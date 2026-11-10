# Positioning a TMLR study of code-model confidence against execution ground truth: which verdicts hold, under which conditions

**Executive summary.** The literature from January 2022 to November 2026 does not leave any of the five candidates fully clean, but it does not fully occupy the strongest one either. Both readings of the evidence (the readings "the topic is taken" and "a defensible residual survives") turn out to be correct, each under a different set of boundary conditions. Four switches decide which reading applies to a given component. (1) Whether concurrent work (first posted after 2026-05-10) counts against novelty. (2) Whether a negative from a failed or partial search instrument is read as absence or as an open question. (3) Whether a reviewer accepts the stated code-specific reason that a code result could differ from the closest general-NLP result (the brief's A21 rule). (4) What the controlled experiment returns once it is run. Under every setting of the first three switches, one contribution survives. It is a supervision-matched, within-problem test of whether hidden-state probes carry correctness information that the model's own readouts (stated confidence, token probability, and sampling agreement) do not, on self-generated code graded by execution. It sits on top of an L1 measurement layer: an estimator set, an oracle swap from base to augmented tests, and a release-date split. The uncontrolled headline "probes beat stated confidence on code" is OCCUPIED by Ribeiro et al. (ICSE 2026) whatever the switches say [[on-llms-internal-representation-of-code-correctness]]. The factorial extension (base versus instruct, reasoning on versus off) is NARROW only if the code-specific A21 reasons are accepted. The two readings disagree mainly about the switches, not about the facts.

The ranked recommendation is conditional, and this draft states the conditions:

- **Rank 1: the controlled L2 test plus the L1 protocol.** It is strongest whatever the controlled test returns, because a null result is itself the finding. Its claims rest on evidence the paper produces itself, which is what TMLR's first criterion asks for.
- **Rank 2: L3 as an offline routing replay with random and label-sorted oracle arms.** It is strongest if concurrent work is ruled out of scope and the controlled test finds a usable within-problem signal.
- **Rank 3: the stated-confidence update after a shown failing test.** It is CLEAN (provisional), and it is the component most exposed to the failed full-text instrument.
- **Rank 4: L4 per-test-group localization.** It needs an unrun pipeline.
- **F: exposition only.** It is OCCUPIED as a framing under every switch setting.

## 1. Scope, instruments, and verdict rules

### 1.1 What this draft argues

The binding scope is the revised positioning brief: five candidates (L1, L2, L3, L4, F), each with occupancy questions; a breadth matrix of 14 dimensions; verdicts of OCCUPIED, OCCUPIED (union), NARROW, CLEAN, and CLEAN (provisional); and the pivot criteria for L2 as the paper's spine. The wave's working verdict table rates L1 OCCUPIED (union) for the comparison and NARROW for the protocol, L2 OCCUPIED for the uncontrolled headline and NARROW for the controlled and factorial versions, L3 NARROW, L4 NARROW (line level OCCUPIED), and F OCCUPIED as a framing. This draft does not overturn those ratings. It shows that each one is a conditional statement, names the condition, and asks what the paper has to produce for the rating to hold up in review.

The reconciling move matters because the strongest pieces of counterevidence point both ways. The within-problem ties that most weaken the probe headline come from concurrent preprints: Campos et al. (0.620 versus 0.629) and Miglani et al. (0.677 versus 0.703) [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]. The difficulty identity that explains those ties is also concurrent (Bulut, Eq. 1) [[its-the-problem-not-the-pathbudget-and-difficulty-confounds-in-llm-reasoning-tra]]. If the operator rules concurrent work out of scope, the residual gets wider, but the paper loses the published reason to expect a small controlled gap. A reviewer will still know those papers. So the concurrency window is not one dial that turns occupancy up or down. It moves novelty and motivation in opposite directions.

### 1.2 The four switches

| Switch | Setting A | Setting B | Components it moves |
|---|---|---|---|
| S1 concurrency window | Concurrent preprints (after 2026-05-10) count as occupants | They count only as related work | L1 Q4, L2 Q2a, L2 Q13, L3 Q1, L3 Q3; the evidence base for the expected size of the controlled gap |
| S2 instrument gaps | A gap is read as absence | A gap is read as a possibly hidden occupant | Every CLEAN (provisional): L1 Q5 (estimator variants), Q10, Q13; L2 Q9 (trace signals), Q11; L3 Q2/Q7; L4 Q3; F Q1 (metrology-proper terms) |
| S3 A21 code-specific reason | Accepted | Rejected | L2 Q2a, Q2b, Q4, Q8 (the factorial residuals); L4 Q1; F Q3 already fails |
| S4 controlled test outcome | Probe keeps a within-problem margin over a trained own readout | Tie, or the trained readout closes the gap | Which L2 headline is true; whether the L2 factorial and L3 routing are worth running |

S1 through S3 are judgment calls about the literature, and the brief already flags the six-month window as a proposal for the operator to confirm. S4 is empirical. It is the only switch the paper can set by itself, which is why the recommendation in section 9 routes everything through it.

### 1.3 Two definitional switches hidden inside the verdict rules

Two more conditions are definitional. They are easy to miss, and they decide two verdicts.

**What counts as "stated confidence".** NeuroSym-Cal's breadth matrix counts "verbal P(True) and self-verification" as the stated family (dossier, Sec 3 and 4.2). Campos et al. use a Yes/No verdict-token probability, which the wave calls "output confidence" and does not count as verbal numeric confidence (searched: "verbalized"). If P(True) counts as stated confidence, the L1 four-family union is easy to assemble. If only numeric or categorical verbal confidence counts, the stated family on code is covered only by Ribeiro (two categorical formats, zero-shot), Tuerlings and Valdenegro-Toro (three verbal formats, verbal only), and Gros and Devanbu (line-verbalized, line level) [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]] [[localized-calibrated-uncertainty-in-code-language-models]].

**What counts as "against execution labels" for a calibration claim.** Ribeiro reports selection accuracy and pass@rank-k, with no AUROC, ECE, or Brier score (searched: "AUROC", "ECE", "calibration error"). Gros and Devanbu report BSS, ECE, and AUC, but on minimal-patch line and token labels: "we assume that 'intent' is fully defined by hidden test cases" (Sec 4) [[localized-calibrated-uncertainty-in-code-language-models]]. Their Tables 3 and 4 compare token probability, multisampling, line-verbalized confidence, and two probes, with five-fold cross-validation. So a four-family comparison with calibration metrics on code already exists in a pre-window preprint, at line granularity. If the L1 core claim is read as granularity-free, Gros and Devanbu nearly occupy L1 Q1 alone. If it is read as program-level, they do not.

The committed reading here is that L1's core claim, as the brief states it, is program-level ("establishes which methods track correctness on code"). That keeps Gros and Devanbu as the L4 occupant and an L1 neighbor, not an L1 occupant. The paper should still say outright that the four-family comparison exists at line level, or a reviewer who knows that paper will read the omission as incorrect novelty.

### 1.4 TMLR's two criteria as a boundary condition

The venue rubric (`docs/s2/venue/TMLR_RUBRIC.md`) quotes three passages that change how occupancy should be weighed. Reviewers are told: "Do not penalize modest significance or lack of novelty". Papers "should be accepted if they meet the criteria, even if the contribution or significance of the work is modest". Rejection targets papers that "incorrectly claim novelty over existing published work" or "merely re-implement an idea that has already been reproduced before." Two consequences follow for the reconciliation. First, at TMLR, OCCUPIED is a constraint on wording, not a bar to acceptance: an OCCUPIED component can appear in the paper if it is framed as replication or as a baseline. Second, the novelty clause names "existing published work". Concurrent preprints therefore weigh less on the novelty clause than on the accuracy clause: a paper that ignores Campos et al. would not falsely claim novelty over published work, but its claim that "no study reports within-problem AUROC for code probes" would be false. Under TMLR, then, S1 matters mostly through accuracy of claims, not through acceptance.

## 2. L1: Execution-graded measurement foundation

### 2.1 Closest occupants

The L1 comparison is spread over several works, none of which crosses all families on the same generations.

- **NeuroSym-Cal (Findings of ACL 2026).** The vault note is ABSTRACT-ONLY, but the dossier rests on the full PDF. It fuses AST consensus across K=10 samples with a self-verification score. Its baselines are logit, P(True), self-consistency, and multicalibration (Sec 3, 4.2). It covers DeepSeek-R1-Distill-Llama-70B, Qwen2.5-Coder-32B-Instruct, and Llama-3.3-70B-Instruct on LiveCodeBench v2406-v2506 (400 problems), HumanEval-Pro, and DS-1000, with a per-model post-cutoff LiveCodeBench subset held out (Sec 4.1). It reports "reducing Expected Calibration Error (ECE) by 37.4% compared to Self-Consistency (0.072 vs. 0.115)" and LiveCodeBench AUROC 0.805 against 0.798 for IGLB (Sec 5.1). It has no probe family [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]].
- **Tuerlings and Valdenegro-Toro (UncertaiNLP 2026).** Six instruct coder models, 365 LiveCodeBench v6 problems in one shared window from 2024-09-19 to 2025-04-30 (Sec 3.1), and code frozen before elicitation so that "correctness labels are determined independently of any confidence estimation" (Sec 3.3). It reports ECE and AUROC decoupling: the lowest ECE, 0.013 (CodeLlama-7B Linguistic), comes with AUROC 0.491, and 8 of 18 cells collapsed (Table 1, Sec 4.6). It is verbal only [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]].
- **Rathnasuriya and Yang (2610.11300, concurrent).** 17 generation-stage and 6 prefill-stage token and sampling metrics, with a best AUC of 0.598 to 0.696 (Table 3). Platt and isotonic maps cut Brier (CodeLlama 0.459 to 0.248) while BSS stays near 0.001 (Table 5) [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]].
- **Sampling-family works with execution labels.** Code Is More Than Text: ensemble AUROC 0.776 against 0.696 for the best NL baseline, with official hidden-test labels kept separate from self-generated tests "since otherwise the functional signal would be trivially perfect by construction" [[code-is-more-than-text-uncertainty-estimation-for-code-generation]]. Semantic-distance estimators: DSDE AUROC above 0.8 in every setting [[using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation]]. Ensemble semantic entropy: Qwen3-8B accuracy 0.8247 against 0.6420 for single-model semantic entropy at 10% FPR [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]]. HonestCoder: +27.79% AUROC over the best baseline [[showing-llm-generated-code-selectively-based-on-confidence-of-llms]].
- **The oracle side.** EvalPlus: 80x tests cut pass@k by 19.3 to 28.9% across 26 LLMs and change rankings [[is-your-code-generated-by-chatgpt-really-correct-rigorous-evaluation-of-large-la]]. Liu et al. on text-to-SQL (concurrent): "Every execution-consistency score looks better under the labels of the oracle that built its clusters, in 16 of 16 combinations" (abstract and Sec 1) [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]].

