# Confidence estimation for code language models against execution ground truth: an occupancy audit read from the occupied side

This draft argues the minority position. Read strictly under the brief's rules, the field is effectively occupied for any novelty claim the planned paper could make. Ribeiro et al. hold the uncontrolled "probe beats verbal" headline on code [[on-llms-internal-representation-of-code-correctness]]. Campos et al. already report the within-problem collapse that a controlled version would test [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. NeuroSym-Cal and Tuerlings and Valdenegro-Toro cover the multi-family, contamination-aware calibration comparison on LiveCodeBench, between them [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]] [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]. Gros and Devanbu hold localization below the solution level [[localized-calibrated-uncertainty-in-code-language-models]]. CodeRefuser holds risk-controlled abstention on code [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]. Probe-SD and RLCR set a strong general-NLP prior that training the verbal channel closes most of the gap in discrimination (the ability to rank correct above incorrect outputs) [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]] [[beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty-2]].

Under a strict reading of amendment A21 (a residual counts only if it is a new factor, granularity, label protocol, or use, and only if there is a concrete reason code could differ from the closest general-NLP result), most components rated NARROW in the working verdict table fall to OCCUPIED or OCCUPIED (union). What remains falls into two kinds. Some cells are CLEAN (provisional) only because arXiv full-text search failed, so they cannot carry an unhedged novelty claim. The rest are controlled re-tests whose expected outcome is a null.

**Bottom line.** The strongest defensible TMLR paper is a claims-reduced controls study. It runs one fixed set of self-generated generations, scores four readout families plus a supervision-matched own-readout within and between problems, and tests sensitivity to the label oracle and the estimator. It must present itself as a correction to how existing code-confidence results are read, not as the discovery of a disconnect. TMLR's criteria make that paper viable: its first criterion is claims-evidence fit, and its second criterion tells reviewers not to penalize modest significance. Its editorial policy, however, rejects papers that "merely re-implement an idea that has already been reproduced before". That rule kills any paper whose only change is swapping models and benchmarks.

## 1. Scope, instruments, and verdict rules

### A. What is being judged

The brief tests five candidates over January 2022 to November 2026:

- **L1:** an execution-graded measurement foundation with a release-date contamination control.
- **L2:** locating the disconnect between hidden-state probes and verbal and sampled readouts.
- **L3:** verification utility, plus whether confidence updates after a failure.
- **L4:** per-requirement confidence and localization.
- **F:** a measurement-instrument framing.

General-NLP work counts for L2 and F only as the comparison side of a residual. Pre-2022 metric work counts as a foundation, not an occupant.

### B. Verdict rules, applied strictly

The brief defines four verdicts:

- **OCCUPIED:** a fetched work makes the core claim at comparable breadth.
- **OCCUPIED (union):** at most three works together cover every dimension of the core claim, and the only thing left is running them on the same problems.
- **NARROW:** a residual survives both clauses of A21.
- **CLEAN (provisional):** CLEAN except for an instrument gap.

This draft's discipline is to apply A21 clause 2 literally. A residual whose expected result is the general-NLP direction, with no mechanism that would make code differ, is OCCUPIED, even if nobody has run it on code. The same applies to a code mechanism that is only asserted.

The draft also applies pivot criterion A14 strictly. If an elicitation, training, or recalibration method that a fair comparison would have to include is likely to close the gap in discrimination, the L2 spine is at risk even before it is formally triggered.

### C. Instruments

arXiv full-text search failed validation. OpenAlex full-text search found one of two known positives, and its daily budget ran out mid-run. Semantic Scholar keyword search returned HTTP 429 throughout. The arXiv export API also returned HTTP 429 to several queries [[interim-report-l3-confidence-routed-execution-and-update-after-failure]] [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]]. Every negative therefore stands as a gap, never a zero.

The contrarian reading adds one point. Instrument gaps cut against novelty as well as for it. The fetched set already shows a high rate of new work arriving: of 75 close-occupant dossiers, 27 are tagged concurrent. Campos et al. were posted on 5 November 2026, five days before the run [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. With that rate, a gap is more likely to hide an occupant than a clean field.

### D. Committed reading

Only the cells that survive both A21 clauses and a working instrument count as residuals. Under that rule, every candidate is at least OCCUPIED (union) in its headline form. A26 (the all-occupied fallback) is therefore the right frame: state the strongest residual per candidate and decide on a claims-reduced study.

## 2. L1: Execution-graded measurement foundation

### A. The four-family comparison is occupied by union

The core L1 claim is that an execution-graded comparison of sampling agreement, token probability, stated confidence, and hidden-state probes, across families, scales, and benchmarks, shows which methods track correctness on code.

NeuroSym-Cal (Findings of ACL 2026) covers most of this. The vault record is abstract-only, and the full text was read from the ACL Anthology PDF for the dossier. It evaluates a fusion network against logit, P(True), self-consistency, AST-consensus, and IGLB multicalibration baselines on three models (DeepSeek-R1-Distill-Llama-70B, Qwen2.5-Coder-32B-Instruct, Llama-3.3-70B-Instruct) and three benchmarks (LiveCodeBench v2406 to v2506, HumanEval-Pro, DS-1000). It reports unbiased ECE (expected calibration error), Brier, AUROC, and AURC (Sec 4.1 and 4.2), with "Expected Calibration Error (ECE) by 37.4% compared to Self-Consistency (0.072 vs. 0.115) for DeepSeek-R1" (Sec 5.1) [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]].

The missing family is the probe. Campos et al. supply it: they compare Yes/No token confidence, EigenScore sampling, linear probes and LAT, and causal DAS predictors on Qwen3-Coder-30B and gpt-oss-20b. They use execution labels and a problem-clustered bootstrap (Sec IV and V) [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].

Siddiq et al. add a third leg with four families (token probability, verbalized, sampling consistency, and a chain-of-thought self-consistency prompt) on three API or open models with Docker execution labels. They report verbalized security ECE from 0.247 to 0.481 by model [[an-empirical-study-of-security-calibration-in-large-language-models-for-code]]. Rathnasuriya and Yang add 17 generation-stage and 6 prefill-stage token and sampling scores on four 7-8B instruct coders, with best AUC 0.598 to 0.696 (Table 3) [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]].

Three works cover every family, at least three model families, at least two scales, and at least three benchmarks. That is the A20 union case, and the working verdict agrees [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]]. Running all four families on the same generations is exactly the "only thing left" that A20 does not count as a residual.

### B. The protocol residual, pushed toward occupied

The working table rescues L1 as a three-control protocol: estimator set, augmented-test oracle swap, and per-model release split. Each control fails the strict test separately.

**Release-date split (Q3).** NeuroSym-Cal holds out a per-model post-cutoff LiveCodeBench subset (Sec 4.1) [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]]. Tuerlings and Valdenegro-Toro use a shared window from 2024-09-19 to 2025-04-30 with code frozen before elicitation (Sec 3.1 and 3.3). They claim the gap outright: "no existing work compares black-box verbalized elicitation strategies across multiple coding-specialized LLMs on a shared temporally filtered window" [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]].

The surviving residual is "apply the split to the probe family as well." That is adding a family to an occupied control, not a new factor. Under A21 clause 1 it is OCCUPIED.

**Pre-cutoff versus post-cutoff contrast (Q13).** This one is formally CLEAN (provisional): no fetched code paper compares calibration before and after the cutoff [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]]. But it is a body-text claim under failed full-text search. By the brief's own rule, the recommendation cannot claim novelty on it without hedging.

**Label independence (Q4).** Liu et al. show on text-to-SQL that "Every execution-consistency score looks better under the labels of the oracle that built its clusters, in 16 of 16 score-by-checkpoint combinations." They conclude that "A consistency score should be evaluated under an oracle that did not build it" [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]].

The stated reason code would differ is that "hidden tests drive both the label and test-based agreement scores." That is not a difference from SQL. It is the same mechanism Liu et al. identified, which their 16 of 16 result already predicts. Text-to-SQL is execution-graded code generation, so moving the test from SQL to Python is a benchmark change. Under A21 clause 1, Q4 is OCCUPIED for the principle. The only open part is a confirmation whose direction is predicted.

**Estimator sensitivity (Q5).** The fact that calibration and discrimination metrics can rank methods oppositely on code is already shown. Tuerlings Table 1 gives the lowest ECE as 0.013 at AUROC 0.491, and the highest AUROC as 0.841 at ECE 0.216. Sec 4.6 reports that 8 of 18 cells collapsed [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]. Gros and Devanbu flag ECE as misleadingly low under bucket collapse and prefer Brier skill [[localized-calibrated-uncertainty-in-code-language-models]]. Outside code, Ghosh et al. show that verbal confidence "looks well calibrated because it clusters near the base rate while discriminating poorly" [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]].

What is left is a swap of metric variants (equal-mass, debiased, smooth ECE). That is a metric change, not a new factor or protocol. I rate it OCCUPIED on the substantive claim and CLEAN (provisional) only on the cosmetic sub-part.

**Recalibration as a control (Q6).** Rathnasuriya and Yang (Sec 6.1, Table 5) show that Platt and isotonic recalibration cut Brier from 0.459 to 0.248 for CodeLlama while Brier skill stays near 0.001 [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]. Probe-SD shows the same split outside code: Verbal-Iso cuts in-domain ECE from .178 to .013 while AUROC stays at .825 [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]]. A monotone map cannot change AUROC. Recalibration as the control that separates mapping from information is therefore established both as a result and as a fact of mathematics. Extending it across families adds families, not a factor.

**Test insufficiency (Q10).** This is the one L1 cell where I concede a residual with a code-specific mechanism. False passes on plausible-but-wrong programs would inflate exactly the families that track test-style agreement [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]]. The nearest code result, selective generation, shows only that a guarantee tightens as the number of tests grows (Sec 5.2.2) [[towards-functional-correctness-of-code-models-with-selective-generation]]. Q10 is CLEAN (provisional). Its direction is predicted by Liu et al., however, so a positive result confirms rather than surprises.

### C. Committed reading for L1

L1 is OCCUPIED (union) as a comparison. As a protocol, it is OCCUPIED on three of its five controls, and CLEAN (provisional) and direction-predicted on the other two (Q10 and Q13). The working table's NARROW rests on bundling: one design that holds several individually occupied controls together. A20 explicitly discounts "running them on the same problems." Bundling is good measurement practice, and that is its value. It is not a contribution TMLR reviewers will read as new.

What a claims-reduced paper can still say is narrower and checkable: on one generation set, whether the ranking of four families changes under base versus augmented tests. That question is cheap with HumanEval and HumanEval+ and survives as a measured fact either way.

## 3. L2: Locating the disconnect between internal state and output

### A. What Ribeiro et al. occupy, and how firmly

Ribeiro, Spiess, Devanbu, and Nadi (ICSE 2026) fit a LAT direction (Representation Engineering: a principal-component direction over hidden-state differences at the last token) on four 7-8B instruct models. They use HumanEval (151 tasks) and BigCodeBench (457 tasks) and pick the correct candidate among four. They report that "On BigCodeBench, it improves accuracy by +13.3 to +29.0 pp over the best reflective accuracy; on HumanEval, gains range from +8.7 to +26.2 pp" (Sec 4.2.1). Their stated contribution is "Empirically validating that LLMs encode correctness internally, with representation-based scores outperforming likelihood and reflective metrics" [[on-llms-internal-representation-of-code-correctness]].

The same group's follow-up reproduces the setup across construction methods, framings, and read-out locations. It finds that "no single configuration is best" and that isolating the fault "does not help" [[on-the-robustness-of-llms-internal-representation-of-code-correctness]]. Gros and Devanbu reproduce the probe-over-verbal ordering at line level: Qwen line-level Probe-7B BSS (Brier skill score) is 0.29 against -0.72 for line-verbalized, with AUC 0.83 against 0.71 (Table 4) [[localized-calibrated-uncertainty-in-code-language-models]].

So the qualitative claim is published, reproduced by its authors under perturbation, and reproduced by a second group at a finer granularity. TMLR's editorial policy names exactly this case as grounds for rejection: "papers that merely re-implement an idea that has already been reproduced before." A paper whose L2 contribution is "the probe-verbal gap on more models or more benchmarks" fails A21 clause 1 and the TMLR policy together.

### B. The controlled test is closer to occupied (union) than the working table says

The working table rescues L2 with a controlled test. It would put the probe, a supervision-matched own-readout, input-only baselines, and verbal numeric and categorical confidence on the same self-generated samples, scored pooled and within problem.

Each element of that test already exists on code, spread across three works:

1. **Within-problem scoring of probe against own confidence on self-generated code.** Campos et al. define within-problem AUROC "over pairs of candidates from the same problem with different labels." Under language shift they report that "within-problem AUROC lies at 0.58-0.64 for all methods and both models, against a pooled AUROC of 0.67-0.81. For Qwen3-Coder confidence performs best within problem (0.629)" (Sec VI-C).
2. **Input-only baselines.** Campos Table V shows that a probe read at the last prompt token, before any code exists, "matches the judging pass in distribution (0.891)". They conclude: "Much of what the methods predict is thus the problem, not the candidate" [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].
3. **Within-problem verbal comparison.** Ribeiro's four-candidate design is within task by construction. Their reflective verbal readouts fall to about 7% (Qwen, HumanEval) or 15.3% (Mistral, True/False) against 25% chance (Sec 4.2.1). Their RQ2 is a self-generated, within-task ranking over 10 samples, where "Only a few comparisons reached statistical significance" [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].
4. **Within-problem centering on an autoregressive code model.** As reported in the probe-confound investigation, Miglani et al. center activations within problem and fold by problem. They find Qwen2.5-Coder probe 0.677 against completion log-probability 0.703 on 56 mixed problems [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].

