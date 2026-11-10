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

from . import files
from .adapter_readout import AdapterReadout
from .codetext import crossfit_codetext
from .common import Folds
from .isotonic import crossfit_isotonic, drop_inner_split, rename_iso
from .lat import crossfit_lat
from .probe import crossfit_family, crossfit_mlp, crossfit_prompt
from .recipe import RecipeTable
from .surrogate import SurrogateTrainer, surrogate_features
from .unsupervised import agreement_scores, ast_cluster_scores, tl_scores
from .verbal import v1_parse_report, v1_scores, v1_train_scores, v2_scores

POPULATIONS = {"label_validity": K.LABEL_VALIDITY_BENCHMARKS, "lcb": ("lcb_v6",)}
SUITES_BY_POP = {"label_validity": ("E", "O"), "lcb": ("lcb_label", "lcb_public", "lcb_full")}  # selection suite first
ISO_BASES = ("SZ_V1", "SZ_V1_drop", "SZ_V2", "TL_geo", "TL_min")
EXTRA_NAMES = ("SZ_V1_drop", "AGREE_problem")
LORA_FAMILY = ("ST", "ST_r1", "ST_r4", "ST_r16", "ST_head", "SR")
STUDY_LIKE = ("MOCK", "SMOKE")


def _populations(cfg: RunConfig) -> list[tuple[str, tuple[str, ...]]]:
    out = []
    for pop, benches in POPULATIONS.items():
        present = tuple(b for b in benches if b in cfg.benchmarks)
        if present:
            out.append((pop, present))
    return out


def _is_primary(model_key: str) -> bool:
    return model_key in K.PRIMARY_MODELS or model_key in STUDY_LIKE


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
        self._real = None
        self._surrogate = None
        suites = cfg.extra.get("suites") or SUITES_BY_POP[population]
        self.suites = [s for s in suites if s in data.labels]
        self.primary = _is_primary(model_key)

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
        mlp_ok = self.want("MLP") and (self.explicit or (self.primary and suite == "E" and seed == 0
                                                          and p == "label_validity"))
        if fam_names or mlp_ok:
            fam = crossfit_family(d, plan, suite, m, p, want=fam_names + (("MLP",) if mlp_ok else ()))
            for n in fam_names:
                w.scores(m, p, n, suite, seed, fam.scores.get(n, []))
                w.fits(m, p, n, suite, seed, fam.fits.get(n, []))
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

    def table(self, seed: int) -> RecipeTable:
        if seed not in self.tables:
            t = RecipeTable()
            ext = self.cfg.extra.get("recipes")
            if isinstance(ext, str) and Path(ext).exists():
                t = RecipeTable.load(Path(ext))
            elif isinstance(ext, dict):
                t = RecipeTable.from_dict(ext)
            elif self.pop != "label_validity" and self.recipes_path(seed, "label_validity").exists():
                t = RecipeTable.load(self.recipes_path(seed, "label_validity"))
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
                lambda tok: provider(self.cfg, self.layout, self.model, self.benches, self.data.sample_uids, tok),
                self.layout.answer_tokens)
        with (self._real.sr() if kind == "sr" else self._real.st(rank=rank, head=head)) as t:
            yield t

    def lora_seeds(self) -> list[int]:
        if self.primary and self.pop == "label_validity":
            return self.seeds
        return self.seeds[:1]

    def run_lora(self) -> None:
        names = [n for n in LORA_FAMILY if self.want(n)]
        if not names:
            return
        for seed in self.lora_seeds():
            plan = self.plans[seed]
            suites = list(self.suites) if seed == self.seeds[0] else [s for s in self.suites if s == "E"]
            if not suites:
                continue
            inner = self.primary and self.pop == "label_validity" and seed == self.seeds[0]
            if "ST" in names or any(n.startswith("ST_") for n in names) or "SR" in names:
                self._run_st(seed, plan, suites, inner, "ST" in names)
            if "SR" in names and seed == self.seeds[0]:
                self._run_sr(seed, plan, suites)
            if seed == self.seeds[0] and self.pop == "label_validity" and "E" in suites and (
                    self.explicit or self.model in K.CAPACITY_MODELS or self.model in STUDY_LIKE):
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
                                    max_steps=self.cfg.lora_max_steps)
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
                if self.cfg.backend == "mock":
                    return None
                return str(self.layout.adapters(m) / f"sr_{p}_{su}_seed{s}_fold{f}")
            with self.trainer("sr") as tr:
                res = AdapterReadout("SR", tr, table, keep_insample=False, max_steps=self.cfg.lora_max_steps,
                                     save_path_fn=save_path).crossfit_full(d, plan, suite, m, p)
            w.scores(m, p, "SR", suite, seed, res.scores)
            w.fits(m, p, "SR", suite, seed, res.fits)
            if self.cfg.backend != "mock" and self.layout.adapters(m).exists():
                w.tree(self.layout.adapters(m))


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


def run(cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport:
    report = StageReport(stage="readouts", ok=True)
    writer = files.Writer(cfg, layout, manifest, report)
    planned: list[str] = []
    for model_key in cfg.models:
        if model_key in cfg.generation_only_models:
            report.skipped.append(f"{model_key}: generation only")
            continue
        for population, benches in _populations(cfg):
            if dry_run:
                planned += _planned(cfg, layout, model_key, population)
                continue
            data = files.load_readout_data(layout, model_key, benches)
            if data is None:
                report.notes.append(f"{model_key}/{population}: no capture index; skipped")
                continue
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
