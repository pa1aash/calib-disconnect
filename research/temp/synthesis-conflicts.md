# Synthesis conflicts (step 11.2)

Resolved by the orchestrator against full texts, the step 8 gap-fill report (`research/positioning/w4/parts/cc-1/REPORT.md`), and W4 Critic B (`research/positioning/w4/parts/critic-B/CHALLENGES.md`). The synthesizer must follow these verdicts.

## Conflict 1: L2 Q11, trained stated confidence on code
- Drafts A, B, and C say CLEAN (provisional): no code study reports discrimination after training stated confidence.
- Source check: the step 8 gap fill fetched CREDO ([[beyond-verbalized-confidence-calibrating-reasoners-with-differentiable-readouts]], arXiv 2609.34857, concurrent), Table 1: trained stated confidence on DeepCoder with execution labels, Qwen3-8B, in-domain code AUROC 0.850 (CREDO), 0.815 (RLCR), 0.776 (DCPO), 0.753 (GRPO), 0.690 (untrained base). No probe arm. Also EpiCaR ([[epicar-knowing-what-you-dont-know-mattersfor-better-reasoning-in-llms]], Table 4): MBPP AUROC 0.538 out of domain.
- **Verdict:** L2 Q11 is NARROW (residual: trained stated confidence against a probe on the same code generations, within problem). Pivot A14 is not triggered (no probe comparison), but the threat is concrete. Draft B's "trained arm likely closes the gap" gains support; the report must say so.

## Conflict 2: L2 Q1c controlled test, NARROW (A, C) versus OCCUPIED (union) except the trained arm (B)
- Source check: Ribeiro RQ2 (Sec 5.1 to 5.2) ranks each model's own samples within a task against verbal confidence, with "only a few comparisons" significant (Critic B). Campos 2611.07876 Table V gives within-problem AUROC for probes and output confidence, no verbal numeric readout and no trained own-readout.
- **Verdict:** NARROW. Under R1 A20, a union verdict requires the works together to cover every dimension of the core claim; verbal numeric confidence and a supervision-matched own-readout on the same within-problem samples are not covered by Ribeiro, Campos, or Miglani. Draft B's reading is engaged as the strongest objection: the residual is small, and its most informative arm (trained own-readout) is exactly the arm CREDO suggests may close the gap.

## Conflict 3: size of the expected controlled gap
- Drafts A and C use "at most about 0.05 within-problem AUROC" (Campos 0.620 vs 0.629; Miglani 0.677 vs 0.703).
- Source check: Campos Table V shows the small margin for Qwen3-Coder under language shift, but for gpt-oss in distribution trained methods reach 0.69 to 0.78 within problem (cc-1 report).
- **Verdict:** state the prediction as model-dependent and medium-low confidence, not as a single number.

## Conflict 4: L2 Q1 label
- **Verdict:** probe versus verbal at whole-solution granularity is OCCUPIED by Ribeiro alone; the four-family uncontrolled comparison (adding sampling) is OCCUPIED (union) of Ribeiro and Campos (Critic B).

## Conflict 5: Gros and Devanbu probe provenance
- One dossier said the probes read a separate supervisor model. Critic B, on the full text: for the Qwen generator, Probe-7B reads the generator's own states, and Table 4 compares all four families on the same code at line level.
- **Verdict:** follow Critic B. Draft C's point stands: the novelty wording must acknowledge that four families have been compared on the same code at line level.

## Conflict 6: L1 Q1 if concurrent work is excluded
- VERDICTS draft said L1 Q1 would become NARROW; Draft C says it stays OCCUPIED (union) via Ribeiro (probe, verbal, likelihood) plus NeuroSym-Cal (token, verbal, sampling), both published.
- **Verdict:** Draft C is correct.

## Conflict 7: Strict readings in Draft B (Q2b reasoning OCCUPIED by A21 clause 2; L3 routing OCCUPIED (union); Q13 OCCUPIED (union); L4 Q2 OCCUPIED (union))
- **Verdict:** keep the working verdicts (NARROW). L3: no fetched work gates on elicited verbal or probe confidence with random and label-sorted oracle arms on unmodified execution labels. Q2b: the general-NLP direction for reasoning is contested (Yoon versus Barkan, Miao and Ungar), so A21 clause 2's "established direction" condition is not met. Draft B's strict column is reported as the adversarial reading, not adopted.

## Conflict 8: status tags
- CodeRefuser 2605.17029 is concurrent; Code-MUE 2607.12273 and 2605.19369 are published (Critic B). L3 Q6 is OCCUPIED by Kaddour 2602.06948 alone (drop "union").
