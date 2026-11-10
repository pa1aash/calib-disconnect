---
title: Trained on Tokens, Calibrated on Concepts:The Emergence of Semantic Calibration
  in LLMs
id: trained-on-tokens-calibrated-on-conceptsthe-emergence-of-semantic-calibration-in
tags:
- code-llm-confidence-positioning-d82d00
- w3-4
- l2-adjacent
created: '2026-11-10T08:23:51.715801Z'
updated: '2026-11-10T08:25:01.508224Z'
source: https://arxiv.org/html/2511.04869
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:51.715304Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Nakkiran et al (Apple), arXiv 2511.04869v1, full text. Theory (B-calibration)
  plus experiments: base LLMs are semantically calibrated on open-domain QA (TriviaQA,
  GSM8k etc, four datasets, Qwen/Gemini/Mistral/Llama 0.5B-70B, SmoothECE); RL/DPO
  instruction tuning and CoT break it (Fig 2, Base/Instruct x Concise/Sentence/CoT).
  Sampling-based readout only; NO code, NO execution labels, NO probes. Bears on L2
  base-vs-instruct as general-domain precedent for the base-vs-instruct calibration
  contrast, so code-specific base/instruct pairing remains unoccupied here.'
---

Trained on Tokens, Calibrated on Concepts:The Emergence of Semantic Calibration in LLMs
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2511.04869v1 [cs.CL] 06 Nov 2025
Trained on Tokens, Calibrated on Concepts:
The Emergence of Semantic Calibration in LLMs
Preetum Nakkiran
Arwen Bradley
Adam Goliński
Eugene Ndiaye
Michael Kirchhof
Sinead Williamson
Affiliation:
Apple
August 24, 2026
Abstract
Large Language Models (LLMs) often lack meaningful confidence estimates for their outputs. While base LLMs are known to exhibit next-token calibration,
it remains unclear whether they can assess confidence in the actual meaning of their responses beyond the token level.
We find that, when using a certain sampling-based notion of semantic calibration, base LLMs are remarkably well-calibrated:
they can meaningfully assess confidence in
open-domain question-answering tasks,
despite not being explicitly trained to do so.
Our main theoretical contribution
establishes a mechanism for why semantic calibration emerges
as a byproduct of next-token prediction, leveraging a recent connection between calibration and local loss optimality.
The theory relies on a general definition of “
B
B
-calibration,”
which is a notion of calibration parameterized by
a choice of equivalence classes (semantic or otherwise).
This theoretical mechanism leads to a testable prediction:
base LLMs will be semantically calibrated when they can easily predict their own distribution over semantic answer classes before generating a response.
We state three implications of this prediction, which we validate through experiments:
(1) Base LLMs are semantically calibrated across question-answering tasks,
(2) RL instruction-tuning systematically breaks this calibration,
and (3) chain-of-thought reasoning breaks calibration.
To our knowledge, our work provides the first principled explanation of when and why semantic calibration emerges in LLMs.
1
Introduction
As Large Language Models (LLMs) become increasingly capable,
it is important to understand the nature and extent of their uncertainty.
While LLMs can produce fluent answers to a range of difficult questions,
they do not inherently convey any sense of certainty in those answers.
Addressing this is an active research question:
can we extract a meaningful notion of confidence in an LLM’s response?
This question is scientifically interesting even aside from applications:
it is a way of asking, do LLMs “know what they don’t know”?
(
Kadavath et al., 2022
)
In the classification literature, one well-understood criterion for
uncertainty quantification is
calibration
:
do the predicted probabilities reflect empirical frequencies?
For example, if an image classifier is 80% confident
on a set of inputs,
then it should be correct on 80% of those predictions.
To apply this definition to LLMs, one approach is to treat the LLM
as a classifier that predicts the next-token, given all previous tokens.
There is strong empirical and theoretical evidence that base LLMs,
which are only pre-trained with the maximum likelihood loss, are typically
next-token-calibrated
(
OpenAI, 2023
;
Zhang et al., 2024
;
Desai and Durrett, 2020
)
.
Next-token calibration is a meaningful notion of calibration in certain settings like True/False or multiple choice questions, where a single token encapsulates the entire response
(
Kadavath et al., 2022
;
Plaut et al., 2025
)
.
For example, if we ask an LLM a multiple-choice question, then
its probability distribution on the next-token (A/B/C/D) defines a
prediction which is often calibrated.
However, when the model produces long-form answers to open-ended questions,
we desire a notion of uncertainty with respect to the
semantic meaning
of the response, which next-token calibration does not
directly capture.
E.g. if we ask the LLM “What is the capital of France?,”
then it might answer “Paris” or “It’s Paris” or “The capital of France is Paris,”
and it is not clear how to use token-wise probabilities to derive meaningful confidences
in the response.
Prior works have proposed a variety of notions of semantic confidence for long-form text, including verbalized measures and sampling-based measures
(e.g.
semantic entropy
of
Farquhar et al. (2024)
).
See
Vashurin et al. (2025)
for a comprehensive overview.
However, from the empirical data it is unclear whether LLMs are naturally calibrated
with respect to
any
of these semantic notions of confidence,
without being specifically trained for calibration
(
Kadavath et al., 2022
;
Yin et al., 2023
;
Band et al., 2024
;
Kapoor et al., 2024
;
Yoon et al., 2025
;
Mei et al., 2025
;
Tian et al., 2023
)
.
Empirically, calibration may depend on many factors:
the test distribution (math, trivia, etc.),
the post-training procedure (RLHF, DPO, RLVR, none, etc.),
the inference-time procedure (few-shot examples, chain-of-thought (CoT), best-of-K, etc.), the model size, the model architecture, the sampling temperature, etc.
All of these factors have been posited to affect calibration, for reasons that are not yet well understood
(
Kadavath et al., 2022
;
OpenAI, 2023
;
Leng et al., 2025
;
Xiao et al., 2025
;
Zhang et al., 2024
;
Wang et al., 2025
)
.
A priori, there is no reason to expect
emergence
1
1
1
We use
emergent
here to mean a
structural regularity that arises implicitly (“for free”) due to system dynamics, not as a result of explicit external constraints. That is, “Emergence Through Compression” in the terminology of
Krakauer et al. (2025)
.
We do not mean to discuss changes as a result of model scaling, which is another common use of the term emergence
(
Wei et al., 2022
)
.
of any of these forms of semantic calibration as a byproduct of standard pre-training with the maximum likelihood loss.
In this work, we propose and test a mechanism by which
a particular type of sampling-based semantic calibration actually can emerge for a large class of LLMs.
At a high level, the mechanism treats the LLM as a standard multi-class classifier (by collapsing outputs with the same semantic meaning),
and then adapts recent theoretical results
on mechanisms of classifier calibration
(
Gopalan et al., 2024
;
Błasiok et al., 2023b
;
Błasiok et al., 2024
)
.
Fig.
1
illustrates the overall phenomenon of semantic calibration
2
2
2
This definition of semantic calibration is
closely related to semantic entropy
(
Farquhar et al., 2024
)
,
as well as the sampling-based definitions of confidence in
Wang et al. (2023)
,
Wei et al. (2024)
, and
Lamb et al. (2025)
.
, described in detail in the next section. To our knowledge, our work is the first to propose a theoretically plausible mechanism
for semantic calibration in LLMs, and we validate the predictions of this theory empirically.
Figure 1
:
Semantic calibration
refers to calibration of an
LLM-induced semantic classifier
(dashed box): the classifier induced by
post-processing LLM outputs with a given semantic collapsing function,
which we refer to as
B
B
throughout.
To measure semantic confidence calibration:
for a given question, sample multiple temperature
T
=
1
T\!=\!1
generations,
and extract semantic answers by applying the
collapsing function
B
B
(e.g. a strong LLM prompted to extract one-word answers).
This yields an empirical distribution over semantic classes (above: Paris, Rome, Berlin),
which we treat as the classifier output.
This classifier output defines a semantic prediction (=argmax probability)
and a semantic confidence (=max probability).
Semantic confidence calibration
means,
over all questions, these predictions are confidence-calibrated in the
standard classification sense.
Summary of Contributions.
We empirically show that LLMs
are
semantically-calibrated surprisingly often, for certain settings and types of questions.
We offer a candidate theoretical mechanism to explain how this calibration emerges from standard LLM training (that does not explicitly encourage it), and discuss under which settings and for which questions we expect it.
The basic prediction of our theory is that semantic calibration is likely to hold when
(1) the model is a base LLM, and
(2) the model is able to
immediately
predict the probability that its answer will land in a given semantic class, even before it has started to generate it. Specifically, this immediate prediction should be “easy to learn” in the sense that, for example, the model could be LoRA-adapted to perform it.
Intuitively, in order to be semantically calibrated, the model must
“know” how likely it is to generate a “Paris”-type answer,
before it has determined exactly how it will phrase its answer.
This theoretical insight leads to a number of practical predictions
about which models and tasks should be semantically calibrated, which
we then test experimentally.
Organization.
We start by formally defining the notion
of calibration we consider in
Sec.
2
.
In
Sec.
3
, we introduce our proposed theoretical mechanism for
emergent calibration, and state our formal results.
In
Sec.
4
, we apply the theory
to make three concrete predictions about when LLMs are semantically calibrated,
and in
Sec.
5
, we experimentally test these predictions.
Figure 2
:
Semantic Calibration of LLMs.
Overlaid reliability diagrams evaluating semantic calibration of
Qwen, Gemini, Mistral, and Llama-family models of sizes
from 0.5B to 70B, on four datasets.
Each model is prompted to respond in one of three different styles:
a single word (“concise”), a complete sentence (“sentence”),
or using chain-of-thought (“CoT”).
This yields 6 color-coded configurations for each model:
(model-variant, response-style)
∈
\in
{Base, Instruct}
×
\times
{Concise, Sentence, CoT}.
We group these configurations into two rows based on our theoretical predictions.
First row (predicted calibrated):
Reliability diagrams of all configurations
predicted to be confidence-calibrated according to our theory:
base models with
concise
or
sentence
response types.
Second row (not predicted calibrated):
Configurations which need not be calibrated according to our theory:
post-trained instruct models with any response type:
concise
,
sentence
,
chain-of-thought
;
and
base models with chain-of-thought
.
Third row:
Box plots summarizing the distribution of calibration errors for each of the 6 configurations.
Only the first two configurations
(
base-concise
and
base-sentence
)
are reliably well-calibrated, as predicted by our theory.
Individual reliability diagrams for all experiments are in
App.
F
.
Figure 3
:
Reliability diagrams demonstrating
semantic confidence-calibration
of base (pretrained-only) LLMs across
various combinations of datasets, models, and prompts.
Calibration error measured with SmoothECE (smECE),
average confidence and accuracy marked with a black cross,
and density of semantic confidences shown in gray histogram;
details in Appendix
D.2
.
2
Semantic Calibration and
B
B
-Calibration
We now informally describe our framework; formal definitions follow in
Sec.
2.1
.
The core of our approach is a collapsing function
B
B
which post-processes
the LLM’s raw text outputs, mapping each generation to one of a finite set of classes.
Of particular interest are
semantic collapsing functions
3
3
3
To implement this function, we use a strong auxiliary LLM prompted to extract a canonical short answer from a long-form string. Details in
App.
D
.
, which we focus on now.
As illustrated in
Fig.
1
,
a semantic collapsing function implicitly transforms the LLM into an
LLM-induced semantic classifier
:
For a given question, the classifier’s output is a distribution over semantic classes,
whose probabilities can be empirically estimated by sampling multiple generations from the LLM and applying
B
B
to each.
From this distribution, we define the
semantic confidence as the probability of the most-likely semantic class,
and the semantic accuracy as whether the most-likely semantic class matches the ground truth’s semantic class.
The LLM is
semantically confidence-calibrated
if these confidences and accuracies are calibrated across a dataset—e.g.,
among questions with 70% semantic confidence, the average semantic accuracy is also 70%.
This definition coincides with
Lamb et al. (2025)
’s definition of “Empirical Semantic Confidence”
when applied to the full distribution.
For example,
Fig.
3
measures calibration of several models using this approach (full experimental details in
Sec.
5
).
2.1
Notation and Setup
We now establish the notation used throughout the paper.
We assume that our semantic collapsing function outputs at most
K
∈
ℕ
K\in\mathbb{N}
classes, which we represent by the set of indices
[
K
]
≡
{
1
,
…
,
K
}
[K]\equiv\{1,\dots,K\}
. We allow
K
K
to be arbitrarily large. We identify these classes with the set of standard basis vectors
ℰ
K
⊂
ℝ
K
\mathcal{E}_{K}\subset\mathbb{R}^{K}
. The set of probability distributions over a finite set
S
S
is denoted
Δ
⁡
(
S
)
\Delta(S)
. For convenience, we use the shorthand
Δ
K
≡
Δ
⁡
(
[
K
]
)
\Delta_{K}\equiv\Delta([K])
for the probability simplex over the
K
K
classes.
Language Model and Data.
Let
𝒱
\mathcal{V}
be the model’s vocabulary. We assume throughout that the evaluation data comes from a ground-truth distribution
𝒟
\mathcal{D}
over prompt-completion pairs
(
x
,
y
)
∈
𝒱
∗
×
𝒱
N
(x,y)\in\mathcal{V}^{*}\times\mathcal{V}^{N}
, where
N
N
is a maximum generation length. An LLM is a function
p
θ
:
𝒱
∗
→
Δ
⁡
(
𝒱
N
)
p_{\theta}:\mathcal{V}^{*}\to\Delta(\mathcal{V}^{N})
that maps a prompt
x
x
to a distribution over output strings. We use conventional notation:
p
x
≡
p
θ
(
⋅
∣
x
)
p_{x}\equiv p_{\theta}(\cdot\mid x)
is the entire distribution over sequences for a given prompt,
so we can denote
p
x
​
(
z
)
=
p
θ
​
(
z
∣
x
)
p_{x}(z)=p_{\theta}(z\mid x)
as the probability of a specific sequence
z
z
.
The conditional probability of the next token is denoted
p
θ
​
(
z
i
∣
x
,
z
<
i
)
p_{\theta}(z_{i}\mid x,z_{<i})
.
To distinguish model outputs from the dataset, we use
z
∈
𝒱
N
z\in\mathcal{V}^{N}
for generated strings and
y
∈
𝒱
N
y\in\mathcal{V}^{N}
for ground-truth completions from
𝒟
\mathcal{D}
.
Collapsing function.
The core of our framework is the collapsing function
B
:
𝒱
∗
×
𝒱
N
→
[
K
]
B:\mathcal{V}^{*}\times\mathcal{V}^{N}\to[K]
that classifies a given prompt-completion pair into one of
K
K
categories.
In our theory,
B
B
is allowed to be arbitrary, but we often will think of it as a
“semantic collapsing” function
, grouping many different strings into a single semantic class, as visualized in
Fig.
1
.
An example of such a function is described in
App.
D
.
For convenience, we write
B
x
​
(
z
)
≡
B
⁡
(
x
,
z
)
B_{x}(z)\equiv B(x,z)
to emphasize its role as a classifier for outputs
z
z
given a fixed prompt
x
x
.
2.2
Confidence Calibration
We first recall the relevant definitions of calibration in the multi-class setting (for a unified treatment, see
Gopalan et al. (2024, Section 2)
). In the
K
K
-class setting,
classifiers output values
c
∈
Δ
K
c\in\Delta_{K}
and the true labels take values
y
∈
ℰ
K
y\in\mathcal{E}_{K}
(one-hot encodings).
Calibration is a property defined for
any
joint distribution of
prediction-label pairs
(
c
,
y
)
∈
Δ
K
×
ℰ
K
(c,y)\in\Delta_{K}\times\mathcal{E}_{K}
, regardless of whether it was
generated by a classifier.
We will focus primarily on
confidence calibration
, which only considers the probability assigned to the predicted class; however, we provide analogous results for full calibration in
Sec.
E.4
.
The following definition is standard:
Definition 1
(Confidence-calibration)
.
A distribution
𝒟
\mathcal{D}
over prediction-output pairs
(
c
,
y
)
∈
Δ
K
×
ℰ
K
(c,y)\in\Delta_{K}\times\mathcal{E}_{K}
is
perfectly confidence-calibrated
if
𝔼
(
c
,
y
)
∼
𝒟
[
y
k
⋆
−
c
k
⋆
∣
c
k
⋆
]
≡
0
​
where
​
k
⋆
←
argmax
k
∈
[
K
]
c
k
.
\mathop{\mathbb{E}}_{\begin{subarray}{c}(c,y)\sim\mathcal{D}\end{subarray}}\left[y_{k^{\star}}-c_{k^{\star}}\mid c_{k^{\star}}\right]\equiv 0\text{ where }k^{\star}\leftarrow\argmax_{k\in[K]}c_{k}.
The definition depends crucially on the distribution
𝒟
\mathcal{D}
.
In this work we take
𝒟
\mathcal{D}
to be the evaluation distribution of interest (e.g. TriviaQA, GSM8k, etc),
unless otherwise specified.
From Language Model to Categorical Predictor
For a given prompt
x
x
, we obtain a distribution over
K
K
categories by
pushing-forward the LLM’s output distribution
p
θ
(
⋅
∣
x
)
p_{\theta}(\cdot\mid x)
via the function
B
x
B_{x}
.
Specifically, the distribution over categories
π
x
:=
B
x
♯
p
x
≡
B
x
♯
p
θ
(
⋅
∣
x
)
\pi_{x}:=B_{x}\sharp p_{x}\equiv B_{x}\sharp p_{\theta}(\cdot\mid x)
assigns to each category
k
∈
[
K
]
k\in[K]
the sum of probabilities of all strings
z
z
that
B
x
B_{x}
maps to that category:
(
B
x
♯
p
x
)
(
k
)
=
Pr
z
∼
p
θ
(
⋅
∣
x
)
[
B
x
(
z
)
=
k
]
=
∑
z
:
B
x
​
(
z
)
=
k
p
θ
(
z
∣
x
)
.
(B_{x}\sharp p_{x})(k)=\Pr_{z\sim p_{\theta}(\cdot\mid x)}[B_{x}(z)=k]=\sum_{z\,:\,B_{x}(z)=k}p_{\theta}(z\mid x).
(2.1)
This process transforms the original prompt-answer pair
(
x
,
y
)
(x,y)
from the dataset
𝒟
\mathcal{D}
into a pair suitable for calibration analysis:
(
B
x
​
♯
​
p
x
,
B
x
​
(
y
)
)
(B_{x}\sharp p_{x},B_{x}(y))
, where
B
x
​
♯
​
p
x
B_{x}\sharp p_{x}
is the model’s predicted distribution over categories and
B
x
​
(
y
)
B_{x}(y)
is the ground-truth category.
Now, we say that the model
p
θ
p_{\theta}
is
B
B
-confidence-calibrated if the induced distribution over
(
B
x
​
♯
​
p
x
,
B
x
​
(
y
)
)
(B_{x}\sharp p_{x},B_{x}(y))
is confidence-calibrated.
That is,
B
B
-confidence-calibration means if the generated and ground-truth answers are both post-processed by
B
B
, then the resulting
K
K
-way-classifier is confidence-calibrated.
Definition 2
(
B
B
-confidence-calibration)
.
The model
p
θ
p_{\theta}
is
B
B
-confidence-calibrated
with respect to distribution
𝒟
\mathcal{D}
if
the induced distribution over pairs
(
B
x
​
♯
​
p
x
,
B
x
​
(
y
)
)
∈
Δ
K
×
[
K
]
(B_{x}\sharp p_{x},B_{x}(y))\in\Delta_{K}\times[K]
is perfectly confidence-calibrated (per
Definition
1
).
Our entire framework is well-defined for any function
B
B
,
though we usually choose
B
B
to be a semantic-collapsing function.
In general, an LLM might be
B
B
-confidence-calibrated for some choices of
B
B
, but not others—one goal of our theory is to understand why.
3
Theoretical Mechanism
Our conjectured mechanism for emergent calibration
builds on the work of
Błasiok et al. (2023b)
;
Błasiok et al. (2024)
which connects the
statistical
property of calibration
to the
optimization
property of local loss optimality.
The core intuition is that a miscalibrated model implies the existence of a “simple” perturbation
to the model that would reduce its test loss.
For example, suppose an LLM is semantically miscalibrated in the following way:
on questions where it is 70% semantically-confident, it is on average only 60% accurate.
Then, an obvious way to improve the LLM’s test loss is:
whenever the original LLM was 70% semantically confident,
it should downweight the probability mass it places on all strings in its majority semantic class, thereby decreasing its confidence.
We argue that base LLMs, trained to minimize cross-entropy loss, should not leave such “easy wins” on the table, and thus should be well-calibrated.
This example reveals some of the subtlety in the LLM setting: unlike standard classifiers,
the LLM does not explicitly output its [semantic] confidences.
Thus to implement such a loss-improving perturbation during pretraining,
the LLM must implicitly “know” its semantic confidence for a given question even before generating its answer—in order to know what type of upweighting/downweighting
of answer strings is required.
In settings where the LLM does not “know” its semantic confidences (informally),
we may expect poor calibration—we will see this aspect in both our theory and experiments.
A technical overview of our results is in
Sec.
3.1
,
followed by formal theorem statements in
Sec.
3.2
and
Sec.
3.3
.
All proofs are deferred to
App.
E
.
3.1
Conjectured Mechanism: Overview
LLM is
B
B
-confidence
-calibrated
LLM is
𝒲
B
\mathcal{W}_{B}
-locally
-loss-optimal
LLM can easily learn all
𝒲
B
\mathcal{W}_{B}
-perturbations
LLM “knows” its
intermediate
B
B
-confidences
LLM “knows”
its own
B
B
-class distribution
x
↦
B
x
​
♯
​
p
x
θ
x\mapsto B_{x}\sharp p^{\theta}_{x}
≈
\approx
Thm.
10
for base LLMs
Thm.
7
A
B
C
D
Claim
11
(experimentally testable)
Figure 4
:
Conjectured Mechanism for Semantic Calibration.
Implications have varying levels of support:
the
solid blue
arrow
(
)
has a formal proof;
the
dashed blue
arrows
(
)
have proofs of “morally similar” (but weaker) implications.
Claim
11
encompasses the full chain of implications,
and has experimental support.
Fig.
4
illustrates our conjectured mechanism.
There are three main steps in the conjecture,
with
different degrees of evidence for each step.
For the first step, we have a fully rigorous proof.
For the other two steps, we have partial theoretical evidence:
proofs of weaker claims which are “morally similar” to our conjectured claim.
Finally, we have experimental evidence for our overall conjecture
(presented later in
Sec.
5
).
We outline each step below,
following
Fig.
4
from right-to-left.
(C)
(D):
The first step of our argument, described in more detail in
Sec.
3.2
,
is a general equivalence between calibration and local loss optimality.
We say an LLM is locally-loss-optimal if its test loss cannot be improved
by post-processing its output distribution via any function in some given set of perturbation functions
(formally,
Definition
5
).
For a particular choice of perturbation functions,
this turns out to exactly characterize
B
B
-calibration.
We prove in
Thm.
7
that for any choice of
collapsing function
B
B
,
B
B
-confidence-calibration is
equivalent
to local-loss-optimality with respect to
a corresponding family of perturbations, denoted
𝒲
B
\mathcal{W}_{B}
.
Roughly speaking, this family
𝒲
B
\mathcal{W}_{B}
consists of perturbations like our earlier example:
“If the
B
B
-class-confidence was 70%, then downweight the probability
of generating all strings in the majority
B
B
-class.”
Overall,
Thm.
7
tells us that if we want to understand
when LLMs are
B
B
-confidence-calibrated, we can equivalently understand
which types of perturbations LLMs are loss-optimal with respect to.
(B)
(C):
At this point, we invoke an informal
assumption proposed in
Błasiok et al. (2023b)
, and likely folklore much earlier:
we assume that base LLMs are nearly locally-loss-optimal on their pretraining distribution, w.r.t.
any perturbation that is “easy” for the LLM to learn.
We state this assumption more precisely as
Claim
22
in the Appendix.
Błasiok et al. (2024, Theorem 1.2)
offers partial theoretical justification for this claim, by proving that, intuitively, if small models can represent a set of perturbations, then ERM over a family of slightly larger models yields local loss optimality w.r.t. these perturbations; this serves as a approximate representational analog of the desired assumption.
The intuition is that pretraining not leave any easy wins
on the table: if a simple (i.e. easily-learnable) perturbation could have
improved the test loss, the LLM would have learned it during training.
4
4
4
Technically, we need local-loss-optimality
not only for the overall pretraining distribution, but also for each evaluation distribution individually (TriviaQA, GSM8k, etc), since we are evaluating calibration on individual distributions.
We will however assume that the latter holds
(which is plausible if each evaluation distribution is a reasonably-sized sub-distribution of the pretraining distribution on which local-loss-optimality holds).
We agree with
Błasiok et al. (2023b)
that this assumption is plausible, because it is fairly weak; it does not require that models are
globally
optimal in any sense.
(A)
(B):
From the above two points, we can conclude that a base LLM
will be
B
B
-confidence-calibrated if the corresponding perturbation family
𝒲
B
\mathcal{W}_{B}
is simple for the LLM to learn.
But when is
𝒲
B
\mathcal{W}_{B}
simple to learn?
This is subtle because the perturbations
𝒲
B
\mathcal{W}_{B}
are
defined over the
sequence-level
probability distribution
but LLMs must implement perturbations by modifying
next-token
probabilities.
For example, in order to implement a perturbation such as
“increase the probability of ultimately generating a Paris-type answer”,
the model must begin by deciding how to adjust its
first token
probabilities in order to achieve this.
We bridge this gap in
Thm.
10
,
by proving a representational analogue of the
implication
(A)
(B)
of
Fig.
4
:
we show that if the LLM “knows” its own induced distribution over
B
B
-classes at each intermediate point during generation (even the very beginning),
then it can implement the associated family of perturbations
𝒲
B
\mathcal{W}_{B}
in a “simple” way. (Notably, this does not require the model to know the
correct answer’s
B
B
-class, only that of its own generation.)
Formally, we prove a circuit-complexity version of this:
the next-token probabilities of the perturbed model
can be computed with a shallow circuit given oracle access to the intermediate
B
B
-confidence functions, and the original next-token probabilities. In practice, we will focus primarily on the model’s ability to predict its
B
B
-distribution at the beginning of generation (before outputting the first token). Intuitively, this is more likely to hold for straightforward questions such as “What is the capital of France?” than questions requiring many steps of reasoning— we will say more about this in the following section.
Putting everything together, the overall mechanism predicts that a base LLM will be
B
B
-confidence-calibrated if the LLM “knows” the distribution of
B
B
-classes of its own answers
(i.e. if it can be LoRA-adapted to immediately output this
B
B
-class distribution, given only the question).
When
B
B
is a semantic collapsing function,
this theory naturally suggests a number of practical predictions about which models and tasks should be semantically calibrated,
which we explore and test experimentally in
Sec.
5
.
The next several sections give the formal theory supporting the mechanism we have just outlined.
3.2
B
B
-calibration and local loss optimality
We now setup and establish
the equivalence between calibration and local loss optimality
(
Thm.
7
).
We consider the sequence-level cross-entropy loss, which decomposes into the
standard autoregressive next-token log-loss:
𝔼
(
x
,
y
)
∼
𝒟
[
ℓ
(
y
,
p
x
)
]
=
𝔼
(
x
,
y
)
∼
𝒟
[
−
∑
i
∈
[
N
]
log
p
θ
(
y
i
∣
y
<
i
,
x
)
]
.
\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}[\ell(y,p_{x})]=\mathop{\mathbb{E}}_{\begin{subarray}{c}(x,y)\sim\mathcal{D}\end{subarray}}\left[-\sum_{i\in[N]}\log p_{\theta}(y_{i}\mid y_{<i},x)\right].
We will use the following notion of perturbing a probability distribution,
known as
exponential tilting
(
Cover and Thomas, 1999
, Chapter 11)
,
which turns out to be the appropriate notion
5
5
5
The appropriate notion of perturbation
depends on the loss function via convex duality; see
Sec.
E.3
for more details.
for the cross-entropy loss.
Definition 3
(Perturbation operator)
.
Given a distribution
f
∈
Δ
⁡
(
𝒱
N
)
f\in\Delta(\mathcal{V}^{N})
over sequences,
and a signed measure
μ
∈
ℝ
|
𝒱
N
|
\mu\in\mathbb{R}^{|\mathcal{V}^{N}|}
,
define the perturbed distribution
(
f
⋆
μ
)
∈
Δ
⁡
(
𝒱
N
)
(f\star\mu)\in\Delta(\mathcal{V}^{N})
as:
∀
z
∈
𝒱
N
:
(
f
⋆
μ
)
[
z
]
\displaystyle\penalty\ \forall z\in\mathcal{V}^{N}:\quad(f\star\mu)[z]
:
=
softmax
⁡
(
μ
⁡
[
z
]
+
log
⁡
f
⁡
[
z
]
)
.
\displaystyle:=\mathrm{softmax}\big(\mu[z]+\log f[z]\big).
(3.1)
This is an operation defined over probability distributions.
We can use it to perturb a model in the following way.
Recall that for a model
p
θ
p_{\theta}
and prompt
x
∈
𝒱
∗
x\in\mathcal{V}^{*}
,
we write
p
x
≡
p
θ
(
⋅
∣
x
)
p_{x}\equiv p_{\theta}(\cdot\mid x)
.
Definition 4
(Perturbed model)
.
Given a model
p
θ
:
x
↦
p
x
p_{\theta}:x\mapsto p_{x}
and a perturbation function
w
:
𝒱
∗
×
Δ
⁡
(
𝒱
N
)
→
ℝ
|
𝒱
N
|
w:\mathcal{V}^{*}\times\Delta(\mathcal{V}^{N})\to\mathbb{R}^{|\mathcal{V}^{N}|}
,
we define the perturbed model
(
p
θ
⋆
w
)
≡
p
~
(p_{\theta}\star w)\equiv\tilde{p}
as
p
~
:
x
↦
(
p
x
⋆
w
x
)
where
​
w
x
≡
w
⁡
(
x
,
p
x
)
∈
ℝ
|
𝒱
N
|
\tilde{p}:x\mapsto(p_{x}\star w_{x})\quad\mathrm{where}\penalty\ w_{x}\equiv w(x,p_{x})\in\mathbb{R}^{|\mathcal{V}^{N}|}
(3.2)
That is, a perturbation function
w
w
takes as input the prompt
x
x
and the model’s generative distribution
p
x
p_{x}
,
and defines how to perturb the generative distribution for that specific prompt.
We can now define local loss optimality with respect to an
arbitrary family of perturbation functions
𝒲
\mathcal{W}
.
Definition 5
(
𝒲
\mathcal{W}
-local loss optimality)
.
We say that model
p
θ
p_{\theta}
is
𝒲
\mathcal{W}
-locally-loss-optimal
on distribution
𝒟
\mathcal{D}
if
∀
w
∈
𝒲
:
𝔼
(
x
,
y
)
∼
𝒟
[
ℓ
(
y
,
p
x
)
]
≤
𝔼
(
x
,
y
)
∼
𝒟
[
ℓ
(
y
,
p
x
⋆
w
x
)
]
where
w
x
≡
w
(
x
,
p
x
)
,
p
x
≡
p
θ
(
⋅
∣
x
)
.
\penalty\ \forall w\in\mathcal{W}:\quad\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}[\ell(y,p_{x})]\leq\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}[\ell(y,p_{x}\star w_{x})]\quad\mathrm{where}\penalty\ w_{x}\equiv w(x,p_{x})\penalty\ ,\penalty\ p_{x}\equiv p_{\theta}(\cdot\mid x).
Next we define a
specific class of perturbations
𝒲
B
\mathcal{W}_{B}
which characterize
B
B
-confidence-calibration.
The formal definition is somewhat technical, based on the language of weighted calibration
developed in
Gopalan et al. (2024)
.
Definition 6
(Semantic Perturbation Function Classes)
.
Given an arbitrary collapsing function
B
x
​
(
z
)
∈
[
K
]
B_{x}(z)\in[K]
,
we define the class
𝒲
B
\mathcal{W}_{B}
of perturbation functions
w
τ
​
(
x
,
p
x
)
∈
ℝ
|
𝒱
N
|
w_{\tau}(x,p_{x})\in\mathbb{R}^{|\mathcal{V}^{N}|}
as follows.
Each function
w
τ
w_{\tau}
is indexed by a map
τ
:
[
0
,
1
]
→
[
−
1
,
1
]
\tau:[0,1]\to[-1,1]
,
and generates a perturbation vector in
ℝ
|
𝒱
N
|
\mathbb{R}^{|\mathcal{V}^{N}|}
based on the prompt
x
x
and the model’s predictive distribution
p
x
p_{x}
.
𝒲
B
\displaystyle\mathcal{W}_{B}
:
=
{
w
τ
∣
τ
:
[
0
,
1
]
→
[
−
1
,
1
]
}
\displaystyle:=\{w_{\tau}\mid\tau:[0,1]\to[-1,1]\}
where
w
τ
​
(
x
,
p
x
)
∈
ℝ
|
𝒱
N
|
w_{\tau}(x,p_{x})\in\mathbb{R}^{|\mathcal{V}^{N}|}
is defined componentwise as follows.
For index
z
∈
𝒱
N
z\in\mathcal{V}^{N}
,
w
τ
(
x
,
p
x
)
[
z
]
=
τ
(
π
x
[
k
∗
]
)
⋅
𝟙
{
B
x
(
z
)
=
k
∗
}
,
where
π
x
:=
B
x
♯
p
x
,
and
k
∗
←
argmax
k
∈
[
K
]
π
x
[
k
]
.
\displaystyle w_{\tau}(x,p_{x})[z]=\tau\big(\pi_{x}[k^{*}]\big)\cdot\mathds{1}\{B_{x}(z)=k^{*}\},\penalty\ \mathrm{where}\penalty\ \pi_{x}:=B_{x}\sharp p_{x},\quad\mathrm{and}\penalty\ \penalty\ k^{*}\leftarrow\argmax_{k\in[K]}\pi_{x}[k].
These perturbations implement a re-mapping of the
B
B
-class-confidences governed by the function
τ
\tau
.
For example, if
B
B
is a semantic collapsing function, then
a perturbation
w
τ
w_{\tau}
could implement the change
“whenever the semantic confidence of a question is 70%, decrease the semantic confidence to 60%,
by downweighting the probability of all strings in the top semantic class.”
Unpacking the notation in
Definition
6
:
π
x
∈
Δ
K
\pi_{x}\in\Delta_{K}
is the model’s distribution over
B
B
-classes,
k
∗
∈
[
K
]
k^{*}\in[K]
is the top
B
B
-class,
z
∈
𝒱
N
z\in\mathcal{V}^{N}
is a string,
and
w
τ
​
(
x
,
p
x
)
​
[
z
]
w_{\tau}(x,p_{x})[z]
represents how much
the perturbed model should up-weight the answer string
z
z
,
for question
x
x
. Then,
w
τ
​
(
x
,
p
x
)
​
[
z
]
⏟
Desired perturbation to
p
θ
​
(
z
∣
x
)
=
τ
⁡
(
π
x
​
[
k
∗
]
⏟
B
-confidence
)
⋅
𝟙
{
B
x
(
z
)
=
k
∗
}
⏟
z
in top
B
-class?
.
\displaystyle\underbrace{w_{\tau}(x,p_{x})[z]}_{\textrm{Desired perturbation to $p_{\theta}(z\mid x)$}}=\tau\big(\underbrace{\pi_{x}[k^{*}]}_{\textrm{$B$-confidence}}\big)\cdot\underbrace{\mathds{1}\{B_{x}(z)=k^{*}\}}_{\textrm{$z$ in top $B$-class?}}.
We can now state the main result of this section
(see
App.
E
for all proofs).
Theorem 7
(Equivalence of Calibration and Local Loss Optimality)
.
For all models
p
θ
p_{\theta}
, collapsing functions
B
B
and distributions
𝒟
\mathcal{D}
, the following are equivalent:
1.
The model
p
θ
p_{\theta}
is perfectly
B
B
-confidence-calibrated
on
𝒟
\mathcal{D}
2.
The model
p
θ
p_{\theta}
is
𝒲
B
\mathcal{W}_{B}
-locally-loss-optimal
on
𝒟
\mathcal{D}
.
Remark 8
.
Thm.
7
states a simplified version
of our full theoretical results, for the sake of exposition.
Thm.
7
only characterizes
perfect confidence-calibration,
but it is possible to show a much more robust equivalence:
it turns out that a model is “close to”
B
B
-calibrated if and only if
it is “close to” locally-loss-optimal in the appropriate sense.
We state and prove this generalized version as
Thm.
25
in
App.
E
, where we also generalize to
allow any arbitrary proper-loss
ℓ
\ell
, and any notion of weighted-calibration
(including canonical calibration and confidence calibration).
3.3
Which Perturbations are Easy to Learn Autoregressively?
It remains to understand
when the perturbation class
𝒲
B
\mathcal{W}_{B}
is easy for an LLM to learn
(box
(B)
in
Fig.
4
).
Although we cannot currently fully answer this question, we can gain insight by studying a simpler question of representation:
when is a perturbation class
𝒲
B
\mathcal{W}_{B}
“easy” for the LLM to represent
(for example, as a small circuit on top of the original LLM)?
The main remaining challenge is that perturbations
are defined on probability distributions over
sequences
(
Definition
3
),
whereas autoregressive models must implement perturbations
token-by-token
.
Fortunately, for perturbations in
𝒲
B
\mathcal{W}_{B}
, it turns out
the perturbed next-token distribution can be expressed as a simple re-weighting of
the LLM’s original next-token distribution.
This re-weighting is governed by a set of scalar-valued functions
{
g
i
}
\{g_{i}\}
, defined below.
We call these functions “intermediate
B
B
-confidences”, because
g
i
​
(
z
≤
i
,
x
)
g_{i}(z_{\leq i};x)
is the probability mass the model places
on its most-likely
B
B
-class, given both the question
x
x
and the response prefix
z
≤
i
z_{\leq i}
generated so far.

