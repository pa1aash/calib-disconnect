---
title: Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation
id: using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation
tags:
- code-llm-confidence-positioning-d82d00
- code-uncertainty
- sample-based-uncertainty
- execution-ground-truth
created: '2026-11-09T23:07:25.935675Z'
updated: '2026-11-09T23:27:44.354038Z'
source: https://arxiv.org/html/2605.09023
source_domain: arxiv.org
fetched_at: '2026-11-09T23:07:25.935222Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'CLOSE for L1: execution-graded confidence estimation on LiveCodeBench, but
  sample-based black-box estimators only; no release-date contamination split, no
  probes. Full text (arXiv HTML). arXiv 2605.09023, full text. Gives a four-axis taxonomy
  (equivalence proxy, aggregation structure, reference behaviour, dissimilarity) of
  sample-based code uncertainty estimators and proposes semantic-distance-aware estimators
  SDE and DSDE (K=10 samples, N=10 fuzz inputs, T=0.6, weights (1,0.8,0.6)). Evaluated
  on LiveCodeBench (primary), MBPP, HumanEval-X (Python/Java/C++), BigCodeBench with
  GPT-3.5-Turbo (pass@1 30.83%), GPT-4o-mini (49.24%), Gemini-2.5-Flash-Lite (60.53%),
  Claude Opus 4.5 (82.73%) and DeepSeek-Coder-V2 (38.14%). Labels: pass@1 (AUROC)
  and partial_pass@1 (Pearson, Spearman). DSDE AUROC above 0.8 in every setting; runtime
  reduction approx 48-79%. Closed API models, no model internals, no verbal or hidden-state
  readouts, no base/instruct contrast, no calibration (ECE) metric, no contamination-controlled
  release-date split documented. Occupies execution-graded sampled-readout evaluation;
  does not occupy probe-vs-verbal or measurement foundation with contamination control.'
