# Confidence estimation for code language models against execution ground truth: occupancy, residuals, and the strongest TMLR contribution (draft a)

**Executive summary.** The headline that a hidden-state probe beats the model's own stated confidence on code is taken. Ribeiro, Spiess, Devanbu, and Nadi (ICSE 2026) show it at whole-solution granularity for four 7-8B instruct models, with probe gains of +13.3 to +29.0 points on BigCodeBench and +8.7 to +26.2 points on HumanEval over the best reflective readout (Section 4.2.1) [[on-llms-internal-representation-of-code-correctness]]. A paper that leads with "probes beat verbal confidence on code" would claim novelty incorrectly, and TMLR's editorial policy lists that as a reason to reject. What is not taken is the controlled version of that claim, and the evidence says the controlled version is the more interesting one. Every code comparison that scores a probe against the model's own confidence within the same problem, on self-generated samples, finds a tie: 0.620 versus 0.629 for Qwen3-Coder [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]], and 0.677 versus 0.703 for Qwen2.5-Coder [[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]]. No code study gives the stated-confidence channel the same execution labels that the probe was fitted on.

The strongest defensible TMLR contribution is therefore a single execution-graded measurement paper. Its headline is a supervision-matched, within-problem test: probe versus the model's own readouts (zero-shot verbal, trained verbal or logit-feature head, token probability, and per-candidate sampling agreement), with prompt-only and code-text-only baselines, scored pooled and within problem on the model's own samples. The test is built on an L1 sensitivity protocol: an estimator set, a swap from the original to the augmented-test oracle, and a per-model release-date split with a pre-cutoff comparison group. An offline L3 routing replay, with random and label-sorted oracle arms at matched budget, is a secondary analysis on the same generations. The base-versus-instruct and reasoning-toggle decompositions become a conditional extension, run only if the controlled gap is measurably non-zero. L4 stays out. F supplies vocabulary and nothing else. The design is publishable whichever way the headline comes out. A null controlled gap would correct the field's reading of the probe literature, which fits TMLR's first and most important criterion. A surviving gap would be the first clean evidence that code models hold correctness information they do not express.

Verdicts in brief:

- **L1:** OCCUPIED (union) as a comparison; NARROW as a protocol, with test insufficiency and contamination effects on calibration CLEAN (provisional).
- **L2:** OCCUPIED as an uncontrolled headline; NARROW as the controlled test and as the factorial decomposition.
- **L3:** NARROW for routing by elicited confidence; CLEAN (provisional) for confidence updating after a shown failing test.
- **L4:** NARROW, with line-level localization OCCUPIED.
- **F:** OCCUPIED.

## 1. Scope, instruments, and verdict rules

### 1.1 What is being judged

The question covers 2022 to November 2026 and asks which confidence-estimation contribution for code language models, graded by execution, is still open and defensible at TMLR. It names five candidates. L1 is a measurement foundation with release-date contamination control. L2 locates the disconnect between internal state and output. L3 is verification utility and confidence updating. L4 is per-requirement confidence and localization. F is a measurement-instrument framing. Each candidate and each component gets a verdict under the brief's definitions:

- **OCCUPIED:** a fetched work makes the core claim with comparable breadth on every dimension the claim names.
- **OCCUPIED (union):** at most three fetched works together cover every dimension, and the only remaining step is running them on the same problems.
- **NARROW:** a precisely stated residual remains. The residual must be a factor, granularity, label protocol, or use, not just a change of models or benchmarks. There must also be a stated reason the code result could differ from the closest general-NLP result.
- **CLEAN:** the search conditions are met and nothing relevant was found.
- **CLEAN (provisional):** the CLEAN conditions hold except for an instrument gap that bears on the claim.

General-NLP work counts only as the comparison side of a residual for L2 and F. Pre-2022 metric works are foundations, not occupants.

### 1.2 The two TMLR criteria, read as design constraints

TMLR's rubric asks two questions. Are the claims supported by accurate, convincing, and clear evidence? This is "the most important criterion", and authors may meet it by reducing their claims. Would at least some of the TMLR audience be interested? Reviewers are told not to penalize modest significance or lack of novelty. The editorial policy rejects papers that "incorrectly claim novelty over existing published work." This draft reads those rules as an engineering specification. The winning contribution needs three properties:

- a claim whose evidence the paper generates itself;
- a framing that is honest about Ribeiro and the concurrent citers;
- a result that is informative whether it comes out positive or null.

TMLR's tolerance for modest novelty makes this easier. Its intolerance for overclaimed novelty makes the uncontrolled L2 headline a liability.

### 1.3 Instruments and how they cap verdicts

The run's instrument record caps every CLEAN at CLEAN (provisional). arXiv full-text search failed validation: `searchtype=ft` is silently ignored, and the full-text host is off the allowlist. OpenAlex full-text search found one of two known positives, and its daily budget ran out at about 05:05 IST. Semantic Scholar keyword search returned HTTP 429 on all ten attempts. The arXiv export API returned HTTP 429 to several later queries. OpenReview forum pages and PDFs sit behind a browser challenge. Section 10 lists these gaps and the verdicts each one weakens. Verdicts below rest on full texts read in the vault, cited by section or table. ABSTRACT-ONLY marks the one load-bearing case where the vault copy is an abstract: NeuroSym-Cal [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]], whose section-level facts come from the run's full-text dossier, not the vault note.

### 1.4 Concurrency

The proposed six-month concurrency window starts 2026-05-10. Several verdict-bearing works fall inside it:

- Campos, Klassert, and Ulges, 2611.07876, posted 5 November 2026;
- Rathnasuriya and Yang, 2610.11300;
- Liu et al., 2609.25938;
- Miglani et al., 2609.36783;
- Bulut, 2609.03436;
- SWE-Verifier, 2610.30284;
- Give-Up, 2611.06372;
- Code-MUE, 2607.12273.

This draft treats them as occupants. A reviewer will read them whether or not the operator rules them out of scope. A positioning that only works if concurrent preprints are ignored is not defensible.

## 2. L1: Execution-graded measurement foundation

### 2.1 Occupancy questions and the comparison itself

L1's core claim is that comparing four confidence families against execution labels shows which methods track correctness on code. The four families are sampling agreement, token probability, stated confidence, and hidden-state probes. The comparison should span three or more model families, two or more scales, and three or more benchmarks, with a release-date control. As a comparison, this claim is occupied by union.

NeuroSym-Cal (Findings of ACL 2026) covers token probability (AvgLogit, Platt), verbal P(True) and self-verification, sampling agreement (self-consistency and AST consensus over K=10 samples), and a multicalibration baseline (IGLB). It runs on DeepSeek-R1-Distill-Llama-70B, Qwen2.5-Coder-32B-Instruct, and Llama-3.3-70B-Instruct. Its benchmarks are LiveCodeBench v2406 to v2506 (400 problems), HumanEval-Pro, and DS-1000 (Sections 3, 4.1, 4.2 per the full-text dossier; vault note ABSTRACT-ONLY) [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]]. It reports ECE 0.072 versus 0.115 for self-consistency on DeepSeek-R1, and LiveCodeBench AUROC 0.805 versus 0.798 for IGLB (Section 5.1). It has no probe. Campos et al. 2611.07876 has the probe. It covers Yes/No token probability, EigenScore sampling, a linear probe, LAT, and two causal (DAS-based) predictors on Qwen3-Coder-30B and gpt-oss-20b, under benchmark and language shift (Sections III to VI) [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. It has no numeric verbal readout. Between them, the two papers touch all four families on different problems: the union case.

Breadth occupants fill in the rest:

- **Code-MUE:** eight models and four benchmarks, but a single execution-agreement family [[code-mue-measuring-code-llms-uncertainty-through-execution-based-semantic-intera]].
- **Functional Entropy:** five closed models over LiveCodeBench, MultiPL-E Java, and LiveSQLBench, with token, sampling, and reflexive scorers (Section 4.1, Table 1) [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]].
- **Rathnasuriya and Yang:** seventeen generation-stage and six prefill-stage token and sampling metrics on four instruct models (Section 4, Table 3) [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]].

