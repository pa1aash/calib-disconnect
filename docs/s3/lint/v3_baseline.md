# Prose lint report: papers/v3/main.tex

Mode: latex. HARD: 138. WARN: 20. Total: 158.

## Counts by category

| Category | HARD | WARN | Total |
| --- | ---: | ---: | ---: |
| negation_not_but | 3 | 0 | 3 |
| negation_cascade | 0 | 1 | 1 |
| rather_than | 0 | 10 | 10 |
| significance_announcer | 2 | 0 | 2 |
| significantly | 0 | 0 | 0 |
| negation_comma_not | 0 | 3 | 3 |
| roadmap | 6 | 0 | 6 |
| softening_adverb | 0 | 4 | 4 |
| contradictory_pair | 0 | 0 | 0 |
| cleft_what | 0 | 0 | 0 |
| cleft_it_that | 0 | 0 | 0 |
| cleft_there_which | 0 | 0 | 0 |
| heading | 2 | 0 | 2 |
| caption_length | 1 | 0 | 1 |
| short_paragraph_end | 0 | 2 | 2 |
| internal_label | 0 | 0 | 0 |
| process_word | 0 | 0 | 0 |
| file_path | 0 | 0 | 0 |
| underscore_identifier | 0 | 0 | 0 |
| decimal_in_prose | 121 | 0 | 121 |
| pvalue_precision | 0 | 0 | 0 |
| mc_precision | 0 | 0 | 0 |
| british_spelling | 0 | 0 | 0 |
| em_dash | 1 | 0 | 1 |
| title | 2 | 0 | 2 |

## Findings

