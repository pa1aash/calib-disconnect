# Recommendation: strongest defensible TMLR contribution (wave 4)

Run date 2026-11-10. This file ranks contributions using the verdicts in `VERDICTS.md`, which were finalized after Critic A, Critic B, and the step 8 gap fill. "Evidence it requires" points to `docs/s3/ORIENTATION.md` section (c), items 1 to 8. The two TMLR criteria (`docs/s2/venue/TMLR_RUBRIC.md` section 2) are:

- **C1:** claims supported by accurate, convincing, and clear evidence ("This is the most important criterion.").
- **C2:** some individuals in the TMLR audience would be interested.

The editorial policy lists, among papers that should not be accepted, "papers that incorrectly claim novelty over existing published work, and papers that merely re-implement an idea that has already been reproduced before." Every novelty sentence below is therefore written as an absence finding with its instrument gaps named.

## Answers to the three required questions

- **L2 pivot criteria (R1 section 6), applied explicitly:**
  1. **A20 (union of at most three works covers probe, stated, and sampling readouts on code with base-instruct pairs and reasoning):** not triggered. Ribeiro et al. (ICSE 2026) and Campos et al. 2611.07876 cover the readouts. No work covers base-instruct pairs or a same-weights reasoning toggle for all three readouts on the same code generations.
  2. **A21 (residual is only a model or benchmark swap, or the only unstudied factor has an established NLP direction):** triggered for the headline "probes beat verbal confidence on code", which is OCCUPIED. Not triggered for the controlled test, whose residual is a label protocol: supervision-matched own readouts, input-only baselines, and within-problem scoring. That residual has code-specific reasons: execution labels allow identical supervision for every readout; function-level difficulty is recoverable from the prompt; and Ribeiro's design contrasts human references with other models' failures. For the base-instruct and reasoning factors, A21 is not triggered because the NLP direction is contested (Yoon versus Barkan, Miao and Ungar), not established.
  3. **A14 (trained stated confidence or recalibration closes the gap in discrimination on code):** not triggered, but now a concrete threat. CREDO 2609.34857 (concurrent, Table 1) raises code AUROC of stated confidence from 0.690 (untrained base) to 0.850 after training on execution labels, with no probe arm. Recalibration cannot close a discrimination gap, because monotone maps leave AUROC unchanged. The strongest version must therefore include a trained own-readout arm.
  4. **A15 (causal intervention already shows where information is lost on code):** not triggered. Code interventions target output correctness (2510.02917; 2609.36783, a null result), not stated confidence.
  - **Outcome:** L2 survives as the spine only in its controlled form. The replacement order of R1 section 6 is not invoked.
- **Measurement-instrument framing (F):** **used.** It is not unused and not contested. Measurement-validity and psychometric vocabulary is used for LLM confidence (Ghosh et al. 2610.25846; 2603.14893). Metrology-proper vocabulary (VIM, GUM, measurand, traceability) is used at a conceptual level for stated-confidence calibration error (2604.26671, Sec 1 and Sec 10; also TRACE 2605.03838 for agentic trust metrics). Every quantity the framing proposes maps onto the Yates or Murphy terms, grouping loss, or meta-I. F may appear only as expository vocabulary, with those works cited, and never as a claimed contribution.
- **Does `src/v4_dprc` belong in the strongest version?** **No.**
  - L4 line-level localization is OCCUPIED (Gros and Devanbu 2512.24560; FLARE 2606.03852).
  - Per-test-group localization and confidence-guided repair are NARROW, and the repair residual shrank after 2609.00854 (abstract only) showed localized repair losing to blind resampling at matched budget.
  - `src/v4_dprc` is frozen legacy code, so L4 would need a new pipeline, a new label unit, and an operator scope decision.
  - Keep it as stated future work. If L4 is mentioned at all, cite 2512.24560 as the line-level occupant and describe the test-group unit as untested.

## Ranked contributions

### Rank 1. Controlled disconnect test on an execution-graded measurement layer (L2 controlled, built on L1, with L3 replay as secondary analysis)

**Contribution sentence.** On self-generated, execution-labeled code from several open model families, we test whether hidden-state probes carry correctness information that the model's own readouts lack, when every readout receives the same supervision, input-only baselines are included, and discrimination is scored both within and between problems; we report how much of the published probe advantage survives these controls and whether the ranking holds under different calibration estimators, an augmented-test oracle, and a per-model release-date split.

