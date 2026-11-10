---
title: Uncertainty Quantification for LLM-based Code Generation
id: uncertainty-quantification-for-llm-based-code-generation
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:09:20.847666Z'
updated: '2026-11-09T23:27:44.647882Z'
source: https://arxiv.org/html/2605.12201
source_domain: arxiv.org
fetched_at: '2026-11-09T23:09:20.847349Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Risk-controlling prediction sets for LLM code generation via Learn Then
  Test with multi-label framing and selective execution; reduces code removal up to
  24.5% at same risk vs PAC prediction sets baseline; three LLMs. FULL TEXT. Verdict:
  L1/L4 adjacent: conformal partial-program prediction sets calibrated with test-case
  execution; no probes or verbal.'
---

Uncertainty Quantification for LLM-based Code Generation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2605.12201v1 [cs.SE] 12 May 2026
Uncertainty Quantification for LLM-based Code Generation
Senrong Xu
Affiliation:
State Key Lab of Novel Software Technology, Nanjing University
Correspondence to:
srxu@smail.nju.edu.cn
Yuhao Tan
Affiliation:
State Key Lab of Novel Software Technology, Nanjing University
Yanke Zhou
Affiliation:
State Key Lab of Novel Software Technology, Nanjing University
Guangyuan Wu
Affiliation:
State Key Lab of Novel Software Technology, Nanjing University
Zenan Li
Affiliation:
ETH Zürich
Yuan Yao
Affiliation:
State Key Lab of Novel Software Technology, Nanjing University
Correspondence to:
y.yao@nju.edu.cn
Taolue Chen
Affiliation:
Birkbeck, University of London
Feng Xu
Affiliation:
State Key Lab of Novel Software Technology, Nanjing University
Xiaoxing Ma
Affiliation:
State Key Lab of Novel Software Technology, Nanjing University
Abstract
Prediction sets provide a theoretically grounded framework for quantifying uncertainty in machine learning models. Adapting them to structured generation tasks, in particular, large language model (LLM) based code generation, remains a challenging problem. An existing attempt proposes PAC prediction sets but is limited by its strong monotonicity assumption on risk and single-label classification framework, which severely limits the space of candidate programs and cannot accommodate the multiple valid outputs inherent to code generation.
To address these limitations,
we propose an approach
RisCoSet
that leverages multiple hypothesis testing to construct risk-controlling predictions for LLM-based code generation. Given a trained code generation model, we produce a prediction set represented by a partial program, which is guaranteed to contain a correct solution with high confidence. Extensive experiments on three LLMs demonstrate the effectiveness of the proposed method. For instance, compared with the state-of-the-art, our method can significantly reduce the code removal by up to 24.5%, at the same level of risk.
Keywords:
Machine Learning, ICML
1
Introduction
Figure 1:
An illustrative example from MBPP. The left part is a correct code snippet, and the right part is a generated but incorrect one.
RisCoSet
removes three nodes in the AST, resulting a prediction set (i.e., a partial program) that contains the correct program.
Large language models (LLMs) have been widely adopted by millions of users worldwide due to their strong performance
(
Achiam et al., 2023
;
Team et al., 2023
)
.
However, they often hallucinate facts and may generate toxic or biased outputs
(
Nadeau et al., 2024
)
, limiting
their use in high-stakes applications such as code generation and legal analysis
(
Liu et al., 2024
;
Dahl et al., 2024
)
.
As an uncertainty quantification method, conformal prediction (CP) can provide model-agnostic, distribution-free uncertainty guarantees for machine learning models, and thus has attracted recent attention
(
Vovk et al., 2005
;
Angelopoulos et al., 2022
)
.
For example, several studies have applied CP into LLM generation by identifying sound components within the LLM output
(
Quach et al., 2024
;
Cherian et al., 2024
)
.
However, these methods assume near independence among components, an assumption that holds for sentences in NLP but fails for structured outputs like code, where components interact systemically
(
Casalnuovo et al., 2019
;
Chen et al., 2022
)
.
To address this,
Khakhar et al. (2023)
proposed PAC (probably approximately correct) prediction sets for code generation, constructing structured prediction sets and providing statistical guarantees via partial programs
(
Guo et al., 2021
)
. However, this approach suffers from two key limitations: (1) it relies on a strong monotonicity constraint that restricts the space of admissible partial programs, which may lead to a suboptimal solution; (2) it is designed for single-label classification and does not easily accommodate the multiple valid programs (e.g., multiple syntactically different programs with identical, correct semantics) that naturally arise in code generation.
In this paper, we introduce a new method,
RisCoSet
, for constructing risk-controlling prediction sets tailored to code generation.
To overcome the limitations in PAC prediction sets, we reframe code uncertainty quantification as a multi-label classification problem, and adopt the Learn Then Test (LTT) framework
(
Angelopoulos et al., 2025
)
, a recent risk-controlling method, to construct structured prediction sets with rigorous statistical guarantees.
That is, given an LLM-generated code,
RisCoSet
yields a partial program (i.e., a subtree of the program’s abstract syntax tree (AST), see Fig.
1
), which is guaranteed, with high confidence, to contain a correct solution.
However, applying LTT into code generation is still challenging. The first challenge lies in the complexity of code search space.
Unlike traditional applications such as classification and regression whose search space is typically one-dimensional, the search space of structured data (such as code) is complex and multi-dimensional
(
Solar-Lezama, 2008
)
.
To this end, we design a tailored risk function and the corresponding optimization problem for obtaining partial programs. Furthermore, in multi-label settings, we need to sample additional candidate programs from LLMs and verify their correctness via test-case execution during calibration.
This is a computationally expensive step.
To reduce this cost, we propose a selective execution strategy that efficiently verifies the correctness of sampled programs by using a well-calibrated threshold to decide which programs require test execution.
Example.
Fig.
1
illustrates a real example from the MBPP dataset
(
Austin et al., 2021
)
.
The left code snippet is from a correct program, while the right one is generated by the model and is incorrect.
Our method,
RisCoSet
, removes the uncertain nodes in the AST (highlighted in red), resulting in a partial program (AST subtree) which can be completed to match a correct program.
This example also shows the potential implication of our method:
RisCoSet
can provide an almost-correct partial program of a given generated program, helping to mitigate code hallucinations
(
Liu et al., 2024
)
and reduce the cost of manual review
(
Zhong and Wang, 2017
)
.
Contributions.
The main contributions of the paper are summarized as:
(1) we specialize an LTT-based code generation approach
RisCoSet
for uncertainty quantification of LLM-based code generation, which reframes the construction of prediction sets for code as a multi-label problem with weaker constraints; (2) we propose a selective execution strategy to balance the trade-off between risk-controlling and sampling costs;
(3) We conduct comprehensive experiments across three LLMs and three code generation datasets, confirming the effectiveness of our method.
To the best of our knowledge, this is the first work to introduce the LTT framework into structured code generation tasks.
Structure.
Section
2
briefly introduces the background. Section
3
compares PAC and LTT in code generation.
Section
4
presents the proposed methods and Section
5
reports the experimental results. Section
6
discusses the related work, and Section
7
concludes the paper.
2
Background
Notations
.
For any natural number
n
n
, let
[
n
]
:=
{
1
,
…
,
n
}
[n]:=\{1,\dots,n\}
.
Let
𝒟
\mathcal{D}
denote a distribution over
𝒳
×
𝒴
\mathcal{X}\times\mathcal{Y}
, and let
𝒟
cal
=
{
(
X
i
,
Y
i
)
}
i
=
1
n
∼
i
.
i
.
d
.
𝒟
\mathcal{D}_{\mathrm{cal}}=\{(X_{i},Y_{i})\}_{i=1}^{n}\stackrel{{\scriptstyle\mathrm{i.i.d.}}}{{\sim}}\mathcal{D}
denote a calibration set.
In the single-label case,
Y
i
∈
𝒴
Y_{i}\in\mathcal{Y}
; in the multi-label case,
Y
i
⊆
𝒴
Y_{i}\subseteq\mathcal{Y}
.
Let
(
X
n
+
1
,
Y
n
+
1
)
∼
𝒟
(X_{n+1},Y_{n+1})\sim\mathcal{D}
be a test sample.
An abstract syntax tree (AST) of a program is denoted by
T
=
(
𝒱
,
ℰ
)
T=(\mathcal{V},\mathcal{E})
, where
𝒱
\mathcal{V}
and
ℰ
\mathcal{E}
are the sets of nodes and edges, respectively.
2.1
PAC Prediction Set
The objective of a PAC prediction
(
Park et al., 2020
)
is to produce a prediction set, instead of a single prediction, that satisfies statistical guarantees while remaining small in size.
Formally, for a test input
X
n
+
1
∈
𝒳
X_{n+1}\in\mathcal{X}
, PAC prediction set
C
τ
​
(
X
n
+
1
)
⊆
𝒴
C_{\tau}(X_{n+1})\subseteq\mathcal{Y}
ensures that the true label
Y
n
+
1
Y_{n+1}
is contained within the set for at least a
1
−
ε
1-\varepsilon
fraction of the population, with a probability at least
1
−
δ
1-\delta
, i.e.,
ℙ
⁡
(
ℙ
(
X
,
Y
)
∼
𝒟
​
(
Y
∈
C
τ
​
(
X
)
)
≥
1
−
ε
)
≥
1
−
δ
,
\mathbb{P}\Big(\mathbb{P}_{(X,Y)\sim\mathcal{D}}\big(Y\in C_{\tau}(X)\big)\geq 1-\varepsilon\Big)\geq 1-\delta,
where
C
τ
​
(
x
)
C_{\tau}(x)
is parameterized by
τ
∈
ℝ
\tau\in\mathbb{R}
, and the
ε
\varepsilon
and error level
δ
\delta
are chosen in advance by the user.
Technically, the prediction set is constructed by fitting the parameter
τ
\tau
on the calibration set
𝒟
cal
\mathcal{D}_{\mathrm{cal}}
. Existing methods
(
Park et al., 2020
;
Khakhar et al., 2023
)
rely on the assumption that
ℙ
⁡
(
Y
n
+
1
∈
C
τ
​
(
X
n
+
1
)
)
\mathbb{P}(Y_{n+1}\in C_{\tau}(X_{n+1}))
is monotone-decreasing in
τ
\tau
, which is typically guaranteed by the monotonicity of prediction sets, i.e.,
τ
<
τ
′
→
C
τ
​
(
X
n
+
1
)
⊇
C
τ
′
​
(
X
n
+
1
)
.
\tau<\tau^{\prime}\rightarrow C_{\tau}(X_{n+1})\supseteq C_{\tau^{\prime}}(X_{n+1}).
(1)
Therefore, a standard PAC formulation defines
C
τ
​
(
X
n
+
1
)
C_{\tau}(X_{n+1})
as the set of all labels whose model-assigned score exceeds the threshold
τ
\tau
:
C
τ
​
(
X
n
+
1
)
:=
{
y
∈
𝒴
∣
f
⁡
(
y
∣
X
n
+
1
)
≥
τ
}
,
C_{\tau}(X_{n+1}):=\left\{y\in\mathcal{Y}\mid f(y\mid X_{n+1})\geq\tau\right\},
where
f
⁡
(
y
∣
X
n
+
1
)
f(y\mid X_{n+1})
is a scoring function (e.g., the softmax output of a trained classifier).
2.2
LTT Framework
The Learn Then Test (LTT) framework
(
Angelopoulos et al., 2025
)
extends PAC prediction sets by providing control over the expectation of an arbitrary risk function, conditional on the calibration data.
It achieves this by reframing the selection of the prediction set parameter as a multiple-hypothesis testing problem.
Specifically, for a parameter
λ
\lambda
, let
𝒯
λ
​
(
x
)
⊆
𝒴
\mathcal{T}_{\lambda}(x)\subseteq\mathcal{Y}
denote the prediction set returned for an input
x
∈
𝒳
x\in\mathcal{X}
.
For a given
𝒯
λ
\mathcal{T}_{\lambda}
, we define a corresponding
risk
R
⁡
(
𝒯
λ
)
∈
ℝ
≥
0
R(\mathcal{T}_{\lambda})\in\mathbb{R}_{\geq 0}
that quantifies a problem-specific statistical error rate.
The goal of the LTT framework is to learn a parameter
λ
^
\hat{\lambda}
such that the function
𝒯
λ
^
\mathcal{T}_{\hat{\lambda}}
satisfies the following error-control guarantee for a test instance
(
X
n
+
1
,
Y
n
+
1
)
(X_{n+1},Y_{n+1})
.
Definition 2.1
(Risk-controlling)
.
A random variable
λ
^
∈
Λ
\hat{\lambda}\in\Lambda
is risk-controlling at
(
α
,
δ
)
(\alpha,\delta)
-level, if it satisfies
ℙ
⁡
(
R
⁡
(
𝒯
λ
^
)
≤
α
)
≥
1
−
δ
.
\mathbb{P}(R(\mathcal{T}_{\hat{\lambda}})\leq\alpha)\geq 1-\delta.
(2)
The risk tolerance
α
\alpha
and error level
δ
∈
(
0
,
1
)
\delta\in(0,1)
are user-specified. For brevity, we abbreviate
R
⁡
(
λ
)
=
R
⁡
(
𝒯
λ
)
R(\lambda)=R(\mathcal{T}_{\lambda})
below.
To control target risks, the LTT framework leverages the base model and the calibration set
𝒟
cal
\mathcal{D}_{\mathrm{cal}}
to identify valid
λ
\lambda
via multiple hypothesis testing.
Each
λ
k
∈
Λ
=
{
λ
1
,
…
,
λ
N
}
\lambda_{k}\in\Lambda=\{\lambda_{1},\dots,\lambda_{N}\}
is associated with the null hypothesis
ℋ
k
:
R
⁡
(
λ
k
)
>
α
\mathcal{H}_{k}:R(\lambda_{k})>\alpha
and
λ
k
\lambda_{k}
is considered valid if
ℋ
k
\mathcal{H}_{k}
is rejected.
For each
λ
k
\lambda_{k}
, a super-uniform
p
p
-value
p
k
p_{k}
is computed.
The output of LTT framework is the reject set
Λ
valid
=
𝒜
⁡
(
p
1
,
…
,
p
N
)
⊆
Λ
\Lambda_{\mathrm{valid}}=\mathcal{A}(p_{1},\dots,p_{N})\subseteq\Lambda
,
where
𝒜
\mathcal{A}
is any algorithm that controls the family-wise error rate (FWER).
With these steps, we have the following theorem.
Theorem 2.2
(Learn Then Test
(
Angelopoulos et al., 2025
)
)
.
Suppose each
p
k
p_{k}
has a super-uniform distribution under
ℋ
k
\mathcal{H}_{k}
. Let
𝒜
\mathcal{A}
be a FWER-controlling algorithm at level
δ
\delta
. Given a test instance
(
X
n
+
1
,
Y
n
+
1
)
(X_{n+1},Y_{n+1})
,
Λ
valid
\Lambda_{\mathrm{valid}}
satisfies
ℙ
⁡
(
sup
λ
∈
Λ
valid
R
⁡
(
λ
)
≤
α
∣
𝒟
cal
)
≥
1
−
δ
,
\mathbb{P}\left(\sup_{\lambda\in\Lambda_{\mathrm{valid}}}R(\lambda)\leq\alpha\mid\mathcal{D}_{\mathrm{cal}}\right)\geq 1-\delta,
(3)
where the supremum over an empty set is defined as
−
∞
-\infty
.
This theorem implies that any
λ
∈
Λ
valid
\lambda\in\Lambda_{\mathrm{valid}}
can be selected to control the risk
R
⁡
(
λ
)
R(\lambda)
on test instances. In particular, we recover a procedure similar to the PAC prediction set by defining
𝒯
λ
​
(
X
n
+
1
)
:=
{
y
∈
𝒴
∣
f
⁡
(
y
∣
X
n
+
1
)
≥
τ
}
\mathcal{T}_{\lambda}(X_{n+1}):=\{y\in\mathcal{Y}\mid f(y\mid X_{n+1})\geq\tau\}
and
R
(
λ
)
:=
𝟏
{
Y
n
+
1
∉
𝒯
λ
(
X
n
+
1
)
}
R(\lambda):=\mathbf{1}\{Y_{n+1}\notin\mathcal{T}_{\lambda}(X_{n+1})\}
.
3
PAC vs. LTT in Code Generation
Code generation is a typical structured prediction task with an exponentially large label space, rendering conventional conformal prediction intractable
(
Vovk et al., 2005
)
.
To address this,
Khakhar et al. (2023)
proposed to construct prediction sets via partial programs.
Their method represents a program as an AST, denoted as
T
=
(
𝒱
,
ℰ
)
T=(\mathcal{V},\mathcal{E})
, and formulates an optimization problem which selectively prunes nodes and edges from
T
T
, yielding a partial program
T
p
=
(
𝒱
p
,
ℰ
p
)
T_{p}=(\mathcal{V}_{p},\mathcal{E}_{p})
.
The resulting prediction set is defined as the collection of all complete programs that can be obtained by expanding
T
p
T_{p}
, and a correct program
T
′
=
(
𝒱
′
,
ℰ
′
)
T^{\prime}=(\mathcal{V}^{\prime},\mathcal{E}^{\prime})
belongs to this set iff
𝒱
p
⊆
𝒱
′
\mathcal{V}_{p}\subseteq\mathcal{V}^{\prime}
and
ℰ
p
⊆
ℰ
′
\mathcal{E}_{p}\subseteq\mathcal{E}^{\prime}
.
This construction enables the application of the PAC prediction set framework to code generation, providing statistical guarantees on program correctness.
However, PAC prediction sets exhibit two limitations when applied to code generation. First, they impose a monotonicity constraint (cf. Eq. (
1
)) as a compromise to PAC guarantee
(
Park et al., 2020
)
and can lead to suboptimal partial programs during optimization.
Second, PAC prediction sets are inherently designed for single-label tasks, whereas code generation naturally admits multiple valid outputs (i.e., multiple syntactically different but semantically-identical programs), rendering it a multi-label problem.
In contrast, the LTT framework avoids these limitations and is inherently flexible and scalable to multi-label settings.
Crucially, LTT does not require defining a scoring function for each program in an exponentially large prediction set; it only requires specifying the prediction set itself and its associated risk without any constraint.
We therefore argue that LTT is better suited for quantifying uncertainty in code generation than PAC prediction sets.
4
The Approach
We now introduce our method,
RisCoSet
, for constructing structured, risk-controlling prediction sets for LLM-based code generation. At a high level,
RisCoSet
defines a structured risk function on code prediction sets via solving an optimization problem.
For each calibration program
X
i
∈
𝒟
cal
X_{i}\in\mathcal{D}_{\mathrm{cal}}
, we sample multiple correct programs to obtain the enhanced label set
Y
~
i
\tilde{Y}_{i}
, according to the corresponding generation task of
X
i
X_{i}
.
Finally, we apply multiple hypothesis testing, following the procedure of LTT, to identify valid parameters
Λ
valid
\Lambda_{\mathrm{valid}}
. These parameters are then used to generate risk-controlling prediction sets for the test program
X
n
+
1
X_{n+1}
.
Additionally, we propose a selective execution strategy to lower the computational cost of verifying sample programs’ correctness, by tolerating a controlled rate of labeling errors.
4.1
Structured Risk Function
Unlike standard multi-label classification problems where the false discovery rate (FDR) is a common control target, our focus is on the semantic correctness of the structured output.
Specifically, given an input program
X
X
, we require the prediction set
𝒯
λ
​
(
X
)
\mathcal{T}_{\lambda}(X)
to contain at least one program that belongs to the set
Y
~
\tilde{Y}
of correct programs.
Formally, we define the empirical structured risk on the enhanced calibration set
{
(
X
i
,
Y
~
i
)
}
i
=
1
n
\{(X_{i},\tilde{Y}_{i})\}_{i=1}^{n}
as
R
^
n
s
(
λ
)
:=
1
n
∑
i
=
1
n
𝟏
{
𝒯
λ
(
X
i
)
∩
Y
~
i
=
∅
}
.
\widehat{R}_{n}^{s}(\lambda):=\frac{1}{n}\sum_{i=1}^{n}\mathbf{1}\{\mathcal{T}_{\lambda}(X_{i})\cap\tilde{Y}_{i}=\emptyset\}.
(4)
Since the label space in code generation is high-dimensional and exponentially large, directly enumerating all complete programs is intractable.
Following
Khakhar et al. (2023)
, we construct the prediction set
𝒯
λ
​
(
X
)
\mathcal{T}_{\lambda}(X)
using partial programs, which provide a compact representation of the candidate program set, as mentioned in Section
3
.
The remaining problem is to obtain partial programs for
X
i
X_{i}
accounting for uncertainty in code generation. Given an AST
T
=
(
𝒱
,
ℰ
)
T=(\mathcal{V},\mathcal{E})
and a parameter
λ
k
∈
Λ
\lambda_{k}\in\Lambda
, we introduce a binary variable
β
i
,
v
(
k
)
\beta^{(k)}_{i,v}
for each node
v
∈
𝒱
v\in\mathcal{V}
, where
β
i
,
v
(
k
)
=
1
\beta^{(k)}_{i,v}=1
indicates that
v
v
is removed from
T
T
, and
β
i
,
v
(
k
)
=
0
\beta^{(k)}_{i,v}=0
otherwise.
Let
π
v
∈
ℝ
≥
0
\pi_{v}\in\mathbb{R}_{\geq 0}
denote the negative log probability of
v
v
conditioned on its ancestors, i.e.,
π
v
=
−
log
⁡
ℙ
⁡
(
v
∣
v
1
,
…
,
v
m
)
\pi_{v}=-\log\mathbb{P}(v\mid v_{1},\dots,v_{m})
.
Partial programs can be obtained by optimization. For fixed
k
∈
[
N
]
k\in[N]
and input program
X
i
X_{i}
:
min
⁡
∑
v
∈
𝒱
β
⁡
β
i
,
v
(
k
)
,
s
.
t
.
∑
v
∈
𝒱
π
v
​
(
1
−
β
i
,
v
(
k
)
)
≤
λ
k
.
\min_{\beta}\sum_{v\in\mathcal{V}}\beta^{(k)}_{i,v},~~\mathrm{s.t.}\sum_{v\in\mathcal{V}}\pi_{v}(1-\beta^{(k)}_{i,v})\leq\lambda_{k}.
(5)
In this minimization problem, the goal is to retain as many nodes as possible while ensuring the total uncertainty of the partial programs does not exceed
λ
k
\lambda_{k}
.
Moreover, the solution must satisfy two additional structure constraints derived from ASTs:
(
SC1
)
​
(
β
i
,
v
(
k
)
=
1
)
→
(
β
i
,
v
′
(
k
)
=
1
)
,
\displaystyle\mathrm{(SC1)}~~(\beta^{(k)}_{i,v}=1)\rightarrow(\beta^{(k)}_{i,v^{\prime}}=1),
∀
(
v
,
v
′
)
∈
ℰ
,
\displaystyle\forall(v,v^{\prime})\in\mathcal{E},
(6)
(
SC2
)
​
∑
(
v
,
v
′
)
∈
ℰ
β
i
,
v
′
(
k
)
​
(
1
−
β
i
,
v
(
k
)
)
≤
t
max
,
\displaystyle\mathrm{(SC2)}~\sum_{(v,v^{\prime})\in\mathcal{E}}\beta^{(k)}_{i,v^{\prime}}(1-\beta^{(k)}_{i,v})\leq t_{\max},
where (SC1) enforces tree connectivity and (SC2) imposes an upper-bound
t
max
∈
ℕ
+
t_{\max}\in\mathbb{N}^{+}
on the number of permissible subtree removals.
In contrast to PAC prediction set
(
Khakhar et al., 2023
)
, our optimization problem for constructing partial programs operates under a less restrictive set of constraints. The most significant relaxation is the removal of the monotonicity condition on prediction sets (cf. Eq.(
1
)), which substantially enlarges the feasible label space.
4.2
Multiple Hypothesis Testing for Code
With the structured risk defined above, we then employ multiple hypothesis testing to identify the reject set
Λ
valid
\Lambda_{\mathrm{valid}}
.
The first step of this procedure is to compute a
p
p
-value
p
k
p_{k}
for each null hypothesis
ℋ
k
\mathcal{H}_{k}
.
Since the structured risk defined in Eq.(
4
) is an average of binary losses,
a valid
p
p
-value can be computed by the following lemma.
Lemma 4.1
(Binomial trial
p
p
-values)
.
Let
R
^
n
s
​
(
λ
k
)
\widehat{R}_{n}^{s}(\lambda_{k})
be the empirical structured risk defined in Eq.(
4
), and let
Bin
⁡
(
n
,
α
)
\mathrm{Bin}(n,\alpha)
denote a binomial random variable with
n
n
trials and success probability
α
\alpha
. Then,
p
k
B
​
T
=
e
​
ℙ
​
(
Bin
⁡
(
n
,
α
)
≤
n
​
R
^
n
s
​
(
λ
k
)
)
p_{k}^{BT}=e\mathbb{P}\big(\mathrm{Bin}(n,\alpha)\leq n\widehat{R}_{n}^{s}(\lambda_{k})\big)
(7)
is a valid p-value for
ℋ
k
:
R
s
​
(
λ
k
)
>
α
\mathcal{H}_{k}:R^{s}(\lambda_{k})>\alpha
.
In LTT, let
𝒜
\mathcal{A}
be any FWER-controlling algorithm at level
δ
\delta
.
Applying
𝒜
\mathcal{A}
to the
p
p
-values
{
p
k
B
​
T
}
k
=
1
N
\{p^{BT}_{k}\}_{k=1}^{N}
yields a set of rejected hypotheses, whose corresponding configurations form
Λ
valid
⊆
Λ
\Lambda_{\mathrm{valid}}\subseteq\Lambda
.
If
Λ
valid
=
∅
\Lambda_{\mathrm{valid}}=\emptyset
, the method abstains (i.e., returns
null
).
Otherwise, any parameter in
Λ
valid
\Lambda_{\mathrm{valid}}
can be selected.
In practice, we select the one that empirically minimizes the number of node removals.
Since the number of removals decreases monotonically with
λ
\lambda
, this amounts to choosing
λ
^
=
max
⁡
(
Λ
valid
)
.
\hat{\lambda}=\max(\Lambda_{\mathrm{valid}}).
(8)
Note that the monotonicity here only affects the number of pruned nodes (i.e., the size of prediction sets), which naturally follows from the optimization objective in Section
4.1
.
This is distinct from and weaker than the explicit monotonicity constraint on prediction sets imposed in Eq. (
1
).
Consequently, the parameter
λ
^
\hat{\lambda}
selected by Eq. (
8
), based on
𝒟
cal
\mathcal{D}_{\mathrm{cal}}
, provides a risk-controlling guarantee for the resulting prediction sets.
Algorithm 1
Risk-Controlling Partial Program
1:
Input:
enhanced calibration set
𝒟
cal
=
{
(
X
i
,
Y
~
i
)
}
i
=
1
n
\mathcal{D}_{\mathrm{cal}}=\{(X_{i},\tilde{Y}_{i})\}_{i=1}^{n}
; test program
X
n
+
1
X_{n+1}
; parameters
Λ
=
{
λ
k
}
k
=
1
N
\Lambda=\{\lambda_{k}\}_{k=1}^{N}
; maximum of subtree removals
t
max
t_{\max}
; risk tolerance
α
\alpha
; error level
δ
\delta
;
2:
Output:
partial program
β
n
+
1
,
v
\beta_{n+1,v}
for
X
n
+
1
X_{n+1}
.
3:
for
k
=
1
,
…
,
N
k=1,\dots,N
do
4:
for
i
=
1
,
…
,
n
i=1,\dots,n
do
5:
β
i
,
v
(
k
)
←
\beta^{(k)}_{i,v}\leftarrow
Solve Eqs.(
5
)-(
6
) for
X
i
X_{i}
, given
λ
k
\lambda_{k}
;
6:
end
for
7:
Define
R
^
n
s
​
(
λ
k
)
\widehat{R}_{n}^{s}(\lambda_{k})
using Eq. (
4
);
8:
Compute p-value
p
k
B
​
T
p_{k}^{BT}
for
R
^
n
s
​
(
λ
k
)
\widehat{R}_{n}^{s}(\lambda_{k})
using Eq. (
7
);
9:
end
for
10:
Obtain
Λ
valid
=
𝒜
⁡
(
p
1
B
​
T
,
…
,
p
N
B
​
T
)
\Lambda_{\mathrm{valid}}=\mathcal{A}(p_{1}^{BT},\dots,p_{N}^{BT})
via controlling FWER;
11:
Select
λ
^
=
max
⁡
(
Λ
valid
)
\hat{\lambda}=\max(\Lambda_{\mathrm{valid}})
;
12:
β
n
+
1
,
v
←
\beta_{n+1,v}\leftarrow
Solve Eqs.(
5
)-(
6
) for
X
n
+
1
X_{n+1}
, given
λ
^
\hat{\lambda}
.
Algorithm
1
summarizes how to obtain risk-controlling partial programs via picking desirable
λ
^
\hat{\lambda}
.
This result ensures that the prediction set
𝒯
λ
^
​
(
X
n
+
1
)
\mathcal{T}_{\hat{\lambda}}(X_{n+1})
constructed by these partial programs is also risk-controlling.
Theorem 4.2
(Structured risk-controlling sets)
.
The prediction set
𝒯
λ
^
​
(
X
n
+
1
)
\mathcal{T}_{\hat{\lambda}}(X_{n+1})
, constructed by the partial program from Algorithm
1
, satisfies Eq. (
2
).
To precisely search and test
Λ
\Lambda
in the context of code generation, in Appendix
B
, we discuss three alternative FWER control algorithms:
Bonferroni method
,
Holm–Bonferroni method
(
Holm, 1979
)
, and
fixed sequence testing
(
Bauer, 1991
)
.
4.3
Selective Execution Strategy
As mentioned in Section
3
, code generation is inherently a multi-label problem. The LTT framework supports label augmentation on the calibration set
𝒟
cal
\mathcal{D}_{\mathrm{cal}}
.
For each generation task of
X
i
∈
𝒟
cal
X_{i}\in\mathcal{D}_{\mathrm{cal}}
, we sample additional
m
m
programs from the generative code model and execute test cases to identify correct instances.
Such a sampling and verification step is performed only during calibration, incurring no computational overhead at test time.
Despite this, in scenarios with severely limited computational resources, we propose a selective execution strategy that maintains high-quality labels while improving sampling efficiency.
Given a total of
M
M
sampled programs on
𝒟
cal
\mathcal{D}_{\mathrm{cal}}
, we use program uncertainty scores
{
U
i
}
i
=
1
M
\{U_{i}\}_{i=1}^{M}
(e.g., perplexity) to decide whether executing test cases is necessary.
We learn a threshold
u
^
\hat{u}
such that programs with
U
i
<
u
^
U_{i}<\hat{u}
are directly accepted as correct, while those with
U
i
≥
u
^
U_{i}\geq\hat{u}
are verified by executing test cases.
This strategy does not require perfectly calibrated models, but better calibration can indeed enhance the precision of
u
^
\hat{u}
. Formally, we define the cumulative error function conditioned on
u
u
as
L
(
u
)
=
1
M
∑
i
=
1
M
ℓ
(
S
i
)
𝟏
{
U
i
<
u
}
,
L(u)=\frac{1}{M}\sum_{i=1}^{M}\ell(S_{i})\mathbf{1}\{U_{i}<u\},
where
S
i
∈
{
0
,
1
}
S_{i}\in\{0,1\}
is a true indicator (
1
1
for a correct program,
0
0
otherwise), and
ℓ
⁡
(
S
i
)
=
1
−
S
i
\ell(S_{i})=1-S_{i}
computes the error.
Our goal is to select a threshold
u
u
such that
L
⁡
(
u
)
≤
ϵ
L(u)\leq\epsilon
, where
ϵ
\epsilon
is a label error rate.
However, directly computing
L
⁡
(
u
)
L(u)
by verifying all
M
M
sampled programs is computationally expensive.
To circumvent this, we instead estimate an error upper bound
L
^
u
​
(
γ
)
\hat{L}^{u}(\gamma)
on
L
⁡
(
u
)
L(u)
that holds pointwise with probability
γ
\gamma
, i.e., satisfies the following inequality:
ℙ
⁡
(
L
^
u
​
(
γ
)
≥
L
⁡
(
u
)
)
≥
1
−
γ
.
\mathbb{P}(\hat{L}^{u}(\gamma)\geq L(u))\geq 1-\gamma.
(9)
To compute an approximate error bound
L
^
u
​
(
γ
)
\hat{L}^{u}(\gamma)
, we propose a procedure analogous to importance sampling, inspired by
Candès et al. (2025)
.
We begin by drawing
h
h
indices
{
i
1
,
…
,
i
h
}
\{i_{1},\dots,i_{h}\}
uniformly with replacement from
[
M
]
[M]
.
For each sampled index
i
j
i_{j}
, whether a test-case execution is performed is determined stochastically by a Bernoulli trial
ξ
i
j
∼
Bern
⁡
(
ω
i
j
)
\xi_{i_{j}}\sim\mathrm{Bern}(\omega_{i_{j}})
, where
{
ω
i
}
i
=
1
M
\{\omega_{i}\}_{i=1}^{M}
are predefined sampling weights.
This procedure yields a set
{
Z
j
​
(
u
)
}
j
=
1
h
\{Z_{j}(u)\}_{j=1}^{h}
of
h
h
i.i.d. random variables, defined as
Z
j
(
u
)
=
ℓ
(
S
i
j
)
(
ξ
i
j
/
ω
i
j
)
𝟏
{
U
i
j
≤
u
}
Z_{j}(u)=\ell(S_{i_{j}})(\xi_{i_{j}}/\omega_{i_{j}})\mathbf{1}\{U_{i_{j}}\leq u\}
.
Since
𝔼
⁡
[
ξ
i
j
/
ω
i
j
∣
i
j
]
=
1
\mathbb{E}[\xi_{i_{j}}/\omega_{i_{j}}\mid i_{j}]=1
, the expectation of
Z
j
​
(
u
)
Z_{j}(u)
equals the target quantity
L
⁡
(
u
)
L(u)
. Therefore, an unbiased estimate of
L
⁡
(
u
)
L(u)
can be obtained from the sample mean of
{
Z
j
​
(
u
)
}
j
=
1
h
\{Z_{j}(u)\}_{j=1}^{h}
. An upper confidence bound for
L
⁡
(
u
)
L(u)
is then constructed by Hoeffding’s inequality
(
Hoeffding, 1963
)
, yielding a finite-sample upper bound
L
^
u
​
(
γ
)
=
μ
^
Z
​
(
u
)
+
δ
H
​
B
​
(
γ
)
,
\hat{L}^{u}(\gamma)=\hat{\mu}_{Z}(u)+\delta_{HB}(\gamma),
(10)
where
μ
^
\hat{\mu}
denotes the empirical mean of
{
Z
j
​
(
u
)
}
j
=
1
h
\{Z_{j}(u)\}_{j=1}^{h}
and Hoeffding bound
δ
H
​
B
​
(
γ
)
=
log
⁡
(
2
/
γ
)
/
2
​
h
/
ω
min
\delta_{HB}(\gamma)=\sqrt{\log(2/\gamma)/2h}/\omega_{\mathrm{min}}
, where
ω
min
=
min
⁡
{
ω
i
}
i
=
1
M
\omega_{\mathrm{min}}=\min\{\omega_{i}\}_{i=1}^{M}
.
After obtaining
L
^
u
​
(
γ
)
\hat{L}^{u}(\gamma)
, let
u
^
=
max
⁡
{
u
∈
[
0
,
1
]
:
L
^
u
​
(
γ
)
≤
ϵ
}
\hat{u}=\max\{u\in[0,1]:\hat{L}^{u}(\gamma)\leq\epsilon\}
where
ϵ
∈
(
0
,
1
)
\epsilon\in(0,1)
, and the final predicted label
S
^
i
\hat{S}_{i}
is
S
^
i
=
S
i
𝟏
{
U
i
≥
u
^
}
+
𝟏
{
U
i
<
u
^
}
.
\hat{S}_{i}=S_{i}\mathbf{1}\{U_{i}\geq\hat{u}\}+\mathbf{1}\{U_{i}<\hat{u}\}.
Algorithm
2
describes the selective execution procedure.
We have the following error upper bound.
Lemma 4.3
(Non-asymptotic error upper bound)
.
If the label set
{
S
^
i
}
i
=
1
M
\{\hat{S}_{i}\}^{M}_{i=1}
of sample programs is computed by Algorithm
2
, then it meets Eq. (
9
) and
L
^
u
​
(
γ
)
≤
ϵ
\hat{L}^{u}(\gamma)\leq\epsilon
.
This result provides a non-asymptotic upper bound for
L
⁡
(
u
)
L(u)
, suitable for settings with limited sample sizes (small
M
M
).
Alternatively, an asymptotic bound for large
M
M
is given in Appendix
C
.
Combining Lemma
4.3
and Theorem
4.2
, we obtain the error-controlling guarantee when using the selective execution strategy.
Proposition 4.4
(Approximately risk-controlling sets)
.
Let the output of Algorithm
2
be the calibration set
𝒟
cal
\mathcal{D}_{\mathrm{cal}}
.
Then, the parameter
λ
^
\hat{\lambda}
selected by Eq. (
8
) satisfies
ℙ
⁡
(
R
s
​
(
λ
^
)
≤
α
+
ϵ
⁡
(
1
−
α
)
)
≥
(
1
−
γ
)
⋅
(
1
−
δ
)
.
\mathbb{P}\big(R^{s}(\hat{\lambda})\leq\alpha+\epsilon(1-\alpha)\big)\geq(1-\gamma)\cdot(1-\delta).
Remark 4.5
.
This guarantee presents a practical trade-off, allowing for controlled relaxation of the risk guarantee in exchange for computational savings by permitting a non-zero label error rate
ϵ
\epsilon
.
When
ϵ
=
0
\epsilon=0
,
the result reduces to the original guarantee of Theorem
4.2
.
Algorithm 2
Selective Execution with Error Bound
1:
Input:
unlabeled sampling programs
{
X
i
}
i
=
1
M
\{X_{i}\}_{i=1}^{M}
; uncertainty scores
{
U
i
}
i
=
1
M
\{U_{i}\}_{i=1}^{M}
; test cases
{
C
i
}
i
=
1
M
\{C_{i}\}_{i=1}^{M}
; sampling weights
{
ω
i
}
i
=
1
M
\{\omega_{i}\}_{i=1}^{M}
; sampling size
h
h
; label error rate
ϵ
\epsilon
; confidence level
γ
\gamma
;
2:
Output:
labeled sampling programs
{
X
i
,
S
^
i
}
i
=
1
M
\{X_{i},\hat{S}_{i}\}^{M}_{i=1}
.
3:
for
j
=
1
,
…
,
h
j=1,\dots,h
do
4:
Sample an index
i
j
∼
Unif
⁡
(
[
M
]
)
i_{j}\sim\mathrm{Unif}([M])
;
5:
Sample a random variable
ξ
i
j
∼
Bern
⁡
(
ω
i
j
)
\xi_{i_{j}}\sim\mathrm{Bern}(\omega_{i_{j}})
;
6:
if
ξ
i
j
=
1
\xi_{i_{j}}=1
then
7:
Execute the test case
C
i
j
C_{i_{j}}
to get
S
i
j
S_{i_{j}}
;
8:
Compute the importance-weighted error using
Z
j
=
ℓ
⁡
(
S
i
j
)
/
ω
i
j
Z_{j}=\ell(S_{i_{j}})/\omega_{i_{j}}
;
9:
else
10:
Z
j
=
0
Z_{j}=0
;
11:
end
if
12:
end
for
13:
Given a threshold
u
u
, define
Z
j
(
u
)
=
Z
j
⋅
𝟏
{
U
i
j
≤
u
}
Z_{j}(u)=Z_{j}\cdot\mathbf{1}\{U_{i_{j}}\leq u\}
for
j
∈
[
h
]
j\in[h]
;
14:
Compute error upper bound
L
^
u
​
(
γ
)
\hat{L}^{u}(\gamma)
on
{
Z
j
​
(
u
)
}
i
=
1
h
\{Z_{j}(u)\}_{i=1}^{h}
for all
u
∈
{
U
i
}
i
=
1
M
u\in\{U_{i}\}_{i=1}^{M}
using Eq. (
10
);
15:
Determine
u
^
=
max
⁡
{
u
∈
[
0
,
1
]
:
L
^
u
​
(
γ
)
≤
ϵ
}
\hat{u}=\max\{u\in[0,1]:\hat{L}^{u}(\gamma)\leq\epsilon\}
;
16:
Obtain
S
^
i
=
S
i
𝟏
{
U
i
≥
u
^
}
+
𝟏
{
U
i
<
u
^
}
\hat{S}_{i}=S_{i}\mathbf{1}\{U_{i}\geq\hat{u}\}+\mathbf{1}\{U_{i}<\hat{u}\}
for
i
∈
[
M
]
i\in[M]
.
5
Experiments
Datasets.
We evaluate our approach on three standard Python code generation benchmarks: HumanEval
(
Chen, 2021
)
, MBPP
(
Austin et al., 2021
)
and APPS
(
Hendrycks et al., 2021
)
. HumanEval consists of 164 hand-written programming problems.
We use the sanitized version of the MBPP dataset (nearly 500 problems) as provided by CodeT
(
Chen et al., 2022
)
, and select the introductory-level problems of the APPS dataset (1,000 problems).
Each dataset is then randomly partitioned into calibration and test sets using a 50/50 split.
To mitigate variance from random partitioning, we repeat this process over 100 independent random trials.
Baselines.
We compare our method
RisCoSet
against two state-of-the-art baselines: the PAC prediction set approach
(
Khakhar et al., 2023
)
and its greedy variant.
The PAC baseline constructs partial programs by solving a complex optimization problem, while the greedy baseline iteratively removes the AST node that reduces the partial program’s negative log-likelihood (NLL) the most.
Evaluation metrics.
To evaluate the structured prediction sets
𝒯
λ
^
​
(
X
n
+
1
)
\mathcal{T}_{\hat{\lambda}}(X_{n+1})
produced by our
RisCoSet
, we report two metrics: (1) the percentage of nodes removed from AST, and (2) the coverage of code sets that contain at least one correct program.
We aim to keep node removals small while ensuring that coverage remains above the target threshold
1
−
α
1-\alpha
, thereby preserving more useful program information.
Hyperparameters.
To control risk, the key hyperparameter is the search space for
λ
\lambda
.
We implement a uniform grid search with an increment of 0.02, a simple but effective discretization.
Empirically, we observe that outcomes are insensitive to the exact resolution, as long as the grid density is adequate to capture the operative range of
λ
\lambda
.
We set the maximum subtree removals
t
max
=
1
t_{\max}=1
and the additional sampling quantity
m
=
20
m=20
for label augmentation on the calibration set by default.
For the risk parameter, we fix
δ
=
0.1
\delta=0.1
and vary
α
\alpha
in our experiments.
Implementations.
We evaluate three open-source LLMs: the code-specialized Deepseek-Coder-33B
(
Guo et al., 2024
)
and Qwen2.5-Coder-32B
(
Hui et al., 2024
)
, along with the general-purpose Llama3.1-70B
(
Grattafiori et al., 2024
)
. For all LLMs, we use a sampling temperature of 0.8 and a top-
p
p
of 0.95 by default.
We choose fixed sequence testing as the FWER algorithm for LTT.
Moreover, we solve the optimization problem for generating partial programs using the Z3 solver, enforcing a 24‑second timeout per instance in accordance with SMT‑COMP
1
1
1
SMT‑COMP is the annual international competition for Satisfiability Modulo Theories (SMT) solvers.
rules.
All the experiments are carried out with Python 3.9.19, Pytorch 2.4.0 and vLLM 0.6.1, running on NVIDIA H800 GPUs with CUDA 12.7.
(a)
DeepSeek-Coder on HumanEval
(b)
Qwen2.5-Coder on MBPP
(c)
Llama3.1 on APPS
Figure 2:
Percentage of node removals (top row) and satisfying code sets (bottom row) w.r.t. risk level
α
\alpha
. The results are the mean over 100 random splits.
The smaller node removal is better, when the code set coverage exceeds the target bound
1
−
α
1-\alpha
.
Our approach constructs prediction sets that remove significantly fewer nodes compared to baselines for three LLMs on all datasets.
Figure 3:
Parameter sensitivity analysis of sampling quantity
m
m
w.r.t. risk level
α
\alpha
on MBPP.
The average results over 100 trials show that a larger value of
m
m
leads to fewer node removals, while maintaining the required risk control.
Error
ϵ
\epsilon
0.05
0.1
0.2
0.3
Removal
71.8
50.6
27.8
3.39
Coverage
88.5
82.9
74.1
66.5
(85.5)
(81.0)
(72.0)
(63.0)
Save
12.0
29.4
57.6
84.4
Table 1:
Percentage of node removals (%), coverage of satisfying code set (%), and fraction of calibration data saved from execution (%) w.r.t. label error
ϵ
\epsilon
when
α
=
0.1
\alpha=0.1
on MBPP.
The average results over 100 trials show that the coverage of the satisfying code set is above the target coverage (i.e., the values in ()), and our selective execution strategy effectively reduces the proportion of programs needed to execute.
5.1
Results
Our main results are presented in Fig.
2
.
For all plots, the solid line shows the average values over 100 trials, and the shaded regions indicate the standard deviation. Additional experimental results are reported in Appendix
D
.
Validity of risk-controlling code generation.
We implement our approach
RisCoSet
for different LLMs on three datasets.
The results in Fig.
2
illustrate, with varying risk levels
α
\alpha
, the percentage of nodes removed from the pruned AST (top row) and the coverage of constructed prediction sets that contain a correct program (bottom row).
Our empirical findings align with Theorem
4.2
in practice, as the average code set coverage consistently exceeds the target bound of
1
−
α
1-\alpha
(the dashed lines).
Across all datasets, our method produces prediction sets that remove significantly fewer AST nodes than the baselines.
For instance, as shown in Fig.
2(b)
and Fig.
2(c)
, our approach reduces node removals by 24.5% and 20.3% compared to the best competitor when
α
=
0.15
\alpha=0.15
on the MBPP and APPS datasets, respectively.
Compared to the PAC baseline, the greedy baseline tends to remove more nodes, which is particularly evident on the MBPP dataset in Fig.
2(b)
, due to its greedy pruning strategy.
For the code-specialized models, our approach performs better with Qwen2.5-Coder than with Deepseek-Coder.
This may be attributed to Qwen2.5-Coder’s stronger code generation capability
(
Hui et al., 2024
)
, suggesting that our method can benefit increasingly from more powerful generative models.
Moreover, the proposed method also achieves performance comparable to that of specialized code generators when applied to the general-purpose Llama3.1 in Fig.
2(c)
, showing its scalability for diverse LLMs.
The significant improvement of our method can be attributed to: (1) we define an optimization problem with fewer constraints, encouraging a better partial program solution with more remaining nodes; (2) our multi-label formalization allows for a more complete exploration of the potential correct program space for a specific LLM compared to baselines.
Parameter sensitivity analysis.
We next analyze the sensitivity of our method to the sampling quantity
m
m
.
We sample
m
m
additional programs for each task in the calibration set with
m
=
{
1
,
5
,
20
,
80
}
m=\{1,5,20,80\}
, and pick correct ones as new labels via verification.
The corresponding node removals and code set coverage on the MBPP dataset
are given in Fig.
3
and Fig.
3
.
We observe a clear trend that a larger
m
m
helps reduce the number of pruned AST nodes while preserving the desired risk control.
Insufficient exploration of the label space at
m
=
1
m=1
leads to more node removals.
Nevertheless, the performance gains diminish for
m
>
5
m>5
, demonstrating that our method already performs well with a relatively small sample size.
Selective execution strategy.
We evaluate the effectiveness of the proposed selective execution strategy when
α
=
0.1
\alpha=0.1
and
m
=
80
m=80
on the MBPP dataset.
In experiments, we set confidence level
γ
=
0.01
\gamma=0.01
, sampling size
h
h
as 10% of total sample quantity
M
M
, and samping weights
ω
=
ω
i
=
1.0
\omega=\omega_{i}=1.0
, for any
i
∈
[
M
]
i\in[M]
.
We report the average results with varying label error
ϵ
\epsilon
over 100 trials in Table
1
.
The key metric for efficiency is the percentage of sample programs saved from execution at the cost of
ϵ
%
\epsilon\%
error in program labels.
First, the observed coverage of the satisfying code set always exceeds the target coverage, which controls risks, consistent with the theoretical guarantee in Proposition
4.4
.
Second, our selective execution strategy largely reduces the proportion of verifications by running test cases.
For instance, at
ϵ
=
0.1
\epsilon=0.1
, it avoids test-case execution for nearly 30% of generated programs, substantially lowering computational cost.
6
Related Work
Conformal prediction and risk control.
Conformal Prediction (CP)
(
Vovk et al., 2005
)
is proposed to provide a framework for uncertainty quantification with distribution-free coverage guarantees
(
Angelopoulos et al., 2023
)
.
CP has been applied to a range of tasks, including image classification
(
Sadinle et al., 2019
)
, object detection
(
Teng et al., 2023
)
, and regression prediction
(
Kato et al., 2023
)
.
These traditional CP methods, designed for classification or regression, are ill-suited for generative tasks due to the finite output space.
Therefore, some risk-controlling frameworks are proposed for generation tasks
(
Bates et al., 2021
;
Angelopoulos et al., 2022
)
.
However, these methods, such as PAC prediction sets
(
Park et al., 2020
)
, require an additional monotonicity constraint regarding risk, making them difficult to adapt to multi-label problems.
To this end, the Learn Then Test (LTT) framework
(
Angelopoulos et al., 2025
)
separates model training from statistical validation and uses multiple hypothesis testing to control risk.
Without imposing the monotonicity assumption on the output space, LTT is particularly applicable to multi-label settings like code generation.
Uncertainty estimation on LLMs.
Existing work
(
Kadavath et al., 2022
;
Vasconcelos et al., 2023
)
has shown that the probability scores produced by LLMs may be poorly calibrated.
Current uncertainty calibration methods for LLMs mainly focus on prompting
(
Lin et al., 2022
)
or post-hoc logit calibration (e.g., temperature scaling
(
Guo et al., 2017
)
and self-consistency
(
Zhou et al., 2025
)
), rather than providing theoretical guarantees.
Additionally, recent work has investigated the application of CP to LLMs to achieve rigorous statistical guarantees on the correctness of generated outputs.

