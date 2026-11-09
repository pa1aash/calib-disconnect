# Scaffold — code-llm-calibration-aaai27-eabf3f (PRIVATE, never appears in report)

## User Prompt (VERBATIM — gospel)
"looks for places where we can extend this paper and make it AAAI 27 main track
level. Go through previous works within this field, look for caveats and holes
that we can write a paper in. shortlist ~5-10 papers and synthesize to have one
final paper idea with a confident headline result that is extremely novel. I
dont want to start running everything and waste time and money and have a dead
paper on my hands. priority 1 is novelty and priority 2 is confidence in
attaining a headline and supporting results. give me a good paper!"

## Run config
- vault_tag: code-llm-calibration-aaai27-eabf3f
- query_file: research/query-code-llm-calibration-aaai27-eabf3f.md
- HPR binary: <user-home>/anaconda3/Scripts/hyperresearch
- modality: **compare/forecast hybrid → treated as SYNTHESIZE** (defended thesis:
  "here is the ONE paper idea and why it beats the alternatives"). Output is a
  single committed recommendation with a scored comparison of candidate ideas.

## Modality rationale
The deliverable is not enumerative coverage of the field (collect) nor a neutral
comparison table. It is a DEFENDED single recommendation: one paper idea, argued
as the best available trade of novelty × confidence, with the runner-up ideas
explicitly compared and dismissed. That is synthesize with a compare sub-structure.

## Tier rationale
[fill after step 1] — expect FULL: this needs contradiction-mapping across the
calibration/selective-generation/train-time-calibration literatures, depth
investigation into whether the headline is achievable on single-GPU compute, and
adversarial critique of novelty vs. closest prior work (Spiess ICSE'25, Campos
multicalibration, Stangel Rewarding Doubt, UQ4CT, semantic-entropy line).

## Binding constraints from the prompt
- P1 NOVELTY, P2 CONFIDENCE-IN-HEADLINE. Ranked, not equal.
- Compute ceiling: single A100-40GB / GH200 98GB. 7B-scale only. No big training.
- Output = ONE paper idea + headline claim + exact experiments + feasibility
  argument + failure mode + fallback + novelty defense.
- Must engage the current paper's own weaknesses (single benchmark, negative/
  diagnostic framing, DeepSeek 0% pass, SFT collapse).

## Wrapper requirements
- No prompt.txt / no wrapper_contract.json present. Save path is the pipeline
  default: research/notes/final_report_code-llm-calibration-aaai27-eabf3f.md
- Citation format: inline with source titles + URLs (standard hyperresearch).
- Terminal section: the final report should end with the committed paper proposal.

## Tier rationale (from step 1)
FULL tier, argumentative, inline citations. This is a research-grade synthesis
that must (a) map a contested multi-literature frontier, (b) adversarially test
whether a proposed headline is both novel AND feasible on constrained compute,
and (c) commit to one defended recommendation with a novelty defense against
named prior work. That requires contradiction-mapping, depth investigation into
feasibility, and adversarial critics — the full 16 steps. Inline citation style
chosen (not wikilink default) because the user explicitly wants a readable
shortlist of 5-10 papers with titles/links they can inspect.

## Dialectical loci to force (P3 argue-don't-report)
- Is the calibration-disconnect finding actually novel/robust, or does Spiess/
  Campos already cover it? (novelty tension)
- Is a PRESCRIPTIVE fix (close the gap) achievable on 7B single-GPU, or does
  every known method need RL/scale we don't have? (feasibility tension)
- Positive result (headline: "we closed the gap") vs. the safer negative-result
  strengthening. Which actually clears AAAI main-track novelty bar?
