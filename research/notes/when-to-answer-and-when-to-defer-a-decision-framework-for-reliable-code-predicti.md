---
title: 'When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions'
id: when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-code-predicti
tags:
- code-llm-calibration-aaai27-eabf3f
- locus-code-verbal-calibration-occupied-or-open
- internal-signal
- abstention-not-verbalized
- early-stage-position-paper
- code-llm-confidence-positioning-d82d00
created: '2026-07-17T19:00:32.285506Z'
updated: '2026-11-09T23:29:04.612418Z'
source: https://arxiv.org/html/2605.19369
source_domain: arxiv.org
fetched_at: '2026-07-17T19:00:32.284939Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Rathnasuriya & Yang (UT Dallas, arXiv 2605.19369). A short work-in-progress/position
  paper proposing a deployment framework combining (i) internal uncertainty signals
  for code models, (ii) pre- and post-deployment calibration, and (iii) tool-based
  abstention (routing low-confidence predictions to static analyzers/program-slicing
  tools via an MCP-style interface) rather than answering directly. The confidence
  signal is INTERNAL (entropy-based scores, confidence margins, variance estimators,
  sampling-based disagreement) plus a POST-HOC weighted logistic-scaling recalibration
  (a Platt-scaling variant that upweights incorrect predictions); it also proposes
  'abstention heads' as a pre-deployment training addition, but this is an abstain/reject-class
  head, not a verbalized confidence-expression trained to be discriminative. Evaluated
  on DeepSeek-Coder-7B and CodeLlama-7B on MBPP+ using ECE and Brier score, reporting
  'over 90% selective accuracy at 80% coverage' after calibration -- no AUROC number
  given, and no code-generation benchmark beyond MBPP+ is reported (early-stage/roadmap
  paper, word count ~4.9k, explicitly frames most content as future work). Confirms
  the code-calibration literature is still working with internal signals + post-hoc
  recalibration + abstention heads, not train-time verbalized-confidence discrimination.
---

