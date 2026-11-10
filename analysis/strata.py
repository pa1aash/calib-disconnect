"""Strata and stratum contrasts (design sections 1.3, 1.7 H4, 4, 10). Every result here is labeled
unadjusted (section 9).

Contamination stratum (section 4): per model, LiveCodeBench problems are split by release_date
strictly after constants.COUNT_DATES[model]. Partitions are "post" and, before or on the date,
"pre" where the count date is stated (Olmo 3, Gemma 4, gpt-oss) or "pre_or_unknown" where it is an
upper bound (Qwen3, Qwen3-Coder, Qwen2.5-Coder). A problem with no release date is in
"pre_or_unknown" for every model. Each partition's budget uses the same draws restricted to its
problems. A model with no post-cutoff problem has no stratum (Qwen3). Pooled results use Olmo 3
and Gemma 4 only (P3, P4, P5, P6).

Stratum contrasts are per-term paired differences on the same draws: instruct minus base
(P1..P6 against B1..B6; C1, C2 against C3, C4), reasoning on minus off (S1 against P1), coder minus
primary of similar scale (descriptive: C1 against the mean of P1 and P3, the 7 to 8B primaries; C2
against the mean of P4 and P6, the 31 to 32B primaries; not same-weights contrasts), the
post-training trajectory B3, T1, T2, P3 (descriptive, consecutive differences), family pooled
budgets (two models each), and scale contrasts within family (P2 - P1, P4 - P3, P6 - P5, each with
its confound stated: Olmo 3 7B and Olmo 3.1 32B differ in release version, Gemma 4 12B and 31B in
architecture).
"""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np

from pipeline.contracts.constants import COUNT_DATES, MODELS, SHAPLEY_MARGINAL_LEVEL

from .bootstrap import interval_dict, percentile_interval

STATED_COUNT_DATE_PREFIXES = ("allenai/", "google/", "openai/")
CONTAMINATION_POOLED = ("P3", "P4", "P5", "P6")
INSTRUCT_BASE = (("P1", "B1"), ("P2", "B2"), ("P3", "B3"), ("P4", "B4"), ("P5", "B5"), ("P6", "B6"),
                 ("C1", "C3"), ("C2", "C4"))
REASONING = ("S1", "P1")
CODER_VS_PRIMARY = {"C1": ("P1", "P3"), "C2": ("P4", "P6")}
TRAJECTORY = ("B3", "T1", "T2", "P3")
FAMILIES = {"qwen3": ("P1", "P2"), "olmo3": ("P3", "P4"), "gemma4": ("P5", "P6")}
SCALE = {"qwen3": ("P2", "P1", "Qwen3-14B against Qwen3-8B"),
         "olmo3": ("P4", "P3", "Olmo-3.1-32B against Olmo-3-7B; the two differ in release version"),
         "gemma4": ("P6", "P5", "gemma-4-31B against gemma-4-12B; the two differ in architecture")}
UNADJUSTED = "unadjusted (section 9)"


def count_date_is_stated(model: str) -> bool:
    return MODELS[model][0].startswith(STATED_COUNT_DATE_PREFIXES)


def contamination_partition(model: str, problems: Sequence[str], release_date: Mapping[str, str | None]) -> dict:
    """Masks over `problems`: "post" (release day strictly after the count date) and the rest, labeled
    "pre" (stated count date, dated problems) or "pre_or_unknown" (upper-bound count date, or no date)."""
    cd = COUNT_DATES[model]
    known = np.array([bool(release_date.get(q)) for q in problems], dtype=bool)
    post = np.array([bool(release_date.get(q)) and str(release_date[q])[:10] > cd for q in problems], dtype=bool)
    stated = count_date_is_stated(model)
    if stated:
        masks = {"post": post, "pre": ~post & known}
        if (~known).any():
            masks["pre_or_unknown"] = ~post & ~known
    else:
        masks = {"post": post, "pre_or_unknown": ~post}
    return {"count_date": cd, "count_date_stated": stated, "masks": masks, "has_stratum": bool(post.any())}


def _terms(store: dict, which: str = "disc"):
    return store[f"{which}_terms_pt"], store.get(f"{which}_terms_rep")


def mean_terms(stores: Sequence[dict], which: str = "disc"):
    pts = [_terms(s, which)[0] for s in stores]
    reps = [_terms(s, which)[1] for s in stores]
    keys = list(pts[0])
    pt = {k: float(np.mean([p[k] for p in pts])) for k in keys}
    rp = None if any(r is None for r in reps) else {k: np.mean(np.vstack([r[k] for r in reps]), axis=0) for k in keys}
    return pt, rp


def term_contrast(a: Sequence[dict], b: Sequence[dict], label: str, which: str = "disc",
                  level: float = SHAPLEY_MARGINAL_LEVEL) -> dict:
    """Per-term mean(a) - mean(b) with paired percentile intervals."""
    pa, ra = mean_terms(a, which)
    pb, rb = mean_terms(b, which)
    out = {"label": label, "adjustment": UNADJUSTED, "terms": {}}
    for k in pa:
        d = pa[k] - pb[k]
        entry = {"a": pa[k], "b": pb[k], "diff": d}
        if ra is not None and rb is not None:
            entry["interval"] = interval_dict(percentile_interval(d, ra[k] - rb[k], level))
        out["terms"][k] = entry
    return out


def term_intervals(stores: Sequence[dict], label: str, which: str = "disc",
                   level: float = SHAPLEY_MARGINAL_LEVEL) -> dict:
    pt, rp = mean_terms(stores, which)
    return {"label": label, "adjustment": UNADJUSTED,
            "terms": {k: {"point": v, "interval": None if rp is None else
                          interval_dict(percentile_interval(v, rp[k], level))} for k, v in pt.items()}}


def stratum_contrasts(stores: Mapping[str, dict]) -> dict:
    """All model-level stratum contrasts for which both sides are present."""
    out: dict = {"adjustment": UNADJUSTED}
    ib = {f"{a}-{b}": term_contrast([stores[a]], [stores[b]], f"instruct {a} minus base {b}")
          for a, b in INSTRUCT_BASE if a in stores and b in stores}
    if ib:
        out["instruct_minus_base"] = ib
    a, b = REASONING
    if a in stores and b in stores:
        out["reasoning_on_minus_off"] = term_contrast([stores[a]], [stores[b]], "S1 (thinking on) minus P1 (off)")
    cv = {}
    for c, prims in CODER_VS_PRIMARY.items():
        if c in stores and all(p in stores for p in prims):
            cv[c] = term_contrast([stores[c]], [stores[p] for p in prims],
                                  f"{c} minus mean of {', '.join(prims)}; descriptive, not a same-weights contrast")
    if cv:
        out["coder_minus_primary"] = cv
    present = [m for m in TRAJECTORY if m in stores]
    if len(present) >= 2:
        out["trajectory"] = {
            "label": "descriptive post-training trajectory",
            "stages": {m: term_intervals([stores[m]], m) for m in present},
            "steps": {f"{b}-{a}": term_contrast([stores[b]], [stores[a]], f"{b} minus {a}")
                      for a, b in zip(present[:-1], present[1:])},
        }
    fam = {f: term_intervals([stores[x] for x in ms], f"{f} mean of {ms[0]} and {ms[1]}")
           for f, ms in FAMILIES.items() if all(x in stores for x in ms)}
    if fam:
        out["family"] = fam
    sc = {f: term_contrast([stores[hi]], [stores[lo]], note) for f, (hi, lo, note) in SCALE.items()
          if hi in stores and lo in stores}
    if sc:
        out["scale"] = sc
    return out
