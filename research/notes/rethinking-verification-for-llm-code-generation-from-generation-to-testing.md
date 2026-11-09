---
title: 'Rethinking Verification for LLM Code Generation: From Generation to Testing'
id: rethinking-verification-for-llm-code-generation-from-generation-to-testing
tags:
- code-llm-requirement-pivots-5d35f5
- test-suite-quality
- rlvr-reward-signal
created: '2026-07-20T06:55:14.272391Z'
updated: '2026-07-20T06:56:07.918573Z'
source: https://arxiv.org/html/2507.06920
source_domain: arxiv.org
fetched_at: '2026-07-20T06:55:14.271704Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Argues HumanEval/LiveCodeBench-style test suites are too thin (homogeneous
  cases), inflating pass@k and corrupting RLVR reward signals. Curates TCGBench (1,840
  competitive-programming problems) and proposes SAGA, a human-LLM collaborative test-case-generation
  method reaching 90.62% bug-detection rate and 10.78pp higher verifier accuracy than
  LiveCodeBench-v6. Documents that LLM-generated test suites have high self-pass rates
  against LLM-generated code -- i.e., models' own tests miss the same categories of
  human-like bugs (logical flaws, integer overflow, boundary conditions) that their
  code-generation blind spots produce -- but this is measured at whole-problem bug-detection-rate
  granularity, not mapped onto a decomposed per-requirement label space shared between
  code failures and test failures.
---

Rethinking Verification for LLM Code Generation: From Generation to Testing
\newmdtheoremenv
corollaryCorollary
\newmdtheoremenv
[linewidth=0pt,innerleftmargin=4pt,innerrightmargin=4pt]lemmaLemma
†
†
†
†
\dagger
†
means corresponding authors,
‡
means project,
∗
*
∗
means authors contributed equally.
Rethinking Verification for LLM Code Generation:
From Generation to Testing
Zihan Ma
1,2,3,
∗
*
∗
,
Taolin Zhang
1,
∗
*
∗
,
Maosong Cao
1
,
Junnan Liu
1
,
Wenwei Zhang
1
,
Minnan Luo
2,3,
†
†
\dagger
†
,
Songyang Zhang
1,
†
,
‡
†
‡
\dagger,\ddagger
† , ‡
,
,Kai Chen
1,
†
†
\dagger
†
1
Shanghai AI Laboratory
2
School of Computer Science and Technology, Xi’an Jiaotong University, China
3
MOE KLINNS Lab, Xi’an Jiaotong University, China
{mazihan880}@stu.xjtu.edu.cn
{zhangtaolin,zhangsongyang}@pjlab.org.cn
{minnluo}@xjtu.edu.cn
Abstract
Large language models (LLMs) have recently achieved notable success in code
-
generation benchmarks such as HumanEval and LiveCodeBench.
However, a detailed examination reveals that these evaluation suites often comprise only a limited number of homogeneous test cases, resulting in subtle faults going undetected. This not only artificially inflates measured performance but also compromises accurate reward estimation in reinforcement learning frameworks utilizing verifiable rewards (RLVR). To address these critical shortcomings, we systematically investigate the test-case generation (TCG) task by proposing multi-dimensional metrics designed to rigorously quantify test-suite thoroughness. Furthermore, we introduce a human-LLM collaborative method (SAGA), leveraging human programming expertise with LLM reasoning capability, aimed at significantly enhancing both the coverage and the quality of generated test cases. In addition, we develop a TCGBench to facilitate the study of the TCG task.
Experiments show that SAGA achieves a detection rate of 90.62% and a verifier accuracy of 32.58% on TCGBench. The Verifier Accuracy (Verifier Acc) of the code generation evaluation benchmark synthesized by SAGA is 10.78% higher than that of LiveCodeBench-v6. These results demonstrate the effectiveness of our proposed method. We hope this work contributes to building a scalable foundation for reliable LLM code evaluation, further advancing RLVR in code generation, and paving the way for automated adversarial test synthesis and adaptive benchmark integration.
1
1
1
The data demo and prompts can be accessed via
https://github.com/open-compass/SAGA
1
Introduction
Large Language Models (LLMs) have triggered a paradigm shift in automatic code generation, demonstrating capabilities on par with or even exceeding human programmers on numerous benchmark tasks. As LLMs become increasingly integrated into software development workflows, ensuring the quality and reliability of the code they produce is paramount. This necessitates reliable evaluation methodologies, where code verifiers—typically powered by test suites—play a critical role. This raises a crucial question:
Are the test cases of current benchmarks for evaluating models’ code capabilities robust enough?
Initial analyses of benchmarks like HumanEval
[
6
]
(avg. 7.7 tests/problem), MBPP
[
3
]
(3 tests/problem), and EvalPlus
[
27
,
28
]
(which saw a 15% pass rate drop with 80× more tests) indicate the fragility of current evaluation setups due to sparse test coverage. While methods like TestEval
[
41
]
tailor tests to specific solutions, they are inefficient for large-scale evaluation and impractical for dynamic integration into RL training loops, thereby hindering the development of models robust against diverse failures. LiveCodeBench
[
19
]
employs LLMs to generate numerous tests from golden solutions and synthetic inputs, aiming to enhance robustness.
Figure 1
:
(a) Verifiers synthesized primarily from LLM-generated data exhibit a high failure rate when testing human-written bugs. (b) PCA analysis reveals that LLM-induced errors are highly clustered, indicating systematic weaknesses, whereas human errors are diverse and dispersed, posing greater challenges to existing verifiers.
However, a fundamental concern is that such methods may inadvertently create tests biased towards typical, often homogenized, LLM error patterns, which starkly contrast with diverse human reasoning errors. Conversely, competitive programming platforms (Online Judges) possess extensive, rigorously curated test suites for assessing code robustness, but these are often private and inaccessible. This underscores the urgent need for accessible and robust code verifiers to enable reliable performance evaluation and reward estimation.
In this work, we first identify limitations in current benchmarks through preliminary experiments. Our investigation reveals critical weaknesses in existing verifier suites. Specifically, when we took LLM-generated solutions that had passed LiveCodeBench’s private tests and re-evaluated them on LeetCode’s online judge, we found that for a significant portion of these solutions—20% for medium and 40% for hard problems, respectively—LeetCode identified errors that LiveCodeBench’s verifier had missed. This demonstrates that LiveCodeBench’s verifiers can be flawed, failing to achieve comprehensive error detection and thereby overestimating the true quality of the LLM-generated solutions. Furthermore, these LLM-centric verifiers themselves exhibit a high failure rate (i.e., they fail to detect existing bugs) when evaluating human-written faulty code, a rate much higher than any apparent failure rate on LLM-generated errors (Figure
1
(a)). PCA analysis of error patterns (Figure
1
(b)) reveals that LLM errors cluster tightly, indicating shared systematic biases, while human errors are widely distributed across a complex error landscape.
These findings underscore the fundamental inadequacy of constructing verifiers solely from LLM-generated data, as such approaches misassess LLMs’ coding capabilities and provide flawed training feedback, manifesting two critical challenges:
(1) Test Case Homogenization and LLM-Centric Bias
: LLM-based TCG methods produce test suites that mirror the generating models’ error patterns and cognitive biases, creating a “homogenization trap” where tests focus on LLM-like failures while neglecting diverse human programming errors (e.g., logical flaws, integer overflows).
(2) Verifier Ineffectiveness and Persistent Blind Spots
: Verifiers built on such test suites exhibit blind spots for human-like errors, failing to rigorously evaluate code due to challenges in generating tests for complex boundary conditions and interaction scenarios, compounded by LLM-centric test design.
These challenges impede reinforcement learning frameworks (e.g., DeepSeek-R1
[
8
]
, O1-IOI
[
10
]
) from leveraging verifiable rewards, leading to
optimization misdirection
via
reward hacking
2
2
2
Models exploit verifier weaknesses instead of achieving genuine correctness, as they are insufficiently penalized for diverse errors.
.
To address these challenges, we develop a comprehensive measurement framework for code verifiers, introducing multi-dimensional evaluation metrics (detection rate, verifier accuracy) and identifying test case diversity and per-case strength as critical quality factors. We derive an upper bound for detection rate and validate it empirically across 1,500+ coding problems. Using this framework, we uncover systemic test quality issues in leading benchmarks, such as CodeForce-CoTs
[
37
]
, where 50% of problems had tests failing to detect known errors and 84% of verifiers were flawed, further underscoring these limitations.
To systematically improve the quality of code verifiers, we formally define the Test Case Generation (TCG) task, comprising three core components:
task formulation
,
benchmark construction
, and
method exploration
. We introduce TCGBench, a benchmark curated by aggregating representative problems from three leading competitive programming platforms—Atcoder, Codeforces, and Nowcoder. TCGBench curates human-verified adversarial examples spanning diverse error patterns (e.g., logical flaws, edge cases) and supports comprehensive evaluation of TCG methods.
We further investigate current TCG methods and propose SAGA (
S
trategic
A
dversarial & Constraint-differential
G
ener
A
tive workflow), a novel human-LLM collaborative framework. SAGA is designed to systematically generate high-coverage, highly discriminative test cases by leveraging both human-derived constraints from correct solutions and insights from failure modes in incorrect solutions. This dual-pronged analytical approach allows SAGA to achieve improvements over current state-of-the-art TCG methods, with the Detection Rate increasing by 9.55% and Verifier Accuracy by 12.14%.
Additionally, we leverage SAGA to enhance the quality of the popular code generation benchmark LiveCodeBench-v6 (subset)
3
3
3
The subset used in our study comprises 101 problems from AtCoder, specifically from contests ABC387 through ABC400 and ARC190 through ARC196 (problems A to F). This selection facilitates a consistent evaluation scope when comparing with benchmarks like our proposed TCGBench, which also incorporates these recent algorithmic challenges.
, and develop CodeCompass, a new high-quality code benchmark. We believe SAGA can further be employed to scale datasets, enabling the production of training data with robust and accurate reward estimation for coding tasks.
Our main contributions are as follows:
•
We construct
TCGBench
, a comprehensive dataset from competitive programming platform, to analyze existing Test Case Generation practices. On it, we formalize multi-dimensional metrics for rigorous test case quality evaluation.
•
We propose and validate
SAGA
, a novel human-LLM collaborative TCG framework (Fig.
5
). By integrating insights from both correct and incorrect human solutions, SAGA generates significantly more effective test suites, improving Verifier Accuracy by 15.86% over existing TCG methods.
•
Using SAGA, we develop
CodeComPass
, a challenging benchmark with human-verified adversarial examples for robust code generation evaluation, and introduce
TCGCoder-7B
, a SAGA-distilled specialist model for capable TCG.
Figure 2
:
The code evaluation pipeline and different TCG paradigms.
2
Evaluating Verifier Quality: Metrics and TCG Paradigms
The reliable evaluation of LLM-generated code is critically constrained by the quality and accessibility of verifiers. Standard benchmarks like HumanEval
[
6
]
often employ limited test suites, while the extensive private verifiers of Online Judges remain largely inaccessible for broader research. This scarcity of robust, accessible verifiers impedes accurate LLM evaluation and the advancement of RLVR.
To surmount this challenge, we focus on leveraging LLMs themselves for
Test Case Generation
—the systematic synthesis of test suites. Figure
2
illustrates the pivotal role of a Code Verifierin the LLM code evaluation pipeline. It also highlights distinct TCG paradigms:
•
Direct Generation:
An LLM directly produces complete test cases (inputs and outputs). Representative works include TestChain
[
22
]
, AceCoder
[
46
]
, and CodeRM
[
31
]
.
•
Input-Interpreter:
An LLM generates test inputs; a ground-truth interpreter (or reference solution) then computes the corresponding outputs. This paradigm, exemplified by LiveCodeBench
[
19
]
and Codeforce-COT
[
37
]
, often employs random input sampling—a strategy proven effective by LiveCodeBench for generating numerous diverse test cases and thus adopted in our baseline evaluations. EvalPlus
[
27
]
, which mutates seed inputs for execution, also aligns with this approach. A comparative analysis with EvalPlus is detailed in Section
3.2.1
.
•
Human Priors (Our Approach):
LLM-driven TCG is guided by structured human expertise, a strategy central to our proposed SAGA framework (detailed in Section
3
).
2.1
Problem Definition
Formally, for a programming problem
P
∈
𝒫
𝑃
𝒫
P\in\mathcal{P}
italic_P ∈ caligraphic_P
with description
D
𝐷
D
italic_D
, input space
𝒳
P
subscript
𝒳
𝑃
\mathcal{X}_{P}
caligraphic_X start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
, and ground-truth solution
f
P
:
𝒳
P
→
𝒴
P
:
subscript
𝑓
𝑃
→
subscript
𝒳
𝑃
subscript
𝒴
𝑃
f_{P}:\mathcal{X}_{P}\to\mathcal{Y}_{P}
italic_f start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT : caligraphic_X start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT → caligraphic_Y start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
, a TCG method aims to produce a test case set
T
=
{
(
I
i
,
O
i
)
}
i
=
1
n
𝑇
superscript
subscript
subscript
𝐼
𝑖
subscript
𝑂
𝑖
𝑖
1
𝑛
T=\{(I_{i},O_{i})\}_{i=1}^{n}
italic_T = { ( italic_I start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT , italic_O start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) } start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT
, where each input
I
i
∈
𝒳
P
subscript
𝐼
𝑖
subscript
𝒳
𝑃
I_{i}\in\mathcal{X}_{P}
italic_I start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ∈ caligraphic_X start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
and its corresponding output
O
i
=
f
P
⁢
(
I
i
)
subscript
𝑂
𝑖
subscript
𝑓
𝑃
subscript
𝐼
𝑖
O_{i}=f_{P}(I_{i})
italic_O start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = italic_f start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT ( italic_I start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT )
.
To quantify the quality of such generated test suites, we employ two key metrics:
Definition 1
(Detection Rate (DR))
.
A solution-level metric, DR quantifies a test suite’s ability to detect errors in a specific incorrect candidate solution
S
≠
f
P
𝑆
subscript
𝑓
𝑃
S\neq f_{P}
italic_S ≠ italic_f start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
. It is the probability that
T
𝑇
T
italic_T
identifies at least one error in
S
𝑆
S
italic_S
:
ϵ
S
⁢
(
T
)
=
ℙ
⁢
(
∃
(
I
,
O
)
∈
T
⁢
s.t.
⁢
S
⁢
(
I
)
≠
O
)
.
subscript
italic-ϵ
𝑆
𝑇
ℙ
𝐼
𝑂
𝑇
s.t.
𝑆
𝐼
𝑂
\epsilon_{S}(T)=\mathbb{P}\left(\exists(I,O)\in T\text{ s.t. }S(I)\neq O\right).
italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T ) = roman_ℙ ( ∃ ( italic_I , italic_O ) ∈ italic_T s.t. italic_S ( italic_I ) ≠ italic_O ) .
If
E
i
=
{
S
⁢
(
I
i
)
≠
f
P
⁢
(
I
i
)
}
subscript
𝐸
𝑖
𝑆
subscript
𝐼
𝑖
subscript
𝑓
𝑃
subscript
𝐼
𝑖
E_{i}=\{S(I_{i})\neq f_{P}(I_{i})\}
italic_E start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = { italic_S ( italic_I start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) ≠ italic_f start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT ( italic_I start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) }
is the event that
S
𝑆
S
italic_S
fails on test case
i
𝑖
i
italic_i
, then
ϵ
S
⁢
(
T
)
=
1
−
ℙ
⁢
(
⋂
i
=
1
n
E
i
¯
)
.
subscript
italic-ϵ
𝑆
𝑇
1
ℙ
superscript
subscript
𝑖
1
𝑛
¯
subscript
𝐸
𝑖
\epsilon_{S}(T)=1-\mathbb{P}\left(\bigcap_{i=1}^{n}\overline{E_{i}}\right).
italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T ) = 1 - roman_ℙ ( ⋂ start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT over¯ start_ARG italic_E start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT end_ARG ) .
A higher average DR across many incorrect solutions indicates the test suite is effective at exposing diverse faults.
Definition 2
(Verifier Accuracy (VAcc))
.
A problem-level metric, VAcc assesses whether a test suite
T
𝑇
T
italic_T
can successfully identify all known incorrect solutions for a given problem
P
𝑃
P
italic_P
. Given
𝒮
wrong
⁢
(
P
)
=
{
S
:
𝒳
P
→
𝒴
P
∣
S
≠
f
P
}
subscript
𝒮
wrong
𝑃
conditional-set
𝑆
→
subscript
𝒳
𝑃
conditional
subscript
𝒴
𝑃
𝑆
subscript
𝑓
𝑃
\mathcal{S}_{\text{wrong}}(P)=\{S:\mathcal{X}_{P}\to\mathcal{Y}_{P}\mid S\neq f%
_{P}\}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT ( italic_P ) = { italic_S : caligraphic_X start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT → caligraphic_Y start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT ∣ italic_S ≠ italic_f start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT }
as the set of all incorrect solutions for
P
𝑃
P
italic_P
, the Verifier Accuracy is:
VAcc
⁢
(
T
)
=
𝕀
⁢
(
∀
S
∈
𝒮
wrong
⁢
(
P
)
,
∃
(
I
,
O
)
∈
T
⁢
s.t.
⁢
S
⁢
(
I
)
≠
O
)
,
VAcc
𝑇
𝕀
formulae-sequence
for-all
𝑆
subscript
𝒮
wrong
𝑃
𝐼
𝑂
𝑇
s.t.
𝑆
𝐼
𝑂
\mathrm{VAcc}(T)=\mathbb{I}\left(\forall S\in\mathcal{S}_{\text{wrong}}(P),%
\exists(I,O)\in T\text{ s.t. }S(I)\neq O\right),
roman_VAcc ( italic_T ) = roman_𝕀 ( ∀ italic_S ∈ caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT ( italic_P ) , ∃ ( italic_I , italic_O ) ∈ italic_T s.t. italic_S ( italic_I ) ≠ italic_O ) ,
where
𝕀
⁢
(
⋅
)
𝕀
⋅
\mathbb{I}(\cdot)
roman_𝕀 ( ⋅ )
is the indicator function.
VAcc
⁢
(
T
)
=
1
VAcc
𝑇
1
\mathrm{VAcc}(T)=1
roman_VAcc ( italic_T ) = 1
if
T
𝑇
T
italic_T
rejects every solution in
𝒮
wrong
⁢
(
P
)
subscript
𝒮
wrong
𝑃
\mathcal{S}_{\text{wrong}}(P)
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT ( italic_P )
, signifying perfect diagnostic capability.
2.2
Investigating Current TCG Paradigms and Their Limitations
Figure 3
:
Direct generation issues: (a) Low quality of LLM-generated tests. (b) High self-pass rates suggest model blind spots.
To ground our exploration of TCG effectiveness, we leverage
TCGBench
, a dataset we curated comprising 1840 recent programming problems from Atcoder, Codeforces, and Nowcoder, along with an average of 36.66 incorrect user submissions per problem. This rich resource (detailed in Appendix
D
) facilitates rigorous evaluation of TCG methodologies. Our analysis employ open-source LLMs: DeepSeek-V3-0324, Qwen2.5-72B-Instruct, and Qwen2.5-Coder-32B-Instruct with the greedy decoding strategy.
For paradigm 1: Is Direct LLM-based Test Case Generation Effective?
Directly prompting an LLM to generate complete test cases (inputs
I
i
LLM
superscript
subscript
𝐼
𝑖
LLM
I_{i}^{\mathrm{LLM}}
italic_I start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT start_POSTSUPERSCRIPT roman_LLM end_POSTSUPERSCRIPT
, outputs
O
i
LLM
superscript
subscript
𝑂
𝑖
LLM
O_{i}^{\mathrm{LLM}}
italic_O start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT start_POSTSUPERSCRIPT roman_LLM end_POSTSUPERSCRIPT
) from a problem description
P
𝑃
P
italic_P
, depends heavily on the LLM’s deep comprehension, particularly of edge cases. Our experiments (Figure
3
), involving LLM generation of 50 diverse test cases per problem, reveal the issues. The
retention rate
(proportion of valid tests post-verification against ground truth) is very low, indicating unreliable quality. This results in poor overall DR (often <60%) and VAcc (<10%). Moreover, LLM-generated solutions easily pass these self-generated tests. Notably, on AtCoder problems with historical official tests
4
4
4
Early AtCoder problems provided official test cases; however, from December 2024 onwards, test cases are no longer publicly available for new contests.
, LLM solutions performed substantially better on their own generated tests, suggesting such tests fail to challenge the model’s cognitive biases.
For paradigm 2: Can a Large Number of Inputs from an Input-Interpreter Approach Compensate for Low Quality?
The Input-Interpreter paradigm, where an LLM generates random inputs
I
i
Rand
∼
𝒳
P
similar-to
superscript
subscript
𝐼
𝑖
Rand
subscript
𝒳
𝑃
I_{i}^{\mathrm{Rand}}\sim\mathcal{X}_{P}
italic_I start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT start_POSTSUPERSCRIPT roman_Rand end_POSTSUPERSCRIPT ∼ caligraphic_X start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
for a ground-truth interpreter, is employed by benchmarks like LiveCodeBench
[
19
]
. While generating many tests is feasible, merely increasing the quantity
n
𝑛
n
italic_n
does not fundamentally improve the detection rate. This limitation arises from inherent correlations between test cases.
We propose here a corollary for the upper bound of the detection rate
5
5
5
The full derivation is provided in Appendix
C
.
:
{corollary}
[Asymptotic Saturation of Detection Rate]

