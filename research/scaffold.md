# Scaffold — code-llm-probe-verbalize-gap-3d8995

## User Prompt (VERBATIM — gospel)
See research/query-code-llm-probe-verbalize-gap-3d8995.md (full verbatim query persisted there).
Assess novelty + AAAI-27 main-track viability of the PIVOTED direction: code LLMs internally encode
per-requirement correctness (probe ~0.72-0.75) but can't verbalize it (self-report ~0.60) — a
per-requirement faithfulness gap on code + probe method + downstream utility. Adversarial reviewer-2
mindset, committed verdict, grounded in our real numbers (oracle 0.805>scalar 0.743, 34% partial-pass,
probe 0.745 trained/0.706 base, self-report 0.603 ce/0.576 brier).

## Run config
- vault_tag: code-llm-probe-verbalize-gap-3d8995
- query_file: research/query-code-llm-probe-verbalize-gap-3d8995.md
- modality: synthesize (defended verdict with evidence chains) + compare (vs closest prior work)
- response_format: argumentative (novelty defense at a reviewing bar)

## Modality rationale
Not enumerative — it's a committed novelty/viability VERDICT grounded in prior-work positioning and our
real results. Argumentative: must defend residual novelty against the closest scoops (probing/EAGLE/
faithfulness) and commit accept/borderline/reject with the harshest objection.

## Tier rationale
Likely FULL — adversarial novelty assessment against a dense prior-work cluster (latent-knowledge
probing, EAGLE, verbalized-confidence faithfulness), committed verdict, high stakes (gates a P2 build).
Confirm from prompt-decomposition.json after step 1.

## Wrapper requirements
- save path: research/notes/final_report_code-llm-probe-verbalize-gap-3d8995.md
- citation style: inline
- terminal sections: prioritized experiments to convert borderline -> clear accept; committed verdict.
