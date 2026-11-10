---
title: 'ACES: Who Tests the Tests? Leave-One-OutAUC Consistency for Code Generation'
id: aces-who-tests-the-tests-leave-one-outauc-consistency-for-code-generation
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
- l4
- test-adequacy
- self-written-tests
created: '2026-11-09T23:08:35.897807Z'
updated: '2026-11-09T23:27:44.487201Z'
source: https://arxiv.org/html/2604.03922
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:35.897204Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Sun et al. (Nanjing Univ., arXiv 2604.03922v2, 12 Jul 2026, full text). Selects
  LLM-generated code using LLM-generated tests by weighting each test with a leave-one-out
  AUC computed solely from the binary code-by-test pass matrix; proves expected LOO-AUC
  is proportional to a test's ability to separate correct from incorrect code and
  gives a Pass@k lower bound (Pass@k(w) >= 1 - (n-/k) exp(-R(w)/2)). ACES-C closed
  form, ACES-O iterative. Evaluated on HumanEval, HumanEval+, MBPP with GPT-3.5-Turbo
  candidates (about 200) and tests (about 500) from Huang et al. 2024. Occupies self-written
  test adequacy/weighting for code selection; no confidence calibration, no ECE, no
  per-requirement grouping, no repair.
---

ACES: Who Tests the Tests? Leave-One-OutAUC Consistency for Code Generation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2604.03922v2 [cs.LG] 12 Jul 2026
ACES: Who Tests the Tests? Leave-One-Out
AUC Consistency for Code Generation
Hui Sun   Yun-Ji Zhang   Zheng Xie   Ren-Biao Liu
Affiliation:
National Key Laboratory for Novel Software Technology, Nanjing University, China
Affiliation:
School of Artificial Intelligence, Nanjing University, China
Yali Du   Xin-Ye Li   Ming Li
Email:
{sunh, zhangyunji, xiez, liurb, duyl, lixy, lim}@lamda.nju.edu.cn
*
Equal contribution.
†
Corresponding author.
Affiliation:
National Key Laboratory for Novel Software Technology, Nanjing University, China
Affiliation:
School of Artificial Intelligence, Nanjing University, China
Abstract
Selecting LLM-generated code candidates using LLM-generated tests is challenging because the tests themselves may be incorrect.
Existing methods treat all tests equally or use ad-hoc heuristics to filter unreliable tests.
Yet determining test correctness requires knowing which codes are correct, creating a
circular dependency
.
Our key insight is that we need not determine test correctness at all:
test votes should rank, not merely count
.
What matters is not how many codes pass a test, but whether it can
distinguish
correct from incorrect code.
We break the circular dependency via leave-one-out evaluation: hold out one test, rank codes by their aggregate scores on all remaining tests, and measure whether the held-out test’s pass/fail pattern agrees with this ranking.
We formalize this agreement as the leave-one-out AUC (LOO-AUC) and prove that the expected LOO-AUC is proportional to each test’s ability to separate correct code from incorrect code.
Building on this, we propose
ACES
(
A
UC
C
onsist
E
ncy
S
coring) with two complementary variants: ACES-C provides closed-form weights that provably approximate the oracle in expectation under a mild assumption on average test quality; ACES-O drops this assumption and iteratively optimizes a differentiable LOO-AUC objective.
Both operate solely on the binary pass matrix with negligible overhead, and achieve state-of-the-art Pass@
k
k
on multiple code generation benchmarks.
1
Introduction
Large language models (LLMs) have demonstrated strong capabilities in code generation
(
Chen et al., 2021
;
Guo et al., 2024
;
Liu et al., 2025
;
Du et al., 2025
)
, yet individual generations are not always correct.
A promising strategy is to scale test-time computation
(
Snell et al., 2025
;
Brown et al., 2024
;
Wu et al., 2025
)
: generate many candidate solutions together with test cases, and select the best candidates based on test execution
(
Li et al., 2022
;
Chen et al., 2023
)
.
The central challenge is that
neither the code nor the tests are guaranteed to be correct
: we need reliable tests to judge code quality, and reliable code to judge test quality, but have neither.
Existing methods either treat all tests equally via majority voting or rely on heuristics: CodeT
(
Chen et al., 2023
)
scores consensus sets by size without weighting individual tests, while MBR-exec (Minimum Bayes Risk)
(
Shi et al., 2022
)
and SRank
(
To et al., 2024
)
require pairwise output comparison beyond the binary pass matrix.
More heavyweight approaches co-evolve code and tests via reinforcement learning
(
Wang et al., 2025
)
or evolutionary search
(
Li et al., 2025b
)
, requiring substantially more computation.
Yet the
circular dependency
between code and test quality remains: to our knowledge, no existing method offers formal guarantees for identifying reliable tests without knowing which codes are correct.
What should such a criterion measure? We observe that code selection is fundamentally a ranking problem: we must order candidates so that correct solutions appear near the top.
Our key insight is that, for this ranking task, a test’s value lies not in its correctness but in its ability to
distinguish
correct code from incorrect code: a trivially correct test that all codes pass offers no ranking signal, while a demanding test that separates candidates is valuable even if imperfect.
Test votes should rank, not merely count.
Under uniform counting, however, this distinction is lost: easy tests that most codes pass dilute the ranking signal, while tests that favor incorrect codes actively corrupt it.
How can we measure a test’s ability to distinguish codes without knowing which codes are correct?
We break the circular dependency via
leave-one-out evaluation among tests themselves
.
Hold out a single test from the generated test set; the remaining tests, aggregated via any reasonable weighting, induce a ranking of the code candidates.
If codes ranked highly by the other tests also tend to pass the held-out test, then the test is informative.
If it
contradicts
the ranking, it is misleading.
If it is uncorrelated, it is uninformative.
This evaluation requires no knowledge of code correctness; it exploits only the internal structure of the pass matrix.
We formalize this as the leave-one-out AUC (LOO-AUC): the area under the ROC curve with the remaining tests’ aggregate scores as predictions and each held-out test’s pass/fail column as the label.
A test contributes to ranking to the extent that correct codes are more likely to pass it than incorrect codes; we call this difference the test’s
discriminative power
.
This quantity is latent, since code correctness is unknown.
Yet LOO-AUC requires no knowledge of code correctness.
We prove that each test’s expected LOO-AUC is proportional to its discriminative power, with a coefficient that depends on the test’s pass-rate variance and the ranking quality of the remaining tests (Theorem
3
).
This provides the theoretical basis for principled non-uniform test weighting.
Building on this, we propose
ACES
(AUC Consistency Scoring) with two complementary variants.
ACES-C
applies the pass-rate correction in closed form under uniform weighting, provably approximating the oracle-optimal test weights in expectation under a mild assumption on average test quality (Theorem
6
).
ACES-O
instead iteratively optimizes the test weights through a differentiable LOO-AUC objective, without requiring this assumption.
Both operate solely on the binary pass matrix with negligible overhead.
The two are complementary: the average-quality assumption holds for the majority of tasks, and in this regime ACES-C’s one-shot correction is near-optimal; for more challenging tasks where it fails, ACES-O’s iterative optimization remains effective.
Our main contributions are as follows:
•
Theoretical foundation.
We introduce the LOO-AUC identity (Theorem
3
), linking each test’s observable consistency with the ranking to its latent discriminative power. To our knowledge, this is the first provable criterion for distinguishing informative from misleading tests using only the binary pass matrix.
•
Algorithms.
Building on this identity, we propose two lightweight algorithms. ACES-C provides closed-form weights provably approximating the oracle-optimal weights in expectation (Theorem
6
); ACES-O iteratively optimizes test weights via a differentiable LOO-AUC objective without requiring the average-quality assumption.
•
Empirical results.
We show that ACES advances the state-of-the-art in Pass@
k
k
on multiple benchmarks, with ACES-O leading as a standalone method and ACES-C excelling as a plug-and-play execution-only scorer when combined with other pre-filtering mechanisms.
2
Theoretical Foundations
We formalize code ranking as a weighted voting problem over the pass matrix and develop the theoretical tools that motivate ACES.
2.1
Problem Setup
Given a programming problem, an LLM generates
n
n
candidate solutions
C
=
{
c
1
,
…
,
c
n
}
C=\{c_{1},\ldots,c_{n}\}
and
m
m
test cases
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
T=\{t_{1},\ldots,t_{m}\}
.
Executing every candidate on every test yields the
pass matrix
B
∈
{
0
,
1
}
n
×
m
,
B
i
​
j
=
𝟏
​
[
c
i
​
passes
​
t
j
]
.
B\in\{0,1\}^{n\times m},\qquad B_{ij}=\mathbf{1}[c_{i}\text{ passes }t_{j}].
(1)
Each code has an unknown correctness label
y
i
∈
{
0
,
1
}
y_{i}\in\{0,1\}
; we write
n
+
=
|
{
i
:
y
i
=
1
}
|
n^{+}=|\{i:y_{i}=1\}|
and
n
−
=
n
−
n
+
n^{-}=n-n^{+}
.
Test quality is also unknown: some tests may have incorrect expected outputs.
Since test reliability varies, we parameterize code ranking by a weight vector over tests:
w
∈
Δ
m
=
{
w
∈
ℝ
+
m
:
∑
j
w
j
=
1
}
w\in\Delta^{m}=\{w\in\mathbb{R}^{m}_{+}:\sum_{j}w_{j}=1\}
induces scores
s
i
​
(
w
)
=
∑
j
=
1
m
w
j
​
B
i
​
j
s_{i}(w)=\sum_{j=1}^{m}w_{j}B_{ij}
.
Codes are ranked by
s
i
​
(
w
)
s_{i}(w)
in descending order (ties broken uniformly at random).
We evaluate with
Pass@
​
k
\text{Pass@}k
, the probability that at least one correct code appears in the top
k
k
:
Pass@
k
(
w
)
=
P
(
min
i
:
y
i
=
1
rank
(
c
i
)
≤
k
)
.
\text{Pass@}k(w)=P\!\left(\min_{i:\,y_{i}=1}\rank(c_{i})\leq k\right).
(2)
The simplest baseline,
majority voting
, sets
w
unif
=
(
1
/
m
,
…
,
1
/
m
)
w_{\mathrm{unif}}=(1/m,\ldots,1/m)
, ranking codes by total passes.
Pairwise analysis.
To understand how
w
w
affects ranking, consider a correct code
c
+
c^{+}
and an incorrect code
c
−
c^{-}
.
Each test
t
j
t_{j}
casts a
vote
h
j
=
B
c
+
,
j
−
B
c
−
,
j
∈
{
+
1
,
0
,
−
1
}
h_{j}=B_{c^{+},j}-B_{c^{-},j}\in\{+1,0,-1\}
on their ordering (Table
1
), and the score difference
s
c
+
​
(
w
)
−
s
c
−
​
(
w
)
=
∑
j
w
j
​
h
j
s_{c^{+}}(w)-s_{c^{-}}(w)=\sum_{j}w_{j}h_{j}
is the weighted sum of these votes: code ranking is a
weighted voting problem
.
Averaging over all such pairs, the probability that
w
w
places the correct code above the incorrect one defines the
true AUC
:
A
⁡
(
w
)
=
P
⁡
(
s
c
+
​
(
w
)
>
s
c
−
​
(
w
)
)
+
1
2
​
P
​
(
s
c
+
​
(
w
)
=
s
c
−
​
(
w
)
)
.
A(w)\;=\;P(s_{c^{+}}(w)>s_{c^{-}}(w))\;+\;\frac{1}{2}\,P(s_{c^{+}}(w)=s_{c^{-}}(w)).
(3)
Since
A
⁡
(
w
)
A(w)
depends on unknown code labels, it cannot be computed directly and appears only in the analysis.
Under uniform weighting, misleading tests contribute as much as informative ones, actively lowering
A
⁡
(
w
)
A(w)
and corrupting the ranking.
Constant columns of
B
B
(all codes agree) yield only uninformative votes and are removed in preprocessing; we assume this throughout.
2.2
Discriminative Power and Pass@k Bound
Codes and tests are typically sampled independently from the LLM.
Conditioned on its correctness label
y
i
y_{i}
, each code’s test outcomes are identically distributed and independent across tests.
This conditional independence is standard when codes and tests are sampled independently from the LLM, and is shared by classical item response theory.
Definition 1
(Discriminative Power)
.
For each test
t
j
t_{j}
, define the
class-conditional pass rates
and
discriminative power
:
α
j
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
1
)
,
β
j
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
0
)
,
δ
j
=
α
j
−
β
j
.
\alpha_{j}=P(B_{ij}=1\mid y_{i}=1),\qquad\beta_{j}=P(B_{ij}=1\mid y_{i}=0),\qquad\delta_{j}=\alpha_{j}-\beta_{j}.
A test is
informative
(
δ
j
>
0
\delta_{j}>0
),
uninformative
(
δ
j
=
0
\delta_{j}=0
), or
misleading
(
δ
j
<
0
\delta_{j}<0
) according to whether correct codes are more, equally, or less likely to pass it than incorrect ones.
Type
Condition
h
j
h_{j}
Effect
Informative
c
+
c^{+}
pass,
c
−
c^{-}
fail
+
1
+1
Raises
s
c
+
−
s
c
−
s_{c^{+}}\!-\!s_{c^{-}}
Uninformative
Both same
0
0
No effect
Misleading
c
−
c^{-}
pass,
c
+
c^{+}
fail
−
1
-1
Lowers
s
c
+
−
s
c
−
s_{c^{+}}\!-\!s_{c^{-}}
Table 1:
Vote types for a test
t
j
t_{j}
on a correct-incorrect pair
(
c
+
,
c
−
)
(c^{+},c^{-})
.
Each test casts a vote
h
j
=
B
c
+
,
j
−
B
c
−
,
j
h_{j}=B_{c^{+},j}-B_{c^{-},j}
on their ordering;
the score difference
s
c
+
−
s
c
−
=
∑
j
w
j
​
h
j
s_{c^{+}}\!-\!s_{c^{-}}=\sum_{j}w_{j}h_{j}
is the weighted aggregate.
Figure 1:
For ranking, only
δ
j
\delta_{j}
matters.
Taxonomy of tests by correctness (
α
j
\alpha_{j}
) and discriminative power (
δ
j
\delta_{j}
).
Figure
1
refines this classification by test correctness: correct tests (
α
j
=
1
\alpha_{j}=1
) are always informative, while incorrect tests (
α
j
<
1
\alpha_{j}<1
) may be constructive (
δ
j
>
0
\delta_{j}>0
) or misleading (
δ
j
<
0
\delta_{j}<0
).
Prior correctness-based filters discard constructive tests together with misleading ones, losing valuable ranking signal; for ranking, only
δ
j
\delta_{j}
matters.
Equivalently,
δ
j
=
𝔼
⁡
[
h
j
]
\delta_{j}=\mathbb{E}[h_{j}]
is the expected pairwise vote.
Pass@
​
k
\text{Pass@}k
is controlled by a signal-to-noise ratio determined by
w
w
and
{
δ
j
}
\{\delta_{j}\}
:
Theorem 2
(Pass@k Bound)
.
Define the
mean signal
and
signal-to-noise ratio
of weights
w
w
:
M
⁡
(
w
)
:=
∑
j
w
j
​
δ
j
,
R
⁡
(
w
)
:=
M
​
(
w
)
2
∑
j
w
j
2
.
M(w)\;:=\;\sum_{j}w_{j}\delta_{j},\qquad R(w)\;:=\;\frac{M(w)^{2}}{\sum_{j}w_{j}^{2}}.
For any
w
w
with
M
⁡
(
w
)
>
0
M(w)>0
and any
k
≥
1
k\geq 1
:
Pass@
​
k
​
(
w
)
≥
1
−
n
−
k
​
exp
⁡
(
−
R
⁡
(
w
)
2
)
,
\text{Pass@}k(w)\;\geq\;1-\frac{n^{-}}{k}\,\exp\!\left(-\frac{R(w)}{2}\right),
(4)
where
n
−
=
n
−
n
+
n^{-}=n-n^{+}
is the number of incorrect codes.
Over non-negative weights,
R
⁡
(
w
)
R(w)
is maximized by
w
j
∗
∝
max
⁡
(
0
,
δ
j
)
w^{*}_{j}\propto\max(0,\;\delta_{j})
.
The proof is in Appendix
A.2
.
The bound improves exponentially with
R
⁡
(
w
)
R(w)
, but the oracle-optimal weights
w
∗
w^{*}
require knowing the unknown discriminative powers
δ
j
\delta_{j}
.
Majority voting baseline.
Writing
δ
¯
:=
(
1
/
m
)
​
∑
j
=
1
m
δ
j
\bar{\delta}:=(1/m)\sum_{j=1}^{m}\delta_{j}
, substituting uniform weights gives
R
⁡
(
w
unif
)
=
m
​
δ
¯
2
R(w_{\mathrm{unif}})=m\bar{\delta}^{2}
and hence:
Pass@
​
k
​
(
w
unif
)
≥
1
−
n
−
k
​
exp
⁡
(
−
m
​
δ
¯
2
2
)
.
\text{Pass@}k(w_{\mathrm{unif}})\;\geq\;1-\frac{n^{-}}{k}\,\exp\!\left(-\frac{m\bar{\delta}^{2}}{2}\right).
(5)
Non-uniform weights can improve this bound by increasing
R
⁡
(
w
)
R(w)
beyond
m
​
δ
¯
2
m\bar{\delta}^{2}
, but the optimal weights
w
∗
w^{*}
are unknown in practice.
2.3
Estimating Test Quality for Ranking: LOO-AUC Identity
The discriminative powers
δ
j
\delta_{j}
are unknown, but the pass matrix
B
B
provides
m
m
surrogate label vectors, one per test column.
An informative test’s column correlates with the unknown
y
y
, while a misleading test’s column anti-correlates.
To distinguish the two, one can hold out test
t
j
t_{j}
, rank codes by their aggregate scores on the remaining tests, and measure whether
t
j
t_{j}
’s pass/fail pattern agrees with that ranking.
Formally, the
leave-one-out scores
and
LOO-AUC
are:
S
i
(
−
j
)
=
∑
j
′
≠
j
w
j
′
B
i
​
j
′
,
LOO
-
AUC
j
(
w
)
=
AUC
(
S
(
−
j
)
,
B
:
,
j
)
,
S^{(-j)}_{i}=\sum_{j^{\prime}\neq j}w_{j^{\prime}}\,B_{ij^{\prime}},\qquad\mathrm{LOO\text{-}AUC}_{j}(w)=\AUC\!\left(S^{(-j)},\;B_{:,j}\right),
(6)
where
S
(
−
j
)
S^{(-j)}
serves as scores and
B
:
,
j
B_{:,j}
as binary labels.
Both are computed from the pass matrix
B
B
alone;
no knowledge of
y
y
is required
.
LOO
​
-
​
AUC
j
\mathrm{LOO\text{-}AUC}_{j}
measures the
consistency
between test
t
j
t_{j}
and the remaining tests: the probability that, among codes distinguished by
t
j
t_{j}
, those passing it are ranked higher by the remaining tests.
A high value (
LOO
​
-
​
AUC
j
>
1
/
2
\mathrm{LOO\text{-}AUC}_{j}>1/2
) indicates agreement with the consensus ranking; a low value (
LOO
​
-
​
AUC
j
<
1
/
2
\mathrm{LOO\text{-}AUC}_{j}<1/2
) indicates disagreement.
The following identity formalizes how this consistency measure relates to discriminative power
δ
j
\delta_{j}
:
Theorem 3
(LOO-AUC Identity)
.
Let
A
(
−
j
)
​
(
w
)
A^{(-j)}(w)
denote the true AUC (Eq.
3
) computed from all tests except
t
j
t_{j}
.
For any weights
w
w
:
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
)
]
−
1
2
=
c
j
​
(
w
)
⋅
δ
j
,
c
j
​
(
w
)
:=
π
⁡
(
1
−
π
)
p
j
​
(
1
−
p
j
)
​
(
A
(
−
j
)
​
(
w
)
−
1
2
)
,
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w)]-\frac{1}{2}\;=\;c_{j}(w)\cdot\delta_{j},\qquad c_{j}(w)\;:=\;\frac{\pi(1-\pi)}{p_{j}(1-p_{j})}\left(A^{(-j)}(w)-\frac{1}{2}\right),
(7)
where
π
=
n
+
/
n
\pi=n^{+}/n
is the correct-code fraction and
p
j
=
P
⁡
(
B
i
​
j
=
1
)
p_{j}=P(B_{ij}=1)
the marginal pass rate of
t
j
t_{j}
.
The proof is in Appendix
A.3
.
The coefficient
c
j
​
(
w
)
c_{j}(w)
has two test-dependent factors: the inverse pass-rate variance
1
/
[
p
j
​
(
1
−
p
j
)
]
1/[p_{j}(1-p_{j})]
and the leave-one-out ranking quality
A
(
−
j
)
​
(
w
)
−
1
/
2
A^{(-j)}(w)-1/2
.
In Section
3
, we exploit this decomposition to construct test weights that target the discriminative powers
δ
j
\delta_{j}
.
3
ACES: AUC Consistency Scoring
We use the LOO-AUC Identity (Theorem
3
) to construct non-uniform test weights that improve Pass@
k
k
through two complementary approaches: ACES-C applies a closed-form pass-rate correction, while ACES-O optimizes weights via differentiable LOO-AUC.
3.1
ACES-C: Closed-Form Weighting
The LOO-AUC Identity (Theorem
3
) gives
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
)
]
−
1
/
2
=
c
j
​
(
w
)
⋅
δ
j
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w)]-1/2=c_{j}(w)\cdot\delta_{j}
.
When
c
j
​
(
w
)
>
0
c_{j}(w)>0
, LOO-AUC excess shares the same sign as
δ
j
\delta_{j}
, so tests scoring above
1
/
2
1/2
are identified as informative and those below as misleading.
This holds whenever
A
(
−
j
)
​
(
w
)
>
1
/
2
A^{(-j)}(w)>1/2
, i.e., the remaining tests rank correct codes higher, the natural regime since the complement would mean the aggregate ranking is no better than random.
To guarantee this for all
j
j
under uniform weights, we introduce:
Assumption 4
.
The average discriminative power is positive, and the test pool is large enough that leaving out any single test has negligible effect on the aggregate ranking. Quantitatively:
δ
¯
:=
1
m
​
∑
j
=
1
m
δ
j
>
2
​
ln
⁡
2
m
.
\bar{\delta}\;:=\;\frac{1}{m}\sum_{j=1}^{m}\delta_{j}\;>\;2\sqrt{\frac{\ln 2}{m}}.
This is our only assumption beyond the model in Section
2.2
; the threshold is
O
⁡
(
1
/
m
)
O(1/\sqrt{m})
, and unlike the classical
weak learner
condition
(
Freund et al., 2003
)
, which requires
every
ranker to be better than random, ours requires this only
on average
, permitting arbitrarily many misleading tests.
Proposition 5
(Structure of
c
j
​
(
w
unif
)
c_{j}(w_{\mathrm{unif}})
)
.
Under Assumption
4
,
A
(
−
j
)
​
(
w
unif
)
>
1
/
2
A^{(-j)}(w_{\mathrm{unif}})>1/2
for all
j
j
, so
c
j
​
(
w
unif
)
>
0
c_{j}(w_{\mathrm{unif}})>0
.
Moreover,
A
(
−
j
)
​
(
w
unif
)
A^{(-j)}(w_{\mathrm{unif}})
is approximately constant across
j
j
.
The proof and quantitative bound are in Appendix
A.4
.
Under uniform weights,
A
(
−
j
)
​
(
w
unif
)
−
1
/
2
A^{(-j)}(w_{\mathrm{unif}})-1/2
is approximately constant across
j
j
(Proposition
5
).
Combined with the constant
π
⁡
(
1
−
π
)
\pi(1-\pi)
, the only significant test-dependent factor in
c
j
​
(
w
unif
)
c_{j}(w_{\mathrm{unif}})
is
1
/
[
p
j
​
(
1
−
p
j
)
]
1/[p_{j}(1-p_{j})]
.
Multiplying the LOO-AUC excess by
p
j
​
(
1
−
p
j
)
p_{j}(1-p_{j})
removes this distortion:
w
j
=
max
⁡
(
0
,
LOO
​
-
​
AUC
j
​
(
w
unif
)
−
1
2
)
⋅
p
j
​
(
1
−
p
j
)
,
w_{j}\;=\;\max\!\left(0,\;\mathrm{LOO\text{-}AUC}_{j}(w_{\mathrm{unif}})-\frac{1}{2}\right)\cdot p_{j}(1-p_{j}),
(8)
where
p
j
=
1
n
​
∑
i
=
1
n
B
i
​
j
p_{j}=\frac{1}{n}\sum_{i=1}^{n}B_{ij}
is the empirical pass rate of test
j
j
.
The
max
⁡
(
0
,
⋅
)
\max(0,\cdot)
ensures non-negative weights, assigning zero weight to tests with
LOO
​
-
​
AUC
j
≤
1
/
2
\mathrm{LOO\text{-}AUC}_{j}\leq 1/2
and filtering out those identified as misleading.
Since only relative magnitudes affect the induced ranking, normalization is unnecessary.
The following theorem shows that the pass-rate-corrected LOO-AUC excess recovers the discriminative power
δ
j
\delta_{j}
exactly in expectation.
Theorem 6
(ACES-C Recovers Discriminative Power)
.
Under Assumption
4
, define the
quality score
q
j
:=
(
LOO
​
-
​
AUC
j
​
(
w
unif
)
−
1
2
)
​
p
j
​
(
1
−
p
j
)
q_{j}:=(\mathrm{LOO\text{-}AUC}_{j}(w_{\mathrm{unif}})-\tfrac{1}{2})\,p_{j}(1{-}p_{j})
. Then:
𝔼
⁡
[
q
j
]
=
π
⁡
(
1
−
π
)
​
(
A
(
−
j
)
​
(
w
unif
)
−
1
2
)
⋅
δ
j
.
\mathbb{E}[q_{j}]\;=\;\pi(1-\pi)\!\left(A^{(-j)}(w_{\mathrm{unif}})-\frac{1}{2}\right)\cdot\delta_{j}.
In particular,
𝔼
⁡
[
q
j
]
>
0
\mathbb{E}[q_{j}]>0
if and only if
δ
j
>
0
\delta_{j}>0
: the expected quality score’s sign identifies informative versus misleading tests.
Since
A
(
−
j
)
​
(
w
unif
)
A^{(-j)}(w_{\mathrm{unif}})
is nearly constant in
j
j
(Proposition
5
),
𝔼
⁡
[
q
j
]
∝
δ
j
\mathbb{E}[q_{j}]\propto\delta_{j}
.
Proof.
By Theorem
3
,
𝔼
⁡
[
LOO
​
-
​
AUC
j
]
−
1
/
2
=
c
j
​
δ
j
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}]-1/2=c_{j}\delta_{j}
with
c
j
=
π
⁡
(
1
−
π
)
p
j
​
(
1
−
p
j
)
​
(
A
(
−
j
)
−
1
/
2
)
>
0
c_{j}=\frac{\pi(1-\pi)}{p_{j}(1-p_{j})}(A^{(-j)}-1/2)>0
under Assumption
4
.
Multiplying by
p
j
​
(
1
−
p
j
)
p_{j}(1{-}p_{j})
cancels the
1
/
[
p
j
​
(
1
−
p
j
)
]
1/[p_{j}(1{-}p_{j})]
factor in
c
j
c_{j}
, yielding
𝔼
⁡
[
q
j
]
=
π
⁡
(
1
−
π
)
​
(
A
(
−
j
)
−
1
/
2
)
​
δ
j
\mathbb{E}[q_{j}]=\pi(1{-}\pi)(A^{(-j)}-1/2)\,\delta_{j}
.
Positivity when
δ
j
>
0
\delta_{j}>0
follows from
A
(
−
j
)
>
1
/
2
A^{(-j)}>1/2
(Proposition
5
).
∎
The ACES-C weight (Eq.
8
) is
w
j
=
max
⁡
(
0
,
q
j
)
w_{j}=\max(0,\,q_{j})
: by the sign property above, the clipping assigns positive weight precisely to tests that are informative in expectation (
δ
j
>
0
\delta_{j}>0
), targeting the oracle
w
j
∗
∝
max
⁡
(
0
,
δ
j
)
w^{*}_{j}\propto\max(0,\,\delta_{j})
.
Quantitatively, the ACES-C weights achieve near-oracle signal-to-noise ratio:
R
≥
ρ
2
​
R
∗
R\geq\rho^{2}R^{*}
where
ρ
→
1
\rho\to 1
as
m
m
grows (Corollary
8
in Appendix
A.5
).
3.2
ACES-O: Optimized Weighting
ACES-C is an efficient closed-form method with provable guarantees under Assumption
4
.
When the assumption may fail, ACES-O jointly optimizes the weights and their induced ranking:
max
w
∈
Δ
m
⁡
J
⁡
(
w
)
=
∑
j
=
1
m
w
j
​
(
LOO
​
-
​
AUC
j
​
(
w
)
−
1
2
)
,
\max_{w\in\Delta^{m}}\;\;J(w)\;=\;\sum_{j=1}^{m}w_{j}\,\bigl(\mathrm{LOO\text{-}AUC}_{j}(w)-\frac{1}{2}\bigr),
(9)
where
LOO
​
-
​
AUC
j
​
(
w
)
\mathrm{LOO\text{-}AUC}_{j}(w)
depends on
w
w
through the leave-one-out scores
S
(
−
j
)
​
(
w
)
S^{(-j)}(w)
(Eq.
6
).
The simplex constraint leaves the induced ranking unchanged but prevents unbounded weights and ill-defined optimization.
ACES-C evaluates LOO-AUC once under uniform weights, whereas ACES-O reevaluates it under the current weights
w
w
.
In ACES-O, tests with LOO-AUC below
1
/
2
1/2
are softly down-weighted, not permanently excluded; as the leave-one-out ranking improves, their values can rise above
1
/
2
1/2
, recovering initially excluded informative tests.
Theoretical motivation.
The LOO-AUC identity (Theorem
3
) gives
𝔼
⁡
[
J
⁡
(
w
)
]
=
∑
j
=
1
m
w
j
​
c
j
​
(
w
)
​
δ
j
.
\mathbb{E}[J(w)]\;=\;\sum_{j=1}^{m}w_{j}\,c_{j}(w)\,\delta_{j}.
(10)
When
c
j
​
(
w
)
>
0
c_{j}(w)>0
, each term has the same sign as
δ
j
\delta_{j}
: informative tests increase
𝔼
⁡
[
J
⁡
(
w
)
]
\mathbb{E}[J(w)]
while misleading tests decrease it.
Maximizing
J
⁡
(
w
)
J(w)
thus drives the weights toward informative tests and away from misleading ones, without requiring knowledge of
δ
j
\delta_{j}
.
Assumption
4
guarantees
c
j
​
(
w
unif
)
>
0
c_{j}(w_{\mathrm{unif}})>0
for all
j
j
(Proposition
5
), providing a valid starting point.
As the optimization updates
w
w
, the leave-one-out ranking improves, raising
c
j
​
(
w
)
c_{j}(w)
for previously misidentified tests and creating a positive feedback loop that can succeed even when the assumption is only weakly satisfied.
Since the AUC is non-differentiable, we optimize a logistic surrogate via gradient ascent; pseudocode, pre-filtering, and hyperparameters are in Appendix
B
.
Appendix
C.1
illustrates this complementarity with two constructed examples: ACES-C suffices when Assumption
4
is well met, whereas ACES-O recovers initially missed informative tests when it is only weakly met.
4
Experiments
We evaluate ACES-C and ACES-O on three code generation benchmarks, focusing on: (1) comparison with existing reranking methods, (2) empirical validation of Assumption
4
, and (3) analysis of robustness and test quality detection under LOO-AUC-based weighting.
4.1
Setup
Benchmarks and generation.
We evaluate on HumanEval
(
Chen et al., 2021
)
(164 problems), HumanEval
+
(
Liu et al., 2023
)
(164 problems, stricter tests), and MBPP
(
Austin et al., 2021
)
(427 problems).
We use candidate solutions and tests from
Huang et al. (2024)
, generated by GPT-3.5-Turbo, with approximately 200 candidates and 500 tests per problem.
We report Pass@
k
k
for
k
∈
{
1
,
2
,
5
}
k\in\{1,2,5\}
.
For reranking methods, Pass@
k
k
follows Eq.
2
; for direct inference baselines, Pass@
k
k
is the unbiased estimator of
Chen et al. (2021)
, averaging over random
k
k
-subsets of candidates.
Baselines.
We compare with post-hoc methods using code
×
\times
test execution:
Majority Voting (
w
unif
w_{\mathrm{unif}}
),
CodeT
(
Chen et al., 2023
)
(consensus-set scoring on the pass matrix),
and MBR-exec
(
Shi et al., 2022
)
(pairwise output comparison beyond the pass matrix);
and methods requiring additional information:
SC+Spec
(
Huang et al., 2024
)
(execution + specification consistency voting),
Self-collaborate
(
Dong et al., 2024
)
(multi-agent LLM calls),
MPSC
(
Huang et al., 2024
)
(multi-perspective consistency voting; Uniform variant, using only inter-consistency),
and
𝒟
​
𝒮
3
\mathcal{DS}^{3}
(
Liu et al., 2026
)
(static analysis).
We also include direct inference from GPT-3.5-Turbo, GPT-4
(
Achiam et al., 2023
)
, DeepSeek-Coder
(
Guo et al., 2024
)
, WizardCoder
(
Luo et al., 2024
)
, and CodeLlama
(
Roziere et al., 2023
)
.
All post-hoc methods share GPT-3.5-Turbo candidates and tests.
Implementation details of ACES-C and ACES-O are in Appendix
B
; results with additional generation models and benchmarks are in Appendix
C
.
4.2
Main Results
Table 2:
Pass@
k
k
(%) on HumanEval, HumanEval
+
, and MBPP. Post-hoc methods rerank GPT-3.5-Turbo candidates (
n
≈
200
n{\approx}200
,
m
≈
500
m{\approx}500
). Subscripts denote the change from GPT-3.5-Turbo direct inference.
Bold
/
underline
: best/second-best within each group.
Shaded
: ours.
HumanEval
HumanEval
+
MBPP
Method
Pass@1
Pass@2
Pass@5
Pass@1
Pass@2
Pass@5
Pass@1
Pass@2
Pass@5
Direct inference
GPT-3.5-Turbo
68.38
76.24
83.15
58.75
66.58
73.96
66.80
72.34
76.60
GPT-4
81.48
86.31
90.46
70.52
75.48
79.54
71.26
74.27
76.99
DeepSeek-Coder
79.30
–
–
–
–
–
70.00
–
–
WizardCoder
73.20
–
–
–
–
–
61.20
–
–
CodeLlama
62.20
–
–
–
–
–
62.20
–
–
Post-hoc reranking using only code
×
\times
test execution
MBR-exec
72.96
+4.6
76.47
+0.2
79.00
-4.2
62.12
+3.4
67.08
+0.5
71.38
-2.6
70.79
+4.0
73.14
+0.8
74.85
-1.8
CodeT
78.05
+9.7
78.05
+1.8
78.30
-4.9
67.87
+9.1
68.75
+2.2
69.65
-4.3
71.90
+5.1
71.95
-0.4
72.02
-4.6
Majority Voting
80.49
+12.1
82.93
+6.7
83.54
+0.4
69.51
+10.8
73.17
+6.6
76.83
+2.9
68.62
+1.8
70.49
-1.9
72.83
-3.8
ACES-C
82.93
+14.6
82.93
+6.7
82.93
-0.2
71.34
+12.6
71.95
+5.4
74.39
+0.4
71.19
+4.4
71.43
-0.9
72.37
-4.2
ACES-O
84.15
+15.8
85.98
+9.7
86.59
+3.4
74.39
+15.6
75.61
+9.0
79.88
+5.9
72.37
+5.6
73.54
+1.2
73.77
-2.8
Post-hoc reranking using additional information
SC+Spec
73.86
+5.5
73.93
-2.3
74.10
-9.1
63.50
+4.8
64.70
-1.9
65.67
-8.3
71.70
+4.9
71.73
-0.6
71.82
-4.8
Self-collaborate
74.40
+6.0
–
–
–
–
–
68.20
+1.4
–
–
MPSC
74.17
+5.8
77.02
+0.8
78.53
-4.6
65.05
+6.3
69.76
+3.2
71.72
-2.2
69.34
+2.5
70.06
-2.3
71.85
-4.8
𝒟
​
𝒮
3
\mathcal{DS}^{3}
81.71
+13.3
82.32
+6.1
82.32
-0.8
72.56
+13.8
73.78
+7.2
75.00
+1.0
75.88
+9.1
77.28
+4.9
78.45
+1.9
ACES-C +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
85.37
+17.0
85.98
+9.7
87.20
+4.1
77.44
+18.7
78.66
+12.1
81.10
+7.1
76.11
+9.3
77.28
+4.9
78.69
+2.1
ACES-O +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
83.54
+15.2
83.54
+7.3
85.98
+2.8
75.00
+16.3
76.22
+9.6
79.88
+5.9
76.58
+9.8
77.28
+4.9
78.69
+2.1
Table
2
summarizes the results. Using only the binary pass matrix, ACES achieves the best Pass@
k
k
among all execution-based methods on all three benchmarks. When further combined with complementary static-analysis methods, it yields the best overall results across all benchmarks.
Execution-only methods.
Among execution-only methods, ACES-O achieves the best Pass@
k
k
on all three benchmarks.
On HumanEval, ACES-O reaches 84.15% Pass@1 versus 81.71% for
𝒟
​
𝒮
3
\mathcal{DS}^{3}
, which leverages additional static-analysis signals beyond the pass matrix.
On HumanEval
+
, whose stricter criteria increase the fraction of misleading tests among the same generated test suite, ACES-O reaches 74.39% Pass@1, again outperforming
𝒟
​
𝒮
3
\mathcal{DS}^{3}
(72.56%) despite using only the pass matrix.
The gain over Majority Voting widens relative to HumanEval (+4.88% vs. +3.66% Pass@1), consistent with our theory: when misleading tests are more prevalent, principled test weighting provides greater benefit (Section
4.3
).
On MBPP, ACES-O leads all execution-only methods (72.37% Pass@1) but trails
𝒟
​
𝒮
3
\mathcal{DS}^{3}
(75.88%), whose orthogonal static-analysis signals are complementary.
Overall, ACES surpasses all baselines on HumanEval and HumanEval
+
using only the pass matrix; on MBPP, only
𝒟
​
𝒮
3
\mathcal{DS}^{3}
(static analysis) ranks higher.
Combination with static analysis.
𝒟
​
𝒮
3
\mathcal{DS}^{3}
operates in two stages: heuristic pre-filtering of candidates, followed by static-analysis scoring (Pylint, AST similarity, cyclomatic complexity).
We reuse its first-stage filtering and combine the second-stage static-analysis scores with ACES scores via a weighted sum (details in Appendix
B
).
ACES-C +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
improves over
𝒟
​
𝒮
3
\mathcal{DS}^{3}
alone on all three benchmarks (
+
3.66
+3.66
/
+
4.88
+4.88
/
+
0.23
+0.23
Pass@1 on HumanEval/HumanEval
+
/MBPP); ACES-O +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
similarly improves, with the largest gain on MBPP (
+
0.70
+0.70
), confirming that the two methods capture orthogonal signals.
Interestingly, ACES-C +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
outperforms ACES-O +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
on HumanEval and HumanEval
+
(e.g., 85.37% vs. 83.54% Pass@1 on HumanEval), because pre-filtering improves candidate quality and makes Assumption
4
better satisfied, a regime where ACES-C’s closed-form correction is already near-optimal (as illustrated in Appendix
C.1
).
In practice, ACES-O extracts more signal for standalone reranking, while ACES-C’s closed-form weights integrate more effectively with high-quality pre-filtering and require no optimization.
Comparison of ACES variants.
ACES-C and ACES-O are alternative weighting schemes rather than cumulative components. ACES-C improves Pass@1 over Majority Voting on all three benchmarks (e.g., 82.93% vs. 80.49% on HumanEval), showing that closed-form LOO-AUC weighting captures meaningful test-quality signal; ACES-O outperforms ACES-C across all reported benchmark–
k
k
settings.
Further analyses, including finer Pass@
k
k
grids, selection vs. weighting, hyperparameter sensitivity, and computational cost, are in Appendix
C
.
4.3
Analysis
(a)
Assumption
4
satisfaction on MBPP at Pass@1. Bottom: pass rate when
δ
¯
>
0
\bar{\delta}>0
vs.
δ
¯
≤
0
\bar{\delta}\leq 0
.
(b)
Impact of each
δ
j
\delta_{j}
bin on Pass@1 (top) and AUC (bottom). Positive: helpful; negative: harmful.
Figure 2:
Empirical analysis on MBPP at Pass@1.
(a)
Tasks binned by
δ
¯
\bar{\delta}
; bars show pass/fail counts, lines show pass rate; bottom panel compares pass rates by assumption status.
(b)
Performance impact of each
δ
j
\delta_{j}
bin upon removing its tests; full results in Appendix
C.4
.
We restrict this analysis to non-trivial tasks (
0
<
n
+
<
n
0<n^{+}<n
; details in Table
7
) and non-constant tests (
0
<
p
j
<
1
0<p_{j}<1
), since neither trivial tasks nor constant test columns carry ranking signal.
Assumption satisfaction.
Figure
2(a)
empirically validates Assumption
4
on MBPP, which has the most non-trivial tasks and the lowest satisfaction rate among the three benchmarks.
We bin tasks by
δ
¯
\bar{\delta}
and use the simplified threshold
δ
¯
>
0
\bar{\delta}>0
for visual clarity (the formal threshold
2
​
ln
⁡
2
/
m
2\sqrt{\ln 2/m}
is small for
m
≈
500
m\approx 500
; see Appendix
C.4
for the formal analysis).
The assumption is well satisfied on all benchmarks; detailed satisfaction rates are in Table
7
.
The performance gains concentrate in the Middle region, where informative and misleading tests coexist: ACES-O passes 52/89 tasks versus 46/89 for ACES-C and 35/89 for Majority Voting.
In the Easy region, all methods achieve near-perfect pass rates (
≥
97
%
\geq 97\%
), leaving little room for improvement; in the Hard region, no method passes more than 1 of 14 tasks, suggesting the pass matrix alone is insufficient when average test quality is very low and complementary signals such as static analysis may be needed (cf. Section
4.2
).
The bottom panel shows that both ACES variants outperform Majority Voting whether or not the assumption holds; when it fails (
δ
¯
≤
0
\bar{\delta}\leq 0
), ACES-O substantially outperforms ACES-C (16/52 vs. 9/52), showing that iterative optimization is particularly valuable in this regime.
Impact of test quality on performance.
To understand
why
ACES-O outperforms, we measure each
δ
j
\delta_{j}
bin’s impact on performance as the drop incurred by removing its tests (Figure
2(b)
).
The key finding is an asymmetric dependence on test quality.
In the misleading-test region (
δ
j
<
0
\delta_{j}<0
), both ACES variants are more robust: the most misleading bin (
δ
j
≈
−
0.9
\delta_{j}\approx{-}0.9
) reduces Pass@1 by
0.056
0.056
for Majority Voting but by only
0.049
0.049
for ACES-C and
0.030
0.030
for ACES-O (
46
%
46\%
less sensitive).
This is consistent with the ACES weights having already down-weighted misleading tests, so that their presence or absence has little effect on the final ranking.
Conversely, informative tests (
δ
j
>
0
\delta_{j}>0
) contribute more to ACES-O than to Majority Voting (e.g.,
0.030
0.030
vs.
0.012
0.012
at
δ
j
≈
0.3
\delta_{j}\approx 0.3
), because the optimization has up-weighted these high-quality tests.
This asymmetry shows that LOO-AUC-based weighting effectively separates informative from misleading tests in the pass matrix.
Figure 3:
Test quality detection.
ACES-C weight
(
LOO
​
-
​
AUC
j
−
1
2
)
​
p
j
​
(
1
−
p
j
)
(\mathrm{LOO\text{-}AUC}_{j}-\tfrac{1}{2})\,p_{j}(1{-}p_{j})
vs. ground-truth discriminative power
δ
j
\delta_{j}
for all non-trivial tests across three benchmarks.
Green/red points denote informative/misleading tests (
δ
j
>
0
\delta_{j}>0
/
δ
j
<
0
\delta_{j}<0
); top marginals give per-bin TP/FP/FN/TN (saturated: errors; light: correct), and quadrants give TP/FP/FN/TN shares by weight sign (summing to 100%).
Test quality detection.
Figure
3
compares ACES-C weights with ground-truth
δ
j
\delta_{j}
across all benchmarks.
Theorem
3
predicts that
𝔼
⁡
[
LOO
​
-
​
AUC
j
]
−
1
2
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}]-\tfrac{1}{2}
and
δ
j
\delta_{j}
share a sign; accordingly, weight signs identify at least
94.8
%
94.8\%
of informative tests.
The top marginals show FP/FN errors cluster near
δ
j
≈
0
\delta_{j}\approx 0
, where weak discriminative power limits their ranking impact.
MBPP exceeds HumanEval in FP fraction (
17.3
%
17.3\%
vs.
9.5
%
9.5\%
) and misleading-test prevalence (FP
+
{+}
TN:
26.3
%
26.3\%
vs.
18.8
%
18.8\%
); because errors cluster near
δ
j
=
0
\delta_{j}=0
, this gap lies mainly among borderline tests.
5
Related Work
Code selection with generated tests.
Post-hoc selection methods rerank candidates from code LLMs
(
Lozhkov et al., 2024
;
Hui et al., 2024
)
using execution-based signals.
CodeT
(
Chen et al., 2023
)
groups candidates into consensus sets by their binary pass profiles and scores each set by the number of passed tests, operating entirely on the pass matrix.
Several methods exploit execution outputs beyond the pass matrix: MBR-exec
(
Shi et al., 2022
)
applies minimum Bayes risk decoding
(
Eikema & Aziz, 2022
)
via pairwise output comparison, SRank
(
To et al., 2024
)
clusters candidates by output equivalence, and ALGO
(
Zhang et al., 2023a
)
verifies against LLM-synthesized oracle programs.
S
∗
(
Li et al., 2025a
)
uses LLM-guided tournament-style selection with adaptively generated inputs.
Others incorporate non-execution signals: Coder-Reviewer
(
Zhang et al., 2023b
)
uses generation log-probabilities, and LEVER
(
Ni et al., 2023
)
trains a verifier on code and execution features.
MPSC
(
Huang et al., 2024
)
adds specification-level consistency voting, and
𝒟
​
𝒮
3
\mathcal{DS}^{3}
(
Liu et al., 2026
)
augments execution with static analysis.
CURE
(
Wang et al., 2025
)
and CoCoEvo
(
Li et al., 2025b
)
jointly improve code and test generators via reinforcement learning or evolutionary search, at the cost of model training; self-debugging
(
Chen et al., 2024
)
iteratively refines candidates using execution feedback rather than selecting among them.
On the test-quality side, ConVerTest
(
Taherkhani et al., 2026
)
applies self-consistency filtering
(
Wang et al., 2023a
)
before voting, and TestCase-Eval
(
Yang et al., 2025
)
evaluates LLM-generated test reliability; recent systematic studies
(
Li et al., 2024
;
Sun et al., 2024
)
further examine how execution-based strategies compose.
Across these approaches, no formal criterion has been established for identifying test quality from the pass matrix alone; ACES fills this gap with a provable criterion for distinguishing informative from misleading tests using only binary execution outcomes.
Ranking and noisy evaluation.
Code selection via weighted voting is a bipartite ranking problem
(
Clémençon et al., 2008
;
Agarwal et al., 2005
;
Liu, 2010
)
.
Pairwise surrogate consistency
(
Gao & Zhou, 2015
)
justifies our logistic loss.
Recent extensions address partial
(
Wang et al., 2023b
)
, weakly supervised
(
Xie et al., 2024
)
, and multi-label
(
Lukasik et al., 2025
)
AUC optimization; our setting fits naturally into the last framework, where each test acts as a noisy annotator
(
Dawid & Skene, 1979
)
.
Unlike RankBoost
(
Freund et al., 2003
)
, which requires every ranker to beat random, our Assumption
4
requires this only
on average
.
The noisy-comparisons literature provides minimax rates
(
Shah & Wainwright, 2018
)
and noise tolerance results
(
Haddad, 2022
)
, but does not address how to identify reliable comparators.
Nguyen et al. (2024)
show that multiple annotators are necessary for such identification; our LOO-AUC mechanism addresses this without external supervision.
The verifier paradigm
(
Cobbe et al., 2021
;
Lightman et al., 2024
)
and LLM-as-judge evaluation
(
Zheng et al., 2023
)
score candidates via trained or prompted models; ACES requires no additional training.
Our
δ
j
\delta_{j}
mirrors the item discrimination index from classical test theory
(
Lord & Novick, 2008
)
, adapted to noisy, machine-generated tests; the key difference is our self-referential LOO-AUC mechanism, which replaces the external criterion classical theory assumes.
6
Conclusion
We presented ACES (AUC Consistency Scoring), built on the insight that
test votes should rank, not merely count
.
By evaluating tests against each other via leave-one-out AUC, we break the circular dependency between code and test quality assessment without any external supervision.
The LOO-AUC identity (Theorem
3
) establishes that each test’s observable consistency with the ranking is proportional to its latent discriminative power, providing the first provable criterion for distinguishing informative from misleading tests using only the binary pass matrix.
Building on this, ACES-C provides closed-form weights that provably approximate the oracle in expectation, and ACES-O complements it by iteratively optimizing a differentiable LOO-AUC objective without requiring the average-quality assumption.
Both operate solely on the binary pass matrix with negligible overhead, and achieve state-of-the-art Pass@
k
k
among execution-only methods; when combined with complementary static-analysis signals, they yield the best overall results across all benchmarks.
The LOO-AUC framework opens several research directions.
Incorporating correlations among LLM-generated tests could yield tighter bounds and stronger weighting schemes.
More broadly, the principle of assessing evaluator quality via internal consistency extends naturally to other noisy-evaluator settings, including LLM-as-judge ensembles, crowdsourced annotation, and verification with process reward models.
References
Achiam et al. (2023)
Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya,
Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman,
Shyamal Anadkat, et al.
GPT-4 technical report.
Arxiv Preprint Arxiv:2303.08774
, 2023.
Agarwal et al. (2005)
Shivani Agarwal, Thore Graepel, Ralf Herbrich, Sariel Har-Peled, and Dan Roth.
Generalization bounds for the area under the roc curve.
Journal of Machine Learning Research
, 6(14):393–425, 2005.
Austin et al. (2021)
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski,
David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al.
Program synthesis with large language models.
Arxiv Preprint Arxiv:2108.07732
, 2021.
Brown et al. (2024)
Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le,
Christopher Ré, and Azalia Mirhoseini.
Large language monkeys: Scaling inference compute with repeated
sampling.
Arxiv Preprint Arxiv:2407.21787
, 2024.
Chen et al. (2023)
Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and
Weizhu Chen.
CodeT: Code generation with generated tests.
In
The Eleventh International Conference on Learning
Representations
, 2023.
Chen et al. (2021)
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira
Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
Brockman, et al.
Evaluating large language models trained on code.
Arxiv Preprint Arxiv:2107.03374
, 2021.
Chen et al. (2024)
Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou.
Teaching large language models to self-debug.
In
The Twelfth International Conference on Learning
Representations
, 2024.
Clémençon et al. (2008)
Stéphan Clémençon, Gábor Lugosi, and Nicolas Vayatis.
Ranking and empirical minimization of u-statistics.
The Annals of Statistics
, pp.  844–874, 2008.
Cobbe et al. (2021)
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz
Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano,
et al.
Training verifiers to solve math word problems, 2021.
Arxiv Preprint Arxiv:2110.14168
, 2021.
Dawid & Skene (1979)
Alexander Philip Dawid and Allan M Skene.
Maximum likelihood estimation of observer error-rates using the em
algorithm.
Journal of the Royal Statistical Society: Series C (applied
Statistics)
, 28(1):20–28, 1979.
Dong et al. (2024)
Yihong Dong, Xue Jiang, Zhi Jin, and Ge Li.
Self-collaboration code generation via ChatGPT.
Acm Transactions on Software Engineering and Methodology
,
33(7), 2024.
Du et al. (2025)
Yali Du, Hui Sun, and Ming Li.
Post-incorporating code structural knowledge into pretrained models
via icl for code translation.
IEEE Transactions on Software Engineering
, 51(11):3038–3055, 2025.
Eikema & Aziz (2022)
Bryan Eikema and Wilker Aziz.
Sampling-based approximations to minimum Bayes risk decoding for
neural machine translation.
In
Proceedings of the 2022 Conference on Empirical Methods in
Natural Language Processing
, pp.  10978–10993. Association for
Computational Linguistics, 2022.
Freund et al. (2003)
Yoav Freund, Raj Iyer, Robert E Schapire, and Yoram Singer.
An efficient boosting algorithm for combining preferences.
Journal of Machine Learning Research
, 4(Nov):933–969, 2003.
Gao & Zhou (2015)
Wei Gao and Zhi-Hua Zhou.
On the consistency of AUC pairwise optimization.
In
International Joint Conference on Artificial Intelligence
,
pp.  939–945, 2015.
Guo et al. (2024)
Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting
Chen, Xiao Bi, Yifan Wu, YK Li, et al.
DeepSeek-Coder: When the large language model meets
programming–the rise of code intelligence.
Arxiv Preprint Arxiv:2401.14196
, 2024.
Haddad (2022)
Dany Haddad.
Noise tolerance of learning to rank under class-conditional label
noise.
Arxiv Preprint Arxiv:2208.02126
, 2022.
Hoeffding (1963)
Wassily Hoeffding.
Probability inequalities for sums of bounded random variables.
Journal of the American Statistical Association
, 58(301):13–30, 1963.
Huang et al. (2024)
Baizhou Huang, Shuai Lu, Xiaojun Wan, and Nan Duan.
Enhancing large language models in coding through multi-perspective
self-consistency.
In
Proceedings of the 62nd Annual Meeting of the Association
for Computational Linguistics (volume 1: Long Papers)
, pp.  1429–1450.
Association for Computational Linguistics, 2024.
Hui et al. (2024)
Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu
Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al.
Qwen2. 5-Coder technical report.
Arxiv Preprint Arxiv:2409.12186
, 2024.
Li et al. (2025a)
Dacheng Li, Shiyi Cao, Chengkun Cao, Xiuyu Li, Shangyin Tan, Kurt Keutzer,
Jiarong Xing, Joseph E. Gonzalez, and Ion Stoica.
S*: Test time scaling for code generation.
In
Findings of the Association for Computational Linguistics:
Emnlp 2025
, pp.  15964–15978. Association for Computational Linguistics,
2025a.
Li et al. (2024)
Haau-Sing Li, Patrick Fernandes, Iryna Gurevych, and André FT Martins.
DOCE: Finding the sweet spot for execution-based code generation.
Arxiv Preprint Arxiv:2408.13745
, 2024.
Li et al. (2025b)
Kefan Li, Yuan Yuan, Hongyue Yu, Tingyu Guo, and Shijie Cao.
CoCoEvo: Co-evolution of programs and test cases to enhance code
generation.
Ieee Transactions on Evolutionary Computation
, pp.  1–1,
2025b.
Li et al. (2022)
Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser,
Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago,
et al.
Competition-level code generation with alphacode.
Science
, 378(6624):1092–1097, 2022.
Lightman et al. (2024)
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker,
Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
Let’s verify step by step.
In
The Twelfth International Conference on Learning
Representations
, 2024.
Liu et al. (2023)
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and LINGMING ZHANG.
Is your code generated by chatGPT really correct? rigorous
evaluation of large language models for code generation.
In
Thirty-Seventh Conference on Neural Information Processing
Systems
, 2023.
Liu et al. (2025)
Ren-Biao Liu, Anqi Li, Chaoding Yang, Hui Sun, and Ming Li.
Revisiting Chain-of-Thought in code generation: Do language models
need to learn reasoning before coding?
In
Proceedings of the 42nd International Conference on Machine
Learning
, volume 267, pp.  38809–38826. PMLR, 13–19 Jul 2025.
Liu et al. (2026)
Ren-Biao Liu, Jiang-Tian Xue, Chao-Zeng Ma, Hui Sun, Xin-Ye Li, and Ming Li.
Dynamic-Static synergistic selection method for candidate code
solutions with generated test cases.
In
Proceedings of the Aaai Conference on Artificial
Intelligence
, pp.  32096–32104, 2026.
Liu (2010)
Tie-Yan Liu.
Learning to rank for information retrieval.
In
Proceedings of the 33rd International Acm Sigir Conference
on Research and Development in Information Retrieval
, pp.  904. Association
for Computing Machinery, 2010.
Lord & Novick (2008)
Frederic M Lord and Melvin R Novick.
Statistical Theories of Mental Test Scores
.
IAP, 2008.
Lozhkov et al. (2024)
Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel
Lamy-Poirier, Nouamane Tazi, Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang
Wei, et al.
Starcoder 2 and the stack v2: The next generation.
Arxiv Preprint Arxiv:2402.19173
, 2024.
Lukasik et al. (2025)
Michal Lukasik, Lin Chen, Harikrishna Narasimhan, Aditya Krishna Menon,
Wittawat Jitkrittum, Felix X. Yu, Sashank J. Reddi, Gang Fu, Mohammadhossein
Bateni, and Sanjiv Kumar.
Bipartite ranking from multiple labels: On loss versus label
aggregation.
In
Proceedings of the 42nd International Conference on Machine
Learning
, volume 267, pp.  41074–41102. PMLR, 13–19 Jul 2025.
Luo et al. (2024)
Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang
Tao, Jing Ma, Qingwei Lin, and Daxin Jiang.
WizardCoder: Empowering code large language models with
evol-instruct.
In
The Twelfth International Conference on Learning
Representations
, 2024.
Nguyen et al. (2024)
Tri Nguyen, Shahana Ibrahim, and Xiao Fu.
Noisy label learning with instance-dependent outliers:
Identifiability via crowd wisdom.
In
Advances in Neural Information Processing Systems
, 2024.
Ni et al. (2023)
Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-tau Yih, Sida
Wang, and Xi Victoria Lin.
LEVER: Learning to verify language-to-code generation with
execution.
In
Proceedings of the 40th International Conference on Machine
Learning
, pp.  26106–26128. PMLR, 2023.
Roziere et al. (2023)
Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat,
Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez,
et al.
Code llama: Open foundation models for code.
Arxiv Preprint Arxiv:2308.12950
, 2023.
Shah & Wainwright (2018)
Nihar B. Shah and Martin J. Wainwright.
Simple, robust and optimal ranking from pairwise comparisons.
Journal of Machine Learning Research
, 18(199):1–38, 2018.
Shi et al. (2022)
Freda Shi, Daniel Fried, Marjan Ghazvininejad, Luke Zettlemoyer, and Sida I.
Wang.
Natural language to code translation with execution.
In
Proceedings of the 2022 Conference on Empirical Methods in
Natural Language Processing
, pp.  3533–3546. Association for Computational
Linguistics, 2022.
Snell et al. (2025)
Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar.
Scaling LLM test-time compute optimally can be more effective than
scaling parameters for reasoning.
In
The Thirteenth International Conference on Learning
Representations
, 2025.
Sun et al. (2024)
Zhihong Sun, Yao Wan, Jia Li, Hongyu Zhang, Zhi Jin, Ge Li, and Chen Lyu.
Sifting through the chaff: On utilizing execution feedback for
ranking the generated code candidates.
pp.  229–241. Association for Computing Machinery, 2024.
Taherkhani et al. (2026)
Hamed Taherkhani, Alireza DaghighFarsoodeh, Mohammad Chowdhury, Hung Viet Pham,
and Hadi Hemmati.
Consistency meets verification: Enhancing test generation quality in
large language models without ground-truth solutions.
Arxiv Preprint Arxiv:2602.10522
, 2026.
To et al. (2024)
Hung Quoc To, Minh Huynh Nguyen, and Nghi D. Q. Bui.
Functional overlap reranking for neural code generation.
In
Findings of the Association for Computational Linguistics:
Acl 2024
, pp.  3686–3704. Association for Computational Linguistics, 2024.
Wang et al. (2023a)
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang,
Aakanksha Chowdhery, and Denny Zhou.
Self-consistency improves chain of thought reasoning in language
models.
In
The Eleventh International Conference on Learning
Representations
, 2023a.
Wang et al. (2025)
Yinjie Wang, Ling Yang, Ye Tian, Ke Shen, and Mengdi Wang.
CURE: Co-evolving coders and unit testers via reinforcement
learning.
In
The Thirty-Ninth Annual Conference on Neural Information
Processing Systems
, 2025.
Wang et al. (2023b)
Zitai Wang, Qianqian Xu, Zhiyong Yang, Yuan He, Xiaochun Cao, and Qingming
Huang.
Optimizing partial area under the top-k curve: Theory and practice.
Ieee Transactions on Pattern Analysis and Machine
Intelligence
, 45(4):5053–5069, 2023b.
Wu et al. (2025)
Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang.
Inference scaling laws: An empirical analysis of compute-optimal
inference for LLM problem-solving.
In
The Thirteenth International Conference on Learning
Representations
, 2025.
Xia et al. (2025)
Yunhui Xia, Wei Shen, Yan Wang, Jason Klein Liu, Huifeng Sun, Siyue Wu, Jian
Hu, and Xiaolong Xu.
LeetCodeDataset: A temporal dataset for robust evaluation and
efficient training of code LLMs.
arXiv preprint arXiv:2504.14655
, 2025.
Xie et al. (2024)
Zheng Xie, Yu Liu, Hao-Yuan He, Ming Li, and Zhi-Hua Zhou.
Weakly supervised auc optimization: A unified partial auc approach.
Ieee Transactions on Pattern Analysis and Machine
Intelligence
, 46(7):4780–4795, 2024.
Yang et al. (2025)
Zheyuan Yang, Zexi Kuang, Xue Xia, and Yilun Zhao.
Can LLMs generate high-quality test cases for algorithm problems?
TestCase-eval: A systematic evaluation of fault coverage and exposure.
In
Proceedings of the 63rd Annual Meeting of the Association
for Computational Linguistics (volume 2: Short Papers)
, pp.  1050–1063.
Association for Computational Linguistics, 2025.
Zhang et al. (2023a)
Kexun Zhang, Danqing Wang, Jingtao Xia, William Yang Wang, and Lei Li.
ALGO: Synthesizing algorithmic programs with generated oracle
verifiers.
In
Thirty-Seventh Conference on Neural Information Processing
Systems
, 2023a.
Zhang et al. (2023b)
Tianyi Zhang, Tao Yu, Tatsunori Hashimoto, Mike Lewis, Wen-tau Yih, Daniel
Fried, and Sida Wang.
Coder reviewer reranking for code generation.
In
Proceedings of the 40th International Conference on Machine
Learning
, pp.  41832–41846. PMLR, 2023b.
Zheng et al. (2023)
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao
Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, Hao Zhang, Joseph E.
Gonzalez, and Ion Stoica.
Judging LLM-as-a-judge with MT-bench and chatbot arena.
In
Thirty-Seventh Conference on Neural Information Processing
Systems Datasets and Benchmarks Track
, 2023.
Appendix A
Proofs and Theoretical Details
This section provides complete proofs for all theoretical results in the main text: the Pass@
k
k
bound (
A.2
), the LOO-AUC identity (
A.3
), the structure of
c
j
​
(
w
unif
)
c_{j}(w_{\mathrm{unif}})
(
A.4
), and the oracle approximation guarantee (
A.5
).
A.1
Proof Preliminaries
We summarize the notation and model properties used throughout the proofs.
Notation.
Throughout the appendix, we use the following notation from the main text:
•
α
j
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
1
)
\alpha_{j}=P(B_{ij}=1\mid y_{i}=1)
,
β
j
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
0
)
\beta_{j}=P(B_{ij}=1\mid y_{i}=0)
: class-conditional pass rates of test
t
j
t_{j}
.
•
δ
j
=
α
j
−
β
j
\delta_{j}=\alpha_{j}-\beta_{j}
: discriminative power of test
t
j
t_{j}
(Definition
1
).
•
C
+
=
{
c
i
:
y
i
=
1
}
C^{+}=\{c_{i}:y_{i}=1\}
,
C
−
=
{
c
i
:
y
i
=
0
}
C^{-}=\{c_{i}:y_{i}=0\}
: sets of correct and incorrect codes.
•
n
+
=
|
C
+
|
n^{+}=|C^{+}|
,
n
−
=
|
C
−
|
n^{-}=|C^{-}|
,
π
=
n
+
/
n
\pi=n^{+}/n
: counts and fraction of correct codes.
•
p
j
=
P
⁡
(
B
i
​
j
=
1
)
=
π
​
α
j
+
(
1
−
π
)
​
β
j
p_{j}=P(B_{ij}=1)=\pi\alpha_{j}+(1-\pi)\beta_{j}
: marginal pass rate of test
t
j
t_{j}
.
Model properties.
As stated in Section
2.2
, codes are sampled independently from the LLM.
Conditioned on the correctness label
y
i
y_{i}
, each code’s test outcomes are identically distributed and mutually independent across tests, since the class-conditional pass rates
α
j
\alpha_{j}
and
β
j
\beta_{j}
(Definition
1
) depend only on the test and the label, not on the specific code.
It follows that the true AUC
A
⁡
(
w
)
A(w)
is the same for every pair
(
c
+
∈
C
+
,
c
−
∈
C
−
)
(c^{+}\in C^{+},\,c^{-}\in C^{-})
and that two codes from the same class have identically distributed scores.
Hoeffding’s inequality.
Several proofs below rely on the following classical concentration inequality, which we state here for reference.
Lemma 7
(Hoeffding’s inequality
(
Hoeffding, 1963
)
)
.
If
Z
1
,
…
,
Z
m
Z_{1},\ldots,Z_{m}
are independent random variables with
Z
j
∈
[
a
j
,
b
j
]
Z_{j}\in[a_{j},b_{j}]
, then for any
t
>
0
t>0
:
P
⁡
(
∑
j
=
1
m
Z
j
−
𝔼
⁡
[
∑
j
=
1
m
Z
j
]
≤
−
t
)
≤
exp
⁡
(
−
2
​
t
2
∑
j
=
1
m
(
b
j
−
a
j
)
2
)
.
P\!\left(\sum_{j=1}^{m}Z_{j}-\mathbb{E}\!\left[\sum_{j=1}^{m}Z_{j}\right]\leq-t\right)\;\leq\;\exp\!\left(-\frac{2\,t^{2}}{\sum_{j=1}^{m}(b_{j}-a_{j})^{2}}\right).
A.2
Proof of Theorem
2
(Pass@k Bound)
Theorem
(
2
, restated)
.
Define the
mean signal
and
signal-to-noise ratio
of weights
w
w
:
M
⁡
(
w
)
:=
∑
j
w
j
​
δ
j
,
R
⁡
(
w
)
:=
M
​
(
w
)
2
∑
j
w
j
2
.
M(w)\;:=\;\sum_{j}w_{j}\delta_{j},\qquad R(w)\;:=\;\frac{M(w)^{2}}{\sum_{j}w_{j}^{2}}.
For any
w
w
with
M
⁡
(
w
)
>
0
M(w)>0
and any
k
≥
1
k\geq 1
:
Pass@
​
k
​
(
w
)
≥
1
−
n
−
k
​
exp
⁡
(
−
R
⁡
(
w
)
2
)
,
\text{Pass@}k(w)\;\geq\;1-\frac{n^{-}}{k}\,\exp\!\left(-\frac{R(w)}{2}\right),
where
n
−
=
n
−
n
+
n^{-}=n-n^{+}
is the number of incorrect codes.
Proof.
The proof proceeds in two steps: first we reduce
Pass@
​
k
\text{Pass@}k
to a pairwise error probability, then we bound that probability using Hoeffding’s inequality.
Step I: Reducing Pass@
k
k
to pairwise comparisons.
Let
c
∗
=
arg
⁡
max
c
∈
C
+
​
s
c
​
(
w
)
c^{*}=\arg\max_{c\in C^{+}}s_{c}(w)
be the highest-scoring correct code, and define
R
c
∗
=
|
{
c
−
∈
C
−
:
s
c
−
​
(
w
)
≥
s
c
∗
​
(
w
)
}
|
,
R_{c^{*}}\;=\;|\{c^{-}\in C^{-}:s_{c^{-}}(w)\geq s_{c^{*}}(w)\}|,
i.e., the number of incorrect codes that score at least as high as the best correct code.
If Pass@
k
k
fails (no correct code in the top
k
k
), then all
k
k
top-scoring codes are incorrect and each scores
≥
s
c
∗
​
(
w
)
\geq s_{c^{*}}(w)
, so
R
c
∗
≥
k
R_{c^{*}}\geq k
.
We now bound
𝔼
⁡
[
R
c
∗
]
\mathbb{E}[R_{c^{*}}]
.
For any fixed correct code
c
+
c^{+}
(not necessarily
c
∗
c^{*}
) and any incorrect code
c
−
c^{-}
, the event
{
s
c
−
≥
s
c
∗
}
\{s_{c^{-}}\geq s_{c^{*}}\}
implies
{
s
c
−
≥
s
c
+
}
\{s_{c^{-}}\geq s_{c^{+}}\}
(since
c
∗
c^{*}
has the highest score among correct codes).
Therefore:
P
⁡
(
s
c
−
≥
s
c
∗
)
≤
P
⁡
(
s
c
−
≥
s
c
+
)
.
P(s_{c^{-}}\geq s_{c^{*}})\;\leq\;P(s_{c^{-}}\geq s_{c^{+}}).
By exchangeability, the right-hand side is the same for every pair
(
c
+
,
c
−
)
(c^{+},c^{-})
.
Summing over all
n
−
n^{-}
incorrect codes:
𝔼
⁡
[
R
c
∗
]
≤
n
−
⋅
P
⁡
(
s
c
−
≥
s
c
+
)
.
\mathbb{E}[R_{c^{*}}]\;\leq\;n^{-}\cdot P(s_{c^{-}}\geq s_{c^{+}}).
Applying Markov’s inequality:
P
⁡
(
Pass@
​
k
​
fails
)
≤
P
⁡
(
R
c
∗
≥
k
)
≤
n
−
⋅
P
⁡
(
s
c
−
≥
s
c
+
)
k
.
P(\text{Pass@}k\text{ fails})\;\leq\;P(R_{c^{*}}\geq k)\;\leq\;\frac{n^{-}\cdot P(s_{c^{-}}\geq s_{c^{+}})}{k}.
It remains to bound the pairwise error probability
P
⁡
(
s
c
−
≥
s
c
+
)
P(s_{c^{-}}\geq s_{c^{+}})
.
Step II: Bounding pairwise error via Hoeffding’s inequality.
Fix a pair
(
c
+
,
c
−
)
(c^{+},c^{-})
and define the per-test vote
h
j
=
B
c
+
,
j
−
B
c
−
,
j
∈
{
−
1
,
0
,
+
1
}
h_{j}=B_{c^{+},j}-B_{c^{-},j}\in\{-1,0,+1\}
.
Then the score difference is:
X
=
s
c
+
​
(
w
)
−
s
c
−
​
(
w
)
=
∑
j
=
1
m
w
j
​
h
j
.
X\;=\;s_{c^{+}}(w)-s_{c^{-}}(w)\;=\;\sum_{j=1}^{m}w_{j}\,h_{j}.
Since tests are independently sampled, conditioned on
(
y
c
+
,
y
c
−
)
=
(
1
,
0
)
(y_{c^{+}},y_{c^{-}})=(1,0)
, the test outcomes for
c
+
c^{+}
and
c
−
c^{-}
are independent across tests.
This means
{
h
j
}
j
=
1
m
\{h_{j}\}_{j=1}^{m}
are mutually independent random variables with:
𝔼
⁡
[
h
j
]
=
α
j
−
β
j
=
δ
j
,
𝔼
⁡
[
X
]
=
∑
j
w
j
​
δ
j
=
M
⁡
(
w
)
>
0
.
\mathbb{E}[h_{j}]\;=\;\alpha_{j}-\beta_{j}\;=\;\delta_{j},\qquad\mathbb{E}[X]\;=\;\sum_{j}w_{j}\delta_{j}\;=\;M(w)\;>\;0.
Each
w
j
​
h
j
∈
[
−
w
j
,
w
j
]
w_{j}h_{j}\in[-w_{j},w_{j}]
.
Applying Lemma
7
with
Z
j
=
w
j
​
h
j
Z_{j}=w_{j}h_{j}
(so
a
j
=
−
w
j
a_{j}=-w_{j}
,
b
j
=
w
j
b_{j}=w_{j}
,
b
j
−
a
j
=
2
​
w
j
b_{j}-a_{j}=2w_{j}
) and
t
=
M
⁡
(
w
)
t=M(w)
:
P
⁡
(
s
c
−
≥
s
c
+
)
\displaystyle P(s_{c^{-}}\geq s_{c^{+}})
=
P
⁡
(
X
≤
0
)
≤
exp
⁡
(
−
2
​
M
​
(
w
)
2
∑
j
(
2
​
w
j
)
2
)
\displaystyle=P(X\leq 0)\;\leq\;\exp\!\left(-\frac{2\,M(w)^{2}}{\sum_{j}(2w_{j})^{2}}\right)
=
exp
⁡
(
−
M
​
(
w
)
2
2
​
∑
j
w
j
2
)
=
exp
⁡
(
−
R
⁡
(
w
)
2
)
.
\displaystyle=\exp\!\left(-\frac{M(w)^{2}}{2\sum_{j}w_{j}^{2}}\right)\;=\;\exp\!\left(-\frac{R(w)}{2}\right).
Combining.
Substituting the Hoeffding bound into Step I:
P
⁡
(
Pass@
​
k
​
fails
)
≤
n
−
k
​
exp
⁡
(
−
R
⁡
(
w
)
2
)
,
P(\text{Pass@}k\text{ fails})\;\leq\;\frac{n^{-}}{k}\,\exp\!\left(-\frac{R(w)}{2}\right),
and therefore:
Pass@
​
k
​
(
w
)
=
1
−
P
⁡
(
Pass@
​
k
​
fails
)
≥
1
−
n
−
k
​
exp
⁡
(
−
R
⁡
(
w
)
2
)
.
\text{Pass@}k(w)\;=\;1-P(\text{Pass@}k\text{ fails})\;\geq\;1-\frac{n^{-}}{k}\,\exp\!\left(-\frac{R(w)}{2}\right).
Step III: Oracle-optimal weights.
Since
R
⁡
(
w
)
=
M
​
(
w
)
2
/
∑
j
w
j
2
R(w)=M(w)^{2}/\sum_{j}w_{j}^{2}
is scale-invariant, we may normalize
∑
j
w
j
2
=
1
\sum_{j}w_{j}^{2}=1
, so that
R
⁡
(
w
)
=
(
∑
j
w
j
​
δ
j
)
2
R(w)=(\sum_{j}w_{j}\delta_{j})^{2}
.
For
w
j
≥
0
w_{j}\geq 0
, any test with
δ
j
≤
0
\delta_{j}\leq 0
contributes non-positively to
∑
j
w
j
​
δ
j
\sum_{j}w_{j}\delta_{j}
, so the optimum requires
w
j
∗
=
0
w^{*}_{j}=0
for all such tests.
Among the remaining tests (
δ
j
>
0
\delta_{j}>0
), by Cauchy–Schwarz:
∑
j
:
δ
j
>
0
w
j
δ
j
≤
∑
j
:
δ
j
>
0
w
j
2
⋅
∑
j
:
δ
j
>
0
δ
j
2
,
\sum_{j:\,\delta_{j}>0}w_{j}\delta_{j}\;\leq\;\sqrt{\sum_{j:\,\delta_{j}>0}w_{j}^{2}}\;\cdot\;\sqrt{\sum_{j:\,\delta_{j}>0}\delta_{j}^{2}},
with equality iff
w
j
∝
δ
j
w_{j}\propto\delta_{j}
.
Under the normalization
∑
j
w
j
2
=
1
\sum_{j}w_{j}^{2}=1
, this gives
w
j
∗
∝
max
⁡
(
0
,
δ
j
)
w^{*}_{j}\propto\max(0,\;\delta_{j})
and
R
(
w
∗
)
=
∑
j
:
δ
j
>
0
δ
j
2
R(w^{*})=\sum_{j:\delta_{j}>0}\delta_{j}^{2}
.
Since
∑
j
:
δ
j
≤
0
δ
j
≤
0
\sum_{j:\delta_{j}\leq 0}\delta_{j}\leq 0
, we have
∑
j
:
δ
j
>
0
δ
j
≥
m
δ
¯
\sum_{j:\delta_{j}>0}\delta_{j}\geq m\bar{\delta}
, and by Cauchy–Schwarz with
g
=
|
{
j
:
δ
j
>
0
}
|
≤
m
g=|\{j:\delta_{j}>0\}|\leq m
:
R
∗
=
∑
j
:
δ
j
>
0
δ
j
2
≥
(
m
​
δ
¯
)
2
m
=
m
δ
¯
2
=
R
(
w
unif
)
.
∎
R^{*}\;=\;\sum_{j:\,\delta_{j}>0}\delta_{j}^{2}\;\geq\;\frac{(m\bar{\delta})^{2}}{m}\;=\;m\bar{\delta}^{2}\;=\;R(w_{\mathrm{unif}}).\qed
A.3
Proof of Theorem
3
(LOO-AUC Identity)
Theorem
(
3
, restated)
.
For any weights
w
w
:
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
)
]
−
1
2
=
c
j
​
(
w
)
⋅
δ
j
,
c
j
​
(
w
)
:=
π
⁡
(
1
−
π
)
p
j
​
(
1
−
p
j
)
​
(
A
(
−
j
)
​
(
w
)
−
1
2
)
,
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w)]-\frac{1}{2}\;=\;c_{j}(w)\cdot\delta_{j},\qquad c_{j}(w)\;:=\;\frac{\pi(1-\pi)}{p_{j}(1-p_{j})}\left(A^{(-j)}(w)-\frac{1}{2}\right),
where
π
=
n
+
/
n
\pi=n^{+}/n
is the fraction of correct codes and
p
j
=
P
⁡
(
B
i
​
j
=
1
)
p_{j}=P(B_{ij}=1)
is the marginal pass rate of test
j
j
.
Proof.
Setup.
Recall the true AUC of the leave-one-out ranking:
A
(
−
j
)
​
(
w
)
=
P
⁡
(
S
c
+
(
−
j
)
​
(
w
)
>
S
c
−
(
−
j
)
​
(
w
)
)
+
1
2
​
P
​
(
S
c
+
(
−
j
)
​
(
w
)
=
S
c
−
(
−
j
)
​
(
w
)
)
,
A^{(-j)}(w)\;=\;P\bigl(S^{(-j)}_{c^{+}}(w)>S^{(-j)}_{c^{-}}(w)\bigr)\;+\;\frac{1}{2}\,P\bigl(S^{(-j)}_{c^{+}}(w)=S^{(-j)}_{c^{-}}(w)\bigr),
and
LOO
-
AUC
j
(
w
)
=
AUC
(
S
(
−
j
)
,
B
:
,
j
)
\mathrm{LOO\text{-}AUC}_{j}(w)=\AUC(S^{(-j)},B_{:,j})
, where
S
(
−
j
)
S^{(-j)}
are the leave-one-out scores and
B
:
,
j
B_{:,j}
are the pass/fail labels of test
t
j
t_{j}
.
By the probabilistic interpretation of AUC,
LOO
​
-
​
AUC
j
​
(
w
)
\mathrm{LOO\text{-}AUC}_{j}(w)
equals the probability that, for a randomly drawn pair of codes (one from those that pass test
t
j
t_{j}
and one from those that fail it), the passer receives a higher leave-one-out score than the failer (with ties counted as
1
/
2
1/2
).
Formally, let
c
p
c_{\mathrm{p}}
and
c
f
c_{\mathrm{f}}
denote codes drawn uniformly at random from
{
i
:
B
i
​
j
=
1
}
\{i:B_{ij}=1\}
and
{
i
:
B
i
​
j
=
0
}
\{i:B_{ij}=0\}
, respectively.
We emphasize that
c
p
c_{\mathrm{p}}
and
c
f
c_{\mathrm{f}}
are defined by the observed pass/fail outcome on test
t
j
t_{j}
, not by the true labels: unlike
c
+
∈
C
+
c^{+}\in C^{+}
and
c
−
∈
C
−
c^{-}\in C^{-}
(which are truly correct and incorrect), a passer
c
p
c_{\mathrm{p}}
may be incorrect and a failer
c
f
c_{\mathrm{f}}
may be correct.
With this notation:
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
)
]
=
P
⁡
(
S
c
p
(
−
j
)
>
S
c
f
(
−
j
)
)
+
1
2
​
P
​
(
S
c
p
(
−
j
)
=
S
c
f
(
−
j
)
)
.
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w)]\;=\;P\bigl(S^{(-j)}_{c_{\mathrm{p}}}>S^{(-j)}_{c_{\mathrm{f}}}\bigr)\;+\;\frac{1}{2}\,P\bigl(S^{(-j)}_{c_{\mathrm{p}}}=S^{(-j)}_{c_{\mathrm{f}}}\bigr).
Case decomposition.
We condition on the true labels
(
y
c
p
,
y
c
f
)
(y_{c_{\mathrm{p}}},y_{c_{\mathrm{f}}})
.
Let
q
10
q_{10}
,
q
01
q_{01}
, and
q
same
q_{\mathrm{same}}
denote the probabilities that the pair falls into each case (these sum to
1
1
):
y
c
p
y_{c_{\mathrm{p}}}
y
c
f
y_{c_{\mathrm{f}}}
Prob.
Cond. AUC
∗
correct
incorrect
q
10
q_{10}
A
(
−
j
)
​
(
w
)
A^{(-j)}(w)
incorrect
correct
q
01
q_{01}
1
−
A
(
−
j
)
​
(
w
)
1-A^{(-j)}(w)
same class
same class
q
same
q_{\mathrm{same}}
1
/
2
1/2
∗
The last column is the conditional AUC of the leave-one-out ranking for each case:
P
⁡
(
S
c
p
(
−
j
)
>
S
c
f
(
−
j
)
∣
y
c
p
,
y
c
f
)
+
1
2
​
P
​
(
S
c
p
(
−
j
)
=
S
c
f
(
−
j
)
∣
y
c
p
,
y
c
f
)
.
P\bigl(S^{(-j)}_{c_{\mathrm{p}}}>S^{(-j)}_{c_{\mathrm{f}}}\mid y_{c_{\mathrm{p}}},y_{c_{\mathrm{f}}}\bigr)\;+\;\frac{1}{2}\,P\bigl(S^{(-j)}_{c_{\mathrm{p}}}=S^{(-j)}_{c_{\mathrm{f}}}\mid y_{c_{\mathrm{p}}},y_{c_{\mathrm{f}}}\bigr).
In the first row,
c
p
c_{\mathrm{p}}
is correct and
c
f
c_{\mathrm{f}}
is incorrect, so this reduces to
A
(
−
j
)
​
(
w
)
A^{(-j)}(w)
by definition.
In the second row the roles are reversed, giving
1
−
A
(
−
j
)
​
(
w
)
1-A^{(-j)}(w)
.
In the third row, both codes belong to the same class; by exchangeability their leave-one-out scores are identically distributed, so the last column equals
1
/
2
1/2
.
By the law of total probability, and substituting
q
same
=
1
−
q
10
−
q
01
q_{\mathrm{same}}=1-q_{10}-q_{01}
:
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
)
]
\displaystyle\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w)]
=
q
10
​
A
(
−
j
)
+
q
01
​
(
1
−
A
(
−
j
)
)
+
(
1
−
q
10
−
q
01
)
⋅
1
2
\displaystyle=q_{10}\,A^{(-j)}+q_{01}(1-A^{(-j)})+(1-q_{10}-q_{01})\cdot\frac{1}{2}
=
1
2
+
q
10
​
(
A
(
−
j
)
−
1
2
)
−
q
01
​
(
A
(
−
j
)
−
1
2
)
\displaystyle=\frac{1}{2}+q_{10}\!\left(A^{(-j)}-\frac{1}{2}\right)-q_{01}\!\left(A^{(-j)}-\frac{1}{2}\right)
=
1
2
+
(
q
10
−
q
01
)
​
(
A
(
−
j
)
​
(
w
)
−
1
2
)
.
\displaystyle=\frac{1}{2}+(q_{10}-q_{01})\!\left(A^{(-j)}(w)-\frac{1}{2}\right).
Computing
q
10
q_{10}
and
q
01
q_{01}
.
The quantity
q
10
q_{10}
is the probability that
c
p
c_{\mathrm{p}}
is correct and
c
f
c_{\mathrm{f}}
is incorrect.
Recall that
π
=
n
+
/
n
\pi=n^{+}/n
is the fraction of correct codes,
α
j
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
1
)
\alpha_{j}=P(B_{ij}=1\mid y_{i}=1)
and
β
j
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
0
)
\beta_{j}=P(B_{ij}=1\mid y_{i}=0)
are the class-conditional pass rates, and
p
j
=
π
​
α
j
+
(
1
−
π
)
​
β
j
p_{j}=\pi\alpha_{j}+(1-\pi)\beta_{j}
is the marginal pass rate.
By Bayes’ rule, the probability that a code passing test
j
j
is correct is:
P
⁡
(
y
i
=
1
∣
B
i
​
j
=
1
)
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
1
)
​
P
​
(
y
i
=
1
)
P
⁡
(
B
i
​
j
=
1
)
=
π
​
α
j
p
j
,
P(y_{i}=1\mid B_{ij}=1)\;=\;\frac{P(B_{ij}=1\mid y_{i}=1)\,P(y_{i}=1)}{P(B_{ij}=1)}\;=\;\frac{\pi\alpha_{j}}{p_{j}},
and the probability that a code failing test
j
j
is incorrect is:
P
⁡
(
y
i
=
0
∣
B
i
​
j
=
0
)
=
P
⁡
(
B
i
​
j
=
0
∣
y
i
=
0
)
​
P
​
(
y
i
=
0
)
P
⁡
(
B
i
​
j
=
0
)
=
(
1
−
π
)
​
(
1
−
β
j
)
1
−
p
j
.
P(y_{i}=0\mid B_{ij}=0)\;=\;\frac{P(B_{ij}=0\mid y_{i}=0)\,P(y_{i}=0)}{P(B_{ij}=0)}\;=\;\frac{(1-\pi)(1-\beta_{j})}{1-p_{j}}.
Since
c
p
c_{\mathrm{p}}
and
c
f
c_{\mathrm{f}}
are drawn independently,
q
10
q_{10}
is the product of these two probabilities:
q
10
=
π
​
α
j
p
j
⋅
(
1
−
π
)
​
(
1
−
β
j
)
1
−
p
j
.
q_{10}\;=\;\frac{\pi\alpha_{j}}{p_{j}}\cdot\frac{(1-\pi)(1-\beta_{j})}{1-p_{j}}.
For
q
01
q_{01}
(
c
p
c_{\mathrm{p}}
is incorrect,
c
f
c_{\mathrm{f}}
is correct), the probability that a code passing test
j
j
is incorrect is:
P
⁡
(
y
i
=
0
∣
B
i
​
j
=
1
)
=
P
⁡
(
B
i
​
j
=
1
∣
y
i
=
0
)
​
P
​
(
y
i
=
0
)
P
⁡
(
B
i
​
j
=
1
)
=
(
1
−
π
)
​
β
j
p
j
,
P(y_{i}=0\mid B_{ij}=1)\;=\;\frac{P(B_{ij}=1\mid y_{i}=0)\,P(y_{i}=0)}{P(B_{ij}=1)}\;=\;\frac{(1-\pi)\beta_{j}}{p_{j}},
and the probability that a code failing test
j
j
is correct is:
P
⁡
(
y
i
=
1
∣
B
i
​
j
=
0
)
=
P
⁡
(
B
i
​
j
=
0
∣
y
i
=
1
)
​
P
​
(
y
i
=
1
)
P
⁡
(
B
i
​
j
=
0
)
=
π
⁡
(
1
−
α
j
)
1
−
p
j
.
P(y_{i}=1\mid B_{ij}=0)\;=\;\frac{P(B_{ij}=0\mid y_{i}=1)\,P(y_{i}=1)}{P(B_{ij}=0)}\;=\;\frac{\pi(1-\alpha_{j})}{1-p_{j}}.
Therefore:
q
01
=
(
1
−
π
)
​
β
j
p
j
⋅
π
⁡
(
1
−
α
j
)
1
−
p
j
.
q_{01}\;=\;\frac{(1-\pi)\beta_{j}}{p_{j}}\cdot\frac{\pi(1-\alpha_{j})}{1-p_{j}}.
Computing
q
10
−
q
01
q_{10}-q_{01}
.
Factoring out the common terms:
q
10
−
q
01
\displaystyle q_{10}-q_{01}
=
π
⁡
(
1
−
π
)
p
j
​
(
1
−
p
j
)
​
[
α
j
​
(
1
−
β
j
)
−
β
j
​
(
1
−
α
j
)
]
\displaystyle=\frac{\pi(1-\pi)}{p_{j}(1-p_{j})}\bigl[\alpha_{j}(1-\beta_{j})-\beta_{j}(1-\alpha_{j})\bigr]
=
π
⁡
(
1
−
π
)
p
j
​
(
1
−
p
j
)
​
[
α
j
−
β
j
]
=
π
⁡
(
1
−
π
)
​
δ
j
p
j
​
(
1
−
p
j
)
.
\displaystyle=\frac{\pi(1-\pi)}{p_{j}(1-p_{j})}\bigl[\alpha_{j}-\beta_{j}\bigr]\;=\;\frac{\pi(1-\pi)\,\delta_{j}}{p_{j}(1-p_{j})}.
Substituting back into the total probability expression:
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
)
]
−
1
2
=
(
q
10
−
q
01
)
​
(
A
(
−
j
)
​
(
w
)
−
1
2
)
=
π
⁡
(
1
−
π
)
p
j
​
(
1
−
p
j
)
⋅
(
A
(
−
j
)
​
(
w
)
−
1
2
)
⏟
=
c
j
​
(
w
)
⋅
δ
j
.
∎
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w)]-\frac{1}{2}\;=\;(q_{10}-q_{01})\!\left(A^{(-j)}(w)-\frac{1}{2}\right)\;=\;\underbrace{\frac{\pi(1-\pi)}{p_{j}(1-p_{j})}\cdot\left(A^{(-j)}(w)-\frac{1}{2}\right)}_{=\;c_{j}(w)}\cdot\;\delta_{j}.\qed
A.4
Proof of Proposition
5
(Structure of
c
j
​
(
w
unif
)
c_{j}(w_{\mathrm{unif}})
)
Proposition
(
5
, restated)
.
Under Assumption
4
,
A
(
−
j
)
​
(
w
unif
)
>
1
/
2
A^{(-j)}(w_{\mathrm{unif}})>1/2
for all
j
j
, so
c
j
​
(
w
unif
)
>
0
c_{j}(w_{\mathrm{unif}})>0
.
Moreover,
A
(
−
j
)
​
(
w
unif
)
A^{(-j)}(w_{\mathrm{unif}})
is approximately constant across
j
j
.
Proof.
Under uniform weights
w
k
=
1
/
m
w_{k}=1/m
, removing test
j
j
gives
w
k
(
−
j
)
=
1
/
m
w^{(-j)}_{k}=1/m
for
k
≠
j
k\neq j
and
w
j
(
−
j
)
=
0
w^{(-j)}_{j}=0
.
The mean signal and sum of squared weights are:
M
(
−
j
)
=
1
m
​
∑
k
≠
j
δ
k
=
m
​
δ
¯
−
δ
j
m
,
∑
k
(
w
k
(
−
j
)
)
2
=
m
−
1
m
2
.
M^{(-j)}\;=\;\frac{1}{m}\sum_{k\neq j}\delta_{k}\;=\;\frac{m\bar{\delta}-\delta_{j}}{m},\qquad\sum_{k}(w^{(-j)}_{k})^{2}\;=\;\frac{m-1}{m^{2}}.
Therefore:
R
(
−
j
)
​
(
w
unif
)
=
M
(
−
j
)
​
2
∑
k
(
w
k
(
−
j
)
)
2
=
(
m
​
δ
¯
−
δ
j
)
2
m
−
1
.
R^{(-j)}(w_{\mathrm{unif}})\;=\;\frac{M^{(-j)\,2}}{\sum_{k}(w^{(-j)}_{k})^{2}}\;=\;\frac{(m\bar{\delta}-\delta_{j})^{2}}{m{-}1}.
Since
|
δ
j
|
≤
1
|\delta_{j}|\leq 1
(each
δ
j
=
α
j
−
β
j
\delta_{j}=\alpha_{j}-\beta_{j}
is a difference of probabilities) and Assumption
4
implies
m
​
δ
¯
>
2
​
m
​
ln
⁡
2
>
1
m\bar{\delta}>2\sqrt{m\ln 2}>1
, the minimum of
R
(
−
j
)
​
(
w
unif
)
R^{(-j)}(w_{\mathrm{unif}})
over
δ
j
∈
[
−
1
,
1
]
\delta_{j}\in[-1,1]
is attained at
δ
j
=
1
\delta_{j}=1
:
R
(
−
j
)
​
(
w
unif
)
≥
(
m
​
δ
¯
−
1
)
2
m
−
1
.
R^{(-j)}(w_{\mathrm{unif}})\;\geq\;\frac{(m\bar{\delta}-1)^{2}}{m{-}1}.
We claim this lower bound exceeds
2
​
ln
⁡
2
2\ln 2
.
Let
a
=
m
​
δ
¯
a=m\bar{\delta}
.
From Assumption
4
,
m
​
δ
¯
2
>
4
​
ln
⁡
2
m\bar{\delta}^{2}>4\ln 2
, so
m
<
a
2
/
(
4
​
ln
⁡
2
)
m<a^{2}/(4\ln 2)
and
2
​
(
m
−
1
)
​
ln
​
2
=
2
​
m
​
ln
​
2
−
2
​
ln
​
2
<
a
2
/
2
−
2
​
ln
​
2
2(m{-}1)\ln 2=2m\ln 2-2\ln 2<a^{2}/2-2\ln 2
.
Therefore:
(
a
−
1
)
2
−
2
​
(
m
−
1
)
​
ln
⁡
2
>
(
a
−
1
)
2
−
a
2
2
+
2
​
ln
⁡
2
=
(
a
−
2
)
2
2
+
(
2
​
ln
⁡
2
−
1
)
>
0
,
(a-1)^{2}-2(m{-}1)\ln 2\;>\;(a-1)^{2}-\frac{a^{2}}{2}+2\ln 2\;=\;\frac{(a-2)^{2}}{2}+(2\ln 2-1)\;>\;0,
where the last step uses
2
​
ln
⁡
2
>
1
2\ln 2>1
.
Hence
R
(
−
j
)
​
(
w
unif
)
>
2
​
ln
⁡
2
R^{(-j)}(w_{\mathrm{unif}})>2\ln 2
for every
j
j
.
To connect this to the AUC, recall from Section
A.2
that for the score difference
X
=
s
c
+
​
(
w
)
−
s
c
−
​
(
w
)
X=s_{c^{+}}(w)-s_{c^{-}}(w)
, the Hoeffding bound gives
P
(
X
≤
0
)
≤
exp
(
−
R
(
w
)
/
2
)
P(X\leq 0)\leq\exp(-R(w)/2)
.
Since the true AUC satisfies
1
−
A
⁡
(
w
)
=
P
⁡
(
X
<
0
)
+
1
2
​
P
​
(
X
=
0
)
≤
P
⁡
(
X
≤
0
)
,
1-A(w)\;=\;P(X<0)+\frac{1}{2}\,P(X=0)\;\leq\;P(X\leq 0),
we obtain
1
−
A
(
w
)
≤
exp
(
−
R
(
w
)
/
2
)
1-A(w)\leq\exp(-R(w)/2)
for any
w
w
with
M
⁡
(
w
)
>
0
M(w)>0
.
Applying this to the leave-one-out ranking:
1
−
A
(
−
j
)
​
(
w
unif
)
≤
exp
⁡
(
−
R
(
−
j
)
​
(
w
unif
)
2
)
<
exp
⁡
(
−
ln
⁡
2
)
=
1
2
.
1-A^{(-j)}(w_{\mathrm{unif}})\;\leq\;\exp\!\left(-\frac{R^{(-j)}(w_{\mathrm{unif}})}{2}\right)\;<\;\exp(-\ln 2)\;=\;\frac{1}{2}.
Therefore
A
(
−
j
)
​
(
w
unif
)
>
1
/
2
A^{(-j)}(w_{\mathrm{unif}})>1/2
for every
j
j
, which gives
c
j
​
(
w
unif
)
>
0
c_{j}(w_{\mathrm{unif}})>0
.
Approximate constancy of
A
(
−
j
)
A^{(-j)}
.
The bound above gives
1
−
A
(
−
j
)
​
(
w
unif
)
≤
exp
⁡
(
−
(
m
​
δ
¯
−
1
)
2
2
​
(
m
−
1
)
)
1-A^{(-j)}(w_{\mathrm{unif}})\;\leq\;\exp\!\left(-\frac{(m\bar{\delta}-1)^{2}}{2(m{-}1)}\right)
for every
j
j
.
Since all
A
(
−
j
)
​
(
w
unif
)
∈
(
1
/
2
,
1
]
A^{(-j)}(w_{\mathrm{unif}})\in(1/2,\,1]
, for any
a
≥
b
>
1
/
2
a\geq b>1/2
we have
a
−
b
≤
1
−
b
=
max
⁡
(
1
−
a
,
1
−
b
)
a-b\leq 1-b=\max(1-a,\,1-b)
, so
|
A
(
−
j
)
−
A
(
−
k
)
|
≤
max
⁡
(
1
−
A
(
−
j
)
,
1
−
A
(
−
k
)
)
≤
exp
⁡
(
−
(
m
​
δ
¯
−
1
)
2
2
​
(
m
−
1
)
)
.
\left|A^{(-j)}-A^{(-k)}\right|\;\leq\;\max\!\left(1-A^{(-j)},\;1-A^{(-k)}\right)\;\leq\;\exp\!\left(-\frac{(m\bar{\delta}-1)^{2}}{2(m{-}1)}\right).
The same reasoning applies to
A
⁡
(
w
unif
)
A(w_{\mathrm{unif}})
, since
R
⁡
(
w
unif
)
=
m
​
δ
¯
2
>
4
​
ln
⁡
2
R(w_{\mathrm{unif}})=m\bar{\delta}^{2}>4\ln 2
gives
1
−
A
(
w
unif
)
≤
exp
(
−
m
δ
¯
2
/
2
)
1-A(w_{\mathrm{unif}})\leq\exp(-m\bar{\delta}^{2}/2)
, which is also exponentially small.
Therefore all values
A
(
−
j
)
​
(
w
unif
)
A^{(-j)}(w_{\mathrm{unif}})
and
A
⁡
(
w
unif
)
A(w_{\mathrm{unif}})
are exponentially close to each other, and
A
(
−
j
)
​
(
w
unif
)
−
1
/
2
A^{(-j)}(w_{\mathrm{unif}})-1/2
is approximately constant across
j
j
.
∎
A.5
Oracle Approximation Guarantee
Corollary 8
.
Under Assumption
4
, let
a
j
=
A
(
−
j
)
​
(
w
unif
)
−
1
/
2
a_{j}=A^{(-j)}(w_{\mathrm{unif}})-1/2
and
ρ
=
a
min
/
a
max
\rho=a_{\min}/a_{\max}
.
Define the
population ACES-C weights
w
¯
j
:=
max
⁡
(
0
,
𝔼
⁡
[
q
j
]
)
\bar{w}_{j}:=\max(0,\,\mathbb{E}[q_{j}])
, where
q
j
q_{j}
is the quality score from Theorem
6
. Since
a
j
>
0
a_{j}>0
, this gives
w
¯
j
=
π
⁡
(
1
−
π
)
​
a
j
​
max
⁡
(
0
,
δ
j
)
\bar{w}_{j}=\pi(1{-}\pi)\,a_{j}\,\max(0,\,\delta_{j})
. Then:
R
⁡
(
w
¯
)
≥
ρ
2
​
R
∗
,
ρ
≥
1
−
2
​
exp
⁡
(
−
(
m
​
δ
¯
−
1
)
2
2
​
(
m
−
1
)
)
,
R(\bar{w})\;\geq\;\rho^{2}\,R^{*},\qquad\rho\;\geq\;1-2\exp\!\left(-\frac{(m\bar{\delta}-1)^{2}}{2(m{-}1)}\right),
where
R
∗
=
∑
j
:
δ
j
>
0
δ
j
2
R^{*}=\sum_{j:\,\delta_{j}>0}\delta_{j}^{2}
is the oracle signal-to-noise ratio (Theorem
2
).
Since
ρ
→
1
\rho\to 1
as
m
m
grows, the population weights achieve near-oracle performance.
Proof.
By definition and Theorem
6
:
w
¯
j
=
π
⁡
(
1
−
π
)
​
a
j
​
max
⁡
(
0
,
δ
j
)
,
\bar{w}_{j}\;=\;\pi(1{-}\pi)\,a_{j}\max(0,\;\delta_{j}),
where
a
j
>
0
a_{j}>0
by Proposition
5
.
Only tests with
δ
j
>
0
\delta_{j}>0
receive positive population weight, so:
M
(
w
¯
)
=
∑
j
:
δ
j
>
0
a
j
δ
j
2
⋅
π
(
1
−
π
)
,
∑
j
w
¯
j
2
=
∑
j
:
δ
j
>
0
a
j
2
δ
j
2
⋅
π
2
(
1
−
π
)
2
.
M(\bar{w})\;=\;\sum_{j:\,\delta_{j}>0}a_{j}\,\delta_{j}^{2}\cdot\pi(1{-}\pi),\qquad\sum_{j}\bar{w}_{j}^{2}\;=\;\sum_{j:\,\delta_{j}>0}a_{j}^{2}\,\delta_{j}^{2}\cdot\pi^{2}(1{-}\pi)^{2}.
Since
R
R
is scale-invariant,
π
⁡
(
1
−
π
)
\pi(1{-}\pi)
cancels:
R
(
w
¯
)
=
(
∑
j
:
δ
j
>
0
a
j
δ
j
2
)
2
∑
j
:
δ
j
>
0
a
j
2
δ
j
2
≥
a
min
2
(
∑
j
:
δ
j
>
0
δ
j
2
)
2
a
max
2
∑
j
:
δ
j
>
0
δ
j
2
=
ρ
2
R
∗
.
R(\bar{w})\;=\;\frac{\bigl(\sum_{j:\delta_{j}>0}a_{j}\,\delta_{j}^{2}\bigr)^{2}}{\sum_{j:\delta_{j}>0}a_{j}^{2}\,\delta_{j}^{2}}\;\geq\;\frac{a_{\min}^{2}\,\bigl(\sum_{j:\delta_{j}>0}\delta_{j}^{2}\bigr)^{2}}{a_{\max}^{2}\,\sum_{j:\delta_{j}>0}\delta_{j}^{2}}\;=\;\rho^{2}\,R^{*}.
For the bound on
ρ
\rho
: by Appendix
A.4
,
1
−
A
(
−
j
)
≤
exp
⁡
(
−
(
m
​
δ
¯
−
1
)
2
2
​
(
m
−
1
)
)
for all
​
j
.
1-A^{(-j)}\;\leq\;\exp\!\left(-\frac{(m\bar{\delta}-1)^{2}}{2(m{-}1)}\right)\quad\text{for all }j.
Since
a
max
≤
1
/
2
a_{\max}\leq 1/2
(because
A
(
−
j
)
≤
1
A^{(-j)}\leq 1
) and
a
min
≥
1
/
2
−
exp
(
−
(
m
δ
¯
−
1
)
2
/
[
2
(
m
−
1
)
]
)
a_{\min}\geq 1/2-\exp\!\bigl(-(m\bar{\delta}-1)^{2}/[2(m{-}1)]\bigr)
:
ρ
=
a
min
a
max
≥
1
/
2
−
exp
(
−
(
m
δ
¯
−
1
)
2
/
[
2
(
m
−
1
)
]
)
1
/
2
=
1
−
2
​
exp
⁡
(
−
(
m
​
δ
¯
−
1
)
2
2
​
(
m
−
1
)
)
.
∎
\rho\;=\;\frac{a_{\min}}{a_{\max}}\;\geq\;\frac{1/2-\exp\!\bigl(-(m\bar{\delta}-1)^{2}/[2(m{-}1)]\bigr)}{1/2}\;=\;1-2\exp\!\left(-\frac{(m\bar{\delta}-1)^{2}}{2(m{-}1)}\right).\qed
Appendix B
Algorithm Details
This section provides pseudocode for both ACES variants, implementation details, and the combination procedure with
𝒟
​
𝒮
3
\mathcal{DS}^{3}
referenced in Section
4
.
B.1
ACES-C
Algorithm
1
implements ACES-C (Section
3.1
).
Under uniform initial weights, the leave-one-out scores reduce to unweighted row sums with one column removed; since the AUC is scale-invariant, normalization is unnecessary.
The algorithm has no tunable parameters: it computes the LOO-AUC for each test, applies the pass-rate correction (Eq.
8
), and returns the weighted scores in a single pass.
Algorithm 1
ACES-C (Closed-Form Weighting)
0:
Pass matrix
B
∈
{
0
,
1
}
n
×
m
B\in\{0,1\}^{n\times m}
0:
Code scores
s
1
,
…
,
s
n
s_{1},\ldots,s_{n}
1:
for
j
=
1
j=1
to
m
m
do
2:
Compute
S
i
(
−
j
)
=
∑
j
′
≠
j
B
i
​
j
′
S^{(-j)}_{i}=\sum_{j^{\prime}\neq j}B_{ij^{\prime}}
for all
i
i
{LOO scores;
∝
\propto
Eq. (
6
) under
w
unif
w_{\mathrm{unif}}
}
3:
Compute
LOO
-
AUC
j
(
w
unif
)
=
AUC
(
S
(
−
j
)
,
B
:
,
j
)
\mathrm{LOO\text{-}AUC}_{j}(w_{\mathrm{unif}})=\AUC(S^{(-j)},B_{:,j})
{AUC is scale-invariant}
4:
end
for
5:
p
j
←
1
n
​
∑
i
B
i
​
j
p_{j}\leftarrow\frac{1}{n}\sum_{i}B_{ij}
for all
j
j
{empirical pass rate}
6:
Set
w
j
←
max
⁡
(
0
,
LOO
​
-
​
AUC
j
​
(
w
unif
)
−
1
/
2
)
⋅
p
j
​
(
1
−
p
j
)
w_{j}\leftarrow\max(0,\;\mathrm{LOO\text{-}AUC}_{j}(w_{\mathrm{unif}})-1/2)\cdot p_{j}(1-p_{j})
for all
j
j
{Eq. (
8
)}
7:
return
s
i
=
∑
j
w
j
​
B
i
​
j
s_{i}=\sum_{j}w_{j}B_{ij}
for all
i
i
B.2
ACES-O
Algorithm
2
implements ACES-O (Section
3.2
), which maximizes the objective
J
⁡
(
w
)
=
∑
j
w
j
​
(
LOO
​
-
​
AUC
j
​
(
w
)
−
1
/
2
)
J(w)=\sum_{j}w_{j}\,(\mathrm{LOO\text{-}AUC}_{j}(w)-1/2)
via gradient ascent.
Since the exact LOO-AUC involves indicator functions and is therefore non-differentiable, we replace it with a logistic surrogate.
For each test
t
j
t_{j}
, let
𝒫
j
=
{
i
:
B
i
​
j
=
1
}
\mathcal{P}_{j}=\{i:B_{ij}=1\}
and
𝒩
j
=
{
i
:
B
i
​
j
=
0
}
\mathcal{N}_{j}=\{i:B_{ij}=0\}
denote the sets of codes that pass and fail
t
j
t_{j}
, respectively.
The surrogate LOO-AUC is:
LOO
​
-
​
AUC
^
j
​
(
w
)
=
1
|
𝒫
j
|
​
|
𝒩
j
|
​
∑
i
∈
𝒫
j
∑
k
∈
𝒩
j
σ
⁡
(
γ
⁡
(
S
i
(
−
j
)
​
(
w
)
−
S
k
(
−
j
)
​
(
w
)
)
)
,
\widehat{\mathrm{LOO\text{-}AUC}}_{j}(w)\;=\;\frac{1}{|\mathcal{P}_{j}|\,|\mathcal{N}_{j}|}\sum_{i\in\mathcal{P}_{j}}\sum_{k\in\mathcal{N}_{j}}\sigma\!\left(\gamma\bigl(S^{(-j)}_{i}(w)-S^{(-j)}_{k}(w)\bigr)\right),
(11)
where
σ
⁡
(
x
)
=
1
/
(
1
+
e
−
x
)
\sigma(x)=1/(1+e^{-x})
is the logistic function and
γ
>
0
\gamma>0
is a sharpness parameter controlling the surrogate tightness.
As
γ
→
∞
\gamma\to\infty
,
σ
⁡
(
γ
​
x
)
\sigma(\gamma x)
approaches the step function and the surrogate recovers the exact LOO-AUC.
This surrogate is smooth and statistically consistent
(
Gao & Zhou, 2015
)
, enabling gradient computation via automatic differentiation.
The weights are parameterized as
w
=
softmax
⁡
(
ℓ
)
w=\mathrm{softmax}(\ell)
with learnable logits
ℓ
∈
ℝ
m
\ell\in\mathbb{R}^{m}
; this ensures
w
∈
Δ
m
w\in\Delta^{m}
throughout optimization.
Algorithm 2
ACES-O (Optimized Weighting)
0:
Pass matrix
B
∈
{
0
,
1
}
n
×
m
B\in\{0,1\}^{n\times m}
, sharpness
γ
\gamma
, learning rate
η
\eta
, steps
T
T
0:
Code scores
s
1
,
…
,
s
n
s_{1},\ldots,s_{n}
1:
Initialize logits
ℓ
←
𝟎
∈
ℝ
m
\ell\leftarrow\mathbf{0}\in\mathbb{R}^{m}
2:
for
t
=
1
t=1
to
T
T
do
3:
w
←
softmax
⁡
(
ℓ
)
w\leftarrow\mathrm{softmax}(\ell)
4:
for
j
=
1
j=1
to
m
m
do
5:
S
i
(
−
j
)
​
(
w
)
←
∑
j
′
≠
j
w
j
′
​
B
i
​
j
′
S^{(-j)}_{i}(w)\leftarrow\sum_{j^{\prime}\neq j}w_{j^{\prime}}B_{ij^{\prime}}
for all
i
i
{leave-one-out scores}
6:
Compute
LOO
​
-
​
AUC
^
j
​
(
w
)
\widehat{\mathrm{LOO\text{-}AUC}}_{j}(w)
via logistic surrogate (Eq.
11
)
7:
end
for
8:
ℓ
←
ℓ
+
η
​
∇
ℓ
​
∑
j
w
j
​
LOO
​
-
​
AUC
^
j
​
(
w
)
\ell\leftarrow\ell+\eta\,\nabla_{\ell}\sum_{j}w_{j}\,\widehat{\mathrm{LOO\text{-}AUC}}_{j}(w)
{gradient ascent (Adam in practice)}
9:
end
for
10:
w
←
softmax
⁡
(
ℓ
)
w\leftarrow\mathrm{softmax}(\ell)
11:
return
s
i
=
∑
j
w
j
​
B
i
​
j
s_{i}=\sum_{j}w_{j}B_{ij}
for all
i
i
The surrogate objective is non-convex because
LOO
​
-
​
AUC
^
j
​
(
w
)
\widehat{\mathrm{LOO\text{-}AUC}}_{j}(w)
depends on
w
w
through the leave-one-out scores, so gradient ascent converges to a stationary point rather than a global maximum.
Initializing from
w
unif
w_{\mathrm{unif}}
(i.e.,
ℓ
=
𝟎
\ell=\mathbf{0}
) provides a favorable starting point, since Proposition
5
guarantees
A
(
−
j
)
​
(
w
unif
)
>
1
/
2
A^{(-j)}(w_{\mathrm{unif}})>1/2
for all
j
j
under Assumption
4
: informative tests are up-weighted in early iterates, improving the ranking and further separating informative from misleading tests in subsequent gradient steps.
Across all benchmarks, we observe stable convergence with no restarts required.
B.3
Implementation Details
For ACES-O, we adopt a two-stage pipeline: first pre-filter to the top-
K
K
candidates by majority vote, then optimize weights on this shortlist.
Pre-filtering removes obviously low-quality candidates and reduces the per-step cost from
O
⁡
(
n
​
m
2
)
O(nm^{2})
to
O
⁡
(
K
​
m
2
)
O(Km^{2})
.
ACES-C requires no pre-filtering and runs on all
n
n
candidates directly.
ACES-O uses Adam with surrogate sharpness
γ
=
10
\gamma{=}10
, learning rate
η
=
0.01
\eta{=}0.01
, and
T
=
90
T{=}90
steps on HumanEval (
η
=
0.05
\eta{=}0.05
,
T
=
90
T{=}90
on HumanEval
+
and MBPP), with top-
K
=
24
K{=}24
pre-filtering (
K
=
32
K{=}32
on MBPP).
B.4
Combination with
𝒟
​
𝒮
3
\mathcal{DS}^{3}
As described in Section
4.2
, we combine ACES with
𝒟
​
𝒮
3
\mathcal{DS}^{3}
(
Liu et al., 2026
)
.
We first summarize
𝒟
​
𝒮
3
\mathcal{DS}^{3}
’s scoring mechanism, then describe the combined formulation.
𝒟
​
𝒮
3
\mathcal{DS}^{3}
scoring.
𝒟
​
𝒮
3
\mathcal{DS}^{3}
first applies a
pre-filtering
stage that sanitizes candidate code (AST-based extraction of the longest valid code block followed by dependency-driven dead-code elimination) and validates test inputs (AST-based argument extraction with signature-conformance checking).
This removes malformed candidates and invalid tests, reducing the sets from
n
n
to
n
′
≤
n
n^{\prime}\leq n
and from
m
m
to
m
′
≤
m
m^{\prime}\leq m
.
On the filtered set,
𝒟
​
𝒮
3
\mathcal{DS}^{3}
computes two signals.
A
static quality vector
𝐪
∈
[
0
,
1
]
n
′
\mathbf{q}\in[0,1]^{n^{\prime}}
scores each candidate by combining a normalized Pylint score (code quality) with a normalized cyclomatic-complexity score (lower complexity yields a higher score).
A
pairwise consensus matrix
P
∈
[
0
,
1
]
n
′
×
n
′
P\in[0,1]^{n^{\prime}\times n^{\prime}}
captures behavioral similarity:
P
i
​
k
=
1
m
′
∑
j
=
1
m
′
[
exec
(
c
i
,
t
j
)
=
exec
(
c
k
,
t
j
)
]
,
P_{ik}\;=\;\frac{1}{m^{\prime}}\sum_{j=1}^{m^{\prime}}\mathbf{1}\!\bigl[\operatorname{exec}(c_{i},t_{j})=\operatorname{exec}(c_{k},t_{j})\bigr],
where
exec
⁡
(
c
i
,
t
j
)
\operatorname{exec}(c_{i},t_{j})
denotes the full output of candidate
c
i
c_{i}
on test
t
j
t_{j}
.
The final
𝒟
​
𝒮
3
\mathcal{DS}^{3}
score is
𝐪
∗
=
P
⋅
𝐪
\mathbf{q}_{*}=P\cdot\mathbf{q}
: each candidate receives a consensus-weighted sum of static quality across all candidates, favoring solutions that are both well-structured and behaviorally consistent.
Combined formulation.
ACES and
𝒟
​
𝒮
3
\mathcal{DS}^{3}
capture complementary signals: ACES computes adaptive test weights from the pass matrix to produce per-candidate scores
s
i
​
(
w
)
=
∑
j
w
j
​
B
i
​
j
s_{i}(w)=\sum_{j}w_{j}B_{ij}
, while
𝒟
​
𝒮
3
\mathcal{DS}^{3}
combines static code quality with pairwise output consensus.
We reuse
𝒟
​
𝒮
3
\mathcal{DS}^{3}
’s pre-filtering to obtain a cleaned candidate set of size
n
′
n^{\prime}
, then combine both signals on the filtered candidates via
𝐫
=
(
α
​
I
n
′
+
(
1
−
α
)
​
P
)
⋅
(
β
​
𝐬
​
(
w
)
+
(
1
−
β
)
​
𝐪
)
,
\mathbf{r}\;=\;\bigl(\alpha\,I_{n^{\prime}}+(1-\alpha)\,P\bigr)\cdot\bigl(\beta\,\mathbf{s}(w)+(1-\beta)\,\mathbf{q}\bigr),
(12)
where
I
n
′
I_{n^{\prime}}
is the identity matrix and
α
,
β
∈
[
0
,
1
]
\alpha,\beta\in[0,1]
.
The coefficient
β
\beta
blends the per-candidate scoring signal: ACES scores
𝐬
⁡
(
w
)
\mathbf{s}(w)
at
β
=
1
\beta=1
and static quality
𝐪
\mathbf{q}
at
β
=
0
\beta=0
.
The coefficient
α
\alpha
controls the aggregation:
α
=
1
\alpha=1
scores each candidate independently, while
α
=
0
\alpha=0
applies pairwise consensus weighting as in
𝒟
​
𝒮
3
\mathcal{DS}^{3}
.
Setting
α
=
β
=
0
\alpha=\beta=0
recovers the original
𝒟
​
𝒮
3
\mathcal{DS}^{3}
score
P
⋅
𝐪
P\cdot\mathbf{q}
.
Both
𝐬
⁡
(
w
)
\mathbf{s}(w)
and
𝐪
\mathbf{q}
lie in
[
0
,
1
]
n
′
[0,1]^{n^{\prime}}
by construction, so no additional normalization is required.
All
𝒟
​
𝒮
3
\mathcal{DS}^{3}
components (pre-filtering, static scoring, pairwise consensus matrix, and all associated hyperparameters) use the official implementation and default settings of
Liu et al. (2026)
.
Appendix C
Additional Experimental Results
This section provides supplementary experiments: an illustrative walkthrough (
C.1
), additional models and benchmarks (
C.2
), extended Pass@
k
k
curves (
C.3
), assumption verification (
C.4
), selection vs. weighting analysis (
C.5
), sensitivity analyses (
C.6
–
C.8
), convergence (
C.9
), hyperparameter sensitivity (
C.10
), runtime (
C.11
), vote statistics (
C.12
), and generation prompts (
C.13
).
C.1
Illustrative Example
To illustrate how the strength of Assumption
4
affects the two ACES variants, we construct two
8
×
10
8\times 10
instances, each with three correct codes, five incorrect codes, and ten tests ordered by
δ
j
\delta_{j}
.
The
Easy
case (
δ
¯
=
0.16
\bar{\delta}=0.16
) represents a favorable regime, whereas the
Hard
case (
δ
¯
=
0.04
\bar{\delta}=0.04
) contains more strongly misleading tests.
Figure
4
summarizes their pass matrices, inferred test weights, and resulting rankings; Tables
3
and
4
report the complete numerical data.
Figure 4:
ACES on two constructed
8
×
10
8\times 10
instances (Easy: top; Hard: bottom).
Test colors: green = perfect, blue = constructive/permissive, red = misleading.
(a) Pass matrix. (b),(c)
LOO
​
-
​
AUC
j
\mathrm{LOO\text{-}AUC}_{j}
(upper) and weights
w
j
w_{j}
(lower, purple). (d) Scores; gold/silver/bronze mark the top-3 codes.
Together, the two cases isolate the transition from a favorable regime, where ACES-C’s closed-form correction is sufficient, to a difficult regime, where ACES-O’s iterative refinement becomes important.
We now trace each case in the same sequence: MV
→
\to
ACES-C
→
\to
ACES-O.
Easy case
(Table
3
).
Eight of ten tests are informative (
δ
j
>
0
\delta_{j}>0
) and only two are misleading, so the signal-to-noise ratio is favorable.
MV
assigns uniform weight to all tests and achieves AUC
=
0.90
=0.90
; however, the lowest correct code
c
3
c_{3}
ties with three incorrect ones at vote
=
4
=4
, making the top-1 selection unreliable.
ACES-C
computes LOO-AUC under uniform weights and finds that 6 of the 8 informative tests have
LOO
​
-
​
AUC
j
>
1
/
2
\mathrm{LOO\text{-}AUC}_{j}>1/2
; it assigns non-zero weight to these 6 via Eq. (
8
), concentrating weight on the most discriminative tests (
t
1
t_{1}
,
t
2
t_{2}
,
t
4
t_{4}
each receive
w
=
0.25
w=0.25
).
This breaks the MV tie and achieves AUC
=
1.00
=1.00
: all three correct codes now rank above all five incorrect ones.
ACES-O
also reaches AUC
=
1.00
=1.00
, further concentrating weight on the single strongest test (
t
1
t_{1}
,
w
=
0.40
w=0.40
).
When test quality is high, the closed-form ACES-C already suffices for perfect separation.
Table 3:
Easy case:
8
×
10
8\times 10
pass matrix with 8 informative and 2 misleading tests (
δ
¯
=
0.16
\bar{\delta}=0.16
).
Tests are sorted by
δ
j
\delta_{j}
descending. MV AUC:
0.90
0.90
; ACES-C AUC:
1.00
1.00
; ACES-O AUC:
1.00
1.00
.
correct
(
α
j
=
1
\alpha_{j}\!=\!1
)
incorrect
(
α
j
<
1
\alpha_{j}\!<\!1
)
perf.
constructive
(
0
<
δ
j
<
1
0<\delta_{j}<1
)
misleading
(
δ
j
<
0
\delta_{j}<0
)
t
1
t_{1}
t
2
t_{2}
t
3
t_{3}
t
4
t_{4}
t
5
t_{5}
t
7
t_{7}
t
6
t_{6}
t
8
t_{8}
t
9
t_{9}
t
10
t_{10}
MV
-C
-O
✓
​
c
1
\checkmark\,c_{1}
1
1
1
1
1
0
1
0
0
0
.60
1.00
1.00
✓
​
c
2
\checkmark\,c_{2}
1
1
0
1
0
1
0
1
0
0
.50
.75
.69
✓
​
c
3
\checkmark\,c_{3}
1
0
1
0
1
1
0
0
0
0
.40
.35
.71
×
c
4
\times\,c_{4}
0
1
1
0
0
0
0
0
1
1
.40
.30
.30
×
c
5
\times\,c_{5}
0
0
0
1
1
0
0
0
1
1
.40
.30
.30
×
c
6
\times\,c_{6}
0
0
0
0
0
1
1
0
1
1
.40
.15
.01
×
c
7
\times\,c_{7}
0
0
0
0
0
0
0
1
1
1
.30
.00
.00
×
c
8
\times\,c_{8}
0
0
0
0
0
0
0
0
1
1
.20
.00
.00
α
j
\alpha_{j}
1.00
.67
.67
.67
.67
.67
.33
.33
.00
.00
β
j
\beta_{j}
.00
.20
.20
.20
.20
.20
.20
.20
1.00
1.00
δ
j
\delta_{j}
+
1.0
+1.0
+
.47
+.47
+
.47
+.47
+
.47
+.47
+
.47
+.47
+
.47
+.47
+
.13
+.13
+
.13
+.13
−
1.0
-1.0
−
1.0
-1.0
LOO
C
{}_{\text{C}}
.67
.67
.53
.67
.53
.40
.63
.33
.00
.00
w
j
C
w_{j}^{\text{C}}
.25
.25
.05
.25
.05
.00
.15
.00
.00
.00
LOO
O
{}_{\text{O}}
.87
.80
.80
.80
.80
.67
.58
.42
.00
.00
w
j
O
w_{j}^{\text{O}}
.40
.14
.15
.14
.15
.00
.00
.00
.00
.00
Hard case
(Table
4
).
By contrast, six tests are informative and four are misleading, with all four misleading tests having strong discriminative power in the wrong direction (
|
δ
j
|
≥
0.67
|\delta_{j}|\geq 0.67
).
MV
achieves only AUC
=
0.60
=0.60
: the incorrect code
c
4
c_{4}
receives vote
=
6
=6
, tying the best correct code
c
1
c_{1}
.
ACES-C
faces a challenge: the strong misleading tests corrupt the uniform-weight ranking, causing only 2 of 6 informative tests (
t
4
t_{4}
and
t
5
t_{5}
) to have
LOO
​
-
​
AUC
j
>
1
/
2
\mathrm{LOO\text{-}AUC}_{j}>1/2
.
Since ACES-C computes weights in closed form from these initial estimates, it can only assign weight to these two tests.
This improves AUC to
0.77
0.77
, but the incorrect
c
4
c_{4}
remains ranked third.
ACES-O
overcomes this limitation through iterative co-evolution: improved weights produce a better ranking, which raises the LOO-AUC of initially misidentified tests, enabling further weight refinement.
At convergence, all six informative tests have
LOO
​
-
​
AUC
j
>
1
/
2
\mathrm{LOO\text{-}AUC}_{j}>1/2
, and ACES-O concentrates weight on the three strongest (
t
1
t_{1}
,
t
3
t_{3}
,
t
2
t_{2}
), achieving AUC
=
1.00
=1.00
.
This demonstrates the value of iterative optimization when misleading tests are prevalent.
Table 4:
Hard case:
8
×
10
8\times 10
pass matrix with 6 informative and 4 misleading tests (
δ
¯
=
0.04
\bar{\delta}=0.04
).
Under uniform weights, only 2/6 informative tests have
LOO
​
-
​
AUC
j
>
1
/
2
\mathrm{LOO\text{-}AUC}_{j}>1/2
; ACES-O’s co-evolution recovers all 6.
MV AUC:
0.60
0.60
; ACES-C AUC:
0.77
0.77
; ACES-O AUC:
1.00
1.00
.
correct
(
α
j
=
1
\alpha_{j}\!=\!1
)
incorrect
(
α
j
<
1
\alpha_{j}\!<\!1
)
perf.
perm.
constructive
misleading
(
δ
j
<
0
\delta_{j}<0
)
t
1
t_{1}
t
2
t_{2}
t
3
t_{3}
t
4
t_{4}
t
5
t_{5}
t
6
t_{6}
t
8
t_{8}
t
9
t_{9}
t
7
t_{7}
t
10
t_{10}
MV
-C
-O
✓
​
c
1
\checkmark\,c_{1}
1
1
1
1
1
0
1
0
0
0
.60
1.00
1.00
✓
​
c
2
\checkmark\,c_{2}
1
1
1
0
0
1
0
0
0
0
.40
.00
.99
✓
​
c
3
\checkmark\,c_{3}
1
1
0
1
1
0
0
1
0
0
.50
1.00
.70
×
c
4
\times\,c_{4}
0
0
0
1
0
1
1
1
1
1
.60
.90
.01
×
c
5
\times\,c_{5}
0
1
0
0
0
0
1
1
1
1
.50
.00
.29
×
c
6
\times\,c_{6}
0
0
0
0
1
0
1
1
1
1
.50
.10
.01
×
c
7
\times\,c_{7}
0
0
0
0
0
0
1
1
1
1
.40
.00
.00
×
c
8
\times\,c_{8}
0
0
0
0
0
0
1
1
0
1
.30
.00
.00
α
j
\alpha_{j}
1.00
1.00
.67
.67
.67
.33
.33
.33
.00
.00
β
j
\beta_{j}
.00
.20
.00
.20
.20
.20
1.00
1.00
.80
1.00
δ
j
\delta_{j}
+
1.0
+1.0
+
.80
+.80
+
.67
+.67
+
.47
+.47
+
.47
+.47
+
.13
+.13
−
.67
-.67
−
.67
-.67
−
.80
-.80
−
1.0
-1.0
LOO
C
{}_{\text{C}}
.40
.41
.46
.80
.53
.46
.42
.21
.41
.20
w
j
C
w_{j}^{\text{C}}
.00
.00
.00
.90
.10
.00
.00
.00
.00
.00
LOO
O
{}_{\text{O}}
1.00
.81
.83
.73
.67
.67
.17
.00
.22
.00
w
j
O
w_{j}^{\text{O}}
.40
.29
.30
.01
.00
.00
.00
.00
.00
.00
Taken together, these controlled cases make the complementarity between ACES-C and ACES-O explicit.
We next move from mechanism-focused examples to broader evaluations across generation models and benchmarks.
C.2
Additional Generation Models and Benchmarks
We evaluate ACES on three additional code generation models beyond GPT-3.5-Turbo: Qwen2.5-Coder-7B and 14B
(
Hui et al., 2024
)
, and DeepSeek-Coder-V2-16B
(
Guo et al., 2024
)
.
In addition to HumanEval and HumanEval
+
, we include LeetCodeDataset
(
Xia et al., 2025
)
as a harder benchmark.
For each model, we generate candidates and test cases following the same protocol as Section
4.1
.
Table
5
reports results on all tasks; Table
6
reports results on non-trivial tasks (
0
<
n
+
<
n
0<n^{+}<n
), excluding tasks where all or no candidates are correct.
Table 5:
Pass@
k
k
(%) with additional generation models on all tasks.
Each model generates its own candidates and test cases following the protocol of Section
4.1
.
Subscripts denote the change from each model’s
zero-shot
baseline.
Bold
/
underline
: best/second-best among reranking methods within each model.
Shaded
: ours.
HumanEval
HumanEval
+
LeetCodeDataset
Method
Pass@1
Pass@2
Pass@5
Pass@1
Pass@2
Pass@5
Pass@1
Pass@2
Pass@5
Qwen2.5-Coder-7B
Zero-shot
81.69
87.21
91.27
75.63
81.38
85.62
14.64
18.82
24.50
Majority Voting
89.02
+7.3
90.24
+3.0
90.24
-1.0
80.49
+4.9
84.15
+2.8
84.15
-1.5
14.04
-0.6
15.79
-3.0
19.74
-4.8
ACES-C
89.63
+7.9
90.24
+3.0
90.24
-1.0
81.71
+6.1
84.15
+2.8
84.76
-0.9
17.54
+2.9
18.86
+0.0
20.18
-4.3
ACES-O
90.24
+8.6
90.85
+3.6
90.85
-0.4
82.93
+7.3
84.76
+3.4
84.76
-0.9
15.35
+0.7
16.67
-2.2
20.61
-3.9
Qwen2.5-Coder-14B
Zero-shot
87.74
91.45
94.50
79.40
82.97
85.96
20.54
24.94
30.48
Majority Voting
92.07
+4.3
92.68
+1.2
92.68
-1.8
84.76
+5.4
85.37
+2.4
87.80
+1.8
23.25
+2.7
26.32
+1.4
31.14
+0.7
ACES-C
92.68
+4.9
92.68
+1.2
93.29
-1.2
84.76
+5.4
84.76
+1.8
86.59
+0.6
28.07
+7.5
29.82
+4.9
32.89
+2.4
ACES-O
93.29
+5.6
93.29
+1.8
93.29
-1.2
85.37
+6.0
85.37
+2.4
87.20
+1.2
21.49
+1.0
24.12
-0.8
28.95
-1.5
DeepSeek-Coder-V2-16B
Zero-shot
77.74
82.26
86.50
71.05
75.30
79.03
20.68
24.25
28.14
Majority Voting
84.76
+7.0
85.98
+3.7
86.59
+0.1
76.83
+5.8
77.44
+2.1
78.05
-1.0
17.11
-3.6
20.18
-4.1
24.12
-4.0
ACES-C
87.20
+9.5
87.20
+4.9
87.20
+0.7
78.66
+7.6
78.66
+3.4
78.66
-0.4
25.00
+4.3
25.88
+1.6
26.75
-1.4
ACES-O
85.98
+8.2
86.59
+4.3
87.20
+0.7
78.05
+7.0
78.05
+2.8
78.66
-0.4
19.74
-0.9
21.05
-3.2
24.56
-3.6
Table 6:
Pass@
k
k
(%) with additional generation models on non-trivial tasks (
0
<
n
+
<
n
0<n^{+}<n
), excluding tasks where all or no candidates are correct.
Subscripts denote the change from each model’s
zero-shot
baseline on the same set of tasks.
Bold
/
underline
: best/second-best among reranking methods within each model.
Shaded
: ours.
HumanEval
HumanEval
+
LeetCodeDataset
Method
Pass@1
Pass@2
Pass@5
Pass@1
Pass@2
Pass@5
Pass@1
Pass@2
Pass@5
Qwen2.5-Coder-7B
Zero-shot
76.98
86.03
92.68
75.03
84.46
91.42
31.02
42.24
57.49
Majority Voting
89.00
+12.0
91.00
+5.0
91.00
-1.7
83.00
+8.0
89.00
+4.5
89.00
-2.4
29.41
-1.6
34.12
-8.1
44.71
-12.8
ACES-C
90.00
+13.0
91.00
+5.0
91.00
-1.7
85.00
+10.0
89.00
+4.5
90.00
-1.4
38.82
+7.8
42.35
+0.1
45.88
-11.6
ACES-O
91.00
+14.0
92.00
+6.0
92.00
-0.7
87.00
+12.0
90.00
+5.5
90.00
-1.4
32.94
+1.9
36.47
-5.8
47.06
-10.4
Qwen2.5-Coder-14B
Zero-shot
68.41
80.36
90.16
67.05
77.32
85.91
32.83
42.87
55.50
Majority Voting
82.35
+13.9
84.31
+4.0
84.31
-5.9
82.46
+15.4
84.21
+6.9
91.23
+5.3
39.00
+6.2
46.00
+3.1
57.00
+1.5
ACES-C
84.31
+15.9
84.31
+4.0
86.27
-3.9
82.46
+15.4
82.46
+5.1
87.72
+1.8
50.00
+17.2
54.00
+11.1
61.00
+5.5
ACES-O
86.27
+17.9
86.27
+5.9
86.27
-3.9
84.21
+17.2
84.21
+6.9
89.47
+3.6
35.00
+2.2
41.00
-1.9
52.00
-3.5
DeepSeek-Coder-V2-16B
Zero-shot
64.38
75.63
86.15
61.77
72.63
82.19
39.14
49.74
61.25
Majority Voting
81.82
+17.4
84.85
+9.2
86.36
+0.2
76.56
+14.8
78.12
+5.5
79.69
-2.5
28.57
-10.6
37.66
-12.1
49.35
-11.9
ACES-C
87.88
+23.5
87.88
+12.3
87.88
+1.7
81.25
+19.5
81.25
+8.6
81.25
-0.9
51.95
+12.8
54.55
+4.8
57.14
-4.1
ACES-O
84.85
+20.5
86.36
+10.7
87.88
+1.7
79.69
+17.9
79.69
+7.1
81.25
-0.9
36.36
-2.8
40.26
-9.5
50.65
-10.6
Three findings emerge from these results.
At least one ACES variant improves Pass@1 over Majority Voting on every model–benchmark pair.
The improvement is most pronounced at
k
=
1
k{=}1
, where ranking quality is most critical.
On HumanEval, the best ACES variant gains
+
1.2
+1.2
to
+
2.4
+2.4
points over MV across the three models; on HumanEval
+
, the gain ranges from
+
0.6
+0.6
to
+
2.4
+2.4
points.
The two variants exhibit complementary strengths: ACES-O leads ACES-C on HumanEval and HumanEval
+
for both Qwen models, whereas ACES-C leads for DeepSeek-Coder-V2-16B and on LeetCodeDataset across all three models.
On LeetCodeDataset, ACES-C is consistently strongest and corrects MV failures on the harder pools.
Majority Voting falls below zero-shot for Qwen2.5-Coder-7B (14.04% vs. 14.64%) and DeepSeek-Coder-V2-16B (17.11% vs. 20.68%), while improving over zero-shot for Qwen2.5-Coder-14B (23.25% vs. 20.54%).
ACES-C reaches 17.54%, 28.07%, and 25.00% Pass@1, respectively, exceeding both MV and zero-shot for every model; its gain over MV grows from
+
3.5
+3.5
points on Qwen2.5-Coder-7B to
+
4.8
+4.8
on Qwen2.5-Coder-14B and
+
7.9
+7.9
on DeepSeek-Coder-V2-16B.
ACES-O is less stable: it improves over MV for Qwen2.5-Coder-7B and DeepSeek-Coder-V2-16B, but trails MV for Qwen2.5-Coder-14B (21.49% vs. 23.25%).
The consistent ACES-C lead, together with ACES-O’s regression on Qwen2.5-Coder-14B, shows that the closed-form variant is more robust on these LeetCodeDataset candidate pools, whereas iterative optimization does not uniformly improve over MV in this regime.
Non-trivial tasks amplify the improvements.
When trivial tasks are excluded (Table
6
), all methods operate on tasks where the ranking actually matters, and the ACES advantage becomes more visible.
On LeetCodeDataset non-trivial tasks, ACES-C improves over MV by
+
9.4
+9.4
points (Qwen2.5-Coder-7B),
+
11.0
+11.0
points (Qwen2.5-Coder-14B), and
+
23.4
+23.4
points (DeepSeek-Coder-V2-16B) at Pass@1.
On HumanEval non-trivial tasks, the corresponding gains are
+
1.0
+1.0
,
+
2.0
+2.0
, and
+
6.1
+6.1
points, respectively.
C.3
Pass@k vs. k
Figure
5
extends the main results (combined with
𝒟
​
𝒮
3
\mathcal{DS}^{3}
pre-filtering) to
k
=
1
,
…
,
20
k=1,\ldots,20
.
Both ACES variants substantially outperform Majority Voting across all benchmarks and
k
k
, with the largest gains at small
k
k
where ranking quality matters most.
On HumanEval and HumanEval
+
, ACES-C +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
leads at small
k
k
(e.g.,
+
2.44
%
+2.44\%
Pass@1 on HumanEval
+
), reflecting its closed-form weighting that concentrates on a few highly discriminative tests for sharp top-1 discrimination; the gap between the two variants narrows as
k
k
grows and they converge at larger
k
k
.
On MBPP, ACES-O +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
slightly leads at small
k
k
, consistent with MBPP’s higher fraction of misleading tests (Section
4.3
) making iterative optimization more valuable; beyond
k
=
2
k{=}2
the two variants are nearly identical.
The overall improvement scales with benchmark difficulty:
∼
6
{\sim}6
–
8
%
8\%
on MBPP (most misleading tests) vs.
∼
3
{\sim}3
–
5
%
5\%
on HumanEval, confirming the greater benefit of principled test weighting when test quality is more heterogeneous.
Figure 5:
Pass@
k
k
vs.
k
k
(
k
=
1
,
…
,
20
k=1,\ldots,20
) on all three benchmarks, combined with
𝒟
​
𝒮
3
\mathcal{DS}^{3}
pre-filtering.
ACES-C +
𝒟
​
𝒮
3
\mathcal{DS}^{3}
leads at small
k
k
on HumanEval/HumanEval
+
; the two variants converge at larger
k
k
. On MBPP they perform comparably throughout.
C.4
Assumption Satisfaction Analysis
We verify Assumption
4
empirically on all three benchmarks.
For each task, we remove trivial tasks (all codes correct or all incorrect) and constant-column tests (all codes pass or all fail), then compute
δ
¯
=
(
1
/
m
)
​
∑
j
δ
j
\bar{\delta}=(1/m)\sum_{j}\delta_{j}
over the remaining
m
m
non-constant tests.
Assumption
4
formally requires
δ
¯
>
2
​
ln
⁡
2
/
m
\bar{\delta}>2\sqrt{\ln 2/m}
, where the threshold is task-specific since each task has a different number of non-constant tests
m
m
.
Table
7
reports the formal satisfaction rate.
The figures in this section bin tasks by
δ
¯
\bar{\delta}
using the simplified threshold
δ
¯
>
0
\bar{\delta}>0
for visual clarity.
Tasks are binned with width
0.1
0.1
(left-open right-closed) and further divided into three equal-width regions (
Hard
/
Middle
/
Easy
).
Table 7:
Assumption
4
satisfaction across benchmarks. The threshold
2
​
ln
⁡
2
/
m
2\sqrt{\ln 2/m}
is evaluated per task using its number of non-constant tests
m
m
.
Benchmark
Non-trivial tasks
δ
¯
>
2
​
ln
⁡
2
/
m
\bar{\delta}>2\sqrt{\ln 2/m}
(%)
δ
¯
\bar{\delta}
range
HumanEval
118
83.1
[
−
0.42
,
1.00
]
[-0.42,\;1.00]
HumanEval
+
123
82.1
[
−
0.42
,
1.00
]
[-0.42,\;1.00]
MBPP
239
71.1
[
−
0.90
,
1.00
]
[-0.90,\;1.00]
The assumption is satisfied for the majority of non-trivial tasks on all benchmarks.
MBPP has a higher proportion of hard tasks, consistent with its greater fraction of misleading tests.
Figures
6
–
8
show the full per-benchmark results for Pass@
k
k
(
k
∈
{
1
,
2
,
5
}
k\in\{1,2,5\}
), extending the MBPP Pass@1 analysis in Section
4.3
to all benchmarks and
k
k
values.
The key findings from the main text generalize consistently across all three benchmarks and
k
k
values:
(i) The Middle region is where ACES provides the most value.
In the Easy region (high
δ
¯
\bar{\delta}
), all methods achieve near-perfect pass rates since most tests are informative and even uniform weighting works well.
The performance gains of ACES concentrate in the Middle region, where informative and misleading tests coexist and principled test weighting becomes critical.
(ii) ACES-O and ACES-C have complementary strengths across difficulty regimes.
When the assumption is not well satisfied (low
δ
¯
\bar{\delta}
), ACES-O’s iterative optimization is more effective at identifying and up-weighting the few reliable tests, giving it a clear advantage over ACES-C.
When the assumption is well satisfied (high
δ
¯
\bar{\delta}
), ACES-C’s closed-form solution is already near-optimal, matching or approaching ACES-O without requiring iterative optimization.
(iii) As
k
k
increases, the gap between methods narrows
, since selecting more candidates reduces the sensitivity to ranking quality at the top.
This pattern is consistent across all benchmarks.
(a)
Pass@1
(b)
Pass@2
(c)
Pass@5
Figure 6:
Assumption
4
analysis on HumanEval (tasks binned by
δ
¯
\bar{\delta}
).
ACES-O leads in the Middle region across all
k
k
; the gap narrows as
k
k
increases.
(a)
Pass@1
(b)
Pass@2
(c)
Pass@5
Figure 7:
Assumption
4
analysis on HumanEval
+
(tasks binned by
δ
¯
\bar{\delta}
).
ACES-O leads in the Middle region across all
k
k
; the gap narrows as
k
k
increases.
(a)
Pass@1
(b)
Pass@2
(c)
Pass@5
Figure 8:
Assumption
4
analysis on MBPP (tasks binned by
δ
¯
\bar{\delta}
).
ACES-O leads in the Middle region across all
k
k
; the gap narrows as
k
k
increases.
C.5
Selection vs. Weighting
ACES-C combines two effects:
test selection
(filtering out misleading tests via the
max
⁡
(
0
,
⋅
)
\max(0,\cdot)
threshold) and
non-uniform weighting
(assigning higher weight to more discriminative tests).
To disentangle their contributions, we first establish a theoretical guarantee for filtering alone, then empirically quantify the additional benefit of weighting.
Theoretical motivation.
By Theorem
3
,
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
)
]
−
1
/
2
=
c
j
​
(
w
)
⋅
δ
j
\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w)]-1/2=c_{j}(w)\cdot\delta_{j}
, where
c
j
​
(
w
unif
)
>
0
c_{j}(w_{\mathrm{unif}})>0
for all
j
j
under Assumption
4
(Proposition
5
).
Since the proportionality constant is positive, the sign is preserved:
sign
⁡
(
𝔼
⁡
[
LOO
​
-
​
AUC
j
​
(
w
unif
)
]
−
1
2
)
=
sign
⁡
(
δ
j
)
.
\mathrm{sign}\!\left(\mathbb{E}[\mathrm{LOO\text{-}AUC}_{j}(w_{\mathrm{unif}})]-\tfrac{1}{2}\right)\;=\;\mathrm{sign}(\delta_{j}).
That is, tests with
LOO
​
-
​
AUC
j
>
1
/
2
\mathrm{LOO\text{-}AUC}_{j}>1/2
are informative (
δ
j
>
0
\delta_{j}>0
) in expectation, and those with
LOO
​
-
​
AUC
j
<
1
/
2
\mathrm{LOO\text{-}AUC}_{j}<1/2
are misleading (
δ
j
<
0
\delta_{j}<0
).
If one could perfectly identify and remove all misleading tests (
δ
j
≤
0
\delta_{j}\leq 0
), assigning uniform weights to the remaining
m
′
m^{\prime}
informative tests would provably improve the signal-to-noise ratio.
Let
R
⁡
(
w
unif
)
=
m
​
δ
¯
2
R(w_{\mathrm{unif}})=m\bar{\delta}^{2}
denote the SNR of Majority Voting (Section
2.2
).
Uniform weighting over only the
m
′
m^{\prime}
tests with
δ
j
>
0
\delta_{j}>0
gives:
R
⁡
(
w
filter
)
R
⁡
(
w
unif
)
=
(
∑
j
:
δ
j
>
0
δ
j
∑
j
=
1
m
δ
j
)
2
⏟
≥
1
⋅
m
m
′
⏟
≥
1
≥
1
,
\frac{R(w_{\mathrm{filter}})}{R(w_{\mathrm{unif}})}\;=\;\underbrace{\left(\frac{\textstyle\sum_{j:\,\delta_{j}>0}\delta_{j}}{\textstyle\sum_{j=1}^{m}\delta_{j}}\right)^{\!2}}_{\geq\,1}\cdot\underbrace{\frac{m}{m^{\prime}}}_{\geq\,1}\;\geq\;1,
since removing non-positive
δ
j
\delta_{j}
terms can only increase the sum, and fewer tests reduce
∑
j
w
j
2
\sum_{j}w_{j}^{2}
.
By Theorem
2
, a higher
R
⁡
(
w
)
R(w)
yields a tighter Pass@
k
k
bound.
The sign identity above provides exactly such a criterion from the pass matrix alone: threshold at
LOO
​
-
​
AUC
j
=
1
/
2
\mathrm{LOO\text{-}AUC}_{j}=1/2
.
We define ACES-C Filter as:
w
j
filter
=
{
1
/
m
′
if
​
LOO
​
-
​
AUC
j
​
(
w
unif
)
>
1
/
2
,
0
otherwise,
m
′
=
|
{
j
:
LOO
​
-
​
AUC
j
​
(
w
unif
)
>
1
/
2
}
|
.
w_{j}^{\mathrm{filter}}\;=\;\begin{cases}1/m^{\prime}&\text{if }\mathrm{LOO\text{-}AUC}_{j}(w_{\mathrm{unif}})>1/2,\\
0&\text{otherwise,}\end{cases}\qquad m^{\prime}=|\{j:\mathrm{LOO\text{-}AUC}_{j}(w_{\mathrm{unif}})>1/2\}|.
Experimental design.
We compare three methods:
(1) Majority Voting (uniform weights on all tests),
(2) ACES-C Filter (discard tests with
LOO
​
-
​
AUC
j
≤
1
/
2
\mathrm{LOO\text{-}AUC}_{j}\leq 1/2
, uniform weights on the rest), and
(3) ACES-C (LOO-AUC excess weighting, Eq. (
8
)).
Table 8:
Selection vs. weighting (Pass@1). Subscripts denote the change from GPT-3.5-Turbo direct inference. ACES-C Filter isolates the contribution of test selection; ACES-C adds non-uniform weighting on top.
Method
HumanEval
HumanEval
+
MBPP
GPT-3.5-Turbo
68.38
58.75
66.80
Majority Voting
80.49
+12.1
69.51
+10.8
68.62
+1.8
ACES-C Filter
81.10
+12.7
69.51
+10.8
69.32
+2.5
ACES-C
82.93
+14.6
71.34
+12.6
71.19
+4.4
Results.
Consistent with the theoretical guarantee, ACES-C Filter matches or improves over Majority Voting on all three benchmarks (+0.61 on HumanEval, +0.00 on HumanEval
+
, +0.70 on MBPP).
However, the gains are modest because most misleading tests have
|
δ
j
|
|\delta_{j}|
close to zero (Figure
3
), so removing them changes
R
⁡
(
w
)
R(w)
only slightly.
The additional gain from non-uniform weighting (ACES-C vs. ACES-C Filter) is substantially larger (+1.83 on HumanEval, +1.83 on HumanEval
+
, +1.87 on MBPP), consistently accounting for over 70% of the total improvement.
This demonstrates that the primary value of LOO-AUC lies not in binary test filtering, but in the continuous weight magnitudes that amplify informative tests proportionally to their discriminative power.
C.6
Sensitivity to Number of Tests
Figure
9
shows Pass@1 as a function of the number of available tests
m
′
m^{\prime}
, where tests are randomly subsampled from the full test suite (averaged over 5 trials).
All methods use the same configuration as in the main experiments (Section
4.1
).
All three methods improve consistently with
m
′
m^{\prime}
, but their scaling behaviors differ substantially.
MV plateaus around
m
′
=
50
m^{\prime}=50
–
100
100
.
Since uniform weighting treats informative and misleading tests equally, adding more tests of mixed quality provides diminishing marginal benefit once the pool is large enough.
Both ACES variants continue improving beyond this plateau: more tests provide better LOO-AUC estimates, enabling finer-grained weight differentiation between informative and misleading tests.
At
m
′
=
100
m^{\prime}=100
, ACES-C already outperforms MV at full
m
′
=
500
m^{\prime}=500
on all benchmarks, showing that intelligent weighting is more valuable than simply collecting more tests.
The gap between ACES-O and ACES-C generally widens with
m
′
m^{\prime}
: at small
m
′
m^{\prime}
the two variants perform similarly, but with more tests ACES-O’s optimization can exploit the richer signal to further refine the weights.
Practically, even a modest test budget (
m
′
≈
100
m^{\prime}\approx 100
) suffices for the LOO-AUC weighting to capture most of the available signal.
Figure 9:
Sensitivity to the number of tests
m
′
m^{\prime}
. Tests are randomly subsampled; results averaged over 5 trials (shaded:
±
\pm
std). MV plateaus around
m
′
=
50
m^{\prime}{=}50
–
100
100
; both ACES variants continue improving and surpass MV at
m
′
=
500
m^{\prime}{=}500
with only
m
′
=
100
m^{\prime}{=}100
tests.
C.7
Sensitivity to Number of Candidate Codes
Figure
10
shows Pass@1 as a function of the number of candidate codes
n
′
n^{\prime}
, where codes are stratified-subsampled to preserve the correct/incorrect ratio
π
\pi
(averaged over 10 trials).
All
m
m
tests are retained; all methods use the same configuration as in the main experiments.
All three methods are stable with respect to
n
′
n^{\prime}
(standard deviations
≤
1.6
%
\leq 1.6\%
throughout), but their scaling behaviors differ.
MV is approximately flat across all
n
′
n^{\prime}
, and on MBPP it
decreases
from 70.8% (
n
′
=
20
n^{\prime}=20
) to 68.6% (
n
′
=
200
n^{\prime}=200
): with more candidates (most of which are incorrect), there are more incorrect codes that may outscore the best correct one under equal weighting.
ACES-C maintains performance close to its full-data result even at
n
′
=
20
n^{\prime}=20
.
This is because ACES-C computes weights in closed form from the pass matrix; even a small candidate pool suffices to produce meaningful LOO-AUC estimates.
ACES-O benefits the most from additional candidates.
At small
n
′
n^{\prime}
, the optimization has too few pairwise comparisons between passing and failing codes to learn reliable weights; as
n
′
n^{\prime}
grows, the gradient signal becomes richer and ACES-O achieves the best performance at
n
′
=
200
n^{\prime}=200
on all benchmarks.
Figure 10:
Sensitivity to the number of candidate codes
n
′
n^{\prime}
. Codes are stratified-subsampled to preserve the correct/incorrect ratio; results averaged over 10 trials (shaded:
±
\pm
std). MV is flat or declining; ACES-C is robust even at small
n
′
n^{\prime}
; ACES-O improves steadily and leads at
n
′
=
200
n^{\prime}{=}200
.
Summary of data sensitivity (Appendices
C.6
–
C.7
).
The two sensitivity analyses reveal complementary strengths of the three methods.
MV plateaus early with
m
′
m^{\prime}
and can even degrade with larger
n
′
n^{\prime}
, since uniform weighting cannot exploit additional tests or candidates.
ACES-C is robust to both
m
′
m^{\prime}
and
n
′
n^{\prime}
, requiring neither many tests nor many candidates to achieve strong performance; it is the safest choice under limited data budgets.
ACES-O achieves the best performance when both
m
′
m^{\prime}
and
n
′
n^{\prime}
are sufficiently large, as the optimization benefits from richer pairwise signal; in the standard setting (
n
=
200
n{=}200
,
m
≈
500
m\approx 500
), it consistently leads on all benchmarks.
C.8
Effect of Pre-Filtering Cutoff
Figure
11
shows the effect of the pre-filtering cutoff
K
K
on both ACES variants.
For each
K
K
, we select the top-
K
K
candidates by majority vote, run the reranking method on the resulting
K
×
m
K\times m
submatrix, and score all
n
=
200
n=200
codes with the learned weights.
The two variants exhibit complementary trends, each excelling in a different regime.
ACES-C generally improves as
K
K
increases, reaching its best performance at
K
=
200
K=200
(no pre-filtering) on all benchmarks.
This is consistent with the findings in Appendix
C.7
: more codes provide better LOO-AUC estimates for the closed-form weighting.
ACES-O achieves its best results at small to moderate
K
K
(8–32), where the pre-filtered candidate pool concentrates on high-quality codes and provides a cleaner optimization landscape.
Performance is strong across a wide range of
K
K
values and declines gradually for larger
K
K
, since including many low-quality candidates introduces noise into the pairwise comparisons.
These complementary profiles are consistent with the design of the two variants: ACES-C operates on all
n
n
candidates to maximize its closed-form estimates, while ACES-O benefits from a focused candidate pool for optimization.
Figure 11:
Sensitivity to the pre-filtering cutoff
K
K
. ACES-C (blue) benefits from larger candidate pools; ACES-O (green) benefits from focused pre-filtering. Dashed line: MV baseline (independent of
K
K
).
C.9
ACES-O Convergence
Figure
12
shows the convergence behavior of ACES-O over
T
=
300
T=300
iterations, averaged across all tasks per benchmark.
The top row plots the surrogate objective
J
⁡
(
w
)
=
∑
j
w
j
​
(
LOO
​
-
​
AUC
^
j
​
(
w
)
−
1
2
)
J(w)=\sum_{j}w_{j}\bigl(\widehat{\mathrm{LOO\text{-}AUC}}_{j}(w)-\tfrac{1}{2}\bigr)
(Eq.
9
), where
LOO
​
-
​
AUC
^
j
\widehat{\mathrm{LOO\text{-}AUC}}_{j}
is the logistic surrogate (Eq.
11
).
The bottom row plots the corresponding Pass@1 (smoothed with a 15-step moving average; raw values shown in light green).
The surrogate objective
J
⁡
(
w
)
J(w)
increases smoothly and monotonically on all three benchmarks, with the steepest gains in the first 50 iterations and near-complete convergence by iteration 80–100.
Pass@1 reflects this stability: once the surrogate converges, the discrete Pass@1 metric remains essentially flat, fluctuating by at most 0.6 percentage points between
T
=
50
T=50
and
T
=
300
T=300
on all benchmarks.
ACES-O surpasses both MV and ACES-C early in the optimization and maintains this advantage throughout, confirming that the objective
J
⁡
(
w
)
J(w)
is well-aligned with downstream Pass@
k
k
performance.
The results are robust to the choice of
T
T
: any value in the range
[
50,300
]
[50,300]
yields comparable performance.
Figure 12:
ACES-O convergence over 300 iterations, averaged across all tasks.
Top:
surrogate objective
J
⁡
(
𝐰
)
J(\mathbf{w})
converges by iteration 80–100.
Bottom:
Pass@1 (smoothed; raw in light green) surpasses both MV (dashed gray) and ACES-C (dashed blue) and remains stable for
T
∈
[
50,300
]
T\in[50,300]
.
C.10
ACES-O Hyperparameter Sensitivity
Figure
13
shows the effect of varying the two key ACES-O hyperparameters independently: the logistic surrogate sharpness
γ
\gamma
(top row) and the learning rate
η
\eta
(bottom row).
When sweeping one parameter, the other is held at its default value.
Both hyperparameters exhibit broad stable regions.
For
γ
\gamma
, the only requirement is that the logistic surrogate be sharp enough to approximate the indicator function:
γ
≤
2
\gamma\leq 2
is insufficient, but any
γ
≥
5
\gamma\geq 5
yields strong performance, with the entire range
[
5
,
50
]
[5,50]
varying by fewer than 2 percentage points on all benchmarks.
For
η
\eta
, the stable region is even wider:
η
∈
[
0.005
,
0.5
]
\eta\in[0.005,0.5]
consistently outperforms MV, again varying by at most 2 percentage points.
The values used in the main experiments fall well within these stable regions.
Figure 13:
ACES-O hyperparameter sensitivity.
Top:
Pass@1 vs. surrogate sharpness
γ
\gamma
(other parameters at defaults).
Bottom:
Pass@1 vs. learning rate
η
\eta
. Dashed gray line: MV baseline. For
γ
≥
5
\gamma\geq 5
and
η
∈
[
0.005
,
0.5
]
\eta\in[0.005,0.5]
, ACES-O consistently outperforms MV on all benchmarks.
C.11
Computational Cost
Figure
14
compares the reranking time per task for five methods (
n
=
200
n=200
,
m
=
500
m=500
), measured on a single CPU core of an Apple M3 MacBook Air (16 GB RAM) and averaged over all tasks.
We time only the reranking step; shared upstream costs (code generation, test generation, code execution) are excluded.
To ensure a fair comparison, all execution outputs are pre-hashed before timing, so that string comparisons in output-level methods (MBR-exec) reduce to integer comparisons.
All methods finish within one second per task.
MV, CodeT, ACES-C, and ACES-O operate solely on the binary pass matrix; among these, ACES-C (9 ms) adds negligible overhead over MV (4 ms) thanks to its closed-form computation.
ACES-O requires
∼
0.85
{\sim}0.85
s for iterative optimization, comparable to MBR-exec (
∼
0.38
{\sim}0.38
s), which incurs
O
⁡
(
n
2
​
m
)
O(n^{2}m)
pairwise output comparisons.
In practice, the reranking cost for all methods is negligible relative to upstream code execution, which dominates wall-clock time.
Note that all methods compared above operate solely on execution results (the binary pass matrix or output strings).
Methods that incorporate static analysis or invoke LLMs for repeated evaluation incur substantially higher costs, often orders of magnitude greater, due to the expense of additional model inference, and are therefore not included in this timing comparison.
Figure 14:
Reranking time per task (log scale,
n
=
200
n{=}200
,
m
=
500
m{=}500
, single CPU core). Shared upstream costs are excluded; execution outputs are pre-hashed for fair comparison. All methods finish within one second.
C.12
Pairwise Vote Statistics
To complement the assumption analysis, we directly measure the empirical distribution of the three pairwise vote types defined in Table
1
.
For each non-trivial task, we enumerate all
(
c
+
,
c
−
,
t
j
)
(c^{+},c^{-},t_{j})
triples and classify each vote
h
j
=
B
c
+
,
j
−
B
c
−
,
j
h_{j}=B_{c^{+},j}-B_{c^{-},j}
as informative (
+
1
+1
), uninformative (
0
0
), or misleading (
−
1
-1
).
Table
9
reports the aggregate proportions.
Table 9:
Pairwise vote distribution across benchmarks. Informative votes consistently dominate misleading ones, confirming Assumption
4
.
Benchmark
Informative (%)
Uninformative (%)
Misleading (%)
Inf/Mis ratio
HumanEval
22.6
72.2
5.3
4.3
×
\times
HumanEval
+
20.7
74.9
4.4
4.7
×
\times
MBPP
30.7
59.1
10.2
3.0
×
\times
Misleading votes are rare across all benchmarks (
≤
10.2
%
\leq 10.2\%
), confirming that the majority of pairwise test–code interactions provide either correct or neutral ranking signal.
Uninformative votes dominate (59–75%): even after removing constant-column tests, most non-constant tests agree on any given
(
c
+
,
c
−
)
(c^{+},c^{-})
pair, since a test that distinguishes some pairs may still assign the same outcome to others.
This highlights the value of concentrating weight on the subset of tests that actively discriminate.
MBPP has roughly twice the misleading rate of HumanEval (10.2% vs. 5.3%), consistent with its lower assumption satisfaction rate (71.1% vs. 83.1%; Table
7
).
The informative-to-misleading ratio remains
≥
3
×
\geq 3\times
on all benchmarks, providing a comfortable margin for Assumption
4
.
C.13
Generation Prompts
HumanEval, HumanEval
+
, and MBPP.
We use the prompts from the MPSC protocol
(
Huang et al., 2024
)
, reproduced below:
Prompt for generating candidate solutions (HumanEval / HumanEval
+
/ MBPP)
⬇
I
want
you
to
act
like
a
Python
programmer
.
I
will
give
you
the
declaration
of
a
function
and
comments
about
its
property
.
You
need
to
implement
the
body
of
the
function
in
the
code
block
.
Do
not
modify
any
code
I
provide
.
Do
not
provide
any
explanations
.
Here
is
the
question
.
‘‘‘
Python
{Docstring}
‘‘‘
Prompt for generating test cases (HumanEval / HumanEval
+
/ MBPP)
⬇
‘‘‘
Python
#
Given
a
docstring
,
continue
to
write
the
#
following
code
with
10
valid
assertion
#
statements
to
check
the
correctness
of
the
#
function
.
Provide
diverse
test
cases
.
{Docstring}
pass
#
check
the
correctness
of
with
10
different
#
valid
assertion
statements
in
the
form
of
#
"
assert
{entry point}
(...)
==
..."
assert
LeetCodeDataset (Appendix
C.2
).
Prompt for generating candidate solutions (LeetCodeDataset)
⬇
You
are
an
expert
Python
programmer
.
You
will
be
given
a
question
(
problem
specification
)
and
will
generate
a
correct
Python
program
that
matches
the
specification
and
passes
all
tests
.
###
Question
:
{question}
###
Format
:
You
will
use
the
following
starter
code
to
write
the
solution
to
the
problem
and
enclose
your
code
within
delimiters
.
‘‘‘
python
{starter_code}
‘‘‘
###
Answer
:
(
use
the
provided
format
with
backticks
)
Prompt for generating test cases (LeetCodeDataset)
⬇
You
are
an
expert
Python
programmer
.
You
will
be
given
a
question
(
problem
specification
)
and
starter
code
,
and
you
will
generate
diverse
and
semantically
correct
Python
assertion
statements
to
test
the
target
function
.
###
Question
:
{question}
###
Starter
Code
:
‘‘‘
python
{starter_code}
‘‘‘
###
Target
Call
:
{entry_point}
###
Format
:
Output
exactly
10
raw
Python
assertion
statements
.
Each
line
must
start
with
‘
assert
‘.
Use
the
exact
target
call
that
is
specified
.
Do
not
output
markdown
,
code
fences
,
comments
,
explanations
,
helper
functions
,
or
any
text
other
than
the
assertions
.
###
Answer
: