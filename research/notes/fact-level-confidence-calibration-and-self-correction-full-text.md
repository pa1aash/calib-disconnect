---
title: Fact-Level Confidence Calibration and Self-Correction (full text)
id: fact-level-confidence-calibration-and-self-correction-full-text
tags:
- code-llm-confidence-positioning-d82d00
- related-l4
created: '2026-11-09T23:10:58.275681Z'
updated: '2026-11-09T23:27:44.688585Z'
source: https://arxiv.org/pdf/2411.13343
status: review
type: note
content_type: paper
deprecated: false
summary: FULL TEXT (arXiv 2411.13343, Yuan et al., Nov 2024). Fact-level calibration
  (F-ECE) to relevance-weighted correctness and ConFix confidence-guided self-correction;
  verbalization, isTrueLogit, consistency on ASQA, LongFact; four datasets, six models.
  Long-form factual text only; no code. Related for L4 fine-grained confidence outside
  code.
---

Fact-Level Confidence Calibration and Self-Correction
Yige Yuan1,2 , Bingbing Xu1 , Hexiang Tan1,2 , Fei Sun1 ,
Teng Xiao3 , Wei Li1 , Huawei Shen1,2 , Xueqi Cheng1,2
1
Institute of Computing Technology, Chinese Academy of Sciences
2
University of Chinese Academy of Sciences, 3 Penn State University

arXiv:2411.13343v1 [cs.CL] 20 Nov 2024

Abstract

What is the Deep Blue?
Deep Blue is a go computer developed by IBM that famously

Confidence calibration in LLMs, i.e., aligning their self-assessed confidence with the actual accuracy of their responses, enabling them
to self-evaluate the correctness of their outputs. However, current calibration methods
for LLMs typically estimate two scalars to
represent overall response confidence and correctness, which is inadequate for long-form
generation where the response includes multiple atomic facts and may be partially confident and correct. These methods also overlook the relevance of each fact to the query.
To address these challenges, we propose a
fact-level calibration framework that operates
at a finer granularity, calibrating confidence
to relevance-weighted correctness at the fact
level. Furthermore, comprehensive analysis under the framework inspired the development
of confidence-guided fact-level self-correction
(ConFix), which uses high-confidence facts
within a response as additional knowledge to
improve low-confidence ones. Extensive experiments across four datasets and six models demonstrate that ConFix effectively mitigates hallucinations without requiring external
knowledge sources such as retrieval systems1 .

1

conﬁdence: 0.30

conﬁdence: 0.90

defeated world champion Garry Kasparov in 1997.
conﬁdence: 0.85

conﬁdence: 0.80

Deep Blue is developed by IBM.
Deep Blue defeated world champion Garry Kasparov.

High
Confidence

enhance

The defeat is in 1997.
Deep Blue is a go computer.

go

chess

Low
Confidence

Deep Blue is a chess computer developed by IBM that famously
conﬁdence: 0.90

conﬁdence: 0.90

defeated world champion Garry Kasparov in 1997.
conﬁdence: 0.85

conﬁdence: 0.80

Figure 1: Motivation of our fact-level confidence calibration and confidence-guided self-correction.

in domains where reliability is crucial, such as in
the legal, financial, and educational fields.
Echoing the ancient adage that “To know what
you know and what you do not know, that is
true wisdom”, confidence calibration in LLMs
emerges as an effective method to mitigate hallucinations (Li et al., 2024; Liu et al., 2023; Huang
et al., 2024). By confidence calibrating, models can
better align their self-assessed confidence with the
actual accuracy of responses, empowering them to
self-evaluate the correctness of outputs. This mechanism offers an effective way to identify hallucinations by using the model’s confidence as a basis to
either trust or question the model’s response.
However, current confidence calibration methods for LLMs (Guo et al., 2017a; Nguyen and
O’Connor, 2015) typically estimate two scalars
to represent the overall confidence and correctness for the entire response. This approach is
unreasonable for long-form generation, where responses may contain multiple atomic facts (illustrated in Fig.1). In such cases, considering the
varying of facts in one response, the confidence
and correctness should also be diverse, capable of
reflecting higher certainty in some facts and greater
uncertainty in others. Furthermore, within long-

Introduction

Large Language Models (LLMs) have recently
shown remarkable capabilities in understanding
and generating language that closely resembles human communication (Brown et al., 2020; OpenAI,
2023). Nonetheless, a major obstacle to their reliability is the prevalence of hallucinations (Lin
et al., 2021; Zhang et al., 2023; Li et al., 2023a;
Golovneva et al., 2022; Bang et al., 2023), a phenomenon where the models generate incorrect and
unreliable outputs. This issue not only undermines
user trust but also restricts the application of LLMs
1

Code is available at https://github.com/yuanyige/
fact-calibration

1

Self-Correction Method: We propose ConFix
based on the fact-level calibration framework to
enhance the generation and reduce hallucinations
without relying on external knowledge sources.

form responses (Xiao et al., 2024b,a), certain facts
exist that may indeed be correct but lack relevance
to the query. Previous calibration methods predominantly (Huang et al., 2024; Liu et al., 2023) focus
on correctness while neglecting the relevance.
To address these challenges, we propose a novel
framework for confidence calibration operating at a
finer fact-level granularity. Within this framework,
the confidence assessment of each fact incorporates two key aspects: correctness and relevance.
Correctness indicates the factual accuracy of the
fact, while relevance measures the extent to which
the fact is related to the query. Calibration of a
response is defined as the degree of alignment between confidence and correctness weighted by relevance across all facts. This framework endows the
model with the capability to exhibit partial confidence and correctness in individual facts. Extensive
analysis based on the aforementioned framework
yields three interesting findings: (1) Calibration on
fact-level imposes a stricter standard than calibration on response-level. (2) Overconfidence issue
stems from implicit facts. (3) High variance exists
in fact-level confidence within a response.
The aforementioned three observations inspire
the development of Confidence-Guided Fact-Level
Self-Correction (ConFix) to enhance the generation
and mitigate hallucinations (illustrated in Fig.1).
For a response, ConFix first leverages the aforementioned framework to segment the response into
multiple facts and evaluate their confidence vector.
It then uses the high-confidence facts and their associated confidence score as additional knowledge
to augment low-confidence facts, with the aim of
all facts within the response achieving high confidence. ConFix can self-enhance to mitigate hallucinations without the need for external knowledge
sources such as retrieval systems. Experiments
with ConFix across four datasets and six models reveal that it can significantly reduce the occurrence
of hallucinations, thereby increasing the models’ reliability and enabling their real-world applications.
In summary, our main contributions are:
Fact-Level Calibration Framework: The proposed fact-level calibration framework operates at
a finer level of granularity to align the confidence
with the correctness weighted by relevance across
all facts. This framework enables LLMs to exhibit
partial confidence and accuracy in individual facts.
Insightful Observations: We uncover insightful
observations regarding the model’s scale and its
calibration capability on fact- and response-levels.

