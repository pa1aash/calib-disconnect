"""Probes, verbal readouts, isotonic maps, unsupervised readouts, CODETEXT, LAT, and the no-test-fold audit."""

import re

import numpy as np
import pytest
from sklearn.metrics import roc_auc_score

from pipeline.contracts import constants as K
from pipeline.contracts.schemas import ReadoutScore
from pipeline.readouts.codetext import crossfit_codetext
from pipeline.readouts.common import Folds, audit_fits
from pipeline.readouts.isotonic import crossfit_isotonic, drop_inner_split, fit_isotonic
from pipeline.readouts.lat import crossfit_lat
from pipeline.readouts.probe import ProbeReadout, crossfit_family, crossfit_mlp, crossfit_prompt
from pipeline.readouts.unsupervised import (agreement_scores, ast_cluster_scores, ast_signature, normalize_signature,
                                            tl_scores)
from pipeline.readouts.verbal import v1_parse_report, v1_scores, v1_train_scores, v2_scores
from readouts_helpers import make_data, make_plan

pytestmark = pytest.mark.filterwarnings("ignore")


@pytest.fixture(scope="module")
def data():
    return make_data()


@pytest.fixture(scope="module")
def plan(data):
    return make_plan(set(data.problem_ids))


def auroc(data, rows, suite="E"):
    idx = {u: i for i, u in enumerate(data.sample_uids)}
    y = [data.labels[suite][idx[r.sample_uid]] for r in rows]
    return roc_auc_score(y, [r.rank_score for r in rows])


# ---------------------------------------------------------------------------------------------------
# No test-fold information in any fit
# ---------------------------------------------------------------------------------------------------
def _check_audit(records, plan, minimum_folds=5):
    seen = set()
    for tag, pids in records:
        m = re.search(r"outer(\d+)", tag)
        assert m, tag
        f = int(m.group(1))
        seen.add(f)
        test = set(plan.outer_test(f))
        assert not (pids & test), f"{tag} saw test-fold problems of outer fold {f}"
        assert pids <= set(plan.outer_train(f)), tag
    assert len(seen) >= minimum_folds


def test_fits_never_see_the_outer_test_fold(data, plan):
    from pipeline.readouts.adapter_readout import AdapterReadout
    from pipeline.readouts.recipe import RecipeTable
    from pipeline.readouts.surrogate import SurrogateTrainer, surrogate_features
    with audit_fits() as rec:
        crossfit_family(data, plan, "E", "MOCK", "label_validity")
        crossfit_prompt(data, plan, "E", "MOCK", "label_validity")
        crossfit_mlp(data, plan, "E", "MOCK", "label_validity", wd_grid=(1e-2,))
        crossfit_codetext(data, plan, "E", "MOCK", "label_validity")
        crossfit_lat(data, plan, "E", "MOCK", "label_validity")
        v1 = v1_scores(data, plan, "MOCK", "label_validity")
        crossfit_isotonic(v1, data, plan, "E", v1_train_scores(data, plan, "MOCK", "label_validity"))
        ar = AdapterReadout("ST", SurrogateTrainer(surrogate_features(data)), RecipeTable(), select=True, inner_adapters=True)
        res = ar.crossfit_full(data, plan, "E", "MOCK", "label_validity")
        crossfit_isotonic(res.scores, data, plan, "E", res.inner_train_scores)
    kinds = {t.split(":")[0] for t, _ in rec}
    assert {"probe", "prompt", "mlp", "codetext", "lat", "v1_median", "isotonic", "adapter_select", "adapter_final",
            "adapter_inner1"} <= kinds
    _check_audit(rec, plan)


# ---------------------------------------------------------------------------------------------------
# Probes
# ---------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def family(data, plan):
    return crossfit_family(data, plan, "E", "MOCK", "label_validity")


