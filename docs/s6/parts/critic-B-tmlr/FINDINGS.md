# Critic B (TMLR reviewer, opus): findings on PIPELINE_DESIGN_R0.md

Saved by the orchestrator from the critic's returned text (the critic's own write was blocked). Content as returned.

**Summary.** The paper would interest TMLR readers (criterion 2). Criterion 1 (claims supported by accurate, convincing, clear evidence) is at risk on five blockers.

## Blockers (verified by the critic)

- **F1 (1.2, 1.6, 1.8, Fig 1).** G0 is pooled AUROC and R is within-problem AUROC (R0:52, 60). "Accounted for" (R0:154) implies the gap is an artifact, and the H1 sentence calls this design's raw gap "the published advantage." Campos already makes the pooled-versus-within point (2611.07876.txt:556). Fix: also report a pooled-level residual Gamma(1,1,0,1); rewrite H1 to say where the probe's advantage remains; cite Campos there.
- **F2 (1.8, R0:158; section 2).** Change to "an analogous lattice on this design's generations for each paper's model and benchmark." Add a reconciliation column showing which budget cell, if any, each entry shares.
- **F3 (7.4).** The rank-16 adapter on every layer reads the code through attention, with the same labels and loss as the probe (R0:552, 563), so equivalence is nearly built in. Fix: test a range of adapter capacities, add a probe at the pre-answer position and an MLP probe, and justify which version counts as stated confidence.
- **F4 (R0:128-130).** If the trained readout beats the probe by more than delta, the outcome is labeled "inconclusive." Fix: a third pre-registered decision with its own sentence.
- **F5 (R0:135).** POWER.md:51-54 shows the design also decides at delta 0.02 (P = 1.00); SHARED_SHOCK.md gives half-width about 0.008. The stated power rationale for 0.03 is wrong. Fix: delete or correct item 2; extend the grid below 0.02.

## Major

- **F6 (partly verified).** Margin anchors mix pooled and within-problem units. Campos .627/.629 is from the language-shift setting; Campos reports within-problem AUROC 0.69 to 0.78 for gpt-oss trained methods in distribution (txt:565-566).
- **F7 (suspicion).** HE+ and MBPP+ predate every model and are saturated for strong models; the simulation's Beta(0.6, 0.5) pass rates make the mixed-problem count optimistic.
- **F8.** The probe gets nested hyperparameter search; the adapter has one fixed setting. The refit check is one model, three seeds.
- **F9.** Missing required citations: 2609.33290 (generation shift, 1.5); MARGIN (label toggle); 2610.31820 and CREDO (7.4); 2610.25846 and 2605.09502 (prompt-only and within-problem controls outside code); 2605.27752 (framing); 2610.27455 (not mentioned); Miglani 2609.36783 (missing from the citation table).
- **F10.** Weak reconciliation criteria: failure to reject counted as reproduction; Campos criterion 2 true by construction (prompt-only score is constant within a problem, so W = 0.5); Ribeiro ordering may inherit a scoring anomaly (Reflective far below Random, suspicion); reading-A comparison not paired; Campos's May 2025 problems not in release_v6 and not listed as a deviation.
- **F11.** Sign of the efficiency equation in the prose (R0:91) contradicts the glossary (R0:918).
- **F12.** Under the label toggle the mixed set changes, so phi_l mixes relabeling with a population change.
- **F13.** Outcome sentences generalize beyond the six named models; four of six are Qwen.

## Minor

- **F14.** MBPP CC-BY-4.0 licence and LiveCodeBench scraped-problem terms omitted.
- **F15.** Figure plan: waterfall implies a fixed order; Fig 3 could be a table; Fig 4 mixes 4-toggle and 3-toggle budgets; Fig 5 puts best-of-k on a budget-fraction axis; likely over 12 pages.
- **F16.** Median-filling missing V1 answers creates ties that pull AUROC toward 0.5.
- **F17 (suspicion).** Generation-shift term mixes pass-rate and mixed-set changes; estimated with thinking off while 2610.31820 used thinking on.
- **F18.** Attribution language reads as causal; interaction indices belong in the main text.
- **F19.** No LLM-use footnote; no release or anonymization plan; supplement cap 100 MB versus under 100 GB of hidden states.
- **F20.** Part A files cite PIPELINE_DESIGN_R1 while the file under review is R0.
- **F21.** Power quoted from M = 9 runs for an M = 6 design; "1.00" rests on 100 replicates; probe AUROC 0.71 in R0 versus 0.72 in POWER.md.
