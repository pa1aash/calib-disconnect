# cc-2 report (corpus-critic gap-fill, L3 routing and update-after-failing-test)

Raw responses: `raw/`. Full query log: `queries.log` (the first A-set and B-set rows appear twice there because the first batch was re-run in the background; results were identical). No client IP appears in the saved responses (checked by pattern). OpenAlex and WebSearch were not used.

## Gap 1: L3 routing by elicited or probe confidence, random and oracle arms (target: NARROW)

### Queries
| Query | Status | Hits |
|---|---|---|
| S2 citations of arXiv:2611.06372 (Give-Up) | 200 | 0 |
| S2 citations of arXiv:2610.30284 (SWE-Verifier) | 200 | 0 |
| S2 citations of arXiv:2606.15841 (Heteroskedastic) | 200 | 2 (2611.05877 knowledge-graph audit; 2608.25553 stale constraints in agent memory; both non-code) |
| arXiv A1 (spec query 2, strict) | 200 | 0 |
| arXiv A2 (spec query 3, as written, OR precedence makes it noisy) | 200 | 50, none relevant by title |
| arXiv A3, A4, A5, A6 (relaxed variants) | 200 each | 0, 1, 0, 0 (A4: Chimera, 2603.22206, a serving scheduler, not relevant) |
| arXiv id_list screen of 8 candidates | 200 | 8 |

### Screened as relevant
- 2610.13870 ARIA: FULL TEXT. Table 1 baselines include "Random: rate-matched advice" and "LLM-decided/prompted consultation"; no oracle arm. Signal is workflow state, "intentionally based on workflow-level signals rather than model-internal confidence or self-assessment". Routes to a stronger model on SWE-bench Verified, Terminal-Bench 2.1, tau2-bench (Gemini models). NARROWS lightly, does not occupy.
- 2608.14653 uncertainty-aware rollback decoding: FULL TEXT. Eight token-level signals, seven code LLMs, equal-budget restart (1,536 tokens). No verbal or probe signal, no random or oracle routing. NARROWS lightly (L4 and L3 vocabulary only).
- 2610.18614 (verbalized step confidence under GRPO, selective execution, ALFWorld/TextWorld/WebShop, Qwen2.5-7B): ABSTRACT-ONLY, not code, not fetched. Not overturning for a code claim.
- 2607.12397 Critic Experience Bank, 2610.36570 CASEL, 2609.02324 Text2Cypher adaptive budgeting, 2601.21469 DebateCoder confidence gating: ABSTRACT-ONLY, screened out (no code confidence routing against random and oracle arms).
- Citation screen of 2306.09896 (317 citers, 4 pages) was also used for Gap 1: no hit with elicited-confidence routing plus random and oracle arms.

### Verdict
No overturning source found (instrument gaps: S2 returned zero citers for Give-Up and SWE-Verifier, which are days to weeks old, so an empty list is an indexing lag, not a zero; the arXiv metadata search is abstract-only and strict AND queries are brittle; the Heteroskedastic citer list has 2 non-code entries).

## Gap 2: update-after-failing-test (target: CLEAN, provisional)

### Queries
| Query | Status | Hits |
|---|---|---|
| arXiv B1 (spec query 1, strict) | 200 | 0 |
| arXiv B2 (spec query 2, strict) | 200 | 0 |
| arXiv B3, B4, B5, B6, B7, B8 (relaxed variants) | 200 each | 0, 1, 1, 1, 0, 0 (B4 2606.31630 probabilistic programs; B5 physics, irrelevant; B6 REHEARSE 2508.14390, non-code cross-instance calibration) |
| S2 citations of arXiv:2306.09896 | 200 (4 pages) | 317 citers, screened by title and abstract (25 by confidence keywords, 59 by repair keywords) |
| S2 citations of arXiv:2607.12985 (Resist-and-Update) | 429 on first try and on 4 backoffs (10, 20, 40, 40 s) | INSTRUMENT GAP, not run |

### Screened as relevant
- 2607.26117 Try Again, Don't Look Back: FULL TEXT. Placebo-controlled matched-budget retry arms (blind resample, content-free notice, execution feedback, feedback plus verbal self-reflection) on MBPP+ at 1.5B, 3B, 7B. Measures repair success only; searched confiden, calibrat, self-assess: no confidence readout. Strengthens the design precedent (placebo arm) but does not occupy.
- 2606.31511 (already in vault, dossier): placebo-controlled self-repair decomposition, no confidence update.
- 2606.31630 Calibration, Not Compilation: ABSTRACT-ONLY via arXiv record; says passing unit tests induce "false confidence that suppresses repair" as a repair-loop effect on probabilistic programs, not a measured model-stated confidence. Not overturning.
- 2608.16003 (checker false alarms after audit-repair context, ProcessBench, signal detection): ABSTRACT-ONLY, non-code verdict shifts; adjacent precedent only.
- 2609.28150, 2610.22698, 2611.06863, 2610.41433, 2611.09212, 2604.10508, 2607.05197: repair-effect studies by abstract; none reports model confidence after failure.

### Verdict
No overturning source found (instrument gaps: Resist-and-Update citer lookup returned 429 after backoffs; arXiv strict AND queries over abstracts cannot see full-text mentions of logged self-assessment in agent papers; S2 citation lists are title-and-abstract screened only).

## Notes created or re-tagged
- ask-your-advisor-learning-when-toconsult-stronger-models-in-agentic-systems (2610.13870), FULL TEXT, claims file written
- do-uncertainty-signals-help-a-systematic-study-of-uncertainty-aware-decoding-wit (2608.14653), FULL TEXT, claims file written
- try-again-dont-look-backblind-resampling-outperforms-self-repair-in-small-code-m (2607.26117), FULL TEXT, claims file written
- Primary-source chase: 0 extra papers.