2

Related Work and Formulation

Related Work Several prior works, such as SelfCheckGPT (Manakul et al., 2023; Wang et al.,
2024; Zhang et al., 2024) and so on (Mündler et al.,
2023), focus on uncertainty-based hallucination
detection. While these methods share a common
goal with ours, there are several key distinctions:
(1) Their focus is primarily on detection, whereas
our work goes beyond that by investigating the
mechanisms of fine-grained confidence estimation
and identifying three novel phenomena. (2) We
introduce a self-correction method that functions
without relying on external knowledge, in contrast
to their approaches, which are limited to detection.
(3) While their methods operate at the sentence
level, we take a more granular approach by breaking down text into atomic facts, enabling a deeper
analysis of confidence at the fact level. (4) Furthermore, we propose a general framework for confidence estimation, with their methods representing specific instances within this broader approach.
There are also works like FactScore (Min et al.,
2023) that focus on fact-level factuality evaluation
by leveraging external knowledge. In contrast, our
method centers on the model’s internal confidence
and calibration, providing a self-correction solution
that operates without the external knowledge.
Problem Formulation Let the dataset be D =
{x1 , x2 , . . . , xN }, where xi represents the i-th
query, and the model’s responses are A =
{y1 , y2 , . . . , yN }. Each query-answer pair (xi , yi )
is associated with a confidence score conf i , indicating the model’s certainty to the answer, and a
correctness score corri , measuring the objective accuracy of the answer. In long-form generation, we
extend this to the fact level, where each response
i
yi contains Mi individual facts {fij }M
j=1 , with each

fact fij assigned a relevance score relji , a correctness score corrji , and a confidence score conf ji . The
aim is to align confidence with relevance-weighted
correctness across all facts in each response.

3

Fact-Level Confidence Calibration

In this section, we first outline the motivation and
provide a overview of the Fact-Level Confidence
2

Q What is the Deep Blue?
A Deep Blue is a go computer developed by IBM that famously defeated world champion Garry Kasparov in 1997.
Fact Extraction

Confidence Estimation

Multiple Facts

Confidence

External Evaluation

Correctness Relevance

Deep Blue is a go computer.

0.30

0.00

1.00

Deep Blue is developed by IBM.

0.90

1.00

1.00

Deep Blue defeated world champion Garry Kasparov.

0.85

1.00

1.00

The defeat is in 1997.

0.80

1.00

0.70

<latexit sha1_base64="4u5SlqdGLI3QPntIzttsm235sxw=">AAACdHicbVHLahsxFNVM0zZx+nDbRRbpQqkT6CZmJtDHJhASUrIqKdRJwOMOGvmOLSxpBulOqJH1Bf277voZ3XRd2XEgrwuCo3PPQVfnFrUUFpPkTxQ/Wnn85OnqWmv92fMXL9uvXp/ZqjEcerySlbkomAUpNPRQoISL2gBThYTzYnI0759fgrGi0t9xWsNAsZEWpeAMA5W3f21niuHYKPclQ/iJbtcfHx17uk8z26jc6f3U/3BfPc1Kw7ibHeaTmV/cJZQ4o9duXhkThBOfu2uKXY68p7s3JLp8UJIZMRrjbDtvd5Jusih6H6RL0CHLOs3bv7NhxRsFGrlk1vbTpMaBYwYFl+BbWWOhZnzCRtAPUDMFduAWoXm6E5ghLSsTjka6YG86HFPWTlURlPNp7d3enHyo12+w/DxwQtcNguZXD5WNpFjR+QboUBjgKKcBMG5EmJXyMQvpYthTK4SQ3v3yfXC2100/dj982+scHC7jWCWb5B15T1LyiRyQE3JKeoSTv9FGRKOt6F/8Nu7EO1fSOFp63pBbFXf/AzQOwcc=</latexit>

Evaluation Metric

F-ECE =

PN

n=1

|Bk |
N

corrkavg

+

conf kavg

Figure 2: An illustration of our fact-level confidence calibration framework for fine-grained LLM calibration.

Calibration framework. Following this, we discuss
three key observations arising from our framework
that offer deeper insights. Finally, we conclude by
summarizing how these observations inform and
shape our approach to conduct self-correction.
3.1

tion, (2) correctness and relevance evaluation, (3)
confidence estimation, (4) calibration evaluation.
Fact Extraction Given query-answer pair
(xi , yi ), the first step is to extract the individual
facts from response. This extraction can be
efficiently carried out using a powerful external
language model, such as GPT-4 (Brown et al.,
i
2020), producing a set of facts {fij }M
j=1 for yi .

Motivation

Compared to the confidence calibration for shortform generation or traditional classification problems, a significant challenge in calibrating longform text generation is that a response may contain
multiple facts, making it unreasonable to assign a
single correctness measure and a single confidence
score to the entire response. The reason is that the
answer might be partially correct, and the model
might also be partially confident in only a subset
of the facts of a response. Meanwhile, some facts
in response are irrelevant to the query, so the calibration based solely on correctness is insufficient.
Based on the above motivation, our proposed calibration framework aims to calibrate the confidence
to relevance-weighted correctness on the fact level,
which leads to the following two advantages: (1)
Finer Granularity: we assign a confidence vector rather than a scalar to a response, where each
item represents confidence for a single fact. This
fine-grained framework allows for more nuanced
and precise calibration. (2) Relevance Awareness:
we assess both the correctness and the relevance of
each fact, which ensures that the confidence score
attributed to each fact can reflect its significance
and appropriateness within the given context.
3.2

Correctness and Relevance Evaluation Once
facts are extracted, we evaluates both the correctness and relevance of each fact in relation to the
query. Correctness is assessed by verifying the factual accuracy of each fact using GPT-4 in combination with retrieval methods, such as search engines
and ground truth answers from relevant datasets,
i
yielding correctness scores {corrji }M
j=1 . Similarly,
i
relevance scores {relji }M
j=1 can also be measured
using GPT-4 to capture each fact’s pertinence to the
query within the context of the overall response.

