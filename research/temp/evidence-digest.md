# Evidence digest (step 9)

Top load-bearing claims from research/temp/claims-*.json (empirical or statistical, or high confidence, with verbatim quoted_support), grouped by candidate. Non-deprecated notes only.

### 2. L1: Execution-graded measurement foundation

- A study of twelve uncertainty estimation methods on eight general LLMs over four NLP tasks and seven programming-capable LLMs on two code tasks (MBPP, HumanEval) finds uncertainty estimation can characterize prediction risks. (empirical)
  > Abstract: twelve uncertainty estimation methods and eight general LLMs on four NLP tasks and seven programming-capable LLMs on two code generation tasks
  [[look-before-you-leap-an-exploratory-study-of-uncertainty-analysis-for-large-lang]]

- Execution-based semantic clustering uses pre-generated tests from Qwen3-Coder-30B; correctness uses official LiveCodeBench hidden tests (proportion of tests passed). (empirical)
  > correctness scores ... defined as the proportion of hidden tests passed
  [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]]

- Program-correctness predictors transfer between benchmarks largely by identifying difficult problems; within-problem ranking is limited and sample-agreement (EigenScore) gives no consistent advantage over a single pass. (empirical)
  > For program correctness, predictors transfer more successfully between benchmarks, largely by identifying problems on which the model tends to fail. However, their ability to rank candidates within the same problem is limited.
  [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]

- CCP measures only the uncertainty of a particular claim value, improving over baselines for seven LLMs and four languages on biography generation. (empirical)
  > Our method Claim Conditioned Probability (CCP) measures only the uncertainty of a particular claim value expressed by the model.
  [[fact-checking-the-output-of-large-language-modelsvia-token-level-uncertainty-qua]]

- Against an oracle (smallest sample count whose majority vote is correct) at N=4 on Qwen2.5-1.5B, vote-entropy UAB (K=2) leaves 10.5% of questions under-allocated versus 13.3% for Uniform and 14.1% for an oracle-difficulty variant. (empirical)
  > UAB (Vote Entropy, K = 2 ) 10.5 75.4 11.7 Oracle (Difficulty) ‡ 14.1 59.8 8.9
  [[1introduction-2]]

- SALT provides six procedurally generated long-form tasks (logic, math, code, translation, Multi-Needle) with deterministic ground truth, allowing unit-level correctness, calibration and ranking evaluation without judges across 50+ LLMs. (empirical)
  > SALT comprises six procedurally generated tasks spanning logic, mathematics, code, translation, and multiple-needles-in-a-haystack (Multi-Needle).
  [[evaluating-llm-uncertainty-in-long-form-generation-using-deterministic-ground-tr]]

- Non-zero incoherence detects about two-thirds of non-zero errors without ground truth (69% MBPP, 66% HumanEval) with no false positives; 16 LLMs. (empirical)
  > a non-zero incoherence effectively detects about two-thirds of the non-zero errors in the absence of a ground truth implementation (69% and 66% detection rate on MBPP and HumanEval, resp.)
  [[incoherence-as-oracle-less-measure-of-error-in-llm-based-code-generation]]

- Multicalibration (calibration across intersecting groups) with prompt-embedding clustering or LLM self-annotation groups yields better-calibrated correctness probabilities than marginal calibration; IGLB and GCULR beat histogram binning and Platt scaling on QA. (empirical)
  > Multicalibration asks for calibration not just marginally, but simultaneously across various intersecting groupings of the data.
  [[multicalibration-for-confidence-scoring-in-llms]]

- Multicalibration with groups from complexity, code length, prompt length and language raises Brier Skill Score over uncalibrated and Platt/HB baselines; uncalibrated BSS is negative on LiveCodeBench (Qwen3 -0.543). (empirical)
  > uncalibrated - -0.543 -0.075 ... Platt - 0.377 0.187 ... LINR ✓ 0.463 0.721
  [[multicalibration-for-llm-based-code-generation]]

- Labels are 'correct if all tests pass' from benchmark unit tests; LiveCodeBench release_v6 (1055 problems, May 2023 to April 2025) chosen to mitigate data leakage. (empirical)
  > Generated code is evaluated via benchmark unit tests and labeled as correct if all tests pass.
  [[multicalibration-for-llm-based-code-generation]]

- Models assign up to 26% higher confidence to their own responses than to identical user-provided answers; framing the answer as user input improves calibration by up to 26% without retraining. (empirical)
  > models assign up to 26% higher confidence to their own responses.
  [[large-language-models-are-overconfident-in-their-own-responses]]

- v3 retracts earlier cross-model efficiency findings because the automated correctness scorer was length-biased; label validity changed the conclusion. (empirical)
  > Validated against 1,200 human adjudications, the scorer missed 53% of one model's human-correct answers and 26% of another's
  [[do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec]]

- On the same 3,000 questions and same weights, M-ratio profiles across four domains are uncorrelated between Q5_K_M and f16 (Spearman rho = 0.00), while Type-2 AUROC profiles are perfectly rank-stable (rho = 1.00). (empirical)
  > M-ratio profiles across four knowledge domains are uncorrelated between formats (Spearman rho=0.00) ... Type-2 AUROC profiles are perfectly stable across formats (rho=1.00)
  [[quantisation-reshapes-the-metacognitivegeometry-of-language-models]]

- Perplexity of code completions depends on language and model; strongly typed languages show lower perplexity, Shell is universally high. (empirical)
  > We find that strongly-typed languages exhibit lower perplexity than dynamically typed languages. Scripting languages also demonstrate higher perplexity. Shell appears universally high in perplexity, whereas Java appears low.
  [[the-fools-are-certain-the-wise-are-doubtful-exploring-llm-confidence-in-code-com]]

- ExeCRE estimates code reliability by statistical analysis of execution-output consistency over many random inputs using a Dawid-Skene latent-reliability model, and uses it to gate self-correction; under GPT-5.2 on LiveCodeBench misleading feedback on already-correct code drops from 113.2 to 14.0. (empirical)
  > Under GPT-5.2 on LiveCodeBench, the average number of misleading feedback cases on already correct code drops from 113.2 with a representative self-correction baseline to 14.0 with ExeCRE.
  [[execre-execution-consistency-guided-reliability-estimation-for-self-correcting-c]]

- The evaluation applies explicit release-window versus knowledge-cutoff control: the 182-problem window is cutoff-clean for Qwen2.5-Coder-32B-Instruct (cutoff 2024-06) and LLaMA-3.1-8B-Instruct (2023-12), but not for GPT-5.2 (2025-08); DeepSeek-V3.2 is unverifiable. (empirical)
  > GPT-5.2, Qwen2.5-Coder-32B-Instruct, and LLaMA-3.1-8B-Instruct have reported knowledge cutoffs of 2025-08, 2024-06, and 2023-12, respectively.
  [[execre-execution-consistency-guided-reliability-estimation-for-self-correcting-c]]

- Every execution-consistency confidence score looks better under the labels of the oracle that built its clusters, in 16 of 16 combinations; under expert labels, suite clusters raise AUROC by 6.96 and 1.53 points. (empirical)
  > Every execution-consistency score looks better under the labels of the oracle that built its clusters, in 16 of 16 combinations.
  [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]]

- Under blinded expert labels a certificate calibrated at nominal 0.10 carries 20.0 and 17.2 points of risk on two checkpoints. (empirical)
  > a certificate calibrated at a nominal 0.10 carries 20.0 and 17.2 points of risk on two checkpoints
  [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]]

- NLI-based semantic entropy collapses to near-chance AUROC on code (Python 0.50-0.53, Java 0.48-0.56, SQL 0.47-0.58) because NLI cannot separate functionally different code. (empirical)
  > Abstract: sampling-based methods relying on natural language inference (NLI) fail because NLI models cannot distinguish functionally different code, causing most responses to collapse into a single semantic cluster.
  [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]]

