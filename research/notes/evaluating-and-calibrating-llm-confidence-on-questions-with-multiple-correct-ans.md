---
title: Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct
  Answers
id: evaluating-and-calibrating-llm-confidence-on-questions-with-multiple-correct-ans
tags:
- aaai-bar-eval-dprc-d78e07
- evaluation-scale-precedent
- multi-model-multi-baseline
created: '2026-07-19T20:07:34.927869Z'
updated: '2026-07-19T20:11:37.555077Z'
source: https://arxiv.org/html/2602.07842v1
source_domain: arxiv.org
fetched_at: '2026-07-19T20:07:34.927467Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Wang, Ni, Ding, Zhan, Li, Bi (ICT/CAS, UCAS, Tsinghua, Renmin; arXiv:2602.07842).
  Diagnoses a failure mode of training-free consistency-based LLM confidence calibration:
  on questions with MULTIPLE valid correct answers, disagreement among equally-correct
  sampled responses is mistaken for uncertainty, systematically under-estimating confidence
  -- accuracy rises with answer cardinality but estimated confidence falls, producing
  severe miscalibration on mixed-answer-count questions. Introduces MACE, a purpose-built
  benchmark of 12,000 factual questions across 6 domains with controlled/varying answer
  cardinality. EVALUATION SCALE (direct bar precedent for this query): 15 representative
  calibration methods x 4 LLM families spanning 7B-72B parameters, tested for both
  single-answer and multi-answer regimes. Proposes Semantic Confidence Aggregation
  (SCA): aggregates confidence across multiple high-probability sampled responses
  (semantic-cluster level rather than exact-match), reaching state-of-the-art calibration
  under mixed-answer settings while preserving single-answer calibration quality.
  Relevant to AAAI-bar question as a concrete example of the BASELINE BREADTH (15
  methods) and MODEL BREADTH (4 families x scale range) treated as necessary for a
  calibration-methods paper to be taken seriously -- single-model, single-baseline
  comparisons are conspicuously absent from this paper''s design. Not code-specific;
  general factual QA domain.'
