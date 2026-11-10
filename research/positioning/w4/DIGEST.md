# Wave 4 digest: positioning for the TMLR submission

> **Wave 5 update (2026-11-10).** Parts of this digest are superseded:
>
> - **Pivot A14 is triggered** by the concurrent work 2610.31820, which shows a trained own-readout tying a same-label probe on code in pooled AUROC. Rank 1 is unseated as the spine, and the proposed new spine is the measurement protocol, with the controlled comparison and the routing replay as analyses.
> - **Cell changes:** L1 Q10 and L3 Q2/Q7 are now NARROW, and L2 Q10 is OCCUPIED (concurrent).
> - **Number corrections:** Campos "0.620 versus 0.629" is a mismatched pair (matched under shift: .627 or .540 versus .629). CREDO's untrained Base-d is .782, not .690. The Ribeiro range mixes baselines, and its unit is selection accuracy.
>
> See the wave 5 change logs at the top of `VERDICTS.md` and `RECOMMENDATION.md`, and `../w5/`.


Run date 2026-11-10. Scope: `docs/s3/POSITIONING_BRIEF_R1.md`. Literature window: January 2022 to November 2026. Full records:

- `VERDICTS.md`: verdicts per component, with critic resolutions;
- `RECOMMENDATION.md`: the ranked contributions;
- `dossiers/`: 75 close papers, each in at most 300 words, with full-text section and table citations;
- `references.bib`: 128 entries, all from fetched arXiv and Crossref records;
- `research/notes/final_report_code-llm-confidence-positioning-d82d00.md`: the long report.

"Concurrent" means first posted after 2026-05-10. That window is a proposal for the operator to confirm.

## Bottom line

**The headline "hidden-state probes beat the model's stated confidence on code" is taken.** Ribeiro, Spiess, Devanbu, and Nadi (ICSE 2026, arXiv 2512.07404) show it on four 7-8B instruct models. Probes are 8.7 to 29.0 points better than verbal and likelihood readouts, depending on benchmark and model.

**What remains open is a controlled version of that comparison.** It needs:

- every readout supervised on the same execution labels, including a trained stated-confidence arm;
- input-only baselines;
- within-problem scoring as well as pooled scoring;
- a measurement layer that checks whether the result depends on the test oracle, the calibration estimator, or contamination.

The published within-problem comparisons on code are close to ties (Campos et al. 2611.07876: 0.620 versus 0.629; Miglani et al. 2609.36783: 0.677 versus 0.703). The controlled gap may therefore be small. A null result would still meet TMLR's first criterion, because it corrects how the uncontrolled results are read.

## Verdicts

| Candidate | Verdict | Strongest surviving residual |
|---|---|---|
| L1 measurement foundation | OCCUPIED (union) as a comparison; NARROW as a protocol | estimator set, augmented-test oracle swap, and per-model release split on identical generations, including a probe family; test insufficiency (Q10) and contamination effect (Q13) are CLEAN (provisional) |
| L2 locating the disconnect | OCCUPIED uncontrolled; NARROW controlled and factorial | supervision-matched, within-problem probe versus own-readout comparison; base-instruct and same-weights reasoning toggles; trained stated confidence on code is NARROW because of CREDO 2609.34857 |
| L3 verification utility | NARROW for routing; CLEAN (provisional) for update after failure | routing gated by elicited verbal or probe confidence at matched execution budget; TRIAGE 2605.13414 already has the random and oracle normalization; whether stated confidence updates after a shown failing test is untested |
| L4 per-requirement | NARROW; line level OCCUPIED | per-test-group localization; targeted repair's prior dropped after 2609.00854 (ABSTRACT-ONLY: localized infilling lost 3:40 to blind resampling at matched attempts) |
| F metrology framing | OCCUPIED as a framing | none as a contribution; the vocabulary is used by 2604.26671, TRACE 2605.03838, Ghosh et al. 2610.25846, and 2603.14893 |

No CLEAN verdict is unconditional. Each rests on searches with the instrument gaps listed below.

## Close occupants by candidate

- **L1:**
  - NeuroSym-Cal (Findings ACL 2026): four readout families, no probe, per-model post-cutoff subset;
  - Tuerlings and Valdenegro-Toro (UncertaiNLP 2026): verbal only, shared post-cutoff window, ECE and AUROC decouple;
  - 2610.11300: recalibration of token readouts, base versus instruct;
  - Liu et al. 2609.25938: oracle dependence on SQL;
  - Code-MUE 2607.12273;
  - Campos et al. 2512.08810: multicalibration of token likelihood.
- **L2:**
  - Ribeiro et al. 2512.07404, including RQ2's within-task ranking;
  - Campos et al. 2611.07876: probes, sampling, and pooled versus within-problem scoring, no verbal;
  - CREDO 2609.34857: trained stated confidence on code, AUROC 0.850 against 0.690, no probe;
  - RLCM 2604.23333;
  - Barkan et al. 2512.24661;
  - Open the Oyster 2511.02197;
  - Miao and Ungar 2603.25052: probe versus verbal across base and instruct, non-code;
  - Tahimic and Cheng 2510.02917.
