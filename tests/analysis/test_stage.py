"""analysis.stage end to end on a synthetic run directory (six primary models, small B)."""

import json

import numpy as np
import pandas as pd
import pytest

from analysis import stage
from pipeline.contracts.constants import FOLD_SEEDS, PRIMARY_MODELS
from pipeline.contracts.hashing import sha256_file
from pipeline.contracts.interfaces import RunConfig
from pipeline.contracts.layout import RunLayout
from pipeline.contracts.manifest import Manifest
from pipeline.contracts.schemas import TABLE_COLUMNS, sample_uid
from synth import make_inputs, v2_chain

N_P, K = 24, 5


def _rows(model, uids, readout, suite, seed, sc, **flags):
    n = len(uids)
    return pd.DataFrame({
        "sample_uid": uids, "model_key": model, "population": "label_validity", "readout": readout,
        "label_suite": suite, "fold_seed": seed, "fold": 0, "prob": sc.prob, "rank_score": sc.rank_score,
        "rank_tiebreak": sc.rank_tiebreak, "missing": flags.get("missing", np.zeros(n, bool)),
        "imputed": flags.get("imputed", np.zeros(n, bool)), "generation_set": "frozen",
        "flagged": flags.get("flagged", False),
    })[list(TABLE_COLUMNS["scores"])]


def build_run(tmp_path, v1_parse_ok=True):
    layout = RunLayout.for_run("t", tmp_path / "runs")
    problems = [f"HumanEval/{i}" for i in range(N_P)]
    (layout.root / "data").mkdir(parents=True)
    rc = [{"problem_id": p, "suite_id": s, "passed": True, "failure": None, "excluded": (p == "HumanEval/0" and s == "E")}
          for p in problems for s in ("O", "E")]
    pd.DataFrame(rc).to_parquet(layout.reference_checks)
    for mi, m in enumerate(PRIMARY_MODELS):
        inp = make_inputs(mi, n_problems=N_P, k=K)
        v2 = v2_chain(inp)
        uids = [sample_uid(m, "humaneval_plus", problems[i], j + 1) for i in range(N_P) for j in range(K)]
        lab = [{"sample_uid": u, "suite_id": s, "y": int(inp.labels[s][n]), "source": "execution",
                "failure": None, "cache_key": None} for n, u in enumerate(uids) for s in ("O", "E")]
        lp = layout.labels(m, "humaneval_plus", "frozen")
        lp.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(lab).to_parquet(lp)
        tabs = []
        imp = inp.zero_shot.imputed if v1_parse_ok else np.ones(len(uids), bool)
        tabs.append(_rows(m, uids, "SZ_V1", None, 0, inp.zero_shot, imputed=imp, missing=imp))
        tabs.append(_rows(m, uids, "SZ_V2", None, None, v2.zero_shot))
        for s in ("O", "E"):
            tabs.append(_rows(m, uids, "P", s, 0, inp.probe[s]))
            tabs.append(_rows(m, uids, "ST", s, 0, inp.trained[s]))
            tabs.append(_rows(m, uids, "iso:ST", s, 0, inp.trained_iso[s]))
            tabs.append(_rows(m, uids, "iso:SZ_V1", s, 0, inp.zero_shot_iso[s]))
            tabs.append(_rows(m, uids, "iso:SZ_V2", s, 0, v2.zero_shot_iso[s]))
        rng = np.random.default_rng(100 + mi)
        for seed in FOLD_SEEDS[1:]:
            for name, base in (("P", inp.probe["E"]), ("ST", inp.trained["E"])):
                sc = type(base)(rank_score=base.rank_score + rng.normal(0, 0.3, len(uids)),
                                rank_tiebreak=base.rank_tiebreak, prob=base.prob)
                tabs.append(_rows(m, uids, name, "E", seed, sc))
        for t in tabs:
            r = t.iloc[0]
            p = layout.scores(m, "label_validity", r["readout"], r["label_suite"],
                              None if pd.isna(r["fold_seed"]) else int(r["fold_seed"]))
            p.parent.mkdir(parents=True, exist_ok=True)
            t.to_parquet(p)
    Manifest(run_id="t").save(layout.manifest)
    return layout


def cfg(tmp_path, seal=False, secondary=False):
    return RunConfig(run_id="t", models=PRIMARY_MODELS, benchmarks=("humaneval_plus",), seal_gamma=seal,
                     extra={"bootstrap_b": 40, "analysis_root": str(tmp_path / "analysis"),
                            "secondary_budgets": secondary, "routing": not secondary})