- LLM-judged functional equivalence methods (functional entropy, equivalence rate, sets) achieve top AUROC in 11 of 15 model-benchmark combinations, up to 0.867 on LiveCodeBench; verbalized confidence is erratic. (empirical)
  > Table 2 (Python AUROC): Func. Equiv. 0.867 (Gem-Fl), Func. Entropy 0.857, Verb. Conf. 0.795/0.716/0.597/0.725/0.681, P(True) 0.771/0.815/0.830/0.752/0.824
  [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]]

- ECE and ACE can give misleading assessments under severe class imbalance: ECE for an imbalanced case (ii)-(b) was smaller than for a well-balanced well-calibrated case (i)-(a). (empirical)
  > For example, the ECE value for case (ii)-(b) was smaller than that for case (i)-(a).
  [[tce-a-test-based-approach-to-measuring-calibration-error]]

- Models at distinct positions in sensitivity-bias space cannot be distinguished by calibration metrics alone. (empirical)
  > models occupying distinct positions in sensitivity–bias space could not be distinguished by calibration metrics alone
  [[llms-as-signal-detectors-sensitivity-bias-and-the-temperature-criterion-analogy]]

- Hybrid reassess-prompt plus Platt scaling improves ECE by up to 0.541 and Brier by up to 0.628. (empirical)
  > The hybrid strategy combining the reassess prompt strategy and Platt Scaling achieves improvements of up to 0.541, 0.628, and 15.084 over the original performance
  [[open-the-oyster-empirical-evaluation-and-improvement-of-code-reasoning-confidenc]]

- Token entropy correlates positively with the rank of the ground-truth token (rho 0.4595 to 0.5249 across nine code models). (empirical)
  > As shown in Table 1, the results consistently exhibit a positive correlation, further reinforcing the notion that entropy serves as a meaningful signal for identifying uncertain decoding steps.
  [[adadec-a-uncertainty-guided-lookahead-decoding-framework-for-llm-based-code-gene]]

- In a 30-programmer mixed-methods study, highlighting tokens by predicted likelihood of being edited speeds task completion and targeted edits; highlighting by generation probability gives no benefit over no highlighting. (empirical)
  > highlighting tokens according to their probability of being generated does not provide any benefit over the baseline with no highlighting.
  [[generation-probabilities-are-not-enough-uncertainty-highlighting-in-ai-code-comp]]

- Larger models generally produce better calibrated results, with effect size varying by task. (empirical)
  > Generally, larger models produce better calibrated results while the level of such effect is diverse among tasks.
  [[on-the-calibration-of-large-language-models-and-alignment]]

- Evaluation uses fuzzing-generated tests (APPS-f, Mercury-f, HumanEval-f, MBPP-f) replacing built-in tests for both learning and evaluation, a different label regime from hidden benchmark tests. (empirical)
  > We construct APPS-f, Mercury-f, HumanEval-f, and MBPP-f, where for each dataset, we replace the built in unit tests from each problem with automatically generated unit tests via fuzzing for both learning and evaluation.
  [[towards-functional-correctness-of-code-models-with-selective-generation]]

- Code-MUE is a black-box uncertainty measure: Von Neumann entropy of an execution-based semantic interaction graph over N=100 sampled programs executed on K=20 probe inputs. (empirical)
  > Code-MUE grounds uncertainty in observable runtime behavior, calculating the Von Neumann entropy of the solution space to quantify global semantic diversity.
  [[code-mue-measuring-code-llms-uncertainty-through-execution-based-semantic-intera]]

### 3. L2: Locating the disconnect between internal state and output

- Rating-probe relationship is not concept-specific and does not improve with scale from 1B to 27B. (empirical)
  > ratings are associated with other concepts’ probes as much as with their own, and change little when the question is about the user. Finally, neither the pre-question coupling nor concept specificity improves with scale (1B–27B).
  [[dont-ask-understanding-what-numeric-self-reports-measure-in-language-models]]

- Across 33 frontier LLMs and 1,500 MMLU items, verbalized-confidence Type-2 AUROC is highest for Applied/Professional (.742) and lowest for Formal Reasoning (.658) and Natural Science (.652); 47,151 observations. (empirical)
  > Applied/Professional knowledge was reliably the easiest benchmark domain to monitor (mean AUROC = .742
  [[domain-level-metacognitive-monitoring-in-frontier-llms-a-33-model-atlas]]

- Truthfulness information in hidden states concentrates at the exact answer tokens, and probes there improve error detection over logit baselines across models. (empirical)
  > We find that truthfulness information is concentrated in the exact answer tokens
  [[llms-know-more-than-they-show-on-the-intrinsic-representation-of-llm-hallucinati]]

- Compares six execution-free predictors in four families (output confidence, EigenScore consistency, hidden-state probe and LAT, causal DAS-based value probe and counterfactual simulation) on Qwen3-Coder-30B and gpt-oss-20b under benchmark shift (LiveCodeBench vs BigCodeBench) and language shift (Python, C++, Java). (empirical)
  > We compare six execution-free predictors from four families on Qwen3-Coder-30B and gpt-oss-20b under benchmark shift between LiveCodeBench and BigCodeBench and language shift across Python, C++ and Java.
  [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]

- For Qwen3-Coder verdict correctness, a probe on the causally localized subspace stays 0.09 AUROC ahead of output confidence under language shift (0.11 in distribution), but this does not generalize consistently to gpt-oss or benchmark shift. (empirical)
  > For Qwen3-Coder a probe on the causally localized subspace stays 0.09 AUROC ahead of output confidence under language shift (0.11 in distribution), significantly outperforming the best non-causal predictor by 0.04 AUROC on average.
  [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]

- Judge balanced accuracy against execution labels ranges from 57.2% to 74.4% (Table I); verdict is single-token Yes/No on the same forward pass as the hidden state; gpt-oss is a reasoning model but is prefilled to answer directly, so reasoning is disabled. (empirical)
  > Since gpt-oss is a reasoning model, we prefill its final channel so that it also answers directly.
  [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]

- The paper does not compare probes with verbalized confidence or base-versus-instruct pairs, and its output-confidence baseline is the Yes/No token probability; LiveCodeBench problems are restricted to Oct 2024-May 2025 for the language-shift study. (empirical)
  > We use 454 LiveCodeBench problems released between October 2024 and May 2025.
  [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]]

- Alignment between token-probability confidence and verbalized confidence is moderate at best: GPT-4 averages Spearman rho 0.42. (empirical)
  > Notably, among the models analyzed, OpenAI's GPT-4 showed the strongest confidence-probability alignment, with an average Spearman's ρ of 0.42, across a wide range of tasks.
  [[confidence-under-the-hood-an-investigation-into-the-confidence-probability-align]]

- A RepE/LAT correctness direction from last-token hidden states outperforms intrinsic likelihood and verbalized (reflective) confidence at picking the correct implementation among four candidates on HumanEval and BigCodeBench for four 7-8B instruct LLMs. (empirical)
  > LAT consistently outperforms all baselines. On BigCodeBench , it improves accuracy by +13.3 to +29.0 pp over the best reflective accuracy; on HumanEval , gains range from +8.7 to +26.2 pp over the strongest baseline.
  [[on-llms-internal-representation-of-code-correctness]]

- Table 3 (BigCodeBench) in-distribution LAT(Val) accuracies are Mistral 51.1% +/-10.6, Qwen 54.4% +/-3.8, CodeLlama 50.3% +/-6.2, OpenCoder 56.3% +/-5.1, against Random 27.5% (Mistral) and verbalized baselines 23.7-41.1%. (empirical)
  > Mistral 27.5% 5.7% ± 0.4 28.9% ± 0.8 23.7% ± 0.0 51.1% ± 10.6 ∗ 47.8% ± 0.8 ∗ 33.0% ± 0.1 ∗ 57.9% ± 4.5
  [[on-llms-internal-representation-of-code-correctness]]

