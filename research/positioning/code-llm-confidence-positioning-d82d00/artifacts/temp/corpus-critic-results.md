# Corpus-critic gap fill results (step 8)

| Gap | Fetcher | Result | Effect on positions |
|---|---|---|---|
| Trained stated confidence on code with AUROC (critical) | cc-1 | **Strengthening/threat source found:** CREDO 2609.34857 Table 1 (code AUROC 0.690 base to 0.850 trained, no probe); EpiCaR 2601.06786 Table 4; ExecuCritic 2609.16604 Table 5 (separate critic) | L2 Q11 CLEAN (provisional) to NARROW; A14 threat concrete, not triggered |
| Controlled probe margin (critical) | cc-1 | No overturning source (19 citers screened); Campos Table V shows the small margin is model-dependent | confidence in "at most about 0.05" lowered to medium-low |
| L3 routing by elicited confidence (critical) | cc-2 | No overturning source; ARIA 2610.13870 (random arm, no oracle, no confidence) and 2608.14653 narrow lightly | L3 routing stays NARROW |
| Update after failing test (high) | cc-2 | No overturning source; 2607.26117 gives a placebo-controlled retry design precedent; Resist-and-Update citers 429 (gap) | stays CLEAN (provisional) |
| Release-date contamination effect on calibration (high) | cc-3 | No overturning source; 2,100 LiveCodeBench citers screened (429 at offset 2,100) | L1 Q3 NARROW, Q13 CLEAN (provisional) |
| Label independence and test insufficiency (high) | cc-3 | No overturning source; 2610.11300 uses only strengthened suites; SWE-ABS rank shifts are for agents | L1 Q4 NARROW, Q10 CLEAN (provisional) |

Reports: `research/positioning/w4/parts/cc-1/REPORT.md` (written by the orchestrator from the sub-agent summary because its write was refused), `cc-2/REPORT.md`, `cc-3/REPORT.md`.
