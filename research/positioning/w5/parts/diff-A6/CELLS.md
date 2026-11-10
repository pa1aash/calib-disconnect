# Differential table, cell evidence (A6)

Run date 2026-11-10. Every cell was read in full text (sources and statuses in `raw/PROVENANCE.md`). Codes: **P** present (the paper implements the control as defined), **Pa** partial (a related or weaker version), **A** absent. For every A, the evidence line names the terms searched in the full text.

Columns:

- **Ribeiro**: Ribeiro, Spiess, Devanbu, and Nadi, arXiv 2512.07404 (ICSE 2026).
- **Campos**: Campos et al., arXiv 2611.07876.
- **CREDO**: arXiv 2609.34857.
- **Spiess**: Spiess et al., arXiv 2402.02047.
- **NeuroSym**: NeuroSym-Cal, Findings of ACL 2026, pp. 6132-6143 (wave 4 local full text; no arXiv version found).
- **RLCM**: arXiv 2604.23333.

## 12 x 6 table

| # | Control | Ribeiro | Campos | CREDO | Spiess | NeuroSym | RLCM |
|---|---|---|---|---|---|---|---|
| 1 | Supervision-matched readouts | A | Pa | Pa | Pa | A | Pa |
| 2 | Trained stated-confidence readout | A | A | P | A | A | P |
| 3 | Prompt-only baseline | A | P | A | A | A | A |
| 4 | Code-text-only baseline | Pa | A | A | Pa | Pa | A |
| 5 | Within-problem scoring | P | P | A | A | A | Pa |
| 6 | Oracle swap of test suites | A | A | A | Pa | A | A |
| 7 | Release or contamination split | A | A | A | A | Pa | A |
| 8 | Calibration estimator set | A | A | A | Pa | A | A |
| 9 | Clustered paired inference | Pa | P | A | A | A | A |
| 10 | Base versus instruct | A | A | A | A | A | A |
| 11 | Same-weights reasoning on/off | A | Pa | A | A | A | A |
| 12 | Routing replay (random and oracle comparators) | A | A | Pa | A | Pa | Pa |

## Per-cell evidence

### Row 1. Supervision-matched readouts (all readouts trained or calibrated on the same execution labels and splits)

- **Ribeiro, A.** LAT is fit on 10% of tasks with labeled correct/incorrect pairs; intrinsic and reflective readouts are never fit; RankEF is trained on 5,000 APPS tasks, not the study labels. Location: Sec 4.1.2, Table 2, Sec 5.1.3.
- **Campos, Pa.** Probe, LAT, DAS, and value probe share the same 60/20/20 problem splits and execution labels; the confidence readout (Yes-token probability) is only temperature-tuned, with no label-trained head. Location: Sec V-A "Splits", Sec V-B "Fitting" and "Selection", Sec IV-A.
- **CREDO, Pa.** GRPO, RLCR, DCPO, and CREDO are all trained on DeepCoder with the same verifier, seeds, and schedule, but each readout is co-trained with its own policy (different generations), the untrained Base is included, and there is no probe. Location: Sec 4.1 "Baselines and training", Table 4 (App B.2), Table 1.
- **Spiess, Pa.** Every confidence measure (token probabilities, Ask T/F, verbalized, length) is Platt-scaled with five-fold fitting on the same correctness labels; this is a two-parameter monotone map, sharing of folds across measures is not stated, and no readout is trained beyond it. Location: Sec III-D, Table IV.
- **NeuroSym, A.** The CCN is trained on a disjoint APPS plus older-LCB corpus; P-True and Self-Consistency are untrained; the fit data for Platt Scaling and IGLB are not stated (searched "Platt", "fit", "training set"). Location: Sec 4.1 "Training Data and CCN Implementation", Sec 4.2, p. 6137.
- **RLCM, Pa.** All methods start from R1-Distill-Qwen-7B with "identical data, hyperparameters, and probe-training protocol"; probes for Base and GRPO are fit post hoc on 80 GRPO-LEAD problems with forced-answer Monte Carlo targets, while RLCR's verbal and C2GSPG's logit readouts come from separately trained policies; code (LCB) is out of domain for all. Location: Sec 4.1 "Baselines", App B.

### Row 2. Trained stated-confidence readout (fine-tuned or RL verbal confidence)