def test_stage_unsealed(tmp_path):
    layout = build_run(tmp_path)
    man = Manifest.load(layout.manifest)
    want_sha = sha256_file(layout.manifest)
    rep = stage.run(cfg(tmp_path), layout, man)
    assert rep.ok, rep.notes
    res = tmp_path / "analysis" / "results" / "t"
    for name in ("metrics", "budgets", "per_seed_residuals", "pooled", "operational"):
        d = json.loads((res / f"{name}.json").read_text())
        assert d["manifest_sha256"] == want_sha and d["bootstrap"]["b"] == 40
    pooled = json.loads((res / "pooled.json").read_text())["pooled"]["label_validity"]
    dec = pooled["primary"]["decision"]
    assert dec["decision"] in ("D1", "D2", "D3", "inconclusive")
    assert len(pooled["primary"]["per_model"]) == 6
    assert "budget_primary_chain" in pooled and "budget_all_v2_chain" in pooled and "r_pool" in pooled
    ops = json.loads((res / "operational.json").read_text())
    # one problem excluded by the reference check under E
    assert ops["reference_checks"]["n_valid"] == N_P - 1
    assert ops["k_rule"]["k"] == 20          # tiny synthetic counts are far below T10
    k3 = ops["k3_degenerate_v2"]           # continuous synthetic V2: never degenerate
    assert k3["n_with_v2"] == 6 and k3["n_degenerate"] == 0 and k3["fires"] is False
    assert "P1|label_validity" in json.loads((res / "sensitivity.json").read_text())["sensitivity"]
    assert "instruct_minus_base" not in json.loads((res / "strata.json").read_text())["strata"]["label_validity"]
    budgets = json.loads((res / "budgets.json").read_text())["budgets"]
    sh = budgets["P1|label_validity"]["discrimination"]["shapley"]
    assert abs(sh["efficiency_gap"]) <= 1e-12
    assert not (layout.root / "sealed").exists()


def test_stage_sealed_writes_nothing_gamma_to_results(tmp_path):
    layout = build_run(tmp_path)
    man = Manifest.load(layout.manifest)
    rep = stage.run(cfg(tmp_path, seal=True, secondary=True), layout, man)
    assert rep.ok
    sp = layout.sealed / "gamma_sealed.json"
    assert sp.exists()
    assert (layout.sealed / "gamma_sealed.sha256").read_text().split()[0] == sha256_file(sp)
    m2 = Manifest.load(layout.manifest)
    assert "sealed/gamma_sealed.json" in m2.entries and "sealed/gamma_sealed.sha256" in m2.entries
    res = tmp_path / "analysis" / "results" / "t"
    assert sorted(p.name for p in res.iterdir()) == ["INDEX.json", "operational.json"]
    idx = json.loads((res / "INDEX.json").read_text())["files"]
    assert idx["operational.json"]["sha256"] == sha256_file(res / "operational.json")
    text = (res / "operational.json").read_text()
    for banned in ("shapley", "phi", "cells", "residual", "decision", "r_bar", "\"W\""):
        assert banned not in text
    ops = json.loads(text)
    assert ops["models"]["P1|label_validity"]["st_W_seed_spread"]["n_seeds"] == 3
    # the report carries no sealed value
    assert "pooled" not in json.dumps(rep.metrics) and "phi" not in json.dumps(rep.metrics)


def test_stage_k3_switch_and_dry_run(tmp_path):
    layout = build_run(tmp_path, v1_parse_ok=False)
    man = Manifest.load(layout.manifest)
    dry = stage.run(cfg(tmp_path), layout, man, dry_run=True)
    assert dry.ok and not (tmp_path / "analysis").exists()
    rep = stage.run(cfg(tmp_path), layout, man)
    ops = json.loads((tmp_path / "analysis" / "results" / "t" / "operational.json").read_text())
    assert ops["models"]["P1|label_validity"]["v1_parse_rate"] == 0.0
    assert ops["models"]["P1|label_validity"]["primary_chain"] == "SZ_V2"
    pooled = json.loads((tmp_path / "analysis" / "results" / "t" / "pooled.json").read_text())["pooled"]
    assert pooled["label_validity"]["k3_switched_models"] == list(PRIMARY_MODELS)
    assert rep.ok


# ---------------------------------------------------------------------------------------------------
# Generation shift and reconciliation wiring
# ---------------------------------------------------------------------------------------------------
def _score_df(model, pop, readout, suite, seed, uids, rank, gen_set="frozen", tb=None):
    n = len(uids)
    from scipy.special import expit
    return pd.DataFrame({
        "sample_uid": uids, "model_key": model, "population": pop, "readout": readout, "label_suite": suite,
        "fold_seed": seed, "fold": 0, "prob": expit(rank), "rank_score": rank,
        "rank_tiebreak": np.full(n, np.nan) if tb is None else tb, "missing": np.zeros(n, bool),
        "imputed": np.zeros(n, bool), "generation_set": gen_set, "flagged": False,
    })[list(TABLE_COLUMNS["scores"])]


