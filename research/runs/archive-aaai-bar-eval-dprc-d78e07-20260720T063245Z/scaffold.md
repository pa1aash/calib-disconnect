# Scaffold — aaai-bar-eval-dprc-d78e07 (PRIVATE)

## User Prompt (VERBATIM — gospel)
See research/query-aaai-bar-eval-dprc-d78e07.md. Evaluate where DPRC stands vs recently-accepted
AAAI main-track papers (calibration/UQ/selective-prediction + code-LLM), 2024-2026; adversarial
area-chair/reviewer-2 bar-calibration + prioritized gap-analysis to clear AAAI-27 main track.
Uses REAL emerging results (TACO collapse; BigCodeBench per-method oracle 0.931>scalar 0.875, 32%
partial). Deliverables: real-bar description w/ accepted examples; honest accept/borderline/reject
verdict + harshest objection; prioritized gap to-do; strongest framing; highest-leverage "cook
harder" additions.

## Run config
- vault_tag: aaai-bar-eval-dprc-d78e07
- query_file: research/query-aaai-bar-eval-dprc-d78e07.md
- HPR: <user-home>/anaconda3/Scripts/hyperresearch.exe
- modality: SYNTHESIZE (defended verdict on standing + prioritized gap plan; compare-vs-accepted as substructure)

## Modality rationale
Not enumerative (collect) — the deliverable is a defended, adversarial VERDICT on acceptance
standing + a committed prioritized gap-closure plan. Compare-against-accepted-papers is the
evidence substructure feeding the verdict. => synthesize.

## Tier rationale
[fill after step 1] — expect FULL: needs (a) surveying real AAAI accepted papers to establish the
bar, (b) adversarial critique of our standing, (c) committed prioritized recommendation. Argumentative.

## Wrapper requirements
No prompt.txt / wrapper_contract. Save path default: research/notes/final_report_aaai-bar-eval-dprc-d78e07.md.
Citation: inline (user wants concrete accepted-paper examples with links). Terminal section: the
prioritized gap-closure to-do + the honest verdict.

## Key tensions to force
- Is the competitive-vs-functional NEGATIVE-then-POSITIVE contrast a STRENGTH (principled scope
  finding) or a WEAKNESS (reads as "our thing only works on one benchmark")?
- Is a self-expressed per-method AUROC (if it lands ~0.80) ENOUGH over DCPO's scalar 0.79-0.91,
  or does the localization capability need a downstream-utility result to matter?
- Single-benchmark (BigCodeBench) risk vs AAAI's generalization expectations.
- Is the honest current standing "borderline-reject needs more" or "solid accept if the number lands"?
