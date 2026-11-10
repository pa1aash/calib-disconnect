---
title: A Survey of Confidence Estimation and Calibration in Large Language Models
  (full text)
id: a-survey-of-confidence-estimation-and-calibration-in-large-language-models-full
tags:
- code-llm-confidence-positioning-d82d00
- related-survey
created: '2026-11-09T23:10:56.560192Z'
updated: '2026-11-09T23:27:44.680197Z'
source: https://arxiv.org/pdf/2311.08298
status: review
type: note
content_type: paper
deprecated: false
summary: FULL TEXT (arXiv 2311.08298 v2, Geng et al., Mar 2024). Survey of logit-based,
  verbalized, consistency, probing (P(IK)) and calibration methods for LLM confidence.
  No dedicated code or execution-label coverage (searched). Use as pre-2024 taxonomy
  background only.
---

A Survey of Confidence Estimation and Calibration
in Large Language Models
Jiahui Geng1 , Fengyu Cai2 , Yuxia Wang1 ,
Heinz Koeppl2 , Preslav Nakov1 , Iryna Gurevych1
1
Mohamed bin Zayed University of Artificial Intelligence
2
Technical University of Darmstadt
{jiahui.geng, yuxia.wang,preslav.nakov,iryna.gurevych}@mbzuai.ac.ae,
{fengyu.cai,heinz.koeppl}@tu-darmstadt.de

arXiv:2311.08298v2 [cs.CL] 25 Mar 2024

Abstract
Large language models (LLMs) have demonstrated remarkable capabilities across a wide
range of tasks in various domains. Despite their
impressive performance, they can be unreliable
due to factual errors in their generations. Assessing their confidence and calibrating them
across different tasks can help mitigate risks
and enable LLMs to produce better generations.
There has been a lot of recent research aiming
to address this, but there has been no comprehensive overview to organize it and outline the
main lessons learned. The present survey aims
to bridge this gap. In particular, we outline the
challenges and we summarize recent technical
advancements for LLM confidence estimation
and calibration. We further discuss their applications and suggest promising directions for
future work.

1

Introduction

Large language models (LLMs) have demonstrated
a wide range of capabilities, such as world knowledge storage, sophisticated language-based reasoning, and in-context learning (Petroni et al., 2019;
Wei et al., 2022; Brown et al., 2020a). However,
LLMs do not consistently achieve good performance (Wang et al., 2023a; Zhang et al., 2023b).
Their generation still includes biases (Zhao et al.,
2021; Wang et al., 2023c) and hallucinations that
do not align with reality (Zhang et al., 2023b). Evaluating the trustworthiness of responses from these
models remains challenging (Liu et al., 2023c).
Confidence (or uncertainty) estimation is crucial for tasks like out-of-distribution detection and
selective prediction (Kendall and Gal, 2017; Lu
et al., 2022), and it has been extensively studied
and applied in various contexts (Lee et al., 2018;
DeVries and Taylor, 2018). A related concept is
that of model calibration, which focuses on aligning predictive probabilities (estimated confidence)
to actual accuracy (Guo et al., 2017).

However, applying these methods directly to
LLMs presents several challenges. The output
space of these models is significantly larger than
that of discriminative models. The number of possible outcomes grows exponentially with the generation length, making it impossible to access all
potential responses. Additionally, different expressions may convey the same meaning, suggesting
that confidence estimation should consider semantics. Lastly, LLMs show unique properties, such as
expressing confidence in words (Lin et al., 2022;
Xiong et al., 2023) and the ability to perform zeroshot or few-shot learning (Brown et al., 2020a).
Nonetheless, their responses can be sensitive to
the prompts, e.g., the examples provided and their
order, which can cause a lot of instability in the
results. Given this, confidence estimation and calibration for LLMs is growing as an emerging area
of interest (Jiang et al., 2021; Lin et al., 2022, 2023;
Shrivastava et al., 2023).
While existing surveys mainly focused on
issues such as hallucination and factuality in
LLMs (Zhang et al., 2023b; Wang et al., 2023b),
there are no comprehensive surveys systematically
discussing the technical advancements in LLMs,
and here we aim to bridge this gap. We explore
the unique challenges posed by LLMs and examine the latest studies addressing these issues. We
first discuss key concepts such as confidence, uncertainty, and calibration in the context of neural
models, as detailed in Section 2. Then, we pursue
two different directions: one addressing confidence
estimation and calibration techniques for generation tasks in Section 3, and the other for classification tasks in Section 4. We conclude by exploring
their practical applications (Section 5) and looking
at potential future research directions (Section 6).
Figure 1 provides a comprehensive representation
of the survey’s structure. By conducting a detailed
examination of existing research, our goal is to illuminate this vital facet of LLMs, contributing to

Classification

Guo et al. (2017); Nixon et al. (2019); Kull et al. (2019); Bradley (1997)

Generation

Kumar and Sarawagi (2019); Lin et al. (2023); Zhu et al. (2023a); Huang et al. (2024)

Confidence Estimation and Calibration in LLMs

Metrics
Logit-based methods

Duan et al. (2023); Kuhn et al. (2023)

Internal state-based
methods

Ren et al. (2022); Kadavath et al. (2022); Burns et al. (2023)
Li et al. (2023); Azaria and Mitchell (2023)

Linguistic confidence

Mielke et al. (2022); Xiong et al. (2023)

Consistency-based
estimation

Manakul et al. (2023b); Lin et al. (2023)

Surrogate models

Shrivastava et al. (2023); Touvron et al. (2023b)

Improving generation

Kumar and Sarawagi (2019); Wang et al. (2020); Lu et al. (2022)
Xiao and Wang (2021); van der Poel et al. (2022); Zablotskaia et al. (2023)
Zhao et al. (2022, 2023a)

Improving linguistic
confidence

Mielke et al. (2022); Lin et al. (2022); Zhou et al. (2023)

Estimation

Logit-based method

Mielke et al. (2022); Lin et al. (2022); Zhou et al. (2023)

Calibration

Bias mitigation

Zhao et al. (2021); Fei et al. (2023); Nie et al. (2022); Han et al. (2022)

Estimation

Generation

Calibration

Methods

Classification

Application

Hallucination Detection
and Mitigation

Manakul et al. (2023a); Zhang et al. (2023a)
Varshney et al. (2023)

Ambiguity detection
and selective generation

Kamath et al. (2020); Zablotskaia et al. (2023)
Cole et al. (2023); Hou et al. (2023)

Uncertainty-guided data
exploitation

Yu et al. (2022); Su et al. (2022); Jiang et al. (2023)

Figure 1: The taxonomy of confidence estimation and calibration in LLMs.

an event with a 70% probability, that event should
actually happen about 70% of the time under similar circumstances. The equation for this relationship is as follows:

the development of more reliable applications.

2

Preliminaries and Background

2.1

Basic Concepts

In machine learning, confidence and uncertainty
are two facets of a single principle: higher confidence corresponds to lower uncertainty (Xiao et al.,
2022; Chen and Mueller, 2023). Research on quantifying model confidence has led to the development of two key concepts: relative confidence score
and absolute confidence score, offering different
methods to assess and to interpret confidence levels (Kamath et al., 2020; Vazhentsev et al., 2023a).
Given input x, ground truth y, and prediction ŷ,
the model’s predictive confidence is denoted as
conf(x, ŷ). Relative confidence scores emphasize
the ability to rank samples, distinguishing correct
predictions from incorrect ones. Ideally, for every
pair of (xi , yi ) and (xj , yj ) and their corresponding
predictions ŷi and ŷj , we have
conf(xi , ŷi ) ≤ conf(xj , ŷj )
⇐⇒ P (ŷi = yi |xi ) ≤ P (ŷj = yj |xj )

(1)

An absolute confidence score indicates that a
model’s score reflects its true accuracy in realworld scenarios. For example, if a model predicts

P (ŷ = y | conf(x, ŷ) = q) = q

(2)

When the model’s predicted confidence scores consistently align with this principle, the model is considered to be well-calibrated.
Kendall and Gal (2017) proposed categorizing
uncertainty in machine learning into aleatoric and
epistemic uncertainty. Aleatoric or data uncertainty
emerges from the inherent randomness or variability of a system or a process. It is an intrinsic feature
of the system and is typically irreducible. Epistemic uncertainty, in contrast, is known as model
uncertainty or systematic uncertainty. It arises from
the lack of knowledge or information about the
system being modeled and is reducible, as it can
diminish with the acquisition of more data and improved modeling techniques (Gal and Ghahramani,
2016; Lakshminarayanan et al., 2017).
2.2

Metrics and Methods

Metrics Due to the continuous nature of confidence scores, it is impossible to accurately calculate the probability as in Eq. 2. Expected calibra-

tion error (ECE; Guo et al. 2017) approximates
it by clustering instances with similar confidence.
The predicted probabilities are first segmented into
various bins. ECE is then calculated by taking the
weighted average of the discrepancies between the
mean predicted probability and the actual accuracy
across all bins Bm , m = 1 · · · , M :
M
X
|Bm |

ECE =

m=1

N

|acc(Bm ) − conf (Bm )| (3)

One drawback of the ECE metric is its sensitivity
to various factors such as bucket width and the variance of samples within these buckets. To overcome
these issues, more sophisticated schemes have been
developed, including static calibration error (SCE),
adaptive calibration error (ACE; Nixon et al. 2019),
and classwise ECE (Kull et al., 2019). ECE can
also be visualized as a reliability diagram, which
plots predicted probabilities against observed frequencies, with points or lines above the diagonal
indicating overconfidence. Additionally, metrics
such as F1 score, area under receiver operating
characteristic curve (AUROC; Bradley 1997) and
area under accuracy-rejection curve (AUARC; Lin
et al. 2023), can indicate whether the confidence
score can appropriately differentiate between correct and incorrect answers.
However, it’s necessary to adapt metrics to effectively process sequence of tokens with semantics. A common approach is to evaluate whether
the next token probability is well-calibrated. Assuming that yi = yi1 , · · · , yiT denotes the sequence of generated tokens (target sentence) and
that xi = xi1 , · · · , xiS denotes the sequence of
input tokens (source sentence), the probability
of generating
QTthe target sequence can be represented as: t=1 P (yit |xi , yi,<t ). For simplicity,
we use Pit (yit ) to represent P (yit |yi,<t , xi ) and
Cit (y) = δ(yit = y) to denote if y matches the
correct label yit . The ECE can be mathematically
expressed as:
M

