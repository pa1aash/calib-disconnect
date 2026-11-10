"""Readouts stage (`pipeline.readouts.stage:run`): fit and score every readout of design section 7.

For each model (except `cfg.generation_only_models`) and each population present in `cfg.benchmarks`
(label_validity: HumanEval+ and MBPP+; lcb: LiveCodeBench), the stage assembles `ReadoutData` from the
capture, label, extraction, and agreement files, loads the fold plans, fits every requested readout
(`cfg.readouts`, empty = all) under each label suite, and writes score parquet and fit JSON files
through `layout.scores` and `layout.fits`. Every file goes into the manifest.

Which fold seeds each readout runs on (`cfg.fold_seeds`, section 7 and 9):
  * non-LoRA readouts: every requested seed (the stability check on seeds 1 and 2);
  * S^T on a primary model (and the MOCK and SMOKE models): every requested seed under suite E, label
    validity population; other suites, populations, and models: the first requested seed (0).
Inner adapters (four per outer fold and suite, the isotonic map's training scores) are fit for primary
models on the label-validity population at fold seed 0; every other S^T map is fit on the final
adapter's in-sample training-fold scores. The recipe is selected per (fold seed, outer fold) on the first
inner split under the first suite (E; for LiveCodeBench lcb_label unless a recipe table is supplied by
`cfg.extra["recipes"]` or exists for the label-validity population), saved to
`readouts/<model>/<population>/ST/recipes_seed<s>.json`, and reused for the other suites, S^R, and the
ladder. Backend "mock" uses the surrogate trainer through the same plumbing.

Checkpoints (RECIPE_SOURCE: B1..B6, T1, T2, S1, C3, C4) reuse the recipe of their source model, read from its
FitRecords; a missing source recipe raises `MissingRecipeError` unless `cfg.extra["allow_own_recipe"]` is set
(the pilot model T1). LiveCodeBench reuses the label-validity recipe the same way. The capacity-ladder ranks 1
and 4 reuse the rank-16 recipe (alpha stays twice the rank). Before the first trained readout of an
architecture class the stage runs the mask unit test (`gate.run_mask_gate`) and refuses to train if it fails.

Extra output names beyond READOUTS (see CONTRACT_REQUESTS.md): SZ_V1_drop, AGREE_problem, and the
isotonic variants iso:ST_inner234, iso:ST_insample, iso:SZ_V1_drop.
"""

from __future__ import annotations

import contextlib
import dataclasses
from pathlib import Path

import numpy as np

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData, RunConfig, StageReport
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import LABEL_SUITES_LCB, LABEL_SUITES_LV, READOUTS, FoldPlan, iso

from . import files, fresh
from .adapter_readout import AdapterReadout
from .codetext import crossfit_codetext
from .common import Folds
from .isotonic import crossfit_isotonic, drop_inner_split, rename_iso
from .lat import crossfit_lat
from .probe import FittedProbe, crossfit_family, crossfit_mlp, crossfit_prompt
from .gate import MaskTestFailed
from .recipe import Recipe, RecipeTable
from .surrogate import SurrogateTrainer, apply_saved_surrogate, surrogate_features
from .unsupervised import agreement_scores, ast_cluster_scores, tl_scores
from .verbal import v1_parse_report, v1_scores, v1_train_scores, v2_scores

POPULATIONS = {"label_validity": K.LABEL_VALIDITY_BENCHMARKS, "lcb": ("lcb_v6",)}
SUITES_BY_POP = {"label_validity": ("E", "O"), "lcb": ("lcb_label", "lcb_public", "lcb_full")}  # selection suite first
ISO_BASES = ("SZ_V1", "SZ_V1_drop", "SZ_V2", "TL_geo", "TL_min")
EXTRA_NAMES = ("SZ_V1_drop", "AGREE_problem")
LORA_FAMILY = ("ST", "ST_r1", "ST_r4", "ST_r16", "ST_head", "SR")
STUDY_LIKE = ("MOCK", "SMOKE")
# Checkpoints that reuse the recipe of a source model, per (fold seed, outer fold) (design 7.4): bases from the
# instruct model of their family, trajectory checkpoints and the Olmo base from P3, thinking-on from thinking-off.
RECIPE_SOURCE = {"B1": "P1", "B2": "P2", "B3": "P3", "B4": "P4", "B5": "P5", "B6": "P6", "T1": "P3", "T2": "P3",
                 "S1": "P1", "C3": "C1", "C4": "C2"}


