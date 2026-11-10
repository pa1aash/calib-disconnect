---
title: Eliminating Hallucination-Induced Errors in LLM Code Generation with Functional
  Clustering
id: eliminating-hallucination-induced-errors-in-llm-code-generation-with-functional
tags:
- code-llm-confidence-positioning-d82d00
- uq-code
created: '2026-11-09T23:08:14.616468Z'
updated: '2026-11-09T23:27:44.421520Z'
source: https://arxiv.org/html/2506.11021
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:14.615729Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT. CLOSE for L1. Functional clustering: execute 100 sampled programs
  on GPT-4o-generated tests, dominant I/O cluster mass as confidence; LiveCodeBench
  returned-answer error ~65% to 2% (36.8% answered), 0% at 15.6% coverage (Sec 4.2).
  GPT-4o, Claude-3-Haiku, GPT-4.1 variants. Threshold curves only; no ECE, no verbal/hidden-state
  confidence, no date-split contamination control.'
---

*Suggested by [[ensemble-based-uncertainty-estimation-for-code-correctness-estimation]] — cited as Ravuri and Amarasinghe 2025 functional clustering*

Eliminating Hallucination-Induced Errors in LLM Code Generation with Functional Clustering
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY-SA 4.0
arXiv:2506.11021v1 [cs.SE] 16 May 2025
Eliminating Hallucination-Induced Errors in LLM Code Generation with Functional Clustering
Chaitanya Ravuri
Affiliation:
Massachusetts Institute of Technology
Email:
cravuri@mit.edu
Saman Amarasinghe
Affiliation:
Massachusetts Institute of Technology
Email:
samana@mit.edu
Abstract
Modern code–generation LLMs can already solve a large fraction of programming problems, yet they still hallucinate subtle bugs that make their outputs unsafe for autonomous deployment. We present
functional clustering
, a black-box wrapper that eliminates nearly all hallucination-induced errors while providing a tunable confidence score. The wrapper samples many candidate programs, executes each on a self-generated test suite, and clusters candidates whose I/O behavior is identical; the empirical mass of the largest cluster serves as an exact confidence estimate. A single scalar threshold on this estimate lets users trade coverage for reliability with exponential guarantees. On
LiveCodeBench
our verifier preserves baseline pass@1 on solvable tasks yet slashes the error rate of returned answers from
∼
\sim
65% to 2%, and drives it to 0% at a conservative threshold while still answering 15.6% of prompts. Manual audits show that the few residual mistakes stem from prompt misinterpretation, not random generation noise, narrowing future work to specification clarity. Because the method requires only sampling and sandbox execution, it applies unchanged to closed-source APIs and future models, offering a practical path toward dependable, autonomous code generation. Our code is available on Github (
this https URL
).
1
Introduction
Large language models (LLMs) have begun to write code at a level once thought exclusive to experienced engineers: they pass university exams
[
22
]
, solve competitive
-
programming problems
[
15
]
, and even draft patches that compile in production repositories
[
18
]
. Despite this progress, practitioners hesitate to deploy them unsupervised
[
26
]
. A single off
-
by
-
one error or mistyped logical operator can crash an application or leak sensitive data, and state
-
of
-
the
-
art models still hallucinate such bugs with disconcerting frequency
[
10
]
.
Most recent work therefore augments LLMs with confidence scores
[
23
]
. Token
-
level likelihoods
[
12
]
, calibrated logits
[
3
]
, and semantic
-
embedding clustering
[
16
]
each offer partial signals, yet all miss a fundamental aspect of code. Two snippets that differ syntactically–or even occupy completely separate regions of embedding space–may be functionally identical. At the same time, semantically similar code with just single-character edits (such changing a
<
<
to
≤
\leq
) flips correctness without appreciably moving the embedding. Treating sequences or embeddings as the unit of analysis necessarily conflates these cases.
Our key observation is that software engineering already supplies an exact, model
-
agnostic criterion for identity: behavior on test inputs. In practice, virtually every production program is accepted not because it is formally proved but because it passes a finite test suite. We leverage the same idea at generation time. For each coding prompt the LLM produces a bag of candidate programs; the same model is then prompted to generate a diverse set of inputs (only inputs—no labeled outputs). Executing every program on every input in a sandbox yields an output vector; candidates whose vectors match exactly are placed in the same functional equivalence class. The empirical probability that a random sample belongs to the largest class, denoted
ρ
\rho
, becomes an
exact
confidence estimate.
This test
-
based clustering confers three immediate advantages.
First, it aligns the score with the real goal–correctness of behavior–rather than proxies such as token probability or embedding distance. If the model assigns
30
%
30\%
probability to two syntactically different but equivalent implementations,
ρ
\rho
correctly reports
60
%
60\%
confidence, whereas logit
-
based metrics would cap the score at
30
%
30\%
.
Second, the approach is entirely black
-
box: it requires only sampling and sandbox execution, not internal logits, gradient access, or fine
-
tuning. Consequently it wraps closed
-
source APIs as easily as open
-
weight models. Third, the statistic separates failure modes. Random
-
chance hallucinations fall exponentially fast with sample size; the rare high
-
confidence errors we observe stem exclusively from prompt misinterpretations. By isolating misunderstandings, the method turns reliability into a research problem that is both narrower and more tractable.
Contributions
1.
We frame uncertainty in code generation as density estimation over functional equivalence classes–programs that produce identical outputs on an automatically
-
generated test suite. This shifts the problem from approximate semantic similarity to exact behavioral identity, giving a mathematically crisp confidence signal without learned similarity models or log
-
probabilities.
2.
The method requires only (i) sampling multiple programs and (ii) running them in a sandbox. It attaches to any code LLM, including closed APIs, without fine
-
tuning, auxiliary classifiers, or access to internal logits. It does not require any additional knowledge beyond the prompt, as it generates its own test data.
3.
By prompting the base model for inputs only (not labeled test cases), we create a task
-
agnostic verifier that introduces no additional source of hallucination and zero human overhead.
4.
A universal threshold on dominant
-
cluster mass converts the LLM into a selective coder that either returns a representative program or abstains, giving a very high confidence of producing a correct solution when responding.
In short, functional clustering converts noisy LLM outputs into a confidence–based response, bringing dependable, autonomous code generation within reach. Empirically, wrapping a modern code LLM with our verifier preserves baseline pass@1 on solvable benchmark tasks while slashing the error rate of returned answers from roughly
65
%
65\%
to
2
%
2\%
. Raising the acceptance threshold drives residual error to zero at the cost of additional abstentions, giving users an explicit accuracy–coverage knob. Manual inspection confirms that remaining failures are all specification misunderstandings—no random hallucinations survive.
2
Related Work
Hallucinations in LLMs have attracted considerable attention, especially in precision-critical domains like code generation. Current research seeks to understand and classify these phenomena, mitigate their occurrence, and develop robust evaluation benchmarks. Below, we survey key directions in this area, highlighting gaps that our approach aims to address.
Hallucinations are outputs that read plausibly yet are semantically wrong. Huang et al.
[
5
]
and Islam et al.
[
21
]
organize natural-language hallucinations into factual, logical, and stylistic errors and catalog mitigation recipes across prompting, decoding and post-hoc verification. Code introduces new failure modes: HalluCode
[
10
]
shows that models mismap argument roles, misname identifiers and mismanage resources even when they compile, while CodeHalu
[
20
]
adds an execution-based benchmark that separates mapping, naming, resource and logic slips, demonstrating that functional correctness and intent fidelity remain brittle despite high surface fluency.
Multiple methods attempt to avoid these errors. One proposed method is to let the LLM grade its own answer. Kadavath et al.
[
7
]
prompt GPT-3 to output a verbal probability “P(True)” and find that the statement is better calibrated than raw token likelihoods, while Tian et al.
[
19
]
attach a value head fine-tuned with RLHF to supply confidence scores; both approaches improve in-domain calibration but generalize poorly to unseen tasks according to the broad empirical audit of Xiong et al.
[
23
]
.
A second method calibrates the token distribution itself Desai and Durrett
[
3
]
show that simple temperature scaling tightens expected calibration error for BERT-style classifiers, and Ma et al.
[
12
]
extend the idea to text generators by analyzing logit dispersion. Because token-based scores regard every distinct sequence as a different outcome, they must apportion probability mass across all syntactic variants of the same behaviour. If two programs that return identical outputs appear with 0.3 likelihood each, the model reports only 0.3 confidence for either one instead of 0.6 for the underlying solution. Thresholds or calibration curves built on that deflated score will wrongly flag many correct answers as “low-confidence,” forcing users to accept lower coverage or loosen the threshold and let more real errors slip through.
Supervised confidence heads trade label cost for sharper selectivity. Lin et al.
[
9
]
fine-tune GPT-3 to express its uncertainty in words; Liu et al.
[
11
]
train a lightweight linear adapter over the last hidden layer to predict a bias term that rescales logits. Though fine-tuned heads produce sharp confidence curves where they are trained, each new domain or model demands fresh annotated triples of
prompt, candidate code, correctness
. Collecting those labels is costly, often impossible for proprietary APIs, and must be repeated whenever the base model is updated—so the approach cannot serve as a drop-in wrapper across tasks or providers.
Embedding-based clustering targets semantic rather than lexical similarity. Farquhar et al.
[
4
]
introduce semantic entropy: they embed multiple generations, cluster by cosine similarity, and measure entropy to flag uncertainty, while Kuhn and Gal
[
8
]
and Qiu and Miikkulainen
[
16
]
refine the notion with invariance-aware kernels and density estimates. For natural language these groupings align with meaning, but for code the mapping from embedding space to behavior is loose. In code, moving from
<
to
<=
, a one-token change that may leave the embedding almost unchanged, can flip every test outcome, while two implementations with totally different variable names and control flow may sit far apart in the vector space yet return identical results. Relying on that geometry therefore blurs the line between correct and buggy solutions.
A recent code-specific variant by Sharma and David
[
17
]
executes symbolic traces to decide whether two programs match, then applies an entropy measure over trace clusters. Symbolic traces compare the exact sequence of states a program visits, so any change in control flow—a loop unrolled one extra time, a recursive call replaced by iteration—yields a different trace even if the outputs on all inputs are identical. As a result, probability mass that ought to accumulate on one correct solution is scattered across several trace “modes,” lowering the reported confidence for each and again driving overly cautious abstention thresholds.
Selective-answer frameworks build reliability guarantees on top of any base score. Abbasi Yadkori et al.
[
24
]
adapt conformal prediction to language models, proving error-rate bounds when the model abstains below a threshold, and Ye et al.
[
25
]
benchmark twenty UQ metrics across tasks, confirming that abstention policies can dominate naive always-answer baselines if the underlying score is well-aligned with correctness.
Despite this progress no existing signal is simultaneously behavioral, exact and black-box. Our functional-clustering verifier fills the gap by treating “produces identical outputs on an automatically generated test suite” as the atomic equivalence relation, merging syntactically diverse but behaviorally identical implementations and concentrating probability mass where it belongs. Because it needs only sampling and sandbox execution, the method plugs directly into the abstention frameworks above and wraps either open-weight or proprietary models without retraining or logit access.
To verify that functional clustering delivers practical reliability, we test it on two widely adopted benchmarks that cover complementary slices of the code-generation landscape. HumanEval
[
2
]
consists of 164 short Python functions, each equipped with hidden unit tests that probe corner cases; because every prompt is self-contained and free from training contamination, pass@k here isolates the model’s raw reasoning and synthesis skills and reveals how much accuracy is recovered once low-confidence answers are filtered out. LiveCodeBench
[
6
]
pushes the same models into longer, resource-bound problems executed in sandboxes under real-time and memory limits; tasks require reading from
stdin
, writing to
stdout
, and handling large inputs, so they approximate continuous-integration pipelines and competitive-programming judges. Success on HumanEval shows that the verifier preserves baseline coverage on micro-level logic, while gains on LiveCodeBench demonstrate that the same mechanism scales to production-style constraints where a single hidden bug can lead to an incorrect solution.
3
Methodology
This section lays out the full technical scaffold behind our verifier. We begin by formalizing the task and the notion of
functional equivalence
(Section
3.1
). We then derive an exact—but usually intractable—confidence metric based on the probability mass of an equivalence class and show how it can be estimated from finite samples (Section
3.2
). Next, we replace undecidable equivalence with a test
-
based proxy and analyze the resulting error bounds (Section
3.4
). Finally, we assemble these pieces into a practical inference algorithm and discuss its computational profile (Section
3.5
).
3.1
Problem statement
Let
𝒳
\mathcal{X}
and
𝒴
\mathcal{Y}
denote the input and output domains of a programming task described by natural
-
language prompt
𝐩
\mathbf{p}
. Conditioned on
𝐩
\mathbf{p}
, an auto-regressive LLM defines a predictive distribution
ℙ
\mathbb{P}
over syntactically valid programs
ϕ
∈
𝒫
\phi\in\mathcal{P}
. For a concrete program
ϕ
∈
𝒫
\phi\in\mathcal{P}
its semantics is the
deterministic function
f
ϕ
:
𝒳
→
𝒴
f_{\phi}:\mathcal{X}\to\mathcal{Y}
.
Two programs are
functionally equivalent
when they return the same output on every possible input:
ϕ
1
≡
ϕ
2
⟺
∀
x
∈
𝒳
,
f
ϕ
1
​
(
x
)
=
f
ϕ
2
​
(
x
)
.
\phi_{1}\equiv\phi_{2}\;\Longleftrightarrow\;\forall x\in\mathcal{X},\;f_{\phi_{1}}(x)=f_{\phi_{2}}(x).
(1)
Throughout the paper we assume that
each task has a single correct output for any given input
. That is, if two programs differ in their behavior on even one test case they cannot both be fully correct. Some benchmark problems violate this assumption–for example, tasks that accept any permutation, any tie-breaking order, or any string that matches a regular expression. We treat such tasks as out of scope, but note that a similar method as ours could be used to determine equivalency in such problems.
Our aim is to (i) estimate the probability mass that
ℙ
\mathbb{P}
assigns to the equivalence class of the program we ultimately return and (ii) output that program only when the mass exceeds a user
-
chosen threshold
τ
∈
(
0
,
1
]
\tau\in(0,1]
; otherwise we abstain. Equivalence classes are defined by Eq.
1
. The intuition is that genuine solutions tend to coalesce: there are many syntactic ways to implement the same correct algorithm, so correct programs accumulate probability in a shared equivalence class. By contrast, hallucinated errors are essentially random and therefore split their probability mass across many small, disjoint classes. A large observed class is thus strong evidence of correctness, whereas a small class signals either rarity or error.
Because universal equivalence is undecidable, we approximate it with agreement on a finite, automatically generated test set and show that the resulting estimator inherits exponential reliability guarantees.
3.2
Empirical confidence
The exact confidence of
ϕ
^
\hat{\phi}
is
C
(
ϕ
^
)
=
Pr
Φ
∼
ℙ
[
Φ
≡
ϕ
^
]
,
C(\hat{\phi})\;=\;\Pr_{\Phi\sim\mathbb{P}}\bigl[\Phi\equiv\hat{\phi}\bigr],
(2)
i.e. the total probability mass of its equivalence class. Calculating
C
C
according to Eq.
2
is typically intractable, so we resort to Monte
-
Carlo:
C
^
n
(
ϕ
^
)
=
1
n
∑
i
=
1
n
[
Φ
i
≡
ϕ
^
]
,
Φ
i
∼
i.i.d.
ℙ
.
\hat{C}_{n}(\hat{\phi})=\frac{1}{n}\sum_{i=1}^{n}\mathbf{1}\!\bigl[\Phi_{i}\equiv\hat{\phi}\bigr],\qquad\Phi_{i}\stackrel{{\scriptstyle\text{i.i.d.}}}{{\sim}}\mathbb{P}.
(3)
The indicator in Eq.
3
is Bernoulli with mean
C
⁡
(
ϕ
^
)
C(\hat{\phi})
, hence
C
^
n
\hat{C}_{n}
is unbiased and its variance scales as
C
⁡
(
1
−
C
)
/
n
C(1-C)/n
.
3.3
Abstention rule and its reliability
We
answer
when
C
^
n
​
(
ϕ
^
)
≥
τ
\hat{C}_{n}(\hat{\phi})\geq\tau
and
abstain
otherwise. The probability of a (potentially harmful) false acceptance is
Pr
⁡
[
C
^
n
≥
τ
∣
C
]
=
∑
k
=
⌈
n
​
τ
⌉
n
(
n
k
)
​
C
k
​
(
1
−
C
)
n
−
k
.
\Pr[\hat{C}_{n}\geq\tau\mid C]\;=\sum_{k=\lceil n\tau\rceil}^{n}\binom{n}{k}C^{k}(1-C)^{n-k}.
(4)
When
C
<
τ
C<\tau
, the tail in Eq.
4
can be bounded with exponential tightness:
Pr
[
C
^
n
≥
τ
∣
C
]
≤
exp
[
−
n
D
KL
(
τ
∥
C
)
]
,
\Pr[\hat{C}_{n}\geq\tau\mid C]\;\leq\;\exp\!\bigl[-n\,D_{\mathrm{KL}}(\tau\|C)\bigr],
(5)
where
D
KL
D_{\mathrm{KL}}
is the binary KL divergence. The quantity
D
KL
(
τ
∥
C
)
D_{\mathrm{KL}}(\tau\|C)
measures the per
-
sample information cost of confounding a Bernoulli distribution of mean
C
C
with one of mean
τ
\tau
. Whenever
τ
≠
C
\tau\neq C
this cost is strictly positive, so the error probability decays exponentially in
n
n
. Doubling the sample size approximately squares the bound, providing a simple knob for practitioners to dial target reliability. The proof of this bound is given in Appendix
A
.
In our experiments we take
n
=
100
n=100
. With a moderate gap
τ
−
C
=
0.2
\tau-C=0.2
the divergence is
D
KL
(
τ
∥
C
)
≈
0.14
D_{\mathrm{KL}}(\tau\|C)\approx 0.14
, so
n
​
D
KL
≈
14
nD_{\mathrm{KL}}\approx 14
and Eq.
5
upper
-
bounds the false
-
accept probability by
e
−
14
≈
10
−
6
e^{-14}\approx 10^{-6}
. This level of assurance is sufficient for practical deployment; larger
n
n
or a wider gap further suppresses risk at the cost of additional LLM queries. Thus, the abstention rule converts the intrinsic randomness of LLM sampling into a rigorously quantified, exponentially small chance of returning a low-confidence solution.
3.4
Practical equivalence via testing
Exact functional equivalence is coNP
-
hard in general, and undecidable when programs may not halt. Mirroring real-world software developmental practice, we use a test
-
based oracle. Let
𝒮
=
{
x
1
,
…
,
x
m
}
\mathcal{S}=\{x_{1},\dots,x_{m}\}
be a set of test inputs drawn from a task
-
dependent distribution
𝒟
\mathcal{D}
. We declare
ϕ
1
≡
𝒮
ϕ
2
⟺
f
ϕ
1
(
x
j
)
=
f
ϕ
2
(
x
j
)
for all
j
.
\phi_{1}\equiv_{\mathcal{S}}\phi_{2}\quad\Longleftrightarrow\quad f_{\phi_{1}}(x_{j})=f_{\phi_{2}}(x_{j})\;\text{ for all }j.
(6)
Suppose two programs disagree on a measurable subset
ℬ
⊆
𝒳
\mathcal{B}\subseteq\mathcal{X}
with
𝒟
⁡
(
ℬ
)
=
δ
>
0
\mathcal{D}(\mathcal{B})=\delta>0
. The oracle defined in Eq.
6
only fails to expose this difference precisely when none of the test inputs
𝒮
\mathcal{S}
are in
ℬ
\mathcal{B}
. The probability of that occurring is
Pr
[
ϕ
1
≡
𝒮
ϕ
2
]
=
(
1
−
δ
)
m
.
\Pr[\phi_{1}\equiv_{\mathcal{S}}\phi_{2}]\;=\;(1-\delta)^{m}.
(7)
Thus, with only hundreds of random tests, the probability in Eq.
7
is exponentially unlikely unless the behavioral divergence itself is vanishingly small. In practice most real defects (off
-
by
-
one errors, edge
-
case branches, etc.) affect a sizable slice of the input space, so such a guarantee suffices. The outer Chernoff exponent in
n
n
from Eq.
5
and the inner detection exponent in
m
m
from Eq.
7
compound multiplicatively: increasing either budget tightens overall guarantees without hidden interactions. Consequently our procedure inherits the best of both worlds—
statistical rigor
from concentration inequalities and
engineering practicality
from black
-
box testing—while remaining compatible with modern LLM pipelines that already generate large candidate batches for re-ranking or self
-
consistency.
3.5
Function clustering routine
Algorithm
1
summarizes the complete pipeline executed at inference time. The routine is parameter
-
free except for three user
-
visible knobs: the number of candidate programs
n
n
, the number of automatically generated test inputs
m
m
, and the acceptance threshold
τ
\tau
.
Algorithm 1
Functional Clustering
1:
task description
𝐩
\mathbf{p}
(string); sample budgets
n
n
(programs) and
m
m
(inputs)  threshold
τ
∈
(
0
,
1
]
\tau\in(0,1]
2:
abstain
or a high
-
confidence program
φ
^
\hat{\varphi}
3:
Step 1: Candidate program sampling
4:
for
i
←
1
i\leftarrow 1
to
n
n
do
5:
φ
i
←
LLMGenerateProgram
​
(
𝐩
)
\varphi_{i}\leftarrow\textsc{LLMGenerateProgram}(\mathbf{p})
6:
Step 2: Test
-
input generation
7:
for
j
←
1
j\leftarrow 1
to
m
m
do
8:
x
j
←
LLMGenerateInput
​
(
𝐩
)
x_{j}\leftarrow\textsc{LLMGenerateInput}(\mathbf{p})
9:
Step 3: Behavioural execution
10:
for
i
←
1
i\leftarrow 1
to
n
n
do
11:
for
j
←
1
j\leftarrow 1
to
m
m
do
12:
o
i
​
j
←
SandboxRun
​
(
φ
i
,
x
j
)
o_{ij}\leftarrow\textsc{SandboxRun}(\varphi_{i},x_{j})
13:
𝐨
i
←
(
o
i
​
1
,
…
,
o
i
​
m
)
\mathbf{o}_{i}\leftarrow(o_{i1},\dots,o_{im})
⊳
\triangleright
output vector
14:
Step 4: Equivalence clustering
15:
Partition
{
φ
i
}
i
=
1
n
\{\varphi_{i}\}_{i=1}^{n}
into classes
𝒞
1
,
…
,
𝒞
K
\mathcal{C}_{1},\dots,\mathcal{C}_{K}
where
𝐨
a
=
𝐨
b
\mathbf{o}_{a}=\mathbf{o}_{b}
iff
a
,
b
∈
𝒞
k
a,b\in\mathcal{C}_{k}
16:
s
max
←
max
k
⁡
|
𝒞
k
|
s_{\max}\leftarrow\max_{k}|\mathcal{C}_{k}|
17:
Step 5: Decision
18:
if
s
max
≥
⌈
τ
​
n
⌉
s_{\max}\geq\lceil\tau n\rceil
then
19:
return
any
φ
∈
arg
​
max
k
⁡
|
𝒞
k
|
\varphi\in\operatorname*{arg\,max}_{k}|\mathcal{C}_{k}|
⊳
\triangleright
high
-
confidence answer
20:
else
21:
return
abstain
The verifier proceeds in three steps. An LLM is first queried
n
n
times for candidate programs
φ
1
:
n
\varphi_{1:n}
and
m
m
times for test inputs
x
1
:
m
x_{1:m}
. We then execute every program on every input in a sandbox, recording the output vectors
𝐨
i
=
(
o
i
​
1
,
…
,
o
i
​
m
)
\mathbf{o}_{i}=(o_{i1},\dots,o_{im})
. Candidates whose vectors match exactly are grouped; if the largest group contains at least
τ
​
n
\tau n
elements we return any representative (all are functionally equivalent on the tests), otherwise we output
abstain
. Exact I/O equality replaces embedding or logit heuristics with a behavioral notion of equivalence.
Computational cost.
The procedure issues
n
+
m
n+m
LLM calls, so
T
LLM
=
𝒪
⁡
(
n
+
m
)
T_{\mathrm{LLM}}=\mathcal{O}(n+m)
dominates wall
-
clock time. Local sandbox evaluation performs
n
​
m
nm
runs,
T
exec
=
𝒪
⁡
(
n
​
m
)
T_{\mathrm{exec}}=\mathcal{O}(nm)
, but those runs are fast relative to the LLM calls. Memory is linear in
n
+
m
n+m
because each vector component is constant
-
size.
4
Experiments
We evaluate our verifier on
HumanEval
and
LiveCodeBench
using two code LLMs: GPT-4o
[
14
]
and Claude-3-Haiku
[
1
]
. For each task we sample 50 candidate programs from each model (100 total) with chain-of-thought plus code prompting; all prompts are reproduced verbatim in Appendix
B
. The self-generated test suites are produced by GPT-4o alone. We then cluster the 100 programs by exact I/O behavior and apply the thresholding rules introduced in Section
3
. Unless stated otherwise, metrics on
HumanEval
use only GPT-4o generations, while
LiveCodeBench
results use the full 100-sample pool.
4.1
HumanEval
(a)
Correctness versus estimated confidence on
HumanEval
.
(b)
Correctness versus estimated confidence on
LiveCodeBench
.
Figure 1
:
Correctness versus estimated confidence across datasets.
Colors encode correctness; Each point is a response that is either correct or wrong, with its
x
x
position denoting the model’s confidence in the response, and its
y
y
position meaningless. Dashed lines mark confidence thresholds, each guaranteeing an empirical error rate of at most the indicated percentage for returned answers. The Cum. Wrong / Cum. Correct step curves plot the cumulative percentage of incorrect and correct programs whose confidence lies above each point on the
x
x
-axis.
Figure
1(a)
plots correctness versus estimated confidence
C
^
n
\hat{C}_{n}
on
HumanEval
. The two step-shaped traces labeled
Cum. Wrong
and
Cum. Correct
summarize the scatter: at every
x
x
-axis value they report, respectively, the percentage of incorrect and of correct submissions whose confidence is greater than that value. Reading the curves from right to left therefore shows how residual error (red curve) and retained coverage (green curve) evolve as one lowers a single acceptance threshold. The baseline pass@1 of GPT-4o is
84.9
84.9
%. With functional clustering we achieve
85.2
85.2
% accuracy at the
τ
2
%
\tau_{2\%}
operating point. Only four tasks lie above the threshold with incorrect code; manual inspection shows that every one of them stems from a prompt misunderstanding rather than a hallucinated bug.
To probe these outliers we rewrote each problematic specification, adding a single clarifying sentence. After the rewrites the model produces high-confidence correct solutions for all four tasks, confirming that the verifier pinpoints specification ambiguity rather than generation noise. Full rewrites are included in Appendix
C
.
4.2
LiveCodeBench
Figure
1(b)
shows the same analysis for
LiveCodeBench
. Confidence again cleanly separates regimes: below
C
^
n
=
0.34
\hat{C}_{n}=0.34
wrong answers dominate; between
0.34
0.34
and
0.57
0.57
the accuracy–coverage trade-off follows the exponential tail predicted by Eq.
5
; above
0.57
0.57
we observe no errors. At
τ
2
%
\tau_{2\%}
the verifier returns
36.8
%
36.8\%
of tasks with a
2
%
2\%
residual error, while
τ
0
%
\tau_{0\%}
answers
15.6
%
15.6\%
of tasks with zero observed errors. Together, these observations confirm that a single scalar threshold gives practitioners a transparent knob to dial coverage versus reliability, with the conservative choice
τ
0
%
\tau_{0\%}
guaranteeing zero observed errors in our evaluation.
Table
1
generalizes that idea across models. We test on three variants of GPT-4.1
[
13
]
, in addition to the GPT-4o and Claude-3-Haiku testing we have done previously. For each model we first locate the confidence cut-off that yields its raw expected accuracy, then report the remaining error rate, i.e. the percentage of tasks on which the model both predicts and is wrong. A lower value therefore signals better calibrated abstention at the model’s own accuracy level. GPT-4o is the clear winner: at its expected accuracy of 36.9% it incurs only a 4.1% error rate, less than half that of any GPT-4.1 variant and one-third that of Claude-3-Haiku. In short, strong confidence separation is not merely a property of our verifier; it is also a competitive axis on which base models differ.
Table 1
:
Error rate when each model is thresholded to the confidence level that achieves its expected accuracy on
LiveCodeBench
. Lower error rates indicate better calibrated abstention.
Model
Expected accuracy (%)
Error rate (%)
GPT-4.1-mini
67.76
11.90
GPT-4.1
66.48
9.52
GPT-4.1-nano
45.95
9.52
GPT-4o
36.93
4.11
Claude-3-Haiku
21.71
12.33
Reasons for Error.
For every task whose dominant cluster was still wrong, we manually inspected the generated programs and grouped the failures into five categories:
(O)
Out-of-scope tasks.
A handful of
LiveCodeBench
problems permit multiple equally valid outputs (e.g. any permutation, either traversal order). Because our verifier presumes a single correct equivalence class, such tasks cannot be resolved by clustering alone.
(I)
Incomplete response.
Trivial syntactic slips, such as omitting a final print, never calling
main
, or leaving “
# TODO
” stubs, that a human would not commit.
(S)
Simple one-line mistakes.
The algorithm is conceptually correct but a one-line error (
<
vs.
<=
, off-by-one, misplaced modulo) breaks edge cases.
These are slips a novice programmer might make.
(HC)
Hard mistakes (missing constraint).
The model overlooks a specification detail (array bounds, divisibility, …) producing a coherent yet wrong algorithm. Many such variants agree with each other, so they can persist into medium-confidence clusters; clarifying examples or rewriting the prompt would likely fix them.
(HA)
Hard mistakes (wrong algorithm).
The chosen approach itself is invalid (e.g. greedy instead of dynamic programming). This mirrors errors an experienced programmer might make on a tricky problem.
(TL)
Time limit exceeded.
The approach is valid, but is inefficient, taking too long on the provided test cases. These errors are not ones that our method is specifically designed to catch, as it looks for correctness not efficiency.
Table
2
reports six accuracy metrics after successively removing each error category (letters are cumulative; e.g.,
O+HC
drops out-of-scope tasks and hard mistakes caused by missing a constraint).
Threshold accuracies
are measured after clustering with
τ
\tau
tuned so that the returned-answer error rate does not exceed
0
%
0\%
,
1
%
1\%
, or
2
%
2\%
; tasks falling below the threshold are returned as
unknown
.
Expected accuracy
is the average probability of emitting a correct program across 100 generations per task, while
clustered accuracy
always returns the majority-cluster program with no thresholding.
Maximum accuracy
is an oracle upper bound that counts a task as solved if any of the 100 generations is correct.
Comparing the rows shows how aggressive filtering tightens guarantees. Dropping only out-of-scope tasks already lifts
τ
2
%
\tau_{2\%}
accuracy above the expected baseline, offering better precision with just a
2
%
2\%
residual error. Achieving the same edge over expected accuracy at
τ
1
%
\tau_{1\%}
requires removing tasks where the model ignores a constraint (
HC
); a zero-error policy demands also eliminating wrong-algorithm cases (
HA
). These observations confirm that residual errors originate from semantic misunderstanding—either of the prompt (HC) or of the algorithmic requirements (HA). Random hallucinations and syntactic slips are effectively eliminated by the verifier; addressing the remaining hard cases will require better specification clarity or interactive disambiguation.
Table 2
:
LiveCodeBench accuracy after removing successive error categories. The full table of results containing all combinations of error categories can be found in Appendix
D
.
Dropped set (remaining)
τ
0
%
\tau_{0\%}
τ
1
%
\tau_{1\%}
τ
2
%
\tau_{2\%}
Expected
Clustered
Max
Baseline (219)
15.07
16.44
31.05
33.97
49.32
66.67
Out of Scope (212)
15.57
25.47
36.79
35.09
50.94
68.87
O+HC (198)
27.27
39.39
39.90
37.21
54.55
71.21
O+HC+HA (181)
43.09
45.86
50.83
40.25
59.67
74.59
O+HC+HA+I+S (159)
67.30
67.30
67.30
44.53
67.30
78.62
O+HC+HA+I+S+TL (107)
100
100
100
64.20
100
100
5
Discussion
Functional clustering draws a sharp line between two error sources. Once candidate programs are grouped by exact I/O behaviour on an automatically generated test suite, random hallucinations nearly vanish. Almost every residual failure can now be traced to the model misreading, under-specifying, or over-constraining the natural-language prompt. Diversity among base models helps further: the few hard mistakes that remain generally occur when one LLM concentrates its probability mass on a single flawed interpretation, whereas an ensemble tends to disagree and thus abstains.
Specification refinements are an immediate lever. Rewriting a handful of ambiguous
HumanEval
tasks boosts both confidence and accuracy, echoing the way human programmers pose follow-up questions when requirements are vague. A natural next step is to let LLMs propose such clarifications automatically, or to iteratively rewrite the prompt until confidence stabilizes.
Time-limit exceedance dominates the harder
LiveCodeBench
tasks. Because functional clustering already verifies behavioral equivalence, we can safely ask the model for optimized variants and accept them only if they match the reference on the full test suite and finish within budget, automating a significant slice of performance tuning.
Limitations
The approach rests on two core assumptions: each task admits a single functionally correct equivalence class, and behavioral agreement on a finite, auto-generated test set is a faithful proxy for universal correctness. Tasks with multiple valid outputs or hidden edge cases violate these assumptions; the verifier therefore fails on such inputs, and future work should investigate coverage-guided or property-based testing.
Reliability depends on the number of sampled programs
n
n
, the number of test inputs
m
m
, and the acceptance threshold
τ
\tau
. Smaller
n
n
or
m
m
, or highly peaked sampling, weakens the Chernoff-style guarantees, whereas larger values raise wall time and cost roughly as
𝒪
⁡
(
n
​
m
)
\mathcal{O}(nm)
. Parallelization, caching, and distilled student models help but do not remove the overhead.
Experiments are limited to Python problems from
HumanEval
and
LiveCodeBench
using two English-language LLMs. Extending to other programming languages will require language-specific sandboxes, new input generators, and fresh validation. Even with sandboxing, sophisticated escape or resource-exhaustion attacks remain possible and must be mitigated with stricter isolation. Because abstentions may correlate with under-represented domains, downstream systems should monitor for disparate coverage and adjust thresholds or training data accordingly.
6
Conclusion
We introduced
functional clustering
, a lightweight wrapper that turns any black-box code LLM into a selective coder with rigorously bounded error. The method samples multiple candidate programs, groups them by exact I/O behavior on an automatically generated test suite, and interprets the empirical mass of the dominant equivalence class as a confidence score. A single scalar threshold allows users to trade coverage for reliability: raising the threshold shrinks the fraction of tasks answered but drives the residual error rate exponentially toward zero, in line with our Chernoff-style analysis.
On
LiveCodeBench
, the wrapper preserves baseline pass@1 on solvable tasks yet cuts the error rate of returned answers from roughly 65% to under 2%. At a more conservative threshold the error rate falls to 0% while still solving 15.6% of benchmark problems. Manual audits reveal that the remaining failures stem from prompt misinterpretation rather than random hallucination, narrowing future work to specification clarity and cross-model consensus.
Unlike prior methods that rely on token-level likelihoods, embedding distances, or privileged logits, functional clustering requires only two black-box capabilities—generating code and running it—making it immediately applicable to closed APIs and future models. Because the same test-oracle infrastructure can validate optimized rewrites, incremental debugging, or ensemble voting, we view functional clustering as a modular building block for dependable, autonomous software pipelines.
References
[1]
Anthropic.
The claude 3 model family: Opus, sonnet, haiku, March 2024.
URL
https://www.anthropic.com/news/claude-3-family
.
[2]
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
Evaluating large language models trained on code, 2021.
URL
https://arxiv.org/abs/2107.03374
.
[3]
Shrey Desai and Greg Durrett.
Calibration of pre-trained transformers.
In Bonnie Webber, Trevor Cohn, Yulan He, and Yang Liu, editors,
Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)
, pages 295–302, Online, November 2020. Association for Computational Linguistics.
doi:
10.18653/v1/2020.emnlp-main.21
.
URL
https://aclanthology.org/2020.emnlp-main.21/
.
[4]
Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and Yarin Gal.
Detecting hallucinations in large language models using semantic entropy.
Nature
, 630(8017):625–630, June 2024.
ISSN 1476-4687.
doi:
10.1038/s41586-024-07421-0
.
URL
https://doi.org/10.1038/s41586-024-07421-0
.
[5]
Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting Liu.
A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions.
ACM Transactions on Information Systems
, November 2024.
ISSN 1558-2868.
doi:
10.1145/3703155
.
URL
http://dx.doi.org/10.1145/3703155
.
[6]
Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
Livecodebench: Holistic and contamination free evaluation of large language models for code, 2024.
URL
https://arxiv.org/abs/2403.07974
.
[7]
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, Scott Johnston, Sheer El-Showk, Andy Jones, Nelson Elhage, Tristan Hume, Anna Chen, Yuntao Bai, Sam Bowman, Stanislav Fort, Deep Ganguli, Danny Hernandez, Josh Jacobson, Jackson Kernion, Shauna Kravec, Liane Lovitt, Kamal Ndousse, Catherine Olsson, Sam Ringer, Dario Amodei, Tom Brown, Jack Clark, Nicholas Joseph, Ben Mann, Sam McCandlish, Chris Olah, and Jared Kaplan.
Language models (mostly) know what they know, 2022.
URL
https://arxiv.org/abs/2207.05221
.
[8]
Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar.
Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation.
In
International Conference on Learning Representations (ICLR)
, 2023.
URL
https://openreview.net/forum?id=VD-AYtP0dve
.
[9]
Stephanie Lin, Jacob Hilton, and Owain Evans.
Teaching models to express their uncertainty in words.
Transactions on Machine Learning Research
, 2022.
Available at
https://openreview.net/forum?id=8s8K2UZGTZ
.
[10]
Fang Liu, Yang Liu, Lin Shi, Houkun Huang, Ruifeng Wang, Zhen Yang, Li Zhang, Zhongqi Li, and Yuchi Ma.
Exploring and evaluating hallucinations in llm-powered code generation, 2024a.
URL
https://arxiv.org/abs/2404.00971
.
[11]
Xin Liu, Muhammad Khalifa, and Lu Wang.
Litcab: Lightweight language model calibration over short and long-form responses.
In
International Conference on Learning Representations (ICLR)
, 2024b.
URL
https://openreview.net/forum?id=jH67LHVOIO
.
[12]
Huan Ma, Jingdong Chen, Guangyu Wang, and Changqing Zhang.
Estimating llm uncertainty with logits, 2025.
URL
https://arxiv.org/abs/2502.00290
.
[13]
OpenAI.
Introducing gpt-4.1 in the api, April 2025.
URL
https://openai.com/index/gpt-4-1/
.
[14]
OpenAI, :, Aaron Hurst, Adam Lerer, Adam P. Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, Aleksander Mądry, Alex Baker-Whitcomb, Alex Beutel, Alex Borzunov, Alex Carney, Alex Chow, Alex Kirillov, Alex Nichol, Alex Paino, Alex Renzin, Alex Tachard Passos, Alexander Kirillov, Alexi Christakis, Alexis Conneau, Ali Kamali, Allan Jabri, Allison Moyer, Allison Tam, Amadou Crookes, Amin Tootoochian, Amin Tootoonchian, Ananya Kumar, Andrea Vallone, Andrej Karpathy, Andrew Braunstein, Andrew Cann, Andrew Codispoti, Andrew Galu, Andrew Kondrich, Andrew Tulloch, Andrey Mishchenko, Angela Baek, Angela Jiang, Antoine Pelisse, Antonia Woodford, Anuj Gosalia, Arka Dhar, Ashley Pantuliano, Avi Nayak, Avital Oliver, Barret Zoph, Behrooz Ghorbani, Ben Leimberger, Ben Rossen, Ben Sokolowsky, Ben Wang, Benjamin Zweig, Beth Hoover, Blake Samic, Bob McGrew, Bobby Spero, Bogo Giertler, Bowen Cheng, Brad Lightcap, Brandon Walkin, Brendan Quinn, Brian Guarraci, Brian Hsu,
Bright Kellogg, Brydon Eastman, Camillo Lugaresi, Carroll Wainwright, Cary Bassin, Cary Hudson, Casey Chu, Chad Nelson, Chak Li, Chan Jun Shern, Channing Conger, Charlotte Barette, Chelsea Voss, Chen Ding, Cheng Lu, Chong Zhang, Chris Beaumont, Chris Hallacy, Chris Koch, Christian Gibson, Christina Kim, Christine Choi, Christine McLeavey, Christopher Hesse, Claudia Fischer, Clemens Winter, Coley Czarnecki, Colin Jarvis, Colin Wei, Constantin Koumouzelis, Dane Sherburn, Daniel Kappler, Daniel Levin, Daniel Levy, David Carr, David Farhi, David Mely, David Robinson, David Sasaki, Denny Jin, Dev Valladares, Dimitris Tsipras, Doug Li, Duc Phong Nguyen, Duncan Findlay, Edede Oiwoh, Edmund Wong, Ehsan Asdar, Elizabeth Proehl, Elizabeth Yang, Eric Antonow, Eric Kramer, Eric Peterson, Eric Sigler, Eric Wallace, Eugene Brevdo, Evan Mays, Farzad Khorasani, Felipe Petroski Such, Filippo Raso, Francis Zhang, Fred von Lohmann, Freddie Sulit, Gabriel Goh, Gene Oden, Geoff Salmon, Giulio Starace, Greg Brockman, Hadi
Salman, Haiming Bao, Haitang Hu, Hannah Wong, Haoyu Wang, Heather Schmidt, Heather Whitney, Heewoo Jun, Hendrik Kirchner, Henrique Ponde de Oliveira Pinto, Hongyu Ren, Huiwen Chang, Hyung Won Chung, Ian Kivlichan, Ian O’Connell, Ian O’Connell, Ian Osband, Ian Silber, Ian Sohl, Ibrahim Okuyucu, Ikai Lan, Ilya Kostrikov, Ilya Sutskever, Ingmar Kanitscheider, Ishaan Gulrajani, Jacob Coxon, Jacob Menick, Jakub Pachocki, James Aung, James Betker, James Crooks, James Lennon, Jamie Kiros, Jan Leike, Jane Park, Jason Kwon, Jason Phang, Jason Teplitz, Jason Wei, Jason Wolfe, Jay Chen, Jeff Harris, Jenia Varavva, Jessica Gan Lee, Jessica Shieh, Ji Lin, Jiahui Yu, Jiayi Weng, Jie Tang, Jieqi Yu, Joanne Jang, Joaquin Quinonero Candela, Joe Beutler, Joe Landers, Joel Parish, Johannes Heidecke, John Schulman, Jonathan Lachman, Jonathan McKay, Jonathan Uesato, Jonathan Ward, Jong Wook Kim, Joost Huizinga, Jordan Sitkin, Jos Kraaijeveld, Josh Gross, Josh Kaplan, Josh Snyder, Joshua Achiam, Joy Jiao, Joyce Lee, Juntang
Zhuang, Justyn Harriman, Kai Fricke, Kai Hayashi, Karan Singhal, Katy Shi, Kavin Karthik, Kayla Wood, Kendra Rimbach, Kenny Hsu, Kenny Nguyen, Keren Gu-Lemberg, Kevin Button, Kevin Liu, Kiel Howe, Krithika Muthukumar, Kyle Luther, Lama Ahmad, Larry Kai, Lauren Itow, Lauren Workman, Leher Pathak, Leo Chen, Li Jing, Lia Guy, Liam Fedus, Liang Zhou, Lien Mamitsuka, Lilian Weng, Lindsay McCallum, Lindsey Held, Long Ouyang, Louis Feuvrier, Lu Zhang, Lukas Kondraciuk, Lukasz Kaiser, Luke Hewitt, Luke Metz, Lyric Doshi, Mada Aflak, Maddie Simens, Madelaine Boyd, Madeleine Thompson, Marat Dukhan, Mark Chen, Mark Gray, Mark Hudnall, Marvin Zhang, Marwan Aljubeh, Mateusz Litwin, Matthew Zeng, Max Johnson, Maya Shetty, Mayank Gupta, Meghan Shah, Mehmet Yatbaz, Meng Jia Yang, Mengchao Zhong, Mia Glaese, Mianna Chen, Michael Janner, Michael Lampe, Michael Petrov, Michael Wu, Michele Wang, Michelle Fradin, Michelle Pokrass, Miguel Castro, Miguel Oom Temudo de Castro, Mikhail Pavlov, Miles Brundage, Miles Wang, Minal
Khan, Mira Murati, Mo Bavarian, Molly Lin, Murat Yesildal, Nacho Soto, Natalia Gimelshein, Natalie Cone, Natalie Staudacher, Natalie Summers, Natan LaFontaine, Neil Chowdhury, Nick Ryder, Nick Stathas, Nick Turley, Nik Tezak, Niko Felix, Nithanth Kudige, Nitish Keskar, Noah Deutsch, Noel Bundick, Nora Puckett, Ofir Nachum, Ola Okelola, Oleg Boiko, Oleg Murk, Oliver Jaffe, Olivia Watkins, Olivier Godement, Owen Campbell-Moore, Patrick Chao, Paul McMillan, Pavel Belov, Peng Su, Peter Bak, Peter Bakkum, Peter Deng, Peter Dolan, Peter Hoeschele, Peter Welinder, Phil Tillet, Philip Pronin, Philippe Tillet, Prafulla Dhariwal, Qiming Yuan, Rachel Dias, Rachel Lim, Rahul Arora, Rajan Troll, Randall Lin, Rapha Gontijo Lopes, Raul Puri, Reah Miyara, Reimar Leike, Renaud Gaubert, Reza Zamani, Ricky Wang, Rob Donnelly, Rob Honsby, Rocky Smith, Rohan Sahai, Rohit Ramchandani, Romain Huet, Rory Carmichael, Rowan Zellers, Roy Chen, Ruby Chen, Ruslan Nigmatullin, Ryan Cheu, Saachi Jain, Sam Altman, Sam Schoenholz, Sam
Toizer, Samuel Miserendino, Sandhini Agarwal, Sara Culver, Scott Ethersmith, Scott Gray, Sean Grove, Sean Metzger, Shamez Hermani, Shantanu Jain, Shengjia Zhao, Sherwin Wu, Shino Jomoto, Shirong Wu, Shuaiqi, Xia, Sonia Phene, Spencer Papay, Srinivas Narayanan, Steve Coffey, Steve Lee, Stewart Hall, Suchir Balaji, Tal Broda, Tal Stramer, Tao Xu, Tarun Gogineni, Taya Christianson, Ted Sanders, Tejal Patwardhan, Thomas Cunninghman, Thomas Degry, Thomas Dimson, Thomas Raoux, Thomas Shadwell, Tianhao Zheng, Todd Underwood, Todor Markov, Toki Sherbakov, Tom Rubin, Tom Stasi, Tomer Kaftan, Tristan Heywood, Troy Peterson, Tyce Walters, Tyna Eloundou, Valerie Qi, Veit Moeller, Vinnie Monaco, Vishal Kuo, Vlad Fomenko, Wayne Chang, Weiyi Zheng, Wenda Zhou, Wesam Manassra, Will Sheu, Wojciech Zaremba, Yash Patil, Yilei Qian, Yongjik Kim, Youlong Cheng, Yu Zhang, Yuchen He, Yuchen Zhang, Yujia Jin, Yunxing Dai, and Yury Malkov.
Gpt-4o system card, 2024.
URL
https://arxiv.org/abs/2410.21276
.
[15]
OpenAI, :, Ahmed El-Kishky, Alexander Wei, Andre Saraiva, Borys Minaiev, Daniel Selsam, David Dohan, Francis Song, Hunter Lightman, Ignasi Clavera, Jakub Pachocki, Jerry Tworek, Lorenz Kuhn, Lukasz Kaiser, Mark Chen, Max Schwarzer, Mostafa Rohaninejad, Nat McAleese, o3 contributors, Oleg Mürk, Rhythm Garg, Rui Shu, Szymon Sidor, Vineet Kosaraju, and Wenda Zhou.
Competitive programming with large reasoning models, 2025.
URL
https://arxiv.org/abs/2502.06807
.
[16]
Xin Qiu and Risto Miikkulainen.
Semantic density: Uncertainty quantification for large language models through confidence measurement in semantic space, 2024.
URL
https://arxiv.org/abs/2405.13845
.
[17]
Arindam Sharma and Cristina David.
Assessing correctness in llm-based code generation via uncertainty estimation, 2025.
URL
https://arxiv.org/abs/2502.11620
.
[18]
Wei Tao, Yucheng Zhou, Yanlin Wang, Wenqiang Zhang, Hongyu Zhang, and Yu Cheng.
Magis: Llm-based multi-agent framework for github issue resolution.
In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors,
Advances in Neural Information Processing Systems
, volume 37, pages 51963–51993. Curran Associates, Inc., 2024.
URL
https://proceedings.neurips.cc/paper_files/paper/2024/file/5d1f02132ef51602adf07000ca5b6138-Paper-Conference.pdf
.
[19]
Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, and Christopher D. Manning.
Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models finetuned with human feedback.
In
Proceedings of EMNLP 2023
, Singapore, 2023. Association for Computational Linguistics.
doi:
10.18653/v1/2023.emnlp-main.330
.
URL
https://aclanthology.org/2023.emnlp-main.330
.
[20]
Yuchen Tian, Weixiang Yan, Qian Yang, Xuandong Zhao, Qian Chen, Wen Wang, Ziyang Luo, Lei Ma, and Dawn Song.
Codehalu: Investigating code hallucinations in llms via execution-based verification, 2024.
URL
https://arxiv.org/abs/2405.00253
.
[21]
S. M Towhidul Islam Tonmoy, S M Mehedi Zaman, Vinija Jain, Anku Rani, Vipula Rawte, Aman Chadha, and Amitava Das.
A comprehensive survey of hallucination mitigation techniques in large language models, 2024.
URL
https://arxiv.org/abs/2401.01313
.
[22]
Arya VarastehNezhad, Reza Tavasoli, Mostafa Masumi, and Fattaneh Taghiyareh.
Llm performance assessment in computer science graduate entrance exams.
In
2024 11th International Symposium on Telecommunications (IST)
, pages 232–237, 2024.
doi:
10.1109/IST64061.2024.10843484
.
[23]
Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan Hooi.
Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms, 2024.
URL
https://arxiv.org/abs/2306.13063
.
[24]
Yasin Abbasi Yadkori, Ilja Kuzborskij, David Stutz, András György, Adam Fisch, Arnaud Doucet, Iuliya Beloshapka, Wei-Hung Weng, Yao-Yuan Yang, Csaba Szepesvári, Ali Taylan Cemgil, and Nenad Tomasev.
Mitigating llm hallucinations via conformal abstention, 2024.
URL
https://arxiv.org/abs/2405.01563
.
[25]
Fanghua Ye, Yang MingMing, Jianhui Pang, Longyue Wang, Derek F. Wong, Emine Yilmaz, Shuming Shi, and Zhaopeng Tu.
Benchmarking llms via uncertainty quantification, 2024.
URL
https://arxiv.org/abs/2401.12794
.
[26]
Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen.
A survey of large language models, 2025.
URL
https://arxiv.org/abs/2303.18223
.
Appendix A
Proof of Equation
5
Theorem 1
(Chernoff–style upper bound)
.
Let
X
1
,
…
,
X
n
∼
i.i.d.
Bernoulli
⁡
(
C
)
X_{1},\dots,X_{n}\stackrel{{\scriptstyle\text{i.i.d.}}}{{\sim}}\mathrm{Bernoulli}(C)
with
C
∈
(
0
,
1
)
C\in(0,1)
, and let
C
^
n
=
1
n
​
∑
i
=
1
n
X
i
\hat{C}_{n}=\frac{1}{n}\sum_{i=1}^{n}X_{i}
.
For any threshold
τ
∈
(
C
,
1
)
\tau\in(C,1)
,
Pr
[
C
^
n
≥
τ
]
≤
exp
[
−
n
D
KL
(
τ
∥
C
)
]
,
\Pr\!\bigl[\hat{C}_{n}\geq\tau\bigr]\;\;\leq\;\;\exp\!\bigl[-n\,D_{\mathrm{KL}}(\tau\;\|\;C)\bigr],
where
D
KL
(
τ
∥
C
)
=
τ
ln
τ
C
+
(
1
−
τ
)
ln
1
−
τ
1
−
C
D_{\mathrm{KL}}(\tau\;\|\;C)=\tau\ln\!\frac{\tau}{C}+(1-\tau)\ln\!\frac{1-\tau}{1-C}
is the binary
Kullback–Leibler divergence.
Proof.
Write
S
n
=
∑
i
=
1
n
X
i
=
n
​
C
^
n
S_{n}=\sum_{i=1}^{n}X_{i}=n\hat{C}_{n}
.
For any
λ
>
0
\lambda>0
, Markov’s inequality gives
Pr
[
S
n
≥
n
τ
]
\displaystyle\Pr[S_{n}\geq n\tau]
=
Pr
[
e
λ
​
S
n
≥
e
λ
​
n
​
τ
]
≤
e
−
λ
​
n
​
τ
𝔼
[
e
λ
​
S
n
]
.
\displaystyle\;=\;\Pr\!\bigl[e^{\lambda S_{n}}\geq e^{\lambda n\tau}\bigr]\;\leq\;e^{-\lambda n\tau}\,\mathbb{E}\!\bigl[e^{\lambda S_{n}}\bigr].
(8)
Because the
X
i
X_{i}
are independent, the moment–generating function factorizes:
𝔼
⁡
[
e
λ
​
S
n
]
=
∏
i
=
1
n
𝔼
⁡
[
e
λ
​
X
i
]
=
(
(
1
−
C
)
+
C
​
e
λ
)
n
.
\mathbb{E}\!\bigl[e^{\lambda S_{n}}\bigr]=\prod_{i=1}^{n}\mathbb{E}[e^{\lambda X_{i}}]=\bigl((1-C)+C\,e^{\lambda}\bigr)^{n}.
Substituting into (
8
) and taking logarithms,
1
n
ln
Pr
[
S
n
≥
n
τ
]
≤
−
λ
τ
+
ln
(
(
1
−
C
)
+
C
e
λ
)
.
\frac{1}{n}\ln\Pr[S_{n}\geq n\tau]\;\leq\;-\lambda\tau+\ln\!\bigl((1-C)+C\,e^{\lambda}\bigr).
The tightest bound arises by minimizing the right-hand side over
λ
>
0
\lambda>0
.
Denote
g
⁡
(
λ
)
=
−
λ
​
τ
+
ln
⁡
(
(
1
−
C
)
+
C
​
e
λ
)
.
g(\lambda)=-\lambda\tau+\ln\!\bigl((1-C)+C\,e^{\lambda}\bigr).
Setting
g
′
​
(
λ
)
=
0
g^{\prime}(\lambda)=0
yields
−
τ
+
C
​
e
λ
⋆
(
1
−
C
)
+
C
​
e
λ
⋆
=
0
⟹
e
λ
⋆
=
τ
⁡
(
1
−
C
)
C
⁡
(
1
−
τ
)
.
-\tau+\frac{C\,e^{\lambda_{\star}}}{(1-C)+C\,e^{\lambda_{\star}}}=0\;\;\Longrightarrow\;\;e^{\lambda_{\star}}=\frac{\tau(1-C)}{C(1-\tau)}.
Plugging
λ
⋆
\lambda_{\star}
back into
g
⁡
(
λ
)
g(\lambda)
gives
min
λ
>
0
g
(
λ
)
=
−
τ
ln
τ
⁡
(
1
−
C
)
C
⁡
(
1
−
τ
)
+
ln
(
1
−
τ
1
−
C
+
τ
1
−
C
)
=
−
D
KL
(
τ
∥
C
)
.
\min_{\lambda>0}g(\lambda)=-\tau\ln\!\frac{\tau(1-C)}{C(1-\tau)}+\ln\!\Bigl(\frac{1-\tau}{1-C}+\frac{\tau}{1-C}\Bigr)=-D_{\mathrm{KL}}(\tau\;\|\;C).
Exponentiating both sides and multiplying by
n
n
recovers
Pr
[
S
n
≥
n
τ
]
≤
exp
[
−
n
D
KL
(
τ
∥
C
)
]
,
\Pr[S_{n}\geq n\tau]\leq\exp[-n\,D_{\mathrm{KL}}(\tau\;\|\;C)],
which is exactly Eq.
5
.
∎
Appendix B
LLM prompts
When generating function completions, we require the response to be in a specific format. For each model the format is slightly different, so we use the system prompt to describe the format of the response to the model. The following is the system prompt for function completions for GPT-4o:
⬇
You
are
an
expert
Python
programmer
and
coding
assistant
.
Your
task
is
to
solve
the
given
problem
in
Python
,
providing
both
a
detailed
explanation
of
your
reasoning
and
the
code
.
Think
through
the
problem
step
by
step
,
considering
any
edge
cases
and
ensuring
the
code
meets
the
requirements
.
If
the
problem
contains
any
examples
,
simulate
running
those
examples
against
your
code
to
verify
whether
your
reasoning
about
the
problem
is
correct
.
Make
sure
to
not
have
any
misunderstandings
about
the
problem
.
The following is the system prompt for Claude-3-Haiku:
⬇
You
are
an
expert
Python
programmer
and
coding
assistant
.
Your
goal
is
to
generate
a
response
**
strictly
**
in
JSON
format
with
exactly
two
top
-
level
fields
:
"explanation"
and
"code"
.
Both
fields
must
be
valid
JSON
strings
that
include
all
necessary
escape
characters
.
-
The
"explanation"
field
should
provide
a
detailed
,
step
-
by
-
step
reasoning
of
how
you
derived
your
solution
.
-
The
"code"
field
must
contain
**
only
**
valid
Python
code
that
can
be
copied
and
run
directly
in
a
Python
file
without
modifications
or
additional
text
.
-
Do
not
include
any
fields
other
than
"explanation"
and
"code"
.
-
Do
not
include
any
text
before
or
after
the
JSON
object
.
-
Do
not
include
markdown
formatting
(
like
triple
backticks
).
Your
output
should
look
like
:
{
"explanation"
:
"..."
,
"code"
:
"..."
}
And
nothing
else
.
Follow
these
instructions
carefully
to
ensure
the
output
is
in
the
correct
format
.
Additionally, we have prompts for each dataset.
HumanEval
and
LiveCodeBench
provide their tasks in different formats. For
HumanEval
, the task is provided as a docstring for a function that the model is expected to complete. For
LiveCodeBench
, the task is provided as a text description scraped from a competitive programming website. So, in the user prompt, we describe the task and provide the input and output formats that the model should follow. The following is the user prompt for
HumanEval
:
⬇
Complete
the
function
’{entry_point}’
in
the
following
code
snippet
.
Provide
a
detailed
explanation
of
your
reasoning
in
the
’explanation’
field
,
and
the
complete
code
in
the
’code’
field
.
Think
carefully
about
the
problem
,
considering
edge
cases
and
the
best
approach
to
implement
the
function
.
If
the
code
snippet
contains
any
examples
,
think
through
those
examples
to
verify
whether
your
reasoning
about
the
problem
is
correct
.
Use
those
examples
to
correct
any
misunderstandings
you
may
have
about
the
problem
.
Do
not
add
new
imports
or
define
any
new
functions
that
were
not
included
in
the
provided
snippet
.
Output
your
response
as
a
JSON
object
with
fields
’explanation’
and
’code’
.
‘‘‘{
function_docstring
}‘‘‘
The following is the user prompt for
LiveCodeBench
:
⬇
Write
Python
code
to
solve
the
following
problem
.
Read
from
standard
input
and
output
to
standard
output
.
Provide
a
detailed
explanation
of
your
reasoning
in
the
’explanation’
field
,
and
the
complete
code
in
the
’code’
field
.
Think
carefully
about
the
problem
,
considering
edge
cases
and
the
best
approach
to
implement
the
function
.
If
the
provided
problem
contains
any
examples
,
think
through
those
examples
to
verify
whether
your
reasoning
about
the
problem
is
correct
.
Use
those
examples
to
correct
any
misunderstandings
you
may
have
about
the
problem
.
Output
your
response
as
a
JSON
object
with
fields
’explanation’
and
’code’
.
###
Problem
Statement:
{
question_content
}
We additionally prompt the LLM to generate test cases. In this case, we use a single LLM, GPT-4o. The following is the prompt used to generate test cases for
HumanEval
:
⬇
Generate
a
comprehensive
list
of
valid
input
test
cases
for
the
function
’{entry_point}’
in
the
following
code
.
The
test
cases
should
cover
all
possible
valid
scenarios
,
including
edge
cases
and
typical
use
cases
.
Provide
only
the
inputs
to
each
test
case
.
Each
set
of
inputs
should
be
a
string
that
can
be
parsed
with
json
.
loads
into
a
valid
dictionary
with
the
function
parameter
names
as
keys
:
‘‘‘{
function_docstring
}‘‘‘
The following is the prompt used to generate test cases for
LiveCodeBench
:
⬇
Generate
a
comprehensive
list
of
valid
input
test
cases
for
the
given
problem
statement
.
The
test
cases
should
cover
all
possible
valid
scenarios
,
including
edge
cases
and
typical
use
cases
.
Provide
only
the
inputs
to
each
test
case
.
Each
input
should
be
a
string
in
the
provided
test
format
that
will
be
passed
into
a
program
through
standard
input
.
###
Problem
Statement:
{
question_content
}
Appendix C
Problem rewrites
The following is a list of all rewritten problems from
HumanEval
. We attempt to make minimal rewrites that clarify a misunderstanding that the model has with the problem. After making these rewrites, the model is able to solve the problem correctly with high confidence.
HumanEval/145
⬇
#
original
snippet
def
order_by_points
(
nums
):
""
"
␣␣␣␣
Write
␣
a
␣
function
␣
which
␣
sorts
␣
the
␣
given
␣
list
␣
of
␣
integers
␣␣␣␣
in
␣
ascending
␣
order
␣
according
␣
to
␣
the
␣
sum
␣
of
␣
their
␣
digits.
␣␣␣␣
Note:
␣
if
␣
there
␣
are
␣
several
␣
items
␣
with
␣
similar
␣
sum
␣
of
␣
their
␣␣␣␣
digits,
␣
order
␣
them
␣
based
␣
on
␣
their
␣
index
␣
in
␣
original
␣
list.
␣␣␣␣
For
␣
example:
␣␣␣␣
>>>
␣
order_by_points([1,
␣
11,
␣
-1,
␣
-11,
␣
-12])
␣
==
␣
[-1,
␣
-11,
␣
1,
␣
-12,
␣
11]
␣␣␣␣
>>>
␣
order_by_points([])
␣
==
␣
[]
␣␣␣␣
"
""
#
clarified
version
def
order_by_points
(
nums
):
""
"
␣␣␣␣
Write
␣
a
␣
function
␣
which
␣
sorts
␣
the
␣
given
␣
list
␣
of
␣
integers
␣␣␣␣
in
␣
ascending
␣
order
␣
according
␣
to
␣
the
␣
sum
␣
of
␣
their
␣
digits.
␣␣␣␣
**If
␣
an
␣
integer
␣
is
␣
negative,
␣
its
␣
first
␣
digit
␣
should
␣
be
␣
treated
␣␣␣␣
as
␣
negative
␣
and
␣
the
␣
remaining
␣
digits
␣
as
␣
positive.**
␣␣␣␣
Note:
␣
if
␣
there
␣
are
␣
several
␣
items
␣
with
␣
similar
␣
sum
␣
of
␣
their
␣␣␣␣
digits,
␣
order
␣
them
␣
based
␣
on
␣
their
␣
index
␣
in
␣
original
␣
list.
␣␣␣␣
For
␣
example:
␣␣␣␣
>>>
␣
order_by_points([1,
␣
11,
␣
-1,
␣
-11,
␣
-12,
␣
-111])
␣
==
␣
[-1,
␣
-11,
␣
1,
␣
-12,
␣
-111,
␣
11]
␣␣␣␣
>>>
␣
order_by_points([])
␣
==
␣
[]
␣␣␣␣
"
""
HumanEval/127
⬇
#
original
snippet
def
intersection
(
interval1
,
interval2
):
""
"
␣␣␣␣
You
␣
are
␣
given
␣
two
␣
intervals,
␣
where
␣
each
␣
interval
␣
is
␣
a
␣
pair
␣
of
␣␣␣␣
integers.
␣
For
␣
example,
␣
interval
␣
=
␣
(start,
␣
end)
␣
=
␣
(1,
␣
2).
␣
The
␣␣␣␣
given
␣
intervals
␣
are
␣
closed
␣
which
␣
means
␣
that
␣
the
␣
interval
␣␣␣␣
(start,
␣
end)
␣
includes
␣
both
␣
start
␣
and
␣
end.
␣
For
␣
each
␣
given
␣␣␣␣
interval,
␣
it
␣
is
␣
assumed
␣
that
␣
its
␣
start
␣
is
␣
less
␣
or
␣
equal
␣
its
␣␣␣␣
end.
␣
Your
␣
task
␣
is
␣
to
␣
determine
␣
whether
␣
the
␣
length
␣
of
␣␣␣␣
intersection
␣
of
␣
these
␣
two
␣
intervals
␣
is
␣
a
␣
prime
␣
number.
␣␣␣␣
Example,
␣
the
␣
intersection
␣
of
␣
the
␣
intervals
␣
(1,
␣
3),
␣
(2,
␣
4)
␣
is
␣␣␣␣
(2,
␣
3)
␣
which
␣
its
␣
length
␣
is
␣
1,
␣
which
␣
not
␣
a
␣
prime
␣
number.
␣
If
␣␣␣␣
the
␣
length
␣
of
␣
the
␣
intersection
␣
is
␣
a
␣
prime
␣
number,
␣
return
␣␣␣␣
"
YES
",
␣
otherwise,
␣
return
␣
"
NO
".
␣
If
␣
the
␣
two
␣
intervals
␣
don’t
␣␣␣␣
intersect,
␣
return
␣
"
NO
".
␣␣␣␣
[input/output]
␣
samples:
␣␣␣␣
intersection((1,
␣
2),
␣
(2,
␣
3))
␣
==>
␣
"
NO
"
␣␣␣␣
intersection((-1,
␣
1),
␣
(0,
␣
4))
␣
==>
␣
"
NO
"
␣␣␣␣
intersection((-3,
␣
-1),
␣
(-5,
␣
5))
␣
==>
␣
"
YES
"
␣␣␣␣
"
""
#
clarified
version
def
intersection
(
interval1
,
interval2
):
""
"
␣␣␣␣
You
␣
are
␣
given
␣
two
␣
intervals,
␣
where
␣
each
␣
interval
␣
is
␣
a
␣
pair
␣
of
␣␣␣␣
integers.
␣
For
␣
example,
␣
interval
␣
=
␣
(start,
␣
end)
␣
=
␣
(1,
␣
2).
␣
The
␣␣␣␣
given
␣
intervals
␣
are
␣
closed
␣
which
␣
means
␣
that
␣
the
␣
interval
␣␣␣␣
(start,
␣
end)
␣
includes
␣
both
␣
start
␣
and
␣
end.
␣
For
␣
each
␣
given
␣␣␣␣
interval,
␣
it
␣
is
␣
assumed
␣
that
␣
its
␣
start
␣
is
␣
less
␣
or
␣
equal
␣
its
␣␣␣␣
end.
␣
**The
␣
length
␣
of
␣
an
␣
interval
␣
(a,
␣
b)
␣
is
␣
defined
␣
as
␣
b
␣
-
␣
a.**
␣␣␣␣
Your
␣
task
␣
is
␣
to
␣
determine
␣
whether
␣
the
␣
length
␣
of
␣␣␣␣
intersection
␣
of
␣
these
␣
two
␣
intervals
␣
is
␣
a
␣
prime
␣
number.
␣␣␣␣
Example:
␣
the
␣
intersection
␣
of
␣
the
␣
intervals
␣
(1,
␣
3),
␣
(2,
␣
4)
␣
is
␣␣␣␣
(2,
␣
3),
␣
whose
␣
length
␣
is
␣
3
␣
-
␣
2
␣
=
␣
1,
␣
which
␣
is
␣
not
␣
a
␣
prime
␣␣␣␣
number.
␣
If
␣
the
␣
length
␣
of
␣
the
␣
intersection
␣
is
␣
a
␣
prime
␣
number,
␣␣␣␣
return
␣
"
YES
",
␣
otherwise,
␣
return
␣
"
NO
".
␣
If
␣
the
␣
two
␣
intervals
␣␣␣␣
don’t
␣
intersect,
␣
return
␣
"
NO
".
␣␣␣␣
[input/output]
␣
samples:
␣␣␣␣
intersection((1,
␣
2),
␣
(2,
␣
3))
␣
==>
␣
"
NO
"
␣␣␣␣
intersection((-1,
␣
1),
␣
(0,
␣
4))
␣
==>
␣
"
NO
"
␣␣␣␣
intersection((-3,
␣
-1),
␣
(-5,
␣
5))
␣
==>
␣
"
YES
"
␣␣␣␣
"
""
HumanEval/134
⬇
#
original
snippet
def
check_if_last_char_is_a_letter
(
txt
):
""
"
␣␣␣␣
Create
␣
a
␣
function
␣
that
␣
returns
␣
True
␣
if
␣
the
␣
last
␣
character
␣␣␣␣
of
␣
a
␣
given
␣
string
␣
is
␣
an
␣
alphabetical
␣
character
␣
and
␣
is
␣
not
␣␣␣␣
a
␣
part
␣
of
␣
a
␣
word,
␣
and
␣
False
␣
otherwise.
␣␣␣␣
Note:
␣
"
word
"
␣
is
␣
a
␣
group
␣
of
␣
characters
␣
separated
␣
by
␣
space.
␣␣␣␣
Examples:
␣␣␣␣
check_if_last_char_is_a_letter("
apple
pie
")
␣
=>
␣
False
␣␣␣␣
check_if_last_char_is_a_letter("
apple
pi
e
")
␣
=>
␣
True
␣␣␣␣
check_if_last_char_is_a_letter("
apple
pi
e
")
␣
=>
␣
False
␣␣␣␣
check_if_last_char_is_a_letter("
")
␣
=>
␣
False
␣␣␣␣
"
""
#
clarified
version
def
check_if_last_char_is_a_letter
(
txt
):
""
"
␣␣␣␣
Create
␣
a
␣
function
␣
that
␣
returns
␣
True
␣
if
␣
the
␣
very
␣
last
␣
character
␣␣␣␣
of
␣
a
␣
given
␣
string
␣
is
␣
an
␣
alphabetical
␣
character
␣
and
␣
is
␣
not
␣␣␣␣
a
␣
part
␣
of
␣
a
␣
word,
␣
and
␣
False
␣
otherwise.
␣␣␣␣
Note:
␣
"
"word"
"
␣
is
␣
a
␣
group
␣
of
␣
characters
␣
separated
␣
by
␣
space.
␣␣␣␣
**Do
␣
not
␣
trim
␣
any
␣
trailing
␣
spaces.**
␣␣␣␣
Examples:
␣␣␣␣
check_if_last_char_is_a_letter("
apple
pie
")
␣
=>
␣
False
␣␣␣␣
check_if_last_char_is_a_letter("
apple
pi
e
")
␣
=>
␣
True
␣␣␣␣
check_if_last_char_is_a_letter("
apple
pi
e
")
␣
=>
␣
False
␣␣␣␣
check_if_last_char_is_a_letter("
")
␣
=>
␣
False
␣␣␣␣
"
""
HumanEval/160
⬇
#
original
snippet
def
do_algebra
(
operator
,
operand
):
""
"
␣␣␣␣
Given
␣
two
␣
lists
␣
operator,
␣
and
␣
operand.
␣
The
␣
first
␣
list
␣
has
␣␣␣␣
basic
␣
algebra
␣
operations,
␣
and
␣
the
␣
second
␣
list
␣
is
␣
a
␣
list
␣
of
␣␣␣␣
integers.
␣
Use
␣
the
␣
two
␣
given
␣
lists
␣
to
␣
build
␣
the
␣
algebric
␣␣␣␣
expression
␣
and
␣
return
␣
the
␣
evaluation
␣
of
␣
this
␣
expression.
␣␣␣␣
The
␣
basic
␣
algebra
␣
operations:
␣␣␣␣
Addition
␣
(
␣
+
␣
)
␣␣␣␣
Subtraction
␣
(
␣
-
␣
)
␣␣␣␣
Multiplication
␣
(
␣
*
␣
)
␣␣␣␣
Floor
␣
division
␣
(
␣
//
␣
)
␣␣␣␣
Exponentiation
␣
(
␣
**
␣
)
␣␣␣␣
Example:
␣␣␣␣
operator[’+’,
␣
’*’,
␣
’-’]
␣␣␣␣
array
␣
=
␣
[2,
␣
3,
␣
4,
␣
5]
␣␣␣␣
result
␣
=
␣
2
␣
+
␣
3
␣
*
␣
4
␣
-
␣
5
␣␣␣␣
=>
␣
result
␣
=
␣
9
␣␣␣␣
Note:
␣␣␣␣␣␣␣␣
The
␣
length
␣
of
␣
operator
␣
list
␣
is
␣
equal
␣
to
␣
the
␣
length
␣
of
␣␣␣␣␣␣␣␣
operand
␣
list
␣
minus
␣
one.
␣
Operand
␣
is
␣
a
␣
list
␣
of
␣
of
␣
non-
␣␣␣␣␣␣␣␣
negative
␣
integers.
␣
Operator
␣
list
␣
has
␣
at
␣
least
␣
one
␣␣␣␣␣␣␣␣
operator,
␣
and
␣
operand
␣
list
␣
has
␣
at
␣
least
␣
two
␣
operands.
␣␣␣␣
"
""
#
clarified
version
def
do_algebra
(
operator
,
operand
):
""
"
␣␣␣␣
Given
␣
two
␣
lists
␣
operator,
␣
and
␣
operand.
␣
The
␣
first
␣
list
␣
has
␣␣␣␣
basic
␣
algebra
␣
operations,
␣
and
␣
the
␣
second
␣
list
␣
is
␣
a
␣
list
␣
of
␣␣␣␣
integers.
␣
Use
␣
the
␣
two
␣
given
␣
lists
␣
to
␣
build
␣
the
␣
algebric
␣␣␣␣
expression
␣
and
␣
return
␣
the
␣
evaluation
␣
of
␣
this
␣
expression.
␣
**Do
␣␣␣␣
not
␣
just
␣
apply
␣
each
␣
of
␣
the
␣
operations
␣
in
␣
the
␣
order
␣
they
␣
are
␣␣␣␣
given,
␣
make
␣
sure
␣
to
␣
keep
␣
order
␣
of
␣
operations
␣
in
␣
mind.**
␣␣␣␣
The
␣
basic
␣
algebra
␣
operations:
␣␣␣␣
Addition
␣
(
␣
+
␣
)
␣␣␣␣
Subtraction
␣
(
␣
-
␣
)
␣␣␣␣
Multiplication
␣
(
␣
*
␣
)
␣␣␣␣
Floor
␣
division
␣
(
␣
//
␣
)
␣␣␣␣
Exponentiation
␣
(
␣
**
␣
)
␣␣␣␣
Example:
␣␣␣␣
operator[’+’,
␣
’*’,
␣
’-’]
␣␣␣␣
array
␣
=
␣
[2,
␣
3,
␣
4,
␣
5]
␣␣␣␣
result
␣
=
␣
2
␣
+
␣
3
␣
*
␣
4
␣
-
␣
5
␣␣␣␣
=>
␣
result
␣
=
␣
9
␣␣␣␣
Note:
␣␣␣␣␣␣␣␣
The
␣
length
␣
of
␣
operator
␣
list
␣
is
␣
equal
␣
to
␣
the
␣
length
␣
of
␣␣␣␣␣␣␣␣
operand
␣
list
␣
minus
␣
one.
␣
Operand
␣
is
␣
a
␣
list
␣
of
␣
of
␣
non-
␣␣␣␣␣␣␣␣
negative
␣
integers.
␣
Operator
␣
list
␣
has
␣
at
␣
least
␣
one
␣␣␣␣␣␣␣␣
operator,
␣
and
␣
operand
␣
list
␣
has
␣
at
␣
least
␣
two
␣
operands.
␣␣␣␣
"
""
Appendix D
Dropped problem sets
Table
A1
shows the full table of accuracies. Out of scope (O) and Time limit exceeded (TL) errors are treated separate as both are not error categories that our method is meant to deal with. The other four categories are simple mistakes (S), incomplete response (I), missing constraint (HC), and wrong algorithm (HA). For these categories, all combinations of the categories are shown to be removed.
Table A1
:
Full table of LiveCodeBench accuracies after removing successive error categories.
Dropped set (remaining)
τ
0
%
\tau_{0\%}
τ
1
%
\tau_{1\%}
τ
2
%
\tau_{2\%}
Expected
Clustered
Max
Baseline (219)
15.07
16.44
31.05
33.97
49.32
66.67
O (212)
15.57
25.47
36.79
35.09
50.94
68.87
O+S (202)
16.34
26.73
38.61
36.14
52.97
68.81
O+I (200)
16.50
27.00
39.00
36.86
54.00
71.50
O+HC (198)
27.27
39.39
39.90
37.21
54.55
71.21
O+HA (195)
16.92
18.46
40.00
37.72
55.38
71.79
O+I+S (190)
17.37
18.95
35.79
38.07
56.32
71.58
O+S+HC (188)
28.72
41.49
43.62
38.46
56.91
71.28
O+I+HC (186)
29.03
41.94
42.47
39.25
58.06
74.19
O+S+HA (185)
17.84
19.46
44.86
39.01
57.84
71.89
O+I+HA (183)
18.03
19.67
42.62
39.83
59.02
74.86
O+HC+HA (181)
43.09
45.86
50.83
40.25
59.67
74.59
O+I+S+HC (176)
30.68
44.32
46.59
40.70
60.80
74.43
O+I+S+HA (173)
19.08
20.81
50.29
41.33
61.85
75.14
O+S+HC+HA (171)
48.54
57.89
60.23
41.79
62.57
74.85
O+I+HC+HA (169)
46.15
53.25
55.62
42.71
63.91
78.11
O+I+S+HC+HA (159)
67.30
67.30
67.30
44.53
67.30
78.62
O+I+S+HC+HA+TL (107)
100
100
100
64.20
100
100