1 X
|
L

X

Cit (ŷit ) − Pit (ŷit )|

(4)

m=1 i,t:Pit (ŷit )∈Bm

P
where L = N
i=1 |yi | is the total number of generated tokens. Kumar and Sarawagi (2019) claimed
that such metric focuses solely on the highest score
label, neglecting the entire probability distribution,
and thereby introduced weighted ECE for refined
calibration distinction. Another approach analyzes

the overall correctness and confidence of answers
directly, especially in tasks like classification and
question answering (Lin et al., 2022; Kadavath
et al., 2022). Huang et al. (2024) treated correctness as distributions instead of binary values, assessing calibration through the distance between
correctness and confidence.
Methods in discriminative models Common
methods for confidence estimation include logitbased methods (Pearce et al., 2021; Pereyra
et al., 2017), ensemble-based and Bayesian methods (Lakshminarayanan et al., 2017; Gal and
Ghahramani, 2016), density-based methods (Lee
et al., 2018), and confidence-learning methods (DeVries and Taylor, 2018). Model calibration (Guo
et al., 2017) can either occur during the model’s
training phase, for example, by improving loss
functions (Szegedy et al., 2016) or be applied after
the model has been trained, such as temperature
scaling (TS; Guo et al. 2017) and feature-based
calibrators (FBC; Jiang et al. 2021). Table 3 represents significant research in the discriminative
LMs, with a list of models, tasks, and calibration
methods. Due to space limitations, please refer to
the Appendix A for detailed principles and comparisons.

3

LLMs for Generation Tasks

3.1

Confidence Estimation

In this section, we generally divide the methods
into white-box and black-box methods. We first
provide a detailed overview of these methods and
then summarize their strengths, weaknesses, and
connections.
3.1.1

White-Box Methods

White-box methods operate on the premise that the
state at every position of the LLMs is accessible
during inference.
Logit-based methods The logit-based method
evaluates sentence uncertainty using token-level
probabilities or entropy (Huang et al., 2023b). To
ensure an evaluation consistent across sentences
of different lengths, the length-normalized likelihood probability is widely utilized (Murray and
Chiang, 2018). Moreover, alternatives such as the
minimum or average token probabilities and the
average entropy are also widely used (Vazhentsev
et al., 2023b). Logit-based techniques readily adapt
to scenarios involving multiple sampling (Vazhent-

Study

Model

Proposed Methods

Duan et al. (2023)

OPT (Zhang et al., 2022)

Manakul et al. (2023b)
Kuhn et al. (2023)

GPT-3 (Brown et al., 2020b)
OPT (Zhang et al., 2022)

Kadavath et al. (2022)

Anthropic LLM (Bai et al., 2022)

SAR (Shifting Attention to Relevance): consider semantic relevance when evaluating
token and sentence-level uncertainty
Semantic uncertainty: evaluate the consistency of responses by various methods
Cluster answers according to semantics and then computes the sum of probabilities
within each cluster to represent confidence
P(True): the probability a model assigns to its answer as True, P(IK): probability a
model assigns to "I know" by leveraging a binary classifier

Xiong et al. (2023)

GPT3/3.5/4 (Brown et al., 2020b),
Hybrid methods combining linguistic confidence and consistency-based confidence
Vicuna (Chiang et al., 2023)

Lin et al. (2023)
Shrivastava et al. (2023)

GPT-3.5
GPT-3.5/4, Claude

Estimate confidence by evaluating the lexical and semantic similarity among responses
Hybrid methods combing confidence from surrogate models and linguistic confidence
of target models

Table 1: Recent studies of LLM confidence estimation. These studies evaluate confidence estimation in questionanswering tasks, utilizing metrics such as ECE, AUROC, etc.

Logit
1

Consistency
2

1

4
Internal state

3

2
4

Semantics

(a) White-box

Linguistic
confidence

3

Surrogate
model

can self-assess to differentiate between correct and
incorrect answers. They suggested a method called
P(True), where the LLM first generates responses
and then evaluates them as "True" or "False". The
probability the model assigns the confidence level
to "True” determines the confidence level.

(b) Black-box

Figure 2: Venn diagram: the taxonomy of information sources for white-box (Left) and black-box (Right)
confidence estimation methods. These two families of
methods can be categorized into the methods relying on
logit, internal state, or semantics, and those relying on
consistency, linguistic confidence, or surrogate model,
respectively. The intersections of these methods are
located in Zone 1 - 4.

sev et al., 2023b) or ensemble models (Malinin and
Gales, 2021a).
To incorporate semantics, Duan et al. (2023)
introduced the concept of token-level relevance,
which evaluates the relevance of the token by comparing semantic change before and after moving
the token with a semantic similarity metric like Sentence Transformer (Reimers and Gurevych, 2019).
Then, sentence uncertainty can be adjusted based
on the token’s relevance. Duan et al. (2023) further proposed sentence-level relevance in multiple sampling settings, considering the similarity
between the returned sentence and other sampled
ones. Kuhn et al. (2023) proposed semantic uncertainty, which first clusters semantically equivalent
samples based on the bidirectional entailment between samples and then approximates semantic
entropy by summing probabilities in each cluster.
Kadavath et al. (2022) discovered that LLMs

Internal state-based methods Ren et al. (2022)
introduced a technique for out-of-distribution detection and selective generation. The method starts by
computing embeddings for both inputs and outputs
in the training data, fitting them to a Gaussian distribution. It then assesses the model’s confidence
in its generated data by calculating the relative Mahalanobis distance of the evaluated data pair from
this Gaussian distribution.
Recent studies have posited the existence of a direction in activation space that effectively separates
true and false inputs (Kadavath et al., 2022; Burns
et al., 2023; Li et al., 2023; Azaria and Mitchell,
2023). Kadavath et al. (2022) proposed training
a classifier (the probe), named P(IK), on the activations of a network to predict whether an LLM
knows the answer. They sampled multiple answers
for each question at a consistent temperature, labeled the correctness of each answer, and then used
the question-correctness pair as the training data.
Similarly, Li et al. (2023) and Azaria and Mitchell
(2023) employed linear probes to examine whether
attention heads in various layers can differentiate
between correct and incorrect answers. Their empirical findings indicated that certain middle layers
and a few attention heads exhibit strong performance in this task, although the layer positions
vary across models. Burns et al. (2023) introduced an unsupervised approach to map hidden
states to probabilities. It entails responding to ques-

Study

Model

Task

Calibration Methods

LSTM (Bahdanau et al., 2015),
Transformer (Vaswani et al., 2017)

Machine Translation

TS with Learnable Parameters

Machine Translation
Machine Translation
Data2Text Generation,
Image Captioning
Text Summarization

Confidence-Based LS
LS, Dropout

van der Poel et al. (2022)

Transformer (Vaswani et al., 2017)
Transformer (Vaswani et al., 2017)
LSTM (Bahdanau et al., 2015),
Transformer (Vaswani et al., 2017)
BART (Lewis et al., 2020)

Zablotskaia et al. (2023)

T5 (Raffel et al., 2020)

Text Summarization

Zhao et al. (2022)

PEGASUS (Zhang et al., 2020a)

Zhao et al. (2023a)
Mielke et al. (2022)
Lin et al. (2022)

T5 (Raffel et al., 2020)
BlenderBot (Roller et al., 2021)
GPT-3 (Brown et al., 2020b)

Zhao et al. (2021)

GPT-3 (Brown et al., 2020b)

Kumar and Sarawagi
(2019)
Lu et al. (2022)
Wang et al. (2020)
Xiao and Wang (2021)

Fei et al. (2023)
Han et al. (2022)
Kumar (2022)
Holtzman et al. (2021)
Zheng et al. (2023)

PALM-2 (Anil et al., 2023),
CLIP (Radford et al., 2021)
GPT-2 (Radford et al., 2019)
GPT-2 (Radford et al., 2019)
GPT-2(Radford et al., 2019),
GPT-3 (Brown et al., 2020b)
LLaMA (Touvron et al., 2023a),
Vicuna (Chiang et al., 2023),
Falcon (Penedo et al., 2023), GPT-3.5

Text Summarization,
Question Answering
Text Summarization
Dialogue Generation
Math Question Answering

Uncertainty-Aware Decoding
CPMI-Based Decoding
MC-Dropout, BE, SNGP,
DeepEnsemble
SLiC
SLiC-HF
Linguistic Calibration
Fine-Tuning

Text Classification, Fact Retrieval
Information Extraction

Contextual Calibration

Text Classification

Domain-Context Calibration

Text Classification
Multiple Choice Question Answering

Prototypical Calibration
Answer-Level Calibration

Multiple Choice Question Answering

PMIDC

Multiple Choice Question Answering

PriDE

Table 2: Studies of LLM calibration. The first half is about generation tasks, and the second half is about
classification tasks. Calibration methods: LS: label smoothing, TS: temperature scaling, BE: Bayesian ensemble,
SNGP: spectral-normalized Gaussian process, MCDropout: Monte Carlo dropout, SLiC: sequence likelihood
calibration, HF: human feedback, FBC: feature-based calibrator, CPMI: conditional pointwise mutual information,
PMIDC: domain conditional pointwise mutual information, PriDE: debiasing with prior estimation.

tions with "Yes" or "No," extracting and converting model activations into truth probabilities, and
optimizing unsupervised loss for consistency. It
ultimately gauges the model’s confidence by estimating the likelihood of a "Yes" response.
Summary White-box methods, as illustrated in
Figure 2a, primarily utilize logits, internal states,
and semantics as sources of information. Logitbased approaches, easy to implement during inference, face a limitation in that low logit probabilities
may reflect various properties of language. Methods focusing on internal states (Kadavath et al.,
2022; Li et al., 2023; Azaria and Mitchell, 2023)
provide insights into the model’s linguistic understanding, though they typically require supervised
training on specially annotated data. Levinstein
and Herrmann (forthcoming) highlighted the limitations of the probing method in generalizing to
unseen examples with negations. Semantics are often used to complement other methods, providing
them with interpretability (Kuhn et al., 2023; Duan
et al., 2023).
To leverage their respective strengths, the current advanced methods tend to combine different
dimensions during confidence estimation. Recent