Ribeiro, Campos, and Miglani are three works. Together they cover the probe, own output confidence, verbal readouts within task, an input-only baseline, and within-problem scoring on self-generated code. The one element none of them supplies is a supervision-matched own-readout (a verbal or logit-feature head trained on the same execution labels).

The controlled test is therefore OCCUPIED (union) except for one arm. That arm is pivot criterion A14 itself, which is what the next subsection examines. The working table's NARROW depends on the trained arm being the residual, and that arm's expected result points the wrong way for a positive spine.

### C. Trained stated confidence: CLEAN (provisional) on code, but the prior is strong

No fetched code study trains stated confidence on execution labels and reports AUROC. The nearest code instance, RLCM on LiveCodeBench, is ECE-only [[interim-report-l2-residual-post-training-reasoning-format-on-code]]. Formally the cell is CLEAN (provisional).

The general-NLP evidence is unusually direct. Probe-SD scores sampled traces with a probe, overwrites the stated confidence, and fine-tunes. It "cuts ECE from 0.178 to 0.024 in-domain and from 0.542 to 0.113 out-of-domain," with AUROC rising "from 0.825/0.715 to 0.928/0.783," against a frozen probe at .948 [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]]. RLCR adds a Brier reward to RL with verifiable rewards and proves that a bounded proper scoring rule yields models "both accurate and well-calibrated." In its Table 1, trained verbal AUROC matches or beats a final-layer probe on the RLVR model: HotpotQA 0.69 against 0.55, and Big-Math 0.67 against 0.65 [[beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty-2]] [[interim-report-l2-residual-post-training-reasoning-format-on-code]].

Probe-SD also reports a result that anticipates the code null: "Internal states answer 'how certain am I' well and 'which answer is right' poorly." When used to pick among N answers, the probe "nearly ties majority voting yet falls far short of the oracle" [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]]. That is the general-NLP form of Campos's "triage rather than selection" [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].

Is there a concrete reason the code result could differ? The candidates on file are a joint-output obstacle and a "reasoning contamination" effect. The first comes from Zeng et al.'s note that models "struggled to output both code snippets and confidence simultaneously." The second is Miao and Ungar's finding that joint solve-and-rate prompting inverts the confidence direction (Sec 3.4) [[closing-the-confidence-faithfulness-gap-in-large-language-models]] [[interim-report-l2-residual-post-training-reasoning-format-on-code]]. Both are reasons that elicitation on code is harder. Neither is a reason that a trained verbal head would fail to close the gap.

So the honest prediction is a split. Training probably narrows the discrimination gap substantially on code (following Probe-SD). Within problem, every readout probably sits near the 0.6 to 0.7 band Campos reports. In both cases the result follows a known direction.

A contested point keeps A14 open rather than triggered. The When Words Fall Short result, recorded in the source tensions, argues that probe overfitting at a single training endpoint biased earlier comparisons toward verbal confidence. With validation-based checkpoint selection, its estimator beats RL-trained verbal confidence. That dispute is real in general NLP, and it is the one place where a code result could add information. But it is a dispute about estimator training hygiene, not about code. A code paper that adjudicates it is a methods paper on probe training, which belongs to a different literature.

### D. The factorial residuals: base and instruct, reasoning toggle, format

**Base versus instruct (Q2a).** The general-NLP direction is crowded:

- The GPT-4 report states that "the pre-trained model is highly calibrated," with calibration reduced after post-training (Fig 8) [[gpt-4-technical-report]].
- Tian et al. find that for RLHF models, verbalized confidence beats conditional probabilities, "often reducing the expected calibration error by a relative 50%" [[just-ask-for-calibration-strategies-for-eliciting-calibrated-confidence-scores-f-3]].
- Six base and instruct pairs show that "instruction tuning fundamentally harms calibration," with ownership bias up to 26% [[large-language-models-are-overconfident-in-their-own-responses]].
- Instruct models show z-ROC slopes of 0.52 to 0.63 against 0.77 to 0.87 for the base model [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]].
- Miao and Ungar find that "base models verbalize poorly calibrated confidence despite encoding well-calibrated accuracy information internally" [[closing-the-confidence-faithfulness-gap-in-large-language-models]].

The location question ("is the gap present in base models?") has a published general-NLP answer: yes.

The code-specific reason offered is Rathnasuriya and Yang Sec 5.5. DeepSeekCoder base token-confidence AUC is 0.4391, rising to 0.5654 after tuning (dAUC +0.1263, CI [0.0447, 0.2089]). OpenCoder moves by -0.0136 with CI [-0.0911, 0.0652] [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]. That is one pair whose interval excludes zero and one that does not, on one benchmark, for token readouts only. It shows that the token-probability sign is not uniform. It says nothing about the probe-minus-verbal gap, which is the L2 quantity.

There is also a design hazard. Ghosh et al. pre-registered a base-versus-instruct test and declined to run it because the 7B base model's verbal output used "essentially two labels" [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]. The comparison may be undefined for verbal readouts on base models unless a P(True)-style format replaces numeric elicitation. Without that format the factor reduces to token readouts, which Rathnasuriya and Yang already occupy.

Tahimic and Cheng show that SAE directions fit on Gemma-2-2b base keep their effectiveness after instruction tuning (feature F1 0.821 base against 0.772 instruct, Sec 5.5) [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]]. So the probe side of the base-instruct question has a code instance too. My verdict: NARROW at most, weak, with the code reason shown only for token readouts on one pair.

**Reasoning toggle (Q2b, Q9, Q10).** Campos reports that medium-effort reasoning raises gpt-oss Yes-probability AUROC "from 0.68 to 0.73, still below the trained internal methods" (Sec VIII) [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. That is a reasoning toggle on code, on output confidence, with the same weights. Outside code, Probe-SD finds the probe beats verbal on all 24 comparisons in two reasoning models [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]]. Hidden-error-awareness finds probe 0.953 against verbalized 0.67 on MATH-500, including DeepSeek-R1-Distill at 0.852 [[hidden-error-awareness-in-chain-of-thought-reasoningthe-signal-is-diagnostic-not]]. The post-training-stage study shows Pre-CoT AUROC of 0.594 (Instruct), 0.526 (SFT), 0.320 (RL), and 0.644 (OPD) from one backbone. It concludes that "post-training does not uniformly improve confidence calibration" [[post-training-shifts-confidence-a-three-stage-analysis-of-how-sft-rl-and-opd-sha]].

