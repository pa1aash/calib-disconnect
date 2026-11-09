---
title: 'FASE: Fast Adaptive Semantic Entropy for Code Quality'
id: fase-fast-adaptive-semantic-entropy-for-code-quality
tags:
- code-llm-calibration-aaai27-eabf3f
- semantic-entropy
- embedding-clustering
- multi-agent
created: '2026-07-17T18:30:55.113214Z'
updated: '2026-07-17T18:33:28.938850Z'
source: https://arxiv.org/html/2606.09800
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:55.112454Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'University of Waterloo (Lin, Tahvildari). Targets multi-agent code-gen reliability
  by replacing costly LLM-driven bidirectional-entailment semantic entropy with Fast
  Adaptive Semantic Entropy (FASE): builds a pairwise cosine-distance matrix from
  code embeddings (Qwen3-Embedding, GTE-ModernBERT, Llama-Embed-Nemotron, All-MiniLM),
  extracts a minimum spanning tree, and adaptively sets the DBSCAN/HDBSCAN clustering
  radius from the scaled MST-mode edge weight -- entirely execution-free and judge-free.
  Evaluated on HumanEval (164 problems) and BigCodeBench-hard (148 problems) using
  four 7B open-weight coders: Mistral-7B, CodeLlama-7B, DeepSeek-Coder-7B, and Qwen2.5-Coder-7B
  (temperature 0.5, top_p 0.95, m=10 samples) -- directly overlapping model family
  with our paper. Headline: FASE (scaled MST-mode) beats LLM-entailment semantic entropy
  by ~25% average Spearman correlation and ~8-19% AUC on average; per-model AUC vs
  pass@1: DeepSeek-Coder 0.74 (coder-only) / 0.91 (with analyst agent), Qwen2.5-Coder
  0.76 (coder-only) / underperformed by naive semantic entropy at 0.90 with analyst.
  FASE-union-structural-entropy (AST-based) hybrid is strongest overall because embeddings
  alone miss single-token/operator semantic flips (e.g., range(n) vs range(n+1)) that
  ASTs catch. Cost: ~0.3% of the runtime of LLM-judge equivalence checks (0.02-0.36s
  embedding vs 17-111s LLM-judge per 10-sample batch). Explicit limitations: only
  7B models tested (compute-constrained, matching our single-GPU regime), simple prompting
  only, and FASE cannot detect cases where all samples consistently drift to the SAME
  wrong answer (low entropy but wrong) -- a structural blind spot shared by any consistency-based
  proxy including plain sampling pass-rate proxies. Relation to disconnect thesis:
  like the Functional Entropy paper, this occupies the ''better internal/proxy signal''
  space (cheap embedding-based clustering as a stand-in for execution) rather than
  the expressed-interface problem; it doesn''t touch log-probs, verbalized confidence,
  or post-hoc calibration at all. Useful as a cheap AST/embedding-clustering baseline
  our expressed-confidence method should be compared against, and as evidence that
  consistency-based signals (however computed) share a common blind spot (correlated
  wrong answers).'
---

