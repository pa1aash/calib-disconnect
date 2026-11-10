# cc-3 corpus-critic gap-fill report

Date 2026-11-10. Network: export.arxiv.org and api.semanticscholar.org only (headless curl, desktop user agent, 4 s spacing, 4 to 40 s backoff on 429). OpenAlex and WebSearch not used. No new paper was fetched: no screened hit could overturn either target, and the two relevant near-occupants (2611.07876, 2610.11300) and SWE-ABS (2603.00520) were already full-text vault notes. Raw responses: `raw/` (no client IP echoed; grep clean).

## Gap 1: release-date split for calibration (L1 Q3), target NARROW

### Queries (status, hits)
| Id | Query | HTTP | Hits |
|---|---|---|---|
| g1q1 | verbatim: abs"contamination" AND (abs"calibration" OR "overconfidence" OR "uncertainty") AND abs"code" AND ("post-cutoff" OR "release date" OR "LiveCodeBench") | 200 | 0 |
| g1q2 | verbatim: abs"memorization" AND "confidence" AND "code language models" AND "calibration" | 200 | 0 |
| g1q1b | relaxed: (contamination OR memorization OR post-cutoff OR LiveCodeBench) AND (calibration OR overconfidence OR "uncertainty estimation") AND (code OR program) | 200 | 100 (cap, mostly off-topic astronomy and ML) |
| g1q2b | memorization AND confidence AND code AND calibration | 200 | 4 |
| g1q3 | LiveCodeBench AND (calibration OR "uncertainty estimation" OR overconfidence OR "confidence estimation") | 200 | 28 |
| g1q4 | contamination AND calibration AND ("code generation" OR "code LLMs" OR "code models") | 200 | 0 |
| g1q5 | (uncertainty OR confidence) AND code AND "data contamination" | 200 | 7 |
| ss_lcb | S2 citations of arXiv:2403.07974 (LiveCodeBench), offsets 0 to 2000 (21 pages x 100 = 2,100 records) | 200 each (some pages after 429 retries); offset 2100 returned 429 on three retries, not reached | 2,100 |
| ss_tuer | S2 DOI:10.18653/2026.uncertainlp-main.21 (Tuerlings) | 200 | record found, citationCount 0 |
| ss_08810 | S2 citations of 2512.08810 | 200 | 4 |
| ss_12489 | S2 citations of 2606.09577 | 200 | 5 |

Verbatim phrase queries return 0 on this API even for known-relevant material, so zeros are instrument behavior, not evidence of absence.

### Screening
Title/abstract regex over the 2,100 LiveCodeBench citers (confidence/uncertainty/probe terms AND code terms AND contamination/date/memorization terms) gave 69 hits, screened by title and abstract (`raw/ss_lcb_o*.json`). Relevant to confidence on code: 2611.07876, 2605.09023, 2605.28500 via other lists, 2603.27098, 2609.13975, 2606.03852, 2512.17385 (UCoder, probing for generation, not calibration). Unrelated to confidence: 2608.12771 (memorization probes for code LLMs, no confidence readouts; abstract only), 2608.14303 (contamination detection via influence functions), 2604.21598, 2609.16604 (ExecuCritic, calibrated critic for RL). The 2512.08810 citers (2611.07876, 2607.12273, NeuroSym-Cal, one RAG paper) and the 2606.09577 citers add nothing new.

### Closest items re-read from vault notes
- 2611.07876 (note `which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca`, full text): token-confidence, EigenScore, probe, causal predictors on LiveCodeBench release_v6 and BigCodeBench; the 454 LCB problems "released between October 2024 and May 2025" are used for language shift (around line 1196 of the note). Partitions are problem-level; no pre/post-cutoff calibration split; metric AUROC, no ECE.
- Tuerlings (verbal only) and 2512.08810 (token likelihood) unchanged.