### 2.2 Reading one: the comparison is taken

Read strictly, L1 Q1 asks whether four families have been compared against execution labels on code. With the P(True) reading of section 1.3, NeuroSym-Cal supplies token, stated, and sampling families, and either Campos et al. (concurrent) or Ribeiro et al. (published) supplies the probe [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] [[on-llms-internal-representation-of-code-correctness]]. That is the A20 union case: at most three works, and "the only thing left to add is running them on the same problems." The working table says that L1 Q1 becomes NARROW if concurrent work is ruled out. This draft disagrees, with a reason. Ribeiro (ICSE 2026, published) plus NeuroSym-Cal (Findings of ACL 2026, published) already form a two-work union across all four families, so the union does not depend on S1. It depends on the second definitional switch, whether Ribeiro's selection accuracy counts as being evaluated "against execution labels." The brief's L1 Q1 does not require a calibration metric, so the union stands. The committed verdict is OCCUPIED (union), robust to S1 and S2 and sensitive only to a strict metric reading.

### 2.3 Reading two: the protocol survives

The other reading holds because no occupant crosses the three controls that decide whether a family ranking can be trusted at all. The three controls are these.

- **The estimator set.** Only Tuerlings shows a ranking change across metrics on code (ECE versus AUROC and PRR, Table 1 and 2, Sec 4.3), and nobody varies the ECE estimator itself (equal-mass, debiased, smooth) [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]].
- **The oracle swap.** No code study recomputes a confidence-method ranking under base versus augmented tests. EvalPlus does it for accuracy rankings only, and Liu et al. for SQL and execution-consistency scores only [[is-your-code-generated-by-chatgpt-really-correct-rigorous-evaluation-of-large-la]] [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]].
- **A pre- versus post-cutoff contrast.** Tuerlings uses a shared post-cutoff window with no pre-cutoff comparison group. NeuroSym-Cal holds out a post-cutoff subset as an out-of-distribution test, not as a contamination contrast. LiveCodeBench supplies the release-date windows that make the contrast possible but tests accuracy, not calibration [[livecodebench-holistic-and-contamination-free-evaluation-of-large-language-model-2]].

The interpretive point that turns this into a contribution is that these controls are not cosmetic. Liu et al.'s 16-of-16 result names a mechanism that transfers to code: when sampling agreement is built from executed tests, it looks better under any label oracle that shares those tests. Code Is More Than Text guards against this by design but never tests it [[code-is-more-than-text-uncertainty-estimation-for-code-generation]]. Weak hidden suites pass plausible but wrong programs. Those false passes inflate exactly the families that track test-style agreement, so a base-versus-augmented relabeling could reorder families, not just shift pass rates.

### 2.4 Conditions

| Component | S1: concurrent excluded | S2: gaps read as possible occupants | S3: A21 rejected |
|---|---|---|---|
| Q1 four families | Stays OCCUPIED (union) via Ribeiro plus NeuroSym-Cal | No effect (positive verdict) | No effect |
| Q2 breadth | Stays NARROW (NeuroSym-Cal is published; Code-MUE is concurrent) | No effect | No effect |
| Q3 release split for calibration | Stays NARROW (Tuerlings and NeuroSym-Cal are published) | No effect | NARROW only if the reason holds: pre-cutoff problems may be memorized, so confidence would track recall, not reasoning. The wave states no direct code evidence for this |
| Q4 label independence | Moves toward CLEAN (provisional): the main evidence, Liu et al., is concurrent | Exposed | The reason is strong: hidden tests drive both the label and test-based agreement |
| Q5 estimator variants | Unchanged | CLEAN (provisional) at risk, because estimator variants would sit in appendices, where body-text search is needed | Weak reason; a reviewer could call it method hygiene |
| Q10 test insufficiency | Unchanged (EvalPlus is published) | CLEAN (provisional) at risk | Strong reason (false passes) |
| Q13 contamination changes calibration | Unchanged | Lower risk: such a result would likely surface in a title or abstract, where metadata search worked | Medium reason |

### 2.5 Committed reading

L1 is OCCUPIED (union) as a comparison and NARROW as a protocol, and both statements are true together. The protocol's value does not depend on novelty. Every L2 and L3 number the paper reports rests on the labels, so label flips under augmented tests would move those numbers too [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]]. L1 is therefore best presented as the paper's measurement layer, not as its headline. The one risk is a fully invariant pilot: if family rankings do not move under any of the three controls, the protocol becomes a robustness note, and the paper should then say "rankings are stable under these controls" rather than drop the controls.

## 3. L2: Locating the disconnect between internal state and output

### 3.1 What Ribeiro et al. occupies and what it leaves open