class PopulationCoverageError(RuntimeError):
    """Labeled problems are missing from the fold plan or the reference checks (never dropped silently)."""


class MissingRecipeError(RuntimeError):
    """A checkpoint's source recipe is absent and cfg.extra["allow_own_recipe"] is not set."""


def _populations(cfg: RunConfig) -> list[tuple[str, tuple[str, ...]]]:
    out = []
    for pop, benches in POPULATIONS.items():
        present = tuple(b for b in benches if b in cfg.benchmarks)
        if present:
            out.append((pop, present))
    return out


def _is_primary(model_key: str) -> bool:
    return model_key in K.PRIMARY_MODELS or model_key in STUDY_LIKE


def _st_primary(model_key: str) -> bool:
    """S^T seed refits (fold seeds 0, 1, 2) and inner adapters: the primary models and the pilot model T1."""
    return _is_primary(model_key) or model_key == K.PILOT_MODEL


# Which LoRA readouts run for which model (G18; design 3.2, 7.4, 7.5, 7.11, 10).
def st_allowed(model_key: str, population: str) -> bool:
    if model_key in ("X1", "X2"):
        return False
    return population != "lcb" or _is_primary(model_key) or model_key == "S1"


def sr_allowed(model_key: str, population: str) -> bool:
    if model_key in STUDY_LIKE:
        return True
    return (population == "label_validity" and model_key in ("P1", "S1")) or (population == "lcb" and model_key == "S1")


def ladder_allowed(model_key: str, population: str) -> bool:
    return population == "label_validity" and (model_key in K.CAPACITY_MODELS or model_key in STUDY_LIKE)