### Verdict
no overturning source found (instrument gaps: arXiv verbatim phrase queries return 0 and full-text search is unavailable; LiveCodeBench citers reached only 2,100 of an unknown larger total because offset 2100 was rate-limited; Tuerlings has 0 indexed citers; titles/abstracts only for non-vault hits; OpenAlex budget exhausted).

## Gap 2: label independence and test insufficiency (L1 Q4), target NARROW

### Queries (status, hits)
| Id | Query | HTTP | Hits |
|---|---|---|---|
| g2q1 | verbatim: (EvalPlus OR "HumanEval+") AND (calibration OR ECE OR AUROC) AND confidence AND "false positive" | 200 | 0 |
| g2q2 | verbatim: ("test insufficiency" OR "weak tests" OR "incorrect programs pass") AND uncertainty AND "code generation" | 200 | 0 |
| g2q1b | (EvalPlus OR "HumanEval+") AND (calibration OR confidence OR uncertainty) | 200 | 75 (mostly diffusion LM decoding, off-topic) |
| g2q2b | ("weak tests" OR "insufficient tests" OR "test insufficiency" OR "false positives") AND (uncertainty OR calibration OR confidence) AND "code generation" | 200 | 2 (2608.14303, 2604.18834; off-topic) |
| g2q3 | uncertainty AND "code generation" AND (test cases OR unit tests) AND (false positive OR weak OR insufficient) | 200 | 0 |
| g2q4 | calibration AND code AND (HumanEval+ OR EvalPlus OR stronger/augmented tests) | 200 | 12 (none a confidence ranking under two suites) |
| g2q5 | tests AND (calibration OR uncertainty) AND (label noise OR false positives OR inflated) | 200 | 100 (cap, off-topic) |
| g2q6 | confidence/calibration AND code AND label/ground truth AND test AND (strengthened OR augmented OR insufficient OR weak) | 200 | 17 (off-topic) |
| g2q7 | ti:"SWE-ABS" | 200 | 1 (2603.00520, already in vault) |
| ss_26100 | S2 citations of 2610.11300 | 200 | 1 (2611.07876) |
| ss_25938 | S2 citations of 2609.25938 | 200 | 0 |

### Papers screened
- 2610.11300 (note `characterizing-overconfident-failure-in-llm-based-code-generation-full-text`, 12,265 words): evaluates only on HumanEval+, MBPP+ (EvalPlus strengthened suites) and BigCodeBench (Section 3.1). There is no base-versus-strengthened oracle swap. Construct-validity paragraph (Section 8, note line 2122): "Although HumanEval+ and MBPP+ strengthen the original tests, execution outcomes may still miss untested" behavior. Supports the claim that the swap is untested here.
- 2603.00520 SWE-ABS (vault, full text): strengthens 50.2 percent of 500 SWE-bench Verified instances, rejects 19.78 percent of passing patches, top agent 78.80 percent to 62.20 percent, "30 rank changes within the top-30 leaderboard". Ranks agents, not confidence estimators; no calibration or AUROC outcome.
- 2609.25938 (SQL, vault): label-oracle sensitivity for conformal risk, not code.

### Verdict
strengthening source found (independent confirmation that the base versus augmented oracle swap on confidence-family rankings is not done in the retrieved code literature: 2610.11300 uses strengthened suites only; SWE-ABS shows rank instability of agents under strengthening, which motivates but does not occupy the swap). No overturning source found (instrument gaps: arXiv verbatim phrase queries return 0; relaxed queries are noisy; 2609.25938 has 0 indexed S2 citers, possibly indexing lag; no full-text search).

## Notes created or re-tagged
None created. Vault notes used, already tagged code-llm-confidence-positioning-d82d00: `which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca`, `characterizing-overconfident-failure-in-llm-based-code-generation-full-text`, `swe-abs-adversarial-benchmark-strengthening-exposes-inflated-success-rates-on-te`. ABSTRACT-ONLY screened items: 2608.12771, 2512.17385, 2609.16604 (not fetched, not load-bearing).