- **Ribeiro, A.** Reflective readouts are prompted only (seven-level and True/False); searched "fine-tun", "trained" (hits refer to RankEF and LAT). Location: Sec 2.3, Sec 6.2.
- **Campos, A.** Only a prompted Yes/No token probability; no numeric verbal readout; searched "verbal", "fine-tun". Location: Sec III-A, Sec IV-A.
- **CREDO, P.** RLCR and DCPO train a verbalized numeral via RL reward, and CREDO trains a two-token confidence readout by regression, all on code execution labels; code AUROC 0.815 (RLCR), 0.776 (DCPO), 0.850 (CREDO) versus 0.690 (Base). Location: Sec 2.2, Sec 3, Table 1.
- **Spiess, A.** Verbalized and Ask T/F are zero-shot or few-shot in context; fine-tuning is named as future work. Location: Sec III-B, Sec IV-D (closing sentence), Table V.
- **NeuroSym, A.** P-True and the 0 to 100 self-verification score are prompted at T=0; the self-verification score is a feature fed into the trained CCN, not a trained verbal readout. Location: Sec 3.2, Sec 4.1, Sec 4.2.
- **RLCM, P.** RLCR (Brier-style reward on verbalized confidence) is RL-trained on the same base and data and evaluated on LiveCodeBench against probe readouts (RLCR LCB ECE .218 versus RLCM probe .051). Location: Sec 4.1 "Baselines", Table 1 (bottom panel).

### Row 3. Prompt-only baseline

- **Ribeiro, A.** Searched "prompt only", "problem only", "difficulty" (difficulty hits describe benchmarks only). Location: Sec 4.1.1.
- **Campos, P.** A probe on the hidden state at the last prompt token, "before any code exists", matches the judging pass in distribution for Qwen3-Coder (pooled 0.891 versus 0.886). Location: Sec VI-C "Reading the generation is as good as asking", Table V.
- **CREDO, A.** Searched "prompt-only", "difficulty", "per-problem"; the prompt-level accuracy appears only in the Bayes-optimal target (Proposition 3), not as a baseline. Location: Sec 3.2.
- **Spiess, A.** The "Unskilled" row is a constant base-rate predictor, not a prompt-conditioned one; searched "prompt only", "difficulty". Location: Sec III-C, Table III.
- **NeuroSym, A.** No baseline conditioned on the problem alone (searched "prompt", "difficulty", "problem-level"). Location: Sec 4.2.
- **RLCM, A.** Searched "prompt-only", "difficulty" (hits describe benchmark difficulty). Location: Sec 4.1 "Datasets".

### Row 4. Code-text-only baseline (classifier on candidate code text, no model internals)

- **Ribeiro, Pa.** RankEF, a CodeT5+ ranker fine-tuned on APPS with execution feedback, ranks candidates from the code (no generator internals), but it uses a different model's encoder and different training data. Location: Sec 5.1.3, Tables 5 and 6, Sec 6.2.
- **Campos, A.** All predictors read the generating model's states or outputs; the "last code token" probe still reads internals; searched "text-only", "TF-IDF", "CodeBERT". Location: Sec IV, Table V.
- **CREDO, A.** Searched "text-only", "TF-IDF", "CodeBERT", "length" (zero hits in the body). Location: Sec 4.1.
- **Spiess, Pa.** A length baseline (character count of the generated code, min-max scaled) is reported beside every readout; it is a single feature, not a trained classifier. Location: Sec III-B, Tables III and IV.
- **NeuroSym, Pa.** Code length, reasoning length, and cyclomatic complexity enter the CCN, and the IGLB baseline groups by complexity and length, but no metadata-only classifier is reported (ablations remove Sintr, Sext, or AST only). Location: Sec 3.4, Sec 4.2 III, Table 2.
- **RLCM, A.** Searched "text-only", "length", "classifier". Location: Sec 4.1.

### Row 5. Within-problem scoring

