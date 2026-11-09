---
title: 'Underspecification does not imply Incoherence: The Risks of Semantic Collapse
  in Coding Models'
id: underspecification-does-not-imply-incoherence-the-risks-of-semantic-collapse-in
tags:
- code-llm-calibration-aaai27-eabf3f
- locus-code-verbal-calibration-occupied-or-open
- semantic-collapse
- sampling-uq-failure-mode
- not-a-calibration-paper
created: '2026-07-17T19:00:38.663674Z'
updated: '2026-07-17T19:01:40.103653Z'
source: https://arxiv.org/html/2607.01953
source_domain: arxiv.org
fetched_at: '2026-07-17T19:00:38.663185Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Paper on ''detrimental semantic collapse'' in code LLMs (arXiv 2607.01953,
  cs.SE): shows that self-consistency/clustering-based uncertainty estimation (the
  same family as semantic entropy) silently fails when repeated samples for an underspecified
  or ambiguous prompt converge on a single WRONG interpretation -- all samples agree,
  so entropy/disagreement-based UQ signals read ''confident,'' but the model is confidently
  wrong. Measured across MBPP, HumanEval, and LiveCodeBench v6 with 3 SOTA coding
  models: detrimental collapse affects 3% of HumanEval, 10-16% of MBPP, and 18-32%
  of LiveCodeBench tasks even on ''well-specified'' original benchmarks, rising up
  to 5.5x under deliberately injected underspecification (contradictions/incompleteness/ambiguity
  variants of MBPP). NOT a verbalized-confidence or calibration-training paper --
  no ECE/AUROC/Brier reported, no confidence elicitation of any kind (verbalized,
  internal-probe, or post-hoc). It is a diagnostic/failure-mode paper about WHY sampling-based
  correctness-prediction methods (like the target paper''s internal sampling signal,
  and like Functional Entropy''s functional-equivalence clustering) can be systematically
  fooled by underspecified prompts. Directly relevant as a caveat/limitation the target
  paper should address: its near-perfectly-calibrated internal sampling signal could
  inherit this blind spot on ambiguous code prompts. Caution: an earlier WebSearch
  AI-generated summary attributed specific numbers (''48.9% MBPP / 45.2% LiveCodeBench
  / 43.4% BigCodeBench pairwise resolution'', ''Pearson r=+0.10/-0.41/-0.63'') to
  a code-confidence paper matching this description; those exact figures do NOT appear
  in this paper''s text and could not be traced to any single real source after further
  search -- treat them as likely hallucinated/conflated and do not cite them.'
---