One line of work applies it to produce a set of candidate responses that, with high probability, contains a valid answer
(
Kumar et al., 2023
;
Ye et al., 2024
)
.
This task‑level approach, however, has limited practicality because evaluating a large number of candidates is computationally expensive.
Alternatively, sample‑level methods apply conformal prediction internally to a single LLM output, identifying its sound components as a prediction set
(
Quach et al., 2024
;
Cherian et al., 2024
)
.
However, these approaches rely on the assumption of near-independence among components. While this may hold in NLP contexts, it breaks down for structured domains like code, where components are systemically interdependent
(
Casalnuovo et al., 2019
;
Chen et al., 2022
)
.
Reliable code generation.
Ensuring code correctness has long been a central concern in software engineering.
Conventional methods include
testing (e.g., unit testing and fuzzing)
(
Zhu et al., 2022
)
, static analysis
(
Park et al., 2021
)
, and formal verification
(
Baier and Katoen, 2008
)
.
Nevertheless, such methods are inadequate for LLM‑generated code, as they cannot effectively leverage the probabilistic nature and uncertainty of modern language models.
The advancement of LLMs for code generation has spurred interest in reliability methods based on statistical, rather than purely deductive, guarantees
(
Chen et al., 2022
)
.
For example,
Guo et al. (2021)
propose to complete the uncertain code parts within the program
sketches to improve the pass rate.
Recently, research has explored constructing PAC prediction sets for code generation
(
Khakhar et al., 2023
)
.
By representing programs via ASTs and building prediction sets defined by partial programs, this method delivers probabilistic guarantees that the code set contains the ground-truth program.
Different from the previous work, our approach introduces LTT framework to eliminate the need for monotonicity constraints and naturally accommodates the multi-label essence of code.
7
Conclusion
This paper addresses the challenge of unreliable LLM outputs in structured generation tasks like code.
We introduce a method for constructing statistically guaranteed prediction sets by reformulating the problem as multi-label classification, eliminating monotonicity constraints.
Our approach applies the LTT framework to ensure a candidate set of programs contains a correct solution with high probability.
Furthermore, a selective execution strategy is proposed to augment label sets for efficient and effective calibration.
Extensive experiments across multiple models and benchmarks confirm the method’s effectiveness.
While our focus is on code generation,
we believe the proposed method can be adapted to other structured prediction problems.
Limitations.
Our method requires executing test cases to augment labels during calibration, which adds computational overhead relative to sample-free baselines.
However, this overhead is confined to the calibration phase and does not impact inference speed on test data.
To further reduce the cost, we introduce a selective execution strategy that allows a bounded label-error rate in exchange for reduced executions.
The strategy’s effectiveness is supported theoretically (Proposition
4.4
) and shown empirically (cf. Table
1
).
Broader Impact
This paper presents work to advance the field of conformal prediction and code generation. Our work has many potential societal consequences, none of which we feel must be specifically highlighted here.
References
Achiam
et al.
(2023)
J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat,
et al.
Gpt-4 technical report
.
arXiv preprint arXiv:2303.08774
.
Cited by:
§1
.
Angelopoulos
et al.
(2025)
A. N. Angelopoulos, S. Bates, E. J. Candès, M. I. Jordan, and L. Lei
Learn then test: calibrating predictive algorithms to achieve risk control
.
The Annals of Applied Statistics
19
(
2
),
pp. 1641–1662
.
Cited by:
§1
,
§2.2
,
Theorem 2.2
,
§6
.
Angelopoulos
et al.
(2022)
A. N. Angelopoulos, S. Bates, A. Fisch, L. Lei, and T. Schuster
Conformal risk control
.
arXiv preprint arXiv:2208.02814
.
Cited by:
§1
,
§6
.
Angelopoulos
et al.
(2023)
A. N. Angelopoulos S. Bates
et al.
Conformal prediction: a gentle introduction
.
Foundations and Trends® in Machine Learning
16
(
4
),
pp. 494–591
.
Cited by:
§6
.
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le,
et al.
Program synthesis with large language models
.
arXiv preprint arXiv:2108.07732
.
Cited by:
§1
,
§5
.
Baier and Katoen (2008)
C. Baier and J. Katoen
Principles of model checking
.
External Links:
Link
Cited by:
§6
.
Bates
et al.
(2021)
S. Bates, A. Angelopoulos, L. Lei, J. Malik, and M. Jordan
Distribution-free, risk-controlling prediction sets
.
Journal of the ACM (JACM)
68
(
6
),
pp. 1–34
.
Cited by:
§6
.
Bauer (1991)
P. Bauer
Multiple testing in clinical trials
.
Statistics in medicine
10
(
6
),
pp. 871–890
.
Cited by:
Appendix B
,
§4.2
.
Bentkus (2004)
V. Bentkus
On hoeffding’s inequalities
.
Cited by:
§A.1
.
Billingsley (1961)
P. Billingsley
The lindeberg-levy theorem for martingales
.
Proceedings of the American Mathematical Society
12
(
5
),
pp. 788–792
.
Cited by:
§A.5
.
Candès
et al.
(2025)
E. J. Candès, A. Ilyas, and T. Zrnic
Probably approximately correct labels
.
arXiv preprint arXiv:2506.10908
.
Cited by:
§4.3
.
Casalnuovo
et al.
(2019)
C. Casalnuovo, K. Sagae, and P. Devanbu
Studying the difference between natural and programming language corpora
.
Empirical Software Engineering
24
(
4
),
pp. 1823–1868
.
Cited by:
§1
,
§6
.
Chen
et al.
(2022)
B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J. Lou, and W. Chen
Codet: code generation with generated tests
.
arXiv preprint arXiv:2207.10397
.
Cited by:
§1
,
§5
,
§6
,
§6
.
Chen (2021)
M. Chen
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
Cited by:
§5
.
Cherian
et al.
(2024)
J. J. Cherian, I. Gibbs, and E. J. Candès
Large language model validity via enhanced conformal prediction methods
.
External Links:
2406.09714
,
Link
Cited by:
§1
,
§6
.
Dahl
et al.
(2024)
M. Dahl, V. Magesh, M. Suzgun, and D. E. Ho
Large legal fictions: profiling legal hallucinations in large language models
.
Journal of Legal Analysis
16
(
1
),
pp. 64–93
.
Cited by:
§1
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
Cited by:
§5
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
Cited by:
§6
.
Guo
et al.
(2021)
D. Guo, A. Svyatkovskiy, J. Yin, N. Duan, M. Brockschmidt, and M. Allamanis
Learning to complete code with sketches
.
arXiv preprint arXiv:2106.10158
.
Cited by:
§1
,
§6
.
Guo
et al.
(2024)
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. Li,
et al.
DeepSeek-coder: when the large language model meets programming–the rise of code intelligence
.
arXiv preprint arXiv:2401.14196
.
Cited by:
§5
.
Hendrycks
et al.
(2021)
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song,
et al.
Measuring coding challenge competence with apps
.
arXiv preprint arXiv:2105.09938
.
Cited by:
§5
.
Hoeffding (1963)
W. Hoeffding
Probability inequalities for sums of bounded random variables
.
Journal of the American statistical association
58
(
301
),
pp. 13–30
.
Cited by:
§4.3
.
Holm (1979)
S. Holm
A simple sequentially rejective multiple test procedure
.
Scandinavian journal of statistics
,
pp. 65–70
.
Cited by:
Appendix B
,
§4.2
.
Hui
et al.
(2024)
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu,
et al.
Qwen2. 5-coder technical report
.
arXiv preprint arXiv:2409.12186
.
Cited by:
§5.1
,
§5
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. J. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Dodds, N. Dassarma, E. Tran-Johnson, S. Johnston, S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen, Y. Bai, S. Bowman, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion, S. Kravec, L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei, T. B. Brown, J. Clark, N. Joseph, B. Mann, S. McCandlish, C. Olah, and J. Kaplan
Language models (mostly) know what they know
.
ArXiv
abs/2207.05221
.
External Links:
Link
Cited by:
§6
.
Kato
et al.
(2023)
Y. Kato, D. M. Tax, and M. Loog
A review of nonconformity measures for conformal prediction in regression
.
Conformal and probabilistic prediction with applications
,
pp. 369–383
.
Cited by:
§6
.
Khakhar
et al.
(2023)
A. Khakhar, S. Mell, and O. Bastani
PAC prediction sets for large language models of code
.
In
International Conference on Machine Learning
,
pp. 16237–16249
.
Cited by:
§1
,
§2.1
,
§3
,
§4.1
,
§4.1
,
§5
,
§6
.
Kumar
et al.
(2023)
B. Kumar, C. Lu, G. Gupta, A. Palepu, D. Bellamy, R. Raskar, and A. Beam
Conformal prediction with large language models for multi-choice question answering
.
arXiv preprint arXiv:2305.18404
.
Cited by:
§6
.
Lin
et al.
(2022)
S. Lin, J. Hilton, and O. Evans
Teaching models to express their uncertainty in words
.
External Links:
2205.14334
,
Link
Cited by:
§6
.
Liu
et al.
(2024)
F. Liu, Y. Liu, L. Shi, H. Huang, R. Wang, Z. Yang, L. Zhang, Z. Li, and Y. Ma
Exploring and evaluating hallucinations in llm-powered code generation
.
arXiv preprint arXiv:2404.00971
.
Cited by:
§1
,
§1
.
Nadeau
et al.
(2024)
D. Nadeau, M. Kroutikov, K. McNeil, and S. Baribeau
Benchmarking llama2, mistral, gemma and gpt for factuality, toxicity, bias and propensity for hallucinations
.
arXiv preprint arXiv:2404.09785
.
Cited by:
§1
.
Park
et al.
(2021)
J. Park, H. Lee, and S. Ryu
A survey of parametric static analysis
.
ACM Comput. Surv.
54
(
7
).
External Links:
ISSN 0360-0300
,
Link
,
Document
Cited by:
§6
.
Park
et al.
(2020)
S. Park, O. Bastani, N. Matni, and I. Lee
Pac confidence sets for deep neural networks via calibrated prediction
.
In
International Conference on Learning Representations
,
Cited by:
§2.1
,
§2.1
,
§3
,
§6
.
Quach
et al.
(2024)
V. Quach, A. Fisch, T. Schuster, A. Yala, J. H. Sohn, T. S. Jaakkola, and R. Barzilay
Conformal language modeling
.
External Links:
2306.10193
,
Link
Cited by:
§1
,
§6
.
Sadinle
et al.
(2019)
M. Sadinle, J. Lei, and L. Wasserman
Least ambiguous set-valued classifiers with bounded error levels
.
Journal of the American Statistical Association
114
(
525
),
pp. 223–234
.
Cited by:
§6
.
Solar-Lezama (2008)
A. Solar-Lezama
Program synthesis by sketching
.
University of California, Berkeley
.
Cited by:
§1
.
Team
et al.
(2023)
G. Team, R. Anil, S. Borgeaud, J. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican,
et al.
Gemini: a family of highly capable multimodal models
.
arXiv preprint arXiv:2312.11805
.
Cited by:
§1
.
Teng
et al.
(2023)
J. Teng, C. Wen, D. Zhang, Y. Bengio, Y. Gao, and Y. Yuan
Predictive inference with feature conformal prediction
.
In
The Eleventh International Conference on Learning Representations
,
Cited by:
§6
.
Vasconcelos
et al.
(2023)
H. Vasconcelos, G. Bansal, A. Fourney, Q. V. Liao, and J. W. Vaughan
Generation probabilities are not enough: exploring the effectiveness of uncertainty highlighting in ai-powered code completions
.
arXiv preprint arXiv:2302.07248
.
Cited by:
§6
.
Vovk
et al.
(2005)
V. Vovk, A. Gammerman, and G. Shafer
Algorithmic learning in a random world
.
Springer
.
Cited by:
§1
,
§3
,
§6
.
Ye
et al.
(2024)
F. Ye, M. Yang, J. Pang, L. Wang, D. Wong, E. Yilmaz, S. Shi, and Z. Tu
Benchmarking llms via uncertainty quantification
.
Advances in Neural Information Processing Systems
37
,
pp. 15356–15385
.
Cited by:
§6
.
Zhong and Wang (2017)
H. Zhong and X. Wang
Boosting complete-code tool for partial program
.
In
2017 32nd IEEE/ACM International Conference on Automated Software Engineering (ASE)
,
pp. 671–681
.
Cited by:
§1
.
Zhou
et al.
(2025)
Z. Zhou, Y. Tan, Z. Li, Y. Yao, L. Guo, Y. Li, and X. Ma
A theoretical study on bridging internal probability and self-consistency for LLM reasoning
.
In
The Thirty-ninth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§6
.
Zhu
et al.
(2022)
X. Zhu, S. Wen, S. Camtepe, and Y. Xiang
Fuzzing: a survey for roadmap
.
ACM Comput. Surv.
54
(
11s
).
External Links:
ISSN 0360-0300
,
Link
,
Document
Cited by:
§6
.
Appendix A
Proofs
A.1
Proof of Lemma
4.1
Proof.
Let
A
=
Bin
⁡
(
n
,
α
)
A=\mathrm{Bin}(n,\alpha)
and
B
=
n
​
R
^
n
s
​
(
λ
k
)
B=n\widehat{R}_{n}^{s}(\lambda_{k})
. Since the risk in Eq. (
4
) is an average of binary outcomes,
B
B
is also binomial with sample size
n
n
and some (unknown) success probability
α
′
\alpha^{\prime}
.
Let
F
A
F_{A}
and
F
B
F_{B}
denote the CDFs of
A
A
and
B
B
, respectively.
Under the null hypothesis
ℋ
k
:
R
s
​
(
λ
k
)
>
α
\mathcal{H}_{k}:R^{s}(\lambda_{k})>\alpha
on test instances,
we have
α
′
>
α
\alpha^{\prime}>\alpha
.
This implies that
B
B
stochastically dominates
A
A
, i.e.,
F
A
​
(
t
)
≥
F
B
​
(
t
)
F_{A}(t)\geq F_{B}(t)
for all
t
t
.
Let
C
=
p
k
B
​
T
=
e
​
F
A
​
(
B
)
C=p_{k}^{BT}=eF_{A}(B)
, then
ℙ
⁡
(
C
≤
c
)
\displaystyle\mathbb{P}(C\leq c)
=
ℙ
⁡
(
F
A
​
(
B
)
≤
c
e
)
\displaystyle=\mathbb{P}(F_{A}(B)\leq\frac{c}{e})
≤
ℙ
⁡
(
F
B
​
(
B
)
≤
c
e
)
.
\displaystyle\leq\mathbb{P}(F_{B}(B)\leq\frac{c}{e}).
By the definition of a CDF, we have
ℙ
​
(
F
B
​
(
B
)
≤
c
e
)
\displaystyle\mathbb{P}(F_{B}(B)\leq\frac{c}{e})
=
ℙ
⁡
(
B
≤
F
B
−
1
​
(
c
e
)
)
\displaystyle=\mathbb{P}(B\leq F_{B}^{-1}(\frac{c}{e}))
=
F
B
​
(
F
B
−
1
​
(
c
e
)
)
\displaystyle=F_{B}\!\left(F_{B}^{-1}\!\left(\frac{c}{e}\right)\right)
=
c
e
≤
c
.
\displaystyle=\frac{c}{e}\leq c.
Therefore, under
ℋ
k
\mathcal{H}_{k}
,
p
k
B
​
T
p_{k}^{BT}
is super-uniform and hence a valid
p
p
-value.
Furthermore, by Bentkus inequality
(
Bentkus, 2004
)
, we obtain
ℙ
⁡
(
R
^
n
s
​
(
λ
k
)
≤
t
)
≤
e
​
ℙ
​
(
Bin
⁡
(
n
,
α
)
≤
⌈
n
​
t
⌉
)
.
\mathbb{P}(\widehat{R}_{n}^{s}(\lambda_{k})\leq t)\leq e\mathbb{P}\big(\mathrm{Bin}(n,\alpha)\leq\lceil nt\rceil\big).
This inequality is nearly tight and
n
​
t
=
⌈
n
​
t
⌉
nt=\lceil nt\rceil
, because
n
​
R
^
n
s
​
(
λ
k
)
n\widehat{R}_{n}^{s}(\lambda_{k})
is binomial as discussed above.
Therefore,
p
k
B
​
T
p_{k}^{BT}
is a near-tight upper bound for the CDF of
R
^
n
s
​
(
λ
k
)
\widehat{R}_{n}^{s}(\lambda_{k})
.
∎
A.2
Proof of Theorem
4.2
Proof.
Since the enhanced calibration set is i.i.d., the set losses
𝟏
{
𝒯
λ
(
X
i
)
∩
Y
~
i
=
∅
}
\mathbf{1}\{\mathcal{T}_{\lambda}(X_{i})\cap\tilde{Y}_{i}=\emptyset\}
in Eq. (
4
) are also i.i.d.
By Lemma
4.1
, each
p
k
B
​
T
p_{k}^{BT}
is a valid
p
p
-value under the null hypothesis
ℋ
k
:
R
s
​
(
λ
k
)
>
α
\mathcal{H}_{k}:R^{s}(\lambda_{k})>\alpha
.
Given a set-valued function
𝒯
λ
\mathcal{T}_{\lambda}
, and a FWER-controlling algorithm at level
δ
\delta
, we can apply Theorem
2.2
to identify
Λ
valid
\Lambda_{\mathrm{valid}}
such that
ℙ
⁡
(
sup
λ
∈
Λ
valid
{
R
s
​
(
λ
)
}
≤
α
∣
𝒟
cal
)
≥
1
−
δ
\mathbb{P}(\sup_{\lambda\in\Lambda_{\mathrm{valid}}}\{R^{s}(\lambda)\}\leq\alpha\mid\mathcal{D}_{\mathrm{cal}})\geq 1-\delta
on test programs. Therefore, we have
ℙ
⁡
(
R
s
​
(
λ
^
)
≤
α
∣
𝒟
cal
)
≥
1
−
δ
,
\mathbb{P}(R^{s}(\hat{\lambda})\leq\alpha\mid\mathcal{D}_{\mathrm{cal}})\geq 1-\delta,
as Eq. (
3
) holds for any
λ
∈
Λ
valid
\lambda\in\Lambda_{\mathrm{valid}}
.
In particular, it holds for
λ
^
\hat{\lambda}
selected by Eq. (
8
).
∎
A.3
Proof of Lemma
4.3
Proof.
We first analyze the properties of the random variables
Z
j
​
(
u
)
Z_{j}(u)
constructed in Algorithm
2
.
The random variables
Z
1
​
(
u
)
,
…
,
Z
h
​
(
u
)
Z_{1}(u),\dots,Z_{h}(u)
are independent, because index
i
j
i_{j}
is uniformly sampled from
[
M
]
[M]
, and
ξ
i
j
\xi_{i_{j}}
is independent of other random variables.
Since binary loss
ℓ
⁡
(
S
i
j
)
\ell(S_{i_{j}})
is bounded by
[
0
,
1
]
[0,1]
, if
ξ
i
j
=
1
\xi_{i_{j}}=1
, we have
Z
j
=
ℓ
⁡
(
S
i
j
)
ω
i
j
≤
1
min
j
⁡
ω
i
j
=
1
ω
min
.
Z_{j}=\frac{\ell(S_{i_{j}})}{\omega_{i_{j}}}\leq\frac{1}{\min_{j}\omega_{i_{j}}}=\frac{1}{\omega_{\mathrm{min}}}.
If
ξ
i
j
=
0
\xi_{i_{j}}=0
,
Z
j
=
0
Z_{j}=0
.
Let
R
=
1
/
ω
min
R=1/\omega_{\mathrm{min}}
. Then
Z
j
∈
[
0
,
R
]
Z_{j}\in[0,R]
for all
j
∈
[
h
]
j\in[h]
.
We denote
Z
¯
​
(
u
)
=
1
h
​
∑
j
=
1
h
Z
j
​
(
u
)
\bar{Z}(u)=\frac{1}{h}\sum_{j=1}^{h}Z_{j}(u)
, and compute the expected
Z
¯
​
(
u
)
\bar{Z}(u)
as
𝔼
​
[
Z
¯
​
(
u
)
]
\displaystyle\mathbb{E}[\bar{Z}(u)]
=
1
h
​
∑
j
=
1
h
𝔼
⁡
[
Z
j
​
(
u
)
]
\displaystyle=\frac{1}{h}\sum_{j=1}^{h}\mathbb{E}[Z_{j}(u)]
=
1
h
∑
j
=
1
h
[
ω
i
j
⋅
ℓ
⁡
(
S
i
j
)
ω
i
j
𝟏
{
U
i
j
≤
u
}
+
(
1
−
ω
i
j
)
⋅
0
]
\displaystyle=\frac{1}{h}\sum_{j=1}^{h}\Big[\omega_{i_{j}}\cdot\frac{\ell(S_{i_{j}})}{\omega_{i_{j}}}\mathbf{1}\{U_{i_{j}}\leq u\}+(1-\omega_{i_{j}})\cdot 0\Big]
=
1
h
∑
j
=
1
h
ℓ
(
S
i
j
)
𝟏
{
U
i
j
≤
u
}
=
L
(
u
)
.
\displaystyle=\frac{1}{h}\sum_{j=1}^{h}\ell(S_{i_{j}})\mathbf{1}\{U_{i_{j}}\leq u\}=L(u).
By Hoeffding’s inequality and
L
​
(
u
)
=
𝔼
​
[
Z
¯
​
(
u
)
]
L(u)=\mathbb{E}[\bar{Z}(u)]
, we obtain
ℙ
⁡
(
|
μ
^
Z
​
(
u
)
−
L
⁡
(
u
)
|
≥
t
)
≤
2
​
exp
⁡
(
−
2
​
h
​
t
2
R
2
)
,
\mathbb{P}\big(\lvert\hat{\mu}_{Z}(u)-L(u)\rvert\geq t\big)\leq 2\exp\Big(-\frac{2ht^{2}}{R^{2}}\Big),
(11)
where
t
>
0
t>0
is arbitrary.
Setting the right-hand side equal to
γ
\gamma
yields
2
​
exp
⁡
(
−
2
​
h
​
t
2
R
2
)
=
γ
⇒
t
=
R
​
log
⁡
(
2
/
γ
)
2
​
h
.
2\exp\Big(-\frac{2ht^{2}}{R^{2}}\Big)=\gamma\quad\Rightarrow\quad t=R\sqrt{\frac{\log(2/\gamma)}{2h}}.
Substituting this value of
t
t
into Eq.
11
yields
ℙ
⁡
(
μ
^
Z
​
(
u
)
−
L
⁡
(
u
)
≤
−
R
​
log
⁡
(
2
/
γ
)
2
​
h
)
≤
γ
2
≤
γ
.
\mathbb{P}\Big(\hat{\mu}_{Z}(u)-L(u)\leq-R\sqrt{\frac{\log(2/\gamma)}{2h}}\Big)\leq\frac{\gamma}{2}\leq\gamma.
Equivalently,
ℙ
⁡
(
L
⁡
(
u
)
≤
μ
^
Z
​
(
u
)
+
R
​
log
⁡
(
2
/
γ
)
2
​
h
)
≥
1
−
γ
.
\mathbb{P}\Big(L(u)\leq\hat{\mu}_{Z}(u)+R\sqrt{\frac{\log(2/\gamma)}{2h}}\Big)\geq 1-\gamma.
Let
L
^
u
​
(
γ
)
=
μ
^
Z
​
(
u
)
+
R
​
log
⁡
(
2
/
γ
)
/
2
​
h
\hat{L}^{u}(\gamma)=\hat{\mu}_{Z}(u)+R\sqrt{\log(2/\gamma)/2h}
. Then
ℙ
⁡
(
L
⁡
(
u
)
≤
L
^
u
​
(
γ
)
)
≥
1
−
γ
,
\mathbb{P}(L(u)\leq\hat{L}^{u}(\gamma))\geq 1-\gamma,
which completes the proof.
∎
A.4
Proof of Proposition
4.4
Proof.
We prove Proposition
4.4
.
In Section
4.3
, we select
u
^
=
max
⁡
{
u
∈
[
0
,
1
]
:
L
^
u
​
(
γ
)
≤
ϵ
}
\hat{u}=\max\{u\in[0,1]:\hat{L}^{u}(\gamma)\leq\epsilon\}
, and by Lemma
4.3
we have the following upper bound:
L
⁡
(
u
)
≤
L
^
u
​
(
γ
)
=
ϵ
.
L(u)\leq\hat{L}^{u}(\gamma)=\epsilon.
(12)
According to Theorem
4.2
, for a test instance
(
X
n
+
1
,
Y
n
+
1
)
(X_{n+1},Y_{n+1})
, we have
OPEN
ℙ
⁡
(
ℙ
⁡
(
𝒯
λ
^
​
(
X
n
+
1
)
∩
Y
n
+
1
=
∅
)
≤
α
)
)
≥
1
−
δ
.
\mathbb{P}\big(\mathbb{P}(\mathcal{T}_{\hat{\lambda}}(X_{n+1})\cap Y_{n+1}=\emptyset)\leq\alpha)\big)\geq 1-\delta.
In this guarantee, let
Y
n
+
1
=
Y
n
+
1
t
∪
Y
n
+
1
f
Y_{n+1}=Y_{n+1}^{t}\cup Y_{n+1}^{f}
, where
Y
n
+
1
t
Y_{n+1}^{t}
and
Y
n
+
1
f
Y_{n+1}^{f}
are disjoint sets and
|
Y
n
+
1
t
|
/
|
Y
n
+
1
|
≥
1
−
ϵ
\lvert Y_{n+1}^{t}\lvert/\lvert Y_{n+1}\lvert\geq 1-\epsilon
according to Eq. (
12
).
For any element
y
∈
Y
n
+
1
y\in Y_{n+1}
, we assume
y
∈
𝒯
λ
^
​
(
X
n
+
1
)
y\in\mathcal{T}_{\hat{\lambda}}(X_{n+1})
independently with equal probability
p
p
. Then,
ℙ
(
𝒯
λ
^
(
X
n
+
1
)
∩
Y
n
+
1
=
∅
)
=
(
1
−
p
)
|
Y
n
+
1
|
≤
α
,
\mathbb{P}(\mathcal{T}_{\hat{\lambda}}(X_{n+1})\cap Y_{n+1}=\emptyset)=(1-p)^{\lvert Y_{n+1}\lvert}\leq\alpha,
Consequently,
ℙ
⁡
(
𝒯
λ
^
​
(
X
n
+
1
)
∩
Y
n
+
1
t
=
∅
)
\displaystyle\mathbb{P}(\mathcal{T}_{\hat{\lambda}}(X_{n+1})\cap Y_{n+1}^{t}=\emptyset)
=
(
1
−
p
)
|
Y
n
+
1
t
|
=
(
(
1
−
p
)
|
Y
n
+
1
|
)
|
Y
n
+
1
t
|
|
Y
n
+
1
|
\displaystyle=(1-p)^{\lvert Y_{n+1}^{t}\lvert}=\Big((1-p)^{\lvert Y_{n+1}\lvert}\Big)^{\frac{\lvert Y_{n+1}^{t}\lvert}{\lvert Y_{n+1}\lvert}}
≤
α
1
−
ϵ
≤
1
−
(
1
−
α
)
​
(
1
−
ϵ
)
\displaystyle\leq\alpha^{1-\epsilon}\leq 1-(1-\alpha)(1-\epsilon)
=
α
+
ϵ
⁡
(
1
−
α
)
\displaystyle=\alpha+\epsilon(1-\alpha)
holds with probability at least
(
1
−
γ
)
⋅
(
1
−
δ
)
(1-\gamma)\cdot(1-\delta)
(since the bounds involving
ϵ
\epsilon
and
α
\alpha
hold with probabilities at least
1
−
γ
1-\gamma
and
1
−
δ
1-\delta
, respectively).
Additionally, we use the Bernoulli inequality for
α
,
ϵ
∈
(
0
,
1
)
\alpha,\epsilon\in(0,1)
in the last inequality.
∎
A.5
Proof of Proposition
C.1
Proof.
Let
h
h
be the number of sample programs from LLMs.
By the Lindeberg–Feller central limit theorem
(
Billingsley, 1961
)
, we obtain
h
​
(
L
⁡
(
u
)
−
μ
^
Z
​
(
u
)
)
σ
Z
​
(
u
)
→
𝒩
⁡
(
0
,
1
)
\frac{\sqrt{h}(L(u)-\hat{\mu}_{Z}(u))}{\sigma_{Z}(u)}\rightarrow\mathcal{N}(0,1)
as
h
→
∞
h\rightarrow\infty
, since the
Z
j
​
(
u
)
Z_{j}(u)
are i.i.d.
By the weak law of large numbers, we have
σ
^
Z
​
(
u
)
→
𝑝
σ
Z
​
(
u
)
,
\hat{\sigma}_{Z}(u)\xrightarrow{p}\sigma_{Z}(u),
and thus,
an application of Slutsky’s theorem gives
ℙ
⁡
(
L
​
(
u
)
−
μ
^
Z
​
(
u
)
σ
^
Z
2
​
(
u
)
/
h
≤
z
1
−
γ
)
→
1
−
γ
,
\mathbb{P}\Big(\frac{L(u)-\hat{\mu}_{Z}(u)}{\sqrt{\hat{\sigma}^{2}_{Z}(u)/h}}\leq z_{1-\gamma}\Big)\rightarrow 1-\gamma,
because
z
1
−
γ
z_{1-\gamma}
is the
(
1
−
γ
)
(1-\gamma)
-quantile of the standard normal distribution.
Equivalently, when
h
h
approaches positive infinity, we have
ℙ
⁡
(
L
⁡
(
u
)
≤
μ
^
Z
​
(
u
)
+
z
1
−
γ
​
σ
^
Z
2
​
(
u
)
/
h
)
→
1
−
γ
,
\mathbb{P}\Big(L(u)\leq\hat{\mu}_{Z}(u)+z_{1-\gamma}\sqrt{\hat{\sigma}^{2}_{Z}(u)/h}\Big)\rightarrow 1-\gamma,
which completes the proof.
∎
Appendix B
FWER-controlling algorithm
After obtaining valid p-values by Eq. (
7
), we discuss procedures for computing
Λ
valid
=
𝒜
⁡
(
p
1
B
​
T
,
…
,
p
N
B
​
T
)
\Lambda_{\mathrm{valid}}=\mathcal{A}(p_{1}^{BT},\dots,p_{N}^{BT})
on structured risks.
Since evaluating multiple hypotheses simultaneously increases the chance of false positives, we require family-wise error rate (FWER) correction.
Definition B.1
.
(FWER control) Let
𝒜
⁡
(
p
1
B
​
T
,
…
,
p
N
B
​
T
)
\mathcal{A}(p_{1}^{BT},\dots,p_{N}^{BT})
be an algorithm that outputs a subset
Λ
valid
⊆
Λ
\Lambda_{\mathrm{valid}}\subseteq\Lambda
. We say
𝒜
\mathcal{A}
controls the FWER at
(
α
,
δ
)
(\alpha,\delta)
-level if
ℙ
⁡
(
sup
λ
∈
Λ
valid
ℙ
⁡
(
R
s
​
(
λ
)
≤
α
)
)
≥
1
−
δ
,
\mathbb{P}\Big(\sup_{\lambda\in\Lambda_{\mathrm{valid}}}\mathbb{P}(R^{s}(\lambda)\leq\alpha)\Big)\geq 1-\delta,
where the supremum over
∅
\emptyset
is defined as
−
∞
-\infty
.
We provide three alternative FWER-controlling algorithms: the
Bonferroni method
, the
Holm–Bonferroni method
(
Holm, 1979
)
, and
fixed sequence testing
(
Bauer, 1991
)
.
The Bonferroni method defines
Λ
valid
:=
{
λ
k
∣
p
k
B
​
T
≤
δ
/
N
}
k
=
1
N
\Lambda_{\mathrm{valid}}:=\{\lambda_{k}\mid p_{k}^{BT}\leq\delta/N\}_{k=1}^{N}
.
The Holm–Bonferroni method is an improved version of the Bonferroni method.
It sorts p-values as
p
(
1
)
≤
⋯
≤
p
(
N
)
p_{(1)}\leq\dots\leq p_{(N)}
and
Λ
valid
:=
{
λ
(
1
)
,
…
,
λ
(
k
)
}
\Lambda_{\mathrm{valid}}:=\{\lambda_{(1)},\dots,\lambda_{(k)}\}
, where
k
∈
[
N
]
k\in[N]
is the minimum index satisfying
p
(
k
)
≤
δ
/
(
N
−
k
+
1
)
p_{(k)}\leq\delta/(N-k+1)
and
p
(
k
+
1
)
>
δ
/
(
N
−
k
)
p_{(k+1)}>\delta/(N-k)
.
For fixed sequence testing, we leverage the prior knowledge that partial programs with more nodes removed correspond to larger prediction sets.
This implies that smaller values of
λ
\lambda
are more likely to satisfy the target risk.
In the extreme case where
λ
=
0
\lambda=0
, the partial program prunes the entire tree, trivially achieving a risk of zero in Eq. (
4
).
Therefore, a heuristic correction strategy is to test
λ
\lambda
in increasing order and stop at the first accepted hypothesis.
To broaden the search, this process can be repeated from different predefined starting points (e.g., a coarse uniform grid in
Λ
\Lambda
).
Let the parameter set
Λ
=
{
λ
1
,
…
,
λ
N
}
\Lambda=\{\lambda_{1},\dots,\lambda_{N}\}
be in descending order (i.e.,
λ
1
≥
⋯
≥
λ
N
\lambda_{1}\geq\dots\geq\lambda_{N}
). The full fixed sequence testing procedure for code is summarized in Algorithm
3
.
Algorithm 3
Fixed sequence testing
1:
Input:
parameter set
Λ
=
{
λ
1
,
…
,
λ
N
}
\Lambda=\{\lambda_{1},\dots,\lambda_{N}\}
; error level
δ
∈
(
0
,
1
)
\delta\in(0,1)
; p-values
{
p
k
B
​
T
}
k
=
1
N
\{p_{k}^{BT}\}_{k=1}^{N}
; predefined starting points
ℐ
⊂
[
N
]
\mathcal{I}\subset[N]
;
2:
Output:
reject set
Λ
valid
\Lambda_{\mathrm{valid}}
.
3:
Initialize a reject set
Λ
valid
=
∅
\Lambda_{\mathrm{valid}}=\emptyset
;
4:
for
k
∈
ℐ
k\in\mathcal{I}
do
5:
if
λ
k
∉
Λ
valid
\lambda_{k}\notin\Lambda_{\mathrm{valid}}
then
⊳
\triangleright
Avoid duplicates
6:
while
p
k
B
​
T
≤
δ
/
|
ℐ
|
p_{k}^{BT}\leq\delta/\lvert\mathcal{I}\rvert
do
7:
Λ
valid
=
Λ
valid
∪
{
λ
k
}
\Lambda_{\mathrm{valid}}=\Lambda_{\mathrm{valid}}\cup\{\lambda_{k}\}
;
8:
k
=
k
−
1
k=k-1
;
9:
end
while
10:
end
if
11:
end
for
Appendix C
Asymptotic upper bound based on CLT
In addition to the non-asymptotic error upper bound used in Lemma
4.3
, we also consider an asymptotic bound for settings where the number of sampled programs
M
M
is large.
In Section
4.3
, we estimate an unbiased upper bound for
L
⁡
(
u
)
L(u)
by constructing a confidence interval for the average of
{
Z
j
​
(
u
)
}
j
=
1
h
\{Z_{j}(u)\}_{j=1}^{h}
.
Based on the central limit theorem (CLT), we obtain the following asymptotic upper bound.
Proposition C.1
(Asymptotic upper bound)
.
Given a threshold
u
u
and the sample size
h
h
, let
Z
j
​
(
u
)
Z_{j}(u)
be the i.i.d. random variables defined in Algorithm
4
for
j
∈
[
h
]
j\in[h]
.
Define the error upper bound based on CLT as
L
^
u
​
(
γ
)
:=
μ
^
Z
​
(
u
)
+
z
1
−
γ
⋅
σ
^
Z
​
(
u
)
h
,
\hat{L}^{u}(\gamma):=\hat{\mu}_{Z}(u)+z_{1-\gamma}\cdot\frac{\hat{\sigma}_{Z}(u)}{\sqrt{h}},
where
μ
^
\hat{\mu}
and
σ
^
\hat{\sigma}
denote the empirical mean and standard deviation of
{
Z
j
​
(
u
)
}
j
=
1
h
\{Z_{j}(u)\}_{j=1}^{h}
, respectively, and
z
1
−
γ
z_{1-\gamma}
is the
(
1
−
γ
)
(1-\gamma)
-quantile of the standard normal distribution.
Then, we have
lim
inf
m
→
∞
⁡
ℙ
⁡
(
L
⁡
(
u
)
≤
L
^
u
​
(
γ
)
)
≥
1
−
γ
.
\mathop{\lim\inf}\limits_{m\rightarrow\infty}\mathbb{P}(L(u)\leq\hat{L}^{u}(\gamma))\geq 1-\gamma.
The proof is provided in Appendix
A.5
, and the overall procedure is described in Algorithm
4
.
Algorithm 4
Selective Verification with Asymptotic Error Bound
1:
Input:
unlabeled sampling programs
{
X
i
}
i
=
1
M
\{X_{i}\}_{i=1}^{M}
; uncertainty scores
{
U
i
}
i
=
1
M
\{U_{i}\}_{i=1}^{M}
; test cases
{
C
i
}
i
=
1
M
\{C_{i}\}_{i=1}^{M}
; sampling weights
{
ω
i
}
i
=
1
M
\{\omega_{i}\}_{i=1}^{M}
; sampling size
h
h
; confidence level
γ
\gamma
;
2:
Output:
error upper bound
L
^
u
​
(
γ
)
\hat{L}^{u}(\gamma)
.
3:
for
j
=
1
,
…
,
h
j=1,\dots,h
do
4:
Sample an index
i
j
∼
Unif
⁡
(
[
M
]
)
i_{j}\sim\mathrm{Unif}([M])
;
5:
Sample a random variable
ξ
i
j
∼
Bern
⁡
(
ω
i
j
)
\xi_{i_{j}}\sim\mathrm{Bern}(\omega_{i_{j}})
;
6:
if
ξ
i
j
=
1
\xi_{i_{j}}=1
then
7:
Run the test case
C
i
j
C_{i_{j}}
to get
S
i
j
S_{i_{j}}
;
8:
Compute the importance-weighted error using
Z
j
=
ℓ
⁡
(
S
i
j
)
/
ω
i
j
Z_{j}=\ell(S_{i_{j}})/\omega_{i_{j}}
;
9:
else
10:
Z
j
=
0
Z_{j}=0
;
11:
end
if
12:
end
for
13:
Given a threshold
u
u
, define
Z
j
(
u
)
=
Z
j
⋅
𝟏
{
U
i
j
≤
u
}
Z_{j}(u)=Z_{j}\cdot\mathbf{1}\{U_{i_{j}}\leq u\}
for
j
∈
[
h
]
j\in[h]
;
14:
μ
^
Z
​
(
u
)
←
1
h
​
∑
j
=
1
h
Z
j
​
(
u
)
\hat{\mu}_{Z}(u)\leftarrow\frac{1}{h}\sum_{j=1}^{h}Z_{j}(u)
;
15:
σ
^
Z
​
(
u
)
←
1
h
​
∑
j
=
1
h
(
Z
j
​
(
u
)
−
μ
^
Z
​
(
u
)
)
2
\hat{\sigma}_{Z}(u)\leftarrow\sqrt{\frac{1}{h}\sum_{j=1}^{h}(Z_{j}(u)-\hat{\mu}_{Z}(u))^{2}}
;
16:
z
1
−
γ
←
z_{1-\gamma}\leftarrow
(
1
−
γ
)
(1-\gamma)
-quantile of the standard normal distribution;
17:
L
^
u
​
(
γ
)
←
μ
^
Z
​
(
u
)
+
z
1
−
γ
⋅
σ
^
Z
​
(
u
)
h
\hat{L}^{u}(\gamma)\leftarrow\hat{\mu}_{Z}(u)+z_{1-\gamma}\cdot\frac{\hat{\sigma}_{Z}(u)}{\sqrt{h}}
.
(a)
Coverage distribution
(b)
Sensitivity analysis on
t
max
t_{\max}
(c)
Sensitivity analysis on
t
max
t_{\max}
Figure 4:
Fig.
4(a)
is the distribution of code set coverage over 100 trials for three different FWER algorithms, respectively; Fig.
4(b)
and
4(c)
are parameter sensitivity results of maximum subtree removals
t
max
t_{\max}
w.r.t risk level
α
\alpha
.
These experiments are conducted on MBPP.
Table 2:
Performance of our method with different FWER algorithms when
α
=
0.1
\alpha=0.1
. The results are the average over 100 random splits. The smaller node removal is better, when the code set coverage exceeds the 0.9.
FWER alg.
Bf
HBf
FST
Removal
87.9
±
3.1
87.9{\scriptstyle\pm 3.1}
87.0
±
3.3
87.0{\scriptstyle\pm 3.3}
82.3
±
1.9
82.3{\scriptstyle\pm 1.9}
Coverage
94.7
±
2.2
94.7{\scriptstyle\pm 2.2}
94.4
±
2.3
94.4{\scriptstyle\pm 2.3}
92.1
±
1.3
92.1{\scriptstyle\pm 1.3}
Appendix D
Additional Results
D.1
Different FWER-controlling algorithm
To evaluate the performance of different FWER algorithms on our method, we plot the distribution of code set coverage (
α
=
0.1
\alpha=0.1
) as a violin plot over 100 random splits of MBPP in Fig.
4(a)
, and list the mean results in Table.
2
.
The results demonstrate that compared to fixed sequence testing (FST), Bonferroni (Bf) and Holm–Bonferroni (HBf) methods are more conservative and remove more nodes, as confirmed by the results in Table
2
.
This indicates the importance of program prior knowledge used in FST.
D.2
Parameter sensitivity analysis on
t
max
t_{\max}
We next perform parameter sensitivity analysis on the maximum subtree removals
t
max
t_{\max}
.
The results on MBPP are shown in Fig.
4(b)
and Fig.
4(c)
.
We observe that the best result is achieved when
t
max
=
1
t_{\max}=1
, and
t
max
≥
2
t_{\max}\geq 2
leads to more node removals than
t
max
=
1
t_{\max}=1
.
A plausible explanation is that when models are not well-calibrated, a larger
t
max
t_{\max}
distributes pruned nodes and may lead to localized errors that cannot be fully corrected.
D.3
Sample outputs
Figure 5:
An illustrative example from HumanEval. The top part is a correct code snippet, and the bottom part is a generated but incorrect one.
RisCoSet
removes one node in the AST, resulting a prediction set (i.e., a partial program) that contains the correct program.
Figure 6:
An illustrative example from APPS. The left part is a correct code snippet, and the right part is a generated but incorrect one.
RisCoSet
removes seven nodes in the AST, resulting a prediction set (i.e., a partial program) that contains the correct program.
Figure 7:
An illustrative example from APPS. The top part is a correct code snippet, and the bottem part is a generated but incorrect one.
RisCoSet
removes three nodes in the AST (we omit the overlapping AST structures for brevity), resulting a prediction set (i.e., a partial program) that contains the correct program.
langley00