def test_probe_family_outputs(data, plan, family):
    assert set(family.scores) == {"P", "P2", "P3", "Pmulti", "P2_single_split"}
    n = len(data.sample_uids)
    for name, rows in family.scores.items():
        assert len(rows) == n, name
        assert len({r.sample_uid for r in rows}) == n
        assert all(0.0 <= r.prob <= 1.0 and np.isnan(r.rank_tiebreak) for r in rows)
        assert [f.outer_fold for f in family.fits[name]] == [0, 1, 2, 3, 4]
        assert all(f.fold_seed == 0 and f.label_suite == "E" for f in family.fits[name])
        assert all(r.fold == plan.assignment[p] for r, p in zip(rows, [data.problem_ids[data.sample_uids.index(r.sample_uid)] for r in rows]))
    assert auroc(data, family.scores["P2"]) > 0.8       # the planted direction is in layer 1 at p2
    assert auroc(data, family.scores["P"]) > 0.8
    for fit in family.fits["P2"]:
        assert fit.selected["member"] == "P2" and fit.selected["layer"] == 1
        assert fit.selected["C"] in K.PROBE_C_GRID
    for fit in family.fits["P"]:
        assert fit.selected["member"] in ("P2", "P3", "Pmulti")
        assert fit.inner_val_logloss < fit.base_rate_logloss
    for fit in family.fits["P2_single_split"]:
        assert fit.selected["selected_on"] == "first inner split"
    # P is the member with the lowest inner CV loss
    for f in range(5):
        losses = {m: [x for x in family.fits[m] if x.outer_fold == f][0].inner_val_logloss for m in ("P2", "P3", "Pmulti")}
        pf = [x for x in family.fits["P"] if x.outer_fold == f][0]
        assert pf.selected["member"] == min(losses, key=losses.get)
        assert pf.inner_val_logloss == pytest.approx(min(losses.values()))


def test_probe_readout_protocol_shares_cache(data, plan):
    cache = {}
    a = ProbeReadout("P3", cache).crossfit(data, plan, "E", "MOCK", "label_validity")
    b = ProbeReadout("Pmulti", cache).crossfit(data, plan, "E", "MOCK", "label_validity")
    assert len(cache) == 1 and len(a[0]) == len(b[0]) == len(data.sample_uids)


def test_pmulti_pca_is_capped_at_training_rank(data, plan):
    # 160 samples, 7 candidate layers are not needed: the cap is min(512, n_train - 1, n_features)
    fam = crossfit_family(data, plan, "E", "MOCK", "label_validity", want=("Pmulti",))
    assert len(fam.scores["Pmulti"]) == len(data.sample_uids)


def test_prompt_probe_is_constant_within_a_problem(data, plan):
    rows, fits = crossfit_prompt(data, plan, "E", "MOCK", "label_validity")
    by = {}
    pid_of = dict(zip(data.sample_uids, data.problem_ids))
    for r in rows:
        by.setdefault(pid_of[r.sample_uid], set()).add(round(r.rank_score, 9))
    assert all(len(v) == 1 for v in by.values())
    assert len(fits) == 5 and fits[0].selected["position"] == "p1"


def test_mlp_probe(data, plan):
    rows, fits = crossfit_mlp(data, plan, "E", "MOCK", "label_validity", wd_grid=(1e-3, 1e-1))
    assert len(rows) == len(data.sample_uids) and len(fits) == 5
    assert fits[0].selected["width"] == K.MLP_PROBE_WIDTH and fits[0].selected["weight_decay"] in (1e-3, 1e-1)
    assert auroc(data, rows) > 0.6


def test_single_class_training_falls_back_to_base_rate(data, plan):
    d = make_data(n_problems=10, k=2)
    d.labels["E"][:] = 1
    fam = crossfit_family(d, make_plan(set(d.problem_ids)), "E", "MOCK", "label_validity", want=("P2",))
    probs = {round(r.prob, 4) for r in fam.scores["P2"]}
    assert len(probs) == 1 and probs.pop() > 0.99