- Out-of-distribution fitting of the correctness direction is erratic: synthetic fitting drops below random for Qwen (12.2%) and CodeLlama (22.2%) on BigCodeBench, MBPP+ fitting stays above random on HumanEval (32.2%-39.9%) but below in-distribution (41.4-60.7%). (empirical)
  > Synthetic fitting is erratic: two models drop below random (Qwen at 12.2%, CodeLlama at 22.2%), while Mistral and OpenCoder exceed it.
  [[on-llms-internal-representation-of-code-correctness]]

- Probes on hidden states of distilled R1 reasoning models verify intermediate answers with high ROC-AUC and low ECE, and a probe-confidence early-exit cuts tokens 24% at unchanged accuracy (math and logic only). (empirical)
  > We adopt the probe as a verifier and implement a confidence-based early-exit strategy by thresholding confidence scores from the probe.
  [[reasoning-models-know-when-theyre-right-probing-hidden-states-for-self-verificat]]

- Openia (Bui et al., JSS 2025) trains a probe on the last-token, last-layer hidden state of DeepSeek-Coder, CodeLlama, and Magicoder to predict correctness of generated code, with up to 2X gain standalone and 3X repository-level over baselines. (empirical)
  > we extracted the internal state of the last generated token from the last layer of the studied LLM for each query as a representation to assess the correctness of the corresponding generated output.
  [[correctness-assessment-of-code-generated-by-large-language-models-using-internal]]

- Small instruct LLMs give degenerate verbal confidence under minimal elicitation, with ceiling above 95% and near-chance AUROC2. (empirical)
  > Small instruct-tuned LLMs produce degenerate verbal confidence under minimal elicitation: ceiling rates above 95%, near-chance Type-2 AUROC (AUROC2 ), and Invalid validity profiles.
  [[distilling-self-consistency-into-verbal-confidence-a-pre-registered-negative-res]]

- Pre-registered CSFT with modal filter failed: verbal AUROC2 fell from 0.554 to 0.509 and accuracy dropped 7.6 pp. (empirical)
  > verbal AUROC2 dropped from 0.554 to 0.509, accuracy degraded 7.6 percentage points, and VRS remained Invalid.
  [[distilling-self-consistency-into-verbal-confidence-a-pre-registered-negative-res]]

- Post-hoc rescue yields verbal AUROC2 0.774 on held-out TriviaQA, exceeding single-pass logit entropy 0.701 and below 10-sample self-consistency 0.999. (empirical)
  > compresses a 10-sample self-consistency signal (AUROC2 = 0.999) into a single-pass verbal readout that exceeds single-pass logit entropy (AUROC2 = 0.701), with a compression loss of approximately 22.5%.
  [[distilling-self-consistency-into-verbal-confidence-a-pre-registered-negative-res]]

- Linear probes on hidden states of two diffusion LMs (LLaDA-8B, Dream-7B) predict functional correctness, with AUC rising 0.08-0.11 across denoising steps on reasoning tasks. (empirical)
  > Across two models (LLaDA-8B, Dream-7B) and four tasks, we find that DLMs uniquely accumulate correctness signal across denoising steps (AUC gains of 0.08–0.11 on reasoning tasks), absent in single-pass AR decoding.
  [[probing-functional-correctness-in-diffusion-language-models-full-text]]

- On MBPP, step-0 probe AUC is about 0.75-0.76 and peaks at about 0.84-0.87 at later steps; baseline MBPP pass rates are 40.9% (LLaDA) and 44.4% (Dream). (empirical)
  > MBPP follows the same gradual-buildup pattern as GSM8K: step-0 AUC is ≈ 0.75–0.76±0.04 and peaks at ≈ 0.84–0.87 ± 0.05 at later steps (step 64 for LLaDA, step 127 for Dream).
  [[probing-functional-correctness-in-diffusion-language-models-full-text]]

- A hidden-state probe beats confidence heuristics from the model's own softmax (entropy, max-prob) by 5-20 points in filtering accuracy at tau=0.80 and by 0.05-0.18 mean peak AUC over LR-entropy. (empirical)
  > Across all eight (dataset, model) settings, the probe outperforms the best raw signal in classification accuracy at τ = 0.80 by 5–20 percentage points, and its peak per-step AUC exceeds LR-entropy by 0.05–0.18 on average (full tables in Appendix J).
  [[probing-functional-correctness-in-diffusion-language-models-full-text]]

- Step-0 probe signal is comparable to an AR (Qwen-2.5-7B) probe on the same prompt, so it reflects prompt difficulty, not diffusion-specific computation. (empirical)
  > The step-0 hidden state already carries above-chance signal (AUC 0.61–0.80), but this is comparable to a probe on an AR model conditioned on the same prompt, indicating that step-0 signal reflects prompt difficulty rather than diffusion-specific computation.
  [[probing-functional-correctness-in-diffusion-language-models-full-text]]

- Instruction tuning raises ECE by 13.1% on average and the chat template adds another 2.74% (total +15.8% vs base) on MMLU logit-based confidence across six base/instruct pairs. (empirical)
  > On average, instruction tuning boosts accuracy by 3.7% but degrades calibration, increasing ECE by 13.1% and Brier score by 6.5%.
  [[large-language-models-are-overconfident-in-their-own-responses]]

- All experiments are on MMLU, GSM8K, TruthfulQA; no code benchmark or execution ground truth. (empirical)
  > Extensive experiments across six recent open-weight LLMs, three benchmarks, and three confidence elicitation methods
  [[large-language-models-are-overconfident-in-their-own-responses]]

- For RLHF-LMs (ChatGPT, GPT-4, Claude), verbalized confidences are typically better calibrated than conditional token probabilities on TriviaQA, SciQ, TruthfulQA, often cutting ECE by a relative 50%. (empirical)
  > verbalized confidences emitted as output tokens are typically better-calibrated than the model's conditional probabilities on the TriviaQA, SciQ, and TruthfulQA benchmarks, often reducing the expected calibration error by a relative 50%.
  [[just-ask-for-calibration-strategies-for-eliciting-calibrated-confidence-scores-f-2]]

- On forecasting (non-code) with Eternis-Forecaster 8B, representation-pooling probes achieve substantially better calibration than the model's own outputs, and routing by the pre-reasoning answer distribution saves 30-47% of generated tokens with no accuracy loss. (empirical)
  > routing questions by the spread of this pre-set answer distribution saves 30–47% of generated tokens, with no loss of accuracy
  [[what-llm-forecasters-know-but-dont-say-probing-internal-representations-for-cali]]

- Action-level uncertainty metrics outperform reasoning-level ones: Table 1 reports Mean Token Entropy action PRR 0.424 / ROC-AUC 0.710 vs reasoning 0.168 / 0.596. (empirical)
  > Mean Token Entropy 0.424 0.710 0.168 0.596
  [[redact-uncertainty-aware-deferral-for-llm-agents]]

- Correctness of Qwen3-4B-Instruct-2507's first-attempt code on 444 LiveCodeBench tasks is linearly decodable from the final-prompt-token hidden state before any output token, with leakage-free held-out AUC 0.881 ± 0.008 over 50 outer splits. (empirical)
  > The correctness of the model’s first-attempt code is linearly decodable from the hidden state at the final prompt token, captured before any output token is generated, with a leakage-free held-out AUC of 0.881 ± 0.008 across 50 outer splits.
  [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]]

- After residualizing each hidden dimension against prompt length the probe retains AUC 0.842 ± 0.010 versus a prompt-length-only baseline of 0.657 ± 0.014; nonlinear prompt-length models (RF 0.642, GB 0.649, MLP 0.657) do not exceed the logistic baseline. (empirical)
  > The probe still achieves an AUC of 0.842 ± 0.010 , substantially above a logistic prompt-length baseline of 0.657 ± 0.014 , and none of the nonlinear models tested improves upon it.
  [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]]

- Layer choice is made by nested CV: layer 30 is modal (16 of 50 outer splits), layer 29 next (13), layer 33 (8); per-layer test AUC plateau 0.880-0.884 across layers 29-36. (empirical)
  > The modal selection across the 50 splits is layer 30 with C = 0.001 , chosen in 16 of them.
  [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]]

