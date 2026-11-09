# Coverage report — code-llm-calibration-aaai27-eabf3f

Corpus: 85 notes, 65 claims files. Full-tier target (45 min / 55-80) exceeded. No wave 2 needed.

| Atomic item | Status | Representative sources |
|---|---|---|
| Frontier: code-LLM calibration/UQ | WELL-COVERED | Functional Entropy, FASE, ConSelf, Sharma&David, Multicalib-for-code, Spiess ICSE'25, semantic-entropy line |
| Caveats/holes at the frontier | WELL-COVERED | Roelofs (ECE bias), Riddell+TRACER (contamination), Kim&Kang (protocol sensitivity), Miao&Ungar (orthogonality/CoT contamination), Obadinma (adversarial verbal), Xiong (black-box verbal 0.52-0.60) |
| Where current paper falls short | WELL-COVERED | disconnect paper (grounding) + Spiess open gaps + In-IDE@scale negative result |
| Internal-signal / probes for code | WELL-COVERED | AutoProbe, Openia, UCoder, Azaria&Mitchell, RLCM(probe) |
| Train-time calibration (RL/SFT/distill) | VERY WELL-COVERED (15+) | Rewarding Doubt, RLCR/Beyond-Binary, RLCM, CSR, CAPO, DCPO, ConfTuner, LACIE, SaySelf, CONQORD, Uncertainty Distillation, ORCE, Jang(self-verification), Just-Ask |
| Self-consistency / semantic entropy / single-pass | WELL-COVERED | SEP, Dist2ill, Farquhar(Nature), Kuhn, Wang(self-consistency), sample-scaling |
| Selective gen / abstention / deployment | WELL-COVERED | Task Abstention for Code, RisCoSet, CIC, conformal abstention(DeepMind), AdaDec, USCD, In-IDE@scale, Copilot-ZoomInfo |
| Human-AI trust for coding | ADEQUATE | Critical-or-Compliant, In-IDE 153-dev design study, Copilot productivity |
| AAAI-27 topic + format | COVERED | areas-and-topics, main-track CFP, submission instructions |

## Uncovered items: NONE.

## Redundancy note
Two convergent (not derivative) clusters — kept all, they are independent corroboration:
- "sampling/execution semantic-entropy works for code" (Functional Entropy, FASE, ConSelf,
  Sharma&David): different groups/venues, independent. Establishes this as 2026 consensus →
  NOT a novel headline on its own.
- "train-time verbal calibration for QA/math" (Rewarding Doubt, RLCR, CSR, ConfTuner, LACIE,
  SaySelf, CONQORD, UD, ORCE, Jang): independent; unanimous on QA/math, ZERO on code → the gap.

## Key contradictions logged for step 3
1. Our paper: self-verbal AUROC ~0.52. vs Functional Entropy verbal 0.52-0.80 / AutoProbe
   external-judge 0.75-0.97 on simple code. (self vs external; untrained vs judge)
2. CSR: "verbalized confidence is unstable, abandon it." vs Rewarding Doubt/Jang/UD:
   "trained verbalized confidence IS discriminative (AUROC 0.81-0.86)." (feasibility of the fix)
3. AutoProbe informational ceiling (single-pass ~0.77) vs sampling oracle 0.987. (can a cheap
   interface ever match sampling? — bounds the probe direction)
4. DCPO: proven gradient conflict jointly optimizing accuracy+calibration. (design caveat)
