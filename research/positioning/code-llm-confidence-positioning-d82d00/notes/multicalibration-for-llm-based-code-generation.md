---
title: Multicalibration for LLM-based Code Generation
id: multicalibration-for-llm-based-code-generation
tags:
- code-llm-calibration-aaai27-eabf3f
- multicalibration
- post-hoc-calibration
- brier-skill-score
- code-llm-confidence-positioning-d82d00
created: '2026-07-17T18:30:49.732341Z'
updated: '2026-11-09T23:27:43.607065Z'
source: https://arxiv.org/html/2512.08810
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:49.731663Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Multicalibration for LLM-based Code Generation (arXiv 2512.08810): four
  group-conditional calibrators on token likelihoods for Qwen3 Coder, GPT-OSS, DeepSeek-R1-Distill
  over LiveCodeBench v6, MultiPL-E, McEval; correctness from benchmark unit tests.
  FULL TEXT (HTML, ~7.7k words). Verdict: L1 near occupant (post-hoc calibration of
  code correctness on execution labels, LiveCodeBench release_v6 as leakage control);
  does not cover probes, verbal, or routing. L4 slight (group = complexity, length,
  language, not per-requirement).'
---

Multicalibration for LLM-based Code Generation
Multicalibration for LLM-based Code Generation
Viola Campos
viola.campos@hs-rm.de
0009-0004-0188-6154
RheinMain University of Applied Sciences
Wiesbaden
Germany
,
Robin Kuschnereit
robin.kuschnereit@gmail.com
RheinMain University of Applied Sciences
Wiesbaden
Germany
and
Adrian Ulges
adrian.ulges@hs-rm.de
0009-0001-1915-2464
RheinMain University of Applied Sciences
Wiesbaden
Germany
Abstract.
As AI-based code generation becomes widespread, researchers are investigating the calibration of code LLMs — ensuring their confidence scores faithfully represent the true likelihood of code correctness.
To do so, we investigate
multicalibration
, which can capture additional factors about a coding problem, such as complexity, code length, or programming language used. We study four multicalibration approaches on three function synthesis benchmarks, using latest-generation code LLMs (Qwen3 Coder, GPT-OSS, DeepSeek-R1-Distill). Our results demonstrate that multicalibration can yield distinct improvements over both uncalibrated token likelihoods (
+
1.03
+1.03
in skill score) and baseline calibrations (
+
0.37
+0.37
in skill score). We study the influence of the aforementioned factors in ablations, and make our dataset (consisting of code generations, likelihoods, and correctness labels) available for future research on code LLM calibration.
Calibration, Uncertainty Estimation, Code LLMs
†
†
copyright:
none
†
†
conference:
arXiv preprint; 2025;
†
†
journalyear:
2025
†
†
ccs:
Computing methodologies Natural language generation
†
†
ccs:
Software and its engineering Functionality
1.
Introduction
AI-based code generators are fundamentally transforming software development practice: By prompting Large Language Models (LLMs), code can be produced and modified much faster and easier, leading to substantial efficiency gains and reducing the knowledge level required by programmers
(
cui2024effects
)
.
However, this promise of higher efficiency comes with the risk of degrading code quality, as LLMs (being probabilistic models) are inherently unreliable
(
ChenLD24deep_dive
;
TambonDNKDA25
)
and developers get overwhelmed as more and more code is generated.
Therefore, approaches are required to support developers with reviewing code efficiently.
Two such approaches are
uncertainty estimation
and
calibration
. Both are closely related: Uncertainty estimation (UE) quantifies the model’s confidence level regarding the correctness of its prediction,
and calibration corrects the model’s confidence scores to better reflect the expected correctness.
Applied to code LLMs, such approaches could pinpoint uncertain predictions, which would improve the efficiency of code reviewing and reduce its mental load.
Uncertainty estimation and calibration of LLMs have been studied
mostly for
natural language understanding (NLU)
tasks,
where hallucinations pose a well-known problem
(
liu25survey
)
.
There are only few works
for
code LLMs
, particularly when it comes to
post-hoc calibration
(
Spiess0PPRAJDA25
)
.
In this paper, we argue that a successful calibration of code LLMs should take additional code-related information into account. This could come in various forms, such as complexity measures of the code or its specification, or the programming language used.
Though this information could easily be collected and leveraged in a calibration,
we are not aware of any studies on the subject. We fill this gap by using
multicalibration
(
HebertJohnsonK18
)
, which groups inputs according to semantic facets and applies a group-specific calibration, and has been applied for hallucination detection in question answering before
(
DetommasoLF024
)
. We apply multi-calibration to code generation by grouping coding problems by complexity and/or programming languague. Thereby, our contributions are the following:
•
To the best of our knowledge, our study is the first to investigate multicalibration for code generation. We investigate four multicalibration approaches, using groups based on complexity, code length, prompt length, and the programming language used.
•
We conduct an evaluation
using latest open-weight reasoning models (namely
Qwen3-Coder-30B-A3B-Instruct
(
yang25qwen3
)
,
OpenAI GPT-OSS-20B
(
openai2025gptoss120bgptoss20bmodel
)
and
DeepSeek-R1-Distill-Qwen-32B
(
guo25deepseek
)
) on three code generation datasets: the multilingual benchmarks MultiPL-E
(
CassanoGNNPPYZAFGGJ23
)
and McEval
(
ChaiL0YJLS0RGWW25
)
, which offer
20
20
and
40
40
programming languages, respectively, and LiveCodeBench
(
JainHGLYZWSSS25
)
, which – since very recent – minimizes the risk of data leakage. Our results show that calibration benefits strongly from taking the aforementioned code factors into account, with accuracy on distinguishing correct from incorrect solutions improving from
+
13.2
%
+13.2\%
to
+
58.3
%
+58.3\%
.
•
To foster future research on this important issue, we make our Dataset
CALIBRI
available as a contribution
1
1
1
https://huggingface.co/datasets/lavis-nlp/CALIBRI
.
CALIBRI
includes correctness labels and token likelihoods for latest-generation LLMs on a fresh dataset with relatively low risk of data leakage.
2.
Related Work
Due to their large-scale pretraining and their enormous capacity, LLMs for code have demonstrated impressive problem-solving skills over a wide range of programming tasks
(
zhao_survey_2023
;
HouZLYWLLLGW24
)
.
However, their accuracy remains limited, as results in program repair demonstrate
(
JimenezYWYPPN24
;
campos25empiricalapr
)
. Moreover, LLMs have been shown to occasionally produce defective code
(
ChenLD24deep_dive
;
TambonDNKDA25
)
, e.g., by reproducing known bugs
(
JesseADM23
)
or generating potentially risky vulnerabilities
(
PearceATDK25
)
.
These limitations pose a significant threat to the reliability of code LLMs, hence quality control of code generation is a vital issue.
UE and Calibration for Large Language Models
Uncertainty estimation and model calibration are long-standing topics in probabilistic modeling and classification
(
glenn1950verification
;
steyerberg2010assessing
)
. Recent work has extended these concepts to LLMs, although research has focused on natural language tasks rather than generative settings
(
geng-etal-2024-survey
)
. Approaches for quantifying uncertainty in generative LLMs can be broadly categorized into black-box and white-box approaches
(
Shorinwa25UQsurvey
)
: Black-box methods operate on input–output pairs only, e.g.,
verbalized uncertainty
, where the model is prompted to express confidence in its output
(
TianMZSRYFM23
;
Kadavath22
;
lin22teachingtoexpress
)
, and
consistency-based methods
, that estimate uncertainty from agreement across multiple generations
(
QiuM24
;
LinT024
;
manakul23selfcheckgpt
)
. White-box methods exploit internal model signals:
information-theoretic approaches
derive confidence scores from output probabilities
(
FomichevaSYBGFA20
;
DuanC0ZWXKX24
)
, while
introspective methods
analyze LLMs internal activations, specifically, self-attention scores
and hidden states to estimate uncertainty
(
snyder24earlydetection
;
bui2025correctness
)
.
Post-hoc Calibration
Post-hoc scaling techniques such as Platt or temperature scaling
(
platt1999probabilistic
)
or Histogram Binning
(
zadrozny01histogrambinning
)
are commonly used to improve predictive calibration. Originally motivated by fairness and acountability, Hébert-Johnson et al. introduced
multiaccuracy
and
multicalibration
(
HebertJohnsonK18
)
, extending standard calibration to multiple, possibly intersecting groups. Recent work has started adapting multicalibration to LLMs: Detommaso et al. apply multicalibration algorithms to enhance the reliability of confidence scores in LLM outputs for question-answering tasks
(
DetommasoLF024
)
, and Hansen et al. evaluate multicalibration methods across a broad range of classification models on tabular, image and language datasets, finding benefits in many settings, especially for large vision and language models
(
HansenDNS24
)
.
Uncertainty Estimation and Calibration for Code Generation
All the above works have been conducted on natural language tasks. In contrast, research on
uncertainty estimation in code generation
is scarcer and has concentrated on two areas. First, several works fine-tune specialized LLMs for correctness estimation
(
zhou23codebertscore
;
hossain2024
;
reddy2025swerank
)
;
these methods risk overfitting to their limited supervised bug training sets, such as defects4j
(
JustJE14defects4j
)
or Swe-Bench-Lite
(
Jimenez24SWEBench
)
.
Second, reflective or judge-LLM approaches run additional reasoning steps to assess (or improve) their outputs
(
tong24codejudge
;
wang2025mctsjudge
)
. When it comes to
post-hoc confidence estimation / calibration
of off-the-shelf code LLMs, Zhou et al.
(
ZhouS024
)
show for four classification-based code understanding tasks, that vanilla code LLMs are not well-calibrated per se. Spiess et al.
(
Spiess0PPRAJDA25
)
show similar results for generative code LLMs and compare Platt-scaling as a standard calibration approach with self-reflection. Beyond these, multicalibration remains unstudied for code LLMs, and a rigorous comparisons of all of the strategies mentioned in Section
2
is lacking.
A recent survey confirmed that the field of LLM-based code correctness estimation remains in its early stages
(
he2025courtroomsurvey
)
.
3.
Background
In this section, we introduce the concepts of calibration and multicalibration for code generation, and describe common metrics for assessing calibration quality.
We assume the input prompt
X
X
to consist of a task description and/or code context, and the output
Z
=
z
1
:
n
Z=z_{1:n}
to be a sequence of code tokens.
Z
Z
’s correctness can be assessed
(e.g. through unit tests), resulting in a correctness label
Y
∈
{
0
,
1
}
Y{\in}\{0,1\}
with
Y
=
1
Y{=}1
iff the predicted code
Z
Z
is correct.
Also, we define a
confidence score
p
^
\hat{p}
representing the model’s estimated confidence in the predicted code to be correct.
p
^
\hat{p}
is derived from the model’s token likelihoods
P
​
(
z
i
|
z
<
i
,
X
)
P(z_{i}|z_{<i},X)
for the individual code tokens on the sequence using different aggregation strategies as described in Section
4.2
.
3.1.
Calibrated Confidences
Calibration aims at measuring how accurately a model’s predicted confidence in a certain outcome depicts the actual frequency of that outcome. For example, we assume a weather prediction model to be well calibrated if, on 90 out of 100 days on which the model predicted
90
%
90\%
confidence of rain the next day, it actually rained.
Formally, a model is considered perfectly
calibrated
(
GuoPSW17
;
JiangADN21
)
if its confidence
p
^
\hat{p}
matches the true probability of correctness:
(1)
P
​
(
Y
=
1
∣
p
^
=
p
)
=
p
∀
p
∈
[
0
,
1
]
P(Y{=}1\mid\hat{p}{=}p)=p\quad\forall p\in[0,1]
In other words, perfect calibration means that the model’s predicted confidence
p
^
\hat{p}
matches the empirical accuracy, i.e. the fraction of correct predictions among all outputs with confidence
p
^
\hat{p}
.
As discussed by Guo et al,
(
GuoPSW17
)
, the probability in Equation
1
cannot be computed exactly with a finite number of samples, since
p
^
\hat{p}
is a continuous random variable. Therefore, calibration in practice is conducted by partitioning confidences into
M
M
disjoint bins of equal width:
[
1
M
]
=
{
i
M
}
i
=
1
M
\left[\frac{1}{M}\right]=\left\{\frac{i}{M}\right\}^{M}_{i=1}
Then, given a set of samples
(
x
1
,
y
1
,
z
1
,
p
^
1
)
,
…
,
(
x
n
,
y
n
,
z
n
,
p
^
n
)
(x_{1},y_{1},z_{1},\hat{p}_{1}),...,(x_{n},y_{n},z_{n},\hat{p}_{n})
, each with correctness label
y
i
y_{i}
and confidence
p
^
i
\hat{p}_{i}
, we assign the confidences
p
^
1
,
…
,
p
^
n
\hat{p}_{1},...,\hat{p}_{n}
to their respective bins, obtaining bin-wise sets of confidences (
S
m
S_{m}
) and indices (
B
m
B_{m}
) for
m
=
1
,
…
​
M
m{=}1,...M
:
(2)
S
m
\displaystyle S_{m}
:=
{
{
p
^
i
|
m
−
1
M
≤
p
^
i
<
m
M
,
i
∈
{
1
,
…
,
n
}
}
if
​
m
<
M
{
p
^
i
|
M
−
1
M
≤
p
^
i
≤
1
,
i
∈
{
1
,
…
,
n
}
}
if
​
m
=
M
\displaystyle:=\begin{cases}\left\{\hat{p}_{i}\;\Big|\;\frac{m-1}{M}\leq\hat{p}_{i}<\frac{m}{M},\;i\in\{1,\ldots,n\}\right\}&\text{if }m<M\\[5.0pt]
\left\{\hat{p}_{i}\;\Big|\;\frac{M-1}{M}\leq\hat{p}_{i}\leq 1,\;i\in\{1,\ldots,n\}\right\}&\text{if }m=M\end{cases}
(3)
B
m
\displaystyle B_{m}
:=
{
i
∈
{
1
,
…
,
n
}
|
p
^
i
∈
S
m
}
\displaystyle:=\left\{i\in\{1,\ldots,n\}\;\Big|\;\hat{p}_{i}\in S_{m}\right\}
A model is then considered calibrated if,
within each bin
, the mean predicted confidence equals the empirical fraction of correct predictions.
For each bin
B
m
B_{m}
, we aggregate the model’s accuracy and confidence as:
(4)
acc
​
(
B
m
)
\displaystyle\text{acc}(B_{m})
=
1
|
B
m
|
​
∑
i
∈
B
m
𝟏
​
(
y
i
=
1
)
\displaystyle=\frac{1}{|B_{m}|}\sum_{i\in B_{m}}\mathbf{1}(y_{i}=1)
(5)
conf
​
(
B
m
)
\displaystyle\text{conf}(B_{m})
=
1
|
B
m
|
​
∑
i
∈
B
m
p
^
i
\displaystyle=\frac{1}{|B_{m}|}\sum_{i\in B_{m}}\hat{p}_{i}
A perfectly calibrated model will have
acc
​
(
B
m
)
=
conf
​
(
B
m
)
\text{acc}(B_{m})=\text{conf}(B_{m})
for all
m
=
1
,
…
,
M
m=1,...,M
. This relationship can be visualized in a
reliability diagram
, which plots the empirical accuracy
acc
​
(
B
m
)
\text{acc}(B_{m})
against the mean confidence
conf
​
(
B
m
)
\text{conf}(B_{m})
for each bin, as shown in Figure
1
.
3.1.1.
Calibration Measures
While reliability diagrams provide an intuitive visualization, a scalar summary measure of (mis)calibration is often preferred. Therefore, several measures are commonly used to quantify the calibration error of a model:
The
Expected Calibration Error (ECE)
(
NaeiniCH15
)
approximates the expected difference between accuracy and confidence as a weighted average of the bins’ deviations between accuracy and confidence:
(6)
ECE
:=
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
⋅
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
\text{ECE}:=\sum_{m=1}^{M}\frac{|B_{m}|}{n}\cdot\left|\text{acc}(B_{m})-\text{conf}(B_{m})\right|
where
n
n
is the total number of samples.
Brier Score
(
glenn1950verification
)
ECE
is intuitive but can be misleading: a naive predictor, whose confidence is always the mean accuracy across all samples
p
r
:=
1
/
n
⋅
∑
i
=
1
n
y
i
p_{r}:=1/n\cdot\sum_{i=1}^{n}y_{i}
(also called the
base rate
) could yield a deceptively low
ECE
, since all predictions fall into a single bin. An alternative measure avoiding this weakness is the Brier score
ℬ
\mathcal{B}
, which quantifies the mean squared difference between confidence and true correctness label:
(7)
ℬ
:=
1
n
​
∑
i
=
1
n
(
p
^
i
−
y
i
)
2
\mathcal{B}:=\frac{1}{n}\sum_{i=1}^{n}(\hat{p}_{i}-y_{i})^{2}
A
Brier score
of
0
implies perfect calibration, with confidences
p
^
i
=
1
\hat{p}_{i}{=}1
for correct outputs and
p
^
i
=
0
\hat{p}_{i}{=}0
for incorrect ones. Random binary confidences are expected to yield
ℬ
=
0.25
\mathcal{B}=0.25
for a balanced dataset (
50
%
50\%
correct and
50
%
50\%
incorrect), while
ℬ
=
1
\mathcal{B}=1
indicates complete confidence in the wrong outcome.
Brier Skill Score (BSS)
(
glenn1950verification
)
For a more interpretable comparison, particularly in unbalanced scenarios, we also report the
Brier Skill Score
: Consider a naive, so-called
unskilled predictor
, which simply assigns every sample the base-rate confidence
p
r
p_{r}
. This baseline’s Brier Score can be derived in closed form as:
(8)
ℬ
r
​
e
​
f
=
p
r
⋅
(
1
−
p
r
)
,
\mathcal{B}_{ref}=p_{r}\cdot(1-p_{r}),
and the Brier Skill score measures the improvement over this baseline:
(9)
BSS
:=
ℬ
r
​
e
​
f
−
ℬ
ℬ
r
​
e
​
f
\text{BSS}:=\frac{\mathcal{B}_{ref}-\mathcal{B}}{\mathcal{B}_{ref}}
where positive
BSS
values show improvement over the unskilled baseline, and negative values show a deterioration.
When
p
r
∈
{
0
,
1
}
p_{r}\in\{0,1\}
, the denominator is zero; by convention, we set
BSS
=
1
\text{BSS}=1
if
ℬ
=
0
\mathcal{B}=0
(perfect prediction) and
BSS
=
−
∞
\text{BSS}=-\infty
otherwise.
3.2.
Multicalibrated Confidences
Following Detommaso et al.
(
DetommasoLF024
)
, we argue that the guarantee provided by standard calibration (Equation
1
) is insufficient for generative language model applications, since LLM performance varies widely across different types of tasks. Consider, for example, two prompt-completion pairs, respectively asking a Code LLM to implement either a bubble sort function or a fully homomorphic encryption scheme. The probability of correctness should differ substantially between these cases, yet calibration is a
marginal
guarantee that may average over both cases. As a result, a calibrated model might produce confidence scores that are systematically overconfident on complex tasks and underconfident on simple tasks, which is not in conflict with even perfect calibration. Ideally, confidence estimates should be calibrated conditionally on as much fine-grained information as possible about the prompt.
Multicalibration
, introduced by Hébert-Johnson et al.
(
HebertJohnsonK18
)
, provides exactly this type of conditional guarantee, ensuring that predicted probabilities align with empirical accuracy across multiple relevant subgroups of inputs.
3.2.1.
Groups
Multicalibration introduces the notion of
groups
, i.e. sets of prompt-completion pairs sharing a common property, such as a level of code complexity or a programming language. Let
𝒟
\mathcal{D}
be the distribution of prompt-completion pairs
(
X
,
Z
)
∼
𝒟
(X,Z)\sim\mathcal{D}
. A
group function
g
:
𝒟
→
{
0
,
1
}
g:\mathcal{D}\to\{0,1\}
indicates group membership, i.e.
g
​
(
x
,
z
)
=
1
g(x,z)=1
iff a pair
(
x
,
z
)
(x,z)
belongs to Group
g
g
. Analogous to the confidence bins
B
m
B_{m}
, we define for each group function
g
g
the corresponding index set as
(10)
G
:=
{
i
∈
{
1
,
…
,
n
}
∣
g
​
(
x
i
,
z
i
)
=
1
}
G:=\left\{i\in\{1,...,n\}\mid g(x_{i},z_{i})=1\right\}
A set of groups
𝒢
\mathcal{G}
is therefore identified by a set of indicator functions. Note that prompt-completion pairs can have multiple non-mutually-exclusive attributes, so that groups in
𝒢
\mathcal{G}
may intersect.
Group-conditional unbiasedness (multiaccuracy)
Before defining multicalibration, we consider a weaker notion:
group-conditional unbiasedness
(also known as
multiaccuracy
)
(
HebertJohnsonK18
;
KimGZ19
)
.
A scoring function
p
^
\hat{p}
is
group-conditionally unbiased
with respect to a data distribution
𝒟
\mathcal{D}
and a set of groups
𝒢
\mathcal{G}
if
(11)
𝔼
𝒟
​
[
Y
−
p
^
∣
g
​
(
X
)
=
1
]
=
0
,
∀
g
∈
𝒢
.
\mathbb{E}_{\mathcal{D}}[Y-\hat{p}\mid g(X)=1]=0,\quad\forall g\in\mathcal{G}.
This condition ensures that the mean predicted confidence equals the true accuracy within each group, but it does not yet account for distributional calibration errors across confidence levels.
Group Average Squared Calibration Error (gASCE)
To quantify calibration error conditioned jointly on the groups
𝒢
\mathcal{G}
and a set of disjoint confidence bins
B
1
,
…
,
B
M
B_{1},...,B_{M}
, we use the
group average squared calibration error
(
DetommasoLF024
)
.
For a single group
g
g
, the gASCE is defined as
(12)
g
​
A
​
S
​
C
​
E
​
(
g
)
\displaystyle gASCE(g)
:=
∑
m
=
1
M
P
​
(
m
|
g
)
⋅
(
Δ
g
,
m
)
2
,
\displaystyle:=\sum_{m=1}^{M}P(m|g)\cdot(\Delta_{g,m})^{2},
where
Δ
g
,
m
\displaystyle\text{where}\quad\Delta_{g,m}
:=
1
|
G
∩
B
m
|
⋅
∑
j
∈
G
∩
B
m
(
y
j
−
p
^
j
)
\displaystyle:=\frac{1}{|G\cap B_{m}|}\cdot\sum_{j\in G\cap B_{m}}(y_{j}-\hat{p}_{j})
and
P
​
(
m
|
g
)
\displaystyle\text{and}\quad P(m|g)
=
|
G
∩
B
m
|
|
G
|
\displaystyle=\frac{|G\cap B_{m}|}{|G|}
3.2.2.
Multicalibration
Recall that classical calibration as defined in Section
3.1
requires a model to be unbiased conditional on a set of disjoint confidence bins. Multicalibration strengthens this guarantee by conditioning additionally on a set of groups
𝒢
\mathcal{G}
, requiring calibration to hold simultaneously within every group
g
∈
𝒢
g\in\mathcal{G}
.
Formally, following Hébert-Johnson et al.
(
HebertJohnsonK18
)
, a scoring function
p
^
\hat{p}
is
α
\alpha
-approximately multicalibrated
with respect to a data distribution
𝒟
\mathcal{D}
and a set of groups
𝒢
\mathcal{G}
iff
(13)
gASCE
​
(
g
)
<
α
ℙ
𝒟
​
(
g
​
(
X
)
=
1
)
,
∀
g
∈
𝒢
,
\text{gASCE}(g)<\frac{\alpha}{\mathbb{P}_{\mathcal{D}}(g(X)=1)},\quad\forall g\in\mathcal{G},
where
α
>
0
\alpha>0
is the admitted error.
4.
Research Methodology / Approach
Our objective is to calibrate the confidence scores of generative models for code rather than improve their raw accuracy. We focus on function synthesis
(
Chen21HumanEval
;
Austin21MBPP
;
JainHGLYZWSSS25
)
as a widely studied, representative task for code generation and aim to develop models that reliably produces confidence scores for the probability that a prompt-completion pair is correct.
Our methodology involves two steps. First, we evaluate how well different initial uncertainty estimation methods align with the actual correctness of generated outputs. Next, we evaluate and compare several approaches for post hoc calibration of these uncertainty measures. Particularly, we compare
multicalibration
with group-agnostic baselines.
4.1.
Research Agenda
To systematically assess calibration techniques for code generation across different influencing factors, we define the following research questions:
•
RQ1: How effective is multicalibration for post-hoc calibration?
And how does it compare to both uncalibrated confidence scores and group-agnostic baselines?
•
RQ2: How do different initial confidence measures compare?
What impact does the initial scoring method have on the final calibration performance?
•
RQ3: Which types of group information contribute most to improved calibration?
4.2.
Initial Confidence Measures
A key challenge in our setup is selecting an appropriate scoring method to derive initial confidences
p
^
\hat{p}
as a starting point for calibration. A range of uncertainty quantification techniques for LLMs have been proposed, broadly categorized into black-box and white-box approaches (see
(
Shorinwa25UQsurvey
)
for a comprehensive survey).
However, a recent comparison of confidence measures for generative LLMs
(
VashurinFVRVTPXSGPBNPS25
)
found no clear winner, better-performing methods were often computationally costly with limited gains. Among simpler approaches, confidence-based measures consistently outperformed reflective ones. We therefore adopt this strategy and define our initial confidence score as the average token likelihood, or
inverse perplexity
, of the generation
(
jelinek1977perplexity
)
:
(14)
p
^
=
exp
​
(
1
n
​
∑
i
=
1
n
log
​
P
​
(
z
i
∣
z
<
i
,
X
)
)
\hat{p}=\text{exp}\left(\frac{1}{n}\sum_{i=1}^{n}\;\text{log}\;P(z_{i}\mid z_{<i},X)\right)
where
X
X
is the prompt and
Z
=
[
z
1
,
…
,
z
n
]
Z=[z_{1},\dots,z_{n}]
the generated output.
Note that this output contains not only the generated code, but also additional reasoning traces, since we use current reasoning models for our experiments.
Therefore, we compare aggregations of token-level confidences over different scopes:
(1)
avg_prob
, the mean likelihood over the entire output sequence, as defined in Equation
14
; (2)
code_prob
, which is averaged only over the tokens of the generated code; and (3)
tail_prob
, which focuses on the last
k
k
tokens, as reasoning quality is known to decline towards the end of generations, so they indicate correctnesss
(
Fu25DeepThink
)
.
4.3.
Calibration Approaches
Previous work has demonstrated that LLM-generated confidences contain a signal for output correctness, but they are not well calibrated
(
GuoPSW17
;
JiangADN21
;
ZhouS024
;
Spiess0PPRAJDA25
)
. To address this, we examine various post-hoc calibration strategies that adjust probability estimates to better align with observations. We distinguish between simple rescaling methods, which aim to improve overall calibration (see Section
3.1
) and more informed, group-based methods, which are designed to provide stronger guarantees through multicalibration (Section
3.2
).
4.3.1.
Simple Rescaling Approaches
We evaluate
Platt scaling
and
Histogram Binning
as two common calibration methods.
Platt Scaling
(
platt1999probabilistic
)
Platt scaling is a common approach that applies logistic regression to the prediction logits,
l
​
o
​
g
​
p
^
log\;\hat{p}
.
More specifically, in the context of neural networks
(
NiculescuMizilC05
)
, Platt scaling learns scalar parameters
a
,
b
∈
ℝ
a,b\in\mathbb{R}
from a training set of confidence-correctness pairs
(
p
^
i
,
y
i
)
(\hat{p}_{i},y_{i})
. It outputs calibrated probabilities by applying the sigmoid function
σ
\sigma
to the scaled log-probabilities, obtaining supposedly calibrated confidences
(15)
p
^
P
​
L
​
A
​
T
​
T
:=
σ
​
(
a
⋅
log
​
p
^
+
b
)
.
\hat{p}^{PLATT}:=\sigma(a\cdot\text{log}\;\hat{p}+b).
Since Spiess et al.
(
Spiess0PPRAJDA25
)
found Platt scaling to improve calibration for code LLMs with some caveats, we include it as a baseline.
Histogram Binning
(
ZadroznyE01
)
Histogramm Binning is a simple non-parametric calibration method. Following Section
3.1
, it first partitions
[
0
,
1
]
[0,1]
into uniform bins
B
1
,
…
,
B
M
B_{1},\dots,B_{M}
and
rounds the raw confidences
p
^
\hat{p}
to the closest grid value
p
^
′
\hat{p}^{\prime}
:
(16)
p
^
′
:=
arg min
b
∈
[
1
m
]
​
|
p
^
−
b
|
.
\hat{p}^{\prime}:=\underset{b\in[\frac{1}{m}]}{\text{arg min}}\;|\hat{p}-b|.
Then, it computes the calibration error
Δ
m
\Delta_{m}
per bin as
(17)
Δ
m
:=
1
|
B
m
|
⋅
∑
i
∈
B
m
y
i
−
p
^
i
′
\Delta_{m}:=\frac{1}{|B_{m}|}\cdot\sum_{i\in B_{m}}y_{i}-\hat{p}^{\prime}_{i}
and applies it as a constant shift to all samples in the respective bin:
(18)
p
^
H
​
B
:=
p
^
i
′
+
Δ
m
∀
m
∈
(
1
,
…
​
M
)
∀
i
∈
B
m
\hat{p}^{HB}:=\hat{p}_{i}^{\prime}+\Delta_{m}\quad\forall m\in(1,\dots M)\quad\forall i\in B_{m}\\
4.3.2.
Multicalibration-based Approaches
As described in Section
3.2
, multicalibration aims at
taking particular characteristics of the prompt / generation pairs into account, by assigning them to semantic
groups
. We first specify the group functions
g
g
we use to capture properties of coding problems. We then describe the group-aware multicalibration approaches we test (namely, Group-Conditional Unbiased Regression (GCUR), Iterative Grouped Histogram Binning (IGHB) and Iterative Grouped Linear Binning (IGLB)).
Group Functions
Multicalibration is defined with respect to a set of
group functions
.
If these groups capture features correlated with
the likelihood of correctness, their inclusion is likely to improve calibration. At the same time, to ensure practical applicability, we restrict ourselves to features that can be computed efficiently.
Specifically, we define the following group functions: (1)
complex-ity-based groups
aim to capture differences in code complexity by grouping examples based on circular complexity or, where available, on benchmark-provided difficulty labels. (2)
length-based groups
divide examples according to the output length, measured either in total characters or lines of code of the extracted code snippet. (3)
language-based groups
group examples by the programming language of the generated code. Based on these groups, we evaluate the following methods:
Group-Conditional Unbiased Regression (GCUR)
(
GopalanHKRW23
)
GCUR provides a
group conditionally unbiased
model as defined in Equation
11
. It uses Algorithm
1
to produce a score
p
^
G
​
C
​
U
​
R
\hat{p}^{GCUR}
by solving a linear regression problem over features defined by the raw score
p
^
\hat{p}
and the group indicator functions in
𝒢
\mathcal{G}
.
Algorithm 1
Group-Conditional Unbiased Regression
1:
Set
p
^
G
​
C
​
U
​
R
:=
p
^
+
∑
g
∈
𝒢
λ
g
⋅
g
​
(
x
)
,
\hat{p}^{GCUR}:=\hat{p}+\sum_{g\in\mathcal{G}}\lambda_{g}\cdot g(x),
s.t.
{
λ
g
}
g
∈
𝒢
=
arg min
​
ℬ
​
(
p
^
G
​
C
​
U
​
R
)
\{\lambda_{g}\}_{g\in\mathcal{G}}=\text{arg min }\mathcal{B}(\hat{p}^{GCUR})
Gopalan et al.
(
GopalanHKRW23
)
later showed that the condition also holds if MSE (or Brier Score
ℬ
\mathcal{B}
) is replaced with a cross-entropy loss, i.e. when solving a logistic regression instead of a linear regression. We evaluate both variants, denoted as
p
^
L
​
I
​
N
​
R
\hat{p}^{LINR}
and
p
^
L
​
O
​
G
​
R
\hat{p}^{LOGR}
respectively.
Iterative Grouped Histogram Binning (IGHB)
(
HebertJohnsonK18
;
DetommasoLF024
)
IGHB (Algorithm
2
) extends Histogram Binning by the concept of groups. The method first evaluates whether
α
\alpha
-approximate multicalibration (as defined in Equation
13
) is satisfied. If this is not the case, IGHB identifies the group/bin combination that contributes most to the gASCE (Step 3) and patches the confidences of the training samples within this bin/group combination (Step 4). IGHB then iterates until convergence. The rounding operation
h
′
h^{\prime}
in Step 5 (as defined in Equation
16
) ensures that the number of bins does not increase, guaranteeing sufficient data in each step.
Note that as the confidences
p
^
i
\hat{p}_{i}
are corrected over the iterations of the algorithm, the memberships to bins
B
m
B_{m}
(and thus
P
​
(
g
,
m
)
,
Δ
g
,
m
P(g,m),\Delta_{g,m}
, and
g
​
A
​
S
​
C
​
E
​
(
g
)
gASCE(g)
) change. This is why we include an additional parameter
t
t
.
Algorithm 2
Iterative Grouped Histogram Binning (IGHB)
1:
Let
α
=
1
M
,
t
=
0
,
p
^
i
t
=
0
:=
p
^
i
′
\alpha=\frac{1}{M},t=0,\;\hat{p}_{i}^{t=0}:=\hat{p}_{i}^{\prime}
for all
i
=
1
,
…
,
n
i=1,...,n
2:
while
max
g
∈
𝒢
​
P
​
(
g
)
⋅
g
​
A
​
S
​
C
​
E
t
​
(
g
)
>
α
\text{max}_{g\in\mathcal{G}}\;P(g)\cdot gASCE^{t}(g)>\alpha
do
3:
Set
(
g
∗
,
m
∗
)
:=
arg max
g
∈
𝒢
,
m
∈
{
1
,
…
,
M
}
​
P
t
​
(
g
,
m
)
⋅
(
Δ
g
,
m
t
)
2
(g^{*},m^{*}):=\underset{g\in\mathcal{G},m\in\{1,...,M\}}{\text{arg max}}\;P^{t}(g,m)\cdot(\Delta_{g,m}^{t})^{2}
4:
Set
h
t
+
1
:=
{
p
^
i
t
+
Δ
g
∗
,
m
∗
t
if
​
i
∈
B
m
∗
t
∩
G
∗
,
p
^
i
t
otherwise.
h_{t+1}:=\left\{\begin{array}[]{l}\hat{p}_{i}^{t}+\Delta_{g^{*},m^{*}}^{t}\quad\text{if }i\in B_{m^{*}}^{t}{\cap}G^{*},\\
\hat{p}_{i}^{t}\hskip 52.00005pt\text{otherwise.}\end{array}\right.
5:
Set
p
^
t
+
1
:=
(
h
t
+
1
)
′
\hat{p}^{t+1}:=(h^{t+1})^{\prime}
6:
end
while
Iterative Grouped Linear Binning (IGLB)
(
DetommasoLF024
)
IGHB, as introduced above, can build complex models by performing iterative updates on intersecting groups, which renders the method prone to overfitting
(
GlobusHarrisHK23
)
. One reason is that IGHB operates on group-bin combinations that may contain only a small number of data points, leading to inaccurate estimates of the distribution. To mitigate this issue, Detommaso et al.
(
DetommasoLF024
)
propose
Iterative Grouped Linear Binning
, demonstrating that – instead of splitting the data into disjoint bins as defined in Equation
2
– it is beneficial to use larger, overlapping bins
B
m
≤
=
{
i
∣
p
^
i
≤
m
M
}
B_{m}^{\leq}=\{i\mid\hat{p}_{i}\leq\frac{m}{M}\}
(and
B
m
≥
B_{m}^{\geq}
analogously) to obtain more stable estimates. Since these bins now contain a range of values rather than sets of identical values, IGLB extends the update step (Step 4 in Algorithm
2
) to
linear patches
of the form
h
t
+
1
=
α
+
β
⋅
p
^
t
h_{t+1}=\alpha+\beta\cdot\hat{p}^{t}
where
α
\alpha
and
β
\beta
are chosen so as to minimize the squared error of the model. Specifically, linear scaling (LS) is applied as:
(19)
LS
​
(
p
^
)
:
\displaystyle\text{LS}(\hat{p}):
=
σ
​
(
α
∗
+
β
∗
​
logit
​
(
p
^
)
)
,
\displaystyle=\sigma(\alpha^{*}+\beta^{*}\,\text{logit}(\hat{p})),
with
(
α
∗
,
β
∗
)
\displaystyle\text{with}\quad(\alpha^{*},\beta^{*})
=
arg min
α
,
β
​
ℬ
​
(
p
^
)
\displaystyle=\underset{\alpha,\beta}{\text{arg min}}\;\mathcal{B}(\hat{p})
Algorithm
3
integrates these strategies into IGHB by iteratively selecting the group-bin combination with the highest error (Step 3) and applying the LS patch according to Equation
19
(Step 5). To prevent overfitting, the method includes two early-stopping rules: it halts if the Brier Score
ℬ
v
​
a
​
l
\mathcal{B}_{val}
on a held out validation set no longer improves (Step 6) or if the probability mass of the conditioning event selected for an update is less than a predefined threshold.
Algorithm 3
Iterative Grouped Linear Binning (IGLB)
1:
Let
t
=
0
,
ϵ
>
0
t=0,\epsilon>0
,
p
^
i
t
=
0
:=
p
^
i
′
\hat{p}_{i}^{t=0}:=\hat{p}_{i}^{\prime}
for all
i
=
1
,
…
,
n
i=1,...,n
2:
while
True
do
3:
Set
(
g
∗
,
m
∗
,
τ
∗
)
:=
arg max
g
∈
𝒢
,
m
∈
{
1
,
…
,
M
}
,
τ
∈
{
≤
,
≥
}
​
P
t
​
(
g
,
m
,
τ
)
⋅
(
Δ
g
,
m
,
τ
t
)
2
(g^{*},m^{*},\tau^{*}):=\underset{\begin{subarray}{c}g\in\mathcal{G},\\
m\in\{1,\dots,M\},\\
\tau\in\{\leq,\geq\}\end{subarray}}{\text{arg max}}P^{t}(g,m,\tau)\cdot(\Delta_{g,m,\tau}^{t})^{2}
4:
break
if
P
t
​
(
g
∗
,
m
∗
,
τ
∗
)
<
ϵ
P^{t}(g^{*},m^{*},\tau^{*})<\epsilon
5:
Set
h
t
+
1
:=
{
LS
​
(
p
^
i
t
)
if
​
i
∈
B
m
∗
τ
∗
∩
G
∗
,
p
^
i
t
otherwise.
h_{t+1}:=\left\{\begin{array}[]{l}\text{LS}(\hat{p}_{i}^{t})\quad\text{if }i\in B_{m^{*}}^{\tau^{*}}{\cap}G^{*},\\
\hat{p}_{i}^{t}\hskip 30.00005pt\text{otherwise.}\end{array}\right.
6:
break
if
ℬ
𝒟
v
​
a
​
l
​
(
h
t
+
1
,
Y
)
≥
ℬ
𝒟
v
​
a
​
l
​
(
p
^
t
,
Y
)
\mathcal{B}_{\mathcal{D}_{val}}(h_{t+1},Y)\geq\mathcal{B}_{\mathcal{D}_{val}}(\hat{p}^{t},Y)
7:
Set
p
^
t
+
1
:=
h
t
+
1
′
\hat{p}_{t+1}:=h^{\prime}_{t+1}
8:
end
while
Table 1.
Comparison of Brier Skill Score (BSS) and binary clasification accuracy (ACC) across uncalibrated scores, two group-agnostic baselines, and four group-based calibration methods. Results for DeepSeek R1 distill on LiveCodeBench are excluded due to unreliable code extraction.
LiveCodeBench
MultiPL-E
McEval
BSS
method
groups
Qwen3
gpt-oss
R1(dist)
Qwen3
gpt-oss
R1(dist)
Qwen3
gpt-oss
R1(dist)
uncalibrated
-
-0.543
-0.075
-
-0.350
-2.073
-1.634
-0.243
-0.228
-0.670
Platt
-
0.377
0.187
-
0.064
0.069
0.125
0.160
0.097
0.093
HB
-
0.383
0.237
-
0.066
0.069
0.119
0.160
0.094
0.112
LINR
✓
0.463
0.721
-
0.304
0.115
0.242
0.297
0.251
0.447
LOGR
✓
0.306
0.733
-
-0.039
-0.024
-0.010
0.038
-0.092
0.312
IGHB
✓
0.232
0.412
-
-0.237
-1.856
-0.747
-0.122
-0.038
-0.039
IGLB
✓
0.480
0.764
-
0.221
0.103
0.151
0.317
0.258
0.479
ACC
Qwen3
gpt-oss
R1(dist)
Qwen3
gpt-oss
R1(dist)
Qwen3
gpt-oss
R1(dist)
uncalibrated
-
0.458
0.511
-
0.568
0.831
0.414
0.613
0.474
0.288
Platt
-
0.798
0.707
-
0.616
0.954
0.861
0.699
0.617
0.734
HB
-
0.797
0.717
-
0.612
0.954
0.861
0.704
0.623
0.755
LINR
✓
0.822
0.924
-
0.745
0.954
0.874
0.763
0.725
0.872
LOGR
✓
0.828
0.933
-
0.744
0.955
0.880
0.771
0.728
0.866
IGHB
✓
0.731
0.814
-
0.571
0.831
0.702
0.613
0.589
0.613
IGLB
✓
0.830
0.930
-
0.715
0.952
0.870
0.768
0.724
0.846
5.
Experimental Setup
This section outlines the task setup, datasets and models used in our study.
We conduct calibration experiments on
function synthesis
, which aims to generate executable methods from natural language problem descriptions (see Subsection
5.1
for details on the benchmarks). We prompt three recent open-weight reasoning models (see Subsection
5.2
) to produce ten generations per sample, recording the associated token probabilities. This yields
171
,
420
171{,}420
prompt–generation–probability tuples. Generated code is evaluated via benchmark unit tests and labeled as correct if all tests pass.
Using this dataset, we compare three initial confidence measures as described in Section
4.2
and six calibration methods: two classical, two group-accuracy-based, and two multicalibration methods (Section
4.3
). All experiments use a grid of
M
=
20
M=20
bins, which preliminary tests found to balance granularity and bin weights effectively.
5.1.
Benchmarks
To capture varying levels of difficulty and language coverage, we employ three complementary benchmarks: MultiPL-E
(
CassanoGNNPPYZAFGGJ23
)
, McEval
(
ChaiL0YJLS0RGWW25
)
and LiveCodeBench
(
JainHGLYZWSSS25
)
.
MultiPL-E
(
CassanoGNNPPYZAFGGJ23
)
is a multilingual code generation benchmark created by translating two popular Python benchmarks (HumanEval
(
Chen21HumanEval
)
and MBPP
(
Austin21MBPP
)
) into 18 programming languages. For our study, we use its 2,952 samples based on HumanEval.
McEval
(
ChaiL0YJLS0RGWW25
)
is a multilingual code benchmark comprising 16K test samples across 40 languages, covering varying difficulty levels and coding scenarios. We use its multilingual code-generation subset of 1,707 samples, which was constructed from curated code snippets augmented with LLM-generated instructions and test cases.
LiveCodeBench
(
JainHGLYZWSSS25
)
is a collection of recently published Python coding problems from three competition platform, designed to provide
contamination free evaluation
of LLMs for code, i.e. addressing the issue of data leakage, where parts of the evaluation data may be included in a model’s training corpus. We use its most recent release (release_v6) containing 1055 problems from May 2023 to April 2025.
The three benchmarks complement each other in scope and difficulty. MultiPL-E and McEval provide multilingual problems – MultiPL-E focusing on relatively simple tasks, and McEval covering a broader range of difficulty levels. LiveCodeBench, in contrast, features more challenging and diverse Python problems, and enables contamination-free evaluation, thereby mitigating potential calibration biases caused by training data overlap.
All datasets include executable test suites for functional verification, which we adopt as the most reliable measure of code correctness.
For all experiments, we require a training set for calibration, a hold-out test set, and an additional validation set for IGLB calibration. To prevent leakage across splits, we partition the data at the
problem level
, ensuring that all generations and translations of a given problem reside within the same split.
5.2.
Models
We evaluate three recent open-weight reasoning LLMs in our experiments:
Qwen3-Coder-30B-A3B-Instruct
(
yang25qwen3
)
,
OpenAI GPT-OSS-20B
(
openai2025gptoss120bgptoss20bmodel
)
and
DeepSeek-R1-Distill-Qwen-32B
(
guo25deepseek
)
. Qwen3-Coder is a family of Mixture-of-Experts (MoE) models for coding and agentic tasks, we use the 30B-A3B-Instruct variant. The GPT-OSS models from OpenAI are MoE models for general reasoning and agentic tasks, and we employ the 20b variant in our evaluation. DeepSeek-R1-Distill-Qwen-32B is a Qwen-32B model distilled from DeepSeek-R1, a large reasoning model.
All three models demonstrate strong coding performance, and are open-weight, which is essential for our use-case as we need access to token-level generation probabilities.
Figure 1.
Top
: Reliability diagrams for Qwen3 Coder on LiveCodeBench. Well calibrated models fit the identity line, while deviations from the diagonal indicate miscalibration. Bin size is encoded by color intensity.
Bottom
: Mean predicted scores versus accuracies across clustered groups. LINR and IGLB achieve the best calibration, consistent with Table
1
.
6.
Results
We first provide an overall quantitative impression of all calibration methods, datasets and models (Section
6.1
), then discuss the influence of the different initial scoring methods (Section
6.2
), followed by a more detailed look on groups, with an ablation study and group-specific calibration results (Section
6.3
).
6.1.
RQ1: How effective is multicalibration for post-hoc calibration?
We compare the uncalibrated initial scoring function (using
avg_score
) against its calibrated variants obtained using the above post-processing algorithms: Platt scaling (Equation
15
), Histogram Binning (HB, Equation
18
), the linear and logistic regression variants of Group-Conditional Unbiased Regression (Algorithm
1
, LINR and LOGR), Iterative Grouped Histogram Binning (Algorithm
2
, IGHB) and Iterative Grouped Linear Binning (Algorithm
3
, IGLB). While Platt scaling and HB perform standard calibration without requiring a grouping strategy. LINR and LOGR ensure group-conditional unbiasedness (Equation
11
), and IGHB and IGLB produce multicalibrated models as defined in Equation
13
.
Table
1
reports the Brier Skill Score (BSS) and binary classification accuracy (ACC) – thresholding at
p
^
≥
50
%
\hat{p}{\geq}50\%
– across all methods, benchmarks and LLMs.
Note that results for DeepSeek R1 distill on LiveCodeBench are omitted, due to formatting inconsistencies that prevented reliable code extraction.
Across all datasets and models, IGLB and the two Group-Conditio-nal Unbiased Regression variants (LINR and LOGR) consistently achieve the best performance. All calibration methods improve upon the uncalibrated baseline, in many cases substantially. While uncalibrated scores were often near-random (
ACC
≈
0.5
\text{ACC}\approx 0.5
) for distinguishing correct from incorrect code, all post-hoc methods yielded substantial gains. After calibration, accuracy rose to between
72.5
%
72.5\%
and
95.5
%
95.5\%
across all models and datasets – an improvement of up to
58.4
%
58.4\%
in the most notable case (DeepSeek R1 distill on McEval). This highlights the potential of calibrated uncertainty measures to effectively predict the correctness of LLM-generated code even without unit tests.
Standard calibration methods such as Platt-Scaling and HB perform well compared to the initial scoring function, yet consistently underperform the multicalibrated IGLB method and the multiaccurate LINR/LOGR. Figure
1
visualizes sample results as reliability diagrams, plotting confidence scores against empirical accuracy (top).
The bottom panels plot the averaged confidence scores against the fraction of positive labels across various groups (each color representing one group).
All calibration methods improve upon the overconfident, uncalibrated scores (left) with IGLB and LINR demonstrating the strongest calibration performance.
6.2.
RQ2: How do different initial confidence measures compare?
Table 2.
Comparison of initial scoring methods for Qwen3 Coder on LiveCodeBench, reporting the Expected Calibration Error (ECE, lower is better) and Brier Skill Score (
B
​
S
​
S
BSS
, higher is better).
For fair comparison, examples where no code could be extracted from the generated output are excluded.
avg_prob
code_prob
tail_prob
Qwen3 C.
ECE
B
​
S
​
S
BSS
ECE
B
​
S
​
S
BSS
ECE
B
​
S
​
S
BSS
uncalib.
0.294
-0.257
0.342
-0.453
0.346
-0.474
HB
0.050
0.278
0.014
0.119
0.025
0.046
LINR
0.079
0.425
0.082
0.402
0.080
0.394
LOGR
0.177
0.237
0.194
0.165
0.204
0.119
IGLB
0.069
0.416
0.093
0.377
0.093
0.358
Table
2
compares calibration results for the three initial confidence-based scoring methods derived from different aggregation strategies (Section
4.2
).
avg_prob
computes the mean likelihood over the entire output sequence, including possible reasoning traces,
code_prob
averages only over the tokens of the generated code, and
tail_prob
averages over the last
40
40
tokens of the generation.
To ensure a fair comparison, we exclude examples where no code could be extracted, as code is required for
code_prob
.
We report results only for Qwen3 Coder, since GPT-OSS primarily failed in cases where no executable code was produced. Since – as mentioned above – we filtered these cases in this experiment, GPT-OSS produced mostly correct generations (
0.908
0.908
) compared to
0.634
0.634
for Qwen3 Coder. As GPT-OSS either produced correct or no code, we consider this experiment uninformative for that model.
For Qwen3 Coder,
avg_prob
achieves the best calibration results, both for the uncalibrated scores and after post-hoc calibration. The uncalibrated ECE for
avg_prob
was
0.048
0.048
and
0.052
0.052
lower than for
code_prob
and
tail_prob
, respectively. For all group-based calibration methods, we achieve the best ECE and BSS using
avg_prob
as the initial score. For instance, after IGLB calibration, the ECE remained
0.024
0.024
lower than with the other scores. This supports the intuition that the entire reasoning trace provides a valuable confidence signal, while the hypothesis of the generation tail being most relevant was not confirmed.
Based on these findings, we argue for
avg_prob
as a robust initial score that can be easily obtained from any LLM that provides access to its token likelihoods, and adopt it as the baseline in all further experiments.
6.3.
RQ3: Which types of group information contribute most to improved calibration?
Table
3
reports the group average squared error (gASCE) per group for the best performing methods from Table
1
. While the group-conditional unbiased regression methods (LINR and LOGR) often achieved the highest accuracy in Table
1
, IGLB yields the lowest gASCE for most groups. This observation aligns with theoretical expectations: LINR and LOGR ensure low group-conditional bias but do not guarantee calibration
within
each group, which is precisely what the gASCE metric captures. The bottom plots in Figure
1
illustrate this observation: average confidence scores per group plotted against their fraction of correct predictions align most closely with the diagonal for IGLB, while LINR and LOGR show slight deviations from the diagonal.
Figure 2.
Ablation experiments evaluating different group combinations on McEval. Results are averaged over the three LLMs.
Ablation experiments
To assess the impact of different grouping features from Section
3.2.1
, we performed ablations on McEval, omitting individual group categories and evaluating their effect on calibration. Figure
2
reports the mean
B
​
S
​
S
BSS
across all models, for the best-performing methods from Table
1
including group-agnostic methods for comparison.
When using only a single category (
complexity
,
language
or
length
),
language
provides the largest performance gain while
complexity
contributes the least. Interestingly, among the combinations of two categories,
complexity & length
yield the lowest results, suggesting that these categories contain redundant information, i.e. that in some cases, code length implicitly encodes information about code complexity and vice versa. The best-performing pair is
language & length
, meaning that omitting the
complexity
related groups is least harmful in our experiments. Overall, the highest performance is achieved when all three categories are included, indicating that, despite the previously mentioned redundancies, the categories still provide complementary information.
Table 3.
Comparison of Group averaged Squared Error (gASCE) for complexity- and length-based groups and some language-based ones for Qwen3 Coder on McEval.
gASCE
type
uncalib.
Platt
LINR
LOGR
IGLB
low
comp.
0.052
0.005
0.003
0.045
0.003
medium
comp.
0.119
0.006
0.011
0.074
0.005
high
comp.
0.261
0.047
0.008
0.061
0.007
len_low
length
0.041
0.003
0.003
0.038
0.003
len_high
length
0.156
0.006
0.006
0.070
0.003
loc_low
length
0.051
0.007
0.003
0.055
0.006
loc_high
length
0.149
0.006
0.007
0.050
0.003
c
lang.
0.130
0.039
0.026
0.017
0.019
python
lang.
0.064
0.051
0.037
0.076
0.027
lua
lang.
0.119
0.031
0.032
0.014
0.033
rust
lang.
0.556
0.250
0.037
0.036
0.036
7.
Threats to Validity
We identified the following potential threats to validity in our study.
First, two of our benchmarks, LiveCodeBench and MultiPL-E, contain artificial problems that may not fully reflect real-world software development. In contrast, McEval is based on real-world code samples, which gives confidence that the positive results observed on this benchmark may generalize to practical SE scenarios.
Second, our analysis focuses on function synthesis and does not cover the full spectrum of code generation tasks. Other software engineering applications may exhibit different calibration behaviors and should be explored in future work.
Finally, a common concern when evaluating LLMs is data leakage. We mitigate this risk to some extent by using two very recent datasets (LiveCodeBench and McEval), for which most samples were published after the models’ knowledge cutoff dates.
8.
Conclusions
In this paper, we argue that calibrated confidence scores can enable more reliable and developer-friendly integration of LLM-generated code into software development workflows. Building on prior findings that LLMs are often poorly calibrated for code synthesis, we replicated this result for current reasoning models and explored a range of post-hoc calibration methods to address the issue. In particular, we introduce the concept of
multicalibration
, which – to our knowledge – has not been previously explored in the context of code generation, and demonstrated its effectiveness compared to classical calibration techniques.
Our experiments highlight that incorporating structured, code-related group information can significantly improve calibration quality. While our study is not exhaustive, it provides a methodological and empirical foundation for further work on confidence calibration in SE. Future directions include exploring alternative initial scoring functions (e.g., based on distributional features of token likelihoods or on internal LLM states) and extending calibration analysis to broader tasks, such as repository-level code generation or program repair. To support this, we make code and data publicly available as a replication package
(
campos2025replication
)
.