- On Gemma 3 27B TriviaQA, verbal confidence and answer log-probs predict first-attempt correctness at AUROC 0.74 and 0.76 with ECE 0.13 and 0.20. (empirical)
  > Verbal confidence and the log-probabilities of the answer tokens yielded an AUROC of 0.74 and 0.76 for predicting A1 correctness, respectively; expected calibration error (ECE) was 0.13 and 0.20, respectively.
  [[how-llms-detect-and-correct-their-own-errors-the-role-of-internal-confidence-sig]]

- PANL activations predict error detection beyond verbal confidence, and patching shows causal sufficiency. (empirical)
  > Activation patching confirms that PANL is causally sufficient to rescue error detection when answer information is corrupted
  [[how-llms-detect-and-correct-their-own-errors-the-role-of-internal-confidence-sig]]

- Findings replicate across Gemma 3 27B and Qwen 2.5 7B on TriviaQA and MNLI. (empirical)
  > All key findings replicate in Gemma 3 27B and Qwen 2.5 7B, using the TriviaQA and MNLI datasets, suggesting a domain-general evaluative mechanism.
  [[how-llms-detect-and-correct-their-own-errors-the-role-of-internal-confidence-sig]]

- AutoProbe dynamically selects layers and token positions via attention for probing code correctness (compilability, functionality, security) and beats a fixed last-token-last-layer probe (Openia). (empirical)
  > AutoProbe consistently outperforms the baselines. For security assessment, AUTOPROBE surpasses the state-of-the-art white-box approach by 18%.
  [[251002934-autoprobe-model-agnostic-correctness-assessment-full-text]]

- In-house LLM-as-judge (the generator assessing its own output) is far weaker than probes on the security criterion. (empirical)
  > Table 4: DeepSeek Coder-1.3B In-house LLM-AJ F1 0.21, External LLM-AJ 0.63, Openia 0.81, AutoProbe 0.89.
  [[251002934-autoprobe-model-agnostic-correctness-assessment-full-text]]

- All seven 3-9B instruct models were classified Invalid on numeric verbal confidence, mean ceiling rate 91.7%, in 8,384 deterministic trials on 524 TriviaQA items. (empirical)
  > All seven instruct models were classified Invalid on numeric confidence (H2 confirmed, 7/7 vs. predicted ≥ 4/7), with a mean ceiling rate of 91.7%
  [[verbal-confidence-saturation-in-3-9b-open-weight-instruction-tuned-llms-a-pre-re]]

### 4. L3: Verification utility and confidence updating

- HVR=0 reasoning traces are correct 96.1% of the time, a zero-cost correctness gate, on non-code benchmarks. (empirical)
  > traces containing no hedging markers are correct 96% of the time, revealing an emergent high-precision confidence gate at zero additional cost
  [[selfdoubt-uncertainty-quantification-for-reasoning-llmsvia-the-hedge-to-verify-r]]

- A two-tier cascade yields 71% coverage at 89.7% accuracy without task labels (non-code deferral analogue to L3). (empirical)
  > A deployment cascade combining both stages attains 90% accuracy at 71% coverage without any task-specific labels.
  [[selfdoubt-uncertainty-quantification-for-reasoning-llmsvia-the-hedge-to-verify-r]]

- Lever trains a verifier on NL input, program, and execution result, then reranks by combining verification score with generation probability and marginalizing over programs with identical execution results. (empirical)
  > The sampled programs are reranked by combining the verification score with the LLM generation probability, and marginalizing over programs with the same execution results.
  [[lever-learning-to-verify-language-to-code-generation-with-execution]]

- Lever improves over base code LLMs by 4.6% to 10.9% with code-davinci-002 and sets new state of the art on all four benchmarks. (empirical)
  > improves over strong baselines that use execution error pruning by 4.6% to 10.9%
  [[lever-learning-to-verify-language-to-code-generation-with-execution]]

- On selective generation at fixed FPR, ESE/EDSE far exceed single-model SE/DSE and NLI-based SE (e.g. Qwen3-8B Acc. 0.8247 vs SE 0.6420 at 10% FPR). (empirical)
  > ESE 0.8247 0.7246 0.7880 ... SE 0.6420 0.3961 0.6199
  [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]]

- Cascading TTS framework Cas uses ESE-based uncertainty plus public-test pass as the escalation signal; ablation removes ensemble, uncertainty, or public-pass components. This is uncertainty-routed compute with hidden-test Pass and cost, but baselines are TTS methods (majority voting, S*), not random/oracle routing. (empirical)
  > Cas 86.11 2.47 69.80 92.13 ... Cas (w/o ensemble) 81.80 2.29 76.86 86.98
  [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]]

- Mid-execution agents (same model as coding agent) lower stated success probability as partial work is observed, but the doubt is uninformative: equal for successes and failures; AUROC GPT ~0.53 stable, Gemini 0.49 to 0.64, Claude 0.62 to 0.52 across 25/50/75% checkpoints. (empirical)
  > Sec 3 'Mid-Execution: Uninformative Doubt'; Table 1; intro: 'confidence decreases as they observe their partial work, but this doubt is uninformative, occurring equally for successes and failures.'
  [[agentic-uncertainty-reveals-agentic-overconfidence]]

- Post-execution agents predict ~73% success vs 35% true for GPT-5.2-Codex; adversarial framing reduces overconfidence by up to 15 pp. (empirical)
  > Intro bullets; Table 2
  [[agentic-uncertainty-reveals-agentic-overconfidence]]

- Ranking 10 self-samples by LAT lifts pass@rank-1 above pass@1 without test execution; e.g. Mistral HumanEval Fit_HE reaches 41.3% at rank-1 versus 34.7% pass@1 and RankEF 35.5%; the paper reports only a few comparisons were statistically significant. (empirical)
  > Numerically, LAT shows superior or comparable accuracy to all baselines, including RankEF, across most settings. Only a few comparisons reached statistical significance.
  [[on-llms-internal-representation-of-code-correctness]]

- Staged verification (lightweight filters then ORM ranking) shifts the accuracy-throughput Pareto frontier outward, giving 11.64x higher throughput at 8.26% accuracy loss versus full test-suite verification. (empirical)
  > We find that ORMs with staged verification shift the Pareto frontier outward, achieving 11.64x higher throughput at a cost of 8.26% accuracy relative to full test-suite verification.
  [[1introduction-3]]

- CODEREFUSER, built on Learn-Then-Test, decides abstention using execution-consistency cluster ratio or semantic entropy over LLM-generated tests, with oracle tests used only in calibration. (empirical)
  > At TEST/DEPLOYMENT time, the method uses ONLY LLM-generated test cases and execution-consistency clustering (vault full-text note extraction)
  [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]

- At alpha=0.2 on MBPP with Qwen2.5-Coder-32B the CR variant abstains on about 30% of tasks versus over 80% for the PPL baseline. (empirical)
  > needs to abstain on only ~30% of tasks ... whereas the PPL static baseline must abstain on over 80% (vault note extraction)
  [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]

- Table 1: HumanEval Qwen2.5-Coder Execution baseline precision 24.29 / F1 38.23 versus CR+STDF 73.33 / 53.85; CodeLlama 72.15/83.82 versus 91.67/91.70. (empirical)
  > Table 1 rows as extracted in the vault note
  [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]

- UAB reallocates a fixed sampling budget across questions using vote entropy of the first K samples with a marginal-greedy solution to a concave coverage surrogate, improving average accuracy by +2.3% over uniform allocation and up to +5.5% on individual benchmarks. (empirical)
  > UAB improves average accuracy by + 2.3 % over uniform allocation, and achieves gains of up to + 5.5 % on individual benchmarks, with the largest gains in low-resource settings.
  [[1introduction-2]]

