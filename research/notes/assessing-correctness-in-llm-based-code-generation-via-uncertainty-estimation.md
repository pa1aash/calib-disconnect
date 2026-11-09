---
title: Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation
id: assessing-correctness-in-llm-based-code-generation-via-uncertainty-estimation
tags:
- code-llm-calibration-aaai27-eabf3f
- symbolic-clustering
- ast-proxy
- abstention-policy
created: '2026-07-17T18:37:35.495970Z'
updated: '2026-07-17T18:38:31.244461Z'
source: https://arxiv.org/html/2502.11620
source_domain: arxiv.org
fetched_at: '2026-07-17T18:37:35.495176Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Sharma and David (2025), arXiv:2502.11620. Directly load-bearing for the
  disconnect thesis''s AST/symbolic-clustering-proxy category. Tests whether standard
  NLG uncertainty-quantification techniques (semantic entropy SE, mutual information
  MI, token log-probabilities) transfer to code generation on LiveCodeBench (831 problems:
  239 Easy/332 Medium/260 Hard) using gpt-3.5-turbo-instruct, DeepSeek-R1, and claude-3-7-sonnet.
  Central finding: semantic entropy and mutual-information methods -- even when adapted
  with code-specific embeddings (text-embedding-ada-002) or CodeBLEU similarity --
  show NO statistically significant correlation with correctness; token-level log-probabilities
  (LLM-Probability) likewise show NO statistically significant correlation with correctness.
  The fix is symbolic clustering: using symbolic execution (treating inputs as symbolic
  variables, comparing programs'' symbolic input-output relations) to precisely group
  semantically-equivalent code outputs restores statistically significant correlation
  for both SE and MI (SE-SymbNorm, SE-SymbUniform, MI-SymbNorm, MI-SymbUniform). Crucially,
  this correlation holds even when completely discarding the LLM''s output-probability
  distribution and assuming a UNIFORM distribution over sampled outputs -- meaning
  the discriminative power comes entirely from precise equivalence clustering, not
  from the log-prob channel. From this the authors distill a minimal correctness proxy,
  symbolic cluster count (CC-Symb, just the number of distinct symbolic-execution
  clusters among samples), which alone correlates with correctness and, when used
  as an abstention-policy threshold (LLM abstains above threshold), achieves false
  positive rate below 0.02% (essentially never presenting incorrect code) with false
  negative rates of 11.9%-20.3%. A code-embedding-based cluster-count baseline (CC-CodeEmbed)
  does NOT show significant correlation, confirming precision of the equivalence check
  (not mere clustering) is what matters. Limitation: symbolic execution is bounded
  (loop unrolling with a timeout), risking false-equivalence for programs whose behavioral
  differences only manifest beyond the unrolling limit; scoped to Python via a lightweight
  in-process symbolic-execution library. Relation to disconnect thesis: this is the
  strongest existing evidence that (a) token log-probabilities carry essentially no
  correctness signal for code (stronger than our paper''s AUROC 0.668 -- this paper
  finds no significant correlation at all), and (b) among proxy/expressed interfaces,
  only PRECISE (symbolic-execution-grounded) equivalence clustering recovers a usable
  signal -- embedding-based and CodeBLEU-based AST-adjacent proxies fail just as badly
  as log-probs. This sets a much higher bar for any AST-clustering proxy claim: coarse
  structural/embedding equivalence is insufficient; only execution-grounded equivalence
  works, which is expensive and Python/loop-bounded. Directly frames a testable open
  question: does symbolic cluster count on Qwen2.5-Coder-7B/DeepSeek-Coder-6.7B/HumanEval
  reproduce this near-zero-log-prob-correlation and near-zero-false-positive abstention
  result, and can it be approximated at a lower cost than full symbolic execution
  for a single-GPU budget?'
---