Ribeiro, Spiess, Devanbu, and Nadi fit a Representation Engineering LAT direction to hidden-state differences between correct and incorrect code at the final token. They use it to pick the correct implementation among four candidates, on Mistral-7B-Instruct-v0.3, Qwen2.5-Coder-7B-Instruct, OpenCoder-8B-Instruct, and CodeLlama-7B-Instruct, with HumanEval (151 tasks) and BigCodeBench (457 tasks) [[on-llms-internal-representation-of-code-correctness]]. Section 4.2.1: "LAT consistently outperforms all baselines. On BigCodeBench, it improves accuracy by +13.3 to +29.0 pp over the best reflective accuracy; on HumanEval, gains range from +8.7 to +26.2 pp over the strongest baseline." The takeaway box says +13.3 to +28.8 pp, an internal inconsistency. The verbal readouts are zero-shot (a seven-level scale and the True/False probability), and the formats disagree: Mistral scores 40.6% with Regular and 15.3% with True/False on HumanEval.

What it occupies: probe beats zero-shot verbal and likelihood readouts at whole-solution granularity, on four 7-8B instruct models, in a within-task selection design.

What it leaves open: calibration-grade metrics, sampling agreement, base and instruct pairs, reasoning models, a release-date control, causal intervention, and sub-solution granularity. Its own threats section concedes that "Prompt formatting choices or verbalized confidence levels could influence our observations."

Three design facts decide how much of the occupied claim survives a controlled replication [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].

- **Provenance.** The correct candidate is the human reference solution, and the three incorrect ones come from other models (Sec 4.1.1).
- **Supervision.** LAT is fit on 10% of tasks while the verbal readouts stay zero-shot (Sec 4.1.2).
- **A reversed likelihood readout.** The intrinsic readout picks the reference only "around 5-6%" of the time on BigCodeBench, against 25% chance, so the label runs strongly against model likelihood.

The self-generated, within-task test (RQ2, 10 samples at temperature 1.0) is the cleaner design. There, Mistral reaches 41.3% at rank 1 on HumanEval against 38.0% random, and "Only a few comparisons reached statistical significance" [[on-llms-internal-representation-of-code-correctness]].

### 3.2 The close citers

The four close citers each extend one side of Ribeiro and never cross the stated-confidence side with a factor.

- **2608.08266, same group.** It varies extraction method, framing, and location on the same four models and finds "no single configuration is best, and that isolating the fault does not help". Fitting on concept framing and validating on neutral framing gives 36 to 48% accuracy, and directions fit on the synthetic set fall to 13 to 33% (Table II). A mutation-isolated direction "separates them with high accuracy in isolation, yet does not transfer", with a 37.1-point drop on BigCodeBench against 5.2 on HumanEval [[on-the-robustness-of-llms-internal-representation-of-code-correctness]] [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].
- **2611.07876, Campos, Klassert, and Ulges (concurrent).** Six predictors from four families on Qwen3-Coder-30B and gpt-oss-20b under benchmark and language shift. It is the only code paper that reports pooled and within-problem AUROC side by side. Under language shift, within-problem AUROC is 0.58 to 0.64 for all methods against pooled 0.67 to 0.81, and confidence is best within problem for Qwen3-Coder (0.629). A probe at the last prompt token has pooled 0.891 but within-problem 0.514 (Table V, Sec VI-C). It has no verbal numeric confidence, no base and instruct pairs, and reasoning prefilled off (Sec V-A). It does include one reasoning-on check, in which medium-effort reasoning raises the Yes-probability AUROC "from 0.68 to 0.73" (Sec VIII) [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].
- **2606.14530, Di Cicco.** A pre-generation linear probe on Qwen3-4B-Instruct-2507 over 444 LiveCodeBench tasks: AUC 0.881, 0.842 after residualizing on prompt length, against a prompt-length baseline of 0.657. With one attempt per task, every scored pair is between problems [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].
- **2607.05188, Silva, Tu, and Monperrus (concurrent).** Probes on agent residual streams decode parse, tests-pass, partial-correctness ("the number of failing tests is strictly less than at the beginning"), and regression labels (Sec 3.3). It has no verbal comparison [[interim-report-l4-localization-occupancy-and-targeted-repair]].

The pattern is the reconciling fact. The probe side of L2 is crowded, and the stated-confidence side of L2 on code is thin (Ribeiro zero-shot; Tuerlings verbal only; Gros line-level). The two sides never meet under a factor.

### 3.3 Reading one: L2 is occupied

The "occupied" reading has real support. Three of the four L2 factors have a general-NLP direction [[interim-report-l2-residual-post-training-reasoning-format-on-code]].

- **Base models.** Miao and Ungar find that base models already show the gap: "base models verbalize poorly calibrated confidence despite encoding well-calibrated accuracy information internally". Probe directions for accuracy and for verbal confidence have cosine similarity "below 0.04" (Sec 3.3), and joint solve-and-rate prompting inverts the relation (Sec 3.4, "Reasoning Contamination Effect") [[closing-the-confidence-faithfulness-gap-in-large-language-models]].
- **Post-training.** Base models are semantically calibrated, and RL or DPO instruction tuning and chain of thought break that calibration (Fig 2) [[trained-on-tokens-calibrated-on-conceptsthe-emergence-of-semantic-calibration-in]].
- **Training the verbal channel.** Probe-SD lifts verbal AUROC from .825 to .928 against a probe at .948, and RLCR's trained verbal confidence beats RLVR plus a probe on HotpotQA (0.69 versus 0.55) [[interim-report-l2-residual-post-training-reasoning-format-on-code]].

On code, format effects within verbal readouts are already shown (Tuerlings Table 1, three formats) [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]. Under A21 clause 2, "a factor with an established direction in general NLP and no stated reason why code would differ" is OCCUPIED. If a reviewer rejects the code-specific reasons, Ribeiro plus Miao and Ungar plus Tuerlings plus Rathnasuriya reads as near-complete coverage, and L2 reduces to a model swap.

### 3.4 Reading two: a controlled, code-grounded residual survives

The "narrow" reading also has real support, and it holds whatever S3 says, because its strongest residual is a label protocol, not a factor whose direction NLP already established. The controlled test asks something the occupants cannot answer, because each controls a different confound and none controls all three [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].

1. **Difficulty (between-problem variance).** Bulut's Eq. 1 decomposes pooled AUROC as lambda times within-problem AUROC plus (1 minus lambda) times between-problem AUROC. "In the standard design with one attempt per problem (k_c = 1), lambda = 0" [[its-the-problem-not-the-pathbudget-and-difficulty-confounds-in-llm-reasoning-tra]]. For 164 problems with 10 samples each, split 5 pass and 5 fail, same-problem pairs are about 0.6% of all pairs, so a pooled AUROC on function-level code is about 99% a between-problem number. The agent literature reports the same structure: ">99.93% of the underlying positive-negative pairs" are cross-unit, and a difficulty oracle reaches pooled AUROC 0.945 while sitting at chance within task [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]]. Trajectory predictors reach about 0.62 AUROC against 0.92 for an issue-difficulty reference, with gain beyond difficulty "statistically equivalent to zero" [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]]. Early prefixes give near-chance within-task discrimination even though 87.51% of runs have already invoked tests [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]].
2. **Supervision asymmetry.** Ribeiro's probe is fit on labels while its verbal readout is zero-shot. In general NLP, matching the supervision flips the winner on 2 of 3 datasets (Liu et al. 2312.03729, Sec 3). On code, the only partial control is Platt scaling on every readout in Gros and Devanbu, where a 0.03 to 0.12 AUC deficit survives for verbal confidence at line level [[localized-calibrated-uncertainty-in-code-language-models]] [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].
3. **Provenance.** A reference-versus-other-model contrast lets a fitted direction learn "human-like versus LLM-like" code. The follow-up paper itself names "variable names or implementation style" as a confound in contrasting pairs [[on-the-robustness-of-llms-internal-representation-of-code-correctness]].

