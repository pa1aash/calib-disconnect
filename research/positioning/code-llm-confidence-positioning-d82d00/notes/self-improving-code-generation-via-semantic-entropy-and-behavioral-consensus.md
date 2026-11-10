---
title: Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus
id: self-improving-code-generation-via-semantic-entropy-and-behavioral-consensus
tags:
- code-llm-calibration-aaai27-eabf3f
- semantic-entropy
- self-improvement
- dpo
- internal-confidence-failure
created: '2026-07-17T18:31:02.239755Z'
updated: '2026-07-17T18:33:41.649265Z'
source: https://arxiv.org/html/2603.29292
source_domain: arxiv.org
fetched_at: '2026-07-17T18:31:02.239016Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'ConSelf (Zhang, Cheng, Hu), ICPC 2026. Self-improvement framework using
  code semantic entropy (execution-behavior clustering entropy, NOT text/NLI-based)
  to curate a curriculum of ''learnable'' problems, then fine-tunes via consensus-driven
  DPO (Con-DPO), which weights each DPO preference pair by behavioral-consensus agreement
  among sampled candidates. Backbones: CodeLlama-7B-instruct, DeepSeek-Coder-6.7B-instruct,
  Qwen2.5-Coder-7B -- exact model family overlap with our paper (DeepSeek-Coder-6.7B,
  Qwen2.5-Coder). Benchmarks: HumanEval, MBPP, HumanEval+/MBPP+ (EvalPlus), LiveCodeBench.
  Headline: 2.73-3.95% relative pass@1 improvement over base models, using far less
  training data than Self-SFT/Self-DPO/PFPO baselines (e.g. DeepSeek-Coder: 6,372
  examples vs 46,734 for unfiltered Self-DPO), while Self-SFT/Self-DPO on unfiltered
  self-generated data actively DEGRADE CodeLlama and DeepSeek-Coder. DIRECTLY LOAD-BEARING
  FINDING for our thesis: at the problem-difficulty-prediction level (not solution-level),
  the paper explicitly benchmarks ''internal confidence metrics'' (token-level entropy,
  negative log-likelihood) against code semantic entropy and finds internal metrics
  ''barely surpass random guessing (near 0.5) on CodeLlama'' and show weak or even
  UNDESIRABLE POSITIVE correlation with pass rate on CodeLlama, while code semantic
  entropy reaches AUC up to 0.804 and Pearson r=-0.717 on Qwen -- an independent replication
  of the internal-signal-strong / expressed-signal-weak (log-prob/entropy) pattern
  our paper documents, but at the aggregate problem level rather than per-solution.
  Naive (text/NLI-based) semantic entropy is only moderately effective, again because
  it misses subtle functional-equivalence-breaking token edits. Explicit limitation:
  code semantic entropy requires executing multiple candidate programs (compute cost),
  offers no benefit on problems far beyond model capacity (external supervision still
  needed there), and carries reward-hacking risk if models overfit to self-consistency
  as a proxy for correctness. Relation to disconnect thesis: corroborates from an
  independent angle (problem-level curriculum selection, not per-solution calibration)
  that token-level log-prob/entropy is an unreliable confidence signal for code LLMs
  including DeepSeek-Coder-6.7B and Qwen2.5-Coder-7B specifically, while behavioral/execution-based
  signals are strong -- strengthens the generality claim of our AUROC 0.668 vs 0.987
  finding. Never addresses expressed-interface / verbalized confidence / post-hoc
  calibration at all -- purely a training-time data-curation and DPO-weighting application
  of the internal signal, leaving the prescriptive expressed-interface gap fully open.'
