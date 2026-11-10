---
title: 'Beyond Confidence: Rethinking Uncertainty Calibration in Deep Code Models'
id: beyond-confidence-rethinking-uncertainty-calibration-in-deep-code-models
tags:
- code-llm-confidence-positioning-d82d00
- w3-forward-citation
created: '2026-11-10T08:24:04.765644Z'
updated: '2026-11-10T08:25:34.261155Z'
source: https://arxiv.org/html/2610.21248
source_domain: arxiv.org
fetched_at: '2026-11-10T08:24:04.761672Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Study of 13 uncertainty signals and 3 post-hoc calibrators (temperature,
  Platt, isotonic) on seven code models (CodeBERT, RoBERTa, GraphCodeBERT, StarCoder-3B,
  CodeLlama-7B, DeepSeek-Coder-7B, Qwen2.5-Coder-7B) for code CLASSIFICATION (vulnerability
  detection, defect prediction) only, explicitly excluding generative code. Finds
  ECE-improving calibrators do not consistently improve selective prediction and calibration
  metrics can disagree with selective-prediction performance. Occupies a metric-validity
  theme (F-adjacent) but on classification with dataset labels, not execution ground
  truth.
---

Beyond Confidence: Rethinking Uncertainty Calibration in Deep Code Models
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2610.21248v1 [cs.SE] 15 Oct 2026
Beyond Confidence: Rethinking Uncertainty Calibration in Deep Code Models
Anonymous Authors
Ravishka Rathnasuriya
Affiliation:
Department of Computer Science
University of Texas at Dallas
ravishka.rathnasuriya@utdallas.edu
Affiliation:
Affiliation:
Wei Yang
Affiliation:
Institute of Systems for Advanced Computing
Fudan University
yang_wei@fudan.edu.cn
Abstract
Deep learning models have shown significant promise in code-related tasks. While confidence calibration techniques have been proposed to improve model reliability, their effectiveness in real-world tasks with strict accuracy requirements remains uncertain. In this paper, we investigate two key questions: first, whether existing measurement metrics, including confidence scores and uncertainty metrics, are effective for guiding selective prediction; and second, whether existing calibration techniques can improve these metrics to better identify cases
where model predictions are likely to succeed or fail.
We conduct a systematic study on defect prediction and vulnerability detection using seven code models, evaluating thirteen uncertainty signals and three widely used post-hoc calibration methods. Our analysis reveals three major findings: (1) even strong uncertainty signals can remain poorly calibrated and provide limited separation at the high-confidence end, constraining selective prediction in practice; (2) standard post-hoc calibrators often improve calibration scores but do not consistently translate into better selective prediction behavior; and (3) commonly used calibration metrics can disagree with selective prediction performance, underscoring the need to evaluate both jointly. Moreover, our findings motivate a decision-oriented view of reliability in deep code models, where calibrated scores must be evaluated together with selective-prediction quality and retained-region risk before they can support accept–defer deployment.
I
Introduction
Deep learning code models have demonstrated impressive capabilities in various code-related tasks such as defect prediction and vulnerability detection
[
1
,
2
,
3
,
4
,
5
,
6
,
7
,
8
,
9
]
. To improve the reliability of these models, recent research
has explored confidence calibration techniques that align predicted probabilities with true correctness likelihoods
[
10
,
11
,
12
,
13
,
14
]
.
However, the practical effectiveness of these techniques in code tasks remains unclear, particularly when models are used in automated systems where inaccurate predictions can lead
to costly failures. In such cases, low-confidence predictions are often deferred to human experts. This paper investigates whether existing calibration methods genuinely enhance code model reliability or whether alternative approaches provide more trustworthy guidance.
While recent techniques
[
14
,
13
,
15
]
have been proposed to improve the confidence calibration on code models, these techniques often treat calibration accuracy as an end in itself rather than as a tool to enhance downstream performance. These techniques primarily aim to align predicted confidence scores with empirical correctness, yet these studies seldom evaluate whether better-calibrated confidence actually improves the utility of code models in practice. In particular, these studies overlook whether calibration improvements lead to gains in accuracy or selective prediction
[
16
,
17
]
, where the model produces an output only when it is sufficiently confident, and otherwise abstains to avoid unreliable predictions. In contrast, our work extends beyond calibration by jointly examining selective prediction and reliability assessment, two concerns that are essential for reliable deployment but often neglected in prior studies. This broader focus helps clarify how calibration can support trustworthy and actionable predictions in real-world settings.
Our investigation is motivated by two key concerns. First, we examine whether existing confidence and uncertainty scores are reliable indicators of prediction quality in code models. Unlike models in other domains, code models face unique challenges that affect their trustworthiness. One such issue is their tendency to rely on superficial patterns rather than truly understanding the semantics of the code, which can lead to misleading predictions. These models may confidently label a vulnerable function as safe simply because it resembles patterns seen in non-vulnerable code. This becomes especially problematic when the vulnerability is hidden within well-structured code that appears correct on the surface. Another challenge is that models often focus on local syntax but fail to capture important relationships across different parts of the codebase, which further reduces their ability to make reliable predictions. In such cases, relying only on confidence or uncertainty scores may not reflect when the model is making a mistake. Even if the score is well-calibrated, it might still assign high confidence to an incorrect prediction. This raises the question of whether existing
[
18
,
19
,
20
,
21
,
22
,
23
,
24
,
25
,
26
]
or new metrics tailored for code model behavior could offer better signals for deciding when model outputs can be trusted.
Even if confidence or uncertainty scores are accepted as reasonable inputs for calibration, widely used calibration metrics face important limitations. Metrics like Expected Calibration Error (ECE)
[
27
]
and Uncertainty Calibration Error (UCE)
[
28
]
focus on aligning predicted probabilities with true correctness across the entire confidence range. However, this broad averaging places equal weight on all predictions, including low-confidence ones that are often ignored in real applications. In practice, such predictions are typically treated as unreliable by default, regardless of how well they are calibrated. What matters more is the accuracy of high-confidence predictions, since these are the outputs that users are most likely to trust. For code-related tasks, errors in this high-confidence region are especially costly. Yet, current calibration metrics often under-represent these cases, providing limited insight into how well the model performs when it is most certain. As a result, improvements in overall calibration may obscure critical failures in the predictions that matter most for reliable deployment.
To address the limitations of existing work, this paper investigates the practical reliability of calibrated deep code models through a focused study of
code classification
tasks. We intentionally restrict our empirical evaluation to defect prediction and vulnerability detection because they provide a clean setting in which correctness and uncertainty can be defined at the example level. This allows us to assess behavioral calibration and selective prediction without conflating the analysis with unresolved measurement issues in generative code tasks. At the same time, this setting remains important in its own right as code classification is a core form of
code understanding
, and it provides a meaningful basis for evaluating how well code models distinguish reliable from unreliable predictions in software engineering workflows.
Within this scope, we study two related questions. First, we evaluate whether current uncertainty signals are effective for selective prediction, that is, whether they can distinguish which predictions a model should make and which it should defer (Section
IV
). Second, we examine whether standard post-hoc calibration techniques improve a model’s ability to separate reliable from unreliable predictions. While these methods are designed to align predicted probabilities with empirical correctness, their value for deployment-oriented decision-making in code tasks remains unclear.
Through a systematic study across SE tasks, we assess how uncertainty estimation and calibration influence a model’s capacity to support selective prediction. Our study yields three takeaways about reliability in deep code classification. First, uncertainty signals can remain poorly calibrated and often fail to reliably prioritize the highest-confidence predictions, which are most critical for practical deployment. This limits how effectively selective prediction can stratify outputs by reliability. As a result, selective prediction gains can plateau and become unstable at high rejection, where decisions are driven by a small retained subset and minor ranking errors have outsized impact. Second, post-hoc calibration improves probability alignment but does not guarantee improved selective decision quality. Even when calibration metrics improve, models can continue to produce high-confidence mistakes, which directly undermines accept–defer behavior. Third, commonly used evaluation metrics provide incomplete guidance when used in isolation. Global calibration scores summarize average alignment but can miss the failure mode most relevant to deployment, namely whether errors are assigned low confidence. This motivates reporting calibration and selective prediction performance jointly, and analyzing how ranking quality changes across the confidence spectrum.
Building on these empirical results, the paper develops a broader account of reliability in deep code models. We show that reliability failure is shaped jointly by data ambiguity, representational bias, optimization objectives, and deployment-time decisions, rather than by score miscalibration alone. This explains why better global calibration does not always translate into safer selective prediction. More importantly, it motivates a shift in software engineering research toward decision-oriented reliability methods and evaluation criteria that emphasize accepted-set safety and behavior in the high-confidence region.
In summary, this paper makes the following contributions:
•
Joint focus on calibration and abstention:
We study uncertainty calibration together with selective prediction, which are ignored in prior calibration work.
•
Empirical study:
A large-scale evaluation of 13 uncertainty metrics and three post-hoc calibration methods across seven code models and two SE tasks, revealing persistent miscalibration, especially in high-confidence regions.
•
Analysis of metric limitations:
We show that common calibration metrics (e.g., ECE) often fail to reflect true prediction reliability.
•
Operationalizing uncertainty for SE:
We show how uncertainty should be evaluated for accept–defer deployment using calibration quality, selective-prediction quality, and retained-region risk.
II
Preliminaries
Deep learning models are increasingly used for software engineering classification tasks such as vulnerability detection and defect prediction
[
1
,
2
,
3
,
4
,
5
,
6
,
7
,
8
,
9
]
. Despite strong predictive performance, these models can produce overconfident errors
[
14
,
13
]
, assigning high confidence to incorrect labels. Such behavior is problematic in automated workflows, where predictions may trigger downstream actions in security and quality assurance settings.
Reliability in these settings requires more than accuracy. It also requires confidence or uncertainty signals that reflect the likelihood of correctness, so that a system can decide when to trust a prediction and when to defer it. Selective prediction formalizes this requirement by allowing a model to abstain on inputs where its decision is unreliable
[
16
,
17
]
. A common implementation accepts predictions whose confidence exceeds a threshold and defers the rest, trading coverage for accuracy on the accepted subset. The effectiveness of this approach depends on whether the underlying confidence or uncertainty signal meaningfully separates correct from incorrect predictions.
II-A
Calibration
Calibration refers to the alignment between a model’s predicted confidence scores and the actual likelihood of correctness
[
27
,
14
,
13
,
10
,
11
]
. For classification models that output a predictive distribution
P
M
(
⋅
∣
X
)
P_{M}(\cdot\mid X)
, the predicted label is
y
^
=
arg
⁡
max
y
​
P
M
​
(
y
∣
X
)
\hat{y}=\arg\max_{y}P_{M}(y\mid X)
and the associated confidence is
c
⁡
(
X
)
=
max
y
⁡
P
M
​
(
y
∣
X
)
c(X)=\max_{y}P_{M}(y\mid X)
.
A model is perfectly calibrated if, for every confidence level
p
∈
[
0
,
1
]
p\in[0,1]
, the predictions made with confidence
p
p
are correct with frequency
p
p
:
Pr
⁡
(
y
^
=
y
∣
c
⁡
(
X
)
=
p
)
=
p
,
∀
p
∈
[
0
,
1
]
.
\Pr(\hat{y}=y\mid c(X)=p)=p,\quad\forall p\in[0,1].
(1)
Because exact conditioning on
c
⁡
(
X
)
=
p
c(X)=p
is not attainable with finite samples, calibration is typically assessed using summary metrics. The Brier score measures the mean squared error between predicted probabilities and the observed labels, while ECE estimates the average gap between confidence and accuracy over confidence bins
[
27
,
11
]
. These metrics are widely used to compare models and to evaluate post hoc calibration methods.
II-B
Uncertainty Calibration for Selective Prediction in Code Tasks
In code classification, confidence can be unreliable even when accuracy is high. Predictions may be driven by lexical or syntactic cues that correlate with labels in the training data but fail to reflect program semantics
[
29
,
30
,
31
,
32
]
. As a result, a model can assign high confidence to a misclassification when the input contains subtle behaviors that are not captured by surface features. Long-range dependencies and interactions across statements further complicate this setting, since errors may depend on relationships that are difficult to represent with local token evidence.
These properties motivate studying uncertainty signals beyond the maximum softmax probability. Prior work has proposed entropy-based and sampling-based measures that aim to capture predictive ambiguity and model variability
[
18
,
19
,
20
,
22
,
23
,
24
]
. In our setting, these measures are used as scoring functions for selective prediction, where larger uncertainty is intended to indicate higher error likelihood. Uncertainty calibration then refers to aligning these scores with empirical correctness so that thresholds correspond to predictable reliability levels. Metrics such as ECE
[
27
,
11
,
10
]
and UCE
[
28
]
are commonly used to quantify this alignment.
Poor calibration weakens selective prediction in two ways. First, overconfident errors may remain among accepted predictions, undermining reliability. Second, overly conservative scores may defer many correct predictions, reducing coverage without improving decision quality. Understanding when uncertainty signals are well calibrated for code models, and when calibration methods and metrics fail to reflect decision utility, is therefore necessary for reliability-oriented deployment.
III
Research Methodology
This section details our experimental methodology for evaluating uncertainty signals and calibration. We present the datasets and models studied, uncertainty estimation techniques, the post-hoc calibration methods, and evaluation metrics employed in this study.
III-A
Subjects
III-A
1
Datasets and Tasks
We study uncertainty and calibration in two widely used
code classification
tasks, vulnerability detection
[
33
]
and defect prediction
[
34
]
. We focus on classification for three reasons: (i) these tasks are widely used in practice, (ii) uncertainty is easy to obtain from predictive probabilities without additional inference, and (iii) confidence thresholds map directly to accept-or-defer decisions in selective prediction.
Vulnerability detection (binary classification).
We use the Devign dataset
[
33
]
, which contains 27,318 C functions from FFmpeg and Qemu labeled as
vulnerable
(14,858) or
clean
(12,460). We use the standard split into training (21,854), validation (2,732), and test (2,732) sets.
Defect prediction (multi-task classification).
We use the CodeChef dataset
[
34
]
, which contains 33,822 C/C++ functions labeled as
no defect
(11,362),
wrong output
(13,656),
timeout error
(5,101), or
runtime error
(3,703). We use the provided split into training (21,647), validation (5,411), and test (6,764) sets.
III-B
Models
We use seven state-of-the-art pre-trained models: CodeBERT
[
35
]
, RoBERTa
[
36
]
, GraphCodeBERT
[
31
]
,
StarCoder-3B
[
37
]
, CodeLlama-7B
[
38
]
, DeepSeek-Coder-7B
[
39
]
, and Qwen2.5-Coder-7B
[
40
]
. These models are fine-tuned on the respective tasks following standard practices
[
41
,
42
]
. Their performance in terms of accuracy (A), precision (P), recall (R), and F1-scores (F1) is summarized in Table
I
. These models are widely used in prior work
[
4
,
43
,
44
]
and collectively cover diverse architectures, including encoder-only and decoder-based code LLMs, providing a representative view of modern code classification models.
TABLE I
:
Overall performance of code models.
Model
Vulnerability Detection
Defect Prediction
A
P
R
F1
A
P
R
F1
CodeBERT
63.32
64.56
63.36
61.07
84.41
84.39
84.17
84.16
RoBERTa
61.96
61.84
61.96
61.18
82.17
81.96
82.03
81.90
GraphCodeBERT
64.31
64.76
64.31
63.04
85.4
85.34
85.40
85.20
StarCoder-3B
59.69
59.01
40.15
47.79
76.24
75.82
76.24
75.19
Qwen2.5-Coder-7B
61.53
59.27
51.95
55.37
77.89
77.34
77.91
77.48
CodeLlama-7B
62.51
60.12
54.66
57.26
77.91
77.16
77.91
77.33
DeepSeek-Coder-7B
59.59
57.51
46.05
51.15
79.77
79.29
79.77
79.47
III-C
Uncertainty Measurement Metrics
We analyze 13 uncertainty metrics covering aleatoric and epistemic uncertainty. Confidence-based metrics such as
vanilla
[
18
]
which uses the highest predicted probability as confidence; margin confidence
(MC)
and ratio confidence
(RC)
[
21
]
that measure the difference between the top two probabilities, with smaller gaps indicating higher uncertainty; and least confidence and Best-vs-Second-Best
(BvSB)
[
21
]
that assess uncertainty by evaluating class score differences. The metrics are widely used due to their simplicity, but they often produce misleading results in code tasks, where models may assign high confidence to semantically incorrect predictions driven by surface-level syntax.
Information theory-based metrics
[
19
,
20
]
such
entropy
that measures the dispersion of the probability distribution and mutual information
(MI)
which captures the difference between total and expected entropy. These metrics may fail when softmax outputs are sharply peaked but misaligned with ground truth. To address these limitations, we also include bayesian approximation-based metrics such as Monte Carlo Dropout
(MCD)
[
22
]
which estimates uncertainty by performing multiple stochastic forward passes and Deep Ensembles
(DE)
[
23
]
which aggregates predictions from multiple independently trained models. We derived three different measures from
MCD
and
DE
namely, (1) Sample winning score
(SWS)
which measures prediction consistency across multiple forward passes; (2) Probability variance
(PV)
which evaluates variance in softmax probabilities; and (3) Bayesian active learning by disagreement
(BALD)
which quantifies epistemic uncertainty. By comparing these metrics, we aim to understand which ones give reliable uncertainty estimates for code-related tasks, where models often behave unpredictably.
III-D
Calibration Methods
We employ three post-hoc calibration techniques: Temperature Scaling (TS)
[
27
,
14
]
, Platt Scaling (PS)
[
13
]
, and Isotonic Regression (Iso.R)
[
27
]
, which have been widely adopted in prior studies
[
27
,
14
,
13
,
11
,
10
,
28
]
.
TS
[
27
,
14
]
applies a single scaling parameter to smooth confidence scores, reducing overconfidence in predictions.
Although simple and effective for correcting mild miscalibration in balanced datasets, TS assumes uniform error across samples and may fail when confidence varies significantly across subgroups or semantic classes. We adapt TS to rescale uncertainty scores via:
u
~
i
=
u
i
T
\tilde{u}_{i}=\frac{u_{i}}{T}
(2)
where
u
i
u_{i}
is the original uncertainty score for sample
i
i
,
T
T
is the learned temperature parameter, and
u
~
i
\tilde{u}_{i}
is the calibrated uncertainty score. Unlike conventional TS, which optimizes Negative Log-Likelihood, we minimize Binary Cross-Entropy (BCE) to suit binary correctness signals. TS is computationally efficient, but it often fails to correct miscalibration in unstable prediction settings, which are common in code classification tasks.
PS
extends TS by applying a logistic transformation with two learnable parameters:
p
i
=
σ
⁡
(
a
​
u
i
+
b
)
p_{i}=\sigma(au_{i}+b)
(3)
where
u
i
{u_{i}}
is the original uncertainty score,
σ
⁡
(
x
)
\sigma(x)
is the sigmoid function, and
p
i
{p_{i}}
is the calibrated probability. The
a
a
and
b
b
are learned parameters. To avoid overfitting, we use five-fold rescaling, iteratively training on 80% of the data and validating on 20%. However, PS assumes a globally smooth calibration curve and may extrapolate poorly on non-monotonic uncertainty patterns, which frequently arise in code tasks.
Iso.R
[
27
]
is a non-parametric calibration method that learns a monotonic function mapping uncertainty scores to empirical correctness. Unlike TS and PS, Iso.R does not assume a predefined functional form, making it highly flexible but prone to overfitting when data is sparse.
The learned function
f
⁡
(
u
)
f(u)
minimizes calibration error:
f
^
=
arg
⁡
min
f
​
is isotonic
​
∑
i
(
f
⁡
(
u
i
)
−
y
i
)
2
\hat{f}=\underset{f\text{ is isotonic}}{\arg\min}\sum_{i}(f(u_{i})-y_{i})^{2}
(4)
where
u
i
u_{i}
represents the original uncertainty score,
y
i
y_{i}
is the observed correctness (binary label), and
f
^
\hat{f}
is the learned isotonic function constrained to be monotonic.
Calibration fitting and evaluation.
We follow a standard post-hoc calibration procedure to avoid test-set leakage
[
27
,
14
,
13
]
. For each subject model, the classifier is trained using the training split. We then fit each calibrator using held-out validation predictions and their corresponding correctness labels. After fitting, the calibration mapping is fixed and applied once to the test split. All reported calibration metrics and selective-prediction results are computed on the test split, which is never used to train, tune, or select calibration parameters.
III-E
Calibration Metrics
We evaluate calibration effectiveness using metrics that quantify the alignment between predicted uncertainty and actual correctness, assessing how well uncertainty estimates reflect model reliability. These metrics are widely used in prior studies to benchmark calibration performance across domains, offering standardized and interpretable measures of miscalibration
[
27
,
14
,
13
,
11
,
10
,
28
]
.
Expected Calibration Error (ECE)
[
27
]
measures the average deviation between predicted confidence and empirical accuracy across
M
M
bins.
𝐸𝐶𝐸
=
∑
m
=
1
M
|
B
m
|
n
​
|
acc
​
(
B
m
)
−
conf
​
(
B
m
)
|
\mathit{ECE}=\sum_{m=1}^{M}\frac{|B_{m}|}{n}\left|\text{acc}(B_{m})-\text{conf}(B_{m})\right|
(5)
where
B
m
B_{m}
is the set of samples whose confidence falls into the
m
t
​
h
m^{th}
bin,
|
B
m
|
|B_{m}|
is the number of samples in bin
m
m
,
n
n
is the total number of samples,
acc
​
(
B
m
)
\text{acc}(B_{m})
is the empirical accuracy of bin
m
m
, and
conf
​
(
B
m
)
\text{conf}(B_{m})
is the average confidence in bin
m
m
.
Although widely adopted, ECE is sensitive to the choice of binning and may smooth over severe local miscalibration. For uncertainty calibration, we define confidence as (
1
−
1-
uncertainty score) for uncertainty measures where higher values indicate lower confidence (e.g., entropy-based uncertainty). For other metrics where higher values indicate greater confidence, we directly use the uncertainty score.
Maximum Expected Calibration Error (MECE):
[
27
]
captures the worst-case miscalibration, addressing binning artifacts in ECE:
𝑀𝐸𝐶𝐸
=
max
m
∈
M
⁡
|
acc
​
(
B
m
)
−
conf
​
(
B
m
)
|
\mathit{MECE}=\max_{m\in M}\left|\text{acc}(B_{m})-\text{conf}(B_{m})\right|
(6)
Unlike ECE, MECE highlights peak miscalibration, making it more suitable when even small pockets of overconfidence can be risky. However, it is highly sensitive to outliers.
Brier Score (BS)
evaluates the mean squared error between predicted probabilities and ground truth labels:
B
=
1
|
T
|
​
∑
i
=
1
|
T
|
(
p
^
i
−
(
✓
⁡
(
y
i
)
)
)
2
B=\frac{1}{|T|}\sum_{i=1}^{|T|}(\hat{p}_{i}-(\checkmark(y_{i})))^{2}
(7)
where
|
T
|
|T|
is the total number of samples,
p
^
i
\hat{p}_{i}
is the predicted probability for sample
i
i
,
(
✓
⁡
(
y
i
)
)
(\checkmark(y_{i}))
is an indicator function that is 1 if the prediction is correct, 0 otherwise. It penalizes both miscalibration and incorrect predictions, but it cannot disentangle whether errors stem from poor uncertainty estimates or low accuracy.
To support selective prediction we use the
area under the accuracy-rejection curve (AUARC)
[
45
]
, which is specifically designed for uncertainty estimation, which plots how the accuracy on the accepted samples changes as more low-confidence answers are rejected. The area under it indicates the uncertainty estimation’s ability to maintain high accuracy when low-confidence answers are rejected. AUARC measures how well uncertainty scores support abstention but can exaggerate performance when abstention primarily removes trivial, highly uncertain failures.
We conducted all our experiments on a server equipped with an Intel(R) Xeon(R) w5-2545 CPU and two RTX 4000 Ada GPUs. Due to space limitation complete tables associated on AUARC values are provided in our project website.
(a)
Uncalibrated
(b)
Temperature Scaling
(c)
Platt Scaling
(d)
Isotonic Regression
Fig. 1
:
ECE values on defect prediction task for CodeBERT (CB), RoBERT (RB), GraphCodeBERT (GCB), StarCoder (SC), DeepSeek (DS), QwenCoder (QC), and CodeLlama (CL) models
(a)
Uncalibrated
(b)
Temperature Scaling
(c)
Platt Scaling
(d)
Isotonic Regression
Fig. 2
:
ECE values on vulnerability detection task for CodeBERT (CB), RoBERT (RB), GraphCodeBERT (GCB), StarCoder (SC), DeepSeek (DS), QwenCoder (QC), and CodeLlama (CL) models
IV
Empirical Study
This empirical study addresses two objectives. First, it evaluates whether commonly used prediction scores and uncertainty estimates provide effective signals for
selective prediction
[
16
]
in code classification. Second, it examines whether standard post-hoc calibration methods improve the usefulness of these signals for selective prediction.
To this end, we conduct experiments on deep code models for two software engineering tasks: vulnerability detection and defect prediction. Using the experimental setup described in Section
III
, we investigate the following research questions:
RQ1.
How well do existing uncertainty metrics reflect prediction reliability and calibration quality in deep code models?
RQ2.
Can existing calibration techniques improve the effectiveness of these measurement metrics in determining input appropriateness?
RQ3.
Do commonly used calibration metrics reliably indicate an uncertainty measure’s ability to assess prediction success in deep learning models?
IV-A
Uncalibrated Reliability of Uncertainty Measures
Tables
II
–
V
and Figures
1(a)
–
2(a)
summarize the
uncalibrated
reliability of uncertainty signals across our subjects. In software engineering settings, an uncertainty signal can remain
useful for ranking
while being
unsafe as a probability
. This gap is large, task-dependent, and directly relevant to deployment decisions.
Uncalibrated uncertainty is not a dependable measure in SE tasks.
Before calibration, the numeric mismatch between confidence and correctness is substantial. In vulnerability detection, ECE ranges from
1.79% to 48.65%
while in defect prediction it is even larger, reaching
72.13%
. The same pattern appears when MECE rises to
65.8
, while BS is consistently lower for probability-based confidence scores (around
0.225
0.225
–
0.244
0.244
on vulnerability detection and around
0.125
0.125
–
0.157
0.157
on defect prediction) than for information-theoretic signals (
0.360
0.360
–
0.397
0.397
and
0.460
0.460
–
0.699
0.699
, respectively). This is not merely generic neural overconfidence. In code tasks, correctness often depends on semantics, hidden interactions, and long-range relations, whereas models can still assign high confidence from lexical or syntactic regularities. Consequently, score magnitude often reflects
pattern familiarity
rather than true correctness.
Ranking reliability and probability reliability diverge in code modeling.
Despite severe miscalibration, AUARC remains relatively strong for many signals:
0.681–0.754
in vulnerability detection and
0.885–0.927
in defect prediction. For example, in vulnerability detection, CodeBERT attains AUARC near
0.754
across several signals even when ECE varies from
11.91%
to above
35%
. This shows that, for SE tasks, a signal may still separate easy from risky inputs well enough for abstention while failing to quantify how trustworthy the retained predictions actually are. Hence,
good rejection behavior does not imply trustworthy probabilities
. This distinction matters in practice when ranking can help triage predictions for review, but uncalibrated confidence is unsafe for threshold-based automation.
No uncertainty measurement metric is generalizable across SE tasks and code models.
No single uncertainty measure is consistently reliable across both tasks and all architectures. The same metric can be well behaved for one model yet highly unreliable for another, and this pattern changes between vulnerability detection and defect prediction. Information-theoretic measures illustrate this most clearly as they often incur substantially higher ECE and BS, and weaker pre-calibration AUARC, than confidence-based alternatives. This suggests that uncertainty behavior is shaped by
task-specific code distributions
,
label ambiguity
, and
model-specific inductive biases
, rather than by the metric alone. Therefore, there is no universally reliable off-the-shelf uncertainty score for SE deployment.
Takeaway.
Existing uncertainty measures in deep code models are best viewed as
task-specific ranking heuristics, not trustworthy probabilities
. Their failure arises from SE-specific error structure—semantic ambiguity, overlap in surface patterns across classes, noisy supervision, and missed long-range program dependencies—which weakens the link between confidence magnitude and correctness. For practitioners, the implication is straightforward:
do not interpret uncalibrated confidence as reliability
. Instead, validate each signal per task and model, and report
both
calibration metrics and AUARC before using uncertainty to support acceptance, deferral, or review prioritization.
(a)
Reliability plot of uncalibrated model
(b)
Reliability plot showing bucket collapse with Iso.R
Fig. 3
:
Example of bucket collapse for MI after Iso.R on defect prediction with DeepSeek.
IV-B
Effectiveness of Calibration Techniques on Uncertainty Metrics
Tables
II
–
V
and Figures
1(b)
–
1(d)
and
2(b)
–
2(d)
summarize the effect of post-hoc calibration on uncertainty signals. For SE tasks, calibration often improves
probability alignment
without improving
decision utility
. That is, a calibrated score may look numerically better while remaining no more useful for deciding which predictions to trust, defer, or inspect.
Monotone calibration preserves ordering but changes probability interpretation.
This distinction is important when interpreting the effect of calibration on selective prediction. Let
s
i
s_{i}
and
s
j
s_{j}
denote the scores used to rank predictions for rejection, and let
f
f
be a strictly monotone calibration map. Then
s
i
>
s
j
s_{i}>s_{j}
if and only if
f
⁡
(
s
i
)
>
f
⁡
(
s
j
)
f(s_{i})>f(s_{j})
. Therefore, at any fixed coverage level, the set of accepted predictions is unchanged by applying
f
f
. Ranking-based selective-prediction metrics such as AUARC are consequently invariant to strictly monotone calibration, except for implementation-level effects such as ties, non-strict mappings, or numerical precision. Calibration metrics and selective-prediction metrics should therefore be interpreted as measuring different properties: ECE and BS assess probability validity, whereas AUARC assesses the quality of the accept–defer ranking.
Post-hoc calibration improves probability alignment without necessarily improving failure separation.
Across models and tasks, PS and Iso.R usually reduce ECE sharply. In vulnerability detection, PS often brings ECE down to
0.403%–8.587%
, while Iso.R frequently reaches
0.880%–4.223%
. In defect prediction, both methods commonly reduce ECE to
below 10%
, and in several cases to
0.10%–0.95%
. In contrast, TS is unstable and can even worsen calibration; for example, Vanilla confidence for CodeBERT increases from
14.596% to 20.314%
in vulnerability detection and from
9.70% to 11.38%
in defect prediction. This behavior is important in SE because code-model errors are not homogeneous, thus they arise from semantically subtle cases, subgroup-specific patterns, and long-range dependencies. A single global remapping can therefore improve average alignment while still missing the error structure that matters in code analysis.
TABLE II
:
MECE values on vulnerability detection task. Each entry shows uncalibrated
→
\rightarrow
best calibrated technique in terms of MECE. Superscripts denote which calibration achieved the best value.
Metric
CodeBERT
RoBERTa
GraphCodeBERT
StarCoder
DeepSeek
QwenCoder
CodeLlama
Vanilla
24.10
→
\rightarrow
12.50
Iso.R
19.00
→
\rightarrow
9.80
PS
25.30
→
\rightarrow
7.10
PS
13.10
→
\rightarrow
13.90
TS
4.00
→
\rightarrow
8.00
TS
11.70
→
\rightarrow
11.80
TS
8.20
→
\rightarrow
8.60
PS
Entropy
19.50
→
\rightarrow
5.40
Iso.R
23.30
→
\rightarrow
8.30
TS
20.20
→
\rightarrow
6.90
PS
21.50
→
\rightarrow
7.50
PS
33.00
→
\rightarrow
2.70
PS
25.70
→
\rightarrow
1.30
PS
28.10
→
\rightarrow
3.90
PS
MI
52.20
→
\rightarrow
2.30
Iso.R
59.50
→
\rightarrow
0.90
Iso.R
51.90
→
\rightarrow
0.40
Iso.R
65.80
→
\rightarrow
2.00
Iso.R
55.40
→
\rightarrow
1.10
Iso.R
64.80
→
\rightarrow
1.10
Iso.R
60.10
→
\rightarrow
0.70
Iso.R
MC
45.70
→
\rightarrow
12.50
Iso.R
49.30
→
\rightarrow
47.90
PS
48.50
→
\rightarrow
83.30
PS
46.30
→
\rightarrow
47.90
TS
46.90
→
\rightarrow
27.60
Iso.R
51.00
→
\rightarrow
16.70
Iso.R
46.30
→
\rightarrow
39.70
Iso.R
RC
44.40
→
\rightarrow
12.50
Iso.R
46.60
→
\rightarrow
49.00
PS
50.30
→
\rightarrow
64.10
PS
45.20
→
\rightarrow
47.80
PS
46.90
→
\rightarrow
27.60
Iso.R
52.30
→
\rightarrow
16.70
Iso.R
45.90
→
\rightarrow
39.70
Iso.R
MCD_sws
15.50
→
\rightarrow
6.80
PS
13.80
→
\rightarrow
10.10
PS
17.10
→
\rightarrow
8.70
PS
13.30
→
\rightarrow
12.40
Iso.R
4.00
→
\rightarrow
7.50
TS
11.50
→
\rightarrow
11.30
TS
8.20
→
\rightarrow
8.10
TS
MCD_pv
36.40
→
\rightarrow
29.80
PS
37.60
→
\rightarrow
18.00
Iso.R
35.40
→
\rightarrow
6.00
Iso.R
62.20
→
\rightarrow
10.30
Iso.R
80.80
→
\rightarrow
11.40
PS
86.80
→
\rightarrow
77.10
TS
37.80
→
\rightarrow
37.90
TS
MCD_bald
46.70
→
\rightarrow
35.00
Iso.R
53.50
→
\rightarrow
16.00
Iso.R
50.40
→
\rightarrow
20.20
Iso.R
51.90
→
\rightarrow
16.30
Iso.R
81.00
→
\rightarrow
24.50
PS
72.50
→
\rightarrow
60.90
TS
37.80
→
\rightarrow
9.00
PS
DE_sws
3.70
→
\rightarrow
9.30
PS
8.00
→
\rightarrow
0.60
PS
5.20
→
\rightarrow
7.30
TS
19.70
→
\rightarrow
11.20
Iso.R
17.30
→
\rightarrow
8.00
Iso.R
15.80
→
\rightarrow
16.90
PS
11.10
→
\rightarrow
6.00
TS
DE_pv
36.40
→
\rightarrow
19.30
PS
37.90
→
\rightarrow
0.60
PS
35.00
→
\rightarrow
0.10
PS
100.00
→
\rightarrow
14.70
Iso.R
100.00
→
\rightarrow
49.50
Iso.R
54.40
→
\rightarrow
6.80
Iso.R
39.50
→
\rightarrow
4.70
PS
DE_bald
52.60
→
\rightarrow
21.20
Iso.R
52.80
→
\rightarrow
14.90
Iso.R
59.90
→
\rightarrow
38.50
PS
36.90
→
\rightarrow
37.50
TS
100.00
→
\rightarrow
19.00
PS
42.80
→
\rightarrow
7.80
Iso.R
32.20
→
\rightarrow
11.30
PS
TABLE III
:
MECE values on defect prediction task. Each entry shows uncalibrated
→
\rightarrow
best calibrated technique in terms of MECE. Superscripts denote which calibration achieved the best value.
Metric
CodeBERT
RoBERTa
GraphCodeBERT
StarCoder
DeepSeek
QwenCoder
CodeLlama
Vanilla
37.69
→
\rightarrow
13.10
Iso.R
20.72
→
\rightarrow
21.94
TS
20.72
→
\rightarrow
21.94
TS
29.60
→
\rightarrow
5.65
TS
29.14
→
\rightarrow
24.29
Iso.R
29.14
→
\rightarrow
17.55
PS
9.06
→
\rightarrow
14.06
Iso.R
Entropy
49.02
→
\rightarrow
11.76
Iso.R
49.34
→
\rightarrow
41.08
PS
49.34
→
\rightarrow
41.08
PS
27.95
→
\rightarrow
18.88
TS
30.82
→
\rightarrow
20.90
TS
29.39
→
\rightarrow
9.47
Iso.R
28.22
→
\rightarrow
13.77
Iso.R
MI
88.23
→
\rightarrow
0.10
Iso.R
88.35
→
\rightarrow
0.21
Iso.R
88.35
→
\rightarrow
0.21
Iso.R
89.51
→
\rightarrow
0.25
Iso.R
92.24
→
\rightarrow
0.94
Iso.R
92.14
→
\rightarrow
0.18
Iso.R
91.80
→
\rightarrow
16.13
PS
MC
42.96
→
\rightarrow
7.64
Iso.R
35.63
→
\rightarrow
10.56
Iso.R
35.63
→
\rightarrow
10.56
Iso.R
37.93
→
\rightarrow
6.17
Iso.R
38.73
→
\rightarrow
3.70
Iso.R
38.37
→
\rightarrow
12.23
Iso.R
35.21
→
\rightarrow
2.40
Iso.R
RC
35.68
→
\rightarrow
27.78
Iso.R
34.42
→
\rightarrow
8.47
Iso.R
34.42
→
\rightarrow
8.47
Iso.R
36.68
→
\rightarrow
3.15
Iso.R
38.11
→
\rightarrow
6.69
Iso.R
37.82
→
\rightarrow
13.19
Iso.R
36.33
→
\rightarrow
3.22
Iso.R
MCD_sws
48.87
→
\rightarrow
23.55
PS
14.98
→
\rightarrow
25.43
TS
14.98
→
\rightarrow
25.43
TS
29.27
→
\rightarrow
5.74
TS
28.90
→
\rightarrow
24.60
Iso.R
28.96
→
\rightarrow
7.92
Iso.R
11.60
→
\rightarrow
16.55
PS
MCD_pv
15.11
→
\rightarrow
4.57
Iso.R
17.36
→
\rightarrow
2.39
Iso.R
17.36
→
\rightarrow
2.39
Iso.R
82.70
→
\rightarrow
58.74
PS
100.00
→
\rightarrow
4.83
Iso.R
71.51
→
\rightarrow
16.67
Iso.R
49.03
→
\rightarrow
44.47
PS
MCD_bald
26.07
→
\rightarrow
27.99
TS
43.72
→
\rightarrow
41.06
PS
43.72
→
\rightarrow
41.06
PS
27.75
→
\rightarrow
18.71
TS
30.01
→
\rightarrow
24.45
TS
27.51
→
\rightarrow
15.93
Iso.R
27.82
→
\rightarrow
11.42
Iso.R
DE_sws
26.54
→
\rightarrow
36.65
TS
49.91
→
\rightarrow
2.20
PS
49.91
→
\rightarrow
2.20
PS
13.18
→
\rightarrow
1.77
Iso.R
16.96
→
\rightarrow
3.62
PS
16.69
→
\rightarrow
16.01
Iso.R
18.26
→
\rightarrow
1.93
Iso.R
DE_pv
14.90
→
\rightarrow
3.87
PS
17.49
→
\rightarrow
0.17
PS
17.49
→
\rightarrow
0.17
PS
19.04
→
\rightarrow
17.79
Iso.R
94.10
→
\rightarrow
30.00
Iso.R
100.00
→
\rightarrow
81.10
PS
100.00
→
\rightarrow
50.00
Iso.R
DE_bald
53.11
→
\rightarrow
17.84
Iso.R
74.70
→
\rightarrow
0.18
PS
74.70
→
\rightarrow
0.18
PS
49.48
→
\rightarrow
34.39
TS
47.87
→
\rightarrow
13.14
Iso.R
50.45
→
\rightarrow
16.67
Iso.R
52.64
→
\rightarrow
40.47
TS
Better calibration scores rarely imply better selective prediction.
Despite large reductions in ECE and BS, selective prediction performance usually improves only marginally. In vulnerability detection, CodeBERT remains near
0.754
across several calibration settings even when ECE falls to roughly
2–3%
. In defect prediction, AUARC for many metrics remains around
0.886–0.928
even when ECE drops close to
1%
. Thus, calibration can improve the
numerical meaning
of a score without improving its
ability to separate correct from incorrect predictions
. For SE practitioners, this is the key warning when a lower ECE does not mean the model has become safer to automate. It may still retain high-confidence wrong predictions, which are precisely the failures that matter most in vulnerability screening and defect triage.
The main limitation of post-hoc calibration is that it improves average probability alignment without correcting the error distribution that governs which code predictions remain risky after thresholding.
TS, PS, and Iso.R are all optimized to improve global agreement between predicted scores and observed correctness, rather than to separate correct from incorrect predictions among the instances the model is most likely to retain. This becomes explicit in defect prediction, where Iso.R reduces ECE for MI-based scores to
0.10%–0.95%
, yet AUARC remains only
0.772–0.843
, well below the
0.915–0.928
reached by stronger confidence-based signals. The root cause is particularly relevant in code tasks where model mistakes are often concentrated in semantically hard or distributionally sparse cases, whereas post-hoc calibration learns a single monotone mapping over the full score range. As a result, calibration can fix
score scale
while leaving
high-confidence errors interleaved with correct predictions
. Therefore, calibration and uncertainty must be treated jointly in SE, not as independent post-processing steps.
Takeaway.
Standard post-hoc calibration techniques improve numeric calibration in deep code models, but they do
not
reliably improve practical reliability for SE deployment. Their failure is not incidental as it follows from a mismatch between what calibration optimizes is the global alignment and what SE applications require is safe trust decisions in the high-confidence region. For practitioners, the implication is to
use calibration to refine probability interpretation, not to assume better abstention behavior
. A calibrated uncertainty score should be trusted for acceptance or deferral after verifying that selective prediction metrics also improve.
TABLE IV
:
BS values on defect prediction. Each entry shows uncalibrated
→
\rightarrow
best calibrated technique in terms of BS. Superscripts denote which calibration achieved the best value.
Metric
CodeBERT
RoBERTa
GraphCodeBERT
StarCoder
DeepSeek
QwenCoder
CodeLlama
Vanilla
24.41
→
\rightarrow
21.73
Iso.R
22.98
→
\rightarrow
22.39
Iso.R
23.96
→
\rightarrow
21.65
Iso.R
23.80
→
\rightarrow
23.42
Iso.R
22.66
→
\rightarrow
22.74
Iso.R
23.11
→
\rightarrow
22.83
Iso.R
22.51
→
\rightarrow
22.50
Iso.R
Entropy
23.67
→
\rightarrow
21.72
Iso.R
25.98
→
\rightarrow
22.37
PS
23.67
→
\rightarrow
21.66
Iso.R
27.52
→
\rightarrow
23.37
PS
28.51
→
\rightarrow
22.62
PS
27.81
→
\rightarrow
22.75
PS
27.55
→
\rightarrow
22.35
PS
MI
36.72
→
\rightarrow
21.76
PS
37.42
→
\rightarrow
22.22
PS
36.06
→
\rightarrow
21.54
PS
39.44
→
\rightarrow
23.29
PS
39.66
→
\rightarrow
22.64
PS
36.99
→
\rightarrow
22.74
PS
37.64
→
\rightarrow
22.29
PS
MC
27.50
→
\rightarrow
21.73
Iso.R
32.74
→
\rightarrow
22.39
Iso.R
27.37
→
\rightarrow
21.65
Iso.R
33.73
→
\rightarrow
23.43
Iso.R
37.62
→
\rightarrow
22.74
Iso.R
34.86
→
\rightarrow
22.83
Iso.R
34.03
→
\rightarrow
22.50
Iso.R
RC
26.44
→
\rightarrow
21.73
Iso.R
29.21
→
\rightarrow
22.39
Iso.R
26.19
→
\rightarrow
21.65
Iso.R
29.19
→
\rightarrow
23.43
Iso.R
31.94
→
\rightarrow
22.74
Iso.R
30.18
→
\rightarrow
22.83
Iso.R
29.00
→
\rightarrow
22.50
Iso.R
MCD_sws
22.99
→
\rightarrow
21.58
Iso.R
22.68
→
\rightarrow
22.43
Iso.R
22.98
→
\rightarrow
21.56
Iso.R
23.79
→
\rightarrow
23.41
Iso.R
22.66
→
\rightarrow
22.75
Iso.R
23.10
→
\rightarrow
22.87
Iso.R
22.52
→
\rightarrow
22.56
Iso.R
MCD_pv
36.49
→
\rightarrow
21.86
Iso.R
37.66
→
\rightarrow
22.74
Iso.R
35.47
→
\rightarrow
21.53
Iso.R
36.22
→
\rightarrow
23.60
Iso.R
39.66
→
\rightarrow
23.78
Iso.R
36.42
→
\rightarrow
23.09
Iso.R
37.87
→
\rightarrow
23.17
Iso.R
MCD_bald
35.33
→
\rightarrow
21.57
Iso.R
43.75
→
\rightarrow
22.36
Iso.R
35.91
→
\rightarrow
21.54
Iso.R
37.22
→
\rightarrow
24.13
Iso.R
39.65
→
\rightarrow
24.00
Iso.R
36.37
→
\rightarrow
23.25
Iso.R
37.84
→
\rightarrow
23.57
Iso.R
DE_sws
21.71
→
\rightarrow
21.72
Iso.R
24.18
→
\rightarrow
23.47
Iso.R
21.40
→
\rightarrow
21.49
PS
24.17
→
\rightarrow
23.63
Iso.R
23.40
→
\rightarrow
23.43
Iso.R
23.69
→
\rightarrow
23.16
Iso.R
23.14
→
\rightarrow
23.16
Iso.R
DE_pv
36.49
→
\rightarrow
23.32
Iso.R
37.91
→
\rightarrow
23.55
PS
35.32
→
\rightarrow
22.79
Iso.R
34.62
→
\rightarrow
24.01
Iso.R
32.36
→
\rightarrow
24.07
PS
31.61
→
\rightarrow
23.17
Iso.R
32.79
→
\rightarrow
23.53
PS
DE_bald
46.08
→
\rightarrow
21.75
Iso.R
27.33
→
\rightarrow
23.47
Iso.R
47.38
→
\rightarrow
21.44
Iso.R
35.24
→
\rightarrow
24.20
PS
33.22
→
\rightarrow
24.01
PS
32.19
→
\rightarrow
23.50
Iso.R
32.99
→
\rightarrow
23.54
PS
TABLE V
:
BS values on vulnerability detection. Each entry shows uncalibrated
→
\rightarrow
best calibrated technique in terms of BS. Superscripts denote which calibration achieved the best value.
Metric
CodeBERT
RoBERTa
GraphCodeBERT
StarCoder
DeepSeek
QwenCoder
CodeLlama
Vanilla
12.50
→
11.30
I
​
s
​
o
.
R
12.50\rightarrow 11.30^{Iso.R}
13.30
→
12.70
I
​
s
​
o
.
R
13.30\rightarrow 12.70^{Iso.R}
13.30
→
12.70
I
​
s
​
o
.
R
13.30\rightarrow 12.70^{Iso.R}
15.70
→
15.50
I
​
s
​
o
.
R
¯
\underline{15.70\rightarrow 15.50^{Iso.R}}
13.00
→
13.00
T
​
S
/
I
​
s
​
o
.
R
13.00\rightarrow 13.00^{TS/Iso.R}
13.70
→
13.70
T
​
S
/
I
​
s
​
o
.
R
¯
\underline{13.70\rightarrow 13.70^{TS/Iso.R}}
13.50
→
13.50
I
​
s
​
o
.
R
¯
\underline{13.50\rightarrow 13.50^{Iso.R}}
Entropy
11.30
→
11.30
T
​
S
/
I
​
s
​
o
.
R
11.30\rightarrow 11.30^{TS/Iso.R}
12.90
→
12.70
T
​
S
/
I
​
s
​
o
.
R
12.90\rightarrow 12.70^{TS/Iso.R}
12.90
→
12.70
T
​
S
/
I
​
s
​
o
.
R
12.90\rightarrow 12.70^{TS/Iso.R}
18.30
→
15.60
I
​
s
​
o
.
R
18.30\rightarrow 15.60^{Iso.R}
15.30
→
13.00
I
​
s
​
o
.
R
15.30\rightarrow 13.00^{Iso.R}
16.70
→
13.90
I
​
s
​
o
.
R
16.70\rightarrow 13.90^{Iso.R}
17.40
→
13.60
I
​
s
​
o
.
R
17.40\rightarrow 13.60^{Iso.R}
MI
69.90
→
13.20
I
​
s
​
o
.
R
69.90\rightarrow 13.20^{Iso.R}
62.10
→
14.70
I
​
s
​
o
.
R
62.10\rightarrow 14.70^{Iso.R}
62.10
→
14.70
I
​
s
​
o
.
R
62.10\rightarrow 14.70^{Iso.R}
46.00
→
18.30
I
​
s
​
o
.
R
46.00\rightarrow 18.30^{Iso.R}
53.70
→
16.40
I
​
s
​
o
.
R
53.70\rightarrow 16.40^{Iso.R}
50.50
→
17.20
I
​
s
​
o
.
R
50.50\rightarrow 17.20^{Iso.R}
48.70
→
17.30
I
​
s
​
o
.
R
48.70\rightarrow 17.30^{Iso.R}
MC
12.20
→
11.30
I
​
s
​
o
.
R
12.20\rightarrow 11.30^{Iso.R}
13.70
→
12.70
P
​
S
/
I
​
s
​
o
.
R
13.70\rightarrow 12.70^{PS/Iso.R}
13.70
→
12.70
P
​
S
/
I
​
s
​
o
.
R
13.70\rightarrow 12.70^{PS/Iso.R}
18.30
→
15.70
T
​
S
/
I
​
s
​
o
.
R
18.30\rightarrow 15.70^{TS/Iso.R}
15.20
→
13.00
I
​
s
​
o
.
R
15.20\rightarrow 13.00^{Iso.R}
16.90
→
13.80
I
​
s
​
o
.
R
16.90\rightarrow 13.80^{Iso.R}
17.20
→
13.80
T
​
S
/
I
​
s
​
o
.
R
17.20\rightarrow 13.80^{TS/Iso.R}
RC
12.70
→
11.40
I
​
s
​
o
.
R
12.70\rightarrow 11.40^{Iso.R}
13.80
→
12.70
T
​
S
/
I
​
s
​
o
.
R
13.80\rightarrow 12.70^{TS/Iso.R}
13.80
→
12.70
T
​
S
/
I
​
s
​
o
.
R
13.80\rightarrow 12.70^{TS/Iso.R}
16.90
→
15.70
I
​
s
​
o
.
R
16.90\rightarrow 15.70^{Iso.R}
14.10
→
13.10
I
​
s
​
o
.
R
14.10\rightarrow 13.10^{Iso.R}
14.90
→
13.90
I
​
s
​
o
.
R
14.90\rightarrow 13.90^{Iso.R}
14.80
→
13.90
I
​
s
​
o
.
R
14.80\rightarrow 13.90^{Iso.R}
MCD_sws
11.80
→
11.10
I
​
s
​
o
.
R
11.80\rightarrow 11.10^{Iso.R}
12.90
→
12.60
P
​
S
/
I
​
s
​
o
.
R
12.90\rightarrow 12.60^{PS/Iso.R}
12.90
→
12.60
P
​
S
/
I
​
s
​
o
.
R
12.90\rightarrow 12.60^{PS/Iso.R}
15.70
→
15.50
I
​
s
​
o
.
R
¯
\underline{15.70\rightarrow 15.50^{Iso.R}}
13.00
→
13.00
T
​
S
/
I
​
s
​
o
.
R
13.00\rightarrow 13.00^{TS/Iso.R}
13.70
→
13.70
T
​
S
/
I
​
s
​
o
.
R
¯
\underline{13.70\rightarrow 13.70^{TS/Iso.R}}
13.50
→
13.50
I
​
s
​
o
.
R
¯
\underline{13.50\rightarrow 13.50^{Iso.R}}
MCD_pv
15.20
→
11.20
I
​
s
​
o
.
R
15.20\rightarrow 11.20^{Iso.R}
17.50
→
12.60
I
​
s
​
o
.
R
17.50\rightarrow 12.60^{Iso.R}
17.50
→
12.60
I
​
s
​
o
.
R
17.50\rightarrow 12.60^{Iso.R}
21.60
→
17.50
I
​
s
​
o
.
R
21.60\rightarrow 17.50^{Iso.R}
19.60
→
14.20
I
​
s
​
o
.
R
19.60\rightarrow 14.20^{Iso.R}
19.40
→
15.10
I
​
s
​
o
.
R
19.40\rightarrow 15.10^{Iso.R}
20.40
→
15.30
I
​
s
​
o
.
R
20.40\rightarrow 15.30^{Iso.R}
MCD_bald
11.50
→
11.00
T
​
S
¯
\underline{11.50\rightarrow 11.00^{TS}}
13.60
→
12.50
T
​
S
/
I
​
s
​
o
.
R
¯
\underline{13.60\rightarrow 12.50^{TS/Iso.R}}
13.60
→
12.50
T
​
S
/
I
​
s
​
o
.
R
¯
\underline{13.60\rightarrow 12.50^{TS/Iso.R}}
18.30
→
15.60
I
​
s
​
o
.
R
18.30\rightarrow 15.60^{Iso.R}
15.30
→
12.90
I
​
s
​
o
.
R
¯
\underline{15.30\rightarrow 12.90^{Iso.R}}
16.70
→
13.90
I
​
s
​
o
.
R
16.70\rightarrow 13.90^{Iso.R}
17.40
→
13.60
I
​
s
​
o
.
R
17.40\rightarrow 13.60^{Iso.R}
DE_sws
12.40
→
12.30
I
​
s
​
o
.
R
12.40\rightarrow 12.30^{Iso.R}
39.60
→
14.70
P
​
S
/
I
​
s
​
o
.
R
39.60\rightarrow 14.70^{PS/Iso.R}
39.60
→
14.70
P
​
S
/
I
​
s
​
o
.
R
39.60\rightarrow 14.70^{PS/Iso.R}
17.70
→
17.00
T
​
S
/
I
​
s
​
o
.
R
17.70\rightarrow 17.00^{TS/Iso.R}
16.70
→
14.90
I
​
s
​
o
.
R
16.70\rightarrow 14.90^{Iso.R}
17.30
→
16.10
T
​
S
/
I
​
s
​
o
.
R
17.30\rightarrow 16.10^{TS/Iso.R}
18.00
→
15.80
P
​
S
/
I
​
s
​
o
.
R
18.00\rightarrow 15.80^{PS/Iso.R}
DE_pv
15.30
→
12.60
I
​
s
​
o
.
R
15.30\rightarrow 12.60^{Iso.R}
17.70
→
14.60
P
​
S
17.70\rightarrow 14.60^{PS}
17.70
→
14.60
P
​
S
17.70\rightarrow 14.60^{PS}
20.70
→
17.20
I
​
s
​
o
.
R
20.70\rightarrow 17.20^{Iso.R}
16.70
→
15.70
I
​
s
​
o
.
R
16.70\rightarrow 15.70^{Iso.R}
18.50
→
16.50
I
​
s
​
o
.
R
18.50\rightarrow 16.50^{Iso.R}
18.00
→
16.90
I
​
s
​
o
.
R
18.00\rightarrow 16.90^{Iso.R}
DE_bald
15.60
→
12.40
I
​
s
​
o
.
R
15.60\rightarrow 12.40^{Iso.R}
38.10
→
14.70
P
​
S
/
I
​
s
​
o
.
R
38.10\rightarrow 14.70^{PS/Iso.R}
38.10
→
14.70
P
​
S
/
I
​
s
​
o
.
R
38.10\rightarrow 14.70^{PS/Iso.R}
29.90
→
16.90
I
​
s
​
o
.
R
29.90\rightarrow 16.90^{Iso.R}
27.50
→
15.00
I
​
s
​
o
.
R
27.50\rightarrow 15.00^{Iso.R}
29.10
→
16.00
I
​
s
​
o
.
R
29.10\rightarrow 16.00^{Iso.R}
33.20
→
15.80
P
​
S
/
I
​
s
​
o
.
R
33.20\rightarrow 15.80^{PS/Iso.R}
IV-C
Effectiveness of Calibration Metrics in Detecting Prediction Success
Tables
II
–
V
and Figures
1(b)
–
1(d)
and
2(b)
–
2(d)
summarize how ECE, MECE, BS, and AUARC evaluate prediction reliability after uncertainty estimation and calibration. These metrics do
not
provide interchangeable evidence in deep code models, however, they prioritize different properties of reliability, can rank the same model–metric pair differently, and can therefore support conflicting deployment decisions. In SE tasks, metric choice directly influences which predictions are trusted, deferred, or subjected to further review.
Metric disagreement is consequential in SE because it changes both model assessment and trust decisions.
The four metrics reward different properties of a score. ECE measures average score–frequency alignment, MECE emphasizes the largest local mismatch, BS combines probability error with class separation, and AUARC evaluates ranking quality for acceptance–rejection decisions. As a result, the same uncertainty signal can appear strong under one metric and weak under another. This effect is especially important in code tasks, where reliability is used operationally rather than descriptively. Practitioners do not only need a score that looks calibrated on average, but they need a score that helps identify which predictions remain safe to retain. Therefore, disagreement among metrics is itself a practical risk.
ECE and MECE can misrepresent reliability in code models because both depend on how scores are distributed across bins.
ECE can drop sharply without improving selective prediction. For example, in vulnerability detection, CodeBERT’s entropy ECE decreases from
12.931%
to about
2.194%
after Iso.R, while AUARC stays near
0.754
. In defect prediction, MI for CodeBERT drops from
72.13%
to
0.10%
after Iso.R, yet its AUARC remains well below the strongest uncertainty signals. MECE is even less stable because it is determined by the worst populated bin and can be dominated by sparse score regions. Thus, in code models with skewed confidence distributions, both ECE and MECE can change substantially even when the set of risky accepted predictions remains largely the same. This makes them useful as diagnostics of score validity, but insufficient for deciding whether a model is safer to use.
Bucket collapse is a mechanism by which calibration can improve aggregate metrics while weakening threshold-based decisions.
Figure
3
illustrates this effect for Iso.R. Unlike TS and PS, Iso.R learns a non-strict monotone step function, so multiple distinct uncertainty scores can be mapped to the same calibrated value. This can improve bin-level calibration because each bucket is assigned an empirical correctness rate, but it also reduces score resolution. Predictions that were separable before calibration can become indistinguishable after calibration. This does not reverse the ordering across different buckets, but it removes the ordering within each collapsed bucket. As a result, selective prediction can become unstable when an accept–defer threshold falls inside a large bucket: the retained set may then depend on arbitrary tie-breaking rather than meaningful uncertainty differences. Thus, bucket collapse is not merely a visual effect; it indicates reduced resolution in the calibrated score space. While Iso.R does not reverse the ordering across buckets, it can eliminate within-bucket distinctions that selective prediction depends on, especially when an operating threshold intersects a large bucket.
BS and AUARC answer different decision questions and neither is sufficient alone.
BS can improve through global rescaling even when the score does not better separate correct from incorrect predictions. In vulnerability detection, calibrated BS values often concentrate near
0.215–0.236
across many signals, even though AUARC remains essentially unchanged. In defect prediction, MI-based BS improves substantially after calibration, but AUARC still trails the strongest confidence-based measures. AUARC, in contrast, is appropriate for evaluating selective prediction, yet it is largely insensitive to whether probabilities are numerically valid. Hence, BS may overstate reliability gains for deployment, while AUARC may understate whether the probabilities themselves are interpretable. In SE, these are distinct requirements where AUARC governs
decision quality
, the BS governs
probability meaning
.
Code models require joint metric interpretation because reliability failures are concentrated in the retained region.
Figure
4
provides an operating-point view of accepted-set risk. For a rejection rate
r
r
, the retained coverage is
1
−
r
1-r
, and the accepted-set error rate is
1
−
Acc
⁡
(
r
)
1-\mathrm{Acc}(r)
, where
Acc
⁡
(
r
)
\mathrm{Acc}(r)
is the accuracy of the retained predictions. Thus, the curve does not only summarize ranking quality; it also shows the residual risk under different accept–defer policies. The key observation is that calibration changes the numerical scale of scores but does not substantially change the attainable risk–coverage tradeoff. In other words, after calibration, a practitioner may obtain better probability alignment while the same risky predictions remain in the accepted set at comparable coverage levels. The curves also become jagged at high rejection because decisions depend on a small retained subset, where minor ranking errors or score ties can determine which predictions survive thresholding.
Takeaway.
ECE, MECE, BS, and AUARC should not be interpreted as competing substitutes, but as complementary views of different reliability properties. Their disagreement is particularly important in SE because it affects three levels:
model comparison
depicts which code model appears most reliable,
decision support
depicts which predictions are trusted or deferred, and
metric interpretation
depicts whether reliability refers to probability validity or selective utility. For practitioners, the implication is that
no single metric should be used to justify deployment claims
. ECE and MECE should be treated as calibration diagnostics, AUARC should be used for trust/defer decisions, and conclusions about reliability should be drawn only from their joint behavior.
(a)
AUARC curve on uncalibrated model
(b)
AUARC curve after applying PS
Fig. 4
:
Accuracy-rejection curve for vulnerability detection task on CodeLlama model before and after applying PS.
IV-D
Summary of Findings
Across the three RQs, our results show that uncertainty reliability in deep code models cannot be characterized by a single metric. First, uncertainty scores can provide useful rankings for rejection while remaining poorly calibrated as probabilities. Second, post-hoc calibration can substantially improve score validity, as measured by ECE, MECE, or BS, without materially changing ranking-based selective-prediction behavior. Third, calibration metrics and selective-prediction metrics can disagree because they measure different properties of the same score: probability alignment, worst-case local mismatch, squared probability error, and accept–defer ranking quality.
Taken together, these findings indicate that calibration improvement should not be interpreted as a direct proxy for deployment reliability. A score may become numerically better aligned with empirical correctness while still failing to better separate correct from incorrect predictions. This distinction motivates the need to evaluate uncertainty in code models using multiple complementary views rather than relying on any single calibration or rejection metric.
V
Operationalizing Reliability in SE Workflows
Our findings suggest that uncertainty in code models should be operationalized as a mechanism for accept–defer decisions, rather than interpreted as a generic confidence score. In SE workflows, the relevant question is not only whether a model is calibrated on average, but whether its scores can support reliable decisions about which predictions may be trusted, deferred, or routed to additional analysis. This requires evaluating uncertainty under the intended operating regime.
Define accepted-set risk.
Practitioners should first specify the risk associated with predictions that the system will accept. This risk is task-specific. In vulnerability detection, the most harmful accepted error is a vulnerable function predicted as non-vulnerable; in defect prediction, different defect classes may carry different costs. Therefore, uncertainty should be evaluated using accepted-set risk, such as the error rate among retained predictions, class-conditional accepted error, or false-safe rate for security tasks. A model should not be considered reliable solely because its global ECE or Brier score improves.
Select thresholds under an explicit operating target.
Acceptance thresholds should be selected on validation data and evaluated on held-out test data. Given a target risk level, practitioners should choose the threshold that maximizes coverage while keeping the validation accepted-set risk below the desired limit. The selected threshold should then be applied to the test set without further tuning. This procedure makes the reliability claim operational: the model is not simply better calibrated, but supports a specific accept–defer policy at a measurable coverage and risk level.
Separate probability validity from selective-prediction quality.
Calibration and selective prediction should be used for different purposes. Calibration improves the interpretation of scores as correctness probabilities, while rejection curves measure whether scores rank reliable predictions ahead of unreliable ones. Because monotone calibrators preserve ranking, they can improve ECE or Brier score without improving AUARC or changing the composition of the retained set. Thus, a deployment claim should require both probability validity and selective-prediction quality.
Inspect the retained region directly.
Practitioners should examine the subset of predictions that would actually be accepted under the chosen threshold. Flexible calibrators such as isotonic regression may reduce calibration error while collapsing many examples into the same score bucket. Such bucket collapse can make threshold-based routing unstable, because many examples become indistinguishable to the decision policy. We therefore recommend reporting retained-region diagnostics, including accepted-set accuracy, high-confidence error rate, and the fraction of examples assigned to large calibrated buckets.
Implication for SE research and practice.
Uncertainty evaluation in SE should report three complementary dimensions: calibration quality, selective-prediction quality, and retained-region risk. Calibration metrics such as ECE and Brier score describe probability validity; rejection curves describe whether uncertainty supports accept–defer ranking; retained-region diagnostics describe the safety of the predictions that would actually be automated. Together, these measures turn uncertainty from a standalone model score into a software reliability policy for trust, deferral, and review decisions.
VI
Limitations
Our evaluation is limited to two code classification tasks and seven code models. While vulnerability detection and defect prediction are important reliability-sensitive SE settings, the results may not fully generalize to other tasks, larger model families, or different deployment environments. We also do not study code generation, where uncertainty must account for token-level behavior, sequence-level correctness, decoding dynamics, and error propagation. Finally, our study focuses on post-hoc calibration and selective prediction, rather than training-time uncertainty objectives or deployment factors such as human review effort, latency, and tool-assisted follow-up analysis. These dimensions remain important directions for future work.
VII
Threats to Validity
This section discusses potential threats to validity in our study, categorizing them into internal validity, which pertains to experimental design and methodology, and external validity, which concerns the generalizability of our findings.
Internal Validity:
A potential limitation of our study is the selection of uncertainty metrics and calibration methods. We evaluate 13 techniques
[
18
,
19
,
20
,
21
,
22
,
23
,
24
]
, alongside post-hoc methods such as TS, PS, and Iso.R. While our comparisons systematically assess effectiveness, certain techniques may interact differently with specific model architectures, potentially biasing results. Further validation with additional calibration methods is needed to ensure the robustness of our conclusions.
Architectural and pretraining differences can affect how uncertainty is expressed and how well scores calibrate. While we evaluate a diverse set of models up to 7B parameters, broader validation on larger models and additional datasets is needed to confirm generality.
A key challenge in uncertainty calibration is bin imbalance during error computation. Fixed-width binning assumes uniformly distributed confidence scores, which rarely holds for real-world models with skewed uncertainties. We do not evaluate adaptive binning methods (e.g., dynamic or density-based)
[
46
,
47
,
48
]
, although they may better characterize calibration in code models.
External Validity:
The generalizability of our findings focus on experiments on vulnerability detection and defect prediction
[
33
,
34
]
. While these address practical SE challenges, they may not fully extend to tasks like code summarization, bug localization, or automated program repair.
The datasets we use are drawn from specific open-source projects and programming platforms, which may not fully represent all real-world software development scenarios. If these datasets contain inherent biases (e.g., an overrepresentation of certain coding patterns or vulnerabilities), our models may learn spurious correlations, affecting uncertainty estimates. Evaluating our findings on more diverse datasets, including proprietary and industry-scale codebases, would provide stronger external validation.
Real-world deployment considerations pose a challenge. While our study evaluates uncertainty calibration in an offline experimental setting, actual deployment scenarios introduce additional factors such as concept or data distribution shifts, and adversarial code modifications. Since models in production environments continually encounter previously unseen code patterns, their uncertainty estimates degrade over time. Future work should assess how calibration techniques adapt to evolving software landscapes to maintain reliability in dynamic development environments.
Our study takes an initial step in identifying key gaps in existing calibration techniques and outlining research directions to improve decision-making in code analysis. We acknowledge these limitations as future work,
recognizing the need for more adaptive calibration techniques and evaluation strategies that go beyond statistical calibration to enhance practical uncertainty separability.
VIII
Related Work
Pre-trained Code Models.
Pre-trained code models, primarily based on the Transformer architecture, fall into three categories: encoder-only, decoder-only, and encoder-decoder models. Encoder-only models (e.g., CodeBERT , GraphCodeBERT ) focus on code understanding
[
35
,
31
,
36
]
, while decoder-only models (e.g., CodeGPT, GPT-C ) are designed for generative tasks like code completion
[
49
,
50
]
. Encoder-decoder models (e.g., PLBART, CodeT5) integrate both components for comprehensive programming language modeling
[
51
,
52
]
. Pre-trained on large-scale code corpora, these models provide transferable representations that can be fine-tuned for downstream tasks such as defect prediction and vulnerability detection.
Model Calibration.
Model calibration has been extensively studied in NLP
[
53
,
54
]
and CV
[
27
,
48
,
47
,
46
,
28
,
12
]
but remains underexplored for code models. Also, research focused on improving calibration through temperature scaling and platt scaling in for code models
[
13
,
14
]
. Later studies evaluated LLM calibration across NLP tasks, revealing improved calibration with model scaling and pretraining, though some findings remain disputed. Some works investigated uncertainty estimation in code models
[
55
,
56
]
, while others explored LLMs’ self-assessment of correctness
[
57
,
58
]
. Techniques such as Bayesian approaches
[
59
]
, mixup
[
60
]
, and perturbation-based methods
[
61
]
have been explored for calibration improvements. However, calibration in software engineering tasks remains largely uncharted. To our knowledge, this is the first systematic study of uncertainty calibration for selective prediction in code classification.
Our work differs by jointly evaluating calibration quality, selective-prediction quality, and retained-region risk for accept–defer decisions in code classification tasks.
IX
Conclusion
In this paper, we examined the reliability of uncertainty estimates and post-hoc calibration for deep code classification models in vulnerability detection and defect prediction. Across a diverse set of modern code models, we found that standard uncertainty scores and widely used calibration methods can improve aggregate calibration measures yet still leave a critical failure mode unresolved: incorrect predictions that retain high confidence, which undermines selective prediction in deployment settings. These results show that numeric probability alignment alone is not sufficient for trustworthy accept–defer decisions, and that evaluation must account for both calibration quality and abstention behavior.
References
[1]
Z. Tian, J. Chen, and X. Zhang
(2023)
On-the-fly improving performance of deep code models via input denoising
.
arXiv preprint arXiv:2308.09969
.
Cited by:
§I
,
§II
.
[2]
Z. Yang, J. Shi, J. He, and D. Lo
(2022)
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
§I
,
§II
.
[3]
W. Zhang, S. Guo, H. Zhang, Y. Sui, Y. Xue, and Y. Xu
(2023)
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
§I
,
§II
.
[4]
S. Lu, D. Guo, S. Ren, J. Huang, A. Svyatkovskiy, A. Blanco, C. Clement, D. Drain, D. Jiang, D. Tang,
et al.
(2021)
Codexglue: a machine learning benchmark dataset for code understanding and generation
.
arXiv preprint arXiv:2102.04664
.
Cited by:
§I
,
§II
,
§III-B
.
[5]
N. Yefet, U. Alon, and E. Yahav
(2020)
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
§I
,
§II
.
[6]
Q. Hu, Y. Guo, X. Xie, M. Cordy, M. Papadakis, L. Ma, and Y. Le Traon
(2023)
CodeS: towards code model generalization under distribution shift
.
In
International Conference on Software Engineering (ICSE): New Ideas and Emerging Results (NIER)
,
Cited by:
§I
,
§II
.
[7]
Y. Li, S. Chen, and W. Yang
(2021)
Estimating predictive uncertainty under program data distribution shift
.
arXiv preprint arXiv:2107.10989
.
Cited by:
§I
,
§II
.
[8]
R. van Tonder and C. L. Goues
(2020)
Tailoring programs for static analysis via program transformation
.
In
Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering
,
pp. 824–834
.
Cited by:
§I
,
§II
.
[9]
H. Peng, Y. Shoshitaishvili, and M. Payer
(2018)
T-fuzz: fuzzing by program transformation
.
In
2018 IEEE Symposium on Security and Privacy (SP)
,
pp. 697–710
.
Cited by:
§I
,
§II
.
[10]
R. Vasilev and A. D’yakonov
(2023)
Calibration of neural networks
.
arXiv preprint arXiv:2303.10761
.
Cited by:
§I
,
§II-A
,
§II-B
,
§III-D
,
§III-E
.
[11]
K. Gupta, A. Rahimi, T. Ajanthan, T. Mensink, C. Sminchisescu, and R. Hartley
(2020)
Calibration of neural networks using splines
.
arXiv preprint arXiv:2006.12800
.
Cited by:
§I
,
§II-A
,
§II-A
,
§II-B
,
§III-D
,
§III-E
.
[12]
R. Krishnan and O. Tickoo
(2020)
Improving model calibration with accuracy versus uncertainty optimization
.
Advances in Neural Information Processing Systems
33
,
pp. 18237–18248
.
Cited by:
§I
,
§VIII
.
[13]
C. Spiess, D. Gros, K. S. Pai, M. Pradel, M. R. I. Rabin, A. Alipour, S. Jha, P. Devanbu, and T. Ahmed
(2024)
Calibration and correctness of language models for code
.
arXiv preprint arXiv:2402.02047
.
Cited by:
§I
,
§I
,
§II-A
,
§II
,
§III-D
,
§III-D
,
§III-E
,
§VIII
.
[14]
Z. Zhou, C. Sha, and X. Peng
(2024)
On calibration of pre-trained code models
.
In
Proceedings of the IEEE/ACM 46th international conference on software engineering
,
pp. 1–13
.
Cited by:
§I
,
§I
,
§II-A
,
§II
,
§III-D
,
§III-D
,
§III-D
,
§III-E
,
§VIII
.
[15]
Y. Virk, P. Devanbu, and T. Ahmed
(2024)
Enhancing trust in llm-generated code summaries with calibrated confidence scores
.
arXiv preprint arXiv:2404.19318
.
Cited by:
§I
.
[16]
J. Xin, R. Tang, Y. Yu, and J. Lin
(2021)
The art of abstention: selective prediction and error regularization for natural language processing
.
In
Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)
,
pp. 1040–1051
.
Cited by:
§I
,
§II
,
§IV
.
[17]
B. Calder, G. Reinman, and D. M. Tullsen
(1999)
Selective value prediction
.
In
Proceedings of the 26th annual international symposium on computer architecture
,
pp. 64–74
.
Cited by:
§I
,
§II
.
[18]
D. Hendrycks and K. Gimpel
(2018)
A baseline for detecting misclassified and out-of-distribution examples in neural networks
.
External Links:
1610.02136
Cited by:
§I
,
§II-B
,
§III-C
,
§VII
.
[19]
J. Steinhardt and P. S. Liang
(2016)
Unsupervised risk estimation using only conditional independence structure
.
Advances in Neural Information Processing Systems
29
.
Cited by:
§I
,
§II-B
,
§III-C
,
§VII
.
[20]
C. E. Shannon
(1948)
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
§I
,
§II-B
,
§III-C
,
§VII
.
[21]
R. M. Monarch
(2021)
Human-in-the-loop machine learning: active learning and annotation for human-centered ai
.
Simon and Schuster
.
Cited by:
§I
,
§III-C
,
§VII
.
[22]
Y. Gal and Z. Ghahramani
(2016)
Dropout as a bayesian approximation: representing model uncertainty in deep learning
.
In
international conference on machine learning
,
pp. 1050–1059
.
Cited by:
§I
,
§II-B
,
§III-C
,
§VII
.
[23]
B. Lakshminarayanan, A. Pritzel, and C. Blundell
(2017)
Simple and scalable predictive uncertainty estimation using deep ensembles
.
Advances in neural information processing systems
30
.
Cited by:
§I
,
§II-B
,
§III-C
,
§VII
.
[24]
R. Rathnasuriya, Z. Zhao, and W. Yang
(2025)
CodeImprove: program adaptation for deep code models
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)
,
pp. 514–526
.
Cited by:
§I
,
§II-B
,
§VII
.
[25]
R. Rathnasuriya and W. Yang
(2026)
When to answer and when to defer: a decision framework for reliable code predictions
.
In
Proceedings of the IEEE/ACM 48th International Conference on Software Engineering
,
pp. 231–235
.
Cited by:
§I
.
[26]
R. Rathnasuriya and W. Yang
(2026)
On-the-fly input adaptation for reliable code intelligence
.
In
Proceedings of the IEEE/ACM 48th International Conference on Software Engineering
,
pp. 226–230
.
Cited by:
§I
.
[27]
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
(2017)
On calibration of modern neural networks
.
External Links:
1706.04599
Cited by:
§I
,
§II-A
,
§II-A
,
§II-B
,
§III-D
,
§III-D
,
§III-D
,
§III-D
,
§III-E
,
§III-E
,
§III-E
,
§VIII
.
[28]
M. Laves, S. Ihler, K. Kortmann, and T. Ortmaier
(2019)
Well-calibrated model uncertainty with temperature scaling for dropout variational inference. arxiv 2019
.
arXiv preprint arXiv:1909.13550
.
Cited by:
§I
,
§II-B
,
§III-D
,
§III-E
,
§VIII
.
[29]
J. Devlin, M. Chang, K. Lee, and K. Toutanova
(2019)
BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
.
arXiv
.
External Links:
1810.04805
,
Document
Cited by:
§II-B
.
[30]
V. Sanh, L. Debut, J. Chaumond, and T. Wolf
(2020)
DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter
.
arXiv
.
External Links:
1910.01108
,
Document
Cited by:
§II-B
.
[31]
D. Guo, S. Ren, S. Lu, Z. Feng, D. Tang, S. Liu, L. Zhou, N. Duan, A. Svyatkovskiy, S. Fu, M. Tufano, S. K. Deng, C. Clement, D. Drain, N. Sundaresan, J. Yin, D. Jiang, and M. Zhou
(2021)
GraphCodeBERT: pre-training code representations with data flow
.
External Links:
2009.08366
Cited by:
§II-B
,
§III-B
,
§VIII
.
[32]
M. Chen, J. Tworek, H. Jun, Q. Yuan, Pinto,
et al.
(2021)
Evaluating Large Language Models Trained on Code
.
arXiv
.
External Links:
2107.03374
Cited by:
§II-B
.
[33]
Y. Zhou, S. Liu, J. Siow, X. Du, and Y. Liu
(2019)
Devign: effective vulnerability identification by learning comprehensive program semantics via graph neural networks
.
Advances in neural information processing systems
32
.
Cited by:
§III-A1
,
§III-A1
,
§VII
.
[34]
A. V. Phan and M. Le Nguyen
(2017)
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
§III-A1
,
§III-A1
,
§VII
.
[35]
Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng, M. Gong, L. Shou, B. Qin, T. Liu, D. Jiang, and M. Zhou
(2020)
CodeBERT: A Pre-Trained Model for Programming and Natural Languages
.
arXiv
.
External Links:
2002.08155
,
Document
Cited by:
§III-B
,
§VIII
.
[36]
Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov
(2019)
RoBERTa: A Robustly Optimized BERT Pretraining Approach
.
arXiv
.
External Links:
1907.11692
Cited by:
§III-B
,
§VIII
.
[37]
R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou, M. Marone, C. Akiki, J. Li, J. Chim,
et al.
(2023)
Starcoder: may the source be with you!
.
arXiv preprint arXiv:2305.06161
.
Cited by:
§III-B
.
[38]
B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez,
et al.
(2023)
Code llama: open foundation models for code
.
arXiv preprint arXiv:2308.12950
.
Cited by:
§III-B
.
[39]
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. Li,
et al.
(2024)
DeepSeek-coder: when the large language model meets programming–the rise of code intelligence
.
arXiv preprint arXiv:2401.14196
.
Cited by:
§III-B
.
[40]
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu,
et al.
(2024)
Qwen2. 5-coder technical report
.
arXiv preprint arXiv:2409.12186
.
Cited by:
§III-B
.
[41]
Y. Ding, Y. Fu, O. Ibrahim, C. Sitawarin, X. Chen, B. Alomair, D. Wagner, B. Ray, and Y. Chen
(2024)
Vulnerability detection with code language models: how far are we?
.
arXiv preprint arXiv:2403.18624
.
Cited by:
§III-B
.
[42]
X. Yin, C. Ni, and S. Wang
(2024)
Multitask-based evaluation of open-source llm on software vulnerability
.
IEEE Transactions on Software Engineering
.
Cited by:
§III-B
.
[43]
Z. Tian, J. Chen, and Z. Jin
(2023)
Code difference guided adversarial example generation for deep code models
.
External Links:
2301.02412
Cited by:
§III-B
.
[44]
Z. Yang, J. Shi, J. He, and D. Lo
(2022)
Natural attack for pre-trained models of code
.
In
Proceedings of the 44th International Conference on Software Engineering
,
pp. 1482–1493
.
Cited by:
§III-B
.
[45]
M. S. A. Nadeem, J. Zucker, and B. Hanczar
(2009)
Accuracy-rejection curves (arcs) for comparing classification methods with a reject option
.
In
Proceedings of the third International Workshop on Machine Learning in Systems Biology
,
S. Džeroski, P. Guerts, and J. Rousu (Eds.)
,
Proceedings of Machine Learning Research
, Vol.
8
,
Ljubljana, Slovenia
,
pp. 65–81
.
Cited by:
§III-E
.
[46]
J. Nixon, M. W. Dusenberry, L. Zhang, G. Jerfel, and D. Tran
(2019)
Measuring calibration in deep learning.
.
In
CVPR workshops
,
Vol.
2
.
Cited by:
§VII
,
§VIII
.
[47]
S. A. Balanya, D. Ramos, and J. Maroñas
(2024)
Adaptive temperature scaling for robust calibration of deep neural networks, march 2023
.
URL https://papers. ssrn. com/abstract
4379258
.
Cited by:
§VII
,
§VIII
.
[48]
C. Wang
(2023)
Calibration in deep learning: a survey of the state-of-the-art
.
arXiv preprint arXiv:2308.01222
.
Cited by:
§VII
,
§VIII
.
[49]
J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat,
et al.
(2023)
Gpt-4 technical report
.
arXiv preprint arXiv:2303.08774
.
Cited by:
§VIII
.
[50]
H. Tian, W. Lu, T. O. Li, X. Tang, S. Cheung, J. Klein, and T. F. Bissyandé
(2023)
Is chatgpt the ultimate programming assistant–how far is it?
.
arXiv preprint arXiv:2304.11938
.
Cited by:
§VIII
.
[51]
Y. Wang, W. Wang, S. Joty, and S. C. H. Hoi
(2021)
CodeT5: identifier-aware unified pre-trained encoder-decoder models for code understanding and generation
.
External Links:
2109.00859
Cited by:
§VIII
.
[52]
W. U. Ahmad, S. Chakraborty, B. Ray, and K. Chang
(2021)
Unified pre-training for program understanding and generation
.
arXiv preprint arXiv:2103.06333
.
Cited by:
§VIII
.
[53]
Y. Chen, L. Yuan, G. Cui, Z. Liu, and H. Ji
(2022)
A close look into the calibration of pre-trained language models
.
arXiv preprint arXiv:2211.00151
.
Cited by:
§VIII
.
[54]
K. Nguyen and B. O’Connor
(2015)
Posterior calibration and exploratory analysis for natural language processing models
.
arXiv preprint arXiv:1508.05154
.
Cited by:
§VIII
.
[55]
H. Vasconcelos, G. Bansal, A. Fourney, Q. V. Liao, and J. W. Vaughan
(2022)
Generation probabilities are not enough: improving error highlighting for ai code suggestions
.
In
HCAI Workshop at NeurIPS
,
Cited by:
§VIII
.
[56]
D. D. Johnson, D. Tarlow, and C. Walder
(2023)
Ru-sure? uncertainty-aware code suggestions by maximizing utility across random user intents
.
arXiv preprint arXiv:2303.00732
.
Cited by:
§VIII
.
[57]
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson,
et al.
(2022)
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Cited by:
§VIII
.
[58]
D. Key, W. Li, and K. Ellis
(2022)
Toward trustworthy neural program synthesis
.
arXiv preprint arXiv:2210.00848
.
Cited by:
§VIII
.
[59]
M. Minderer, J. Djolonga, R. Romijnders, F. Hubis, X. Zhai, N. Houlsby, D. Tran, and M. Lucic
(2021)
Revisiting the calibration of modern neural networks
.
Advances in neural information processing systems
34
,
pp. 15682–15694
.
Cited by:
§VIII
.
[60]
S. Y. Park and C. Caragea
(2022)
On the calibration of pre-trained language models using mixup guided by area under the margin and saliency
.
arXiv preprint arXiv:2203.07559
.
Cited by:
§VIII
.
[61]
Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma
(2023)
Look before you leap: an exploratory study of uncertainty measurement for large language models
.
arXiv preprint arXiv:2307.10236
.
Cited by:
§VIII
.