FASE: Fast Adaptive Semantic Entropy for Code Quality
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY-NC-SA 4.0
arXiv:2606.09800v1 [cs.SE] 08 Jun 2026
FASE: Fast Adaptive Semantic Entropy for Code Quality
Shizhe Lin
University of Waterloo
Waterloo
Canada
s222lin@uwaterloo.ca
0009-0005-2766-0281
and
Ladan Tahvildari
University of Waterloo
Waterloo
Canada
ltahvild@uwaterloo.ca
0000-0001-8314-5560
(5 June 2026)
Abstract.
Multi-agent code generation offers a promising paradigm for autonomous software development by simulating the human software engineering lifecycle. However, system reliability remains hindered by LLM hallucinations and error propagation across interacting agents. While semantic entropy provides a principled way to quantify uncertainty without ground-truth answers, current methods often rely on costly LLM-driven equivalence checks. In this work, we introduce Fast Adaptive Semantic Entropy (FASE), a novel metric that approximates functional correctness based on the minimum spanning tree of structural and semantic dissimilarity graphs. Evaluations on HumanEval and BigCodeBench demonstrate that FASE outperforms state-of-the-art semantic entropy by LLM entailment, achieving a 25% average improvement in Spearman correlation and a 19% increase in ROCAUC score against Pass@1 from ground-truth test cases when using the Qwen3-Embedding-8B model. Furthermore, by eliminating costly LLM-driven equivalence evaluation, FASE incurs negligible computational overhead, requiring only approximately 0.3% of the runtime cost of traditional semantic entropy approaches. These results position FASE as a practical, cost-effective solution for optimizing uncertainty quantification in real-world multi-agent workflows.
Generative AI, Agentic Code Generation, Adaptive Workflow, Trust in Agent Output
†
†
copyright:
acmlicensed
†
†
journalyear:
2026
†
†
doi:
XXXXXXX.XXXXXXX
†
†
conference:
ACM Transactions on Software Engineering and Methodology; August 1–2,
2026; place, HOLDER
†
†
isbn:
978-1-4503-XXXX-X/2018/06
†
†
ccs:
Mathematics of computing Information theory
†
†
ccs:
Software and its engineering Automatic programming
†
†
ccs:
Computing methodologies Artificial intelligence
1.
Introduction
Recent advances in large language models (LLMs) have accelerated the emergence of autonomous multi-agent systems for software engineering tasks
(Ferrag
et al.
,
2025
; Liu
et al.
,
2024b
; He
et al.
,
2025
)
. Rather than relying on a single model to generate code end-to-end, modern frameworks increasingly decompose software development into collaborative workflows involving specialized agents responsible for requirement analysis, planning, coding, testing, debugging, and review
(Talebirad and Nadiri,
2023
; Dong
et al.
,
2024
)
. Inspired by human software engineering practices, systems such as MetaGPT
(Hong
et al.
,
2024
)
, CodeCoR
(Pan
et al.
,
2025
)
, and AdaCoder
(Zhu
et al.
,
2025b
)
demonstrate that role specialization and structured collaboration can substantially improve code generation quality and task-solving capability for complex programming problems. These agentic workflows further enable LLMs to address repository-level development tasks, long-horizon reasoning, and iterative refinement processes that are difficult for standalone models to handle effectively.
Despite these advances, LLM-based software engineering systems remain fundamentally limited by hallucinations and uncertainty in generated outputs
(Liu
et al.
,
2024a
; Agarwal
et al.
,
2024
; Liu
et al.
,
2026
; Yehudai
et al.
,
2025
)
. Errors produced during early stages of reasoning or implementation can propagate across agents, leading to cascading failures throughout the development pipeline
(Mohammadi
et al.
,
2025
)
as shown in Fig.
1
. Existing approaches attempt to mitigate these issues through self-reflection
(Kadavath
et al.
,
2022
)
, retrieval-augmented generation
(Eghbali and Pradel,
2024
; Das
et al.
,
2025
)
, iterative debugging
(Ji
et al.
,
2023
; Fakhoury
et al.
,
2024
)
, static analysis
(Yang
et al.
,
2025
; Liu
et al.
,
2024c
)
, mutation testing
(Wang
et al.
,
2026
; Tip
et al.
,
2025
)
, and fuzz testing
(Chen
et al.
,
2025
; Cao
et al.
,
2025
)
. Recent frameworks also introduce consensus-based reasoning
(Xu
et al.
,
2026
)
, and repository-aware grounding strategies
(Liao
et al.
,
2024
)
to improve factual consistency and functional correctness.
Figure 1
.
The risk of hallucination from unreliable agents (red) undermines the credibility of coherent agents (blue) and propagates across different workflow architectures.
However, many of these techniques rely on expensive iterative interactions with LLMs, resulting in substantial computational overhead and limited scalability for real-world deployment. Entropy-based uncertainty estimation methods have recently been explored to evaluate the reliability of LLM-generated code without requiring ground-truth labels
(Kuhn
et al.
,
2023
)
. Semantic entropy
(Farquhar
et al.
,
2024
)
measures uncertainty by grouping outputs according to functional equivalence rather than textual similarity, but it requires bidirectional entailment checks using LLMs, which limits scalability in practical multi-agent systems. To improve efficiency, structural entropy
(Song
et al.
,
2025
)
has been proposed as an alternative designed specifically for source code. Nevertheless, structural similarity alone cannot fully capture program semantics, as functionally equivalent solutions may have different structures while structurally similar code may still exhibit different behaviours. Building upon the prior works, this paper makes the following contributions:
•
Lightweight semantic entropy via embedding models:
Fast Adaptive Semantic Entropy (FASE) that leverages the semantic signals captured by code embedding models and dynamically adapts clustering according to the unique structure of each programming task’s solution space. FASE enables the estimation of the functional correctness of LLM-generated code without requiring ground-truth test cases while incurring only negligible computational overhead.
•
Critical evaluation on estimation of code functional correctness:
Evaluation on the reliability and accuracy of the proposed FASE entropy against existing LLM-based semantic entropy methods, self-evaluation techniques, and other baseline approaches in terms of their correlation and predictive capability for code functional correctness.
•
Cost–accuracy trade-off analysis for multi-agent observation:
Quantitative comparison of computational runtime between FASE and other baselines, demonstrating that the proposed approaches offer substantially improved efficiency while maintaining useful correctness signals for scalable multi-agent systems.
The rest of the paper is organized as follows. Section
2
formalizes the problem and identifies the key research gaps. Section
3
presents the methodology of the proposed FASE approach. Section
4
outlines the research questions addressed in this work, details the experimental setup, reports the results, and provides a comprehensive analysis of the evaluation. The related work and state-of-the-art are listed in Section
5
. Section
6
discusses threats to validity. Finally, Section
7
concludes by summarizing the main findings and discussing future research directions.
2.
Problem Definition
The increasing adoption of LLM systems for software development creates a growing need for efficient and reliable methods to estimate the quality of generated code without relying on ground-truth test cases.
Entropy of LLM Output:
One common measure of uncertainty is the predictive entropy of the output distribution, which quantifies the amount of information the model has about the output given the input
(Lindley,
1956
)
:
P
​
E
​
(
X
)
=
H
​
(
Y
|
x
)
=
−
∑
P
​
(
y
|
x
)
​
ln
⁡
P
​
(
y
|
x
)
PE(X)=H(Y|x)=-\sum P(y|x)\ln P(y|x)
where the predictive entropy for an input
x
x
is defined as the conditional entropy of the output random variable
Y
Y
given
x
x
. Low predictive entropy reflects a sharply peaked output distribution, implying high model confidence, while high predictive entropy indicates a more uniform distribution in which many possible outputs have comparable likelihoods.
The derivation of entropy for a set of code samples
X
X
given a programming task is presented in Eq.
1
, where
c
c
denotes an equivalence class within the set of all possible classes
𝒞
\mathcal{C}
. In practice, however, only a finite set of code samples is available, and the computation should be based on individual output
s
s
observed within the sampled set.
(1)
P
​
E
​
(
X
)
=
H
​
(
𝒞
|
x
)
=
−
∑
c
P
​
(
c
|
x
)
​
log
⁡
P
​
(
c
|
x
)
=
−
∑
c
(
[
∑
s
∈
c
P
​
(
s
|
x
)
]
​
log
⁡
[
∑
s
∈
c
P
​
(
s
|
x
)
]
)
PE(X)=H(\mathcal{C}|x)=-\sum_{c}P(c|x)\log P(c|x)=-\sum_{c}\left(\left[\sum_{s\in c}P(s|x)\right]\log\left[\sum_{s\in c}P(s|x)\right]\right)
Textual, Structural and Semantic Equivalence:
The equivalence classes
c
c
of outputs are determined by clustering the results using an equivalence function
E
​
(
⋅
,
⋅
)
E(\cdot,\cdot)
. For a given equivalence class, all output sentences within the class are pairwise equivalent,
∀
s
,
s
′
∈
c
:
E
​
(
s
,
s
′
)
\forall s,s^{\prime}\in c:E(s,s^{\prime})
, meaning they convey the same content.
A straightforward approach to determining whether two outputs are equivalent is to compare their textual similarity but it fails to reliably distinguish between coherent and hallucinated responses
(Farquhar
et al.
,
2024
; Song
et al.
,
2025
)
. Structural entropy
(Song
et al.
,
2025
)
addresses this limitation by introducing a higher-level perspective that abstracts away trivial textual differences and groups code based on similarities in their abstract syntax trees. Nevertheless, solutions to programming tasks are not constrained to a single structural form, and functionally equivalent programs may exhibit diverse syntactic representations. To overcome this, recent work has proposed semantic entropy
(Farquhar
et al.
,
2024
)
through LLM-based bidirectional entailment, which quantifies uncertainty at the level of meaning rather than tokens, providing a more faithful estimate of a model’s confidence. However, applying this approach directly to programming tasks remains imperfect
(Maveli
et al.
,
2024
)
, as LLMs often fail to detect subtle code variations that can result in substantial differences in functionality.
There are three limitations of the current state-of-the-art entropy calculation:
•
The accuracy of bidirectional entailment relies on LLM’s self-evaluation capability; different models often produce inconsistent judgments, making it difficult to identify a reliable and universally optimal evaluator, particularly in the coding domain.
•
The cost of producing equivalence-class labels grows exponentially with the number of generated outputs for LLM-based semantic entropy, rendering the method impractical for multi-step, multi-agent workflows where time efficiency is critical.
•
Structural entropy alone fails to account for multiple valid structural representations of a given task, often assigning functionally equivalent code samples to different classes.
These limitations motivate the need for more accurate, efficient, and model-agnostic approaches to estimate the consistency of functionality in code generation.
3.
Methodology
The proposed FASE entropy for LLM-generated code offers a more efficient approach to computing semantic entropy and estimating code quality without relying on equivalence prediction of LLMs, following the workflow shown in Fig.
2
1
1
1
Fig.1 and Fig.2 contain icons designed using resources from Flaticon.com
. By mapping code artifacts into a continuous embedding space, their semantic relationships can be quantified directly, enabling fast and cost-effective assessment of functional similarity and divergence among generated solutions.
Figure 2
.
The workflow of computing encoder-based semantic entropy for the samples of code generated for a given task.
Pairwise Semantic Distance via Encoder-Only Embedding Models:
The current realization of the semantic equivalence function
E
​
(
⋅
,
⋅
)
E(\cdot,\cdot)
relies on LLM-based bidirectional entailment
(Farquhar
et al.
,
2024
)
. While effective, this approach incurs substantial computational cost from LLM inference. This combination of high per-query cost and
𝒪
​
(
|
x
|
2
)
\mathcal{O}(|x|^{2})
scaling results in significant overhead, rendering the method impractical for deployment in real-world or large-scale production settings. This paper leverages the low computational cost and high efficiency of embedding models to replace the existing approach, enabling finer-grained estimation of the pairwise semantic distance matrix at substantially reduced cost. For the samples of AI-generated code
x
x
from the LLM coder, their pairwise semantic distance matrix consists of
|
x
|
2
|x|^{2}
values where
d
i
,
j
∈
[
0
,
1
]
d_{i,j}\in[0,1]
represents the semantic difference between the generated code
x
i
x_{i}
and
x
j
x_{j}
,
i
,
j
∈
|
x
|
i,j\in|x|
through cosine distance. As
|
x
|
|x|
increases, the estimated distribution converges to the true underlying distribution. The resulting class labels can then be used to compute semantic entropy in the same manner as approaches that rely on LLMs to judge bidirectional functional equivalence.
Structural Abstraction using Minimum Spanning Trees:
While the full matrix encodes all pairwise distances, it is often redundant and obscures local structure due to its density. Extracting a minimum spanning tree (MST) from a densely connected pairwise distance matrix provides a compact representation of the underlying semantic structure by preserving only the most informative relationships among samples
(Gagolewski
et al.
,
2025
)
. The MST retains the subset of edges
(
x
i
,
x
j
,
w
)
(x_{i},x_{j},w)
for
x
i
,
x
j
x_{i},x_{j}
with
i
,
j
∈
|
x
|
i,j\in|x|
of weight
w
w
that connect all samples with minimal total distance, effectively highlighting the strongest semantic affinities while discarding weaker, less informative connections. As a result, the MST reveals the intrinsic topology of the data, including local neighborhoods, cluster boundaries, and the relative dispersion of samples. This abstraction enables efficient downstream analysis while preserving essential structural information.
Adaptive Density-Based Clustering for Equivalence Class Construction:
With access to a pairwise distance matrix, density-based methods can conveniently be used to compute equivalence clusters. However, fixed reachability or cluster size do not generalize well across tasks since the number and size of semantic equivalence classes are precisely the quantities we aim to estimate for entropy computation. This issue can be addressed by our adaptive density-based clustering algorithm, which leverages key structural properties derived from the pairwise distance matrix and the extracted minimum spanning tree (MST). Empirically, we observe that: (1) even when two sample sets exhibit similar average pairwise distances, those containing meaningful local clusters will yield an MST with a smaller average edge weight; and (2) edges that connect distinct clusters tend to have significantly larger weights than edges within the same cluster. Based on these observations, the adaptive neighborhood threshold
ϵ
\epsilon
is determined using the
mode
of the MST edge weights
w
w
, thereby reducing the influence of the relatively rare, high-weight inter-cluster edges. The mode is estimated as the maximizer of a Gaussian kernel density estimation computed over
w
w
. The
Mo
​
(
w
)
\mathrm{Mo}(w)
is then scaled by the ratio between the mean edge weight of the MST and the mean value of the full distance matrix as shown in Eq.
2
:
(2)
ϵ
a
​
d
​
a
​
p
​
t
​
i
​
v
​
e
=
α
⋅
Mo
​
(
w
)
⋅
(
1
−
w
¯
d
¯
)
\epsilon_{adaptive}=\alpha\cdot\mathrm{Mo}(w)\cdot(1-\frac{\bar{w}}{\bar{d}})
where
α
\alpha
is a constant used to control the clustering granularity. The choice of
α
\alpha
depends on the selected coder LLM and embedding model across the entire code generation dataset, unlike
w
¯
\bar{w}
or
d
¯
\bar{d}
, which are task-specific adaptive variables. The semantic equivalence class labels of the generated codes become FASE entropy through Eq.
1
.
To summarize, FASE introduces a novel approach for uncertainty estimation in code generation by replacing expensive LLM-based semantic equivalence checks with an efficient embedding-driven graph analysis framework. By combining semantic embeddings, minimum spanning tree extraction, and adaptive density-based clustering, FASE captures functional uncertainty without ground-truth knowledge and further bridges the gap between fast but structurally limited syntax-based approaches and semantically accurate but computationally expensive LLM-based evaluation, providing a practical and effective solution for reliable code quality estimation for large multi-agent workflows and real-world software engineering scenarios.
4.
Evaluation
The evaluation section begins by presenting the research questions, followed by a description of the experimental setup. It then investigates the properties of the PDM and MST in differentiating functional variations among generated code samples. Next, the study demonstrates the necessity of adaptive clustering for semantic entropy estimation. Subsequently, the proposed FASE entropy and its variants are compared against existing baselines. Finally, the section provides a comprehensive analysis of the overhead associated with all evaluated metrics.
The development of the proposed FASE entropy aims to answer the following research questions:
•
RQ1.
How effectively can embedding-based graph abstractions in the form of Pairwise Distance Matrix (PDM) and Minimum Spanning Tree (MST) differentiate between tasks with high and low functional consistency in code generation?
This research identifies the most influential factors derived from the pairwise distance matrix and the extracted MST that effectively differentiate the quality of generated code samples.
•
RQ2.
To what extent does task-specific adaptive clustering optimize the modeling of semantic equivalence classes compared to fixed-threshold baselines?
Given the distance matrix, density-based clustering methods can efficiently group code samples into equivalence classes; however, their performance is highly sensitive to key hyperparameters. Whether a fixed criterion can generalize across different coding tasks remains an open question that requires empirical evaluation.
•
RQ3.
How do FASE and its structural hybrid variants compare against state-of-the-art LLM-based semantic entropy and self-evaluation baselines in predicting code functional correctness within multi-agent workflows?
To demonstrate the effectiveness of the proposed method, experiments are conducted comparing it against state-of-the-art structural and semantic entropy approaches, as well as other self-evaluation methods.
•
RQ4.
What are the computational efficiency and scalability gains of FASE compared to traditional LLM-driven bidirectional entailment checks?
A quantitative comparison of runtime and resource usage is required to demonstrate the practical value of alternative observation methods.
Answering these research questions provides a comprehensive understanding of both the effectiveness and efficiency of embedding-based uncertainty estimation for code generation. Together, these analyses establish a principled trade-off between accuracy and efficiency, demonstrating the practicality of FASE for scalable code quality assessment in real-world multi-agent systems.
4.1.
Experiment Setup
Two code generation benchmarks are selected to examine the correlation between semantic entropy and code generation quality.
•
HumanEval
(Zheng
et al.
,
2023
)
is widely used as a foundational benchmark for code-generation models. It consists of 164 handwritten Python programming problems of basic algorithms.
•
BigCodeBench
(Zhuo
et al.
,
2024
)
is a more challenging and practical code-generation benchmark compared to HumanEval. In particular, we use the BigCodeBench-hard subset, which contains 148 Python problems that are closer to real-world programming scenarios.
Four open-source 7-billion-parameter LLMs are selected as coders and analysts in the experiments: Mistral-7B
(Jiang
et al.
,
2023
)
, CodeLlama-7B
(Roziere
et al.
,
2023
)
, DeepSeek-Coder-7B
(Guo
et al.
,
2024
)
, and Qwen2.5-Coder-7B
(Hui
et al.
,
2024
)
. By evaluating this diverse set of models, this research explores the generality of semantic entropy signals across different model designs, training objectives, and data distributions. The number of parameters is identical to avoid the impact of model scale.
Table 1
.
Embedding Models Used in the Study
Name
# Parameters
Dimensionality
Context Window
All-MiniLM-L6-v2
0.02B
384
0.2K
GTE-ModernBERT-base
0.1B
768
8K
Llama-Embed-Nemotron
8B
4096
32K
Qwen3-Embedding
0.6B
1024
32K
Qwen3-Embedding
4B
2560
32K
Qwen3-Embedding
8B
4096
32K
For generating semantic embeddings of code and task descriptions, four encoder-only embedding models of different sizes are selected with high performance in text embedding, searching, ranking and clustering tasks as shown in Tab.
1
: All-MiniLM-L6-v2
(Wang
et al.
,
2020
)
, GTE-ModernBERT-base
(Zhang
et al.
,
2024
)
, Llama-Embed-Nemotron
(Babakhin
et al.
,
2025
)
and Qwen3-Embedding
(Zhang
et al.
,
2025a
)
. Their embedding dimensionalities are 384, 768 and 4096 for All-MiniLM, ModernBERT, and Nemotron, respectively. We also explored the impact of parameter size on the same model for Qwen3-Embedding of 0.6B, 4B and 8B parameters with dimensional vector size of 1024, 2560 and 4096. Each encoder differs in underlying training design and domain emphasis, allowing us to test whether semantic representation quality impacts semantic distance, clustering results, and ultimately the estimation of functional correctness. By incorporating this variety of embedding models, we aim to strengthen the soundness and generality of our experimental findings.
The experiment is conducted on ASUSTeK ESC4000A-E12 with AMD EPYC™ 9554 processor on a Ubuntu 24.04.2 LTS environment. The GPU we used is NVIDIA H100 NVL with driver version 550.163.01 and CUDA version 12.4. We deployed
CodeLlama-7b-Instruct-hf
for the agent model. When generating output with nucleus sampling, we set the
temperature
to 0.5 and
top_p
to 0.95 for more consistent results. For each task, 10 samples will be generated to compute related metrics. The implementation and experimental artifacts are publicly available at
this link
2
2
2
https://github.com/corvolin/CSE4AgenticSoftDev
4.2.
Effectiveness of Embedding Representations in Capturing Functional Correctness
The overall performance of the selected models on code generation benchmarks is summarized in Fig.
3
, which presents results on the HumanEval and BigCodeBench-hard tasks.
Figure 3
.
Pass@1 distribution of code generated by Mistral, CodeLlama, DeepseekCoder, Qwen2.5-Coder on HumanEval and BigCodeBench-hard
The green region denotes the number of tasks with pass@1
(Chen
et al.
,
2021
)
equal to 1, indicating that the model consistently generates functionally correct solutions on the first attempt. The red region represents tasks with pass@1 equal to 0, where no correct solutions are produced. The orange region captures intermediate cases with 0¡pass@1¡1, reflecting partial success across multiple attempts.
On the HumanEval benchmark, most LLMs are able to generate partially correct solutions, with the number of tasks achieving pass@1 = 1 ranging from 31 for Mistral to 101 for both DeepSeek-Coder and Qwen2.5-Coder. In contrast, performance on the BigCodeBench-Hard benchmark is substantially lower: the majority of models fail to produce any functionally correct solutions. The best performance is achieved by Qwen2.5-Coder, with only 2 tasks reaching pass@1 = 1 and 15 tasks exhibiting partial success with 0¡pass@1¡1. We also evaluated the effect of introducing an analyst agent that provides semi-structured information on data and control flow based on the task’s functional requirements. The impact on pass@1 is mixed. Across both HumanEval and BigCodeBench-Hard, the number of tasks with pass@1 = 0 and pass@1 = 1 decreases, while the number of tasks with intermediate outcomes of 0¡pass@1¡1 increases. For instance, Qwen2.5-Coder reduces 9 cases of pass@1 = 0 at the cost of 4 cases of pass@1 = 1. In contrast, other models tend to exhibit a larger reduction in pass@1 = 1 than in pass@1 = 0. These results suggest that naively introducing an analyst agent without task-specific adaptation does not necessarily improve overall performance, aligning with growing concerns in the research community regarding hallucination propagation in multi-agent systems.
(a)
All-MiniLM PDM
(b)
All-MiniLM MST
(c)
Qwen3-Emb.-0.6B PDM
(d)
Qwen3-Emb.-0.6B MST
(e)
ModernBERT PDM
(f)
ModernBERT MST
(g)
Qwen3-Emb.-4B PDM
(h)
Qwen3-Emb.-4B MST
(i)
Nemoron PDM
(j)
Nemotron MST
(k)
Qwen3-Emb.-8B PDM
(l)
Qwen3-Emb.-8B MST
Figure 4
.
The ratio of mean distance in Pairwise Distance Matrix (PDM) and mean edge weight in MST categorized by their connected nodes, Pass-Pass(Blue), Fail-Fail(Purple) and Pass-Fail(Brown), compared to all distances and weights in its samples.
The PDM generated from the embedding models indeed capture meaningful semantic differences among code samples for each task. This research firstly focus on tasks with intermediate pass@1 values and categorize pairwise distances into three groups: (i) between functionally correct codes that passed provided test cases, (ii) between codes that failed the test cases, and (iii) between a correct and a failed code. For each category, the ratio between its mean distance and the overall mean distance of the PDM is computed, and the distribution of these ratios are shown in Fig.
4
. Across all embedding models, distances between pairs of functionally correct codes are consistently the smallest. Distances between failed code pairs are slightly larger, likely reflecting diverse failed root cause despite shared task objectives. Notably, both categories yield ratios below 1, whereas distances between correct and failed code pairs consistently exceed 1. This indicates that substantial functional differences correspond to significantly larger semantic distances relative to the task-specific average.
After extracting the MST from the PDM, the previously observed pattern remains consistent. Edges connecting functionally correct codes exhibit the smallest ratio, followed by edges between failed codes. In contrast, edges linking correct and failed codes show substantially larger ratio, increasing from approximately 1.7–1.8 in the PDM to 3.4–3.6 in the MST. This amplification indicates that the MST preferentially selects low-weight edges that capture local structure, effectively forming tight clusters among semantically similar codes. Once these intra-cluster connections are established, the higher-weight edges representing connections between functionally distinct groups are incorporated to link the clusters. Consequently, the extracted MST further differentiates the separation of semantic clusters compared to the original PDM.
(a)
All-MiniLM
(b)
ModernBERT
(c)
Nemotron
(d)
Qwen3-Emb.-0.6B
(e)
Qwen3-Emb.-4B
(f)
Qwen3-Emb.-8B
Figure 5
.
The ratio between mean distance in Pairwise Distance Matrix (PDM) and mean edge weight in MST categorized for tasks with Pass@1 of 0, between 0 and 1, and 1.
However, as shown in Fig.
3
, the majority of code generation tasks across all four LLMs exhibit either pass@1 = 0 or pass@1 = 1. In such cases, there are few or no edges connecting functionally correct and failed codes with substantially higher weights relative to the task average. Moreover, the difference of intra-cluster edges between pairs of correct codes and pairs of failed codes is relatively small. Although not shown, the distributions of pairwise distances and MST edge weights do not differ significantly between tasks with pass@1 = 0 and those with pass@1 = 1.
While examining the PDM and MST in isolation does not reveal strong differences between tasks with pass@1 = 1 and pass@1 = 0, comparing edge weights before and after MST extraction provides additional insight. Fig.
5
illustrates the ratio between the mean edge weight of the MST and the mean pairwise distance of the PDM for each task. Across all embedding models, a consistent pattern emerges: tasks with pass@1 = 1 exhibit the lowest ratios, followed by tasks with intermediate pass@1 values, while tasks with pass@1 = 0 have the highest ratios. This indicates that, although overall distance distributions appear similar across tasks, those with pass@1 = 1 contain stronger local structure, reflected by relatively smaller MST edge weights. In contrast, tasks with pass@1 = 0 lack such structure, with their minimum edges remaining comparable to the overall pairwise distances.
Answer to RQ.1:
The cosine-distance distributions derived from the PDM and its corresponding MST capture meaningful patterns of functional consistency among generated code samples. In particular, high-weight edges in the extracted MST often correspond to genuine functional differences between correct and incorrect solutions. Although the overall distance distributions for tasks with Pass@1 = 1 and Pass@1 = 0 appear similar, tasks with Pass@1 = 1 consistently exhibit a substantially lower mean MST-to-PDM weight ratio.
4.3.
Impact of Adaptive Clustering on Semantic Equivalence Modeling
Given the pairwise distance matrix derived from semantic embeddings of the generated code, an intuitive approach for identifying semantic clusters is to apply density-based clustering techniques
(Ester
et al.
,
1996
; Campello
et al.
,
2013
)
. The foundation of adaptive clustering is DBSCAN with a fixed neighborhood radius
ϵ
\epsilon
and HDBSCAN with a fixed minimum cluster size (MCS). The parameter
ϵ
\epsilon
is varied from 0.01 to 0.2, covering the largest range of pairwise semantic distances across different embedding models. The MCS varies from 2 to 9, with a single cluster of size 10 permitted. The adaptive
ϵ
\epsilon
based on the MST/PDM ratio are derived as Eq.
2
. The constant
α
\alpha
ranges from 0.1 to 3 to control clustering granularity.
(a)
All-MiniLM
(b)
ModernBERT
(c)
Nemotron
(d)
Qwen3-Emb.-0.6B
(e)
Qwen3-Emb.-4B
(f)
Qwen3-Emb.-8B
Figure 6
.
The Spearman’s
ρ
\rho
correlation measured between the semantic entropy of each method and the pass@1 results when only the coder is involved.
Fig.
6
presents the Spearman’s
ρ
\rho
correlation between semantic entropy and pass@1 in the coder-only setting and all clustering methods show only weak correlation between 0.1 and -0.2. The light and dark grey dashed curves correspond to DBSCAN with a fixed
ϵ
\epsilon
and HDBSCAN with a fixed MCS, respectively. Both fixed clustering approaches exhibit weak correlation with the actual functional correctness of the generated code. The blue curves represent adaptive clustering based on the mean pairwise distance of the PDM, where the dashed and dotted variants correspond to approaches without additional scaling, and the solid variant incorporates the proposed scaling mechanism. Similarly, the green curves represent adaptive clustering based on the mean edge weight of the MST. Overall, semantic entropy derived from MST-based statistics demonstrates stronger correlation with functional correctness than approaches based solely on the PDM mean, and the inclusion of scaling further improves the correlation. The solid red curves correspond to semantic entropy computed using the MST mode as the adaptive reference value. This approach consistently achieves the strongest correlation across most clustering granularities, except in extremely fine-grained clustering settings where MST-mean-based approaches occasionally perform better.
(a)
All-MiniLM
(b)
ModernBERT
(c)
Nemotron
(d)
Qwen3-Emb.-0.6B
(e)
Qwen3-Emb.-4B
(f)
Qwen3-Emb.-8B
Figure 7
.
The Spearman’s
ρ
\rho
correlation measured between the semantic entropy of each method and the pass@1 results when the analyst agent provides additional instruction to the coder
The adaptive clustering approaches exhibit stronger correlation when an analyst agent is introduced before the coder agent. As shown in Fig.
7
, nearly all adaptive clustering methods produce semantic entropy values with improved correlation to pass@1, whereas the fixed clustering approaches remain close to zero correlation. The relative ranking of the adaptive methods remains largely consistent, although the scaled PDM-mean approach now outperforms the MST-mean-based approach. Among all methods, the scaled MST-mode strategy achieves the strongest overall performance across nearly all settings, with the exception of Qwen3-Embedding-0.6B under extremely fine-grained clustering configurations, where alternative approaches perform better.
Answer to RQ.2:
Task-specific adaptiveness is essential when clustering code samples represented as semantic embeddings. The strongest correlation between semantic entropy and functional correctness is consistently achieved by density-based clustering methods that use the scaled mode of MST edge weights as the neighborhood radius
ϵ
\epsilon
.
4.4.
Comparison with LLM-based Semantic Entropy, Self-Evaluation Methods and Other Baselines
To demonstrate the effectiveness of the proposed FASE measurement, this experiment compares it against the state-of-the-art semantic entropy approach based on bidirectional entailment using LLM judgments, as well as alternative entropy formulations derived from textual and structural equivalence. In addition, the evaluation includes widely used LLM self-evaluation baselines such as P(True) and majority voting, where functional correctness is determined according to predictions generated either by the coding LLM itself or by a committee of auxiliary LLMs. The evaluation considers two complementary perspectives: (1) Spearman’s
ρ
\rho
coefficient, which measures the correlation between each uncertainty metric and the ground-truth pass@1 values, and (2) the Area Under the Curve (AUC) score, which evaluates the binary predictive capability of each metric in determining whether a task achieves pass@1 = 1.
Table 2
.
The Spearmnar’s
ρ
\rho
correlation coefficient and AUC score for the baselines and FASE-related entropy using Qwen3-Embedding-8B in different workflow and coding LLMs. The entropy measurements are inverted by
1
−
entropy
1-\text{entropy}
to keep correlation positive, as lower entropy indicates greater consistency and better functional correctness. Best scores for each setting are highlighted.
Metric
Coder Only
Analyst + Coder
Mistral
CodeLlama
DeepSeek
Qwen2.5
Mistral
CodeLlama
DeepSeek
Qwen2.5
ρ
\rho
AUC
ρ
\rho
AUC
ρ
\rho
AUC
ρ
\rho
AUC
ρ
\rho
AUC
ρ
\rho
AUC
ρ
\rho
AUC
ρ
\rho
AUC
Self P(True)
0.07
0.51
0.22
0.65
0.05
0.52
0.32
0.65
0.02
0.52
0.17
0.84
0.15
0.56
0.22
0.59
Majority Voting
0.13
0.52
0.19
0.61
0.06
0.53
0.28
0.63
0.04
0.51
0.18
0.83
0.07
0.54
0.18
0.59
Textual Entropy
0.06
0.64
0.18
0.74
0.24
0.66
0.36
0.73
0.26
0.6
0.24
0.78
0.4
0.76
0.41
0.67
Structural Entropy
0.2
0.8
0.18
0.76
0.31
0.73
0.37
0.74
0.45
0.95
0.34
0.96
0.56
0.91
0.61
0.86
Semantic Entropy
0.13
0.62
0.35
0.77
0.25
0.69
0.41
0.76
0.15
0.74
0.38
0.85
0.45
0.88
0.7
0.9
Fixed MCS
0.04
0.63
0.12
0.69
0.19
0.63
0.02
0.52
0.07
0.57
0.02
0.51
0.22
0.61
0.13
0.53
Fixed
ϵ
\epsilon
0
0.63
0
0.54
0.04
0.52
0.11
0.53
0.02
0.8
0.04
0.74
0.27
0.78
0.13
0.62
FASE-PDM Mean
0.1
0.57
0.14
0.58
0.19
0.62
0.38
0.73
0.37
0.91
0.24
0.83
0.51
0.86
0.46
0.76
FASE-MST Mean
0.31
0.73
0.22
0.68
0.39
0.73
0.48
0.75
0.37
0.91
0.26
0.83
0.51
0.86
0.46
0.76
FASE-Scaled PDM Mean
0.31
0.73
0.24
0.74
0.39
0.73
0.48
0.75
0.37
0.93
0.28
0.84
0.51
0.86
0.46
0.76
FASE-Scaled MST Mean
0.33
0.75
0.25
0.75
0.4
0.74
0.5
0.76
0.39
0.93
0.28
0.84
0.51
0.86
0.47
0.76
FASE-Scaled MST Mode
0.34
0.75
0.25
0.75
0.4
0.74
0.5
0.76
0.39
0.93
0.3
0.89
0.51
0.86
0.47
0.76
FASE
∪
\cup
Structural
0.34
0.77
0.28
0.75
0.4
0.74
0.5
0.76
0.47
0.96
0.34
0.98
0.59
0.91
0.61
0.87
The results, presented in Tab.
2
, demonstrate that FASE entropy consistently outperforms LLM-entailment-based semantic entropy in both correlation and predictive performance across code generation workflows involving either a standalone coder LLM or an analyst–coder pipeline. In particular, combining the semantic equivalence labels generated by FASE using scaled MST-mode clustering with structural equivalence classes through a
union
operation produces the entropy measure with the strongest overall correlation and predictive capability, outperforming all baseline methods across the evaluated settings.
In the coder-only setting, when Mistral is used, all FASE-related variants achieve moderate correlation with functional correctness, although structural entropy attains the highest AUC score of 0.80. For CodeLlama, traditional semantic entropy outperforms the other metrics in both Spearman’s
ρ
\rho
and AUC, while FASE remains highly competitive. In the case of DeepSeek-Coder, FASE with scaled MST Mean/Mode achieves the strongest performance with a
ρ
\rho
of 0.40 and an AUC of 0.74. Similarly, for Qwen2.5-Coder, FASE with scaled MST Mean/Mode again yields the best overall results, reaching a
ρ
\rho
of 0.50 and an AUC of 0.76.
When an analyst agent is incorporated into the workflow, FASE
∪
\cup
structural entropy provides the most accurate estimation of functional correctness for Mistral-generated outputs, achieving a
ρ
\rho
of 0.47 and an AUC of 0.96. For CodeLlama, the highest correlation is obtained using traditional semantic entropy with a
ρ
\rho
of 0.38, whereas FASE achieves the best predictive performance with an AUC of 0.98. FASE again produces the strongest results for DeepSeek-Coder, with a
ρ
\rho
of 0.59 and an AUC of 0.91. For Qwen2.5-Coder, traditional semantic entropy achieves the best overall performance, reaching a
ρ
\rho
of 0.70 and an AUC of 0.90.
Answer to RQ.3:
FASE and its structural hybrid variants outperforms existing state-of-the-art LLM-based semantic entropy methods by approximately 25% in correlation and 8% in AUC on average, achieving the strongest overall performance across most experimental settings involving all four selected LLMs and both the coder-only and analyst+coder workflows.
4.5.
Computational Cost and Scalability Analysis
One of the primary reasons that traditional semantic entropy is impractical in large-scale code generation evaluation is its computational cost from bidirectional entailment queries which scales in
𝒪
​
(
|
x
|
2
)
\mathcal{O}(|x|^{2})
as code sampling increases. Tab.
3(b)
records and compares the time required for all LLM-related tasks discussed in earlier evaluation steps, and Tab.
3(b)
covers time costs associated with embedding models.
Table 3
.
The time cost for LLM and embedding model tasks measured in seconds.
(a)
The time cost of LLM-related tasks.
Observation Method
Mistral
Codellama
Deepseek-Coder
Qwen2.5-Coder
Self-Evaluation
3.34
25.4
3.74
2.72
Majority Voting
31.86
9.8
31.46
32.48
Semantic Equivalence
44.23
110.98
39.24
17.63
(b)
The time cost of embedding-related tasks.
Embedding Model
PDM Generation
MST Extraction
All-MiniLM
0.021
0.0000342
ModernBERT
0.073
0.0000265
Nemotron
0.327
0.0000265
Qwen3-Emb.-0.6B
0.112
0.0000265
Qwen3-Emb.-4B
0.264
0.0000264
Qwen3-Emb.-8B
0.357
0.0000264
The self-evaluation metric P(True) is relatively efficient to compute compared to more expensive semantic equivalence checks. For a batch of 10 self-evaluation predictions, Mistral, DeepSeek-Coder, and Qwen2.5-Coder require approximately 2–3 seconds, whereas CodeLlama requires substantially longer at 25.4 seconds. Majority voting, which relies on a committee of auxiliary LLMs excluding the coding model itself, incurs significantly higher computational cost, requiring approximately 30 seconds. In comparison, conducting bidirectional semantic equivalence checks across 10 code samples is considerably more expensive, taking 44.23 s, 110.98 s, 39.24 s, and 17.63 s for the respective models.
Tasks involving embedding models instead of LLMs are an order of magnitude faster than LLM-based operations. Computing the PDM for 10 code samples or functionality reviews requires only approximately 0.02–0.3 seconds. Among the evaluated embedding models, All-MiniLM-L6-v2 is generally the fastest, followed by GTE-ModernBERT, while the Nemotron and Qwen3-Embedding series are the slowest, consistent with their larger model sizes. The extraction of the MST from the PDM incurs negligible computational overhead and is effectively independent of the choice of embedding model.
Answer to RQ.4:
The embedding models provide substantial efficiency gains, reducing the overhead to approximately 0.3% of the traditional pairwise LLM-based equivalence checks on average.
Overall, the experimental results provide strong evidence supporting the effectiveness and efficiency of the proposed framework. The results show that embedding-based representations meaningfully capture functional differences between code samples, and adaptiveness is crucial for reliable clustering, with density-based methods using scaled MST-PDM ratio. FASE consistently outperforms existing LLM-based semantic entropy methods and offers substantial efficiency benefits, reducing computational overhead to roughly 0.3% of that required by traditional LLM-based equivalence checking. Collectively, these findings validate both the predictive strength and practical efficiency of FASE for scalable code quality estimation.
5.
Related Work
Several lines of research have explored the use of multiple LLM agents to enhance automated code generation. At the same time, considerable attention has been devoted to understanding their inherent limitations, particularly those arising from code quality issues, hallucination propagation, and strategies for mitigating cascading errors across collaborative agent workflows.
Multi-agent Frameworks for Code Generation.
Recent advances in large language models (LLMs) have enabled autonomous AI agents for software development, motivating extensive research on agent architectures, collaboration, and evaluation
(Mohammadi
et al.
,
2025
; Ferrag
et al.
,
2025
; Liu
et al.
,
2024b
; He
et al.
,
2025
)
. Prior studies highlight both the potential of these systems to automate complex software engineering tasks and the challenges they introduce, including error propagation, limited self-assessment, and coordination overhead
(Yehudai
et al.
,
2025
)
. To improve robustness, multi-agent frameworks have been proposed to encourage specialization and collaboration among agents with distinct responsibilities
(Talebirad and Nadiri,
2023
)
. Several collaborative agent frameworks have shown promising results for code generation and repair. CodeCoR
(Pan
et al.
,
2025
)
employs specialized agents for prompt generation, coding, testing, and repair, while MetaGPT
(Hong
et al.
,
2024
)
integrates human-inspired software engineering workflows into structured multi-agent prompting pipelines. Dong et al.
(Dong
et al.
,
2024
)
propose a self-collaboration framework with analyst, coder, and tester agents that substantially improves Pass@1 over single-agent generation. AdaCoder
(Zhu
et al.
,
2025b
)
further introduces adaptive planning and iterative debugging, achieving better generalizability, faster inference, and lower token consumption across diverse LLMs. Beyond code generation, multi-agent collaboration has also been applied to software requirement compliance verification through retrieval-augmented generation and human-in-the-loop feedback
(Das
et al.
,
2025
)
. Collectively, these studies demonstrate the importance of adaptive coordination and reliability estimation in autonomous software engineering systems.
Agent Hallucination and Uncertainty.
Hallucination in large language models has received significant attention, leading to extensive surveys and empirical studies on hallucination detection and mitigation
(Zhang
et al.
,
2025b
; Huang
et al.
,
2025
; Zhang
et al.
,
2025c
)
. Prior work categorizes hallucinations across both natural language and code generation tasks, highlighting the challenge of identifying hallucinations without ground-truth answers. FEWL
(Wei
et al.
,
2024
)
introduces a principled hallucination metric that weights evaluator LLMs according to estimated expertise. In code generation, HalluCode
(Liu
et al.
,
2024a
)
shows that current LLMs struggle to recognize and classify hallucinations effectively. CodeMirage
(Agarwal
et al.
,
2024
)
further establishes one of the first comprehensive taxonomies of code hallucinations and introduces a dedicated benchmark for hallucination detection. Extending this direction, Liu et al.
(Liu
et al.
,
2026
)
propose a broader taxonomy covering multiple categories of hallucinations, their causes, and impacts across different models and benchmarks. Recent studies also explore improved detection methodologies. Yang et al.
(Yang
et al.
,
2025
)
propose a hybrid static–dynamic hallucination detection framework that substantially improves detection performance on multiple benchmarks. Foodeei et al.
(Foodeei
et al.
,
2025
)
investigate semantic uncertainty under different decoding strategies and show that structured reasoning can improve both semantic diversity and functional correctness. Collectively, these studies motivate the need for efficient semantic-level uncertainty estimation methods for reliable code generation systems.
LLM Code Quality Assurance.
Several lines of research have explored software quality assurance for LLM-based systems. Self-confidence estimation methods such as P(True) and P(IK)
(Kadavath
et al.
,
2022
)
attempt to predict output reliability without ground-truth labels, while self-reflection frameworks improve consistency through iterative feedback and refinement
(Ji
et al.
,
2023
)
. To reduce hallucinations in code generation, De-Hallucinator
(Eghbali and Pradel,
2024
)
iteratively retrieves project-specific API references to ground model predictions, significantly improving API usage and test generation quality. Repository-aware approaches such as
A
3
A^{3}
-CodGen
(Liao
et al.
,
2024
)
further incorporate local, global, and third-party library context to reduce logical inconsistencies and improve code reuse. At the systems level, multi-agent software engineering frameworks increasingly adopt software engineering practices such as milestone-based collaboration assessment
(Zhu
et al.
,
2025a
)
, contribution-aware agent selection
(Liu
et al.
,
2024e
)
, and adaptive coordination strategies. Interactive workflows such as TICODER
(Fakhoury
et al.
,
2024
)
improve code generation accuracy through iterative intent clarification and test-driven feedback. Recent work also explores LLM-assisted software testing and oracle generation. CANDOR
(Xu
et al.
,
2026
)
proposes a multi-agent framework for automated unit test generation that combines specialized agents and consensus-based reasoning to mitigate hallucinations in generated test oracles, significantly improving oracle correctness and mutation scores over existing approaches. Empirical studies also examine the reliability and maintainability of LLM-generated code. Liu et al.
(Liu
et al.
,
2024d
)
evaluate ChatGPT-generated programs across correctness, complexity, and security dimensions, highlighting issues related to non-determinism and vulnerability generation. Subsequent work
(Liu
et al.
,
2024c
)
shows that iterative self-repair and static-analysis-guided refinement can partially improve maintainability and correctness. In parallel, automated mutation testing
(Tip
et al.
,
2025
; Wang
et al.
,
2026
)
and fuzz testing
(Cao
et al.
,
2025
; Chen
et al.
,
2025
)
demonstrate strong potential for validating LLM-generated code. Recent semantic representation learning approaches such as Tailor
(Liu
et al.
,
2023
)
further emphasize the importance of semantic-level reasoning for reliable functional similarity detection and code quality assurance.
Entropy of LLM output.
Several prior works have investigated uncertainty estimation in LLMs by accounting for code equivalence, recognizing that multiple surface forms may convey the same underlying meaning. To address this challenge, semantic entropy was proposed as an unsupervised uncertainty measure that aggregates model outputs at the level of meaning rather than token sequences
(Kuhn
et al.
,
2023
)
. These methods demonstrate robustness across tasks and datasets, generalize to unseen scenarios, and do not rely on prior task knowledge or labeled data
(Farquhar
et al.
,
2024
)
. In the context of code generation, structural entropy
(Song
et al.
,
2025
)
is specifically designed for source code represented as abstract syntax trees, providing an alternative approach for efficient code quality estimation.
FASE provides a scalable uncertainty estimation mechanism that directly addresses a key limitation in current multi-agent code generation systems—namely, the lack of efficient and reliable measures for agent-level hallucination and error propagation. By bridging embedding-based semantic reasoning with entropy-driven evaluation, it complements existing LLM code quality assurance and entropy-based methods, offering a practical alternative for modeling uncertainty in complex multi-agent workflows.
6.
Threats to Validity
Despite its strong empirical performance, FASE inherits common limitations of embedding-based and clustering-driven approaches, as well as constraints of experiments:
Embedding Representation:
A key limitation of textual and structural similarity measures is that the true semantics of a program may change drastically due to a single operator or variable modification. Although modern embedding models often employ attention mechanisms, embeddings of code snippets with opposite functionality may still exhibit high similarity, thereby undermining the validity of pairwise semantic comparisons. The combination of FASE and structural entropy through a union operation achieves the best overall performance in Tab.
2
because abstract syntax trees are highly sensitive to fine-grained token-level mutations that embedding-based semantic representations may overlook.
Prompt Engineering:
The quality of prompts significantly influences LLM-generated outputs
(Khojah
et al.
,
2025
)
. The experiments conducted in this study employ relatively simple prompting strategies. For code generation tasks, the models are provided with only basic coding instructions with a persona system prompt. For functional correctness and equivalence evaluation, a 2-shot prompting strategy is adopted, consisting of one positive example (functional/equivalent) and one negative example (failed/not equivalent). The extent to which FASE generalizes under more sophisticated prompting strategies remains an open question.
Code Generation Scale:
Due to computational resource constraints, this study evaluates only open-source models with 7B parameters. The inclusion of additional models with broader architectural diversity and varying parameter scales may influence the observed performance and generalizability of FASE.
7.
Conclusion & Future Directions
This research explores the application of FASE entropy in code generation and demonstrates its effectiveness in estimating the functional correctness of generated code in the absence of ground-truth test cases. Given the impractical computational cost of LLM-based bidirectional equivalence checks, this research offers a scalable alternative that combines code semantic and structural consistency. Extensive evaluations across four widely used code LLMs and four embedding models show that this approach achieves high correlation and predictive performance while significantly reducing computation time. By enabling efficient, ground-truth–free monitoring of code quality, the proposed FASE entropy supports multi-agent code generation workflows with reduced risk of error propagation and hallucination.
Several directions remain for future work. First, the evaluation can be expanded to include a broader range of foundation LLMs, embedding models, and code generation benchmarks to further validate the robustness and generalizability of FASE. Second, FASE does not explicitly distinguish cases where all generated solutions consistently drift away from the intended functionality with low entropy. Incorporating an additional dimension of semantic alignment with task requirements may improve the detection of functionally incorrect yet semantically consistent outputs. Finally, FASE can be integrated directly into adaptive multi-agent decision-making frameworks, where uncertainty estimates dynamically guide agent selection, workflow orchestration, refinement strategies, or verification depth.
References
V. Agarwal, Y. Pei, S. Alamir, and X. Liu (2024)
Codemirage: hallucinations in code generated by large language models
.
arXiv preprint arXiv:2408.08333
.
Cited by:
§1
,
§5
.
Y. Babakhin, R. Osmulski, R. Ak, G. Moreira, M. Xu, B. Schifferer, B. Liu, and E. Oldridge (2025)
Llama-embed-nemotron-8b: a universal text embedding model for multilingual and cross-lingual tasks
.
External Links:
2511.07025
,
Link
Cited by:
§4.1
.
R. J. Campello, D. Moulavi, and J. Sander (2013)
Density-based clustering based on hierarchical density estimates
.
In
Pacific-Asia conference on knowledge discovery and data mining
,
pp. 160–172
.
Cited by:
§4.3
.
D. Cao, Y. Hong, Q. Pan, and J. Wu (2025)
Program interoperable large language model software testing scheme: a case study on javascript engine fuzzing
.
IEEE Transactions on Dependable and Secure Computing
.
Cited by:
§1
,
§5
.
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
et al.
(2021)
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
Cited by:
§4.2
.
X. Chen, J. Liu, Y. Zhang, Q. Hu, Y. Han, R. Zhang, J. Ran, L. Yan, B. Huang, and S. Ma (2025)
TraceAwareness and dual-strategy fuzz testing: enhancing path coverage and crash localization with stochastic science and large language models
.
Computers and Electrical Engineering
123
,
pp. 110266
.
Cited by:
§1
,
§5
.
S. Das, N. Deb, N. Chaki, and A. Cortesi (2025)
A multi-agent rag framework for regulatory compliance checking of software requirements
.
ACM Transactions on Software Engineering and Methodology
.
Cited by:
§1
,
§5
.
Y. Dong, X. Jiang, Z. Jin, and G. Li (2024)
Self-collaboration code generation via chatgpt
.
ACM Transactions on Software Engineering and Methodology
33
(
7
),
pp. 1–38
.
Cited by:
§1
,
§5
.
A. Eghbali and M. Pradel (2024)
De-hallucinator: mitigating llm hallucinations in code generation tasks via iterative grounding
.
arXiv preprint arXiv:2401.01701
.
Cited by:
§1
,
§5
.
M. Ester, H. Kriegel, J. Sander, X. Xu,
et al.
(1996)
A density-based algorithm for discovering clusters in large spatial databases with noise
.
In
Proceedings of the Second International Conference on Knowledge Discovery and Data Mining
,
Vol.
96
,
pp. 226–231
.
Cited by:
§4.3
.
S. Fakhoury, A. Naik, G. Sakkas, S. Chakraborty, and S. K. Lahiri (2024)
Llm-based test-driven interactive code generation: user study and empirical evaluation
.
IEEE Transactions on Software Engineering
50
(
9
),
pp. 2254–2268
.
Cited by:
§1
,
§5
.
S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal (2024)
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
§1
,
§2
,
§3
,
§5
.
M. A. Ferrag, N. Tihanyi, and M. Debbah (2025)
From llm reasoning to autonomous ai agents: a comprehensive review
.
arXiv preprint arXiv:2504.19678
.
Cited by:
§1
,
§5
.
D. Foodeei, S. Fan, and M. Jaggi (2025)
Semantic uncertainty in advanced decoding methods for llm generation
.
arXiv preprint arXiv:2506.17296
.
Cited by:
§5
.
M. Gagolewski, A. Cena, M. Bartoszuk, and Ł. Brzozowski (2025)
Clustering with minimum spanning trees: how good can it be?
.
Journal of Classification
42
(
1
),
pp. 90–112
.
Cited by:
§3
.
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. Li,
et al.
(2024)
DeepSeek-coder: when the large language model meets programming–the rise of code intelligence
.
arXiv preprint arXiv:2401.14196
.
Cited by:
§4.1
.
J. He, C. Treude, and D. Lo (2025)
Llm-based multi-agent systems for software engineering: literature review, vision, and the road ahead
.
ACM Transactions on Software Engineering and Methodology
34
(
5
),
pp. 1–30
.
Cited by:
§1
,
§5
.
S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, J. Wang, C. Zhang, S. Yau, Z. Lin, L. Zhou,
et al.
(2024)
MetaGPT: meta programming for a multi-agent collaborative framework
.
In
Proceedings of the International Conference on Learning Representations
,
Vol.
2024
,
pp. 23247–23275
.
Cited by:
§1
,
§5
.
L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin,
et al.
(2025)
A survey on hallucination in large language models: principles, taxonomy, challenges, and open questions
.
ACM Transactions on Information Systems
43
(
2
),
pp. 1–55
.
Cited by:
§5
.
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu,
et al.
(2024)
Qwen2. 5-coder technical report
.
arXiv preprint arXiv:2409.12186
.
Cited by:
§4.1
.
Z. Ji, T. Yu, Y. Xu, N. Lee, E. Ishii, and P. Fung (2023)
Towards mitigating llm hallucination via self reflection
.
In
Findings of the Association for Computational Linguistics
,
pp. 1827–1843
.
Cited by:
§1
,
§5
.
A. Q. Jiang, A. Sablayrolles, N. Nadeau, N. Usunier, and G. Lample (2023)
Mistral 7b
.
arXiv preprint arXiv:2310.06825
.
Cited by:
§4.1
.
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson,
et al.
(2022)
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Cited by:
§1
,
§5
.
R. Khojah, F. G. de Oliveira Neto, M. Mohamad, and P. Leitner (2025)
The impact of prompt programming on function-level code generation
.
IEEE Transactions on Software Engineering
.
Cited by:
§6
.
L. Kuhn, Y. Gal, and S. Farquhar (2023)
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
arXiv preprint arXiv:2302.09664
.
Cited by:
§1
,
§5
.
D. Liao, S. Pan, X. Sun, X. Ren, Q. Huang, Z. Xing, H. Jin, and Q. Li (2024)
A3-codgen: a repository-level code generation framework for code reuse with local-aware, global-aware, and third-party-library-aware
.
IEEE Transactions on Software Engineering
50
(
12
),
pp. 3369–3384
.
Cited by:
§1
,
§5
.
D. V. Lindley (1956)
On a measure of the information provided by an experiment
.
The Annals of Mathematical Statistics
27
(
4
),
pp. 986–1005
.
Cited by:
§2
.
F. Liu, Y. Liu, L. Shi, H. Huang, R. Wang, Z. Yang, L. Zhang, Z. Li, and Y. Ma (2024a)
Exploring and evaluating hallucinations in llm-powered code generation
.
arXiv preprint arXiv:2404.00971
.
Cited by:
§1
,
§5
.
F. Liu, Y. Liu, L. Shi, Z. Yang, L. Zhang, X. Lian, Z. Li, and Y. Ma (2026)
Beyond functional correctness: exploring hallucinations in llm-generated code
.
IEEE Transactions on Software Engineering
.
Cited by:
§1
,
§5
.
J. Liu, J. Zeng, X. Wang, and Z. Liang (2023)
Learning graph-based code representations for source-level functional similarity detection
.
In
Proceedings of the 45th International Conference on Software Engineering
,
pp. 345–357
.
Cited by:
§5
.
J. Liu, K. Wang, Y. Chen, X. Peng, Z. Chen, L. Zhang, and Y. Lou (2024b)
Large language model-based agents for software engineering: a survey
.
ACM Transactions on Software Engineering and Methodology
.
Cited by:
§1
,
§5
.
Y. Liu, T. Le-Cong, R. Widyasari, C. Tantithamthavorn, L. Li, X. D. Le, and D. Lo (2024c)
Refining chatgpt-generated code: characterizing and mitigating code quality issues
.
ACM Transactions on Software Engineering and Methodology
33
(
5
),
pp. 1–26
.
Cited by:
§1
,
§5
.
Z. Liu, Y. Tang, X. Luo, Y. Zhou, and L. F. Zhang (2024d)
No need to lift a finger anymore? assessing the quality of code generation by chatgpt
.
IEEE Transactions on Software Engineering
50
(
6
),
pp. 1548–1584
.
Cited by:
§5
.
Z. Liu, Y. Zhang, P. Li, Y. Liu, and D. Yang (2024e)
A dynamic llm-powered agent network for task-oriented agent collaboration
.
In
First Conference on Language Modeling
,
Cited by:
§5
.
N. Maveli, A. Vergari, and S. B. Cohen (2024)
What can large language models capture about code functional equivalence?
.
arXiv preprint arXiv:2408.11081
.
Cited by:
§2
.
M. Mohammadi, Y. Li, J. Lo, and W. Yip (2025)
Evaluation and benchmarking of llm agents: a survey
.
In
Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2
,
pp. 6129–6139
.
Cited by:
§1
,
§5
.
R. Pan, H. Zhang, and C. Liu (2025)
CodeCoR: an llm-based self-reflective multi-agent framework for code generation
.
arXiv preprint arXiv:2501.07811
.
Cited by:
§1
,
§5
.
B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez,
et al.
(2023)
Code llama: open foundation models for code
.
arXiv preprint arXiv:2308.12950
.
Cited by:
§4.1
.
Y. Song, T. Sun, X. Tang, P. K. Rajput, T. F. Bissyandé, and J. Klein (2025)
Measuring llm code generation stability via structural entropy
.
In
Proceedings of the 40th IEEE/ACM International Conference on Automated Software Engineering
,
pp. 3922–3926
.
Cited by:
§1
,
§2
,
§5
.
Y. Talebirad and A. Nadiri (2023)
Multi-agent collaboration: harnessing the power of intelligent llm agents
.
arXiv preprint arXiv:2306.03314
.
Cited by:
§1
,
§5
.
F. Tip, J. Bell, and M. Schäfer (2025)
Llmorpheus: mutation testing using large language models
.
IEEE Transactions on Software Engineering
.
Cited by:
§1
,
§5
.
G. Wang, Q. Xu, L. Briand, and K. Liu (2026)
Mutation-guided unit test generation with a large language model
.
IEEE Transactions on Software Engineering
.
Cited by:
§1
,
§5
.
W. Wang, F. Wei, L. Dong, H. Bao, N. Yang, and M. Zhou (2020)
Minilm: deep self-attention distillation for task-agnostic compression of pre-trained transformers
.
Advances in neural information processing systems
33
,
pp. 5776–5788
.
Cited by:
§4.1
.
J. Wei, Y. Yao, J. Ton, H. Guo, A. Estornell, and Y. Liu (2024)
Measuring and reducing llm hallucination without gold-standard answers
.
arXiv preprint arXiv:2402.10412
.
Cited by:
§5
.
Q. Xu, G. Wang, L. Briand, and K. Liu (2026)
Hallucination to consensus: multi-agent llms for end-to-end junit test generation
.
ACM Transactions on Software Engineering and Methodology
.
Cited by:
§1
,
§5
.
B. Yang, J. Dang, H. Liu, and Z. Jin (2025)
Advancing llm-generated code reliability: a hybrid approach for hallucination detection
.
IEEE Transactions on Software Engineering
.
Cited by:
§1
,
§5
.
A. Yehudai, L. Eden, A. Li, G. Uziel, Y. Zhao, R. Bar-Haim, A. Cohan, and M. Shmueli-Scheuer (2025)
Survey on evaluation of llm-based agents
.
arXiv preprint arXiv:2503.16416
.
Cited by:
§1
,
§5
.
X. Zhang, Y. Zhang, D. Long, W. Xie, Z. Dai, J. Tang, H. Lin, B. Yang, P. Xie, F. Huang,
et al.
(2024)
MGTE: generalized long-context text representation and reranking models for multilingual text retrieval
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track
,
pp. 1393–1412
.
Cited by:
§4.1
.
Y. Zhang, M. Li, D. Long, X. Zhang, H. Lin, B. Yang, P. Xie, A. Yang, D. Liu, J. Lin, F. Huang, and J. Zhou (2025a)
Qwen3 embedding: advancing text embedding and reranking through foundation models
.
arXiv preprint arXiv:2506.05176
.
Cited by:
§4.1
.
Y. Zhang, Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, Y. Chen,
et al.
(2025b)
Siren’s song in the ai ocean: a survey on hallucination in large language models
.
Computational Linguistics
,
pp. 1–46
.
Cited by:
§5
.
Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma, W. Zhong, J. Chen, M. Mao, and Z. Zheng (2025c)
Llm hallucinations in practical code generation: phenomena, mechanism, and mitigation
.
ACM on Software Engineering
2
(
ISSTA022
),
pp. 481–503
.
Cited by:
§5
.
Q. Zheng, X. Xia, X. Zou, Y. Dong, S. Wang, Y. Xue, L. Shen, Z. Wang, A. Wang, Y. Li,
et al.
(2023)
Codegeex: a pre-trained model for code generation with multilingual benchmarking on humaneval-x
.
In
Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining
,
pp. 5673–5684
.
Cited by:
1st item
.
K. Zhu, H. Du, Z. Hong, X. Yang, S. Guo, Z. Wang, Z. Wang, C. Qian, X. Tang, H. Ji,
et al.
(2025a)
Multiagentbench: evaluating the collaboration and competition of llm agents
.
arXiv preprint arXiv:2503.01935
.
Cited by:
§5
.
Y. Zhu, C. Liu, X. He, X. Ren, Z. Liu, R. Pan, and H. Zhang (2025b)
Adacoder: an adaptive planning and multi-agent framework for function-level code generation
.
IEEE Transactions on Software Engineering
.
Cited by:
§1
,
§5
.
T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf, H. Zhan, J. He, I. Paul,
et al.
(2024)
Bigcodebench: benchmarking code generation with diverse function calls and complex instructions
.
arXiv preprint arXiv:2406.15877
.
Cited by:
2nd item
.