# ---------------------------------------------------------------------------------------------------
# Verbal readouts
# ---------------------------------------------------------------------------------------------------
def test_v1_imputation_uses_training_folds_only(data, plan):
    rows = {r.sample_uid: r for r in v1_scores(data, plan, "MOCK", "label_validity")}
    pid = dict(zip(data.sample_uids, data.problem_ids))
    for f in range(5):
        train_vals = [c.v1_value for c, p in zip(data.capture, data.problem_ids)
                      if c.v1_value is not None and plan.assignment[p] != f]
        med = float(np.median(train_vals))
        for c in data.capture:
            r = rows[c.sample_uid]
            if plan.assignment[pid[c.sample_uid]] != f:
                continue
            if c.v1_value is None:
                assert r.missing and r.imputed and r.prob == pytest.approx(med) and r.rank_score == pytest.approx(med)
            else:
                assert not r.missing and not r.imputed and r.prob == c.v1_value
    # changing test-fold values leaves the imputed value of that fold unchanged
    import copy
    d2 = copy.deepcopy(data)
    for c, p in zip(d2.capture, d2.problem_ids):
        if plan.assignment[p] == 0 and c.v1_value is not None:
            object.__setattr__(c, "v1_value", 0.99)
    rows2 = {r.sample_uid: r for r in v1_scores(d2, plan, "MOCK", "label_validity")}
    for u, r in rows.items():
        if r.fold == 0 and r.imputed:
            assert rows2[u].prob == pytest.approx(r.prob)


def test_v1_drop_variant_parse_rate_and_k3(data, plan):
    drop = v1_scores(data, plan, "MOCK", "label_validity", drop_missing=True)
    n_parsed = sum(c.v1_value is not None for c in data.capture)
    assert len(drop) == n_parsed and not any(r.missing or r.imputed for r in drop)
    rep = v1_parse_report(data)
    assert rep["n_parsed"] == n_parsed and rep["parse_rate"] == pytest.approx(n_parsed / len(data.capture))
    assert rep["k3_switch_to_v2"] == (rep["parse_rate"] < K.K3_MIN_V1_PARSE_RATE)
    low = make_data(n_problems=10, k=2, v1_missing=0.5)
    assert v1_parse_report(low)["k3_switch_to_v2"] is True
    hi = make_data(n_problems=10, k=2, v1_missing=0.0)
    assert v1_parse_report(hi) == {"n": 20, "n_parsed": 20, "parse_rate": 1.0, "k3_switch_to_v2": False}


def test_v2_is_float32_logodds_and_never_missing(data):
    rows = v2_scores(data, "MOCK", "label_validity")
    for r, c in zip(rows, data.capture):
        assert r.rank_score == float(np.float32(c.yes_no_logodds)) and not r.missing
        assert r.prob == pytest.approx(1 / (1 + np.exp(-r.rank_score)))
        assert r.label_suite is None and r.fold_seed is None


# ---------------------------------------------------------------------------------------------------
# Isotonic
# ---------------------------------------------------------------------------------------------------
def test_isotonic_tie_rule_clip_and_values(data, plan):
    v1 = v1_scores(data, plan, "MOCK", "label_validity")
    out = crossfit_isotonic(v1, data, plan, "E", v1_train_scores(data, plan, "MOCK", "label_validity"))
    assert len(out) == len(v1)
    src = {r.sample_uid: r for r in v1}
    pid = dict(zip(data.sample_uids, data.problem_ids))
    for r in out:
        assert r.readout == "iso:SZ_V1" and r.prob == r.rank_score and 0.0 <= r.prob <= 1.0
        assert r.rank_tiebreak == src[r.sample_uid].rank_score
        assert r.label_suite == "E" and r.fold == plan.assignment[pid[r.sample_uid]]
    # within a problem the lexicographic order (iso value, pre-map score) equals the pre-map order
    by = {}
    for r in out:
        by.setdefault(pid[r.sample_uid], []).append(r)
    for rows in by.values():
        pre = sorted(rows, key=lambda r: r.rank_tiebreak)
        lex = sorted(rows, key=lambda r: (r.rank_score, r.rank_tiebreak))
        assert [r.rank_tiebreak for r in pre] == [r.rank_tiebreak for r in lex]