**Verdict basis.**

- **NARROW:** L2 Q1c (the controlled test), L2 Q11 (trained stated confidence on code), L2 Q13 (pooled versus within-problem scoring), and the L1 protocol (Q3, Q4, Q5).
- **CLEAN (provisional):** L1 Q10 (test insufficiency) and L1 Q13 (contamination effect on calibration).
- **Closest occupants:**
  - Ribeiro et al. 2512.07404, published at ICSE 2026, including the RQ2 within-task ranking;
  - Campos et al. 2611.07876, concurrent, with within-problem AUROC for probes and output confidence but no verbal readout;
  - CREDO 2609.34857, concurrent, with trained stated confidence on code but no probe;
  - NeuroSym-Cal, Findings ACL 2026, with four readout families but no probe;
  - Tuerlings and Valdenegro-Toro, UncertaiNLP 2026, verbal only, using a post-cutoff window.

**Evidence it requires (ORIENTATION section c).**

- **Item 1, breadth:**
  - at least three open families at two scales;
  - three benchmarks, one post-cutoff per model (LiveCodeBench windows);
  - k of 10 or more samples per problem, so within-problem scoring is defined;
  - at least about 100 mixed-outcome problems per model for the headline comparison.
  - Base and instruct pairs and a same-weights reasoning toggle are run only if the controlled gap clears a pre-registered margin.
- **Item 2, verified harness:** reference solutions pass, flaky tests are removed, and extraction failures are counted separately from wrong code.
- **Item 3, independent labels:** sampling-agreement scores are built only from tests disjoint from the label suite. 2605.09023 Table 6 shows that test-seeded inputs inflate agreement AUROC.
- **Item 4, fixed settings:** seeds, verbatim prompts, parse rules, and pinned revisions are recorded.
- **Item 5, uncertainty at the right unit:** problem-clustered paired bootstrap intervals for every difference.
- **Item 6, controls:**
  - recalibration (isotonic on each readout, with AUROC reported beside Brier skill);
  - at least two formats for stated confidence;
  - the release-date split;
  - the augmented-test oracle swap (HumanEval+ and MBPP+ against the original tests);
  - input-only baselines (a prompt-only probe and a candidate-text-only classifier);
  - a trained own-readout (a verbal or logit-feature head fit on the same execution labels).
- **Item 7, claim sizing:** the headline is reported per model, because the within-problem margin is model-dependent (Campos Table V: about tied for Qwen3-Coder under shift; trained methods at 0.69 to 0.78 within problem for gpt-oss in distribution).
- **Item 8, released artifacts:** per-sample outputs, labels, and analysis JSON.
- **Secondary analysis (L3):** an offline routing replay on the same generations, gated by stated or probe confidence and compared with random routing and a label-sorted oracle at matched execution budgets, stratified by pass rate.

**TMLR fit.**

- **C1:** strong by construction. The claim is a controlled measurement reported whichever way it comes out. A null result would correct how the uncontrolled code probe results are read. A positive result would locate a real loss of information under matched supervision and justify the factorial follow-up.
- **C2:** good. The audience includes calibration researchers (exact labels), code-generation and agent researchers (when to run tests or defer), and interpretability researchers (whether states encode unreported correctness). The occupants' venues in 2026 (ICSE, Findings of ACL, UncertaiNLP, COLM) show active interest.

**Main risk.**

- **Scooped by concurrent work.** A concurrent group runs the supervision-matched within-problem comparison first. Campos et al. already report within-problem AUROC and have the models and labels. Even so, the verbal readouts, the trained own-readout arm, the oracle swap, and the release contrast would still stand.
- **Concrete threats:**
  - the trained arm closes the gap, as CREDO and Probe-SD suggest it may. That would be the reported finding, not a failure.
  - verbal readouts may collapse on small models.
  - the unread leads (Crossref record 10.1109/tse.2026.3713834; 2610.19226) are read before submission.

### Rank 2. Label-oracle and estimator sensitivity protocol alone (L1)

**Contribution sentence.** We show whether the ranking of four confidence families on code (sampling agreement, token probability, stated confidence, and hidden-state probes) changes when execution labels are strengthened with augmented tests, when the calibration estimator changes, and when problems released after each model's training cutoff are separated from those released before.

**Verdict basis.**