### negation_not_but (3)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 102:649 | HARD | not a lack of internal signal but | \citet{spiess2025calibration} provided the first rigorous study of calibration in code LLMs at ICSE 2025, demonstrating that token-level probabilities are poor predictors of functional correctness and that calibration varies substantially across problem difficulty. \citet{campos2025multicalibrati... |
| 357:682 | HARD | not specific to Qwen2.5-Coder but | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 588:969 | HARD | not temperature mismatch but | The consistent failure of verbal confidence across both temperatures points to structural limitations rather than prompting or temperature deficiencies. RLHF and preference optimization incentivize appearing confident, as human annotators tend to prefer authoritative-sounding responses~\citep{tia... |

### negation_cascade (1)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 593:427 | WARN | Token-level probabilities measure the model's confidence in its token choices, not in the functio... (3 consecutive sentences rule out alternatives) | The isotonic regression and Platt scaling results provide a clean empirical answer to a natural question: is log-probability's poor AUROC due to miscalibration (a fixable mapping problem) or poor discrimination (a fundamental information problem)? The answer is unambiguous. Post-hoc methods impro... |

### rather_than (10)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 66:1078 | WARN | rather than | AI coding assistants present all generated code with equal certainty, providing developers no signal for calibrating trust. We conduct the first systematic comparison of seven confidence estimation methods for code language models, spanning sampling consistency, token log-probabilities with post-... |
| 86:164 | WARN | rather than | \item We show that confidence-calibrated SFT reduces verbal ECE by 64\% but per-problem discrimination analysis reveals the improvement reflects better defaults rather than problem-sensitive uncertainty. |
| 108:84 | WARN | rather than | A nascent line of work addresses calibration through the training objective itself rather than post-hoc correction. \citet{stangel2025rewarding} proposed Rewarding Doubt, which incorporates proper scoring rule rewards into RLHF to encourage calibrated verbal confidence during RL training. Related... |
| 124:348 | WARN | rather than | We distinguish three properties of a confidence estimator. \emph{Calibration} requires that among problems assigned confidence $c$, a fraction $c$ are correct. \emph{Discrimination} requires that correct problems receive higher confidence than incorrect ones. \emph{Sharpness} requires that the co... |
| 574:258 | WARN | rather than | \caption{Verbal confidence distribution: base vs.\ SFT on the 80-problem subset. The base model distributes across $\{1.0, 0.8, 0.6\}$. SFT collapses to a single default (0.9 for 95\% of problems), achieving better calibration through a more accurate prior rather than problem-sensitive discrimina... |
| 588:103 | WARN | rather than | The consistent failure of verbal confidence across both temperatures points to structural limitations rather than prompting or temperature deficiencies. RLHF and preference optimization incentivize appearing confident, as human annotators tend to prefer authoritative-sounding responses~\citep{tia... |
| 608:245 | WARN | rather than | The SFT analysis reveals a subtle but important distinction between calibration and discrimination. The 64\% ECE reduction is genuine and practically meaningful, but it arises from the model learning a better-calibrated default confidence (0.9 rather than 1.0) that happens to be close to the marg... |
| 616:630 | WARN | rather than | Our study evaluates two models on a single benchmark. While the consistency of findings across Qwen2.5-Coder and DeepSeek-Coder, across four temperatures, and across four sample counts suggests robustness, extending to additional model families and sizes is necessary for universality claims. Huma... |
| 626:477 | WARN | rather than | We have conducted the first systematic comparison of seven confidence estimation methods for code language models, using an independent labeling protocol, two models, post-hoc calibration baselines, a test-free AST proxy, and the TACE metric. Our central finding is a robust calibration disconnect... |
| 626:689 | WARN | rather than | We have conducted the first systematic comparison of seven confidence estimation methods for code language models, using an independent labeling protocol, two models, post-hoc calibration baselines, a test-free AST proxy, and the TACE metric. Our central finding is a robust calibration disconnect... |

### significance_announcer (2)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 331:61 | HARD | noteworthy | The AST clustering proxy achieves AUROC\,=\,0.689, which is noteworthy for a method requiring no test execution. Its discrimination is comparable to raw log-probability (0.668) and substantially exceeds verbal confidence (0.564 at $\tau$\,=\,0.1). The high ECE (0.351) reflects systematic overconf... |
| 357:317 | HARD | particularly striking | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |

### negation_comma_not (3)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 66:1482 | WARN | , not problem-sensitive | AI coding assistants present all generated code with equal certainty, providing developers no signal for calibrating trust. We conduct the first systematic comparison of seven confidence estimation methods for code language models, spanning sampling consistency, token log-probabilities with post-... |
| 84:205 | WARN | , not a | \item We demonstrate via cross-validated isotonic regression and Platt scaling that post-hoc calibration cannot rescue log-probability discrimination (AUROC degrades), proving the failure is fundamental, not a calibration artifact. |
| 593:504 | WARN | , not in | The isotonic regression and Platt scaling results provide a clean empirical answer to a natural question: is log-probability's poor AUROC due to miscalibration (a fixable mapping problem) or poor discrimination (a fundamental information problem)? The answer is unambiguous. Post-hoc methods impro... |

### roadmap (6)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 216:1 | HARD | Table~\ref{tab:main} presents | Table~\ref{tab:main} presents calibration metrics for all seven confidence methods on HumanEval with bootstrap 95\% confidence intervals, using the independent labeling protocol. The independent-label pass@1 is 0.823. |
| 251:1 | HARD | Figure~\ref{fig:reliability} presents | Figure~\ref{fig:reliability} presents reliability diagrams comparing sampling and verbal ($\tau$\,=\,0.1) confidence. The sampling diagram closely tracks the perfect-calibration diagonal, with points spanning the full $[0,1]$ confidence range. The high-confidence region contains the majority of p... |
| 336:1 | HARD | Table~\ref{tab:deepseek} presents | Table~\ref{tab:deepseek} presents results for DeepSeek-Coder-6.7B-Instruct, which achieves pass@1\,=\,0.000 on HumanEval due to an instruction-format mismatch (the model produces completions incompatible with the test harness). While AUROC is undefined with a single class, ECE remains informative... |
| 362:1 | HARD | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 424:1 | HARD | Table~\ref{tab:samples} and Figure~\ref{fig:samples_tradeoff} present | Table~\ref{tab:samples} and Figure~\ref{fig:samples_tradeoff} present the sample count analysis. Even $n$\,=\,3 achieves excellent calibration (ECE\,=\,0.025, AUROC\,=\,0.998) at only 6.5 seconds of latency. Increasing beyond $n$\,=\,3 provides no meaningful ECE improvement; the slight increase a... |
| 499:1 | HARD | Table~\ref{tab:sft} presents | Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT model reduces verbal ECE from 0.148 to 0.053 (64\% reduction) with negligible impact on code quality (pass@1: 0.950\,$\rightarrow$\,0.938). However, AUROC improves only marginally (0.428\,$\rightarrow$\,0.47... |

### softening_adverb (4)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 105:470 | WARN | particularly | \citet{wang2023selfconsistency} demonstrated that sampling multiple reasoning paths and aggregating by majority vote provides a natural confidence estimate through agreement rates. \citet{kuhn2023semantic} introduced semantic uncertainty, which clusters generations by meaning before computing unc... |
| 357:478 | WARN | relatively | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 362:454 | WARN | effectively | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 608:516 | WARN | essentially | The SFT analysis reveals a subtle but important distinction between calibration and discrimination. The 64\% ECE reduction is genuine and practically meaningful, but it arises from the model learning a better-calibrated default confidence (0.9 rather than 1.0) that happens to be close to the marg... |

### heading (2)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 328:13 | HARD | Test-Free Confidence: AST Clustering (contains ':' or '?') | \subsection{Test-Free Confidence: AST Clustering} |
| 605:13 | HARD | SFT: Better Defaults Without Discrimination (contains ':' or '?') | \subsection{SFT: Better Defaults Without Discrimination} |

### caption_length (1)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 419:10 | HARD | ECE vs. sampling temperature on HumanEval subset. Sampling ECE increases gradually with but remai... (4 sentences (max 3)) | \caption{ECE vs.\ sampling temperature on HumanEval subset. Sampling ECE increases gradually with $\tau$ but remains below 0.05. Log-probability ECE is volatile. Verbal ECE is flat (elicited at fixed $\tau$\,=\,0.1).} |

### short_paragraph_end (2)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 216:180 | WARN | The independent-label pass@1 is 0.823. (final sentence has 5 words) | Table~\ref{tab:main} presents calibration metrics for all seven confidence methods on HumanEval with bootstrap 95\% confidence intervals, using the independent labeling protocol. The independent-label pass@1 is 0.823. |
| 518:397 | WARN | In contrast, the base model distributes confidence across $\{1.0{:}\,37, 0.8{:}\,27, 0.6{:}\,16\}$. (final sentence has 8 words) | To understand why, we analyze the SFT model's discrimination on easy and hard problem subsets (Table~\ref{tab:sft_disc}). The SFT model assigns mean confidence of 0.900 to \emph{both} easy problems (pass\,$\geq$\,0.8, $n$\,=\,73) and hard problems (pass\,$<$\,0.5, $n$\,=\,5). Its verbal confidenc... |

### decimal_in_prose (121)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 66:646 | HARD | 6.7 | AI coding assistants present all generated code with equal certainty, providing developers no signal for calibrating trust. We conduct the first systematic comparison of seven confidence estimation methods for code language models, spanning sampling consistency, token log-probabilities with post-... |
| 66:869 | HARD | 0.059 | AI coding assistants present all generated code with equal certainty, providing developers no signal for calibrating trust. We conduct the first systematic comparison of seven confidence estimation methods for code language models, spanning sampling consistency, token log-probabilities with post-... |
| 66:886 | HARD | 0.987 | AI coding assistants present all generated code with equal certainty, providing developers no signal for calibrating trust. We conduct the first systematic comparison of seven confidence estimation methods for code language models, spanning sampling consistency, token log-probabilities with post-... |
| 79:163 | HARD | 0.987 | Our key finding is a striking calibration disconnect: the internal uncertainty signal available through repeated sampling is near-perfectly calibrated (AUROC\,=\,0.987 with independent labels), while all alternative methods fail to provide reliable correctness predictions. Post-hoc calibration of... |
| 79:490 | HARD | 0.689 | Our key finding is a striking calibration disconnect: the internal uncertainty signal available through repeated sampling is near-perfectly calibrated (AUROC\,=\,0.987 with independent labels), while all alternative methods fail to provide reliable correctness predictions. Post-hoc calibration of... |
| 79:517 | HARD | 6.7 | Our key finding is a striking calibration disconnect: the internal uncertainty signal available through repeated sampling is near-perfectly calibrated (AUROC\,=\,0.987 with independent labels), while all alternative methods fail to provide reliable correctness predictions. Post-hoc calibration of... |
| 85:86 | HARD | 0.689 | \item We introduce AST-based clustering as a test-free confidence proxy (AUROC\,=\,0.689) and validate findings across two models (Qwen2.5-Coder-7B, DeepSeek-Coder-6.7B). |
| 85:167 | HARD | 6.7 | \item We introduce AST-based clustering as a test-free confidence proxy (AUROC\,=\,0.689) and validate findings across two models (Qwen2.5-Coder-7B, DeepSeek-Coder-6.7B). |
| 159:42 | HARD | 0.1 | \paragraph{Verbal confidence ($\tau$\,=\,0.1).} |
| 160:52 | HARD | 0.1 | We prompt the model at low temperature ($\tau$\,=\,0.1) to generate a solution and rate its confidence on a scale mapped to $\{0.2, 0.4, 0.6, 0.8, 1.0\}$. The prompt instructs: ``Rate your confidence that this solution is correct on a scale of 1--5.'' This is the standard verbal elicitation used ... |
| 162:42 | HARD | 0.8 | \paragraph{Verbal confidence ($\tau$\,=\,0.8).} |
| 163:79 | HARD | 0.8 | To enable an apples-to-apples comparison with sampling (which uses $\tau$\,=\,0.8), we also elicit verbal confidence at the \emph{same} temperature. If verbal confidence is poor only because of the temperature mismatch, this condition should substantially improve calibration. |
| 200:135 | HARD | 6.7 | We evaluate two models: \textbf{Qwen2.5-Coder-7B-Instruct}~\citep{hui2024qwen25coder} as our primary model and \textbf{DeepSeek-Coder-6.7B-Instruct}~\citep{guo2024deepseek} for cross-model validation. Experiments use HumanEval~\citep{chen2021evaluating} (164 problems) loaded from the \texttt{open... |
| 200:427 | HARD | 0.8 | We evaluate two models: \textbf{Qwen2.5-Coder-7B-Instruct}~\citep{hui2024qwen25coder} as our primary model and \textbf{DeepSeek-Coder-6.7B-Instruct}~\citep{guo2024deepseek} for cross-model validation. Experiments use HumanEval~\citep{chen2021evaluating} (164 problems) loaded from the \texttt{open... |
| 200:710 | HARD | 0.95 | We evaluate two models: \textbf{Qwen2.5-Coder-7B-Instruct}~\citep{hui2024qwen25coder} as our primary model and \textbf{DeepSeek-Coder-6.7B-Instruct}~\citep{guo2024deepseek} for cross-model validation. Experiments use HumanEval~\citep{chen2021evaluating} (164 problems) loaded from the \texttt{open... |
| 200:755 | HARD | 2.18 | We evaluate two models: \textbf{Qwen2.5-Coder-7B-Instruct}~\citep{hui2024qwen25coder} as our primary model and \textbf{DeepSeek-Coder-6.7B-Instruct}~\citep{guo2024deepseek} for cross-model validation. Experiments use HumanEval~\citep{chen2021evaluating} (164 problems) loaded from the \texttt{open... |
| 205:340 | HARD | 0.9 | To explore whether verbal confidence can be improved through training, we constructed a 274-example SFT dataset from HumanEval execution feedback. Using the 10-sample results as ground-truth difficulty indicators, each training example includes a solution paired with a verbal confidence tier: ``I... |
| 205:423 | HARD | 0.6 | To explore whether verbal confidence can be improved through training, we constructed a 274-example SFT dataset from HumanEval execution feedback. Using the 10-sample results as ground-truth difficulty indicators, each training example includes a solution paired with a verbal confidence tier: ``I... |
| 205:515 | HARD | 0.3 | To explore whether verbal confidence can be improved through training, we constructed a 274-example SFT dataset from HumanEval execution feedback. Using the 10-sample results as ground-truth difficulty indicators, each training example includes a solution paired with a verbal confidence tier: ``I... |
| 216:212 | HARD | 0.823 | Table~\ref{tab:main} presents calibration metrics for all seven confidence methods on HumanEval with bootstrap 95\% confidence intervals, using the independent labeling protocol. The independent-label pass@1 is 0.823. |
| 218:109 | HARD | 0.059 | Sampling-based confidence achieves the best calibration across all metrics by a substantial margin: ECE\,=\,0.059, Brier\,=\,0.036, AUROC\,=\,0.987, and TACE\,=\,0.041. The AUROC of 0.987 under independent labeling confirms that sampling's excellent discrimination is not an artifact of statistica... |
| 218:126 | HARD | 0.036 | Sampling-based confidence achieves the best calibration across all metrics by a substantial margin: ECE\,=\,0.059, Brier\,=\,0.036, AUROC\,=\,0.987, and TACE\,=\,0.041. The AUROC of 0.987 under independent labeling confirms that sampling's excellent discrimination is not an artifact of statistica... |
| 218:143 | HARD | 0.987 | Sampling-based confidence achieves the best calibration across all metrics by a substantial margin: ECE\,=\,0.059, Brier\,=\,0.036, AUROC\,=\,0.987, and TACE\,=\,0.041. The AUROC of 0.987 under independent labeling confirms that sampling's excellent discrimination is not an artifact of statistica... |
| 218:163 | HARD | 0.041 | Sampling-based confidence achieves the best calibration across all metrics by a substantial margin: ECE\,=\,0.059, Brier\,=\,0.036, AUROC\,=\,0.987, and TACE\,=\,0.041. The AUROC of 0.987 under independent labeling confirms that sampling's excellent discrimination is not an artifact of statistica... |
| 218:183 | HARD | 0.987 | Sampling-based confidence achieves the best calibration across all metrics by a substantial margin: ECE\,=\,0.059, Brier\,=\,0.036, AUROC\,=\,0.987, and TACE\,=\,0.041. The AUROC of 0.987 under independent labeling confirms that sampling's excellent discrimination is not an artifact of statistica... |
| 220:53 | HARD | 0.058 | Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimination (AUROC\,=\,0.668) and a higher Brier score (0.122). The critical test comes from the post-hoc calibration baselines. Isotonic regression (5-fold CV) reduces ECE to 0.047 but degrades AUROC to 0.587. P... |
| 220:109 | HARD | 0.668 | Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimination (AUROC\,=\,0.668) and a higher Brier score (0.122). The critical test comes from the post-hoc calibration baselines. Isotonic regression (5-fold CV) reduces ECE to 0.047 but degrades AUROC to 0.587. P... |
| 220:142 | HARD | 0.122 | Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimination (AUROC\,=\,0.668) and a higher Brier score (0.122). The critical test comes from the post-hoc calibration baselines. Isotonic regression (5-fold CV) reduces ECE to 0.047 but degrades AUROC to 0.587. P... |
| 220:262 | HARD | 0.047 | Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimination (AUROC\,=\,0.668) and a higher Brier score (0.122). The critical test comes from the post-hoc calibration baselines. Isotonic regression (5-fold CV) reduces ECE to 0.047 but degrades AUROC to 0.587. P... |
| 220:290 | HARD | 0.587 | Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimination (AUROC\,=\,0.668) and a higher Brier score (0.122). The critical test comes from the post-hoc calibration baselines. Isotonic regression (5-fold CV) reduces ECE to 0.047 but degrades AUROC to 0.587. P... |
| 220:328 | HARD | 0.003 | Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimination (AUROC\,=\,0.668) and a higher Brier score (0.122). The critical test comes from the post-hoc calibration baselines. Isotonic regression (5-fold CV) reduces ECE to 0.047 but degrades AUROC to 0.587. P... |
| 220:373 | HARD | 0.386 | Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimination (AUROC\,=\,0.668) and a higher Brier score (0.122). The critical test comes from the post-hoc calibration baselines. Isotonic regression (5-fold CV) reduces ECE to 0.047 but degrades AUROC to 0.587. P... |
| 222:35 | HARD | 0.689 | AST clustering achieves AUROC\,=\,0.689 without requiring test execution, comparable to raw log-probability's 0.668. Its high ECE (0.351) reflects a systematic bias toward overconfidence, since structurally similar programs may differ in corner-case behavior. Nonetheless, as a test-free proxy, it... |
| 222:111 | HARD | 0.668 | AST clustering achieves AUROC\,=\,0.689 without requiring test execution, comparable to raw log-probability's 0.668. Its high ECE (0.351) reflects a systematic bias toward overconfidence, since structurally similar programs may differ in corner-case behavior. Nonetheless, as a test-free proxy, it... |
| 222:132 | HARD | 0.351 | AST clustering achieves AUROC\,=\,0.689 without requiring test execution, comparable to raw log-probability's 0.668. Its high ECE (0.351) reflects a systematic bias toward overconfidence, since structurally similar programs may differ in corner-case behavior. Nonetheless, as a test-free proxy, it... |
| 224:69 | HARD | 0.1 | Both verbal methods perform poorly. Verbal confidence at $\tau$\,=\,0.1 achieves ECE\,=\,0.079 and AUROC\,=\,0.564, while verbal confidence at the matching $\tau$\,=\,0.8 is worse on every metric (ECE\,=\,0.113, AUROC\,=\,0.519). The matched-temperature condition rules out the hypothesis that ver... |
| 224:90 | HARD | 0.079 | Both verbal methods perform poorly. Verbal confidence at $\tau$\,=\,0.1 achieves ECE\,=\,0.079 and AUROC\,=\,0.564, while verbal confidence at the matching $\tau$\,=\,0.8 is worse on every metric (ECE\,=\,0.113, AUROC\,=\,0.519). The matched-temperature condition rules out the hypothesis that ver... |
| 224:110 | HARD | 0.564 | Both verbal methods perform poorly. Verbal confidence at $\tau$\,=\,0.1 achieves ECE\,=\,0.079 and AUROC\,=\,0.564, while verbal confidence at the matching $\tau$\,=\,0.8 is worse on every metric (ECE\,=\,0.113, AUROC\,=\,0.519). The matched-temperature condition rules out the hypothesis that ver... |
| 224:168 | HARD | 0.8 | Both verbal methods perform poorly. Verbal confidence at $\tau$\,=\,0.1 achieves ECE\,=\,0.079 and AUROC\,=\,0.564, while verbal confidence at the matching $\tau$\,=\,0.8 is worse on every metric (ECE\,=\,0.113, AUROC\,=\,0.519). The matched-temperature condition rules out the hypothesis that ver... |
| 224:206 | HARD | 0.113 | Both verbal methods perform poorly. Verbal confidence at $\tau$\,=\,0.1 achieves ECE\,=\,0.079 and AUROC\,=\,0.564, while verbal confidence at the matching $\tau$\,=\,0.8 is worse on every metric (ECE\,=\,0.113, AUROC\,=\,0.519). The matched-temperature condition rules out the hypothesis that ver... |
| 224:223 | HARD | 0.519 | Both verbal methods perform poorly. Verbal confidence at $\tau$\,=\,0.1 achieves ECE\,=\,0.079 and AUROC\,=\,0.564, while verbal confidence at the matching $\tau$\,=\,0.8 is worse on every metric (ECE\,=\,0.113, AUROC\,=\,0.519). The matched-temperature condition rules out the hypothesis that ver... |
| 228:68 | HARD | 0.8 | \caption{Calibration results on HumanEval ($n$\,=\,164, $\tau$\,=\,0.8, 10 samples, independent labels). pass@1\,=\,0.823. All intervals are bootstrap 95\% CIs from 1{,}000 iterations. Best values in bold.} |
| 228:117 | HARD | 0.823 | \caption{Calibration results on HumanEval ($n$\,=\,164, $\tau$\,=\,0.8, 10 samples, independent labels). pass@1\,=\,0.823. All intervals are bootstrap 95\% CIs from 1{,}000 iterations. Best values in bold.} |
| 251:102 | HARD | 0.1 | Figure~\ref{fig:reliability} presents reliability diagrams comparing sampling and verbal ($\tau$\,=\,0.1) confidence. The sampling diagram closely tracks the perfect-calibration diagonal, with points spanning the full $[0,1]$ confidence range. The high-confidence region contains the majority of p... |
| 251:333 | HARD | 1.0 | Figure~\ref{fig:reliability} presents reliability diagrams comparing sampling and verbal ($\tau$\,=\,0.1) confidence. The sampling diagram closely tracks the perfect-calibration diagonal, with points spanning the full $[0,1]$ confidence range. The high-confidence region contains the majority of p... |
| 251:607 | HARD | 0.6 | Figure~\ref{fig:reliability} presents reliability diagrams comparing sampling and verbal ($\tau$\,=\,0.1) confidence. The sampling diagram closely tracks the perfect-calibration diagonal, with points spanning the full $[0,1]$ confidence range. The high-confidence region contains the majority of p... |
| 318:201 | HARD | 0.1 | \caption{Reliability diagrams for Qwen2.5-Coder-7B on HumanEval. \textbf{(a)} Sampling confidence closely tracks the diagonal across the full $[0,1]$ range. \textbf{(b)} Verbal confidence ($\tau$\,=\,0.1) collapses to three bins in $[0.6, 1.0]$ with 67\% at maximum confidence.} |
| 326:253 | HARD | 0.058 | The post-hoc calibration results in Table~\ref{tab:main} provide the strongest evidence that log-probability's poor performance reflects a fundamental discrimination weakness. Isotonic regression, a flexible non-parametric calibrator, reduces ECE from 0.058 to 0.047 but degrades AUROC from 0.668 ... |
| 326:262 | HARD | 0.047 | The post-hoc calibration results in Table~\ref{tab:main} provide the strongest evidence that log-probability's poor performance reflects a fundamental discrimination weakness. Isotonic regression, a flexible non-parametric calibrator, reduces ECE from 0.058 to 0.047 but degrades AUROC from 0.668 ... |
| 326:292 | HARD | 0.668 | The post-hoc calibration results in Table~\ref{tab:main} provide the strongest evidence that log-probability's poor performance reflects a fundamental discrimination weakness. Isotonic regression, a flexible non-parametric calibrator, reduces ECE from 0.058 to 0.047 but degrades AUROC from 0.668 ... |
| 326:301 | HARD | 0.587 | The post-hoc calibration results in Table~\ref{tab:main} provide the strongest evidence that log-probability's poor performance reflects a fundamental discrimination weakness. Isotonic regression, a flexible non-parametric calibrator, reduces ECE from 0.058 to 0.047 but degrades AUROC from 0.668 ... |
| 326:349 | HARD | 0.003 | The post-hoc calibration results in Table~\ref{tab:main} provide the strongest evidence that log-probability's poor performance reflects a fundamental discrimination weakness. Isotonic regression, a flexible non-parametric calibrator, reduces ECE from 0.058 to 0.047 but degrades AUROC from 0.668 ... |
| 326:525 | HARD | 0.386 | The post-hoc calibration results in Table~\ref{tab:main} provide the strongest evidence that log-probability's poor performance reflects a fundamental discrimination weakness. Isotonic regression, a flexible non-parametric calibrator, reduces ECE from 0.058 to 0.047 but degrades AUROC from 0.668 ... |
| 331:45 | HARD | 0.689 | The AST clustering proxy achieves AUROC\,=\,0.689, which is noteworthy for a method requiring no test execution. Its discrimination is comparable to raw log-probability (0.668) and substantially exceeds verbal confidence (0.564 at $\tau$\,=\,0.1). The high ECE (0.351) reflects systematic overconf... |
| 331:171 | HARD | 0.668 | The AST clustering proxy achieves AUROC\,=\,0.689, which is noteworthy for a method requiring no test execution. Its discrimination is comparable to raw log-probability (0.668) and substantially exceeds verbal confidence (0.564 at $\tau$\,=\,0.1). The high ECE (0.351) reflects systematic overconf... |
| 331:223 | HARD | 0.564 | The AST clustering proxy achieves AUROC\,=\,0.689, which is noteworthy for a method requiring no test execution. Its discrimination is comparable to raw log-probability (0.668) and substantially exceeds verbal confidence (0.564 at $\tau$\,=\,0.1). The high ECE (0.351) reflects systematic overconf... |
| 331:243 | HARD | 0.1 | The AST clustering proxy achieves AUROC\,=\,0.689, which is noteworthy for a method requiring no test execution. Its discrimination is comparable to raw log-probability (0.668) and substantially exceeds verbal confidence (0.564 at $\tau$\,=\,0.1). The high ECE (0.351) reflects systematic overconf... |
| 331:263 | HARD | 0.351 | The AST clustering proxy achieves AUROC\,=\,0.689, which is noteworthy for a method requiring no test execution. Its discrimination is comparable to raw log-probability (0.668) and substantially exceeds verbal confidence (0.564 at $\tau$\,=\,0.1). The high ECE (0.351) reflects systematic overconf... |
| 336:62 | HARD | 6.7 | Table~\ref{tab:deepseek} presents results for DeepSeek-Coder-6.7B-Instruct, which achieves pass@1\,=\,0.000 on HumanEval due to an instruction-format mismatch (the model produces completions incompatible with the test harness). While AUROC is undefined with a single class, ECE remains informative... |
| 336:103 | HARD | 0.000 | Table~\ref{tab:deepseek} presents results for DeepSeek-Coder-6.7B-Instruct, which achieves pass@1\,=\,0.000 on HumanEval due to an instruction-format mismatch (the model produces completions incompatible with the test harness). While AUROC is undefined with a single class, ECE remains informative... |
| 340:49 | HARD | 6.7 | \caption{Cross-model validation: DeepSeek-Coder-6.7B on HumanEval. pass@1\,=\,0.000. AUROC is undefined (single class). ECE reveals systematic overconfidence across all non-sampling methods.} |
| 340:79 | HARD | 0.000 | \caption{Cross-model validation: DeepSeek-Coder-6.7B on HumanEval. pass@1\,=\,0.000. AUROC is undefined (single class). ECE reveals systematic overconfidence across all non-sampling methods.} |
| 357:69 | HARD | 0.000 | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 357:108 | HARD | 0.0 | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 357:125 | HARD | 0.0 | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 357:217 | HARD | 0.886 | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 357:284 | HARD | 0.701 | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 357:294 | HARD | 0.688 | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 357:503 | HARD | 0.140 | Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fail, confidence is 0.0, accuracy is 0.0). In contrast, log-probability assigns high confidence despite 0\% correctness (ECE\,=\,0.886), and verbal methods exhibit extreme overconfidence (ECE\,=\,0.701 and 0.68... |
| 362:202 | HARD | 0.010 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:222 | HARD | 0.2 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:229 | HARD | 0.044 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:249 | HARD | 1.0 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:380 | HARD | 0.566 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:387 | HARD | 0.702 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:476 | HARD | 0.020 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:483 | HARD | 0.028 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 362:534 | HARD | 0.1 | Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset. Sampling ECE increases slightly with temperature (0.010 at $\tau$\,=\,0.2 to 0.044 at $\tau$\,=\,1.0) but AUROC remains near-perfect across all se... |
| 419:124 | HARD | 0.05 | \caption{ECE vs.\ sampling temperature on HumanEval subset. Sampling ECE increases gradually with $\tau$ but remains below 0.05. Log-probability ECE is volatile. Verbal ECE is flat (elicited at fixed $\tau$\,=\,0.1).} |
| 419:212 | HARD | 0.1 | \caption{ECE vs.\ sampling temperature on HumanEval subset. Sampling ECE increases gradually with $\tau$ but remains below 0.05. Log-probability ECE is volatile. Verbal ECE is flat (elicited at fixed $\tau$\,=\,0.1).} |
| 424:153 | HARD | 0.025 | Table~\ref{tab:samples} and Figure~\ref{fig:samples_tradeoff} present the sample count analysis. Even $n$\,=\,3 achieves excellent calibration (ECE\,=\,0.025, AUROC\,=\,0.998) at only 6.5 seconds of latency. Increasing beyond $n$\,=\,3 provides no meaningful ECE improvement; the slight increase a... |
| 424:170 | HARD | 0.998 | Table~\ref{tab:samples} and Figure~\ref{fig:samples_tradeoff} present the sample count analysis. Even $n$\,=\,3 achieves excellent calibration (ECE\,=\,0.025, AUROC\,=\,0.998) at only 6.5 seconds of latency. Increasing beyond $n$\,=\,3 provides no meaningful ECE improvement; the slight increase a... |
| 424:185 | HARD | 6.5 | Table~\ref{tab:samples} and Figure~\ref{fig:samples_tradeoff} present the sample count analysis. Even $n$\,=\,3 achieves excellent calibration (ECE\,=\,0.025, AUROC\,=\,0.998) at only 6.5 seconds of latency. Increasing beyond $n$\,=\,3 provides no meaningful ECE improvement; the slight increase a... |
| 424:320 | HARD | 0.046 | Table~\ref{tab:samples} and Figure~\ref{fig:samples_tradeoff} present the sample count analysis. Even $n$\,=\,3 achieves excellent calibration (ECE\,=\,0.025, AUROC\,=\,0.998) at only 6.5 seconds of latency. Increasing beyond $n$\,=\,3 provides no meaningful ECE improvement; the slight increase a... |
| 428:79 | HARD | 0.8 | \caption{Sample count sensitivity on HumanEval subset ($n$\,=\,80, $\tau$\,=\,0.8). Even $n$\,=\,3 achieves strong calibration. All intervals are bootstrap 95\% CIs.} |
| 491:191 | HARD | 6.5 | \caption{Cost-quality tradeoff for sampling confidence. ECE (left, solid) is flat across sample counts; latency (right, dashed) grows linearly. Even $n$\,=\,3 provides strong calibration at 6.5s overhead.} |
| 499:121 | HARD | 0.148 | Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT model reduces verbal ECE from 0.148 to 0.053 (64\% reduction) with negligible impact on code quality (pass@1: 0.950\,$\rightarrow$\,0.938). However, AUROC improves only marginally (0.428\,$\rightarrow$\,0.47... |
| 499:130 | HARD | 0.053 | Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT model reduces verbal ECE from 0.148 to 0.053 (64\% reduction) with negligible impact on code quality (pass@1: 0.950\,$\rightarrow$\,0.938). However, AUROC improves only marginally (0.428\,$\rightarrow$\,0.47... |
| 499:201 | HARD | 0.950 | Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT model reduces verbal ECE from 0.148 to 0.053 (64\% reduction) with negligible impact on code quality (pass@1: 0.950\,$\rightarrow$\,0.938). However, AUROC improves only marginally (0.428\,$\rightarrow$\,0.47... |
| 499:223 | HARD | 0.938 | Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT model reduces verbal ECE from 0.148 to 0.053 (64\% reduction) with negligible impact on code quality (pass@1: 0.950\,$\rightarrow$\,0.938). However, AUROC improves only marginally (0.428\,$\rightarrow$\,0.47... |
| 499:272 | HARD | 0.428 | Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT model reduces verbal ECE from 0.148 to 0.053 (64\% reduction) with negligible impact on code quality (pass@1: 0.950\,$\rightarrow$\,0.938). However, AUROC improves only marginally (0.428\,$\rightarrow$\,0.47... |
| 499:294 | HARD | 0.473 | Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT model reduces verbal ECE from 0.148 to 0.053 (64\% reduction) with negligible impact on code quality (pass@1: 0.950\,$\rightarrow$\,0.938). However, AUROC improves only marginally (0.428\,$\rightarrow$\,0.47... |
| 518:164 | HARD | 0.900 | To understand why, we analyze the SFT model's discrimination on easy and hard problem subsets (Table~\ref{tab:sft_disc}). The SFT model assigns mean confidence of 0.900 to \emph{both} easy problems (pass\,$\geq$\,0.8, $n$\,=\,73) and hard problems (pass\,$<$\,0.5, $n$\,=\,5). Its verbal confidenc... |
| 518:214 | HARD | 0.8 | To understand why, we analyze the SFT model's discrimination on easy and hard problem subsets (Table~\ref{tab:sft_disc}). The SFT model assigns mean confidence of 0.900 to \emph{both} easy problems (pass\,$\geq$\,0.8, $n$\,=\,73) and hard problems (pass\,$<$\,0.5, $n$\,=\,5). Its verbal confidenc... |
| 518:261 | HARD | 0.5 | To understand why, we analyze the SFT model's discrimination on easy and hard problem subsets (Table~\ref{tab:sft_disc}). The SFT model assigns mean confidence of 0.900 to \emph{both} easy problems (pass\,$\geq$\,0.8, $n$\,=\,73) and hard problems (pass\,$<$\,0.5, $n$\,=\,5). Its verbal confidenc... |
| 518:365 | HARD | 0.9 | To understand why, we analyze the SFT model's discrimination on easy and hard problem subsets (Table~\ref{tab:sft_disc}). The SFT model assigns mean confidence of 0.900 to \emph{both} easy problems (pass\,$\geq$\,0.8, $n$\,=\,73) and hard problems (pass\,$<$\,0.5, $n$\,=\,5). Its verbal confidenc... |
| 518:392 | HARD | 0.6 | To understand why, we analyze the SFT model's discrimination on easy and hard problem subsets (Table~\ref{tab:sft_disc}). The SFT model assigns mean confidence of 0.900 to \emph{both} easy problems (pass\,$\geq$\,0.8, $n$\,=\,73) and hard problems (pass\,$<$\,0.5, $n$\,=\,5). Its verbal confidenc... |
| 522:109 | HARD | 0.900 | \caption{SFT discrimination analysis by difficulty subset. The SFT model assigns identical mean confidence (0.900) to easy and hard problems, indicating no problem-sensitive discrimination.} |
| 537:162 | HARD | 0.9 | Figure~\ref{fig:sft_dist} visualizes this distribution shift. The ECE improvement comes entirely from the SFT model learning a better-calibrated \emph{default} (0.9 is closer to the true pass rate of 0.938 than the base model's mode of 1.0), not from learning to identify which specific problems a... |
| 537:201 | HARD | 0.938 | Figure~\ref{fig:sft_dist} visualizes this distribution shift. The ECE improvement comes entirely from the SFT model learning a better-calibrated \emph{default} (0.9 is closer to the true pass rate of 0.938 than the base model's mode of 1.0), not from learning to identify which specific problems a... |
| 537:237 | HARD | 1.0 | Figure~\ref{fig:sft_dist} visualizes this distribution shift. The ECE improvement comes entirely from the SFT model learning a better-calibrated \emph{default} (0.9 is closer to the true pass rate of 0.938 than the base model's mode of 1.0), not from learning to identify which specific problems a... |
| 574:172 | HARD | 0.9 | \caption{Verbal confidence distribution: base vs.\ SFT on the 80-problem subset. The base model distributes across $\{1.0, 0.8, 0.6\}$. SFT collapses to a single default (0.9 for 95\% of problems), achieving better calibration through a more accurate prior rather than problem-sensitive discrimina... |
| 588:780 | HARD | 0.1 | The consistent failure of verbal confidence across both temperatures points to structural limitations rather than prompting or temperature deficiencies. RLHF and preference optimization incentivize appearing confident, as human annotators tend to prefer authoritative-sounding responses~\citep{tia... |
| 588:929 | HARD | 0.8 | The consistent failure of verbal confidence across both temperatures points to structural limitations rather than prompting or temperature deficiencies. RLHF and preference optimization incentivize appearing confident, as human annotators tend to prefer authoritative-sounding responses~\citep{tia... |
| 598:34 | HARD | 0.987 | The near-perfect sampling AUROC (0.987) means coding agents could provide highly reliable uncertainty signals by generating multiple solutions and computing agreement. Our sample count analysis shows that $n$\,=\,3 suffices, adding only 6.5 seconds at 2.18s per sample. For interactive coding assi... |
| 598:238 | HARD | 6.5 | The near-perfect sampling AUROC (0.987) means coding agents could provide highly reliable uncertainty signals by generating multiple solutions and computing agreement. Our sample count analysis shows that $n$\,=\,3 suffices, adding only 6.5 seconds at 2.18s per sample. For interactive coding assi... |
| 598:253 | HARD | 2.18 | The near-perfect sampling AUROC (0.987) means coding agents could provide highly reliable uncertainty signals by generating multiple solutions and computing agreement. Our sample count analysis shows that $n$\,=\,3 suffices, adding only 6.5 seconds at 2.18s per sample. For interactive coding assi... |
| 598:598 | HARD | 6.5 | The near-perfect sampling AUROC (0.987) means coding agents could provide highly reliable uncertainty signals by generating multiple solutions and computing agreement. Our sample count analysis shows that $n$\,=\,3 suffices, adding only 6.5 seconds at 2.18s per sample. For interactive coding assi... |
| 598:652 | HARD | 0.689 | The near-perfect sampling AUROC (0.987) means coding agents could provide highly reliable uncertainty signals by generating multiple solutions and computing agreement. Our sample count analysis shows that $n$\,=\,3 suffices, adding only 6.5 seconds at 2.18s per sample. For interactive coding assi... |
| 608:241 | HARD | 0.9 | The SFT analysis reveals a subtle but important distinction between calibration and discrimination. The 64\% ECE reduction is genuine and practically meaningful, but it arises from the model learning a better-calibrated default confidence (0.9 rather than 1.0) that happens to be close to the marg... |
| 608:257 | HARD | 1.0 | The SFT analysis reveals a subtle but important distinction between calibration and discrimination. The 64\% ECE reduction is genuine and practically meaningful, but it arises from the model learning a better-calibrated default confidence (0.9 rather than 1.0) that happens to be close to the marg... |
| 608:333 | HARD | 0.938 | The SFT analysis reveals a subtle but important distinction between calibration and discrimination. The 64\% ECE reduction is genuine and practically meaningful, but it arises from the model learning a better-calibrated default confidence (0.9 rather than 1.0) that happens to be close to the marg... |
| 608:437 | HARD | 0.900 | The SFT analysis reveals a subtle but important distinction between calibration and discrimination. The 64\% ECE reduction is genuine and practically meaningful, but it arises from the model learning a better-calibrated default confidence (0.9 rather than 1.0) that happens to be close to the marg... |
| 626:345 | HARD | 0.987 | We have conducted the first systematic comparison of seven confidence estimation methods for code language models, using an independent labeling protocol, two models, post-hoc calibration baselines, a test-free AST proxy, and the TACE metric. Our central finding is a robust calibration disconnect... |
| 659:51 | HARD | 0.1 | \paragraph{Verbal confidence (numeric, $\tau$\,=\,0.1).} |
| 667:42 | HARD | 0.8 | \paragraph{Verbal confidence ($\tau$\,=\,0.8).} |
| 668:75 | HARD | 0.8 | The same prompt as above, but generation temperature is set to $\tau$\,=\,0.8 to match the sampling temperature. |
| 704:58 | HARD | 0.95 | \item \textbf{Generation}: max 512 tokens, top-$p$\,=\,0.95 |
| 706:60 | HARD | 2.5 | \item \textbf{Bootstrap}: 1{,}000 resampling iterations, 2.5th/97.5th percentile CIs |
| 706:66 | HARD | 97.5 | \item \textbf{Bootstrap}: 1{,}000 resampling iterations, 2.5th/97.5th percentile CIs |
| 707:64 | HARD | 1.4 | \item \textbf{Post-hoc calibration}: 5-fold CV, scikit-learn 1.4 |

### em_dash (1)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 205:485 | HARD | --- | To explore whether verbal confidence can be improved through training, we constructed a 274-example SFT dataset from HumanEval execution feedback. Using the 10-sample results as ground-truth difficulty indicators, each training example includes a solution paired with a verbal confidence tier: ``I... |

### title (2)

| Line:Col | Severity | Match | Source line |
| --- | --- | --- | --- |
| 46:19 | HARD | Mind the Gap: Calibration Disconnect in Code Language Models (title contains ':' or '?') | \icmltitlerunning{Mind the Gap: Calibration Disconnect in Code Language Models} |
| 51:12 | HARD | Mind the Gap: The Calibration Disconnect Between Internal and Expressed Confidence in Code Langua... (title contains ':' or '?') | \icmltitle{Mind the Gap: The Calibration Disconnect Between\\Internal and Expressed Confidence in Code Language Models} |

