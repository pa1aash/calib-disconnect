---
title: Do Uncertainty Signals Help? A Systematic Study of Uncertainty-Aware Decoding
  with Rollback Mechanisms
id: do-uncertainty-signals-help-a-systematic-study-of-uncertainty-aware-decoding-wit
tags:
- code-llm-confidence-positioning-d82d00
- l3-routing
- cc-2
created: '2026-11-10T09:08:36.534271Z'
updated: '2026-11-10T09:09:48.337096Z'
source: https://arxiv.org/html/2608.14653
source_domain: arxiv.org
fetched_at: '2026-11-10T09:08:36.533871Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Uncertainty-aware rollback decoding (arXiv 2608.14653, FULL TEXT): eight
  token-level signals, seven code LLMs, five benchmarks, equal-budget restart comparison
  (1,536 tokens); gains up to 0.26 pass@1; ablation attributes main gain to feedback-guided
  rollback. No verbal or probe signal, no random or oracle routing. L3: NARROWS lightly.'
---

Do Uncertainty Signals Help? A Systematic Study of Uncertainty-Aware Decoding with Rollback Mechanisms
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2608.14653v1 [cs.LG] 31 Jul 2026
Do Uncertainty Signals Help?
A Systematic Study of Uncertainty-Aware Decoding with Rollback Mechanisms
Xianzong Wu
1
,
Xiaohong Li
1
,
Xinyang Liu
1
,
Junjie Wang
1
,
Qiang Hu
1
,
Yuejun Guo
2
,
Tianlin Li
3
Affiliation:
Affiliation:
1
Tianjin University, China
2
Luxembourg Institute of Science and Technology, Luxembourg
3
Beihang University, China
Abstract
Prediction uncertainty is a widely adopted metric for quantifying model confidence, with downstream applications spanning model explanation, data selection, and prediction rollback. Despite its demonstrated utility, the potential of uncertainty quantification to enhance code generation in large language models (LLMs) remains largely underexplored, raising a critical question:
to what extent can uncertainty serve as an effective signal for improving LLM-based code generation?
To answer this question, we study uncertainty-aware rollback decoding, an inference-time strategy that uses uncertainty signals to identify unreliable generation regions and roll back to earlier valid prefixes without retraining the model. We evaluate this framework on seven code LLMs, five code generation benchmarks, and eight token-level uncertainty signals under a unified decoding setup.
Our results show that the complete rollback framework improves over equal-budget restart across the evaluated benchmarks and model settings, with gains of up to 0.26 in pass@1 and 0.35 in AvgTestPassRate on functional code generation benchmarks, and an absolute improvement of up to 6.4% in Patch-Aligned Safe Rate on Dsec-Python.
Among the evaluated signals, information-theoretic measures such as token entropy and negative log-likelihood show the most favorable overall trend, frequently achieving the best or near-best results on standard benchmarks.
A component-controlled ablation further shows that feedback-guided rollback provides the main improvement, while uncertainty localization provides an additional gain when checking, budget, rollback, and branch decay are held fixed.
I
Introduction
Large language models (LLMs) have achieved strong performance on a wide range of code generation benchmarks, from function-level synthesis tasks to more realistic programming scenarios involving execution-based evaluation and complex instructions
[
1
,
2
,
3
,
4
]
. Despite this progress, code generation remains fundamentally fragile. Unlike natural language generation, code is governed by strict syntactic, semantic, and execution constraints, so a single early mistake can invalidate an entire program. Under standard left-to-right decoding, such errors are irreversibly incorporated into the generation prefix and may subsequently propagate through later statements, causing error accumulation and amplifying their downstream impact.
Prior work improves generated code through self-debugging, iterative refinement, execution guidance, and intermediate verification
[
5
,
6
,
7
,
8
,
9
]
. Rollback-based decoding further enables failures to be corrected before a complete program is produced
[
10
]
, while uncertainty estimation can identify unreliable generations
[
11
,
12
,
13
]
. However, post-generation repair acts only after errors have propagated, and uncertainty has mainly been studied as a final-answer reliability measure rather than a decoding-time control signal.
We therefore study whether uncertainty can guide rollback localization and regeneration. Our unified framework incrementally generates and checks code, rolls back after detected failures, and uses uncertainty to identify unreliable regions. We compare information-theoretic and sampling-based signals across multiple benchmarks and model scales under a fixed rollback mechanism.
Our study is organized around three research questions:
•
RQ1: Does the complete rollback framework improve over equal-budget restart across datasets and models?
We answer this question by comparing the full framework with equal-budget restart on multiple benchmarks and model families. This comparison evaluates the complete framework rather than isolating uncertainty.
•
RQ2: What are the individual contributions of rollback, uncertainty, and branch decay?
Here, rollback denotes reverting to an earlier generation prefix after detecting failure, uncertainty denotes model-based signals for locating unreliable generation steps, and branch decay denotes a mechanism for reducing repeated exploration of unpromising branches. We answer this question through ablation experiments, rollback-localization diagnostics, and same-budget comparisons that isolate the effect of uncertainty-guided localization from additional generation budget.
•
RQ3: How does uncertainty behave across rollback-triggering error types?
We answer this question by analyzing the distribution of uncertainty scores across different categories of rollback-triggering errors.
Our results show that the complete rollback framework improves over equal-budget restart across the evaluated settings. The matched component ablation attributes the main improvement to feedback-guided rollback and an additional gain to uncertainty localization. Across the evaluated settings, information-theoretic signals generally provide more stable benefits than sampling-based alternatives.
In summary, this paper makes the following contributions:
•
We formulate uncertainty-aware rollback decoding as a decoding-time strategy for mitigating error accumulation in LLM-based code generation.
•
We provide a controlled empirical comparison of information-theoretic and sampling-based uncertainty signals within a unified rollback framework.
•
We present a multi-benchmark, multi-model evaluation of the complete rollback framework, together with a component-controlled uncertainty ablation and diagnostics of rollback localization, token cost, and same-budget alternatives.
II
Problem Statement
We formalize code generation as an autoregressive decoding process conditioned on a problem specification.
Given an input prompt
x
x
(e.g., a function signature together with a natural-language description),
a pretrained language model generates an output token sequence
𝐲
1
:
T
=
(
y
1
,
…
,
y
T
)
\mathbf{y}_{1:T}=(y_{1},\ldots,y_{T})
of length
T
T
,
where
y
t
y_{t}
denotes the token at position
t
t
.
We use
𝐲
<
t
=
𝐲
1
:
t
−
1
\mathbf{y}_{<t}=\mathbf{y}_{1:t-1}
to denote the generated prefix before step
t
t
.
The conditional distribution over the full sequence is factorized as
p
(
𝐲
1
:
T
∣
x
)
=
∏
t
=
1
T
p
(
y
t
∣
x
,
𝐲
<
t
)
.
p(\mathbf{y}_{1:T}\mid x)=\prod_{t=1}^{T}p(y_{t}\mid x,\mathbf{y}_{<t}).
Standard left-to-right decoding cannot revise an erroneous prefix, so early code mistakes can propagate into later statements and execution failures
[
8
,
10
,
14
,
1
]
. This is especially problematic for code, where one decision can make the remaining program syntactically invalid, semantically inconsistent, or non-executable.
Rollback-based decoding permits revision after a detected failure. Execution-based feedback has been used to assess generated code and guide inference-time revision or selection
[
7
,
8
,
10
,
15
,
16
,
17
,
18
]
. In our framework, execution feedback determines
whether
to reconsider the current prefix, while uncertainty refines
where
rollback should occur
[
11
,
12
]
.
Let
r
<
t
r<t
denote a rollback position.
When the current partial program corresponding to prefix
𝐲
1
:
t
\mathbf{y}_{1:t}
fails an execution check or a test case,
the generated sequence is truncated back to the earlier prefix
𝐲
<
r
=
𝐲
1
:
r
−
1
\mathbf{y}_{<r}=\mathbf{y}_{1:r-1}
,
and decoding resumes from position
r
r
.
This changes generation from a strictly forward process into a search with selective revision. The key subproblem is selecting
r
r
: without a principled criterion, rollback remains a heuristic operation. We study uncertainty signals derived from the predictive distribution as a basis for this selection
[
11
,
12
,
13
]
.
During decoding, each generated token
y
t
y_{t}
is associated with an uncertainty score
u
t
u_{t}
, computed from the predictive distribution
p
(
⋅
∣
x
,
𝐲
<
t
)
p(\cdot\mid x,\mathbf{y}_{<t})
, for example using token entropy or negative log-likelihood.
Tokens with high uncertainty indicate positions where the predictive distribution is diffuse, suggesting lower confidence and a higher likelihood of erroneous generation.
The central question is not only whether rollback helps, but whether uncertainty can indicate where rollback should occur. We therefore keep the rollback mechanism fixed while varying the uncertainty signal, enabling a controlled assessment against standard decoding and uncertainty-agnostic rollback.
III
Uncertainty Signals
Since rollback operates online, its uncertainty estimator must be efficiently computable and localized. We distinguish:
single-pass token-level signals
, which can be computed from a single forward pass at each decoding step, and
multi-pass signals
, which require repeated forward passes to estimate predictive uncertainty more robustly.
This follows the standard separation between measures from one predictive distribution and those estimated through stochastic inference or committee-style disagreement
[
19
,
20
,
21
]
.
III-A
Single-Pass Token-Level Signals
Single-pass token-level signals are computed directly from
p
(
⋅
∣
x
,
y
<
t
)
p(\cdot\mid x,y_{<t})
without additional stochastic sampling.
We evaluate six such signals:
•
Average Negative Log-Likelihood (Avg NLL)
: the average surprisal of generated tokens
[
22
]
.
•
Max Token Entropy
: the maximum token-level entropy within the current statement or span
[
22
,
19
]
.
•
Max Probability
: token confidence is converted to uncertainty as
1
−
max
v
⁡
p
⁡
(
v
∣
x
,
y
<
t
)
1-\max_{v}p(v\mid x,y_{<t})
, and the maximum converted score within the statement is used
[
23
,
19
]
.
•
Least Confidence
: the same token-level conversion,
1
−
max
v
⁡
p
⁡
(
v
∣
x
,
y
<
t
)
1-\max_{v}p(v\mid x,y_{<t})
, is averaged over the statement. Thus, the two confidence measures share a common direction but differ in statement-level aggregation
[
23
,
19
]
.
•
Margin of Confidence
:
1
−
(
p
(
1
)
−
p
(
2
)
)
1-(p_{(1)}-p_{(2)})
, where
p
(
1
)
p_{(1)}
and
p
(
2
)
p_{(2)}
are the two largest token probabilities; statement scores use the mean
[
19
]
.
•
Gini Impurity
:
1
−
∑
v
p
​
(
v
∣
x
,
y
<
t
)
2
1-\sum_{v}p(v\mid x,y_{<t})^{2}
, capturing distributional dispersion
[
24
]
.
Avg NLL, Least Confidence, Margin of Confidence, and Gini Impurity use statement means; Max Token Entropy and converted Max Probability use statement maxima. Larger values consistently indicate higher uncertainty.
III-B
Multi-Pass Signals
Multi-pass signals require repeated stochastic forward passes. We consider two such signals:
•
Predictive Entropy
: the entropy of the mean predictive distribution across stochastic samples
[
20
,
25
]
.
•
Variation Ratio
:
1
−
f
/
N
1-f/N
, where
f
f
is the modal-token frequency over
N
N
samples
[
21
,
25
]
.
These signals require repeated stochastic inference and therefore cost more than single-pass signals
[
20
]
.
III-C
Usage in Rollback Decoding
Uncertainty complements rather than replaces execution feedback. Execution checks indicate
whether
a generated prefix is problematic, while uncertainty helps locate
where
to roll back. For single-pass signals, token scores are aggregated over the current statement span: Avg NLL uses mean token surprisal, Max Token Entropy uses maximum token entropy, and confidence-style signals are oriented so that larger values indicate lower confidence before statement-level ranking.
For multi-pass signals, token scores are computed from multiple stochastic forward passes and averaged within each statement before rollback is triggered
[
20
,
25
]
.
Table
I
summarizes the uncertainty signals evaluated in this work and their grouping by computation type.
TABLE I:
Uncertainty signals considered in this work.
Computation Type
Signals
Single-pass token-level
Avg NLL, Max Token Entropy,
Max Probability, Least Confidence,
Margin of Confidence, Gini Impurity
Multi-pass sampling-based
Predictive Entropy, Variation Ratio
All signals are integrated into the same rollback framework, so decoding, checking, and rollback conditions remain identical across estimators. Our goal is not to propose a new estimator, but to compare which signals best support rollback-based correction. We emphasize single-pass signals for online use, while multi-pass estimators serve as higher-cost references
[
20
,
19
]
.
Fig. 1:
Overview of the study design. The task setup combines programming prompts, visible public tests, seven code LLMs, and eight uncertainty signals. During decoding, successful chunks extend the accepted prefix, whereas failed checks trigger feedback- or uncertainty-guided rollback, branch decay, prefix restoration, and regeneration. The evaluation addresses overall effectiveness, component contributions, and uncertainty across rollback-triggering error types.
IV
Uncertainty-Aware Decoding Framework
Figure
1
illustrates the overall workflow of our framework.
Building on rollback-based code decoding
[
10
]
, we instantiate a unified backbone that alternates incremental generation, lightweight checking, and rollback-based revision, while varying only the uncertainty signal. Given a task prompt and public tests, the decoder generates local chunks rather than the whole program at once. Execution feedback determines whether revision is needed, and uncertainty refines the rollback location. The goal is not a new rollback mechanism, but a controlled comparison under the same generation, checking, and regeneration protocol.
Incremental statement generation.
As shown in Algorithm
1
,
y
y
is the accepted prefix. At each iteration, the model extends it with a token-by-token, newline-bounded chunk
s
s
, which serves as a statement-like unit in practice. This enables validation after each local extension instead of waiting for the complete function.
Algorithm
1
uses the following notation. The candidate continuation is
c
=
y
⊕
s
c=y\oplus s
, where
⊕
\oplus
denotes concatenation.
Norm
⁡
(
c
)
\operatorname{Norm}(c)
makes an incomplete candidate executable using the normalization rules described below.
Check
\operatorname{Check}
returns either
Pass
or a diagnostic
e
e
after syntax checking, public-test execution, and repetition detection.
Loc
⁡
(
e
)
\operatorname{Loc}(e)
maps a valid syntax offset to its reported position, a repetition error to the beginning of the repeated line, and another execution error to the beginning of its reported line; it returns
⊥
\bot
when that position is invalid. For each statement
S
S
on the current path,
U
⁡
(
S
)
U(S)
is the statement-level score of the selected uncertainty signal, using the aggregation defined in Section III, and
start
⁡
(
S
)
\operatorname{start}(S)
is its first token position.
Complete
⁡
(
c
,
L
)
\operatorname{Complete}(c,L)
is true when generation emits the end-of-sequence marker or reaches the maximum length
L
L
.
The trie
𝒢
\mathcal{G}
stores generated tokens, their uncertainty values, and previously explored outgoing branches;
Path
⁡
(
𝒢
)
\operatorname{Path}(\mathcal{G})
denotes the statements on its current candidate path. The counter
b
b
includes all generated tokens, including discarded continuations. The pair
(
ℓ
prev
,
k
)
(\ell_{\mathrm{prev}},k)
tracks the most recent feedback location and its consecutive failure count. Feedback localization is used for at most
K
=
2
K=2
consecutive failures at one location; otherwise, rollback selects the highest-scoring statement on the current path. At the restored node, branch decay multiplies the stored sampling weight of the outgoing edge that begins the failed suffix by
γ
=
0.9
\gamma=0.9
before regeneration.
Algorithm 1
Uncertainty-Aware Rollback Decoding
Input:
Prompt
x
x
, model
M
M
, public tests
𝒯
\mathcal{T}
, maximum length
L
L
, token budget
B
B
Output:
Completion
y
y
y
←
∅
y\leftarrow\emptyset
,
𝒢
←
root
\mathcal{G}\leftarrow\operatorname{root}
,
b
←
0
b\leftarrow 0
,
(
ℓ
prev
,
k
)
←
(
⊥
,
0
)
(\ell_{\mathrm{prev}},k)\leftarrow(\bot,0)
//
Step 1: Generate and record uncertainty
while
b
<
B
b<B
and
|
y
|
<
L
|y|<L
do
Generate a newline-bounded chunk
s
s
from
M
(
⋅
∣
x
,
y
)
M(\cdot\mid x,y)
Record every token and its uncertainty in
𝒢
\mathcal{G}
b
←
b
+
|
s
|
b\leftarrow b+|s|
,
c
←
y
⊕
s
c\leftarrow y\oplus s
//
Step 2: Validate the candidate
z
←
Norm
⁡
(
c
)
z\leftarrow\operatorname{Norm}(c)
,
e
←
Check
⁡
(
z
,
𝒯
)
e\leftarrow\operatorname{Check}(z,\mathcal{T})
if
e
=
Pass
e=\mathrm{Pass}
then
y
←
c
y\leftarrow c
,
(
ℓ
prev
,
k
)
←
(
⊥
,
0
)
(\ell_{\mathrm{prev}},k)\leftarrow(\bot,0)
if
Complete
⁡
(
y
,
L
)
\operatorname{Complete}(y,L)
then
return
y
y
else
//
Step 3: Select and apply rollback
ℓ
←
Loc
⁡
(
e
)
\ell\leftarrow\operatorname{Loc}(e)
if
ℓ
=
ℓ
prev
\ell=\ell_{\mathrm{prev}}
then
k
←
k
+
1
k\leftarrow k+1
else
(
ℓ
prev
,
k
)
←
(
ℓ
,
1
)
(\ell_{\mathrm{prev}},k)\leftarrow(\ell,1)
if
ℓ
≠
⊥
\ell\neq\bot
and
k
≤
K
k\leq K
then
r
←
ℓ
r\leftarrow\ell
else
r
←
start
⁡
(
arg
​
max
S
∈
Path
⁡
(
𝒢
)
⁡
U
​
(
S
)
)
r\leftarrow\operatorname{start}\!\left(\operatorname*{arg\,max}_{S\in\operatorname{Path}(\mathcal{G})}U(S)\right)
Downweight by
γ
\gamma
the edge entering the failed suffix at
r
r
y
←
y\leftarrow
the prefix immediately preceding
r
r
Restore the current node of
𝒢
\mathcal{G}
to that prefix
return
y
y
During this process, the selected signal’s token-level values are attached to nodes in
𝒢
\mathcal{G}
and aggregated into statement scores
U
⁡
(
S
)
U(S)
. These scores are consulted only when feedback localization is invalid or repeatedly fails.
Program assembly and feedback checking.
The candidate partial program is normalized into executable form even when the function is incomplete. This includes completing indentation blocks and temporarily inserting
break
inside an open
while
block to avoid non-terminating intermediate execution. Lightweight analysis then performs syntax checking, public-test execution, and repetition detection. A passing chunk is merged into the accepted prefix; otherwise, the unreliable suffix is rolled back rather than discarding the whole program.
Rollback strategy.
Unlike restart-based regeneration, rollback preserves the verified prefix. Reliable syntax offsets, repetition locations, and runtime error lines determine rollback directly. However, a runtime failure can surface after its underlying mistake, and shallow rollback can repeatedly revisit the same region. If the reported location is invalid or fails repeatedly, the decoder instead rolls back to the highest-uncertainty statement on the current trace, allowing it to bypass a larger suspicious region.
Generation trace and branch decay.
The trie stores the accepted path together with previously explored continuations. On rollback, the decoder restores an earlier valid node and decays the outgoing edge that begins the failed suffix. This soft penalty reduces the probability of regenerating exactly the same continuation without permanently blocking it, preserving flexibility when the search later revisits the prefix.
Termination and budget control.
The decoding loop is bounded by a token budget and a maximum generation length. When the model emits the end-of-sequence marker or reaches the maximum generation length, decoding terminates and returns the current completion. Hidden benchmark tests are applied only afterward for final evaluation and never affect online stopping or rollback.
Overall, the framework separates three complementary roles during decoding. Intermediate checking determines whether the current candidate remains executable, rollback preserves previously verified prefixes instead of restarting from scratch, and uncertainty is used only when explicit feedback cannot reliably localize the underlying error.
V
Experimental Setup
Unless otherwise stated, models are evaluated without retraining, and the rollback mechanism, checking procedure, and decoding loop remain fixed across conditions.
V-A
Benchmarks
We evaluate the framework on five code generation benchmarks and one security-oriented benchmark, covering function-level synthesis, multilingual execution, competition-style problem solving, and secure code repair
[
26
,
27
]
.
HumanEval
[
1
]
contains 164 function-level Python tasks with hidden unit tests. Intermediate checking uses executable public inputs when available; final evaluation follows the benchmark-standard pipeline.
MBPP
[
28
]
provides shorter, structured Python synthesis tasks, complementing HumanEval with basic algorithmic and library problems.
HumanEval-CPP
[
29
]
extends HumanEval-style evaluation to C++ and its stricter compilation constraints, where small structural errors can immediately invalidate the program
[
27
]
.
CodeForces2305
[
30
]
contains 90 recent competition problems emphasizing long-range reasoning, input/output handling, and algorithm design
[
15
,
4
]
. The problems go beyond function-level synthesis, and their release dates reduce contamination risk for many evaluated models.
APPS (Competition subset)
[
31
]
provides difficult programming tasks with hidden tests and less constrained solution spaces, complementing the recent CodeForces problems with a broader standard benchmark.
Dsec-Python
[
32
]
evaluates whether generated security patches align with the intended secure edit region, using a patch-level metric rather than functional pass rate
[
33
,
34
]
.
V-B
Decoding Setup
The model generates a statement-level continuation up to a newline or local structural boundary, then immediately checks it before generating the next statement. This allows rollback to occur online rather than only after a full draft is produced
[
35
,
36
,
37
]
.
Unless otherwise specified, decoding uses temperature
=
0.0
=0.0
, top-
k
=
50
k=50
, top-
p
=
1.0
p=1.0
, and one sample per task.
The maximum generation length is set to 768 tokens, and the total token budget is limited to twice this length.
For each task, error-line rollback is used for at most two consecutive failures at the same location before uncertainty-guided localization is activated.
A path-decay factor of
0.9
0.9
is applied during regeneration to reduce repeated exploration of previously failed continuations.
V-C
Intermediate Checking and Rollback
After each statement, benchmark-specific checks either accept the prefix or trigger rollback and regeneration from an earlier prefix.
We maintain a strict separation among lightweight checks, public tests, and hidden evaluation tests. Lightweight checks perform syntax validation, executable-prefix checks, and repetition detection during generation. Public tests are benchmark-provided visible examples used only for online checking and rollback decisions. Hidden tests are accessed only after generation terminates for final evaluation. No hidden-test result is exposed to decoding, rollback localization, branch decay, candidate selection, or early stopping.
Rollback localization follows a hybrid strategy.
When explicit error information is available, such as syntax offsets, runtime error lines, or repetition-triggering regions, rollback is applied near the reported failure location.
If this location is invalid or fails more than twice consecutively, the framework instead selects the statement containing the highest-uncertainty token in the current generation trace.
This design separates two roles: execution or analysis feedback determines
whether
the current prefix is problematic, while uncertainty helps determine
where
the decoding trajectory should be revised
[
38
]
.
Path decay downweights, rather than blocks, previously failed continuations.
V-D
Uncertainty Signals
We evaluate the signals in Table
I
. For each token position, multi-pass signals use
N
=
5
N=5
stochastic forward passes with MC dropout and sampling temperature
1.0
1.0
. During uncertainty estimation, the model is temporarily switched to training mode to activate dropout, gradients are disabled, and the fixed per-task random seed is retained. The model is restored to evaluation mode for main-path generation. Predictive Entropy uses the mean probability distribution across the five passes; Variation Ratio uses their modal-token frequency
[
39
]
.
All uncertainty signals are used only for rollback localization; the surrounding decoding, testing, and rollback mechanism is kept unchanged across all settings.
Table
III
compares predictive effectiveness under the same rollback framework, but multi-pass signals require additional forward passes and the comparison is not compute-normalized.
V-E
Baselines and Ablation Settings
Our main RQ1 baseline is
equal-budget restart
. It uses the same prompt, model, sampling configuration, and 1,536-token total budget as the full framework. Each attempt is limited to 768 tokens; after a failed attempt, generation restarts from the original prompt within the remaining budget, without error feedback, rollback, path decay, or uncertainty localization.
Component ablations include rollback without uncertainty guidance and uncertainty scoring without rollback, separating the effects of rollback, localization, and branch decay.
We also conduct a same-budget comparison on HumanEval and CodeForces2305 to test whether the observed gains are simply caused by using more generation tokens.
All compared strategies use CodeLlama-7B, temperature
=
0.2
=0.2
, and the same 1536-token budget; for each task, they share the initial seed defined as the base seed plus the task index.
The first strategy,
restart from scratch
, discards a failed attempt and regenerates a complete solution from the original prompt without error feedback, path decay, or sequence blocking.
The second strategy,
error-line rollback
, rolls back according to the reported error location without uncertainty-based refinement. Error-line rollback and the full framework use identical checking, regeneration, and branch-decay mechanisms; they differ only in whether uncertainty can refine the rollback location.
The third strategy is the full framework with uncertainty-guided rollback localization.
All strategies use public tests as the stopping signal.
Under the shared token budget, restart comparison controls for additional generation, while error-line rollback versus the full framework measures the incremental contribution of uncertainty-guided localization. The component ablation separately evaluates branch decay.
For Dsec-Python, equal-budget restart and the full framework use the same model, sampling configuration, and total token budget. The full framework permits at most three rollback recoveries within that budget, while restart may produce at most three candidates under the same budget. Both methods are counted as successful if any generated candidate satisfies PASR. PASR is computed only after generation and is not used for candidate selection, rollback, or stopping.
V-F
Evaluation Metrics
For HumanEval, MBPP, HumanEval-CPP, CodeForces2305, and APPS, we report
pass@1
and
AvgTestPassRate
. For task
i
i
, let
T
i
T_{i}
denote its hidden tests and
y
i
y_{i}
the single generated program. Then
AvgTestPassRate
=
1
|
D
|
∑
i
=
1
|
D
|
1
|
T
i
|
∑
j
=
1
|
T
i
|
𝟏
[
y
i
⊧
t
i
​
j
]
.
\mathrm{AvgTestPassRate}=\frac{1}{|D|}\sum_{i=1}^{|D|}\frac{1}{|T_{i}|}\sum_{j=1}^{|T_{i}|}\mathbf{1}[y_{i}\models t_{ij}].
pass@1
records whether
y
i
y_{i}
passes all hidden tests for task
i
i
, whereas
AvgTestPassRate
macro-averages the fraction of hidden tests passed per task. Thus, both metrics are compatible with one generated sample per task
[
1
,
28
,
31
]
.
For Dsec-Python,
Patch-Aligned Safe Rate (PASR)
requires line-level IoU
≥
0.5
\geq 0.5
and normalized similarity
≥
0.6
\geq 0.6
in the modified region. A task succeeds if any of at most three candidates generated within the matched total token budget meets both criteria.
For the uncertainty-guided rollback diagnostics, we retain only events logged as
uncertainty_fallback
or
uncertainty_refinement
, excluding error-line and other feedback-only rollbacks. We report the number of uncertainty-selected events, the subset with a comparable reported error line, the within-3-line rate over that subset, and the fraction of uncertainty-selected events whose next lightweight check succeeds. The line-distance metric remains an operational proxy rather than manually annotated bug-localization ground truth.
For functional-error analysis, we use
AssertionError
as a proxy for functional failures, meaning programs that execute but fail test assertions; this should not be interpreted as a manually labeled semantic-error category.
V-G
Implementation Details
The framework uses PyTorch
[
40
]
and HuggingFace Transformers
[
41
]
. The main experiments ran on four NVIDIA Tesla V100-SXM2 GPUs (16GB each), 28 Intel Xeon Gold 6132 CPU cores, and 754GB RAM, using Python 3.10, PyTorch 2.8.0, Transformers 4.40.0, and CUDA 12.7.
The rollback-diagnostic and same-budget experiments reported in Section
VI-B
were run separately from the main multi-model evaluation using CodeLlama-7B and Max Token Entropy.
We therefore interpret these results as within-environment comparisons among rollback strategies rather than as direct runtime comparisons with the main server experiments.
The diagnostic machine used an NVIDIA RTX 3090 (24GB), Intel Xeon Gold 6226R CPUs, 125GB RAM, and Ubuntu 20.04.6, with Python 3.11.9, PyTorch 2.3.0+cu121, and Transformers 4.40.1.
VI
Results
This section evaluates overall effectiveness, uncertainty signals, model-scale effects, rollback diagnostics, component ablations, and error types. The main results are shown in Table
II
, Table
III
, Table
IV
, Table
V
, and Table
VI
, with complementary analyses in Figures
2
and
3
.
VI-A
RQ1: Does the complete rollback framework improve over equal-budget restart across datasets and models?
Table
II
compares the complete rollback framework with equal-budget restart. Because the full framework jointly includes feedback, rollback, branch decay, and uncertainty localization, this comparison supports the complete framework rather than the isolated effect of uncertainty. Improvements appear on HumanEval, MBPP, and HumanEval-CPP. For example, on HumanEval, DeepSeek-7B improves from 0.32/0.49 to 0.52/0.69, Qwen2.5-7B from 0.36/0.56 to 0.55/0.77, and CodeLlama-34B from 0.48/0.68 to 0.61/0.81.
TABLE II:
RQ1 complete-framework results against equal-budget restart. The full framework uses Max Token Entropy. Both settings use a 1,536-token total budget and at most 768 tokens per attempt. Generation benchmarks report pass@1 / AvgTestPassRate; Dsec-Python reports PASR.
Dataset
DS
DeepSeek-7B
SC
StarCoder2-7B
Q
Qwen2.5-7B
M
Mistral-7B
CL
CodeLlama-7B
S
SafeCoder-7B
CL
CodeLlama-34B
HumanEval
0.52/0.69
0.45/0.68
0.55/0.77
0.40/0.61
0.39/0.61
0.36/0.59
0.61/0.81
MBPP
0.34/0.55
0.30/0.50
0.36/0.58
0.27/0.46
0.25/0.43
0.23/0.41
0.43/0.66
HumanEval-CPP
0.36/0.56
0.41/0.57
0.43/0.66
0.29/0.44
0.35/0.54
0.30/0.47
0.53/0.73
CodeForces2305
0.09/0.28
0.08/0.26
0.10/0.32
0.07/0.24
0.06/0.20
0.05/0.18
0.15/0.40
APPS-Competition
0.16/0.26
0.13/0.21
0.15/0.24
0.14/0.25
0.10/0.18
0.07/0.10
0.23/0.34
Dsec-Python
0.56
0.51
0.57
0.48
0.55
0.53
0.54
HumanEval–Restart
0.32/0.49
0.27/0.38
0.36/0.56
0.22/0.40
0.23/0.42
0.20/0.37
0.48/0.68
MBPP–Restart
0.22/0.35
0.19/0.32
0.23/0.37
0.17/0.29
0.16/0.27
0.14/0.26
0.34/0.54
HumanEval-CPP–Restart
0.18/0.30
0.20/0.27
0.17/0.31
0.15/0.27
0.23/0.33
0.16/0.24
0.43/0.61
CodeForces2305–Restart
0.05/0.15
0.04/0.14
0.06/0.18
0.04/0.13
0.03/0.11
0.03/0.10
0.11/0.30
APPS-Competition–Restart
0.13/0.24
0.08/0.17
0.14/0.19
0.09/0.15
0.08/0.18
0.05/0.16
0.16/0.34
Dsec-Python–Restart
0.50
0.47
0.52
0.45
0.49
0.47
0.50
The trend remains visible on harder long-horizon benchmarks. On CodeForces2305, StarCoder2-7B from 0.04/0.14 to 0.08/0.26, and CodeLlama-34B from 0.11/0.30 to 0.15/0.40.
For Dsec-Python, the complete framework also improves over equal-budget restart across all evaluated models in Table
II
, e.g., from 0.50 to 0.56 for DeepSeek-7B and from 0.52 to 0.57 for Qwen2.5-7B. However, the margins are smaller than those on execution-based benchmarks. A likely reason is that Patch-Aligned Safe Rate is a relatively coarse static metric, whose sensitivity to fine-grained decoding differences is limited.
Finding 1.
The complete rollback framework improves over equal-budget restart across the evaluated benchmarks; this comparison does not isolate the contribution of uncertainty.
Table
III
compares the predictive effectiveness of uncertainty signals under the same rollback framework; it is not an equal-compute comparison because multi-pass signals require five forward passes per token position. Overall, information-theoretic signals, especially
Max Token Entropy
and
Avg NLL
, show the strongest trend on standard code-generation benchmarks. Max Token Entropy achieves the best or near-best results in many settings, including HumanEval, MBPP, HumanEval-CPP, and CodeForces2305. Avg NLL is also consistently competitive.
TABLE III:
Predictive-effectiveness comparison of uncertainty signals under the same rollback framework; results are not compute-normalized. Generation benchmarks report pass@1 / AvgTestPassRate; Dsec-Python reports PASR. Multi-pass signals use five stochastic forward passes. The best result for each dataset–model pair is shaded and boldfaced (ties included).
Dataset
Method
DS
DeepSeek-7B
SC
StarCoder2-7B
Q
Qwen2.5-7B
M
Mistral-7B
CL
CodeLlama-7B
S
SafeCoder-7B
CL
CodeLlama-34B
HumanEval
Avg NLL
0.49/0.67
0.45/0.62
0.54/0.72
0.38/0.56
0.42/0.59
0.34/0.55
0.60/0.77
Max Token Entropy
0.52/0.69
0.45/0.68
0.55/0.77
0.40/0.61
0.39/0.61
0.36/0.59
0.61/0.81
Max Probability
0.44/0.61
0.48/0.59
0.47/0.67
0.37/0.54
0.43/0.61
0.36/0.52
0.53/0.70
Least Confidence
0.46/0.63
0.43/0.64
0.51/0.65
0.42/0.58
0.40/0.57
0.31/0.53
0.52/0.72
Margin of Confidence
0.47/0.65
0.50/0.68
0.49/0.69
0.36/0.55
0.44/0.58
0.37/0.51
0.56/0.71
Gini Impurity
0.51/0.62
0.41/0.66
0.55/0.68
0.43/0.60
0.39/0.56
0.35/0.58
0.54/0.69
Predictive Entropy
0.43/0.66
0.49/0.61
0.48/0.73
0.39/0.61
0.36/0.53
0.33/0.59
0.57/0.78
Variation Ratio
0.45/0.60
0.46/0.67
0.50/0.64
0.35/0.57
0.37/0.54
0.30/0.50
0.51/0.74
MBPP
Avg NLL
0.32/0.53
0.28/0.47
0.36/0.55
0.26/0.44
0.25/0.42
0.23/0.40
0.42/0.64
Max Token Entropy
0.34/0.55
0.30/0.50
0.36/0.58
0.27/0.46
0.25/0.43
0.23/0.41
0.43/0.66
Max Probability
0.29/0.49
0.32/0.44
0.30/0.52
0.25/0.41
0.28/0.46
0.25/0.38
0.37/0.60
Least Confidence
0.31/0.50
0.27/0.48
0.33/0.51
0.29/0.43
0.23/0.41
0.21/0.40
0.36/0.60
Margin of Confidence
0.30/0.52
0.32/0.50
0.32/0.54
0.24/0.40
0.27/0.42
0.26/0.37
0.40/0.59
Gini Impurity
0.34/0.48
0.26/0.50
0.35/0.53
0.30/0.45
0.22/0.40
0.25/0.44
0.38/0.58
Predictive Entropy
0.30/0.55
0.31/0.47
0.29/0.53
0.27/0.48
0.21/0.39
0.20/0.43
0.43/0.66
Variation Ratio
0.28/0.48
0.31/0.53
0.32/0.50
0.24/0.43
0.26/0.39
0.20/0.38
0.37/0.59
HumanEval-CPP
Avg NLL
0.33/0.57
0.36/0.51
0.40/0.68
0.27/0.39
0.32/0.56
0.28/0.43
0.49/0.74
Max Token Entropy
0.36/0.56
0.41/0.57
0.43/0.66
0.29/0.44
0.35/0.54
0.30/0.47
0.53/0.73
Max Probability
0.29/0.46
0.38/0.54
0.35/0.61
0.26/0.37
0.37/0.50
0.32/0.41
0.45/0.70
Least Confidence
0.34/0.49
0.33/0.55
0.39/0.55
0.31/0.47
0.32/0.54
0.25/0.45
0.47/0.63
Margin of Confidence
0.30/0.54
0.40/0.59
0.37/0.64
0.24/0.35
0.37/0.55
0.33/0.40
0.50/0.67
Gini Impurity
0.36/0.53
0.34/0.56
0.42/0.58
0.32/0.41
0.28/0.48
0.27/0.49
0.51/0.65
Predictive Entropy
0.29/0.53
0.39/0.47
0.36/0.63
0.28/0.46
0.29/0.44
0.24/0.47
0.46/0.72
Variation Ratio
0.31/0.43
0.36/0.58
0.41/0.53
0.23/0.46
0.27/0.41
0.26/0.38
0.44/0.71
CodeForces2305
Avg NLL
0.08/0.26
0.07/0.24
0.08/0.28
0.06/0.22
0.05/0.19
0.04/0.17
0.14/0.38
Max Token Entropy
0.09/0.28
0.08/0.26
0.10/0.32
0.07/0.24
0.06/0.20
0.05/0.18
0.15/0.40
Max Probability
0.07/0.23
0.08/0.23
0.07/0.26
0.06/0.19
0.06/0.20
0.05/0.16
0.12/0.35
Least Confidence
0.08/0.24
0.07/0.25
0.08/0.25
0.07/0.20
0.05/0.18
0.04/0.17
0.12/0.36
Margin of Confidence
0.07/0.25
0.09/0.26
0.07/0.28
0.05/0.18
0.07/0.19
0.06/0.15
0.13/0.34
Gini Impurity
0.09/0.24
0.06/0.24
0.08/0.27
0.08/0.23
0.04/0.17
0.05/0.19
0.11/0.33
Predictive Entropy
0.06/0.27
0.08/0.24
0.07/0.29
0.06/0.25
0.04/0.16
0.04/0.18
0.14/0.37
Variation Ratio
0.07/0.21
0.07/0.25
0.07/0.23
0.05/0.19
0.06/0.15
0.03/0.15
0.10/0.32
APPS-Competition
Avg NLL
0.15/0.24
0.12/0.20
0.14/0.23
0.13/0.21
0.09/0.16
0.06/0.09
0.21/0.31
Max Token Entropy
0.16/0.26
0.13/0.21
0.15/0.24
0.14/0.25
0.10/0.18
0.07/0.10
0.23/0.34
Max Probability
0.11/0.19
0.15/0.22
0.10/0.18
0.12/0.17
0.11/0.19
0.08/0.11
0.18/0.27
Least Confidence
0.13/0.20
0.10/0.18
0.13/0.19
0.15/0.22
0.08/0.15
0.05/0.08
0.17/0.28
Margin of Confidence
0.14/0.22
0.16/0.24
0.12/0.20
0.10/0.16
0.12/0.17
0.09/0.12
0.20/0.29
Gini Impurity
0.17/0.23
0.09/0.17
0.16/0.22
0.16/0.24
0.07/0.14
0.08/0.13
0.19/0.26
Predictive Entropy
0.11/0.20
0.14/0.19
0.12/0.20
0.12/0.22
0.06/0.13
0.04/0.09
0.22/0.32
Variation Ratio
0.09/0.17
0.11/0.20
0.12/0.18
0.08/0.15
0.07/0.12
0.03/0.06
0.16/0.24
Dsec-Python
Avg NLL
0.54
0.53
0.56
0.50
0.53
0.51
0.55
Max Token Entropy
0.56
0.51
0.57
0.48
0.55
0.53
0.54
Max Probability
0.51
0.56
0.52
0.51
0.55
0.50
0.52
Least Confidence
0.54
0.50
0.55
0.52
0.49
0.55
0.51
Margin of Confidence
0.52
0.57
0.53
0.47
0.56
0.51
0.50
Gini Impurity
0.57
0.49
0.55
0.53
0.48
0.56
0.53
Predictive Entropy
0.53
0.55
0.51
0.51
0.52
0.54
0.56
Variation Ratio
0.51
0.54
0.54
0.46
0.50
0.49
0.48
At the same time, no single signal is universally optimal. In several cases, confidence-based or alternative signals remain competitive. For example, Gini Impurity performs strongly on APPS-Competition for DeepSeek-7B, and the best-performing signal on Dsec-Python varies by model. The differences among signals also become smaller on harder settings such as CodeForces2305, APPS-Competition, and Dsec-Python.
Finding 2.
In the predictive-effectiveness comparison, Max Token Entropy and Avg NLL perform relatively better than other signals, but no signal consistently dominates; multi-pass results are not compute-normalized.
The gains in Table
II
are not limited to a single evaluated backbone. Improvements appear across multiple 7B models, including DeepSeek-7B, StarCoder2-7B, Qwen2.5-7B, Mistral-7B, CodeLlama-7B, and SafeCoder-7B, suggesting that the method is not tied to a specific architecture.
The framework also remains effective for stronger models. In Table
II
, CodeLlama-34B improves from 0.48/0.68 to 0.61/0.81 on HumanEval, from 0.34/0.54 to 0.43/0.66 on MBPP, and from 0.43/0.61 to 0.53/0.73 on HumanEval-CPP. This suggests that rollback remains useful not only for weaker models, but also for stronger generators in the evaluated settings.
We also fine-tune CodeLlama-7B on the APPS training split using 4-bit NF4 QLoRA for two epochs (learning rate
2
×
10
−
4
2\times 10^{-4}
, rank 16, LoRA alpha 32, seed 42). Figure
2
compares the merged final-epoch model with the base model under the same rollback configuration.
Fig. 2:
CodeLlama-7B and its fine-tuned variant under the same rollback configuration. Red labels show the maximum absolute gain in each panel.
These improvements are consistently observed across models with different parameter scales and across both functional and security-oriented benchmarks. Although the absolute gains vary depending on task difficulty and model capability, the overall trend suggests that rollback-based decoding remains beneficial under diverse evaluation settings.
Finding 3.
The proposed framework remains effective across the evaluated model scales, and the fine-tuned variant also improves over its base model.
VI-B
RQ2: What are the contributions of rollback, uncertainty, and branch decay?
VI-B
1
Rollback Diagnostics and Controlled Comparison
To examine uncertainty-guided decisions directly, we instrumented CodeLlama-7B with Max Token Entropy on HumanEval and on CodeForces2305 with its revised evaluation harness. The diagnostic run uses temperature
=
0.0
=0.0
and seed
=
0
=0
. It records token entropy and, when the reported line is invalid or the same location fails more than twice, rolls back to the line containing the highest-entropy token on the current path; no fixed entropy threshold is used.
Table
IV
includes only
uncertainty_fallback
and
uncertainty_refinement
events. On HumanEval, 1,346 rollbacks are selected by entropy; 226 have a comparable reported error line, and 85.84% of these selections fall within three lines. The next lightweight check succeeds after 77.93% of uncertainty-selected rollbacks. On CodeForces2305, the corresponding counts are 951 and 417, with a 72.90% within-3-line rate and a 70.14% next-check pass rate.
TABLE IV:
Diagnostics restricted to uncertainty-selected rollback events. UC Ev.: uncertainty-selected events; Comp.: events with a comparable reported error line;
≤
\leq
3: rollback within three lines.
Dataset
UC Ev.
Comp.
≤
\leq
3
Next Pass
HumanEval
1,346
226
85.84%
77.93%
CF2305
951
417
72.90%
70.14%
These measurements isolate behavior after entropy-based localization rather than mixing it with feedback-only rollback. They show that uncertainty-selected points are often close to the observed failure and frequently enable the next check to pass, although they do not by themselves constitute a counterfactual comparison against alternative localization rules.
The runs average 11.52 and 20.24 rollbacks per task on HumanEval and CodeForces2305, respectively. Uncertainty-score computation accounts for 3.99% and 1.86% of runtime in these diagnostic runs; these values do not represent end-to-end overhead relative to standard decoding.
We further compare the full framework against two alternatives under the same 1536-token budget.
As shown in Table
V
, simply restarting from the original prompt after failure reaches 23.17% pass rate on HumanEval, while rolling back directly to the reported error line reaches 32.32%.
The full framework reaches 41.46% while using fewer average generated tokens than both alternatives.
The same trend appears on CodeForces2305: restart and error-line rollback both reach 2.22%, while the full framework reaches 4.44%.
Although the absolute pass rate on CodeForces2305 remains low due to task difficulty, the controlled comparison indicates that the gain is not explained merely by allowing more tokens or more regeneration attempts.
TABLE V:
Same-budget comparison under a 1536-token budget. Tok.: average generated tokens; RB: average rollback count (not applicable to restart).
Dataset
Strategy
Pass
Tok.
RB
HumanEval
Restart from scratch
23.17%
1224.15
–
Error-line rollback
32.32%
935.34
72.15
Full framework
41.46%
644.27
13.40
CodeForces2305
Restart from scratch
2.22%
1427.47
–
Error-line rollback
2.22%
1399.00
96.87
Full framework
4.44%
1304.71
51.10
Functional-failure proxy.
To distinguish assertion failures from parsing and runtime errors, we track
AssertionError
, which indicates that a program executes but fails a test assertion. In the temperature-
0.0
0.0
diagnostic run, it accounts for 1,102/1,889 (58.34%) rollback events and 69/164 (42.07%) final samples on HumanEval, and 534/1,822 (29.31%) rollback events and 72/90 (80.00%) final samples on CodeForces2305. Event-level and final-sample statistics therefore use different denominators. In the separate temperature-
0.2
0.2
same-budget run, final
AssertionError
proxy cases decrease from 110 to 76 on HumanEval and from 73 to 67 on CodeForces2305 when the full method replaces error-line rollback. This is a test-level proxy rather than manually annotated semantic-error ground truth.
Finding 4.
Strictly filtered uncertainty-guided rollbacks frequently select locations near the reported failure and are followed by high next-check pass rates; uncertainty-score computation occupies a small fraction of diagnostic runtime, while same-budget comparisons show gains beyond extra generation budget and fewer final
AssertionError
proxy cases than error-line rollback.
An additional observation is that the framework often requires fewer generated tokens before converging to a successful solution. Instead of repeatedly regenerating complete programs, rollback revisits only suspicious regions while preserving verified prefixes. This behavior explains why the full framework can simultaneously achieve higher accuracy and lower average token consumption under the same overall decoding budget.
This result also suggests that rollback improves search efficiency instead of merely increasing exploration. Because validated prefixes are retained throughout decoding, the search process can concentrate on correcting suspicious regions rather than reconstructing already verified program fragments. Consequently, the available generation budget is allocated more effectively, allowing additional refinement attempts before the decoding budget is exhausted.
VI-B
2
Component Ablation
Table
VI
reports the CodeLlama-7B ablation on HumanEval. Feedback-Only Detection improves only slightly over Vanilla Decoding (0.25 vs. 0.23 pass@1), while Feedback-Guided Rollback reaches 0.33 pass@1 and 0.53 AvgTestPassRate. The causal comparison for uncertainty is between Feedback-Guided Rollback and the Full Framework: both use feedback, rollback, branch decay, the same checks, and the same budget, and differ only in uncertainty localization. Adding uncertainty raises pass@1 from 0.33 to 0.39 and AvgTestPassRate from 0.53 to 0.61. This matched evidence is currently limited to CodeLlama-7B on HumanEval.
TABLE VI:
CodeLlama-7B ablation results on HumanEval. Feedback-Guided Rollback and Full Framework share feedback, rollback, branch decay, checking, and budget; only the latter uses uncertainty localization. Comp. denotes compilation pass rate.
Variant
pass@1
AvgTestPassRate
Comp.
Vanilla Decoding
0.23
0.42
0.84
Feedback-Only Detection
0.25
0.44
0.86
Feedback-Guided Rollback
0.33
0.53
0.92
Uncertainty-Guided Rollback
0.27
0.46
0.88
Full w/o Branch Decay
0.37
0.59
0.94
Full Framework
0.39
0.61
0.96
Finding 5.
Feedback-guided rollback provides the main improvement, while uncertainty provides an additional gain when checking, budget, rollback, and branch decay are controlled.
VI-C
RQ3: How does uncertainty behave across rollback-triggering error types?
Table
VII
complements the aggregate analysis with representative corrections across rollback-triggering error types.
TABLE VII:
Representative corrections across rollback-triggering error types on HumanEval. Highlighted tokens indicate the repaired fragments.
Error Type
Before Rollback
After Rollback
NameError
⬇
#
TASK
4
mean
=
sum
(
numbers
)
/
len
(
numbers
)
return
sum
(
abs
(
x
-
mean(numbers)
)
for
x
in
numbers
)
⬇
#
TASK
4
mean
=
sum
(
numbers
)
/
len
(
numbers
)
return
sum
(
abs
(
x
-
mean
)
for
x
in
numbers
)
IndexError
⬇
#
TASK
33
l
.
insert
(
i
,
sorted
(
l
[
i
:
i
+3]))
l
.
pop
(
i
+1)
l
.
pop
(
i
+1)
l.pop(i+1)
⬇
#
TASK
33
l[i:i+3] = sorted(l[i:i+3])
RepeatPatternError
⬇
#
TASK
1
if
paren_string
==
’()’
:
return
[
’()’
]
if
paren_string
==
’()()’
:
return
[
’()’
,
’()’
]
if paren_string == ’()()()’:
⬇
#
TASK
1
groups
,
cur
,
bal
=
[],
[],
0
for
ch
in
paren_string
:
bal
+=
1
if
ch
==
’(’
else
-1
cur
.
append
(
ch
)
if
bal
==
0:
groups
.
append
(
’’
.
join
(
cur
));
cur
=
[]
SyntaxError
⬇
#
TASK
6
for
ch
in
paren_string
:
if
ch
==
’(’
:
depth
+=
1
return
[
⬇
#
TASK
6
for
ch
in
paren_string
:
if
ch
==
’(’
:
depth
+=
1
return
depth
Table
VII
illustrates that rollback supports both localized repairs and broader structural revisions. NameError and SyntaxError are corrected through small fragment replacements, whereas IndexError and RepeatPatternError require rewriting a larger statement or control-flow block, showing why rollback depth should adapt to the observed failure pattern.
Figure
3
shows the distribution of rollback-triggering error types and their associated uncertainty values. NameError (
n
=
283
n=283
) and TypeError (
n
=
202
n=202
) are among the most frequent error categories, followed by RepeatPatternError, IndexError, and ValueError.
Fig. 3:
Rollback-triggering error types and uncertainty. Bars show event-level means, white circles show medians, and error bars denote one standard deviation across rollback events. Error bars are omitted for categories with
n
=
1
n=1
.
At the same time, the highest uncertainty values are associated with more structurally unstable errors. SyntaxError has the highest mean uncertainty (1.85), while IndentationError (1.51) and TypeError (1.51) are also clearly above the overall average. In contrast, more common local semantic errors such as NameError (0.94), IndexError (0.83), and ValueError (0.70) show lower uncertainty. This suggests that uncertainty is not simply tracking how often an error occurs; instead, it better reflects how destabilizing that error is to the ongoing generation process.
The observed uncertainty distribution also suggests that uncertainty is associated with structural instability rather than merely reflecting error frequency. This observation is consistent with the intuition that rollback should prioritize regions where the decoding trajectory becomes unstable instead of simply revisiting the most recently generated tokens.
This pattern supports the role of uncertainty in our framework: it is more useful as a cue for rollback localization than as a standalone predictor of final correctness.
We note that categories with fewer than five events are reported descriptively and should be interpreted cautiously; the error bars summarize dispersion and are not confidence intervals.
Finding 6.
Rollback-triggering uncertainty tends to be higher for structurally unstable errors than for common local semantic mistakes, supporting its use as a rollback-localization cue.
VII
Threats to Validity
Statistical validity.
Due to computational cost, our experiments use a single-run evaluation setting and do not include repeated trials, confidence intervals, or formal significance tests. Therefore, the reported improvements should be interpreted as empirical trends on the evaluated benchmarks rather than statistically conclusive effect estimates, especially when the gaps between uncertainty signals are small
[
3
,
4
,
30
]
.
Construct validity.
Our evaluation uses functional correctness metrics (e.g., pass@1 and AvgTestPassRate) for code-generation benchmarks and Patch-Aligned Safe Rate for Dsec-Python. While practical, these metrics do not fully capture all aspects of generation quality. In particular, the Dsec-Python metric relies on patch alignment and lightweight static validation, so its sensitivity to subtle security improvements is limited compared with end-to-end exploit-level verification.
Similarly, our rollback-line distance and
AssertionError
analyses are operational proxies rather than manually annotated ground truth for bug localization or semantic functional-error categories.
External validity.
Although we evaluate multiple representative open-source code LLMs, including several 7B-scale models and one 34B model, the study still covers only a limited portion of the model space. In addition, most benchmarks are Python-centered. Therefore, the findings should be understood as evidence on the evaluated settings rather than a universal conclusion.
Methodological validity.
Our conclusions are drawn under a fixed rollback-based decoding framework with a specific intermediate-checking and branch-decay design. Therefore, the observed effectiveness of uncertainty signals should be interpreted in this context. Different rollback strategies, checking mechanisms, or search policies may lead to different relative behaviors of uncertainty estimators. In addition, lightweight intermediate checking may not capture all failure modes equally well.
The diagnostic and same-budget experiments were conducted on a separate machine from the main multi-model evaluation, so their runtime numbers should be interpreted within that diagnostic setting rather than directly compared with the main experimental server.
Future work may further investigate adaptive rollback policies, alternative intermediate verification strategies, and larger proprietary code models. We also expect stronger execution feedback to further improve uncertainty-guided localization in more realistic programming environments.
VIII
Conclusion
This paper studied whether uncertainty signals can improve rollback-based decoding for code generation. The complete rollback framework improves over equal-budget restart across the evaluated models and benchmarks, with gains of up to 0.26 in pass@1 and 0.35 in AvgTestPassRate on functional benchmarks and up to 6.4% in Patch-Aligned Safe Rate on Dsec-Python. These comparisons evaluate the complete framework rather than uncertainty alone. In the matched component ablation, feedback-guided rollback provides the main improvement, while uncertainty adds a further gain when checking, budget, rollback, and branch decay are controlled. Diagnostics restricted to entropy-selected events show high within-3-line and next-check pass rates; uncertainty-score computation accounts for a small fraction of diagnostic runtime but does not measure end-to-end overhead relative to standard decoding. Information-theoretic signals show the most stable predictive effectiveness, although multi-pass comparisons are not compute-normalized and no signal is universally best.
Data Availability Statement
The replication package, including the source code and evaluation scripts, is available through an anonymous repository: https://anonymous.4open.science/r/ICSE2027-257C
References
[1]
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba
(2021)
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
Cited by:
§I
,
§II
,
§V-A
,
§V-F
.
[2]
B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J. Lou, and W. Chen
(2023)
CodeT: code generation with generated tests
.
In
The Eleventh International Conference on Learning Representations
,
External Links:
Link
Cited by:
§I
.
[3]
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
(2023)
Is your code generated by ChatGPT really correct? rigorous evaluation of large language models for code generation
.
In
Advances in Neural Information Processing Systems
,
Vol.
36
.
Cited by:
§I
,
§VII
.
[4]
T. Y. Zhuo, C. Vu, J. Chim, H. Hu, H. Zhan, W. Yu, N. Muennighoff, J. Kaddour, W. Li, J. He, M. Xu, Z. Zhang, R. Widyasari, I. Paul, S. Brunner, I. N. B. Yusuf, T. Hoang, C. Gong, A. Zebaze, and P. Yadav
(2025)
BigCodeBench: benchmarking code generation with diverse function calls and complex instructions
.
In
The Thirteenth International Conference on Learning Representations (ICLR)
,
External Links:
Link
Cited by:
§I
,
§V-A
,
§VII
.
[5]
X. Chen, M. Lin, N. Schärli, and D. Zhou
(2024)
Teaching large language models to self-debug
.
In
International Conference on Learning Representations
,
Vol.
2024
,
pp. 8746–8825
.
External Links:
Link
Cited by:
§I
.
[6]
A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang, S. Gupta, B. P. Majumder, K. Hermann, S. Welleck, A. Yazdanbakhsh, and P. Clark
(2023)
SELF-refine: iterative refinement with self-feedback
.
In
Proceedings of the 37th International Conference on Neural Information Processing Systems
,
NIPS ’23
,
Red Hook, NY, USA
.
External Links:
Link
Cited by:
§I
.
[7]
A. Ni, S. Iyer, D. Radev, V. Stoyanov, W. Yih, S. I. Wang, and X. V. Lin
(2023)
LEVER: learning to verify language-to-code generation with execution
.
In
Proceedings of the 40th International Conference on Machine Learning (ICML)
,
Proceedings of Machine Learning Research
, Vol.
202
,
pp. 26106–26128
.
External Links:
Link
Cited by:
§I
,
§II
.
[8]
S. Zhang, Z. Chen, Y. Shen, M. Ding, J. B. Tenenbaum, and C. Gan
(2023)
Planning with large language models for code generation
.
In
The Eleventh International Conference on Learning Representations (ICLR)
,
External Links:
Link
Cited by:
§I
,
§II
,
§II
.
[9]
H. Le, H. Chen, A. Saha, A. Gokul, D. Sahoo, and S. Joty
(2024)
CodeChain: towards modular code generation through chain of self-revisions with representative sub-modules
.
In
The Twelfth International Conference on Learning Representations (ICLR)
,
Cited by:
§I
.
[10]
X. Jiang, Y. Dong, Y. Tao, H. Liu, Z. Jin, and G. Li
(2025)
ROCODE: integrating backtracking mechanism and program analysis in large language models for code generation
.
In
Proceedings of the IEEE/ACM 47th International Conference on Software Engineering
,
pp. 334–346
.
External Links:
Document
,
Link
Cited by:
§I
,
§II
,
§II
,
§IV
.
[11]
L. Kuhn, Y. Gal, and S. Farquhar
(2023)
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
The Eleventh International Conference on Learning Representations (ICLR)
,
External Links:
Link
Cited by:
§I
,
§II
.
[12]
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
§I
,
§II
.
[13]
A. V. Nikitin, J. Kossen, Y. Gal, and P. Marttinen
(2024)
Kernel language entropy: fine-grained uncertainty quantification for llms from semantic similarities
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Vol.
37
.
External Links:
Document
Cited by:
§I
,
§II
.
[14]
T. X. Olausson, J. P. Inala, C. Wang, J. Gao, and A. Solar-Lezama
(2024)
Is self-repair a silver bullet for code generation?
.
In
The Twelfth International Conference on Learning Representations (ICLR)
,
External Links:
Link
Cited by:
§II
.
[15]
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy, C. de Masson d’Autume, I. Babuschkin, X. Chen, P. Huang, J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S. Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals
(2022)
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
Cited by:
§II
,
§V-A
.
[16]
H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. H. Hoi
(2022)
CodeRL: mastering code generation through pretrained models and deep reinforcement learning
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Vol.
35
,
pp. 21314–21328
.
Cited by:
§II
.
[17]
T. Zheng, G. Zhang, T. Shen, X. Liu, B. Y. Lin, J. Fu, W. Chen, and X. Yue
(2024)
OpenCodeInterpreter: integrating code generation with execution and refinement
.
In
Findings of the Association for Computational Linguistics: ACL 2024
,
pp. 12834–12859
.
External Links:
Document
Cited by:
§II
.
[18]
Z. Bi, Y. Wan, Z. Wang, H. Zhang, B. Guan, F. Lu, Z. Zhang, Y. Sui, H. Jin, and X. Shi
(2024)
Iterative refinement of project-level code context for precise code generation with compiler feedback
.
In
Findings of the Association for Computational Linguistics: ACL 2024
,
pp. 2336–2353
.
External Links:
Document
Cited by:
§II
.
[19]
B. Settles
(2009)
Active learning literature survey
.
Technical report
Technical Report
1648
,
University of Wisconsin–Madison
.
External Links:
Link
Cited by:
2nd item
,
3rd item
,
4th item
,
5th item
,
§III-C
,
§III
.
[20]
Y. Gal and Z. Ghahramani
(2016)
Dropout as a bayesian approximation: representing model uncertainty in deep learning
.
In
Proceedings of the 33rd International Conference on Machine Learning
,
pp. 1050–1059
.
External Links:
Link
Cited by:
1st item
,
§III-B
,
§III-C
,
§III-C
,
§III
.
[21]
H. S. Seung, M. Opper, and H. Sompolinsky
(1992)
Query by committee
.
In
Proceedings of the Fifth Annual Workshop on Computational Learning Theory
,
pp. 287–294
.
External Links:
Document
Cited by:
2nd item
,
§III
.
[22]
C. E. Shannon
(1948)
A mathematical theory of communication
.
Bell System Technical Journal
27
(
3
),
pp. 379–423
.
External Links:
Document
Cited by:
1st item
,
2nd item
.
[23]
D. D. Lewis and W. A. Gale
(1994)
A sequential algorithm for training text classifiers
.
In
Proceedings of the 17th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval
,
pp. 3–12
.
External Links:
Document
Cited by:
3rd item
,
4th item
.
[24]
L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone
(1984)
Classification and regression trees
.
Wadsworth
,
Belmont, CA
.
Cited by:
6th item
.
[25]
Y. Gal
(2016)
Uncertainty in deep learning
.
Ph.D. Thesis
,
University of Cambridge
.
External Links:
Link
Cited by:
1st item
,
2nd item
,
§III-C
.
[26]
Z. Zheng, K. Ning, Y. Wang, J. Zhang, D. Zheng, M. Ye, and J. Chen
(2023)
A survey of large language models for code: evolution, benchmarking, and future trends
.
CoRR
abs/2311.10372
.
External Links:
Link
Cited by:
§V-A
.
[27]
J. Cao, Z. Chen, J. Wu, S. Cheung, and C. Xu
(2024)
JavaBench: a benchmark of object-oriented code generation for evaluating large language models
.
In
Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering
,
pp. 870–882
.
External Links:
Document
,
Link
Cited by:
§V-A
,
§V-A
.
[28]
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton
(2021)
Program synthesis with large language models
.
arXiv preprint arXiv:2108.07732
.
Cited by:
§V-A
,
§V-F
.
[29]
Q. Zheng, X. Xia, X. Zou, Y. Dong, S. Wang, Y. Xue, Z. Wang, L. Shen, A. Wang, Y. Li, T. Su, Z. Yang, and J. Tang
(2023)
CodeGeeX: a pre-trained model for code generation with multilingual benchmarking on humaneval-x
.
In
Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining
,
pp. 5673–5684
.
External Links:
Document
,
Link
Cited by:
§V-A
.
[30]
Y. Dong, X. Jiang, H. Liu, Z. Jin, B. Gu, M. Yang, and G. Li
(2024)
Generalization or memorization: data contamination and trustworthy evaluation for large language models
.
In
Findings of the Association for Computational Linguistics: ACL 2024
,
Bangkok, Thailand
,
pp. 12039–12050
.
External Links:
Document
,
Link
Cited by:
§V-A
,
§VII
.
[31]
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song, and J. Steinhardt
(2021)
Measuring coding challenge competence with apps
.
In
Advances in Neural Information Processing Systems Datasets and Benchmarks Track
,
Vol.
34
.
External Links:
Link
Cited by:
§V-A
,
§V-F
.
[32]
J. He, M. Vero, G. Krasnopolska, and M. Vechev
(2024)
Instruction tuning for secure code generation
.
In
Proceedings of the 41st International Conference on Machine Learning
,
Proceedings of Machine Learning Research
, Vol.
235
,
pp. 18043–18062
.
External Links:
Link
Cited by:
§V-A
.
[33]
M. H. M. Bhuiyan, A. S. Parthasarathy, N. Vasilakis, M. Pradel, and C. Staicu
(2023)
SecBench.js: an executable security benchmark suite for server-side javascript
.
In
Proceedings of the 45th IEEE/ACM International Conference on Software Engineering
,
pp. 1059–1070
.
External Links:
Document
Cited by:
§V-A
.
[34]
J. Zhao, Y. Sun, C. Huang, C. Liu, Y. Guan, Y. Zeng, and Y. Liu
(2025)
Towards secure code generation with llms: a study on common weakness enumeration
.
IEEE Transactions on Software Engineering
51
(
12
),
pp. 3507–3523
.
External Links:
Document
,
Link
Cited by:
§V-A
.
[35]
H. Zhang, H. Chen, M. Chen, and T. Zhang
(2025)
Active layer-contrastive decoding reduces hallucination in large language model generation
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
Suzhou, China
,
pp. 3028–3046
.
External Links:
Document
,
Link
Cited by:
§V-B
.
[36]
X. Jiang, Y. Dong, L. Wang, Z. Fang, Q. Shang, G. Li, Z. Jin, and W. Jiao
(2024)
Self-planning code generation with large language models
.
ACM Transactions on Software Engineering and Methodology
33
(
7
),
pp. 182:1–182:30
.
External Links:
Document
,
Link
Cited by:
§V-B
.
[37]
Y. Fu, B. Li, L. Li, W. Zhang, and T. Xie
(2025)
The first prompt counts the most! an evaluation of large language models on iterative example-based code generation
.
Proceedings of the ACM on Software Engineering
2
(
ISSTA
),
pp. 1583–1606
.
External Links:
Document
,
Link
Cited by:
§V-B
.
[38]
L. Gröninger, B. Souza, and M. Pradel
(2025)
ChangeGuard: validating code changes via pairwise learning-guided execution
.
Proceedings of the ACM on Software Engineering
2
(
FSE
),
pp. 936–956
.
External Links:
Document
Cited by:
§V-C
.
[39]
Z. Wang, Z. Zhou, D. Song, Y. Huang, S. Chen, L. Ma, and T. Zhang
(2025)
Towards understanding the characteristics of code generation errors made by large language models
.
In
Proceedings of the 47th IEEE/ACM International Conference on Software Engineering
,
pp. 2587–2599
.
External Links:
Document
Cited by:
§V-D
.
[40]
A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, A. Desmaison, A. Köpf, E. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang, J. Bai, and S. Chintala
(2019)
PyTorch: an imperative style, high-performance deep learning library
.
In
Advances in Neural Information Processing Systems
,
Vol.
32
.
External Links:
Link
Cited by:
§V-G
.
[41]
T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi, P. Cistac, T. Rault, R. Louf, M. Funtowicz, J. Davison, S. Shleifer, P. von Platen, C. Ma, Y. Jernite, J. Plu, C. Xu, T. L. Scao, S. Gugger, M. Drame, Q. Lhoest, and A. M. Rush
(2020)
Transformers: state-of-the-art natural language processing
.
In
Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations
,
Online
,
pp. 38–45
.
External Links:
Document
,
Link
Cited by:
§V-G
.