The reasoning residual is "read the probe under reasoning on code with the same weights." Its expected result, "probe still ahead of verbal, verbal modestly better with reasoning," is the union of Campos and Probe-SD. Under A21 clause 2 that is OCCUPIED.

**Format (Q3).** Tuerlings Table 1 occupies format as a factor within verbal readouts on code. Examples: Qwen-32B AUROC 0.834, 0.810, and 0.841 across Direct, CoT, and Linguistic; DS-6.7B 0.518, 0.716, and 0.498 [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]. Ghosh occupies cross-format instability outside code, with Spearman 0.126, -0.069, and 0.247 between formats [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]. The format-by-readout interaction is a nuisance factor to control, not a finding. I rate it OCCUPIED.

**Causal location (Q12).** Code causal work exists and is negative or off-target. Tahimic and Cheng steer output correctness: steering fixes 4.04% of errors but corrupts 14.66% of correct code [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]]. Miglani et al. report a steering null [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]. Outside code, circuit-level work localizes inflated verbal confidence and cuts ECE "0.647 to 0.068" by intervention [[wired-for-overconfidence-a-mechanistic-perspective-on-inflated-verbalized-confid]]. Miao and Ungar steer verbal confidence toward the internal estimate [[closing-the-confidence-faithfulness-gap-in-large-language-models]]. Hidden-error-awareness finds the signal "diagnostic, not causal" [[hidden-error-awareness-in-chain-of-thought-reasoningthe-signal-is-diagnostic-not]]. Pivot A15 is not triggered, but a correlational code paper adds no claim about location either.

### E. Pivot criteria, read strictly

1. **A20 (union).** Formally not triggered for the full factorial, because no three works cross stated confidence with base and instruct pairs and a reasoning toggle on code. For the controlled headline it is triggered except for the trained arm (Sec 3.B).
2. **A21 (residual is only a model or benchmark change).** Triggered for the uncontrolled headline. For the factors, the only code-specific reason on file applies to token readouts, not to the probe-verbal gap. I read that as clause 2 failing for Q2a, Q2b, and Q3, and as surviving only weakly for Q4.
3. **A14 (gap closes under a method we must include).** Not triggered on code, and probably triggered by the paper's own data if it runs the arm the design requires. A spine that depends on A14 not triggering is a spine that may fail its own control.
4. **A15 (causal localization on code).** Not triggered.

### F. Committed reading for L2

L2 as "locating the disconnect" is effectively occupied. The descriptive gap is published and reproduced. Its within-problem collapse is published. The factors either follow known general-NLP directions or cannot be measured for verbal readouts on base models.

The one contribution left is the controlled measurement itself: a single table on the same samples with probe, trained own-readout, zero-shot verbal, token, per-candidate sampling, and input-only rows, scored pooled and within problem. Its most likely result is that the within-problem differences between readouts sit within a few hundredths of AUROC. The evidence predicting that is Campos 0.620 against 0.629, and 0.677 against 0.703 in the Miglani comparison. The probe-confound investigation committed to a controlled gap of "at most about 0.05" at about 65% confidence [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].

That is a null with a clear message: the disconnect on code, as reported, is mostly between-problem difficulty and supervision asymmetry. It is publishable under TMLR's first criterion. It is not "locating the disconnect"; it is showing that the disconnect, as usually measured, is not where it was claimed to be.

## 4. L3: Verification utility and confidence updating

### A. Selective prediction and abstention on code: occupied

CodeRefuser gives risk-controlled abstention (Learn-Then-Test) over execution-cluster agreement on four open code models. It reports "an average of 26.5% and 11.9% absolute improvements w.r.t. abstention precision and F1-score" (Sec 4, Table 1). On MBPP with Qwen2.5-Coder-32B at alpha 0.2 it abstains on about 30% of tasks, against more than 80% for perplexity [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]. Selective generation with FDR control (false-discovery-rate control on the non-abstained outputs) uses fuzz-generated tests [[towards-functional-correctness-of-code-models-with-selective-generation]]. The ICSE-NIER deferral framework reports selective accuracy over 70% at 80% coverage on MBPP+ (Sec 4.1) [[when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-code-predicti]]. Q3 is OCCUPIED, and the working table agrees.

### B. Routing against random and oracle: occupied by union, by strict reading

The working table keeps routing NARROW. Its residual is elicited verbal or probe confidence as the gate, on unmodified execution labels, with matched random and label-sorted oracle arms. Three works already supply every element except the gate's signal class:

1. **Heteroskedastic signals.** Random, threshold, cost-stratified, and oracle routing on MBPP with unit-test feedback and Qwen3-8B, LLaMA3-8B, and GPT-4o-mini. At beta=10%: Random .551, Threshold .636, CST .671, Oracle 1.00 (Table 1). The paper's own finding is that "some regions exhibit near-random discriminability while concentrating many errors" [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]].
2. **Give Up to Get More.** Oracle and round-robin comparators on code (CodeContests), and the deciding theory. The best difficulty-proportional rule captures "at most 13% on hard workloads, even given true pass rates," and the gain from a prior "vanishes between prior rank correlations of about 0.3 and 0.55" [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]].
3. **Campos et al.** The use claim stated directly for the readouts in question: "the predictors are more useful for identifying problems that warrant verification than for choosing among candidates." Also: "To decide which candidates to test in a new programming language, output confidence is a strong baseline" (Sec VI-C and VII) [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].

Switching the gate from a logit proxy to an elicited verbal or probe score is a change of signal, not of factor, granularity, label protocol, or use. Removing Heteroskedastic's 10% injected label noise is a cleaner label, not a new protocol. More decisively, the outcome is predictable from published numbers. A gate helps only above a rank correlation of roughly 0.3 to 0.55, while within-problem AUROC for every code readout is 0.58 to 0.64 under shift [[interim-report-l3-confidence-routed-execution-and-update-after-failure]]. Routing across problems will therefore work about as well as difficulty triage already does, and routing within problems will do little.

The agent literature confirms the pattern at the trajectory unit:

- Learned restarting beats matched random restarting "by up to 1.98 percentage points," entirely via between-task allocation, with within-task AUC "0.50 [0.48, 0.51]" [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]].
- Trajectory predictors reach about 0.62 AUROC against 0.92 for issue difficulty, with gain beyond difficulty "statistically equivalent to zero" [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]].
- More than 99.93% of positive-negative pairs are cross-unit [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]].

SWE-Verifier shows that a trained gate gives 75.47 to 77.20 resolve at 1.09x cost on MiniMax-M2.7 (Table 1) [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]]. CoTT gates test-output generation by sampling agreement and cuts cost from $0.077 to $0.065 [[confidence-gated-transductive-test-generation-for-code-reranking]].

My strict verdict for routing is OCCUPIED (union). The working table's NARROW can be defended only if a change of gate signal counts as a "use." I do not think a TMLR reviewer will read it that way, since the use (budget routing against random and oracle on code) is already demonstrated.