---

Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2605.09023v1 [cs.SE] 09 May 2026
Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation
Weilin He
Affiliation:
University of Bristol
Email:
te23071@bristol.ac.uk
Arindam Sharma
Affiliation:
University of Bristol
Email:
arindam.sharma@bristol.ac.uk
Cristina David
Affiliation:
University of Bristol
Email:
cristina.david@bristol.ac.uk
Abstract
LLMs show strong performance in code generation, but their outputs lack
correctness guarantees. Sample-based uncertainty estimators
address this by generating multiple candidate programs and measuring
their disagreement. However, existing estimators make different design
choices about how behaviours are identified, aggregated, referenced
and compared, making them difficult to assess. We therefore
first introduce a taxonomy that disentangles these choices and reveals
a missing design point:
semantic distance-aware uncertainty estimation
, which measures
not only whether sampled programs disagree, but how severely their
execution behaviours differ.
Across
LiveCodeBench, MBPP, HumanEval-X and BigCodeBench, spanning Python, Java and C++, our metrics provide
strong proxies for correctness, and consistently outperform state-of-the-art
sample-based baselines across both closed-source models (GPT-3.5-Turbo, GPT-4o-mini, Gemini-2.5-Flash-Lite, Claude Opus 4.5) and an open-source model (DeepSeek-Coder-V2). The method is practical: it requires neither
model internals nor LLM-as-judge calls, remains robust across models,
languages, sampling temperatures and fuzzing settings, and reduces
runtime by approximately
48
48
–
79
%
79\%
relative to existing baselines.
1
Introduction
The adoption of Large Language Models (LLMs) in software engineering
has been rapid, with the volume of LLM-generated code projected to
increase further
[
6
]
. As such, the
well-known problem of hallucinations now threatens the reliability of
critical software systems
[
19
]
,
spurring a growing body of work on assessing the correctness of
LLM-generated code
[
9
]
.
Yet, in many settings, external validation is unavailable or
incomplete: generated programs may lack reference implementations or
complete test suites
[
13
,
21
,
22
]
.
A common reference-free strategy is to estimate uncertainty
[
14
]
from
disagreement
across multiple independently sampled outputs. In
natural language generation, such methods interpret variation across
samples as a signal of epistemic
uncertainty
[
7
,
16
,
1
]
. Recent work adapts the same principle to code
generation
[
17
,
23
,
24
]
, using signals that range from static
analysis of program text to dynamic comparison of execution
behaviour.
A four-axis taxonomy of sample-based uncertainty estimators.
Although many uncertainty estimators now exist, they are
difficult to compare directly: they combine different notions of
equivalence, aggregation, reference behaviour and disagreement. Our
first contribution is therefore a taxonomy that makes these choices
explicit.
At a high level, the methods in Table
1
share
a common sample-and-aggregate structure: they sample
K
K
candidate
outputs, identify or compare behaviours using some proxy for
equivalence, and aggregate the resulting evidence into a scalar
uncertainty score. We organise this design space along four axes:
equivalence proxy
,
aggregation structure
,
reference behaviour
and
dissimilarity
.
Equivalence proxy
specifies how candidate outputs are represented
or grouped into behaviours. Existing methods use a range of proxies,
including NLI- or LLM-based equivalence judgements
[
20
]
, syntactic and data-flow
heuristics
[
17
]
, symbolic execution
[
23
]
, execution-based grouping on shared
inputs
[
24
]
, exact string
matching
[
25
]
, and embedding similarity
[
18
]
.
Aggregation structure
specifies whether uncertainty is computed
from marginal behaviour probabilities or from pairwise comparisons
between behaviours. Marginal methods
[
7
,
23
,
25
]
summarise
how probability mass is spread across behaviours, without asking
whether two behaviours are semantically close or far apart. Pairwise
methods
[
20
,
8
,
17
,
24
,
18
]
, by
contrast, explicitly compare behaviours.
Reference behaviour
applies to pairwise methods and specifies
which behaviours are compared. Some methods aggregate over all pairs
(
uniform-pairwise
)
[
20
,
17
,
18
]
; some compare the dominant
behaviour against alternatives (
top-anchored
)
[
24
]
; and some compare only the
top-ranked output against alternatives while discarding alternative
probabilities (
top1-only
)
[
8
]
.
Dissimilarity
applies to pairwise methods and specifies how
differences between compared behaviours are scored. Existing pairwise
methods use a binary or shallow notion of disagreement: two behaviours
either agree or disagree
[
20
,
8
,
24
]
. Marginal methods, such
as Semantic Entropy
[
7
]
, do not use an
inter-behaviour dissimilarity at all.
Table 1
:
Representative sample-based uncertainty estimators positioned
along four design axes.
Equiv. proxy
denotes how outputs are
represented or grouped into behaviours.
Aggregation
is marginal
or pairwise.
Reference
specifies which behaviours are compared
for pairwise methods.
Dissimilarity
specifies how compared
behaviours are scored; N/A indicates that no pairwise comparison is
used.
Method
Equiv. proxy
Aggregation
Reference
Dissimilarity
Semantic Entropy
[
7
,
16
]
NL-Entailment
marginal
N/A
N/A
Symbolic equiv.
[
23
]
symbolic execution
marginal
N/A
N/A
Self-Consistency
[
25
]
exact string match
marginal
N/A
N/A
SelfCheckGPT
[
20
]
NL-LLM
pairwise
uniform-pairwise
binary
ChainPoll
[
8
]
LLM voting
pairwise
top1-only
binary
HonestCoder
[
17
]
multi-modal heuristic
pairwise
uniform-pairwise
binary
DiffTrust
[
24
]
execution fuzz
pairwise
top-anchored
binary
EigenScore
[
18
]
NL-Embedding
pairwise
uniform-pairwise
binary
SDE (ours)
execution fuzz
pairwise
uniform-pairwise
graded
DSDE (ours)
execution fuzz
pairwise
top-anchored
graded
Limitation of existing methods.
By separating design choices, the taxonomy makes prior methods easier to
compare and exposes a key limitation:
existing estimators provide only
a coarse account of behavioural difference.
Marginal methods collapse uncertainty to the distribution of
mass over behaviours, without asking whether those behaviours are
semantically close or far apart. Pairwise methods do compare
behaviours, but typically only through a binary or shallow
agree/disagree signal. As a result,
two programs that differ on one input out of ten may be treated like
two programs that disagree on every input. This is a poor abstraction
for code, where behavioural differences are often graded
[
27
]
. A useful sample-based uncertainty estimator should
therefore capture not only whether sampled programs disagree, but also
how severely they disagree.
Our approach.
Our key observation is that programs, unlike free-form natural
language, are executable objects. This makes semantic difference
directly measurable: two programs can be compared by how often, and in
what ways, their executions differ on shared inputs.
We therefore propose
semantic distance-aware
uncertainty estimation
. Instead of treating all behavioural
disagreements as equally severe, we assign graded dissimilarities
between execution behaviours and aggregate them into uncertainty
scores. The framework is agnostic to the equivalence proxy: any
procedure that identifies behaviourally equivalent programs can be
used. In this paper, we use fuzzing:
unlike lightweight static
proxies
[
17
]
, it captures observable program behaviour, while avoiding the
substantial cost of more principled static techniques such as symbolic
execution
[
23
]
.
We define two metrics, corresponding to two reference behaviours.
SDE uses uniform-pairwise aggregation, grounded in Rao’s quadratic
entropy, and measures global behavioural diversity across sampled
programs. DSDE uses top-anchored aggregation, measuring how strongly
the alternatives disagree with the dominant behaviour containing the
top-ranked program. The former is suited to task- or model-level
uncertainty, while the latter targets the reliability of the specific
output shown to the user.
In summary, the contributions of this paper are as follows:
•
We introduce a four-axis
taxonomy of sample-based uncertainty
estimators
, making existing methods easier to compare and
clarifying which design choices distinguish them.
•
We propose
semantic distance-aware uncertainty metrics
as a
proxy for correctness in code generation. On
LiveCodeBench
, our metrics achieve
strong
discrimination between correct and incorrect solutions
, with
AUROC
>
0.8
>0.8
.
•
We provide extensive evidence of generalisation across
benchmarks, languages, models, and sampling regimes. Beyond
LiveCodeBench
, our metrics remain effective on
MBPP
[
2
]
,
BigCodeBench
[
29
]
and
HumanEval-X
[
28
]
; across
Python
,
Java
and
C++
; across closed-source and open-weights models;
and under varying task difficulties and sampling temperatures.
•
We show that distance-aware uncertainty is
cost-effective
relative to strong state-of-the-art
uncertainty estimation baselines: our metrics substantially improve predictive
performance while reducing runtime by approximately
48
48
–
79
%
79\%
.
2
Distance-Aware Uncertainty Measures
We now formalise the three components needed to compute our
distance-aware uncertainty scores: semantic clusters, distances between
clusters, and the aggregation rules that turn these distances into a
scalar uncertainty estimate. The clustering step is not specific to
our metric: any procedure that partitions candidate programs into
behaviourally equivalent groups can be used. In this paper, we use
execution signatures over a shared input set, which provides a simple
and practical instantiation.
Setup: Semantic Clusters.
Given a task description
d
d
, let
Π
=
{
π
1
,
…
,
π
K
}
\Pi=\{\pi_{1},\ldots,\pi_{K}\}
be
K
K
candidate programs sampled from a
stochastic code-generation model. Let
ℐ
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
\mathcal{I}=(x_{1},\ldots,x_{N})
be a fixed set of inputs shared across
all candidates. Executing a program
π
\pi
on
ℐ
\mathcal{I}
yields its
execution signature
σ
ℐ
​
(
π
)
=
(
o
1
​
(
π
)
,
…
,
o
N
​
(
π
)
)
\sigma_{\mathcal{I}}(\pi)=\bigl(o_{1}(\pi),\ldots,o_{N}(\pi)\bigr)
,
where
o
k
​
(
π
)
o_{k}(\pi)
is the observed outcome of
π
\pi
on input
x
k
x_{k}
.
An outcome is either a normal output value or an abnormal termination
labelled by its error type.
Programs are placed in the same semantic cluster iff their execution
signatures are identical. Let
{
C
1
,
…
,
C
M
}
\{C_{1},\ldots,C_{M}\}
be the resulting
partition of
Π
\Pi
. The empirical cluster probability is
p
i
=
|
C
i
|
K
p_{i}=\frac{|C_{i}|}{K}
, with
∑
i
=
1
M
p
i
=
1
\sum_{i=1}^{M}p_{i}=1
.
2.1
Semantic Distance
We next define a graded distance between semantic clusters. Since all
programs in a cluster have the same execution signature on
ℐ
\mathcal{I}
, the distance between two clusters is independent of the
choice of representatives.
For any
π
∈
C
i
\pi\in C_{i}
and
π
′
∈
C
j
\pi^{\prime}\in C_{j}
, the semantic distance between
clusters
C
i
C_{i}
and
C
j
C_{j}
is
d
i
​
j
=
1
N
​
∑
k
=
1
N
δ
⁡
(
o
k
​
(
π
)
,
o
k
​
(
π
′
)
)
.
d_{ij}=\frac{1}{N}\sum_{k=1}^{N}\delta\bigl(o_{k}(\pi),o_{k}(\pi^{\prime})\bigr).
(1)
The per-input outcome distance
δ
⁡
(
o
,
o
′
)
∈
[
0
,
1
]
\delta(o,o^{\prime})\in[0,1]
is defined as
δ
⁡
(
o
,
o
′
)
=
{
0
if
o
and
o
′
are equal normal outputs,
1
if both outcomes are normal and
o
≠
o
′
,
a
if exactly one outcome is abnormal,
b
if both outcomes are abnormal with different error types,
c
if both outcomes are abnormal with the same error type.
\delta(o,o^{\prime})=\begin{cases}0&\text{if $o$ and $o^{\prime}$ are equal normal outputs,}\\
1&\text{if both outcomes are normal and $o\neq o^{\prime}$,}\\
a&\text{if exactly one outcome is abnormal,}\\
b&\text{if both outcomes are abnormal with different error types,}\\
c&\text{if both outcomes are abnormal with the same error type.}\end{cases}
(2)
where
a
,
b
,
c
∈
[
0
,
1
]
a,b,c\in[0,1]
are graded disagreement costs. We treat these
values as hyperparameters because abnormal executions do not induce a
canonical semantic distance: identical errors may indicate related
failure modes, but need not imply behavioural equivalence. We use a
fixed default in the main experiments (see §
4.1
) and assess sensitivity in
§
4.5
.
By construction,
d
i
​
j
d_{ij}
is symmetric, satisfies
d
i
​
i
=
0
d_{ii}=0
, and lies
in
[
0
,
1
]
[0,1]
.
2.2
Uncertainty Metrics
Given semantic clusters
{
C
1
,
…
,
C
M
}
\{C_{1},\ldots,C_{M}\}
, empirical probabilities
{
p
1
,
…
,
p
M
}
\{p_{1},\ldots,p_{M}\}
, and pairwise distances
{
d
i
​
j
}
\{d_{ij}\}
, we define
two distance-aware uncertainty metrics. They share the same clustering
and distance definitions, but differ in their anchor: one aggregates
globally over all cluster pairs, while the other anchors uncertainty
to the cluster containing the top-ranked output.
Semantic Distance Entropy (SDE).
Our first measure is a symmetric distance-aware estimator inspired by
Rao’s quadratic entropy, weighting each cluster pair by the product of
cluster probabilities and their semantic distance:
S
​
D
​
E
=
∑
i
<
j
p
i
​
p
j
​
d
i
​
j
.
SDE=\sum_{i<j}p_{i}\,p_{j}\,d_{ij}.
(3)
SDE captures global behavioural diversity: it is large when
substantial probability mass is spread across clusters that are far
apart in execution behaviour.
Dominant Semantic Distance Entropy (DSDE).
In deployment, users typically inspect or rely on the model’s
top-ranked output
[
5
]
. We therefore define a
top-anchored variant that measures uncertainty relative to the
behaviour that would actually be served. Let
c
∗
∈
{
1
,
…
,
M
}
c^{*}\in\{1,\ldots,M\}
be the index of the cluster containing the
top-ranked program
π
1
\pi_{1}
, so that
C
c
∗
=
C
⁡
(
π
1
)
C_{c^{*}}=C(\pi_{1})
. We define
D
​
S
​
D
​
E
=
∑
i
≠
c
∗
p
i
​
d
c
∗
,
i
.
DSDE=\sum_{i\neq c^{*}}p_{i}\,d_{c^{*},i}.
(4)
DSDE measures how strongly the alternatives disagree with the
top-ranked behaviour, weighted by the empirical probability of each
alternative. Unlike SDE, which treats all cluster pairs
symmetrically, DSDE is targeted at the reliability of the specific
output shown to the user.
3
Overview of the Approach
We present an end-to-end evaluation pipeline for execution-based
uncertainty estimation in code generation, which consists of four main stages:
First stage: Candidate program sampling.
Given a programming task described by natural language input
d
d
,
let
Coder
​
(
⋅
)
\text{Coder}(\cdot)
denote a code generation system.
Without access to reference implementations or model internals,
the system independently samples
K
K
candidate programs
{
π
1
,
π
2
,
…
,
π
K
}
,
π
k
∼
p
⁡
(
π
∣
d
)
,
\{\pi_{1},\pi_{2},\ldots,\pi_{K}\},\pi_{k}\sim p(\pi\mid d),
where each
π
k
\pi_{k}
corresponds to the raw code returned by API call.
Second stage: Fuzzing-based input generation.
Starting from an initial set of valid task inputs, we generate fuzzed
inputs using a lightweight, type-aware mutation strategy designed for
the heterogeneous input spaces common in code-generation benchmarks.
We apply structure-preserving, type-specific mutations iteratively
until
N
N
executable fuzzed inputs are obtained, providing behavioural
variation for execution-based equivalence and uncertainty estimation.
By default, we follow Valentin et al.
[
24
]
and use benchmark-provided test cases as seed inputs. However, our
pipeline does not rely on such seeds: in §
4.5
, we show that
a seed-free variant remains effective.
We also report input-quality
diagnostics for the resulting fuzz suites, including validity,
uniqueness, and coverage, in Appendix
A
.
More generally, the pipeline is
fuzzer-agnostic
: the input-generation component can be replaced
by any suitable fuzzing strategy, allowing us to inherit advances from
the fuzzing community. For example, in §
4.3
, we use
whitebox fuzzing
[
10
]
for BigCodeBench.
Third stage: Execution-based representation and clustering.
Let
𝐢
=
(
i
1
,
i
2
,
…
,
i
N
)
\mathbf{i}=(i_{1},i_{2},\ldots,i_{N})
denote the set of test inputs associated
with the task, where
N
N
is the number of inputs.
This input set is shared across all candidate programs
𝝅
=
(
π
1
,
π
2
,
…
,
π
K
)
\boldsymbol{\pi}=(\pi_{1},\pi_{2},\ldots,\pi_{K})
.
Each candidate program
π
k
\pi_{k}
is executed on all inputs in
𝐢
\mathbf{i}
, yielding
an execution output vector
𝐨
k
=
(
π
k
​
(
i
1
)
,
π
k
​
(
i
2
)
,
…
,
π
k
​
(
i
N
)
)
.
\mathbf{o}_{k}=\bigl(\pi_{k}(i_{1}),\pi_{k}(i_{2}),\ldots,\pi_{k}(i_{N})\bigr).
Candidate programs are clustered according to behavioural equivalence: programs
with identical execution signatures are assigned to the same behavioural cluster.
For abnormal executions, programs are grouped into the same cluster if they
terminate with the same error.
Fourth stage: Uncertainty computation.
Based on the semantic clusters, we compute SDE and DSDE.
4
Experiments
In this section, we will evaluate our distance-aware uncertainty metrics.
Our experiments are designed to answer the following questions:
RQ1 (Predictive Performance).
Do distance-aware uncertainty metrics reliably estimate program correctness, and how do they
compare to existing
baselines
[
24
,
17
,
7
]
?
RQ2 (Generalisation).
Do distance-aware uncertainty metrics transfer across benchmarks of varying difficulty and
scale, programming languages, sampling temperatures and model
families?
RQ3 (Cost-effectiveness).
Are distance-aware uncertainty metrics cheap enough for inference-time deployment under
aggressive sample budgets and competitive against runtime baselines?
RQ4 (Robustness to design choices).
Do distance-aware uncertainty metrics remain reliable under different design choices, including
fixed versus tuned distance weights and the absence of
benchmark-provided test inputs?
4.1
Experimental Setup
Models.
We conduct experiments using representative code generation models
spanning different capability tiers: GPT-3.5-Turbo (low), GPT-4o-mini
(medium), Gemini-2.5-Flash-Lite (medium), and Claude Opus 4.5 (high),
with respective
pass@1
success rates of 30.83%, 49.24%, 60.53%,
and 82.73% on
LiveCodeBench
. To assess generalisation
(§
4.3
), we additionally use the open-weights model
DeepSeek-Coder-V2 (
pass@1
38.14% on
LiveCodeBench
).
Datasets.
We evaluate on four complementary benchmarks spanning different
task difficulties and programming languages.
Our primary benchmark is
LiveCodeBench
(LCB)
[
15
]
(Python). To assess generalisation
(§
4.3
), we additionally use
MBPP
[
2
]
(Python),
HumanEval-X
[
28
]
(Python, Java,
and C++), and
BigCodeBench
[
29
]
(Python). Detailed statistics and task descriptions are in
Appendix
C.3
.
Experimental configuration.
Unless otherwise specified, we sample with temperature
T
=
0.6
T=0.6
following prior code-generation work
[
17
,
11
]
, generate
K
=
10
K=10
candidate programs per task, and
evaluate them on
N
=
10
N=10
fuzz inputs with a
0.2
0.2
s per-input
execution timeout. We use
(
a
,
b
,
c
)
=
(
1
,
0.8
,
0.6
)
(a,b,c)=(1,0.8,0.6)
from §
2.1
; a sensitivity analysis shows the fixed weights deviate by less than
0.011
0.011
AUROC from per-setting learned weights, more details can be found in §
4.4
.
All experiments are run on an Apple M4 Pro with
24 GB of RAM.
Prediction targets.
Following prior work
[
5
]
, we adopt
pass@1
as a primary
correctness signal, capturing whether the model succeeds on its first attempt.
Since
pass@1
is binary, it does not distinguish near-correct programs from
substantially incorrect ones. We therefore use
partial_pass@1
as a
complementary, graded execution-based target, defined as the proportion of
test cases passed by the first sampled program, as in
[
23
]
.
This provides a useful measure of
partial correctness
.
Evaluation metrics.
For
pass@1
, which is a binary outcome, we evaluate how well uncertainty scores
discriminate
between correct and incorrect generations using the area
under the ROC curve (AUROC)
[
4
]
.
For the continuous-valued
partial_pass@1
,
we assess its association with uncertainty scores using Pearson
[
3
]
and Spearman
[
26
]
correlation coefficients, capturing linear and monotonic relationships, respectively.
4.2
Answering RQ1 (Predictive Performance)
pass@1
and
partial_pass@1
prediction.
Table
2
reports AUROC for
pass@1
failure
prediction and Pearson
r
r
/Spearman
ρ
\rho
correlations with
partial_pass@1
on
LiveCodeBench
. Across all four models, SDE and
DSDE provide strong predictive signals: DSDE achieves AUROC above
0.8
0.8
in every setting, and both metrics correlate negatively with
partial_pass@1
, indicating that higher uncertainty corresponds to lower
partial correctness.
On the main closed-source LiveCodeBench evaluation,
DSDE improves over SDE across all models and metrics, supporting
the top-anchored design: when assessing the program
shown to the user, uncertainty can be more informative when measured
relative to that program’s behaviour rather than averaged uniformly
across all samples. This advantage may depend on
the first sample being representative; when it is not, as suggested by
DeepSeek-Coder-V2 in Table
3
, the symmetric
SDE estimator can be more stable.
Comparison with baselines.
We compare against three strong baselines, chosen to cover
the main existing design choices in Table
1
:
DiffTrust, the state-of-the-art incoherence-based proxy
[
24
]
;
HonestCoder, a representative confidence estimator combining embeddings,
data-flow signatures, and syntactic
n
n
-grams
[
17
]
;
and Semantic Entropy, the standard entropy-based uncertainty estimator
over LLM-judged semantic clusters
[
7
]
. As
shown in Table
2
, even these competitive baselines
are only weakly informative on
LiveCodeBench
. By contrast,
SDE and DSDE outperform every baseline on every model and metric,
suggesting that graded semantic distance captures correctness-relevant
information missed by binary disagreement and marginal entropy-based
uncertainty.
Table 2
:
Performance of SDE, DSDE, and the three
baselines on
LiveCodeBench
across models (
T
=
0.6
T=0.6
). Best
result per metric per row is shown in bold. AUC denotes AUROC;
r
r
and
ρ
\rho
are Pearson and Spearman correlations with
partial_pass@1
, respectively.
Per-difficulty breakdowns (Easy/Medium/Hard) are reported in
Appendix
C.1
.
SDE
DSDE
DiffTrust
HC
Semantic Entropy
Model
AUC
r
r
ρ
\rho
AUC
r
r
ρ
\rho
AUC
r
r
ρ
\rho
AUC
r
r
ρ
\rho
AUC
r
r
ρ
\rho
GPT-3.5-Turbo-0125
0.827
−
-
0.587
−
-
0.581
0.844
−
-
0.622
−
-
0.620
0.669
−
-
0.259
−
-
0.267
0.646
−
-
0.344
−
-
0.328
0.605
−
-
0.240
−
-
0.237
GPT-4o-mini
0.826
−
-
0.589
−
-
0.584
0.844
−
-
0.624
−
-
0.624
0.534
−
-
0.024
−
-
0.064
0.646
−
-
0.344
−
-
0.328
0.607
−
-
0.240
−
-
0.238
Gemini-2.5-Flash-Lite
0.794
−
-
0.494
−
-
0.491
0.808
−
-
0.532
−
-
0.512
0.688
−
-
0.296
−
-
0.298
0.668
−
-
0.301
−
-
0.329
0.639
−
-
0.237
−
-
0.242
Claude-opus-4.5
0.818
−
-
0.552
−
-
0.450
0.825
−
-
0.611
−
-
0.461
0.606
−
-
0.139
−
-
0.139
0.739
−
-
0.424
−
-
0.350
0.687
−
-
0.275
−
-
0.287
4.3
Answering RQ2 (Generalisation)
Across benchmarks of varying difficulty.
The first block of Table
3
evaluates SDE
and DSDE on three Python benchmarks spanning entry-level function
completion (MBPP), competitive programming (
LiveCodeBench
), and
repository-scale tasks (BigCodeBench). Both metrics retain strong
predictive performance on MBPP and
LiveCodeBench
, with AUROC above
0.75
0.75
and Spearman correlations close to
−
0.6
-0.6
.
Beyond function-level benchmarks: BigCodeBench.
BigCodeBench is the most demanding benchmark we consider and, to our
knowledge, the first repository-scale evaluation of
sample-based uncertainty estimation for LLM-generated code.
Its tasks include cross-file
dependencies, side effects, stochastic operations, and often a range
of valid outputs for the same specification. This makes exact-match
execution clustering too brittle: semantically valid programs may
produce different concrete outputs and be incorrectly separated.
Our formulation can accommodate this setting because it is agnostic with respect to
the clustering proxy. We therefore make
a single drop-in change: instead of clustering by exact output match,
we use whitebox fuzzing
[
10
]
to target
specification predicates and group programs by predicate satisfaction.
With this adaptation, DSDE achieves AUROC
0.668
0.668
and Spearman
ρ
=
−
0.335
\rho=-0.335
on BigCodeBench. Although lower than on function-level
benchmarks, this remains a non-trivial signal in a substantially more
challenging repository-scale regime.
Across programming languages.
On HumanEval-X
[
28
]
, covering Python, Java, and
C++, both metrics perform consistently across languages without
language-specific tuning.
Across sampling temperatures.
We sweep the sampling temperature
T
∈
{
0.2
,
0.6
,
0.8
}
T\in\{0.2,0.6,0.8\}
using
GPT-4o-mini on
LiveCodeBench
. As shown in Table
3
,
performance improves with temperature: lower temperatures reduce
sample diversity, while higher temperatures expose richer behavioural
variation for uncertainty estimation. Nevertheless, SDE and DSDE
remain informative across all settings, indicating that distance-aware
uncertainty benefits from, but does not depend on, high sampling
diversity.
Across model families.
Finally, we evaluate on the open-weights DeepSeek-Coder-V2 model,
which achieves
pass@1
of
38.14
%
38.14\%
on
LiveCodeBench
. Both metrics
retain meaningful AUROC and correlations with
partial_pass@1
, showing that
the distance-aware signal transfers beyond the closed-source models
used in RQ1.
Table 3
:
Performance of SDE and DSDE across benchmarks,
languages, sampling temperatures, and model families
(
GPT-4o-mini
,
T
=
0.6
T=0.6
, unless noted). Better of
SDE/DSDE per row in AUROC in bold. Per-difficulty
LiveCodeBench
breakdowns are in
Appendix
C.1
.
AUROC
Pearson
r
r
Spearman
ρ
\rho
Benchmark
SDE
DSDE
SDE
DSDE
SDE
DSDE
Increased difficulty (Python benchmarks, easy to hard)
MBPP
0.751
0.752
−
-
0.480
−
-
0.434
−
-
0.601
−
-
0.595
LiveCodeBench
0.826
0.844
−
-
0.589
−
-
0.624
−
-
0.584
−
-
0.624
BigCodeBench
0.664
0.668
−
-
0.281
−
-
0.287
−
-
0.333
−
-
0.335
Programming languages (HumanEval-X)
Python
0.751
0.757
−
-
0.523
−
-
0.521
−
-
0.631
−
-
0.634
Java
0.740
0.745
−
-
0.509
−
-
0.516
−
-
0.605
−
-
0.603
C++
0.796
0.804
−
-
0.599
−
-
0.619
−
-
0.573
−
-
0.587
Sampling temperature (GPT-4o-mini, LCB)
T
=
0.2
T=0.2
0.780
0.779
−
-
0.538
−
-
0.529
−
-
0.524
−
-
0.522
T
=
0.6
T=0.6
0.826
0.844
−
-
0.589
−
-
0.624
−
-
0.584
−
-
0.624
T
=
0.8
T=0.8
0.837
0.853
−
-
0.612
−
-
0.660
−
-
0.609
−
-
0.646
Open-weights model (LCB)
DeepSeek-Coder-V2
0.778
0.769
−
-
0.483
−
-
0.469
−
-
0.479
−
-
0.462
4.4
Answering RQ3 (Cost-effectiveness)
Scaling
K
K
and
N
N
up to test for further gains.
To check whether allocating a larger budget improves predictive
performance, we extend the sensitivity analysis on a 50-task
LiveCodeBench
subset across all four code-generation models.
Sweeping
K
∈
{
5
,
10
,
15
,
20
}
K\in\{5,10,15,20\}
at fixed
N
=
10
N=10
leaves
DSDE AUROC within
0.024
0.024
of the default
(
K
,
N
)
=
(
10
,
10
)
(K,N)=(10,10)
across all values;
sweeping
N
N
from
10
10
up to
1,000
1{,}000
at fixed
K
=
10
K=10
likewise
produces no measurable trend (Figure
1
).
Both sweeps indicate that scaling
K
K
or
N
N
beyond the default
(
K
,
N
)
=
(
10
,
10
)
(K,N)=(10,10)
yields no measurable predictive gain.
Figure 1
:
Sensitivity of DSDE to the number of fuzz inputs
N
N
on a 50-task
LiveCodeBench
subset, with
K
K
fixed to
10
10
. AUROC,
Pearson
r
r
, and Spearman
ρ
\rho
remain essentially flat across
N
∈
{
10
,
20
,
50
,
100
,
500
,
1000
}
N\in\{10,20,50,100,500,1000\}
for all four
code-generation models.
Scaling
K
K
and
N
N
down to find the minimal viable configuration.
Since enlarging the budget does not help, we instead probe how far
(
K
,
N
)
(K,N)
can be reduced before the predictive signal degrades. We
sweep
K
,
N
∈
{
3
,
5
,
8
,
10
}
K,N\in\{3,5,8,10\}
jointly
(Figure
2
). The smallest configuration
(
K
,
N
)
=
(
3
,
3
)
(K,N)=(3,3)
already yields AUROC
0.783
0.783
, recovering
∼
93
%
{\sim}93\%
of
the AUROC at
(
10
,
10
)
(10,10)
while requiring an order-of-magnitude less
sample and execution cost. Therefore,
(
3
,
3
)
(3,3)
can be adopted as a
cost-effective deployment default for budget-constrained settings.
Figure 2
:
Joint cost-effectiveness analysis of DSDE on
LiveCodeBench
(GPT-4o-mini,
T
=
0.6
T=0.6
), varying
K
∈
{
3
,
5
,
8
,
10
}
K\in\{3,5,8,10\}
and
N
∈
{
3
,
5
,
8
,
10
}
N\in\{3,5,8,10\}
.
Runtime against baselines.
We now compare
end-to-end wall-clock cost against other uncertainty
estimators. Table
4
breaks runtime into:
candidate-program sampling, additional model-side computation
(
Model Cost
, e.g. embeddings or LLM-as-judge calls), fuzz-input
generation, program execution and metric computation. The sampling
cost is shared across methods; the main differences arise from the
additional model-side or execution costs required by each estimator.
At the default
(
K
,
N
)
=
(
10
,
10
)
(K,N)=(10,10)
, our method takes on average
∼
5.7
{\sim}5.7
s per
task, compared with
∼
11
{\sim}11
s for HonestCoder,
∼
13
{\sim}13
s for
Semantic Entropy, and
∼
27
{\sim}27
s for DiffTrust. This is a
∼
79
%
{\sim}79\%
reduction relative to state-of-the-art DiffTrust. With the deployment
default
(
K
,
N
)
=
(
3
,
3
)
(K,N)=(3,3)
, the runtime falls further to
∼
2
{\sim}2
s per
task.
Table 4
:
Per-task runtime breakdown on
LiveCodeBench
with
GPT-4o-mini
.
Method
𝑵
\boldsymbol{N}
Sampling
Model Cost
Fuzzing
Execution
Metric
Total
HonestCoder
—
∼
3
{\sim}3
s
∼
7
{\sim}7
s
—
—
∼
1
{\sim}1
s
∼
11
{\sim}11
s
Semantic Entropy
—
∼
3
{\sim}3
s
∼
10
{\sim}10
s
—
—
<
1
{<}1
ms
∼
13
{\sim}13
s
DiffTrust
1000
∼
3
{\sim}3
s
—
∼
3
{\sim}3
s
∼
20
{\sim}20
s
∼
1
{\sim}1
s
∼
27
{\sim}27
s
Ours
10
∼
3
{\sim}3
s
—
<
5
{<}5
ms
∼
2.7
{\sim}2.7
s
<
1
{<}1
ms
∼
5.7
\boldsymbol{{\sim}5.7}
s
The saving comes from two design choices: (i) distance-aware uncertainty metrics avoid
model costs entirely (no embeddings, no LLM-as-judge); and
(ii) while DiffTrust requires
N
=
1,000
N=1{,}000
test inputs by default
to satisfy the variance bounds of its Monte Carlo incoherence
estimator, our metric is a deterministic pairwise aggregate over
execution clusters and does not depend on a large
N
N
for
statistical guarantees.
4.5
Answering RQ4 (Robustness to Design Choices)
Robustness to graded disagreement costs
(
a
,
b
,
c
)
(a,b,c)
.
The graded disagreement costs
(
a
,
b
,
c
)
(a,b,c)
are fixed to
(
1
,
0.8
,
0.6
)
(1,0.8,0.6)
throughout the experiments above. To quantify the gap between this
fixed scheme and a per-setting tuned alternative, we additionally fit
(
a
,
b
,
c
)
(a,b,c)
via an 80:20 train–test split per model on
LiveCodeBench
at
T
=
0.6
T=0.6
. As shown in Table
5
, the
default and learned schemes differ by less than
0.011
0.011
AUROC across
all four models, indicating that the fixed weights are sufficient on
LiveCodeBench
. In our current experiments, the default setting appears to be stable and strong, but learned weights may still be useful in future settings or datasets with different failure patterns.
Table 5
:
Robustness to distance weights
(
a
,
b
,
c
)
(a,b,c)
: fixed default
(
1.0
,
0.8
,
0.6
)
(1.0,0.8,0.6)
vs. per-setting learned weights on
LiveCodeBench
(
GPT-4o-mini
,
T
=
0.6
T=0.6
, 80:20 train–test
split per model).
Setting
(
a
,
b
,
c
)
(a,b,c)
Default
Learned
Δ
\Delta
Claude Opus 4.5
(
0.90
,
0.90
,
0.25
)
(0.90,0.90,0.25)
0.8248
0.8206
−
-
0.0042
Gemini-2.5-Flash-Lite
(
0.90
,
0.90
,
0.90
)
(0.90,0.90,0.90)
0.8075
0.7974
−
-
0.0101
GPT-3.5-Turbo
(
0.97
,
0.88
,
0.88
)
(0.97,0.88,0.88)
0.8442
0.8395
−
-
0.0047
GPT-4o-mini
(
1.00
,
0.80
,
0.80
)
(1.00,0.80,0.80)
0.8442
0.8524
+
+
0.0082
Robustness under seed-free input generation
(no dataset-provided test inputs).
In contrast to the seeded experiments above (where the fuzzer
mutates benchmark-provided test inputs as initial seeds), we further
evaluate a
seed-free
variant in which the fuzzer never reads
benchmark-provided test cases, expected outputs, or reference
implementations. Parameter types are inferred by a
rule-based parser from the function interface, using type
annotations when available and parameter names or natural-language
hints from the prompt otherwise. Inputs are then sampled from
generic type-level distributions. As shown in
Table
6
, the AUROC degradation is small (at most
0.087
0.087
) and the predictive signal remains substantially above
chance across all benchmarks, confirming that SDE and DSDE are
fuzzer-agnostic.
Table 6
:
Robustness to fuzz-input seeds: AUROC, Pearson, and
Spearman across three fuzzer seeds on
LiveCodeBench
(
GPT-4o-mini
,
T
=
0.6
T=0.6
).
SDE
DSDE
Benchmark
Seed
Seed-free
Δ
\Delta
Seed
Seed-free
Δ
\Delta
MBPP
0.751
0.712
−
0.039
-0.039
0.752
0.711
−
0.041
-0.041
LiveCodeBench
0.826
0.786
−
0.040
-0.040
0.844
0.787
−
0.057
-0.057
HumanEval-X (Python)
0.751
0.705
−
0.046
-0.046
0.757
0.704
−
0.053
-0.053
HumanEval-X (Java)
0.748
0.725
−
0.023
-0.023
0.745
0.731
−
0.014
-0.014
HumanEval-X (C++)
0.796
0.709
−
0.087
-0.087
0.804
0.723
−
0.081
-0.081
Robustness to fuzz-input random seeds.
Here, “seed” refers to the random seed of the fuzz-input generator,
not to the benchmark-provided seed inputs used to initialise fuzzing.
We keep the tasks, prompts, sampled programs, and benchmark-provided
initial inputs fixed, and rerun only the fuzzing step with three
different random seeds. This isolates the effect of randomness in the
mutation process itself.
We re-run the
LiveCodeBench
pipeline on
GPT-4o-mini
(
T
=
0.6
T=0.6
,
K
=
N
=
10
K=N=10
) under three
independent fuzz-input-generator seeds. As shown in
Table
7
, cross-seed standard deviations
are at most
0.0024
0.0024
on AUROC and
0.0050
0.0050
on Spearman for both
SDE and DSDE, indicating that the reported numbers do not
depend on the choice of seed.
Table 7
:
Robustness to fuzz-input-generator randomness on
LiveCodeBench
(
GPT-4o-mini
,
T
=
0.6
T=0.6
,
K
=
N
=
10
K=N=10
).
The random seed controlling fuzz-input mutations is
varied. Results report mean
±
\pm
standard deviation over three
independent fuzz-input-generator seeds.
Metric
AUROC
Pearson
Spearman
SDE
0.8238
±
0.0011
0.8238\pm 0.0011
−
0.5880
±
0.0035
-0.5880\pm 0.0035
−
0.5831
±
0.0022
-0.5831\pm 0.0022
DSDE
0.8413
±
0.0005
\mathbf{0.8413\pm 0.0005}
−
0.6249
±
0.0030
\mathbf{-0.6249\pm 0.0030}
−
0.6240
±
0.0023
\mathbf{-0.6240\pm 0.0023}
5
Limitations
Our framework inherits several limitations from its underlying
assumptions. (i)
Equivalence proxy.
Effectiveness depends on the proxy
exposing meaningful behavioural differences; weak fuzz inputs may yield
overly coarse equivalence classes.
(ii)
Fuzzing is not a correctness oracle.
Two incorrect
programs may agree on all sampled inputs but diverge elsewhere, and
two valid programs may disagree when the specification admits
multiple acceptable behaviours, as seen on BigCodeBench.
(iii)
Top-ranked reference.
When the top-ranked sample is
unrepresentative of the model’s behavioural distribution, anchoring
becomes unstable, consistent with our DeepSeek-Coder-V2 result
where SDE slightly outperforms DSDE.
(iv)
Heuristic graded distance.
The abnormal-execution costs
(
a
,
b
,
c
)
(a,b,c)
are hyperparameters with no canonical value across
failure modes. Weights may need adaptation for other runtimes,
languages, or benchmarks.
6
Conclusions
We introduced a four-axis taxonomy of sample-based uncertainty
estimators (Table
1
) and identified an
unoccupied region: pairwise uncertainty estimation with graded
semantic dissimilarity. We instantiated this region with two estimators:
SDE, a symmetric Rao quadratic entropy over execution clusters,
and DSDE, a top-anchored variant measuring disagreement between
alternative samples and the served output. Both improve predictive
performance over sample-based baselines at lower computational cost,
and remain stable across benchmarks, languages, temperatures and
fuzzing settings.
References
[1]
Y. Abbasi-Yadkori, I. Kuzborskij, A. György, and C. Szepesvari
(2024)
To believe or not to believe your llm: iterative prompting for estimating epistemic uncertainty
.
In
The Thirty-eighth Annual Conference on Neural Information Processing Systems
,
Cited by:
§1
.
[2]
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
Table 12
,
3rd item
,
§4.1
.
[3]
J. Benesty, J. Chen, Y. Huang, and I. Cohen
(2009)
Pearson correlation coefficient
.
In
Noise Reduction in Speech Processing
,
Springer Topics in Signal Processing
, Vol.
2
,
pp. 1–37
.
External Links:
Document
,
ISBN 978-3-642-00296-0
Cited by:
§4.1
.
[4]
A. P. Bradley
(1997)
The use of the area under the ROC curve in the evaluation of machine learning algorithms
.
Pattern Recognition
30
(
7
),
pp. 1145–1159
.
External Links:
ISSN 0031-3203
,
Document
Cited by:
§4.1
.
[5]
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
et al.
(2021)
Evaluating large language models trained on code
.
External Links:
2107.03374
,
Link
Cited by:
§2.2
,
§4.1
.
[6]
V. M. de Brito and K. Farias
(2025)
Understanding the role of large language models in software engineering: evidence from an industry survey
.
External Links:
2512.21347
,
Link
Cited by:
§1
.
[7]
S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal
(2024)
Detecting hallucinations in large language models using semantic entropy
.
Nature
630
(
8017
),
pp. 625–630
.
External Links:
Document
Cited by:
§C.1
,
§1
,
§1
,
Table 1
,
§1
,
§4.2
,
§4
.
[8]
R. Friel and A. Sanyal
(2023)
ChainPoll: a high efficacy method for llm hallucination detection
.
Note:
arXiv preprint arXiv:2310.18344
External Links:
Link
Cited by:
§1
,
§1
,
§1
,
Table 1
.
[9]
C. Gao, G. Fan, C. Y. Chong, S. Chen, C. Liu, D. Lo, Z. Zheng, and Q. Liao
(2025)
A systematic literature review of code hallucinations in llms: characterization, mitigation methods, challenges, and future directions for reliable ai
.
External Links:
2511.00776
,
Link
Cited by:
§1
.
[10]
P. Godefroid, M. Y. Levin, D. A. Molnar,
et al.
(2008)
Automated whitebox fuzz testing.
.
In
Ndss
,
Vol.
8
,
pp. 151–166
.
Cited by:
§3
,
§4.3
.
[11]
D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi, X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao, Z. Li, Z. Gao, A. Liu, B. Xue, B. Wang, B. Wu, B. Feng, C. Lu, C. Zhao, C. Deng, C. Ruan, D. Dai, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Xu, H. Ding, H. Gao, H. Qu, H. Li, J. Guo, J. Li, J. Chen, J. Yuan, J. Tu, J. Qiu, J. Li, J. L. Cai, J. Ni, J. Liang, J. Chen, K. Dong, K. Hu, K. You, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Zhao, L. Wang, L. Zhang, L. Xu, L. Xia, M. Zhang, M. Zhang, M. Tang, M. Zhou, M. Li, M. Wang, M. Li, N. Tian, P. Huang, P. Zhang, Q. Wang, Q. Chen, Q. Du, R. Ge, R. Zhang, R. Pan, R. Wang, R. J. Chen, R. L. Jin, R. Chen, S. Lu, S. Zhou, S. Chen, S. Ye, S. Wang, S. Yu, S. Zhou, S. Pan, S. S. Li, S. Zhou, S. Wu, T. Yun, T. Pei, T. Sun, T. Wang, W. Zeng, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, W. L. Xiao, W. An, X. Liu, X. Wang, X. Chen, X. Nie, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yang, X. Li, X. Su, X. Lin, X. Q. Li, X. Jin, X. Shen, X. Chen, X. Sun, X. Wang, X. Song, X. Zhou, X. Wang, X. Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. Zhang, Y. Xu, Y. Li, Y. Zhao, Y. Sun, Y. Wang, Y. Yu, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Ou, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Xiong, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. X. Zhu, Y. Huang, Y. Li, Y. Zheng, Y. Zhu, Y. Ma, Y. Tang, Y. Zha, Y. Yan, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Xie, Z. Zhang, Z. Hao, Z. Ma, Z. Yan, Z. Wu, Z. Gu, Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Pan, Z. Huang, Z. Xu, Z. Zhang, and Z. Zhang
(2025)
DeepSeek-r1 incentivizes reasoning in large language models through reinforcement learning
.
Nature
645
(
8081
),
pp. 633–638
.
Cited by:
§4.1
.
[12]
J. A. Hanley and B. J. McNeil
(1982)
The meaning and use of the area under a receiver operating characteristic (roc) curve
.
Radiology
143
(
1
),
pp. 29–36
.
Cited by:
§C.1
.
[13]
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song, and J. Steinhardt
(2021)
Measuring coding challenge competence with APPS
.
External Links:
2105.09938
,
Link
Cited by:
§1
.
[14]
Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma
(2025)
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
Document
Cited by:
§1
.
[15]
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
Table 12
,
§4.1
.
[16]
L. Kuhn, Y. Gal, and S. Farquhar
(2023)
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
The Eleventh International Conference on Learning Representations,
ICLR 2023, Kigali, Rwanda, May 1-5, 2023
,
External Links:
Link
Cited by:
Table 1
,
§1
.
[17]
J. Li, Y. Zhu, Y. Li, G. Li, and Z. Jin
(2024)
Showing llm-generated code selectively based on confidence of llms
.
Note:
arXiv preprint arXiv:2410.03234
External Links:
Link
Cited by:
§C.1
,
§1
,
§1
,
§1
,
§1
,
Table 1
,
§1
,
§4.1
,
§4.2
,
§4
.
[18]
Z. Lin, S. Trivedi, and J. Sun
(2023)
Generating with confidence: uncertainty quantification for black-box large language models
.
arXiv preprint arXiv:2305.19187
.
Cited by:
§1
,
§1
,
§1
,
Table 1
.
[19]
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
(2023)
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
External Links:
2305.01210
,
Link
Cited by:
§1
.
[20]
P. Manakul, A. Liusie, and M. J. F. Gales
(2023)
SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models
.
Note:
arXiv preprint arXiv:2303.08896
External Links:
Link
Cited by:
§1
,
§1
,
§1
,
§1
,
Table 1
.
[21]
N. Nguyen and S. Nadi
(2022)
An empirical evaluation of github copilot’s code suggestions
.
In
Proceedings of the 19th International Conference on Mining Software Repositories (MSR)
,
pp. 1–5
.
External Links:
Document
Cited by:
§1
.
[22]
R. P. Nogueira, M. Vieira, and J. R. Campos
(2025)
Beyond functional correctness: an empirical evaluation of large language models for text-to-code generation
.
In
Proceedings of the IEEE International Symposium on Software Reliability Engineering (ISSRE)
,
pp. 264–275
.
External Links:
Document
Cited by:
§1
.
[23]
A. Sharma and C. David
(2025)
Assessing correctness in LLM-based code generation via uncertainty estimation
.
External Links:
2502.11620
,
Link
Cited by:
§1
,
§1
,
§1
,
Table 1
,
§1
,
§4.1
.
[24]
T. Valentin, A. Madadi, G. Sapia, and M. Böhme
(2026)
Incoherence as oracle-less measure of error in LLM-based code generation
.
In
Proceedings of the 40th AAAI Conference on Artificial Intelligence (AAAI)
,
Note:
Accepted for publication
Cited by:
§C.1
,
§1
,
§1
,
§1
,
§1
,
Table 1
,
§1
,
§3
,
§4.2
,
§4
.
[25]
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
§1
,
§1
,
Table 1
.
[26]
C. Wissler
(1905)
The spearman correlation formula
.
Science
22
(
558
),
pp. 309–311
.
External Links:
Document
Cited by:
§4.1
.
[27]
S. Yeo, Y. Ma, S. C. Kim, H. Jun, and T. Kim
(2024)
Framework for evaluating code generation ability of large language models
.
ETRI Journal
46
(
1
),
pp. 106–117
.
External Links:
Document
Cited by:
§1
.
[28]
Q. Zheng, X. Xia, X. Zou, Y. Dong, S. Wang, Y. Xue, L. Shen, Z. Wang, A. Wang, Y. Li, T. Su, Z. Yang, and J. Tang
(2023)
CodeGeeX: A pre-trained model for code generation with multilingual benchmarking on humaneval-x
.
In
Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery
and Data Mining, KDD 2023, Long Beach, CA, USA, August 6-10, 2023
,
A. K. Singh, Y. Sun, L. Akoglu, D. Gunopulos, X. Yan, R. Kumar, F. Ozcan, and J. Ye (Eds.)
,
pp. 5673–5684
.
External Links:
Link
,
Document
Cited by:
Table 12
,
3rd item
,
§4.1
,
§4.3
.
[29]
T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf, H. Zhan, J. He, I. Paul, S. Brunner, C. Gong, J. Hoang, A. R. Zebaze, X. Hong, W. Li, J. Kaddour, M. Xu, Z. Zhang, P. Yadav, and et al.
(2025)
BigCodeBench: benchmarking code generation with diverse function calls and complex instructions
.
In
The Thirteenth International Conference on Learning Representations,
ICLR 2025, Singapore, April 24-28, 2025
,
External Links:
Link
Cited by:
Table 12
,
3rd item
,
§4.1
.
Appendix A
Detailed Input-Quality Diagnostics
The reliability of SDE and DSDE ultimately depends on whether
the generated test inputs
ℐ
\mathcal{I}
produce useful behavioural
signal on the sampled programs. This appendix reports four
diagnostics that characterise this signal, computed per task over
ℐ
=
{
x
1
,
…
,
x
10
}
\mathcal{I}=\{x_{1},\dots,x_{10}\}
and the candidate set
𝒞
\mathcal{C}
, and averaged across tasks. We organise the
diagnostics into two groups: (i) input-side validity metrics that
measure how well
ℐ
\mathcal{I}
is constructed; (ii) coverage
metrics that measure how thoroughly
ℐ
\mathcal{I}
exercises the
candidate code.
Input validity metrics
ValidExecRate
is the fraction of inputs on which at least
one candidate program returns a non-crash output. An input on
which every candidate crashes carries no behavioural signal and
cannot contribute to clustering:
ValidExecRate
=
|
{
x
j
∈
ℐ
:
∃
c
∈
𝒞
,
c
(
x
j
)
is non-crash
}
|
|
ℐ
|
.
\mathrm{ValidExecRate}\;=\;\frac{|\{\,x_{j}\in\mathcal{I}:\exists\,c\in\mathcal{C},\;c(x_{j})\text{ is non-crash}\,\}|}{|\mathcal{I}|}.
(5)
UniqueInputRate
is the fraction of inputs that remain
distinct after canonical normalisation. A value below one
indicates that the fuzzer has produced redundant or equivalent
inputs within the same task:
UniqueInputRate
=
|
unique
⁡
(
{
normalize
⁡
(
x
j
)
:
x
j
∈
ℐ
}
)
|
|
ℐ
|
.
\mathrm{UniqueInputRate}\;=\;\frac{\bigl|\,\mathrm{unique}\!\left(\{\mathrm{normalize}(x_{j}):x_{j}\in\mathcal{I}\}\right)\bigr|}{|\mathcal{I}|}.
(6)
CrashPollutionRate
is the fraction of all
candidate-by-input execution cells that crash. A high rate
indicates that many cells contribute no meaningful behavioural
signal and therefore add noise to clustering:
CrashPollutionRate
=
|
{
(
c
,
x
j
)
∈
𝒞
×
ℐ
:
c
⁡
(
x
j
)
​
crashes
}
|
|
𝒞
|
⋅
|
ℐ
|
.
\mathrm{CrashPollutionRate}\;=\;\frac{|\{\,(c,x_{j})\in\mathcal{C}\times\mathcal{I}:c(x_{j})\text{ crashes}\,\}|}{|\mathcal{C}|\cdot|\mathcal{I}|}.
(7)
Code-coverage metrics
LineCoverage
and
BranchCoverage
measure the
fraction of executable lines and branches in the candidate
programs that are exercised by
ℐ
\mathcal{I}
. For each candidate
c
∈
𝒞
c\in\mathcal{C}
, let
L
⁡
(
c
)
L(c)
and
L
cov
​
(
c
)
L_{\mathrm{cov}}(c)
denote
the total and covered executable lines when
c
c
is executed on
ℐ
\mathcal{I}
, and let
B
⁡
(
c
)
B(c)
and
B
cov
​
(
c
)
B_{\mathrm{cov}}(c)
denote the
analogous quantities for branches. The micro-averaged coverages
are
LineCoverage
=
∑
c
∈
𝒞
L
cov
​
(
c
)
∑
c
∈
𝒞
L
⁡
(
c
)
,
BranchCoverage
=
∑
c
∈
𝒞
B
cov
​
(
c
)
∑
c
∈
𝒞
B
⁡
(
c
)
.
\mathrm{LineCoverage}\;=\;\frac{\sum_{c\in\mathcal{C}}L_{\mathrm{cov}}(c)}{\sum_{c\in\mathcal{C}}L(c)},\qquad\mathrm{BranchCoverage}\;=\;\frac{\sum_{c\in\mathcal{C}}B_{\mathrm{cov}}(c)}{\sum_{c\in\mathcal{C}}B(c)}.
(8)
Together they bound how much of each candidate’s behaviour is
observable through the fuzz suite.
Table 8:
Input-quality diagnostics on
LiveCodeBench
at
T
=
0.6
T=0.6
.
Per task we use the first
N
=
10
N=10
available inputs; tasks with no
available inputs are excluded. Each metric is averaged over the
remaining tasks. LineCov and BranchCov are micro-averaged.
Model
ValidExec
Unique
Crash
LineCov
BranchCov
GPT-3.5-Turbo
0.901
0.948
0.209
0.937
0.888
GPT-4o-mini
0.898
0.948
0.213
0.937
0.889
Gemini-2.5-Flash-Lite
0.851
0.951
0.269
0.919
0.874
Claude-opus-4.5
0.863
0.950
0.201
0.917
0.879
Results.
Table
8
reports the diagnostics on
LiveCodeBench
at
T
=
0.6
T=0.6
. UniqueInputRate is approximately
0.95
0.95
across all four models, and ValidExecRate stays above
0.85
0.85
,
indicating that the fuzzer rarely produces redundant inputs and
that most inputs successfully exercise at least one candidate
program. LineCoverage exceeds
0.91
0.91
and BranchCoverage exceeds
0.87
0.87
on every model, indicating that the fuzz suite reaches
most code paths in each candidate. The input pool therefore
remains diverse, mostly executable, and largely covering across
all four models. CrashPollutionRate sits around
0.20
0.20
–
0.27
0.27
,
indicating that roughly one in five execution cells contributes
no behavioural signal; reducing this rate (e.g. via type-aware
input constraints or LLM-guided fuzzers) is a direct lever for
strengthening the upstream signal that SDE and DSDE consume.
Appendix B
End-to-End Evaluation Pipeline
Figure
3
summarises the end-to-end
evaluation pipeline used in this paper. Candidate programs are first sampled
from the code generation model; type-aware mutations then produce a shared
set of inputs; each candidate is executed on this input set to obtain
an execution signature; programs with identical signatures are clustered; and
finally the distance-aware uncertainty metrics SDE and DSDE are computed
from the resulting cluster distribution.
Figure 3
:
End-to-end evaluation pipeline for execution-based uncertainty
estimation in code generation.
Appendix C
Extended Experimental Results
This appendix presents additional experimental analyses that complement the
main evaluation in Section
4
. Unless stated otherwise,
all settings follow the protocol used in the main paper:
K
=
10
K=10
sampled
programs and
N
=
10
N=10
test inputs per task, with execution timeout
0.2
0.2
s
and sampling temperature
T
=
0.6
T=0.6
.
C.1
Extended Per-Difficulty Tables
Table
9
and Table
10
correspond directly
to the AUROC and correlation tables in the main paper, evaluated on four
closed-source code-generation models —
GPT-3.5-Turbo-0125
,
GPT-4o-mini
,
Gemini-2.5-Flash-Lite
, and
Claude-opus-4.5
— with results for an additional open-source model (
DeepSeek-Coder-V2
)
reported in Section
4.3
.
We compare our two distance-aware uncertainty metrics, SDE and DSDE,
against three sample-based uncertainty baselines:
DiffTrust
[
24
]
, an incoherence-based
behavioural-disagreement metric for code generation;
HonestCoder
[
17
]
, which combines semantic embeddings and
dataflow features with syntactic n-gram features over sampled programs; and
Semantic Entropy
[
7
]
, which clusters
programs based on binary semantic-equivalence judgments from an LLM judge
and computes Shannon entropy over the resulting clusters.
Table 9:
AUROC for pass@1 failure prediction across task difficulty levels and
models (
T
=
0.6
T=0.6
).
SDE
DSDE
DiffTrust
HonestCoder
Semantic Entropy
GPT-3.5-Turbo-0125
LiveCodeBench All
0.827
0.844
0.669
0.646
0.605
LiveCodeBench Easy
0.786
0.801
0.577
0.645
0.592
LiveCodeBench Medium
0.718
0.753
0.610
0.576
0.548
LiveCodeBench Hard
0.806
0.831
0.568
0.570
0.550
GPT-4o-mini
LiveCodeBench All
0.826
0.844
0.534
0.646
0.607
LiveCodeBench Easy
0.785
0.796
0.565
0.645
0.594
LiveCodeBench Medium
0.712
0.752
0.504
0.576
0.548
LiveCodeBench Hard
0.801
0.829
0.523
0.570
0.553
Gemini-2.5-Flash-Lite
LiveCodeBench All
0.794
0.808
0.688
0.668
0.639
LiveCodeBench Easy
0.735
0.730
0.671
0.566
0.470
LiveCodeBench Medium
0.742
0.762
0.686
0.635
0.597
LiveCodeBench Hard
0.705
0.737
0.523
0.590
0.645
Claude-opus-4.5
LiveCodeBench All
0.818
0.825
0.606
0.739
0.687
LiveCodeBench Easy
0.483
0.482
0.473
0.423
0.452
LiveCodeBench Medium
0.723
0.733
0.556
0.605
0.572
LiveCodeBench Hard
0.815
0.839
0.507
0.735
0.638
Table 10
:
Correlation with partial_pass@1 across task difficulty levels and models
(
T
=
0.6
T=0.6
). Left block: Pearson
r
r
. Right block: Spearman
ρ
\rho
.
Pearson
r
r
Spearman
ρ
\rho
SDE
DSDE
DiffTrust
HC
Semantic Entropy
SDE
DSDE
DiffTrust
HC
Semantic Entropy
GPT-3.5-Turbo-0125
LiveCodeBench All
-0.587
-0.622
-0.259
-0.344
-0.240
-0.581
-0.620
-0.267
-0.328
-0.237
LiveCodeBench Easy
-0.588
-0.645
-0.184
-0.259
-0.169
-0.549
-0.581
-0.145
-0.256
-0.176
LiveCodeBench Medium
-0.412
-0.467
-0.153
-0.185
-0.112
-0.426
-0.474
-0.144
-0.179
-0.105
LiveCodeBench Hard
-0.474
-0.516
-0.063
-0.205
-0.144
-0.429
-0.492
-0.044
-0.162
-0.121
GPT-4o-mini
LiveCodeBench All
-0.589
-0.624
-0.024
-0.344
-0.240
-0.584
-0.624
-0.064
-0.328
-0.238
LiveCodeBench Easy
-0.590
-0.644
-0.180
-0.259
-0.170
-0.547
-0.571
-0.143
-0.255
-0.176
LiveCodeBench Medium
-0.416
-0.474
0.013
-0.185
-0.110
-0.433
-0.488
-0.033
-0.179
-0.106
LiveCodeBench Hard
-0.470
-0.515
-0.018
-0.205
-0.142
-0.426
-0.485
-0.059
-0.162
-0.123
Gemini-2.5-Flash-Lite
LiveCodeBench All
-0.494
-0.532
-0.296
-0.301
-0.237
-0.491
-0.512
-0.298
-0.329
-0.242
LiveCodeBench Easy
-0.414
-0.449
-0.307
-0.106
-0.005
-0.314
-0.308
-0.215
-0.134
-0.033
LiveCodeBench Medium
-0.446
-0.499
-0.346
-0.249
-0.179
-0.414
-0.443
-0.309
-0.275
-0.178
LiveCodeBench Hard
-0.307
-0.370
0.025
-0.221
-0.237
-0.308
-0.365
0.031
-0.184
-0.235
Claude-opus-4.5
LiveCodeBench All
-0.552
-0.611
-0.139
-0.424
-0.275
-0.450
-0.461
-0.139
-0.350
-0.287
LiveCodeBench Easy
0.005
0.026
-0.056
0.071
0.057
0.024
0.025
0.024
0.052
0.048
LiveCodeBench Medium
-0.406
-0.492
-0.082
-0.177
-0.099
-0.253
-0.265
-0.059
-0.143
-0.107
LiveCodeBench Hard
-0.548
-0.635
0.008
-0.446
-0.252
-0.531
-0.580
-0.003
-0.414
-0.273
Discussion of the Claude–Easy outlier.
On the LCB Easy split for Claude-opus-4.5 the AUROC drops markedly relative
to the other splits. This appears to be driven by extreme class imbalance:
Claude achieves a pass@1 success rate of
95.34
%
95.34\%
on this subset, leaving
very few failure instances. AUROC is equivalent to the Wilcoxon rank-sum
statistic
[
12
]
, whose standard error grows rapidly as the
minority class shrinks, so small changes in the ranking of a handful of
failures produce disproportionate fluctuations in the reported value.
C.2
Sensitivity to Distance Weights
The crash-aware distance weights
(
a
,
b
,
c
)
(a,b,c)
are fixed to
(
1
,
0.8
,
0.6
)
(1,0.8,0.6)
throughout the main paper. To quantify the gap between this fixed scheme
and a per-setting tuned alternative, we additionally consider learning
(
a
,
b
,
c
)
(a,b,c)
via an 80:20 train–test split: the weights are fitted on the
training set and the resulting AUROC is measured on the held-out test set.
The default and learned schemes differ by less than
0.011
0.011
in AUROC across
all settings. On
LiveCodeBench
, only a small subset of inputs (consistently
below 3 out of 10) result in abnormal execution and therefore depend on
(
a
,
b
,
c
)
(a,b,c)
, which explains the small gap. In domains where abnormal
executions are more frequent, learning the weights is expected to become
more beneficial; for the regimes considered here, the fixed weighting
scheme is sufficient.
Table 11:
Fixed default weights
(
1.0
,
0.8
,
0.6
)
(1.0,0.8,0.6)
vs. per-setting learned weights.
Setting
(
a
,
b
,
c
)
(a,b,c)
Default
Learned
Δ
\Delta
Abnormal (/10)
Across models (fixed
T
=
0.6
T=0.6
)
Claude Opus 4.5
(
0.90
,
0.90
,
0.25
)
(0.90,0.90,0.25)
0.8248
0.8206
−
-
0.0042
2.01
Gemini-2.5-Flash-Lite
(
0.90
,
0.90
,
0.90
)
(0.90,0.90,0.90)
0.8075
0.7974
−
-
0.0101
2.69
GPT-3.5-Turbo
(
0.97
,
0.88
,
0.88
)
(0.97,0.88,0.88)
0.8442
0.8395
−
-
0.0047
2.09
GPT-4o-mini
(
1.00
,
0.80
,
0.80
)
(1.00,0.80,0.80)
0.8442
0.8524
+
+
0.0082
2.13
Across temperatures (fixed GPT-4o-mini)
GPT-4o-mini (
T
=
0.2
T=0.2
)
(
0.51
,
0.41
,
0.31
)
(0.51,0.41,0.31)
0.7789
0.7743
−
-
0.0045
2.69
GPT-4o-mini (
T
=
0.6
T=0.6
)
(
1.00
,
0.80
,
0.80
)
(1.00,0.80,0.80)
0.8442
0.8524
+
+
0.0082
2.13
GPT-4o-mini (
T
=
0.8
T=0.8
)
(
0.60
,
0.60
,
0.60
)
(0.60,0.60,0.60)
0.8530
0.8446
−
-
0.0084
1.82
C.3
Benchmark Details
LiveCodeBench
(LCB) is our primary benchmark, containing 1,055
programming tasks stratified into Easy, Medium, and Hard difficulty
levels with a relatively balanced distribution.
MBPP
contains 257 entry-level Python function-completion
problems.
HumanEval-X
comprises 164 hand-written problems
parallel-translated into Python, Java, and C++, and is used to test
cross-language transfer.
BigCodeBench
consists of 1,140 repository-scale tasks
featuring cross-file dependencies, multiple interacting components,
and complex control flow.
Together these benchmarks span a wide range of task difficulty (from
entry-level to repository-scale), programming languages (Python,
Java, C++), and problem styles (function completion, competitive
programming, and realistic library usage).
Table 12
:
Statistics of the four benchmarks used in this paper.
Benchmark
#Tasks
Languages
Task style
Difficulty
LiveCodeBench
[
15
]
1,055
Python
Competitive programming
Easy / Medium / Hard
MBPP
[
2
]
257
Python
Function completion
Entry-level
HumanEval-X
[
28
]
164
Python, Java, C++
Function completion
Mixed
BigCodeBench
[
29
]
1,140
Python
Repository-scale, library usage
Hard
C.4
Abstention Policy for Practical Deployment
To support practical use of uncertainty estimates, we introduce a
simple abstention policy that determines whether to accept or reject
the model’s top-ranked generated solution. The policy requires no
additional models or supervision; instead, it operationalises our
distance-aware uncertainty metrics as an actionable decision rule.
Formally, given a programming task
π
\pi
and its associated
uncertainty score
U
⁡
(
π
)
U(\pi)
, the abstention decision is defined as
δ
⁡
(
π
)
=
{
1
,
U
⁡
(
π
)
≤
τ
(accept)
0
,
U
⁡
(
π
)
>
τ
(abstain)
,
\delta(\pi)=\begin{cases}1,&U(\pi)\leq\tau\quad\text{(accept)}\\
0,&U(\pi)>\tau\quad\text{(abstain)},\end{cases}
where
τ
\tau
is a decision threshold selected via cross-validation on
training data and evaluated on held-out validation folds.
Table
13
reports abstention
performance for GPT-4o-mini under different operating constraints.
In
safety-oriented
settings, we impose an upper bound on the
false positive rate (FPR), defined as the fraction of incorrect
solutions that are accepted. For each constraint,
τ
\tau
is chosen
to maximise accuracy under strict correctness (Pass@1
=
1
=1
). Under
a highly conservative constraint (FPR
≤
5
%
\leq 5\%
), both SDE and
DSDE achieve strong and comparable performance. Under a more
balanced setting (FPR
≤
20
%
\leq 20\%
), DSDE yields a consistent
accuracy improvement over SDE.
Table 13:
Abstention policy performance under strict correctness
(Pass@1
=
1.0
=1.0
) on
LiveCodeBench
using GPT-4o-mini (
T
=
0.6
T=0.6
).
Results are shown under two representative operating points:
Strict Safety
and
Balanced
. Accuracy is maximised
subject to the corresponding FPR constraint. Values are reported as
mean
±
\pm
standard deviation over
5
5
-fold cross-validation.
Metric
Constraint
Accuracy
FPR
SDE
FPR
≤
\leq
5%
0.745
±
\pm
0.095
0.064
±
\pm
0.028
DSDE
FPR
≤
\leq
5%
0.745
±
\pm
0.095
0.064
±
\pm
0.028
SDE
FPR
≤
\leq
20%
0.734
±
\pm
0.088
0.069
±
\pm
0.028
DSDE
FPR
≤
\leq
20%
0.750
±
\pm
0.095
0.068
±
\pm
0.028
C.5
Execution Timeout
Performance is robust to the choice of per-input execution timeout
(Table
14
). Across all settings, the
proportion of
LiveCodeBench
problems that triggered at least one
timeout error is below
2
%
2\%
, indicating that the timeout has only a
minor effect on abnormal-termination rates.
Table 14:
Effect of the per-input execution timeout on SDE and
DSDE (
GPT-4o-mini
,
T
=
0.6
T=0.6
).
AUROC
Pearson
r
r
Spearman
ρ
\rho
Timeout (s)
SE
SDE
DSDE
SE
SDE
DSDE
SE
SDE
DSDE
0.1
0.802
0.804
0.819
−
-
0.505
−
-
0.540
−
-
0.575
−
-
0.493
−
-
0.534
−
-
0.573
0.2
0.824
0.826
0.844
−
-
0.543
−
-
0.589
−
-
0.624
−
-
0.524
−
-
0.584
−
-
0.624
0.3
0.798
0.808
0.821
−
-
0.499
−
-
0.550
−
-
0.583
−
-
0.486
−
-
0.545
−
-
0.580
Appendix D
Notation
Table
15
lists every symbol used in the paper.
Where the pipeline (§
3
) and metrics
(§
2
) sections use different surface forms for the same
object, both forms are shown joined by ‘
≡
\equiv
’.
Table 15:
Notation summary. Defaults from §
4.1
are in parentheses.
Symbol
Description
(i) Task and model
d
d
Natural-language task description
Coder
⁡
(
⋅
)
\mathrm{Coder}(\cdot)
Code-generation model
p
⁡
(
π
∣
d
)
p(\pi\!\mid\!d)
Conditional distribution over programs given
d
d
(ii) Candidate programs
K
K
Number of candidates per task (
K
=
10
K{=}10
)
π
\pi
,
π
k
\pi_{k}
,
π
1
\pi_{1}
Generic /
k
k
-th sampled / top-ranked candidate
𝝅
≡
Π
\boldsymbol{\pi}\equiv\Pi
Candidate set
{
π
1
,
…
,
π
K
}
\{\pi_{1},\dots,\pi_{K}\}
(iii) Test inputs and execution
N
N
Number of test inputs per task (
N
=
10
N{=}10
)
i
ℓ
≡
x
ℓ
i_{\ell}\equiv x_{\ell}
The
ℓ
\ell
-th test input,
ℓ
∈
{
1
,
…
,
N
}
\ell\in\{1,\dots,N\}
𝐢
≡
ℐ
\mathbf{i}\equiv\mathcal{I}
Input set
(
i
1
,
…
,
i
N
)
(i_{1},\dots,i_{N})
, shared across candidates
π
⁡
(
i
ℓ
)
≡
o
ℓ
​
(
π
)
\pi(i_{\ell})\equiv o_{\ell}(\pi)
Outcome of
π
\pi
on
i
ℓ
i_{\ell}
: a normal value or labelled error
𝐨
k
≡
σ
ℐ
​
(
π
k
)
\mathbf{o}_{k}\equiv\sigma_{\mathcal{I}}(\pi_{k})
Execution signature
(
o
1
​
(
π
k
)
,
…
,
o
N
​
(
π
k
)
)
\bigl(o_{1}(\pi_{k}),\dots,o_{N}(\pi_{k})\bigr)
(iv) Behaviour clusters
M
M
Number of clusters
C
i
C_{i}
,
|
C
i
|
|C_{i}|
The
i
i
-th cluster and its size
C
⁡
(
π
)
C(\pi)
Cluster containing program
π
\pi
p
i
p_{i}
Empirical cluster probability
|
C
i
|
/
K
|C_{i}|/K
,
∑
i
p
i
=
1
\sum_{i}p_{i}{=}1
c
∗
c^{*}
Index of cluster containing
π
1
\pi_{1}
, i.e.
C
c
∗
=
C
⁡
(
π
1
)
C_{c^{*}}=C(\pi_{1})
(v) Distances and weights
δ
⁡
(
⋅
,
⋅
)
\delta(\cdot,\cdot)
Per-input outcome dissimilarity (Eq. (
2
)),
δ
∈
[
0
,
1
]
\delta\in[0,1]
d
i
​
j
d_{ij}
Cluster-level distance (Eq. (
1
)); symmetric,
d
i
​
i
=
0
d_{ii}{=}0
a
a
Cost when exactly one outcome is abnormal (
a
=
1
a{=}1
)
b
b
Cost when both outcomes abnormal, different errors (
b
=
0.8
b{=}0.8
)
c
c
Cost when both outcomes abnormal, same error (
c
=
0.6
c{=}0.6
)
(vi) Uncertainty metrics
SDE
\mathrm{SDE}
Semantic Distance Entropy (Eq. (
3
))
DSDE
\mathrm{DSDE}
Dominant SDE, anchored at
C
c
∗
C_{c^{*}}
(Eq. (
4
))
U
⁡
(
π
)
U(\pi)
Generic uncertainty score (e.g., SDE or DSDE) used in abstention
(vii) Experimental settings and targets
T
T
Sampling temperature (
T
=
0.6
T{=}0.6
)
τ
\tau
Decision threshold of the abstention policy
FPR
\mathrm{FPR}
False positive rate (incorrect solutions accepted)
pass
​
@
​
1
\mathrm{pass@1}
Binary:
π
1
\pi_{1}
passes all reference tests
partial
​
_
​
pass
​
@
​
1
\mathrm{partial\_pass@1}
Fraction of reference tests passed by
π
1
\pi_{1}
, in
[
0
,
1
]
[0,1]
AUROC
\mathrm{AUROC}
Area under ROC for predicting
pass
​
@
​
1
\mathrm{pass@1}
failure
r
r
,
ρ
\rho
Pearson and Spearman correlations with
partial
​
_
​
pass
​
@
​
1
\mathrm{partial\_pass@1}
Appendix E
Concrete Case Study Examples
This appendix provides full task descriptions and representative cluster implementations for the two case studies. Each task is sampled
K
=
10
K=10
times; programs sharing identical execution outcomes on the shared test inputs are grouped into a single execution-behaviour cluster. The cluster membership for all four tasks is summarised in Table
16
. To complement the results in RQ1, we present two representative case studies that explicitly isolate the effect of semantic distance between execution clusters. The first case study focuses on
binary correctness
(pass@1), while the second examines
partial correctness
(partial_pass@1). In both cases, the tasks induce the same number of execution clusters (i.e., the same count of distinct behaviours); differences in correctness therefore arise solely from variation in the
semantic distance
between clusters rather than from the number of observed behaviours.
Table 16:
Execution-behaviour cluster membership and cluster probabilities for the
case-study tasks.
Task ID
Cluster
Cluster prob.
Member program indices
Case A: Binary correctness distinction
3367
C
0
C_{0}
0.800 (8/10)
[0, 1, 2, 3, 4, 5, 6, 7]
3367
C
1
C_{1}
0.200 (2/10)
[8, 9]
abc332_b
C
0
C_{0}
0.200 (2/10)
[0, 3]
abc332_b
C
1
C_{1}
0.800 (8/10)
[1, 2, 4, 5, 6, 7, 8, 9]
Case B: Partial correctness under identical pass@1
abc326_b
C
0
C_{0}
0.400 (4/10)
[0, 4, 5, 7]
abc326_b
C
1
C_{1}
0.600 (6/10)
[1, 2, 3, 6, 8, 9]
3163
C
0
C_{0}
0.400 (4/10)
[0, 1, 3, 8]
3163
C
1
C_{1}
0.600 (6/10)
[2, 4, 5, 6, 7, 9]
E.1
Case A: Binary Correctness Distinction
Case A contrasts two LiveCodeBench tasks whose execution-behaviour cluster
structures
are identical (in both tasks the 10 sampled programs split
into two clusters of size 8 and 2), yet whose binary correctness outcomes
differ. The contrast isolates the contribution of inter-cluster semantic
distance: dispersion-based statistics cannot distinguish the two cases, but
the distance-aware metrics can.
Figure 4
:
Case A: two LiveCodeBench tasks with identical execution-behaviour
cluster structures but different inter-cluster semantic distances and
binary correctness outcomes.
Case A: Semantic Distance Explains Binary Correctness (pass@1).
Table
17
compares two tasks with identical cluster
structure (
M
=
2
M=2
, one cluster contains 2 programs, and the other 8 programs)
but different binary outcomes. One task consistently produces
correct executions (pass@1 = 1), while the other fails (pass@1 = 0). Importantly,
both tasks exhibit the same dispersion over execution clusters, ruling out
dispersion-based explanations.
Table 17
:
Case A: Metric-level comparison illustrating the binary correctness
distinction. Task 1 (
3367
,
pass
​
@
​
1
=
1
\mathrm{pass@1}=1
) and Task 2
(
abc332_b
,
pass
​
@
​
1
=
0
\mathrm{pass@1}=0
) induce an identical
M
=
2
M=2
cluster structure with sizes 8 and 2, but exhibit very different
inter-cluster distances.
Metric
Task 1 (Low-Distance)
Task 2 (High-Distance)
Diff.
Pass@1
1
0
–
partial_pass@1
1.0000
0.0000
1.0000
Clusters
2 (8/2)
2 (8/2)
0
Distance
0.10
1.00
0.90
SDE
0.0160
0.1600
0.1440
DSDE
0.0200
0.8000
0.7800
Although the two tasks induce identical cluster structures, they differ
substantially in the semantic distance between clusters. For the correct task (task 1),
the distance between the two clusters is small (e.g.,
d
01
=
0.10
d_{01}=0.10
), indicating
highly similar execution outcomes. In contrast, the incorrect task (task 2) exhibits a
much larger inter-cluster distance (e.g.,
d
01
=
1.00
d_{01}=1.00
), reflecting severe
semantic divergence. This difference in cluster distance directly explains the
observed binary correctness gap and is captured by distance-aware uncertainty
metrics such as SDE and DSDE.
E.1.1
Problem 3367: Find the Sum of Encrypted Integers
Problem statement.
Given an integer array
nums
, define
encrypt(x)
as
replacing every digit in
x
with the largest digit in
x
.
Return the sum of encrypted elements. For example,
encrypt(523) = 555
and
encrypt(213) = 333
.
Cluster structure.
Two clusters with probabilities
p
0
=
0.80
p_{0}=0.80
(8 samples) and
p
1
=
0.20
p_{1}=0.20
(2 samples). Cluster
C
0
C_{0}
passes all test cases; cluster
C
1
C_{1}
fails on negative-number inputs with a
ValueError
.
Cluster
C
0
C_{0}
— Correct implementation (8 samples)
⬇
1
class
Solution
:
2
def
sumOfEncryptedInt
(
self
,
nums
:
List
[
int
])
->
int
:
3
total_sum
=
0
4
for
num
in
nums
:
5
max_digit
=
max
(
str
(
num
))
6
encrypted_num
=
int
(
max_digit
*
len
(
str
(
num
)))
7
total_sum
+=
encrypted_num
8
return
total_sum
Key characteristic
Uses
max(str(num))
, which returns the maximum character directly
and handles positive integers correctly.
Cluster
C
1
C_{1}
— Fails on negative numbers (2 samples)
⬇
1
class
Solution
:
2
def
sumOfEncryptedInt
(
self
,
nums
:
List
[
int
])
->
int
:
3
total_sum
=
0
4
for
num
in
nums
:
5
largest_digit
=
max
([
int
(
digit
)
for
digit
in
str
(
num
)])
6
encrypted_num
=
int
(
str
(
largest_digit
)
*
len
(
str
(
num
)))
7
total_sum
+=
encrypted_num
8
return
total_sum
Key characteristic
Attempts to convert each character to an integer, raising
ValueError: invalid literal for int() with base 10: ’-’
on
negative inputs.
E.1.2
Problem abc332_b: Glass and Mug
Problem statement.
Given a glass with capacity
G
G
ml and a mug with capacity
M
M
ml, both
initially empty, repeat
K
K
operations:
(1) if the glass is empty, fill the mug completely;
(2) else if the mug is empty, discard all water from the glass;
(3) otherwise, transfer water from the mug to the glass (the glass fills
completely if possible, with any remainder staying in the mug).
Output the final water amounts in the glass and the mug.
Cluster structure.
Two clusters with probabilities
p
0
=
0.20
p_{0}=0.20
(2 samples) and
p
1
=
0.80
p_{1}=0.80
(8 samples). Both clusters produce incorrect solutions, but
with different error patterns.
Cluster
C
0
C_{0}
— Wrong condition check (2 samples)
⬇
1
K
,
G
,
M
=
map
(
int
,
input
().
split
())
2
glass
,
mug
=
0,
0
3
for
_
in
range
(
K
):
4
if
glass
<
G
:
#
Wrong:
should
check
glass
==
0
5
glass
=
G
6
elif
mug
==
0:
7
mug
=
M
8
else
:
9
transfer
=
min
(
mug
,
G
-
glass
)
10
glass
+=
transfer
11
mug
-=
transfer
12
print
(
glass
,
mug
)
Key characteristic
Uses
glass < G
instead of
glass == 0
, misinterpreting
the problem requirements.
Cluster
C
1
C_{1}
— Incorrect operation order (8 samples)
⬇
1
K
,
G
,
M
=
map
(
int
,
input
().
split
())
2
glass
,
mug
=
0,
0
3
for
_
in
range
(
K
):
4
if
glass
==
0:
5
mug
=
M
6
elif
mug
==
0:
7
glass
=
0
#
Wrong:
should
fill
glass,
not
empty
it
8
else
:
9
transferred
=
min
(
M
-
mug
,
glass
)
10
mug
+=
transferred
11
glass
-=
transferred
12
print
(
glass
,
mug
)
Key characteristic
The glass is emptied when the mug is empty (line 6), so the glass always
ends at
0
0
.
E.2
Case B: Partial Correctness Distinction
Case B isolates the contribution of inter-cluster distance under
identical
pass@1 outcomes: both tasks have
pass
​
@
​
1
=
0
\mathrm{pass@1}=0
and
admit the same 6/4 cluster split, yet differ substantially in
partial_pass@1. Distance-aware metrics recover this distinction; dispersion-only
metrics cannot.
Case B: Semantic Distance Explains Partial Correctness.
Table
18
presents a complementary scenario,
where both tasks have pass@1 = 0 and induce
identical execution cluster structure (
M
=
2
M=2
, one cluster contains 6 programs, and the other 4 programs), yet differ substantially in
partial_pass@1.
Table 18
:
Case B: Metric-level comparison illustrating partial correctness under
identical binary outcomes. Task 1 (
abc326_b
) and Task 2
(
3163
) both have
pass
​
@
​
1
=
0
\mathrm{pass@1}=0
and induce an identical
M
=
2
M=2
cluster structure with sizes 6 and 4, but differ in their
inter-cluster distance and therefore in partial_pass@1.
Metric
Task 1 (Low-Distance)
Task 2 (High-Distance)
Diff.
pass@1
0
0
–
partial_pass@1
0.6667
0.0000
0.6667
Clusters
2 (6/4)
2 (6/4)
0
Distance
0.30
1.00
0.70
SDE
0.0720
0.2400
0.1680
DSDE
0.1800
0.6000
0.4200
In this case, dispersion-based signals provide no discrimination, as the two
tasks share identical cluster structures and probabilities. However, the
semantic distance between clusters differs markedly. The task with higher
partial correctness exhibits smaller inter-cluster distances (e.g.,
d
01
=
0.30
d_{01}=0.30
), whereas the task with lower partial correctness shows much larger
distances (e.g.,
d
01
=
1.00
d_{01}=1.00
). These differences align closely with the partial
correctness outcomes and are faithfully reflected by distance-aware metrics.
E.2.1
Problem abc326_b: 326-like Numbers
Problem statement.
A positive integer is a
326-like number
if it is a three-digit
number satisfying (hundreds digit)
×
\times
(tens digit)
=
=
(ones digit).
For example,
326
326
,
400
400
, and
144
144
are 326-like. Given a positive
integer
N
N
, return the smallest integer
≥
N
\geq N
that is a 326-like
number.
Cluster structure.
Two clusters with probabilities
p
0
=
0.60
p_{0}=0.60
(6 samples,
partial
​
_
​
pass
​
@
​
1
=
1.0
\mathrm{partial\_pass@1}=1.0
) and
p
1
=
0.40
p_{1}=0.40
(4 samples,
partial
​
_
​
pass
​
@
​
1
=
0.0
\mathrm{partial\_pass@1}=0.0
). The two clusters differ by
an off-by-one ordering of the increment and the predicate check.
Cluster
C
0
C_{0}
— Correct: check before increment (6 samples)
⬇
1
N
=
int
(
input
())
2
while
True
:
3
hundreds
=
N
//
100
4
tens
=
(
N
%
100)
//
10
5
ones
=
N
%
10
6
if
hundreds
*
tens
==
ones
:
#
Check
condition
first
7
print
(
N
)
8
break
9
N
+=
1
#
Then
increment
Key characteristic
The predicate is checked before incrementing
N
N
, so the case in which
N
N
itself is already a 326-like number is handled correctly.
Cluster
C
1
C_{1}
— Off-by-one error (4 samples)
⬇
1
N
=
int
(
input
())
2
while
True
:
3
N
+=
1
#
Wrong:
increment
before
checking
4
hundreds
=
N
//
100
5
tens
=
(
N
%
100)
//
10
6
ones
=
N
%
10
7
if
hundreds
*
tens
==
ones
:
#
Then
check
condition
8
print
(
N
)
9
break
Key characteristic
N
N
is incremented before the predicate is checked, producing an
off-by-one error whenever
N
N
itself is already a 326-like number.
E.2.2
Problem 3163: Subarrays Distinct Element Sum of Squares II
Problem statement.
Given a
0
0
-indexed integer array
nums
, the distinct count of a
subarray is the number of distinct elements it contains. Return the sum
of the squares of the distinct counts of all subarrays. For example,
with
nums = [1,2,1]
, the answer is
1
2
+
1
2
+
1
2
+
2
2
+
2
2
+
2
2
=
15
1^{2}+1^{2}+1^{2}+2^{2}+2^{2}+2^{2}=15
.
Cluster structure.
Two clusters with probabilities
p
0
=
0.40
p_{0}=0.40
(4 samples,
partial
​
_
​
pass
​
@
​
1
=
0.0
\mathrm{partial\_pass@1}=0.0
) and
p
1
=
0.60
p_{1}=0.60
(6 samples,
partial
​
_
​
pass
​
@
​
1
=
1.0
\mathrm{partial\_pass@1}=1.0
). The two clusters differ in
what
is being squared.
Cluster
C
0
C_{0}
— Wrong: sums squared frequencies (4 samples)
⬇
1
from
collections
import
Counter
2
class
Solution
:
3
def
sumCounts
(
self
,
nums
:
List
[
int
])
->
int
:
4
total
=
0
5
n
=
len
(
nums
)
6
for
i
in
range
(
n
):
7
count
=
Counter
()
8
for
j
in
range
(
i
,
n
):
9
count
[
nums
[
j
]]
+=
1
10
#
Wrong:
sums
(frequency^2),
not
(distinct
count)^2
11
total
+=
sum
(
val
**
2
for
val
in
count
.
values
())
12
return
total
Key characteristic
Computes
∑
k
f
k
2
\sum_{k}f_{k}^{2}
, where
f
k
f_{k}
is the frequency of element
k
k
,
instead of (number of distinct elements)
2
—a fundamental
misinterpretation of the specification.
Cluster
C
1
C_{1}
— Correct: squares the distinct count (6 samples)
⬇
1
class
Solution
:
2
def
sumCounts
(
self
,
nums
:
List
[
int
])
->
int
:
3
ans
=
0
4
n
=
len
(
nums
)
5
for
i
in
range
(
n
):
6
freq
=
{}
7
distinct_count
=
0
8
for
j
in
range
(
i
,
n
):
9
if
nums
[
j
]
not
in
freq
:
10
distinct_count
+=
1
11
freq
[
nums
[
j
]]
=
1
12
else
:
13
freq
[
nums
[
j
]]
+=
1
14
ans
+=
distinct_count
**
2
#
Correct:
(distinct
count)^2
15
return
ans
Key characteristic
Tracks the number of distinct elements and squares this count, matching
the specification.
Across both cases, correctness differences cannot be explained by cluster counts
or dispersion alone. Instead, they are driven by the magnitude of semantic
distance between execution clusters. These examples provide concrete, intuitive
evidence that the effectiveness observed in Section
4.2
arises from incorporating
semantic distance, supporting the use of distance-aware uncertainty estimation
for LLM-generated code.