Confidence Estimation Confidence estimation
quantifies the certainty of the LLM for each fact
in its response. To derive a confidence vector
i
{conf ji }M
j=1 for each response, we employ three
widely used confidence estimation methods: (1)
Verbalization-based method (Tian et al., 2023):
model is prompted to verbally express confidence
score for each fact in the response. (2) Logit-based
method (Kadavath et al., 2022a): confidence is determined by the probability assigned to the “True”
token when evaluating the response as True or
False. (3) Consistency-based method (Manakul
et al., 2023): confidence is determined by the consistency across multiple sampled outputs. Formally,

Architecture

To calibrate confidence with relevance-weighted
correctness at fact level, our framework comprises
four components, as shown in fig. 2: (1) fact extrac3

Table 1: Comparison of confidence estimation and calibration performance across five base models for three
confidence estimation methods (Verbalization, isTrueLogit, Consistency) on the ASQA and LongFact datasets.
Dataset (→)

ASQA

Metric (→) / Model (↓)

Confidence

Method (↓) / Level (→)

Verbalization

isTrueLogit

Consistency

LongFact
Calibration

Confidence

Calibration

Fact

Response

Fact

Response

Fact

Response

Fact

Response

Llama-2-7b
Llama-2-13b
Vicuna-7b
Vicuna-13b
GPT-3.5-turbo

0.6946
0.7629
0.8054
0.8661
0.9620

0.7110
0.8289
0.8425
0.9339
0.9673

0.2605
0.2404
0.3365
0.2540
0.1789

0.2508
0.2606
0.3524
0.2688
0.1855

0.6753
0.7510
0.7567
0.8838
0.9659

0.7842
0.8418
0.8591
0.9299
0.9554

0.2109
0.1556
0.1505
0.1134
0.0856

0.1415
0.1310
0.1369
0.1094
0.0935

Comparison

0.8182

0.8567

0.0040

0.0043

0.8065

0.8741

0.0025

0.0006

Llama-2-7b
Llama-2-13b
Vicuna-7b
Vicuna-13b
GPT-3.5-turbo

0.6639
0.9741
0.5448
0.8116
-

0.8088
0.9483
0.5672
0.6342
-

0.2972
0.3723
0.2867
0.2486
-

0.3748
0.3764
0.2806
0.2837
-

0.5081
0.8693
0.5607
0.8648
-

0.8624
0.9696
0.6186
0.7947
-

0.3525
0.1635
0.2998
0.1240
-

0.1998
0.1932
0.2539
0.2213
-

Comparison

0.7486

0.7396

0.0018

0.0000

0.7007

0.8113

0.0167

0.0003

Llama-2-7b
Llama-2-13b
Vicuna-7b
Vicuna-13b w
GPT-3.5-turbo

0.8714
0.8903
0.8834
0.9250
0.8859

0.8334
0.8320
0.8227
0.9007
0.8393

0.3224
0.3101
0.3312
0.2473
0.1572

0.3331
0.3326
0.3373
0.2500
0.1807

0.9276
0.8940
0.9397
0.9727
0.9613

0.9760
0.8980
0.9767
0.9767
0.9480

0.2167
0.1385
0.1946
0.1020
0.0715

0.1660
0.1804
0.1477
0.1085
0.0957

Comparison

0.8912

0.8456

0.0080

0.0069

0.9391

0.9551

0.0047

0.0014

the confidence of fij can be represented as:


conf ji = C LLM(·), pc (fij , xi , yi ) ,

conf kavg = |B1k |
(1)

F-ECE =

4

Calibration Evaluation We define Fact-Level
Expected Calibration Error (F-ECE) as the evaluation metric used to quantify the discrepancy
between a model’s confidence and the relevanceweighted correctness across all responses and their
corresponding facts. For each fact within a response, we calculate the relevance-weighted correctness as the product of the fact’s correctness
score and its relevance score. The response-level
relevance-weighted correctness and confidence are
then computed by averaging these values across all
facts within a response, as detailed in eq. (2).

j=1
M

1 Xi
conf i =
conf ji ,
Mi

4.1

corrkavg − conf kavg

(3)

Key Observation

Experiment Setup

This section outlines the experimental setups, including the datasets, models, and evaluations.
Datasets We utilize two long-form response
datasets: (1) LongFact (Wei et al., 2024): a dataset
contains prompts that evaluate model’s factuality
in open-end responses. (2) ASQA (Stelmakh et al.,
2022): a dataset centers on ambiguous factoid questions with multiple reference answers.

(2)

j=1

F-ECE is then computed by assessing the difference between the average relevance-weighted correctness and the average confidence within each
bin k, where B is the number of bins for grouping
confidence scores, and Bk is the set
of responses in
1 P
k
the k-th bin. Let corravg = |Bk | i∈Bk corri and

N

This section discusses three important phenomena observed under our fact-level calibration.These
findings not only demonstrate the superiority of
our framework over traditional response-level
calibration, but also inspire the development
of a confidence-guided fact-level self-correction
method based on these insights.

M

1 Xi
corrji × relji ,
Mi

i∈Bk conf i ,

N
X
|Bk |

n=1

where LLM is the model to be evaluated, pc is the
prompt, C denotes the method used for estimation.

corri =

P

Models We use five popular models from
different families and scales, including: (1)
LLaMA (Touvron et al., 2023): include LLaMA7b-chat and LLaMA-13b-chat. (2) Vicuna (Chiang
et al., 2023): include Vicuna-7b and Vicuna-13b.
(3) GPT (Brown et al., 2020): GPT-3.5-turbo.
4

Correctness and Relevance Estimation We
use the Search-Augmented Factuality Evaluator
(SAFE), a pipeline proposed by (Wei et al., 2024)
that employs LLMs as agents to automatically evaluate the factuality of long-form responses. It utilizes a multi-step reasoning process that includes
sending search queries to Google Search (Hillis
et al., 2012) to verify the information provided.