- **L3:**
  - TRIAGE 2605.13414;
  - 2606.15841: random, threshold, and oracle routing with a logit proxy;
  - Give-Up 2611.06372: gates fail at low pass rates;
  - Kaddour et al. 2602.06948;
  - CodeRefuser: abstention, concurrent;
  - the placebo-controlled retry design of 2607.26117.
- **L4:**
  - Gros and Devanbu 2512.24560: line-level calibrated localization;
  - FLARE 2606.03852;
  - TokenRepair 2511.18001;
  - Olausson et al. 2306.09896 and Iscan 2606.31511: matched-budget repair;
  - 2609.00854.
- **F:** 2604.26671; TRACE 2605.03838; 2610.25846; 2603.14893; and the Yates and Murphy decomposition literature, which already contains every quantity the framing would name.

## Pivot criteria (R1 section 6)

- **A20** (a union of at most three works covers the L2 spine): not triggered. No work crosses all readouts with base-instruct pairs and a reasoning toggle on the same generations.
- **A21** (the residual is only a swap): triggered for the uncontrolled headline. Not triggered for the controlled test, which has a code-specific reason: execution labels allow identical supervision for every readout, and difficulty at function level is recoverable from the prompt.
- **A14** (trained stated confidence closes the gap): not triggered, but a concrete threat because of CREDO. A trained own-readout arm is therefore required.
- **A15** (causal localization already done on code): not triggered.

## Recommendation

1. **Rank 1: controlled disconnect test on an execution-graded measurement layer.** Arms:
   - probe;
   - zero-shot and isotonic verbal confidence in two formats;
   - a trained own-readout on the same labels;
   - token likelihood;
   - sampling agreement using tests disjoint from the label suite;
   - prompt-only and candidate-text-only baselines.

   Scoring is pooled and within problem, on self-generated code from at least three open families at two scales and three benchmarks (one post-cutoff per model), with at least about 100 mixed-outcome problems per model. Uncertainty comes from a problem-clustered paired bootstrap. The measurement layer swaps original and EvalPlus tests, varies the estimator, and splits by release date. An offline routing replay is the secondary analysis. Base-instruct and reasoning arms are run only if the controlled gap clears a pre-registered margin.
2. **Rank 2: the L1 protocol alone.** This is the fallback if Rank 1 is scooped.
3. **Rank 3: stated-confidence update after a shown failing test.** A small section, CLEAN (provisional).
4. **Rank 4: confidence-routed execution budgets.** Folded into Rank 1 as a replay.

**Decisions:**

- **Measurement-instrument framing:** used. It is exposition only, never a claimed contribution.
- **`src/v4_dprc`:** stays out of the strongest version. Line-level localization is occupied, the repair residual shrank, and the legacy code is frozen.

**Main risks to Rank 1:**

- **Scoop.** A concurrent group runs the supervision-matched within-problem comparison first; Campos et al. have the models, labels, and within-problem metric.
- **Closed gap.** The trained arm closes the gap. That would be the reported finding.
- **Unread leads.** These must be read before any novelty sentence:
  - 2610.19226 (abstract only; LADDER 2610.34737 was checked in full text and does not occupy L3 Q2: it uses simulated user feedback on non-code QA);
  - Crossref record 10.1109/tse.2026.3713834 (title only);
  - the forward citers of Resist-and-Update, which were not screened.

## Instrument gaps

- **G-FT:** arXiv full-text search failed validation. The `searchtype=ft` parameter is ignored, and the real full-text host is off the allowlist.
- **G-OA:** OpenAlex full-text search found 1 of 2 known positives. The OpenAlex daily budget ran out at about 05:05 IST.
- **G-S2:** Semantic Scholar keyword search returned HTTP 429 throughout. Lookups and citation lists worked.
- **G-AX:** the arXiv export API returned HTTP 429 intermittently.
- **G-OR:** OpenReview forum pages and PDFs sit behind a browser challenge.
- **G-FCS:** some forward-citation screens were partial: the Spiess citation list stopped at 100, the last three G4 seeds were blocked, and the Resist-and-Update citers were not screened.

## What the operator should decide

1. **Network access.** Allow search.arxiv.org (full-text search), api2.openreview.net, api.datacite.org, and osf.io for a short gap-closing pass. Alternatively, provide a Semantic Scholar or OpenAlex API key.
2. **Concurrency window.** Confirm the six-month window. If concurrent works are excluded, L2 Q11 returns to CLEAN (provisional); the ranking does not change.
3. **v4 scope.** Confirm that `src/v4_dprc` stays out of scope.
4. **Unread leads.** Read or authorize reading of the leads listed above before the introduction is drafted.
