# CITING: forward-citation screen, fcs-A3 (wave 5, Part A)

Retrieval date 2026-11-10. Sources: Semantic Scholar Graph API `/paper/arXiv:<id>/citations` (no key, paced about 1.5 s, backoff 2 to 32 s on 429) and OpenAlex `works?filter=cites:<W id>&per-page=200&cursor=*` (no key). Every raw response is in `raw/` with a `.hdr.txt` giving URL, date, and HTTP status. Abstracts came from the citation APIs; arXiv posting dates from `raw/ax_meta.xml` (export.arxiv.org). Merge by arXiv id, then by normalized title (lowercase alphanumerics, first 60 characters). Vault check: `grep -rilF` on arXiv id and distinctive title words over `research/notes`, `research/positioning/w4/dossiers`, and `research/positioning/w4/VERDICTS.md`.

Tags as in W4: CLOSE = could make or partly make a candidate's core claim; RELATED = relevant, not core; UNRELATED. Tags rest on title plus abstract; the one new CLOSE citer was then read in full text (`dossiers/2611.07913.md`).

## Count summary and completeness

Seed-level S2 `citationCount` lookups for the four non-Spiess seeds returned HTTP 429 after backoff (`raw/s2_<id>_meta.*`); their citation lists themselves returned HTTP 200 with no `next`, so completeness for those rests on the list endpoint and on the OpenAlex `cited_by_count` cross-check.


| Seed | Title (short) | S2 citers | OpenAlex rows (`cited_by_count`) | Merged distinct | New vs W4 | Completeness |
|---|---|---|---|---|---|---|
| 2607.12985 | Resist and Update: Counterfactual Report Coordinates | 2 (HTTP 200, no `next`) | 2 (2) | 3 | 3 (never screened) | complete on both sources |
| 2603.18893 | Don't Ask: What Numeric Self-Reports Measure | 1 (HTTP 200, no `next`) | 2 (2) | 2 | 1 (OpenAlex only) | complete on both sources |
| 2610.18066 | Uncertainty Evaluation: Bridging ML and Measurement Science | 0 (HTTP 200) | 0 (0) | 0 | 0 | complete: zero citers on both sources |
| 2504.03359 | A metrological framework for uncertainty evaluation in ML classification | 14 (HTTP 200, no `next`) | 13 (15) | 16 | 2 (OpenAlex only) | S2 complete; OpenAlex returned 13 rows against `cited_by_count` 15, a gap of 2 records the `cites:` filter does not expose |
| 2402.02047 | Calibration and Correctness of Language Models for Code (Spiess et al.) | 100 (see below) | 96 (102) | 122 | 0 | S2 complete; OpenAlex returned 96 rows against `cited_by_count` 102, a gap of 6 records the `cites:` filter does not expose |

### Spiess et al. (2402.02047): resolution of the W4 gap

- **Semantic Scholar is complete at 100.** The paper record (`raw/s2_2402.02047_meta.json`) reports `citationCount` 100. A single call with `limit=1000` returned 100 rows; `offset=99` returned 1 row; `offset=100, 200, 300, 400, 500` each returned an empty `data` array (HTTP 200). The W4 "cap at 100" was the true total, not a cap.
- **OpenAlex is 96, not 200.** The W4 table's "200" for OpenAlex was the HTTP status recorded in `fcs-G2/raw/_status_log.json`; the saved W4 page `oa_arXiv_2402.02047_p0.json` has `meta.count` 96 and no `next_cursor`. The fresh pull (`raw/oa_2402.02047_c0.json`, per-page 200) also returns 96 with no cursor. A title search (`raw/oa_spiess_titlesearch.json`) finds one other OpenAlex work with the title, the Zenodo ICSE artifact (W7223731100, 0 citers); there is no separate unmerged arXiv record.
- **Dedupe against W4.** The W4 Spiess set (fcs-G2 raw S2 page plus OpenAlex page, merged with the same rule) has 122 distinct citers. The W5 set also has 122. By arXiv id and normalized title, **122 of 122 match; 0 citers are new**. Nothing remained to screen under the A3 rule.
- **Audit of the W4 blanket tag (not required, recorded for the orchestrator).** fcs-G2 itemized about 16 Spiess citers and tagged "the remaining" UNRELATED without a list. Reading the 122 titles, every item that bears on the highlight criteria is already in the vault: 2512.07404 (Ribeiro et al.; also as 10.48550/arXiv.2512.07404 "Do LLMs Trust the Code They Write?"), 2611.07876, 2608.08266, 2501.12934, 2504.14640, 2610.21248, 2605.19369, 2604.06723, 2508.16131, 2510.22614, 2503.15341, 2512.24560, 2512.08810, 2605.28500, 2607.12273, 2610.11300, and 10.1016/j.jss.2026.112852 (mentioned in vault notes as a reference). Two unitemized citers should be RELATED rather than UNRELATED, both absent from the vault: 10.1109/BigData62323.2024.10825139 "Predicting ChatGPT's Ability to Solve Complex Programming Challenges" (predicts success on 3,323 Kattis tasks from task characteristics; bears on the input-only baseline of L2), and 10.1186/s13040-026-00518-4 "A crisis of overconfidence" (clinical perspective on post-training overconfidence). No unitemized citer is CLOSE.

