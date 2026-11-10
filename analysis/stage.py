"""Analysis stage (STAGES["analysis"] = "analysis.stage:run"). The only module with file IO.

Inputs (all under the run root, read only):
- ReadoutScore parquet files under readouts/ (RunLayout.scores scheme; the columns, not the path,
  identify model, population, readout, label suite, and fold seed);
- labels execute/labels/<model>/<benchmark>/frozen.parquet (sample_uid, suite_id, y, source, ...);
- data/reference_checks.parquet: the label-validity population is the set of problems whose reference
  passes both "O" and "E" (excluded is False for both);
- data/folds_<population>_seed0.json (FoldPlan) for the fold-averaged diagnostic, if present.

Outputs: JSON files under analysis/results/<run_id>/ (AnalysisLayout; cfg.extra["analysis_root"]
overrides the analysis root, for tests), each carrying the SHA-256 of the run manifest read at the
start. With cfg.seal_gamma (pilot, section 13), every Gamma cell, Shapley term, residual, decision,
and per-readout metric (from which cells could be derived) is written only to
<run>/sealed/gamma_sealed.json; its SHA-256 goes to <run>/sealed/gamma_sealed.sha256 and both files
are added to the manifest. No sealed value is printed, logged, or returned; analysis/results then
receives only operational outputs (mixed counts, pass-count histograms, tie rates, parse rates,
extraction-failure rates, reference exclusions, the k rule, and the seed-to-seed spread of W for S^T
given as an SD and a range, with no W value and no cell).

Generation shift (section 1.5): for P1 and S1, when ReadoutScore rows exist on fresh generation sets
"fresh:SR_<suite>_seed<s>_fold<f>", the five fold sets of a suite are merged into one fresh set (each
problem in exactly one fold set, else the suite is skipped with a note); labels come from
layout.labels(model, benchmark, <generation set>). Reconciliation (section 2): the checks of the
orchestrator's mapping (analysis.recon_checks), each computed only when its readouts exist, with
paired 95 percent intervals, the diagnostic excluding extraction-failure and truncated samples, and
one verb per paper. Every file written to analysis/results/<run_id>/ is listed with its SHA-256 in
INDEX.json there.

cfg.extra keys: "bootstrap_b" (default B_BOOTSTRAP), "analysis_root", "secondary_budgets" (default
True), "routing" (default True).
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from pipeline.contracts.constants import (B_BOOTSTRAP, BOOTSTRAP_SEED, CAMPOS_TIE_WIDTH, DECISION_INTERVAL_LEVEL,
                                          FOLD_SEEDS, K3_MIN_V1_PARSE_RATE, LABEL_VALIDITY_BENCHMARKS,
                                          PRIMARY_MODELS, R2610_TIE_WIDTH, RECONCILIATION_LEVEL,
                                          SHAPLEY_MARGINAL_LEVEL)
from pipeline.contracts.hashing import config_hash, sha256_file
from pipeline.contracts.interfaces import RunConfig, StageReport
from pipeline.contracts.layout import AnalysisLayout, RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import FoldPlan, MetricResult

from . import metrics as M
from .bootstrap import bca_interval, draw, interval_dict, jackknife_counts, percentile_interval
from . import gap as G
from . import sensitivity as SENS
from . import strata as ST
from .budget import model_budget, pooled_budget, three_player_report
from .decisions import pooled_residual_report, primary_report
from .gap import GapInputs, Scores, per_seed_residual, replace_inputs, subset_inputs, tie_rates
from .generation_shift import GenSet, contrasts, set_rates
from .krule import k_rule_report
from .recon_checks import Term, contrast, run_check
from .reconciliation import paper_verb

PRODUCER = "analysis.stage:run"
POPULATIONS = {"label_validity": ("O", "E"), "lcb": ("lcb_public", "lcb_label")}
LCB_BENCHMARKS = ("lcb_v6",)
FRESH_RE = re.compile(r"^fresh:SR_(.+)_seed(\d+)_fold(\d+)$")
GEN_SHIFT_MODELS = ("P1", "S1")


# ---------------------------------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------------------------------
def _clean(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if hasattr(o, "to_dict") and not isinstance(o, (pd.DataFrame, pd.Series)):
        return _clean(o.to_dict())
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, (float, np.floating)):
        f = float(o)
        return f if math.isfinite(f) else None
    return o


def _write_json(path: Path, obj: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_clean(obj), indent=1, sort_keys=True) + "\n")
    return path


def code_sha256() -> str:
    """SHA-256 over the analysis modules (name and bytes, sorted by name)."""
    h = hashlib.sha256()
    for p in sorted(Path(__file__).resolve().parent.glob("*.py")):
        h.update(p.name.encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


# ---------------------------------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------------------------------
def _problem_of(uid: str) -> str:
    return uid.split("|")[3]


def load_labels(layout: RunLayout, models, benchmarks, gen_sets=("frozen",)) -> pd.DataFrame:
    frames = []
    for m in models:
        for b in benchmarks:
          for gs in gen_sets:
            p = layout.labels(m, b, gs)
            if p.exists():
                df = pd.read_parquet(p)
                df["model_key"] = m
                df["benchmark"] = b
                df["generation_set"] = gs
                frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["sample_uid", "suite_id", "y", "source", "model_key", "benchmark", "problem_id"])
    out = pd.concat(frames, ignore_index=True)
    out["problem_id"] = out["sample_uid"].map(_problem_of)
    return out


def valid_lv_problems(layout: RunLayout) -> tuple[list[str], dict]:
    rc = pd.read_parquet(layout.reference_checks)
    rc = rc[rc["suite_id"].isin(["O", "E"])]
    ok = rc.groupby("problem_id").apply(
        lambda g: set(g.loc[~g["excluded"].astype(bool), "suite_id"]) >= {"O", "E"}, include_groups=False)
    valid = sorted(ok[ok].index)
    excl = {s: int(rc[(rc["suite_id"] == s) & rc["excluded"].astype(bool)]["problem_id"].nunique()) for s in ("O", "E")}
    return valid, {"n_checked": int(rc["problem_id"].nunique()), "n_valid": len(valid), "excluded_per_suite": excl}


def _norm(ls, fs):
    ls = None if ls is None or (isinstance(ls, float) and math.isnan(ls)) else str(ls)
    fs = None if fs is None or (isinstance(fs, float) and math.isnan(fs)) else int(fs)
    return ls, fs


def load_scores(layout: RunLayout) -> tuple[dict, dict, dict]:
    """Returns (frozen, fresh, fresh_sets).
    frozen: (model, population, readout, label_suite, fold_seed) -> rows on the frozen generations.
    fresh: (model, population, readout, label_suite, fresh_suite) -> rows on the fresh set of that
    suite, the union of its fold-specific generation sets "fresh:SR_<suite>_seed<s>_fold<f>".
    fresh_sets: (model, population, fresh_suite) -> sorted generation-set names."""
    frozen: dict[tuple, pd.DataFrame] = {}
    parts: dict[tuple, list] = {}
    sets: dict[tuple, set] = {}
    base = layout.root / "readouts"
    if not base.exists():
        return frozen, {}, {}
    for p in sorted(base.rglob("*.parquet")):
        df = pd.read_parquet(p)
        if df.empty:
            continue
        if "generation_set" not in df:
            df["generation_set"] = "frozen"
        for key, g in df.groupby(["model_key", "population", "readout", "generation_set"], dropna=False):
            ls, fs = _norm(g["label_suite"].iloc[0], g["fold_seed"].iloc[0])
            if key[3] == "frozen":
                frozen[(key[0], key[1], key[2], ls, fs)] = g.reset_index(drop=True)
                continue
            mt = FRESH_RE.match(str(key[3]))
            if mt is None:
                continue
            parts.setdefault((key[0], key[1], key[2], ls, mt.group(1)), []).append(g)
            sets.setdefault((key[0], key[1], mt.group(1)), set()).add(str(key[3]))
    fresh = {k: pd.concat(v, ignore_index=True).drop_duplicates("sample_uid") for k, v in parts.items()}
    return frozen, fresh, {k: sorted(v) for k, v in sets.items()}


def find(scores: dict, model: str, pop: str, readout: str, suite: str | None, seed: int | None):
    for k in ((model, pop, readout, suite, seed), (model, pop, readout, suite, None),
              (model, pop, readout, None, seed), (model, pop, readout, None, None),
              (model, pop, readout, None, 0)):
        if k in scores:
            return scores[k]
    return None


def align(df: pd.DataFrame | None, uids: list[str]) -> Scores | None:
    if df is None:
        return None
    d = df.drop_duplicates("sample_uid").set_index("sample_uid")
    if not set(uids) <= set(d.index):
        return None
    d = d.loc[uids]
    tb = pd.to_numeric(d["rank_tiebreak"], errors="coerce").to_numpy(dtype=np.float64)
    imp = d["imputed"].astype(bool).to_numpy() if "imputed" in d else None
    return Scores(rank_score=d["rank_score"].to_numpy(np.float64), rank_tiebreak=tb,
                  prob=d["prob"].to_numpy(np.float64), imputed=imp)


def fold_of_problem(layout: RunLayout, pop: str, problems: list[str]) -> np.ndarray | None:
    p = layout.folds(pop, 0)
    if not p.exists():
        return None
    plan = FoldPlan.from_dict(json.loads(p.read_text()))
    if not set(problems) <= set(plan.assignment):
        return None
    return np.array([plan.assignment[q] for q in problems], dtype=np.int64)


# ---------------------------------------------------------------------------------------------------
# Per (model, population)
# ---------------------------------------------------------------------------------------------------
class ModelData:
    def __init__(self, model: str, pop: str, suites, labels: pd.DataFrame, problems: list[str]):
        self.model, self.pop, self.suites = model, pop, suites
        lab = labels[(labels["model_key"] == model) & labels["problem_id"].isin(set(problems))
                     & labels["suite_id"].isin(suites)]
        wide = lab.pivot_table(index="sample_uid", columns="suite_id", values="y", aggfunc="first")
        wide = wide.dropna(subset=[s for s in suites if s in wide.columns]) if set(suites) <= set(wide.columns) else wide.iloc[0:0]
        self.uids = sorted(wide.index)
        pos = {q: i for i, q in enumerate(problems)}
        self.n_problems = len(problems)
        self.problem_index = np.array([pos[_problem_of(u)] for u in self.uids], dtype=np.int64)
        self.labels = {s: wide.loc[self.uids, s].to_numpy().astype(np.int8) for s in suites} if self.uids else {}
        self.excluded: dict[str, np.ndarray] = {}
        for s in suites:
            src = lab[lab["suite_id"] == s].drop_duplicates("sample_uid").set_index("sample_uid")
            if not self.uids:
                continue
            src = src.loc[self.uids]
            ef = (src["source"] == "extraction_failure").to_numpy() if "source" in src else np.zeros(len(self.uids), bool)
            tr = (src["failure"] == "truncated").fillna(False).to_numpy(dtype=bool) if "failure" in src else np.zeros(len(self.uids), bool)
            self.excluded[s] = ef | tr
        self.extraction_failed = (self.excluded[suites[-1]] if self.uids else None)

    def scored(self, sc: Scores, suite: str):
        from ._common import make_scored_set
        return make_scored_set(self.problem_index, self.labels[suite], sc.rank_score, sc.rank_tiebreak, sc.prob)


def v1_parse_rate(scores: dict, md: ModelData) -> float | None:
    df = find(scores, md.model, md.pop, "SZ_V1", None, 0)
    if df is None:
        return None
    d = df[df["sample_uid"].isin(set(md.uids))]
    if d.empty:
        return None
    unparsed = d["missing"].astype(bool) | d["imputed"].astype(bool)
    return float(1.0 - unparsed.mean())


def operational(md: ModelData) -> dict:
    out: dict = {"n_samples": len(md.uids)}
    from ._common import make_scored_set
    for s in md.suites:
        s_set = make_scored_set(md.problem_index, md.labels[s], np.zeros(len(md.uids)))
        out[f"counts_{s}"] = M.mixed_counts(s_set, md.n_problems)
        out[f"pass_count_histogram_{s}"] = M.pass_count_histogram(s_set, md.n_problems)
        out[f"pass_rate_{s}"] = float(np.mean(md.labels[s])) if len(md.uids) else None
    if md.extraction_failed is not None and md.extraction_failed.size:
        out["extraction_failure_rate"] = float(np.mean(md.extraction_failed))
    return out


def metrics_rows(scores: dict, md: ModelData, fop, counts) -> list[dict]:
    rows = []
    for (m, pop, readout, suite, seed), df in sorted(scores.items(), key=lambda kv: str(kv[0])):
        if m != md.model or pop != md.pop:
            continue
        sc = align(df, md.uids)
        if sc is None:
            continue
        if suite is not None and suite not in md.suites:
            continue
        for lab in ([suite] if suite is not None else list(md.suites)):
            if lab == "lcb_full" and readout.startswith("AGREE"):
                continue      # section 4: the full-suite labeling sensitivity has no agreement readout
            s = md.scored(sc, lab)
            # Readouts that can be missing for a sample (AGREE for a problem with no agreement inputs,
            # section 4) are scored on the non-missing samples only; never imputed. A non-finite score on
            # a row not flagged missing is an error.
            fin = np.isfinite(s.rank_score)
            n_missing = int((~fin).sum())
            if n_missing:
                flags = df.drop_duplicates("sample_uid").set_index("sample_uid").loc[md.uids, "missing"]
                if not flags.astype(bool).to_numpy()[~fin].all():
                    raise ValueError(f"{m}/{readout}: non-finite rank_score on rows not flagged missing")
                from ._common import subset
                s = subset(s, fin)
            tab = M.metric_table(s, md.n_problems, fop)
            tab["n_missing"] = n_missing
            rs = M.RankStats(s, md.n_problems)
            ivs = {}
            for name, fn in (("auroc_pooled", rs.auroc_pooled), ("W", rs.W), ("W_avg", rs.W_avg)):
                ivs[name] = interval_dict(percentile_interval(tab[name], fn(counts), SHAPLEY_MARGINAL_LEVEL))
            c = tab["counts"]
            for name, val in tab.items():
                if name == "counts":
                    continue
                scalar = val if not isinstance(val, dict) else None
                rows.append(MetricResult(
                    metric=name, model_key=m, population=pop, label_suite=lab, readout=readout,
                    value=scalar, undefined_reason=None if val is not None else "undefined (one class or no mixed problem)",
                    n_samples=c["n_samples"], n_problems=c["n_problems"], n_mixed=c["mixed"],
                    extra={"fit_suite": suite, "fold_seed": seed, "interval": ivs.get(name),
                           **({"components": val} if isinstance(val, dict) else {})}).to_dict())
    return rows


def gap_inputs(scores, md: ModelData, zs_name: str, fop) -> GapInputs | None:
    l0, l1 = md.suites
    parts = {"probe": {}, "zsi": {}, "st": {}, "sti": {}}
    for s in md.suites:
        parts["probe"][s] = align(find(scores, md.model, md.pop, "P", s, 0), md.uids)
        parts["zsi"][s] = align(find(scores, md.model, md.pop, f"iso:{zs_name}", s, 0), md.uids)
        parts["st"][s] = align(find(scores, md.model, md.pop, "ST", s, 0), md.uids)
        parts["sti"][s] = align(find(scores, md.model, md.pop, "iso:ST", s, 0), md.uids)
    zs = align(find(scores, md.model, md.pop, zs_name, None, 0), md.uids)
    if zs is None or any(v is None for d in parts.values() for v in d.values()):
        return None
    return GapInputs(problem_index=md.problem_index, n_problems=md.n_problems, labels=md.labels,
                     probe=parts["probe"], zero_shot=zs, zero_shot_iso=parts["zsi"], trained=parts["st"],
                     trained_iso=parts["sti"], suites=(l0, l1), fold_of_problem=fop)


def seed_residuals(scores, md: ModelData, counts, jk):
    l1 = md.suites[1]
    pts, reps, jks, w_st, flagged = [], [], [], [], False
    for seed in FOLD_SEEDS:
        p = align(find(scores, md.model, md.pop, "P", l1, seed), md.uids)
        st_df = find(scores, md.model, md.pop, "ST", l1, seed)
        st = align(st_df, md.uids)
        sti = align(find(scores, md.model, md.pop, "iso:ST", l1, seed), md.uids) if seed == 0 else None
        if p is None or st is None or (seed == 0 and sti is None):
            return None
        if st_df is not None and "flagged" in st_df and st_df["flagged"].astype(bool).any():
            flagged = True
        pt, rp = per_seed_residual(md.problem_index, md.n_problems, md.labels[l1], p, st, sti, counts)
        _, rj = per_seed_residual(md.problem_index, md.n_problems, md.labels[l1], p, st, sti, jk)
        pts.append(pt)
        reps.append(rp)
        jks.append(rj)
        w_st.append(M.within_problem_auroc(md.scored(st, l1), n_problems=md.n_problems))
    return {"points": pts, "reps": reps, "jk": jks, "w_st": w_st, "flagged": flagged}


# ---------------------------------------------------------------------------------------------------
# Sensitivities, strata, and listings
# ---------------------------------------------------------------------------------------------------
def load_release_dates(layout: RunLayout) -> dict[str, str | None]:
    p = layout.problems("lcb_v6")
    out: dict[str, str | None] = {}
    if p.exists():
        for line in p.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["problem_id"]] = r.get("release_date")
    return out


def sensitivity_for(scores, md: ModelData, inp: GapInputs, store: dict, counts, chain: str, labels,
                    problems, fop, notes: list) -> dict:
    """Section 1.2, 1.3, 1.5, 4, 6, 7.1 to 7.4, 7.11 sensitivities for one model (analysis.sensitivity)."""
    m, pop = md.model, md.pop
    l0, l1 = md.suites
    out: dict = {"adjustment": "unadjusted (section 9)", "level": SHAPLEY_MARGINAL_LEVEL}
    subs = {}
    for name in SENS.PROBE_SUBSTITUTES + SENS.STATED_SUBSTITUTES:
        df = find(scores, m, pop, name, l1, 0)
        sc = align(df, md.uids)
        if sc is not None:
            subs[name] = sc
    if subs:
        out["readout_substitutions"] = SENS.r_substitutions(inp, subs, counts)
    if "ST_r16" in subs and "ST_r1" in subs:
        out["capacity_rule"] = SENS.capacity_rule(inp, subs["ST_r16"], subs["ST_r1"], counts)
    if "ST_head" in subs:
        out["head_contrast"] = SENS.head_contrast(inp, subs["ST_head"], counts)
    out["no_tiebreak_budget"] = SENS.budget_vs_primary(store, replace_inputs(inp, use_tiebreak=False), counts)
    # V1-drop budget
    if chain == "SZ_V1":
        dz = find(scores, m, pop, "SZ_V1_drop", None, 0)
        if dz is not None:
            ok = np.isfinite(pd.to_numeric(dz["rank_score"], errors="coerce").to_numpy(np.float64))
            if "missing" in dz:
                ok &= ~dz["missing"].astype(bool).to_numpy()
            kept = set(dz.loc[ok, "sample_uid"])
            mask = np.array([u in kept for u in md.uids])
            sub_uids = [u for u, k in zip(md.uids, mask) if k]
            zs = align(dz, sub_uids)
            zsi = {s: align(find(scores, m, pop, "iso:SZ_V1_drop", s, 0), sub_uids) for s in md.suites}
            if mask.any() and zs is not None and all(v is not None for v in zsi.values()):
                alt = replace_inputs(subset_inputs(inp, mask), zero_shot=zs, zero_shot_iso=zsi)
                out["v1_drop_budget"] = SENS.budget_vs_primary(store, alt, counts)
                out["v1_drop_budget"]["n_dropped"] = int((~mask).sum())
    # isotonic-map sensitivities for S^T
    for name in ("ST_inner234", "ST_insample"):
        found = {s: align(find(scores, m, pop, f"iso:{name}", s, 0), md.uids) for s in md.suites}
        found = {s: v for s, v in found.items() if v is not None}
        if found:
            alt = replace_inputs(inp, trained_iso={**inp.trained_iso, **found})
            out[f"iso_map_{name}"] = SENS.budget_vs_primary(store, alt, counts)
            out[f"iso_map_{name}"]["suites_replaced"] = sorted(found)
    # extraction-failure and truncation excluded
    if md.excluded:
        mask = ~(md.excluded[l0] | md.excluded[l1])
        n_ex = int((~mask).sum())
        if n_ex == 0:
            out["extraction_excluded_budget"] = {"n_excluded": 0, "note": "no excluded sample; equals the primary"}
        elif mask.any():
            out["extraction_excluded_budget"] = SENS.budget_vs_primary(store, subset_inputs(inp, mask), counts)
            out["extraction_excluded_budget"]["n_excluded"] = n_ex
    # readout-format contrast S^R against S^T at g = 0
    sr = {s: align(find(scores, m, pop, "SR", s, 0), md.uids) for s in md.suites}
    sr = {s: v for s, v in sr.items() if v is not None}
    if sr:
        out["readout_format_contrast_g0"] = SENS.readout_format_contrast(inp, sr, counts)
    # LiveCodeBench full-suite labeling sensitivity (no agreement readout)
    if pop == "lcb":
        mdf = ModelData(m, pop, ("lcb_public", "lcb_full"), labels, problems)
        if mdf.uids:
            alt = gap_inputs(scores, mdf, chain, fop)
            if alt is not None:
                rep_f = SENS.budget_vs_primary(store, alt, counts)
                tp, _ = three_player_report(G.discrimination_cells(alt)["cells"],
                                            None if counts is None else G.discrimination_cells(alt, counts)["cells"])
                rep_f["three_player"] = tp
                out["lcb_full_labeling"] = rep_f
            else:
                notes.append(f"{m}/lcb: lcb_full readouts incomplete; full-suite sensitivity skipped")
    return out


def contamination_for(md: ModelData, inp: GapInputs, problems, release_dates, counts) -> tuple[dict, dict]:
    part = ST.contamination_partition(md.model, problems, release_dates)
    rep: dict = {"count_date": part["count_date"], "count_date_stated": part["count_date_stated"],
                 "has_stratum": part["has_stratum"], "adjustment": ST.UNADJUSTED, "partitions": {}}
    stores: dict = {}
    if not part["has_stratum"]:
        rep["note"] = "no LiveCodeBench problem is released after the count date; no contamination stratum"
    for label, pmask in part["masks"].items():
        smask = np.asarray(pmask)[inp.problem_index]
        entry = {"n_problems": int(np.asarray(pmask).sum())}
        if smask.any() and part["has_stratum"]:
            r, s = model_budget(subset_inputs(inp, smask), counts, None, secondary=False, routing=False,
                                three_player=True, diagnostics=False)
            entry["budget"] = r
            stores[label] = s
        rep["partitions"][label] = entry
    if "post" in stores:
        other = "pre" if "pre" in stores else "pre_or_unknown" if "pre_or_unknown" in stores else None
        if other:
            rep["post_minus_" + other] = ST.term_contrast([stores["post"]], [stores[other]], f"post minus {other}")
    return rep, stores


def lcb_listings(labels: pd.DataFrame, problems: list[str]) -> dict:
    """Section 6: problems no sample of any model passes under lcb_public, and problems whose public and
    full-suite labels disagree for every sample that passes the public tests."""
    lab = labels[labels["problem_id"].isin(set(problems)) & labels["suite_id"].isin(["lcb_public", "lcb_full"])]
    pub = lab[lab["suite_id"] == "lcb_public"]
    passes = pub.groupby("problem_id")["y"].max()
    none_pass = sorted(q for q in problems if q in passes.index and int(passes[q]) == 0)
    disagree = None
    if (lab["suite_id"] == "lcb_full").any():
        wide = lab.pivot_table(index=["problem_id", "sample_uid"], columns="suite_id", values="y", aggfunc="first")
        wide = wide.dropna()
        pp = wide[wide["lcb_public"] == 1]
        g = pp.groupby(level="problem_id")["lcb_full"].max()
        disagree = sorted(str(q) for q, v in g.items() if int(v) == 0)
    return {"no_sample_passes_public": none_pass, "public_full_disagree_for_every_passing_sample": disagree,
            "n_problems_with_public_labels": int(passes.size)}


# ---------------------------------------------------------------------------------------------------
# Generation shift (section 1.5)
# ---------------------------------------------------------------------------------------------------
def _intervals_nested(pt: dict, rp: dict, level: float = SHAPLEY_MARGINAL_LEVEL) -> dict:
    return {k: {s: interval_dict(percentile_interval(float(pt[k][s][0]), rp[k][s], level)) for s in pt[k]}
            for k in pt}


def fresh_labels(layout: RunLayout, model: str, benchmarks, gen_sets) -> pd.DataFrame:
    return load_labels(layout, [model], benchmarks, tuple(gen_sets))


def fresh_model_data(layout, model, pop, suite, problems, benchmarks, fresh_sets, notes) -> ModelData | None:
    gsets = fresh_sets.get((model, pop, suite))
    if not gsets:
        return None
    fl = fresh_labels(layout, model, benchmarks, gsets)
    if fl.empty:
        notes.append(f"{model}/{pop}: fresh set {suite} has no labels")
        return None
    per = fl.groupby("problem_id")["generation_set"].nunique()
    if (per > 1).any():
        notes.append(f"{model}/{pop}: fresh set {suite} has problems in more than one fold set; skipped")
        return None
    md = ModelData(model, pop, (suite,), fl, problems)
    return md if md.uids else None


def generation_shift_for(model, pop, problems, frozen, fresh, fresh_sets, labels, layout, benchmarks,
                         counts, notes) -> dict | None:
    out: dict = {}
    for suite in POPULATIONS[pop]:
        mdr = fresh_model_data(layout, model, pop, suite, problems, benchmarks, fresh_sets, notes)
        if mdr is None:
            continue
        mdf = ModelData(model, pop, (suite,), labels, problems)
        p0 = align(find(frozen, model, pop, "P", suite, 0), mdf.uids)
        s0 = align(find(frozen, model, pop, "SR", suite, 0), mdf.uids)
        p1 = align(fresh.get((model, pop, "P", suite, suite)), mdr.uids)
        s1 = align(fresh.get((model, pop, "SR", suite, suite)), mdr.uids)
        if any(x is None for x in (p0, s0, p1, s1)):
            notes.append(f"{model}/{pop}: generation shift for {suite} skipped (P or SR missing on a set)")
            continue
        g0 = GenSet(mdf.problem_index, mdf.labels, {suite: p0}, {suite: s0}, mdf.excluded[suite])
        g1 = GenSet(mdr.problem_index, mdr.labels, {suite: p1}, {suite: s1}, mdr.excluded[suite])
        n = len(problems)
        pt, rp = contrasts(g0, g1, n, (suite,)), contrasts(g0, g1, n, (suite,), counts)
        out[suite] = {
            "generation_sets": fresh_sets[(model, pop, suite)],
            "contrasts": _intervals_nested(pt, rp),
            "rates_frozen": {k: float(v[0]) for k, v in set_rates(g0, n, (suite,)).items()},
            "rates_fresh": {k: float(v[0]) for k, v in set_rates(g1, n, (suite,)).items()},
        }
    return out or None


# ---------------------------------------------------------------------------------------------------
# Reconciliation (section 2; orchestrator mapping)
# ---------------------------------------------------------------------------------------------------
def reconciliation_for(models, pops, frozen, fresh, fresh_sets, labels, layout, benchmarks, draws_by_pop,
                       notes) -> dict | None:
    checks: list[dict] = []
    descriptive: dict = {}

    def term(md: ModelData, sc: Scores | None, stat: str, suite: str):
        return None if sc is None else Term(md.scored(sc, suite), stat, md.excluded[suite])

    # [Ribeiro]: C1, HumanEval only, pass@rank-1 within problem, original suite
    if "C1" in models and "label_validity" in pops:
        problems = pops["label_validity"]
        md = ModelData("C1", "label_validity", ("O",), labels, problems)
        if md.uids:
            counts = draws_by_pop["label_validity"].counts
            mask = np.array([q.startswith("HumanEval/") for q in problems])
            n = len(problems)
            lat = term(md, align(find(frozen, "C1", "label_validity", "LAT", "O", 0), md.uids), "rank1", "O")
            sz2 = term(md, align(find(frozen, "C1", "label_validity", "SZ_V2", None, None), md.uids), "rank1", "O")
            tlg = term(md, align(find(frozen, "C1", "label_validity", "TL_geo", None, None), md.uids), "rank1", "O")
            if lat is not None:
                rnd = Term(lat.s, "random", lat.excluded)
                checks.append(run_check("ribeiro_lat_above_random", "ribeiro", None, "C1", "ordering", 1, None,
                                        lat, rnd, counts, n, mask))
                if sz2 is not None:
                    checks.append(run_check("ribeiro_lat_above_reflective_tf", "ribeiro", None, "C1", "ordering", 1,
                                            None, lat, sz2, counts, n, mask))
                if tlg is not None:
                    c = contrast(lat, tlg, counts, n, mask)
                    descriptive["ribeiro_lat_minus_intrinsic"] = {"value": c["value"], "interval": interval_dict(c["interval"])}
            else:
                notes.append("ribeiro: LAT scores for C1 missing; checks skipped")

    # [Campos]: X1, X2 on LiveCodeBench, suite lcb_label
    if "lcb" in pops:
        problems = pops["lcb"]
        n = len(problems)
        counts = draws_by_pop["lcb"].counts
        for m in ("X1", "X2"):
            if m not in models:
                continue
            md = ModelData(m, "lcb", ("lcb_label",), labels, problems)
            if not md.uids:
                continue
            get = lambda r: align(find(frozen, m, "lcb", r, "lcb_label", 0), md.uids)  # noqa: E731
            P, PROMPT, P2, P3 = get("P"), get("PROMPT"), get("P2"), get("P3")
            if P is not None and PROMPT is not None:
                a, b = term(md, PROMPT, "auroc", "lcb_label"), term(md, P, "auroc", "lcb_label")
                if m == "X1":
                    checks.append(run_check("campos_x1_prompt_tie_probe_pooled", "campos", None, m, "tie", 0,
                                            CAMPOS_TIE_WIDTH, a, b, counts, n))
                else:
                    checks.append(run_check("campos_x2_prompt_below_probe_pooled", "campos", None, m, "ordering", -1,
                                            None, a, b, counts, n))
            if P is not None:
                checks.append(run_check(f"campos_{m.lower()}_probe_W_above_half", "campos", None, m, "above_value", 1,
                                        None, term(md, P, "W", "lcb_label"), 0.5, counts, n))
            if m == "X1" and P2 is not None and P3 is not None:
                checks.append(run_check("campos_x1_judging_probe_below_code_probe_W", "campos", None, m, "ordering",
                                        -1, None, term(md, P3, "W", "lcb_label"), term(md, P2, "W", "lcb_label"),
                                        counts, n))

        # [2610.31820]: S1 on LiveCodeBench, reading B (frozen) and reading A (fresh)
        if "S1" in models:
            suite = "lcb_label"
            readings = []
            md = ModelData("S1", "lcb", (suite,), labels, problems)
            if md.uids:
                g = lambda r, ls, s: align(find(frozen, "S1", "lcb", r, ls, s), md.uids)  # noqa: E731
                readings.append(("B", md, g("SR", suite, 0), g("P", suite, 0), g("SZ_V1", None, 0)))
            mdr = fresh_model_data(layout, "S1", "lcb", suite, problems, benchmarks, fresh_sets, notes)
            if mdr is not None:
                f = lambda r, ls: align(fresh.get(("S1", "lcb", r, ls, suite)), mdr.uids)  # noqa: E731
                readings.append(("A", mdr, f("SR", suite), f("P", suite), f("SZ_V1", None)))
            for reading, mdx, SR, P, SZ in readings:
                if SR is None or P is None:
                    notes.append(f"r2610 reading {reading}: SR or P missing; checks skipped")
                    continue
                tsr, tp = term(mdx, SR, "auroc", suite), term(mdx, P, "auroc", suite)
                checks.append(run_check(f"r2610_{reading}_sr_tie_probe_pooled", "r2610", reading, "S1", "tie", 0,
                                        R2610_TIE_WIDTH, tsr, tp, counts, n))
                if SZ is None:
                    notes.append(f"r2610 reading {reading}: SZ_V1 missing; verbalized checks skipped")
                    continue
                tz = term(mdx, SZ, "auroc", suite)
                checks.append(run_check(f"r2610_{reading}_verbalized_below_sr", "r2610", reading, "S1", "ordering",
                                        -1, None, tz, tsr, counts, n))
                checks.append(run_check(f"r2610_{reading}_verbalized_below_probe", "r2610", reading, "S1", "ordering",
                                        -1, None, tz, tp, counts, n))
    if not checks and not descriptive:
        return None
    verbs = {}
    for paper in sorted({c["check"]["paper"] for c in checks}):
        outs = [c["check"]["outcome"] for c in checks if c["check"]["paper"] == paper]
        diag = [c["check"]["diagnostic_excluding_truncation"] for c in checks if c["check"]["paper"] == paper]
        v, cnt = paper_verb(outs)
        dv, dcnt = paper_verb(diag)
        verbs[paper] = {"verb": v, "counts": cnt, "diagnostic_verb": dv, "diagnostic_counts": dcnt}
    return {"level": RECONCILIATION_LEVEL, "adjustment": "none (each check is a separate pre-stated check)",
            "checks": checks, "descriptive": descriptive, "verbs": verbs}


# ---------------------------------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------------------------------
def run(cfg: RunConfig, layout: RunLayout, manifest: Manifest, *, dry_run: bool = False) -> StageReport:
    report = StageReport(stage="analysis", ok=True)
    b = int(cfg.extra.get("bootstrap_b", B_BOOTSTRAP))
    root = cfg.extra.get("analysis_root")
    alayout = AnalysisLayout.for_run(cfg.run_id, Path(root) if root else None)
    man_sha = sha256_file(layout.manifest) if layout.manifest.exists() else None
    header = {"run_id": cfg.run_id, "manifest_sha256": man_sha, "analysis_code_sha256": code_sha256(),
              "bootstrap": {"b": b, "seed": BOOTSTRAP_SEED}, "config_hash": config_hash(cfg.to_dict())}
    if man_sha is None:
        report.notes.append("run manifest not found; manifest_sha256 is null")

    models = tuple(dict.fromkeys(tuple(cfg.models) + tuple(cfg.generation_only_models)))
    labels = load_labels(layout, models, cfg.benchmarks)
    pops: dict[str, list[str]] = {}
    ref_info = None
    if any(bm in LABEL_VALIDITY_BENCHMARKS for bm in cfg.benchmarks):
        if not layout.reference_checks.exists():
            report.ok = False
            report.notes.append("reference checks missing: the label-validity population is undefined")
        else:
            valid, ref_info = valid_lv_problems(layout)
            have = set(labels.loc[labels["benchmark"].isin(LABEL_VALIDITY_BENCHMARKS), "problem_id"])
            pops["label_validity"] = sorted(set(valid) & have) if have else valid
    if any(bm in LCB_BENCHMARKS for bm in cfg.benchmarks):
        lc = labels[labels["benchmark"].isin(LCB_BENCHMARKS)]
        pops["lcb"] = sorted(set(lc["problem_id"]))
    scores, fresh, fresh_sets = load_scores(layout)
    report.metrics["n_score_tables"] = len(scores)
    report.metrics["n_fresh_sets"] = len(fresh_sets)
    report.metrics["populations"] = {p: len(v) for p, v in pops.items()}
    if dry_run or not report.ok:
        report.notes.append("dry run: inputs checked, nothing written" if dry_run else "stopped before analysis")
        return report

    sealed = bool(cfg.seal_gamma)
    ops: dict = {"reference_checks": ref_info, "models": {}}
    res: dict = {"metrics": [], "budgets": {}, "per_seed": {}, "pooled": {}, "generation_shift": {},
                 "reconciliation": None, "sensitivity": {}, "contamination": {}, "strata": {}}
    release_dates = load_release_dates(layout) if "lcb" in pops else {}
    draws_by_pop: dict = {}
    written: list[Path] = []

    for pop, problems in pops.items():
        if not problems:
            continue
        suites = POPULATIONS[pop]
        draws = draw(problems, b, BOOTSTRAP_SEED)
        draws_by_pop[pop] = draws
        jk = jackknife_counts(len(problems))
        fop = fold_of_problem(layout, pop, problems)
        stores, chains, seeds, contam = {}, {}, {}, {}
        for m in models:
            md = ModelData(m, pop, suites, labels, problems)
            if not md.uids:
                continue
            op = operational(md)
            pr = v1_parse_rate(scores, md)
            op["v1_parse_rate"] = pr
            chain = "SZ_V2" if pr is not None and pr < K3_MIN_V1_PARSE_RATE else "SZ_V1"
            op["primary_chain"] = chain
            ops["models"][f"{m}|{pop}"] = op
            if m in cfg.generation_only_models:
                continue
            res["metrics"].extend(metrics_rows(scores, md, fop, draws.counts))
            if pop == "lcb":
                md_full = ModelData(m, pop, ("lcb_full",), labels, problems)
                if md_full.uids:
                    res["metrics"].extend(metrics_rows(scores, md_full, fop, draws.counts))
            v2s = align(find(scores, m, pop, "SZ_V2", None, None), md.uids)
            op["v2_degenerate"] = None if v2s is None else bool(np.unique(v2s.rank_score).size == 1)
            inp = gap_inputs(scores, md, chain, fop)
            if inp is None:
                report.notes.append(f"{m}/{pop}: readouts of the 16-cell game incomplete; budget skipped")
            else:
                op["tie_rates"] = tie_rates(inp)
                inp_v2 = gap_inputs(scores, md, "SZ_V2", fop) if chain == "SZ_V1" else None
                rep, store = model_budget(inp, draws.counts, inp_v2,
                                          secondary=bool(cfg.extra.get("secondary_budgets", True)),
                                          routing=bool(cfg.extra.get("routing", True)),
                                          three_player=(pop == "lcb"))
                rep["primary_chain"] = chain
                res["budgets"][f"{m}|{pop}"] = rep
                stores[m] = store
                chains[m] = chain
                if cfg.extra.get("sensitivities", True):
                    res["sensitivity"][f"{m}|{pop}"] = sensitivity_for(scores, md, inp, store, draws.counts, chain,
                                                                       labels, problems, fop, report.notes)
                if pop == "lcb":
                    crep, cst = contamination_for(md, inp, problems, release_dates, draws.counts)
                    res["contamination"][m] = crep
                    contam[m] = cst
            sr = seed_residuals(scores, md, draws.counts, jk)
            if sr is not None:
                seeds[m] = sr
                w = np.array([x for x in sr["w_st"] if x is not None], dtype=float)
                op["st_W_seed_spread"] = {"sd": float(np.std(w, ddof=1)) if w.size > 1 else None,
                                          "range": float(w.max() - w.min()) if w.size else None,
                                          "n_seeds": int(w.size)}
                res["per_seed"][f"{m}|{pop}"] = {"points": sr["points"], "flagged": sr["flagged"]}
        for m in GEN_SHIFT_MODELS:
            if m in cfg.models:
                gsr = generation_shift_for(m, pop, problems, scores, fresh, fresh_sets, labels, layout,
                                           cfg.benchmarks, draws.counts, report.notes)
                if gsr is not None:
                    res["generation_shift"][f"{m}|{pop}"] = gsr
        if stores:
            res["strata"][pop] = ST.stratum_contrasts(stores)
        if pop == "lcb":
            ops["lcb_listings"] = lcb_listings(labels, problems)
            if contam:
                pooled_c: dict = {"models": [x for x in ST.CONTAMINATION_POOLED if x in contam],
                                  "no_stratum": sorted(x for x in contam if not res["contamination"][x]["has_stratum"]),
                                  "adjustment": ST.UNADJUSTED}
                for part in ("post", "pre"):
                    have = [x for x in ST.CONTAMINATION_POOLED if part in contam.get(x, {})]
                    if have == list(ST.CONTAMINATION_POOLED):
                        pooled_c[part] = {"four_player": pooled_budget({x: contam[x][part] for x in have}),
                                          "three_player": ST.term_intervals([contam[x][part] for x in have],
                                                                            f"{part}, Olmo 3 and Gemma 4", "three")}
                if "post" in pooled_c and "pre" in pooled_c:
                    pooled_c["post_minus_pre"] = ST.term_contrast([contam[x]["post"] for x in ST.CONTAMINATION_POOLED],
                                                                  [contam[x]["pre"] for x in ST.CONTAMINATION_POOLED],
                                                                  "post minus pre, Olmo 3 and Gemma 4")
                res["contamination"]["pooled_olmo3_gemma4"] = pooled_c
        if pop == "label_validity":
            prim = {mm: ops["models"].get(f"{mm}|{pop}", {}).get("v2_degenerate") for mm in PRIMARY_MODELS}
            n_deg = sum(1 for v in prim.values() if v)
            ops["k3_degenerate_v2"] = {"per_model": prim, "n_degenerate": n_deg,
                                       "n_with_v2": sum(1 for v in prim.values() if v is not None),
                                       "fires": n_deg > len(PRIMARY_MODELS) / 2}
            lv = {mm: ops["models"].get(f"{mm}|{pop}") for mm in PRIMARY_MODELS}
            if all(v is not None for v in lv.values()):
                ops["k_rule"] = k_rule_report(
                    {mm: v["counts_E"]["mixed"] for mm, v in lv.items()},
                    pair_counts={mm: v["counts_E"]["pass_fail_pairs"] for mm, v in lv.items()},
                    histograms={mm: v["pass_count_histogram_E"] for mm, v in lv.items()})
        if all(mm in seeds for mm in PRIMARY_MODELS):
            psr = {mm: seeds[mm]["points"] for mm in PRIMARY_MODELS}
            prep = {mm: seeds[mm]["reps"] for mm in PRIMARY_MODELS}
            r_bar = float(np.mean([np.mean(v) for v in psr.values()]))
            rep_bar = np.mean([np.mean(np.vstack(prep[mm]), axis=0) for mm in PRIMARY_MODELS], axis=0)
            jk_bar = np.mean([np.mean(np.vstack(seeds[mm]["jk"]), axis=0) for mm in PRIMARY_MODELS], axis=0)
            bca = interval_dict(bca_interval(r_bar, rep_bar, jk_bar, DECISION_INTERVAL_LEVEL))
            res["pooled"][pop] = {"primary": primary_report(psr, prep, {mm: seeds[mm]["flagged"] for mm in PRIMARY_MODELS},
                                                            bca={"unwidened": bca})}
        if all(mm in stores for mm in PRIMARY_MODELS):
            pst = {mm: stores[mm] for mm in PRIMARY_MODELS}
            pooled = res["pooled"].setdefault(pop, {})
            pooled["budget_primary_chain"] = pooled_budget(pst)
            if pop == "lcb":
                pooled["budget_three_player"] = ST.term_intervals(list(pst.values()), "six primary models, l = lcb_label",
                                                                  "three")
            pooled["k3_switched_models"] = sorted(mm for mm in PRIMARY_MODELS if chains[mm] == "SZ_V2")
            v2 = {}
            for mm in PRIMARY_MODELS:
                if chains[mm] == "SZ_V2":
                    v2[mm] = {"c": pst[mm]["disc_cells_pt"], "r": pst[mm]["disc_cells_rep"]}
                elif pst[mm].get("v2_cells_pt") is not None:
                    v2[mm] = {"c": pst[mm]["v2_cells_pt"], "r": pst[mm]["v2_cells_rep"]}
            if len(v2) == len(PRIMARY_MODELS):
                pooled["budget_all_v2_chain"] = pooled_budget(v2, "c", "r")
            for est in ("brier", "ece_debiased_equal_mass", "smooth_ece", "ks_calibration_error"):
                if all("secondary" in pst[mm] for mm in PRIMARY_MODELS):
                    sec = {mm: pst[mm]["secondary"][est] for mm in PRIMARY_MODELS}
                    pooled.setdefault("secondary", {})[est] = pooled_budget(sec, "pt", "rep")
            rp_pt = {mm: pst[mm]["disc_cells_pt"]["1101"] for mm in PRIMARY_MODELS}
            rp_rep = {mm: pst[mm]["disc_cells_rep"]["1101"] for mm in PRIMARY_MODELS}
            pooled["r_pool"] = pooled_residual_report(rp_pt, rp_rep)
            if "primary" in pooled:
                r0 = float(np.mean([pst[mm]["disc_cells_pt"]["1111"] for mm in PRIMARY_MODELS]))
                pooled["r_bar_minus_r0"] = pooled["primary"]["r_bar"] - r0
                pooled["r0"] = r0

    res["reconciliation"] = reconciliation_for(set(cfg.models), pops, scores, fresh, fresh_sets, labels, layout,
                                               cfg.benchmarks, draws_by_pop, report.notes)

    if sealed:
        layout.sealed.mkdir(parents=True, exist_ok=True)
        sp = _write_json(layout.sealed / "gamma_sealed.json", {**header, **res})
        digest = sha256_file(sp)
        hp = layout.sealed / "gamma_sealed.sha256"
        hp.write_text(f"{digest}  gamma_sealed.json\n")
        ch = config_hash(cfg.to_dict())
        for p in (sp, hp):
            manifest.add(layout.root, p, PRODUCER, ch)
            report.outputs.append(str(p.relative_to(layout.root)))
        manifest.save(layout.manifest)
        report.notes.append("Gamma outputs sealed; hash recorded in the manifest")
    else:
        written.append(_write_json(alayout.result("metrics"), {**header, "rows": res["metrics"]}))
        written.append(_write_json(alayout.result("budgets"), {**header, "budgets": res["budgets"]}))
        written.append(_write_json(alayout.result("per_seed_residuals"), {**header, "per_seed": res["per_seed"]}))
        written.append(_write_json(alayout.result("pooled"), {**header, "pooled": res["pooled"]}))
        if res["generation_shift"]:
            written.append(_write_json(alayout.result("generation_shift"),
                                       {**header, "generation_shift": res["generation_shift"]}))
        for name in ("sensitivity", "contamination", "strata"):
            if res[name]:
                written.append(_write_json(alayout.result(name), {**header, name: res[name]}))
        if res["reconciliation"] is not None:
            written.append(_write_json(alayout.result("reconciliation"), {**header, **res["reconciliation"]}))
    written.append(_write_json(alayout.result("operational"), {**header, **ops}))
    index = {p.name: {"sha256": sha256_file(p), "bytes": p.stat().st_size} for p in written}
    written.append(_write_json(alayout.result("INDEX"), {**header, "files": index}))
    report.notes.extend(f"analysis_result: {p}" for p in written)
    report.metrics["models_analyzed"] = sorted(ops["models"])
    report.metrics["sealed"] = sealed
    return report