class _Ctx:
    """Everything one (model, population) needs."""

    def __init__(self, cfg: RunConfig, layout: RunLayout, writer: files.Writer, report: StageReport, model_key: str,
                 population: str, benches: tuple[str, ...], data: ReadoutData):
        self.cfg, self.layout, self.w, self.report = cfg, layout, writer, report
        self.model, self.pop, self.benches, self.data = model_key, population, benches, data
        self.plans: dict[int, FoldPlan] = {}
        for s in (cfg.fold_seeds or (0,)):
            p = files.load_plan(layout, population, s)
            if p is None:
                report.notes.append(f"no fold plan for {population} seed {s}; seed skipped")
            else:
                self.plans[s] = p
        self.seeds = sorted(self.plans)
        self.tables: dict[int, RecipeTable] = {}
        self.recipe_origin = "selected here"
        self.fresh_only = False
        self._real = None
        self._surrogate = None
        suites = cfg.extra.get("suites") or SUITES_BY_POP[population]
        self.suites = [s for s in suites if s in data.labels]
        self.primary = _is_primary(model_key)
        self.st_primary = _st_primary(model_key)

    # -- selection of what to run ------------------------------------------------------------------
    def want(self, name: str) -> bool:
        r = self.cfg.readouts
        return not r or name in r or iso(name) in r

    @property
    def explicit(self) -> bool:
        return bool(self.cfg.readouts)

    # -- unsupervised and zero-shot ----------------------------------------------------------------
    def run_unsupervised(self) -> dict[str, list]:
        m, p, w, d = self.model, self.pop, self.w, self.data
        rows: dict[str, list] = {}
        if any(self.want(n) for n in ("TL_geo", "TL_min", "TL_sum")):
            for name, r in tl_scores(d, m, p).items():
                if self.want(name):
                    rows[name] = r
        if self.want("SZ_V2") and d.capture:
            rows["SZ_V2"] = v2_scores(d, m, p)
        if (self.want("AGREE") or self.want("AGREE_problem")) and d.agreement_outputs is not None:
            for name, r in agreement_scores(d, m, p).items():
                if self.want(name):
                    rows[name] = r
        elif self.want("AGREE") and d.agreement_outputs is None:
            self.report.notes.append(f"{m}/{p}: no agreement outputs; AGREE skipped")
        if self.want("AST") and d.code_texts is not None:
            rows["AST"] = ast_cluster_scores(d, m, p)
        for name, r in rows.items():
            w.scores(m, p, name, None, None, r)
            if name.startswith("TL_") or name == "AGREE":
                self.report.metrics.setdefault("missing_counts", {}).setdefault(f"{m}/{p}", {})[name] = {
                    "n": len(r), "missing": sum(x.missing for x in r)}
        return rows

    def run_zero_shot_seed(self, seed: int, plan: FoldPlan, unsup: dict[str, list]) -> None:
        m, p, w, d = self.model, self.pop, self.w, self.data
        bases: dict[str, tuple[list, dict | None]] = {}
        if (self.want("SZ_V1") or self.want("SZ_V1_drop")) and d.capture:
            if self.want("SZ_V1"):
                r = v1_scores(d, plan, m, p)
                w.scores(m, p, "SZ_V1", None, seed, r)
                bases["SZ_V1"] = (r, v1_train_scores(d, plan, m, p))
            if self.want("SZ_V1_drop"):
                r = v1_scores(d, plan, m, p, drop_missing=True)
                w.scores(m, p, "SZ_V1_drop", None, seed, r)
                bases["SZ_V1_drop"] = (r, v1_train_scores(d, plan, m, p, drop_missing=True))
            if seed == self.seeds[0]:
                rep = v1_parse_report(d)
                w.json(self.layout.scores(m, p, "SZ_V1", None, None).parent / "parse_rate.json", rep)
                self.report.metrics.setdefault("v1", {})[f"{m}/{p}"] = rep
        for name in ("SZ_V2", "TL_geo", "TL_min"):
            if name in unsup:
                bases[name] = (unsup[name], None)
        for suite in self.suites:
            for name, (rows, train) in bases.items():
                if self.want(name):
                    w.scores(m, p, iso(name), suite, seed, crossfit_isotonic(rows, d, plan, suite, train))

    # -- probes and other non-LoRA supervised readouts ------------------------------------------------
    def run_probes(self, seed: int, plan: FoldPlan, suite: str) -> None:
        m, p, w, d = self.model, self.pop, self.w, self.data
        fam_names = tuple(n for n in ("P", "P2", "P3", "Pmulti", "P2_single_split") if self.want(n))
        mlp_ok = self.want("MLP") and self.primary and (self.explicit or (suite == "E" and seed == 0
                                                                         and p == "label_validity"))
        if self.want("MLP") and not self.primary:
            self.report.notes.append(f"{m}: MLP probe runs on primary models only")
        if fam_names or mlp_ok:
            fam = crossfit_family(d, plan, suite, m, p, want=fam_names + (("MLP",) if mlp_ok else ()))
            for n in fam_names:
                w.scores(m, p, n, suite, seed, fam.scores.get(n, []))
                w.fits(m, p, n, suite, seed, fam.fits.get(n, []))
            if sr_allowed(m, p):   # G4: persist P for reading A (the probe read on the fresh sets)
                for (f, n), fp in fam.fitted.items():
                    if n == "P":
                        pp = fresh.probe_path(self.layout, m, p, suite, seed, f)
                        fp.save(pp)
                        w._register(pp)
            if mlp_ok:
                s, f = crossfit_mlp(d, plan, suite, m, p, layer_by_fold=fam.best_single_layer)
                w.scores(m, p, "MLP", suite, seed, s)
                w.fits(m, p, "MLP", suite, seed, f)
        if self.want("PROMPT"):
            s, f = crossfit_prompt(d, plan, suite, m, p)
            w.scores(m, p, "PROMPT", suite, seed, s)
            w.fits(m, p, "PROMPT", suite, seed, f)
        if self.want("CODETEXT") and d.code_texts is not None:
            s, f = crossfit_codetext(d, plan, suite, m, p)
            w.scores(m, p, "CODETEXT", suite, seed, s)
            w.fits(m, p, "CODETEXT", suite, seed, f)
        if self.want("LAT"):
            s, f = crossfit_lat(d, plan, suite, m, p)
            w.scores(m, p, "LAT", suite, seed, s)
            w.fits(m, p, "LAT", suite, seed, f)

    # -- LoRA family -----------------------------------------------------------------------------------
    def recipes_path(self, seed: int, population: str | None = None) -> Path:
        return self.layout.root / "readouts" / self.model / (population or self.pop) / "ST" / f"recipes_seed{seed}.json"

    def source_model(self) -> str | None:
        return RECIPE_SOURCE.get(self.model)

    def _recipes_from_fits(self, source: str, seed: int) -> RecipeTable:
        """Recipes of `source` for fold seed `seed`, read from its label-validity ST FitRecords (suite E)."""
        t = RecipeTable()
        path = self.layout.fits(source, "label_validity", "ST", "E", seed)
        if path.exists():
            for fr in files.json_load_fits(path):
                sel = fr.selected
                t.put(seed, fr.outer_fold, Recipe(
                    lr=sel["lr"], steps=sel["steps"], n_train_inner=sel["n_train_inner"],
                    epoch_fraction=sel["epoch_fraction"], schedule_epochs=sel["schedule_epochs"],
                    inner_val_logloss=fr.inner_val_logloss, base_rate_logloss=fr.base_rate_logloss,
                    retried=fr.retried, flagged=fr.flagged))
        return t

    def table(self, seed: int) -> RecipeTable:
        """The recipe table for this model. Order: an explicit cfg.extra["recipes"]; the source model's
        FitRecords (checkpoints, and LiveCodeBench from the label-validity fits); otherwise empty, which
        means "select here", allowed only for models without a source (primary models on the label-validity
        population) or when cfg.extra["allow_own_recipe"] is set (the pilot model T1)."""
        if seed not in self.tables:
            t = RecipeTable()
            ext = self.cfg.extra.get("recipes")
            self.recipe_origin = "selected here"
            if isinstance(ext, str) and Path(ext).exists():
                t, self.recipe_origin = RecipeTable.load(Path(ext)), f"file {Path(ext).name}"
            elif isinstance(ext, dict):
                t, self.recipe_origin = RecipeTable.from_dict(ext), "cfg.extra"
            else:
                src = self.source_model()
                if src is not None or self.pop != "label_validity":
                    t = self._recipes_from_fits(src or self.model, seed)
                    self.recipe_origin = f"{src or self.model} FitRecords"
                    if not t.recipes:
                        if not self.cfg.extra.get("allow_own_recipe"):
                            raise MissingRecipeError(
                                f"{self.model}/{self.pop}: no recipe of {src or self.model} for fold seed {seed}; fit its "
                                "S^T first or set cfg.extra['allow_own_recipe']")
                        self.recipe_origin = "selected here (allow_own_recipe)"
            self.tables[seed] = t
        return self.tables[seed]

    def _save_table(self, seed: int) -> None:
        t = self.table(seed)
        if t.recipes:
            t.save(self.recipes_path(seed))
            self.w._register(self.recipes_path(seed))

    @contextlib.contextmanager
    def trainer(self, kind: str, rank: int = K.LORA_RANK, head: bool = False):
        """Yield an AdapterTrainer: the surrogate on the mock backend, else a model-backed trainer."""
        if self.cfg.backend == "mock":
            if self._surrogate is None:
                self._surrogate = SurrogateTrainer(surrogate_features(self.data))
            yield self._surrogate
            return
        if self._real is None:
            from .real_backend import RealBackend, load_layouts_provider
            provider = load_layouts_provider(self.cfg)
            self._real = RealBackend.from_pretrained(
                self.cfg, self.model,
                lambda tok, mdl: provider(self.cfg, self.layout, self.model, self.benches, self.data.sample_uids, tok, mdl),
                self.layout.answer_tokens)
        if not self._real.gate_done:   # 7.12: refuse to train unless the mask test passes for this class
            from .gate import arch_key
            rp = self.layout.config_dir / f"mask_test_{arch_key(self._real.model)}.json"
            if self.fresh_only and not rp.exists():
                raise MaskTestFailed(f"no mask test report {rp.name}: run the frozen S^R training before its fresh sets")
            self._real.mask_gate(rp, register=self.w._register)
        with (self._real.sr() if kind == "sr" else self._real.st(rank=rank, head=head)) as t:
            yield t

    def lora_seeds(self) -> list[int]:
        if self.st_primary and self.pop == "label_validity":
            return self.seeds
        return self.seeds[:1]

    def run_lora(self) -> None:
        names = [n for n in LORA_FAMILY if self.want(n)]
        allowed = {"ST": st_allowed(self.model, self.pop), "SR": sr_allowed(self.model, self.pop)}
        for n in ("ST_r1", "ST_r4", "ST_r16", "ST_head"):
            allowed[n] = ladder_allowed(self.model, self.pop) and allowed["ST"]
        dropped = [n for n in names if not allowed[n]]
        if dropped and self.explicit:
            self.report.notes.append(f"{self.model}/{self.pop}: {dropped} not run for this model's role")
        names = [n for n in names if allowed[n]]
        if not names:
            return
        for seed in self.lora_seeds():
            plan = self.plans[seed]
            suites = list(self.suites) if seed == self.seeds[0] else [s for s in self.suites if s == "E"]
            if not suites:
                continue
            inner = self.st_primary and self.pop == "label_validity" and seed == self.seeds[0]
            if "ST" in names or any(n.startswith("ST_") for n in names) or "SR" in names:
                self._run_st(seed, plan, suites, inner, "ST" in names)
            if "SR" in names and seed == self.seeds[0]:
                self._run_sr(seed, plan, suites)
            if seed == self.seeds[0] and "E" in suites and any(n.startswith("ST_") for n in names):
                self._run_ladder(seed, plan)

    def _have_recipes(self, seed: int, plan: FoldPlan, suite: str) -> bool:
        return self.table(seed).has_seed(seed, Folds(self.data, plan, suite).outer_folds)

    def _run_st(self, seed: int, plan: FoldPlan, suites: list[str], inner: bool, emit: bool) -> None:
        m, p, w, d = self.model, self.pop, self.w, self.data
        from .recipe import select_recipes
        for suite in suites:
            table = self.table(seed)
            select = not self._have_recipes(seed, plan, suite)
            if not emit:
                if select:   # S^R or the ladder needs a recipe: select it, nothing else
                    with self.trainer("st") as tr:
                        for f, rec in select_recipes(tr, Folds(d, plan, suite), max_steps=self.cfg.lora_max_steps).items():
                            table.put(seed, f, rec)
                    self._save_table(seed)
                break
            with self.trainer("st") as tr:
                ar = AdapterReadout("ST", tr, table, select=select, inner_adapters=inner,
                                    max_steps=self.cfg.lora_max_steps,
                                    extra_selected={"recipe_source": self.recipe_origin})
                res = ar.crossfit_full(d, plan, suite, m, p)
            if select:
                self._save_table(seed)
            w.scores(m, p, "ST", suite, seed, res.scores)
            w.fits(m, p, "ST", suite, seed, res.fits)
            if not self.want("ST"):
                continue
            if inner:
                w.scores(m, p, iso("ST"), suite, seed, crossfit_isotonic(res.scores, d, plan, suite, res.inner_train_scores))
                w.scores(m, p, iso("ST_inner234"), suite, seed, rename_iso(crossfit_isotonic(
                    res.scores, d, plan, suite, drop_inner_split(res.inner_train_scores, d, plan, 0)), "ST_inner234"))
                w.scores(m, p, iso("ST_insample"), suite, seed, rename_iso(crossfit_isotonic(
                    res.scores, d, plan, suite, res.insample_train_scores), "ST_insample"))
            else:
                w.scores(m, p, iso("ST"), suite, seed, crossfit_isotonic(res.scores, d, plan, suite, res.insample_train_scores))
                self.report.notes.append(f"{m}/{p}/{suite}/seed{seed}: iso:ST map fit on in-sample training-fold scores")

    def _run_ladder(self, seed: int, plan: FoldPlan) -> None:
        m, p, w, d = self.model, self.pop, self.w, self.data
        table = self.table(seed)
        if not self._have_recipes(seed, plan, "E"):
            self.report.notes.append(f"{m}: capacity ladder needs the E-suite recipe; run ST first")
            return
        for rank in K.CAPACITY_RANKS:
            name = f"ST_r{rank}"
            if not self.want(name):
                continue
            if rank == K.LORA_RANK:   # same spec, recipe, and seed as ST: an alias, not a refit
                src = w.layout.scores(m, p, "ST", "E", seed)
                if src.exists():
                    rows = [dataclasses.replace(r, readout=name) for r in files.read_scores(src)]
                    w.scores(m, p, name, "E", seed, rows)
                    fits = files.json_load_fits(w.layout.fits(m, p, "ST", "E", seed))
                    w.fits(m, p, name, "E", seed, [dataclasses.replace(f, readout=name, selected={**f.selected, "alias_of": "ST"}) for f in fits])
                    continue
            with self.trainer("st", rank=rank) as tr:
                res = AdapterReadout(name, tr, table, max_steps=self.cfg.lora_max_steps,
                                     keep_insample=False, extra_selected={"rank": rank}).crossfit_full(d, plan, "E", m, p)
            w.scores(m, p, name, "E", seed, res.scores)
            w.fits(m, p, name, "E", seed, res.fits)
        if self.want("ST_head"):
            with self.trainer("st", head=True) as tr:
                res = AdapterReadout("ST_head", tr, table, max_steps=self.cfg.lora_max_steps, keep_insample=False,
                                     extra_selected={"head": "linear on the final p3 state"}).crossfit_full(d, plan, "E", m, p)
            w.scores(m, p, "ST_head", "E", seed, res.scores)
            w.fits(m, p, "ST_head", "E", seed, res.fits)

    def _run_sr(self, seed: int, plan: FoldPlan, suites: list[str]) -> None:
        m, p, w, d = self.model, self.pop, self.w, self.data
        table = self.table(seed)
        if not self._have_recipes(seed, plan, suites[0]):
            self._run_st(seed, plan, suites[:1], False, False)
        for suite in suites:
            def save_path(s, f, su):
                return str(fresh.sr_adapter_path(self.layout, m, p, su, s, f, surrogate=self.cfg.backend == "mock"))
            with self.trainer("sr") as tr:
                res = AdapterReadout("SR", tr, table, keep_insample=False, max_steps=self.cfg.lora_max_steps,
                                     save_path_fn=save_path).crossfit_full(d, plan, suite, m, p)
            w.scores(m, p, "SR", suite, seed, res.scores)
            w.fits(m, p, "SR", suite, seed, res.fits)
            if self.layout.adapters(m).exists():
                w.tree(self.layout.adapters(m))

    # -- reading A: fresh sets (G4) -------------------------------------------------------------------
    def run_fresh(self, only: str | None = None) -> None:
        if not sr_allowed(self.model, self.pop) or not (self.want("SR") or self.want("P")):
            return
        m, p, w = self.model, self.pop, self.w
        for fs in fresh.discover_fresh_sets(self.layout, m, self.benches):
            if only is not None and fs.gen_set != only:
                continue
            data = files.load_readout_data(self.layout, m, self.benches, fs.gen_set)
            if data is None:
                self.report.notes.append(f"{m}/{p}/{fs.gen_set}: no capture")
                continue
            pp = fresh.probe_path(self.layout, m, p, fs.suite, fs.seed, fs.fold)
            if self.want("P"):
                if pp.exists():
                    w.scores(m, p, "P", fs.suite, fs.seed, fresh.probe_rows(data, FittedProbe.load(pp), m, p, fs), fs.gen_set)
                else:
                    self.report.notes.append(f"{m}/{p}/{fs.gen_set}: no persisted probe at {pp.name}")
            if not self.want("SR"):
                continue
            mock = self.cfg.backend == "mock"
            ap = fresh.sr_adapter_path(self.layout, m, p, fs.suite, fs.seed, fs.fold, surrogate=mock)
            if not ap.exists():
                self.report.notes.append(f"{m}/{p}/{fs.gen_set}: no saved S^R adapter {ap.name}")
                continue
            if mock:
                z = apply_saved_surrogate(ap, surrogate_features(data))
            else:
                from .real_backend import load_layouts_provider
                from .rtuning import score_rtuning
                with self.trainer("sr") as tr:
                    tr.mlm.load_adapter(ap)
                    lays = load_layouts_provider(self.cfg)(self.cfg, self.layout, m, self.benches, data.sample_uids,
                                                           self._real.tok, self._real.model, gen_set=fs.gen_set)
                    sc = score_rtuning(self._real.model, tr.mlm, [(l.prompt_ids, l.completion_ids) for l in lays],
                                       self._real.rtuning_tokens, batch_size=tr.eval_batch, pad_id=self._real.pad_id,
                                       own_suffix=True)
                z = np.array([x.logit for x in sc])
            w.scores(m, p, "SR", fs.suite, fs.seed, fresh.sr_rows(data, z, m, p, fs), fs.gen_set)