def _write_scores(layout, df, tag=""):
    r = df.iloc[0]
    p = layout.scores(r["model_key"], r["population"], r["readout"], r["label_suite"],
                      None if pd.isna(r["fold_seed"]) else int(r["fold_seed"]))
    if tag:
        p = p.with_name(f"{tag}.parquet")
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(p)


def _labels(layout, model, bench, gen_set, uids, y_by_suite, truncated=None):
    rows = []
    for n, u in enumerate(uids):
        for s, y in y_by_suite.items():
            tr = truncated is not None and truncated[n]
            rows.append({"sample_uid": u, "suite_id": s, "y": 0 if tr else int(y[n]),
                         "source": "extraction_failure" if tr else "execution",
                         "failure": "truncated" if tr else None, "cache_key": None})
    p = layout.labels(model, bench, gen_set)
    p.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(p)


def build_recon_run(tmp_path):
    rng = np.random.default_rng(7)
    layout = RunLayout.for_run("r", tmp_path / "runs")
    (layout.root / "data").mkdir(parents=True)
    lv = [f"HumanEval/{i}" for i in range(12)] + [f"Mbpp/{i}" for i in range(6)]
    lcb = [f"lcb/q{i}" for i in range(20)]
    pd.DataFrame([{"problem_id": p, "suite_id": s, "passed": True, "failure": None, "excluded": False}
                  for p in lv for s in ("O", "E")]).to_parquet(layout.reference_checks)

    def samples(model, problems, bench_of, k=5, gen_set="frozen"):
        return [sample_uid(model, bench_of(q), q, j + 1, gen_set) for q in problems for j in range(k)]

    def latent_labels(n):
        diff = np.repeat(rng.normal(0, 1, n // 5), 5)
        lat = diff + rng.normal(0, 1, n)
        return lat, (lat > 0).astype(int)

    lv_bench = lambda q: "humaneval_plus" if q.startswith("HumanEval") else "mbpp_plus"  # noqa: E731
    # C1: [Ribeiro]
    u = samples("C1", lv, lv_bench)
    lat, y = latent_labels(len(u))
    for bench in ("humaneval_plus", "mbpp_plus"):
        idx = [i for i, x in enumerate(u) if f"|{bench}|" in x]
        _labels(layout, "C1", bench, "frozen", [u[i] for i in idx], {"O": y[idx], "E": y[idx]})
    _write_scores(layout, _score_df("C1", "label_validity", "LAT", "O", 0, u, 3 * lat + rng.normal(0, 0.5, len(u))))
    _write_scores(layout, _score_df("C1", "label_validity", "SZ_V2", None, None, u, -3 * lat))
    _write_scores(layout, _score_df("C1", "label_validity", "TL_geo", None, None, u, rng.normal(size=len(u))))
    # X1, X2: [Campos]; S1: [2610.31820]
    for m in ("X1", "X2", "S1"):
        u = samples(m, lcb, lambda q: "lcb_v6")
        lat, y = latent_labels(len(u))
        trunc = rng.uniform(size=len(u)) < 0.1
        _labels(layout, m, "lcb_v6", "frozen", u, {"lcb_public": y, "lcb_label": y}, trunc)
        prob_lat = 2 * lat + rng.normal(0, 0.5, len(u))
        for r, sc in (("P", prob_lat), ("P2", prob_lat), ("P3", 0.3 * prob_lat + rng.normal(0, 1, len(u))),
                      ("PROMPT", np.repeat(prob_lat.reshape(-1, 5).mean(1), 5)), ("SR", prob_lat + rng.normal(0, 0.1, len(u)))):
            _write_scores(layout, _score_df(m, "lcb", r, "lcb_label", 0, u, sc))
        _write_scores(layout, _score_df(m, "lcb", "SZ_V1", None, 0, u, rng.normal(size=len(u))))
    # fresh sets: S1 on lcb_label, P1 on O and E, each split over five fold sets
    def fresh(model, pop, problems, bench_of, suite, with_sz=False):
        frames = {"P": [], "SR": [], "SZ_V1": []}
        for f in range(5):
            gs = f"fresh:SR_{suite}_seed0_fold{f}"
            probs = [q for i, q in enumerate(problems) if i % 5 == f]
            u = samples(model, probs, bench_of, gen_set=gs)
            lat, y = latent_labels(len(u))
            for bench in sorted({bench_of(q) for q in probs}):
                idx = [i for i, x in enumerate(u) if f"|{bench}|" in x]
                _labels(layout, model, bench, gs, [u[i] for i in idx], {suite: y[idx]})
            sc = 2 * lat + rng.normal(0, 0.5, len(u))
            frames["P"].append(_score_df(model, pop, "P", suite, 0, u, sc, gs))
            frames["SR"].append(_score_df(model, pop, "SR", suite, 0, u, sc + rng.normal(0, 1, len(u)), gs))
            frames["SZ_V1"].append(_score_df(model, pop, "SZ_V1", None, 0, u, rng.normal(size=len(u)), gs))
        for r, fr in frames.items():
            if r == "SZ_V1" and not with_sz:
                continue
            _write_scores(layout, pd.concat(fr, ignore_index=True), tag=f"fresh_{r}_{suite}")
    fresh("S1", "lcb", lcb, lambda q: "lcb_v6", "lcb_label", with_sz=True)
    u = samples("P1", lv, lv_bench)
    lat, y = latent_labels(len(u))
    for bench in ("humaneval_plus", "mbpp_plus"):
        idx = [i for i, x in enumerate(u) if f"|{bench}|" in x]
        _labels(layout, "P1", bench, "frozen", [u[i] for i in idx], {"O": y[idx], "E": y[idx]})
    for s in ("O", "E"):
        _write_scores(layout, _score_df("P1", "label_validity", "P", s, 0, u, 2 * lat))
        _write_scores(layout, _score_df("P1", "label_validity", "SR", s, 0, u, lat + rng.normal(0, 1, len(u))))
        fresh("P1", "label_validity", lv, lv_bench, s)
    Manifest(run_id="r").save(layout.manifest)
    return layout


def test_stage_generation_shift_and_reconciliation(tmp_path):
    layout = build_recon_run(tmp_path)
    c = RunConfig(run_id="r", models=("P1", "C1", "X1", "X2", "S1"),
                  benchmarks=("humaneval_plus", "mbpp_plus", "lcb_v6"),
                  extra={"bootstrap_b": 60, "analysis_root": str(tmp_path / "analysis")})
    rep = stage.run(c, layout, Manifest.load(layout.manifest))
    assert rep.ok, rep.notes
    res = tmp_path / "analysis" / "results" / "r"
    gs = json.loads((res / "generation_shift.json").read_text())["generation_shift"]
    assert set(gs["P1|label_validity"]) == {"O", "E"}
    assert len(gs["P1|label_validity"]["E"]["generation_sets"]) == 5
    assert "d1_lcb_label_mixed_both" in gs["S1|lcb"]["lcb_label"]["contrasts"]
    rc = json.loads((res / "reconciliation.json").read_text())
    ids = {x["check"]["check_id"]: x for x in rc["checks"]}
    assert set(ids) == {
        "ribeiro_lat_above_random", "ribeiro_lat_above_reflective_tf",
        "campos_x1_prompt_tie_probe_pooled", "campos_x2_prompt_below_probe_pooled",
        "campos_x1_probe_W_above_half", "campos_x2_probe_W_above_half",
        "campos_x1_judging_probe_below_code_probe_W",
        "r2610_B_sr_tie_probe_pooled", "r2610_B_verbalized_below_sr", "r2610_B_verbalized_below_probe",
        "r2610_A_sr_tie_probe_pooled", "r2610_A_verbalized_below_sr", "r2610_A_verbalized_below_probe"}
    # a strong probe: W(P) - 0.5 has an interval above zero
    assert ids["campos_x1_probe_W_above_half"]["check"]["outcome"] == "consistent"
    # LAT ranks by the latent and SZ_V2 against it: LAT above the reflective analog
    assert ids["ribeiro_lat_above_reflective_tf"]["check"]["outcome"] == "consistent"
    for x in ids.values():
        assert x["check"]["diagnostic_excluding_truncation"] in ("consistent", "not_consistent", "undetermined")
    # truncated samples exist on lcb, so the diagnostic differs from the full-set value
    w = ids["campos_x1_probe_W_above_half"]
    assert w["diagnostic"]["value"] != w["check"]["value"]
    assert set(rc["verbs"]) == {"ribeiro", "campos", "r2610"}
    assert rc["verbs"]["campos"]["counts"]["n"] == 5
    assert "ribeiro_lat_minus_intrinsic" in rc["descriptive"]
    idx = json.loads((res / "INDEX.json").read_text())["files"]
    for name in ("reconciliation.json", "generation_shift.json", "operational.json"):
        assert idx[name]["sha256"] == sha256_file(res / name)


def test_mixed_tiebreaks_raise():
    from analysis.ranking import lex_keys
    with pytest.raises(ValueError):
        lex_keys(np.array([0.1, 0.2, 0.3]), np.array([1.0, np.nan, 2.0]))
