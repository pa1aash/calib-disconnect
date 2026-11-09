---
vault_tag: aaai-bar-eval-dprc
created: 2026-07-20T00:00:00Z
source: user-prompt
---

Evaluate where the DPRC paper-in-progress actually stands against RECENTLY ACCEPTED AAAI main-track papers (2024, 2025, 2026) in the relevant subareas (ML: Bayesian Learning & Uncertainty Quantification / calibration / selective prediction; and code-LLM / NLP code generation), and determine concretely what MORE is needed to clear the AAAI-27 main-track acceptance bar. Be adversarial and specific — area-chair/reviewer-2 mindset — not a generic survey.

CURRENT STATE OF OUR WORK (real results from the running experiment, use these to assess OUR specific standing):
- Base paper: "The Calibration Disconnect" — code LLMs have a near-perfect INTERNAL sampling confidence (AUROC 0.987) but no EXPRESSED interface communicates it.
- Proposed extension "DPRC": train a code LLM (LoRA, single-GPU) to SELF-EXPRESS calibrated, discriminative confidence at PER-REQUIREMENT / per-unittest-method granularity — localizing which requirement its own solution will fail. Elicited by priming "REQ <requirement>: <0-9 digit>" and reading the model's digit distribution (tokenized-Brier readout).
- KEY EMPIRICAL FINDINGS so far (on the box, Qwen2.5-Coder-7B):
  (1) On COMPETITIVE code (TACO): per-requirement confidence COLLAPSES to scalar — oracle per-test AUROC 0.86 == scalar oracle 0.88, because competitive correctness is all-or-nothing (a solution passes all tests or fails all). ~0% partial-pass.
  (2) On REALISTIC functional code (BigCodeBench, unittest methods as requirements): per-requirement is REAL — oracle per-method AUROC 0.931 > scalar oracle 0.875, and 32% of solutions PARTIALLY pass (some requirements yes, some no). This competitive-vs-functional contrast is itself a candidate finding (explains WHEN localized confidence helps for code, and why per-claim NL methods like CURE/Atomic Calibration don't transfer to competitive code).
  (3) The 0.931 is the ORACLE ceiling (using actual n-sample per-method pass rates). The open question the scaled run answers: how close can the TRAINED model's SELF-EXPRESSED per-method AUROC get to that ceiling. A micro-pilot (50 problems) was too small (model undertrained, output near-constant low confidence). Full BigCodeBench (~1140 problems) labeling is running now; proper training + eval next.
- Compute: single A100-80GB, LoRA, both Qwen2.5-Coder-7B + DeepSeek-Coder-6.7B planned. Closest prior work: DCPO (ICML 2026, scalar decoded confidence on code, AUROC 0.79-0.91), CURE/Atomic Calibration (per-claim NL, not code), FLARE/Gros&Devanbu (external probes / spatial line-level, not self-expressed functional), Rewarding Doubt/ConfTuner (scalar verbalized, QA only). Live scoop risk: UT-Dallas "Beyond Execution" under review.

DELIVERABLES the research must produce:
1. What do ACCEPTED AAAI main-track papers in this space actually look like — the real bar (scope, # experiments, baselines, novelty type, models/scale, what reviewers reward and reject). Pull concrete recently-accepted examples.
2. Honest verdict: given our current + projected results, where does DPRC stand vs that bar — accept / borderline / reject, and the single harshest fair objection.
3. Concrete gap list: exactly what additional experiments, baselines, ablations, framing, and headline numbers are needed to move from where we are to a clear accept. Prioritized.
4. The strongest possible framing/headline given the competitive-vs-functional finding (is the negative-on-competitive + positive-on-functional contrast a strength to lead with, or a distraction?).
5. What would make this "cook harder" — the highest-leverage additions (e.g., a mechanism/theory result, a downstream utility result, a scale/generalization result) that most raise acceptance odds.

Priority: an honest, adversarial, concrete assessment of standing + a prioritized to-do to clear the AAAI-27 main-track bar. Not novelty-discovery (that's done) — this is BAR-CALIBRATION and GAP-ANALYSIS against real accepted papers.