works (Kuhn et al., 2023; Duan et al., 2023) achieve
outstanding performance on uncertainty estimation
for open-domain question answering by combining logit-based approaches with semantics, using
tools like bi-directional entailment or sentence encoders, aligning with Zone 2. Rephrasing and
round-trip translation can also be considered as using semantics to augment the remaining two methods (Jiang et al., 2021; Zhao et al., 2023b), corresponding to Zones 2 and 3. P(True) leverages the
self-evaluation capability of large language models (Kadavath et al., 2022). While it primarily uses
logit probability, it is clear that this probability is influenced by internal states and semantics, related to
Zone 4. Anticipated advancements in collaborative
information utilization will heighten computational
demands, especially for nuanced semantic analysis (Duan et al., 2023). This underscores the need
for a careful balance between performance and resource efficiency.
3.1.2

Black-box Methods

Black-box methods assume that all parameters during inference are unknown, allowing access only
to the generations.

Linguistic confidence (verbalized method)
refers to prompting language models to express
uncertainty in human language. This involves discerning different levels of uncertainty from the
model’s responses, such as "I don’t know," "most
probably," or "Obviously" (Mielke et al., 2022) or
prompting the model to output various verbalized
words (e.g., "lowest", "low", "medium", "high",
"highest") or numbers (e.g., "85%"). Xiong et al.
(2023) demonstrated that prompting strategies like
CoT (Wei et al., 2022), top-k (Tian et al., 2023),
and their proposed multi-step method can improve
the calibration of linguistic confidence.
Consistency-based estimation assumes that a
model’s lack of confidence correlates with various
responses, often leading to hallucinatory outputs.
SelfCheckGPT (Manakul et al., 2023b) proposed
a simple sampling-based approach that uses consistency among generations to find potential hallucinations. Five variants are utilized to measure
the consistency: BERTScore (Zhang et al., 2020b),
question-answering, n-gram, natural language inference (NLI) model (He et al., 2023), and LLM
prompting. Lin et al. (2023) proposed to calculate
the similarity matrix between generations and then
estimate the uncertainty based on the analysis of
the similarity matrix, such as the sum of the eigenvalues of the graph Laplacian, the degree matrix,
and the eccentricity.
Surrogate models Shrivastava et al. (2023) introduced white-box models as surrogate models,
like LLaMA-2 (Touvron et al., 2023b) and then
employed logit-based methods to estimate the confidence of the target model when prompted with the
same task. They also showed that integrating such
confidence with linguistic confidence from blackbox LLMs can provide better confidence estimates
across various tasks.
Summary Figure 2b illustrates the information
sources for confidence evaluation when model
states are not accessible: linguistic confidence, consistency, including lexical and semantic similarity,
and surrogate models. Linguistic confidence can
be elicited through prompts, but in practice, a mismatch between these has been observed (Lin et al.,
2022; Liu et al., 2023c). Surrogate models (Shrivastava et al., 2023) facilitate white-box methods
on black-box LLMs. However, they rely on the
assumption of approximate parameter distribution
of models, necessitating further work to validate

their effectiveness. Consistency methods are computationally intensive but have proven effective in
various tasks. They can benefit the remaining two
approaches (Zone 1 and 2), such as the hybrid
method proposed by Xiong et al. (2023). Additionally, integrating all three methods (Zone 4) has
been explored by Shrivastava et al. (2023) to offer
further benefits. Table 1 presents the latest representative works in confidence estimation for large
language models, briefly describing their proposed
methods.
3.2

Calibration Methods

This section categories related work in terms of
calibration objectives: to enhance the quality of
generated text through calibration techniques and
to improve the model’s handling of unknown or ambiguous issues by enabling it to express uncertainty
more accurately. The first half of Table 2 presents
recent work on calibrating LLMs over generation
tasks.
3.2.1

Improve the quality of generation

Many studies (Kumar and Sarawagi, 2019; Wang
et al., 2020; Lu et al., 2022) indicated that the miscalibration of token-level logit probabilities during generation is one of the reasons for the decline in generation quality. Kumar and Sarawagi
(2019) introduced a modified temperature scaling
approach where the temperature value adjusts according to various factors, including the entropy
of attention, token logit, token identity, and input
coverage. Wang et al. (2020) noted a pronounced
prevalence of over-estimated tokens compared to
under-estimated ones. They introduced graduated
label smoothing, applying heightened smoothing
penalties to confident predictions. Xiao and Wang
(2021) and van der Poel et al. (2022) calibrated the
token probability separately by adding a weighted
uncertainty estimated with model ensembles (Lakshminarayanan et al., 2017) and pointwise mutual
information between the source and the target tokens. Zablotskaia et al. (2023) adapted diverse
methods to improve model calibration in neural
summarization tasks.
Zhao et al. (2022) suggested that MLE training
can result in poorly calibrated sentence-level confidence, as the model is only exposed to one gold
reference. They proposed the sequence likelihood
calibration (SLiC) technique to rectify this. It first
generates m multiple sequences {ŷ}m from the
initial model θ0 , then calibrates the model’s confi-

dence with:
X
Lcal (θ, x, ȳ, {ŷ}m ) + λLreg (θ, θ0 , x, ȳ)
{x,ȳ}

(5)
where the calibration loss Lcal aims to align models’ decoded candidates’ sequence likelihood according to their similarity to the reference ȳ, and
the regularization loss Lreg prevents models from
deviating strongly. They further introduced SLiCHF (Zhao et al., 2023a), which was designed to
learn from human preferences.
3.2.2

Improve the linguistic confidence

Mielke et al. (2022) proposed a calibratorcontrolled method for chatbots, which involves a
trained calibrator to return the model confidence
score and fine-tuned generative models to enable
control over linguistic confidence. Lin et al. (2022)
fine-tuned GPT-3 with the human-labeled dataset
containing verbalized words and numbers to express uncertainty naturally. Zhou et al. (2023) empirically found that injecting expressions of uncertainty into prompts significantly increases the
accuracy of GPT-3’s answers and the calibration
scores.
Different datasets (Amayuelas et al., 2023; Yin
et al., 2023; Wang et al., 2023d; Liu et al., 2023a)
have been presented on questions that language
models cannot answer or for which there is no clear
answer. Amayuelas et al. (2023) analyzed how different language models, including both smaller and
open-source models, classify a dataset of various
unanswerable questions. They observed that LLMs
show varying accuracy levels depending on the
question type, while smaller and open-source models tend to perform almost randomly. Liu et al.
(2023a) evaluated both open-source models like
LLaMA-2 (Touvron et al., 2023b), Vicuna (Chiang et al., 2023), and closed-source models such
as GPT-3.5 and GPT-4, focusing on their refusal
rate, accuracy, and uncertainty in handling unanswerable questions.

4

LLMs for Classification Tasks

LLMs are recognized for their efficiency in classification tasks, enabling rapid task implementation
via prompts (Brown et al., 2020a; Zhao et al., 2021).
Although the underlying principles of confidence
estimation are similar to those in generation tasks,
the objectives of calibration and the approaches
differ significantly.

4.1

In-Context Learning

In-context learning (ICL) is a new learning
paradigm with LLMs, where the model learns
to perform a task based on a few examples
and the context in which the task is presented. Assuming that k selected input-label pairs
(x1 , y1 ), · · · , (xk , yk ) are given as demonstrations,
with the predictive probability as the confidence,
ICL makes predictions as follows:
ŷ = arg max P (y|x1 , y1 , · · · , xk , yk , x)

(6)

y

When there are no demonstrations, the model performs zero-shot classification.
Calibration methods We refer to the input-label
pairs as C for context, and the original predictive
probability is denoted as P (y|C, x). Zhao et al.
(2021) introduced a method called contextual calibration. It gauges the model’s bias with contextfree prompts such as "[N/A]", "[MASK]" and an
empty string. Then the context-free score is obtained by P̂cf = P (y|C, [N/A]). Subsequently, it
transforms the scores with W = diag(p̂cf )−1 to
offset the miscalibration. Fei et al. (2023) proposed
domain-context calibration, which estimates the
prior bias for each class with n times model average with random text
of an average sentence length:
1 Pn
P̄rd (y|C) = n i=1 P (y|C, [RANDOM TEXT]).
The prediction is obtained with:
ŷ = arg max
y

P (y|C, x)
P̄rd (y|C)

(7)

Some methods aim to improve few-shot learning performance by combining classic statistical
machine learning techniques. Nie et al. (2022)
enhanced predictions by integrating a k-nearestneighbor classifier with a datastore containing
cached few-shot instance representations, while
Han et al. (2022) introduced prototypical calibration, which employs Gaussian mixture models
(GMM) to learn decision boundaries.
4.2

ICL Application: Multiple-Choice
Question Answering

Multiple-choice question answering (MCQA) is
an application of ICL, which is used in evaluating LLMs by prompting them to answer questions with predefined choices. The context C
contains the question q, and the set of options
I(q) = {o1 , · · · , oK }, where each is prefaced

