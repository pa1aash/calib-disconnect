---
title: 'UCoder: Unsupervised Code Generation by Internal Probing of Large Language
  Models'
id: ucoder-unsupervised-code-generation-by-internal-probing-of-large-language-models
tags:
- code-llm-calibration-aaai27-eabf3f
- internal-probing
- self-consistency
- unsupervised-training
created: '2026-07-17T18:31:06.175955Z'
updated: '2026-07-17T18:33:21.567531Z'
source: https://arxiv.org/html/2512.17385
source_domain: arxiv.org
fetched_at: '2026-07-17T18:31:06.175219Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'UCoder/IPC (Wu et al., Beihang+Huawei, Dec 2025): unsupervised post-training
  framework using LLM "internal probing" to self-generate problems, tests, and candidate
  solutions with NO external labeled data. Despite the "internal probing" name, this
  is NOT hidden-state activation probing -- it is a 6-stage self-bootstrap pipeline
  where the model itself: (1-3) generates problems with specs, (4) generates ~100
  test cases/problem, (5) densely samples n=128 candidate solutions and clusters them
  by execution signature (behaviorally-identical outputs on the self-generated tests),
  (6) consolidates the largest "consensus cluster" as SFT training data. Correctness
  proxy = execution-signature clustering (majority-vote over 128 samples), i.e., an
  EXPENSIVE n-sample self-consistency signal, not a cheap single-pass probe.


  Theorem 2.4 (Consensus Convergence) gives a formal guarantee: if candidates are
  independently sampled with ≥k correct w.p. ≥1-δ, and any two incorrect implementations
  agree on a single test with probability ≤p, then given test-set size |T| ≥ log(n/k)/(-log
  p), the largest consensus cluster is entirely correct with probability ≥ 1-δ-n²p^|T|.
  Quality is scored by three metrics: execution success rate e(r), consensus/cluster
  size s(r), and code fluency f(r) = exp(-mean log-prob) i.e. perplexity. Notably
  perplexity IS used as a lightweight (near-free, log-prob-derived) correctness proxy
  for intra-cluster tie-breaking: over 9,700 sampled candidates, solutions with execution
  success >80% cluster below perplexity 1.05, with sharp degradation above that threshold
  -- a genuine but weak single-pass log-prob signal, secondary to the expensive n=128
  sampling/clustering step.


  Results: UCoder-7B/14B/32B (built on Qwen2.5-Coder self-training with zero external
  data) reach performance competitive with the supervised Qwen2.5-Coder-Instruct baselines
  across HumanEval(+), MBPP(+), BigCodeBench-Complete/Instruct, LiveCodeBench, FullStackBench
  -- e.g. UCoder-7B: HumanEval 83.5, HumanEval+ 76.8, MBPP 85.2, FullStackBench 51.27,
  vs supervised Qwen2.5-Coder-7B-Instruct: HumanEval 88.4, MBPP 83.5, FullStackBench
  47.95 (UCoder-7B actually beats the supervised instruct model on BCB-Complete, BCB-Instruct,
  and FullStackBench). Ablation shows consensus-clustering selection beats Random,
  dominant-cluster-only, Low-PPL-only, and Success-Rate-threshold-only baselines,
  with the margin widening at larger scale (Random gap grows from 6.7 to 13.9 points
  7B->32B on FullStackBench).


  Relevance to the internal->expressed gap: this paper is a data-curation/self-training
  method, not a calibration or uncertainty-communication paper -- it does not report
  AUROC of any signal against ground-truth correctness on a fixed benchmark, so it
  does NOT directly answer whether a cheap probe matches n-sample AUROC. Its main
  contribution to the survey is (a) further evidence that dense self-consistency sampling
  (n=128) is a reliable correctness signal usable for training, reinforcing the "internal
  signal exists via sampling" thesis, and (b) perplexity/fluency as a cheap complementary
  proxy, correlated with but weaker than full execution-based consensus. Limitations
  acknowledged by authors: consensus selection needs executable test cases (fails
  for tasks with no clean oracle); n=128 sampling remains computationally expensive;
  diminishing returns/overfitting after several self-training iterations; Python-only.'
---

*Suggested by [[251217385-ucoder-unsupervised-code-generation-by-internal-probing-of-large-langu]] — full HTML text needed for exact probe accuracy numbers*

