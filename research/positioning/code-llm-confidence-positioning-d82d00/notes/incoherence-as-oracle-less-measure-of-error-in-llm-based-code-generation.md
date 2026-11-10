---
title: Incoherence as Oracle-less Measure of Error in LLM-Based Code Generation
id: incoherence-as-oracle-less-measure-of-error-in-llm-based-code-generation
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:10:31.078196Z'
updated: '2026-11-09T23:27:44.659848Z'
source: https://arxiv.org/html/2507.00057
source_domain: arxiv.org
fetched_at: '2026-11-09T23:10:31.077812Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Valentin et al. 2025 (arXiv 2507.00057): incoherence, probability that two
  sampled programs differ on I/O, lower-bounds error; 16 LLMs on MBPP and HumanEval;
  nonzero incoherence detects 69% (MBPP) and 66% (HumanEval) of nonzero errors with
  no false positives. FULL TEXT. Verdict: L1 close sampling-based occupant; cited
  by ESE paper.'
---

*Suggested by [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]] — cited as Valentin et al. 2025 incoherence oracle-less code correctness*

Incoherence as Oracle-less Measure of Error in LLM-Based Code Generation
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2507.00057v2 [cs.PL] 13 Dec 2025
Incoherence as Oracle-less Measure of Error in LLM-Based Code Generation
Thomas Valentin
Ardi Madadi
Gaetano Sapia
Marcel Böhme
Abstract
Generating code from a natural language programming task is one of the most successful applications of Large Language Models (LLMs). Yet, the generated program may be buggy. Without an oracle, such as an existing, correct implementation or a formal specification, can we somehow estimate how likely the generated program is correct?
In this paper, we propose a measure of incorrectness, called
incoherence
, that can be estimated efficiently in the absence of an oracle and allows us to establish a lower bound on the error, i.e., the probability that the LLM-generated program for that specification is incorrect.
In our experiments, our incoherence-based methodology can automatically identify about two-thirds of incorrect programs without reports of false positives for the average task.
In fact,
an oracle-based evaluation of LLMs can be reliably replaced by an incoherence-based evaluation
. In particular, we find a very strong agreement between the ranking of LLMs by the number of programs deemed correct via an oracle (pass@1) and the ranking of LLMs by the number of programs deemed correct via incoherence.
1
ENS Paris-Saclay, France
2
Max Planck Institute for Security and Privacy, Germany
thomas.valentin@ens-paris-saclay.fr, {ardi.madadi, gaetano.sapia, marcel.boehme}@mpi-sp.org
Data & analysis
—
https://github.com/mpi-softsec/difftrust
Extended version
—
https://arxiv.org/abs/2507.00057
1
Introduction
LLMs have demonstrated remarkable performance on code generation tasks. Yet, confabulation remains a key concern. Models often produce syntactically correct but functionally incorrect code, raising the critical question of when such outputs can be trusted.
For instance,
Fan et al. (2023)
found that the vast majority of auto-generated programs for easy to medium LeetCode programming tasks are incorrect and explain that 57% of those do not even properly implement the task (“algorithmic misalignment”) while another 19% can only be fixed by changing multiple different code locations (multi-hunk).
Pearce et al. (2025)
analyzed code generated in scenarios relevant to high-risk cybersecurity weaknesses and found that 40% of the 1.7k LLM-generated programs actually contain security vulnerabilities.
While ground truth implementations or regression test suites provide a post-hoc evaluation of the generated code, they are often unavailable in real-world deployments, motivating the need for
correctness proxies
—that is, mechanisms that can flag potential failures without external supervision.
Can we estimate how likely an LLM-generated program is correct in the absence of an oracle?
Our work continues a recent stream of works addressing the confabulation problem using the
disagreement
between independently sampled responses to detect untruthful or erroneous outputs
(
Manakul et al. 2023
;
Friel and Sanyal 2023
;
Li et al. 2024
;
Farquhar et al. 2024
)
. A high disagreement indicates a high factual inconsistency.
However, existing measures of disagreement provide
no guarantees
; they are fundamentally heuristic in nature.
Crucially, they can struggle to distinguish between confidently incorrect answers and correct answers generated under uncertainty—especially in complex structured domains like code, where semantics are hard to capture and where correctness is binary and unambiguous.
Figure 1:
Rankings of 16 LLMs on the two most popular code generation benchmarks, MBPP and HumanEval. “Rank 1” indicates the highest probability of producing correct programs.
X-axis
: Ranking in terms of
[
1
−
pass@1
]
[1-\texttt{pass@1}]
(i.e., the proportion of tasks with non-zero empirical error).
Y-axis
: Ranking in terms of the proportion of tasks with non-zero empirical incoherence. Note that incoherence can be estimated in the absence of a ground truth implementation.
Our key insight is that—in the domain of code—the disagreement between independently sampled solutions for a task can be interpreted
semantically
: if two LLM-generated programs behave differently on the same input, at least one must be incorrect.
If the two programs behave identically across a representative input distribution, we gain empirical confidence in their correctness. This enables a shift from heuristic proxies to semantically grounded ones.
In this work, we formalize this intuition. We argue that incoherence, i.e., the behavioral divergence across samples, is a principled and theoretically justified proxy for model error. Concretely, given an LLM and a programming task
d
d
, we call the probability that any two programs generated to implement
d
d
are functionally different as the LLM’s
incoherence
on
d
d
. If we are also given a ground truth implementation
f
d
∗
f^{\ast}_{d}
for
d
d
, we call the probability that
f
d
∗
f^{\ast}_{d}
and a program generated to implement
d
d
are functionally different as the LLM’s
error
on
d
d
.
We note that the widely-used
pass@1
score
(
Chen et al. 2021
;
Liu et al. 2023
)
on a benchmark set can be written in terms of the empirical error (i.e., the error’s maximum likelihood estimate) on each task.
We develop a probabilistic framework that establishes a lower bound on the model’s error in terms of incoherence. In contrast to prior work that relies on shallow patterns or internal model metrics, our approach directly leverages the one setting where semantic equivalence is exactly observable: executable code.
In experiments with 16 state-of-the-art LLMs and two popular code generation benchmarks, our incoherence measure, which requires
no
ground truth implementation, works incredibly well as a substitute for
pass@1
. Figure
1
shows rankings of those LLMs, both in terms of the proportion of tasks with non-zero empirical error (i.e.,
[
1
−
pass@1
]
[1-\texttt{pass@1}]
) and the proportion of tasks with non-zero empirical incoherence. These rankings very strongly agree despite the absence of oracles for our incoherence measure (
ρ
≥
0.92
\rho\geq 0.92
).
We also find that a non-zero incoherence effectively detects about two-thirds of the non-zero errors in the absence of a ground truth implementation (69% and 66% detection rate on MBPP and HumanEval, resp.). No false positives. In cases where the incoherence is zero, the mean error is substantially lower than the average. If we increase the number of generated programs for a programming task 5-fold (from 10 to 50), the detection rate further increases by eight (8) percentage points—of course, at the cost of a 5-fold increase in monetary expenses for additional queries to the LLM.
Contributions:
1.
We propose
incoherence
, a formal, unsupervised proxy for correctness that lower-bounds LLM error.
2.
We develop a probabilistic framework linking incoherence to pass@1, with PAC-style efficiency guarantees.
3.
Our study shows, incoherence detects errors reliably and yields rankings that agree with oracle-based evaluations.
4.
We release all code, results, and analysis scripts.
2
Background
Code generation is a primary application of LLMs in software engineering
(
Hou et al. 2024
)
. Tools like Copilot have seen widespread adoption, with over 40 million installations. Today, even general-purpose LLMs are competitive coders
(
Leaderboards 2025
)
. In June 2025, nearly 25% of the 7.5 trillion tokens on
(
OpenRouter.ai 2025
)
were coding-related.
Jiang et al. (2024)
highlight that
trustworthiness
is essential for LLM adoption in programming. Yet, LLMs are prone to generating incorrect code. How can correctness be validated without ground truth? Existing work addresses factuality in text by sampling multiple responses and measuring internal consistency—e.g., SelfCheckGPT
(
Manakul et al. 2023
)
, ChainPoll
(
Friel and Sanyal 2023
)
, and semantic entropy approaches
(
Farquhar et al. 2024
)
. These methods cluster outputs and estimate confidence based on entropy or token overlap. For code generation, variants include HonestCoder
(
Li et al. 2024
)
, which uses syntax and data-flow modalities, and functional equivalence methods using symbolic execution
(
Sharma and David 2025
)
. However, these approaches are fundamentally heuristic and lack formal guarantees. Their reliance on patterns or output similarity do not capture semantic correctness.
Mahmud et al. (2025)
are interested in generating the most likely correct program for a task, and propose to select from a pool of candidates generated by multiple LLMs that program which best aligns with consensus, where consensus is defined both syntactically and semantically.
Our work addresses the
oracle problem
in software testing
(
Barr et al. 2015
)
. While runtime crashes are detectable via sanitizers
(
Serebryany et al. 2012
)
, functional correctness is domain-specific and often unobservable. We address this problem by viewing the generated program as a random variable and using incoherence as a proxy for correctness.
3
Defining Error and Incoherence
We consider the task of automatically generating a program from a natural language specification. Formally, given a textual description
d
d
of a programming task, a code generation system
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
—treated as a black-box stochastic process—samples a program
π
∼
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\pi\sim\mathsf{Coder}(d)
intended to satisfy the task description
d
d
. Our objective is to assess the correctness of these programs
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
without supervision, reference solutions, or access to model internals.
3.1
Notation
We write
ℙ
⁡
(
⋅
)
\mathbb{P}(\cdot)
for probability and
𝔼
⁡
[
⋅
]
\mathbb{E}[\cdot]
for expectation, leaving the underlying probability space implicit. For any expression
expr
involving random variables,
ℙ
⁡
(
expr
)
\mathbb{P}(\textit{expr})
denotes the probability of the corresponding event. We use
𝕀
⁡
(
expr
)
\mathbb{I}(\textit{expr})
for the indicator function, which is
1
1
when
expr
holds and
0
0
otherwise.
We denote by
𝖣𝖾𝗌𝖼𝗋
\mathsf{Descr}
the set of textual function descriptions and by
𝖯𝗋𝗈𝗀
\mathsf{Prog}
be the set of programs that define a function.
Let
⟦
⋅
⟧
\llbracket\cdot\rrbracket
denote the operational semantics such that for all
π
∈
𝖯𝗋𝗈𝗀
\pi\in\mathsf{Prog}
,
⟦
π
⟧
\llbracket\pi\rrbracket
represents the function defined by
π
\pi
. We refer to
⟦
π
⟧
\llbracket\pi\rrbracket
as the functional interpretation of
π
\pi
.
3.2
Error of a Code Generation System
We model a code generation system
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
as a function that maps each task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
to a corresponding (unknown) distribution over
𝖯𝗋𝗈𝗀
\mathsf{Prog}
. Formally, for all
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
:
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\displaystyle\mathsf{Coder}(d)
:
π
∈
𝖯𝗋𝗈𝗀
↦
p
π
d
∈
[
0
,
1
]
\displaystyle:\pi\in\mathsf{Prog}\mapsto p_{\pi}^{d}\in[0,1]
(1)
where
p
π
d
p_{\pi}^{d}
is the probability of obtaining
π
\pi
when querying
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
with task
d
d
. A program sampled from
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
for the task
d
d
is thus modelled by a random variable that follows the
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
distribution:
Π
d
∼
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
.
\displaystyle\Pi^{d}\sim\mathsf{Coder}(d).
(2)
For every task description
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
, we assume there exist an input set
𝖨𝗇𝗉𝗎𝗍
d
\mathsf{Input}_{d}
, an output set
𝖮𝗎𝗍𝗉𝗎𝗍
d
\mathsf{Output}_{d}
and a correct (deterministic) ground truth implementation
π
d
∗
∈
𝖯𝗋𝗈𝗀
\pi^{\ast}_{d}\in\mathsf{Prog}
with its functional interpretation
f
d
∗
:=
⟦
π
d
∗
⟧
f^{\ast}_{d}:=\llbracket\pi^{\ast}_{d}\rrbracket
such that
f
d
∗
:
𝖨𝗇𝗉𝗎𝗍
d
→
𝖮𝗎𝗍𝗉𝗎𝗍
d
f^{\ast}_{d}:\mathsf{Input}_{d}\to\mathsf{Output}_{d}
.
The
pass@1
score
(
Chen et al. 2021
)
is a standard metric to evaluate the performance of
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
.
For a finite set of tasks
S
⊂
𝖣𝖾𝗌𝖼𝗋
S\subset\mathsf{Descr}
,
pass@1
is defined as the expected fraction of sampled programs that are functionally equivalent to the ground truth implementation:
pass@1
​
(
S
)
:=
𝔼
⁡
[
1
|
S
|
​
∑
d
∈
S
𝕀
⁡
(
⟦
Π
d
⟧
=
f
d
∗
)
]
.
\displaystyle\text{{pass@1} }(S):=\mathbb{E}\left[\frac{1}{|S|}\sum_{d\in S}\mathbb{I}\bigl(\llbracket\Pi^{d}\rrbracket=f^{\ast}_{d}\bigr)\right].
(3)
We define the
functional error
of
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
on task
d
d
as the complement of
pass@1
computed for a single task
d
d
, i.e., the probability that the generated program is not functionally equivalent to the ground truth:
ℰ
⁡
(
d
)
:=
ℙ
⁡
(
⟦
Π
d
⟧
≠
f
d
∗
)
=
1
−
pass@1
​
(
{
d
}
)
.
\Err(d):=\mathbb{P}\left(\llbracket\Pi^{d}\rrbracket\neq f^{\ast}_{d}\right)=1-\text{{pass@1} }(\{d\}).
(4)
This definition captures the natural notion of error.
Moreover, we introduce a
probabilistic interpretation of correctness
with respect to (w.r.t.) a distribution of inputs. Rather than asking whether the generated function is correct for
all
inputs, which is undecidable due to Rice’s theorem, we ask whether it is correct for a
typical input
, drawn from a distribution that represents expected usage. We use this probabilistic interpretation of correctness to introduce a pointwise notion of the error such that
a non-zero pointwise error implies a non-zero functional error
(cf. Eq. (
4
)).
We model an input generation system
𝖦𝖾𝗇
\mathsf{Gen}
as a function that maps each task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
to an (unknown) probability distribution over the corresponding input set
𝖨𝗇𝗉𝗎𝗍
d
\mathsf{Input}_{d}
. This distribution might represent how the program is executed under a typical workload. Formally, for all
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
:
𝖦𝖾𝗇
⁡
(
d
)
\displaystyle\mathsf{Gen}(d)
:
x
∈
𝖨𝗇𝗉𝗎𝗍
d
↦
p
x
d
∈
[
0
,
1
]
\displaystyle:x\in\mathsf{Input}_{d}\mapsto p_{x}^{d}\in[0,1]
(5)
where
p
x
d
p_{x}^{d}
intuitively models how likely is a function for
d
d
to be called on input
x
∈
𝖨𝗇𝗉𝗎𝗍
d
x\in\mathsf{Input}_{d}
.
We define the
pointwise error
of
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
w.r.t.
𝖦𝖾𝗇
\mathsf{Gen}
for any task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
as
ℰ
𝖦𝖾𝗇
⁡
(
d
)
:=
ℙ
⁡
(
⟦
Π
d
⟧
​
(
X
)
≠
f
d
∗
​
(
X
)
)
\Err_{\mathsf{Gen}}(d):=\mathbb{P}(\llbracket\Pi^{d}\rrbracket(X)\neq f^{\ast}_{d}(X))
(6)
where
X
∼
𝖦𝖾𝗇
⁡
(
d
)
X\sim\mathsf{Gen}(d)
.
While the functional error can be computed only by verification of functional equivalence (an undecidable problem), the pointwise error can be estimated efficiently (c.f. Appendix
C.1
)—
in the presence of the oracle
f
d
∗
f^{\ast}_{d}
.
We note that a non-zero pointwise error implies a non-zero functional error, i.e.,
(
ℰ
𝖦𝖾𝗇
⁡
(
d
)
>
0
)
⟹
(
ℰ
⁡
(
d
)
>
0
)
.
\displaystyle\left(\Err_{\mathsf{Gen}}(d)>0\right)\implies(\Err(d)>0).
(7)
Our pointwise error
ℰ
𝖦𝖾𝗇
⁡
(
d
)
\Err_{\mathsf{Gen}}(d)
models the practical reality that a program might be correct on almost all inputs that are empirically observed when the program is tested, deployed, or used in practice.
By evaluating the probability of failure on a representative input distribution, the pointwise error provides a meaningful and practical estimate of the model’s reliability in practical scenarios.
The pointwise error also formalizes the experimental setup originally proposed and now widely used to estimate
pass@1
(i.e., the complement of the mean functional error on a fixed set of programming tasks) using a fixed set of random test cases
(
Chen et al. 2021
;
Liu et al. 2023
)
.
4
Incoherence of a Code Generation System
Our core challenge is to estimate the pointwise error
ℰ
𝖦𝖾𝗇
⁡
(
d
)
\Err_{\mathsf{Gen}}(d)
in the absence of the oracle
f
d
∗
f^{\ast}_{d}
, i.e., without supervision. We aim to achieve this using only observations from sampled implementations, without relying on any internal details of
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
.
To this end, we specialize the disagreement-based hallucination detection approach
(
Manakul et al. 2023
)
to the domain of code generation. The precise definition of the (probabilistic) correctness of a program w.r.t. an oracle (i.e., a ground truth implementation) provides us with the unique opportunity to formalize the approach and to introduce actual
probabilistic guarantees
.
We define the
pointwise incoherence
of
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
w.r.t. an input generation system
𝖦𝖾𝗇
\mathsf{Gen}
and a task
d
d
as the probability that two independently sampled programs produce different outputs on a generated input, i.e.,
ℐ
𝖦𝖾𝗇
⁡
(
d
)
:=
ℙ
⁡
(
⟦
Π
1
d
⟧
​
(
X
)
≠
⟦
Π
2
d
⟧
​
(
X
)
)
\Inc_{\mathsf{Gen}}(d):=\mathbb{P}\left(\llbracket\Pi^{d}_{1}\rrbracket(X)\neq\llbracket\Pi^{d}_{2}\rrbracket(X)\right)\\
(8)
where
Π
1
d
,
Π
2
d
​
∼
i
​
i
​
d
​
𝖢𝗈𝖽𝖾𝗋
​
(
d
)
\Pi^{d}_{1},\Pi^{d}_{2}\overset{iid}{\sim}\mathsf{Coder}(d)
are two independently sampled programs and
X
∼
𝖦𝖾𝗇
⁡
(
d
)
X\sim\mathsf{Gen}(d)
is an input sampled from
𝖦𝖾𝗇
\mathsf{Gen}
for task
d
d
.
This quantity captures the model’s internal uncertainty as revealed through behavioral divergence. Crucially,
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\Inc_{\mathsf{Gen}}(d)
is fully observable and efficient to estimate without an oracle (see Appendix
C.2
).
In the following, we show that this notion of pointwise incoherence provides a rigorous lower bound on the pointwise error and that it can be efficiently estimated.
In Appendix
D
, we develop the notion of functional incoherence and establish a lower bound on the functional error in terms of the functional incoherence in parallel.
4.1
Lower Bound on Error in Terms of Incoherence
The pointwise incoherence provides a lower bound on the pointwise error. Intuitively, if two programs disagree on an input, at least one must be wrong; therefore, the probability of disagreement places a floor on the probability of failure.
Theorem 4.1
(Pointwise Incoherence Inequality)
.
∀
𝖦𝖾𝗇
,
∀
d
∈
𝖣𝖾𝗌𝖼𝗋
,
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≤
2
×
ℰ
𝖦𝖾𝗇
⁡
(
d
)
.
\forall\mathsf{Gen},\forall d\in\mathsf{Descr},\quad\Inc_{\mathsf{Gen}}(d)\leq 2\times\Err_{\mathsf{Gen}}(d).
Proof.
See Appendix
B
.
∎
This result establishes
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\Inc_{\mathsf{Gen}}(d)
as a sound and theoretically grounded proxy for estimating model error on
d
d
. Unlike heuristic confidence or divergence metrics based on representation-level similarity,
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\Inc_{\mathsf{Gen}}(d)
directly, precisely, and formally captures observable functional disagreement.
Crucially, an error detection method based on our incoherence metric
never produces false positives
. The inequality guarantees that if the model has zero pointwise error on a task—i.e.,
ℰ
𝖦𝖾𝗇
⁡
(
d
)
=
0
\Err_{\mathsf{Gen}}(d)=0
—then its pointwise incoherence must also be zero:
ℐ
𝖦𝖾𝗇
⁡
(
d
)
=
0
\Inc_{\mathsf{Gen}}(d)=0
. This property distinguishes it from all previously proposed unsupervised proxies, which may still flag “uncertainty” even when outputs are correct.
4.2
Incoherence is Efficiently Estimated
A key advantage of incoherence as a surrogate for correctness is that it can be estimated efficiently and without access to ground-truth implementations. In this section, we formalize this claim by showing that both the pointwise incoherence and the decision problem of detecting non-zero incoherence admit simple, sample-efficient Monte Carlo estimators with standard PAC-style guarantees.
Theorem 4.2
(PAC Estimation)
.
There exists a randomized algorithm that, given parameters
δ
>
0
\delta>0
,
ϵ
>
0
\epsilon>0
, code generator
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
, input generator
𝖦𝖾𝗇
\mathsf{Gen}
, and task
d
∈
D
d\in D
, computes
ℐ
¯
𝖦𝖾𝗇
​
(
d
)
\bar{\Inc}_{\mathsf{Gen}}(d)
such that
ℙ
⁡
(
|
ℐ
¯
𝖦𝖾𝗇
​
(
d
)
−
ℐ
𝖦𝖾𝗇
⁡
(
d
)
|
≤
ϵ
)
≥
1
−
δ
\mathbb{P}(|\bar{\Inc}_{\mathsf{Gen}}(d)-\Inc_{\mathsf{Gen}}(d)|\leq\epsilon)\geq 1-\delta
using at most
⌈
log
⁡
(
2
/
δ
)
2
​
ϵ
2
⌉
\left\lceil\frac{\log(2/\delta)}{2\epsilon^{2}}\right\rceil
samples.
A similar theorem for the pointwise error, the randomized algorithms using Monte Carlo estimation, and the proofs for both theorems using a trivial application of Hoeffdings inequality are postponed to Appendix
C.1
&
C.2
.
If we are only interested in the decision problem using a boolean interpretation of correctness, a detection method offers a statistically sound and substantially more sample-efficient means to certify that
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
generates correct programs for a task
d
d
w.r.t. a well-specified usage distribution.
Theorem 4.3
(PAC Detection)
.
There exists a randomized algorithm that, given parameters
δ
>
0
\delta>0
,
ϵ
>
0
\epsilon>0
, code generator
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
, input generator
𝖦𝖾𝗇
\mathsf{Gen}
, and task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
, returns
true
if a disagreement is observed and
false
otherwise, such that:
•
If the algorithm returns
true
:
ℐ
𝖦𝖾𝗇
⁡
(
d
)
>
0
\Inc_{\mathsf{Gen}}(d)>0
.
•
If the algorithm returns
false
:
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≤
ϵ
\Inc_{\mathsf{Gen}}(d)\leq\epsilon
with probability at least
1
−
δ
1-\delta
,
using at most
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
\left\lceil\frac{\log(\delta)}{\log(1-\epsilon)}\right\rceil
samples.
A randomized algorithm based on Monte Carlo estimation and the proof is provided in Appendix
C.3
.
Implication for Error Detection.
Although the algorithm described in Theorem
4.3
is designed to detect
non-zero incoherence
, we can use it to infer the presence of
non-zero error
due to the theoretical bound established in Theorem
4.1
, which states:
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≤
2
⋅
ℰ
𝖦𝖾𝗇
⁡
(
d
)
.
\Inc_{\mathsf{Gen}}(d)\leq 2\cdot\Err_{\mathsf{Gen}}(d).
This implies that any task
d
d
for which
ℐ
𝖦𝖾𝗇
⁡
(
d
)
>
0
\Inc_{\mathsf{Gen}}(d)>0
must satisfy:
ℰ
𝖦𝖾𝗇
⁡
(
d
)
>
0
.
\Err_{\mathsf{Gen}}(d)>0.
Therefore, when the PAC detection algorithm returns
true
with high probability, we can conclude that the error rate is also bounded away from zero. This provides a conservative but sound certificate of model error without requiring access to a reference implementation.
5
Practical Considerations
5.1
Fixed Sampling Budget for
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
In theory, pointwise incoherence can be estimated efficiently. The estimator defined by Equation (
8
) is easy to implement, parallelizable, and statistically robust. Voth incoherence estimation and detection admit PAC guarantees with low sample complexity (cf. Thm.
4.2
, Thm.
4.3
).
In practice, however, the primary bottleneck in large-scale evaluation is not sampling from the input distribution
𝖦𝖾𝗇
\mathsf{Gen}
, which is typically inexpensive, but generating programs from
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
, which typically requires querying an LLM. This cost can be substantial, especially when applied across a large set of tasks
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
.
To reduce this cost, we adopt a fixed sampling budget strategy: given a budget
m
m
, we draw
m
m
programs
𝖯𝗋𝗈𝗀
m
=
⟨
π
1
,
…
,
π
m
⟩
\mathsf{Prog}_{m}=\langle\pi_{1},\ldots,\pi_{m}\rangle
once from
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
and define an empirical code generator
𝖢𝗈𝖽𝖾𝗋
m
​
(
d
)
\mathsf{Coder}_{m}(d)
as the uniform distribution over these programs:
𝖢𝗈𝖽𝖾𝗋
m
​
(
d
)
:=
Uniform
​
(
𝖯𝗋𝗈𝗀
m
)
.
\mathsf{Coder}_{m}(d):=\text{Uniform}(\mathsf{Prog}_{m}).
This empirical generator approximates the original distribution
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
while avoiding repeated expensive LLM queries at test time. As
m
m
increases,
𝖢𝗈𝖽𝖾𝗋
m
​
(
d
)
\mathsf{Coder}_{m}(d)
converges to
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
in distribution, and the resulting estimates of incoherence become more faithful.
While this approximation introduces some additional variance, it is highly effective in practice. It amortizes LLM sampling costs across many evaluations, enabling scalable incoherence and error estimation. Experimentally, we find that a larger
m
m
consistently yields more reliable estimates.
5.2
Test Input Generation to Implement
𝖦𝖾𝗇
\mathsf{Gen}
Automatic software test input generation is a well-studied problem in the software engineering community.
Cast as a
constraint satisfaction problem
, we can use symbolic execution to generate inputs that exercise the different paths of a program
(
King 1976
)
or that reveal a difference between two program versions
(
Böhme et al. 2013
)
.
Cast as an
optimization problem
, we can use heuristic search to generate inputs that maximize code coverage
(
Ferguson and Korel 1996
)
.
For our purposes, we propose to use
fuzzing
, an approach that mutates a set of user-provided or auto-generated seed inputs to generate new inputs. Today, fuzzing is the most successful and most widely-deployed automatic testing technique in practice
(
Böhme et al. 2021a
)
. Like random test input generation, fuzzing is amenable to
statistical guarantees
, e.g., to quantify the probability of finding a bug with the next generated input in an ongoing testing campaign that has found no bugs
(
Böhme 2019
;
Böhme 2018
;
Böhme et al. 2021b
;
Lee and Böhme 2026
;
Lee and Böhme 2025
;
Lee and Böhme 2023
)
.
In fact, fuzzing has recently been proposed specifically to improve the soundness of the evaluation of LLM-based code generators on the HumanEval and MBPP benchmarks
(
Liu et al. 2023
)
, where
pass@1
(i.e., mean error across all benchmark tasks) was traditionally computed using five test inputs per task
(
Chen et al. 2021
)
. The technique EvalPlus constructs the input distributions
𝖦𝖾𝗇
\mathsf{Gen}
in two stages:
1.
Seed Corpus Generation
: An LLM is prompted with the specification (or the ground truth implementation) to produce a set of canonical input examples.
2.
Type-Aware Mutation
: These examples are mutated using transformations that preserve the input types but introduce variation (e.g., altering values, shuffling list contents, varying string formats).
We observe that Stage 1 might introduce a bias where an LLM’s generated code might appear to perform better on inputs generated by the same LLM, compared to inputs generated by another LLM. Hence, in our experiments, to provide a fair evaluation of all considered LLMs, we mitigate that potential bias by using the benchmark-provided test inputs as seed inputs. In practice, in the absence of existing test inputs, we suggest using the original method or discovering the seed corpus using greybox fuzzings
(
Zalewski 2014
)
.
6
Experimental Setup
6.1
Research Questions
Our study aims to answer the following research questions.
•
RQ.1 (Effectiveness)
.
How effectively can errors be detected using incoherence alone without an oracle?
What is the average error when incoherence is zero?
How strong is the relationship between incoherence and error?
•
RQ.2 (Agreement)
.
Does the result of an incoherence-based evaluation agree with the result of an error-based evaluation of LLMs?
•
RQ.3 (Ablation)
. How do incoherence and error vary as a function of a) the number of synthesized programs, b) the number of generated inputs, or c) the temperature?
6.2
Models and Datasets
Claude 4 Opus (2025/05/14)
Claude 4 Sonnet (2025/05/14)
DeepSeek-Coder R1
DeepSeek-V3 (0324)
Gemini 2.0 Flash Lite
Gemini 2.5 Pro (preview 05/06)
Gemini 2.5 Flash (preview 05/20)
GPT-3.5 Turbo
GPT-4
GPT-4 Turbo
GPT-4o
GPT-o4 Mini
LLaMA 3.1 8B Instruct
LLaMA 3.3 70B Instruct
LLaMA 4 Maverick 17B
Ministral 8B
Table 1:
Large Language Models used in our experiments.
Models
.
Table
1
shows the large language models (LLMs) used in our experiments. At the time of writing, these 16 LLMs represent the most successful LLMs for code generation according to several popular leaderboards
(
Leaderboards 2025
)
. They also represent the current portfolio of the most popular LLM vendors: Anthropic, DeepSeek, Google, Meta, Mistral, and OpenAI.
By default, we chose a
temperature of 0.6
, a value commonly used in prior work on code generation
(
Li et al. 2024
;
DeepSeek-AI et al. 2025
)
. We vary the temperature parameter in the ablation study (RQ3).
Datasets
. We evaluate our measures of incoherence and error using the 16 LLMs on two (2) popular code generation benchmarks: HumanEval
(
Ji et al. 2025
)
and MBPP (Mostly Basic Python Problems)
(
Hu et al. 2025
)
.
HumanEval
is a human-written benchmark published by OpenAI in 2021, consisting of 164 programming tasks.
MBPP
is a crowd-sourced benchmark published by Google in 2022. We used the author-sanitized version of MBPP containing 426 hand-verified programming tasks.
For every task, they offer
•
a natural language description of the task
d
d
,
•
a ground-truth Python implementation
f
d
∗
f^{\ast}_{d}
, and
•
an average of 7.7 (and 3) Python test inputs for HumanEval (and MBPP, respectively).
6.3
Variables and Measures
Given a code generator
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
and input generator
𝖦𝖾𝗇
\mathsf{Gen}
, programming task
d
d
, a query budget
m
m
and a testing budget
n
n
, the
empirical error
ℰ
^
​
(
d
,
m
,
n
)
\hat{\Err}(d,m,n)
on
d
d
as estimator of the pointwise error is computed as
ℰ
^
​
(
d
,
m
,
n
)
=
1
n
​
∑
i
=
1
n
𝕀
⁡
(
⟦
π
y
i
d
⟧
​
(
x
i
d
)
≠
f
d
∗
​
(
x
i
d
)
)
\hat{\Err}(d,m,n)=\frac{1}{n}\sum_{i=1}^{n}\mathbb{I}\bigl(\llbracket\pi^{d}_{y_{i}}\rrbracket(x^{d}_{i})\neq f^{\ast}_{d}(x^{d}_{i})\bigr)
(9)
and the
empirical incoherence
ℐ
^
​
(
d
,
m
,
n
)
\hat{\Inc}(d,m,n)
on
d
d
as estimator of the pointwise incoherence is computed as
ℐ
^
​
(
d
,
m
,
n
)
=
1
n
​
∑
i
=
1
n
𝕀
⁡
(
⟦
π
y
i
d
⟧
​
(
x
i
d
)
≠
⟦
π
y
i
′
d
⟧
​
(
x
i
d
)
)
\hat{\Inc}(d,m,n)=\frac{1}{n}\sum_{i=1}^{n}\mathbb{I}\bigl(\llbracket\pi^{d}_{y_{i}}\rrbracket(x_{i}^{d})\neq\llbracket\pi^{d}_{y^{\prime}_{i}}\rrbracket(x_{i}^{d})\bigr)
(10)
where
π
1
d
,
…
,
π
m
d
\pi^{d}_{1},...,\pi^{d}_{m}
are sampled from
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
,
x
1
d
,
…
,
x
n
d
x_{1}^{d},...,x_{n}^{d}
are sampled from
𝖦𝖾𝗇
⁡
(
d
)
\mathsf{Gen}(d)
and
y
1
,
…
,
y
n
,
y
1
′
,
…
,
y
n
′
y_{1},...,y_{n},y^{\prime}_{1},...,y^{\prime}_{n}
are sampled from
Uniform
​
(
{
1
,
…
,
m
}
)
\text{Uniform}(\{1,...,m\})
.
Given the set of programming tasks
S
S
, we can now write the
empirical
pass@1
score in terms of the empirical error (cf. Eq. (
4
)):
1
−
1
|
S
|
​
∑
d
∈
S
𝕀
⁡
(
0
≠
ℰ
^
​
(
d
,
1
,
n
)
)
\displaystyle 1-\frac{1}{|S|}\sum_{d\in S}\mathbb{I}\bigl(0\neq\hat{\Err}(d,1,n)\bigr)
(11)
The
mean empirical error
ℰ
¯
​
(
S
,
m
,
n
)
\bar{\Err}(S,m,n)
is
∑
d
∈
S
ℰ
^
​
(
d
,
m
,
n
)
|
S
|
\sum_{d\in S}\frac{\hat{\Err}(d,m,n)}{|S|}
while the
mean empirical incoherence
ℐ
¯
​
(
S
,
m
,
n
)
\bar{\Inc}(S,m,n)
is computed as
∑
d
∈
S
ℐ
^
​
(
d
,
m
,
n
)
|
S
|
\sum_{d\in S}\frac{\hat{\Inc}(d,m,n)}{|S|}
.
The
detection rate
is the proportion of tasks with non-
zero emp. error that have a non-zero empirical incoherence, i.e.,
1
|
S
x
|
​
∑
d
∈
S
x
𝕀
⁡
(
0
≠
ℐ
^
​
(
d
,
m
,
n
)
)
\frac{1}{|S_{x}|}\sum_{d\in S_{x}}\mathbb{I}\bigl(0\neq\hat{\Inc}(d,m,n)\bigr)
where
S
x
=
{
d
|
d
∈
S
∧
ℰ
^
​
(
d
,
m
,
n
)
≠
0
}
S_{x}=\{d\ |\ d\in S\wedge\hat{\Err}(d,m,n)\neq 0\}
.
The
undetected mean empirical error
is the mean empirical error of tasks with zero empirical incoherence, i.e.,
1
|
S
u
|
​
∑
d
∈
S
u
ℰ
^
​
(
d
,
m
,
n
)
\frac{1}{|S_{u}|}\sum_{d\in S_{u}}\hat{\Err}(d,m,n)
where
S
u
=
{
d
|
d
∈
S
∧
ℐ
^
​
(
d
,
m
,
n
)
=
0
}
S_{u}=\{d\ |\ d\in S\wedge\hat{\Inc}(d,m,n)=0\}
.
We measure the
strength of the relationship
between two random variables, i.e., empirical incoherence and error, using Spearman’s rank correlation coefficient
ρ
\rho
.
We measure the
agreement on ranking
when sorting the performance of LLMs measured by the proportion of programming tasks (a) with zero mean empirical error versus (b) with zero mean empirical incoherence, also using Spearman’s rank correlation coefficient.
6.4
Implementation
For each task, we generate
m
m
candidate functions per coder (default
m
=
10
m=10
), using vendor APIs. Inputs are generated via mutation-based fuzzing (
n
=
1000
n=1000
by default). We estimate both error (w.r.t. ground truth
f
d
∗
f^{*}_{d}
) and incoherence (between candidates), with all executions sandboxed (60s timeout). Experiments ran on AMD EPYC 7713P CPU (128 threads), 251 GB RAM. More details in Appendix
A
.
7
Empirical Results
RQ-1. Effectiveness
Mean
Mean
Spearman
Detection
Undetected
LLM
Error
Incoherence
Correlation
Rate
Mean Error
MBPP
Code
0.2960
0.0995
0.5276
0.6866
0.2071
General
0.2773
0.1123
0.6105
0.7243
0.1638
Small
0.3741
0.1641
0.5892
0.7037
0.2107
Mean
0.3009
0.1203
0.5621
0.6857
0.1866
Human
Eval
Code
0.0763
0.0295
0.7171
0.7188
0.0417
General
0.0927
0.0483
0.7181
0.7042
0.0460
Small
0.1585
0.0911
0.7282
0.7381
0.0737
Mean
0.1050
0.0560
0.6861
0.6616
0.0471
Table 2:
Performance of 3 LLMs on 2 benchmarks.
The
mean
is reported across all 16 LLMs;
Code
= Gemini 2.5 Pro,
General
= Gpt–4o, and
Small
= Ministral 8b.
Table
2
shows the results for across all 16 LLMs (mean) and for three representative models (code, general, and small) for both code generation benchmarks. Table 4 (appendix) shows the results for all 16 LLMs. The measures in the header row are discussed in Section
6.3
. Figure
2
shows a scatter plot illustrating the relationship between error and incoherence.
Results
. A non-zero incoherence
effectively
detects a non-zero error without access to a ground truth implementation. The mean detection rate across all 16 LLMs for MBPP and HumanEval are 69% and 66%, respectively. There does not seem to be a substantial difference in detection rate between the code-generation specific LLM (Gemini 2.5 Pro) and the general-purpose or the small LLM (GPT-4o, Mistral 8b).
In cases where the incoherence is zero, the mean error is also substantially lower. Concretely, the mean error reduces from 30% to 19% for MBPP and from 11% to 5% for HumanEval (“Undetected Mean Error”). For the small LLM, the mean error is generally higher than for the other LLMs, but the percentage decrease when incoherence is zero is similar.
Figure
2
best illustrates the relationship between error and incoherence. We can clearly see the consequence of the inequality in Theorem
4.1
. Error is usually greater than incoherence for a programming task. There are some tasks (on the left of each plot) where incoherence is zero but the error is non-zero.
For the average LLM, we find a
moderate correlation
between error and incoherence (0.56 for MBPP; 0.69 for HumanEval). In Table
2
, for the three LLMs evaluated on HumanEval, we even find a
strong correlation
(gt. 0.7).
RQ-1
.
A non-zero incoherence effectively detects about two-thirds of the non-zero errors in the absence of a ground truth implementation. In cases where the incoherence is zero, the mean error is substantially lower than the average. The plot of error and incoherence provides empirical confirmation for our inequality.
Figure 2:
Relationship between error and incoherence for GPT-4o on MBPP and HumanEval benchmarks. The dashed line demonstrates the inequality in Theorem
4.1
.
RQ-2. Agreement on LLM Ranking
If the incoherence- and error-based rankings of LLMs agree, we can reliably substitute one measure for the other. We could remove the requirement to provide painstakingly manually-written ground-truth implementations for every programming task when constructing new code generation benchmarks. We could
mitigate critical threats to validity
in benchmarking of new LLM-based code generation systems, such as overfitting or data leakage.
Figure
1
(on the title page) shows a scatter plot of the ranking of all 16 LLMs in terms of the number of projects with zero error (i.e.,
pass@1
; cf. Eqn. (
3
)) versus the ranking of the same LLMs in terms of the number of projects with our non-zero oracle-less incoherence measure.
Results
. We observe a
very strong agreement
on the rankings. Concretely,
ρ
=
0.92
\rho=0.92
and
ρ
=
0.94
\rho=0.94
for MBPP and HumanEval, respectively, at a significance level
p
<
0.0001
p<0.0001
. The rankings are close to the diagonal.
RQ-2
.
An oracle-based evaluation can be reliably substituted by an incoherence-based evaluation.
Specifically, there is a
very strong agreement
between the rankings of LLMs in terms of the proportion of programming tasks that are considered correct (a) via the lack of a pointwise difference with a ground truth implementation (as in,
pass@1
) versus (b) via the lack of a pointwise difference between two randomly generated solutions.
MBPP
HumanEval
Expenses
Detection
Expenses
Detection
(in USD)
Rate
(in USD)
Rate
m
=
m=
1
1
0.8730
0.0000
0.4436
0.0000
m
=
m=
2
2
1.7557
0.3974
0.8904
0.3333
m
=
m=
5
5
4.3992
0.6357
2.2189
0.5846
m
=
m=
10
10
8.8138
0.7243
4.4530
0.7042
m
=
m=
25
25
22.0332
0.7742
11.1055
0.8267
m
=
m=
50
50
43.9539
0.8105
22.2106
0.8182
(a) Detection rate and LLM costs as the query budget, i.e., the number
m
m
of programs generated by
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
increases.
t
=
t=
0.2
0.2
8.8138
0.5422
4.4530
0.5556
t
=
t=
0.6
0.6
8.8174
0.7148
4.4840
0.7286
t
=
t=
1
1
9.0657
0.8050
4.5254
0.7600
(b) Detection rate and LLM costs as temperature
t
t
of
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
increases.
n
=
n=
100
100
8.8174
0.6811
4.4840
0.6615
n
=
n=
1000
1000
8.8174
0.7148
4.4840
0.7286
n
=
n=
2000
2000
8.8174
0.7200
4.4840
0.7083
n
=
n=
5000
5000
8.8174
0.7355
4.4840
0.7222
n
=
n=
10000
10000
8.8174
0.7445
4.4840
0.7222
(c) Detection rate and LLM costs as the testing budget, i.e., the number
n
n
of test inputs generated by
𝖦𝖾𝗇
⁡
(
d
)
\mathsf{Gen}(d)
increases.
Table 3:
Results of our ablation study. We vary one value while keeping all others constant.
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
is GPT-4o. Default number of programs per task:
m
=
10
m=10
. Default number of test inputs per task:
n
=
1000
n=1000
. Default temperature:
t
=
0.6
t=0.6
.
RQ-3. Ablation
Table
3
shows the results of our ablation study as we vary the LLM the number
m
m
of generated programs, the number
n
n
of generated test inputs, or the LLM’s temperature
t
t
. A higher temperature increases the likelihood that the LLM samples a lower-probability token during next-token prediction.
We vary one parameter and keep all others constant (
m
=
10
m=10
,
n
=
1000
n=1000
,
t
=
0.6
t=0.6
, GPT4-o; cf. §
6
).
Query budget
m
m
. The detection rate increases with
m
m
. For instance, when changing
m
m
from 10 to 50, the detection rate increases by 14–19% from 0.7 to about 0.83 for HumanEval and from 0.72 to 0.82 for MBPP. The advantage comes at a substantial monetary cost. When changing
m
m
from 10 to 50, our expenses increased by more than fivefold, e.g., from $9 to $44 for MBPP.
For HumanEval, we actually observe a slightly higher detection rate (0.83) at
m
=
25
m=25
, which we explain by the randomness of the sampling and test generation process. It might also indicate that the detection rate starts to saturate for larger values of
m
m
(which we determined as uneconomical for us to test).
Another interesting observation is that just sampling a second program (
m
=
2
m=2
) already gives us a 0.33 to 0.4 detection rate.
Temperature
t
t
. Detection rate increases with
t
t
. For instance, when changing
t
t
from 0.2 to 1.0, we see detection rate increase by 36–50% from 0.54 to 0.81 for MBPP and from 0.56 to 0.76 for HumanEval. A high temperature induces a high output diversity, which seems to increase the LLM’s incoherence, which serves us well in error detection.
Test inputs
n
n
. Detection rate increases with
n
n
. However, compared to the other hyperparameters, a substantial increase in the number of generated test inputs induces only a relatively small increase in detection rate.
RQ-3
.
Increasing
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
’s query budget
m
m
,
𝖦𝖾𝗇
\mathsf{Gen}
’s testing budget
n
n
, or the temperature
t
t
also increases the detection rate. However, an x-fold increase in query budget comes at a greater-than x-fold increase in expenses.
8
Threats to Validity
As with any empirical study, there are threats to the validity of our results and conclusions. The first threat is to the
external validity
, i.e., the extent to which our findings can be generalized. As the subjects of our study, we selected LLMs from all major LLM vendors that were top-performing according to code generation leaderboards. They represent the current state-of-the-art.
As the objects of our study, we selected the two most widely used code generation benchmarks, MBPP and HumanEval, to facilitate comparison with results in related research. However, the findings may not generalize to more complex programming tasks or programming languages other than Python, and we call on the community to replicate our experiments for their use cases. Beyond the empirical results we also formally prove certain properties of incoherence and its estimation in the general.
The second threat is to the internal validity, i.e., the extent to which the presented evidence supports our claims about cause and effect within the context of our study. In the benchmarks, the task description may be ambiguous or the ground-truth implementation incorrect
(
Siddiq et al. 2024
)
. We use popular well-scrutinized benchmarks. From MBPP, we chose the best-quality, hand-curated set of tasks.
DiffTrustmay contain bugs itself, but we release all our scripts and data for the community to scrutinize.
9
Perspective
We believe that our incoherence-based perspective gives rise to a proliferation of new techniques built for
trustworthy code generation with probabilistic guarantees
.
In this paper, we discuss the formal estimation of the correctness of an LLM-generated program when there is
no automated mechanism
to decide whether a program is correct or not (e.g., a formal specification or a ground-truth implementation). We model the generated program as a random variable drawn from an unknown distribution induced by the coder (e.g., the LLM). This opens the door for a probabilistic notion of correctness. Our measure, incoherence, formalizes the observation that, if two random programs for the same task disagree on the output for an input, at least one must be incorrect. We formally demonstrate how the coder’s error on a task has a lower bound in terms of the coder’s incoherence on that task and empirically observe that a non-zero incoherence detects more than two-thirds of the incorrect programs. Since incoherence does not depend on model internals, it can be applied broadly across LLMs of any kind and even to probabilistic systems like LLM-agents.
An incoherence-based evaluation of the code generation capabilities of multiple LLMs also addresses several open challenges of the traditional ground-truth-based
pass@1
evaluation. The existing process of curating large coding benchmarks with correct human-generated ground-truth implementations is labour-intensive, error-prone, and subject to future data leakage issues
(
Ramos et al. 2025
)
. Incoherence paves the way for evaluations on a substantially larger scale, basically on a stream of programming tasks.
Acknowledgments
We thank the anonymous reviewers for their constructive feedback
and for helping us improve this paper. This research is partially
funded by the European Union. Views and opinions expressed are
however those of the author(s) only and do not necessarily reflect
those of the European Union or the European Research Council
Executive Agency. Neither the European Union nor the granting
authority can be held responsible for them. This work is supported
by ERC grant (Project AT_SCALE, 101179366). This research is also
partially funded by the ENS Paris-Saclay who graciously supported the internship
of the first author at the MPI for Security and Privacy.
References
Barr
et al.
(2015)
E. T. Barr, M. Harman, P. McMinn, M. Shahbaz, and S. Yoo
The oracle problem in software testing: a survey
.
IEEE Transactions on Software Engineering
41
(
5
),
pp. 507–525
.
External Links:
Document
Cited by:
§2
.
Böhme
et al.
(2021a)
M. Böhme, C. Cadar, and A. Roychoudhury
Fuzzing: challenges and reflections
.
IEEE Software
38
(
3
),
pp. 79–86
.
External Links:
Document
Cited by:
§5.2
.
Böhme
et al.
(2021b)
M. Böhme, D. Liyanage, and V. Wüstholz
Estimating residual risk in greybox fuzzing
.
In
Proceedings of the 15th Joint meeting of the European Software Engineering Conference and the ACM SIGSOFT Symposium on the Foundations of Software Engineering
,
ESEC/FSE
,
pp. 494–504
.
External Links:
Document
Cited by:
§5.2
.
Böhme
et al.
(2013)
M. Böhme, B. C. D. S. Oliveira, and A. Roychoudhury
Partition-based regression verification
.
In
2013 35th International Conference on Software Engineering (ICSE)
,
Vol.
,
pp. 302–311
.
External Links:
Document
Cited by:
§5.2
.
Böhme (2018)
M. Böhme
STADS: software testing as species discovery
.
ACM Trans. Softw. Eng. Methodol.
27
(
2
).
External Links:
ISSN 1049-331X
,
Link
,
Document
Cited by:
§5.2
.
Böhme (2019)
M. Böhme
Assurance in software testing: a roadmap
.
In
Proceedings of the 41st International Conference on Software Engineering: New Ideas and Emerging Results
,
ICSE-NIER ’19
,
pp. 5–8
.
External Links:
Link
,
Document
Cited by:
§5.2
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba
Evaluating large language models trained on code
.
External Links:
2107.03374
,
Link
Cited by:
§1
,
§3.2
,
§3.2
,
§5.2
.
DeepSeek-AI
et al.
(2025)
DeepSeek-AI, D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao, Z. Li, Z. Gao, A. Liu, B. Xue, B. Wang, B. Wu, B. Feng, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, D. Dai, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Bao, H. Xu, H. Wang, H. Ding, H. Xin, H. Gao, H. Qu, H. Li, J. Guo, J. Li, J. Wang, J. Chen, J. Yuan, J. Qiu, J. Li, J. L. Cai, J. Ni, J. Liang, J. Chen, K. Dong, K. Hu, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Zhao, L. Wang, L. Zhang, L. Xu, L. Xia, M. Zhang, M. Zhang, M. Tang, M. Li, M. Wang, M. Li, N. Tian, P. Huang, P. Zhang, Q. Wang, Q. Chen, Q. Du, R. Ge, R. Zhang, R. Pan, R. Wang, R. J. Chen, R. L. Jin, R. Chen, S. Lu, S. Zhou, S. Chen, S. Ye, S. Wang, S. Yu, S. Zhou, S. Pan, S. S. Li, S. Zhou, S. Wu, S. Ye, T. Yun, T. Pei, T. Sun, T. Wang, W. Zeng, W. Zhao, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, W. L. Xiao, W. An, X. Liu, X. Wang, X. Chen, X. Nie, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yang, X. Li, X. Su, X. Lin, X. Q. Li, X. Jin, X. Shen, X. Chen, X. Sun, X. Wang, X. Song, X. Zhou, X. Wang, X. Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. Zhang, Y. Xu, Y. Li, Y. Zhao, Y. Sun, Y. Wang, Y. Yu, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Ou, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Xiong, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. X. Zhu, Y. Xu, Y. Huang, Y. Li, Y. Zheng, Y. Zhu, Y. Ma, Y. Tang, Y. Zha, Y. Yan, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Xie, Z. Zhang, Z. Hao, Z. Ma, Z. Yan, Z. Wu, Z. Gu, Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Pan, Z. Huang, Z. Xu, Z. Zhang, and Z. Zhang
DeepSeek-r1: incentivizing reasoning capability in llms via reinforcement learning
.
External Links:
2501.12948
,
Link
Cited by:
§6.2
.
Fan
et al.
(2023)
Z. Fan, X. Gao, M. Mirchev, A. Roychoudhury, and S. H. Tan
Automated repair of programs from large language models
.
In
Proceedings of the 45th International Conference on Software Engineering
,
ICSE ’23
,
pp. 1469–1481
.
External Links:
ISBN 9781665457019
,
Link
,
Document
Cited by:
§1
.
Farquhar
et al.
(2024)
S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal
Detecting hallucinations in large language models using semantic entropy
.
Nature
630
,
pp. 625–627
.
External Links:
Document
,
Link
Cited by:
§1
,
§2
.
Ferguson and Korel (1996)
R. Ferguson and B. Korel
The chaining approach for software test data generation
.
ACM Trans. Softw. Eng. Methodol.
5
(
1
),
pp. 63–86
.
External Links:
ISSN 1049-331X
,
Link
,
Document
Cited by:
§5.2
.
Friel and Sanyal (2023)
R. Friel and A. Sanyal
ChainPoll: a high efficacy method for llm hallucination detection
.
arXiv preprint arXiv:2310.18344
.
External Links:
Link
Cited by:
§1
,
§2
.
Hou
et al.
(2024)
X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy, and H. Wang
Large language models for software engineering: a systematic literature review
.
ACM Trans. Softw. Eng. Methodol.
33
(
8
).
External Links:
ISSN 1049-331X
,
Link
,
Document
Cited by:
§2
.
Hu
et al.
(2025)
Y. Hu, Q. Zhou, Q. Chen, X. Li, L. Liu, D. Zhang, A. Kachroo, T. Oz, and O. Tripp
QualityFlow: an agentic workflow for program synthesis controlled by llm quality checks
.
arXiv preprint arXiv:2501.17167
.
Cited by:
§6.2
.
Ji
et al.
(2025)
S. Ji, Z. Song, F. Zhong, J. Jia, Z. Wu, Z. Cao, and T. Xu
MyGO multiplex cot: a method for self-reflection in large language models via double chain of thought thinking
.
arXiv preprint arXiv:2501.13117
.
Cited by:
§6.2
.
Jiang
et al.
(2024)
J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim
A survey on large language models for code generation
.
External Links:
2406.00515
,
Link
Cited by:
§2
.
King (1976)
J. C. King
Symbolic execution and program testing
.
Communications of the ACM
19
(
7
),
pp. 385–394
.
External Links:
ISSN 0001-0782
,
Link
,
Document
Cited by:
§5.2
.
Leaderboards (2025)
A. Leaderboards
Various leaderboards for llm-based code generation
.
Note:
https://livecodebench.github.io/leaderboard.html
https://evalplus.github.io/leaderboard.html
https://bigcode-bench.github.io/
Cited by:
§2
,
§6.2
.
Lee and Böhme (2023)
S. Lee and M. Böhme
Statistical reachability analysis
.
In
Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering
,
ESEC/FSE 2023
,
pp. 12
.
External Links:
Document
Cited by:
§5.2
.
Lee and Böhme (2025)
S. Lee and M. Böhme
How much is unseen depends chiefly on information about the seen
.
In
Proceedings of the 13th International Conference on Learning Representations
,
ICLR’25
.
Cited by:
§5.2
.
Lee and Böhme (2026)
S. Lee and M. Böhme
Dependency-aware residual risk analysis
.
In
Proceedings of the 48th IEEE/ACM International Conference on Software Engineering
,
ICSE’26
.
Cited by:
§5.2
.
Li
et al.
(2024)
J. Li, Y. Zhu, Y. Li, G. Li, and Z. Jin
Showing llm-generated code selectively based on confidence of llms
.
arXiv preprint arXiv:2410.03234
.
External Links:
Link
Cited by:
§1
,
§2
,
§6.2
.
Liu
et al.
(2023)
J. Liu, C. S. Xia, Y. Wang, and L. ZHANG
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
In
Advances in Neural Information Processing Systems
,
A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine (Eds.)
,
Vol.
36
,
pp. 21558–21572
.
External Links:
Link
Cited by:
Appendix A
,
§1
,
§3.2
,
§5.2
.
Mahmud
et al.
(2025)
T. Mahmud, B. Duan, C. Pasareanu, and G. Yang
Enhancing llm code generation with ensembles: a similarity-based selection approach
.
External Links:
2503.15838
,
Link
Cited by:
§2
.
Manakul
et al.
(2023)
P. Manakul, A. Liusie, and M. J. F. Gales
SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models
.
arXiv preprint arXiv:2303.08896
.
External Links:
Link
Cited by:
§1
,
§2
,
§4
.
OpenRouter.ai (2025)
OpenRouter.ai
Top llms in programming
.
Note:
https://openrouter.ai/rankings/programming?view=month
Cited by:
§2
.
Pearce
et al.
(2025)
H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri
Asleep at the keyboard? assessing the security of github copilot’s code contributions
.
Commun. ACM
68
(
2
),
pp. 96–105
.
External Links:
ISSN 0001-0782
,
Link
,
Document
Cited by:
§1
.
Ramos
et al.
(2025)
D. Ramos, C. Mamede, K. Jain, P. Canelas, C. Gamboa, and C. L. Goues
Are large language models memorizing bug benchmarks?
.
External Links:
2411.13323
,
Link
Cited by:
§9
.
Schober
et al.
(2018)
P. Schober, C. Boer, and L. Schwarte
Correlation coefficients: appropriate use and interpretation
.
Anesthesia & Analgesia
126
,
pp. 1
.
External Links:
Document
Cited by:
Table 5
.
Serebryany
et al.
(2012)
K. Serebryany, D. Bruening, A. Potapenko, and D. Vyukov
AddressSanitizer: a fast address sanity checker
.
In
Proceedings of the 2012 USENIX Conference on Annual Technical Conference
,
USENIX ATC’12
,
USA
,
pp. 28
.
Cited by:
§2
.
Sharma and David (2025)
A. Sharma and C. David
Assessing correctness in llm-based code generation via uncertainty estimation
.
External Links:
2502.11620
,
Link
Cited by:
§2
.
Siddiq
et al.
(2024)
M. L. Siddiq, S. Dristi, J. Saha, and J. C. S. Santos
The fault in our stars: quality assessment of code generation benchmarks
.
External Links:
2404.10155
,
Link
Cited by:
§8
.
Zalewski (2014)
M. Zalewski
Pulling jpegs out of thin air
.
Note:
https://lcamtuf.blogspot.com/2014/11/pulling-jpegs-out-of-thin-air.html
Cited by:
§5.2
.
Appendix A
Implementation Details
Figure
3
provides a procedural overview of our Python implementation, called DiffTrust. For every programming
task
in a dataset, for every
coder
(i.e., LLM), repeated
M
M
times to produce
M
M
candidate functions
, DiffTrustuses the LLM vendor-provided application programming interface (API) to generate a Python program that implements the natural language specification
d
d
that is provided with the task. The coder’s prompt further contains instructions to adhere to a given function signature. To optimize throughput, DiffTrustdispatches LLM queries in parallel whenever possible, with a fallback to sequential execution in the event of API rate limiting or errors. By default, we generate
m
=
10
m=10
candidate functions for each task. We vary
m
∈
{
1
,
2
,
5
,
10
,
25
,
50
}
m\in\{1,2,5,10,25,50\}
in the ablation study (RQ3).
For every programming task, once for the empirical error and once for the empirical incoherence, DiffTrustuses the
input generator
to generate
n
n
inputs for the generated
candidate functions
using the task-provided
seed inputs
. The test generator implements the budget-constrained
𝖢𝗈𝖽𝖾𝗋
m
\mathsf{Coder}_{m}
presented in Section
5.1
and the type-aware mutation-based fuzzing method
𝖦𝖾𝗇
\mathsf{Gen}
introduced in EvalPlus
(
Liu et al. 2023
)
and discussed in Section
5.2
. We provide a list of supported mutations in the appendix (Table
6
). We note that non-zero incoherence implies non-zero error for all
𝖦𝖾𝗇
\mathsf{Gen}
(Thm.
4.1
and Eqn. (
7
)). We also note that point-wise error [Eqn. (
6
)] and incoherence [Eqn. (
7
)] are defined w.r.t. the same distribution induced by
𝖦𝖾𝗇
\mathsf{Gen}
.
To ensure robustness, all executions, whether for compilation, incoherence estimation, or error estimation, are subject to a 60-second timeout.
The empirical error is computed using the task-provided ground-truth (GT) function
f
d
∗
f^{*}_{d}
. By default, we generate
n
=
1000
n=1000
test inputs. We vary
n
∈
{
100
,
1000
,
2000
,
5000
,
10000
}
n\in\{100,1000,2000,5000,10000\}
in RQ3.
Figure 3:
Workflow of our implementation DiffTrust.
We publish all data, the analysis, and the virtual experimental infrastructure to reproduce our experiments:
https://github.com/mpi-softsec/difftrust
A.1
Infrastructure
We used a single machine equipped with an AMD EPYC 7713P 64-Core Processor (128 threads), 251 GB of RAM, running Ubuntu 22.04.5 LTS 64-bit.
Appendix B
Proof of Pointwise Incoherence Inequality
For readers who prefer a fully explicit probability-theoretic formalization, we describe here the underlying probability space used implicitly in the main text.
We consider a probability space
(
Ω
,
ℱ
,
ℙ
)
(\Omega,\mathcal{F},\mathbb{P})
, where
Ω
\Omega
is the sample space,
ℱ
\mathcal{F}
the
σ
\sigma
-algebra of events, and
ℙ
\mathbb{P}
the probability measure. Random variables are measurable functions from
Ω
\Omega
to their codomain. For a mathematical expression
e
​
x
​
p
​
r
​
[
X
1
,
…
,
X
n
]
expr[X_{1},\dots,X_{n}]
involving random variables, we write
{
e
​
x
​
p
​
r
}
:=
{
ω
∈
Ω
∣
e
​
x
​
p
​
r
​
[
X
1
​
(
ω
)
,
…
,
X
n
​
(
ω
)
]
​
holds
}
.
\{expr\}:=\{\omega\in\Omega\mid expr[X_{1}(\omega),\dots,X_{n}(\omega)]\text{ holds}\}.
Theorem
4.1
states that :
∀
𝖦𝖾𝗇
,
∀
d
∈
𝖣𝖾𝗌𝖼𝗋
,
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≤
2
×
ℰ
𝖦𝖾𝗇
⁡
(
d
)
.
\forall\mathsf{Gen},\forall d\in\mathsf{Descr},\quad\Inc_{\mathsf{Gen}}(d)\leq 2\times\Err_{\mathsf{Gen}}(d).
Proof.
Let
𝖦𝖾𝗇
\mathsf{Gen}
be an input generation system and let
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
.
Let
Π
1
d
,
Π
2
d
​
∼
i
​
i
​
d
​
𝖢𝗈𝖽𝖾𝗋
​
(
d
)
\Pi^{d}_{1},\Pi^{d}_{2}\overset{iid}{\sim}\mathsf{Coder}(d)
represent two independently sampled programs from
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
output distribution for task
d
d
and let
X
∼
𝖦𝖾𝗇
⁡
(
d
)
X\sim\mathsf{Gen}(d)
represent an input sampled from
𝖦𝖾𝗇
\mathsf{Gen}
for task
d
d
.
For every sample
ω
∈
Ω
\omega\in\Omega
, let
f
1
=
⟦
Π
1
d
​
(
ω
)
⟧
f_{1}=\llbracket\Pi^{d}_{1}(\omega)\rrbracket
,
f
2
=
⟦
Π
2
d
​
(
ω
)
⟧
f_{2}=\llbracket\Pi^{d}_{2}(\omega)\rrbracket
and
x
=
X
⁡
(
ω
)
x=X(\omega)
be the corresponding outcomes of
⟦
Π
1
d
⟧
,
⟦
Π
2
d
⟧
\llbracket\Pi^{d}_{1}\rrbracket,\llbracket\Pi^{d}_{2}\rrbracket
and
X
X
. Then we have the following implication
f
1
​
(
x
)
≠
f
2
​
(
x
)
⟹
(
f
1
​
(
x
)
≠
f
d
∗
​
(
x
)
∨
f
2
​
(
x
)
≠
f
d
∗
​
(
x
)
)
.
f_{1}(x)\neq f_{2}(x)\implies(f_{1}(x)\neq f^{\ast}_{d}(x)\lor f_{2}(x)\neq f^{\ast}_{d}(x)).
Taking corresponding probabilistic events
E
Π
1
d
,
Π
2
d
:=
{
⟦
Π
1
d
⟧
(
X
)
≠
⟦
Π
2
d
⟧
(
X
)
}
\displaystyle E_{\Pi^{d}_{1},\Pi^{d}_{2}}:=\{\llbracket\Pi^{d}_{1}\rrbracket(X)\neq\llbracket\Pi^{d}_{2}\rrbracket(X)\}
E
Π
1
d
,
f
d
∗
:=
{
⟦
Π
1
d
⟧
(
X
)
≠
f
d
∗
(
X
)
}
\displaystyle E_{\Pi^{d}_{1},f^{\ast}_{d}}:=\{\llbracket\Pi^{d}_{1}\rrbracket(X)\neq f^{\ast}_{d}(X)\}
E
Π
2
d
,
f
d
∗
:=
{
⟦
Π
2
d
⟧
(
X
)
≠
f
d
∗
(
X
)
}
\displaystyle E_{\Pi^{d}_{2},f^{\ast}_{d}}:=\{\llbracket\Pi^{d}_{2}\rrbracket(X)\neq f^{\ast}_{d}(X)\}
We thus have
E
Π
1
d
,
Π
2
d
⊆
E
Π
1
d
,
f
d
∗
∪
E
Π
2
d
,
f
d
∗
.
E_{\Pi^{d}_{1},\Pi^{d}_{2}}\subseteq E_{\Pi^{d}_{1},f^{\ast}_{d}}\cup E_{\Pi^{d}_{2},f^{\ast}_{d}}.
Therefore
ℙ
⁡
(
E
Π
1
d
,
Π
2
d
)
\displaystyle\mathbb{P}(E_{\Pi^{d}_{1},\Pi^{d}_{2}})
≤
ℙ
⁡
(
E
Π
1
d
,
f
d
∗
∪
E
Π
2
d
,
f
d
∗
)
\displaystyle\leq\mathbb{P}(E_{\Pi^{d}_{1},f^{\ast}_{d}}\cup E_{\Pi^{d}_{2},f^{\ast}_{d}})
≤
ℙ
⁡
(
E
Π
1
d
,
f
d
∗
)
+
ℙ
⁡
(
E
Π
2
d
,
f
d
∗
)
.
\displaystyle\leq\mathbb{P}(E_{\Pi^{d}_{1},f^{\ast}_{d}})+\mathbb{P}(E_{\Pi^{d}_{2},f^{\ast}_{d}}).
Since by definition,
ℐ
𝖦𝖾𝗇
⁡
(
d
)
=
ℙ
⁡
(
E
Π
1
d
,
Π
2
d
)
\Inc_{\mathsf{Gen}}(d)=\mathbb{P}(E_{\Pi^{d}_{1},\Pi^{d}_{2}})
and
ℰ
𝖦𝖾𝗇
⁡
(
d
)
=
ℙ
⁡
(
E
Π
1
d
,
f
d
∗
)
=
ℙ
⁡
(
E
Π
2
d
,
f
d
∗
)
\Err_{\mathsf{Gen}}(d)=\mathbb{P}(E_{\Pi^{d}_{1},f^{\ast}_{d}})=\mathbb{P}(E_{\Pi^{d}_{2},f^{\ast}_{d}})
.
We thus obtain
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≤
2
×
ℰ
𝖦𝖾𝗇
⁡
(
d
)
.
\Inc_{\mathsf{Gen}}(d)\leq 2\times\Err_{\mathsf{Gen}}(d).
∎
Appendix C
Estimation of Incoherence and Error
C.1
Monte Carlo Estimation of Pointwise Error
Given
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
a code generation system and provided
𝖦𝖾𝗇
\mathsf{Gen}
an input generation system, when the ground truth implementation
f
d
∗
f^{\ast}_{d}
is available, we can estimate the pointwise error
ℰ
𝖦𝖾𝗇
⁡
(
d
)
\Err_{\mathsf{Gen}}(d)
using a Monte Carlo procedure based on Definition (
6
) as illustrated in Algorithm
1
.
Algorithm 1
Monte Carlo Estimation of
ℰ
𝖦𝖾𝗇
⁡
(
d
)
\Err_{\mathsf{Gen}}(d)
Input
:
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
,
𝖦𝖾𝗇
\mathsf{Gen}
, task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
, ground truth
f
d
∗
f^{\ast}_{d}
, error tolerance
ϵ
>
0
\epsilon>0
, failure probability
δ
>
0
\delta>0
Output
:
ℰ
¯
𝖦𝖾𝗇
​
(
d
)
\bar{\Err}_{\mathsf{Gen}}(d)
estimate such that
|
ℰ
¯
𝖦𝖾𝗇
​
(
d
)
−
ℰ
𝖦𝖾𝗇
⁡
(
d
)
|
≤
ϵ
|\bar{\Err}_{\mathsf{Gen}}(d)-\Err_{\mathsf{Gen}}(d)|\leq\epsilon
with probability
≥
1
−
δ
\geq 1-\delta
1:
Let
N
=
⌈
log
⁡
(
2
/
δ
)
2
​
ϵ
2
⌉
N=\left\lceil\frac{\log(2/\delta)}{2\epsilon^{2}}\right\rceil
2:
for
i
=
1
i=1
to
N
N
do
3:
Sample
π
∼
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\pi\sim\mathsf{Coder}(d)
4:
Sample
x
∼
𝖦𝖾𝗇
⁡
(
d
)
x\sim\mathsf{Gen}(d)
5:
e
i
←
𝕀
⁡
(
⟦
π
⟧
​
(
x
)
≠
f
d
∗
​
(
x
)
)
e_{i}\leftarrow\mathbb{I}\bigl(\llbracket\pi\rrbracket(x)\neq f^{\ast}_{d}(x)\bigr)
6:
end
for
7:
return
ℰ
¯
𝖦𝖾𝗇
​
(
d
)
=
1
N
​
∑
i
=
1
N
e
i
\bar{\Err}_{\mathsf{Gen}}(d)=\frac{1}{N}\sum_{i=1}^{N}e_{i}
Correctness Guarantee.
Each
e
i
e_{i}
is a Bernoulli random variable with
𝔼
⁡
[
e
i
]
=
ℰ
𝖦𝖾𝗇
⁡
(
d
)
\mathbb{E}[e_{i}]=\Err_{\mathsf{Gen}}(d)
. By Hoeffding’s inequality:
ℙ
⁡
(
|
ℰ
¯
𝖦𝖾𝗇
​
(
d
)
−
ℰ
𝖦𝖾𝗇
⁡
(
d
)
|
≥
ϵ
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
N
​
ϵ
2
)
.
\mathbb{P}(|\bar{\Err}_{\mathsf{Gen}}(d)-\Err_{\mathsf{Gen}}(d)|\geq\epsilon)\leq 2\exp(-2N\epsilon^{2}).
Thus, with
N
≥
log
⁡
(
2
/
δ
)
2
​
ϵ
2
N\geq\frac{\log(2/\delta)}{2\epsilon^{2}}
, we obtain the desired PAC guarantee.
C.2
Monte Carlo Estimation of Pointwise Incoherence
Given
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
a code generation system and provided
𝖦𝖾𝗇
\mathsf{Gen}
an input generation system, even if the ground truth implementation
f
d
∗
f^{\ast}_{d}
is unavailable, we can estimate the pointwise incoherence
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\Inc_{\mathsf{Gen}}(d)
using a Monte Carlo procedure based on Definition (
8
) as illustrated in Algorithm
2
.
Algorithm 2
Monte Carlo Estimation of
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\Inc_{\mathsf{Gen}}(d)
Input
:
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
,
𝖦𝖾𝗇
\mathsf{Gen}
, task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
, error tolerance
ϵ
>
0
\epsilon>0
, failure probability
δ
>
0
\delta>0
Output
:
ℐ
¯
𝖦𝖾𝗇
​
(
d
)
\bar{\Inc}_{\mathsf{Gen}}(d)
estimate such that
|
ℐ
¯
𝖦𝖾𝗇
​
(
d
)
−
ℐ
𝖦𝖾𝗇
⁡
(
d
)
|
≤
ϵ
|\bar{\Inc}_{\mathsf{Gen}}(d)-\Inc_{\mathsf{Gen}}(d)|\leq\epsilon
with probability
≥
1
−
δ
\geq 1-\delta
1:
Let
N
=
⌈
log
⁡
(
2
/
δ
)
2
​
ϵ
2
⌉
N=\left\lceil\frac{\log(2/\delta)}{2\epsilon^{2}}\right\rceil
2:
for
i
=
1
i=1
to
N
N
do
3:
Sample
π
1
,
π
2
​
∼
i
​
i
​
d
​
𝖢𝗈𝖽𝖾𝗋
​
(
d
)
\pi_{1},\pi_{2}\overset{iid}{\sim}\mathsf{Coder}(d)
4:
Sample
x
∼
𝖦𝖾𝗇
⁡
(
d
)
x\sim\mathsf{Gen}(d)
5:
d
i
←
𝕀
⁡
(
⟦
π
1
⟧
​
(
x
)
≠
⟦
π
2
⟧
​
(
x
)
)
d_{i}\leftarrow\mathbb{I}\bigl(\llbracket\pi_{1}\rrbracket(x)\neq\llbracket\pi_{2}\rrbracket(x)\bigr)
6:
end
for
7:
return
ℐ
¯
𝖦𝖾𝗇
​
(
d
)
=
1
N
​
∑
i
=
1
N
d
i
\bar{\Inc}_{\mathsf{Gen}}(d)=\frac{1}{N}\sum_{i=1}^{N}d_{i}
Correctness Guarantee.
Each
d
i
d_{i}
is a Bernoulli random variable with
𝔼
⁡
[
d
i
]
=
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\mathbb{E}[d_{i}]=\Inc_{\mathsf{Gen}}(d)
. Applying Hoeffding’s inequality:
ℙ
⁡
(
|
ℐ
¯
𝖦𝖾𝗇
​
(
d
)
−
ℐ
𝖦𝖾𝗇
⁡
(
d
)
|
≥
ϵ
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
N
​
ϵ
2
)
.
\mathbb{P}(|\bar{\Inc}_{\mathsf{Gen}}(d)-\Inc_{\mathsf{Gen}}(d)|\geq\epsilon)\leq 2\exp(-2N\epsilon^{2}).
Hence, with
N
≥
log
⁡
(
2
/
δ
)
2
​
ϵ
2
N\geq\frac{\log(2/\delta)}{2\epsilon^{2}}
, we obtain the desired PAC guarantee.
C.3
PAC Detection of Nonzero Incoherence
Given
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
a code generation system and provided
𝖦𝖾𝗇
\mathsf{Gen}
an input generation system, we may want to detect with high confidence whether the model exhibits nonzero pointwise incoherence on a given task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
. We present a probabilistically sound decision procedure based on repeated disagreement tests, as illustrated in Algorithm
3
.
Algorithm 3
PAC Detection of non-zero
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\Inc_{\mathsf{Gen}}(d)
Input
:
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
,
𝖦𝖾𝗇
\mathsf{Gen}
, task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
, incoherence threshold
ϵ
>
0
\epsilon>0
, confidence parameter
δ
>
0
\delta>0
Output
:
true
if
ℐ
𝖦𝖾𝗇
⁡
(
d
)
>
0
\Inc_{\mathsf{Gen}}(d)>0
is detected, otherwise
false
1:
Let
N
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
N=\left\lceil\frac{\log(\delta)}{\log(1-\epsilon)}\right\rceil
2:
for
i
=
1
i=1
to
N
N
do
3:
Sample
π
1
,
π
2
​
∼
i
​
i
​
d
​
𝖢𝗈𝖽𝖾𝗋
​
(
d
)
\pi_{1},\pi_{2}\overset{iid}{\sim}\mathsf{Coder}(d)
4:
Sample
x
∼
𝖦𝖾𝗇
⁡
(
d
)
x\sim\mathsf{Gen}(d)
5:
if
⟦
π
1
⟧
​
(
x
)
≠
⟦
π
2
⟧
​
(
x
)
\llbracket\pi_{1}\rrbracket(x)\neq\llbracket\pi_{2}\rrbracket(x)
then
6:
return
true
7:
end
if
8:
end
for
9:
return
false
Correctness Guarantee.
Let
ϵ
>
0
\epsilon>0
and
δ
>
0
\delta>0
. Then Algorithm
3
, when run with parameters
ϵ
\epsilon
and
δ
\delta
, satisfies the following:
•
If
ℐ
𝖦𝖾𝗇
⁡
(
d
)
=
0
\Inc_{\mathsf{Gen}}(d)=0
, the algorithm always returns
false
.
•
If
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≥
ϵ
\Inc_{\mathsf{Gen}}(d)\geq\epsilon
, the algorithm returns
true
with probability at least
1
−
δ
1-\delta
.
In other words, the algorithm detects non-zero incoherence with confidence at least
1
−
δ
1-\delta
, and it never returns false positives.
Proof.
Let
ϵ
>
0
\epsilon>0
and
δ
>
0
\delta>0
, and let
N
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
N=\left\lceil\frac{\log(\delta)}{\log(1-\epsilon)}\right\rceil
. Then Algorithm
3
satisfies the following:
•
No false positives.
If
ℐ
𝖦𝖾𝗇
⁡
(
d
)
=
0
\Inc_{\mathsf{Gen}}(d)=0
, then all sampled programs agree on all inputs almost surely. Therefore, no disagreement can ever be observed, and the algorithm always returns
false
.
•
False negative probability
≤
δ
\leq\delta
.
Suppose instead that
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≥
ϵ
\Inc_{\mathsf{Gen}}(d)\geq\epsilon
. Then in each trial of the algorithm, the probability of observing a disagreement is at least
ϵ
\epsilon
. Since the trials are independent, the probability that all
N
N
trials fail to detect a disagreement is at most:
(
1
−
ϵ
)
N
.
(1-\epsilon)^{N}.
By the choice of
N
N
, this is at most
δ
\delta
:
(
1
−
ϵ
)
N
≤
δ
.
(1-\epsilon)^{N}\leq\delta.
Hence, the probability that the algorithm detects a disagreement and returns
true
is at least
1
−
δ
1-\delta
.
∎
Implication for Error Detection.
Although the algorithm only checks for non-zero
incoherence
, we can derive a guarantee for non-zero
error
via Theorem
4.1
, which states:
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≤
2
⋅
ℰ
𝖦𝖾𝗇
⁡
(
d
)
.
\Inc_{\mathsf{Gen}}(d)\leq 2\cdot\Err_{\mathsf{Gen}}(d).
Thus, a detection of
ℐ
𝖦𝖾𝗇
⁡
(
d
)
≥
ϵ
\Inc_{\mathsf{Gen}}(d)\geq\epsilon
implies that
ℰ
𝖦𝖾𝗇
⁡
(
d
)
≥
ϵ
/
2
\Err_{\mathsf{Gen}}(d)\geq\epsilon/2
. Consequently, this detection method provides a statistically sound way to identify non-zero errors without requiring access to a ground truth implementation.
Appendix D
Functional Incoherence
While pointwise incoherence measures this divergence over specific inputs, functional incoherence extends the idea to the full input space. That is, two implementations are functionally incoherent if they disagree on
any
input. This notion aligns with the classic definition of program equivalence.
Let
Π
1
d
,
Π
2
d
​
∼
i
​
i
​
d
​
𝖢𝗈𝖽𝖾𝗋
​
(
d
)
\Pi_{1}^{d},\Pi_{2}^{d}\overset{iid}{\sim}\mathsf{Coder}(d)
be two independently sampled programs for a task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
. Let
⟦
Π
1
d
⟧
,
⟦
Π
2
d
⟧
\llbracket\Pi^{d}_{1}\rrbracket,\llbracket\Pi^{d}_{2}\rrbracket
denote their functional interpretations. We define the
functional incoherence
of a code generation system
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
for a task
d
d
is the probability that two independently sampled implementations are not functionally equivalent:
ℐ
⁡
(
d
)
:=
ℙ
⁡
(
⟦
Π
1
d
⟧
≠
⟦
Π
2
d
⟧
)
\Inc(d):=\mathbb{P}(\llbracket\Pi_{1}^{d}\rrbracket\neq\llbracket\Pi_{2}^{d}\rrbracket)
(12)
This notion captures global behavioral disagreement between sampled programs. In practice, while direct evaluation of functional equivalence is undecidable in general, functional incoherence may be conservatively approximated via testing or symbolic execution.
Functional incoherence can be seen as the limiting form of pointwise incoherence. Specifically,
ℐ
𝖦𝖾𝗇
⁡
(
d
)
\Inc_{\mathsf{Gen}}(d)
(as defined in the main text) estimates incoherence over a distribution of inputs, whereas
ℐ
⁡
(
d
)
\Inc(d)
considers disagreement over the entire input space.
Importantly, just as pointwise incoherence lower-bounds pointwise error, we can show that functional incoherence provides a lower bound on functional error.
D.1
Functional Incoherence as a Lower Bound on Error
Theorem D.1
(Functional Incoherence Inequality)
.
For any task
d
∈
𝖣𝖾𝗌𝖼𝗋
d\in\mathsf{Descr}
, functional incoherence provides a lower bound on functional error:
ℐ
⁡
(
d
)
≤
2
×
ℰ
⁡
(
d
)
.
\Inc(d)\leq 2\times\Err(d).
Proof.
Let
f
d
∗
f^{\ast}_{d}
denote the ground truth implementation for task
d
d
.
Let
f
1
:=
⟦
Π
1
d
⟧
f_{1}:=\llbracket\Pi_{1}^{d}\rrbracket
and
f
2
:=
⟦
Π
2
d
⟧
f_{2}:=\llbracket\Pi_{2}^{d}\rrbracket
be two independently sampled implementations from
𝖢𝗈𝖽𝖾𝗋
⁡
(
d
)
\mathsf{Coder}(d)
. Then:
{
f
1
≠
f
2
}
⊆
{
f
1
≠
f
d
∗
}
∪
{
f
2
≠
f
d
∗
}
\{f_{1}\neq f_{2}\}\subseteq\{f_{1}\neq f^{\ast}_{d}\}\cup\{f_{2}\neq f^{\ast}_{d}\}
This holds because if two functions differ, at least one must differ from the ground truth. Taking probabilities:
ℙ
⁡
(
f
1
≠
f
2
)
\displaystyle\mathbb{P}(f_{1}\neq f_{2})
≤
ℙ
⁡
(
f
1
≠
f
d
∗
)
+
ℙ
⁡
(
f
2
≠
f
d
∗
)
\displaystyle\leq\mathbb{P}(f_{1}\neq f^{\ast}_{d})+\mathbb{P}(f_{2}\neq f^{\ast}_{d})
Thus:
ℐ
⁡
(
d
)
≤
2
⋅
ℰ
⁡
(
d
)
\Inc(d)\leq 2\cdot\Err(d)
∎
Discussion.
This result mirrors the pointwise inequality established in the main text (Theorem
4.1
) and shows that disagreement between implementations is a rigorous signal of potential failure—even in the absence of ground truth.
While
ℰ
⁡
(
d
)
\Err(d)
requires access to
f
d
∗
f^{\ast}_{d}
,
ℐ
⁡
(
d
)
\Inc(d)
is fully estimable from samples of
𝖢𝗈𝖽𝖾𝗋
\mathsf{Coder}
. This makes functional incoherence a valuable unsupervised proxy for reliability, particularly in settings where model outputs must be audited without labeled data.
Table 4:
Performance of 16 LLMs on two benchmarks. The final row in each benchmark section reports the mean performance across all 16 models.
Mean
Mean
Spearman
Detection
Undetected
Model
Error
Incoherence
Correlation
Rate
Mean Error
MBPP
GPT-4o
0.2773
0.1123
0.6105
0.7243
0.1638
Claude 4 Opus (2025/05/14)
0.2715
0.0583
0.4508
0.4815
0.2140
Gemini 2.5 Pro (preview 05/06)
0.2960
0.0995
0.5276
0.6866
0.2071
LLaMA 4 Maverick 17B
0.2980
0.0680
0.4291
0.4741
0.2352
Claude 4 Sonnet (2025/04/14)
0.2693
0.0452
0.4151
0.4016
0.2150
DeepSeek-V3 (Mar 2024)
0.2659
0.1185
0.6112
0.7406
0.1555
GPT-o4 Mini
0.3109
0.1045
0.5646
0.7543
0.1784
Mistral 8B
0.3741
0.1641
0.5892
0.7037
0.2107
LLaMA 3 70B Instruct
0.3574
0.1689
0.5419
0.8139
0.2288
DeepSeek-Coder R1
0.2286
0.0811
0.5650
0.6453
0.1640
Gemini 2.5 Flash (preview 05/20)
0.2949
0.0936
0.5216
0.7122
0.2183
Gemini 2.0 Flash Lite
0.2913
0.1097
0.6237
0.6782
0.1586
LLaMA 3 8B Instruct
0.4022
0.2978
0.6509
0.9427
0.1544
GPT-4 Turbo
0.2825
0.1195
0.6186
0.7249
0.1556
GPT-4
0.2906
0.1511
0.6619
0.7840
0.1570
GPT-3.5 Turbo
0.3041
0.1334
0.6115
0.7027
0.1698
MBPP (Mean)
0.3009
0.1203
0.5621
0.6857
0.1866
HumanEval
GPT-4o
0.0927
0.0483
0.7181
0.7042
0.0460
Claude 4 Opus (2025/05/14)
0.0632
0.0067
0.4041
0.3000
0.0601
Gemini 2.5 Pro (preview 05/06)
0.0763
0.0295
0.7171
0.7188
0.0417
LLaMA 4 Maverick 17B
0.0876
0.0367
0.6242
0.5397
0.0583
Claude 4 Sonnet
0.0605
0.0076
0.4098
0.2778
0.0533
DeepSeek-V3 (Mar 2024)
0.0781
0.0235
0.5346
0.4576
0.0552
GPT-o4 Mini
0.0893
0.0388
0.7092
0.7051
0.0420
Mistral 8B
0.1585
0.0911
0.7282
0.7381
0.0737
LLaMA 3 70B Instruct
0.1223
0.0928
0.8173
0.8395
0.0314
DeepSeek-Coder R1
0.0724
0.0356
0.7994
0.7538
0.0180
Gemini 2.5 Flash (preview 05/20)
0.0796
0.0347
0.7584
0.7538
0.0339
Gemini 2.0 Flash Lite
0.1165
0.0343
0.4829
0.4118
0.0851
LLaMA 3 8B Instruct
0.2140
0.1954
0.8890
0.9245
0.0261
GPT-4 Turbo
0.0912
0.0477
0.7528
0.7606
0.0398
GPT-4
0.1144
0.0823
0.8127
0.8471
0.0424
GPT-3.5 Turbo
0.1635
0.0906
0.8192
0.8537
0.0458
HumanEval (Mean)
0.1050
0.0560
0.6861
0.6616
0.0471
Table 5:
Interpretation of Spearman’s
ρ
\rho
, based on thresholds from
Schober et al. (2018)
.
Spearman’s
ρ
\rho
Interpretation
0.00 – 0.09
Negligible correlation
0.10 – 0.39
Weak correlation
0.40 – 0.69
Moderate correlation
0.70 – 0.89
Strong correlation
0.90 – 1.00
Very strong correlation
Table 6:
List of basic type-aware mutations over input
x
x
.
Object Type
Mutation
Object Type
Mutation
int
,
float
Add (
±
\pm
1,
±
\pm
10, random)
NoneType
None
bool
Random boolean (True or False)
user-defined
Shallow copy + mutate fields recursively
str
Insert char at random index
list
,
set
Insert random element at random index/key
Delete char at random index
Insert dummy element at random index/key
Replace char w/ random ASCII
Swap two elements
Truncate random substring
dict
,
tuple
Duplicate entries randomly
Extend random substring
Insert entry at random index/key
Duplicate random substring
Delete element at random index/key