## Seed 2607.12985: Resist and Update: Counterfactual Report Coordinates for Incentive-Compatible LLMs

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2611.07913 | Same Answer, Different Future: Matched Predictions Do Not Imply Matched Belief Updating in Language Models | S2+OA | CLOSE (abstract); nearest, not occupying after full text | L3 Q2/Q7: stated estimate versus continuation updating after new evidence; synthetic Bernoulli, no code | absent; dossier written |
| 2 | 2026 | 2609.22359 | Resist, Update, Reject: Preference Optimization Installs a Prior-Dependent Reliability Switch | S2 | RELATED | L3 Q7 analogue: update on reliable, reject unreliable sources; answers, not confidence; Qwen2.5-7B, Llama-3.1-8B | absent |
| 3 | 2026 | 2610.25650 | Consistency Training Suppresses Cue Following Without Teaching Cue Selectivity | OA | RELATED | L3 Q7 analogue: valid versus spurious cues; answer changes, not confidence; no code | absent |

## Seed 2603.18893: Don't Ask: What Numeric Self-Reports Measure in Language Models

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2608.20569 | Open-Weight Masked Introspection: Measuring What Language Models Can Report About Their Own Computation | S2+OA | RELATED (W4: UNRELATED) | L2/F: linear probe recovers intervention presence at 75% to 95.8% while self-report is at chance (AUROC about 0.5007); introspection, not correctness, no code | absent |
| 2 | 2026 | 2610.22460 | Functional Welfare for AI Safety | OA | UNRELATED |  | absent (phrase "functional welfare" appears in the Don't Ask note, not this paper) |

## Seed 2610.18066: Uncertainty Evaluation: Bridging Machine Learning and Measurement Science

No citing papers on either source (S2 `data` empty; OpenAlex `meta.count` 0, seed `cited_by_count` 0).

## Seed 2504.03359: A metrological framework for uncertainty evaluation in ML classification models

Rows 1 to 14 repeat the W4 S2 list (fcs-G4 CITING.md); W4 tags are unchanged. Rows 15 and 16 are new from OpenAlex.

| # | Year | Id | Title | Src | Tag | Bears on | Vault |
|---|---|---|---|---|---|---|---|
| 1 | 2026 | 2605.03838 | TRACE: A Metrologically-Grounded Engineering Framework for Trustworthy Agentic AI Systems | S2+OA | CLOSE (W4) | F.1: metrology vocabulary for agentic AI trust metrics | dedicated (W4 note added after fcs-G4) |
| 2 | 2026 | 2602.12975 | Extending confidence calibration to generalised measures of variation | S2 | RELATED | F: VCE calibration metric | absent |
| 3 | 2027 | 10.1016/j.measurement.2026.123752 | Uncertainty evaluation and metrological traceability of ML-based measurement systems: a review of GUM extensions | S2+OA | UNRELATED |  |  |
| 4 | 2026 | 10.1016/j.measurement.2026.122819 | Physically constrained TCN-CRF cascade framework for hydraulic support state recognition | S2+OA | UNRELATED |  |  |
| 5 | 2026 | 10.1088/1681-7575/aea165 | Digital precision in metrology: significant figures and trailing zeros | S2+OA | UNRELATED |  |  |
| 6 | 2026 | 10.3390/metrology6030050 | Metrological framework for low-cost radiation shield errors | S2+OA | UNRELATED |  |  |
| 7 | 2026 | 10.1088/1681-7575/ae85ff | Digital transformation in ionizing radiation metrology | S2 | UNRELATED |  |  |
| 8 | 2026 | 10.1109/AI4IM69129.2026.11558218 | Uncertainty Evaluation in classification-based ML measurements: towards a GUM-based methodology | S2+OA | UNRELATED |  |  |
| 9 | 2026 | 10.1088/2632-2153/ae35ce | U-TraCE: a conformal prediction approach to UQ in black-box models | S2+OA | UNRELATED |  |  |
| 10 | 2025 | 10.1007/s10712-025-09916-5 | A Metrological Framework for Uncertainty in Satellite and In Situ Earth Observations | S2+OA | UNRELATED |  |  |
| 11 | 2025 | 2511.00301 | Systematic evaluation of UQ techniques in deep learning: photoplethysmography | S2+OA | UNRELATED |  |  |
| 12 | 2025 | 2505.18893 | Reality Check: A New Evaluation Ecosystem Is Necessary to Understand AI's Real World Effects | S2 | UNRELATED |  |  |
| 13 | 2025 | 2503.21510 | An uncertainty-aware Bayesian framework for ML classification: land cover | S2+OA | UNRELATED |  |  |
| 14 | 2026 | 10.1109/TGRS.2025.3649800 | Terrain-Aware UQ and Cross-Sensor Consistency of Hyperspectral Surface Reflectance | S2+OA | UNRELATED |  |  |
| 15 | 2026 | 2607.19999 | Good Practice Guide for quantifying uncertainties for ML models applied to photoplethysmography signals | OA | UNRELATED |  |  |
| 16 | 2026 | 10.2139/ssrn.7460168 | Optical edge localization with a learned search domain: measurement-chain integrity and uncertainty evaluation | OA | UNRELATED |  |  |

## Seed 2402.02047: Calibration and Correctness of Language Models for Code

No citer is new relative to the W4 fcs-G2 set (0 of 122; see the resolution above). No rows to screen.

## Highlight check

No CLOSE citer found in this pass runs probes against verbal or trained stated confidence on execution-labeled code, uses within-problem scoring, swaps the test oracle, or splits calibration by pre- and post-cutoff release. No citer measures stated-confidence change after a shown failing test on code. The only update-after-evidence citer (2611.07913) is a synthetic Bernoulli task with no code and no self-correctness confidence.
