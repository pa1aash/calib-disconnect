# Orchestrator notes — best-AAAI-paper scan (code-llm-best-aaai-paper-6ded37)

## Scout (benchmark-artifact) — STRONGEST LEAD OF THE SESSION.
**Testlet/requirement-level IRT on per-unit-test pass/fail (BigCodeBench).**
- Novelty OPEN: psychometrics-for-LLMs survey (2505.08245) explicitly flags nested/testlet response models
  as unexplored; NO paper does per-unit-test IRT for code.
- AAAI-fit PROVEN: PSN-IRT "Lost in Benchmarks" = AAAI-2026 ORAL (whole-item IRT benchmark audit). Template.
- Artifact: fit testlet-IRT (2PL nested/bifactor) on per-req pass/fail -> per-requirement DIFFICULTY + DISCRIMINATION.
  (1) saturation-resistant diagnostic subset (selected by statistical discrimination, not solve-rate heuristic);
  (2) IRT requirement-weighted ability score w/ SEs+invariance (AvgPassRatio/pass@k lack these);
  (3) headline: which requirement TYPES (edge/exception vs core-logic vs library-composition) show high vs
      collapsed discrimination; transfer Qwen<->DeepSeek.
- RESCUES the correlated-failure fact (mean 2.27 co-fail): testlet models EXIST to handle within-testlet
  correlation -> the nuisance becomes the motivation. Beautiful fit.
- Feasibility: need enough "respondents" (solutions/problem) for stable IRT -> generate more solutions across
  models/temps via fast vLLM. Within infra.
- Differentiate vs: TaskEval (whole-task IRT code), PSN-IRT (AAAI'26, whole-item general).
- Answers the "just descriptive" critique that killed plain partial-credit measurement.

## Awaiting: Scout (conformal/UQ-theory), Scout (meta reverse-engineer + capability-science).
