---
title: 'Code-MUE: Measuring Code LLMs’ Uncertainty through Execution-based Semantic
  Interaction Graphs'
id: code-mue-measuring-code-llms-uncertainty-through-execution-based-semantic-intera
tags:
- code-llm-confidence-positioning-d82d00
- code-uncertainty
created: '2026-11-09T23:08:47.280155Z'
updated: '2026-11-09T23:27:44.540477Z'
source: https://arxiv.org/html/2607.12273
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:47.279637Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: FULL TEXT (ISSTA 2026). Black-box Von Neumann entropy over execution semantic
  graph of N=100 samples, K=20 probe inputs; 8 LLMs, HumanEval/MBPP200/QuixBugs/CodeNet200;
  Spearman up to -0.98, AUROC>0.85. Problem-level labels, excludes logits/hidden states
  and verbal confidence, no contamination control. Close to L1 on execution grounding,
  not L2.
---

Code-MUE: Measuring Code LLMs’ Uncertainty through Execution-based Semantic Interaction Graphs
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2607.12273v2 [cs.SE] 17 Jul 2026
Code-MUE
: Measuring Code LLMs’ Uncertainty through Execution-based Semantic Interaction Graphs
DOI:
XXXXXXX.XXXXXXX
Conference:
35th ACM SIGSOFT International Symposium on Software Testing and Analysis; October 3–9, 2026; Oakland, CA, USA
ISBN:
978-1-4503-XXXX-X/2018/06
Journal:
PACMSE
Volume:
3
ISSTA
ISSTA185
10
DOI:
10.1145/3832276
CCS:
Software and its engineering Automatic programming
CCS:
Computing methodologies Natural language processing
CCS:
Computing methodologies Machine learning
CCS:
Mathematics of computing Information theory
Xiaoning Ren
Affiliation:
Xi’an Jiaotong University
,
China
email:
hnurxn@mail.ustc.edu.cn
,
Yinxing Xue
Affiliation:
Institute of AI for Industries, Chinese Academy of Sciences
,
China
email:
yxxue@iaii.ac.cn
,
Lei Ma
Affiliation:
The University of Tokyo, Japan, and University of Alberta
,
Canada
email:
ma.lei@acm.org
and
Yuheng Huang
Affiliation:
The University of Tokyo
,
Japan
Note:
Corresponding Author
email:
yuhenghuang42@g.ecc.u-tokyo.ac.jp
2026
Abstract.
As Code Large Language Models (LLMs) become central to modern software engineering, their inherent stochasticity poses significant real-world risks, where even minor errors can lead to severe functional, security, or safety consequences. Reliable automation, therefore, demands the ability to distinguish between confident, well-supported predictions and stochastic guessing. However, existing uncertainty estimation methods face a critical gap: white and grey-box techniques are often inapplicable to closed-source models, while standard “black-box” text metrics fail to capture the unique fragility of code, where syntactic variation does not always imply semantic divergence. To bridge this syntax-semantics gap, we introduce
Code-MUE
, a purely black-box framework that measures uncertainty through execution-based Semantic Interaction Graphs. Different from prior approaches that rely on superficial textual similarity,
Code-MUE
grounds uncertainty in observable runtime behavior, calculating the Von Neumann entropy of the solution space to quantify global semantic diversity. A large-scale empirical study across eight state-of-the-art LLMs demonstrates that
Code-MUE
achieves a strong negative correlation with functional correctness (Spearman’s correlation up to -0.98), significantly outperforming lexical and embedding-based baselines while enabling robust risk detection and selective prediction in practical workflows.
Keywords:
Code LLMs, Uncertainty, Code Generation, Execution Semantics
†
†
cc-license:
by
1.
Introduction
Uncertainty is a fundamental quantity that characterizes the degree of unknownness in stochastic systems
(
He et al., 2025
)
. Code Large Language Models (LLMs), which are increasingly integrated into next-generation Software Engineering (SE) workflows, are inherently stochastic due to their probabilistic generation mechanisms
(
Ouyang et al., 2025
)
. Quantifying their uncertainty is therefore a critical problem for reliable SE with LLMs. In code-related tasks, correctness is often discrete, and even minor errors can lead to severe functional, security, or safety consequences
(
Liu et al., 2024b
)
. As a result, dependable automation requires the ability to distinguish between well-supported predictions and stochastic guessing. Beyond risk assessment, prior work has also shown that uncertainty estimates provide a valuable signal throughout the model lifecycle, including guiding alignment during fine-tuning
(
Zhao et al., 2025
;
Li et al., 2025b
)
, selecting the best model among multiple candidates through routing
(
Chuang et al., 2025
)
, and enabling test-time scaling strategies
(
Zhu et al., 2025
;
Wu et al., 2025
)
in which models adapt their computation and execution paths to improve the ultimate performance.
To operationalize uncertainty measurement in practice, prior work has primarily relied on white-box
(
Li et al., 2025c
;
Liu et al., 2024a
)
or grey-box
(
Huang et al., 2025c
;
Spiess et al., 2025
)
signals derived from the model’s internal states. Standard baselines typically exploit token-level predictive distributions (e.g., logits) to compute metrics such as entropy or perplexity, or analyze internal hidden representations to capture epistemic uncertainty. In some domains, these intrinsic signals often correlate strongly with correctness, enabling systems to flag potentially erroneous outputs. However, applying these traditional measurement techniques to the modern landscape of Code LLMs presents several fundamental challenges:
(1)
The Black-Box Accessibility Barrier
: The most capable models for code (e.g., GPT-5, Gemini 3 Pro) are increasingly deployed as closed-source services. These systems typically restrict access to internal weights, hidden states, and often even output logits. Consequently, white-box methods that rely on token entropy or internal activation analysis are rendered inapplicable in many real-world, API-driven environments.
(2)
The “Token vs. Problem” Granularity Mismatch
: Even when internal signals are accessible, the inference paradigm of LLM auto-regressive generation complicates uncertainty estimation. LLMs generate responses token-by-token, optimizing for local probability at each step. While standard metrics like perplexity or mean log-probability capture uncertainty at this syntactic, token-level distribution, they may fail to represent the problem-level distribution. A model may be highly confident in predicting the next keyword while remaining “uncertain” about the global logic. Consequently, aggregating local token probabilities can often be insufficient to quantify the semantic uncertainty of the entire program.
Attempting to overcome these limitations, a line of research adopts black-box multi-sample consistency measures, which estimate uncertainty by generating multiple outputs for the same input and assessing how much they agree with each other. The core idea is that confident models produce stable outputs, while large variation across samples signals higher uncertainty. This principle is closely related to Monte Carlo (MC) dropout
(
Gal and Ghahramani, 2016
;
Li and Gal, 2017
)
, which approximates uncertainty by sampling the model repeatedly. In natural language processing, this idea is effectively realized through semantic entropy
(
Kuhn et al., 2023
)
, which goes beyond surface string matching and evaluates outputs based on their meaning, allowing different phrasings with the same intent to be treated as consistent. However, this leads to the third challenge:
(3)
The Syntax–Semantics Gap
: Unlike natural language, where meaning changes gradually, code is discrete and fragile: a single token difference can fundamentally change program behavior, even when embeddings appear similar. As a result, semantic entropy metrics developed for natural language often fail to distinguish harmless syntactic variation from critical logic errors in code.
To address these challenges, we propose a method grounded in a lightweight, black-box design philosophy. We observe that code possesses a unique, actionable property:
executability
. Even without access to model internals or ground-truth test cases, we can leverage the execution behavior of generated code to approximate semantic uncertainty. By sampling multiple programs and executing them against generated inputs, we can cluster solutions based on their runtime behavior rather than their textual surface form.
In this paper, we propose
Code-MUE
, a purely black-box, execution-based framework for quantifying uncertainty in Code LLMs. Unlike prior approaches that rely on inaccessible internal signals or superficial textual similarity,
Code-MUE
grounds uncertainty estimation in the observable runtime behavior of generated programs. Specifically, it first exposes a model’s latent uncertainty via Monte Carlo sampling and probes the resulting programs using an oracle-free hybrid test suite. It then organizes the resulting execution traces into a Semantic Interaction Graph, in which nodes represent programs and edges encode functional consensus. Finally, by interpreting this graph as a statistical density matrix,
Code-MUE
computes the Von Neumann entropy of its spectrum. This entropy-based measure captures the global structural diversity of the semantic solution space, enabling
Code-MUE
to distinguish between benign syntactic variation and substantive semantic ambiguity.
This paper makes the following contributions:
•
New Perspective & Metric
: We introduce a novel uncertainty metric tailored for Code LLMs that relies solely on execution feedback, validating our lightweight black-box philosophy by bypassing the need for model internals (logits)
•
Large-Scale Empirical Study
: We conduct a large-scale empirical study evaluating eight SOTA LLMs across four distinct SE tasks: code completion, program synthesis, program repair, and code translation. Our results demonstrate that
Code-MUE
achieves a strong negative correlation with functional correctness (Spearman’s
ρ
\rho
up to -0.98), significantly outperforming traditional lexical and embedding-based uncertainty baselines.
•
Practical Implications for AI Safety and Reliability
: We demonstrate the practical utility of
Code-MUE
as a robust mechanism for risk detection and selective prediction in SE tasks. By effectively discriminating between reliable and unreliable code generations (e.g., achieving AUROC scores exceeding 0.85 on multiple benchmarks), our framework enables systems to “abstain” or request human intervention when confidence is low.
In addition to our quantitative evaluation, we conduct in-depth qualitative case studies to diagnose specific failure modes, such as overconfidence and efficiency gaps, and discuss the theoretical properties of our metric in greater detail.
2.
Related Work
2.1.
LLM Uncertainty Measurement and Calibration
Uncertainty is a fundamental, objective quantity that characterizes the degree of unknownness inherent in a stochastic system. As modern LLMs are inherently stochastic due to both data uncertainty and probabilistic generation, uncertainty becomes an intrinsic property of LLM behavior and a critical signal throughout the LLM lifecycle. Prior work has demonstrated its importance in guiding model pre-training and fine-tuning
(
Wang et al., 2024
;
Li et al., 2025a
)
, supporting risk and error detection during inference
(
Kotelevskii et al., 2025
;
Huang et al., 2025c
)
, enhancing reasoning and deliberation processes
(
Fu et al., 2025
)
, and enabling selective prediction and abstention mechanisms
(
Kuhn et al., 2023
)
.
In well-defined mathematical settings, such as a coin-flipping process, uncertainty admits a unique ground-truth value determined by the underlying probability distribution. In contrast, for complex real-world systems, and in particular for LLM inference, this ground-truth uncertainty is generally inaccessible. As a result, practical methods must rely on uncertainty estimation to approximate this latent quantity
(
Shorinwa et al., 2025
)
. Existing approaches to uncertainty estimation in LLMs generally fall into three categories based on the information source they use:
(1)
Grey-box Methods (Logit-based)
: These utilize output distributions (e.g., token entropy)
(
Kadavath et al., 2022
;
Huang et al., 2025c
)
. While computationally efficient, intrinsic signals may fail to capture semantic correctness, particularly in code, where high token probability does not guarantee functional accuracy
(
Huang et al., 2025c
;
Spiess et al., 2025
)
. Furthermore, logit access is frequently restricted in commercial LLMs.
(2)
White-box Methods (Internal States)
: These approaches derive uncertainty from internal activations, which can enhance quantification accuracy
(
Beigi et al., 2024
;
Xiao et al., 2025
;
Mielke et al., 2022
;
Li et al., 2025c
;
Liu et al., 2024a
)
. However, reliance on internal states makes them computationally expensive and often infeasible for closed-source models (e.g., GPT-4) where such access is blocked.
(3)
Black-box Methods (Output Analysis)
: Essential for proprietary models, these methods infer uncertainty externally. Strategies include verbalized confidence, which is intuitive but prone to overconfidence bias
(
Lin et al., 2022
;
Xiong et al., 2024
;
Tian et al., 2023
;
Groot and Valdenegro - Toro, 2024
)
. Alternatively, sampling-based disagreement
(
Gal and Ghahramani, 2016
;
Zhang et al., 2020
)
based on hidden space embedding representation is widely used in NLP
(
Kuhn et al., 2023
;
Nikitin et al., 2024
;
Lin et al., 2024
)
but struggles with code, where syntactic diversity often does not imply semantic divergence
(
Huang et al., 2025c
;
Sharma and David, 2025
)
. While recent work explores symbolic execution to assess functional equivalence
(
Sharma and David, 2025
)
, such methods are often too computationally heavy or language-specific for general deployment.
Different from these prior approaches, our method estimates semantic uncertainty based on execution consensus across multiple generated programs. This design is motivated by a broader tradition in software engineering, where program executions provide quantitative evidence of program behavior. Classical fault localization leverages passing and failing executions together with coverage spectra to assign suspiciousness scores to program elements
(
Jones et al., 2002
;
Jones and Harrold, 2005
)
. Statistical debugging models predicate observations
(
Liu et al., 2005
)
and execution path profiles
(
Chilimbi et al., 2009
)
collected during program execution to identify behaviors correlated with failures. Subsequent work has further analyzed spectrum-based suspiciousness formulas as measures of failure risk
(
Xie et al., 2013
)
. Beyond fault localization, dynamic anomaly detection infers runtime invariants to identify behavioral deviations
(
Hangal and Lam, 2002
)
, while metamorphic testing exploits relations among outputs from multiple executions when reliable test oracles are unavailable
(
Zhou et al., 2015
)
. In a similar spirit, our approach treats execution agreement among independently generated programs as a signal for estimating semantic uncertainty.
Finally, another line of research focuses on uncertainty calibration
(
Spiess et al., 2025
;
Virk et al., 2025
)
, which attempts to link raw uncertainty scores directly to prediction risk. In this setting, the ultimate goal is to transform an uncertainty score (e.g., entropy or variance) into a calibrated probability that serves as a faithful indicator of the model’s correctness, where such a mapping is often post-hoc (e.g., through machine learning). Representative techniques include Temperature Scaling
(
Guo et al., 2017
)
, Platt Scaling
(
Gros and Devanbu, 2025
)
, or Isotonic Regression
(
Bakman et al., 2025
;
Campos et al., 2025
)
. While uncertainty calibration and measurement are closely tied together, we emphasize that they are still distinct research directions. Calibration aims to regularize an existing signal, but its effectiveness is fundamentally limited by the quality of that signal. Our work focuses on the former challenge: developing a more robust methodology to measure uncertainty itself, specifically by leveraging execution-based multi-inference to capture semantic (rather than just textual) dispersion.
2.2.
Risk Assessment of LLMs
Risk assessment for LLM-driven SE has drawn inspiration from metamorphic testing, employing tools like Drowzee
(
Li et al., 2024
)
and MetaQA
(
Yang et al., 2025
)
to detect behavioral inconsistencies. However, these NLP-centric methods may struggle to address the structural constraints of code. While some approaches utilize LLM-as-a-Judge paradigms (e.g., CodeMirage
(
Agarwal et al., 2024
)
) or define hallucination taxonomies
(
Zhang et al., 2025
)
, recent findings such as CodeJudge
(
Tong and Zhang, 2024
)
demonstrate that LLMs are often unreliable at detecting subtle logical errors in their own output. Alternatively, test oracle synthesis
(
Hayet et al., 2024
;
Hossain et al., 2025
;
Molina et al., 2025
)
offers a validation pathway but relies heavily on high-quality specifications that are frequently unavailable in real-world settings. To address this limitation, Allamanis et al.
(
Allamanis et al., 2024
)
introduce an unsupervised behavioral evaluation approach. The method estimates the correctness of code generated by LLMs by verifying whether semantic equivalence is maintained across code-to-description and description-to-code round-trip transformations. Another line of research examines internal model signals, such as hidden states or attention patterns
(
Kou et al., 2024
;
Song et al., 2024
;
Huang et al., 2025a
;
Huang et al., 2025b
)
, which correlate strongly with defects. Despite their effectiveness, these white-box methods incur high computational overhead and are inapplicable to closed-source models.
3.
Background and Motivating Example
Uncertainty signals derived solely from a model’s internal predictive probabilities, such as perplexity or token-level log-likelihood, have been shown to correlate only weakly with LLM correctness in certain scenarios
(
Huang et al., 2025c
;
Xiong et al., 2024
;
Farquhar et al., 2024
)
. This limitation exposes a fundamental challenge in uncertainty estimation for LLMs: a pronounced gap between token-level uncertainty, which reflects confidence in local syntactic choices, and problem-level uncertainty, which captures confidence in the correctness of the global logical solution. To bridge this gap, a complementary line of work seeks to estimate uncertainty directly at the problem level, often from a Bayesian perspective.
More specifically, the LLM can be viewed as a parametric model
P
⁡
(
Y
|
X
,
θ
)
P(Y|X,\theta)
where the parameters
θ
\theta
are treated as random variables. The central problem in uncertainty measurement is to obtain the conditional probability
η
⁡
(
x
)
=
P
⁡
(
Y
|
X
=
x
)
\eta(x)=P(Y|X=x)
, where
x
x
is the model input (e.g., LLM prompt) and
Y
Y
is the output (e.g., generated answers instead of the next token). This
η
⁡
(
x
)
\eta(x)
is the foundation of DNN risk assessment and has a wide range of applications
(
Kotelevskii et al., 2025
)
. However, its true value is computationally intractable. Instead, it can be estimated through:
(1)
η
⁡
(
x
)
≈
∫
P
⁡
(
Y
|
X
=
x
,
θ
)
⋅
p
⁡
(
θ
|
𝒟
)
​
𝑑
θ
\eta(x)\approx\int P(Y|X=x,\theta)\cdot p(\theta|\mathcal{D})d\theta
where
𝒟
\mathcal{D}
is the training data. In the Bayesian Approximation framework, the intractable posterior distribution
p
⁡
(
θ
|
𝒟
)
p(\theta|\mathcal{D})
is estimated by a variational distribution
q
⁡
(
θ
)
q(\theta)
. From this distribution, multiple parametric model instances are sampled for a fixed input
x
x
(
Gal and Ghahramani, 2016
;
Li and Gal, 2017
)
, allowing the integral to be approximated by averaging the resulting predictive distributions (i.e., Monte Carlo approximation).
In traditional deep neural networks, the predictive distribution is often approximated by the classification confidence obtained from a single forward pass
(
Gal and Ghahramani, 2016
)
. In contrast, the autoregressive generation mechanism of LLMs renders this approximation inadequate, as local token-level uncertainty can correlate poorly with global, answer-level correctness (as discussed earlier). To better capture global uncertainty, recent work has shifted toward estimating uncertainty
in the semantic space
induced by the model’s sampled generation traces
(
Kuhn et al., 2023
;
Huang et al., 2025c
)
. Multiple samples are obtained under stochastic inference. By characterizing their distribution within the semantic space, information-theoretic measures such as entropy can be used to quantify uncertainty in the model’s high-level behavior with respect to the given
x
x
. Intuitively, a widely dispersed set of samples indicates high uncertainty, whereas tightly clustered samples suggest confident, stable behavior. Despite its theoretical appeal, a central open challenge remains: how to construct a semantic space that faithfully captures meaningful divergence among sampled outputs.
Figure 1.
Motivating example showing the limitations of surface-level and embedding-based similarity across different implementations of two programming tasks.
To operationalize this semantic space, existing approaches typically approximate the distance
d
⁡
(
𝐲
,
𝐲
′
)
d(\mathbf{y},\mathbf{y}^{\prime})
using surface-form similarity metrics (e.g., BLEU or CodeBLEU)
(
Huang et al., 2025c
)
, distances in dense embedding spaces
(
Nikitin et al., 2024
;
Qiu and Miikkulainen, 2024
)
, or discrete equivalence relations induced by latent classifiers (e.g., NLI-based Semantic Entropy
(
Kuhn et al., 2023
)
).
Although these methods have proven effective in natural language processing, we argue that defining a robust distance metric over any of these representations faces fundamental limitations in code-related tasks. The crux of the issue is a misalignment between these proxy measures and the true objective of interest: functional divergence in program behavior.
We illustrate this limitation in Fig.
1
via a comparative analysis of two structurally isomorphic yet functionally opposite algorithms, FindMax and FindMin. As shown, the two implementations share an almost identical syntactic structure, including looping constructs, variable initialization patterns, and comparison logic. Consequently, the Lexical Similarity Heatmap indicates near-perfect overlap, and the CodeBERT Embedding Space projects these distinct traces into the same tight cluster, implying a semantic distance
d
⁡
(
𝐲
,
𝐲
′
)
≈
0
d(\mathbf{y},\mathbf{y}^{\prime})\approx 0
. However, despite this apparent convergence in the standard semantic space, the algorithms are diametrically opposed in their functional objectives. A single token variation (flipping
>
>
to
<
<
) creates a massive functional cliff that these metrics fail to register. This demonstrates that while the model’s traces may appear stable and low-uncertainty under traditional NLP metrics, the functional epistemic uncertainty remains dangerously high, as the metric cannot distinguish between the correct solution and its logical inverse.
To bridge the gap between superficial similarity and true functional equivalence, we exploit a fundamental distinction between code and natural language. Our core insight is that
code is not merely text; it is a structured artifact that specifies executable behavior
. As a result, code exhibits an intrinsic property: it admits execution that yields observable outputs that reflect the true meaning of the code. By shifting the measurement of sampling trace divergence from ambiguous embedding spaces to the concrete execution space, we ground Bayesian uncertainty estimation in observable behavior. Accordingly, rather than asking “Do these two traces look similar?”, we ask “Do these two traces behave identically?”, yielding a more precise and semantically aligned signal of functional uncertainty.
4.
Method
4.1.
Overview
The fundamental challenge addressed in this work is how to characterize the distribution of model-generated programs corresponding to a given prompt
x
x
in semantic space. Building on the observation that source code is intrinsically executable, we introduce
Code-MUE
, an uncertainty quantification method built upon the graph structure of code samples in semantic space.
Code-MUE
estimates model uncertainty through functional equivalence rather than surface-form similarity. In contrast to prior approaches targeting natural language, such as lexical overlap or embedding-based distances, the proposed approach anchors uncertainty estimation in the observable runtime behavior of generated programs.
To operationalize this principle, we organize the samples produced by a code generation model for a given query into a structured probabilistic object termed the
Semantic Interaction Graph
(SIG). In this graph, each node corresponds to a candidate program produced by the model, while edges encode semantic agreement derived from dynamic execution traces (e.g., input–output behaviors). Two programs are connected when their executions exhibit equivalent or sufficiently similar functional behavior under a shared execution context. This graph-based abstraction enables reasoning about uncertainty at a global level. Rather than relying on isolated pairwise comparisons, SIG captures the geometric and topological structure of the solution space induced by program semantics. Intuitively, a confident model produces a highly concentrated graph structure that has a single, densely connected semantic component. Such a structure indicates a strong consensus among generated programs. Conversely, an uncertain model can generate a fragmented graph with multiple weakly connected or disconnected components, reflecting competing semantic interpretations of the task.
Figure 2.
Overview of the proposed Graph-based Semantic Uncertainty Quantification framework.
As illustrated in Figure
2
,
Code-MUE
performs semantic uncertainty estimation through a three-stage pipeline:
(1)
Probabilistic Sampling and Test Input Synthesis.
We expose the model’s latent uncertainty by sampling a diverse ensemble of candidate programs via temperature-based stochastic decoding. Concurrently, we construct a hybrid input-only probe set combining rule-based boundary cases with LLM-generated nominal inputs to systematically probe the runtime behavior of the sampled programs.
(2)
Semantic Interaction Graph Construction.
We execute the sampled programs against a hybrid test suite that combines nominal inputs with boundary cases, thereby exercising both typical and corner-case behaviors. Based on the resulting execution outcomes, we construct a pairwise semantic similarity matrix that captures functional consensus between programs.
(3)
Graph-based Uncertainty Quantification.
We interpret the induced semantic interaction graph as a quantum-inspired density matrix whose spectrum reflects the global connectivity structure of the solution space. By computing the corresponding Von Neumann entropy, we obtain a robust scalar measure of semantic uncertainty without requiring expected ground truth.
4.2.
Probabilistic Sampling and Test Input Synthesis
Our framework operates under a strict black-box setting, assuming no access to the model’s internal logits or gradients. The foundation of our uncertainty estimation lies in approximating the model’s
system-level semantic distribution
through stochastic sampling and dynamic probing.
4.2.1.
Response Sampling via Temperature-based Stochastic Decoding
Given a coding prompt
x
x
, the first step is to externalize the model’s uncertainty into a discrete set of observable programs. We query the LLM
ℳ
\mathcal{M}
N
N
times with an identical prompt, producing a response ensemble
𝒫
=
{
p
1
,
p
2
,
…
,
p
N
}
\mathcal{P}=\{p_{1},p_{2},\dots,p_{N}\}
. Crucially, to obtain a valid probabilistic estimate of uncertainty, this generation process should reflect variability in the model’s predictive distribution rather than repeatedly collapsing to its single most likely output.
To this end, we employ stochastic decoding with a fixed sampling temperature (e.g.,
τ
=
1.0
\tau=1.0
(
Kadavath et al., 2022
)
) rather than greedy decoding. Here, temperature refers only to the decoding hyperparameter that controls sampling diversity, not to post-hoc temperature scaling for calibration
(
Spiess et al., 2025
)
. This ensemble
𝒫
\mathcal{P}
thereby serves as an empirical proxy for the model’s true output distribution, enabling the quantification of variance in the subsequent semantic analysis.
4.2.2.
Hybrid Input Synthesis
To quantify the functional divergence within
𝒫
\mathcal{P}
, we require a set of test inputs capable of distinguishing between semantically distinct implementations.
we require only valid
inputs
to observe execution traces, effectively bypassing the “Oracle Problem” inherent in generating ground-truth assertions.
We construct a probe set
ℐ
\mathcal{I}
of size
K
K
using a
Hybrid Synthesis Strategy
. This strategy is designed to maximize the
discriminative power
of our similarity metric by combining deterministic boundary probing with semantic-aware nominal testing.
1. Type-based Boundary Inputs (
ℐ
edge
\mathcal{I}_{\text{edge}}
).
To expose fragility in conditional logic and error handling—where subtle semantic deviations often manifest, we allocate a heuristic portion of the budget (
K
/
2
K/2
) to edge-case testing. We employ static analysis to parse the function signature of the generated code, mapping detected types to a rigorous set of “corner values” designed to trigger boundary behaviors:
•
Numeric (
int
,
float
):
Critical values including Zero (
0
0
, to test logic boundaries), negative unity (
−
1
-1
), extreme bounds (e.g.,
sys.maxsize
), and precision singularities (e.g.,
1e-9
).
•
Sequence (
str
,
list
,
tuple
):
Empty sequences (e.g.,
""
,
[]
) to expose
IndexError
vulnerabilities and singleton collections (targeting fencepost errors).
2. LLM-guided Semantic-Aware Nominal Inputs (
ℐ
nom
\mathcal{I}_{\text{nom}}
).
While edge cases capture fragility, they may fail to verify the core algorithmic logic. We allocate the remaining budget (
K
/
2
K/2
) to nominal inputs that represent “typical” usage scenarios. Leveraging the LLM’s semantic understanding of the task description
T
T
, we prompt the model to synthesize representative inputs (e.g.,
“Generate 5 diverse input arrays for a quicksort implementation”
). Notice that we never ask the LLM to generate expected outputs or assertions, and these inputs are not used to decide whether a program is correct. They are used only to induce comparable execution signatures across the sampled programs.
Final Probe Set.
We use a
1
:
1
1{:}1
split between edge-case and nominal probes by default (i.e.,
|
ℐ
edge
|
=
|
ℐ
nom
|
=
K
/
2
|\mathcal{I}_{\text{edge}}|=|\mathcal{I}_{\text{nom}}|=K/2
). If the number of valid boundary inputs is insufficient (e.g., due to limited type-specific values for a given signature), we compensate by generating additional LLM-based nominal inputs to ensure that the total number of test cases remains
K
K
.
The final execution probe set is the union
ℐ
=
ℐ
edge
∪
ℐ
nom
\mathcal{I}=\mathcal{I}_{\text{edge}}\cup\mathcal{I}_{\text{nom}}
. By broadcasting these inputs to all
N
N
responses in
𝒫
\mathcal{P}
, we obtain the raw I/O streams necessary for the subsequent similarity analysis.
4.3.
Semantic Interaction Graph Construction
With the candidate ensemble
𝒫
\mathcal{P}
and the probe set
ℐ
\mathcal{I}
generated, we proceed to construct the latent semantic space of LLMs’ output. This phase entails two primary operations: executing the ensemble to harvest observable output traces, and determining the functional consensus among programs to construct the Semantic Interaction Graph.
4.3.1.
Dynamic Feature Profiling
To characterize the semantics of each program
p
i
∈
𝒫
p_{i}\in\mathcal{P}
beyond surface-level syntax, we employ a sandboxed execution engine. We execute every generated program
p
i
p_{i}
against the full probe set
ℐ
=
{
x
1
,
…
,
x
K
}
\mathcal{I}=\{x_{1},\dots,x_{K}\}
.
For a specific input
x
k
x_{k}
, the execution outcome
o
i
,
k
o_{i,k}
is mapped to a discrete state in the observable output space
Ω
\Omega
. We categorize these states into three distinct behavioral modes to maximize the resolution of our uncertainty measurement:
•
Return Value (
v
v
):
The code executes successfully and returns a specific value (e.g.,
42
, a
list
). This represents the standard functional behavior.
•
Differentiated Runtime Exception (
E
type
E_{\text{type}}
):
The program halts due to an error. Crucially, we treat the
exception type
as a semantic feature (e.g., distinguishing an
IndexError
from a
RecursionError
). This distinction is vital, as different crash modes often imply distinct underlying logic faults.
•
Timeout (
T
T
):
The execution exceeds a predefined time limit, indicating potential infinite loops or inefficient algorithms.
Formally, for each program
p
i
p_{i}
, we aggregate these outcomes into an
Execution Signature Vector
𝐎
i
=
[
o
i
,
1
,
o
i
,
2
,
…
,
o
i
,
K
]
\mathbf{O}_{i}=[o_{i,1},o_{i,2},\dots,o_{i,K}]
, where
𝐎
i
∈
Ω
K
\mathbf{O}_{i}\in\Omega^{K}
. If
p
i
p_{i}
fails an initial syntax check, it is marked as
Invalid
and treated as a disjoint node in the subsequent graph analysis.
4.3.2.
Behavioral Similarity Calculation
We construct the pairwise similarity matrix
𝐖
∈
ℝ
N
×
N
\mathbf{W}\in\mathbb{R}^{N\times N}
to represent the semantic coupling between samples. The entry
W
i
​
j
W_{ij}
quantifies the agreement between the execution signature vectors
𝐎
i
\mathbf{O}_{i}
and
𝐎
j
\mathbf{O}_{j}
.
Handling Syntax Errors (The Isolation Rule).
We define syntax errors as having “null semantic value” since they cannot perform the task. Therefore, if either
p
i
p_{i}
or
p
j
p_{j}
contains a syntax error, their semantic similarity is zero (unless
i
=
j
i=j
, where self-similarity is preserved as 1 for matrix stability):
(2)
W
i
​
j
=
0
if
​
i
≠
j
∧
(
is_syntax_error
​
(
p
i
)
∨
is_syntax_error
​
(
p
j
)
)
W_{ij}=0\quad\text{if }i\neq j\land(\text{is\_syntax\_error}(p_{i})\lor\text{is\_syntax\_error}(p_{j}))
In the graph view, these samples become isolated nodes, contributing to higher entropy (uncertainty).
Handling Timeouts.
Timeouts are treated separately from ordinary runtime exceptions because a timeout does not expose a comparable output value. For distinct programs, we therefore do not count matching timeouts as semantic agreement: if
i
≠
j
i\neq j
and both executions exceed the sandbox time limit on input
x
k
x_{k}
, the comparison for that input contributes
0
0
to
W
i
​
j
W_{ij}
. Self-similarity is still preserved through
W
i
​
i
=
1
W_{ii}=1
. This conservative rule avoids falsely merging programs that may time out for different reasons, such as infinite loops versus extremely slow but terminating computations.
Measuring Functional Consensus.
For any two syntactically valid programs
p
i
p_{i}
and
p
j
p_{j}
, we calculate their similarity by measuring the proportion of test inputs on which they exhibit
identical
behavior.
Let
𝕀
⁡
(
⋅
)
\mathbb{I}(\cdot)
be the indicator function which equals 1 if the condition is true and 0 otherwise. The similarity is defined as:
(3)
W
i
​
j
=
1
K
​
∑
k
=
1
K
𝕀
⁡
(
o
i
,
k
≡
o
j
,
k
)
W_{ij}=\frac{1}{K}\sum_{k=1}^{K}\mathbb{I}(o_{i,k}\equiv o_{j,k})
Here, the condition
o
i
,
k
≡
o
j
,
k
o_{i,k}\equiv o_{j,k}
holds if:
•
Both return the same numerical/string value.
•
Both trigger the same type of Runtime Error (e.g., both raise
ValueError
).
The resulting metric
W
i
​
j
∈
[
0
,
1
]
W_{ij}\in[0,1]
represents the strength of the semantic link between
p
i
p_{i}
and
p
j
p_{j}
. The matrix
𝐖
\mathbf{W}
thus serves as the weighted adjacency matrix for the Semantic Interaction Graph, where dense clusters indicate strong functional consensus.
4.4.
Graph-based Uncertainty Quantification
Having constructed the similarity matrix
𝐖
\mathbf{W}
from the dynamic execution traces, we now proceed to quantify the system-level uncertainty. This step is crucial to transforming the Monte Carlo samples drawn from the posterior to a single score (as formulated in Section
3
).
While performing moment-based aggregation of
𝐖
\mathbf{W}
, such as computing the average pairwise agreement (
W
¯
\bar{W}
), is straightforward, such measures capture only a first-order characterization of behavioral agreement. For instance, average pairwise agreement can be interpreted as the probability that two randomly sampled generated programs exhibit identical behavior on the probe set. Although informative, this statistic collapses the full pairwise structure into a single expectation. Consequently, it is insensitive to the internal organization of agreement within the ensemble: the same value of
W
¯
\bar{W}
may arise when most programs form a dominant agreement cluster with a few outliers, when programs partition into several balanced behavioral groups, or when weak partial agreement is diffusely distributed across the ensemble.
This limitation is structural. The matrix
𝐖
\mathbf{W}
encodes not only the overall extent of agreement, but also how agreement is organized across samples. To preserve this richer relational structure, we reinterpret
𝐖
\mathbf{W}
as a graph whose nodes correspond to generated programs and whose edge weights quantify behavioral agreement. This graph representation makes it possible to characterize whether the ensemble concentrates around a single dominant consensus region, separates into several competing regions, or fragments into many isolated behaviors. We formalize this induced graph structure as follows.
4.4.1.
Semantic Interaction Graph Construction
We conceptualize the set of
N
N
generated programs as a
Semantic Interaction Graph
, denoted as
𝒢
=
(
𝒱
,
ℰ
,
𝐖
)
\mathcal{G}=(\mathcal{V},\mathcal{E},\mathbf{W})
.
•
Nodes (
𝒱
\mathcal{V}
):
Each node
v
i
v_{i}
corresponds to a generated sample
p
i
p_{i}
.
•
Edges (
𝐖
\mathbf{W}
):
The graph is fully connected and weighted. Crucially, the similarity matrix
𝐖
\mathbf{W}
derived in Section
4.3
serves as the
Adjacency Matrix
of this graph. The weight
W
i
​
j
W_{ij}
represents the
functional coupling strength
between program
p
i
p_{i}
and
p
j
p_{j}
.
4.4.2.
Spectral State and Density Matrix
Once the ensemble is represented as a weighted graph, its global organization is encoded in the spectrum of the corresponding adjacency operator. This is a standard principle in spectral graph analysis: local edge weights define a matrix operator, and the eigenvalues of this operator summarize coarse structural properties such as the number, strength, and separation of connected regions. In our setting, these regions correspond to behavioral modes among generated programs.
We therefore construct the density matrix
𝝆
\boldsymbol{\rho}
by trace-normalizing the behavioral agreement matrix
𝐖
\mathbf{W}
before analyzing its eigenvalue distribution. The raw matrix
𝐖
\mathbf{W}
encodes the behavioral coupling among generated programs, but its scale depends on the number of samples. To compare ensembles through their spectral structure, we normalize
𝐖
\mathbf{W}
so that its total spectral mass is fixed:
(4)
𝝆
=
𝐖
Tr
​
(
𝐖
)
=
𝐖
N
\boldsymbol{\rho}=\frac{\mathbf{W}}{\text{Tr}(\mathbf{W})}=\frac{\mathbf{W}}{N}
where
Tr
​
(
𝐖
)
=
N
\text{Tr}(\mathbf{W})=N
due to the reflexive property (
W
i
​
i
=
1
W_{ii}=1
). Thus,
𝝆
\boldsymbol{\rho}
is the density matrix in our formulation, obtained by trace-normalizing the behavioral agreement matrix
𝐖
\mathbf{W}
. Conceptually, it describes the
mixed semantic state
of the LLM’s generation process. We then perform eigen-decomposition on
𝝆
\boldsymbol{\rho}
to obtain its spectrum
Λ
=
{
λ
1
,
λ
2
,
…
,
λ
N
}
\Lambda=\{\lambda_{1},\lambda_{2},\dots,\lambda_{N}\}
, subject to
λ
k
≥
0
\lambda_{k}\geq 0
and
∑
λ
k
=
1
\sum\lambda_{k}=1
.
Physical Interpretation of Eigenvalues.
The eigenvalues
Λ
\Lambda
provide a profound insight into the model’s internal state. They represent the probability distribution over the
Latent Semantic Modes
(i.e., independent functional clusters) within the ensemble:
•
Pure State (
λ
1
≈
1
\lambda_{1}\approx 1
):
Corresponds to a rank-1 matrix where all samples collapse into a single semantic consensus. The model is “purely” confident in one logic.
•
Mixed State (Dispersed
λ
\lambda
):
Indicates that the probability mass is split among multiple conflicting modes. The model is oscillating between different functional realizations.
4.4.3.
Von Neumann Entropy Calculation
Finally, given the normalized spectral state
𝝆
\boldsymbol{\rho}
, uncertainty corresponds to how concentrated or dispersed its spectral mass is across behavioral modes. We use
Von Neumann entropy
(
Bengtsson and Życzkowski, 2017
)
because it is the standard entropy functional for such matrix-valued states: it measures the mixedness of
𝝆
\boldsymbol{\rho}
rather than only the average amount of pairwise disagreement:
(5)
H
spec
=
−
Tr
(
𝝆
ln
𝝆
)
=
−
∑
k
=
1
N
λ
k
ln
(
λ
k
)
H_{\text{spec}}=-\text{Tr}(\boldsymbol{\rho}\ln\boldsymbol{\rho})=-\sum_{k=1}^{N}\lambda_{k}\ln(\lambda_{k})
(6)
U
⁡
(
𝒫
)
=
H
spec
ln
⁡
(
N
)
U(\mathcal{P})=\frac{H_{\text{spec}}}{\ln(N)}
where the normalization factor
ln
⁡
(
N
)
\ln(N)
corresponds to the maximum entropy state (the identity matrix
𝐈
N
\mathbf{I}_{N}
, representing
N
N
distinct, mutually exclusive semantics).
Unlike token-level Shannon entropy, which measures uncertainty from the model’s predictive probability distribution, Von Neumann entropy quantifies uncertainty over the execution-based semantic interaction graph, providing a soft and topology-aware characterization of the generated solution space. This quantity,
U
⁡
(
𝒫
)
∈
[
0
,
1
]
U(\mathcal{P})\in[0,1]
, serves as a structurally informed measure of semantic uncertainty:
U
⁡
(
𝒫
)
→
0
U(\mathcal{P})\to 0
indicates convergence toward consistent semantic behavior, while
U
⁡
(
𝒫
)
→
1
U(\mathcal{P})\to 1
signifies high semantic divergence among candidate programs.
5.
Evaluation
5.1.
Experimental Setup
Models.
We conduct a large-scale evaluation across eight LLMs, evenly split between closed-source API-based systems and open-source instruction-tuned models. The closed-source set includes gpt-4.1-mini
(
OpenAI, 2025a
)
, gpt-4.1-nano
(
OpenAI, 2025b
)
, claude-3-haiku
(
Anthropic, 2024
)
, and gemini-2.5-flash-lite
(
DeepMind, 2025
)
. These models represent widely deployed, production-grade systems that are optimized for low latency and strong instruction following, and they provide competitive reference points for uncertainty evaluation under real-world API settings. The open-source set includes Llama 3.1-8B-Instruct
(
Meta, 2024
)
, Mistral-7B-Instruct-v0.3
(
AI, 2024b
)
, DeepSeek-Coder-6.7B-Instruct
(
AI, 2024a
)
, and Qwen2.5-7B-Instruct
(
Team, 2025
)
. These models cover multiple major open model families and include both general-purpose instruction-tuned models and code-specialized models (i.e., DeepSeek-Coder).
Datasets.
We evaluate on four established code benchmarks, each mapped to a distinct task type, to probe uncertainty under different generation constraints. HumanEval
(
Chen et al., 2021
)
is used as a function-level code completion task, where the model completes an implementation conditioned on a provided function scaffold and natural-language specification. MBPP (Mostly Basic Python Problems)
(
Austin et al., 2021
)
is treated as program synthesis, emphasizing specification-to-code generation with comparatively weaker scaffolding than HumanEval. QuixBugs
(
Lin et al., 2017
)
is used for program fixing, where the model must repair a buggy implementation to satisfy the intended behavior. Project CodeNet
(
Puri et al., 2021
)
is used for program translation
(
Pan et al., 2024
)
, where the model translates an implementation across programming languages while preserving semantics. Across all tasks, functional correctness is assessed by executing model outputs against the benchmark-provided tests or reference I/O where available.
Due to the substantial computational cost associated with repeated sampling and dynamic execution
1
1
1
To systematically study the effect of Monte Carlo sampling scale, we perform 100 stochastic samples per question, leading to approximately 500,000 inference calls for closed-source APIs under the current setting.
, we evaluate MBPP and CodeNet on randomly sampled subsets of 200 tasks each, while using the full benchmark for HumanEval and QuixBugs. Under this setup, overall functional correctness results are summarized in Table
1
. We use pass@k
(
Chen et al., 2021
)
to measure baseline code generation performance, estimating the probability that at least one of k generated samples passes all functional tests.
Method Setup.
For each problem instance, we sample
N
=
100
N=100
candidate programs and execute them on a shared probe set. For uncertainty estimation, we draw up to
K
=
20
K=20
valid probe inputs per task from a pre-generated input pool using a deterministic task-level seed. These probe inputs are used only to compare the behavior of generated programs; their expected outputs are not used when constructing the semantic similarity matrix. Each generated program is executed in a separate worker process under a restricted Python environment. The harness disables direct termination calls such as
exit
,
quit
, and
sys.exit
, and applies a five-second timeout to each program-input execution. This threshold follows common practice in code evaluation, where execution limits are typically set to a few seconds
(
Chen et al., 2021
;
Qing et al., 2026
)
. Execution outcomes are normalized into return values, runtime exception types, timeout markers, or syntax/compile failures.
Baselines.
To align with real-world deployment scenarios involving closed-source LLMs, our evaluation targets black-box uncertainty measurement. We therefore exclude white-box or grey-box approaches that rely on token-level logits or internal activation states, as such signals are frequently inaccessible in commercial API-based services. Instead, we compare
Code-MUE
against representative multi-sample consistency baselines that derive uncertainty solely from observable outputs: (1)
Lexical Semantic Entropy
: A text-based diversity metric that clusters responses using surface-form similarity (e.g., ROUGE-L overlap) to estimate entropy
(
Huang et al., 2025c
)
. (2)
Embedding Semantic Entropy
: A consistency measure that clusters responses based on their distances in a dense embedding space to capture semantic divergence.
2
2
2
We adapt the original NLI-based formulation by substituting the Natural Language Inference model with a domain-specific code embedding model (CodeBERT) to better capture programming semantics.
(
Kuhn et al., 2023
;
Qiu and Miikkulainen, 2024
)
(3)
Length Variance
(Coefficient of Variation): A heuristic that quantifies uncertainty via the dispersion of response lengths (normalized by the mean). This metric is grounded in the intuition that a confident model should consistently produce solutions of comparable structural complexity. We are further motivated by recent findings
(
Wang et al., 2025
)
that point out the LOC of answers as critical indicators for characterizing model errors. (4)
Logit-based
: The classical intrinsic baseline that estimates uncertainty using token-level predictive probabilities. Concretely, for each generated program we compute the mean negative log-probability of the generated top-1 token at each step, and then average this score across the
N
N
sampled generations to obtain a single scalar per instance
(
Kadavath et al., 2022
)
.
Table 1.
Functional Correctness (Pass@
k
k
) on Code Benchmarks.
We report Pass@1 and Pass@5 (%) for all models across four datasets. All values are evaluated using our standardized experimental setup.
Model
HumanEval
MBPP200
QuixBugs
CodeNet200
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Closed-Source Models
GPT-4.1-mini
94.14
97.62
58.27
64.52
88.08
96.66
70.42
83.11
GPT-4.1-nano
85.58
93.30
54.44
61.03
79.60
89.73
68.47
87.40
Claude-3-Haiku
66.52
80.18
53.19
58.82
65.22
86.03
62.78
78.28
Gemini-2.5-Flash-Lite
89.87
94.08
49.82
57.86
78.35
90.41
67.00
81.76
Open-Source Models
Llama 3.1-8B-Instruct
57.80
77.73
38.38
51.91
52.45
76.12
42.33
70.93
Mistral-7B-Instruct-v0.3
36.67
57.75
31.41
42.45
39.95
71.51
38.49
65.22
DeepSeek-Coder-6.7B-Instruct
66.45
87.57
42.18
58.10
47.42
80.87
57.63
78.25
Qwen2.5-7B-Instruct
75.40
88.35
46.27
57.13
62.68
83.84
48.49
67.92
Research Questions.
While uncertainty metrics have broad applicability across the LLM lifecycle from guiding alignment to model routing, we focus here on
risk assessment
as the most direct and critical application for reliable Software Engineering, leaving other use cases for future work. We structure our evaluation to answer three core questions, progressing from the metric’s fundamental validity to its practical utility and behavioral boundaries. First, we establish the baseline validity by investigating whether the estimated uncertainty serves as a reliable proxy for functional correctness (RQ1). Next, we evaluate its effectiveness in two actionable downstream scenarios:
selective prediction
(filtering out unreliable generations) and
response selection
(identifying the optimal candidate from a set) (RQ2). Finally, we diagnose the limitations of our approach through qualitative case studies of failure modes, such as overconfidence, to understand when the estimation fails (RQ3):
•
RQ1 (Correctness Alignment):
Can
Code-MUE
reliably distinguish between functionally correct and incorrect code generations?
•
RQ2 (Practical Utility):
Can the uncertainty signal be effectively leveraged for risk detection and candidate re-ranking?
•
RQ3 (Case Studies on Uncertainty-Accuracy Misalignments):
What do overconfident and underconfident outliers reveal about the limitations of
Code-MUE
?
5.2.
RQ1: Correctness Alignment
Goal.
We first validate whether
Code-MUE
serves as a faithful proxy for code generation quality—whether lower uncertainty scores reliably correspond to higher functional correctness.
5.2.1.
Experimental Design
We first assess how well each metric aligns with correctness by computing its Spearman correlation with instance-level Pass@1, where Pass@1 is a binary indicator of whether the returned program passes all tests. Since higher uncertainty should correspond to lower Pass@1, we expect negative correlations, with larger absolute values (i.e., closer to
−
1
-1
) indicating stronger alignment. To further evaluate discriminative ability, we assign each instance a binary label:
Solved
if at least one of the
N
N
sampled candidates passes all tests, and
Unsolved
otherwise. We then measure how effectively each uncertainty metric separates these two groups using AUROC.
5.2.2.
Results
Table 2.
Comparison of correlation (Spearman’s
ρ
\rho
) and discrimination (AUROC) capabilities across four datasets and eight LLMs. “Ours” denotes our proposed Spectral Graph Entropy method. The best results (highest AUROC or strongest negative correlation) are highlighted in
bold
, and the second-best results are
underlined
. Claude-3-Haiku, token log-probabilities are unavailable, so Logit entries are shown as “–”.
Dataset
Model
Spearman Correlation (
ρ
\rho
)
↓
\downarrow
AUROC
↑
\uparrow
Ours
Lexical
Embedding
Length
Logit
Ours
Lexical
Embedding
Length
Logit
CodeNet
DeepSeek-Coder-6.7b
−
-
0.879
-0.246
-0.246
-0.150
0.041
0.816
0.480
0.477
0.454
0.412
Llama3.1-8B
−
-
0.703
-0.158
-0.120
0.042
0.066
0.855
0.429
0.406
0.371
0.386
Mistral-7B-v0.3
−
-
0.853
-0.368
-0.225
-0.046
-0.019
0.866
0.485
0.424
0.429
0.457
Qwen2.5-7B
−
-
0.735
-0.112
-0.110
-0.097
0.028
0.657
0.318
0.351
0.431
0.364
Claude-3-Haiku
−
-
0.932
-0.269
-0.334
-0.351
–
0.868
0.458
0.484
0.543
–
Gemini-2.5-Flash
−
-
0.961
-0.076
0.004
-0.026
0.091
0.894
0.279
0.308
0.392
0.331
GPT-4.1-mini
−
-
0.966
-0.215
-0.216
-0.160
-0.007
0.906
0.376
0.385
0.398
0.468
GPT-4.1-nano
−
-
0.917
-0.198
-0.061
0.171
0.074
0.825
0.314
0.381
0.449
0.422
HumanEval
DeepSeek-Coder-6.7b
−
-
0.829
-0.687
-0.475
-0.184
0.012
0.712
0.735
0.520
0.581
0.488
Llama3.1-8B
−
-
0.788
-0.454
-0.298
-0.164
0.063
0.684
0.564
0.494
0.557
0.521
Mistral-7B-v0.3
−
-
0.695
-0.496
-0.340
-0.338
-0.024
0.772
0.682
0.594
0.654
0.572
Qwen2.5-7B
−
-
0.870
-0.453
-0.310
-0.265
0.037
0.638
0.545
0.451
0.418
0.463
Claude-3-Haiku
−
-
0.827
-0.103
0.049
0.112
–
0.726
0.534
0.467
0.458
–
Gemini-2.5-Flash
−
-
0.985
-0.424
-0.419
-0.477
0.094
0.919
0.854
0.809
0.828
0.506
GPT-4.1-mini
−
-
0.987
-0.412
-0.315
-0.350
0.021
0.841
0.414
0.590
0.534
0.447
GPT-4.1-nano
−
-
0.962
-0.436
-0.275
-0.271
-0.016
0.780
0.694
0.687
0.618
0.621
MBPP
DeepSeek-Coder-6.7b
−
-
0.761
-0.368
-0.303
-0.178
0.008
0.787
0.585
0.545
0.533
0.452
Llama3.1-8B
−
-
0.734
-0.408
-0.230
-0.097
-0.031
0.789
0.610
0.573
0.545
0.555
Mistral-7B-v0.3
−
-
0.741
-0.429
-0.337
-0.302
0.055
0.823
0.634
0.592
0.594
0.418
Qwen2.5-7B
−
-
0.831
-0.332
-0.224
-0.152
0.073
0.858
0.565
0.539
0.528
0.536
Claude-3-Haiku
−
-
0.874
-0.357
-0.166
-0.080
–
0.896
0.627
0.540
0.547
–
Gemini-2.5-Flash
−
-
0.850
-0.295
-0.188
-0.287
-0.006
0.875
0.577
0.533
0.584
0.512
GPT-4.1-mini
−
-
0.870
-0.346
-0.276
-0.296
0.038
0.900
0.629
0.584
0.616
0.604
GPT-4.1-nano
−
-
0.840
-0.321
-0.183
-0.192
0.096
0.860
0.598
0.529
0.552
0.471
QuixBugs
DeepSeek-Coder-6.7b
−
-
0.553
-0.233
-0.412
0.151
0.083
0.541
0.500
0.500
0.500
0.451
Llama3.1-8B
−
-
0.708
-0.469
-0.050
0.113
0.104
0.591
0.667
0.378
0.315
0.407
Mistral-7B-v0.3
−
-
0.495
-0.157
-0.161
-0.031
-0.028
0.613
0.609
0.550
0.514
0.563
Qwen2.5-7B
−
-
0.858
-0.565
-0.444
-0.474
0.045
0.797
0.897
0.641
0.718
0.542
Claude-3-Haiku
−
-
0.818
-0.278
-0.191
-0.059
–
0.684
0.409
0.513
0.355
–
Gemini-2.5-Flash
−
-
0.940
-0.502
-0.307
-0.391
0.017
0.821
0.821
0.667
0.667
0.492
GPT-4.1-mini
−
-
0.978
-0.518
-0.406
-0.316
-0.011
0.742
0.744
0.667
0.590
0.587
GPT-4.1-nano
−
-
0.835
-0.342
-0.301
-0.295
0.058
0.677
0.632
0.684
0.658
0.444
Table
2
presents a systematic evaluation of
Code-MUE
against three baseline methods across four datasets and eight LLMs. The results underscore the superior capability of our method in quantifying semantic uncertainty.
Strong Alignment with Correctness.
Code-MUE
exhibits the strongest negative correlation with generation accuracy across nearly all experimental settings. Notably, on the HumanEval dataset, our method achieves a near-perfect monotonic relationship with model performance, reaching Spearman correlations of
ρ
=
−
0.987
\rho=-0.987
(GPT-4.1-mini) and
ρ
=
−
0.985
\rho=-0.985
(Gemini-2.5-Flash-Lite). In contrast, the best-performing baseline (Lexical Entropy) typically yields correlations between
−
0.2
-0.2
and
−
0.5
-0.5
. This significant margin suggests that our graph-based metric serves as a highly calibrated indicator: distinct
from
surface-level variations, low spectral entropy accurately reflects the model’s true confidence in the
functional
correctness of the code.
Superior Discrimination Capability.
In terms of binary error detection (AUROC), our method outperforms baselines in 26 out of 32 scenarios, consistently maintaining scores above
0.85
0.85
on CodeNet and MBPP. The substantial gap between our method and the
Length
or
Embedding
baselines highlights the limitation of static features. By constructing similarity graphs based on execution semantics, our approach successfully groups syntactically diverse but functionally equivalent solutions, thereby preventing false alarms caused by mere stylistic variations.
We also observe that the classical logit-based baseline is generally weaker and less stable than multi-sample agreement baselines on these code tasks, highlighting the token-vs.-problem granularity mismatch.
Robustness and Outlier Analysis.
The effectiveness of our metric remains robust across diverse model architectures (from 7B open-weights models to GPT-4 class proprietary models) and problem types. A minor anomaly is observed in the QuixBugs dataset, where baselines occasionally surpass our method in AUROC (e.g., with Qwen2.5-7B). We attribute this to the dataset’s extremely small sample size (
|
𝒟
|
=
40
|\mathcal{D}|=40
), which introduces high statistical variance in binary classification thresholds. However, even in these cases, our method retains the highest Spearman correlation (e.g.,
−
0.978
-0.978
for GPT-4.1-mini), confirming that the underlying trend of our uncertainty estimation remains the most reliable reflection of model confidence.
5.3.
RQ2: Practical Utility (Rejection & Selection)
Goal.
Beyond establishing a statistical correlation, the ultimate test of an uncertainty metric lies in its actionable value for downstream SE tasks. In real-world deployments, practitioners need more than just a correctness probability; they require a reliable signal to govern decision-making—specifically, to decide
when
to trust a model’s output and
which
output to trust. We therefore evaluate the utility of
Code-MUE
in two critical scenarios: (1)
Selective Prediction (Rejection)
, where the system safeguards reliability by abstaining from answering when confidence is low; and (2)
Response Selection (Re-ranking)
, where the system automatically discriminates the optimal solution from a noisy set of candidates without test oracles such as expected outputs, assertions, or reference implementations.
5.3.1.
Experimental Design
Scenario I: Selective Prediction (Rejection).
A lower AURC indicates a better estimator, meaning the system can significantly reduce error rates by rejecting a small fraction of uncertain predictions.
We quantify the effectiveness of selective prediction using the Area Under the Risk-Coverage Curve (AURC)
(
Zhou et al., 2025
)
, a widely established metric in the literature
(
Galil et al., 2023
)
. Formally, we rank all dataset samples by their estimated uncertainty and compute the risk (error rate)
r
⁡
(
c
)
r(c)
at each coverage level
c
∈
[
0
,
1
]
c\in[0,1]
, where
c
c
represents the proportion of the most confident samples retained. The AURC integrates this risk profile, where a lower value indicates a superior capability to concentrate errors within the rejected (high-uncertainty) subset.
Scenario II: Response Selection (Re-ranking).
To further demonstrate the extensibility of
Code-MUE
to real-world workflows, we apply our framework to the unsupervised response selection task, beyond the risk assessment. Here, the goal is to identify the optimal solution
y
^
\hat{y}
from the sampled ensemble
𝒫
\mathcal{P}
without access to ground-truth test cases. Our approach relies on the
Semantic Consensus Hypothesis
: we posit that while incorrect programs exhibit chaotic failure modes, correct programs are functionally equivalent and coalesce into a dense, highly connected cluster. To operationalize this application, we exploit the unique topological properties of the Semantic Interaction Graph constructed by
Code-MUE
. Unlike standard baselines that produce only scalar scores, our graph formulation allows us to propose a
Centrality-based Selection
strategy:
(7)
y
^
=
y
i
where
i
=
arg
⁡
max
j
​
Centrality
​
(
v
j
)
\hat{y}=y_{i}\quad\text{where}\quad i=\arg\max_{j}\text{Centrality}(v_{j})
We use Eigenvector Centrality to identify the semantic “center” of the sampled distribution. We measure performance using
Selection Accuracy on Solvable Tasks
—defined as the percentage of tasks where the selected
y
^
\hat{y}
is correct, considering only tasks where at least one correct candidate exists.
5.3.2.
Results
Risk-Coverage Performance.
Figure
3
presents the risk-coverage curves for HumanEval. The results demonstrate that
Code-MUE
(solid red line) significantly outperforms all baselines.
•
Steep Descent:
Our curves exhibit the steepest descent at high coverage levels. For instance, by rejecting only the top
10
%
10\%
to
20
%
20\%
most uncertain samples, the risk (error rate) drops precipitously. This indicates that our metric effectively flags the most egregious errors (e.g., hallucinations or timeouts).
•
Lower AURC:
The Lexical and Length-based baselines (blue and grey lines) appear flatter, closer to the diagonal (random rejection), suggesting these surface-level metrics struggle to distinguish hard failures from correct logic. In contrast, our semantic graph approach consistently achieves the lowest AURC, providing a reliable “fail-safe” mechanism for deployment.
Unsupervised Response Selection.
Figure
4
illustrates the selection utility on solvable tasks.
•
High Precision Re-ranking:
Across all eight models, our centrality-based method achieves impressive selection accuracy, often exceeding
80
%
80\%
(e.g., on CodeNet) and even reaching
>
90
%
>90\%
on strong models like GPT-4.1-mini and Gemini-2.5-Flash-Lite.
•
Validation of Consensus Hypothesis:
This high accuracy strongly validates our core hypothesis: correct solutions form a semantic consensus (a dense clique in the graph), leading to high eigenvector centrality. Conversely, incorrect solutions (due to logic bugs or syntax errors) tend to be isolated or form smaller, fragmented clusters.
•
Practical Implication:
This result suggests that generating
N
N
samples and selecting the “semantic center” can substantially improve the chance of selecting a correct answer when at least one correct candidate is present, without requiring expensive or unavailable unit tests during inference.
Figure 3.
Risk-Coverage curves on HumanEval across eight LLMs.
The plots show the trade-off between coverage and selective risk. A lower curve indicates a more effective uncertainty estimator; our method (
solid red line
) consistently achieves the lowest risk profile and AURC scores compared to all baselines.
Figure 4.
Reranking performance of Spectral Graph Entropy.
Bars show selection accuracy across eight LLMs and four datasets. By selecting responses with the highest eigenvector centrality, our method consistently identifies correct solutions (often
>
80
%
>80\%
), validating that correct implementations form a dense semantic consensus while incorrect ones diverge.
5.4.
RQ3: Case Studies on Uncertainty-Accuracy Misalignments
While
Code-MUE
generally exhibits a strong negative correlation with model performance (i.e., higher uncertainty typically implies lower accuracy), we observed a distinct cluster of outliers: samples with
near-zero uncertainty
but
zero Pass@1
accuracy. To determine whether this phenomenon arises from inaccuracies in uncertainty estimation or instead reflects cases where the model is confidently incorrect, we conduct a series of case studies and identify a representative pattern. A very common pattern is
Overconfident Error
. In these cases, the model does not exhibit semantic confusion or chaotic behavior; rather, it consistently converges to an incorrect solution due to systematic biases induced by the prompt. We present one representative example in the main paper and provide additional case studies in the supplementary material
(
, 2026
)
.
5.4.1.
Case I: Conceptual Ambiguity (HumanEval/163)
In this task, the model is asked to generate “even digits” between two integers.
The DeepSeek-Coder-6.7b-Instruct model achieved an extremely low entropy of
0.0485
, indicating high internal consensus. However, the Pass@1 score was
0.0
:
Problem Prompt:
Given two positive integers a and b, return the even digits between a and b... generate_integers(2, 8) => [2, 4, 6, 8]
Model Generation (Consensus):
def generate_integers(a, b):
    even_integers = []
    for i in range(min(a, b), max(a, b) + 1):
        if i % 2 == 0:  # <--- The Error
            even_integers.append(i)
    return even_integers