The committed reading is that nobody needs another code-confidence leaderboard. A paper whose claim is "we compared the four families" re-implements a union that three fetched works already span. It would also have to beat NeuroSym-Cal's breadth on the families it shares.

### 2.2 What is not occupied: the instrument under the comparison

The open territory is whether these rankings survive changes to the measuring instrument. Three controls matter, and each nearest occupant holds exactly one of them.

**Estimator.** Tuerlings and Valdenegro-Toro (UncertaiNLP 2026) is the only code study that shows a method ranking change by metric. In Table 1, the lowest ECE (0.013, CodeLlama-7B Linguistic) comes with AUROC 0.491. The highest AUROC (0.841, Qwen-32B Linguistic) comes with ECE 0.216. The paper states that "ECE and AUROC measure different properties and do not correlate across cells." Eight of 18 cells collapsed (Section 4.6) [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]. But it uses ten equal-width bins (Section 3.5). No code study compares equal-mass, debiased, smooth, or kernel estimators. Gros and Devanbu flag ECE as "misleadingly low" under bucket collapse and prefer Brier skill [[localized-calibrated-uncertainty-in-code-language-models]]. Campos, Kuschnereit, and Ulges report binned ECE and Brier skill for token likelihood only [[multicalibration-for-llm-based-code-generation]].

**Label oracle.** Liu et al. hold the oracle-swap result, in text-to-SQL. Swapping the shipped database for a multi-instance test suite raises conformal held-out risk by 2.73 to 10.23 points. "Every execution-consistency score looks better under the labels of the oracle that built its clusters, in 16 of 16 combinations." Under expert labels, a certificate at nominal 0.10 carries 20.0 and 17.2 points of risk [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]]. EvalPlus showed that 80 times more tests cut pass@k by 19.3% to 28.9% across 26 models, and that "test insufficiency can lead to mis-ranking" of models [[is-your-code-generated-by-chatgpt-really-correct-rigorous-evaluation-of-large-la]]. Nobody has recomputed a confidence-method ranking under original versus augmented tests on code.

**Contamination.** NeuroSym-Cal holds out a per-model post-cutoff LiveCodeBench subset (Section 4.1, dossier). Tuerlings uses one shared post-cutoff window, 2024-09-19 to 2025-04-30, for the verbal family only (Section 3.1). Campos, Kuschnereit, and Ulges take LiveCodeBench release_v6 (1,055 problems, May 2023 to April 2025) as a whole-benchmark leakage control [[multicalibration-for-llm-based-code-generation]]. The Klassert thesis says it "prioritizes ... over strict contamination control" (Section 4.1) [[abstract]]. Lugoloobi et al. use release-date splits for pre-generation probes, but to predict accuracy, not to contrast calibration [[llms-encode-their-failures-predicting-success-from-pre-generation-activations]]. No fetched work compares calibration or discrimination on pre-cutoff versus post-cutoff problems. A held-out window is a hygiene step. A contrast is a measurement.

### 2.3 Label independence is a live defect, not a formality

The label-independence question sounds pedantic until you see where it fails in print. Code-MUE's AUROC label "Solved" means at least one of the N sampled candidates passes all tests. The label is therefore computed from the same samples whose agreement the method scores (Section 5.2.1, per its dossier) [[code-mue-measuring-code-llms-uncertainty-through-execution-based-semantic-intera]]. Liu et al.'s 16-of-16 result is the general mechanism: a consistency score built from an oracle's tests flatters itself under that oracle's labels [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]]. Good practice does exist:

- Tuerlings freezes code before elicitation, "so ... correctness labels are determined independently of any confidence estimation" (Section 3.3) [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]].
- Code Is More Than Text keeps self-generated tests apart from the official label suite, "since otherwise the functional signal would be trivially perfect by construction" [[code-is-more-than-text-uncertainty-estimation-for-code-generation]].

Neither tests independence as a factor. There is also a concrete reason code could differ from SQL. Benchmark tests drive both the label and every test-execution agreement score. A thin suite therefore gives false-pass labels on plausible but wrong programs, and it inflates exactly the families that correlate with test-style agreement.

### 2.4 Recalibration as a control

Rathnasuriya and Yang separate the score mapping from the information it carries. Platt and isotonic maps cut CodeLlama's Brier score from 0.459 to 0.248, while Brier skill stays at about 0.001 (Section 6.1, Table 5) [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]. Multicalibration with group features lifts LiveCodeBench Brier skill from -0.543 (uncalibrated Qwen3) to positive values [[multicalibration-for-llm-based-code-generation]]. The Klassert thesis reports a Qwen3-Coder probe at Brier skill 0.5888 versus 0.4680 for IGLB on the CALIBRI split (Table 5.7) [[abstract]]. Recalibration control is therefore occupied for token readouts. The cross-family version remains NARROW: does a monotone map leave the family ranking intact while changing the ECE ranking?

### 2.5 Committed reading on L1

L1 as a comparison is OCCUPIED (union). L1 as a protocol is NARROW and worth building, but as the measurement layer under L2, not as a standalone benchmark paper. The protocol has three controls: the estimator set, the original-versus-augmented oracle swap, and a per-model release split with a pre-cutoff contrast. The decisive reason is structural. The same instrument fragilities that could reorder an L1 leaderboard would also move every L2 and L3 number. Label flips under HumanEval+ and MBPP+ change which candidates count as discordant pairs. Collapsed verbal distributions change both ECE and within-problem AUROC. An L2 headline reported without the L1 controls invites a reviewer to ask whether it survives a stronger oracle, and the paper would have no answer. The test-insufficiency question (L1 Q10) and the contamination-effect question (Q13) are CLEAN (provisional). They are cheap to answer inside the same design, and they give the paper two findings that hold whatever the probe result. For a first submission, that insurance is worth more than any single novelty claim.

## 3. L2: Locating the disconnect between internal state and output

### 3.1 The uncontrolled headline is occupied, and it should be

Ribeiro et al. fit a Representation Engineering direction (LAT, PCA over differences of hidden states for correct and incorrect code at the last token). They use it to pick the correct implementation among four candidates. The models are Mistral-7B-Instruct-v0.3, Qwen2.5-Coder-7B-Instruct, OpenCoder-8B-Instruct, and CodeLlama-7B-Instruct, on HumanEval (151 tasks) and BigCodeBench (457 tasks) [[on-llms-internal-representation-of-code-correctness]]. The probe beats intrinsic likelihood and two verbal formats (seven-level and True/False) by the margins quoted above (Section 4.2.1). In-distribution LAT accuracy on BigCodeBench is 50.3% to 56.3%, against 27.5% random for Mistral and 23.7% to 41.1% for verbal baselines (Table 3). Campos et al. add a sampling family and AUROC, without a verbal numeric readout [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. On code, then, the probe-versus-stated-confidence-versus-likelihood comparison under execution labels exists, and its uncontrolled direction is settled. L2 Q1, uncontrolled, is OCCUPIED.

The occupant's prior art makes this firmer. Openia trained last-token, last-layer probes on DeepSeek-Coder, CodeLlama, and Magicoder, with "up to a 2X improvement in standalone code generation and a 3X enhancement in repository-specific scenarios" over baselines that include LLM-as-judge [[correctness-assessment-of-code-generated-by-large-language-models-using-internal]]. AutoProbe's attention-weighted probe reaches 0.63 to 0.71 functionality accuracy against 0.32 to 0.61 for the generator judging itself (Table 5) [[model-agnostic-correctness-assessment-for-llm-generated-code-via-dynamic-interna]]. The broader probing facets (L2 Q5 to Q7: probes for code correctness, transfer, and other white-box readouts) are OCCUPIED by these works, by Campos et al. under shift, by the SAE study [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]], by Di Cicco's pre-generation probe [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]], and by diffusion-model probes [[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]].

