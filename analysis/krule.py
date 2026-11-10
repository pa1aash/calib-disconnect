"""The k rule (design section 13, operator sign-off item 2; the only data-dependent adjustment).

m_bar = mean over P1 to P6 of the number of problems mixed under the EvalPlus suite on the
label-validity population after reference exclusions. k = 20 if m_bar < T10 (185), otherwise k = 10.
If k = 20 is triggered, the mean mixed count at k = 20 is compared with T20 (125) after generation;
the comparison is reported and changes nothing. Per-model counts, pass-fail pair counts, and
per-problem pass-count histograms are passed through for the report and the audit rerun.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from pipeline.contracts.constants import K_DEFAULT, K_EXPANDED, PRIMARY_MODELS, T10, T20
from pipeline.contracts.schemas import KRuleResult


def k_from_mean(m_bar: float) -> int:
    return K_EXPANDED if m_bar < T10 else K_DEFAULT


def k_rule(per_model_mixed: Mapping[str, float], m_bar_k20: float | None = None) -> KRuleResult:
    """Apply the k rule over exactly the six primary models."""
    if set(per_model_mixed) != set(PRIMARY_MODELS):
        raise ValueError(f"the k rule uses exactly {PRIMARY_MODELS}; got {sorted(per_model_mixed)}")
    vals = [per_model_mixed[m] for m in PRIMARY_MODELS]
    if any((not np.isfinite(v)) or v < 0 for v in vals):
        raise ValueError("mixed counts must be finite and non-negative")
    m_bar = float(np.mean(vals))
    k = k_from_mean(m_bar)
    below = None
    if m_bar_k20 is not None:
        if k != K_EXPANDED:
            raise ValueError("the T20 comparison applies only after k = 20 was triggered")
        below = bool(m_bar_k20 < T20)
    return KRuleResult(per_model_mixed={m: per_model_mixed[m] for m in PRIMARY_MODELS}, m_bar=m_bar,
                       t10=T10, k=k, t20=T20, m_bar_k20=None if m_bar_k20 is None else float(m_bar_k20),
                       below_t20=below)


def k_rule_report(per_model_mixed: Mapping[str, float], pair_counts: Mapping[str, int] | None = None,
                  histograms: Mapping[str, Mapping[int, int]] | None = None,
                  m_bar_k20: float | None = None) -> dict:
    """KRuleResult plus the pass-through per-model pair counts and pass-count histograms."""
    res = k_rule(per_model_mixed, m_bar_k20)
    out = res.to_dict()
    out["pair_counts"] = dict(pair_counts or {})
    out["pass_count_histograms"] = {m: {str(k): int(v) for k, v in h.items()} for m, h in (histograms or {}).items()}
    return out
