---
title: Towards Functional Correctness of Code Models with Selective Generation
id: towards-functional-correctness-of-code-models-with-selective-generation
tags:
- code-llm-confidence-positioning-d82d00
- selective-generation
created: '2026-11-09T23:08:19.072522Z'
updated: '2026-11-09T23:27:44.428949Z'
source: https://arxiv.org/html/2505.13553
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:19.071933Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: FULL TEXT. CLOSE for L3. Selective code generation with FDR-CE control (alpha=0.35,
  delta_S=0.1) using fuzz-generated unit tests (APPS-f, Mercury-f, HumanEval-f, MBPP-f);
  GPT-4o, Gemini-1.5 Pro, DeepSeek R1, CodeLlama 13B. Abstention with guarantees,
  not execution-budget routing; i.i.d. assumption; no verbal confidence updating after
  test failures.
---

Towards Functional Correctness of Code Models with Selective Generation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2505.13553v4 [cs.SE] 29 Oct 2026
Towards Functional Correctness of Code Models with Selective Generation
Jaewoo Jeong
Affiliation:
CSE, POSTECH
Taesoo Kim
Affiliation:
SCS&SCP GaTech
Affiliation:
Microsoft
Sangdon Park
Affiliation:
CSE, POSTECH
Affiliation:
GSAI, POSTECH
Correspondence to:
sangdon@postech.ac.kr
Abstract
The hallucination of code generation models hinders their applicability to systems requiring higher safety standards.
One critical bottleneck in addressing code hallucination is the difficulty of identifying the functional correctness of generated code, due to its unnatural form.
We address this core bottleneck by automatically generating unit tests using dynamic code analysis tools, leveraging the
executable nature
of code.
Accordingly, we propose a
selective code generator
that abstains from uncertain generations – based on the functional correctness evaluated by generated unit tests – to theoretically control the correctness among non-abstained answers,
i.e.,
the false discovery rate.
Finally, we propose to use generated unit tests in evaluation as well as in learning for precise code evaluation, calling this paradigm
FuzzEval
.
We demonstrate the efficacy of our method along with the controllability of code hallucination and reasonable selection efficiency.
Keywords:
Machine Learning, ICML
1
Introduction
Large language models (LLMs) have recently been proven to be performant in various tasks, including question-answering, summarization, mathematical reasoning, and algorithmic problem-solving
(
Brown et al., 2020
;
Li et al., 2022
;
Touvron et al., 2023
;
Ahn et al., 2024
)
.
Along with language generation, code generation is closely related but has its own benefit as a core task for addressing many applications, including mathematical solving via program of thought, security patch generation, and general program development
(
Chen et al., 2023b
;
Hossain et al., 2024
;
Kim et al., 2025
)
.
Recent developments on large code models have primarily focused on enhancing model performance
(
Guo et al., 2025
;
OpenAI et al., 2025
)
– thereby
indirectly controlling
the functional hallucination.
However,
direct control
methods to address
functional hallucination in code generation
,
i.e.,
a situation where generated code does not satisfy a desired functionality, remain unexplored.
In contrast to hallucination control in code, heuristic and certified methods for hallucination control in natural language generation have been extensively studied beyond enhancing the model performance.
For example, the language hallucination is heuristically measured by generating multiple answers and checking the consensus among them
(
Manakul et al., 2023
;
Kuhn et al., 2023
)
.
As more sophisticated methods, hallucination is carefully controlled by certified methods, including conformal prediction
(
Vovk et al., 2005
)
and selective prediction
(
Geifman and El-Yaniv, 2017
)
, providing certified ways to mitigate language hallucination
(
Quach et al., 2024
;
Mohri and Hashimoto, 2024
;
Lee et al., 2024
)
.
Figure 1:
Overview of our proposed selective code generation. We leverage an abstaining option to selectively generate code to
control
the rate of hallucination in an FDR. Our selective generator learns a selection function by leveraging dynamic code analysis tools to automatically generate unit tests and use them as a calibration set for the selection function and also as a test set for evaluation.
We claim that a critical bottleneck in mitigating code hallucination mainly stems from
the intricacy of identifying functional equivalence between two code snippets due to the unnatural form of code.
In natural language, textual entailment
(
Bowman et al., 2015
)
is the main building block in measuring the semantic correctness of an answer,
i.e.,
an answer is correct if a question-associated context entails the answer. Given this definition on the correctness between two sentences, humans can manually annotate entailment labels to learn entailment-predicting models
(
Williams et al., 2018
)
.
However, this is challenging in code as it is not easy for humans to decide whether one code entails another due to its complex, un-natural structure for obtaining entailment labels. This can be partially mitigated by constructing a few unit tests
(
Chen et al., 2021
;
Austin et al., 2021
;
Cassano et al., 2022
)
and executing it to check discrepancies in output, while limited to a small number of unit tests.
To address these challenges, we build on prior programming language literature to re-define entailment for code generation.
We further exploit the
executable property of code
by automatically generating unit tests through code analysis tools.
In particular, we leverage fuzzing methods
(
Miller et al., 1990
)
, one of the practical code analysis tools, to automatically generate unit tests.
Given the code entailment definition and generated unit tests, we propose certified selective code generation for code hallucination control. This includes a learning algorithm of a selective generator for code, a post-processor of an original generator, which provides a controllability guarantee on the rate of hallucination in a false discovery rate (FDR),
i.e.,
a learned selective generator provides a desired or minimum level of hallucination.
The learning algorithm mainly leverages fuzzing for checking the correctness of code in a self-supervised manner for supervised learning in selective code generators.
Finally, we leverage fuzzing for code evaluation as well as selective generator learning. We claim that automatically generated unit tests provide rigorous evaluation, calling this evaluation paradigm
FuzzEval
to distinguish from
HumanEval
(
Chen et al., 2021
)
.
The main contribution of our work lies in the selective generation learning algorithm that controls the hallucination rate. We demonstrate the efficacy of our algorithm over open and closed code generators under diverse experiment setups, including four code generators, four datasets, four programming languages, and diverse baselines. Our results demonstrate the hallucination-controllability with reasonable efficiency, and further demonstrate the benefits of automatically generated unit tests. We will release code and dataset at
https://github.com/trustml-lab/selective-code-generation
.
1.1
Related Work
Execution Based Code Correctness Evaluation.
Popular code generation benchmarks, such as HumanEval
(
Chen et al., 2021
)
, APPS
(
Hendrycks et al., 2021
)
, or MBPP
(
Austin et al., 2021
)
evaluate the functional correctness of a generated code snippet by executing unit tests.
However, generating unit tests for such evaluation purposes is a costly task.
Automated unit test generation has been explored in recent work. LLMs themselves have been used to improve unit tests
(
Alshahwan et al., 2024
)
.
EvalPlus
(
Liu et al., 2023
)
and SemCoder
(
Ding et al., 2024
)
adopt a type-aware input mutation strategy based on LLM-generated seeds, while Mercury
(
Du et al., 2024
)
leverages LLMs to generate random test case generators for evaluation split.
Our work complements these works by generating unit tests via dynamic analysis tools,
e.g.,
fuzzing tools
, that have been extensively studied and validated within the computer security community, to explore execution paths.
Previous works that leverage unit tests for evaluation commonly use the pass@k metric to assess functional correctness
(
Liu et al., 2023
;
Ding et al., 2024
)
.
EvalPlus
(
Liu et al., 2023
)
reports a drop in pass@k metric with larger test suites indicating that the metric is sensitive to the number and quality of unit tests.
Furthermore, pass@k cannot consider partially correct programs.
Our work addresses this by introducing the FDR-CE metric with a statistical guarantee.
Code Generation and Hallucination.
Code generation is the task of generating a program that satisfies given functional specifications. The main challenge for this task is the generation of functionally incorrect code, often referred to as
code hallucination
in the previous literature
(
Tian et al., 2025
;
Zhang et al., 2025
)
.
Recent work has mostly focused on improving the functionality itself. DeepSeek-R1
(
Guo et al., 2025
)
, OpenAI-IOI
(
OpenAI et al., 2025
)
leverage reinforcement learning based finetuning, resulting in highly performant code generation models. CodeT
(
Chen et al., 2023a
)
, TiCoder
(
Fakhoury et al., 2024
)
, 3DGen
(
Fakhoury et al., 2025
)
, MPSC
(
Huang et al., 2024
)
, S*
(
Li et al., 2025
)
, and CodeRL
(
Le et al., 2022
)
rank generated solutions during the inference or evaluation phase to determine which outputs to adopt. AlphaCode
(
Li et al., 2022
)
leverages both finetuning and a ranking mechanism to improve performance. The key distinction of our work lies in directly controlling the rate of falsely generated code (FDR-CE), making the underlying code generator more trustworthy. Furthermore, our work is applicable on top of each method providing an upper bound on the FDR-CE (
e.g.,
DeepSeek result in Figure
2(c)
shows that our method can provide an additional statistical guarantee when applied on top of GRPO based fine-tuning
(
Guo et al., 2025
)
).
The methods mentioned above leveraged unit tests to improve performance. The ranking-based methods
(
Chen et al., 2023a
;
Fakhoury et al., 2024
;
Fakhoury et al., 2025
;
Huang et al., 2024
;
Li et al., 2025
;
Le et al., 2022
)
leverage unit tests to rank sampled solutions and select the best code, whereas fine-tuning based methods
(
Guo et al., 2025
;
OpenAI et al., 2025
)
leverage unit tests to provide execution feedback for reinforcement learning. Unlike prior work, our method leverages unit tests to determine
α
\alpha
-code entailment and apply a selective generation learning algorithm.
Selective Generation.
Selective prediction abstains from answering if a model is not confident of the answer, from which it controls the risk at a desirable level. This method can be applicable to various tasks. Selective classification for deep learning
(
Geifman and El-Yaniv, 2017
)
considers classification tasks. Selective text generation
(
Lee et al., 2024
)
is applied to a language generation task by introducing textual entailment to control hallucination. We extend selective generation for code by leveraging an executable property of code, while still controlling hallucination.
2
Preliminary
We introduce preliminaries on textual entailment for measuring correctness between two answers, selective generation to control the rate of hallucination, and dynamic code analysis via fuzzing for learning and evaluating functional correctness of code snippets.
Selective Generation.
Language models suffer from generating hallucinated facts. Recently, certified ways to control the rate of hallucination in language models have been proposed
(
Quach et al., 2024
;
Mohri and Hashimoto, 2024
;
Lee et al., 2024
)
. Among them, selective generation, which extends traditional selective classification
(
Geifman and El-Yaniv, 2017
)
, provides a way to control the rate of hallucination defined in terms of a false discovery rate with entailment (FDR-E) that leverages textual entailment to measure the correctness of two answers.
In particular,
a selective generator
S
^
​
(
𝐱
)
\hat{{S}}(\mathbf{x})
given a question
𝐱
\mathbf{x}
returns a generated answer
G
⁡
(
𝐱
)
G(\mathbf{x})
from a language model or abstains from answering by returning “I don’t know” (
IDK
). The FDR-E of this selective generator with respect to a true answer
𝐲
\mathbf{y}
is defined as
ℛ
⁡
(
S
^
)
≔
ℙ
⁡
{
S
^
​
(
𝐱
)
∉
E
⁡
(
𝐲
)
|
S
^
​
(
𝐱
)
≠
IDK
}
.
\mathcal{{R}}(\hat{{S}})\coloneqq\mathbbm{P}\{\hat{{S}}(\mathbf{x})\notin E(\mathbf{y})\;|\;\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\}.
Here,
E
E
is an entailment set that contains entailed answers,
i.e.,
E
⁡
(
𝐲
)
≔
{
𝐲
¯
∣
𝐲
¯
entails
𝐲
}
E(\mathbf{y})\coloneqq\{\bar{\mathbf{y}}\mid\text{$\bar{\mathbf{y}}$ entails $\mathbf{y}$}\}
(where a reverse relation is also valid),
so
S
^
​
(
𝐱
)
∈
E
​
(
𝐲
)
\hat{{S}}(\mathbf{x})\in E(\mathbf{y})
means that
S
^
​
(
𝐱
)
\hat{{S}}(\mathbf{x})
entails
𝐲
\mathbf{y}
.
In semi-supervised selective generation
(
Lee et al., 2024
)
, a learning algorithm leverages an estimated entailment set
E
^
\hat{{E}}
learned from the handful of entailment labels, where
E
^
\hat{{E}}
is used as a pseudo-labeling function for entailment labels.
Based on the estimated entailment set, the following surrogate of the FDR-E is considered:
ℛ
^
​
(
S
^
)
≔
ℙ
⁡
{
S
^
​
(
𝐱
)
∉
E
^
​
(
𝐲
)
|
S
^
​
(
𝐱
)
≠
IDK
}
.
\hat{\mathcal{{R}}}(\hat{{S}})\coloneqq\mathbbm{P}\{\hat{{S}}(\mathbf{x})\notin\hat{{E}}(\mathbf{y})\;|\;\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\}.
The algorithm leverages the relation between
ℛ
⁡
(
S
^
)
\mathcal{{R}}(\hat{{S}})
and
ℛ
^
​
(
S
^
)
\hat{\mathcal{{R}}}(\hat{{S}})
to bound
ℛ
⁡
(
S
^
)
\mathcal{{R}}(\hat{{S}})
, as shown in the following lemma.
Lemma 2.1
.
(
Lee et al., 2024
)
ℛ
⁡
(
S
^
)
\mathcal{{R}}(\hat{{S}})
is decomposed in
ℛ
⁡
(
S
^
)
≔
ℙ
𝒟
S
^
​
{
e
=
0
,
e
^
=
1
}
−
ℙ
𝒟
S
^
​
{
e
=
1
,
e
^
=
0
}
+
ℛ
^
​
(
S
^
)
,
\mathcal{{R}}(\hat{{S}})\coloneqq\mathbbm{P}_{\mathcal{{D}}_{\hat{{S}}}}\{e=0,\hat{{e}}=1\}-\mathbbm{P}_{\mathcal{{D}}_{\hat{{S}}}}\{e=1,\hat{{e}}=0\}+\hat{\mathcal{{R}}}(\hat{{S}}),
where
ℙ
S
^
{
⋅
}
≔
ℙ
{
⋅
∣
S
^
(
𝐱
)
≠
IDK
}
\mathbbm{P}_{\hat{{S}}}\{\cdot\}\coloneqq\mathbbm{P}\{\cdot\mid\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\}
,
e
≔
𝟙
​
(
S
^
​
(
𝐱
)
∈
E
​
(
𝐲
)
)
e\coloneqq\mathbbm{1}(\hat{{S}}(\mathbf{x})\in E(\mathbf{y}))
, and
e
^
≔
𝟙
​
(
S
^
​
(
𝐱
)
∈
E
^
​
(
𝐲
)
)
\hat{{e}}\coloneqq\mathbbm{1}(\hat{{S}}(\mathbf{x})\in\hat{{E}}(\mathbf{y}))
.
Importantly,
the above lemma assumes that the true label
𝐲
\mathbf{y}
is given. But, in code generation it is equivalent to considering a unit test generator
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
where generated unit tests play a role of the true label
𝐲
\mathbf{y}
.
By controlling the upper bound of three decomposed terms in
ℛ
⁡
(
S
^
)
\mathcal{{R}}(\hat{{S}})
at a desired level, the algorithm learns a selective generator
S
^
\hat{{S}}
.
We leverage this framework to learn
E
^
\hat{{E}}
via generated unit tests via dynamic code analysis tools.
See Appendix
A
for additional detail.
3
Problem
We consider a learning problem in code generation. In particular, we learn a code generator to control code hallucination from the perspective of
functional correctness
where the generator abstains from answering if it is not certain on the correctness of the generated code.
Let
𝒲
\mathcal{W}
be a set of tokens,
𝒲
∗
≔
∪
i
=
0
∞
𝒲
i
\mathcal{{W}}^{*}\coloneqq\cup_{i=0}^{\infty}\mathcal{{W}}^{i}
,
𝒳
≔
𝒲
∗
\mathcal{{X}}\coloneqq\mathcal{{W}}^{*}
be a set of input prompts (
e.g.,
problem descriptions) for a code generator,
𝒴
≔
𝒲
∗
\mathcal{{Y}}\coloneqq\mathcal{{W}}^{*}
be a set of code snippets,
𝒟
\mathcal{{D}}
be a distribution that depends on prompt and code pairs
𝒳
×
𝒴
\mathcal{{X}}\times\mathcal{{Y}}
along with other random sources,
and
G
:
𝒳
→
𝒴
G:\mathcal{{X}}\to\mathcal{{Y}}
be a code generator.
To control the hallucination rate of a code generator
G
G
, we consider the following selective generator
S
^
:
𝒳
→
𝒴
∪
{
IDK
}
\hat{{S}}:\mathcal{{X}}\to\mathcal{{Y}}\cup\{\texttt{IDK}\}
(
Geifman and El-Yaniv, 2017
;
Lee et al., 2024
)
:
S
^
​
(
𝐱
)
≔
{
G
⁡
(
𝐱
)
if
​
s
^
​
(
𝐱
)
=
1
IDK
otherwise
,
\hat{{S}}(\mathbf{x})\coloneqq\begin{cases}G(\mathbf{x})&\text{if~}\hat{{s}}(\mathbf{x})=1\\
\texttt{IDK}&\text{otherwise}\end{cases},
where
IDK
is a short-hand for “I don’t know”
and
s
^
:
𝒳
→
{
0
,
1
}
\hat{{s}}:\mathcal{{X}}\to\{0,1\}
is a selection function.
Here, we consider a setup that the target code generator
G
G
is given and we learn a selection function
s
^
\hat{{s}}
.
We mainly learn the selective generator under the independent and identically distributed (i.i.d.) assumption by controlling a false discovery rate (FDR) for code.
In particular, we consider the risk definition of a selective generator
S
^
\hat{{S}}
via an FDR with a relation
R
R
,
i.e.,
ℛ
R
​
(
S
^
)
≔
ℙ
⁡
{
(
S
^
​
(
𝐱
)
,
ℱ
⁡
(
𝐱
)
)
∉
R
|
S
^
​
(
𝐱
)
≠
IDK
}
,
\mathcal{{R}}_{R}(\hat{{S}})\coloneqq\mathbbm{P}\left\{(\hat{{S}}(\mathbf{x}),\mathcal{{F}}(\mathbf{x}))\notin R\;\middle|\;\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\right\},
(1)
where
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
is a unit test generator from a problem description
𝐱
\mathbf{x}
and
the probability is taken over
𝐱
∼
𝒟
\mathbf{x}\sim\mathcal{{D}}
and the randomness of
S
^
\hat{{S}}
and
ℱ
\mathcal{{F}}
.
We measure the ratio of failure,
i.e.,
the ratio that generated code
G
⁡
(
𝐱
)
G(\mathbf{x})
does not have a relation
R
R
with respect to a unit test generator
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
, among not-abstaining cases.
Given the learning objective in the FDR,
we find a learning algorithm
𝒜
\mathcal{{A}}
for
S
^
\hat{{S}}
such that given a calibration set
𝐙
\mathbf{Z}
with
|
𝐙
|
=
n
|\mathbf{Z}|=n
, the learned selective generator
S
^
≔
𝒜
⁡
(
𝐙
)
\hat{{S}}\coloneqq\mathcal{{A}}(\mathbf{Z})
controls a desired risk level
ε
\varepsilon
with probability at least
1
−
δ
1-\delta
,
i.e.,
ℙ
{
ℛ
R
(
𝒜
(
𝐙
)
)
≤
ε
}
≥
1
−
δ
,
\mathbbm{P}\left\{\mathcal{{R}}_{R}(\mathcal{{A}}(\mathbf{Z}))\leq\varepsilon\right\}\geq 1-\delta,
where the probability is taken over
𝐙
∼
𝒟
n
\mathbf{Z}\sim\mathcal{{D}}^{n}
.
Here, the main challenges include (1) designing a correctness relation
R
R
for code generation and (2) finding a learning algorithm with the above PAC-style controllability guarantee, while maximizing
selection efficiency
,
i.e.,
ℙ
{
S
^
(
𝐱
)
≠
IDK
}
\mathbbm{P}\{\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\}
, which are addressed in the following section.
4
Method: Selective Code Generation
We introduce a definition of code entailment in Section
4.1
, followed by a risk definition in Section
4.2
. Section
4.3
and
4.4
present the theoretical bound. Our FDR-controlling algorithm is described in Section
4.5
, followed by its controllability guarantee in Section
4.6
. Lastly, we highlight the importance of evaluation via fuzzing in Section
4.7
.
4.1
Code Entailment
Measuring the functional correctness of a generated code snippet is a challenging task.
In particular, the functionality of generated code is evaluated using only a limited set of manually chosen unit tests
(
Chen et al., 2021
)
.
We re-define the concept of
code entailment
that leverages automated unit test generators (
e.g.,
LLMs or dynamic code analysis tools) along with manual unit tests to define the functional correctness with larger unit tests.
To this end, let
𝒰
\mathcal{{U}}
and
𝒱
\mathcal{{V}}
be sets of input and output states for all code snippets, respectively. A unit test generator
ℱ
:
𝒳
→
Δ
⁡
(
𝒰
×
𝒱
)
\mathcal{{F}}:\mathcal{{X}}\to\Delta(\mathcal{{U}}\times\mathcal{{V}})
returns a pair of input and output states from a problem description
𝐱
\mathbf{x}
,
i.e.,
(
𝐮
,
𝐯
)
∼
ℱ
⁡
(
𝐱
)
.
(\mathbf{u},\mathbf{v})\sim\mathcal{F}(\mathbf{x}).
We then introduce the definition of
α
\alpha
-code entailment by leveraging the unit test generator
ℱ
\mathcal{{F}}
.
Definition 4.1
(
α
\alpha
-code entailment)
.
A unit test generator
ℱ
\mathcal{{F}}
on
𝐱
\mathbf{x}
,
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
,
α
\alpha
-entails
𝐲
^
∈
𝒴
\hat{\mathbf{y}}\in\mathcal{Y}
if
an
expected functional correctness
of
𝐲
^
\hat{\mathbf{y}}
with respect to
ℱ
\mathcal{{F}}
,
i.e.,
ℙ
{
𝐲
^
(
𝐮
)
=
𝐯
}
\mathbb{P}\left\{\hat{\mathbf{y}}(\mathbf{u})=\mathbf{v}\right\}
, satisfies
ℙ
{
𝐲
^
(
𝐮
)
=
𝐯
}
≥
1
−
α
,
\mathbb{P}\left\{\hat{\mathbf{y}}(\mathbf{u})=\mathbf{v}\right\}\geq 1-\alpha,
(2)
where the probability is taken over
(
𝐮
,
𝐯
)
∼
ℱ
⁡
(
𝐱
)
(\mathbf{u},\mathbf{v})\sim\mathcal{{F}}(\mathbf{x})
.
We formally re-define the concept of
probabilistic tests
originally introduced by
Massalin (1987)
.
Our definition differs from prior work,
Claessen and Hughes (2000)
;
McKeeman (1998)
;
Chen and Su (2015)
, which focuses on identifying counterexamples for program inequivalence.
Also, our definition differs slightly from program equivalence definitions in
Jakobs and Wiesner (2022)
;
Lahiri et al. (2012)
;
Felsing et al. (2014)
, as we use
α
\alpha
to accommodate different code generator quality and enhance practicality.
In code generation,
the
α
\alpha
-code entailment provides a foundation for measuring functional correctness.
In particular,
suppose that we have a target code snippet
𝐲
\mathbf{y}
for intuitive explanation. Then,
to measure the functional correctness between two code snippets
𝐲
\mathbf{y}
and
𝐲
^
\hat{\mathbf{y}}
, we need to check whether two code snippets
𝐲
\mathbf{y}
and
𝐲
^
\hat{\mathbf{y}}
have the same output state for all input states.
To check this bidirectional equivalence relation,
we first consider the one-directional definition via code entailment by checking whether code
𝐲
^
\hat{\mathbf{y}}
satisfies all input and output pairs for code
𝐲
\mathbf{y}
, equivalently unit tests from
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
where
𝐲
\mathbf{y}
is reference code for a problem
𝐱
\mathbf{x}
, following Definition
4.1
. By considering entailment from
𝐲
\mathbf{y}
to
𝐲
^
\hat{\mathbf{y}}
and vice versa, we can eventually define the functional equivalence.
In this paper, instead of analyzing the bidirectional equivalence, we only consider the one-directional relaxed notion of correctness via code entailment, which suffices for code generation,
e.g.,
we can say that
𝐲
^
\hat{\mathbf{y}}
is correct if it contains all functionalities of
𝐲
\mathbf{y}
along with other functionalities. The example of
α
\alpha
-entailment is presented in Table
.
4.2
False Discovery Rate via Code Entailment
We define a relation for the FDR risk in (
1
) via
α
\alpha
-code entailment.
We first denote the set of
α
\alpha
-entailment code snippets of
𝐱
\mathbf{x}
by
E
α
​
(
𝐱
)
E_{\alpha}(\mathbf{x})
,
i.e.,
E
α
(
𝐱
)
≔
{
𝐲
¯
∣
ℙ
{
𝐲
¯
(
𝐮
)
=
𝐯
}
≥
1
−
α
}
,
E_{\alpha}(\mathbf{x})\coloneqq\left\{\bar{\mathbf{y}}\mid\mathbbm{P}\{\bar{\mathbf{y}}(\mathbf{u})=\mathbf{v}\}\geq 1-\alpha\right\},
which approximately corresponds to the set of all code snippets that have the most functionalities described by unit tests from
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
.
By the definition of the
α
\alpha
-code entailment,
𝐲
^
∈
E
α
​
(
𝐱
)
\hat{\mathbf{y}}\in E_{\alpha}(\mathbf{x})
implies that
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
α
\alpha
-entails
𝐲
^
\hat{\mathbf{y}}
.
Using the same definition of
E
α
​
(
𝐱
)
E_{\alpha}(\mathbf{x})
, we further define the correctness relation between two code snippets as follows:
R
α
≔
{
(
𝐲
^
,
ℱ
⁡
(
𝐱
)
)
∣
𝐲
^
∈
E
α
​
(
𝐱
)
}
.
R_{\alpha}\coloneqq\left\{(\hat{\mathbf{y}},\mathcal{{F}}(\mathbf{x}))\mid\hat{\mathbf{y}}\in E_{\alpha}(\mathbf{x})\right\}.
Then, from (
1
), we define the FDR with code entailment relation
R
α
R_{\alpha}
(FDR-CE). Equivalently, we use the following FDR-CE definition:
ℛ
α
​
(
S
^
)
≔
ℙ
⁡
{
S
^
​
(
𝐱
)
∉
E
α
​
(
𝐱
)
|
S
^
​
(
𝐱
)
≠
IDK
}
.
\mathcal{{R}}_{\alpha}(\hat{{S}})\coloneqq\mathbbm{P}\{\hat{{S}}(\mathbf{x})\notin E_{\alpha}(\mathbf{x})\;|\;\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\}.
4.3
Code Entailment Estimation
In natural languages, an entailment relation between two sentences can be easily obtained by human annotators. However, identifying functionalities between two code snippets by humans (
i.e.,
deciding whether
S
^
​
(
𝐱
)
∉
E
α
​
(
𝐱
)
\hat{{S}}(\mathbf{x})\notin E_{\alpha}(\mathbf{x})
or not) is challenging due to the un-natural form of programming languages. We overcome this challenge with unit tests that exploit an
executable property of code
.
Inspired by
(
Lee et al., 2024
)
,
we estimate
E
α
E_{\alpha}
and use it as a pseudo-labeling function as the exact
E
α
E_{\alpha}
is difficult to obtain.
In particular,
recall
the expected functional correctness
ℙ
{
𝐲
¯
(
𝐮
)
=
𝐯
}
\mathbbm{P}\{\bar{\mathbf{y}}(\mathbf{u})=\mathbf{v}\}
between unit tests from a test generator on
𝐱
\mathbf{x}
,
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
, and a generated code snippet
𝐲
¯
\bar{\mathbf{y}}
from
𝐱
\mathbf{x}
.
Considering that the input-output pairs
(
𝐮
,
𝐯
)
(\mathbf{u},\mathbf{v})
are independently drawn from the test generator
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
,
we estimate the lower bound of the expected functional correctness by using the standard binomial tail bound.
Specifically,
let the lower binomial tail bound
L
^
\hat{{L}}
of
ℙ
{
𝐲
¯
(
𝐮
)
=
𝐯
}
\mathbbm{P}\{\bar{\mathbf{y}}(\mathbf{u})=\mathbf{v}\}
be
L
^
​
(
ℱ
⁡
(
𝐱
)
,
𝐲
¯
,
n
𝐱
,
ε
E
)
≔
L
^
Binom
​
(
k
^
,
n
𝐱
,
ε
E
)
\hat{{L}}(\mathcal{{F}}(\mathbf{x}),\bar{\mathbf{y}},n_{\mathbf{x}},\varepsilon_{E})\coloneqq\hat{{L}}_{\text{Binom}}(\hat{{k}};n_{\mathbf{x}},\varepsilon_{E})
,
where
n
𝐱
n_{\mathbf{x}}
is the number of samples,
𝐔
𝐱
∼
ℱ
​
(
𝐱
)
n
𝐱
\mathbf{U}_{\mathbf{x}}\sim\mathcal{{F}}(\mathbf{x})^{n_{\mathbf{x}}}
is a set of generated unit tests,
and
k
^
≔
∑
(
𝐮
,
𝐯
)
∈
𝐔
𝐱
𝟙
​
(
𝐲
¯
​
(
𝐮
)
=
𝐯
)
\hat{{k}}\coloneqq\sum_{(\mathbf{u},\mathbf{v})\in\mathbf{U}_{\mathbf{x}}}\mathbbm{1}(\bar{\mathbf{y}}(\mathbf{u})=\mathbf{v})
.
Here,
L
^
Binom
\hat{{L}}_{\text{Binom}}
is the lower standard binomial tail bound, where
F
⁡
(
k
,
n
,
θ
)
F(k;n,\theta)
is a cumulative distribution function of a binomial distribution with
n
n
trials and success probability
θ
\theta
,
and
L
^
Binom
​
(
k
,
n
,
δ
)
≔
sup
{
θ
∈
[
0
,
1
]
∣
1
−
F
⁡
(
k
,
n
,
θ
)
≤
δ
}
∪
{
0
}
\hat{{L}}_{\text{Binom}}(k;n,\delta)\coloneqq\sup\left\{\theta\in[0,1]\mid 1-F(k;n,\theta)\leq\delta\right\}\cup\{0\}
.
Then, due to its definition, the lower bound holds with high probability
(
Clopper and Pearson, 1934
)
as follows:
ℙ
{
L
^
(
ℱ
(
𝐱
)
,
𝐲
¯
,
n
𝐱
,
ε
E
)
≤
ℙ
𝐲
{
𝐲
¯
(
𝐮
)
=
𝐯
}
}
≥
1
−
ε
E
,
\mathbbm{P}\{\hat{{L}}(\mathcal{{F}}(\mathbf{x}),\bar{\mathbf{y}},n_{\mathbf{x}},\varepsilon_{E})\leq\mathbbm{P}_{\mathbf{y}}\{\bar{\mathbf{y}}(\mathbf{u})=\mathbf{v}\}\}\geq 1-\varepsilon_{E},
where the probability is taken over
𝐔
𝐱
∼
ℱ
​
(
𝐱
)
n
𝐱
\mathbf{U}_{\mathbf{x}}\sim\mathcal{{F}}(\mathbf{x})^{n_{\mathbf{x}}}
.
Importantly, we carefully choose reasonably small unit test size
n
𝐱
n_{\mathbf{x}}
for a given
𝐱
\mathbf{x}
via Algorithm
.
In particular,
sample size for the binomial tail bound is usually given, but we can generate as many samples as we wish by executing a unit test generator
ℱ
\mathcal{{F}}
.
Here, the number of samples should depend on the difficulty in evaluating the correctness of generated code
𝐲
^
\hat{\mathbf{y}}
,
i.e.,
as the generated code is ambiguous to check the
α
\alpha
-code entailment, we need more samples to be certain.
To this end, we increase the unit test size
n
𝐱
n_{\mathbf{x}}
until the lower bound
L
^
\hat{{L}}
of an expected functional correctness is larger than
1
−
α
1-\alpha
(Line
) to achieve the expected correctness as well.
If the sample size exceeds maximum size
n
max
n_{\text{max}}
, the algorithm returns
n
max
n_{\text{max}}
(Line
).
From this lower bound
L
^
\hat{{L}}
, we define an
estimated entailment set
as follows:
E
^
α
,
ε
E
​
(
𝐱
)
≔
{
𝐲
¯
|
L
^
​
(
ℱ
⁡
(
𝐱
)
,
𝐲
¯
,
n
𝐱
,
ε
E
)
≥
1
−
α
}
.
\hat{{E}}_{\alpha,\varepsilon_{E}}(\mathbf{x})\coloneqq\left\{\bar{\mathbf{y}}\;\middle|\;\hat{{L}}(\mathcal{{F}}(\mathbf{x}),\bar{\mathbf{y}},n_{\mathbf{x}},\varepsilon_{E})\geq 1-\alpha\right\}.
(3)
Intuitively, code
𝐲
¯
∈
E
^
α
,
ε
E
​
(
𝐱
)
\bar{\mathbf{y}}\in\hat{{E}}_{\alpha,\varepsilon_{E}}(\mathbf{x})
likely satisfies
𝐲
¯
∈
E
α
​
(
𝐱
)
\bar{\mathbf{y}}\in E_{\alpha}(\mathbf{x})
, meaning
ℱ
⁡
(
𝐱
)
\mathcal{{F}}(\mathbf{x})
α
\alpha
-entails
𝐲
^
\hat{\mathbf{y}}
with high probability.
Thus, the FDR-CE based on the estimated entailment set is defined as
ℛ
α
,
ε
E
​
(
S
^
)
≔
ℙ
⁡
{
S
^
​
(
𝐱
)
∉
E
^
α
,
ε
E
​
(
𝐱
)
|
S
^
​
(
𝐱
)
≠
IDK
}
.
\mathcal{{R}}_{\alpha,\varepsilon_{E}}(\hat{{S}})\!\coloneqq\!\mathbbm{P}\{\hat{{S}}(\mathbf{x})\notin\hat{{E}}_{\alpha,\varepsilon_{E}}(\mathbf{x})|\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\}.
Here, the probability is taken over
(
𝐱
,
n
𝐱
)
∼
𝒟
𝒳
×
ℕ
(\mathbf{x},n_{\mathbf{x}})\sim\mathcal{{D}}_{\mathcal{{X}}\times\mathbb{N}}
and
𝐔
𝐱
∼
ℱ
⁡
(
𝐱
)
\mathbf{U}_{\mathbf{x}}\sim\mathcal{{F}}(\mathbf{x})
,
where we simply denote the distribution associated to
(
𝐱
,
n
𝐱
,
𝐔
𝐱
)
(\mathbf{x},n_{\mathbf{x}},\mathbf{U}_{\mathbf{x}})
by
𝒟
\mathcal{{D}}
.
It is a good alternative for the original FDR-CE
ℛ
α
​
(
S
^
)
\mathcal{{R}}_{\alpha}(\hat{{S}})
.
In the following, we connect
ℛ
α
\mathcal{{R}}_{\alpha}
and
ℛ
α
,
ε
E
\mathcal{{R}}_{\alpha,\varepsilon_{E}}
in learning.
4.4
False Discovery Rate Bound
We consider the upper bound of the FDR-CE
ℛ
α
​
(
S
^
)
\mathcal{{R}}_{\alpha}(\hat{{S}})
, which leverages the estimated entailment set.
Specifically, from Lemma
2.1
, we have
ℛ
α
​
(
S
^
)
≤
ℙ
𝒟
S
^
​
{
e
=
0
,
e
^
=
1
}
+
ℛ
α
,
ε
E
​
(
S
^
)
.
\mathcal{{R}}_{\alpha}(\hat{{S}})\leq\mathbbm{P}_{\mathcal{{D}}_{\hat{{S}}}}\{e=0,\hat{{e}}=1\}+\mathcal{{R}}_{\alpha,\varepsilon_{E}}(\hat{{S}}).
Here,
e
≔
G
⁡
(
𝐱
)
∈
E
α
​
(
𝐱
)
e\coloneqq G(\mathbf{x})\in E_{\alpha}(\mathbf{x})
,
e
^
≔
G
⁡
(
𝐱
)
∈
E
^
α
,
ε
E
​
(
𝐱
)
\hat{{e}}\coloneqq G(\mathbf{x})\in\hat{{E}}_{\alpha,\varepsilon_{E}}(\mathbf{x})
,
and
ℙ
𝒟
S
^
{
⋅
}
=
ℙ
{
⋅
∣
S
^
(
𝐱
)
≠
IDK
}
\mathbbm{P}_{\mathcal{{D}}_{\hat{{S}}}}\{\cdot\}=\mathbbm{P}\{\cdot\mid\hat{{S}}(\mathbf{x})\neq\texttt{IDK}\}
,
where the probability is taken over
(
𝐱
,
n
𝐱
,
𝐔
𝐱
)
∼
𝒟
(\mathbf{x},n_{\mathbf{x}},\mathbf{U}_{\mathbf{x}})\sim\mathcal{{D}}
.
This intuitively suggests that the FDR-CE over the exact entailment set can be approximated by the FDR-CE over the estimated entailment set along with its false entailment rate (FER).
Moreover,
the FER is related to the correctness of the binomial tail bound, controlled by
ε
E
\varepsilon_{E}
.
This implies the following key lemma. See Appendix
for a proof.
Lemma 4.2
.
For any
α
,
ε
E
∈
(
0
,
1
)
\alpha,\varepsilon_{E}\in(0,1)
, and
S
^
\hat{{S}}
, we have
ℛ
α
​
(
S
^
)
≤
ε
E
+
ℛ
α
,
ε
E
​
(
S
^
)
.
\mathcal{{R}}_{\alpha}(\hat{{S}})\leq\varepsilon_{E}+\mathcal{{R}}_{\alpha,\varepsilon_{E}}(\hat{{S}}).
Next, we use this bound to provide an algorithm for
S
^
\hat{{S}}
, controlling this upper bound at a desired level.
4.5
FDR-CE Control Algorithm
We propose a selective generator learning algorithm for code that controls the FDR-CE.
In particular,
we consider a scalar-parameterization of the selection function
s
^
\hat{{s}}
,
i.e.,
s
^
​
(
𝐱
)
≔
𝟙
​
(
f
⁡
(
𝐱
,
G
⁡
(
𝐱
)
)
≥
τ
)
,
\hat{{s}}(\mathbf{x})\coloneqq\mathbbm{1}\left(f(\mathbf{x},G(\mathbf{x}))\geq\tau\right),
where
τ
∈
ℝ
\tau\in\mathbb{R}
.
While the scoring function can be any function that quantifies the confidence on generated code, we employ the standard length-normalized log-probability for generated tokens as the default choice,
i.e.,
f
norm
​
(
𝐱
,
G
⁡
(
𝐱
)
)
=
∑
i
ln
⁡
p
i
/
|
G
⁡
(
𝐱
)
|
f_{\text{norm}}(\mathbf{x},G(\mathbf{x}))={\sum_{i}{\ln p_{i}}}\mathbin{/}{|G(\mathbf{x})|}
,
where
p
i
p_{i}
is the probability assigned by
G
G
to generating the
i
i
-th token.
Additionally, we exploit hold-out
U
U
-unit tests as part of our new scoring function by averaging the
f
norm
f_{\text{norm}}
with a pass@1 score,
i.e.,
f
mixed
​
(
𝐱
,
G
⁡
(
𝐱
)
)
≔
0.5
​
f
norm
​
(
𝐱
,
G
⁡
(
𝐱
)
)
+
0.5
​
∑
(
u
i
,
v
i
)
∼
ℱ
⁡
(
𝐱
)
𝟙
​
(
G
⁡
(
𝐱
)
​
(
u
i
)
=
v
i
)
U
f_{\text{mixed}}(\mathbf{x},G(\mathbf{x}))\coloneqq 0.5f_{\text{norm}}(\mathbf{x},G(\mathbf{x}))+0.5\frac{\sum_{(u_{i},v_{i})\sim\mathcal{F}(\mathbf{x})}\mathbbm{1}(G(\mathbf{x})(u_{i})=v_{i})}{U}
.
Then, our algorithm searches
S
^
\hat{{S}}
that closely controls the upper bound in Lemma
4.2
within
ε
S
\varepsilon_{S}
by solving the following optimization problem:
min
τ
∈
ℝ
⁡
τ
​
subj. to
​
ε
E
+
U
^
Binom
​
(
k
^
,
|
𝐙
^
|
,
δ
S
⌈
log
2
⁡
|
𝐙
|
⌉
)
≤
ε
S
,
\min_{\tau\in\mathbb{R}}\tau~\text{subj. to}~\varepsilon_{E}+\hat{{U}}_{\text{Binom}}\left(\hat{{k}};|\hat{\mathbf{Z}}|,\frac{\delta_{S}}{\lceil\log_{2}|\mathbf{Z}|\rceil}\right)\leq\varepsilon_{S},
(4)
where
𝐙
∼
𝒟
n
\mathbf{Z}\sim\mathcal{{D}}^{n}
,
𝐙
^
≔
{
(
𝐱
,
𝐲
,
_
)
∈
𝐙
∣
f
⁡
(
𝐱
,
G
⁡
(
𝐱
)
)
≥
τ
}
\hat{\mathbf{Z}}\coloneqq\{(\mathbf{x},\mathbf{y},\_)\in\mathbf{Z}\mid f(\mathbf{x},G(\mathbf{x}))\geq\tau\}
,
k
^
≔
∑
(
𝐱
,
𝐲
,
_
)
∈
𝐙
^
𝟙
​
(
G
⁡
(
𝐱
)
∉
E
^
α
,
ε
E
​
(
𝐱
)
)
\hat{{k}}\coloneqq\sum_{(\mathbf{x},\mathbf{y},\_)\in\hat{\mathbf{Z}}}\mathbbm{1}(G(\mathbf{x})\notin\hat{{E}}_{\alpha,\varepsilon_{E}}(\mathbf{x}))
,
and
U
^
Binom
\hat{{U}}_{\text{Binom}}
is the upper binomial tail bound, similarly defined as the lower bound
L
^
Binom
\hat{{L}}_{\text{Binom}}
.
Here,
the algorithm also returns
U
^
≔
ε
E
+
U
^
Binom
​
(
⋅
)
\hat{{U}}\coloneqq\varepsilon_{E}+\hat{{U}}_{\text{Binom}}(\cdot)
, the upper bound of the FDR-CE for the optimal
τ
^
\hat{\tau}
.
We denote the algorithm solving (
4
) by
𝒜
SCG
\mathcal{{A}}_{\text{SCG}}
and see Algorithm
for its implementation details.
Appendix
includes guidelines on user-specified parameter selection.
At a high level, the algorithm essentially finds a selective code generator (parametrized by
τ
\tau
) that minimizes
τ
\tau
, to maximize the selection efficiency of the selective generator, under the constraint of controlling the FDR-CE by a desired level
ε
S
\varepsilon_{S}
. If the minimization is not feasible, the algorithm returns a selective generator that controls the minimum FDR-CE, indicated by
U
^
\hat{{U}}
.
Automated Unit Test Generation.
We consider any unit test generator
ℱ
:
𝒳
→
𝒰
×
𝒱
\mathcal{{F}}:\mathcal{{X}}\to\mathcal{{U}}\times\mathcal{{V}}
to generate a unit test
(
𝐮
,
𝐯
)
(\mathbf{u},\mathbf{v})
, including LLM-based unit test generators
(
Liu et al., 2023
;
Chen et al., 2023a
)
, and manual unit test generation. Here, we adopt a fuzzing method that has been popularized due to its simplicity and efficacy in finding bugs. This method is usually used for exploiting a certain execution to trigger bugs but we rather use it for exploring wider execution paths.
In particular,
we randomly sample a binary stream
s
s
from a seed distribution
𝒟
𝒰
\mathcal{{D}}_{\mathcal{{U}}}
and use it as a seed,
i.e.,
𝐬
∼
𝒟
𝒰
\mathbf{s}\sim\mathcal{{D}}_{\mathcal{{U}}}
, to arbitrarily assign an input state for code,
e.g.,
randomly initializing input parameters for a function call. The initial state typically fails to lead to an interesting execution path; therefore, the fuzzing method mutates the input seed to explore wider execution paths;
e.g.,
Atheris
(
Google, 2020
)
mutates an input to increase code coverage. Moreover, we consider problems
𝐱
\mathbf{x}
with reference code
𝐲
\mathbf{y}
. During this repeated execution of the reference code, multiple input and output state pairs are generated, and we randomly select one of them as our final pair
(
𝐮
,
𝐯
)
(\mathbf{u},\mathbf{v})
for each seed
𝐬
\mathbf{s}
.
Note that for LLM-based unit test generation or manual unit test generation, we often don’t need reference code
𝐲
\mathbf{y}
.
4.6
Controllability Guarantee
Our algorithm
𝒜
SCG
\mathcal{{A}}_{\text{SCG}}
controls an FDR-CE of a learned selective generator. This is a direct consequence of selective prediction
(
Geifman and El-Yaniv, 2017
;
Lee et al., 2024
)
. See a proof in Appendix
.
Theorem 4.3
.
For any
ε
S
∈
(
0
,
1
)
\varepsilon_{S}\in(0,1)
,
δ
S
∈
(
0
,
1
)
\delta_{S}\in(0,1)
,
α
∈
(
0
,
1
)
\alpha\in(0,1)
,
f
f
,
ℱ
\mathcal{{F}}
, and
𝒟
\mathcal{{D}}
, we have
ℙ
{
ℛ
α
(
S
^
)
≤
U
^
}
≥
1
−
δ
S
,
\mathbbm{P}\{\mathcal{{R}}_{\alpha}(\hat{{S}})\leq\hat{{U}}\}\geq 1-\delta_{S},
where
the probability is taken over
𝐙
∼
𝒟
n
\mathbf{Z}\sim\mathcal{{D}}^{n}
and
(
S
^
,
U
^
)
≔
𝒜
SCG
​
(
𝐙
)
(\hat{{S}},\hat{{U}})\coloneqq\mathcal{{A}}_{\text{SCG}}(\mathbf{Z})
.
This means that
𝒜
SCG
\mathcal{{A}}_{\text{SCG}}
finds a selective code generator satisfying a desired FDR-CE
ε
S
\varepsilon_{S}
(if
ε
S
≥
U
^
\varepsilon_{S}\geq\hat{{U}}
) or minimum level
U
^
\hat{{U}}
(if
U
^
>
ε
S
\hat{{U}}>\varepsilon_{S}
),
without human-feedback
on code entailment labels.
4.7
FuzzEval: Evaluation via Fuzzing
We suggest to use automatically generated unit tests via fuzzing in evaluation benchmarks where the reference code snippets are available and fuzzing harnesses are provided.
Traditionally, identifying the functional equivalence between desired code and generated code in code generation has relied on manually obtained unit tests,
e.g.,
HumanEval
(
Chen et al., 2021
)
.
But, as desired code becomes more complex so the number of its execution paths exponentially increases,
manually obtaining a sufficient number of unit tests is challenging. To address this bottleneck,
we propose to use fuzzing, a dynamic code analysis tool, to automatically generate unit tests for a given code snippet, calling this evaluation paradigm
FuzzEval
.
5
Experiments
We demonstrate the efficacy of our selective code generation on open and closed LLMs in an algorithmic solving task.
See Appendix
for additional experiments.
(a)
GPT-4o
(b)
Gemini-1.5 Pro
(c)
DeepSeek R1
Figure 2:
The box plots of the FDR-CE and selection efficiency for various LLMs (
δ
S
=
0.1
\delta_{S}=0.1
,
ε
S
=
0.3
\varepsilon_{S}=0.3
,
ε
E
=
0.05
\varepsilon_{E}=0.05
,
α
=
0.35
\alpha=0.35
). See Figure
for results with CodeLlama 13B Instruct.
Table 1:
Comparison results of
SCG
against baseline methods on different datasets with GPT-4o (
α
=
0.35
,
δ
S
=
0.1
,
ε
E
=
0.05
\alpha=0.35,\delta_{S}=0.1,\varepsilon_{E}=0.05
for all datasets). The FDR-CE satisfying the desired guarantees and the highest efficiency among methods that comply with the FDR-CE guarantees are marked in
bold.
Methods
w/o Selective Generation
w/ Selective Generation
τ
=
−
∞
\tau=-\infty
SCG-EM
SCG-manual
SCG-small
SCG-H
SCG
APPS-f
(
ε
S
=
0.3
\varepsilon_{S}=0.3
)
1 - pass@1
(
↓
)
(\downarrow)
0.436
0.436
±
0.012
\pm 0.012
0.020
0.020
±
0.098
\pm 0.098
0.293
0.293
±
0.014
\pm 0.014
0.226
0.226
±
0.015
\pm 0.015
0.282
0.282
±
0.020
\pm 0.020
0.227
0.227
±
0.017
\pm 0.017
FDR-CE
(
↓
)
(\downarrow)
0.431
0.431
±
0.011
\pm 0.011
0.020
0.020
±
0.099
\pm 0.099
0.291
0.291
±
0.014
\pm 0.014
0.226
0.226
±
0.015
\pm 0.015
0.280
0.280
±
0.020
\pm 0.020
0.224
0.224
±
0.018
\pm 0.018
Efficiency
(
↑
)
(\uparrow)
1.000
1.000
±
0.000
\pm 0.000
0.000
0.000
±
0.000
\pm 0.000
0.497
0.497
±
0.014
\pm 0.014
0.339
0.339
±
0.012
\pm 0.012
0.463
0.463
±
0.019
\pm 0.019
0.337
0.337
±
0.011
\pm 0.011
MBPP-f
(
ε
S
=
0.4
\varepsilon_{S}=0.4
)
1 - pass@1
0.299
0.299
±
0.022
\pm 0.022
0.000
0.000
±
0.000
\pm 0.000
0.258
0.258
±
0.040
\pm 0.040
-
0.301
0.301
±
0.028
\pm 0.028
0.304
0.304
±
0.032
\pm 0.032
FDR-CE
0.294
0.294
±
0.027
\pm 0.027
0.000
0.000
±
0.000
\pm 0.000
0.254
0.254
±
0.041
\pm 0.041
-
0.296
0.296
±
0.029
\pm 0.029
0.300
0.300
±
0.032
\pm 0.032
Efficiency
1.000
1.000
±
0.000
\pm 0.000
0.001
0.001
±
0.003
\pm 0.003
0.499
0.499
±
0.038
\pm 0.038
-
0.997
0.997
±
0.004
\pm 0.004
0.996
0.996
±
0.006
\pm 0.006
HumanEval-f
(
ε
S
=
0.3
\varepsilon_{S}=0.3
)
1 - pass@1
0.185
0.185
±
0.058
\pm 0.058
0.000
0.000
±
0.000
\pm 0.000
0.142
0.142
±
0.080
\pm 0.080
-
0.156
0.156
±
0.165
\pm 0.165
0.069
0.069
±
0.173
\pm 0.173
FDR-CE
0.207
0.207
±
0.064
\pm 0.064
0.000
0.000
±
0.000
\pm 0.000
0.156
0.156
±
0.086
\pm 0.086
-
0.145
0.145
±
0.123
\pm 0.123
0.049
0.049
±
0.111
\pm 0.111
Efficiency
1.000
1.000
±
0.000
\pm 0.000
0.008
0.008
±
0.017
\pm 0.017
0.492
0.492
±
0.080
\pm 0.080
-
0.578
0.578
±
0.401
\pm 0.401
0.164
0.164
±
0.118
\pm 0.118
Mercury-f
(
ε
S
=
0.3
\varepsilon_{S}=0.3
)
1 - pass@1
0.174
0.174
±
0.018
\pm 0.018
0.000
0.000
±
0.000
\pm 0.000
0.138
0.138
±
0.024
\pm 0.024
-
0.169
0.169
±
0.017
\pm 0.017
0.170
0.170
±
0.020
\pm 0.020
FDR-CE
0.170
0.170
±
0.019
\pm 0.019
0.000
0.000
±
0.000
\pm 0.000
0.133
0.133
±
0.022
\pm 0.022
-
0.164
0.164
±
0.019
\pm 0.019
0.165
0.165
±
0.020
\pm 0.020
Efficiency
1.000
1.000
±
0.000
\pm 0.000
0.001
0.001
±
0.002
\pm 0.002
0.504
0.504
±
0.033
\pm 0.033
-
0.998
0.998
±
0.003
\pm 0.003
0.998
0.998
±
0.002
\pm 0.002
(a)
Varying
ε
S
\varepsilon_{S}
(b)
Varying
α
\alpha
(c)
Varying Scoring Functions
Figure 3:
The FDR-CE results for GPT-4o with varying parameters and scoring functions. We use
ε
S
=
0.3
,
δ
S
=
0.1
,
α
=
0.35
\varepsilon_{S}=0.3,\delta_{S}=0.1,\alpha=0.35
, and
ε
E
=
0.05
\varepsilon_{E}=0.05
for Figure
3(a)
and
3(b)
and
ε
S
=
0.2
,
δ
S
=
0.1
,
α
=
0.15
\varepsilon_{S}=0.2,\delta_{S}=0.1,\alpha=0.15
, and
ε
E
=
0.05
\varepsilon_{E}=0.05
for Figure
3(c)
Table 2:
Comparison results of before and after applying
SCG
on various code generators, including
CodeT
(
Chen et al., 2023a
)
,
LDB
(
Zhong et al., 2024
)
, and
SFS
(
Light et al., 2025
)
with GPT-3.5-Turbo. We use
α
=
0.3
,
δ
S
=
0.1
,
ε
E
=
0.05
\alpha=0.3,\delta_{S}=0.1,\varepsilon_{E}=0.05
, and
ε
S
=
0.25
\varepsilon_{S}=0.25
for all datasets. We use the mixed scoring function
f
mix
f_{\text{mix}}
for this experiment. For HumanEval-f, we utilized a full dataset, whereas for MBPP-f, we constructed a new dataset using the union of subsets released by the authors of baseline methods. The FDR-CE satisfying the desired guarantees are marked in
bold.
Methods
Base Model
Chen et al. (2023a)
Zhong et al. (2024)
Light et al. (2025)
w/o
SCG
w/
SCG
w/o
SCG
w/
SCG
w/o
SCG
w/
SCG
w/o
SCG
w/
SCG
MBPP-f
1 - pass@1
(
↓
)
(\downarrow)
0.496
0.496
±
0.039
\pm 0.039
0.163
0.163
±
0.058
\pm 0.058
0.502
0.502
±
0.034
\pm 0.034
0.155
0.155
±
0.046
\pm 0.046
0.442
0.442
±
0.044
\pm 0.044
0.150
0.150
±
0.045
\pm 0.045
0.486
0.486
±
0.037
\pm 0.037
0.151
0.151
±
0.043
\pm 0.043
FDR-CE
(
↓
)
(\downarrow)
0.491
0.491
±
0.042
\pm 0.042
0.145
0.145
±
0.052
\pm 0.052
0.498
0.498
±
0.034
\pm 0.034
0.148
0.148
±
0.045
\pm 0.045
0.442
0.442
±
0.044
\pm 0.044
0.142
0.142
±
0.043
\pm 0.043
0.483
0.483
±
0.039
\pm 0.039
0.140
0.140
±
0.042
\pm 0.042
Efficiency
(
↑
)
(\uparrow)
1.000
1.000
±
0.000
\pm 0.000
0.576
0.576
±
0.039
\pm 0.039
1.000
1.000
±
0.000
\pm 0.000
0.587
0.587
±
0.040
\pm 0.040
1.000
1.000
±
0.000
\pm 0.000
0.655
0.655
±
0.044
\pm 0.044
1.000
1.000
±
0.000
\pm 0.000
0.604
0.604
±
0.038
\pm 0.038
HumanEval-f
1 - pass@1
(
↓
)
(\downarrow)
0.294
0.294
±
0.057
\pm 0.057
0.100
0.100
±
0.069
\pm 0.069
0.308
0.308
±
0.058
\pm 0.058
0.129
0.129
±
0.072
\pm 0.072
0.253
0.253
±
0.069
\pm 0.069
0.143
0.143
±
0.071
\pm 0.071
0.274
0.274
±
0.068
\pm 0.068
0.135
0.135
±
0.059
\pm 0.059
FDR-CE
(
↓
)
(\downarrow)
0.305
0.305
±
0.055
\pm 0.055
0.112
0.112
±
0.075
\pm 0.075
0.312
0.312
±
0.062
\pm 0.062
0.135
0.135
±
0.069
\pm 0.069
0.230
0.230
±
0.062
\pm 0.062
0.121
0.121
±
0.066
\pm 0.066
0.288
0.288
±
0.072
\pm 0.072
0.158
0.158
±
0.058
\pm 0.058
Efficiency
(
↑
)
(\uparrow)
1.000
1.000
±
0.000
\pm 0.000
0.778
0.778
±
0.065
\pm 0.065
1.000
1.000
±
0.000
\pm 0.000
0.808
0.808
±
0.061
\pm 0.061
1.000
1.000
±
0.000
\pm 0.000
0.878
0.878
±
0.052
\pm 0.052
1.000
1.000
±
0.000
\pm 0.000
0.850
0.850
±
0.056
\pm 0.056
5.1
Setup
Dataset.
We considered datasets with coding problems, where each problem has a correct solution. We chose APPS
(
Hendrycks et al., 2021
)
, Mercury
(
Du et al., 2024
)
, HumanEval
(
Chen et al., 2021
)
, and MBPP
(
Austin et al., 2021
)
for our task. Each dataset consists of Python programming questions, canonical code solutions, and a few unit tests.
Each Python programming question is provided to an LLM as a prompt to generate code, and then the generated code is measured for its functionality by running the unit tests.
We construct APPS-f, Mercury-f, HumanEval-f, and MBPP-f,
where for each dataset,
we replace the built in unit tests from each problem with automatically generated unit tests via fuzzing for both learning and evaluation.
In particular,
each question consists of constraints to inputs. We manually post-processed Python programming questions and their solutions of each dataset such that the solution code can be easily called by a fuzzing tool while satisfying the input constraints of questions.
Among the post-processed code,
we conducted fuzzing and extracted at least 600 input-output pairs as our unit tests for calibration and its evaluation. Additional details can be found in Appendix
.
LLMs.
We used three closed LLMs,
i.e.,
GPT-4o
(
OpenAI, 2024
)
, Gemini 1.5 Pro
(
Team et al., 2024
)
, GPT-4.1
(
OpenAI, 2025
)
and two open LLMs,
i.e.,
CodeLlama 13B-instruct
(
Rozière et al., 2024
)
and DeepSeek-R1
(
Guo et al., 2025
)
.
Here, we use the following default parameters unless specified:
ε
S
=
0.3
\varepsilon_{S}=0.3
,
δ
S
=
0.1
\delta_{S}=0.1
,
α
=
0.35
\alpha=0.35
,
ε
E
=
0.05
\varepsilon_{E}=0.05
,
and
n
max
=
150
n_{\text{max}}=150
.
Method.
We consider seven baseline methods
SCG-EM
(
Geifman and El-Yaniv, 2017
)
,
SCG-manual
,
SCG-small
,
SCG-H
,
CodeT
(
Chen et al., 2023a
)
,
LDB
(
Zhong et al., 2024
)
, and
SFS
(
Light et al., 2025
)
to compare with our method
SCG
.
•
SCG-EM
(
Geifman and El-Yaniv, 2017
)
: This baseline is a conventional selective predictor method that compares the generated code and solution code, without measuring its functional correctness.
•
SCG-manual
: This baseline is a simple selective generator that selects the upper
k
k
% of scores for a threshold
τ
\tau
to highlight the importance of controlling the FDR-CE.
•
SCG-small
:
This is our method but only using unit tests, provided by the APPS dataset to show the efficacy of generated unit tests via fuzzing. We sampled 21 test cases for each problem to apply our algorithm. See Appendix
for additional details.
•
SCG-H
: This baseline is a heuristic of our method omitting false entailment rate (FER) as in Lemma
4.2
.
It searches for a selective generator as in (
4
) with
ε
E
=
0
\varepsilon_{E}=0
(
i.e.,
an ablation method of ours).
Scoring Function.
To analyze the effect of calibration on our method
SCG
, we consider four different scoring functions. The detailed explanations on the scoring functions are provided in Appendix
but by default we use the length-normalized scoring function
f
norm
f_{\text{norm}}
unless specified.
Evaluation.
We evaluate our method along with baselines based on
the empirical counterpart of the FDR-CE and selection efficiency from a test set
𝐙
t
∼
𝒟
n
test
\mathbf{Z}_{\text{t}}\sim\mathcal{{D}}^{n_{\text{test}}}
in (
) and (
), respectively.
Interestingly,
FDR-CE and 1-
pass@1
(
Chen et al., 2021
)
on selected samples by
SCG
may be
asymptotically equivalent when
α
→
0
\alpha\to 0
and
n
𝐱
→
∞
n_{\mathbf{x}}\to\infty
for
pass@1
(See Appendix
for a discussion).
5.2
Results
We demonstrate the efficacy of our method
SCG
on different models, datasets, and programming languages. In addition, we highlight the benefits of fuzzing, and analyze the effect of calibration.
In short, the proposed method satisfies the desired FDR-CE constraint with reasonable efficiency (compared to the maximum efficiency of the underlying generators) where the baseline fails to do so (
i.e.,
SCG-EM
and
SCG-small
exhibit poor or trivial efficiency in Figure
2(a)
and Table
1
, respectively;
and
SCG-manual
and
SCG-H
violate the FDR-CE constraint in Figure
2(b)
).
5.2.1
Controllability and Selection Efficiency
Figure
2
shows that
SCG
controls the FDR-CE. To this end, we conducted random experiments.
We ran the experiment 50 times by randomly splitting the calibration set and test set at 8:2 ratio each time. The whiskers on each plot denote the range between
δ
S
\delta_{S}
and
1
−
δ
S
1-\delta_{S}
percentile of the distributions.
SCG-manual
may perform better than our method depending on the choice of
k
k
. However, manually selecting an appropriate
k
k
for different situations is a challenging task.
SCG-small
bounds the FDR-CE successfully. However, this method demonstrates lower efficiency compared to our method. The result stems from a lack of unit tests to correctly infer
expected functional correctness
, illustrating the advantage of fuzzing in learning.
SCG-H
shows that it is not able to bound a desired FDR-CE, as it ignores an estimation error for inferring expected functional correctness.
Our method shows how it successfully bounds desired FDR-CEs on diverse models (Figure
2
), diverse parameters (Figure
3
, Figure
), diverse datasets (Table
1
), diverse methods (Table
2
), and diverse programming languages (Table
).
In Figure
2
,
3
, and
, this is shown by the upper whisker bar lying below the desired FDR-CE in dotted line, while Table
1
,
2
,
, the results are indicated by bold text.
Table
shows qualitative results of our method that accepts correct code and rejects uncertain code.
Note that
a poorly performing model,
e.g.,
CodeLlama in Figure
, may not find a selective generator with a desired FDR-CE
ε
S
\varepsilon_{S}
. This is an expected result due to an un-calibrated scoring function
(
Lee et al., 2024
)
, as discussed in Section
5.2.4
.
5.2.2
Benefit of Fuzzing
We show the benefits of fuzzing in learning and evaluation.
We empirically show the benefit of fuzzing in learning.
As shown in Figure
,
the FDR-CE bound (at the top of the whisker) gets tighter to a desired FDR-CE level
without violating it
because smaller
ε
E
\varepsilon_{E}
requires a larger number of unit tests, thus providing a precise estimation on expected functional correctness.
This shows that generated unit tests by fuzzing help to provide a tighter FDR-CE guarantee, with higher selection efficiency.
Additionally, we demonstrate that
automatic unit test generation is beneficial in rigorous evaluation.
As shown in Figure
, the FDR-CE decreases as the number of unit tests for evaluation increases.
Recalling that
α
\alpha
-entailment is determined by comparing the lower bound of expected functional correctness with
1
−
α
1-\alpha
as in Definition
4.1
,
the lower bound gets tighter as we use more unit tests to evaluate code. The tighter lower bound results in more accurate comparison and evaluation, thus reducing the FDR-CE. This shows that fuzzing has a benefit of reducing evaluation error.
5.2.3
Extension over Prior Work
We compare our method
SCG
with prior code generation baselines and demonstrate that these baselines can be extended through our approach to provide additional functionality guarantees. As further discussed in Section
1.1
, improvements in functionality – inherently reducing
functional hallucination
– can be broadly categorized into two approaches: (1) enhancing the model performance during training or fine-tuning
(
OpenAI et al., 2025
;
Guo et al., 2025
)
or (2) employing post-filtering methods
(
Chen et al., 2023a
;
Zhong et al., 2024
;
Light et al., 2025
)
. In this work, we focus on comparison with post-filtering methods, as
SCG
post-processes the generated code to control hallucinations but training and fine-tuning based methods are orthogonal to this work.
Table
2
compares
SCG
with prior post-filtering methods. In particular,
SCG
controls and achieves lower FDR-CE than prior methods depending on the choice of
ε
S
\varepsilon_{S}
.
Furthermore, Table
2
,
, and Figure
3(a)
demonstrate the applicability of our method in a model- and method-agnostic manner across diverse experiment setups, including integration with finetuning methods (
e.g.,
DeepSeek GRPO, OpenAI RLHF) and compatibility with post-processing methods.
5.2.4
Effect of Scoring Function
We demonstrate the effect of calibration on our method
SCG
. As shown in Figure
3(c)
, the choice of scoring function affects whether FDR-CE can be successfully bounded to the desired
ε
S
\varepsilon_{S}
.
In particular,
f
verb
f_{\text{verb}}
in Figure
3(c)
fails to properly bound the FDR-CE.
Furthermore, CodeLlama in Figure
fails to find a selective generator with a desired
ε
S
\varepsilon_{S}
, due to an un-calibrated scoring function
(
Lee et al., 2024
)
. Thus, the model finds a minimum FDR-CE by returning
U
^
\hat{{U}}
in this case.
These results underscore the importance of selecting appropriate scoring functions for the efficacy of our method.
6
Conclusion
This paper considers the code hallucination problem. In particular,
we define the concept of code entailment based on automatically generated unit tests via fuzzing, one of the dynamic code analysis tools. Given this, we propose a learning algorithm for selective code generators to theoretically control the hallucination in the FDR of selective generators.
We further leverage fuzzing to automatically generate unit tests for learning and evaluation purposes, enabling the large-scale collection of unit tests.
Lastly, we demonstrate the controllability of the proposed selective generator and its selection efficiency over open and closed code generators under different experiment setups.
Limitations.
The proposed method controls the rate of hallucination, but its selection efficiency heavily depends on the quality of code generation models, requiring improvement for code generators. Moreover, the i.i.d. assumption for the FDR controllability guarantee limits its applicability in distribution-shifting environments.
Impact Statement
This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here.
Acknowledgment
We appreciate constructive feedback from anonymous reviewers.
This work was supported by Institute of Information & communications Technology Planning & Evaluation (IITP) and the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIT) (RS-2019-II191906, Artificial Intelligence Graduate School Program (POSTECH) (10%); RS-2024-00457882, National AI Research Lab Project (25%); No. RS-2024-00509258 and No. RS-2024-00469482, Global AI Frontier Lab (25%); RS-2025-00560062 (40%)).
References
Ahn
et al.
(2024)
J. Ahn, R. Verma, R. Lou, D. Liu, R. Zhang, and W. Yin
Large language models for mathematical reasoning: progresses and challenges
.
In
Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: Student Research Workshop
,
N. Falk, S. Papi, and M. Zhang (Eds.)
,
St. Julian’s, Malta
,
pp. 225–237
.
External Links:
Link
Cited by:
§1
.
Alshahwan
et al.
(2024)
N. Alshahwan, J. Chheda, A. Finogenova, B. Gokkaya, M. Harman, I. Harper, A. Marginean, S. Sengupta, and E. Wang
Automated unit test improvement using large language models at meta
.
In
Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering
,
FSE 2024
,
New York, NY, USA
,
pp. 185–196
.
External Links:
ISBN 9798400706585
,
Link
,
Document
Cited by:
§1.1
.
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton
Program synthesis with large language models
.
External Links:
2108.07732
,
Link
Cited by:
§1.1
,
§1
,
§5.1
.
Bowman
et al.
(2015)
S. Bowman, G. Angeli, C. Potts, and C. D. Manning
A large annotated corpus for learning natural language inference
.
In
Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing
,
pp. 632–642
.
Cited by:
Appendix A
,
§1
.
Brown
et al.
(2020)
T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei
Language models are few-shot learners
.
External Links:
2005.14165
Cited by:
§1
.
Cassano
et al.
(2022)
F. Cassano, J. Gouwar, D. Nguyen, S. Nguyen, L. Phipps-Costin, D. Pinckney, M. Yee, Y. Zi, C. J. Anderson, M. Q. Feldman,
et al.
Multipl-e: a scalable and extensible approach to benchmarking neural code generation
.
arXiv preprint arXiv:2208.08227
.
Cited by:
§1
.
Chen
et al.
(2023a)
B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J. Lou, and W. Chen
CodeT: code generation with generated tests
.
In
The Eleventh International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1.1
,
§1.1
,
§4.5
,
§5.1
,
§5.2.3
,
Table 2
,
Table 2
,
Table 2
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
External Links:
2107.03374
Cited by:
§1.1
,
§1
,
§1
,
§4.1
,
§4.7
,
§5.1
,
§5.1
.
Chen
et al.
(2023b)
W. Chen, X. Ma, X. Wang, and W. W. Cohen
Program of thoughts prompting: disentangling computation from reasoning for numerical reasoning tasks
.
Transactions on Machine Learning Research
.
Cited by:
§1
.
Chen and Su (2015)
Y. Chen and Z. Su
Guided differential testing of certificate validation in ssl/tls implementations
.
In
Proceedings of the 2015 10th Joint Meeting on Foundations of Software Engineering
,
ESEC/FSE 2015
,
New York, NY, USA
,
pp. 793–804
.
External Links:
ISBN 9781450336758
,
Link
,
Document
Cited by:
§4.1
.
Claessen and Hughes (2000)
K. Claessen and J. Hughes
QuickCheck: a lightweight tool for random testing of haskell programs
.
SIGPLAN Not.
35
(
9
),
pp. 268–279
.
External Links:
ISSN 0362-1340
,
Link
,
Document
Cited by:
§4.1
.
Clopper and Pearson (1934)
C. J. Clopper and E. S. Pearson
The use of confidence or fiducial limits illustrated in the case of the binomial
.
Biometrika
26
(
4
),
pp. 404–413
.
Cited by:
§4.3
.
Ding
et al.
(2024)
Y. Ding, J. Peng, M. J. Min, G. Kaiser, J. Yang, and B. Ray
SemCoder: training code language models with comprehensive semantics reasoning
.
In
Advances in Neural Information Processing Systems
,
A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (Eds.)
,
Vol.
37
,
pp. 60275–60308
.
External Links:
Link
Cited by:
§1.1
,
§1.1
.
Du
et al.
(2024)
M. Du, L. A. Tuan, B. Ji, Q. Liu, and S. Ng
Mercury: a code efficiency benchmark for code large language models
.
In
Advances in Neural Information Processing Systems
,
A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (Eds.)
,
Vol.
37
,
pp. 16601–16622
.
External Links:
Link
Cited by:
§1.1
,
§5.1
.
Fakhoury
et al.
(2025)
S. Fakhoury, M. Kuppe, S. K. Lahiri, T. Ramananandro, and N. Swamy
3DGen: ai-assisted generation of provably correct binary format parsers
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)
,
Vol.
,
Los Alamitos, CA, USA
,
pp. 2535–2547
.
External Links:
ISSN
,
Document
,
Link
Cited by:
§1.1
,
§1.1
.
Fakhoury
et al.
(2024)
S. Fakhoury, A. Naik, G. Sakkas, S. Chakraborty, M. Musuvathi, and S. Lahiri
Exploring the effectiveness of llm based test-driven interactive code generation: user study and empirical evaluation
.
In
Proceedings of the 2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings
,
ICSE-Companion ’24
,
New York, NY, USA
,
pp. 390–391
.
External Links:
ISBN 9798400705021
,
Link
,
Document
Cited by:
§1.1
,
§1.1
.
Felsing
et al.
(2014)
D. Felsing, S. Grebing, V. Klebanov, P. Rümmer, and M. Ulbrich
Automating regression verification
.
In
Proceedings of the 29th ACM/IEEE International Conference on Automated Software Engineering
,
ASE ’14
,
New York, NY, USA
,
pp. 349–360
.
External Links:
ISBN 9781450330138
,
Link
,
Document
Cited by:
§4.1
.
Geifman and El-Yaniv (2017)
Y. Geifman and R. El-Yaniv
Selective classification for deep neural networks
.
Advances in neural information processing systems
30
.
Cited by:
§1.1
,
§1
,
§2
,
§3
,
§4.6
,
1st item
,
§5.1
.
Google (2020)
Google
Atheris: a coverage-guided, native python fuzzer
.
External Links:
Link
Cited by:
Appendix A
,
§4.5
.
Guo
et al.
(2025)
D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi,
et al.
DeepSeek-r1 incentivizes reasoning in llms through reinforcement learning
.
Nature
645
(
8081
),
pp. 633–638
.
Cited by:
§1.1
,
§1.1
,
§1
,
§5.1
,
§5.2.3
.
Hendrycks
et al.
(2021)
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song, and J. Steinhardt
Measuring coding challenge competence with APPS
.
In
Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)
,
External Links:
Link
Cited by:
§1.1
,
§5.1
.
Hossain
et al.
(2024)
S. B. Hossain, N. Jiang, Q. Zhou, X. Li, W. Chiang, Y. Lyu, H. Nguyen, and O. Tripp
A deep dive into large language models for automated bug localization and repair
.
Proc. ACM Softw. Eng.
1
(
FSE
).
External Links:
Link
,
Document
Cited by:
§1
.
Huang
et al.
(2024)
B. Huang, S. Lu, X. Wan, and N. Duan
Enhancing large language models in coding through multi-perspective self-consistency
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 1429–1450
.
External Links:
Link
,
Document
Cited by:
§1.1
,
§1.1
.
Jakobs and Wiesner (2022)
M. Jakobs and M. Wiesner
PEQtest: testing functional equivalence
.
In
Fundamental Approaches to Software Engineering
,
E. B. Johnsen and M. Wimmer (Eds.)
,
Cham
,
pp. 184–204
.
External Links:
ISBN 978-3-030-99429-7
Cited by:
§4.1
.
Kim
et al.
(2025)
T. Kim, H. Han, S. Park, D. R. Jeong, D. Kim, D. Kim, E. Kim, J. Kim, J. Wang, K. Kim, S. Ji, W. Song, H. Zhao, A. Chin, G. Lee, K. Stevens, M. Alharthi, Y. Zhai, C. Zhang, J. Jang, Y. Jang, A. Askar, D. Kim, F. Fleischer, J. Cho, J. Kim, K. Ko, I. Yun, S. Park, D. Baik, H. Lee, H. Heo, M. Gwon, M. Lee, M. Baek, S. Min, W. Kim, Y. Jin, Y. Park, Y. Choi, J. Jung, G. Lee, J. Jang, K. Kim, Y. Cha, and Y. Kim
ATLANTIS: ai-driven threat localization, analysis, and triage intelligence system
.
External Links:
2509.14589
,
Link
Cited by:
§1
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
The Eleventh International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
.
Lahiri
et al.
(2012)
S. K. Lahiri, C. Hawblitzel, M. Kawaguchi, and H. Rebêlo
SYMDIFF: a language-agnostic semantic diff tool for imperative programs
.
In
Computer Aided Verification
,
P. Madhusudan and S. A. Seshia (Eds.)
,
Berlin, Heidelberg
,
pp. 712–717
.
External Links:
ISBN 978-3-642-31424-7
Cited by:
§4.1
.
Le
et al.
(2022)
H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. Hoi
CodeRL: mastering code generation through pretrained models and deep reinforcement learning
.
In
Advances in Neural Information Processing Systems
,
A. H. Oh, A. Agarwal, D. Belgrave, and K. Cho (Eds.)
,
External Links:
Link
Cited by:
§1.1
,
§1.1
.
Lee
et al.
(2024)
M. Lee, K. Kim, T. Kim, and S. Park
Selective generation for controllable language models
.
Advances in Neural Information Processing Systems
37
,
pp. 50494–50527
.
Cited by:
Appendix A
,
§1.1
,
§1
,
Lemma 2.1
,
§2
,
§3
,
§4.3
,
§4.6
,
§5.2.1
,
§5.2.4
.
Li
et al.
(2025)
D. Li, S. Cao, C. Cao, X. Li, S. Tan, K. Keutzer, J. Xing, J. E. Gonzalez, and I. Stoica
S*: test time scaling for code generation
.
In
Findings of the Association for Computational Linguistics: EMNLP 2025
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 15964–15978
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-335-7
Cited by:
§1.1
,
§1.1
.
Li
et al.
(2022)
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy, C. de Masson d’Autume, I. Babuschkin, X. Chen, P. Huang, J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S. Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals
Competition-level code generation with alphacode
.
Science
378
(
6624
),
pp. 1092–1097
.
External Links:
Document
,
Link
,
https://www.science.org/doi/pdf/10.1126/science.abq1158
Cited by:
§1.1
,
§1
.
Light
et al.
(2025)
J. Light, Y. Wu, Y. Sun, W. Yu, Y. Liu, X. Zhao, Z. Hu, H. Chen, and W. Cheng
SFS: smarter code space search improves LLM inference scaling
.
In
The Thirteenth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§5.1
,
§5.2.3
,
Table 2
,
Table 2
,
Table 2
.
Liu
et al.
(2023)
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
In
Proceedings of the 37th International Conference on Neural Information Processing Systems
,
NIPS ’23
,
Red Hook, NY, USA
.
Cited by:
§1.1
,
§1.1
,
§4.5
.
Manakul
et al.
(2023)
P. Manakul, A. Liusie, and M. Gales
SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models
.
In
The 2023 Conference on Empirical Methods in Natural Language Processing
,
Cited by:
§1
.
Massalin (1987)
H. Massalin
Superoptimizer: a look at the smallest program
.
In
Proceedings of the Second International Conference on Architectual Support for Programming Languages and Operating Systems
,
ASPLOS II
,
New York, NY, USA
,
pp. 122–126
.
External Links:
ISBN 0818608056
,
Link
,
Document
Cited by:
§4.1
.
McKeeman (1998)
W. M. McKeeman
Differential testing for software
.
Digit. Tech. J.
10
,
pp. 100–107
.
Cited by:
§4.1
.
Miller
et al.
(1990)
B. P. Miller, L. Fredriksen, and B. So
An empirical study of the reliability of unix utilities
.
Communications of the ACM
33
(
12
),
pp. 32–44
.
Cited by:
§1
.
Mohri and Hashimoto (2024)
C. Mohri and T. Hashimoto
Language models with conformal factuality guarantees
.
In
Proceedings of the 41st International Conference on Machine Learning
,
ICML’24
.
Cited by:
Appendix A
,
§1
,
§2
.
OpenAI
et al.
(2025)
OpenAI, :, A. El-Kishky, A. Wei, A. Saraiva, B. Minaiev, D. Selsam, D. Dohan, F. Song, H. Lightman, I. Clavera, J. Pachocki, J. Tworek, L. Kuhn, L. Kaiser, M. Chen, M. Schwarzer, M. Rohaninejad, N. McAleese, o3 contributors, O. Mürk, R. Garg, R. Shu, S. Sidor, V. Kosaraju, and W. Zhou
Competitive programming with large reasoning models
.
External Links:
2502.06807
,
Link
Cited by:
§1.1
,
§1.1
,
§1
,
§5.2.3
.
OpenAI (2024)
OpenAI
GPT-4 technical report
.
External Links:
2303.08774
,
Link
Cited by:
§5.1
.
OpenAI (2025)
OpenAI
Introducing gpt-4.1 in the api
.
External Links:
Link
Cited by:
§5.1
.
Quach
et al.
(2024)
V. Quach, A. Fisch, T. Schuster, A. Yala, J. H. Sohn, T. S. Jaakkola, and R. Barzilay
Conformal language modeling
.
In
The Twelfth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
,
§2
.
Rozière
et al.
(2024)
B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez, J. Rapin, A. Kozhevnikov, I. Evtimov, J. Bitton, M. Bhatt, C. C. Ferrer, A. Grattafiori, W. Xiong, A. Défossez, J. Copet, F. Azhar, H. Touvron, L. Martin, N. Usunier, T. Scialom, and G. Synnaeve
Code llama: open foundation models for code
.
External Links:
2308.12950
,
Link
Cited by:
§5.1
.
Semmle (2019)
Semmle
CodeQL
.
External Links:
Link
Cited by:
Appendix A
.
Team
et al.
(2024)
G. Team, P. Georgiev, V. I. Lei, R. Burnell, L. Bai, A. Gulati, G. Tanzer, D. Vincent, Z. Pan, S. Wang,
et al.
Gemini 1.5: unlocking multimodal understanding across millions of tokens of context
.
External Links:
2403.05530
,
Link
Cited by:
§5.1
.
Tian
et al.
(2025)
Y. Tian, W. Yan, Q. Yang, X. Zhao, Q. Chen, W. Wang, Z. Luo, L. Ma, and D. Song
Codehalu: investigating code hallucinations in llms via execution-based verification
.
In
Proceedings of the AAAI Conference on Artificial Intelligence
,
pp. 25300–25308
.
Cited by:
§1.1
.
Touvron
et al.
(2023)
H. Touvron, T. Lavril, G. Izacard, X. Martinet, M. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample
LLaMA: open and efficient foundation language models
.
External Links:
2302.13971
Cited by:
§1
.
Vovk
et al.
(2005)
V. Vovk, A. Gammerman, and G. Shafer
Algorithmic learning in a random world
.
Springer Science & Business Media
.
Cited by:
§1
.
Williams
et al.
(2018)
A. Williams, N. Nangia, and S. R. Bowman
A broad-coverage challenge corpus for sentence understanding through inference
.
In
Proceedings of NAACL-HLT
,
pp. 1112–1122
.
Cited by:
§1
.
Zalewski (2014)
M. Zalewski
Technical “whitepaper” for afl-fuzz
.
URl: http://lcamtuf. coredump. cx/afl/technical details. txt
.
Cited by:
Appendix A
.
Zhang
et al.
(2025)
Z. Zhang, Y. Wang, C. Wang, J. Chen, and Z. Zheng
LLM hallucinations in practical code generation: phenomena, mechanism, and mitigation
.
External Links:
Link
Cited by:
§1.1
.
Zhong
et al.
(2024)
L. Zhong, Z. Wang, and J. Shang
Debug like a human: a large language model debugger via verifying runtime execution step by step
.
In
Findings of the Association for Computational Linguistics ACL 2024
,
pp. 851–870
.
Cited by:
§5.1
,
§5.2.3
,
Table 2
,
Table 2
,
Table 2
.
Appendix A
Preliminary
Textual Entailment.
In natural languages, textual entailment is a concept of evaluating a semantic relation between two sentences by checking an entailment relation
(
Bowman et al., 2015
)
.
In particular,
denoting two sentences by a premise and a hypothesis,
we say that a premise entails a hypothesis if
the hypothesis is true given the premise. Otherwise, we say the premise contradicts the hypothesis.
This textual entailment has been used to measure semantic correctness between a question and an answer in learning language models
(
Mohri and Hashimoto, 2024
;
Lee et al., 2024
)
. If a generated answer entails a true one, we can consider the generated answer as true in textual entailment. In evaluating correctness of generated answers in natural language processing, introducing textual entailment is crucial as a simple, traditional exact match,
i.e.,
the generated answer and the true one are exactly the same, does not measure the semantic relation between two answers. However, in code generation, there is no notion of entailment to check the semantic correctness between two code snippets. We overcome this hurdle by introducing
code entailment
for measuring functional correctness, leveraging executable properties of code.
Dynamic Code Analysis via Fuzzing.
Computer programs suffer from undefined behaviors, called
bugs
,
e.g.,
crash by buffer overflow.
To find the bugs, security researchers have extensively developed static and dynamic code analysis tools,
e.g.,
CodeQL
(
Semmle, 2019
)
,
AFL
(
Zalewski, 2014
)
, and
Atheris
(
Google, 2020
)
.
The dynamic analysis tools exploit the executable property of code to find bugs, while the static analysis tools inspect code without execution.
We mainly focus on more informative dynamic analysis tools.
In particular,
fuzzing, a representative class of methods for dynamic code analysis, generates the input of a given program, called seed, executes the program with the input, and checks whether undefined behaviors can be observable. Given the observation, fuzzing methods randomly mutate the input of programs to explore wider execution paths or exploit execution paths toward targeted code.
In this paper, we re-purpose fuzzing methods for identifying functionality of code, instead of finding bugs in code by generating the input and output pairs of code.
Appendix B
Qualitative Result of our Methods
Table 3:
Qualitative results of our selective code generator with GPT-4o (
ε
S
=
0.3
\varepsilon_{S}=0.3
,
δ
S
=
0.1
\delta_{S}=0.1
,
ε
E
=
0.05
\varepsilon_{E}=0.05
, and
α
=
0.15
\alpha=0.15
).
The accepted generated code is
α
\alpha
-entailment with a score of
−
0.05
-0.05
, meaning high certainty, where the code is also semantically correct. The rejected code is not
α
\alpha
-entailment with the score of
−
53.87
-53.87
, meaning low certainty probably due to the complexity of the question. In particular, it returns a wrong answer, 2, for an input, [1,1,0,1,0,0,0,1,0,1,0,0,1,1,0,1], where the expected answer is 14, due to the inequality in “
count > max_count
” that does not follow the tie instruction.
Note that the contents are manually truncated for presentation purposes.