### 3.2 Why the occupant's margin does not answer the question it seems to answer

The occupied claim is real, but it is a fact about a supervised reader, not evidence of unexpressed knowledge. Three confounds, each documented in a fetched full text, sit between Ribeiro's numbers and the claim that the model knows more than it says.

**Difficulty.** Bulut's Equation 1 makes the diagnosis exact: AUROC_pooled = lambda times AUROC_within plus (1 minus lambda) times AUROC_between, where lambda is the share of discordant pairs from the same problem. "Every question-only predictor has AUROC_within = 1/2 exactly ... in the standard design with one attempt per problem (k_c = 1), lambda = 0." Bulut's reconstruction of a published early-window probe on MATH gives pooled AUROC 0.849 [0.735, 0.919] but within-problem 0.496 (Section 4.4) [[its-the-problem-not-the-pathbudget-and-difficulty-confounds-in-llm-reasoning-tra]]. At function-level scale, a balanced design of 164 problems with 10 samples each puts only about 0.6% of pairs within the same problem. A pooled code AUROC is therefore about 99% a between-problem number [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]. The agent literature reports more than 99.93% cross-unit pairs [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]]. On code, the effect is measured directly. Campos et al. Table V shows a probe at the last prompt token, which sees only the problem, with pooled AUROC 0.891 and within-problem 0.514. The authors' gloss: "Much of what the methods predict is thus the problem, not the candidate" [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. On LiveCodeBench, a TF-IDF classifier on prompt text recovers 0.84 to 0.86 of the 0.90 to 0.91 probe AUROC for Qwen2.5-Coder, and beats the probe for R1-Distill (Table 2, Pass@5 target; column labels read from the header) [[llms-encode-their-failures-predicting-success-from-pre-generation-activations]]. Di Cicco's 0.881 ± 0.008, or 0.842 after removing prompt length, uses one attempt per task. By Equation 1 it carries zero within-problem information [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]].

The same identity cuts against published verbal-confidence numbers. Tuerlings elicits confidence on one greedy generation per problem [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]], and Functional Entropy scores one original response per prompt [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]]. So Qwen-32B's AUROC of 0.841 and the verbal range of 0.597 to 0.795 are between-problem numbers. They measure whether the model knows which problems it fails. They say nothing about whether its stated confidence ranks its own candidates. No fetched code study reports a within-problem AUROC for numeric verbal confidence on self-generated samples. This is the single most important gap in the literature for this project.

**Supervision asymmetry.** Ribeiro fits LAT on 10% of tasks and validates on another 10% (Section 4.1.2). The verbal readouts are zero-shot. Liu, Casper, Hadfield-Menell, and Andreas named this asymmetry in 2023: "the superior calibration and accuracy of probes over queries might not seem surprising given that probes are trained many-shot while queries use the model zero-shot." When they fine-tuned the queried model, probes were "1.7% better accuracy than fine-tuned model queries on BoolQ", but queries were "6.9% and 4.0% better" on SciQ and CREAK (Section 3) [[cognitive-dissonance-why-do-language-model-outputs-disagree-with-internal-repres]]. The winner flipped on two of three datasets. On code, the only partial control is Gros and Devanbu's Platt scaling of every readout. Platt cannot change AUC, so the Qwen line-level gap (probe 0.83 versus verbalized 0.71) survives it, but no trained verbal head is present [[localized-calibrated-uncertainty-in-code-language-models]]. For GPT-4o, that paper's "probe" reads a separate 0.5B or 7B supervisor model, so it is not GPT-4o's own internal state.

**Provenance.** Ribeiro's correct class is the human reference solution. The three incorrect candidates come from other models: Llama-3.3-70B, GPT-4o, and Gemini 2.0 Flash on BigCodeBench (Section 4.1.1). The intrinsic readout picks the reference only 5% to 6% of the time on BigCodeBench against 25% chance (Section 4.2.1). So model likelihood is strongly anti-correlated with this label, and any supervised reader that learns the sign wins. The authors' own follow-up names the confound ("variable names or implementation style"). It finds that a direction fit on fault-isolating mutation pairs "does not transfer", with a 37.1-point accuracy drop on BigCodeBench versus 5.2 points on HumanEval. It also finds that "no single configuration is best, and that isolating the fault does not help" [[on-the-robustness-of-llms-internal-representation-of-code-correctness]]. Ribeiro's cleaner test, RQ2, ranks ten self-generated samples. There the gains are small: Mistral HumanEval rank-1 41.3% against 34.7% pass@1 and 35.5% for RankEF, and "Only a few comparisons reached statistical significance" [[on-llms-internal-representation-of-code-correctness]].

### 3.3 What the controlled comparisons that do exist say

Three comparisons on code score a probe against the model's own output confidence within the problem on self-generated samples. All three tie or favor the readout:

- **Miglani et al. (Section 4.2, Table 1):** DiffuCoder-7B probe 0.842 against negative token entropy 0.838 (19 mixed problems), and Qwen2.5-Coder probe 0.677 against completion log-probability 0.703 (56 mixed problems, 448 attempts). Their reading: "Model confidence is thus a competitive baseline ... Reading hidden states provides little apparent gain" [[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]].
- **Campos et al. (Section VI-C):** "under language shift, within-problem AUROC lies at 0.58-0.64 for all methods and both models ... For Qwen3-Coder confidence performs best within problem (0.629)." The probe at the last code token reaches 0.620 [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].

The one exception is gpt-oss in distribution, where trained methods reach 0.69 to 0.78 within problem, and the advantage is lost under shift. On the other side, the strongest supervision-matched evidence for a real probe edge on code comes from non-autoregressive models: a probe beats supervised logistic regression on entropy by 0.08 to 0.10 AUC on MBPP for diffusion models (Dream 0.879 versus 0.776) [[probing-functional-correctness-in-diffusion-language-models-full-text]]. That result is pooled.

Read together, the best estimate is that a probe's within-problem edge over a well-formed own-confidence readout on self-generated code is within about 0.05 AUROC, and may be zero [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]. I commit to that estimate as the paper's pre-registered hypothesis, not its conclusion. The samples are small (19 and 56 mixed problems). Miglani's confidence intervals are not reported. None of the three comparisons includes a numeric or categorical verbal readout, a trained own-readout, or per-candidate sampling agreement. Campos's EigenScore scores the problem, not the candidate, so its within-problem AUROC is 0.5 by construction.

### 3.4 The trained-readout threat, and why it is the arm that makes the paper

Pivot criterion 3 asks whether the gap closes under an elicitation method, a stated-confidence training method, or recalibration that the paper would have to include. On code it is not triggered. Outside code it is the strongest evidence that the gap closes:

