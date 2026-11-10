# Gap-fill report cc-1 (written by the orchestrator from the sub-agent's returned summary)

The sub-agent's own write of this file was refused by its tool policy. Its per-query log is `raw/_status.log`, with raw responses in `raw/`. The text below restates its returned summary.

## Gap 1: trained stated confidence on code with AUROC

**Strengthening source found; L2 Q11 moves from CLEAN (provisional) to NARROW.**

- CREDO (arXiv 2609.34857, Table 1) trains stated confidence with execution labels on DeepCoder, Qwen3-8B. In-domain code AUROC: CREDO 0.850, RLCR 0.815, DCPO 0.776, GRPO 0.753, untrained base 0.690. No probe arm, so pivot criterion 3 (A14) is not triggered.
- EpiCaR (arXiv 2601.06786, Table 4): AUROC 0.538 on MBPP, out of domain, no probe.
- ExecuCritic (arXiv 2609.16604, Table 5): a separate pass/fail critic, AUC 72.8; not the coder's own stated confidence.
- RLCR, ConfTuner, and Rewarding Doubt: no code or execution content in their full texts.

## Gap 2: controlled probe margin

**No overturning source found.** Screened: 14 citers of 2512.07404, 1 of 2608.08266, 4 of 2606.14530 (Semantic Scholar citations); none runs a supervision-matched control. In-vault 2611.07876 (Table V, Sec V-C) gives within-problem AUROC: the "about 0.05" margin holds for Qwen3-Coder under language shift, but not for gpt-oss in distribution, where trained methods reach 0.69 to 0.78 within problem.

## Notes created

`beyond-verbalized-confidence-calibrating-reasoners-with-differentiable-readouts` (CREDO), `execucritic-calibrated-critic-shaping-forcode-generation-with-verifiable-rewards`, `epicar-knowing-what-you-dont-know-mattersfor-better-reasoning-in-llms`, and one off-target note deprecated. All full text.

## Gaps

arXiv full-text search unavailable; Semantic Scholar citation lists lag; OpenAlex not called.