Figure 5.
DeepSeek-Coder consistently misinterprets "even digits" as “even integers”.
Analysis:
As shown in Figure
5
, the model consistently generated logic to find
even integers
(e.g., returning 10, 12) rather than
even digits
(which are strictly 0, 2, 4, 6, 8).
While the example provided in the prompt (
2
,
…
,
8
2,\dots,8
) satisfies both definitions, the logic fails for multi-digit inputs (e.g., 12 is an even integer, but not a digit). The model failed to distinguish the subtle semantic difference, likely because "finding even integers in a range" is a significantly more frequent pattern in the pre-training corpus than “finding even digits.” This
frequency bias
leads to a Confident but Wrong state, which our metric accurately characterizes as low entropy (high consensus) on the incorrect behavior.
5.4.2.
Case II: The Efficiency Gap (HumanEval/83)
Next, we identify a contrasting scenario where the model exhibits
High Uncertainty
despite converging to a logically correct (but computationally inefficient) solution. We examine
HumanEval/83
, which requires counting
n
n
-digit numbers that start or end with ‘1’.
Problem Prompt:
Given a positive integer n, return the count of the numbers of n-digit positive integers that start or end with 1.
Model Generation (Brute Force):
def starts_one_ends(n):
    count = 0
    # O(10^n) Complexity: Iterates through all numbers
    for i in range(10**(n-1), 10**n):
        if str(i).startswith(’1’) or str(i).endswith(’1’):
            count += 1
    return count