with an identifier such as "A", and, if available,
with a demonstration as an instruction.
It is worth noting that implementing the evaluation protocols can significantly impact the ranking
of models. For instance, the original evaluation of
the MMLU (Hendrycks et al., 2021) ranks the probabilities of the four option identifiers. The answer
is considered correct when the highest probability corresponds to the correct option. The HELM
implementation (Liang et al., 2022) considers probabilities over the complete vocabulary. The HARNESS implementation1 prefers length-normalized
probabilities of the entire answer sequence.
Calibration methods Jiang et al. (2021) proposed various fine-tuning loss functions and temperature scaling for calibrating the performance
of MQCA datasets. Additionally, they proposed
techniques such as candidate output paraphrasing
and input augmentation to calibrate the confidence.
Holtzman et al. (2021) claimed that surface form
competition occurs when different valid surface
forms compete for probability. Thus, they introduced domain conditional pointwise mutual information (PMIDC), which reweighs each option according to a term that is proportional to its prior
likelihood within the context of the specific zeroshot task. To overcome the bias from the choice position, Zheng et al. (2023) proposed PriDe, which
first decomposes the observed model prediction
distribution into an intrinsic prediction over option
contents and a prior distribution over option identifiers and then estimates the prior by permuting
option contents on a small number of test samples. Kumar (2022) believed that under the neutral context Cϕ , the probabilities of different options should be the same, but obviously, the LLM
cannot meet this condition, so they proposed using log P (ok |C) − sim(C, Cϕ ) log P (ok |Cϕ ) to
make the prediction. Given that C is very similar
to the neutral context Cϕ , the approach will assign
an equal score to each choice.
Summary The second half of Table 2 lists recent
calibration studies over classification tasks. Current calibration methods primarily aim to mitigate
biases associated with labels or choice positions in
MCQA (Zhao et al., 2021; Jiang et al., 2021). A
growing trend in the field is to deepen the understanding of the ICL (Holtzman et al., 2021) and
1

https://github.com/EleutherAI/lm-evaluationharness/tree/v0.3.0

to integrate semantics (Kumar, 2022). Besides, a
systematic benchmark for evaluating different calibration methods is still missing.

5

Applications

Confidence estimation and calibration can be effectively employed in the following applications as an
indispensable component in ensuring reliable AI.
Hallucination detection and mitigation Confidence or uncertainty can be applied as a signal for
detecting and mitigating hallucinations generated
by LLMs (Zhang et al., 2023b; Huang et al., 2023a).
SelfCheckGPT (Manakul et al., 2023a) and SAC 3
(Zhang et al., 2023a) both explored hallucinations
in the generation with self-consistency, while the
latter also checked cross-model response consistency by taking generations from other models as
the reference. Varshney et al. (2023) proposed a
method that leverages the model’s logits to identify potential hallucinations, checks their correctness through a validation procedure, appends the
repaired sentence to the prompt, and continues to
generate.
Ambiguity detection and selective generation
When identifying ambiguity in data or unanswerable questions, reliable LLMs are anticipated to
refrain from providing answers rather than generating responses arbitrarily (Kamath et al., 2020).
Ren et al. (2022) proposed a selective generation
method based on relative Mahalanobis distance.
Zablotskaia et al. (2023) provided a comprehensive benchmark study that evaluates various calibration methods in neural summarization. Cole
et al. (2023) and Hou et al. (2023) respectively employed a disambiguate-and-answer approach and
input clarification ensembling to measure data uncertainty for detecting ambiguous questions.
Uncertainty-guided data exploitation Through
measuring data uncertainty, the most representative instances will be selected for few-shot learning
(Yu et al., 2022) or human annotation (Su et al.,
2022). Regarding the knowledge enhancement to
LLMs, Jiang et al. (2023) proposed an adaptive
multi-retrieval method that first forecasts future
content and retrieves relevant documents stimulated by low-confidence tokens within upcoming
sentences.

6

Future Directions

Comprehensive Benchmarks While confidence
estimation and calibration have wide-ranging applications, a comprehensive benchmark across tasks
and domains is required to better understand and
evaluate these techniques’ robustness and utility.
Addressing this issue requires extensive human
efforts to annotate the responses of LLMs, especially in long-form generation (Huang et al., 2024;
Mishra et al., 2024). Treating LLMs’ long generation for confidence estimation and calibration
by parts, instead of as a whole, offers a promising
direction for further enhancement.
Multi-modal LLMs By employing additional
pre-training with image-text pairings or by finetuning on specialized visual-instruction datasets,
LLMs can be transited into the multimodal domain (Dai et al., 2023; Liu et al., 2023b; Zhu et al.,
2023b). However, it remains unclear whether these
confidence estimation methods are effective for
multimodal large language models (MLLMs) and
whether these models are well-calibrated. We look
forward to more efforts in detecting hallucinations
in MLLMs through confidence estimation and in
calibrating these models to discern events that are
impossible in the real world.
Calibration to human variation Plank (2022)
clarified the prevalent existence of human variation, i.e., humans have different opinions when labeling the same data. Human disagreement (Jiang
and de Marneffe, 2022) can be attributed to task
ambiguity (Tamkin et al., 2022), annotator’s subjectivity (Sap et al., 2022), and input ambiguity
(Meissner et al., 2021). Recent work (Baan et al.,
2022; Lee et al., 2023) demonstrated the misalignment between LLM calibration measures and human disagreement in various learning paradigms.
Expressing the concern regarding different types
of ambiguity (Xiong et al., 2023), abstaining from
answering ambiguous questions (Yoshikawa and
Okazaki, 2023), and further resolving ambiguity
(Varshney and Baral, 2023) are necessary for trustworthy and reliable LLMs aligned with human variation.

7

Conclusion

This survey highlights the critical role of confidence estimation and calibration in addressing errors and biases in LLMs. The evolution of LLMs
has paved the way for novel research opportunities

and presented distinctive challenges. We first introduced the fundamental concepts of confidence
and uncertainty, along with common metrics, estimation methods, and calibration techniques used
in traditional discriminative models. We then identified the challenges these methods face in LLMs.
Next, we delved into the latest research, introducing the principles, advantages, and drawbacks of
various methods in generation and classification
tasks. We concluded by discussing the current applications and future research directions.

Limitations
This survey mainly has the following limitations:
No experimental benchmarks Without original
experiments, this paper cannot offer empirical validation of the theories or concepts. This limits the
paper’s ability to contribute new, verified knowledge to the field.
Potential omissions We have made our best effort to compile the latest advancements. Due to
the rapid development in this field, there is still
a possibility that some important work may have
been overlooked.

Ethical Considerations and Potential Risks
We anticipate no significant ethical concerns in our
work. Our review surveys the latest developments
in this research field, and as we did not conduct
experiments, nor did we engage with risky datasets;
we also did not employ any workers for manual
annotation.

References
Alfonso Amayuelas, Liangming Pan, Wenhu Chen, and
William Wang. 2023. Knowledge of knowledge: Exploring known-unknowns uncertainty with large language models. ArXiv preprint, abs/2305.13712.
Rohan Anil, Andrew M. Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin, Alexandre Passos, Siamak
Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng
Chen, Eric Chu, Jonathan H. Clark, Laurent El
Shafey, Yanping Huang, Kathy Meier-Hellstern, Gaurav Mishra, Erica Moreira, Mark Omernick, Kevin
Robinson, Sebastian Ruder, Yi Tay, Kefan Xiao,
Yuanzhong Xu, Yujing Zhang, Gustavo Hernández
Ábrego, Junwhan Ahn, Jacob Austin, Paul Barham,
Jan A. Botha, James Bradbury, Siddhartha Brahma,
Kevin Brooks, Michele Catasta, Yong Cheng, Colin
Cherry, Christopher A. Choquette-Choo, Aakanksha
Chowdhery, Clément Crepy, Shachi Dave, Mostafa
Dehghani, Sunipa Dev, Jacob Devlin, Mark Díaz,

Nan Du, Ethan Dyer, Vladimir Feinberg, Fangxiaoyu Feng, Vlad Fienber, Markus Freitag, Xavier
Garcia, Sebastian Gehrmann, Lucas Gonzalez, and
et al. 2023. Palm 2 technical report. ArXiv preprint,
abs/2305.10403.
Amos Azaria and Tom Mitchell. 2023. The internal
state of an llm knows when its lying. ArXiv preprint,
abs/2304.13734.
Joris Baan, Wilker Aziz, Barbara Plank, and Raquel
Fernandez. 2022. Stop measuring calibration when
humans disagree. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language
Processing, pages 1892–1915, Abu Dhabi, United
Arab Emirates. Association for Computational Linguistics.
Joris Baan, Nico Daheim, Evgenia Ilia, Dennis Ulmer, Haau-Sing Li, Raquel Fernández, Barbara
Plank, Rico Sennrich, Chrysoula Zerva, and Wilker
Aziz. 2023. Uncertainty in natural language generation: From theory to applications. ArXiv preprint,
abs/2307.15703.
Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. 2015. Neural machine translation by jointly
learning to align and translate. In 3rd International
Conference on Learning Representations, ICLR 2015,
San Diego, CA, USA, May 7-9, 2015, Conference
Track Proceedings.
Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda
Askell, Anna Chen, Nova DasSarma, Dawn Drain,
Stanislav Fort, Deep Ganguli, Tom Henighan, et al.
2022. Training a helpful and harmless assistant with
reinforcement learning from human feedback. ArXiv
preprint, abs/2204.05862.
Andrew P. Bradley. 1997. The use of the area under
the roc curve in the evaluation of machine learning
algorithms. Pattern Recognition, 30(7):1145–1159.
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss,
Gretchen Krueger, Tom Henighan, Rewon Child,
Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,
Clemens Winter, Christopher Hesse, Mark Chen, Eric
Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
Jack Clark, Christopher Berner, Sam McCandlish,
Alec Radford, Ilya Sutskever, and Dario Amodei.
2020a. Language models are few-shot learners. In
Advances in Neural Information Processing Systems
33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 612, 2020, virtual.
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss,
Gretchen Krueger, Tom Henighan, Rewon Child,
Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,