- **Probe-SD:** distilling a probe into the verbal channel lifts Qwen3-14B's verbal AUROC on TriviaQA from .825 to .928 in domain, against a probe at .948. Isotonic recalibration of the verbal channel leaves AUROC at .825 (Tables 1 and 2) [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]].
- **RLCR:** on HotpotQA, trained verbal confidence reaches AUROC 0.69 against 0.55 for a final-layer probe on the RLVR model; on Big-Math, 0.67 against 0.65 (Table 1) [[beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty-2]].
- **ConfTuner:** gains of up to 14.4% in AUROC from HotpotQA training [[conftuner-training-large-language-models-to-express-their-confidence-verbally]].

The opposing evidence is just as specific. When Words Fall Short shows that estimator overfitting at a single training endpoint "can bias comparisons in favor of verbalized confidence". With validation-based checkpoint selection, a hidden-state estimator beats RL-trained verbal confidence in AUROC by 0.161 in domain and 0.078 out of domain (Section 2.2) [[when-words-fall-short-iterative-synergy-between-verbalized-reasoning-and-hidden]]. On LiveCodeBench, RLCM's probe-read confidence has ECE 0.051 against 0.218 for RLCR's verbal confidence. This is the only code instance, it reports ECE only, and the model was trained on math (Table 1) [[process-supervision-of-confidence-margin-for-calibrated-llm-reasoning]].

These two sides do not cancel. They define the experiment. General NLP does not settle whether training the stated channel closes the discrimination gap, because RLCR and When Words Fall Short disagree over the same comparison. Code adds a concrete reason the answer could differ. Execution labels let every readout be trained on exactly the same supervision as the probe, at no annotation cost. That symmetric-supervision condition is what the NLP comparisons lack, because their labels come from judges or string match. A supervision-matched arm (a trained verbal head, or a logit-feature head fit on the same execution labels) is therefore not optional. It is the arm that turns "the probe beats a zero-shot prompt" into "the information is or is not reachable by the output channel." It also pre-empts the most obvious reviewer citation.

### 3.5 Base versus instruct, reasoning, and format: residuals that are real but dependent

The factorial residuals survive the residual rule (A21), and I accept them as NARROW. On code, though, they rest on a premise the controlled test has not yet established.

**Base versus instruct.** Rathnasuriya and Yang Section 5.5 is the only code comparison of base and instruct models under execution labels, and it is token-level only. DeepSeekCoder's base confidence AUC is 0.4391, which means certainty is anti-aligned with correctness. It rises to 0.5654 after tuning (change +0.1263, CI [0.0447, 0.2089]). OpenCoder's AUC changes by -0.0136 (CI [-0.0911, 0.0652]), while failing-program confidence rises from 0.8685 to 0.9224 [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]. The SAE study finds base-trained directions persisting after instruction tuning in Gemma-2-2b (F1 0.821 to 0.772), with no verbal readout [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]]. On the NLP side, Miao and Ungar test base and instruct models and find that "base models verbalize poorly calibrated confidence despite encoding well-calibrated accuracy information internally". The accuracy and verbal-confidence directions have cosine similarity below 0.04 (Section 3.3) [[closing-the-confidence-faithfulness-gap-in-large-language-models]]. The code-specific reason is real: an anti-aligned base readout inverts the usual story that tuning corrupts a calibrated base. So base versus instruct by readout on code is NARROW.

**Reasoning.** Campos prefills gpt-oss so that it answers without reasoning. Only in a construct-validity check does reasoning raise the Yes-probability AUROC from 0.68 to 0.73, and the probe is never read under reasoning (Sections V-A and VIII) [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. Barkan et al. toggle reasoning budgets for in-advance verbal confidence on BigCodeBench and find "reasoning LLMs perform comparably to or worse than non-reasoning LLMs" [[do-large-language-models-know-what-they-are-capable-of]]. Open the Oyster compares DeepSeek-Reasoner with DeepSeek-Chat, which are different weights, on code-reasoning tasks (CCP ECE 0.066 versus 0.143, Section 5.1.1) [[open-the-oyster-empirical-evaluation-and-improvement-of-code-reasoning-confidenc]]. Outside code, Yoon et al. find reasoning models better calibrated "in 33 out of the 36 settings" [[reasoning-models-better-express-their-confidence]]. Sarfati et al. find probes ahead of verbal output in reasoning models (GLM-4.7-Flash AUROC 0.768 versus 0.669; ECE 0.054 versus 0.287, Table 1) [[what-llm-forecasters-know-but-dont-say-probing-internal-representations-for-cali]]. Zeng et al. excluded code because "most models struggled to output both code snippets and confidence simultaneously" [[thinking-out-loud-do-reasoning-models-know-when-theyre-right]]. That is a code-specific obstacle with a mechanism attached: Miao and Ungar's joint solve-and-rate prompting inverts the confidence relation from +0.26 to -0.63 (Section 3.4) [[closing-the-confidence-faithfulness-gap-in-large-language-models]]. A same-weights reasoning toggle on code, with the probe read under reasoning, is NARROW.

**Format.** Within verbal readouts on code, format is OCCUPIED. Tuerlings' three formats give Qwen-32B AUROC of 0.834, 0.810, and 0.841, and DeepSeek-6.7B 0.518, 0.716, and 0.498 (Table 1) [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]. Only the format-by-readout interaction is NARROW. It belongs in the design as a controlled nuisance factor, not as a finding.

These residuals are NARROW, but they should not be the headline. If the controlled within-problem gap is near zero, decomposing it by tuning stage and reasoning partitions noise. A decomposition presumes there is something to decompose. Only the controlled test can establish that. The factorial arms therefore go in a pre-registered conditional extension: run them if the controlled gap clears a stated margin with a confidence interval that excludes zero, and report them as exploratory otherwise. The order costs nothing if the gap is real. If it is not, it saves the paper from overclaiming.

### 3.6 Causal location

On code, causal work targets output correctness, not stated confidence. SAE steering fixes 4.04% of errors but corrupts 14.66% of correct code [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]]. Steering along Miglani's probe direction lowers pass@1 from 0.433 to 0.388 toward pass and to 0.298 toward fail [[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]]. Outside code, Kumaran et al. show by activation patching that a post-answer-newline probe is causally sufficient to rescue error detection. Within incorrect trials it reaches AUROC .986 against a best behavioral baseline of .908 [[how-llms-detect-and-correct-their-own-errors-the-role-of-internal-confidence-sig]]. Pivot criterion 4 is not triggered. Causal intervention on stated confidence for code (L2 Q12) is NARROW. I would not put it in the first paper: it multiplies the method surface without strengthening the headline.

### 3.7 Pivot criteria and committed reading on L2

- **Criterion 1 (union):** not triggered. No three works put probe, stated, and sampling readouts on the same code generations together with base and instruct pairs and a reasoning factor.
- **Criterion 2 (residual):** fails for the uncontrolled headline and survives for the controlled test and the factorial versions.
- **Criterion 3 (trained readout closes the gap):** open, and the design must include the arm that tests it.
- **Criterion 4 (causal localization on code):** not triggered.

Whole L2 is NARROW, conditional on the controlled test being the headline. The residual in one sentence: a same-sample comparison on self-generated, function-level code, under execution labels, scored pooled and within problem, of five readouts. They are a probe; a supervision-matched own readout (a verbal or logit-feature head trained on the same labels); zero-shot numeric and categorical verbal confidence; token probability; and per-candidate sampling agreement, with prompt-only and code-text-only baselines. Closest code work: Ribeiro (zero-shot verbal, provenance-confounded) and Campos (pooled versus within, no verbal, no trained own readout). Closest NLP work: Liu et al. 2023 (supervision-matched, GPT-2-XL, no execution labels) [[cognitive-dissonance-why-do-language-model-outputs-disagree-with-internal-repres]].

