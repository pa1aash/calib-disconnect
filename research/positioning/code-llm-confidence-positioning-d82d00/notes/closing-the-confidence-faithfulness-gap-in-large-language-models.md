---
title: Closing the Confidence-Faithfulness Gap in Large Language Models
id: closing-the-confidence-faithfulness-gap-in-large-language-models
tags:
- code-llm-confidence-positioning-d82d00
- probe-verbal
- close-occupant
created: '2026-11-09T23:08:42.445377Z'
updated: '2026-11-09T23:27:44.513330Z'
source: https://arxiv.org/html/2603.25052
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:42.444772Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT. Miao and Ungar: calibration and verbalized-confidence directions
  orthogonal in three open-weight models and four datasets; Reasoning Contamination
  Effect; CAA steering and two-stage adaptive steering. Base and instruct, 7-8B, non-code,
  no reasoning models.'
---

Closing the Confidence-Faithfulness Gap in Large Language Models
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2603.25052v2 [cs.CL] 01 Apr 2026
Closing the Confidence-Faithfulness Gap in Large Language Models
Miranda Muqing Miao
†
†
thanks:
Corresponding author:
miaom@seas.upenn.edu
. Department of Computer and Information Science.
Lyle Ungar
Affiliation:
University of Pennsylvania
Abstract
Large language models (LLMs) tend to verbalize confidence scores that are largely detached from their actual accuracy, yet the geometric relationship governing this behavior remain poorly understood. In this work, we present a mechanistic interpretability analysis of verbalized confidence, using linear probes and contrastive activation addition (CAA) steering to show that calibration and verbalized confidence signals are encoded linearly but are orthogonal to one another — a finding consistent across three open-weight models and four datasets. Interestingly, when models are prompted to simultaneously reason through a problem and verbalize a confidence score, the reasoning process disrupts the verbalized confidence direction, exacerbating miscalibration. We term this the ”Reasoning Contamination Effect.” Leveraging this insight, we introduce a two-stage adaptive steering pipeline that reads the model’s internal accuracy estimate and steers verbalized output to match it, substantially improving calibration alignment across all evaluated models.
1
Introduction
Large language models have shown to be systematically overconfident. This miscalibration primarily takes two forms: at the token level, where output probabilities are poorly calibrated despite high accuracy
(
Guo et al., 2017
;
Desai and Durrett, 2020
)
, and at the
verbalized level
, where models cluster their verbal confidence scores near the top of the range regardless of actual performance
(
Lin et al., 2022a
;
Kadavath et al., 2022
;
Xiong et al., 2024
)
. Instruction tuning and RLHF exacerbate the problem, compressing verbalized confidence even further toward high certainty
(
Tian et al., 2023
;
Leng et al., 2025
)
. Of these two failure modes, verbalized confidence is particularly consequential for safe deployment. It is the primary natural language channel through which the average user receives uncertainty information. When a model tells a physician “I am 95% confident” about a diagnosis it answers correctly only 40% of the time, the downstream consequences can be catastrophic.
We argue that verbalized miscalibration is not caused by a lack of internal knowledge but by a failure to read out signals that are already present. The information needed for faithful confidence statements exists in the residual stream; the generation process simply fails to use it. This understanding shifts the question from “how do we teach models to be calibrated?” to “how do we correct the readout?”
A growing body of mechanistic-interpretability research has shown that high-level semantic and behavioral properties are encoded as linear directions in the residual stream. Linear probes recover truth and falsehood from internal activations
(
Burns et al., 2024
;
Marks and Tegmark, 2024
;
Azaria and Mitchell, 2023
)
, and steering vectors along these directions causally shift model behavior at inference time for truthfulness
(
Li et al., 2023
)
, broad behavioral traits
(
Zou et al., 2025
;
Turner et al., 2024
;
Rimsky et al., 2024
)
, and refusal
(
Arditi et al., 2024
)
. Simultaneous work has begun extending this lens to verbalized confidence.
Kumaran et al. (2026)
show that verbal confidence is cached at answer-adjacent positions and retrieved later.
Seo et al. (2026)
identify “answer-independence” as a driver of overconfidence and propose a fine-tuning fix. These studies establish that verbalized confidence has a nontrivial internal presence, yet a core question remains unanswered: what is the geometric relationship between the model’s internal accuracy signal and its verbalized confidence, and can that relationship be leveraged to improve calibration?
Existing methods for improving verbalized-confidence calibration treat the model as a black box. Prompt-engineering strategies elicit better-calibrated scores by asking models to consider top-
K
K
alternatives
(
Tian et al., 2023
)
or by aggregating across multiple response samples
(
Xiong et al., 2024
)
. The most closely related prompting work, SteerConf
(
Zhou et al., 2025
)
, shifts verbalized confidence through a range of cautious-to-confident prompt framings and aggregates the resulting scores. Training-based approaches fine-tune models to express calibrated scores using proper scoring rules
(
Li et al., 2025
)
or RL reward shaping
(
Bani-Harouni et al., 2026
)
. All of these methods manipulate the input or retrain the model without leveraging existing signals at the representational level. By contrast, our two-stage pipeline reads the model’s internal accuracy estimate and steers the output to match it, achieving substantially lower calibration error than both unsteered verbalized confidence and SteerConf across all evaluated models.
Our main contributions are:
•
Geometric dissociation.
Models encode well-calibrated accuracy information in a linearly accessible direction, but verbalized confidence occupies a separate, nearly orthogonal direction (cosine similarity
<
0.04
<0.04
). The model “knows” when it is likely wrong, but the generation process fails to surface this signal.
•
Reasoning contamination.
When the model solves a problem and rates its confidence jointly, the confidence and accuracy directions shift from weakly aligned to sharply opposed (cosine similarity dropping from
+
0.26
+0.26
to
−
0.63
-0.63
), meaning joint prompting actively inverts the relationship between what the model knows and what it says.
•
Steering-based calibration.
Contrastive activation addition produces causally controlled shifts in verbalized confidence that generalize across datasets and transfer from base to instruction-tuned models. We introduce a two-stage adaptive steering pipeline that reads the model’s internal accuracy estimate and steers verbalized output to match, improving calibration by
4
4
–
7
×
7\times
.
2
Method
This section describes the two methodological tools that underpin our analysis. We first introduce gold calibration linear probing, which tests whether accuracy information is linearly accessible in the residual stream. We then describe contrastive activation steering, which constructs steering vectors that causally shift verbalized confidence at inference time. The remaining paragraphs detail the datasets, models, activation extraction procedure, and prompt design used throughout.
2.1
Gold Calibration Linear Probing
To test whether calibration information is linearly accessible in model activations, we train ridge regression probes on extracted activation vectors. For
gold calibration probing
, we use activations from the
pure correctness
prompt and regress against binary correctness labels or binned empirical accuracy (the fraction of times the model answers a question correctly across 50 samples with different random seeds). We sweep over a broad range of
ℓ
2
\ell_{2}
regularization strengths and select the value that maximizes
validation
performance.
2.2
Contrastive Activation Steering
To move beyond correlation and establish a causal link between activation directions and verbalized confidence, we apply contrastive activation addition (CAA)
(
Turner et al., 2025
)
. We elicit the same set of questions under
K
=
11
K=11
prompt framings that span a wide range of instructed confidence levels, collecting hidden-state activations
𝐡
q
,
k
(
ℓ
)
∈
ℝ
d
\mathbf{h}_{q,k}^{(\ell)}\in\mathbb{R}^{d}
at layer
ℓ
\ell
for question
q
q
under framing
k
k
. Each instance is paired with its parsed verbalized confidence
c
q
,
k
∈
[
0
,
1
]
c_{q,k}\in[0,1]
. The exact
K
K
prompts used are shown in the Appendix.
We partition instances into a
high-confidence
set
ℋ
q
=
{
k
:
c
q
,
k
>
τ
hi
}
\mathcal{H}_{q}=\{k:c_{q,k}>\tau_{\mathrm{hi}}\}
and a
low-confidence
set
ℒ
q
=
{
k
:
c
q
,
k
<
τ
lo
}
\mathcal{L}_{q}=\{k:c_{q,k}<\tau_{\mathrm{lo}}\}
, with
τ
hi
=
0.75
\tau_{\mathrm{hi}}=0.75
and
τ
lo
=
0.25
\tau_{\mathrm{lo}}=0.25
. For each question
q
q
that contains at least one instance in both sets, we compute a per-question contrast:
𝜹
q
(
ℓ
)
=
1
|
ℋ
q
|
​
∑
k
∈
ℋ
q
𝐡
q
,
k
(
ℓ
)
−
1
|
ℒ
q
|
​
∑
k
∈
ℒ
q
𝐡
q
,
k
(
ℓ
)
.
\boldsymbol{\delta}_{q}^{(\ell)}=\frac{1}{|\mathcal{H}_{q}|}\sum_{k\in\mathcal{H}_{q}}\mathbf{h}_{q,k}^{(\ell)}-\frac{1}{|\mathcal{L}_{q}|}\sum_{k\in\mathcal{L}_{q}}\mathbf{h}_{q,k}^{(\ell)}.
(1)
The steering vector is then obtained by averaging over all qualifying questions
𝒬
\mathcal{Q}
:
𝐯
(
ℓ
)
=
1
|
𝒬
|
​
∑
q
∈
𝒬
𝜹
q
(
ℓ
)
.
\mathbf{v}^{(\ell)}=\frac{1}{|\mathcal{Q}|}\sum_{q\in\mathcal{Q}}\boldsymbol{\delta}_{q}^{(\ell)}.
(2)
Because each
𝜹
q
\boldsymbol{\delta}_{q}
is computed
within
a single question, this design controls for confounds such as question difficulty, topic, and prompt framing, isolating the component of the activation that varies specifically with expressed confidence.
At inference time, we inject the steering vector into the residual stream during autoregressive generation. Let
𝐡
t
(
ℓ
)
\mathbf{h}_{t}^{(\ell)}
denote the hidden state at layer
ℓ
\ell
and generation step
t
t
. The steered activation is:
𝐡
~
t
(
ℓ
)
=
𝐡
t
(
ℓ
)
+
α
​
𝐯
^
(
ℓ
)
,
\tilde{\mathbf{h}}_{t}^{(\ell)}=\mathbf{h}_{t}^{(\ell)}+\alpha\,\hat{\mathbf{v}}^{(\ell)},
(3)
where
𝐯
^
(
ℓ
)
=
𝐯
(
ℓ
)
‖
𝐯
(
ℓ
)
‖
⋅
n
¯
(
ℓ
)
\hat{\mathbf{v}}^{(\ell)}=\frac{\mathbf{v}^{(\ell)}}{\|\mathbf{v}^{(\ell)}\|}\cdot\bar{n}^{(\ell)}
is the steering vector normalized to unit length and rescaled by the mean activation norm
n
¯
(
ℓ
)
\bar{n}^{(\ell)}
at layer
ℓ
\ell
, and
α
∈
ℝ
\alpha\in\mathbb{R}
controls steering strength. We evaluate three injection sites: the last prompt token only, every answer token, and both jointly. Steering at the answer-token position yields the most stable results, slightly outperforming the combined condition; we therefore report answer-token steering throughout. The steering layer, variant, and strength are selected on a validation split, and all steered generations use temperature
T
=
1.0
T=1.0
, matching the activation-collection setting.
Datasets:
We evaluate on four question-answering benchmarks that span mathematical reasoning, broad knowledge, and truthfulness: MATH
(
Hendrycks et al., 2021b
)
, MMLU
(
Hendrycks et al., 2021a
)
, TriviaQA
(
Joshi et al., 2017
)
, and TruthfulQA
(
Lin et al., 2022b
)
. Each dataset contains three non-overlapping splits: a training split for extracting activations and fitting probes, a validation split for selecting optimal steering layers and strengths, and a held-out test split for final evaluation.
Models:
We conduct experiments across three model families: Llama-3.1-8B
(
Grattafiori and et al, 2024
)
, Qwen2.5-7B
(
Qwen et al., 2025
)
, and Mistral-7B-v0.1
(
Jiang et al., 2023
)
. For each family, we analyze both the base (pretrained) model and its corresponding instruction-tuned (instruct) variant.
Activation Extraction:
We extract residual stream activations after the MLP sublayer at each transformer layer. For each input, we record the hidden state at two positions: the final prompt token (
prompt completion
) and the final generated token (
answer completion
). Both extraction points yield similar steering vectors and downstream effects; we use prompt-completion activations throughout, as they can be obtained before generation begins and are therefore more practical for inference-time interventions. All generations use sampling temperature
T
=
1.0
T{=}1.0
to elicit the model’s default output distribution.
Prompt Design:
We utilize three prompt types to disentangle the model’s representations of answer correctness and expressed confidence. The
pure correctness
prompt asks the model only to answer the question, with no mention of confidence. The
pure confidence
prompt asks the model only to state how confident it is in answering a given question correctly, without producing the answer. The
joint
prompt asks the model to both express its confidence and provide an answer. This design is
critical
for analyzing the relationship between accuracy and verbalized confidence in Sec.
3.4
of the paper. Exactly prompts are shown in the Appendix.
3
Results
We organize our results around three questions. First, are accuracy and verbalized confidence linearly encoded, and how do they relate geometrically? We show both signals are linearly decodable but nearly orthogonal, and that joint prompting inverts their relationship (§
3.1
–
3.4
). Second, is the verbalized confidence direction causally active and general? We show that steering vectors shift verbalized confidence in a controlled manner, generalize across datasets, and transfer from base to instruction-tuned models (§
3.5
–
3.7
). Third, can we close the calibration gap? We introduce an adaptive steering pipeline that meaningfully improves ECE, brier score, and MAE. (§
3.8
).
3.1
Gold Calibration Information Is Linearly Encoded
Figure 1:
Ridge probe projection at layer 21 (Qwen-2.5-7B-Base).
Left:
Distribution of activations projected onto the probe weight vector,
separated by correct (blue) and incorrect (pink) answers (Cohen’s
d
=
1.88
d=1.88
).
Right:
The same scalar projection plotted against binned empirical accuracy
(
r
=
0.80
r=0.80
).
Takeaway:
The model encodes well-calibrated accuracy information in a single
linear direction, even when never asked about confidence.
We extract activations under a
pure correctness
prompt, one that asks the model to produce only an answer, with no mention of confidence, then train a ridge regression probe to predict empirical accuracy: the fraction of times the model answers a given question correctly across repeated samples. As shown in Figure
1
, a single linear direction in the residual stream cleanly separates correct from incorrect responses (Cohen’s
d
=
1.88
d=1.88
) and, more importantly, tracks graded empirical accuracy at
r
=
0.80
r=0.80
. The model thus encodes well-calibrated uncertainty information in a linearly accessible direction, even when it is never prompted to express confidence; the calibration signal is present in the activations, but the generation process fails to surface it.
3.2
Verbalized Confidence Is Linearly Separable
Figure 2:
High and low verbalized confidence occupy distinct regions of
activation space (25th vs. 75th percentile split).
First principal component of
activations from the
pure confidence
prompt, colored by whether the model
verbalized high or low confidence.
Takeaway:
Verbalized confidence is linearly separable in later layers,
confirming that the model constructs a dedicated confidence representation during
processing.
Using activations from the
pure confidence
prompt, we project onto the first principal component and color each point by whether the model expressed high or low confidence. Figure
2
reveals clear linear separability between high- and low-confidence activations in later layers, suggesting that the model progressively constructs a linearly separable representation of its own confidence. To quantify this effect, we train linear ridge regression and report train and test time
R
2
R^{2}
in Figure
3
a and b. The natural next question is whether they share the same direction or dissociated, which would explain verbalized miscalibration.
3.3
Verbalized Confidence and Accuracy Occupy Orthogonal Directions
Figure 3:
Probe fit and directional analysis across layers (Qwen-2.5-7B-Base).
(a, b)
Train and test
R
2
R^{2}
of ridge probes predicting empirical accuracy
(gold calibration, blue) and verbalized confidence (pure verbal, orange).
(c)
Cosine similarity between the two probe weight vectors (pure verbal
vs. gold calibration).
(d)
Cosine similarity between contrastive confidence and accuracy directions,
computed separately under the pure confidence prompt (blue) and the joint
solve-and-rate prompt (red). Shaded region indicates the gap between the two
conditions, the
reasoning contamination effect
.
Takeaway:
Accuracy and confidence are encoded in nearly orthogonal directions
(cosine similarity
<
0.04
<0.04
), and joint prompting inverts their relationship
(from
+
0.26
+0.26
to
−
0.63
-0.63
).
Although both gold calibration and pure verbalized confidence are both individually predictable using linear probes, with test
R
2
R^{2}
reaching 0.55 and 0.85 respectively (Figure
3
a, b), the directions that encode these two signals are nearly orthogonal. Figure
3
(c) shows that the cosine similarity between the two ridge probe weight vectors remains below 0.04 across all layers. The model thus likely maintains separate linear subspaces for “how likely am I to be correct” and “how confident do I say I am.” This dissociation is consistent with our observation that base models verbalize poorly calibrated confidence despite encoding well-calibrated accuracy information internally (§
3.1
). To further illustrate the clear orthogonality phenomenon in higher dimensions, we include four distinct subspace-level analyses in Appendix
B
.
3.4
Reasoning Contamination Inverts the Verbalized Confidence–Accuracy Relationship
Does the relationship between the confidence and accuracy directions depend on how the model is prompted? We define two setups: a
pure confidence
condition, where the model rates its confidence on answering a question correctly without solving the problem, and a
joint
condition, where the model solves the problem and rates its confidence in the same generation. For each condition and layer, we extract a contrastive confidence direction (mean activation of high-confidence instances minus mean of low-confidence instances) and a contrastive accuracy direction (mean of high-accuracy instances minus mean of low-accuracy instances), then measure the cosine similarity between them.
Figure
3
(d) demonstrate the layer-wise output. Under the pure condition (blue), the confidence and accuracy directions start out as completely orthogonal and become are weakly positive, reaching
+
0.26
+0.26
at layer 21. This indicates that when the model assesses confidence in isolation, its confidence representation partially aligns with genuine competence. Under the joint condition (red), the relationship inverts. The two directions are completely anti-correlated across all layers, reaching
−
0.63
-0.63
at layer 15. When the model reasons about a problem and rates its confidence simultaneously, the direction encoding verbalized confidence actively opposes the direction encoding correctness. We coin this the
reasoning contamination effect
. Joint prompts produce representations in which confidence and accuracy point in opposite directions.
This effect is prominent during CAA steering. When we apply verbalized confidence steering using
joint
solve-and-rate generation, the more we influenced the verbalized confidence output, the more we erode the model’s accuracy performance. This motivates the design of our two-stage pipeline in Sec.
3.8
, where we improve verbalized confidence calibration using
pure confidence
prompts, leaving the model’s problem-solving pass entirely unperturbed in a separate run.
3.5
Steering Produces Principled Shifts in Verbalized Confidence
The preceding sections establish the direction of gold calibration and verbalized confidence. But is the verbalized confidence direction merely a statistical pattern, or is it causally active? We apply CAA steering vectors constructed from top-versus-bottom quartile activations under the
pure confidence
prompt. Steering is applied during generation under the same prompt condition, so that the model is only verbalizing confidence, not solving the problem. Table
1
presents the central causal result: scaling the steering vector produces a clean positive shift in verbalized confidence across MATH, TriviaQA, and TruthfulQA. Positive scaling increases verbalized confidence, negative scaling decreases it, and the relationship is approximately linear over a wide range of steering strengths.
Table 1:
Activation steering produces principled shifts in verbalized
confidence.
Mean verbalized confidence as a function of steering strength
(multiples of the CAA vector), evaluated on MATH, TriviaQA, TruthfulQA, and MMLU.
Takeaway:
The verbalized confidence direction is causally active, with
positive and negative scaling producing controlled, approximately linear shifts
across all models and datasets. Results increase (→) across columns.
Neg. Steering
Pos. Steering
Model
Dataset
α
=
−
0.75
\alpha{=}{-}0.75
−
0.50
{-}0.50
−
0.25
{-}0.25
0
0
0.25
0.25
0.50
0.50
0.75
0.75
Mistral-7B
MATH
23.1
51.4
57.2
64.7
64.7
88.6
99.0
(layer 27)
TriviaQA
34.5
38.4
42.8
56.2
67.1
83.1
94.5
TruthfulQA
24.0
35.3
41.5
54.2
77.5
82.2
92.6
MMLU
25.8
35.5
45.6
60.0
60.8
88.0
97.9
Llama-3.1-8B
MATH
18.2
29.3
37.4
45.3
55.1
71.4
85.8
(layer 24)
TriviaQA
17.8
26.8
30.6
48.1
56.5
71.2
87.7
TruthfulQA
38.7
40.8
49.3
51.8
56.8
64.9
85.9
MMLU
18.9
21.4
28.3
48.5
65.6
73.0
88.3
Qwen2.5-7B
1
1
1
Qwen2.5-7B verbalizes meaningfully higher baseline confidence ( 15-20% higher) than Llama and Mistral during the activation collection process, leaving a narrower dynamic range and less headroom for upward steering.
MATH
29.3
35.7
48.6
66.0
82.1
84.3
92.5
(layer 21)
TriviaQA
45.5
53.0
55.5
60.6
63.5
65.0
67.8
TruthfulQA
52.6
54.3
56.3
60.2
61.4
62.8
64.1
MMLU
62.2
64.1
66.3
66.6
71.3
71.1
77.0
3.6
Cross-Dataset Generalization
A steering vector is most useful if it generalizes beyond the distribution on which it was constructed. We calculate CAA vectors exclusively on MATH activations and evaluate their steering effect on MMLU, TriviaQA, and TruthfulQA without any adaptation. Table
2
reports the results.
Table 2:
MATH-derived steering vectors transfer across datasets.
Mean
verbalized confidence (%) under varying steering magnitudes, using a CAA vector
trained only on MATH at layer 21 of Qwen2.5-7B, layer 24 of Llama-3.1-8B, and
layer 27 of Mistral-7B-v0.1.
Takeaway:
The confidence direction is domain-general, not an artifact of
mathematical notation or problem format. Results increase (→) across columns.
Negative Steering
Positive Steering
Target Dataset
α
=
−
0.75
\alpha{=}{-}0.75
−
0.50
{-}0.50
−
0.25
{-}0.25
0
0
0.25
0.25
0.50
0.50
0.75
0.75
Llama-3.1-8B
MMLU
3.6
6.4
13.8
18.7
34.3
56.6
76.2
TriviaQA
6.0
7.2
15.6
24.2
30.4
57.5
76.5
TruthfulQA
5.6
9.7
19.5
21.9
35.7
57.7
75.7
Mistral-7B-v0.1
MMLU
8.1
18.5
22.6
33.8
50.5
74.7
86.4
TriviaQA
10.8
18.5
26.1
41.0
54.6
75.3
85.0
TruthfulQA
12.9
20.9
27.5
43.2
58.6
73.5
85.4
Qwen2.5-7B
MMLU
58.3
59.1
64.2
64.0
67.1
66.3
68.8
TriviaQA
52.7
54.9
57.9
59.2
60.6
61.8
64.3
TruthfulQA
52.2
54.3
59.1
59.6
59.9
61.6
62.9
The MATH-derived vector produces consistent directional shifts across all target datasets. This cross-dataset generalization indicates that the confidence direction is not an artifact of MATH-specific features such as mathematical notation or problem format. Instead, it reflects a shared, domain-general mechanism through which language models represent and express confidence.
3.7
Base-to-Instruct Transfer
Finally, we test whether confidence directions extracted from base models can steer the verbalized confidence of their instruction-tuned counterparts. This experiment is motivated by the observation that instruct models exhibit more severe overconfidence than base models, suggesting that post-training procedures may suppress or distort the confidence signal that is present in the base model.
Table 3:
Base model steering vectors modulate instruct model confidence.
Steering vectors extracted from base models applied to their corresponding instruct
variants.
Takeaway:
The confidence direction partially survives post-training,
suggesting that instruct-model overconfidence reflects a readout failure rather than
loss of the underlying signal. Results increase (→) across columns.
Neg. Steering
Pos. Steering
Model
α
=
−
0.75
\alpha{=}{-}0.75
−
0.50
{-}0.50
−
0.25
{-}0.25
0
0
0.25
0.25
0.50
0.50
0.75
0.75
Qwen2.5-7B-Inst.
38.6
75.5
86.5
88.4
90.3
94.1
98.6
Llama-3.1-8B-Inst.
11.4
39.2
85.8
87.8
92.3
94.4
95.8
Mistral-7B-Inst.-v0.1
37.6
46.7
50.0
63.2
80.5
86.6
90.2
Table
3
shows that base-model-derived steering vectors successfully modulate instruct model confidence across all three model families. This result has two implications. First, the linear confidence direction identified in base models is not completely eliminated by post-training; it persists in the instruct model’s residual stream in a geometrically compatible form and remains stronger in some models than others. Second, it is possible that the overconfidence exhibited by instruct models is not a consequence of losing the confidence signal entirely, but rather of the generation process failing to read it out faithfully. Thus, steering could provide a direct mechanism to restore confidence control in instruct-tuned models.
3.8
Adaptive Two-Stage Steering for Verbalized Calibration Improvement
The previous findings show that activation steering can reliably shift verbalized confidence up or down. We now ask whether it can be used to
improve verbalized calibration
, that is, to make verbalized confidence match empirical accuracy. The challenge is that a single global steering strength cannot calibrate all questions. We address this with a two-stage pipeline that assigns a
per-question
steering strength.
Stage 1: Probe-based target estimation.
We have demonstrated in
3.1
that our gold calibration probe can effectively predict the empirical accuracy of a question using the internal states of the model at prompt completion (before model starts answering) only. The probe’s prediction serves as the target confidence for that question: what the model
should
say, given what its activations reveal about its likelihood of being correct. We apply isotonic regression on a held-out validation set to calibrate the probe outputs.
Stage 2: Adaptive steering.
Table 4:
Activation steering improves calibration across all models.
Expected Calibration Error (ECE), Brier Score, and Mean Absolute Error (MAE) for
four confidence sources on MATH. Bolded numbers indicate the best performing
outcomes.
Takeaway:
Adaptive steering effectively reduces ECE relative to
unsteered verbalized confidence and substantially outperforms SteerConf, confirming
that reading the model’s internal accuracy signal and steering output to match it
closes much of the faithfulness gap.
Model
Confidence Source
ECE
↓
\downarrow
Brier
↓
\downarrow
MAE
↓
\downarrow
Llama-3.1-8B
Logit baseline
68.4
50.5
68.5
Verbalized
14.9
8.4
20.2
SteerConf
46.3
40.6
53.6
Verbalized (steered)
3.7
2.4
10.5
Mistral-7B–v0.1
Logit baseline
73.5
57.5
73.5
Verbalized
35.1
15.9
40.0
SteerConf
24.3
20.1
29.1
Verbalized (steered)
3.3
2.1
9.3
Qwen2.5-7B
Logit baseline
75.0
58.3
74.7
Verbalized
36.0
16.7
36.9
SteerConf
19.5
25.9
41.4
Verbalized (steered)
10.7
3.5
11.8
We exclusively apply steering during generation under the
pure confidence
prompt. We sweep steering strength
α
∈
[
−
2.0
,
+
2.0
]
\alpha\in[-2.0,+2.0]
with 0.1 increments on validation questions to build a transfer function mapping
α
\alpha
to mean verbalized confidence. We invert this function via monotone Piecewise Cubic Hermite Interpolating Polynomial (PCHIP) interpolation: given a target confidence
c
q
∗
c^{*}_{q}
for question
q
q
, the inverse yields the steering strength
α
q
∗
\alpha^{*}_{q}
that would, on average, produce that confidence level. Each test question thus receives a
question-specific
α
q
∗
\alpha^{*}_{q}
, steering overconfident questions downward and underconfident questions upward. We generate 50 samples per question under adaptive steering and report the mean verbalized confidence as the final estimate. We also generate 50 samples of solutions per question in a separate pass to calculate empirical accuracy and match question-level confidence and accuracy to calculate calibration metrics.
Table
4
reports calibration metrics for three confidence sources. The logit baseline, the token probability assigned to the predicted answer, is severely miscalibrated across all models (ECE
≥
68
\geq 68
). Unsteered verbalized confidence improves over logit baseline, but remains far from calibrated. Adaptive steering reduces ECE by 4–7
×
\times
relative to unsteered verbalized confidence. Mistral shows the largest improvement, dropping from 35.1 to 3.3 ECE and from 15.9 to 2.1 Brier score. The pattern is consistent across all three metrics: by reading the model’s internal estimate of its own competence and steering its verbalized output to match, we are able to close much of the faithfulness gap of
verbalized confidence .
4
Related Work
Verbalized confidence calibration.
Lin et al. (2022a)
introduced verbalized confidence elicitation, and subsequent work has consistently found that LLMs are systematically overconfident across models, domains, and elicitation strategies
(
Kadavath et al., 2022
;
Xiong et al., 2024
;
Groot and Valdenegro - Toro, 2024
)
. Prompting-based remedies attempt to shift this distribution:
Tian et al. (2023)
ask the model to consider top-
K
K
alternatives before scoring,
Xiong et al. (2024)
aggregate confidence across multiple response samples, and
Zhou et al. (2025)
interpolate between cautious and confident prompt framings. Training-based approaches take a different route, fine-tuning models to produce calibrated scores via proper scoring rules
(
Li et al., 2025
)
or RL reward shaping
(
Bani-Harouni et al., 2026
)
. Our differs by operating on the representations directly, reading the model’s internal accuracy signal and steering the output to match.
Internal representations of confidence.
A growing body of work shows that LLMs encode uncertainty-relevant information in their hidden states.
Burns et al. (2024)
and
Marks and Tegmark (2024)
recover truth and falsehood via linear probes,
Azaria and Mitchell (2023)
detect when models produce false statements from hidden-state classifiers, and
Stolfo et al. (2024)
identify dedicated neurons that regulate token-level output entropy. Concurrent work has begun applying similar tools to verbalized confidence specifically.
Kumaran et al. (2026)
use activation patching and steering to show that verbal confidence is cached at answer-adjacent positions and reflects richer signals than token log-probabilities.
Seo et al. (2026)
identify answer-independence as a driver of overconfidence through attention and gradient attribution analysis. Our work differs from these studies in both question and method. Where prior analyses ask
what
verbalized confidence represents or
when
it is computed, we ask
why
it diverges from accuracy.
5
Discussion, Limitations, and Conclusion
Discussion:
We hypothesize that reasoning contamination reflects a conflict between two computationally distinct tasks. Problem-solving is heavily optimized during training, while confidence assessment requires self-evaluation the model has far less practice performing. Under joint prompting, high-magnitude activations along effort-encoding directions appear to be interpreted as engagement rather than difficulty, inflating confidence on precisely the questions the model struggles with most. This explains why separating the two tasks into distinct passes, as our pipeline does, prevents the interference.
Limitation:
Our experiments use 7–8B parameter models, and whether the linear encoding and orthogonality findings hold at larger scales, where representations may occupy higher-dimensional subspaces, remains open. Our evaluation is restricted to question-answering tasks with verifiable answers, extending to open-ended generation would require rethinking how the probe target is constructed. Finally, our pipeline requires a separate generation pass for confidence assessment. Learning to steer within a single forward pass is a natural next step toward practical deployment.
Conclusion:
The central message of this work is that verbalized miscalibration in LLMs is a readout failure, not a knowledge deficit. Models encode gold calibration along a linear direction and verbalized confidence along a separate, nearly orthogonal linear direction. The signal needed to produce faithful confidence statements is present in the residual stream, but the generation process fails to use it. Our two-stage pipeline turns this understanding into a practical intervention: a linear probe reads the model’s internal accuracy estimate, and contrastive activation addition steers verbalized output to match, substantially reducing calibration error. The verbalized confidence steering vectors generalize across datasets and transfer from base to instruction-tuned models, confirming that the confidence direction is a stable, general-purpose feature of language model representations. More broadly, this work illustrates a pattern we believe will recur: when a model’s outputs are misaligned with its internal representations, the most direct remedy is not retraining or prompt engineering but identifying the internal signal and correcting the readout. Verbalized confidence is one instance of this pattern, and we suspect it is not the last.
References
Arditi
et al.
(2024)
A. Arditi, O. B. Obeso, A. Syed, D. Paleka, N. Rimsky, W. Gurnee, and N. Nanda
Refusal in language models is mediated by a single direction
.
In
The Thirty-eighth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.
Azaria and Mitchell (2023)
A. Azaria and T. Mitchell
The internal state of an LLM knows when it’s lying
.
In
Findings of the Association for Computational Linguistics: EMNLP 2023
,
H. Bouamor, J. Pino, and K. Bali (Eds.)
,
Singapore
,
pp. 967–976
.
External Links:
Link
,
Document
Cited by:
§1
,
§4
.
Bani-Harouni
et al.
(2026)
D. Bani-Harouni, C. Pellegrini, P. Stangel, E. Özsoy, K. Zaripova, M. Keicher, and N. Navab
Rewarding doubt: a reinforcement learning approach to calibrated confidence expression of large language models
.
In
The Fourteenth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
,
§4
.
Burns
et al.
(2024)
C. Burns, H. Ye, D. Klein, and J. Steinhardt
Discovering latent knowledge in language models without supervision
.
External Links:
2212.03827
,
Link
Cited by:
§1
,
§4
.
Desai and Durrett (2020)
S. Desai and G. Durrett
Calibration of pre-trained transformers
.
In
Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)
,
B. Webber, T. Cohn, Y. He, and Y. Liu (Eds.)
,
Online
,
pp. 295–302
.
External Links:
Link
,
Document
Cited by:
§1
.
Grattafiori and et al (2024)
A. Grattafiori and A. D. et al
The llama 3 herd of models
.
External Links:
2407.21783
,
Link
Cited by:
§2.2
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
§4
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
Proceedings of the 34th International Conference on Machine Learning - Volume 70
,
ICML’17
,
pp. 1321–1330
.
Cited by:
§1
.
Hendrycks
et al.
(2021a)
D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt
Measuring massive multitask language understanding
.
In
International Conference on Learning Representations
,
External Links:
Link
Cited by:
§2.2
.
Hendrycks
et al.
(2021b)
D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
Measuring mathematical problem solving with the MATH dataset
.
In
Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)
,
External Links:
Link
Cited by:
§2.2
.
Jiang
et al.
(2023)
A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford, D. S. Chaplot, D. de las Casas, F. Bressand, G. Lengyel, G. Lample, L. Saulnier, L. R. Lavaud, M. Lachaux, P. Stock, T. L. Scao, T. Lavril, T. Wang, T. Lacroix, and W. E. Sayed
Mistral 7b
.
External Links:
2310.06825
,
Link
Cited by:
§2.2
.
Joshi
et al.
(2017)
M. Joshi, E. Choi, D. Weld, and L. Zettlemoyer
TriviaQA: a large scale distantly supervised challenge dataset for reading comprehension
.
In
Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
R. Barzilay and M. Kan (Eds.)
,
Vancouver, Canada
,
pp. 1601–1611
.
External Links:
Link
,
Document
Cited by:
§2.2
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson, S. Johnston, S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen, Y. Bai, S. Bowman, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion, S. Kravec, L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei, T. Brown, J. Clark, N. Joseph, B. Mann, S. McCandlish, C. Olah, and J. Kaplan
Language models (mostly) know what they know
.
External Links:
2207.05221
,
Link
Cited by:
§1
,
§4
.
Kumaran
et al.
(2026)
D. Kumaran, A. Conmy, F. Barbero, S. Osindero, V. Patraucean, and P. Velickovic
How do llms compute verbal confidence
.
External Links:
2603.17839
,
Link
Cited by:
§1
,
§4
.
Leng
et al.
(2025)
J. Leng, C. Huang, B. Zhu, and J. Huang
Taming overconfidence in LLMs: reward calibration in RLHF
.
In
The Thirteenth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
.
Li
et al.
(2023)
K. Li, O. Patel, F. Viégas, H. Pfister, and M. Wattenberg
Inference-time intervention: eliciting truthful answers from a language model
.
In
Thirty-seventh Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.
Li
et al.
(2025)
Y. Li, M. Xiong, J. Wu, and B. Hooi
ConfTuner: training large language models to express their confidence verbally
.
In
The Thirty-ninth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
,
§4
.
Lin
et al.
(2022a)
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
§1
,
§4
.
Lin
et al.
(2022b)
S. Lin, J. Hilton, and O. Evans
TruthfulQA: measuring how models mimic human falsehoods
.
In
Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
S. Muresan, P. Nakov, and A. Villavicencio (Eds.)
,
Dublin, Ireland
,
pp. 3214–3252
.
External Links:
Link
,
Document
Cited by:
§2.2
.
Marks and Tegmark (2024)
S. Marks and M. Tegmark
The geometry of truth: emergent linear structure in large language model representations of true/false datasets
.
External Links:
Link
Cited by:
§1
,
§4
.
Qwen
et al.
(2025)
Qwen, :, A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, H. Lin, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Lin, K. Dang, K. Lu, K. Bao, K. Yang, L. Yu, M. Li, M. Xue, P. Zhang, Q. Zhu, R. Men, R. Lin, T. Li, T. Tang, T. Xia, X. Ren, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Wan, Y. Liu, Z. Cui, Z. Zhang, and Z. Qiu
Qwen2.5 technical report
.
External Links:
2412.15115
,
Link
Cited by:
§2.2
.
Rimsky
et al.
(2024)
N. Rimsky, N. Gabrieli, J. Schulz, M. Tong, E. Hubinger, and A. Turner
Steering llama 2 via contrastive activation addition
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 15504–15522
.
External Links:
Link
,
Document
Cited by:
§1
.
Seo
et al.
(2026)
K. J. Seo, S. Lim, and T. Kim
ADVICE: answer-dependent verbalized confidence estimation
.
External Links:
2510.10913
,
Link
Cited by:
§1
,
§4
.
Stolfo
et al.
(2024)
A. Stolfo, B. P. Wu, W. Gurnee, Y. Belinkov, X. Song, M. Sachan, and N. Nanda
Confidence regulation neurons in language models
.
In
The Thirty-eighth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§4
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
§1
,
§1
,
§4
.
Turner
et al.
(2025)
A. M. Turner, L. Thiergart, G. Leech, D. Udell, J. J. Vazquez, U. Mini, and M. MacDiarmid
Steering language models with activation engineering
.
External Links:
Link
Cited by:
§2.2
.
Turner
et al.
(2024)
A. M. Turner, L. Thiergart, G. Leech, D. Udell, J. J. Vazquez, U. Mini, and M. MacDiarmid
Steering language models with activation engineering
.
External Links:
2308.10248
,
Link
Cited by:
§1
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
§1
,
§1
,
§4
.
Zhou
et al.
(2025)
Z. Zhou, T. Jin, J. Shi, and L. Qing
SteerConf: steering LLMs for confidence elicitation
.
In
The Thirty-ninth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
,
§4
.
Zou
et al.
(2025)
A. Zou, L. Phan, S. Chen, J. Campbell, P. Guo, R. Ren, A. Pan, X. Yin, M. Mazeika, A. Dombrowski, S. Goel, N. Li, M. J. Byun, Z. Wang, A. Mallen, S. Basart, S. Koyejo, D. Song, M. Fredrikson, J. Z. Kolter, and D. Hendrycks
Representation engineering: a top-down approach to ai transparency
.
External Links:
2310.01405
,
Link
Cited by:
§1
.
Appendix A
Prompt Design
(a) Pure Correctness Prompt
Solve the following math problem step by step.
Problem: {problem}
Show your work, then write your final answer on a new line in the format:
Answer: [your answer]
(b) Pure Confidence Prompt
Read the following math problem and rate your confidence that you can solve it correctly. Do not solve the problem.
Problem: {problem}
Rate how confident you are that you can solve this problem correctly on a scale from 0 to 100, where 0 means certainly incorrect and 100 means certainly correct.
Confidence:
(c) Joint Prompt
Read the following math problem. First rate your confidence that you can solve it correctly, then solve it step by step.
Problem: {problem}
Rate how confident you are that you can solve this problem correctly on a scale from 0 to 100, where 0 means certainly incorrect and 100 means certainly correct.
Confidence: [0–100]
Show your work, then write your final answer on a new line in the format:
Answer: [your answer]
Figure 4:
Prompt templates for three elicitation conditions.
(a) The pure correctness prompt asks the model only to solve the problem, with no mention of confidence. (b) The pure confidence prompt asks the model only to rate its confidence, without producing a solution. (c) The joint prompt asks the model to first rate its confidence and then solve the problem. Separating these conditions allows us to isolate the model’s confidence representation from the computational process of problem-solving.
Fig
4
shows the three types of base prompts used for activations extraction under the three conditions: pure answer elicitation, pure confidence elicitation, and both answer and confidence elicitation.
Table 5:
Prompt framings used to elicit diverse verbalized confidence levels (
K
=
11
K{=}11
). Each framing appends a “Note” to the base prompt (see below). The
Vanilla
framing appends no note. Target ranges are approximate and were calibrated on a pilot study with Qwen-2.5-7B-Base.
k
k
Target Conf.
Appended Note
1
10–20%
“You are extremely uncertain about your mathematical abilities. You should assume you are likely wrong unless the problem is trivially simple. Assign confidence below 20 for most problems, and only above 50 if you are absolutely certain of every step.”
2
25–35%
“You are making important decisions, thus you should avoid giving a wrong answer with high confidence. You should be very cautious. For most problems, your confidence should be below 30 unless you are very sure of every step.”
3
35–50%
“You are making important decisions, thus you should avoid giving a wrong answer with high confidence. You should be cautious and critical of your own reasoning. Assign confidence below 50 unless you have verified every step carefully.”
4
45–60%
“You are making important decisions, thus you should avoid giving a wrong answer with high confidence. Be realistic about the difficulty of the problem. Most math problems have subtle traps, so moderate confidence (40–70) is appropriate for most answers.”
5
20–40%
“(1) You are making important decisions, thus you should avoid giving a wrong answer with high confidence. (2) You should be very cautious, and tend to give low confidence on almost all of the answers.”
6
30–50%
“(1) You are making important decisions, thus you should avoid giving a wrong answer with high confidence. When in doubt, err on the side of lower confidence.”
7
40–60%
“(1) You are making important decisions, thus you should avoid giving a wrong answer with high confidence. Try to be honest about your uncertainty.”
8
variable
“Your confidence should accurately reflect the probability that your answer is correct. A confidence of 30 means you expect to be right about 30% of the time. A confidence of 80 means you expect to be right about 80% of the time. Be precise and honest.”
9
60–80%
“You are a capable mathematical problem solver. Express your confidence honestly, but do not underestimate yourself. If you followed a clear reasoning chain, that warrants reasonable confidence.”
10
80–95%
“(1) You are making important decisions, thus you should avoid giving a right answer with low confidence. Trust your reasoning process.”
11
95–100%
(no note appended — vanilla baseline)
Table
5
displays the 11 verbalized confidence notes we used on top of the base confidence elicitation prompts to derive a wide range of confidence expression from the model. Those notes are only used in conjunction with
pure confidence
base prompts for extracting the CAA verbalized confidence steering vector.
Figure 5:
Subspace orthogonality analysis between gold calibration and verbalized confidence representations across transformer layers.
(a)
Mean principal angle between 10-dimensional predictive subspaces extracted via iterative ridge regression with deflation; the gray band shows the
±
2
​
σ
\pm 2\sigma
range for random subspace pairs of equal dimensionality.
(b)
Top two canonical correlations from CCA applied to the 5-dimensional projections of each concept’s subspace.
(c)
R
2
R^{2}
retention ratio after projecting out the other concept’s top-10 subspace (cross-concept removal) versus projecting out one’s own subspace (self-removal control).
(d)
Variance decomposition showing unique and shared
R
2
R^{2}
for each concept, where shared
R
2
R^{2}
is measured by predicting one target using only the other concept’s subspace directions.
Across all four analyses and all layers, the two representations occupy nearly orthogonal subspaces with negligible shared structure.
Appendix B
Subspace and CCA Analysis
A potential concern with the cosine similarity analysis in Section
3.3
is that near-orthogonality of two fitted ridge weight vectors does not preclude correlated multi-dimensional subspaces: linear readouts are not unique, and the two concepts could share higher-dimensional structure invisible to single-direction comparisons.
To address this, we conduct four complementary subspace-level analyses.
For each layer, we extract 10-dimensional predictive subspaces for both gold calibration and verbalized confidence via iterative ridge regression with deflation on matched activations (PCA-reduced to 200 dimensions, retaining
>
>
96% of variance), using question-level train/validation/test splits.
Principal angles between subspaces.
The multi-dimensional predictive subspaces for gold calibration and verbalized confidence are nearly as separated as random subspace pairs of equal dimensionality.
We extract 10 orthogonal predictive directions for each concept via iterative ridge regression with deflation, then compute the principal angles between the two resulting subspaces.
Across all layers, the mean principal angle ranges from
76.0
​
°
76.0\degree
to
79.6
​
°
79.6\degree
, closely tracking the random-subspace baseline of
79.1
​
°
±
0.8
​
°
79.1\degree\pm 0.8\degree
(Figure
5
a).
Even the smallest principal angle—which captures the maximally aligned pair of directions—remains above
56.8
​
°
56.8\degree
(layer 3) and exceeds
62
​
°
62\degree
at later layers.
These values confirm that the two subspaces do not share any closely aligned directions, ruling out the possibility of correlated multi-dimensional structure hidden from single-vector comparisons.
Canonical Correlation Analysis.
CCA between the two concept subspaces reveals only weak canonical correlations, reinforcing the orthogonality finding.
We project the shared activation matrix onto each concept’s top-5 subspace directions and compute CCA on the test set.
The largest canonical correlation across all layers is 0.40 (layer 6), and most layers exhibit a top correlation between 0.23 and 0.36, with higher-order correlations dropping rapidly toward zero (Figure
5
b).
These modest values indicate that even the maximally correlated linear combinations of the two subspaces share limited statistical dependence, far below what would be expected if the concepts occupied overlapping representational subspaces.
Cross-prediction after subspace removal.
Removing one concept’s entire 10-dimensional subspace barely affects the other concept’s predictability, while self-removal completely destroys it.
After projecting out all 10 gold calibration directions, the verbalized confidence probe retains 96–99% of its original
R
2
R^{2}
across layers (e.g.,
R
2
=
0.80
→
0.77
R^{2}=0.80\rightarrow 0.77
at layer 24).
Conversely, after removing the verbalized confidence subspace, the gold calibration probe retains 72–96% of its
R
2
R^{2}
(Figure
5
c).
As a control, removing a concept’s
own
subspace reduces
R
2
R^{2}
to
≈
0.0
{\approx}\,0.0
in every case, confirming that the extracted directions do capture the relevant information.
This asymmetric ablation provides the strongest functional evidence that the two concepts’ information resides in genuinely distinct subspaces.
Variance decomposition.
The vast majority of each concept’s explained variance is unique, with negligible shared variance between the two representations.
We quantify shared
R
2
R^{2}
by predicting each target using only the other concept’s subspace directions: the shared component is at most
0.056
0.056
(layer 6 for verbalized confidence) and typically below
0.03
0.03
, compared to unique
R
2
R^{2}
values of
0.59
0.59
–
0.78
0.78
for verbalized confidence and
0.17
0.17
–
0.28
0.28
for gold calibration (Figure
5
d).
Across all layers, shared variance accounts for less than 9% of either concept’s total explained variance, confirming that the two probes extract information from functionally independent subspaces of the activation space.