Clemens Winter, Christopher Hesse, Mark Chen, Eric
Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
Jack Clark, Christopher Berner, Sam McCandlish,
Alec Radford, Ilya Sutskever, and Dario Amodei.
2020b. Language models are few-shot learners. In
Advances in Neural Information Processing Systems
33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 612, 2020, virtual.
Collin Burns, Haotian Ye, Dan Klein, and Jacob Steinhardt. 2023. Discovering latent knowledge in language models without supervision. In The Eleventh
International Conference on Learning Representations.
Jiuhai Chen and Jonas Mueller. 2023. Quantifying uncertainty in answers from any language model via
intrinsic and extrinsic confidence assessment. ArXiv
preprint, abs/2308.16175.
Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng,
Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan
Zhuang, Yonghao Zhuang, Joseph E Gonzalez, et al.
2023. Vicuna: An open-source chatbot impressing
gpt-4 with 90%* chatgpt quality. See https://vicuna.
lmsys. org (accessed 14 April 2023).
Jeremy R Cole, Michael JQ Zhang, Daniel Gillick, Julian Martin Eisenschlos, Bhuwan Dhingra, and Jacob
Eisenstein. 2023. Selectively answering ambiguous
questions. ArXiv preprint, abs/2305.14613.
Charles Corbière, Nicolas Thome, Avner Bar-Hen,
Matthieu Cord, and Patrick Pérez. 2019. Addressing failure prediction by learning model confidence.
In Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information
Processing Systems 2019, NeurIPS 2019, December
8-14, 2019, Vancouver, BC, Canada, pages 2898–
2909.
Wenliang Dai, Junnan Li, Dongxu Li, Anthony
Meng Huat Tiong, Junqi Zhao, Weisheng Wang,
Boyang Li, Pascale Fung, and Steven C. H. Hoi.
2023. Instructblip: Towards general-purpose visionlanguage models with instruction tuning. ArXiv
preprint, abs/2305.06500.
Shrey Desai and Greg Durrett. 2020. Calibration of
pre-trained transformers. In Proceedings of the 2020
Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 295–302, Online.
Association for Computational Linguistics.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
Kristina Toutanova. 2019. BERT: Pre-training of
deep bidirectional transformers for language understanding. In Proceedings of the 2019 Conference of
the North American Chapter of the Association for
Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pages
4171–4186, Minneapolis, Minnesota. Association for
Computational Linguistics.

Terrance DeVries and Graham W Taylor. 2018. Learning confidence for out-of-distribution detection in
neural networks. ArXiv preprint, abs/1802.04865.
Jinhao Duan, Hao Cheng, Shiqi Wang, Chenan Wang,
Alex Zavalny, Renjing Xu, Bhavya Kailkhura, and
Kaidi Xu. 2023. Shifting attention to relevance: Towards the uncertainty estimation of large language
models. ArXiv preprint, abs/2307.01379.
Yu Fei, Yifan Hou, Zeming Chen, and Antoine Bosselut.
2023. Mitigating label biases for in-context learning.
ArXiv preprint, abs/2305.19148.
Yarin Gal and Zoubin Ghahramani. 2016. Dropout
as a bayesian approximation: Representing model
uncertainty in deep learning. In Proceedings of the
33nd International Conference on Machine Learning,
ICML 2016, New York City, NY, USA, June 19-24,
2016, volume 48 of JMLR Workshop and Conference
Proceedings, pages 1050–1059. JMLR.org.
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017. On calibration of modern neural networks. In Proceedings of the 34th International Conference on Machine Learning, ICML 2017, Sydney,
NSW, Australia, 6-11 August 2017, volume 70 of
Proceedings of Machine Learning Research, pages
1321–1330. PMLR.

Bairu Hou, Yujian Liu, Kaizhi Qian, Jacob Andreas,
Shiyu Chang, and Yang Zhang. 2023. Decomposing uncertainty for large language models through
input clarification ensembling. ArXiv preprint,
abs/2311.08718.
Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong,
Zhangyin Feng, Haotian Wang, Qianglong Chen,
Weihua Peng, Xiaocheng Feng, Bing Qin, et al.
2023a. A survey on hallucination in large language
models: Principles, taxonomy, challenges, and open
questions. ArXiv preprint, abs/2311.05232.
Yuheng Huang, Jiayang Song, Zhijie Wang, Huaming Chen, and Lei Ma. 2023b. Look before you
leap: An exploratory study of uncertainty measurement for large language models. ArXiv preprint,
abs/2307.10236.
Yukun Huang, Yixin Liu, Raghuveer Thirukovalluru,
Arman Cohan, and Bhuwan Dhingra. 2024. Calibrating long-form generations from large language
models. ArXiv preprint, abs/2402.06544.
Abhyuday Jagannatha and Hong Yu. 2020. Calibrating structured output predictors for natural language
processing. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics,
pages 2078–2092, Online. Association for Computational Linguistics.

Zhixiong Han, Yaru Hao, Li Dong, Yutao Sun, and
Furu Wei. 2022. Prototypical calibration for fewshot learning of language models. ArXiv preprint,
abs/2205.10183.

Nan-Jiang Jiang and Marie-Catherine de Marneffe.
2022. Investigating reasons for disagreement in natural language inference. Transactions of the Association for Computational Linguistics, 10:1357–1374.

Marton Havasi, Rodolphe Jenatton, Stanislav Fort,
Jeremiah Zhe Liu, Jasper Snoek, Balaji Lakshminarayanan, Andrew Mingbo Dai, and Dustin Tran.
2021. Training independent subnetworks for robust
prediction. In 9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021. OpenReview.net.

Zhengbao Jiang, Jun Araki, Haibo Ding, and Graham
Neubig. 2021. How can we know when language
models know? on the calibration of language models
for question answering. Transactions of the Association for Computational Linguistics, 9:962–977.

Pengcheng He, Jianfeng Gao, and Weizhu Chen. 2023.
DeBERTav3: Improving deBERTa using ELECTRAstyle pre-training with gradient-disentangled embedding sharing. In The Eleventh International Conference on Learning Representations.
Dan Hendrycks, Collin Burns, Steven Basart, Andy
Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. 2021. Measuring massive multitask language
understanding. In 9th International Conference on
Learning Representations, ICLR 2021, Virtual Event,
Austria, May 3-7, 2021. OpenReview.net.
Ari Holtzman, Peter West, Vered Shwartz, Yejin Choi,
and Luke Zettlemoyer. 2021. Surface form competition: Why the highest probability answer isn’t
always right. In Proceedings of the 2021 Conference
on Empirical Methods in Natural Language Processing, pages 7038–7051, Online and Punta Cana, Dominican Republic. Association for Computational
Linguistics.

Zhengbao Jiang, Frank F Xu, Luyu Gao, Zhiqing
Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang,
Jamie Callan, and Graham Neubig. 2023. Active
retrieval augmented generation. ArXiv preprint,
abs/2305.06983.
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
Henighan, Dawn Drain, Ethan Perez, Nicholas
Schiefer, Zac Hatfield Dodds, Nova DasSarma,
Eli Tran-Johnson, et al. 2022. Language models
(mostly) know what they know. ArXiv preprint,
abs/2207.05221.
Amita Kamath, Robin Jia, and Percy Liang. 2020. Selective question answering under domain shift. In
Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 5684–
5696, Online. Association for Computational Linguistics.
Alex Kendall and Yarin Gal. 2017. What uncertainties
do we need in bayesian deep learning for computer
vision? In Advances in Neural Information Processing Systems 30: Annual Conference on Neural

Information Processing Systems 2017, December 4-9,
2017, Long Beach, CA, USA, pages 5574–5584.
Jaeyoung Kim, Dongbin Na, Sungchul Choi, and Sungbin Lim. 2023. Bag of tricks for in-distribution calibration of pretrained transformers. In Findings of the
Association for Computational Linguistics: EACL
2023, pages 551–563, Dubrovnik, Croatia. Association for Computational Linguistics.
Lingkai Kong, Haoming Jiang, Yuchen Zhuang, Jie
Lyu, Tuo Zhao, and Chao Zhang. 2020. Calibrated language model fine-tuning for in- and outof-distribution data. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language
Processing (EMNLP), pages 1326–1340, Online. Association for Computational Linguistics.
Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.
Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation.
ArXiv preprint, abs/2302.09664.
Alex Kulesza and Ben Taskar. 2012. Determinantal
point processes for machine learning. Foundations
and Trends® in Machine Learning, 5(2–3):123–286.
Meelis Kull, Miquel Perelló-Nieto, Markus Kängsepp,
Telmo de Menezes e Silva Filho, Hao Song, and
Peter A. Flach. 2019. Beyond temperature scaling:
Obtaining well-calibrated multi-class probabilities
with dirichlet calibration. In Advances in Neural
Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019,
NeurIPS 2019, December 8-14, 2019, Vancouver, BC,
Canada, pages 12295–12305.
Aviral Kumar and Sunita Sarawagi. 2019. Calibration
of encoder decoder models for neural machine translation. ArXiv preprint, abs/1903.00802.
Sawan Kumar. 2022. Answer-level calibration for freeform multiple choice question answering. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers), pages 665–679, Dublin, Ireland. Association
for Computational Linguistics.
Balaji Lakshminarayanan, Alexander Pritzel, and
Charles Blundell. 2017. Simple and scalable predictive uncertainty estimation using deep ensembles.
In Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information
Processing Systems 2017, December 4-9, 2017, Long
Beach, CA, USA, pages 6402–6413.
Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin.
2018. A simple unified framework for detecting outof-distribution samples and adversarial attacks. In
Advances in Neural Information Processing Systems
31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8,
2018, Montréal, Canada, pages 7167–7177.
Noah Lee, Na Min An, and James Thorne. 2023. Can
large language models infer and disagree like humans? ArXiv preprint, abs/2305.13788.

Benjamin A. Levinstein and Daniel A. Herrmann. forthcoming. Still no lie detector for language models:
Probing empirical and conceptual roadblocks. Philosophical Studies, pages 1–27.
Mike Lewis, Yinhan Liu, Naman Goyal, Marjan
Ghazvininejad, Abdelrahman Mohamed, Omer Levy,
Veselin Stoyanov, and Luke Zettlemoyer. 2020.
BART: Denoising sequence-to-sequence pre-training
for natural language generation, translation, and comprehension. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics,
pages 7871–7880, Online. Association for Computational Linguistics.
Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter
Pfister, and Martin Wattenberg. 2023. Inference-time
intervention: Eliciting truthful answers from a language model. ArXiv preprint, abs/2306.03341.
Percy Liang, Rishi Bommasani, Tony Lee, Dimitris
Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian
Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Kumar, et al. 2022. Holistic evaluation of language
models. ArXiv preprint, abs/2211.09110.
Stephanie Lin, Jacob Hilton, and Owain Evans. 2022.
Teaching models to express their uncertainty in
words. ArXiv preprint, abs/2205.14334.
Tsung-Yi Lin, Priya Goyal, Ross B. Girshick, Kaiming He, and Piotr Dollár. 2017. Focal loss for dense
object detection. In IEEE International Conference
on Computer Vision, ICCV 2017, Venice, Italy, October 22-29, 2017, pages 2999–3007. IEEE Computer
Society.
Zhen Lin, Shubhendu Trivedi, and Jimeng Sun. 2023.
Generating with confidence: Uncertainty quantification for black-box large language models. ArXiv
preprint, abs/2305.19187.
Genglin Liu, Xingyao Wang, Lifan Yuan, Yangyi Chen,
and Hao Peng. 2023a. Prudent silence or foolish
babble? examining large language models’ responses
to the unknown. ArXiv preprint, abs/2311.09731.
Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae
Lee. 2023b. Visual instruction tuning. ArXiv
preprint, abs/2304.08485.
Yang Liu, Yuanshun Yao, Jean-Francois Ton, Xiaoying
Zhang, Ruocheng Guo Hao Cheng, Yegor Klochkov,
Muhammad Faaiz Taufiq, and Hang Li. 2023c. Trustworthy llms: a survey and guideline for evaluating
large language models’ alignment. ArXiv preprint,
abs/2308.05374.
Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
Luke Zettlemoyer, and Veselin Stoyanov. 2019.
Roberta: A robustly optimized bert pretraining approach. ArXiv preprint, abs/1907.11692.