## 4. L3: Verification utility and confidence updating

### 4.1 Routing by elicited confidence

Every positive code result for confidence-routed compute uses a learned or proxy gate. None uses the generating model's elicited verbal confidence or its own probe:

- **Heteroskedastic Signals:** replays MBPP with a logit-margin proxy. At beta of 10% for Qwen3-8B, Random scores .551, Threshold .636, cost-stratified thresholding .671, and Oracle 1.00 (Table 1). The authors "add 10% Bernoulli label noise and Gaussian proxy noise". The oracle is the label itself, and the gain at 10% has CI [-0.2, +7.0] [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]].
- **SWE-Verifier:** gates step sampling with a trained Qwen3.5-4B scorer. MiniMax-M2.7 goes from 75.47 to 77.20 at 1.09x cost. Its "Oracle@3" (82.20 at 3.00x) is best-of-three rollouts, not a routing oracle, and no random gate at a matched rate is reported (Tables 1 and 2) [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]].
- **SWE-Router:** uses a trained 7B value head and reports Route-AUC 0.780, +15.3 points over a non-temporal baseline, with a curve above a random-assignment band. It has no oracle arm, and it routes between models, not execution budgets (Section 5.3) [[swe-router-routing-in-multi-turn-agentic-software-engineering-tasks]].

The negatives use other budget units. Give-Up shows that difficulty-proportional rules capture "at most 13%" of oracle gain on hard workloads even with true pass rates. On CodeContests (Llama-3-8B, mean p 0.021), the best rule captures 1%. A history prior must reach a rank correlation of about 0.3 to 0.55 before Thompson sampling beats round-robin, and LLM-derived priors give Spearman 0.10 to 0.46 (Tables 1 and 3) [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]]. Uncertainty-triggered regeneration lowers pass@1 in five of six configurations [[1introduction]].

The residual is a gate built from the code model's elicited verbal or probe confidence, under unmodified execution labels, with matched-budget random and label-sorted oracle arms. It is NARROW. The code reason is Give-Up's: pass rates on hard code are very low, which is the regime where difficulty-based rules fail, so a code result can differ from math. Selective prediction with coverage control on code is OCCUPIED by CodeRefuser. Its Learn-Then-Test abstention at alpha 0.2 on MBPP with Qwen2.5-Coder-32B abstains on about 30% of tasks against more than 80% for perplexity (Table 1, Figures 2 and 3) [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]. Repository-agent uncertainty is OCCUPIED (union) at the step and trajectory unit.

### 4.2 Updating after a shown failing test

No fetched record measures stated confidence before and after the model sees a failing test on its own program, tied to the repair outcome, with a contrast between valid and spurious failures. The nearest works miss the condition in instructive ways:

- **Kaddour et al.:** mid-execution confidence drops in an "uninformative" way. But the agent "cannot execute code, run tests" (Section 2.2.1), so no failure is ever observed [[agentic-uncertainty-reveals-agentic-overconfidence]].
- **Barkan et al.:** confidence is updated after outcomes of earlier contracts, not test failures on the same code [[do-large-language-models-know-what-they-are-capable-of]].
- **Iscan:** feedback content is decomposed with a placebo arm, but confidence is never elicited [[falsification-not-exposure-placebo-controlled-decomposition-of-self-repair-feedb]].

This component is CLEAN (provisional). The gaps bear on it directly: a one-paragraph experiment inside an agent paper would not show up in title and abstract search.

### 4.3 Committed reading on L3

L3 is NARROW and belongs in the paper as a secondary analysis, because it costs almost nothing once L1 and L2 generations exist. The design is an offline replay at budgets of 10%, 20%, 30%, and 50%, with at least ten seeds, a paired gain with a 95% CI, stratification by mean pass rate (below 0.1 versus above 0.4), and unmodified labels. The L2 headline also sets an upper bound on the L3 result. If within-problem AUROC is 0.6 to 0.7 at best, a within-problem gate can gain little, and Give-Up predicts that the hard stratum fails for every gate. A replay that confirms this is still a finding, and an honest one. The update-after-failure probe is the most novel-looking component on paper, but it is CLEAN only provisionally. It also needs a new elicitation protocol: genuine, spurious, and placebo failures. I would include it as a small, hedged experiment only if it fits the compute budget, and never as the headline.

## 5. L4: Per-requirement confidence and localization

Gros and Devanbu occupy line-level and token-level localization. Their labels come from "Minimal Intent Aligning Patches" verified by hidden tests. They compare token probability, probes, multisampling, and line-level verbalized confidence on GPT-4o and Qwen2.5-Coder-7B-Instruct across HumanEval+, MBPP+, LiveCodeBench, and RepoCod. For Qwen at line level, Probe-7B has Brier skill 0.29 against -0.72 for line-verbalized confidence (Tables 3 and 4) [[localized-calibrated-uncertainty-in-code-language-models]]. FLARE covers localization feeding repair: 67% Top-1 localization and gains of 1.72% to 7.42% over NL-Debugging, with no matched resampling arm (Table 4) [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement-2]]. Step-level agent probes decode "partial correctness: the number of failing tests is strictly less than at the beginning" with AUC up to 0.84 [[260705188-latent-programming-horizons-in-coding-agents-full-text]].

Per-test-group confidence as localization of the failing requirement is NARROW. The residual is that requirement units are specification-level and need no patch oracle. Targeted repair versus regeneration is NARROW. The matched-budget literature says repair is not a free win: "pass rates are higher or equally high with i.i.d. sampling (without repair), especially when the budget is small" [[is-self-repair-a-silver-bullet-for-code-generation]], and blind resampling beat bare retry by 18 net unlocks [[falsification-not-exposure-placebo-controlled-decomposition-of-self-repair-feedb]]. The targeted-repair papers lack the matched arm [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]]. Self-written test adequacy versus own confidence is CLEAN (provisional). The nearest work measures adequacy without confidence: 19.7% of LLM-written tests fail to execute and 15.6% of failures are wrong-oracle [[261032548-beyond-coverage-and-mutation-a-blind-spot-analysis-of-llm-generated-un]].

Committed reading: L4 is NARROW but the wrong bet for a first TMLR paper. It needs the unrun v4 pipeline, a new label unit that is noisier than published patch labels, and a repair-method comparison that adds no calibration claim. Gros and Devanbu's leave-one-out collapse (Qwen Probe-7B Brier skill -0.01 on LiveCodeBench, Table 7) also warns that fine-grained probes may not transfer. Cite the line-level occupant, name the test-group unit as untested future work, and move on.

## 6. F: Measurement-instrument framing

Every quantity F proposes maps onto an existing one:

| F quantity | Nearest existing quantity |
|---|---|
| Readout bias | Yates calibration-in-the-large term, (mu_F minus mu_Y) squared [[260305544-yates-covariance-decomposition-rearrangement-for-brier-score-full-text]], or the signal-detection criterion [[measuring-some-aspects-of-the-metacognition-of-ai]] |
| Resolution against an internal reference | A difference of Murphy resolutions; Ghosh et al. report 0.06371 for behavioral consensus against 0.03160 for verbal, a 2.02x ratio (Section 6, Table 3) [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]. Alternatively, the grouping term, which recalibration "leaves essentially unchanged" [[decomposing-probabilistic-scores-reliability-information-loss-and-uncertaintysup]] |
| Cross-format noise | Already reported as pairwise Spearman of 0.126, -0.069, and 0.247 across three verbal formats [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]], and as AUPRC spread under paraphrase [[factual-confidence-of-llms-on-reliability-and-robustness-of-current-estimators]] |
| Metacognitive efficiency | meta-I after Cacioli's v3 retraction of the M-ratio for open-ended generation [[do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec]] |