for facts are described in section 3.2. The detailed
prompt template is available in Appendix C. To
generate the reliability histograms, we divide the
model’s predictions into ten bins based on confidence scores and calculate the average accuracy for
each bin. Ideally, an optimally calibrated model
would produce a diagonal pattern in the histogram.
As shown in fig. 3, a comparison of the histograms on the left and right demonstrates that our
fact-level framework can better distinguish calibration performance across models of varying scales.
Notably, models such as Llama-2-7b, which appear
well-calibrated under traditional response-level calibration, perform significantly worse under factlevel calibration. A similar trend is consistently
observed in table 1, where, as highlighted in the table, the variance in fact-level calibration across five
different models is nearly an order of magnitude
higher than that of response-level calibration. This
ability to reveal discrepancies arises from fact-level
calibration’s consideration of fine-grained correctness for each fact, as well as the relevance of each
fact to the query. The alignment with the model’s
capabilities highlights both the superiority and validity of our method, indicating that fact-level calibration imposes a stricter standard.

Confidence Estimation We utilize three popular confidence estimation methods from different
categories (Geng et al., 2024): Verbalization (Tian
et al., 2023), isTrueLogit (Kadavath et al., 2022a),
and Consistency (Manakul et al., 2023).
Calibration Evaluation Metrics We use Expected Calibration Error (ECE) (Guo et al., 2017a;
Naeini et al., 2015) at response-level, and F-ECE
at the fact-level, as introduced in section 3.2.
4.2

Results on Fact-Level Calibration

This section highlights three key phenomena observed during our fact-level calibration. These
findings not only underscore the advantages of
our framework compared to traditional responselevel’s, but also inform the design of a confidenceguided fact-level self-correction approach.

Observation 2: Understanding over-confidence
through fact-level analysis. We examine the distribution of sentence confidence for both fact-level
and response-level calibrations. For the responselevel, we directly plot its confidence scores distribution in a grey violin plot. For the fact-level, since
confidence for a single response is represented as a
vector rather than a scalar, we compute three statistical measures: the mean, maximum, and minimum
of the vector. These measures are then visualized
as three separate purple violin plots.
The results, shown in fig. 4, reveal two noteworthy phenomena: (1) The confidence distribution at the response level is narrow, concentrated
around higher confidence values, while the distribution of the mean confidence in the fact-level calibration is wider and indicates lower overall confidence. (2) The response-level confidence distribution closely mirrors the distribution of the maximum confidence values in the fact-level method.
Furthermore, a similar phenomenon is also corroborated in table 1, where the average confidence at the
fact level across five different models is generally
lower than that at the response level.
These observations suggest that response-level

Observation 1: Fact-level calibration imposes
a stricter standard. We compare fact-level and
response-level calibration following the protocol
outlined in (Guo et al., 2017a), where reliability
histograms and statistical metrics for is summarized. For both fact and response level, we estimate
confidence through all three confidence estimation
method, where the correctness/relevance evaluation
Fact-Level

Response-Level

Accuracy

#Samples

Confidence

Figure 3: Comparison of calibration measures between
fact-level and response-level across models of three different scales: LLaMA-7B/13B, and GPT-3.5, indicating
fact-level imposes a stricter standard (Observation 1).

5

Llama-2-13b

Vicuna-7b

Vicuna-13b

GPT-3.5-turbo

ASQA

LongFact

Llama-2-7b

Figure 4: Comparison of confidence distribution across different responses between fact-level and response-level,
with the purple plots representing fact-level distribution under different statistical metrics and the gray plots showing
the response-level distribution, highlighting the over-confidence issue at the response level, which stems from the
dominance of the implicit high-confidence facts hidden within the response (Observation 2).
Llama-2-13b

Vicuna-7b

Vicuna-13b

GPT-3.5-turbo

ASQA

LongFact

Llama-2-7b

Figure 5: Confidence distribution within individual responses at fact level, with red bar indicating the response-level
confidence score, indicating high variance exists in fact-level confidence within a single response (Observation 3).

confidence is largely influenced by the fact with
the highest implicit confidence, which can result in
overconfidence. In contrast, fact-level framework
breaks down the response into individual facts, assessing confidence for each one. This approach
highlights less confident aspects of the response,
helping to mitigate the issue of overconfidence.

in the box plots indicate these outliers, which generally correspond to facts with substantially lower
confidence, falling below the main distribution.
This suggests that certain facts are generated by
the model with considerably less confidence compared to others within the same response.

5
Observation 3: High variance exists in fact-level
confidence within a response. We examine the
variance in fact-level confidence within each individual responses. Specifically, for each response,
we extract its confidence vector and visualize its
distribution using box plots. Due to space constraints, we have visualized 10 responses for each
model across both datasets, as shown in fig. 5. Red
bar represents the response-level confidence score.
Two key observations can be made: (1) Factlevel confidence exhibits significant variance
within individual responses, whereas responselevel confidence tends to be concentrated at a
higher level. (2) Outlier facts typically have much
lower confidence scores. The numerous white dots

Application: Confidence-Guided
Fact-Level Self-Correction

In this section, we introduce the motivation and
architecture of Confidence-Guided Fact-Level SelfCorrection, dubbed ConFix. ConFix utilizes facts
with high confidence as references to revise facts
with low confidence, thereby enhancing the generation quality and mitigating hallucinations. Importantly, ConFix operates in real-time during the
generation process, eliminating the need for additional fine-tuning or retraining, which reduces
computational costs and enhances its adaptability.
Furthermore, it functions without relying on external knowledge sources, significantly broadening its
applicability across diverse scenarios.
6

Q

What is the Deep Blue?

A

Deep Blue is a go computer developed by IBM that famously defeated world champion Garry Kasparov in 1997.

High Confidence Facts

Low Confidence Fact

0.90 Deep Blue is developed by IBM.
0.85 Deep Blue defeated world champion Garry Kasparov.
0.80 The defeat is in 1997.
0.30 Deep Blue is a go computer.

(2) Factor Extraction & Fact Correction
High Conf Facts

(1) Fact Extraction & Confidence Estimation

Low Conf Fact

Deep Blue is a go computer.
Factor Extraction

Deep Blue, Go Computer

Factors

OldConf

Fact Correction

0.90 Deep Blue is a chess computer.

T
NewConf > OldConf

Fact after Correction

F

0.90

NewConf

Modification

Go Computer

Chess Computer

Corrected Fact

Deep Blue is a chess computer.

(3) Confidence Re-Estimation
Figure 6: An illustration of our confidence-guided fact-level self-correction framework (ConFix), consisting of
three steps: (1) fact extraction and confidence estimation; (2) fact correction using high-confidence facts; and (3)
confidence re-estimation. These three steps can be iterated until the desired level of enhancement is achieved.

5.1

