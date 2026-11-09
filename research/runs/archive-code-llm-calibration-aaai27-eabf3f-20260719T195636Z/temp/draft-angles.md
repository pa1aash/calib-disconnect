# Draft angles — code-llm-calibration-aaai27-eabf3f

The deliverable is a committed paper PROPOSAL. Three risk postures so the synthesizer can
integrate a bold headline with honest risk-management and a concrete plan.

## Draft A — Strongest-thesis (the bold committed recommendation)
Argue forcefully that THE paper is: "Structured, execution-grounded confidence for code — train a
code LLM to SELF-EXPRESS calibrated, discriminative confidence at per-test-case/per-requirement
granularity, localizing which part of a solution will fail, via DCPO-style decoupled LoRA training
against continuous per-test execution-pass-rate targets." Full proposal: headline, exact
experiment producing the headline number, why it lands (DCPO/Rewarding-Doubt/CURE evidence),
supporting results, failure mode + fallback, novelty defense vs the 4-axis wedge, AAAI-27 topic.
Confident and specific. This is the primary.

## Draft B — Steelman-contrarian / risk-first (could this still be a dead paper?)
Take seriously that the space is crowded and timeline-risky: DCPO already trains decoded confidence
on code with AUROC 0.91; Gros&Devanbu already publish "Localized Calibrated Uncertainty in Code
LMs"; the UT Dallas group has two on-topic under-review papers; the AAAI-27 paper deadline is ~10
days out; per-test structured confidence is a HARDER training target that might land at mediocre
AUROC. Defend the most DEFENSIVE version of the paper that still clears main-track: e.g. lead with
the guaranteed selective-generation utility result + scalar replication, treat structured
confidence as the novel-but-risky upside, and/or recommend the next venue if AAAI-27 is infeasible.
Argue what scoping maximizes P2 (confidence) without sacrificing acceptance.

## Draft C — Synthesis / practitioner (the actual runnable plan)
Boundary conditions: when does the bold structured headline win vs the safe fallback? Produce the
concrete, runnable experiment protocol with PRE-REGISTERED decision points and de-scoping ladder:
Day-1 pilot, model(s), benchmarks (TACO/CodeContests for dense per-test labels; LiveCodeBench for
contamination-free eval; HumanEval legacy), label pipeline (reuse existing n-sample per-test
pass/fail), training recipe (decoupled masked-gradient LoRA + bounded Brier), metrics (per-test
AUROC primary, debiased ECE secondary, risk-coverage utility), ablations (joint-vs-decoupled,
continuous-vs-tiered targets), GPU-hour budget, reproducibility-checklist items, AAAI-27 vs
next-venue contingency. The "how to actually not waste time/money" draft.
