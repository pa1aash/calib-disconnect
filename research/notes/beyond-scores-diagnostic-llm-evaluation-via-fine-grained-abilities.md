---
title: 'Beyond Scores: Diagnostic LLM Evaluation via Fine-Grained Abilities'
id: beyond-scores-diagnostic-llm-evaluation-via-fine-grained-abilities
tags:
- code-llm-best-aaai-paper-6ded37
- capability-science
- closest-prior-work
- cognitive-diagnosis-qmatrix
created: '2026-07-20T07:42:35.783686Z'
updated: '2026-07-20T07:45:51.118428Z'
source: https://arxiv.org/html/2604.12191
source_domain: arxiv.org
fetched_at: '2026-07-20T07:42:35.782979Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Proposes a cognitive-diagnostic framework using multidimensional Item Response
  Theory (mIRT) plus a hand-built item-ability association matrix (Q-matrix) to decompose
  LLM benchmark performance into fine-grained ability dimensions (35-dim taxonomy
  for math, 27 for physics, 58 for chemistry, 12 for computer science). Evaluated
  on 41 models; predicts performance on unseen benchmark items with AUC 0.80-0.89
  within-benchmark and 0.77-0.86 cross-benchmark. THIS IS THE CLOSEST PRIOR WORK to
  a requirement-level capability-science paper: same mechanism class (Q-matrix + IRT
  ability decomposition) but applied per-QUESTION across whole benchmarks/domains,
  using a taxonomy of abstract cognitive/knowledge skills (e.g. ''multi-step reasoning'',
  ''algebra''), not per-REQUIREMENT (per-unittest-method) within a single code-generation
  problem, and does not study whether failure structure is shared vs idiosyncratic
  across two specific model families. No arXiv comment confirms AAAI acceptance; appears
  to be an ICML-track submission per internal header despite being posted under cs.AI
  in 2026.'
---