def test_isotonic_fit_clip_and_single_class():
    m = fit_isotonic([0.1, 0.2, 0.3, 0.4], [0, 0, 1, 1])
    assert list(m([-5.0, 99.0])) == [0.0, 1.0]            # out_of_bounds = clip
    m1 = fit_isotonic([0.1, 0.2, 0.3], [1, 1, 1])
    assert np.allclose(m1([0.0, 0.5]), 1 - 1e-6)           # single class: the training base rate
    m0 = fit_isotonic([0.1, 0.2, 0.3, 0.4], [1, 0, 0, 1])
    assert np.all(np.diff(m0([0.1, 0.2, 0.3, 0.4])) >= 0)


def test_isotonic_train_scores_replace_own_scores(data, plan):
    pid = dict(zip(data.sample_uids, data.problem_ids))
    rng = np.random.default_rng(0)
    rows = [ReadoutScore(u, "MOCK", "label_validity", "X", None, None, None, 0.5, float(rng.normal()), float("nan"))
            for u in data.sample_uids]
    # a training set that is a constant function of the score: with y = 1 above 0 and 0 below, the map is a step
    train = {f: [ReadoutScore(r.sample_uid, "MOCK", "label_validity", "X", None, None, None, 0.5, r.rank_score, float("nan"))
                 for r in rows if plan.assignment[pid[r.sample_uid]] != f] for f in range(5)}
    data2 = make_data()
    data2.labels["E"][:] = np.array([int(r.rank_score > 0) for r in rows], dtype=np.int8)
    out = crossfit_isotonic(rows, data2, plan, "E", train)
    assert all((r.prob > 0.5) == (r.rank_tiebreak > 0) for r in out if abs(r.rank_tiebreak) > 0.3)
    # inner splits 2 to 4 only: rows of the first inner validation fold are dropped
    sub = drop_inner_split(train, data2, plan, 0)
    for f in range(5):
        drop_fold = [g for g in range(5) if g != f][0]
        assert all(plan.assignment[pid[r.sample_uid]] not in (f, drop_fold) for r in sub[f])


def test_isotonic_skips_missing_rows(data, plan):
    r = [ReadoutScore(data.sample_uids[0], "MOCK", "label_validity", "AGREE", None, None, None, np.nan, np.nan, np.nan, missing=True)]
    assert crossfit_isotonic(r, data, plan, "E") == []


# ---------------------------------------------------------------------------------------------------
# Unsupervised readouts, hand-made cases
# ---------------------------------------------------------------------------------------------------
def _mini(codes, sigs=None, lps=None):
    from pipeline.contracts.interfaces import ReadoutData
    n = len(codes)
    pids = [f"HumanEval/{i // 3}" for i in range(n)]
    uids = [f"MOCK|frozen|humaneval_plus|{p}|{i}" for i, p in enumerate(pids)]
    return ReadoutData(sample_uids=uids, problem_ids=pids, labels={}, code_texts=codes,
                       agreement_outputs=None if sigs is None else dict(zip(uids, sigs)),
                       code_logprobs=lps)


def test_token_likelihood_variants():
    lp = [np.log(np.array([0.5, 0.25], dtype=np.float32)), np.array([], dtype=np.float32), np.log(np.array([0.9], dtype=np.float32))]
    d = _mini(["a", "b", "c"], lps=lp)
    r = tl_scores(d, "MOCK", "label_validity")
    assert r["TL_geo"][0].prob == pytest.approx(np.sqrt(0.125), rel=1e-5)
    assert r["TL_min"][0].prob == pytest.approx(0.25, rel=1e-5)
    assert r["TL_sum"][0].rank_score == pytest.approx(np.log(0.125), rel=1e-5)
    assert r["TL_sum"][0].prob == pytest.approx(0.125, rel=1e-5)
    assert r["TL_geo"][1].missing and r["TL_geo"][1].prob == 0.0
    assert r["TL_sum"][1].rank_score < min(r["TL_sum"][0].rank_score, r["TL_sum"][2].rank_score)
    assert not r["TL_geo"][2].missing and r["TL_geo"][2].prob == pytest.approx(0.9, rel=1e-5)