The A21 test for this residual does not depend on contested NLP directions. Clause 1 holds, because the residual is a label protocol and a set of controls, not a model swap. Clause 2 holds through three reasons specific to code. Execution labels let every readout be trained on the same supervision. Function-level difficulty can be recovered from prompt text (a TF-IDF baseline gets 0.84 to 0.86 of a 0.90 to 0.91 pre-generation probe on LiveCodeBench). And the occupant's contrast classes differ in provenance [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]. Reading two therefore keeps the controlled test under both settings of S3.

### 3.5 The controlled test is the hinge, and each outcome yields a different paper

Both readings point to one deciding experiment: a same-sample, within-problem comparison on code that includes a trained own readout. Two investigations reached it by different routes. One came from the post-training literature (pivot A14), the other from the supervision asymmetry in the occupant's design [[interim-report-l2-residual-post-training-reasoning-format-on-code]] [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]]. The best current estimate comes from three within-problem comparisons on self-generated code. Miglani et al. find DiffuCoder 0.842 against 0.838, and Qwen2.5-Coder 0.677 against 0.703 for completion log-probability (56 mixed problems). Campos et al. find Qwen3-Coder probe 0.620 against confidence 0.629. These predict a controlled gap of at most about 0.05 within-problem AUROC, possibly zero. That estimate rests on samples of 19 and 56 mixed problems, and it was held at about 65% confidence [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]] [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].

The outcome branches map onto distinct, defensible papers:

| Outcome of the controlled test | What the paper can claim | What then becomes worth running |
|---|---|---|
| (α) Probe keeps a within-problem margin above about 0.05 over a trained own readout, with a problem-clustered CI that excludes zero | The disconnect is real unexpressed information on code, beyond difficulty and supervision; this corrects and strengthens Ribeiro's design | The factorial decomposition (base versus instruct, same-weights reasoning toggle) as the location claim; L3 routing by the probe |
| (β) Probe matches a trained own readout but beats zero-shot verbal | The "disconnect" is an elicitation and supervision gap: the information reaches the output channel once that channel is trained on execution labels. This is the code analogue of Probe-SD and RLCR, and it is unmeasured on code | Trained-readout routing in L3; the factorial run becomes optional |
| (γ) Every readout sits near 0.5 to 0.65 within problem, and pooled differences are difficulty | Code correctness readouts at this scale mostly detect hard problems; the pooled probe advantage in the literature is mostly between-problem | L3 replay, expected to fail in the hard stratum (a prediction the paper can test and report) |

Outcome γ does not trigger pivot criterion 3, and outcome β does not either, because the brief defines pivot 3 over a fetched record showing the gap closes. If the paper's own trained arm closes the gap, that is a finding, not a disqualification. The A14 criterion protects against building on a claim the literature has already refuted. It does not stop the paper from refuting the claim itself. Under TMLR's first criterion, all three outcomes are publishable if the design is right. Under its second, outcomes α and β interest the probing and calibration audiences directly, and outcome γ interests anyone who reports pooled AUROC for code correctness, a practice the occupants themselves follow.

### 3.6 Pivot criteria under the switches

- **Pivot 1 (A20 union covers probe, stated, sampling, base and instruct, and reasoning).** It is not triggered under any switch setting. With concurrent work included, Campos et al. add sampling and a single reasoning-on check for output confidence, but no stated numeric confidence and no base models. With concurrent work excluded, the coverage shrinks further.
- **Pivot 2 (A21 residual is only a model change).** It is triggered for the headline under all settings. For the factorial versions it is triggered only if S3 is rejected. For the controlled test it is never triggered.
- **Pivot 3 (A14, trained stated confidence closes the gap on code).** It is not triggered by any fetched work, but the CLEAN (provisional) status of "trained verbal confidence on code with AUROC" depends on S2. The nearest code data point, RLCM's LiveCodeBench column (probe-read ECE 0.051 against trained verbal 0.218), reports ECE only [[interim-report-l2-residual-post-training-reasoning-format-on-code]]. A one-column result inside a math-training paper is exactly the kind of evidence that body-text search would find and title search would miss.
- **Pivot 4 (A15, causal localization on code).** It is not triggered. The code interventions that exist act on output correctness, not on stated confidence. Tahimic and Cheng's steering fixes 4.04% of errors and corrupts 14.66% of correct code (Sec 5, Fig 8), and Miglani's steering is null [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]] [[interim-report-l2-residual-post-training-reasoning-format-on-code]].

### 3.7 The factorial residuals, and why they depend on S3

The base-versus-instruct residual on code has one direct data point, which does not follow the NLP sign. In Rathnasuriya and Yang (Sec 5.5, MBPP+), instruction tuning raised failing-program confidence for OpenCoder from 0.8685 to 0.9224 with ΔAUC −0.0136 (CI [−0.0911, 0.0652]). DeepSeekCoder's base confidence was anti-aligned with correctness (AUC 0.4391) and rose to 0.5654 after tuning (ΔAUC +0.1263, CI [0.0447, 0.2089]) [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]. That sign flip is the A21 reason for Q2a and Q8, and it rests on one model pair, at the token level only. Tahimic and Cheng add that SAE directions trained on Gemma-2-2b base remain effective after instruction tuning (feature F1 0.821 base, 0.772 instruct, Sec 5.5), with no verbal readout [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]]. The reasoning residual's A21 reason is operational. Code-plus-confidence generation is hard to elicit jointly (Zeng et al. excluded code reasoning for that reason), and Miao and Ungar's reasoning contamination predicts that joint prompts degrade verbal discrimination [[interim-report-l2-residual-post-training-reasoning-format-on-code]] [[closing-the-confidence-faithfulness-gap-in-large-language-models]].

Committed reading: if a reviewer accepts these reasons, Q2a, Q2b, and Q4 are NARROW and form a second contribution conditional on outcome α. If the reviewer rejects them, they are OCCUPIED by analogy, and the paper should present them as a replication of general-NLP directions on code, which TMLR does not penalize as long as they are not claimed as novel. Either way, they belong after the controlled test, never before it. Decomposing a gap that has not been shown to exist under controls would partition noise.

## 4. L3: Verification utility and confidence updating

### 4.1 Routing: positives and negatives use different gates and different budget units

The positive code results all gate with a trained or proxy signal.

- **Heteroskedastic signals (concurrent).** It replays MBPP with a logit-margin proxy and reports Random .551, Threshold .636, CST .671, and Oracle 1.00 at β=10%, after adding "10% Bernoulli label noise". The CST gain over thresholding has CI [−0.2, +7.0], and its oracle is the label itself [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]].
- **SWE-Verifier (concurrent).** It gates step-level sampling with a trained Qwen3.5-4B scorer: MiniMax-M2.7 moves from 75.47 ± 1.40 to 77.20 ± 0.87 at 1.09x cost, with 3.43% of steps verified, against 75.27 at 3.35x for all-step self-verification. Its "Oracle@3" (82.20 at 3.00x) is a best-of-three trajectory oracle, and it has no random gate (Table 1, Table 2) [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]].
- **Capability self-assessment.** It improves "over random routing by about 8.2 percentage points at matched cloud-call budgets", on math with a trained decision. Code appears only as transfer (Table 5 and 7) [[capability-self-assessment-in-large-language-models]].

The negative results use different budget units.

- **Give Up to Get More (concurrent).** Difficulty-proportional rules capture "at most 13%" of oracle gain on hard workloads even with true pass rates (CodeContests, Llama-3-8B, mean p 0.021, captures 1%). Thompson sampling helps only when the prior's rank correlation with outcome clears about 0.3 to 0.55. LLM-derived priors reach Spearman 0.10 to 0.46 and gain −2.1 to −0.1 against round-robin (Tables 1 and 3) [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]].
- **2608.14659 (concurrent).** Uncertainty-triggered regeneration lowers Pass@1 in 5 of 6 configurations, verbalized confidence has Pearson −0.327, −0.090, and −0.114 against correctness, and the held-out set is n=31 [[1introduction]].
- **Agent stopping.** Learned stopping beats matched random restarting by at most 1.98 pp, and only through allocation between tasks [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]].