i
scores {conf ji }M
j=1 , we then split the facts into
two groups: high-confidence and low-confidence,
based on a confidence threshold τ . The highconfidence group shown in eq. (4) is used as a form
of internal knowledge base, whose knowledge is
leveraged to reinforce and augment facts within the
low-confidence group, which is shown in eq. (5),

Motivation

The development of Confidence-Guided LLM SelfCorrection is driven by the three observations discussed earlier. The rationale behind these observations supporting self-correction is as follows: (1)
Observations 1 and 2 demonstrate that, even under strict conditions, the fact-level framework reduces overconfidence and enhances the model’s
calibration, aligning confidence more closely with
factual accuracy. This improved calibration is crucial for enabling effective confidence-guided selfcorrection. (2) Observation 3 reveals that highconfidence and low-confidence facts often coexist
within the same response. Even when the overall
confidence is relatively consistent, outliers tend
to be low-confidence facts. This enables highconfidence facts to serve as some kind of references, providing the necessary information to refine and correct the low-confidence facts.
5.2

fh = {fij | conf ji ≥ τ }

(4)

fl = {fij | conf ji < τ },

(5)

where the threshold is defined asPthe mean confij
i
dence score across facts τ = M1 i M
j=1 conf i .

S2: Factor Extraction & Fact Correction To
ensure that only the erroneous parts of the lowconfidence facts are modified without changing the
overall meaning, we restrict the modifiable parts.
Specifically, we first parse the key factors through
Kj

j
i
factor extraction. Let {fa j,k
i }k=1 represent the Ki
factors extracted from the target fact fij ∈ fl ,

Architecture

Kj

j
i
{fa j,k
i }k=1 = F(LLM(·), pf (fi )),

The overall architecture of ConFix is illustrated
in fig. 6, including three steps: (1) fact extraction &
confidence estimation, (2 )factor extraction & fact
correction, and (3) fact confidence re-estimation.

(6)

where pf is the prompt, which includes: (1) A
clear task description. (2) Several instances. (3)
The task containing the input sentence. The model
is expected to output its extracted factors.
After extracting factors, we then perform fact
correction, targeting only the extracted factors for
modification. This process can be represented as,

S1: Fact Extraction & Confidence Estimation
Given a response yi , ConFix first conducts fact
extraction and confidence estimation for each extracted fact, following the same process as described in section 3.2. After obtaining the facts
i
{fij }M
j=1 for yi and their corresponding confidence

j