### C. Update after a shown failing test: the one CLEAN (provisional) cell with a code reason

The nearest works do not occupy this cell. Kaddour et al. elicit confidence mid-execution, but "the agent cannot execute code, run tests." Barkan et al. restate confidence per tool call and after contract outcomes, not after a failing test on the same program. Resist-and-Update and Not-One-Belief are non-code QA. Iscan's placebo-controlled self-repair never elicits confidence [[interim-report-l3-confidence-routed-execution-and-update-after-failure]].

Here a concrete code reason exists. A failing unit test is verifiable, local evidence about the model's own artifact, and a spurious failure (a wrong test) can be built cleanly. Neither has a clean analogue in QA pressure studies.

But the cell is a body-text claim under failed full-text search. The forward screens of the three closest occupants were not run. The investigator's own confidence is 45 to 55% [[interim-report-l3-confidence-routed-execution-and-update-after-failure]]. One paragraph inside an agent paper would not appear in any title or abstract search. And the experiment is small, a few hundred paired programs, so it supports a section, not a spine.

### D. Committed reading for L3

Selective prediction is OCCUPIED. Routing is OCCUPIED (union) in strict reading and NARROW in a permissive one. Its expected result is a negative in the hard stratum and difficulty-level triage elsewhere. Update-after-failure is CLEAN (provisional), and it is the most interesting surviving cell in the whole audit. It should be a hedged secondary experiment, not a contribution claim.

## 5. L4: Per-requirement confidence and localization

### A. Line, token, edit, and step localization: occupied

Gros and Devanbu build "Minimal Intent Aligning Patches" verified by hidden tests. They compare token probability, multisampling, line-verbalized reflection, and probes on HumanEval+, MBPP+, LiveCodeBench, and RepoCod-s. Probes "with a small supervisor model can achieve low calibration error and Brier Skill Score of approx 0.2" [[localized-calibrated-uncertainty-in-code-language-models]].

The other granularities are covered too:

- FLARE localizes at line level from coder token probabilities: 67% Top-1 localization, and +1.72 to +7.42 pp Pass@1 over NL-Debugging [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement]].
- PtTrust assesses line-level risk from internal states [[risk-assessment-framework-for-code-llms-via-leveraging-internal-states]].
- Local Platt scaling of token and edit confidence covers 14 models, with text-match rather than execution labels [[fine-grained-approaches-for-confidence-calibration-of-llms-in-automated-code-rev]].
- Agent-step probes decode test-pass, failing-test reduction, and regression with "AUC up to 0.83" [[260705188-latent-programming-horizons-in-coding-agents-full-text]].

Q4 is OCCUPIED.

### B. Per-test-group unit: the residual survives A21, and that is not enough

Per-test-group confidence, evaluated as localization of the failing requirement, is a new granularity. It passes A21 clause 1. Gros and Devanbu state that their setting "does not assume access to test cases," in contrast to spectrum-based fault localization [[interim-report-l4-localization-occupancy-and-targeted-repair]]. And 2607.05188's "partial correctness" label is a program-version unit, not a test group [[260705188-latent-programming-horizons-in-coding-agents-full-text]]. Formally, NARROW.

The contrarian objection is evidential, not definitional. The pipeline is frozen legacy code run only as a five-problem stub. Its labels are hidden-test outcomes, which are noisier and less independent than patch labels. And Gros and Devanbu's leave-one-out collapse warns that fine-grained probes transfer badly (Qwen Probe-7B BSS -0.01 on held-out LiveCodeBench) [[interim-report-l4-localization-occupancy-and-targeted-repair]]. A TMLR paper needs evidence in hand, and L4 has none.

### C. Targeted repair versus regeneration: occupied by union

FLARE gives confidence-derived targeted repair without a matched-budget arm [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement]]. Olausson et al. give the matched-budget protocol: "pass rates are higher or equally high with i.i.d. sampling (without repair), especially when the budget is small." Iscan's pre-registered study finds that blind resampling beat bare-code retry by +18 net unlocks [[interim-report-l4-localization-occupancy-and-targeted-repair]]. Siddiq et al. find that calibration-guided repair gives "only limited improvements while frequently introducing functional regressions" [[an-empirical-study-of-security-calibration-in-large-language-models-for-code]].

The signal, the protocol, and a negative prior all exist. What is left is running FLARE-style targeting under the Olausson protocol, which is the A20 union case. And it is a repair-method comparison, not a calibration claim.

### D. Self-written test adequacy against own confidence

This cell is CLEAN (provisional), with only four forward citers of the line-level occupant screened [[interim-report-l4-localization-occupancy-and-targeted-repair]]. It is the least connected to the paper's calibration question.

### E. Committed reading for L4

L4 is OCCUPIED at line level and OCCUPIED (union) for targeted repair. It is NARROW only for a test-group unit that has no evidence behind it. It ranks last.

## 6. F: Measurement-instrument framing

### A. Every proposed quantity maps onto an existing one

The framing proposes three quantities:

- **Readout bias.** This is the calibration-in-the-large term (mu_F - mu_Y)^2 of the Yates covariance decomposition, which Vieira rearranges into "a variance mismatch term, a correlation deficit term, and a calibration-in-the-large term" [[260305544-yates-covariance-decomposition-rearrangement-for-brier-score-full-text]]. Equivalently, it is the criterion c of signal detection theory [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]].
- **Resolution relative to an internal reference.** This is a difference of Murphy resolutions across readouts: Ghosh et al. report behavioral 0.06371 against verbal 0.03160 [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]. It is also the grouping term of Charpentier and Fernandes Machado, the information lost in mapping features to score, which post-hoc recalibration cannot fix [[decomposing-probabilistic-scores-reliability-information-loss-and-uncertaintysup]].
- **Cross-format noise.** Ghosh reports it as cross-format Spearman of 0.126, -0.069, and 0.247 [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]. Mahaut et al. report it as AUPRC spread under paraphrase. They also already conclude that "trained hidden-state probes provide the most reliable confidence estimates" [[factual-confidence-of-llms-on-reliability-and-robustness-of-current-estimators]].

The decisive problem is circularity [[interim-report-f-metrology-residual-quantity]]. On code the "internal reference" is a probe trained on the same execution labels it is meant to referee. Any quantity defined relative to internal state therefore collapses to a contrast of two ordinary resolutions, or to a conditional mutual information. Both are functions of distributions the decompositions already cover.

### B. The vocabulary is used, and meta-d' does not apply