Adjacent works stake out other parts of the space. Staged verification gives 11.64x throughput at 8.26% accuracy loss, but has no confidence-routed arm [[1introduction-3]]. CodeRefuser occupies risk-controlled abstention: at α=0.2 on MBPP with Qwen2.5-Coder-32B it abstains on about 30% of tasks, against over 80% for a perplexity baseline [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]. An ensemble cascade cuts FLOPs by 64.9% without random or oracle routing [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]].

**Reconciliation.** "Confidence gating helps" and "gating does not help" are both right, because they test different gate classes and budget units [[interim-report-l3-confidence-routed-execution-and-update-after-failure]]. Give Up supplies the quantity that joins them: a gate helps only if its within-pool rank correlation with outcome clears roughly 0.3 to 0.55 and the workload is not mostly hopeless. That makes L3 depend on S4 in a way that can be stated in advance. Under outcome α or β, an elicited or probe gate may clear the threshold in the middle pass-rate stratum. Under outcome γ, the replay is predicted to fail in the hard stratum, and confirming that prediction is a result. No occupant routes by elicited verbal or probe confidence against both a matched random arm and a label-sorted oracle at equal budget on unmodified execution labels, so the routing component is NARROW.

### 4.2 Updating after a shown failing test

This is the cleanest residual in the corpus. It is also the one most exposed to the failed full-text instrument. The nearest works never show the model a failing test.

- **Kaddour et al.** elicit stated success probability before, during, and after execution on SWE-bench Pro. Agents "develop 'cold feet': confidence decreases as they observe their partial work, but this doubt is uninformative, occurring equally for successes and failures". Mid-execution AUROC is about 0.53 for GPT, 0.49 to 0.64 for Gemini, and 0.62 to 0.52 for Claude. Yet the agent "cannot execute code, run tests" (Sec 2.2.1) [[agentic-uncertainty-reveals-agentic-overconfidence]].
- **XConf** builds confidence from graded past episodes across tasks, not from revision after a failure on the same program [[confidence-comes-from-experience-experiential-confidence-estimation-from-reasoni]].
- **Resist and Update** localizes confidence report coordinates by interchange intervention, finds confidence "a weaker instrument" than answer and caveat coordinates, and gives the evidence-versus-pressure design. It is non-code [[260712985-resist-and-update-counterfactual-report-coordinates-full-text]].
- **Iscan's** preregistered placebo design shows "blind resampling beat bare-code retry by +18 net unlocks" (p=0.0021), and it never elicits confidence [[falsification-not-exposure-placebo-controlled-decomposition-of-self-repair-feedb]].

The A21 reason here is the strongest in the whole study. Code is the domain where the evidence shown to the model can be made executable and verifiable, and where a spurious failure can be built deliberately by mutating a test. A QA setting cannot offer a valid-versus-spurious failure contrast with ground truth. The verdict is CLEAN (provisional). Under S2, though, it is the most fragile CLEAN in the study, because such a measurement could sit as one paragraph inside an agent or self-repair paper, invisible to the title and abstract search that worked. Forward screens of 2611.06372, 2610.30284, and 2608.14659 were not run [[interim-report-l3-confidence-routed-execution-and-update-after-failure]].

### 4.3 Conditions and committed reading

L3 is the candidate most sensitive to S1. Every routing positive and the main negative are concurrent (Heteroskedastic, SWE-Verifier, SWE-Router, Give Up, and 2608.14659). With concurrent work excluded, the routing component moves from NARROW toward CLEAN (provisional), and the nearest pre-window works are staged verification and ensemble cascades without random arms. That makes L3 look like the cleanest candidate exactly when the operator's window is strict. It does not make it the strongest. Its claims-evidence fit depends on the readout quality that L2 measures, so it cannot stand without L1 and L2. Committed reading: L3 is NARROW and a secondary analysis on the same generations, with an honest negative in the hard stratum as an expected, publishable outcome. The update-after-failure test is a small, hedged probe whose novelty claim must be written as "we found no prior measurement" with the instrument gaps named.

## 5. L4: Per-requirement confidence and localization

### 5.1 What is occupied

Line and token localization from model signals against execution-derived labels is OCCUPIED by Gros and Devanbu, a preprint first posted 2025-12-31, so not concurrent. On Qwen2.5-Coder-7B-Instruct at line level (Table 4), token probability has BSS −1.18, ECE 0.54, and AUC 0.55; multisampling 0.01, 0.17, and 0.72; line-verbalized confidence −0.72, 0.43, and 0.71; and Probe-7B 0.29, 0.08, and 0.83 [[localized-calibrated-uncertainty-in-code-language-models]]. The probe-over-verbal ordering reproduces at sub-solution granularity. But for GPT-4o, the "probe" reads a 0.5B or 7B supervisor's hidden states, so it is an external reader, not GPT-4o's own internal state. The authors also admit "the lack of a clean heldout test set" (Sec 10.2), and leave-one-dataset-out results degrade sharply (Table 7) [[interim-report-l4-localization-occupancy-and-targeted-repair]].

Targeted repair has occupants too. TokenRepair fixes 88 bugs on Defects4J 1.2 and 139 on HumanEval-Java, with token-localization Top-K accuracy of 0.589 to 0.695, and removing uncertainty-guided localization costs 20.6% [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]]. FLARE (concurrent) gains 1.72 to 7.42% absolute pass@1 over NL-Debugging [[interim-report-l4-localization-occupancy-and-targeted-repair]]. Two neighbors bound what token signals can do. Highlighting by generation probability "does not provide any benefit over the baseline with no highlighting", while highlighting by an edit model does [[generation-probabilities-are-not-enough-uncertainty-highlighting-in-ai-code-comp]]. Outside code, a calibrated correctness probe misses 81% of single-step unrecoverable failures, and no probe beats a trace-length rule at localizing the failing step [[effectiveness-of-hidden-state-probesfor-localizing-reasoning-failures]].

### 5.2 What survives, and the conditions

Three residuals survive.

- **Per-test-group confidence as failing-requirement localization.** It is NARROW. The A21 reason is medium-strength: tests cluster by requirement, the unit needs no patch oracle, and wrong-oracle rates in LLM-written tests (15.6% of failures) point to label noise at the test level.
- **Confidence-guided targeted repair against matched-budget regeneration.** It is NARROW. Olausson et al. find "pass rates are higher or equally high with i.i.d. sampling (without repair), especially when the budget is small", and the targeted-repair papers omit the matched resampling arm [[is-self-repair-a-silver-bullet-for-code-generation]] [[falsification-not-exposure-placebo-controlled-decomposition-of-self-repair-feedb]].
- **Adequacy of self-written tests against the model's own confidence.** It is CLEAN (provisional). ACES weights LLM-written tests by leave-one-out AUC from the pass matrix, with no confidence calibration [[aces-who-tests-the-tests-leave-one-outauc-consistency-for-code-generation]].

L4 is stable under S1, because its occupants are mostly pre-window. It is sensitive to S2 only for test adequacy. What blocks it is not the literature but readiness: the per-test pipeline in `src/v4_dprc` is frozen legacy code, never run beyond a stub. Committed reading: L4 is NARROW and last in rank. The paper should cite Gros and Devanbu as the line-level occupant and name the test-group unit as untested future work.

## 6. F: Measurement-instrument framing

F is the one candidate whose verdict does not move under any switch. Every quantity the framing would introduce maps onto an existing one [[interim-report-f-metrology-residual-quantity]].

- **Readout bias** is calibration-in-the-large in the Yates covariance decomposition, or the SDT criterion.
- **Readout resolution relative to an internal reference** is a difference of Murphy resolutions. Ghosh et al. already report it as behavioral 0.06371, verbal 0.03160, and probe 0.05154 (a 2.02x ratio). It can also be read as Charpentier and Fernandes Machado's grouping term with the probe as reference.
- **Cross-format noise** is already reported as pairwise Spearman correlations of 0.126, −0.069, and 0.247 across three verbal formats, and as AUPRC spread under paraphrase (Mahaut et al.).
- **Metacognitive efficiency** is covered by meta-d' and the model-free meta-I, and M-ratio is undefined for open-ended code generation.