def _planned(cfg: RunConfig, layout: RunLayout, model_key: str, population: str) -> list[str]:
    suites = SUITES_BY_POP[population]
    seeds = cfg.fold_seeds or (0,)
    names = [n for n in READOUTS if not cfg.readouts or n in cfg.readouts]
    out = []
    for n in names:
        sup = n in ("P", "P2", "P3", "Pmulti", "P2_single_split", "MLP", "PROMPT", "CODETEXT", "LAT") or n in LORA_FAMILY
        if sup:
            sd = seeds if (n not in LORA_FAMILY or (_is_primary(model_key) and population == "label_validity")) else seeds[:1]
            out += [str(layout.scores(model_key, population, n, s, sd_).relative_to(layout.root)) for s in suites for sd_ in sd]
        else:
            out.append(str(layout.scores(model_key, population, n, None, None).relative_to(layout.root)))
    return out


def check_coverage(layout: RunLayout, model_key: str, population: str, data: ReadoutData, seeds) -> None:
    """Every problem with a label in the population must be in the fold plan of each fold seed and, for the
    label-validity population, in the reference checks. Raises PopulationCoverageError; never drops silently."""
    labeled = [i for i in range(len(data.sample_uids)) if any(int(v[i]) != files.NO_LABEL for v in data.labels.values())]
    by_bench: dict[str, set[str]] = {}
    for i in labeled:
        by_bench.setdefault(data.sample_uids[i].split("|")[2], set()).add(data.problem_ids[i])

    def missing(have: set[str]) -> dict[str, list[str]]:
        return {b: sorted(ps - have) for b, ps in by_bench.items() if ps - have}

    for s in seeds:
        plan = files.load_plan(layout, population, s)
        if plan is None:
            continue
        miss = missing(set(plan.assignment))
        if miss:
            raise PopulationCoverageError(
                f"{model_key}/{population}: the fold plan of seed {s} lacks labeled problems: "
                + "; ".join(f"{b}: {len(v)} of {len(by_bench[b])} (first {v[0]})" for b, v in sorted(miss.items())))
    if population == "label_validity":
        rc = files.reference_problem_ids(layout)
        if rc is not None:
            miss = missing(rc)
            if miss:
                raise PopulationCoverageError(
                    f"{model_key}/{population}: data/reference_checks.parquet lacks labeled problems: "
                    + "; ".join(f"{b}: {len(v)} of {len(by_bench[b])} (first {v[0]})" for b, v in sorted(miss.items())))