---

Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2603.29292v1 [cs.SE] 31 Mar 2026
\setcctype
by
Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus
Huan Zhang
0009-0000-0644-3775
State Key Laboratory for Novel Software Technology
Nanjing University
Nanjing
China
zhanghuan.nju@gmail.com
,
Wei Cheng
0000-0001-6128-7293
State Key Laboratory for Novel Software Technology
Nanjing University
Nanjing
China
wchengcs.nju@gmail.com
and
Wei Hu
0000-0003-3635-6335
State Key Laboratory for Novel Software Technology
National Institute of Healthcare
Data Science
Nanjing University
Nanjing
China
whu@nju.edu.cn
(2026)
Abstract.
Improving the code generation capabilities of large language models (LLMs) typically relies on supervised fine-tuning or preference optimization, both of which require costly external resources such as powerful teacher models or reliable test units.
However, in real-world scenarios, it is much harder to obtain reference solutions and test oracles than problem descriptions and test inputs.
In this paper, we tackle a challenging yet realistic question:
Can a code language model improve itself without access to a superior teacher and a test oracle?
To answer this, we propose
ConSelf
, a self-improving approach built upon two key ideas.
First, we introduce
code semantic entropy
, a novel metric that measures problem-level uncertainty by assessing the functional diversity of program behaviors, enabling a curriculum construction with the most learnable problems.
Second, we present
consensus-driven direct preference optimization (Con-DPO)
, a preference-based fine-tuning method that weights each preference pair by its behavioral consensus, thereby mitigating the impact of noisy self-generated supervision.
Experiments on various benchmarks and backbone LLMs demonstrate that
ConSelf
significantly outperforms baselines, validating the effectiveness of semantic entropy-based curriculum construction and consensus-driven optimization in improving code generation without external supervision.
code generation, preference optimization, large language model
†
†
journalyear:
2026
†
†
copyright:
cc
†
†
conference:
34th IEEE/ACM International Conference on Program Comprehension; April 12–13, 2026; Rio de Janeiro, Brazil
†
†
booktitle:
34th IEEE/ACM International Conference on Program Comprehension (ICPC ’26), April 12–13, 2026, Rio de Janeiro, Brazil
†
†
doi:
10.1145/3794763.3794798
†
†
isbn:
979-8-4007-2482-4/2026/04
†
†
ccs:
Software and its engineering Automatic programming
1.
Introduction
Automated code generation has become increasingly vital in modern software development, significantly enhancing programming productivity and reducing development costs.
Large language models (LLMs) have demonstrated remarkable progress in this area, with recent models
(OpenAI,
2023
,
2024
; Guo
et al.
,
2024
; Hui
et al.
,
2024
)
achieving impressive performance across a range of code-related tasks and benchmarks.
As the field evolves, researchers have explored various directions to further improve code generation capabilities.
One important research direction is to improve the performance of open-source models, which are more accessible but often lag behind proprietary alternatives.
The predominant paradigm for improving these models is supervised fine-tuning (SFT) on large volumes of high-quality annotated data.
Since manual annotation at scale is prohibitively expensive, numerous data synthesis approaches
(Luo
et al.
,
2024
; Wei
et al.
,
2024b
; Ahmad
et al.
,
2025
; Xu
et al.
,
2025
)
have emerged.
These approaches typically rely on powerful teacher models to generate diverse problem descriptions paired with reference solutions, which are then used to train target models.
Beyond direct SFT, preference-based approaches
(Shojaee
et al.
,
2023
; Zhang
et al.
,
2025a
,
b
,
2024a
; Gee
et al.
,
2025
)
have also shown promise by constructing preference pairs to guide model training.
These approaches generally leverage the execution results of candidate programs on test cases to establish preferences, driving the model to generate preferred code that is functionally correct or more efficient.
Candidate programs used for preference construction are typically sampled from a teacher model
(Zhang
et al.
,
2025a
,
b
)
or generated by the model itself
(Zhang
et al.
,
2024a
; Gee
et al.
,
2025
; Shojaee
et al.
,
2023
)
.
While effective, these approaches hinge on two costly prerequisites: access to a powerful teacher model or the availability of trustworthy test cases.
First, relying on a superior teacher model is not always feasible, as a more capable model may not always exist for specialized or frontier domains.
Moreover, many data synthesis practices typically depend on proprietary LLMs through paid APIs, which introduce significant costs, potential licensing or compliance issues
(Wei
et al.
,
2024a
)
, limiting reproducibility and broader adoption.
Second, the use of test cases (consisting of test inputs and corresponding oracles) poses another fundamental barrier.
Although test inputs can often be synthesized automatically using conventional tools
(Fraser and Arcuri,
2011
; Lukasczyk and Fraser,
2022
)
or LLM-based techniques
(Chen
et al.
,
2023
; Jiao
et al.
,
2025
; Li
et al.
,
2023
; Liu
et al.
,
2023b
; Jiang
et al.
,
2024b
)
, obtaining reliable test oracles remains a persistent challenge, commonly referred to as the
test oracle problem
(Barr
et al.
,
2015
)
in software testing.
Even state-of-the-art LLMs frequently struggle to produce correct oracles
(Wang
et al.
,
2025b
; Liu
et al.
,
2025
; Chen
et al.
,
2025
; Hossain and Dwyer,
2025
)
, leading to false positives that degrade training quality.
Efforts to improve oracle quality via external tools
(Li and Yuan,
2024
)
or additional fine-tuning
(Dinella
et al.
,
2022
; Prasad
et al.
,
2025
; Hossain and Dwyer,
2025
; Ma
et al.
,
2025
)
invariably add to significant cost and complexity.
This disparity motivates our research question:
Can a code language model effectively improve itself with access only to problem descriptions and test inputs, without relying on a superior teacher model or pre-existing test oracles?
This reflects a challenging yet realistic scenario: problem descriptions and test inputs are relatively easy to obtain, whereas reference solutions and reliable test oracles remain expensive and labor-intensive.
Figure 1.
The dilemma of learning from “noisy data” generated for an intractable problem. When all self-generated solutions are flawed, any learning method (SFT/DPO) becomes futile, highlighting the need to identify and filter out such problems.
The dilemma of learning from “noisy data” generated for an intractable problem. When all self-generated solutions are flawed, any learning method (SFT/DPO) becomes futile, highlighting the need to identify and filter out such problems.
In this unsupervised setting, a fundamental challenge arises: Not all problems are equally learnable.
Without external supervision, the model must depend solely on its self-generated outputs.
However, for problems that exceed the model’s current capabilities, these outputs are often highly noisy and devoid of meaningful learning signals.
Figure
1
illustrates this dilemma using the example of
count_primes(n)
. For such a challenging problem, the model may produce several distinct yet flawed solutions.
This diversity of erroneous behaviors makes it nearly impossible for standard self-training approaches
(Huang
et al.
,
2023
; Jiao
et al.
,
2025
)
to identify a reliable learning direction, resulting in what we refer to as “noisy data”.
Training on such low-quality data not only fails to improve the model but also degrades the overall performance and squanders training resources.
Moreover, some problems may already be mastered by the model, offering little marginal value for further training.
We argue that effective unsupervised self-improvement for code generation necessitates a dual-pronged strategy that addresses two complementary challenges.
First,
what to learn?
Select suitable problems and construct a high-quality, learnable curriculum derived from the model’s own outputs.
Second,
how to learn?
Design a robust training algorithm to extract meaningful learning signals while tolerating residual noise in the constructed training samples.
In this paper, we propose
ConSelf
, a consensus-guided approach for self-improving code generation.
To address the challenge of
what to learn
, we introduce a novel metric,
code semantic entropy
, which quantifies the model’s epistemic uncertainty for each problem by measuring the diversity of execution behaviors across multiple generated samples.
High semantic entropy indicates that the model lacks a coherent solving strategy for a given problem. Training on such outputs would likely be unproductive.
ConSelf
implements this insight via a simple yet effective entropy-based filtering mechanism, ensuring that training focuses on problems for which the model can produce meaningful, low-entropy solutions.
As we show shortly, this behavioral metric offers a substantially more reliable indicator of problem difficulty than conventional internal confidence scores, such as token-level entropy and log-likelihood
(Geng
et al.
,
2024
)
.
To address the challenge of
how to learn
, we move beyond the standard direct preference optimization (DPO) paradigm
(Rafailov
et al.
,
2023
)
.
We argue that the binary preference assumption of DPO (the preferred sample is considered strictly better than the rejected ones) does not suit the self-training context, as self-generated preference labels are inherently noisy and vary in reliability.
Therefore, we introduce
consensus-driven DPO (Con-DPO)
, which reframes the learning objective from absolute to consensus-aware preferences.
At the sample level, Con-DPO assigns a consensus score to each preference pair, reflecting the behavioral agreement of the preferred sample with its peers.
By weighting the loss for each preference pair with this score,
ConSelf
adaptively attenuates the learning signal for less reliable preferences, leading to more robust and stable self-improvement.
The main contributions of this paper are outlined as follows:
•
We introduce code semantic entropy, a novel metric that leverages program execution behaviors to robustly estimate a model’s problem-level epistemic uncertainty in an unsupervised manner.
•
We propose
ConSelf
, a self-improvement approach that implements a dual learning strategy. It employs entropy-based filtering to construct a learnable curriculum and adopts consensus-driven DPO to enable robust training.
•
We conduct extensive experiments on standard benchmarks, demonstrating 2.73%–3.95% relative improvement over base models. Further analysis highlights the limitations of internal confidence metrics and underscores the critical role of curriculum design in self-improving for code generation.
2.
Methodology
In this section, we begin by formally defining the problem setup and notations.
Then, we provide an overview of the
ConSelf
approach, followed by a detailed description of each component.
Figure 2.
Overview of the
ConSelf
approach. The model generates code samples for each problem by observation-guided sampling, estimates code semantic entropy to filter problems, and fine-tunes itself on consensus-driven preference pairs.
Overview of the ConSelf approach. The model generates code samples for each problem by observation-guided sampling, estimates code semantic entropy to filter problems, and fine-tunes itself on consensus-driven preference pairs.
2.1.
Overview
Problem Setup.
Let
𝒫
=
{
p
1
,
p
2
,
…
,
p
N
}
\mathcal{P}=\{p_{1},p_{2},\dots,p_{N}\}
denote a set of code generation problems, where each
p
∈
𝒫
p\in\mathcal{P}
is a description of a programming task in natural language.
For each problem
p
p
, we assume access to a corresponding set of test inputs
ℐ
p
=
{
i
1
,
i
2
,
…
,
i
M
}
\mathcal{I}_{p}=\{i_{1},i_{2},\dots,i_{M}\}
.
Unlike prior approaches that rely on external supervision such as reference solutions or test oracles, our setting only requires problem descriptions and associated test inputs.
Our goal is to improve a base code language model
π
θ
\pi_{\theta}
under this constraint by leveraging only self-generated code and the observable behaviors induced by executing these programs on the test inputs.
Approach Overview.
The
ConSelf
approach operates in three main stages. First, for each problem, we prompt the initial model
π
θ
\pi_{\theta}
to generate a diverse set of candidate programs guided by multiple observations.
Second, we evaluate the behavioral consistency of these programs via execution-based clustering. From this, we compute a novel metric, code semantic entropy, which quantifies the model’s epistemic uncertainty for each problem.
An entropy-based filtering strategy allows us to filter out uninformative or intractable problems and construct a curriculum tailored to the current model’s capabilities.
Finally, we construct preference pairs from the retained problems using a consensus-based strategy.
The model is then fine-tuned using Con-DPO, which adaptively weights learning signals based on behavioral consensus.
A high-level illustration of the workflow is shown in Figure
2
.
The full procedure is summarized in Algorithm
1
.
Input:
Problem set
𝒫
\mathcal{P}
, test inputs
ℐ
p
\mathcal{I}_{p}
for each
p
p
, base model
π
θ
\pi_{\theta}
, entropy threshold
τ
\tau
Output:
Updated model
π
θ
′
\pi_{\theta}^{\prime}
1
2
foreach
problem
p
∈
𝒫
p\in\mathcal{P}
do
//
Observation-guided sampling
3
𝒪
p
=
{
o
1
,
…
,
o
n
obs
}
∼
π
θ
(
⋅
∣
Prompt
obs
,
p
)
\mathcal{O}_{p}=\{o_{1},\dots,o_{n_{\text{obs}}}\}\sim\pi_{\theta}(\cdot\mid\text{Prompt}_{\text{obs}},p)
;
4
𝒞
p
←
∅
\mathcal{C}_{p}\leftarrow\emptyset
;
5
foreach
o
i
∈
𝒪
p
o_{i}\in\mathcal{O}_{p}
do
6
C
i
=
{
c
1
(
i
)
,
…
,
c
n
code
(
i
)
}
∼
π
θ
(
⋅
∣
Prompt
code
,
p
,
o
i
)
C_{i}=\{c_{1}^{(i)},\dots,c_{n_{\text{code}}}^{(i)}\}\sim\pi_{\theta}(\cdot\mid\text{Prompt}_{\text{code}},p,o_{i})
;
7
𝒞
p
←
𝒞
p
∪
C
i
\mathcal{C}_{p}\leftarrow\mathcal{C}_{p}\cup C_{i}
;
//
Code semantic entropy computation
8
foreach
c
k
∈
𝒞
p
c_{k}\in\mathcal{C}_{p}
do
9
𝐄
k
←
Execute
​
(
c
k
,
ℐ
p
)
\mathbf{E}_{k}\leftarrow\text{Execute}(c_{k},\mathcal{I}_{p})
;
10
H
​
(
p
)
←
CodeSemanticEntropy
​
(
{
𝐄
k
}
k
=
1
K
)
H(p)\leftarrow\text{CodeSemanticEntropy}(\{\mathbf{E}_{k}\}_{k=1}^{K})
;
⊳
\triangleright
Eq. (
2
)
11
12
//
Curriculum curation
𝒫
filtered
←
{
p
∈
𝒫
∣
0
<
H
norm
​
(
p
)
<
τ
}
\mathcal{P}_{\text{filtered}}\leftarrow\{p\in\mathcal{P}\mid 0<H_{\text{norm}}(p)<\tau\}
;
⊳
\triangleright
Sec.
2.3
13
//
Preference construction and optimization
14
foreach
p
∈
𝒫
filtered
p\in\mathcal{P}_{\text{filtered}}
do
{
R
​
(
c
k
)
}
←
ConsensusScore
​
(
p
,
𝒞
p
,
ℐ
p
,
{
𝐄
k
}
)
\{R(c_{k})\}\leftarrow\text{ConsensusScore}(p,\mathcal{C}_{p},\mathcal{I}_{p},\{\mathbf{E}_{k}\})
;
⊳
\triangleright
Alg.
2
𝒟
p
←
ConstructPairs
​
(
p
,
𝒞
p
,
{
R
​
(
c
k
)
}
)
\mathcal{D}_{p}\leftarrow\text{ConstructPairs}(p,\mathcal{C}_{p},\{R(c_{k})\})
;
⊳
\triangleright
Sec.
2.4
15
16
𝒟
←
⋃
p
∈
𝒫
filtered
𝒟
p
\mathcal{D}\leftarrow\bigcup_{p\in\mathcal{P}_{\text{filtered}}}\mathcal{D}_{p}
;
π
θ
′
←
Con-DPO
​
(
π
θ
,
𝒟
)
\pi_{\theta}^{\prime}\leftarrow\text{Con-DPO}(\pi_{\theta},\mathcal{D})
;
⊳
\triangleright
Eq. (
5
)
17
return
π
θ
′
\pi_{\theta}^{\prime}
;
Algorithm 1
The framework of
ConSelf
2.2.
Observation-Guided Sampling
A diverse and informative set of candidate programs is a prerequisite for any meaningful self-improvement.
If the model repeatedly generates a single (potentially incorrect) solution for a given problem, it provides little useful signal for preference-based learning or curriculum construction.
To address this foundational need, we design an observation-guided sampling strategy to create a rich and behaviorally diverse candidate pool.
Our method is inspired by recent findings in search-based code generation
(Wang
et al.
,
2025a
)
, which demonstrate that prompting the model to first generate diverse “plans” or “observations” about a problem leads to a significantly more diverse set of final solutions.
We incorporate this principle into our sampling strategy.
Figure 3.
The prompt template for observation generation and example observations generated for the
count_primes(n)
problem.
The prompt guides the model to produce diverse insights, serving as varied conditions for code generation.
The prompt template for observation generation.
The process is outlined in Lines 2–6 of Algorithm
1
. For each problem
p
p
, we first prompt the model
π
θ
\pi_{\theta}
to generate a set of
n
obs
n_{\text{obs}}
distinct textual observations
𝒪
p
=
{
o
1
,
…
,
o
n
obs
}
\mathcal{O}_{p}=\{o_{1},\dots,o_{n_{\text{obs}}}\}
.
Figure
3
shows the prompt template that we use, along with concrete examples of the observations generated for the
count_primes(n)
problem, illustrating how they capture different facets like key definitions, potential pitfalls, and high-level strategies.
Second, for each observation
o
i
∈
𝒪
p
o_{i}\in\mathcal{O}_{p}
, we condition the code generation on it, prompting the model to generate
n
code
n_{\text{code}}
candidate programs using high-temperature sampling (see Figure
4
).
The final candidate set
𝒞
p
\mathcal{C}_{p}
for problem
p
p
is the union of all programs generated across all observations.
This two-step process steers the model towards a wider spectrum of solution attempts in a controlled manner, creating a richer foundation for subsequent analysis.
Note that this observation-guided sampling is a foundational setup applied consistently across all methods evaluated in our experiments, including our
ConSelf
and all baselines.
Its purpose is to ensure that every method starts with a sufficiently diverse candidate pool, which is a necessary precondition for any meaningful self-improvement study.
Thus, it is not considered a component for ablation but rather part of the problem-solving testbed itself.
Figure 4.
The prompt template for code generation. The model generates
n
code
n_{\text{code}}
candidate programs conditioned on each observation to enhance solution diversity.
The prompt template for code generation.
2.3.
Curriculum Curation
After generating a diverse candidate pool
𝒞
p
\mathcal{C}_{p}
for each problem
p
p
, we arrive at the central challenge of
what to learn
.
As shown in Figure
1
, indiscriminately training on all problems can introduce significant noise, leading to wasted computation or even performance degradation.
The next step is to curate a curriculum by identifying problems that are learnable and informative tailored to the current model
π
θ
\pi_{\theta}
.
In our unsupervised setting, where reference solutions and test oracles are unavailable, assessing a model’s competence on a given problem requires a reliable uncertainty metric.
We begin by considering representative baseline metrics to contextualize our contribution.
Internal Confidence Metrics
The most common methods for estimating LLM uncertainty rely on the model’s internal state during generation
(Geng
et al.
,
2024
)
.
We consider
token-level entropy
, which measures the average predictive uncertainty at each decoding step, and
negative log-likelihood (NLL)
, which reflects how probable a generated sequence is under the model’s own distribution.
Naive Semantic Entropy
Inspired by uncertainty estimation in natural language generation (NLG) tasks, we adapt the
semantic entropy
(Kuhn
et al.
,
2023
)
directly to code.
This approach treats code as plain text, first generating multiple candidate programs and then clustering them based on linguistic invariances, typically measured by bidirectional entailment relationships captured via an additionally fine-tuned text-embedding model.
The entropy is then computed over the resulting cluster distribution.
All of the aforementioned metrics are fundamentally misaligned with the primary goal of code generation:
functional correctness
. As we empirically show in Section
3.3
, they often fail to reliably distinguish between correct and incorrect programs.
A model can be highly “confident” (low NLL, low token entropy) yet consistently produce buggy code.
More critically, treating code as text like naive semantic entropy ignores its executable nature, which is its most important property.
Moreover, the reliance on linguistic invariances from naive semantic entropy is fragile for code.
The correctness of a program is acutely sensitive to symbolic changes that may be imperceptible to text-embedding models.
These limitations motivate our search for a more robust metric.
Code Semantic Entropy
To overcome these shortcomings, we propose
code semantic entropy
, an uncertainty metric grounded in the observable functional behavior of programs.
Our central insight is that for code, true semantic uncertainty must be measured in the space of program execution, not linguistic representation or internal confidence.
Instead of asking “How confident does the model feel?”, code semantic entropy asks “How consistently does the model act?”.
This move from internal, subjective state to external, verifiable behavior is key to robustly assessing a model’s true competence.
The computation involves two main steps.
First, for each problem
p
∈
𝒫
p\in\mathcal{P}
, we execute its candidate programs
𝒞
p
=
{
c
1
,
…
,
c
K
}
\mathcal{C}_{p}=\{c_{1},\dots,c_{K}\}
, against the set of test inputs
ℐ
p
=
{
i
1
,
…
,
i
M
}
\mathcal{I}_{p}=\{i_{1},\dots,i_{M}\}
.
The execution trace of a candidate
c
k
c_{k}
is the tuple of its outputs:
𝐄
k
=
[
Exec
​
(
c
k
,
i
1
)
,
…
,
Exec
​
(
c
k
,
i
M
)
]
.
\mathbf{E}_{k}=\left[\text{Exec}(c_{k},i_{1}),\dots,\text{Exec}(c_{k},i_{M})\right].
This execution step grounds our analysis in concrete, observable functional behavior.
Candidates that fail to compile or trigger runtime errors on all test inputs are marked as
crashed
.
Let
𝒞
p
′
⊆
𝒞
p
\mathcal{C}^{\prime}_{p}\subseteq\mathcal{C}_{p}
denote the set of non-crashed candidates.
We exclude problems where
|
𝒞
p
′
|
<
3
|\mathcal{C}^{\prime}_{p}|<3
as this provides insufficient data for a meaningful entropy calculation.
Second, we group the surviving candidates
𝒞
p
′
\mathcal{C}^{\prime}_{p}
by their identical execution traces, forming a set of behavioral clusters
ℬ
p
=
{
B
1
,
…
,
B
N
p
}
\mathcal{B}_{p}=\{B_{1},\dots,B_{N_{p}}\}
, where each
B
j
⊆
𝒞
p
′
B_{j}\subseteq\mathcal{C}^{\prime}_{p}
contains candidates with the same output behavior.
Formally, the partition satisfies:
(1)
{
∀
c
m
,
c
n
∈
B
j
,
𝐄
m
=
𝐄
n
∀
B
j
≠
B
j
′
,
∃
c
∈
B
j
,
c
′
∈
B
j
′
,
𝐄
c
≠
𝐄
c
′
.
\displaystyle\begin{cases}\forall c_{m},c_{n}\in B_{j},&\mathbf{E}_{m}=\mathbf{E}_{n}\\
\forall B_{j}\neq B_{j^{\prime}},\;\exists\,c\in B_{j},c^{\prime}\in B_{j^{\prime}},&\,\,\mathbf{E}_{c}\neq\mathbf{E}_{c^{\prime}}\end{cases}.
This reveals a key insight:
due to the variability of incorrect semantics and the diversity induced by observation-guided sampling, intractable problems tend to fragment into many small behavioral clusters.
To quantify this behavioral dispersion, we define the code semantic entropy for problem
p
p
as the Shannon entropy over the cluster distribution:
(2)
H
​
(
p
)
=
−
∑
j
=
1
N
p
|
B
j
|
|
𝒞
p
′
|
​
log
⁡
(
|
B
j
|
|
𝒞
p
′
|
)
.
\displaystyle H(p)=-\sum_{j=1}^{N_{p}}\frac{|B_{j}|}{|\mathcal{C}^{\prime}_{p}|}\log\left(\frac{|B_{j}|}{|\mathcal{C}^{\prime}_{p}|}\right).
This metric quantifies the epistemic uncertainty at the problem level: high entropy signifies high functional disagreement, while low entropy suggests that the model has converged on a consistent behavior, whether correct or not.
Entropy-Based Filtering
With the code semantic entropy
H
​
(
p
)
H(p)
computed for each problem, we can construct the learnable curriculum.
Problems at the extremes of the uncertainty spectrum are suboptimal for self-improvement: those with excessively high entropy indicate chaotic model behavior with no reliable learning signal, while zero-entropy problems offer no behavioral variation from which to form preference pairs.
We therefore curate the curriculum by filtering out these two extremes.
To enable consistent filtering, we first normalize the entropy values across all problems to the range
[
0
,
1
]
[0,1]
using min-max normalization.
We then select problems whose normalized entropy lies within the range:
(3)
𝒫
filtered
=
{
p
∈
𝒫
∣
0
<
H
norm
​
(
p
)
<
τ
}
,
\displaystyle\mathcal{P}_{\text{filtered}}=\{p\in\mathcal{P}\mid 0<H_{\text{norm}}(p)<\tau\},
where
τ
\tau
is a tunable upper threshold used to discard high-entropy problems.
Zero-entropy cases are naturally excluded, as they indicate that all generated candidates are functionally identical. This typically corresponds to two scenarios:
(1)
Trivial Success:
The model has already mastered the problem: all candidates are correct. No further improvement is needed.
(2)
Consistent Failure:
The model is stuck in a single incorrect behavior, no useful learning signal can be derived.
In both scenarios, zero-entropy problems are either unnecessary or useless for self-improvement.
Our primary focus is therefore on tuning the upper threshold
τ
\tau
, which controls the trade-off between including more diverse problems and introducing more noise.
We examine this trade-off in detail in Section
3.5
.
This filtering process directly realizes our strategy of selecting
what to learn
.
2.4.
Consensus-Driven Preference Optimization
After curating the curriculum, we turn to the second core challenge:
how to learn
from this filtered yet still imperfect self-generated data.
We build upon direct preference optimization (DPO)
(Rafailov
et al.
,
2023
)
, a powerful technique that has proven effective for code generation
(Jiao
et al.
,
2025
; Zhang
et al.
,
2025a
,
2024a
; Gee
et al.
,
2025
)
.
The standard DPO process involves fine-tuning a model on a dataset of preference pairs
(
y
w
,
y
l
)
(y_{w},y_{l})
, where
y
w
y_{w}
is the preferred response (winner) and
y
l
y_{l}
is the rejected one (loser).
Applying DPO in our unsupervised setting introduces a challenge: constructing reliable preference pairs
(
y
w
,
y
l
)
(y_{w},y_{l})
without access to ground-truth labels.
A common approach is to designate a “winner” using a proxy signal such as a score derived from consistency
(Huang
et al.
,
2023
)
.
Although this winner may appear more plausible, it is not guaranteed to be correct, as the selection is made within a noisy candidate set.
The standard DPO objective, which treats all preference pairs with equal confidence, is ill-suited to handle the varying reliability of these self-labeled pairs.
This can lead to overfitting on ambiguous or incorrect preferences, undermining the self-improvement process.
To address this, we introduce
consensus-driven DPO (Con-DPO)
. Instead of treating all preferences as equally valid, Con-DPO reframes the learning objective to be confidence-aware.
It achieves this through a three-step process: (1) quantifying the reliability of each candidate with a consensus score, (2) constructing preference pairs based on these scores, and (3) optimizing the model with a consensus-weighted loss.
Behavioral Consensus Score
We first quantify the reliability of each candidate with a behavioral consensus score, denoted by
R
​
(
c
k
)
R(c_{k})
.
This score reflects the degree to which a candidate’s functional behavior aligns with its peers.
The underlying intuition is that a behavior shared by many independently sampled candidates is more likely to be correct or at least plausible, while a behavior that appears rarely is more likely to be an error or an outlier.
In Algorithm
2
, let
E
k
​
[
j
]
\textbf{E}_{k}[j]
denote the execution output of candidate
c
k
c_{k}
on input
i
j
i_{j}
.
For each test input
i
j
∈
ℐ
p
i_{j}\in\mathcal{I}_{p}
, we collect the set of valid outputs
𝒱
j
\mathcal{V}_{j}
produced by all candidates.
Then, we calculate how frequently
c
k
c_{k}
’s output
E
k
​
[
j
]
\textbf{E}_{k}[j]
appears within
𝒱
j
\mathcal{V}_{j}
.
The final score
R
​
(
c
k
)
R(c_{k})
is the average of these frequencies across all test inputs.
This score, ranging from 0 to 1, serves as a soft measure of behavioral consensus.
Crashed candidates are assigned a score of zero as they fail to produce any valid output on any given test input.
Preference Pair Construction
With the consensus scores computed, we construct the training dataset
𝒟
\mathcal{D}
.
This process is outlined in Lines 11–14 of Algorithm
1
.
For each problem
p
∈
𝒫
filtered
p\in\mathcal{P}_{\text{filtered}}
, we construct multiple preference tuples of the form
(
p
,
y
w
,
y
l
)
(p,y_{w},y_{l})
, where
y
w
y_{w}
is the preferred winner and
y
l
y_{l}
is the rejected loser.
Specifically, we select the candidate with the highest consensus score as the winner, and pair it with other candidates that have strictly lower scores as the losers.
To maximize the informativeness of the training signal, we prioritize pairing
y
w
y_{w}
with non-crashed, low-scoring candidates, which encourages the model to learn from meaningful behavioral differences.
In practice, we select up to three such negative samples per problem to balance informativeness and dataset size.
The final training dataset
𝒟
\mathcal{D}
is the collection of all such tuples from all problems across the curated curriculum.
The Objective of Con-DPO
Finally, we adopt the standard DPO objective to incorporate our confidence measure.
The original DPO loss encourages the policy to assign a higher likelihood to preferred responses compared to rejected ones.
For a given preference tuple
(
p
,
y
w
,
y
l
)
(p,y_{w},y_{l})
, the reward difference is defined as
(4)
r
^
​
(
y
w
,
y
l
)
=
β
​
(
log
⁡
π
θ
​
(
y
w
∣
p
)
π
ref
​
(
y
w
∣
p
)
−
log
⁡
π
θ
​
(
y
l
∣
p
)
π
ref
​
(
y
l
∣
p
)
)
,
\displaystyle\hat{r}(y_{w},y_{l})=\beta\left(\log\frac{\pi_{\theta}(y_{w}\mid p)}{\pi_{\text{ref}}(y_{w}\mid p)}-\log\frac{\pi_{\theta}(y_{l}\mid p)}{\pi_{\text{ref}}(y_{l}\mid p)}\right),
where
π
θ
\pi_{\theta}
is the current policy,
π
ref
\pi_{\text{ref}}
is a frozen reference model, and
β
\beta
is a scaling hyperparameter.
The DPO loss for the dataset
𝒟
\mathcal{D}
is then computed as:
ℒ
DPO
=
−
𝔼
(
p
,
y
w
,
y
l
)
∼
𝒟
​
[
log
⁡
σ
​
(
r
^
​
(
y
w
,
y
l
)
)
]
\mathcal{L}_{\text{DPO}}=-\,\mathbb{E}_{(p,y_{w},y_{l})\sim\mathcal{D}}[\log\sigma(\hat{r}(y_{w},y_{l}))]
.
To reflect our confidence in each self-labeled pair, we refine this objective by incorporating the winner’s consensus score
R
​
(
y
w
)
R(y_{w})
as a sample-wise weight.
The resulting Con-DPO objective is
(5)
ℒ
Con-DPO
=
−
𝔼
(
p
,
y
w
,
y
l
)
∼
𝒟
​
[
R
​
(
y
w
)
⋅
log
⁡
σ
​
(
r
^
​
(
y
w
,
y
l
)
)
]
.
\displaystyle\mathcal{L}_{\text{Con-DPO}}=-\,\mathbb{E}_{(p,y_{w},y_{l})\sim\mathcal{D}}\left[R(y_{w})\cdot\log\sigma(\hat{r}(y_{w},y_{l}))\right].
By weighting each term by
R
​
(
y
w
)
R(y_{w})
, Con-DPO adaptively modulates the learning signal.
The model learns aggressively from high-consensus pairs, which are deemed more reliable, while learning more cautiously from uncertain ones.
This consensus-weighted learning mechanism mitigates the risk of overfitting to noisy or unreliable self-generated preferences, directly realizing our strategy for
how to learn
.
Input:
Problem
p
p
with candidates
𝒞
p
\mathcal{C}_{p}
, test inputs
ℐ
p
\mathcal{I}_{p}
, execution traces
{
𝐄
k
:
c
k
∈
𝒞
p
}
\{\mathbf{E}_{k}:c_{k}\in\mathcal{C}_{p}\}
Output:
Consensus scores
{
R
​
(
c
k
)
:
c
k
∈
𝒞
p
}
\{R(c_{k}):c_{k}\in\mathcal{C}_{p}\}
1
foreach
c
k
∈
𝒞
p
c_{k}\in\mathcal{C}_{p}
do
2
R
​
(
c
k
)
←
0
R(c_{k})\leftarrow 0
;
3
foreach
i
j
∈
ℐ
p
i_{j}\in\mathcal{I}_{p}
do
//
Collect all valid outputs
4
𝒱
j
←
{
𝐄
l
​
[
j
]
:
c
l
∈
𝒞
p
,
𝐄
l
​
[
j
]
≠
crash
}
\mathcal{V}_{j}\leftarrow\{\mathbf{E}_{l}[j]:c_{l}\in\mathcal{C}_{p},\mathbf{E}_{l}[j]\neq\text{crash}\}
;
5
f
​
r
​
e
​
q
j
←
|
{
o
∈
𝒱
j
:
o
=
𝐄
k
​
[
j
]
}
|
freq_{j}\leftarrow|\{o\in\mathcal{V}_{j}:o=\mathbf{E}_{k}[j]\}|
;
6
R
​
(
c
k
)
←
R
​
(
c
k
)
+
f
​
r
​
e
​
q
j
|
𝒱
j
|
R(c_{k})\leftarrow R(c_{k})+\frac{freq_{j}}{|\mathcal{V}_{j}|}
;
7
8
R
​
(
c
k
)
←
R
​
(
c
k
)
|
ℐ
p
|
R(c_{k})\leftarrow\frac{R(c_{k})}{|\mathcal{I}_{p}|}
;
9
10
return
{
R
​
(
c
k
)
}
\{R(c_{k})\}
;
Algorithm 2
Consensus score calculation
Table 1.
Performance comparison across different LLMs and methods on four code generation benchmarks. All results are reported using pass@1 scores (%). RI denotes relative improvement over the base model.
Performance comparison across different LLMs and methods on four code generation benchmarks.
Backbone LLMs
Methods
HumanEval
MBPP
EvalPlus
LiveCodeBench
Avg.
RI
↑
\uparrow
HE+
MBPP+
Easy
Medium
Hard
Overall
CodeLlama-7B
Base model
35.98
52.91
31.10
44.80
23.06
1.21
0.27
7.80
34.52
-
PFPO
34.55
53.09
29.27
44.97
23.66
1.01
0.54
8.11
33.99
−
1.54
%
-1.54\%
Self-SFT
32.93
50.88
27.24
43.03
20.19
0.91
0.02
6.82
32.18
−
6.78
%
-6.78\%
Self-DPO
33.54
53.17
28.86
45.33
19.35
1.11
0.36
7.73
33.73
−
2.29
%
-2.29\%
ConSelf
36.59
55.03
31.50
46.74
24.85
1.31
0.27
8.45
35.66
3.30%
DeepSeek-Coder-6.7B
Base model
77.24
74.87
71.14
66.58
44.21
9.97
0.72
18.07
61.58
-
PFPO
74.39
72.75
69.51
64.81
43.01
8.76
0.63
17.27
59.75
−
2.97
%
-2.97\%
Self-SFT
72.56
70.90
68.29
62.17
40.14
7.55
0.54
15.80
57.94
−
5.91
%
-5.91\%
Self-DPO
74.80
73.28
70.12
65.08
43.73
8.46
0.72
17.35
60.13
−
2.35
%
-2.35\%
ConSelf
78.46
76.98
72.15
68.78
48.75
10.88
0.90
19.92
63.26
2.73%
Qwen2.5-Coder-7B
Base model
88.21
82.80
84.15
71.34
68.58
22.05
2.97
31.29
71.56
-
PFPO
89.21
82.54
85.37
71.69
69.89
23.56
2.88
32.20
72.20
0.89%
Self-SFT
85.77
82.01
81.09
71.16
65.23
21.75
1.80
29.70
69.95
−
2.25
%
-2.25\%
Self-DPO
88.82
82.63
84.53
71.52
69.53
22.26
2.79
31.59
71.78
0.31%
ConSelf
91.46
86.51
86.59
74.60
71.33
23.26
3.33
32.77
74.39
3.95%
3.
Experiments
In this section, we conduct experiments to evaluate the effectiveness of
ConSelf
. We focus on the following research questions:
•
RQ1 (overall performance):
Can
ConSelf
effectively improve the performance of code language models under the unsupervised setting, and to what extent?
•
RQ2 (effectiveness of code semantic entropy):
In the context of code generation, is code semantic entropy a more reliable indicator of model uncertainty compared to existing internal confidence metrics?
•
RQ3 (ablation study):
How do the core components of
ConSelf
, including curriculum curation and Con-DPO, contribute to the overall performance?
•
RQ4 (impact of filtering threshold):
How does the varying curriculum filtering threshold
τ
\tau
impact performance?
3.1.
Experimental Setup
Dataset Construction
All training data in our experiments are drawn from the TACO dataset
(Li
et al.
,
2023
)
, a large-scale and comprehensive code generation dataset integrating several existing benchmarks, such as APPS
(Hendrycks
et al.
,
2021
)
and CodeContest
(Li
et al.
,
2022
)
.
TACO provides a diverse set of Python code problems spanning a wide range of difficulty levels, each accompanied by a rich collection of test inputs.
To simulate the unsupervised setup, we only use the problem descriptions and associated test inputs, discarding the reference solutions and oracle outputs.
We perform a preprocessing step to ensure data quality, removing problems that contain images, lack test inputs, or include malformed starter code.
To prevent data leakage, we further perform string-based matching on problem descriptions to ensure no overlap with downstream evaluation benchmarks.
We obtain a final set of 19,764 problems for our experiments.
Benchmarks and Backbone LLMs
We evaluate on four widely-used benchmarks, spanning a range of difficulty levels and domains:
HumanEval, MBPP, EvalPlus, and LiveCodeBench.
HumanEval
(Chen
et al.
,
2021
)
is a standard benchmark consisting of 164 hand-authored Python problems.
MBPP
(Austin
et al.
,
2021
)
is a crowd-sourced dataset of basic programming tasks.
EvalPlus
(Liu
et al.
,
2023b
)
enhances the previous two with more rigorous edge cases, creating the HE+ and MBPP+ variants for a more challenging evaluation.
LiveCodeBench
(Jain
et al.
,
2025
)
contains 880 problems from programming competitions collected up to February 2025, categorized by difficulty. We use version 5 in our evaluation.
For backbone models, we adopt three open-source code LLMs: CodeLlama-7B-instruct
(Rozière
et al.
,
2023
)
, DeepSeek-Coder-6.7B-instruct
(Guo
et al.
,
2024
)
, and Qwen-2.5-Coder-7B-instruct
(Hui
et al.
,
2024
)
.
These models are developed by different organizations and collectively represent the current landscape of publicly available code language models.
Evaluation Metrics
Following previous works
(Chen
et al.
,
2024
; Jiang
et al.
,
2024a
; Li
et al.
,
2025
; Zhang
et al.
,
2024b
)
, we use greedy pass@1 as our primary evaluation metric.
All models perform inference with
temperature
=
0
\text{temperature}=0
for deterministic decoding.
Implementation
All models are fine-tuned using Low-Rank Adaptation (LoRA)
(Hu
et al.
,
2022
)
with a maximum sequence length of 2,048 tokens.
We use a global batch size of 16 and a learning rate of 5e-6, scheduled with cosine decay and warm-up.
Training is conducted using the bf16 data type.
We assign the LoRA rank to 16 and
α
\alpha
to 32.
For preference optimization methods, we use a DPO parameter of
β
=
0.1
\beta=0.1
.
We employ vLLM
(Kwon
et al.
,
2023
)
for efficient inference.
The filtering threshold
τ
\tau
in our main evaluation is set to 0.55 for Qwen2.5-Coder and 0.3 for CodeLlama and DeepSeek-Coder.
We use the official test set of the TACO dataset as the validation set to select
τ
\tau
. This set has zero overlap with our final evaluation benchmarks.
For each problem
p
p
, we follow the observation-guided sampling strategy described in Section
2.2
to obtain the candidate program set
𝒞
p
\mathcal{C}_{p}
.
To balance candidate diversity against computational cost, we generate
n
obs
=
3
n_{\text{obs}}=3
textual observations, and for each observation, we sample
n
code
=
5
n_{\text{code}}=5
candidate programs by temperature sampling with
temperature
=
1.0
\text{temperature}=1.0
, resulting in
K
=
15
K=15
candidates per problem.
1
1
1
https://github.com/nju-websoft/ConSelf
All experiments are conducted on an X86 server with two Intel Xeon Gold 6326 CPUs, 512 GB of memory, and NVIDIA A800 GPU.
3.2.
Overall Performance
To answer RQ1, we evaluate whether
ConSelf
can effectively improve the code generation performance in the unsupervised setting.
The primary goal is to determine if our proposed approach can achieve superior performance over existing unsupervised methods and self-training variants.
To avoid high variance and randomness, we run each approach three times and report the average as the final result.
We compare
ConSelf
with the following methods:
•
Base model
: The original instruction-tuned model without any further training on TACO.
•
PFPO
(pseudo feedback preference optimization)
(Jiao
et al.
,
2025
)
: For a problem, PFPO first performs majority voting on execution outputs across all candidates to create “pseudo” test cases.
It then constructs preference pairs based on the proportion of pseudo test cases that each candidate passes and fine-tunes the model using the standard DPO loss.
•
Self-SFT
(Huang
et al.
,
2023
)
: We choose the preferred candidate
y
w
y_{w}
as the “high confidence” solutions from all problems without any filtering and fine-tune the model using those solutions as target outputs with the standard language modeling loss.
•
Self-DPO
: This method uses all problems without filtering. For each problem, it constructs preference pairs from self-generated candidates following Section
2.4
and fine-tunes the model using the standard DPO loss.
All methods access execution and crash information under the same execution environment to ensure a fair comparison.
Figure 5.
Comparison of the number of training examples generated by different methods for each model.
A bar chart comparing the number of training examples for three models: CodeLlama, DeepSeek-Coder, and Qwen2.5-Coder. For each model, there are four bars. The bar for ConSelf is consistently short.
Results and Analysis.
The results are shown in Table
1
, where we report pass@1 accuracy and relative improvements over the base models.
Across all settings,
ConSelf
consistently improves over the base model and outperforms other baselines.
For CodeLlama-7B, DeepSeek-Coder-6.7B, and Qwen2.5-Coder-7B,
ConSelf
obtains average relative improvements of
+
3.30
%
+3.30\%
,
+
2.73
%
+2.73\%
, and
+
3.95
%
+3.95\%
, respectively.
These gains are achieved without access to reference code and test oracles, demonstrating the effectiveness of our approach.
Notably, these superior results are achieved with remarkable data efficiency. Figure
5
shows that our curriculum curation strategy enables
ConSelf
to train on a substantially smaller and more focused dataset.
For instance, on DeepSeek-Coder, it utilizes just 6,372 training examples, a small fraction of the data used by the unfiltered Self-DPO (46,734) and PFPO (42,278).
By filtering out intractable problems, our approach builds a high-quality training set that provides more reliable learning signals.
The precise trade-off between data diversity and quality is analyzed in Section
3.5
.
Figure 6.
Area Under ROC Curve (AUC) for discriminating solvable (
pass rate
>
0
\text{pass rate}>0
) problems and unsolvable (
pass rate
=
0
\text{pass rate}=0
) ones. An AUC of 0.5 indicates no discriminative ability.
Area Under ROC Curve (AUC) for discriminating solvable ($\text{pass rate}>0$) problems.
In contrast, the baselines reveal the pitfalls of unsupervised learning without a well-designed curriculum.
Self-SFT and Self-DPO, both trained on the full unfiltered set of self-generated data, consistently degrade performance on CodeLlama and DeepSeek-Coder.
Self-SFT, which fine-tunes directly on winning candidates, performs the worst across all settings.
Self-DPO, while using a preference-based objective, offers only marginal gains and still fails to outperform the base models.
This shows that preference modeling alone is insufficient—without filtering, the model is overwhelmed by noisy and uninformative preference pairs.
Naively learning from self-generated noisy outputs leads to overfitting spurious patterns and reinforces its own incorrect behaviors.
While PFPO slightly improves Qwen2.5-Coder, it degrades performance on the other two models, highlighting the brittleness of pseudo test case construction in noisy settings.
Answer to RQ1
ConSelf
consistently improves code generation accuracy across models and datasets without relying on reference code or test oracles.
It outperforms both SFT- and DPO-based baselines using significantly less training data.
3.3.
Effectiveness of Code Semantic Entropy
As presented in Section
2.3
, effective curriculum curation requires a reliable signal to determine if a problem is learnable for the current model.
This learnability implies that a model can generate diverse, partially correct outputs, indicating the task is neither trivially solvable nor entirely beyond its capability.
A good indicator should therefore capture this behavioral uncertainty and correlate strongly with actual model performance.
To evaluate the effectiveness of different metrics, we compare our
code semantic entropy
against two internal confidence metrics (
token-level entropy
and
negative log-likelihood
) and the
naive semantic entropy
adapted from the original paper
(Kuhn
et al.
,
2023
)
.
In addition, we include
crash rate
as a heuristic, model-agnostic baseline. Although it does not directly measure uncertainty, we include it for reference, as problems with frequent execution failures tend to be more difficult.
For our analysis, we compute the pass rate for each problem using the dataset-provided test oracles.
Note that these oracles are used solely for evaluation purposes and are never seen by
ConSelf
during training.
We evaluate the metrics on three complementary tasks:
•
Discriminative Ability:
To assess each metric’s ability to distinguish “solvable” problems (
pass rate
>
0
\text{pass rate}>0
) from “unsolvable” ones (
pass rate
=
0
\text{pass rate}=0
), we report the
Area Under ROC Curve (AUC)
.
An AUC score closer to 1.0 indicates better discriminative power.
•
Correlation with Performance:
We compute the correlation between each metric and the problem pass rate using Pearson, Spearman, and Kendall coefficients.
A strong negative correlation indicates that the metric reliably reflects problem difficulty or model uncertainty.
•
End-to-End Impact:
To fairly compare each metric’s effectiveness in selecting high-quality data for self-improvement, we use each to curate a training set matching the sample count of the
ConSelf
(Figure
5
).
We then train separate models with the identical Con-DPO process and compare their average performance.
Table 2.
Correlation coefficients and
p
p
-values between each metric and pass rate for each model. Background color indicates correlation strength and direction (blue = desirable, and red = undesirable). “0” indicates
p
<
10
−
300
p<10^{-300}
.
Correlation coefficients and $p$-values between each metric and pass rate for each model.
Metrics
Pearson (
p
p
)
Spearman (
p
p
)
Kendall (
p
p
)
CodeLlama-7B
Crash rate
−
0.344
-0.344
(6e-181)
−
0.240
-0.240
(9e-83)
−
0.207
-0.207
(5e-85)
Code sem. entropy
−
0.327
-0.327
(4e-195)
−
0.292
-0.292
(1e-133)
−
0.195
-0.195
(8e-133)
Naive sem. entropy
−
0.265
-0.265
(2e-110)
−
0.229
-0.229
(5e-95)
−
0.180
-0.180
(1e-65)
Neg. log-likelihood
0.084
0.084
(4e-26)
0.061
0.061
(1e-14)
0.041
0.041
(1e-14)
Token-level entropy
0.078
0.078
(1e-22)
0.058
0.058
(1e-13)
0.039
0.039
(1e-13)
DeepSeek-Coder-6.7B
Crash rate
−
0.270
-0.270
(4e-295)
−
0.337
-0.337
(0)
−
0.287
-0.287
(0)
Code sem. entropy
−
0.712
-0.712
(0)
−
0.572
-0.572
(0)
−
0.445
-0.445
(0)
Naive sem. entropy
−
0.275
-0.275
(8e-12)
−
0.244
-0.244
(4e-7)
−
0.225
-0.225
(4e-7)
Neg. log-likelihood
−
0.054
-0.054
(5e-13)
−
0.035
-0.035
(3e-6)
−
0.027
-0.027
(4e-6)
Token-level entropy
−
0.033
-0.033
(9e-6)
−
0.014
-0.014
(6e-6)
−
0.011
-0.011
(7e-4)
Qwen2.5-Coder-7B
Crash rate
−
0.261
-0.261
(4e-277)
−
0.303
-0.303
(0)
−
0.256
-0.256
(0)
Code sem. entropy
−
0.717
-0.717
(0)
−
0.624
-0.624
(0)
−
0.528
-0.528
(0)
Naive sem. entropy
−
0.287
-0.287
(3e-130)
−
0.251
-0.251
(6e-105)
−
0.232
-0.232
(1e-95)
Neg. log-likelihood
−
0.353
-0.353
(0)
−
0.341
-0.341
(0)
−
0.262
-0.262
(0)
Token-level entropy
−
0.364
-0.364
(0)
−
0.341
-0.341
(0)
−
0.262
-0.262
(0)
Results and Analysis.
Figure
6
visualizes the discriminative ability of each metric via AUC scores.
It shows that behavioral metrics (crash rate and code semantic entropy) substantially outperform in distinguishing solvable from unsolvable problems than internal and text-based metrics.
While internal metrics barely surpass random guessing (near 0.5) on CodeLlama, code semantic entropy consistently achieves high AUC scores, reaching up to 0.804.
We notice that the crash rate shows the highest AUC on CodeLlama, which can be attributed to its tendency to generate code with syntactic errors or runtime crashes, providing a simple but effective failure signal.
However, its effectiveness drops significantly on stronger models like Qwen, which rarely fail syntactically.
Similarly, naive semantic entropy performs only moderately, as its underlying text-embedding models struggle to capture the functional impact of subtle but critical symbolic changes (e.g.,
range(n)
vs.
range(n+1)
), limiting its sensitivity to functional equivalence.
This distinction highlights the fundamental difference between these signals. While crash rate detects only surface-level errors and naive semantic entropy operates in a shallow textual space, code semantic entropy quantifies semantic disagreement in the functional behavior space, thereby capturing epistemic uncertainty more faithfully.
By focusing on execution semantics rather than token-level patterns or simple crashes, it remains robust and highly discriminative across all models.
Furthermore, its model-agnostic design makes it applicable even to black-box or API-only models where internal states are inaccessible.
Table
2
reinforces these findings through correlation analysis.
Code semantic entropy shows the strongest and most consistent negative correlation with pass rates across all models (e.g.,
−
0.717
-0.717
Pearson on Qwen).
In contrast, the internal metrics show weak or even
undesirable positive correlation
on CodeLlama, confirming their unreliability for lower-capacity models.
Naive semantic entropy demonstrates moderate negative correlation, reflecting its limited sensitivity to functional equivalence.
All reported coefficients are statistically significant, with extremely small
p
p
-values (e.g.,
p
<
10
−
300
p<10^{-300}
) due to the large evaluation set (nearly 20,000 data points).
Finally, Table
3
reports the end-to-end impact of curriculum curated by each metric.
The models trained with the code semantic entropy–based curriculum achieve the best downstream results across all backbones.
This confirms that our metric’s superior ability to identify truly learnable problems by measuring uncertainty in the functional behavior space translates directly into the most tangible and effective self-improvement.
Table 3.
End-to-end average performance comparison of curricula curated by different uncertainty metrics.
End-to-end average performance comparison of curricula curated by different uncertainty metrics.
Metrics
CodeLlama
DeepSeek-Coder
Qwen2.5-Coder
Neg. log-likelihood
31.95
60.62
72.85
Token-level entropy
32.18
60.44
72.90
Naive sem. entropy
33.65
61.75
72.20
Code sem. entropy
35.66
63.26
74.39
Answer to RQ2
Code semantic entropy is a substantially more reliable and robust metric for a model’s competence and uncertainty on a given problem.
By measuring this uncertainty in the functional behavior space, it provides a more accurate signal for curating a curriculum of appropriately challenging problems, forming the cornerstone of our approach’s success.
Table 4.
Ablation results. RD denotes relative degradation in performance compared to
ConSelf
.
Ablation results.
Backbone LLMs
Methods
HumanEval
MBPP
EvalPlus
LiveCodeBench
Avg.
RD
HE+
MBPP+
Easy
Medium
Hard
Overall
CodeLlama-7B
ConSelf
36.59
55.03
31.50
46.74
24.85
1.31
0.27
8.45
35.66
-
w/o CW
35.77
53.70
30.49
45.41
24.25
1.51
0.27
8.37
34.75
−
2.55
%
-2.55\%
w/o CC
34.15
53.44
28.66
45.24
23.30
1.21
0.27
7.95
33.89
−
4.96
%
-4.96\%
DeepSeek-Coder-6.7B
ConSelf
78.46
76.98
72.15
68.78
48.75
10.88
0.90
19.92
63.26
-
w/o CW
77.44
75.40
71.95
67.20
46.95
10.47
0.81
19.17
62.23
−
1.63
%
-1.63\%
w/o CC
75.61
74.07
70.93
66.40
45.52
9.06
0.63
18.11
61.02
−
3.54
%
-3.54\%
Qwen2.5-Coder-7B
ConSelf
91.46
86.51
86.59
74.60
71.33
23.26
3.33
32.77
74.39
-
w/o CW
90.85
85.71
86.38
72.75
70.61
22.66
3.06
32.20
73.58
−
1.09
%
-1.09\%
w/o CC
89.63
83.07
84.76
71.96
70.25
22.36
2.70
31.82
72.25
−
2.88
%
-2.88\%
3.4.
Ablation Study
To answer RQ3, we conduct an ablation study to disentangle the contributions of two core components of
ConSelf
: (1) curriculum curation via code semantic entropy filtering and (2) Con-DPO.
By systematically removing them, we aim to quantify their individual impact on the final performance.
For each backbone LLM, we evaluate two degraded variants:
•
w/o CW (without consensus weighting)
: This variant uses our entropy-based curriculum but replaces the Con-DPO objective with standard DPO. It allows us to isolate the impact of our consensus-aware weighting scheme.
•
w/o CC (without curriculum curation)
: This variant applies our full Con-DPO objective but trains on the entire unfiltered dataset. It is designed to measure the contribution of the curriculum curation component.
Results and Analysis.
The results in Table
4
reveal the distinct and synergistic contributions of the two core components.
The most significant finding from our ablation study is the paramount importance of curriculum curation. For every LLM tested, the
w/o CC
variant suffers the largest performance degradation.
On DeepSeek-Coder, removing curriculum curation leads to a substantial 3.54% relative degradation, and on CodeLlama, the drop is even more stark at 4.96%.
This degradation strongly supports our central hypothesis: strategically filtering out high-entropy, noisy problems is more crucial than the choice of the learning algorithm itself in this unsupervised setting.
Without this filtering, even a more robust learning objective like Con-DPO struggles to overcome the harm caused by training on a massive but low-quality dataset.
While curriculum curation provides the foundational improvement, the Con-DPO offers a further, significant refinement. The
w/o CW
variant, which uses the standard DPO objective, consistently underperforms the full
ConSelf
approach across all LLMs.
On CodeLlama, removing the consensus weighting results in a 2.55% relative degradation. This shows that even within a high-quality, filtered curriculum, there is still residual noise in the self-generated preference labels.
The consensus weighting mechanism effectively mitigates this by adaptively down-weighting less reliable preference pairs, leading to a more stable and effective training process.
The full
ConSelf
, which combines both components, achieves the highest performance.
The performance degradation observed when either component is removed confirms that curriculum curation and consensus-driven learning are complementary.
The filtering mechanism first provides a high-quality, low-noise starting point, and the Con-DPO objective then refines the learning process by intelligently handling the residual noise within that curated set.
Answer to RQ3
Both core components of
ConSelf
are crucial for its success. Curriculum curation provides the most significant performance impact by creating a high-signal, data-efficient training environment. Consensus weighting offers a further refinement by robustly handling the residual noise in self-generated preferences.
3.5.
Impact of Filtering Threshold
As defined in Section
2.3
, problems are selected if their normalized code semantic entropy
H
norm
​
(
p
)
H_{\text{norm}}(p)
falls within
(
0
,
τ
)
(0,\tau)
.
We conduct a parameter sweep on the DeepSeek-Coder-6.7B model, varying
τ
\tau
from 1.0 (most lenient) to 0.1 (most strict).
For each value of
τ
\tau
, we evaluate the final model’s average pass@1 performance across four benchmarks.
To better highlight the relative benefit of filtering, we report the percentage improvement over the base model.
Importantly, this sweep is performed purely to illustrate the effect of different threshold values; the main results in Table
1
use
τ
\tau
selected on an independent validation set.
Results and Analysis.
Our analysis shows how the filtering threshold
τ
\tau
directly governs the model’s final performance. As shown in Figure
7
(a), the relationship is not monotonic.
When the filter is very lenient (
τ
=
1.0
\tau=1.0
), including nearly all problems, the performance gain is minimal. As the filter becomes stricter, the model’s performance steadily rises, peaking at an optimal value of
0.3
0.3
.
This initial improvement confirms that filtering out high-entropy noisy problems is indeed beneficial.
However, the performance starts to decline when the filter becomes even stricter (
τ
<
0.3
\tau<0.3
).
To answer this, we analyze the composition of the training data in Figure
7
(b).
We define the “golden rate” as the percentage of preference pairs
(
y
w
,
y
l
)
(y_{w},y_{l})
in the training data where the winner
y
w
y_{w}
is functionally correct and the loser
y
l
y_{l}
is wrong according to the ground-truth test oracles.
Note that the oracle information is used for analysis only.
The golden rate steadily increases as the filter tightens, rising from approximately 15% to over 60%.
This confirms that our filtering mechanism is highly effective at improving the training data quality.
However, the total count of golden pairs decreases.
The reduction in quantity limits the diversity of the curriculum, as fewer problems remain for the model to learn from.
Figure 7.
Impact of the filtering threshold
τ
\tau
on DeepSeek-Coder-6.7B training data. (a) Number of training samples and average performance improvement over the base model. (b) Golden count and golden rate in the filtered dataset.
Impact of the filtering threshold $\tau$ on training data. Lower thresholds reduce sample quantity but improve data quality, with optimal performance at $\tau=0.3$.
This reveals a fundamental trade-off. The initial performance improvement (from
τ
=
1.0
\tau=1.0
to 0.3) is driven by the removal of noisy data, which improves signal quality.
The subsequent decline (from
τ
=
0.3
\tau=0.3
to 0.1) can be attributed to the diminishing quantity and diversity of the training data. Although this smaller dataset is of higher quality, it becomes insufficient for the model to learn generalizable patterns.
The peak performance at
0.3
0.3
thus represents the optimal balance point.
Ultimately, this analysis shows that the effectiveness of
ConSelf
stems not from an arbitrary heuristic, but from an interpretable mechanism.
The optimal threshold emerges from this controllable trade-off, validating our strategy of targeting problems of moderate difficulty where both learning signal and problem diversity are adequate.
Answer to RQ4
The filtering threshold
τ
\tau
governs a clear trade-off between the diversity and quality of the training data. The model’s performance follows a concave curve as
τ
\tau
varies, peaking at a balance point.
This demonstrates that our curriculum curation mechanism is not arbitrary but is governed by an interpretable principle.
4.
Threats to Validity
First, code semantic entropy requires executing multiple candidate programs to estimate functional disagreement, introducing additional computational cost.
However, execution offers precise semantic feedback and provides a robust, model-agnostic uncertainty signal.
For proprietary or API-based models without access to internal logits, such behavioral metrics remain among the few viable options for uncertainty estimation.
Second, the effectiveness of curriculum filtering depends on the dataset’s difficulty and the model’s capability.
Our method shows limited gains on problems far beyond model capacity, indicating that external supervision (e.g., teacher models or test oracles) remains necessary.
Nevertheless, our findings offer valuable insights into model uncertainty and problem difficulty, informing data curation and evaluation practices.
Third, like other self-improving methods, our approach faces potential reward-hacking risks, where models might overfit to proxy signals such as self-consistency, generating coherent but incorrect outputs.
We mitigate this by grounding the signal in observable functional behavior via execution traces rather than internal states.
While the risk cannot be fully removed without external supervision, our design greatly reduces its impact in practice. We leave the exploration of such failure modes for future work.
5.
Related Work
Fine-tuning on large-scale datasets is a primary approach for enhancing the code generation capabilities of LLMs. Since manually annotated data is scarce
(Muennighoff
et al.
,
2024
)
, research has focused on automated data synthesis using powerful “teacher” models, with strategies ranging from evolutionary prompting
(Luo
et al.
,
2024
; Wang
et al.
,
2024
)
to mining open-source codebases
(Wei
et al.
,
2024b
; Yu
et al.
,
2024
)
. To ensure data quality, various techniques filter samples using compiler feedback or consistency checks
(Xu
et al.
,
2025
; Ahmad
et al.
,
2025
; Wei
et al.
,
2024a
)
. Beyond SFT, preference-based optimization has become popular, training models on preference datasets based on functional correctness
(Zhang
et al.
,
2024a
,
2025a
; Gee
et al.
,
2025
; Dou
et al.
,
2024
)
or via advanced learning algorithms
(Le
et al.
,
2022
; Shojaee
et al.
,
2023
; Liu
et al.
,
2023a
; Zhang
et al.
,
2025b
)
. However, both SFT and preference-based methods share a fundamental dependency on either a superior teacher model for reference solutions or reliable test oracles for correctness labels. Our work diverges by operating in a setting where neither of these expensive forms of external supervision is available.
The reliance on test oracles is hampered by the long-standing “test oracle problem”
(Barr
et al.
,
2015
)
in software testing.
Traditional approaches like fuzzing
(Pacheco and Ernst,
2007
)
rely on implicit oracles such as exceptions from unintended behavior. Search-based tools like EvoSuite
(Fraser and Arcuri,
2011
)
are limited to generating regression oracles and cannot detect pre-existing bugs.
While LLMs have advanced the field, recent studies consistently show that LLMs also struggle significantly in generating correct oracles.
For instance, LLM-generated tests often suffer from compilation and execution errors
(Yuan
et al.
,
2024
)
and exhibit extremely low accuracy on complex problems
(Liu
et al.
,
2025
)
.
TestEval
(Wang
et al.
,
2025b
)
shows that while LLMs excel at producing syntactically valid and executable test inputs, the correctness of test oracles themselves remains very low. Efforts to mitigate this reintroduce significant costs
(Dinella
et al.
,
2022
; Prasad
et al.
,
2025
; Hossain and Dwyer,
2025
; Ma
et al.
,
2025
; Li and Yuan,
2024
)
. In stark contrast, test input synthesis is a far more tractable problem
(Fraser and Arcuri,
2011
; Lukasczyk and Fraser,
2022
; Li
et al.
,
2023
; Liu
et al.
,
2023b
; Jiang
et al.
,
2024b
; He
et al.
,
2025
; Liu
et al.
,
2025
)
. This well-documented gap motivates our work, which assumes access to test inputs but not test oracles.
Uncertainty estimation offers another lens for assessing LLM reliability. Methods include those based on model’s internal states (e.g., token-level entropy and negative log-likelihood
(Geng
et al.
,
2024
)
) and those based on linguistic invariances
(Kuhn
et al.
,
2023
)
.
Prior study
(Huang
et al.
,
2025
)
shows that analyzing output diversity is a more robust method for uncertainty estimation in code generation, aligning with our approach of evaluating a diverse candidate pool.
Our large-scale experiments further confirm that existing metrics struggle to detect subtle semantic errors, consistent with these observations.
Crucially, we address this gap by grounding uncertainty in observable functional behavior rather than linguistic representation.
6.
Conclusion
We presented
ConSelf
, a self-improvement approach for code generation that operates without costly supervision from teacher models and test oracles.
We argued that effective self-learning requires a dual strategy of first curating a learnable curriculum (what to learn) and then robustly learning from it (how to learn).
We introduced code semantic entropy, a behavior-based metric that reliably gauges a model’s epistemic uncertainty, and consensus-driven DPO, a preference learning objective that adaptively weights self-generated training signals.
Our experiments demonstrated that
ConSelf
synergistically combines these components to achieve consistent and data-efficient performance gains across multiple models.
Acknowledgements.
This work was supported in part by the National Natural Science Foundation of China (No. 62272219), the Cooperation Fund of Huawei Cooperation Project (No. TC20230202021-2024-12), and the Postgraduate Research & Practice Innovation Program of Jiangsu Province (No. KYCX25_0314).
References
W. U. Ahmad, A. Ficek, M. Samadi, J. Huang, V. Noroozi, S. Majumdar, and B. Ginsburg (2025)
OpenCodeInstruct: a large-scale instruction tuning dataset for code llms
.
CoRR
2504.04030
,
pp. 1–22
.
Cited by:
§1
,
§5
.
J. Austin, A. Odena, M. I. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. J. Cai, M. Terry, Q. V. Le, and C. Sutton (2021)
Program synthesis with large language models
.
CoRR
2108.07732
,
pp. 1–34
.
Cited by:
§3.1
.
E. T. Barr, M. Harman, P. McMinn, M. Shahbaz, and S. Yoo (2015)
The oracle problem in software testing: a survey
.
IEEE Trans. Softw. Eng.
41
,
pp. 507–525
.
Cited by:
§1
,
§5
.
B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J. Lou, and W. Chen (2023)
CodeT: code generation with generated tests
.
In
ICLR
,
Kigali, Rwanda
.
Cited by:
§1
.
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba (2021)
Evaluating large language models trained on code
.
CoRR
2107.03374
,
pp. 1–35
.
Cited by:
§3.1
.
X. Chen, Z. Tao, K. Zhang, C. Zhou, W. Gu, Y. He, M. Zhang, X. Cai, H. Zhao, and Z. Jin (2025)
Revisit self-debugging with self-generated tests for code generation
.
CoRR
2501.12793
,
pp. 1–20
.
Cited by:
§1
.
X. Chen, M. Lin, N. Schärli, and D. Zhou (2024)
Teaching large language models to self-debug
.
In
ICLR
,
Vienna, Austria
.
Cited by:
§3.1
.
E. Dinella, G. Ryan, T. Mytkowicz, and S. K. Lahiri (2022)
TOGA: a neural method for test oracle generation
.
In
ICSE
,
Pittsburgh, PA, USA
,
pp. 2130–2141
.
Cited by:
§1
,
§5
.
S. Dou, Y. Liu, H. Jia, E. Zhou, L. Xiong, J. Shan, C. Huang, X. Wang, X. Fan, Z. Xi, Y. Zhou, T. Ji, R. Zheng, Q. Zhang, T. Gui, and X. Huang (2024)
StepCoder: improving code generation with reinforcement learning from compiler feedback
.
In
ACL
,
Bangkok, Thailand
,
pp. 4571–4585
.
Cited by:
§5
.
G. Fraser and A. Arcuri (2011)
EvoSuite: automatic test suite generation for object-oriented software
.
In
ESEC/FSE
,
Szeged, Hungary
,
pp. 416–419
.
Cited by:
§1
,
§5
.
L. Gee, M. Gritta, G. Lampouras, and I. Iacobacci (2025)
Code-optimise: self-generated preference data for correctness and efficiency
.
In
Findings of NAACL
,
Albuquerque, NM, USA
,
pp. 79–94
.
Cited by:
§1
,
§2.4
,
§5
.
J. Geng, F. Cai, Y. Wang, H. Koeppl, P. Nakov, and I. Gurevych (2024)
A survey of confidence estimation and calibration in large language models
.
In
NAACL
,
Mexico City, Mexico
,
pp. 6577–6595
.
Cited by:
§1
,
§2.3
,
§5
.
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. K. Li, F. Luo, Y. Xiong, and W. Liang (2024)
DeepSeek-coder: when the large language model meets programming - the rise of code intelligence
.
CoRR
2401.14196
,
pp. 1–23
.
Cited by:
§1
,
§3.1
.
Z. He, Y. M. Choi, K. Zhang, J. Ji, J. Zhou, D. Xu, I. Bercovich, A. Zhang, and L. Li (2025)
HardTests: synthesizing high-quality test cases for llm coding
.
CoRR
2505.24098
,
pp. 1–37
.
Cited by:
§5
.
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song, and J. Steinhardt (2021)
Measuring coding challenge competence with apps
.
In
NeurIPS
,
Virtual
.
Cited by:
§3.1
.
S. B. Hossain and M. B. Dwyer (2025)
TOGLL: correct and strong test oracle generation with llms
.
In
ICSE
,
Los Alamitos, CA, USA
,
pp. 1475–1487
.
Cited by:
§1
,
§5
.
E. J. Hu, yelong shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen (2022)
LoRA: low-rank adaptation of large language models
.
In
ICLR
,
Virtual
.
Cited by:
§3.1
.
J. Huang, S. Gu, L. Hou, Y. Wu, X. Wang, H. Yu, and J. Han (2023)
Large language models can self-improve
.
In
EMNLP
,
Singapore
,
pp. 1051–1068
.
Cited by:
§1
,
§2.4
,
3rd item
.
Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma (2025)
Look before you leap: an exploratory study of uncertainty analysis for large language models
.
TSE
51
(
2
),
pp. 413–429
.
Cited by:
§5
.
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu, K. Dang, Y. Fan, Y. Zhang, A. Yang, R. Men, F. Huang, B. Zheng, Y. Miao, S. Quan, Y. Feng, X. Ren, X. Ren, J. Zhou, and J. Lin (2024)
Qwen2.5-coder technical report
.
CoRR
2409.12186
,
pp. 1–32
.
Cited by:
§1
,
§3.1
.
N. Jain, K. Han, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica (2025)
LiveCodeBench: holistic and contamination free evaluation of large language models for code
.
In
ICLR
,
Singapore
.
Cited by:
§3.1
.
X. Jiang, Y. Dong, L. Wang, Z. Fang, Q. Shang, G. Li, Z. Jin, and W. Jiao (2024a)
Self-planning code generation with large language models
.
ACM Trans. Softw. Eng. Methodol.
33
.
Cited by:
§3.1
.
Z. Jiang, M. Wen, J. Cao, X. Shi, and H. Jin (2024b)
Towards understanding the effectiveness of large language models on directed test input generation
.
In
ASE
,
Sacramento, CA, USA
,
pp. 1408–1420
.
Cited by:
§1
,
§5
.
F. Jiao, G. Guo, X. Zhang, N. F. Chen, S. Joty, and F. Wei (2025)
Preference optimization for reasoning with pseudo feedback
.
In
ICLR
,
Singapore
.
Cited by:
§1
,
§1
,
§2.4
,
2nd item
.
L. Kuhn, Y. Gal, and S. Farquhar (2023)
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
ICLR
,
Kigali, Rwanda
.
Cited by:
§2.3
,
§3.3
,
§5
.
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. Gonzalez, H. Zhang, and I. Stoica (2023)
Efficient memory management for large language model serving with pagedattention
.
In
SOSP
,
Koblenz, Germany
,
pp. 611–626
.
Cited by:
§3.1
.
H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C.H. Hoi (2022)
CodeRL: mastering code generation through pretrained models and deep reinforcement learning
.
In
NeurIPS
,
New Orleans, LA, USA
,
pp. 21314–21328
.
Cited by:
§5
.
J. Li, G. Li, Y. Li, and Z. Jin (2025)
Structured chain-of-thought prompting for code generation
.
ACM Trans. Softw. Eng. Methodol.
34
.
Cited by:
§3.1
.
K. Li and Y. Yuan (2024)
Large language models as test case generators: performance evaluation and enhancement
.
CoRR
2404.13340
,
pp. 1–20
.
Cited by:
§1
,
§5
.
R. Li, J. Fu, B. Zhang, T. Huang, Z. Sun, C. Lyu, G. Liu, Z. Jin, and G. Li (2023)
TACO: topics in algorithmic code generation dataset
.
CoRR
2312.14852
,
pp. 1–10
.
Cited by:
§1
,
§3.1
,
§5
.
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy, C. de Masson d’Autume, I. Babuschkin, X. Chen, P. Huang, J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S. Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals (2022)
Competition-level code generation with alphacode
.
Science
378
,
pp. 1092–1097
.
Cited by:
§3.1
.
J. Liu, Y. Zhu, K. Xiao, Q. FU, X. Han, Y. Wei, and D. Ye (2023a)
RLTF: reinforcement learning from unit test feedback
.
Trans. Mach. Learn. Res.
11
.
Cited by:
§5
.
J. Liu, C. S. Xia, Y. Wang, and L. Zhang (2023b)
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
In
NeurIPS
,
New Orleans, LA, USA
,
pp. 21558–21572
.
Cited by:
§1
,
§3.1
,
§5
.
K. Liu, Y. Liu, Z. Chen, J. M. Zhang, Y. Han, Y. Ma, G. Li, and G. Huang (2025)
LLM-powered test case generation for detecting bugs in plausible programs
.
In
ACL
,
Vienna, Austria
.
Cited by:
§1
,
§5
.
S. Lukasczyk and G. Fraser (2022)
Pynguin: automated unit test generation for python
.
In
ICSE
,
Pittsburgh, PA, USA
,
pp. 168–172
.
Cited by:
§1
,
§5
.
Z. Luo, C. Xu, P. Zhao, Q. Sun, X. Geng, W. Hu, C. Tao, J. Ma, Q. Lin, and D. Jiang (2024)
WizardCoder: empowering code large language models with evol-instruct
.
In
ICLR
,
Vienna, Austria
.
Cited by:
§1
,
§5
.
Z. Ma, X. Zhang, J. Zhang, J. Yu, S. Luo, and J. Tang (2025)
Dynamic scaling of unit tests for code reward modeling
.
In
ACL
,
Vienna, Austria
.
Cited by:
§1
,
§5
.
N. Muennighoff, Q. Liu, A. R. Zebaze, Q. Zheng, B. Hui, T. Y. Zhuo, S. Singh, X. Tang, L. V. Werra, and S. Longpre (2024)
OctoPack: instruction tuning code large language models
.
In
ICLR
,
Vienna, Austria
.
Cited by:
§5
.
OpenAI (2023)
GPT-4 technical report
.
CoRR
2303.08774
,
pp. 1–100
.
Cited by:
§1
.
OpenAI (2024)
GPT-4o system card
.
CoRR
2410.21276
,
pp. 1–33
.
Cited by:
§1
.
C. Pacheco and M. D. Ernst (2007)
Randoop: feedback-directed random testing for java
.
In
OOPSLA
,
Montréal, QC, Canada
,
pp. 815–816
.
Cited by:
§5
.
A. Prasad, E. Stengel-Eskin, J. C. Chen, Z. Khan, and M. Bansal (2025)
Learning to generate unit tests for automated debugging
.
CoRR
2502.01619
,
pp. 1–19
.
Cited by:
§1
,
§5
.
R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn (2023)
Direct preference optimization: your language model is secretly a reward model
.
In
NeurIPS
,
Vol.
36
,
New Orleans, LA, USA
,
pp. 53728–53741
.
Cited by:
§1
,
§2.4
.
B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez, J. Rapin, A. Kozhevnikov, I. Evtimov, J. Bitton, M. Bhatt, C. C. Ferrer, A. Grattafiori, W. Xiong, A. Défossez, J. Copet, F. Azhar, H. Touvron, L. Martin, N. Usunier, T. Scialom, and G. Synnaeve (2023)
Code llama: open foundation models for code
.
CoRR
2308.12950
,
pp. 1–48
.
Cited by:
§3.1
.
P. Shojaee, A. Jain, S. Tipirneni, and C. K. Reddy (2023)
Execution-based code generation using deep reinforcement learning
.
Trans. Mach. Learn. Res.
2023
,
pp. 1–26
.
Cited by:
§1
,
§5
.
E. Z. Wang, F. Cassano, C. Wu, Y. Bai, W. Song, V. Nath, Z. Han, S. M. Hendryx, S. Yue, and H. Zhang (2025a)
Planning in natural language improves LLM search for code generation
.
In
ICLR
,
Singapore
.
Cited by:
§2.2
.
W. Wang, C. Yang, Z. Wang, Y. Huang, Z. Chu, D. Song, L. Zhang, A. R. Chen, and L. Ma (2025b)
TestEval: benchmarking large language models for test case generation
.
In
Findings of NAACL
,
Albuquerque, NM, USA
,
pp. 3547–3562
.
Cited by:
§1
,
§5
.
Y. Wang, K. He, G. Dong, P. Wang, W. Zeng, M. Diao, W. Xu, J. Wang, M. Zhang, and X. Cai (2024)
DolphCoder: echo-locating code large language models with diverse and multi-objective instruction tuning
.
In
ACL
,
Bangkok, Thailand
,
pp. 4706–4721
.
Cited by:
§5
.
Y. Wei, F. Cassano, J. Liu, Y. Ding, N. Jain, Z. Mueller, H. de Vries, L. von Werra, A. Guha, and L. Zhang (2024a)
SelfCodeAlign: self-alignment for code generation
.
In
NeurIPS
,
Vancouver, BC, Canada
,
pp. 62787–62874
.
Cited by:
§1
,
§5
.
Y. Wei, Z. Wang, J. Liu, Y. Ding, and L. Zhang (2024b)
Magicoder: empowering code generation with oss-instruct
.
In
ICML
,
Vienna, Austria
,
pp. 52632–52657
.
Cited by:
§1
,
§5
.
Z. Xu, Y. Liu, Y. Yin, M. Zhou, and R. Poovendran (2025)
KodCode: a diverse, challenging, and verifiable synthetic dataset for coding
.
In
Findings of ACL
,
Vienna, Austria
.
Cited by:
§1
,
§5
.
Z. Yu, X. Zhang, N. Shang, Y. Huang, C. Xu, Y. Zhao, W. Hu, and Q. Yin (2024)
WaveCoder: widespread and versatile enhancement for code large language models by instruction tuning
.
In
ACL
,
Bangkok, Thailand
,
pp. 5140–5153
.
Cited by:
§5
.
Z. Yuan, M. Liu, S. Ding, K. Wang, Y. Chen, X. Peng, and Y. Lou (2024)
Evaluating and improving chatgpt for unit test generation
.
Proc. ACM Softw. Eng.
1
(
FSE
),
pp. 1703–1726
.
Cited by:
§5
.
D. Zhang, S. Diao, X. Zou, and H. Peng (2024a)
PLUM: improving code lms with execution-guided on-policy preference learning driven by synthetic test cases
.
CoRR
2406.06887
,
pp. 1–24
.
Cited by:
§1
,
§2.4
,
§5
.
H. Zhang, W. Cheng, Y. Wu, and W. Hu (2024b)
A pair programming framework for code generation via multi-plan exploration and feedback-driven refinement
.
In
ASE
,
Sacramento, CA, USA
,
pp. 1319–1331
.
Cited by:
§3.1
.
K. Zhang, G. Li, Y. Dong, J. Xu, J. Zhang, J. Su, Y. Liu, and Z. Jin (2025a)
CodeDPO: aligning code models with self generated and verified source code
.
In
ACL
,
Vienna, Austria
.
Cited by:
§1
,
§2.4
,
§5
.
K. Zhang, G. Li, J. Li, Y. Dong, J. Li, and Z. Jin (2025b)
Focused-dpo: enhancing code generation through focused preference optimization on error-prone points
.
In
Findings of ACL
,
Vienna, Austria
.
Cited by:
§1
,
§5
.