Underspecification does not imply Incoherence: The Risks of Semantic Collapse in Coding Models
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY-SA 4.0
arXiv:2607.01953v1 [cs.SE] 02 Jul 2026
Underspecification does
not
imply Incoherence: The Risks of Semantic Collapse in Coding Models
Cedric Richter
Mike Papadakis
Abstract
Large Language Models (LLMs) have become increasingly effective at generating code when task descriptions are clear and precise. Yet, in practice, user-provided task descriptions are often ambiguous, incomplete, or contradictory, leaving critical aspects of the intended program behavior underspecified. In such cases, multiple behaviorally distinct interpretations may satisfy the description equally well, yet semantically differ in ways that matter/affect the user intent. A natural expectation, often assumed by researchers, is that prompt underspecification manifests as
incoherence
: When asked multiple times, an LLM produces multiple semantically distinct implementations reflecting the ambiguity of the task description. In this paper, we challenge this assumption. We find that LLMs frequently collapse onto a single incorrect interpretation of the task description, consistently generating coherent but behaviorally misaligned code. We term this failure mode
detrimental semantic collapse
and find that it affects over 10% of tasks in MBPP, 3% in HumanEval, and 32% of LiveCodeBench, all benchmarks assumed to be well-specified. By deliberately injecting underspecification issues in the benchmark prompts, the rate rises to over 5 times, exposing a fundamental blind spot in disambiguation and correctness estimation techniques that rely on incoherence as a proxy for prompt underspecification.
I
Introduction
When a developer is asked to implement a function that retrieves the maximum value from a list, the task seems straightforward. But what should be returned if the list contains heterogeneous elements such as integers, floating-point numbers, or strings? The maximum integer, the largest number, or the lexicographically largest string? The task description does not say.
Software developers are frequently confronted with task descriptions that are ambiguous, incomplete, or contradictory, leaving critical aspects of the intended behavior unspecified
[
8
,
17
,
18
,
11
]
. In these cases, the developer has to disambiguate between multiple behaviorally distinct interpretations by asking clarifying questions, exploring alternatives, or committing to a single interpretation.
Today, software development has been largely transformed by large language models (LLMs), which increasingly automate tasks that traditionally require significant manual effort
[
29
]
. The most prominent such application is code generation
[
6
,
15
,
22
]
: given a natural language task description, an LLM can produce a working implementation. This raises a critical question: when the task description is underspecified, as is frequently the case in practice, how does the LLM behave?
A natural expectation is that underspecification leads to
incoherence
: When repeatedly asked with the same underspecified task description, an LLM should produce multiple semantically distinct implementations reflecting the ambiguity of the task. This incoherence can be detected by clustering LLM-generated programs into equivalence classes based on their execution behavior. If multiple clusters emerge, the task description is deemed underspecified
[
18
,
11
]
.
This assumption has motivated several studies. Mu et al.
[
18
]
use semantic clustering to identify
underspecified task descriptions and generate clarifying questions. Jia et al.
[
11
]
cluster generated programs to automatically repair ambiguous task descriptions. More recent work
[
21
,
25
]
has also started to use semantic clustering as a proxy for program incorrectness, treating incoherent outputs as evidence of incorrectness. All of these studies focus on the implications of LLM incoherence, leaving open a critical question:
Does underspecification imply incoherence?
A positive answer would reinforce the applicability of the related studies and motivate further efforts to improve code correctness and, more broadly, the reliability of automatic coding systems. Conversely, a negative answer would highlight a significant limitation of existing methods and further emphasize both the importance and the difficulty of mitigating the issues arising from the prompt underspecification.
In this work, we answer the above question by systematically studying whether prompt underspecification leads to incoherence of coding models. We evaluate three state-of-the-art coding LLMs, namely Claude Sonnet 4.5
[
2
]
, GPT-4.1-mini
[
19
]
, and Qwen3
[
23
]
, on systematically underspecified variants of three widely used coding benchmarks: MBPP
[
3
]
, HumanEval
[
6
]
, and LiveCodeBench
[
10
]
.
Underspecified Prompt - MBPP/294
Write a function to find the
maximum value
in a given heterogeneous list.
Consistent Model Response
⬇
numeric_values
=
[
item
for
item
in
lst
if
isinstance
(
item
,
(int, float)
)
]
...
maximum
integer
value
(a)
Example
Expectation
Underspecified Prompt
LLM
⋯
\cdots
dominant
interpretation
Semantic Collapse
Underspecified Prompt
LLM
dominant
interpretation
(b)
Semantic Clustering
(c)
Detrimental Semantic Collapse
Figure 1
:
Motivating example.
(a) Real-world programming tasks are often underspecified. (b) Semantic clustering approaches assume that underspecified prompts lead LLMs in producing multiple semantically different interpretations when prompted multiple times (with the same prompt/description). We observe that such a phenomenon happens, but more often it does not as LLMs collapse to a single interpretation. (c) Collapse is often detrimental, producing a single incorrect interpretation breaking the key assumption made by semantic clustering methods. For example underspecification manifested in form of ambiguous descriptions, increases the risk for detrimental collapse.
Contrary to the prevailing assumption, we find that prompt underspecification does not imply incoherence. Instead, LLMs frequently collapse to a single incorrect interpretation, while remaining coherent across repeated generations. We term this failure mode
detrimental semantic collapse
, as the LLM silently commits to a wrong interpretation, providing neither a correct solution nor any indication that the task description was underspecified.
We further show that detrimental semantic collapse is prevalent even on benchmarks widely regarded as well-specified, affecting over 3% of HumanEval, 11% of MBPP, and 32% of LiveCodeBench tasks. Under controlled underspecification, collapse rates can increase by a factor of up to 5.5x on individual benchmarks, suggesting that current LLMs are substantially less capable of surfacing ambiguity than assumed.
Motivating example.
Figure
5(a)
shows the task description of MBPP/294, a benchmark task of the popular MBPP
[
3
]
coding benchmark, and a response from Claude Sonnet 4.5. The LLM is tasked to implement a function to retrieve the maximum value in a heterogeneous list. Interestingly, the description does not specify what the maximum value in a list of integers, floats, and strings is. The LLMs consistently assumes across multiple trials that the function should return the maximum
number
(floats and integers) in a list, yet the developer tests reveal that the actual intention was to only retrieve the maximum
integer
value. Unfortunately, the consequence of this underspecification issue is that the LLM collapses to a single incorrect interpretation, even though in practice multiple feasible interpretations exist.
MBPP/294 is one of several benchmark tasks that we manually identified as ambiguous
1
1
1
Examples of Ambiguity: MBPP/294, MBPP/102, MBPP/410, MBPP/576
, incomplete
2
2
2
Incompletness: MBPP/7, MBPP/137, MBPP/244, MBPP/261, MBPP/278
, or contradictory
3
3
3
Contradictions: MBPP/459, MBPP/638, MBPP/639
. The thing is, as we show in this paper, that repeatedly sampling a response from an LLM produces the same incorrect interpretation each time.
This is particularly problematic for clustering-based approaches (
Figure
5(b)
) that assume that underspecification yields distinct semantic clusters representing different interpretations, e.g., one cluster supporting integer inputs only and another supporting all numeric types. Under detrimental semantic collapse, clustering-based approaches fail silently, failures evade detection, as the incorrect implementation is consistent across generations, leaving users unaware of the underlying misalignment. Our experiments show that detrimental semantic collapse appears frequently across models, and is further amplified by underspecification (as shown for MBPP in
Figure
5(c)
).
Contributions.
Overall, our work makes the following three key contributions:
•
We identify the
detrimental semantic collapse
, a previously overlooked failure mode in which coding LLMs consistently commit to a single behaviorally misaligned interpretation of an underspecified task, providing neither a correct solution nor any signal of incorrectness or underspecification.
•
We show that prompt underspecification frequently does not induce incoherence in coding LLMs, challenging a foundational assumption of semantic clustering-based approaches.
•
Through experiments on three state-of-the-art coding models and systematically underspecified variants of MBPP, HumanEval, and LiveCodeBench, we demonstrate that detrimental collapse rates can rise from 10% on original benchmark tasks (MBPP) to over 50% on systematically underspecified variants.
More broadly, our findings expose a fundamental limitation of approaches that use incoherence as a proxy for prompt ambiguity or program incorrectness: coherent model behavior cannot be interpreted as evidence of correct task understanding. In practice, this means that under-specified prompts cannot be reliably detected using the LLMs’ interpretations, thereby limiting the confidence one can place in generated code without performing any independent testing.
These results can be seen as a ‘call to arms’ for the research community to develop more principled methods for evaluating prompts and model understanding, including formal specifications, robustness benchmarks, and verification frameworks that go beyond surface-level coherence.
II
Related Work
We observe an increasing trend of methods that rely on
semantic incoherence
in the scientific literature, results of a mini-collection survey, performed in an ad-hoc procedure that checks the titles of papers published in SE (FSE, ASE, and ISSTA) and AI (NeurIPS, ICLR, ACL, EMNLP, and AAAI) conferences, over the past 4 years is shown in
Figure
2
. The topics of these studies are related to (1) candidate selection, (2) estimating correctness, and (3) identifying underspecification, with topics (2) and (3) gaining popularity over the years.
Figure 2
:
Number of publications published in top-tier SE and AI conferences that rely on the semantic clustering of LLM outputs as a proxy signal, grouped by year and per research topic/purpose, i.e., solution selection, correctness estimation, and prompt quality detection. The 2025–26 bar combines both years as 2026 is ongoing.
Self-consistent Candidate Selection.
Self-consistency
[
26
]
is an effective candidate selection method that only reports the answer that occurs most often across sampled LLM responses. Self-consistency has been adapted in many forms to the coding domain: MBR-Exec
[
22
]
selects a program that is most consistent with all other sampled programs when executed on a small set of test inputs. DOCE
[
14
]
combines MBR-Exec’s selection strategy with self-debugging. AlphaCode
[
15
]
clusters generated programs by executing them on generated test inputs and picks candidate solutions from the largest clusters.
CodeT
[
4
]
samples multiple programs and test inputs and selects candidate programs that have the highest code-test consistency. MPSC
[
9
]
aligns generates programs, formal specifications, and test cases while selecting programs that have the strongest execution alignment with tests and specifications. SRank
[
24
]
clusters and ranks code candidates by their execution similarity. LLMCodeChoice
[
7
]
clusters programs by execution, but leaves the selection to an LLM judge.
FunCoder
[
5
]
uses execution similarity to select sub-routines in larger coding contexts. Functional Majority Voting
[
13
]
has recently been proposed as a way for execution-based clustering and test-time training. All these techniques share a common assumption: Mistakes in LLM-generated code produce divergent behavior on individual test inputs, while correct behavior is shared across a majority of implementations.
Interestingly, we find that detrimental semantic collapse represents a
major bottleneck
of these methods: When the LLM’s output collapses to a single semantically incorrect interpretation, self-consistency methods fail to identify any correct solution.
Correctness.
There is a recent surge in interest of using semantic incoherence of LLMs as an oracle-less measure of incorrectness
[
21
,
25
,
20
,
28
,
13
]
. Sharma and David
[
21
]
found that the count of semantic clusters correlates with code correctness, e.g. a lower number of clusters indicates a higher correctness likelihood. Valentin et al.
[
25
]
established semantic incoherence as a lower bound on model error. Ravuri and Amarasinghe
[
20
]
further employ semantic incoherence to identify hallucination-induced errors.
Based on these insights, recent methods started to use semantic coherence as a pseudo-label for program correctness
[
28
,
13
]
. Our experiments indicate a
major blind spot
of these methods: While semantic incoherence is an effective way to identify potential model error, its absence is not a reliable indicator of model correctness.
Underspecification.
While semantic incoherence has traditionally been interpreted as a symptom of model error, recent work has evaluated semantic incoherence as a signal of prompt underspecification, using variance across generations to identify and clarify ambiguous or incomplete task descriptions
[
18
,
27
,
11
]
.
ClarifyGPT
[
18
]
uses semantic clustering to identify underspecified prompts and exploits semantic differences between candidates in different clusters to ask clarifying questions. ClarifyCoder
[
27
]
employs the clarification strategy of ClarifyGPT to generate training examples and train language models to ask clarifying questions.
SpecFix
[
11
]
exploits semantic differences of candidates in different clusters to localize and repair problems in task descriptions. While often effective in practice, these technique rely on the assumption that underspecified task descriptions produce divergent semantic clusters.
Unfortunately, we observe that specifically prompt underspecification increases the risk of detrimental semantic collapse, rendering these methods ineffective on a large fraction of underspecified prompts.
III
Objectives and Research Questions
We aim to assess the behavior of large language models on the task of code generation from task descriptions especially when these are
underspecified
. Formally, given a textual task description
d
d
of programming task, the goal of the task is to generate the intended target program
P
∗
P^{*}
. The task description
d
d
is underspecified by admitting multiple feasible interpretations:
𝕀
​
(
d
)
=
{
P
1
,
P
2
,
…
}
,
\mathbb{I}(d)=\{P_{1},P_{2},\dots\},
(1)
where
P
∗
∈
𝕀
​
(
d
)
P^{*}\in\mathbb{I}(d)
, i.e. the intended program is one of many feasible interpretations.
We are specifically interested in whether large language models reflect the ambiguity of underspecified task descriptions through semantically diverse responses, or whether they collapse to a single interpretation, the key assumption made by clustering-based approaches, as we already discussed.
III-A
Research Questions
We investigate the behavior of large language models when confronted with underspecified task descriptions by answering the following research questions (RQs):
RQ1.
Do LLMs explore multiple interpretations of underspecified task descriptions?
A natural assumption is that LLMs produce multiple inconsistent interpretations when prompted with underspecified task descriptions. We investigate whether this is true by measuring whether underspecified task descriptions lead to semantically diverse responses.
RQ2.
How frequently does semantic collapse become detrimental?
While RQ1 examines whether underspecification increases inconsistency of LLM responses, inconsistency alone does not indicate correctness, nor does semantic collapse necessarily imply incorrectness. We measure the rate of detrimental collapse across both well-specified and underspecified task descriptions, investigating whether underspecification elevates the likelihood that a collapsed interpretation is incorrect despite being internally consistent.
RQ3.
What is the impact of detrimental semantic collapse on downstream techniques?
Methods that rely on semantic incoherence to detect prompt underspecification, such as clarification question generation, presuppose that underspecified prompts produce multiple distinct interpretations. We evaluate the extent to which detrimental collapse constitutes a blind spot for such techniques, causing them to silently return incorrect functionality without triggering clarification.
III-B
Semantic Clustering and Collapse
Semantic Clustering.
Two programs
P
P
and
P
′
P^{\prime}
are
semantically indistinguishable
with respect to a set of test inputs
𝒯
\mathcal{T}
(
P
≡
𝒯
P
′
P\equiv_{\mathcal{T}}P^{\prime}
) if:
∀
x
∈
𝒯
:
P
​
(
x
)
=
P
′
​
(
x
)
,
\forall x\in\mathcal{T}:P(x)=P^{\prime}(x),
(2)
We cluster sampled programs into equivalence classes
[
P
]
≡
𝒯
[P]_{\equiv_{\mathcal{T}}}
, where
P
′
∈
[
P
]
≡
𝒯
P^{\prime}\in[P]_{\equiv_{\mathcal{T}}}
if
P
′
P^{\prime}
is semantically indistinguishable from
P
P
. Each equivalence class corresponds to a distinct interpretation of the task description
d
d
.
Semantic Collapse.
Let
𝗌𝗎𝗉𝗉
≡
​
(
d
)
\mathsf{supp}_{\equiv}(d)
be the set of equivalence classes
4
4
4
For brevity, we use equivalence classes and their representatives (programs) interchangeably.
obtained by sampling from
𝖫𝖫𝖬
\mathsf{LLM}
. We define the support
𝗌𝗎𝗉𝗉
≡
​
(
d
)
\mathsf{supp}_{\equiv}(d)
as
semantically collapsed
iff:
|
𝗌𝗎𝗉𝗉
≡
​
(
d
)
|
=
1
,
\left|\mathsf{supp}_{\equiv}(d)\right|=1,
(3)
i.e. repeatedly sampling from the
𝖫𝖫𝖬
\mathsf{LLM}
yields a single interpretation, despite
|
𝕀
​
(
d
)
|
>
1
\left|\mathbb{I}(d)\right|>1
.
Semantic collapse is
benign
when
𝗌𝗎𝗉𝗉
≡
​
(
d
)
=
{
P
∗
}
\mathsf{supp}_{\equiv}(d)=\{P^{*}\}
, i.e. the LLM consistently produces the same interpretation, and
detrimental
when
𝗌𝗎𝗉𝗉
≡
​
(
d
)
=
{
P
′
}
\mathsf{supp}_{\equiv}(d)=\{P^{\prime}\}
with
P
′
≠
P
∗
P^{\prime}\neq P^{*}
, i.e. the LLM converges on a single incorrect interpretation.
Critically, benign and detrimental collapse are observably indistinguishable without access to an oracle: The distribution of LLM responses provides no indication that the task description was underspecified.
III-C
Measuring Semantic Collapse under Finite Budget
Algorithm 1
Sequential Clustering for Collapse Detection
1:
Task description
d
d
, language model
𝖫𝖫𝖬
\mathsf{LLM}
, a set of test inputs
𝒯
\mathcal{T}
, budget
k
k
2:
Set of cluster representatives
R
R
3:
R
←
∅
R\leftarrow\emptyset
⊳
\triangleright
Set of cluster representatives
4:
for
i
←
1
i\leftarrow 1
to
k
k
do
5:
P
i
∼
𝖫𝖫𝖬
​
(
d
)
P_{i}\sim\mathsf{LLM}(d)
⊳
\triangleright
Sample program from LLM
6:
matched
←
false
\textit{matched}\leftarrow\textbf{false}
7:
for
P
∈
R
P\in R
do
8:
if
∀
x
∈
𝒯
:
P
i
​
(
x
)
=
P
​
(
x
)
\forall x\in\mathcal{T}:P_{i}(x)=P(x)
then
9:
matched
←
true
\textit{matched}\leftarrow\textbf{true}
10:
break
11:
if
not
matched
then
12:
R
←
R
∪
{
P
i
}
R\leftarrow R\cup\{P_{i}\}
13:
if
|
R
|
>
1
|R|>1
then
14:
return
R
R
⊳
\triangleright
Collapse refuted
15:
return
R
R
⊳
\triangleright
Collapse confirmed:
|
R
|
=
1
|R|=1
Finite approximation of
𝗌𝗎𝗉𝗉
≡
​
(
d
)
\mathsf{supp}_{\equiv}(d)
.
While semantic collapse cannot be confirmed with certainty from a finite set of samples, we can derive an efficient detection algorithm that provides PAC-style guarantees
[
25
]
. Assume we have observed independent samples
P
1
,
P
2
,
…
,
P
k
∼
𝖫𝖫𝖬
​
(
d
)
P_{1},P_{2},\dots,P_{k}\sim\mathsf{LLM}(d)
with empirical support
|
𝗌𝗎𝗉𝗉
≡
k
​
(
d
)
|
=
1
\left|\mathsf{supp}_{\equiv}^{k}(d)\right|=1
, i.e. all
k
k
samples fall in a single cluster. Then, we can derive a bound on the probability that a future interpretation can be sampled from
𝖫𝖫𝖬
\mathsf{LLM}
that does not fall into the cluster, which would refute semantic collapse. Using
k
=
⌈
log
⁡
(
δ
)
log
⁡
(
1
−
ϵ
)
⌉
k=\lceil\frac{\log(\delta)}{\log(1-\epsilon)}\rceil
, it holds that
ℙ
​
(
P
∉
𝗌𝗎𝗉𝗉
≡
k
​
(
d
)
∣
P
∼
𝖫𝖫𝖬
​
(
d
)
)
≤
ϵ
,
\mathbb{P}(P\not\in\mathsf{supp}_{\equiv}^{k}(d)\mid P\sim\mathsf{LLM}(d))\leq\epsilon,
(4)
with probability of at least
1
−
δ
1-\delta
. In other words, by choosing a sufficiently large
k
k
, we can bound the risk of incorrectly concluding that the support has collapsed.
Sequential Semantic Clustering.
Based on this observation, we derive an efficient algorithm for detecting semantic collapse (see
Algorithm
1
). Given a task description
d
d
, we draw samples from
𝖫𝖫𝖬
​
(
d
)
\mathsf{LLM}(d)
one at a time (Line 3), assigning each new program to an existing equivalence class if it is semantically indistinguishable from a representative (Line 4-8), or creating a new class otherwise (Line 10). Sampling terminates early as soon as a second equivalence class is discovered (Line 11) – refuting collapse – or once the budget
k
k
is exhausted, in which case the empirical support has collapsed to a single interpretation (Line 13).
This sequential strategy avoids unnecessary sampling: under collapse the full budget is used, but a single divergent sample is sufficient to terminate early.
Test input generation.
The equivalence check in Line 6 of
Algorithm
1
requires a set of representative test inputs
𝒯
\mathcal{T}
to compare program behavior. In general, there are many ways to derive test inputs
𝒯
\mathcal{T}
. We follow a common two-stage approach to derive
𝒯
\mathcal{T}
from the task description
d
d
[
16
]
:
1.
Seed Corpus:
An initial set of test inputs is generated by prompting an
𝖫𝖫𝖬
\mathsf{LLM}
with the task description
d
d
, covering representative cases including typical inputs, boundary conditions, and edge cases suggested by the task description.
2.
Type-Aware Mutation:
To broaden test diversity beyond what is generated directly, type-aware mutation is applied to the seed corpus. Given a seed input, variants are produced by applying type-preserving perturbations, e.g. boundary values and sign changes for integers, length and content variations for lists, and sub-string changes for strings. This increases the likelihood of exposing behavioral differences between programs that agree on typical inputs but diverge on edge cases.
In our main experiments,
𝒯
\mathcal{T}
is instantiated using inputs from the gold test suite provided with each benchmark, isolating the effect of underspecification on semantic clustering from any confounding effects of automated test generation. The impact of test inputs derived from underspecified task descriptions on semantic clustering is evaluated separately in
Section
V-B
.
IV
Experimental Setup
IV-A
Benchmarks
Our evaluation is based on three widely used code generation benchmarks:
MBPP
+
[
16
,
3
]
,
HumanEval
+
[
16
,
6
]
, and LiveCodeBench
[
10
]
. We consider both the original benchmarks and underspecified variants:
MBPP
+
.
MBPP
+
comprises 378 crowd-sourced Python programming problems, designed to be approachable by entry-level programmers. Each task contains a task description, a reference implementation, and an extensive set of test cases. For MBPP
+
, we consider three forms of underspecification taken from
[
12
]
:
Ambiguous.
A variant of MBPP
+
in which each of the 378 task descriptions is rewritten to introduce ambiguity, admitting multiple plausible interpretations.
Incomplete.
A variant of MBPP
+
in which each task description omits one or more requirements, leaving aspects of the intended behavior unspecified and admitting multiple valid implementations.
Contradictory.
A variant of MBPP
+
in which each task description contains inconsistent requirements, forcing a choice between competing resolutions each corresponding to a distinct interpretation.
HumanEval
+
.
HumanEval
+
contains 164 Python programming tasks. The intended behavior is captured by a reference implementation and an extensive set of test cases. For underspecification, we consider a recently introduced dataset of underspecified HumanEval problems
[
1
]
:
Underspecified.
A variant of HumanEval
+
in which the textual description of the task is underspecified, admitting multiple plausible interepretations.
LiveCodeBench.
LiveCodeBench is a continuously evolving benchmark of programming challenges. The benchmark enables contamination-free evaluation of LLMs by providing challenges published after the knowledge cutoff of LLMs. We employ LiveCodeBench v6 considering 182 problems published after January 1st 2025, which is the knowledge cutoff of all our evaluated models. For underspecification, we adopt a recently introduced underspecified variant
[
1
]
:
Underspecified.
A variant of LiveCodeBench in which the task description, e.g. competition-style programming problem, is underspecified, allowing for multiple interpretations.
For all benchmarks, the intended target behavior
P
∗
P^{*}
is defined by the original benchmarks.
IV-B
Evaluation Metrics
To answer our research questions, we use the following metrics with respect to a sampling budget
k
k
:
Pass@k.
The likelihood that at least one solution among
k
k
sampled LLM responses is correct by passing all test cases of the original benchmark
[
6
]
.
Inconsistency (
ℐ
​
c
\mathcal{I}c
).
We measure inconsistency in terms of pointwise incoherence
[
25
]
. Pointwise incoherence is the likelihood that two random programs (among the
k
k
sampled LLM responses for a task
d
d
) can be distinguished by a random test input.
Semantic Collapse (%SC).
The percentage of tasks
d
d
where
|
𝗌𝗎𝗉𝗉
≡
k
​
(
d
)
|
=
1
\left|\mathsf{supp}_{\equiv}^{k}(d)\right|=1
. Detrimental semantic collapse is the percentage of tasks that are semantically collapsed tasks with
P
​
a
​
s
​
s
​
@
​
k
=
0
Pass@k=0
.
IV-C
Models
We consider three state-of-the-art code generation LLMs: Claude Sonnet 4.5
[
2
]
, GPT-4.1-mini
[
19
]
, Qwen3-32B
[
23
]
. These represent popular coding models: Claude Sonnet 4.5 is one of the most capable coding LLMs
[
10
]
, GPT-4.1-mini is an economical option for coding, and Qwen3 32B is an effective open source model that can run on consumer hardware. By default, we sample from the output distribution of these models with a temperature of 0.8 and the full response is evaluated against the test suite of each benchmark. We vary the temperature in the ablation study (
Section
VI
).
V
Results
TABLE I
:
Evaluation results of three representative LLMs under underspecified task descriptions at different sampling budgets
k
∈
{
1
,
5
,
10
,
25
}
k\in\{1,5,10,25\}
. We report average Pass@k, inconsistency (
ℐ
​
c
\mathcal{I}c
), and semantic collapse (%SC). Arrows denote the absolute difference in Pass@k to the original benchmark results.
MBPP
+
HumanEval
+
Underspecified
LiveCodeBench
Underspecified
Ambiguous
Incomplete
Contradictory
Model
k
k
Pass@
k
k
ℐ
​
c
\mathcal{I}c
%SC
Pass@
k
k
ℐ
​
c
\mathcal{I}c
%SC
Pass@
k
k
ℐ
​
c
\mathcal{I}c
%SC
Pass@
k
k
ℐ
​
c
\mathcal{I}c
%SC
Pass@
k
k
ℐ
​
c
\mathcal{I}c
%SC
1
44.0
↓
\downarrow
-35.7
0.0
100.0
39.1
↓
\downarrow
-40.6
0.0
100.0
12.9
↓
\downarrow
-66.8
0.0
100.0
87.9
↓
\downarrow
-5.0
0.0
100.0
28.5
↓
\downarrow
-2.3
0.0
100.0
5
49.1
↓
\downarrow
-34.3
6.5
86.5
44.2
↓
\downarrow
-39.2
4.1
89.7
18.2
↓
\downarrow
-65.2
7.6
84.4
91.7
↓
\downarrow
-3.3
1.9
90.8
33.6
↓
\downarrow
-3.3
20.9
54.9
10
50.7
↓
\downarrow
-33.4
15.8
59.8
45.9
↓
\downarrow
-38.2
11.9
66.1
20.1
↓
\downarrow
-64.0
14.0
64.6
92.8
↓
\downarrow
-2.7
2.7
86.6
35.6
↓
\downarrow
-3.9
22.2
50.0
Claude
Sonnet 4.5
25
52.1
↓
\downarrow
-33.1
15.5
52.6
47.6
↓
\downarrow
-37.6
12.5
59.5
22.0
↓
\downarrow
-63.3
14.5
61.6
93.9
↓
\downarrow
-1.8
2.9
82.3
39.0
↓
\downarrow
-3.9
23.9
43.4
1
36.4
↓
\downarrow
-39.4
0.0
100.0
32.7
↓
\downarrow
-43.1
0.0
100.0
11.2
↓
\downarrow
-64.6
0.0
100.0
71.4
↓
\downarrow
-12.7
0.0
100.0
25.2
↓
\downarrow
-2.9
0.0
100.0
5
43.5
↓
\downarrow
-37.1
10.2
79.4
38.9
↓
\downarrow
-41.7
7.9
81.0
15.9
↓
\downarrow
-64.7
8.7
80.7
75.9
↓
\downarrow
-15.3
2.4
89.6
30.9
↓
\downarrow
-4.1
23.4
55.5
10
45.8
↓
\downarrow
-35.9
20.8
50.3
41.4
↓
\downarrow
-40.3
17.4
56.1
17.9
↓
\downarrow
-63.8
18.2
57.1
78.0
↓
\downarrow
-14.4
6.5
76.2
33.5
↓
\downarrow
-4.8
23.7
53.3
GPT-4.1
mini
25
48.4
↓
\downarrow
-34.4
21.7
43.9
44.7
↓
\downarrow
-38.1
17.6
48.4
20.3
↓
\downarrow
-61.4
19.0
50.3
80.5
↓
\downarrow
-12.8
6.9
70.1
36.8
↓
\downarrow
-5.7
24.5
48.4
1
39.0
↓
\downarrow
-37.5
0.0
100.0
32.7
↓
\downarrow
-43.8
0.0
100.0
11.1
↓
\downarrow
-65.4
0.0
100.0
61.2
↓
\downarrow
-6.8
0.0
100.0
34.4
↓
\downarrow
-2.6
0.0
100.0
5
48.6
↓
\downarrow
-36.3
7.3
85.7
38.9
↓
\downarrow
-46.0
10.2
79.1
15.9
↓
\downarrow
-69.0
8.5
80.7
67.9
↓
\downarrow
-4.8
2.6
92.7
44.6
↓
\downarrow
-3.8
28.9
48.4
10
51.2
↓
\downarrow
-35.2
9.9
73.0
41.4
↓
\downarrow
-45.0
21.0
50.3
17.9
↓
\downarrow
-68.5
18.1
57.4
69.1
↓
\downarrow
-4.5
3.4
89.6
48.0
↓
\downarrow
-4.4
29.2
44.5
Qwen3
32B
25
54.8
↓
\downarrow
-33.3
17.5
23.8
44.7
↓
\downarrow
-43.4
17.7
43.4
20.4
↓
\downarrow
-67.7
18.6
50.0
70.1
↓
\downarrow
-4.3
11.6
42.7
52.2
↓
\downarrow
-3.8
29.4
43.4
Figure 3
:
Expected: Underspecification increases inconsistency
on average
.
Relative increase of inconsistency for Claude Sonnet 4.5.
V-A
RQ1 - Underspecification and Diversity
To answer RQ1, we start to evaluate the impact of prompt underspecification on the diversity of LLM responses for sampling budgets
k
∈
{
1
,
5
,
10
,
25
}
k\in\{1,5,10,25\}
. We use
k
=
10
k=10
as our default configuration.
Table
I
shows our experimental results, reporting metrics on underspecified benchmarks alongside absolute difference to the original benchmarks.
Underspecification increases inconsistency
on average
.
Increasing the sampling budget from
k
=
1
k=1
to
k
=
25
k=25
increases the Pass@k of all LLMs, suggesting that LLMs explore different interpretations of the task description and eventually discover the correct interpretation. Compared to the original benchmark (see
Figure
3
), inconsistency increases by a factor of 2.79x, confirming that LLM responses on underspecified tasks are more diverse
on average
.
LLMs often miss the correct interpretation under underspecification.
While increased inconsistency is expected and has motivated previous works, we observe a significant gap in Pass@k of up to 66.8% compared to the original benchmark. For MBPP, this gap persists at higher sampling budgets (e.g. up to Pass@25), suggesting that repeated sampling alone is insufficient for LLMs to reliably produce the correct interpretation of underspecified tasks. On HumanEval and LiveCodeBench, where task descriptions include example input-output pairs that partially compensate for underspecification
[
1
]
, the gap is substantially smaller but still persists.
Semantic collapse persists for underspecification.
Surprisingly, semantic collapse persists for a large fraction of tasks from
k
=
5
k=5
to
k
=
25
k=25
. At
k
=
10
k=10
, between
50.3
50.3
% to
73.0
73.0
% of underspecified MBPP tasks, varying across benchmarks and models, produce semantically indistinguishable programs across all samples.
Increasing the sampling budget to
k
=
25
k=25
reduces collapse, yet it sill persists for
23.8
%
23.8\%
to
61.6
61.6
% of tasks. Consistent trends are observed for HumanEval and LiveCodeBench.
This means that while inconsistency increases on average, LLMs still converge to a single interpretation for a large fraction of underspecified tasks, providing no signal to clustering-based approaches that the task description was underspecified.
Underspecification does not imply inconsistency.
While underspecification increases inconsistency on average, suggesting that LLMs explore multiple inconsistent interpretations, this aggregated trend masks a per-task reality: LLMs frequently collapse to a single interpretation on a large fraction of underspecified tasks, providing no signal that the description was underspecified.
V-B
RQ2 - Detrimental Semantic Collapse
Figure 4
:
Unexpected: 1 in 10 MBPP tasks show detrimental collapse.
Percentage of tasks with detrimental semantic collapse. The light color show the percentage of tasks with erroneous responses.
Not all semantic collapse is
detrimental
: converging on the correct interpretation is often desirable. To answer RQ2, we measure the frequency of detrimental collapse and whether prompt underspecification increases its rate relative to the original benchmark. Overall, we find that:
Detrimental collapse is pervasive across benchmarks.
Figure
4
shows the rate of detrimental collapse. Detrimental collapse is non-trivial across all original descriptions of the studied benchmarks but varies considerably: over 3% of task on HumanEval, 10 to 16% on MBPP, and 18% to 32% on LiveCodeBench exhibit detrimental collapse.
The substantially higher rate on LiveCodeBench reflects the interplay between task difficulty and semantic collapse: competitive programming tasks have inherently low pass rate, yet LLMs still confidently produce semantically indistinguishable programs, frequently converging on an incorrect interpretation with no indication of uncertainty.
(a)
Claude Sonnet 4.5
(b)
GPT-4.1-mini
(c)
Qwen3 32B
Figure 5
:
Detrimental collapse increases with underspecification.
Percentage of tasks with detrimental collapse. Bold numbers indicate the relative increase of detrimental collapse between the original benchmark and the underspecified variant.
Underspecification increases detrimental collapse.
Figure
5
shows the increase in detrimental semantic collapse on underspecified task descriptions relative to the original benchmark. For MBPP, detrimental collapse increases by a factor of
1.45
×
1.45\times
to
5.53
×
5.53\times
depending on the underspecification type and model, making it the dominant failure mode: between 23% and 55% of underspecified tasks exhibit detrimental collapse, compared to 10 – 11% on the original task descriptions. For HumanEval, underspecification increases detrimental collapse by a factor of 1.07x to
3.67
×
3.67\times
. On LiveCodeBench, underspecification has only a marginal impact of a factor of
0.92
×
0.92\times
to
1.00
×
1.00\times
.
Figure 6
:
Impact of LLM-based test generation.
Percentage of tasks with detrimental collapse for Claude Sonnet 4.5 as decided by the golden test inputs and generated test inputs (
n
=
1000
n=1000
). Bold numbers indicate the relative difference in detrimental collapse. Decrease stems from the test inputs being better aligned with the LLM’s understanding of the task.
Impact of LLM-generated test inputs.
Semantic clustering is in practice often performed by executing programs on
LLM-generated test inputs
[
18
,
25
]
. We generate
n
=
1
,
000
n=1{,}000
test inputs (see
Section
III-C
) and
use them to partition programs into semantic clusters.
Figure
6
shows the
impact of LLM-generated test inputs on detrimental collapse for Claude Sonnet
4.5 on the underspecified benchmarks; results for GPT-4.1-mini and Qwen3 32B
follow the same trend. LLM-generated test inputs increase the rate of
detrimental collapse on most benchmarks, with multipliers ranging from
1.03
×
1.03\times
(MBPP Incomp.) to
1.14
×
1.14\times
(HumanEval Underspec.), suggesting
that generated tests are less effective at distinguishing between incorrect
solutions. A notable exception is LiveCodeBench Underspec., where detrimental
collapse decreases by a factor of
0.52
×
0.52\times
, which we attribute to generated
test inputs being better aligned with the LLM’s understanding of the task. Across all variants, detrimental collapse persists under
LLM-generated tests, confirming that detrimental collapse persists under LLM-generated tests.
Incorrectness does not imply inconsistency.
Semantic collapse becomes detrimental in 3% to 32% of tasks of the original benchmark set, increasing by a factor of up to 5.5x under prompt underspecification. Detrimental collapse accounts for a substantial fraction of incorrectly solved tasks, providing no indication of incorrectness.
V-C
RQ3 - Impact on Disambiguation
To answer RQ3, we follow existing work
[
18
]
to simulate clarification dialogues in the presence of prompt underspecification.
Disambiguation simulation.
We simulate a multi-turn clarification conversation following the setup of ClarifyGPT
[
18
]
, replacing the human user with an LLM prompted with the ground truth intent
P
∗
P^{*}
. The simulation process proceeds as follows: (1) The user initiates the conversation with a task description
d
d
; (2) the LLM samples up to
k
k
programs from
𝖫𝖫𝖬
​
(
d
)
\mathsf{LLM}(d)
; (3) if multiple clusters are produced, the LLM generates a clarifying question which the user answers based on
P
∗
P^{*}
; the task description is updated, and the process repeats from step (2). (4) If all samples fall into a single cluster, a solution is returned from that cluster and the conversation ends.
Figure 7
:
Conversation simulation on ambiguous MBPP tasks.
The blue line shows the pass rate of GPT-4.1-mini generated solutions after asking
T
T
questions. The light dashed line is the baseline performance without asking questions. The darker dashed line shows the performance of GPT-4.1-mini on the original benchmark.
Disambiguation improves performance by decreasing inconsistency.
Figure
7
illustrates the conversation behaviour of GPT-4.1-mini
on MBPP-Ambiguous. By asking clarifying questions, disambiguation improves
code generation performance from 36.4% to 46.8% after the first turn, and
further to 51.3% after around 4 turns.
Table
II
summarises the conversation simulations across all benchmarks. Disambiguation produces consistent improvements over the underspecified baseline: from 36.4% to 51.3% on MBPP-Ambiguous, from 32.7% to 51.3% on MBPP-Incomplete, from
11.2% to 13.8% on MBPP-Contradictory, from 71.4% to 82.9% on HumanEval-Underspec., and from 25.2% to 26.4% on LiveCodeBench-Underspec.
These improvements are driven by a reduction in inconsistency: conversation simulations converge to a single semantic cluster within 0 to 9 turns, indicating that clarification is an effective means of achieving consistency.
Disambiguation leaves a substantial gap to the original benchmark performance.
Despite the improvements reported above,
Figure
7
and
Table
II
reveal a substantial remaining gap to the original
benchmark performance. On MBPP in particular, disambiguated performance remains
24.5% to 62.0% below the original benchmark even after full clarification.
The gap is considerably smaller for HumanEval (
−
1.2
%
-1.2\%
) and LiveCodeBench (
−
1.7
%
-1.7\%
), suggesting that the degree of underspecification in MBPP is fundamentally harder to resolve through clarification alone.
This highlights that clustering-based disambiguation, while effective at reducing inconsistency,
does not fully resolve underspecification.
TABLE II
:
Summary of conversation simulations across underspecified benchmarks. We report the final pass rate, the minimum – maximum number of turns, the detrimental semantic collapse at turn 0 (DC@0), after one clarification question (DC@1), after follow-up questions (DC@10). Arrows denote the absolute difference of pass rate and Pass@1 of the original benchmark tasks.
Benchmark
Pass rate
Turns
DC@0
DC@1
DC@10
MBPP-Ambiguous
51.3
↓
\downarrow
-24.5
0 – 6
23.0
37.3
48.7
MBPP-Incomplete
51.3
↓
\downarrow
-24.5
0 – 5
32.3
42.1
48.7
MBPP-Contradictory
13.8
↓
\downarrow
-62.0
0 – 7
49.7
76.5
86.2
HumanEval-Underspec.
82.9
↓
\downarrow
-1.2
0 – 4
11.0
13.4
17.1
LCB-Underspec.
26.4
↓
\downarrow
-1.7
0 – 9
31.9
48.4
73.6
Detrimental collapse is a blind spot.
As shown in
Table
II
, detrimental semantic collapse is a
major blind spot of clustering-based disambiguation: from 11% to 49.7% of
tasks receive an incorrect solution without triggering a clarifying question.
Moreover, asking questions does not always produce correct results: after one clarification turn, detrimental collapse increases to 37.3%–76.5% on MBPP variants. This is in part because clarifying questions are grounded in the behavioural differences the model itself produces: if two incorrect solutions for example differ only in edge case handling, the clarifying question will concern edge cases rather than the more fundamental source of incorrectness.
Detrimental semantic collapse is a fundamental blind spot of clustering-based disambiguation.
Even when a simulated user provides clarifications, disambiguation fails silently on tasks affected by detrimental collapse: the model converges to a single incorrect interpretation without ever asking a question, returning a wrong solution with full confidence.
VI
Discussion
We now discuss the risks of detrimental collapse in coding models and its implications for existing and future research studies that rely on semantic clustering.
Model uncertainty and inconsistency.
Our results indicate that neither underspecification nor incorrectness implies
inconsistency. We therefore argue that inconsistency should be interpreted for
what it is: an
expression of model uncertainty
.
Prompt underspecification and misunderstanding can each induce model
uncertainty, and we find in RQ1 that underspecification does indeed increase average
inconsistency. Yet our results also reveal that a large fraction of tasks
exhibit detrimental collapse: the model remains highly certain yet ultimately
fails to solve the task correctly.
Risks for clustering-based methods.
A core consequence of our findings is that any semantic clustering-based
detection method has a
blind spot
dependent on the LLM and benchmark.
For disambiguation methods, detrimental collapse risks returning a confidently
incorrect solution for an underspecified task without prompting for
clarification. For correctness estimation, it causes models that are
confidently incorrect to be systematically overvalued.
Ablation.
Semantic clustering is sensitive to the sampling budget
k
k
and the sampling temperature
τ
\tau
. We evaluate the impact of both parameters on detrimental collapse. Our results are shown in
Table
III
.
Sampling budget.
As the cost of frontier LLMs has increased, sampling budgets in existing work
have decreased over time:
[
18
]
evaluated GPT-3.5 at
k
=
25
k=25
,
[
25
]
employed
k
=
10
k=10
for more recent models, and
[
21
]
evaluated at
k
=
5
k=5
. Our ablation (
Table
III
) confirms that larger
k
k
reduces detrimental collapse, and that this trend needs to be reversed to mitigate detrimental collapse. We use
k
=
10
k=10
as our default as a practical
compromise: increasing from
k
=
10
k=10
to
k
=
25
k=25
reduces detrimental collapse by 2.6 percentage points on MBPP and 6.0 percentage points on LiveCodeBench,
but at 2.5
×
\times
the cost. In practical settings, this trade-off is likely to favor lower
k
k
values, given that the incurred cost is proportional to all coding prompting tasks, even those involving fault fixing.
Temperature.
The sampling temperature controls the determinism of an LLM’s output. A temperature close to zero yields near-deterministic outputs, while a temperature close to or above one often deteriorates performance
[
6
]
. Our ablation (
Table
III
) shows that increasing temperature consistently reduces detrimental collapse, from 15.1% to 11.1% on MBPP and from 38.5% to 32.4%
on LiveCodeBench at no additional cost. We use
τ
=
0.8
\tau=0.8
as our default, as it is commonly adopted in code generation benchmarks to maximise performance
[
10
]
.
Practical implications.
Detrimental collapse can be partly mitigated by increasing the sampling budget, but at a direct cost to practitioners. At the time of writing, solving 378 MBPP tasks with Claude Sonnet 4.5 costs approximately $1.30 at
k
=
1
k=1
, $6.52 at
k
=
5
k=5
, $13.04 at
k
=
10
k=10
, and $32.60 at
k
=
25
k=25
. Reducing the risk of missing an interpretation to below 1% (at
δ
=
95
%
\delta=95\%
confidence;
see
Section
III-C
) would require
k
=
300
k=300
, incurring an estimated cost of over $391 per benchmark run. This cost becomes prohibitive in large-scale deployment, where semantic clustering would need to be applied across thousands
of functions.
TABLE III
:
Ablation analysis of sampling parameters on the detrimental collapse of GPT-4.1-mini. We report percentage of task with detrimental collapse (%DC) and the cost of the performed evaluation ($).
MBPP
+
HumanEval
+
LiveCodeBench
%DC
$
%DC
$
%DC
$
Detrimental collapse at different
k
k
k
=
1
k=1
24.1
$0.14
12.1
$0.08
73.1
$0.20
k
=
5
k=5
19.6
$0.72
6.7
$0.41
52.2
$1.02
k
=
10
k=10
11.1
$1.44
3.0
$0.82
32.4
$2.04
k
=
25
k=25
8.5
$3.59
3.0
$2.05
26.4
$5.10
Detrimental collapse at different temperature
τ
\tau
τ
=
0.2
\tau=0.2
15.1
$1.44
6.1
$0.82
38.5
$2.04
τ
=
0.6
\tau=0.6
11.1
$1.44
3.0
$0.82
37.4
$2.04
τ
=
0.8
\tau=0.8
11.1
$1.44
3.0
$0.82
32.4
$2.04
τ
=
1.0
\tau=1.0
10.3
$1.44
3.0
$0.82
30.1
$2.04
VII
Threats to Validity
VII-A
External validity
Our findings are derived from Python code generation tasks which might thus limit the generalization of our finding. We performed our experiments on three popular programming benchmarks (MBPP, HumanEval, and LiveCodeBench). MBPP and HumanEval focus on relatively small self-contained functions, while LiveCodeBench is a collection of competition-level programming tasks. Although these tasks are varied in complexity and topic, they do not cover all possible coding scenarios. We consider that our findings will be amplified in more complex projects, where cost of sampling becomes an even greater concern.
The underspecification in our benchmarks is artificially introduced
[
12
]
. While validated by experts, the types of underspecification might not reflect all forms of underspecification observed in the real world. Furthermore, the concrete instantiation of underspecification might not be representative for real-world underspecification. We however observe that these specification flaws exists in real-world specification and can induce detrimental collapse.
We evaluated three popular state-of-the-art coding models, namely Claude Sonnet 4.5, GPT-4.1-mini, and Qwen3 (32B). This diversity of models and tasks increases confidence that our conclusions are not tied to a specific model or dataset.
VII-B
Internal validity
Our methodology to detect semantic collapse is sensitive to the sampling budget
k
k
. Since we limit the budget to
k
∈
{
1
,
5
,
10
,
25
}
k\in\{1,5,10,25\}
, our method might have prematurely concluded semantic collapse. As these sampling rates are commonly used by existing methods, our results remain practically relevant and represent a true failure mode of semantic clustering-based approaches.
We further employ LLMs to simulate user responses during disambiguation. Real user responses may deviate from simulated ones in practice, and hence our results may not generalize to real user interactions.
Nevertheless,
detrimental collapse will cause clustering-based disambiguation to withhold clarifying questions regardless of the user simulation, as it occurs before
any interaction takes place.
A potential threat is that we sample responses from the LLM provider’s API, which might implement caching mechanisms that reduce output variability. We mitigate this threat by sampling model responses across different sessions and varying the API keys used. In addition, we observe detrimental collapse for both closed- and open-source models, indicating that detrimental collapse is a fundamental property of LLMs rather than an artifact of provider-specific caching mechanisms.
Another potential confounding factor is memorization. The tasks may have been seen during the training, inflating the performance of the LLMs. In this case, detrimental collapse might represent a failure mode of the training process, i.e. the model collapses because of a wrong training signal. However, our findings generalize to a contamination-free subset of LiveCodeBench, indicating that the failure mode persists beyond what have been seen during training.
VII-C
Construct validity
Construct validity concerns the extent to which operationalizations used in the study accurately capture the underlying concepts of interest—namely prompt underspecification, model incoherence, and detrimental semantic collapse.
Incoherence is measured via semantic clustering of generated programs, grouping implementations according to their observed execution behavior on test cases. This operationalization is inherently dependent on the quality of the employed test suites. If test cases are incomplete or fail to distinguish semantically different implementations, distinct behaviors may be grouped into the same cluster, leading to an underestimation of incoherence. Conversely, overly sensitive distinctions in clustering may exaggerate differences that are not semantically meaningful. Thus, the mapping from behavioral equivalence to coherence is only approximate.
Coherence is inferred from output consistency across repeated generations, but such consistency may arise from factors unrelated to semantic understanding. For instance, the use of decoding strategies (e.g., temperature settings), training data biases, or model priors may experience low semantic collapse. Additionally, the analysis is based solely on observable outputs, without access to the model’s internal reasoning processes. As a result, the study cannot distinguish between true semantic collapse—where the model fails to represent alternative interpretations—and cases where multiple interpretations are internally considered but not expressed in the final output.
VIII
Conclusion
Semantic clustering, i.e. grouping LLM-generated programs by their observable
behaviour, is increasingly applied to detect prompt underspecification and model incorrectness in coding tasks. As both are critical challenges in code
generation, understanding the capabilities and limitations of clustering-based approaches is essential.
In this work, we studied the inconsistency of three state-of-the-art coding models under underspecification, and identified
detrimental semantic collapse
as a critical blind spots. Our results show that models collapse detrimentally on a substantial fraction
of tasks, ranging from 3% in HumanEval to over 32% in LiveCodeBench, and that underspecification significantly increases the rate of detrimental
collapse. Crucially, detrimental collapse is not an artifact of correct solutions as previously assumed: models frequently commit to a single incorrect interpretation even when they fail to solve the task, rendering inconsistency-based detection ineffective precisely where it is needed most.
These findings have direct implications for methods that rely on semantic clustering as a proxy for incorrectness or underspecification. Our results show that inconsistency
can be a meaningful signal when present, but its absence cannot be interpreted as evidence of correct specification or solution.
We further demonstrate that the sampling budgets prevalent in the literature are likely insufficient to reliably distinguish collapse from genuine consistency, a gap that cannot be closed by simply increasing
k
k
, given the fundamental statistical limits of finite-sample collapse detection. The practical implication is that developers must spend a significant share
of their budget on resampling and evaluating code candidates to apply clustering-based methods, without gaining substantially more
trust
in their correctness.
We hope these findings prompt the community to revisit the assumptions underlying clustering-based evaluation and disambiguation methods, and to develop detection approaches that remain effective even in the absence of observable inconsistency. This could be for instance achieved by leveraging internal uncertainty signals, reasoning traces, and diversity-aware sampling strategies that may better explore alternative semantic interpretations. Further work is also needed to understand the underlying causes of collapse, establish theoretical limits for finite-sample collapse detection, and develop benchmarks with controlled levels of underspecification.
References
[1]
A. Akli, M. Papadakis, M. Cordy, and Y. L. Traon
(2026)
When prompt under-specification improves code correctness: an exploratory study of prompt wording and structure effects on llm-based code generation
.
CoRR
abs/2604.24712
.
External Links:
Link
,
Document
,
2604.24712
Cited by:
§
IV-A
,
§
IV-A
,
§
V-A
.
[2]
Anthropic
(2025)
Claude sonnet 4.5
.
Note:
Accessed: 2025
External Links:
Link
Cited by:
§I
,
§
IV-C
.
[3]
J. Austin, A. Odena, M. I. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. J. Cai, M. Terry, Q. V. Le, and C. Sutton
(2021)
Program synthesis with large language models
.
CoRR
abs/2108.07732
.
External Links:
Link
,
2108.07732
Cited by:
§I
,
§I
,
§
IV-A
.
[4]
B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J. Lou, and W. Chen
(2023)
CodeT: code generation with generated tests
.
In
The Eleventh International Conference on Learning Representations,
ICLR 2023, Kigali, Rwanda, May 1-5, 2023
,
External Links:
Link
Cited by:
§II
.
[5]
J. Chen, H. Tang, Z. Chu, Q. Chen, Z. Wang, M. Liu, and B. Qin
(2024)
Divide-and-conquer meets consensus: unleashing the power of functions in code generation
.
In
Advances in Neural Information Processing Systems 37: Annual Conference
on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver,
BC, Canada, December 10 - 15, 2024
,
A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang (Eds.)
,
Cited by:
§II
.
[6]
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba
(2021)
Evaluating large language models trained on code
.
CoRR
abs/2107.03374
.
External Links:
Link
,
2107.03374
Cited by:
§I
,
§I
,
§
IV-A
,
§
IV-B
,
§VI
.
[7]
Z. Fan, H. Ruan, S. Mechtaev, and A. Roychoudhury
(2024)
Oracle-guided program selection from large language models
.
In
Proceedings of the 33rd ACM SIGSOFT International Symposium on
Software Testing and Analysis, ISSTA 2024, Vienna, Austria, September
16-20, 2024
,
M. Christakis and M. Pradel (Eds.)
,
pp. 628–640
.
External Links:
Link
,
Document
Cited by:
§II
.
[8]
V. Gervasi, A. Ferrari, D. Zowghi, and P. Spoletini
(2019)
Ambiguity in requirements engineering: towards a unifying framework
.
In
From Software Engineering to Formal Methods and Tools, and Back -
Essays Dedicated to Stefania Gnesi on the Occasion of Her 65th Birthday
,
M. H. ter Beek, A. Fantechi, and L. Semini (Eds.)
,
Lecture Notes in Computer Science
, Vol.
11865
,
pp. 191–210
.
External Links:
Link
,
Document
Cited by:
§I
.
[9]
B. Huang, S. Lu, X. Wan, and N. Duan
(2024)
Enhancing large language models in coding through multi-perspective self-consistency
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand,
August 11-16, 2024
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
pp. 1429–1450
.
External Links:
Link
,
Document
Cited by:
§II
.
[10]
N. Jain, K. Han, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica
(2025)
LiveCodeBench: holistic and contamination free evaluation of large language models for code
.
In
The Thirteenth International Conference on Learning Representations,
ICLR 2025, Singapore, April 24-28, 2025
,
External Links:
Link
Cited by:
§I
,
§
IV-A
,
§
IV-C
,
§VI
.
[11]
H. Jia, R. Morris, H. Ye, F. Sarro, and S. Mechtaev
(2025)
Automated repair of ambiguous problem descriptions for llm-based code generation
.
In
40th IEEE/ACM International Conference on Automated Software Engineering,
ASE 2025, Seoul, Korea, Republic of, November 16-20, 2025
,
pp. 367–379
.
External Links:
Link
,
Document
Cited by:
§I
,
§I
,
§I
,
§II
,
§II
.
[12]
M. Larbi, A. Akli, M. Papadakis, R. Bouyousfi, M. Cordy, F. Sarro, and Y. L. Traon
(2025)
When prompts go wrong: evaluating code model robustness to ambiguous, contradictory, and incomplete task descriptions
.
CoRR
abs/2507.20439
.
External Links:
Link
,
Document
,
2507.20439
Cited by:
§
IV-A
,
§
VII-A
.
[13]
T. Launer, J. Hübotter, M. Bagatella, I. Hakimi, and A. Krause
(2026)
Majority voting for code generation
.
CoRR
abs/2604.15618
.
External Links:
Link
,
Document
,
2604.15618
Cited by:
§II
,
§II
,
§II
.
[14]
H. Li, P. Fernandes, I. Gurevych, and A. F. T. Martins
(2024)
DOCE: finding the sweet spot for execution-based code generation
.
CoRR
abs/2408.13745
.
External Links:
Link
,
Document
,
2408.13745
Cited by:
§II
.
[15]
Y. Li, D. H. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy, C. de Masson d’Autume, I. Babuschkin, X. Chen, P. Huang, J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S. Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals
(2022)
Competition-level code generation with alphacode
.
CoRR
abs/2203.07814
.
External Links:
Link
,
Document
,
2203.07814
Cited by:
§I
,
§II
.
[16]
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
(2023)
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
In
Advances in Neural Information Processing Systems 36: Annual Conference
on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans,
LA, USA, December 10 - 16, 2023
,
A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine (Eds.)
,
External Links:
Link
Cited by:
§
III-C
,
§
IV-A
.
[17]
A. Mavin, P. Wilkinson, A. R. G. Harwood, and M. Novak
(2009)
Easy approach to requirements syntax (EARS)
.
In
RE 2009, 17th IEEE International Requirements Engineering Conference,
Atlanta, Georgia, USA, August 31 - September 4, 2009
,
pp. 317–322
.
External Links:
Link
,
Document
Cited by:
§I
.
[18]
F. Mu, L. Shi, S. Wang, Z. Yu, B. Zhang, C. Wang, S. Liu, and Q. Wang
(2024)
ClarifyGPT: A framework for enhancing llm-based code generation via requirements clarification
.
Proc. ACM Softw. Eng.
1
(
FSE
),
pp. 2332–2354
.
External Links:
Link
,
Document
Cited by:
§I
,
§I
,
§I
,
§II
,
§II
,
§
V-B
,
§
V-C
,
§
V-C
,
§VI
.
[19]
OpenAI
(2023)
GPT-4 technical report
.
CoRR
abs/2303.08774
.
External Links:
Link
,
2303.08774
Cited by:
§I
,
§
IV-C
.
[20]
C. Ravuri and S. Amarasinghe
(2025)
Eliminating hallucination-induced errors in LLM code generation with functional clustering
.
CoRR
abs/2506.11021
.
External Links:
Link
,
Document
,
2506.11021
Cited by:
§II
.
[21]
A. Sharma and C. David
(2025)
Assessing correctness in llm-based code generation via uncertainty estimation
.
CoRR
abs/2502.11620
.
External Links:
Link
,
Document
,
2502.11620
Cited by:
§I
,
§II
,
§VI
.
[22]
F. Shi, D. Fried, M. Ghazvininejad, L. Zettlemoyer, and S. I. Wang
(2022)
Natural language to code translation with execution
.
In
Proceedings of the 2022 Conference on Empirical Methods in Natural
Language Processing, EMNLP 2022, Abu Dhabi, United Arab Emirates,
December 7-11, 2022
,
Y. Goldberg, Z. Kozareva, and Y. Zhang (Eds.)
,
pp. 3533–3546
.
External Links:
Link
,
Document
Cited by:
§I
,
§II
.
[23]
Q. Team
(2025)
Qwen3 technical report
.
CoRR
abs/2505.09388
.
External Links:
Link
,
2505.09388
Cited by:
§I
,
§
IV-C
.
[24]
H. To, M. Nguyen, and N. Bui
(2024)
Functional overlap reranking for neural code generation
.
In
Findings of the Association for Computational Linguistics, ACL 2024,
Bangkok, Thailand and virtual meeting, August 11-16, 2024
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Findings of ACL
, Vol.
ACL 2024
,
pp. 3686–3704
.
External Links:
Link
,
Document
Cited by:
§II
.
[25]
T. J. Valentin, A. Madadi, G. Sapia, and M. Böhme
(2026)
Incoherence as oracle-less measure of error in llm-based code generation
.
In
Fortieth AAAI Conference on Artificial Intelligence, Thirty-Eighth
Conference on Innovative Applications of Artificial Intelligence,
Sixteenth Symposium on Educational Advances in Artificial Intelligence,
AAAI 2026, Singapore, January 20-27, 2026
,
S. Koenig, C. Jenkins, and M. E. Taylor (Eds.)
,
pp. 33305–33313
.
External Links:
Link
,
Document
Cited by:
§I
,
§II
,
§
III-C
,
§
IV-B
,
§
V-B
,
§VI
.
[26]
X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou
(2023)
Self-consistency improves chain of thought reasoning in language models
.
In
The Eleventh International Conference on Learning Representations,
ICLR 2023, Kigali, Rwanda, May 1-5, 2023
,
External Links:
Link
Cited by:
§II
.
[27]
J. J. Wu, M. Chaudhary, D. Abrahamyan, A. Khaku, A. Wei, and F. H. Fard
(2025)
ClarifyCoder: clarification-aware fine-tuning for programmatic problem solving
.
CoRR
abs/2504.16331
.
External Links:
Link
,
Document
,
2504.16331
Cited by:
§II
,
§II
.
[28]
H. Zhang, W. Cheng, and W. Hu
(2026)
Self-improving code generation via semantic entropy and behavioral consensus
.
CoRR
abs/2603.29292
.
External Links:
Link
,
Document
,
2603.29292
Cited by:
§II
,
§II
.
[29]
Z. Zheng, K. Ning, Q. Zhong, J. Chen, W. Chen, L. Guo, W. Wang, and Y. Wang
(2025)
Towards an understanding of large language models in software engineering tasks
.
Empir. Softw. Eng.
30
(
2
),
pp. 50
.
External Links:
Link
,
Document
Cited by:
§I
.