- **OCCUPIED (union):** the comparison itself (Ribeiro plus NeuroSym-Cal, both published).
- **NARROW:** the protocol (Q3, Q4, Q5).
- **CLEAN (provisional):** Q10 (test insufficiency changes rankings) and Q13 (contamination changes calibration).

**Evidence it requires.** ORIENTATION items 1 to 8, with item 6 as the core: the oracle swap, the estimator set (equal-width, equal-mass, and debiased ECE, Brier skill with reliability intervals, AUROC, and AURC), and the release split.

**TMLR fit.**

- **C1:** strong. The claims are factual and checkable.
- **C2:** moderate. The audience is mainly people who evaluate code models, and the paper is a methods contribution rather than a finding about models.

**Main risk.** The rankings may turn out invariant to all three controls. That would still be publishable as a narrowly stated robustness result, but it is less interesting. The CLEAN (provisional) cells also rest on gapped instruments: arXiv full-text search failed, the OpenAlex budget was exhausted, and Semantic Scholar keyword search was rate-limited.

**Role.** This is the fallback spine if Rank 1 is scooped. It is also the measurement layer of Rank 1.

### Rank 3. Stated-confidence update after a shown failing test (L3 Q2 and Q7)

**Contribution sentence.** We measure whether a code model's stated confidence changes after it is shown a genuinely failing test, a spuriously failing test, or a placebo, and whether the change predicts repair success.

**Verdict basis.** CLEAN (provisional). The nearest works do not occupy it:

- Kaddour et al. 2602.06948: tests are never observed;
- Barkan et al. 2512.24661: in-advance confidence only;
- Not-One-Belief 2610.35694 and Resist-and-Update: non-code.

**Leads to read before any novelty sentence:**

- 2610.19226, abstract only (LADDER 2610.34737 was checked in full text and is adjacent: domain-level self-assessment from simulated user feedback on non-code QA, no executed tests);
- the forward citers of Resist-and-Update, which were not screened (HTTP 429).

**Evidence it requires.** ORIENTATION items 3 to 5 and 7: paired programs with each of the three arm types, the change in stated confidence, its AUROC against repair success, and problem-clustered intervals. The placebo-controlled retry design of 2607.26117 is the design precedent.

**TMLR fit.**

- **C1:** good for a small, well-controlled study.
- **C2:** moderate, mainly the agent community.

**Main risk.** It is an add-on rather than a paper on its own. Its CLEAN (provisional) verdict rests on the gapped instruments listed above, and a one-paragraph experiment inside an agent paper would not show up in titles or abstracts. It fits best as a section of the Rank 1 paper.

### Rank 4. Confidence-routed execution budgets (L3 Q1, Q4, Q5)

**Contribution sentence.** On the same generations, we compare routing execution by elicited stated or probe confidence with random routing and a label-sorted oracle at matched execution budgets, stratified by pass rate.

**Verdict basis.** NARROW. The comparator design is published:

- TRIAGE 2605.13414 normalizes token-budget plans between random and oracle on LiveCodeBench;
- 2606.15841 has random, threshold, and oracle arms with a logit proxy and injected label noise.

What remains is the gate (elicited verbal or probe confidence) and the unit (execution budget per candidate).

**Evidence it requires.** ORIENTATION items 3, 5, and 7.

**TMLR fit.**

- **C1:** good as an offline replay.
- **C2:** moderate.

**Main risk.** Give-Up 2611.06372 predicts that gates fail when the mean pass rate is below about 0.1 or the rank correlation is below about 0.3 to 0.55, so the result may be null on hard strata. The analysis is inside Rank 1 as a secondary result.

### Not recommended

- **L4 per-requirement confidence (`src/v4_dprc`).** NARROW, but it needs an unrun pipeline and an operator scope decision. It stays as future work (see above).
- **F as a contribution.** OCCUPIED. Its vocabulary may be used for exposition only.
- **Any headline of the form "probes beat stated confidence on code".** OCCUPIED (Ribeiro et al., ICSE 2026). Claiming it would be an incorrect novelty claim.

## Concurrency sensitivity

The six-month concurrency window (works first posted after 2026-05-10) is an operator decision. If concurrent works are ruled out of scope:

- L2 Q11 returns to CLEAN (provisional), because CREDO is concurrent;
- L2 Q13 moves toward CLEAN (provisional);
- L1 Q1 stays OCCUPIED (union) through published works.

The ranking above does not change. Rank 1 is designed against the concurrent works, not around their absence.