The vocabulary is already in use. "Measurement validity" appears in Ghosh. "SDT is applied here as a measurement framework" appears in the signal-detection study [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]]. Psychometric meta-d' framing appears in Servajean and Servajean [[measuring-some-aspects-of-the-metacognition-of-ai]]. A model-free meta-I appears in Cacioli, whose v3 retracts M-ratio "because the meta-d' efficiency ratio is not well defined for open-ended QA" [[do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec]]. "Instrument" itself appears in a reactivity argument: the rating question "displace[s] the probed state" [[dont-ask-understanding-what-numeric-self-reports-measure-in-language-models]]. Ji-An et al. run a literal reference-and-readout paradigm, in which models report their own activation directions within a low-dimensional "metacognitive space" [[language-models-are-capable-of-metacognitive-monitoring-and-control-of-their-int]].

Only metrology-proper terms (GUM uncertainty budgets, traceability) are unused for LLM confidence. The two formal metrology papers treat classifiers, and one explicitly excludes generative ML [[a-metrological-framework-for-uncertainty-evaluation-in-machine-learning-classifi]] [[uncertainty-evaluation-bridging-machine-learning-and-measurement-science-full-te]].

### C. Committed reading for F

F is a relabeling. Its quantities are Yates, Murphy, grouping-loss, and meta-I terms, and its vocabulary is in use. meta-d' is undefined for open-ended code generation, so F "differs from" it only by not applying. F fails pivot criterion 3 on both counts. Use its words for exposition and claim nothing for it.

## 7. Close occupants

The breadth matrices are in the dossiers. This section states, for each occupant on this draft's list, what it takes away. Status tags follow A23.

| Occupant | Status | What it occupies | What it leaves |
|---|---|---|---|
| Ribeiro et al., ICSE 2026 [[on-llms-internal-representation-of-code-correctness]] | published | Probe over likelihood and two verbal formats, four 7-8B instruct models, HumanEval and BigCodeBench, within task (Sec 4.2.1) | Calibration metrics, sampling family, base, reasoning, self-generated incorrect class in RQ1 |
| Ribeiro follow-up 2608.08266 [[on-the-robustness-of-llms-internal-representation-of-code-correctness]] | concurrent | Probe robustness across construction, framing, and location; "no single configuration is best" | Any new readout contrast |
| Campos et al. 2611.07876 [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] | concurrent (5 Nov 2026) | Four families including probe and causal; pooled versus within-problem AUROC; prompt-only probe control; reasoning-on check (Sec VI-C, Table V, Sec VIII) | Verbal numeric, base and instruct, trained own-readout, ECE |
| NeuroSym-Cal [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]] | published, Findings ACL 2026 | Token, P(True), self-verification, sampling, multicalibration; per-model post-cutoff LiveCodeBench; unbiased ECE, AUROC, AURC (Sec 4.1, 5.1) | Probe family; base, toggle, format |
| Tuerlings and Valdenegro-Toro [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]] | published workshop | Verbal formats on code, shared post-cutoff window, frozen code (Sec 3.1, 3.3, Table 1) | Non-verbal families, per-model split |
| Rathnasuriya and Yang 2610.11300 [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]] | concurrent | 23 token and sampling scores; base and instruct on two pairs; recalibration with BSS near 0.001 (Sec 5.5, Table 5) | Verbal, probe |
| Gros and Devanbu 2512.24560 [[localized-calibrated-uncertainty-in-code-language-models]] | preprint | Line and token localization across four families with execution-verified patches (Tables 3-4) | Test-group unit, repair arm, own-model probes |
| CodeRefuser 2605.17029 [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]] | concurrent | Risk-controlled abstention on code (Table 1) | Budget routing, verbal, probe |
| Heteroskedastic signals 2606.15841 [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]] | concurrent | Random, threshold, and oracle routing on MBPP (Table 1) | Elicited gate, clean labels |
| Give Up 2611.06372 [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]] | concurrent | Allocation theory with oracle and round-robin on CodeContests | Elicited confidence |
| SWE-Verifier 2610.30284 [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]] | concurrent | Trained step gate for agents (Table 1) | Random arm, calibration |
| Probe-SD 2609.33290 [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]] | preprint (non-code) | Trained verbal closes most of the probe gap in AUROC; recalibration does not (Table 2) | Code, execution labels |
| RLCR 2507.16806 [[beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty-2]] | preprint (non-code) | Proper-score RL for stated confidence; trained verbal at or above probe (Table 1) | Code |
| Miao and Ungar 2603.25052 [[closing-the-confidence-faithfulness-gap-in-large-language-models]] | preprint (non-code) | Gap present in base models; steering; reasoning contamination | Code, AUROC |
| Ghosh et al. 2610.25846 [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]] | concurrent (non-code) | Three-channel audit, Murphy resolution, format instability, base verbal degeneracy | Code |

Ribeiro's close citers each take one more slice:

- **2611.07876 (Campos et al.):** the within-problem collapse.
- **2608.08266:** probe fragility.
- **2606.14530:** a pre-generation probe on one model, with leakage-free AUC 0.881 falling to 0.842 after residualizing on prompt length, against a 0.657 length-only baseline [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].
- **2607.05188:** step-level agent probes [[260705188-latent-programming-horizons-in-coding-agents-full-text]].

None of the four adds verbal numeric confidence. Every one adds evidence that the probe signal on code is real, fragile, and mostly problem-level, which is the contrarian thesis.

## 8. Verdict table

"Working" is the orchestrator's working verdict. "Strict" is this draft's reading under A21 and A14. Locations come from fetched full texts or dossiers. ABSTRACT-ONLY marks the one vault record without a body; its verdict rests on the dossier's PDF read.