Beyond Scores: Diagnostic LLM Evaluation via Fine-Grained Abilities
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2604.12191v1 [cs.AI] 14 Apr 2026
Beyond Scores: Diagnostic LLM Evaluation
via Fine-Grained Abilities
Xu Zhang
Xudong Gong
Jiacheng Qin
Qiang Wang
JiaQi Liao
Zhe Wang
Dawei Feng
Bo Ding
Abstract
Current evaluations of large language models aggregate performance across diverse tasks into single scores. This obscures fine-grained ability variation, limiting targeted model improvement and ability-guided selection for specific tasks. Motivated by this gap, we propose a cognitive diagnostic framework that estimates model abilities across multiple fine-grained dimensions. For mathematics, we construct a 35-dimensional ability taxonomy grounded in cognitive theory and domain knowledge. The framework employs multidimensional Item Response Theory with an item-ability association matrix to estimate fine-grained ability levels, which in turn enable prediction of performance on unseen items (questions of benchmark). Evaluated on 41 models, our approach demonstrates strong criterion validity, consistent ability estimates across benchmarks, and accurate prediction of unseen items with AUC ranging from 0.80 to 0.89 within benchmarks and from 0.77 to 0.86 across benchmarks, substantially exceeding trivial baselines. The framework generalizes across scientific domains, producing consistent diagnostic performance in physics (27 dimensions), chemistry (58 dimensions), and computer science (12 dimensions). This work establishes a principled framework for fine-grained assessment of abilities, with potential applications in targeted training, ability-guided model selection, and ability-aware benchmark design.
Machine Learning, ICML
1
Introduction
Figure 1
:
A diagnostic framework for evaluating LLMs via fine-grained mathematical abilities. Centered on Bloom’s taxonomy, we decompose Mathematical Abilities into two core dimensions: Knowledge (e.g., Algebra, Calculus) and Cognitive (e.g., Multi-step Problem Solving, Critical Reasoning). Each is further subdivided into interpretable sub-skills. The framework links benchmark questions (left) to their underlying abilities and maps them to real-world problem domains (right), enabling granular diagnosis beyond aggregate scores and bridging the gap between evaluation benchmarks and practical task demands.
Large language models (LLMs) have demonstrated remarkable progress across diverse domains, with performance on standardized benchmarks approaching or surpassing human levels in specific tasks
(Qin
et al.
,
2025
; Wu
et al.
,
2024
; Wang
et al.
,
2025
)
. However, this progress is predominantly quantified through aggregate scores that condense performance across diverse tasks into single numerical summaries. Because a model’s task-level capabilities emerge from the composition of fine-grained abilities, such as recalling algebraic identities (domain knowledge) or planning multi-step derivations (cognitive processes), these aggregate metrics obscure fine-grained ability variation and limit both targeted model improvement and ability-guided selection for specific tasks. Prior studies reinforce this view: Griot et al.
(Griot
et al.
,
2025
)
highlight missing metacognitive skills in medical reasoning; Cao et al.
(Cao
et al.
,
2025
)
advocate shifting from task-based to ability-centric evaluation; and Liu et al.
(Liu
et al.
,
2024
)
demonstrate that aggregate accuracy masks mastery of specific concepts.
Cognitive diagnostic methods from educational assessment, including Classical Test Theory (CTT)
(DeVellis,
2006
)
, Item Response Theory (IRT)
(Harvey and Hammer,
1999
)
, and multidimensional IRT (mIRT)
(Ackerman,
2014
)
, were originally developed to diagnose students’ fine-grained abilities from their responses to assessment items. Recent work has successfully adapted these methods to LLM evaluation
(Liu
et al.
,
2023
; Yao
et al.
,
2025
; Zhao
et al.
,
2025
; Zhou
et al.
,
2025
)
, establishing IRT as a viable framework for model assessment. However, these adaptations treat benchmark items as atomic units and lack explicit mappings between items and the fine-grained abilities they engage. Consequently, they remain confined to coarse-grained performance summaries and cannot support ability-level diagnosis for targeted improvement or task-aligned selection.
To overcome this limitation, we propose a cognitive diagnostic framework that estimates model abilities across multiple fine-grained dimensions. The framework constructs domain-specific ability taxonomies grounded in cognitive theory and domain knowledge; for mathematics, this yields a 35-dimensional taxonomy. An item-ability association matrix (Q-matrix) encodes which fine-grained abilities each benchmark item (question) engages. The framework employs mIRT with the Q-matrix to estimate fine-grained ability levels. These estimates enable both ability-aware model selection aligned with task requirements and accurate prediction of performance on unseen items.
Evaluated on 41 models, the framework demonstrates strong criterion validity, consistent ability estimates across benchmarks, and accurate prediction of unseen items with AUC ranging from 0.80 to 0.89 within benchmarks and from 0.77 to 0.86 across benchmarks. The framework generalizes across scientific domains, producing consistent diagnostic performance in physics (27 dimensions), chemistry (58 dimensions), and computer science (12 dimensions).
Our work establishes a principled diagnostic framework that produces interpretable fine-grained ability profiles for LLMs, with potential to inform targeted training, ability-guided model selection, ability-aware benchmark design, and alignment between benchmark evaluations and real-world task demands (Figure
1
).
2
Diagnostic LLM Evaluation via Fine-Grained Abilities
2.1
Overview
We describe a diagnostic evaluation framework that decomposes model performance on existing benchmarks into fine-grained abilities. These abilities include domain knowledge (e.g., algebraic rules, geometric facts) and cognitive processes (e.g., multi-step reasoning, problem decomposition). As shown in Figure
2
, the framework comprises three components.
(1) A model-item response matrix (R-matrix) derived from existing benchmark evaluations without modifying the original assessment protocol, where entries indicate model correctness on individual items;
(2) An item-ability association matrix (Q-matrix) that explicitly maps each benchmark item to the fine-grained abilities it engages;
(3) Multidimensional Item Response Theory (mIRT) that estimates latent ability levels for each model based on the Q-matrix and R-matrix.
Figure 2
:
Architecture of the fine-grained ability assessment framework. The framework comprises three stages: (a) Response Matrix Construction, where models are evaluated on benchmarks to generate a binary model-item response matrix; (b) Association Matrix Construction, in which each item of benchmark is mapped to fine-grained abilities (e.g., domain knowledge or cognitive processes) via expert annotation and prior knowledge, forming a Q-matrix; and (c) Fine-Grain Ability Evaluation, where a cognitive diagnostic model estimates latent ability profiles by jointly analyzing the response and association matrices.
Model-Item Response Matrix Construction.
We evaluate each target model on all items in a given benchmark and record its responses in binary form, where
1
1
indicates a correct answer and
0
indicates an incorrect or incomplete response. This yields an
m
×
n
m\times n
response matrix
𝐑
\mathbf{R}
, with
m
m
denoting the number of models and
n
n
the number of benchmark items. This matrix serves as the empirical basis for subsequent diagnostic inference.
Item-Ability Association Matrix Construction.
The Q-matrix, denoted
𝐐
∈
{
0
,
1
}
n
×
k
\mathbf{Q}\in\{0,1\}^{n\times k}
, specifies which fine-grained abilities are required to correctly solve each item of benchmarks. Here,
k
k
is the total number of predefined abilities, for example, "recalling trigonometric identities" or "constructing a proof by contradiction." An entry
q
i
​
j
=
1
q_{ij}=1
indicates that item
i
i
depends on ability
j
j
; otherwise,
q
i
​
j
=
0
q_{ij}=0
. The Q-matrix is constructed through a combination of expert annotation and LLM-assisted ability labeling, guided by our taxonomy of mathematical competence (Section
2.3
).
Fine-Grained Ability Estimation.
Given the response matrix
𝐑
\mathbf{R}
and the Q-matrix
𝐐
\mathbf{Q}
, we estimate each model’s latent ability profile (a
k
k
-dimensional vector quantifying its proficiency across fine-grained abilities) using a multidimensional cognitive diagnostic model grounded in mIRT (Section
2.4
). Specifically, the probability that model
m
m
answers item
i
i
correctly is modeled as a function of its proficiency across the
k
k
abilities, along with the item’s discrimination and difficulty parameters. These profiles enable interpretable diagnosis beyond aggregate scores.
2.2
Fine-Grained Ability Taxonomy
As illustrated in Figure
1
, our ability taxonomy is inspired by Bloom’s Taxonomy
(Forehand,
2010
)
and organizes model competence along two dimension categories: domain knowledge and cognitive processes. Each dimension is further decomposed into fine-grained, interpretable subcategories that serve as the basis for diagnostic evaluation.
Domain knowledge
refers to the model’s mastery of static, factual, or procedural content within a specific discipline. In the context of mathematical reasoning, we define knowledge subcategories, such as Algebra, Functions, Arithmetic, and Geometry, by aligning with standard mathematical curricula and the scope of the benchmarks used.
Cognitive processes
capture the model’s capacity to apply knowledge in task-solving contexts. Rather than directly adopting Bloom’s original cognitive levels, which were designed for human learners, we adapt them to the LLM setting by focusing on observable reasoning behaviors. This yields six operationalized cognitive dimensions:
(1) Information Recognition and Extraction,
(2) Concept Understanding and Manipulation,
(3) Analysis, Synthesis, and Verification,
(4) Critical Reasoning and Debugging,
(5) Creative Generation, and
(6) Multi-step Problem Solving.
These dimensions are defined based on the types of reasoning required to solve benchmark items, ensuring alignment between ability definitions and empirical evaluation.
Each benchmark item is linked to one or more abilities spanning both dimensions, with the full annotation protocol described in Section
2.3
.
2.3
Constructing the Q-Matrix via Expert-Supervised LLM Annotation
To enable diagnostic evaluation on existing benchmarks, we construct the Q-matrix, an item-ability association matrix that maps each benchmark item to fine-grained abilities along both domain knowledge and cognitive processes dimensions (Section
2.2
), using a human-in-the-loop annotation pipeline. This pipeline leverages LLMs for scalable ability labeling while incorporating domain experts at critical stages to ensure conceptual fidelity and alignment with educational standards. The process proceeds in three stages.
(a) Ability Pool Generation.
For each benchmark item, we prompt an LLM to identify the fine-grained abilities it assesses, covering both domain knowledge (e.g., Algebra, Geometry) and cognitive processes (e.g., Multi-step Problem Solving, Logical Inference). The union of all identified abilities across items forms an initial ability pool.
(b) Hierarchical Ability System Refinement.
Guided by standard mathematical curricula and our adapted Bloom’s Taxonomy, we design structured prompts to organize the ability pool into a hierarchical system spanning multiple granularities (e.g., coarse: "Algebra"; fine: "polynomials"). This system is then fully reviewed and revised by domain experts to ensure conceptual coherence and alignment with educational standards.
(c) Q-Matrix Construction.
From the refined hierarchy, we select a target granularity level as the final set of evaluation dimensions. An LLM is then prompted to map each benchmark item to the relevant dimensions in this set, producing a preliminary Q-matrix.
Throughout the process, stage (b) undergoes full expert review, while stages (a) and (c) are spot-checked by experts at a 10% random sampling rate, with corrections applied to the entire dataset when systematic errors are detected. All prompts used in this workflow are provided in Appendix
A
.
2.4
Estimating Fine-Grained Abilities via mIRT
Latent trait measurement is a well-established paradigm in psychometrics, with mature methodologies in educational assessment and cognitive diagnosis. To estimate fine-grained ability profiles of LLMs, we adapt mIRT to model the relationship between model responses and underlying competencies spanning both domain knowledge and cognitive processes.
Item Response Theory (IRT) posits a probabilistic relationship between an examinee’s latent traits and their observed binary responses. Our framework enables two key functionalities:
(1) estimating continuous latent ability profiles from model-item response data, and
(2) predicting performance on unseen items by jointly modeling ability parameters and item characteristics, such as discrimination and difficulty.
Figure 3
:
Structure of the IRT-based fine-grained ability evaluation model. Based on the IRT method, a simple fully connected neural network is implemented on the Interaction Layer to fit model performance in downstream tasks, thereby achieving fine-grained ability evaluation.
We adapt the NeuralCD framework
(Wang
et al.
,
2023
)
, a neural extension of mIRT, to estimate LLM ability profiles based on our fine-grained ability taxonomy (Section
2.2
). As shown in Figure
3
, the model enforces the monotonicity assumption of IRT, which states that higher ability levels should yield higher probabilities of correct responses, by constraining all weights in the three fully connected layers to be non-negative. This ensures that the predicted response probability is a monotonically increasing function of each latent ability dimension.
Then, the interaction layer is inspired by mIRT and formalized as follows:
𝒙
=
𝒒
⊙
(
𝒂
−
𝑰
diff
)
×
𝑰
disc
\boldsymbol{\mathit{x}}=\boldsymbol{q}\odot(\boldsymbol{a}-\boldsymbol{I}_{\mathrm{diff}})\times\boldsymbol{I}_{\mathrm{disc}}
(1)
Here,
𝒒
∈
{
0
,
1
}
K
\boldsymbol{q}\in\{0,1\}^{K}
is the item-ability association vector (i.e., a row of the Q-matrix),
𝒂
∈
[
0
,
1
]
K
\boldsymbol{\mathit{a}}\in[0,1]^{K}
denotes the model’s latent ability profile,
𝑰
diff
∈
[
0
,
1
]
K
\boldsymbol{I}_{\mathrm{diff}}\in[0,1]^{K}
represents item-specific difficulty parameters,
I
disc
∈
[
0
,
1
]
K
I_{\mathrm{disc}}\in[0,1]^{K}
is the item discrimination scalar,
⊙
\odot
denotes element-wise multiplication,
and
𝒙
∈
ℝ
K
\boldsymbol{\mathit{x}}\in\mathbb{R}^{K}
is the input to the subsequent MLP layer.
The model’s ability profile
𝒂
\boldsymbol{\mathit{a}}
is then computed via:
𝒂
=
sigmoid
​
(
𝒙
m
×
𝐀
)
\boldsymbol{\mathit{a}}=\mathrm{sigmoid}(\boldsymbol{\mathit{x}}_{m}\times\mathbf{A})
(2)
where
𝒙
m
∈
{
0
,
1
}
1
×
M
\boldsymbol{\mathit{x}}_{m}\in\{0,1\}^{1\times M}
is a one-hot vector indicating the
m
m
-th model, and
𝐀
∈
ℝ
M
×
K
\mathbf{A}\in\mathbb{R}^{M\times K}
is a trainable matrix whose rows represent the fine-grained ability profiles of all
M
M
evaluated models.
This formulation allows us to jointly learn item parameters
(
𝑰
𝐝𝐢𝐟𝐟
,
𝑰
𝐝𝐢𝐬𝐜
)
(\boldsymbol{I_{\mathrm{diff}}},\boldsymbol{I_{\mathrm{disc}}})
and model ability profiles
𝐀
\mathbf{A}
from observed response data, yielding interpretable, multi-dimensional diagnostics beyond aggregate scores.
3
Experiment and Result Analysis
3.1
Experiment Setup
(a)
Distributions of Knowledge Abilities
(b)
Distributions of Cognitive Abilities
Figure 4
:
Distribution of item coverage across 35 fine-grained abilities in three mathematical benchmarks.
The distributions are inconsistent across knowledge-oriented and cognition-oriented dimensions, with pronounced differences among individual dimensions.
Left
: benchmark-knowledge ability associations, indicating distinct assessment emphases across benchmarks.
Right
: benchmark-cognition ability associations, exhibiting greater overlap in assessment tendencies while retaining benchmark-specific emphases.
We evaluate our fine-grained diagnostic framework on a diverse set of benchmarks and models. The effectiveness of the framework is validated from three perspectives: (1) diagnostic utility of the fine-grained ability estimates, (2) cross-benchmark consistency of ability estimates, and (3) predictive performance on held-out items. We further assess cross-domain generalization by extending the evaluation to three non-mathematical subjects.
For the mathematical domain, we use three widely adopted benchmarks: MMLU-MATH, MMLU-Pro-MATH, and MATH500.
Our evaluation encompasses 35 open-source LLMs and 6 proprietary online LLMs.
All models are evaluated through the OpenCompass benchmarking suite, which provides consistent prompt templates, decoding strategies, and scoring rules across benchmarks.
For each model, a binary response matrix is generated by evaluating it on all benchmark items, with correct answers encoded as 1 and incorrect responses as 0.
As shown in Figure
4
, the three mathematical benchmarks exhibit distinct distributions of item coverage across ability dimensions. Detailed coverage statistics are provided in Appendix
D.3
. This heterogeneity motivates our cross-benchmark analysis, which evaluates whether ability profiles generalize across these differing distributions.
For ability estimation, we implement the mIRT-based evaluation model described in Section
2.4
, a three-layer fully connected network with hidden dimensions (256, 1024, 128). The model employs CrossEntropyLoss as the loss function and is optimized using Adam with an initial learning rate of 0.001 (decayed by 0.8) and a batch size of 256. All experiments use an NVIDIA RTX 3090 GPU.
Further details of the experimental setup are provided in Appendix
D
.
3.2
Validity of the Fine-Grained Diagnostic Framework
Validity refers to the extent to which a measurement tool accurately reflects the construct it is intended to assess. We focus on criterion-related validity, which evaluates whether estimated ability scores correlate with external measures of performance on relevant tasks. To this end, we compute Spearman’s rank correlation coefficient (
ρ
\rho
) between the estimated ability score for each dimension and the model’s accuracy on the set of benchmark items linked to that dimension.
For each dimension, accuracy is defined as the mean binary accuracy across all items associated with that dimension in the Q-matrix. High correlation indicates that the estimated ability levels reliably capture the model’s actual performance on relevant evaluation items.
The detailed computation procedure is provided in Appendix
D.4
.
Results across the three mathematical benchmarks, MMLU-MATH, MMLU-Pro-MATH, and MATH500, are visualized in Figure
5
, with full numerical results in Appendix
B
. We define correlation strength as follows: strong (
ρ
>
0.7
\rho>0.7
), moderate (
0.5
<
ρ
≤
0.7
0.5<\rho\leq 0.7
), weak (
0.3
<
ρ
≤
0.5
0.3<\rho\leq 0.5
), and non-significant (
ρ
≤
0.3
\rho\leq 0.3
or
p
>
0.05
p>0.05
).
To assess the robustness of our diagnostic framework, we examine the consistency of criterion validity for each of the 35 ability dimensions across all three mathematical benchmarks. This analysis reveals two key patterns.
First, 18 dimensions exhibit strong criterion correlation in at least two benchmarks, demonstrating stable diagnostic power. Notably, 9 dimensions maintain strong correlation across all three benchmarks. The consistency of these signals across diverse item sets confirms that our framework captures generalizable model competencies.
Figure 5
:
Correlation between estimated fine-grained abilities and model performance on associated benchmark items.
Spearman’s rank correlation coefficient (
ρ
\rho
) measures the association between each ability dimension (columns) and model accuracy on its linked items across three benchmarks (rows).
Color coding
: Blue indicates
ρ
>
0.7
\rho>0.7
(strong), yellow indicates
0.5
<
ρ
≤
0.7
0.5<\rho\leq 0.7
(moderate), and red indicates
0.3
<
ρ
≤
0.5
0.3<\rho\leq 0.5
(weak).
Significance markers
: ** denotes
p
<
0.01
p<0.01
, * denotes
p
<
0.05
p<0.05
.
N/A
indicates that no items in the benchmark are associated with that dimension (i.e., invalid for evaluation).
Dimensions with consistent strong correlation across benchmarks reflect stable diagnostic signals; weak correlations often arise from low item coverage (<10 items).
Second, dimensions with weak or non-significant correlations are consistently associated with sparse item coverage. As shown in Figure
4
, these dimensions correspond to subsets containing fewer than 10 questions, which is less than 5% of the total item pool. For such low-sample dimensions, correlation estimates are inherently unstable, leading to reduced validity. Crucially, no dimension shows high correlation in one benchmark but low in another, indicating that our Q-matrix and ability taxonomy produce coherent, cross-dataset interpretable profiles.
All reported correlations with moderate or stronger strength have p-values < 0.01, confirming statistical significance. Together, these results validate that our method provides reliable, fine-grained diagnostics, provided sufficient items per dimension are available.
3.3
Cross-Benchmark Consistency of Fine-Grained Ability Estimates
Building upon the within-benchmark validity analysis, we further evaluate the generalization of our diagnostic framework across benchmarks with differing distributions of ability dimensions. To ensure reliable comparison, we retain only those ability dimensions for which both benchmarks contain more than 10 associated items. This threshold is chosen to mitigate instability from sparse item coverage.
Figure 6
:
Cross-benchmark correlation of estimated fine-grained ability levels.
Spearman’s
ρ
\rho
between paired benchmarks, computed over 19 of 35 ability dimensions with
>
10
>10
items in all benchmarks.
Color: purple = MMLU-MATH vs MATH500, blue = MMLU-MATH vs MMLU-Pro-MATH, red = MMLU-Pro-MATH vs MATH500.
Shape: squares (
p
<
0.01
p<0.01
), triangles (
p
<
0.05
p<0.05
), diamonds (
p
>
0.05
p>0.05
).
Dashed lines mark thresholds:
ρ
=
0.3
\rho=0.3
(weak),
0.5
0.5
(moderate),
0.7
0.7
(strong).
14 of these 19 dimensions show
ρ
>
0.5
\rho>0.5
across all pairwise comparisons.
We compute Spearman’s rank correlation coefficient (
ρ
\rho
) between the estimated ability scores for each dimension across benchmark pairs.
The results are visualized in Figure
6
, with correlation strength categorized as follows: strong (
ρ
>
0.7
\rho>0.7
), moderate (
0.5
<
ρ
≤
0.7
0.5<\rho\leq 0.7
), and weak (
0.3
<
ρ
≤
0.5
0.3<\rho\leq 0.5
). All reported correlations with
ρ
>
0.3
\rho>0.3
are statistically significant at
p
<
0.05
p<0.05
; those with
ρ
>
0.5
\rho>0.5
satisfy
p
<
0.01
p<0.01
.
Overall, the fine-grained ability estimates demonstrate strong cross-benchmark consistency.
Among the 19 ability dimensions that are valid across all three benchmarks (i.e., each has more than 10 associated items in every benchmark), 14 dimensions exhibit moderate or stronger correlation (
ρ
>
0.5
\rho>0.5
) across all three benchmark pairs, indicating robust generalization.
At the aggregate level, the median pairwise correlation across all dimension-benchmark combinations is
ρ
=
0.66
\rho=0.66
, and 86% of shared dimension-benchmark pairs achieve at least moderate correlation.
These results confirm that our method produces stable, generalizable ability profiles across diverse mathematical benchmarks, reinforcing its suitability for evaluation.
3.4
Predicting Model Performance on Unseen Items
Unlike indirect evaluation methods that rely solely on aggregate test set performance, our fine-grained ability evaluation framework, grounded in mIRT, enables prediction of correct or incorrect responses to unseen items based on the association between each item and a set of fine-grained abilities defined by the Q-matrix.
We evaluate this predictive capability on three mathematical benchmarks: MMLU-MATH, MMLU-Pro-MATH, and MATH500. The area under the ROC curve (AUC) is used as the evaluation metric, as it is threshold-invariant and well-suited for binary response prediction in psychometric settings. For each scenario, we compute AUC separately for each of the 41 models, then report the distribution of these per-model AUC scores. Experiments are structured into two settings, with results visualized in Figure
7
.
(a) Within-Benchmark Prediction.
For each benchmark, we randomly split its items into an evaluation set (90%) and a prediction set (10%), repeating this procedure 10 times to account for partition variance. We estimate model ability levels using the evaluation set, then predict responses on the prediction set using the IRT-based scoring function (Section
2.4
). For unseen items, difficulty and discrimination parameters are fixed to neutral defaults (
I
diff
=
0.5
I_{\text{diff}}=0.5
,
I
disc
=
1.0
I_{\text{disc}}=1.0
), following standard IRT conventions.
(b)
Cross-Benchmark Prediction.
We construct six ordered benchmark pairs (e.g., MMLU-MATH
→
\rightarrow
MATH500), using the source benchmark for ability estimation and the target for prediction. Target items use the same fixed parameters (
I
diff
=
0.5
I_{\text{diff}}=0.5
,
I
disc
=
1.0
I_{\text{disc}}=1.0
).
We compare against three baselines under identical unseen-item conditions:
(1)
Accuracy-based
: uses model’s overall accuracy (AUC = 0.500);
(2)
Standard unidimensional IRT
: models a single latent trait (AUC = 0.500);
(3)
Random prediction
: samples probabilities from
𝒩
​
(
0.5
,
0.2
2
)
\mathcal{N}(0.5,0.2^{2})
truncated to
[
0
,
1
]
[0,1]
, yielding AUCs of 0.4968
±
\pm
0.1157 (MMLU-MATH), 0.4708
±
\pm
0.1326 (MMLU-Pro-MATH), and 0.4992
±
\pm
0.0586 (MATH500).
Figure 7
:
AUC distribution across 41 LLMs for nine prediction scenarios.
Boxplots show median, IQR, and outliers (whiskers = 1.5
×
\times
IQR).
First three: within-benchmark prediction on MMLU-MATH, MATH500, MMLU-Pro-MATH;
remaining six: cross-benchmark prediction over all ordered benchmark pairs.
All scenarios significantly outperform baselines under identical item assumptions:
accuracy-based (AUC = 0.50),
standard IRT (AUC = 0.50),
and random prediction (mean AUC = 0.49).
Within-benchmark predictions achieve mean AUC > 0.81, while cross-benchmark results range from 0.77 to 0.81.
Results in Figure
7
show that all scenarios significantly outperform these baselines, demonstrating that our framework reliably predicts model behavior on unseen items even across benchmarks with differing item–ability distributions.
3.5
Cross-Domain Generalization of the Diagnostic Framework
To evaluate the generalizability of our evaluation framework beyond mathematical reasoning, we extend the analysis to three additional domains: physics, chemistry, and computer science, using the corresponding subsets from the MMLU-Pro benchmark. Following the pipeline in Sections
2.3
–
2.4
, we construct domain-specific Q-matrices via expert-supervised LLM annotation, aligning ability dimensions with each domain’s knowledge structure.
For criterion validity, we analyze only those ability dimensions with sufficient item coverage (>10 associated items). The proportion of dimensions achieving moderate or stronger correlation (
ρ
>
0.5
\rho>0.5
) is as follows:
Chemistry
: 48 out of 58 dimensions (82.8%);
Physics
: 27 out of 27 dimensions (100%);
Computer Science
: 10 out of 12 dimensions (83.3%).
For prediction performance, the AUC values are 0.7664 in chemistry, 0.7925 in physics, and 0.7824 in computer science. These results fall within the range observed in mathematical benchmarks (AUC: 0.77–0.84), indicating that the framework maintains consistent predictive power when transferred to new scientific and technical domains. All cross-domain predictions significantly outperform baselines under identical conditions: accuracy-based (AUC = 0.500), standard unidimensional IRT (AUC = 0.500), and random prediction with mean AUC of 0.4927
±
\pm
0.0838 (chemistry), 0.4958
±
\pm
0.0894 (physics), and 0.5142
±
\pm
0.1078 (computer science).
These findings confirm that our method can be effectively extended beyond mathematics through curriculum-aligned ability definition and Q-matrix construction, without loss of diagnostic or predictive fidelity.
4
Related Work
4.1
Large Language Model Evaluation
Current evaluation of LLMs relies primarily on standardized benchmarks that report aggregate performance metrics. The MMLU benchmark
(Hendrycks
et al.
,
2020
)
evaluates cross-domain knowledge through multiple-choice questions spanning 57 subjects, while MATH and GSM8K
(
cobbe2021gsm8k
)
assess mathematical reasoning using specialized problem sets. More recent efforts such as Humanity’s Last Exam
(Phan
et al.
,
2025
)
compile expert-level challenges to probe advanced deductive capabilities. Despite their widespread adoption, these benchmarks treat each task as a monolithic unit, collapsing diverse cognitive and knowledge-based processes into a single scalar score. This coarse-grained approach yields inconsistent model rankings across benchmarks and provides limited insight into the underlying sources of success or failure.
To address this limitation, several works have introduced more structured evaluation schemes. AtomThink
(Xiang
et al.
,
2024
)
models complex reasoning as compositions of atomic operations, illustrating how higher-level capabilities emerge from basic modules. FineMath
(Liu
et al.
,
2024
)
decomposes elementary mathematics into 17 problem types to enable fine-grained analysis of reasoning pipelines. SciEval
(Sun
et al.
,
2024
)
proposes a four-dimensional taxonomy, including knowledge, application, analysis, and evaluation, to measure 24 scientific competencies.
However, these approaches rely on manually defined taxonomies that reflect designer-specific assumptions about ability structure. Moreover, they either assess abilities in isolation or focus on generative modeling rather than diagnostic evaluation. Crucially, none establish a shared, psychometrically grounded ability space that supports (1) cross-benchmark comparison under heterogeneous distributions, (2) interpretable diagnosis of model ability profiles, or (3) prediction of model behavior on unseen items.
4.2
Psychometrics and Cognitive Diagnosis
Psychometrics provides a formal framework for measuring latent traits such as cognitive abilities and domain knowledge through observable responses. Classical Test Theory (CTT)
(DeVellis,
2006
)
models an observed score as the sum of a true ability and random error, but treats ability as a single global construct. Item Response Theory (IRT)
(Harvey and Hammer,
1999
)
models the probability of a correct response as a function of both examinee ability and item properties, such as difficulty and discrimination, enabling more precise individual assessment. However, standard IRT assumes a unidimensional latent trait, which is insufficient when tasks require multiple distinct competencies. mIRT
(Ackerman,
2014
)
extends this paradigm by representing ability as a vector of fine-grained traits, allowing items to depend on multiple underlying dimensions simultaneously.
This advancement is formalized in Cognitive Diagnosis Models (CDMs)
(De La Torre,
2009
)
, which explicitly define the relationship between test items and required skills via a Q-matrix. The Q-matrix is a binary mapping that indicates which attributes each item measures. CDMs such as DINA
(Junker and Sijtsma,
2001
)
and G-DINA
(De La Torre,
2011
)
estimate mastery profiles over discrete skill sets, supporting both diagnostic interpretation and prediction of future responses.
Recent work integrates neural networks into this framework. NeuralCD
(Wang
et al.
,
2023
)
replaces linear link functions with deep architectures to model complex interactions between skills and items, while preserving the interpretability of the Q-matrix. These models demonstrate that structured psychometric frameworks can be enhanced with modern machine learning without sacrificing diagnostic transparency.
Collectively, these approaches establish a principled foundation for decomposing performance into interpretable ability components, a perspective increasingly relevant to the evaluation of LLMs.
4.3
Diagnosis Model-based LLM Evaluation
Recent work has begun to adapt psychometric models for LLM evaluation. Castleman et al.
(Castleman
et al.
,
2025
)
analyze mathematical benchmarks and argue that datasets like GSM8K and MathOdyssey fail to reliably assess state-of-the-art models, advocating for IRT-based analysis to improve evaluation validity. Liu et al.
(Liu
et al.
,
2023
)
apply IRT to evaluate 51 recommendation algorithms, showing that high aggregate rankings do not necessarily reflect progress in user preference modeling. Zhou et al.
(Zhou
et al.
,
2025
)
use IRT to construct neural networks that mitigate the impact of benchmark difficulty and complexity on model assessment. Rodriguez et al.
(Rodriguez
et al.
,
2021
)
employ IRT to quantify how item characteristics affect model rankings, though they do not estimate underlying abilities.
Building on these insights, JE-IRT
(Yao
et al.
,
2025
)
jointly embeds LLMs and items into a shared space using classical IRT, decomposing a single score into multiple ability dimensions. Similarly, Zhao et al.
(Zhao
et al.
,
2025
)
adopt a Bayesian framework to predict model performance in vision-language tasks. However, both methods require partial response records for target items to perform matrix completion, whereas our framework predicts items with no prior responses by mapping them into a shared ability space via the Q-matrix, enabling cross-benchmark generalization and interpretable diagnosis.
Despite these advances, current diagnosis-based evaluations remain limited in three key aspects. First, they lack a principled, fine-grained ability taxonomy; most define abilities post hoc or at the task level. Second, they are typically validated within a single benchmark, with little evidence of cross-benchmark or cross-domain generalization. Third, they focus on fitting observed responses rather than predicting performance on novel items. In contrast, our framework defines a unified 35-dimensional ability space spanning domain knowledge and cognitive processes, constructs a Q-matrix to map items across benchmarks, and demonstrates accurate prediction on unseen items both within and across scientific domains.
5
Conclusion and Future Directions
We propose a cognitive diagnostic framework for fine-grained LLM evaluation grounded in multidimensional Item Response Theory (mIRT). The framework constructs domain-specific ability taxonomies by integrating cognitive theory with domain knowledge structures; for mathematics, this yields a 35-dimensional taxonomy spanning domain knowledge and cognitive processes. Evaluated on 41 models, the framework demonstrates strong criterion validity, consistent ability estimates across benchmarks, and accurate prediction of unseen items with AUC ranging from 0.80 to 0.89 within benchmarks and from 0.77 to 0.86 across benchmarks, substantially exceeding trivial baselines.
The framework generalizes across scientific domains, producing consistent diagnostic performance in physics (27 dimensions), chemistry (58 dimensions), and computer science (12 dimensions). By estimating interpretable fine-grained ability profiles, our approach provides a principled foundation for LLM assessment with potential to inform targeted training, ability-guided model selection, ability-aware benchmark design, and alignment between benchmark evaluations and real-world task demands.
Limitations include the manual effort required for taxonomy construction and Q-matrix annotation, potential subjectivity in mapping items to fine-grained abilities, and uneven ability coverage in existing benchmarks. Future work will extend the framework to additional domains, develop ability-aware benchmarks with balanced coverage, and explore ability-guided model training based on diagnostic profiles.
Impact Statements
This paper presents work whose goal is to advance the field of machine learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here.
References
T. A. Ackerman (2014)
Multidimensional item response theory models
.
Wiley StatsRef: Statistics Reference Online
.
Cited by:
§1
,
§4.2
.
Y. Cao, S. Hong, X. Li, J. Ying, Y. Ma, H. Liang, Y. Liu, Z. Yao, X. Wang, D. Huang,
et al.
(2025)
Toward generalizable evaluation in the llm era: A survey beyond benchmarks
.
arXiv preprint arXiv:2504.18838
.
External Links:
2504.18838
Cited by:
§1
.
J. Castleman, N. Nadeem, T. Namjoshi, and L. T. Liu (2025)
Rethinking math benchmarks for llms using IRT
.
Proceedings of Machine Learning Research
273
,
pp. 66–82
.
Cited by:
§4.3
.
J. De La Torre (2009)
A cognitive diagnosis model for cognitively based multiple-choice options
.
Applied Psychological Measurement
33
(
3
),
pp. 163–183
.
Cited by:
§4.2
.
J. De La Torre (2011)
The generalized DINA model framework
.
Psychometrika
76
(
2
),
pp. 179–199
.
Cited by:
§4.2
.
R. F. DeVellis (2006)
Classical test theory
.
Medical care
44
(
11
),
pp. S50–S59
.
Cited by:
§1
,
§4.2
.
M. Forehand (2010)
Bloom’s taxonomy
.
Emerging perspectives on learning, teaching, and technology
41
(
4
),
pp. 47–56
.
Cited by:
§2.2
.
M. Griot, C. Hemptinne, J. Vanderdonckt, and D. Yuksel (2025)
Large Language Models lack essential metacognition for reliable medical reasoning
.
Nature Communications
16
(
1
),
pp. 642
.
External Links:
ISSN 2041-1723
,
Document
Cited by:
§1
.
R. J. Harvey and A. L. Hammer (1999)
Item response theory
.
The Counseling Psychologist
27
(
3
),
pp. 353–383
.
Cited by:
§1
,
§4.2
.
D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt (2020)
Measuring massive multitask language understanding
.
arXiv preprint arXiv:2009.03300
.
External Links:
2009.03300
Cited by:
§4.1
.
B. W. Junker and K. Sijtsma (2001)
Cognitive assessment models with few assumptions, and connections with nonparametric item response theory
.
Applied Psychological Measurement
25
(
3
),
pp. 258–272
.
Cited by:
§4.2
.
Y. Liu, R. Jin, L. Shi, Z. Yao, and D. Xiong (2024)
Finemath: A fine-grained mathematical evaluation benchmark for chinese large language models
.
arXiv preprint arXiv:2403.07747
.
External Links:
2403.07747
Cited by:
§1
,
§4.1
.
Y. Liu, A. Medlar, and D. Glowacka (2023)
What we evaluate when we evaluate recommender systems: Understanding recommender systems’ performance using item response theory
.
In
Proceedings of the 17th ACM Conference on Recommender Systems
,
RecSys ’23
,
New York, NY, USA
,
pp. 658–670
.
External Links:
Document
,
ISBN 979-8-4007-0241-9
Cited by:
§1
,
§4.3
.
L. Phan, A. Gatti, Z. Han, N. Li, J. Hu, H. Zhang, C. B. C. Zhang, M. Shaaban, J. Ling, S. Shi,
et al.
(2025)
Humanity’s last exam
.
arXiv preprint arXiv:2501.14249
.
External Links:
2501.14249
Cited by:
§4.1
.
Y. Qin, S. Wang, Y. Lou, J. Dong, K. Wang, X. Li, and X. Mao (2025)
SoapFL: A standard operating procedure for LLM-based method-level fault localization
.
IEEE Transactions on Software Engineering
51
(
4
),
pp. 1173–1187
.
External Links:
Document
Cited by:
§1
.
P. Rodriguez, J. Barrow, A. M. Hoyle, J. P. Lalor, R. Jia, and J. Boyd-Graber (2021)
Evaluation examples are not equally informative: How should that change NLP leaderboards?
.
In
Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)
,
C. Zong, F. Xia, W. Li, and R. Navigli (Eds.)
,
Online
,
pp. 4486–4503
.
External Links:
Document
Cited by:
§4.3
.
L. Sun, Y. Han, Z. Zhao, D. Ma, Z. Shen, B. Chen, L. Chen, and K. Yu (2024)
SciEval: A Multi-Level Large Language Model Evaluation Benchmark for Scientific Research
.
Proceedings of the AAAI Conference on Artificial Intelligence
38
(
17
),
pp. 19053–19061
.
External Links:
ISSN 2374-3468, 2159-5399
,
Document
Cited by:
§4.1
.
F. Wang, Q. Liu, E. Chen, Z. Huang, Y. Yin, S. Wang, and Y. Su (2023)
NeuralCD: A General Framework for Cognitive Diagnosis
.
IEEE Transactions on Knowledge and Data Engineering
35
(
8
),
pp. 8312–8327
.
External Links:
ISSN 1041-4347, 1558-2191, 2326-3865
,
Document
Cited by:
§2.4
,
§4.2
.
X. Wang, Q. Xu, K. Xu, T. Yu, B. Ding, D. Feng, and Y. Dou (2025)
Large pretrained foundation model for key performance indicator multivariate time series anomaly detection
.
IEEE Open J. Comput. Soc.
6
,
pp. 176–187
.
External Links:
Document
Cited by:
§1
.
X. Wu, S. Huang, G. Wang, J. Xiong, and F. Wei (2024)
Boosting text-to-video generative model with mllms feedback
.
In
Advances in Neural Information Processing Systems
,
A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (Eds.)
,
Vol.
37
,
pp. 139444–139469
.
External Links:
Document
Cited by:
§1
.
K. Xiang, Z. Liu, Z. Jiang, Y. Nie, R. Huang, H. Fan, H. Li, W. Huang, Y. Zeng, J. Han,
et al.
(2024)
Atomthink: A slow thinking framework for multimodal mathematical reasoning
.
arXiv preprint arXiv:2411.11930
.
External Links:
2411.11930
Cited by:
§4.1
.
L. H. Yao, N. Jarvis, T. Zhan, S. Ghosh, L. Liu, and T. Jiang (2025)
JE-IRT: a geometric lens on LLM abilities through joint embedding item response theory
.
arXiv preprint arXiv:2509.22888
.
External Links:
2509.22888
Cited by:
§1
,
§4.3
.
Q. Zhao, M. Xu, K. Gupta, A. Asthana, L. Zheng, and S. Gould (2025)
Can We Predict Performance of Large Models across Vision-Language Tasks?
.
External Links:
2410.10112
,
Document
Cited by:
§1
,
§4.3
.
H. Zhou, H. Huang, Z. Zhao, L. Han, H. Wang, K. Chen, M. Yang, W. Bao, J. Dong, B. Xu,
et al.
(2025)
Lost in benchmarks? Rethinking large language model benchmarking with item response theory
.
arXiv preprint arXiv:2505.15055
.
External Links:
2505.15055
Cited by:
§1
,
§4.3
.
Appendix A
Methodology for Fine-Grained Ability Taxonomy and Q-Matrix Construction
We employ a human-in-the-loop framework that leverages large language models (LLMs) under expert supervision to construct a fine-grained ability taxonomy grounded in domain knowledge and Bloom’s taxonomy, and to subsequently derive the Q-matrix. The process consists of three sequential stages. First, in item analysis, we map benchmark items to relevant cognitive attributes using established educational frameworks (e.g., K-16 mathematics curricula) and Bloom’s taxonomy, yielding an initial attribute pool; human experts sample LLM-generated mappings to assess validity and iteratively refine the prompting strategy to improve alignment with pedagogical standards. Second, during taxonomy construction, we organize this pool into a hierarchical structure: the LLM proposes groupings and provides concise definitions for abilities at each level, which domain experts then fully review to ensure coherence, non-redundancy, and fidelity to educational theory. Third, in Q-matrix construction, we select an appropriate granularity level from the taxonomy as the target ability dimensions for evaluation, and under expert supervision, the LLM annotates each benchmark item with binary indicators denoting required abilities, producing the final Q-matrix.
The prompts used in each stage are provided below.
A.1
Prompt of Item Analysis
In the item analysis stage, we prompt the LLM to map each benchmark item to relevant cognitive attributes based on domain knowledge and Bloom’s taxonomy. The prompt used is as follows.
System Prompt:
⬇
You
are
a
professional
mathematics
education
assessment
expert
with
15
years
of
experience
in
mathematics
curriculum
design
and
test
question
analysis
.
You
excel
at
precisely
deconstructing
the
ability
structure
required
for
test
questions
from
the
dual
perspectives
of
cognitive
psychology
and
mathematics
pedagogy
.
Please
analyze
the
following
mathematics
test
question
and
output
**
both
the
specific
abilities
covered
by
this
question
and
the
reasons
why
these
abilities
are
required
**.
For
each
type
of
ability
,
please
include
:
1.
**
What
specific
abilities
are
covered
**
-
List
the
exact
abilities
needed
2.
**
Why
these
abilities
are
covered
**
-
Explain
how
each
ability
is
applied
in
solving
this
specific
question
**
Ability
Categories
:**
-
Knowledge
-
based
abilities
:
Identify
specific
,
concrete
mathematical
facts
,
concepts
,
formulas
,
theorems
,
or
procedures
that
the
user
must
recall
or
recognize
.
Output
must
be
extremely
concise
,
but
not
too
closely
related
to
the
specific
formulas
or
data
in
the
question
.
Using
only
standard
domain
-
specific
keywords
or
very
short
phrases
(
e
.
g
.,
’
Pythagorean
theorem
’,
’
quadratic
formula
’,
’
derivative
rules
’).
**
Avoid
complete
sentences
or
explanatory
clauses
.**
-
Cognitive
abilities
:
Identify
the
higher
-
order
mental
processes
and
strategic
abilities
required
to
apply
the
knowledge
.
Output
must
be
concise
,
using
generic
,
transferable
skill
names
expressed
as
short
noun
phrases
or
gerunds
(
e
.
g
.,
’
algebraic
manipulation
’,
’
logical
reasoning
’,
’
modeling
’,
’
interpretation
’).
**
Avoid
broad
verbs
like
’
solve
’
or
’
use
’;
strive
for
precise
,
compact
terms
.**
**
Strict
Output
Requirements
:**
-
Each
ability
must
be
directly
relevant
to
answering
the
test
question
-
Knowledge
-
based
abilities
should
be
specific
to
mathematical
concepts
-
Cognitive
abilities
should
use
professional
ability
names
(
e
.
g
.,
"
logical
reasoning
,"
"
spatial
imagination
")
-
For
each
ability
,
provide
a
clear
explanation
of
why
it
’
s
needed
for
this
specific
question
-
Only
analyze
abilities
and
their
justifications
;
do
not
evaluate
difficulty
or
provide
suggestions
-
Output
strictly
in
JSON
format
,
without
any
additional
text
-
All
skills
must
be
in
English
,
using
precise
and
commonly
accepted
terminology
**
Output
Format
:**
{
"
knowledge_abilities
":
[
{
"
ability
":
"
mathematical
knowledge
point
1",
"
explanation
":
"
why
this
knowledge
is
required
for
solving
this
question
"
},
{
"
ability
":
"
specific
mathematical
knowledge
point
2",
"
explanation
":
"
why
this
knowledge
is
required
for
solving
this
question
"
}
],
"
cognitive_abilities
":
[
{
"
ability
":
"
cognitive
ability
name
1",
"
explanation
":
"
why
this
cognitive
ability
is
applied
in
solving
this
question
"
},
{
"
ability
":
"
cognitive
ability
name
2",
"
explanation
":
"
why
this
cognitive
ability
is
applied
in
solving
this
question
"
}
]
}
User Prompt:
⬇
Analyze
the
following
problem
:
[
problem
text
]
A.2
Prompt of Taxonomy Construction
In the taxonomy construction stage, human experts provide an initial set of fine-grained knowledge points derived from item analysis. The LLM is then tasked with organizing these into a hierarchical competency framework grounded in educational theory. The prompts used are as follows.
System Prompt:
⬇
You
are
an
expert
in
mathematics
education
and
curriculum
design
.
Your
task
is
to
construct
a
comprehensive
and
well
-
structured
mathematical
competency
framework
based
on
a
set
of
fine
-
grained
knowledge
points
provided
by
the
user
.
**1.
Core
Design
Principles
**
-
**
Theoretical
Anchoring
**:
The
framework
design
must
be
primarily
based
on
the
**
Revised
Bloom
’
s
Taxonomy
**’
s
cognitive
process
dimension
(
Remember
,
Understand
,
Apply
,
Analyze
,
Evaluate
,
Create
)
and
knowledge
dimension
(
Factual
,
Conceptual
,
Procedural
,
Metacognitive
).
Additionally
,
references
can
be
made
to
classifications
in
mathematics
education
,
such
as
**
Declarative
Knowledge
**
(
related
to
abstraction
and
logical
reasoning
)
and
**
Procedural
Knowledge
**
(
related
to
computation
and
modeling
).
-
**
Granularity
Consistency
**:
This
is
a
key
requirement
.
Each
branch
of
the
framework
must
maintain
balanced
hierarchical
depth
and
subdivision
granularity
.
-
**
Horizontal
Consistency
**:
All
nodes
at
the
same
level
(
e
.
g
.,
all
secondary
nodes
)
should
represent
competency
domains
of
roughly
the
same
scale
.
-
**
Vertical
Progression
**:
The
division
of
levels
should
have
clear
logic
(
e
.
g
.,
"
Knowledge
Domain
->
Core
Concept
->
Specific
Component
"
or
"
Cognitive
Process
->
Specific
Practice
->
Performance
Description
"),
with
a
depth
typically
not
exceeding
4-5
layers
to
avoid
some
paths
being
too
deep
while
others
are
too
shallow
.
**2.
Competency
Framework
Structure
Requirements
**
The
framework
must
consist
of
the
following
two
parts
:
-
**
Knowledge
Abilities
**:
Reflects
familiarity
with
and
mastery
of
mathematical
knowledge
itself
.
The
structure
should
embody
the
internal
logic
of
mathematical
content
(
e
.
g
.,
Number
and
Quantity
,
Geometry
,
etc
.).
-
**
Cognitive
Abilities
**:
Reflects
the
application
and
thinking
processes
applied
to
mastered
knowledge
.
The
structure
should
reflect
a
spectrum
of
cognitive
skills
from
lower
-
order
to
higher
-
order
,
integrating
mathematical
practices
such
as
problem
-
solving
,
reasoning
,
modeling
,
and
communication
.
**3.
Level
Definition
and
Description
Specifications
**
You
must
provide
a
clear
description
for
**
every
custom
non
-
leaf
node
**
(
i
.
e
.,
all
category
and
subcategory
nodes
)
in
the
framework
to
ensure
the
intent
of
the
hierarchical
construction
is
explicit
and
aligns
with
research
consensus
.
Descriptions
should
follow
this
format
:
-
‘"
level_definition
"‘:
Define
the
core
connotation
of
the
abilities
at
this
level
in
1-2
sentences
.
-
‘"
differentiation_criteria
"‘:
Explain
the
principles
(
e
.
g
.,
different
knowledge
domains
,
cognitive
behaviors
,
practical
contexts
)
used
to
differentiate
between
sibling
nodes
under
the
same
parent
node
.
-
‘"
example_verbs_or_actions
"‘:
Provide
2-3
typical
action
verbs
or
task
examples
that
align
with
the
abilities
at
this
level
(
e
.
g
.,
for
an
"
Apply
"
level
,
these
could
be
"
execute
a
computation
",
"
use
a
formula
to
solve
a
routine
problem
").
**4.
Knowledge
Point
Mapping
and
Output
Format
**
-
You
must
ensure
that
all
**
fine
-
grained
knowledge
points
**
provided
by
the
user
can
be
accurately
categorized
as
**
leaf
nodes
**
under
the
appropriate
parent
node
at
the
most
granular
level
of
the
framework
.
-
The
output
must
be
in
strict
,
directly
parsable
JSON
format
,
containing
no
non
-
ASCII
characters
.
The
JSON
structure
must
strictly
adhere
to
the
following
template
,
with
your
"
description
"
for
each
non
-
leaf
node
embedded
in
the
corresponding
node
’
s
‘"
description
"‘
field
.
**
Output
Format
:**
{
"
knowledge_abilities
":
{
"
children
":
{
"
node1
":
{
"
name
":
"
node1
",
"
description
":
"
description
of
node1
",
"
children
":
{
"
node1
-1":
{
"
name
":
"
node11
",
"
description
":
"
description
of
node1
-1",
"
children
":
{
"
node1
-1-1":
{
"
name
":
"
node111
",
"
description
":
"
description
of
node1
-1-1",
"
children
":
{
"
node1
-1-1-1":
"
knowledge
point
11",
"
node1
-1-1-2":
"
knowledge
point
12"
}
}
}
}
}
}
}
},
"
cognitive_abilities
":
{
"
children
":
{
"
node2
":
{
"
name
":
"
node2
",
"
description
":
"
description
of
node2
",
"
children
":
{
"
node2
-1":
{
"
name
":
"
node21
",
"
description
":
"
description
of
node2
-1",
"
children
":
{
"
node2
-1-1":
{
"
name
":
"
node211
",
"
description
":
"
description
of
node2
-1-1",
"
children
":
{
"
node2
-1-1-1":
"
knowledge
point
21",
"
node2
-1-1-2":
"
knowledge
point
22"
}
}
}
}
}
}
}
}
}
Note
:
Ensure
all
provided
knowledge
points
can
be
found
with
corresponding
parent
nodes
in
the
tree
structure
,
and
place
them
at
appropriate
levels
.
The
output
must
be
valid
JSON
that
can
be
directly
parsed
.
User Prompt:
⬇
Please
generate
the
competency
framework
based
on
the
following
knowledge
points
:
[
selected
fine
-
grained
abilities
]
A.3
Prompt of Q-Matrix Construction
In the Q-matrix construction stage, the LLM annotates each benchmark item by mapping it to relevant abilities from the finalized taxonomy. The system and user prompts used are as follows.
System Prompt:
⬇
You
are
a
professional
math
test
item
analysis
assistant
.
Please
strictly
adhere
to
the
following
requirements
for
the
analysis
task
:
**
Task
Requirements
:**
1.
For
each
input
test
question
,
analyze
the
mathematical
abilities
it
assesses
.
2.
**
Abilities
**
must
and
can
only
come
from
the
user
-
provided
ability
list
.
Do
not
add
points
outside
the
list
.
3.
The
output
must
be
in
**
strict
JSON
format
**,
with
the
specific
structure
detailed
below
.
4.
For
each
related
ability
,
provide
a
brief
explanatory
note
justifying
why
and
how
the
question
assesses
this
ability
.
**
Analysis
Principles
:**
1.
Read
each
question
carefully
to
identify
the
core
concepts
,
formulas
,
theorems
,
or
methods
being
tested
.
2.
Strictly
match
the
identified
core
concepts
against
the
provided
abilities
list
.
3.
When
matching
,
the
ability
name
should
be
an
exact
or
core
synonymous
match
(
as
per
the
given
list
).
4.
Explanations
should
be
specific
,
pointing
to
conditions
,
problems
,
or
solution
steps
within
the
question
.
5.
**
All
special
characters
must
be
expressed
in
escaped
form
**
to
ensure
valid
JSON
format
.
For
example
:
-
Double
quotes
should
be
escaped
as
\"
-
Backslashes
should
be
escaped
as
\\
-
Other
JSON
special
characters
should
be
escaped
accordingly
6.
**
JSON
key
names
must
strictly
adhere
to
the
following
specifications
**:
-
Key
names
**
must
not
contain
any
extra
spaces
**
-
Key
names
must
exactly
match
those
in
the
example
.
**
JSON
Key
Examples
:**
"
question_content
",
"
related_abilities
",
"
ability
",
"
explanation
"
**
Output
JSON
Format
:**
{
"
question_content
":
"
Given
a
right
triangle
with
legs
of
lengths
3
and
4,
find
the
length
of
the
hypotenuse
.",
"
related_abilities
":
[
{
"
ability
":
"
Pythagorean
Theorem
",
"
explanation
":
"
The
question
explicitly
gives
the
two
legs
of
a
right
triangle
and
asks
for
the
hypotenuse
,
requiring
direct
application
of
the
Pythagorean
Theorem
\"
a
^2
+
b
^2
=
c
^2\"."
},
{
"
ability
":
"
Square
Root
Computation
",
"
explanation
":
"
After
applying
the
Pythagorean
Theorem
,
the
solver
must
compute
the
square
root
of
25
to
obtain
the
final
answer
."
}
]
}
**
Output
Format
Specification
:**
-
Use
the
above
JSON
structure
.
Place
the
analysis
results
for
each
question
in
a
list
if
multiple
questions
are
processed
(
though
typically
one
at
a
time
in
our
pipeline
).
User Prompt:
⬇
Analyze
the
following
problem
:
[
problem
text
]
Appendix B
Mathematical Ability Taxonomy
Following our methodology for constructing fine-grained ability taxonomies grounded in cognitive theory, we analyze three mathematical benchmarks (MMLU-MATH, MMLU-Pro-MATH, and MATH500) through the lens of K-16 mathematics curricula and Bloom’s taxonomy. This yields a hierarchical taxonomy for mathematical problem solving.
The final taxonomy comprises 35 fine-grained abilities, refined from an initial set of 45 dimensions through iterative expert review. These abilities are organized into two primary dimensions:
Knowledge
(abilities 0–21) and
Cognitive
(abilities 22–34). The structure is visualized in Figure
1
, with the complete numbered list presented below.
B.1
Knowledge Dimension
•
Arithmetic
–
Properties of Numbers (ability_0)
: Recognize characteristics such as parity, divisibility, and magnitude.
–
Operations of Numbers (ability_1)
: Perform computations on integers, fractions, and decimals.
–
Number Theory (ability_2)
: Apply concepts of primes, divisibility, and modular arithmetic.
•
Algebra
–
Expressions and Equations (ability_3)
: Simplify symbolic expressions and solve algebraic equations.
–
Polynomials (ability_4)
: Manipulate polynomials through addition, multiplication, and factorization.
•
Functions
–
Concepts of Functions (ability_5)
: Understand input-output relationships and function properties.
–
Elementary Functions (ability_6)
: Work with linear, quadratic, exponential, and logarithmic functions.
•
Geometry
–
Euclidean Geometry (ability_7)
: Apply axioms and theorems to plane geometric figures.
–
Analytic Geometry (ability_8)
: Use coordinate systems to represent and solve geometric problems.
–
Geometric Measurement (ability_9)
: Compute lengths, areas, volumes, and angles.
•
Calculus
–
Limits and Continuity (ability_10)
: Analyze function behavior near points or at infinity.
–
Differential Calculus (ability_11)
: Compute derivatives and apply them to rates of change and optimization.
–
Integral Calculus (ability_12)
: Evaluate integrals and interpret them as accumulated quantities.
•
Probability and Statistics
–
Descriptive Statistics (ability_13)
: Summarize data using measures of center and spread.
–
Probability (ability_14)
: Calculate likelihoods using classical or theoretical models.
–
Statistical Inference (ability_15)
: Draw conclusions about populations from sample data.
•
Linear Algebra
–
Vectors and Matrices (ability_16)
: Perform operations including addition and multiplication.
–
Linear Systems (ability_17)
: Solve systems of linear equations using algebraic or matrix methods.
–
Vector Spaces (ability_18)
: Analyze subspaces, bases, and dimension.
•
Discrete Mathematics
–
Sets and Logic (ability_19)
: Apply set operations and logical reasoning.
–
Combinatorial Counting (ability_20)
: Count arrangements using permutations and combinations.
–
Graph Theory (ability_21)
: Analyze connectivity and structures in networks.
B.2
Cognitive Dimension
•
Information Recognition and Extraction
–
Element Identification (ability_22)
: Recognize and classify mathematical objects such as numbers or symbols.
–
Knowledge Retrieval (ability_23)
: Recall definitions, formulas, or procedures from memory.
•
Concept Understanding and Manipulation
–
Interpretation and Connection (ability_24)
: Link mathematical representations to meanings or prior knowledge.
–
Concept Manipulation (ability_25)
: Reorganize or transform concepts for new problem contexts.
•
Analysis, Synthesis, and Verification
–
Analysis and Decomposition (ability_26)
: Break complex problems into simpler components.
–
Synthesis and Evaluation (ability_27)
: Combine ideas and judge solution validity or efficiency.
•
Critical Reasoning and Debugging
–
Error Diagnosis (ability_28)
: Detect and explain mistakes in reasoning or computation.
–
Robustness Analysis (ability_29)
: Test solutions under varying conditions or edge cases.
•
Creative Generation
–
Generation and Construction (ability_30)
: Create new mathematical objects, models, or representations.
–
Abstraction and Generalization (ability_31)
: Derive general principles from specific examples.
•
Multi-step Problem Solving
–
Procedure Construction (ability_32)
: Design step-by-step methods for novel problems.
–
Procedure Execution (ability_33)
: Carry out algorithms or computational steps accurately.
–
Conventional Modeling (ability_34)
: Translate real-world scenarios into mathematical forms.
Appendix C
Extended Domain Taxonomies
To demonstrate the generalizability of our taxonomy construction methodology, we apply it to three additional scientific domains beyond mathematics: physics, chemistry, and computer science. Each domain-specific taxonomy is constructed through expert-supervised LLM annotation aligned with the field’s knowledge structure. Below we present the resulting ability taxonomies.
C.1
Physics
The physics taxonomy comprises 27 fine-grained abilities spanning classical mechanics, electromagnetism, thermodynamics, optics, modern physics, astronomy, and cognitive processes. The complete list is presented below.
•
Kinematics and Dynamics (ability_0)
: Analyze motion and forces using Newtonian principles.
•
Rotational and Oscillatory Motion (ability_1)
: Apply concepts of torque, angular momentum, and harmonic oscillation.
•
Gravitation and Orbital Mechanics (ability_2)
: Model gravitational interactions and orbital trajectories.
•
Wave Basics (ability_3)
: Describe wave properties including frequency, wavelength, and propagation.
•
Geometric Optics (ability_4)
: Apply ray tracing and lens/mirror equations to optical systems.
•
Physical Optics (ability_5)
: Analyze interference, diffraction, and polarization phenomena.
•
Temperature and Units (ability_6)
: Convert between temperature scales and thermal units.
•
Heat, Calorimetry, and Phase (ability_7)
: Compute heat transfer and analyze phase transitions.
•
Gas Laws, Processes, and Radiation (ability_8)
: Apply ideal gas law and analyze thermodynamic cycles.
•
Electrostatics and Fields (ability_9)
: Calculate electric fields and potentials from charge distributions.
•
Magnetism and Induction (ability_10)
: Analyze magnetic fields and electromagnetic induction.
•
Circuits and Electromagnetic Waves (ability_11)
: Solve circuit problems and describe electromagnetic wave propagation.
•
Quantum and Atomic Physics (ability_12)
: Explain quantization, atomic structure, and wave-particle duality.
•
Nuclear Physics and Radioactivity (ability_13)
: Analyze nuclear reactions, decay processes, and radiation.
•
Relativity and High-Energy Physics (ability_14)
: Apply special relativity principles and describe particle interactions.
•
Solar System Dynamics (ability_15)
: Model planetary motion and gravitational interactions within the solar system.
•
Observational Astronomy (ability_16)
: Interpret astronomical observations and measurement techniques.
•
Planetary Geology and Atmospheres (ability_17)
: Analyze surface features and atmospheric properties of celestial bodies.
•
Units and Conversions (ability_18)
: Perform dimensional conversions across physical quantities.
•
Dimensional Analysis and Estimation (ability_19)
: Derive relationships and estimate magnitudes using dimensional reasoning.
•
Vectors and Calculus Tools (ability_20)
: Apply vector operations and calculus to physical problems.
•
Interferometry and Zone Relations (ability_21)
: Interpret interference patterns and Fresnel zone constructions.
•
Lens Design and Cardinal Points (ability_22)
: Characterize optical systems using principal planes and focal points.
•
Factual Knowledge (ability_23)
: Recall fundamental physics facts, constants, and definitions.
•
Conceptual Understanding (ability_24)
: Explain physical principles and relationships between concepts.
•
Procedural Skill (ability_25)
: Execute problem-solving procedures and mathematical derivations.
•
Metacognitive Awareness (ability_26)
: Monitor and regulate problem-solving strategies and solution validity.
C.2
Chemistry
The chemistry taxonomy comprises 58 fine-grained abilities spanning core concepts, physical chemistry, inorganic chemistry, organic chemistry, analytical techniques, and cognitive processes. The complete list is presented below.
•
Units and Conversions (ability_0)
: Perform dimensional conversions across chemical contexts.
•
Physical Constants and Reference Values (ability_1)
: Recall and apply fundamental constants in chemical calculations.
•
Atomic Structure and Electron Configuration (ability_2)
: Describe atomic models and electron arrangements.
•
Chemical Bonding and Intermolecular Forces (ability_3)
: Analyze covalent, ionic, and intermolecular interactions.
•
Ideal and Real Gases (ability_4)
: Apply gas laws to ideal and non-ideal gas behavior.
•
Thermodynamic Quantities and Processes (ability_5)
: Calculate energy changes in chemical processes.
•
Equilibrium Concepts (ability_6)
: Analyze dynamic equilibrium in chemical systems.
•
Acid-Base and p-Scales (ability_7)
: Interpret acid-base behavior and pH calculations.
•
Buffers and Titrations (ability_8)
: Design and analyze buffer systems and titration curves.
•
Potentials and Nernst (ability_9)
: Calculate electrochemical potentials using Nernst equation.
•
Faraday Laws and Charge Accounting (ability_10)
: Relate electrical charge to chemical change in electrochemistry.
•
Cell Notation and Conventions (ability_11)
: Interpret standard electrochemical cell diagrams.
•
Rate Laws and Integrated Forms (ability_12)
: Determine reaction rates and integrated rate equations.
•
Mechanisms and Approximations (ability_13)
: Analyze reaction mechanisms and kinetic approximations.
•
Hydrogenic Models and Energy Levels (ability_14)
: Apply quantum models to atomic energy systems.
•
Selection Rules and Photon Relations (ability_15)
: Interpret spectroscopic transitions and photon interactions.
•
Uncertainty and Time-Energy Relations (ability_16)
: Apply quantum uncertainty principles in chemical contexts.
•
Magnetic Resonance (EPR/NMR) (ability_17)
: Analyze molecular structure using spectroscopic techniques.
•
Optical Absorption (ability_18)
: Interpret absorption spectra and Beer-Lambert law applications.
•
Crystal Structures and Geometry (ability_19)
: Describe crystalline arrangements and symmetry.
•
Lattice Parameters and Distances (ability_20)
: Calculate unit cell dimensions and interatomic distances.
•
Crystal Density and Formula Units (ability_21)
: Determine crystal densities from structural data.
•
Reaction Stoichiometry and Balancing (ability_22)
: Balance chemical equations and apply stoichiometric ratios.
•
Mass-Mole-Amount Conversions (ability_23)
: Convert between mass, moles, and particle quantities.
•
Precipitation and Solubility Rules (ability_24)
: Predict precipitation and solubility behavior.
•
Concentration Measures (ability_25)
: Calculate and convert between concentration units.
•
Colligative Properties (ability_26)
: Analyze vapor pressure, boiling point, and freezing point changes.
•
Decay Laws and Activity (ability_27)
: Apply radioactive decay kinetics to nuclear processes.
•
Particle Properties (ability_28)
: Characterize subatomic particles and their interactions.
•
Functional Groups and Nomenclature (ability_29)
: Identify organic functional groups and apply IUPAC naming.
•
Representative Reactions (ability_30)
: Recognize characteristic organic reaction types.
•
Biomolecules and Properties (ability_31)
: Analyze structures and functions of biological macromolecules.
•
Toxicology and Safety (ability_32)
: Evaluate chemical hazards and safety protocols.
•
Notation and Precision (ability_33)
: Apply significant figures and precision in chemical reporting.
•
Stoichiometric and Equilibrium Schemas (ability_34)
: Construct reaction schematics for complex systems.
•
Factual Knowledge (ability_35)
: Recall fundamental chemical facts and constants.
•
Conceptual Understanding (ability_36)
: Explain chemical principles and relationships.
•
Procedural Skill (ability_37)
: Execute chemical problem-solving procedures.
•
Conceptual Interpretation (ability_38)
: Interpret conceptual relationships in chemical systems.
•
Representation Translation (ability_39)
: Convert between symbolic, graphical, and verbal representations.
•
Summarization and Categorization (ability_40)
: Synthesize information and classify chemical concepts.
•
Quantitative Computation and Unit Management (ability_41)
: Perform numerical calculations with proper unit handling.
•
Stoichiometric Reasoning and Bookkeeping (ability_42)
: Track material balances in chemical processes.
•
Modeling and Equation Setup (ability_43)
: Formulate mathematical models for chemical phenomena.
•
Problem Decomposition and Constraint Analysis (ability_44)
: Break down complex problems and identify constraints.
•
Comparative and Sign-Sensitive Reasoning (ability_45)
: Compare chemical behaviors and interpret sign-dependent phenomena.
•
Pattern Recognition and Trend Analysis (ability_46)
: Identify patterns and trends in chemical data.
•
Assumption and Approximation Management (ability_47)
: Evaluate and justify modeling assumptions.
•
Option Screening and Decision (ability_48)
: Select appropriate methods and evaluate alternatives.
•
Error Checking and Propagation (ability_49)
: Verify results and analyze error propagation.
•
Model Building and Equation Synthesis (ability_50)
: Construct and synthesize chemical models.
•
Multi-step Planning and Integration (ability_51)
: Design integrated solution pathways for complex problems.
•
Algorithmic and Computational Fluency (ability_52)
: Execute computational procedures efficiently.
•
Problem Solving and Strategy (ability_53)
: Apply strategic approaches to chemical problem-solving.
•
Reasoning and Algebra (ability_54)
: Apply algebraic reasoning to chemical problems.
•
Data Handling and Extraction (ability_55)
: Process and extract information from chemical data.
•
Unit Consistency and Dimensional Reasoning (ability_56)
: Ensure dimensional consistency in calculations.
•
Decision and Option Management (ability_57)
: Evaluate and manage decision options in chemical contexts.
C.3
Computer Science
The computer science taxonomy comprises 12 fine-grained abilities spanning discrete foundations, data systems, algorithmic reasoning, and professional practice. The complete list is presented below.
•
Discrete Mathematics (ability_0)
: Apply logic, set theory, combinatorics, and graph theory to computational problems.
•
Data Representation and Formats (ability_1)
: Encode and interpret data using appropriate structures and encoding schemes.
•
Data Management and Query (ability_2)
: Design and query databases using relational or non-relational paradigms.
•
Data Analysis and Machine Learning (ability_3)
: Analyze datasets and apply supervised or unsupervised learning techniques.
•
Societal Impact and Policy (ability_4)
: Evaluate broader societal implications, legal frameworks, and policy considerations of computing technologies.
•
Algorithmic Problem Solving (ability_5)
: Design and analyze algorithms for computational tasks with attention to correctness and efficiency.
•
Abstraction and Modeling (ability_6)
: Construct abstract representations of real-world problems for computational solution.
•
Data Reasoning (ability_7)
: Infer patterns, relationships, and insights from structured or unstructured data.
•
Systems Thinking (ability_8)
: Analyze interactions between components in complex computational systems.
•
Debugging and Testing (ability_9)
: Identify, isolate, and resolve errors through systematic testing and validation.
•
Communication and Collaboration (ability_10)
: Articulate technical concepts and collaborate effectively in team settings.
•
Ethical Decision Making (ability_11)
: Apply ethical frameworks to navigate dilemmas in software development and deployment.
Appendix D
Experiment Setup Details
We evaluate 41 language models on three mathematical benchmarks (MMLU-MATH, MMLU-Pro-MATH, and MATH500). For each model, we derive a 35-dimensional ability profile using multidimensional item response theory (mIRT) with the Q-matrix defined in Appendix B. The validity of these profiles is assessed along three dimensions: (1) construct validity through internal consistency, (2) cross-benchmark reliability, and (3) predictive utility for held-out item performance. Additionally, we evaluate cross-domain generalization by applying the same profiling pipeline to three non-mathematical subsets of MMLU-Pro (Chemistry, Physics, and Computer Science).
D.1
Evaluated Models
We evaluate a total of 41 language models across two categories: online API models and open-source models. The full list is presented in Table
1
.
Table 1:
List of evaluated language models with unique identifiers.
ID
Category
Series
Model
Parameter Size
1
Online Model
DeepSeek
deepseek-v3.2
N/A
2
deepseek-v3
N/A
3
GPT
gpt-4o
N/A
4
gpt-5.1
N/A
5
gpt-o1
N/A
6
gpt-o3
N/A
7
Open Source Model
Gemma3
gemma3-12b-it
12B
8
gemma3-1b-it
1B
9
gemma3-4b-it
4B
10
GPT
gpt-oss-20b
20B
11
Llama3
Llama3-8B-Instruct
8B
12
Llama3-8B
8B
13
Llama3.1
Llama3.1-8B-Instruct
8B
14
Llama3.1-8B
8B
15
Llama3.2
Llama3.2-1B-Instruct
1B
16
Llama3.2-1B
1B
17
Llama3.2-3B-Instruct
3B
18
Llama3.2-3B
3B
19
Mistral
Mistral-7B-Instruct-v0_1
7B
20
Mistral-7B-Instruct-v0_2
7B
21
Mistral-7B-Instruct-v0_3
7B
22
Qwen2.5
qwen2.5-0.5b-instruct
0.5B
23
qwen2.5-0.5b
0.5B
24
qwen2.5-1.5b-instruct
1.5B
25
qwen2.5-1.5b
1.5B
26
qwen2.5-14b-instruct
14B
27
qwen2.5-14b
14B
28
qwen2.5-32b-instruct
32B
29
qwen2.5-32b
32B
30
qwen2.5-3b-instruct
3B
31
qwen2.5-3b
3B
32
qwen2.5-7b-instruct
7B
33
qwen2.5-7b
7B
34
Qwen3
qwen3-0.6b
0.6B
35
qwen3-1.7b
1.7B
36
qwen3-14b
14B
37
qwen3-30b-a3b
30B
38
qwen3-32b
32B
39
qwen3-4b
4B
40
qwen3-8b
8B
41
QwQ
qwq-32b
32B
D.2
Evaluated Benchmarks
We evaluate models on six subsets across three benchmark suites: MMLU, MMLU-Pro, and MATH500. The full list is presented in Table
2
.
Table 2:
List of evaluated benchmarks with detailed metadata.
ID
Subject
Name
# Items
Source
Answer Format
1
Math
MMLU-MATH
748
cais/mmlu
Multiple-choice
2
MMLU-Pro-MATH
1351
TIGER-Lab/MMLU-Pro
Multiple-choice
3
MATH500
500
HuggingFaceH4/MATH-500
Free-response
4
Chemistry
MMLU-Pro-Chemistry
1132
TIGER-Lab/MMLU-Pro
Multiple-choice
5
Physics
MMLU-Pro-Physics
1299
TIGER-Lab/MMLU-Pro
Multiple-choice
6
Computer science
MMLU-Pro-CS
410
TIGER-Lab/MMLU-Pro
Multiple-choice
We quantify the coverage of each of the 35 fine-grained abilities across the three mathematical benchmarks (MMLU-MATH, MMLU-Pro-MATH, MATH500) by counting the number of items associated with each ability in the Q-matrix. Table
3
reports both absolute counts and relative proportions (radio = count / total items per benchmark).
D.3
Ability Coverage Statistics of Mathematical Benchmarks
As shown in Table
3
, we analysis the item coverage of each ability across three mathematical benchmarks.
Table 3
:
Item coverage of per ability dimension across mathematical benchmarks.
Dimension
MMLU-MATH
MMLU-Pro-MATH
MATH500
Count
Ratio
Count
Ratio
Count
Ratio
ability_0
61
0.0816
55
0.0407
20
0.0400
ability_1
340
0.4545
300
0.2221
125
0.2500
ability_2
77
0.1029
112
0.0829
84
0.1680
ability_3
183
0.2447
189
0.1399
167
0.3340
ability_4
23
0.0307
57
0.0422
64
0.1280
ability_5
41
0.0548
68
0.0503
41
0.0820
ability_6
36
0.0481
81
0.0600
45
0.0900
ability_7
37
0.0495
62
0.0459
73
0.1460
ability_8
30
0.0401
38
0.0281
56
0.1120
ability_9
49
0.0655
58
0.0429
47
0.0940
ability_10
11
0.0147
67
0.0496
3
0.0060
ability_11
30
0.0401
121
0.0896
15
0.0300
ability_12
16
0.0214
113
0.0836
0
0.0000
ability_13
15
0.0201
72
0.0533
4
0.0080
ability_14
38
0.0508
189
0.1399
16
0.0320
ability_15
3
0.0040
99
0.0733
0
0.0000
ability_16
18
0.0241
54
0.0400
24
0.0480
ability_17
8
0.0107
18
0.0133
8
0.0160
ability_18
12
0.0160
27
0.0200
2
0.0040
ability_19
28
0.0374
104
0.0770
5
0.0100
ability_20
60
0.0802
147
0.1088
61
0.1220
ability_21
3
0.0040
12
0.0089
0
0.0000
ability_22
2
0.0027
2
0.0015
0
0.0000
ability_23
19
0.0254
72
0.0533
1
0.0020
ability_24
40
0.0535
87
0.0644
10
0.0200
ability_25
40
0.0535
107
0.0792
37
0.0740
ability_26
42
0.0561
173
0.1281
83
0.1660
ability_27
442
0.5909
838
0.6203
330
0.6600
ability_28
103
0.1377
130
0.0962
20
0.0400
ability_29
77
0.1029
240
0.1776
111
0.2220
ability_30
1
0.0013
1
0.0007
0
0.0000
ability_31
0
0.0000
3
0.0022
2
0.0040
ability_32
0
0.0000
0
0.0000
0
0.0000
ability_33
0
0.0000
0
0.0000
0
0.0000
ability_34
1
0.0013
2
0.0015
0
0.0000
D.4
Correlation Analysis
We adopt the Spearman rank correlation coefficient (
ρ
\rho
) as the primary measure of association for three reasons. First, ability estimates from multidimensional item response theory (mIRT) are interval-scale but may violate the linearity and normality assumptions required by Pearson correlation. Second, our focus is on
rank-order consistency
of model capabilities (e.g., whether a model consistently ranks higher across abilities), which Spearman directly captures. Third, Spearman correlation is robust to outliers and monotonic nonlinearities, critical given the heterogeneous performance distributions across 41 models and 35 ability dimensions.
To assess the validity and consistency of fine-grained ability profiles, we compute pairwise Spearman rank correlations between model ability vectors across the 35 mathematical dimensions.
Ability-Performance Association.
For each ability dimension
i
i
, we compute the Spearman correlation between models’ estimated abilities on dimension
i
i
and their observed accuracy on items associated with that dimension. The observed accuracy of
m
m
-th model for dimension
i
i
on a benchmark is calculated as:
ACC
m
​
i
=
∑
j
=
1
N
q
j
​
i
⋅
r
j
​
m
∑
j
=
1
N
q
j
​
i
,
\mathrm{ACC}_{mi}=\frac{\sum_{j=1}^{N}q_{ji}\cdot r_{jm}}{\sum_{j=1}^{N}q_{ji}},
(3)
where:
•
q
j
​
i
∈
{
0
,
1
}
q_{ji}\in\{0,1\}
is the Q-matrix entry indicating whether item
j
j
requires ability
i
i
,
•
r
j
​
m
∈
{
0
,
1
}
r_{jm}\in\{0,1\}
is the correctness of
m
m
-th model’s binary response on item
j
j
,
•
N
N
is the total number of items in the benchmark.
This metric represents the proportion of correctly answered items among those that load on ability
i
i
.
Cross-Benchmark Consistency.
For each model, we compute the Spearman correlation between its ability profiles estimated from different mathematical benchmarks. High correlation indicates stable rank-order ability estimation across benchmark pairs.
Appendix E
Unseen Item Prediction Details
This appendix provides per-model results for unseen item prediction experiments described in Section
3.4
. For within-benchmark prediction, we perform 10 independent random splits (90% evaluation set, 10% prediction set) per model. For cross-benchmark prediction, we use the source benchmark for ability estimation and the target benchmark for prediction. All predictions use fixed item parameters (
I
diff
=
0.5
I_{\text{diff}}=0.5
,
I
disc
=
1.0
I_{\text{disc}}=1.0
) for unseen items.
E.1
Within-Benchmark Prediction Performance
Table
4
reports prediction performance for all 41 models across three mathematical benchmarks. All results substantially exceed trivial baselines (accuracy-based: AUC = 0.500; unidimensional IRT: AUC = 0.500; random prediction: mean AUC
≈
\approx
0.49).
Table 4
:
Within-benchmark unseen item prediction performance per model (AUC
±
\pm
std over 10 random splits with different seeds).
Model
MMLU-MATH
MATH500
MMLU-Pro-MATH
0
0.8711
±
\pm
0.0489
0.8732
±
\pm
0.0401
0.8522
±
\pm
0.0303
1
0.8672
±
\pm
0.0356
0.8434
±
\pm
0.0863
0.8683
±
\pm
0.0288
2
0.8548
±
\pm
0.0338
0.8049
±
\pm
0.0681
0.8584
±
\pm
0.0222
3
0.8560
±
\pm
0.0593
0.8557
±
\pm
0.0405
0.8573
±
\pm
0.0398
4
0.8583
±
\pm
0.0607
0.8634
±
\pm
0.0654
0.8547
±
\pm
0.0316
5
0.8474
±
\pm
0.0331
0.8586
±
\pm
0.0552
0.8517
±
\pm
0.0480
6
0.8586
±
\pm
0.0283
0.8396
±
\pm
0.0604
0.8474
±
\pm
0.0485
7
0.8761
±
\pm
0.0265
0.8513
±
\pm
0.0627
0.8593
±
\pm
0.0232
8
0.8526
±
\pm
0.0420
0.8552
±
\pm
0.0534
0.8582
±
\pm
0.0298
9
0.8465
±
\pm
0.0470
0.8336
±
\pm
0.0697
0.8595
±
\pm
0.0288
10
0.8599
±
\pm
0.0554
0.8446
±
\pm
0.0297
0.8638
±
\pm
0.0320
11
0.8495
±
\pm
0.0320
0.8459
±
\pm
0.0413
0.8479
±
\pm
0.0319
12
0.8282
±
\pm
0.0194
0.8529
±
\pm
0.0481
0.8437
±
\pm
0.0133
13
0.8248
±
\pm
0.0553
0.8698
±
\pm
0.0620
0.8485
±
\pm
0.0349
14
0.8587
±
\pm
0.0416
0.8816
±
\pm
0.0483
0.8432
±
\pm
0.0402
15
0.8581
±
\pm
0.0372
0.8552
±
\pm
0.0507
0.8551
±
\pm
0.0180
16
0.8526
±
\pm
0.0392
0.8862
±
\pm
0.0540
0.8667
±
\pm
0.0203
17
0.8563
±
\pm
0.0295
0.8774
±
\pm
0.0322
0.8374
±
\pm
0.0325
18
0.8500
±
\pm
0.0356
0.8618
±
\pm
0.0568
0.8625
±
\pm
0.0385
19
0.8273
±
\pm
0.0334
0.8813
±
\pm
0.0416
0.8456
±
\pm
0.0363
20
0.8688
±
\pm
0.0344
0.8449
±
\pm
0.0335
0.8693
±
\pm
0.0323
21
0.8555
±
\pm
0.0592
0.8699
±
\pm
0.0504
0.8557
±
\pm
0.0488
22
0.8612
±
\pm
0.0534
0.8336
±
\pm
0.0874
0.8412
±
\pm
0.0397
23
0.8638
±
\pm
0.0366
0.8516
±
\pm
0.0545
0.8546
±
\pm
0.0281
24
0.8423
±
\pm
0.0392
0.8347
±
\pm
0.0689
0.8398
±
\pm
0.0254
25
0.8378
±
\pm
0.0486
0.8415
±
\pm
0.0466
0.8558
±
\pm
0.0230
26
0.8355
±
\pm
0.0362
0.8317
±
\pm
0.0513
0.8650
±
\pm
0.0427
27
0.8603
±
\pm
0.0352
0.8478
±
\pm
0.0350
0.8586
±
\pm
0.0329
28
0.8429
±
\pm
0.0544
0.8635
±
\pm
0.0288
0.8567
±
\pm
0.0231
29
0.8523
±
\pm
0.0358
0.8268
±
\pm
0.0786
0.8350
±
\pm
0.0289
30
0.8480
±
\pm
0.0459
0.8547
±
\pm
0.0289
0.8588
±
\pm
0.0346
31
0.8401
±
\pm
0.0356
0.8387
±
\pm
0.0667
0.8429
±
\pm
0.0340
32
0.8371
±
\pm
0.0543
0.8941
±
\pm
0.0290
0.8505
±
\pm
0.0265
33
0.8157
±
\pm
0.0766
0.8474
±
\pm
0.0411
0.8343
±
\pm
0.0342
34
0.8548
±
\pm
0.0604
0.8634
±
\pm
0.0418
0.8540
±
\pm
0.0475
35
0.8660
±
\pm
0.0421
0.8782
±
\pm
0.0305
0.8582
±
\pm
0.0263
36
0.8526
±
\pm
0.0335
0.8576
±
\pm
0.0578
0.8462
±
\pm
0.0277
37
0.8703
±
\pm
0.0518
0.8893
±
\pm
0.0414
0.8657
±
\pm
0.0311
38
0.8451
±
\pm
0.0391
0.8799
±
\pm
0.0467
0.8635
±
\pm
0.0201
39
0.8218
±
\pm
0.0407
0.8521
±
\pm
0.0526
0.8587
±
\pm
0.0439
40
0.8576
±
\pm
0.0375
0.8718
±
\pm
0.0523
0.8654
±
\pm
0.0254
The results demonstrate consistently strong predictive performance across all models and benchmarks, with mean AUC values ranging from 0.8049 to 0.8941. Standard deviations remain modest (typically
<
0.06
<0.06
), indicating stable prediction quality across random item partitions.
E.2
Cross-Benchmark Prediction Performance
Table
5
reports prediction performance for all 41 models across six ordered benchmark pairs. For each pair, we use the source benchmark for ability estimation and the target benchmark for prediction. All results substantially exceed trivial baselines (accuracy-based: AUC = 0.500; unidimensional IRT: AUC = 0.500; random prediction: mean AUC
≈
\approx
0.49).
Table 5
:
Cross-benchmark unseen item prediction performance per model (AUC
±
\pm
std over repeat for 10 times).
Model
MMLU
→
\rightarrow
MATH500
MMLU
→
\rightarrow
MMLU-Pro
MATH500
→
\rightarrow
MMLU
MATH500
→
\rightarrow
MMLU-Pro
MMLU-Pro
→
\rightarrow
MMLU
MMLU-Pro
→
\rightarrow
MATH500
0
0.7686
±
\pm
0.0070
0.8345
±
\pm
0.0035
0.8254
±
\pm
0.0027
0.8305
±
\pm
0.0023
0.8448
±
\pm
0.0057
0.7870
±
\pm
0.0022
1
0.7942
±
\pm
0.0031
0.8329
±
\pm
0.0032
0.8132
±
\pm
0.0017
0.8106
±
\pm
0.0022
0.8330
±
\pm
0.0030
0.8287
±
\pm
0.0045
2
0.7766
±
\pm
0.0033
0.8385
±
\pm
0.0035
0.8498
±
\pm
0.0032
0.8203
±
\pm
0.0017
0.8521
±
\pm
0.0038
0.7953
±
\pm
0.0028
3
0.7784
±
\pm
0.0041
0.8425
±
\pm
0.0046
0.8390
±
\pm
0.0017
0.8268
±
\pm
0.0019
0.8636
±
\pm
0.0046
0.7917
±
\pm
0.0052
4
0.8085
±
\pm
0.0052
0.8288
±
\pm
0.0041
0.8299
±
\pm
0.0019
0.8110
±
\pm
0.0018
0.8309
±
\pm
0.0047
0.8201
±
\pm
0.0028
5
0.7774
±
\pm
0.0036
0.8457
±
\pm
0.0045
0.8158
±
\pm
0.0049
0.8172
±
\pm
0.0020
0.8145
±
\pm
0.0042
0.8197
±
\pm
0.0024
6
0.8043
±
\pm
0.0047
0.8336
±
\pm
0.0044
0.8353
±
\pm
0.0028
0.8076
±
\pm
0.0025
0.8488
±
\pm
0.0048
0.8204
±
\pm
0.0075
7
0.8031
±
\pm
0.0077
0.8338
±
\pm
0.0038
0.8099
±
\pm
0.0018
0.8320
±
\pm
0.0014
0.8273
±
\pm
0.0075
0.8346
±
\pm
0.0040
8
0.8107
±
\pm
0.0058
0.8453
±
\pm
0.0035
0.8229
±
\pm
0.0051
0.8310
±
\pm
0.0018
0.8333
±
\pm
0.0034
0.8271
±
\pm
0.0031
9
0.8244
±
\pm
0.0053
0.8338
±
\pm
0.0023
0.8457
±
\pm
0.0035
0.8041
±
\pm
0.0030
0.8464
±
\pm
0.0015
0.8363
±
\pm
0.0048
10
0.8331
±
\pm
0.0061
0.8268
±
\pm
0.0025
0.8240
±
\pm
0.0027
0.8005
±
\pm
0.0022
0.8518
±
\pm
0.0024
0.8420
±
\pm
0.0015
11
0.8056
±
\pm
0.0036
0.8421
±
\pm
0.0020
0.8305
±
\pm
0.0017
0.8242
±
\pm
0.0023
0.8362
±
\pm
0.0044
0.8310
±
\pm
0.0034
12
0.7813
±
\pm
0.0057
0.8362
±
\pm
0.0051
0.8208
±
\pm
0.0028
0.8187
±
\pm
0.0016
0.8393
±
\pm
0.0049
0.7841
±
\pm
0.0043
13
0.7821
±
\pm
0.0042
0.8438
±
\pm
0.0031
0.8361
±
\pm
0.0038
0.8192
±
\pm
0.0021
0.8476
±
\pm
0.0050
0.8145
±
\pm
0.0038
14
0.7810
±
\pm
0.0061
0.8286
±
\pm
0.0017
0.8297
±
\pm
0.0029
0.8161
±
\pm
0.0022
0.8459
±
\pm
0.0040
0.8027
±
\pm
0.0021
15
0.8053
±
\pm
0.0045
0.8556
±
\pm
0.0024
0.8454
±
\pm
0.0032
0.8297
±
\pm
0.0024
0.8413
±
\pm
0.0045
0.8338
±
\pm
0.0074
16
0.8003
±
\pm
0.0055
0.8275
±
\pm
0.0026
0.8347
±
\pm
0.0033
0.8031
±
\pm
0.0022
0.8643
±
\pm
0.0025
0.8333
±
\pm
0.0023
17
0.7788
±
\pm
0.0051
0.8513
±
\pm
0.0018
0.8094
±
\pm
0.0024
0.8274
±
\pm
0.0017
0.8105
±
\pm
0.0084
0.8071
±
\pm
0.0040
18
0.8091
±
\pm
0.0043
0.8410
±
\pm
0.0029
0.8342
±
\pm
0.0024
0.8162
±
\pm
0.0023
0.8351
±
\pm
0.0061
0.8336
±
\pm
0.0041
19
0.7826
±
\pm
0.0084
0.8438
±
\pm
0.0029
0.8174
±
\pm
0.0043
0.8128
±
\pm
0.0034
0.8459
±
\pm
0.0021
0.7979
±
\pm
0.0051
20
0.7935
±
\pm
0.0037
0.8292
±
\pm
0.0023
0.8198
±
\pm
0.0020
0.8203
±
\pm
0.0021
0.8344
±
\pm
0.0052
0.8146
±
\pm
0.0032
21
0.7901
±
\pm
0.0022
0.8296
±
\pm
0.0023
0.8461
±
\pm
0.0020
0.8093
±
\pm
0.0018
0.8408
±
\pm
0.0029
0.8085
±
\pm
0.0026
22
0.8144
±
\pm
0.0050
0.8319
±
\pm
0.0033
0.8453
±
\pm
0.0018
0.8202
±
\pm
0.0012
0.8542
±
\pm
0.0075
0.8350
±
\pm
0.0025
23
0.8009
±
\pm
0.0068
0.8330
±
\pm
0.0036
0.8438
±
\pm
0.0022
0.8216
±
\pm
0.0019
0.8474
±
\pm
0.0029
0.8339
±
\pm
0.0023
24
0.7912
±
\pm
0.0061
0.8350
±
\pm
0.0038
0.8169
±
\pm
0.0038
0.8130
±
\pm
0.0032
0.8179
±
\pm
0.0054
0.8259
±
\pm
0.0032
25
0.7684
±
\pm
0.0043
0.8352
±
\pm
0.0030
0.8218
±
\pm
0.0035
0.8144
±
\pm
0.0024
0.8479
±
\pm
0.0026
0.7867
±
\pm
0.0031
26
0.7891
±
\pm
0.0031
0.8349
±
\pm
0.0033
0.8253
±
\pm
0.0034
0.8121
±
\pm
0.0023
0.8374
±
\pm
0.0049
0.8025
±
\pm
0.0030
27
0.7930
±
\pm
0.0047
0.8331
±
\pm
0.0036
0.8231
±
\pm
0.0041
0.8111
±
\pm
0.0028
0.8234
±
\pm
0.0065
0.8132
±
\pm
0.0051
28
0.8026
±
\pm
0.0062
0.8062
±
\pm
0.0047
0.8139
±
\pm
0.0025
0.8046
±
\pm
0.0019
0.8330
±
\pm
0.0059
0.8006
±
\pm
0.0030
29
0.7743
±
\pm
0.0061
0.8439
±
\pm
0.0035
0.8204
±
\pm
0.0027
0.8236
±
\pm
0.0017
0.8353
±
\pm
0.0054
0.8045
±
\pm
0.0031
30
0.7927
±
\pm
0.0054
0.8387
±
\pm
0.0037
0.8349
±
\pm
0.0020
0.8299
±
\pm
0.0019
0.8441
±
\pm
0.0046
0.8014
±
\pm
0.0032
31
0.8067
±
\pm
0.0048
0.8355
±
\pm
0.0029
0.8484
±
\pm
0.0018
0.8123
±
\pm
0.0022
0.8461
±
\pm
0.0051
0.8331
±
\pm
0.0068
32
0.8078
±
\pm
0.0061
0.8262
±
\pm
0.0021
0.8114
±
\pm
0.0022
0.8261
±
\pm
0.0024
0.8034
±
\pm
0.0081
0.8292
±
\pm
0.0031
33
0.7914
±
\pm
0.0052
0.8373
±
\pm
0.0046
0.8156
±
\pm
0.0023
0.8298
±
\pm
0.0023
0.8270
±
\pm
0.0050
0.8077
±
\pm
0.0025
34
0.7742
±
\pm
0.0056
0.8273
±
\pm
0.0032
0.8274
±
\pm
0.0020
0.8145
±
\pm
0.0022
0.8442
±
\pm
0.0040
0.7980
±
\pm
0.0027
35
0.7920
±
\pm
0.0051
0.8433
±
\pm
0.0025
0.8149
±
\pm
0.0010
0.8297
±
\pm
0.0013
0.8113
±
\pm
0.0059
0.8069
±
\pm
0.0039
36
0.7718
±
\pm
0.0059
0.8349
±
\pm
0.0038
0.8175
±
\pm
0.0017
0.8051
±
\pm
0.0014
0.8222
±
\pm
0.0043
0.7898
±
\pm
0.0062
37
0.7820
±
\pm
0.0056
0.8402
±
\pm
0.0044
0.8188
±
\pm
0.0034
0.8103
±
\pm
0.0011
0.8378
±
\pm
0.0039
0.7968
±
\pm
0.0037
38
0.7688
±
\pm
0.0077
0.8253
±
\pm
0.0030
0.8042
±
\pm
0.0050
0.7895
±
\pm
0.0021
0.8273
±
\pm
0.0043
0.7958
±
\pm
0.0031
39
0.8058
±
\pm
0.0035
0.8426
±
\pm
0.0028
0.8179
±
\pm
0.0041
0.8225
±
\pm
0.0028
0.8344
±
\pm
0.0056
0.8267
±
\pm
0.0044
40
0.7864
±
\pm
0.0067
0.8444
±
\pm
0.0031
0.7991
±
\pm
0.0020
0.8267
±
\pm
0.0029
0.8142
±
\pm
0.0087
0.8070
±
\pm
0.0015
The results demonstrate consistent cross-benchmark generalization with mean AUC values ranging from 0.7684 to 0.8556. Performance remains stable across all model-benchmark pairs, with standard deviations typically
<
0.008
<0.008
, confirming the framework’s robustness in transferring ability estimates across domains.