The circularity argument decides the case. On code, the internal reference is a probe trained on the same execution labels it is meant to referee, so any quantity "relative to internal state" collapses into a contrast of two ordinary resolutions. The one quantity outside Murphy (an item-by-format variance component) has no stated code reason to differ, so it fails A21.

S2 bears only on vocabulary. Metrology-proper terms (GUM uncertainty budget, traceability) applied to LLM confidence are CLEAN (provisional), but vocabulary that no one uses is not a contribution. Measurement-validity and construct-validity framing is already applied to coding agents, with submit rates against resolve rates (GPT-5 100% against 44%) [[confident-and-wrong-silent-semantic-failures-in-coding-agents]]. A calibrated invariance audit of 30.73 million executed generations already uses within-task randomization against an exchangeability null [[identity-or-prompt-noise-a-calibrated-invariance-audit-of-llm-code-generation]]. That audit design is the right template for one L2 nuisance factor: whether a format effect on stated confidence exceeds what prompt-wording noise alone produces. It is a design borrowing, not an F contribution. Committed reading: F is OCCUPIED as a framing. Its vocabulary ("readout", "measurand") is usable as exposition inside L2, together with Murphy terms and meta-I.

## 7. Close occupants

The table gives each close occupant's status tag, what it occupies, and the switch its weight depends on. Dossier-level breadth matrices exist for every row.

| Work | Status (A23) | Occupies | Leaves open | Sensitive to |
|---|---|---|---|---|
| Ribeiro et al. 2512.07404 [[on-llms-internal-representation-of-code-correctness]] | Published, ICSE 2026 | Probe beats zero-shot verbal and likelihood, whole solution, four 7-8B instruct models (Sec 4.2.1) | Calibration metrics, sampling, base and instruct pairs, reasoning, release split, causal intervention, sub-solution granularity | None; robust under all switches |
| Ribeiro et al. follow-up 2608.08266 [[on-the-robustness-of-llms-internal-representation-of-code-correctness]] | Concurrent | Probe robustness across extraction choices; "no single configuration is best" | Any verbal variation | S1 (weight as an occupant); evidence for the provenance confound either way |
| Campos, Klassert, and Ulges 2611.07876 [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] | Concurrent (2026-11-05) | Probe, LAT, output confidence, EigenScore, causal; pooled versus within problem; shift | Verbal numeric confidence, base and instruct, reasoning-on probe, ECE | S1 strongly; it is both the occupant of L2 Q13 and the strongest evidence for a small controlled gap |
| Di Cicco 2606.14530 [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]] | Concurrent (preprint, first posting June 2026 per arXiv id) | Pre-generation probe on one model (AUC 0.881) | Within-problem signal (k=1), verbal comparison | S1 |
| Silva, Tu, and Monperrus 2607.05188 [[interim-report-l4-localization-occupancy-and-targeted-repair]] | Concurrent | Step-level probes in agents, including a partial-correctness label | Verbal comparison, test-group unit | S1 |
| NeuroSym-Cal [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]] | Published, Findings of ACL 2026 (vault note ABSTRACT-ONLY; dossier on full PDF) | Token, P(True) and self-verification, sampling, multicalibration; per-model post-cutoff subset (Sec 4.1) | Probe family, base and instruct, reasoning toggle | The definitional switch on what counts as stated confidence |
| Tuerlings and Valdenegro-Toro [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]] | Published, UncertaiNLP 2026 | Verbal formats on code; shared post-cutoff window; ECE and AUROC decoupling (Table 1) | Non-verbal families, per-model split, pre-cutoff contrast | None |
| Rathnasuriya and Yang 2610.11300 [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]] | Concurrent | Token-level overconfidence; base and instruct at token level (Sec 5.5); recalibration control (Table 5) | Verbal, probe | S1 and S3 (its sign flip is the A21 reason) |
| Gros and Devanbu 2512.24560 [[localized-calibrated-uncertainty-in-code-language-models]] | Preprint only (2025-12-31) | Line and token localization across four families with BSS, ECE, and AUC (Tables 3-4) | Test-group unit, repair against regeneration, program-level four-family comparison | The definitional switch on granularity |
| Miao and Ungar 2603.25052 [[closing-the-confidence-faithfulness-gap-in-large-language-models]] | Preprint only | Probe versus verbal, base and instruct, causal steering, outside code | Code, execution labels, AUROC | S3 (it is the NLP side of every factorial residual) |
| Liu et al. 2609.25938 [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]] | Concurrent | Oracle dependence of reported risk and of consistency scores, SQL | Code generation, families beyond consistency | S1 and S3 |
| CodeRefuser 2605.17029 [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]] | Concurrent (submitted 2026-05-16, six days inside the window) | Risk-controlled abstention on code | Routing against random and oracle | S1; L3 Q3 then rests on 2505.13553 and 2605.19369 |
| Heteroskedastic signals, SWE-Verifier, Give Up [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]] [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]] [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]] | All concurrent | Routing comparators (random, threshold, oracle) with proxy or trained gates; pass-rate priors | Elicited or probe gate, unmodified labels, attainable oracle | S1 strongly |
| Kaddour et al. 2602.06948 [[agentic-uncertainty-reveals-agentic-overconfidence]] | Preprint only (February 2026) | Stated confidence before, during, and after execution in agents | A shown failing test (read-only access) | S2 |

An independence caveat applies when counting occupants. The Devanbu and Nadi groups appear in Ribeiro, its follow-up, and Gros and Devanbu, so "three papers find probes beat verbal on code" is closer to one research line than three. Campos et al. and the Klassert thesis share an author. Counting groups rather than papers makes the "probe beats verbal" camp smaller than its citation count suggests, which strengthens the case for running the controlled test.

## 8. Verdict table

The table gives the verdict per component under the working settings (concurrent work counts; gaps are gaps; A21 reasons accepted), followed by the verdict under each changed switch. A dash means no change. "Prov." stands for CLEAN (provisional).