Thus, the difficulty of representating the sequence-level perturbation reduces to the difficulty of representing these intermediate confidences values during generation.
Definition 9
(Intermediate
B
B
-Confidences)
.
For a given function
B
:
𝒱
∗
×
𝒱
N
→
[
K
]
B:\mathcal{V}^{*}\times\mathcal{V}^{N}\to[K]
and model
p
θ
p_{\theta}
,
we define the
intermediate
B
B
-confidences
as
the scalar-valued functions
{
g
i
}
i
∈
{
0
,
1
,
…
,
N
}
\{g_{i}\}_{i\in\{0,1,\dots,N\}}
:
g
i
(
z
≤
i
;
x
)
:=
Pr
z
∼
p
θ
(
⋅
∣
x
,
z
≤
i
)
[
B
x
(
z
)
=
k
∗
]
where
k
∗
←
argmax
k
∈
[
K
]
(
B
x
♯
p
x
)
[
k
]
.
\displaystyle g_{i}(z_{\leq i};x):=\Pr_{z\sim p_{\theta}(\cdot\mid x,z_{\leq i})}[B_{x}(z)=k^{*}]\penalty\ \penalty\ \mathrm{where}\penalty\ \penalty\ k^{*}\leftarrow\argmax_{k\in[K]}(B_{x}\sharp p_{x})[k].
We will informally say
that the LLM “knows” its intermediate
B
B
-confidences if
the functions
g
i
g_{i}
have a simple representation
(e.g. each
g
i
g_{i}
is computable by a small circuit on top of the LLM).
In that case, we show in
Thm.
10
that for any perturbation
w
∈
𝒲
B
w\in\mathcal{W}_{B}
,
the perturbed model
p
θ
⋆
w
p_{\theta}\star w
has an only-slightly-more-complex representation than the
original model
p
θ
p_{\theta}
.
Specifically, the perturbed model can be computed by composing a circuit
C
w
C_{w}
with the
functions
g
i
g_{i}
. Explicit formulas are provided in
Sec.
E.6
.
Theorem 10
.
For all functions
B
:
𝒱
∗
×
𝒱
N
→
[
K
]
B:\mathcal{V}^{*}\times\mathcal{V}^{N}\to[K]
and all perturbations
w
∈
𝒲
B
w\in\mathcal{W}_{B}
,
there exists a small circuit
6
6
6
Specifically, an arithmetic circuit of constant depth and
Θ
⁡
(
K
)
\Theta(K)
width.
C
w
C_{w}
such that for all models
p
θ
:
𝒱
∗
→
Δ
⁡
(
𝒱
N
)
p_{\theta}:\mathcal{V}^{*}\to\Delta(\mathcal{V}^{N})
,
all
x
∈
𝒱
∗
,
z
∈
𝒱
N
x\in\mathcal{V}^{*},z\in\mathcal{V}^{N}
, all
i
∈
[
N
]
i\in[N]
,
and with
p
x
:=
p
θ
(
⋅
∣
x
)
p_{x}:=p_{\theta}(\cdot\mid x)
,
w
x
:=
w
⁡
(
x
,
p
x
)
w_{x}:=w(x,p_{x})
,
the perturbed model
x
↦
p
x
⋆
w
x
x\mapsto p_{x}\star w_{x}
satisfies
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
∝
C
w
​
(
a
,
g
i
​
(
z
≤
i
,
x
)
,
g
0
​
(
x
)
)
\displaystyle(p_{x}\star w_{x})(z_{i}\mid z_{<i})\propto C_{w}(a,g_{i}(z_{\leq i};x),g_{0}(x))
(3.3)
where the constant of proportionality is independent of
z
i
z_{i}
,
a
:=
p
x
​
(
z
i
∣
z
<
i
)
a:=p_{x}(z_{i}\mid z_{<i})
is the original next-token probabilities, and
g
0
,
g
i
g_{0},g_{i}
are the intermediate
B
B
-confidences of
Definition
9
.
Putting all the theory together,
the message is: if the LLM “knows” its intermediate
B
B
-confidences,
then perturbations
𝒲
B
\mathcal{W}_{B}
are easy to implement,
and we should expect emergent
B
B
-calibration.
4
Experimental Predictions: When are LLMs calibrated?
Our main empirical question is:
Under what conditions and
for which functions
B
B
should we expect a pretrained LLM to be
B
B
-confidence-calibrated?
The theory of the previous section suggested an answer:
we should expect emergent
B
B
-confidence-calibration for a base LLM when
the LLM “knows” its intermediate
B
B
-confidences (
Definition
9
).
We simplify this (as discussed below) into an experimentally-testable heuristic:
for a given question
x
x
, does the LLM “know”
the distribution of of its answers post-processed by
B
B
(i.e.
B
x
​
♯
​
p
x
B_{x}\sharp p_{x}
)?
Practically, we operationalize this
by training a small LoRA on top of the base LLM to predict the
B
B
-class of the answer.
Claim 11
(Main, heuristic)
.
Let
(
x
,
y
)
∼
𝒟
(x,y)\sim\mathcal{D}
be a distribution on question-answer pairs,
let
B
:
𝒱
∗
×
𝒱
N
→
[
K
]
B:\mathcal{V}^{*}\times\mathcal{V}^{N}\to[K]
be a collapsing function,
and let
p
θ
​
(
z
∣
x
)
p_{\theta}(z\mid x)
be an autoregressive language model trained on
𝒟
\mathcal{D}
with cross-entropy loss.
Then,
p
θ
p_{\theta}
will be
B
B
-confidence-calibrated on
𝒟
\mathcal{D}
if the function
G
:
𝒱
∗
→
Δ
K
G:\mathcal{V}^{*}\to\Delta_{K}
defined as
G
:
x
↦
B
x
​
♯
​
p
x
is “easy to learn” for the LLM (e.g. with a LoRA adapter)
\displaystyle G:x\mapsto B_{x}\sharp p_{x}\quad\textrm{is ``easy to learn'' for the LLM (e.g. with a LoRA adapter)}
In words: the LLM should be able to accurately estimate
the distribution over semantic labels
B
x
​
(
z
)
B_{x}(z)
, under its own generative process,
given the question
x
x
.
Remark 12
.
Importantly,
Claim
11
does not require ground-truth labels to verify.
That is, although calibration is a property of the model
p
θ
p_{\theta}
and the joint distribution
(
x
,
y
)
(x,y)
,
we manage to predict calibration using only
p
θ
p_{\theta}
and the marginal distribution of
x
x
.
Remark 13
(Heuristic Simplifications)
.
Claim
11
involves two main simplifications of
Thm.
10
. Recall that
Thm.
10
considers the functions
{
g
i
}
\{g_{i}\}
of
Definition
9
, for all prefix lengths
i
∈
[
N
]
i\in[N]
.
First,
Claim
11
only considers the empty prefix (
i
=
0
i=0
)
i.e. the model’s
B
B
-class distribution given only the question.
Intuitively, the prediction from the empty prefix is likely the most challenging, and practically, this simplification means that only one simple-to-implement probe is required.
Second, instead of considering learnability of only the
B
B
-confidences
(
g
0
g_{0}
),
Claim
11
considers learnability of the entire
B
B
-class distribution
(
B
x
​
♯
​
p
x
B_{x}\sharp p_{x}
),
which can be estimated as a standard KL loss (see Appendix
D.3
).
Empirically, we did not find these simplifications to significantly affect the conclusions.
Finally, we specialize
Claim
11
to the practical case of semantic calibration—that is, we let
B
B
be a function that collapses long-form
answers into semantic equivalence classes, yielding the following:
Corollary 14
(Main, heuristic)
.
LLMs trained autoregressively with cross-entropy loss will be semantically calibrated
on in-distribution data if: the model “knows” its own output distribution
over semantic answers,
given only the question.
Corollary
14
leads to the following predictions, which we verify experimentally in
Sec.
5
.
Prediction 1: Semantic calibration emerges from standard pretraining.
When
B
B
is a semantic-collapsing function,
we expect it to be easy-to-learn in many settings:
Claim
11
only requires
that the LLM intuitively “knows” what types of semantic-answers
it is likely to output for a given question.
Thus, we
should
expect emergent semantic calibration
for a large class of pretrained LLMs, a remarkable fact not previously understood.
Prediction 2: RL post-training can break calibration.
We only
theoretically predict calibration in models trained autoregressively with cross-entropy loss, that is, standard pretraining or SFT. (Cross-entropy loss is required to connect calibration with local-loss-optimality in
Thm.
7
.) We have no reason to expect calibration in models trained in other ways, including Instruct models post-trained with RLHF, DPO, or RLVR – although our theory does not preclude it.
Prediction 3: Chain-of-thought reasoning (CoT) can break calibration.
To satisfy the conditions of our theory, the
model must “know” its own distribution over semantic answers,
even before generating the first token.
In hard CoT setting such as math problem-solving,
the model usually
does not
know what its final answer
will be until it has finished “thinking”.
Therefore, CoT is expected to break our mechanism for calibration.
Notably, what makes CoT powerful
(allowing the model to leverage more
compute to produce a better answer than it could have produced immediately)
is exactly what makes our mechanism of calibration fail.
Remark 15
.
These predictions are not entirely novel; some versions of them have been made in prior works,
with varying degrees of evidence.
Our contribution is providing a unified theoretical explanation of these phenomena,
and more conclusive experimental evidence.
5
Experiments
In this section, we experimentally test the predictions of our theory
on real models and datasets.
Full experimental details are in
App.
D
.
Datasets.
We focus on open-ended question-answer (QA) settings,
since calibration for multiple-choice QA is
already well-studied
(
Kadavath et al., 2022
;
Zhu et al., 2023
)
,
and a special case of our results.
We evaluate on four datasets:
(1) GSM8K
(
Cobbe et al., 2021
)
containing grade-school math word problems,
(2) OpenMathInstruct-2
(
Toshniwal et al., 2025
)
containing primarily
7
7
7
OpenMathInstruct-2 also contains
∼
\sim
16% of problems derived from GSM8K. We used OpenMathInstruct-2 as a large set of challenging math problems with a permissible license.
competition-level math problems
synthetically derived from MATH
(
Hendrycks et al., 2021
)
,
(3) TriviaQA
(
Joshi et al., 2017
)
containing trivia questions,
and (4) SimpleQA
(
Wei et al., 2024
)
containing factual questions
selected to be hard for GPT 3.5/4o.
Notably, the space of possible semantic answers is very large in all these settings.
Sampling and Evaluation.
All of our experiments include
5
5
-shot examples in the prompt.
We compare three different prompts, designed to elicit different styles
of responses from the model: “concise” (answer in a single word/phrase),
“sentence” (answer in a complete sentence), and “chain-of-thought (CoT)”.
The few-shot examples are formatted in the desired style
(e.g. for the “sentence” type, the few-shot examples have complete sentence answers).
For each question evaluated, we construct the appropriate
5
5
-shot prompt,
sample
M
=
50
M=50
responses from the LLM at temperature
1
1
,
and then apply the semantic collapsing function (described below) to each response.
To measure calibration error, we use the SmoothECE metric
8
8
8
We use a particular bandwidth choice; see
App.
D
for details.
(
Błasiok and Nakkiran, 2024
)
.
Semantic Collapsing.
We implement the semantic collapsing function
differently depending on the dataset type and response type.
Briefly, for math settings with “concise” and “chain-of-thought” prompt types,
we just extract the final answer from the generated string using regex matching,
and then perform basic string normalization. For other settings, we use
a strong LLM (Qwen3-14B-Instruct) to extract and cluster canonical answers
from long-form generations.
See
App.
D
for more details.
5.1
Experimental Results
We evaluate semantic calibration of Qwen, Gemini, Mistral, and Llama-family models,
of varying sizes from 0.5B to 72B,
for base and instruct variants, using each of the 3 response styles,
on all 4 question-answer datasets.
This yields over 650
evaluation experiments,
which we compile into
Fig.
2
by overlaying their reliability diagrams.
The box-plots in the bottom row of
Fig.
2
show the
distribution of calibration errors in aggregate for each dataset and configuration.
We will use this condensed figure to discuss our experimental predictions.
The full list of models is in
Sec.
D.4
and disaggregated results are
reported
in
App.
F
.
Prediction 1: Semantic calibration emerges from standard pretraining.
Our theory predicts that base models, in non-CoT settings, should be semantically calibrated.
The top row of
Fig.
2
shows reliability diagrams for all such models we evaluated
(configurations
base-concise
and
base-sentence
),
and we observe nearly all of these experiments are well-calibrated.
Notably, semantic calibration does not depend significantly on model size for base models:
even small models (
≤
\leq
1B) are remarkably calibrated;
see
App.
C
for a more in-depth look at this aspect.
Models are also well-calibrated regardless of the response style
(“sentence” vs. “concise”),
supporting our theory that semantic calibration depends not on
the specific phrasing of the answer,
but rather on whether the model “knows”
its semantic class distribution before starting to generate.
Prediction 2: Post-training can break calibration.
The middle row of
Fig.
2
includes reliability diagrams for instruct post-trained models,
for all three response types.
Many of these settings are miscalibrated, typically overconfident (i.e. a curve below the diagonal), as expected from a reward-maximizing RL objective.
Fig.
6
takes a closer look at the effect of different types of
instruction-tuning on calibration.
We compare three models from the same lineage:
a base model (Mistral-7B-v0.1),
a version of it post-trained via instruction supervised finetuning (SFT, zephyr-7b-sft-full)
(
Tunstall et al., 2023
)
,
and a version post-trained via both SFT and Direct Preference Optimization (DPO, zephyr-7b-dpo-full)
(
Rafailov et al., 2024
)
.
The DPO model (not trained with a proper loss) is significantly miscalibrated,
while the SFT-only model and the base model
(both trained with proper losses) are better calibrated.
Prediction 3: CoT reasoning can break calibration.
The middle row of
Fig.
2
shows CoT with both
base
and
instruct
models,
which are poorly calibrated in the math settings (GSM8K and OpenMathInstruct).
Base-cot
responses are underconfident
(above the diagonal),
while
instruct-cot
are underconfident for GSM8K, but overconfident for OpenMathInstruct,
see last row of
Fig.
7
.
Notably, this miscalibration is not inherent to math:
base models are calibrated
when asked to provide the answer immediately
(
base-concise
and
base-sentence
),
but become miscalibrated when allowed to reason (
base-cot
).
Remark 16
(Underconfidence of CoT)
.
The systematic underconfidence (rather than overconfidece)
of
base-cot
models
may seem surprising.
It is important to recall that our definitions of semantic confidence and accuracy
involve plurality vote.
For say GSM8K with CoT, the underconfidence manifests as follows:
when we sample multiple chain-of-thoughts for a given question,
the
plurality answer
is almost always correct, but it is a weak plurality.
Thus the semantic accuracy is nearly 100%, since the argmax answer is almost always right,
but the semantic confidence is significantly less than 100%.
Figure 5
:
Calibration error for three models based on Mistral-7B-v0.1:
pretrained-only,
instruction-supervised-finetuned,
and DPO-finetuned.
Here, “sentence” response style,
see
Fig.
8
for others.
Figure 6
:
Testing
Claim
11
across Qwen2.5 models and response styles.
Colors per
Fig.
2
.
Quantitative Learnability Probe.
Claim
11
suggests an explicit experiment
to predict when a base model will be
B
B
-confidence-calibrated for a given choice of
B
B
:
can the model “easily learn” the function
G
:
x
↦
B
x
​
♯
​
p
x
G:x\mapsto B_{x}\sharp p_{x}
mapping a question
x
x
to
the distribution over
the model’s own semantic answers for that question?
We can test this by training a small LoRA
(
Hu et al., 2022
)
on top of the model,
to directly generate the semantic class distribution
B
x
​
♯
​
p
x
B_{x}\sharp p_{x}
when prompted with the question
x
x
.
For example, in CoT settings, this would require the LoRA to “short-circuit”
the reasoning steps, and immediately generate the final answer that the model would have produced with CoT.
Notably, this does not require the model to produce the
correct
semantic answer,
but just match its own generative distribution.
In
Fig.
6
, we train rank-8 LoRAs on
Qwen2.5 base models of varying sizes (0.5B, 1.5B, 3B, 7B, 14B),
for all three response types on GSM8K.
We then compare each LoRA’s KL gap to optimality (x-axis) to the underlying model’s calibration error (y-axis).
The correlation agrees with our theory:
models which can easily predict their own semantic class distribution (low KL gap)
are also well-calibrated.
Full details in
Sec.
D.3
.
Figure 7
:
Effect of Scale:
We plot Calibration Error vs. Semantic Accuracy
for all models in
Fig.
2
;
each dot represents a separate model.
First row (predicted calibrated):
In the settings our theory applies,
we see no correlation between
the model capability (semantic accuracy) and the calibration error.
Second row (overconfident):
Configurations which we empirically observed to be mostly overconfident.
The dashed line illustrates the upper bound on the calibration error w.r.t. the accuracy, for a maximally overconfident predictor.
We see little correlation between semantic accuracy and the calibration error beyond what is dictated by the upper bound.
Third row (underconfident):
We see little correlation between calibration and accuracy,
except near the extreme when models approach perfect accuracy.
TriviaQA and SimpleQA plots are empty because
there are no underconfident configurations.
Fourth row:
The distribution of
average overconfidence
across models,
for each configuration;
positive/negative values indicate over–/underconfidence.
Model Scaling Effects.
Here, we aim to explore the effect of model scaling (parameter count, compute, data) on calibration.
Since information about training details are most often not publicly available, we use the model capability (measured with accuracy) as a proxy variable for model scale.
In
Fig.
7
, we plot calibration error (smECE) vs. semantic accuracy.
For base models without chain-of-thought (first row), we see no correlation
between model capability (semantic accuracy) and calibration error.
This is consistent with our theoretical predictions,
which have no explicit dependency on model scale or capability.
It is worth noting that prior works have observed that calibration of base models can improve with model scale for other notion of calibration:
next-token prediction in multiple-choice question setups
(
Kadavath et al., 2022
;
Zhu et al., 2023
;
Plaut et al., 2025
)
.
We do not find such improvements for semantic calibration of
base models
.
For instruct models and base models with chain-of-thought,
we empirically observe that some configurations are overconfident, while other underconfident,
and we divide those configurations into separate rows in
Fig.
7
.
The dashed line illustrates the upper bound on the calibration error w.r.t. the accuracy for an overconfident configurations,
which is dictated by the behavior of a maximally-overconfident predictor that puts its entire probability mass on a single choice.
For the overconfident configurations,
we see little correlation between calibration error and accuracy beyond what is dictated by the upper bound.
For the underconfident configurations,
we see also little correlation overall,
except for in the high-accuracy regime:
calibration error tends to decrease
when models approach perfect semantic accuracy
9
9
9
Notably, this is not mathematically necessary.
Since semantic accuracy involves only the
argmax
-probability class,
it is possible for a predictor to be perfectly semantically-accurate
while having high calibration error.
.
However, it is not clear whether this is a robust phenomenon.
5.2
Discussion: Calibration in LLMs vs other deep networks
One may wonder why the state of calibration in LLMs seems significantly
different from calibration in non-LLM deep networks (e.g. image classifiers).
Specifically, deep network classifiers are sometimes severely overconfident,
and sometimes well-calibrated,
depending on the specific network (e.g.
Guo et al. (2017)
vs.
Minderer et al. (2021)
).
On the other hand, all base LLMs we tested were well-calibrated
(in non-CoT settings) — there was no significant calibration difference between models.
This difference between LLMs and classifiers is due to
differences in training practices:
when training LLMs, practitioners monitor the test/validation loss closely,
and stop training before the test loss overfits (increases).
On the other hand, when training classifiers,
practitioners care about the test
classification error
,
and often continue training even as test
loss
increases.
Most trained LLMs are therefore locally-loss-optimal w.r.t. test loss (and thus calibrated),
but trained classifiers might have high test loss (and thus be miscalibrated).
This perspective on the calibration of deep networks was articulated in Section 1.1 of
Błasiok et al. (2023b)
.
6
Conclusion
We find that base LLMs,
despite being trained with a
token-level syntactic
objective,
are remarkably calibrated
with respect to the
sequence-level semantics
of their generations.
Our central contribution is a principled mechanism behind this emergence,
building on recent theoretical connections between calibration and loss-optimality
(
Błasiok et al., 2023b
;
Błasiok et al., 2024
)
.
This theory provides a unified lens through which to understand
the nuanced calibration behavior of models in practice,
distinguishing settings which are calibrated from
those which are not.
More generally, our work can be seen as a step towards
understanding the structure of LLMs’ output distribution:
B
B
-calibration is one formal way of quantifying how close the LLM’s
distribution is to the ground-truth pretraining distribution.
For the interested reader,
we have an extended discussion and technical remarks
in
App.
B
.
6.1
Limitations
Types of Calibration.
One limitation of our paper is that we focus on a very specific
type of calibration, which is essentially a sampling-based notion
(
B
B
-confidence-calibration).
It is possible that other types of calibration (e.g. verbalized calibration
(
Tian et al., 2023
;
Mielke et al., 2022
)
)
also emerge for certain types of LLM training; we consider this possibility interesting
but out-of-scope for the current work.
Practical Implications.
Our work is primarily scientifically motivated,
and so we do not fully explore practical considerations or implications.
For example, we do not consider the computational efficiency of our confidence measurements.
This is a limitation to using such measures in practice,
since computing semantic confidence requires sampling an LLM
multiple times for the same question.
We consider translating our scientific results into
real-world improvements to be an important direction for future work.
Datasets.
Although we evaluate on a variety of different models,
we only evaluate on 4 selected datasets.
We chose these datasets to cover a diversity of domains and problem difficulties,
from questions about world-knowledge to mathematical reasoning problems.
Further, we chose datasets with
open-ended
answers,
since calibration of multiple-choice datasets is already extensively studied
(
Kadavath et al., 2022
;
Zhu et al., 2023
)
.
Although we do not expect our results to depend significantly
on the choice of dataset, it is possible that certain other datasets
have different calibration behavior; this is a limitation of our experiments.
Remark 17
.
Notably, there are some datasets which
we would expect to behave differently,
such as TruthfulQA
(
Lin et al., 2022b
)
,
which is a dataset containing common human misconceptions.
This dataset fails to satisfy the “in-distribution” requirement
of our results (e.g.
Corollary
14
and Footnote
4
),
and so it is consistent with our theory for models to be miscalibrated.
Theory Formalism.
There remain several steps in our conjectured mechanism (Fig
4
)
lacking formal definitions and proofs.
It is an open question to formalize these in meaningful and tractable ways.
Acknowledgments
We are grateful for discussion and feedback from
Parikshit Gopalan,
Eran Malach,
Aravind Gollakota,
Omid Saremi,
Madhu Advani,
Etai Littwin,
Josh Susskind,
and
Russ Webb.
†
†
Apple and the Apple logo are trademarks of Apple Inc., registered in the U.S. and other countries and regions.
References
Abdin
et al.
(2024)
M. Abdin, J. Aneja, H. Behl, S. Bubeck, R. Eldan, S. Gunasekar, M. Harrison, R. J. Hewett, M. Javaheripi, P. Kauffmann,
et al.
Phi-4 technical report
.
arXiv preprint arXiv:2412.08905
.
Cited by:
Table 3
.
Angelopoulos
et al.
(2023)
A. N. Angelopoulos S. Bates
et al.
Conformal prediction: a gentle introduction
.
Foundations and trends® in machine learning
16
(
4
),
pp. 494–591
.
Cited by:
§E.9
.
Band
et al.
(2024)
N. Band, X. Li, T. Ma, and T. Hashimoto
Linguistic calibration of long-form generations
.
External Links:
2404.00474
Cited by:
§1
.
Beck and Teboulle (2003)
A. Beck and M. Teboulle
Mirror descent and nonlinear projected subgradient methods for convex optimization
.
Operations Research Letters
31
(
3
),
pp. 167–175
.
Cited by:
§E.8.1
.
Błasiok
et al.
(2024)
J. Błasiok, P. Gopalan, L. Hu, A. T. Kalai, and P. Nakkiran
Loss minimization yields multicalibration for large neural networks
.
In
Innovations in Theoretical Computer Science Conference
,
Vol.
287
,
pp. 17–1
.
Cited by:
§1
,
§3.1
,
§3
,
§6
.
Błasiok
et al.
(2023a)
J. Błasiok, P. Gopalan, L. Hu, and P. Nakkiran
A unifying theory of distance from calibration
.
In
ACM Symposium on Theory of Computing
,
pp. 1727–1740
.
Cited by:
§D.1
.
Błasiok
et al.
(2023b)
J. Błasiok, P. Gopalan, L. Hu, and P. Nakkiran
When does optimizing a proper loss yield calibration?
.
In
Advances in Neural Information Processing Systems
,
Cited by:
§E.8
,
§1
,
§3.1
,
§3
,
§5.2
,
§6
.
Błasiok and Nakkiran (2024)
J. Błasiok and P. Nakkiran
Smooth ECE: principled reliability diagrams via kernel smoothing
.
In
International Conference on Learning Representations
,
Cited by:
Appendix D
,
§D.1
,
§D.1
,
§D.2
,
§5
.
Cobbe
et al.
(2021)
K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and J. Schulman
Training verifiers to solve math word problems
.
arXiv preprint arXiv:2110.14168
.
Cited by:
Appendix D
,
§5
.
Cover and Thomas (1999)
T. M. Cover and J. A. Thomas
Elements of information theory
.
John Wiley & Sons
.
Cited by:
§3.2
.
Desai and Durrett (2020)
S. Desai and G. Durrett
Calibration of pre-trained transformers
.
In
Empirical Methods in Natural Language Processing
,
pp. 295–302
.
Cited by:
§1
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
Appendix A
,
§1
,
footnote 11
,
footnote 2
.
Gemma Team
et al.
(2025)
T. Gemma Team, A. Kamath, J. Ferret, S. Pathak, N. Vieillard, R. Merhej, S. Perrin, T. Matejovicova, A. Ramé, M. Rivière,
et al.
Gemma 3 technical report
.
arXiv preprint arXiv:2503.19786
.
Cited by:
Table 2
,
Table 3
.
Gemma Team
et al.
(2024)
T. Gemma Team, M. Riviere, S. Pathak, P. G. Sessa, C. Hardin, S. Bhupatiraju, L. Hussenot, T. Mesnard, B. Shahriari, A. Ramé,
et al.
Gemma 2: improving open language models at a practical size
.
arXiv preprint arXiv:2408.00118
.
Cited by:
Table 2
,
Table 3
.
Gneiting and Raftery (2007)
T. Gneiting and A. E. Raftery
Strictly proper scoring rules, prediction, and estimation
.
Journal of the American statistical Association
102
(
477
),
pp. 359–378
.
Cited by:
§E.8
.
Gopalan
et al.
(2024)
P. Gopalan, L. Hu, and G. N. Rothblum
On computationally efficient multi-class calibration
.
In
Conference on Learning Theory
,
pp. 1983–2026
.
Cited by:
§B.1
,
§E.2
,
§E.9
,
§1
,
§2.2
,
§3.2
,
Definition 23
,
Lemma 45
,
footnote 10
.
Grattafiori
et al.
(2024)
A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan,
et al.
The llama 3 herd of models
.
arXiv preprint arXiv:2407.21783
.
Cited by:
Table 2
,
Table 3
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
International Conference on Machine Learning
,
pp. 1321–1330
.
Cited by:
§5.2
.
Hébert-Johnson
et al.
(2018)
U. Hébert-Johnson, M. Kim, O. Reingold, and G. Rothblum
Multicalibration: calibration for the (computationally-identifiable) masses
.
In
International Conference on Machine Learning
,
pp. 1939–1948
.
Cited by:
Remark 20
,
Remark 24
.
Hendrycks
et al.
(2021)
D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
Measuring mathematical problem solving with the math dataset
.
arXiv preprint arXiv:2103.03874
.
Cited by:
§5
.
Hou
et al.
(2024)
B. Hou, Y. Liu, K. Qian, J. Andreas, S. Chang, and Y. Zhang
Decomposing uncertainty for large language models through input clarification ensembling
.
In
International Conference on Machine Learning
,
Cited by:
Appendix A
.
Hu
et al.
(2022)
E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen,
et al.
Lora: low-rank adaptation of large language models.
.
In
International Conference on Learning Representations
,
Cited by:
§D.3
,
§5.1
.
Jiang
et al.
(2023a)
A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford, D. S. Chaplot, D. de Las Casas, F. Bressand, G. Lengyel, G. Lample, L. Saulnier, L. R. Lavaud, M. Lachaux, P. Stock, T. L. Scao, T. Lavril, T. Wang, T. Lacroix, and W. E. Sayed
Mistral 7b
.
arXiv preprint arXiv:2310.06825
.
Cited by:
Table 2
,
Table 3
.
Jiang
et al.
(2023b)
M. Jiang, Y. Ruan, S. Huang, S. Liao, S. Pitis, R. B. Grosse, and J. Ba
Calibrating language models via augmented prompt ensembles
.
In
International Conference on Machine Learning Workshop on Deployable Generative AI
,
Cited by:
Appendix A
.
Joshi
et al.
(2017)
M. Joshi, E. Choi, D. Weld, and L. Zettlemoyer
TriviaQA: a large scale distantly supervised challenge dataset for reading comprehension
.
In
Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 1601–1611
.
External Links:
Document
Cited by:
Appendix D
,
§5
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
Appendix A
,
Appendix D
,
§D.3
,
§1
,
§1
,
§1
,
§5
,
§5.1
,
§6.1
.
Kapoor
et al.
(2024)
S. Kapoor, N. Gruver, M. Roberts, K. Collins, A. Pal, U. Bhatt, A. Weller, S. Dooley, M. Goldblum, and A. G. Wilson
Large language models must be taught to know what they don’t know
.
In
Advances in Neural Information Processing Systems
,
Cited by:
§1
.
Krakauer
et al.
(2025)
D. C. Krakauer, J. W. Krakauer, and M. Mitchell
Large language models and emergence: a complex systems perspective
.
arXiv preprint arXiv:2506.11135
.
Cited by:
footnote 1
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
International Conference on Learning Representations
,
Cited by:
Appendix D
.
Kwon
et al.
(2023)
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. Gonzalez, H. Zhang, and I. Stoica
Efficient memory management for large language model serving with pagedattention
.
In
Symposium on Operating Systems Principles
,
pp. 611–626
.
Cited by:
Appendix D
.
Lamb
et al.
(2025)
T. A. Lamb, D. R. Ivanova, P. Torr, and T. G. Rudner
Semantic-level confidence calibration of language models via temperature scaling
.
In
ICLR Workshop: Quantify Uncertainty and Hallucination in Foundation Models: The Next Frontier in Reliable AI
,
Cited by:
Appendix A
,
§2
,
footnote 2
.
Leng
et al.
(2025)
J. Leng, C. Huang, B. Zhu, and J. Huang
Taming overconfidence in llms: reward calibration in rlhf
.
In
International Conference on Learning Representations
,
Cited by:
Appendix A
,
§1
.
Lewkowycz
et al.
(2022)
A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone, C. Anil, I. Schlag, T. Gutman-Solo,
et al.
Solving quantitative reasoning problems with language models
.
Advances in Neural Information Processing Systems
35
,
pp. 3843–3857
.
Cited by:
Appendix D
.
Lhoest
et al.
(2021)
Q. Lhoest, A. V. Del Moral, Y. Jernite, A. Thakur, P. Von Platen, S. Patil, J. Chaumond, M. Drame, J. Plu, L. Tunstall,
et al.
Datasets: a community library for natural language processing
.
arXiv preprint arXiv:2109.02846
.
Cited by:
Appendix D
.
Li
et al.
(2025)
Y. Li, D. Rügamer, B. Bischl, and M. Rezaei
Calibrating llms with information-theoretic evidential deep learning
.
In
International Conference on Learning Representations
,
Cited by:
Appendix A
.
Lin
et al.
(2022a)
S. Lin, J. Hilton, and O. Evans
Teaching models to express their uncertainty in words
.
Transactions on Machine Learning Research
.
External Links:
ISSN 2835-8856
Cited by:
Appendix A
.
Lin
et al.
(2022b)
S. Lin, J. Hilton, and O. Evans
TruthfulQA: measuring how models mimic human falsehoods
.
In
Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 3214–3252
.
Cited by:
Remark 17
.
Mei
et al.
(2025)
Z. Mei, C. Zhang, T. Yin, J. Lidard, O. Shorinwa, and A. Majumdar
Reasoning about uncertainty: do reasoning models know when they don’t know?
.
arXiv preprint arXiv:2506.18183
.
Cited by:
§1
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
Document
Cited by:
Appendix A
,
§6.1
.
Minderer
et al.
(2021)
M. Minderer, J. Djolonga, R. Romijnders, F. Hubis, X. Zhai, N. Houlsby, D. Tran, and M. Lucic
Revisiting the calibration of modern neural networks
.
Advances in neural information processing systems
34
,
pp. 15682–15694
.
Cited by:
§5.2
.
Mistral AI Team (2023)
Mistral AI Team
Mixtral of experts
.
Note:
https://mistral.ai/news/mixtral-of-experts
Accessed: 2025-09-22
Cited by:
Table 2
.
Mistral AI Team (2024a)
Mistral AI Team
Ministraux: a structural and semantic evolution for ministral
.
Note:
https://mistral.ai/news/ministraux
Accessed: 2025-09-22
Cited by:
Table 3
.
Mistral AI Team (2024b)
Mistral AI Team
Mistral small 3.1: efficient, powerful, and affordable
.
Note:
https://mistral.ai/news/mistral-small-3-1
Accessed: 2025-09-22
Cited by:
Table 2
,
Table 3
.
Nakkiran and Bansal (2020)
P. Nakkiran and Y. Bansal
Distributional generalization: a new kind of generalization
.
arXiv preprint arXiv:2009.08092
.
Cited by:
Remark 18
.
Nesterov (2005)
Y. Nesterov
Smooth minimization of non-smooth functions
.
Mathematical Programming
103
(
1
),
pp. 127–152
.
Cited by:
§E.8.1
.
Nous Research (2024a)
Nous Research
Nous-hermes-2-mixtral-8x7b-dpo
.
Note:
https://huggingface.co/NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO
Hugging Face Model Repository. Accessed: 2025-09-22
Cited by:
Table 3
.
Nous Research (2024b)
Nous Research
Nous-hermes-2-mixtral-8x7b-sft
.
Note:
https://huggingface.co/NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT
Hugging Face Model Repository. Accessed: 2025-09-22
Cited by:
Table 3
.
OpenAI (2023)
OpenAI
Gpt-4 technical report
.
arXiv preprint arXiv:2303.08774
.
Cited by:
Appendix A
,
§1
,
§1
.
Plaut
et al.
(2025)
B. Plaut, K. X. Nguyen, and T. Trinh
Probabilities of chat LLMs are miscalibrated but still predict correctness on multiple-choice q&a
.
Transactions on Machine Learning Research
.
External Links:
ISSN 2835-8856
Cited by:
§1
,
§5.1
.
Rafailov
et al.
(2024)
R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and C. Finn
Direct preference optimization: your language model is secretly a reward model
.
External Links:
2305.18290
Cited by:
§5.1
.
Savage (1971)
L. J. Savage
Elicitation of personal probabilities and expectations
.
Journal of the American Statistical Association
66
(
336
),
pp. 783–801
.
Cited by:
§E.8
.
Schervish (1989)
M. J. Schervish
A general method for comparing probability assessors
.
The Annals of Statistics
17
(
4
),
pp. 1856–1879
.
Cited by:
§E.8
.
Shen
et al.
(2024)
M. Shen, S. Das, K. Greenewald, P. Sattigeri, G. W. Wornell, and S. Ghosh
Thermometer: towards universal calibration for large language models
.
In
International Conference on Machine Learning
,
pp. 44687–44711
.
Cited by:
Appendix A
.
Tian
et al.
(2023)
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. Manning
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
Empirical Methods in Natural Language Processing
,
pp. 5433–5442
.
External Links:
Document
Cited by:
§1
,
§6.1
.
Tibshirani (2023)
R. Tibshirani
Conformal prediction
.
Technical report
UC Berkeley
.
External Links:
Link
Cited by:
§E.9
.
Toshniwal
et al.
(2025)
S. Toshniwal, W. Du, I. Moshkov, B. Kisacanin, A. Ayrapetyan, and I. Gitman
Openmathinstruct-2: accelerating ai for math with massive open-source instruction data
.
In
International Conference on Learning Representations
,
Cited by:
Appendix D
,
§5
.
Tunstall
et al.
(2023)
L. Tunstall, E. Beeching, N. Lambert, N. Rajani, K. Rasul, Y. Belkada, S. Huang, L. Von Werra, C. Fourrier, N. Habib,
et al.
Zephyr: direct distillation of lm alignment
.
arXiv preprint arXiv:2310.16944
.
Cited by:
Table 3
,
§5.1
.
Ulmer
et al.
(2024)
D. Ulmer, M. Gubri, H. Lee, S. Yun, and S. Oh
Calibrating large language models using their generations only
.
In
Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 15440–15459
.
External Links:
Document
Cited by:
Appendix A
.
Vashurin
et al.
(2025)
R. Vashurin, E. Fadeeva, A. Vazhentsev, L. Rvanova, D. Vasilev, A. Tsvigun, S. Petrakov, R. Xing, A. Sadallah, K. Grishchenkov, A. Panchenko, T. Baldwin, P. Nakov, M. Panov, and A. Shelmanov
Benchmarking uncertainty quantification methods for large language models with LM-polygraph
.
Transactions of the Association for Computational Linguistics
13
,
pp. 220–248
.
External Links:
Document
Cited by:
§1
.
von Werra
et al.
(2020)
L. von Werra, Y. Belkada, L. Tunstall, E. Beeching, T. Thrush, N. Lambert, S. Huang, K. Rasul, and Q. Gallouédec
TRL: transformer reinforcement learning
.
GitHub
.
Note:
https://github.com/huggingface/trl
Cited by:
§D.3
.
Wang
et al.
(2023)
X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou
Self-consistency improves chain of thought reasoning in language models
.
In
International Conference on Learning Representations
,
Cited by:
Appendix A
,
footnote 2
.
Wang
et al.
(2025)
Z. Wang, Z. Shi, H. Zhou, S. Gao, Q. Sun, and J. Li
Towards objective fine-tuning: how LLMs’ prior knowledge causes potential poor calibration?
.
In
Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 14830–14853
.
External Links:
Document
,
ISBN 979-8-89176-251-0
Cited by:
Appendix A
,
§1
.
Wei
et al.
(2024)
J. Wei, N. Karina, H. W. Chung, Y. J. Jiao, S. Papay, A. Glaese, J. Schulman, and W. Fedus
Measuring short-form factuality in large language models
.
In
Advances in Neural Information Processing Systems
,
Cited by:
Appendix A
,
Appendix D
,
§5
,
footnote 2
.
Wei
et al.
(2022)
J. Wei, Y. Tay, R. Bommasani, C. Raffel, B. Zoph, S. Borgeaud, D. Yogatama, M. Bosma, D. Zhou, D. Metzler, E. H. Chi, T. Hashimoto, O. Vinyals, P. Liang, J. Dean, and W. Fedus
Emergent abilities of large language models
.
Transactions on Machine Learning Research
.
External Links:
ISSN 2835-8856
Cited by:
footnote 1
.
Wolf
et al.
(2019)
T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi, P. Cistac, T. Rault, R. Louf, M. Funtowicz,
et al.
Huggingface’s transformers: state-of-the-art natural language processing
.
arXiv preprint arXiv:1910.03771
.
Cited by:
Appendix D
.
Xiao
et al.
(2025)
J. Xiao, B. Hou, Z. Wang, R. Jin, Q. Long, W. J. Su, and L. Shen
Restoring calibration for aligned large language models: a calibration-aware fine-tuning approach
.
In
International Conference on Machine Learning
,
Cited by:
Appendix A
,
§1
.
Xie
et al.
(2024)
J. Xie, A. S. Chen, Y. Lee, E. Mitchell, and C. Finn
Calibrating language models with adaptive temperature scaling
.
In
Empirical Methods in Natural Language Processing
,
pp. 18128–18138
.
External Links:
Document
Cited by:
Appendix A
.
Yang
et al.
(2024a)
A. X. Yang, M. Robeyns, X. Wang, and L. Aitchison
Bayesian low-rank adaptation for large language models
.
In
International Conference on Learning Representations
,
Cited by:
Appendix A
.
Yang
et al.
(2025)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv,
et al.
Qwen3 technical report
.
arXiv preprint arXiv:2505.09388
.
Cited by:
Table 2
,
Table 3
.
Yang
et al.
(2024b)
A. Yang, B. Zhang, B. Hui, B. Gao, B. Yu, C. Li, D. Liu, J. Tu, J. Zhou, J. Lin,
et al.
Qwen2.5-math technical report: toward mathematical expert model via self-improvement
.
arXiv preprint arXiv:2409.12122
.
Cited by:
Table 2
,
Table 3
.
Yang
et al.
(2024c)
Q. A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, G. Dong, H. Wei, H. Lin, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Lin, K. Dang, K. Lu, K. Bao, K. Yang, L. Yu, M. Li, M. Xue, P. Zhang, Q. Zhu, R. Men, R. Lin, T. Li, T. Xia, X. Ren, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Wan, Y. Liu, Z. Cui, Z. Zhang, Z. Qiu, S. Quan, and Z. Wang
Qwen2.5 technical report
.
arXiv preprint arXiv:2412.15115
.
Cited by:
Table 2
,
Table 3
.
Yin
et al.
(2023)
Z. Yin, Q. Sun, Q. Guo, J. Wu, X. Qiu, and X. Huang
Do large language models know what they don’t know?
.
In
Findings of the Association for Computational Linguistics: ACL 2023
,
pp. 8653–8665
.
Cited by:
§1
.
Yoon
et al.
(2025)
D. Yoon, S. Kim, S. Yang, S. Kim, S. Kim, Y. Kim, E. Choi, Y. Kim, and M. Seo
Reasoning models better express their confidence
.
arXiv preprint arXiv:2505.14489
.
Cited by:
§1
.
Zhai
et al.
(2025)
S. Zhai, R. Zhang, P. Nakkiran, D. Berthelot, J. Gu, H. Zheng, T. Chen, M. Á. Bautista, N. Jaitly, and J. M. Susskind
Normalizing flows are capable generative models
.
In
International Conference on Machine Learning
,
Cited by:
§B.1
.
Zhang
et al.
(2024)
H. Zhang, Y. Zhang, Y. Yu, D. Madeka, D. Foster, E. Xing, H. Lakkaraju, and S. Kakade
A study on the calibration of in-context learning
.
In
Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
,
pp. 6118–6136
.
External Links:
Document
Cited by:
Appendix A
,
§1
,
§1
,
Remark 19
.
Zhu
et al.
(2023)
C. Zhu, B. Xu, Q. Wang, Y. Zhang, and Z. Mao
On the calibration of large language models and alignment
.
In
Findings of the Association for Computational Linguistics: EMNLP
,
pp. 9778–9795
.
External Links:
Document
Cited by:
Appendix D
,
§5
,
§5.1
,
§6.1
.
Appendix Contents
Appendix A
Additional Related Works
Recalibration Methods.
A number of prior works study methods to improve the calibration of LLMs, ranging from temperature-scaling at inference-time
(
Xie et al., 2024
;
Shen et al., 2024
, e.g.,)
to training calibration-specific probes that predict correctness
(
Mielke et al., 2022
)
or training with calibration-improving regularization terms
(
Wang et al., 2025
)
. Other approaches attempt to cluster questions and predict per-cluster accuracy
(
Lin et al., 2022a
;
Ulmer et al., 2024
)
, or make use of the fact that ensembling models tends to improve calibration
(
Jiang et al., 2023b
;
Hou et al., 2024
)
. Probabilistic approaches (such as Bayesian deep learning, or evidential deep learning) have been found to often yield better calibration
(
Li et al., 2025
;
Yang et al., 2024a
, e.g.,)
.
Sampling-based Confidences.
A number of prior works have proposed sampling-based approaches to defining LLM uncertainty.
Both
Wang et al. (2023)
and
Wei et al. (2024)
sample multiple answers per-question, and define confidence
as the frequency of the most-common answer.
Wei et al. (2024)
additionally groups answers together by string-matching,
which allows for some degree of semantic equivalence.
This approach was extended and popularized by
the notion of
semantic entropy
(
Farquhar et al., 2024
)
.
Semantic entropy clusters sampled answers together
by semantic content, and then measures the empirical entropy of clustered answers.
Recently,
Lamb et al. (2025)
define Empirical Semantic Confidence,
which is essentially an empirical version of our notion of semantic confidence.
Note that one distinguishing aspect of our formalism is,
we parameterize the notion of calibration by the choice of collapsing function
B
B
.
This allows us to develop somewhat more general theoretical insights,
which are not tied to a fixed notion of semantics.
Factors which Harm LLM Calibration.
Various factors have been observed in prior work to harm LLM calibration.
It is well-known that RLHF often harms calibration in multiple-choice QA settings
(
Kadavath et al., 2022
;
OpenAI, 2023
)
.
Other RL post-training methods such as DPO have also been observed to harm calibration
(
Leng et al., 2025
;
Xiao et al., 2025
)
.
Some studies have also found chain-of-thought responses to harm calibration,
agreeing with our results
(
Zhang et al., 2024
)
.
However, we warn that not all of these works use the same notion of confidence and calibration as we do,
and so are not directly comparable.
Appendix B
Extended Discussion and Remarks
B.1
Potential Extensions
The theoretical framework described here is fairly general, and extends beyond the
setting of confidence-calibration in LLMs.
Briefly, since most of our theory
is stated in the language of
weighted calibration
(
Gopalan et al., 2024
)
,
it applies
to any property that can be written as weighted calibration.
This includes slightly stronger notions of calibration,
such as top-label calibration,
and also includes conformal-prediction type of guarantees (more details in
Sec.
E.9.1
.
See
Gopalan et al. (2024)
for a number of properties which can be expressed
as weighted calibration, and
Sec.
E.9
for the connection to conformal prediction.
Our general theoretical results appear in
App.
E
.
Intuitively, the high-level message of our results is that if a model is trained
with a max-likelihood / log-loss objective, then we should expect it to
satisfy weighted calibration
for a “simple” family of weight functions.
The appropriate notion of simplicity depends on the model architecture;
simple weight functions should roughly correspond to easy-to-learn perturbations
to the model’s output distribution.
At this level of generality, we expect some version of our results to apply
even for real-valued density models, such as continuous normalizing flows
(e.g.
Zhai et al. (2025)
), which are also trained with
the log-likelihood objective. That is, we should expect such normalizing flows
to also exhibit certain (weak) types of calibration.
We believe this is a promising avenue for future work.
Remark 18
.
This high-level message can be interpreted as
“models should match the true distribution with respect to all
easy-to-learn features.”
Interestingly, a very similar statement was conjectured for
interpolating
classifiers in
Nakkiran and Bansal (2020)
,
called “Feature Calibration.”
The exact relation to our present work is unclear.
B.2
Technical Remarks
We collect several technical remarks regarding the theory of
Sec.
3
.
Remark 19
(The Distribution)
.
One detail of the theory worth discussing further is the role of the
distribution
𝒟
\mathcal{D}
.
Technically, our theory only implies calibration if the base model
has been trained on the exact same distribution on which calibration is evaluated.
This is obviously not strictly true (e.g. models are not pretrained only on GSM8K).
However, we may imagine modern pretrained models to behave “as if”
they were trained on the evaluation distributions, since the pretraining distribution
is large and diverse.
Notably, this reasoning requires the evaluation dataset and
prompt choice to be reasonably in-distribution for the pretraining
(see
Zhang et al. (2024)
for settings where the
prompting scheme affects calibration).
We discuss a more formal way to think about the choice of distribution in
Remark
20
below.
Remark 20
(Multicalibration)
.
For clarity of exposition, we described the theory as if there is only one
distribution
𝒟
\mathcal{D}
of interest, but in reality, we evaluate calibration across
multiple distributions (TriviaQA, GSM8K, etc),
and we pretrain on yet another distribution.
Moreover, we find that a single model can be
simultaneously calibrated across many evaluation distributions.
We touched upon this issue in Footnote
4
,
but there is a theoretically cleaner (though more involved)
way to think about multiple distributions, which we outline now.
Formally, requiring
B
B
-calibration across multiple distributions simultaneously
can be thought of as a
multi-calibration
property
(
Hébert-Johnson et al., 2018
)
.
Suppose for example that the pretraining distribution
𝒟
\mathcal{D}
is some mixture of disjoint sub-distributions:
𝒟
=
α
1
​
D
1
+
α
2
​
D
2
+
…
\mathcal{D}=\alpha_{1}D_{1}+\alpha_{2}D_{2}+\dots
.
Suppose we are interested in
B
B
-calibration simultaneously for distributions
D
1
D_{1}
and
D
2
D_{2}
.
Then, it is possible to show a generalization of
Thm.
7
:
A model is
B
B
-confidence-calibrated across both
D
1
D_{1}
and
D
2
D_{2}
if and only if it is locally-loss-optimal on
𝒟
\mathcal{D}
w.r.t.
an expanded class of perturbations
𝒲
B
∗
\mathcal{W}_{B}^{*}
.
Informally, the class of perturbations
𝒲
B
∗
\mathcal{W}_{B}^{*}
is essentially
the usual class
𝒲
B
\mathcal{W}_{B}
(of
Definition
6
)
augmented by indicator functions
𝟙
{
x
∈
𝒟
1
}
,
1
{
x
∈
𝒟
2
}
\mathbbm{1}\{x\in\mathcal{D}_{1}\},\penalty\ \mathbbm{1}\{x\in\mathcal{D}_{2}\}
for membership in each sub-distribution.
We will not get into the technical details,
but using this version of
Thm.
7
,
it is possible to carry out the remaining steps
of the argument from
Sec.
3
and
Fig.
4
.
Applying the same heuristics, for example, we would conclude:
an LLM will be simultaneously
B
B
-confidence-calibrated
on distributions
𝒟
1
,
𝒟
2
\mathcal{D}_{1},\mathcal{D}_{2}
if
it is easy for the LLM to
(1) estimate its own distribution on
B
B
-classes
and (2) identify samples as either
x
∈
𝒟
1
x\in\mathcal{D}_{1}
or
x
∈
𝒟
2
x\in\mathcal{D}_{2}
.
The second condition is likely to be satisfied in all our experiments,
since all our evaluation datasets are distinct and easy to identify.
Thus, the predictions of our theory remain unchanged,
justifying our choice to avoid discussing multicalibration in the main body.
Remark 21
(Full calibration)
.
At first glance, it may seem that a
minor generalization of our mechanism (
Fig.
4
)
would also imply
full
B
B
-calibration (i.e., canonical calibration of the
B
B
-induced classifier),
rather than just
confidence
-calibration.
After all,
Thm.
7
formally generalizes to
arbitrary weight families
𝒲
\mathcal{W}
(see
Thm.
25
),
including the family corresponding to full
B
B
-calibration
(defined as
𝒲
B
(
full
)
\mathcal{W}_{B}^{\rm{(full)}}
in
Definition
35
).
However, full
B
B
-calibration is too strong a property to hold in general
10
10
10
For example, when
K
K
(the number of
B
B
-classes) is large, full
B
B
-calibration
would be computationally intractable to even estimate
(
Gopalan et al., 2024
)
.
.
So, which part of our argument in
Fig.
4
breaks for full calibration?
The culprit is the step (B)
⟹
\implies
(C).
The weight family
𝒲
B
(
full
)
\mathcal{W}_{B}^{\rm{(full)}}
relevant for full calibration is, roughly speaking, “too large”
for this step to hold.
To better understand why the heuristic fails, here is
more general version of the (B)
⟹
\implies
(C) step in
Fig.
4
,
which we believe is plausible for arbitrary weight families
𝒲
\mathcal{W}
.
Claim 22
(assumption, informal)
.
If a perturbation family
𝒲
\mathcal{W}
is easy-to-learn for a pretrained LLM, meaning:
for all perturbations
w
∈
𝒲
w\in\mathcal{W}
,
the LLM
p
θ
:
𝒱
∗
→
Δ
⁡
(
𝒱
N
)
p_{\theta}:\mathcal{V}^{*}\to\Delta(\mathcal{V}^{N})
can be easily LoRA-fine-tuned to
match the distribution of a perturbed-model
G
:
𝒱
∗
→
Δ
⁡
(
𝒱
N
)
G:\mathcal{V}^{*}\to\Delta(\mathcal{V}^{N})
,
G
:
x
↦
p
x
⋆
w
x
≡
p
θ
(
⋅
∣
x
)
⋆
w
(
x
,
p
x
)
G:x\mapsto p_{x}\star w_{x}\equiv p_{\theta}(\cdot\mid x)\star w(x,p_{x})
(B.1)
then
p
θ
p_{\theta}
will be
𝒲
\mathcal{W}
-locally-loss-optimal w.r.t. its pretraining loss.
In other words, if all perturbations in the family
𝒲
\mathcal{W}
can be “easily learnt,” then we should expect the LLM to be loss-optimal w.r.t.
𝒲
\mathcal{W}
.
If we believe
Claim
22
, we can see why our mechanism would apply
to confidence-calibration but not to full-calibration:
For confidence-calibration, the perturbation class
𝒲
B
\mathcal{W}_{B}
(
Definition
6
)
is simple enough to be learnable,
while for full calibration, the corresponding perturbation class
𝒲
B
(
full
)
\mathcal{W}_{B}^{\rm{(full)}}
(
Definition
35
) is too large to be efficiently learnable from samples.
To gain intuition for this, it helps to directly compare
Definition
35
to
Definition
6
.
From this discussion, we can see it is likely possible to extend our results
to certain types of calibration which are weaker than full-calibration,
but stronger than confidence-calibration.
We leave this direction for future work.
Appendix C
Additional Experimental Results
Due to their volume, disaggregated reliability diagram results are reported separately in
App.
F
.
Figure 8
:
Calibration error for three models based on Mistral-7B-
v0.1: pretrained-only, instruction-SFT model (zephyr-7b-sft-full),
DPO model (zephyr-7b-dpo-full).
We did not evaluate TriviaQA and SimpleQA for the “cot” response style.
The “cot” result for Mistral-7B-v0.1 for OpenMathInstruct is missing due to the model not terminating generation within its maximum context length.
Appendix D
Additional Experimental Details
Datasets.
We focus on open-ended question-answer (QA) settings,
since calibration for multiple-choice QA is
already well-studied
(
Kadavath et al., 2022
;
Zhu et al., 2023
)
, and a special case of our results.
We evaluate on:
GSM8K
(
Cobbe et al., 2021
)
,
OpenMathInstruct-2
(
Toshniwal et al., 2025
)
,
TriviaQA
(
Joshi et al., 2017
)
,
and SimpleQA
(
Wei et al., 2024
)
,
from Huggingface datasets
(
Wolf et al., 2019
;
Lhoest et al., 2021
)
.
Models.
We evaluate on models including
the Qwen, Gemini, Mistral, and Llama family,
of sizes from 0.5B to 72B.
The full list of models we evaluate is in
Sec.
D.4
.
We use vLLM
(
Kwon et al., 2023
)
for inference.
Prompt format.
See
Sec.
D.5
for the exact phrasing used in prompts.
All of our experiments include
5
5
-shot examples in the prompt.
We use three different prompt types, designed to elicit three different styles
of responses from the model: “sentence”, “concise”, and “chain-of-thought (cot)”. The few-shot examples are formatted in the desired style (e.g. for the “sentence” type, the few-shot examples have complete-sentence answers). For instruct models, in addition to formatted few-shot examples, the prompt also includes explicit formatting instructions.
The “concise” prompt type encourages the model to respond with just the final answer (a single word, phrase, or number).
The “sentence” prompt type asks the model to answer each question in a complete sentence (making it likely to phrase the same semantic answer in different ways, so the
B
B
-collapsing function is essential for a meaningful notion of semantic calibration).
The “cot” prompt type elicits chain-of-thought reasoning from the model; this prompt
type is only used for math datasets.
These prompts are typically successful in eliciting the desired type of responses from the model.
However, in some cases we observed models (especially Qwen models)
produce “chain-of-thought” responses
even when prompted to reply in a single word.
To exclude such cases, we exclude any responses for the
“concise” prompt on math datasets which are too long
(heuristically, more than 15 characters before the first newline).
The semantic collapsing function.
Recall, the function
B
B
is intended to collapse semantically-equivalent
generations into a single class, an idea proposed by
Kuhn et al. (2023)
.
We implement the function
B
B
with a two-stage procedure as follows.
The first stage is canonicalization: we extract a short “canonical form” answer
from the LLM’s response. For “concise” and “cot” prompt types, this is done via simple
string parsing (for “cot”, extracting only the final answer).
For the “sentence” type, we use a strong LLM (Qwen3-14B-Instruct) prompted
to extract a short-answer from the generation, given the question as context.
The prompts used for canonicalization are in
Sec.
D.5
:
Prompt
D.5
for non-math settings, and
Prompt
D.5
for math settings.
We also normalize strings at this stage, converting to lower-case and stripping spaces,
including a math-specific normalization for domains with LaTeX outputs.
Specifically, we use the MATH string-normalization
from Minerva, given in Listing 1, Appendix D.1 of
Lewkowycz et al. (2022)
.
The second stage, used only for non-math settings, is semantic clustering:
we prompt an LLM judge (Qwen3-14B-Instruct) to assess whether two responses to a question are semantically equivalent, and use the output to cluster responses
11
11
11
This is a slight variation of the two-way entailment method used by
Farquhar et al. (2024)
.
.
This is necessary for non-math settings to handle irrelevant differences in canonical forms
(e.g. “Seattle, WA” vs “Seattle”).
The prompt used for semantic equivalence is Prompt
D.5
in
Sec.
D.5
.
For math settings, the second stage is unnecessary, since the first stage already outputs a
number or symbol that can be directly compared.
Measuring calibration.
We first produce an LLM-induced semantic classifier, following the experimental procedure described in
Sec.
2
and illustrated in
Fig.
1
.
For each dataset, we take 10K random evaluation samples
(or the entire dataset for those with fewer than 10K total samples).
For each question, we construct the appropriate
5
5
-shot prompt,
sample
M
=
50
M=50
responses from the LLM at temperature
1
1
,
and then apply the semantic collapsing function (described above) to each response.
The semantic confidence is defined as the empirical frequency of the plurality semantic class,
and the semantic accuracy is the
0
/
1
0/1
indicator of whether this
plurality class matches the ground-truth’s semantic class.
This yields, for each question, a pair of
(semantic-confidence, semantic-accuracy)
∈
[
0
,
1
]
×
{
0
,
1
}
\in[0,1]\times\{0,1\}
.
We then evaluate the calibration of the resulting classifier
over the entire dataset of questions using SmoothECE (smECE,
Błasiok and Nakkiran (2024)
),
a theoretically-principled version of the Expected Calibration Error (ECE),
as described below.
D.1
Calibration Metric: SmoothECE
We measure calibration error using SmoothECE (smECE)
Błasiok and Nakkiran (2024)
,
which is essentially a kernel-smoothed version of Expected-Calibration-Error
with better theorhetical properties.
For interpretability reasons,
we chose to use a
fixed
bandwidth of
σ
=
0.05
\sigma=0.05
,
rather than the automatic bandwidth defined by SmoothECE.
This fixed choice makes smECE behave closer to a “smoothed” version of
BinnedECE with bin-width
=
0.05
=0.05
, which makes the metric more directly comparable to prior works.
Fixing the bandwidth comes at the cost of slightly weaker theoretical guarantees; however the smECE at scale
σ
\sigma
still bounds the distance-to-calibration
(
Błasiok et al., 2023a
)
in the following way:
(
dCE
¯
−
σ
)
≤
smECE
σ
≤
(
1
+
1
σ
)
​
dCE
¯
.
(\underline{\mathrm{dCE}}-\sigma)\leq\mathrm{smECE}_{\sigma}\leq\left(1+\frac{1}{\sigma}\right)\underline{\mathrm{dCE}}.
(D.1)
The LHS is
Błasiok and Nakkiran (2024, Lemma 8)
and the RHS is
Błasiok and Nakkiran (2024, Lemma 9)
.
We use the SmoothECE implementation provided by:
https://github.com/apple/ml-calibration
.
Specifically, we use
relplot.smECE_sigma
with
σ
=
0.05
\sigma=0.05
.
D.2
Visualizing calibration: reliability diagrams
We follow the guidance of
Błasiok and Nakkiran (2024)
,
and visualize calibration using kernel-smoothed reliability diagrams.
Reading the Diagram.
Fig.
3
gives several examples of reliability diagrams.
The solid red line is the regression line,
an estimate of
μ
⁡
(
c
)
:=
𝔼
[
semantic accuracy
∣
semantic confidence
=
c
]
\mu(c):=\mathop{\mathbb{E}}[\textrm{semantic accuracy}\mid\textrm{semantic confidence}=c]
.
The black cross is the point
(
𝔼
[
semantic confidence
]
,
𝔼
[
semantic accuracy
]
)
∈
[
0
,
1
]
×
[
0
,
1
]
(\mathop{\mathbb{E}}[\textrm{semantic confidence}],\mathop{\mathbb{E}}[\textrm{semantic accuracy}])\in[0,1]\times[0,1]
, that is, the average semantic confidence and accuracy.
The gray histograms at the bottom of the plot visualize the
density of semantic confidences.
We plot two overlaid histograms,
one for the confidence distribution of correct predictions
(i.e. the confidence of samples where semantic-accuracy=1),
and another for the confidence distribution of incorrect predictions.
The width of the red regression line varies with the overall density of
semantic-confidences.
Implementation Details.
For reliability diagrams, we use the implementation of
relplot (
https://github.com/apple/ml-calibration
)
with minor modifications:
we use a fixed kernel bandwidth
σ
=
0.05
\sigma=0.05
for the regression line,
and we visualize the density of confidences using histogram binning with 15 constant-width bins.
D.3
LoRA Fine-Tuning
To test
Claim
11
more quantitatively, we train a
LoRA version of the LLM to explicitly learn the function
G
G
defined in
Claim
11
.
We do this as follows.
Let
p
θ
p_{\theta}
be the base model.
Instantiate a rank=8 LoRA adapter
(
Hu et al., 2022
)
on top of the original model
p
θ
p_{\theta}
,
which we denote
p
ϕ
p_{\phi}
.
We want to train
p
ϕ
p_{\phi}
to behave as the “semantically-collapsed” version of
p
θ
p_{\theta}
.
That is, when prompted with a question
x
x
, the model
p
ϕ
p_{\phi}
should generate
a distribution on answers
b
b
which imitates the base model’s semantic answers
B
x
​
(
z
)
B_{x}(z)
:
p
ϕ
(
b
∣
x
)
≈
Pr
z
∼
p
θ
(
⋅
∣
x
)
[
B
x
(
z
)
=
b
]
≡
(
B
x
♯
p
x
)
(
b
)
\quad p_{\phi}(b\mid x)\approx\Pr_{z\sim p_{\theta}(\cdot\mid x)}[B_{x}(z)=b]\equiv(B_{x}\sharp p_{x})(b)
(D.2)
Since our implementation of the collapsing function
B
B
produces string outputs (canonical answers),
we can train
p
ϕ
p_{\phi}
as a standard autoregressive model.
Explicitly:
1.
For each question in the dataset
x
x
,
sample the original model 50 times, and apply the collapsing function
B
B
to each generation.
This produces 50 samples
{
(
x
,
b
i
)
}
\{(x,b_{i})\}
of question
x
x
and canonical-answer
b
i
b_{i}
for each
original question
x
x
, effectively expanding the original dataset size by 50 times.
2.
Train
p
ϕ
p_{\phi}
with the standard autoregressive objective,
on the prompt-completion pairs
{
(
x
,
b
i
)
}
\{(x,b_{i})\}
from above.
That is, train
p
ϕ
p_{\phi}
to complete prompt
x
x
with generation
b
i
b_{i}
.
Our training procedure is similar to the procedure used to train “P(IK)” in
Kadavath et al. (2022)
,
in that we also train on an “expanded” training set defined by base model samples.
Similar to
Kadavath et al. (2022)
, we do this mainly for convenience.
For GSM8K, we hold-out 2000 questions for evaluation, and use the remainder for training as above.
We train all models on an 8xA100 node for 1 epoch on the expanded dataset, using the
SFTTrainer
implementation
from Huggingface TRL
(
von Werra et al., 2020
)
with the following parameters in
Table
1
.
Note, we shuffle the expanded training set manually beforehand,
so we do not ask the dataloader to shuffle.
Table 1
:
Hyperparameters for Supervised Fine-Tuning (SFT).
Parameter
Value
Training & Hardware
num_train_epochs
1
per_device_train_batch_size
4
gradient_accumulation_steps
2
(Effective Batch Size)
64 (4 x 8 GPUs x 2)
bf16
True
Optimizer & Scheduler
optim
adamw_torch_fused
learning_rate
5e-5
weight_decay
0.0
warmup_ratio
0.05
PEFT (LoRA) Configuration
use_peft
True
lora_r
8
lora_alpha
16
lora_dropout
0.0
lora_target_modules
all-linear
task_type
CAUSAL_LM
bias
none
Data Handling
packing
False
dataloader_shuffle
False
After training, we evaluate how closely
Eq.
D.2
holds,
by estimating the KL divergence between RHS and LHS of
Eq.
D.2
.
This KL measures how well our LoRA
p
ϕ
p_{\phi}
matches its training distribution.
Conveniently, the KL can be written as the difference between
the
negative-log-loss
of
p
ϕ
p_{\phi}
and
the
semantic entropy
of the original model
p
θ
p_{\theta}
:
Gap to optimality
:
=
K
L
(
(
B
x
♯
p
x
)
∥
p
ϕ
(
⋅
∣
x
)
)
\displaystyle:=KL(\penalty\ (B_{x}\sharp p_{x})\penalty\ \penalty\ \|\penalty\ \penalty\ p_{\phi}(\cdot\mid x)\penalty\ )
(D.3)
=
𝔼
x
∼
𝒟
z
∼
p
θ
​
(
z
∣
x
)
[
−
log
⁡
p
ϕ
​
(
B
⁡
(
z
)
∣
x
)
]
⏟
Eval NLL loss of
p
ϕ
−
H
⁡
(
B
x
​
♯
​
p
x
)
⏟
Semantic entropy of
p
θ
\displaystyle=\underbrace{\mathop{\mathbb{E}}_{\begin{subarray}{c}x\sim\mathcal{D}\\
z\sim p_{\theta}(z\mid x)\end{subarray}}[-\log p_{\phi}(B(z)\mid x)]}_{\textrm{Eval NLL loss of $p_{\phi}$}}-\underbrace{H(B_{x}\sharp p_{x})}_{\textrm{Semantic entropy of $p_{\theta}$}}
(D.4)
This is particularly convenient because the eval log-loss is a
standard metric tracked during training.
Note that for our purposes, it is important to compute the
unnormalized
log-loss (i.e., not normalized by sequence-length).
In
Fig.
6
,
we plot the KL gap of
Eq.
D.4
on the x-axis, and the SmoothECE of the original model
p
θ
p_{\theta}
on the y-axis.
We evaluate base models: Qwen2.5-{0.5B, 1.5B, 3B, 7B, 14B},
with all three response styles:
concise
,
sentence
,
cot
.
This results in 15 points plotted in
Fig.
6
,
colored according to response style using the color scheme of
Fig.
2
.
We observe that, consistent with
Claim
11
,
configurations where the semantic class distribution is easy-to-learn
(low KL gap) also have small calibration error.
The points with high KL (and high calibration error) are
the
chain-of-thought
experiments,
as well as the small 0.5B model with the “sentence” response type.
D.4
LLMs evaluated
Below, we list all models evaluated in this paper.
All were obtained from HuggingFace.
Table 2
:
Pretrained-only base models evaluated in this paper. Models sharing a prefix and reference are grouped.
Family Prefix
Model Suffix
Reference
google/
gemma-2-2b
(
Gemma Team et al., 2024
)
gemma-2-9b
gemma-2-27b
gemma-3-1b-pt
(
Gemma Team et al., 2025
)
gemma-3-4b-pt
gemma-3-12b-pt
gemma-3-27b-pt
Qwen/
Qwen2.5-0.5B
(
Yang et al., 2024c
)
Qwen2.5-1.5B
Qwen2.5-3B
Qwen2.5-7B
Qwen2.5-14B
Qwen2.5-32B
Qwen2.5-72B
Qwen2.5-Math-1.5B
(
Yang et al., 2024b
)
Qwen2.5-Math-7B
Qwen2.5-Math-72B
Qwen3-0.6B-Base
(
Yang et al., 2025
)
Qwen3-1.7B-Base
Qwen3-4B-Base
Qwen3-8B-Base
Qwen3-14B-Base
mistralai/
Mistral-7B-v0.1
(
Jiang et al., 2023a
)
Mistral-7B-v0.3
Mistral-Small-24B-Base-2501
(
Mistral AI Team, 2024b
)
Mixtral-8x7B-v0.1
(
Mistral AI Team, 2023
)
meta-llama/
Llama-3.1-8B
(
Grattafiori et al., 2024
)
Llama-3.1-70B
Table 2
:
Table 3
:
Instruction-tuned models evaluated in this paper. Models sharing a prefix and reference are grouped.
Family Prefix
Model Suffix
Reference
google/
gemma-2-2b-it
(
Gemma Team et al., 2024
)
gemma-2-9b-it
gemma-2-27b-it
gemma-3-1b-it
(
Gemma Team et al., 2025
)
gemma-3-4b-it
gemma-3-12b-it
gemma-3-27b-it
Qwen/
Qwen2.5-0.5B-Instruct
(
Yang et al., 2024c
)
Qwen2.5-1.5B-Instruct
Qwen2.5-3B-Instruct
Qwen2.5-7B-Instruct
Qwen2.5-14B-Instruct
Qwen2.5-32B-Instruct
Qwen2.5-72B-Instruct
Qwen2.5-Math-1.5B-Instruct
(
Yang et al., 2024b
)
Qwen2.5-Math-7B-Instruct
Qwen2.5-Math-72B-Instruct
Qwen3-0.6B
(
Yang et al., 2025
)
Qwen3-1.7B
Qwen3-4B
Qwen3-8B
Qwen3-14B
Qwen3-32B
mistralai/
Mistral-7B-Instruct-v0.1
(
Jiang et al., 2023a
)
Mistral-7B-Instruct-v0.3
Ministral-8B-Instruct-2410
(
Mistral AI Team, 2024a
)
Mistral-Small-24B-Instruct-2501
(
Mistral AI Team, 2024b
)
NousResearch/
Nous-Hermes-2-Mixtral-8x7B-SFT
(
Nous Research, 2024b
)
Nous-Hermes-2-Mixtral-8x7B-DPO
(
Nous Research, 2024a
)
alignment-
zephyr-7b-dpo-full
(
Tunstall et al., 2023
)
handbook/
zephyr-7b-sft-full
meta-llama/
Llama-3.1-8B-Instruct
(
Grattafiori et al., 2024
)
Llama-3.1-70B-Instruct
Llama-3.3-70B-Instruct
microsoft/
phi-4
(
Abdin et al., 2024
)
Table 3
:
D.5
Prompts
We use 3 different prompt styles: concise, sentence, and chain-of-thought (cot).
All prompts use 5 few-shot examples from the dataset.
We describe the prompt formatting here by way of example, using our prompts for the GSM8K dataset.
For base models, we use the full prompt text as context,
while for instruct models we format
the few-shot examples using the model-specific chat template (per Huggingface).
Prompt
D.5
shows the
“concise"
prompt for GSM8K.
This prompt style uses only the final answers provided by the dataset
(excluding any chain-of-thought).
Prompt
D.5
shows the
“sentence"
prompt type.
This prompt formats the few-shot answers in complete sentences,
and also includes instructions to format answers accordingly.
Note that we intentionally varied the sentence structure of the few-shot examples,
to encourage the model to use a diversity of phrasings.
This makes the “sentence” responses more syntactically complex than the “concise” responses,
though not more
semantically
complex — thus testing the limits of our theory.
Prompt
D.5
shows the
“cot"
prompt type.
This includes reasoning and formatting instructions, as well
as few-shot examples that include reasoning-traces (provided by the dataset).
The prompt formatting for other datasets follow the same conventions as these GSM8K examples.
We exclude the “cot” prompt type for non-math datasets.
Prompt 1: GSM8K-concise
⬇
Question
:
Natalia
sold
clips
to
48
of
her
friends
in
April
,
and
then
she
sold
half
as
many
clips
in
May
.
How
many
clips
did
Natalia
sell
altogether
in
April
and
May
?
Answer
:
72
Question
:
Weng
earns
$12
an
hour
for
babysitting
.
Yesterday
,
she
just
did
50
minutes
of
babysitting
.
How
much
did
she
earn
?
Answer
:
10
Question
:
Betty
is
saving
money
for
a
new
wallet
which
costs
$100
.
Betty
has
only
half
of
the
money
she
needs
.
Her
parents
decided
to
give
her
$15
for
that
purpose
,
and
her
grandparents
twice
as
much
as
her
parents
.
How
much
more
money
does
Betty
need
to
buy
the
wallet
?
Answer
:
5
Question
:
Julie
is
reading
a
120-
page
book
.
Yesterday
,
she
was
able
to
read
12
pages
and
today
,
she
read
twice
as
many
pages
as
yesterday
.
If
she
wants
to
read
half
of
the
remaining
pages
tomorrow
,
how
many
pages
should
she
read
?
Answer
:
42
Question
:
James
writes
a
3-
page
letter
to
2
different
friends
twice
a
week
.
How
many
pages
does
he
write
a
year
?
Answer
:
624
Question
:
{
QUESTION
}
Answer
:
Prompt 2: GSM8K-sentence
⬇
Answer
the
following
question
in
a
single
brief
but
complete
sentence
.
Question
:
Natalia
sold
clips
to
48
of
her
friends
in
April
,
and
then
she
sold
half
as
many
clips
in
May
.
How
many
clips
did
Natalia
sell
altogether
in
April
and
May
?
Answer
:
Natalia
sold
72
clips
in
April
and
May
combined
.
Answer
the
following
question
in
a
single
brief
but
complete
sentence
.
Question
:
Weng
earns
$12
an
hour
for
babysitting
.
Yesterday
,
she
just
did
50
minutes
of
babysitting
.
How
much
did
she
earn
?
Answer
:
Weng
earned
only
$10
yesterday
.
Answer
the
following
question
in
a
single
brief
but
complete
sentence
.
Question
:
Betty
is
saving
money
for
a
new
wallet
which
costs
$100
.
Betty
has
only
half
of
the
money
she
needs
.
Her
parents
decided
to
give
her
$15
for
that
purpose
,
and
her
grandparents
twice
as
much
as
her
parents
.
How
much
more
money
does
Betty
need
to
buy
the
wallet
?
Answer
:
Betty
needs
$5
more
to
buy
the
wallet
.
Answer
the
following
question
in
a
single
brief
but
complete
sentence
.
Question
:
Julie
is
reading
a
120-
page
book
.
Yesterday
,
she
was
able
to
read
12
pages
and
today
,
she
read
twice
as
many
pages
as
yesterday
.
If
she
wants
to
read
half
of
the
remaining
pages
tomorrow
,
how
many
pages
should
she
read
?
Answer
:
She
would
need
to
read
42
pages
tomorrow
.
Answer
the
following
question
in
a
single
brief
but
complete
sentence
.
Question
:
James
writes
a
3-
page
letter
to
2
different
friends
twice
a
week
.
How
many
pages
does
he
write
a
year
?
Answer
:
James
writes
624
pages
per
year
.
Answer
the
following
question
in
a
single
brief
but
complete
sentence
.
Question
:
{
QUESTION
}
Answer
:
Prompt 3: GSM8K-cot
⬇
Answer
the
following
question
.
To
do
that
,
first
reason
about
it
by
saying
’
Reasoning
:’
and
then
derive
the
answer
.
After
that
,
when
you
are
done
,
write
’
My
answer
is
:
’
and
write
a
short
and
concise
answer
to
the
question
.
Last
,
write
<
DONE
>.
Question
:
Natalia
sold
clips
to
48
of
her
friends
in
April
,
and
then
she
sold
half
as
many
clips
in
May
.
How
many
clips
did
Natalia
sell
altogether
in
April
and
May
?
Answer
:
Reasoning
:
Natalia
sold
48/2
=
<<48/2=24>>24
clips
in
May
.
Natalia
sold
48+24
=
<<48+24=72>>72
clips
altogether
in
April
and
May
.
My
answer
is
:
72<
DONE
>
Answer
the
following
question
.
To
do
that
,
first
reason
about
it
by
saying
’
Reasoning
:’
and
then
derive
the
answer
.
After
that
,
when
you
are
done
,
write
’
My
answer
is
:
’
and
write
a
short
and
concise
answer
to
the
question
.
Last
,
write
<
DONE
>.
Question
:
Weng
earns
$12
an
hour
for
babysitting
.
Yesterday
,
she
just
did
50
minutes
of
babysitting
.
How
much
did
she
earn
?
Answer
:
Reasoning
:
Weng
earns
12/60
=
$
<<12/60=0.2>>0.2
per
minute
.
Working
50
minutes
,
she
earned
0.2
x
50
=
$
<<0.2*50=10>>10.
My
answer
is
:
10<
DONE
>
Answer
the
following
question
.
To
do
that
,
first
reason
about
it
by
saying
’
Reasoning
:’
and
then
derive
the
answer
.
After
that
,
when
you
are
done
,
write
’
My
answer
is
:
’
and
write
a
short
and
concise
answer
to
the
question
.
Last
,
write
<
DONE
>.
Question
:
Betty
is
saving
money
for
a
new
wallet
which
costs
$100
.
Betty
has
only
half
of
the
money
she
needs
.
Her
parents
decided
to
give
her
$15
for
that
purpose
,
and
her
grandparents
twice
as
much
as
her
parents
.
How
much
more
money
does
Betty
need
to
buy
the
wallet
?
Answer
:
Reasoning
:
In
the
beginning
,
Betty
has
only
100
/
2
=
$
<<100/2=50>>50.
Betty
’
s
grandparents
gave
her
15
*
2
=
$
<<15*2=30>>30.
This
means
,
Betty
needs
100
-
50
-
30
-
15
=
$
<<100-50-30-15=5>>5
more
.
My
answer
is
:
5<
DONE
>
Answer
the
following
question
.
To
do
that
,
first
reason
about
it
by
saying
’
Reasoning
:’
and
then
derive
the
answer
.
After
that
,
when
you
are
done
,
write
’
My
answer
is
:
’
and
write
a
short
and
concise
answer
to
the
question
.
Last
,
write
<
DONE
>.
Question
:
Julie
is
reading
a
120-
page
book
.
Yesterday
,
she
was
able
to
read
12
pages
and
today
,
she
read
twice
as
many
pages
as
yesterday
.
If
she
wants
to
read
half
of
the
remaining
pages
tomorrow
,
how
many
pages
should
she
read
?
Answer
:
Reasoning
:
Maila
read
12
x
2
=
<<12*2=24>>24
pages
today
.
So
she
was
able
to
read
a
total
of
12
+
24
=
<<12+24=36>>36
pages
since
yesterday
.
There
are
120
-
36
=
<<120-36=84>>84
pages
left
to
be
read
.
Since
she
wants
to
read
half
of
the
remaining
pages
tomorrow
,
then
she
should
read
84/2
=
<<84/2=42>>42
pages
.
My
answer
is
:
42<
DONE
>
Answer
the
following
question
.
To
do
that
,
first
reason
about
it
by
saying
’
Reasoning
:’
and
then
derive
the
answer
.
After
that
,
when
you
are
done
,
write
’
My
answer
is
:
’
and
write
a
short
and
concise
answer
to
the
question
.
Last
,
write
<
DONE
>.
Question
:
James
writes
a
3-
page
letter
to
2
different
friends
twice
a
week
.
How
many
pages
does
he
write
a
year
?
Answer
:
Reasoning
:
He
writes
each
friend
3*2=<<3*2=6>>6
pages
a
week
So
he
writes
6*2=<<6*2=12>>12
pages
every
week
That
means
he
writes
12*52=<<12*52=624>>624
pages
a
year
My
answer
is
:
624<
DONE
>
Answer
the
following
question
.
To
do
that
,
first
reason
about
it
by
saying
’
Reasoning
:’
and
then
derive
the
answer
.
After
that
,
when
you
are
done
,
write
’
My
answer
is
:
’
and
write
a
short
and
concise
answer
to
the
question
.
Last
,
write
<
DONE
>.
Question
:
{
QUESTION
}
Answer
:
Prompt 4: Canonicalization
⬇
Question
:
"{
QUESTION
}"
Response
:
"{
RESPONSE
}"
Your
task
is
to
return
**
only
**
the
core
answer
from
this
response
.
Follow
these
rules
:
-
Keep
only
the
core
answer
(
e
.
g
.,
a
number
,
a
name
,
or
a
short
phrase
).
-
Remove
all
extra
words
and
filler
.
-
Expand
all
abbreviations
to
their
full
form
(
e
.
g
.,
’
USA
’
->
’
United
States
of
America
’).
-
Write
all
numbers
with
digits
,
not
as
words
(
e
.
g
.,
’
eight
’
->
’8’).
-
For
locations
,
output
only
the
highest
-
precision
part
(
e
.
g
.
’
Seattle
,
Washington
’
->
’
Seattle
’)
-
For
dates
,
unless
otherwise
specified
,
format
as
YYYY
-
MM
-
DD
(
e
.
g
.
"
August
1,
1990"
->
"1990-08-01").
If
only
a
month
or
year
is
specified
,
leave
as
-
is
(
e
.
g
.
"
August
"
or
"2003"
or
"
July
,
2000").
Do
not
make
up
unspecified
information
.
-
No
explaining
or
reasoning
.
Output
the
core
answer
only
.
-
If
the
response
does
not
address
the
question
,
or
if
you
are
unsure
what
to
do
,
return
the
response
unchanged
.
-
Never
alter
the
meaning
of
the
response
,
even
if
it
is
incorrect
.
-
Do
not
infer
missing
information
;
only
rephrase
what
is
given
in
the
response
.
Prompt 5: Canonicalization (math)
⬇
Response
:
"{
RESPONSE
}"
Your
task
is
to
return
**
only
**
the
core
answer
from
this
response
.
Follow
these
rules
:
-
Keep
only
the
core
answer
,
as
a
raw
number
or
LaTeX
string
(
e
.
g
.
’0.5’
or
’\
frac
{1}{2}’).
-
If
the
answer
is
the
value
of
a
variable
,
only
output
the
value
itself
(
e
.
g
.
’
x
=10’
->
’10’).
-
Write
all
numbers
with
digits
,
not
as
words
(
e
.
g
.,
’
eight
’
->
’8’).
-
Remove
all
extra
words
and
filler
.
-
No
explaining
or
reasoning
.
Output
the
core
answer
only
.
-
If
the
response
does
not
contain
a
numeric
value
,
or
if
you
are
unsure
what
to
do
,
return
the
response
unchanged
.
-
Never
alter
the
value
of
the
response
,
even
if
it
is
incorrect
.
-
Do
not
infer
missing
information
;
only
extract
what
is
given
in
the
response
.
Prompt 6: Semantic Equivalence
⬇
You
will
be
given
a
question
,
and
two
possible
responses
.
Your
task
is
to
determine
whether
the
two
answers
are
semantically
consistent
,
i
.
e
.,
whether
the
two
responses
agree
on
what
the
answer
to
the
question
is
.
Question
:
{
QUESTION
}
Response
1:
{
RESPONSE1
}
Response
2:
{
RESPONSE2
}
Are
these
two
responses
semantically
aligned
responses
to
the
question
?
Respond
only
with
either
the
string
"
Yes
"
or
the
string
"
No
".
Appendix E
Theory
E.1
Quick Reference
In this section, we provide proofs of the theorems presented in the main text.
•
Thm.
7
is proved in
Sec.
E.5
.
•
Thm.
10
is formally restated and proved as
Thm.
31
in
Sec.
E.6
.
Proving these theorems involves some additional theoretical machinery, particularly
weighted calibration
,
which we develop here.
We restate some of the notation
and definitions from the main body for convenience.
We also give more general versions of several of our results in this section:
•
Sec.
E.7
gives
full calibration
analogs of our confidence-calibration results.
•
Sec.
E.8
extends from cross-entropy loss to general
proper losses
, providing quantitative bounds between post-processing and calibration gap.
E.2
Weighted Calibration
A key object in our theory is the notion of
weighted calibration
,
from
Gopalan et al. (2024)
,
which is capable of expressing many different types of calibration.
We will use a version of this definition suitable for our LLM setting,
stated below.
Definition 23
(Weighted Calibration,
Gopalan et al. (2024)
)
.
For a set
𝒲
\mathcal{W}
of weight functions
w
:
𝒱
∗
×
Δ
⁡
(
𝒱
N
)
→
ℝ
N
w:\mathcal{V}^{*}\times\Delta(\mathcal{V}^{N})\to\mathbb{R}^{N}
,
and a distribution
𝒟
\mathcal{D}
over pairs
(
x
,
y
)
∈
𝒱
∗
×
𝒱
N
(x,y)\in\mathcal{V}^{*}\times\mathcal{V}^{N}
,
a model
p
θ
p_{\theta}
is
perfectly
𝒲
\mathcal{W}
-weighted-calibrated on
𝒟
\mathcal{D}
if:
𝔼
(
x
,
y
)
∼
𝒟
[
⟨
y
~
−
p
x
,
w
⁡
(
x
,
p
x
)
⟩
]
≡
0
\displaystyle\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}\left[\left\langle\tilde{y}-p_{x},w(x,p_{x})\right\rangle\right]\equiv 0
where
p
x
:=
p
θ
(
⋅
∣
x
)
∈
Δ
(
𝒱
N
)
⊂
ℝ
|
𝒱
N
|
p_{x}:=p_{\theta}(\cdot\mid x)\in\Delta(\mathcal{V}^{N})\subset\mathbb{R}^{|\mathcal{V}^{N}|}
is the model’s output distribution on input
x
x
,
and
y
~
∈
{
0
,
1
}
|
𝒱
N
|
\tilde{y}\in\{0,1\}^{|\mathcal{V}^{N}|}
is the one-hot-encoding of
y
y
.
Remark 24
.
For the reader familiar with multi-calibration
(
Hébert-Johnson et al., 2018
)
:
note that in our definition above, the weight functions
w
w
are allowed to depend
on the prompt
x
x
. This allows weighted calibration to capture various kinds of multi-calibration.
E.3
Equivalence between Weighted Calibration and Local Loss Optimality
Weighted calibration is equivalent to local loss optimality w.r.t. perturbations in the weight class. In this section, we prove this in a special case relevant to our framework; a more general result presented in
Sec.
E.8
.
For the log-loss
ℓ
(
y
,
f
)
:=
−
∑
i
y
i
log
(
f
i
)
\ell(y,f):=-\sum_{i}y_{i}\log(f_{i})
, we can analyze perturbations more easily through its dual representation. The dual loss, which operates on a logit vector
z
z
is defined as
ℓ
⋆
​
(
y
,
z
)
=
log
⁡
(
∑
j
=
1
K
e
z
j
)
−
y
T
​
z
​
and
​
∇
z
ℓ
⋆
​
(
y
,
z
)
=
softmax
​
(
z
)
−
y
=
f
−
y
\ell^{\star}(y,z)=\log\left(\sum_{j=1}^{K}e^{z_{j}}\right)-y^{T}z\text{ and }\nabla_{z}\ell^{\star}(y,z)=\text{softmax}(z)-y=f-y
The primal and dual views are connected by the variable mapping
z
=
log
⁡
f
z=\log f
, which provides the key equality
ℓ
⁡
(
y
,
f
)
=
ℓ
⋆
​
(
y
,
z
)
\ell(y,f)=\ell^{\star}(y,z)
. (This is a special case of a more general primal/dual framework for proper losses; c.f.
Table
4
.) The relationship allows us to translate complex perturbations in the probability space into simple ones in the logit space. A multiplicative re-weighting of the probabilities, defined as
f
⋆
w
:=
softmax
​
(
log
⁡
f
+
w
)
=
softmax
​
(
z
+
w
)
f\star w:=\text{softmax}(\log f+w)=\text{softmax}(z+w)
, is equivalent to a simple additive perturbation
w
w
on the logits. Therefore, the loss of the perturbed model can be expressed in either world:
ℓ
⁡
(
y
,
f
⋆
w
)
⏟
Loss on perturbed probabilities
=
ℓ
⋆
​
(
y
,
z
+
w
)
⏟
Loss on perturbed logits
\underbrace{\ell(y,f\star w)}_{\text{Loss on perturbed probabilities}}\quad=\quad\underbrace{\ell^{\star}(y,z+w)}_{\text{Loss on perturbed logits}}
(E.1)
Theorem 25
(Equivalence of Calibration and Local Loss Optimality)
.
For all models
p
θ
p_{\theta}
, distributions
𝒟
\mathcal{D}
,
proper losses
ℓ
\ell
and families of weight functions
𝒲
\mathcal{W}
(Definition
23
):
the model
p
θ
p_{\theta}
is perfectly
𝒲
\mathcal{W}
-weighted-calibrated
on
𝒟
\mathcal{D}
if and only if
it is
𝒲
\mathcal{W}
-locally loss-optimal on
𝒟
\mathcal{D}
w.r.t. loss
ℓ
\ell
.
Proof.
We apply the first-order optimality condition to the dual loss
ℓ
⋆
​
(
y
,
z
)
\ell^{\star}(y,z)
with a simple additive perturbation
w
w
on the logits
z
z
. With the perturbed loss function, for
ε
>
0
\varepsilon>0
,
ℒ
⁡
(
ε
)
=
ℓ
⋆
​
(
y
,
z
+
ε
​
w
)
​
and
​
d
​
ℒ
d
​
ε
​
(
ε
)
=
⟨
∇
z
ℓ
⋆
​
(
y
,
z
+
ε
​
w
)
,
w
⟩
\mathcal{L}(\varepsilon)=\ell^{\star}(y,z+\varepsilon w)\text{ and }\frac{d\mathcal{L}}{d\varepsilon}(\varepsilon)=\langle\nabla_{z}\ell^{\star}(y,z+\varepsilon w),w\rangle
By local loss optimality
0
\displaystyle 0
≤
ℒ
⁡
(
ε
)
−
ℒ
⁡
(
0
)
ε
=
d
​
ℒ
d
​
ε
​
(
0
)
+
o
⁡
(
ε
)
ε
⟶
⟨
∇
z
ℓ
⋆
​
(
y
,
z
)
,
w
⟩
\displaystyle\leq\frac{\mathcal{L}(\varepsilon)-\mathcal{L}(0)}{\varepsilon}=\frac{d\mathcal{L}}{d\varepsilon}(0)+\frac{o(\varepsilon)}{\varepsilon}\longrightarrow\langle\nabla_{z}\ell^{\star}(y,z),w\rangle
The same reasoning replacing
w
w
by
−
w
-w
, we also have
⟨
∇
z
ℓ
⋆
​
(
y
,
z
)
,
w
⟩
≤
0
\langle\nabla_{z}\ell^{\star}(y,z),w\rangle\leq 0
. Thus
ℓ
⋆
​
(
y
,
z
)
≤
ℓ
⋆
​
(
y
,
z
+
ε
​
w
)
⟹
⟨
∇
z
ℓ
⋆
​
(
y
,
z
)
,
w
⟩
=
0
\ell^{\star}(y,z)\leq\ell^{\star}(y,z+\varepsilon w)\Longrightarrow\langle\nabla_{z}\ell^{\star}(y,z),w\rangle=0
The opposite implication follow from convexity, we have:
ℓ
⋆
​
(
y
,
z
+
w
)
≥
ℓ
⋆
​
(
y
,
z
)
+
⟨
∇
z
ℓ
⋆
​
(
y
,
z
)
,
w
⟩
.
\ell^{\star}(y,z+w)\geq\ell^{\star}(y,z)+\langle\nabla_{z}\ell^{\star}(y,z),w\rangle.
Thus, if
⟨
∇
z
ℓ
⋆
​
(
y
,
z
)
,
w
⟩
=
0
\langle\nabla_{z}\ell^{\star}(y,z),w\rangle=0
holds, the inequality simplifies to:
ℓ
⋆
​
(
y
,
z
+
w
)
≥
ℓ
⋆
​
(
y
,
z
)
.
\ell^{\star}(y,z+w)\geq\ell^{\star}(y,z).
Taking the expectation on both side
𝔼
(
x
,
y
)
∼
𝒟
[
ℓ
⁡
(
y
,
f
)
]
≤
𝔼
(
x
,
y
)
∼
𝒟
[
ℓ
⁡
(
y
,
f
⋆
w
)
]
\displaystyle\mathop{\mathbb{E}}_{\begin{subarray}{c}(x,y)\sim\mathcal{D}\end{subarray}}[\ell(y,f)]\leq\mathop{\mathbb{E}}_{\begin{subarray}{c}(x,y)\sim\mathcal{D}\end{subarray}}[\ell(y,f\star w)]
⟺
𝔼
(
x
,
y
)
∼
𝒟
[
ℓ
⋆
​
(
y
,
z
)
]
≤
𝔼
(
x
,
y
)
∼
𝒟
[
ℓ
⋆
​
(
y
,
z
+
w
)
]
\displaystyle\Longleftrightarrow\mathop{\mathbb{E}}_{\begin{subarray}{c}(x,y)\sim\mathcal{D}\end{subarray}}[\ell^{\star}(y,z)]\leq\mathop{\mathbb{E}}_{\begin{subarray}{c}(x,y)\sim\mathcal{D}\end{subarray}}[\ell^{\star}(y,z+w)]
⟺
𝔼
(
x
,
y
)
∼
𝒟
⟨
f
−
y
,
w
⟩
=
𝔼
(
x
,
y
)
∼
𝒟
⟨
∇
z
ℓ
⋆
​
(
y
,
z
)
,
w
⟩
=
0
\displaystyle\Longleftrightarrow\mathop{\mathbb{E}}_{\begin{subarray}{c}(x,y)\sim\mathcal{D}\end{subarray}}\langle f-y,w\rangle=\mathop{\mathbb{E}}_{\begin{subarray}{c}(x,y)\sim\mathcal{D}\end{subarray}}\langle\nabla_{z}\ell^{\star}(y,z),w\rangle=0
A model is calibrated under the log-loss if and only if its expected prediction error
f
−
y
f-y
is orthogonal to any systematic perturbation
w
w
of its logits.
∎
E.4
Equivalence between
B
B
-confidence-calibration and weighted calibration
In this section we prove that
B
B
-confidence-calibration can be characterized in terms of weighted calibration (
Definition
23
).
Notation and Setup
There are two relevant output spaces:
the space
𝒱
N
\mathcal{V}^{N}
of long-form answer strings,
and the space
[
K
]
[K]
of semantic answer classes.
Let
M
:=
|
𝒱
N
|
M:=|\mathcal{V}^{N}|
.
It will be convenient to identify strings
z
∈
𝒱
N
z\in\mathcal{V}^{N}
with an index in
[
M
]
[M]
, and we will abuse notation by writing
z
∈
[
M
]
z\in[M]
.
To simplify some of the proofs, we will rely on an explicit one-hot representation.
For a string
y
∈
𝒱
N
y\in\mathcal{V}^{N}
, we denote its one-hot representation as
y
~
∈
{
0
,
1
}
M
\tilde{y}\in\{0,1\}^{M}
.
For a given prompt
x
∈
𝒱
∗
x\in\mathcal{V}^{*}
, the model’s distribution over completions is
p
θ
(
⋅
∣
x
)
∈
Δ
(
𝒱
N
)
⊂
ℝ
M
p_{\theta}(\cdot\mid x)\in\Delta(\mathcal{V}^{N})\subset\mathbb{R}^{M}
,
which we treat as a vector embedded in
ℝ
M
\mathbb{R}^{M}
.
We write
p
x
:=
p
θ
(
⋅
∣
x
)
p_{x}:=p_{\theta}(\cdot\mid x)
for convenience.
A collapsing function
B
:
𝒱
∗
×
𝒱
N
→
[
K
]
B:\mathcal{V}^{*}\times\mathcal{V}^{N}\to[K]
assigns to each prompt
x
∈
𝒱
∗
x\in\mathcal{V}^{*}
and long-answer
y
∈
𝒱
N
y\in\mathcal{V}^{N}
a
B
B
-class
B
x
​
(
y
)
∈
[
K
]
B_{x}(y)\in[K]
.
Moreover, the function
B
B
along with the model
p
θ
p_{\theta}
induces a distribution on classes
[
K
]
[K]
as follows.
For a given input
x
∈
𝒱
∗
x\in\mathcal{V}^{*}
, we take the model’s distribution
p
θ
(
⋅
∣
x
)
p_{\theta}(\cdot\mid x)
and push it forward through
B
x
B_{x}
to obtain a categorical distribution
π
x
\pi_{x}
defined as
π
x
:=
B
x
♯
p
θ
(
⋅
∣
x
)
∈
Δ
K
.
\pi_{x}:=B_{x}\sharp p_{\theta}(\cdot\mid x)\;\in\;\Delta_{K}.
(E.2)
Explicitly, the probability assigned to a category
c
∈
[
K
]
c\in[K]
is:
π
x
(
c
)
=
(
B
x
♯
p
x
)
(
c
)
=
Pr
z
∼
p
θ
(
⋅
∣
x
)
[
B
x
(
z
)
=
c
]
=
∑
z
:
B
x
​
(
z
)
=
c
p
θ
(
z
∣
x
)
.
\pi_{x}(c)=\left(B_{x}\sharp p_{x}\right)(c)=\Pr_{z\sim p_{\theta}(\cdot\mid x)}\left[B_{x}(z)=c\right]=\sum_{z:B_{x}(z)=c}p_{\theta}(z\mid x).
(E.3)
Definitions
In the main text, we defined confidence calibration and
B
B
-confidence calibration via
Definition
1
and
Definition
2
. We formally restate these definitions below.
Definition 26
(Confidence Calibration)
.
A distribution
𝒟
\mathcal{D}
over prediction-output pairs
(
c
,
y
)
∈
Δ
K
×
ℰ
K
(c,y)\in\Delta_{K}\times\mathcal{E}_{K}
is perfectly confidence-calibrated if, conditioned on the model’s top predicted probability, that probability matches the expected outcome. Formally,
𝔼
(
c
,
y
)
∼
𝒟
[
y
k
⋆
−
c
k
⋆
∣
c
k
⋆
]
≡
0
​
where
​
k
⋆
=
argmax
k
∈
[
K
]
c
k
.
\mathop{\mathbb{E}}_{(c,y)\sim\mathcal{D}}\left[y_{k^{\star}}-c_{k^{\star}}\mid c_{k^{\star}}\right]\equiv 0\text{ where }k^{\star}=\argmax_{k\in[K]}c_{k}.
(E.4)
Applying to our LLM setting, we say that a model is
B
B
-confidence-calibrated if the categorical distribution it induces is confidence-calibrated:
Definition 27
(
B
B
-Confidence-Calibration)
.
A model
p
θ
p_{\theta}
is
B
B
-confidence-calibrated on a distribution
𝒟
\mathcal{D}
if the induced distribution over pairs
(
π
x
,
B
x
​
(
y
)
)
(\pi_{x},B_{x}(y))
is perfectly
confidence-calibrated according to Definition
26
.
This requires that, for
k
⋆
=
argmax
k
∈
[
K
]
π
x
​
(
k
)
k^{\star}=\argmax_{k\in[K]}\pi_{x}(k)
,
𝔼
(
x
,
y
)
∼
𝒟
[
𝟙
{
B
x
(
y
)
=
k
⋆
}
−
π
x
(
k
⋆
)
|
π
x
(
k
⋆
)
]
=
0
.
\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}\left[\mathds{1}\{B_{x}(y)=k^{\star}\}-\pi_{x}(k^{\star})\;\middle|\;\pi_{x}(k^{\star})\right]=0.
(E.5)
We also restate
Definition
6
here for convenience:
Definition 28
(Semantic Perturbation Function Classes)
.
Given an arbitrary collapsing function
B
x
​
(
z
)
∈
[
K
]
B_{x}(z)\in[K]
, we define the class
𝒲
B
\mathcal{W}_{B}
of perturbation functions
w
⁡
(
x
,
p
x
)
∈
ℝ
|
𝒱
N
|
w(x,p_{x})\in\mathbb{R}^{|\mathcal{V}^{N}|}
as follows.
These functions generate a perturbation vector based on the prompt
x
x
and the
model’s predictive distribution
p
x
p_{x}
:
𝒲
B
:=
{
w
|
\displaystyle\mathcal{W}_{B}:=\Big\{w\;\Big|\;
∃
τ
:
[
0
,
1
]
→
[
−
1
,
1
]
∀
z
∈
𝒱
N
:
w
(
x
,
p
x
)
[
z
]
=
τ
(
π
x
(
k
⋆
)
)
⋅
𝟙
{
B
x
(
z
)
=
k
⋆
}
}
,
\displaystyle\exists\tau:[0,1]\to[-1,1]\;\;\penalty\ \forall z\in\mathcal{V}^{N}:\;w(x,p_{x})[z]=\tau\big(\pi_{x}(k^{\star})\big)\cdot\mathds{1}\{B_{x}(z)=k^{\star}\}\Big\},
where
​
π
x
:=
B
x
​
♯
​
p
x
,
k
⋆
:=
argmax
k
∈
[
K
]
π
x
​
(
k
)
.
\displaystyle\text{where }\pi_{x}:=B_{x}\sharp p_{x},\quad k^{\star}:=\argmax_{k\in[K]}\pi_{x}(k).
Equivalence Theorem
Using the above definitions, we have the following equivalence.
Theorem 29
(B-Confidence-Calibration as Weighted Calibration)
.
A model
p
θ
p_{\theta}
is perfectly
B
B
-confidence-calibrated
if and only if it is perfectly
𝒲
B
\mathcal{W}_{B}
-weighted-calibrated.
Proof.
The model is
𝒲
B
\mathcal{W}_{B}
-weighted-calibrated if, for all
w
∈
𝒲
B
w\in\mathcal{W}_{B}
, the following holds:
𝔼
(
x
,
y
)
∼
𝒟
[
⟨
y
~
−
p
x
,
w
⁡
(
x
,
p
x
)
⟩
]
=
0
.
\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}\left[\langle\tilde{y}-p_{x},w(x,p_{x})\rangle\right]=0.
For a given
w
w
defined by a function
τ
:
[
0
,
1
]
→
[
−
1
,
1
]
\tau:[0,1]\to[-1,1]
, since
y
~
\tilde{y}
is a one-hot vector with a
1
1
in the coordinate
z
=
y
z=y
, the first term evaluates to
⟨
y
~
,
w
⁡
(
x
,
p
x
)
⟩
=
∑
z
y
~
​
[
z
]
​
w
​
(
x
,
p
x
)
​
[
z
]
=
w
⁡
(
x
,
p
x
)
​
[
y
]
,
\langle\tilde{y},w(x,p_{x})\rangle=\sum_{z}\tilde{y}[z]\,w(x,p_{x})[z]=w(x,p_{x})[y],
(E.6)
Substituting the definition of
w
w
:
w
(
x
,
p
x
)
[
y
]
=
τ
(
v
x
⋆
)
⋅
𝟙
{
B
x
(
y
)
=
k
⋆
}
where
v
x
⋆
:=
π
x
(
k
⋆
)
.
w(x,p_{x})[y]=\tau\left(v_{x}^{\star}\right)\cdot\mathds{1}_{\{B_{x}(y)=k^{\star}\}}\text{ where }v_{x}^{\star}:=\pi_{x}(k^{\star}).
The second term is
⟨
p
x
,
w
⁡
(
x
,
p
x
)
⟩
=
∑
z
p
x
​
(
z
)
​
w
​
(
x
,
p
x
)
​
[
z
]
\langle p_{x},w(x,p_{x})\rangle=\sum_{z}p_{x}(z)w(x,p_{x})[z]
. Substituting the definition of
w
w
:
∑
z
p
x
​
(
z
)
​
w
​
(
x
,
p
x
)
​
[
z
]
\displaystyle\sum_{z}p_{x}(z)w(x,p_{x})[z]
=
∑
z
p
x
(
z
)
(
τ
(
v
x
⋆
)
⋅
𝟙
{
B
x
(
z
)
=
k
⋆
}
)
\displaystyle=\sum_{z}p_{x}(z)\left(\tau\left(v_{x}^{\star}\right)\cdot\mathds{1}_{\{B_{x}(z)=k^{\star}\}}\right)
=
τ
(
v
x
⋆
)
⋅
∑
z
p
x
(
z
)
𝟙
{
B
x
(
z
)
=
k
⋆
}
\displaystyle=\tau\left(v_{x}^{\star}\right)\cdot\sum_{z}p_{x}(z)\mathds{1}_{\{B_{x}(z)=k^{\star}\}}
=
τ
(
v
x
⋆
)
⋅
Pr
[
B
x
(
z
)
=
k
⋆
]
=
τ
(
v
x
⋆
)
⋅
v
x
⋆
\displaystyle=\tau\left(v_{x}^{\star}\right)\cdot\Pr[B_{x}(z)=k^{\star}]=\tau\left(v_{x}^{\star}\right)\cdot v_{x}^{\star}
Putting these together, the weighted calibration condition becomes:
𝔼
(
x
,
y
)
∼
𝒟
[
τ
(
v
x
⋆
)
⋅
𝟙
{
B
x
(
y
)
=
k
⋆
}
−
τ
(
v
x
⋆
)
⋅
v
x
⋆
]
=
0
⟺
𝔼
(
x
,
y
)
∼
𝒟
[
τ
(
v
x
⋆
)
⋅
(
𝟙
{
B
x
(
y
)
=
k
⋆
}
−
v
x
⋆
)
]
=
0
.
\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}\left[\tau\left(v_{x}^{\star}\right)\cdot\mathds{1}_{\{B_{x}(y)=k^{\star}\}}-\tau\left(v_{x}^{\star}\right)\cdot v_{x}^{\star}\right]=0\Longleftrightarrow\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}\left[\tau\left(v_{x}^{\star}\right)\cdot\left(\mathds{1}_{\{B_{x}(y)=k^{\star}\}}-v_{x}^{\star}\right)\right]=0.
This condition must hold for all functions
τ
:
[
0
,
1
]
→
[
−
1
,
1
]
\tau:[0,1]\to[-1,1]
. By the properties of conditional expectation, this is true if and only if the term being multiplied by the arbitrary function of
v
x
⋆
v_{x}^{\star}
has a conditional expectation of zero. This gives us:
𝔼
[
𝟙
{
B
x
(
y
)
=
k
⋆
}
−
v
x
⋆
∣
v
x
⋆
]
=
0
,
\mathop{\mathbb{E}}\left[\mathds{1}_{\{B_{x}(y)=k^{\star}\}}-v_{x}^{\star}\mid v_{x}^{\star}\right]=0,
which is precisely the definition of
B
B
-confidence-calibration.
∎
E.5
Proof of
Thm.
7
We can now combine the above ingredients to
directly prove
Thm.
7
from the main body.
Proof.
Recall we have a model
p
θ
p_{\theta}
, a collapsing function
B
B
, and a distribution
𝒟
\mathcal{D}
.
We have the following equivalences:
p
θ
p_{\theta}
is
B
B
-confidence-calibrated on
𝒟
\mathcal{D}
⇔
p
θ
is
𝒲
B
-weighted-calibrated on
𝒟
\displaystyle\iff\textrm{$p_{\theta}$ is $\mathcal{W}_{B}$-weighted-calibrated on $\mathcal{D}$}
(by
Thm.
29
)
⇔
p
θ
is
𝒲
B
-locally-loss-optimal on
𝒟
\displaystyle\iff\textrm{$p_{\theta}$ is $\mathcal{W}_{B}$-locally-loss-optimal on $\mathcal{D}$}
(by
Thm.
25
)
∎
E.6
Proof of
Thm.
10
:
A Simple Circuit for B-Confidence-Perturbations
Recall
Definition
3
of the perturbation operator:
∀
z
∈
𝒱
N
:
(
f
⋆
w
)
[
z
]
\displaystyle\penalty\ \forall z\in\mathcal{V}^{N}:\quad(f\star w)[z]
:
=
softmax
⁡
(
w
⁡
[
z
]
+
log
⁡
f
⁡
[
z
]
)
=
f
⁡
[
z
]
​
exp
⁡
(
w
⁡
[
z
]
)
∑
z
′
∈
𝒱
N
f
⁡
[
z
′
]
​
exp
⁡
(
w
⁡
[
z
′
]
)
\displaystyle:=\mathrm{softmax}\big(w[z]+\log f[z]\big)=\frac{f[z]\exp(w[z])}{\sum_{z^{\prime}\in\mathcal{V}^{N}}f[z^{\prime}]\exp(w[z^{\prime}])}
(E.7)
which highlights that this transformation is a multiplicative reweighting of the reference distribution
f
f
by
e
w
⁡
[
z
]
e^{w[z]}
, followed by a renormalization to get a valid distribution. We will show that perturbations of this form can be implemented autoregressively via a small, efficient arithmetic circuit.
The key is to define two “intermediate top-1 confidence” vectors that can be tracked during generation.
Definition 30
(Intermediate Top-1 Confidence)
.
Given a model
p
x
p_{x}
and mapping
B
x
B_{x}
, let
π
x
=
B
x
​
♯
​
p
x
\pi_{x}=B_{x}\sharp p_{x}
be the initial categorical distribution, and let
k
⋆
:=
argmax
k
∈
[
K
]
⁡
(
π
x
)
k
k^{\star}:=\operatorname{argmax}_{k\in[K]}(\pi_{x})_{k}
be the single most likely category. We define:
1.
The top confidence value
v
x
⋆
∈
[
0
,
1
]
v_{x}^{\star}\in[0,1]
, which is the model’s confidence in this top category:
v
x
⋆
:=
(
π
x
)
k
⋆
.
v_{x}^{\star}:=(\pi_{x})_{k^{\star}}.
(E.8)
2.
The conditional probability of hitting the top category,
g
i
(
conf
)
​
(
x
,
z
≤
i
)
∈
[
0
,
1
]
g_{i}^{(\mathrm{conf})}(x,z_{\leq i})\in[0,1]
, which is the probability of eventually generating a sequence in category
k
⋆
k^{\star}
, given the prefix
z
≤
i
z_{\leq i}
:
g
i
(
conf
)
(
x
,
z
≤
i
)
:=
Pr
z
′
∼
p
x
(
⋅
∣
z
≤
i
)
[
B
x
(
z
≤
i
,
z
′
)
=
k
⋆
]
.
g_{i}^{(\mathrm{conf})}(x,z_{\leq i}):=\Pr_{z^{\prime}\sim p_{x}(\cdot\mid z_{\leq i})}[B_{x}(z_{\leq i},z^{\prime})=k^{\star}].
(E.9)
With these scalars, the autoregressive update becomes a simple linear transformation.
Theorem 31
.
For any perturbation
w
∈
𝒲
B
w\in\mathcal{W}_{B}
(defined by a function
τ
\tau
), the perturbed next-token probability is proportional to the original probability modified by a simple scalar circuit
C
w
C_{w}
:
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
∝
p
x
​
(
z
i
∣
z
<
i
)
⋅
C
w
​
(
v
x
⋆
,
g
i
(
conf
)
​
(
x
,
z
≤
i
)
)
,
(p_{x}\star w_{x})(z_{i}\mid z_{<i})\propto p_{x}(z_{i}\mid z_{<i})\cdot C_{w}(v_{x}^{\star},g_{i}^{(\mathrm{conf})}(x,z_{\leq i})),
(E.10)
where the circuit
C
w
C_{w}
is a linear function of
g
i
(
conf
)
g_{i}^{(\mathrm{conf})}
:
C
w
​
(
v
,
g
)
:=
1
+
(
exp
⁡
(
τ
⁡
(
v
)
)
−
1
)
×
g
.
C_{w}(v,g):=1+\left(\exp(\tau(v))-1\right)\times g.
(E.11)
The following helper lemma will assist with the proof of
Thm.
31
:
Lemma 32
(Autoregressive Decomposition of the Perturbation)
.
For any position
i
i
, the perturbed conditional probability of the next token is the original conditional probability multiplied by a ratio of
“lookahead expectations”:
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
=
p
x
​
(
z
i
∣
z
<
i
)
⋅
𝔼
z
>
i
∼
p
x
(
⋅
∣
z
≤
i
)
[
exp
(
w
x
(
z
≤
i
,
z
>
i
)
)
]
𝔼
z
≥
i
∼
p
x
(
⋅
∣
z
<
i
)
[
exp
(
w
x
(
z
<
i
,
z
≥
i
)
)
]
.
(p_{x}\star w_{x})(z_{i}\mid z_{<i})=p_{x}(z_{i}\mid z_{<i})\cdot\frac{\mathop{\mathbb{E}}_{z_{>i}\sim p_{x}(\cdot\mid z_{\leq i})}\!\big[\exp(w_{x}(z_{\leq i},z_{>i}))\big]}{\mathop{\mathbb{E}}_{z_{\geq i}\sim p_{x}(\cdot\mid z_{<i})}\!\big[\exp(w_{x}(z_{<i},z_{\geq i}))\big]}.
(E.12)
Proof.
Let
Z
:=
∑
z
p
x
​
(
z
)
​
e
w
x
​
(
z
)
Z:=\sum_{z}p_{x}(z)\,e^{w_{x}(z)}
. By definition of conditional probability,
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
=
(
p
x
⋆
w
x
)
​
(
z
≤
i
)
(
p
x
⋆
w
x
)
​
(
z
<
i
)
.
(p_{x}\star w_{x})(z_{i}\mid z_{<i})=\frac{(p_{x}\star w_{x})(z_{\leq i})}{(p_{x}\star w_{x})(z_{<i})}.
(E.13)
Expanding the perturbation operator and applying
p
x
​
(
z
≤
i
,
z
>
i
)
=
p
x
​
(
z
≤
i
)
​
p
x
​
(
z
>
i
∣
z
≤
i
)
p_{x}(z_{\leq i},z_{>i})=p_{x}(z_{\leq i})p_{x}(z_{>i}\mid z_{\leq i})
,
(
p
x
⋆
w
x
)
​
(
z
≤
i
)
\displaystyle(p_{x}\star w_{x})(z_{\leq i})
=
1
Z
​
∑
z
>
i
p
x
​
(
z
≤
i
,
z
>
i
)
​
e
w
x
​
(
z
≤
i
,
z
>
i
)
\displaystyle=\frac{1}{Z}\sum_{z_{>i}}p_{x}(z_{\leq i},z_{>i})\,e^{w_{x}(z_{\leq i},z_{>i})}
=
p
x
​
(
z
≤
i
)
Z
𝔼
z
>
i
∼
p
x
(
⋅
∣
z
≤
i
)
[
e
w
x
​
(
z
≤
i
,
z
>
i
)
]
.
\displaystyle=\frac{p_{x}(z_{\leq i})}{Z}\,\mathop{\mathbb{E}}_{z_{>i}\sim p_{x}(\cdot\mid z_{\leq i})}[e^{w_{x}(z_{\leq i},z_{>i})}].
Similarly,
(
p
x
⋆
w
x
)
(
z
<
i
)
=
p
x
​
(
z
<
i
)
Z
𝔼
z
≥
i
∼
p
x
(
⋅
∣
z
<
i
)
[
e
w
x
​
(
z
<
i
,
z
≥
i
)
]
.
(p_{x}\star w_{x})(z_{<i})=\frac{p_{x}(z_{<i})}{Z}\,\mathop{\mathbb{E}}_{z_{\geq i}\sim p_{x}(\cdot\mid z_{<i})}[e^{w_{x}(z_{<i},z_{\geq i})}].
(E.14)
Taking the ratio and canceling
Z
Z
,
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
\displaystyle(p_{x}\star w_{x})(z_{i}\mid z_{<i})
=
p
x
​
(
z
≤
i
)
p
x
​
(
z
<
i
)
⋅
𝔼
z
>
i
∼
p
x
(
⋅
∣
z
≤
i
)
[
e
w
x
​
(
z
≤
i
,
z
>
i
)
]
𝔼
z
≥
i
∼
p
x
(
⋅
∣
z
<
i
)
[
e
w
x
​
(
z
<
i
,
z
≥
i
)
]
\displaystyle=\frac{p_{x}(z_{\leq i})}{p_{x}(z_{<i})}\cdot\frac{\mathop{\mathbb{E}}_{z_{>i}\sim p_{x}(\cdot\mid z_{\leq i})}[e^{w_{x}(z_{\leq i},z_{>i})}]}{\mathop{\mathbb{E}}_{z_{\geq i}\sim p_{x}(\cdot\mid z_{<i})}[e^{w_{x}(z_{<i},z_{\geq i})}]}
=
p
x
​
(
z
i
∣
z
<
i
)
⋅
𝔼
z
>
i
∼
p
x
(
⋅
∣
z
≤
i
)
[
e
w
x
​
(
z
≤
i
,
z
>
i
)
]
𝔼
z
≥
i
∼
p
x
(
⋅
∣
z
<
i
)
[
e
w
x
​
(
z
<
i
,
z
≥
i
)
]
.
\displaystyle=p_{x}(z_{i}\mid z_{<i})\cdot\frac{\mathop{\mathbb{E}}_{z_{>i}\sim p_{x}(\cdot\mid z_{\leq i})}[e^{w_{x}(z_{\leq i},z_{>i})}]}{\mathop{\mathbb{E}}_{z_{\geq i}\sim p_{x}(\cdot\mid z_{<i})}[e^{w_{x}(z_{<i},z_{\geq i})}]}.
∎
Now we can proceed with the proof of
Thm.
31
.
Proof.
(
Thm.
31
)
By Lemma
32
,
(
p
x
⋆
w
x
)
(
z
i
∣
z
<
i
)
∝
p
x
(
z
i
∣
z
<
i
)
⋅
𝔼
z
∼
p
x
(
⋅
∣
z
≤
i
)
[
exp
(
w
x
(
z
)
)
]
.
(p_{x}\star w_{x})(z_{i}\mid z_{<i})\;\propto\;p_{x}(z_{i}\mid z_{<i})\cdot\mathop{\mathbb{E}}_{z\sim p_{x}(\cdot\mid z_{\leq i})}\big[\exp(w_{x}(z))\big].
(E.15)
For
w
∈
𝒲
B
w\in\mathcal{W}_{B}
we have
w
x
​
(
z
)
\displaystyle w_{x}(z)
=
c
x
⋅
𝟙
{
B
x
(
z
)
=
k
⋆
}
,
with
c
x
:=
τ
(
v
x
⋆
)
.
\displaystyle=c_{x}\cdot\mathds{1}\{B_{x}(z)=k^{\star}\},\quad\text{with }c_{x}:=\tau(v_{x}^{\star}).
exp
⁡
(
w
x
​
(
z
)
)
\displaystyle\exp(w_{x}(z))
=
1
+
(
exp
(
c
x
)
−
1
)
⋅
𝟙
{
B
x
(
z
)
=
k
⋆
}
.
\displaystyle=1+(\exp(c_{x})-1)\cdot\mathds{1}\{B_{x}(z)=k^{\star}\}.
Taking expectation under
z
∼
p
x
(
⋅
∣
z
≤
i
)
z\sim p_{x}(\cdot\mid z_{\leq i})
yields
1
+
(
exp
⁡
(
c
x
)
−
1
)
​
Pr
⁡
[
B
x
​
(
z
)
=
k
⋆
∣
z
≤
i
]
=
1
+
(
exp
⁡
(
τ
⁡
(
v
x
⋆
)
)
−
1
)
​
g
i
(
conf
)
​
(
x
,
z
≤
i
)
.
1+(\exp(c_{x})-1)\,\Pr[B_{x}(z)=k^{\star}\mid z_{\leq i}]=1+(\exp(\tau(v_{x}^{\star}))-1)\,g_{i}^{(\mathrm{conf})}(x,z_{\leq i}).
(E.16)
By Lemma
32
, the perturbed conditional
probability is the original
p
x
​
(
z
i
∣
z
<
i
)
p_{x}(z_{i}\mid z_{<i})
scaled by the ratio of this term to an analogous denominator depending only on
the prefix
z
<
i
z_{<i}
. Since the denominator is independent of
z
i
z_{i}
, it can be absorbed
into the overall proportionality constant.
∎
E.7
Full calibration
In this section, we provide
full calibration
analogs of our confidence-calibration results.
Confidence calibration is a weaker form of calibration that focuses only on the model’s top prediction, while full calibration is a stronger notion that considers the probability placed on all classes. We begin by defining full calibration and applying it to the LLM setting to define
B
B
-calibration
.
Definition 33
(Full Calibration)
.
A distribution
𝒟
\mathcal{D}
over prediction-output pairs
(
c
,
y
)
∈
Δ
K
×
ℰ
K
(c,y)\in\Delta_{K}\times\mathcal{E}_{K}
is perfectly calibrated if the expected error, conditioned on the prediction, is the zero vector:
𝔼
(
c
,
y
)
∼
𝒟
[
y
−
c
∣
c
]
≡
0
.
\mathop{\mathbb{E}}_{(c,y)\sim\mathcal{D}}\left[y-c\mid c\right]\equiv 0.
(E.17)
Note that since
y
y
and
c
c
are both vectors in
ℝ
K
\mathbb{R}^{K}
, this subtraction is well-defined.
Now, we apply this template to our LLM setting. We say a model is
B
B
-calibrated if the distribution it induces over the collapsed, semantic categories is itself perfectly calibrated.
Definition 34
(
B
B
-Calibration)
.
A model
p
θ
p_{\theta}
is
B
B
-calibrated on a distribution
𝒟
\mathcal{D}
if the induced distribution over pairs
(
π
x
,
B
x
​
(
y
)
)
(\pi_{x},B_{x}(y))
is perfectly calibrated according to Definition
33
. Here,
π
x
=
B
x
​
♯
​
p
x
\pi_{x}=B_{x}\sharp p_{x}
takes the role of the prediction
c
c
, and the ground-truth category
B
x
​
(
y
)
∈
[
K
]
B_{x}(y)\in[K]
takes the role of the outcome
y
y
. Formally,
𝔼
(
x
,
y
)
∼
𝒟
[
B
x
​
(
y
)
−
π
x
∣
π
x
]
≡
0
.
\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}\left[B_{x}(y)-\pi_{x}\mid\pi_{x}\right]\equiv 0.
(E.18)
Following our convention, the scalar
B
x
​
(
y
)
∈
[
K
]
B_{x}(y)\in[K]
is identified with its one-hot vector in
ℰ
K
\mathcal{E}_{K}
to perform the vector subtraction.
Collapsing matrix
To help with the remaining statements and proofs in this section we introduce a matrix representation of the collapsing function
B
B
. Recall from
Eq.
E.3
that
π
x
\pi_{x}
assigns the explicit probabilities
π
x
(
c
)
=
(
B
x
♯
p
x
)
(
c
)
=
Pr
z
∼
p
θ
(
⋅
∣
x
)
[
B
x
(
z
)
=
c
]
=
∑
z
:
B
x
​
(
z
)
=
c
p
θ
(
z
∣
x
)
,
for each
c
∈
[
K
]
.
\pi_{x}(c)=\left(B_{x}\sharp p_{x}\right)(c)=\Pr_{z\sim p_{\theta}(\cdot\mid x)}\left[B_{x}(z)=c\right]=\sum_{z:B_{x}(z)=c}p_{\theta}(z\mid x),\quad\text{for each $c\in[K]$.}
This push-forward operation can be written in matrix form.
Define the collapsing matrix
𝐁
x
\mathbf{B}_{x}
as:
𝐁
x
∈
{
0
,
1
}
K
×
M
,
[
𝐁
x
]
k
,
z
=
𝟙
{
B
x
(
z
)
=
k
}
.
\mathbf{B}_{x}\in\{0,1\}^{K\times M},\qquad[\mathbf{B}_{x}]_{k,z}=\mathds{1}_{\{B_{x}(z)=k\}}.
(E.19)
Then the pushforward distribution and ground-truth semantic class can be
expressed as
π
x
=
𝐁
x
​
p
x
∈
Δ
K
,
𝐁
x
​
y
~
=
e
B
x
​
(
y
)
∈
ℰ
K
.
\pi_{x}=\mathbf{B}_{x}p_{x}\in\Delta_{K},\qquad\mathbf{B}_{x}\tilde{y}=e_{B_{x}(y)}\in\mathcal{E}_{K}.
Thus, matrix-vector multiplication exactly implements the pushforward operation:
(
π
x
)
k
=
∑
z
:
B
x
​
(
z
)
=
k
p
θ
(
z
∣
x
)
=
[
𝐁
x
p
x
]
k
.
(\pi_{x})_{k}=\sum_{z:B_{x}(z)=k}p_{\theta}(z\mid x)=[\mathbf{B}_{x}p_{x}]_{k}.
(E.20)
E.7.1
Equivalence between
B
B
-calibration and weighted calibration
In this section, we provide a result analogous to
Thm.
29
connecting
B
B
-calibration with weighted calibration.
Definition 35
(Semantic Perturbation Function Classes; Full Calibration)
.
Given an arbitrary function
B
x
​
(
z
)
∈
[
K
]
B_{x}(z)\in[K]
, which we think of as a semantic
collapsing function,
we define the
B
B
-induced weighted function class (a class of perturbation functions
w
⁡
(
x
,
p
x
)
w(x,p_{x})
that generate a perturbation vector based on the context
x
x
and the model’s predictive distribution
p
x
p_{x}
):
𝒲
B
(
full
)
=
{
w
τ
∣
w
τ
(
x
,
p
x
)
[
z
]
=
τ
(
π
x
)
[
B
x
(
z
)
]
for some
τ
:
Δ
K
→
[
−
1
,
1
]
K
}
.
\mathcal{W}_{B}^{\rm{(full)}}=\left\{w_{\tau}\mid w_{\tau}(x,p_{x})[z]=\tau(\pi_{x})[B_{x}(z)]\text{ for some }\tau:\Delta^{K}\to[-1,1]^{K}\right\}.
(E.21)
Intuitively, every sequence
z
z
is assigned a weight based on its semantic category
B
x
​
(
z
)
∈
[
K
]
B_{x}(z)\in[K]
, and the weighting scheme itself can adapt based on the model’s overall categorical prediction
π
x
\pi_{x}
.
Lemma 36
.
Let
w
∈
𝒲
B
(
full
)
w\in\mathcal{W}_{B}^{\rm{(full)}}
be a weight function defined by
w
⁡
(
x
,
p
x
)
​
[
z
]
=
τ
⁡
(
π
x
)
​
[
B
x
​
(
z
)
]
w(x,p_{x})[z]=\tau(\pi_{x})[B_{x}(z)]
. Its corresponding vector representation is given by
𝐁
x
⊤
​
τ
​
(
π
x
)
\mathbf{B}_{x}^{\top}\tau(\pi_{x})
.
Proof.
We will prove the equivalence by showing that for any sequence
z
∈
𝒱
N
z\in\mathcal{V}^{N}
, the
z
z
-th component of the vector
𝐁
x
⊤
​
τ
​
(
π
x
)
\mathbf{B}_{x}^{\top}\tau(\pi_{x})
is equal to
τ
⁡
(
π
x
)
​
[
B
x
​
(
z
)
]
\tau(\pi_{x})[B_{x}(z)]
. Let
u
=
τ
⁡
(
π
x
)
u=\tau(\pi_{x})
, which is a vector in
ℝ
K
\mathbb{R}^{K}
.
Now, we want to analyze the components of the vector
v
=
𝐁
x
⊤
​
u
v=\mathbf{B}_{x}^{\top}u
.
For any
z
∈
𝒱
N
z\in\mathcal{V}^{N}
, the
z
z
-th component of
v
v
is given by the definition of matrix-vector multiplication:
[
v
]
z
\displaystyle[v]_{z}
=
[
𝐁
x
⊤
u
]
z
=
∑
k
=
1
K
[
𝐁
x
⊤
]
z
,
k
⋅
u
k
=
∑
k
=
1
K
[
𝐁
x
]
k
,
z
⋅
u
k
=
∑
k
=
1
K
𝟙
{
B
x
(
z
)
=
k
}
⋅
u
k
\displaystyle=[\mathbf{B}_{x}^{\top}u]_{z}=\sum_{k=1}^{K}[\mathbf{B}_{x}^{\top}]_{z,k}\cdot u_{k}=\sum_{k=1}^{K}[\mathbf{B}_{x}]_{k,z}\cdot u_{k}=\sum_{k=1}^{K}\mathds{1}_{\{B_{x}(z)=k\}}\cdot u_{k}
where the last equality is by definition of
𝐁
x
\mathbf{B}_{x}
; see
Eq.
E.19
.
The indicator function
𝟙
{
B
x
(
z
)
=
k
}
\mathds{1}_{\{B_{x}(z)=k\}}
is non-zero for only one value of
k
k
in the sum, namely when
k
k
is equal to the category of the sequence
z
z
, i.e.,
k
=
B
x
​
(
z
)
k=B_{x}(z)
. Therefore, the sum collapses to a single term:
[
v
]
z
\displaystyle[v]_{z}
=
1
⋅
u
B
x
​
(
z
)
+
∑
B
x
​
(
z
)
≠
k
0
⋅
u
k
=
u
B
x
​
(
z
)
.
\displaystyle=1\cdot u_{B_{x}(z)}+\sum_{B_{x}(z)\neq k}0\cdot u_{k}=u_{B_{x}(z)}.
Substituting back the definition of
u
=
τ
⁡
(
π
x
)
u=\tau(\pi_{x})
, we get:
[
v
]
z
=
τ
⁡
(
π
x
)
​
[
B
x
​
(
z
)
]
[v]_{z}=\tau(\pi_{x})[B_{x}(z)]
.
This expression matches the definition of
w
​
(
x
,
p
x
)
​
[
z
]
w(x,p_{x})[z]
exactly.
Since this holds for all sequences
z
z
, the vector
𝐁
x
⊤
​
τ
​
(
π
x
)
\mathbf{B}_{x}^{\top}\tau(\pi_{x})
is the vector representation of the function
w
⁡
(
x
,
p
x
)
w(x,p_{x})
.
∎
With the definition of the weighted class and its vector representation, we can state the main equivalence theorem (analogous to
Thm.
29
).
Theorem 37
(B-Calibration as Weighted Calibration)
.
A model
p
θ
p_{\theta}
is perfectly
B
B
-calibrated if and only if it is perfectly
𝒲
B
(
full
)
\mathcal{W}_{B}^{\rm{(full)}}
-weighted-calibrated.
Proof.
We start from the definition of
B
B
-calibration, which (as established in Definition
33
) is formally expressed as a vector condition:
𝔼
[
e
B
x
​
(
y
)
−
π
x
∣
π
x
]
=
0
.
\mathop{\mathbb{E}}\left[e_{B_{x}(y)}-\pi_{x}\mid\pi_{x}\right]=0.
By the properties of conditional expectation, this holds if and only if for all functions
τ
:
Δ
K
→
[
−
1
,
1
]
K
\tau:\Delta_{K}\to[-1,1]^{K}
, it holds
𝔼
[
⟨
e
B
x
​
(
y
)
−
π
x
,
τ
⁡
(
π
x
)
⟩
]
=
0
.
\mathop{\mathbb{E}}\left[\langle e_{B_{x}(y)}-\pi_{x},\tau(\pi_{x})\rangle\right]=0.
(E.22)
Substituting the matrix representation into
Eq.
E.22
:
𝔼
[
⟨
e
B
x
​
(
y
)
−
π
x
,
τ
⁡
(
π
x
)
⟩
]
=
0
\displaystyle\mathop{\mathbb{E}}\left[\langle e_{B_{x}(y)}-\pi_{x},\tau(\pi_{x})\rangle\right]=0
⇔
𝔼
[
⟨
𝐁
x
​
y
~
−
𝐁
x
​
p
x
,
τ
⁡
(
𝐁
x
​
p
x
)
⟩
]
=
0
\displaystyle\iff\mathop{\mathbb{E}}\left[\langle\mathbf{B}_{x}\tilde{y}-\mathbf{B}_{x}p_{x},\tau(\mathbf{B}_{x}p_{x})\rangle\right]=0
⇔
𝔼
[
⟨
𝐁
x
(
y
~
−
p
x
)
,
τ
(
𝐁
x
p
x
)
⟩
]
=
0
\displaystyle\iff\quad\mathop{\mathbb{E}}\left[\langle\mathbf{B}_{x}(\tilde{y}-p_{x}),\tau(\mathbf{B}_{x}p_{x})\rangle\right]=0
⇔
𝔼
[
⟨
y
~
−
p
x
,
𝐁
x
⊤
τ
(
𝐁
x
p
x
)
⟩
]
=
0
\displaystyle\iff\quad\mathop{\mathbb{E}}\left[\langle\tilde{y}-p_{x},\mathbf{B}_{x}^{\top}\tau(\mathbf{B}_{x}p_{x})\rangle\right]=0
From
Lemma
36
, the term
𝐁
x
⊤
​
τ
​
(
𝐁
x
​
p
x
)
\mathbf{B}_{x}^{\top}\tau(\mathbf{B}_{x}p_{x})
is precisely the vector representation of the function
w
⁡
(
x
,
p
x
)
w(x,p_{x})
from
Definition
35
. Thus, the condition is equivalent to:
𝔼
[
⟨
y
~
−
p
x
,
w
⁡
(
x
,
p
x
)
⟩
]
=
0
,
for all
​
w
∈
𝒲
B
(
full
)
,
\mathop{\mathbb{E}}\left[\langle\tilde{y}-p_{x},w(x,p_{x})\rangle\right]=0,\quad\text{for all }w\in\mathcal{W}_{B}^{\rm{(full)}},
which is exactly the definition of
𝒲
B
(
full
)
\mathcal{W}_{B}^{\rm{(full)}}
-weighted-calibration ; see
Definition
23
.
∎
E.7.2
A Simple Circuit for
B
B
-Perturbations
Given a model
p
x
p_{x}
and a semantic mapping
B
x
B_{x}
, we define two “intermediate B-confidence” vectors as follows:
1.
The initial B-confidence
g
0
​
(
x
)
∈
Δ
K
g_{0}(x)\in\Delta_{K}
, which is the model’s overall predicted distribution on the
K
K
categories before generation begins. This corresponds to the
B
B
-induced pushforward distribution
π
x
=
B
x
​
♯
​
p
x
\pi_{x}=B_{x}\sharp p_{x}
:
g
0
(
x
)
[
b
]
:=
Pr
z
∼
p
x
[
B
x
(
z
)
=
b
]
.
g_{0}(x)[b]:=\Pr_{z\sim p_{x}}[B_{x}(z)=b].
(E.23)
2.
The conditional B-confidence
g
i
​
(
x
,
z
≤
i
)
∈
Δ
K
g_{i}(x,z_{\leq i})\in\Delta_{K}
, which is the model’s predicted distribution on categories, conditioned on having generated the prefix
z
≤
i
z_{\leq i}
:
g
i
(
x
,
z
≤
i
)
[
b
]
:=
Pr
z
′
∼
p
x
(
⋅
∣
z
≤
i
)
[
B
x
(
z
≤
i
,
z
′
)
=
b
]
.
g_{i}(x,z_{\leq i})[b]:=\Pr_{z^{\prime}\sim p_{x}(\cdot\mid z_{\leq i})}[B_{x}(z_{\leq i},z^{\prime})=b].
(E.24)
Theorem 38
(Simple Circuit for B-Perturbations)
.
For any perturbation
w
∈
𝒲
B
w\in\mathcal{W}_{B}
(defined by a scaling function
τ
\tau
),
the perturbed next-token probability is proportional to the original conditional probability
multiplied by a simple circuit
C
w
C_{w}
:
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
∝
p
x
​
(
z
i
∣
z
<
i
)
⋅
C
w
​
(
g
0
​
(
x
)
,
g
i
​
(
x
,
z
≤
i
)
)
,
(p_{x}\star w_{x})(z_{i}\mid z_{<i})\propto p_{x}(z_{i}\mid z_{<i})\cdot C_{w}(g_{0}(x),g_{i}(x,z_{\leq i})),
(E.25)
where the constant of proportionality does not depend on
z
i
z_{i}
, and
C
w
​
(
g
0
,
g
i
)
=
∑
b
=
1
K
exp
⁡
(
τ
⁡
(
g
0
)
​
[
b
]
)
⋅
g
i
​
[
b
]
.
C_{w}(g_{0},g_{i})=\sum_{b=1}^{K}\exp(\tau(g_{0})[b])\cdot g_{i}[b].
(E.26)
This circuit has constant depth and width linear in
K
K
.
Proof.
From
Lemma
32
, we know that
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
=
p
x
​
(
z
i
∣
z
<
i
)
⋅
𝔼
z
∼
p
x
(
⋅
∣
z
≤
i
)
[
e
w
x
​
(
z
≤
i
,
z
)
]
𝔼
z
∼
p
x
(
⋅
∣
z
<
i
)
[
e
w
x
​
(
z
<
i
,
z
)
]
.
(p_{x}\star w_{x})(z_{i}\mid z_{<i})=p_{x}(z_{i}\mid z_{<i})\cdot\frac{\mathop{\mathbb{E}}_{z\sim p_{x}(\cdot\mid z_{\leq i})}[e^{w_{x}(z_{\leq i},z)}]}{\mathop{\mathbb{E}}_{z\sim p_{x}(\cdot\mid z_{<i})}[e^{w_{x}(z_{<i},z)}]}.
(E.27)
For
w
∈
𝒲
B
w\in\mathcal{W}_{B}
, by definition,
w
x
​
(
z
)
=
τ
⁡
(
g
0
​
(
x
)
)
​
[
B
x
​
(
z
)
]
where
g
0
​
(
x
)
=
B
x
​
♯
​
p
x
.
w_{x}(z)=\tau(g_{0}(x))[B_{x}(z)]\quad\text{where}\quad g_{0}(x)=B_{x}\sharp p_{x}.
Expanding the expectation,
𝔼
z
∼
p
x
(
⋅
∣
z
≤
i
)
[
e
w
x
​
(
z
≤
i
,
z
)
]
\displaystyle\mathop{\mathbb{E}}_{z\sim p_{x}(\cdot\mid z_{\leq i})}[e^{w_{x}(z_{\leq i},z)}]
=
𝔼
z
∼
p
x
(
⋅
∣
z
≤
i
)
[
e
τ
⁡
(
g
0
​
(
x
)
)
​
[
B
x
​
(
z
≤
i
,
z
)
]
]
\displaystyle=\mathop{\mathbb{E}}_{z\sim p_{x}(\cdot\mid z_{\leq i})}[e^{\tau(g_{0}(x))[B_{x}(z_{\leq i},z)]}]
=
∑
b
=
1
K
Pr
[
B
x
(
z
≤
i
,
z
)
=
b
]
⋅
e
τ
​
(
g
0
​
(
x
)
)
​
[
b
]
\displaystyle=\sum_{b=1}^{K}\Pr[B_{x}(z_{\leq i},z)=b]\cdot e^{\tau(g_{0}(x))[b]}
=
∑
b
=
1
K
g
i
​
(
x
,
z
≤
i
)
​
[
b
]
⋅
e
τ
​
(
g
0
​
(
x
)
)
​
[
b
]
.
\displaystyle=\sum_{b=1}^{K}g_{i}(x,z_{\leq i})[b]\cdot e^{\tau(g_{0}(x))[b]}.
The denominator is an expectation over
z
∼
p
x
(
⋅
|
z
<
i
)
z\sim p_{x}(\cdot|z_{<i})
,
which depends only on the prefix
z
<
i
z_{<i}
and not on the choice of
z
i
z_{i}
.
Hence it is a constant with respect to
z
i
z_{i}
and can be absorbed into the proportionality.
Therefore,
(
p
x
⋆
w
x
)
​
(
z
i
∣
z
<
i
)
∝
p
x
​
(
z
i
∣
z
<
i
)
⋅
⟨
exp
⁡
(
τ
⁡
(
g
0
​
(
x
)
)
)
,
g
i
​
(
x
,
z
≤
i
)
⟩
.
(p_{x}\star w_{x})(z_{i}\mid z_{<i})\propto p_{x}(z_{i}\mid z_{<i})\cdot\langle\exp(\tau(g_{0}(x))),g_{i}(x,z_{\leq i})\rangle.
∎
E.8
Quantitative Bounds on Multi-Class Calibration and Post-Processing Gap for Proper Losses
Beyond cross-entropy loss, we provide in this section a generalization for the class of proper loss functions and quantitative bounds relating post-processing and calibration gap.
The main result in this section,
Thm.
43
should be interpreted
as a generalization of Theorem E.3 in
Błasiok et al. (2023b)
to the multi-class setting, and a robust version of
Thm.
25
:
it essentially states that a model is “close to”
𝒲
\mathcal{W}
-weighted-calibrated
if it is “close to”
𝒲
\mathcal{W}
-loss-optimal.
First, we recall a standard result on convex representation of proper losses
(
Savage, 1971
;
Schervish, 1989
;
Gneiting and Raftery, 2007
)
.
Definition 39
(Savage representation)
.
A loss function
ℓ
:
{
e
1
,
…
,
e
K
}
×
Δ
K
→
ℝ
\ell:\{e_{1},\dots,e_{K}\}\times\Delta_{K}\to\mathbb{R}
is
proper
iff there exists a convex function
ϕ
:
Δ
K
→
ℝ
\phi:\Delta_{K}\to\mathbb{R}
such that
ℓ
⁡
(
y
,
v
)
=
−
ϕ
⁡
(
v
)
+
⟨
v
−
y
,
∇
ϕ
​
(
v
)
⟩
.
\ell(y,v)\;=\;-\phi(v)+\langle v-y,\nabla\phi(v)\rangle.
(E.28)
Next, define the convex conjugate
ψ
=
ϕ
∗
\psi=\phi^{*}
, a dual variable, and the dual form of the loss.
Definition 40
(Dual loss)
.
For a proper loss
ℓ
\ell
with potential
ϕ
\phi
as in
Definition
39
, define:
Convex conjugate:
ψ
⁡
(
u
)
:=
ϕ
∗
​
(
u
)
:=
sup
v
∈
Δ
K
(
⟨
u
,
v
⟩
−
ϕ
⁡
(
v
)
)
,
\displaystyle\psi(u):=\phi^{*}(u):=\sup\limits_{v\in\Delta_{K}}\big(\langle u,v\rangle-\phi(v)\big),
Dual variable:
dual
​
(
v
)
:=
∇
ϕ
​
(
v
)
,
\displaystyle\text{dual}(v):=\nabla\phi(v),
Dual loss:
ℓ
(
ψ
)
​
(
y
,
z
)
:=
ψ
⁡
(
z
)
−
⟨
y
,
z
⟩
.
\displaystyle\ell^{(\psi)}(y,z):=\psi(z)-\langle y,z\rangle.
Remark 41
.
The dual parameterization of
Definition
40
satisfies:
1.
Agreement between primal and dual losses:
ℓ
(
ψ
)
​
(
y
,
dual
​
(
v
)
)
=
ℓ
⁡
(
y
,
v
)
.
\ell^{(\psi)}(y,\text{dual}(v))=\ell(y,v).
2.
Probability
→
\to
dual map:
dual
​
(
v
)
=
∇
ϕ
​
(
v
)
\text{dual}(v)=\nabla\phi(v)
for all
v
∈
Δ
K
v\in\Delta_{K}
.
3.
Dual
→
\to
probability map:
v
=
∇
ψ
​
(
dual
​
(
v
)
)
v=\nabla\psi(\text{dual}(v))
for all
v
∈
Δ
K
v\in\Delta_{K}
.
Definition 42
(Generalized dual calibration and post-processing gap)
.
Let
𝒲
\mathcal{W}
be a class of functions
w
:
𝒳
×
ℝ
K
→
ℝ
K
w:\mathcal{X}\times\mathbb{R}^{K}\to\mathbb{R}^{K}
,
and let
𝒟
\mathcal{D}
be a distribution over
𝒳
×
{
e
1
,
…
,
e
K
}
\mathcal{X}\times\{e_{1},\dots,e_{K}\}
.
For a predictor
f
:
𝒳
→
Δ
K
f:\mathcal{X}\to\Delta_{K}
, let
g
:
𝒳
→
ℝ
K
g:\mathcal{X}\to\mathbb{R}^{K}
be its dual representation such that
f
⁡
(
x
)
=
∇
ψ
​
(
g
⁡
(
x
)
)
∀
x
∈
𝒳
.
f(x)=\nabla\psi(g(x))\quad\penalty\ \forall x\in\mathcal{X}.
(E.29)
Define for shorthand
Δ
⁡
(
w
)
:=
𝔼
(
x
,
y
)
∼
𝒟
​
[
⟨
y
−
f
⁡
(
x
)
,
w
⁡
(
x
,
g
⁡
(
x
)
)
⟩
]
,
ℒ
⁡
(
h
)
:=
𝔼
(
x
,
y
)
∼
𝒟
​
[
ℓ
(
ψ
)
​
(
y
,
h
⁡
(
x
)
)
]
.
\Delta(w):=\mathbb{E}_{(x,y)\sim\mathcal{D}}\big[\langle y-f(x),w(x,g(x))\rangle\big],\qquad\mathcal{L}(h):=\mathbb{E}_{(x,y)\sim\mathcal{D}}[\ell^{(\psi)}(y,h(x))].
(E.30)
•
The
dual calibration error
of
g
g
with respect to
𝒲
\mathcal{W}
is
CE
⁡
(
g
,
𝒲
)
:=
sup
w
∈
𝒲
|
Δ
⁡
(
w
)
|
.
\mathrm{CE}(g;\mathcal{W}):=\sup\limits_{w\in\mathcal{W}}|\Delta(w)|.
(E.31)
•
The
dual post-processing gap
of
g
g
with respect to a function class
ℋ
\mathcal{H}
is
Gap
⁡
(
g
,
ℋ
)
:=
ℒ
⁡
(
g
)
−
inf
h
∈
ℋ
ℒ
⁡
(
h
)
.
\mathrm{Gap}(g;\mathcal{H}):=\mathcal{L}(g)-\inf\limits_{h\in\mathcal{H}}\mathcal{L}(h).
(E.32)
Theorem 43
(General relationship between calibration and post-processing)
.
Let
ψ
:
ℝ
K
→
ℝ
\psi:\mathbb{R}^{K}\to\mathbb{R}
be differentiable and
λ
\lambda
-smooth, i.e.
∇
ψ
\nabla\psi
is
λ
\lambda
-Lipschitz.
Let
𝒲
\mathcal{W}
be a class of bounded functions
w
:
𝒳
×
ℝ
K
→
ℝ
K
w:\mathcal{X}\times\mathbb{R}^{K}\to\mathbb{R}^{K}
with
‖
w
x
‖
≤
1
\|w_{x}\|\leq 1
.
For
w
∈
𝒲
w\in\mathcal{W}
and
β
∈
[
−
1
/
λ
,
1
/
λ
]
\beta\in[-1/\lambda,1/\lambda]
, define the perturbed dual predictor
g
w
​
(
x
)
:=
g
⁡
(
x
)
+
β
​
w
​
(
x
,
g
⁡
(
x
)
)
.
g_{w}(x):=g(x)+\beta\,w(x,g(x)).
(E.33)
Let
𝒢
𝒲
:=
{
g
w
:
w
∈
𝒲
,
β
∈
[
−
1
/
λ
,
1
/
λ
]
}
\mathcal{G}_{\mathcal{W}}:=\{g_{w}:w\in\mathcal{W},\;\beta\in[-1/\lambda,1/\lambda]\}
.
Then, for every
g
:
𝒳
→
ℝ
K
g:\mathcal{X}\to\mathbb{R}^{K}
and distribution
𝒟
\mathcal{D}
,
1
2
​
(
CE
⁡
(
g
,
𝒲
)
)
2
≤
λ
⋅
Gap
⁡
(
g
,
𝒢
𝒲
)
≤
CE
⁡
(
g
,
𝒲
)
.
\frac{1}{2}\,\Big(\mathrm{CE}(g;\mathcal{W})\Big)^{2}\;\leq\;\lambda\cdot\mathrm{Gap}(g;\mathcal{G}_{\mathcal{W}})\;\leq\;\mathrm{CE}(g;\mathcal{W}).
(E.34)
Proof.
By the definition of
ℓ
(
ψ
)
\ell^{(\psi)}
,
ℒ
⁡
(
g
)
−
ℒ
⁡
(
g
w
)
\displaystyle\mathcal{L}(g)-\mathcal{L}(g_{w})
=
𝔼
⁡
[
ψ
⁡
(
g
⁡
(
x
)
)
−
⟨
y
,
g
⁡
(
x
)
⟩
−
ψ
⁡
(
g
w
​
(
x
)
)
+
⟨
y
,
g
w
​
(
x
)
⟩
]
\displaystyle=\mathbb{E}\!\big[\psi(g(x))-\langle y,g(x)\rangle-\psi(g_{w}(x))+\langle y,g_{w}(x)\rangle\big]
=
𝔼
⁡
[
ψ
⁡
(
g
⁡
(
x
)
)
−
ψ
⁡
(
g
w
​
(
x
)
)
+
β
⁡
⟨
y
,
w
⁡
(
x
,
g
⁡
(
x
)
)
⟩
]
.
\displaystyle=\mathbb{E}\!\big[\psi(g(x))-\psi(g_{w}(x))+\beta\langle y,w(x,g(x))\rangle\big].
By convexity and
λ
\lambda
-smoothness of
ψ
\psi
, for
z
=
g
⁡
(
x
)
,
z
′
=
g
w
​
(
x
)
z=g(x),\,z^{\prime}=g_{w}(x)
and
w
x
=
w
⁡
(
x
,
g
⁡
(
x
)
)
w_{x}=w(x,g(x))
⟨
∇
ψ
​
(
z
)
,
β
​
w
x
⟩
≤
ψ
⁡
(
z
′
)
−
ψ
⁡
(
z
)
≤
⟨
∇
ψ
​
(
z
)
,
β
​
w
x
⟩
+
λ
​
β
2
2
​
‖
w
x
‖
2
.
\langle\nabla\psi(z),\beta w_{x}\rangle\;\leq\;\psi(z^{\prime})-\psi(z)\;\leq\;\langle\nabla\psi(z),\beta w_{x}\rangle+\frac{\lambda\beta^{2}}{2}\|w_{x}\|^{2}.
(E.35)
Since
f
​
(
x
)
=
∇
ψ
​
(
g
​
(
x
)
)
f(x)=\nabla\psi(g(x))
and
‖
w
x
‖
≤
1
\|w_{x}\|\leq 1
, this yields
β
​
Δ
​
(
w
)
−
λ
​
β
2
2
≤
ℒ
⁡
(
g
)
−
ℒ
⁡
(
g
w
)
≤
β
​
Δ
​
(
w
)
.
\beta\,\Delta(w)-\frac{\lambda\beta^{2}}{2}\;\leq\;\mathcal{L}(g)-\mathcal{L}(g_{w})\;\leq\;\beta\,\Delta(w).
(E.36)
Lower bound.
For
w
∈
𝒲
w\in\mathcal{W}
, set
β
=
Δ
⁡
(
w
)
/
λ
\beta=\Delta(w)/\lambda
(which lies in
[
−
1
/
λ
,
1
/
λ
]
[-1/\lambda,1/\lambda]
). Then
1
2
​
λ
​
Δ
​
(
w
)
2
≤
ℒ
⁡
(
g
)
−
ℒ
⁡
(
g
w
)
.
\frac{1}{2\lambda}\,\Delta(w)^{2}\;\leq\;\mathcal{L}(g)-\mathcal{L}(g_{w}).
(E.37)
Taking
sup
w
∈
𝒲
\sup\limits_{w\in\mathcal{W}}
yields
1
2
​
(
CE
⁡
(
g
,
𝒲
)
)
2
≤
λ
⋅
Gap
⁡
(
g
,
𝒢
𝒲
)
.
\frac{1}{2}\,\big(\mathrm{CE}(g;\mathcal{W})\big)^{2}\;\leq\;\lambda\cdot\mathrm{Gap}(g;\mathcal{G}_{\mathcal{W}}).
(E.38)
Upper bound.
For
g
w
∈
𝒢
𝒲
g_{w}\in\mathcal{G}_{\mathcal{W}}
, since
|
β
|
≤
1
/
λ
|\beta|\leq 1/\lambda
ℒ
⁡
(
g
)
−
ℒ
⁡
(
g
w
)
≤
β
​
Δ
​
(
w
)
≤
1
λ
​
|
Δ
⁡
(
w
)
|
.
\mathcal{L}(g)-\mathcal{L}(g_{w})\;\leq\;\beta\,\Delta(w)\leq\;\frac{1}{\lambda}\,|\Delta(w)|.
(E.39)
Taking
sup
w
∈
𝒲
\sup\limits_{w\in\mathcal{W}}
gives
λ
⋅
Gap
⁡
(
g
,
𝒢
𝒲
)
≤
CE
⁡
(
g
,
𝒲
)
.
\lambda\cdot\mathrm{Gap}(g;\mathcal{G}_{\mathcal{W}})\;\leq\;\mathrm{CE}(g;\mathcal{W}).
(E.40)
Combining the upper and lower bounds proves
Eq.
E.34
.
∎
Remark 44
(Tighter exponent under strong convexity)
.
If, in addition,
ψ
\psi
is
μ
\mu
-strongly convex for some
μ
>
0
\mu>0
i.e.
ψ
⁡
(
z
′
)
≥
ψ
⁡
(
z
)
+
⟨
∇
ψ
​
(
z
)
,
z
′
−
z
⟩
+
μ
2
​
‖
z
′
−
z
‖
2
,
\psi(z^{\prime})\geq\psi(z)+\langle\nabla\psi(z),z^{\prime}-z\rangle+\tfrac{\mu}{2}\|z^{\prime}-z\|^{2},
then one obtains matching upper and lower bounds.
In this case, both inequalities in
Thm.
43
become quadratic in the calibration error:
μ
2
​
λ
2
​
(
CE
⁡
(
g
,
𝒲
)
)
2
≤
Gap
⁡
(
g
,
𝒢
𝒲
)
≤
1
2
​
μ
​
(
CE
⁡
(
g
,
𝒲
)
)
2
.
\frac{\mu}{2\lambda^{2}}\,\big(\mathrm{CE}(g;\mathcal{W})\big)^{2}\;\leq\;\mathrm{Gap}(g;\mathcal{G}_{\mathcal{W}})\;\leq\;\frac{1}{2\mu}\,\big(\mathrm{CE}(g;\mathcal{W})\big)^{2}.
(E.41)
That is, the dual post-processing gap and the squared dual calibration error
are equivalent up to constants determined by
(
μ
,
λ
)
(\mu,\lambda)
.
E.8.1
Specialization to cross-entropy loss
For completeness, we summarize the standard facts about the dual parametrization of the negative log-loss in
Table
4
.
Table 4
:
Duality relationships for the Negative Log-Loss (Cross-Entropy) proper scoring rule.
Primal Proper Loss (
ℓ
nll
\ell_{\text{nll}}
)
ℓ
(
y
,
v
)
=
−
∑
i
=
1
K
y
i
log
v
i
\ell(y,v)=-\sum_{i=1}^{K}y_{i}\log v_{i}
Convex Function (
ϕ
\phi
)
ϕ
⁡
(
v
)
=
∑
i
=
1
K
v
i
​
log
⁡
(
v
i
)
\phi(v)=\sum_{i=1}^{K}v_{i}\log(v_{i})\quad
(Negative Entropy)
Convex Conjugate (
ϕ
∗
\phi^{*}
)
ϕ
∗
​
(
z
)
=
log
⁡
(
∑
i
=
1
K
exp
⁡
(
z
i
)
)
\phi^{*}(z)=\log\left(\sum_{i=1}^{K}\exp(z_{i})\right)\quad
(Log-Sum-Exp)
Dual Loss (
ℓ
nll
∗
\ell^{*}_{\text{nll}}
)
ℓ
∗
​
(
y
,
z
)
=
ϕ
∗
​
(
z
)
−
y
T
​
z
\ell^{*}(y,z)=\phi^{*}(z)-y^{T}z
Dual Mapping (
∇
ϕ
∗
\nabla\phi^{*}
)
∇
ϕ
∗
​
(
z
)
=
softmax
​
(
z
)
\nabla\phi^{*}(z)=\text{softmax}(z)
The log-sum-exp function
ϕ
∗
​
(
z
)
=
log
⁡
(
∑
i
=
1
K
exp
⁡
(
z
i
)
)
\phi^{*}(z)=\log\left(\sum_{i=1}^{K}\exp(z_{i})\right)
is
1
/
4
1/4
-smooth, as shown in
Beck and Teboulle (2003)
and
Nesterov (2005)
, so
Thm.
43
applies with
λ
=
1
/
4
\lambda=1/4
.
Moreover, to translate the result into the notation of our main theorems, recall the relationship between the primal prediction
f
⁡
(
x
)
f(x)
and its dual representation
g
⁡
(
x
)
g(x)
:
f
⁡
(
x
)
\displaystyle f(x)
=
∇
ϕ
∗
​
(
g
⁡
(
x
)
)
=
softmax
​
(
g
⁡
(
x
)
)
\displaystyle=\nabla\phi^{*}(g(x))=\text{softmax}(g(x))
g
⁡
(
x
)
\displaystyle g(x)
=
log
⁡
(
f
⁡
(
x
)
)
\displaystyle=\log(f(x))
The perturbed loss can then be expressed in terms of the dual variables. The dual loss on perturbed logits
g
+
w
g+w
is equivalent to the primal loss on the perturbed probability distribution
f
⋆
w
f\star w
:
ℓ
nll
∗
​
(
y
,
g
+
w
)
=
ℓ
nll
​
(
y
,
softmax
​
(
g
+
w
)
)
=
ℓ
nll
​
(
y
,
f
⋆
w
)
\ell^{*}_{\text{nll}}(y,g+w)=\ell_{\text{nll}}(y,\text{softmax}(g+w))=\ell_{\text{nll}}(y,f\star w)
where
f
⋆
w
=
softmax
​
(
log
⁡
(
f
)
+
w
)
f\star w=\text{softmax}(\log(f)+w)
.
E.9
Conformal Prediction via Weighted Calibration
Here we observe that conformal prediction guarantees
can be expressed as a type of
weighted calibration
(
Gopalan et al., 2024
)
,
for a particular weight family.
Recall conformal prediction asks for a model
F
⁡
(
x
)
F(x)
which outputs a
set
of
labels, with the guarantee that this set contains the true label with high probability.
Specifically, a conformal predictor has
coverage
α
\alpha
if:
Pr
x
,
y
∼
𝒟
[
y
∈
F
(
x
)
]
≥
1
−
α
.
\Pr_{x,y\sim\mathcal{D}}[y\in F(x)]\geq 1-\alpha.
(E.42)
For an introduction to conformal prediction, see
Angelopoulos et al. (2023)
or the lecture notes of
Tibshirani (2023)
.
E.9.1
Conformal Prediction from Full Calibration
Given a standard predictor
f
f
, which outputs a distribution on labels, one natural
way to construct a conformal predictor
F
α
F_{\alpha}
is: given input
x
x
, and prediction
f
⁡
(
x
)
f(x)
,
output the set of highest-predicted-probability labels which sum to total probability
1
−
α
1-\alpha
. This means, outputting the
K
K
most-likely classes according to
f
⁡
(
x
)
f(x)
,
where
K
K
is chosen per-sample based on the predicted probabilities.
The first observation (which is folklore) is:
if the predictor
f
f
is perfectly calibrated, in the sense of full-calibration,
then the induced conformal predictor
F
α
F_{\alpha}
is correct (i.e. has coverage
α
\alpha
).
This statement is not very relevant in practice, since full calibration is often too strong to hold.
However, we can achieve the same result with a weaker notion of calibration.
This is a straightforward result; we sketch the argument below.
E.9.2
Conformal Prediction from Weighted Calibration
Lemma 45
.
Suppose
f
:
𝒳
→
Δ
N
f:\mathcal{X}\to\Delta_{N}
is perfectly weighted-calibrated (in the sense of
Gopalan et al. (2024)
) with respect to the
following family of weight functions
w
⁡
(
f
)
∈
ℝ
N
w(f)\in\mathbb{R}^{N}
:
𝒲
:=
{
w
(
f
)
=
σ
𝟙
T
α
​
(
f
)
∣
α
∈
[
0
,
1
]
,
σ
∈
{
±
1
}
}
\displaystyle\mathcal{W}:=\{w(f)=\sigma\mathbbm{1}_{T_{\alpha}(f)}\mid\alpha\in[0,1],\sigma\in\{\pm 1\}\}
(E.43)
Where
𝟙
T
∈
{
0
,
1
}
N
\mathbbm{1}_{T}\in\{0,1\}^{N}
is the indicator-vector for set of indices
T
T
, and the set
T
T
contains
the highest-probability labels, defined as:
t
α
∗
​
(
f
)
\displaystyle t_{\alpha}^{*}(f)
:
=
max
{
t
:
(
∑
i
∈
[
N
]
f
i
𝟙
{
f
i
≥
t
}
)
≥
1
−
α
}
\displaystyle:=\max\{t:\left(\sum_{i\in[N]}f_{i}\mathbbm{1}\{f_{i}\geq t\}\right)\geq 1-\alpha\}
(the threshold probability, given
f
f
)
T
α
​
(
f
)
\displaystyle T_{\alpha}(f)
:
=
{
i
:
f
i
≥
t
α
∗
​
(
f
)
}
\displaystyle:=\{i:f_{i}\geq t^{*}_{\alpha}(f)\}
(The set of top-class indices, for given level
α
\alpha
)
That is, suppose:
𝔼
(
x
,
y
)
∼
𝒟
[
⟨
y
−
f
⁡
(
x
)
,
w
⁡
(
f
⁡
(
x
)
)
⟩
]
≡
0
\displaystyle\mathop{\mathbb{E}}_{(x,y)\sim\mathcal{D}}\left[\left\langle y-f(x),w(f(x))\right\rangle\right]\equiv 0
Then, the induced conformal predictor
F
α
F_{\alpha}
of
f
f
is valid at all coverage levels
α
\alpha
.
Proof.
(Sketch)
Notice that by construction,
⟨
f
,
𝟙
T
α
​
(
f
)
⟩
≥
1
−
α
\langle f,\mathbbm{1}_{T_{\alpha}(f)}\rangle\geq 1-\alpha
.
Therefore by calibration we must have:
⟨
y
,
𝟙
T
α
​
(
f
)
⟩
≥
1
−
α
\langle y,\mathbbm{1}_{T_{\alpha}(f)}\rangle\geq 1-\alpha
.
Moreover, the set
T
α
​
(
f
)
T_{\alpha}(f)
is exactly the output of the induced conformal predictor
F
α
F_{\alpha}
, given base prediction
f
f
.
Therefore
Pr
[
y
∈
T
α
(
f
(
x
)
)
]
\displaystyle\Pr[y\in T_{\alpha}(f(x))]
=
𝔼
[
⟨
y
,
𝟙
T
α
​
(
f
)
⟩
]
\displaystyle=\mathop{\mathbb{E}}[\langle y,\mathbbm{1}_{T_{\alpha}(f)}\rangle]
(E.44)
≥
1
−
α
\displaystyle\geq 1-\alpha
(E.45)
∎
By the general connection of Theorem
25
,
if a model
f
f
is
𝒲
\mathcal{W}
-locally-loss-optimal w.r.t. the weight class of Equation (
E.43
),
then the induced conformal predictor
F
α
F_{\alpha}
has coverage
α
\alpha
for all
α
∈
[
0
,
1
]
\alpha\in[0,1]
.
Appendix F
Disaggregated Reliability Diagram Results
In this section, we report disaggregated reliability diagram results for individual configurations we evaluated. The plots are displayed as follow:
•
the right three columns present results for instruct models,
•
the left three columns present results for the corresponding base models.
In some cases, there are multiple instruct models trained from a single base models, hence for some base models, their results are being presented multiple times.
Some instruct models do not have a public corresponding base model—in those cases, the left three columns of the row are empty.
As discussed in the
Sec.
5
, TriviaQA and SimpleQA were not evaluated for the CoT response style.
The figures start on the next page. For a quick references:
•
GSM8K in
Sec.
F.1
•
OpenMathInstruct in
Sec.
F.2
•
TriviaQA in
Sec.
F.3
•
SimpleQA in
Sec.
F.4
F.1
GSM8K
F.2
OpenMathInstruct
F.3
TriviaQA
F.4
SimpleQA