def test_agreement_share_of_other_samples():
    a, b, c = ("1", "2"), ("1", "2.0000000001"), ("9", "9")
    # problem 0: a, b (equal after 9-digit normalization), c; problem 1: no agreement inputs; problem 2: one sample
    d = _mini(["x"] * 7, sigs=[a, b, c, None, None, None, a])
    assert normalize_signature(a) == normalize_signature(b)
    rows = agreement_scores(d, "MOCK", "label_validity")
    s = {r.sample_uid: r for r in rows["AGREE"]}
    u = d.sample_uids
    assert s[u[0]].prob == pytest.approx(0.5) and s[u[1]].prob == pytest.approx(0.5) and s[u[2]].prob == 0.0
    assert all(s[x].missing and np.isnan(s[x].prob) for x in u[3:6])   # no inputs: missing, never imputed
    assert s[u[6]].missing                                              # single sample: undefined
    p = {r.sample_uid: r for r in rows["AGREE_problem"]}
    assert p[u[0]].prob == pytest.approx(2 / 3) and p[u[2]].prob == pytest.approx(2 / 3)


def test_agreement_float_normalization_and_none_sample():
    assert normalize_signature(("0.1234567891",)) == normalize_signature(("0.1234567894",))
    assert normalize_signature(("0.123456",)) != normalize_signature(("0.123457",))
    d = _mini(["x"] * 3, sigs=[("1",), ("1",), None])
    s = {r.sample_uid: r.prob for r in agreement_scores(d, "MOCK", "label_validity")["AGREE"]}
    assert list(s.values()) == [0.5, 0.5, 0.0]       # a sample without a signature agrees with no one


def test_ast_renaming_docstrings_and_singletons():
    a = 'def f(x, y):\n    """Add."""\n    # comment\n    t = x + y\n    return t\n'
    b = 'def g(p, q):\n    s = p + q\n    return s\n'
    c = 'def f(x, y):\n    t = x - y\n    return t\n'
    e = "def f(:\n"
    d = _mini([a, b, c, e, None, "def h(z):\n    return len(z)\n"])
    assert ast_signature(a) == ast_signature(b) and ast_signature(a) != ast_signature(c)
    assert ast_signature(e) is None and ast_signature(None) is None
    sc = {r.sample_uid: r.prob for r in ast_cluster_scores(d, "MOCK", "label_validity")}
    u = d.sample_uids
    assert sc[u[0]] == sc[u[1]] == pytest.approx(2 / 3) and sc[u[2]] == pytest.approx(1 / 3)
    assert sc[u[3]] == pytest.approx(1 / 3) and sc[u[4]] == pytest.approx(1 / 3)   # unparseable: singletons
    assert sc[u[5]] == pytest.approx(1 / 3)
    # builtins and library names are not renamed
    assert "len" in ast_signature("def h(z):\n    return len(z)\n")


# ---------------------------------------------------------------------------------------------------
# CODETEXT and LAT
# ---------------------------------------------------------------------------------------------------
def test_codetext_reads_surface_text_only():
    d = make_data(n_problems=40, k=4)
    plan = make_plan(set(d.problem_ids))
    rows, fits = crossfit_codetext(d, plan, "E", "MOCK", "label_validity")
    assert len(rows) == len(d.sample_uids) and len(fits) == 5
    assert all(f.selected["C"] in K.PROBE_C_GRID and f.selected["ngram_range"] == [3, 5] for f in fits)
    assert auroc(d, rows) > 0.8     # "+ 1" versus "- 1" is visible in the text


def test_codetext_empty_vocabulary_falls_back():
    d = make_data(n_problems=10, k=2)
    d.code_texts = ["ab"] * len(d.sample_uids)   # shorter than 3 characters: no n-gram at all
    rows, _ = crossfit_codetext(d, make_plan(set(d.problem_ids)), "E", "MOCK", "label_validity")
    assert len({round(r.prob, 6) for r in rows}) <= 5


def test_lat_direction_and_sign():
    d = make_data()
    plan = make_plan(set(d.problem_ids))
    rows, fits = crossfit_lat(d, plan, "E", "MOCK", "label_validity")
    assert len(rows) == len(d.sample_uids)
    assert all(f.selected["layer"] == 1 for f in fits)
    assert auroc(d, rows) > 0.8      # sign aligned: passing samples score higher