UCoder: Unsupervised Code Generation by Internal Probing of Large Language Models
UCoder: Unsupervised Code Generation by Internal
Probing of Large Language Models
Jiajun Wu
1
,
Jian Yang
1
,
Wei Zhang
1
,
Lin Jing
1
,
Yuqing Ma
2
,
Ensheng Shi
2
,
Yuchi Ma
2
,
Zhoujun Li
2
,
Xianglong Liu
1
1
Beihang University;
2
Huawei;
{wuyuverse,jiayang}@buaa.edu.cn
Corresponding Author.
Abstract
Large language models (LLMs) have demonstrated remarkable capabilities in code generation tasks. However, their effectiveness heavily relies on supervised training with extensive labeled (e.g., question-answering pairs) or unlabeled datasets (e.g., code snippets), which are often expensive and difficult to obtain at scale. To address this limitation, this paper introduces a method
IPC
, an unsupervised framework that leverages
I
nternal
P
robing of LLMs for
C
ode generation without any external corpus, even unlabeled code snippets. We introduce the problem space probing, test understanding probing, solution space probing, and knowledge consolidation and reinforcement to probe the internal knowledge and confidence patterns existing in LLMs. Further, IPC identifies reliable code candidates through self-consistency mechanisms and representation-based quality estimation to train UCoder (coder with unsupervised learning). We validate the proposed approach across multiple code benchmarks, demonstrating that unsupervised methods can achieve competitive performance compared to supervised approaches while significantly reducing the dependency on labeled data and computational resources. Analytic experiments reveal that internal model states contain rich signals about code quality and correctness, and that properly harnessing these signals enables effective unsupervised learning for code generation tasks, opening new directions for training code LLMs in resource-constrained scenarios.
1
Introduction
Large language models (LLMs) have demonstrated strong capabilities in code generation, producing functional code from natural language descriptions. This progress has attracted substantial interest from both academia and industry due to its practical impact on software development. Closed-source LLMS such as GPT-5
openai2025gpt5codex
and Claude-4.5
claude45
can generate file-level code with high accuracy, while open-source alternatives, including StarCoder
starcoder
;
starcoder2
, DeepSeek-Coder
deepseek_coder
, and QwenCoder
qwen25coder
have emerged as competitive solutions for code intelligence.
Figure 1:
Comparison between supervised and unsupervised paradigms for code generation.
Figure 2:
Overview of the proposed six-stage self-bootstrapping framework for unsupervised code generation.
Most existing approaches for improving code generation rely on supervised instruction tuning, where LLMs are fine-tuned on curated problem-solution pairs annotated by human experts or LLM-based annotated. However, creating high-quality instruction data requires substantial human effort in problem design, implementation, and verification, with costs increasing as model capabilities advance.
The recent
sft_effect1
;
sft_effect2
;
sft_effect3
works emphasize that pre-training brings the knowledge, and post-training is weak at knowledge integration but focuses on knowledge utilization and alignment.
These challenges motivate a fundamental question: Can LLMs autonomously improve their generation capabilities using post-training without any external corpus, relying only on pre-trained knowledge?
In this work, we introduce an unsupervised framework that performs
I
nternal
P
robing of LLMs for
C
ode generation, enabling post-training without external corpora or human-annotated instruction data. Our approach exploits latent programming knowledge in LLMs and uses execution feedback as a scalable, deterministic supervision signal grounded in program semantics. We implement a six-stage self-bootstrapping process that generates diverse programming tasks, synthesizes test suites, samples candidate solutions, and applies execution-driven consensus clustering to identify correct implementations. High-consensus solutions are iteratively consolidated as training data, forming a feedback loop that progressively improves model performance.
Despite using no external data, UCoder achieves comparable performance to the supervised baseline across multiple benchmarks. The primary contributions of this work are:
•
We successfully probe latent programming knowledge in LLMs by forcing models to generate programming problems and their solutions, then identify correct solutions by finding clusters of similar implementations. Then, the self-training method progressively improves the LLM by reinforcing solutions.
•
Based on the self-generated data from the unsupervised framework using internal probing of LLMs (IPC) without any external data, UCoder (7B, 14B, 32B) achieves performance competitive with supervised baselines.
•
We provide empirical analysis showing that self-generated data maintains rich lexical, semantic, and structural diversity, while consensus-based selection improves solution quality and exhibits inverse scaling behavior.
2
Unsupervised Code Generation
2.1
Task Definition
2.1.1
Supervised Code Generation
Supervised code generation is formulated as a sequence-to-sequence learning task. Given a training dataset
𝒟
=
{
(
x
i
,
y
i
)
}
i
=
1
N
\mathcal{D}=\{(x_{i},y_{i}^{)}\}_{i=1}^{N}
, the model parameters are optimized by maximizing log-likelihood:
θ
∗
=
arg
⁡
max
θ
​
∑
i
=
1
N
log
⁡
p
θ
​
(
y
i
|
x
i
)
\theta^{*}=\arg\max_{\theta}\sum_{i=1}^{N}\log p_{\theta}(y_{i}|x_{i})
(1)
where
x
i
∈
𝒳
x_{i}\in\mathcal{X}
denotes a natural language query,
y
i
∈
𝒴
y_{i}\in\mathcal{Y}
represents the corresponding reference implementation, and
p
θ
​
(
y
|
x
)
p_{\theta}(y|x)
is the conditional distribution over code sequences parameterized by
θ
\theta
. We adopt Pass@k
chen2021codex
to evaluate code correctness, which measures the probability that at least one of
k
k
independently sampled solutions passes all test cases.
2.1.2
Unsupervised Code Generation
Unsupervised code generation aims to improve LLM code generation capabilities without human-annotated supervision. Given an initial model
M
0
:
𝒳
→
𝒴
M_{0}:\mathcal{X}\rightarrow\mathcal{Y}
, the objective is to develop a self-improvement algorithm
𝒜
\mathcal{A}
producing an enhanced model
M
∗
=
𝒜
​
(
M
0
)
M^{*}=\mathcal{A}(M_{0})
such that
Pass@
​
k
​
(
M
∗
)
>
Pass@
​
k
​
(
M
0
)
\texttt{Pass@}k(M^{*})>\texttt{Pass@}k(M_{0})
on held-out test sets, without access to paired training data
(
x
,
y
)
∈
𝒳
×
𝒴
(x,y)\in\mathcal{X}\times\mathcal{Y}
. This presents three fundamental challenges: (1)
Problem Space Construction.
Automatically generating diverse programming problems with appropriate difficulty distributions while maintaining semantic clarity; (2)
Unsupervised Correctness Verification.
Assessing functional correctness without reference implementations; (3)
Self-Bootstrapping Signal Construction.
Extracting reliable training signals from noisy candidates while ensuring iterative stability. We address these through an execution-driven consensus mechanism coupled with a self-bootstrapping framework, detailed in the following sections.
2.2
Probing Internal Knowledge in LLMs
LLMs encode extensive programming knowledge through pre-training, yet this knowledge remains implicit and difficult to elicit. We propose a six-stage framework to surface and reinforce these latent capabilities, as shown in
Figure 2
. First, we probe the problem space (Stages 1–3) by prompting the model to generate algorithmic problems with complete specifications, revealing its understanding of programming paradigms and data structures. Representative examples of problem generation, difficulty assessment, and solution skeleton construction are illustrated in
Figure 3
.
We then assess semantic understanding (Stage 4) by generating approximately 100 test cases per problem to identify boundary conditions and edge cases. At the core (Stage 5), we probe the solution space via dense sampling, where execution-driven consensus clustering reveals that correct implementations form tight clusters while incorrect ones are dispersed. We quantify solution quality using execution success rate
e
​
(
r
)
e(r)
, consensus strength
s
​
(
r
)
s(r)
, and code fluency
f
​
(
r
)
f(r)
. Finally (Stage 6), we consolidate high-consensus samples through supervised fine-tuning, reinforcing correct patterns. The process forms a positive feedback loop: at iteration
t
t
, the improved LLM
M
t
M_{t}
produces higher-quality candidates, enabling more reliable selection and further strengthening
M
t
+
1
M_{t+1}
. Our experimental results in
subsection 3.2
validate that pre-trained models already contain the knowledge required to solve target tasks in implicit form.
Figure 3:
Problem space probing proceeds through three stages: problem generation with function signatures and input-output contracts, difficulty rating assessment and categorization, and solution skeleton generation with implementation structure.
2.3
Execution-Driven Consensus Clustering
Our approach exploits that correctness is singular while incorrectness is diverse: correct implementations produce identical outputs, but incorrect ones fail heterogeneously. This clustering structure allows the maximum-consensus cluster to indicate correctness without ground truth, formalized in
Theorem 2.4
and validated in
subsection 4.2
.
2.3.1
Definitions
Consensus clustering has three definitions.
Model
HumanEval
MBPP
BCB-Complete
BCB-Instruct
LiveCode-
FullStack-
HE
HE+
MBPP
MBPP+
Full
Hard
Full
Hard
Bench
Bench
6B+ LLMs
CodeLlama-7B-Instruct
40.9
33.5
39.9
33.6
25.7
4.1
21.9
3.4
7.1
25.40
DS-Coder-6.7B-Instruct
74.4
71.3
74.9
65.6
43.8
15.5
35.5
10.1
15.5
40.16
OpenCoder-8B-Instruct
83.5
78.7
79.1
69.0
50.9
18.9
43.2
18.2
23.2
41.08
Qwen2.5-Coder-7B
61.6
53.0
76.9
62.9
45.8
16.2
-
-
-
-
Qwen2.5-Coder-7B-Instruct
88.4
84.1
83.5
71.7
48.8
20.3
41.0
18.2
18.2
47.95
UCoder-7B
83.5
76.8
85.2
72.2
52.0
22.3
41.1
15.5
22.9
51.27
13B+ LLMs
CodeLlama-13B-Instruct
40.2
32.3
60.3
51.1
31.7
6.8
28.5
9.5
6.1
27.00
Starcoder2-15B-Instruct-v0.1
67.7
60.4
78.0
65.1
45.1
14.9
37.2
11.5
12.1
42.68
DS-Coder-V2-Lite-Instruct
81.1
75.6
82.8
70.4
47.6
18.2
36.8
16.2
24.3
-
Qwen2.5-Coder-14B
64.0
57.9
81.0
66.7
51.8
22.3
-
-
-
-
Qwen2.5-Coder-14B-Instruct
89.6
87.2
86.2
72.8
56.7
29.7
48.4
22.2
23.4
55.28
UCoder-14B
87.8
81.1
86.5
74.3
53.9
24.3
40.9
16.2
20.6
52.52
32B+ LLMs
CodeLlama-34B-Instruct
48.2
40.2
61.1
50.5
35.6
10.8
29.0
8.8
8.4
27.56
DS-Coder-33B-Instruct
81.1
75.0
80.4
70.1
51.1
20.9
42.0
17.6
21.3
48.19
DS-Coder-V2-Instruct
85.4
82.3
89.4
75.1
59.7
29.7
48.2
24.3
27.9
56.37
Qwen2.5-Coder-32B
65.9
60.4
83.0
68.2
53.6
26.4
-
-
-
-
Qwen2.5-Coder-32B-Instruct
92.7
87.2
90.2
75.1
58.0
33.8
49.6
27.0
31.4
56.88
UCoder-32B
89.0
82.9
89.7
75.7
55.4
27.7
45.7
17.6
21.4
53.35
Closed-APIs
GPT-4o-2024-08-06
92.1
86.0
86.8
72.5
-
36.5
50.1
25.0
34.6
58.89
Claude-3.5-Sonnet-20241022
92.1
86.0
91.0
74.6
58.6
35.1
46.8
25.7
31.6
60.70
Table 1:
Performance comparison of
Qwen2.5-Coder
Base and Instruct models with our iterative SFT models across code generation benchmarks. All metrics represent Pass@1 execution rates (%). Complete split is reported for Base models and Instruct split for Instruct models.
Bold
indicates best performance within each size category. “-” denotes unavailable or inapplicable results.
Definition 2.1
(Execution Signature)
.
Given candidates
R
=
{
r
1
,
…
,
r
n
}
R=\{r_{1},\dots,r_{n}\}
and tests
T
=
{
t
1
,
…
,
t
m
}
T=\{t_{1},\dots,t_{m}\}
, define
Exec
:
R
×
T
→
{
0
,
1
}
\mathrm{Exec}:R\times T\rightarrow\{0,1\}
as the pass indicator:
Exec
​
(
r
i
,
t
j
)
=
1
\mathrm{Exec}(r_{i},t_{j})=1
if
r
i
r_{i}
passes
t
j
t_{j}
, and
0
otherwise.
The execution signature of
r
i
r_{i}
on
T
T
is
σ
​
(
r
i
;
T
)
=
⨁
j
=
1
m
Exec
​
(
r
i
,
t
j
)
,
\sigma(r_{i};T)=\bigoplus_{j=1}^{m}\mathrm{Exec}(r_{i},t_{j}),
(2)
where
⨁
\bigoplus
denotes ordered concatenation. Thus
σ
​
(
r
i
;
T
)
∈
{
0
,
1
}
m
\sigma(r_{i};T)\in\{0,1\}^{m}
, and
σ
​
(
r
i
;
T
)
=
𝟏
m
\sigma(r_{i};T)=\mathbf{1}_{m}
indicates that
r
i
r_{i}
passes all
m
m
tests.
Definition 2.2
(Consensus Clusters)
.
If
σ
​
(
r
i
,
T
)
=
σ
​
(
r
j
,
T
)
\sigma(r_{i},T)=\sigma(r_{j},T)
, we can regard the
r
i
r_{i}
and
r
j
r_{j}
as equivalent solution.
Given the value of
σ
​
(
r
i
,
T
)
\sigma(r_{i},T)
, we can partition
R
R
into clusters
𝒞
=
{
C
1
,
…
,
C
ℓ
}
\mathcal{C}=\{C_{1},\dots,C_{\ell}\}
of behaviorally identical candidates.
Definition 2.3
(Quality Metrics)
.
Each candidate
r
∈
R
r\in R
is scored by:
e
​
(
r
)
\displaystyle e(r)
=
|
{
t
∈
T
:
Exec
​
(
r
,
t
)
≠
⟂
}
|
|
T
|
,
\displaystyle=\frac{|\{t\in T:\mathrm{Exec}(r,t)\neq\perp\}|}{|T|},
(3)
s
​
(
r
)
\displaystyle s(r)
=
|
{
r
′
∈
R
:
σ
​
(
r
′
)
=
σ
​
(
r
)
}
|
,
\displaystyle=|\{r^{\prime}\in R:\sigma(r^{\prime})=\sigma(r)\}|,
f
​
(
r
)
\displaystyle f(r)
=
exp
⁡
(
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
|
r
|
log
⁡
p
​
(
x
i
∣
x
<
i
)
)
,
\displaystyle=\exp\!\left(-\frac{1}{|r|}\sum_{i=1}^{|r|}\log p(x_{i}\mid x_{<i})\right),
where
e
​
(
r
)
e(r)
measures execution success,
s
​
(
r
)
s(r)
consensus strength, and
f
​
(
r
)
f(r)
code fluency.
2.3.2
Hierarchical Selection
Iter
HumanEval
MBPP
BCB-Complete
BCB-Instruct
LiveCode-
FullStack-
HE
HE+
MBPP
MBPP+
Full
Hard
Full
Hard
Bench
Bench
Ucoder-7B
0
77.4
67.1
72.0
63.0
44.4
15.5
34.6
14.9
13.0
40.2
1
81.7
+
​
4.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.3}
74.4
+
​
7.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.3}
72.0
0.0
63.0
0.0
51.3
+
​
6.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.9}
23.0
+
​
7.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.5}
42.2
+
​
7.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.6}
20.9
+
​
6.0
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.0}
15.3
+
​
2.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.3}
48.2
+
​
7.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.9}
2
84.1
+
​
6.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.7}
77.4
+
​
10.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}10.3}
79.1
+
​
7.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.1}
66.4
+
​
3.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.4}
44.7
+
​
0.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.3}
14.9
-
​
0.6
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.6}
35.8
+
​
1.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.2}
12.2
-
​
2.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.7}
14.5
+
​
1.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.5}
40.2
-
​
0.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.1}
3
84.1
+
​
6.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.7}
76.8
+
​
9.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.7}
81.2
+
​
9.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.2}
69.0
+
​
6.0
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.0}
44.4
0.0
15.5
0.0
34.5
-
​
0.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.1}
13.5
-
​
1.4
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}1.4}
21.4
+
​
8.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}8.4}
40.2
0.0
4
84.1
+
​
6.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.7}
77.4
+
​
10.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}10.3}
79.1
+
​
7.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.1}
66.4
+
​
3.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.4}
44.7
+
​
0.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.3}
14.9
-
​
0.6
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.6}
35.8
+
​
1.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.2}
12.2
-
​
2.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.7}
14.5
+
​
1.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.5}
40.2
-
​
0.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.1}
5
81.7
+
​
4.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.3}
75.0
+
​
7.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.9}
83.9
+
​
11.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}11.9}
71.2
+
​
8.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}8.2}
52.2
+
​
7.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.8}
19.6
+
​
4.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.1}
40.7
+
​
6.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.1}
14.2
-
​
0.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.7}
20.6
+
​
7.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.6}
50.0
+
​
9.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.7}
6
83.5
+
​
6.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.1}
76.8
+
​
9.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.7}
85.2
+
​
13.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}13.2}
72.2
+
​
9.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.2}
52.0
+
​
7.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.6}
22.3
+
​
6.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.8}
41.1
+
​
6.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.5}
15.5
+
​
0.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.6}
22.9
+
​
9.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.9}
51.3
+
​
11.0
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}11.0}
Ucoder-14B
0
83.5
76.8
75.9
64.0
53.3
23.6
43.2
16.2
22.1
50.1
1
85.4
+
​
1.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.9}
77.4
+
​
0.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.6}
87.8
+
​
11.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}11.9}
73.3
+
​
9.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.3}
53.1
-
​
0.2
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.2}
21.6
-
​
2.0
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.0}
41.0
-
​
2.2
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.2}
14.2
-
​
2.0
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.0}
17.6
-
​
4.5
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}4.5}
53.6
+
​
3.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.5}
2
84.8
+
​
1.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.3}
76.2
-
​
0.6
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.6}
84.9
+
​
9.0
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}9.0}
70.6
+
​
6.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}6.6}
50.4
-
​
2.9
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.9}
23.6
0.0
40.9
-
​
2.3
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.3}
15.5
-
​
0.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.7}
19.1
-
​
3.0
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}3.0}
49.9
-
​
0.2
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.2}
3
84.8
+
​
1.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.3}
78.0
+
​
1.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.2}
83.6
+
​
7.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.7}
72.2
+
​
8.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}8.2}
51.6
-
​
1.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}1.7}
23.0
-
​
0.6
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.6}
41.8
-
​
1.4
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}1.4}
15.5
-
​
0.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.7}
18.3
-
​
3.8
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}3.8}
49.8
-
​
0.3
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.3}
4
84.8
+
​
1.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.3}
78.0
+
​
1.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.2}
84.1
+
​
8.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}8.2}
72.8
+
​
8.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}8.8}
51.8
-
​
1.5
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}1.5}
18.2
-
​
5.4
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}5.4}
41.1
-
​
2.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.1}
12.8
-
​
3.4
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}3.4}
22.1
0.0
50.4
+
​
0.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.3}
5
87.8
+
​
4.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.3}
81.1
+
​
4.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.3}
86.5
+
​
10.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}10.6}
74.3
+
​
10.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}10.3}
53.9
+
​
0.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.6}
24.3
+
​
0.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.7}
40.9
-
​
2.3
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.3}
16.2
0.0
20.6
-
​
1.5
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}1.5}
52.5
+
​
2.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.4}
6
87.2
+
​
3.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.7}
80.5
+
​
3.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.7}
84.4
+
​
8.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}8.5}
71.7
+
​
7.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}7.7}
53.3
0.0
23.0
-
​
0.6
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.6}
43.5
+
​
0.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.3}
16.2
0.0
22.9
+
​
0.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.8}
51.6
+
​
1.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.5}
Ucoder-32B
0
86.0
78.0
86.2
72.2
54.8
28.4
44.6
18.9
22.1
53.0
1
87.8
+
​
1.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.8}
82.3
+
​
4.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.3}
89.9
+
​
3.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.7}
75.9
+
​
3.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.7}
55.4
+
​
0.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.6}
23.6
-
​
4.8
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}4.8}
44.5
-
​
0.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.1}
17.6
-
​
1.3
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}1.3}
17.6
-
​
4.5
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}4.5}
54.3
+
​
1.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.2}
2
86.6
+
​
0.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.6}
81.1
+
​
3.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.1}
88.4
+
​
2.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.2}
74.6
+
​
2.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.4}
56.2
+
​
1.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.4}
23.0
-
​
5.4
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}5.4}
44.8
+
​
0.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.2}
18.9
0.0
16.0
-
​
6.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}6.1}
52.4
-
​
0.6
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.6}
3
87.8
+
​
1.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.8}
81.1
+
​
3.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.1}
88.9
+
​
2.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.7}
74.6
+
​
2.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.4}
54.3
-
​
0.5
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.5}
22.3
-
​
6.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}6.1}
43.8
-
​
0.8
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.8}
16.9
-
​
2.0
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.0}
19.8
-
​
2.3
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.3}
54.7
+
​
1.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.7}
4
89.0
+
​
3.0
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.0}
82.9
+
​
4.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.9}
89.7
+
​
3.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.5}
75.7
+
​
3.5
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.5}
55.4
+
​
0.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.6}
27.7
-
​
0.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.7}
45.7
+
​
1.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.1}
17.6
-
​
1.3
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}1.3}
21.4
-
​
0.7
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.7}
53.4
+
​
0.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.3}
5
88.4
+
​
2.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.4}
81.7
+
​
3.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.7}
87.8
+
​
1.6
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.6}
73.3
+
​
1.1
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.1}
54.5
-
​
0.3
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.3}
24.3
-
​
4.1
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}4.1}
43.8
-
​
0.8
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.8}
18.9
0.0
22.9
+
​
0.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.8}
53.3
+
​
0.2
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.2}
6
88.4
+
​
2.4
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}2.4}
82.3
+
​
4.3
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}4.3}
89.2
+
​
3.0
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}3.0}
74.1
+
​
1.9
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}1.9}
54.0
-
​
0.8
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.8}
23.6
-
​
4.8
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}4.8}
44.1
-
​
0.5
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}0.5}
16.9
-
​
2.0
{}_{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\text{-}2.0}
22.9
+
​
0.8
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.8}
53.8
+
​
0.7
{}_{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}\text{+}0.7}
Table 2:
Performance (Pass@1) across iterative SFT rounds at different model scales using Qwen2.5-Coder as the base model. Orange-highlighted rows show Iter 0 (initial model trained on seed data), while subsequent iterations use self-generated synthetic data. Blue-highlighted rows indicate the best-performing iteration for each scale. Bold denotes best performance, underline denotes second-best performance for each metric within each scale, and subscripts show differences from Iter 0 (
g
​
r
​
e
​
e
​
n
{\color[rgb]{0,0.6,0}\definecolor[named]{pgfstrokecolor}{rgb}{0,0.6,0}green}
for improvement,
r
​
e
​
d
{\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}red}
for decline).
We select the valid candidates using three criteria:
(1) Reliability Filtering.
Candidates with low execution success are removed (threshold
ρ
=
0.8
\rho=0.8
):
R
′
=
{
r
∈
R
:
e
​
(
r
)
≥
ρ
}
R^{\prime}=\{r\in R:e(r)\geq\rho\}
.
(2) Consensus Selection.
We select the largest non-trivial cluster:
C
∗
=
arg
⁡
max
C
∈
𝒞
′
,
|
C
|
≥
τ
⁡
|
C
|
C^{*}=\arg\max_{C\in\mathcal{C}^{\prime},\,|C|\geq\tau}|C|
(3) Intra-Cluster Selection.
Within
C
∗
C^{*}
, we choose
r
∗
=
arg
⁡
max
r
∈
C
∗
⁡
⟨
e
​
(
r
)
,
−
f
​
(
r
)
⟩
r^{*}=\arg\max_{r\in C^{*}}\langle e(r),-f(r)\rangle
.
2.3.3
Theoretical Guarantee
Theorem 2.4
(Consensus Convergence)
.
Let
R
=
{
r
1
,
…
,
r
n
}
R=\{r_{1},\dots,r_{n}\}
be
n
n
candidates sampled independently from a model, and let T denote a set of unit tests.
Assume that at least
k
k
candidates in
R
R
are functionally correct with probability at least
1
−
δ
1-\delta
, and that any pair of incorrect implementations produces identical outputs on a single test with probability at most
p
<
1
p<1
.
If the test set size satisfies
|
T
|
≥
log
⁡
(
n
/
k
)
−
log
⁡
p
,
|T|\geq\frac{\log(n/k)}{-\log p},
then the largest consensus cluster
C
max
C_{\max}
contains only correct implementations with probability at least
P
​
(
C
max
​
is correct
)
≥
1
−
δ
−
n
2
​
p
|
𝒯
|
.
P(C_{\max}\ \text{is correct})\geq 1-\delta-n^{2}p^{|\mathcal{T}|}.
2.4
Iterative Self-Training
We formalize the iterative self-training procedure and explain why it yields consistent improvement.
Definition 2.5
(Iterative Update)
.
At iteration
t
t
, we construct training set
𝒟
t
=
{
(
q
i
,
r
i
∗
)
}
\mathcal{D}_{t}=\{(q_{i},r_{i}^{*})\}
, where each
r
i
∗
r_{i}^{*}
is selected via consensus from
n
n
candidates sampled from
ℳ
t
\mathcal{M}_{t}
, and update:
θ
t
+
1
=
arg
⁡
max
θ
​
∑
(
q
,
r
∗
)
∈
𝒟
t
log
⁡
p
θ
​
(
r
∗
∣
q
)
.
\theta_{t+1}=\arg\max_{\theta}\sum_{(q,r^{*})\in\mathcal{D}_{t}}\log p_{\theta}(r^{*}\mid q).
(4)
Why Self-Training Improves Performance?
Iterative self-training is effective because consensus selection acts as a quality filter. Let
Q
​
(
r
)
∈
[
0
,
1
]
Q(r)\in[0,1]
denote candidate quality. For
n
n
independent samples, random selection yields expected quality
𝔼
r
∼
ℳ
t
​
[
Q
​
(
r
)
]
\mathbb{E}_{r\sim\mathcal{M}_{t}}[Q(r)]
, whereas consensus selection favors correct implementations that cluster by execution behavior, achieving (for some
Δ
>
0
\Delta>0
):
𝔼
​
[
Q
​
(
r
∗
)
]
=
𝔼
r
∼
ℳ
t
​
[
Q
​
(
r
)
]
+
Δ
,
\mathbb{E}[Q(r^{*})]=\mathbb{E}_{r\sim\mathcal{M}_{t}}[Q(r)]+\Delta,
(5)
Optimizing on
𝒟
t
\mathcal{D}_{t}
shifts the model toward higher-quality samples. As
ℳ
t
+
1
\mathcal{M}_{t+1}
increases
p
θ
​
(
r
∗
∣
q
)
p_{\theta}(r^{*}\mid q)
for above-average outputs:
𝔼
r
∼
ℳ
t
+
1
​
[
Q
​
(
r
)
]
≥
𝔼
r
∼
ℳ
t
​
[
Q
​
(
r
)
]
,
\mathbb{E}_{r\sim\mathcal{M}_{t+1}}[Q(r)]\geq\mathbb{E}_{r\sim\mathcal{M}_{t}}[Q(r)],
(6)
where it induces a positive feedback loop where improved models generate higher-quality candidates and more reliable training signals.
3
Experiments
3.1
Training and Evaluation Details
Model Configuration.
We experiment with Qwen2.5-Coder
qwen25coder
models at 7B, 14B, and 32B scales, starting from base checkpoints without prior instruction tuning and applying identical self-bootstrapping procedures across all scales for fair comparison.
Training Hyperparameters.
We employ consistent training settings across experiments. Models are fine-tuned for 3 epochs per iteration using AdamW with a learning rate of 5e-6 and a cosine decay schedule. We use a batch size of 128 with gradient accumulation to fit memory constraints.
Evaluation Benchmarks.
We evaluate on six benchmarks:
HumanEval
humaneval
and
MBPP/MBPP+
mbpp
assess classic Python programming;
LiveCodeBench
LiveCodeBench
provides contamination-free competitive programming problems;
BigCodeBench (BCB)
bigcodebench
evaluates function completion with broader context and API usage (both Complete and Instruct variants); and
FullStackBench
fullstack
covers diverse real-world scenarios. We report Pass@1 accuracy with execution-based validation; solutions must pass all test cases.
Figure 4:
Lexical entropy distribution of 16,867 generated problems. Histogram with KDE shows per-problem entropy; CDF (green) and boxplot show cumulative coverage.
Figure 5:
Complexity versus semantic coverage distribution. Color encodes density; red line shows linear trend (
r
=
0.664
r=0.664
).
Figure 6:
Quality distribution characterization.
Top: perplexity distribution across 9,700 samples with quartile stratification and KDE overlay (truncated at 1.12). Bottom: perplexity versus execution success rate, showing high-quality samples (80%+ success) concentrated below perplexity 1.05.
3.2
Main Results
Table 1
demonstrates that unsupervised self-bootstrapping achieves performance comparable to supervised instruction tuning across diverse code generation benchmarks. Compared with other instruction-tuned models of similar scale, UCoder exhibits competitive or superior performance, consistently matching or exceeding Qwen2.5-Coder-Instruct on challenging benchmarks including MBPP+, BigCodeBench-Complete, and FullStackBench at all model scales (7B, 14B, 32B). Although certain Instruct models retain advantages on HumanEval, our approach progressively narrows this gap as model scale increases. These results indicate that execution-driven self-training can effectively elicit the latent instruction-following capabilities embedded in pre-trained code models, achieving supervised-level performance without requiring any human annotations or curated instruction data.
3.3
Effects of Iterative Self-Improvement
Table 2
reports performance across six self-bootstrapping iterations at three model scales, demonstrating both framework effectiveness and scale-dependent dynamics.
Framework Effectiveness.
Iterative self-bootstrapping consistently improves performance without external supervision. Across benchmarks, all model scales show substantial gains over seed-trained baselines (Iter 0), with improvements of +6.1 to +13.2 points at 7B, +4.3 to +10.6 at 14B, and +3.0 to +4.9 at 32B. Gains are most pronounced on benchmarks requiring diverse programming skills, such as MBPP, FullStackBench, and LiveCodeBench, rather than narrowly scoped tasks like HumanEval. This supports our hypothesis that self-generated problem diversity combined with execution-driven consensus expands capability coverage beyond seed data.
Inverse Scaling of Improvement.
Performance gains exhibit an inverse scaling trend, with smaller models benefiting disproportionately. We attribute this effect to
latent capability gaps
, where pre-trained knowledge is only partially accessible through standard prompting. Consensus-based selection mitigates this gap by reinforcing correct patterns that smaller models generate inconsistently. Notably, the self-improved 7B model reaches 85.2% on MBPP, approaching the 32B baseline (86.2%), highlighting self-bootstrapping as a compute-efficient alternative to model scaling.
Convergence Characteristics.
The optimal number of iterations decreases with model scale—six for 7B, five for 14B, and four for 32B. Beyond these points, performance exhibits mild oscillation rather than degradation, reflecting a trade-off between specialization on synthetic data and generalization to held-out distributions. These observations motivate early stopping based on validation performance.
Method
HumanEval
MBPP
BCB-Complete
BCB-Instruct
LiveCode-
FullStack-
HE
HE+
MBPP
MBPP+
Full
Hard
Full
Hard
Bench
Bench
7B Models
UCoder
77.4
67.1
72.0
63.0
44.4
15.5
34.6
14.9
13.0
40.25
Random
73.8
64.6
65.6
56.6
45.5
14.9
37.5
13.5
10.7
33.55
Cluster
73.8
66.5
68.8
58.5
41.3
12.2
36.5
12.2
10.7
38.35
Low PPL
77.4
70.7
70.1
59.3
45.6
17.6
37.3
12.2
12.2
37.11
Success Rate
75.0
67.7
66.9
57.1
41.4
11.5
33.0
12.2
12.2
40.01
14B Models
UCoder
83.5
76.8
75.9
64.0
53.3
23.6
43.2
16.2
22.1
50.09
Random
81.7
76.2
71.7
60.1
53.8
20.9
43.3
17.6
16.8
47.95
Cluster
82.3
76.8
73.0
64.0
50.4
18.2
42.4
15.5
17.6
48.55
Low PPL
82.9
77.4
73.3
63.5
50.7
20.3
42.2
23.0
19.1
49.32
Success Rate
82.3
75.6
74.1
63.2
50.6
20.9
41.3
14.9
17.6
47.36
32B Models
UCoder
86.0
78.0
86.2
72.2
54.8
28.4
44.6
18.9
22.1
53.05
Random
84.8
79.3
80.7
69.6
53.7
25.0
46.6
21.6
15.3
39.18
Cluster
83.5
75.6
81.5
71.2
53.9
23.0
45.1
16.9
13.0
49.91
Low PPL
84.1
76.2
79.9
67.5
53.5
27.7
45.4
23.0
18.3
50.09
Success Rate
82.3
75.6
81.2
69.6
54.1
27.7
44.2
17.6
21.4
50.50
Table 3:
Ablation study comparing data selection strategies across model scales:
UCoder
(execution-driven consensus),
Random
(random sampling from successful solutions), Cluster (clustering-based),
Low PPL
(lowest perplexity), and
Success Rate
(weighted by execution success). All metrics show Pass@1 execution rates (%).
Bold/Underline
indicate best/second-best performance per size category.
4
Analysis
4.1
Diversity of Self-Generated Problems
Lexical Diversity.
We quantify lexical diversity using Shannon entropy
H
=
−
∑
i
p
i
​
log
2
⁡
p
i
H=-\sum_{i}p_{i}\log_{2}p_{i}
, where
p
i
p_{i}
denotes token probability. Figure
4
shows a near-Gaussian entropy distribution (mean
μ
=
3.64
\mu=3.64
bits,
σ
=
0.69
\sigma=0.69
, median 3.62), indicating natural variation rather than templated construction. The smooth CDF and moderate interquartile range further suggest balanced coverage from concise to elaborate specifications.
Semantic Coverage.
As shown in Figure
9
(Appendix), the generated problems contain 229 domain-specific terms across seven categories, with Data Structures (18.3%), Algorithms (14.8%), and String Processing (11.4%) being most prominent. No category exceeds 20%, demonstrating broad semantic coverage, while concrete algorithmic terms (e.g.,
dijkstra
,
greedy
,
traversal
) indicate non-generic, verifiable challenges.
Complexity Distribution.
We assess problem difficulty and conceptual breadth using a
Complexity Score
(0–10, aggregating parameter count, description length, algorithmic keywords, and constraints) and a
Semantic Coverage Score
(weighted keyword matches across seven categories). Figure
5
shows a moderate positive correlation (
r
=
0.664
r=0.664
), indicating that more complex problems tend to integrate multiple concepts. Problems span the full score ranges (complexity:
3.55
±
1.60
3.55\pm 1.60
, semantic:
3.16
±
1.32
3.16\pm 1.32
) with a continuous density profile, suggesting a natural difficulty continuum suitable for curriculum learning.
4.2
Execution-Driven Consensus Effectiveness
Solution Space Diversity.
We first examine whether dense sampling with
n
=
128
n=128
candidates yields a sufficiently diverse solution pool. As shown in Figure
8
, the abstract syntax tree (AST) node distribution spans 15 syntactic constructs across 2.6M generated samples (212M total nodes), indicating diverse implementation structures beyond primitive elements. The joint distribution of cyclomatic complexity and code length further shows broad dispersion (mean complexity
2.7
±
2.3
2.7\pm 2.3
, mean length
22.4
±
10.5
22.4\pm 10.5
lines), confirming substantial heterogeneity in the solution space.
Quality Distribution Characterization.
Given this diversity, we examine whether solution quality exhibits sufficient separation for reliable selection. Figure
6
shows the perplexity distribution over 9,700 sampled candidates and its relationship with execution success. The distribution is right-skewed (mean 1.03, std 0.03) with clear stratification: high-quality samples concentrate at low perplexity values around 1.01, while lower-quality samples progressively shift toward higher perplexity, extending beyond 1.10. Consistently, solutions with execution success rates above 80% cluster predominantly below perplexity 1.05, with rapid performance degradation beyond this range. This sharp transition indicates that high-quality solutions form a distinct and identifiable subset within the candidate pool.
Figure 7:
Filtered dataset (green) improves quality over full dataset (gray) while maintaining diversity.
Quality Improvement.
Consensus-based filtering yields substantial improvements across all quality metrics. In
Figure 7
, the filtered dataset consistently outperforms the full dataset in success rate, error-free rate, and code uniqueness. Besides, these gains are achieved without sacrificing diversity, where structural and semantic entropy remain comparable between the two datasets. This demonstrates that execution-driven consensus selection effectively resolves the quality–diversity trade-off.
4.3
Ablation Study
To isolate the effect of data selection, we compare our consensus-based approach with four alternatives:
Random
uniform sampling,
Cluster
selection from dominant output-hash clusters,
Low PPL
selection based on minimal perplexity, and
Success Rate
filtering with a 0.5 execution threshold.
Table 3
shows our approach consistently outperforms all baselines across three model scales, achieving the best results on most benchmarks. The performance gap widens with scale, on FullStackBench, the margin over Random increases from 6.7 points at 7B to 13.9 points at 32B, suggesting larger models produce more diverse candidate pools where principled selection matters most. While individual baselines excel on specific benchmarks, none matches the robustness of consensus-based selection. Notably, Success Rate filtering fails to consistently outperform Random, indicating binary pass/fail criteria inadequately capture quality differences, whereas consensus-based selection leverages behavioral consistency across test inputs as a richer quality signal.
5
Related Work
Unsupervised Learning for Code Post-training.
Unsupervised learning has become increasingly prominent in code generation through pre-training on vast unlabeled code repositories, building on early findings that source code exhibits statistical regularities similar to natural language
code_llama
;
deepseek_coder
;
starcoder
;
starcoder2
;
vgamegym
;
livereporeflection
. Recent work on unsupervised code post-training has focused on leveraging unlabeled code snippets and use LLM to generate synthetic question-answering data. Magicoder
magicoder
uses open-source code examples to teach LLMs how to create varied coding instructions and training data. Besides, WizardCoder
wizardcoder
progressively evolves simple coding instructions into complex ones for training. Further, WaveCoder
codearena
and CodeArena
codearena
generate more diverse and high-quality instruction data from the open source code dataset. Besides, there are some works
unsupervised_code_changes
;
unsupervised_code_translation
that adopt supervised learning for code translation and code change tasks.
Code Instruction Tuning.
Instruction tuning
opencoder
;
qwen25coder
;
yang2025codefoundationmodelsagents
has emerged as an effective approach for improving LLMs by fine-tuning them on instruction-based datasets, enabling better generalization and more accurate instruction-following capabilities. To improve the capabilities of code LLM, researchers have enhanced multiple code tasks and benchmarks, such as code generation of multiple domains (e.g., BigCodeBench
bigcodebench
and FullStackBench
fullstack
), multilingual code generation (e.g., MultiPl-E
multiple
and McEval
mceval
), and competitive programming problems (e.g., LiveCodeBench
LiveCodeBench
).
6
Conclusion
In this work, we introduce an execution-driven self-bootstrapping framework that removes the need for human-annotated instruction data in code generation. UCoder exploits latent programming knowledge in pre-trained models and uses execution feedback as a scalable, deterministic supervision signal for autonomous improvement. Guided by execution-driven consensus clustering, iterative self-training identifies correct implementations via behavioral consistency and constructs high-quality training data. Our results demonstrate that code models can achieve performance competitive with supervised baselines through fully autonomous learning, highlighting a scalable and cost-effective path for advancing code intelligence.
Limitations
Despite the promising results, our work has several limitations that warrant future investigation. First, the effectiveness of our consensus-based selection mechanism relies on the availability of executable test cases, which may not always be feasible for certain programming tasks or domains where formal specifications are difficult to construct. Second, while our method demonstrates strong performance on standard benchmarks, the computational cost of generating and evaluating 128 candidate solutions per problem remains substantial, potentially limiting its applicability in resource-constrained scenarios. Third, our approach primarily focuses on functional correctness through execution-based validation, which may not capture other important code quality attributes such as maintainability, documentation quality, or adherence to specific coding standards beyond those explicitly testable. Fourth, the iterative self-training process exhibits diminishing returns and potential overfitting to synthetic data distributions after a certain number of iterations, requiring careful validation-based early stopping. Finally, our analysis is primarily conducted on Python programming tasks, and the generalizability of our findings to other programming languages with different execution characteristics and paradigms remains to be thoroughly validated. These limitations highlight important directions for future work in unsupervised code generation.
Ethics Statement
This work on unsupervised code generation acknowledges several ethical considerations. Automated code generation systems can be misused to produce malicious code or security vulnerabilities, requiring appropriate safeguards, including content filtering and usage monitoring. All experiments used publicly available benchmarks and open-source models, ensuring transparency without collecting proprietary data. We advocate for responsible development with clear documentation, transparent methodologies, and adherence to intellectual property rights.
Acknowledgment
This work was supported by State Key Laboratory of Complex & Critical Software Environment (SKLCCSE) of Beihang University and supported by the Fundamental Research Funds for the Central Universities. This work was supported in part by the National Natural Science Foundation of China (Grant Nos. 62276017, 62406033, U1636211, 61672081), and the State Key Laboratory of Complex & Critical Software Environment (Grant No. SKLCCSE-2024ZX-18).
Appendix A
Additional Analysis Figures
Figure 8:
Solution space diversity analysis. Left: AST node type distribution across 2.6M samples totaling 212M nodes, spanning 15 distinct syntactic constructs. Right: Cyclomatic complexity versus code length with density contours, showing broad dispersion (complexity:
2.7
±
2.3
2.7\pm 2.3
, length:
22.4
±
10.5
22.4\pm 10.5
lines).
Figure 9:
Semantic distribution of 229 frequent terms in generated problems. Word size indicates frequency; colors denote categories.