Yu Lu, Jiali Zeng, Jiajun Zhang, Shuangzhi Wu, and
Mu Li. 2022. Learning confidence for transformerbased neural machine translation. In Proceedings
of the 60th Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers),
pages 2353–2364, Dublin, Ireland. Association for
Computational Linguistics.
Andrey Malinin and Mark J. F. Gales. 2021a. Uncertainty estimation in autoregressive structured prediction. In 9th International Conference on Learning
Representations, ICLR 2021, Virtual Event, Austria,
May 3-7, 2021. OpenReview.net.
Andrey Malinin and Mark J. F. Gales. 2021b. Uncertainty estimation in autoregressive structured prediction. In 9th International Conference on Learning
Representations, ICLR 2021, Virtual Event, Austria,
May 3-7, 2021. OpenReview.net.
Potsawee Manakul, Yassir Fathullah, Adian Liusie,
Vyas Raina, Vatsal Raina, and Mark Gales. 2023a.
CUED at ProbSum 2023: Hierarchical ensemble
of summarization models. In The 22nd Workshop
on Biomedical Natural Language Processing and
BioNLP Shared Tasks, pages 516–523, Toronto,
Canada. Association for Computational Linguistics.
Potsawee Manakul, Adian Liusie, and Mark JF Gales.
2023b. Selfcheckgpt: Zero-resource black-box hallucination detection for generative large language
models. ArXiv preprint, abs/2303.08896.
Johannes Mario Meissner, Napat Thumwanit, Saku Sugawara, and Akiko Aizawa. 2021. Embracing ambiguity: Shifting the training target of NLI models. In
Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th
International Joint Conference on Natural Language
Processing (Volume 2: Short Papers), pages 862–869,
Online. Association for Computational Linguistics.
Sabrina J. Mielke, Arthur Szlam, Emily Dinan, and YLan Boureau. 2022. Reducing conversational agents’
overconfidence through linguistic calibration. Transactions of the Association for Computational Linguistics, 10:857–872.
Abhika Mishra, Akari Asai, Vidhisha Balachandran,
Yizhong Wang, Graham Neubig, Yulia Tsvetkov, and
Hannaneh Hajishirzi. 2024. Fine-grained hallucination detection and editing for language models. ArXiv
preprint, abs/2401.06855.
Jooyoung Moon, Jihyo Kim, Younghak Shin, and
Sangheum Hwang. 2020. Confidence-aware learning for deep neural networks. In Proceedings of the
37th International Conference on Machine Learning,
ICML 2020, 13-18 July 2020, Virtual Event, volume
119 of Proceedings of Machine Learning Research,
pages 7034–7044. PMLR.
Jishnu Mukhoti, Viveka Kulharia, Amartya Sanyal, Stuart Golodetz, Philip H. S. Torr, and Puneet K. Dokania. 2020. Calibrating deep neural networks using

focal loss. In Advances in Neural Information Processing Systems 33: Annual Conference on Neural
Information Processing Systems 2020, NeurIPS 2020,
December 6-12, 2020, virtual.
Kenton Murray and David Chiang. 2018. Correcting
length bias in neural machine translation. In Proceedings of the Third Conference on Machine Translation:
Research Papers, pages 212–223, Brussels, Belgium.
Association for Computational Linguistics.
Feng Nie, Meixi Chen, Zhirui Zhang, and Xu Cheng.
2022. Improving few-shot performance of language
models via nearest neighbor calibration. ArXiv
preprint, abs/2212.02216.
Jeremy Nixon, Michael W. Dusenberry, Linchuan
Zhang, Ghassen Jerfel, and Dustin Tran. 2019. Measuring calibration in deep learning. In IEEE Conference on Computer Vision and Pattern Recognition
Workshops, CVPR Workshops 2019, Long Beach, CA,
USA, June 16-20, 2019, pages 38–41. Computer Vision Foundation / IEEE.
Seo Yeon Park and Cornelia Caragea. 2022. On the calibration of pre-trained language models using mixup
guided by area under the margin and saliency. In
Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1:
Long Papers), pages 5364–5374, Dublin, Ireland. Association for Computational Linguistics.
Tim Pearce, Alexandra Brintrup, and Jun Zhu. 2021.
Understanding softmax confidence and uncertainty.
ArXiv preprint, abs/2106.04972.
Guilherme Penedo, Quentin Malartic, Daniel Hesslow,
Ruxandra Cojocaru, Alessandro Cappelli, Hamza
Alobeidli, Baptiste Pannier, Ebtesam Almazrouei,
and Julien Launay. 2023. The refinedweb dataset
for falcon LLM: outperforming curated corpora with
web data, and web data only. ArXiv preprint,
abs/2306.01116.
Gabriel Pereyra, George Tucker, Jan Chorowski, Łukasz
Kaiser, and Geoffrey Hinton. 2017. Regularizing
neural networks by penalizing confident output distributions. ArXiv preprint, abs/1701.06548.
Fabio Petroni, Tim Rocktäschel, Sebastian Riedel,
Patrick Lewis, Anton Bakhtin, Yuxiang Wu, and
Alexander Miller. 2019. Language models as knowledge bases? In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference
on Natural Language Processing (EMNLP-IJCNLP),
pages 2463–2473, Hong Kong, China. Association
for Computational Linguistics.
Barbara Plank. 2022. The “problem” of human label
variation: On ground truth in data, modeling and
evaluation. In Proceedings of the 2022 Conference
on Empirical Methods in Natural Language Processing, pages 10671–10682, Abu Dhabi, United Arab
Emirates. Association for Computational Linguistics.

Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya
Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark,
Gretchen Krueger, and Ilya Sutskever. 2021. Learning transferable visual models from natural language
supervision. In Proceedings of the 38th International
Conference on Machine Learning, ICML 2021, 18-24
July 2021, Virtual Event, volume 139 of Proceedings
of Machine Learning Research, pages 8748–8763.
PMLR.
Alec Radford, Jeff Wu, Rewon Child, David Luan,
Dario Amodei, and Ilya Sutskever. 2019. Language
models are unsupervised multitask learners. Technical report.
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine
Lee, Sharan Narang, Michael Matena, Yanqi Zhou,
Wei Li, and Peter J. Liu. 2020. Exploring the limits
of transfer learning with a unified text-to-text transformer. J. Mach. Learn. Res., 21:140:1–140:67.
Nils Reimers and Iryna Gurevych. 2019. SentenceBERT: Sentence embeddings using Siamese BERTnetworks. In Proceedings of the 2019 Conference on
Empirical Methods in Natural Language Processing
and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages
3982–3992, Hong Kong, China. Association for Computational Linguistics.
Jie Ren, Jiaming Luo, Yao Zhao, Kundan Krishna, Mohammad Saleh, Balaji Lakshminarayanan, and Peter J Liu. 2022. Out-of-distribution detection and
selective generation for conditional language models.
ArXiv preprint, abs/2209.15558.
Stephen Roller, Emily Dinan, Naman Goyal, Da Ju,
Mary Williamson, Yinhan Liu, Jing Xu, Myle Ott,
Eric Michael Smith, Y-Lan Boureau, and Jason Weston. 2021. Recipes for building an open-domain
chatbot. In Proceedings of the 16th Conference of
the European Chapter of the Association for Computational Linguistics: Main Volume, pages 300–325,
Online. Association for Computational Linguistics.
Maarten Sap, Swabha Swayamdipta, Laura Vianna,
Xuhui Zhou, Yejin Choi, and Noah A. Smith. 2022.
Annotators with attitudes: How annotator beliefs
and identities bias toxic language detection. In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational
Linguistics: Human Language Technologies, pages
5884–5906, Seattle, United States. Association for
Computational Linguistics.
Artem Shelmanov, Evgenii Tsymbalov, Dmitri Puzyrev,
Kirill Fedyanin, Alexander Panchenko, and Maxim
Panov. 2021. How certain is your Transformer? In
Proceedings of the 16th Conference of the European
Chapter of the Association for Computational Linguistics: Main Volume, pages 1833–1840, Online.
Association for Computational Linguistics.
Vaishnavi Shrivastava, Percy Liang, and Ananya Kumar.
2023. Llamas know what gpts don’t show: Surrogate