| Candidate and component | Verdict (working) | If concurrent excluded (S1) | If A21 rejected (S3) | Gap exposure (S2) | Evidence location |
|---|---|---|---|---|---|
| L1 Q1 four families, execution labels | OCCUPIED (union) | Stays OCCUPIED (union): Ribeiro plus NeuroSym-Cal | - | None | NeuroSym-Cal Sec 3, 4.2 [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]]; Ribeiro Sec 4.2.1 [[on-llms-internal-representation-of-code-correctness]]; Campos Sec IV |
| L1 Q2 breadth (3+ families, 2+ scales, 3+ benchmarks) | NARROW | - | - | None | NeuroSym-Cal Sec 4.1 [[neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc]] |
| L1 Q3 release split for calibration | NARROW | - | Becomes OCCUPIED only if the memorization reason is rejected | Low | Tuerlings Sec 3.1 [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]]; NeuroSym-Cal Sec 4.1 |
| L1 Q4 label independence as a tested factor | NARROW | Toward Prov. | - (strong reason) | Medium | Tuerlings Sec 3.3; Liu abstract, Sec 1 [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]] |
| L1 Q5 ranking changes with estimator | NARROW (fact); Prov. (estimator variants) | - | Toward OCCUPIED (method hygiene) | High for variants | Tuerlings Table 1, Sec 4.3, 4.6 [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]] |
| L1 Q6 recalibration as a control | OCCUPIED (token, line); NARROW (across families) | - (Gros is pre-window) | - | None | Rathnasuriya Table 5 [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]; Gros Tables 3-4 [[localized-calibrated-uncertainty-in-code-language-models]] |
| L1 Q7, Q8 test-free agreement, execution clustering | OCCUPIED | - | - | None | [[code-is-more-than-text-uncertainty-estimation-for-code-generation]]; [[using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation]]; [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]] |
| L1 Q10 test insufficiency changes rankings | Prov. | - | - | High | EvalPlus, accuracy only [[is-your-code-generated-by-chatgpt-really-correct-rigorous-evaluation-of-large-la]] |
| L1 Q13 contamination changes calibration | Prov. | - | Medium | Low to medium | None found [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]] |
| L2 Q1 probe versus own readouts, uncontrolled | OCCUPIED | - | - | None | Ribeiro Sec 4.2.1 [[on-llms-internal-representation-of-code-correctness]] |
| L2 Q1c controlled (supervision-matched, input-only baselines, within problem, self-generated) | NARROW | Stays NARROW (wider residual) | - (label-protocol reason) | Low | Ribeiro Sec 4.1.1-4.1.2; Campos Table V, Sec VI-C [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] |
| L2 Q2a base versus instruct | NARROW | Stays NARROW (code side drops to Tahimic) | OCCUPIED by analogy | Medium | Rathnasuriya Sec 5.5; Tahimic Sec 5.5 [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]]; Miao and Ungar Sec 3.1 [[closing-the-confidence-faithfulness-gap-in-large-language-models]] |
| L2 Q2b reasoning on versus off, same weights | NARROW | - | OCCUPIED by analogy | Medium | Campos Sec V-A, VIII [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] |
| L2 Q3 elicitation format | OCCUPIED (within verbal); NARROW (format by readout) | - | Interaction becomes OCCUPIED | Low | Tuerlings Table 1 |
| L2 Q4 where the gap arises | NARROW | - | OCCUPIED by analogy (gap present in base, NLP) | Medium | Miao and Ungar Sec 3.1, 3.3 |
| L2 Q5-7 probes, transfer, other white-box readouts | OCCUPIED | - | - | None | Ribeiro; 2608.08266 Table II [[on-the-robustness-of-llms-internal-representation-of-code-correctness]]; Tahimic Sec 5 |
| L2 Q8 post-training stages, execution labels | NARROW (weak) | - | OCCUPIED | Medium | Trained-on-tokens Fig 2, non-code [[trained-on-tokens-calibrated-on-conceptsthe-emergence-of-semantic-calibration-in]] |
| L2 Q9 trace signals beat the final number on code | Prov. | - | - | High | None found |
| L2 Q10 probing reasoning models, reasoning on | NARROW | - | - | Medium | RLCM LCB column, ECE only [[interim-report-l2-residual-post-training-reasoning-format-on-code]] |
| L2 Q11 trained stated confidence on code, discrimination | Prov. | - | - | High | None on code; Probe-SD, RLCR outside code |
| L2 Q12 causal intervention on stated confidence | NARROW | - | - | Low | Tahimic Sec 5, Fig 8; Miao and Ungar Table 4 |
| L2 Q13 pooled versus within problem | NARROW | Toward Prov. | - | Low | Campos Sec VI-C; 2610.05572 [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]] |
| L3 Q1/Q4/Q5 routing by elicited or probe confidence against random and oracle | NARROW | Toward Prov. | - (low pass-rate reason) | Medium | Heteroskedastic Table 1 [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]]; SWE-Verifier Tables 1-2; Give Up Tables 1, 3 [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]] |
| L3 Q2/Q7 update after a shown failing test, valid versus spurious | Prov. | - | - (strongest reason) | Highest | Kaddour Sec 2.2.1, Table 1 [[agentic-uncertainty-reveals-agentic-overconfidence]] |
| L3 Q3 selective prediction with coverage on code | OCCUPIED | Toward NARROW (rests on 2505.13553) | - | None | CodeRefuser Table 1, Figs 2-3 [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]] |
| L3 Q6 repository-agent uncertainty | OCCUPIED (union) | Toward NARROW (Kaddour remains) | - | None | SWE-Verifier [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]]; Kaddour |
| L4 Q1 per-test-group localization | NARROW | - | OCCUPIED by line-level analogy | Medium | Gros Sec 4, Tables 3-4 |
| L4 Q2 targeted repair against matched regeneration | NARROW | - | - | Low | Olausson Sec 4 [[is-self-repair-a-silver-bullet-for-code-generation]]; TokenRepair ablation [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]] |
| L4 Q3 self-written test adequacy against own confidence | Prov. | - | - | High | ACES, no confidence [[aces-who-tests-the-tests-leave-one-outauc-consistency-for-code-generation]] |
| L4 Q4 line, token, edit, step localization | OCCUPIED | - | - | None | Gros Tables 3-4 [[localized-calibrated-uncertainty-in-code-language-models]]; TokenRepair Table 1 |
| F Q1 metrology vocabulary | OCCUPIED (validity terms); Prov. (metrology-proper) | - | - | Low (no stakes) | 2610.25846; Confident and Wrong [[confident-and-wrong-silent-semantic-failures-in-coding-agents]] |
| F Q2 bias, resolution, noise decomposition | OCCUPIED (union) | - | - | None | Yates; Charpentier; Ghosh [[interim-report-f-metrology-residual-quantity]] |
| F Q3 A24 residual quantity | OCCUPIED (effective) | - | Already fails | None | Ghosh Table 2; Mahaut |
| F Q4 meta-d' | OCCUPIED | - | - | None | Servajean; Cacioli [[interim-report-f-metrology-residual-quantity]] |

Whole-candidate verdicts:

- **L1:** OCCUPIED (union) as a comparison and NARROW as a protocol, under all switch settings.
- **L2:** OCCUPIED as a headline, and NARROW as a controlled test under all switch settings. The factorial versions are NARROW only if A21 is accepted.
- **L3:** NARROW, moving toward CLEAN (provisional) if concurrent work is excluded.
- **L4:** NARROW.
- **F:** OCCUPIED as a framing.

No component the recommendation rests on becomes OCCUPIED under any setting of S1 or S3.

## 9. Ranked recommendation for TMLR

### 9.1 Rank 1: the controlled disconnect test on an L1 measurement layer

**Contribution sentence.** On self-generated, execution-graded code, the paper tests whether a hidden-state probe carries correctness information that the model's own readouts do not. The own readouts are numeric and categorical stated confidence, token probability, and per-candidate sampling agreement, each also given a trained version fit on the same labels. The test is run with input-only baselines and scored both pooled and within problem. Its rankings are recomputed under an estimator set, an oracle swap from base to augmented tests, and a release-date split.

**When it is strongest.** Under every switch setting. It is the only candidate whose residual is a label protocol rather than a contested factor, so S3 cannot remove it. Its closest occupants are published (Ribeiro) or concurrent (Campos), so S1 only changes how wide the residual is. S4 changes the headline, not whether there is a paper (section 3.5).

**Evidence it must generate to be defensible either way:**