- **Ribeiro, P.** RQ2 ranks each model's own 10 samples per task and reports pass@rank-k (selection among samples of one problem); RQ1 selects among four candidates per task. Location: Sec 4.1.3, Sec 5.1.1, Sec 5.1.3, Tables 5 and 6.
- **Campos, P.** Within-problem AUROC over same-problem pairs with different labels, beside pooled AUROC (e.g., 0.58 to 0.64 under language shift). Location: Sec V-C "Metrics", Fig 3, Table V, Sec VI-C.
- **CREDO, A.** Four samples per code problem at evaluation, but only pooled ECE, AUROC, Brier, and AURC are reported; searched "within", "per-problem" (hits refer to GRPO groups). Location: App B.3, Table 5 (datasets).
- **Spiess, A.** Temperature 0, one generation per problem; searched "within" (the two hits concern rescaling across tasks). Location: Sec III-F.
- **NeuroSym, A.** K=10 samples per problem feed consensus, but all metrics are pooled; within-problem re-ordering is mentioned only qualitatively. Location: Sec 4.1, Sec 5.1 "Discriminative Power".
- **RLCM, Pa.** Confidence-weighted voting among rollouts of the same question, with majority and oracle comparators, framed as "within-question ordering"; reported for math benchmarks (AIME24/25, OlympiadBench, MATH-500), with LiveCodeBench not named. Location: Sec 5.2, Table 3, App F.

### Row 6. Oracle swap of test suites (original versus augmented tests)

- **Ribeiro, A.** MBPP+ (EvalPlus) appears only as an out-of-distribution fitting source; labels come from the benchmark suites; searched "EvalPlus", "HumanEval+", "augment". Location: Sec 4.1.2, Table 1.
- **Campos, A.** One test suite per benchmark; tests that "can miss errors" are a stated threat only; searched "EvalPlus", "augment". Location: Sec V-A "Candidates and labels", Sec VIII.
- **CREDO, A.** HumanEval+ is one evaluation set; no original-HumanEval contrast; searched "HumanEval ", "augment". Location: App B.3, Table 5.
- **Spiess, Pa.** Correctness criterion is swapped between exact match and test passing on DyPyBench (cross-tabulated; 6.89% of exact matches fail flaky tests); this is an oracle change, not test augmentation. Location: Sec III-A, Sec IV-A2, Table II.
- **NeuroSym, A.** HumanEval-Pro is used for its "more rigorous hidden test cases", but there is no original-versus-augmented comparison; searched "augment", "original tests". Location: Sec 4.1 "HumanEval-Pro".
- **RLCM, A.** Searched "EvalPlus", "augment", "test suite". Location: Sec 4.1.

### Row 7. Release or contamination split

- **Ribeiro, A.** Searched "contamin", "release", "cutoff" (release hits refer to the replication package). Location: Sec 7.
- **Campos, A.** LiveCodeBench problems released October 2024 to May 2025 are used for the language sets, but no pre- versus post-cutoff contrast; searched "cutoff", "contamin". Location: Sec V-A "Benchmarks".
- **CREDO, A.** LiveCodeBench v5 and v6 are separate evaluation sets, not a per-model release split; searched "contamin", "cutoff", "release". Location: Sec 4.1, App D.1.
- **Spiess, A.** Searched "contamin", "memoriz", "cutoff", "release". Location: Sec VI.
- **NeuroSym, Pa.** Per-model knowledge cutoffs define a post-cutoff LCB subset "treated as out-of-distribution", but Table 1 reports LCB as one column with no pre- versus post-cutoff contrast. Location: Sec 4.1 "LiveCodeBench", pp. 6136-6137, Table 1.
- **RLCM, A.** Searched "contamin", "cutoff", "release" (contamin hit is a reference title). Location: Sec 4.1.

### Row 8. Calibration estimator set (more than one ECE estimator, or a binning-free estimator)

- **Ribeiro, A.** No calibration metric is computed; selection accuracy and pass@rank-k only; searched "ECE", "Brier", "expected calibration" (zero hits; "calibrat" occurs only in Sec 6.3 and Sec 8 prose). Location: Sec 4.1.3, Sec 5.1.3.
- **Campos, A.** AUROC only; searched "ECE", "Brier", "calibration error". Location: Sec V-C.
- **CREDO, A.** One ECE estimator (ten equal-width bins); Brier and AUROC are not calibration-error estimators. Location: App B.3, eq. 20.
- **Spiess, Pa.** Equal-width ECE plus Brier and Brier skill score; reliability plots also shown with quantile bins, and binning sensitivity is noted, but no second ECE value is reported. Location: Sec III-C, Fig 2 caption, Tables III and IV.
- **NeuroSym, A.** One estimator ("unbiased estimator with M = 10 bins"); Soft-ECE is a training loss, not an evaluation estimator. Location: Sec 4.3, Sec 3.4 eq. 6.
- **RLCM, A.** Binned ECE and PCE (ECE restricted to overconfident bins), same binning; searched "kernel", "smooth", "bins" (smooth hits describe curves; no second estimator). Location: Sec 4.1 "Evaluation Metrics".