models for confidence estimation. ArXiv preprint,
abs/2311.08877.
Chenglei Si, Chen Zhao, Sewon Min, and Jordan BoydGraber. 2022. Re-examining calibration: The case
of question answering. In Findings of the Association for Computational Linguistics: EMNLP 2022,
pages 2814–2829, Abu Dhabi, United Arab Emirates.
Association for Computational Linguistics.
Hongjin Su, Jungo Kasai, Chen Henry Wu, Weijia Shi,
Tianlu Wang, Jiayi Xin, Rui Zhang, Mari Ostendorf,
Luke Zettlemoyer, Noah A Smith, et al. 2022. Selective annotation makes language models better fewshot learners. ArXiv preprint, abs/2209.01975.
Hao Sun, Boris van Breugel, Jonathan Crabbe, Nabeel
Seedat, and Mihaela van der Schaar. 2022. Daux: a
density-based approach for uncertainty explanations.
ArXiv preprint, abs/2207.05161.
Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe,
Jonathon Shlens, and Zbigniew Wojna. 2016. Rethinking the inception architecture for computer vision. In 2016 IEEE Conference on Computer Vision
and Pattern Recognition, CVPR 2016, Las Vegas,
NV, USA, June 27-30, 2016, pages 2818–2826. IEEE
Computer Society.
Alex Tamkin, Kunal Handa, Avash Shrestha, and Noah
Goodman. 2022. Task ambiguity in humans and
language models. ArXiv preprint, abs/2212.10711.
Katherine Tian, Eric Mitchell, Allan Zhou, Archit
Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn,
and Christopher Manning. 2023. Just ask for calibration: Strategies for eliciting calibrated confidence
scores from language models fine-tuned with human
feedback. In Proceedings of the 2023 Conference
on Empirical Methods in Natural Language Processing, pages 5433–5442, Singapore. Association for
Computational Linguistics.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
Martinet, Marie-Anne Lachaux, Timothée Lacroix,
Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
Azhar, Aurélien Rodriguez, Armand Joulin, Edouard
Grave, and Guillaume Lample. 2023a. Llama: Open
and efficient foundation language models. ArXiv
preprint, abs/2302.13971.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
Martinet, Marie-Anne Lachaux, Timothée Lacroix,
Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
Azhar, et al. 2023b. Llama: Open and efficient foundation language models. ArXiv preprint,
abs/2302.13971.
Liam van der Poel, Ryan Cotterell, and Clara Meister. 2022. Mutual information alleviates hallucinations in abstractive summarization. In Proceedings
of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 5956–5965, Abu
Dhabi, United Arab Emirates. Association for Computational Linguistics.

Neeraj Varshney and Chitta Baral. 2023.
Postabstention: Towards reliably re-attempting the abstained instances in QA. In Proceedings of the 61st
Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), pages 967–982,
Toronto, Canada. Association for Computational Linguistics.
Neeraj Varshney, Wenlin Yao, Hongming Zhang, Jianshu Chen, and Dong Yu. 2023. A stitch in time saves
nine: Detecting and mitigating hallucinations of
llms by validating low-confidence generation. ArXiv
preprint, abs/2307.03987.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz
Kaiser, and Illia Polosukhin. 2017. Attention is all
you need. In Advances in Neural Information Processing Systems 30: Annual Conference on Neural
Information Processing Systems 2017, December 4-9,
2017, Long Beach, CA, USA, pages 5998–6008.
Artem Vazhentsev, Gleb Kuzmin, Artem Shelmanov,
Akim Tsvigun, Evgenii Tsymbalov, Kirill Fedyanin,
Maxim Panov, Alexander Panchenko, Gleb Gusev,
Mikhail Burtsev, Manvel Avetisian, and Leonid
Zhukov. 2022. Uncertainty estimation of transformer
predictions for misclassification detection. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers), pages 8237–8252, Dublin, Ireland. Association for Computational Linguistics.
Artem Vazhentsev, Gleb Kuzmin, Akim Tsvigun,
Alexander Panchenko, Maxim Panov, Mikhail Burtsev, and Artem Shelmanov. 2023a. Hybrid uncertainty quantification for selective text classification
in ambiguous tasks. In Proceedings of the 61st Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), pages 11659–
11681, Toronto, Canada. Association for Computational Linguistics.
Artem Vazhentsev, Akim Tsvigun, Roman Vashurin,
Sergey Petrakov, Daniil Vasilev, Maxim Panov,
Alexander Panchenko, and Artem Shelmanov. 2023b.
Efficient out-of-domain detection for sequence to sequence models. In Findings of the Association for
Computational Linguistics: ACL 2023, pages 1430–
1454, Toronto, Canada. Association for Computational Linguistics.
Vikas Verma, Alex Lamb, Christopher Beckham, Amir
Najafi, Ioannis Mitliagkas, David Lopez-Paz, and
Yoshua Bengio. 2019. Manifold mixup: Better representations by interpolating hidden states. In Proceedings of the 36th International Conference on Machine
Learning, ICML 2019, 9-15 June 2019, Long Beach,
California, USA, volume 97 of Proceedings of Machine Learning Research, pages 6438–6447. PMLR.
Cunxiang Wang, Xiaoze Liu, Yuanhao Yue, Xiangru
Tang, Tianhang Zhang, Jiayang Cheng, Yunzhi Yao,
Wenyang Gao, Xuming Hu, Zehan Qi, Yidong Wang,
Linyi Yang, Jindong Wang, Xing Xie, Zheng Zhang,

and Yue Zhang. 2023a. Survey on factuality in large
language models: Knowledge, retrieval and domainspecificity. ArXiv preprint, abs/2310.07521.
Cunxiang Wang, Xiaoze Liu, Yuanhao Yue, Xiangru Tang, Tianhang Zhang, Cheng Jiayang, Yunzhi
Yao, Wenyang Gao, Xuming Hu, Zehan Qi, et al.
2023b. Survey on factuality in large language models: Knowledge, retrieval and domain-specificity.
ArXiv preprint, abs/2310.07521.
Shuo Wang, Zhaopeng Tu, Shuming Shi, and Yang Liu.
2020. On the inference calibration of neural machine
translation. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics,
pages 3070–3079, Online. Association for Computational Linguistics.
Xiaosu Wang, Yun Xiong, Beichen Kang, Yao Zhang,
Philip S. Yu, and Yangyong Zhu. 2023c. Reducing
negative effects of the biases of language models in
zero-shot setting. In Proceedings of the Sixteenth
ACM International Conference on Web Search and
Data Mining, WSDM ’23, page 904–912, New York,
NY, USA. Association for Computing Machinery.
Yuxia Wang, Haonan Li, Xudong Han, Preslav Nakov,
and Timothy Baldwin. 2023d. Do-not-answer: A
dataset for evaluating safeguards in LLMs. ArXiv
preprint, abs/2308.13387.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
et al. 2022. Chain-of-thought prompting elicits reasoning in large language models. Advances in Neural
Information Processing Systems, 35:24824–24837.
Jason Wei and Kai Zou. 2019. EDA: Easy data augmentation techniques for boosting performance on text
classification tasks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language
Processing and the 9th International Joint Conference on Natural Language Processing (EMNLPIJCNLP), pages 6382–6388, Hong Kong, China. Association for Computational Linguistics.
Yijun Xiao and William Yang Wang. 2021. On hallucination and predictive uncertainty in conditional
language generation. In Proceedings of the 16th Conference of the European Chapter of the Association
for Computational Linguistics: Main Volume, pages
2734–2744, Online. Association for Computational
Linguistics.
Yuxin Xiao, Paul Pu Liang, Umang Bhatt, Willie
Neiswanger, Ruslan Salakhutdinov, and LouisPhilippe Morency. 2022. Uncertainty quantification
with pre-trained language models: A large-scale empirical analysis. In Findings of the Association for
Computational Linguistics: EMNLP 2022, pages
7273–7284, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.
Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie
Fu, Junxian He, and Bryan Hooi. 2023. Can llms
express their uncertainty? an empirical evaluation

of confidence elicitation in llms. ArXiv preprint,
abs/2306.13063.
Zhangyue Yin, Qiushi Sun, Qipeng Guo, Jiawen Wu,
Xipeng Qiu, and Xuanjing Huang. 2023. Do large
language models know what they don’t know? ArXiv
preprint, abs/2305.18153.
KiYoon Yoo, Jangho Kim, Jiho Jang, and Nojun Kwak.
2022. Detection of word adversarial examples in text
classification: Benchmark and baseline via robust
density estimation. ArXiv preprint, abs/2203.01677.
Hiyori Yoshikawa and Naoaki Okazaki. 2023. SelectiveLAMA: Selective prediction for confidence-aware
evaluation of language models. In Findings of the Association for Computational Linguistics: EACL 2023,
pages 2017–2028, Dubrovnik, Croatia. Association
for Computational Linguistics.
Yue Yu, Rongzhi Zhang, Ran Xu, Jieyu Zhang, Jiaming Shen, and Chao Zhang. 2022. Cold-start data
selection for few-shot language model fine-tuning:
A prompt-based uncertainty propagation approach.
ArXiv preprint, abs/2209.06995.
Polina Zablotskaia, Du Phan, Joshua Maynez, Shashi
Narayan, Jie Ren, and Jeremiah Liu. 2023. On uncertainty calibration and selective generation in probabilistic neural summarization: A benchmark study.
ArXiv preprint, abs/2304.08653.
Hongyi Zhang, Moustapha Cissé, Yann N. Dauphin, and
David Lopez-Paz. 2018. mixup: Beyond empirical
risk minimization. In 6th International Conference
on Learning Representations, ICLR 2018, Vancouver,
BC, Canada, April 30 - May 3, 2018, Conference
Track Proceedings. OpenReview.net.
Jiaxin Zhang, Zhuohang Li, Kamalika Das, Bradley A.
Malin, and Kumar Sricharan. 2023a. Sac3: Reliable
hallucination detection in black-box language models
via semantic-aware cross-check consistency. ArXiv
preprint, abs/2311.01740.
Jingqing Zhang, Yao Zhao, Mohammad Saleh, and Peter J. Liu. 2020a. PEGASUS: pre-training with extracted gap-sentences for abstractive summarization.
In Proceedings of the 37th International Conference
on Machine Learning, ICML 2020, 13-18 July 2020,
Virtual Event, volume 119 of Proceedings of Machine
Learning Research, pages 11328–11339. PMLR.
Shujian Zhang, Chengyue Gong, and Eunsol Choi. 2021.
Knowing more about questions can help: Improving
calibration in question answering. In Findings of
the Association for Computational Linguistics: ACLIJCNLP 2021, pages 1958–1970, Online. Association
for Computational Linguistics.
Susan Zhang, Stephen Roller, Naman Goyal, Mikel
Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona Diab, Xian Li, Xi Victoria Lin, et al. 2022.
Opt: Open pre-trained transformer language models.
ArXiv preprint, abs/2205.01068.

Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q.
Weinberger, and Yoav Artzi. 2020b. Bertscore: Evaluating text generation with BERT. In 8th International Conference on Learning Representations,
ICLR 2020, Addis Ababa, Ethiopia, April 26-30,
2020. OpenReview.net.
Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu,
Tingchen Fu, Xinting Huang, Enbo Zhao, Yu Zhang,
Yulong Chen, et al. 2023b. Siren’s song in the ai
ocean: A survey on hallucination in large language
models. ArXiv preprint, abs/2309.01219.
Yao Zhao, Rishabh Joshi, Tianqi Liu, Misha Khalman,
Mohammad Saleh, and Peter J Liu. 2023a. Slic-hf:
Sequence likelihood calibration with human feedback. ArXiv preprint, abs/2305.10425.
Yao Zhao, Misha Khalman, Rishabh Joshi, Shashi
Narayan, Mohammad Saleh, and Peter J Liu.
2022. Calibrating sequence likelihood improves
conditional language generation. ArXiv preprint,
abs/2210.00045.
Yukun Zhao, Lingyong Yan, Weiwei Sun, Guoliang
Xing, Chong Meng, Shuaiqiang Wang, Zhicong
Cheng, Zhaochun Ren, and Dawei Yin. 2023b.
Knowing what llms do not know: A simple yet
effective self-detection method. ArXiv preprint,
abs/2310.17918.
Zihao Zhao, Eric Wallace, Shi Feng, Dan Klein, and
Sameer Singh. 2021. Calibrate before use: Improving few-shot performance of language models. In
Proceedings of the 38th International Conference on
Machine Learning, ICML 2021, 18-24 July 2021, Virtual Event, volume 139 of Proceedings of Machine
Learning Research, pages 12697–12706. PMLR.
Chujie Zheng, Hao Zhou, Fandong Meng, Jie Zhou,
and Minlie Huang. 2023. Large language models are
not robust multiple choice selectors. ArXiv preprint,
abs/2309.03882.
Kaitlyn Zhou, Dan Jurafsky, and Tatsunori Hashimoto.
2023. Navigating the grey area: Expressions of
overconfidence and uncertainty in language models.
ArXiv preprint, abs/2302.13439.
Chiwei Zhu, Benfeng Xu, Quan Wang, Yongdong
Zhang, and Zhendong Mao. 2023a. On the calibration of large language models and alignment. ArXiv
preprint, abs/2311.13240.
Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and
Mohamed Elhoseiny. 2023b. Minigpt-4: Enhancing
vision-language understanding with advanced large
language models. ArXiv preprint, abs/2304.10592.