- Logit-based signals (NLL, Max Token NLL, ANLL) give allocation accuracies of 44.8-45.0 average, below vote entropy 47.0, indicating sampled disagreement is the stronger routing signal in this setting. (empirical)
  > Max Token NLL 46.8 ±0.3 43.4 ±1.5 18.0 ±1.0 60.6 ±1.9 56.3 ±2.1 45.0 0.688
  [[1introduction-2]]

- Probe-based selective generation avoids 36-98% of denoising compute in an offline simulation that does not cost the probe forward pass. (empirical)
  > The selective generation analysis is a simulation on states from full 128-step generation and does not account for inference overhead of running probes in real time.
  [[probing-functional-correctness-in-diffusion-language-models-full-text]]

- Gating costly transductive test generation on low inductive agreement cuts average cost from $0.077 to $0.065 while keeping reranking quality. (empirical)
  > Compared with TT w/o Gating, CoTT reduces the average inference cost from $0.077 to $0.065
  [[confidence-gated-transductive-test-generation-for-code-reranking]]

- Deferring about 15% of decisions from a small to a large LLM based on calibrated uncertainty matches large-model quality in text-based embodied environments. (empirical)
  > deferring only about 15% of decisions to the large model can match the quality of using it exclusively, while significantly reducing inference costs.
  [[redact-uncertainty-aware-deferral-for-llm-agents]]

- Self-repair data are starved: of 266 first-attempt failures only 20 recover within 5 attempts (14 at the first repair); conditional pass rate falls from 40.1% at attempt 0 to 5.3%, 2.0%, 0.4%, 0%. (empirical)
  > Of the 266 tasks whose first attempt fails, only 20 ever recover within the 5-attempt budget, 14 of them at the first repair, and the conditional pass rate among still-unsolved tasks collapses from 40.1% at attempt 0 to 5.3%, 2.0%, 0.4% and 0% at attempts 1 through 4.
  [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]]

- Learned early stopping's gain over matched random restarting (up to 1.98 pp) comes from between-task allocation, not within-task attempt selection, and continuation dominates restarts. (empirical)
  > an exact decomposition proving that learned stopping's gain over matched random restarting (up to 1.98 percentage points) stems from between-task stopping allocation rather than within-task attempt selection
  [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]]

- Early prefixes yield near-chance within-task discrimination even after tests were invoked. (empirical)
  > near-chance within-task discrimination (AUC_within approx 0.50) ... even though 87.51% of primary-corpus runs have already invoked tests and 32.80% have edited code by 20k tokens
  [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]]

- Interchange-intervention study finds confidence report coordinate is a weaker instrument than answer and caveat coordinates and shows confidence reports should respond to licensed evidence but resist pressure; non-code. (empirical)
  > (partial functional disentanglement rather than full independence; confidence a weaker instrument)
  [[260712985-resist-and-update-counterfactual-report-coordinates-full-text]]

### 5. L4: Per-requirement confidence and localization

- FLARE trains a 6-layer, 8-head transformer encoder on generator token probabilities, embeddings, and syntactic token types to predict line-level suspiciousness, then searches top-k regions and selects by execution outcome. (empirical)
  > we present Flare, an iterative framework with a lightweight diagnostic model that predicts line-level suspiciousness signals for bug localization and code refinement.
  [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement-2]]

- FLARE (k=1) gains 1.72% to 7.42% absolute pass@1 over NL-Debugging; k=10 gives 8.50% average improvement over no candidate search; on LiveCodeBench Llama-3.3-70B goes from 46.86 (alone) to 64.57 (k=1) and 76.57 (k=10). (empirical)
  > Even without expanded search, Flare (k=1) still outperforms Self-Debugging and Self-Refine in all settings and surpasses NL-Debugging in 9 of the 10 settings.
  [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement-2]]

- Confidence enters only as input features to a supervised localizer; no calibration metric (ECE, Brier) of line-level or requirement-level confidence is reported, and the signals come from the generator's token probabilities, not hidden states or verbal confidence. (empirical)
  > we use the LLM's confidence signals, token embeddings, and syntactic token types as inputs to the diagnostic model.
  [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement-2]]

- Self-Debugging improves baseline accuracy by up to 12% on TransCoder and MBPP where unit tests exist, and 2-3% on Spider without tests, using execution feedback and self-explanation. (empirical)
  > On TransCoder and MBPP where unit tests are available, Self-Debugging improves the baseline accuracy by up to
  [[teaching-large-language-models-to-self-debug]]

- TokenRepair uses context-aware token-level uncertainty fluctuations to localize likely-faulty tokens in a patch and rewrites only those, then filters low-quality patches by external feedback; it fixes 88 bugs on Defects4J 1.2 and 139 on HumanEval-Java. (empirical)
  > TokenRepair achieves new state-of-the-art repair performance, correctly fixing 88 bugs on Defects4J 1.2 and 139 bugs on HumanEval-Java, demonstrating substantial improvements ranging from 8.2% to 34.9% across all models on Defects4J 1.2 and from 3.3% to 16.1% on HumanEval-Java.
  [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]]

- Token suspiciousness scores localize faulty tokens with average Top-K accuracy 0.589 to 0.695 across models and decay settings, evidence of a correlation between uncertainty scores and patch correctness. (empirical)
  > achieving average localization accuracy ranging from 0.589 to 0.695, indicating promising effectiveness of uncertainty-guided token-level fault localization
  [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]]

- Ablation shows uncertainty-guided fault localization is the most influential component: removing it lowers performance by 20.6%. (empirical)
  > uncertainty-guided fault localization has the most substantial impact, it could drop the performance by 20.6% upon removal
  [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]]

- Evaluation uses temperature 1, patch budget capped at 50, and the repair terminates when a plausible patch is found; no per-requirement or test-group confidence is used and no verbalized confidence is elicited. (empirical)
  > The overall patch generation budget is capped at 50, meaning that the repair process terminates once either all budgets are consumed or a plausible patch is found.
  [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]]

- VeRPO converts per-test pass fractions into density-calibrated dense rewards plus a global outcome reward, identifies a cardinality bias in partial-success rewards, and gains up to +8.83 pass@1 with negligible overhead. (empirical)
  > partial success, passing a subset of test cases, offers an intrinsic, verifiable source of dense supervision.
  [[beyond-binary-turning-partial-success-into-dense-verifiable-rewards-for-reinforc]]

- SpanUQ, a ~25M-parameter probe over frozen hidden states, estimates span-level uncertainty (AUROC 0.908-0.944) on a 20K-prompt, ~293K-span benchmark, outperforming sampling methods at 10-20x lower cost. (empirical)
  > a lightweight ( ∼25M parameter) probe that distills the uncertainty knowledge from expensive multi-sample inference into a single forward pass over LLM hidden states
  [[spanuq-span-level-uncertainty-quantificationfor-large-language-model-generation]]

- Jointly pruning code and refreshing self-generated tests from the execution matrix raises BoN from 22.1% to 33.2% and unit-test accuracy from 14.6% to 78.3% on Qwen2.5-7B-Instruct. (empirical)
  > CoSPlay on Qwen2.5-7B-Instruct improves average BoN from 22.1% to 33.2% and UT accuracy from 14.6% to 78.3%
  [[cosplay-cooperative-self-play-at-test-time-with-self-generated-code-and-unit-tes]]

- Fact-level calibration to relevance-weighted correctness plus confidence-guided self-correction (ConFix) reduces hallucination across four datasets and six models, in long-form text, not code. (empirical)
  > we propose a fact-level calibration framework that operates at a finer granularity, calibrating confidence to relevance-weighted correctness at the fact level.
  [[fact-level-confidence-calibration-and-self-correction-full-text]]

- The edit model was built from 9 participants editing completions; a token's edit probability is the fraction of participants who edited it; tokens edited by at least 4 of 6 were highlighted (203 characters). (empirical)
  > For each token in the completion, we then set the probability of an edit to be the fraction of participants who edited it.
  [[generation-probabilities-are-not-enough-uncertainty-highlighting-in-ai-code-comp]]