When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2605.19369v1 [cs.SE] 19 May 2026
\setcctype
by
When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions
Ravishka Rathnasuriya
0009-0005-6129-2865
The University of Texas at Dallas
USA
ravishka.rathnasuriya@utdallas.edu
and
Wei Yang
0000-0002-5338-7347
The University of Texas at Dallas
USA
wei.yang@utdallas.edu
(2026)
Abstract.
Code language models are increasingly adopted for both understanding and generative tasks. Despite their success, these models frequently produce overconfident incorrect predictions and underconfident correct predictions, undermining their reliability in deployment. Practical deployment demands three capabilities: accurately estimating the likelihood of correctness, abstaining on uncertain predictions, and invoking external mechanisms to validate or repair abstained outputs.
Existing calibration and uncertainty estimation methods, primarily developed for natural language tasks, do not readily transfer to code. Notably, post-hoc calibration techniques often reduce probability misalignment but fail to improve the ranking of predictions by correctness likelihood—a requirement for selective prediction under partial coverage. Furthermore, most approaches treat uncertainty as a passive indicator rather than an actionable signal.
This work introduces a unified framework that integrates uncertainty estimation, model calibration, and tool-based abstention handling for code models. The proposed design enables models to assign reliable correctness probabilities, abstain under uncertainty, and invoke lightweight program analysis procedures to process abstained cases. By combining these components within a single deployment-oriented workflow, this framework supports risk-aware, coverage-controlled use of code models across both classification and generation settings.
†
†
journalyear:
2026
†
†
copyright:
cc
†
†
conference:
2026 IEEE/ACM 48th International Conference on Software Engineering; April 12–18, 2026; Rio de Janeiro, Brazil
†
†
booktitle:
2026 IEEE/ACM 48th International Conference on Software Engineering (ICSE-NIER ’26), April 12–18, 2026, Rio de Janeiro, Brazil
†
†
doi:
10.1145/3786582.3786845
†
†
isbn:
979-8-4007-2425-1/2026/04
1.
Introduction
Code language models are increasingly applied across two primary classes of tasks: classification tasks, including vulnerability detection and defect prediction
(Tian
et al.
,
2023
; Yang
et al.
,
2022
; Zhang
et al.
,
2023
; Lu
et al.
,
2021
; Yefet
et al.
,
2020
; Hu
et al.
,
2023
; Li
et al.
,
2021
; van Tonder and Goues,
2020
; Peng
et al.
,
2018
)
, and generative tasks, such as code completion, synthesis, and repair
(Roziere
et al.
,
2023
; Guo
et al.
,
2024
; Jiang
et al.
,
2024
; Liu
et al.
,
2023
,
2024
)
. These models are now integral to developer workflows via integration into IDEs, CI pipelines, and automated programming assistants. However, despite their success, these models frequently exhibit poor alignment between predictive confidence and actual correctness
(Spiess
et al.
,
2024
; Zhou
et al.
,
2024
)
. In practice, they often assign high confidence to incorrect predictions and low confidence to correct ones which undermine their reliability, especially when used in high-stakes or partially automated environments.
Reliable deployment of code models requires more than producing high-confidence outputs. It requires mechanisms that can estimate, for each prediction, whether it is likely to be correct. This entails three key capabilities. First, models must produce a well-calibrated estimate of per-sample correctness, that is, the predicted confidence should reflect the true likelihood of correctness. Second, systems must support selective abstention, allowing models to withhold predictions when uncertainty is high. Third, there must be principled mechanisms for acting on abstained inputs, for example, by routing them to lightweight analysis tools, heuristic checks, or human review. These capabilities enable a deployment setting where model outputs can be accepted only when trustworthy, and otherwise deferred for further handling.
While uncertainty estimation and calibration have been studied extensively in other domains
(Guo
et al.
,
2017
; Zhou
et al.
,
2024
; Vasilev and D’yakonov,
2023
; Gupta
et al.
,
2020
)
, existing methods face fundamental limitations when applied to code. Confidence signals often fail to capture the structured and semantic nature of code predictions. Similarly, post-hoc calibration techniques
(Guo
et al.
,
2017
; Zhou
et al.
,
2024
; Spiess
et al.
,
2024
)
may reduce average miscalibration but do not improve per-sample reliability in a way that supports effective abstention decisions. Moreover, these methods typically operate in isolation, with no integrated support for resolving the uncertain cases they identify.
Empirical studies from our prior work further underscore this gap
(Spiess
et al.
,
2024
; Zhou
et al.
,
2024
)
. We find that uncertainty signals
(Hendrycks and Gimpel,
2018
; Steinhardt and Liang,
2016
; Shannon,
1948
; Monarch,
2021
; Gal and Ghahramani,
2016
; Lakshminarayanan
et al.
,
2017
; Rathnasuriya
et al.
,
2025
; Rathnasuriya,
2025a
,
b
; Vashurin
et al.
,
2024
)
, across both classification and generation tasks, often correlate poorly with correctness, particularly in code scenarios involving rare patterns, ambiguous syntax, or long-range dependencies. Calibration improves score alignment but fails to improve abstention efficacy: the calibrated probabilities do not reliably distinguish between trustworthy and untrustworthy predictions. These findings motivate the need for a unified formulation that not only estimates uncertainty and calibrates output confidence, but also makes abstention operationally useful.
We propose a deployment-oriented framework for code models that addresses this gap. Our formulation supports both classification and generation tasks, and integrates three essential components: (i) the construction of more informative uncertainty signals tailored to code, (ii) both pre-deployment and post-deployment calibration strategies that improve the interpretability of model confidence, and (iii) the incorporation of model–context–protocol (MCP)
(Sarkar and Sarkar,
2025
)
tools to handle abstained predictions through lightweight rule-based, static, or semantic analyses. This approach supports coverage-controlled decision-making and enables actionable abstention pipelines without requiring model retraining as a prerequisite. Together, these components provide a foundation for robust and risk-aware deployment of code models in real-world software engineering workflows.
2.
Our Envision
We propose a structured framework for deploying code intelligence systems that unifies model uncertainty, selective abstention, and tool-informed recovery into a single decision process (Figure
1
). This design allows models to generate confidence-aware outputs, withhold unreliable predictions, and route uncertain cases through task-specific post-processing. Our goal is to move beyond passive confidence reporting and toward operational systems that act cautiously under uncertainty and adapt their behavior based on calibrated, interpretable signals.
Figure 1
.
Overview of the Proposed Framework
Inputs and model scope.
The framework begins with task-specific inputs, each routed to either a classification model or a generative model
(Li
et al.
,
2023
; Roziere
et al.
,
2023
; Guo
et al.
,
2024
; Hui
et al.
,
2024
)
. Classification tasks include vulnerability detection, defect prediction, or API misuse identification, where the model maps a code representation to a discrete label. Generative tasks include code synthesis, completion, or repair, where the model produces a token sequence given a partial specification or prompt
(Tian
et al.
,
2023
; Yang
et al.
,
2022
; Zhang
et al.
,
2023
; Lu
et al.
,
2021
; Yefet
et al.
,
2020
; Hu
et al.
,
2023
; Li
et al.
,
2021
; van Tonder and Goues,
2020
; Peng
et al.
,
2018
)
. The inputs may consist of code snippets, function signatures, or contextual metadata, and are tokenized and encoded according to model requirements. Each model then produces an output, which is a prediction or a completion, along with internal signals used to compute uncertainty.
Uncertainty estimation.
The framework begins by extracting internal uncertainty signals from the model, serving as indicators of prediction confidence. Unlike evaluation-centric confidence measures, these signals are used to inform downstream decisions, specifically, whether to trust a model output or defer it.
To support this, we adopt uncertainty estimation strategies that reflect model reliability in both classification and generative tasks. These include metrics derived from predictive distributions as well as methods that quantify model variability under controlled perturbations
(Hendrycks and Gimpel,
2018
; Steinhardt and Liang,
2016
; Shannon,
1948
; Monarch,
2021
; Gal and Ghahramani,
2016
; Lakshminarayanan
et al.
,
2017
; Vashurin
et al.
,
2024
; Rathnasuriya
et al.
,
2025
; Rathnasuriya,
2025a
,
b
)
. The motivation is to enable the system to make task-specific deferral decisions without relying on costly external validation. These signals are not used directly to filter outputs but instead provide the basis for computing correctness likelihood via calibration.
Pre-deployment calibration.
Standard code models are not trained to produce abstention behavior or calibrated uncertainty. Their objectives focus on maximizing prediction accuracy without accounting for decision risk. To enable confidence-aware abstention, we introduce pre-deployment calibration mechanisms that adjust model behavior during training.
For classification models, we introduce mechanisms that allow the model to explicitly abstain. One approach adds a dedicated abstention output pathway trained to identify low-confidence examples. This
abstention head
is supervised with selective risk-aware losses, encouraging the model to defer when it cannot produce reliable predictions. Another approach extends the label space to include a
reject class
, allowing the model to route ambiguous inputs away from fixed categories. These strategies convert the model from a closed-world classifier into a system that can explicitly indicate when it should not decide.
For generative models, pre-deployment calibration is implemented via
reward-aware training
. The model is optimized not only to produce syntactically fluent outputs, but to align generation with correctness proxies such as validation pass rates or task-specific behavior. This changes the behavioral geometry of the model where the model learns to be conservative when uncertain and to structure its generations around downstream acceptability. These techniques require retraining and modify the predictive behavior itself, enabling the model to internalize abstention as a learned action.
Post-deployment calibration.
While pre-deployment techniques change model behavior directly, post-deployment calibration enables abstention over existing models without retraining. The objective here is to convert raw uncertainty signals into calibrated correctness scores that can support abstention decisions.
For classification models, we introduce two forms of post deployment calibration. The first is a
weighted calibration
scheme, where standard calibration mappings
(Guo
et al.
,
2017
; Zhou
et al.
,
2024
; Spiess
et al.
,
2024
)
are trained using loss functions that emphasize certain examples—such as high-error or underrepresented classes—more predominantly. This reflects the real-world need to prioritize reliability over uniform calibration error. The second approach is a
variance-aware calibration
method, where confidence scores are derived from repeated perturbations of model predictions, and their dispersion is mapped to correctness probabilities. This captures distributional uncertainty more effectively and allows calibrated scores to reflect stability, not just average alignment.
For generative models, post-deployment calibration can operate at multiple granularities. At the
token level
, uncertainty scores associated with each step of the generation are recalibrated to reflect empirical correctness likelihoods. This is useful in settings like code completion or repair, where partial outputs must be trusted incrementally. At the
sequence level
, the entire output is assigned a correctness score based on features such as output consistency, structure, and coverage, calibrated against reference data. This holistic calibration allows the system to determine whether the generation, taken as a whole, should be served or deferred. These calibrated scores are then compared to abstention thresholds to decide whether to accept or withhold predictions.
Abstention decisions and recovery.
Once a calibrated correctness score is available, the system enforces a policy such that, if the score exceeds a tunable threshold, the prediction is accepted; otherwise, the input is abstained. However, abstention is not terminal. The system activates recovery modules based on the nature of the input and task. For
generative tasks
, we introduce a
MCP
layer that resolves abstained predictions via targeted interventions. This layer addresses three distinct failure modes.
First, when the model fails due to missing task information, such as under-specified prompts, the MCP layer augments the input. It may invoke model reasoning strategies to generate intermediate plans or sketches that clarify intent. If the uncertainty indicates multiple plausible completions, decoding is diversified, and candidates are re-ranked based on follow-up uncertainty estimation. This turns an ambiguous prompt into a controlled exploration.
Second, when failure arises from missing external knowledge, such as unknown libraries or undocumented behaviors, the system injects contextual information, such as documentation snippets or relevant specifications. In addition, lightweight analyzers or compilers may be invoked to validate outputs. These tools convert knowledge uncertainty into evidence the model can act on, reducing epistemic uncertainty and improving downstream calibration.
Third, if the model faces a capability gap where the input falls outside the model’s learned competence, the MCP system enforces simplifications. This may include constraining generation length, enforcing intermediate validation steps, or breaking the task into smaller subtasks. If uncertainty remains high after such interventions, the system abstains definitively, ensuring correctness is never sacrificed for coverage.
For
classification tasks
, abstention triggers domain-specific recovery. Static analyzers, program slicing tools, or rule-based validators are applied to the input. These tools assess properties such as control flow, data dependencies, or security patterns to validate or reject predictions. This external analysis layer ensures that classification decisions are always supported by either model confidence or symbolic evidence. This work reframes abstention as a principled decision-making mechanism rather than a fixed thresholding heuristic in future code intelligence systems.
3.
Contributions
In summary, this research makes the following contributions:
•
Unified framework for abstention across code modeling tasks:
We envision a framework that generalizes across classification and generative tasks, enabling selective abstention and structured recovery under uncertainty.
•
Task- and model-specific uncertainty calibration:
We introduce calibration strategies tailored to both classification and generative models.
•
Pre- and post-deployment abstention mechanisms:
We demonstrate how models can be trained to abstain explicitly with abstention heads, reject classes or retrofitted via calibrated confidence thresholds without retraining.
•
MCP-guided abstention recovery:
We define a MCP policy layer for resolving abstained predictions via tool-guided interventions.
•
Abstention as an actionable decision primitive:
We reconceptualize abstention not as failure, but as a route to recovery. The framework incorporates fallback execution and optional feedback loops that adapt to uncertainty in real time.
•
Open science and reproducibility commitment:
All code, configuration files, and calibration datasets will be released under a permissive license upon acceptance.
4.
Preliminary Results
We investigate whether uncertainty metrics and calibration techniques developed for language and vision tasks can transfer effectively to pretrained code models under both classification and generation settings. Our evaluation is guided by three core questions: (1) Do uncertainty metrics align with correctness in code tasks? (2) Can calibration techniques produce trustworthy abstention decisions? (3) Does abstention improve accuracy under coverage constraints? The findings below support the necessity of behavioral calibration and abstention-aware deployment.
4.1.
Impact of Weighted Scaling for Generative Models
We implement a lightweight calibration method for generative models based on a weighted logistic scaling approach. The technique maps raw model confidence scores to calibrated correctness probabilities using a monotonic transformation, where the loss function upweights incorrect predictions to penalize overconfident errors. Due to space constraints, we report results on two representative models: DeepSeek-Coder-7b and CodeLlama-7b on the MBPP+
(Dong
et al.
,
2025
)
benchmark. However, we have applied the technique across multiple models and tasks with similar trends. For comparison, we evaluate this against platt scaling and isotonic regression. Results are summarized in Table
1
. Our findings show that weighted scaling consistently improves both calibration error (ECE)
(Guo
et al.
,
2017
)
and brier score (Brier)
(Guo
et al.
,
2017
)
across models. Selective prediction at 80% coverage achieves over 70% accuracy, indicating that calibrated abstention decisions help isolate reliable outputs. These results validate our framework’s emphasis on conservative, task-specific calibration mechanisms for generative code modeling.
4.2.
Effectiveness of Logit-Based Calibration in Classification
We propose a behavioral calibration method that operates directly on model logits, bypassing softmax compression and preserving richer information about class separability. Instead of mapping post-softmax scores, our approach trains a correctness estimator directly on raw logit features using a lightweight regressor. This design allows the model to retain decision boundary information and improve per-instance reliability. We apply this method to defect prediction
(Phan and Le Nguyen,
2017
)
using DeepSeek-Coder-7b and Qwen-Coder-7b, with results shown in Table
2
. Due to space constraints, only these two models are reported here, but we have evaluated the method across multiple model-task pairs and observe consistent improvements in calibration and selective prediction. The method yields the lowest brier score and ECE scores among tested strategies, and at 80% coverage, achieves over 90% selective accuracy. These results highlight the benefit of behavioral calibration, thus aligning confidence to correctness at the instance level, rather than relying solely on distributional metrics.
Table 1
.
Calibration Results on MBPP+ (
↓
\downarrow
)
DeepSeek–Coder–7B
CodeLlama–7B
Method
Brier
ECE
Brier
ECE
Base Model
0.273
0.223
0.220
0.108
Platt Scaling
0.224
0.103
0.248
0.062
Isotonic Regression
0.216
0.143
0.215
0.054
Weighted Platt Calibration
0.162
0.072
0.172
0.045
Table 2
.
Calibration Results on defect prediction (
↓
\downarrow
).
DeepSeek–Coder–7B
Qwen–Coder-7B
Method
Brier
ECE
Brier
ECE
Base
0.130
0.029
0.137
0.023
Temperature Scaling
0.131
0.035
0.137
0.023
Platt Scaling
0.134
0.056
0.140
0.050
Isotonic Regression
0.130
0.015
0.137
0.016
Confidence
0.098
0.012
0.089
0.011
4.3.
Evaluation of Uncertainty Metrics Across Tasks
We evaluate 16 uncertainty metrics
(Hendrycks and Gimpel,
2018
; Steinhardt and Liang,
2016
; Shannon,
1948
; Monarch,
2021
; Gal and Ghahramani,
2016
; Lakshminarayanan
et al.
,
2017
; Rathnasuriya
et al.
,
2025
; Rathnasuriya,
2025a
,
b
)
across multiple tasks: defect prediction, vulnerability detection, and code generation. These include entropy-based scores, confidence margins, variance estimators, and sampling-based disagreement measures. Our findings show that while many metrics correlate with prediction correctness, few can be directly used to implement abstention in a reliable way.
Without calibration, uncertainty metrics often overestimate reliability on erroneous predictions. Even after applying standard calibration mappings, improvements in selective prediction vary widely by task and model. In particular, no single uncertainty metric emerges as a task-agnostic solution. This supports one of our key insights: effective abstention in code tasks requires behavioral calibration, i.e., alignment of internal confidence with correctness at the per-instance level.
Unlike settings where probabilistic confidence reflects quality (e.g., classification on natural images), code models often emit confident but incorrect predictions due to superficial pattern matching, semantic ambiguity, and structural repetition. These characteristics limit the utility of uncalibrated uncertainty metrics and motivate our call for abstention-aware calibration pipelines.
5.
Future Plan
Our current efforts have focused on a systematic investigation of existing calibration methods, uncertainty metrics, and their impact on confidence estimation in pretrained code models. Based on these insights, we have begun building a structured foundation for abstention-aware deployment in both classification and generation tasks. Looking forward, our research roadmap includes both short-term objectives and longer-term ambitions to operationalize, scale, and generalize the proposed framework.
Short-Term Plan.
Our short-term goals focus on solidifying the empirical foundation and translating the proposed design into implementable modules: (1)
Publishing empirical findings:
We aim to disseminate our results on the limitations of existing calibration methods and the effectiveness of abstention-aware strategies. These findings will help motivate the community to re-express confidence as a decision-making primitive; (2)
Designing and validating envisioned calibration techniques:
We will systematically implement the techniques described in our envisioned framework including both pre-deployment and post-deployment calibration methods for classification and generative models. This includes reward-aware training, weighted scaling, and logit-based behavioral calibration; and (3)
Integrating MCP tools:
We will implement concrete MCP modules for both model types. For classification, this includes rule-based validators and static analysis backends and for generation, we will integrate constraint-based decoding, prompt augmentation, and lightweight synthesis validators. These milestones are planned for completion within a 12 month timeframe and will result in a reproducible, modular codebase covering the full pipeline.
Long-Term Plan.
Beyond initial implementation, we aim to generalize, scale, and evaluate the framework in real-world deployment contexts. Our long-term vision includes: (1)
Expanding across tasks, models, and domains:
We plan to extend the evaluation across broader model families and additional code intelligence tasks, such as code summarization, clone detection, and test generation. This will help assess task- and model-specific calibration needs;
Black-box model integration and robustness testing:
We aim to validate abstention strategies in scenarios where model internals are not accessible. This will test the applicability of our techniques under limited observability and motivate proxy calibration methods; (3)
Developer-facing deployment integration:
We will integrate our abstention framework into real-world development tools, including IDEs and CI systems. This will allow us to evaluate not only model behavior, but also the usability and trustworthiness of abstention as perceived by developers; (4)
End-to-end system engineering and next-generation MCP tooling:
We plan to build a full abstention-aware inference stack, supporting calibration-aware serving, feedback-driven refinement, and dynamic tool invocation. Over time, we will co-develop next-generation MCP tools that combine program analysis with model introspection to guide abstention and recovery adaptively; and (5)
Open ecosystem and community contribution:
All tools, datasets, and evaluation protocols will be released with support for easy extension, benchmarking, and reproducibility. This will facilitate downstream research on abstention-aware learning, calibration, and human-in-the-loop code AI. These milestones are planned for completion within a 12 to 18 month timeframe. Together, these directions aim to transform abstention from an evaluation artifact into a principled mechanism for safe, adaptive, and trustworthy deployment of code intelligence models.
6.
ACKNOWLEDGMENTS
This work was partially supported by NSF grants NSF CCF2146443 and Amazon Trust AI Research Award.
References
Y. Dong, J. Ding, X. Jiang, G. Li, Z. Li, and Z. Jin (2025)
Codescore: evaluating code generation by learning code execution
.
ACM Transactions on Software Engineering and Methodology
34
(
3
),
pp. 1–22
.
Cited by:
§4.1
.
Y. Gal and Z. Ghahramani (2016)
Dropout as a bayesian approximation: representing model uncertainty in deep learning
.
In
international conference on machine learning
,
pp. 1050–1059
.
Cited by:
§1
,
§2
,
§4.3
.
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger (2017)
On calibration of modern neural networks
.
External Links:
1706.04599
Cited by:
§1
,
§2
,
§4.1
.
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. Li,
et al.
(2024)
DeepSeek-coder: when the large language model meets programming–the rise of code intelligence
.
arXiv preprint arXiv:2401.14196
.
Cited by:
§1
,
§2
.
K. Gupta, A. Rahimi, T. Ajanthan, T. Mensink, C. Sminchisescu, and R. Hartley (2020)
Calibration of neural networks using splines
.
arXiv preprint arXiv:2006.12800
.
Cited by:
§1
.
D. Hendrycks and K. Gimpel (2018)
A baseline for detecting misclassified and out-of-distribution examples in neural networks
.
External Links:
1610.02136
Cited by:
§1
,
§2
,
§4.3
.
Q. Hu, Y. Guo, X. Xie, M. Cordy, M. Papadakis, L. Ma, and Y. Le Traon (2023)
CodeS: towards code model generalization under distribution shift
.
In
International Conference on Software Engineering (ICSE): New Ideas and Emerging Results (NIER)
,
Cited by:
§1
,
§2
.
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu,
et al.
(2024)
Qwen2. 5-coder technical report
.
arXiv preprint arXiv:2409.12186
.
Cited by:
§2
.
X. Jiang, Y. Dong, L. Wang, Z. Fang, Q. Shang, G. Li, Z. Jin, and W. Jiao (2024)
Self-planning code generation with large language models
.
ACM Transactions on Software Engineering and Methodology
33
(
7
),
pp. 1–30
.
Cited by:
§1
.
B. Lakshminarayanan, A. Pritzel, and C. Blundell (2017)
Simple and scalable predictive uncertainty estimation using deep ensembles
.
Advances in neural information processing systems
30
.
Cited by:
§1
,
§2
,
§4.3
.
R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou, M. Marone, C. Akiki, J. Li, J. Chim,
et al.
(2023)
Starcoder: may the source be with you!
.
arXiv preprint arXiv:2305.06161
.
Cited by:
§2
.
Y. Li, S. Chen, and W. Yang (2021)
Estimating predictive uncertainty under program data distribution shift
.
arXiv preprint arXiv:2107.10989
.
Cited by:
§1
,
§2
.
J. Liu, C. S. Xia, Y. Wang, and L. Zhang (2023)
Is your code generated by chatGPT really correct? rigorous evaluation of large language models for code generation
.
In
Thirty-seventh Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.
J. Liu, S. Xie, J. Wang, Y. Wei, Y. Ding, and L. Zhang (2024)
Evaluating language models for efficient code generation
.
In
First Conference on Language Modeling
,
External Links:
Link
Cited by:
§1
.
S. Lu, D. Guo, S. Ren, J. Huang, A. Svyatkovskiy, A. Blanco, C. Clement, D. Drain, D. Jiang, D. Tang,
et al.
(2021)
Codexglue: a machine learning benchmark dataset for code understanding and generation
.
arXiv preprint arXiv:2102.04664
.
Cited by:
§1
,
§2
.
R. M. Monarch (2021)
Human-in-the-loop machine learning: active learning and annotation for human-centered ai
.
Simon and Schuster
.
Cited by:
§1
,
§2
,
§4.3
.
H. Peng, Y. Shoshitaishvili, and M. Payer (2018)
T-fuzz: fuzzing by program transformation
.
In
2018 IEEE Symposium on Security and Privacy (SP)
,
pp. 697–710
.
Cited by:
§1
,
§2
.
A. V. Phan and M. Le Nguyen (2017)
Convolutional neural networks on assembly code for predicting software defects
.
In
2017 21st Asia Pacific Symposium on Intelligent and Evolutionary Systems (IES)
,
Vol.
,
pp. 37–42
.
External Links:
Document
Cited by:
§4.2
.
R. Rathnasuriya, Z. Zhao, and W. Yang (2025)
CodeImprove: program adaptation for deep code models
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)
,
pp. 676–676
.
Cited by:
§1
,
§2
,
§4.3
.
R. Rathnasuriya (2025a)
A framework for on the fly input refinement for deep learning models
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering: Companion Proceedings (ICSE-Companion)
,
pp. 140–144
.
Cited by:
§1
,
§2
,
§4.3
.
R. Rathnasuriya (2025b)
On the fly input refinement for code language models
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering: Companion Proceedings (ICSE-Companion)
,
pp. 230–231
.
Cited by:
§1
,
§2
,
§4.3
.
B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez,
et al.
(2023)
Code llama: open foundation models for code
.
arXiv preprint arXiv:2308.12950
.
Cited by:
§1
,
§2
.
A. Sarkar and S. Sarkar (2025)
Survey of llm agent communication with mcp: a software design pattern centric review
.
arXiv preprint arXiv:2506.05364
.
Cited by:
§1
.
C. E. Shannon (1948)
A mathematical theory of communication
.
The Bell system technical journal
27
(
3
),
pp. 379–423
.
Cited by:
§1
,
§2
,
§4.3
.
C. Spiess, D. Gros, K. S. Pai, M. Pradel, M. R. I. Rabin, A. Alipour, S. Jha, P. Devanbu, and T. Ahmed (2024)
Calibration and correctness of language models for code
.
arXiv preprint arXiv:2402.02047
.
Cited by:
§1
,
§1
,
§1
,
§2
.
J. Steinhardt and P. S. Liang (2016)
Unsupervised risk estimation using only conditional independence structure
.
Advances in Neural Information Processing Systems
29
.
Cited by:
§1
,
§2
,
§4.3
.
Z. Tian, J. Chen, and X. Zhang (2023)
On-the-fly improving performance of deep code models via input denoising
.
arXiv preprint arXiv:2308.09969
.
Cited by:
§1
,
§2
.
R. van Tonder and C. L. Goues (2020)
Tailoring programs for static analysis via program transformation
.
In
Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering
,
pp. 824–834
.
Cited by:
§1
,
§2
.
R. Vashurin, E. Fadeeva, A. Vazhentsev, L. Rvanova, A. Tsvigun, D. Vasilev, R. Xing, A. B. Sadallah, K. Grishchenkov, S. Petrakov,
et al.
(2024)
Benchmarking uncertainty quantification methods for large language models with lm-polygraph
.
arXiv preprint arXiv:2406.15627
.
Cited by:
§1
,
§2
.
R. Vasilev and A. D’yakonov (2023)
Calibration of neural networks
.
arXiv preprint arXiv:2303.10761
.
Cited by:
§1
.
Z. Yang, J. Shi, J. He, and D. Lo (2022)
Natural attack for pre-trained models of code
.
In
Proceedings of the 44th International Conference on Software Engineering
,
ICSE ’22
,
New York, NY, USA
,
pp. 1482–1493
.
External Links:
ISBN 9781450392211
,
Link
,
Document
Cited by:
§1
,
§2
.
N. Yefet, U. Alon, and E. Yahav (2020)
Adversarial examples for models of code
.
Proceedings of the ACM on Programming Languages
4
(
OOPSLA
),
pp. 1–30
.
Cited by:
§1
,
§2
.
W. Zhang, S. Guo, H. Zhang, Y. Sui, Y. Xue, and Y. Xu (2023)
Challenging Machine Learning-based Clone Detectors via Semantic-preserving Code Transformations
.
IEEE Transactions on Software Engineering
49
(
5
),
pp. 3052–3070
.
External Links:
2111.10793
,
ISSN 0098-5589, 1939-3520, 2326-3881
,
Document
Cited by:
§1
,
§2
.
Z. Zhou, C. Sha, and X. Peng (2024)
On calibration of pre-trained code models
.
In
Proceedings of the IEEE/ACM 46th international conference on software engineering
,
pp. 1–13
.
Cited by:
§1
,
§1
,
§1
,
§2
.