Ki
fˆij = R(LLM(·), pr (fij , {fa j,k
i }k=1 , fh )

7

(7)

where pr is the prompt, which includes: (1) A clear
task description. (2) Several instances. (3) The task
containing the input target fact, the extracted factors and the high-confidence reference facts. The
model is expected to output the modified target fact,
noting that the model allows for returning “NoError” to make no modifications to the input.

est proportion of improve for almost all models,
with the exception of LLaMA-2-7B.
The performance drop observed in LLaMA-2-7B
is interesting, as it aligns with findings from previous experiments: ConFix depends on the model’s
calibration capabilities, functioning effectively
when confidence is well-aligned with correctness.
However, LLaMA-2-7B is inadequately calibrated,
as indicated by its higher ECE/F-ECE scores in table 1. Therefore, the self-correction performance
drop in LLaMA-2-7B does not undermine our
ConFix, but rather highlights the importance of
adequate calibration. Under the right conditions,
our method can significantly improve model performance without the need for external knowledge,
and these conditions are easily met, as calibration can be enhanced using various existing techniques (Liu et al., 2023; Geng et al., 2024).

S3: Fact Confidence Re-Estimation Finally, the
modified facts undergo the confidence estimation
process again to obtain new confidence scores:


ˆ j = C LLM(·), pc (fˆj , xi , yi ) , (8)
conf
i
i
j

ˆ represents the confidence score of the
where conf
i
ˆ j > conf j , the
modified fact fˆij . Finally, if conf
i
i
modification is deemed successful and is accepted.
Otherwise, ConFix will repeat the process of factor extraction, fact correction, and confidence reestimation. This iterative process continues until
either a satisfactory confidence score is achieved or
a predetermined maximum number of iterations N
is reached, where the model return “NoError” and
make no modifications to the input.
5.3

Table 2: Acc., Precision and Recall of Error-Detection.
Base Model

Accuracy (%) Precision (%) Recall (%)

GPT-3.5-turbo
Vicuna-7b
Vicuna-13b
Llama-2-7b
Llama-2-13b

Experiment on Self-Correction

Experiment Setup We adopt a two-fold evaluation. First, we assess error detection performance
using standard metrics such as Accuracy, Precision, and Recall (Powers, 2020). Subsequently,
for evaluating self-correction, we leverage GPT-4
in a zero-shot pairwise evaluation framework (see
prompts in Appendix C), measuring improvement
ratio, consistency ratio, and regression ratio to capture the performance of correction.

83.29
60.06
74.81
64.26
70.45

87.89
99.90
77.68
67.86
77.45

13.71
0.15
8.46
13.35
30.62

Table 3: GPT-4 Evaluation of Self-Correction.
Base Model
GPT-3.5-turbo
Vicuna-7b
Vicuna-13b
Llama-2-7b
Llama-2-13b

6

Improved (%) Same (%) Regressed (%) #Revised
46.30
50.00
49.40
6.76
53.35

24.07
50.00
28.92
12.56
19.59

29.63
0.00
21.69
80.68
27.07

108
2
83
207
418

Conclusion

This paper presents a novel fact-level calibration
and self-correction framework designed to address
hallucination issues in long-form responses generated by large language models. Traditional
response-level methods fall short when handling
complex outputs containing multiple facts. Our
approach evaluates each fact’s correctness and
relevance individually, both externally and internally, enabling fine-grained confidence assessments. This framework imposes a stricter standard
than response-level methods, reduces overconfidence, and highlights significant confidence variance across facts within a response. By leveraging
high-confidence facts for in-context learning, our
self-correction method ConFix can effectively mitigate hallucinations without the need for external
knowledge, as demonstrated across various models.

Error Detection Table 2 shows the error detection results of our proposed method across five different base models. As seen from the table, larger
models, such as GPT and the 13B model, outperform smaller models like the 7B model in terms
of Accuracy and Precision. However, all models
show lower performance in Recall, suggesting that
a significant number of erroneous facts go undetected. This indicates a persistent overconfidence
issue, with models often incorrectly considering
false information as correct.
Error Correction Table 3 presents the error correction results of our method across five different
base models. The results show that, among the
three possible outcomes: Improved, Same, and Regressed, our method consistently achieves the high8

7

Limitations and Broader Impacts

Yann Dubois, Balázs Galambosi, Percy Liang, and Tatsunori B Hashimoto. 2024. Length-controlled alpacaeval: A simple way to debias automatic evaluators. arXiv preprint arXiv:2404.04475.

In this work, we propose a fact-level calibration
framework and, based on this framework, introduce a confidence-guided fact-level self-correction
method. However, for this self-correction method
to be effective, the model itself must possess a certain level of calibration ability. In our paper, we
discuss how our calibration framework can alleviate over-confidence. In future work, we will further
explore ways to enhance calibration ability within
the calibration framework, paving the way for more
effective confidence-guided self-correction.

Yann Dubois, Xuechen Li, Rohan Taori, Tianyi Zhang,
Ishaan Gulrajani, Jimmy Ba, Carlos Guestrin, Percy
Liang, and Tatsunori B. Hashimoto. 2023. Alpacafarm: A simulation framework for methods that learn
from human feedback. Preprint, arXiv:2305.14387.

References

Jiahui Geng, Fengyu Cai, Yuxia Wang, Heinz Koeppl,
Preslav Nakov, and Iryna Gurevych. 2024. A survey of confidence estimation and calibration in
large language models. In Proceedings of the 2024
Conference of the North American Chapter of the
Association for Computational Linguistics: Human
Language Technologies (Volume 1: Long Papers),
pages 6577–6595.

Yejin Bang, Samuel Cahyawijaya, Nayeon Lee, Wenliang Dai, Dan Su, Bryan Wilie, Holy Lovenia, Ziwei
Ji, Tiezheng Yu, Willy Chung, et al. 2023. A multitask, multilingual, multimodal evaluation of chatgpt
on reasoning, hallucination, and interactivity. arXiv
preprint arXiv:2302.04023.

Olga Golovneva, Moya Peng Chen, Spencer Poff, Martin Corredor, Luke Zettlemoyer, Maryam FazelZarandi, and Asli Celikyilmaz. 2022. Roscoe: A
suite of metrics for scoring step-by-step reasoning. In
The Eleventh International Conference on Learning
Representations.
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q Weinberger. 2017a. On calibration of modern neural
networks. In International conference on machine
learning, pages 1321–1330. PMLR.

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
2020. Language models are few-shot learners. In
Advances in Neural Information Processing Systems
33: Annual Conference on Neural Information
Processing Systems 2020, NeurIPS 2020, December
6-12, 2020, virtual.

Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017b. On calibration of modern neural
networks. In Proceedings of the 34th International
Conference on Machine Learning, ICML 2017,
Sydney, NSW, Australia, 6-11 August 2017, volume 70 of Proceedings of Machine Learning
Research, pages 1321–1330. PMLR.
Ken Hillis, Michael Petit, and Kylie Jarrett. 2012.
Google and the Culture of Search. Routledge.
Mengting Hu, Zhen Zhang, Shiwan Zhao, Minlie
Huang, and Bingzhe Wu. 2023. Uncertainty in natural language processing: Sources, quantification, and
applications. arXiv preprint arXiv:2306.04459.

Silei Cheng, Zhe Gan, Zhengyuan Yang, Shuohang
Wang, Jianfeng Wang, Jordan Boyd-Graber, and
Lijuan Wang. 2023. Prompting gpt-3 to be reliable. In International Conference on Learning
Representations (ICLR 23).

Yukun Huang, Yixin Liu, Raghuveer Thirukovalluru,
Arman Cohan, and Bhuwan Dhingra. 2024. Calibrating long-form generations from large language
models. arXiv preprint arXiv:2402.06544.

Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng,
Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan
Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion
Stoica, and Eric P. Xing. 2023. Vicuna: An opensource chatbot impressing gpt-4 with 90%* chatgpt
quality.

Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
Henighan, Dawn Drain, Ethan Perez, Nicholas
Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli
Tran-Johnson, Scott Johnston, Sheer El Showk, Andy
Jones, Nelson Elhage, Tristan Hume, Anna Chen,
Yuntao Bai, Sam Bowman, Stanislav Fort, Deep
Ganguli, Danny Hernandez, Josh Jacobson, Jackson Kernion, Shauna Kravec, Liane Lovitt, Kamal Ndousse, Catherine Olsson, Sam Ringer, Dario
Amodei, Tom Brown, Jack Clark, Nicholas Joseph,
Ben Mann, Sam McCandlish, Chris Olah, and Jared
Kaplan. 2022a. Language models (mostly) know
what they know. CoRR, abs/2207.05221.

Soham Dan and Dan Roth. 2021. On the effects of
transformer size on in-and out-of-domain calibration.
In Findings of the Association for Computational
Linguistics: EMNLP 2021, pages 2096–2101.
Shrey Desai and Greg Durrett. 2020.
Calibration of pre-trained transformers. arXiv preprint
arXiv:2003.07892.

9

Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
Henighan, Dawn Drain, Ethan Perez, Nicholas
Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli
Tran-Johnson, et al. 2022b. Language models
(mostly) know what they know. arXiv preprint
arXiv:2207.05221.

AAAI Conference on Artificial Intelligence. AAAI
Conference on Artificial Intelligence, 2015:2901–
2907.
Khanh Nguyen and Brendan O’Connor. 2015. Posterior calibration and exploratory analysis for natural language processing models. In Proceedings
of the 2015 Conference on Empirical Methods
in Natural Language Processing, EMNLP 2015,
Lisbon, Portugal, September 17-21, 2015, pages
1587–1598. The Association for Computational Linguistics.

Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.
Semantic uncertainty: Linguistic invariances for
uncertainty estimation in natural language generation. In The Eleventh International Conference
on Learning Representations, ICLR 2023, Kigali,
Rwanda, May 1-5, 2023. OpenReview.net.

OpenAI. 2023. GPT-4 technical report.
abs/2303.08774.

Junyi Li, Xiaoxue Cheng, Wayne Xin Zhao, JianYun Nie, and Ji-Rong Wen. 2023a. Halueval:
A large-scale hallucination evaluation benchmark
for large language models. In Proceedings of the
2023 Conference on Empirical Methods in Natural
Language Processing, pages 6449–6464.

CoRR,

David MW Powers. 2020. Evaluation: from precision, recall and f-measure to roc, informedness, markedness and correlation. arXiv preprint
arXiv:2010.16061.

Moxin Li, Wenjie Wang, Fuli Feng, Fengbin Zhu, Qifan
Wang, and Tat-Seng Chua. 2024. Think twice before
assure: Confidence estimation for large language
models through reflection on multiple answers. arXiv
preprint arXiv:2403.09972.

Ivan Stelmakh, Yi Luan, Bhuwan Dhingra, and
Ming-Wei Chang. 2022. Asqa: Factoid questions meet long-form answers. arXiv preprint
arXiv:2204.06092.

Xuechen Li, Tianyi Zhang, Yann Dubois, Rohan Taori,
Ishaan Gulrajani, Carlos Guestrin, Percy Liang, and
Tatsunori B. Hashimoto. 2023b. Alpacaeval: An
automatic evaluator of instruction-following models.
https://github.com/tatsu-lab/alpaca_eval.

Katherine Tian, Eric Mitchell, Allan Zhou, Archit
Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn,
and Christopher D Manning. 2023. Just ask for calibration: Strategies for eliciting calibrated confidence
scores from language models fine-tuned with human
feedback. arXiv preprint arXiv:2305.14975.

Stephanie Lin, Jacob Hilton, and Owain Evans. 2021.
Truthfulqa: Measuring how models mimic human
falsehoods. arXiv preprint arXiv:2109.07958.

Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike
Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer,
Luke Zettlemoyer, and Hannaneh Hajishirzi. 2023.
Factscore: Fine-grained atomic evaluation of factual precision in long form text generation. CoRR,
abs/2305.14251.

Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay
Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
Bhosale, Dan Bikel, Lukas Blecher, Cristian CantonFerrer, Moya Chen, Guillem Cucurull, David Esiobu,
Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller,
Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan
Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa,
Isabel Kloumann, Artem Korenev, Punit Singh Koura,
Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten,
Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu,
Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan,
Melanie Kambadur, Sharan Narang, Aurélien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas
Scialom. 2023. Llama 2: Open foundation and finetuned chat models. CoRR, abs/2307.09288.

Niels Mündler, Jingxuan He, Slobodan Jenko, and Martin Vechev. 2023. Self-contradictory hallucinations
of large language models: Evaluation, detection and
mitigation. arXiv preprint arXiv:2305.15852.

Ante Wang, Linfeng Song, Baolin Peng, Ye Tian, Lifeng
Jin, Haitao Mi, Jinsong Su, and Dong Yu. 2024. Finegrained self-endorsement improves factuality and reasoning. arXiv preprint arXiv:2402.15631.

Mahdi Pakdaman Naeini, Gregory F. Cooper, and Milos
Hauskrecht. 2015. Obtaining well calibrated probabilities using bayesian binning. Proceedings of the ...

Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V.
Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2023. Self-consistency

Xin Liu, Muhammad Khalifa, and Lu Wang. 2023.
Lightweight language model calibration for openended question answering with varied answer
lengths. In The Twelfth International Conference
on Learning Representations.
Potsawee Manakul, Adian Liusie, and Mark Gales.
2023. SelfCheckGPT: Zero-resource black-box hallucination detection for generative large language
models. In Proceedings of the 2023 Conference on
Empirical Methods in Natural Language Processing,
pages 9004–9017, Singapore. Association for Computational Linguistics.

10

improves chain of thought reasoning in language
models. In The Eleventh International Conference
on Learning Representations, ICLR 2023, Kigali,
Rwanda, May 1-5, 2023. OpenReview.net.
Jerry Wei, Chengrun Yang, Xinying Song, Yifeng Lu,
Nathan Hu, Dustin Tran, Daiyi Peng, Ruibo Liu,
Da Huang, Cosmo Du, et al. 2024. Long-form factuality in large language models. arXiv preprint
arXiv:2403.18802.
Teng Xiao, Mingxiao Li, Yige Yuan, Huaisheng Zhu,
Chao Cui, and Vasant G Honavar. 2024a. How to
leverage demonstration data in alignment for large
language model? a self-imitation learning perspective. arXiv preprint arXiv:2410.10093.
Teng Xiao, Yige Yuan, Huaisheng Zhu, Mingxiao Li,
and Vasant G Honavar. 2024b. Cal-dpo: Calibrated
direct preference optimization for language model
alignment. In The Thirty-eighth Annual Conference
on Neural Information Processing Systems.
Caiqi Zhang, Fangyu Liu, Marco Basaldella, and Nigel
Collier. 2024. Luq: Long-text uncertainty quantification for llms. arXiv preprint arXiv:2403.20279.
Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu,
Tingchen Fu, Xinting Huang, Enbo Zhao, Yu Zhang,
Yulong Chen, et al. 2023. Siren’s song in the ai ocean:
A survey on hallucination in large language models.
arXiv preprint arXiv:2309.01219.

11

A

Datasets

GPT-3.5-turbo (Brown et al., 2020) This model
is part of OpenAI’s well-known GPT series. GPT3.5-turbo is an enhanced version of GPT-3, offering improved performance and efficiency. It is
designed to handle a wide range of language tasks,
from text generation to comprehension and translation. The "turbo" variant is optimized for faster
inference and lower latency, making it ideal for
real-time applications where quick response times
are crucial. GPT-3.5-turbo is widely used in both
research and industry due to its versatility and highquality output.

LongFact (Wei et al., 2024): A dataset consisting of prompts designed to assess a model’s factuality in long-form responses created by GPT-4.
This dataset includes a diverse range of topics and
ensures that the prompts require detailed and nuanced answers, making it a robust benchmark for
evaluating the factual accuracy of language models
in generating extended text. The dataset is particularly valuable for testing the capabilities of models in maintaining factual consistency over longer
passages, which is crucial for applications such
as content creation, summarization, and complex
question answering.
ASQA
(Stelmakh et al., 2022): A dataset
designed for long-form question answering that
uniquely centers on ambiguous factoid questions.
ASQA provides a challenging testbed for models
as it includes questions that can have multiple valid
answers depending on the interpretation of the ambiguity. This dataset emphasizes the need for models to not only retrieve accurate information but
also to handle the inherent uncertainty and provide
comprehensive responses. ASQA is instrumental
in pushing the boundaries of model performance in
scenarios where clarity and precision are essential,
such as in education and interactive AI systems.

B

C

Prompts

C.1

Prompt for Fact-Level Confidence
Estimation

The specific prompts used for fact-level confidence
estimation are detailed below.
Instructions:
1. The following STATEMENT has been extracted
from the broader context of the given RESPONSE
to the given QUESTION.
2.
Indicate how confident you are in the
accuracy of the STATEMENT when answering the
QUESTION, based on your knowledge.
3.
The confidence evaluation should be a
value between 0 and 1 (with two decimal places
retained), based on the following scoring
criterion:
{Criterion} 4. Your task is to do this for the
STATEMENT, RESPONSE and QUESTION under "Your
Task".
Some examples have been provided for you to
learn how to do this task.

Models

LLaMA-7b-chat & LLaMA-13b-chat (Touvron et al., 2023): These models are part of the
LLaMA family, known for their strong performance in various natural language processing tasks.
The “chat” versions are particularly fine-tuned for
conversational contexts, making them suitable for
generating coherent and contextually appropriate
responses in dialogue settings. LLaMA models
are designed to balance performance and computational efficiency, making it a popular choice for
research and application in interactive AI systems.

{Some Examples}
Your Task:
QUESTION:
{Question}
RESPONSE:
{Response}
STATEMENT:
{Statement}

Table 4: Prompt for fact-level confidence estimation
{Criterion}, {Question}, {Response} and {Statement}
are placeholders.

Vicuna-7b and Vicuna-13b
(Chiang et al.,
2023) Vicuna is an open-source chatbot trained by
fine-tuning LLaMA on user-shared conversations
collected from ShareGPT. Preliminary evaluation
using GPT-4 as a judge shows Vicuna-13B achieves
more than 90% quality of ChatGPT and Bard while
outperforming other models like LLaMA and Stanford Alpaca (Li et al., 2023b; Dubois et al., 2024,
2023) in more than 90% of cases.

C.2

Prompt for Response-Level Confidence
Estimation

The specific prompts used for response-level confidence estimation are detailed below.
12

Instructions:
1. The following RESPONSE is the answer to the
given QUESTION.
2.
Indicate how confident you are in the
accuracy of the RESPONSE when answering the
QUESTION, based on your knowledge.
3.
The confidence evaluation should be a
value between 0 and 1 (with two decimal places
retained), based on the following scoring
criterion:
{Criterion}
4. Your task is to do this for the RESPONSE and
QUESTION under “Your Task”.
Some examples have been provided for you to
learn how to do this task.

Instructions:
You have been provided with a sentence and some
reference knowledge.
The sentence has been analyzed, and its factors
have been identified.
However, it is acknowledged that there may
be errors or inaccuracies in the identified
factors.
Your task is to first review the identified
factors and check for any errors or
inaccuracies.
If there are no errors, simply return “NoError”
to indicate that no corrections are needed.
If errors are present, proceed to make the
necessary corrections.
Ensure that the corrections are limited to the
existing factors without adding new content.
Use the format <old factor -> new factor> for
each correction.

{Some Examples}
Your Task:
QUESTION:
{Question}

{Some Examples}

RESPONSE:
{Response}

Your Task:
SENTENCE:
{Sentence}

Table 5: Prompt for response-level confidence estimation {Criterion}, {Question}, {Response} and {Statement} are placeholders.

FACTORS:
{Factor}
REFERENCE:
{Reference}

C.3

Prompt for Factor Extraction

Table 7: Prompt for fact correction {Sentence}, {Factor}
and {Reference} are placeholders.

The specific prompts used for factor extraction are
detailed below.

C.5
Instructions:
You are to read a sentence and identify the key
factors within it.
The task involves pinpointing the essential
elements
or
aspects
that
significantly
influence or characterize the situation, event,
or subject described.
Return the identified key factors using the
format <[factor1, factor2, ...]>
Some examples have been provided for you to
learn how to do this task.

For the self-correction, we utilize GPT-4 for zeroshot pair-wise evaluation. We use gpt-4-0314 for
all our experiments. The specific prompts used for
GPT-4 evaluation are detailed below.

D

Related Work

The concept of confidence calibration was first introduced to nerual networks by (Guo et al., 2017a)
to prevent logits from making incorrect classifications with high probability. This concept has
since been extended to NLP models (Desai and
Durrett, 2020; Dan and Roth, 2021; Hu et al., 2023).
Common methods for estimating confidence scores
include logit-based methods, consistency-based
methods, and verbalization-based methods. Logitbased methods (Guo et al., 2017b; Cheng et al.,
2023; Kadavath et al., 2022b) assess model confidence by examining the logits predicted by the
model. Consistency-based methods (Wang et al.,
2023; Kuhn et al., 2023) rely on the principle that
language models tend to produce similar outputs
consistently when they are confident. Recently, re-

{Some Examples}
Your Task:
SENTENCE:
{Sentence}

Table 6: Prompt for factor extraction {Sentence} is
placeholders.

C.4

GPT-4 Judgments for Self-Correction

Prompt for Fact Correction

The specific prompts used for fact correction are
detailed below.
13

You will be provided with a QUESTION, its
RESPONSE, and all facts extracted from the
RESPONSE under the heading "ALL FACTS". You
will also be provided with a specific fact under
the heading "TARGET FACT 1", which is included
in ALL FACTS. Additionally, you will be given a
modified version of this target fact under the
heading "TARGET FACT 2".
Based on your knowledge, evaluate whether
the modification of the target fact is an
improvement, the same, or a regression.
An improvement implies:
1. More accurate information.
2. Greater relevance to the question.
3. Minimal overlap with other facts in ALL
FACTS.
A regression implies: 1.
Introduction of
erroneous or inaccurate information.
2. Lower relevance to the question.
3. Repetition or introduction of information
that is already provided with other facts in
ALL FACTS.

QUESTION:
{Question}
RESPONSE:
{Response}
ALL FACTS:
{All Facts}
TARGET FACT 1:
{Original Fact}
TARGET FACT 2:
{New Fact}
First, provide a one-sentence comparison of the
two facts and explain whether you think the
modification is an improvement, the same, or a
regression. Second, on a new line, the state
only "IMPROVED", "SAME", or "REGRESSED" to
indicate the effectiveness of the modification.
Your response should use the following format:
COMPARISON:
<one-sentence
comparison
and
explanation>
REVISION: <"IMPROVED", "SAME", or "REGRESSED">

Table 8: Prompt for GPT-4 evaluation for the selfcorrection {Question}, {Response}, {All Facts}, {All
Facts}, {Original Facts} and {New Fact} are placeholders.

search has indicated that verbalization-based methods (Tian et al., 2023) might offer superior confidence estimation.

14