| Cand. | Component | Working | Strict | Evidence location | Gaps |
|---|---|---|---|---|---|
| L1 | Q1 four families on execution labels | OCCUPIED (union) | OCCUPIED (union) | NeuroSym-Cal Sec 4.2 (vault ABSTRACT-ONLY, dossier full text); Campos Sec IV, Table II; Siddiq Sec IV-A3 | none needed |
| L1 | Q2 breadth (3+ families, 2+ scales, 3+ benchmarks) | NARROW | OCCUPIED (union) | NeuroSym-Cal Sec 4.1; Rathnasuriya Table 3 | none needed |
| L1 | Q3 release split for calibration | NARROW | OCCUPIED | NeuroSym-Cal Sec 4.1; Tuerlings Sec 3.1 | none needed |
| L1 | Q4 label independence | NARROW | OCCUPIED (principle, SQL to code is a benchmark change) | Liu 2609.25938 Sec 1; Tuerlings Sec 3.3 | G-FT |
| L1 | Q5 estimator changes ranking | NARROW | OCCUPIED (substance); CLEAN (provisional) for ECE variants | Tuerlings Table 1, Sec 4.6 | G-FT, G-OA, G-S2 |
| L1 | Q6 recalibration control | OCCUPIED / NARROW | OCCUPIED | Rathnasuriya Sec 6.1, Table 5; Probe-SD Table 2 | none needed |
| L1 | Q7, Q8 test-free agreement, execution-clustered entropy | OCCUPIED | OCCUPIED | CodeRefuser Sec 3; dossiers 2502.11620, 2605.28500 | none |
| L1 | Q10 test insufficiency changes rankings | CLEAN (provisional) | CLEAN (provisional), direction predicted | Selective generation Sec 5.2.2; Liu 16 of 16 | G-FT, G-OA, G-S2, G-AX |
| L1 | Q11 multicalibration | OCCUPIED / NARROW | OCCUPIED | Multicalibration Table 1 (dossier 2512.08810) | none needed |
| L1 | Q12 judge or self-judgment | OCCUPIED | OCCUPIED | NeuroSym-Cal self-verification; Campos Yes/No judge | none |
| L1 | Q13 contamination changes calibration | CLEAN (provisional) | CLEAN (provisional) | none fetched | G-FT, G-OA, G-S2, G-AX |
| L2 | Q1 uncontrolled probe versus readouts | OCCUPIED | OCCUPIED | Ribeiro Sec 4.2.1; Gros and Devanbu Table 4 | none needed |
| L2 | Q1c controlled, within problem | NARROW | OCCUPIED (union) except trained arm | Campos Sec VI-C, Table V; Ribeiro Sec 4.1.1, RQ2; Miglani Table 1 (via probe-confound note) | G-FT |
| L2 | Q2a base versus instruct | NARROW | NARROW (weak; code reason token-only) | Rathnasuriya Sec 5.5; Tahimic Sec 5.5; Miao and Ungar Sec 3.1 | G-FT |
| L2 | Q2b reasoning toggle | NARROW | OCCUPIED (A21 clause 2) | Campos Sec VIII; Probe-SD Table 1; Hidden-error Table 2 | G-FT, G-AX |
| L2 | Q3 elicitation format | OCCUPIED / NARROW | OCCUPIED | Tuerlings Table 1; Ghosh Sec 5 | none needed |
| L2 | Q4 where the gap arises | NARROW | NARROW (weak) | Miao and Ungar; Rathnasuriya Sec 5.5 | G-FT |
| L2 | Q5, Q6, Q7 probes, transfer, other white-box | OCCUPIED | OCCUPIED | Campos; 2608.08266; Tahimic | none |
| L2 | Q8 post-training stages | NARROW (weak) | OCCUPIED by analogy | Post-training Table 1 (math); GPT-4 Fig 8 | G-FT |
| L2 | Q9 reasoning and stated confidence on code | NARROW / CLEAN (provisional) | NARROW / CLEAN (provisional) | Campos Sec VIII; Barkan (via L2 note) | G-FT, G-OA, G-S2, G-AX |
| L2 | Q11 trained stated confidence on code | CLEAN (provisional) | CLEAN (provisional), strong NLP prior that it closes | Probe-SD Table 2; RLCR Table 1 | G-FT, G-OA, G-S2, G-AX |
| L2 | Q12 causal intervention on stated confidence | NARROW | NARROW (location claim unsupported by correlational design) | Tahimic Sec 5; Wired Abstract; Miao and Ungar Table 4 | G-FT |
| L2 | Q13 pooled versus within problem | NARROW | OCCUPIED (union) | Campos Sec IV and VI-C; Disentangling Abstract | none needed |
| L3 | Q1, Q4, Q5 routing versus random and oracle | NARROW | OCCUPIED (union) | Heteroskedastic Table 1; Give Up Abstract, Table 1; Campos Sec VII | G-FCS |
| L3 | Q2, Q7 update after shown failing test | CLEAN (provisional) | CLEAN (provisional) | none fetched; nearest Kaddour Sec 2.2.1 | G-FT, G-OA, G-S2, G-AX, G-FCS |
| L3 | Q3 selective prediction | OCCUPIED | OCCUPIED | CodeRefuser Table 1 | none |
| L3 | Q6 repository agents | OCCUPIED (union) | OCCUPIED (union) | SWE-Verifier Table 1; Continue or Restart Abstract | none |
| L4 | Q4 line, token, edit, step | OCCUPIED | OCCUPIED | Gros and Devanbu Tables 3-4; FLARE Table 4; 2607.05188 Sec 4.1 | none |
| L4 | Q1 per-test-group localization | NARROW | NARROW (no evidence in hand) | Gros and Devanbu Sec 3 | G-FT, G-S2, G-FCS |
| L4 | Q2 targeted repair versus regeneration | NARROW | OCCUPIED (union) | FLARE; Olausson Sec 4; Iscan | G-FT |
| L4 | Q3 test adequacy versus own confidence | CLEAN (provisional) | CLEAN (provisional) | none fetched | G-FT, G-S2, G-FCS |
| F | Q1 vocabulary | OCCUPIED / CLEAN (provisional) | OCCUPIED (metrology-proper terms CLEAN (provisional)) | Ghosh; SDT; Servajean | G-FT, G-OA, G-S2 |
| F | Q2 decomposition | OCCUPIED (union) | OCCUPIED (union) | Vieira Sec 1.3; Charpentier Thm 2.1-2.6; Ghosh Sec 6 | none |
| F | Q3 A24 residual quantity | OCCUPIED | OCCUPIED | Mahaut robustness section; Ghosh Gate 2 | none |
| F | Q4 meta-d' | OCCUPIED | OCCUPIED (undefined for code) | Cacioli v3 abstract; Servajean | none |

**Whole-candidate verdicts:**

| Candidate | Working | Strict |
|---|---|---|
| L1 | OCCUPIED (union); protocol NARROW | OCCUPIED (union); two CLEAN (provisional) cells |
| L2 | NARROW, conditional on the controlled headline | OCCUPIED (union) except the trained-readout arm, whose likely outcome triggers A14 |
| L3 | NARROW | OCCUPIED (union); one CLEAN (provisional) cell |
| L4 | NARROW | OCCUPIED (union); NARROW only on an unevidenced unit |
| F | OCCUPIED | OCCUPIED |

The verdicts that rest on concurrent works (Campos, 2608.08266, 2610.11300, CodeRefuser, Heteroskedastic, Give Up, SWE-Verifier, Ghosh) would soften if the operator ruled concurrent works out of scope. TMLR's novelty rule refers to "existing published work," so concurrent preprints do not formally bar a novelty claim. A reviewer who has read Campos, however, will judge the controlled test against it regardless of its status.

## 9. Ranked recommendation for TMLR

TMLR has two acceptance criteria:

1. Claims are supported by accurate, convincing, and clear evidence. This is "the most important criterion," and it explicitly allows authors to "adjust (reduce) their claims."
2. At least some of the audience would be interested, and reviewers are told not to penalize modest significance or lack of novelty.

The editorial policy adds two grounds for rejection: incorrect novelty claims, and re-implementing an idea that has already been reproduced. Read together, these rules favor a paper whose claims are small, exact, and verified over one whose claims are novel and fragile. That is the only reason the occupied verdicts above do not end the project.