Figure 6.
The model generates a correct but exponentially slow solution, leading to universal timeouts.
Analysis:
As shown in Figure
6
, the model defaulted to a brute-force simulation (
O
⁡
(
10
n
)
O(10^{n})
complexity) instead of the expected combinatorial solution (
O
⁡
(
1
)
O(1)
).
When
n
n
is large (e.g.,
n
=
10
n=10
), the execution exceeds the sandbox time limit.
Method Implication:
In
Code-MUE
, we adopt a conservative stance:
execution outputs are the only ground truth for semantics
.
When two programs both timeout, their outputs are undefined. Unlike syntax errors (which can be statically grouped), timeouts may stem from diverse causes (e.g., infinite loops vs. massive calculations).
Consequently, to avoid falsely assuming consensus, we conservatively define the semantic similarity between distinct timed-out instances as
zero
.
This design choice results in
High Entropy
for this case, even though the generated codes are textually similar. We argue this provides a critical “Fail-Safe” property: a code that cannot be executed within reasonable limits is functionally equivalent to an uncertain or unreliable solution.
5.4.3.
Summarization
These case studies highlight a critical property of our Uncertainty Estimation framework:
•
High Uncertainty
implies the model is oscillating between multiple potential solutions (a sign of ignorance).
•
Low Uncertainty with Low Accuracy
implies the model has collapsed into a systematic error (a sign of bias or hallucination).
Consequently, our metric serves a dual purpose even under these two apparent “failure” scenarios: it enables the automatic rejection of
soft failures
(i.e., high uncertainty) and facilitates the identification of
hard failures
(i.e., low uncertainty, systematic errors) that require external intervention, such as prompt refinement or model fine-tuning.
6.
Discussion
Table 3.
Sample Size Sensitivity Analysis.
Spearman Correlation (
ρ
\rho
)
AUROC
N
=
5
N=5
N
=
25
N=25
N
=
50
N=50
N
=
75
N=75
N
=
100
N=100
N
=
5
N=5
N
=
25
N=25
N
=
50
N=50
N
=
75
N=75
N
=
100
N=100
-0.525
-0.804
-0.822
-0.829
-0.831
0.635
0.765
0.776
0.782
0.782
Table 4.
Test Inputs Sensitivity Analysis.
Spearman Correlation (
ρ
\rho
)
AUROC
K
=
4
K=4
K
=
8
K=8
K
=
12
K=12
K
=
16
K=16
K
=
20
K=20
K
=
4
K=4
K
=
8
K=8
K
=
12
K=12
K
=
16
K=16
K
=
20
K=20
-0.682
-0.731
-0.784
-0.812
-0.831
0.681
0.734
0.736
0.771
0.782
6.1.
Sensitivity to the Sample Size and the Number of Test Inputs
Sensitivity to the Sample Size.
CODE-MUE relies on sampling multiple candidate programs to approximate the model’s semantic hypothesis space, which is essential for building a consensus-aware semantic graph. Increasing the sampling budget
N
N
can capture a wider range of functional behaviors and thus improve uncertainty quality, but it also increases computational cost (primarily LLM inference).
Table
3
reports the sensitivity to
N
∈
{
5
,
25
,
50
,
75
,
100
}
N\in\{5,25,50,75,100\}
. As expected, performance improves with larger
N
N
for both correctness alignment (more negative Spearman’s
ρ
\rho
) and discrimination (higher AUROC). Notably, the improvements exhibit diminishing returns beyond moderate budgets: reducing
N
N
from 100 to 25 only slightly changes
ρ
\rho
(from
−
0.831
-0.831
to
−
0.804
-0.804
) and AUROC (from
0.782
0.782
to
0.765
0.765
), retaining most of the full-budget effectiveness. Even under strict constraints (
N
=
5
N=5
), CODE-MUE still provides a meaningful signal, indicating robustness to reduced sampling in practical deployments.
Sensitivity to the Number of Test Inputs.
Our semantic similarity computation executes each sampled program on a probe set
ℐ
\mathcal{I}
of size
K
K
(default
K
=
20
K=20
). A larger
K
K
increases the chance of exposing behavioral divergences, but increases execution cost approximately linearly. To quantify this trade-off, we fix
N
=
100
N=100
and vary
K
∈
{
4
,
8
,
12
,
16
,
20
}
K\in\{4,8,12,16,20\}
, with results in Table
4
.
Overall, increasing
K
K
yields more reliable uncertainty signals: both correctness alignment (more negative Spearman’s
ρ
\rho
) and discrimination (higher AUROC) improve as
K
K
grows. Importantly, even a small probe budget already provides useful signal (e.g.,
K
=
4
K=4
still achieves
ρ
=
−
0.682
\rho=-0.682
), while the marginal gains diminish at higher budgets. This suggests that moderate probe sizes can preserve strong performance while reducing execution overhead.
6.2.
Computational Overhead and Deployment Practicality
Discussing overhead is critical for practical adoption. The total overhead scales with the number of sampled candidates (
n
n
, i.e.,
N
N
) and the number of synthesized inputs (
m
m
, i.e.,
K
K
), and can be decoupled into four phases:
•
Candidate Generation (
O
⁡
(
n
)
O(n)
LLM Inference):
Generating multiple candidates is a standard prerequisite for modern LLM decoding and evaluation (e.g., pass@k, self-consistency). We view this as a shared baseline cost rather than a bottleneck unique to CODE-MUE.
•
Test Input Synthesis (
O
⁡
(
m
)
O(m)
LLM Inference):
We only prompt the LLM to generate
raw input values
(no expected outputs/assertions). This uses few tokens and can be further amortized by asking the model to synthesize multiple diverse inputs in a single call.
•
Dynamic Execution (
O
⁡
(
n
×
m
)
O(n\times m)
CPU Compute):
Executing
n
n
programs on
m
m
inputs is the primary overhead. However, execution in a local sandbox relies on cheap, highly parallelizable CPU computation, which is typically far more cost-efficient than GPU-bound LLM inference.
•
Uncertainty Quantification (Negligible Compute):
Computing the Von Neumann entropy uses lightweight matrix operations on a small distance matrix and typically takes milliseconds.
In practice, the total cost is dominated by the first three phases. We therefore report a quantitative breakdown in Tables
6
and
6
: we first fix
K
=
20
K=20
and vary
N
N
, and then fix
N
=
100
N=100
and vary
K
K
. The results confirm a clear trade-off: larger
N
N
and
K
K
generally improve uncertainty quality, but also increase cost. Importantly, the end-to-end runtime grows much more with
N
N
than with
K
K
, as candidate generation (LLM inference) is the dominant contributor, whereas increasing
K
K
mainly affects input synthesis and execution with a relatively modest impact on the total time. This further supports the key practical point that, while the primary overhead scales with
O
⁡
(
n
×
m
)
O(n\times m)
, the most scalable component (dynamic execution) is cheap and highly parallelizable CPU computation rather than expensive LLM inference. Overall, together with Tables
3
and
4
, we observe that reducing
N
N
and
K
K
can substantially lower cost while preserving strong performance, providing a wide range of viable operating points for deployment; moreover, candidate generation can be accelerated via batching/parallel queries and stronger inference hardware.
Table 5.
Overhead breakdown vs.
N
N
(fixed
K
=
20
K=20
).
N
N
Cand. Gen.
Input Syn.
Dyn. Exec.
Total
5
3.70
3.83
0.02
7.55
25
18.02
3.83
0.02
21.87
50
26.18
3.83
0.04
30.05
75
37.02
3.83
0.06
40.91
100
51.52
3.83
0.08
55.43
Table 6.
Overhead breakdown vs.
K
K
(fixed
N
=
100
N=100
).
K
K
Cand. Gen.
Input Syn.
Dyn. Exec.
Total
4
51.52
1.81
0.01
53.34
8
51.52
2.44
0.02
53.98
12
51.52
2.71
0.03
54.26
16
51.52
3.39
0.05
54.96
20
51.52
3.83
0.08
55.43
6.3.
Scalability to Larger Code Scenarios
While the dynamic execution overhead of CODE-MUE scales with program length, it is designed to align with modern, modular software engineering workflows, where LLMs are typically used at the function, class, or snippet level rather than generating monolithic systems end-to-end. In large codebases, LLM-generated code is naturally modular—comprising functions, classes, or patches—and is often validated in isolation via unit tests. CODE-MUE can therefore be applied at the same granularity by evaluating these isolated modules, making it compatible with repository-scale development.
Moreover, both candidate generation and probe execution are embarrassingly parallel, which substantially mitigates the wall-clock overhead in practical deployments.
As a concrete repository-level case study, we consider a RepoClassBench
(
Deshpande et al., 2024
)
task (
psf__requests-6028_SESsiON
). After sampling 20 candidates with GPT-4.1-nano, we decompose each generated class into method-level modules via AST parsing, and apply CODE-MUE to one representative module (
gET_aDAPteR
). The procedure yields a low uncertainty score (
H
=
0.09
H=0.09
). Manual inspection further confirms that 18 out of 20 sampled implementations exhibit the correct behavior, which aligns with the intuition that modules with a high fraction of correct implementations tend to receive low uncertainty.
7.
Threats to Validity
Internal Validity.
Model configuration and hyperparameter choices can distort output distributions; we mitigate this by enforcing a consistent configuration (e.g.,
T
=
1.0
T=1.0
) across all models. Additionally, while
Code-MUE
avoids oracle-label bias by using inputs strictly to compare execution behavior rather than generate labels, LLM-generated inputs risk coverage bias. If inputs miss critical semantic regions, distinct behavioral modes may merge, underestimating uncertainty. We mitigate this by implementing a hybrid strategy that combines rule-based boundary inputs with LLM-generated nominal inputs; future work can consider integrating stronger fuzzing, symbolic, or domain-specific input generators.
External threats.
The selection of subject LLMs presents a potential threat to the generalizability of our findings. To address this, we evaluated a diverse set of eight LLMs, evenly split between closed-source API-based systems (e.g., GPT-4.1, Gemini 2.5) and open-source models (e.g., Llama 3.1, DeepSeek-Coder). Another concern is whether our findings hold across different types of coding tasks. We mitigated this by conducting evaluations on four distinct benchmarks (HumanEval, MBPP, QuixBugs, and CodeNet), covering a broad spectrum of tasks including code completion, synthesis, program repair, and translation.
8.
Conclusion
In this paper, we proposed
Code-MUE
, a black-box uncertainty quantification framework that grounds LLM confidence in execution-based semantic consensus rather than superficial textual similarity.
Extensive evaluations demonstrate that
Code-MUE
serves as a highly reliable proxy for functional correctness, achieving strong negative correlations (Spearman’s
ρ
\rho
up to
−
0.98
-0.98
). Beyond accurate measurement, we validated the framework’s practical utility in two distinct deployment scenarios: (1)
Selective Prediction
, where rejecting high-uncertainty samples significantly reduces system error rates; and (2)
Unsupervised Response Selection
, where our centrality-based re-ranking mechanism identifies correct solutions with high precision without requiring ground-truth test oracles.
Data Availability
To facilitate reproducibility and support Open Science, we provide the code at
https://github.com/hnurxn/Code-Uncertainty
.
Acknowledgment
This work was supported in part by JST CRONOS Grant (No. JPMJCS24K8), JSPS KAKENHI Grant (No.JP24K02920, No.JP26KJ0789), and the project “Theoretical Research on Trustworthy Evaluation of Intelligent Software” (Grant No. E6430219G8).
References
Agarwal
et al.
(2024)
V. Agarwal, Y. Pei, S. Alamir, and X. Liu
Codemirage: hallucinations in code generated by large language models
.
arXiv preprint arXiv:2408.08333
.
Cited by:
§2.2
.
AI (2024a)
D. AI
Deepseek-ai/deepseek-coder-6.7b-instruct (model card)
.
Note:
https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct
Accessed: 2026-01-26
Cited by:
§5.1
.
AI (2024b)
M. AI
Mistralai/mistral-7b-instruct-v0.3 (model card)
.
Note:
https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3
Accessed: 2026-01-26
Cited by:
§5.1
.
Allamanis
et al.
(2024)
M. Allamanis, S. Panthaplackel, and P. Yin
Unsupervised evaluation of code llms with round-trip correctness
.
ICML’24
.
Cited by:
§2.2
.
Anthropic (2024)
Claude 3 Haiku large language model
Anthropic
.
External Links:
Link
Cited by:
§5.1
.
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le,
et al.
Program synthesis with large language models
.
arXiv preprint arXiv:2108.07732
.
Cited by:
§5.1
.
Bakman
et al.
(2025)
Y. F. Bakman, D. N. Yaldiz, S. Kang, T. Zhang, B. Buyukates, S. Avestimehr, and S. P. Karimireddy
Reconsidering LLM uncertainty estimation methods in the wild
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 29531–29556
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-251-0
Cited by:
§2.1
.
Beigi
et al.
(2024)
M. Beigi, Y. Shen, R. Yang, Z. Lin, Q. Wang, A. Mohan, J. He, M. Jin, C. Lu, and L. Huang
InternalInspector
I
2
I^{2}
: robust confidence estimation in LLMs through internal states
.
In
Findings of the Association for Computational Linguistics: EMNLP 2024
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 12847–12865
.
External Links:
Link
,
Document
Cited by:
§2.1
.
Bengtsson and Życzkowski (2017)
I. Bengtsson and K. Życzkowski
Geometry of quantum states: an introduction to quantum entanglement
.
Cambridge university press
.
Cited by:
§4.4.3
.
Campos
et al.
(2025)
V. Campos, R. Kuschnereit, and A. Ulges
Multicalibration for llm-based code generation
.
arXiv preprint arXiv:2512.08810
.
Cited by:
§2.1
.
Chen
et al.
(2021)
M. Chen J. Tworek
et al.
Evaluating large language models trained on code
.
External Links:
2107.03374
Cited by:
§5.1
,
§5.1
.
Chilimbi
et al.
(2009)
T. M. Chilimbi, B. Liblit, K. Mehra, A. V. Nori, and K. Vaswani
Holmes: effective statistical debugging via efficient path profiling
.
In
2009 IEEE 31st International Conference on Software Engineering
,
pp. 34–44
.
Cited by:
§2.1
.
Chuang
et al.
(2025)
Y. Chuang, P. K. Sarma, P. Gopalan, J. Boccio, S. Bolouki, X. Hu, and H. Zhou
Learning to route LLMs with confidence tokens
.
In
Forty-second International Conference on Machine Learning
,
External Links:
Link
Cited by:
§1
.
DeepMind (2025)
Gemini 2.5 Flash-Lite large language model
Google DeepMind
.
External Links:
Link
Cited by:
§5.1
.
Deshpande
et al.
(2024)
A. Deshpande, A. Agarwal, S. Shet, A. Iyer, A. Kanade, R. Bairi, and S. Parthasarathy
Natural language to class-level code generation by iterative tool-augmented reasoning over repository
.
In
ICML 2024 Workshop on Data-Centric Machine Learning Research
,
External Links:
Link
Cited by:
§6.3
.
Farquhar
et al.
(2024)
S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal
Detecting hallucinations in large language models using semantic entropy
.
Nature
630
(
8017
),
pp. 625–630
.
Cited by:
§3
.
Fu
et al.
(2025)
Y. Fu, X. Wang, Y. Tian, and J. Zhao
Deep think with confidence
.
arXiv preprint arXiv:2508.15260
.
Cited by:
§2.1
.
Gal and Ghahramani (2016)
Y. Gal and Z. Ghahramani
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
§2.1
,
§3
.
Galil
et al.
(2023)
I. Galil, M. Dabbah, and R. El-Yaniv
What can we learn from the selective prediction and uncertainty estimation performance of 523 imagenet classifiers?
.
In
The Eleventh International Conference on Learning Representations
,
External Links:
Link
Cited by:
§5.3.1
.
Groot and Valdenegro - Toro (2024)
T. Groot and M. Valdenegro - Toro
Overconfidence is key: verbalized uncertainty evaluation in large language and vision-language models
.
In
Proceedings of the 4th Workshop on Trustworthy Natural Language Processing (TrustNLP 2024)
,
A. Ovalle, K. Chang, Y. T. Cao, N. Mehrabi, J. Zhao, A. Galstyan, J. Dhamala, A. Kumar, and R. Gupta (Eds.)
,
Mexico City, Mexico
,
pp. 145–171
.
External Links:
Link
,
Document
Cited by:
§2.1
.
Gros and Devanbu (2025)
D. Gros and P. Devanbu
Localized calibrated uncertainty in code language models
.
arXiv preprint arXiv:2512.24560
.
Cited by:
§2.1
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
Proceedings of the 34th International Conference on Machine Learning
,
D. Precup and Y. W. Teh (Eds.)
,
Proceedings of Machine Learning Research
, Vol.
70
,
pp. 1321–1330
.
Cited by:
§2.1
.
Hangal and Lam (2002)
S. Hangal and M. S. Lam
Tracking down software bugs using automatic anomaly detection
.
In
Proceedings of the 24th international conference on Software engineering
,
pp. 291–301
.
Cited by:
§2.1
.
Hayet
et al.
(2024)
I. Hayet, A. Scott, and M. d’Amorim
Chatassert: llm-based test oracle generation with external tools assistance
.
IEEE Transactions on Software Engineering
51
(
1
),
pp. 305–319
.
Cited by:
§2.2
.
He
et al.
(2025)
W. He, Z. Jiang, T. Xiao, Z. Xu, and Y. Li
A survey on uncertainty quantification methods for deep learning
.
ACM Computing Surveys
.
Cited by:
§1
.
Hossain
et al.
(2025)
S. B. Hossain, R. Taylor, and M. Dwyer
Doc2OracLL: investigating the impact of documentation on llm-based test oracle generation
.
Proceedings of the ACM on Software Engineering
2
(
FSE
),
pp. 1870–1891
.
Cited by:
§2.2
.
Huang
et al.
(2025a)
Y. Huang, L. Ma, K. Nishikino, and T. Akazaki
Risk assessment framework for code llms via leveraging internal states
.
In
Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering
,
pp. 432–443
.
Cited by:
§2.2
.
Huang
et al.
(2025b)
Y. Huang, J. Song, Q. Hu, F. Juefei-Xu, and L. Ma
AcTracer: active testing of large language model via multi-stage sampling
.
ACM Transactions on Software Engineering and Methodology
.
Cited by:
§2.2
.
Huang
et al.
(2025c)
Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma
Look before you leap: an exploratory study of uncertainty analysis for large language models
.
IEEE Transactions on Software Engineering
.
Cited by:
§1
,
§2.1
,
§2.1
,
§2.1
,
§3
,
§3
,
§3
,
§5.1
.
Jones
et al.
(2002)
J. A. Jones, M. J. Harrold, and J. Stasko
Visualization of test information to assist fault localization
.
In
Proceedings of the 24th international conference on Software engineering
,
pp. 467–477
.
Cited by:
§2.1
.
Jones and Harrold (2005)
J. A. Jones and M. J. Harrold
Empirical evaluation of the tarantula automatic fault-localization technique
.
In
Proceedings of the 20th IEEE/ACM international Conference on Automated software engineering
,
pp. 273–282
.
Cited by:
§2.1
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson,
et al.
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Cited by:
§2.1
,
§4.2.1
,
§5.1
.
Kotelevskii
et al.
(2025)
N. Kotelevskii, V. Kondratyev, M. Takáč, E. Moulines, and M. Panov
From risk to uncertainty: generating predictive uncertainty measures via bayesian estimation
.
In
The Thirteenth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§2.1
,
§3
.
Kou
et al.
(2024)
B. Kou, S. Chen, Z. Wang, L. Ma, and T. Zhang
Do large language models pay similar attention like human programmers when generating code?
.
Proceedings of the ACM on Software Engineering
1
(
FSE
),
pp. 2261–2284
.
Cited by:
§2.2
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
The Eleventh International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
,
§2.1
,
§2.1
,
§3
,
§3
,
§5.1
.
Li
et al.
(2025a)
J. Li, Y. Tang, and Y. Yang
Know the unknown: an uncertainty-sensitive method for LLM instruction tuning
.
In
Findings of the Association for Computational Linguistics: ACL 2025
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 2972–2989
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-256-5
Cited by:
§2.1
.
Li
et al.
(2025b)
L. Li, H. Liu, Y. Zhou, Z. Gui, X. Weng, Y. Yuan, Z. Wei, and Z. Li
Uncertainty-aware iterative preference optimization for enhanced llm reasoning
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 23996–24012
.
Cited by:
§1
.
Li
et al.
(2024)
N. Li, Y. Li, Y. Liu, L. Shi, K. Wang, and H. Wang
Drowzee: metamorphic testing for fact-conflicting hallucination detection in large language models
.
Proceedings of the ACM on Programming Languages
8
(
OOPSLA2
),
pp. 1843–1872
.
Cited by:
§2.2
.
Li
et al.
(2025c)
R. Li, J. Long, M. Qi, H. Xia, L. Sha, P. Wang, and Z. Sui
Towards harmonized uncertainty estimation for large language models
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 22938–22953
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-251-0
Cited by:
§1
,
§2.1
.
Li and Gal (2017)
Y. Li and Y. Gal
Dropout inference in bayesian neural networks with alpha-divergences
.
In
International conference on machine learning
,
pp. 2052–2061
.
Cited by:
§1
,
§3
.
Lin
et al.
(2017)
D. Lin, J. Koppel, A. Chen, and A. Solar-Lezama
QuixBugs: a multi-lingual program repair benchmark set based on the quixey challenge
.
SPLASH Companion 2017
,
New York, NY, USA
,
pp. 55–56
.
External Links:
ISBN 9781450355148
,
Link
,
Document
Cited by:
§5.1
.
Lin
et al.
(2022)
S. Lin, J. Hilton, and O. Evans
Teaching models to express their uncertainty in words
.
Transactions on Machine Learning Research
.
Note:
External Links:
ISSN 2835-8856
,
Link
Cited by:
§2.1
.
Lin
et al.
(2024)
Z. Lin, S. Trivedi, and J. Sun
Generating with confidence: uncertainty quantification for black-box large language models
.
Transactions on Machine Learning Research
.
Note:
External Links:
ISSN 2835-8856
,
Link
Cited by:
§2.1
.
Liu
et al.
(2005)
C. Liu, X. Yan, L. Fei, J. Han, and S. P. Midkiff
SOBER: statistical model-based bug localization
.
ACM SIGSOFT Software Engineering Notes
30
(
5
),
pp. 286–295
.
Cited by:
§2.1
.
Liu
et al.
(2024a)
L. Liu, Y. Pan, X. Li, and G. Chen
Uncertainty estimation and quantification for llms: a simple supervised approach
.
arXiv preprint arXiv:2404.15993
.
Cited by:
§1
,
§2.1
.
Liu
et al.
(2024b)
Z. Liu, Y. Tang, X. Luo, Y. Zhou, and L. F. Zhang
No need to lift a finger anymore? assessing the quality of code generation by chatgpt
.
IEEE Transactions on Software Engineering
50
(
6
),
pp. 1548–1584
.
Cited by:
§1
.
Meta (2024)
Meta
Meta-llama/llama-3.1-8b-instruct (model card)
.
Note:
https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
Accessed: 2026-01-26
Cited by:
§5.1
.
Mielke
et al.
(2022)
S. J. Mielke, A. Szlam, E. Dinan, and Y. Boureau
Reducing conversational agents’ overconfidence through linguistic calibration
.
Transactions of the Association for Computational Linguistics
10
,
pp. 857–872
.
External Links:
Link
,
Document
Cited by:
§2.1
.
Molina
et al.
(2025)
F. Molina, A. Gorla, and M. d’Amorim
Test oracle automation in the era of llms
.
ACM Transactions on Software Engineering and Methodology
34
(
5
),
pp. 1–24
.
Cited by:
§2.2
.
Nikitin
et al.
(2024)
A. Nikitin, J. Kossen, Y. Gal, and P. Marttinen
Kernel language entropy: fine-grained uncertainty quantification for llms from semantic similarities
.
Advances in Neural Information Processing Systems
37
,
pp. 8901–8929
.
Cited by:
§2.1
,
§3
.
OpenAI (2025a)
OpenAI
GPT-4.1 mini model (openai api documentation)
.
Note:
https://platform.openai.com/docs/models/gpt-4.1-mini
Accessed: 2026-01-26
Cited by:
§5.1
.
OpenAI (2025b)
OpenAI
GPT-4.1 nano model (openai api documentation)
.
Note:
https://platform.openai.com/docs/models/gpt-4.1-nano
Accessed: 2026-01-26
Cited by:
§5.1
.
Ouyang
et al.
(2025)
S. Ouyang, J. M. Zhang, M. Harman, and M. Wang
An empirical study of the non-determinism of chatgpt in code generation
.
ACM Transactions on Software Engineering and Methodology
34
(
2
),
pp. 1–28
.
Cited by:
§1
.
Pan
et al.
(2024)
R. Pan, A. R. Ibrahimzada, R. Krishna, D. Sankar, L. P. Wassi, M. Merler, B. Sobolev, R. Pavuluri, S. Sinha, and R. Jabbarvand
Lost in translation: a study of bugs introduced by large language models while translating code
.
In
Proceedings of the IEEE/ACM 46th International Conference on Software Engineering
,
pp. 1–13
.
Cited by:
§5.1
.
Puri
et al.
(2021)
R. Puri, D. S. Kung, G. Janssen, W. Zhang, G. Domeniconi, V. Zolotov, J. Dolby, J. Chen, M. Choudhury, L. Decker, V. Thost, L. Buratti, S. Pujar, S. Ramji, U. Finkler, S. Malaika, and F. Reiss
CodeNet: a large-scale AI for code dataset for learning a diversity of coding tasks
.
In
Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)
,
External Links:
Link
Cited by:
§5.1
.
Qing
et al.
(2026)
Y. Qing, B. Zhu, M. Du, Z. Guo, T. Y. Zhuo, Q. Zhang, J. Zhang, H. Cui, S. M. Yiu, D. Huang,
et al.
Effibench-x: a multi-language benchmark for measuring efficiency of llm-generated code
.
Advances in Neural Information Processing Systems
38
.
Cited by:
§5.1
.
Qiu and Miikkulainen (2024)
X. Qiu and R. Miikkulainen
Semantic density: uncertainty quantification for large language models through confidence measurement in semantic space
.
Advances in neural information processing systems
37
,
pp. 134507–134533
.
Cited by:
§3
,
§5.1
.
Sharma and David (2025)
A. Sharma and C. David
Assessing correctness in llm-based code generation via uncertainty estimation
.
arXiv preprint arXiv:2502.11620
.
Cited by:
§2.1
.
Shorinwa
et al.
(2025)
O. Shorinwa, Z. Mei, J. Lidard, A. Z. Ren, and A. Majumdar
A survey on uncertainty quantification of large language models: taxonomy, open research challenges, and future directions
.
ACM Computing Surveys
.
Cited by:
§2.1
.
Song
et al.
(2024)
D. Song, X. Xie, J. Song, D. Zhu, Y. Huang, F. Juefei-Xu, and L. Ma
Luna: a model-based universal analysis framework for large language models
.
IEEE Transactions on Software Engineering
50
(
7
),
pp. 1921–1948
.
Cited by:
§2.2
.
Spiess
et al.
(2025)
C. Spiess, D. Gros, K. S. Pai, M. Pradel, M. R. I. Rabin, A. Alipour, S. Jha, P. Devanbu, and T. Ahmed
Calibration and correctness of language models for code
.
ICSE ’25
,
pp. 540–552
.
External Links:
ISBN 9798331505691
,
Link
,
Document
Cited by:
§1
,
§2.1
,
§2.1
,
§4.2.1
.
Team (2025)
Q. Team
Qwen/qwen2.5-7b-instruct (model card)
.
Note:
https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
Accessed: 2026-01-26
Cited by:
§5.1
.
Tian
et al.
(2023)
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. Manning
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
H. Bouamor, J. Pino, and K. Bali (Eds.)
,
Singapore
,
pp. 5433–5442
.
External Links:
Link
,
Document
Cited by:
§2.1
.
Tong and Zhang (2024)
W. Tong and T. Zhang
CodeJudge: evaluating code generation with large language models
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 20032–20051
.
External Links:
Link
,
Document
Cited by:
§2.2
.
Virk
et al.
(2025)
Y. Virk, P. Devanbu, and T. Ahmed
Calibration of large language models on code summarization
.
Proc. ACM Softw. Eng.
2
(
FSE
).
External Links:
Link
,
Document
Cited by:
§2.1
.
Wang
et al.
(2024)
Y. Wang, R. Zheng, L. Ding, Q. Zhang, D. Lin, and D. Tao
Uncertainty aware learning for language model alignment
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 11087–11099
.
External Links:
Link
,
Document
Cited by:
§2.1
.
Wang
et al.
(2025)
Z. Wang, Z. Zhou, D. Song, Y. Huang, S. Chen, L. Ma, and T. Zhang
Towards understanding the characteristics of code generation errors made by large language models
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)
,
pp. 717–717
.
Cited by:
§5.1
.
[68]
(2026)
Website for this work
.
Note:
https://github.com/hnurxn/Code-Uncertainty
Cited by:
§5.4
.
Wu
et al.
(2025)
M. Wu, C. Zhou, S. Bates, and T. Jaakkola
Thought calibration: efficient and confident test-time scaling
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 14291–14305
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§1
.
Xiao
et al.
(2025)
Z. Xiao, D. Dou, B. Xiong, Y. Chen, and G. Chen
Enhancing uncertainty estimation in llms with expectation of aggregated internal belief
.
arXiv preprint arXiv:2509.01564
.
Cited by:
§2.1
.
Xie
et al.
(2013)
X. Xie, T. Y. Chen, F. Kuo, and B. Xu
A theoretical analysis of the risk evaluation formulas for spectrum-based fault localization
.
ACM Transactions on software engineering and methodology (TOSEM)
22
(
4
),
pp. 1–40
.
Cited by:
§2.1
.
Xiong
et al.
(2024)
M. Xiong, Z. Hu, X. Lu, Y. LI, J. Fu, J. He, and B. Hooi
Can LLMs express their uncertainty? an empirical evaluation of confidence elicitation in LLMs
.
In
The Twelfth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§2.1
,
§3
.
Yang
et al.
(2025)
B. Yang, M. A. Al Mamun, J. M. Zhang, and G. Uddin
Hallucination detection in large language models with metamorphic relations
.
Proceedings of the ACM on Software Engineering
2
(
FSE
),
pp. 425–445
.
Cited by:
§2.2
.
Zhang
et al.
(2020)
X. Zhang, X. Xie, L. Ma, X. Du, Q. Hu, Y. Liu, J. Zhao, and M. Sun
Towards characterizing adversarial defects of deep learning software from the lens of uncertainty
.
In
Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering
,
pp. 739–751
.
Cited by:
§2.1
.
Zhang
et al.
(2025)
Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma, W. Zhong, J. Chen, M. Mao, and Z. Zheng
Llm hallucinations in practical code generation: phenomena, mechanism, and mitigation
.
Proceedings of the ACM on Software Engineering
2
(
ISSTA
),
pp. 481–503
.
Cited by:
§2.2
.
Zhao
et al.
(2025)
X. Zhao, Z. Kang, A. Feng, S. Levine, and D. Song
Learning to reason without external rewards
.
arXiv preprint arXiv:2505.19590
.
Cited by:
§1
.
Zhou
et al.
(2025)
H. Zhou, J. V. Landeghem, T. Popordanoska, and M. B. Blaschko
A novel characterization of the population area under the risk coverage curve (AURC) and rates of finite sample estimators
.
In
Forty-second International Conference on Machine Learning
,
External Links:
Link
Cited by:
§5.3.1
.
Zhou
et al.
(2015)
Z. Q. Zhou, S. Xiang, and T. Y. Chen
Metamorphic testing for software quality assessment: a study of search engines
.
IEEE Transactions on Software Engineering
42
(
3
),
pp. 264–284
.
Cited by:
§2.1
.
Zhu
et al.
(2025)
Y. Zhu, G. Li, X. Jiang, J. Li, H. Mei, Z. Jin, and Y. Dong
Uncertainty-guided chain-of-thought for code generation with llms
.
arXiv preprint arXiv:2503.15341
.
Cited by:
§1
.