---

Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct Answers
Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct Answers
Yuhan Wang
1
2
2
footnotemark:
2
Shiyu Ni
1,2
Zhikai Ding
1
1
1
footnotemark:
1
Zihang Zhan
3
1
1
footnotemark:
1
Yuanzi Li
4
Keping Bi
1,2
1
State Key Laboratory of AI Safety, Institute of Computing Technology, CAS
2
University of Chinese Academy of Sciences
3
Tsinghua University
4
Renmin University of China
fzzh040114@gmail.com
{nishiyu23z,bikeping}@ict.ac.cn
Code
Datasets
Work done during an internship at ICT,CAS  Equal contribution  Corresponding author
Abstract
Confidence calibration is essential for making large language models (LLMs) reliable, yet existing training-free methods have been primarily studied under single-answer question answering.
In this paper, we show that these methods break down in the presence of multiple valid answers, where disagreement among equally correct responses leads to systematic underestimation of confidence. To enable a systematic study of this phenomenon, we introduce MACE, a benchmark of 12,000 factual questions spanning six domains with varying numbers of correct answers. Experiments across 15 representative calibration methods and four LLM families (7B–72B) reveal that while accuracy increases with answer cardinality, estimated confidence consistently decreases, causing severe miscalibration for questions with mixed answer counts. To address this issue, we propose Semantic Confidence Aggregation (SCA), which aggregates confidence over multiple high-probability sampled responses. SCA achieves state-of-the-art calibration performance under mixed-answer settings while preserving strong calibration on single-answer questions.
Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct Answers
Yuhan Wang
1
†
†
thanks:
Work done during an internship at ICT,CAS
2
2
footnotemark:
2
Shiyu Ni
1,2
†
†
thanks:
Equal contribution
Zhikai Ding
1
1
1
footnotemark:
1
Zihang Zhan
3
1
1
footnotemark:
1
Yuanzi Li
4
Keping Bi
1,2
†
†
thanks:
Corresponding author
1
State Key Laboratory of AI Safety, Institute of Computing Technology, CAS
2
University of Chinese Academy of Sciences
3
Tsinghua University
4
Renmin University of China
fzzh040114@gmail.com
{nishiyu23z,bikeping}@ict.ac.cn
Code
Datasets
Figure 1:
Failure of consistency-based calibration on multi-answer questions. Disagreement among sampled correct answers yields low estimated confidence, indistinguishable from uncertainty caused by alternation between correct and incorrect answers in single-answer settings.
1
Introduction
Confidence calibration aims to align a model’s expressed confidence with its true predictive performance
(Guo
et al.
,
2017
; Desai and Durrett,
2020
)
, and has long been a central research topic for improving the reliability of machine learning systems. In recent years, confidence calibration for large language models (LLMs) has attracted increasing attention, as honesty has been recognized as a fundamental aspect of aligning LLMs with human values
(Askell and others,
2021
)
. When properly calibrated, LLMs’ confidence can serve as a meaningful indicator of their uncertainty, reflecting the likelihood of hallucination
(Maynez
et al.
,
2020
; Min
et al.
,
2023
)
and guiding when retrieval augmentation is required
(Ni
et al.
,
2024
)
.
Confidence calibration methods can be divided into training-based and training-free approaches. Training-based methods learn to align confidence with ground-truth accuracy and can achieve strong in-domain calibration
(Lin
et al.
,
2022a
; Ni
et al.
,
2025b
)
. However, they require substantial annotation and often generalize poorly to other questions or domains
(Ni
et al.
,
2025a
)
. In this paper, we focus on training-free methods, which can be roughly categorized into three approaches:
1) leveraging token-level generation probabilities
(Guo
et al.
,
2017
; Desai and Durrett,
2020
; Jiang
et al.
,
2021
; Si
et al.
,
2022
)
, 2) prompting models to explicitly verbalize confidence
Lin
et al.
(
2022a
); Yin
et al.
(
2023
); Xiong
et al.
(
2024
); Ni
et al.
(
2024
)
, and 3) measuring semantic consistency across multiple sampled responses
(Manakul
et al.
,
2023
; Kuhn
et al.
,
2023
; Zhang
et al.
,
2023
)
.
Among these, response-consistency–based methods achieve the state-of-the-art (SOTA) performance.
Response–consistency–based approaches rely on the implicit assumption that higher agreement among generated responses indicates greater correctness. While this assumption often holds for single-answer questions, it breaks down for questions with multiple valid answers. In such cases, disagreement among equally correct responses can lead to low confidence estimates, even when the model possesses the relevant knowledge.
For example, as shown in Figure
1
, when asked “name one person who received the Nobel Prize in Physics in 1995”, the model may correctly generate either “Martin Lewis Perl” or “Frederick Reines” across samples. However, answer-level inconsistency results in low estimated confidence, similar to situations in which the model fluctuates among potentially wrong answers.
Because existing datasets predominantly contain single-answer questions, prior calibration studies have largely overlooked multi-answer settings, leaving it unclear how training-free confidence calibration methods—especially consistency-based approaches—behave in this scenario. Although multi-answer questions can be easier, as any correct answer suffices and accuracy may increase, consistency-based methods may assign low confidence due to disagreement among equally valid answers, potentially reducing overconfidence
(Yin
et al.
,
2023
; Xiong
et al.
,
2024
)
but in a miscalibrated manner. To systematically study confidence estimation under multi-answer question answering (QA), we introduce MACE (
M
ulti-
A
nswer
C
onfidence
E
stimation), a benchmark of 12,000 question–answer pairs spanning six factual domains, where each question has 1, 2, 4, or 6 correct answers.
Grounded on MACE, we evaluate 15 representative confidence calibration methods, including token-probability–based, verbalized, and consistency-based approaches, across four LLM families (LLaMA, Qwen, DeepSeek, and GPT), ranging from 7B to 72B parameters. Our experiments reveal that: (1) as the number of correct answers increases, LLMs achieve higher QA accuracy but exhibit lower confidence; (2) in realistic settings with mixed ground-truth answer cardinalities, methods that achieve SOTA calibration on single-answer questions collapse due to severe miscalibration on multi-answer questions; and (3) this confidence degradation is more pronounced for larger models (e.g., 70B), as they tend to alternate among a wider set of correct answers than smaller models.
To address this, we propose SCA (
S
emantic
C
onfidence
A
ggregation), which calibrates confidence by aggregating the probabilities of multiple high-confidence answers rather than relying on the most confident one. Specifically, we use the token-level sequence generation probability of each sampled response as its confidence signal. Since low-confidence responses contribute minimally, a simple summation over sampled responses yields improved calibration under mixed-answer settings, while preserving calibration performance on single-answer questions, outperforming SOTA baselines.
In summary, this work advances confidence calibration from single-answer QA to a more general setting with mixed numbers of ground-truth answers. We introduce the MACE benchmark, conduct a comprehensive evaluation across four LLM families, and propose SCA, which achieves state-of-the-art calibration performance in this general QA scenario.
2
Related Work
Calibration in Large Language Models.
Existing calibration methods for large language models (LLMs) can be training-based and training-free. Training-based methods require finetuning to enhance knowledge boundary perception
(Lin
et al.
,
2022a
; Zhang
et al.
,
2024
; Yang
et al.
,
2024
)
.
Training-free methods can be broadly categorized into three approaches:
Probability-based
methods leverage the model’s internal representations, such as token probabilities, logits, or hidden activations
(Jiang
et al.
,
2021
; Kadavath
et al.
,
2022
; Ren
et al.
,
2023
; Wightman
et al.
,
2023
; Ling
et al.
,
2024
; Ni
et al.
,
2025b
)
.
Verbalized-based
methods prompt LLMs to directly express confidence in natural language
(Lin
et al.
,
2022a
; Tian
et al.
,
2023
; Tanneru
et al.
,
2024
)
,
Consistency-based
methods estimate reliability by measuring agreement across multiple generations or reasoning chains
(Manakul
et al.
,
2023
; Cole
et al.
,
2023
; Lyu
et al.
,
2024
; Ni
et al.
,
2025a
)
.
While existing calibration studies primarily focus on single-answer scenarios, our work broadens this scope to encompass realistic and complex multi-answer settings.
Datasets for Confidence Estimation.
Existing datasets are not fully suitable for studying confidence estimation under varying ground-truth answer counts. Most datasets contain questions with a single answer.
Question-Answering benchmarks
include
ParaRel
(Elazar
et al.
,
2021
)
, HotpotQA
(Yang
et al.
,
2018
)
, SelfAware
(Yin
et al.
,
2023
)
, HaluEval
(Li
et al.
,
2023
)
, FalseQA
(Hu and others,
2023
)
, and NEC
(Liu and others,
2023
)
.
Multiple-Choice benchmarks
include MMLU
(Hendrycks
et al.
,
2021
)
, FEVER
(Thorne
et al.
,
2018
)
and WiCE
(Kamoi and others,
2023
)
.
However, existing benchmarks remain limited by the insufficient volume of questions for specific fixed answer counts and the lack of completed ground-truth annotations, restricting their utility for investigation into confidence estimation within multi-answer settings.
Figure 2:
The MACE benchmark construction pipeline
, illustrated using the
Honorable Award
domain.
①②
Valid triplet
(e.g., Pritzker Prize winners) are retained.
③
Low-popularity triplet
(e.g., obscure awards like the Ig Nobel Prize) are removed via
Popularity Filter
.
④
Noisy triplet
containing invalid formats (e.g., URLs) are removed via a
Validity Filter
.
⑤
Factually incorrect triplet
are identified and removed during the
Manual Verification
.
Finally, QA pairs are generated using triplet under four ground-truth counts settings (1a, 2a, 4a, 6a).
3
The MACE Benchmark
In this section, we provide the overview and construction process of the MACE benchmark.
3.1
Overview
To study how existing confidence calibration methods perform on multi-answer questions, we introduce MACE (
M
ulti-
A
nswer
C
onfidence
E
stimation), a benchmark comprising questions with one or multiple correct answers.
MACE spans six factual domains: Honorable Award (Award), Political Office (Office), Regional Affiliation (Region), Mathematical Concept (Math), Natural River (River), and Linguistic Culture (Language).
For each domain, MACE includes four question types with 1, 2, 4, or 6 correct answers, respectively (abbreviated as 1a, 2a, 4a, and 6a, in the paper), with 500 questions per type.
The construction of MACE has three key phases, shown in Figure
2
:
knowledge collection
that collects knowledge triplets
{
subject
,
relation
,
object
}
\{\text{subject},\text{relation},\text{object}\}
in the domains except Math,
knowledge filtering
that filters out low-quality triplets and ensure answer completeness, and
QA pair generation
that construct natural language QA pairs based on the triplets.
Dataset statistics are summarized in Table
1
.
Table 1:
Statistics of the six factual domains in MACE.
#Sub.
: Number of subjects collected from Wikidata.
#Obj.
: Number of objects associated with the subjects and used as answers.
Obj-Type
: Types of the target objects.
#Q.
: Total number of questions in MACE, including those with 1, 2, 4, and 6 correct answers.
#UsedQ
: Used questions sampled from constructed questions.
Domain
Sub.
Obj.
Obj-Type
#Q
#UsedQ
Award
175
2,370
Person
9,384
2,000
Office
159
1,923
Person
6,177
2,000
Region
99
1,536
Country
5,120
2,000
Math
5
–
Number
2,000
2,000
River
810
810
Country
2,000
2,000
Language
933
933
Country
2,000
2,000
3.2
Knowledge Collection
Domain Identification.
We collaborate with LLMs to identify domains in which ground-truth answers are clear and complete. Mathematical questions are straightforward to verify, while factual questions—such as award recipients or regional affiliations—are generally uncontroversial and supported by reliable evidence. Balancing coverage and annotation cost, we ultimately select six domains for inclusion in MACE.
Triplet Collection.
For Math questions, the knowledge is derived via predefined rules.
For other domains, we first use Wikidata
1
1
1
https://query.wikidata.org/sparql
, a widely recognized, reliable knowledge source, to identify all possible subjects and then retrieve their corresponding objects via the predefined relations.
The subject type, relation, and object type of each domain can be found in Table
6
. The subject counts are reported in the
Raw
column of Table
2
.
3.3
Knowledge Filtering
To ensure answer correctness and completeness, we conduct heuristic filtering and manual verification. The count of the remaining subjects after each step is shown in Table
2
.
Heuristic-Based Filtering.
We use a two-stage pipeline to remove low-quality data:
(i)
Popularity Filter
: retains only high-traffic subjects based on Wikipedia pageviews;
(ii)
Validity Filter
: applies domain-specific rules to eliminate invalid or noisy subjects.
This step removes 92.4% of the initial data, retaining a high-quality subset and substantially reducing the workload for human verification.
Manual Verification.
We recruit ten domain experts to manually audit the remaining triplets, recognizing any remaining factual errors and enriching incomplete entries. Finally, they remove an additional 14.5% of subjects, achieving high inter-annotator agreement (Cohen’s
κ
=
0.94
\kappa=0.94
).
Table 2:
Counts of subjects remaining after each filtering step.
Raw
: Total count of retrieved subjects.
Pop.
: Count after popularity filter.
Val.
: Count after validity filter.
Man.
: Count after manual verification.
Domain
Raw
Pop.
Val.
Man.
Award
8,422
4,168
206
175
Office
7,306
5,000
289
159
Region
183
183
129
99
River
10,357
3,726
910
810
Language
7,251
3,830
1,012
933
3.4
QA Pair Generation
For each domain, we design a corresponding prompt template (See Table
5
) and use the remaining triplets to generate QA pairs. We create questions by selecting a subject and its associated relation, with the object serving as the answer. By varying the subjects and relations, we can generate questions with different numbers of correct answers, e.g., “Name one person who received {award} between {lower_year} and {upper_year}”.
For each domain, the number of constructed questions varies, shown in the
#Q
column of Table
1
. To prevent any domain from dominating the evaluation, we sample 500 questions for each setting (1a, 2a, 4a, and 6a) in each domain for evaluation, resulting in 2,000 QA pairs per domain.
3.5
Construction Characteristics
Our construction pipeline ensures that: 1) all questions in MACE have clear, complete, and correct ground-truth answers; 2) questions with different numbers of valid answers are explicitly separated, enabling analysis of answer-count effects and realistic mixed-question scenarios; and 3) questions across varying answer-count settings are grounded in the same knowledge types, differing only in factors such as year range, thereby maintaining comparable difficulty.
4
Experimental Setup
4.1
Confidence Estimation Methods
We categorize existing confidence estimation methods into more fine-grained approaches:
Single-turn
and
Double-turn
approaches. Detailed formulations are provided in Appendix §
B.1
.
Single-turn.
Most of these methods estimate confidence based on whether the model concentrates on a single response for a given question. We further divide them into two types:
•
Question-level Confidence
Malinin and Gales (
2021
); Kadavath
et al.
(
2022
); Kuhn
et al.
(
2023
)
. These methods quantify the entropy of the model’s output distribution.
Prediction Entropy (Prob Entropy)
directly measures the entropy of the answer probability space;
Length-Normalize Prediction Entropy(N-Prob Entropy)
refines this by normalizing for sequence length; and
Semantic Entropy (Sem Entropy)
focuses on the semantic meaning regardless of the specific formatting.
•
Answer-level Confidence
Jiang
et al.
(
2021
); Manakul
et al.
(
2023
); Xiong
et al.
(
2024
)
. These methods evaluate the confidence of specific answers.
Verb
prompts the model to directly express confidence in natural language, while
Verb-Topk
outputs confidence scores for top-
k
k
candidates.
Consistency(Consis)
measures confidence via agreement across multiple sampled outputs.
Consis-Verb
and
Consis-Verb-Topk
further weight this consistency using the verbalized scores from
Verb
and
Verb-Topk
.
Perplexity
directly derives confidence from the sequence’s generation probability.
Double-turn.
These methods adopt a post-hoc approach, measuring confidence through a secondary query after the initial answer is produced, rather than assessing the model’s generation probability for that answer.
•
P
True
P_{\text{True}}
(Kadavath
et al.
,
2022
)
. The model verifies its answer via a binary
True
/
False
judgment. Specifically,
P
True
​
-Consis
P_{\text{True}}\text{-Consis}
approximates the confidence of
True
via black-box sampling, whereas
P
True
​
-Prob
P_{\text{True}}\text{-Prob}
directly extracts the token’s probability. Their conditioned variants,
P
True
​
-Consis-Cand
P_{\text{True}}\text{-Consis-Cand}
and
P
True
​
-Prob-Cand
P_{\text{True}}\text{-Prob-Cand}
, augment the verification prompt with multiple candidate answers to assist the judgment.
•
Self-Ask
(Tian
et al.
,
2023
)
. The model explicitly verbalizes a numerical confidence score in natural language.
Self-Ask
performs this assessment directly, while
Self-Ask-Cand
incorporates multiple candidate answers as assistance.
4.2
Models
We evaluate a diverse set of representative language models across different scales and series.
For open-source models, we include Qwen2.5-Instruct series (7B, 14B, 32B, 72B)
(Yang
et al.
,
2025
)
, LLaMA3.1-Instruct series (8B, 70B)
(Grattafiori
et al.
,
2024
)
, and DeepSeek-V3
(DeepSeek-AI,
2024
)
.
Additionally, we include two state-of-the-art closed-source models GPT-4o-mini and GPT-4o
(Hurst
et al.
,
2024
)
.
4.3
Evaluation
Metrics.
We evaluate the model using three metrics:
Accuracy
measures the correctness of the model’s predictions.
Confidence
quantifies the model’s certainty regarding its predictions.
Area Under the Receiver Operating Characteristic Curve (AUROC)
(Hanley and McNeil,
1982
)
is used to evaluate calibration ability. It quantifies the model’s ability to discriminate between correct and incorrect predictions, where a higher AUROC indicates that the model consistently assigns higher confidence to its correct outputs. For each metric, we report the average across all domains.
Correctness and Consistency Evaluator.
Given the diversity of output formats, we use
GPT-4o
as our primary evaluator, following
Liu
et al.
(
2023
)
. An answer is deemed correct if GPT-4o determines that it matches any of the ground-truth answers. GPT-4o is also employed to assess semantic consistency between pairs of responses. To validate the reliability of these automatic judgments, we perform human evaluation on 300 randomly sampled instances, observing a Cohen’s
κ
\kappa
of 0.92, which indicates high agreement among annotators.
5
Results and Analysis
In this section, we examine how existing confidence estimation methods behave in multi-answer settings. We first analyze how QA performance and estimated confidence vary on questions with more correct answers, and then evaluate calibration performance under mixed questions with different answer counts. Due to space constraints, we focus on LLaMA-3.1-70B-Instruct, which shows trends consistent with other models; full results are provided in Appendix §
C.1
.
Table 3:
Confidence scores of LLaMA-3.1-70B-Instruct under different counts of correct answers. “1a” denotes questions with a single correct answer, and the remaining settings follow the same convention.
Method
1a
2a
4a
6a
Accuracy
48.0
55.4
59.9
61.7
Single-turn
Question-level
Prob Entropy
71.6
70.0
66.6
65.6
N-Prob Entropy
91.5
90.9
89.9
89.7
Sem Entropy
60.8
57.9
49.7
45.2
Answer-level
Verb
94.8
94.7
93.1
92.3
Verb-Topk
81.9
73.9
62.1
56.9
Consis
51.3
48.9
40.2
35.9
Consis-Verb
50.3
47.9
40.5
36.4
Consis-Verb-Topk
47.6
45.9
38.4
34.2
Perplexity
77.6
76.4
73.0
71.0
Double-turn
P
True
-Consis
79.3
79.3
77.0
75.5
P
True
-Prob
79.2
79.0
76.8
75.4
P
True
-Consis-Cand
88.1
87.9
87.1
87.9
P
True
-Prob-Cand
88.1
87.8
87.1
87.8
Self-Ask
63.6
60.9
56.1
54.4
Self-Ask-Cand
64.5
63.5
59.6
56.8
Figure 3:
AUROC of LLaMA-3.1-70B-Instruct on mixed questions with varying counts of correct answers.
Figure 4:
QA performance and confidence variation with the number of correct answers across model scales.
5.1
Model Confidence Decreases as the Number of Correct Answers Increases
As demonstrated in Table
3
, increasing the number of ground-truth answers leads to a steady improvement in accuracy, suggesting that the questions become empirically easier. However, Table
3
reveals a consistent downward trend in confidence across most estimation methods.
This indicates that miscalibration between confidence and QA performance arises in multi-answer settings not only for response-consistency-based methods, but for nearly all existing approaches. Across different domains, the overall trend is similar. In more challenging domains, such as Region, the model’s confidence decreases less sharply (see Figure
9
).
Notably, consistency-based methods exhibit the best calibration performance among existing methods (See Figure
3
and Table
18
). On single-answer questions, consistent with prior studies, the estimated confidence exceeds QA performance, indicating overconfidence. However, when the ground-truth answers become more, the estimated confidence changes from overconfident to over-prudent.
Larger Models Experience a Sharper Confidence Drop.
This phenomenon is shown in Figure
4
.
For instance, within the
LLaMA
series, the 70B model exhibits a significant confidence decrement of
0.154
from single-answer to six-answer settings, while the 8B model drops only
0.056
; notably, its confidence even shows a slight increase when moving from the 1a to the 2a setting.
We speculate that this is because larger models possess a much broader knowledge coverage. As the number of correct answers increases, larger models tend to generate a wider range of potential valid answers. In contrast, smaller models have limited knowledge coverage, so their generation space is often confined to a narrow subset of the possible answers.
We provide a granular investigation into the impact of knowledge coverage, with detailed findings presented in Section
5.3
.
5.2
Calibration Degrades on Mixed Questions with Varying Answer Counts
To evaluate exisiting methods in a more realistic scenario where questions can have different numbers of valid answers, we mix the questions and examine overall calibration performance for each domain. AUROC results are illustrated in Figure
3
. We observe a
consistent downward trend in AUROC as questions become more heterogeneous in the number of correct answers for most of the methods
. This stems from the misalignment between rising accuracy and declining confidence estimates.
Compared to double-turn methods, single-turn methods typically exhibit stronger calibration performance except for verbalized approaches due to models’ inherent overconfidence
(Kadavath
et al.
,
2022
; Lin
et al.
,
2022b
)
.
As we expected in Section §
4
show greater sensitivity to fluctuations in the number of valid answers. This is because they directly use the generation distribution to measure confidence while double-turn methods rely on the model’s post-hoc judgement.
5.3
Why Does Confidence Decline More Sharply in Larger Models?
Definition of Knowledge Coverage.
We consider the knowledge possessed by a model to be reflected in the answers for which it assigns high confidence. Accordingly, we define knowledge coverage as the number of high-confidence answer clusters, where sampled responses are grouped into clusters based on semantic consistency. Specifically, we apply a token-level probability–based filter and retain only clusters whose cumulative probability exceeds a threshold of
τ
=
0.1
\tau=0.1
. A detailed analysis of the cluster probability distribution and the choice of threshold is provided in Appendix §
C.2
.
Figure 5:
Knowledge coverage across ground-truth (GT) set sizes. Different color schemes denote different model families. Color intensity increases from light to dark to indicate increasing model size.
Figure 6:
Distribution of the cluster sizes after filtering.
Figure
5
illustrates how knowledge coverage scales with model size, and Figure
6
shows the distribution of cluster sizes. Larger models consistently exhibit a greater knowledge coverage than smaller ones, with the gap widening as the number of ground-truth answers increases. This suggests that larger models encode broader knowledge, whereas smaller models may fail to produce effective answers even when more correct answers exist.
Consequently, as the number of correct answers increases, larger models—due to their broader knowledge—tend to generate a wider range of potentially correct answers, reducing response consistency and thus lowering estimated confidence. In contrast, smaller models are constrained to a narrower candidate set, leading to a more gradual decline in confidence. As a result, larger models exhibit a sharper confidence decline due to more rapidly increasing knowledge coverage. Further analysis is provided in Appendix §
C.3
.
6
Semantic Confidence Aggregation
In this section, we propose Semantic Confidence Aggregation (SCA), a method for confidence calibration in realistic multi-answer scenarios. The key idea is that overall confidence should reflect the aggregate confidence of all valid answers rather than rely on the single most confident response, and that response inconsistency (e.g., high entropy) does not necessarily imply low confidence.
Table 4:
AUROC score on LLaMA-3.1-70B-Instruct
of different calibration methods under increasing answer mixture.
τ
=
0
\tau=0
denotes no-filtering, while
τ
≠
0
\tau\neq 0
uses the threshold value that achieves the best AUROC on the development set.
Bold
marks the best, and
underlined
the second-best, in each column.
Method
[1]
[1,2]
[1,2,4]
[1,2,4,6]
Single-turn
Question-level
Prob Entropy
74.5
72.6
69.0
66.1
N-Prob Entropy
73.8
70.4
66.2
63.3
Sem Entropy
78.9
78.6
75.8
72.5
Answer-level
Verb
58.4
58.4
57.2
55.8
Verb-Topk
60.7
56.2
51.2
48.4
Consis
80.2
80.3
78.1
75.3
Consis-Verb
79.7
79.1
76.6
73.8
Consis-Verb-Topk
80.0
79.0
77.0
74.3
Perplexity
80.9
79.4
76.5
73.8
Double-turn
P
True
-Consis
68.1
66.4
64.1
63.5
P
True
-Prob
72.9
70.1
67.6
66.7
P
True
-Consis-Cand
62.6
62.7
62.9
62.5
P
True
-Prob-Cand
76.0
73.5
72.5
71.1
Self-Ask
66.5
66.1
65.0
63.9
Self-Ask-Cand
66.5
66.8
66.9
66.1
Confidence Aggregation Baselines
SNCA (
τ
=
0.5
\tau=0.5
)
77.9
77.3
74.2
70.5
SNCA (
τ
=
0
\tau=0
)
50.0
50.0
50.0
50.0
SFCA (
τ
=
0.25
\tau=0.25
)
77.1
77.2
75.2
73.0
SFCA (
τ
=
0
\tau=0
)
50.0
50.0
50.0
50.0
Ours
SCA (
τ
=
0.05
\tau=0.05
)
80.6
81.2
79.2
76.7
SCA (
τ
=
0
\tau=0
)
80.5
81.2
79.1
76.7
Figure 7:
Illustration of SCA method without tuning.
As shown, confidence estimation is dominated by high-confidence clusters. SCA sums probabilities across all clusters, achieving consistent strong calibration performance in both single-answer and multi-answer settings.
6.1
Methodology
Similar to Sem Entropy, we begin by sampling multiple answers and clustering them based on semantic similarity.
Let
𝒮
=
{
s
1
,
…
,
s
N
}
\mathcal{S}=\{s_{1},\dots,s_{N}\}
denote
N
N
sampled responses for a given question. We partition
𝒮
\mathcal{S}
into
M
M
clusters
𝒞
=
{
C
1
,
…
,
C
M
}
\mathcal{C}=\{C_{1},\dots,C_{M}\}
. Since token-level generation probabilities reflect the model’s certainty, for a cluster
C
m
C_{m}
, we compute its confidence as the sum of the token-level probabilities of all responses within the cluster, rather than relying on the proportion of samples it contains. The formulation is:
P
SCA
​
(
C
m
)
=
∑
s
∈
C
m
p
​
(
s
)
,
P_{\text{SCA}}(C_{m})=\sum_{s\in C_{m}}p(s),
(1)
where
p
​
(
s
)
p(s)
represents the token-level generation probability of sequence
s
s
.
Since low-probability responses may be generated by chance rather than representing answers the model considers likely correct, we sum only the probabilities of clusters whose confidence exceeds a threshold
τ
\tau
. The set of valid clusters is defined as
𝒞
valid
=
{
C
m
∈
𝒞
∣
P
​
(
C
m
)
>
τ
}
\mathcal{C}_{\text{valid}}=\{C_{m}\in\mathcal{C}\mid P(C_{m})>\tau\}
and the final confidence score for the question is computed as:
Confidence
=
∑
C
m
∈
𝒞
valid
P
​
(
C
m
)
.
\text{Confidence}=\sum_{C_{m}\in\mathcal{C}_{\text{valid}}}P(C_{m}).
(2)
Experimental results show that SCA achieves comparable performance at
τ
=
0
\tau=0
to that obtained with the optimal
τ
\tau
(Table
4
). This indicates that simply summing token-level probabilities over all sampled responses is sufficient, without requiring clustering or filtering, thereby reducing computational cost.
6.2
Experimental Setup
Additional Aggregation Methods.
To verify whether using token-level probabilities to compute cluster confidence is appropriate, we compare two additional methods. These methods differ only in how cluster confidence is calculated.
•
SNCA (
S
emantic
N
ormalized
C
onfidence
A
ggregation):  normalizes the aggregated token-level probabilities across all clusters to capture relative magnitudes:
P
SNCA
​
(
C
m
)
=
P
SCA
​
(
C
m
)
∑
j
=
1
M
P
SCA
​
(
C
j
)
.
P_{\text{SNCA}}(C_{m})=\frac{P_{\text{SCA}}(C_{m})}{\sum_{j=1}^{M}P_{\text{SCA}}(C_{j})}.
•
SFCA (
S
emantic
F
requency
C
onfidence
A
ggregation): defines probability of a cluster based on the count of samples within it without considering token-level probability:
P
SFCA
​
(
C
m
)
=
|
C
m
|
N
P_{\text{SFCA}}(C_{m})=\frac{|C_{m}|}{N}
.
Models and Datasets.
Due to space constraints, experiments focus on LLaMA-3.1-70B-Instruct; results for other models are reported in Appendix §
D.1
. We randomly sample 20% of MACE as a development set and use the remaining data for testing.
For each aggregation method, two settings are evaluated: a fixed threshold
τ
=
0
\tau=0
and an optimal threshold tuned on the development set.
Figure 8:
Sensitivity of average AUROC across answer settings to the threshold for our methods.
6.3
Results and Analysis
Table
4
shows calibration performance on the test set, and Figure
8
shows how the three aggregation methods vary with the threshold on the development set.
We observe that
SCA matches the best-performing existing methods in the single-answer setting and achieves the strongest results across all three mixed multi-answer scenarios with
τ
=
0
\tau=0
. This means that SCA achieves strong calibration performance without clustering or any filtering, simply by summing the token-level probabilities of all responses. Compared with SNCA and SFCA, SCA is less sensitive to the threshold. This indicates that the absolute values of token-level probabilities inherently capture the model’s perception of answer correctness, assigning high probabilities to likely correct answers and low probabilities to spurious ones, as shown in Figure
7
.
7
Conclusion
This work extends confidence calibration from single-answer QA to a more general setting with mixed numbers of ground-truth answers. We introduce the MACE benchmark, containing 12,000 QA pairs across six factual domains, with 1, 2, 4, or 6 correct answers per question. Using MACE, we evaluate 15 existing calibration methods and find that, as the number of correct answers increases, LLMs achieve higher QA accuracy but lower estimated confidence, leading to severe miscalibration. Consequently, all these methods collapse in realistic settings with mixed answer cardinalities. To address this, we propose SCA (Semantic Confidence Aggregation), which aggregates probabilities of multiple high-confidence answers rather than relying on the top one, achieving state-of-the-art calibration in this general multi-answer setting.
Limitations
While this study offers novel insights into confidence estimation within multi-answer settings, several limitations warrant further consideration. First, our evaluation is currently restricted to English-language datasets; extending this analysis to multilingual or cross-lingual contexts remains essential for a more global understanding of calibration. Second, our scope primarily encompasses short factual responses. Since real-world applications often involve open-ended and compositional generation, investigating confidence behavior in long-form contexts is a crucial next step. Nonetheless, we believe our work provides a useful perspective for more robust calibration frameworks in realistic scenarios.
Ethics Statement
All data used in this study are derived from publicly available and legally accessible sources.
We employ both open-weight and API-based large language models under their respective usage policies.
All experiments are conducted strictly for academic research purposes, without involving human subjects or sensitive content.
References
A. Askell
et al.
(2021)
A general language assistant as a laboratory for alignment
.
arXiv preprint arXiv:2112.00861
.
Cited by:
§1
.
J. Cole, M. Zhang, D. Gillick, J. Eisenschlos, B. Dhingra, and J. Eisenstein (2023)
Selectively answering ambiguous questions
.
In
Proceedings of EMNLP 2023
,
pp. 530–543
.
External Links:
Document
Cited by:
§2
.
DeepSeek-AI (2024)
DeepSeek-v3: scaling open-source language models with dense and mixture-of-experts architecture
.
arXiv preprint arXiv:2412.19437
.
External Links:
2412.19437
Cited by:
§4.2
.
S. Desai and G. Durrett (2020)
Calibration of pre-trained transformers
.
arXiv preprint arXiv:2003.07892
.
Cited by:
§1
,
§1
.
Y. Elazar, N. Kassner, S. Ravfogel, E. Ravichander, H. Schütze, and Y. Goldberg (2021)
Measuring and improving consistency in pre-trained language models
.
In
Transactions of the Association for Computational Linguistics (TACL)
,
Cited by:
§2
.
A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, and … (2024)
The llama 3 herd of models
.
Note:
arXiv preprint arXiv:2407.21783[cs.AI]
External Links:
Link
,
Document
Cited by:
§4.2
.
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger (2017)
On calibration of modern neural networks
.
In
International conference on machine learning
,
pp. 1321–1330
.
Cited by:
§1
,
§1
.
J. A. Hanley and B. J. McNeil (1982)
The meaning and use of the area under a receiver operating characteristic (roc) curve.
.
Radiology
143
(
1
),
pp. 29–36
.
Cited by:
§4.3
.
D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt (2021)
Measuring massive multitask language understanding
.
In
Proceedings of the International Conference on Learning Representations (ICLR)
,
Cited by:
§2
.
J. Hu
et al.
(2023)
Uncertainty in natural language generation: from theory to practice
.
ArXiv preprint
.
Note:
(Note: Verify specific title for Hu et al 2023 depending on context, assuming FalseQA refers to recent hallucination work)
Cited by:
§2
.
A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow, A. Welihinda, A. Hayes, A. Radford, A. Mądry, …, R. Zellers, and … (2024)
GPT-4o system card
.
Note:
arXiv preprint arXiv:2410.21276[cs.CL]
External Links:
Link
,
Document
Cited by:
§4.2
.
Z. Jiang, J. Araki, H. Ding, and G. Neubig (2021)
How can we know when language models know? on the calibration of language models for question answering
.
Transactions of the Association for Computational Linguistics
9
,
pp. 962–977
.
External Links:
Document
Cited by:
4th item
,
§1
,
§2
,
2nd item
.
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson,
et al.
(2022)
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
External Links:
2207.05221
Cited by:
1st item
,
1st item
,
2nd item
,
§2
,
1st item
,
1st item
,
§5.2
.
R. Kamoi
et al.
(2023)
WiCE: real-world entailment for claims in wikipedia
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)
,
Cited by:
§2
.
L. Kuhn, Y. Gal, and S. Farquhar (2023)
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
International Conference on Learning Representations (ICLR)
,
External Links:
2302.09664
Cited by:
3rd item
,
§1
,
1st item
.
J. Li, X. Cheng, W. X. Zhao, J. Nie, and J. Wen (2023)
HaluEval: a large-scale hallucination evaluation benchmark for large language models
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)
,
Cited by:
§2
.
S. Lin, J. Hilton, and O. Evans (2022a)
Teaching models to express their uncertainty in words
.
Transactions on Machine Learning Research
.
External Links:
Link
Cited by:
§1
,
§2
.
S. Lin, J. Hilton, and O. Evans (2022b)
TruthfulQA: measuring how models mimic human falsehoods
.
arXiv preprint arXiv:2109.07958
.
External Links:
2109.07958
Cited by:
§5.2
.
C. Ling, X. Zhao, X. Zhang, W. Cheng, Y. Liu, Y. Sun, M. Oishi, T. Osaki, K. Matsuda, J. Ji, G. Bai, L. Zhao, and H. Chen (2024)
Uncertainty quantification for in-context learning of large language models
.
In
Proceedings of NAACL 2024
,
pp. 3357–3370
.
External Links:
Document
Cited by:
§2
.
X. Liu
et al.
(2023)
Evaluating the necessary and sufficient conditions for knowledge understanding in large language models
.
ArXiv preprint
.
Cited by:
§2
.
Y. Liu, D. Iter, Y. Xu, S. Wang, R. Xu, and C. Zhu (2023)
G-eval: nlg evaluation using gpt-4 with better human alignment
.
arXiv preprint arXiv:2303.16634
.
External Links:
Link
Cited by:
§4.3
.
Q. Lyu, K. Shridhar, C. Malaviya, L. Zhang, Y. Elazar, N. Tandon, M. Apidianaki, M. Sachan, and C. Callison-Burch (2024)
Calibrating large language models with sample consistency
.
arXiv preprint arXiv:2402.13904
.
External Links:
2402.13904
Cited by:
§2
.
A. Malinin and M. Gales (2021)
Uncertainty estimation in autoregressive structured prediction
.
In
International Conference on Learning Representations (ICLR)
,
External Links:
Link
Cited by:
2nd item
,
1st item
.
P. Manakul, A. Liusie, and M. Gales (2023)
SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models
.
In
Proceedings of EMNLP 2023
,
pp. 9004–9017
.
External Links:
Document
Cited by:
1st item
,
1st item
,
§1
,
§2
,
2nd item
.
J. Maynez, S. Narayan, B. Bohnet, and R. McDonald (2020)
On faithfulness and factuality in abstractive summarization
.
In
Proceedings of ACL 2020
,
pp. 1906–1919
.
Cited by:
§1
.
S. Min, K. Krishna, X. Velocity, S. Singh, and H. Hajishirzi (2023)
FActScore: fine-grained atomic evaluation of factual precision in long form text generation
.
In
Proceedings of ACL 2023
,
Cited by:
§1
.
S. Ni, K. Bi, J. Guo, and X. Cheng (2024)
When do llms need retrieval augmentation? mitigating llms’ overconfidence helps retrieval augmentation
.
arXiv preprint arXiv:2402.11457
.
Cited by:
§1
,
§1
.
S. Ni, K. Bi, J. Guo, M. Tang, J. Wu, Z. Han, and X. Cheng (2025a)
Annotation-efficient universal honesty alignment
.
arXiv preprint arXiv:2510.17509
.
Cited by:
§1
,
§2
.
S. Ni, K. Bi, J. Guo, L. Yu, B. Bi, and X. Cheng (2025b)
Towards fully exploiting llm internal states to enhance knowledge boundary perception
.
arXiv preprint arXiv:2502.11677
.
Cited by:
§1
,
§2
.
J. Ren, J. Luo, Y. Zhao, K. Krishna, M. Saleh, B. Lakshminarayanan, and P. J. Liu (2023)
Out-of-distribution detection and selective generation for conditional language models
.
In
International Conference on Learning Representations (ICLR)
,
External Links:
Link
Cited by:
§2
.
C. Si, Z. Gan, Z. Yang, S. Wang, J. Wang, J. Boyd-Graber, and L. Wang (2022)
Prompting gpt-3 to be reliable
.
arXiv preprint arXiv:2210.09150
.
Cited by:
§1
.
S. H. Tanneru, C. Agarwal, and H. Lakkaraju (2024)
Quantifying uncertainty in natural language explanations of large language models
.
In
Proceedings of the 27th International Conference on Artificial Intelligence and Statistics (AISTATS)
,
Proceedings of Machine Learning Research
, Vol.
238
,
pp. 1072–1080
.
External Links:
Link
Cited by:
§2
.
J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal (2018)
FEVER: a large-scale dataset for fact extraction and verification
.
In
Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT)
,
Cited by:
§2
.
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. Manning (2023)
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
Proceedings of EMNLP 2023
,
Singapore
,
pp. 5433–5442
.
Cited by:
1st item
,
2nd item
,
§2
,
2nd item
.
G. P. Wightman, A. Delucia, and M. Dredze (2023)
Strength in numbers: estimating confidence of large language models by prompt agreement
.
In
Proceedings of the 3rd Workshop on Trustworthy Natural Language Processing (TrustNLP 2023)
,
pp. 326–362
.
External Links:
Document
Cited by:
§2
.
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi (2024)
Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms
.
In
International Conference on Learning Representations (ICLR 2024)
,
Cited by:
5th item
,
2nd item
,
§1
,
§1
,
2nd item
.
A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, H. Lin, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Lin, K. Dang, K. Lu, K. Bao, K. Yang, L. Yu, M. Li, M. Xue, P. Zhang, Q. Zhu, R. Men, R. Lin, T. Li, T. Tang, T. Xia, X. Ren, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Wan, Y. Liu, Z. Cui, Z. Zhang, and Z. Qiu (2025)
Qwen2.5 technical report
.
Note:
arXiv preprint arXiv:2412.15115[cs.CL]
External Links:
Link
,
Document
Cited by:
§4.2
.
Y. Yang, E. Chern, X. Qiu, G. Neubig, and P. Liu (2024)
Alignment for honesty
.
In
Proceedings of the 38th Annual Conference on Neural Information Processing Systems (NeurIPS)
,
External Links:
Link
Cited by:
§2
.
Z. Yang, P. Qi, S. Zhang, Y. Bengio, W. W. Cohen, R. Salakhutdinov, and C. D. Manning (2018)
HotpotQA: a dataset for diverse, explainable multi-hop question answering
.
In
Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP)
,
Cited by:
§2
.
Z. Yin, Q. Sun, Q. Guo, J. Wu, X. Qiu, and X. Huang (2023)
Do large language models know what they don’t know?
.
In
Findings of the Association for Computational Linguistics: ACL 2023
,
Cited by:
§1
,
§1
,
§2
.
H. Zhang, S. Diao, Y. Lin, Y. R. Fung, Q. Lian, X. Wang, Y. Chen, H. Ji, and T. Zhang (2024)
R-tuning: instructing large language models to say ‘I don’t know’
.
In
Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
,
pp. 7106–7132
.
External Links:
Link
Cited by:
§2
.
J. Zhang, Z. Li, K. Das, B. Malin, and S. Kumar (2023)
SAC3: reliable hallucination detection in black-box language models via semantic-aware cross-check consistency
.
In
Findings of the Association for Computational Linguistics: EMNLP 2023
,
pp. 15445–15458
.
Cited by:
§1
.
Domain
Core Prompt Template
Award
Name one person who received {award} between {lower_year} and {upper_year}.
Office
Name one person from who officially assumed the office of {office name} between {lower_year} and {upper_year}.
Country
Name one first-level administrative division of {country} whose area lies between {lower_area} and {upper_area} km
2
.
Math
Name one {number type} number between {lower_num} and {upper_num}.
Language
Name one country where {language_1},{language_2} or {language_3} was predominantly spoken by native speakers.
River
Name one country through which the {river_1}, {river_2}, or {river_3} flows.
Table 5:
Core prompt templates for each factual domain.
Table 6:
Detailed schema of relations and entity types across six factual domains.
This table outlines the semantic categories for subjects and objects, along with the specific predicates used to query the knowledge graph.
Domain
Subject Type
Relation Description
Object Type
Honorable Award
Award Name
Is officially awarded to
Person
Political Office
Political Position
Is officially held by
Person
Regional Affiliation
Sovereign Country
Contains
First-level Administrative Division
Mathematical Concept
Number Types
Includes as an instance
Number
Natural River
River Name
Flows through geographically
Country
Linguistic Culture
Human Language
Is spoken widely in
Country
Appendix A
The MACE Benchmark
A.1
Domain Identification
To ensure the quality and utility of the benchmark, we establish three core selection principles: objective verifiability, knowledge diversity, and cross-difficulty coverage. Guided by these criteria, we conduct iterative LLM prompting (e.g., GPT-4o, DeepSeek-V3) followed by expert deliberation to refine candidate topics. Ultimately, we finalize six representative factual domains: Honorable Award (Award), Political Office (Office), Regional Affiliation (Region), Mathematical Concept (Math), Natural River (River), and Linguistic Culture (Language).
A.2
Triplet Collection
In our setting, knowledge is represented as a triplet
(
s
,
r
,
𝒪
)
(s,r,\mathcal{O})
, where each component is defined as follows:
(1) The
subject
s
s
represents the primary entity or anchor of the query (e.g.,
Nobel Prize in Physics
);
(2) The
relation
r
r
denotes the semantic predicate or attribute connecting the subject to the answers (e.g.,
laureate of
);
(3) The
object set
𝒪
=
{
o
1
,
o
2
,
…
,
o
k
}
\mathcal{O}=\{o_{1},o_{2},\dots,o_{k}\}
contains the set of all valid ground-truth entities that satisfy the relation
r
r
for subject
s
s
.
By varying the cardinality of the object set
|
𝒪
|
∈
{
1
,
2
,
4
,
6
}
|\mathcal{O}|\in\{1,2,4,6\}
.
Except for the
Math
domain, which is generated through rule synthesis,
all other domains are collected via the Wikidata SPARQL endpoint
2
2
2
https://query.wikidata.org/sparql
.
Specifically, for each domain, we query Wikidata to retrieve relevant subjects and their associated factual objects based on defined relations (see Table
6
). For instance, in the
Award
domain, we retrieve the entity
Nobel Prize in Physics
as the subject and obtain its
laureates
in a specific year as the objects based on relations "is officially awarded to". To ensure alignment with common model knowledge, we restrict the temporal coverage to the years 1800–2023.
A.3
Heuristic-Based Filtering
To ensure data quality, we apply a two-stage filtering process:
Popularity Filter
followed by a
Validity Filter
.
Popularity Filter
is applied to the subjects of the knowledge triplets while
Validity filter
is applied to subjects and objects.
Popularity Filter
ranks all entity labels within each domain by their 12-month Wikipedia pageviews, retaining the top 5K entries and any items with more than 1K views.
Afterward,
Validity Filter
removes entries with empty or invalid fields (e.g., missing labels, broken links, unresolved QIDs) and applies domain-specific refinement criteria.
Because raw Wikidata outputs are often incomplete or noisy, we further impose structured constraints to ensure factual consistency and completeness:
•
Award:
retain only subjects granted to a single laureate per year,
with continuous yearly records and at least three objects per subject.
•
Office:
preserve subjects held by exactly one person per year,
requiring a minimum of ten recorded years per subject.
•
Region:
include only countries with at least three administrative subdivisions.
•
River
&
Language:
keep entities associated with no more than six countries
to avoid overly generic mappings. To control annotation cost, we sample 600 instances
from objects associated with a single subject.
A.4
Manual Verification
To ensure the factual accuracy and internal consistency of all harvested labels,
we conduct a multi-stage human verification process.
Two domain experts independently review each domain’s entries
for factual correctness, completeness, and consistency with Wikidata metadata.
Each label is cross-checked against its supporting evidence
(e.g., year, person, or country linkage)
to confirm semantic validity and eliminate potential entity mismatches.
Disagreements are resolved through consensus discussions.
Annotation reliability, measured using Cohen’s
κ
=
0.94
\kappa=0.94
across all domains, indicating strong agreement.
We further perform iterative spot-checking for quality assurance:
for each domain, a random sample of 50 instances is revalidated
to confirm factual soundness and formatting consistency.
This verification–revision loop is repeated until no residual errors remain
(two full rounds in total).
A.5
QA Pair Generation
Our prompt templates are summarized in Table
5
.
Retrival-based Domains.
Each domain consists of a unique set of factual subjects, where each subject is linked to one or more objects, forming the foundational knowledge triplets
(
s
,
r
,
𝒪
)
(s,r,\mathcal{O})
. To construct questions with a specific number of correct answers (
k
∈
{
1
,
2
,
4
,
6
}
k\in\{1,2,4,6\}
), we dynamically adjust the constraints within each domain.
Specifically, we employ a
constraint relaxation
strategy to obtain triplets with the desired number of ground-truth objects based on the initial subject-to-object mapping. We implement this through two distinct approaches:
(1)
One-to-Many Expansion (Intra-subject):
. Include domains
Award
,
Office
, and
Region
. For subjects that naturally possess multiple objects under a broad relation, we relax the relational constraints while keeping the subject fixed. For instance, instead of querying for the "winner of the 1995 Nobel Prize in Physics" (single-answer), we expand the relation to "winners of the Nobel Prize in Physics between 1990 and 1995" to harvest a larger, pre-defined set of objects.
(2)
One-to-Few Aggregation (Cross-subject):
Include domains
Language
and
River
. For scenarios where a single subject-relation pair cannot naturally yield enough objects, we construct multi-answer instances by systematically combining multiple subjects that share the same relation. For example, we may aggregate two subjects that each possess only one or two correct answers into a single question (e.g., "Name one country speaking language A or language B") to satisfy the required answer count.
This dual-path approach ensures that the factual density of our benchmark is systematically controlled while maintaining logical coherence and high relevance across different answer counts.
Rule-based Domain.
The
Math
domain is defined through five numeric subjects. (Table
7
),
each acting as a pseudo-label.
As these categories span broad numerical ranges, we do not construct natural questions explicitly.
Instead, we generate queries by uniformly sampling numbers from the interval
[
0
,
1
,
000
,
000
]
[0,\,1{,}000{,}000]
,
providing wide coverage of numerical reasoning behaviors.
Quality control
All generated QA instances first undergo rigorous deduplication, and we ensure that no label appears in multiple domains to prevent cross-domain leakage.
To construct a representative and balanced dataset, we employ a clustering-based sampling strategy.
Specifically, for each answer setting within a domain, we perform K-Means clustering to partition the instances into
k
=
500
k=500
clusters and select the sample closest to the centroid of each cluster.
This process yields 2,000 distinct samples per domain, resulting in a final dataset totaling 12,000 instances.
Number Type
Definition
prime
p
>
1
,
p
∈
ℕ
,
∄
​
d
∈
(
1
,
p
)
:
d
∣
p
p>1,\;p\in\mathbb{N},\;\nexists d\in(1,p):\,d\mid p
square
n
=
k
2
,
k
∈
ℕ
n=k^{2},\;k\in\mathbb{N}
cube
n
=
k
3
,
k
∈
ℕ
n=k^{3},\;k\in\mathbb{N}
fibonacci
F
n
=
F
n
−
1
+
F
n
−
2
,
F
1
=
F
2
=
1
F_{n}=F_{n-1}+F_{n-2},\;F_{1}=F_{2}=1
triangular
T
n
=
n
​
(
n
+
1
)
2
,
n
∈
ℕ
T_{n}=\frac{n(n+1)}{2},\;n\in\mathbb{N}
Table 7:
Five mathematical number types used to construct questions in the
Math
domain.
Each defines a distinct numeric sequence within
[
0
,
10
6
]
[0,\,10^{6}]
.
Appendix B
Experiment Setup
B.1
Calibration Methods
•
Prediction Entropy.
Kadavath
et al.
(
2022
)
To capture uncertainty across
M
M
generated responses, we compute the mean token-level entropy over all samples:
U
Prob Entropy
=
−
1
M
​
∑
j
=
1
M
∑
i
=
1
|
r
j
|
p
z
i
​
log
⁡
p
z
i
,
U_{\text{Prob Entropy}}=-\frac{1}{M}\sum_{j=1}^{M}\sum_{i=1}^{|r_{j}|}p_{z_{i}}\log p_{z_{i}},
(3)
where
p
z
i
p_{z_{i}}
represents the normalized probability distribution over tokens within the
j
j
-th generation.
•
Length-Normalized Prediction Entropy.
Malinin and Gales (
2021
)
To avoid bias toward longer sequences, we normalize the entropy of each sampled response by its length:
U
N-Prob Entropy
=
−
1
M
​
∑
j
=
1
M
1
|
r
j
|
​
∑
i
=
1
|
r
j
|
p
z
i
​
log
⁡
p
z
i
.
U_{\text{N-Prob Entropy}}=-\frac{1}{M}\sum_{j=1}^{M}\frac{1}{|r_{j}|}\sum_{i=1}^{|r_{j}|}p_{z_{i}}\log p_{z_{i}}.
(4)
This normalization ensures comparable uncertainty estimates across outputs of varying lengths.
•
Semantic Entropy.
Kuhn
et al.
(
2023
)
Given a set of semantic clusters
{
C
1
,
…
,
C
K
}
\{C_{1},\dots,C_{K}\}
obtained from multiple sampled responses,
we compute a probability distribution over clusters by aggregating the sentence-level probabilities.
Specifically, the probability assigned to cluster
C
k
C_{k}
is
P
​
(
C
k
)
=
∑
r
j
∈
C
k
P
​
(
r
j
)
,
P(C_{k})=\sum_{r_{j}\in C_{k}}P(r_{j}),
(5)
where
P
​
(
r
j
)
P(r_{j})
denotes the generation probability of response
r
j
r_{j}
.
In standard semantic-entropy settings, these cluster probabilities are typically normalized to form a valid distribution:
P
~
​
(
C
k
)
=
P
​
(
C
k
)
∑
i
=
1
K
P
​
(
C
i
)
,
\tilde{P}(C_{k})=\frac{P(C_{k})}{\sum_{i=1}^{K}P(C_{i})},
(6)
yielding
P
~
​
(
C
k
)
∈
[
0
,
1
]
\tilde{P}(C_{k})\in[0,1]
and
∑
k
P
~
​
(
C
k
)
=
1
\sum_{k}\tilde{P}(C_{k})=1
.
The semantic entropy is then computed as the Shannon entropy of the normalized cluster distribution:
U
SE
=
−
∑
k
=
1
K
P
~
​
(
C
k
)
​
log
⁡
P
~
​
(
C
k
)
,
U_{\text{SE}}=-\sum_{k=1}^{K}\tilde{P}(C_{k})\log\tilde{P}(C_{k}),
(7)
which quantifies the degree of semantic dispersion in the model’s outputs—high values indicate diverse or inconsistent answer patterns, while low values correspond to concentrated semantic predictions.
•
Verb.
(Jiang
et al.
,
2021
)
This method elicits confidence by prompting the model to verbalize a numeric confidence score alongside its answer.
Given a question
x
x
, the model generates a textual response containing both the answer
y
^
\hat{y}
and a confidence expression.
The confidence value
C
C
is then extracted from the generated text:
C
Verb
=
LLM
​
(
x
)
.
C_{\text{Verb}}=\text{LLM}(x).
(8)
Example prompt:
[Instruction]
You are a knowledgeable assistant.
Please answer the following question and provide your confidence as a numeric value between 0 and 1
(e.g., 0.85 means you are 85% confident).
[Input]
Question: {question}
[Output format]
Answer: {answer}
Confidence: {confidence between 0 and 1, with two-decimal precision}
•
Verb
Topk
.
(Xiong
et al.
,
2024
)
This variant extends the verbalization setting by asking the model to provide
k
k
distinct candidate answers
{
y
^
1
,
y
^
2
,
…
,
y
^
k
}
\{\hat{y}_{1},\hat{y}_{2},\dots,\hat{y}_{k}\}
along with their respective confidences
{
C
1
,
C
2
,
…
,
C
k
}
\{C_{1},C_{2},\dots,C_{k}\}
.
The final confidence is defined as the maximum confidence among semantically valid candidates:
C
Verb
Topk
=
max
1
≤
i
≤
k
⁡
(
C
i
⋅
𝕀
​
{
y
^
i
∈
𝒴
∗
}
)
,
C_{\text{Verb\textsubscript{Topk}}}=\max_{1\leq i\leq k}\left(C_{i}\cdot\mathbb{I}\{\hat{y}_{i}\in\mathcal{Y}^{*}\}\right),
(9)
where
𝒴
∗
\mathcal{Y}^{*}
denotes the set of semantically valid answers.
Example prompt:
[Instruction]
You are a knowledgeable assistant.
Please list your top-$k$ most likely answers to the following question.
For each answer, report your numeric confidence between 0 and 1
(e.g., 0.85 means 85% confident).
Use two-decimal precision for all confidence values.
[Input]
Question: {question}
[Output format]
1. Answer: {answer_1}, Confidence: {confidence_1}
2. Answer: {answer_2}, Confidence: {confidence_2}
3. Answer: {answer_3}, Confidence: {confidence_3}
… up to $k$ answers.
•
Consistency.
Manakul
et al.
(
2023
)
Consistency score measures the proportion of model samples that agree with the aggregated prediction
Y
~
\tilde{Y}
among
M
M
sampled outputs:
C
consistency
=
1
M
​
∑
i
=
1
M
𝕀
​
{
Y
^
i
=
Y
~
}
,
C_{\text{consistency}}=\frac{1}{M}\sum_{i=1}^{M}\mathbb{I}\{\hat{Y}_{i}=\tilde{Y}\},
(10)
•
Weighted Consistency
Xiong
et al.
(
2024
)
To incorporate the self-reported confidence
C
i
C_{i}
of each sampled answer, we further introduce a weighted variant:
C
conf
=
∑
i
=
1
M
𝕀
​
{
Y
^
i
=
Y
~
}
×
C
i
∑
i
=
1
M
C
i
,
C_{\text{conf}}=\frac{\sum_{i=1}^{M}\mathbb{I}\{\hat{Y}_{i}=\tilde{Y}\}\times C_{i}}{\sum_{i=1}^{M}C_{i}},
(11)
where higher-confidence answers contribute proportionally more to the final score.
When
C
i
C_{i}
is obtained from the
Verb
or
Verb
Topk
methods, this variant corresponds to
Consistency-Verb
and
Consistency-Verb-Topk
, respectively.
•
Perplexity.
Manakul
et al.
(
2023
)
Perplexity is computed as the average negative log-likelihood of token probabilities:
U
Perplexity
=
−
1
|
r
|
​
∑
i
=
1
N
log
⁡
p
z
i
,
U_{\text{Perplexity}}=-\frac{1}{|r|}\sum_{i=1}^{N}\log p_{z_{i}},
(12)
where
r
r
denotes the generated sequence and
p
z
i
p_{z_{i}}
is the model-assigned probability for the
i
i
-th token.
•
P
True
-Consis/P
True
-Prob
(Kadavath
et al.
,
2022
)
.
These methods estimate model confidence by prompting the LLM to explicitly verify whether its previously generated answer is correct.
The verification prompt
x
′
x^{\prime}
asks the model to respond with “
True
” or “
False
”, and the resulting confidence is defined as the probability of the token “
True
”:
C
P
True
=
p
​
(
z
true
∣
x
′
)
.
C_{\text{P\textsubscript{True}}}=p(z_{\text{true}}\mid x^{\prime}).
(13)
We implement two variants:
(1) In the
P
True
-Consis
variant, confidence is obtained by performing multiple sampling runs and taking the empirical frequency of the “
True
” response across samples;
(2) In the
P
True
-Prob
variant, we directly use the model’s internal probability (logit-derived softmax value) assigned to the “
True
” token, without repeated sampling.
Example prompt:
[Instruction]
You will be given a question and the model’s previous answer.
Please respond with
True
if the answer is factually correct, or
False
if it is incorrect.
Answer strictly with either “True” or “False” only.
[Input]
Question: What is the capital of France?
Model answer: Paris.
[Output]
True
•
P
True
-Consis-Cand/P
True
-Prob-Cand
(Kadavath
et al.
,
2022
)
.
To better handle multi-answer scenarios, we extend the verification prompt
x
′
x^{\prime}
by including a set of candidate answers
{
a
1
,
a
2
,
…
,
a
K
}
\{a_{1},a_{2},\dots,a_{K}\}
, allowing the model to evaluate its response in the context of multiple plausible answers:
C
P
True
-Consis-Cand
=
p
​
(
z
true
∣
x
′
,
{
a
1
,
a
2
,
…
,
a
K
}
)
.
C_{\text{P\textsubscript{True}-Consis-Cand}}=p(z_{\text{true}}\mid x^{\prime},\{a_{1},a_{2},\dots,a_{K}\}).
(14)
Similarly, two variants are considered:
(1) In the
P
True
-Consis-Cand
variant, confidence is computed as the empirical frequency of “
True
” responses across multiple sampling runs;
(2) In the
P
True
-Prob-Cand
variant, the probability assigned to the “
True
” token from the model’s logits is used directly as the confidence score.
Example prompt:
[Instruction]
You will be given a question, the model’s answer, and several candidate answers.
Please respond with
True
if the model’s answer is factually correct,
or
False
if it is incorrect.
Answer strictly with either “True” or “False” only.
[Input]
Question: Which player won the UEFA Euro 2016 Best Young Player Award?
Model answer: Renato Sanches.
Candidate answers: Renato Sanches, Anthony Martial, Raheem Sterling.
[Output]
True
•
Self
Ask
(Tian
et al.
,
2023
)
.
This method prompts the model to
self-assess
and directly verbalize its own confidence score after producing an answer.
Given a question–answer pair
(
x
,
y
^
)
(x,\hat{y})
, the model is re-prompted with a meta-instruction asking it to output a numerical confidence value (e.g., “0.85”) that reflects how certain it is about
y
^
\hat{y}
.
The resulting confidence is defined as:
C
Self
Ask
=
LLM
​
(
x
′
,
y
^
)
,
C_{\text{Self\textsubscript{Ask}}}=\text{LLM}(x^{\prime},\hat{y}),
(15)
where
x
′
x^{\prime}
denotes the self-assessment prompt and
LLM
​
(
⋅
)
\text{LLM}(\cdot)
returns a scalar confidence value verbalized by the model.
Example prompt:
Question:
What is the capital of France?
Answer:
Paris.
How confident are you that your answer is correct?
Please output only a number between 0 and 1 (e.g., 0.85).
•
Self
Ask
-Cand
Tian
et al.
(
2023
)
.
To better account for uncertainty among multiple plausible answers, this variant augments the verification prompt with a set of candidate answers
{
a
1
,
a
2
,
…
,
a
K
}
\{a_{1},a_{2},\dots,a_{K}\}
.
The model is instructed to assess its confidence in
y
^
\hat{y}
given this broader context.
The confidence is computed as:
C
Self
Ask
-Cand
=
LLM
​
(
x
′
,
y
^
,
{
a
1
,
a
2
,
…
,
a
K
}
)
,
C_{\text{Self\textsubscript{Ask}-Cand}}=\text{LLM}(x^{\prime},\hat{y},\{a_{1},a_{2},\dots,a_{K}\}),
(16)
where
x
′
x^{\prime}
includes both the original answer and the candidate list as context for self-evaluation.
Example prompt:
Question:
What is the capital of France?
Candidate answers: Paris, Lyon, Marseille.
Considering these candidates, how confident are you that your original answer (Paris) is correct?
Please output only a number between 0 and 1 (e.g., 0.85).
Figure 9:
Domain-specific accuracy and confidence under different ground-truth sizes.
B.2
Domain Effects: Relation Between Question Type and Difficulty
We analyze the domain-level calibration behavior of
LLaMA-3.1-70B-Instruct
across varying ground-truth set sizes. As illustrated in Figure
9
, all configurations (
1a/2a/4a/6a
) exhibit a highly consistent trend: domains characterized by higher accuracy (lower intrinsic difficulty) also demonstrate higher confidence levels. Crucially, due to the significant disparity in intrinsic difficulty across these specialized domains, we employ the macro-average as the primary metric. This approach prevents the aggregate performance from being disproportionately skewed by high-accuracy, low-difficulty domains, thereby ensuring a more representative evaluation of global calibration.
The observed variation in accuracy and confidence is primarily driven by the structural differences in question construction across domains (see Appendix §
A.5
). Each domain imposes unique constraints on how questions are formulated and how answers are distributed, which directly modulates the cognitive load and retrieval complexity of the task.
One-to-Few Domains (Language, River): Low Difficulty.
Domains such as
Language
and
River
follow a one-to-few mapping, where each subject is associated with only a handful of factual objects. Multi-answer questions are constructed by relaxing constraints of subjects scope. Since the options consist of short, distinct noun phrases within a tightly bounded semantic space, the model encounters minimal ambiguity. Consequently, these domains yield the highest accuracy and confidence.
One-to-Many Domains (Award, Office, Region): Moderate to High Difficulty.
In
Award
,
Office
, and
Region
, each subject corresponds to a vast pool of factual objects. To ensure answer uniqueness, questions must be grounded in specific contextual attributes (e.g., years, tenure, or administrative roles). This necessitates additional reasoning steps, such as linking a specific temporal constraint to a unique recipient, thereby increasing the complexity of the
answer space
. Among these,
Region
represents the most challenging domain; many entities share similar geopolitical or geographic features, leading to high semantic overlap and an increased likelihood of model confusion.
Rule-Based Numerical Questions (Math): Moderate Difficulty.
The
Math
domain utilizes five numeric categories as subjects, with queries constructed by sampling values from broad numerical intervals. Unlike the factual retrieval required in other domains, these tasks demand the recognition of abstract numeric properties. The resulting performance is intermediate—outperforming the complex attribute-linking in
Award
and
Country
, but proving more difficult than the simple noun-phrase enumeration found in
Language
and
River
.
Appendix C
Results and Analysis
C.1
Estimated Confidence Drops on Questions with More Correct Answers.
We report the
confidence
of all evaluated models under different numbers of valid answers (
1a/2a/4a/6a
), as shown in Tables
8
–
15
. Note that for API-based models (e.g., GPT-4o, GPT-4o-mini, and DeepSeek-V3), we do not report methods that rely on logit probabilities or internal token distributions, such as Prob-Entropy, N-Prob-Entropy and Sem Entropy.
Across model families and parameter scales, a clear and consistent pattern emerges: model accuracy follows a steady upward trend as the number of valid answers increases. However, the model confidence exhibits a diametrically opposite decline over the same range. This diverging behavior reveals a significant misalignment between the models’ actual performance and their certainty: as the task environment becomes more "favorable" (i.e., more valid answers are available), the models paradoxically become increasingly "underconfident." Such a monotonic decline in confidence despite rising accuracy demonstrates that existing calibration methods are unable to remain stable when confronted with multi-answer variation, highlighting a fundamental limitation of current approaches.
Table 8:
Confidence scores of
Qwen2.5-7B-Instruct
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Prob Entropy
67.8
68.2
66.9
66.6
N-Prob Entropy
92.1
92.3
92.0
91.9
Sem Entropy
64.7
65.5
63.6
62.9
Answer-level
Verb
94.7
95.4
94.8
94.7
Verb
Topk
82.5
81.3
73.7
71.8
Consistency
53.1
54.7
52.6
51.9
Consis-Verb
44.9
44.3
41.2
40.5
Consis-Verb-Topk
35.1
35.3
31.1
30.7
Perplexity
79.2
79.6
79.4
79.1
Double-turn
P
True
-Consis
46.9
47.0
45.0
46.9
P
True
-Prob
46.8
46.9
44.9
46.8
P
True
-Consis-Cand
59.3
61.0
62.9
65.0
P
True
-Prob-Cand
59.4
61.1
63.0
65.2
Self
Ask
73.7
73.8
73.0
73.7
Self
Ask
-Cand
70.5
71.5
71.1
72.2
Table 9:
Confidence scores of
Qwen2.5-14B-Instruct
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Prob Entropy
73.4
73.3
72.4
71.7
N-Prob Entropy
93.7
93.6
93.5
93.2
Sem Entropy
70.6
71.3
69.9
68.4
Answer-level
Verb
87.4
87.1
85.6
85.4
Verb
Topk
87.6
84.0
74.1
70.5
Consistency
62.7
63.3
62.5
61.0
Consis-Verb
42.2
45.6
43.4
41.7
Consis-Verb-Topk
45.5
44.8
42.7
40.7
Perplexity
85.6
85.8
85.8
85.4
Double-turn
P
True
-Consis
50.1
52.2
49.4
49.5
P
True
-Prob
50.1
52.2
49.4
49.5
P
True
-Consis-Cand
67.1
69.8
71.8
71.9
P
True
-Prob-Cand
67.1
69.8
71.8
71.9
Self
Ask
77.5
78.7
76.0
75.2
Self
Ask
-Cand
76.2
78.2
78.0
77.4
Table 10:
Confidence scores of
Qwen2.5-32B-Instruct
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Prob Entropy
74.9
74.2
73.4
72.7
N-Prob Entropy
94.1
94.1
93.8
93.6
Sem Entropy
72.8
72.4
71.2
69.1
Answer-level
Verb
88.6
88.1
87.3
87.7
Verb
Topk
87.6
82.4
75.1
72.4
Consistency
64.9
63.9
62.9
61.2
Consis-Verb
54.1
52.7
51.8
50.5
Consis-Verb-Topk
48.1
45.9
44.7
42.2
Perplexity
85.9
85.7
85.5
85.0
Double-turn
P
True
-Consis
69.4
76.2
78.2
78.4
P
True
-Prob
69.5
76.2
78.3
78.5
P
True
-Consis-Cand
74.9
78.7
81.0
81.9
P
True
-Prob-Cand
74.9
78.7
81.1
81.9
Self
Ask
72.8
72.5
70.7
72.4
Self
Ask
-Cand
73.2
75.2
75.6
76.1
Table 11:
Confidence scores of
Qwen2.5-72B-Instruct
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Prob Entropy
76.4
75.4
74.3
73.4
N-Prob Entropy
94.1
93.9
93.5
93.3
Sem Entropy
71.8
70.3
68.3
66.6
Answer-level
Verb
87.9
87.3
86.2
86.8
Verb
Topk
85.9
79.5
70.8
69.9
Consistency
65.4
64.2
61.5
59.8
Consis-Verb
59.0
58.2
55.5
53.7
Consis-Verb-Topk
53.2
52.8
48.1
45.0
Perplexity
87.7
87.2
86.2
85.5
Double-turn
P
True
-Consis
75.1
73.3
68.6
73.7
P
True
-Prob
75.2
73.3
68.8
73.9
P
True
-Consis-Cand
75.8
76.0
73.4
77.6
P
True
-Prob-Cand
75.8
76.1
73.5
77.7
Self
Ask
84.9
79.7
72.9
75.3
Self
Ask
-Cand
83.5
81.8
76.6
79.5
Table 12:
Confidence scores of
LLaMA-3.1-8B-Instruct
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Prob Entropy
63.4
62.5
60.6
59.5
N-Prob Entropy
89.7
89.3
88.8
88.6
Sem Entropy
49.9
51.4
47.5
45.1
Answer-level
Verb
96.2
96.1
96.2
96.2
Verb
Topk
95.8
96.3
96.2
96.3
Consistency
36.0
36.8
32.7
30.4
Consis-Verb
37.1
37.0
33.5
30.7
Consis-Verb-Topk
30.4
29.8
26.9
24.6
Perplexity
67.0
67.6
65.9
64.4
Double-turn
P
True
-Consis
53.3
50.8
46.2
45.9
P
True
-Prob
53.1
50.9
46.4
45.7
P
True
-Consis-Cand
64.8
65.7
66.1
65.7
P
True
-Prob-Cand
64.7
65.7
65.9
65.9
Self
Ask
37.7
31.7
26.8
27.2
Self
Ask
-Cand
45.4
47.8
46.3
46.1
Table 13:
Confidence scores of
GPT-4o-mini
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Sem Entropy
49.6
50.1
46.2
44.9
Answer-level
Verb
93.2
92.1
91.1
90.8
Verb
Topk
83.7
73.0
61.5
56.5
Consistency
60.1
60.3
57.6
56.5
Consis-Verb
54.1
54.3
51.2
50.2
Consis-Verb-Topk
48.7
46.3
42.4
41.1
Double-turn
P
True
-Consis
62.5
67.7
68.3
70.5
P
True
-Consis-Cand
72.3
77.0
77.6
79.1
Self
Ask
76.3
76.1
73.7
74.9
Self
Ask
-Cand
73.7
76.4
76.9
76.6
Table 14:
Confidence scores of
GPT-4o
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Sem Entropy
63.0
54.1
45.4
40.4
Answer-level
Verb
92.1
90.7
88.8
88.5
Verb
Topk
89.6
85.6
71.8
67.4
Consistency
70.1
64.3
56.5
52.6
Consis-Verb
68.8
62.8
54.8
50.6
Consis-Verb-Topk
65.1
58.5
48.8
45.8
Double-turn
P
True
-Consis
64.3
66.8
68.4
70.4
P
True
-Consis-Cand
80.0
81.0
80.5
80.0
Self
Ask
77.8
75.8
74.9
75.3
Self
Ask
-Cand
80.5
80.4
79.0
77.9
Table 15:
Confidence scores of
DeepSeek-V3
under different ground truth(GT) set sizes.
Method
1a
2a
4a
6a
Single-turn
Question-level
Sem Entropy
80.9
78.6
76.2
72.9
Answer-level
Verb
85.3
85.5
85.8
86.0
Verb
Topk
63.5
57.5
52.7
50.5
Consistency
81.1
79.1
76.7
73.2
Consis-Verb
69.0
65.9
60.6
55.6
Consis-Verb-Topk
63.4
58.5
53.6
49.0
Double-turn
P
True
-Consis
64.3
64.6
64.7
66.2
P
True
-Consis-Cand
82.4
81.5
82.5
80.5
Self
Ask
76.5
72.8
69.8
71.2
Self
Ask
-Cand
83.8
81.3
80.8
78.7
Table 16:
AUROC score on Qwen-2.5-72B-Instruct
of different calibration methods under increasing answer mixture.
τ
=
0
\tau=0
denotes no-filtering, while
τ
≠
0
\tau\neq 0
uses the threshold value that achieves the best AUROC on the development set.
Bold
marks the best, and
underlined
the second-best, in each column.
Method
[1]
[1,2]
[1,2,4]
[1,2,4,6]
Single-turn
Question-level
Prob Entropy
82.4
79.1
78.4
77.5
N-Prob Entropy
81.8
78.4
77.0
76.2
Sem Entropy
77.3
75.6
75.1
73.9
Answer-level
Verb
64.3
60.6
58.5
57.4
Verb-Topk
67.7
64.1
59.9
57.7
Consis
78.2
77.1
76.7
75.8
Consis-Verb
77.5
75.8
75.4
74.1
Consis-Verb-Topk
75.1
73.3
72.3
71.0
Perplexity
82.0
79.9
78.5
77.4
Double-turn
P
True
-Consis
73.7
70.0
69.4
69.6
P
True
-Prob
81.3
77.2
76.2
76.3
P
True
-Consis-Cand
71.1
69.2
68.3
68.2
P
True
-Prob-Cand
81.5
77.5
75.8
75.6
Self-Ask
67.1
64.1
62.1
61.6
Self-Ask-Cand
74.4
70.6
67.2
66.0
Confidence Aggregation Baselines
SNCA (
τ
=
0.2
\tau=0.2
)
76.5
74.9
73.6
72.0
SNCA (
τ
=
0
\tau=0
)
50.0
50.0
50.0
50.0
SFCA (
τ
=
0.2
\tau=0.2
)
76.4
75.2
74.2
73.4
SFCA (
τ
=
0
\tau=0
)
50.0
50.0
50.0
50.0
Ours
SCA (
τ
=
0.3
\tau=0.3
)
82.0
80.3
79.5
78.4
SCA (
τ
=
0
\tau=0
)
82.0
80.4
79.5
78.4
C.2
Analysis of Cluster Probability Distribution
To obtain a reliable measure of the
effective
answer space, it is important to examine how probability mass is distributed across semantic clusters formed from multiple sampled responses.
Our statistical analysis of cluster probabilities shows that over
70%
of clusters lie within the 0–0.1 range, indicating that most clusters carry only negligible probability mass and predominantly represent spurious or semantically irrelevant outputs.
In contrast, a small number of clusters receive substantially higher mass and represent the dominant semantic modes of the model’s response distribution.
Because each cluster’s probability is defined as the
sum of absolute probabilities
of its member responses, applying a threshold effectively filters out clusters whose cumulative probability is intrinsically small. In other words, clusters with
P
​
(
C
m
)
<
τ
P(C_{m})<\tau
contribute only negligible absolute probability mass and primarily reflect sampling noise rather than meaningful alternative answers.
Motivated by the empirical distribution, we retain only clusters whose cumulative probability satisfies
P
​
(
C
m
)
≥
0.1
.
P(C_{m})\geq 0.1.
This value serves as a natural dividing point between the large concentration of near-zero clusters and the smaller set of semantically coherent ones.
Across domains and models, clusters above this threshold consistently exhibit stable semantics, while those below it are dominated by fragmented or degenerate responses.
Applying this threshold yields a more faithful estimate of the
effective
answer space and provides a clearer view of how semantic dispersion influences confidence.
Table 17:
Spearman correlation of confidence with knowledge coverage
across ground-truth(GT) set sizes.
Model
1a
2a
4a
6a
Qwen2.5-7B
0.009
-0.000
-0.000
-0.012
Qwen2.5-14B
-0.443
-0.438
-0.427
-0.421
Qwen2.5-32B
-0.421
-0.421
-0.407
-0.399
Qwen2.5-72B
-0.616
-0.551
-0.533
-0.516
Llama-3.1-8B
0.242
0.227
0.325
0.366
Llama-3.1-70B
-0.393
-0.314
-0.167
-0.055
GPT-4o-mini
-0.590
-0.563
-0.567
-0.544
GPT-4o
-0.821
-0.779
-0.729
-0.684
DeepSeek-V3
-0.854
-0.827
-0.820
-0.807
C.3
Spearman Validity Across Knowledge Coverage
To assess the reliability of the Spearman correlation between model confidence and answer space size,
we first analyze how the distribution of semantic clusters changes across different ground-truth cardinalities (1a, 2a, 4a, 6a).
As shown in Figure.
6
, all GT settings exhibit a smooth distribution, with no domination by a small number of cluster sizes.
For 1a, the majority of clusters are of size 1–3, with a light tail. As GT increases to 2, 4, and 6, the distribution shifts toward larger cluster sizes, remaining well-dispersed without skewing toward any particular cluster size.
This consistent shift suggests that the answer space expands in a stable and balanced manner:
higher GT increases the space without collapsing it into a narrow mode or generating extreme outliers that might bias rank-based correlation measures.
Because cluster frequencies remain diverse and avoid dominance effects, the Spearman correlation is not artificially skewed by outlier cluster sizes.
Results in Table
17
show the Spearman correlation between confidence and knowledge coverage. We find a notable negative correlation between these two metrics across multiple models, suggesting that higher confidence does not necessarily align with broader knowledge coverage.
Appendix D
Semantic Confidence Aggregation
D.1
Generalization Across Models
To evaluate the generalization capability of our methods, we extend our experiments to the
Qwen-2.5-72B-Instruct
model. As reported in Table
16
, our methods consistently achieve superior performance on this alternative architecture. This consistent improvement demonstrates that SCA is robust and model-agnostic, maintaining its effectiveness across different large language models.
Table 18:
ECE score on LLaMA-3.1-70B-Instruct
of different calibration methods under increasing answer mixture.
Bold
marks the best (lowest), and
underlined
the second-best, in each column.
Method
[1]
[1,2]
[1,2,4]
[1,2,4,6]
Single-turn
Question-level
Prob Entropy
26.2
21.7
20.8
19.4
N-Prob Entropy
43.5
35.5
31.7
30.3
Sem Entropy
12.5
9.6
16.6
21.3
Answer-level
Verb
46.8
39.5
34.6
33.1
Verb
Topk
35.8
22.5
19.3
21.9
Consistency
8.6
10.4
21.6
27.0
Consis-Verb
11.7
12.3
21.5
27.1
Consis-Verb-Topk
12.4
14.3
23.6
29.1
Perplexity
30.6
23.4
20.9
19.6
Double-turn
P
True
-Consis
35.3
34.1
33.0
31.5
P
True
-Prob
35.1
33.7
32.7
31.4
P
True
-Consis-Cand
41.7
35.6
30.4
30.6
P
True
-Prob-Cand
41.6
35.4
30.2
30.0
Self
Ask
36.6
40.9
45.8
46.7
Self
Ask
-Cand
26.3
22.8
23.5
25.6