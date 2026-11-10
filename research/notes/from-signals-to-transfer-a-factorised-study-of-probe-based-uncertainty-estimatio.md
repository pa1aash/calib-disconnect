---
title: 'From Signals to Transfer: A Factorised Study of Probe-Based Uncertainty Estimation
  in Large Language Models'
id: from-signals-to-transfer-a-factorised-study-of-probe-based-uncertainty-estimatio
tags:
- code-llm-confidence-positioning-d82d00
- w3-4
- l2-adjacent
created: '2026-11-10T08:24:01.732313Z'
updated: '2026-11-10T08:25:03.195569Z'
source: https://arxiv.org/html/2606.27679
source_domain: arxiv.org
fetched_at: '2026-11-10T08:24:01.731710Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Srey et al, arXiv 2606.27679v2, full text. Factorised study of probe-based
  uncertainty estimation (feature design, label construction, prompting, distribution
  shift) on 5 instruct LLMs (Llama-3.1-8B, Qwen3-4B/8B, Qwen3.5-9B, Gemma-3-12B) using
  TriviaQA-style factual generation; hidden states/attention hard to beat in-domain,
  structured features more robust under shift. No code generation, no execution labels.
  Bears on L2 probe methodology (matched-conditions design) in factual QA only.
---

From Signals to Transfer: A Factorised Study of Probe-Based Uncertainty Estimation in Large Language Models
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2606.27679v2 [cs.CL] 15 Oct 2026
From Signals to Transfer: A Factorised Study of Probe-Based Uncertainty Estimation in Large Language Models
Ponhvoan Srey
Affiliation:
Nanyang Technological University
Email:
ponhvoan002@ntu.edu.sg
Xiaobao Wu
†
†
thanks:
Corresponding Authors.
Affiliation:
Shanghai Jiao Tong University
Email:
vuducanh001@ntu.edu.sg
Cong-Duy Nguyen
Affiliation:
VinUniversity
Email:
anhtuan.luu@ntu.edu.sg
Quang Minh Nguyen
Affiliation:
KAIST
Email:
xiaobaowu@sjtu.edu.cn
Duc Anh Vu
Affiliation:
Nanyang Technological University
Email:
duy.ntc@vinuni.edu.vn
Anh Tuan Luu
1
1
footnotemark:
1
Affiliation:
Nanyang Technological University
Affiliation:
VinUniversity
Email:
qm.nguyen@kaist.ac.kr
Abstract
Probe-based uncertainty estimation (UE) has emerged as a prominent approach to detect hallucinations in Large Language Models (LLMs) by learning uncertainty from internal model signals. Yet, recent methods vary simultaneously across feature design, training data construction, and evaluation setting, obscuring what actually drives performance.
To address this issue, we propose a factorised study of probe-based UE under matched conditions.
Our results show that raw hidden states and attention features are difficult to outperform in-domain.
However, under distribution shift, structured and compressed features are more robust, suggesting that in-domain performance alone is insufficient to measure progress.
Furthermore, prompting and label construction significantly affect probe behaviour.
Building on these empirical design principles, we construct benchmark-pretrained probes that retain useful discriminative signal on open-ended factual generation. Their competitive performance relative to limited-label target setting probes and sampling-based estimators suggests that they can provide a practical starting point for subsequent target-domain adaptation.
More broadly, our work encourages deployment-oriented evaluation of probe-based uncertainty estimators
2
2
2
The code repository is available at
https://github.com/ponhvoan/ProbeUE
.
.
1
Introduction
Hallucination in Large Language Models (LLMs), the tendency to generate fictitious information, remains a persistent barrier to reliable deployment in real-world applications
(
Sahoo et al., 2024
;
Huang et al., 2025a
;
Zhang et al., 2025b
)
. This necessitates the development of robust uncertainty estimation (UE) to accurately flag potentially erroneous generations for users
(
Vashurin et al., 2025
)
. Recent work suggests that probe-based UE, which leverages internal model states, provides some of the most effective signals for hallucination detection
(
Mahaut et al., 2024
;
Tan et al., 2025
)
.
This has led to a growing body of work that engineers progressively more structured and informative internal features and integrates them into more sophisticated optimisation protocols
(
Chuang et al., 2024
;
He et al., 2024
;
Vazhentsev et al., 2025
;
Shelmanov et al., 2025
)
.
However, despite this progress, two questions remain unresolved: what accounts for the gains reported, and whether these gains translate beyond matched benchmark settings.
First, current evaluations conflate multiple design choices, such as training data acquisition, feature representation, supervision, and probe architecture, making it unclear what actually accounts for the observed gains. This motivates our first central research question:
What truly drives performance in probe-based uncertainty estimation?
At the same time, a critical bottleneck of probe-based UE is limited generalisability.
Even though probes are highly effective under matched train-test conditions, their performance often degrades when applied to new domains or generation settings
(
CH-Wang et al., 2024
;
Chuang et al., 2024
)
.
This limits their utility in real use cases, where uncertainty estimators must handle open-ended generations, rather than only the benchmark format on which they were trained.
Although some prior work evaluates transfer across datasets, such evaluations are restricted to benchmark-to-benchmark transfer
(
Chuang et al., 2024
)
, or remain within comparable long-form and claim-level generation setups
(
Han et al., 2025
;
Shelmanov et al., 2025
)
.
In these settings, probes are tested under distribution shift, but the generation format, answer structure, supervision signal, and evaluation protocol remain relatively constrained.
This leaves open whether probes can generalise to less standardised target settings, where outputs are open-ended, vary significantly in length and style, and contain more diverse factual errors.
Such a setting is practically motivated because target-specific probes require costly construction and annotation of in-domain long-form data, whereas benchmark-pretrained probes provide an immediate baseline that can be adapted with target-domain labels.
This formulates our second research question:
Can probes trained under controlled benchmark settings retain useful factuality signal when transferred to open-ended long-form generation tasks?
To answer these questions, we conduct a controlled study of probe-based UE across three primary dimensions: feature representations, training data construction, and transfer settings.
Our study covers a wide range of recently proposed feature representations, spanning latent embeddings, output probabilities, attention patterns, and their combinations
(
Azaria and Mitchell, 2023
;
Chuang et al., 2024
;
He et al., 2024
;
Huang et al., 2025b
;
Shelmanov et al., 2025
)
, evaluated with different probe architectures, supervision sizes, prompting strategies, and automated correctness labels.
We further study benchmark-to-benchmark transfer and a deployment-oriented setting in which probes pretrained on benchmark data are applied to open-ended long-form factual generation.
Together, these allow us to identify which design choices drive in-domain performance, which remain robust under shift, and which design principles support reusable pretrained factuality probes.
Our findings challenge several common assumptions.
First, simple linear probes over raw hidden states and attention features are surprisingly difficult to outperform, even with limited supervision.
Second, data construction choices strongly shape probe behaviour: reasoning-eliciting prompts and lexical matching-based labels can often degrade probe discriminability.
Finally, structured and compressed features offer better trade-offs under distribution shift.
These findings yield a practical recipe: use simple probe architectures, concise generations with semantic correctness labels, and transfer-robust feature representations.
Building on these recommendations, we show that structured benchmark-pretrained probes can remain competitive with limited-label target setting probes and training-free estimators, including expensive sampling-based methods, under open-ended transfer, although performance varies across settings.
Collectively, our work pushes probe-based UE beyond in-domain benchmark comparison toward deployment-oriented practice. Rather than pursuing increasingly complex internal state representation features in isolation, the field should prioritise simple and transferable probe configurations that maintain reliability beyond benchmarks. In summary, our contributions are threefold:
•
We propose a factorised evaluation framework to disentangle the design factors behind probe-based UE performance.
•
We identify empirical design recommendations to train lightweight uncertainty probes under different constraints.
•
We stress test probes pretrained with these practices under benchmark-to-open-ended transfer, characterising when reusable uncertainty signals persist.
(a)
Average AUROC (
↑
\uparrow
)
(b)
Average ECE (
↓
\downarrow
)
Figure 1:
Main results: In-domain performance averaged over all benchmarks and ranked by mean (rightmost).
2
Related Work
In this section, we outline key research threads related to our work. For a more detailed review, please refer to
Appendix
A
.
Probe-based Uncertainty Estimation (UE)
trains lightweight probes on top of LLM internal signals to predict response correctness or, conversely, hallucination risk. Early work shows that truth-related information is linearly accessible from final-layer hidden states
(
Azaria and Mitchell, 2023
;
Burns et al., 2022
;
Marks and Tegmark, 2023
)
. Subsequent methods use richer representations, including all-layer or token-sequence hidden states
(
CH-Wang et al., 2024
;
Shelmanov et al., 2025
;
Zhu et al., 2024
)
, hidden-state geometry and density
(
Srey et al., 2026b
;
Vazhentsev et al., 2025
;
Wang et al., 2025b
)
, attention patterns
(
Chuang et al., 2024
)
, intermediate-layer and output probabilities
(
Huang et al., 2025b
;
He et al., 2024
)
, and a combination of these signals
(
He et al., 2024
;
Shelmanov et al., 2025
)
. However, these approaches frequently vary feature representations, data construction, prompting, probe architecture, and evaluation setting simultaneously, obscuring which choices account for their gains.
Benchmarking and Evaluation.
LM-Polygraph
(
Fadeeva et al., 2023
)
and a follow-up benchmarking work
(
Vashurin et al., 2025
)
standardise the comparison of diverse UE methods across tasks, while other work examines robustness to input or dataset shifts
(
Mahaut et al., 2024
;
Wang et al., 2025a
)
.
Han et al. (2025)
establish that linear hidden-states probes can detect factual errors in long-form generation effectively. Similarly,
Shelmanov et al. (2025)
investigated long-form tasks with more sophisticated pretrained uncertainty heads.
Separately,
Janiak et al. (2025)
show that lexical correctness metrics can substantially misrepresent hallucination detection performance.
Likewise,
Santilli et al. (2025)
corroborate this finding, and additionally, include supervised final-token probes. We further test how broadly this phenomenon extends across substantially more diverse probe representations.
Positioning of Our Study.
Our contribution is a unifying, probe-specific factorisation under matched conditions. In
Section
3
, we jointly vary feature representation, probe architecture, supervision size, prompting, annotation, and transfer setting to identify robust design practices under different constraints.
In
Section
4
, we then stress test whether these practices support probes pretrained only on short-form benchmarks and deployed off-the-shelf on atomic claims from open-ended long-form generations.
Unlike prior long-form probing work, this setting introduces simultaneous shifts in task, response format, domain, and annotation granularity.
Our work therefore provides a controlled account of what makes probe-based UE work, where it fails, and which design choices better support benchmark-to-open-ended transfer.
3
What Drives Probe Performance?
In this section, we answer our first research question:
What truly drives performance in probe-based uncertainty estimation?
To this end, we perform a factorised analysis by varying important design choices, namely feature representation, probe architecture, and supervision budget (
Section
3.2
), and training data and annotation construction (
Section
3.3
). We then scrutinise a benchmark-to-benchmark transfer setting (
Section
3.4
), where training and test data differ, but they are both derived from the benchmark pool.
We find that
(i)
raw hidden state and attention features are strong in-domain, even with simple linear probes and limited supervision;
(ii)
response elicitation and ground truth annotation strategy choices can substantially affect probe quality; and
(iii)
structured features are more robust under transfer.
3.1
Experimental Setup
Datasets.
We evaluate on seven datasets spanning three response-format groups:
(i)
Question Answering (QA):
we use TriviaQA
(
Joshi et al., 2017
)
, SciQ
(
Welbl et al., 2017
)
, and PopQA
(
Mallen et al., 2023
)
as fact-heavy short-answer QA datasets, encompassing general trivia, science knowledge, and long-tail entity knowledge, respectively;
(ii)
Verification
: we include BoolQ
(
Clark et al., 2019
)
and StrategyQA
(
Geva et al., 2021
)
as factual and logical verification tasks that often require understanding and implicit reasoning;
(iii)
Multiple-Choice Questions (MCQ)
: we use CommonsenseQA
(
Talmor et al., 2019
, CSQA;)
and ARC
(
Clark et al., 2018
)
.
These datasets cover diverse topics, answer formats, and reasoning demands.
For compactness, we refer to these response-format groups as tasks when describing within- and cross-group transfer below.
We present our prompts in
Section
B.4
.
To obtain correctness labels of LLM generations for the QA datasets, we utilise Gemini-3.1-Flash-Lite
(
Google DeepMind, 2026
)
as the default LLM-as-a-judge ground truth annotator.
We discuss the effects of different annotation strategies in
Section
3.3
.
Language Models.
For the main experiment, we evaluate with five popular LLMs across three model families: Llama-3.1-8B
(
Grattafiori et al., 2024
)
, Qwen-3-4B, Qwen-3-8B
(
Yang et al., 2025
)
, Qwen-3.5-9B
(
Qwen Team, 2026
)
, Gemma-3-12B-Instruct
(
Kamath et al., 2025
)
. We use instruction-tuned versions of all models except for Qwen-3-8B as its official implementation is unavailable.
Llama and Qwen-3-4B are deferred to
Appendix
C
for better readability.
Evaluation Metrics.
To evaluate our results, we report two complementary metrics that capture key desiderata of uncertainty estimation:
(i)
Area Under the Receiver-Operating characteristics Curve
(
Davis and Goadrich, 2006
, AUROC;)
, which measures discriminability, or the probe’s ability to separate correct responses from incorrect ones, with
1.0
1.0
indicating perfect discrimination and
0.5
0.5
no better than chance; and
(ii)
Expected Calibration Error
(
Guo et al., 2017
, ECE;)
, which measures calibration,
i.e.
how closely the predicted probabilities align with real-world outcomes, with
0.0
0.0
indicating perfect calibration. We follow the standard implementation with 10 equal-width bins.
Given the imbalanced dataset, with considerably fewer positive (hallucinated) instances, we additionally report Area Under the Precision-Recall curve (AUPR) in
Appendix
C
.
Feature Representations.
For each query, we run greedy decoding and extract 19 feature representations from the LLM’s internal generation trace, grouped into four information levels. First, we use hidden state representation summaries:
Embedding (last)
,
Embedding (mean)
, and
Embedding (all)
(
Azaria and Mitchell, 2023
;
Su et al., 2024
)
; trajectory-based
CoE-R
and
CoE-C
(
Wang et al., 2025b
)
; dispersion-based
Circular Variance
and
Cov. Determinant
(
Srey et al., 2026b
)
; and density-based
SATMD
(
Vazhentsev et al., 2025
)
.
Second, probability features capture output-side uncertainty:
Max. Seq. Prob. (MSP)
,
Entropy
,
Perplexity
(
Huang et al., 2025b
)
,
Energy
(
Liu et al., 2020
)
,
Top-
m
m
Prob.
(
He et al., 2024
)
, with
m
=
10
m=10
as default.
Third, we include attention features that reflect attention allocation between input and generated tokens, namely recent-token
Attention
(
Shelmanov et al., 2025
)
, and
Lookback Ratio
(
Chuang et al., 2024
)
.
Finally, combined features concatenate complementary signals into
Layer Top-
m
m
Prob
(
He et al., 2024
)
,
Attention + MSP
,
Internal Variance
, and
SATMD + MSP
.
We provide more details on feature representation in
Section
B.1
.
Probe Training.
We train lightweight binary probes on top of each feature representation to predict response correctness. Our default is a linear probe, and we evaluate two non-linear variants (see
Section
3.2
): an MLP probe with one ReLU-activated hidden layer, and a CNN that applies 1D convolutions over the flattened feature vector before pooling and classification.
We adopt the binary cross-entropy loss, optimised using Adam, with feature normalisation and early stopping based on validation AUROC.
We include training details in
Section
B.3
.
3.2
Simple Features Are Difficult to Outperform
Figure 2:
Effect of probe architecture on AUROC.
Simple Signals Win.
Under a fixed linear-probe setting, more complex feature engineering does not consistently improve in-domain uncertainty estimation.
As shown in
Figures
1
and
8
, simple features, referring to relatively direct representations which do not require fitted density models or substantial geometric transformations, namely Embedding (mean), Embedding (last), Lookback Ratio, and Attention, are consistently competitive across all models, with Lookback Ratio standing out for its smaller input dimension.
Additionally, in line with previous findings, concatenating embeddings from all layers does not always improve performance
(
Chuang et al., 2024
;
Su et al., 2024
)
. In contrast, augmenting hidden state features with logit-based signals, such as MSP and Entropy, or vice versa for Top-
m
m
Prob.,
does
reliably increase discriminability, suggesting that fusing complementary signal types is more useful than simply adding more of the same type of internal features.
Linear Probes Are Stable.
We further test whether stronger probe architectures would affect feature ranking using Qwen-3-8B.
Figure
2
shows that MLP and CNN probes can improve weaker feature representations, especially low-dimensional and scalar features,
e.g.
Internal Variance and Energy, but bring limited gains for strong hidden state and attention-based signals.
We observe a similar trend in calibration (
Figure
14
). However, under the transfer setting (see
Figure
13
), higher-capacity probes generally worsen performance, suggesting that they may capture dataset-specific patterns that hurt generalisation. Thus, probe complexity is not uniformly beneficial: once feature representation is sufficiently informative, linear probes are often competitive and more stable.
Figure 3:
Dependence on number of training examples.
Limited Supervision Is Sufficient.
Next, we vary the number of labelled training examples to determine how much supervision is required.
Figure
3
visualises AUROC for a strong set of Qwen-3-8B features. Performance steadily improves with more labelled data, but satisfactory performance is recovered with relatively few labels, with average AUROC reaching a useful threshold at around 128-256 examples.
Informative representations like Embeddings (last) perform well with few examples and gains beyond 128–256 examples are modest.
Overall, these results suggest that factuality information is largely linearly accessible in the hidden states even with limited supervision.
The main benefit of recent feature engineering may therefore not be stronger in-domain discrimination, but better performance under other constraints, such as calibration and transfer. For instance, ECE results in
Figure
1
show that internal variance is relatively well-calibrated despite lower AUROC.
This motivates our further examination in transfer tasks rather than treating in-domain AUROC as the sole indicator of progress.
3.3
Data Construction Strongly Shapes Performance
To obtain training data, there are two crucial design choices: prompting, which directly affects the internal states, and the ground truth annotation strategy.
Figure 4:
Impact of various automated annotation options on probe performance.
Figure 5:
Benchmark-transfer performance. Average AUROC across In-domain, Out-of-domain (same task), and Out-of-domain (cross task) configurations. Methods are ranked by out-of-domain (cross task) performance.
Reasoning-Eliciting Prompts Can Reduce Probe Discriminability.
We compare no-, medium-, and long-reasoning prompts (
Table
3
) on ARC and CSQA using Qwen-3-8B (
Figure
16
) and Gemma-3-12B-Instruct (
Figure
18
).
Although reasoning elicitation does not reduce answer accuracy, it can substantially alter probe discriminability. Across both models, the constrained medium-reasoning condition is generally weakest, whereas long reasoning partially restores performance and occasionally matches or exceeds direct answering. We hypothesise that one-sentence explanations introduce relatively stereotyped tokens without adding much correctness-specific information, whereas longer traces contain richer task-relevant content. However, longer traces also shift the answer position and, for sequence-aggregated features, may dilute relevant information, potentially explaining why they may often remain below direct answering.
We replicate these experiments on StrategyQA and MATH-500
(
Lightman et al., 2024
)
(
Figure
17
). We observe similar prompt sensitivity trends except when reasoning improves both answer accuracy and probe discriminability in tandem (Gemma on MATH-500).
We present more reasoning-control analysis in
Appendix
C
.
Therefore, we recommend direct answering as a stable and computationally efficient default, while emphasising that the effect is feature- and model-dependent.
Ground Truth Annotation Matters.
We study how the choice of correctness annotation affects probe evaluation.
Because obtaining human annotations at scale is costly, we resort to automated scorers, a common practice in the field
(
Duan et al., 2024
;
Janiak et al., 2025
;
Kuhn et al., 2023
;
Vazhentsev et al., 2025
)
.
Specifically, we examine three types of labelling strategies on TriviaQA, SciQ, and PopQA with Qwen-3-8B: Rouge
(
Lin, 2004
)
, AlignScore
(
Zha et al., 2023
)
, and LLM-as-a-judge with Gemini-3.1-Flash-Lite.
We present the detailed validation procedure in
Appendix
C
.
In
Figure
4
, we investigate the effect of varying the labelling choice for the training data.
We find that LLM-as-a-judge labels consistently yield the highest AUROC.
These results caution against relying on lexical metrics to obtain ground truth labels, and instead advocate for LLM-as-a-judge labelling, which better captures semantic correctness.
3.4
Structured Features Are More Robust Under Transfer
For benchmark transfer, we report average performance for Qwen-3-8B (
Figure
5
) and Gemma-3-12B-Instruct (
Figure
9
) across the three groups: QA, Verification, and MCQ. Further, we distinguish between in-domain, out-of-domain (OOD) (same task), and OOD (cross task) performance. By OOD (same task), we mean testing on a different dataset from the same task,
e.g.
TriviaQA
→
\rightarrow
SciQ, and OOD (cross task) refers to all remaining OOD train-test configurations.
On average, there is a clear gap between in-domain and transfer performance, especially across tasks. This confirms that probes are brittle, and strong in-domain performance alone is not sufficient evidence they will be useful in deployment.
The in-domain advantage of raw hidden state and attention features, narrows considerably as they may encode task-specific biases that inhibit generalisation.
In comparison, several structured probability and dispersion features, such as Internal Variance and Top-
m
m
Prob., retain more of their performance under same task and cross task transfer. As a practical takeaway, pretrained probes should not be selected solely by in-domain performance, but also, by robustness to dataset shift.
4
Stress-Testing Benchmark-Pretrained Probes on Open-Ended Generation
In this section, we answer our second research question:
Can probes trained under controlled benchmark settings retain useful factuality signal when transferred to open-ended generation tasks?
We compare benchmark-pretrained probes against feature-matched probes trained with limited target setting supervision, as well as training-free and sampling baselines.
We find that structured benchmark-pretrained probes retain useful factuality signal under this substantial distribution shift, motivating their use as an immediate baseline when target-domain labels are unavailable.
4.1
Experimental Setup
Evaluation Data and Models.
We sample 100 entities from the dataset used in
(
Min et al., 2023
)
, and 50 from each domain in
(
Shelmanov et al., 2025
)
. In total, we have 500 entities spanning nine domains:
Biographies (in-domain; ID)
,
Biographies (OOD)
,
Artworks
,
Books
,
Cities
,
Events
,
Inventions
,
Landmarks
,
Movies
.
Using Qwen-3-8B, Gemma-3-12B-Instruct, and Llama-3.1-8B, we use the same simple prompts as
Shelmanov et al. (2025)
to generate texts for each entity up to 512 tokens.
Similar to
Han et al. (2025)
, we utilise Gemini-3.1-Flash-Lite to automatically decompose the long-form continuation into atomic factual claims (see
Section
B.4
for complete instructions).
For each claim, we obtain the features and labels as in
Section
3
, but use GPT-5.4-Mini
(
OpenAI, 2026
)
for factuality annotation as it shows substantially higher agreement with human judgements on our validation subset (
Table
11
).
Thus, benchmark-pretrained probes additionally face this supervision-source shift as part of the intended benchmark-to-open-ended transfer setting.
This produces ~500–1,000 claim-label pairs per domain; we report the detailed statistics in
Table
7
.
Figure 6:
Mean OOD across the eight held-out domains. We compare representative Biographies-ID-trained, benchmark pretrained, and training-free estimators. Benchmark-pretrained structured probes are competitive overall, but their relative performance varies across models; we report full domain results in
Tables
12
,
13
and
14
.
Pretrained Probes.
We pretrain linear probes on features extracted from the pooled seven-benchmark dataset. Guided by findings in
Section
3
, we use direct-answer generation, LLM-judge labels, and representative transfer-oriented features: Lookback Ratio, Layer Top-
m
m
Prob., and Internal Variance, retaining Embedding (last) as a comparison.
Furthermore, we consider two simple ensembles:
Ensemble (probe), which averages from three Internal variance probes trained separately on QA, Verification, and MCQ; and
Ensemble (task), which averages predictions from probes trained on pooled data using the three features.
Biographies-ID-Trained and Training-Free Baselines.
To isolate the effect of benchmark pretraining from feature choice, we compare benchmark-pretrained probes against feature-matched linear probes trained on 256 claim–label pairs from Biographies (ID).
We refer to these as
Biographies-ID-trained
probes.
For Qwen-3-8B, we additionally report Embedding (last) probes under varying label budgets and probe architectures. We also include training-free logits- (MSP, Entropy, Perplexity, Energy) and sampling-based baselines (Semantic Entropy
(
Kuhn et al., 2023
)
, Eigenscore
(
Chen et al., 2024
)
) with five samples per query.
Surrogate-Model Features.
We additionally test whether probes require the generator’s own internal states. We pass generated claims through an accessible surrogate model and evaluate its pretrained probes. We report full results in
Appendix
C
.
4.2
Results and Discussion
Benchmark-Pretrained Probes Retain Useful Zero-Label Signal.
Figure
6
summarises the mean OOD results across models.
Structured benchmark-pretrained probes retain useful discriminative signal despite receiving no labels from the open-ended target domains.
Aggregated across OOD domains, the best benchmark-pretrained and training-free methods are broadly competitive, with no method class dominating consistently across models and domains.
Importantly, the benchmark-pretrained probes require only a single greedy generation trace, while sampling-based baselines use five samples per query. We therefore interpret the supported result as a practical and computationally efficient zero-target-label baseline.
Performance Varies Across Models and Domains.
The aggregate picture masks considerable heterogeneity.
Tables
12
,
13
and
14
provide full domain breakdown.
On Qwen, structured benchmark-pretrained probes are among the strongest methods on average, whereas on Gemma and Llama, training-free estimators are often equally strong or stronger. The relative ordering also varies across domains: a feature that transfers well to one domain can approach chance on another.
Furthermore, performance still remains modest with several feature–domain combinations approaching chance, indicating that transferable factuality signal can weaken or vanish under severe shift. Pretrained probes should therefore be viewed as reusable baselines rather than universally superior, deployment-ready detectors.
Toward Reusable Uncertainty Probes.
Taken together, these results support a modular view of probe-based UE: a broadly trained uncertainty head can offer a reasonable and immediate starting baseline.
Qualitative examples in
Table
17
illustrate this potential: pretrained structured probes successfully flag several hallucinated claims and assign high confidence to correct generations, while the included failure cases show that confident errors remain. A natural next step is to adapt such probes with limited target-domain supervision as deployment data become available.
The surrogate-model results further suggest that the uncertainty module need not share the generator’s architecture, opening a path toward factuality estimation for black-box LLMs.
5
Conclusion
In this work, we examine the influence of feature representation, training data construction, and transfer on probe-based UE. Our results indicate that raw features are surprisingly strong in-domain. However, under distribution shift, structured features are more robust, suggesting that in-domain discriminability alone is insufficient for assessing progress.
Based on these findings, we distil practical design recommendations to train probes on benchmark data. Even without task-specific supervision, these pretrained probes demonstrate reasonable performance when transferred to long-form open-ended factual generation, providing a useful off-the-shelf baseline. We hope this work encourages the field to move beyond matched benchmark comparison and towards probe configurations that remain useful under realistic distribution shifts. Future work can build on this direction by adapting pretrained probes, enabling stronger performance in deployment.
Limitations
Although our work has derived design recommendations to train uncertainty/factuality probes and has shown how these can support deployment-oriented open-ended generation, it has the following limitations:
Constrained Open-Ended Generation.
We simulate a more realistic setting by considering long-form generation involving an entity. However, there are many other uncovered use cases, such as unconstrained dialogue and multi-turn interaction. Thus, our conclusions about pretrained probe transfer should be interpreted as evidence for entity-centric factual generation, rather than a universal claim of robustness across all open-ended settings.
Model and Feature Coverage.
Our study covers a broad set of LLMs, probe features, and design factors, but it is not exhaustive. We focus on popular open-weight LLMs and internal signals.
In particular, we conduct our detailed analysis with base Qwen-3-8B and Gemma-3-12B-Instruct.
Future work can assess how broadly the observed best practices apply to larger instruction-tuned LLMs and other feature representations.
Hallucination Mitigation.
We focus on hallucination detection using probes. We leave probe-guided hallucination mitigation to future work. They can investigate whether the probe configurations identified here also support effective mitigation strategies.
Transfer Direction.
We study transfer from short-form QA benchmarks to open-ended factual
generation. This reflects our intended practical setting, where benchmark supervision is readily available, but target annotation can be costly. The reverse direction has not been studied and can additional limitations of supervised methods.
LLM-as-a-judge Labels.
In our experiments, we regard LLM annotations as ground truth labels. Human validation across multiple benchmark and open-ended domains show high,
but imperfect
, agreement with these annotations. Reported performance should therefore be interpreted as agreement with the chosen annotation protocol.
References
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
§A.1
,
Table 1
,
§1
,
§2
,
§3.1
.
Bouchard
et al.
(2026)
D. Bouchard, M. S. Chauhan, D. Skarbrevik, H. Ra, V. Bajaj, and Z. Ahmad
Uqlm: a python package for uncertainty quantification in large language models
.
Journal of Machine Learning Research
27
(
13
),
pp. 1–10
.
Cited by:
§A.2
.
Burns
et al.
(2022)
C. Burns, H. Ye, D. Klein, and J. Steinhardt
Discovering latent knowledge in language models without supervision
.
arXiv preprint arXiv:2212.03827
.
External Links:
Link
Cited by:
§A.1
,
§2
.
CH-Wang
et al.
(2024)
S. CH-Wang, B. Van Durme, J. Eisner, and C. Kedzie
Do androids know they’re only dreaming of electric sheep?
.
In
Findings of the Association for Computational Linguistics: ACL 2024
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 4401–4420
.
External Links:
Link
,
Document
Cited by:
§A.1
,
§A.2
,
§1
,
§2
.
Chen
et al.
(2024)
C. Chen, K. Liu, Z. Chen, Y. Gu, Y. Wu, M. Tao, Z. Fu, and J. Ye
INSIDE: LLMs’ internal states retain the power of hallucination detection
.
In
The Twelfth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§4.1
.
Chuang
et al.
(2024)
Y. Chuang, L. Qiu, C. Hsieh, R. Krishna, Y. Kim, and J. R. Glass
Lookback lens: detecting and mitigating contextual hallucinations in large language models using only attention maps
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 1419–1436
.
External Links:
Link
,
Document
Cited by:
§A.1
,
§A.2
,
§B.2
,
Table 1
,
§1
,
§1
,
§1
,
§2
,
§3.1
,
§3.2
.
Clark
et al.
(2019)
C. Clark, K. Lee, M. Chang, T. Kwiatkowski, M. Collins, and K. Toutanova
BoolQ: exploring the surprising difficulty of natural yes/no questions
.
In
Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)
,
J. Burstein, C. Doran, and T. Solorio (Eds.)
,
Minneapolis, Minnesota
,
pp. 2924–2936
.
External Links:
Link
,
Document
Cited by:
item ii
.
Clark
et al.
(2018)
P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord
Think you have solved question answering? try arc, the ai2 reasoning challenge
.
arXiv preprint arXiv:1803.05457
.
External Links:
Link
Cited by:
item iii
.
Davis and Goadrich (2006)
J. Davis and M. Goadrich
The relationship between precision-recall and roc curves
.
In
Proceedings of the 23rd international conference on Machine learning
,
pp. 233–240
.
External Links:
Link
Cited by:
item i
.
Duan
et al.
(2024)
J. Duan, H. Cheng, S. Wang, A. Zavalny, C. Wang, R. Xu, B. Kailkhura, and K. Xu
Shifting attention to relevance: towards the predictive uncertainty quantification of free-form large language models
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 5050–5063
.
External Links:
Link
,
Document
Cited by:
Appendix C
,
§3.3
.
Fadeeva
et al.
(2023)
E. Fadeeva, R. Vashurin, A. Tsvigun, A. Vazhentsev, S. Petrakov, K. Fedyanin, D. Vasilev, E. Goncharova, A. Panchenko, M. Panov, T. Baldwin, and A. Shelmanov
LM-polygraph: uncertainty estimation for language models
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations
,
Y. Feng and E. Lefever (Eds.)
,
Singapore
,
pp. 446–461
.
External Links:
Link
,
Document
Cited by:
§A.2
,
§2
.
Fu
et al.
(2025)
T. Fu, J. Conde, G. Martínez, M. Grandury, and P. Reviriego
Multiple choice questions: reasoning makes large language models (llms) more self-confident even when they are wrong
.
arXiv preprint arXiv:2501.09775
.
Cited by:
§A.3
.
Geva
et al.
(2021)
M. Geva, D. Khashabi, E. Segal, T. Khot, D. Roth, and J. Berant
Did aristotle use a laptop? a question answering benchmark with implicit reasoning strategies
.
Transactions of the Association for Computational Linguistics
9
,
pp. 346–361
.
External Links:
Link
,
Document
Cited by:
item ii
.
Google DeepMind (2026)
Google DeepMind
Gemini 3.1 flash-lite
.
Note:
https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite
Accessed: May 22, 2026
Cited by:
§3.1
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
External Links:
Link
Cited by:
§3.1
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
International conference on machine learning
,
pp. 1321–1330
.
External Links:
Link
Cited by:
item ii
.
Han
et al.
(2025)
J. Han, N. Band, M. Razzak, J. Kossen, T. G. J. Rudner, and Y. Gal
Simple factuality probes detect hallucinations in long-form natural language generation
.
In
Findings of the Association for Computational Linguistics: EMNLP 2025
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 16209–16226
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-335-7
Cited by:
§A.2
,
§B.4
,
§1
,
§2
,
§4.1
.
He
et al.
(2024)
J. He, Y. Gong, Z. Lin, C. Wei, Y. Zhao, and K. Chen
LLM factoscope: uncovering LLMs’ factual discernment through measuring inner states
.
In
Findings of the Association for Computational Linguistics: ACL 2024
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 10218–10230
.
External Links:
Link
,
Document
Cited by:
§A.1
,
Table 1
,
Table 1
,
§1
,
§1
,
§2
,
§3.1
.
Huang
et al.
(2025a)
L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin, and T. Liu
A survey on hallucination in large language models: principles, taxonomy, challenges, and open questions
.
ACM Trans. Inf. Syst.
43
(
2
).
External Links:
ISSN 1046-8188
,
Link
,
Document
Cited by:
§1
.
Huang
et al.
(2025b)
Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma
Look before you leap: an exploratory study of uncertainty analysis for large language models
.
IEEE Transactions on Software Engineering
51
(
2
),
pp. 413–429
.
External Links:
Link
Cited by:
Table 1
,
§1
,
§2
,
§3.1
.
Janiak
et al.
(2025)
D. Janiak, J. Binkowski, A. Sawczyn, B. Gabrys, R. Shwartz-Ziv, and T. J. Kajdanowicz
The illusion of progress: re-evaluating hallucination detection in LLMs
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 34728–34745
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§A.3
,
Appendix C
,
§2
,
§3.3
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
item i
.
Kamath
et al.
(2025)
A. Kamath, J. Ferret, S. Pathak, N. Vieillard, R. Merhej, S. Perrin, T. Matejovicova, A. Ramé, M. Rivière, L. Rouillard,
et al.
Gemma 3 technical report
.
arXiv preprint arXiv:2503.19786
4
.
External Links:
Link
Cited by:
§3.1
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
arXiv preprint arXiv:2302.09664
.
External Links:
Link
Cited by:
§3.3
,
§4.1
.
Lei
et al.
(2023)
D. Lei, Y. Li, M. Hu, M. Wang, V. Yun, E. Ching, and E. Kamal
Chain of natural language inference for reducing large language model ungrounded hallucinations
.
arXiv preprint arXiv:2310.03951
.
External Links:
Link
Cited by:
Appendix C
.
Li
et al.
(2025a)
K. Li, Y. Li, T. Zhang, H. Luo, X. Wu, J. R. Glass, and H. M. Meng
RAG-zeval: enhancing RAG responses evaluator through end-to-end reasoning and ranking-based reinforcement learning
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 24925–24943
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§B.4
.
Li
et al.
(2025b)
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
§A.1
.
Lightman
et al.
(2024)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
Let’s verify step by step
.
In
International Conference on Learning Representations
,
Vol.
2024
,
pp. 39578–39601
.
Cited by:
§3.3
.
Lin (2004)
C. Lin
ROUGE: a package for automatic evaluation of summaries
.
In
Text Summarization Branches Out
,
Barcelona, Spain
,
pp. 74–81
.
External Links:
Link
Cited by:
§A.3
,
§3.3
.
Liu
et al.
(2020)
W. Liu, X. Wang, J. Owens, and Y. Li
Energy-based out-of-distribution detection
.
Advances in neural information processing systems
33
,
pp. 21464–21475
.
External Links:
Link
Cited by:
Table 1
,
§3.1
.
Mahaut
et al.
(2024)
M. Mahaut, L. Aina, P. Czarnowska, M. Hardalov, T. Müller, and L. Marquez
Factual confidence of LLMs: on reliability and robustness of current estimators
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 4554–4570
.
External Links:
Link
,
Document
Cited by:
§A.2
,
§1
,
§2
.
Mallen
et al.
(2023)
A. Mallen, A. Asai, V. Zhong, R. Das, D. Khashabi, and H. Hajishirzi
When not to trust language models: investigating effectiveness of parametric and non-parametric memories
.
In
Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
A. Rogers, J. Boyd-Graber, and N. Okazaki (Eds.)
,
Toronto, Canada
,
pp. 9802–9822
.
External Links:
Link
,
Document
Cited by:
item i
.
Marks and Tegmark (2023)
S. Marks and M. Tegmark
The geometry of truth: emergent linear structure in large language model representations of true/false datasets
.
arXiv preprint arXiv:2310.06824
.
External Links:
Link
Cited by:
§A.1
,
§2
.
Mei
et al.
(2026)
Z. Mei, C. Zhang, T. Yin, J. Lidard, O. Sho, and A. Majumdar
Reasoning about uncertainty: do reasoning models know when they don’t know?
.
In
Findings of the Association for Computational Linguistics: EACL 2026
,
V. Demberg, K. Inui, and L. Marquez (Eds.)
,
Rabat, Morocco
,
pp. 3408–3458
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-386-9
Cited by:
§A.3
.
Min
et al.
(2023)
S. Min, K. Krishna, X. Lyu, M. Lewis, W. Yih, P. Koh, M. Iyyer, L. Zettlemoyer, and H. Hajishirzi
FActScore: fine-grained atomic evaluation of factual precision in long form text generation
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
H. Bouamor, J. Pino, and K. Bali (Eds.)
,
Singapore
.
Cited by:
§B.4
,
§4.1
.
Obeso
et al.
(2025)
O. Obeso, A. Arditi, J. Ferrando, J. Freeman, C. Holmes, and N. Nanda
Real-time detection of hallucinated entities in long-form generation
.
arXiv preprint arXiv:2509.03531
.
External Links:
Link
Cited by:
§A.2
.
OpenAI (2026)
OpenAI
Introducing gpt‑5.4 mini and nano
.
Note:
https://openai.com/index/introducing-gpt-5-4-mini-and-nano//
Accessed: May 25, 2026
Cited by:
§4.1
.
Qwen Team (2026)
Qwen Team
Qwen3.5: Towards Native Multimodal Agents
.
Note:
https://qwen.ai/blog?id=qwen3.5
Accessed: May 22, 2026
Cited by:
§3.1
.
Sahoo
et al.
(2024)
P. Sahoo, P. Meharia, A. Ghosh, S. Saha, V. Jain, and A. Chadha
A comprehensive survey of hallucination in large language, image, video and audio foundation models
.
In
Findings of the Association for Computational Linguistics: EMNLP 2024
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 11709–11724
.
External Links:
Link
,
Document
Cited by:
§1
.
Santilli
et al.
(2025)
A. Santilli, A. Golinski, M. Kirchhof, F. Danieli, A. Blaas, M. Xiong, L. Zappella, and S. Williamson
Revisiting uncertainty quantification evaluation in language models: spurious interactions with response length bias results
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 743–759
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-252-7
Cited by:
§A.3
,
§2
.
Shelmanov
et al.
(2025)
A. Shelmanov, E. Fadeeva, A. Tsvigun, I. Tsvigun, Z. Xie, I. Kiselev, N. Daheim, C. Zhang, A. Vazhentsev, M. Sachan, P. Nakov, and T. Baldwin
A head to predict and a head to question: pre-trained uncertainty quantification heads for hallucination detection in LLM outputs
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 35712–35731
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§A.1
,
§A.1
,
§A.2
,
§B.4
,
Table 1
,
§1
,
§1
,
§1
,
§2
,
§2
,
§3.1
,
§4.1
.
Srey
et al.
(2026a)
P. Srey, Q. M. Nguyen, X. Wu, and A. T. Luu
Towards reliable truth-aligned uncertainty estimation in large language models
.
arXiv preprint arXiv:2604.00445
.
External Links:
Link
Cited by:
§A.1
,
§B.1
.
Srey
et al.
(2025)
P. Srey, X. Wu, and A. T. Luu
Unsupervised hallucination detection by inspecting reasoning processes
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 22117–22129
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§A.1
,
§A.1
.
Srey
et al.
(2026b)
P. Srey, X. Wu, C. Nguyen, and A. T. Luu
Learning uncertainty from sequential internal dispersion in large language models
.
arXiv preprint arXiv:2604.15741
.
External Links:
Link
Cited by:
§A.1
,
§A.1
,
Table 1
,
§2
,
§3.1
.
Su
et al.
(2024)
W. Su, C. Wang, Q. Ai, Y. Hu, Z. Wu, Y. Zhou, and Y. Liu
Unsupervised real-time hallucination detection based on the internal states of large language models
.
In
Findings of the Association for Computational Linguistics: ACL 2024
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 14379–14391
.
External Links:
Link
,
Document
Cited by:
Table 1
,
Table 1
,
§3.1
,
§3.2
.
Talmor
et al.
(2019)
A. Talmor, J. Herzig, N. Lourie, and J. Berant
CommonsenseQA: a question answering challenge targeting commonsense knowledge
.
In
Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)
,
J. Burstein, C. Doran, and T. Solorio (Eds.)
,
Minneapolis, Minnesota
,
pp. 4149–4158
.
External Links:
Link
,
Document
Cited by:
item iii
.
Tan
et al.
(2025)
H. Tan, F. Sun, S. Liu, D. Su, Q. Cao, X. Chen, J. Wang, X. Cai, Y. Wang, H. Shen, and X. Cheng
Too consistent to detect: a study of self-consistent errors in LLMs
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 4755–4765
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§A.1
,
§1
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
Link
,
Document
Cited by:
§A.2
,
§1
,
§2
.
Vazhentsev
et al.
(2025)
A. Vazhentsev, L. Rvanova, I. Lazichny, A. Panchenko, M. Panov, T. Baldwin, and A. Shelmanov
Token-level density-based uncertainty quantification methods for eliciting truthfulness of large language models
.
In
Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
,
L. Chiruzzo, A. Ritter, and L. Wang (Eds.)
,
Albuquerque, New Mexico
,
pp. 2246–2262
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-189-6
Cited by:
§A.1
,
§A.1
,
§B.1
,
Table 1
,
§1
,
§2
,
§3.1
,
§3.3
.
Wang
et al.
(2025a)
K. Wang, S. A. Moktar, J. Li, K. Li, and F. Chen
Measuring aleatoric and epistemic uncertainty in llms: empirical evaluation on id and ood qa tasks
.
arXiv preprint arXiv:2511.03166
.
External Links:
Link
Cited by:
§A.2
,
§2
.
Wang
et al.
(2025b)
Y. Wang, P. Zhang, B. Yang, D. Wong, and R. Wang
Latent space chain-of-embedding enables output-free llm self-evaluation
.
In
International Conference on Learning Representations
,
Vol.
2025
,
pp. 70938–70970
.
External Links:
Link
Cited by:
Table 1
,
§2
,
§3.1
.
Wei
et al.
(2022)
J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou,
et al.
Chain-of-thought prompting elicits reasoning in large language models
.
Advances in neural information processing systems
35
,
pp. 24824–24837
.
External Links:
Link
Cited by:
§B.4
.
Wei
et al.
(2024)
J. Wei, C. Yang, X. Song, Y. Lu, N. Hu, J. Huang, D. Tran, D. Peng, R. Liu, D. Huang,
et al.
Long-form factuality in large language models
.
Advances in Neural Information Processing Systems
37
,
pp. 80756–80827
.
Cited by:
§B.4
.
Welbl
et al.
(2017)
J. Welbl, N. F. Liu, and M. Gardner
Crowdsourcing multiple choice science questions
.
In
Proceedings of the 3rd Workshop on Noisy User-generated Text
,
L. Derczynski, W. Xu, A. Ritter, and T. Baldwin (Eds.)
,
Copenhagen, Denmark
,
pp. 94–106
.
External Links:
Link
,
Document
Cited by:
item i
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
External Links:
Link
Cited by:
§3.1
.
Ye
et al.
(2024)
F. Ye, M. Yang, J. Pang, L. Wang, D. F. Wong, E. Yilmaz, S. Shi, and Z. Tu
Benchmarking llms via uncertainty quantification
.
In
Proceedings of the 38th International Conference on Neural Information Processing Systems
,
NIPS ’24
,
Red Hook, NY, USA
.
External Links:
ISBN 9798331314385
Cited by:
§A.2
.
Yoon
et al.
(2026)
D. Yoon, S. Kim, S. Yang, S. Kim, S. Kim, Y. Kim, E. Choi, Y. Kim, and M. Seo
Reasoning models better express their confidence
.
Advances in Neural Information Processing Systems
38
,
pp. 103869–103896
.
Cited by:
§A.3
.
Zha
et al.
(2023)
Y. Zha, Y. Yang, R. Li, and Z. Hu
AlignScore: evaluating factual consistency with a unified alignment function
.
In
Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
A. Rogers, J. Boyd-Graber, and N. Okazaki (Eds.)
,
Toronto, Canada
,
pp. 11328–11348
.
External Links:
Link
,
Document
Cited by:
§3.3
.
Zhang
et al.
(2025a)
F. Zhang, P. Yu, B. Yi, B. Zhang, T. Li, and Z. Liu
Prompt-guided internal states for hallucination detection of large language models
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 21806–21818
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-251-0
Cited by:
§A.1
,
§A.3
.
Zhang
et al.
(2025b)
Y. Zhang, Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, Y. Chen, L. Wang, A. T. Luu, W. Bi, F. Shi, and S. Shi
Siren’s song in the ai ocean: a survey on hallucination in large language models
.
Computational Linguistics
51
(
4
),
pp. 1373–1418
.
External Links:
Link
,
Document
Cited by:
§1
.
Zhu
et al.
(2024)
D. Zhu, D. Chen, Q. Li, Z. Chen, L. Ma, J. Grossklags, and M. Fritz
PoLLMgraph: unraveling hallucinations in large language models via state transition dynamics
.
In
Findings of the Association for Computational Linguistics: NAACL 2024
,
K. Duh, H. Gomez, and S. Bethard (Eds.)
,
Mexico City, Mexico
,
pp. 4737–4751
.
External Links:
Link
,
Document
Cited by:
§A.1
,
§2
.
Appendix A
Extended Related Work
Here, we provide additional background on related work that we omit from the main text for clearer presentation.
A.1
Probe-based Uncertainty Estimation
Probe-based UE leverages LLM internal states to predict whether generated responses are correct or factual, with the predicted probability reflecting model confidence, or inversely, uncertainty.
This paradigm is attractive because it typically requires only a single LLM forward pass, unlike expensive sampling-based methods, and often achieves strong in-domain performance.
Early work showed that truth-related information can be extracted from hidden activations, often from the final layer and final token, using simple linear classifiers
(
Azaria and Mitchell, 2023
;
Burns et al., 2022
;
Marks and Tegmark, 2023
)
. Subsequent methods extend this paradigm by deriving more informative hidden state representations in several ways.
Some works steer the generation procedure via prompting to elicit responses, and hence internal states, that are more discriminative for factual verification
(
Zhang et al., 2025a
;
Srey et al., 2025
)
.
Later work exposes the probe to richer hidden-state information, for example by pooling hidden states across all layers
(
CH-Wang et al., 2024
)
, or by modelling hidden states from all generated tokens as sequential inputs
(
Shelmanov et al., 2025
;
Srey et al., 2026b
;
Zhu et al., 2024
)
, or by integrating cross-model hidden states
(
Tan et al., 2025
)
.
Another approach transforms hidden states into structured summaries intended to capture uncertainty- and hallucination-relevant geometry, such as density-based features across layers
(
Vazhentsev et al., 2025
)
, or cross-layer dynamics
(
Srey et al., 2026b
)
.
A parallel line of work explores internal signals beyond hidden states alone. Attention-based methods, for example, use patterns such as the lookback ratio
(
Chuang et al., 2024
)
, the relative attention paid to source context compared to generated tokens.
Related works also incorporate probability-space information, such as token probabilities
(
Vazhentsev et al., 2025
)
, entropy
(
Srey et al., 2026b
)
, or logit-derived features, such as top-
k
k
output indices
(
He et al., 2024
)
.
These recent hybrid methods combine hidden states, attention maps, and probability-based signals through direct concatenation
(
Shelmanov et al., 2025
;
Srey et al., 2025
;
Vazhentsev et al., 2025
)
, or through specialised submodules
(
He et al., 2024
)
.
Related calibration methods learn post-hoc mappings from heuristic UE scores to correctness-aligned estimates with a model-specific corrector
(
Li et al., 2025b
;
Srey et al., 2026a
)
, further extending internal-state probes.
Overall, these methods show that diverse information relevant to factuality is available within the generation trace.
As a result, probe-based UE has increasingly been framed as a search for richer features, better calibrated signals, and higher-capacity optimisation pipelines.
However, these methods often vary simultaneously in many design factors, making it unclear which choices actually account for the observed gains.
Our work clarifies when such engineering is necessary, when simple hidden state probes suffice, and which design choices remain robust under transfer.
A.2
Benchmarking and Transfer Robustness
LM-Polygraph
Fadeeva et al. (2023)
provides an extensive toolkit for comparing uncertainty estimators, while
Vashurin et al. (2025)
benchmark a broad collection of UE and confidence-normalisation methods across numerous generation tasks. UQLM
(
Bouchard et al., 2026
)
similarly supplies off-the-shelf black-box, white-box, LLM-judge, and ensemble scorers. Other evaluation studies examine robustness to semantically equivalent prompts
(
Mahaut et al., 2024
)
, in-domain and OOD question answering
(
Wang et al., 2025a
)
, uncertainty-aware LLM benchmarking
(
Ye et al., 2024
)
, and real-time entity-level hallucination detection
(
Obeso et al., 2025
)
. These efforts establish the importance of consistent multi-task evaluation, although they do not systematically factorise the training pipeline of supervised internal-state probes. LM-Polygraph’s central contribution is broad, controllable UE benchmarking rather than a probe-specific analysis of training-test transfer.
Probe transfer has been considered in several forms. For example,
CH-Wang et al. (2024)
and
Chuang et al. (2024)
evaluate transfer between benchmark datasets. More recently, this extends to long-form generations.
Han et al. (2025)
demonstrate that lightweight final-state probes can detect factual errors in long-form generations, and generalise to outputs from other models and generations of other entities.
Similarly,
Shelmanov et al. (2025)
train reusable uncertainty heads and study their application when deployed to generations in other domains. These works motivate reusable probes but within relatively constrained settings, while our experiments specifically consider probes trained on short-form benchmark responses and transferred to claim-level open-ended generation.
Han et al. (2025)
’s principal finding is therefore complementary to our focus on factorised design and transfer across generation formats.
A.3
Correctness Annotation and Prompting
The evaluation of UE requires a correctness annotation protocol or function against which uncertainty scores are assessed. Lexical overlap metrics such as ROUGE
(
Lin, 2004
)
are inexpensive but may not capture semantically correct paraphrases and are threshold-sensitive.
Janiak et al. (2025)
show that ROUGE can align poorly with human factuality judgements and can substantially misguide conclusions on UE performance.
Santilli et al. (2025)
analyse how shared biases, namely response-length bias, between correctness functions and UE scores can distort AUROC rankings.
Their evaluation covers lexical, embedding-based, and LLM-judge correctness functions as well as learned final-token probes trained with ROUGE-L or LLM-judge supervision. They find LLM-judge correctness functions to be comparatively well aligned with human judgements and less susceptible to length-related confounding.
Our annotation study builds on these findings rather than claiming the general observation as new. We test whether the effect extends across hidden-state, attention, probability, dispersion, and hybrid probe representations while holding the evaluation labels fixed. This places annotation choice within the broader probe-training pipeline and allows its interaction with feature design to be examined under matched conditions.
Prompting can likewise alter both model confidence and internal representations used by uncertainty estimators. Prior work finds that reasoning can improve confidence expressed in the output token space in some settings
(
Yoon et al., 2026
)
, but not consistently
(
Mei et al., 2026
)
, and may inflate probability-based confidence on multiple-choice tasks
(
Fu et al., 2025
)
. Prompt-guided probe methods also intentionally elicit representations that are more separable for factuality prediction
(
Zhang et al., 2025a
)
.
These findings motivate our controlled comparison of direct, concise-reasoning, and long-reasoning response formats.
Our novelty.
While our work recovers several prior observations, our controlled comparison yields two novel insights. First, in-domain superiority and transfer robustness favour different feature classes, encouraging researchers to look beyond in-domain benchmark evaluation. Second, probes pretrained only on short-form benchmarks, adopting our findings, can retain meaningful factuality signals when transferred to open-ended generation, providing a useful zero-target-label baseline for when collecting annotated long-form data is costly.
Collectively, these findings identify transfer robustness as a distinct design objective and demonstrate a practical path towards reusable uncertainty probes beyond matched benchmarks.
Appendix B
Experimental Setup Details
B.1
Feature Representations
Table
1
summarises the feature representations used in our factorised study.
We follow the original formulation proposed in the respective papers and apply sequence mean aggregation as needed.
In particular, for embedding- and logit-based UE scores, we apply TAC
(
Srey et al., 2026a
)
to better align raw confidence with truthfulness, and we adapt Internal Variance to a sequence-level internal-dispersion feature.
Feature and Probe Coverage.
We compare representative features under a tractable design. On top of concatenation with MSP, as is standard in prior work
(
Vazhentsev et al., 2025
)
, the evaluated hybrid combinations include: Internal Variance combines with Entropy; Layer Top-m Probability projects intermediate-layer representations through the output head, combining embeddings with logits. Other combinations are worthwhile, but evaluating every pair would be infeasible and obscure the factorised comparison.
Our evaluation also includes layer-wise information: Embedding (all) retains a representation from every layer, while Layer Top-
m
m
Probability and several structured features capture layer-wise trajectories. The study does not exhaustively cover alternative token- and layer-wise representations.
Subsequently, we limit the probe architectures to simple classifiers as these features were primarily designed as fixed-length, sequence-level features. Adapting them to variable-length sequences would require redefining their aggregation, introducing padding and masking choices, and substantially increasing storage and training costs. A systematic evaluation of sequential probes, such as Transformers, is valuable but constitutes a separate design axis beyond the current scope.
Type
Name
Description
Citation
Hidden State
Embedding (last)
Last generated token, last layer embedding
(
Azaria and Mitchell, 2023
)
Embedding (mean)
Mean embedding across generated tokens and layers
(
Su et al., 2024
)
Embedding (all)
Token-mean embeddings across all layers
(
Su et al., 2024
)
CoE-R, CoE-C
Geometry of hidden state trajectory across successive layers
(
Wang et al., 2025b
)
Circular Variance, Cov. Determinant
Cross-layer internal dispersion
(
Srey et al., 2026b
)
SATMD
Layer-wise token deviations from the distribution of correct generations
(
Vazhentsev et al., 2025
)
Logit
MSP, Entropy, Perplexity, Energy
Logit-derived uncertainty score
(
Huang et al., 2025b
;
Liu et al., 2020
)
Top-
m
m
m
m
-highest predicted token probabilities.
(
He et al., 2024
)
Attention
Attention
Attention maps to previous tokens.
(
Shelmanov et al., 2025
)
Lookback Ratio
Relative attention paid to input context versus generated tokens.
(
Chuang et al., 2024
)
Combined
Layer Top-
m
m
Prob.
Concatenation of Top-
m
m
Prob. from all layers.
(
He et al., 2024
)
Internal Variance, Attention + MSP, SATMD + MSP
Combination via concatenation.
—
Table 1:
Feature representations used in our study.
B.2
Feature Formulations
Here, we provide brief formulae of the feature representations.
More detailed formulations can be found in the respective papers.
Notation.
Let
x
=
(
x
1
,
…
,
x
N
)
x=(x_{1},\ldots,x_{N})
denote the input query and
y
=
(
y
1
,
…
,
y
T
)
y=(y_{1},\ldots,y_{T})
the response.
The LM has
L
L
transformer layers, hidden dimension
d
d
,
Q
Q
attention heads per layer, and vocabulary
𝒱
\mathcal{V}
.
We write
h
l
,
t
∈
ℝ
d
h_{l,t}\in\mathbb{R}^{d}
for the hidden state of generated token
t
t
at layer
l
∈
{
0
,
…
,
L
}
l\in\{0,\ldots,L\}
, including the embedding output at
l
=
0
l=0
. We define sequence-mean embedding, LM predicted probability, and logit, respectively, as
h
¯
l
\displaystyle\bar{h}_{l}
=
1
T
​
∑
t
=
1
T
h
l
,
t
,
\displaystyle=\frac{1}{T}\sum_{t=1}^{T}h_{l,t},
p
t
\displaystyle p_{t}
=
softmax
⁡
(
z
t
)
,
\displaystyle=\operatorname{softmax}(z_{t}),
z
t
\displaystyle z_{t}
=
W
u
​
h
L
,
t
+
b
U
,
\displaystyle=W_{u}h_{L,t}+b_{U},
where
W
U
W_{U}
is the LM output head. Let
Top
m
⁡
(
p
)
∈
ℝ
m
\operatorname{Top}_{m}(p)\in\mathbb{R}^{m}
return the
m
m
largest entries of
p
p
in descending order, and let
⨁
\bigoplus
denote the concatenation operator. Unless otherwise stated, token-level quantities are averaged over the generated response. We use
m
=
10
m=10
, energy temperature
τ
=
0.7
\tau=0.7
, attention-window size
k
=
2
k=2
, and covariance regularisation
η
=
10
−
3
\eta=10^{-3}
.
Hidden-state embeddings.
We evaluate three embedding aggregations: Embedding (last), Embedding (mean), and Embedding (all), which are defined, respectively, as
f
last
\displaystyle f_{\text{last}}
=
h
L
,
T
,
\displaystyle=h_{L,T},
f
mean
\displaystyle f_{\text{mean}}
=
1
L
+
1
​
∑
l
=
0
L
h
¯
l
,
\displaystyle=\frac{1}{L+1}\sum_{l=0}^{L}\bar{h}_{l},
f
all
\displaystyle f_{\text{all}}
=
⨁
l
=
0
L
h
¯
l
\displaystyle=\bigoplus_{l=0}^{L}\bar{h}_{l}
Thus, Embedding (last) uses the final token and final layer, Embedding (mean) averages across tokens and layers, and Embedding (all) averages across tokens while retaining the embedding from every layer.
Cross-layer evolution.
Let
c
⁡
(
a
,
b
)
=
(
a
⊤
​
b
)
/
(
‖
a
‖
2
​
‖
b
‖
2
)
c(a,b)=(a^{\top}b)/(\|a\|_{2}\|b\|_{2})
, and for
l
=
1
,
…
,
L
l=1,\ldots,L
, define the successive-layer normalised angular and magnitude changes
a
l
=
arccos
⁡
(
c
⁡
(
h
¯
l
,
h
¯
l
−
1
)
)
arccos
⁡
(
c
⁡
(
h
¯
L
,
h
¯
0
)
)
,
d
l
=
‖
h
¯
l
−
h
¯
l
−
1
‖
2
‖
h
¯
L
−
h
¯
0
‖
2
,
a_{l}=\frac{\arccos\left(c(\bar{h}_{l},\bar{h}_{l-1})\right)}{\arccos\left(c(\bar{h}_{L},\bar{h}_{0})\right)},\;d_{l}=\frac{\|\bar{h}_{l}-\bar{h}_{l-1}\|_{2}}{\|\bar{h}_{L}-\bar{h}_{0}\|_{2}},
The two cross-layer evolution summaries, CoE-R and CoE-C, are
f
CoE-R
=
1
L
​
∑
l
=
1
L
(
d
l
−
a
l
)
\displaystyle f_{\text{CoE-R}}=\frac{1}{L}\sum_{l=1}^{L}(d_{l}-a_{l})
f
CoE-C
=
\displaystyle f_{\text{CoE-C}}=
(
1
L
∑
l
=
1
L
d
l
cos
a
l
)
2
+
(
1
L
∑
l
=
1
L
d
l
sin
a
l
)
2
\displaystyle\sqrt{\left(\frac{1}{L}\sum_{l=1}^{L}d_{l}\cos a_{l}\right)^{2}+\left(\frac{1}{L}\sum_{l=1}^{L}d_{l}\sin a_{l}\right)^{2}}
Cross-layer dispersion.
Circular Variance measures directional disagreement among layer representations
f
CircVar
=
1
−
‖
1
L
+
1
​
∑
l
=
0
L
h
¯
l
‖
h
¯
l
‖
2
‖
2
f_{\text{CircVar}}=1-\left\lVert\frac{1}{L+1}\sum_{l=0}^{L}\frac{\bar{h}_{l}}{\|\bar{h}_{l}\|_{2}}\right\rVert_{2}
For Cov. Determinant, let
H
∈
ℝ
(
L
+
1
)
×
d
H\in\mathbb{R}^{(L+1)\times d}
contain
h
¯
l
⊤
\bar{h}_{l}^{\top}
as its rows, and centre each row across its hidden dimensions
H
~
l
,
r
=
H
l
,
r
−
1
d
​
∑
s
=
1
d
H
l
,
s
\tilde{H}_{l,r}=H_{l,r}-\frac{1}{d}\sum_{s=1}^{d}H_{l,s}
We compute the regularised layer covariance
C
=
H
~
​
H
~
⊤
d
−
1
+
η
​
I
C=\frac{\tilde{H}\tilde{H}^{\top}}{d-1}+\eta I
with
I
I
being the identity matrix and
η
=
10
−
3
\eta=10^{-3}
, and use its normalised log-determinant
f
CovDet
=
1
L
+
1
​
logdet
⁡
C
=
1
L
+
1
​
∑
j
=
1
L
+
1
log
⁡
λ
j
​
(
C
)
,
f_{\text{CovDet}}=\frac{1}{L+1}\operatorname{logdet}C=\frac{1}{L+1}\sum_{j=1}^{L+1}\log\lambda_{j}(C),
where
λ
j
\lambda_{j}
is the
j
j
-th eigenvalue.
Density-based feature.
SATMD fits a Gaussian reference distribution at each layer using token representations from correct training responses. Let
μ
l
\mu_{l}
and
Σ
l
\Sigma_{l}
be the corresponding layer-wise mean and regularised covariance. The Mahalanobis distance of token
t
t
is
D
l
,
t
=
(
h
l
,
t
−
μ
l
)
⊤
​
Σ
l
−
1
​
(
h
l
,
t
−
μ
l
)
D_{l,t}=\sqrt{(h_{l,t}-\mu_{l})^{\top}\Sigma_{l}^{-1}(h_{l,t}-\mu_{l})}
SATMD retains the mean distance from each layer
f
SATMD
=
⨁
l
=
0
L
(
1
T
​
∑
t
=
1
T
D
l
,
t
)
f_{\text{SATMD}}=\bigoplus_{l=0}^{L}\left(\frac{1}{T}\sum_{t=1}^{T}D_{l,t}\right)
Output-distribution features.
The sequence-level Max. Seq. Prob. (MSP), Entropy, (log-)Perplexity, and Energy scores are
f
MSP
\displaystyle f_{\text{MSP}}
=
1
T
​
∑
t
=
1
T
max
v
∈
𝒱
⁡
p
t
​
(
v
)
,
\displaystyle=\frac{1}{T}\sum_{t=1}^{T}\max_{v\in\mathcal{V}}p_{t}(v),
f
Entropy
\displaystyle f_{\text{Entropy}}
=
−
1
T
∑
t
=
1
T
∑
v
∈
𝒱
p
t
(
v
)
log
p
t
(
v
)
,
\displaystyle=-\frac{1}{T}\sum_{t=1}^{T}\sum_{v\in\mathcal{V}}p_{t}(v)\log p_{t}(v),
f
Perplexity
\displaystyle f_{\text{Perplexity}}
=
−
1
T
∑
t
=
1
T
log
max
v
∈
𝒱
p
t
(
v
)
,
\displaystyle=-\frac{1}{T}\sum_{t=1}^{T}\log\max_{v\in\mathcal{V}}p_{t}(v),
f
Energy
\displaystyle f_{\text{Energy}}
=
−
τ
T
∑
t
=
1
T
log
∑
v
∈
𝒱
exp
(
z
t
​
(
v
)
τ
)
\displaystyle=-\frac{\tau}{T}\sum_{t=1}^{T}\log\sum_{v\in\mathcal{V}}\exp{\left(\frac{z_{t}(v)}{\tau}\right)}
Top-
m
m
Prob. retains more information from the output distribution
f
Top-
​
m
=
1
T
​
∑
t
=
1
T
Top
m
⁡
(
p
t
)
f_{\text{Top-}m}=\frac{1}{T}\sum_{t=1}^{T}\operatorname{Top}_{m}(p_{t})
For Layer Top-
m
m
Prob., every intermediate hidden state is projected through the output head
p
l
,
t
\displaystyle p_{l,t}
=
softmax
⁡
(
W
U
​
h
l
,
t
+
b
U
)
,
\displaystyle=\operatorname{softmax}(W_{U}h_{l,t}+b_{U}),
f
LayerTop-
​
m
\displaystyle f_{\text{LayerTop-}m}
=
⨁
l
=
1
L
[
1
T
​
∑
t
=
1
T
Top
m
⁡
(
p
l
,
t
)
]
\displaystyle=\bigoplus_{l=1}^{L}\left[\frac{1}{T}\sum_{t=1}^{T}\operatorname{Top}_{m}(p_{l,t})\right]
Attention features.
Let
α
t
,
j
l
,
q
\alpha_{t,j}^{l,q}
denote the attention weight from token
t
t
to
j
j
, at layer
l
l
, and head
q
q
. For Lookback Ratio, we compute the mean attention assigned to the input and preceding generated tokens
A
ctx
l
,
q
​
(
t
)
\displaystyle A^{l,q}_{\text{ctx}}(t)
=
1
N
​
∑
j
=
1
N
α
t
,
j
l
,
q
,
\displaystyle=\frac{1}{N}\sum_{j=1}^{N}\alpha_{t,j}^{l,q},
A
gen
l
,
q
​
(
t
)
\displaystyle A^{l,q}_{\text{gen}}(t)
=
1
max
⁡
(
t
−
1
,
1
)
​
∑
j
=
1
t
−
1
α
t
,
N
+
j
l
,
q
,
\displaystyle=\frac{1}{\max(t-1,1)}\sum_{j=1}^{t-1}\alpha_{t,N+j}^{l,q},
R
t
l
,
q
\displaystyle R_{t}^{l,q}
=
A
ctx
l
,
q
​
(
t
)
A
ctx
l
,
q
​
(
t
)
+
A
gen
l
,
q
​
(
t
)
\displaystyle=\frac{A^{l,q}_{\text{ctx}}(t)}{A^{l,q}_{\text{ctx}}(t)+A^{l,q}_{\text{gen}}(t)}
The fixed-length Lookback Ratio representation averages this quantity across generated tokens and concatenates all layers and head
f
LookbackRatio
=
⨁
l
=
1
L
⨁
q
=
1
Q
(
1
T
​
∑
t
=
1
T
R
t
l
,
q
)
f_{\text{LookbackRatio}}=\bigoplus_{l=1}^{L}\bigoplus_{q=1}^{Q}\left(\frac{1}{T}\sum_{t=1}^{T}R_{t}^{l,q}\right)
Recent-token Attention retains each head’s attention to the
k
k
immediately preceding generated tokens
f
Attention
=
⨁
l
=
1
L
⨁
q
=
1
Q
⨁
r
=
1
k
[
1
T
∑
t
=
1
T
𝟙
[
t
>
r
]
α
t
,
N
+
t
−
r
l
,
q
]
f_{\text{Attention}}=\bigoplus_{l=1}^{L}\bigoplus_{q=1}^{Q}\bigoplus_{r=1}^{k}\left[\frac{1}{T}\sum_{t=1}^{T}\mathbbm{1}[t>r]\alpha_{t,N+t-r}^{l,q}\right]
Unavailable preceding positions at the beginning of a generation are zero-padded. Following the small-window setting
(
Chuang et al., 2024
)
, we fix
k
=
2
k=2
for all settings.
Hybrid features.
These are constructed by direct concatenation
f
Attention
+
MSP
\displaystyle f_{\text{Attention}+\text{MSP}}
=
f
Attention
⊕
f
MSP
,
\displaystyle=f_{\text{Attention}}\oplus f_{\text{MSP}},
f
InternalVar
\displaystyle f_{\text{InternalVar}}
=
f
CircVar
⊕
f
CovDet
⊕
f
Entropy
,
\displaystyle=f_{\text{CircVar}}\oplus f_{\text{CovDet}}\oplus f_{\text{Entropy}},
f
SATMD
+
MSP
\displaystyle f_{\text{SATMD}+\text{MSP}}
=
f
SATMD
⊕
f
MSP
\displaystyle=f_{\text{SATMD}}\oplus f_{\text{MSP}}
Finally, each representation is flattened into a fixed-length vector and standardised dimension-wise using statistics fitted only on the training split
f
~
j
=
f
j
−
μ
j
train
σ
j
train
+
ϵ
\tilde{f}_{j}=\frac{f_{j}-\mu_{j}^{\text{train}}}{\sigma_{j}^{\text{train}}+\epsilon}
The linear probe then estimates correctness as
P
⁡
(
y
is correct
|
f
)
=
σ
⁡
(
w
⊤
​
f
~
+
b
)
P(\text{$y$ is correct}|f)=\sigma(w^{\top}\tilde{f}+b)
B.3
Probe Training
Data Construction.
For each LLM/dataset configuration, we train a separate uncertainty probe per feature with label 1 denoting a correct generated response. TriviaQA, SciQ, and PopQA responses are labelled by Gemini-3.1-Flash-Lite LLM-Judge, whereas ARC, CSQA, BoolQ, and StrategyQA are labelled by comparing the parsed final answer against the reference answer.
For each dataset, we use the full 1000-example SciQ test split and the full 1221-example CSQA validation split. For TriviaQA validation, PopQA test, BoolQ validation, StrategyQA train, and ARC Challenge split, we select a random subset of 1000 examples.
We run five-seed experiments for
Figures
1
and
8
while other experiments are single-seed. Then, we construct a stratified 80/20 train/test split using binary correctness labels.
For the pooled seven-benchmark probes in
Section
4
experiments, we combine the labelled responses, obtaining approximately 7000 instances in total.
Hyperparameter Specifications.
Each feature is normalised before probe fitting. Sequence- or layer-structured representations are flattened before normalisation.
We employ the binary cross-entropy loss using the Adam optimiser with learning rate
10
−
3
10^{-3}
and batch size 32.
We train the probes for at most 100 epochs, with early stopping of patience 20 using validation AUROC. The linear probe is a single affine map from the standardised feature vector to one logit. The MLP uses a 32-unit hidden layer with ReLU activation followed by a scalar output layer. The CNN treats the flattened feature vector as a one-channel one-dimensional sequence and applies two 1D convolutional layers (32 channels, kernel size 3, same-length padding), each followed by ReLU. An adaptive global average pool and a final linear layer produce the scalar logit.
B.4
Prompt Templates
Tables
2
,
3
,
4
,
5
and
6
report all prompts. For long reasoning, we follow CoT
(
Wei et al., 2022
)
, and we adapt it to elicit constrained medium reasoning output.
Thinking mode is disabled, and reasoning is elicited solely through prompt suffixes.
The open-ended generation prompts follow entity-centric templates of
Shelmanov et al. (2025)
, with Biographies (ID) and claim-span setup aligned with
Han et al. (2025)
. For claim-level annotation, we adopt the established decompose-then-verify framework
(
Min et al., 2023
;
Wei et al., 2024
)
, extracting atomic, self-contained claims before assigning binary factuality labels. We request the LLM-judge for schema-constrained JSON outputs with verbatim source spans and offsets to support reliable parsing similar to
Li et al. (2025a)
.
Shared Prefix
You are a helpful assistant, providing accurate and concise information without overthinking.
TriviaQA, SciQ, PopQA
{question}
Be concise, and output only the final answer.
ARC
Answer the following multiple choice science question. Your final answer should be of the following format: “Answer: $LABEL” (without quotes), where LABEL is one of the provided choice labels. Be concise, and output only the final answer.
Question: {question}
Choices:
{label}. {choice}
BoolQ
Read the passage and answer the yes/no question. Your final answer should be of the following format: “Answer: yes” or “Answer: no” (without quotes). Be concise, and output only the final answer.
Passage: {passage}
Question: {question}
CommonsenseQA
Answer the following multiple choice common-sense reasoning question. Your final answer should be of the following format: “Answer: $LETTER” (without quotes), where LETTER is one of ABCDE. Be concise, and output only the final answer.
{question-with-choices}
StrategyQA
Answer the following yes/no question. Your final answer should be of the following format: “Answer: yes” or “Answer: no” (without quotes). Be concise, and output only the final answer.
{question}
Table 2:
Generation prompts for the Section 3 datasets.
Appendix C
Supplementary Experiments
Mode
Suffix
NR
Be concise, and output only the final answer.
MR
Output a single sentence of reasoning before the final answer.
LR
Think step by step and output the reasoning process before answering.
Table 3:
Reasoning-control suffixes for the NR, MR, and LR prompts for ARC and CommonsenseQA.
Domain
Prompt
Biographies (ID)
Tell me a paragraph bio of
{person}
.
Biographies (OOD)
Tell me a bio of
{person}
.
Artworks
Tell me about the artwork
{artwork}
and its artist.
Books
Tell me about the book
{book}
and its author.
Cities
Tell me the history of
{city}
.
Events
Tell me about
{event}
event.
Inventions
Tell me about the invention of
{invention}
and its inventor.
Landmarks
Tell me about the landmark
{landmark}
.
Movies
Tell me about the movie
{movie}
and its cast.
Table 4:
Prompts for open-ended entity-centric generation in Section 4.
Component
Prompt
System
You decompose long-form passages into atomic factual claims. Return JSON only.
User
Task:
Break the passage into atomic factual claims.
Rules:
(1) Each claim should contain exactly one checkable piece of information. (2) Claims should be self-contained; include the relevant person/entity name when needed. (3) Do not include opinions, formatting, or non-factual filler. (4) For every claim, copy the shortest exact contiguous source quote from the passage that supports where the claim came from. (5) The source quote must be a verbatim substring of the passage. (6) Return
source_start
and
source_end
as zero-based Python character offsets into the passage for
source_quote
;
source_end
is exclusive. (7) Return claims in passage order. Source spans may overlap when one sentence supports multiple atomic claims.
Return JSON only:
{"claims":[{"claim":"...","source_quote":"...",
"source_start":0,"source_end":10}]}
Return JSON matching this schema:
{decomposition-schema}
Entity: {entity}
(included when available)
Passage
{generated-passage}
Table 5:
System and user prompts used to decompose each long-form generation into atomic claims. The API is run with temperature zero and JSON output enabled.
Component
Prompt
System
You are a strict factuality evaluation assistant. Return JSON only, with exactly one result per input ID:
{"results":[{"id":"...","label":1}]}
.
User
You are evaluating one atomic factual claim using the supplied reference evidence. Label only whether every factual detail in the claim is directly and precisely supported by that evidence; do not use the generated answer as evidence.
0 means contradicted, unsupported, unverifiable, vague, approximate, wrong entity/topic, or only partially supported. 1 means fully and precisely supported. Be strict: if any part is uncertain or unsupported, return 0.
Return JSON matching this schema:
{label-schema}
Claims to evaluate:
[{"id":{id}, "entity":{entity}, "prompt":{generation-prompt},
"claim_to_label":{atomic-claim}, "reference_source":
{"title":{title}, "url":{url}, "evidence":{evidence}}}]
Table 6:
System and user prompts for claim-level annotation by LLM-Judge. Annotations for Biographies (ID) are evidence-grounded while other domains are not.
Domain
# Claims
Correct Claims (%)
Qwen
Gemma
Llama
Qwen
Gemma
Llama
Bio (ID)
822
907
800
33.09
40.46
58.13
Bio (OOD)
682
703
983
66.86
78.09
80.37
Artworks
603
595
623
85.57
84.54
82.99
Books
746
637
784
88.87
95.45
87.37
Cities
714
542
714
71.57
75.65
72.97
Events
675
550
711
88.74
93.09
85.65
Inventions
692
545
715
86.99
86.97
76.64
Landmarks
803
675
820
83.94
89.78
81.10
Movies
722
611
905
76.73
92.31
87.62
Table 7:
Statistics for open-ended generation datasets.
Here, we provide supplementary experiments.
Figure 7:
AUPR for the main models.
AUPR Results.
We report the five-seed AUPR in
Figure
7
, where incorrect responses represent the positive class, and summarise the rankings in
Table
8
. These results support our main conclusions.
Figure 8:
AUROC and ECE of Llama-3.1-8B-Instruct and Qwen-3-4B-Instruct.
Figure 9:
Benchmark-transfer performance with Gemma-3-12B-Instruct. Average AUROC across In-domain, Out-of-domain (same task), and Out-of-domain (cross task) configurations.
Additional Model Results.
Figure
8
reports in-domain AUROC and ECE for Qwen-3-4B-Instruct and Llama-3.1-8B-Instruct.
The overall trends are consistent with the main results: hidden state and attention-based features remain strong in-domain.
Figure
9
replicates task transfer analysis in
Section
3.4
with Gemma-3-12B-Instruct.
The broad conclusion remains consistent: hidden state and attention features lose much of their in-domain advantage, particularly under cross-task shift, whereas several structured probability and dispersion features retain performance more consistently. However, the ordering of individual representations changes substantially, indicating that transfer robustness is model-dependent, with no dominant feature.
Discriminability
Calibration
Precision
Feature
AUROC
Mean Rank (SE)
Feature
ECE
Mean Rank (SE)
Feature
AUPR
Mean Rank (SE)
Embedding (Mean)
82.77
3.68 (0.33)
Internal Variance
15.42
4.78 (0.59)
Embedding (Mean)
62.05
3.56 (0.36)
Lookback Ratio
82.38
4.14 (0.51)
Top-
m
m
Prob.
18.53
6.30 (0.53)
Attention + MSP
61.45
4.08 (0.32)
Attention + MSP
82.03
4.32 (0.36)
Lookback Ratio
20.84
6.98 (0.50)
Lookback Ratio
60.86
4.15 (0.47)
Embedding (Last)
81.88
4.41 (0.40)
Layer Top-
m
m
Prob.
20.04
7.10 (0.56)
Embedding (Last)
61.14
4.22 (0.50)
Attention
81.18
5.23 (0.56)
Embedding (Last)
21.55
7.43 (0.41)
Attention
59.22
5.85 (0.56)
Embedding (All)
80.91
5.60 (0.36)
Attention + MSP
21.48
7.64 (0.44)
Layer Top-
m
m
Prob.
53.48
7.26 (0.65)
Internal Variance
75.56
8.17 (0.58)
Attention
21.63
8.02 (0.50)
Internal Variance
54.84
7.65 (0.52)
Layer Top-
m
m
Prob.
76.46
8.28 (0.72)
Embedding (Mean)
22.67
8.46 (0.42)
Top-
m
m
Prob.
53.48
7.96 (0.63)
Top-
m
m
Prob.
75.28
8.59 (0.60)
Max. Seq. Prob.
28.22
10.12 (0.73)
Embedding (All)
53.15
8.58 (0.47)
SATMD + MSP
65.98
11.75 (0.63)
CoE-R
28.72
10.56 (0.48)
Perplexity
42.87
12.17 (0.49)
SATMD
64.77
12.36 (0.65)
Embedding (All)
26.80
10.62 (0.92)
Entropy
40.07
12.26 (0.82)
Perplexity
52.84
12.70 (0.79)
Circular Variance
29.67
11.17 (0.62)
SATMD + MSP
40.60
12.95 (0.55)
Entropy
58.33
12.86 (0.51)
Energy
30.08
11.20 (0.41)
Max. Seq. Prob.
41.27
13.10 (0.51)
Max. Seq. Prob.
57.17
13.72 (0.46)
Cov. Determinant
29.77
11.34 (0.50)
Energy
39.13
13.73 (0.47)
Energy
55.95
13.96 (0.44)
Perplexity
31.13
11.41 (0.51)
SATMD
39.28
13.82 (0.51)
Cov. Determinant
52.91
14.78 (0.36)
CoE-C
30.94
11.64 (0.55)
CoE-R
38.42
14.20 (0.43)
CoE-R
55.06
14.81 (0.31)
Entropy
32.56
11.98 (0.64)
Cov. Determinant
37.30
14.50 (0.39)
Circular Variance
51.54
15.27 (0.30)
SATMD + MSP
59.48
16.59 (0.72)
CoE-C
35.99
14.95 (0.39)
CoE-C
53.48
15.35 (0.32)
SATMD
62.36
16.65 (0.89)
Circular Variance
35.37
15.00 (0.33)
Table 8:
Summary ranking statistics.
Aggregate Ranking Statistics.
Table
8
lists the explicit ranking statistics for the main results in
Figures
1
and
8
aggregated across all datasets, models, and five seeds.
Table
9
summarises the ranking for the benchmark transfer analysis in
Figure
5
. To obtain the SE’s, we bootstrap resamples of target datasets within each task; thus, these values describe uncertainty in method rankings across these benchmarks.
Figure 10:
Benchmark-transfer performance. Average ECE across In-domain, Out-of-domain (same task), and Out-of-domain (cross task) configurations.
Calibration under Transfer.
Figure
10
reports ECE under the same in-domain, OOD same-task, and OOD cross-task settings. This shows that discriminability and calibration do not always move together. Features with strong AUROC are not necessarily the best calibrated, and some lower-dimensional structured features remain comparatively stable under shift.
Figure 11:
In-domain AUROC against OOD setting for individual benchmarks with Qwen-3-8B.
Figure 12:
In-domain ECE against OOD setting for individual benchmarks with Qwen-3-8B.
Per-dataset Transfer.
Figure
11
and
Figure
12
provide per-dataset transfer results for AUROC and ECE, respectively. While the degree of transfer degradation varies across datasets, hidden state features generally remain strong in-domain, whereas structured features tend to retain performance more consistently under OOD evaluation.
In particular, some features occasionally demonstrate significant OOD improvements, namely Cov. Determinant and Circular Variance.
Both features reduce cross-layer dispersion into a single scalar, so the linear probe primarily determines the direction and threshold of its association with correctness. Our per-dataset results show that this direction can be unstable: on the same target, probes trained on different sources sometimes produce approximately reversed rankings. An ID probe can therefore perform poorly when its training split estimates the direction unreliably, while an OOD source may learn the direction that happens to align better with the target test split.
The apparent improvement should thus not be interpreted as distribution shift improving the feature. Rather, it exposes the instability of fitting individual scalar dispersion measures.
Figure
5
further accentuates the pattern by averaging multiple unstable source-target transfers.
Figure 13:
Average OOD performance with different probe architectures.
Figure 14:
Effect of probe architecture on ECE.
Figure 15:
AUROC for individual dataset with varying training set size.
Transfer Ranking.
Table
9
presents a summary ranking for the main transfer AUROC results.
OOD (same task)
OOD (cross task)
Feature
AUROC
Mean rank (SE)
Feature
AUROC
Mean rank (SE)
Lookback Ratio
82.13
3.78 (0.53)
Internal Variance
74.56
2.84 (0.33)
Embedding (mean)
79.67
4.50 (0.79)
Cov. Determinant
66.14
5.68 (0.51)
Embedding (last)
79.19
4.72 (0.86)
Embedding (mean)
63.95
7.22 (0.40)
Attention + MSP
77.82
5.39 (1.33)
Circular Variance
58.38
8.01 (0.43)
Attention
77.39
6.28 (1.52)
Embedding (all)
61.06
8.18 (0.39)
Internal Variance
76.03
6.39 (0.59)
Top-
m
m
Prob.
58.75
8.92 (0.44)
Cov. Determinant
71.74
7.94 (1.03)
Embedding (last)
60.34
9.03 (0.68)
Embedding (all)
76.04
7.97 (0.11)
Max. Seq. Prob.
57.10
9.62 (0.29)
Energy
57.58
10.33 (1.86)
Energy
52.06
10.18 (0.33)
Circular Variance
61.29
10.89 (2.30)
Attention + MSP
56.65
10.71 (0.28)
Layer Top-
m
m
Prob.
67.55
11.14 (1.19)
Layer Top-
m
m
Prob.
55.38
10.98 (0.48)
Top-
m
m
Prob.
63.90
11.78 (1.08)
Lookback Ratio
54.70
11.33 (0.39)
Max. Seq. Prob.
58.49
12.39 (0.51)
CoE-C
51.13
11.50 (0.50)
CoE-R
55.26
12.94 (0.85)
Attention
52.98
11.63 (0.31)
Perplexity
51.07
13.33 (1.58)
CoE-R
47.40
12.13 (0.76)
SATMD + MSP
57.81
14.22 (0.70)
Perplexity
45.81
12.13 (0.30)
SATMD
56.08
14.44 (0.58)
SATMD + MSP
51.48
12.34 (0.15)
CoE-C
49.44
15.50 (0.91)
Entropy
42.12
13.51 (0.16)
Entropy
38.90
16.06 (1.07)
SATMD
45.75
14.04 (0.51)
Table 9:
Transfer summary ranking statistics.
Probe Architecture and Training Size.
Figure
13
and
Figure
14
provide average OOD performance for different probe architectures and effect of probe architecture on ECE, respectively. Higher-capacity probes can improve some weak feature representations, but do not consistently improve transfer performance, supporting our use of linear probes as the default architecture.
Figure
15
presents per-dataset performance with different training set sizes, showing that performance often improves rapidly with limited supervision and achieves a satisfactory level at around 128–256 examples for many feature representations.
Annotator
TriviaQA
SciQ
PopQA
Rouge-1
.684 (85%)
.237 (56%)
.756 (95%)
Rouge-2
.245 (66%)
.069 (32%)
.319 (89%)
Rouge-L
.684 (85%)
.228 (55%)
.756 (95%)
AlignScore
.728 (87%)
.220 (60%)
.756 (95%)
LLM-as-a-judge
.960 (98%)
.820 (94%)
.879 (97%)
Table 10:
Cohen’s kappa (agreement %) for automated labels and human judgement.
LLM-Judge
TriviaQA
SciQ
PopQA
Gemini-3.1-Flash-Lite
.960 (98%)
.820 (94%)
.879 (97%)
GPT-5.4-Mini
.940 (97%)
.702 (90%)
.917 (98%)
Bio (ID)
Artworks
Books
Gemini-3.1-Flash-Lite
.715 (89%)
.153 (91%)
.000 (91%)
GPT-5.4-Mini
.836 (93%)
.627 (93%)
.595 (92%)
Table 11:
Cohen’s kappa (agreement %) between LLM-judge and human labels.
Lexical and LLM-as-a-judge Annotation Validation.
On TriviaQA, SciQ, and PopQA with Qwen-3-8B, we binarise Rouge and AlignScore using a generic decision threshold of 0.5, consistent with prior work
(
Duan et al., 2024
;
Lei et al., 2023
)
.
To assess the fidelity of the automatically generated lexical labels, we randomly select 100 generations from each dataset, and measure agreement of correctness label between the automated scorer and a human annotator.
To obtain gold ground truth labels, we instruct the human annotator to compare the generated answer with the reference answer, and to use web search if a further check is required.
Table
10
presents Cohen’s kappa and percentage of agreed labels between the automated and human scorer.
Furthermore, to assess the reliability of the LLM-as-a-judge labels in
Section
4
, we compare the same subsets from TriviaQA, SciQ, and PopQA, and additionally 105, 113, and 104 claims from Bio (ID), Artworks, and Books passages, against human annotations.
Consistent with findings by
Janiak et al. (2025)
, LLM-as-a-judge aligns much more closely with human judgement than lexical labels, with AlignScore as second-best but still subpar by a large margin.
Due to its high agreement, we utilise LLM-as-a-judge labels as the ground truth.
Between the two LLM-judges, GPT-5.4-Mini shows stronger agreement on the open-ended generation setting, while Gemini-3.1-Flash-Lite remains comparable on the short-answer benchmark datasets.
Gemini’s tendency to label claims as true results in lower Cohen’s
κ
\kappa
, falling to 0 for the Books subset as it labelled all instances as true.
We select the judge according to the annotation regime rather than enforcing the same judge across substantially different tasks.
Thus, we use Gemini labels for the benchmark experiments in
Section
3.4
and GPT-5.4-Mini labels for the open-ended factual generation experiments in
Section
4
.
Figure 16:
Effects of inducing reasoning (Qwen-3-8B).
Figure 17:
Effects of inducing reasoning on StrategyQA and MATH-500.
Figure 18:
Effects of inducing reasoning with Gemma-3-12B-Instruct.
More Reasoning-Eliciting Experiments.
We extend the no-, medium-, and long-reasoning comparison to StrategyQA and MATH-500 using Qwen-3-8B and Gemma-3-12B-Instruct (
Figures
17
and
18
). StrategyQA broadly reproduces the prompt sensitivity observed on ARC and CSQA. On MATH-500, however, reasoning can substantially improve answer accuracy and probe discriminability, in particular, for Gemma, showing that probe performance is prompt-sensitive but not necessarily that reasoning elicitation is intrinsically harmful.
Figure 19:
Effect of answer-token-only aggregation. Values report AUROC difference between answer-token-only and full-trace aggregation.
(a)
Effect of trimming and re-encoding only reasoning or answer spans. Values report AUROC change relative to the original trace.
(b)
Effect of reasoning token aggregation. Values report AUROC difference between reasoning-token-only and full-trace aggregation.
Figure 20:
Reasoning-content and aggregation results.
Reasoning-Content and Aggregation Controls.
We further analyse StrategyQA with Gemma-3-12B-Instruct using two complementary controls. First, Gemini-3.1-Flash-Lite identifies sentences that do not contribute to the reasoning. We exclude these spans and re-encode the prompt and shortened trace before recomputing the features; we also consider an answer-only condition that retains only the final answer (
Figure
20(a)
). This control captures both non-reasoning-content removal and the resulting changes to token context and position.
Second, we retain the original complete trace and its token states, but aggregate features only over the identified reasoning tokens (
Figure
20(b)
) and answer tokens (
Figure
19
). This isolates the aggregation choice without changing the encoded sequence.
Both controls produce mixed, feature-dependent effects. Re-encoding the trimmed trace leads to larger changes for several representations, whereas reasoning-token-only aggregation generally has more modest effects and does occasionally improve performance but not uniformly and is not stable.
Interestingly, answer-token-only aggregation benefits some embedding features but may severely degrade several probability-based features (
Figure
19
).
These results partially support the dilution hypothesis, but indicate that aggregation alone is insufficient: non-reasoning content may also alter the contextual representations from which uncertainty features are extracted.
We caution that these findings should not be over-interpreted. The reasoning-token spans are identified by an auxiliary LLM and may contain classification errors, and both analyses are post-hoc controls over fixed generations rather than causal interventions on the reasoning process. We therefore treat them as diagnostic evidence for reasoning-content- and aggregation-dependent effects, not as establishing a causal mechanism.
Method
Biographies
(ID)
Biographies
(OOD)
Artworks
Books
Cities
Events
Inventions
Landmarks
Movies
OOD
Mean
OOD
Rank
Bio-ID-trained
Linear (#64)
64.83 (
±
\pm
2.04)
60.19 (
±
\pm
2.16)
59.57 (
±
\pm
3.11)
56.87 (
±
\pm
3.57)
54.51 (
±
\pm
2.25)
53.75 (
±
\pm
3.67)
59.56 (
±
\pm
3.03)
58.27 (
±
\pm
2.72)
62.44 (
±
\pm
2.63)
58.14 (
±
\pm
1.04)
16.75
Linear (#128)
72.43 (
±
\pm
2.01)
62.61 (
±
\pm
2.10)
64.89 (
±
\pm
3.01)
53.53 (
±
\pm
3.74)
61.8 (
±
\pm
2.18)
57.22 (
±
\pm
3.91)
60.81 (
±
\pm
3.1)
61.24 (
±
\pm
2.82)
64.45 (
±
\pm
2.47)
60.82 (
±
\pm
1.05)
13.38
MLP (#128)
73.69 (
±
\pm
1.91)
58.65 (
±
\pm
2.14)
62.15 (
±
\pm
2.94)
48.06 (
±
\pm
3.48)
58.97 (
±
\pm
2.24)
54.40 (
±
\pm
3.55)
58.03 (
±
\pm
3.15)
57.51 (
±
\pm
2.59)
60.06 (
±
\pm
2.51)
57.23 (
±
\pm
1.01)
17.13
Linear (#256)
78.15 (
±
\pm
2.06)
64.72 (
±
\pm
2.04)
64.72 (
±
\pm
2.81)
56.30 (
±
\pm
3.55)
64.37 (
±
\pm
2.13)
57.30 (
±
\pm
3.42)
61.63 (
±
\pm
3.19)
61.28 (
±
\pm
2.68)
65.55 (
±
\pm
2.41)
61.98 (
±
\pm
1.00)
12.25
Lookback Ratio
77.06 (
±
\pm
2.15)
63.72 (
±
\pm
2.26)
67.14 (
±
\pm
3.05)
62.53 (
±
\pm
2.97)
67.08 (
±
\pm
2.18)
60.60 (
±
\pm
3.40)
59.73 (
±
\pm
3.11)
63.28 (
±
\pm
2.60)
66.65 (
±
\pm
2.30)
63.84 (
±
\pm
0.98)
9.25
Layer Top-
m
m
Prob.
63.91 (
±
\pm
2.42)
64.10 (
±
\pm
2.22)
57.90 (
±
\pm
3.31)
57.71 (
±
\pm
3.31)
65.62 (
±
\pm
2.20)
52.12 (
±
\pm
3.50)
64.05 (
±
\pm
3.01)
64.39 (
±
\pm
2.64)
72.25 (
±
\pm
2.39)
62.27 (
±
\pm
1.01)
12.63
Internal Variance
71.40 (
±
\pm
2.38)
68.43 (
±
\pm
2.10)
62.31 (
±
\pm
3.39)
60.58 (
±
\pm
3.24)
67.24 (
±
\pm
2.25)
50.96 (
±
\pm
3.67)
65.39 (
±
\pm
3.17)
66.23 (
±
\pm
2.66)
71.35 (
±
\pm
2.41)
64.06 (
±
\pm
1.03)
10.44
Training-free
Max. Seq. Prob.
65.71 (
±
\pm
2.50)
67.70 (
±
\pm
2.12)
66.36 (
±
\pm
3.46)
61.03 (
±
\pm
3.40)
72.07 (
±
\pm
1.99)
56.32 (
±
\pm
3.10)
68.98 (
±
\pm
2.94)
68.54 (
±
\pm
2.49)
73.63 (
±
\pm
2.25)
66.83 (
±
\pm
0.98)
7.25
Entropy
66.91 (
±
\pm
2.48)
68.72 (
±
\pm
2.12)
68.61 (
±
\pm
3.38)
61.68 (
±
\pm
3.38)
72.73 (
±
\pm
1.98)
57.08 (
±
\pm
3.14)
71.02 (
±
\pm
2.86)
69.22 (
±
\pm
2.53)
76.29 (
±
\pm
2.23)
68.17 (
±
\pm
0.97)
4.25
Perplexity
66.12 (
±
\pm
2.48)
68.48 (
±
\pm
2.11)
67.15 (
±
\pm
3.47)
61.26 (
±
\pm
3.41)
72.45 (
±
\pm
2.00)
55.92 (
±
\pm
3.11)
69.14 (
±
\pm
2.94)
68.65 (
±
\pm
2.48)
74.63 (
±
\pm
2.25)
67.21 (
±
\pm
0.98)
6.13
Energy
54.16 (
±
\pm
2.46)
65.59 (
±
\pm
2.23
70.29 (
±
\pm
3.23)
60.74 (
±
\pm
3.29)
73.07 (
±
\pm
1.96)
61.49 (
±
\pm
3.34)
74.06 (
±
\pm
2.70)
65.14 (
±
\pm
2.67)
76.83 (
±
\pm
2.12)
68.40 (
±
\pm
0.97)
4.63
Semantic Entropy
71.85 (
±
\pm
2.27)
61.84 (
±
\pm
2.17)
64.91 (
±
\pm
2.98)
67.44 (
±
\pm
2.96)
68.25 (
±
\pm
2.09)
62.23 (
±
\pm
3.15)
66.78 (
±
\pm
2.90)
72.77 (
±
\pm
2.30)
70.09 (
±
\pm
2.21)
66.79 (
±
\pm
0.93)
6.50
Eigenscore
62.25 (
±
\pm
2.53)
57.73 (
±
\pm
2.25)
58.37 (
±
\pm
3.20)
58.33 (
±
\pm
3.25)
57.24 (
±
\pm
2.37)
48.77 (
±
\pm
3.42)
58.94 (
±
\pm
3.03)
59.92 (
±
\pm
2.73)
68.31 (
±
\pm
2.31)
58.45 (
±
\pm
1.01)
16.50
Pretrained
Embedding (last)
54.85 (
±
\pm
2.42)
60.51 (
±
\pm
2.12)
52.11 (
±
\pm
2.97)
57.17 (
±
\pm
3.39)
54.68 (
±
\pm
2.49)
50.93 (
±
\pm
3.68)
59.29 (
±
\pm
3.08)
61.01 (
±
\pm
2.59)
66.25 (
±
\pm
2.41)
57.74 (
±
\pm
1.02)
16.63
Lookback Ratio
64.02 (
±
\pm
2.32)
61.68 (
±
\pm
2.14)
63.12 (
±
\pm
2.81)
59.87 (
±
\pm
2.97)
58.23 (
±
\pm
2.30)
56.60 (
±
\pm
3.80)
57.08 (
±
\pm
3.20)
62.72 (
±
\pm
2.44)
71.97 (
±
\pm
2.31)
61.41 (
±
\pm
0.99)
13.38
Layer Top-
m
m
Prob.
66.16 (
±
\pm
2.26)
68.60 (
±
\pm
1.99)
66.44 (
±
\pm
3.07)
64.11 (
±
\pm
3.56)
66.48 (
±
\pm
2.14)
61.77 (
±
\pm
3.29)
72.96 (
±
\pm
3.03)
69.31 (
±
\pm
2.48)
80.14 (
±
\pm
1.93)
68.73 (
±
\pm
0.97)
3.88
Internal Variance
67.27 (
±
\pm
2.27)
70.19 (
±
\pm
1.96)
68.49 (
±
\pm
2.96)
64.46 (
±
\pm
3.34)
67.24 (
±
\pm
2.09)
59.28 (
±
\pm
3.48)
69.90 (
±
\pm
3.12)
67.74 (
±
\pm
2.57)
77.80 (
±
\pm
2.05)
68.14 (
±
\pm
0.97)
4.31
Ensemble (probe)
73.76 (
±
\pm
2.03)
70.18 (
±
\pm
2.00)
63.72 (
±
\pm
3.20)
58.88 (
±
\pm
3.42)
65.67 (
±
\pm
2.26)
55.00 (
±
\pm
3.57)
68.08 (
±
\pm
3.36)
64.46 (
±
\pm
2.76)
73.17 (
±
\pm
2.43)
64.90 (
±
\pm
1.04)
9.50
Ensemble (task)
68.38 (
±
\pm
2.27)
70.85 (
±
\pm
1.86)
65.38 (
±
\pm
3.02)
64.53 (
±
\pm
3.25)
63.44 (
±
\pm
2.24)
56.79 (
±
\pm
3.64)
70.23 (
±
\pm
3.06)
69.25 (
±
\pm
2.46)
77.93 (
±
\pm
2.03)
67.30 (
±
\pm
0.98)
5.25
Table 12:
AUROC with bootstrapped standard errors (Qwen-3-8B). Baselines are indicated with probe architecture and number of training examples from Biographies (ID).
Method
Biographies
(ID)
Biographies
(OOD)
Artworks
Books
Cities
Events
Inventions
Landmarks
Movies
OOD
Mean
OOD
Rank
Bio-ID-trained
Embedding (last)
74.08 (
±
\pm
1.86)
55.92 (
±
\pm
2.64)
55.47 (
±
\pm
3.14)
68.40 (
±
\pm
4.95)
60.60 (
±
\pm
2.74)
52.78 (
±
\pm
4.77)
64.38 (
±
\pm
3.43)
53.97 (
±
\pm
3.75)
63.47 (
±
\pm
4.32)
59.37 (
±
\pm
1.35)
9.50
Lookback Ratio
75.62 (
±
\pm
1.90)
53.41 (
±
\pm
2.63)
61.96 (
±
\pm
3.21)
46.69 (
±
\pm
5.31)
56.53 (
±
\pm
3.10)
53.51 (
±
\pm
5.36)
51.92 (
±
\pm
4.18)
52.39 (
±
\pm
3.91)
61.94 (
±
\pm
4.17)
54.79 (
±
\pm
1.45)
12.13
Layer Top-
m
m
Prob.
63.80 (
±
\pm
2.23)
60.19 (
±
\pm
2.45)
51.70 (
±
\pm
3.34)
43.25 (
±
\pm
5.56)
57.28 (
±
\pm
2.81)
55.81 (
±
\pm
4.72)
72.62 (
±
\pm
3.02)
49.44 (
±
\pm
3.80)
57.43 (
±
\pm
4.01)
55.97 (
±
\pm
1.36)
11.88
Internal Variance
69.30 (
±
\pm
2.06)
61.34 (
±
\pm
2.58)
55.97 (
±
\pm
3.44)
51.30 (
±
\pm
4.68)
60.13 (
±
\pm
2.58)
54.44 (
±
\pm
4.87)
68.96 (
±
\pm
3.29)
54.36 (
±
\pm
3.54)
60.65 (
±
\pm
4.02)
58.39 (
±
\pm
1.31)
10.25
Training-free
Max. Seq. Prob.
67.24 (
±
\pm
2.15)
62.09 (
±
\pm
2.56)
56.38 (
±
\pm
3.36)
52.12 (
±
\pm
4.55)
60.34 (
±
\pm
2.58)
58.05 (
±
\pm
4.16)
69.53 (
±
\pm
3.24)
56.50 (
±
\pm
3.66)
62.38 (
±
\pm
3.49)
59.67 (
±
\pm
1.24)
7.50
Entropy
69.09 (
±
\pm
2.09)
62.67 (
±
\pm
2.59)
57.31 (
±
\pm
3.40)
52.35 (
±
\pm
4.54)
60.72 (
±
\pm
2.57)
59.00 (
±
\pm
4.38)
72.40 (
±
\pm
3.05)
56.44 (
±
\pm
3.69)
63.84 (
±
\pm
3.55)
60.59 (
±
\pm
1.25)
5.00
Perplexity
67.31 (
±
\pm
2.15)
61.84 (
±
\pm
2.56)
56.18 (
±
\pm
3.36)
52.40 (
±
\pm
4.66)
60.46 (
±
\pm
2.61)
58.49 (
±
\pm
4.22)
69.59 (
±
\pm
3.24)
56.42 (
±
\pm
3.67)
62.27 (
±
\pm
3.52)
59.71 (
±
\pm
1.25)
7.50
Energy
66.73 (
±
\pm
2.17)
57.64 (
±
\pm
2.52)
57.46 (
±
\pm
3.21)
66.46 (
±
\pm
4.76)
62.10 (
±
\pm
2.80)
59.66 (
±
\pm
4.67)
67.12 (
±
\pm
3.58)
66.85 (
±
\pm
3.54)
63.98 (
±
\pm
3.88)
62.66 (
±
\pm
1.31)
4.75
Semantic Entropy
72.55 (
±
\pm
1.96)
59.32 (
±
\pm
2.40)
56.73 (
±
\pm
3.17)
58.34 (
±
\pm
5.00)
66.70 (
±
\pm
2.45)
58.41 (
±
\pm
4.47)
67.33 (
±
\pm
3.42)
61.21 (
±
\pm
3.43)
72.71 (
±
\pm
3.55)
62.59 (
±
\pm
1.27)
5.25
Eigenscore
65.21 (
±
\pm
1.94)
58.04 (
±
\pm
2.39)
55.02 (
±
\pm
3.00)
50.66 (
±
\pm
4.79)
57.47 (
±
\pm
2.71)
49.79 (
±
\pm
4.51)
59.56 (
±
\pm
3.44)
52.60 (
±
\pm
3.39)
60.00 (
±
\pm
4.19)
55.39 (
±
\pm
1.29)
13.25
Pretrained
Embedding (last)
55.83 (
±
\pm
2.04)
51.99 (
±
\pm
2.43)
60.80 (
±
\pm
3.26)
56.11 (
±
\pm
5.51)
53.09 (
±
\pm
2.76)
58.09 (
±
\pm
4.78)
63.75 (
±
\pm
3.40)
58.28 (
±
\pm
3.77)
67.31 (
±
\pm
3.85)
58.68 (
±
\pm
1.36)
8.00
Lookback Ratio
60.30 (
±
\pm
1.89)
50.34 (
±
\pm
2.64)
49.78 (
±
\pm
3.29)
50.13 (
±
\pm
5.51)
49.29 (
±
\pm
2.84)
43.85 (
±
\pm
4.87)
48.75 (
±
\pm
3.77)
48.65 (
±
\pm
3.77)
48.07 (
±
\pm
3.86)
48.61 (
±
\pm
1.39)
15.75
Layer Top-
m
m
Prob.
71.13 (
±
\pm
1.71)
61.37 (
±
\pm
2.55)
56.92 (
±
\pm
3.40)
53.81 (
±
\pm
4.45)
59.90 (
±
\pm
2.60)
61.34 (
±
\pm
4.33)
71.74 (
±
\pm
2.95)
56.72 (
±
\pm
3.63)
63.05 (
±
\pm
3.69)
60.61 (
±
\pm
1.24)
5.88
Internal Variance
70.95 (
±
\pm
1.70)
61.87 (
±
\pm
2.59)
56.27 (
±
\pm
3.41)
51.28 (
±
\pm
4.72)
60.76 (
±
\pm
2.53)
55.04 (
±
\pm
4.69)
69.79 (
±
\pm
3.22)
56.14 (
±
\pm
3.48)
61.52 (
±
\pm
3.90)
59.08 (
±
\pm
1.29)
8.25
Ensemble (Probe)
70.20 (
±
\pm
1.72)
61.45 (
±
\pm
2.61)
57.45 (
±
\pm
3.41)
52.42 (
±
\pm
4.23)
59.92 (
±
\pm
2.64)
59.07 (
±
\pm
4.65)
71.76 (
±
\pm
3.08)
54.00 (
±
\pm
3.68)
63.10 (
±
\pm
3.78)
59.90 (
±
\pm
1.26)
6.50
Ensemble (Task)
70.31 (
±
\pm
1.81)
60.50 (
±
\pm
2.56)
61.38 (
±
\pm
3.30)
53.53 (
±
\pm
4.78)
57.77 (
±
\pm
2.59)
59.65 (
±
\pm
4.34)
72.67 (
±
\pm
3.11)
59.90 (
±
\pm
3.48)
66.36 (
±
\pm
3.45)
61.47 (
±
\pm
1.25)
4.63
Table 13:
AUROC with bootstrapped standard errors (Gemma-3-12B-Instruct).
Method
Biographies
(ID)
Biographies
(OOD)
Artworks
Books
Cities
Events
Inventions
Landmarks
Movies
OOD
Mean
OOD
Rank
Bio-ID-trained
Embedding (last)
66.11 (
±
\pm
2.38)
55.66 (
±
\pm
2.31)
59.63 (
±
\pm
2.83)
54.12 (
±
\pm
3.11)
59.57 (
±
\pm
2.41)
53.85 (
±
\pm
3.03)
55.53 (
±
\pm
2.47)
54.20 (
±
\pm
2.55)
57.02 (
±
\pm
2.76)
56.20 (
±
\pm
0.95)
14.44
Lookback Ratio
70.26 (
±
\pm
2.23)
63.62 (
±
\pm
2.16)
69.13 (
±
\pm
2.73)
58.16 (
±
\pm
3.02)
66.48 (
±
\pm
2.19)
55.99 (
±
\pm
2.83)
62.93 (
±
\pm
2.44)
64.58 (
±
\pm
2.22)
70.47 (
±
\pm
2.37)
63.92 (
±
\pm
0.89)
8.12
Layer Top-
m
m
Prob.
64.45 (
±
\pm
2.50)
56.17 (
±
\pm
2.33)
51.26 (
±
\pm
3.32)
54.04 (
±
\pm
3.19)
51.44 (
±
\pm
2.35)
46.80 (
±
\pm
3.14)
59.20 (
±
\pm
2.55)
51.70 (
±
\pm
2.86)
62.97 (
±
\pm
3.07)
54.20 (
±
\pm
1.02)
14.88
Internal Variance
77.40 (
±
\pm
2.02)
64.87 (
±
\pm
2.08)
61.51 (
±
\pm
3.15)
61.18 (
±
\pm
3.10)
69.38 (
±
\pm
2.22)
59.85 (
±
\pm
3.32)
69.01 (
±
\pm
2.37)
65.99 (
±
\pm
2.40)
76.86 (
±
\pm
2.41)
66.08 (
±
\pm
0.94)
5.12
Training-free
Max. Seq. Prob.
75.39 (
±
\pm
2.04)
63.53 (
±
\pm
2.00)
64.52 (
±
\pm
2.68)
59.12 (
±
\pm
3.21)
67.34 (
±
\pm
2.19)
59.49 (
±
\pm
3.17)
69.25 (
±
\pm
2.21)
63.25 (
±
\pm
2.47)
70.43 (
±
\pm
2.72)
64.62 (
±
\pm
0.92)
7.25
Entropy
75.58 (
±
\pm
2.04)
65.10 (
±
\pm
2.01)
66.75 (
±
\pm
2.66)
60.90 (
±
\pm
3.27)
68.73 (
±
\pm
2.19)
59.24 (
±
\pm
3.23)
70.70 (
±
\pm
2.22)
65.14 (
±
\pm
2.48)
72.73 (
±
\pm
2.65)
66.16 (
±
\pm
0.93)
4.50
Perplexity
75.25 (
±
\pm
2.03)
64.40 (
±
\pm
2.01)
64.43 (
±
\pm
2.73)
59.51 (
±
\pm
3.18)
67.55 (
±
\pm
2.20)
60.20 (
±
\pm
3.20)
69.21 (
±
\pm
2.21)
63.21 (
±
\pm
2.48)
70.98 (
±
\pm
2.70)
64.94 (
±
\pm
0.93)
6.44
Energy
72.03 (
±
\pm
2.22)
60.01 (
±
\pm
2.13)
62.36 (
±
\pm
2.97)
56.42 (
±
\pm
3.23)
67.30 (
±
\pm
2.21)
54.86 (
±
\pm
3.23)
70.07 (
±
\pm
2.25)
54.20 (
±
\pm
2.63)
67.49 (
±
\pm
2.88)
61.59 (
±
\pm
0.96)
10.69
Semantic Entropy
69.17 (
±
\pm
2.27)
68.16 (
±
\pm
2.02)
63.79 (
±
\pm
2.82)
59.35 (
±
\pm
2.72)
66.40 (
±
\pm
2.24)
59.09 (
±
\pm
2.82)
60.67 (
±
\pm
2.43)
59.83 (
±
\pm
2.56)
69.81 (
±
\pm
2.45)
63.39 (
±
\pm
0.89)
8.62
Eigenscore
66.81 (
±
\pm
2.25)
65.57 (
±
\pm
2.15)
63.96 (
±
\pm
2.77)
58.58 (
±
\pm
2.93)
63.73 (
±
\pm
2.26)
52.32 (
±
\pm
2.97)
62.65 (
±
\pm
2.53)
55.50 (
±
\pm
2.48)
68.97 (
±
\pm
2.42)
61.41 (
±
\pm
0.91)
10.50
Pretrained
Embedding (last)
55.09 (
±
\pm
2.54)
52.95 (
±
\pm
2.32)
46.70 (
±
\pm
3.22)
52.82 (
±
\pm
2.93)
60.08 (
±
\pm
2.32)
54.01 (
±
\pm
3.29)
56.94 (
±
\pm
2.55)
58.07 (
±
\pm
2.55)
59.02 (
±
\pm
2.77)
55.07 (
±
\pm
0.98)
14.38
Lookback Ratio
62.63 (
±
\pm
2.38)
67.40 (
±
\pm
1.91)
66.13 (
±
\pm
2.75)
62.03 (
±
\pm
3.01)
54.74 (
±
\pm
2.34)
55.45 (
±
\pm
2.86)
50.63 (
±
\pm
2.51)
65.61 (
±
\pm
2.25)
75.23 (
±
\pm
2.49)
62.15 (
±
\pm
0.90)
7.25
Layer Top-
m
m
Prob.
71.06 (
±
\pm
2.21)
60.45 (
±
\pm
2.17)
58.02 (
±
\pm
3.10)
56.55 (
±
\pm
3.24)
64.87 (
±
\pm
2.19)
57.23 (
±
\pm
2.93)
62.75 (
±
\pm
2.40)
60.83 (
±
\pm
2.60)
66.09 (
±
\pm
3.00)
60.85 (
±
\pm
0.97)
11.38
Internal Variance
77.50 (
±
\pm
2.02)
64.92 (
±
\pm
2.08)
60.94 (
±
\pm
3.13)
61.50 (
±
\pm
3.07)
69.20 (
±
\pm
2.24)
60.38 (
±
\pm
3.31)
69.04 (
±
\pm
2.38)
65.86 (
±
\pm
2.40)
75.84 (
±
\pm
2.53)
65.96 (
±
\pm
0.95)
4.88
Ensemble (probe)
77.16 (
±
\pm
1.99)
64.99 (
±
\pm
2.02)
64.23 (
±
\pm
2.93)
62.18 (
±
\pm
3.13)
69.55 (
±
\pm
2.20)
60.20 (
±
\pm
3.26)
70.21 (
±
\pm
2.29)
66.05 (
±
\pm
2.45)
73.99 (
±
\pm
2.62)
66.43 (
±
\pm
0.94)
3.31
Ensemble (task)
75.64 (
±
\pm
2.06)
65.74 (
±
\pm
1.96)
64.88 (
±
\pm
2.74)
62.84 (
±
\pm
2.96)
68.71 (
±
\pm
2.14)
59.17 (
±
\pm
3.05)
66.75 (
±
\pm
2.33)
67.29 (
±
\pm
2.30)
72.75 (
±
\pm
2.57)
66.02 (
±
\pm
0.90)
4.25
Table 14:
AUROC with bootstrapped standard errors (Llama-3.1-8B-Instruct).
Probe
Biographies
(ID)
Biographies
(OOD)
Artworks
Books
Cities
Events
Inventions
Landmarks
Movies
OOD
Mean
Surrogate: Qwen3-4B-Instruct
Bio-ID-trained
Embedding (Last)
75.48 (
±
\pm
2.19)
59.14 (
±
\pm
2.33)
56.75 (
±
\pm
3.27)
60.36 (
±
\pm
3.29)
57.86 (
±
\pm
2.23)
54.91 (
±
\pm
3.30)
57.33 (
±
\pm
2.89)
66.08 (
±
\pm
2.75)
68.05 (
±
\pm
2.14)
60.06 (
±
\pm
0.99)
Lookback Ratio
77.65 (
±
\pm
2.17)
65.14 (
±
\pm
2.17)
61.50 (
±
\pm
2.97)
62.05 (
±
\pm
3.15)
69.03 (
±
\pm
1.98)
57.75 (
±
\pm
3.44)
62.57 (
±
\pm
3.10)
65.88 (
±
\pm
2.42)
68.36 (
±
\pm
2.31)
64.03 (
±
\pm
0.97)
Layer Top-
m
m
Prob.
66.40 (
±
\pm
2.50)
64.40 (
±
\pm
2.21)
59.53 (
±
\pm
3.26)
49.50 (
±
\pm
3.32)
60.34 (
±
\pm
2.21)
57.92 (
±
\pm
3.43)
63.15 (
±
\pm
3.03)
62.33 (
±
\pm
2.63)
70.18 (
±
\pm
2.23)
60.92 (
±
\pm
1.00)
Internal Variance
70.36 (
±
\pm
2.39)
66.72 (
±
\pm
2.15)
61.88 (
±
\pm
3.37)
61.20 (
±
\pm
3.28)
68.77 (
±
\pm
2.07)
58.49 (
±
\pm
3.29)
72.69 (
±
\pm
2.84)
67.70 (
±
\pm
2.59)
72.64 (
±
\pm
2.42)
66.26 (
±
\pm
0.99)
Pretrained
Embedding (Last)
52.63 (
±
\pm
2.73)
57.41 (
±
\pm
2.30)
60.79 (
±
\pm
3.16)
62.35 (
±
\pm
3.53)
58.39 (
±
\pm
2.35)
52.43 (
±
\pm
3.67)
64.18 (
±
\pm
2.91)
57.77 (
±
\pm
2.89)
64.84 (
±
\pm
2.39)
59.77 (
±
\pm
1.04)
Lookback Ratio
71.13 (
±
\pm
2.45)
63.87 (
±
\pm
2.20)
70.96 (
±
\pm
3.00)
58.71 (
±
\pm
2.96)
65.59 (
±
\pm
2.14)
55.74 (
±
\pm
3.49)
70.03 (
±
\pm
2.80)
68.45 (
±
\pm
2.35)
73.70 (
±
\pm
2.23)
65.88 (
±
\pm
0.95)
Layer Top-
m
m
Prob.
64.18 (
±
\pm
2.54)
63.92 (
±
\pm
2.23)
71.85 (
±
\pm
2.90)
62.70 (
±
\pm
3.08)
68.40 (
±
\pm
2.09)
58.23 (
±
\pm
3.31)
72.48 (
±
\pm
3.02)
67.81 (
±
\pm
2.57)
76.68 (
±
\pm
2.15)
67.76 (
±
\pm
0.96)
Internal Variance
65.60 (
±
\pm
2.49)
66.94 (
±
\pm
2.16)
68.01 (
±
\pm
3.04)
62.57 (
±
\pm
3.26)
70.74 (
±
\pm
2.02)
58.77 (
±
\pm
3.30)
73.21 (
±
\pm
3.00)
69.65 (
±
\pm
2.55)
79.31 (
±
\pm
1.99)
68.65 (
±
\pm
0.96)
Ensemble (Probe)
67.34 (
±
\pm
2.47)
67.75 (
±
\pm
2.13)
65.81 (
±
\pm
3.32)
63.46 (
±
\pm
3.31)
70.92 (
±
\pm
2.00)
62.30 (
±
\pm
3.17)
74.24 (
±
\pm
2.92)
68.80 (
±
\pm
2.58)
76.68 (
±
\pm
2.34)
68.75 (
±
\pm
0.98)
Ensemble (Task)
67.16 (
±
\pm
2.52)
67.57 (
±
\pm
2.12)
71.35 (
±
\pm
2.75)
64.00 (
±
\pm
3.11)
70.49 (
±
\pm
2.02)
58.46 (
±
\pm
3.36)
73.92 (
±
\pm
2.94)
70.82 (
±
\pm
2.38)
78.80 (
±
\pm
2.07)
69.43 (
±
\pm
0.93)
Surrogate: Gemma-3-12B-Instruct
Bio-ID-trained
Embedding (Last)
75.13 (
±
\pm
2.29)
61.31 (
±
\pm
2.21)
58.32 (
±
\pm
3.24)
59.24 (
±
\pm
3.19)
62.95 (
±
\pm
2.20)
57.34 (
±
\pm
3.46)
64.27 (
±
\pm
3.13)
66.64 (
±
\pm
2.55)
70.02 (
±
\pm
2.25)
62.51 (
±
\pm
1.00)
Lookback Ratio
75.41 (
±
\pm
2.15)
57.79 (
±
\pm
2.32)
52.11 (
±
\pm
3.67)
55.67 (
±
\pm
3.02)
61.85 (
±
\pm
2.32)
49.10 (
±
\pm
3.60)
52.00 (
±
\pm
3.69)
58.73 (
±
\pm
2.76)
50.83 (
±
\pm
2.76)
54.76 (
±
\pm
1.08)
Layer Top-
m
m
Prob.
64.25 (
±
\pm
2.49)
64.66 (
±
\pm
2.25)
55.01 (
±
\pm
3.51)
55.81 (
±
\pm
3.15)
63.97 (
±
\pm
2.22)
59.48 (
±
\pm
3.37)
63.79 (
±
\pm
2.98)
61.63 (
±
\pm
2.80)
61.60 (
±
\pm
2.54)
60.74 (
±
\pm
1.02)
Internal Variance
69.92 (
±
\pm
2.37)
64.91 (
±
\pm
2.21)
62.26 (
±
\pm
3.33)
58.38 (
±
\pm
3.31)
69.57 (
±
\pm
2.06)
54.61 (
±
\pm
3.29)
65.86 (
±
\pm
2.97)
63.49 (
±
\pm
2.83)
70.17 (
±
\pm
2.27)
63.66 (
±
\pm
1.00)
Pretrained
Embedding (Last)
56.85 (
±
\pm
2.51)
55.24 (
±
\pm
2.34)
53.55 (
±
\pm
3.44)
55.15 (
±
\pm
3.39)
57.70 (
±
\pm
2.28)
55.29 (
±
\pm
3.47)
61.28 (
±
\pm
3.25)
59.55 (
±
\pm
2.49)
67.94 (
±
\pm
2.21)
58.21 (
±
\pm
1.03)
Lookback Ratio
55.83 (
±
\pm
2.60)
47.61 (
±
\pm
2.37)
42.83 (
±
\pm
3.58)
48.28 (
±
\pm
3.00)
48.43 (
±
\pm
2.24)
46.46 (
±
\pm
3.46)
40.30 (
±
\pm
3.16)
43.27 (
±
\pm
2.69)
35.21 (
±
\pm
2.61)
44.05 (
±
\pm
1.03)
Layer Top-
m
m
Prob.
68.65 (
±
\pm
2.42)
65.59 (
±
\pm
2.17)
62.49 (
±
\pm
3.47)
59.44 (
±
\pm
3.34)
70.21 (
±
\pm
2.06)
55.43 (
±
\pm
3.35)
66.97 (
±
\pm
2.88)
64.23 (
±
\pm
2.74)
69.57 (
±
\pm
2.27)
64.24 (
±
\pm
1.00)
Internal Variance
70.23 (
±
\pm
2.36)
65.50 (
±
\pm
2.16)
62.43 (
±
\pm
3.37)
58.90 (
±
\pm
3.27)
70.03 (
±
\pm
2.07)
55.47 (
±
\pm
3.30)
66.59 (
±
\pm
2.95)
64.91 (
±
\pm
2.77)
70.14 (
±
\pm
2.27)
64.25 (
±
\pm
1.00)
Ensemble (Probe)
68.62 (
±
\pm
2.36)
64.11 (
±
\pm
2.22)
62.37 (
±
\pm
3.45)
59.50 (
±
\pm
3.33)
70.60 (
±
\pm
2.01)
53.55 (
±
\pm
3.40)
66.30 (
±
\pm
2.96)
64.78 (
±
\pm
2.80)
70.19 (
±
\pm
2.29)
63.92 (
±
\pm
1.01)
Ensemble (Task)
67.33 (
±
\pm
2.35)
64.09 (
±
\pm
2.18)
62.25 (
±
\pm
3.38)
56.75 (
±
\pm
3.32)
67.75 (
±
\pm
1.97)
55.31 (
±
\pm
3.25)
63.63 (
±
\pm
2.81)
62.75 (
±
\pm
2.75)
65.49 (
±
\pm
2.22)
62.25 (
±
\pm
0.98)
Table 15:
Surrogate-model AUROC with bootstrapped standard errors. Text and atomic claims are generated by Qwen3-8B, while probe features are extracted
post hoc using the indicated model.
Probe
Biographies
(ID)
Biographies
(OOD)
Artworks
Books
Cities
Events
Inventions
Landmarks
Movies
OOD
Mean
Surrogate: Qwen3-4B-Instruct
Bio-ID-trained
Embedding (Last)
70.65 (
±
\pm
1.95)
57.88 (
±
\pm
2.63)
56.35 (
±
\pm
3.22)
71.45 (
±
\pm
3.65)
55.23 (
±
\pm
2.75)
51.53 (
±
\pm
5.10)
69.13 (
±
\pm
3.28)
59.39 (
±
\pm
3.60)
62.36 (
±
\pm
3.62)
60.41 (
±
\pm
1.26)
Lookback Ratio
76.09 (
±
\pm
1.88)
53.64 (
±
\pm
2.58)
59.48 (
±
\pm
3.03)
49.65 (
±
\pm
5.15)
56.58 (
±
\pm
2.73)
56.61 (
±
\pm
4.79)
67.66 (
±
\pm
3.39)
54.17 (
±
\pm
3.72)
56.53 (
±
\pm
4.19)
56.79 (
±
\pm
1.34)
Layer Top-
m
m
Prob.
62.73 (
±
\pm
2.19)
58.30 (
±
\pm
2.51)
47.35 (
±
\pm
3.16)
54.58 (
±
\pm
5.00)
50.51 (
±
\pm
2.82)
54.09 (
±
\pm
4.53)
58.27 (
±
\pm
3.51)
54.22 (
±
\pm
3.90)
52.84 (
±
\pm
3.83)
53.77 (
±
\pm
1.32)
Internal Variance
70.21 (
±
\pm
2.07)
62.53 (
±
\pm
2.70)
56.19 (
±
\pm
3.34)
56.87 (
±
\pm
5.18)
61.60 (
±
\pm
2.61)
60.01 (
±
\pm
4.45)
74.69 (
±
\pm
3.27)
58.52 (
±
\pm
3.57)
67.91 (
±
\pm
3.46)
62.29 (
±
\pm
1.29)
Pretrained
Embedding (Last)
53.55 (
±
\pm
2.32)
52.93 (
±
\pm
2.76)
58.21 (
±
\pm
3.00)
59.29 (
±
\pm
5.60)
60.15 (
±
\pm
2.89)
53.91 (
±
\pm
4.35)
56.28 (
±
\pm
3.91)
59.53 (
±
\pm
3.32)
58.61 (
±
\pm
3.64)
57.36 (
±
\pm
1.34)
Lookback Ratio
65.37 (
±
\pm
2.18)
55.02 (
±
\pm
2.61)
63.03 (
±
\pm
3.02)
62.14 (
±
\pm
5.84)
61.92 (
±
\pm
2.64)
61.07 (
±
\pm
5.13)
63.39 (
±
\pm
3.42)
64.98 (
±
\pm
3.49)
58.13 (
±
\pm
4.32)
61.21 (
±
\pm
1.40)
Layer Top-
m
m
Prob.
63.30 (
±
\pm
2.22)
58.12 (
±
\pm
2.59)
55.15 (
±
\pm
3.33)
57.93 (
±
\pm
5.34)
60.78 (
±
\pm
2.62)
60.93 (
±
\pm
4.29)
75.96 (
±
\pm
2.83)
60.89 (
±
\pm
3.48)
63.33 (
±
\pm
4.15)
61.64 (
±
\pm
1.30)
Internal Variance
63.38 (
±
\pm
2.20)
60.00 (
±
\pm
2.57)
57.56 (
±
\pm
3.20)
60.17 (
±
\pm
5.92)
63.90 (
±
\pm
2.58)
62.00 (
±
\pm
4.42)
75.74 (
±
\pm
3.12)
59.98 (
±
\pm
3.62)
63.64 (
±
\pm
4.22)
62.87 (
±
\pm
1.36)
Ensemble (Probe)
66.04 (
±
\pm
2.19)
60.83 (
±
\pm
2.70)
57.04 (
±
\pm
3.37)
54.20 (
±
\pm
5.47)
63.76 (
±
\pm
2.59)
58.64 (
±
\pm
4.49)
74.61 (
±
\pm
3.39)
60.95 (
±
\pm
3.56)
66.27 (
±
\pm
3.90)
62.04 (
±
\pm
1.34)
Ensemble (Task)
64.23 (
±
\pm
2.21)
59.93 (
±
\pm
2.61)
57.95 (
±
\pm
3.12)
60.41 (
±
\pm
5.13)
63.34 (
±
\pm
2.56)
61.94 (
±
\pm
4.43)
76.03 (
±
\pm
2.96)
60.78 (
±
\pm
3.52)
63.07 (
±
\pm
4.38)
62.93 (
±
\pm
1.31)
Surrogate: Qwen3-8B
Bio-ID-trained
Embedding (Last)
70.02 (
±
\pm
1.96)
58.20 (
±
\pm
2.55)
51.97 (
±
\pm
3.15)
62.95 (
±
\pm
3.76)
47.96 (
±
\pm
2.86)
58.96 (
±
\pm
4.60)
64.14 (
±
\pm
3.10)
57.87 (
±
\pm
3.29)
50.67 (
±
\pm
4.05)
56.59 (
±
\pm
1.23)
Lookback Ratio
73.02 (
±
\pm
2.03)
52.29 (
±
\pm
2.63)
54.91 (
±
\pm
3.34)
44.80 (
±
\pm
4.73)
60.68 (
±
\pm
2.79)
53.91 (
±
\pm
5.08)
57.54 (
±
\pm
3.40)
51.76 (
±
\pm
3.59)
57.40 (
±
\pm
3.82)
54.16 (
±
\pm
1.33)
Layer Top-
m
m
Prob.
56.63 (
±
\pm
2.28)
53.98 (
±
\pm
2.59)
51.73 (
±
\pm
3.49)
49.85 (
±
\pm
6.16)
56.34 (
±
\pm
2.83)
54.91 (
±
\pm
4.65)
57.15 (
±
\pm
3.56)
48.80 (
±
\pm
3.81)
52.04 (
±
\pm
4.00)
53.10 (
±
\pm
1.42)
Internal Variance
71.08 (
±
\pm
2.07)
61.75 (
±
\pm
2.84)
56.61 (
±
\pm
3.36)
54.57 (
±
\pm
5.24)
59.07 (
±
\pm
2.72)
59.26 (
±
\pm
4.52)
70.83 (
±
\pm
3.47)
63.08 (
±
\pm
3.34)
68.34 (
±
\pm
3.74)
61.69 (
±
\pm
1.32)
Pretrained
Embedding (Last)
49.35 (
±
\pm
2.44)
57.13 (
±
\pm
2.47)
47.42 (
±
\pm
2.98)
53.61 (
±
\pm
4.76)
56.63 (
±
\pm
2.83)
63.10 (
±
\pm
4.78)
57.60 (
±
\pm
3.64)
55.46 (
±
\pm
3.56)
55.96 (
±
\pm
4.32)
55.86 (
±
\pm
1.33)
Lookback Ratio
60.62 (
±
\pm
2.30)
56.31 (
±
\pm
2.62)
61.71 (
±
\pm
2.93)
57.91 (
±
\pm
5.86)
57.56 (
±
\pm
2.87)
54.48 (
±
\pm
5.21)
51.98 (
±
\pm
3.63)
58.69 (
±
\pm
3.59)
58.90 (
±
\pm
4.25)
57.19 (
±
\pm
1.42)
Layer Top-
m
m
Prob.
59.74 (
±
\pm
2.24)
60.58 (
±
\pm
2.49)
58.28 (
±
\pm
3.29)
58.83 (
±
\pm
4.59)
61.96 (
±
\pm
2.56)
54.90 (
±
\pm
5.23)
77.27 (
±
\pm
2.86)
65.90 (
±
\pm
3.28)
66.17 (
±
\pm
4.02)
62.99 (
±
\pm
1.29)
Internal Variance
65.96 (
±
\pm
2.15)
59.25 (
±
\pm
2.67)
58.05 (
±
\pm
3.35)
55.34 (
±
\pm
5.37)
61.29 (
±
\pm
2.64)
57.60 (
±
\pm
4.65)
71.22 (
±
\pm
3.35)
63.26 (
±
\pm
3.53)
67.54 (
±
\pm
3.70)
61.69 (
±
\pm
1.33)
Ensemble (Probe)
70.37 (
±
\pm
2.11)
61.54 (
±
\pm
2.88)
56.95 (
±
\pm
3.40)
53.39 (
±
\pm
4.88)
60.00 (
±
\pm
2.71)
57.22 (
±
\pm
4.49)
71.04 (
±
\pm
3.61)
63.78 (
±
\pm
3.33)
67.10 (
±
\pm
3.53)
61.38 (
±
\pm
1.30)
Ensemble (Task)
63.29 (
±
\pm
2.22)
62.04 (
±
\pm
2.54)
60.85 (
±
\pm
3.15)
58.33 (
±
\pm
5.17)
62.89 (
±
\pm
2.61)
54.00 (
±
\pm
4.91)
70.72 (
±
\pm
3.47)
64.71 (
±
\pm
3.48)
66.66 (
±
\pm
4.25)
62.52 (
±
\pm
1.35)
Table 16:
Surrogate-model AUROC with bootstrapped standard errors. Text and atomic claims are generated by Gemma-3-12B-Instruct, while probe features are extracted post hoc using the indicated surrogate model.
Surrogate-Model Experiment: The Generator and Detector Can Be Decoupled.
The surrogate-model experiments in
Tables
15
and
16
show that features extracted post hoc from a separate model can remain competitive with generator-native features, and occasionally perform better. However, performance varies across surrogate–feature combinations, indicating that surrogate compatibility matters. These results suggest that probe-based factuality estimation can extend to black-box generators using an accessible white-box surrogate, though robustness of the surrogate and generator-surrogate compatibility remain future work.
Query
Response
Qwen3-8B
Biographies (ID)
Tell me a paragraph bio of Gemma Arterton.
…she gained international recognition for her role as the Bond girl in
Quantum of Solace (2008)
[
𝐒
:
0.01
\mathrm{S}:0.01
,
𝐋
:
0.75
\mathrm{L}:0.75
,
ℰ
:
0.75
\mathcal{E}:0.75
]
, which launched her career in Hollywood. Over the years, she has appeared in a variety of films, including
The Golden Compass (2007)
[
𝐒
:
0.01
\mathrm{S}:0.01
,
𝐋
:
0.06
\mathrm{L}:0.06
,
ℰ
:
0.36
\mathcal{E}:0.36
]
,
Tinker Tailor Soldier Spy (2011)
[
𝐒
:
0.95
\mathrm{S}:0.95
,
𝐋
:
0.22
\mathrm{L}:0.22
,
ℰ
:
0.33
\mathcal{E}:0.33
]
, …
Inventions
Tell me about the invention of WiFi and its inventor.
…WiFi technology is based on
the IEEE 802.11 standards, which were developed by the Institute of Electrical and Electronics Engineers (IEEE)
[
𝐒
:
0.04
\mathrm{S}:0.04
,
𝐋
:
0.59
\mathrm{L}:0.59
,
ℰ
:
0.57
\mathcal{E}:0.57
]
…
However,
the inventor most commonly associated with WiFi is Victor W. Grantham
[
𝐒
:
0.30
\mathrm{S}:0.30
,
𝐋
:
0.00
\mathrm{L}:0.00
,
ℰ
:
0.09
\mathcal{E}:0.09
]
, a researcher at Hewlett-Packard (HP)
[
𝐒
:
1.00
\mathrm{S}:1.00
,
𝐋
:
0.00
\mathrm{L}:0.00
,
ℰ
:
0.04
\mathcal{E}:0.04
]
. …
Inventions (Failure)
Tell me about the invention of Solar Power and its inventor.
…
Augustin Mouchot (1828–1889) built the first solar-powered engine in 1860
[
𝐒
:
0.07
\mathrm{S}:0.07
,
𝐋
:
0.20
\mathrm{L}:0.20
,
ℰ
:
0.31
\mathcal{E}:0.31
]
, which was used to pump water in Algeria.
The Birth of Modern Solar Power
The breakthrough in modern solar power came
in the 1950s with the invention of the photovoltaic cell
[
𝐒
:
0.13
\mathrm{S}:0.13
,
𝐋
:
0.36
\mathrm{L}:0.36
,
ℰ
:
0.30
\mathcal{E}:0.30
]
, which converts sunlight directly into electricity.
- Inventors:
Daryl Chapin, Calvin Fuller, and Jerry Pearson at Bell Labs (now part of Lucent Technologies) developed the first practical silicon solar cell in 1954
[
𝐒
:
0.21
\mathrm{S}:0.21
,
𝐋
:
0.39
\mathrm{L}:0.39
,
ℰ
:
0.26
\mathcal{E}:0.26
]
. …
Gemma-3-12B-IT
Biographies (ID)
Tell me a paragraph bio of Radhika Apte.
Radhika Apte is a highly acclaimed Indian actress
[
𝐒
:
1.00
\mathrm{S}:1.00
,
𝐋
:
0.75
\mathrm{L}:0.75
,
ℰ
:
0.43
\mathcal{E}:0.43
]
known for her versatility and captivating performances across film, television, and theatre.
Beginning her career in theatre
[
𝐒
:
0.14
\mathrm{S}:0.14
,
𝐋
:
0.58
\mathrm{L}:0.58
,
ℰ
:
0.56
\mathcal{E}:0.56
]
, she transitioned to Bollywood and quickly gained recognition for her roles in
films like "Vaastav: The Reality,"
[
𝐒
:
0.99
\mathrm{S}:0.99
,
𝐋
:
0.05
\mathrm{L}:0.05
,
ℰ
:
0.14
\mathcal{E}:0.14
]
…
Artworks
Tell me about the artwork "Still Life with Apples" by Paul Cézanne and its artist.
…
The Artwork: "Still Life with Apples" (c. 1893)
[
𝐒
:
0.46
\mathrm{S}:0.46
,
𝐋
:
0.66
\mathrm{L}:0.66
,
ℰ
:
0.63
\mathcal{E}:0.63
]
Description: …
Medium: Oil on canvas.
[
𝐒
:
0.15
\mathrm{S}:0.15
,
𝐋
:
0.73
\mathrm{L}:0.73
,
ℰ
:
0.66
\mathcal{E}:0.66
]
Size: Approximately 38 cm × 51 cm (15 in × 20 in)
[
𝐒
:
0.70
\mathrm{S}:0.70
,
𝐋
:
0.07
\mathrm{L}:0.07
,
ℰ
:
0.29
\mathcal{E}:0.29
]
…
Landmarks (Failure)
Tell me about the landmark The Giza Pyramid Complex, Egypt.
…It’s a vast complex of structures
built during the Fourth Dynasty of the Old Kingdom
[
𝐒
:
0.36
\mathrm{S}:0.36
,
𝐋
:
0.12
\mathrm{L}:0.12
,
ℰ
:
0.25
\mathcal{E}:0.25
]
(
roughly 2589–2566 BC
)
[
𝐒
:
0.42
\mathrm{S}:0.42
,
𝐋
:
0.64
\mathrm{L}:0.64
,
ℰ
:
0.64
\mathcal{E}:0.64
]
.
It served as a necropolis (city of the dead) for the pharaohs and their consorts
[
𝐒
:
0.00
\mathrm{S}:0.00
,
𝐋
:
0.16
\mathrm{L}:0.16
,
ℰ
:
0.44
\mathcal{E}:0.44
]
…
Table 17:
Qualitative claim-level predictions. Green and red spans are correct and hallucinated claims, respectively. After each span,
S
\mathrm{S}
,
L
L
, and
ℰ
\mathcal{E}
give
P
⁡
(
y
=
1
)
P(y=1)
from the supervised embedding baseline, Layer Top-
m
m
, and Ensemble (Task). Green probability text denotes a prediction
≥
0.5
\geq 0.5
; red denotes a prediction
<
0.5
<0.5
.