# Feeling Out the Pivot: Is "Per-Requirement Code Probe + Verbalization Gap" Novel Enough for AAAI-27?

**Committed verdict: VIABLE BUT NARROW — and the "faithfulness gap" cannot be the headline.** The pivot
survives only as a *utility-anchored, per-requirement* paper. The exciting part (the internal-vs-verbalized
gap) is multiply scooped; the defensible novelty is a narrow quartet, and the closest prior work sits one
notch away. Grounded in our real numbers (oracle 0.805>scalar 0.743, probe 0.745/0.706, self-report 0.603/0.576,
34% partial-pass) and four adversarial literature sweeps.

## 1. What is already occupied (the scoop map)
- **"Internal signal > verbalized self-report" is a mature, named result in general NLP** — Burns et al. CCS
  (ICLR'23), Azaria & Mitchell SAPLMA (EMNLP'23), Kadavath P(True) ('22), Orgad/Gekhman "LLMs Know More Than
  They Show" (ICLR'25), Farquhar/Kuhn semantic entropy (Nature'24). Whole-answer granularity, general QA.
- **It is ALREADY demonstrated on code** — **Ribeiro, Spiess, Devanbu, Nadi, "On LLMs' Internal Representation
  of Code Correctness" (ICSE'26, accepted).** A contrastive hidden-state direction beats BOTH log-likelihood
  AND the model's verbalized confidence on 4 code LLMs. **This is the single closest prior work.** But:
  whole-solution granularity only; zero-shot *prompted* verbalization (not trained).
- **The "faithfulness gap" is an active 2026 research area** — Miao & Ungar "Closing the Confidence-Faithfulness
  Gap" (Mar'26: calibration vs verbalized are orthogonal directions, steering fix); Sarfati et al. "What LLM
  Forecasters Know but Don't Say" (Jul'26: probe>verbalized + causal ablation test + 30-47% token-saving utility).
  Both pair diagnosis with an intervention/utility payoff. A bare gap-diagnosis reads as incremental.
- **Fine-grained code confidence exists** — per-edit Platt-scaling recalibration (SE venue) closes off
  "granularity" as a standalone novelty claim.

## 2. The genuinely unoccupied residual novelty (narrow, must be stated precisely)
No paper found does ALL of: **(1) per-requirement/per-unit-test granularity** of both probe and verbalization
target; **(2) TRAINED (SFT/RL) self-report** as the target (Ribeiro = zero-shot prompted); **(3) code domain**
with execution-grounded probe labels; **(4) per-requirement downstream utility** (targeted repair). Each element
alone is modest; the paper lives or dies on making the quartet load-bearing and sharply differentiated vs Ribeiro.

## 3. Two vulnerabilities the sweep exposed (both serious)
- **Ribeiro ICSE'26 is one notch away.** Reviewer-2 will cite it and demand differentiation on granularity +
  trained-vs-prompted + utility — the "internal>verbalized on code" claim itself is gone.
- **Our "self-report stuck at 0.60, invariant to loss" is UNDER-SUPPORTED.** Trained self-report reaches
  ~0.86 AUROC on QA (ConfTuner, "Rewarding Doubt" RL). We tried only 2 SFT losses (and brier 0.576 < ce 0.603
  suggests a weak Brier impl, not a law). A reviewer will say "undertrained, not fundamentally stuck." To claim a
  gap we must show even a strong RL-trained self-report stays stuck on code — which is MORE work AND risks
  disproving our own thesis (if RL self-report hits ~0.75, the gap narrows). This is the biggest internal risk.

## 4. The path to a clear accept (demanding; utility is mandatory)
1. **[Anchor, mandatory] Targeted repair via per-requirement probe** — route the lowest-confidence requirement(s)
   to a repair pass; report **+2-8pp absolute pass@1** over (a) no-localization, (b) FLARE-style line-level, (c)
   whole regeneration, across **≥2 benchmarks × ≥3-5 models** (calibrated vs FLARE's 1.72-7.42pp).
2. **[Load-bearing ablation] Probe vs verbalized as the repair-routing signal** — makes the gap *do work*, answers "so what".
3. **[Recommended] Causal faithfulness test** (Sarfati-style evidence ablation) — preempts "just noisier self-report".
4. **[Robustness] Strong RL-trained self-report** — to defend "stuck ~0.60" or honestly report it's an elicitation gap.
5. **[Differentiation] Ablate vs Ribeiro contrastive direction + vs Platt recalibration** (probe captures what recalibration can't).
6. **[Rigor] Bootstrap CIs, Wilcoxon, ≥3 seeds, dev-split layer selection, public code.**

## 5. Honest bottom line + the timeline reality
The pivot is REAL but its novelty is **narrower and its nearest scoop (Ribeiro ICSE'26) closer** than the pivot's
framing implied. The "faithfulness gap" — the part that felt exciting — is largely taken. What remains genuinely
open and AAAI-rewarded is the **per-requirement DOWNSTREAM UTILITY** (targeted repair), with the probe as mechanism
and the gap demoted to a supporting ablation. That is a utility-first paper, not a gap paper.

**For AAAI-27 (8 days):** the required scope — multi-benchmark × multi-model targeted repair + causal test +
self-report robustness + differentiation + rigor — is NOT achievable to a competitive standard in the window, and
the novelty is thin enough that a rushed version invites the "incremental vs Ribeiro" reject. The best-paper route
is utility-anchored and realistically targets a **later venue**. A scoped AAAI-27 attempt is possible but high-risk.