- Moving a misconception from hypothesis to plan raises failure by 32.2% in PersistQueue and 28.9% in Dijkstra; different misconceptions yield distinct model-dependent patterns of violated obligations. (empirical)
  > Moving the misconception from hypothesis to plan increased failure by 32.2% in PersistQueue and 28.9% in Dijkstra after matching the experimental mix.
  [[poison-valleys-diagnosing-path-dependent-failure-in-llm-code-repair]]

### 6. F: Measurement-instrument framing

- Asking a rating question displaces the probed internal state; the rating is weakly coupled to the pre-question probe but strongly to the post-question probe. (empirical)
  > We find that rating questions displace the probed state, and that the rating is only weakly coupled with the probe score before the question but tracks the post-question probe much more strongly.
  [[dont-ask-understanding-what-numeric-self-reports-measure-in-language-models]]

- Standard post-hoc calibrators improve calibration scores but not consistently selective prediction; calibration metrics can disagree with selective-prediction performance. (empirical)
  > (2) standard post-hoc calibrators often improve calibration scores but do not consistently translate into better selective prediction behavior; and (3) commonly used calibration metrics can disagree with selective prediction performance
  [[beyond-confidence-rethinking-uncertainty-calibration-in-deep-code-models]]

- Pre-registered SDT study of 3 LLMs over 168,000 trials finds temperature increases sensitivity (AUC) and shifts criterion simultaneously, so the temperature-as-criterion analogy breaks. (empirical)
  > Our results confirm the breakdown with temperature simultaneously increasing sensitivity (AUC) and shifting criterion.
  [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]]

- Limitations: two model families at 7-8B with quantization, 30.1% scoring missed-match rate, factual QA only; no code or execution ground truth. (empirical)
  > Only two model families (Llama-3-8B and Mistral-7B) were tested, both at 7–8B parameters with Q5_K_M quantisation.
  [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]]

- A pilot with gpt-4.1-nano on 45 synthetic vignettes x 3 prompt variants (135 trials) gives accuracy 93.5%, mean confidence 78.4%, AUROC2 0.876, using a psychophysics-inspired metacognitive-sensitivity framework. (empirical)
  > Across forced-choice trials, diagnostic accuracy was 93.5%, mean confidence was 78.4%, and AUROC2 was 0.876.
  [[large-language-models-show-metacognitive-sensitivity-in-medical-reasoning]]

- An SDT Type-2 decomposition of LLM confidence separates discrimination from calibration level and reveals unequal-variance structure invisible to ECE. (empirical)
  > Standard evaluation of LLM confidence relies on calibration metrics (ECE, Brier score) that conflate two distinct capacities: how much a model knows (Type-1 accuracy) and how well its confidence signal tracks that knowledge (Type-2 metacognitive sensitivity).
  [[do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec]]

- Pre-registered confidence-amplification SFT doubled the Science NLP gap (0.076 to 0.152) but did not improve meta-d' (all four confirmatory hypotheses null), showing a first-moment confidence gap can rise without better discrimination structure. (empirical)
  > The training successfully reshaped confidence distributions, doubling the NLP gap in Science from 0.076 to 0.152, but did not improve meta-d'
  [[quantisation-reshapes-the-metacognitivegeometry-of-language-models]]

- Across five experiments on 17 models from five LLM series, reasoning ability scales with model size but item-level metacognitive sensitivity does not; in some series the smallest models show higher sensitivity than larger ones. ABSTRACT-ONLY (Crossref record of the OSF/PsyArXiv preprint). (empirical)
  > Although reasoning ability reliably scales with model size, metacognitive sensitivity does not; in some series, the smallest models even exhibit higher metacognitive sensitivity than their larger counterparts.
  [[8jq4f_v1]]

- A pre-registered audit of verbal, probe, and sampling-agreement confidence on five Qwen2.5 models (0.5B-7B, one base/instruct pair at 7B) finds three formats of verbal confidence barely correlate (Spearman 0.126, -0.069, 0.247 vs target >=0.60). (empirical)
  > Table 2: Format A vs. Format B +0.126; Format A vs. Format C -0.069; Format B vs. Format C +0.247; all FALSIFIED against >=0.60
  [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]

- ECE misleads: verbal confidence has low ECE by clustering near the base rate, while sampling agreement has worse ECE but about 2.02x the Murphy resolution and the lowest Brier. (empirical)
  > Table 3: Verbal ECE(15 bins) 0.0366, Resolution 0.03160, Brier 0.1713; Internal Probe 0.0500, 0.05154, 0.1524; Behavioral Consensus 0.0704, 0.06371, 0.1465
  [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]

- The paper positions itself as a measurement-validity study with pre-registered hypotheses and audit gates, and names Mahaut et al. 2024 and DECK (Chauhan 2026) as closest prior work. (empirical)
  > Section 2: We position this paper as a measurement-validity study rather than a discovery
  [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]

- More than 99.93% of positive-negative pairs in pooled AUROC are cross-unit, so a run-blind difficulty oracle reaches AUROC up to 0.945. (empirical)
  > pooled AUROC is dominated by comparisons across different agent-task units: more than 99.93% of the underlying positive-negative pairs are cross-unit
  [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]]

- Six PAI/MMPI-3-derived validity indices (L, K, F, Fp, RBS, TRIN) applied to 20 frontier models over 524 items identify four models as construct-level invalid and two as elevated. (empirical)
  > identifies four models as construct-level invalid and two as elevated
  [[before-you-interpret-the-profilevalidity-scaling-for-llm-metacognitive-self-repo]]

- Five measurement hazards change conclusions; numerical precision alone changes about one episode verdict in ten: bfloat16 and float16 agree with float32 on only 88.4% and 89.6% of episode verdicts, below a pre-registered 95% bar. (empirical)
  > Both bfloat16 and float16 fell below the pre-registered 95% agreement bar, at 88.4% and 89.6% respectively.
  [[a-capitulation-direction-emerges-with-scale-and-is-causallyload-bearing-where-va]]

### Ungrouped

- Bootstrap CIs on 198 model-domain cells have median width .199; split-half aggregate stability r = .893. (empirical)
  > Bootstrap 95% CIs (1,000 resamples) on the 198 model-domain cells have median width .199
  [[domain-level-metacognitive-monitoring-in-frontier-llms-a-33-model-atlas]]

- ESE aggregates execution-behavior semantic distributions across models; H_ESE equals mean within-model SE plus Jensen-Shannon divergence across models (Eq. 10), motivated by consistent-but-wrong single-model clusters. (empirical)
  > H_ESE(x) = (1/L) sum_l H_SE(x; theta_l) + JSD(p(.|x,theta_1),...,p(.|x,theta_L))
  [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]]

- Results are averaged over six seeds with 95% CIs; median CI width 1.48 percentage points. (empirical)
  > Results are averaged over six random seeds with 95% confidence intervals; median CI width is 1.48 percentage points.
  [[1introduction-3]]

- Test-based filtering catches bugs the ORM misses: filtered candidates sat 31 ranks too high on average. (empirical)
  > Test-based filtering catches bugs the ORM misses, particularly single-character errors that preserve surface form but fail at runtime. Filtered candidates sat 31 ranks too high on average; removing them shifts the frontier.
  [[1introduction-3]]

- Evaluation uses HumanEval (164), HumanEval+ (164), MBPP (427) with GPT-3.5-Turbo candidates and tests from Huang et al. (2024), about 200 candidates and 500 tests per problem. (empirical)
  > We use candidate solutions and tests from Huang et al. (2024), generated by GPT-3.5-Turbo, with approximately 200 candidates and 500 tests per problem.
  [[aces-who-tests-the-tests-leave-one-outauc-consistency-for-code-generation]]

- On KernelBench, selecting the highest-surprisal correct sample gives 80% success versus 50% for most-confident selection; surprisal-guided-top3 matches oracle at 100%. (empirical)
  > selecting the highest-surprisal (lowest-confidence) correct sample yields 80% success vs. 50% for most-confident selection, a 30% improvement.
  [[260207670-surprisal-guided-selection-for-execution-grounded-code-generation-full]]