*Suggested by [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]] — cited as symbolic/AST-clustering uncertainty method for code, directly relevant to AST-clustering proxy in disconnect thesis*

Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation
Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation
Arindam Sharma
University of Bristol
Bristol, United Kingdom
arindam.sharma@bristol.ac.uk
&Cristina David
University of Bristol
Bristol, United Kingdom
cristina.david@bristol.ac.uk
Abstract
Large Language Models (LLMs) have shown strong performance in code generation, but their outputs lack inherent correctness guarantees. In natural language generation (NLG), uncertainty—often grounded in information theory—has been used as a proxy for output quality. However, state-of-the-art techniques
[
27
,
14
,
3
]
fail to exhibit a correlation between estimated uncertainty and correctness when applied to code. We investigate this discrepancy and identify semantic clustering as the key factor: existing learned embeddings and heuristic metrics such as CodeBLEU fail to capture functional equivalence with sufficient precision to support reliable uncertainty estimation.
We propose
symbolic clustering
, a principled alternative based on symbolic execution, enabling precise clustering of semantically equivalent programs. Incorporating symbolic clustering into NLG-derived uncertainty techniques restores their predictive power. We further show that token-level probabilities are not essential—uncertainty estimates assuming uniform distributions perform comparably. Based on this, we introduce a lightweight correctness proxy: symbolic cluster count. Despite its simplicity, it correlates with correctness and supports highly effective abstention policies, achieving a false positive rate below 0.02%.
1
Introduction
LLMs have shown impressive capabilities across a range of software engineering tasks, including code synthesis
[
29
,
43
]
, bug fixing
[
13
,
53
]
, refactoring
[
9
,
42
,
40
]
, and translation
[
52
,
33
,
12
,
39
]
. However, LLM-generated code lacks inherent correctness guarantees. As a result, correctness is typically assessed by running the code against
external oracles
—test suites, reference solutions, or other expert specifications.
While these external techniques can provide evidence of functional correctness, such as passing unit tests, they are not always available.
Even when present, they may be insufficiently precise, e.g., unit tests may only cover a limited subset of the code’s behaviour.
In contrast, NLG has made notable strides in oracle-free quality estimation by leveraging internal model signals, such as token-level log-probabilities.
Among the most effective are information-theoretic methods
[
14
,
27
,
3
]
, which estimate a model’s
uncertainty
based on the intuition that it peaks when outputs are least informative, using entropy
[
14
,
27
]
or mutual information
[
3
]
as their foundation.
Other techniques
[
28
,
10
,
35
,
38
,
8
,
51
,
18
,
23
]
are either shown to be less effective or rely on costly additional training steps.
A key innovation in uncertainty estimation, introduced by Kuhn et al.
[
27
]
, is
semantic clustering
, which accounts for the diversity of plausible outputs. Rather than estimating uncertainty over individual responses, they group responses into clusters based on semantic equivalence, and compute uncertainty over this coarser space. This shift allows the uncertainty estimates to reflect variation in meaning rather than superficial syntactic differences.
In this paper, we investigate whether state-of-the-art information-theoretic approaches for estimating model uncertainty—specifically those by Kuhn et al.
[
27
,
14
]
and Abbasi et al.
[
3
]
—generalise to code generation. We evaluate their predictive power by testing for correlation between estimated uncertainty and correctness. Our results show that even when replacing text-specific embeddings with code-specific ones for semantic clustering, uncertainty measures from the original NLG methods fail to correlate with correctness in code generation tasks.
We attribute this to the rigid nature of programs, where small syntactic differences can imply significant behavioural changes or none at all, making learned semantic clustering brittle. To address this, we explore the use of semantic clustering techniques grounded in
symbolic reasoning
.
As a first step, we evaluate CodeBLEU
[
41
]
, a commonly used similarity metric that augments syntactic matching with data flow analysis to approximate semantics
[
47
]
. However, CodeBLEU remains a heuristic—it lacks formal reasoning and cannot reliably capture semantic equivalence. In our evaluation, clustering based on CodeBLEU failed to improve the correlation between uncertainty and correctness, confirming that its semantic component is too coarse-grained for this purpose.
This led us to pursue a more precise alternative:
symbolic clustering
via
symbolic execution
, where symbolic execution executes programs over symbolic rather than concrete inputs
[
6
]
. By comparing the programs’ output expressions, symbolic execution offers us a principled way to identify semantically equivalent programs, even when they vary significantly in syntax. We integrated symbolic clustering into leading NLG-based uncertainty estimation frameworks
[
3
,
14
,
27
]
, adapting them to the code generation setting. Unlike their original versions, the adapted methods exhibit a statistically significant correlation between estimated uncertainty and actual correctness. This supports the view that precise semantic reasoning, grounded in formal methods like symbolic execution, is essential for reliable uncertainty estimation in code generation.
Interestingly, we find that token log-probabilities output by the LLM—used by the entropy and mutual information calculations in
[
27
,
14
]
and
[
3
]
, respectively—have limited effect: assuming a uniform output distribution performs comparably. This highlights another insight: semantic equivalence, not probabilistic confidence, is the dominant signal for correctness in code generation.
Building on this insight, we propose a much simpler correctness metric: the
symbolic cluster count
. The intuition is straightforward—fewer functionally distinct outputs suggest greater model confidence. Despite its simplicity, this metric shows a correlation with actual correctness, highlighting its effectiveness as a lightweight yet reliable proxy for correctness.
We further leverage our insights into the correlation between uncertainty estimates and correctness to define
abstention policies
, where the model should refrain from generating a response if
the response is estimated to be incorrect. Our evaluation shows that, under these policies, the LLM achieves a false positive rate below 0.02%, effectively ensuring that it never outputs incorrect responses, with false negative rates ranging from 11.9% to 20.3%. Notably, this strong performance holds even for the abstention policy based solely on the symbolic cluster count, despite its simplicity.
Contributions.
•
We investigate the correlation between LLM uncertainty—computed using state-of-the-art NLG techniques
[
3
,
14
,
27
]
—and correctness in code generation tasks. We find that even when adapted to code (for example by incorporating code-specific learned embeddings or heuristic symbolic metrics like CodeBLEU) these methods fail to exhibit a statistically significant correlation between estimated uncertainty and actual correctness.
•
To the best of our knowledge, we are the first to address these limitations by introducing
symbolic clustering
, i.e. a symbolic execution–based approach for clustering semantically equivalent code outputs. This leads to a correlation between uncertainty estimates and functional correctness. Moreover, we show that this correlation holds even when ignoring the LLM’s output distribution and assuming an uniform distribution.
•
Motivated by our findings, we propose a lightweight alternative correctness metric based solely on
symbolic clusters count
. Despite its simplicity, our experimental evaluation shows it performs on par with more complex, information-theoretic approaches.
•
We define
abstention policies
, where the model should refrain from generating a response if the response is estimated to be incorrect.
Our evaluation results show that, under these policies, the LLM achieves a false positive rate below 0.02%.
•
We conduct an experimental evaluation involving 3 LLMs, the
LiveCodeBench
dataset for code-related tasks
[
20
]
, 13 correctness proxy techniques, and 5 abstention policies.
2
Background on NLG-Based Uncertainty Estimation Techniques
We selected two recent and well-established state-of-the-art techniques for information-theoretic uncertainty estimation in NLG to adapt and evaluate on code generation tasks.
In the first one, Kuhn et al.
[
14
,
27
]
estimate the uncertainty of a model’s prediction as the entropy of the output distribution.
In order to account for outputs that differ in form but share the same meaning, they introduce the idea of
semantic entropy
.
First, they group sampled model outputs into clusters of semantically equivalent responses, and define
p
⁢
(
c
∣
x
)
=
∑
s
∈
c
p
⁢
(
s
∣
x
)
𝑝
conditional
𝑐
𝑥
subscript
𝑠
𝑐
𝑝
conditional
𝑠
𝑥
p(c\mid x)\;=\;\sum_{s\in c}p(s\mid x)
italic_p ( italic_c ∣ italic_x ) = ∑ start_POSTSUBSCRIPT italic_s ∈ italic_c end_POSTSUBSCRIPT italic_p ( italic_s ∣ italic_x )
as the total probability mass of cluster
c
𝑐
c
italic_c
under the model’s output distribution. They then measure uncertainty over meanings (rather than raw token sequences) by taking the entropy of this cluster-level distribution:
SE
⁢
(
x
)
=
−
∑
c
p
⁢
(
c
∣
x
)
⁢
log
⁡
p
⁢
(
c
∣
x
)
SE
𝑥
subscript
𝑐
𝑝
conditional
𝑐
𝑥
𝑝
conditional
𝑐
𝑥
\mathrm{SE}(x)\;=\;-\sum_{c}p(c\mid x)\,\log p(c\mid x)
roman_SE ( italic_x ) = - ∑ start_POSTSUBSCRIPT italic_c end_POSTSUBSCRIPT italic_p ( italic_c ∣ italic_x ) roman_log italic_p ( italic_c ∣ italic_x )
.
This notion of semantic entropy offers a more accurate measure of uncertainty in free-form NLG, as it collapses paraphrases into a single representation before computing entropy.
In the second work, Abbasi et al.
[
3
]
further distinguish between “epistemic” uncertainty (caused by incomplete or incorrect knowledge) and “aleatoric” uncertainty (resulting from inherent randomness, such as multiple valid answers).
Intuitively, only epistemic uncertainty serves as a meaningful indicator of the correctness of the model’s response.
To isolate epistemic uncertainty, they propose an iterative prompting technique in which the model is repeatedly queried, with its prior responses incorporated into the context.
This method assesses the mutual information between successive responses to capture their dependencies: a high degree of dependency indicates elevated epistemic uncertainty, revealing the model’s uncertainty about the ground truth.
Similar to the work of Kuhn et al. , Abbasi et al. cluster responses into semantic equivalence classes, ensuring that the mutual information reflects semantic relationships.
More precisely, in order to isolate epistemic uncertainty, Abbasi et al.
[
3
]
quantify it as the mutual information of the pseudo-joint distribution over
n
𝑛
n
italic_n
successive responses:
I
⁢
(
μ
~
)
=
∑
y
1
:
n
μ
~
⁢
(
y
1
:
n
∣
x
)
⁢
log
⁡
μ
~
⁢
(
y
1
:
n
∣
x
)
∏
i
=
1
n
μ
~
i
⁢
(
y
i
∣
x
)
𝐼
~
𝜇
subscript
subscript
𝑦
:
1
𝑛
~
𝜇
conditional
subscript
𝑦
:
1
𝑛
𝑥
~
𝜇
conditional
subscript
𝑦
:
1
𝑛
𝑥
superscript
subscript
product
𝑖
1
𝑛
subscript
~
𝜇
𝑖
conditional
subscript
𝑦
𝑖
𝑥
I(\tilde{\mu})\;=\;\sum_{y_{1:n}}\tilde{\mu}(y_{1:n}\mid x)\log\frac{\tilde{%
\mu}(y_{1:n}\mid x)}{\prod_{i=1}^{n}\tilde{\mu}_{i}(y_{i}\mid x)}
italic_I ( over~ start_ARG italic_μ end_ARG ) = ∑ start_POSTSUBSCRIPT italic_y start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT end_POSTSUBSCRIPT over~ start_ARG italic_μ end_ARG ( italic_y start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x ) roman_log divide start_ARG over~ start_ARG italic_μ end_ARG ( italic_y start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x ) end_ARG start_ARG ∏ start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT over~ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( italic_y start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ∣ italic_x ) end_ARG
Here,
μ
~
⁢
(
y
1
:
n
∣
x
)
=
∏
i
=
1
n
μ
⁢
(
Y
i
∣
F
i
−
1
⁢
(
x
,
Y
1
:
i
−
1
)
)
~
𝜇
conditional
subscript
𝑦
:
1
𝑛
𝑥
superscript
subscript
product
𝑖
1
𝑛
𝜇
conditional
subscript
𝑌
𝑖
subscript
𝐹
𝑖
1
𝑥
subscript
𝑌
:
1
𝑖
1
\tilde{\mu}(y_{1:n}\mid x)=\prod_{i=1}^{n}\mu\bigl{(}Y_{i}\mid F_{i-1}(x,Y_{1:%
i-1})\bigr{)}
over~ start_ARG italic_μ end_ARG ( italic_y start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x ) = ∏ start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT italic_μ ( italic_Y start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ∣ italic_F start_POSTSUBSCRIPT italic_i - 1 end_POSTSUBSCRIPT ( italic_x , italic_Y start_POSTSUBSCRIPT 1 : italic_i - 1 end_POSTSUBSCRIPT ) )
is the pseudo-joint distribution obtained by iteratively prompting the model (with
F
i
−
1
⁢
(
x
,
Y
1
:
i
−
1
)
subscript
𝐹
𝑖
1
𝑥
subscript
𝑌
:
1
𝑖
1
F_{i-1}(x,Y_{1:i-1})
italic_F start_POSTSUBSCRIPT italic_i - 1 end_POSTSUBSCRIPT ( italic_x , italic_Y start_POSTSUBSCRIPT 1 : italic_i - 1 end_POSTSUBSCRIPT )
denoting the context composed of the original query
x
𝑥
x
italic_x
plus all previous responses
Y
1
,
…
,
Y
i
−
1
subscript
𝑌
1
…
subscript
𝑌
𝑖
1
Y_{1},\dots,Y_{i-1}
italic_Y start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , … , italic_Y start_POSTSUBSCRIPT italic_i - 1 end_POSTSUBSCRIPT
),
μ
~
i
⁢
(
y
i
∣
x
)
=
∑
y
¬
i
μ
~
⁢
(
y
1
:
n
∣
x
)
subscript
~
𝜇
𝑖
conditional
subscript
𝑦
𝑖
𝑥
subscript
subscript
𝑦
𝑖
~
𝜇
conditional
subscript
𝑦
:
1
𝑛
𝑥
\tilde{\mu}_{i}(y_{i}\mid x)=\sum_{y_{\neg i}}\tilde{\mu}(y_{1:n}\mid x)
over~ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( italic_y start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ∣ italic_x ) = ∑ start_POSTSUBSCRIPT italic_y start_POSTSUBSCRIPT ¬ italic_i end_POSTSUBSCRIPT end_POSTSUBSCRIPT over~ start_ARG italic_μ end_ARG ( italic_y start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x )
is its marginal for the
i
𝑖
i
italic_i
-th response, and
I
⁢
(
μ
~
)
𝐼
~
𝜇
I(\tilde{\mu})
italic_I ( over~ start_ARG italic_μ end_ARG )
measures how much knowing one response reduces uncertainty about the others.
3
Motivating Example
⬇
1
def
solve
(
nums
):
2
max_num
=
max
(
nums
)
3
expected_length
=
max_num
+
1
4
if
len
(
nums
)
!=
expected_length
:
5
return
False
6
count
=
{}
7
for
num
in
nums
:
8
if
num
in
count
:
9
count
[
num
]
+=
1
10
else
:
11
count
[
num
]
=
1
12
for
num
in
range
(1,
max_num
):
13
if
count
.
get
(
num
,
0)
!=
1:
14
return
False
15
if
count
.
get
(
max_num
,
0)
!=
2:
16
return
False
17
return
True
(a)
Snippet 1
⬇
1
def
solve
(
nums
):
2
n
=
max
(
nums
)
3
base
=
list
(
range
(1,
n
))
+
[
n
,
n
]
4
if
len
(
nums
)
!=
len
(
base
):
5
return
False
6
count_nums
=
{}
7
count_base
=
{}
8
for
num
in
nums
:
9
count_nums
[
num
]
=
count_nums
.
get
(
num
,
0)
+
1
10
for
num
in
base
:
11
count_base
[
num
]
=
count_base
.
get
(
num
,
0)
+
1
12
return
count_nums
==
count_base
(b)
Snippet 2
⬇
1
def
solve
(
nums
):
2
max_num
=
max
(
nums
)
3
n
=
max_num
4
expected_length
=
n
+
1
5
if
len
(
nums
)
!=
expected_length
:
6
return
False
7
count
=
{}
8
for
num
in
nums
:
9
if
num
!=
n
and
nums
.
count
(
num
)
!=
1:
10
return
False
11
if
num
==
n
and
nums
.
count
(
num
)
!=
2:
12
return
False
13
for
i
in
range
(1,
n
):
14
if
i
not
in
nums
:
15
return
False
16
return
True
(c)
Snippet 3
Figure 1
:
Three code snippets from the
DeepSeek-R1
[
15
]
, all correct, semantically equivalent.
We use problem
2892
from
LiveCodeBench
, where the task is to determine whether the given array is a “good” array or not.
An array is considered good if it is a permutation of an array base[n] where base[n] = [1, 2, …, n - 1, n, n] (in other words, it is an array of length n + 1 which contains 1 to n - 1 exactly once, plus two occurrences of n). For example, base[1] = [1, 1] and base[3] = [1, 2, 3, 3].
We sample three programs generated by
DeepSeek-R1
. Although they differ syntactically in their loop structures and placement of
if
statement guards, they are semantically equivalent and correctly solve the task.
Clustering with learned embeddings.
Despite this, semantic clustering using
DeBERTa
embeddings
[
16
]
(as used by Kuhn et al.
[
27
]
) and
OpenAI
’s
GPT
text-embedding-ada-002
embeddings (shown to outperform prior code embeddings like
code-search-babbage-001
and
code-search-ada-001
[
37
]
) fails to recognise their equivalence, placing each snippet in a separate cluster.
Clustering with
CodeBLEU
.
When applying
CodeBLEU
-based clustering, the similarity scores between snippets are low:
CodeBLEU
(Snippet
1(a)
, Snippet
1(b)
) =
0.49
times
0.49
absent
0.49\text{\,}
start_ARG 0.49 end_ARG start_ARG times end_ARG start_ARG end_ARG
,
CodeBLEU
(Snippet
1(a)
, Snippet
1(c)
) =
0.47
times
0.47
absent
0.47\text{\,}
start_ARG 0.47 end_ARG start_ARG times end_ARG start_ARG end_ARG
, and
CodeBLEU
(Snippet
1(b)
, Snippet
1(c)
) =
0.28
times
0.28
absent
0.28\text{\,}
start_ARG 0.28 end_ARG start_ARG times end_ARG start_ARG end_ARG
.
For context, heuristic thresholds in the range of 0.7-0.8 are often used to indicate high similarity.
As such,
CodeBLEU
fails to cluster these semantically equivalent programs, placing each in its own distinct cluster.
Symbolic clustering.
This highlights the need for a more principled approach. Symbolic execution
[
24
,
6
]
offers such a technique: it analyses programs by treating inputs as symbolic variables rather than concrete values.
As the program executes, it incrementally constructs symbolic expressions representing arithmetic computations and accumulates path constraints at conditional branches.
The result is a precise, algebraic characterisation of the program’s behaviour that uses symbolic expressions and logical formulas rather than actual values or executions.
By comparing the behaviour of the three snippets as captured by the symbolic input-output relations, we conclude that there are all semantically equivalent, meaning that they go into the same cluster.
Due to the symbolic value for the length of the input array
n
⁢
u
⁢
m
⁢
s
𝑛
𝑢
𝑚
𝑠
nums
italic_n italic_u italic_m italic_s
, which means that we don’t know how many times we need to unwind loops, we perform a bounded equivalence check as explained in Section
4
.
Impact of clustering on uncertainty estimation.
With symbolic clustering, which correctly groups all three snippets into the same cluster, the uncertainty scores reported by Kuhn et al.
[
27
]
and Abbasi et al.
[
3
]
are zero, as expected for semantically equivalent and correct outputs.
In contrast, all other clustering methods yield non-zero uncertainty. For instance, Kuhn et al. ’s method produces an uncertainty score of
1.49
times
1.49
absent
1.49\text{\,}
start_ARG 1.49 end_ARG start_ARG times end_ARG start_ARG end_ARG
when using the
GPT
text-embedding-ada-002
embeddings (which are also tailored for code
[
37
]
).
As a reference point, the abstention threshold for this method in our experimental evaluation is
0.82
times
0.82
absent
0.82\text{\,}
start_ARG 0.82 end_ARG start_ARG times end_ARG start_ARG end_ARG
(see Section
5.1
for how this threshold is derived), meaning that the model would incorrectly abstain from outputting any of these correct solutions.
We also experiment with replacing the model-derived probability distribution (e.g.,
0.48
times
0.48
absent
0.48\text{\,}
start_ARG 0.48 end_ARG start_ARG times end_ARG start_ARG end_ARG
,
0.29
times
0.29
absent
0.29\text{\,}
start_ARG 0.29 end_ARG start_ARG times end_ARG start_ARG end_ARG
,
0.23
times
0.23
absent
0.23\text{\,}
start_ARG 0.23 end_ARG start_ARG times end_ARG start_ARG end_ARG
for
DeepSeek-R1
) with a uniform distribution.
Even under this simplified setting, uncertainty estimates based on symbolic clustering remain zero, underscoring the symbolic clustering’s robustness to changes in the underlying probability distribution.
Symbolic cluster count.
Using the symbolic cluster count, which is 1 in this case, as all snippets fall into the same cluster, the abstention policy permits outputting the result, since the count is below the corresponding abstention threshold.
4
Estimating Uncertainty with Symbolic Clustering
In the domain of code generation, program equivalence has a precise definition: two programs are considered equivalent if they produce identical behaviour for all possible inputs.
Consequently, a domain-specific equivalence check is required.
In this paper, we base the semantic equivalence check on
symbolic execution
, where, instead of executing a program with concrete inputs,
symbolic variables
are used to represent inputs, generating constraints that describe the program’s behaviour across all possible input values
[
6
]
.
The particular flavor of symbolic execution we use in this work is inspired by the lightweight
peer architecture
described in Bruni et al.
[
5
]
.
Unlike traditional approaches that require building a standalone symbolic interpreter, this architecture embeds the symbolic execution engine as a lightweight library operating alongside the target program.
Their design is based on the insight that languages that provide the ability to dynamically dispatch primitive operations (e.g., Python) allow symbolic values to behave as native values and be tracked at runtime.
Symbolic execution typically traverses the program’s control flow graph, maintaining a symbolic state consisting of
path constraints
(i.e. logical conditions that must be satisfied for a given execution path to be feasible) and
symbolic expressions
(i.e. representations of program variables as functions of the symbolic inputs).
Algorithm 1
Symbolic Clustering
1:
Set of generated code snippets
{
s
(
1
)
,
…
,
s
(
M
)
}
superscript
𝑠
1
…
superscript
𝑠
𝑀
\{s^{(1)},\ldots,s^{(M)}\}
{ italic_s start_POSTSUPERSCRIPT ( 1 ) end_POSTSUPERSCRIPT , … , italic_s start_POSTSUPERSCRIPT ( italic_M ) end_POSTSUPERSCRIPT }
2:
Clusters of semantically equivalent snippets
C
=
{
c
1
,
c
2
,
…
,
c
k
}
𝐶
subscript
𝑐
1
subscript
𝑐
2
…
subscript
𝑐
𝑘
C=\{c_{1},c_{2},\ldots,c_{k}\}
italic_C = { italic_c start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_c start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT , … , italic_c start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT }
3:
Initialise an empty cluster set
C
←
∅
←
𝐶
C\leftarrow\emptyset
italic_C ← ∅
, and an equivalence map
E
←
∅
←
𝐸
E\leftarrow\emptyset
italic_E ← ∅
4:
for
each snippet
s
(
i
)
superscript
𝑠
𝑖
s^{(i)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT
do
5:
if
s
(
i
)
superscript
𝑠
𝑖
s^{(i)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT
is invalid
then
6:
E
⁢
[
s
(
i
)
]
←
{
s
(
i
)
}
←
𝐸
delimited-[]
superscript
𝑠
𝑖
superscript
𝑠
𝑖
E[s^{(i)}]\leftarrow\{\,s^{(i)}\}
italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ] ← { italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT }
▷
▷
\triangleright
▷
Assign invalid snippet to its own equivalence class
7:
end
if
8:
end
for
9:
for
each pair of valid snippets
(
s
(
i
)
,
s
(
j
)
)
superscript
𝑠
𝑖
superscript
𝑠
𝑗
(s^{(i)},s^{(j)})
( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT , italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT )
do
10:
Perform symbolic execution on
s
(
i
)
superscript
𝑠
𝑖
s^{(i)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT
and
s
(
j
)
superscript
𝑠
𝑗
s^{(j)}
italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT
to extract traces
T
⁢
(
s
(
i
)
)
𝑇
superscript
𝑠
𝑖
T(s^{(i)})
italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT )
and
T
⁢
(
s
(
j
)
)
𝑇
superscript
𝑠
𝑗
T(s^{(j)})
italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT )
11:
if
T
⁢
(
s
(
i
)
)
≡
T
⁢
(
s
(
j
)
)
𝑇
superscript
𝑠
𝑖
𝑇
superscript
𝑠
𝑗
T(s^{(i)})\equiv T(s^{(j)})
italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) ≡ italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT )
then
12:
E
⁢
[
s
(
i
)
]
←
E
⁢
[
s
(
i
)
]
∪
{
s
(
j
)
}
←
𝐸
delimited-[]
superscript
𝑠
𝑖
𝐸
delimited-[]
superscript
𝑠
𝑖
superscript
𝑠
𝑗
E[s^{(i)}]\leftarrow E[s^{(i)}]\cup\{\,s^{(j)}\}
italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ] ← italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ] ∪ { italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT }
13:
E
⁢
[
s
(
j
)
]
←
E
⁢
[
s
(
j
)
]
∪
{
s
(
i
)
}
←
𝐸
delimited-[]
superscript
𝑠
𝑗
𝐸
delimited-[]
superscript
𝑠
𝑗
superscript
𝑠
𝑖
E[s^{(j)}]\leftarrow E[s^{(j)}]\cup\{\,s^{(i)}\}
italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ] ← italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ] ∪ { italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT }
14:
end
if
15:
if
s
(
i
)
∼
s
(
j
)
similar-to
superscript
𝑠
𝑖
superscript
𝑠
𝑗
s^{(i)}\sim s^{(j)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ∼ italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT
and
s
(
j
)
∼
s
(
k
)
similar-to
superscript
𝑠
𝑗
superscript
𝑠
𝑘
s^{(j)}\sim s^{(k)}
italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ∼ italic_s start_POSTSUPERSCRIPT ( italic_k ) end_POSTSUPERSCRIPT
for some
s
(
k
)
superscript
𝑠
𝑘
s^{(k)}
italic_s start_POSTSUPERSCRIPT ( italic_k ) end_POSTSUPERSCRIPT
then
▷
▷
\triangleright
▷
Enforce transitivity of equivalences
16:
E
⁢
[
s
(
i
)
]
←
E
⁢
[
s
(
i
)
]
∪
{
s
(
k
)
}
←
𝐸
delimited-[]
superscript
𝑠
𝑖
𝐸
delimited-[]
superscript
𝑠
𝑖
superscript
𝑠
𝑘
E[s^{(i)}]\leftarrow E[s^{(i)}]\cup\{\,s^{(k)}\}
italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ] ← italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ] ∪ { italic_s start_POSTSUPERSCRIPT ( italic_k ) end_POSTSUPERSCRIPT }
17:
E
⁢
[
s
(
k
)
]
←
E
⁢
[
s
(
k
)
]
∪
{
s
(
i
)
}
←
𝐸
delimited-[]
superscript
𝑠
𝑘
𝐸
delimited-[]
superscript
𝑠
𝑘
superscript
𝑠
𝑖
E[s^{(k)}]\leftarrow E[s^{(k)}]\cup\{\,s^{(i)}\}
italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_k ) end_POSTSUPERSCRIPT ] ← italic_E [ italic_s start_POSTSUPERSCRIPT ( italic_k ) end_POSTSUPERSCRIPT ] ∪ { italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT }
18:
end
if
19:
end
for
20:
Identify equivalence classes in
E
𝐸
E
italic_E
to form final clusters
C
𝐶
C
italic_C
21:
return
C
𝐶
C
italic_C
Symbolic clustering.
Algorithm
1
illustrates how to cluster code snippets based on their functional semantics, with an additional check for invalid snippets.
We first create empty structures for storing the final clusters (
C
𝐶
C
italic_C
) and an equivalence map (
E
𝐸
E
italic_E
) to track relationships (line
3
).
Next, in the
invalid snippet handling phase
(line
4
), each code snippet
s
(
i
)
superscript
𝑠
𝑖
s^{(i)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT
is examined and, if it is detected to be syntactically invalid, it is immediately placed in its own equivalence class in
E
𝐸
E
italic_E
and thus isolated from further consideration.
In the
pairwise comparison phase
(line
9
), each pair of
valid
snippets
(
s
(
i
)
,
s
(
j
)
)
superscript
𝑠
𝑖
superscript
𝑠
𝑗
(s^{(i)},s^{(j)})
( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT , italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT )
is symbolically executed. For each snippet
s
(
i
)
superscript
𝑠
𝑖
s^{(i)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT
, symbolic execution produces a
set of traces
T
⁢
(
s
(
i
)
)
=
{
τ
1
,
τ
2
,
…
}
𝑇
superscript
𝑠
𝑖
subscript
𝜏
1
subscript
𝜏
2
…
T\bigl{(}s^{(i)}\bigr{)}\;=\;\bigl{\{}\tau_{1},\tau_{2},\dots\bigr{\}}
italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) = { italic_τ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_τ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT , … }
,
where each trace
τ
∈
T
⁢
(
s
(
i
)
)
𝜏
𝑇
superscript
𝑠
𝑖
\tau\in T(s^{(i)})
italic_τ ∈ italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT )
comprises of a path constraint, and a symbolic state, which encodes the expressions for all variables encountered along that path.
We declare two snippets
s
(
i
)
superscript
𝑠
𝑖
s^{(i)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT
and
s
(
j
)
superscript
𝑠
𝑗
s^{(j)}
italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT
semantically equivalent
exactly when their trace sets are the same (line
11
):
T
⁢
(
s
(
i
)
)
≡
T
⁢
(
s
(
j
)
)
𝑇
superscript
𝑠
𝑖
𝑇
superscript
𝑠
𝑗
T\bigl{(}s^{(i)}\bigr{)}\;\equiv\;T\bigl{(}s^{(j)}\bigr{)}
italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) ≡ italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT )
,
i.e. for
every
trace
τ
𝜏
\tau
italic_τ
in
T
⁢
(
s
(
i
)
)
𝑇
superscript
𝑠
𝑖
T(s^{(i)})
italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT )
, there is a matching trace in
T
⁢
(
s
(
j
)
)
𝑇
superscript
𝑠
𝑗
T(s^{(j)})
italic_T ( italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT )
and vice versa. Two traces
τ
1
subscript
𝜏
1
\tau_{1}
italic_τ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
and
τ
2
subscript
𝜏
2
\tau_{2}
italic_τ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
match if there is no counterexample input that leads to distinguishing output states for
τ
1
subscript
𝜏
1
\tau_{1}
italic_τ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
and
τ
2
subscript
𝜏
2
\tau_{2}
italic_τ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
. Since program equivalence is undecidable in general, we perform a bounded equivalence check, where we verify that no counterexample input exists when exploring traces up to a given depth.
If the snippets are semantically equivalent, we add each snippet to the other’s equivalence class (line
13
).
To maintain consistency, we also enforce transitivity: whenever
s
(
i
)
∼
s
(
j
)
similar-to
superscript
𝑠
𝑖
superscript
𝑠
𝑗
s^{(i)}\sim s^{(j)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ∼ italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT
and
s
(
j
)
∼
s
(
k
)
similar-to
superscript
𝑠
𝑗
superscript
𝑠
𝑘
s^{(j)}\sim s^{(k)}
italic_s start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ∼ italic_s start_POSTSUPERSCRIPT ( italic_k ) end_POSTSUPERSCRIPT
, we merge
s
(
i
)
superscript
𝑠
𝑖
s^{(i)}
italic_s start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT
and
s
(
k
)
superscript
𝑠
𝑘
s^{(k)}
italic_s start_POSTSUPERSCRIPT ( italic_k ) end_POSTSUPERSCRIPT
.
Finally, the equivalence map
E
𝐸
E
italic_E
is processed to extract the clusters themselves (line
20
), and the resulting set of clusters is returned (line
21
).
Uncertainty estimation for code generation.
The original NLG techniques by Kuhn et al.
[
27
]
and Abbasi et al.
[
3
]
involve sampling responses from an LLM, extracting token-level log-probabilities, and applying softmax-style normalization to interpret these as a probability distribution. However, in contrast to the original evaluations (where the outputs were typically short, one-word answers from question-answering datasets) code generation yields much longer responses. Since the probability of a response is computed as the joint probability of its tokens, it decays exponentially with length, often leading to
numerical underflow
. In such cases, the softmax normalisation can produce NaNs, rendering uncertainty estimates unusable.
To address this, we explore two strategies for approximating the output distribution of LLM responses. First, following prior work
[
36
,
26
,
34
]
, we normalise the log-probability of each program by its length, mitigating the bias against longer outputs and preventing underflow. Secondly, as a more radical simplification, we ignore log-probabilities altogether and assume a uniform distribution over the
n
𝑛
n
italic_n
sampled responses, assigning each a probability of
1
/
n
1
𝑛
1/n
1 / italic_n
.
Under this uniform-distribution simplification, we set
p
⁢
(
s
∣
x
)
=
1
n
𝑝
conditional
𝑠
𝑥
1
𝑛
p(s\mid x)=\frac{1}{n}
italic_p ( italic_s ∣ italic_x ) = divide start_ARG 1 end_ARG start_ARG italic_n end_ARG
and
p
⁢
(
c
∣
x
)
=
∑
s
∈
c
p
⁢
(
s
∣
x
)
=
|
c
|
n
𝑝
conditional
𝑐
𝑥
subscript
𝑠
𝑐
𝑝
conditional
𝑠
𝑥
𝑐
𝑛
p(c\mid x)=\sum_{s\in c}p(s\mid x)=\frac{|c|}{n}
italic_p ( italic_c ∣ italic_x ) = ∑ start_POSTSUBSCRIPT italic_s ∈ italic_c end_POSTSUBSCRIPT italic_p ( italic_s ∣ italic_x ) = divide start_ARG | italic_c | end_ARG start_ARG italic_n end_ARG
.
Hence the semantic entropy becomes
SE
uniform
⁢
(
x
)
=
−
∑
c
|
c
|
n
⁢
log
⁡
|
c
|
n
subscript
SE
uniform
𝑥
subscript
𝑐
𝑐
𝑛
𝑐
𝑛
\mathrm{SE}_{\mathrm{uniform}}(x)=-\sum_{c}\frac{|c|}{n}\,\log\!\frac{|c|}{n}
roman_SE start_POSTSUBSCRIPT roman_uniform end_POSTSUBSCRIPT ( italic_x ) = - ∑ start_POSTSUBSCRIPT italic_c end_POSTSUBSCRIPT divide start_ARG | italic_c | end_ARG start_ARG italic_n end_ARG roman_log divide start_ARG | italic_c | end_ARG start_ARG italic_n end_ARG
.
Likewise, the mutual information over
n
𝑛
n
italic_n
iterative responses simplifies to
I
uniform
⁢
(
x
)
=
∑
c
1
:
n
p
⁢
(
c
1
:
n
∣
x
)
⁢
log
⁡
p
~
⁢
(
c
1
:
n
∣
x
)
∏
i
=
1
n
p
i
⁢
(
c
i
∣
x
)
,
subscript
𝐼
uniform
𝑥
subscript
subscript
𝑐
:
1
𝑛
𝑝
conditional
subscript
𝑐
:
1
𝑛
𝑥
~
𝑝
conditional
subscript
𝑐
:
1
𝑛
𝑥
superscript
subscript
product
𝑖
1
𝑛
subscript
𝑝
𝑖
conditional
subscript
𝑐
𝑖
𝑥
I_{\mathrm{uniform}}(x)=\sum_{c_{1:n}}p(c_{1:n}\mid x)\log\frac{\displaystyle%
\tilde{p}(c_{1:n}\mid x)}{\displaystyle\prod_{i=1}^{n}p_{i}(c_{i}\mid x)},
italic_I start_POSTSUBSCRIPT roman_uniform end_POSTSUBSCRIPT ( italic_x ) = ∑ start_POSTSUBSCRIPT italic_c start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT end_POSTSUBSCRIPT italic_p ( italic_c start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x ) roman_log divide start_ARG over~ start_ARG italic_p end_ARG ( italic_c start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x ) end_ARG start_ARG ∏ start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( italic_c start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ∣ italic_x ) end_ARG ,
where
p
⁢
(
c
1
:
n
∣
x
)
=
∏
i
=
1
n
p
~
⁢
(
c
i
∣
F
i
−
1
⁢
(
x
,
c
1
:
i
−
1
)
)
=
∏
i
=
1
n
|
c
i
|
n
𝑝
conditional
subscript
𝑐
:
1
𝑛
𝑥
superscript
subscript
product
𝑖
1
𝑛
~
𝑝
conditional
subscript
𝑐
𝑖
subscript
𝐹
𝑖
1
𝑥
subscript
𝑐
:
1
𝑖
1
superscript
subscript
product
𝑖
1
𝑛
subscript
𝑐
𝑖
𝑛
p(c_{1:n}\mid x)=\prod_{i=1}^{n}\tilde{p}(c_{i}\mid F_{i-1}(x,\,c_{1:i-1}))=%
\prod_{i=1}^{n}\frac{|c_{i}|}{n}
italic_p ( italic_c start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x ) = ∏ start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT over~ start_ARG italic_p end_ARG ( italic_c start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ∣ italic_F start_POSTSUBSCRIPT italic_i - 1 end_POSTSUBSCRIPT ( italic_x , italic_c start_POSTSUBSCRIPT 1 : italic_i - 1 end_POSTSUBSCRIPT ) ) = ∏ start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT divide start_ARG | italic_c start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT | end_ARG start_ARG italic_n end_ARG
and
p
i
⁢
(
c
i
∣
x
)
=
∑
c
¬
i
p
~
⁢
(
c
1
:
n
∣
x
)
subscript
𝑝
𝑖
conditional
subscript
𝑐
𝑖
𝑥
subscript
subscript
𝑐
𝑖
~
𝑝
conditional
subscript
𝑐
:
1
𝑛
𝑥
p_{i}(c_{i}\mid x)=\sum_{c_{\neg i}}\tilde{p}(c_{1:n}\mid x)
italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( italic_c start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ∣ italic_x ) = ∑ start_POSTSUBSCRIPT italic_c start_POSTSUBSCRIPT ¬ italic_i end_POSTSUBSCRIPT end_POSTSUBSCRIPT over~ start_ARG italic_p end_ARG ( italic_c start_POSTSUBSCRIPT 1 : italic_n end_POSTSUBSCRIPT ∣ italic_x )
.
Interestingly, the uniform approximation performs comparably to the use of actual log-probabilities, reinforcing our central finding: semantic equivalence, not probabilistic confidence, is the dominant signal for estimating uncertainty in code generation.
Motivated by this, we propose a much simpler metric: the
symbolic cluster count
. Intuitively, a smaller number of distinct semantic outputs reflects higher model confidence. Despite its simplicity, this metric performs on par with more complex, information-theoretic approaches—provided the clustering is powered by symbolic execution.
The adaptations of the techniques by Kuhn et al. and Abbasi et al. to the code generation domain are detailed in Appendix Sections
A
and
B
, respectively.
5
Evaluation
LLM selection.
We selected the open-source model
DeepSeek-R1
[
15
]
as it represents the latest state-of-the-art among publicly available models. To complement this, we included
gpt-3.5-turbo-instruct
[
2
]
from
OpenAI
[
1
]
, the most recent
OpenAI
model that exposes token-level
logprobs
via its API, making it well-suited for evaluating information-theoretic uncertainty techniques. Finally, to evaluate methods that do not rely on log-probabilities, such as those assuming a uniform distribution or based on symbolic cluster counts, we also used
claude-3-7-sonnet
[
4
]
, a state-of-the-art proprietary model that does not expose log-probabilities.
Dataset selection.
We evaluate our techniques using
LiveCodeBench
[
20
]
, a contamination-free benchmark for code-related tasks comprising
831
times
831
absent
831\text{\,}
start_ARG 831 end_ARG start_ARG times end_ARG start_ARG end_ARG
problems, categorised as
Easy
(
239
times
239
absent
239\text{\,}
start_ARG 239 end_ARG start_ARG times end_ARG start_ARG end_ARG
),
Medium
(
332
times
332
absent
332\text{\,}
start_ARG 332 end_ARG start_ARG times end_ARG start_ARG end_ARG
), and
Hard
(
260
times
260
absent
260\text{\,}
start_ARG 260 end_ARG start_ARG times end_ARG start_ARG end_ARG
). Sourced from LeetCode, AtCoder, and CodeForces, each problem includes a natural language description and I/O test cases. We use the natural language description in the query provided to the LLM, and the test cases for evaluating our techniques, as detailed later in the section. Table
1
presents statistics describing the behaviour of the models evaluated in this study (
gpt-3.5-turbo-instruct
,
DeepSeek-R1
, and
claude-3-7-sonnet
) on
LiveCodeBench
.
Table 1
:
Solution statistics for
gpt-3.5-turbo-instruct
,
DeepSeek-R1
and
claude-3-7-sonnet
across various problem difficulty levels from
LiveCodeBench
.
Metric
gpt-3.5-turbo-instruct
DeepSeek-R1
claude-3-7-sonnet
Easy
Medium
Hard
Easy
Medium
Hard
Easy
Medium
Hard
Pass Rate
50
times
50
absent
50\text{\,}
start_ARG 50 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
30
times
30
absent
30\text{\,}
start_ARG 30 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
23
times
23
absent
23\text{\,}
start_ARG 23 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
84
times
84
absent
84\text{\,}
start_ARG 84 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
74
times
74
absent
74\text{\,}
start_ARG 74 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
52
times
52
absent
52\text{\,}
start_ARG 52 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
70
times
70
absent
70\text{\,}
start_ARG 70 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
61
times
61
absent
61\text{\,}
start_ARG 61 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
43
times
43
absent
43\text{\,}
start_ARG 43 end_ARG start_ARG times end_ARG start_ARG end_ARG
%
Average Lines of Code
13
times
13
absent
13\text{\,}
start_ARG 13 end_ARG start_ARG times end_ARG start_ARG end_ARG
20
times
20
absent
20\text{\,}
start_ARG 20 end_ARG start_ARG times end_ARG start_ARG end_ARG
22
times
22
absent
22\text{\,}
start_ARG 22 end_ARG start_ARG times end_ARG start_ARG end_ARG
12
times
12
absent
12\text{\,}
start_ARG 12 end_ARG start_ARG times end_ARG start_ARG end_ARG
29
times
29
absent
29\text{\,}
start_ARG 29 end_ARG start_ARG times end_ARG start_ARG end_ARG
36
times
36
absent
36\text{\,}
start_ARG 36 end_ARG start_ARG times end_ARG start_ARG end_ARG
12
times
12
absent
12\text{\,}
start_ARG 12 end_ARG start_ARG times end_ARG start_ARG end_ARG
31
times
31
absent
31\text{\,}
start_ARG 31 end_ARG start_ARG times end_ARG start_ARG end_ARG
38
times
38
absent
38\text{\,}
start_ARG 38 end_ARG start_ARG times end_ARG start_ARG end_ARG
Average Tokens
198
times
198
absent
198\text{\,}
start_ARG 198 end_ARG start_ARG times end_ARG start_ARG end_ARG
207
times
207
absent
207\text{\,}
start_ARG 207 end_ARG start_ARG times end_ARG start_ARG end_ARG
218
times
218
absent
218\text{\,}
start_ARG 218 end_ARG start_ARG times end_ARG start_ARG end_ARG
81
times
81
absent
81\text{\,}
start_ARG 81 end_ARG start_ARG times end_ARG start_ARG end_ARG
188
times
188
absent
188\text{\,}
start_ARG 188 end_ARG start_ARG times end_ARG start_ARG end_ARG
212
times
212
absent
212\text{\,}
start_ARG 212 end_ARG start_ARG times end_ARG start_ARG end_ARG
74
times
74
absent
74\text{\,}
start_ARG 74 end_ARG start_ARG times end_ARG start_ARG end_ARG
192
times
192
absent
192\text{\,}
start_ARG 192 end_ARG start_ARG times end_ARG start_ARG end_ARG
231
times
231
absent
231\text{\,}
start_ARG 231 end_ARG start_ARG times end_ARG start_ARG end_ARG
Experimental setup.
Our experiments were conducted on a machine running
Ubuntu 20.04.5 LTS (Focal Fossa)
with one
NVIDIA A100 GPU (80GB)
. For the approach based on Kuhn et al.
[
27
]
, we ask the LLM to generate
5
times
5
absent
5\text{\,}
start_ARG 5 end_ARG start_ARG times end_ARG start_ARG end_ARG
responses for each problem along with their respective
log-probabilities
. On top of that, for the approach based on Abbasi et al.
[
3
]
, we perform
2
times
2
absent
2\text{\,}
start_ARG 2 end_ARG start_ARG times end_ARG start_ARG end_ARG
iterations of prompting for each of the
5
times
5
absent
5\text{\,}
start_ARG 5 end_ARG start_ARG times end_ARG start_ARG end_ARG
generated responses.
The first iteration involves querying the model with the original prompt, while the second iteration uses a concatenated prompt, combining the original prompt and the response from the first iteration.
In order to perform symbolic execution for clustering, we use
Crosshair
[
7
]
with a per condition timeout of
5
s
times
5
s
5\text{\,}\mathrm{s}
start_ARG 5 end_ARG start_ARG times end_ARG start_ARG roman_s end_ARG
and the same per path timeout of
5
s
times
5
s
5\text{\,}\mathrm{s}
start_ARG 5 end_ARG start_ARG times end_ARG start_ARG roman_s end_ARG
.
In addition to this, we also impose an overall timeout of
10
s
times
10
s
10\text{\,}\mathrm{s}
start_ARG 10 end_ARG start_ARG times end_ARG start_ARG roman_s end_ARG
for each pair of programs that is being checked for equivalence.
If a counterexample showing the difference in behaviour is not found within this timeout, we assume that the programs belong in the same cluster.
We evaluate three main categories of techniques:
SE
—based on the semantic entropy method proposed by Kuhn et al.
[
27
,
14
]
;
MI
—based on the mutual information approach by Abbasi et al.
[
3
]
; and
CC
—the cluster count metric.
For
SE
and
MI
, we explore several variants depending on how semantic clustering is performed and how response probabilities are treated.
We use the following suffixes to distinguish them:
•
NLG
: the original implementation using natural language embeddings;
•
CodeEmbed
: using
GPT
text-embedding-ada-002
embeddings for clustering, which outperform prior code models like
code-search-babbage-001
and
code-search-ada-001
[
37
]
;
•
CodeBLEU
: using
CodeBLEU
for clustering;
•
Symb
: using symbolic clustering;
•
SymbUniform
: using symbolic clustering while assuming a uniform distribution over outputs.
For
CC
, we evaluate
CodeEmbed
and
Symb
, where
CC-Symb
is our proposed symbolic cluster count metric.
For each problem in the benchmark, we compute:
•
The corresponding
uncertainty score
for all the variants of
SE
and
MI
.
•
The
number of clusters
obtained for all variants of
CC
.
•
The
probablity of the top-ranked response
for
LLM-Probability
.
•
The
correctness score
, which is calculated as follows: the top-ranked response generated by the LLM (as determined by the API’s ranking) is executed against the benchmark’s test cases. The percentage of test cases successfully passed is recorded as the correctness score. A generous timeout of
5
s
times
5
s
5\text{\,}\mathrm{s}
start_ARG 5 end_ARG start_ARG times end_ARG start_ARG roman_s end_ARG
is applied to each test case. If the candidate solution exceeds this timeout, the test case is considered “failed”.
Results.
In Table
2
, we compute the Pearson correlation between the result computed by each of the techniques in the first column and the correctness scores (for a particular model and dataset).
We report the Pearson correlation coefficient and p-value, with statistically significant results highlighted. For
claude-3-7-sonnet
, which does not expose log-probabilities, the evaluation is limited to
SE-SymbUniform
and
CC-Symb
, and shown in Table
4
in Appendix.
Table 2
:
Correlation Results — Pearson coefficient (p-value) for
gpt-3.5-turbo-instruct
and
DeepSeek-R1
. Statistically significant results are highlighted in
bold
.
Technique
gpt-3.5-turbo-instruct
DeepSeek-R1
Easy
Medium
Hard
Easy
Medium
Hard
SE-NLG
−
0.04
times
-0.04
absent
-0.04\text{\,}
start_ARG - 0.04 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.5792
times
0.5792
absent
0.5792\text{\,}
start_ARG 0.5792 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.02
times
-0.02
absent
-0.02\text{\,}
start_ARG - 0.02 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.6520
times
0.6520
absent
0.6520\text{\,}
start_ARG 0.6520 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.01
times
-0.01
absent
-0.01\text{\,}
start_ARG - 0.01 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.2941
times
0.2941
absent
0.2941\text{\,}
start_ARG 0.2941 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.06
times
-0.06
absent
-0.06\text{\,}
start_ARG - 0.06 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.2762
times
0.2762
absent
0.2762\text{\,}
start_ARG 0.2762 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.06
times
-0.06
absent
-0.06\text{\,}
start_ARG - 0.06 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1651
times
0.1651
absent
0.1651\text{\,}
start_ARG 0.1651 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.08
times
-0.08
absent
-0.08\text{\,}
start_ARG - 0.08 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.9289
times
0.9289
absent
0.9289\text{\,}
start_ARG 0.9289 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
SE-CodeEmbed
−
0.10
times
-0.10
absent
-0.10\text{\,}
start_ARG - 0.10 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1083
times
0.1083
absent
0.1083\text{\,}
start_ARG 0.1083 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
0.07
times
0.07
absent
0.07\text{\,}
start_ARG 0.07 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1867
times
0.1867
absent
0.1867\text{\,}
start_ARG 0.1867 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.02
times
-0.02
absent
-0.02\text{\,}
start_ARG - 0.02 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1945
times
0.1945
absent
0.1945\text{\,}
start_ARG 0.1945 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.09
times
-0.09
absent
-0.09\text{\,}
start_ARG - 0.09 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1631
times
0.1631
absent
0.1631\text{\,}
start_ARG 0.1631 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.08
times
-0.08
absent
-0.08\text{\,}
start_ARG - 0.08 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1409
times
0.1409
absent
0.1409\text{\,}
start_ARG 0.1409 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.08
times
-0.08
absent
-0.08\text{\,}
start_ARG - 0.08 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1567
times
0.1567
absent
0.1567\text{\,}
start_ARG 0.1567 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
SE-CodeBLEU
−
0.21
times
-0.21
absent
-0.21\text{\,}
start_ARG - 0.21 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0892
times
0.0892
absent
0.0892\text{\,}
start_ARG 0.0892 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.18
times
-0.18
absent
-0.18\text{\,}
start_ARG - 0.18 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0945
times
0.0945
absent
0.0945\text{\,}
start_ARG 0.0945 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.17
times
-0.17
absent
-0.17\text{\,}
start_ARG - 0.17 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0888
times
0.0888
absent
0.0888\text{\,}
start_ARG 0.0888 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.13
times
-0.13
absent
-0.13\text{\,}
start_ARG - 0.13 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0512
times
0.0512
absent
0.0512\text{\,}
start_ARG 0.0512 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.11
times
-0.11
absent
-0.11\text{\,}
start_ARG - 0.11 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0904
times
0.0904
absent
0.0904\text{\,}
start_ARG 0.0904 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.10
times
-0.10
absent
-0.10\text{\,}
start_ARG - 0.10 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1256
times
0.1256
absent
0.1256\text{\,}
start_ARG 0.1256 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
SE-SymbNorm
−
0.56
times
-0.56
absent
-0.56\text{\,}
start_ARG - 0.56 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0001
times
0.0001
absent
0.0001\text{\,}
start_ARG 0.0001 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.52
times
-0.52
absent
-0.52\text{\,}
start_ARG - 0.52 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.49
times
-0.49
absent
-0.49\text{\,}
start_ARG - 0.49 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.45
times
-0.45
absent
-0.45\text{\,}
start_ARG - 0.45 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.40
times
-0.40
absent
-0.40\text{\,}
start_ARG - 0.40 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0001
times
0.0001
absent
0.0001\text{\,}
start_ARG 0.0001 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.41
times
-0.41
absent
-0.41\text{\,}
start_ARG - 0.41 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0008
times
0.0008
absent
0.0008\text{\,}
start_ARG 0.0008 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
SE-SymbUniform
−
0.51
times
-0.51
absent
-0.51\text{\,}
start_ARG - 0.51 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0001
times
0.0001
absent
0.0001\text{\,}
start_ARG 0.0001 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.48
times
-0.48
absent
-0.48\text{\,}
start_ARG - 0.48 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0001
times
0.0001
absent
0.0001\text{\,}
start_ARG 0.0001 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.47
times
-0.47
absent
-0.47\text{\,}
start_ARG - 0.47 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.45
times
-0.45
absent
-0.45\text{\,}
start_ARG - 0.45 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.41
times
-0.41
absent
-0.41\text{\,}
start_ARG - 0.41 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0001
times
0.0001
absent
0.0001\text{\,}
start_ARG 0.0001 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.40
times
-0.40
absent
-0.40\text{\,}
start_ARG - 0.40 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0007
times
0.0007
absent
0.0007\text{\,}
start_ARG 0.0007 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
MI-NLG
−
0.02
times
-0.02
absent
-0.02\text{\,}
start_ARG - 0.02 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.6353
times
0.6353
absent
0.6353\text{\,}
start_ARG 0.6353 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.04
times
-0.04
absent
-0.04\text{\,}
start_ARG - 0.04 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1828
times
0.1828
absent
0.1828\text{\,}
start_ARG 0.1828 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.07
times
-0.07
absent
-0.07\text{\,}
start_ARG - 0.07 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.4748
times
0.4748
absent
0.4748\text{\,}
start_ARG 0.4748 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.05
times
-0.05
absent
-0.05\text{\,}
start_ARG - 0.05 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.7674
times
0.7674
absent
0.7674\text{\,}
start_ARG 0.7674 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.04
times
-0.04
absent
-0.04\text{\,}
start_ARG - 0.04 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.8372
times
0.8372
absent
0.8372\text{\,}
start_ARG 0.8372 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.05
times
-0.05
absent
-0.05\text{\,}
start_ARG - 0.05 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.5365
times
0.5365
absent
0.5365\text{\,}
start_ARG 0.5365 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
MI-CodeEmbed
−
0.024
times
-0.024
absent
-0.024\text{\,}
start_ARG - 0.024 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.9123
times
0.9123
absent
0.9123\text{\,}
start_ARG 0.9123 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.056
times
-0.056
absent
-0.056\text{\,}
start_ARG - 0.056 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.7735
times
0.7735
absent
0.7735\text{\,}
start_ARG 0.7735 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.081
times
-0.081
absent
-0.081\text{\,}
start_ARG - 0.081 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.6744
times
0.6744
absent
0.6744\text{\,}
start_ARG 0.6744 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.09
times
-0.09
absent
-0.09\text{\,}
start_ARG - 0.09 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.3245
times
0.3245
absent
0.3245\text{\,}
start_ARG 0.3245 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.12
times
-0.12
absent
-0.12\text{\,}
start_ARG - 0.12 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.7823
times
0.7823
absent
0.7823\text{\,}
start_ARG 0.7823 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.02
times
-0.02
absent
-0.02\text{\,}
start_ARG - 0.02 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.5456
times
0.5456
absent
0.5456\text{\,}
start_ARG 0.5456 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
MI-CodeBLEU
−
0.12
times
-0.12
absent
-0.12\text{\,}
start_ARG - 0.12 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.7865
times
0.7865
absent
0.7865\text{\,}
start_ARG 0.7865 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.11
times
-0.11
absent
-0.11\text{\,}
start_ARG - 0.11 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.7698
times
0.7698
absent
0.7698\text{\,}
start_ARG 0.7698 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.08
times
-0.08
absent
-0.08\text{\,}
start_ARG - 0.08 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.8213
times
0.8213
absent
0.8213\text{\,}
start_ARG 0.8213 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.21
times
-0.21
absent
-0.21\text{\,}
start_ARG - 0.21 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.5443
times
0.5443
absent
0.5443\text{\,}
start_ARG 0.5443 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.17
times
-0.17
absent
-0.17\text{\,}
start_ARG - 0.17 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.5242
times
0.5242
absent
0.5242\text{\,}
start_ARG 0.5242 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.12
times
-0.12
absent
-0.12\text{\,}
start_ARG - 0.12 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.8728
times
0.8728
absent
0.8728\text{\,}
start_ARG 0.8728 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
MI-SymbNorm
−
0.22
times
-0.22
absent
-0.22\text{\,}
start_ARG - 0.22 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0292
times
0.0292
absent
0.0292\text{\,}
start_ARG 0.0292 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.24
times
-0.24
absent
-0.24\text{\,}
start_ARG - 0.24 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0132
times
0.0132
absent
0.0132\text{\,}
start_ARG 0.0132 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.19
times
-0.19
absent
-0.19\text{\,}
start_ARG - 0.19 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0145
times
0.0145
absent
0.0145\text{\,}
start_ARG 0.0145 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.37
times
-0.37
absent
-0.37\text{\,}
start_ARG - 0.37 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0261
times
0.0261
absent
0.0261\text{\,}
start_ARG 0.0261 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.38
times
-0.38
absent
-0.38\text{\,}
start_ARG - 0.38 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0121
times
0.0121
absent
0.0121\text{\,}
start_ARG 0.0121 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.33
times
-0.33
absent
-0.33\text{\,}
start_ARG - 0.33 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0187
times
0.0187
absent
0.0187\text{\,}
start_ARG 0.0187 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
MI-SymbUniform
−
0.21
times
-0.21
absent
-0.21\text{\,}
start_ARG - 0.21 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.18
times
-0.18
absent
-0.18\text{\,}
start_ARG - 0.18 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0004
times
0.0004
absent
0.0004\text{\,}
start_ARG 0.0004 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.19
times
-0.19
absent
-0.19\text{\,}
start_ARG - 0.19 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0008
times
0.0008
absent
0.0008\text{\,}
start_ARG 0.0008 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.33
times
-0.33
absent
-0.33\text{\,}
start_ARG - 0.33 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0001
times
0.0001
absent
0.0001\text{\,}
start_ARG 0.0001 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.34
times
-0.34
absent
-0.34\text{\,}
start_ARG - 0.34 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0004
times
0.0004
absent
0.0004\text{\,}
start_ARG 0.0004 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.32
times
-0.32
absent
-0.32\text{\,}
start_ARG - 0.32 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0003
times
0.0003
absent
0.0003\text{\,}
start_ARG 0.0003 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
CC-CodeEmbed
−
0.01
times
-0.01
absent
-0.01\text{\,}
start_ARG - 0.01 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.8385
times
0.8385
absent
0.8385\text{\,}
start_ARG 0.8385 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
0.05
times
0.05
absent
0.05\text{\,}
start_ARG 0.05 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.3076
times
0.3076
absent
0.3076\text{\,}
start_ARG 0.3076 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.08
times
-0.08
absent
-0.08\text{\,}
start_ARG - 0.08 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.2787
times
0.2787
absent
0.2787\text{\,}
start_ARG 0.2787 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.11
times
-0.11
absent
-0.11\text{\,}
start_ARG - 0.11 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.1060
times
0.1060
absent
0.1060\text{\,}
start_ARG 0.1060 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.02
times
-0.02
absent
-0.02\text{\,}
start_ARG - 0.02 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.6685
times
0.6685
absent
0.6685\text{\,}
start_ARG 0.6685 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.01
times
-0.01
absent
-0.01\text{\,}
start_ARG - 0.01 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.7844
times
0.7844
absent
0.7844\text{\,}
start_ARG 0.7844 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
CC-Symb
−
0.51
times
-0.51
absent
-0.51\text{\,}
start_ARG - 0.51 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.44
times
-0.44
absent
-0.44\text{\,}
start_ARG - 0.44 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0003
times
0.0003
absent
0.0003\text{\,}
start_ARG 0.0003 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.49
times
-0.49
absent
-0.49\text{\,}
start_ARG - 0.49 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0003
times
0.0003
absent
0.0003\text{\,}
start_ARG 0.0003 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.46
times
-0.46
absent
-0.46\text{\,}
start_ARG - 0.46 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0001
times
0.0001
absent
0.0001\text{\,}
start_ARG 0.0001 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.41
times
-0.41
absent
-0.41\text{\,}
start_ARG - 0.41 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.40
times
-0.40
absent
-0.40\text{\,}
start_ARG - 0.40 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0004
times
0.0004
absent
0.0004\text{\,}
start_ARG 0.0004 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
LLM-Probability
0.17
times
0.17
absent
0.17\text{\,}
start_ARG 0.17 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0200
times
0.0200
absent
0.0200\text{\,}
start_ARG 0.0200 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
0.11
times
0.11
absent
0.11\text{\,}
start_ARG 0.11 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.8236
times
0.8236
absent
0.8236\text{\,}
start_ARG 0.8236 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
0.09
times
0.09
absent
0.09\text{\,}
start_ARG 0.09 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.3838
times
0.3838
absent
0.3838\text{\,}
start_ARG 0.3838 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
0.18
times
0.18
absent
0.18\text{\,}
start_ARG 0.18 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.8221
times
0.8221
absent
0.8221\text{\,}
start_ARG 0.8221 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
0.11
times
0.11
absent
0.11\text{\,}
start_ARG 0.11 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.2762
times
0.2762
absent
0.2762\text{\,}
start_ARG 0.2762 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
0.13
times
0.13
absent
0.13\text{\,}
start_ARG 0.13 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.6353
times
0.6353
absent
0.6353\text{\,}
start_ARG 0.6353 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
5.1
Discussion of Results
Symbolic clustering enables NLG-based uncertainty estimation methods to perform effectively in code generation.
As shown in Table
2
, the
SE
and
MI
techniques fail to exhibit statistically significant correlation between estimated uncertainty and correctness when applied to code generation—even when adapted with OpenAI’s
GPT
text-embedding-ada-002
embeddings, which are tailored for code
[
37
]
or heuristic similarity metrics such as
CodeBLEU
. Notably, both techniques only achieve statistically significant correlation when paired with symbolic clustering (
SE-SymbNorm
,
SE-SymbUniform
,
MI-SymbNorm
, and
MI-SymbUniform
), highlighting the importance of precise semantic equivalence analysis in this domain.
Semantic equivalence among the LLM responses is a strong indicator of correctness.
When relying on log-probabilities computed by the LLM (row corresponding to
LLM-Probability
in Table
2
), we find no statistically significant correlation with correctness, indicating that token-level probabilities are insufficient proxies for correctness in code generation. In contrast, symbolic clustering provides a much stronger signal. Even when assuming a uniform distribution over LLM responses,
SE-SymbUniform
and
MI-SymbUniform
still yield a statistically significant correlation with correctness.
Lightweight metrics based on symbolic clustering can still yield effective correctness estimates.
Pushing this abstraction further,
CC-Symb
, which relies solely on the number of symbolic clusters, also correlates with correctness.
Crucially, this correlation hinges on the precision of clustering:
CC
-
CodeEmbed
doesn’t exhibit statistically significant results.
This result is particularly relevant because many modern LLMs do not expose reliable log-probabilities. For instance, it allows us to evaluate
CC-Symb
and
SE-SymbUniform
—methods that disregard the LLM log-probabilities— for
claude-3-7-sonnet
(results in Table
4
, Appendix), showing that both achieve a statistically significant correlation with correctness.
Our results hold across different models and different problem complexities.
Abstention policies.
We envision uncertainty scores being utilised as part of an abstention policy, similar to the approach described by Abbasi et al.
[
3
]
.
In this policy, an uncertainty threshold is set such that LLM responses with scores below the threshold are assumed to be functionally corrent, while those above the threshold are considered incorrect. For the latter, the LLM may abstain from presenting these responses to the user. LLM responses are classified as correct if their correctness score exceeds a predefined threshold and incorrect otherwise. We used a correctness score threshold of 90%. To determine the corresponding
uncertainty threshold
for the abstention policy, we select the value that maximises correctness accuracy.
We split the dataset 50/50 into training and validation.
To mitigate overfitting and reduce bias, we employed 2-fold cross-validation, alternating between training and validation for each fold.
For our experimental evaluation, we focus on the best-performing uncertainty estimation techniques—
SE-SymbNorm
,
SE-SymbUniform
, and
CC-Symb
—while using
SE-CodeEmbed
and
LLM-Probability
as baselines for comparison.
Table
3
shows that
SE-SymbNorm
,
SE-SymbUniform
, and
CC-Symb
, all using symbolic clustering, achieve high accuracy and extremely low false positive rates, i.e. the fraction of incorrect responses mistakenly shown to the user. This conservative acceptance of LLM outputs is crucial for code generation, where incorrect code poses safety risks.
False negative rates (i.e., correct responses unnecessarily filtered out) range from 11.9% to 20.3%, an acceptable trade-off for enhanced reliability.
SE-CodeEmbed
and
LLM-Probability
performed significantly worse across accuracy, false positive, and false negative rates, rendering them ineffective in practice. In particular,
SE-CodeEmbed
’s poor results highlight that simply replacing NLG-specific embeddings with code-specific ones is insufficient for adapting uncertainty estimation techniques to code generation and building effective abstention policies.
Table 3
:
Abstention metrics
Technique
gpt-3.5-turbo-instruct
DeepSeek-R1
Accuracy
False Pos.
False Neg.
Accuracy
False Pos.
False Neg.
SE-SymbNorm
81.2
%
times
81.2
percent
81.2\text{\,}\%
start_ARG 81.2 end_ARG start_ARG times end_ARG start_ARG % end_ARG
0.01
%
times
0.01
percent
0.01\text{\,}\%
start_ARG 0.01 end_ARG start_ARG times end_ARG start_ARG % end_ARG
17.5
%
times
17.5
percent
17.5\text{\,}\%
start_ARG 17.5 end_ARG start_ARG times end_ARG start_ARG % end_ARG
84.6
%
times
84.6
percent
84.6\text{\,}\%
start_ARG 84.6 end_ARG start_ARG times end_ARG start_ARG % end_ARG
0.01
%
times
0.01
percent
0.01\text{\,}\%
start_ARG 0.01 end_ARG start_ARG times end_ARG start_ARG % end_ARG
12.4
%
times
12.4
percent
12.4\text{\,}\%
start_ARG 12.4 end_ARG start_ARG times end_ARG start_ARG % end_ARG
SE-SymbUniform
77.8
%
times
77.8
percent
77.8\text{\,}\%
start_ARG 77.8 end_ARG start_ARG times end_ARG start_ARG % end_ARG
0.01
%
times
0.01
percent
0.01\text{\,}\%
start_ARG 0.01 end_ARG start_ARG times end_ARG start_ARG % end_ARG
20.3
%
times
20.3
percent
20.3\text{\,}\%
start_ARG 20.3 end_ARG start_ARG times end_ARG start_ARG % end_ARG
81.3
%
times
81.3
percent
81.3\text{\,}\%
start_ARG 81.3 end_ARG start_ARG times end_ARG start_ARG % end_ARG
0.01
%
times
0.01
percent
0.01\text{\,}\%
start_ARG 0.01 end_ARG start_ARG times end_ARG start_ARG % end_ARG
17.6
%
times
17.6
percent
17.6\text{\,}\%
start_ARG 17.6 end_ARG start_ARG times end_ARG start_ARG % end_ARG
CC-Symb
79.1
%
times
79.1
percent
79.1\text{\,}\%
start_ARG 79.1 end_ARG start_ARG times end_ARG start_ARG % end_ARG
0.02
%
times
0.02
percent
0.02\text{\,}\%
start_ARG 0.02 end_ARG start_ARG times end_ARG start_ARG % end_ARG
16.6
%
times
16.6
percent
16.6\text{\,}\%
start_ARG 16.6 end_ARG start_ARG times end_ARG start_ARG % end_ARG
83.1
%
times
83.1
percent
83.1\text{\,}\%
start_ARG 83.1 end_ARG start_ARG times end_ARG start_ARG % end_ARG
0.01
%
times
0.01
percent
0.01\text{\,}\%
start_ARG 0.01 end_ARG start_ARG times end_ARG start_ARG % end_ARG
11.9
%
times
11.9
percent
11.9\text{\,}\%
start_ARG 11.9 end_ARG start_ARG times end_ARG start_ARG % end_ARG
SE-CodeEmbed
58.2
%
times
58.2
percent
58.2\text{\,}\%
start_ARG 58.2 end_ARG start_ARG times end_ARG start_ARG % end_ARG
10.1
%
times
10.1
percent
10.1\text{\,}\%
start_ARG 10.1 end_ARG start_ARG times end_ARG start_ARG % end_ARG
24.5
%
times
24.5
percent
24.5\text{\,}\%
start_ARG 24.5 end_ARG start_ARG times end_ARG start_ARG % end_ARG
59.6
%
times
59.6
percent
59.6\text{\,}\%
start_ARG 59.6 end_ARG start_ARG times end_ARG start_ARG % end_ARG
11.2
%
times
11.2
percent
11.2\text{\,}\%
start_ARG 11.2 end_ARG start_ARG times end_ARG start_ARG % end_ARG
23.4
%
times
23.4
percent
23.4\text{\,}\%
start_ARG 23.4 end_ARG start_ARG times end_ARG start_ARG % end_ARG
LLM-Probability
36.5
%
times
36.5
percent
36.5\text{\,}\%
start_ARG 36.5 end_ARG start_ARG times end_ARG start_ARG % end_ARG
26.8
%
times
26.8
percent
26.8\text{\,}\%
start_ARG 26.8 end_ARG start_ARG times end_ARG start_ARG % end_ARG
37.3
%
times
37.3
percent
37.3\text{\,}\%
start_ARG 37.3 end_ARG start_ARG times end_ARG start_ARG % end_ARG
38.5
%
times
38.5
percent
38.5\text{\,}\%
start_ARG 38.5 end_ARG start_ARG times end_ARG start_ARG % end_ARG
21.4
%
times
21.4
percent
21.4\text{\,}\%
start_ARG 21.4 end_ARG start_ARG times end_ARG start_ARG % end_ARG
32.1
%
times
32.1
percent
32.1\text{\,}\%
start_ARG 32.1 end_ARG start_ARG times end_ARG start_ARG % end_ARG
Limitations.
A key limitation of our approach lies in the bounded nature of symbolic execution, particularly with respect to loops. To ensure tractability, we unroll loops and explore program paths only up to the timeout described in the experimental setup. While this enables efficient analysis, it introduces the risk of false positives in equivalence checking: two code snippets may be deemed semantically equivalent simply because their behavioural differences only manifest beyond the unrolling limit.
Another important limitation is that we only focus on the NLG-based uncertainty estimation techniques proposed by Kuhn et al.
[
27
,
14
]
and Abbasi et al.
[
3
]
. We mitigated this by selecting two recent state-of-the-art methods that have received significant attention and citations in the literature.
6
Related Work
Numerous approaches have been proposed for LLM evaluation in NLG. One class of methods involves training dedicated evaluators
[
49
,
48
]
or using proprietary LLMs such as ChatGPT
[
45
,
25
]
. However, these approaches are static, opaque, or biased
[
46
]
, and are outside the scope of our oracle-free setting.
Within NLG, oracle-free evaluation has leveraged both self-assessment
[
22
,
50
,
30
,
23
]
and internal signals—such as token-level log-probabilities—to estimate uncertainty
[
3
,
14
,
27
,
34
]
.
In this paper, we focus on the most recent state-of-the-art approaches based on entropy
[
14
,
27
]
and mutual information
[
3
]
, which have demonstrated strong performance in NLG.
Other techniques
[
28
,
10
,
35
,
38
,
8
,
51
,
18
,
23
]
are either shown to be less effective or rely on costly additional training steps. In another related work, Jiang et al.
[
21
]
show that naive log-likelihoods are weak correctness proxies.
While all the aforementioned works focus on natural language, most code generation studies rely on external oracles to assess the quality of LLM-generated code.
For example, works such as
[
32
]
and
[
44
]
conduct large-scale evaluations of LLM-generated code against existing correctness oracles. Similarly, Honarvar et al.
[
17
]
introduce a test suite expansion technique to generate additional code generation problems with oracles, enabling a more comprehensive evaluation of LLM performance.
Another closely related area is hallucination detection, where studies such as
[
31
]
and
[
11
]
focus on evaluating LLMs using problems specifically designed to expose inconsistencies and hallucinations.
Liu et al.
[
31
]
establish a taxonomy of hallucinations in LLM-generated code and propose a benchmark to evaluate the ability of code LLMs to recognise hallucinations.
Eghbali and Pradel
[
11
]
introduce a technique that grounds LLM predictions by retrieving relevant API references and iteratively refining prompts with increasingly relevant context, leading to more reliable LLM-generated code.
Closest to our work, Huang et al.
[
19
]
explore lightweight uncertainty proxies (e.g.,
CodeBLEU
) for code generation, but find them ineffective. Unlike prior work, we introduce symbolic clustering and propose metrics that show correlation with correctness—making us, to our knowledge, the first to identify effective oracle-free uncertainty estimators in code generation.
7
Conclusion
Our investigation reveals that existing uncertainty estimation techniques from natural language generation fail to generalise to code generation unless paired with precise semantic clustering. By introducing symbolic execution–based clustering, we restore the correlation between estimated uncertainty and correctness. This enables both more accurate uncertainty estimation and the definition of abstention policies with near-zero false positives. We further demonstrate that a simple symbolic cluster count offers a lightweight yet effective proxy for correctness, providing practical value even in settings where token-level probabilities are unavailable.
References
[1]
OpenAI.
https://openai.com
.
Accessed: January 19, 2025.
gpt [2023]
gpt-3.5-turbo-instruct.
https://platform.openai.com/docs/models/gpt-3-5
, 2023.
Accessed: January 19, 2025.
Abbasi-Yadkori et al. [2024]
Yasin Abbasi-Yadkori, Ilja Kuzborskij, András György, and Csaba
Szepesvari.
To believe or not to believe your llm: Iterative prompting for
estimating epistemic uncertainty.
In
The Thirty-eighth Annual Conference on Neural Information
Processing Systems
, 2024.
Anthropic [2023]
Anthropic.
Claude 3: A large language model.
https://www.anthropic.com/claude
, 2023.
Bruni et al. [2011]
Alessandro Maria Bruni, Tim Disney, and Cormac Flanagan.
A peer architecture for lightweight symbolic execution.
2011.
URL
https://api.semanticscholar.org/CorpusID:61565931
.
Cadar et al. [2008]
Cristian Cadar, Daniel Dunbar, and Dawson Engler.
Klee: unassisted and automatic generation of high-coverage tests for
complex systems programs.
In
Proceedings of the 8th USENIX Conference on Operating
Systems Design and Implementation
, OSDI’08, page 209–224, USA, 2008.
USENIX Association.
Chaney [2023]
Phillip S. Chaney.
Crosshair: A python analysis tool for exploring the correctness of
programs.
https://github.com/pschanely/CrossHair
, 2023.
Accessed: January 19, 2025.
Cole et al. [2023]
Jeremy R Cole, Michael JQ Zhang, Daniel Gillick, Julian Martin Eisenschlos,
Bhuwan Dhingra, and Jacob Eisenstein.
Selectively answering ambiguous questions.
arXiv preprint arXiv:2305.14613
, 2023.
David et al. [2025]
Cristina David, Pascal Kesseli, Daniel Kroening, and Hanliang Zhang.
Quantifying the benefits of code hints for refactoring deprecated
java apis.
In
Companion Proceedings of the 33rd ACM SIGSOFT International
Symposium on the Foundations of Software Engineering (FSE 2025 - Industry
Track)
, Trondheim, Norway, 2025. ACM.
Industry Track.
Desai and Durrett [2020]
Shrey Desai and Greg Durrett.
Calibration of pre-trained transformers.
arXiv preprint arXiv:2003.07892
, 2020.
Eghbali and Pradel [2024]
Aryaz Eghbali and Michael Pradel.
De-hallucinator: Iterative grounding for llm-based code completion.
arXiv preprint arXiv:2401.01701
, 2024.
Eniser et al. [2024]
Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Maria
Christakis, Brandon Paulsen, Joey Dodds, and Daniel Kroening.
Towards translating real-world code with llms: A study of translating
to rust.
arXiv preprint arXiv:2405.11514
, 2024.
Fan et al. [2023]
Zhiyu Fan, Xiang Gao, Martin Mirchev, Abhik Roychoudhury, and Shin Hwei Tan.
Automated repair of programs from large language models.
In
Proceedings of the 45th International Conference on Software
Engineering
, ICSE ’23, page 1469–1481. IEEE Press, 2023.
ISBN 9781665457019.
doi:
10.1109/ICSE48619.2023.00128
.
URL
https://doi.org/10.1109/ICSE48619.2023.00128
.
Farquhar et al. [2024]
Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and Yarin Gal.
Detecting hallucinations in large language models using semantic
entropy.
Nature
, 630(8017):625–630, 2024.
Guo et al. [2025]
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu,
Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al.
Deepseek-r1: Incentivizing reasoning capability in llms via
reinforcement learning.
arXiv preprint arXiv:2501.12948
, 2025.
He et al. [2020]
Pengcheng He, Xiaodong Liu, Jianfeng Gao, and Weizhu Chen.
Deberta: Decoding-enhanced bert with disentangled attention.
arXiv preprint arXiv:2006.03654
, 2020.
Honarvar et al. [2024]
Shahin Honarvar, Mark van der Wilk, and Alastair Donaldson.
Turbulence: Systematically and automatically testing
instruction-tuned large language models for code, 2024.
URL
https://arxiv.org/abs/2312.14856
.
Hou et al. [2023]
Bairu Hou, Yujian Liu, Kaizhi Qian, Jacob Andreas, Shiyu Chang, and Yang Zhang.
Decomposing uncertainty for large language models through input
clarification ensembling.
arXiv preprint arXiv:2311.08718
, 2023.
Huang et al. [2025]
Yuheng Huang, Jiayang Song, Zhijie Wang, Shengming Zhao, Huaming Chen, Felix
Juefei-Xu, and Lei Ma.
Look before you leap: An exploratory study of uncertainty analysis
for large language models.
IEEE Transactions on Software Engineering
, 2025.
Jain et al. [2024]
Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida
Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
Livecodebench: Holistic and contamination free evaluation of large
language models for code, 2024.
URL
https://arxiv.org/abs/2403.07974
.
Jiang et al. [2021]
Zhengbao Jiang, Jun Araki, Haibo Ding, and Graham Neubig.
How can we know when language models know? on the calibration of
language models for question answering.
Transactions of the Association for Computational Linguistics
,
9:962–977, 2021.
Johnson et al. [2024]
Daniel D. Johnson, Daniel Tarlow, David Duvenaud, and Chris J. Maddison.
Experts don’t cheat: Learning what you don’t know by predicting
pairs.
In
Forty-first International Conference on Machine Learning,
ICML 2024, Vienna, Austria, July 21-27, 2024
. OpenReview.net, 2024.
URL
https://openreview.net/forum?id=AVEc9LvSlO
.
Kadavath et al. [2022]
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan
Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli
Tran-Johnson, Scott Johnston, Sheer El Showk, Andy Jones, Nelson Elhage,
Tristan Hume, Anna Chen, Yuntao Bai, Sam Bowman, Stanislav Fort, Deep
Ganguli, Danny Hernandez, Josh Jacobson, Jackson Kernion, Shauna Kravec,
Liane Lovitt, Kamal Ndousse, Catherine Olsson, Sam Ringer, Dario Amodei, Tom
Brown, Jack Clark, Nicholas Joseph, Ben Mann, Sam McCandlish, Chris Olah, and
Jared Kaplan.
Language models (mostly) know what they know.
CoRR
, abs/2207.05221, 2022.
doi:
10.48550/ARXIV.2207.05221
.
URL
https://doi.org/10.48550/arXiv.2207.05221
.
King [1976]
James C. King.
Symbolic execution and program testing.
Commun. ACM
, 19(7):385–394, July 1976.
ISSN 0001-0782.
doi:
10.1145/360248.360252
.
URL
https://doi.org/10.1145/360248.360252
.
Kocmi and Federmann [2023]
Tom Kocmi and Christian Federmann.
Large language models are state-of-the-art evaluators of translation
quality.
In Mary Nurminen, Judith Brenner, Maarit Koponen, Sirkku Latomaa,
Mikhail Mikhailov, Frederike Schierl, Tharindu Ranasinghe, Eva Vanmassenhove,
Sergi Alvarez Vidal, Nora Aranberri, Mara Nunziatini, Carla Parra
Escartín, Mikel L. Forcada, Maja Popovic, Carolina Scarton, and Helena
Moniz, editors,
Proceedings of the 24th Annual Conference of the
European Association for Machine Translation, EAMT 2023, Tampere, Finland,
12-15 June 2023
, pages 193–203. European Association for Machine
Translation, 2023.
URL
https://aclanthology.org/2023.eamt-1.19
.
Koehn and Knowles [2017]
Philipp Koehn and Rebecca Knowles.
Six challenges for neural machine translation.
In Thang Luong, Alexandra Birch, Graham Neubig, and Andrew M. Finch,
editors,
Proceedings of the First Workshop on Neural Machine
Translation, NMT@ACL 2017, Vancouver, Canada, August 4, 2017
, pages 28–39.
Association for Computational Linguistics, 2017.
doi:
10.18653/V1/W17-3204
.
URL
https://doi.org/10.18653/v1/w17-3204
.
Kuhn et al. [2023]
Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar.
Semantic uncertainty: Linguistic invariances for uncertainty
estimation in natural language generation.
In
The Eleventh International Conference on Learning
Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023
. OpenReview.net,
2023.
URL
https://openreview.net/forum?id=VD-AYtP0dve
.
Lahlou et al. [2021]
Salem Lahlou, Moksh Jain, Hadi Nekoei, Victor Ion Butoi, Paul Bertin, Jarrid
Rector-Brooks, Maksym Korablyov, and Yoshua Bengio.
Deup: Direct epistemic uncertainty prediction.
arXiv preprint arXiv:2102.08501
, 2021.
Li et al. [2024]
Yixuan Li, Julian Parsert, and Elizabeth Polgreen.
Guiding enumerative program synthesis with large language models.
In
International Conference on Computer Aided Verification
,
pages 280–301. Springer, 2024.
Lin et al. [2022]
Stephanie Lin, Jacob Hilton, and Owain Evans.
Teaching models to express their uncertainty in words.
Trans. Mach. Learn. Res.
, 2022, 2022.
URL
https://openreview.net/forum?id=8s8K2UZGTZ
.
Liu et al. [2024a]
Fang Liu, Yang Liu, Lin Shi, Houkun Huang, Ruifeng Wang, Zhen Yang, Li Zhang,
Zhongqi Li, and Yuchi Ma.
Exploring and evaluating hallucinations in llm-powered code
generation.
arXiv preprint arXiv:2404.00971
, 2024a.
Liu et al. [2024b]
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang.
Is your code generated by chatgpt really correct? rigorous evaluation
of large language models for code generation.
Advances in Neural Information Processing Systems
, 36,
2024b.
Luo et al. [2024]
Yang Luo, Richard Yu, Fajun Zhang, Ling Liang, and Yongqiang Xiong.
Bridging gaps in llm code translation: Reducing errors with call
graphs and bridged debuggers.
In
Proceedings of the 39th IEEE/ACM International Conference on
Automated Software Engineering
, pages 2448–2449, 2024.
Malinin and Gales [2021]
Andrey Malinin and Mark J. F. Gales.
Uncertainty estimation in autoregressive structured prediction.
In
9th International Conference on Learning Representations,
ICLR 2021, Virtual Event, Austria, May 3-7, 2021
. OpenReview.net, 2021.
URL
https://openreview.net/forum?id=jN5y-zb5Q7m
.
Mielke et al. [2022]
Sabrina J Mielke, Arthur Szlam, Emily Dinan, and Y-Lan Boureau.
Reducing conversational agents’ overconfidence through linguistic
calibration.
Transactions of the Association for Computational Linguistics
,
10:857–872, 2022.
Murray and Chiang [2018]
Kenton Murray and David Chiang.
Correcting length bias in neural machine translation.
In Ondrej Bojar, Rajen Chatterjee, Christian Federmann, Mark Fishel,
Yvette Graham, Barry Haddow, Matthias Huck, Antonio Jimeno-Yepes, Philipp
Koehn, Christof Monz, Matteo Negri, Aurélie Névéol,
Mariana L. Neves, Matt Post, Lucia Specia, Marco Turchi, and Karin Verspoor,
editors,
Proceedings of the Third Conference on Machine Translation:
Research Papers, WMT 2018, Belgium, Brussels, October 31 - November 1,
2018
, pages 212–223. Association for Computational Linguistics, 2018.
doi:
10.18653/V1/W18-6322
.
URL
https://doi.org/10.18653/v1/w18-6322
.
OpenAI [2022]
OpenAI.
New and improved embedding model.
https://openai.com/index/new-and-improved-embedding-model/
,
December 2022.
Accessed: 2025-05-13.
Osband et al. [2023]
Ian Osband, Zheng Wen, Seyed Mohammad Asghari, Vikranth Dwaracherla, Morteza
Ibrahimi, Xiuyuan Lu, and Benjamin Van Roy.
Epistemic neural networks.
Advances in Neural Information Processing Systems
,
36:2795–2823, 2023.
Pan et al. [2024]
Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lambert Pouguem
Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh Sinha, and
Reyhaneh Jabbarvand.
Lost in translation: A study of bugs introduced by large language
models while translating code.
In
Proceedings of the IEEE/ACM 46th International Conference on
Software Engineering
, pages 1–13, 2024.
Pomian et al. [2024]
Dorin Pomian, Abhiram Bellur, Malinda Dilhara, Zarina Kurbatova, Egor
Bogomolov, Timofey Bryksin, and Danny Dig.
Next-generation refactoring: Combining llm insights and ide
capabilities for extract method.
In
2024 IEEE International Conference on Software Maintenance
and Evolution (ICSME)
, pages 275–287. IEEE, 2024.
Ren et al. [2020]
Shuo Ren, Daya Guo, Shuai Lu, Long Zhou, Shujie Liu, Duyu Tang, Neel
Sundaresan, Ming Zhou, Ambrosio Blanco, and Shuai Ma.
Codebleu: a method for automatic evaluation of code synthesis.
CoRR
, abs/2009.10297, 2020.
URL
https://arxiv.org/abs/2009.10297
.
Shirafuji et al. [2023]
Atsushi Shirafuji, Yusuke Oda, Jun Suzuki, Makoto Morishita, and Yutaka
Watanobe.
Refactoring programs using large language models with few-shot
examples.
In
2023 30th Asia-Pacific Software Engineering Conference
(APSEC)
, pages 151–160. IEEE, 2023.
Tao et al. [2024]
Ning Tao, Anthony Ventresque, Vivek Nallur, and Takfarinas Saber.
Enhancing program synthesis with large language models using
many-objective grammar-guided genetic programming.
Algorithms
, 17(7):287, 2024.
Vaithilingam et al. [2022]
Priyan Vaithilingam, Tianyi Zhang, and Elena L Glassman.
Expectation vs. experience: Evaluating the usability of code
generation tools powered by large language models.
In
Chi conference on human factors in computing systems
extended abstracts
, pages 1–7, 2022.
Wang et al. [2023a]
Jiaan Wang, Yunlong Liang, Fandong Meng, Haoxiang Shi, Zhixu Li, Jinan Xu,
Jianfeng Qu, and Jie Zhou.
Is chatgpt a good NLG evaluator? A preliminary study.
CoRR
, abs/2303.04048, 2023a.
doi:
10.48550/ARXIV.2303.04048
.
URL
https://doi.org/10.48550/arXiv.2303.04048
.
Wang et al. [2024]
Peiyi Wang, Lei Li, Liang Chen, Zefan Cai, Dawei Zhu, Binghuai Lin, Yunbo Cao,
Lingpeng Kong, Qi Liu, Tianyu Liu, and Zhifang Sui.
Large language models are not fair evaluators.
In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors,
Proceedings of the 62nd Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok,
Thailand, August 11-16, 2024
, pages 9440–9450. Association for
Computational Linguistics, 2024.
doi:
10.18653/V1/2024.ACL-LONG.511
.
URL
https://doi.org/10.18653/v1/2024.acl-long.511
.
Wang et al. [2023b]
Shangwen Wang, Mingyang Geng, Bo Lin, Zhensu Sun, Ming Wen, Yepang Liu, Li Li,
Tegawendé F. Bissyandé, and Xiaoguang Mao.
Natural language to code: How far are we?
In
Proceedings of the 31st ACM Joint European Software
Engineering Conference and Symposium on the Foundations of Software
Engineering
, ESEC/FSE 2023, page 375–387, New York, NY, USA,
2023b. Association for Computing Machinery.
ISBN 9798400703270.
doi:
10.1145/3611643.3616323
.
URL
https://doi.org/10.1145/3611643.3616323
.
Wang et al. [2023c]
Tianlu Wang, Ping Yu, Xiaoqing Ellen Tan, Sean O’Brien, Ramakanth Pasunuru,
Jane Dwivedi-Yu, Olga Golovneva, Luke Zettlemoyer, Maryam Fazel-Zarandi,
and Asli Celikyilmaz.
Shepherd: A critic for language model generation.
CoRR
, abs/2308.04592, 2023c.
doi:
10.48550/ARXIV.2308.04592
.
URL
https://doi.org/10.48550/arXiv.2308.04592
.
Wang et al. [2023d]
Yidong Wang, Zhuohao Yu, Zhengran Zeng, Linyi Yang, Cunxiang Wang, Hao Chen,
Chaoya Jiang, Rui Xie, Jindong Wang, Xing Xie, Wei Ye, Shikun Zhang, and Yue
Zhang.
Pandalm: An automatic evaluation benchmark for LLM instruction
tuning optimization.
CoRR
, abs/2306.05087, 2023d.
doi:
10.48550/ARXIV.2306.05087
.
URL
https://doi.org/10.48550/arXiv.2306.05087
.
Xia et al. [2024]
Tingyu Xia, Bowen Yu, Yuan Wu, Yi Chang, and Chang Zhou.
Language models can evaluate themselves via probability discrepancy.
In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors,
Findings of the Association for Computational Linguistics, ACL 2024,
Bangkok, Thailand and virtual meeting, August 11-16, 2024
, pages 4889–4901.
Association for Computational Linguistics, 2024.
doi:
10.18653/V1/2024.FINDINGS-ACL.291
.
URL
https://doi.org/10.18653/v1/2024.findings-acl.291
.
Yona et al. [2024]
Gal Yona, Roee Aharoni, and Mor Geva.
Narrowing the knowledge evaluation gap: Open-domain question
answering with multi-granularity answers.
arXiv preprint arXiv:2401.04695
, 2024.
Zhang et al. [2025]
Hanliang Zhang, Cristina David, Wang Meng, Brandon Paulsen, and Daniel
Kroening.
Scalable, validated code translation of entire projects using large
language models.
Programming Language Design and Implementation (PLDI)
, 2025.
Zhang et al. [2024]
Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury.
Autocoderover: Autonomous program improvement.
In
Proceedings of the 33rd ACM SIGSOFT International Symposium
on Software Testing and Analysis
, ISSTA 2024, page 1592–1604, New York,
NY, USA, 2024. Association for Computing Machinery.
ISBN 9798400706127.
doi:
10.1145/3650212.3680384
.
URL
https://doi.org/10.1145/3650212.3680384
.
Appendix A
Semantic Uncertainty via Symbolic Clustering
This section presents our adaptation of the semantic entropy-based approach by Kuhn et al.
[
27
]
for code generation.
We follow the main steps from the original work while diverging in two key aspects: the way we estimate the distribution of generated LLM responses and the clustering methodology.
A.0.1
Generation
The first step involves sampling
M
𝑀
M
italic_M
code snippets (using the same hyperparameters as Kuhn et al.
[
27
]
),
{
s
(
1
)
,
…
,
s
(
M
)
}
superscript
𝑠
1
…
superscript
𝑠
𝑀
\{s^{(1)},\ldots,s^{(M)}\}
{ italic_s start_POSTSUPERSCRIPT ( 1 ) end_POSTSUPERSCRIPT , … , italic_s start_POSTSUPERSCRIPT ( italic_M ) end_POSTSUPERSCRIPT }
, from the LLM’s output distribution
p
⁢
(
s
∣
x
)
𝑝
conditional
𝑠
𝑥
p(s\mid x)
italic_p ( italic_s ∣ italic_x )
for a given prompt
x
𝑥
x
italic_x
.
The probabilities of the collected samples are processed using a softmax-style normalization function, ensuring that the resulting values can be interpreted as a valid probability distribution.
Given that this process can lead to numerical underflows, to mitigate this, we approximate the probability distribution of the LLM responses using either length-normalization or a uniform distribution.
Following this approximation, let
p
~
⁢
(
s
∣
x
)
~
𝑝
conditional
𝑠
𝑥
\tilde{p}(s\mid x)
over~ start_ARG italic_p end_ARG ( italic_s ∣ italic_x )
denote the probability of a snippet
s
𝑠
s
italic_s
according to the adjusted distribution.
A.0.2
Clustering via Symbolic Execution
The second step works by grouping the aforementioned snippets into clusters based on semantic equivalence. This process, as shown in Algorithm
1
from Section
4
, is based on symbolic execution.
A.0.3
Entropy Estimation
The final step computes uncertainty as the semantic entropy over clusters, reflecting the diversity of functional behaviours.
First, the probability associated with a cluster
c
𝑐
c
italic_c
is calculated as:
p
~
⁢
(
c
∣
x
)
=
∑
s
∈
c
p
~
⁢
(
s
∣
x
)
,
~
𝑝
conditional
𝑐
𝑥
subscript
𝑠
𝑐
~
𝑝
conditional
𝑠
𝑥
\tilde{p}(c\mid x)=\sum_{s\in c}\tilde{p}(s\mid x),
over~ start_ARG italic_p end_ARG ( italic_c ∣ italic_x ) = ∑ start_POSTSUBSCRIPT italic_s ∈ italic_c end_POSTSUBSCRIPT over~ start_ARG italic_p end_ARG ( italic_s ∣ italic_x ) ,
where
s
∈
c
𝑠
𝑐
s\in c
italic_s ∈ italic_c
indicates that the snippet
s
𝑠
s
italic_s
belongs to the cluster
c
𝑐
c
italic_c
.
Then, the entropy
H
⁢
(
C
∣
x
)
𝐻
conditional
𝐶
𝑥
H(C\mid x)
italic_H ( italic_C ∣ italic_x )
over the set of clusters
C
𝐶
C
italic_C
is defined as:
H
⁢
(
C
∣
x
)
=
−
∑
c
∈
C
log
⁡
p
~
⁢
(
c
∣
x
)
,
𝐻
conditional
𝐶
𝑥
subscript
𝑐
𝐶
~
𝑝
conditional
𝑐
𝑥
H(C\mid x)=-\sum_{c\in C}\log\tilde{p}(c\mid x),
italic_H ( italic_C ∣ italic_x ) = - ∑ start_POSTSUBSCRIPT italic_c ∈ italic_C end_POSTSUBSCRIPT roman_log over~ start_ARG italic_p end_ARG ( italic_c ∣ italic_x ) ,
where
C
𝐶
C
italic_C
denotes all semantic clusters obtained from Algorithm
1
in Section
4
.
A higher entropy indicates greater semantic diversity and hence higher uncertainty in the functional behaviour captured by the clusters.
Conversely, a lower entropy suggests that the model’s outputs are concentrated around a few semantically equivalent behaviours, reflecting higher confidence.
Appendix B
Mutual Information Estimation via Symbolic Clustering
This section presents an adaptation of the mutual information-based approach for quantifying epistemic uncertainty by Abbasi et al.
[
3
]
to the domain of code generation.
We follow the steps from the original work: iterative prompting for generating LLM responses, clustering, and mutual information estimation.
However, similar to Section
A
, we diverge with respect to the methodology for clustering responses and the way we estimate the distribution of generated LLM responses.
B.0.1
Iterative Prompting for Code Generation
Iterative prompting is used for generating multiple responses from the LLM and consequently in constructing a pseudo joint distribution of outputs.
More precisely, the LLM is sampled to produce
n
𝑛
n
italic_n
responses while also getting their respective probabilities,
μ
⁢
(
X
j
)
𝜇
subscript
𝑋
𝑗
\mu(X_{j})
italic_μ ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT )
for
j
=
1
,
2
,
…
,
n
𝑗
1
2
…
𝑛
j=1,2,\ldots,n
italic_j = 1 , 2 , … , italic_n
.
These responses are first used to construct iterative prompts by appending the response to the original prompt and asking the LLM to produce more responses.
This step then makes use of softmax-style normalization to obtain values that can then be treated as probabilities which are used in the subsequent steps.
As before since this process can lead to numerical underflows, to mitigate this, we use length-normalization.
As opposed to the approach in Section
A
, here we did not use the uniform distribution approximation, as the actual LLM-reported probabilities are needed to distinguish between aleatoric and epistemic uncertainties.
Following length normalization, we compute conditional probabilities,
μ
⁢
(
X
m
|
X
n
)
𝜇
conditional
subscript
𝑋
𝑚
subscript
𝑋
𝑛
\mu(X_{m}|X_{n})
italic_μ ( italic_X start_POSTSUBSCRIPT italic_m end_POSTSUBSCRIPT | italic_X start_POSTSUBSCRIPT italic_n end_POSTSUBSCRIPT )
for
m
,
n
=
1
,
2
,
…
,
n
formulae-sequence
𝑚
𝑛
1
2
…
𝑛
m,n=1,2,\ldots,n
italic_m , italic_n = 1 , 2 , … , italic_n
, by looking at the response probabilities received from the LLM when subjected to the aforementioned iterative prompts.
B.0.2
Clustering via Symbolic Execution
To handle functional diversity, the generated program snippets are clustered based on their semantic equivalence using Algorithm
1
.
B.0.3
Mutual Information Estimation
Once clustering is complete, mutual information is computed over the resulting clusters to quantify epistemic uncertainty.
The aggregated probabilities are defined as:
μ
1
′
⁢
(
X
i
)
=
∑
j
∈
D
⁢
(
i
)
μ
⁢
(
X
j
)
,
μ
2
′
⁢
(
X
t
∣
X
i
)
=
∑
j
∈
D
⁢
(
t
)
μ
⁢
(
X
j
∣
X
i
)
,
formulae-sequence
superscript
subscript
𝜇
1
′
subscript
𝑋
𝑖
subscript
𝑗
𝐷
𝑖
𝜇
subscript
𝑋
𝑗
superscript
subscript
𝜇
2
′
conditional
subscript
𝑋
𝑡
subscript
𝑋
𝑖
subscript
𝑗
𝐷
𝑡
𝜇
conditional
subscript
𝑋
𝑗
subscript
𝑋
𝑖
\mu_{1}^{\prime}(X_{i})=\sum_{j\in D(i)}\mu(X_{j}),\quad\mu_{2}^{\prime}(X_{t}%
\mid X_{i})=\sum_{j\in D(t)}\mu(X_{j}\mid X_{i}),
italic_μ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) = ∑ start_POSTSUBSCRIPT italic_j ∈ italic_D ( italic_i ) end_POSTSUBSCRIPT italic_μ ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT ) , italic_μ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) = ∑ start_POSTSUBSCRIPT italic_j ∈ italic_D ( italic_t ) end_POSTSUBSCRIPT italic_μ ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) ,
where
X
i
subscript
𝑋
𝑖
X_{i}
italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
and
X
t
subscript
𝑋
𝑡
X_{t}
italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT
are clusters,
μ
⁢
(
X
j
)
𝜇
subscript
𝑋
𝑗
\mu(X_{j})
italic_μ ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT )
represents the probability of the output
X
j
subscript
𝑋
𝑗
X_{j}
italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT
, and
μ
⁢
(
X
j
∣
X
i
)
𝜇
conditional
subscript
𝑋
𝑗
subscript
𝑋
𝑖
\mu(X_{j}\mid X_{i})
italic_μ ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT )
is the conditional probability of
X
j
subscript
𝑋
𝑗
X_{j}
italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT
given
X
i
subscript
𝑋
𝑖
X_{i}
italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
. The set
D
⁢
(
i
)
𝐷
𝑖
D(i)
italic_D ( italic_i )
contains all outputs assigned to the cluster
X
i
subscript
𝑋
𝑖
X_{i}
italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
.
The normalised empirical distributions are:
μ
^
1
⁢
(
X
i
)
=
μ
1
′
⁢
(
X
i
)
Z
,
where
Z
=
∑
j
∈
S
μ
1
′
⁢
(
X
j
)
,
formulae-sequence
subscript
^
𝜇
1
subscript
𝑋
𝑖
superscript
subscript
𝜇
1
′
subscript
𝑋
𝑖
𝑍
where
𝑍
subscript
𝑗
𝑆
superscript
subscript
𝜇
1
′
subscript
𝑋
𝑗
\hat{\mu}_{1}(X_{i})=\frac{\mu_{1}^{\prime}(X_{i})}{Z},\quad\text{where}\quad Z%
=\sum_{j\in S}\mu_{1}^{\prime}(X_{j}),
over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) = divide start_ARG italic_μ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) end_ARG start_ARG italic_Z end_ARG , where italic_Z = ∑ start_POSTSUBSCRIPT italic_j ∈ italic_S end_POSTSUBSCRIPT italic_μ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT ) ,
μ
^
2
⁢
(
X
t
∣
X
i
)
=
μ
2
′
⁢
(
X
t
∣
X
i
)
Z
i
,
where
Z
i
=
∑
j
∈
S
μ
2
′
⁢
(
X
j
∣
X
i
)
.
formulae-sequence
subscript
^
𝜇
2
conditional
subscript
𝑋
𝑡
subscript
𝑋
𝑖
superscript
subscript
𝜇
2
′
conditional
subscript
𝑋
𝑡
subscript
𝑋
𝑖
subscript
𝑍
𝑖
where
subscript
𝑍
𝑖
subscript
𝑗
𝑆
superscript
subscript
𝜇
2
′
conditional
subscript
𝑋
𝑗
subscript
𝑋
𝑖
\hat{\mu}_{2}(X_{t}\mid X_{i})=\frac{\mu_{2}^{\prime}(X_{t}\mid X_{i})}{Z_{i}}%
,\quad\text{where}\quad Z_{i}=\sum_{j\in S}\mu_{2}^{\prime}(X_{j}\mid X_{i}).
over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) = divide start_ARG italic_μ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) end_ARG start_ARG italic_Z start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT end_ARG , where italic_Z start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = ∑ start_POSTSUBSCRIPT italic_j ∈ italic_S end_POSTSUBSCRIPT italic_μ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) .
Here,
μ
^
1
⁢
(
X
i
)
subscript
^
𝜇
1
subscript
𝑋
𝑖
\hat{\mu}_{1}(X_{i})
over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT )
is the normalised marginal distribution for cluster
X
i
subscript
𝑋
𝑖
X_{i}
italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
, and
μ
^
2
⁢
(
X
t
∣
X
i
)
subscript
^
𝜇
2
conditional
subscript
𝑋
𝑡
subscript
𝑋
𝑖
\hat{\mu}_{2}(X_{t}\mid X_{i})
over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT )
is the normalised conditional distribution for
X
t
subscript
𝑋
𝑡
X_{t}
italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT
given
X
i
subscript
𝑋
𝑖
X_{i}
italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
. The terms
Z
𝑍
Z
italic_Z
and
Z
i
subscript
𝑍
𝑖
Z_{i}
italic_Z start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
are normalization constants to ensure that the distributions sum to 1.
The joint and pseudo-joint distributions are defined as:
μ
^
⁢
(
X
i
,
X
t
)
^
𝜇
subscript
𝑋
𝑖
subscript
𝑋
𝑡
\displaystyle\hat{\mu}(X_{i},X_{t})
over^ start_ARG italic_μ end_ARG ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT )
=
μ
^
1
⁢
(
X
i
)
⁢
μ
^
2
⁢
(
X
t
∣
X
i
)
,
absent
subscript
^
𝜇
1
subscript
𝑋
𝑖
subscript
^
𝜇
2
conditional
subscript
𝑋
𝑡
subscript
𝑋
𝑖
\displaystyle=\hat{\mu}_{1}(X_{i})\,\hat{\mu}_{2}(X_{t}\mid X_{i}),
= over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) ,
μ
^
⊗
⁢
(
X
i
,
X
t
)
superscript
^
𝜇
tensor-product
subscript
𝑋
𝑖
subscript
𝑋
𝑡
\displaystyle\hat{\mu}^{\otimes}(X_{i},X_{t})
over^ start_ARG italic_μ end_ARG start_POSTSUPERSCRIPT ⊗ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT )
=
μ
^
1
⁢
(
X
i
)
⁢
∑
j
∈
S
μ
^
1
⁢
(
X
j
)
⁢
μ
^
2
⁢
(
X
t
∣
X
j
)
.
absent
subscript
^
𝜇
1
subscript
𝑋
𝑖
subscript
𝑗
𝑆
subscript
^
𝜇
1
subscript
𝑋
𝑗
subscript
^
𝜇
2
conditional
subscript
𝑋
𝑡
subscript
𝑋
𝑗
\displaystyle=\hat{\mu}_{1}(X_{i})\,\sum_{j\in S}\hat{\mu}_{1}(X_{j})\,\hat{%
\mu}_{2}(X_{t}\mid X_{j}).
= over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) ∑ start_POSTSUBSCRIPT italic_j ∈ italic_S end_POSTSUBSCRIPT over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT ) over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ( italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ∣ italic_X start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT ) .
The joint distribution
μ
^
⁢
(
X
i
,
X
t
)
^
𝜇
subscript
𝑋
𝑖
subscript
𝑋
𝑡
\hat{\mu}(X_{i},X_{t})
over^ start_ARG italic_μ end_ARG ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT )
combines the marginal and conditional distributions, while the pseudo-joint distribution
μ
^
⊗
⁢
(
X
i
,
X
t
)
superscript
^
𝜇
tensor-product
subscript
𝑋
𝑖
subscript
𝑋
𝑡
\hat{\mu}^{\otimes}(X_{i},X_{t})
over^ start_ARG italic_μ end_ARG start_POSTSUPERSCRIPT ⊗ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT )
assumes independence between clusters.
Finally, the mutual information is computed as:
I
^
⁢
(
γ
1
,
γ
2
)
=
∑
i
,
t
∈
S
μ
^
⁢
(
X
i
,
X
t
)
⁢
ln
⁡
(
μ
^
⁢
(
X
i
,
X
t
)
+
γ
1
μ
^
⊗
⁢
(
X
i
,
X
t
)
+
γ
2
)
.
^
𝐼
subscript
𝛾
1
subscript
𝛾
2
subscript
𝑖
𝑡
𝑆
^
𝜇
subscript
𝑋
𝑖
subscript
𝑋
𝑡
^
𝜇
subscript
𝑋
𝑖
subscript
𝑋
𝑡
subscript
𝛾
1
superscript
^
𝜇
tensor-product
subscript
𝑋
𝑖
subscript
𝑋
𝑡
subscript
𝛾
2
\hat{I}(\gamma_{1},\gamma_{2})=\sum_{i,t\in S}\hat{\mu}(X_{i},X_{t})\ln\left(%
\frac{\hat{\mu}(X_{i},X_{t})+\gamma_{1}}{\hat{\mu}^{\otimes}(X_{i},X_{t})+%
\gamma_{2}}\right).
over^ start_ARG italic_I end_ARG ( italic_γ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_γ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ) = ∑ start_POSTSUBSCRIPT italic_i , italic_t ∈ italic_S end_POSTSUBSCRIPT over^ start_ARG italic_μ end_ARG ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ) roman_ln ( divide start_ARG over^ start_ARG italic_μ end_ARG ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ) + italic_γ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_ARG start_ARG over^ start_ARG italic_μ end_ARG start_POSTSUPERSCRIPT ⊗ end_POSTSUPERSCRIPT ( italic_X start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_X start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ) + italic_γ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_ARG ) .
Here,
γ
1
subscript
𝛾
1
\gamma_{1}
italic_γ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
and
γ
2
subscript
𝛾
2
\gamma_{2}
italic_γ start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
are small stabilization parameters to prevent division by zero, and
S
𝑆
S
italic_S
is the set of clusters.
This mutual information score serves as a proxy for epistemic uncertainty.
High
I
^
^
𝐼
\hat{I}
over^ start_ARG italic_I end_ARG
values signal significant uncertainty.
Appendix C
Additional Evaluation
C.1
Experimental Results for
claude-3-7-sonnet
Table 4:
Correlation Results — Pearson coefficient (p-value) for
claude-3-7-sonnet
. Statistically significant results are highlighted in
bold
.
Technique
claude-3-7-sonnet
Easy
Medium
Hard
SE-SymbUniform
−
0.35
times
-0.35
absent
-0.35\text{\,}
start_ARG - 0.35 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.34
times
-0.34
absent
-0.34\text{\,}
start_ARG - 0.34 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.32
times
-0.32
absent
-0.32\text{\,}
start_ARG - 0.32 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0003
times
0.0003
absent
0.0003\text{\,}
start_ARG 0.0003 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
CC-Symb
−
0.35
times
-0.35
absent
-0.35\text{\,}
start_ARG - 0.35 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.34
times
-0.34
absent
-0.34\text{\,}
start_ARG - 0.34 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0002
times
0.0002
absent
0.0002\text{\,}
start_ARG 0.0002 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
−
0.32
times
-0.32
absent
-0.32\text{\,}
start_ARG - 0.32 end_ARG start_ARG times end_ARG start_ARG end_ARG
(
0.0003
times
0.0003
absent
0.0003\text{\,}
start_ARG 0.0003 end_ARG start_ARG times end_ARG start_ARG end_ARG
)
C.2
Details on the Abstention Policy Evaluation
Given that
gpt-3.5-turbo-instruct
’s responses exhibit a low unit test passing rate, leading to an imbalanced dataset where incorrect responses significantly outnumber correct ones. This imbalance risks trivializing the classification task, as an “all-incorrect” model would dominate. To address this, we followed standard practice and applied random downsampling, removing a portion of incorrect responses to prevent the model from defaulting to a trivial solution. We split the dataset 50/50 into training and validation.
To mitigate overfitting and reduce bias, we employed 2-fold cross-validation, alternating between training and validation for each fold.