### Row 9. Clustered paired inference

- **Ribeiro, Pa.** GEE logistic regression with Benjamini-Hochberg correction for significance; the clustering unit and paired structure are not stated. Location: Sec 4.2.1, Tables 3 and 4 (asterisks).
- **Campos, P.** "Paired, problem-clustered bootstrap with 2,000 resamples", with shared resamples across language pairs. Location: Sec V-C "Significance".
- **CREDO, A.** Means and standard errors over three training seeds; searched "bootstrap", "paired", "cluster". Location: Table 1 caption, App B.3.
- **Spiess, A.** No inference; "bootstrapped p-values" named as future work; the only bootstrap is a data-size sweep for Platt scaling. Location: Sec VI, Sec IV-B (Figure A8 reference).
- **NeuroSym, A.** No intervals or tests; searched "significan", "bootstrap", "interval" (hits are narrative). Location: Sec 5, Table 1.
- **RLCM, A.** Searched "bootstrap", "paired", "cluster", "significan" (zero hits). Location: Sec 4.2.

### Row 10. Base versus instruct

- **Ribeiro, A.** Four instruct models only; searched "base model". Location: Sec 4.1.4.
- **Campos, A.** Two instruct or reasoning models; searched "base model". Location: Sec V-A "Models".
- **CREDO, A.** "Base" means untrained Qwen3-8B before RLVR, not a pretrained-only checkpoint. Location: Sec 4.1, App B.1.
- **Spiess, A.** CodeGen2 is described as "without instruction tuning", but it is a different model, not a pair. Location: Sec IV-A4.
- **NeuroSym, A.** Three instruct or distilled models; searched "base". Location: Sec 4.1.
- **RLCM, A.** "Base" is R1-Distill-Qwen-7B before RL; App C.1 swaps to Qwen3-4B-Instruct, a different family. Location: Sec 4.1, App C.1.

### Row 11. Same-weights reasoning on/off

- **Ribeiro, A.** Searched "reasoning", "thinking" (hits are generic). Location: Sec 4.1.4.
- **Campos, Pa.** gpt-oss judges without reasoning by design; one check on 498 candidates with medium-effort reasoning raises Yes-probability AUROC from 0.68 to 0.73, for the confidence readout only. Location: Sec V-A "Models", Sec VIII "Construct validity".
- **CREDO, A.** Qwen3-8B; searched "think", "non-thinking" (zero hits). Location: App B.1.
- **Spiess, A.** Searched "reasoning", "thinking", "chain-of-thought" (named as future work only). Location: Sec IV-D.
- **NeuroSym, A.** One distilled reasoning model versus two instruct models, across weights. Location: Sec 4.1.
- **RLCM, A.** App C.1 contrasts reasoning versus non-reasoning initialization confounded with family and scale; forced answers at token budgets truncate reasoning but are not an on/off toggle. Location: App A, App C.1, Sec 4.3.

### Row 12. Routing replay (confidence allocates execution, verification, or deferral, with random and oracle comparators)

- **Ribeiro, A.** Best-of-10 selection without tests is compared with Random and a pass@10 ceiling, but no execution, verification, or deferral is allocated; triage use is discussion only. Location: Sec 5.1.3, Sec 6.1.
- **Campos, A.** Gating test execution is future work. Location: Sec VII "Triage rather than selection", Sec IX.
- **CREDO, Pa.** Selective prediction (abstention): AURC and accuracy at 50/80/90% coverage versus other methods; no random or oracle comparator; searched "random", "oracle" (zero hits). Location: Sec 4.4, Table 3, Fig 5.
- **Spiess, A.** Graduated review policy is discussion only. Location: Sec I, Sec V.
- **NeuroSym, Pa.** Risk-coverage and AURC for selective generation on LCB versus baselines; no random or oracle comparator. Location: Sec 5.2, Fig 3.
- **RLCM, Pa.** Learn-Then-Test early exit (compute allocation) on AMC versus GRPO and RLCR, and confidence-weighted voting with an oracle comparator; math only, no random comparator for routing. Location: Sec 5.1, Fig 6, App F.