### Rank 1: a claims-reduced controls paper on one generation set (L2 controlled test with an L1 measurement layer)

**Contribution sentence.** On self-generated, execution-labeled code, we compare hidden-state probes, a supervision-matched own-readout, zero-shot verbal confidence, token probability, per-candidate sampling agreement, and input-only baselines on identical samples. We score them pooled and within problem, under original and augmented tests. We report how much of the published probe advantage survives these controls.

**What it offers once claims are reduced.** It offers one table nobody has published. The parts are occupied separately, but no fetched work puts a verbal numeric readout and a trained own-readout beside a probe and an input-only baseline within problem on code [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]. The likely finding is that within-problem differences sit within a few hundredths of AUROC. That would correct how Ribeiro's and similar headlines are read [[on-llms-internal-representation-of-code-correctness]] [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. Some of the audience would be interested, namely anyone using pooled AUROC on code, as the agent literature's 99.93% cross-unit result shows [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]].

**Evidence needs.** Execution labels for every sample, from a fresh pipeline (no legacy numbers). At least 100 mixed-outcome problems. A problem-clustered paired bootstrap. Validation-based checkpoint selection for every fitted reader. An isotonic-verbal control. A trained verbal or logit-feature head on the same labels.

**Main risk.** The null may read as uninteresting, and the trained arm may close the gap and trigger A14. Mitigation: frame the trained arm's result as the finding either way. If it closes the gap, the code result matches Probe-SD [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]]. If it does not, the code result contradicts it.

### Rank 2: label-oracle and estimator sensitivity as the measurement layer (L1 Q10 and Q5)

**Contribution sentence.** The ranking of four confidence families changes, or does not, when HumanEval and MBPP labels are replaced by their augmented-test versions and when the estimator moves from equal-width ECE to Brier skill and AUROC.

**Fit.** It is cheap, factual, and CLEAN (provisional) on its core cell. It rests on Liu et al.'s mechanism and Tuerlings' metric decoupling [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]] [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]].

**Risk.** Its direction is predicted, and it is a section of rank 1, not a paper.

### Rank 3: routing replay and update-after-failure as hedged secondary analyses (L3)

**Contribution sentence.** On the same generations, an offline replay of routing against random and label-sorted oracle arms at matched budgets, stratified by pass rate. A paired experiment then tests whether stated confidence moves after a genuine, spurious, or placebo failing test.

**Fit.** The replay will likely reproduce Give Up's hard-stratum failure [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]]. The update test is the most original cell in the audit, but it is CLEAN (provisional) only [[interim-report-l3-confidence-routed-execution-and-update-after-failure]].

**Risk.** Novelty claims on the update test must be hedged, and the routing replay adds utility without adding a claim.

### Rank 4: L4 per-test-group confidence

Keep it out. Line-level localization is occupied, targeted repair is OCCUPIED (union), and the test-group pipeline has no runs [[interim-report-l4-localization-occupancy-and-targeted-repair]].

### Rank 5: F

Use it as exposition only. It is a relabeling of Yates, Murphy, and grouping-loss terms [[interim-report-f-metrology-residual-quantity]].

### What would overturn this ranking

- A within-problem probe margin above 0.05 with a confidence interval excluding zero, in a pilot of rank 1. That would revive "locating the disconnect" as a positive spine.
- A trained own-readout that still trails the probe by at least 0.08 within-problem AUROC. That would make the A14 contradiction the headline.
- A working full-text search that turns up no occupant for the update-after-failure test. That would raise rank 3.

### Forward-looking implications

The literature's direction of travel predicts more occupancy, not less. Campos, Hard Issue, Disentangling, and Continue or Restart all landed within weeks of the run. Each is converging on the same correction: correctness signals on code mostly predict problems, not candidates [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]] [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]]. Within a review cycle, a within-problem verbal comparison on code is likely to appear as a section of someone else's paper.

The training-side literature is also moving from calibrating the verbal channel toward discrimination: Probe-SD's AUROC gains, and RLCR's proof that proper-score rewards yield calibrated models [[beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty-2]]. The first code paper to train stated confidence on execution labels will then occupy Q11 and probably close the gap. A paper begun now should therefore be designed to stay correct under both events. It should claim what it measured, report within-problem numbers beside pooled ones, and include the trained arm, so a later paper cannot invalidate it, only extend it. That is the strongest version of a claims-reduced paper. Its durability comes from controls, not from a gap that may close.

## 10. Instrument gaps

| Gap | What failed | Verdicts it weakens |
|---|---|---|
| G-FT | arXiv full-text search: `searchtype=ft` ignored; the full-text host is off the allowlist | Every CLEAN (provisional) cell: L1 Q10, Q13, Q5 sub-part; L2 Q9 sub-part, Q11; L3 Q2 and Q7; L4 Q3; F Q1 metrology-proper terms |
| G-OA | OpenAlex full text partial (1 of 2 positives); daily budget exhausted about 05:05 IST | The same cells; every later OpenAlex negative |
| G-S2 | Semantic Scholar keyword search HTTP 429 throughout | Keyword recall for all candidates |
| G-AX | arXiv export API HTTP 429 to several queries | Metadata recall in the L2, L3, and L4 investigations [[interim-report-l3-confidence-routed-execution-and-update-after-failure]] [[interim-report-l4-localization-occupancy-and-targeted-repair]] |
| G-OR | OpenReview forum pages and PDFs behind a browser challenge | OpenReview-only full texts |
| G-FCS | Forward screens partial: 2611.06372, 2610.30284, and 2608.14659 citers not screened; only four citers of 2512.24560 | L3 update cell, L4 Q1 and Q3 |

**Record-level gaps that bear on cited evidence:**

- The NeuroSym-Cal vault record is ABSTRACT-ONLY. Its section citations come from the dossier's PDF read, which also corrects the vault summary: the final method is self-verification, not latent perturbation [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]].
- Campos Table II was garbled in extraction. The within-problem numbers cited here come from Sec VI-C, Table V, and Sec VIII text [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].
- Miglani et al.'s confidence intervals for 0.677 against 0.703 are not reported in the sections read [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].
- The Hard Issue record ends after Section III [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]].
- The Tian et al. record under the cited ID resolved only by file path, because of an index collision [[just-ask-for-calibration-strategies-for-eliciting-calibrated-confidence-scores-f-3]].

**The contrarian reading of the gaps.** The brief treats gaps as reasons a CLEAN verdict must stay provisional. This draft adds the converse: the observed arrival rate (27 of 75 dossiered occupants concurrent, and nine with October or November 2026 identifiers) makes it more likely than not that a working full-text search would find at least one further occupant of a provisional cell. That is a judgment from the arrival rate, not a measured probability. Novelty claims on any provisional cell should therefore be phrased as "we found no prior report," with the instruments named.
