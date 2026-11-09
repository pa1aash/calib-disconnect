---
title: Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code
  Revision
id: fine-grained-approaches-for-confidence-calibration-of-llms-in-automated-code-rev
tags:
- code-llm-calibration-aaai27-eabf3f
- locus-code-verbal-calibration-occupied-or-open
- internal-logit-signal
- post-hoc-platt-scaling
- code-revision-not-generation
created: '2026-07-17T18:57:44.640325Z'
updated: '2026-07-17T19:01:24.784058Z'
source: https://arxiv.org/html/2604.06723
source_domain: arxiv.org
fetched_at: '2026-07-17T18:57:44.639768Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Lin, Liu, Gao, Thongtanunam & Treude (Univ. Melbourne/Singapore Management
  Univ., arXiv 2604.06723, cs.SE). Studies confidence calibration for automated code
  revision (ACR: program repair, vulnerability repair, code refinement/review-comment
  resolution) across 14 models. The confidence signal is entirely INTERNAL/LOGIT-DERIVED,
  never verbalized: they compare sequence-level scores (normalised sequence likelihood,
  average token probability) against three new fine-grained scores (minimum token
  probability, lowest-K token probability, attention-weighted uncertainty), all read
  off the softmax over the model''s own generated tokens. Calibration method is POST-HOC
  (local vs. global Platt-scaling fit per task/cluster on held-out data), not train-time
  and not RL/SFT on the model''s confidence expression. Discrimination is measured
  via Wasserstein-1 distance (W1) and Kendall''s tau_b rank correlation between the
  confidence-score distributions of correct vs incorrect revisions -- NOT AUROC. Key
  numbers: minimum token probability gives the widest separation (Exact-Match W1:
  0.13-0.26; Edit-Pass W1: 0.13-0.20) vs 0.01-0.03 for sequence-level scores; minimum-token-probability
  tau_b of 0.26-0.45 (EM) / 0.24-0.37 (EP). Relevant as a negative case: confirms
  that even the most code-specific 2026 calibration paper in this space still treats
  confidence purely as an internal/post-hoc-calibrated signal, not as something trained
  into the model''s verbalized output.'