def _run_timing(cfg: RunConfig, layout: RunLayout, report: StageReport, dry_run: bool) -> StageReport:
    """cfg.extra["timing_only"]: LoRA step timing on the "timing" generation set; writes no score, adapter, or probe.
    Exempt from generation_only_models."""
    from . import timing
    n_steps = int(cfg.lora_max_steps or 10)
    report.notes.append("timing_only: masked-LoRA step timing; no score, adapter, or probe is written")
    for model_key in cfg.models:
        for population, benches in _populations(cfg):
            uids = timing.timing_uids(layout, model_key, benches)
            if dry_run:
                report.notes.append(f"would time {n_steps} LoRA steps of {model_key}/{population} on {len(uids)} timing samples")
                continue
            if cfg.backend == "mock":
                report.notes.append(f"{model_key}: mock backend has no model; nothing timed")
                continue
            if not uids:
                report.notes.append(f"{model_key}/{population}: no timing generations")
                continue
            from .real_backend import RealBackend, load_layouts_provider
            provider = load_layouts_provider(cfg)
            backend = RealBackend.from_pretrained(
                cfg, model_key,
                lambda tok, mdl: provider(cfg, layout, model_key, benches, uids, tok, mdl, gen_set=timing.TIMING_SET),
                layout.answer_tokens)
            res = timing.time_lora_steps(backend, n_steps)
            report.metrics.setdefault("timing", {})[f"{model_key}/{population}"] = res
            timing.write_timing_log(layout, model_key, res)
    return report


