---
title: Why Are LLMs Confidently Wrong? Correcting Overconfident Errors via Causal
  Head Intervention
id: why-are-llms-confidently-wrong-correcting-overconfident-errors-via-causal-head-i
tags:
- code-llm-confidence-positioning-d82d00
- w3-3
created: '2026-11-10T08:23:58.618939Z'
updated: '2026-11-10T08:25:58.650848Z'
source: https://arxiv.org/html/2610.34994
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:58.618178Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'RMIT, arXiv 2610.34994 full text: CoCHI, inference-time causal head gating
  that suppresses attention heads responsible for overconfident errors; LLaMA-3.1-8B,
  Gemma-2-9B, Mistral-7B; five multiple-choice QA benchmarks; improves calibration
  metrics while preserving accuracy vs post-hoc calibration. Not code, no execution
  labels, no probe-vs-verbal comparison. Marginal to L2 causal-intervention idea only.'
---

Why Are LLMs Confidently Wrong? Correcting Overconfident Errors via Causal Head Intervention
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2610.34994v1 [cs.AI] 26 Oct 2026
Why Are LLMs Confidently Wrong?
Correcting Overconfident Errors via Causal Head Intervention
Jing Ren
Affiliation:
RMIT University
Bowen Li
Affiliation:
RMIT University
Ziqi Xu
Affiliation:
RMIT University
Xuechao Yang
Affiliation:
RMIT University
Feng Xia
Email:
{S4065838, S3890442}@student.rmit.edu.au{ziqi.xu, xuechao.yang, feng.xia}@rmit.edu.au
#
Equal contribution
*
Corresponding author
https://aisuko.github.io/confix
Affiliation:
RMIT University
Abstract
Modern large language models (LLMs) often exhibit overconfident errors, assigning high confidence to incorrect predictions and thereby undermining reliability in real-world use. Existing calibration methods typically rely on post-hoc adjustment or retraining, operating at the output level without addressing the underlying causes of miscalibration. We propose
CoCHI
(
C
lass-
o
riented
C
ausal
H
ead
I
ntervention), a framework that improves calibration by identifying and intervening on internal components responsible for distinct confidence behaviours. By analysing predictions through correctness-confidence patterns, CoCHI enables targeted intervention on model internals, reducing overconfident errors while preserving correct predictions. Our approach provides a mechanistic perspective on calibration, linking reliability to identifiable structures within the model rather than treating it as an output-level issue. Experiments across multiple LLMs show consistent improvements in calibration metrics, including Expected Calibration Error, Negative Log-Likelihood, and Brier Score, while maintaining accuracy on five multiple-choice question answering benchmarks. These results suggest that effective calibration requires not only adjusting outputs, but also addressing the underlying causal mechanisms within the model.
1
Introduction
Modern neural models have achieved remarkable performance across a wide range of tasks. However, they frequently produce overconfident errors, assigning high confidence to incorrect predictions
[
1
,
2
,
3
,
4
]
and thereby undermining reliability in high-stakes applications. This issue is further amplified in large language models (LLMs)
[
5
,
6
,
7
]
, which have become a dominant paradigm in modern AI and are widely deployed in domains such as healthcare, education, and scientific reasoning, where incorrect yet confident outputs can lead to significant downstream risks
[
8
,
9
,
10
,
11
,
12
]
.
To address this problem, a large body of work has focused on
calibration
, aiming to align predicted confidence with empirical accuracy
[
13
,
14
,
15
]
. Existing approaches, such as temperature scaling and its variants, primarily operate at the output level by adjusting logits or confidence scores, while more recent methods introduce learned calibrators or inference-time interventions
[
16
]
. Despite their effectiveness in some settings, these approaches share a fundamental limitation: they treat miscalibration as a surface-level phenomenon and do not address the
internal mechanisms
that give rise to overconfident errors. As a result, they often fail to generalise and provide limited insight into why models are confidently wrong.
In this work, we take a different perspective and ask:
what internal components of a model are responsible for overconfident errors, and can we intervene on them directly?
Recent advances in mechanistic interpretability
[
17
,
18
,
19
,
20
]
have made significant progress in moving beyond correlational post-hoc explanations toward causally grounded, intervention-based understanding of how LLMs implement computations internally. In particular, causal intervention methods such as causal head gating
[
17
]
, causal mediation analysis
[
18
,
21
]
, and causal tracing
[
19
]
allow us to identify internal components that are causally responsible for specific model behaviours by systematically perturbing internal activations and observing the resulting change in the model’s output distribution. However, existing interpretability approaches largely focus on post-hoc analysis and explanation, rather than leveraging these insights to actively improve model reliability. Consequently, the connection between internal computational circuits and miscalibration remains largely unexplored.
To bridge this gap, we propose
CoCHI
(
C
lass-
o
riented
C
ausal
H
ead
I
ntervention), a framework that improves calibration by directly targeting the internal causes of overconfident errors in large language models. Our key insight is that miscalibration is not merely an output-level issue, but arises from specific internal components that systematically promote incorrect yet highly confident predictions or introduce noise into otherwise correct ones. To capture this, we decompose model predictions into four calibration classes based on correctness and confidence, and perform class-conditioned causal analysis to identify attention heads associated with distinct behaviours. Based on this analysis, CoCHI constructs a structured intervention that selectively suppresses heads responsible for overconfident errors while removing non-contributing components in correct predictions. This results in a minimal, targeted modification to the model’s internal computation that improves calibration without altering model parameters, providing a mechanism-aware alternative to conventional post-hoc approaches.
Contributions.
Our main contributions are as follows:
•
We propose a structural causal mask for calibration, operating directly on model internals rather than relying on post-hoc output adjustment.
•
We partition model predictions into four fine-grained classes based on correctness and confidence, enabling precise identification of attention heads that causally promote overconfident errors or fail to support correct predictions.
•
We introduce CoCHI (Class-oriented Causal Head Intervention), an inference-time framework that performs class-aware causal analysis and constructs a structured mask to selectively suppress problematic attention heads.
•
Extensive experiments across five multiple-choice question answering benchmarks show that CoCHI consistently improves calibration metrics while preserving accuracy, outperforming traditional post-hoc calibration methods.
2
Related Work
Uncertainty Estimation and Overconfident Errors.
A large body of work studies uncertainty estimation in neural models, including Bayesian approaches
[
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
, deep ensembles
[
27
]
, and post-hoc techniques such as temperature scaling
[
16
]
, which rescale logits using a learned temperature parameter. In the context of LLMs, uncertainty estimation and calibration have received increasing attention
[
28
]
. Recent efforts extend post-hoc calibration to LLMs, including adaptive temperature scaling
[
29
]
and learned calibrators such as Thermometer
[
30
]
, aiming to better align predicted confidence with empirical accuracy. Other approaches adjust hidden representations, for example by training a linear layer on top of the final hidden states for confidence prediction
[
31
]
, or exploit prompt-based strategies and self-consistency to estimate uncertainty
[
32
,
33
,
34
,
35
,
15
]
. Despite their effectiveness in some settings, these methods primarily operate at the output or representation level, but recent work such as Inference-Time Intervention
[
36
]
shows that undesirable behaviours (e.g., hallucination) are governed by internal mechanisms. These methods primarily enhance truthful representations, while overlooking the role of mechanisms that specifically drive overconfident errors, where incorrect predictions are assigned high confidence scores. Recent work has shown that attention heads encode rich signals about model uncertainty, enabling unsupervised uncertainty estimation without additional training
[
37
]
. However, these approaches primarily focus on extracting uncertainty signals from internal representations, without modifying the model’s behaviour. This limitation motivates our approach, which targets the structural causal components responsible for overconfident errors and performs structured intervention to improve calibration.
Circuit Discovery in Mechanistic Interpretability
Circuit discovery aims to identify the minimal subgraph of a language model responsible for a specific behaviour. The seminal work of
[
38
]
manually identified the Indirect Object Identification (IOI) circuit in GPT-2 Small, comprising 28 attention heads across seven functional classes. To scale this process,
Conmy et al. [39]
proposed Automatic Circuit Discovery (ACDC), an iterative pruning method based on activation patching, which successfully rediscovered known circuits such as Greater-Than and recovered most components of the IOI circuit. Subsequent approaches, including Efficient Attribution Patching (EAP), further improved the efficiency and scalability of automated circuit discovery
[
40
]
. Beyond circuit discovery, mechanistic interpretability has increasingly incorporated tools from causal inference
[
41
]
. These approaches leverage counterfactual interventions and structured perturbations to uncover how structural heads contribute to model outputs
[
42
,
43
,
44
,
45
]
. In particular, causal head gating identifies functional roles of attention heads by assigning graded scores for facilitation, interference, or irrelevance based on their causal effect on task performance, going beyond purely correlational analyses
[
17
]
. Recent mechanistic studies have shown that verbalised confidence in LLMs is governed by dedicated internal circuits that are largely decoupled from factual correctness
[
46
]
. These findings suggest that overconfidence arises not from miscalibration at the output layer, but from specific internal mechanisms that consistently generate confident responses regardless of their accuracy
[
47
]
. Building on this insight, we identify and suppress attention heads that contribute to high-confidence errors, leading to improved calibration and reliability.
3
Preliminaries
We briefly introduce the key components for identifying the causal roles of attention heads in transformer models via differentiable intervention.
Transformer with Head-wise Gating.
Consider a transformer model with
L
L
layers and
H
H
attention heads per layer. For each attention head
(
ℓ
,
h
)
(\ell,h)
, we introduce a continuous gating variable
G
ℓ
,
h
∈
[
0
,
1
]
G_{\ell,h}\in[0,1]
that scales the output of the head:
Z
ℓ
,
h
=
G
ℓ
,
h
⋅
(
A
ℓ
,
h
​
V
ℓ
,
h
)
,
Z_{\ell,h}=G_{\ell,h}\cdot\big(A_{\ell,h}V_{\ell,h}\big),
(1)
where
A
ℓ
,
h
A_{\ell,h}
denotes the attention weights (after softmax) and
V
ℓ
,
h
V_{\ell,h}
denotes the value projections.
The gated head outputs are concatenated and projected as in standard multi-head attention. By varying
G
ℓ
,
h
G_{\ell,h}
, we perform soft interventions on individual heads without modifying model parameters.
Gate Optimisation.
The gating variables are optimised while keeping model parameters frozen. Given a dataset
𝒟
\mathcal{D}
, we minimise the negative log-likelihood objective:
ℒ
⁡
(
G
)
=
−
𝔼
(
x
,
y
)
∼
𝒟
​
log
⁡
P
⁡
(
y
∣
x
;
G
)
,
\mathcal{L}(G)=-\mathbb{E}_{(x,y)\sim\mathcal{D}}\log P(y\mid x;G),
(2)
where
P
⁡
(
y
∣
x
;
G
)
P(y\mid x;G)
denotes the model output under gating configuration
G
G
.
Optionally, a regularisation term can be introduced to encourage sparsity or density of the gating values. This formulation allows us to assess the causal contribution of each head by observing how scaling its output affects model behaviour.
Dual Optimisation and Role Identification.
To disambiguate causal importance from incidental effects, we optimise two sets of gates:
•
G
+
G^{+}
: optimised under a retention bias, encouraging gates towards 1,
•
G
−
G^{-}
: optimised under a sparsity bias, encouraging gates towards 0.
The divergence between
G
+
G^{+}
and
G
−
G^{-}
reveals the causal role of each head: heads that remain active under sparsity are necessary for the task, while those suppressed even under retention bias are likely harmful.
Causal Head Taxonomy.
Based on the optimised gates, each attention head is assigned a causal role.
Facilitating heads
contribute positively to performance and remain active under sparsity (
G
−
G^{-}
), indicating necessity.
Interfering heads
degrade performance and are suppressed even under retention bias (
G
+
G^{+}
), indicating harmful contributions.
Irrelevant heads
have negligible impact, with gating values varying under different regularisation regimes. This taxonomy provides a causal, rather than correlational, characterisation of model internals, validated through targeted ablation and intervention.
4
Methodology
We reframe calibration as a problem of causal intervention on model heads. Specifically, our framework identifies and suppresses causal heads responsible for overconfident errors, while removing sources of noise in otherwise correct predictions. This perspective provides a mechanistic view of miscalibration, linking reliability to identifiable structural components within the model. An overview of
CoCHI
is shown in Figure
1
.
Figure 1:
The framework of CoCHI.
4.1
Problem Setup
Let
f
θ
​
(
x
)
f_{\theta}(x)
denote a pretrained language model that maps an input
x
x
to a probability distribution
p
θ
(
⋅
∣
x
)
p_{\theta}(\cdot\mid x)
over a fixed answer space
𝒴
\mathcal{Y}
. The model prediction is defined as:
y
^
​
(
x
)
=
arg
⁡
max
y
∈
𝒴
​
p
θ
​
(
y
∣
x
)
.
\hat{y}(x)=\arg\max_{y\in\mathcal{Y}}p_{\theta}(y\mid x).
(3)
The corresponding confidence is defined as:
c
⁡
(
x
)
=
max
y
∈
𝒴
⁡
p
θ
​
(
y
∣
x
)
.
c(x)=\max_{y\in\mathcal{Y}}p_{\theta}(y\mid x).
(4)
Let
y
∗
y^{*}
denote the ground-truth label. A prediction is correct if
y
^
​
(
x
)
=
y
∗
\hat{y}(x)=y^{*}
. We focus on the failure mode of
overconfident errors
, defined as incorrect predictions with high confidence:
y
^
​
(
x
)
≠
y
∗
,
c
⁡
(
x
)
≥
τ
c
,
\hat{y}(x)\neq y^{*},\quad c(x)\geq\tau_{c},
(5)
where
τ
c
\tau_{c}
is a predefined confidence threshold.
Our goal is to design an inference-time intervention that reduces such errors by targeting their underlying internal causes, thereby improving calibration while preserving predictive accuracy.
4.2
Calibration-Class Decomposition
Rather than treating calibration as a global property of output probabilities, we decompose model behaviour into four calibration classes based on correctness and confidence:
𝒞
=
{
correct_high
,
correct_low
,
wrong_high
,
wrong_low
}
.
\mathcal{C}=\{\texttt{correct\_high},\texttt{correct\_low},\texttt{wrong\_high},\texttt{wrong\_low}\}.
Formally, this defines a partition over predictions induced by correctness (
y
^
​
(
x
)
=
y
∗
\hat{y}(x)=y^{*}
or
y
^
​
(
x
)
≠
y
∗
\hat{y}(x)\neq y^{*}
) and confidence (
c
⁡
(
x
)
≥
τ
c
c(x)\geq\tau_{c}
or
c
⁡
(
x
)
<
τ
c
c(x)<\tau_{c}
). This decomposition isolates overconfident errors (
wrong_high
) as a distinct subset, enabling us to analyse the structural causal head that give rise to miscalibrated confidence, rather than conflating them with other types of errors.
4.3
Class-Conditioned Causal Head Attribution
Following Causal Head Gating (CHG)
[
17
]
, we attribute model behaviour to individual attention heads by estimating their causal contribution. Let
ℋ
\mathcal{H}
denote the set of all attention heads across
l
l
layers. For each head
h
∈
ℋ
h\in\mathcal{H}
, CHG computes two scores with respect to a target behaviour defined on a dataset
𝒟
\mathcal{D}
: a
necessary score
s
h
nec
s_{h}^{\text{nec}}
, measuring the drop in performance when the head is ablated, and a
sufficient score
s
h
suf
s_{h}^{\text{suf}}
, measuring how well the head alone can reproduce the behaviour when isolated.
In our setting, we apply CHG in a class-conditioned manner. For each calibration class
c
∈
𝒞
c\in\mathcal{C}
, we construct a subset
𝒟
c
\mathcal{D}_{c}
consisting of inputs whose predictions fall into class
c
c
, and perform CHG using the model’s own predictions as the target signal. This yields a
necessary score
s
h
nec
​
(
c
)
s_{h}^{\text{nec}}(c)
and a
sufficient score
s
h
suf
​
(
c
)
s_{h}^{\text{suf}}(c)
for each head. The necessary score measures how strongly a head persists when the optimisation is encouraged to minimise the number of active heads, whereas the sufficient score measures how strongly a head remains selected when the optimisation is encouraged to retain all heads compatible with good task performance.
CoCHI is trained in three sequential stages. First, an unregularised optimisation stage (
λ
=
0
\lambda=0
) is performed to obtain a shared task-relevant initialisation:
z
l
,
h
0
→
stage 1
z
^
l
,
h
.
z^{0}_{l,h}\xrightarrow{\text{stage 1}}\hat{z}_{l,h}.
(6)
The resulting logits
z
^
l
,
h
\hat{z}_{l,h}
are then copied into two separate optimisation branches:
z
^
l
,
h
→
z
l
,
h
+
,
z
^
l
,
h
→
z
l
,
h
−
,
\hat{z}_{l,h}\rightarrow z^{+}_{l,h},\quad\hat{z}_{l,h}\rightarrow z^{-}_{l,h},
(7)
corresponding to the positive-L1 and negative-L1 stages, respectively.
During each forward pass, the learned logit is converted into a multiplicative gate using a sigmoid function and applied directly to the attention head output:
x
~
l
,
h
=
σ
⁡
(
z
l
,
h
)
⋅
x
l
,
h
,
\tilde{x}_{l,h}=\sigma(z_{l,h})\cdot x_{l,h},
(8)
where
x
l
,
h
∈
ℝ
T
×
d
h
x_{l,h}\in\mathbb{R}^{T\times d_{h}}
denotes the output of head
h
h
at layer
l
l
, and
T
T
is the sequence length. A gate value close to
0
0
suppresses the head, while a value close to
1
1
preserves its contribution.
The optimisation objective is defined as:
ℒ
=
−
1
|
S
|
∑
t
∈
S
log
p
θ
(
x
t
+
1
∣
x
≤
t
)
−
λ
⋅
1
L
​
H
∑
l
,
h
clamp
(
z
l
,
h
,
−
4
,
4
)
,
\mathcal{L}=-\frac{1}{|S|}\sum_{t\in S}\log p_{\theta}(x_{t+1}\mid x_{\leq t})-\lambda\cdot\frac{1}{LH}\sum_{l,h}\mathrm{clamp}(z_{l,h},-4,4),
(9)
where the first term is the next-token negative log-likelihood and the second term is the regularisation objective. The logits are clamped to
[
−
4
,
4
]
[-4,4]
before regularisation to stabilise optimisation and encourage near-binary gate values.
Two complementary optimisation stages are then performed. In the positive-L1 stage (
λ
=
+
0.1
\lambda=+0.1
), the optimiser is encouraged to suppress unnecessary heads, so only heads whose removal significantly increases the NLL retain large gate values. These heads correspond to necessary heads. In the negative-L1 stage (
λ
=
−
0.1
\lambda=-0.1
), the optimiser instead encourages larger gate values, identifying heads that are sufficient to maintain low task loss.
At the end of optimisation, the final sigmoid gate values are recorded as:
s
h
nec
​
(
c
)
=
σ
​
(
z
l
,
h
+
)
(
final
)
,
s_{h}^{\text{nec}}(c)=\sigma(z^{+}_{l,h})^{(\mathrm{final})},
(10)
s
h
suf
​
(
c
)
=
σ
​
(
z
l
,
h
−
)
(
final
)
,
s_{h}^{\text{suf}}(c)=\sigma(z^{-}_{l,h})^{(\mathrm{final})},
(11)
which define the necessary and sufficient scores, respectively.
A binary threshold
τ
=
0.5
\tau=0.5
is then applied to derive discrete causal roles:
role
l
,
h
=
{
facilitating
,
s
h
nec
​
(
c
)
≥
τ
∧
s
h
suf
​
(
c
)
≥
τ
,
interfering
,
s
h
nec
​
(
c
)
<
τ
∧
s
h
suf
​
(
c
)
≥
τ
,
irrelevant
,
otherwise
.
\mathrm{role}_{l,h}=\begin{cases}\textbf{facilitating},&s_{h}^{\text{nec}}(c)\geq\tau\ \wedge\ s_{h}^{\text{suf}}(c)\geq\tau,\\
\textbf{interfering},&s_{h}^{\text{nec}}(c)<\tau\ \wedge\ s_{h}^{\text{suf}}(c)\geq\tau,\\
\textbf{irrelevant},&\text{otherwise}.\end{cases}
(12)
A head is considered
facilitating
for class
c
c
if both scores exceed a threshold
τ
\tau
, indicating that it is both necessary and sufficient for producing the corresponding behaviour; otherwise, it is treated as non-facilitating, encompassing both interfering and irrelevant heads.
This procedure yields two sets per class,
ℋ
c
fac
\mathcal{H}_{c}^{\text{fac}}
and
ℋ
c
non-fac
\mathcal{H}_{c}^{\text{non-fac}}
. Crucially, this class-conditioned decomposition associates specific structural causal head with distinct calibration behaviours and forms the basis for targeted intervention in subsequent steps.
4.4
Canonical-Union Mask Construction
We construct a targeted structural causal mask for calibration by combining two complementary types of heads. First, from the
wrong_high
class, we extract the facilitating heads:
ℋ
err
=
ℋ
wrong_high
fac
,
\mathcal{H}^{\text{err}}=\mathcal{H}_{\texttt{wrong\_high}}^{\text{fac}},
(13)
which contribute to generating high-confidence incorrect predictions. These heads can be interpreted as forming the targeted structural causal mask that amplify erroneous outputs.
Second, from the
correct_high
class, we extract the non-facilitating heads:
ℋ
noise
=
ℋ
correct_high
non-fac
,
\mathcal{H}^{\text{noise}}=\mathcal{H}_{\texttt{correct\_high}}^{\text{non-fac}},
(14)
which do not support correct predictions and may introduce variability in confidence estimation.
We then define the candidate mask set as the union
ℋ
mask
=
ℋ
err
∪
ℋ
noise
\mathcal{H}^{\text{mask}}=\mathcal{H}^{\text{err}}\cup\mathcal{H}^{\text{noise}}
.
To avoid excessive intervention, we rank heads by their attribution strength:
r
⁡
(
h
)
=
max
⁡
(
|
s
h
nec
|
,
|
s
h
suf
|
)
,
r(h)=\max\big(|s_{h}^{\text{nec}}|,|s_{h}^{\text{suf}}|\big),
(15)
and select the top-
k
k
heads to form a compact mask
ℋ
top-
​
k
\mathcal{H}^{\text{top-}k}
. This ranking focuses the intervention on the most influential components while preserving the overall functionality of the model.
4.5
Inference-Time Intervention
Given the identified set of influential heads
ℋ
top-
​
k
\mathcal{H}^{\text{top-}k}
, we perform a structured intervention on the model’s internal computation at inference time. Rather than modifying model parameters or post-processing outputs, our approach directly alters the forward pass by selectively suppressing specific attention heads.
Let
z
h
​
(
x
)
z_{h}(x)
denote the output of attention head
h
h
for input
x
x
. We define a binary gating operator
g
h
∈
{
0
,
1
}
g_{h}\in\{0,1\}
for each head as:
g
h
=
{
0
,
if
​
h
∈
ℋ
top-
​
k
,
1
,
otherwise
,
g_{h}=\begin{cases}0,&\text{if }h\in\mathcal{H}^{\text{top-}k},\\
1,&\text{otherwise},\end{cases}
(16)
and obtain the modified head output:
z
~
h
​
(
x
)
=
g
h
⋅
z
h
​
(
x
)
.
\tilde{z}_{h}(x)=g_{h}\cdot z_{h}(x).
(17)
This yields a perturbed model
f
θ
masked
​
(
x
)
f_{\theta}^{\text{masked}}(x)
.
This operation can be interpreted as a form of
causal editing
on the model’s computation graph, where selected edges (i.e., head outputs) are removed to disrupt specific functional circuits. In particular, masking heads in
ℋ
err
\mathcal{H}^{\text{err}}
suppresses pathways responsible for overconfident errors, while masking heads in
ℋ
noise
\mathcal{H}^{\text{noise}}
reduces spurious variation in otherwise correct predictions.
The intervention is both
local
and
minimal
, modifying only a small subset of heads and thus preserving most of the model’s representational capacity. The calibration classes are used exclusively during mask construction. At inference time, the resulting global mask is applied uniformly to all test inputs without requiring ground-truth labels or sample-specific class identification. From a computational perspective, the overhead is negligible, as the intervention involves only element-wise gating during the forward pass. Since no parameters are updated, the method can be seamlessly applied to pretrained models in a plug-and-play manner.
5
Experiments
5.1
Implementation Details
In practice, we apply CoCHI on a small subset of the data (typically fewer than 50 samples), with balanced sampling across calibration classes to ensure stable attribution estimates. We use a fixed confidence threshold
τ
c
=
0.5
\tau_{c}=0.5
to define calibration classes, and a threshold
τ
\tau
to identify facilitating heads. The number of masked heads
k
k
is treated as a hyperparameter; we find that small values (e.g.,
k
∈
[
6
,
8
]
k\in[6,8]
) provide a favourable trade-off between calibration improvement and accuracy preservation. The penalty coefficient was empirically tuned across 15 model–dataset runs, yielding a stable trade-off that limits degradation on
correct_high
calibration (
Δ
​
ECE
<
0.015
\Delta\mathrm{ECE}<0.015
) while still effectively suppressing overconfident errors on incorrect predictions. We evaluate our method on three representative open-source large language models:
LLaMA-3.1-8B
[
7
]
,
Gemma-2-9B
[
48
]
, and
Mistral-7B-v0.1
[
49
]
. We adopt
LLaMA-3.1-8B
as the primary backbone for ablation and hyperparameter studies. All experiments are conducted in a zero-shot setting, ensuring that improvements in calibration are solely attributable to the proposed inference-time intervention. Further experimental details are provided in Appendix
A
.
5.2
Evaluation Protocols
Datasets.
We evaluate our method on five widely used multiple-choice question answering benchmarks spanning diverse domains, including general knowledge, science, and medicine, to assess both generalisation and domain-specific robustness of calibration. Measuring Massive Multitask Language Understanding (MMLU)
[
50
]
is a large-scale multi-domain benchmark covering 57 subjects such as STEM, humanities, and social sciences, designed to evaluate general knowledge and reasoning ability. MedMCQA
[
51
]
is a large medical QA dataset derived from real-world entrance examinations, focusing on domain-specific knowledge in healthcare. OpenBookQA
[
52
]
is a science QA benchmark requiring multi-hop reasoning over a small set of core science facts. MedQA-USMLE
[
53
]
is a challenging medical benchmark based on USMLE exams, evaluating clinical reasoning and professional knowledge. SciQ
[
54
]
is a science QA dataset constructed from educational materials, focusing on factual understanding and basic reasoning. All datasets are formatted as four-choice multiple-choice tasks, and we adopt a unified evaluation protocol.
Baselines.
We compare our method against several representative calibration approaches, including both post-hoc and inference-time techniques. Temperature Scaling (TS)
[
16
]
is a standard post-hoc method that learns a single scalar temperature
T
T
on a held-out validation set to rescale logits. Inference-Time Intervention (ITI)
[
36
]
modifies model activations during inference using a fixed intervention strength
α
\alpha
, enabling reliability improvements without retraining. Thermometer (Therm.)
[
30
]
is a learned calibration method that trains a lightweight MLP-based calibrator on top of model outputs to better align predicted confidence with empirical accuracy. Adaptive Temperature Scaling (ATS)
[
29
]
extends TS by dynamically adapting the temperature based on input features, allowing more flexible calibration across samples.
Metrics.
We evaluate performance in terms of both accuracy and calibration. Prediction quality is measured by
accuracy
, defined as the proportion of correctly predicted answers. Calibration is assessed using
Expected Calibration Error (ECE)
[
16
]
, which measures the discrepancy between predicted confidence and empirical accuracy across confidence bins;
Negative Log-Likelihood (NLL)
, which evaluates the quality of predicted probability distributions by penalising overconfident incorrect predictions; and the
Brier Score (BS)
, which computes the mean squared error between predicted probabilities and ground-truth labels. Lower values of ECE, NLL, and Brier Score indicate better calibration. Together, these metrics provide a comprehensive assessment of both predictive correctness and the reliability of confidence estimates.
Table 1:
Results on four benchmarks (MMLU, MedMCQA, OpenBookQA, and MedQA-USMLE). Best results are highlighted in bold.
MMLU
MedMCQA
Method
Accuracy
↑
\uparrow
ECE
↓
\downarrow
NLL
↓
\downarrow
BS
↓
\downarrow
Accuracy
↑
\uparrow
ECE
↓
\downarrow
NLL
↓
\downarrow
BS
↓
\downarrow
Gemma-2-9B
TS
0.6653
±
\pm
0.0050
0.0660
±
\pm
0.0173
0.5060
±
\pm
0.0335
0.1683
±
\pm
0.0125
0.5607
±
\pm
0.0186
0.0556
±
\pm
0.0261
0.6114
±
\pm
0.0151
0.2122
±
\pm
0.0066
ITI
0.6693
±
\pm
0.0060
0.0605
±
\pm
0.0062
0.5029
±
\pm
0.0233
0.1675
±
\pm
0.0105
0.5673
±
\pm
0.0200
0.0451
±
\pm
0.0140
0.6085
±
\pm
0.0154
0.2122
±
\pm
0.0070
Therm.
0.6653
±
\pm
0.0050
0.1831
±
\pm
0.0567
1.8729
±
\pm
1.1455
0.2302
±
\pm
0.0429
0.5607
±
\pm
0.0186
0.2849
±
\pm
0.0106
2.9242
±
\pm
0.4188
0.3293
±
\pm
0.0165
ATS
0.6653
±
\pm
0.0050
0.3784
±
\pm
0.0052
0.9191
±
\pm
0.0066
0.3553
±
\pm
0.0030
0.5607
±
\pm
0.0186
0.3534
±
\pm
0.0783
4.1559
±
\pm
1.3606
0.3702
±
\pm
0.0396
CoCHI
0.6730
±
\pm
0.0023
0.0601
±
\pm
0.0011
0.4982
±
\pm
0.0141
0.1654
±
\pm
0.0056
0.5873
±
\pm
0.0023
0.0380
±
\pm
0.0263
0.5983
±
\pm
0.0064
0.2070
±
\pm
0.0027
LLaMA-3.1-8B
TS
0.6007
±
\pm
0.0061
0.0569
±
\pm
0.0040
0.5205
±
\pm
0.0138
0.1936
±
\pm
0.0065
0.5753
±
\pm
0.0297
0.0557
±
\pm
0.0124
0.6173
±
\pm
0.0142
0.2144
±
\pm
0.0052
ITI
0.5853
±
\pm
0.0685
0.2014
±
\pm
0.1191
0.7161
±
\pm
0.1590
0.2580
±
\pm
0.0643
0.3747
±
\pm
0.0893
0.3766
±
\pm
0.2287
1.2043
±
\pm
0.7682
0.3831
±
\pm
0.1870
Therm.
0.6007
±
\pm
0.0061
0.1717
±
\pm
0.0778
1.9024
±
\pm
0.7247
0.2415
±
\pm
0.0354
0.5753
±
\pm
0.0297
0.2327
±
\pm
0.0356
1.8116
±
\pm
0.8973
0.2907
±
\pm
0.0208
ATS
0.6007
±
\pm
0.0061
0.3265
±
\pm
0.0257
1.7325
±
\pm
1.5251
0.3330
±
\pm
0.0157
0.5753
±
\pm
0.0301
0.3307
±
\pm
0.0727
2.5476
±
\pm
2.9442
0.3495
±
\pm
0.0501
CoCHI
0.6120
±
\pm
0.0626
0.0490
±
\pm
0.0089
0.5168
±
\pm
0.0236
0.1743
±
\pm
0.0008
0.5773
±
\pm
0.0081
0.0365
±
\pm
0.0090
0.6064
±
\pm
0.0032
0.2114
±
\pm
0.0012
Mistral-7B
TS
0.5987
±
\pm
0.0121
0.0902
±
\pm
0.0182
0.5754
±
\pm
0.0130
0.1974
±
\pm
0.0037
0.4867
±
\pm
0.0081
0.0604
±
\pm
0.0308
0.6424
±
\pm
0.0339
0.2249
±
\pm
0.0133
ITI
0.3980
±
\pm
0.1152
0.3693
±
\pm
0.2666
1.2168
±
\pm
0.8397
0.3845
±
\pm
0.2056
0.3293
±
\pm
0.0939
0.3985
±
\pm
0.3280
1.4918
±
\pm
1.2039
0.4317
±
\pm
0.2469
Therm.
0.5987
±
\pm
0.0121
0.2988
±
\pm
0.0449
1.4277
±
\pm
0.9584
0.3177
±
\pm
0.0274
0.4867
±
\pm
0.0081
0.2668
±
\pm
0.0776
2.6632
±
\pm
0.6919
0.3385
±
\pm
0.0372
ATS
0.5987
±
\pm
0.0121
0.3379
±
\pm
0.0290
2.5765
±
\pm
1.4883
0.3462
±
\pm
0.0184
0.4867
±
\pm
0.0081
0.3817
±
\pm
0.1376
3.6701
±
\pm
2.4950
0.4032
±
\pm
0.0945
CoCHI
0.6100
±
\pm
0.0040
0.0854
±
\pm
0.0015
0.5649
±
\pm
0.0008
0.1941
±
\pm
0.0005
0.4847
±
\pm
0.0023
0.0383
±
\pm
0.0035
0.6168
±
\pm
0.0012
0.2146
±
\pm
0.0006
OpenBookQA
MedQA-USMLE
Method
Accuracy
↑
\uparrow
ECE
↓
\downarrow
NLL
↓
\downarrow
BS
↓
\downarrow
Accuracy
↑
\uparrow
ECE
↓
\downarrow
NLL
↓
\downarrow
BS
↓
\downarrow
Gemma-2-9B
TS
0.6080
±
\pm
0.0087
0.0686
±
\pm
0.0119
0.5410
±
\pm
0.0076
0.1848
±
\pm
0.0054
0.7714
±
\pm
0.0124
0.1782
±
\pm
0.0188
0.5109
±
\pm
0.0377
0.1829
±
\pm
0.0118
ITI
0.6100
±
\pm
0.0111
0.0682
±
\pm
0.0064
0.5438
±
\pm
0.0070
0.1848
±
\pm
0.0043
0.7927
±
\pm
0.0151
0.1725
±
\pm
0.0143
0.5091
±
\pm
0.0163
0.1708
±
\pm
0.0072
Therm.
0.6080
±
\pm
0.0087
0.2635
±
\pm
0.0266
2.4829
±
\pm
0.5178
0.2930
±
\pm
0.0223
0.7810
±
\pm
0.0114
0.1767
±
\pm
0.0298
1.7598
±
\pm
0.2096
0.1757
±
\pm
0.0205
ATS
0.6080
±
\pm
0.0087
0.3350
±
\pm
0.0165
1.9401
±
\pm
1.8405
0.3399
±
\pm
0.0090
0.7740
±
\pm
0.0164
0.1863
±
\pm
0.0131
2.2281
±
\pm
0.2476
0.1866
±
\pm
0.0141
CoCHI
0.6090
±
\pm
0.0766
0.0434
±
\pm
0.0116
0.5353
±
\pm
0.0268
0.1840
±
\pm
0.0092
0.7893
±
\pm
0.0223
0.1723
±
\pm
0.0070
0.5081
±
\pm
0.0046
0.1694
±
\pm
0.0019
LLaMA-3.1-8B
TS
0.6827
±
\pm
0.0170
0.0618
±
\pm
0.0106
0.5776
±
\pm
0.0125
0.1853
±
\pm
0.0066
0.7360
±
\pm
0.0087
0.1198
±
\pm
0.0200
0.5603
±
\pm
0.0394
0.1750
±
\pm
0.0123
ITI
0.5200
±
\pm
0.1618
0.2272
±
\pm
0.2848
0.9131
±
\pm
0.6744
0.2952
±
\pm
0.2009
0.5387
±
\pm
0.0908
0.1611
±
\pm
0.0761
0.6333
±
\pm
0.0739
0.2226
±
\pm
0.0332
Therm.
0.6827
±
\pm
0.0170
0.1654
±
\pm
0.0405
1.5188
±
\pm
0.5910
0.2180
±
\pm
0.0302
0.7360
±
\pm
0.0087
0.1954
±
\pm
0.0372
1.9680
±
\pm
0.4174
0.2124
±
\pm
0.0213
ATS
0.6827
±
\pm
0.0170
0.3346
±
\pm
0.0658
2.6951
±
\pm
1.5194
0.3195
±
\pm
0.0403
0.7360
±
\pm
0.0087
0.2432
±
\pm
0.0119
3.1290
±
\pm
0.1205
0.2430
±
\pm
0.0082
CoCHI
0.6700
±
\pm
0.0040
0.0523
±
\pm
0.0193
0.5069
±
\pm
0.0090
0.1730
±
\pm
0.0035
0.7307
±
\pm
0.0186
0.0961
±
\pm
0.0169
0.5066
±
\pm
0.0121
0.1700
±
\pm
0.0048
Mistral-7B
TS
0.5100
±
\pm
0.0100
0.0673
±
\pm
0.0383
0.6016
±
\pm
0.0130
0.2076
±
\pm
0.0033
0.6707
±
\pm
0.0064
0.1489
±
\pm
0.0077
0.5720
±
\pm
0.0115
0.1987
±
\pm
0.0089
ITI
0.3567
±
\pm
0.0996
0.3583
±
\pm
0.2315
1.0117
±
\pm
0.3433
0.3684
±
\pm
0.1309
0.5193
±
\pm
0.0574
0.1522
±
\pm
0.0597
0.6011
±
\pm
0.0402
0.2089
±
\pm
0.0195
Therm.
0.5100
±
\pm
0.0100
0.2388
±
\pm
0.0647
2.0444
±
\pm
0.3463
0.3042
±
\pm
0.0360
0.6707
±
\pm
0.0064
0.2214
±
\pm
0.0398
2.0876
±
\pm
0.3632
0.2511
±
\pm
0.0222
ATS
0.5100
±
\pm
0.0100
0.4317
±
\pm
0.0040
4.2157
±
\pm
0.0519
0.4266
±
\pm
0.0012
0.6707
±
\pm
0.0064
0.2904
±
\pm
0.0064
3.0443
±
\pm
0.0280
0.2896
±
\pm
0.0046
CoCHI
0.5120
±
\pm
0.0040
0.0316
±
\pm
0.0073
0.5912
±
\pm
0.0029
0.2047
±
\pm
0.0014
0.6700
±
\pm
0.0139
0.1432
±
\pm
0.0108
0.5634
±
\pm
0.0068
0.2028
±
\pm
0.0035
5.3
Main Results
The results in Table
1
show that
CoCHI
consistently improves calibration across all datasets and models while maintaining competitive accuracy. On datasets such as
MMLU
and
MedMCQA
, CoCHI achieves clear reductions in ECE together with improved NLL and Brier Score. Similar trends are observed on
OpenBookQA
and
MedQA-USMLE
, where CoCHI attains the lowest or near-lowest calibration errors without sacrificing predictive performance. In several cases, CoCHI also improves accuracy, particularly on LLaMA-3.1-8B and Mistral-7B.
In contrast, existing methods show limited or unstable behaviour across datasets. Post-hoc methods such as TS and ATS provide only marginal improvements and can severely degrade calibration in some settings, while Thermometer often increases NLL, indicating unreliable probability estimates. ITI also exhibits high variance across models and datasets. The advantage of CoCHI is especially evident on Mistral-7B, where it consistently achieves lower ECE together with strong NLL and Brier Score performance. Overall, these results suggest that intervening on targeted causal attention heads provides more effective and stable calibration than conventional output-level adjustment methods.
Additional results are provided in Appendix
B.1
.
5.4
Ablation Study
Table 2:
Ablation study of different masking strategies on MMLU.
Mask Rule
Masked Acc
↑
\uparrow
Masked ECE
↓
\downarrow
Wrong-high facilitating only
0.2044
±
\pm
0.0038
0.4745
±
\pm
0.1477
Correct-high non-facilitating only
0.2389
±
\pm
0.0398
0.1518
±
\pm
0.0474
Correct-high interfering only
0.4267
±
\pm
0.0462
0.0694
±
\pm
0.0488
Canonical union (broad)
0.2189
±
\pm
0.0271
0.3850
±
\pm
0.1816
Random size-matched
0.2111
±
\pm
0.0077
0.4330
±
\pm
0.2736
CoCHI
0.6120
±
\pm
0.0626
0.0490
±
\pm
0.0089
The ablation results in Table
2
highlight the importance of structured, causally-informed masking. Naive strategies, such as masking only wrong-high facilitating heads or applying a broad canonical-union mask, severely degrade both accuracy and calibration (accuracy 0.2044/0.2189; ECE 0.4745/0.3850), suggesting that indiscriminate head removal disrupts essential model functionality. More targeted variants also fail to achieve a satisfactory trade-off: masking correct-high interfering heads lowers ECE to 0.0694 but substantially reduces accuracy to 0.4267, while random size-matched masking performs poorly (accuracy 0.2111, ECE 0.4330). In contrast,
CoCHI
achieves the best balance, with accuracy 0.6120 and ECE 0.0490. These results show that effective intervention depends not only on identifying problematic heads, but also on selecting a compact set of high-impact components through canonical-union design and top-
k
k
ranking.
5.5
Sensitivity Analysis
Table 3:
Sensitivity analysis of the confidence threshold
τ
c
\tau_{c}
on MMLU.
τ
c
\tau_{c}
Accuracy
↑
\uparrow
ECE
↓
\downarrow
NLL
↓
\downarrow
BS
↓
\downarrow
0.2
0.5933
±
\pm
0.0217
0.0555
±
\pm
0.0096
0.5385
±
\pm
0.0075
0.1808
±
\pm
0.0032
0.3
0.6060
±
\pm
0.0059
0.0643
±
\pm
0.0102
0.5319
±
\pm
0.0043
0.1781
±
\pm
0.0017
0.4
0.5860
±
\pm
0.0118
0.0665
±
\pm
0.0108
0.5276
±
\pm
0.0058
0.1761
±
\pm
0.0025
0.5
0.6120
±
\pm
0.0626
0.0490
±
\pm
0.0089
0.5168
±
\pm
0.0236
0.1743
±
\pm
0.0008
0.7
0.5873
±
\pm
0.0377
0.0705
±
\pm
0.0099
0.5548
±
\pm
0.0212
0.1873
±
\pm
0.0083
0.9
0.5933
±
\pm
0.0081
0.0696
±
\pm
0.0277
0.5255
±
\pm
0.0059
0.1748
±
\pm
0.0022
Table
3
presents the sensitivity analysis of the confidence threshold
τ
c
\tau_{c}
. Overall, the proposed method remains relatively stable across different threshold settings, indicating that its performance is not highly sensitive to the choice of
τ
c
\tau_{c}
. Among all configurations,
τ
c
=
0.5
\tau_{c}=0.5
achieves the best overall trade-off, yielding the lowest ECE, while also obtaining competitive Accuracy, NLL, and Brier Score values. In contrast, very high thresholds (e.g.,
τ
c
=
0.7
\tau_{c}=0.7
and
0.9
0.9
) lead to noticeable degradation in calibration quality, reflected by increased ECE and NLL. Lower thresholds such as
0.2
0.2
provide reasonable calibration performance but slightly reduce predictive accuracy. These results suggest that moderate confidence thresholds are more effective for balancing classification performance and uncertainty calibration.
5.6
Efficiency Analysis
Table 4:
Efficiency comparison of calibration methods using 40 calibration samples on MMLU.
Method
GPU
Cal. time (s)
↓
\downarrow
Artifact size
↓
\downarrow
Inf.
Prunable
TS
No
0.5
4 B
Negligible
No
ATS
No
25.8
16 B
Negligible
No
ITI
Yes
18.4
16 KB
O
⁡
(
k
⋅
d
)
O(k\cdot d)
No
Therm.
No
19.4
1.0 MB
O
⁡
(
H
⋅
C
)
O(H\cdot C)
No
CoCHI
Yes
69.9
40 B
None
Yes
Table
4
presents an efficiency comparison across calibration methods, highlighting a clear trade-off between calibration cost and inference overhead. CoCHI requires GPU computation during a one-time calibration phase (69.9s), but produces an extremely compact artifact (40 B) and introduces zero inference overhead, as the intervention is implemented by directly zeroing selected attention heads. In contrast, methods such as ITI and Thermometer incur additional computation at every forward pass (e.g.,
O
⁡
(
k
⋅
d
)
O(k\cdot d)
and
O
⁡
(
H
⋅
C
)
O(H\cdot C)
, respectively), leading to ongoing runtime costs and significantly larger artifacts (up to 1.0 MB). Lightweight post-hoc approaches such as TS and ATS have minimal calibration cost (0.5s and 25.8s) and negligible inference overhead, but do not modify the model’s internal behaviour and therefore lack structural impact.
A key advantage of CoCHI is its
prunability
: the masked heads can be permanently removed, yielding a smaller model with no runtime wrapper. Overall, CoCHI shifts the computational burden from continuous inference to a one-time structural calibration step, offering a more deployment-efficient solution for improving model reliability. More results are available in Appendix
B.2
.
5.7
Case Study
Figure 2:
ECE comparison between the unmasked model and CoCHI on
correct_low
and
wrong_high
subsets.
Figure
2
presents a per-class calibration comparison between the unmasked baseline and our method across five datasets, focusing on correct predictions with low confidence (left) and wrong predictions with high confidence (right). While our method is primarily designed to address
wrong_high
errors, we observe consistent improvements in both regimes. In the
correct_low
subset, our method reduces ECE across all datasets (e.g., 0.10 on MMLU and 0.09 on MedMCQA), indicating improved confidence alignment for underconfident correct predictions. In the more challenging
wrong_high
subset, our method also consistently lowers ECE, albeit with smaller margins. This suggests that suppressing causally relevant heads not only mitigates overconfident errors but also improves overall confidence stability.
6
Conclusion
In this work, we study overconfident errors in large language models and argue that miscalibration should be addressed not only at the output level, but also through the internal mechanisms that give rise to unreliable confidence estimates. We propose CoCHI, a class-oriented causal head intervention framework that decomposes predictions by correctness and confidence, identifies attention heads associated with distinct calibration behaviours, and performs targeted inference-time masking without updating model parameters. Across multiple LLMs and five multiple-choice QA benchmarks, CoCHI consistently improves calibration metrics while maintaining competitive predictive accuracy. The ablation and sensitivity analyses further show that reliable calibration depends on structured causal selection rather than indiscriminate head removal. Moreover, while CoCHI primarily targets
wrong_high
errors, it also yields improvements in
correct_low
cases. These findings support a mechanism-aware view of calibration, linking model reliability to identifiable internal structures rather than treating it solely as a post-hoc output adjustment problem.
Limitations.
This work focuses on multiple-choice question answering, where confidence can be naturally defined over a fixed answer space. Extending CoCHI to open-ended generation, long-form reasoning, and multi-turn interaction requires further investigation, especially when correctness and confidence are harder to define. In addition, our current intervention operates at the attention-head level, which provides an efficient and interpretable unit for masking, but may not capture all sources of miscalibration arising from MLP layers, residual streams, or cross-layer interactions.
Acknowledgements
We acknowledge the RMIT Advanced Compute Environment (RACE) for providing the high-performance computing resources and infrastructure that supported this research. We also thank Patrick Taylor for his valuable technical support and assistance.
References
[1]
Y. Abbasi-Yadkori, I. Kuzborskij, A. György, and C. Szepesvári
(2024)
To believe or not to believe your LLM: iterative prompting for estimating epistemic uncertainty
.
In
Advances in Neural Information Processing Systems 37: Annual Conference
on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver,
BC, Canada, December 10 - 15, 2024
,
External Links:
Link
Cited by:
§1
.
[2]
M. Steyvers, H. T. Lemus, A. Kumar, C. G. Belém, S. Karny, X. Hu, L. W. Mayer, and P. Smyth
(2025)
What large language models know and what people think they know
.
Nature Machine Intelligence
7
(
2
),
pp. 221–231
.
External Links:
Link
,
Document
Cited by:
§1
.
[3]
J. Ren, J. Du, B. Li, Z. Xu, X. Zheng, H. Jia, S. Ma, X. Xu, and F. Xia
(2026)
Spiking graph predictive coding for reliable OOD generalization
.
In
Proceedings of the ACM Web Conference 2026, WWW 2026, Dubai, United
Arab Emirates, originally scheduled for April 13-17, 2026, rescheduled
for June 29 - July 3, 2026
,
pp. 9056–9067
.
External Links:
Link
,
Document
Cited by:
§1
.
[4]
V. Nguyen, Z. Xu, J. Chan, E. He, F. Xia, and X. Zhang
(2026)
Hallucinate less by thinking more: aspect-based causal abstention for large language models
.
In
Fortieth AAAI Conference on Artificial Intelligence, Thirty-Eighth
Conference on Innovative Applications of Artificial Intelligence,
Sixteenth Symposium on Educational Advances in Artificial Intelligence,
AAAI 2026, Singapore, January 20-27, 2026
,
pp. 32555–32563
.
External Links:
Link
,
Document
Cited by:
§1
.
[5]
OpenAI
(2023)
GPT-4 technical report
.
CoRR
abs/2303.08774
.
External Links:
Link
,
Document
,
2303.08774
Cited by:
§1
.
[6]
DeepSeek-AI
(2024)
DeepSeek-v3 technical report
.
CoRR
abs/2412.19437
.
External Links:
Link
,
Document
,
2412.19437
Cited by:
§1
.
[7]
L. Team
(2024)
The llama 3 herd of models
.
CoRR
abs/2407.21783
.
External Links:
Link
,
Document
,
2407.21783
Cited by:
§1
,
§5.1
.
[8]
Y. Bang, Z. Ji, A. Schelten, A. Hartshorn, T. Fowler, C. Zhang, N. Cancedda, and P. Fung
(2025)
HalluLens: LLM hallucination benchmark
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria,
July 27 - August 1, 2025
,
pp. 24128–24156
.
External Links:
Link
,
Document
Cited by:
§1
.
[9]
A. Ravichander, S. Ghela, D. Wadden, and Y. Choi
(2025)
HALoGEN: fantastic LLM hallucinations and where to find them
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria,
July 27 - August 1, 2025
,
pp. 1402–1425
.
External Links:
Link
,
Document
Cited by:
§1
.
[10]
S. Wu, H. Fei, L. Pan, W. Y. Wang, S. Yan, and T. Chua
(2025)
Combating multimodal LLM hallucination via bottom-up holistic reasoning
.
In
Thirty-Ninth AAAI Conference on Artificial Intelligence, Thirty-Seventh
Conference on Innovative Applications of Artificial Intelligence,
Fifteenth Symposium on Educational Advances in Artificial Intelligence,
AAAI 2025, Philadelphia, PA, USA, February 25 - March 4, 2025
,
pp. 8460–8468
.
External Links:
Link
,
Document
Cited by:
§1
.
[11]
A. Okutomi
(2025)
Stable but miscalibrated: A kantian view on overconfidence from filters to large language models
.
CoRR
abs/2510.14925
.
External Links:
Link
,
Document
,
2510.14925
Cited by:
§1
.
[12]
Y. Yang, Z. Xu, J. Li, C. Ma, J. Chan, M. Sanderson, X. Zheng, and Y. Ren
(2026)
Mitigating bias in large language model based question answering through causal front door prompting
.
In
Proceedings of the 49th International ACM SIGIR Conference on
Research and Development in Information Retrieval, SIGIR 2026, MelbourneVICAustralia,
July 20-24, 2026
,
pp. 2208–2218
.
External Links:
Link
,
Document
Cited by:
§1
.
[13]
D. Ulmer, M. Gubri, H. Lee, S. Yun, and S. J. Oh
(2024)
Calibrating large language models using their generations only
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand,
August 11-16, 2024
,
pp. 15440–15459
.
External Links:
Link
,
Document
Cited by:
§1
.
[14]
C. Huang, L. Huang, J. Leng, J. Liu, and J. Huang
(2026)
CaTS: calibrated test-time scaling for efficient LLM reasoning
.
In
The Fourteenth International Conference on Learning Representations,
ICLR 2026, Rio de Janeiro, Brazil, April 23-27, 2026
,
External Links:
Link
Cited by:
§1
.
[15]
J. Ren, B. Li, Z. Xu, X. Zhang, H. M. Fayek, and X. Li
(2026)
When to trust: A causality-aware calibration framework for accurate knowledge graph retrieval-augmented generation
.
In
Proceedings of the ACM Web Conference 2026, WWW 2026, Dubai, United
Arab Emirates, originally scheduled for April 13-17, 2026, rescheduled
for June 29 - July 3, 2026
,
pp. 3859–3869
.
External Links:
Link
,
Document
Cited by:
§1
,
§2
.
[16]
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
(2017)
On calibration of modern neural networks
.
In
Proceedings of the 34th International Conference on Machine Learning,
ICML 2017, Sydney, NSW, Australia, 6-11 August 2017
,
Proceedings of Machine Learning Research
, Vol.
70
,
pp. 1321–1330
.
External Links:
Link
Cited by:
§1
,
§2
,
§5.2
,
§5.2
.
[17]
A. Nam, H. Conklin, Y. Yang, T. Griffiths, J. D. Cohen, and S. Leslie
(2025)
Causal head gating: A framework for interpreting roles of attention heads in transformers
.
In
Advances in Neural Information Processing Systems 38: Annual Conference
on Neural Information Processing Systems 2025, NeurIPS 2025, San Diego,
CA, USA, December 2-7, 2025 / Mexico City, Mexico, November 30 - December
5, 2025
,
External Links:
Link
Cited by:
§1
,
§2
,
§4.3
.
[18]
J. Vig, S. Gehrmann, Y. Belinkov, S. Qian, D. Nevo, Y. Singer, and S. M. Shieber
(2020)
Investigating gender bias in language models using causal mediation analysis
.
In
Advances in Neural Information Processing Systems 33: Annual Conference
on Neural Information Processing Systems 2020, NeurIPS 2020, December
6-12, 2020, virtual
,
External Links:
Link
Cited by:
§1
.
[19]
K. Meng, D. Bau, A. Andonian, and Y. Belinkov
(2022)
Locating and editing factual associations in GPT
.
In
Advances in Neural Information Processing Systems 35: Annual Conference
on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans,
LA, USA, November 28 - December 9, 2022
,
External Links:
Link
Cited by:
§1
.
[20]
D. Cheng, Z. Xu, J. Li, L. Liu, K. Yu, T. D. Le, and J. Liu
(2026)
Linking model intervention to causal interpretation in model explanation
.
Pattern Recognit.
173
,
pp. 112814
.
External Links:
Link
,
Document
Cited by:
§1
.
[21]
Z. Xu, D. Cheng, J. Li, J. Liu, L. Liu, and K. Wang
(2023)
Disentangled representation for causal mediation analysis
.
In
Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI
2023, Thirty-Fifth Conference on Innovative Applications of Artificial
Intelligence, IAAI 2023, Thirteenth Symposium on Educational Advances
in Artificial Intelligence, EAAI 2023, Washington, DC, USA, February
7-14, 2023
,
pp. 10666–10674
.
External Links:
Link
,
Document
Cited by:
§1
.
[22]
D. J. C. Mackay
(1992)
Bayesian methods for adaptive models
.
California Institute of Technology
.
Cited by:
§2
.
[23]
A. Graves
(2011)
Practical variational inference for neural networks
.
In
Advances in Neural Information Processing Systems 24: 25th Annual
Conference on Neural Information Processing Systems 2011. Proceedings
of a meeting held 12-14 December 2011, Granada, Spain
,
J. Shawe-Taylor, R. S. Zemel, P. L. Bartlett, F. C. N. Pereira, and K. Q. Weinberger (Eds.)
,
pp. 2348–2356
.
External Links:
Link
Cited by:
§2
.
[24]
C. Blundell, J. Cornebise, K. Kavukcuoglu, and D. Wierstra
(2015)
Weight uncertainty in neural network
.
In
Proceedings of the 32nd International Conference on Machine Learning,
ICML 2015, Lille, France, 6-11 July 2015
,
JMLR Workshop and Conference Proceedings
, Vol.
37
,
pp. 1613–1622
.
External Links:
Link
Cited by:
§2
.
[25]
J. M. Hernández-Lobato and R. P. Adams
(2015)
Probabilistic backpropagation for scalable learning of bayesian neural networks
.
In
Proceedings of the 32nd International Conference on Machine Learning,
ICML 2015, Lille, France, 6-11 July 2015
,
JMLR Workshop and Conference Proceedings
, Vol.
37
,
pp. 1861–1869
.
External Links:
Link
Cited by:
§2
.
[26]
M. Welling and Y. W. Teh
(2011)
Bayesian learning via stochastic gradient langevin dynamics
.
In
Proceedings of the 28th International Conference on Machine Learning,
ICML 2011, Bellevue, Washington, USA, June 28 - July 2, 2011
,
pp. 681–688
.
External Links:
Link
Cited by:
§2
.
[27]
B. Lakshminarayanan, A. Pritzel, and C. Blundell
(2017)
Simple and scalable predictive uncertainty estimation using deep ensembles
.
In
Advances in Neural Information Processing Systems 30: Annual Conference
on Neural Information Processing Systems 2017, December 4-9, 2017,
Long Beach, CA, USA
,
pp. 6402–6413
.
External Links:
Link
Cited by:
§2
.
[28]
Y. Xia, P. H. L. de Araujo, K. Zaporojets, and B. Roth
(2025)
Influences on LLM calibration: A study of response agreement, loss functions, and prompt styles
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria,
July 27 - August 1, 2025
,
pp. 3740–3761
.
External Links:
Link
,
Document
Cited by:
§2
.
[29]
J. Xie, A. S. Chen, Y. Lee, E. Mitchell, and C. Finn
(2024)
Calibrating language models with adaptive temperature scaling
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural
Language Processing, EMNLP 2024, Miami, FL, USA, November 12-16,
2024
,
pp. 18128–18138
.
External Links:
Link
,
Document
Cited by:
§2
,
§5.2
.
[30]
M. Shen, S. Das, K. H. Greenewald, P. Sattigeri, G. W. Wornell, and S. Ghosh
(2024)
Thermometer: towards universal calibration for large language models
.
In
Forty-first International Conference on Machine Learning, ICML 2024,
Vienna, Austria, July 21-27, 2024
,
Proceedings of Machine Learning Research
, Vol.
235
,
pp. 44687–44711
.
External Links:
Link
Cited by:
§2
,
§5.2
.
[31]
X. Liu, M. Khalifa, and L. Wang
(2024)
LitCab: lightweight language model calibration over short- and long-form responses
.
In
The Twelfth International Conference on Learning Representations,
ICLR 2024, Vienna, Austria, May 7-11, 2024
,
External Links:
Link
Cited by:
§2
.
[32]
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. D. Manning
(2023)
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural
Language Processing, EMNLP 2023, Singapore, December 6-10, 2023
,
pp. 5433–5442
.
External Links:
Link
,
Document
Cited by:
§2
.
[33]
M. Zhang, J. He, T. Ji, and C. Lu
(2024)
Don’t go to extremes: revealing the excessive sensitivity and calibration limitations of llms in implicit hate speech detection
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand,
August 11-16, 2024
,
pp. 12073–12086
.
External Links:
Link
,
Document
Cited by:
§2
.
[34]
K. Zhou, D. Jurafsky, and T. Hashimoto
(2023)
Navigating the grey area: how expressions of uncertainty and overconfidence affect language models
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural
Language Processing, EMNLP 2023, Singapore, December 6-10, 2023
,
pp. 5506–5524
.
External Links:
Link
,
Document
Cited by:
§2
.
[35]
S. J. Mielke, A. Szlam, E. Dinan, and Y. Boureau
(2022)
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
§2
.
[36]
K. Li, O. Patel, F. B. Viégas, H. Pfister, and M. Wattenberg
(2023)
Inference-time intervention: eliciting truthful answers from a language model
.
In
Advances in Neural Information Processing Systems 36: Annual Conference
on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans,
LA, USA, December 10 - 16, 2023
,
External Links:
Link
Cited by:
§2
,
§5.2
.
[37]
A. Vazhentsev, L. Rvanova, G. Kuzmin, E. Fadeeva, I. Lazichny, A. Panchenko, M. Panov, T. Baldwin, M. Sachan, P. Nakov, and A. Shelmanov
(2025)
Uncertainty-aware attention heads: efficient unsupervised uncertainty quantification for llms
.
CoRR
abs/2505.20045
.
External Links:
Link
,
Document
,
2505.20045
Cited by:
§2
.
[38]
K. R. Wang, A. Variengien, A. Conmy, B. Shlegeris, and J. Steinhardt
(2023)
Interpretability in the wild: a circuit for indirect object identification in GPT-2 small
.
In
The Eleventh International Conference on Learning Representations,
ICLR 2023, Kigali, Rwanda, May 1-5, 2023
,
External Links:
Link
Cited by:
§2
.
[39]
A. Conmy, A. N. Mavor-Parker, A. Lynch, S. Heimersheim, and A. Garriga-Alonso
(2023)
Towards automated circuit discovery for mechanistic interpretability
.
In
Advances in Neural Information Processing Systems 36: Annual Conference
on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans,
LA, USA, December 10 - 16, 2023
,
External Links:
Link
Cited by:
§2
.
[40]
A. R. Hsu, G. Zhou, Y. Cherapanamjeri, Y. Huang, A. Y. Odisho, P. R. Carroll, and B. Yu
(2025)
Efficient automated circuit discovery in transformers using contextual decomposition
.
In
The Thirteenth International Conference on Learning Representations,
ICLR 2025, Singapore, April 24-28, 2025
,
External Links:
Link
Cited by:
§2
.
[41]
J. Pearl
(2009)
Causality
.
Cambridge university press
.
Cited by:
§2
.
[42]
A. Geiger, H. Lu, T. Icard, and C. Potts
(2021)
Causal abstractions of neural networks
.
In
Advances in Neural Information Processing Systems 34: Annual Conference
on Neural Information Processing Systems 2021, NeurIPS 2021, December
6-14, 2021, virtual
,
pp. 9574–9586
.
External Links:
Link
Cited by:
§2
.
[43]
J. Kaddour, A. Lynch, Q. Liu, M. J. Kusner, and R. Silva
(2025)
Causal machine learning: A survey and open problems
.
Foundations and Trends in Optimization
9
(
1-2
),
pp. 1–247
.
External Links:
Link
,
Document
Cited by:
§2
.
[44]
Z. Wu, A. Geiger, J. Rozner, E. Kreiss, H. Lu, T. Icard, C. Potts, and N. D. Goodman
(2022)
Causal distillation for language models
.
In
Proceedings of the 2022 Conference of the North American Chapter of
the Association for Computational Linguistics: Human Language Technologies,
NAACL 2022, Seattle, WA, United States, July 10-15, 2022
,
pp. 4288–4295
.
External Links:
Link
,
Document
Cited by:
§2
.
[45]
X. Li, S. Yang, Z. Xu, F. Xia, Q. Z. Sheng, and L. Yao
(2026)
Causal abstraction learning for multi-modal grounded planning
.
In
Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery
and Data Mining V.2, KDD 2026, Jeju Island, Korea, August 9-13,
2026
,
pp. 2790–2801
.
External Links:
Link
,
Document
Cited by:
§2
.
[46]
T. Zhao, Y. He, W. Zheng, Y. Zhang, and C. Chen
(2026)
Wired for overconfidence: A mechanistic perspective on inflated verbalized confidence in llms
.
CoRR
abs/2604.01457
.
External Links:
Link
,
Document
,
2604.01457
Cited by:
§2
.
[47]
A. Joshi, A. Ahmad, and A. Modi
(2025)
Calibration across layers: understanding calibration evolution in llms
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural
Language Processing, EMNLP 2025, Suzhou, China, November 4-9, 2025
,
pp. 14686–14714
.
External Links:
Link
,
Document
Cited by:
§2
.
[48]
G. Team
(2024)
Gemma 2: improving open language models at a practical size
.
CoRR
abs/2408.00118
.
External Links:
Link
,
Document
,
2408.00118
Cited by:
§5.1
.
[49]
A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford, D. S. Chaplot, D. de Las Casas, F. Bressand, G. Lengyel, G. Lample, L. Saulnier, L. R. Lavaud, M. Lachaux, P. Stock, T. L. Scao, T. Lavril, T. Wang, T. Lacroix, and W. E. Sayed
(2023)
Mistral 7b
.
CoRR
abs/2310.06825
.
External Links:
Link
,
Document
,
2310.06825
Cited by:
§5.1
.
[50]
D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt
(2021)
Measuring massive multitask language understanding
.
In
9th International Conference on Learning Representations, ICLR 2021,
Virtual Event, Austria, May 3-7, 2021
,
External Links:
Link
Cited by:
§5.2
.
[51]
A. Pal, L. K. Umapathi, and M. Sankarasubbu
(2022)
MedMCQA: A large-scale multi-subject multi-choice dataset for medical domain question answering
.
In
Conference on Health, Inference, and Learning, CHIL 2022, 7-8 April
2022, Virtual Event
,
Proceedings of Machine Learning Research
, Vol.
174
,
pp. 248–260
.
External Links:
Link
Cited by:
§5.2
.
[52]
T. Mihaylov, P. Clark, T. Khot, and A. Sabharwal
(2018)
Can a suit of armor conduct electricity? A new dataset for open book question answering
.
In
Proceedings of the 2018 Conference on Empirical Methods in Natural
Language Processing, Brussels, Belgium, October 31 - November 4, 2018
,
pp. 2381–2391
.
External Links:
Link
,
Document
Cited by:
§5.2
.
[53]
D. Jin, E. Pan, N. Oufattole, W. Weng, H. Fang, and P. Szolovits
(2021)
What disease does this patient have? a large-scale open domain question answering dataset from medical exams
.
Applied Sciences
11
(
14
).
External Links:
Link
,
ISSN 2076-3417
,
Document
Cited by:
§5.2
.
[54]
J. Welbl, N. F. Liu, and M. Gardner
(2017)
Crowdsourcing multiple choice science questions
.
In
Proceedings of the 3rd Workshop on Noisy User-generated Text, NUT@EMNLP
2017, Copenhagen, Denmark, September 7, 2017
,
pp. 94–106
.
External Links:
Link
,
Document
Cited by:
§5.2
.
Appendix A
Dataset Preparation and Experimental Pipeline
This section details the data preparation and experimental pipeline to ensure reproducibility.
A.1
Datasets
We use five publicly available multiple-choice question answering datasets (as shown in Table
5
) from HuggingFace, covering general knowledge, science, and medical domains. All datasets are formatted as four-option multiple-choice questions with a single correct answer.
Table 5:
Statistical summary of the datasets.
Dataset
Domain
# Questions
MMLU
Multi-domain knowledge
14,042
MedQA-USMLE
Medical exam
11,451
OpenBookQA
Science
∼
\sim
4,200
SciQ
Science
13,679
MedMCQA
Medical exam
187,005
A.2
Data Cleaning and Standardisation
All datasets are converted into a unified format containing: question ID, dataset source, question text, four answer choices (A–D), and the correct label. We remove samples that: (i) do not contain exactly four options, or (ii) have missing or invalid answer labels.
SciQ Adjustment.
In SciQ, the correct answer appears in a fixed position. To avoid positional bias, we cyclically rotate answer options to ensure a uniform distribution.
A.3
Prompt Formatting
All inputs follow a unified zero-shot prompt:
Answer the following multiple choice question with a single letter: A, B, C, or D.
Question: [question text]
A. [choice 1]
B. [choice 2]
C. [choice 3]
D. [choice 4]
Answer:
No demonstrations or additional context are provided.
A.4
Training Example Selection
From the fit pool, we sample a balanced calibration subset:
•
up to 10 examples per class,
•
maximum of 40 samples per dataset.
This simulates a low-resource calibration setting.
A.5
Top-
k
k
Head Selection
We determine the number of masked heads
k
k
via grid search over
k
∈
{
1
,
…
,
20
}
k\in\{1,\dots,20\}
. Selection is based on minimising Expected Calibration Error (ECE), subject to an accuracy drop constraint of at most 1% relative to the unmodified model.
A single
k
k
is selected per model and applied across all datasets to capture model-level calibration properties. The selected values are
k
=
10
k=10
for LLaMA-3.1-8B, and
k
=
8
k=8
for Gemma-2-9B and Mistral-7B.
Table 6:
Results on SciQ. Best results are highlighted in bold.
Method
Acc
↑
\uparrow
ECE
↓
\downarrow
NLL
↓
\downarrow
BS
↓
\downarrow
Gemma-2-9B
TS
0.9173
±
\pm
0.0012
0.0579
±
\pm
0.0184
0.4699
±
\pm
0.4226
0.0641
±
\pm
0.0094
ITI
0.9253
±
\pm
0.0083
0.1027
±
\pm
0.0091
0.2337
±
\pm
0.0076
0.0617
±
\pm
0.0025
Therm.
0.9223
±
\pm
0.0021
0.0609
±
\pm
0.0066
1.0836
±
\pm
0.1824
0.0599
±
\pm
0.0068
ATS
0.9173
±
\pm
0.0012
0.0607
±
\pm
0.0067
1.1578
±
\pm
0.1183
0.0602
±
\pm
0.0065
CoCHI
0.9353
±
\pm
0.1069
0.0563
±
\pm
0.0199
0.2309
±
\pm
0.1276
0.0548
±
\pm
0.0472
LLaMA-3.1-8B
TS
0.8790
±
\pm
0.0210
0.0354
±
\pm
0.0109
0.2377
±
\pm
0.0145
0.0721
±
\pm
0.0045
ITI
0.8647
±
\pm
0.0311
0.0359
±
\pm
0.0176
0.3032
±
\pm
0.0329
0.0921
±
\pm
0.0139
Therm.
0.8920
±
\pm
0.0131
0.0738
±
\pm
0.0112
0.9514
±
\pm
0.2711
0.0807
±
\pm
0.0065
ATS
0.8790
±
\pm
0.0210
0.0932
±
\pm
0.0219
1.4970
±
\pm
0.2712
0.0928
±
\pm
0.0195
CoCHI
0.9020
±
\pm
0.0020
0.0330
±
\pm
0.0010
0.2266
±
\pm
0.0012
0.0676
±
\pm
0.0004
Mistral-7B
TS
0.8667
±
\pm
0.0150
0.0764
±
\pm
0.0048
0.3057
±
\pm
0.0402
0.0944
±
\pm
0.0045
ITI
0.5720
±
\pm
0.1512
0.2095
±
\pm
0.1429
0.6363
±
\pm
0.1672
0.2249
±
\pm
0.0680
Therm.
0.8467
±
\pm
0.0310
0.0986
±
\pm
0.0084
1.4162
±
\pm
0.0701
0.0978
±
\pm
0.0073
ATS
0.8667
±
\pm
0.0150
0.1056
±
\pm
0.0139
1.6920
±
\pm
0.2413
0.1049
±
\pm
0.0134
CoCHI
0.8773
±
\pm
0.0046
0.0730
±
\pm
0.0116
0.3030
±
\pm
0.0144
0.0903
±
\pm
0.0046
Appendix B
Additional Results
B.1
Main results
Table
6
confirms the effectiveness of our method on SciQ, demonstrating consistent improvements in calibration across all models while maintaining strong predictive performance. On Gemma-2-9B, our method achieves the best overall calibration, reducing ECE and improving both NLL and Brier Score , while matching the highest accuracy. On LLaMA-3.1-8B, the gains are even more pronounced: our method simultaneously achieves the best performance across all four metrics, improving accuracy, lowering ECE, and reducing both NLL and Brier Score. Similar trends are observed on Mistral-7B, where our method achieves the best results across all metrics, outperforming the strongest baseline (ATS) in both calibration and accuracy. These results indicate that the proposed intervention consistently improves confidence alignment without sacrificing predictive quality.
In contrast, baseline methods exhibit unstable and inconsistent behaviour. ITI achieves competitive accuracy on Gemma-2-9B but significantly worsens calibration, while on Mistral-7B it severely degrades both accuracy and calibration. Post-hoc methods such as TS and ATS provide moderate or inconsistent calibration improvements but often fail to jointly optimise NLL and Brier Score, with ATS in particular showing substantial degradation in probabilistic metrics (e.g., NLL exceeding 1.0 across models). Thermometer similarly leads to large increases in NLL, indicating unreliable probability estimates. Overall, these results reinforce our central claim: calibration is better improved by targeting internal causal mechanisms rather than relying on output-level adjustments, leading to more stable and reliable performance across diverse models.
B.2
Efficiency Analysis
Table
7
shows that the calibration cost of our method scales predictably with model size while remaining practical. The average calibration time increases from 39 s for Mistral-7B to 58 s for LLaMA-3.1-8B and 88 s for Gemma-2-9B, reflecting the expected growth in forward-pass complexity, yet all models complete calibration within roughly 1–1.5 minutes. The variance is moderate (std
≈
\approx
20–23 s), indicating stable computational behaviour. Peak GPU memory ranges from 28.1 GiB to 46.2 GiB, increasing with model size but remaining within the capacity of standard high-end GPUs. Notably, these costs include multiple class-conditioned forward passes, which are essential to our method, yet remain comparable to inference-time intervention baselines. Overall, the results indicate that the calibration procedure introduces only moderate overhead, scales with model size, and is practical for real-world deployment.
Table 7:
Calibration time (s; mean
±
\pm
std) of CoCHI across three model families, averaged over 15 runs per model. Costs include class-conditioned forward passes and exclude model loading, and scale with model size while remaining practical.
Model
Cal. time (s)
↓
\downarrow
Min
Max
Peak GPU (GiB)
Mistral-7B-v0.1
39
±
\pm
21
21
80
28.1
Llama-3.1-8B
58
±
\pm
20
41
93
30.4
Gemma-2-9B
88
±
\pm
23
72
159
46.2