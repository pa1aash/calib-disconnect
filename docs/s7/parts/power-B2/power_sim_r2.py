"""Design-stage power simulation, wave 7 (power-B2), revision of docs/s6/power/power_sim.py.

Planning arithmetic under stated assumptions, not a result. No study data are used.

What changed relative to wave 6 (B9):
  1. Between-model heterogeneity (fixed-effects: residual deviations centered so the named-model mean
     is exactly R*; random-effects variant uncentered, sensitivity only), in the residual gap, probe
     within-AUROC, zero-shot stated within-AUROC, difficulty loadings, and weak-suite false-pass fraction.
  2. Per-model pass-probability distributions Beta(mu*kappa, (1-mu)*kappa) with kappa fit to published anchors
     (analysis in the "mixed" block of the JSON), problem difficulty correlated across models (Gaussian copula).
  3. Readout-estimation noise: per-model, per-fold-seed relative perturbation of the separation of the trained
     readout (LoRA) and, smaller, of the probe; refit variance s_refit^2 computed from three fold seeds with the
     LoRA share scaled by M / (number of sub-study models), and the interval widened as in R1 section 9.
  4. Lexicographic tie rule for recalibrated scores (R1 section 1.2): within-problem W of a recalibrated score
     equals W of the pre-map score; pooled AUROC ranks by (isotonic value, pre-map bin).
  5. Three decisions (D1, D2, D3), two margins, k in {10, 20}, a sweep over n for the mixed-count threshold.

Run:  python3 -I docs/s7/parts/power-B2/power_sim_r2.py [--quick] [--config PATH] [--workers N] [--out PATH]
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"

import json
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from scipy.special import betaincinv, betaln, ndtr, ndtri

HERE = Path(__file__).resolve().parent
QUICK = "--quick" in sys.argv


def _arg(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


BASE_SEED = 20261110
A_P0, A_S0 = 0.8, 0.3
HET_SD = 0.3                    # per-problem separation shift, shared by both readouts of one model (as in B9)
SHOCK_SD = 0.05 / 0.26          # per-model per-problem probe shock (as in B9)
RHO_E = 0.5                     # corr(e_P, e_S) (as in B9)
RHO_D = 0.7                     # copula correlation of problem difficulty across models (assumption)
F_FP0 = 0.08
D_GRID = np.array([0.0, 0.25, 0.5, 0.8, 1.2, 1.7, 2.3, 3.0])
Z90 = 1.645

# ------------------------------------------------------------------ literature values (file:line cited in JSON/MD)
LIT = {
    "ribeiro_2512.07404_file": "research/positioning/w4/parts/fetcher-l2/raw/2512.07404v3.txt",
    "qwen25coder7b_random_pass_at_rank1_T1": 0.645,   # Table 5, extraction lines 1349-1350 (column order inferred)
    "qwen25coder7b_pass_at_10_ceiling_T1": 0.959,     # prose line 1558
    "qwen25coder7b_pass_at_1_baseline_T02": 0.851,    # prose, Sec 5.2.2 (85.1 percent), line near 1313
    "mistral7b_v03_random_pass_at_rank1_T1": 0.380,   # prose line 1292 and Table 5 line 1349
    "mistral7b_v03_pass_at_10_ceiling_T1": 0.678,     # prose lines 1308 and 1841
    "mistral7b_v03_pass_at_1_baseline_T02": 0.347,    # prose line 1292
    "n_tasks": 121,
    # 2610.31820 Table 3, code AUROC (ID, OOD): research/positioning/w5/parts/ft-A4b/raw/ft/2610.31820.txt
    # (Qwen3-8B: Verbalized .60/.61, R-Tuning .86/.85, Probe .88/.84; Nemotron-Cascade-8B: .58/.60, .89/.79, .89/.80)
    "t3_verbalized": [0.60, 0.61, 0.58, 0.60],
    "t3_rtuning": [0.86, 0.85, 0.89, 0.79],
    "t3_probe": [0.88, 0.84, 0.89, 0.80],
    # Campos 2611.07876 Table V (txt lines 541-558), within-problem AUROC in distribution
    "campos_within_id": {"Qwen3-Coder-30B": {"judging_pass": 0.553, "code_token": 0.620, "prompt_token": 0.514},
                         "gpt-oss-20b": {"judging_pass": 0.772, "code_token": 0.781, "prompt_token": 0.524}},
}


def sd1(x):
    return float(np.std(np.asarray(x, float), ddof=1))


def derive_taus():
    """Derive heterogeneity SDs from the literature values above; every derivation is returned as text."""
    v, r, p = (np.array(LIT[k]) for k in ("t3_verbalized", "t3_rtuning", "t3_probe"))
    c = LIT["campos_within_id"]
    d_rt = r - p                                               # pooled R-Tuning minus probe
    g_verb = p - v                                             # pooled probe minus verbalized (G0-like)
    camp_gap = [c[m]["judging_pass"] - c[m]["code_token"] for m in c]   # within-problem judging minus code-token probe
    camp_probe = [c[m]["code_token"] for m in c]
    d = {
        "sd_rtuning_minus_probe_pooled": sd1(d_rt), "values_rtuning_minus_probe": [round(float(x), 3) for x in d_rt],
        "sd_probe_minus_verbalized_pooled_G0like": sd1(g_verb), "values_probe_minus_verbalized": [round(float(x), 3) for x in g_verb],
        "sd_probe_pooled_across_4": sd1(p), "sd_verbalized_pooled_across_4": sd1(v),
        "campos_judging_minus_codetoken_within": [round(x, 3) for x in camp_gap], "sd_campos_gap_within_n2": sd1(camp_gap),
        "campos_codetoken_probe_within": camp_probe, "sd_campos_codetoken_probe_within_n2": sd1(camp_probe),
        "campos_max_abs_gap_within": float(max(abs(x) for x in camp_gap)),
    }
    return d


DER = derive_taus()

# Heterogeneity settings. Each SD is between-model, in the units of the quantity it perturbs.
HETS = {
    "nominal": {
        "tau_R": 0.02, "tau_P": 0.04, "tau_0": 0.02, "tau_aP": 0.22, "tau_aS": 0.11, "tau_f": 0.03,
        "source": {
            "tau_R": "SD of pooled R-Tuning minus probe over the 4 model-split cells of 2610.31820 Table 3 code = %.4f, rounded to 0.02" % DER["sd_rtuning_minus_probe_pooled"],
            "tau_P": "SD of the 4 pooled probe AUROCs of 2610.31820 Table 3 code = %.4f, rounded to 0.04 and applied to within-problem AUROC (assumption: same order of spread)" % DER["sd_probe_pooled_across_4"],
            "tau_0": "SD of the 4 pooled verbalized AUROCs of 2610.31820 Table 3 code = %.4f, rounded up to 0.02" % DER["sd_verbalized_pooled_across_4"],
            "tau_aP/tau_aS": "no direct literature value; tuned (16-world population check: 0.15/0.08 gives G0 SD 0.039, 0.25/0.12 gives 0.053; 0.22/0.11 chosen) so the between-model SD of the raw gap G0 matches the SD of the 4 pooled probe-minus-verbalized gaps = %.4f (check in heterogeneity_check block)" % DER["sd_probe_minus_verbalized_pooled_G0like"],
            "tau_f": "assumption (no located source): SD 0.03 around a 0.08 false-pass fraction of failing samples",
        }},
    "conservative": {
        "tau_R": 0.04, "tau_P": 0.08, "tau_0": 0.03, "tau_aP": 0.30, "tau_aS": 0.15, "tau_f": 0.05,
        "source": {
            "tau_R": "SD of the two Campos Table V within-problem gaps (judging-pass minus code-token probe: Qwen3-Coder, gpt-oss) = %.4f (n = 2), rounded to 0.04" % DER["sd_campos_gap_within_n2"],
            "tau_P": "twice nominal; the Campos code-token probe within-problem AUROCs (.620, .781) have SD %.4f (n = 2), larger still (see extreme)" % DER["sd_campos_codetoken_probe_within_n2"],
            "tau_0": "1.5 times nominal",
            "tau_aP/tau_aS": "twice nominal",
            "tau_f": "assumption: 0.05",
        }},
    "extreme": {
        "tau_R": 0.06, "tau_P": 0.114, "tau_0": 0.05, "tau_aP": 0.40, "tau_aS": 0.20, "tau_f": 0.08,
        "source": {
            "tau_R": "just under the larger Campos within-problem gap in absolute value (%.3f), used as a model-level SD (a deliberate overstatement)" % DER["campos_max_abs_gap_within"],
            "tau_P": "SD of the Campos code-token probe within-problem AUROCs (n = 2) = %.4f" % DER["sd_campos_codetoken_probe_within_n2"],
            "others": "assumptions, larger than conservative"}},
}
HET_ID = {"nominal": 0, "conservative": 1, "extreme": 2}
KAPPA_ID = {"k080": 0, "k183": 1, "k040": 2}

REFIT = {"nominal": {"rel_lora": 0.10, "rel_probe": 0.05}}   # relative SD of the separation per fold seed


# ------------------------------------------------------------------ pass-probability model (analytic)
def e_pk(mu, kap, k):
    a, b = mu * kap, (1 - mu) * kap
    return math.exp(betaln(a + k, b) - betaln(a, b))


def e_qk(mu, kap, k):
    a, b = mu * kap, (1 - mu) * kap
    return math.exp(betaln(a, b + k) - betaln(a, b))


def mixed_frac(mu, kap, k):
    return 1.0 - e_pk(mu, kap, k) - e_qk(mu, kap, k)


def fit_kappa(mu, ceiling, k=10):
    return brentq(lambda kap: 1.0 - e_qk(mu, kap, k) - ceiling, 0.05, 500.0)


def kappa_analysis():
    n = LIT["n_tasks"]
    out = {}
    for name, mu, ce in (("Qwen2.5-Coder-7B-Instruct", LIT["qwen25coder7b_random_pass_at_rank1_T1"], LIT["qwen25coder7b_pass_at_10_ceiling_T1"]),
                         ("Mistral-7B-Instruct-v0.3", LIT["mistral7b_v03_random_pass_at_rank1_T1"], LIT["mistral7b_v03_pass_at_10_ceiling_T1"])):
        se = math.sqrt(ce * (1 - ce) / n)
        row = {"mu_T1": mu, "ceiling": ce, "ceiling_binomial_se_n121": round(se, 4)}
        for lab, c in (("kappa", ce), ("kappa_ceiling_minus1se", ce - se), ("kappa_ceiling_plus1se", min(ce + se, 0.9995))):
            try:
                row[lab] = round(fit_kappa(mu, c), 3)
            except ValueError:
                row[lab] = None
        row["mixed_frac_k10"] = round(mixed_frac(mu, row["kappa"], 10), 4)
        row["mixed_frac_k20"] = round(mixed_frac(mu, row["kappa"], 20), 4)
        out[name] = row
    return out


# ------------------------------------------------------------------ scoring primitives
def nums_pairs(s, lab, chunk=3000):
    """Per-problem count of correctly ordered pass-fail pairs (ties half) and number of pairs."""
    n = s.shape[0]
    num = np.empty(n)
    for a in range(0, n, chunk):
        ss, ll = s[a:a + chunk], lab[a:a + chunk]
        d = ss[:, :, None] - ss[:, None, :]
        m = ll[:, :, None] & ~ll[:, None, :]
        num[a:a + chunk] = ((d > 0) & m).sum((1, 2)) + 0.5 * ((d == 0) & m).sum((1, 2))
    npass = lab.sum(1)
    return num, (npass * (lab.shape[1] - npass)).astype(float)


def to_bin(s):
    return np.rint(10.0 / (1.0 + np.exp(-s))).astype(np.int64)


def make_W(rng, n, B):
    idx = rng.integers(0, n, size=(B, n))
    flat = (idx + np.arange(B)[:, None] * n).ravel()
    W = np.bincount(flat, minlength=B * n).reshape(B, n).astype(float)
    return np.vstack([np.ones((1, n)), W])


def ratio(Wall, num, pr):
    den = Wall @ pr
    return np.where(den > 0, (Wall @ num) / np.where(den > 0, den, 1.0), np.nan)


# ------------------------------------------------------------------ worlds (model-level parameters)
def make_world(het_name, w, models, fe=True):
    H = HETS[het_name]
    M = len(models)
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, 10, HET_ID[het_name], w]))
    u = rng.normal(0, H["tau_R"], M)
    if fe:
        u = u - u.mean()
    auc_P = np.clip(0.72 + rng.normal(0, H["tau_P"], M), 0.56, 0.92)
    auc_0 = np.clip(0.60 + rng.normal(0, H["tau_0"], M), 0.52, 0.75)
    aP = np.clip(A_P0 + rng.normal(0, H["tau_aP"], M), 0.1, None)
    aS = np.clip(A_S0 + rng.normal(0, H["tau_aS"], M), 0.0, None)
    f = np.clip(F_FP0 + rng.normal(0, H["tau_f"], M), 0.01, 0.30)
    return {"u": u, "D_P": math.sqrt(2) * ndtri(auc_P), "D_0": math.sqrt(2) * ndtri(auc_0), "auc_P": auc_P,
            "auc_0": auc_0, "aP": aP, "aS": aS, "f": f}


def draw_p_models(rng, n, models, kappa):
    g = rng.normal(size=n)
    e = rng.normal(size=(n, len(models)))
    U = np.clip(ndtr(math.sqrt(RHO_D) * g[:, None] + math.sqrt(1 - RHO_D) * e), 1e-12, 1 - 1e-12)
    p = np.empty_like(U)
    for m, mod in enumerate(models):
        a, b = mod["mu"] * kappa, (1 - mod["mu"]) * kappa
        p[:, m] = betaincinv(a, b, U[:, m])
    return p


def std_logit(p):
    pc = np.clip(p, 1e-3, 1 - 1e-3)
    lg = np.log(pc / (1 - pc))
    sd = lg.std()
    return (lg - lg.mean()) / (sd if sd > 0 else 1.0)


def draw_noise(rng, p, k):
    n = len(p)
    y = rng.random((n, k)) < p[:, None]
    het = rng.normal(0, HET_SD, n)
    shock = rng.normal(0, SHOCK_SD, n)
    eP = rng.normal(size=(n, k))
    eS = RHO_E * eP + math.sqrt(1 - RHO_E ** 2) * rng.normal(size=(n, k))
    return y, het, shock, eP, eS


# ------------------------------------------------------------------ calibration of the trained separation
def calib_world(task):
    """Population within-AUROC of the probe and of the stated readout over a grid of separations, per model."""
    het, kid, kap, k, w, ncal, models = (task[x] for x in ("het", "kid", "kappa", "k", "w", "ncal", "models"))
    world = make_world(het, w, models)
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, 11, HET_ID[het], KAPPA_ID[kid], k, w]))
    out = []
    for m, mod in enumerate(models):
        p = rng.beta(mod["mu"] * kap, (1 - mod["mu"]) * kap, ncal)
        z = std_logit(p)
        y, het_, shock, eP, eS = draw_noise(rng, p, k)
        sP = np.maximum(world["D_P"][m] + het_ + shock, 0)[:, None] * y + world["aP"][m] * z[:, None] + eP
        nP, pr = nums_pairs(sP, y)
        base = world["aS"][m] * z[:, None] + eS
        ws = []
        for d in D_GRID:
            sS = to_bin(np.maximum(d + het_, 0)[:, None] * y + base)
            nS, _ = nums_pairs(sS, y)
            ws.append(float(nS.sum() / pr.sum()))
        nS0, _ = nums_pairs(to_bin(np.maximum(world["D_0"][m] + het_, 0)[:, None] * y + base), y)
        out.append({"W_P": float(nP.sum() / pr.sum()), "W_S_grid": ws, "W_S_zeroshot": float(nS0.sum() / pr.sum()),
                    "mixed_frac": float((pr > 0).mean()), "pass_rate": float(y.mean())})
    return {"het": het, "kid": kid, "k": k, "w": w, "models": out}


def d1_for(cal_m, target_W):
    """Invert the monotone W_S(d) curve at target; returns (d1, clipped_flag)."""
    W = np.maximum.accumulate(np.array(cal_m["W_S_grid"]))
    W = W + 1e-9 * np.arange(len(W))
    lo, hi = W[0], W[-1]
    clipped = bool(target_W < lo or target_W > hi)
    t = float(np.clip(target_W, lo, hi))
    return float(PchipInterpolator(W, D_GRID)(t)), clipped


# ------------------------------------------------------------------ decision cells
R_LIST = [0.0, 0.02, 0.03, 0.04, 0.06, -0.04, -0.06]


def run_group(task):
    """One (het, mode, kappa, k, n, world) group: reps replicates, all R* values with common random numbers."""
    het, mode, kid, kap, k, n, w = (task[x] for x in ("het", "mode", "kid", "kappa", "k", "n", "w"))
    reps, B, models, cal = task["reps"], task["B"], task["models"], task["cal"]
    stream = task.get("stream", 12)
    rel_L, rel_P = task["rel_lora"], task["rel_probe"]
    active = task.get("active", list(range(len(models))))
    sub = task["sub"]                       # indices (into the full model list) of the refit sub-study models
    share_het = task.get("share_het", False)
    Rs = task.get("R_list", R_LIST)
    fe = mode == "FE"
    world = make_world(het, w, models, fe=fe)
    Ma = len(active)
    sub_a = [m for m in active if m in sub]
    scale = Ma / max(len(sub_a), 1)
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, stream, HET_ID[het], KAPPA_ID[kid], k, n, w]))
    # d1 per (model, R*)
    d1 = np.zeros((len(models), len(Rs)))
    nclip = 0
    for m in active:
        for ri, R in enumerate(Rs):
            tgt = cal["models"][m]["W_P"] - (R + world["u"][m])
            d1[m, ri], cl = d1_for(cal["models"][m], tgt)
            nclip += cl
    out = np.full((reps, len(Rs), 8), np.nan)    # pt, L, U, Lw, Uw, s_probe, s_lora, hw_raw
    mixed = np.zeros(reps)
    for rep in range(reps):
        p = draw_p_models(rng, n, models, kap)
        Wall = make_W(rng, n, B)
        epsP = rng.normal(0, rel_P, (len(models), 3))
        epsS = rng.normal(0, rel_L, (len(models), 3))
        shared = draw_noise(rng, p[:, active[0]], k) if share_het else None
        boot = np.zeros((len(Rs), B + 1))
        Rp = np.zeros((len(Rs), 3))
        Rl = np.zeros((len(Rs), 3))
        mx = 0
        for m in active:
            pm = p[:, m]
            z = std_logit(pm)
            y, het_, shock, eP, eS = draw_noise(rng, pm, k)
            if share_het:
                het_, shock = shared[1], shared[2]
            base = world["aS"][m] * z[:, None] + eS
            dpb = np.maximum(world["D_P"][m] + het_ + shock, 0)
            nPs = []
            for s in range(3):
                sP = (dpb * (1 + epsP[m, s]))[:, None] * y + world["aP"][m] * z[:, None] + eP
                num, pr = nums_pairs(sP, y)
                nPs.append(num)
            mx += (pr > 0).sum()
            WP0 = ratio(Wall, nPs[0], pr)
            WPs = [WP0[0]] + [nPs[s].sum() / pr.sum() for s in (1, 2)]
            for ri in range(len(Rs)):
                ds = np.maximum(d1[m, ri] + het_, 0)
                ws_boot = None
                ws_pts = []
                for s in range(3):
                    if s > 0 and m not in sub_a:
                        ws_pts.append(ws_pts[0])
                        continue
                    sS = to_bin((ds * (1 + epsS[m, s]))[:, None] * y + base)
                    nS, _ = nums_pairs(sS, y)
                    if s == 0:
                        ws_boot = ratio(Wall, nS, pr)
                        ws_pts.append(ws_boot[0])
                    else:
                        ws_pts.append(nS.sum() / pr.sum())
                boot[ri] += WP0 - ws_boot
                for s in range(3):
                    Rp[ri, s] += WPs[s] - ws_pts[0]
                    Rl[ri, s] += WPs[0] - ws_pts[s]
        boot /= Ma
        Rp /= Ma
        Rl /= Ma
        mixed[rep] = mx / Ma
        for ri in range(len(Rs)):
            L, U = np.nanquantile(boot[ri, 1:], [0.05, 0.95])
            sp2, sl2 = np.var(Rp[ri], ddof=1), np.var(Rl[ri], ddof=1) * scale
            s_ref = math.sqrt(sp2 + sl2)
            c, h = 0.5 * (L + U), 0.5 * (U - L)
            hw = math.sqrt(h * h + (Z90 * s_ref) ** 2)
            out[rep, ri] = [boot[ri, 0], L, U, c - hw, c + hw, math.sqrt(sp2), math.sqrt(sl2), h]
    return {"key": task["key"], "w": w, "out": out, "mixed": mixed, "nclip": nclip,
            "true_mean_R": [float(np.mean([Rs[ri] + world["u"][m] for m in active])) for ri in range(len(Rs))]}


# ------------------------------------------------------------------ aggregation
def rates(pt, L, U, delta):
    eq = (L > -delta) & (U < delta)
    sup = L > delta
    stat = U < -delta
    return eq, sup, stat


def cluster_se(x_by_world):
    xw = np.array([np.mean(v) for v in x_by_world])
    return float(xw.std(ddof=1) / math.sqrt(len(xw))) if len(xw) > 1 else float("nan")


def summarize(results, Rs, deltas=(0.02, 0.03)):
    """results: list of run_group outputs of one key. Returns dict by R* -> stats."""
    res = sorted(results, key=lambda r: r["w"])
    out = {"n_worlds": len(res), "reps_total": int(sum(r["out"].shape[0] for r in res)),
           "mean_mixed_per_model": round(float(np.mean([r["mixed"].mean() for r in res])), 1),
           "n_clipped_calibrations": int(sum(r["nclip"] for r in res)), "by_R": {}}
    for ri, R in enumerate(Rs):
        A = [r["out"][:, ri, :] for r in res]
        allA = np.vstack(A)
        d = {"R_true": R,
             "mean_point": round(float(allA[:, 0].mean()), 4), "mean_true_R_in_world": round(float(np.mean([r["true_mean_R"][ri] for r in res])), 4),
             "sd_point": round(float(allA[:, 0].std(ddof=1)), 4),
             "mean_halfwidth_bootstrap": round(float(allA[:, 7].mean()), 4),
             "mean_s_refit_probe": round(float(np.sqrt((allA[:, 5] ** 2).mean())), 4),
             "mean_s_refit_lora_scaled": round(float(np.sqrt((allA[:, 6] ** 2).mean())), 4),
             "mean_halfwidth_widened": round(float(((allA[:, 4] - allA[:, 3]) / 2).mean()), 4),
             "mean_L_widened": round(float(allA[:, 3].mean()), 4), "mean_U_widened": round(float(allA[:, 4].mean()), 4)}
        for delta in deltas:
            for tag, (Lc, Uc) in (("widened", (3, 4)), ("unwidened", (1, 2))):
                row = {}
                for nm, idx in (("D1", 0), ("D2", 1), ("D3", 2)):
                    xs = [rates(a[:, 0], a[:, Lc], a[:, Uc], delta)[idx] for a in A]
                    pooled = float(np.mean(np.concatenate(xs)))
                    row[nm] = round(pooled, 3)
                    row[nm + "_se_cluster"] = round(cluster_se(xs), 3)
                    row[nm + "_se_binom"] = round(math.sqrt(max(pooled * (1 - pooled), 1e-12) / sum(len(x) for x in xs)), 3)
                row["inconclusive"] = round(1 - row["D1"] - row["D2"] - row["D3"], 3)
                d[f"delta_{delta}_{tag}"] = row
        out["by_R"][str(R)] = d
    return out


# ------------------------------------------------------------------ Shapley run (16 cells, weak suite, lexicographic ties)
PLAYERS = ["RECAL", "TRAIN", "DIFF", "LABEL"]


def pav_map(pos, tot):
    nb = len(tot)
    blocks = []
    for b in range(nb):
        if tot[b] > 0:
            blocks.append([float(pos[b]), float(tot[b]), [b]])
            while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] >= blocks[-1][0] / blocks[-1][1]:
                b2 = blocks.pop()
                blocks[-1][0] += b2[0]
                blocks[-1][1] += b2[1]
                blocks[-1][2] += b2[2]
    if not blocks:
        return np.full(nb, 0.5)
    out = np.full(nb, np.nan)
    for s, t, mem in blocks:
        out[mem] = s / t
    last = out[np.isfinite(out)][0]
    for b in range(nb):
        if np.isfinite(out[b]):
            last = out[b]
        else:
            out[b] = last
    return out


def recal_key(bins, lab, half):
    """Cross-fit isotonic map, ranked lexicographically by (map value, pre-map bin)."""
    val = np.empty(bins.shape)
    for h in (0, 1):
        fit = half == h
        tot = np.bincount(bins[fit].ravel(), minlength=11)
        pos = np.bincount(bins[fit][lab[fit]], minlength=11)
        val[~fit] = pav_map(pos, tot)[bins[~fit]]
    _, inv = np.unique(val, return_inverse=True)
    return inv.reshape(val.shape) * 16 + bins


def counts(bins, lab, nb):
    n = bins.shape[0]
    flat = np.arange(n)[:, None] * nb + bins
    pos = np.bincount(flat[lab], minlength=n * nb).reshape(n, nb).astype(float)
    neg = np.bincount(flat[~lab], minlength=n * nb).reshape(n, nb).astype(float)
    return pos, neg


def pooled_auc(Wall, pos, neg):
    P, N = Wall @ pos, Wall @ neg
    cum = np.cumsum(N, axis=1) - N
    return (P * (cum + 0.5 * N)).sum(1) / (P.sum(1) * N.sum(1))


def model_metrics_full(sim, Wall, half):
    res = {}
    sP = sim["sP"]
    edges = np.quantile(sP, np.arange(1, 128) / 128)
    pb = np.searchsorted(edges, sP)
    for l, lab in ((1, sim["y"]), (0, sim["yw"])):
        nP, pr = nums_pairs(sP, lab)
        res[("P", l, 1)] = ratio(Wall, nP, pr)
        ps, ng = counts(pb, lab, 128)
        res[("P", l, 0)] = pooled_auc(Wall, ps, ng)
        for t in (0, 1):
            bins = sim["b1"] if t else sim["b0"]
            for r in (0, 1):
                vals = recal_key(bins, lab, half) if r else bins
                nS, _ = nums_pairs(vals.astype(float), lab)
                res[("S", t, r, l, 1)] = ratio(Wall, nS, pr)
                u, inv = np.unique(vals, return_inverse=True)
                ps, ng = counts(inv.reshape(vals.shape), lab, len(u))
                res[("S", t, r, l, 0)] = pooled_auc(Wall, ps, ng)
    return res


def cell_gap_m(res, mask):
    r, t, d, l = [(mask >> i) & 1 for i in range(4)]
    return res[("P", l, d)] - res[("S", t, r, l, d)]


def decompose(v):
    out = {"G0": v[0], "R": v[15]}
    fact = [math.factorial(i) for i in range(5)]
    for i in range(4):
        acc = 0
        for mask in range(16):
            if (mask >> i) & 1:
                continue
            s = bin(mask).count("1")
            acc = acc + fact[s] * fact[3 - s] / fact[4] * (v[mask | (1 << i)] - v[mask])
        out["phi_" + PLAYERS[i]] = acc
    return out


def run_shapley(task):
    het, kid, kap, k, n, w, reps, B, models, cal = (task[x] for x in ("het", "kid", "kappa", "k", "n", "w", "reps", "B", "models", "cal"))
    R = task["R"]
    world = make_world(het, w, models)
    M = len(models)
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, 14, HET_ID[het], KAPPA_ID[kid], k, w]))
    half = np.arange(n) % 2
    d1 = [d1_for(cal["models"][m], cal["models"][m]["W_P"] - (R + world["u"][m]))[0] for m in range(M)]
    keys = ["G0", "R", "phi_RECAL", "phi_TRAIN", "phi_DIFF", "phi_LABEL"]
    pooled_pt = {k_: [] for k_ in keys}
    pooled_hw = {k_: [] for k_ in keys}
    model_pt = {k_: [] for k_ in keys}
    for _ in range(reps):
        p = draw_p_models(rng, n, models, kap)
        Wall = make_W(rng, n, B)
        mm = []
        for m in range(M):
            pm = p[:, m]
            z = std_logit(pm)
            y, het_, shock, eP, eS = draw_noise(rng, pm, k)
            w_ = np.exp(-0.5 * ((pm - 0.5) / 0.15) ** 2)
            c = world["f"][m] * (1 - pm).sum() / max(((1 - pm) * w_).sum(), 1e-12)
            q = np.minimum(1.0, c * w_)
            yw = y | ((~y) & (rng.random((n, k)) < q[:, None]))
            sP = np.maximum(world["D_P"][m] + het_ + shock, 0)[:, None] * y + world["aP"][m] * z[:, None] + eP
            base = world["aS"][m] * z[:, None] + eS
            sim = {"y": y, "yw": yw, "sP": sP,
                   "b0": to_bin(np.maximum(world["D_0"][m] + het_, 0)[:, None] * y + base),
                   "b1": to_bin(np.maximum(d1[m] + het_, 0)[:, None] * y + base)}
            mm.append(model_metrics_full(sim, Wall, half))
        v_pool = [sum(cell_gap_m(r_, mask) for r_ in mm) / M for mask in range(16)]
        dec = decompose(v_pool)
        for k_ in keys:
            arr = dec[k_]
            pooled_pt[k_].append(arr[0])
            lo, hi = np.quantile(arr[1:], [0.025, 0.975])
            pooled_hw[k_].append((hi - lo) / 2)
        per = [decompose([cell_gap_m(r_, mask)[:1] for mask in range(16)]) for r_ in mm]
        for k_ in keys:
            model_pt[k_].append([float(d_[k_][0]) for d_ in per])
    return {"het": het, "kid": kid, "k": k, "n": n, "w": w, "R": R,
            "pooled_point": {k_: float(np.mean(v)) for k_, v in pooled_pt.items()},
            "pooled_hw95": {k_: float(np.mean(v)) for k_, v in pooled_hw.items()},
            "model_point_mean_over_reps": {k_: np.mean(np.array(v), axis=0).tolist() for k_, v in model_pt.items()}}


# ------------------------------------------------------------------ heterogeneity check (population level, no sampling noise)
def het_check(task):
    """Between-model SD of population G0 (zero-shot stated, pooled, original labels) for sampled worlds."""
    het, kap, k, w, ncal, models = (task[x] for x in ("het", "kappa", "k", "w", "ncal", "models"))
    world = make_world(het, w, models)
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, 15, HET_ID[het], w]))
    g0, wp, w0 = [], [], []
    for m, mod in enumerate(models):
        p = rng.beta(mod["mu"] * kap, (1 - mod["mu"]) * kap, ncal)
        z = std_logit(p)
        y, het_, shock, eP, eS = draw_noise(rng, p, k)
        w_ = np.exp(-0.5 * ((p - 0.5) / 0.15) ** 2)
        c = world["f"][m] * (1 - p).sum() / max(((1 - p) * w_).sum(), 1e-12)
        yw = y | ((~y) & (rng.random((ncal, k)) < np.minimum(1.0, c * w_)[:, None]))
        sP = np.maximum(world["D_P"][m] + het_ + shock, 0)[:, None] * y + world["aP"][m] * z[:, None] + eP
        s0 = np.maximum(world["D_0"][m] + het_, 0)[:, None] * y + world["aS"][m] * z[:, None] + eS
        b0 = to_bin(s0)
        W1 = np.ones((1, ncal))
        sim = {"y": y, "yw": yw, "sP": sP, "b0": b0, "b1": b0}
        res = model_metrics_full(sim, W1, np.arange(ncal) % 2)
        g0.append(float(res[("P", 0, 0)][0] - res[("S", 0, 0, 0, 0)][0]))
        wp.append(float(res[("P", 1, 1)][0]))
        w0.append(float(res[("S", 0, 0, 1, 1)][0]))
    return {"G0": g0, "W_P": wp, "W_S0": w0}


# ------------------------------------------------------------------ config and mapping
def load_config(path):
    cfg = json.loads(Path(path).read_text())
    return cfg


def map_greedy_to_mu(greedy, kap):
    """Rule for greedy pass@1 -> mu at T = 1: among candidate mappings take the one with FEWER mixed problems at k = 10.
    Candidates: identity; Qwen2.5-Coder-7B anchor shift (-20.6 points) and ratio (64.5/85.1); Mistral anchor shift (+3.3 points).
    The anchors disagree in sign, so no single relation is defensible and the minimum-mixed rule applies."""
    q_sh = LIT["qwen25coder7b_random_pass_at_rank1_T1"] - LIT["qwen25coder7b_pass_at_1_baseline_T02"]
    q_ra = LIT["qwen25coder7b_random_pass_at_rank1_T1"] / LIT["qwen25coder7b_pass_at_1_baseline_T02"]
    m_sh = LIT["mistral7b_v03_random_pass_at_rank1_T1"] - LIT["mistral7b_v03_pass_at_1_baseline_T02"]
    cands = {"identity": greedy, "qwen_shift": greedy + q_sh, "qwen_ratio": greedy * q_ra, "mistral_shift": greedy + m_sh}
    cands = {a: float(np.clip(b, 0.02, 0.98)) for a, b in cands.items()}
    best = min(cands, key=lambda a: mixed_frac(cands[a], kap, 10))
    return cands[best], best, cands


def resolve_models(cfg, kap):
    models = []
    for m in cfg["models"]:
        mm = dict(m)
        if m.get("greedy_pass1_humaneval_plus") is not None and m.get("greedy_pass1_mbpp_plus") is not None:
            g = (164 * m["greedy_pass1_humaneval_plus"] + 378 * m["greedy_pass1_mbpp_plus"]) / 542
            mm["mu"], mm["mu_rule"], _ = map_greedy_to_mu(g, kap)
        else:
            mm["mu"] = m["mu_T1"]
            mm["mu_rule"] = "provisional placeholder used directly as mu at T = 1"
        models.append(mm)
    return models


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    cfg_path = Path(_arg("--config", HERE / "config_models.json"))
    out_path = Path(_arg("--out", HERE / ("power_r2_quick.json" if QUICK else "power_r2.json")))
    nproc = int(_arg("--workers", min(8, os.cpu_count() or 1)))
    cfg = load_config(cfg_path)
    kan = kappa_analysis()
    kap_cons = min(r["kappa"] for r in kan.values())       # conservative: fewer mixed
    kap_alt = max(r["kappa"] for r in kan.values())
    KAP = {"k080": kap_cons, "k183": kap_alt, "k040": 0.4}
    models = resolve_models(cfg, kap_cons)
    M = len(models)
    sub = [i for i, m in enumerate(models) if m.get("refit_substudy")]
    W_N = 4 if QUICK else 40
    REPS = 3 if QUICK else 12
    B = 100 if QUICK else 500
    NCAL = {10: 3000 if QUICK else 20000, 20: 2000 if QUICK else 10000}
    ns_sweep = [150, 300, 542] if QUICK else [100, 150, 200, 250, 300, 400, 542, 700, 900]
    reflog = lambda s: print(f"[{time.time() - t0:7.0f}s] {s}", file=sys.stderr, flush=True)

    # analytic mixed-fraction grids
    mus = [0.40, 0.50, 0.55, 0.65, 0.75, 0.80, 0.85, 0.90, 0.95]
    kaps = [0.4, 0.8, 1.1, 1.83, 3.0, 5.0]
    grid = {f"k{kk}": [{"kappa": ka, **{f"mu_{mu}": round(mixed_frac(mu, ka, kk), 3) for mu in mus}} for ka in kaps] for kk in (10, 20)}
    model_mixed = {f"kappa_{kk_}": [{"name": m["name"], "mu": m["mu"], "mixed_k10": round(mixed_frac(m["mu"], kv, 10), 4),
                                     "mixed_k20": round(mixed_frac(m["mu"], kv, 20), 4)} for m in models]
                   for kk_, kv in KAP.items()}
    mean_mixed_n542 = {f"{kk_}_k{k}": round(542 * float(np.mean([mixed_frac(m["mu"], kv, k) for m in models])), 1)
                       for kk_, kv in KAP.items() for k in (10, 20)}
    b9_mixed = {"beta_0.6_0.5_kappa_1.1_mu_0.545_k10": round(mixed_frac(0.6 / 1.1, 1.1, 10), 3)}

    with Pool(nproc) as pool:
        # ---------------- calibration stage
        combos = [("nominal", "k080"), ("conservative", "k080"), ("extreme", "k080"), ("nominal", "k183"), ("nominal", "k040")]
        if QUICK:
            combos = combos[:2]
        ctasks = [{"het": h, "kid": kid, "kappa": KAP[kid], "k": k, "w": w, "ncal": NCAL[k], "models": models}
                  for (h, kid) in combos for k in (10, 20) for w in range(W_N)]
        ctasks.sort(key=lambda t: -t["k"])
        cals = {}
        for c in pool.imap_unordered(calib_world, ctasks, chunksize=1):
            cals[(c["het"], c["kid"], c["k"], c["w"])] = c
        reflog(f"calibration done ({len(ctasks)} tasks)")

        # ---------------- heterogeneity check
        htasks = [{"het": h, "kappa": KAP["k080"], "k": 10, "w": w, "ncal": 6000 if not QUICK else 2000, "models": models}
                  for h in ("nominal", "conservative", "extreme") for w in range(30 if not QUICK else 4)]
        hres = pool.map(het_check, htasks, chunksize=1)
        hc = {}
        for h in ("nominal", "conservative", "extreme"):
            rr = [r for r, t in zip(hres, htasks) if t["het"] == h]
            g0 = np.array([r["G0"] for r in rr])
            wp = np.array([r["W_P"] for r in rr])
            hc[h] = {"mean_G0": round(float(g0.mean()), 4), "between_model_sd_G0_mean_over_worlds": round(float(g0.std(axis=1, ddof=1).mean()), 4),
                     "mean_W_P": round(float(wp.mean()), 4), "between_model_sd_W_P": round(float(wp.std(axis=1, ddof=1).mean()), 4),
                     "n_worlds": len(rr)}
        reflog("heterogeneity check done")

        # ---------------- decision groups
        def mk(key, het, mode, kid, k, n, reps, stream=12, rel_lora=None, rel_probe=None, active=None, sub_=None,
               share_het=False, R_list=None, worlds=None):
            tl = []
            for w in range(worlds or W_N):
                tl.append({"key": key, "het": het, "mode": mode, "kid": kid, "kappa": KAP[kid], "k": k, "n": n, "w": w, "reps": reps,
                           "B": B, "models": models, "cal": cals[(het, kid, k, w)], "stream": stream,
                           "rel_lora": REFIT["nominal"]["rel_lora"] if rel_lora is None else rel_lora,
                           "rel_probe": REFIT["nominal"]["rel_probe"] if rel_probe is None else rel_probe,
                           "sub": sub if sub_ is None else sub_, "active": active or list(range(M)),
                           "share_het": share_het, "R_list": R_list or R_LIST})
            return tl

        tasks = []
        hets_main = ["nominal", "conservative"] if not QUICK else ["nominal"]
        for h in hets_main:
            for k in (10, 20):
                for n in ns_sweep:
                    tasks += mk(("main", h, "FE", "k080", k, n), h, "FE", "k080", k, n, REPS)
        if not QUICK:
            for k in (10, 20):
                tasks += mk(("main", "extreme", "FE", "k080", k, 542), "extreme", "FE", "k080", k, 542, REPS)
                for h in ("nominal", "conservative"):
                    tasks += mk(("RE", h, "RE", "k080", k, 542), h, "RE", "k080", k, 542, REPS, stream=12)
                tasks += mk(("kappa183", "nominal", "FE", "k183", k, 542), "nominal", "FE", "k183", k, 542, REPS)
                tasks += mk(("kappa040", "nominal", "FE", "k040", k, 542), "nominal", "FE", "k040", k, 542, REPS)
                # stress tests (nominal heterogeneity, kappa 0.80, n = 542)
                tasks += mk(("stress_no_refit", "nominal", "FE", "k080", k, 542), "nominal", "FE", "k080", k, 542, REPS, rel_lora=0.0, rel_probe=0.0)
                tasks += mk(("stress_refit_x2", "nominal", "FE", "k080", k, 542), "nominal", "FE", "k080", k, 542, REPS, rel_lora=0.20, rel_probe=0.10)
                tasks += mk(("stress_refit_x0.5", "nominal", "FE", "k080", k, 542), "nominal", "FE", "k080", k, 542, REPS, rel_lora=0.05, rel_probe=0.025)
                tasks += mk(("stress_refit_x0.25", "nominal", "FE", "k080", k, 542), "nominal", "FE", "k080", k, 542, REPS, rel_lora=0.025, rel_probe=0.0125)
                tasks += mk(("stress_lora_only_x1", "nominal", "FE", "k080", k, 542), "nominal", "FE", "k080", k, 542, REPS, rel_lora=0.10, rel_probe=0.0)
                tasks += mk(("stress_M1", "nominal", "FE", "k080", k, 542), "nominal", "FE", "k080", k, 542, REPS, active=[3], sub_=[3])
                tasks += mk(("stress_shared_problem_shock", "nominal", "FE", "k080", k, 542), "nominal", "FE", "k080", k, 542, REPS, share_het=True)
        tasks.sort(key=lambda t: -(t["n"] * t["k"] ** 2 * t["reps"]))
        groups = {}
        for r in pool.imap_unordered(run_group, tasks, chunksize=1):
            groups.setdefault(r["key"], []).append(r)
        reflog(f"decision groups done ({len(tasks)} tasks)")
        summ = {key: summarize(v, R_LIST) for key, v in groups.items()}

        # ---------------- threshold search from sweep
        thr = {}
        for h in hets_main:
            for k in (10, 20):
                curve = []
                for n in ns_sweep:
                    s = summ[("main", h, "FE", "k080", k, n)]
                    row = {"n": n, "mean_mixed_per_model": s["mean_mixed_per_model"]}
                    for delta in (0.02, 0.03):
                        b = s["by_R"]
                        p1 = b["0.0"][f"delta_{delta}_widened"]["D1"]
                        p2 = b[str(2 * delta)][f"delta_{delta}_widened"]["D2"] if str(2 * delta) in b else None
                        p3 = b[str(-2 * delta)][f"delta_{delta}_widened"]["D3"] if str(-2 * delta) in b else None
                        row[f"delta_{delta}"] = {"D1": p1, "D2": p2, "D3": p3, "min": min(p1, p2, p3)}
                    curve.append(row)
                thr[f"{h}_k{k}"] = curve
        # unwidened curves (shows what the refit rule costs)
        thr_unw = {}
        for h in hets_main:
            for k in (10, 20):
                curve = []
                for n in ns_sweep:
                    s = summ[("main", h, "FE", "k080", k, n)]
                    row = {"n": n, "mean_mixed_per_model": s["mean_mixed_per_model"]}
                    for delta in (0.02, 0.03):
                        b = s["by_R"]
                        vals = [b["0.0"][f"delta_{delta}_unwidened"]["D1"], b[str(2 * delta)][f"delta_{delta}_unwidened"]["D2"],
                                b[str(-2 * delta)][f"delta_{delta}_unwidened"]["D3"]]
                        row[f"delta_{delta}"] = {"D1": vals[0], "D2": vals[1], "D3": vals[2], "min": min(vals)}
                    curve.append(row)
                thr_unw[f"{h}_k{k}"] = curve

        # ---------------- Shapley
        sh_out = []
        if not QUICK:
            stasks = []
            for h in ("nominal", "conservative"):
                for w in range(8):
                    stasks.append({"het": h, "kid": "k080", "kappa": KAP["k080"], "k": 10, "n": 542, "w": w, "reps": 4, "B": 300,
                                   "models": models, "cal": cals[(h, "k080", 10, w)], "R": 0.0})
        else:
            stasks = [{"het": "nominal", "kid": "k080", "kappa": KAP["k080"], "k": 10, "n": 542, "w": 0, "reps": 1, "B": 60,
                       "models": models, "cal": cals[("nominal", "k080", 10, 0)], "R": 0.0}]
        sh_res = pool.map(run_shapley, stasks, chunksize=1)
        for h in sorted({r["het"] for r in sh_res}):
            rr = [r for r in sh_res if r["het"] == h]
            keys = list(rr[0]["pooled_point"].keys())
            sh_out.append({"het": h, "k": 10, "n": 542, "M": M, "R_true": 0.0, "n_worlds": len(rr), "reps_per_world": stasks[0]["reps"], "B": stasks[0]["B"],
                           "mean_point": {k_: round(float(np.mean([r["pooled_point"][k_] for r in rr])), 4) for k_ in keys},
                           "mean_ci95_halfwidth": {k_: round(float(np.mean([r["pooled_hw95"][k_] for r in rr])), 4) for k_ in keys},
                           "between_model_sd_of_point": {k_: round(float(np.mean([np.std(r["model_point_mean_over_reps"][k_], ddof=1) for r in rr])), 4) for k_ in keys}})
        reflog("shapley done")

        # ---------------- verification at interpolated thresholds
        verif = {}
        interp = {}
        for name, curve in thr.items():
            for delta in (0.02, 0.03):
                xs = [r["mean_mixed_per_model"] for r in curve]
                ys = [r[f"delta_{delta}"]["min"] for r in curve]
                nn = [r["n"] for r in curve]
                found = None
                for i in range(len(xs)):
                    if ys[i] >= 0.90:
                        if i == 0:
                            found = {"mixed": xs[0], "n": nn[0]}
                        else:
                            f = (0.90 - ys[i - 1]) / (ys[i] - ys[i - 1]) if ys[i] != ys[i - 1] else 1.0
                            found = {"mixed": xs[i - 1] + f * (xs[i] - xs[i - 1]), "n": nn[i - 1] + f * (nn[i] - nn[i - 1])}
                        break
                interp[f"{name}_delta{delta}"] = found if found else {"status": "0.90 not reached on the sweep", "max_min_power": max(ys), "at_n": nn[int(np.argmax(ys))]}
        if not QUICK:
            vtasks = []
            for key, f in interp.items():
                if "n" in f and f["n"] < ns_sweep[-1]:
                    h, kpart, dpart = key.split("_")[0], key.split("_")[1], key.split("_")[2]
                    k = int(kpart[1:])
                    n_ver = int(math.ceil(f["n"]))
                    kk = ("verify", h, k, n_ver)
                    if kk not in verif:
                        verif[kk] = None
                        vtasks += mk(kk, h, "FE", "k080", k, n_ver, 20, stream=13)
            vres = {}
            for r in pool.imap_unordered(run_group, vtasks, chunksize=1):
                vres.setdefault(r["key"], []).append(r)
            verif_out = {f"{kk[1]}_k{kk[2]}_n{kk[3]}": summarize(v, R_LIST) for kk, v in vres.items()}
        else:
            verif_out = {}

        # ---------------- refit-noise sweep is the stress_refit_* rows
    runtime = time.time() - t0

    def key_s(t):
        return "|".join(str(x) for x in t)

    doc = {
        "status": "design-stage planning arithmetic under stated assumptions; not a result; provisional per-model inputs",
        "quick": QUICK, "runtime_seconds": round(runtime, 1), "numpy_version": np.__version__,
        "python_version": sys.version.split()[0], "base_seed": BASE_SEED,
        "settings": {"worlds": W_N, "replicates_per_world": REPS, "replicates_total_per_cell": W_N * REPS, "bootstrap_B": B,
                     "n_calibration_problems": NCAL, "sweep_n": ns_sweep, "M": M, "refit_substudy_indices": sub, "R_list": R_LIST,
                     "mc_error": "SE reported two ways: binomial over all replicates, and cluster SE over worlds (worlds are exchangeable draws of the six-model heterogeneity); the larger is the honest one"},
        "config_used": {"path_name": cfg_path.name, "status": cfg.get("status"), "models": models},
        "literature_values_used": LIT, "derived_from_literature": DER,
        "heterogeneity_settings": HETS, "refit_assumption": REFIT,
        "other_assumptions": {
            "rho_difficulty_copula": RHO_D, "problem_het_sd": HET_SD, "probe_shock_sd_auroc_units": 0.05, "corr_eP_eS": RHO_E,
            "difficulty_loadings_mean": {"a_P": A_P0, "a_S": A_S0}, "probe_within_auroc_mean": 0.72, "zero_shot_within_auroc_mean": 0.60,
            "weak_suite_false_pass_mean": F_FP0, "stated_bins": 11,
            "fixed_effects": "R_m = R* + u_m, u_m ~ N(0, tau_R^2) centered to mean zero per world; trained separation d1_m calibrated per model so the population within-AUROC residual equals R_m",
            "random_effects": "same, u_m not centered; decision still judged against R* (sensitivity only)",
            "refit_rule": "s_refit^2 = Var_ddof1 over 3 seeds of Rbar with probe refit in all models (S at seed 0) + (M / n_sub) * Var_ddof1 over 3 seeds of Rbar with trained readout refit in the n_sub sub-study models only (probe and other models at seed 0); half-width sqrt(h^2 + (1.645 s_refit)^2) about the percentile interval center",
            "seed0_perturbation": "the observed Rbar uses seed-0 perturbed separations; the estimand R* is defined at the unperturbed calibrated separation",
            "lexicographic_ties": "W of the recalibrated readout equals W of the pre-map bins; pooled AUROC ranks by (isotonic value, bin)",
            "decisions_use": "R on EvalPlus labels (true y) only; weak-suite labels enter only G0 and the Shapley cells",
        },
        "kappa_analysis": kan, "kappa_used": KAP,
        "greedy_to_T1_rule": {
            "anchors": {"Qwen2.5-Coder-7B": {"greedy_T02": LIT["qwen25coder7b_pass_at_1_baseline_T02"], "T1_random": LIT["qwen25coder7b_random_pass_at_rank1_T1"]},
                        "Mistral-7B-v0.3": {"greedy_T02": LIT["mistral7b_v03_pass_at_1_baseline_T02"], "T1_random": LIT["mistral7b_v03_random_pass_at_rank1_T1"]}},
            "shift_points": {"Qwen": round(100 * (LIT["qwen25coder7b_random_pass_at_rank1_T1"] - LIT["qwen25coder7b_pass_at_1_baseline_T02"]), 1),
                             "Mistral": round(100 * (LIT["mistral7b_v03_random_pass_at_rank1_T1"] - LIT["mistral7b_v03_pass_at_1_baseline_T02"]), 1)},
            "defensible": False,
            "reason": "the two anchors move in opposite directions (-20.6 and +3.3 points); the baseline in the paper is temperature 0.2, not greedy; two models cannot define a relation",
            "rule_applied": "mu at T = 1 is the candidate (identity, Qwen shift, Qwen ratio, Mistral shift) with the fewest mixed problems at kappa conservative; for greedy above 0.5 this is the identity",
        },
        "mixed_fraction_grid": grid, "b9_planning_mixed_fraction": b9_mixed,
        "mixed_per_model_analytic": model_mixed, "mean_mixed_count_n542_analytic": mean_mixed_n542,
        "heterogeneity_check": hc, "literature_G0_like_sd": DER["sd_probe_minus_verbalized_pooled_G0like"],
        "groups": {key_s(k_): v for k_, v in summ.items()},
        "threshold_curves_widened": thr, "threshold_curves_unwidened": thr_unw, "threshold_interpolated": interp,
        "threshold_verification": verif_out,
        "shapley_M6": sh_out,
    }
    out_path.write_text(json.dumps(doc, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + "\n")
    print(f"wrote {out_path} in {runtime:.0f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
