---
title: 1Introduction
id: 1introduction-2
tags:
- code-llm-confidence-positioning-d82d00
- test-time-compute
- budget-allocation
- self-consistency
- l3-related
created: '2026-11-09T23:09:05.091749Z'
updated: '2026-11-09T23:27:44.605178Z'
source: https://arxiv.org/html/2605.26849
source_domain: arxiv.org
fetched_at: '2026-11-09T23:09:05.090630Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv HTML v2, Oct 2026; Deakin). Note title mis-extracted as
  ''1Introduction-2''; paper is ''Uncertainty-Aware Budget Allocation for Adaptive
  Test-Time Reasoning'' (Nguyen, Gupta, Le). Two-phase concave integer allocation:
  Phase-1 gives each question K samples whose vote entropy is the difficulty signal;
  Phase-2 marginal-greedy allocation of the rest. Five open models (1.5B-27B) on MATH500,
  Formal Logic, DeepScaler, GSM8K, Graded Arithmetic; +2.3% average over uniform (up
  to +5.5%); Table 5 compares allocation to Oracle(q) (under-allocated 10.5% vs Uniform
  13.3%). Logit baselines (NLL, ANLL) trail vote entropy (Table 4). No code benchmarks,
  no verbalized or probe confidence, no calibration metrics. RELATED to L3 (uncertainty-routed
  budgets vs uniform/random/oracle) only for math/logic via sampled disagreement.'
---