The internal-reference idea is also circular on code. The probe is trained on the same execution labels it would referee, so any "relative to internal state" quantity reduces to a contrast of two ordinary resolutions [[interim-report-f-metrology-residual-quantity]]. The measurement-validity vocabulary is in use. Metrology-proper terms (measurand, GUM uncertainty budget) are CLEAN (provisional) for LLM confidence, but vocabulary is not a contribution.

F is OCCUPIED. It earns a place as a reporting discipline: separate bias, resolution, and noise; report Murphy terms and Brier skill beside AUROC. The L1 protocol already requires that discipline. Use "readout" as exposition and claim nothing.

## 7. Close occupants

### 7.1 Ribeiro et al., ICSE 2026 (arXiv 2512.07404), published

**What it occupies:** probe beats likelihood and verbal confidence on code, at whole-solution granularity, for four 7-8B instruct code models on HumanEval and BigCodeBench, measured as selection accuracy among four candidates (Sections 4.1.4, 4.2.1; Tables 3 and 4) [[on-llms-internal-representation-of-code-correctness]].

**What it leaves open:**

- calibration metrics (none reported);
- sampling agreement;
- base and instruct pairs, reasoning models, and contamination control (all absent; the dossier lists the search terms);
- supervision-matched readouts (verbal is zero-shot, Section 4.1.2);
- self-generated candidates in the headline design (the correct class is the human reference, Section 4.1.1);
- within-problem AUROC on the model's own samples (RQ2 reports pass@rank only, and "only a few comparisons reached statistical significance").

**How to cite it:** as the occupant of the qualitative claim, and as the motivating design whose three confounds the new paper controls. Never as a strawman.

### 7.2 The four close citers

- **Campos, Klassert, and Ulges, 2611.07876 (concurrent, 5 November 2026).** Occupies probe versus token probability versus EigenScore under benchmark and language shift on two models. It is the only code paper reporting pooled and within-problem AUROC side by side (Sections IV, VI-C; Tables IV and V), and it recommends "reporting such a within-problem measure alongside the pooled one." It leaves open verbal numeric confidence, base and instruct pairs, ECE, and a probe read under reasoning [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]. It is the closest occupant of the proposed headline. The new paper extends its within-problem scoring to verbal, trained, and per-candidate sampling readouts on self-generated samples. Its Qwen3-Coder tie (0.620 versus 0.629) is the prior result the new paper either replicates at scale or overturns.
- **Ribeiro et al. follow-up, 2608.08266 (concurrent).** Occupies the probe-robustness facet: the configuration flips by benchmark, only mean-difference directions generalize, and fault isolation does not help. It reruns no verbal or sampling readout [[on-the-robustness-of-llms-internal-representation-of-code-correctness]].
- **Di Cicco, 2606.14530 (concurrent).** Occupies the pre-generation probe on one model, Qwen3-4B-Instruct-2507, with 444 LiveCodeBench tasks, AUC 0.881, and a 0.657 prompt-length baseline. Because it uses one attempt per task, it carries no within-problem information [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]].
- **Silva, Tu, and Monperrus, 2607.05188 (concurrent).** Occupies step-level probes in coding agents, with AUC up to 0.83 for full correctness. It has no verbal, token, or sampling comparison [[260705188-latent-programming-horizons-in-coding-agents-full-text]].

### 7.3 Other close occupants by candidate

| Occupant | Status | Occupies | Leaves open for this design |
|---|---|---|---|
| NeuroSym-Cal [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]] | Findings of ACL 2026 (vault ABSTRACT-ONLY; full text per dossier) | Three families plus multicalibration, three models, three benchmarks, per-model post-cutoff holdout | Probe, label independence, pre-cutoff contrast |
| Tuerlings and Valdenegro-Toro [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]] | UncertaiNLP 2026 | Verbal formats on code, shared post-cutoff window, ECE and AUROC decoupling | Non-verbal families, estimator variants, within-problem scoring |
| Rathnasuriya and Yang [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]] | concurrent | Token-level overconfidence, base versus instruct (two pairs), Brier skill after recalibration | Probe, verbal readout, oracle swap |
| Liu et al. [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]] | concurrent | Oracle dependence and label independence, text-to-SQL | General code, cross-family rankings |
| Gros and Devanbu [[localized-calibrated-uncertainty-in-code-language-models]] | preprint (December 2025) | Line-level probe versus verbal versus sampling, with Platt on every readout | Program-level, own-model probe for GPT-4o, trained verbal |
| Miglani et al. [[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]] | concurrent | Within-problem probe versus confidence, steering null | Verbal readout, sample size |
| Klassert thesis [[abstract]] | preprint (MSc thesis) | Probe calibration (Brier skill) on code | Readout contrast, contamination control |
| Code-MUE, Functional Entropy, Sharma and David [[code-mue-measuring-code-llms-uncertainty-through-execution-based-semantic-intera]] [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]] [[assessing-correctness-in-llm-based-code-generation-via-uncertainty-estimation]] | ISSTA 2026; concurrent; preprint | Execution and symbolic agreement families | Probes, label independence (Code-MUE violates it) |
| Openia, AutoProbe [[correctness-assessment-of-code-generated-by-large-language-models-using-internal]] [[model-agnostic-correctness-assessment-for-llm-generated-code-via-dynamic-interna]] | JSS 2025; preprint | Probes for code correctness | Numeric verbal, calibration metrics |
| Tahimic and Cheng [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]] | preprint | SAE directions, base-to-instruct persistence, steering | Verbal readout, calibration |
| CodeRefuser [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]] | concurrent (16 May 2026) | Risk-controlled abstention on code | Budget routing against random and oracle |
| Heteroskedastic Signals, SWE-Verifier, SWE-Router, Give-Up [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]] [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]] [[swe-router-routing-in-multi-turn-agentic-software-engineering-tasks]] [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]] | concurrent | Gated compute with proxy, trained, or prior signals | Elicited verbal or probe gate, clean labels, attainable oracle |
| Barkan et al.; Open the Oyster [[do-large-language-models-know-what-they-are-capable-of]] [[open-the-oyster-empirical-evaluation-and-improvement-of-code-reasoning-confidenc]] | preprints | Reasoning and verbal confidence on code-adjacent tasks | Same-weights toggle, probe under reasoning |
| Miao and Ungar; Probe-SD; RLCR; When Words Fall Short; RLCM; Bulut [[closing-the-confidence-faithfulness-gap-in-large-language-models]] [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]] [[beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty-2]] [[when-words-fall-short-iterative-synergy-between-verbalized-reasoning-and-hidden]] [[process-supervision-of-confidence-margin-for-calibrated-llm-reasoning]] [[its-the-problem-not-the-pathbudget-and-difficulty-confounds-in-llm-reasoning-tra]] | preprints; COLM 2026 (RLCM) | The general-NLP side of every L2 residual: gap in base models, training closes or does not close it, the within/between identity | Execution labels and symmetric supervision on code |

## 8. Verdict table

| Candidate | Component | Verdict | Load-bearing location | Status the verdict rests on |
|---|---|---|---|---|
| L1 | Q1 four families against execution labels | OCCUPIED (union) | NeuroSym-Cal Sec 4.2 (dossier; vault ABSTRACT-ONLY); Campos 2611.07876 Sec IV | published plus concurrent |
| L1 | Q2 breadth on identical generations | NARROW | Code-MUE Sec 5.1; NeuroSym-Cal Sec 4.1 | published |
| L1 | Q3 release split for calibration | NARROW | NeuroSym-Cal Sec 4.1; Tuerlings Sec 3.1; Campos 2512.08810 Sec 5.1 | published plus preprint |
| L1 | Q4 label independence as a tested factor | NARROW | Liu 2609.25938 abstract and Sec 1; Tuerlings Sec 3.3; Code-MUE Sec 5.2.1 | concurrent |
| L1 | Q5 ranking changes with estimator | NARROW (ECE versus AUROC); CLEAN (provisional) for estimator variants | Tuerlings Table 1, Sec 4.6 | published |
| L1 | Q6 recalibration control | OCCUPIED (token level); NARROW (cross-family) | 2610.11300 Sec 6.1, Table 5 | concurrent |
| L1 | Q7, Q8 test-free agreement, execution or symbolic semantic entropy | OCCUPIED | 2502.11620 Sec 1; 2605.28500 Sec 4.1; Code-MUE | preprint and published |
| L1 | Q9 release-window benchmarks used for calibration | OCCUPIED | Tuerlings Sec 3.1; NeuroSym-Cal Sec 4.1 | published |
| L1 | Q10 test insufficiency changes rankings | CLEAN (provisional) | Nearest: EvalPlus (accuracy only); Liu (SQL) | n/a |
| L1 | Q11 multicalibration | OCCUPIED (token); NARROW (cross-family) | 2512.08810 Table 1; Klassert Table 5.7 | preprint |
| L1 | Q12 self-judgment as confidence | OCCUPIED | AutoProbe Table 5; NeuroSym-Cal | preprint and published |
| L1 | Q13 contamination changes calibration | CLEAN (provisional) | None fetched | n/a |
| L1 | Whole: comparison / protocol | OCCUPIED (union) / NARROW | as above | |
| L2 | Q1 probe versus own readouts, uncontrolled | OCCUPIED | Ribeiro Sec 4.2.1, Tables 3-4 | published (ICSE 2026) |
| L2 | Q1c controlled: supervision-matched, input-only baselines, within problem, self-generated | NARROW | Campos 2611.07876 Sec VI-C, Table V; Miglani Sec 4.2, Table 1; Liu 2312.03729 Sec 3 | concurrent plus 2023 |
| L2 | Q2a base versus instruct by readout | NARROW | 2610.11300 Sec 5.5; 2510.02917 Sec 5.5; 2603.25052 Sec 3.1, 3.3 | concurrent and preprint |
| L2 | Q2b same-weights reasoning toggle by readout | NARROW | Campos Sec V-A, VIII; Barkan Exp. 1, 3; Open the Oyster Sec 5.1 | concurrent and preprint |
| L2 | Q3 format | OCCUPIED (within verbal); NARROW (format by readout) | Tuerlings Table 1 | published |
| L2 | Q4 where the gap arises on code | NARROW | 2603.25052; 2610.11300 Sec 5.5 | |
| L2 | Q5-Q7 code probes, transfer, white-box readouts | OCCUPIED | Openia; AutoProbe; 2611.07876; 2510.02917; 2606.14530 | mixed |
| L2 | Q8 post-training stages | NARROW (weak residual) | math only: 2607.13753 Table 1 | concurrent |
| L2 | Q9 reasoning and stated confidence on code | NARROW; CLEAN (provisional) for trace signals beating the stated number | Barkan; Open the Oyster; Yoon (non-code) | preprint |
| L2 | Q10 probe versus stated, reasoning on, code | NARROW | RLCM Table 1 (ECE only) | COLM 2026 |
| L2 | Q11 trained stated confidence on code, discrimination | CLEAN (provisional) | NLP: Probe-SD Table 2; RLCR Table 1; When Words Fall Short Sec 2.2 | preprints |
| L2 | Q12 causal intervention on stated confidence | NARROW | 2510.02917 Sec 5; Miglani Sec 4.4; Kumaran 2604.22271 (non-code) | |
| L2 | Q13 pooled versus within problem | NARROW | Campos Table V; 2610.05572 (agents) | concurrent |
| L2 | Whole | NARROW, conditional on the controlled headline | | |
| L3 | Q1, Q4, Q5 routing by elicited confidence against random and oracle | NARROW | 2606.15841 Table 1; 2610.30284 Tables 1-2; 2607.00053 Sec 5.3; 2611.06372 Tables 1, 3 | concurrent |
| L3 | Q2, Q7 update after a shown failing test | CLEAN (provisional) | Nearest: Kaddour Sec 2.2.1; Barkan Exp. 2-3 | preprint |
| L3 | Q3 selective prediction on code | OCCUPIED | CodeRefuser Table 1, Figs 2-3 | concurrent |
| L3 | Q6 repository-agent uncertainty | OCCUPIED (union) | SWE-Verifier; SWE-Router; Kaddour | concurrent |
| L3 | Whole | NARROW | | |
| L4 | Q4 line, token, step localization | OCCUPIED | 2512.24560 Tables 3-4; FLARE Table 4; 2607.05188 Sec 3.3 | preprint and concurrent |
| L4 | Q1 per-test-group localization | NARROW | 2512.24560; 2607.05188 | |
| L4 | Q2 targeted repair versus regeneration | NARROW | FLARE; Olausson Sec 4; Iscan | |
| L4 | Q3 test adequacy versus own confidence | CLEAN (provisional) | Nearest: 2610.32548 | |
| L4 | Whole | NARROW | | |
| F | Q1 vocabulary | OCCUPIED (measurement validity, psychometrics); CLEAN (provisional) for metrology-proper terms | 2610.25846; 2603.14893 | concurrent and preprint |
| F | Q2 bias, resolution, noise decomposition | OCCUPIED (union) | 2603.05544; 2603.15232; 2610.25846 | preprint |
| F | Q3 residual quantity | OCCUPIED (effective) | 2406.13415; 2610.25846 | |
| F | Q4 meta-d' | OCCUPIED | 2603.29693; 2603.25112 v3 | preprint |
| F | Whole | OCCUPIED | | |

If the operator rules concurrent works out of scope, L1 Q1 becomes NARROW and L2 Q13 moves toward CLEAN (provisional). Neither change alters the recommendation. The design below holds up against the concurrent works, not just in their absence.

## 9. Ranked recommendation for TMLR

### 9.1 Rank 1: one execution-graded measurement paper with a controlled headline

**Contribution sentence.** "On self-generated function-level code with execution labels, we test whether hidden-state probes carry correctness information the model's own readouts lack. Every readout receives the same supervision. Within-problem and between-problem discrimination are scored separately. The ranking is checked against the calibration estimator, a stronger test oracle, and a per-model release-date split."

**Design.**

1. Generate k samples per problem from at least three open model families at two scales on three benchmarks. Use HumanEval+/MBPP+ with original and augmented tests, and LiveCodeBench windows split around each model's cutoff.
2. Score each sample with the following readouts:
   - a last-token probe and a prompt-final probe;
   - a trained own readout (a verbal or logit-feature head) on the same execution labels;
   - zero-shot numeric and categorical verbal confidence;
   - token probability;
   - per-candidate sampling agreement (cluster size under execution equivalence);
   - prompt-only and code-text-only classifiers.