As the number of generated test cases
n
→
∞
→
𝑛
n\to\infty
italic_n → ∞
, if
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
(the average probability of a single test detecting an error,
0
<
p
¯
<
1
0
¯
𝑝
1
0<\bar{p}<1
0 < over¯ start_ARG italic_p end_ARG < 1
) and
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
(the effective average positive correlation between detection events,
ρ
¯
eff
>
0
subscript
¯
𝜌
eff
0
\bar{\rho}_{\mathrm{eff}}>0
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT > 0
) are stable characteristics, the approximate upper bound on the detection rate
ϵ
S
⁢
(
T
)
subscript
italic-ϵ
𝑆
𝑇
\epsilon_{S}(T)
italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T )
converges to:
lim
n
→
∞
ϵ
S
⁢
(
T
)
≈
1
−
(
1
−
p
¯
)
1
/
ρ
¯
eff
<
1
.
subscript
→
𝑛
subscript
italic-ϵ
𝑆
𝑇
1
superscript
1
¯
𝑝
1
subscript
¯
𝜌
eff
1
\lim_{n\to\infty}\epsilon_{S}(T)\approx 1-(1-\bar{p})^{1/\bar{\rho}_{\mathrm{%
eff}}}<1.
roman_lim start_POSTSUBSCRIPT italic_n → ∞ end_POSTSUBSCRIPT italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T ) ≈ 1 - ( 1 - over¯ start_ARG italic_p end_ARG ) start_POSTSUPERSCRIPT 1 / over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT end_POSTSUPERSCRIPT < 1 .
This corollary implies that due to inter-test correlation
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
, simply increasing the number of random tests cannot guarantee 100% error detection; the detection rate will saturate. The underlying reasoning involves the concept of an "effective sample size"
n
eff
≈
n
/
(
1
+
(
n
−
1
)
⁢
ρ
¯
eff
)
subscript
𝑛
eff
𝑛
1
𝑛
1
subscript
¯
𝜌
eff
n_{\mathrm{eff}}\approx n/(1+(n-1)\bar{\rho}_{\mathrm{eff}})
italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT ≈ italic_n / ( 1 + ( italic_n - 1 ) over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT )
[
20
]
, which quantifies the diminishing utility of additional correlated tests. Our experiments on TCGBench (Figure
4
) confirm this: detection rates plateau (Fig.
4
(a)), and marginal gains diminish rapidly. Notably, plotting the detection rate against the logarithm of the number of test cases (Fig.
4
(b)) reveals a trend consistent with our derived theoretical upper bound, further validating the impact of correlation
ρ
¯
¯
𝜌
\bar{\rho}
over¯ start_ARG italic_ρ end_ARG
.
Figure 4
:
Experimental validation of Input-Interpreter (random sampling) limitations on TCGBench. (a) Detection rate vs. number of test cases (linear scale), showing clear saturation below 100%. (b) Detection rate vs. log of the number of test cases (semi-log scale), illustrating diminishing returns consistent with the theoretical upper bound
1
−
(
1
−
p
¯
)
n
eff
1
superscript
1
¯
𝑝
subscript
𝑛
eff
1-(1-\bar{p})^{n_{\mathrm{eff}}}
1 - ( 1 - over¯ start_ARG italic_p end_ARG ) start_POSTSUPERSCRIPT italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT end_POSTSUPERSCRIPT
, validating the impact of correlation
ρ
¯
¯
𝜌
\bar{\rho}
over¯ start_ARG italic_ρ end_ARG
.
Beyond DR and Acc, to more deeply quantify the intrinsic quality and efficiency of TCG strategies like SAGA (introduced in Section
3
), we employ two advanced metrics. These provide observable insights into test suite characteristics related to
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
(average test potency) and
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
(inter-test correlation):
•
Distinct Error Pattern Coverage (DEPC)
: For a test suite
𝒯
𝒯
\mathcal{T}
caligraphic_T
and
N
P
subscript
𝑁
𝑃
N_{P}
italic_N start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
problems, let
v
⁢
(
t
k
)
𝑣
subscript
𝑡
𝑘
v(t_{k})
italic_v ( italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT )
be the error pattern vector for test
t
k
subscript
𝑡
𝑘
t_{k}
italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT
. DEPC is
|
{
v
⁢
(
t
k
)
∣
t
k
∈
𝒯
⁢
and
⁢
‖
v
⁢
(
t
k
)
‖
1
≥
1
}
|
conditional-set
𝑣
subscript
𝑡
𝑘
subscript
𝑡
𝑘
𝒯
and
subscript
norm
𝑣
subscript
𝑡
𝑘
1
1
\Bigl{|}\bigl{\{}v(t_{k})\mid t_{k}\in\mathcal{T}\text{ and }\|v(t_{k})\|_{1}%
\geq 1\bigr{\}}\Bigr{|}
| { italic_v ( italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT ) ∣ italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT ∈ caligraphic_T and ∥ italic_v ( italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT ) ∥ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ≥ 1 } |
. The
Diversity Ratio
is
DEPC
⁢
(
𝒯
)
/
n
DEPC
𝒯
𝑛
\mathrm{DEPC}(\mathcal{T})/n
roman_DEPC ( caligraphic_T ) / italic_n
. Higher DEPC suggests lower
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
, indicating broader unique error detection.
•
Normalized Area Under the Accuracy-Number of test cases Curve (AUC-AccN)
: For Verifier Accuracy
A
⁢
c
⁢
c
⁢
(
k
)
𝐴
𝑐
𝑐
𝑘
Acc(k)
italic_A italic_c italic_c ( italic_k )
with
k
𝑘
k
italic_k
tests up to
N
𝑁
N
italic_N
,
AUC
⁢
@
⁢
N
≈
1
N
−
k
m
⁢
i
⁢
n
⁢
∑
i
=
k
m
⁢
i
⁢
n
N
−
1
A
⁢
c
⁢
c
⁢
(
k
i
)
+
A
⁢
c
⁢
c
⁢
(
k
i
+
1
)
2
⁢
(
k
i
+
1
−
k
i
)
.
AUC
@
N
1
𝑁
subscript
𝑘
𝑚
𝑖
𝑛
superscript
subscript
𝑖
subscript
𝑘
𝑚
𝑖
𝑛
𝑁
1
𝐴
𝑐
𝑐
subscript
𝑘
𝑖
𝐴
𝑐
𝑐
subscript
𝑘
𝑖
1
2
subscript
𝑘
𝑖
1
subscript
𝑘
𝑖
\mathrm{AUC@N}\approx\frac{1}{N-k_{min}}\sum_{i=k_{min}}^{N-1}\frac{Acc(k_{i})%
+Acc(k_{i+1})}{2}(k_{i+1}-k_{i}).
roman_AUC @ roman_N ≈ divide start_ARG 1 end_ARG start_ARG italic_N - italic_k start_POSTSUBSCRIPT italic_m italic_i italic_n end_POSTSUBSCRIPT end_ARG ∑ start_POSTSUBSCRIPT italic_i = italic_k start_POSTSUBSCRIPT italic_m italic_i italic_n end_POSTSUBSCRIPT end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_N - 1 end_POSTSUPERSCRIPT divide start_ARG italic_A italic_c italic_c ( italic_k start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) + italic_A italic_c italic_c ( italic_k start_POSTSUBSCRIPT italic_i + 1 end_POSTSUBSCRIPT ) end_ARG start_ARG 2 end_ARG ( italic_k start_POSTSUBSCRIPT italic_i + 1 end_POSTSUBSCRIPT - italic_k start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) .
Higher AUC@
N
𝑁
N
italic_N
indicates superior average verifier accuracy, reflecting potent (high
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) and efficiently diverse tests.
Detailed explanations and derivations for these metrics are in Appendix
B
.
3
SAGA: A Human-LLM Collaborative Framework for Advanced TCG
The preceding analysis (Section
2.2
) revealed critical limitations in prevalent Test Case Generation (TCG) paradigms, such as low test quality and homogeneity. To address this, we introduce
SAGA
(
S
trategic
A
dversarial & Constraint-differential
G
ener
A
tive workflow), a novel human-LLM collaborative framework (Figure
5
). SAGA systematically generates high-quality, diverse, and discriminative test suites by maximizing test potency (
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) and diversity (lowering correlation
ρ
¯
¯
𝜌
\bar{\rho}
over¯ start_ARG italic_ρ end_ARG
). Additionally, we trained
TCGCoder-7B
, a SAGA-distilled 7B specialist model from 15,000 problems (details in Appendix
J
), as a strong TCG baseline and reference.
3.1
The SAGA Framework: Integrating Human Expertise
Table 1
:
Initial Impact of Incorporating Simple Human Priors (
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
) into Basic TCG Paradigms on AtCoder Results (Accuracy@50).
Method
Accuracy@50
Direct Gen. (Paradigm 1)
11.30%
Direct Gen. + Simple Priors
15.06%
(+3.76%)
Input-Interpreter (Paradigm 2)
23.36%
Input-Interpreter + Simple Priors
27.95%
(+4.59%)
Recognizing the limitations of naive TCG, SAGA explores the integration of human expertise. Intuitively, leveraging human problem-solving insights should enhance TCG. Table
1
shows that incorporating simple human priors (e.g., boundary values from
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
) into basic TCG paradigms on TCGBench-Full yields some improvement. However, these gains are often marginal, failing to fully exploit LLM potential for detecting complex flaws. While methods like EvalPlus
[
27
]
use human solutions, it’s often for mutating seeds or formatting inputs, not deeply guiding large-scale challenging test generation.
SAGA advances beyond such superficial integration. As depicted in Figure
5
, it deeply incorporates multifaceted human programming insights—from both correct solutions (GroundTruth,
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
) and incorrect submissions (Human Bugs,
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
)—with LLM reasoning via a structured, dual-pronged analytical strategy. An LLM is fed the problem description
P
𝑃
P
italic_P
and insights gleaned from human solutions through a customized prompting module. This process generates Python
Case Scripts
to produce test inputs, accompanied by
Math Explanations
and
Self-Validation
code to ensure correctness and relevance. The generated inputs are then processed by an
Interpreter
(ground-truth solution) to yield test outputs, forming the final test cases. SAGA’s core analytical dimensions are:
Figure 5
:
Overview of the SAGA framework. SAGA leverages both GroundTruth (correct human solutions) and Human Bugs (incorrect submissions) alongside the Problem description. An LLM performs Multi-Dimensional Analysis and Differential Analysis to generate Python Case Scripts for test input synthesis. These scripts are accompanied by Math Explanations (capturing testing strategies and constraints) and Self-Validation code. The generated Test Inputs are then passed to an Interpreter (ground-truth solution) to produce Test Outputs, forming the final test cases.
•
Multidimensional Analysis (Leveraging
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
):
This dimension extracts profound insights from correct solutions to engineer challenging tests. It involves:
1.
Constraint Handling Differences:
Discrepancies in how
S
wrong
subscript
𝑆
wrong
S_{\text{wrong}}
italic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
and
S
correct
′
superscript
subscript
𝑆
correct
′
S_{\text{correct}}^{\prime}
italic_S start_POSTSUBSCRIPT correct end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
manage problem-specific constraints.
2.
Defense Pattern Deconstruction:
This is where the
Math Explanation
component (Figure
5
) plays a key role. Diverse defensive logic and problem-solving strategies within
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
are decomposed into formal mathematical or logical constraints (e.g., "equivalence class: player pairs", "boundary_value: [(1,2), (N,N-1)]"). This allows SAGA to target singularities, extremal values, or specific structural properties, guiding the generation of edge and adversarial test cases.
3.
Targeted Test Generation:
Using these constraints and pitfalls to guide the LLM in constructing challenging test inputs
I
𝐼
I
italic_I
via the
Case Scripts
.
This analytical approach aims to generate test cases that not only cover a wide spectrum of valid scenarios, including complex boundary conditions and intricate interactions, but also enhance test diversity (lowering
ρ
¯
¯
𝜌
\bar{\rho}
over¯ start_ARG italic_ρ end_ARG
) and individual test potency (increasing
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
).
•
Differential Analysis (Leveraging
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
):
This addresses error types missed by analyzing only correct solutions. It compares failed submissions (
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
) with their corrected versions (
S
correct
′
superscript
subscript
𝑆
correct
′
S_{\text{correct}}^{\prime}
italic_S start_POSTSUBSCRIPT correct end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
) to find inputs
I
diff
subscript
𝐼
diff
I_{\text{diff}}
italic_I start_POSTSUBSCRIPT diff end_POSTSUBSCRIPT
where
S
wrong
⁢
(
I
diff
)
≠
S
correct
′
⁢
(
I
diff
)
subscript
𝑆
wrong
subscript
𝐼
diff
superscript
subscript
𝑆
correct
′
subscript
𝐼
diff
S_{\text{wrong}}(I_{\text{diff}})\neq S_{\text{correct}}^{\prime}(I_{\text{%
diff}})
italic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT ( italic_I start_POSTSUBSCRIPT diff end_POSTSUBSCRIPT ) ≠ italic_S start_POSTSUBSCRIPT correct end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ( italic_I start_POSTSUBSCRIPT diff end_POSTSUBSCRIPT )
, revealing common error patterns. This targets:
1.
Constraint Handling Differences:
Discrepancies in how
S
wrong
subscript
𝑆
wrong
S_{\text{wrong}}
italic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
and
S
correct
′
superscript
subscript
𝑆
correct
′
S_{\text{correct}}^{\prime}
italic_S start_POSTSUBSCRIPT correct end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
manage problem-specific constraints.
2.
Lack of Defensive Completeness:
Deficiencies in
S
wrong
subscript
𝑆
wrong
S_{\text{wrong}}
italic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
related to handling edge cases or boundary inputs, as revealed by comparison with
S
correct
′
superscript
subscript
𝑆
correct
′
S_{\text{correct}}^{\prime}
italic_S start_POSTSUBSCRIPT correct end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
.
3.
Failure Pattern Analysis:
Generating specific inputs that trigger failures in
S
wrong
subscript
𝑆
wrong
S_{\text{wrong}}
italic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
but are correctly handled by
S
correct
′
superscript
subscript
𝑆
correct
′
S_{\text{correct}}^{\prime}
italic_S start_POSTSUBSCRIPT correct end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
.
The incorporation of these differentially identified inputs
I
diff
subscript
𝐼
diff
I_{\text{diff}}
italic_I start_POSTSUBSCRIPT diff end_POSTSUBSCRIPT
into the test suite
T
𝑇
T
italic_T
creates a more rigorous and challenging evaluation framework, as it specifically targets known failure modes, thereby substantially increasing the discriminative power of the resulting verifier.
The
Self-Validation
scripts (Figure
5
) ensure that generated test inputs adhere to problem constraints and the intended testing strategy before execution.
For Multidimensional Analysis, SAGA leverages insights from 10 distinct, correct user solutions per problem to broaden perspective. In Differential Analysis, it meticulously pairs a user’s correct solution with their most recent preceding incorrect submission. This focus on closely related yet differing attempts enhances SAGA’s ability to identify subtle error patterns and generate challenging corner cases.
By synergistically combining these refined analytical dimensions, SAGA produces comprehensive and highly effective test suites.
3.2
Experimental Validation of SAGA
SAGA’s effectiveness was initially validated on the
TCGBench
. Figure
6
visually summarizes SAGA’s multifaceted superiority in this context, comparing it against the random Input-Interpreter baseline and its core analytical components (Multidimensional Analysis and Differential Analysis).
Figure 6
:
SAGA outperforms the Baseline (Random Input-Interpreter) and its individual analytical components (Multidimensional Analysis leveraging
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
; Differential Analysis leveraging
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
) on the AtCoder subset of the full
TCGBench
across: (a) Detection Rate, (b) Verifier Accuracy (with AUC@50 values), (c) Distinct Error Pattern Coverage (DEPC), and (d) Diversity Ratio. Dotted lines in (a) & (b) show baseline performance at
n
=
100
𝑛
100
n=100
italic_n = 100
. See Appendix
F
for SAGA’s performance on other platforms within the full TCGBench.
Key Findings from Comparison on TCGBench (Fig.
6
):
SAGA markedly improves
solution vetting capabilities
: its DR surpasses 93.81% (vs. baseline’s 82.85% at
n
=
100
𝑛
100
n=100
italic_n = 100
) and VAcc reaches 41.33% (vs. baseline’s 21.89% at
n
=
100
𝑛
100
n=100
italic_n = 100
) with only 50 tests. SAGA’s AUC@50 (0.5445) more than doubles the baseline’s (0.2586), showcasing superior efficiency.
SAGA also generates test suites of
superior intrinsic quality
: it achieves the highest DEPC (broader error coverage, lower
ρ
¯
¯
𝜌
\bar{\rho}
over¯ start_ARG italic_ρ end_ARG
) and Diversity Ratio (more efficient error discovery per test). Both Multidimensional and Differential analysis components individually outperform the baseline, but their synergy in SAGA yields optimal results. This robustly validates SAGA’s systematic leveraging of human insights on a large scale.
3.2.1
Main Results and Analysis on TCGBench-Lite
For focused main comparisons and ablation studies, we curated
TCGBench-Lite
, a challenging subset of 270 problems from AtCoder, Codeforces, and Nowcoder contests since June 2024. This ensures contemporary relevance and minimizes potential data leakage. TCGBench-Lite includes an average of 41.41 incorrect submissions (
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
) per problem. Its difficulty distribution (Easy: 27.04%, Medium: 32.59%, Hard: 40.37%) was determined by platform tags and contest characteristics (details in Appendix
E
). This curated set allows for rigorous yet manageable evaluation. Unless specified, all LLM-driven methods use DeepSeek-V3-0324 as the backbone for fair comparison. We evaluate against the
Input-Interpreter (LiveCodeBench-style random sampling)
,
TestChain
[
22
]
,
EvalPlus
[
27
]
, and our SAGA-distilled
TCGCoder-7B
. Results are in Table
2
.
Table 2
:
Experimental Results: Main Comparison of SAGA with Baselines and Ablation Studies on TCGBench-Lite. Metrics are DR@
k
𝑘
k
italic_k
, VAcc@
k
𝑘
k
italic_k
, AUC@50, and DivRatio@50. All methods use DeepSeek-V3-0324 backbone unless specified in ablation.
Method / Configuration
DR@20
DR@50
VAcc@20
VAcc@50
AUC@50
DivRatio@50
Main Comparison with Baseline TCG Methods
TestChain
[
22
]
65.91%
68.31%
8.12%
11.88%
0.0841
50.09%
Input-Interpreter (LiveCodeBench-style
[
19
]
)
77.84%
81.07%
12.36%
16.72%
0.1234
79.42%
EvalPlus
[
27
]
67.52%
71.12%
11.56%
15.15%
0.1139
79.27%
TCGCoder-7B (SAGA-distilled model)
85.14%
89.44%
17.93%
29.11%
0.1890
94.43%
SAGA (DeepSeek-V3 Backbone)
85.66%
90.62%
22.40%
32.58%
0.2228
94.06%
SAGA Ablation Studies
Analytical Component Ablation
SAGA w/ Multidim. Analysis only
84.51%
88.00%
20.70%
26.05%
0.1923
95.81%
SAGA w/ Differential Analysis only
84.31%
88.16%
19.85%
26.67%
0.1926
94.41%
Prompt Design Ablation
SimpleCOT Prompt for SAGA
83.36%
84.54%
15.61%
19.11%
0.1424
96.23%
Random Input w/ GT for SAGA
82.31%
86.64%
16.44%
22.70%
0.1616
85.38%
EvalPlus w/ GT for SAGA
76.72%
79.56%
11.67%
20.44%
0.1278
89.49%
Base LLM Ablation for SAGA
SAGA w/ Qwen2.5-Coder-7B-Instruct
78.88%
79.78%
19.70%
22.96%
0.1810
96.80%
SAGA w/ Qwen2.5-72B-Instruct
82.77%
85.08%
20.30%
26.46%
0.1943
94.92%
SAGA w/ Qwen2.5-Coder-32B-Instruct
86.25%
90.54%
20.74%
32.73%
0.2139
94.72%
Analysis of Main Comparison (Table
2
):
SAGA’s structured integration of human insights yields substantial gains over other TCG methods on TCGBench-Lite. Notably, SAGA achieves an AUC@50 of 0.2228, surpassing the Input-Interpreter (0.1234), which is limited by random sampling’s homogeneity. This highlights SAGA’s ability to produce more consistently effective tests. While EvalPlus achieves a high raw Diversity Ratio through mutation, its lower AUC@50 (0.1278) suggests that SAGA’s deep analysis of human solutions is more critical for overall verifier quality than mere test variety. TestChain, lacking rich human priors, performs weakest.
Crucially, our SAGA-distilled
TCGCoder-7B
(AUC@50: 0.1890) outperforms all these established baselines, even when they utilize a much larger backbone model (DeepSeek-V3-0324). This demonstrates SAGA’s potential to distill effective TCG strategies into smaller, specialized, and highly capable models, thereby making advanced TCG more accessible.
Analysis of Ablation Studies (Table
2
):
Value of Structured Human Insights:
Isolating SAGA’s Multidimensional Analysis (leveraging
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
) and Differential Analysis (leveraging
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
) reveals that both significantly outperform simpler prompting (SimpleCOT) and the Input-Interpreter baseline in terms of AUC@50. This underscores that structured analysis of human solutions, whether correct or incorrect, is fundamental for higher-quality verifiers. The full SAGA framework, synergistically combining both analytical dimensions, achieves the optimal overall quality (highest AUC@50), confirming their complementary benefits.
Importance of Prompt Design:
The substantial performance degradation when replacing SAGA’s detailed, insight-driven prompts with generic CoT (SimpleCOT) highlights that the
methodology
of integrating human insights is as critical as the insights themselves for effective TCG.
Robustness Across LLMs:
SAGA demonstrates commendable robustness when paired with different LLM backbones. While peak performance on specific metrics can vary with the LLM (e.g., SAGA with Qwen2.5-Coder-32B-Instruct yields the highest VAcc@50), the SAGA framework with its default DeepSeek-V3 backbone consistently provides the best overall AUC@50. This indicates SAGA’s comprehensive design is more impactful for holistic verifier quality than relying on specific LLM capabilities or optimizing for isolated metrics like Diversity Ratio. Notably, SAGA also shows strong performance with Qwen2.5-Coder-7B-Instruct (TCGCoder-7B’s base model), further validating SAGA’s efficacy on smaller, specialized coder models.
4
Towards Advanced Applications of SAGA
SAGA’s proven capability in generating high-quality, diverse, and discriminative test suites (Section
3
) enables advancements in LLM code evaluation and training. This section primarily explores the development of a superior code generation benchmark,
CodeComPass
, while also noting the potential for SAGA-enhanced verifiers to contribute to more reliable Reinforcement Learning from Verifiable Rewards (RLVR).
CodeCompass: A SAGA-Enhanced Benchmark for Code Generation Evaluation
To address the need for more challenging and discerning evaluation of LLM code generation models, we introduce
CodeCompass
. The verifiers within CodeCompass are synthesized using SAGA for the 270 contemporary problems that also constitute TCGBench-Lite (detailed in Appendix
E
), ensuring relevance and minimizing data leakage risks. Each problem in CodeCompass features a rich test suite, averaging 50.54 SAGA-generated test cases, meticulously curated to ensure comprehensive coverage (with additional manual curation applied if initial generation yielded fewer than a target threshold).
For comparative analysis of verifier quality and impact on model evaluation, we focus on a shared subset of 101 AtCoder problems that overlap between our CodeCompass verifiers and the test suites used by LiveCodeBench-v6. This allows for a direct comparison on common ground.
Table 3
:
Verifier Quality: CodeCompass vs. LCB-v6 (Shared Subset, @40 tests).
Metric
LiveCodeBench-v6
CodeCompass
DR@40
78.85%
93.44%
VAcc@40
19.61%
30.39%
DivRatio@40
53.56%
96.69%
AUC@40
0.1388
0.1980
Figure 7
:
Avg. Pass@1 by Difficulty.
Figure 8
:
Model Ranking Changes.
Superior Verifier Quality of CodeCompass.
We first establish the intrinsic quality of CodeCompass verifiers using core TCG metrics against those of LiveCodeBench-v6 on the shared AtCoder subset (Table
3
). CodeCompass demonstrates markedly higher efficacy in identifying faulty solutions, greater efficiency in discovering unique error patterns (Diversity Ratio@40: +43.13%), and faster convergence to quality. This confirms that SAGA produces verifiers that are intrinsically more diverse, discriminative, and effective.
Enhanced Discriminative Power for Code Generation Model Evaluation.
This superior verifier quality translates directly to a more challenging and discerning evaluation for LLM code generation models. As shown in Figure
7
, CodeComPass consistently elicits lower average Pass@1 rates across all problem difficulties compared to LiveCodeBench-v6 on the shared subset, indicating a more rigorous test. Critically, this increased stringency enhances discriminative power (Figure
8
): when evaluated on CodeComPass, the average Pass@1 for various models drops by a relative 9.56% compared to their performance on LiveCodeBench-v6. This relative decrease leads to a re-ranking of models (e.g., Qwen2.5-72B and Qwen2.5-Coder-32B switch relative positions). This ability to expose nuanced differences in model capabilities confirms that CodeComPass offers a more robust and insightful assessment of true code generation proficiency.
Meanwhile, the superior SAGA-generated verifiers, exemplified by CodeComPass, promise to enhance Reinforcement Learning from Verifiable Rewards (RLVR) frameworks
[
8
,
10
]
by delivering more accurate reward signals and mitigating reward hacking, thereby fostering more robust and capable code generation models.
5
Conclusion
This paper critically re-evaluates LLM-based Test Case Generation (TCG), highlighting current verifier limitations and formalizing key quality metrics alongside TCGBench, a foundational TCG research dataset. We introduce
SAGA
, a novel human-LLM collaborative framework that integrates human programming insights with LLM reasoning to demonstrably generate superior test suites. Leveraging SAGA, we developed
CodeComPass
, an enhanced verifier suite for robust code generation evaluation, and distilled
TCGCoder-7B
, a specialized, efficient TCG model. Collectively, these contributions significantly advance reliable LLM code evaluation and pave the way for future automated test synthesis and effective adversarial testing.
References
Anand et al. [2013]
Saswat Anand, Edmund K. Burke, Tsong Yueh Chen, John A. Clark, Myra B. Cohen, Wolfgang Grieskamp, Mark Harman, Mary Jean Harrold, and Phil McMinn.
An orchestrated survey of methodologies for automated software test case generation.
J. Syst. Softw.
, 86(8):1978–2001, 2013.
doi:
10.1016/J.JSS.2013.02.061
.
URL
https://doi.org/10.1016/j.jss.2013.02.061
.
Anil et al. [2023]
Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M. Dai, Anja Hauth, Katie Millican, David Silver, Slav Petrov, Melvin Johnson, Ioannis Antonoglou, Julian Schrittwieser, Amelia Glaese, Jilin Chen, Emily Pitler, Timothy P. Lillicrap, Angeliki Lazaridou, Orhan Firat, James Molloy, Michael Isard, Paul Ronald Barham, Tom Hennigan, Benjamin Lee, Fabio Viola, Malcolm Reynolds, Yuanzhong Xu, Ryan Doherty, Eli Collins, Clemens Meyer, Eliza Rutherford, Erica Moreira, Kareem Ayoub, Megha Goel, George Tucker, Enrique Piqueras, Maxim Krikun, Iain Barr, Nikolay Savinov, Ivo Danihelka, Becca Roelofs, Anaïs White, Anders Andreassen, Tamara von Glehn, Lakshman Yagati, Mehran Kazemi, Lucas Gonzalez, Misha Khalman, Jakub Sygnowski, and et al.
Gemini: A family of highly capable multimodal models.
CoRR
, abs/2312.11805, 2023.
doi:
10.48550/ARXIV.2312.11805
.
URL
https://doi.org/10.48550/arXiv.2312.11805
.
Austin et al. [2021]
Jacob Austin, Augustus Odena, Maxwell I. Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie J. Cai, Michael Terry, Quoc V. Le, and Charles Sutton.
Program synthesis with large language models.
CoRR
, abs/2108.07732, 2021.
URL
https://arxiv.org/abs/2108.07732
.
Beyleda and Gruhn [2003]
S. Beyleda and V. Gruhn.
Bintest - search-based test case generation.
In
Proceedings 27th Annual International Computer Software and Applications Conference. COMPAC 2003
, pages 28–33, 2003.
doi:
10.1109/CMPSAC.2003.1245318
.
Cadar and Sen [2013]
Cristian Cadar and Koushik Sen.
Symbolic execution for software testing: three decades later.
Commun. ACM
, 56(2):82–90, 2013.
doi:
10.1145/2408776.2408795
.
URL
https://doi.org/10.1145/2408776.2408795
.
Chen et al. [2021]
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
Evaluating large language models trained on code.
CoRR
, abs/2107.03374, 2021.
URL
https://arxiv.org/abs/2107.03374
.
Chen et al. [2023]
Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou.
Teaching large language models to self-debug.
arXiv preprint arXiv:2304.05128
, 2023.
DeepSeek-AI [2025]
DeepSeek-AI.
Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025.
URL
https://arxiv.org/abs/2501.12948
.
Duan et al. [2022]
Zhiyu Duan, Yujia Li, Pubo Ma, Xiaodong Gou, and Shunkun Yang.
A multi-layer fault triggering framework based on evolutionary strategy guided symbolic execution for automated test case generation.
In
22nd IEEE International Conference on Software Quality, Reliability, and Security, QRS 2022 - Companion, Guangzhou, China, December 5-9, 2022
, pages 255–262. IEEE, 2022.
doi:
10.1109/QRS-C57518.2022.00045
.
URL
https://doi.org/10.1109/QRS-C57518.2022.00045
.
El-Kishky et al. [2025]
Ahmed El-Kishky, Alexander Wei, Andre Saraiva, Borys Minaiev, Daniel Selsam, David Dohan, Francis Song, Hunter Lightman, Ignasi Clavera Gilaberte, Jakub Pachocki, Jerry Tworek, Lorenz Kuhn, Lukasz Kaiser, Mark Chen, Max Schwarzer, Mostafa Rohaninejad, Nat McAleese, o3 contributors, Oleg Mürk, Rhythm Garg, Rui Shu, Szymon Sidor, Vineet Kosaraju, and Wenda Zhou.
Competitive programming with large reasoning models.
CoRR
, abs/2502.06807, 2025.
doi:
10.48550/ARXIV.2502.06807
.
URL
https://doi.org/10.48550/arXiv.2502.06807
.
Fioraldi et al. [2023]
Andrea Fioraldi, Alessandro Mantovani, Dominik Christian Maier, and Davide Balzarotti.
Dissecting american fuzzy lop: A fuzzbench evaluation.
ACM Trans. Softw. Eng. Methodol.
, 32(2):52:1–52:26, 2023.
doi:
10.1145/3580596
.
URL
https://doi.org/10.1145/3580596
.
Fitzmaurice et al. [2012]
Garrett M Fitzmaurice, Nan M Laird, and James H Ware.
Applied longitudinal analysis
.
John Wiley & Sons, 2012.
Guo et al. [2024]
Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Y. Wu, Y. K. Li, Fuli Luo, Yingfei Xiong, and Wenfeng Liang.
Deepseek-coder: When the large language model meets programming - the rise of code intelligence.
CoRR
, abs/2401.14196, 2024.
doi:
10.48550/ARXIV.2401.14196
.
URL
https://doi.org/10.48550/arXiv.2401.14196
.
Harman et al. [2012]
Mark Harman, S. Afshin Mansouri, and Yuanyuan Zhang.
Search-based software engineering: Trends, techniques and applications.
ACM Comput. Surv.
, 45(1), December 2012.
ISSN 0360-0300.
doi:
10.1145/2379776.2379787
.
URL
https://doi.org/10.1145/2379776.2379787
.
Huang et al. [2024a]
Dong Huang, Qingwen Bu, Yuhao Qing, and Heming Cui.
Codecot: Tackling code syntax errors in cot reasoning for code generation, 2024a.
URL
https://arxiv.org/abs/2308.08784
.
Huang et al. [2024b]
Dong Huang, Jie M. Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming Cui.
Agentcoder: Multi-agent-based code generation with iterative testing and optimisation, 2024b.
URL
https://arxiv.org/abs/2312.13010
.
Hui et al. [2024]
Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Kai Dang, et al.
Qwen2. 5-coder technical report.
arXiv preprint arXiv:2409.12186
, 2024.
Jain et al. [2024a]
Kush Jain, Gabriel Synnaeve, and Baptiste Rozière.
Testgeneval: A real world unit test generation and test completion benchmark, 2024a.
Jain et al. [2024b]
Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
Livecodebench: Holistic and contamination free evaluation of large language models for code.
arXiv preprint arXiv:2403.07974
, 2024b.
Kish [1965]
Leslie Kish.
Survey sampling. new york: John wesley & sons.
Am Polit Sci Rev
, 59(4):1025, 1965.
Le et al. [2022]
Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven Chu-Hong Hoi.
Coderl: Mastering code generation through pretrained models and deep reinforcement learning.
In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors,
Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022
, 2022.
URL
http://papers.nips.cc/paper_files/paper/2022/hash/8636419dea1aa9fbd25fc4248e702da4-Abstract-Conference.html
.
Li and Yuan [2024]
Kefan Li and Yuan Yuan.
Large language models as test case generators: Performance evaluation and enhancement.
CoRR
, abs/2404.13340, 2024.
doi:
10.48550/ARXIV.2404.13340
.
URL
https://doi.org/10.48550/arXiv.2404.13340
.
Li et al. [2023a]
Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue Zhuo, Thomas Wang, Olivier Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro, Oleh Shliazhko, Nicolas Gontier, Nicholas Meade, Armel Zebaze, Ming-Ho Yee, Logesh Kumar Umapathi, Jian Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy V, Jason T. Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey, Zhihan Zhang, Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu, Swayam Singh, Sasha Luccioni, Paulo Villegas, Maxim Kunakov, Fedor Zhdanov, Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire Schlesinger, Hailey Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson, Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried, Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf,
Arjun Guha, Leandro von Werra, and Harm de Vries.
Starcoder: may the source be with you!
Trans. Mach. Learn. Res.
, 2023, 2023a.
URL
https://openreview.net/forum?id=KoFOg41haE
.
Li et al. [2023b]
Rongao Li, Jie Fu, Bo-Wen Zhang, Tao Huang, Zhihong Sun, Chen Lyu, Guang Liu, Zhi Jin, and Ge Li.
Taco: Topics in algorithmic code generation dataset.
arXiv preprint arXiv:2312.14852
, 2023b.
Li et al. [2022]
Yujia Li, David H. Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
Competition-level code generation with alphacode.
CoRR
, abs/2203.07814, 2022.
doi:
10.48550/ARXIV.2203.07814
.
URL
https://doi.org/10.48550/arXiv.2203.07814
.
Liu and Liang [1997]
Guanghan Liu and Kung-Yee Liang.
Sample size calculations for studies with correlated observations.
Biometrics
, pages 937–947, 1997.
Liu et al. [2023]
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang.
Is your code generated by chatGPT really correct? rigorous evaluation of large language models for code generation.
In
Thirty-seventh Conference on Neural Information Processing Systems
, 2023.
URL
https://openreview.net/forum?id=1qvx610Cu7
.
Liu et al. [2024a]
Jiawei Liu, Songrun Xie, Junhao Wang, Yuxiang Wei, Yifeng Ding, and Lingming Zhang.
Evaluating language models for efficient code generation.
In
First Conference on Language Modeling
, 2024a.
URL
https://openreview.net/forum?id=IBCBMeAhmC
.
Liu et al. [2024b]
Kaibo Liu, Yudong Han, Yiyang Liu, Jie M. Zhang, Zhenpeng Chen, Federica Sarro, Gang Huang, and Yun Ma.
Trickybugs: A dataset of corner-case bugs in plausible programs.
In
2024 IEEE/ACM 21st International Conference on Mining Software Repositories (MSR)
, pages 113–117, 2024b.
Lohr [2021]
Sharon L Lohr.
Sampling: design and analysis
.
Chapman and Hall/CRC, 2021.
Ma et al. [2025]
Zeyao Ma, Xiaokang Zhang, Jing Zhang, Jifan Yu, Sijia Luo, and Jie Tang.
Dynamic scaling of unit tests for code reward modeling, 2025.
URL
https://arxiv.org/abs/2501.01054
.
Manès et al. [2021]
Valentin J.M. Manès, HyungSeok Han, Choongwoo Han, Sang Kil Cha, Manuel Egele, Edward J. Schwartz, and Maverick Woo.
The art, science, and engineering of fuzzing: A survey.
IEEE Transactions on Software Engineering
, 47(11):2312–2331, 2021.
doi:
10.1109/TSE.2019.2946563
.
McMinn [2004]
Phil McMinn.
Search-based software test data generation: a survey.
Softw. Test. Verification Reliab.
, 14(2):105–156, 2004.
doi:
10.1002/STVR.294
.
URL
https://doi.org/10.1002/stvr.294
.
Ni et al. [2023]
Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-Tau Yih, Sida I. Wang, and Xi Victoria Lin.
LEVER: learning to verify language-to-code generation with execution.
In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett, editors,
International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA
, volume 202 of
Proceedings of Machine Learning Research
, pages 26106–26128. PMLR, 2023.
URL
https://proceedings.mlr.press/v202/ni23b.html
.
OpenAI [2023]
OpenAI.
GPT-4 technical report.
CoRR
, abs/2303.08774, 2023.
doi:
10.48550/ARXIV.2303.08774
.
URL
https://doi.org/10.48550/arXiv.2303.08774
.
Pacheco and Ernst [2007]
Carlos Pacheco and Michael D. Ernst.
Randoop: feedback-directed random testing for java.
In
Companion to the 22nd ACM SIGPLAN Conference on Object-Oriented Programming Systems and Applications Companion
, OOPSLA ’07, page 815–816, New York, NY, USA, 2007. Association for Computing Machinery.
ISBN 9781595938657.
doi:
10.1145/1297846.1297902
.
URL
https://doi.org/10.1145/1297846.1297902
.
Penedo et al. [2025]
Guilherme Penedo, Anton Lozhkov, Hynek Kydlíček, Loubna Ben Allal, Edward Beeching, Agustín Piqueres Lajarín, Quentin Gallouédec, Nathan Habib, Lewis Tunstall, and Leandro von Werra.
Codeforces cots.
https://huggingface.co/datasets/open-r1/codeforces-cots
, 2025.
Rozière et al. [2023]
Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton-Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet, Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and Gabriel Synnaeve.
Code llama: Open foundation models for code.
CoRR
, abs/2308.12950, 2023.
doi:
10.48550/ARXIV.2308.12950
.
URL
https://doi.org/10.48550/arXiv.2308.12950
.
Serebryany and the LLVM Team [2016]
Kostya Serebryany and the LLVM Team.
libFuzzer – a library for coverage-guided fuzz testing.
https://llvm.org/docs/LibFuzzer.html
, 2016.
Accessed: 2024-04-15.
Shojaee et al. [2023]
Parshin Shojaee, Aneesh Jain, Sindhu Tipirneni, and Chandan K Reddy.
Execution-based code generation using deep reinforcement learning.
arXiv preprint arXiv:2301.13816
, 2023.
Wang et al. [2024]
Wenhan Wang, Chenyuan Yang, Zhijie Wang, Yuheng Huang, Zhaoyang Chu, Da Song, Lingming Zhang, An Ran Chen, and Lei Ma.
TESTEVAL: benchmarking large language models for test case generation.
CoRR
, abs/2406.04531, 2024.
doi:
10.48550/ARXIV.2406.04531
.
URL
https://doi.org/10.48550/arXiv.2406.04531
.
Wang et al. [2021]
Yue Wang, Weishi Wang, Shafiq R. Joty, and Steven C. H. Hoi.
Codet5: Identifier-aware unified pre-trained encoder-decoder models for code understanding and generation.
In Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and Scott Wen-tau Yih, editors,
Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021
, pages 8696–8708. Association for Computational Linguistics, 2021.
doi:
10.18653/V1/2021.EMNLP-MAIN.685
.
URL
https://doi.org/10.18653/v1/2021.emnlp-main.685
.
Wang et al. [2023]
Yue Wang, Hung Le, Akhilesh Gotmare, Nghi D. Q. Bui, Junnan Li, and Steven C. H. Hoi.
Codet5+: Open code large language models for code understanding and generation.
In Houda Bouamor, Juan Pino, and Kalika Bali, editors,
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023
, pages 1069–1088. Association for Computational Linguistics, 2023.
doi:
10.18653/V1/2023.EMNLP-MAIN.68
.
URL
https://doi.org/10.18653/v1/2023.emnlp-main.68
.
Yang et al. [2024]
An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Yang Fan, Yang Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zhihao Fan.
Qwen2 technical report.
arXiv preprint arXiv:2407.10671
, 2024.
Yatoh et al. [2015]
Kohsuke Yatoh, Kazunori Sakamoto, Fuyuki Ishikawa, and Shinichi Honiden.
Feedback-controlled random test generation.
In Michal Young and Tao Xie, editors,
Proceedings of the 2015 International Symposium on Software Testing and Analysis, ISSTA 2015, Baltimore, MD, USA, July 12-17, 2015
, pages 316–326. ACM, 2015.
doi:
10.1145/2771783.2771805
.
URL
https://doi.org/10.1145/2771783.2771805
.
Zeng et al. [2025]
Huaye Zeng, Dongfu Jiang, Haozhe Wang, Ping Nie, Xiaotong Chen, and Wenhu Chen.
Acecoder: Acing coder rl via automated test-case synthesis.
ArXiv
, 2502.01718, 2025.
Zheng et al. [2023]
Qinkai Zheng, Xiao Xia, Xu Zou, Yuxiao Dong, Shan Wang, Yufei Xue, Lei Shen, Zihan Wang, Andi Wang, Yang Li, Teng Su, Zhilin Yang, and Jie Tang.
Codegeex: A pre-trained model for code generation with multilingual benchmarking on humaneval-x.
In
Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining
, KDD ’23, page 5673–5684, New York, NY, USA, 2023. Association for Computing Machinery.
ISBN 9798400701030.
doi:
10.1145/3580305.3599790
.
URL
https://doi.org/10.1145/3580305.3599790
.
Zhuo et al. [2024]
Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu, Wenhao Yu, Ratnadira Widyasari, Imam Nur Bani Yusuf, Haolan Zhan, Junda He, Indraneil Paul, et al.
Bigcodebench: Benchmarking code generation with diverse function calls and complex instructions.
arXiv preprint arXiv:2406.15877
, 2024.
Appendix
Appendix A
Related Works
A.1
Advancements and Challenges in LLM-based Code Generation and Evaluation
Large Language Models (LLMs) have revolutionized automated code generation, with models like AlphaCode
[
25
]
, GPT-4
[
35
]
, Gemini
[
2
]
, and specialized code models such as CodeT5
[
42
,
43
]
, StarCoder
[
23
]
, DeepSeek Coder
[
13
]
, CodeLlama
[
38
]
, and Qwen2.5-Coder
[
44
,
17
]
demonstrating remarkable capabilities. These models, whether trained via Supervised Fine-Tuning or enhanced through Reinforcement Learning (RL) with execution feedback (e.g., AlphaCode
[
25
]
, PPOCoder
[
40
]
, CodeRL
[
21
]
), increasingly match or exceed human performance on diverse programming benchmarks.
The reliable evaluation of these sophisticated models is paramount and hinges on the quality of
Code Verifiers
—typically test suites—that ascertain the functional correctness of generated code. This is especially critical for RL frameworks employing verifiable rewards (RLVR)
[
8
,
10
,
34
]
, where test case quality directly impacts reward accuracy and training efficacy. However, as highlighted in Section
1
, the comprehensiveness and robustness of verifiers often present a significant bottleneck, underscoring the critical need for effective Test Case Generation.
To this end, the research community has developed numerous benchmarks. Early benchmarks like HumanEval
[
6
]
and MBPP
[
3
]
provided foundational testbeds. Subsequent efforts like EvalPlus
[
27
,
28
]
and MBPP-Plus aimed to improve robustness by expanding existing test sets. More comprehensive benchmarks such as TACO
[
24
]
, CodeContests
[
25
]
(focused on algorithmic problems), BigCodeBench
[
48
]
(complex multi-library tasks), LiveCodeBench
[
19
]
(simulating online judge environments), and HumanEvalPack
[
47
]
(multilingual program synthesis) have broadened the evaluative scope. Concurrently, dedicated TCG benchmarks like TESTEVAL
[
41
]
and TestGenEval
[
18
]
have emerged. Despite these advancements, persistent issues in test case quality, coverage, and potential LLM-centric biases necessitate continuous efforts towards developing high-quality, diverse, and unbiased Code Verifiers.
A.2
Methodologies for Test Case Generation (TCG)
TCG is fundamental to validating code correctness and providing feedback for both evaluation and training of code generation models. While formally defined as a distinct task in this paper, TCG principles are integral to benchmark creation (e.g., LiveCodeBench
[
19
]
, TESTEVAL
[
41
]
) and RL data pipelines (e.g., ACECODER
[
46
]
, CodeRL
[
21
]
). However, suboptimal test quality in existing datasets (e.g., TACO
[
24
]
, CodeForces-CoTs
[
37
]
) can lead to overestimated model performance and reward hacking, particularly in rule-based RL systems like AlphaCode
[
25
]
and DeepSeek Coder
[
13
]
, thus highlighting the urgent need for effective TCG.
Traditional TCG Techniques:
Software testing has a rich history of TCG.
Search-Based Software Testing (SBST)
[
1
,
14
]
uses metaheuristics like genetic algorithms
[
4
,
33
]
to optimize for coverage criteria, though it can be computationally intensive.
Symbolic Execution
[
9
,
5
]
explores program paths systematically but faces path explosion and challenges with complex code.
Fuzzing
[
32
,
11
]
, especially coverage-guided variants like AFL
[
11
]
and libFuzzer
[
39
]
, excels at finding crashes and vulnerabilities by mutating inputs, though it may lack semantic depth for logical tests. Feedback-directed random testing
[
45
,
36
]
also discovers defects but can sometimes lack diversity.
LLM-based TCG Paradigms:
With the rise of LLMs, new TCG methods have emerged, leveraging semantic understanding for potentially greater coverage and diversity. As discussed in Section
2
, these generally follow two paradigms:
1.
Direct Generation:
LLMs produce complete test cases (inputs and outputs). This includes assertion-focused methods (e.g., CodeCoT
[
15
]
, AgentCoder
[
16
]
) and direct input-output synthesis (e.g., TestChain
[
22
]
, CodeRM
[
31
]
, AceCoder
[
46
]
), aiming for logical coverage and boundary conditions.
2.
Input-Interpreter:
LLMs generate test inputs, which are then executed by a ground-truth solution to derive outputs. This is seen in LiveCodeBench
[
19
]
,CodeForce-Cot
[
37
]
and related to LLM-guided fuzzing. EvalPlus
[
27
,
28
]
also aligns by mutating seed inputs for execution. TestChain
[
22
]
also showed improvements by decoupling input and output generation.
Advanced and Specialized TCG Approaches:
In RL contexts, dynamic TCG is crucial. CodeRM-8B
[
31
]
adjusts test quantity by problem difficulty. LEVER
[
34
]
uses learned verifiers, and other works focus on execution-feedback for reward model optimization, all highlighting the impact of test quality on RL outcomes. Differential testing, as in AID
[
29
]
, compares program versions to expose bugs, showing strong results on datasets like TrickyBugs
[
29
]
and EvalPlus
[
27
]
. Recent efforts also explore generating tests targeting prior failures
[
7
]
or using LLMs for test suite refinement.
Despite these diverse approaches, achieving comprehensive logical coverage, generating truly diverse and challenging corner-case tests, and maintaining computational efficiency remain significant hurdles. Furthermore, many LLM-centric TCG methods may perpetuate biases inherent in the LLMs themselves (Section
1
). This paper’s SAGA framework addresses these limitations by proposing a novel human-LLM collaborative paradigm that systematically integrates deep human insights from both correct and incorrect solutions. By focusing on a dynamic, adaptive, and efficient TCG process, SAGA aims to enhance the reliability of LLM code evaluation and training, paving a new path for TCG research.
Appendix B
Formulation and Interpretation of Advanced Evaluation Metrics
This section provides detailed explanations and interpretations for the advanced metrics introduced in Section
2.2
to evaluate the intrinsic quality of test suites.
B.1
Distinct Error Pattern Coverage (DEPC) and Diversity Ratio
Formulation (from main text):
For a test suite
𝒯
𝒯
\mathcal{T}
caligraphic_T
and
N
P
subscript
𝑁
𝑃
N_{P}
italic_N start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
problems, let
v
⁢
(
t
k
)
𝑣
subscript
𝑡
𝑘
v(t_{k})
italic_v ( italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT )
be the
N
P
subscript
𝑁
𝑃
N_{P}
italic_N start_POSTSUBSCRIPT italic_P end_POSTSUBSCRIPT
-dimensional binary error pattern vector for test
t
k
subscript
𝑡
𝑘
t_{k}
italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT
(where
v
⁢
(
t
k
)
j
=
1
𝑣
subscript
subscript
𝑡
𝑘
𝑗
1
v(t_{k})_{j}=1
italic_v ( italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT ) start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT = 1
if
t
k
subscript
𝑡
𝑘
t_{k}
italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT
reveals an error for problem
j
𝑗
j
italic_j
).
DEPC
⁢
(
𝒯
)
=
|
{
v
⁢
(
t
k
)
∣
t
k
∈
𝒯
⁢
and
⁢
‖
v
⁢
(
t
k
)
‖
1
≥
1
}
|
.
DEPC
𝒯
conditional-set
𝑣
subscript
𝑡
𝑘
subscript
𝑡
𝑘
𝒯
and
subscript
norm
𝑣
subscript
𝑡
𝑘
1
1
\mathrm{DEPC}(\mathcal{T})=\Bigl{|}\bigl{\{}v(t_{k})\mid t_{k}\in\mathcal{T}%
\text{ and }\|v(t_{k})\|_{1}\geq 1\bigr{\}}\Bigr{|}.
roman_DEPC ( caligraphic_T ) = | { italic_v ( italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT ) ∣ italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT ∈ caligraphic_T and ∥ italic_v ( italic_t start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT ) ∥ start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ≥ 1 } | .
The
Diversity Ratio
is
DEPC
⁢
(
𝒯
)
/
n
DEPC
𝒯
𝑛
\mathrm{DEPC}(\mathcal{T})/n
roman_DEPC ( caligraphic_T ) / italic_n
, where
n
=
|
𝒯
|
𝑛
𝒯
n=|\mathcal{T}|
italic_n = | caligraphic_T |
.
Interpretation:
DEPC measures the breadth of error coverage by counting the number of unique ways (patterns) in which the test suite can detect failures across a set of problems. A higher DEPC signifies that the test suite is capable of identifying a wider variety of distinct error types or combinations of errors. This directly relates to the concept of inter-test case correlation (
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
) discussed in our theoretical model (Appendix
C
): a test suite with high DEPC is likely composed of tests that are less correlated in terms of the errors they detect, thus having a lower
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
. The Diversity Ratio normalizes DEPC by the number of test cases, indicating the average efficiency of each test in contributing a new, distinct error pattern. A high Diversity Ratio suggests that the test suite is not only diverse but also concise, with less redundancy among its test cases.
B.2
Normalized Area Under the Accuracy-Number of test cases Curve (AUC-AccN)
Formulation (from main text):
For Verifier Accuracy
A
⁢
c
⁢
c
⁢
(
k
)
𝐴
𝑐
𝑐
𝑘
Acc(k)
italic_A italic_c italic_c ( italic_k )
achieved with a test suite of size
k
𝑘
k
italic_k
(up to a maximum
N
𝑁
N
italic_N
, starting from
k
m
⁢
i
⁢
n
subscript
𝑘
𝑚
𝑖
𝑛
k_{min}
italic_k start_POSTSUBSCRIPT italic_m italic_i italic_n end_POSTSUBSCRIPT
), the AUC-AccN is approximated by the trapezoidal rule:
AUC
⁢
@
⁢
N
≈
1
N
−
k
m
⁢
i
⁢
n
⁢
∑
i
=
k
m
⁢
i
⁢
n
N
−
1
A
⁢
c
⁢
c
⁢
(
k
i
)
+
A
⁢
c
⁢
c
⁢
(
k
i
+
1
)
2
⁢
(
k
i
+
1
−
k
i
)
.
AUC
@
N
1
𝑁
subscript
𝑘
𝑚
𝑖
𝑛
superscript
subscript
𝑖
subscript
𝑘
𝑚
𝑖
𝑛
𝑁
1
𝐴
𝑐
𝑐
subscript
𝑘
𝑖
𝐴
𝑐
𝑐
subscript
𝑘
𝑖
1
2
subscript
𝑘
𝑖
1
subscript
𝑘
𝑖
\mathrm{AUC@N}\approx\frac{1}{N-k_{min}}\sum_{i=k_{min}}^{N-1}\frac{Acc(k_{i})%
+Acc(k_{i+1})}{2}(k_{i+1}-k_{i}).
roman_AUC @ roman_N ≈ divide start_ARG 1 end_ARG start_ARG italic_N - italic_k start_POSTSUBSCRIPT italic_m italic_i italic_n end_POSTSUBSCRIPT end_ARG ∑ start_POSTSUBSCRIPT italic_i = italic_k start_POSTSUBSCRIPT italic_m italic_i italic_n end_POSTSUBSCRIPT end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_N - 1 end_POSTSUPERSCRIPT divide start_ARG italic_A italic_c italic_c ( italic_k start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) + italic_A italic_c italic_c ( italic_k start_POSTSUBSCRIPT italic_i + 1 end_POSTSUBSCRIPT ) end_ARG start_ARG 2 end_ARG ( italic_k start_POSTSUBSCRIPT italic_i + 1 end_POSTSUBSCRIPT - italic_k start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) .
Interpretation:
AUC-AccN quantifies the average Verifier Accuracy as the test suite size grows, providing a single scalar value to compare the overall effectiveness and efficiency of different TCG strategies. A higher AUC@
N
𝑁
N
italic_N
(ranging from 0 to 1) indicates that a TCG strategy consistently generates test suites that achieve higher verifier accuracy across various sizes up to
N
𝑁
N
italic_N
.
This metric is a composite reflection of both the average potency of individual test cases (
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) and the effective diversity of the test suite (related to
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
).
•
Impact of
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
(Test Potency):
A higher average
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
means individual tests are more likely to detect errors. This leads to a steeper initial rise in the
A
⁢
c
⁢
c
⁢
(
k
)
𝐴
𝑐
𝑐
𝑘
Acc(k)
italic_A italic_c italic_c ( italic_k )
curve and a higher overall level of accuracy achieved, both of which contribute to a larger AUC@
N
𝑁
N
italic_N
. Thus, AUC-AccN is particularly sensitive to
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
.
•
Impact of Diversity (low
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
):
Greater diversity (lower
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
), empirically reflected by a high DEPC, allows the
A
⁢
c
⁢
c
⁢
(
k
)
𝐴
𝑐
𝑐
𝑘
Acc(k)
italic_A italic_c italic_c ( italic_k )
curve to sustain its rise or plateau at a higher level for a larger number of test cases before saturation effects become dominant. This sustained high accuracy also contributes to a larger AUC@
N
𝑁
N
italic_N
.
Therefore, a high AUC@
N
𝑁
N
italic_N
signifies a TCG strategy that excels at generating tests that are individually powerful (high
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) and collectively non-redundant (low
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
), leading to efficient and robust verifier construction within the specified test suite size limit. It reflects a better overall quality of the generated test cases in achieving high average performance.
Appendix C
Theoretical Analysis of Detection Rate
We analyze the detection rate
ϵ
S
⁢
(
T
)
=
ℙ
⁢
(
X
≥
1
)
subscript
italic-ϵ
𝑆
𝑇
ℙ
𝑋
1
\epsilon_{S}(T)=\mathbb{P}(X\geq 1)
italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T ) = roman_ℙ ( italic_X ≥ 1 )
for a test suite
T
=
{
t
1
,
…
,
t
n
}
𝑇
subscript
𝑡
1
…
subscript
𝑡
𝑛
T=\{t_{1},\dots,t_{n}\}
italic_T = { italic_t start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , … , italic_t start_POSTSUBSCRIPT italic_n end_POSTSUBSCRIPT }
, where
X
=
∑
i
=
1
n
𝟏
E
i
𝑋
superscript
subscript
𝑖
1
𝑛
subscript
1
subscript
𝐸
𝑖
X=\sum_{i=1}^{n}\mathbf{1}_{E_{i}}
italic_X = ∑ start_POSTSUBSCRIPT italic_i = 1 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT italic_n end_POSTSUPERSCRIPT bold_1 start_POSTSUBSCRIPT italic_E start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT end_POSTSUBSCRIPT
and
p
i
=
ℙ
⁢
(
E
i
)
subscript
𝑝
𝑖
ℙ
subscript
𝐸
𝑖
p_{i}=\mathbb{P}(E_{i})
italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = roman_ℙ ( italic_E start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT )
is the probability that test
t
i
subscript
𝑡
𝑖
t_{i}
italic_t start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
detects an error.
C.1
Modeling Correlated Heterogeneous Bernoulli Trials
The expectation of
X
𝑋
X
italic_X
is
𝔼
⁢
[
X
]
=
∑
p
i
=
n
⁢
p
¯
𝔼
delimited-[]
𝑋
subscript
𝑝
𝑖
𝑛
¯
𝑝
\mathbb{E}[X]=\sum p_{i}=n\bar{p}
roman_𝔼 [ italic_X ] = ∑ italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = italic_n over¯ start_ARG italic_p end_ARG
, where
p
¯
=
1
n
⁢
∑
p
i
¯
𝑝
1
𝑛
subscript
𝑝
𝑖
\bar{p}=\frac{1}{n}\sum p_{i}
over¯ start_ARG italic_p end_ARG = divide start_ARG 1 end_ARG start_ARG italic_n end_ARG ∑ italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
.
The variance is
Var
⁢
(
X
)
=
∑
p
i
⁢
(
1
−
p
i
)
+
∑
i
≠
j
Cov
⁢
(
𝟏
E
i
,
𝟏
E
j
)
Var
𝑋
subscript
𝑝
𝑖
1
subscript
𝑝
𝑖
subscript
𝑖
𝑗
Cov
subscript
1
subscript
𝐸
𝑖
subscript
1
subscript
𝐸
𝑗
\mathrm{Var}(X)=\sum p_{i}(1-p_{i})+\sum_{i\neq j}\mathrm{Cov}(\mathbf{1}_{E_{%
i}},\mathbf{1}_{E_{j}})
roman_Var ( italic_X ) = ∑ italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( 1 - italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) + ∑ start_POSTSUBSCRIPT italic_i ≠ italic_j end_POSTSUBSCRIPT roman_Cov ( bold_1 start_POSTSUBSCRIPT italic_E start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT end_POSTSUBSCRIPT , bold_1 start_POSTSUBSCRIPT italic_E start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT end_POSTSUBSCRIPT )
.
To model the effect of correlation in a tractable manner that allows for insights similar to the homogeneous case (uniform
p
𝑝
p
italic_p
, uniform
ρ
𝜌
\rho
italic_ρ
), we consider an
approximating model
. We define an effective average pairwise covariance,
C
¯
eff
subscript
¯
𝐶
eff
\bar{C}_{\mathrm{eff}}
over¯ start_ARG italic_C end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
, and an average individual variance,
σ
p
2
¯
=
1
n
⁢
∑
p
i
⁢
(
1
−
p
i
)
¯
subscript
superscript
𝜎
2
𝑝
1
𝑛
subscript
𝑝
𝑖
1
subscript
𝑝
𝑖
\bar{\sigma^{2}_{p}}=\frac{1}{n}\sum p_{i}(1-p_{i})
over¯ start_ARG italic_σ start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT start_POSTSUBSCRIPT italic_p end_POSTSUBSCRIPT end_ARG = divide start_ARG 1 end_ARG start_ARG italic_n end_ARG ∑ italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( 1 - italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT )
. We then model the variance as if it arose from a system with these averaged second-order characteristics:
Var
approx
⁢
(
X
)
=
n
⁢
σ
p
2
¯
+
n
⁢
(
n
−
1
)
⁢
C
¯
eff
.
subscript
Var
approx
𝑋
𝑛
¯
subscript
superscript
𝜎
2
𝑝
𝑛
𝑛
1
subscript
¯
𝐶
eff
\mathrm{Var}_{\mathrm{approx}}(X)=n\bar{\sigma^{2}_{p}}+n(n-1)\bar{C}_{\mathrm%
{eff}}.
roman_Var start_POSTSUBSCRIPT roman_approx end_POSTSUBSCRIPT ( italic_X ) = italic_n over¯ start_ARG italic_σ start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT start_POSTSUBSCRIPT italic_p end_POSTSUBSCRIPT end_ARG + italic_n ( italic_n - 1 ) over¯ start_ARG italic_C end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT .
If we further posit that these average characteristics can be related through an effective average correlation
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
such that
C
¯
eff
≈
ρ
¯
eff
⁢
avg
⁢
(
p
i
⁢
(
1
−
p
i
)
)
2
subscript
¯
𝐶
eff
subscript
¯
𝜌
eff
avg
superscript
subscript
𝑝
𝑖
1
subscript
𝑝
𝑖
2
\bar{C}_{\mathrm{eff}}\approx\bar{\rho}_{\mathrm{eff}}\sqrt{\text{avg}(p_{i}(1%
-p_{i}))^{2}}
over¯ start_ARG italic_C end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT ≈ over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT square-root start_ARG avg ( italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( 1 - italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) ) start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG
or, more simply for conceptual linkage,
C
¯
eff
≈
ρ
¯
eff
⁢
p
¯
⁢
(
1
−
p
¯
)
subscript
¯
𝐶
eff
subscript
¯
𝜌
eff
¯
𝑝
1
¯
𝑝
\bar{C}_{\mathrm{eff}}\approx\bar{\rho}_{\mathrm{eff}}\bar{p}(1-\bar{p})
over¯ start_ARG italic_C end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT ≈ over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT over¯ start_ARG italic_p end_ARG ( 1 - over¯ start_ARG italic_p end_ARG )
(assuming
p
i
subscript
𝑝
𝑖
p_{i}
italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
are not excessively dispersed, making
σ
p
2
¯
≈
p
¯
⁢
(
1
−
p
¯
)
¯
subscript
superscript
𝜎
2
𝑝
¯
𝑝
1
¯
𝑝
\bar{\sigma^{2}_{p}}\approx\bar{p}(1-\bar{p})
over¯ start_ARG italic_σ start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT start_POSTSUBSCRIPT italic_p end_POSTSUBSCRIPT end_ARG ≈ over¯ start_ARG italic_p end_ARG ( 1 - over¯ start_ARG italic_p end_ARG )
), then:
Var
approx
⁢
(
X
)
≈
n
⁢
p
¯
⁢
(
1
−
p
¯
)
⁢
[
1
+
(
n
−
1
)
⁢
ρ
¯
eff
]
.
subscript
Var
approx
𝑋
𝑛
¯
𝑝
1
¯
𝑝
delimited-[]
1
𝑛
1
subscript
¯
𝜌
eff
\mathrm{Var}_{\mathrm{approx}}(X)\approx n\bar{p}(1-\bar{p})[1+(n-1)\bar{\rho}%
_{\mathrm{eff}}].
roman_Var start_POSTSUBSCRIPT roman_approx end_POSTSUBSCRIPT ( italic_X ) ≈ italic_n over¯ start_ARG italic_p end_ARG ( 1 - over¯ start_ARG italic_p end_ARG ) [ 1 + ( italic_n - 1 ) over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT ] .
(1)
This equation models the variance of
X
𝑋
X
italic_X
as if it were a sum of
n
𝑛
n
italic_n
Bernoulli trials with a common success probability
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
and a common pairwise correlation
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
. The validity of this approximation depends on the actual distribution of
p
i
subscript
𝑝
𝑖
p_{i}
italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
and the structure of covariances. However, it serves as a useful model to understand the qualitative impact of average correlation.
Definition 3
(Model-Based Effective Sample Size
n
eff
∗
superscript
subscript
𝑛
eff
n_{\mathrm{eff}}^{*}
italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT
)
.
Within this approximating model (Eq.
1
), and by analogy to Kish’s design effect
[
20
]
(where
deff
∗
≈
1
+
(
n
−
1
)
⁢
ρ
¯
eff
superscript
deff
1
𝑛
1
subscript
¯
𝜌
eff
\text{deff}^{*}\approx 1+(n-1)\bar{\rho}_{\mathrm{eff}}
deff start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ≈ 1 + ( italic_n - 1 ) over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
), the model-based effective sample size is:
n
eff
∗
≈
n
1
+
(
n
−
1
)
⁢
ρ
¯
eff
.
superscript
subscript
𝑛
eff
𝑛
1
𝑛
1
subscript
¯
𝜌
eff
n_{\mathrm{eff}}^{*}\approx\frac{n}{1+(n-1)\bar{\rho}_{\mathrm{eff}}}.
italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ≈ divide start_ARG italic_n end_ARG start_ARG 1 + ( italic_n - 1 ) over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT end_ARG .
This
n
eff
∗
superscript
subscript
𝑛
eff
n_{\mathrm{eff}}^{*}
italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT
represents the number of hypothetical independent Bernoulli(
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) trials that would exhibit the variance given by Eq.
1
. This is consistent with adjustments for correlated data
[
30
,
12
,
26
]
.
C.2
Upper Bound and Saturation within the Model
Using
n
eff
∗
superscript
subscript
𝑛
eff
n_{\mathrm{eff}}^{*}
italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT
and
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
from our model, we analyze the detection rate
ϵ
S
⁢
(
T
)
=
1
−
ℙ
⁢
(
X
=
0
)
subscript
italic-ϵ
𝑆
𝑇
1
ℙ
𝑋
0
\epsilon_{S}(T)=1-\mathbb{P}(X=0)
italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T ) = 1 - roman_ℙ ( italic_X = 0 )
.
Theorem 1
(Model-Based Approximate Upper Bound on Detection Rate)
.
Within the described approximating model, the detection rate
ϵ
S
⁢
(
T
)
subscript
italic-ϵ
𝑆
𝑇
\epsilon_{S}(T)
italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T )
is approximately upper bounded by:
ϵ
S
⁢
(
T
)
≈
1
−
(
1
−
p
¯
)
n
eff
∗
≈
1
−
(
1
−
p
¯
)
n
1
+
(
n
−
1
)
⁢
ρ
¯
eff
.
subscript
italic-ϵ
𝑆
𝑇
1
superscript
1
¯
𝑝
superscript
subscript
𝑛
eff
1
superscript
1
¯
𝑝
𝑛
1
𝑛
1
subscript
¯
𝜌
eff
\epsilon_{S}(T)\approx 1-(1-\bar{p})^{n_{\mathrm{eff}}^{*}}\approx 1-(1-\bar{p%
})^{\frac{n}{1+(n-1)\bar{\rho}_{\mathrm{eff}}}}.
italic_ϵ start_POSTSUBSCRIPT italic_S end_POSTSUBSCRIPT ( italic_T ) ≈ 1 - ( 1 - over¯ start_ARG italic_p end_ARG ) start_POSTSUPERSCRIPT italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT end_POSTSUPERSCRIPT ≈ 1 - ( 1 - over¯ start_ARG italic_p end_ARG ) start_POSTSUPERSCRIPT divide start_ARG italic_n end_ARG start_ARG 1 + ( italic_n - 1 ) over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT end_ARG end_POSTSUPERSCRIPT .
Proof Sketch.
The probability
ℙ
⁢
(
X
=
0
)
ℙ
𝑋
0
\mathbb{P}(X=0)
roman_ℙ ( italic_X = 0 )
is approximated by that of
n
eff
∗
superscript
subscript
𝑛
eff
n_{\mathrm{eff}}^{*}
italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT
independent Bernoulli(
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) trials, which is
(
1
−
p
¯
)
n
eff
∗
superscript
1
¯
𝑝
superscript
subscript
𝑛
eff
(1-\bar{p})^{n_{\mathrm{eff}}^{*}}
( 1 - over¯ start_ARG italic_p end_ARG ) start_POSTSUPERSCRIPT italic_n start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT end_POSTSUPERSCRIPT
.
∎
This theorem suggests that even when individual
p
i
subscript
𝑝
𝑖
p_{i}
italic_p start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
vary, if there’s an effective positive average correlation
ρ
¯
eff
>
0
subscript
¯
𝜌
eff
0
\bar{\rho}_{\mathrm{eff}}>0
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT > 0
, the system behaves as if it has fewer independent tests, limiting the detection rate.
C.3
Interpretation and Implications for Performance Metrics
The derivation above, employing an approximating model based on average parameters (
p
¯
,
ρ
¯
eff
¯
𝑝
subscript
¯
𝜌
eff
\bar{p},\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_p end_ARG , over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
), robustly indicates that a persistent positive effective correlation among test case detection events leads to a saturation of the overall detection rate. The core insight—that redundancy limits the marginal gain from additional tests—remains.
This theoretical observation is crucial for understanding the performance of TCG strategies and their impact on the empirical metrics used in this paper:
•
Verifier Accuracy (
A
⁢
c
⁢
c
⁢
(
T
)
𝐴
𝑐
𝑐
𝑇
Acc(T)
italic_A italic_c italic_c ( italic_T )
) and its relation to
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
:
The Verifier Accuracy at any given test suite size
n
𝑛
n
italic_n
,
A
⁢
c
⁢
c
⁢
(
T
n
)
𝐴
𝑐
𝑐
subscript
𝑇
𝑛
Acc(T_{n})
italic_A italic_c italic_c ( italic_T start_POSTSUBSCRIPT italic_n end_POSTSUBSCRIPT )
, is fundamentally driven by the test suite’s ability to expose errors, which is heavily influenced by the average potency of its constituent test cases. A higher average error detection probability,
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
, means that individual tests are, on average, more "powerful" or "incisive." Consequently, a TCG strategy yielding a higher
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
will lead to a verifier that more readily and correctly identifies faulty solutions, directly boosting
A
⁢
c
⁢
c
⁢
(
T
n
)
𝐴
𝑐
𝑐
subscript
𝑇
𝑛
Acc(T_{n})
italic_A italic_c italic_c ( italic_T start_POSTSUBSCRIPT italic_n end_POSTSUBSCRIPT )
. While high correlation (
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
) can limit the ultimate achievable accuracy by causing early saturation of distinct error discovery, a strong
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
is essential for the accuracy curve to reach a high level in the first place.
•
AUC-AccN as a reflection of sustained high
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
and managed
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
:
The Area Under the Accuracy-Number of test cases Curve (AUC-AccN), which quantifies the average Verifier Accuracy as test suite size increases, is a composite reflection of both
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
and
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
. A high
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
ensures that the
A
⁢
c
⁢
c
⁢
(
k
)
𝐴
𝑐
𝑐
𝑘
Acc(k)
italic_A italic_c italic_c ( italic_k )
curve rises steeply and achieves a significant altitude. This initial rapid ascent and the overall height of the curve contribute substantially to a larger AUC-AccN. Concurrently, a lower effective correlation
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
(i.e., greater diversity, reflected empirically by DEPC) allows the accuracy to be sustained or to continue growing across a larger number of test cases before significant saturation, thereby expanding the area under the curve. Therefore, strategies achieving a high AUC-AccN are those that likely generate test cases with a consistently high average error detection probability (
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) and effectively manage redundancy (lower
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
). The magnitude of
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
is particularly critical for the "value" captured by AUC-AccN, as it dictates the average level of accuracy being integrated.
•
DEPC and its relation to
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
:
DEPC empirically captures the diversity of error patterns. A TCG strategy that yields high DEPC is effectively generating tests with low effective average correlation
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
, thus mitigating the saturation effect on discovering new types of errors and allowing for a more sustained increase in overall detection capability.
Therefore, the pursuit of TCG methods like SAGA, which aim to enhance both individual test case strength (targeting a higher
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) and inter-test case diversity (targeting a lower
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
), is theoretically well-founded for optimizing these key verifier performance metrics.
Appendix D
TCGBench: Foundational Dataset for TCG Research
As introduced in Section
2.2
,
TCGBench
is the comprehensive dataset curated for our Test Case Generation (TCG) research. It aggregates 1840 recent programming problems sourced from three leading competitive programming platforms: AtCoder (
https://atcoder.jp
), Codeforces (
https://codeforces.com
), and Nowcoder (
https://www.nowcoder.com
). These platforms are recognized for their diverse algorithmic challenges. For each problem in TCGBench, we also collected an average of 36.66 incorrect human submissions, specifically those resulting in "Wrong Answer" (WA) or "Time Limit Exceeded" (TLE) verdicts. This large-scale collection of problems, along with their corresponding WA/TLE submissions, provides a rich empirical foundation for studying human error patterns and rigorously developing and evaluating TCG methodologies. The problems are sourced from recent contests to ensure currency and minimize data leakage risks when evaluating contemporary LLMs. Further details on data collection, filtering criteria, and specific contest sources are available in supplementary materials.
Appendix E
TCGBench-Lite and CodeCompass: Curated Set for Evaluation
For the main experimental comparisons and ablation studies presented in Section
3.2.1
, and for constructing the
CodeCompass
verifiers (Section
4
), we curated
TCGBench-Lite
. This is a focused subset of 270 problems sourced from AtCoder, Codeforces, and Nowcoder contests held since June 2024, ensuring high contemporary relevance and minimizing potential data leakage for evaluating newer models. TCGBench-Lite features an average of 41.41 incorrect submissions per problem.
The difficulty distribution for TCGBench-Lite and CodeCompass (Easy: 27.04%, Medium: 32.59%, Hard: 40.37%) was determined by a multi-faceted approach. This involved considering platform-provided difficulty tags, the type of contest round (e.g., AtCoder Beginner Contest vs. Regular Contest; Codeforces Div.4/3 vs. Div.2/1), typical problem-solving patterns associated with specific problem slots within these contests, and general community perception of difficulty for similar problems. For instance, early problems in beginner-focused contests were generally classified as ’Easy’, while later problems in advanced contests or those requiring complex algorithms/data structures were classified as ’Hard’. This classification aims to provide a balanced yet challenging set for rigorous evaluation. The verifiers in CodeCompass, used for code generation evaluation, consist of an average of 50.54 SAGA-generated test cases per problem for these 270 problems. The characteristics are summarized in Table
4
.
Table 4
:
Overview of TCGBench-Lite (Core Dataset for CodeCompass Verifiers).
Aspect
Details for CodeCompass Evaluation
Core Dataset Source
Atcoder, Codeforces, Nowcoder (June 2024 - Present)
Total Problems
270
Difficulty Distribution
Easy (27.04%), Medium (32.59%), Hard (40.37%)
Scale for CG Evaluation
Avg. Test Cases/Problem: 50.54
Avg.
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
/Problem (for SAGA’s TCG): 41.41
Primary CG Metric
Pass@k
Figure 9
:
SAGA performance on Codeforces (CF) and Nowcoder (NC) problems from the full TCGBench dataset: (a) Detection Rate, (b) Verifier Accuracy (with AUC@50), (c) DEPC, and (d) Diversity Ratio, compared to Baseline (Input-Interpreter) and SAGA’s analytical components (Multidimensional Analysis and Differential Analysis). Dotted lines in (a) & (b) show respective baseline performance at
n
=
100
𝑛
100
n=100
italic_n = 100
.
Appendix F
SAGA Performance on Full TCGBench
To demonstrate SAGA’s broader applicability beyond the AtCoder subset shown in Figure
6
(which used the full TCGBench for that visualization), Figure
9
presents SAGA’s performance on the Codeforces and Nowcoder portions of the complete TCGBench dataset. SAGA consistently replicates its superior performance, exhibiting enhanced efficacy (DR, Acc) and superior test suite quality (DEPC, Diversity Ratio) compared to the baseline and its individual analytical components across these platforms as well. This consistent pattern of improvement underscores the fundamental benefits of SAGA’s structured, insight-driven approach to TCG.
To further demonstrate SAGA’s broad applicability and robustness, Figure
10
presents its Detection Rate (DR) and Verifier Accuracy (VAcc) when paired with different LLM backbones (Qwen2.5-Coder-7B-Instruct, Qwen2.5-72B-Instruct, and DeepSeek-V3-0324) on the Codeforces and Nowcoder portions of the full TCGBench dataset, compared against the Input-Interpreter baseline (using DeepSeek-V3). Across both platforms and all LLM backbones, SAGA consistently and significantly outperforms the baseline in DR and VAcc at various test case sizes. Notably, even SAGA with the smaller Qwen2.5-Coder-7B often surpasses the baseline that utilizes the larger DeepSeek-V3, highlighting SAGA’s ability to effectively guide diverse LLMs. While larger SAGA backbones generally yield higher absolute performance, the consistent uplift provided by the SAGA framework across different models and problem sources underscores its fundamental benefits and general applicability for advanced TCG.
Figure 10
:
SAGA performance with different LLM backbones (Qwen-Coder, Qwen-72B, DeepSeek-V3) compared to the Baseline (Input-Interpreter with DeepSeek-V3) on Codeforces and Nowcoder portions of the full TCGBench dataset. Metrics: Detection Rate (DR) and Verifier Accuracy (VAcc) at varying test case sizes. Dashed lines indicate baseline performance.
Appendix G
Detailed Performance Analysis on TCGBench-Lite by Difficulty
To provide a more granular understanding of how different Test Case Generation (TCG) methods perform across varying levels of problem complexity, Figure
11
illustrates the Verifier Accuracy (VAcc@50) and Detection Rate (DR@50) of SAGA, its analytical components (Multidimensional Analysis only, denoted "w/ MultiDim"; Differential Analysis only, denoted "w/ Differ"), and baseline TCG methods (TestChain, EvalPlus, and Random Input-Interpreter) on the Easy, Medium, and Hard problem subsets within TCGBench-Lite.
Figure 11
:
Performance comparison (VAcc@50 and DR@50) of SAGA, its components, and baseline TCG methods across Easy, Medium, and Hard problem subsets of TCGBench-Lite. SAGA consistently outperforms baselines across all difficulties, and its full framework generally surpasses its individual analytical components, especially on harder problems.
Key Observations from Figure
11
:
•
Consistent Superiority of SAGA:
Across all difficulty tiers (Easy, Medium, Hard) and for both VAcc@50 and DR@50, the full SAGA framework consistently outperforms all baseline methods (TestChain, EvalPlus, Random). This underscores SAGA’s robustness and its ability to generate more effective test suites regardless of problem complexity. For instance, on Hard problems, SAGA achieves a VAcc@50 of 25.06%, substantially higher than the Random baseline (18.47%) and other methods. A similar trend is observed for DR@50, where SAGA reaches 87.0% on Hard problems.
•
Impact of Problem Difficulty on Baselines:
The performance of baseline methods, particularly TestChain and EvalPlus, degrades more noticeably as problem difficulty increases. For example, EvalPlus’s VAcc@50 drops from 38.10% on Easy problems to a mere 5.56% on Hard problems. This suggests that these methods may struggle to generate effective test cases for more complex scenarios or subtle bugs prevalent in harder problems. The Random Input-Interpreter shows more resilience than TestChain and EvalPlus on harder problems but still falls short of SAGA.
•
Synergy of SAGA’s Analytical Components:
While both Multidimensional Analysis ("w/ MultiDim") and Differential Analysis ("w/ Differ") components of SAGA individually outperform the baselines, the full SAGA framework generally achieves the best performance or is highly competitive.
–
On
Easy
problems, SAGA’s VAcc@50 (55.59%) is notably higher than "w/ MultiDim" (50.00%) and "w/ Differ" (49.15%), indicating that the combination of insights from both correct and incorrect solutions is beneficial even for simpler problems.
–
For
Medium
problems, SAGA (VAcc@50: 33.24%) again leads, showing a clear advantage over relying on only one type of human prior.
–
On
Hard
problems, the synergy is particularly evident. SAGA’s VAcc@50 (25.06%) is superior to "w/ MultiDim" (21.92%) and "w/ Differ" (21.25%). This suggests that for complex problems with elusive bugs, leveraging diverse insights from both correct solution structures and patterns of common errors is crucial for generating highly discriminative test suites.
A similar synergistic effect is generally observed for DR@50, where the full SAGA framework often provides the highest or near-highest detection rates.
•
Effectiveness of Differential Analysis on Harder Problems:
Interestingly, the "w/ Differ" component (Differential Analysis leveraging
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
) shows relatively strong performance on Hard problems compared to its performance on Easy problems, particularly for VAcc@50. This might imply that analyzing patterns from incorrect submissions is especially valuable for uncovering the types of subtle or complex errors that characterize more difficult problems.
•
Limitations of Simpler Priors:
The performance of "Random" (Input-Interpreter) and even "EvalPlus" (which uses human solutions for mutation) on Medium and Hard problems highlights that merely having access to human solutions or employing random generation is insufficient. SAGA’s structured approach to
analyzing and strategically leveraging
these human priors is what drives its superior performance, especially as complexity increases.
Appendix H
Supplementary Experimental Analyses
To further explore mechanisms for robust test suite construction and the value of diverse generation strategies, we present two additional studies: an analysis of mixing random test cases from different LLMs, and an ablation study on SAGA’s knowledge sources.
H.1
Efficacy of Mixing Random Test Cases from Different Language Models
Our theoretical framework highlights that test suite quality is influenced by individual test potency (
p
¯
¯
𝑝
\bar{p}
over¯ start_ARG italic_p end_ARG
) and inter-test case correlation (
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
). We investigated managing
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
by mixing random test cases (akin to the Input-Interpreter paradigm from Section
2.2
) sourced from different LLMs (V3: DeepSeek-V3-0324, 72B: Qwen2.5-72B-Instruct, Coder: Qwen2.5-Coder-7B-Instruct). The hypothesis is that tests from
different
models may exhibit lower inter-source correlation, leading to improved combined suite characteristics. Figure
12
shows the AUC@50 when mixing random tests, with diagonal elements representing single-LLM suites.
Figure 12
:
Heatmap illustrating AUC@50 performance of mixed random test suites. Diagonal elements: suites from a single model (V3, 72B, Coder). Off-diagonal (i,j): mixing random tests from model i and model j.
Observations
•
Benefit of Model-Source Diversity
: Mixing random tests from two different LLMs frequently yields superior AUC@50 compared to using tests from only one, across AtCoder, Codeforces, and Nowcoder datasets. For instance, on Codeforces, mixing V3 (AUC@50: 0.2014) with 72B (0.1691) results in a mixed AUC@50 of 0.2629, surpassing both. This suggests complementary biases even in random generation.
•
Reduced Effective Correlation
: The improvements imply that combining tests from different models likely lowers
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
compared to single-source suites. Enhanced diversity allows the combined suite to cover a broader error spectrum, increasing AUC@50.
•
Surpassing Stronger Components
: Often, the mixed suite outperforms even the stronger individual model in the pair (e.g., V3+72B on Codeforces). This robustly shows different LLMs contribute unique, valuable random tests, highlighting complementary strengths.
Take-away
: Diversifying the source of even "naive" random tests reduces correlation and improves test suite quality, supporting our theoretical framework. While SAGA achieves this more directly via structured analysis, this experiment underscores the general impact of minimizing
ρ
¯
eff
subscript
¯
𝜌
eff
\bar{\rho}_{\mathrm{eff}}
over¯ start_ARG italic_ρ end_ARG start_POSTSUBSCRIPT roman_eff end_POSTSUBSCRIPT
.
H.2
Ablation Study: Impact of Human Knowledge Source Volume in SAGA
To dissect SAGA’s knowledge source contributions, we conducted an ablation study on the Codeforces portion of TCGBench. We modified SAGA by removing its Differential Analysis component (insights from incorrect solutions,
𝒮
wrong
subscript
𝒮
wrong
\mathcal{S}_{\text{wrong}}
caligraphic_S start_POSTSUBSCRIPT wrong end_POSTSUBSCRIPT
) entirely. Instead, we doubled the volume of correct human solutions (
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
) fed into SAGA’s Multidimensional Analysis component, creating a "Multidim-Enhanced" version. The aim was to see if increasing one type of human insight could compensate for omitting another. Table
5
compares the original SAGA with this "Multidim-Enhanced" configuration.
Table 5
:
Ablation Study on Codeforces (TCGBench): SAGA vs. Multidim-Enhanced (Double
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
for Multidimensional Analysis, No Differential Analysis).
Configuration
DR@50
VAcc@50
AUC@50
DivRatio@50
SAGA (Multidim. + Differ.)
90.89%
47.08%
0.3195
0.697
Multidim-Enhanced
88.09%
38.73%
0.2744
0.701
Analysis of Ablation Results (Table
5
):
•
Degradation in Core Effectiveness
: Despite doubling
𝒮
human
subscript
𝒮
human
\mathcal{S}_{\text{human}}
caligraphic_S start_POSTSUBSCRIPT human end_POSTSUBSCRIPT
input, the "Multidim-Enhanced" version shows a clear drop in VAcc@50 (from 47.08% to 38.73%) and AUC@50 (from 0.3195 to 0.2744) compared to the full SAGA. This suggests insights from incorrect solutions via Differential Analysis are crucial for verifier quality and cannot be fully compensated by merely increasing the volume of correct solutions for Multidimensional Analysis.
•
Diversity vs. Effectiveness
: While the Diversity Ratio is comparable or slightly higher for "Multidim-Enhanced", this raw diversity doesn’t translate to better overall verifier quality (AUC@50). This reinforces that the
type
of diversity and the nature of uncovered error patterns (targeted by Differential Analysis) are critical, not just diversity as a raw count.
•
Implications for SAGA’s Design
: This strongly supports SAGA’s dual-pronged approach of integrating insights from
both
correct and incorrect human solutions. The unique error patterns revealed by Differential Analysis appear vital for building high-quality, discriminative verifiers, and their contribution is not simply replicable by scaling up the input to Multidimensional Analysis alone.
Appendix I
Model Performance on CodeCompass
To further illustrate the utility of CodeCompass as a challenging benchmark for evaluating LLM code generation capabilities, Table
6
summarizes the Pass@1 performance of several contemporary LLMs. The evaluation was conducted separately for C++ and Python problem instances within CodeCompass, utilizing its SAGA-enhanced verifier suite.
The results demonstrate a clear differentiation among models in both languages, underscoring CodeCompass’s ability to effectively rank and assess current code generation models. The challenging nature of the SAGA-generated test cases in CodeCompass provides a rigorous testbed for future model development and comparison.
Table 6
:
Performance of Various LLMs on CodeCompass (Pass@1) for C++ and Python.
Model
Pass@1 on CodeCompass (C++)
Pass@1 on CodeCompass (Python)
Qwen2.5-Coder-32B-Instruct
15.93%
12.59%
Qwen2.5-72B-Instruct
17.04%
14.81%
GPT-4o (2024-11-20)
20.74%
14.44%
DeepSeek-V3
24.81%
23.33%
QWQ-32B
31.85%
26.30%
DeepSeek-Chat-R1
38.15%
34.07%
Qwen3-235B-A22B
43.70%
36.30%
From Table
6
, it is evident that CodeCompass effectively differentiates LLM performance across both C++ and Python. While relative model rankings show some consistency, language-specific performance variations are also notable, highlighting the benchmark’s capacity to reveal nuanced capabilities. The generally moderate Pass@1 rates underscore the challenging nature of CodeCompass due to its SAGA-enhanced test suites, making it a valuable resource for rigorous multi-lingual code generation assessment.
Appendix J
TCGCoder-7B Training Details
TCGCoder-7B, our specialist 7-billion-parameter model for Test Case Generation (TCG), was fine-tuned from
Qwen2.5-Coder-7B-Instruct
[
44
,
17
]
. The training dataset, distinct from our evaluation sets to prevent data leakage, comprised 15,000 early-stage programming problems from Codeforces and NowCoder, processed by our SAGA framework (Section
3
) to generate structured outputs (Python
Case Scripts
,
Math Explanations
,
Self-Validation
code, per Figure
5
). The fine-tuning aimed to distill SAGA’s TCG reasoning into TCGCoder-7B. Key training configurations included 3 epochs, a global batch size of 16, an initial learning rate of 5e-6 (minimum 3e-7), a max sequence length of 61,335 tokens, and the qwen2 chat template. Training utilized Fully Sharded Data Parallel (FSDP) across 2 nodes, each with 8 GPUs.