1Introduction
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2605.26849v2 [cs.CL] 08 Oct 2026
Uncertainty-Aware Budget Allocation for
Adaptive Test-Time Reasoning
Manh Nguyen
Sunil Gupta
Hung Le
Applied Artificial Intelligence Initiative, Deakin University, Australia
manh.nguyen@deakin.edu.au
Abstract
Sampling multiple responses improves language model reasoning, but uniform compute allocation is inefficient because easy questions are over-sampled while hard questions remain under-explored.
We propose
Uncertainty-Aware Budget Allocation (UAB)
, a concave integer optimization framework that reallocates a fixed sampling budget using uncertainty estimated from the initial samples themselves.
In Phase-1, every question receives a small fixed number of generations. Their answer disagreement, measured by vote entropy, provides a difficulty signal while these generations contribute to the final vote.
In Phase-2, the remaining budget is allocated by a marginal-greedy algorithm that optimally solves a concave coverage-maximization surrogate, concentrating samples on questions whose initial answers disagree.
Across five open-weight models (1.5B–27B parameters) and five reasoning benchmarks of varying difficulty, UAB improves average accuracy by
+
2.3
%
+2.3\%
over uniform allocation, and achieves gains of up to
+
5.5
%
+5.5\%
on individual benchmarks, with the largest gains in low-resource settings. Moreover, UAB meets the target budget exactly and requires no auxiliary model or additional LLM calls.
Code is publicly available at
https://github.com/manhitv/UAB
.
1
Introduction
Large language models (LLMs) are increasingly deployed for reasoning-intensive tasks where inference cost is a primary deployment concern.
Test-time compute scaling, which generates multiple outputs and aggregates them via self-consistency
(
Wang et al., 2023
)
or best-of-
N
N
selection
(
Lightman et al., 2024
;
Nguyen et al., 2026a
)
, is an effective way to improve accuracy
(
Snell et al., 2025
;
Wu et al., 2025
)
.
However, its benefit exhibits diminishing returns: each additional sample yields a smaller accuracy gain than the previous one, and this marginal value varies sharply across questions
(
Brown et al., 2024
)
.
We therefore ask:
given a fixed total generation budget
B
B
for
M
M
questions, how should samples be distributed to maximize accuracy?
Self-consistency (SC) answers with uniform allocation: every question receives exactly
N
N
samples regardless of difficulty.
This is wasteful, because easy questions saturate after one correct generation while genuinely hard ones remain under-sampled, and the inefficiency is sharpest at small
N
N
, which is also where inference cost matters most.
A growing line of work confirms that uncertainty signals can redirect compute toward harder questions, but each existing approach makes a structural compromise unsuited to fixed-budget cross-question reasoning.
Sequential early-stopping methods such as Adaptive-Consistency
(
Aggarwal et al., 2023
)
, ESC
(
Li et al., 2024
)
, and ReASC
(
Kim et al., 2026
)
optimize a per-question stopping rule under an unbounded cap: their realized cost depends on how many questions trigger early termination, so they do not explicitly support a fixed total budget
B
B
a priori, nor reallocate samples saved on easy questions toward harder ones.
Auxiliary-component methods rely on a separate LLM or trained estimator to predict difficulty
(
Ji et al., 2026
;
Wang et al., 2025
;
Li et al., 2026a
;
Yoon et al., 2026
)
, adding setup or per-question overhead that dominates at small
N
N
.
Intra-trace budgeting methods target a different decision variable. MUR
(
Yan et al., 2026
)
allocates thinking tokens across reasoning steps, while SelfBudgeter
(
Li et al., 2026b
)
RL-trains the model to predict a per-query token cap. Both allocate tokens within a response instead of deciding
how many samples
to draw under a shared budget.
Closest to our setting, prior methods also allocate a shared budget across questions, but rely on learned difficulty predictors
(
Damani et al., 2025
)
or alternative inference configurations
(
Zhang et al., 2025
)
.
We instead show that answer agreement among the first few samples is a sufficient allocation signal when paired with an exact solution to a concave coverage surrogate.
We propose
Uncertainty-Aware Budget Allocation (UAB)
, a two-phase inference framework for
M
M
questions under total budget
B
=
N
×
M
B{=}N{\times}M
.
In
Phase-1
, every question receives the same
K
K
generations, whose vote entropy provides a difficulty signal without additional inference, while all
K
K
generations contribute to the final answer aggregation.
In
Phase-2
, the remaining budget is allocated by a marginal-greedy algorithm that optimally solves a concave coverage-maximization surrogate, prioritizing questions whose next sample yields the largest marginal coverage gain.
Across five open-weight models ranging from 1.5B to 27B and five reasoning tasks spanning a diverse range of difficulty levels, UAB outperforms uniform allocation with the same budgets on average across models, with improvements concentrated at low budgets (
N
≈
4
−
8
N\approx 4{-}8
).
Average accuracy gains reach
+
2.3
%
+2.3\%
over uniform allocation, with up to
+
3.1
%
+3.1\%
per model and
+
5.5
%
+5.5\%
on individual benchmarks.
The two-phase pipeline adds minor wall-clock overhead; ablations validate its allocation behavior, oracle efficiency, and robustness to key design choices.
Figure
1
provides an overview of UAB.
Our contributions are as follows.
•
We formulate LLM budget allocation as a concave integer program driven by vote entropy, solved exactly by marginal-greedy allocation.
•
We propose UAB, a two-phase uncertainty-aware allocation method built on this formulation that requires no auxiliary model and adds only minor wall-clock overhead.
•
Experiments show that UAB achieves the highest average accuracy at low budgets, with ablations validating its key design choices.
Figure 1:
Uniform vs. Uncertainty-Aware Budget allocation (UAB)
under a total budget of
B
=
16
B{=}16
samples across
M
=
4
M{=}4
questions.
➊
Uniform allocates
N
=
4
N{=}4
samples per question and fails on Q3 and Q4, where four samples are not enough to identify the correct answer.
➋
UAB draws
K
=
2
K{=}2
samples per question and computes their vote entropy
H
H
. Q1 and Q2 agree (
H
=
0
H{=}0
) and stop; the remaining
B
−
K
​
M
=
8
B-KM{=}8
samples are split evenly between the disagreeing Q3 and Q4 (
H
=
1
H{=}1
), giving each six samples in total. UAB answers all four questions correctly at the same total budget.
2
Related Work
Adaptive self-consistency.
Self-consistency
(
Wang et al., 2023
)
spends the same number of samples on every input. Adaptive variants differ along three axes.
Budget guarantee:
sequential early-stopping methods such as Adaptive-Consistency
(
Aggarwal et al., 2023
)
, ESC
(
Li et al., 2024
)
, and ReASC
(
Kim et al., 2026
)
decide per question when to stop, so their total cost depends on how many questions stop early and cannot be fixed in advance.
Signal source:
Several methods estimate difficulty with a separate LLM call or a trained predictor
(
Ji et al., 2026
;
Wang et al., 2025
;
Yoon et al., 2026
;
Li et al., 2026a
)
, an overhead that becomes significant at small
N
N
. UAB instead reads difficulty from the agreement among its voting samples, at no additional inference cost.
Decision unit:
batch-level methods distribute a shared budget across questions. Among these,
Damani et al. (2025)
learn a difficulty predictor, and PETS
(
Liu et al., 2026
)
optimizes agreement with the infinite-budget majority vote through a crowdsourcing model re-simulated by Monte Carlo before each sampling decision, whereas UAB allocates the entire remaining budget in a single greedy pass based on early-sample agreement.
Budget Allocation and Compute Scaling.
Test-time compute scaling
(
Snell et al., 2025
;
Wu et al., 2025
)
establishes that sample-level reallocation improves accuracy at fixed cost, extended by best-of-
N
N
and process-reward policies
(
Lightman et al., 2024
;
Cobbe et al., 2021
)
.
Recent work generalizes beyond fixed-batch SC: AVA
(
Anonymous, 2026
)
jointly schedules search, sampling, and verification under a user budget, and SelfBudgeter
(
Li et al., 2026b
)
RL-trains the model to predict a per-query token budget. Beyond LLMs, budget-constrained inference in active learning
(
Settles, 2009
)
motivates greedy allocation under concave utility.
UAB is unique in combining a query-free voting signal with an provably optimal greedy solution to a concave coverage objective, requiring no extra model, training stage, or LLM call.
Confidence Signals in LLMs.
Orthogonal to
how many
samples to draw, prior work examines
what
confidence to use: self-calibration
(
Huang et al., 2026
)
, intra-trace filtering
(
Fu et al., 2025
)
, confidence-weighted voting
(
Taubenfeld et al., 2025
)
, semantic entropy
(
Kuhn et al., 2023
)
, vote entropy
(
Argamon-Engelson and Dagan, 1999
)
, and probability-only
(
Nguyen et al., 2026b
)
estimators. UAB is estimator-agnostic and uses vote entropy (
K
=
2
K{=}2
) as its default signal.
3
Budget-Aware Sample Allocation
We formalize the problem of distributing a finite inference budget
B
=
N
×
M
B{=}N{\times}M
across
M
M
questions, where
N
N
is the average per-question budget and each question
x
i
x_{i}
receives
N
i
≥
1
N_{i}\geq 1
samples with
∑
i
=
1
M
N
i
=
B
\sum_{i=1}^{M}N_{i}=B
.
3.1
Optimization Problem
Let
p
i
∈
[
0
,
1
]
p_{i}\in[0,1]
denote the per-sample success probability for question
x
i
x_{i}
, i.e., the probability that a single generation from the model is correct. Given per-sample success probabilities
{
p
i
}
i
=
1
M
\{p_{i}\}_{i=1}^{M}
, we seek the integer allocation
𝑵
=
(
N
1
,
…
,
N
M
)
\bm{N}=(N_{1},\ldots,N_{M})
that maximizes the expected number of questions solved by at least one of the sampled solutions (expected coverage) under budget
B
B
:
max
𝑵
\displaystyle\max_{\bm{N}}
∑
i
=
1
M
[
1
−
(
1
−
p
i
)
N
i
]
\displaystyle\sum_{i=1}^{M}\bigl[1-(1-p_{i})^{N_{i}}\bigr]
(1)
s.t.
\displaystyle\text{s.t.}
∑
i
=
1
M
N
i
=
B
,
N
i
∈
ℤ
+
.
\displaystyle\sum_{i=1}^{M}N_{i}=B,N_{i}\in\mathbb{Z}_{+}.
The objective
1
−
(
1
−
p
i
)
N
i
1-(1-p_{i})^{N_{i}}
is the probability that
at least one
of
N
i
N_{i}
i.i.d. samples is correct, a coverage surrogate for majority-vote accuracy.
We discuss the gap between coverage, majority vote, and the i.i.d. approximation in Appendix
C
.
We first draw
K
K
samples for every question (
1
≤
K
≤
N
1\leq K\leq N
) to estimate
p
i
p_{i}
. These
K
K
samples are already spent when the allocation decision is made and remain part of the final vote. We therefore write the total allocation as
N
i
=
K
+
n
i
N_{i}=K+n_{i}
, where
n
i
≥
0
n_{i}\geq 0
is the number of additional samples allocated to question
x
i
x_{i}
. The remaining budget is
B
eff
=
B
−
K
​
M
=
(
N
−
K
)
​
M
B_{\mathrm{eff}}=B-KM=(N-K)M
.
This reparameterization turns the remaining allocation into a zero-based problem, allowing some questions to receive no additional samples.
Substituting
N
i
=
K
+
n
i
N_{i}=K+n_{i}
into Eq.
1
, we obtain
∑
i
[
1
−
(
1
−
p
i
)
N
i
]
=
M
−
∑
i
(
1
−
p
i
)
K
+
n
i
\sum_{i}\bigl[1-(1-p_{i})^{N_{i}}\bigr]=M-\sum_{i}(1-p_{i})^{K+n_{i}}
.
Since
∑
i
(
1
−
p
i
)
K
\sum_{i}(1-p_{i})^{K}
is constant with respect to
𝒏
\bm{n}
, maximizing over
𝒏
\bm{n}
is equivalent to maximizing the weighted coverage objective
∑
i
(
1
−
p
i
)
K
​
[
1
−
(
1
−
p
i
)
n
i
]
\sum_{i}(1-p_{i})^{K}\bigl[1-(1-p_{i})^{n_{i}}\bigr]
, giving
max
𝒏
\displaystyle\max_{\bm{n}}
∑
i
(
1
−
p
i
)
K
​
[
1
−
(
1
−
p
i
)
n
i
]
\displaystyle\sum_{i}(1-p_{i})^{K}\bigl[1-(1-p_{i})^{n_{i}}\bigr]
(2)
s.t.
\displaystyle\text{s.t.}
∑
i
n
i
=
B
eff
,
n
i
∈
ℤ
≥
0
.
\displaystyle\sum_{i}n_{i}=B_{\mathrm{eff}},\quad n_{i}\in\mathbb{Z}_{\geq 0}.
Eq.
2
is a separable concave knapsack with nonnegative integer allocations and diminishing marginal gains, so marginal-greedy allocation is exact
(
Fox, 1966
;
Federgruen and Groenevelt, 1986
)
.
Section
3.2
specifies how
p
i
p_{i}
is obtained from the
K
K
samples.
3.2
Estimating Success Probabilities
From a
K
K
-sample signal to a success probability.
For each question
x
i
x_{i}
, we first draw a fixed round of
K
≥
1
K\geq 1
samples
y
i
1
,
…
,
y
i
K
{y_{i}^{1},\ldots,y_{i}^{K}}
, with all
K
K
samples contributing to the final vote. We refer to this fixed round as
Phase-1
throughout, while the subsequent adaptive round,
Phase-2
, is described in Section
3.3
.
From these
K
K
samples, a scalar uncertainty score is computed and mapped to a success probability,
s
i
=
Signal
⁡
(
y
i
1
,
…
,
y
i
K
)
,
p
i
=
g
⁡
(
s
i
)
∈
[
0
,
1
]
,
s_{i}=\mathrm{Signal}(y_{i}^{1},\ldots,y_{i}^{K}),\qquad p_{i}=g(s_{i})\in[0,1],
(3)
where
g
g
maps higher uncertainty to lower
p
i
p_{i}
.
Vote-entropy signal (our default).
Following prior work that uses answer-agreement entropy for difficulty-adaptive self-consistency
(
Wang et al., 2025
;
Ji et al., 2026
)
, we extract the final answer from each Phase-1 sample
y
i
k
y_{i}^{k}
and compute the empirical vote distribution over the extracted answers. Specifically,
q
^
i
(
a
)
=
1
K
∑
k
=
1
K
𝟏
[
answer
(
y
i
k
)
=
a
]
,
\hat{q}_{i}(a)=\frac{1}{K}\sum_{k=1}^{K}\mathbf{1}\bigl[\text{answer}(y_{i}^{k})=a\bigr],
(4)
where
q
^
i
​
(
a
)
\hat{q}_{i}(a)
is the fraction of the
K
K
samples (Phase-1) whose extracted answer is
a
a
, so
∑
a
q
^
i
​
(
a
)
=
1
\sum_{a}\hat{q}_{i}(a)=1
. For
K
≥
2
K\geq 2
, we then define the normalized Shannon entropy of this vote distribution
(
Argamon-Engelson and Dagan, 1999
)
as
H
i
=
−
1
log
⁡
K
∑
a
q
^
i
(
a
)
log
q
^
i
(
a
)
,
H
i
∈
[
0
,
1
]
,
H_{i}=-\frac{1}{\log K}\sum_{a}\hat{q}_{i}(a)\log\hat{q}_{i}(a),\qquad H_{i}\in[0,1],
(5)
where
H
i
=
0
H_{i}=0
when all
K
K
samples yield the same answer and
H
i
=
1
H_{i}=1
when all
K
K
extracted answers are distinct. Finally, we convert the entropy into a difficulty-dependent success probability:
p
i
=
e
−
H
i
/
τ
.
p_{i}=e^{-H_{i}/\tau}.
(6)
where
τ
>
0
\tau>0
is a hyperparameter (default
OPEN
τ
=
1
)
\tau{=}1)
that controls how sharply the
p
i
p_{i}
for uncertain answers are positioned relative to the marginal-gain peak
p
⋆
p^{\star}
, thereby shaping how the Phase-2 budget is allocated among them (Section
3.3
).
Here,
s
i
=
H
i
s_{i}=H_{i}
and
g
(
s
)
=
e
−
s
/
τ
g(s)=e^{-s/\tau}
in Eq.
3
; the log-probability variant in Appendix
F
instantiates the same two maps differently.
Trade-off in
K
K
and
K
=
2
K{=}2
degeneracy.
Larger
K
K
consumes more samples for uncertainty estimation, leaving less budget for adaptive allocation, but provides a richer vote-entropy signal. Although
K
=
1
K{=}1
permits log-probability-based uncertainty metrics, we defer these to Appendix
F
and Table
4
. At
K
=
2
K{=}2
(our default),
H
i
H_{i}
has only two values:
0
0
for agreement and
1
1
for disagreement, giving
p
i
∈
{
1
,
e
−
1
/
τ
}
p_{i}\in\{1,e^{-1/\tau}\}
. Thus, all disagreeing questions have identical
p
i
p_{i}
, and
τ
\tau
only rescales their tied marginal gains without affecting the allocation. UAB therefore keeps agreeing questions at
K
K
samples and distributes the remaining budget evenly across the
D
D
disagreeing questions. Because the marginal gain strictly decreases after each assignment, greedy gives each disagreeing question either
⌊
B
eff
/
D
⌋
\lfloor B_{\mathrm{eff}}/D\rfloor
or
⌈
B
eff
/
D
⌉
\lceil B_{\mathrm{eff}}/D\rceil
extra samples, with tie-breaking determining only the remainder. Hence,
K
=
2
K{=}2
reduces to agree/disagree rule with an even split, while the optimization formulation extends naturally to
K
≥
3
K\geq 3
, where finer ranking becomes possible.
Figure
1
shows a concrete example of this even split.
Algorithm 1
Uncertainty-Aware Budget Allocation
1:
Questions
{
x
i
}
i
=
1
M
\{x_{i}\}_{i=1}^{M}
, per-question budget
N
N
, signal reveal count
K
K
2:
Final answer
a
^
i
\hat{a}_{i}
for each question
3:
// Phase-1: Fixed round (
K
K
generations per question)
4:
for
each question
x
i
x_{i}
in parallel
do
5:
{
y
i
1
,
…
,
y
i
K
}
←
Generate
​
(
x
i
,
count
=
K
)
\{y_{i}^{1},\ldots,y_{i}^{K}\}\leftarrow\text{Generate}(x_{i},\text{count}=K)
6:
s
i
←
Signal
​
(
y
i
1
,
…
,
y
i
K
)
s_{i}\leftarrow\text{Signal}(y_{i}^{1},\ldots,y_{i}^{K})
⊳
\triangleright
no extra LLM call
7:
p
i
←
g
⁡
(
s
i
)
p_{i}\leftarrow g(s_{i})
8:
end
for
9:
// Marginal-greedy budget allocation
10:
n
i
←
0
n_{i}\leftarrow 0
for all
i
i
;
B
eff
←
(
N
−
K
)
​
M
B_{\mathrm{eff}}\leftarrow(N{-}K)M
11:
for
t
=
1
,
2
,
…
,
B
eff
t=1,2,\ldots,B_{\mathrm{eff}}
do
12:
i
∗
←
arg
⁡
max
i
​
p
i
​
(
1
−
p
i
)
K
+
n
i
i^{*}\leftarrow\arg\max_{i}p_{i}(1-p_{i})^{K+n_{i}}
⊳
\triangleright
ties broken by lowest index
13:
n
i
∗
←
n
i
∗
+
1
n_{i^{*}}\leftarrow n_{i^{*}}+1
14:
end
for
15:
// Phase-2: Adaptive round
16:
for
each question
x
i
x_{i}
with
n
i
>
0
n_{i}>0
in parallel
do
17:
{
y
i
K
+
1
,
…
,
y
i
K
+
n
i
}
←
Generate
​
(
x
i
,
count
=
n
i
)
\{y_{i}^{K+1},\ldots,y_{i}^{K+n_{i}}\}\leftarrow\text{Generate}(x_{i},\text{count}=n_{i})
18:
end
for
19:
// Aggregation
20:
for
each question
x
i
x_{i}
do
21:
a
^
i
←
MajorityVote
​
(
y
i
1
,
…
,
y
i
K
+
n
i
)
\hat{a}_{i}\leftarrow\text{MajorityVote}(y_{i}^{1},\ldots,y_{i}^{K+n_{i}})
22:
end
for
23:
return
{
a
^
i
}
\{\hat{a}_{i}\}
3.3
Uncertainty-Aware Budget Allocation
Two-Phase Inference Pipeline.
UAB collects the difficulty signal and allocates the remaining budget in two phases.
Phase-1 is fixed and uniform
: every question receives
K
K
generations, and the difficulty signal requires no additional generations, since these
K
K
samples also enter the final vote, with
N
i
=
n
i
+
K
N_{i}{=}n_{i}{+}K
(
n
i
≥
0
n_{i}\geq 0
the Phase-2 count). The remaining
B
eff
=
(
N
−
K
)
​
M
B_{\mathrm{eff}}=(N{-}K)M
budget is distributed greedily by repeatedly assigning each unit to the question with the largest marginal gain
Δ
i
​
(
N
i
)
=
p
i
​
(
1
−
p
i
)
N
i
\Delta_{i}(N_{i})=p_{i}(1-p_{i})^{N_{i}}
.
The full procedure is Algorithm
1
. Since the difficulty signal is computed from answer-level agreement (vote-entropy), the pipeline can also be applied to black-box, API-only models.
Table 1:
Accuracy (%) at
N
=
4
N{=}4
across five benchmarks.
N
=
1
N{=}1
is the single-call reference.
Bold
= best,
underline
= second-best.
Model
Method
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
Avg
Qwen2.5-1.5B
N=1
40.3
±
\pm
0.7
43.4
±
\pm
2.6
17.4
±
\pm
1.0
53.8
±
\pm
1.1
47.0
±
\pm
1.6
40.4
Random
45.3
±
\pm
1.1
42.9
±
\pm
2.8
18.3
±
\pm
0.7
57.7
±
\pm
1.4
51.3
±
\pm
1.2
43.1
Length
46.6
±
\pm
1.4
42.9
±
\pm
1.3
18.0
±
\pm
0.7
59.6
±
\pm
1.7
56.3
±
\pm
2.1
44.7
Uniform
47.1
±
\pm
0.1
43.1
±
\pm
1.3
18.2
±
\pm
1.0
59.8
±
\pm
1.1
57.0
±
\pm
1.6
45.0
LLM-Judge
46.7
±
\pm
1.0
44.4
±
\pm
1.1
17.8
±
\pm
0.2
60.4
±
\pm
1.8
49.3
±
\pm
2.1
43.7
ASC
45.3
±
\pm
1.2
43.9
±
\pm
1.6
16.3
±
\pm
0.5
68.7
±
\pm
2.2
51.7
±
\pm
1.2
45.2
PETS
42.6
±
\pm
1.0
43.9
±
\pm
1.6
16.3
±
\pm
1.2
47.9
±
\pm
1.5
49.3
±
\pm
2.5
40.0
UAB
†
48.9
±
\pm
0.8
42.3
±
\pm
0.4
19.4
±
\pm
0.4
65.3
±
\pm
2.8
59.0
±
\pm
2.2
47.0
Llama3.2-3B
N=1
27.5
±
\pm
1.2
37.8
±
\pm
2.7
15.2
±
\pm
1.7
68.6
±
\pm
1.8
59.7
±
\pm
1.9
41.8
Random
32.4
±
\pm
2.1
37.8
±
\pm
3.1
15.1
±
\pm
2.0
73.2
±
\pm
0.6
61.0
±
\pm
0.8
43.9
Length
32.3
±
\pm
1.5
40.2
±
\pm
2.0
16.1
±
\pm
0.6
75.2
±
\pm
1.3
61.3
±
\pm
2.6
45.0
Uniform
33.7
±
\pm
1.3
41.5
±
\pm
0.7
16.9
±
\pm
0.9
74.6
±
\pm
2.3
61.0
±
\pm
2.2
45.5
LLM-Judge
30.3
±
\pm
0.7
36.8
±
\pm
2.1
15.9
±
\pm
0.8
67.9
±
\pm
0.3
59.3
±
\pm
1.7
42.0
ASC
29.0
±
\pm
1.6
47.1
±
\pm
0.4
16.3
±
\pm
0.5
80.7
±
\pm
1.4
62.0
±
\pm
1.4
47.0
PETS
30.5
±
\pm
1.8
36.8
±
\pm
2.0
15.3
±
\pm
1.0
67.7
±
\pm
0.5
61.0
±
\pm
0.8
42.3
UAB
†
34.9
±
\pm
0.8
44.2
±
\pm
1.3
17.6
±
\pm
1.0
80.1
±
\pm
0.4
62.7
±
\pm
1.2
47.9
Qwen2.5-7B
N=1
62.7
±
\pm
0.9
57.9
±
\pm
3.0
28.3
±
\pm
2.6
83.4
±
\pm
0.3
57.7
±
\pm
5.7
58.0
Random
65.1
±
\pm
0.8
61.4
±
\pm
3.6
28.7
±
\pm
2.1
87.3
±
\pm
0.3
58.7
±
\pm
1.2
60.2
Length
65.6
±
\pm
0.5
61.1
±
\pm
1.9
26.7
±
\pm
1.7
89.1
±
\pm
0.2
58.0
±
\pm
1.6
60.1
Uniform
65.6
±
\pm
0.6
60.6
±
\pm
2.7
26.1
±
\pm
1.8
88.4
±
\pm
0.6
58.3
±
\pm
1.7
59.8
LLM-Judge
65.2
±
\pm
0.3
59.5
±
\pm
3.9
26.8
±
\pm
0.8
87.4
±
\pm
1.8
62.7
±
\pm
2.1
60.3
ASC
67.0
±
\pm
1.3
61.1
±
\pm
2.2
26.7
±
\pm
1.0
92.7
±
\pm
0.5
61.3
±
\pm
1.2
61.8
PETS
62.3
±
\pm
0.5
59.0
±
\pm
2.7
23.6
±
\pm
1.1
83.0
±
\pm
0.3
55.7
±
\pm
1.7
56.7
UAB
†
66.8
±
\pm
0.6
62.7
±
\pm
0.6
30.7
±
\pm
1.4
92.4
±
\pm
1.5
61.7
±
\pm
1.7
62.9
Table 2:
Accuracy (%) at
N
=
4
N{=}4
on two large open-weight models.
N
=
1
N{=}1
is the single-call reference.
Bold
= best,
underline
= second-best.
Model
Method
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
Avg
GPT-OSS-20B
N=1
57.3
±
\pm
0.8
78.3
±
\pm
2.6
24.1
±
\pm
1.9
87.6
±
\pm
0.6
66.0
±
\pm
0.8
62.7
Random
58.6
±
\pm
0.4
79.9
±
\pm
1.6
24.2
±
\pm
1.6
89.4
±
\pm
0.6
64.7
±
\pm
1.2
63.4
Length
59.1
±
\pm
0.8
81.7
±
\pm
1.7
24.1
±
\pm
1.9
91.4
±
\pm
0.6
64.3
±
\pm
1.7
64.1
Uniform
59.1
±
\pm
0.8
81.2
±
\pm
3.3
23.4
±
\pm
1.0
90.2
±
\pm
0.8
63.7
±
\pm
1.9
63.5
LLM-Judge
58.8
±
\pm
0.5
76.7
±
\pm
2.3
23.9
±
\pm
1.2
90.0
±
\pm
1.0
64.3
±
\pm
0.9
62.7
ASC
60.7
±
\pm
0.5
83.9
±
\pm
1.0
28.3
±
\pm
0.9
93.0
±
\pm
0.0
66.0
±
\pm
1.4
66.4
PETS
56.7
±
\pm
0.4
78.3
±
\pm
2.5
21.6
±
\pm
1.0
85.3
±
\pm
0.5
63.3
±
\pm
0.5
61.1
UAB
†
60.5
±
\pm
0.1
83.6
±
\pm
1.0
27.8
±
\pm
0.6
93.0
±
\pm
0.0
66.0
±
\pm
1.4
66.2
Gemma3-27B
N=1
68.4
±
\pm
0.8
79.1
±
\pm
2.0
32.8
±
\pm
0.6
92.3
±
\pm
0.3
79.7
±
\pm
0.9
70.5
Random
69.7
±
\pm
0.6
77.0
±
\pm
2.8
32.3
±
\pm
1.0
92.7
±
\pm
0.5
80.3
±
\pm
0.9
70.4
Length
70.5
±
\pm
0.5
79.4
±
\pm
2.2
34.1
±
\pm
1.4
93.8
±
\pm
0.4
81.7
±
\pm
1.2
71.9
Uniform
70.5
±
\pm
0.4
79.9
±
\pm
0.4
33.1
±
\pm
1.0
93.1
±
\pm
1.0
81.3
±
\pm
1.2
71.6
LLM-Judge
70.3
±
\pm
0.2
78.6
±
\pm
1.1
34.0
±
\pm
1.0
94.1
±
\pm
0.7
81.7
±
\pm
0.5
71.7
ASC
71.1
±
\pm
0.7
83.6
±
\pm
2.5
35.4
±
\pm
0.7
94.3
±
\pm
0.3
83.0
±
\pm
0.0
73.5
PETS
69.3
±
\pm
0.9
74.3
±
\pm
2.0
31.7
±
\pm
0.7
90.4
±
\pm
0.3
81.0
±
\pm
0.8
69.3
UAB
†
71.3
±
\pm
0.5
83.3
±
\pm
2.3
33.7
±
\pm
0.3
94.3
±
\pm
0.3
83.0
±
\pm
0.0
73.1
Figure 2:
Average accuracy (%, over the five benchmarks) vs. per-question sampling budget
N
∈
{
4
,
8
,
12
,
16
}
N\in\{4,8,12,16\}
.
Optimality condition.
After
m
m
total samples, the marginal gain from one more sample for question
i
i
is
Δ
i
​
(
m
)
=
p
i
​
(
1
−
p
i
)
m
,
\displaystyle\Delta_{i}(m)=p_{i}(1-p_{i})^{m},
(7)
which is non-increasing in
m
m
. Eq.
2
is separable and concave, and the marginal value of the next extra sample for question
i
i
is
Δ
i
​
(
K
+
n
i
)
=
p
i
​
(
1
−
p
i
)
K
+
n
i
\Delta_{i}(K+n_{i})=p_{i}(1-p_{i})^{K+n_{i}}
. An allocation
𝒏
∗
\bm{n}^{*}
is optimal iff there exists a price
λ
∗
≥
0
\lambda^{*}\geq 0
such that
p
i
​
(
1
−
p
i
)
K
+
n
i
∗
−
1
≥
λ
∗
≥
p
i
​
(
1
−
p
i
)
K
+
n
i
∗
,
p_{i}(1-p_{i})^{K+n_{i}^{*}-1}\geq\lambda^{*}\geq p_{i}(1-p_{i})^{K+n_{i}^{*}},
(8)
for every
i
i
with
n
i
∗
>
0
n_{i}^{*}>0
, while only the right inequality is required when
n
i
∗
=
0
n_{i}^{*}=0
. We restate the proof for completeness in Appendix Proposition
1
.
Thus, every extra sample has marginal gain at least
λ
∗
\lambda^{*}
when allocated, while the next sample is worth at most
λ
∗
\lambda^{*}
.
Because
Δ
i
​
(
m
)
\Delta_{i}(m)
decays geometrically from
p
i
p_{i}
, high-
p
i
p_{i}
questions saturate quickly, very low-
p
i
p_{i}
questions may never reach
λ
∗
\lambda^{*}
.
Algorithm
1
implements this condition by assigning each of the
B
eff
B_{\mathrm{eff}}
units to
arg
⁡
max
i
​
Δ
i
​
(
K
+
n
i
)
\arg\max_{i}\Delta_{i}(K+n_{i})
, returning the exact optimum of Eq.
2
(Appendix Proposition
2
).
When Does Reallocation Help?
For fixed
m
m
,
Δ
i
​
(
m
)
\Delta_{i}(m)
is unimodal in
p
i
p_{i}
with peak
p
⋆
=
1
/
(
m
+
1
)
p^{\star}{=}1/(m{+}1)
, so the allocator favors intermediate-difficulty questions rather than the hardest ones. As
m
m
grows, the peak shifts toward smaller
p
i
p_{i}
, where the marginal coverage gain from additional samples is smaller and increasingly misaligned with majority-vote accuracy (Appendix
C
).
For
K
≥
3
K\geq 3
, where
H
i
H_{i}
can take more than two values,
τ
\tau
shapes the allocation as follows.
Agreeing questions (
H
i
=
0
H_{i}=0
) always have
p
i
=
1
p_{i}=1
and
Δ
i
=
0
\Delta_{i}=0
for all
m
≥
1
m\geq 1
, so they receive no Phase-2 samples for any
τ
\tau
. For disagreeing questions, the two limiting regimes behave differently. As
τ
→
0
\tau\to 0
, all
p
i
→
0
p_{i}\to 0
and
Δ
i
(
m
)
≈
e
−
H
i
/
τ
\Delta_{i}(m)\approx e^{-H_{i}/\tau}
becomes nearly independent of
m
m
, causing the allocator to concentrate the budget on the disagreeing questions with the
smallest
H
i
H_{i}
. In contrast, as
τ
→
∞
\tau\to\infty
,
1
−
p
i
≈
H
i
/
τ
1-p_{i}\approx H_{i}/\tau
and
Δ
i
​
(
m
)
≈
(
H
i
/
τ
)
m
\Delta_{i}(m)\approx(H_{i}/\tau)^{m}
, so questions with fewer samples have larger marginal gains. The allocation therefore approaches an even split across disagreeing questions, with
H
i
H_{i}
serving only to break ties among questions with the same number of samples. Intermediate values of
τ
\tau
smoothly interpolate between these two regimes.
4
Experiments
4.1
Experimental Setup
Models.
We evaluate five open-weight LLMs from 1.5B to 27B parameters:
Qwen2.5-1.5B, 7B
(
Yang et al., 2024
)
,
Llama3.2-3B
(
Grattafiori et al., 2024
)
,
GPT-OSS-20B
(
OpenAI, 2025
)
, and
Gemma3-27B
(
Gemma Team et al., 2025
)
.
Datasets.
We evaluate on five benchmarks covering diverse reasoning types and difficulty regimes,
using 100–500 questions per benchmark:
(1) MATH500
(
Hendrycks et al., 2021b
;
Lightman et al., 2024
)
: competition mathematics;
(2) MMLU Formal Logic
(
Hendrycks et al., 2021a
)
: deductive reasoning;
(3) DeepScaler
(
Agentica Research, 2025
)
: challenging math competition problems;
(4) GSM8K
(
Cobbe et al., 2021
)
: grade-school math word problems;
and
(5) Graded Arithmetic
: procedurally generated arithmetic expressions with an interpretable ten-level difficulty ladder, enabling controlled evaluation across progressively harder reasoning instances.
Dataset details are in Appendix
E
.
Baselines.
Under the same total budget
B
=
N
×
M
B{=}N{\times}M
, we compare six baselines:
(1) Random
, which allocates samples uniformly at random across questions;
(2) Length
, which uses input question length as a difficulty proxy;
(3) Uniform
, the self-consistency baseline
(
Wang et al., 2023
)
where every question receives exactly
N
N
samples;
(4) LLM-Judge
, which prompts the LLM to classify each question as easy or hard, giving easy questions
1
1
sample and distributing the remaining
N
−
1
N{-}1
budget units per question across hard ones, motivated by
Wang et al. (2025)
;
(5) Adaptive-Consistency (ASC)
(
Aggarwal et al., 2023
)
, which stops sampling once a confidence threshold
θ
\theta
is
met; and
(6) PETS
(
Liu et al., 2026
)
, a batch-level allocator that selects each next sample by the expected knowledge gradient of a Dirichlet model over answer options (Appendix
D.2
).
UAB (Ours)
uses vote-entropy with
τ
=
1
\tau{=}1
and
K
=
2
K{=}2
samples per question in Phase-1 (which contribute to the final vote) and reallocates the remaining
(
N
−
K
)
​
M
(N{-}K)M
budget adaptively.
At
K
=
2
K{=}2
,
τ
\tau
does not change the allocation (Section
4.3
) and only affects the reported
p
^
\hat{p}
in Table
3
.
Since ASC has no budget parameter, we tune
θ
\theta
separately for each model, dataset and
N
N
so that its realized average budget matches
N
N
on that dataset; DSC
(
Wang et al., 2025
)
is excluded because its stopping rule cannot reach our low-sampling budget (Appendix
D.1
).
We use
N
=
4
N{=}4
samples per question as the default budget, and additionally explore up to
N
=
16
N{=}16
.
All results are averaged across three seeds and reported as accuracy percentages (mean
±
\pm
std).
Implementation details are in Appendix
D
.
Figure 3:
UAB’s gains over Uniform on Qwen2.5-1.5B, averaged over five datasets.
Left:
gain vs. sharpness
τ
\tau
at
N
=
4
N{=}4
;
Right:
gain vs. Phase-1 sample count
K
∈
{
2
,
…
,
8
}
K\in\{2,\dots,8\}
, at each budget
N
∈
{
4
,
8
,
12
,
16
}
N\in\{4,8,12,16\}
(only
K
≤
N
K{\leq}N
is feasible).
Per-dataset breakdown in Appendix Figure
5
.
Table 3:
MATH500 by difficulty level (vote-entropy
K
=
2
K{=}2
,
τ
=
1
\tau{=}1
,
N
=
4
N{=}4
).
N
¯
\bar{N}
= mean allocated samples (UAB);
p
^
\hat{p}
= mean
p
i
p_{i}
(Eq.
6
), so
p
^
∈
[
e
−
1
,
1
]
\hat{p}\in[e^{-1},1]
.
Bold
= higher of Uniform/UAB.
Model
Level
n
n
N
¯
\bar{N}
p
^
\hat{p}
Uniform
UAB
†
Qwen2.5-1.5B
L1
43
2.95
0.819
72.9
75.2
L2
90
3.30
0.749
65.9
69.3
L3
105
3.78
0.655
58.1
59.7
L4
128
4.24
0.572
44.0
45.1
L5
134
4.76
0.469
20.6
22.1
Llama3.2-3B
L1
43
3.26
0.696
72.1
74.4
L2
90
3.53
0.632
50.4
53.0
L3
105
3.94
0.532
39.7
40.3
L4
128
4.16
0.491
28.1
28.9
L5
134
4.45
0.428
10.9
11.7
Qwen2.5-7B
L1
43
2.53
0.946
82.2
81.4
L2
90
2.83
0.920
76.3
77.0
L3
105
3.36
0.866
74.3
75.2
L4
128
4.18
0.789
64.3
66.7
L5
134
5.59
0.652
47.5
48.8
4.2
Main Results
UAB Outperforms Baselines.
Table
1
reports accuracy across all model–benchmark pairs. UAB achieves the highest average accuracy for all three models, outperforming Uniform in 14 of 15 settings, with an average gain of
+
2.5
%
+2.5\%
, up to
+
3.1
%
+3.1\%
per models,
+
5.5
%
+5.5\%
on GSM8K (Qwen2.5-1.5B and Llama3.2-3B). A paired bootstrap test on per-question correctness finds 9 of these 15 improvements significant at
p
<
0.05
p<0.05
(Appendix Table
8
). Among the baselines, ASC is the strongest, slightly outperforming Uniform for every model, yet UAB still wins in 9 of 15 settings and maintains the higher average accuracy.
PETS trails the other methods at this budget because its warm-up sample consumes a quarter of the budget before any adaptive allocation.
LLM-Judge concentrates its surplus budget on a small set of questions classified as hard and underperforms Uniform in several settings, suggesting that binary easy/hard classification is too coarse for fine-grained budget allocation.
Table
2
extends evaluation to two large open-weight models. UAB again beats Uniform across all settings, with average gains of
+
2.7
%
+2.7\%
(GPT-OSS-20B) and
+
1.5
%
+1.5\%
(Gemma3-27B), and improves over the single-call
N
=
1
N{=}1
baseline by up to
+
5.4
%
+5.4\%
(GPT-OSS-20B, GSM8K). However, UAB no longer leads ASC, which attains a slightly higher average on both models, likely because stronger models agree more often in Phase-1, which leaves fewer disagreeing questions to reallocate.
Scaling With Budget.
Figure
2
shows accuracy across
N
∈
{
4
,
8
,
12
,
16
}
N\in\{4,8,12,16\}
.
UAB’s gains over Uniform are concentrated at low budgets (
N
≈
4
−
8
N\approx 4{-}8
), where adaptive allocation matters most. As the budget grows, the average gain diminishes, and at
N
=
16
N{=}16
no setting significantly favors UAB (Appendix Table
8
). PETS improves as its fixed warm-up cost is amortized, catching up with UAB by
N
=
16
N{=}16
. At larger budgets (
N
≥
12
N\geq 12
), UAB and ASC also become nearly indistinguishable on average, as reallocating additional samples is less effective when most questions already have enough samples.
Per-dataset breakdowns for these budgets are in Appendix Tables
14
–
16
.
4.3
Ablation Studies
Budget Allocation Analysis.
Table
3
gives the per-level breakdown for the default vote-entropy signal at
N
=
4
N{=}4
: estimated success probability (
p
^
\hat{p}
) decreases and allocated budget (
N
¯
\bar{N}
) increases monotonically with difficulty for all three main models. The accuracy gain over Uniform is not largest at the hardest level, peaking at L2 for Qwen2.5-1.5B and Llama3.2-3B and at L4 for Qwen2.5-7B. At the easiest levels, most questions already agree after Phase-1, leaving little budget to reallocate, while at the hardest levels, additional samples often fail to improve majority-vote accuracy because the correct answer is absent from the sampled responses (Section
3.3
). The peak shifts to harder levels for the stronger model, which has higher per-level success rates.
Table 4:
Full per-dataset breakdown of the difficulty-signal ablation (
N
=
4
N{=}4
,
τ
=
1
\tau{=}1
, Qwen2.5-1.5B).
Bold
= best value over five ranking signals and
underline
= second-best. AUROC ranks each signal’s raw score against Phase-1 correctness, computed per dataset and then averaged over the 5 datasets. Results for Llama3.2-3B and Qwen2.5-7B are in Appendix Table
11
.
Ranking Signal
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
Avg
AUROC
UAB w/o Uncertainty
47.1
±0.1
43.1
±1.3
18.2
±1.0
59.8
±1.1
57.0
±1.6
45.0
–
UAB w/o probe reuse
47.7
±0.6
43.4
±0.7
18.1
±0.6
64.2
±2.5
56.7
±1.9
46.0
–
NLL
46.4
±0.7
43.4
±1.9
17.2
±0.6
60.8
±0.4
54.0
±1.4
44.4
0.742
Token Var
46.7
±0.7
43.7
±3.0
17.9
±0.3
60.2
±1.4
55.7
±1.9
44.8
0.672
Max Token NLL
46.8
±0.3
43.4
±1.5
18.0
±1.0
60.6
±1.9
56.3
±2.1
45.0
0.688
ANLL
46.9
±0.5
41.8
±1.3
18.6
±0.6
60.4
±2.3
56.7
±1.2
44.9
0.662
UAB (Vote Entropy)
48.9
±0.8
42.3
±0.4
19.4
±0.4
65.3
±2.8
59.0
±2.2
47.0
0.780
Table 5:
Allocation quality relative to Oracle(
q
q
), the smallest number of samples whose majority vote is correct, at
N
=
4
N{=}4
(Qwen2.5-1.5B, mean over five datasets, excluding questions unsolved within 16 samples). %Under is the share of questions given fewer samples than Oracle(
q
q
), which are always wrong, while %Over-C and %Over-W are the shares given more samples whose vote is correct or wrong, so Oracle scores 0 on all three.
‡
\ddagger
marks MATH500 and Graded Arithmetic only, where Oracle (Difficulty) assigns budgets by annotated level (Appendix Table
10
), and
bold
/
underline
is best/second-best in the top block. Per-dataset results and all baselines in Appendix Table
9
.
Allocation Signal
%Under
↓
\downarrow
%Over-C
↑
\uparrow
%Over-W
↓
\downarrow
Uniform
13.3
70.5
11.8
UAB (ANLL,
K
=
1
K{=}1
)
13.0
68.9
12.4
UAB (NLL,
K
=
1
K{=}1
)
14.0
66.0
12.6
UAB (Vote Entropy,
K
=
2
K{=}2
)
10.5
75.4
11.7
Oracle (Difficulty)
‡
14.1
59.8
8.9
UAB (Vote Entropy,
K
=
2
K{=}2
)
‡
10.0
82.5
6.0
Oracle
(true minimum)
0.0
0.0
0.0
Allocation vs. Oracle.
Table
5
indicates UAB leaves the fewest questions under-allocated (
10.5
%
10.5\%
) and the largest share of over-sampled questions correct (
75.4
%
75.4\%
). On the two datasets with annotated difficulty, it also outperforms allocation based on true difficulty across all three measures, showing that its two-sample signal is competitive with ground-truth difficulty. The remaining errors arise from both insufficient sampling and extra samples that shift the vote to an incorrect answer, suggesting that
allocation, rather than signal quality alone, remains a key bottleneck
.
Sharpness
τ
\tau
and
K
K
.
For
K
≥
3
K\geq 3
,
τ
\tau
determines which disagreeing questions receive extra samples: small
τ
\tau
favors the least uncertain of them, while large
τ
\tau
approaches an even split (Section
3.2
). Figure
3
(left) shows that Vote-Entropy (
K
=
3
K{=}3
) benefits from larger
τ
\tau
, whereas Vote-Entropy (
K
=
2
K{=}2
) is flat by construction, since
τ
\tau
does not affect its allocation, and achieves the best average gain.
For
N
≤
12
N\leq 12
,
K
=
2
K{=}2
yields the largest gain (Figure
3
, right), as its agree/disagree split captures most of the reallocation benefit while preserving more budget for Phase-2.
Uncertainty Metric.
In Table
4
, we first isolate UAB’s two components:
w/o Uncertainty
reduces to Uniform by construction, while
w/o probe reuse
excludes the
K
K
probe samples from the final vote when Phase-2 samples are allocated. This variant underperforms the full method because discarding the probes shrinks the effective vote despite preserving their allocation guidance. Allocation alone accounts for at least half of UAB’s gain over Uniform, even with the smaller vote.
We then compare four
K
=
1
K{=}1
logprob-based signals (Appendix
F
) with our default
K
=
2
K{=}2
vote entropy. Vote entropy achieves the highest AUROC and realized accuracy on all three models despite using one additional Phase-1 sample, as its uncertainty measure is directly aligned with the allocation objective and the final Phase-1 vote.
Wall-Clock and Token Efficiency.
Appendix Table
12
reports wall-clock time at
N
=
4
N{=}4
. Batch processing and parallelism keep live-measured methods within 2.5 minutes, with UAB adding minor overhead over Uniform. The overhead is more visible on shorter generations, where the two-phase dependency has less computation to spread it over. PETS is substantially more expensive because its Monte-Carlo knowledge-gradient decision is made per sample.
Appendix Table
13
shows that the differences in wall-clock time are not due to higher per-sample cost. All fixed-budget methods use the same model and decoding settings, so their average per-sample token costs are similar. UAB only changes how samples are allocated across questions.
5
Conclusion
We show that, under a fixed inference budget, redistributing samples according to answer disagreement among initial generations improves self-consistency accuracy. Using vote entropy from these generations, UAB improves average accuracy over Uniform for all five models at low budgets, with gains diminishing as the budget grows. UAB’s two-phase pipeline adds minor overhead, requires no auxiliary model, and meets the target budget exactly, making it practical for adaptive sampling under tight budgets.
Limitations are discussed in Appendix
G
.
AI use statement
In this work, we used generative AI tools solely to support writing, including proofing, language polishing, and
improving readability. We did not use them to develop research ideas, conduct experiments, or generate the substantive content of the work. All AI-assisted text was reviewed and verified by the authors, who take full responsibility for the final content.
References
Agentica Research (2025)
Agentica Research
DeepScaleR: surpassing O1-Preview with a 1.5B model by scaling RL
.
Cited by:
§4.1
.
Aggarwal
et al.
(2023)
P. Aggarwal, A. Madaan, Y. Yang, and Mausam
Let’s sample step by step: adaptive-consistency for efficient reasoning and coding with LLMs
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
pp. 12375–12396
.
Cited by:
§D.1
,
§1
,
§2
,
§4.1
.
Anonymous (2026)
Anonymous
Anytime verified agents: adaptive compute allocation for reliable LLM reasoning under budget constraints
.
Submitted to Transactions on Machine Learning Research
.
External Links:
Link
Cited by:
§2
.
Argamon-Engelson and Dagan (1999)
S. Argamon-Engelson and I. Dagan
Committee-based sample selection for probabilistic classifiers
.
Journal of Artificial Intelligence Research
11
,
pp. 335–360
.
Cited by:
§2
,
§3.2
.
Brown
et al.
(2024)
B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, and A. Mirhoseini
Large language monkeys: scaling inference compute with repeated sampling
.
arXiv preprint arXiv:2407.21787
.
Cited by:
§1
.
Choi
et al.
(2025)
H. K. Choi, X. Zhu, and S. Li
Debate or vote: which yields better decisions in multi-agent large language models?
.
In
Advances in Neural Information Processing Systems
,
Vol.
38
,
pp. 112802–112834
.
Cited by:
Appendix D
.
Cobbe
et al.
(2021)
K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano,
et al.
Training verifiers to solve math word problems
.
arXiv preprint arXiv:2110.14168
.
Cited by:
§2
,
§4.1
.
Damani
et al.
(2025)
M. Damani, I. Shenfeld, A. Peng, A. Bobu, and J. Andreas
Learning how hard to think: input-adaptive allocation of LM computation
.
In
International Conference on Learning Representations
,
Cited by:
§1
,
§2
.
Federgruen and Groenevelt (1986)
A. Federgruen and H. Groenevelt
The greedy procedure for resource allocation problems: necessary and sufficient conditions for optimality
.
Operations Research
34
(
6
),
pp. 909–918
.
Cited by:
Appendix A
,
§3.1
.
Fox (1966)
B. Fox
Discrete optimization via marginal analysis
.
Management Science
13
(
3
),
pp. 210–216
.
Cited by:
Appendix A
,
§3.1
.
Fu
et al.
(2025)
Y. Fu, X. Wang, Y. Tian, and J. Zhao
Deep think with confidence
.
arXiv preprint arXiv:2508.15260
.
Cited by:
§2
.
Gemma Team
et al.
(2025)
Gemma Team, A. Kamath, J. Ferret, S. Pathak, N. Vieillard, R. Merhej, S. Perrin, T. Matejovicova, A. Ramé, M. Rivière,
et al.
Gemma 3 technical report
.
arXiv preprint arXiv:2503.19786
.
Cited by:
§4.1
.
Grattafiori
et al.
(2024)
A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan,
et al.
The Llama 3 herd of models
.
arXiv preprint arXiv:2407.21783
.
Cited by:
§4.1
.
Hendrycks
et al.
(2021a)
D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt
Measuring massive multitask language understanding
.
In
International Conference on Learning Representations
,
Cited by:
§4.1
.
Hendrycks
et al.
(2021b)
D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
Measuring mathematical problem solving with the MATH dataset
.
In
Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks
,
Vol.
1
.
Cited by:
§4.1
.
Huang
et al.
(2026)
C. Huang, L. Huang, J. Leng, J. Liu, and J. Huang
CaTS: calibrated test-time scaling for efficient LLM reasoning
.
In
International Conference on Learning Representations
,
External Links:
Link
Cited by:
§2
.
Ji
et al.
(2026)
S. Ji, Y. Wang, Y. Liu, Q. Zhu, and W. Che
Seer self-consistency: advance budget estimation for adaptive test-time scaling
.
In
Findings of the Association for Computational Linguistics: ACL 2026
,
pp. 42734–42747
.
External Links:
Document
Cited by:
§1
,
§2
,
§3.2
.
Kim
et al.
(2026)
J. Kim, N. Yang, K. Min, and K. Jung
Reliability-aware adaptive self-consistency for efficient sampling in LLM reasoning
.
In
Findings of the Association for Computational Linguistics: ACL 2026
,
M. Liakata, V. P. Moreira, J. Zhang, and D. Jurgens (Eds.)
,
San Diego, California, United States
,
pp. 21575–21590
.
External Links:
Link
,
Document
Cited by:
§1
,
§2
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
International Conference on Learning Representations
,
Cited by:
§2
.
Li
et al.
(2026a)
P. Li, B. Hou, Y. Zhu, Y. Feng, K. Ye, T. Lei, Z. Chen, T. Chen, and X. Du
Adaptive thinking: large language models know when to think in latent space
.
In
International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
,
§2
.
Li
et al.
(2024)
Y. Li, P. Yuan, S. Feng, B. Pan, X. Wang, B. Sun, H. Wang, and K. Li
Escape sky-high cost: early-stopping self-consistency for multi-step reasoning
.
In
International Conference on Learning Representations
,
Cited by:
§1
,
§2
.
Li
et al.
(2026b)
Z. Li, Q. Dong, J. Ma, D. Zhang, K. Jia, and Z. Sui
SelfBudgeter: adaptive token allocation for efficient LLM reasoning
.
In
Findings of the Association for Computational Linguistics: ACL 2026
,
pp. 21135–21156
.
Cited by:
§1
,
§2
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
§1
,
§2
,
§4.1
.
Liu
et al.
(2026)
Z. Liu, H. Qu, X. Yin, H. Sun, Y. Han, T. Chen, and Z. Deng
PETS: a principled framework towards optimal trajectory allocation for efficient test-time self-consistency
.
In
International Conference on Machine Learning
,
Cited by:
§D.2
,
§2
,
§4.1
.
Manakul
et al.
(2023)
P. Manakul, A. Liusie, and M. Gales
SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
pp. 9004–9017
.
Cited by:
Appendix F
.
Nguyen
et al.
(2026a)
M. Nguyen, S. Gupta, and H. Le
Beyond majority voting: efficient best-of-n with radial consensus score
.
arXiv preprint arXiv:2604.12196
.
Cited by:
§1
.
Nguyen
et al.
(2026b)
M. Nguyen, S. Gupta, and H. Le
Probabilities are all you need: a probability-only approach to uncertainty estimation in large language models
.
In
Proceedings of the AAAI Conference on Artificial Intelligence
,
pp. 32546–32554
.
External Links:
Document
Cited by:
Appendix F
,
§2
.
Nguyen
et al.
(2026c)
M. Nguyen, A. Nguyen, D. Nguyen, S. Venkatesh, and H. Le
Hear both sides: efficient multi-agent debate via diversity-aware message retention
.
arXiv preprint arXiv:2603.20640
.
Cited by:
Appendix D
.
OpenAI (2025)
OpenAI
Gpt-oss-120b & gpt-oss-20b Model Card
.
arXiv preprint arXiv:2508.10925
.
Cited by:
§4.1
.
Settles (2009)
B. Settles
Active learning literature survey
.
Computer Sciences Technical Report
Technical Report
1648
,
University of Wisconsin–Madison
.
Cited by:
§2
.
Snell
et al.
(2025)
C. Snell, J. Lee, K. Xu, and A. Kumar
Scaling LLM test-time compute optimally can be more effective than scaling parameters for reasoning
.
In
International Conference on Learning Representations
,
Vol.
2025
,
pp. 10131–10165
.
Cited by:
§1
,
§2
.
Taubenfeld
et al.
(2025)
A. Taubenfeld, T. Sheffer, E. Ofek, A. Feder, A. Goldstein, Z. Gekhman, and G. Yona
Confidence improves self-consistency in LLMs
.
In
Findings of the Association for Computational Linguistics: ACL 2025
,
pp. 20090–20111
.
Cited by:
§2
.
Wang
et al.
(2025)
X. Wang, S. Feng, Y. Li, P. Yuan, Y. Zhang, C. Tan, B. Pan, Y. Hu, and K. Li
Make every penny count: difficulty-adaptive self-consistency for cost-efficient reasoning
.
In
Findings of the Association for Computational Linguistics: NAACL 2025
,
pp. 6919–6932
.
Cited by:
§D.1
,
§1
,
§2
,
§3.2
,
§4.1
.
Wang
et al.
(2023)
X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou
Self-consistency improves chain of thought reasoning in language models
.
In
International Conference on Learning Representations
,
Cited by:
§1
,
§2
,
§4.1
.
Wu
et al.
(2025)
Y. Wu, Z. Sun, S. Li, S. Welleck, and Y. Yang
Inference scaling laws: an empirical analysis of compute-optimal inference for LLM problem-solving
.
In
International Conference on Learning Representations
,
Vol.
2025
,
pp. 55824–55845
.
Cited by:
§1
,
§2
.
Yan
et al.
(2026)
H. Yan, F. Xu, R. Xu, Y. Li, J. Zhang, H. Luo, X. Wu, A. T. Luu, H. Zhao, Q. Lin, and J. Liu
MUR: momentum uncertainty guided reasoning for large language models
.
In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
M. Liakata, V. P. Moreira, J. Zhang, and D. Jurgens (Eds.)
,
San Diego, California, United States
,
pp. 23078–23103
.
External Links:
Link
,
Document
Cited by:
§1
.
Yang
et al.
(2024)
A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei,
et al.
Qwen2.5 technical report
.
arXiv preprint arXiv:2412.15115
.
Cited by:
§4.1
.
Yoon
et al.
(2026)
T. Yoon, G. Jeong, G. Park, S. Yeom, and H. Kim
Breaking the pre-sampling barrier: activation-informed difficulty-aware self-consistency
.
arXiv preprint arXiv:2602.09438
.
Cited by:
§1
,
§2
.
Zhang
et al.
(2025)
K. Zhang, S. Zhou, D. Wang, W. Y. Wang, and L. Li
Scaling LLM inference efficiently with optimized sample compute allocation
.
In
Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies
,
pp. 7959–7973
.
Cited by:
§1
.
Checklist
1.
For all models and algorithms presented, check if you include:
(a)
A clear description of the mathematical setting, assumptions, algorithm, and/or model. [Yes] Section 3.
(b)
An analysis of the properties and complexity (time, space, sample size) of any algorithm. [Yes] Section 3.
(c)
(Optional) Anonymized source code, with specification of all dependencies, including external libraries. [Yes] Along with the paper submission.
2.
For any theoretical claim, check if you include:
(a)
Statements of the full set of assumptions of all theoretical results. [Yes] Section 3.
(b)
Complete proofs of all theoretical results. [Yes] Appendix A, B.
(c)
Clear explanations of any assumptions. [Yes] Section 3.
3.
For all figures and tables that present empirical results, check if you include:
(a)
The code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL). [Yes]
(b)
All the training details (e.g., data splits, hyperparameters, how they were chosen). [Yes] Section 4.1.
(c)
A clear definition of the specific measure or statistics and error bars (e.g., with respect to the random seed after running experiments multiple times). [Yes] Section 4.1.
(d)
A description of the computing infrastructure used. (e.g., type of GPUs, internal cluster, or cloud provider). [Yes] Appendix D.
4.
If you are using existing assets (e.g., code, data, models) or curating/releasing new assets, check if you include:
(a)
Citations of the creator If your work uses existing assets. [Yes]
(b)
The license information of the assets, if applicable. [Yes] We comply with the licenses of all datasets and models used.
(c)
New assets either in the supplemental material or as a URL, if applicable. [Yes] We create Graded Arithmetics dataset with a full documentation in Appendix E.
(d)
Information about consent from data providers/curators. [Not Applicable] We only use open datasets/models.
(e)
Discussion of sensible content if applicable, e.g., personally identifiable information or offensive content. [Not Applicable]
5.
If you used crowdsourcing or conducted research with human subjects, check if you include:
(a)
The full text of instructions given to participants and screenshots. [Not Applicable]
(b)
Descriptions of potential participant risks, with links to Institutional Review Board (IRB) approvals if applicable. [Not Applicable]
(c)
The estimated hourly wage paid to participants and the total amount spent on participant compensation. [Not Applicable]
Appendix
Appendix A
Optimality of Marginal-Greedy Allocation
The results below are classical for separable concave resource allocation
(
Fox, 1966
;
Federgruen and Groenevelt, 1986
)
; we restate them with self-contained proofs to cover both Eq.
1
(
L
=
1
L{=}1
) and the Phase-2 problem (
L
=
K
L{=}K
) in one statement.
Let
f
i
​
(
m
)
=
1
−
(
1
−
p
i
)
m
f_{i}(m)=1-(1-p_{i})^{m}
and
Δ
i
​
(
m
)
=
f
i
​
(
m
+
1
)
−
f
i
​
(
m
)
=
p
i
​
(
1
−
p
i
)
m
\Delta_{i}(m)=f_{i}(m+1)-f_{i}(m)=p_{i}(1-p_{i})^{m}
(with the convention
0
0
=
1
0^{0}=1
), where
m
m
is the total number of samples of question
i
i
.
For every
p
i
∈
[
0
,
1
]
p_{i}\in[0,1]
,
Δ
i
​
(
m
)
\Delta_{i}(m)
is non-increasing in
m
m
, so each
f
i
f_{i}
is concave on
ℤ
≥
0
\mathbb{Z}_{\geq 0}
; if
p
i
∈
(
0
,
1
)
p_{i}\in(0,1)
, the decrease is strict. Only the non-increasing property is used below, so all results hold for
p
i
∈
[
0
,
1
]
p_{i}\in[0,1]
.
To cover both the original problem Eq.
1
and the Phase-2 sub-problem in one statement, fix an integer floor
L
≥
0
L\geq 0
and consider the feasible set
ℱ
L
=
{
𝑵
∈
ℤ
M
:
∑
i
=
1
M
N
i
=
B
,
N
i
≥
L
∀
i
}
,
\mathcal{F}_{L}=\Bigl\{\bm{N}\in\mathbb{Z}^{M}:\ \textstyle\sum_{i=1}^{M}N_{i}=B,\ N_{i}\geq L\ \forall i\Bigr\},
assumed non-empty (
B
≥
L
​
M
B\geq LM
).
L
=
1
L=1
recovers Eq.
1
;
L
=
K
L=K
gives the Phase-2 sub-problem, which is Eq.
2
under the change of variables
N
i
=
K
+
n
i
N_{i}=K+n_{i}
. Indeed,
∑
i
f
i
​
(
K
+
n
i
)
=
∑
i
(
1
−
p
i
)
K
​
[
1
−
(
1
−
p
i
)
n
i
]
+
∑
i
f
i
​
(
K
)
\sum_{i}f_{i}(K+n_{i})=\sum_{i}(1-p_{i})^{K}\bigl[1-(1-p_{i})^{n_{i}}\bigr]+\sum_{i}f_{i}(K)
, and the last sum does not depend on
𝒏
\bm{n}
.
We say
𝑵
∗
∈
ℱ
L
\bm{N}^{*}\in\mathcal{F}_{L}
satisfies the
marginal-equalization condition
if there exists
λ
∗
≥
0
\lambda^{*}\geq 0
such that
Δ
i
​
(
N
i
∗
−
1
)
≥
λ
∗
∀
i
​
with
​
N
i
∗
>
L
,
Δ
i
​
(
N
i
∗
)
≤
λ
∗
∀
i
.
\Delta_{i}(N_{i}^{*}-1)\;\geq\;\lambda^{*}\quad\forall i\text{ with }N_{i}^{*}>L,\qquad\qquad\Delta_{i}(N_{i}^{*})\;\leq\;\lambda^{*}\quad\forall i.
(9)
For
L
=
K
L=K
this is exactly Eq.
8
;
L
=
1
L=1
gives the corresponding condition for Eq.
1
. Note that the left inequality is imposed only on coordinates strictly above the floor: a coordinate sitting at the floor cannot give up a unit,
so no lower bound on its last marginal is needed.
Proposition 1
(Optimality condition)
.
𝑵
∗
∈
ℱ
L
\bm{N}^{*}\in\mathcal{F}_{L}
maximizes
∑
i
f
i
​
(
N
i
)
\sum_{i}f_{i}(N_{i})
over
ℱ
L
\mathcal{F}_{L}
if and only if it satisfies Eq.
9
.
Proof.
Necessity.
Suppose
𝑵
∗
\bm{N}^{*}
is optimal over
ℱ
L
\mathcal{F}_{L}
. Take any
i
≠
j
i\neq j
with
N
j
∗
>
L
N_{j}^{*}>L
, and let
𝑵
~
\tilde{\bm{N}}
be the allocation with
N
~
i
=
N
i
∗
+
1
\tilde{N}_{i}=N_{i}^{*}+1
,
N
~
j
=
N
j
∗
−
1
\tilde{N}_{j}=N_{j}^{*}-1
,
N
~
k
=
N
k
∗
\tilde{N}_{k}=N_{k}^{*}
for
k
≠
i
,
j
k\neq i,j
.
This is feasible because the total is unchanged and
N
~
j
=
N
j
∗
−
1
≥
L
\tilde{N}_{j}=N_{j}^{*}-1\geq L
.
Since only indices
i
i
and
j
j
differ between
𝑵
~
\tilde{\bm{N}}
and
𝑵
∗
\bm{N}^{*}
, all other terms cancel; using
Δ
i
​
(
m
)
=
f
i
​
(
m
+
1
)
−
f
i
​
(
m
)
\Delta_{i}(m)=f_{i}(m+1)-f_{i}(m)
:
∑
k
f
k
​
(
N
~
k
)
−
∑
k
f
k
​
(
N
k
∗
)
\displaystyle\sum_{k}f_{k}(\tilde{N}_{k})-\sum_{k}f_{k}(N_{k}^{*})
=
[
f
i
​
(
N
i
∗
+
1
)
−
f
i
​
(
N
i
∗
)
]
+
[
f
j
​
(
N
j
∗
−
1
)
−
f
j
​
(
N
j
∗
)
]
\displaystyle\quad=\bigl[f_{i}(N_{i}^{*}+1)-f_{i}(N_{i}^{*})\bigr]+\bigl[f_{j}(N_{j}^{*}-1)-f_{j}(N_{j}^{*})\bigr]
=
Δ
i
​
(
N
i
∗
)
−
Δ
j
​
(
N
j
∗
−
1
)
.
\displaystyle\quad=\Delta_{i}(N_{i}^{*})-\Delta_{j}(N_{j}^{*}-1).
(10)
By optimality of
𝑵
∗
\bm{N}^{*}
this is
≤
0
\leq 0
, i.e.,
Δ
i
​
(
N
i
∗
)
≤
Δ
j
​
(
N
j
∗
−
1
)
\Delta_{i}(N_{i}^{*})\leq\Delta_{j}(N_{j}^{*}-1)
for all
i
≠
j
i\neq j
with
N
j
∗
>
L
N_{j}^{*}>L
.
For
i
=
j
i=j
the same inequality holds because
Δ
j
\Delta_{j}
is non-increasing. Therefore
max
i
Δ
i
(
N
i
∗
)
≤
min
j
:
N
j
∗
>
L
Δ
j
(
N
j
∗
−
1
)
,
\max_{i}\,\Delta_{i}(N_{i}^{*})\;\leq\;\min_{j:\,N_{j}^{*}>L}\Delta_{j}(N_{j}^{*}-1),
with the convention that a minimum over the empty set is
+
∞
+\infty
.
Setting
λ
∗
=
max
i
⁡
Δ
i
​
(
N
i
∗
)
≥
0
\lambda^{*}=\max_{i}\Delta_{i}(N_{i}^{*})\geq 0
, the right inequality of Eq.
9
holds by definition and the left inequality holds by the display above.
Sufficiency.
Suppose Eq.
9
holds for some
λ
∗
≥
0
\lambda^{*}\geq 0
.
For any
𝑵
∈
ℱ
L
\bm{N}\in\mathcal{F}_{L}
and each question
i
i
, the telescoping identity (empty sums equal zero) gives:
f
i
​
(
N
i
)
−
f
i
​
(
N
i
∗
)
\displaystyle f_{i}(N_{i})-f_{i}(N_{i}^{*})
=
∑
m
=
N
i
∗
N
i
−
1
Δ
i
​
(
m
)
−
∑
m
=
N
i
N
i
∗
−
1
Δ
i
​
(
m
)
.
\displaystyle=\sum_{m=N_{i}^{*}}^{N_{i}-1}\!\Delta_{i}(m)-\sum_{m=N_{i}}^{N_{i}^{*}-1}\!\Delta_{i}(m).
(11)
To see this: if
N
i
>
N
i
∗
N_{i}>N_{i}^{*}
, the first sum telescopes
f
i
​
(
N
i
∗
)
→
f
i
​
(
N
i
)
f_{i}(N_{i}^{*})\to f_{i}(N_{i})
and the second is empty; if
N
i
<
N
i
∗
N_{i}<N_{i}^{*}
, the second sum telescopes
f
i
​
(
N
i
)
→
f
i
​
(
N
i
∗
)
f_{i}(N_{i})\to f_{i}(N_{i}^{*})
with a sign flip and the first is empty;
if
N
i
=
N
i
∗
N_{i}=N_{i}^{*}
, both are empty. We bound each non-empty sum using Eq.
9
and monotonicity of
Δ
i
\Delta_{i}
.
•
If
N
i
>
N
i
∗
N_{i}>N_{i}^{*}
: for every
m
≥
N
i
∗
m\geq N_{i}^{*}
,
Δ
i
​
(
m
)
≤
Δ
i
​
(
N
i
∗
)
≤
λ
∗
\Delta_{i}(m)\leq\Delta_{i}(N_{i}^{*})\leq\lambda^{*}
, so
∑
m
=
N
i
∗
N
i
−
1
Δ
i
​
(
m
)
≤
λ
∗
​
(
N
i
−
N
i
∗
)
\sum_{m=N_{i}^{*}}^{N_{i}-1}\Delta_{i}(m)\leq\lambda^{*}(N_{i}-N_{i}^{*})
.
•
If
N
i
<
N
i
∗
N_{i}<N_{i}^{*}
: since
N
i
≥
L
N_{i}\geq L
, we have
N
i
∗
>
L
N_{i}^{*}>L
, so the left inequality
of Eq.
9
applies to
i
i
; for every
m
≤
N
i
∗
−
1
m\leq N_{i}^{*}-1
,
Δ
i
​
(
m
)
≥
Δ
i
​
(
N
i
∗
−
1
)
≥
λ
∗
\Delta_{i}(m)\geq\Delta_{i}(N_{i}^{*}-1)\geq\lambda^{*}
, so
−
∑
m
=
N
i
N
i
∗
−
1
Δ
i
(
m
)
≤
−
λ
∗
(
N
i
∗
−
N
i
)
=
λ
∗
(
N
i
−
N
i
∗
)
-\sum_{m=N_{i}}^{N_{i}^{*}-1}\Delta_{i}(m)\leq-\lambda^{*}(N_{i}^{*}-N_{i})=\lambda^{*}(N_{i}-N_{i}^{*})
.
In all cases:
f
i
​
(
N
i
)
−
f
i
​
(
N
i
∗
)
≤
λ
∗
​
(
N
i
−
N
i
∗
)
.
\displaystyle f_{i}(N_{i})-f_{i}(N_{i}^{*})\leq\lambda^{*}\,(N_{i}-N_{i}^{*}).
(12)
Summing Eq.
12
over all
i
i
:
∑
i
f
i
​
(
N
i
)
−
∑
i
f
i
​
(
N
i
∗
)
≤
λ
∗
​
∑
i
(
N
i
−
N
i
∗
)
=
0
,
\displaystyle\sum_{i}f_{i}(N_{i})-\sum_{i}f_{i}(N_{i}^{*})\leq\lambda^{*}\!\sum_{i}(N_{i}-N_{i}^{*})=0,
where the equality uses
∑
i
N
i
=
∑
i
N
i
∗
=
B
\sum_{i}N_{i}=\sum_{i}N_{i}^{*}=B
.
Hence
∑
i
f
i
​
(
N
i
∗
)
≥
∑
i
f
i
​
(
N
i
)
\sum_{i}f_{i}(N_{i}^{*})\geq\sum_{i}f_{i}(N_{i})
for all
𝑵
∈
ℱ
L
\bm{N}\in\mathcal{F}_{L}
, so
𝑵
∗
\bm{N}^{*}
is optimal over
ℱ
L
\mathcal{F}_{L}
.
∎
Remark.
The floor affects both the exchange argument and the KKT condition. In the Necessity step, an exchange is feasible only when
N
j
∗
>
L
N_{j}^{*}>L
, while in the Sufficiency case
N
i
<
N
i
∗
N_{i}<N_{i}^{*}
implies
N
i
∗
>
L
N_{i}^{*}>L
. Hence, the left inequality in Eq.
9
is required only above the floor. This floor is essential because the Phase-1 samples are already spent, so the relevant feasible set is
ℱ
K
\mathcal{F}_{K}
, not the original
ℱ
1
\mathcal{F}_{1}
.
Appendix B
Greedy Algorithm and its Exactness
Algorithm
1
implements the optimality condition Eq.
9
with
L
=
K
L=K
by simulating the marginal-equalization process one unit at a time. We state the result for
L
=
K
L=K
, as used by UAB; the same proof applies to any floor
L
L
by replacing
K
K
with
L
L
and
B
eff
B_{\mathrm{eff}}
with
B
−
L
​
M
B-LM
.
Proposition 2
(Exactness of Greedy)
.
The marginal-greedy loop of Algorithm
1
returns an exact optimal solution to Eq.
2
, i.e., to Eq.
1
under the additional constraint
N
i
≥
K
N_{i}\geq K
for every
i
i
.
The result holds for any tie-breaking rule in the
arg
⁡
max
\arg\max
.
Proof.
If
B
eff
=
0
B_{\mathrm{eff}}=0
, the only feasible point of Eq.
2
is
𝒏
=
𝟎
\bm{n}=\bm{0}
, which greedy returns. Assume
B
eff
≥
1
B_{\mathrm{eff}}\geq 1
.
Let
n
i
(
t
)
n_{i}^{(t)}
denote the number of Phase-2 units assigned to question
i
i
after step
t
t
, with
n
i
(
0
)
=
0
n_{i}^{(0)}=0
for all
i
i
(every question enters Phase 2 already holding its
K
K
Phase-1 samples), and let
𝒏
G
=
𝒏
(
B
eff
)
\bm{n}^{G}=\bm{n}^{(B_{\mathrm{eff}})}
be the greedy output, so question
i
i
ends with
N
i
G
=
K
+
n
i
G
N_{i}^{G}=K+n_{i}^{G}
samples in total.
At step
t
t
, the
available marginal
of question
i
i
is
a
i
(
t
)
=
Δ
i
​
(
K
+
n
i
(
t
−
1
)
)
a_{i}^{(t)}=\Delta_{i}\bigl(K+n_{i}^{(t-1)}\bigr)
; greedy picks
i
t
∗
∈
arg
⁡
max
i
⁡
a
i
(
t
)
i^{*}_{t}\in\arg\max_{i}a_{i}^{(t)}
and accepts the gain
g
t
=
a
i
t
∗
(
t
)
=
max
i
⁡
a
i
(
t
)
g_{t}=a_{i^{*}_{t}}^{(t)}=\max_{i}a_{i}^{(t)}
.
The accepted gains are non-increasing.
After step
t
t
, the chosen coordinate’s available marginal becomes
Δ
i
t
∗
​
(
K
+
n
i
t
∗
(
t
−
1
)
+
1
)
≤
g
t
\Delta_{i^{*}_{t}}\bigl(K+n_{i^{*}_{t}}^{(t-1)}+1\bigr)\leq g_{t}
because
Δ
i
t
∗
\Delta_{i^{*}_{t}}
is non-increasing, and every other coordinate’s available marginal is unchanged and was already
≤
g
t
\leq g_{t}
. Hence
g
t
+
1
=
max
i
⁡
a
i
(
t
+
1
)
≤
g
t
g_{t+1}=\max_{i}a_{i}^{(t+1)}\leq g_{t}
, so
g
1
≥
g
2
≥
⋯
≥
g
B
eff
g_{1}\geq g_{2}\geq\cdots\geq g_{B_{\mathrm{eff}}}
.
Set
λ
∗
=
g
B
eff
≥
0
\lambda^{*}=g_{B_{\mathrm{eff}}}\geq 0
. We show that
𝑵
G
=
K
​
𝟏
+
𝒏
G
\bm{N}^{G}=K\bm{1}+\bm{n}^{G}
satisfies Eq.
9
with
L
=
K
L=K
and this
λ
∗
\lambda^{*}
.
Left inequality (only for
N
i
G
>
K
N_{i}^{G}>K
).
Take any
i
i
with
n
i
G
>
0
n_{i}^{G}>0
. Its last Phase-2 unit was accepted at some step
t
′
≤
B
eff
t^{\prime}\leq B_{\mathrm{eff}}
, when its count went from
n
i
G
−
1
n_{i}^{G}-1
to
n
i
G
n_{i}^{G}
, so
g
t
′
=
Δ
i
​
(
K
+
n
i
G
−
1
)
=
Δ
i
​
(
N
i
G
−
1
)
g_{t^{\prime}}=\Delta_{i}(K+n_{i}^{G}-1)=\Delta_{i}(N_{i}^{G}-1)
. Since
(
g
t
)
(g_{t})
is non-increasing,
Δ
i
​
(
N
i
G
−
1
)
=
g
t
′
≥
g
B
eff
=
λ
∗
\Delta_{i}(N_{i}^{G}-1)=g_{t^{\prime}}\geq g_{B_{\mathrm{eff}}}=\lambda^{*}
.
Questions with
n
i
G
=
0
n_{i}^{G}=0
sit exactly at the floor
N
i
G
=
K
N_{i}^{G}=K
, and Eq.
9
imposes no lower condition on them.
Right inequality (all
i
i
).
Consider the last step
t
=
B
eff
t=B_{\mathrm{eff}}
.
If
i
≠
i
B
eff
∗
i\neq i^{*}_{B_{\mathrm{eff}}}
, the count of
i
i
does not change at that step, so
n
i
(
B
eff
−
1
)
=
n
i
G
n_{i}^{(B_{\mathrm{eff}}-1)}=n_{i}^{G}
and its available marginal at that step is
a
i
(
B
eff
)
=
Δ
i
​
(
N
i
G
)
a_{i}^{(B_{\mathrm{eff}})}=\Delta_{i}(N_{i}^{G})
; since greedy selected the maximum,
Δ
i
​
(
N
i
G
)
≤
g
B
eff
=
λ
∗
\Delta_{i}(N_{i}^{G})\leq g_{B_{\mathrm{eff}}}=\lambda^{*}
.
If
i
=
i
B
eff
∗
i=i^{*}_{B_{\mathrm{eff}}}
, then
g
B
eff
=
Δ
i
​
(
N
i
G
−
1
)
g_{B_{\mathrm{eff}}}=\Delta_{i}(N_{i}^{G}-1)
, and monotonicity gives
Δ
i
​
(
N
i
G
)
≤
Δ
i
​
(
N
i
G
−
1
)
=
λ
∗
\Delta_{i}(N_{i}^{G})\leq\Delta_{i}(N_{i}^{G}-1)=\lambda^{*}
.
Thus
𝑵
G
∈
ℱ
K
\bm{N}^{G}\in\mathcal{F}_{K}
satisfies Eq.
9
with
L
=
K
L=K
, and by the Sufficiency direction of Proposition
1
,
𝑵
G
\bm{N}^{G}
is optimal over
ℱ
K
\mathcal{F}_{K}
. Under the change of variables
N
i
=
K
+
n
i
N_{i}=K+n_{i}
, this means
𝒏
G
\bm{n}^{G}
is optimal for Eq.
2
.
∎
Appendix C
Allocation Shape and Coverage–Accuracy Divergence
For a question with
e
e
Phase-2 units already allocated, the marginal coverage gain of one additional sample is
Δ
⁡
(
p
,
e
)
=
p
​
(
1
−
p
)
K
+
e
,
\Delta(p;e)=p(1-p)^{K+e},
(13)
where the exponent counts all previous samples. This marginal is unimodal in
p
p
:
∂
Δ
∂
p
=
(
1
−
p
)
K
+
e
−
1
​
[
(
1
−
p
)
−
(
K
+
e
)
​
p
]
,
\frac{\partial\Delta}{\partial p}=(1-p)^{K+e-1}\bigl[(1-p)-(K+e)p\bigr],
(14)
with peak
p
⋆
=
1
K
+
e
+
1
.
p^{\star}=\frac{1}{K+e+1}.
(15)
Thus, marginal-greedy allocation concentrates on intermediate-difficulty questions rather than the easiest or hardest cases. At the first Phase-2 step,
K
=
1
K=1
gives
p
⋆
=
1
/
2
p^{\star}=1/2
, whereas
K
=
2
K=2
gives
p
⋆
=
1
/
3
p^{\star}=1/3
, so additional Phase-1 evidence shifts
the marginal peak toward harder questions. As
e
e
grows,
p
⋆
p^{\star}
decreases toward zero, consistent with the leftward shift of the empirical allocation peak in Figure
4
.
Figure 4:
Marginal gain
Δ
i
​
(
m
)
=
p
i
​
(
1
−
p
i
)
m
\Delta_{i}(m){=}p_{i}(1{-}p_{i})^{m}
as a function of success probability
p
i
p_{i}
, for sample count
m
∈
{
4
,
8
,
12
,
16
}
m\in\{4,8,12,16\}
. The peak (
⋆
\star
), located at
p
⋆
=
1
/
(
m
+
1
)
p^{\star}{=}1/(m{+}1)
, drifts toward
0
0
as
m
m
grows.
For binary correctness with uniform tie-breaking, the coverage objective also differs from the majority-vote evaluation objective. Let
a
⁡
(
p
,
n
)
a(p,n)
denote the majority-vote accuracy of
n
n
i.i.d. samples. Then
a
⁡
(
p
,
2
​
k
)
=
a
⁡
(
p
,
2
​
k
−
1
)
∀
k
≥
1
,
sign
⁡
(
a
⁡
(
p
,
2
​
k
+
1
)
−
a
⁡
(
p
,
2
​
k
)
)
=
sign
⁡
(
p
−
1
2
)
,
a(p,2k)=a(p,2k-1)\ \ \forall k\geq 1,\qquad\operatorname{sign}\!\bigl(a(p,2k{+}1)-a(p,2k)\bigr)=\operatorname{sign}\!\left(p-\tfrac{1}{2}\right),
(16)
The even step is neutral because an odd-sized vote has no ties: the
2
​
k
2k
-th sample can only turn a
k
k
to
k
−
1
k{-}1
win into a
k
k
-
k
k
tie, which uniform tie-breaking resolves with the probability
1
/
2
1/2
. The odd step instead breaks those ties according to
p
p
, so it helps exactly when
p
>
1
/
2
p>1/2
. Hence
sign
⁡
(
a
⁡
(
p
,
n
+
2
)
−
a
⁡
(
p
,
n
)
)
=
sign
⁡
(
p
−
1
2
)
\operatorname{sign}(a(p,n{+}2)-a(p,n))=\operatorname{sign}(p-\tfrac{1}{2})
for every
n
≥
1
n\geq 1
: additional samples improve majority accuracy when
p
>
1
/
2
p>1/2
but reduce it when
p
<
1
/
2
p<1/2
. In contrast, the coverage marginal
Δ
⁡
(
p
,
e
)
\Delta(p;e)
is positive for all
p
∈
(
0
,
1
)
p\in(0,1)
. Thus, as the budget grows and marginal-greedy allocation shifts toward
increasingly hard
questions, the coverage objective continues to assign positive value to questions where additional samples no longer improve majority-vote accuracy. This divergence explains why UAB’s gains concentrate at low budgets.
For multi-class majority voting, the corresponding threshold depends on the strongest competing answer and reduces to
1
/
2
1/2
in the binary case.
Finally, the allocation model assumes conditional independence of repeated samples within a question. Positive within-question correlation, caused for example by shared reasoning biases, would generally reduce the effective gain from additional samples, making the i.i.d. model optimistic about absolute coverage gains. We therefore use this surrogate to rank questions, not to predict realized coverage.
Appendix D
Additional Implementation Details
We follow the inference setup of prior work
(
Choi et al., 2025
;
Nguyen et al., 2026c
)
, using
vLLM
with temperature
1
1
and
max_new_tokens
=
1024
{=}1024
. Results are averaged over three seeds (
42
42
,
44
44
,
46
46
), with all experiments run on a single H100 (80 GB) GPU.
D.1
ASC/DSC matched-budget methodologies
We follow the implementation released with each method’s own code.
Both ASC
(
Aggarwal et al., 2023
)
and DSC
(
Wang et al., 2025
)
stop sampling using a global confidence threshold rather than a target budget. For ASC, we tune the threshold per model, dataset and
N
N
on a grid of thresholds in
[
0.05
,
0.999
]
[0.05,0.999]
, picking the value whose realized budget averaged over seeds is closest to
N
N
.
DSC’s windowed hard-stop rule only activates once part of its window budget has already been spent, so even its most aggressive easy-stop threshold still yields a realized budget of about 15 samples per question, far above our main budgets (
N
=
4
N{=}4
–
8
8
).
We therefore omit DSC from Table
1
instead of reporting it at an unmatched budget.
D.2
PETS offline allocator
We follow the released PETS implementation
(
Liu et al., 2026
)
, adapting its offline optimal knowledge gradient (OKG) allocator to our sampled pools. PETS maintains Dirichlet counts over answer options and greedily selects the question with the largest expected gain for the current majority answer. This gain is estimated by Monte Carlo as the increase in the probability that the majority answer wins a fresh draw. We retain the released defaults of
max_options
=
32
{=}32
, 500 Monte-Carlo draws per decision, and one uniform warm-up sample per question. Warm-up samples count toward the budget, so PETS uses exactly
N
×
M
N\times M
samples in every setting.
D.3
LLM-Judge prompt.
The judge uses the same backbone model as the generator with the following zero-shot prompt:
Is the following question easy or hard for a language model to answer
correctly? Respond with a single word:
easy
or
hard
.
[question text]
Questions labelled
easy
receive
c
min
=
1
c_{\min}=1
sample; questions labelled
hard
divide the remaining budget
(
N
−
c
min
)
×
M
easy
(N-c_{\min})\times M_{\text{easy}}
equally, with any remainder distributed round-robin. If no question is labelled
hard
, no budget is freed and the allocation reduces to Uniform.
Appendix E
Dataset Details
Graded Arithmetic is procedurally generated at 10 discrete difficulty levels, with difficulty controlled by construction rather than inferred post hoc (Table
6
). From level 1 to 10, expressions become progressively more complex through more operands, wider operands, additional operator types, deeper parenthesization, and, at the highest levels, occasional exponentiation. Invalid or overly large expressions are discarded and regenerated, with all retained results bounded by
10
9
10^{9}
.
Answers are parsed as floats and scored correct when they match the reference after rounding to one decimal place. Parentheses may wrap a single operand, for example
(
14
)
(14)
, which does not change the value. We use 100 samples for this dataset, with 10 samples per difficulty level.
More details of other datasets are in Table
7
.
Appendix F
Log-probability-based Uncertainty Metrics
As an alternative to vote-entropy, our framework can use log-probability-based confidence metrics with only a single generation per question (
K
=
1
K{=}1
), leaving more of the budget for Phase-2 reallocation. For the generated sequence
y
i
1
y_{i}^{1}
of length
l
l
, let
u
i
,
t
=
−
log
⁡
P
⁡
(
y
i
,
t
1
∣
x
i
,
y
i
,
<
t
1
)
u_{i,t}=-\log P(y_{i,t}^{1}\mid x_{i},y_{i,<t}^{1})
be the negative log-likelihood (NLL) of token
t
t
and
u
¯
i
=
1
l
​
∑
t
=
1
l
u
i
,
t
\bar{u}_{i}=\frac{1}{l}\sum_{t=1}^{l}u_{i,t}
.
We consider four metrics: the length-unnormalized NLL
(
Nguyen et al., 2026b
)
, its length-normalized counterpart, the average negative log-likelihood (ANLL)
(
Manakul et al., 2023
)
, the variance of token NLLs (Token Var), and the NLL of the least confident token (Max Token NLL):
NLL
i
\displaystyle\mathrm{NLL}_{i}
=
∑
t
=
1
l
u
i
,
t
,
\displaystyle=\sum_{t=1}^{l}u_{i,t},
ANLL
i
\displaystyle\mathrm{ANLL}_{i}
=
u
¯
i
,
\displaystyle=\bar{u}_{i},
(17)
TokenVar
i
\displaystyle\mathrm{TokenVar}_{i}
=
1
l
​
∑
t
=
1
l
(
u
i
,
t
−
u
¯
i
)
2
,
\displaystyle=\frac{1}{l}\sum_{t=1}^{l}\bigl(u_{i,t}-\bar{u}_{i}\bigr)^{2},
MaxTokenNLL
i
\displaystyle\mathrm{MaxTokenNLL}_{i}
=
max
1
≤
t
≤
l
⁡
u
i
,
t
.
\displaystyle=\max_{1\leq t\leq l}u_{i,t}.
Because the four metrics are on different scales, we min-max normalize the chosen metric across all questions in each dataset:
s
i
=
m
i
−
min
j
⁡
m
j
max
j
⁡
m
j
−
min
j
⁡
m
j
,
s_{i}=\frac{m_{i}-\min_{j}m_{j}}{\max_{j}m_{j}-\min_{j}m_{j}},
(18)
where
m
i
m_{i}
denotes the value of the chosen metric for question
i
i
. We then convert the normalized score into a success probability using
p
i
=
e
−
s
i
/
τ
,
(
K
=
1
)
.
p_{i}=e^{-s_{i}/\tau},\qquad(K{=}1).
(19)
These log-probability-based metrics provide alternatives when multiple Phase-1 samples are undesirable or unavailable.
Appendix G
Limitations
Surrogate objective.
UAB optimizes a coverage surrogate rather than majority-vote accuracy directly. Closing this objective gap is left to future work.
Independence assumption.
The allocation model assumes i.i.d. samples within each question, whereas repeated samples may share model-level biases.
Majority-vote aggregation.
UAB requires sampled responses to be mapped to discrete answer categories. Extension to open-ended tasks where majority voting is ill-defined is left to future work.
Modality.
All experiments use text-only models and tasks with extractable answer categories. Extending UAB to multimodal and more open-ended settings is left to future work.
Table 6:
Graded Arithmetic’s 10-level difficulty ladder.
#Ops
= operand count,
MaxDig
= max digits per operand,
Operators
= allowed binary operators,
ParenP
/
ExpP
= probability of a parenthesized sub-expression / a whole-expression exponent wrap (
–
= not yet enabled at that level).
Example
is one real generated question per level.
Level
#Ops
MaxDig
Operators
ParenP
ExpP
Example
1
2
1
+
⁣
−
+-
–
–
3
−
2
=
1
3-2=1
2
3
1
+
⁣
−
+-
–
–
1
−
2
+
2
=
1
1-2+2=1
3
3
1
+
−
∗
+-*
–
–
4
−
9
×
3
=
−
23
4-9\times 3=-23
4
4
2
+
−
∗
+-*
0.20
–
31
−
39
+
(
14
)
−
93
=
−
87
31-39+(14)-93=-87
5
4
2
+
−
∗
/
+-*/
0.25
–
80
+
33
−
95
−
(
46
)
=
−
28
80+33-95-(46)=-28
6
5
2
+
−
∗
/
+-*/
0.30
–
74
+
(
11
÷
63
×
98
)
−
34
=
57.11
74+(11\div 63\times 98)-34=57.11
7
5
3
+
−
∗
/
+-*/
0.35
–
332
+
(
971
)
×
155
−
(
405
)
+
(
667
)
=
151099
332+(971)\times 155-(405)+(667)=151099
8
6
3
+
−
∗
/
+-*/
0.40
0.20
(
233
+
(
380
)
−
986
+
385
÷
(
130
)
÷
(
198
)
)
3
=
−
51888874.28
(233+(380)-986+385\div(130)\div(198))^{3}=-51888874.28
9
6
3
+
−
∗
/
+-*/
0.45
0.40
(
475
+
(
628
)
+
(
383
+
274
)
÷
142
÷
(
191
)
)
2
=
1216662.44
(475+(628)+(383+274)\div 142\div(191))^{2}=1216662.44
10
7
4
+
−
∗
/
+-*/
0.50
0.50
(
2341
÷
(
2900
÷
261
)
+
(
752
)
+
(
14
)
÷
(
2962
)
×
(
1293
)
)
2
=
938576.17
(2341\div(2900\div 261)+(752)+(14)\div(2962)\times(1293))^{2}=938576.17
Table 7:
Benchmark details. “Task” describes the evaluation format; “Size” is the
number of test questions used in our experiments.
Benchmark
Task
Size
HuggingFace path
MATH500
Math (Open)
500
HuggingFaceH4/MATH-500
MMLU Formal Logic
Deductive (MC)
126
cais/mmlu
DeepScaler
Math (Open)
300
lime-nlp/DeepScaleR_Difficulty
GSM8K
Math (Open)
300
openai/gsm8k
Graded Arithmetic
Arithmetic (Open)
100
in-house, procedurally generated
Table 8:
Paired bootstrap on per-question correctness,
10,000
10{,}000
resamples of the questions with the pairing kept, reported as the accuracy difference in points with the two-sided
p
p
in brackets.
Bold
marks
p
<
0.05
p<0.05
, a positive value favors UAB, and the two blocks compare UAB against Uniform and against ASC at the same budget (60 model–dataset–
N
N
cells per block).
Model
Dataset
UAB
−
-
Uniform
UAB
−
-
ASC
N
=
4
N{=}4
N
=
8
N{=}8
N
=
12
N{=}12
N
=
16
N{=}16
N
=
4
N{=}4
N
=
8
N{=}8
N
=
12
N{=}12
N
=
16
N{=}16
Qwen2.5-1.5B
MATH500
+1.8
(0.00)
+1.0 (0.09)
+1.1 (0.06)
+0.5 (0.42)
+3.7
(0.00)
+0.8 (0.24)
+0.7 (0.14)
+0.1 (0.79)
Formal Logic
-0.8 (0.51)
+1.9 (0.14)
+0.8 (0.51)
+1.1 (0.31)
-1.6 (0.10)
-0.3 (0.78)
+0.0 (1.00)
+0.0 (1.00)
DeepScaler
+1.2
(0.04)
+1.8
(0.00)
+0.7 (0.33)
+0.1 (0.93)
+3.1
(0.00)
+4.1
(0.00)
+1.1 (0.16)
+0.1 (0.93)
GSM8K
+5.6
(0.00)
+3.4
(0.00)
+2.3
(0.02)
-0.1 (0.98)
-3.3
(0.00)
-2.1
(0.01)
-0.4 (0.53)
+0.0 (1.00)
Graded Arith.
+2.0 (0.16)
+4.3
(0.00)
-0.3 (0.88)
+0.0 (1.00)
+7.3
(0.00)
+1.7 (0.17)
+0.7 (0.60)
-0.3 (0.84)
Llama3.2-3B
MATH500
+1.2
(0.00)
+0.8 (0.16)
+0.9 (0.11)
-0.1 (0.97)
+5.9
(0.00)
+6.0
(0.00)
+2.1
(0.00)
+0.3 (0.56)
Formal Logic
+2.6 (0.12)
+1.1 (0.61)
+3.7
(0.02)
+2.1 (0.24)
-2.9 (0.08)
-0.3 (0.92)
+0.8 (0.56)
-0.5 (0.75)
DeepScaler
+0.7 (0.16)
-0.1 (0.91)
+0.3 (0.49)
+0.4 (0.49)
+1.2 (0.14)
-1.0 (0.12)
+0.2 (0.78)
+0.7 (0.29)
GSM8K
+5.6
(0.00)
+1.6 (0.06)
+1.4 (0.11)
+0.7 (0.45)
-0.6 (0.52)
-0.7 (0.29)
+0.0 (1.00)
+0.0 (1.00)
Graded Arith.
+1.7 (0.17)
+1.0 (0.36)
+0.7 (0.65)
+1.3 (0.27)
+0.7 (0.63)
-1.0 (0.34)
+0.0 (1.00)
+0.0 (1.00)
Qwen2.5-7B
MATH500
+1.2
(0.02)
+0.9 (0.10)
+0.1 (0.95)
+0.2 (0.73)
-0.2 (0.75)
-0.6
(0.05)
+0.0 (1.00)
+0.0 (1.00)
Formal Logic
+2.1 (0.12)
-1.9 (0.14)
-0.3 (0.91)
-1.9 (0.15)
+1.6 (0.21)
-0.5 (0.64)
+0.0 (1.00)
+0.0 (1.00)
DeepScaler
+4.6
(0.00)
+1.0 (0.26)
+0.6 (0.56)
-0.1 (0.95)
+4.0
(0.00)
+0.0 (1.00)
-0.1 (0.92)
+0.1 (0.92)
GSM8K
+4.0
(0.00)
+0.7 (0.36)
-0.9 (0.18)
-1.2
(0.03)
-0.2 (0.69)
+0.0 (1.00)
+0.0 (1.00)
+0.0 (1.00)
Graded Arith.
+3.3
(0.01)
+1.7 (0.36)
-2.0 (0.23)
-2.7
(0.02)
+0.3 (0.88)
+1.7 (0.06)
+0.3 (0.79)
+0.3 (0.73)
Table 9:
Allocation categories relative to Oracle(
q
q
) at
N
=
4
N{=}4
, per dataset (Qwen2.5-1.5B, average over three seeds), backing Table
5
. %Under: questions given fewer samples than Oracle(
q
q
), hence always wrong; %Over-C/%Over-W: over-sampled questions (budget
>
>
Oracle(
q
q
)) whose final vote is correct/wrong. %Censored is the rate of questions never correct within the first
N
=
16
N{=}16
samples (Oracle(
q
q
) undefined there, excluded from every other column).
Bold
/
underline
= best/second-best per dataset among the non-reference rows (lower is better for %Under/%Over-W, higher for %Over-C).
Allocation Signal
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
%Under
%Over-C
%Over-W
%Under
%Over-C
%Over-W
%Under
%Over-C
%Over-W
%Under
%Over-C
%Over-W
%Under
%Over-C
%Over-W
%Censored
40.1%
46.8%
69.3%
16.6%
31.7%
Random
17.7
60.7
6.6
9.0
65.7
10.4
25.4
42.4
14.9
20.4
55.1
10.5
19.5
63.4
5.4
Length
13.8
71.9
8.2
5.5
78.6
13.9
23.2
52.5
18.1
15.2
65.2
13.4
12.7
76.6
4.9
Uniform
13.1
75.1
8.1
5.5
79.6
13.4
21.4
53.6
19.2
14.4
66.4
14.0
12.2
78.0
4.4
LLM-Judge
16.0
44.7
10.8
7.5
62.7
14.4
23.9
27.9
25.0
15.2
52.1
18.0
22.4
18.5
3.9
ASC
15.7
68.0
8.1
2.0
81.6
15.4
30.4
45.7
14.1
9.9
68.4
8.0
16.6
67.3
6.8
PETS
19.5
65.0
9.4
8.0
73.1
9.5
27.9
47.8
18.8
25.4
51.7
17.2
20.5
67.8
7.3
Oracle (Difficulty)
‡
15.5
61.1
9.0
–
–
–
–
–
–
–
–
–
12.7
58.5
8.8
UAB (ANLL,
K
=
1
K{=}1
)
12.6
74.4
9.1
3.0
75.6
18.4
22.5
53.6
17.0
14.9
64.8
12.6
12.2
76.1
4.9
UAB (NLL,
K
=
1
K{=}1
)
13.9
72.0
8.6
2.5
71.6
15.9
25.0
50.7
18.8
14.9
64.4
12.3
13.7
71.2
7.3
UAB (Vote Entropy,
K
=
2
K{=}2
)
10.7
79.6
7.6
3.0
78.6
17.4
18.1
57.2
18.5
11.2
76.0
10.5
9.3
85.4
4.4
Oracle
(true minimum)
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
Table 10:
Fixed per-level sample budgets used by
Oracle (Difficulty)
, with a linear ramp from 1 sample at the easiest level to the most at the hardest. The ramp is constructed from each dataset’s level distribution to achieve a weighted average of at most
N
=
4
N{=}4
. The resulting averages are
3.96
3.96
for MATH500 and exactly
4
4
for Graded Arithmetic.
Dataset
Level (1 = easiest)
Wtd. Avg.
MATH500 (1–5)
1
2
3
5
6
–
–
–
–
–
3.96
Graded Arith. (1–10)
1
2
2
3
4
4
5
6
6
7
4.00
Figure 5:
Per-dataset breakdown of Figure
3
(main text, §
4.3
), Qwen2.5-1.5B. Both rows on the same gain-over-Uniform
(%) scale.
Top row:
gain vs. sharpness
τ
\tau
at
N
=
4
N{=}4
.
Bottom row:
gain vs. Phase-1 sample
K
K
, at each budget
N
∈
{
4
,
8
,
12
,
16
}
N\in\{4,8,12,16\}
.
Table 11:
Full per-dataset breakdown of the difficulty-signal ablation (
N
=
4
N{=}4
,
τ
=
1
\tau{=}1
, Llama3.2-3B and Qwen2.5-7B).
Bold
/
underline
= best/second-best over the five ranking signals (ties share the mark), AUROC ranks each signal’s raw score against Phase-1 correctness, computed per dataset and then averaged over the 5 datasets.
Model
Ranking Signal
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
Avg
AUROC
Llama3.2-3B
UAB w/o Uncertainty
33.7
±1.3
41.5
±0.7
16.9
±0.9
74.6
±2.3
61.0
±2.2
45.5
–
UAB w/o probe reuse
33.3
±0.7
42.9
±2.3
18.1
±0.6
78.4
±0.6
62.0
±0.8
46.9
–
NLL
32.3
±2.1
41.8
±0.4
15.8
±0.2
75.6
±1.5
62.0
±0.8
45.5
0.756
Token Var
32.5
±1.7
39.9
±1.0
17.1
±0.2
75.4
±1.6
62.0
±1.4
45.4
0.704
Max Token NLL
32.7
±2.1
40.7
±1.0
16.2
±0.6
75.7
±1.4
61.3
±1.2
45.3
0.729
ANLL
33.0
±1.4
41.8
±0.4
16.7
±0.3
75.6
±1.4
62.3
±1.9
45.9
0.679
UAB (Vote Entropy)
34.9
±0.8
44.2
±1.3
17.6
±1.0
80.1
±0.4
62.7
±1.2
47.9
0.762
Qwen2.5-7B
UAB w/o Uncertainty
65.6
±0.6
60.6
±2.7
26.1
±1.8
88.4
±0.6
58.3
±1.7
59.8
–
UAB w/o probe reuse
66.5
±0.7
62.4
±0.4
29.2
±1.3
92.6
±1.6
62.7
±0.9
62.7
–
NLL
65.8
±1.1
61.6
±3.3
27.4
±2.3
89.7
±0.7
59.3
±0.5
60.8
0.736
Token Var
66.1
±0.7
61.1
±1.1
27.8
±1.1
89.2
±1.2
59.3
±0.9
60.7
0.561
Max Token NLL
65.9
±1.0
60.8
±3.3
27.2
±0.8
89.7
±0.9
58.7
±1.2
60.5
0.659
ANLL
65.6
±0.8
61.4
±1.3
28.1
±0.9
89.2
±0.3
59.7
±1.9
60.8
0.533
UAB (Vote Entropy)
66.8
±0.6
62.7
±0.6
30.7
±1.4
92.4
±1.5
61.7
±1.7
62.9
0.781
Table 12:
Wall-clock time (s) per full-dataset run at budget
N
=
4
N{=}4
. PETS was run offline on the sampled pools, so its row is Uniform’s generation time plus PETS’s measured allocation time at
N
=
4
N{=}4
.
Bold
= fastest per column.
†
\dagger
our method.
Method
Formal Logic
MATH500
Qwen2.5-1.5B
Llama3.2-3B
Qwen2.5-1.5B
Llama3.2-3B
Random
45 ± 5
54 ± 5
139 ± 5
111 ± 1
Length
45 ± 3
52 ± 1
145 ± 1
118 ± 1
Uniform
43 ± 1
51 ± 1
136 ± 1
110 ± 1
LLM-Judge
43 ± 1
56 ± 1
144 ± 1
123 ± 1
ASC
60 ± 6
64 ± 6
113 ± 5
105 ± 4
PETS
157 ± 1
153 ± 1
1815 ± 27
1867 ± 30
UAB
†
49 ± 1
54 ± 0
134 ± 3
109 ± 2
Table 13:
Average
per-sample
token consumption (input / output / total), i.e. each question’s token total divided by the number of samples it actually used, averaged across questions then mean
±
std over 3 seeds.
Bold
= lowest value in each In/Out/Total column.
†
\dagger
our method.
Qwen2.5-1.5B
Llama3.2-3B
Method
Formal Logic
MATH500
Formal Logic
MATH500
In
Out
Total
In
Out
Total
In
Out
Total
In
Out
Total
Random
161
±0
136
±2
297
±2
139
±0
507
±6
645
±6
167
±0
277
±3
445
±3
143
±0
354
±3
496
±3
Length
161
±0
144
±2
305
±2
139
±0
504
±4
643
±4
167
±0
280
±3
447
±3
143
±0
351
±5
493
±5
Uniform
161
±0
143
±3
304
±3
139
±0
504
±5
643
±5
167
±0
281
±3
448
±3
143
±0
353
±3
496
±3
LLM-Judge
161
±0
140
±11
302
±11
139
±0
509
±2
648
±2
167
±0
271
±5
438
±5
143
±0
345
±7
488
±7
ASC
161
±0
136
±8
297
±8
139
±0
507
±4
646
±4
167
±0
274
±5
441
±5
143
±0
349
±2
492
±2
PETS
161
±0
139
±8
300
±8
139
±0
514
±1
653
±1
167
±0
272
±5
439
±5
143
±0
349
±7
491
±7
UAB
†
161
±0
136
±7
297
±7
139
±0
507
±5
646
±5
167
±0
279
±4
446
±4
143
±0
350
±3
493
±3
Table 14:
Full accuracy (%) at
N
=
8
N=8
.
Bold
= best per model–dataset cell.
†
\dagger
our method.
Model
Method
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
Avg
Qwen2.5-1.5B
Random
48.7
±
\pm
0.7
43.7
±
\pm
3.4
19.7
±
\pm
0.8
63.7
±
\pm
1.5
54.7
±
\pm
2.9
46.1
Length
49.7
±
\pm
0.8
42.9
±
\pm
1.7
20.9
±
\pm
2.1
68.6
±
\pm
1.1
60.0
±
\pm
0.0
48.4
Uniform
51.0
±
\pm
0.7
42.1
±
\pm
0.0
21.6
±
\pm
1.7
69.0
±
\pm
1.5
60.3
±
\pm
0.5
48.8
LLM-Judge
48.9
±
\pm
0.3
43.1
±
\pm
1.0
21.4
±
\pm
1.5
69.0
±
\pm
1.0
53.3
±
\pm
2.1
47.1
ASC
51.2
±
\pm
1.1
44.2
±
\pm
1.9
19.2
±
\pm
0.4
74.6
±
\pm
2.7
63.0
±
\pm
0.8
50.4
PETS
49.9
±
\pm
1.4
43.9
±
\pm
0.4
19.2
±
\pm
0.7
68.7
±
\pm
1.4
60.0
±
\pm
2.2
48.3
UAB
†
52.0
±
\pm
0.6
43.9
±
\pm
1.0
23.3
±
\pm
0.7
72.4
±
\pm
2.6
64.7
±
\pm
1.7
51.3
Llama3.2-3B
Random
36.5
±
\pm
0.5
41.8
±
\pm
2.6
16.8
±
\pm
1.3
76.2
±
\pm
1.1
62.0
±
\pm
1.4
46.7
Length
37.7
±
\pm
1.1
44.4
±
\pm
1.7
18.1
±
\pm
0.3
80.9
±
\pm
0.7
62.7
±
\pm
0.9
48.8
Uniform
39.9
±
\pm
1.1
45.8
±
\pm
2.9
18.7
±
\pm
0.5
80.9
±
\pm
0.4
62.3
±
\pm
1.2
49.5
LLM-Judge
38.9
±
\pm
1.6
41.8
±
\pm
2.0
18.2
±
\pm
1.0
80.6
±
\pm
1.3
63.7
±
\pm
1.7
48.6
ASC
34.7
±
\pm
1.5
47.1
±
\pm
1.5
19.6
±
\pm
0.4
83.1
±
\pm
0.6
64.3
±
\pm
2.1
49.8
PETS
36.7
±
\pm
0.8
43.1
±
\pm
1.0
17.6
±
\pm
1.0
81.3
±
\pm
1.2
64.3
±
\pm
0.5
48.6
UAB
†
40.7
±
\pm
0.5
46.8
±
\pm
1.7
18.6
±
\pm
1.0
82.4
±
\pm
1.4
63.3
±
\pm
0.9
50.4
Qwen2.5-7B
Random
65.4
±
\pm
0.6
63.2
±
\pm
2.0
28.7
±
\pm
2.4
89.7
±
\pm
0.5
61.7
±
\pm
2.4
61.7
Length
67.5
±
\pm
0.2
63.0
±
\pm
1.0
30.1
±
\pm
2.0
92.2
±
\pm
0.4
66.3
±
\pm
1.2
63.8
Uniform
66.5
±
\pm
0.5
63.2
±
\pm
0.4
30.7
±
\pm
1.5
92.0
±
\pm
0.3
65.7
±
\pm
2.6
63.6
LLM-Judge
67.2
±
\pm
0.4
61.1
±
\pm
2.3
31.4
±
\pm
2.1
86.0
±
\pm
1.4
62.3
±
\pm
3.4
61.6
ASC
68.1
±
\pm
0.2
61.9
±
\pm
2.8
31.7
±
\pm
1.9
92.7
±
\pm
0.5
65.7
±
\pm
1.7
64.0
PETS
67.2
±
\pm
0.3
63.2
±
\pm
1.0
29.2
±
\pm
1.0
94.6
±
\pm
0.6
69.0
±
\pm
0.8
64.6
UAB
†
67.5
±
\pm
0.2
61.4
±
\pm
2.0
31.7
±
\pm
1.8
92.7
±
\pm
0.5
67.3
±
\pm
1.7
64.1
Table 15:
Full accuracy (%) at
N
=
12
N=12
.
Bold
= best per model–dataset cell.
†
\dagger
our method.
Model
Method
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
Avg
Qwen2.5-1.5B
Random
49.5
±
\pm
0.7
42.6
±
\pm
2.6
21.9
±
\pm
2.3
65.8
±
\pm
1.3
57.3
±
\pm
1.2
47.4
Length
52.5
±
\pm
1.3
42.6
±
\pm
1.3
22.6
±
\pm
1.2
73.1
±
\pm
1.5
64.0
±
\pm
0.8
51.0
Uniform
52.7
±
\pm
1.3
43.7
±
\pm
1.1
23.4
±
\pm
1.7
72.6
±
\pm
1.5
64.7
±
\pm
0.5
51.4
LLM-Judge
49.8
±
\pm
0.5
43.4
±
\pm
0.4
21.6
±
\pm
1.5
70.9
±
\pm
0.7
53.0
±
\pm
2.4
47.7
ASC
53.0
±
\pm
0.6
44.4
±
\pm
1.7
23.0
±
\pm
0.7
75.3
±
\pm
2.6
63.7
±
\pm
0.9
51.9
PETS
52.9
±
\pm
0.8
44.4
±
\pm
1.7
21.2
±
\pm
1.0
76.6
±
\pm
1.7
64.3
±
\pm
0.5
51.9
UAB
†
53.7
±
\pm
0.1
44.4
±
\pm
1.7
24.1
±
\pm
0.6
74.9
±
\pm
2.2
64.3
±
\pm
1.2
52.3
Llama3.2-3B
Random
38.5
±
\pm
0.6
42.3
±
\pm
1.0
17.1
±
\pm
2.0
77.3
±
\pm
1.2
62.3
±
\pm
1.2
47.5
Length
41.3
±
\pm
0.4
46.8
±
\pm
1.3
18.9
±
\pm
0.6
81.8
±
\pm
1.4
64.0
±
\pm
0.8
50.6
Uniform
42.5
±
\pm
0.5
44.4
±
\pm
1.7
19.1
±
\pm
0.4
81.7
±
\pm
1.4
63.7
±
\pm
0.5
50.3
LLM-Judge
42.1
±
\pm
0.2
43.7
±
\pm
1.9
19.2
±
\pm
1.0
81.4
±
\pm
0.6
64.3
±
\pm
1.2
50.1
ASC
41.3
±
\pm
1.0
47.4
±
\pm
2.0
19.2
±
\pm
0.3
83.1
±
\pm
0.6
64.3
±
\pm
2.1
51.1
PETS
39.9
±
\pm
0.8
47.6
±
\pm
0.6
18.3
±
\pm
1.0
83.6
±
\pm
0.8
64.0
±
\pm
1.6
50.7
UAB
†
43.4
±
\pm
0.8
48.1
±
\pm
1.3
19.4
±
\pm
1.0
83.1
±
\pm
0.6
64.3
±
\pm
2.1
51.7
Qwen2.5-7B
Random
66.1
±
\pm
0.4
62.7
±
\pm
1.1
29.2
±
\pm
1.5
90.8
±
\pm
1.5
63.3
±
\pm
1.9
62.4
Length
67.5
±
\pm
0.2
62.2
±
\pm
0.7
32.1
±
\pm
1.6
93.4
±
\pm
0.8
69.3
±
\pm
0.9
64.9
Uniform
68.0
±
\pm
0.4
61.9
±
\pm
1.1
31.4
±
\pm
1.3
93.6
±
\pm
1.2
69.3
±
\pm
0.5
64.8
LLM-Judge
67.5
±
\pm
1.0
61.1
±
\pm
2.8
31.9
±
\pm
1.6
92.7
±
\pm
0.5
62.3
±
\pm
4.2
63.1
ASC
68.1
±
\pm
0.3
61.6
±
\pm
3.0
32.1
±
\pm
1.5
92.7
±
\pm
0.5
67.0
±
\pm
2.2
64.3
PETS
67.9
±
\pm
0.3
63.2
±
\pm
2.5
32.2
±
\pm
1.1
94.4
±
\pm
0.8
70.0
±
\pm
1.4
65.5
UAB
†
68.1
±
\pm
0.3
61.6
±
\pm
3.0
32.0
±
\pm
1.5
92.7
±
\pm
0.5
67.3
±
\pm
1.7
64.3
Table 16:
Full accuracy (%) at
N
=
16
N=16
.
Bold
= best per model–dataset cell.
†
\dagger
our method.
Model
Method
MATH500
Formal Logic
DeepScaler
GSM8K
Graded Arithmetic
Avg
Qwen2.5-1.5B
Random
50.8
±
\pm
0.6
42.3
±
\pm
2.0
21.9
±
\pm
2.4
68.4
±
\pm
1.8
59.3
±
\pm
0.5
48.5
Length
53.4
±
\pm
0.9
43.9
±
\pm
1.5
23.0
±
\pm
1.9
75.6
±
\pm
1.0
63.3
±
\pm
1.2
51.8
Uniform
53.4
±
\pm
1.0
43.4
±
\pm
1.0
23.7
±
\pm
0.8
75.4
±
\pm
0.7
63.7
±
\pm
1.2
51.9
LLM-Judge
50.3
±
\pm
0.1
42.9
±
\pm
0.0
21.7
±
\pm
1.4
73.1
±
\pm
0.6
61.3
±
\pm
1.7
49.9
ASC
53.7
±
\pm
0.9
44.4
±
\pm
1.7
23.7
±
\pm
0.0
75.3
±
\pm
2.6
64.0
±
\pm
0.8
52.2
PETS
54.3
±
\pm
0.7
45.0
±
\pm
1.9
22.2
±
\pm
1.2
77.2
±
\pm
1.5
63.7
±
\pm
1.2
52.5
UAB
†
53.9
±
\pm
0.3
44.4
±
\pm
1.7
23.8
±
\pm
0.7
75.3
±
\pm
2.6
63.7
±
\pm
0.9
52.2
Llama3.2-3B
Random
40.7
±
\pm
0.2
41.3
±
\pm
0.6
17.4
±
\pm
1.0
77.9
±
\pm
0.8
63.0
±
\pm
1.4
48.1
Length
42.7
±
\pm
0.5
46.0
±
\pm
1.7
19.3
±
\pm
0.3
82.6
±
\pm
2.1
63.3
±
\pm
1.2
50.8
Uniform
43.8
±
\pm
0.8
44.2
±
\pm
0.4
19.6
±
\pm
1.1
82.4
±
\pm
1.5
63.0
±
\pm
0.8
50.6
LLM-Judge
43.5
±
\pm
0.7
46.6
±
\pm
1.0
19.1
±
\pm
0.6
82.4
±
\pm
1.0
64.7
±
\pm
0.9
51.3
ASC
43.4
±
\pm
1.1
46.8
±
\pm
3.0
19.3
±
\pm
0.5
83.1
±
\pm
0.6
64.3
±
\pm
2.1
51.4
PETS
42.4
±
\pm
1.1
47.9
±
\pm
2.1
19.7
±
\pm
1.0
83.8
±
\pm
0.4
64.7
±
\pm
2.1
51.7
UAB
†
43.7
±
\pm
0.6
46.3
±
\pm
1.9
20.0
±
\pm
0.7
83.1
±
\pm
0.6
64.3
±
\pm
2.1
51.5
Qwen2.5-7B
Random
66.4
±
\pm
0.2
63.8
±
\pm
1.9
30.1
±
\pm
0.8
90.9
±
\pm
0.9
64.0
±
\pm
2.8
63.0
Length
68.1
±
\pm
0.3
61.9
±
\pm
0.6
32.7
±
\pm
0.7
94.1
±
\pm
0.9
70.3
±
\pm
1.9
65.4
Uniform
67.9
±
\pm
0.5
63.5
±
\pm
1.3
31.8
±
\pm
0.7
93.9
±
\pm
0.8
70.0
±
\pm
1.6
65.4
LLM-Judge
66.9
±
\pm
0.8
61.1
±
\pm
2.2
31.9
±
\pm
0.6
93.6
±
\pm
1.0
65.0
±
\pm
0.8
63.7
ASC
68.1
±
\pm
0.3
61.6
±
\pm
3.0
31.6
±
\pm
1.2
92.7
±
\pm
0.5
67.0
±
\pm
2.2
64.2
PETS
68.0
±
\pm
0.3
62.4
±
\pm
2.5
32.7
±
\pm
0.3
94.4
±
\pm
0.8
69.3
±
\pm
0.9
65.4
UAB
†
68.1
±
\pm
0.3
61.6
±
\pm
3.0
31.7
±
\pm
0.9
92.7
±
\pm
0.5
67.3
±
\pm
2.4
64.3