- BlindSpotEval evaluates LLM-generated unit tests by three obligation metrics (Boundary-Value Adequacy, Control-Flow Adequacy, Oracle Strength) plus execution reliability, on ObligBench with 895 complex and 700 low-complexity Java functions. (empirical)
  > a complexity-stratified Java benchmark comprising 895 complex and 700 low-complexity functions with source-side obligation annotations.
  [[beyond-coverage-and-mutation-a-blind-spot-analysis-of-llm-generated-unit-tests]]

- Four LLMs evaluated: GPT-5.4, Gemma-4-31B, Gemini-3.6-flash, Qwen3-Coder-30B. (empirical)
  > we evaluate four LLMs (GPT-5.4, Gemma-4-31B, Gemini-3.6-flash, and Qwen3-Coder-30B)
  [[beyond-coverage-and-mutation-a-blind-spot-analysis-of-llm-generated-unit-tests]]

### Consensus claims [consensus]

- [consensus] Hidden states of code models linearly encode the execution correctness of generated code above chance (reported AUCs or accuracies well above random across autoregressive, diffusion, agentic, and pre-generation settings). | scope: Code with execution labels; 8+ independent groups after collapsing Devanbu/Nadi and Bui/Vu clusters | sources: [[on-llms-internal-representation-of-code-correctness]], [[250112934-correctness-assessment-of-code-generated-by-large-language-models-usin]], [[260614530-code-correctness-linearly-decodable-from-hidden-states-before-generati]], [[260705188-latent-programming-horizons-in-coding-agents-full-text]], [[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]], [[probing-functional-correctness-in-diffusion-language-models-full-text]], [[mechanistic-interpretability-of-code-correctness-in-llms-via-sparse-autoencoders]], [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]], [[abstract]]

- [consensus] Stated (verbal or reflective) confidence of code models is poorly calibrated, overconfident, or inconsistent as a predictor of execution correctness, especially for small open instruct models. | scope: Code with execution labels; Ribeiro et al. (same Devanbu/Nadi cluster as 240202047) counted once | sources: [[240202047-calibration-and-correctness-of-language-models-for-code]], [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]], [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]], [[an-empirical-study-of-security-calibration-in-large-language-models-for-code]], [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]], [[1introduction]]

- [consensus] Token-level likelihood or entropy is a weak discriminator of pass versus fail across problems on code (AUROC near or below about 0.70 in most reported settings). | scope: Code with execution labels; exceptions are within-task mutant ranking and token-localization uses | sources: [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]], [[semantic-vs-structural-signals-log-probability-and-llm-as-a-judge-for-reference]], [[assessing-correctness-in-llm-based-code-generation-via-uncertainty-estimation]], [[240202047-calibration-and-correctness-of-language-models-for-code]], [[multicalibration-for-llm-based-code-generation]]

- [consensus] NLI- or embedding-based semantic entropy transferred from NLG fails on code; clustering sampled programs by execution behavior or symbolic equivalence is needed for sampled agreement to track correctness. | scope: Code with execution labels; assessing-correctness and using-semantic-distance may share the Sharma and David group, so only one is listed | sources: [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]], [[assessing-correctness-in-llm-based-code-generation-via-uncertainty-estimation]], [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]], [[code-mue-measuring-code-llms-uncertainty-through-execution-based-semantic-intera]]

- [consensus] Binned ECE alone is a misleading calibration measure: it can be near zero for base-rate or collapsed predictors and decouples from discrimination, so resolution, Brier skill, or AUROC must be reported alongside it. | scope: Mixed: code with execution labels (240202047, verbalized-uncertainty, characterizing-overconfident) and general-domain | sources: [[240202047-calibration-and-correctness-of-language-models-for-code]], [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]], [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]], [[tce-a-test-based-approach-to-measuring-calibration-error]], [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]], [[when-calibration-rankings-reverse-accuracy-controlled-evaluation-for-fair-compar]], [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]]

- [consensus] Calibration and discrimination dissociate: post-hoc recalibration improves calibration error or Brier but does not improve ranking by correctness, and cannot recover information the score has lost. | scope: Mixed: code (generation and classification) plus general statistical theory | sources: [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]], [[when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-code-predicti]], [[beyond-confidence-rethinking-uncertainty-calibration-in-deep-code-models]], [[decomposing-probabilistic-scores-reliability-information-loss-and-uncertaintysup]], [[rethinking-early-stopping-refine-then-calibrate]], [[statistical-inference-for-score-decompositions]]

- [consensus] Benchmark test suites are thin enough that execution labels carry false passes; strengthening tests lowers measured pass rates and can change model rankings. | scope: Code with execution labels (function-level, repository-level, text-to-SQL) | sources: [[is-your-code-generated-by-chatgpt-really-correct-rigorous-evaluation-of-large-la]], [[rethinking-verification-for-llm-code-generation-from-generation-to-testing]], [[swe-abs-adversarial-benchmark-strengthening-exposes-inflated-success-rates-on-te]], [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]]

- [consensus] LLM-written tests are not independent verifiers: they inherit the generator's blind spots, often fail to execute or carry wrong oracles, and agreement-based selection fails when samples share correlated errors. | scope: Code with execution labels; duplicate notes for verification-trap and beyond-coverage counted once | sources: [[261005170-verification-trap-understanding-test-time-selection-failures-under-fal]], [[261032548-beyond-coverage-and-mutation-a-blind-spot-analysis-of-llm-generated-un]], [[certified-against-which-oracleexecution-labels-set-the-reported-riskof-conformal]], [[inference-time-code-selection-via-symbolic-equivalence-partitioning-full-text]], [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]]

- [consensus] Pooled AUROC of code and agent correctness predictors is dominated by problem difficulty; within-problem or within-run discrimination is much weaker. | scope: Code with execution labels; disentangling, hard-issue, and continue-or-restart may share authors (not confirmed in the redundancy audit), so independence rests on which-signals and the diffusion probe paper plus at least one agent paper | sources: [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]], [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]], [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]], [[probing-functional-correctness-in-diffusion-language-models-full-text]], [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]]

- [consensus] Outside code, hidden-state probes or internal estimators predict answer correctness better than verbalized confidence. | scope: General-domain (math, factual QA, forecasting, true/false statements); no execution labels | sources: [[hidden-error-awareness-in-chain-of-thought-reasoningthe-signal-is-diagnostic-not]], [[calibration-not-answer-selection-distilling-internal-confidence-in-reasoning-mod]], [[when-words-fall-short-iterative-synergy-between-verbalized-reasoning-and-hidden]], [[what-llm-forecasters-know-but-dont-say-probing-internal-representations-for-cali]], [[how-llms-detect-and-correct-their-own-errors-the-role-of-internal-confidence-sig]], [[the-internal-state-of-an-llm-knows-when-its-lying]]

- [consensus] Post-training (instruction tuning, RLHF, RL with verifiable rewards) degrades token-probability calibration relative to the base model in general NLP. | scope: General-domain (MMLU, QA, math); code evidence limited to characterizing-overconfident at token level | sources: [[gpt-4-technical-report]], [[large-language-models-are-overconfident-in-their-own-responses]], [[trained-on-tokens-calibrated-on-conceptsthe-emergence-of-semantic-calibration-in]], [[beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty-2]], [[post-training-shifts-confidence-a-three-stage-analysis-of-how-sft-rl-and-opd-sha]]

- [consensus] Verbal confidence from small or mid-size instruct models is often degenerate (saturated near a ceiling or collapsed into few values), and its behavior depends on elicitation format. | scope: Mixed: code (verbalized-uncertainty) and general-domain; verbal-confidence-saturation and measurement-validity may share an author line (pre-registered validity series), counted cautiously | sources: [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]], [[260722034-small-vlms-know-when-wrong-but-cannot-say-so-full-text]], [[verbal-confidence-saturation-in-3-9b-open-weight-instruction-tuned-llms-a-pre-re]], [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]], [[can-llms-express-their-uncertainty-an-empirical-evaluation-of-confidence-elicita]]