def run(cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport:
    report = StageReport(stage="readouts", ok=True)
    if cfg.extra.get("timing_only"):
        return _run_timing(cfg, layout, report, dry_run)
    writer = files.Writer(cfg, layout, manifest, report)
    gen_set = str(cfg.extra.get("gen_set", "frozen"))
    fresh_only = gen_set.startswith("fresh:")
    planned: list[str] = []
    for model_key in cfg.models:
        if model_key in cfg.generation_only_models:
            report.skipped.append(f"{model_key}: generation only")
            continue
        for population, benches in _populations(cfg):
            if dry_run:
                planned += ([str(layout.scores(model_key, population, "SR", None, None, gen_set).relative_to(layout.root))]
                            if fresh_only else _planned(cfg, layout, model_key, population))
                continue
            if fresh_only:   # N3: score the fresh set only; no frozen score, probe, or adapter is touched
                ctx = _Ctx(cfg, layout, writer, report, model_key, population, benches,
                           ReadoutData(sample_uids=[], problem_ids=[], labels={}))
                ctx.fresh_only = True
                try:
                    ctx.run_fresh(only=gen_set)
                except (MaskTestFailed, MissingRecipeError):
                    raise
                except RuntimeError as e:
                    report.ok = False
                    report.notes.append(f"{model_key}/{population}: {e}")
                continue
            data = files.load_readout_data(layout, model_key, benches)
            if data is None:
                report.notes.append(f"{model_key}/{population}: no capture index; skipped")
                continue
            check_coverage(layout, model_key, population, data, cfg.fold_seeds or (0,))   # N1, before any exclusion
            if population == "label_validity":   # G1: problems valid under BOTH suites, for every suite
                n_removed = files.apply_reference_exclusions(data, files.valid_label_validity_problems(layout))
                report.metrics.setdefault("reference_excluded_samples", {})[f"{model_key}/{population}"] = n_removed
            ctx = _Ctx(cfg, layout, writer, report, model_key, population, benches, data)
            if not ctx.seeds:
                report.ok = False
                report.notes.append(f"{model_key}/{population}: no fold plan found")
                continue
            try:
                unsup = ctx.run_unsupervised()
                for seed in ctx.seeds:
                    plan = ctx.plans[seed]
                    ctx.run_zero_shot_seed(seed, plan, unsup)
                    for suite in ctx.suites:
                        ctx.run_probes(seed, plan, suite)
                ctx.run_lora()
                ctx.run_fresh()
            except (MissingRecipeError, MaskTestFailed):
                raise
            except RuntimeError as e:   # for example a missing token-layout provider for the real backend
                report.ok = False
                report.notes.append(f"{model_key}/{population}: {e}")
    if dry_run:
        report.metrics["planned"] = planned
        report.notes.append("dry run: nothing computed or written")
        return report
    manifest.save(layout.manifest)
    report.metrics["n_outputs"] = len(report.outputs)
    return report
