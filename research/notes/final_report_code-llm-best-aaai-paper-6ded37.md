# The Best AAAI-27 Paper Achievable With These Assets: A Psychometric Model of Code-LLM Competence

**Committed recommendation: a psychometric / latent-skill model of code-LLM competence at REQUIREMENT
granularity** — fit a factor-analytic / testlet-IRT model to the per-unit-test pass/fail matrix on
BigCodeBench, decompose competence into a few latent skills, and test whether that skill structure is
shared or idiosyncratic across model families. Two independent scouts converged on this; it is the
strongest, best-fit, un-scooped direction found across all three research passes this session.

## Why this is the answer (after three misses)
The prior misses were all in crowded lanes (calibration/probing, RL reward, repair). This is different:
- **Genuinely novel + survey-confirmed open.** The 400-ref "LLM Psychometrics" survey (2505.08245)
  explicitly flags nested/testlet response models as unexplored. No paper does IRT/factor decomposition at
  the **sub-item (per-unit-test/requirement)** level for code. Nearest work is at the WRONG granularity:
  *Beyond Scores* (2604.12191, whole-question mIRT + Q-matrix), *From Benchmarks to Skills* (2507.20208,
  model×benchmark factor analysis), *TaskEval* (whole-task IRT for code), *Failure Independence* (2607.02808,
  N-version reliability, correlated failures but across implementations not within-solution requirements).
- **AAAI-fit is PROVEN, not hoped.** *Lost in Benchmarks / PSN-IRT* is an **AAAI-2026 ORAL** (whole-item IRT
  benchmark audit); *Incoherence* is AAAI-2026 main track. The accepted SHAPE in this territory is exactly:
  **(new measurement mechanism, theory-backed) + (multi-model empirical validation) + (crisp numeric headline)
  + (downstream practical tool).** Our direction fits all four.
- **It converts our liabilities into the paper's evidence.** The correlated-failure fact that sank Direction B
  (solutions fail 2.27/5 requirements together; only 11% fail exactly one) is *precisely* the low-rank/testlet
  signal a factor/IRT model is built to capture — the nuisance becomes the load-bearing result. The hidden-state
  probe (0.72) becomes a *validation instrument*, not a scooped headline.
- **Feasible on data we already have.** Mostly CPU analysis on the existing 498×~5×N pass/fail pool; escalate
  respondent count via fast vLLM sampling only if IRT stability needs it. Follow the solution-priority ladder:
  **FA / low-rank SVD first** (cheap, needs fewer respondents) → full multidimensional IRT only if warranted.

## The paper (headline results to chase)
1. **A few latent skills (target k≈3-6) explain most requirement-failure covariance** in code LLMs — a low-rank
   structure one granularity level below anything published.
2. **Cross-model-family test (the single most reviewer-legible number):** fit factors on Qwen2.5-Coder-7B vs
   DeepSeek-Coder-6.7B; report factor congruence (Tucker's φ). Shared skill geometry (φ≈0.8) OR the more
   interesting divergence ("families share only 2 of 5 factors, splitting on [skill]").
3. **Predictive validity:** latent factors predict held-out requirement failure (AUC, cf. *Beyond Scores* 0.77-0.89)
   at finer grain and cheaper — a compact diagnostic (fewer requirements to place a new model/problem in skill-space).
4. **Ties to our probe:** does the 0.72 hidden-state probe implicitly track one specific latent skill? (Interpretability hook.)
5. **[Practical-tool section] Per-requirement conformal selective acceptance** — return the subset of requirements
   claimable-satisfied at controlled risk (conformal risk control on probe scores + execution labels). This lane is
   otherwise partial-to-scooped as a *flagship* (RisCoSet / Task Abstention, May'26) but is a clean, novel-at-
   per-requirement-granularity *tool section* that supplies the AAAI-shape "downstream payoff."

## Honest caveats
- Differentiate SHARPLY vs *Beyond Scores* + *From Benchmarks to Skills* (our delta = sub-item/per-requirement +
  within-problem + cross-model-family + code + probe grounding). Reviewer will cite these.
- IRT respondent/item ratio is the real technical risk → start with FA, add vLLM-sampled solutions for respondents.
- Still weeks-scale (fit + cross-model + validation + write) → later venue, but the strongest bet by far.

## Immediate de-risk (cheap, do first)
Run FA / low-rank SVD on the EXISTING per-requirement pass/fail matrix (CPU, hours): does a low-rank structure
exist (scree/variance-explained), and is it non-trivial across the two models? If yes → commit and build; if the
matrix is full-rank noise → reconsider. This tests the paper's foundational claim before any weeks of investment.