- [consensus] Under a matched sampling budget, self-repair with feedback is often no better than independent resampling on code. | scope: Code with execution labels | sources: [[is-self-repair-a-silver-bullet-for-code-generation]], [[falsification-not-exposure-placebo-controlled-decomposition-of-self-repair-feedb]], [[code-correctness-is-linearly-decodable-from-llm-hidden-states-before-generation]]

- [consensus] Agreement- or confidence-based adaptive sampling and early stopping reduce compute at near-equal accuracy on mostly solvable reasoning workloads. | scope: Mostly general-domain math and reasoning (lets-sample includes code datasets); contested for hard workloads by give-up-to-get-more | sources: [[lets-sample-step-by-stepadaptive-consistency-for-efficient-reasoning-and-coding]], [[efficient-test-time-scaling-via-self-calibration]], [[zero-overhead-introspectionfor-adaptive-test-time-compute]], [[1introduction-2]], [[reasoning-models-know-when-theyre-right-probing-hidden-states-for-self-verificat]]

- [consensus] Execution-based selection among sampled programs (generated-test agreement, behavior clustering, execution-result MBR, execution-aware verifiers) improves over plain generation. | scope: Code with execution labels | sources: [[codet-code-generation-with-generated-tests]], [[competition-level-code-generation-with-alphacode]], [[natural-language-to-code-translation-with-execution]], [[lever-learning-to-verify-language-to-code-generation-with-execution]], [[inference-time-code-selection-via-symbolic-equivalence-partitioning-full-text]]

- [consensus] Fine-grained (token- or line-level) localization of likely-faulty code from model signals is feasible and already demonstrated. | scope: Code; labels are repair patches, edits, or execution outcomes rather than per-requirement test groups | sources: [[251224560-localized-calibrated-uncertainty-in-code-language-models-full-text]], [[abstract]], [[risk-assessment-framework-for-code-llms-via-leveraging-internal-states]], [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]], [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement-2]], [[semguard-real-time-semantic-evaluator-for-correcting-llm-generated-code]]

- [consensus] Signal-detection and psychometric framings (type-2 AUROC, meta-d', sensitivity versus bias, validity screening) are already applied to LLM confidence outside code. | scope: General-domain; none on code with execution labels | sources: [[do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec]], [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]], [[measuring-some-aspects-of-the-metacognition-of-ai]], [[the-metacognitive-monitoring-battery-a-cross-domain-benchmark-for-llm-self-monit]], [[metacognition-and-uncertainty-communication-in-humans-and-large-language-models]], [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]

### Contested claim pairs (top 5 of contradiction-graph.json)

- **probe-vs-own-readout-on-code**: On code with execution labels, does a hidden-state probe beat the model's own output readouts (verbal confidence, log-probability, softmax entropy, yes/no token probability)?
  - Side A: Yes: probes beat the model's own readouts on code correctness, at whole-solution, line, and diffusion-step granularity. ([[on-llms-internal-representation-of-code-correctness]], [[250112934-correctness-assessment-of-code-generated-by-large-language-models-usin]], [[251002934-autoprobe-model-agnostic-correctness-assessment-full-text]], [[251224560-localized-calibrated-uncertainty-in-code-language-models-full-text]], [[probing-functional-correctness-in-diffusion-language-models-full-text]], [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]], [[abstract]])
  - Side B: No consistent advantage: matched against the model's own confidence, the probe ties or loses, and the advantage depends on setting and probe configuration. ([[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]], [[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]], [[on-the-robustness-of-llms-internal-representation-of-code-correctness]], [[1introduction]])

- **verbal-confidence-on-code-informative-or-chance**: Is a code model's stated (verbal or reflective) confidence informative about execution correctness, or near chance?
  - Side A: Informative in some cells: verbal confidence reaches useful AUROC for some models and strategies, can be improved by prompting plus Platt scaling, and is judged the most practical elicitation. ([[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]], [[an-empirical-study-of-security-calibration-in-large-language-models-for-code]], [[open-the-oyster-empirical-evaluation-and-improvement-of-code-reasoning-confidenc]], [[240202047-calibration-and-correctness-of-language-models-for-code]])
  - Side B: Near chance or erratic: reflective confidence is inconsistent, often no better than random at ranking code, and prompted abstention fails. ([[on-llms-internal-representation-of-code-correctness]], [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]], [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]], [[1introduction]], [[calibration-and-correctness-of-language-models-for-code]], [[verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl]])

- **sampling-agreement-vs-single-pass-on-code**: Is sampling agreement (functional or semantic clustering of sampled programs) a stronger correctness signal on code than single-pass readouts?
  - Side A: Yes: sampled-agreement readouts, when clustered by execution or symbolic equivalence, are the strongest black-box code signals. ([[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]], [[using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation]], [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]], [[showing-llm-generated-code-selectively-based-on-confidence-of-llms]], [[1introduction]], [[assessing-correctness-in-llm-based-code-generation-via-uncertainty-estimation]])
  - Side B: No: single-pass signals match sampling at lower cost, and sample agreement gives no consistent advantage once difficulty is controlled or when samples share correlated errors. ([[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]], [[code-is-more-than-text-uncertainty-estimation-for-code-generation]], [[inference-time-code-selection-via-symbolic-equivalence-partitioning-full-text]], [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]], [[an-empirical-study-of-security-calibration-in-large-language-models-for-code]])

- **pooled-vs-within-problem-discrimination**: Do code-correctness predictors (probes, confidence, failure predictors) discriminate correct from incorrect solutions of the same problem, or mainly identify hard problems?
  - Side A: Mainly difficulty: pooled AUROC is dominated by cross-problem pairs, run-blind difficulty references match or beat predictors, and pre-generation signals reflect prompt difficulty. ([[which-signals-of-code-correctness-survive-distribution-shift-hidden-state-and-ca]], [[disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction]], [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]], [[probing-functional-correctness-in-diffusion-language-models-full-text]], [[continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents]])
  - Side B: Within-problem signal exists: probes and likelihood separate correct from incorrect variants of the same task, and pre-generation probes survive length controls. ([[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]], [[semantic-vs-structural-signals-log-probability-and-llm-as-a-judge-for-reference]], [[on-llms-internal-representation-of-code-correctness]], [[260614530-code-correctness-linearly-decodable-from-hidden-states-before-generati]])

- **token-probability-informative-on-code**: Are token probabilities, log-likelihood, or token entropy informative about code correctness?
  - Side A: Informative: log-probability and token entropy carry real correctness or fault-location signal, sometimes matching sampling or probes. ([[semantic-vs-structural-signals-log-probability-and-llm-as-a-judge-for-reference]], [[code-is-more-than-text-uncertainty-estimation-for-code-generation]], [[a-heckler-in-the-hidden-statecorrectness-signals-in-diffusion-language-models]], [[enhancing-automated-program-repair-via-faulty-token-localization-and-quality-awa]], [[adadec-a-uncertainty-guided-lookahead-decoding-framework-for-llm-based-code-gene]])
  - Side B: Weak or misleading: token-level confidence barely discriminates pass from fail, is badly calibrated, and can anti-correlate with quality. ([[semantic-vs-structural-signals-log-probability-and-llm-as-a-judge-for-reference]], [[assessing-correctness-in-llm-based-code-generation-via-uncertainty-estimation]], [[characterizing-overconfident-failure-in-llm-based-code-generation-full-text]], [[multicalibration-for-llm-based-code-generation]], [[generation-probabilities-are-not-enough-uncertainty-highlighting-in-ai-code-comp]], [[260207670-surprisal-guided-selection-for-execution-grounded-code-generation-full]], [[240202047-calibration-and-correctness-of-language-models-for-code]])