---

Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2604.06723v1 [cs.SE] 08 Apr 2026
Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision
Hong Yi Lin, 
Chunhua Liu, 
Haoyu Gao, 
Patanamon Thongtanunam, 
Christoph Treude
Abstract
In today’s AI-assisted software engineering landscape, developers increasingly depend on large language models (LLMs) that are highly capable, yet inherently imperfect.
The tendency of these models to produce incorrect outputs can interrupt a developer’s workflow and reduce developer productivity.
One approach to improving developer interactions with these imperfect models is to provide greater transparency at the instance-level.
This is often achieved by complementing the model generated output with a well-calibrated confidence score that faithfully reflects the likelihood correctness.
Such information allows users to make immediate decisions regarding output acceptance, abstain error-prone outputs, and better align their expectations with the model’s capabilities.
Since post-trained LLMs do not inherently produce well-calibrated confidence scores, researchers have developed post-hoc calibration methods, with global Platt-scaling of sequence-level confidence scores proving effective in many generative software engineering tasks but remaining unreliable or unexplored for automated code revision tasks such as program repair, vulnerability repair, and code refinement.
We hypothesise that the coarse-grained nature of this conventional method makes it ill-suited for automated code revision tasks, where correctness is often determined by local edit decisions and miscalibration can be sample-dependent, thereby motivating fine-grained confidence calibration.
To address this challenge, our study proposes local Platt-scaling applied separately to three different fine-grained confidence scores.
Through our experiments across three separate tasks and correctness metrics, as well as 14 different models of various sizes, we find that fine-grained confidence scores consistently achieve lower calibration error across a broader range of probability intervals compared to sequence-level confidence scores, and this effect is further amplified when global Platt-scaling is replaced with local Platt-scaling.
As a practical recommendation, we find that global Platt-scaling with fine-grained confidence scores can produce estimates with sufficiently low calibration error for program and vulnerability repair when inference latency is a priority; otherwise, applying local Platt-scaling can achieve the greatest reduction in calibration error at the cost of additional computation.
On the other hand, for automated code refinement, applying local Platt-scaling with fine-grained confidence scores is essential for producing estimates with sufficiently low calibration error.
Our replication package can be found here:
https://github.com/hongyi-tom/FinegrainedCalibrationACR
I
Introduction
Large Language Models have become an indispensable tool for today’s software developer.
Their proficiency in both natural language and source code allows them to be instructed to perform a wide range of daily code revision activities, such as repairing buggy programs
[
57
]
, patching security vulnerabilities
[
46
]
, and resolving code review comments
[
15
]
.
Whilst these models have shown the potential to enhance developer productivity, their susceptibility to generating incorrect outputs can also create friction that limits their synergy with human developers
[
27
]
.
More specifically, incorrect code generations can disrupt a developer’s workflow due to the time wasted in debugging and rewriting implementations
[
64
]
.
When occurring repeatedly, these inaccuracies can even induce frustration, annoyance, and distrust, eventually causing some developers to abandon the tool altogether
[
42
]
.
Figure 1:
Miscalibrated (Left) and Well-Calibrated (Right) Confidence Scores for Code Revisions Generated by CodeLlama-70B in Automated Code Refinement
To this end, prior research have shown that interactions with imperfect models can be enhanced through increased model transparency and information integrity at the instance-level
[
40
,
3
,
42
,
69
]
.
This is often operationalised as a quantifiable measure—namely, the confidence score assigned by the model to a given output
[
69
,
3
,
37
]
.
A well-calibrated confidence score which faithfully reflects the model’s empirical likelihood of correctness, enables model users to make immediate decisions about whether to disregard its output
[
69
]
.
Such a measure also supports abstention mechanisms, whereby outputs that have been assigned a confidence score that is below a certain pre-selected threshold are suppressed
[
78
]
.
Tangential to this, explicitly communicating a trustworthy measure of the model’s uncertainty can help align the expectations with the model’s capability, thereby mitigating over reliance, or excessive scepticism
[
53
,
49
,
7
,
82
]
.
For a software developer, such information can support routine decision-making regarding when the boundaries of the model’s coding capabilities are exceeded and human-written implementations are needed.
However, these benefits are contingent on the availability of well-calibrated confidence scores, which post-trained LLMs are generally unable to provide out-of-the-box
[
86
,
34
,
35
,
55
]
, giving rise to the long-standing field of confidence calibration
[
14
]
.
Although prior research on confidence calibration for software engineering tasks have reported promising results across a variety of generative tasks, including line completion, function synthesis
[
60
]
, and code summarisation
[
66
]
, these methods have either not been examined or proven ineffective for automated code revision (ACR) tasks, which form an important class of real-world software quality assurance activities.
In particular, existing post-hoc calibration approaches such as Platt-scaling
[
48
]
i.e., a single logistic regression that maps sequence-level confidence scores to correctness probabilities, have been found to be ineffective for program repair
[
60
]
and have not yet been evaluated on core tasks like vulnerability repair
[
46
]
and automated code refinement
[
28
]
.
We hypothesise that the coarse-grained nature of this conventional method is unsuitable for the ACR scenario.
Firstly, we posit that sequence-level confidence scores
[
60
]
are unable to reflect meaningful uncertainty for ACR tasks, where the most salient signals are concentrated in local edit decisions.
If the vast majority of the revised code sequence represent trivial model decisions, then the probability mass over the entire sequence for a correct code revision will be similar to an incorrect one.
Secondly, the use of a single calibrator implies a coarse-grained assumption of uniformity in the mapping between uncalibrated confidence scores and true probabilities of correctness.
However, no prior evidence suggests that a model’s calibration error for all possible samples of a given task lies on a shared sigmoid function.
Given the potential for streamlining LLM-augmented developer workflows, this study explores fine-grained calibration approaches for eliciting well-calibrated confidence scores in ACR tasks.
We address this issue by proposing two fine-grained confidence calibration approaches, namely the use of fine-grained confidence scores and local Platt-scaling.
Firstly, we propose three fine-grained confidence scores: minimum token probability, lowest-
K
K
token probability, and attention-weighted uncertainty, and compare them with two traditional sequence-level confidence scores: normalised sequence likelihood and average token probability
[
60
]
.
Secondly, we replace conventional Platt-scaling, which shares a single calibrator amongst all samples of a given task (global Platt-scaling), with local Platt-scaling, a sample-aware method that selects from an ensemble of local calibrators according to embedding-based cluster assignment.
Through our experiments, we demonstrate that fine-grained confidence scores consistently achieve lower calibration error across a wider range of probability intervals than sequence-level scores.
In particular, minimum token probability is the best-performing confidence score across all tasks, correctness metrics, and models considered.
Furthermore, we find that local Platt-scaling outperforms the conventional global implementation, with particularly strong effectiveness for automated code refinement and, to a lesser extent, for automated program and vulnerability repair.
Figure
1
shows a reliability plot comparing miscalibrated confidence scores produced by the conventional method against well-calibrated confidence scores produced by combining our two fine-grained approaches.
These results indicate that both fine-grained confidence scores and local Platt-scaling are more effective methods for yielding well-calibrated confidence estimates in ACR tasks.
Based on our findings, we provide the following practical recommendations for those intending to use our fine-grained approaches for confidence calibration.
In terms of program and vulnerability repair, global Platt-scaling with fine-grained confidence scores can yield adequately calibrated confidence estimates while incurring negligible latency overhead.
As such, the decision to further incorporate local Platt-scaling to achieve enhanced calibration, at the cost of additional latency, may therefore be delegated to the user.
For automated code refinement, the application of local Platt-scaling is essential for correcting severe confidence miscalibration.
Contributions:
•
The first to propose fine-grained confidence scores for calibration in ACR tasks, revealing salient uncertainty signals hidden in local edit decisions that sequence-level confidence scores failed to capture
•
The first to propose local Platt-scaling for calibration in ACR tasks, correcting sample-dependent miscalibration patterns that the conventional method of global Platt-scaling failed to capture
•
A comprehensive analysis of five confidence scores and two calibration methods across three ACR tasks and correctness metrics for 14 different models
II
Related Work
This work spans the domains of LLM-based automated code revision and confidence calibration in machine learning.
II-A
Automated Code Revision.
Following rapid gains in the general effectiveness of LLMs, the field of AI for software engineering has largely converged on these types of models for generative tasks
[
17
]
.
Specifically, they have demonstrated state-of-the-art capabilities in automating code revision-based software quality assurance tasks.
In this study, we focus on three of the most extensively researched ACR tasks for software quality assurance: automated program repair, vulnerability repair, and automated code refinement.
Automated program repair
[
58
,
57
,
73
]
aims to generate bug-fixing patches for erroneous code, typically addressing functional defects that cause incorrect program behaviour.
Vulnerability repair
[
46
,
83
]
aims to generate security patches, fixing weaknesses in code that expose the software to potential exploits.
Automated code refinement
[
15
,
63
,
28
]
seeks to resolve code review comments in pull requests.
They cover a wide variety of issues, ranging from critical defects to maintainability concerns
[
39
]
.
Whilst prior work emphasises improving the correctness of LLM-generated code revisions, our study instead addresses how to accurately communicate their likelihood of correctness, enabling trustworthy and efficient use in their current, imperfect state.
II-B
Confidence Calibration.
The field of confidence calibration has a long-standing history in machine learning, where it plays a key role in ensuring trustworthy applications ranging from natural language processing
[
86
,
6
,
70
]
to computer vision
[
33
,
62
,
20
]
.
Prior work on LLMs indicate that larger model sizes and longer pretraining are associated with improved confidence calibration when performance is far from saturation
[
6
]
, whereas extensive post-training often degrades it
[
86
]
.
In general, deep learning models are uncalibrated by default and therefore require post-hoc calibration techniques to align the model’s confidence with their likelihood of correctness
[
14
]
.
Traditional post-hoc calibration techniques include statistical methods, e.g., Platt-scaling
[
48
]
, temperature scaling
[
14
]
, histogram binning
[
79
]
, and isotonic regression
[
80
]
, which only require the original inference step from the underlying LLM, whereas more recent techniques, e.g., P(True)
[
21
,
61
,
29
]
and stochastic sampling
[
8
]
, require additional rounds of inference.
Amongst traditional post-hoc calibration techniques, histogram binning and isotonic regression involve a higher degree of parameterisation and are therefore prone to overfitting, making them ill-suited for the typical sizes of software engineering benchmarks
[
60
]
.
Since Platt-scaling is a strict generalisation of temperature scaling, owing to its additional bias term, we focus on the former technique.
Amongst the more recent techniques, P(True) prompts a well-calibrated LLM to estimate the probability that its previously generated output is correct, whereas stochastic sampling quantifies uncertainty through repeated sampling of it.
These techniques are not considered in our study as they belong to a different inference-time complexity where the latency is incomparable.
In the field of AI for software engineering, confidence calibration have been investigated for both code classification tasks
[
85
]
e.g., exception type, defect detection, clone detection, and code generation tasks
[
60
,
66
]
e.g., code summarisation, function synthesis, automated program repair.
Prior studies on calibration for code generation have shown that conventional Platt-scaling with sequence-level confidence scores is sufficient for most tasks, with the notable exception of program repair
[
60
]
.
We posit that code revision differs from general code generation, where solutions are produced from scratch rather than focused adaptations of existing code.
As such, salient uncertainty information is dependent on local contexts, rendering sequence-level confidence scores and conventional Platt-scaling overly coarse-grained.
Motivated by this hypothesis, our study investigates whether fine-grained calibration approaches can address this specific class of tasks.
Whilst the notion of fine-grained uncertainty has been explored in code generation, it has not yet been applied in real-world code revision tasks or to the context of calibration.
Additionally, these approaches either rely on auxiliary deep learning models trained on supplementary code-editing data that is seldom available
[
65
]
or repeated sampling techniques
[
19
]
that may not be feasible in actual deployment due to latency.
III
Problem Statement
We now formally introduce the problem of confidence calibration.
To be considered well-calibrated, a model’s confidence should approximate their empirical likelihood of correctness
[
14
]
.
Formally, given input
X
X
, a perfectly calibrated probabilistic model should satisfy the following condition:
P
(
y
^
=
y
∣
P
(
y
^
∣
X
)
=
p
^
)
=
p
~
,
∀
p
∈
[
0
,
1
]
P(\hat{y}=y\mid P(\hat{y}\mid X)=\hat{p})=\tilde{p},\forall p\in[0,1]
(1)
In this perfect parity, the model’s confidence in the output
p
^
\hat{p}
should be exactly equal to the empirical fraction of correct examples at that confidence level
p
~
\tilde{p}
, for all levels of model confidence.
In practice, it is impossible to achieve this continuous parity
∀
p
∈
[
0
,
1
]
\forall p\in[0,1]
with finite samples, therefore achieving a close empirical approximation, such that
p
^
≈
p
~
\hat{p}\approx\tilde{p}
in a target test-set should suffice for downstream applications.
IV
Study Design and Methodology
We formulate three research questions (RQs) to examine the suitability and effectiveness of fine-grained confidence calibration approaches for LLMs in ACR tasks.
RQ1. How well can fine-grained confidence scores separate correct from incorrect code revisions in ACR tasks?
H1:
Certain local edit decisions capture the most informative signals regarding correctness.
Motivated by this hypothesis, we set out to explore three fine-grained confidence scores, i.e., minimum token probability, lowest-
K
K
token probability, and attention-weighted uncertainty.
We compare their distributions with conventional sequence-level confidence scores i.e., normalised sequence likelihood, average token probability, to assess if they can better separate correct from incorrect code revisions.
This informs the extent to which fine-grained confidence scores are suitable for calibration.
RQ2. How effective is Platt scaling for ACR tasks when using fine-grained confidence scores?
To test whether our hypothesis on informative local edit decisions
(H1)
is effective in practice, we conduct global Platt-scaling with both fine-grained and sequence-level confidence scores to compare their effectiveness in confidence calibration across the ACR tasks.
Specifically, we are interested in the extent to which fine-grained confidence scores can produce informative and well-calibrated confidence estimates for ACR tasks, a feat previously unattainable with sequence-level confidence scores
[
60
]
.
RQ3. To what extent can local Platt-scaling improve over conventional Platt-scaling in ACR tasks?
H2:
Calibration errors can be non-uniform and sample-specific.
Motivated by this hypothesis, we investigate whether local Platt-scaling, a method that learns separate calibrators for distinct sample clusters, can provide the expressivity needed to better capture localised errors.
Specifically, we evaluate whether the fine-grained approach enhances calibration performance over the conventional method of global Platt-scaling for ACR tasks.
IV-A
Confidence Scores
This study focuses on intrinsic single inference measures of confidence due to practical considerations for model serving.
Specifically, we restrict our consideration to methods with low inference-time complexity to ensure minimal computational overhead and latency.
Since these methods rely on access to model internals, they are considered white-box methods.
IV-A
1
Sequence-Level Confidence Scores
We discuss the two separate sequence-level confidence scores commonly used in past calibration studies
[
70
,
60
,
66
]
.
They represent the baselines that our study aims to improve upon.
Normalised Sequence Likelihood.
This measure represents the model assigned likelihood for the generated output as a whole.
It is the product of the conditional probabilities assigned to each token in the output sequence.
The conditional probabilities are from the softmax layer of the auto-regressive LLM.
We adopt the formulation from prior work on confidence calibration for software engineering
[
60
]
.
The sequence likelihood can be formalised by the following equation:
P
s
​
l
​
(
y
^
)
=
∏
t
=
1
T
P
​
(
y
^
t
∣
y
^
<
t
,
X
)
P_{sl}(\hat{y})=\prod_{t=1}^{T}P(\hat{y}_{t}\mid\hat{y}_{<t},X)
(2)
Where
y
^
t
\hat{y}_{t}
is the current token being generated,
y
^
<
t
\hat{y}_{<t}
are the previously generated tokens, and
T
T
is the sequence length.
Since this measure penalises longer sequences, we consider the length normalised version.
The length normalised sequence likelihood can be formalised by the following equation:
P
s
​
l
​
_
​
n
​
o
​
r
​
m
​
(
y
^
)
=
P
s
​
l
​
(
y
^
)
1
T
P_{sl\_norm}(\hat{y})=P_{sl}(\hat{y})^{\frac{1}{T}}
.
This measure ensures that longer sequences which involve more token probabilities are not disproportionately penalised compared to shorter sequences that involve less token probabilities.
Average Token Probability.
This measure represents an average of the model assigned likelihoods to each token in the sequence.
This simply computes the arithmetic mean of the conditional token probabilities.
The average token probability can be formalised by the following equation:
P
a
​
v
​
g
​
(
y
^
)
=
1
T
​
∑
t
=
1
T
P
​
(
y
^
t
∣
y
^
<
t
,
X
)
P_{avg}(\hat{y})=\frac{1}{T}\sum_{t=1}^{T}P(\hat{y}_{t}\mid\hat{y}_{<t},X)
(3)
Whilst the normalised sequence likelihood uses a geometric mean that is sensitive to small probabilities, average token probability is instead sensitive to large probabilities due to the additive properties of the arithmetic mean.
IV-A
2
Fine-Grained Confidence Scores
Rather than consider the probabilities of all output tokens, we hypothesise that correctness in ACR tasks is best captured by the model assigned probabilities to local edit decisions
(H1)
.
Hence, we propose three fine-grained confidence scores that are also intrinsic and single inference: minimum token probability, lowest-K token probability, and attention-weighted uncertainty.
Each represents a different approach to determining the locality of salient decisions.
The concept of minimum token probability is well aligned with broader work in uncertainty quantification
[
38
]
under different formulations and domains, yet remains unexplored for automated software engineering tasks.
Meanwhile, lowest-
K
K
token probability and attention-weighted uncertainty are novel formulations of confidence introduced in this study.
Minimum Token Probability.
This measure represents the minimum likelihood assigned by the model to any token in the output sequence.
In ACR, edit decisions are often granular but critical
[
18
,
28
]
, where any single incorrect token may invalidate the entire implementation.
We therefore use this measure to reflect the potential fragility introduced by the model’s least confident decision.
The minimum token probability can be formalised by the following equation:
P
min
​
(
y
^
)
=
min
t
≤
T
⁡
P
​
(
y
^
t
∣
y
^
<
t
,
X
)
P_{\min}(\hat{y})=\min_{t\leq T}P(\hat{y}_{t}\mid\hat{y}_{<t},X)
(4)
Lowest-
K
K
Token Probability.
Unlike average token probability which indiscriminately averages probabilities over the entire output sequence, this measure restricts the averaging to tokens with the lowest-
K
K
probabilities.
Compared to minimum token probability, this measure should be more robust to individual outlier tokens that are mistakenly under-confident.
We utilise the arithmetic mean rather than the geometric mean due to the fact that these tokens can be disjoint.
The lowest-
K
K
token probability can be formalised by the following equation:
P
low
​
-
​
K
​
(
y
^
)
\displaystyle P_{\mathrm{low}\text{-}K}(\hat{y})
=
1
K
​
∑
t
∈
ℐ
K
P
​
(
y
^
t
∣
y
^
<
t
,
X
)
,
\displaystyle=\frac{1}{K}\sum_{t\in\mathcal{I}_{K}}P\big(\hat{y}_{t}\mid\hat{y}_{<t},X\big),
(5)
ℐ
K
\displaystyle\mathcal{I}_{K}
=
arg
​
sort
t
(
K
)
⁡
P
​
(
y
^
t
∣
y
^
<
t
,
X
)
\displaystyle=\operatorname*{arg\,sort}_{t}^{(K)}P\big(\hat{y}_{t}\mid\hat{y}_{<t},X\big)
Where
ℐ
K
\mathcal{I}_{K}
represents the set of token positions with the lowest-
K
K
token probabilities.
We use the Kneedle algorithm
[
54
]
to dynamically select
K
K
for each sample.
Following our hypothesis
(H1)
, if the majority of tokens lie in the high probability region whilst a minority of tokens lie in the low probability region, they will form a sharply increasing concave with a long plateau when sorted in ascending order.
The algorithm identifies the local maximum of the difference from the
y
=
x
y=x
diagonal in the concave curve, corresponding to the
K
t
​
h
K^{th}
token where the curve of token probabilities begins to plateau.
Similar to the original implementation
[
54
]
, we set a sensitivity of
S
=
0
S=0
and use the offline setting.
Attention-Weighted Uncertainty.
This measure extends the lowest-
K
K
token probability by incorporating attention-based, token-level weighting.
Our lowest-
K
K
token probability measure carries an assumption that all of the lowest token probabilities are equally informative.
However, it is possible that correctly generated tokens arise from diffuse softmax distributions.
Rather than reflecting the model’s uncertainty about correctness, these lower probabilities may instead arise from syntactic flexibility in the token completion i.e., multiple correct alternatives, or from the correct token being statistically rare in the training distribution
[
30
]
(e.g., unconventional syntax, formatting, expressions).
As such, we want to reduce their impact on the calculation of the confidence score, since they don’t meaningfully affect the overall correctness of the revision.
To address this, attention-weighted uncertainty scales each token’s probability according to their model assigned saliency in the generated code revision.
We quantify a token’s saliency using the attention mass assigned to it by subsequently generated tokens.
The intuition is that uncertainty in tokens with strong downstream influence should matter more than the aforementioned trivial tokens.
If such a token is assigned a low softmax probability, the likelihood of cascading errors in the rest of the code revision increases, and its uncertainty should therefore be more heavily weighted.
The attention-weighted uncertainty can be formalised by the following equation:
P
a
​
t
​
t
​
n
​
-
​
ω
​
(
y
^
)
\displaystyle P_{attn\text{-}\omega}(\hat{y})
=
1
K
​
∑
t
∈
ℐ
K
P
​
(
y
^
t
∣
y
^
<
t
,
X
)
,
\displaystyle=\frac{1}{K}\sum_{t\in\mathcal{I}_{K}}P\big(\hat{y}_{t}\mid\hat{y}_{<t},X\big),
(6)
ℐ
K
\displaystyle\mathcal{I}_{K}
=
arg
​
sort
t
(
K
)
⁡
[
w
t
⋅
(
1
−
P
​
(
y
^
t
∣
y
^
<
t
,
X
)
)
]
,
\displaystyle=\operatorname*{arg\,sort}_{t}^{(K)}\left[w_{t}\cdot\left(1-P\big(\hat{y}_{t}\mid\hat{y}_{<t},X\big)\right)\right],
where
​
w
t
\displaystyle\text{where }w_{t}
=
∑
j
=
t
T
A
~
j
,
t
+
1
\displaystyle=\sum_{j=t}^{T}\tilde{A}_{j,t}+1
Where
ℐ
K
\mathcal{I}_{K}
represents the set of token positions with the highest-
K
K
weighted token uncertainties.
Similar to lowest-
K
K
token probability, we use the Kneedle algorithm
[
54
]
to dynamically select
K
K
for each sample.
Unlike the lowest-
K
K
token probability setup, which orders softmax probabilities in ascending, concave order, we instead adopt a decreasing, convex ordering, as weighted uncertainties represent an inverse quantity and should be prioritised in descending order.
We compute
A
~
j
,
t
\tilde{A}_{j,t}
using the rollout method
[
1
]
, which estimates layer-wise attention propagation with residual stream effects.
IV-B
Calibration Techniques
Given that deep learning-based language models traditionally do not optimise with a calibration-aware loss function, the token probabilities they emit do not naturally approximate the aforementioned parity that is expected from a well-calibrated model
[
86
]
.
Thus, a conventional solution is to rescale the model’s own confidence in its generated sequence using post-hoc calibration techniques.
This study focuses on the statistical technique of Platt-scaling. We choose this method because it has minimal parameterisation, which makes it less prone to overfitting on typical software engineering benchmark sizes
[
60
]
.
Additionally, it has lightweight inference-time complexity i.e., introduces minimal computational overhead and latency.
Together, these properties make the method well-suited for practical deployment in software engineering tasks.
IV-B
1
Global Platt-scaling
This conventional method trains a univariate logistic regression model to map a target model’s real-valued outputs (e.g., decision scores) onto binary correctness outcomes using a held-out training set
[
48
]
.
Formally, this can be represented by the following equation:
P
​
(
y
=
1
∣
X
)
=
σ
​
(
w
​
p
^
+
β
)
P(y=1\mid X)=\sigma(w\hat{p}+\beta)
(7)
Where
σ
​
(
z
)
=
1
1
+
e
−
z
\sigma(z)=\frac{1}{1+e^{-z}}
and
w
,
β
∈
ℝ
w,\beta\in\mathbb{R}
are learnable parameters.
This method takes a global approach, where the single calibrator is shared across all samples for a given task.
IV-B
2
Local Platt-scaling
Since we will be proposing a localised version of the conventional method, we identify the baseline as global Platt-scaling, and our proposed approach as local Platt-scaling.
Conventional Platt-scaling assumes calibration errors are uniform across a task by learning only a single global calibrator.
However, the variability in code and specifications within ACR tasks can induce heterogeneous errors
[
67
,
9
,
77
]
(H2)
.
Because global Platt-scaling uses a single set of fixed parameters
w
w
and
β
\beta
, it lacks the expressivity to account for sample-dependent features, which can result in suboptimal uncertainty estimates for instances that deviate from the global average.
To address this potential shortfall, we propose local Platt-scaling, a calibration method that is sample-specific, and therefore capable of providing fine-grained calibration for different types of scenarios within an ACR task.
In contrast to global Platt-scaling, local Platt-scaling trains distinct calibrators for specific clusters of samples.
These clusters are partitioned according to a multidimensional space comprised of input/output embeddings, alongside their corresponding uncalibrated confidence scores.
Local platt-scaling can be formalised by the following equation:
P
​
(
y
=
1
∣
X
)
=
{
σ
​
(
w
k
​
p
^
+
β
k
)
if
​
H
​
(
ϕ
​
(
x
)
)
=
k
ψ
​
(
p
^
)
if
​
H
​
(
ϕ
​
(
x
)
)
=
−
1
P(y=1\mid X)=\begin{cases}\sigma(w_{k}\hat{p}+\beta_{k})&\text{if }H(\phi(x))=k\\
\psi(\hat{p})&\text{if }H(\phi(x))=-1\end{cases}
(8)
Where
ϕ
​
(
x
)
\phi(x)
denotes the feature vector that is constructed by concatenating an
n
n
-dimensional UMAP projection
[
41
]
of the input/output embeddings with the uncalibrated confidence score.
Following similar setups from past studies
[
9
]
, we used
n
=
20
n=20
dimensions.
For text embeddings, we used the Qwen3-Embedding-8B
[
81
]
model, as it is considered state-of-the-art for the coding domain at the time of writing
1
1
1
As of March 2026, based to the MTEB leaderboard
[
43
]
.
We selected HDBSCAN
[
5
]
to be the
H
​
(
⋅
)
H(\cdot)
clustering operator since it is a non-parametric method that can manage varying densities, detecting outliers, and automatically determining the optimal number of clusters.
The hyperparameters for HDBSCAN are
minimum cluster size
which defines the smallest number of points required to form a cluster and
minimum samples
which determines the density threshold required for a point to be considered a core part of a cluster rather than an outlier.
At training time, clusters and outliers are first identified based on a held-out training set, after which a separate local calibrator is fitted to each cluster.
During inference, the new instance’s cluster (or outlier) membership is determined based on its nearest neighbour.
If an instance is assigned to cluster
k
k
, the corresponding local calibrator is applied; otherwise, it is classified as an outlier, triggering our novel
ψ
​
(
⋅
)
\psi(\cdot)
backoff function.
The selection of the backoff strategy is treated as a hyperparameter, which can either be the conventional global calibrator or simply the uncalibrated confidence score.
IV-C
Descriptive Statistics
We now introduce the statistical measures used in RQ1 to support the preliminary analysis of token-level softmax probabilities and confidence scores before confidence calibration.
Median Token-level Skewness (
γ
~
1
\tilde{\gamma}_{1}
).
To explore whether fine-grained confidence scores have the potential to yield substantially different distributions compared to sequence-level confidence scores, we first analyse the skewness of token-level softmax probabilities in LLM-generated code revisions.
For each ACR benchmark, the per-sample skewness values are aggregated by taking their median across the test set.
If our hypothesis
(H1)
is correct, there should be strong negative skewness across each test set, which indicates that the majority of token probabilities in generated code revisions are clustered around higher probabilities, whilst a few outliers are assigned far lower token probabilities.
The median token-level skewness can be formalised by the following equation:
γ
~
1
=
median
i
=
1
N
⁡
(
1
T
i
​
∑
t
=
1
T
i
(
p
i
,
t
−
p
¯
i
s
i
)
3
)
\tilde{\gamma}_{1}=\operatorname{median}_{i=1}^{N}\left(\frac{1}{T_{i}}\sum_{t=1}^{T_{i}}\left(\frac{p_{i,t}-\bar{p}_{i}}{s_{i}}\right)^{3}\right)
(9)
Where
p
i
,
t
p_{i,t}
is the softmax probability of the
t
t
-th generated token in the
i
i
-th sample.
For the
i
i
-th sample,
T
i
T_{i}
is the number of generated tokens,
p
¯
i
\bar{p}_{i}
is the mean of the token probabilities, and
s
i
s_{i}
is the standard deviation of the token probabilities.
For the outer operator,
N
N
is the overall number of samples.
Wasserstein Distance (
W
1
W_{1}
).
To compare sequence-level and fine-grained confidence scores in terms of their inherent ability to separate the distributions of correct and incorrect code revisions, we use the Wasserstein distance.
This statistic quantifies the minimal “effort” required to transform one probability distribution into another in metric space, where a higher
W
1
W_{1}
reflects wider separation.
If our hypothesis
(H1)
is correct, we expect
W
1
W_{1}
of fine-grained confidence scores to be higher than sequence-level confidence scores.
The Wasserstein distance can be formalised by the following discrete equation:
W
1
=
min
π
∈
Π
​
(
μ
,
ν
)
​
∑
i
=
1
n
∑
j
=
1
m
|
p
i
−
p
j
|
​
π
i
​
j
W_{1}=\min_{\pi\in\Pi(\mu,\nu)}\sum_{i=1}^{n}\sum_{j=1}^{m}|p_{i}-p_{j}|\pi_{ij}
(10)
Where
p
i
p_{i}
and
p
j
p_{j}
are the confidence scores of individual samples drawn from distributions
μ
\mu
and
ν
\nu
, respectively.
These two distributions represent the correct and incorrect code revisions, where
n
n
and
m
m
are their respective number of samples.
The most efficient way to morph one distribution into the other is captured by
π
i
​
j
\pi_{ij}
, the optimal transport plan.
Kendall’s
τ
\tau
Coefficient
(
τ
b
)
(\tau_{b})
.
To compare sequence-level and fine-grained confidence scores in terms of their inherent ability to preserve the ranking consistency between correct and incorrect code revisions, we use Kendall’s
τ
\tau
coefficient.
This statistic measures each confidence score’s ability to sort correct and incorrect code revisions, where a higher
τ
b
\tau_{b}
represents better rank correlation.
If our hypothesis
(H1)
is correct, we expect
τ
b
\tau_{b}
of fine-grained confidence scores to be higher than sequence-level confidence scores.
The Kendall’s
τ
\tau
coefficient can be formalised by the following equation:
τ
b
=
n
c
−
n
d
(
n
0
−
n
1
)
​
(
n
0
−
n
2
)
\tau_{b}=\frac{n_{c}-n_{d}}{\sqrt{(n_{0}-n_{1})(n_{0}-n_{2})}}
(11)
Were
n
c
n_{c}
and
n
d
n_{d}
are the numbers of concordant and discordant pairs.
The total number of pairs is denoted by
n
0
n_{0}
, whilst
n
1
n_{1}
and
n
2
n_{2}
are the number tie adjustments for each variable.
In our case, these variables are the chosen confidence score and correctness label.
For a given confidence score, stronger measures in both
W
1
W_{1}
and
τ
b
\tau_{b}
indicate a structure that closely approximates a monotonic, calibratable relationship with the correctness label, and thus greater amenability to Platt-scaling.
IV-D
Calibration Metrics
We now introduce the main metrics used to measure the degree of confidence calibration in both RQ2 and RQ3.
If both hypotheses
(H1)
and
(H2)
hold, we expect the introduction of fine-grained confidence scores and local Platt-scaling to yield improvements in these metrics compared to sequence-level confidence scores with global Platt-scaling.
Expected Calibration Error (ECE).
To measure confidence calibration, we require a metric that can capture the degree of mismatch between a model’s confidence and its correctness using finite samples.
To this end, expected calibration error
E
​
C
​
E
ECE
[
44
]
has been the standard in past research
[
14
,
60
,
66
]
.
As demonstrated in Figure
1
, this metric reflects the confidence-correctness mismatch based on model outputs that have been discretised into bins.
The expected calibration error can be formalised by the following equation:
E
​
C
​
E
=
∑
b
=
1
B
P
​
(
b
)
⋅
|
o
b
−
e
b
|
ECE=\sum_{b=1}^{B}P(b)\cdot|o_{b}-e_{b}|
(12)
Where
B
B
is the number of bins,
o
b
o_{b}
is the fraction of correct outputs within the
b
th
b^{\text{th}}
bin,
e
b
e_{b}
is the average confidence within the
b
th
b^{\text{th}}
bin, and
P
​
(
b
)
P(b)
is the fraction of all outputs that fall into the
b
th
b^{\text{th}}
bin.
Following prior studies
[
60
]
, we use
B
=
10
B=10
equal width bins to partition the entire confidence range.
Brier Score (
ℬ
\mathcal{B}
).
Since
E
​
C
​
E
ECE
can be sensitive to the choice of binning mechanism
[
24
,
45
,
52
]
, particularly when small sample sizes lead to sparse bins, we additionally report the Brier score
ℬ
\mathcal{B}
[
13
]
, which avoids binning altogether.
The Brier score can be formalised by the following equation:
ℬ
=
1
N
​
∑
i
=
1
N
(
p
i
−
𝟙
​
(
f
​
(
X
i
)
)
)
2
\mathcal{B}=\frac{1}{N}\sum_{i=1}^{N}(p_{i}-\mathbbm{1}(f(X_{i})))^{2}
(13)
Where
N
N
is the overall number of samples,
p
i
p_{i}
is the model’s confidence in the
i
th
i^{\text{th}}
output, and
𝟙
​
(
f
​
(
X
i
)
)
\mathbbm{1}(f(X_{i}))
is a binary correctness function that evaluates to value
∈
{
1
,
0
}
\in{\{1,0\}}
based on the
i
th
i^{\text{th}}
output.
This metric has the advantage of being well-defined for any sample size
N
N
.
However,
E
​
C
​
E
ECE
is widely regarded as a calibration-focused metric, whereas
ℬ
\mathcal{B}
captures both accuracy and confidence calibration, potentially conflating the two. Accordingly, we report both metrics as complementary perspectives for a more comprehensive evaluation.
Bin Coverage (BC).
For any downstream application, a well-calibrated confidence score should also be informative over the wider probability space, i.e., reasonable coverage of confidence bins.
Figure
1
illustrates confidence scores under limited bin coverage (left) and high bin coverage (right).
This is a key component to the original goal of confidence calibration
[
14
]
, as stated by the condition in Equation
1
.
The importance of inducing such a trustworthy confidence score lies in its ability to support more granular decision-making across a wider range of probability intervals
[
68
]
.
This enables finer distinctions in uncertainty, allowing different decisions or thresholds to be applied based on varying confidence scores rather than a limited set of cutoffs.
To measure this, we include bin coverage
B
​
C
BC
, which counts the number of bins that are covered by the calibrated confidence score.
In our case, the maximum bin coverage would be
B
=
10
B=10
, which means that every confidence level is represented.
In past experiments with automated program repair
[
60
]
, global Platt-scaling with sequence-level confidence scores induced single bin collapse i.e.,
B
​
C
=
1
BC=1
, effectively producing near identical confidence scores for all samples in the test set.
Since this type of degenerate confidence score lacks the capability of instance-level discrimination, it cannot support decision-making or thresholding.
Following past work
[
60
]
,
E
​
C
​
E
ECE
and
ℬ
\mathcal{B}
results are ignored for this type of scenario.
IV-E
Automated Code Revision Benchmarks
To assess confidence calibration across the ACR tasks, we carefully select benchmarks that utilise real-world examples.
These benchmarks are also deliberately curated with the intention to mitigate data leakage which may cause calibration results to appear deceptively optimistic
[
50
]
.
Additionally, we require benchmarks to be substantially large such that we are able to reliably compute calibration error.
Below, we describe three ACR benchmarks used in this study.
Automated Program Repair.
We use the non-security partition of the DeepCode AI Fix benchmark (DCF-Bug)
[
4
]
, as it is the only program repair dataset that satisfies our criteria: it contains real-world examples, is non-contaminated, and is sufficiently large.
Specifically, the task is formulated as
P
​
(
C
f
​
i
​
x
∣
C
b
​
u
​
g
,
V
n
​
l
)
P(C_{fix}\mid C_{bug},V_{nl})
, where
C
f
​
i
​
x
C_{fix}
is the fixed code snippet to be inferred,
C
b
​
u
​
g
C_{bug}
is the buggy code snippet submitted as input, and
V
n
​
l
V_{nl}
is the violated static analysis rule that can be considered as the natural language specification.
This benchmark includes 777 non-security related bugs from 489 GitHub repositories written in JavaScript and TypeScript.
The static analysis rules check for issues such as missing tags, duplicate variable names, invalid dataflows, resource leaks, and incorrect method interaction.
Concerns regarding data leakage are mitigated by the projects’ non-permissive licenses, which explicitly prohibit LLM training whilst permitting evaluation.
To support Platt-scaling, we use the training set accompanying DCF-Bug, which includes 1,917 bugs from 1,123 different GitHub repositories that use permissive licenses.
Vulnerability Repair.
We use the security partition of the DeepCode AI Fix benchmark (DCF-Vul)
[
4
]
, as it is the only vulnerability repair dataset that satisfies our criteria: it contains real-world examples, is non-contaminated, and is sufficiently large.
Specifically, the task is formulated as
P
​
(
C
f
​
i
​
x
∣
C
v
​
u
​
l
,
V
n
​
l
)
P(C_{fix}\mid C_{vul},V_{nl})
, where
C
f
​
i
​
x
C_{fix}
is the fixed code snippet to be inferred,
C
v
​
u
​
l
C_{vul}
is the vulnerable code snippet submitted as input, and
V
n
​
l
V_{nl}
is the violated static application security testing (SAST) rule that can be considered as the natural language specification.
This benchmark includes 1,041 security fixes from 600 GitHub repositories written in JavaScript and TypeScript.
The static analysis rules check for issues such as unsecure API usage, security misconfigurations, and dataflow vulnerabilities.
Similarly, concerns regarding data leakage are mitigated by the projects’ non-permissive licenses.
To support Platt-scaling, we use the training set accompanying DCF-Vul, which includes 1,615 vulnerabilities from 1,008 different GitHub repositories that use permissive licenses.
Automated Code Refinement.
We use the CodeReviewQA benchmark
[
28
]
, as it is the only automated code refinement test set that is manually curated; other datasets in this space are known to contain substantial noise
[
63
]
.
Specifically, the task is formulated as
P
​
(
C
p
​
o
​
s
​
t
∣
C
p
​
r
​
e
,
R
n
​
l
)
P(C_{post}\mid C_{pre},R_{nl})
, where
C
p
​
o
​
s
​
t
C_{post}
is the code snippet revised to address the attached code review comment
R
n
​
l
R_{nl}
, and
C
p
​
r
​
e
C_{pre}
is the code snippet under review.
This benchmark features 900 resolved code review comments from 199 GitHub repositories written in nine different programming languages, i.e., C, C++, C#, Go, Java, JavaScript, PHP, Python, and Ruby.
Given that these code reviews occurred in 2022 which may be susceptible to data contamination, we employed Gemini 2.5 Pro to transform the examples in terms of surface-level text (CR-Trans).
This involved using semantic-preserving transformations (e.g., identifier renaming, statement reordering) to refactor both
C
p
​
r
​
e
C_{pre}
and
C
p
​
o
​
s
​
t
C_{post}
code snippets
[
72
]
.
The natural language comments
R
n
​
l
R_{nl}
were then adapted to align with the transformed code snippets, as well as lightly paraphrased into different forms of expression (e.g., formality shifts, syntactic restructure).
All examples were manually verified for validity after the transformations.
To support Platt-scaling, we leveraged the CodeReviewer training set
[
26
]
, which is widely used in prior work
[
63
,
36
]
.
It contains 150k resolved GitHub code review comments.
Since this dataset has been shown to have high amounts of noise
[
63
]
, we first conducted LLM-based data cleaning
[
32
]
.
After validating on 50 examples, we find that Gemini 2.5 Pro can label clean data with 88% accuracy.
The remaining 12% comprised an even mix of borderline false positive and false negative cases, in which
R
n
​
l
R_{nl}
was contextually relevant to
C
p
​
r
​
e
C_{pre}
but necessitated nuanced reasoning to assess its alignment with
C
p
​
o
​
s
​
t
C_{post}
.
We subsequently used the LLM to clean the entire dataset.
To ensure comparability across tasks, we sampled a subset of examples to match the size of DCF-Bug’s training set.
The sampling was conducted in a stratified manner to maintain diversity of programming languages and repositories.
The final training set includes 1,917 code reviews from 140 different GitHub repositories resolved before 2022.
It includes the same nine programming languages mentioned above.
IV-F
Correctness Metrics for ACR Tasks
Selecting an appropriate correctness metric is critical as it determines the calibration target.
Specifically, these metrics evaluate whether a generated code revision is correct for a given ACR task.
In this section, we discuss the three separate correctness metrics considered in this study.
Exact Match.
To be considered correct, exact match
E
​
M
EM
requires the LLM-generated code revision to be identical to the ground truth implementation in terms of surface-level text.
That is
C
f
​
i
​
x
^
=
C
f
​
i
​
x
\hat{C_{fix}}=C_{fix}
and
C
p
​
o
​
s
​
t
^
=
C
p
​
o
​
s
​
t
\hat{C_{post}}=C_{post}
are the only scenarios where the generated code revision can be considered as correct.
We implement
E
​
M
EM
that is whitespace insensitive.
Edit Progress.
Whilst
E
​
M
EM
ensures no false positives are counted as correct, it can be overly strict, treating all generated code revisions that are non-identical to the ground truth implementation as equally incorrect.
To alleviate this, we utilise edit progress
E
​
P
EP
, a relaxed distance-based text matching metric
[
12
]
that is specifically designed for ACR-like tasks
[
84
]
.
From a productivity perspective, developers have deemed code generations that reduce the overall effort to complete the task as valuable
[
10
]
, even if they have not exactly fulfilled the developer’s intent.
Specifically,
E
​
P
EP
can be formalised by the following equation:
E
​
P
=
|
D
C
~
→
C
|
−
|
D
C
^
→
C
|
|
D
C
~
→
C
|
EP=\frac{|D_{\tilde{C}\rightarrow C}|-|D_{\hat{C}\rightarrow C}|}{|D_{\tilde{C}\rightarrow C}|}
(14)
Where
D
D
is the edit distance between two sequences
[
25
]
,
C
~
\tilde{C}
is the submitted code,
C
^
\hat{C}
is the candidate code revision, and
C
C
is the ground-truth code revision.
Therefore,
E
​
P
EP
represents the percentage of progress in transforming
C
~
\tilde{C}
to
C
C
, and (
1
−
E
​
P
1-EP
) represents the remaining effort to correct
C
^
\hat{C}
to
C
C
.
If a model generates more errors than correct edits,
E
​
P
EP
can be negative.
Following prior work
[
12
]
, we operationlise
E
​
P
EP
into a binary correctness metric, where any positive edit progress
E
​
P
+
EP^{+}
is considered as a net improvement to developer productivity.
Checks Passed.
This is a reference-free metric that instead relies on static analysis tools to check for correctness.
More specifically, we consider an LLM-generated code revision to be correct if it resolves the violated
V
n
​
l
V_{nl}
rule’s alarm without triggering any other alarms, i.e., passes all the checks ran by the static analysis tool.
The checks passed
C
​
P
CP
metric can capture semantically correct solutions with syntactically different implementations, i.e., a reduction in false negatives compared to
E
​
M
EM
.
As such,
C
​
P
CP
can determine if a solution is plausibly correct.
This particular metric is only applicable to DCF-Vul, as the relevant rules for DCF-Bug have been deprecated in the Snyk Code SAST engine
[
59
]
.
V
Experiment Setup
We now discuss the selected models, implementation details, as well as model performances on the ACR tasks.
V-A
Selected Models
We consider state-of-the-art LLMs from model families that are frequently included in research for ACR tasks.
Specifically, we consider models that use the canonical decoder-only transformer architecture, with billion scale parameter counts.
Given that our study is based on compute-efficient single inference measures of confidence, we only consider open-source models that allow white-box access.
We use instruction-tuned model variants as we need to engage in zero-shot prompting to perform the ACR tasks.
From the Llama series, we include Llama-3.1
[
46
,
28
]
and CodeLlama
[
46
,
57
]
.
From the Qwen series, we include Qwen2.5
[
58
,
28
]
and Qwen2.5-Coder
[
46
,
58
]
.
From the DeepSeek series (DS), we include DeepSeek-LLM
[
28
,
16
]
, DeepSeek-Coder
[
28
,
16
]
, DeepSeek-V2-Lite
[
58
,
28
]
, and DeepSeek-Coder-V2-Lite
[
46
,
28
]
.
We include a variation of architecture sizes from each series to increase the generalisability of our findings.
V-B
Implementation Details
To ensure consistency within the evaluation of each benchmark, we use the same prompt setups for all models.
Specifically, we only consider zero-shot prompts aimed at revising each code snippet within a single forward pass.
The aim of our study is to improve the intrinsic confidence calibration of the studied models, which can be difficult to interpret when conflated with the effects of advanced prompting mechanisms.
For each benchmark, we use the same context provided in the original study with the addition of instructions to only generate the code revision.
This controlled design allows us to examine the models’ confidence in its own code revision conditioned solely on the input prompt.
We use greedy decoding and deterministically select the single most probable candidate.
This represents the models’ strongest belief and is the sample most trusted by developers
[
2
]
.
To faithfully represent the models, we deploy them in their native bfloat-16 precision.
For Platt-scaling, we use the canonical implementation of logistic regression, which optimises via the limited-memory BFGS algorithm with a L2 penalty term for regularisation.
For local Platt-scaling, we optimise HDBSCAN’s hyperparameters via grid search.
For
minimum cluster size
we search 50-150 (step=25).
The lower bound ensures adequate support for logistic regression
[
47
]
, whilst the upper bound restricts cluster growth from approximating global Platt-scaling.
For
minimum samples
, we search 5-80 (step=15) to regulate the trade-off between local manifold sensitivity and density smoothing
[
5
]
.
The final results are presented based on the most optimal settings according to the three calibration metrics.
TABLE I:
Correctness (%) Achieved by LLMs in ACR Tasks
DCF-Bug
DCF-Vul
CR-Trans
n=777
n=1,041
n=900
Model
Size
EM
EP
EM
EP
CP
EM
EP
8B
32.9
59.3
7.7
29.2
59.6
36.3
59.3
Llama-3.1
70B
34.5
58.0
9.7
31.2
72.9
45.9
67.1
7B
32.3
55.6
8.8
26.1
40.2
40.1
60.4
CodeLlama
70B
40.5
66.8
12.0
29.0
44.9
51.8
72.4
7B
26.6
51.1
5.7
18.6
62.6
28.2
53.8
Qwen2.5
72B
27.9
52.1
3.7
16.0
70.2
46.0
71.0
7B
28.8
55.3
5.6
20.2
66.0
27.9
49.9
Qwen2.5-Coder
32B
32.8
57.4
5.8
20.3
70.3
37.9
64.0
7B
13.6
35.1
4.0
15.7
46.0
17.7
40.1
DS-LLM
67B
35.3
62.7
9.1
28.9
49.9
38.4
62.1
7B
30.5
58.0
8.6
27.1
62.4
35.6
58.9
DS-Coder
33B
38.0
63.6
8.6
30.3
66.3
42.1
67.9
DS-V2
16B
18.9
39.0
4.5
19.2
47.8
17.2
35.0
DS-Coder-V2
16B
32.9
56.9
6.3
23.9
57.7
33.1
55.1
Bold Number:
Best Result for that Task and Correctness Measure
EM:
Exact Match,
EP:
Edit Progress,
CP:
Checks Passed
V-C
Model Performance on ACR Tasks
We preliminarily assess the models’ competencies in the ACR tasks. Table
I
shows their performance in terms of each correctness metric.
Across the tasks, models generally struggle with DCF-Vul (EM: 3.7-12.0, EP: 15.7-31.2) more than DCF-Bug (EM: 13.6-40.5, EP: 35.1-66.8) and CR-Trans (EM: 17.2-51.8, EP: 35.0-72.4), when using
E
​
M
EM
and
E
​
P
EP
as correctness metrics.
However, when considering the more lenient
C
​
P
CP
metric in DCF-Vul, all models yielded far stronger performances (CP: 40.2-72.9).
For DCF-Vul, we omit exact match as a calibration target because models typically achieve less than 10% accuracy, resulting in the available positive signal being too sparse for effective calibration.
The remaining correctness metrics are retained as models attain comparatively reliable performances by their measurements, rendering them more suitable for decision-making or thresholding.
As expected, we find that larger model variants generally outperform their lightweight counterparts across all correctness metrics and tasks.
Overall, CodeLlama-70B achieves the best performances across both DCF-Bug and CR-Trans, whilst Llama-3.1-70B achieves the best performance for DCF-Vul.
VI
Results
RQ1. How well can fine-grained confidence scores separate correct from incorrect code revisions in ACR tasks?
This forms the preliminary analysis on token-level softmax probabilities and confidence scores before conducting calibration.
Figure
2
2
2
2
All p-values are statistically significant and are therefore omitted.
shows
γ
~
1
\tilde{\gamma}_{1}
values for each model and ACR task.
Confirming our hypothesis
(H1)
, the distributions of softmax probabilities consistently exhibit strong negative skewness for all models and tasks.
This indicates that low softmax probabilities are consistently centred around a few outlier tokens in the generated code revisions.
The
γ
~
1
\tilde{\gamma}_{1}
values range from -7.2 to -4.1 for DCF-Bug, -5.7 to -3.1 for DCF-Vul, and -7.7 to -4.1 for CR-Trans.
In the case of sequence-level confidence scores, signals from these outlier tokens will be averaged away by the cluster of higher probabilities, either by the geometric mean in normalised sequence likelihood or by the arithmetic mean in the average token probability.
In contrast, the fine-grained confidence scores are designed to identify and focus on these particular outliers, whilst discarding the overpowering effects from the cluster of higher probabilities.
Figure 2:
Median Skewness of Token-Level Softmax Probabilities for LLM-Generated Code Revisions (
γ
~
1
\tilde{\gamma}_{1}
)
Key Finding I:
Preliminary analysis indicates that
γ
~
1
\tilde{\gamma}_{1}
for generated code revisions in ACR tasks consistently exhibit strong negative skewness.
In such scenarios, fine-grained confidence scores preserve signal from low probability outliers that are suppressed by sequence-level averaging.
We also compare the distributions of correct and incorrect code revisions under each confidence score to assess their inherent ability to separate and rank them.
We leverage two statistical measures,
W
1
W_{1}
and
τ
b
\tau_{b}
[
22
]
, to facilitate the preliminary analysis.
These two statistical measures capture the extent to which each confidence score exhibits a monotonic, calibratable relationship with the correctness label, providing an initial indication of their amenability to Platt-scaling.
Figures
3
and
4
†
†
footnotemark:
show the
W
1
W_{1}
and
τ
b
\tau_{b}
for each confidence score and model in DCF-Bug.
For all models, we find that the fine-grained confidence scores are far better separated than sequence-level confidence scores.
Specifically, minimum token probability yields the widest separation (EM-
W
1
W_{1}
: 0.13-0.26, EP-
W
1
W_{1}
: 0.13-0.20), whilst sequence-level confidence scores have a separation of 0.01-0.03 for the majority of models against both correctness metrics.
In terms of rank correlation for both correctness metrics, we find that minimum token probability is consistently the top performer (EM-
τ
b
\tau_{b}
: 0.26-0.45, EP-
τ
b
\tau_{b}
: 0.24-0.37), whilst lowest-
K
K
token probability and attention-weighted uncertainty can equal or outperform the sequence-level confidence scores for 10 out of 14 models.
The sequence-level confidence scores achieve near identical rank correlation (EM-
τ
b
\tau_{b}
: 0.13-0.39, EP-
τ
b
\tau_{b}
: 0.18-0.32), which are on average the worst performers.
These results suggest that fine-grained confidence scores are on average more amenable to Platt-scaling for DCF-Bug.
As such, we expect more accurate confidence calibration when using them.
Figure 3:
DCF-Bug (Wasserstein Distance
W
1
W_{1}
)
Figure 4:
DCF-Bug (Kendall’s
τ
b
\tau_{b}
Coefficient)
Figures
5
and
6
†
†
footnotemark:
show the
W
1
W_{1}
and
τ
b
\tau_{b}
for each confidence score and model in DCF-Vul.
Similar to the DCF-Bug, we find that fine-grained confidence scores are better separated than sequence-level confidence scores, with minimum token probability as the top performer (EP-
W
1
W_{1}
: 0.04-0.18, CP-
W
1
W_{1}
: 0.02-0.08).
The sequence-level confidence scores have a separation of 0.00-0.02 for the majority of models against both correctness metrics.
In terms of rank correlation for both correctness metrics, we still find that minimum token probability is consistently the top performer (EP-
τ
b
\tau_{b}
: 0.08-0.31, CP-
τ
b
\tau_{b}
: 0.00-0.18), whilst lowest-
K
K
token probability and attention-weighted uncertainty can equal or outperform the sequence-level confidence scores for 10 out of 14 models.
Again, the sequence-level confidence scores achieve near identical rank correlation (EP-
τ
b
\tau_{b}
: 0.04-0.27, CP-
τ
b
\tau_{b}
: 0.03-0.12), which are on average the worst performers.
Whilst these results suggest that fine-grained confidence scores are more amenable to Platt-scaling for DCF-Vul, all
W
1
W_{1}
and
τ
b
\tau_{b}
results are much weaker than found in DCF-Bug.
Therefore, it is expected that this task induces weaker calibration results for all confidence scores.
Figure 5:
DCF-Vul (Wasserstein Distance
W
1
W_{1}
)
Figure 6:
DCF-Vul (Kendall’s
τ
b
\tau_{b}
Coefficient)
Figures
7
and
8
†
†
footnotemark:
show the
W
1
W_{1}
and
τ
b
\tau_{b}
for each confidence score and model in CR-Trans.
Similar to the prior tasks, we find that fine-grained confidence scores are far better separated than sequence-level confidence scores.
In general, we find minimum token probability yields the widest separation (EM-
W
1
W_{1}
: 0.15-0.26, EP-
W
1
W_{1}
: 0.12-0.23), whilst sequence-level confidence scores again have a separation of only 0.01-0.03 for the majority of models against both correctness metrics.
In terms of rank correlation, we find an interesting phenomenon that contrasts behaviours found in DCF-Bug and DCF-Vul, where sequence-level confidence scores are consistently the top performers (EM-
τ
b
\tau_{b}
: 0.32-0.49, EP-
τ
b
\tau_{b}
: 0.31-0.45).
On the other hand, fine-grained confidence scores yield weaker correlations for this task (EM-
τ
b
\tau_{b}
: 0.25-0.48, EP-
τ
b
\tau_{b}
: 0.22-0.39).
This behaviour can be explained by the fundamental difference in solution space between CR-Trans and the two prior tasks.
In short, DCF-Bug and DCF-Vul are both expecting code revisions to address explicit static analysis warnings that have narrow solutions spaces (e.g.,
Cookie has the Secure attribute set to false. Set it to true to protect the cookie from man-in-the-middle attacks.
), whilst CR-Trans expects code revisions to address human-written reviews that allow for wider solution spaces (e.g.,
We’ll have to think about a unified system for integrating regularization as part of the loss
).
Therefore, lower token probabilities in CR-Trans can be a result of multiple correct alternative code edits sharing the model’s solution space (aleatoric uncertainty), rather than the model truly being unaware of the correct code edit (epistemic uncertainty)
[
23
]
.
This weakens lower token probabilities’ correlations with correctness.
Nevertheless, we do not expect sequence-level confidence scores to be more amenable to Platt-scaling for CR-Trans.
Since
W
1
W_{1}
for sequence-level measures are still extremely low, the calibrator will be required to learn an unstable
w
w
that conflicts with standard regularisation.
Ultimately, given the substantially stronger
W
1
W_{1}
results for fine-grained confidence scores, alongside
τ
b
\tau_{b}
results that remain comparable, we still expect these methods to yield more accurate confidence calibration overall.
Figure 7:
CR-Trans (Wasserstein Distance
W
1
W_{1}
)
Figure 8:
CR-Trans (Kendall’s
τ
b
\tau_{b}
Coefficient)
Key Finding II:
Preliminary analysis of
W
1
W_{1}
and
τ
b
\tau_{b}
suggest that fine-grained confidence scores generally induce stronger separation and ranking of correct and incorrect code revisions compared to sequence-level scores, making them more amenable to Platt-scaling for ACR tasks.
TABLE II:
Global Platt-Scaling Results for DCF-Bug in Terms of Exact Match and Edit Progress
EM
EP
sl_norm
avg
min
low-K
attn-
ω
\omega
sl_norm
avg
min
low-K
attn-
ω
\omega
Model
Size
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
8B
0.11
0.21
3
0.03
0.21
2
0.05
0.16
9
0.06
0.18
7
0.04
0.18
7
0.07
0.23
3
0.06
0.23
2
0.08
0.21
8
0.08
0.21
7
0.08
0.22
7
Llama-3.1
70B
0.11
0.21
3
0.12
0.22
2
0.04
0.18
8
0.04
0.18
7
0.04
0.18
7
0.12
0.22
2
0.10
0.23
2
0.04
0.20
7
0.04
0.21
6
0.04
0.21
6
7B
-
-
1
-
-
1
0.04
0.19
8
0.06
0.21
5
0.04
0.20
6
0.05
0.24
2
-
-
1
0.04
0.22
7
0.03
0.23
6
0.03
0.23
6
CodeLlama
70B
0.03
0.24
2
-
-
1
0.04
0.20
8
0.08
0.21
7
0.08
0.21
7
-
-
1
-
-
1
0.05
0.18
6
0.06
0.19
5
0.06
0.19
5
7B
0.05
0.19
2
0.04
0.19
2
0.06
0.15
7
0.06
0.16
6
0.05
0.16
6
0.08
0.24
2
0.10
0.24
2
0.04
0.21
7
0.09
0.22
6
0.07
0.23
6
Qwen2.5
72B
0.04
0.20
2
0.04
0.20
2
0.06
0.16
7
0.06
0.17
6
0.06
0.17
6
0.04
0.24
2
0.03
0.24
2
0.08
0.21
8
0.06
0.21
7
0.06
0.21
7
7B
0.07
0.19
2
0.07
0.20
2
0.06
0.14
9
0.06
0.16
7
0.03
0.16
7
0.10
0.24
3
0.11
0.24
2
0.07
0.21
8
0.09
0.23
8
0.10
0.24
7
Qwen2.5-Coder
32B
0.02
0.21
2
0.02
0.22
2
0.05
0.18
8
0.04
0.19
6
0.04
0.19
6
0.04
0.24
2
0.04
0.24
2
0.06
0.22
7
0.04
0.22
7
0.04
0.22
7
7B
0.05
0.12
3
0.05
0.12
3
0.04
0.11
5
0.05
0.11
5
0.04
0.11
4
0.06
0.22
4
0.03
0.22
3
0.06
0.21
8
0.08
0.22
7
0.06
0.22
6
DS-LLM
67B
0.06
0.23
2
0.09
0.23
2
0.07
0.19
8
0.07
0.21
6
0.07
0.21
6
0.07
0.22
2
0.08
0.23
2
0.07
0.20
7
0.08
0.21
5
0.08
0.21
5
7B
0.04
0.21
2
-
-
1
0.07
0.17
8
0.07
0.18
6
0.07
0.18
6
0.06
0.24
2
-
-
1
0.06
0.20
9
0.06
0.20
7
0.07
0.21
7
DS-Coder
33B
0.05
0.23
2
0.04
0.23
2
0.04
0.18
8
0.08
0.18
7
0.08
0.19
7
0.05
0.23
2
-
-
1
0.05
0.18
7
0.06
0.20
6
0.07
0.20
6
DS-V2
16B
-
-
1
-
-
1
0.07
0.14
7
0.07
0.14
5
0.06
0.15
4
0.04
0.23
2
0.04
0.23
2
0.08
0.22
8
0.07
0.23
6
0.05
0.22
5
DS-Coder-V2
16B
-
-
1
-
-
1
0.04
0.18
7
0.06
0.19
6
0.08
0.19
6
-
-
1
-
-
1
0.04
0.22
6
0.10
0.23
6
0.09
0.23
6
sl_norm
:
Normalised Sequence Likelihood
avg
:
Average Token Probability,
min
:
Minimum Token Probability,
low-K
:
Lowest-
K
K
Token Probability
attn-
ω
\omega
:
Attention-Weighted Uncertainty
EM:
Exact Match,
EP:
Edit Progress,
ECE:
Expected Calibration Error (↓),
𝓑
\boldsymbol{\mathcal{B}}
:
Brier Score (↓),
BC:
Bin Coverage (↑),
Bold Number:
Best Result for that Model and Correctness Measure
TABLE III:
Global Platt-Scaling Results for DCF-Vul in Terms of Edit Progress and Checks Passed
EP
CP
sl_norm
avg
min
low-K
attn-
ω
\omega
sl_norm
avg
min
low-K
attn-
ω
\omega
Model
Size
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
8B
0.04
0.20
2
0.02
0.20
2
0.02
0.19
7
0.02
0.20
4
0.02
0.20
4
0.04
0.24
2
-
-
1
0.06
0.23
5
0.04
0.24
4
-
-
1
Llama-3.1
70B
0.03
0.21
2
0.03
0.21
2
0.05
0.19
6
0.05
0.20
5
0.05
0.20
5
-
-
1
-
-
1
0.05
0.19
3
-
-
1
-
-
1
7B
0.02
0.19
2
-
-
1
0.03
0.19
3
0.02
0.19
3
0.01
0.19
3
0.03
0.24
2
0.03
0.24
2
0.04
0.24
3
0.02
0.24
4
0.03
0.24
2
CodeLlama
70B
0.03
0.21
2
-
-
1
0.03
0.20
2
0.03
0.20
3
0.03
0.20
3
-
-
1
-
-
1
-
-
1
0.08
0.25
2
0.08
0.25
2
7B
-
-
1
-
-
1
0.03
0.13
4
0.02
0.14
4
0.03
0.14
4
-
-
1
-
-
1
0.04
0.23
3
0.05
0.23
3
0.03
0.23
3
Qwen2.5
72B
0.10
0.13
2
0.11
0.13
2
0.02
0.12
4
0.02
0.12
5
0.02
0.12
5
-
-
1
-
-
1
0.05
0.21
3
0.04
0.21
2
0.04
0.21
2
7B
0.06
0.16
2
0.05
0.16
2
0.05
0.13
5
0.04
0.15
4
0.04
0.15
4
0.05
0.23
2
0.05
0.23
2
0.07
0.22
2
0.05
0.22
2
-
-
1
Qwen2.5-Coder
32B
0.06
0.16
2
0.05
0.16
2
0.02
0.14
5
0.02
0.15
5
0.02
0.15
5
-
-
1
-
-
1
0.05
0.22
2
0.05
0.22
2
-
-
1
7B
-
-
1
-
-
1
0.01
0.12
4
0.02
0.12
3
0.02
0.13
3
0.02
0.24
3
-
-
1
-
-
1
0.03
0.25
3
-
-
1
DS-LLM
67B
-
-
1
-
-
1
0.04
0.20
4
0.02
0.20
3
0.02
0.20
3
-
-
1
-
-
1
0.04
0.25
2
0.06
0.25
2
0.06
0.25
2
7B
0.06
0.19
2
-
-
1
0.04
0.17
7
0.03
0.18
4
0.03
0.19
5
0.01
0.24
2
-
-
1
0.03
0.23
4
0.03
0.23
2
0.01
0.23
2
DS-Coder
33B
-
-
1
-
-
1
0.06
0.19
6
0.04
0.20
4
0.05
0.20
4
-
-
1
-
-
1
0.03
0.23
3
0.03
0.23
3
0.03
0.23
3
DS-V2
16B
-
-
1
-
-
1
0.03
0.15
4
0.03
0.15
3
0.03
0.15
3
0.02
0.25
2
0.02
0.25
2
0.03
0.25
2
0.02
0.25
2
0.01
0.25
3
DS-Coder-V2
16B
0.06
0.18
2
0.08
0.18
2
0.04
0.16
5
0.04
0.17
4
0.05
0.17
4
-
-
1
-
-
1
0.04
0.24
4
0.03
0.24
3
0.05
0.25
2
sl_norm
:
Normalised Sequence Likelihood
avg
:
Average Token Probability,
min
:
Minimum Token Probability,
low-K
:
Lowest-
K
K
Token Probability
attn-
ω
\omega
:
Attention-Weighted Uncertainty
EP:
Edit Progress,
CP:
Checks Passed,
ECE:
Expected Calibration Error (↓),
𝓑
\boldsymbol{\mathcal{B}}
:
Brier Score (↓),
BC:
Bin Coverage (↑),
Bold Number:
Best Result for that Model and Correctness Measure
TABLE IV:
Global Platt-Scaling Results for CR-Trans in Terms of Exact Match and Edit Progress
EM
EP
sl_norm
avg
min
low-K
attn-
ω
\omega
sl_norm
avg
min
low-K
attn-
ω
\omega
Model
Size
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
8B
0.22
0.27
2
0.23
0.27
2
0.16
0.20
6
0.17
0.22
4
0.17
0.23
4
0.23
0.27
3
0.24
0.28
2
0.17
0.23
7
0.18
0.24
6
0.18
0.24
5
Llama-3.1
70B
0.25
0.28
2
0.25
0.29
2
0.17
0.22
7
0.19
0.25
5
0.19
0.25
5
0.21
0.24
3
0.21
0.25
3
0.14
0.21
7
0.16
0.23
5
0.16
0.23
5
7B
-
-
1
-
-
1
0.19
0.23
6
0.21
0.25
4
0.21
0.25
4
0.29
0.31
2
0.29
0.31
2
0.25
0.27
5
0.26
0.29
4
0.26
0.29
4
CodeLlama
70B
0.31
0.33
2
0.31
0.34
2
0.21
0.25
7
0.25
0.29
5
0.25
0.29
5
0.31
0.29
2
0.32
0.30
2
0.26
0.25
5
0.28
0.27
4
0.28
0.27
4
7B
0.16
0.22
2
-
-
1
0.14
0.18
5
0.14
0.20
3
0.14
0.20
3
0.19
0.27
2
-
-
1
0.17
0.24
6
0.17
0.24
5
0.17
0.25
5
Qwen2.5
72B
0.26
0.30
2
0.26
0.30
2
0.19
0.21
6
0.20
0.24
5
0.20
0.24
5
0.26
0.25
2
0.26
0.26
2
0.20
0.20
7
0.21
0.22
6
0.21
0.22
6
7B
0.11
0.20
3
0.11
0.20
3
0.13
0.19
4
0.12
0.20
3
0.11
0.20
3
0.16
0.25
2
0.16
0.25
2
0.17
0.25
4
0.16
0.25
3
0.15
0.26
3
Qwen2.5-Coder
32B
0.23
0.26
2
-
-
1
0.14
0.18
6
0.15
0.22
4
0.15
0.22
4
0.26
0.27
2
0.27
0.27
2
0.16
0.20
7
0.17
0.22
5
0.17
0.22
5
7B
-
-
1
-
-
1
0.06
0.09
2
0.06
0.09
2
0.05
0.09
2
0.09
0.17
2
0.09
0.17
2
0.09
0.16
4
0.09
0.16
3
0.10
0.17
3
DS-LLM
67B
-
-
1
-
-
1
0.17
0.22
5
0.19
0.24
4
0.19
0.24
4
-
-
1
-
-
1
0.24
0.26
5
0.25
0.27
3
0.25
0.27
3
7B
-
-
1
-
-
1
0.19
0.21
6
0.19
0.23
4
0.19
0.23
4
0.26
0.28
2
0.26
0.29
2
0.21
0.24
7
0.21
0.25
5
0.21
0.25
5
DS-Coder
33B
0.23
0.29
2
-
-
1
0.17
0.22
7
0.19
0.25
5
0.19
0.25
5
0.28
0.29
2
0.28
0.29
2
0.22
0.24
6
0.23
0.25
4
0.23
0.25
4
DS-V2
16B
-
-
1
-
-
1
0.10
0.13
3
0.10
0.14
2
0.10
0.14
2
0.18
0.25
2
0.17
0.25
2
0.13
0.22
5
0.13
0.23
4
0.13
0.23
2
DS-Coder-V2
16B
-
-
1
-
-
1
0.14
0.20
5
0.16
0.22
3
0.15
0.22
3
-
-
1
-
-
1
0.18
0.25
5
0.19
0.26
4
0.19
0.27
3
sl_norm
:
Normalised Sequence Likelihood
avg
:
Average Token Probability,
min
:
Minimum Token Probability,
low-K
:
Lowest-
K
K
Token Probability
attn-
ω
\omega
:
Attention-Weighted Uncertainty
EM:
Exact Match,
EP:
Edit Progress,
ECE:
Expected Calibration Error (↓),
𝓑
\boldsymbol{\mathcal{B}}
:
Brier Score (↓),
BC:
Bin Coverage (↑),
Bold Number:
Best Result for that Model and Correctness Measure
RQ2. How effective is Platt scaling for ACR tasks when using fine-grained confidence scores?
The main calibration metrics are used to facilitate this analysis.
Specifically, we compare fine-grained and sequence-level confidence scores in terms of
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
after global Platt-scaling for each ACR task.
To platt-scale a confidence score, we train a single global calibrator with each task’s training set and selected measure of correctness.
This produces a separate calibrator for each combination of model, task, confidence score, and correctness metric.
The calibrators are then deployed for inference on their respective test sets for evaluation.
Overall, the consistent improvements from fine-grained confidence scores across all models, correctness metrics, and ACR tasks demonstrate that our hypothesis
(H1)
holds in practice.
Table
II
shows the
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
results after global Platt-scaling for DCF-Bug.
We find that sequence-level confidence scores exhibit the same phenomenon as found in past research
[
60
]
, where they are susceptible to single bin collapse.
In these cases, the calibrator was unable to learn an effective
w
w
and defaulted to a global average for the task.
For normalised sequence likelihood, we find that single bin collapse occurred for three models against
E
​
M
EM
, and two models against
E
​
P
EP
.
For average token probability, we find that single bin collapse occurred for five models against both
E
​
M
EM
and
E
​
P
EP
.
Whilst each sequence-level confidence score appear to attain the lowest
E
​
C
​
E
ECE
for five models, they were achieved at the expense of extremely low bin coverage (
B
​
C
BC
: 2-3).
Thus, indicating inability to support granular decision-making for DCF-Bug.
Sequence-level confidence scores also consistently exhibit the highest instance-level miscalibrations (
ℬ
\mathcal{B}
: 0.12-0.24).
In comparison, lowest-
K
K
token probability and attention-weighted uncertainty can achieve the lowest
E
​
C
​
E
ECE
for five models against
E
​
M
EM
and four models against
E
​
P
EP
, with reasonable bin coverage (
B
​
C
BC
: 4-8).
We find that attention-weighted uncertainty can outperform lowest-
K
K
token probability for six models against
E
​
M
EM
and four models against
E
​
P
EP
, but does not produce a meaningful difference for the rest of the cases.
Overall, we find that minimum token probability achieves the lowest calibration errors on average (
E
​
C
​
E
ECE
: 0.04-0.08,
ℬ
\mathcal{B}
: 0.11-0.22), whilst achieving the highest bin coverage (
B
​
C
BC
: 5-9).
Against both
E
​
M
EM
and
E
​
P
EP
, minimum token probability can achieve the lowest
E
​
C
​
E
ECE
for five models and the lowest
ℬ
\mathcal{B}
for all models.
These results align with our analysis in RQ1, where the measure achieved the highest
W
1
W_{1}
and
τ
b
\tau_{b}
.
Thus, minimum token probability is the most optimal choice when considering
E
​
M
EM
and
E
​
P
EP
in DCF-Bug, as it can provide the most accurate prediction for likelihood of correctness across the widest range of probability intervals.
Table
III
shows the
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
results after global Platt-scaling for DCF-Vul.
In line with the low
W
1
W_{1}
and
τ
b
\tau_{b}
results from RQ1, all confidence scores exhibit worse calibration performance compared to DCF-Bug.
For sequence-level confidence scores, the single bin collapse issue is more severe in DCF-Vul.
Normalised sequence likelihood is completely degenerate for five models against
E
​
P
EP
and eight models against
C
​
P
CP
, whilst average token probability is completely degenerate for eight models against
E
​
P
EP
, and 11 models against
C
​
P
CP
.
For the remaining cases, sequence-level confidence scores still achieve extremely low bin coverage (
B
​
C
BC
: 2-3), indicating an inability to support granular decision-making for DCF-Vul.
For
E
​
P
EP
, lowest-
K
K
token probability and attention-weighted uncertainty produce similar calibration errors (
E
​
C
​
E
ECE
: 0.02-0.05,
ℬ
\mathcal{B}
: 0.12-0.20), achieving the lowest
E
​
C
​
E
ECE
for 11 and nine models, respectively.
However, their bin coverage is generally low (
B
​
C
BC
: 2-5).
Against
E
​
P
EP
, minimum token probability achieves slightly lower calibration error than other fine-grained confidence scores (
E
​
C
​
E
ECE
: 0.01-0.05,
ℬ
\mathcal{B}
: 0.12-0.20) with higher bin coverage (
B
​
C
BC
: 2-7).
This results in the lowest
E
​
C
​
E
ECE
for seven models and lowest
ℬ
\mathcal{B}
for all models.
Against
C
​
P
CP
, minimum token probability, lowest-
K
K
token probability, and attention-weighted uncertainty all achieve similar calibration error (
E
​
C
​
E
ECE
: 0.01-0.08,
ℬ
\mathcal{B}
: 0.19-0.25), producing the lowest
E
​
C
​
E
ECE
for four, eight and six models, respectively.
In general, the bin coverage against
C
​
P
CP
was lower (
B
​
C
BC
: 2-5).
Against
C
​
P
CP
, single bin collapse also occurred with fine-grained confidence scores, albeit to a far lesser extent, affecting two, one, and five models, respectively.
Similar to prior results, minimum token probability is the most optimal choice when considering
E
​
P
EP
and
C
​
P
CP
in DCF-Vul, since it still achieves the lowest calibration error for the widest bin coverage.
Table
IV
shows the
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
results after global Platt-scaling for CR-Trans.
Whilst fine-grained confidence scores can provide improved calibration results over sequence-level confidence scores, they struggled to achieve below 0.14
E
​
C
​
E
ECE
.
This indicates that global Platt-scaling is insufficient for supporting decision-making in CR-Trans.
Against
E
​
M
EM
, single bin collapse occurred for six models using normalised sequence likelihood and nine models using average token probability.
For the remaining cases, they exhibited the highest calibration error (
E
​
C
​
E
ECE
: 0.11-0.31,
ℬ
\mathcal{B}
: 0.20-0.34), whilst covering the lowest amount of bins (
B
​
C
BC
: 2-3).
These results reflect our
W
1
W_{1}
findings in RQ1.
We find that attention-weighted uncertainty can outperform lowest-
K
K
token probability for three models, but achieve identical results for the rest of the cases (
E
​
C
​
E
ECE
: 0.05-0.25,
ℬ
\mathcal{B}
: 0.09-0.29).
Similar to prior tasks, minimum token probability generally yields the lowest calibration errors (
E
​
C
​
E
ECE
: 0.06-0.21 ,
ℬ
\mathcal{B}
: 0.09-0.25) with the highest bin coverage (
B
​
C
BC
: 2-7).
Against
E
​
P
EP
, single bin collapse occurred for two models using normalised sequence likelihood and three models using average token probability.
For the remaining cases, they still exhibited the highest calibration error (
E
​
C
​
E
ECE
: 0.09-0.32,
ℬ
\mathcal{B}
: 0.17-0.31), whilst covering the lowest amount of bins (
B
​
C
BC
: 2-3).
Against
E
​
P
EP
, lowest-
K
K
token probability and attention-weighted uncertainty also achieved near identical results (
E
​
C
​
E
ECE
: 0.09-0.28,
ℬ
\mathcal{B}
: 0.16-0.29).
Similar to prior results, minimum token probability generally achieves the lowest calibration error (
E
​
C
​
E
ECE
: 0.09-0.26,
ℬ
\mathcal{B}
: 0.16-0.27), with the highest bin coverage (
B
​
C
BC
: 4-7).
Although fine-grained confidence scores can improve global Platt-scaling for CR-Trans, the extent of miscalibration is still unfit for facilitating accurate decision-making.
Key Finding III:
The results from global Platt-scaling demonstrate that fine-grained confidence scores consistently produce lower calibration error over a wider range of probability intervals compared to sequence-level scores.
In particular, minimum token probability yields the top performance across
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
for all ACR tasks.
RQ3. To what extent can local Platt-scaling improve over conventional Platt-scaling in ACR tasks?
The main calibration metrics are used to facilitate this analysis.
Based on prior results, we find that global Platt-scaling is generally sufficient for achieving low calibration error in DCF-Bug and DCF-Vul (best calibration results
≤
\leq
0.08
E
​
C
​
E
ECE
), yet falls short for CR-Trans (best calibration results generally
≥
\geq
0.14
E
​
C
​
E
ECE
).
This discrepancy suggests that CR-Trans exhibits higher error heterogeneity, presenting a significant opportunity for local Platt-scaling to further improve confidence calibration.
In contrast, the two former tasks offer only marginal opportunities for further calibration gains.
We apply local Platt-scaling to each scenario, training a separate set of clusters and calibrators for each combination of model, confidence score, correctness metric, and ACR task, before evaluating on their respective test sets.
Overall, the consistent improvements from local Platt-scaling across all combinations of settings demonstrate that our hypothesis
(H2)
holds in practice.
TABLE V:
Local Platt-Scaling Results for DCF-Bug in Terms of Exact Match and Edit Progress
EM
EP
min
low-K
attn-
ω
\omega
min
low-K
attn-
ω
\omega
Model
Size
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
8B
0.03 (-0.02)
0.15 (-0.01)
9 (=0)
0.03 (-0.03)
0.18 (=0)
7 (=0)
0.03 (-0.01)
0.18 (=0)
7 (=0)
0.06 (-0.02)
0.20 (-0.01)
9 (+1)
0.05 (-0.03)
0.21 (=0)
8 (+1)
0.06 (-0.02)
0.22 (=0)
9 (+2)
Llama-3.1
70B
0.03 (-0.01)
0.17 (-0.01)
8 (=0)
0.04 (=0)
0.18 (=0)
7 (=0)
0.04 (=0)
0.18 (=0)
7 (=0)
0.03 (-0.01)
0.20 (=0)
8 (+1)
0.04 (=0)
0.21 (=0)
6 (=0)
0.04 (=0)
0.21 (=0)
6 (=0)
7B
0.02 (-0.02)
0.19 (=0)
8 (=0)
0.03 (-0.03)
0.21 (=0)
5 (=0)
0.02 (-0.02)
0.20 (=0)
6 (=0)
0.03 (-0.01)
0.22 (=0)
7 (=0)
0.03 (=0)
0.23 (=0)
6 (=0)
0.03 (=0)
0.23 (=0)
6 (=0)
CodeLlama
70B
0.04 (=0)
0.20 (=0)
8 (=0)
0.07 (-0.01)
0.20 (-0.01)
7 (=0)
0.07 (-0.01)
0.20 (-0.01)
7 (=0)
0.04 (-0.01)
0.18 (=0)
7 (+1)
0.06 (=0)
0.19 (=0)
5 (=0)
0.06 (=0)
0.19 (=0)
5 (=0)
7B
0.04 (-0.02)
0.15 (=0)
7 (=0)
0.05 (-0.01)
0.16 (=0)
6 (=0)
0.04 (-0.01)
0.16 (=0)
6 (=0)
0.05 (+0.01)
0.21 (=0)
9 (+2)
0.05 (-0.04)
0.22 (=0)
6 (=0)
0.04 (-0.03)
0.23 (=0)
7 (+1)
Qwen2.5
72B
0.04 (-0.02)
0.16 (=0)
7 (=0)
0.06 (=0)
0.16 (-0.01)
6 (=0)
0.06 (=0)
0.16 (-0.01)
6 (=0)
0.03 (-0.05)
0.21 (=0)
8 (=0)
0.05 (-0.01)
0.21 (=0)
8 (+1)
0.05 (-0.01)
0.21 (=0)
8 (+1)
7B
0.04 (-0.02)
0.14 (=0)
9 (=0)
0.05 (-0.01)
0.15 (-0.01)
7 (=0)
0.03 (=0)
0.16 (=0)
7 (=0)
0.05 (-0.02)
0.21 (=0)
9 (+1)
0.08 (-0.01)
0.22 (-0.01)
8 (=0)
0.10 (=0)
0.24 (=0)
7 (=0)
Qwen2.5-Coder
32B
0.03 (-0.02)
0.17 (-0.01)
8 (=0)
0.04 (=0)
0.17 (-0.02)
8 (+2)
0.04 (=0)
0.17 (-0.02)
8 (+2)
0.03 (-0.03)
0.20 (-0.02)
8 (+1)
0.04 (=0)
0.21 (-0.01)
7 (=0)
0.04 (=0)
0.21 (-0.01)
8 (+1)
7B
0.02 (-0.02)
0.10 (-0.01)
5 (=0)
0.02 (-0.03)
0.11 (=0)
4 (+1)
0.02 (-0.02)
0.11 (=0)
4 (=0)
0.04 (-0.02)
0.21 (=0)
8 (=0)
0.05 (-0.03)
0.22 (=0)
7 (=0)
0.06 (=0)
0.22 (=0)
6 (=0)
DS-LLM
67B
0.05 (-0.02)
0.19 (=0)
8 (=0)
0.07 (=0)
0.20 (-0.01)
6 (=0)
0.07 (=0)
0.20 (-0.01)
6 (=0)
0.03 (-0.04)
0.19 (-0.01)
7 (=0)
0.06 (-0.02)
0.21 (=0)
6 (+1)
0.06 (-0.02)
0.21 (=0)
6 (+1)
7B
0.03 (-0.04)
0.17 (=0)
8 (=0)
0.06 (-0.01)
0.17 (-0.01)
6 (=0)
0.06 (-0.01)
0.17 (-0.01)
7 (+1)
0.04 (-0.02)
0.20 (=0)
9 (=0)
0.06 (=0)
0.20 (=0)
7 (=0)
0.07 (=0)
0.21 (=0)
7 (=0)
DS-Coder
33B
0.04 (=0)
0.17 (-0.01)
8 (=0)
0.06 (-0.02)
0.18 (=0)
7 (=0)
0.05 (-0.03)
0.18 (-0.01)
7 (=0)
0.03 (-0.02)
0.18 (=0)
8 (+1)
0.04 (-0.02)
0.20 (=0)
7 (+1)
0.04 (-0.03)
0.20 (=0)
7 (+1)
DS-V2
16B
0.03 (-0.04)
0.13 (-0.01)
6 (-1)
0.05 (-0.02)
0.13 (-0.01)
5 (=0)
0.06 (=0)
0.13 (-0.02)
5 (+1)
0.05 (-0.03)
0.22 (=0)
8 (=0)
0.04 (-0.03)
0.22 (-0.01)
6 (=0)
0.04 (-0.01)
0.22 (=0)
6 (+1)
DS-Coder-V2
16B
0.03 (-0.01)
0.17 (-0.01)
7 (=0)
0.04 (-0.02)
0.19 (=0)
6 (=0)
0.04 (-0.04)
0.18 (-0.01)
8 (+2)
0.04 (=0)
0.22 (=0)
6 (=0)
0.03 (-0.07)
0.22 (-0.01)
6 (=0)
0.04 (-0.05)
0.22 (-0.01)
6 (=0)
min
:
Minimum Token Probability,
low-K
:
Lowest-
K
K
Token Probability
attn-
ω
\omega
:
Attention-Weighted Uncertainty,
EM:
Exact Match,
EP:
Edit Progress,
ECE:
Expected Calibration Error (↓),
𝓑
\boldsymbol{\mathcal{B}}
:
Brier Score (↓),
BC:
Bin Coverage (↑)
Bold Number:
Best Result for that Model and Correctness Measure,
(+/-/=):
Difference from Global Platt-Scaling
TABLE VI:
Local Platt-Scaling Results for DCF-Vul in Terms of Edit Progress and Checks Passed
EP
CP
min
low-K
attn-
ω
\omega
min
low-K
attn-
ω
\omega
Model
Size
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
8B
0.02 (=0)
0.19 (=0)
7 (=0)
0.02 (=0)
0.20 (=0)
4 (=0)
0.02 (=0)
0.20 (=0)
5 (+1)
0.03 (-0.03)
0.23 (=0)
5 (=0)
0.03 (-0.01)
0.24 (=0)
4 (=0)
0.02
0.24
3 (+2)
Llama-3.1
70B
0.05 (=0)
0.19 (=0)
6 (=0)
0.05 (=0)
0.20 (=0)
5 (=0)
0.05 (=0)
0.20 (=0)
5 (=0)
0.04 (-0.01)
0.19 (=0)
3 (=0)
0.05
0.20
3 (+2)
0.05
0.20
3 (+2)
7B
0.03 (=0)
0.19 (=0)
3 (=0)
0.03 (=0)
0.19 (=0)
3 (=0)
0.01 (=0)
0.19 (=0)
3 (=0)
0.03 (-0.01)
0.24 (=0)
3 (=0)
0.02 (=0)
0.24 (=0)
4 (=0)
0.03 (=0)
0.24 (=0)
2 (=0)
CodeLlama
70B
0.02 (-0.01)
0.20 (=0)
3 (+1)
0.03 (=0)
0.20 (=0)
4 (+1)
0.03 (=0)
0.20 (=0)
4 (+1)
0.05
0.23
6 (+5)
0.05 (-0.03)
0.24 (-0.01)
2 (=0)
0.05 (-0.03)
0.24 (-0.01)
2 (=0)
7B
0.03 (=0)
0.13 (=0)
4 (=0)
0.02 (-0.01)
0.14 (=0)
4 (=0)
0.03 (=0)
0.14 (=0)
4 (=0)
0.04 (=0)
0.22 (-0.01)
6 (+3)
0.04 (-0.01)
0.22 (-0.01)
6 (+3)
0.03 (=0)
0.22 (-0.01)
6 (+3)
Qwen2.5
72B
0.02 (=0)
0.12 (=0)
5 (+1)
0.02 (=0)
0.12 (=0)
5 (=0)
0.02 (=0)
0.12 (=0)
5 (=0)
0.03 (-0.02)
0.20 (-0.01)
5 (+2)
0.03 (-0.01)
0.20 (-0.01)
5 (+3)
0.03 (-0.01)
0.20 (-0.01)
5 (+3)
7B
0.04 (-0.01)
0.13 (=0)
5 (=0)
0.04 (-0.01)
0.15 (=0)
4 (=0)
0.04 (=0)
0.15 (=0)
4 (=0)
0.07 (=0)
0.21 (-0.01)
4 (+2)
0.05 (=0)
0.21 (-0.01)
4 (+2)
0.06
0.22
7 (+6)
Qwen2.5-Coder
32B
0.02 (=0)
0.14 (=0)
5 (=0)
0.02 (=0)
0.15 (=0)
5 (=0)
0.02 (=0)
0.15 (=0)
5 (=0)
0.03 (-0.02)
0.20 (-0.02)
6 (+4)
0.03 (-0.02)
0.21 (-0.01)
3 (+1)
0.02
0.21
3 (+2)
7B
0.01 (=0)
0.12 (=0)
4 (=0)
0.01 (=0)
0.12 (=0)
4 (+1)
0.02 (=0)
0.12 (-0.01)
3 (=0)
0.03
0.24
5 (+4)
0.03 (=0)
0.24 (-0.01)
5 (+2)
0.02
0.24
5 (+4)
DS-LLM
67B
0.03 (-0.01)
0.20 (=0)
4 (=0)
0.04 (=0)
0.20 (=0)
3 (=0)
0.02 (=0)
0.20 (=0)
3 (=0)
0.02 (-0.02)
0.25 (=0)
2 (=0)
0.02 (-0.04)
0.25 (=0)
2 (=0)
0.02 (-0.04)
0.25 (=0)
2 (=0)
7B
0.04 (=0)
0.17 (=0)
7 (=0)
0.03 (-0.01)
0.19 (+0.01)
5 (+1)
0.03 (=0)
0.19 (=0)
5 (=0)
0.03 (=0)
0.23 (=0)
4 (=0)
0.03 (=0)
0.23 (=0)
5 (+3)
0.03 (+0.02)
0.23 (=0)
5 (+3)
DS-Coder
33B
0.05 (-0.01)
0.19 (=0)
6 (=0)
0.05 (-0.01)
0.20 (=0)
4 (=0)
0.05 (=0)
0.20 (=0)
4 (=0)
0.03 (=0)
0.22 (-0.01)
5 (+2)
0.01 (-0.02)
0.22 (-0.01)
5 (+2)
0.03 (=0)
0.22 (-0.01)
5 (+2)
DS-V2
16B
0.02 (-0.01)
0.15 (=0)
4 (=0)
0.03 (=0)
0.15 (=0)
4 (+1)
0.03 (=0)
0.15 (=0)
3 (=0)
0.03 (=0)
0.24 (-0.01)
3 (+1)
0.02 (=0)
0.24 (-0.01)
3 (+1)
0.03 (+0.02)
0.24 (-0.01)
4 (+1)
DS-Coder-V2
16B
0.04 (=0)
0.16 (=0)
5 (=0)
0.04 (=0)
0.17 (=0)
5 (+1)
0.05 (=0)
0.17 (=0)
5 (+1)
0.02 (-0.02)
0.23 (-0.01)
5 (+1)
0.02 (-0.01)
0.24 (=0)
4 (+1)
0.03 (-0.02)
0.24 (-0.01)
5 (+3)
min
:
Minimum Token Probability,
low-K
:
Lowest-
K
K
Token Probability
attn-
ω
\omega
:
Attention-Weighted Uncertainty,
EM:
Exact Match,
EP:
Edit Progress,
ECE:
Expected Calibration Error (↓),
𝓑
\boldsymbol{\mathcal{B}}
:
Brier Score (↓),
BC:
Bin Coverage (↑)
Bold Number:
Best Result for that Model and Correctness Measure,
(+/-/=):
Difference from Global Platt-Scaling
TABLE VII:
Local Platt-Scaling Results for CR-Trans in Terms of Exact Match and Edit Progress
EM
EP
min
low-K
attn-
ω
\omega
min
low-K
attn-
ω
\omega
Model
Size
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
ECE
𝓑
\boldsymbol{\mathcal{B}}
BC
8B
0.13 (-0.03)
0.20 (=0)
9 (+3)
0.18 (-0.01)
0.22 (=0)
4 (=0)
0.17 (=0)
0.23 (=0)
4 (=0)
0.07 (-0.10)
0.22 (-0.01)
9 (+2)
0.11 (-0.07)
0.23 (-0.01)
8 (+2)
0.18 (=0)
0.24 (=0)
5 (=0)
Llama-3.1
70B
0.08 (-0.09)
0.22 (=0)
9 (+2)
0.19 (=0)
0.25 (=0)
5 (=0)
0.19 (=0)
0.25 (=0)
5 (=0)
0.09 (-0.05)
0.20 (-0.01)
8 (+1)
0.08 (-0.08)
0.21 (-0.02)
7 (+2)
0.16 (=0)
0.23 (=0)
5 (=0)
7B
0.12 (-0.07)
0.22 (-0.01)
8 (+2)
0.21 (=0)
0.25 (=0)
4 (=0)
0.21 (=0)
0.25 (=0)
4 (=0)
0.10 (-0.15)
0.22 (-0.05)
7 (+2)
0.18 (-0.08)
0.25 (-0.04)
7 (+3)
0.26 (=0)
0.29 (=0)
4 (=0)
CodeLlama
70B
0.10 (-0.11)
0.22 (-0.03)
8 (+1)
0.23 (+0.02)
0.28 (-0.01)
8 (+3)
0.25 (=0)
0.29 (=0)
5 (=0)
0.18 (-0.08)
0.22 (-0.03)
7 (+2)
0.12 (-0.16)
0.21 (-0.06)
8 (+4)
0.28 (=0)
0.27 (=0)
4 (=0)
7B
0.13 (-0.01)
0.18 (=0)
8 (+3)
0.14 (=0)
0.20 (=0)
3 (=0)
0.14 (=0)
0.20 (=0)
3 (=0)
0.07 (-0.10)
0.23 (-0.01)
8 (+2)
0.16 (-0.01)
0.24 (=0)
7 (+2)
0.17 (=0)
0.25 (=0)
5 (=0)
Qwen2.5
72B
0.12 (-0.07)
0.21 (=0)
10 (+4)
0.20 (=0)
0.24 (=0)
5 (=0)
0.20 (=0)
0.24 (=0)
5 (=0)
0.08 (-0.12)
0.17 (-0.03)
8 (+1)
0.14 (-0.07)
0.20 (-0.02)
6 (=0)
0.21 (=0)
0.22 (=0)
6 (=0)
7B
0.06 (-0.07)
0.18 (-0.01)
6 (+2)
0.10 (-0.02)
0.20 (=0)
3 (=0)
0.10 (-0.01)
0.20 (=0)
3 (=0)
0.11 (-0.06)
0.24 (-0.01)
6 (+2)
0.09 (-0.07)
0.24 (-0.01)
7 (+4)
0.14 (-0.01)
0.25 (-0.01)
3 (=0)
Qwen2.5-Coder
32B
0.11 (-0.03)
0.19 (-0.01)
10 (+4)
0.15 (=0)
0.22 (=0)
4 (=0)
0.15 (=0)
0.22 (=0)
4 (=0)
0.09 (-0.07)
0.19 (-0.01)
8 (+1)
0.14 (-0.03)
0.22 (=0)
8 (+3)
0.17 (=0)
0.22 (=0)
5 (=0)
7B
0.10 (+0.04)
0.10 (+0.01)
6 (+4)
0.06 (=0)
0.09 (=0)
2 (=0)
0.05 (=0)
0.09 (=0)
2 (=0)
0.06 (-0.03)
0.16 (=0)
7 (+3)
0.09 (=0)
0.16 (=0)
4 (+1)
0.08 (-0.02)
0.17 (=0)
3 (=0)
DS-LLM
67B
0.15 (-0.02)
0.22 (=0)
10 (+5)
0.18(-0.01)
0.24 (=0)
4 (=0)
0.18 (-0.01)
0.24 (=0)
4 (=0)
0.08 (-0.16)
0.21 (-0.05)
8 (+3)
0.15 (-0.10)
0.24 (-0.03)
7 (+4)
0.25 (=0)
0.27 (=0)
3 (=0)
7B
0.16 (-0.03)
0.21 (=0)
7 (+1)
0.19 (=0)
0.23 (=0)
4 (=0)
0.19 (=0)
0.23 (=0)
4 (=0)
0.08 (-0.13)
0.21 (-0.03)
9 (+2)
0.14 (-0.07)
0.24 (-0.01)
8 (+3)
0.21 (=0)
0.25 (=0)
5 (=0)
DS-Coder
33B
0.11 (-0.06)
0.22 (=0)
10 (+3)
0.19 (=0)
0.25 (-0.02)
5 (=0)
0.19 (=0)
0.25 (=0)
5 (=0)
0.13 (-0.09)
0.21 (-0.03)
8 (+2)
0.11 (-0.12)
0.21 (-0.04)
7 (+3)
0.24 (-0.01)
0.25 (=0)
4 (=0)
DS-V2
16B
0.10 (=0)
0.13 (=0)
3 (=0)
0.10 (=0)
0.14 (=0)
2 (=0)
0.10 (=0)
0.14 (=0)
2 (=0)
0.13 (=0)
0.22 (=0)
5 (=0)
0.13 (=0)
0.23 (=0)
4 (=0)
0.13 (=0)
0.23 (=0)
2 (=0)
DS-Coder-V2
16B
0.14 (=0)
0.20 (=0)
5 (=0)
0.16 (=0)
0.22 (=0)
3 (=0)
0.15 (=0)
0.22 (=0)
3 (=0)
0.18 (=0)
0.25 (=0)
5 (=0)
0.19 (=0)
0.26 (=0)
4 (=0)
0.19 (=0)
0.27 (=0)
4 (+1)
min
:
Minimum Token Probability,
low-K
:
Lowest-
K
K
Token Probability
attn-
ω
\omega
:
Attention-Weighted Uncertainty,
EM:
Exact Match,
EP:
Edit Progress,
ECE:
Expected Calibration Error (↓),
𝓑
\boldsymbol{\mathcal{B}}
:
Brier Score (↓),
BC:
Bin Coverage (↑)
Bold Number:
Best Result for that Model and Correctness Measure,
(+/-/=):
Difference from Global Platt-Scaling
Table
V
shows the
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
results after local Platt-scaling for DCF-Bug.
In general, we find that confidence calibration can be improved regardless of model, confidence score, or correctness metric.
Specifically, minimum token probability is the most amenable to local Platt-scaling, yielding reductions in
E
​
C
​
E
ECE
and
ℬ
\mathcal{B}
across the highest number of models.
This further solidifies its position as the best performing confidence score for both correctness metrics considered in DCF-Bug.
In terms of (
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
) against
E
​
M
EM
, (12, 7), (10, 7), and (8, 8) models experienced improvements for minimum token probability, lowest-
K
K
token probability, and attention-weighted uncertainty.
In terms of (
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
) against
E
​
P
EP
, (12, 3), (9, 4), and (7, 2) models experienced improvements, respectively.
In terms of bin coverage, the results show that local Platt-scaling can also induce higher
B
​
C
BC
for certain models.
These findings are most prevalent for
E
​
P
EP
, where seven, four, and seven models experienced increases in
B
​
C
BC
for minimum token probability, lowest-
K
K
token probability, and attention-weighted uncertainty, respectively.
Despite the favourable findings, we note that all calibration improvements are still marginal (
E
​
C
​
E
ECE
:
Δ
\Delta
0.01-0.07,
ℬ
\mathcal{B}
:
Δ
\Delta
0.01-0.02,
B
​
C
BC
:
Δ
\Delta
1-2).
These results suggest that while error heterogeneity exists for automated program repair, it is relatively modest.
Table
III
shows the
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
results after local Platt-scaling for DCF-Vul.
In general, we find that confidence calibration can be improved for the majority of models against
C
​
P
CP
, but is relatively ineffective against
E
​
P
EP
.
As in DCF-Bug, minimum token probability remains the most effective confidence score, owing to its strong baseline performance and amenability to local Platt-scaling.
In terms of (
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
) against
E
​
P
EP
, only (5, 0), (4, 0), and (0, 1) models experienced improvements for minimum token probability, lowest-
K
K
token probability, and attention-weighted uncertainty.
In contrast, for (
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
) against
C
​
P
CP
, (9, 9), (9, 9), and (9, 11) models experienced improvements, respectively.
These results suggest that error heterogeneity is largely confined against
E
​
P
EP
.
Interestingly, we find that the low bin coverage issue against
C
​
P
CP
can be greatly improved, where nine, 10, and 11 models experienced increases in
B
​
C
BC
for minimum token probability, lowest-
K
K
token probability, and attention-weighted uncertainty, respectively.
Despite persistent cases of bin collapse under global Platt-scaling for these fine-grained confidence scores, local Platt-scaling entirely mitigates the issue.
Overall, while the reduction in calibration error against
C
​
P
CP
is comparable to that of DCF-Bug (
E
​
C
​
E
ECE
:
Δ
\Delta
0.01-0.04,
ℬ
\mathcal{B}
:
Δ
\Delta
0.01-0.02), local Platt-scaling for DCF-Vul achieves a significantly greater increase in bin coverage (
B
​
C
BC
:
Δ
\Delta
1-6).
This suggests that errors in the task of vulnerability repair, as governed by security rules, exhibit greater variation.
Table
IV
shows the
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
results after local Platt-scaling for CR-Trans.
In general, this task yields the largest improvement in confidence calibration.
Specifically, local Platt-scaling is highly effective for minimum token probability against both
E
​
M
EM
and
E
​
P
EP
.
In terms of (
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
) against
E
​
M
EM
, (11, 4) models experienced improvements for minimum token probability, whilst only (3, 2) and (2, 0) models experienced improvements for lowest-
K
K
token probability and attention-weighted uncertainty.
In contrast, for (
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
) against
E
​
P
EP
, (12, 11) and (11, 9) models experienced improvements for minimum token probability and lowest-
K
K
token probability, whilst only (3, 2) models experienced improvements for attention-weighted uncertainty.
Under local Platt-scaling,
E
​
P
EP
is easier to calibrate than
E
​
M
EM
.
Using minimum token probability, nine models can achieve
≤
\leq
0.10
E
​
C
​
E
ECE
against
E
​
P
EP
, compared to only five against
E
​
M
EM
.
Additionally, using this confidence score can increase bin coverage for 12 models against both correctness metrics.
Compared to the prior tasks, CR-Trans exhibits higher error heterogeneity, much of which can be captured by local Platt-scaling (
E
​
C
​
E
ECE
:
Δ
\Delta
0.01-0.16,
ℬ
\mathcal{B}
:
Δ
\Delta
0.01-0.06,
B
​
C
BC
:
Δ
\Delta
1-5).
Overall, the results suggest that using minimum token probability with local Platt-scaling is necessary for facilitating accurate decision-making with generated code revisions in automated code refinement.
Key Finding IV:
Local Platt-scaling is highly effective in CR-Trans, and to a lesser extent in DCF-Bug and DCF-Vul.
Its congruence with minimum token probability consistently makes this combination the top-performing strategy.
Without it, calibration error cannot be reduced to a level sufficient for reliable decision-making in CR-Trans.
VII
Discussion
Although the results demonstrate the effectiveness of local Platt-scaling with fine-grained confidence scores, a more principled understanding is still needed, particularly regarding its role across the tasks, the underlying clustering dynamics, hyperparameter sensitivity, validation data requirements, and practical deployment.
This section facilitates this analysis.
Why is local Platt-scaling more essential for CR-Trans compared to DCF-Bug and DCF-Vul?
As established by the main results, CR-Trans suffers from much higher error heterogeneity, compared to DCF-Bug and DCF-Vul, resulting in the reliance on local Platt-scaling to achieve reasonable calibration error.
Figure
9
compares UMAP visualisations of Qwen3-Embedding-8B
representations of examples across each of the ACR Tasks.
Each example consists of an input concatenated with its corresponding code revision generated by CodeLlama-70B.
We find that examples in CR-Trans are not only highly varied within the training set, but also exhibit covariate shift when comparing between training and test sets.
Intuitively, automated code refinement has the potential to cover a much larger and unexpected variation of
C
p
​
r
​
e
C_{pre}
and
R
n
​
l
R_{nl}
due to the fact that code reviews are human oriented.
The requested code revisions may address a wide range of issues, spanning across both functional issues and evolvability concerns
[
39
]
, as well as any ad hoc issues in between.
This implies that not only is the data diverse in any collected calibration set, but it can also give rise to vastly different scenarios during deployment.
In contrast, the scope of both DCF-Bug and DCF-Vul is more limited than that of CR-Trans: DCF-Bug focuses specifically on bugs, while DCF-Vul targets vulnerabilities.
In contrast, CR-Trans can theoretically capture both types of issues as subpopulations, depending on the focus of the human reviewer.
Additionally, both DCF-Bug and DCF-Vul are based on fixed static analysis rules
V
n
​
l
V_{nl}
, which means the variability in
C
p
​
r
​
e
C_{pre}
is limited.
This implies that scenarios encountered during deployment will be relatively similar to those found in the training sets, meaning that there is limited opportunity for covariate shift.
In summary, the open-ended nature of automated code refinement induces a wider range of scenarios, increasing both variability and unpredictability of errors from the underlying LLM, thereby highlighting the need for local Platt-scaling with a backoff strategy.
Figure 9:
UMAP Visualisations of Qwen3-Embedding-8B Representations of Inputs w/ CodeLlama-70B Outputs
How many clusters does local Platt-scaling require to achieve optimal confidence calibration?
The Z-axis for the scatter plots in Figure
10
shows the number of clusters induced by local Platt-Scaling under the most optimal hyperparameters for the top performing confidence score i.e., minimum token probability.
Interestingly, we find that more clusters are required in DCF-Bug, despite previous findings of modest error heterogeneity compared to DCF-Vul and CR-Trans.
For both DCF-Bug and DCF-Vul, the number of induced clusters range from three to 13.
For DCF-Bug, seven clusters were most frequently induced, whereas for DCF-Vul, the most common number was four.
For CR-Trans, the number of induced clusters range from three to seven, with the most common number being five.
The fact that conventional Platt-scaling, based on a single global cluster, achieves low calibration error with high bin coverage on DCF-Bug suggests that errors induced by different clusters are sufficiently similar to be captured by a shared
σ
​
(
z
)
\sigma(z)
function.
For this task, local Platt-scaling is only able to marginally reduce calibration error by fitting many slightly different calibrators.
In contrast, CR-Trans exhibited high calibration error under conventional Platt-scaling, which indicates that errors for the task do not neatly lie on a shared
σ
​
(
z
)
\sigma(z)
function.
For this task, local Platt-scaling is able to significantly reduce calibration error by fitting a few highly disparate calibrators.
We expect this to also be the case for the few clusters induced in DCF-Vul, as local Platt-scaling is able to significantly increase bin coverage in the task.
Figure 10:
Optimal Hyperparameters for Local Platt-Scaling w/ Minimum Token Probability
To what extent do the optimal hyperparameters for local Platt-scaling vary?
The X-axis and Y-axis for the scatter plots in Figure
10
show the most optimal combination of hyperparameters for local Platt-scaling.
The former represents
minimum cluster size
, whilst the latter represents
minimum samples
.
The backoff strategy is denoted by the marker.
In general, we find that optimal hyperparameter combinations vary widely for DCF-Bug, minimally for DCF-Vul, and moderately for CR-Trans.
Whilst, there isn’t a general preference for
minimum samples
, we find that optimal values for
minimum cluster size
in CR-Trans tends toward a smaller value (50-100), whilst the opposite is true for DCF-Vul (125-150).
In terms of backoff strategy, DCF-Vul only prefers the global calibrator.
Whilst this is the case against
E
​
M
EM
for DCF-Bug, half of the cases against
E
​
P
EP
prefer backing off to the uncalibrated confidence score.
For CR-Trans, all but four cases prefer the uncalibrated confidence score, indicating that outliers in the task deviate substantially from the shared
σ
​
(
z
)
\sigma(z)
function.
This further corroborates previous findings of substantial error heterogeneity and covariate shift in automated code refinement.
Figure 11:
Hyperparameter Search for Local Platt-Scaling w/ Minimum Token Probability using CR-Trans Test Samples
How much validation data is required to approximate the optimal hyperparameters for local Platt-scaling in automated code refinement?
As established, the open-ended nature of CR-Trans may induce covariate shift, necessitating local Platt-scaling.
Since the optimal hyperparameters are unknown a priori, we examine how many samples from the test distribution are required to obtain an accurate approximation.
Figure
11
shows hyperparameter search experiments for local Platt-scaling with minimum token probability using various percentages of the test distribution.
We focus on two of the most performant models in CR-Trans, CodeLlama-70B and Qwen2.5-72B.
We explore validation subsets between 0-100% (step=20) of the full test set, where 0% requires random hyperparameter selection.
The lines represent the mean calibration result across 10 resamples, whilst the shaded region represents the standard error.
In general we find that the optimal
E
​
C
​
E
ECE
,
ℬ
\mathcal{B}
, and
B
​
C
BC
can be consistently approximated within 20-40% of the new test distribution, after which the results completely stabilise.
This indicates that optimal calibration can be achieved using only early samples from the new test distribution, and that the hyperparameter selection is stable.
What is the recommended confidence calibration strategy for practical deployment in ACR tasks?
For practitioners requiring well-calibrated confidence scores from their LLMs, selecting the most appropriate fine-grained strategy depends on the specific ACR task they are targeting and their tolerance for added latency.
For those targeting automated program repair in the setup of DCF-Bug, minimum token probability with global Platt-scaling is generally sufficient.
This prescription is also broadly applicable to those targeting vulnerability repair in the setup of DCF-Vul.
The local Platt-scaling method becomes necessary when achieving the lowest possible calibration error is critical, such that even a
Δ
​
0.02
\Delta 0.02
increase in ECE is intolerable.
Another scenario is in vulnerability repair, where the practitioner’s focus is on ensuring a wider coverage of probability intervals for
E
​
P
EP
.
In both scenarios, the practitioner must accept increased latency.
Specifically, global Platt-scaling incurs only an additional logistic regression call per code revision, whereas local Platt-scaling further requires a forward pass through the Qwen3-Embedding-8B model and a cluster assignment before the logistic regression.
We note that, given the relatively small size of the embedding model, local Platt-scaling remains significantly faster than approaches like P(True)
[
21
,
61
,
29
]
or stochastic sampling
[
8
]
.
For practitioners interested in automated code refinement in the style of CR-Trans, combining minimum token probability with local Platt-scaling is essential; without it, the resulting confidence scores are severely miscalibrated, which will result in misinformed decisions regarding the generated code revision.
VIII
Threats to Validity
We now discuss the threats to internal and external validity.
Internal Validity.
To mitigate dataset specific effects, we consider three different ACR tasks, each associated with distinct training and test sets.
In addition, for each task we report results using two complementary correctness metrics.
To mitigate potential effects from data leakage, we either use test sets with non-permissive licenses or conduct semantic preserving code transformations coupled with natural language paraphrasing.
To address prior concerns about unstable results in small software engineering benchmarks
[
60
]
(120-164), we introduce larger training (1.6K–1.8K) and test sets (777–1K).
This is a prerequisite condition for reliable calibration calculation.
To ensure comparability and consistency across inference runs, we consider only zero-shot prompts with greedy decoding and deploy all models using native bfloat-16 precision.
External Validity.
To demonstrate the general applicability of our fine-grained calibration techniques across LLMs, we evaluate 14 open-source models drawn from three distinct series, spanning sizes from
≤
\leq
8B to
≤
\leq
72B parameters.
Given that many state-of-the-art models now have hundreds of billions to trillions of parameters
[
51
,
11
,
74
,
31
]
, we encourage researchers with sufficient computing resources to replicate our experiments using more powerful models.
Because our methods rely on token-level softmax probabilities with some requiring access to the attention mechanism, they are generally not applicable to most closed-source models that are only available through an API.
As such, we consider our fine-grained calibration methods as white-box approaches.
We focus on three main ACR tasks.
Since our experiments are not exhaustive, replication studies on additional code revision tasks are needed before applying our approaches in production.
For each task, we present only a specific problem setup due to limitations in the sizes of other recent benchmarks
[
58
,
46
]
.
We recommend follow-up studies for alternative task formats once sufficient non-contaminated data is available for facilitating reliable calculation of calibration error.
Whilst we explored three different correctness metrics, they remain imperfect proxies for true correctness due to the possibility of false positives and negatives. Therefore, future researchers should replicate our studies when more reliable proxies for correctness are available for these tasks.
IX
Conclusion
In this study, we explored the use of fine-grained approaches for confidence calibration of LLMs in automated code revision tasks.
Our experiments encompassed three tasks, namely automated program repair, vulnerability repair, and automated code refinement; three correctness metrics, namely exact match, edit progress, and checks passed; and 14 different open-source models spanning across various sizes.
We find that fine-grained confidence scores, in particular the minimum token probability, consistently achieve both lower calibration error and greater coverage of probability intervals compared to traditional sequence-level confidence scores.
Additionally, we find that applying Platt-scaling with an ensemble of local calibrators can further improve over the conventional implementation that uses a single global calibrator.
For automated program and vulnerability repair, the selection between local and global Platt-scaling is contingent upon the user’s prioritisation of absolute calibration error reduction versus inference latency; in contrast, for automated code refinement, the application of local Platt-scaling is imperative to achieving an adequately calibrated confidence signal.
Looking forward, future research could further explore universal calibrators to support adaptive switching across different software engineering tasks
[
56
]
, robust calibration for out-of-distribution scenarios
[
62
]
, as well as confidence calibration across different reasoning paradigms such as chain-of-thought
[
71
]
, tree-of-thoughts
[
75
]
, and multi-step agentic setups
[
76
]
.
We hope this work encourages further research on confidence calibration in AI for software engineering and, more broadly, promotes the development of principled uncertainty quantification methods for reliable and trustworthy AI-driven software development tools.
References
[1]
S. Abnar and W. H. Zuidema
(2020)
Quantifying attention flow in transformers
.
In
58th ACL
,
External Links:
Document
Cited by:
§
IV-A
2
.
[2]
S. Barke, M. B. James, and N. Polikarpova
(2023)
Grounded copilot: how programmers interact with code-generating models
.
In
ACM OOPSLA
,
External Links:
Document
Cited by:
§
V-B
.
[3]
N. C. Benz and M. G. Rodriguez
(2023)
Human-aligned calibration for ai-assisted decision making
.
In
37th NeurIPS
,
Cited by:
§I
.
[4]
B. Berabi, A. Gronskiy, V. Raychev, G. Sivanrupan, V. Chibotaru, and M. T. Vechev
(2024)
DeepCode AI fix: fixing security vulnerabilities with large language models
.
arXiv preprint arXiv.2402.13291
.
Cited by:
§
IV-E
,
§
IV-E
.
[5]
R. J. Campello, D. Moulavi, and J. Sander
(2013)
Density-based clustering based on hierarchical density estimates
.
In
Springer PAKDD
,
Cited by:
§
IV-B
2
,
§
V-B
.
[6]
Y. Chen, L. Yuan, G. Cui, Z. Liu, and H. Ji
(2023)
A close look into the calibration of pre-trained language models
.
In
61st ACL
,
External Links:
Document
Cited by:
§
II-B
.
[7]
R. Choudhuri, B. Trinkenreich, R. Pandita, E. Kalliamvakou, I. Steinmacher, M. A. Gerosa, C. Sanchez, and A. Sarma
(2025)
What guides our choices? modeling developers’ trust and behavioral intentions towards genai
.
In
47th IEEE/ACM ICSE
,
External Links:
Document
Cited by:
§I
.
[8]
Y. Chung, I. Char, and J. Schneider
(2024)
Sampling-based multi-dimensional recalibration
.
In
41st ICML
,
Cited by:
§
II-B
,
§VII
.
[9]
G. Detommaso, M. A. Bertran, R. Fogliato, and A. Roth
(2024)
Multicalibration for confidence scoring in llms
.
In
41st ICML
,
Cited by:
§
IV-B
2
,
§
IV-B
2
.
[10]
V. Dibia, A. Fourney, G. Bansal, F. Poursabzi-Sangdeh, H. Liu, and S. Amershi
(2023)
Aligning offline metrics and human judgments of value for code generation models
.
In
Findings of ACL
,
External Links:
Document
Cited by:
§
IV-F
.
[11]
A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Yang, A. Fan,
et al.
(2024)
The llama 3 herd of models
.
arXiv preprint arXiv:2407.21783
.
Cited by:
§VIII
.
[12]
A. Elgohary, C. Meek, M. Richardson, A. Fourney, G. Ramos, and A. H. Awadallah
(2021)
NL-EDIT: correcting semantic parse errors through natural language interaction
.
In
NAACL-HLT
,
External Links:
Document
Cited by:
§
IV-F
,
§
IV-F
.
[13]
W. B. Glenn
et al.
(1950)
Verification of forecasts expressed in terms of probability
.
Mon. Weather Rev.
78
(
1
),
pp. 1–3
.
Cited by:
§
IV-D
.
[14]
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
(2017)
On calibration of modern neural networks
.
In
34th ICML
,
Cited by:
§I
,
§
II-B
,
§
II-B
,
§III
,
§
IV-D
,
§
IV-D
.
[15]
Q. Guo, J. Cao, X. Xie, S. Liu, X. Li, B. Chen, and X. Peng
(2024)
Exploring the potential of chatgpt in automated code refinement: an empirical study
.
In
46th IEEE/ACM ICSE
,
External Links:
Document
Cited by:
§I
,
§
II-A
.
[16]
Q. Guo, X. Xie, S. Liu, M. Hu, X. Li, and L. Bu
(2025)
Intention is all you need: refining your code from your intention
.
In
47th IEEE/ACM ICSE
,
External Links:
Document
Cited by:
§
V-A
.
[17]
X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy, and H. Wang
(2024)
Large language models for software engineering: a systematic literature review
.
ACM TOSEM
33
(
8
).
External Links:
Document
Cited by:
§
II-A
.
[18]
N. Jiang, K. Liu, T. Lutellier, and L. Tan
(2023)
Impact of code language models on automated program repair
.
In
45th IEEE/ACM ICSE
,
External Links:
Document
Cited by:
§
IV-A
2
.
[19]
D. D. Johnson, D. Tarlow, and C. Walder
(2023)
RU-sure? uncertainty-aware code suggestions by maximizing utility across random user intents
.
In
40th ICML
,
Cited by:
§
II-B
.
[20]
T. Joy, F. Pinto, S. Lim, P. H. Torr, and P. K. Dokania
(2023)
Sample-dependent adaptive temperature scaling for improved calibration
.
In
37th AAAI
,
Cited by:
§
II-B
.
[21]
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson,
et al.
(2022)
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Cited by:
§
II-B
,
§VII
.
[22]
M. G. Kendall
(1938)
A new measure of rank correlation
.
Biometrika
30
(
1-2
),
pp. 81–93
.
Cited by:
§VI
.
[23]
L. Kuhn, Y. Gal, and S. Farquhar
(2023)
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
11th ICLR
,
Cited by:
§VI
.
[24]
A. Kumar, P. Liang, and T. Ma
(2019)
Verified uncertainty calibration
.
In
32nd NeurIPS
,
Cited by:
§
IV-D
.
[25]
V. I. Levenshtein
(1965)
Binary codes capable of correcting deletions, insertions, and reversals
.
Sov. Phys. Dokl.
10
,
pp. 707–710
.
Cited by:
§
IV-F
.
[26]
Z. Li, S. Lu, D. Guo, N. Duan, S. Jannu, G. Jenks, D. Majumder, J. Green, A. Svyatkovskiy, S. Fu, and N. Sundaresan
(2022)
Automating code review activities by large-scale pre-training
.
In
30th ACM ESEC/FSE
,
External Links:
Document
Cited by:
§
IV-E
.
[27]
J. T. Liang, C. Yang, and B. A. Myers
(2024)
A large-scale survey on the usability of AI programming assistants: successes and challenges
.
In
46th IEEE/ACM ICSE
,
External Links:
Document
Cited by:
§I
.
[28]
H. Y. Lin, C. Liu, H. Gao, P. Thongtanunam, and C. Treude
(2025)
CodeReviewQA: the code review comprehension assessment for large language models
.
In
Findings of ACL
,
Cited by:
§I
,
§
II-A
,
§
IV-A
2
,
§
IV-E
,
§
V-A
.
[29]
S. Lin, J. Hilton, and O. Evans
(2022)
Teaching models to express their uncertainty in words
.
TMLR
.
Cited by:
§
II-B
,
§VII
.
[30]
Z. Lin, S. Trivedi, and J. Sun
(2024)
Contextualized sequence likelihood: enhanced confidence scores for natural language generation
.
In
EMNLP
,
External Links:
Document
Cited by:
§
IV-A
2
.
[31]
A. Liu, B. Feng, B. Wang, B. Wang, B. Liu, C. Zhao, C. Dengr, C. Ruan, D. Dai, D. Guo,
et al.
(2024)
Deepseek-v2: a strong, economical, and efficient mixture-of-experts language model
.
arXiv preprint arXiv:2405.04434
.
Cited by:
§VIII
.
[32]
C. Liu, H. Y. Lin, and P. Thongtanunam
(2025)
Too noisy to learn: enhancing data quality for code review comment generation
.
In
22nd IEEE/ACM MSR
,
External Links:
Document
Cited by:
§
IV-E
.
[33]
J. Liu, C. Ye, S. Wang, R. Cui, J. Zhang, K. Zhang, and N. Barnes
(2023)
Model calibration in dense classification with adaptive label perturbation
.
In
IEEE/CVF ICCV
,
Cited by:
§
II-B
.
[34]
X. Liu, F. F. Bayat, and L. Wang
(2024)
Enhancing language model factuality via activation-based confidence calibration and guided decoding
.
In
EMNLP
,
External Links:
Document
Cited by:
§I
.
[35]
X. Liu, M. Khalifa, and L. Wang
(2024)
LitCab: lightweight language model calibration over short- and long-form responses
.
In
12th ICLR
,
Cited by:
§I
.
[36]
J. Lu, L. Yu, X. Li, L. Yang, and C. Zuo
(2023)
LLaMA-reviewer: advancing code review automation with large language models through parameter-efficient fine-tuning
.
In
34th IEEE ISSRE
,
External Links:
Document
Cited by:
§
IV-E
.
[37]
S. Ma, Y. Lei, X. Wang, C. Zheng, C. Shi, M. Yin, and X. Ma
(2023)
Who should I trust: AI or myself? leveraging human and AI correctness likelihood to promote appropriate trust in ai-assisted decision-making
.
In
41st ACM CHI
,
External Links:
Document
Cited by:
§I
.
[38]
P. Manakul, A. Liusie, and M. Gales
(2023)
Selfcheckgpt: zero-resource black-box hallucination detection for generative large language models
.
In
EMNLP
,
Cited by:
§
IV-A
2
.
[39]
M. V. Mäntylä and C. Lassenius
(2009)
What types of defects are really discovered in code reviews?
.
IEEE TSE
35
(
3
),
pp. 430–448
.
External Links:
Document
Cited by:
§
II-A
,
§VII
.
[40]
L. Marusich, J. Z. Bakdash, Y. Zhou, and M. Kantarcioglu
(2024)
Using AI uncertainty quantification to improve human decision-making
.
In
41st ICML
,
Cited by:
§I
.
[41]
L. McInnes, J. Healy, N. Saul, and L. Großberger
(2018)
UMAP: uniform manifold approximation and projection
.
J. Open Source Softw.
3
(
29
),
pp. 861
.
External Links:
Document
Cited by:
§
IV-B
2
.
[42]
C. M. Montes and R. Khojah
(2025)
Emotional strain and frustration in llm interactions in software engineering
.
In
29th ACM EASE
,
Cited by:
§I
,
§I
.
[43]
N. Muennighoff, N. Tazi, L. Magne, and N. Reimers
(2023)
Mteb: massive text embedding benchmark
.
In
17th EACL
,
Cited by:
footnote 1
.
[44]
M. P. Naeini, G. F. Cooper, and M. Hauskrecht
(2015)
Obtaining well calibrated probabilities using bayesian binning
.
In
29th AAAI
,
External Links:
Document
Cited by:
§
IV-D
.
[45]
J. Nixon, M. W. Dusenberry, L. Zhang, G. Jerfel, and D. Tran
(2019)
Measuring calibration in deep learning
.
In
IEEE/CVF CVPR
,
Cited by:
§
IV-D
.
[46]
Y. Nong, H. Yang, L. Cheng, H. Hu, and H. Cai
(2025)
APPATCH: automated adaptive prompting large language models for real-world software vulnerability patching
.
In
34th USENIX
,
Cited by:
§I
,
§I
,
§
II-A
,
§
V-A
,
§VIII
.
[47]
P. Peduzzi, J. Concato, E. Kemper, T. R. Holford, and A. R. Feinstein
(1996)
A simulation study of the number of events per variable in logistic regression analysis
.
Elsevier J. Clin. Epidemiol.
49
(
12
),
pp. 1373–1379
.
Cited by:
§
V-B
.
[48]
J. Platt
et al.
(1999)
Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods
.
Adv. Large Margin Classif.
10
(
3
),
pp. 61–74
.
Cited by:
§I
,
§
II-B
,
§
IV-B
1
.
[49]
S. Prabhudesai, L. Yang, S. Asthana, X. Huan, Q. V. Liao, and N. Banovic
(2023)
Understanding uncertainty: how lay decision-makers perceive and interpret uncertainty in human-ai decision making
.
In
8th ACM IUI
,
External Links:
Document
Cited by:
§I
.
[50]
D. Ramos, C. Mamede, K. Jain, P. Canelas, C. Gamboa, and C. Le Goues
(2025)
Are large language models memorizing bug benchmarks?
.
In
2nd IEEE/ACM LLM4Code@ICSE
,
External Links:
Document
Cited by:
§
IV-E
.
[51]
X. Ren, P. Zhou, X. Meng, X. Huang, Y. Wang, W. Wang, P. Li, X. Zhang, A. Podolskiy, G. Arshinov,
et al.
(2023)
Pangu-
{
\{
\
\backslash
sigma
}
\}
: towards trillion parameter language model with sparse heterogeneous computing
.
arXiv preprint arXiv:2303.10845
.
Cited by:
§VIII
.
[52]
R. Roelofs, N. Cain, J. Shlens, and M. C. Mozer
(2022)
Mitigating bias in calibration error estimation
.
In
25th AISTATS
,
Cited by:
§
IV-D
.
[53]
S. Sabouri, P. Eibl, X. Zhou, M. Ziyadi, N. Medvidovic, L. Lindemann, and S. Chattopadhyay
(2025)
Trust dynamics in ai-assisted development: definitions, factors, and implications
.
In
47th IEEE/ACM ICSE
,
External Links:
Document
Cited by:
§I
.
[54]
V. Satopaa, J. R. Albrecht, D. E. Irwin, and B. Raghavan
(2011)
Finding a ”kneedle” in a haystack: detecting knee points in system behavior
.
In
31st IEEE/ACM ICDCSW
,
External Links:
Document
Cited by:
§
IV-A
2
,
§
IV-A
2
.
[55]
M. Shen, S. Das, K. H. Greenewald, P. Sattigeri, G. W. Wornell, and S. Ghosh
(2024)
Thermometer: towards universal calibration for large language models
.
In
41st ICML
,
Cited by:
§I
.
[56]
M. Shen, S. Das, K. Greenewald, P. Sattigeri, G. W. Wornell, and S. Ghosh
(2024)
Thermometer: towards universal calibration for large language models
.
In
41st ICML
,
Cited by:
§IX
.
[57]
A. Silva, S. Fang, and M. Monperrus
(2025)
RepairLLaMA: efficient representations and fine-tuned adapters for program repair
.
IEEE TSE
51
(
8
),
pp. 2366–2380
.
External Links:
Document
Cited by:
§I
,
§
II-A
,
§
V-A
.
[58]
A. Silva and M. Monperrus
(2025)
RepairBench: leaderboard of frontier models for program repair
.
In
2nd IEEE/ACM LLM4Code@ICSE
,
External Links:
Document
Cited by:
§
II-A
,
§
V-A
,
§VIII
.
[59]
Snyk
Snyk code - developer-focused, real-time sast.
.
Note:
https://snyk.io/product/snyk-code/
Accessed: Oct. 14, 2025
Cited by:
§
IV-F
.
[60]
C. Spiess, D. Gros, K. S. Pai, M. Pradel, Md. R. I. Rabin, A. Alipour, S. Jha, P. Devanbu, and T. Ahmed
(2025)
Calibration and correctness of language models for code
.
In
47th IEEE/ACM ICSE
,
External Links:
Document
Cited by:
§I
,
§I
,
§
II-B
,
§
II-B
,
§
IV-A
1
,
§
IV-A
1
,
§
IV-B
,
§
IV-D
,
§
IV-D
,
§
IV-D
,
§IV
,
§VI
,
§VIII
.
[61]
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. Manning
(2023)
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
EMNLP
,
Cited by:
§
II-B
,
§VII
.
[62]
C. Tomani, S. Gruber, M. E. Erdem, D. Cremers, and F. Buettner
(2021)
Post-hoc uncertainty calibration for domain drift scenarios
.
In
IEEE/CVF CVPR
,
Cited by:
§
II-B
,
§IX
.
[63]
R. Tufano, O. Dabic, A. Mastropaolo, M. Ciniselli, and G. Bavota
(2024)
Code review automation: strengths and weaknesses of the state of the art
.
IEEE TSE
50
(
2
),
pp. 338–353
.
External Links:
Document
Cited by:
§
II-A
,
§
IV-E
,
§
IV-E
.
[64]
P. Vaithilingam, T. Zhang, and E. L. Glassman
(2022)
Expectation vs. experience: evaluating the usability of code generation tools powered by large language models
.
In
40th ACM CHI
,
External Links:
Document
Cited by:
§I
.
[65]
H. Vasconcelos, G. Bansal, A. Fourney, Q. V. Liao, and J. Wortman Vaughan
(2025)
Generation probabilities are not enough: uncertainty highlighting in ai code completions
.
ACM TOCHI
32
(
1
),
pp. 1–30
.
Cited by:
§
II-B
.
[66]
Y. Virk, P. T. Devanbu, and T. Ahmed
(2025)
Calibration of large language models on code summarization
.
In
33rd ACM FSE
,
External Links:
Document
Cited by:
§I
,
§
II-B
,
§
IV-A
1
,
§
IV-D
.
[67]
Y. Wald, A. Feder, D. Greenfeld, and U. Shalit
(2021)
On calibration and out-of-domain generalization
.
In
35th NeurIPS
,
Cited by:
§
IV-B
2
.
[68]
D. Wang, L. Feng, and M. Zhang
(2021)
Rethinking calibration of deep neural networks: do not be afraid of overconfidence
.
In
34th NeurIPS
,
Cited by:
§
IV-D
.
[69]
R. Wang, R. Cheng, D. Ford, and T. Zimmermann
(2024)
Investigating and designing for trust in ai-powered code generation tools
.
In
7th ACM FAccT
,
External Links:
Document
Cited by:
§I
.
[70]
S. Wang, Z. Tu, S. Shi, and Y. Liu
(2020)
On the inference calibration of neural machine translation
.
In
58th ACL
,
External Links:
Document
Cited by:
§
II-B
,
§
IV-A
1
.
[71]
J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou
(2022)
Chain-of-thought prompting elicits reasoning in large language models
.
In
36th NeurIPS
,
Cited by:
§IX
.
[72]
Y. Wu, N. Jiang, H. V. Pham, T. Lutellier, J. Davis, L. Tan, P. Babkin, and S. Shah
(2023)
How effective are neural networks for fixing security vulnerabilities
.
In
32nd ACM SIGSOFT ISSTA
,
External Links:
Document
Cited by:
§
IV-E
.
[73]
C. S. Xia and L. Zhang
(2024)
Automated program repair via conversation: fixing 162 out of 337 bugs for
$
\mathdollar
0.42 each using chatgpt
.
In
33rd ACM SIGSOFT ISSTA
,
External Links:
Document
Cited by:
§
II-A
.
[74]
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv,
et al.
(2025)
Qwen3 technical report
.
arXiv preprint arXiv:2505.09388
.
Cited by:
§VIII
.
[75]
S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan
(2023)
Tree of thoughts: deliberate problem solving with large language models
.
In
37th NeurIPS
,
Cited by:
§IX
.
[76]
S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. R. Narasimhan, and Y. Cao
(2023)
ReAct: synergizing reasoning and acting in language models
.
In
11th ICLR
,
Cited by:
§IX
.
[77]
Y. Yu, S. Bates, Y. Ma, and M. Jordan
(2022)
Robust calibration with multi-domain temperature scaling
.
In
36th NeurIPS
,
Cited by:
§
IV-B
2
.
[78]
P. Zablotskaia, D. Phan, J. Maynez, S. Narayan, J. Ren, and J. Z. Liu
(2023)
On uncertainty calibration and selective generation in probabilistic neural summarization: A benchmark study
.
In
Findings of EMNLP
,
External Links:
Document
Cited by:
§I
.
[79]
B. Zadrozny and C. Elkan
(2001)
Obtaining calibrated probability estimates from decision trees and naive bayesian classifiers
.
In
8th ICML
,
Cited by:
§
II-B
.
[80]
B. Zadrozny and C. Elkan
(2002)
Transforming classifier scores into accurate multiclass probability estimates
.
In
8th ACM SIGKDD KDD
,
Cited by:
§
II-B
.
[81]
Y. Zhang, M. Li, D. Long, X. Zhang, H. Lin, B. Yang, P. Xie, A. Yang, D. Liu, J. Lin, F. Huang, and J. Zhou
(2025)
Qwen3 embedding: advancing text embedding and reranking through foundation models
.
arXiv preprint arXiv:2506.05176
.
Cited by:
§
IV-B
2
.
[82]
Y. Zhang, Q. V. Liao, and R. K. E. Bellamy
(2020)
Effect of confidence and explanation on accuracy and trust calibration in ai-assisted decision making
.
In
20th ACM FAT*
,
External Links:
Document
Cited by:
§I
.
[83]
X. Zhou, S. Cao, X. Sun, and D. Lo
(2025)
Large language model for vulnerability detection and repair: literature review and the road ahead
.
ACM TOSEM
34
(
5
).
External Links:
Document
Cited by:
§
II-A
.
[84]
X. Zhou, K. Kim, B. Xu, D. Han, J. He, and D. Lo
(2023)
Generation-based code review automation: how far are we?
.
In
31st IEEE/ACM ICPC
,
External Links:
Document
Cited by:
§
IV-F
.
[85]
Z. Zhou, C. Sha, and X. Peng
(2024)
On calibration of pre-trained code models
.
In
IEEE/ACM 46th ICSE
,
External Links:
Document
Cited by:
§
II-B
.
[86]
C. Zhu, B. Xu, Q. Wang, Y. Zhang, and Z. Mao
(2023)
On the calibration of large language models and alignment
.
In
Findings of EMNLP
,
Cited by:
§I
,
§
II-B
,
§
IV-B
.