Study

Model

(Desai and Durrett, 2020)

Nature Language Inference,
BERT (Devlin et al., 2019), Paraphrase Detection,
Commonsense Reasoning
RoBERTa (Liu et al., 2019)

TS, LS

(Kim et al., 2023)

RoBERTa (Liu et al., 2019)

BL, ERL, MixUp, DeepEnsemble,
MCDropout, MIMO

(Park and Caragea, 2022)

BERT (Devlin et al., 2019),
RoBERTa (Liu et al., 2019)
BERT-based Span Extractor
(Zhang et al., 2021)
BERT-based Span Extractor
(Si et al., 2022)

(Zhang et al., 2021)
(Si et al., 2022)

Task

Calibration Methods

Text Classification
Nature Language Inference,
Paraphrase Detection,
Commonsense Reasoning

TS, LS, MixUp, Manifold-MixUp,
AUM-guided MixUp

Extractive Question Answering

FBC

Extractive Question Answering

LS, TS, FBC

Table 3: Studies of discriminative LM calibration. Calibration methods: LS=label smoothing, TS=temperature
scaling, BL=brier loss, ERL=entropy regularization loss, BE=Bayesian Ensemble, SNGP: spectral-normalized
Gaussian process, FBC=feature-based calibrator

A

Appendix

A.1

Confidence Estimation Methods

The methods for confidence estimation have been
extensively studied and can generally be categorized into the following groups:
Logit-based estimation Given the model input
x, the logit z, along with the prediction ŷ (i.e.,
the class with the highest probability emitted by
softmax activation σ), the model confidence is estimated directly using the probability value:

Gales, 2021b; Shelmanov et al., 2021; Vazhentsev
et al., 2022), and there is the need to optimize the
computation. For example, determinantal point process (Kulesza and Taskar, 2012) can be applied to
facilitate MCDropout by sampling diverse neurons
in the dropout layer (Shelmanov et al., 2021).

There are methods for estimating confidence based
on transformations of the logit probabilities, such
as examining the gap between the two highest probabilities (Yoshikawa and Okazaki, 2023) or utilizing entropy, which indicates the uncertainty with a
larger value.

Density-based estimation Density-based approaches (Lee et al., 2018; Yoo et al., 2022) are
based on the assumption that regions of the input space where training data is dense are regions
where the model is likely to be more confident in its
predictions. Conversely, regions with sparse training data are areas of higher uncertainty. Lee et al.
(2018) first proposed a Mahalanobis distance-based
confidence score, which calculates the distance between one test point and a Gaussian distribution
fitting test data. The confidence estimation is obtained by exponentiating the negative value of the
distance.

Ensemble-based & Bayesian methods DeepEnsemble methods (Lakshminarayanan et al., 2017)
train multiple neural networks independently and
estimate the uncertainty by computing the variance
of the outputs from these models. Monte Carlo
dropout (MCDropout, Gal and Ghahramani 2016)
methods extend the dropout techniques to estimating uncertainty. As in the training phase, dropout
is also applied during inference, and multiple forward passes are performed to obtain predictions.
The final prediction is obtained through averaging
predictions, with the variability of the predictions
reflecting the model uncertainty.
Methods such as deep-ensemble and MCDropout introduce a heavy computational overhead,
especially when applied to LLMs (Malinin and

Confidence learning employs a specific network
branch to learn the confidence of model predictions.
DeVries and Taylor (2018) leveraged a confidence
estimation branch to forecast scalar confidence, and
the original probability is modified by interpolating
the ground truth according to the confidence to provide “hints” during the training process. Additionally, it discourages the network from always asking
for hints by applying a small penalty. Corbière et al.
(2019) empirically demonstrated that confidence
based on true class probability (TCP) is better for
distinguishing between correct and incorrect predictions. Given the ground truth y, TCP can be
represented as P (y|x). However, y is not available
when estimating the confidence of the predictions.
Hence, Corbière et al. (2019) used a confidence

confsp (x, ŷ) = P (ŷ|x) = σ(z)ŷ

(8)

learning network to learn TCP confidence during
training.
A.2

Model Calibration

Calibration methods can be categorized based on
their execution time as in-training and post-hoc
methods.
A.2.1

In-Training Calibration

Research indicates that model generalization methods can be used for calibration (Kim et al., 2023),
and calibration methods can enhance model performance, particularly in out-of-domain generation (Desai and Durrett, 2020).
Novel loss functions Many studies considered
the cross-entropy (CE) loss to be one of the causes
leading to model miscalibration (Mukhoti et al.,
2020; Kim et al., 2023). Mukhoti et al. (2020)
demonstrated that focal loss (Lin et al., 2017), designed to give more importance to hard-to-classify
examples and to down-weight the easy-to-classify
examples, can improve the calibration of neural networks. The correctness ranking loss (CRL; Moon
et al. 2020) calibrated models by penalizing incorrect rankings within the same batch and by using the difference in proportions as the margin to
differentiate sample confidence. Besides, entropy
regularization loss (ERL; Pereyra et al. 2017) and
label smoothing (LS; Szegedy et al. 2016) were
introduced to discourage overly confident output
distributions.
Data augmentation involves creating new training examples by applying various transformations
or perturbations to the original data. It has been
widely used for calibration of discriminative LMs
by alleviating the issue of over-confidence, such
as MixUp (Zhang et al., 2018), EDA (Wei and
Zou, 2019), Manifold-MixUp (Verma et al., 2019),
MIMO (Havasi et al., 2021) and AUM-guided
MixUp (Park and Caragea, 2022).
Ensemble and Bayesian methods were initially
introduced to quantify model uncertainty. However,
both can also be valuable for model calibration, as
they can enhance accuracy, mitigate overfitting,
and reduce overconfidence (Kong et al., 2020; Kim
et al., 2023).
A.2.2

et al., 2017). Using a validation set, they finetune the predicted probabilities to better align with
the true outcomes, leveraging the negative loglikelihood (NLL) loss. Among them, temperature
scaling (TS) is popular due to its low complexity
and efficiency. It involves re-weighting the logits
before the softmax function by a learned scalar τ ,
known as the temperature.

Post-Hoc Calibration

Scaling methods are exemplified by matrix scaling, vector scaling and temperature scaling (Guo

Feature-based calibrator leverages both input
features and model predictions to refine the predicted probabilities. To train the calibrator, one
first applies a trained model on a validation dataset.
Subsequently, both the original input features and
the model’s predictions from this dataset are passed
to a binary classifier (Jagannatha and Yu, 2020;
Jiang et al., 2021; Si et al., 2022).
A.3

Summary

Confidence estimation Logit-based methods
stand out as the most straightforward to implement
and interpret. Reducing computational cost and
improving the sampling efficiency pose challenges
to ensemble-based and Bayesian methods. Densitybased estimation can be used to identify which data
points are associated with different types of uncertainties. However, it requires assumptions of
data distribution (Baan et al., 2023) and can also
be computationally intensive when dealing with
large datasets (Sun et al., 2022). Confidence learning can acquire task-relevant confidence; however,
it requires modifying the neural network and performing specific training.
Model calibration Post-hoc methods are generally model-independent and can calibrate probabilities without impacting the model’s performance (Guo et al., 2017). Desai and Durrett
(2020) empirically found that temperature scaling effectively reduces calibration error in-domain,
whereas label smoothing is more beneficial in outof-domain settings. Kim et al. (2023) found that
augmentation can enhance both classification accuracy and calibration performance. However, ensemble methods may sometimes degrade model
calibration if individual members produce similar
predictions due to overfitting. Table 3 represents
significant work in calibrating discriminative LMs.
We have comprehensively listed the models, tasks,
and calibration methods they employed.