3. Report pooled, within-problem, and between-problem AUROC using Bulut's decomposition [[its-the-problem-not-the-pathbudget-and-difficulty-confounds-in-llm-reasoning-tra]], plus Brier skill with reliability intervals and ECE under equal-width, equal-mass, and debiased estimators.
4. Pre-register the margin. Under the 0.05 estimate drawn from Campos and Miglani, a conservative design needs well over 100 mixed problems per model, with a problem-clustered paired bootstrap. Rathnasuriya's own ΔAUC interval for OpenCoder spans [-0.0911, 0.0652] [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]], which shows how wide uncontrolled intervals run.
5. Add an offline routing replay with random and label-sorted oracle arms at matched budgets, stratified by pass rate.
6. Run the base-versus-instruct and same-weights reasoning arms only if the controlled gap clears the pre-registered margin.

**Evidence needs.** The new pipeline must produce every number. The legacy bundle supplies none. The trained own-readout arm and the augmented-test relabeling are the two components whose absence a reviewer would cite first: Probe-SD and RLCR for the former, EvalPlus and Liu for the latter.

**TMLR fit.** Criterion 1 is met by construction. The headline claim is a controlled measurement whose outcome is reported either way. A null result says that the published probe advantage on code is a supervised, between-problem effect, and that the model's own confidence, given the same labels, ranks its candidates as well as a probe does. That would revise how Ribeiro, Openia, Di Cicco, and the Klassert thesis are read. A positive result says that information is lost between state and output even under matched supervision, and only then does the decomposition become worth running. Criterion 2 is met because the ML calibration audience and the SE confidence audience are both active (ICSE 2026, ISSTA 2026, Findings of ACL 2026, UncertaiNLP 2026, COLM 2026, and many concurrent preprints). Novelty is claimed only for the controlled test and the protocol, which keeps the paper clear of the incorrect-novelty clause.

**Main risk.** A concurrent paper runs the within-problem, supervision-matched comparison first. Campos et al. already recommend within-problem reporting, and the RheinMain group has the models, the probes, and the CALIBRI labels [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] [[abstract]]. Mitigation: the L1 protocol and the verbal and trained-readout arms are what that group's papers lack, so even a scoop of the probe-versus-confidence tie leaves the verbal and trained arms, the oracle swap, and the release contrast standing. A second risk is that verbal readouts collapse on small instruct models: 8 of 18 cells in Tuerlings [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]. Mitigation: report collapse as a validity outcome with a distinct-values guard, and rely on the trained head for the matched-supervision comparison.

### 9.2 Rank 2: L1 plus L3 as a measurement-only paper

**Contribution sentence.** "Confidence-method rankings for code under execution labels are, or are not, stable to the estimator, the test oracle, and contamination; and confidence-routed execution budgets do or do not beat random routing once those controls are applied." Under the replacement order in the brief, this is the fallback if the probe arms prove infeasible. It claims no novelty for the comparison, which is OCCUPIED (union), only for the protocol (NARROW) and for Q10 and Q13 (CLEAN (provisional)). TMLR fit is good on criterion 1 and modest on criterion 2. Main risk: rankings may turn out invariant to every control. That is still a robustness finding, but a less interesting one.

### 9.3 Rank 3: L2 factorial decomposition as the spine

**Contribution sentence.** "On code, the probe-minus-stated-confidence gap opens at instruction tuning or closes with reasoning." The residual is NARROW, and the code reasons hold: DeepSeekCoder's anti-aligned base readout, and the obstacle of producing code and confidence together. But the spine presumes a gap the controlled evidence suggests may be small, so it ranks below the design that tests the gap first. It is the conditional extension of Rank 1, not a separate paper. Main risk: decomposing a near-zero gap, plus the elicitation problem for base models, where Ghosh's 7B base model emitted "essentially two labels" [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]].

### 9.4 Rank 4: L4

NARROW, but it needs an unrun pipeline and an operator scope decision, and it adds a repair-method claim rather than a calibration claim. Keep it as future work.

### 9.5 Rank 5: F

OCCUPIED. Use the vocabulary as exposition only.

### 9.6 Forward-looking implications

The field is converging on one measurement correction from several directions. Bulut's identity [[its-the-problem-not-the-pathbudget-and-difficulty-confounds-in-llm-reasoning-tra]], the agent-difficulty decompositions [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]] [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]], Campos's within-problem recommendation, and Liu's oracle-independence rule all say the same thing: most published confidence numbers measure the problem and the oracle, not the candidate. Within a year, I expect reviewers at ML and SE venues to ask for within-problem scores and oracle swaps as a matter of course, much as EvalPlus made augmented tests standard for accuracy. A paper that arrives with that protocol already applied to all four families, and with a supervision-matched answer to whether probes know more, will be cited as the reference measurement whichever way its headline falls. A paper that arrives with another pooled "probes beat verbal" table will meet a literature that has already moved past it. Two further consequences follow. First, if trained own-readouts close the gap on code, the practical message for tool builders is to train the output channel on execution labels rather than ship probes, and L3's routing becomes a question about trained heads. Second, if the gap survives within problem under matched supervision, the case for white-box confidence in code tools becomes much stronger than the current literature can support, and the factorial decomposition becomes the natural follow-up.

## 10. Instrument gaps

Each gap and the verdicts it weakens:

- **G-FT (arXiv full-text search failed validation).** `searchtype=ft` returns a blank form, and the full-text host is off the allowlist. Every body-text negative is a gap: L1 Q5 (estimator variants), Q10, and Q13; L2 Q9 (trace signals) and Q11; L3 Q2 and Q7; L4 Q3; F Q1 (metrology-proper terms). A one-paragraph experiment inside a larger paper would be invisible to title and abstract search, which bears most on L3 Q7 and L2 Q11.
- **G-OA (OpenAlex).** Full text is partial (one of two known positives), and the daily budget was exhausted at about 05:05 IST. Every later OpenAlex negative is a gap, including the last three seeds of a forward-citation screen.
- **G-S2 (Semantic Scholar keyword search).** HTTP 429 throughout, on ten attempts with backoff. Keyword recall from Semantic Scholar is missing. Citation lookups worked intermittently.
- **G-AX (arXiv export API).** HTTP 429 on several queries, including searches for within-problem code probes and per-test confidence. No negative in this draft rests on arXiv metadata search.
- **G-OR (OpenReview).** Forum pages and PDFs sit behind a browser challenge. OpenReview-only full texts, including possible TMLR, ICLR, and COLM submissions, are unreachable.
- **G-FCS (partial forward-citation screens).** Not screened or only partly screened: 2611.06372, 2610.30284, 2608.14659, and 2607.00053 (L3); forward citers of 2512.24560, of which only four were returned (L4); Zeng 2504.06564 and Yoon 2505.14489 (L2 reasoning). Ribeiro's close citers, the four in Section 7.2, were screened. Campos 2611.07876 is five days old at the run date, so its citers are not yet indexed. That bears on the Rank 1 scoop risk.
- **Evidence-quality gaps, not instrument failures:**
  - NeuroSym-Cal's vault note is ABSTRACT-ONLY, and its section citations come from the full-text dossier, which also records a mismatch: the final method is prompted self-verification, not latent perturbation.
  - The column mapping of Lugoloobi et al.'s Table 2 was read from the header.
  - Campos et al.'s Table II was garbled in extraction; within-problem numbers come from Section VI-C, Table IV, and Table V.
  - Miglani et al.'s confidence intervals for 0.677 versus 0.703 are not reported in the sections read.
  - The Spiess et al. ICSE 2025 note was treated as abstract-level by one investigation and as full text by its dossier [[240202047-calibration-and-correctness-of-language-models-for-code]]. No verdict here rests on it.

These gaps mean every CLEAN verdict here is provisional, and the recommendation claims novelty only for components that are NARROW against named occupants. The headline of Rank 1 is NARROW, not CLEAN. Its defensibility comes from the controls it adds against named, fetched works, not from an absence that broken instruments cannot certify.