1. **Multiple samples per problem.** At least 10 per problem, so that lambda in Bulut's Eq. 1 is not zero, and enough mixed problems to resolve within-problem differences near 0.05 [[its-the-problem-not-the-pathbudget-and-difficulty-confounds-in-llm-reasoning-tra]]. The wave's working floor is at least 100 mixed problems for the claim, and about 400 or more problems per cell to resolve base-versus-instruct effects near 0.05. That floor follows from Rathnasuriya's OpenCoder ΔAUC interval [−0.0911, 0.0652] [[interim-report-l2-residual-post-training-reasoning-format-on-code]]. The fraction of problems that are mixed depends on pass rate: at per-problem pass rate p and k samples it is 1 minus p^k minus (1 minus p)^k. This is an illustrative formula, not a measured number. Hard benchmarks with pass rates of 8 to 30%, like Tuerlings' window, will therefore need more problems.
2. **A supervision-matched own readout.** A logit-feature head or a trained verbal head fit on the same execution labels, with validation-based checkpoint selection for every fitted reader. Without it, a reviewer can cite Probe-SD and RLCR to say the gap closes, or the estimator-overfitting result to say it does not [[interim-report-l2-residual-post-training-reasoning-format-on-code]].
3. **Input-only baselines.** A prompt-only probe (Campos et al.'s last-prompt-token probe has pooled 0.891 and within-problem 0.514) and a candidate-text-only classifier, so that difficulty and surface style are measured, not assumed away [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]].
4. **A provenance check on the occupant.** A sign-reversed or fitted likelihood baseline on Ribeiro's public data, to test whether the reference-versus-other-model design explains part of the +13.3 to +29.0 pp [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]].
5. **The measurement layer.** Rankings under equal-width, equal-mass, and debiased or smooth ECE, Brier skill with reliability intervals, AUROC, and AURC. Base-test versus augmented-test labels. A per-model pre- versus post-cutoff split using LiveCodeBench windows. Sampling-agreement scores built only from tests disjoint from the label suite [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]] [[livecodebench-holistic-and-contamination-free-evaluation-of-large-language-model-2]].
6. **Problem-clustered paired bootstrap** for every difference, with AUROC reported beside BSS for every recalibrated readout, because monotone maps cannot change AUROC [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]].

**TMLR fit.** Claims-evidence: the claim matches what the paper generates, and it holds whichever way the test comes out. Audience interest: probing, calibration, and code-evaluation readers, plus anyone who reports pooled AUROC for code correctness. **Main risk:** an occupant appears behind the S2 gaps, most plausibly a 2026 code paper with a trained verbal arm reported in AUROC. **Mitigation:** write the novelty sentence as "we found no prior code study that" and name the instrument gaps.

### 9.2 Rank 2: L3 as an offline routing replay on the same generations

**When it is strongest.** When S1 excludes concurrent work (routing moves toward CLEAN (provisional)) and S4 returns α or β, so that the gate's within-pool rank correlation can clear the 0.3 to 0.55 break-even [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]]. **When it is weakest.** Under outcome γ, a positive result is unlikely. The replay is then still worth reporting as a tested prediction ("gates fail when mean pass rate is below about 0.1"). **Evidence it must generate:** random and label-sorted oracle arms at equal budgets of 10, 20, 30, and 50%, with 10 or more seeds; paired gains with 95% CIs, given that the closest occupant's single-point gain has CI [−0.2, +7.0]; stratification by pass rate; and no injected label noise [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]] [[interim-report-l3-confidence-routed-execution-and-update-after-failure]]. **TMLR fit:** adds utility to the Rank 1 paper; too thin alone.

### 9.3 Rank 3: stated-confidence update after a shown failing test

**When it is strongest.** If S2 is read optimistically and the forward screens of the three closest L3 occupants are completed without a hit. It has the strongest code-specific A21 reason of any component, since failures can be made valid, spurious, or placebo by construction. **Evidence it must generate:** paired programs with a genuine failing test, a spurious failure (an executed test that is wrong), and a placebo, following the evidence-versus-pressure design of Resist and Update and the placebo logic of Iscan; the change in stated confidence; and that change's AUROC against repair success [[260712985-resist-and-update-counterfactual-report-coordinates-full-text]] [[falsification-not-exposure-placebo-controlled-decomposition-of-self-repair-feedb]]. **Main risk:** the highest S2 exposure in the study. It fits best as a hedged section of the Rank 1 paper.

### 9.4 Rank 4: L4, and F as exposition

L4 is strongest only if the operator decides to run the v4 per-test pipeline. Even then, it is a repair-method comparison more than a calibration claim, and the matched-budget protocol already exists [[is-self-repair-a-silver-bullet-for-code-generation]]. F should appear only as vocabulary inside L2, with Murphy terms and meta-I reported and no novelty claimed [[interim-report-f-metrology-residual-quantity]].

### 9.5 If the switches go against the paper

Suppose a hidden occupant appears behind the gaps and the operator rejects A21. Then the brief's all-occupied fallback applies only to the factorial and routing components. The Rank 1 controlled test would still be a claims-reduced study with a correct-by-construction design. Under TMLR's rubric, that is acceptable if it does not claim novelty over published work it overlaps with.

### 9.6 Looking ahead

The field is moving fast, and it is moving toward the controls this paper would run. Between August and November 2026, three papers on code models or coding agents started reporting within-problem discrimination or difficulty references (Campos et al., and the disentangling and hard-issue agent studies), and a text-to-SQL study named oracle dependence as a design rule ("A consistency score should be evaluated under an oracle that did not build it") [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]] [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]] [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]] [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]]. Two implications follow. First, the window for the controlled test is real but short. A group already holding Campos-style infrastructure needs only a trained own-readout arm to occupy Rank 1, so speed of submission is itself a positioning variable. Second, if outcome γ holds, the probe-for-code-correctness literature will have to re-report its pooled numbers as between-problem difficulty detection, and a paper that supplies the decomposition and the measurement layer becomes a reference point for that correction. Under outcome α, the same infrastructure feeds the factorial location study and probe-gated execution budgets, which then get a measured gate quality instead of an assumed one. Either way, the measurement layer outlives the headline.

## 10. Instrument gaps

The wave's instrument validation sets the epistemic ceiling: no CLEAN verdict is unconditional, and every claim that would need body-text search is at best CLEAN (provisional) [[interim-report-l1-estimator-and-label-oracle-sensitivity-with-contamination-cont]] [[interim-report-l3-confidence-routed-execution-and-update-after-failure]].

| Gap | What failed | Verdicts it bears on |
|---|---|---|
| G-FT | arXiv full-text search failed validation: `searchtype=ft` is silently ignored, and `full_text` redirects off the allowlist | Every CLEAN (provisional): L1 Q5 variants, Q10, Q13; L2 Q9, Q11; L3 Q2/Q7; L4 Q3; F Q1 metrology terms |
| G-OA | OpenAlex full text found 1 of 2 known positives, and the daily budget ran out at about 05:05 IST, so later OpenAlex negatives are gaps | Same set, plus late forward screens |
| G-S2 | Semantic Scholar keyword search returned HTTP 429 throughout; lookups and citations worked intermittently | Keyword recall for all candidates |
| G-AX | The arXiv export API returned HTTP 429 to several queries, including within-problem probe queries and L3 queries [[interim-report-probe-advantage-real-or-difficulty-confound-on-code]] | L2 Q1c, Q13; L3 |
| G-OR | OpenReview forum pages and PDFs sit behind a browser challenge; only v1 search works | OpenReview-only full texts, concentrated in ML-venue submissions |
| G-FCS | Forward screens incomplete: 2611.06372, 2610.30284, 2608.14659, and 2607.00053 not screened; only 4 citers of 2512.24560 [[interim-report-l4-localization-occupancy-and-targeted-repair]] | L3 Q1, Q2/Q7; L4 Q3 |

How exposed each CLEAN (provisional) is depends on where an occupant would report the result, because metadata search worked and body-text search did not. Results that would be a paper's main claim are lower risk: contamination changing calibration (L1 Q13), or trained verbal confidence on code as a title topic. These would likely appear in titles or abstracts, which the passing instruments cover, subject to the OpenAlex and arXiv rate limits. Results that would be one experiment inside a larger paper are high risk: an estimator-variant appendix (L1 Q5), a confidence-revision paragraph in an agent study (L3 Q2/Q7), a LiveCodeBench column in a math-training paper (L2 Q11, as RLCM shows), or a test-adequacy analysis in a test-generation paper (L4 Q3). Every high-exposure item is a sub-experiment, not a headline. That is the main reason this draft ranks the controlled test (low exposure) above the update-after-failure test (highest exposure), even though the latter has the stronger A21 reason.

Before submission, the paper must close what it can: rerun the incomplete forward screens once the rate limits reset, and repeat the keyword set on OpenAlex within a fresh budget. Every novelty sentence that rests on a body-text negative must be written with the gap named, as the brief requires.
