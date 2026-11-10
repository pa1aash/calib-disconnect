---
title: 'ExecuCritic: Calibrated Critic Shaping forCode Generation with Verifiable
  Rewards'
id: execucritic-calibrated-critic-shaping-forcode-generation-with-verifiable-rewards
tags:
- code-llm-confidence-positioning-d82d00
- trained-stated-confidence
- cc-1-gapfill
created: '2026-11-10T08:55:12.434933Z'
updated: '2026-11-10T08:58:12.002039Z'
source: https://arxiv.org/html/2609.16604
source_domain: arxiv.org
fetched_at: '2026-11-10T08:55:12.434626Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'ExecuCritic (arXiv 2609.16604, FULL TEXT via arXiv HTML): jointly trains
  a coder and a critic on the same execution rollouts; critic reads prompt plus candidate
  and emits a critique then a verdict token whose pass/fail probability is the calibrated
  score. Table 5 reports critic reliability on validation rollouts (HumanEval+, LiveCodeBench,
  APPS, SWE-bench Lite): ExecuCritic ECE 0.061, Brier 0.137, AUC 72.8 vs frozen prompt
  critic ECE 0.213, AUC 60.4. Backbones Qwen3-8B and DeepSeek-Coder-V2-Lite-Instruct.
  A separate trained pass/fail predictor, not the coder''s own stated confidence;
  no probe, no verbal-versus-probe comparison. Bears on cc-1 gap 1: NARROWS ''trained
  pass/fail estimator on execution labels with calibration and AUC reported''; does
  not trigger pivot 3.'
---

ExecuCritic: Calibrated Critic Shaping forCode Generation with Verifiable Rewards
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2609.16604v1 [cs.SE] 15 Sep 2026
ExecuCritic: Calibrated Critic Shaping for
Code Generation with Verifiable Rewards
Junjie Cao
Affiliation:
Intel Corporation, Beijing, China
E-mail
junjie.cao@intel.com
Yingjie He
Affiliation:
Peking University, Beijing, China
Abstract
Execution feedback is a useful supervision signal for code models because
unit tests are objective and directly measure program correctness. Its
weakness is that an entire program is often reduced to one pass or fail
bit, leaving RLVR to solve a difficult credit assignment problem. At the
same time, coding systems often include separate reviewer or tester
roles, but these critics are usually prompted rather than trained and are
not calibrated against execution. We propose
ExecuCritic
, a joint
training framework in which a coder and a critic are updated on the same
execution rollouts. The critic predicts pass or fail outcomes and gives
short diagnostic feedback; the coder uses this signal only when the
critic agrees with the executor on the current rollout group. Across
eight code benchmarks and two recent open backbones, ExecuCritic improves
over GRPO without a critic, prompted reviewer systems and scalar reward
model baselines, while requiring fewer policy gradient steps and fewer
sandbox executions. Ablations and reliability analyses suggest that the
gains come from better credit assignment rather than larger sampling
budgets.
Keywords:
Code generation Verifiable reward Multi agent
learning Reinforcement learning Critic models.
1
Introduction
Code language models
[
6
]
are increasingly evaluated as software agents rather
than as autocomplete systems
[
49
,
51
]
. In a realistic coding task, a model may
need to understand an issue, modify several files, run tests, read the
resulting trace and revise its patch. This workflow has made execution
feedback especially attractive: a unit test is cheap compared with human
annotation, and its result is directly tied to whether the program works.
Reinforcement learning with verifiable rewards (RLVR) builds on this
property by fine tuning code models with policy gradient methods such as
GRPO
[
38
]
using rewards from sandboxed execution.
Recent code RL systems
[
7
,
43
,
48
,
27
]
show that even binary test feedback can
improve coding and reasoning ability, and parallel work on reward design
for LLM reasoning reports similar gains from denser or better aligned
signals
[
50
,
39
,
22
]
.
A second line of work improves code generation by decomposing the task
into roles. Several systems built around prompting
[
12
,
10
,
13
,
31
]
introduce
programmers, reviewers, testers or debuggers, so that a candidate program
can be checked before it is submitted. The analogy to ordinary software
development is clear: code is reviewed, tested and diagnosed rather than
written once and accepted. However, in most such systems the critic is
only a prompted role. It may produce fluent comments, but it is not
trained to match executor outcomes, and the coder is not trained to know
when those comments should be followed.
The two approaches therefore solve different parts of the problem. RLVR
has a trustworthy verifier, but the learning signal is thin. A long patch
receives the same binary credit on every generated token, even though the
failure may be caused by one branch condition, one API call or one
missing import. This leads to noisy updates whose effect is hard to
attribute to a specific mistake
[
53
,
16
]
, and
often encourages large rollout groups, which are expensive when every
candidate must be executed. Prompted systems with multiple roles provide richer language
feedback, but the feedback is not grounded in the actual executor. A
critic can be confident and wrong, and nothing in the training objective
teaches the coder to discount such advice. This motivates the question we
study in this paper: can execution rewards and learned critiques be
combined so that the critic makes RLVR less sparse without becoming an
untrusted reward model?
We propose
ExecuCritic
, a joint training framework for a coder
agent
π
c
\pi_{c}
and a critic agent
π
v
\pi_{v}
. The two agents share a frozen
backbone and use separate LoRA adapters
[
11
]
, and both are
updated on the same pool of rollouts labelled by execution. For each
prompt, the coder samples candidate programs and a sandbox returns pass
or fail outcomes. The critic predicts these outcomes, ranks passing candidates
above failing ones and produces a short diagnosis tied to the observed
failure type. The coder is then trained with a calibrated advantage: the
standard GRPO signal is augmented with a critic score, but only to the
extent that the critic agrees with the executor within the current
rollout group. When the critic is unreliable, the update falls back
toward ordinary RLVR; when it becomes calibrated, its scores provide a
dense signal for credit assignment.
The critic is also not an extra frozen judge bolted on after training: it
has seen the same evolving distribution of code as the coder, so it can
rank candidates before execution and supply feedback when all of them
fail. In repository repair, where one sandbox call may install
dependencies and run many tests, this ranking cuts expensive executions
without simply enlarging the sampling budget.
We evaluate ExecuCritic with two recent open code backbones on benchmarks
spanning function synthesis, contamination controlled programming, library
use, competitive programming, repository issue resolution, cross-language
editing, patch ranking and test selection. Under matched data and token
budgets it improves over the strongest critic-free RLVR baseline by 3–4
absolute points and over prompted reviewer systems by 6–7, and reaches
that baseline’s final accuracy with roughly
40
%
40\%
fewer policy gradient
steps. Ablations tie the gains to the calibration gate, the pass/fail
margin and the diagnosis consistency objective rather than to extra
sampling.
Contributions.
•
We formulate code agent training as joint optimisation of a coder
and an execution-grounded critic updated on the same RLVR rollouts.
•
We introduce a calibrated advantage that trusts critic scores only
where they agree with executor outcomes, giving denser feedback with
less risk of reward hacking.
•
We train the critic to predict verdicts, rank passing above
failing programs, and diagnose failures from executor traces.
•
We study two backbones and eight benchmark views with ablations,
seed checks, reliability, sample efficiency, budget and failure-type
analyses.
2
Related Work
RL with verifiable rewards for code.
Following recent
work on RLVR for code
[
7
,
43
,
35
,
48
,
27
,
28
]
, a wave of studies has
applied executable feedback to code generation. These systems optimise
patching at repository scale or function synthesis with curated data
augmented by tests. They demonstrate the power of executable
supervision, but they still train a
single
policy against a
single
scalar reward and therefore inherit the sparsity problem
studied in this paper. Related efforts outside code shape the reward
itself rather than the data, by aligning updates with gradient
evidence
[
50
]
, by distributing group relative credit
across reasoning steps
[
39
]
, or by replacing surface
overlap metrics with hierarchical task aware
rewards
[
42
,
22
]
.
Code generation with multiple agents.
A separate line of
work keeps the model frozen and orchestrates several roles through
prompting.
Self-Refine
[
31
]
iterates between generation and
critique with one model; AgentCoder
[
12
]
,
Meta-GPT
[
10
]
, MapCoder
[
13
]
and
AutoGen-Coder
[
45
]
introduce dedicated programmer,
tester and reviewer agents. CodeT
[
2
]
and
Reflexion
[
40
]
similarly use generated tests or
verbal feedback to filter or rewrite candidates. Learned coordination
policies decide which agent or action to invoke instead of fixing the
schedule in advance
[
15
,
33
]
, and similar
role decompositions have been applied to multimodal decision
tasks
[
19
]
. These pipelines benefit
from role decomposition, but their critics are generally frozen and
uncalibrated. ExecuCritic instead trains the critic and coder jointly
under a verifiable reward.
Critic and verifier models.
Process reward
models
[
24
]
and
CriticGPT
[
32
]
demonstrate that critics trained
on labelled traces can rival much larger frozen judges. Outcome reward
models for math and code
[
3
]
extend
this idea to scalar correctness prediction. Analyses of how reasoning
models fail, whether by enumerating an error forest
[
16
]
or by making the reasoning pathway explicit and
controllable
[
4
]
, suggest that a critic benefits
from naming the failure rather than only scoring it. Our work differs in
two key ways: the critic is trained
simultaneously
with the policy whose
outputs it scores, and its score is fed back into the policy gradient
rather than used only during decoding.
Reward shaping and dense feedback.
Reward shaping is a
classical idea in RL
[
34
]
; recent LLM work explores
intrinsic rewards
[
47
]
, learned dense
verifiers
[
41
]
and feedback generated by AI
systems
[
1
]
. When several learning signals
disagree, reweighting them by their mutual consistency is often more
stable than summing them, an idea also used to resolve conflicting client
updates in distributed training
[
9
]
. ExecuCritic can
be viewed as reward shaping grounded by a verifier: the dense bonus is provided by a learned
critic, but the critic itself remains anchored to a verifiable executable
signal, which empirically helps prevent reward hacking.
3
Method
3.1
Problem setup
We study a code generation setting in which a prompt
x
x
(a natural
language specification, a function signature, or a buggy file plus an
issue description) is mapped to a candidate solution
y
y
(a function body
or a unified diff). A black box executor
E
⁡
(
x
,
y
)
∈
{
0
,
1
}
E(x,y)\in\{0,1\}
returns
1
1
iff
y
y
passes all hidden unit tests for
x
x
and
0
0
otherwise. RLVR maximises
the expected execution reward
J
(
π
)
=
𝔼
x
∼
𝒟
𝔼
y
∼
π
(
⋅
∣
x
)
[
E
(
x
,
y
)
]
,
J(\pi)\;=\;\mathbb{E}_{x\sim\mathcal{D}}\,\mathbb{E}_{y\sim\pi(\cdot\mid x)}\bigl[\,E(x,y)\,\bigr],
(1)
typically with GRPO, which draws a group of
K
K
rollouts
{
y
i
}
i
=
1
K
\{y_{i}\}_{i=1}^{K}
for each prompt and computes an advantage
A
i
=
(
R
i
−
μ
R
)
/
σ
R
A_{i}=(R_{i}-\mu_{R})/\sigma_{R}
from rewards normalised within the group,
where
R
i
=
E
⁡
(
x
,
y
i
)
R_{i}=E(x,y_{i})
. The advantage is then used in a clipped policy
gradient update
[
37
]
.
ExecuCritic extends this setup with a second policy
π
v
\pi_{v}
, the
critic
, which receives the prompt and a candidate solution and
produces both a critique in natural language
c
c
and a scalar
score
s
^
∈
[
0
,
1
]
\hat{s}\in[0,1]
. Both
π
c
\pi_{c}
and
π
v
\pi_{v}
are implemented as LoRA
adapters on top of a shared frozen backbone
π
0
\pi_{0}
, so the additional
parameter cost over RLVR with only the coder remains modest. Unlike a
conventional reward model,
π
v
\pi_{v}
is trained on the coder’s evolving
output distribution, encouraging it to recognise the mistakes that the
current coder actually makes.
3.2
Coder and critic architecture
Figure 1:
Pipeline of
ExecuCritic
. Stage 1 cold starts the coder with
SFT and the critic with warm start triplets of prompts, programs, executor
verdicts and distilled critiques. Stage 2 trains both on shared rollouts:
the sandbox gives pass/fail rewards, the critic predicts pass probability
and diagnoses failures, and the coder is updated with a calibrated
advantage. Stage 3 uses the critic at test time to rank candidates, execute
only the top ones, and feed critiques back when all candidates fail.
Figure
1
summarises the training and inference pipeline. The coder
π
c
​
(
y
∣
x
)
\pi_{c}(y\mid x)
is a standard autoregressive policy. The critic
π
v
(
c
,
s
^
∣
x
,
y
)
\pi_{v}(c,\hat{s}\mid x,y)
first emits a short critique in natural
language
c
c
, followed by a special
<verdict>
token whose
probability mass on
pass
/
fail
is read as the calibrated
score
s
^
\hat{s}
. Placing the critique before the verdict provides a mild
form of reasoning regularisation: in our experiments it improves
calibration relative to a direct regression head while preserving
interpretability.
3.3
Calibrated advantage from the critic
The core of ExecuCritic is a modification of the GRPO advantage that
uses the critic’s signal only after checking calibration. For a group
of
K
K
rollouts
{
y
i
}
\{y_{i}\}
with execution rewards
R
i
R_{i}
and critic scores
s
^
i
\hat{s}_{i}
, we define the standardised execution advantage
A
i
=
(
R
i
−
μ
R
)
/
(
σ
R
+
ϵ
)
A_{i}=(R_{i}-\mu_{R})/(\sigma_{R}+\epsilon)
and the standardised critic
advantage
S
i
=
(
s
^
i
−
μ
s
^
)
/
(
σ
s
^
+
ϵ
)
S_{i}=(\hat{s}_{i}-\mu_{\hat{s}})/(\sigma_{\hat{s}}+\epsilon)
.
The resulting advantage is
A
~
i
=
A
i
+
α
​
ρ
K
​
(
R
,
s
^
)
​
S
i
,
\tilde{A}_{i}\;=\;A_{i}\;+\;\alpha\,\rho_{K}\bigl(R,\hat{s}\bigr)\,S_{i},
(2)
where
ρ
K
​
(
R
,
s
^
)
∈
[
−
1
,
1
]
\rho_{K}(R,\hat{s})\in[-1,1]
is the rank correlation within the
group between executor rewards and critic scores, and
α
>
0
\alpha>0
is a
fixed shaping weight. The factor
ρ
K
\rho_{K}
is the key design choice: when
the critic is well calibrated on a particular prompt (
ρ
K
→
1
\rho_{K}\!\to\!1
),
the critic term reinforces the executor signal and spreads it across
rollouts; when the critic is miscalibrated or adversarial
(
ρ
K
≤
0
\rho_{K}\!\leq\!0
), the term collapses or changes direction, preventing
unreliable scores from being treated as trustworthy rewards. This
behaviour stabilises joint training before the critic has fully
converged.
3.4
Critic objective
The critic is updated on the same rollouts. Let
v
i
∈
{
0
,
1
}
v_{i}\in\{0,1\}
be the
verdict token target derived from
R
i
R_{i}
, and let
z
i
z_{i}
denote a compact
failure descriptor obtained from the executor trace when the program
fails (syntax error, assertion mismatch, timeout, import/API error or
runtime exception). We train the critic with a loss that ties its verdict,
relative ordering and textual diagnosis to the executor feedback:
ℒ
v
=
\displaystyle\mathcal{L}_{v}=
−
𝔼
i
​
[
log
⁡
π
v
​
(
v
i
∣
x
,
y
i
)
]
\displaystyle-\mathbb{E}_{i}\bigl[\log\pi_{v}(v_{i}\mid x,y_{i})\bigr]
+
β
​
𝔼
(
i
+
,
i
−
)
​
[
max
⁡
(
0
,
m
−
(
s
^
i
+
−
s
^
i
−
)
)
]
\displaystyle+\beta\,\mathbb{E}_{(i^{+},i^{-})}\!\Bigl[\max\!\bigl(0,\,m-(\hat{s}_{i^{+}}-\hat{s}_{i^{-}})\bigr)\Bigr]
+
γ
𝔼
i
:
R
i
=
0
[
−
log
π
v
(
z
i
∣
x
,
y
i
)
]
.
\displaystyle+\gamma\,\mathbb{E}_{i:R_{i}=0}\bigl[-\log\pi_{v}(z_{i}\mid x,y_{i})\bigr].
(3)
The first term is the likelihood of the executor verdict. The hinge term
is used only for rollout groups that contain at least one passing program
i
+
i^{+}
and one failing program
i
−
i^{-}
; it asks the critic to score the
passing program at least
m
m
higher. The last term is applied to failed
rollouts and trains the critique to match the failure type extracted from
the executor trace. In practice, the hinge term avoids a nearly constant
verdict score, and the diagnosis term makes the feedback useful when the
coder resamples during inference.
3.5
Coder objective
The coder is optimised with a clipped PPO/GRPO surrogate using the
advantage in Eq. (
2
):
ℒ
c
=
−
𝔼
i
∑
t
min
[
r
i
,
t
A
~
i
,
clip
(
r
i
,
t
,
1
−
ε
,
1
+
ε
)
A
~
i
]
+
λ
KL
(
π
c
∥
π
ref
)
,
\mathcal{L}_{c}\!=\!-\mathbb{E}_{i}\!\!\sum_{t}\!\!\min\!\Bigl[\,r_{i,t}\,\tilde{A}_{i},\;\mathrm{clip}(r_{i,t},1{-}\varepsilon,1{+}\varepsilon)\,\tilde{A}_{i}\Bigr]+\lambda\,\mathrm{KL}\bigl(\pi_{c}\,\|\,\pi_{\text{ref}}\bigr),
(4)
where
r
i
,
t
=
π
c
​
(
y
i
,
t
∣
x
,
y
i
,
<
t
)
/
π
c
,
old
​
(
y
i
,
t
∣
x
,
y
i
,
<
t
)
r_{i,t}=\pi_{c}(y_{i,t}\mid x,y_{i,<t})/\pi_{c,\text{old}}(y_{i,t}\mid x,y_{i,<t})
is the importance ratio and
π
ref
\pi_{\text{ref}}
is the SFT checkpoint used
as a reference. The KL term, set with
λ
\lambda
small but nonzero,
prevents the coder from drifting into degenerate styles that the
critic happens to overrate.
3.6
Training pipeline
ExecuCritic is implemented in three stages.
Stage 1: SFT initialisation.
We fine tune the coder with supervision on a mixture of OSS-Instruct
[
44
]
and Evol-Code
[
30
]
until
it reliably produces outputs that compile and can be tested. The critic
is initialised on triplets
(
x
,
y
,
v
,
z
)
(x,y,v,z)
, where
v
v
is the executor verdict
and
z
z
is either a distilled critique from a stronger teacher
(
e.g.
DeepSeek-V3) or a normalised failure descriptor from
the executor trace. This stage requires only a few thousand examples and
avoids learning diagnostic language entirely from scratch.
Stage 2: Joint RLVR.
On each prompt we draw
K
=
8
K{=}8
coder rollouts, score them with both the executor and the
current critic, and apply Eqs. (
2
)–(
4
).
The two LoRA adapters are updated sequentially within each optimiser
step: first the critic, then the coder using calibrated advantages
computed from the same rollout-level critic scores, while sharing the
rollouts and the frozen backbone. Algorithm
1
gives the full
procedure.
Stage 3: Refinement at inference.
At inference, the coder produces
N
N
candidates; the critic ranks them,
and only the top
k
k
are executed in the sandbox. If none passes, the
critic’s textual critique on the failure with the highest score is fed
back to the coder as additional context, and a new round of
N
N
candidates
is sampled. We cap the loop at
T
T
rounds. Because critic scoring requires
a single forward pass whereas sandbox execution can take seconds, ranking
with the critic substantially reduces running time relative to executing
all sampled candidates.
Algorithm 1
ExecuCritic joint training (one outer iteration)
1:
dataset
𝒟
\mathcal{D}
, executor
E
E
, coder
π
c
\pi_{c}
, critic
π
v
\pi_{v}
, group size
K
K
2:
for
minibatch of prompts
{
x
(
b
)
}
⊂
𝒟
\{x^{(b)}\}\subset\mathcal{D}
do
3:
for
each prompt
x
x
do
4:
Sample
K
K
rollouts
{
y
i
}
∼
π
c
(
⋅
∣
x
)
\{y_{i}\}\sim\pi_{c}(\cdot\mid x)
5:
Compute executor rewards and failure descriptors
(
R
i
,
z
i
)
←
E
⁡
(
x
,
y
i
)
(R_{i},z_{i})\!\leftarrow\!E(x,y_{i})
6:
Compute critic scores, critiques and verdict logits with
π
v
(
⋅
∣
x
,
y
i
)
\pi_{v}(\cdot\mid x,y_{i})
7:
Compute
A
i
A_{i}
,
S
i
S_{i}
and the rank correlation
ρ
K
​
(
R
,
s
^
)
\rho_{K}(R,\hat{s})
8:
Form calibrated advantage
A
~
i
←
A
i
+
α
​
ρ
K
​
S
i
\tilde{A}_{i}\leftarrow A_{i}+\alpha\,\rho_{K}\,S_{i}
9:
end
for
10:
Update
π
v
\pi_{v}
with
ℒ
v
\mathcal{L}_{v}
from Eq. (
3
)
11:
Update
π
c
\pi_{c}
with
ℒ
c
\mathcal{L}_{c}
from Eq. (
4
) using
A
~
i
\tilde{A}_{i}
12:
end
for
4
Experiments
4.1
Setup
Backbones.
We use
Qwen3-8B
[
46
]
as
the headline backbone and
DeepSeek-Coder-V2-Lite-Instruct
(16B MoE,
∼
2.4
{\sim}2.4
B active)
[
54
]
to check that the result carries
across architectures, plus the smaller Qwen3-4B in scaling ablations. All
training uses rank-
32
32
LoRA adapters on attention and MLP projections with
the backbone frozen, in bf16 with gradient checkpointing.
Benchmarks.
We evaluate on eight benchmark views covering
increasingly difficult forms of code intelligence.
HumanEval+
and
MBPP+
[
26
]
test short function synthesis
with strengthened unit tests.
LiveCodeBench
v5
[
14
]
measures competitive programming with contamination controls.
BigCodeBench-Hard
[
55
]
stresses library
use, long instructions and reasoning over multiple calls.
APPS
[
8
]
and
CodeContests
[
23
]
cover longer contest-style programs with more
ambiguous intermediate credit.
SWE-bench Lite
[
17
]
evaluates issue resolution at repository scale on 300 real GitHub tasks.
Multi-SWE-bench
evaluates repository repair across Python and
Java subsets. We further include a
SWE-bench Verified ranking
view, where the critic ranks a small set of candidate patches before
execution, and a view for selecting which generated tests should be
trusted as auxiliary verifiers. Function synthesis benchmarks report
unbiased pass@1 with greedy decoding; repository benchmarks report
resolved issue rate; ranking views report NDCG@5 and AUC.
Training data.
The initial SFT stage uses a
mixture of 75 k examples from OSS-Instruct
[
44
]
and
Evol-Code-Alpaca, filtered to keep examples that compile in the sandbox.
RLVR prompts are drawn from the train splits of the Code Contests
corpus
[
23
]
, the SWE-Gym training set
[
35
]
,
a 30 k prompt subset of APPS
[
8
]
, and a 12 k
subset of repository edits whose tests run in Docker within 120 seconds.
We deduplicate against all evaluation benchmarks at the prompt level using
MinHash with Jaccard threshold
0.7
0.7
, and remove near duplicate function
signatures by exact AST normalisation. Critic failure descriptors are
normalised into seven categories: syntax, import/API, type, assertion,
timeout, runtime exception and unknown.
Baselines.
We compare ExecuCritic with:
(B1)
the
base backbone without task training;
(B2)
a coder trained only
with SFT;
(B3)
RLVR with a single coder, using vanilla GRPO and
executor rewards to reproduce the SWE-RL/AceCoder recipe;
(B4)
a prompted system with a frozen coder and frozen critic in
the style of AgentCoder;
(B5)
Self-Refine
[
31
]
with the same coder;
(B6)
trained critic reranking, with the coder
left at the SFT checkpoint;
(B7)
execution of all sampled
candidates across refinement rounds; and
(B8)
outcome reward model
shaping, which replaces the textual diagnosis with a scalar reward model.
Trained baselines (B2, B3, B6, B8) share our backbone, prompts and token
budget; prompted ones (B1, B4, B5, B7) reuse the backbone untrained. B3
uses
K
=
16
K{=}16
rollouts to match or exceed our training-time sandbox calls.
Hyperparameters.
Unless stated otherwise we use
K
=
8
K{=}8
rollouts per prompt,
α
=
0.5
\alpha{=}0.5
,
β
=
0.5
\beta{=}0.5
,
γ
=
0.2
\gamma{=}0.2
, margin
m
=
0.2
m{=}0.2
, PPO clipping
ε
=
0.2
\varepsilon{=}0.2
, KL coefficient
λ
=
0.01
\lambda{=}0.01
, learning rate
×
10
−
6
5\!\times\!10^{-6}
for both adapters, batch size
128
128
, and a total
of
400
400
RLVR steps. At inference we use
N
=
8
N{=}8
,
k
=
3
k{=}3
,
T
=
3
T{=}3
for
the loop that refines candidates after failed execution. For repository
tasks, each candidate is allowed at most 120 seconds of test execution
and 16k input tokens.
4.2
Main results
Table 1:
Function synthesis and programming benchmarks (pass@1, %), with a
shared backbone and training budget. Best in bold, second best underlined.
HE+, MBPP+, LCB and BCB-H are HumanEval+, MBPP+, LiveCodeBench and
BigCodeBench-Hard.
Method (Qwen3-8B)
HE+
MBPP+
LCB
BCB-H
APPS
CC
Avg.
B1 Base direct
71.3
65.8
24.7
28.1
19.4
18.8
38.0
B2 SFT only
74.6
68.4
26.2
30.0
21.1
20.5
40.1
B4 Prompted reviewer system
75.9
69.5
27.0
31.2
22.0
21.4
41.2
B5 Self-Refine
76.2
70.0
27.6
31.6
22.4
21.9
41.6
B6 Trained critic rerank
77.4
71.2
28.3
32.4
23.0
22.5
42.5
B7 Execute all samples
79.8
73.0
30.4
34.0
24.7
24.0
44.3
B3 RLVR with one coder
80.5
73.6
30.9
34.5
25.2
24.6
44.9
Ours: ExecuCritic
84.2
77.0
34.1
37.8
28.8
28.0
48.3
Method (DS-Coder-V2-Lite)
HE+
MBPP+
LCB
BCB-H
APPS
CC
Avg.
B3 RLVR with one coder
82.1
74.8
31.5
35.8
26.0
25.4
45.9
Ours: ExecuCritic
85.6
77.9
34.7
38.6
29.5
28.7
49.2
Table 2:
Repository tasks and critic evaluation. Repair columns report
resolve rate; Rank and Test-AUC report NDCG@5 and AUC; Exec. is sandbox
calls per solved instance.
Method (Qwen3-8B)
SWE-Lite
MSB-Py
MSB-Java
Rank
Test-AUC
Exec.
B2 SFT only
9.7
8.2
5.9
42.5
57.1
17.8
B4 Prompted reviewer system
11.0
9.1
6.4
48.8
60.4
16.9
B5 Self-Refine
11.7
9.6
6.8
50.2
61.0
16.1
B6 Trained critic rerank
12.4
10.0
7.1
59.6
67.5
13.4
B7 Execute all samples
14.0
11.3
7.9
–
–
24.0
B3 RLVR with one coder
14.6
11.7
8.3
55.8
64.2
18.6
Ours: ExecuCritic
18.3
14.4
10.6
66.9
72.8
10.7
Tables
1
and
2
report the main results. On
Qwen3-8B, ExecuCritic improves over RLVR with a single coder by
+
3.4
+3.4
average points across the six function and programming benchmarks and by
+
3.7
+3.7
on SWE-bench Lite; on DeepSeek-Coder-V2-Lite the margin remains
+
3.3
+3.3
, so the gain is not an artefact of a weak baseline. The critic also
raises patch ranking NDCG@5 by
+
11.1
+11.1
and cuts sandbox executions per
solved task from
18.6
18.6
to
10.7
10.7
.
The gains are largest on
LiveCodeBench
,
APPS
,
CodeContests
and
SWE-bench Lite
, where generations are
longer and credit assignment is noisier. Prompted reviewer and
Self-Refine baselines remain below RLVR with a single coder, indicating
that role decomposition alone is insufficient; the critic must be
calibrated and trained with the coder.
4.3
Statistical robustness
Table 3:
Robustness of the Qwen3-8B headline comparison: mean
±
\pm
standard
deviation over three RLVR seeds, with a paired bootstrap 95% confidence
interval for the gain over RLVR with a single coder.
Evaluation
B3 RLVR
ExecuCritic
Gain
95% CI
HumanEval+ pass@1
80.5
±
0.8
80.5{\pm}0.8
84.2
±
0.6
84.2{\pm}0.6
+
3.7
+3.7
[
+
2.4
,
+
5.0
]
[+2.4,+5.0]
MBPP+ pass@1
73.6
±
0.7
73.6{\pm}0.7
77.0
±
0.5
77.0{\pm}0.5
+
3.4
+3.4
[
+
2.1
,
+
4.6
]
[+2.1,+4.6]
LiveCodeBench pass@1
30.9
±
0.6
30.9{\pm}0.6
34.1
±
0.7
34.1{\pm}0.7
+
3.2
+3.2
[
+
1.8
,
+
4.5
]
[+1.8,+4.5]
BigCodeBench-Hard pass@1
34.5
±
0.7
34.5{\pm}0.7
37.8
±
0.6
37.8{\pm}0.6
+
3.3
+3.3
[
+
2.0
,
+
4.7
]
[+2.0,+4.7]
SWE-bench Lite resolve
14.6
±
0.8
14.6{\pm}0.8
18.3
±
0.9
18.3{\pm}0.9
+
3.7
+3.7
[
+
1.9
,
+
5.5
]
[+1.9,+5.5]
SWE-bench ranking NDCG@5
55.8
±
1.0
55.8{\pm}1.0
66.9
±
1.2
66.9{\pm}1.2
+
11.1
+11.1
[
+
8.4
,
+
13.8
]
[+8.4,+13.8]
Table
3
checks whether the gains fall within normal RLVR
variability. Across three seeds, all paired confidence intervals exclude
zero, and ExecuCritic shows slightly lower variance on short programming
benchmarks. The widest interval occurs on SWE-bench Lite because only
300 repository issues are evaluated, but its lower bound remains above
+
1.9
+1.9
points, making a seed artefact unlikely.
4.4
Ablation study
Table 4:
Ablation on Qwen3-8B: average pass@1 over
HE+/MBPP+/LCB/BCB-H/APPS/CC, and SWE-bench Lite resolve rate. Bold marks
the default setting;
K
=
16
K{=}16
doubles the training sandbox budget.
Variant
Avg. pass@1
SWE-Lite
Full ExecuCritic (default)
48.3
18.3
α
=
0
\alpha{=}0
(no critic shaping)
45.2
15.0
no calibration gate (
ρ
K
=
1
\rho_{K}\!=\!1
)
46.0
15.8
β
=
0
\beta{=}0
(no pass/fail margin)
46.3
16.1
γ
=
0
\gamma{=}0
(no critique consistency)
46.7
16.4
reward model with scalar score
46.5
16.0
no shared backbone
46.9
16.7
staged critic then coder
46.2
15.9
K
=
4
K{=}4
rollouts
46.1
15.7
K
=
16
K{=}16
rollouts
48.5
18.5
T
=
1
T{=}1
inference refinement
46.9
16.8
Table
4
shows that no single component explains the whole
gain. Removing critic shaping nearly reverts to RLVR, while a constant
trust weight (
ρ
K
=
1
\rho_{K}\!=\!1
) hurts when early critic scores are wrong.
Dropping the pass/fail margin weakens discrimination, and dropping critique
consistency weakens inference-time refinement; the scalar reward model
behaves similarly, so textual diagnosis matters when tied to executor
failure types. Sharing the backbone helps but is not decisive, and staged
training loses more, supporting joint updates on one rollout distribution.
Raising
K
K
to 16 gains little while doubling sandbox cost, so we use
K
=
8
K{=}8
,
T
=
3
T{=}3
.
4.5
Sample efficiency and reward density analysis
steps
pass@1
(a) sample
efficiency
ExecuCritic
RLVR without critic
0
200
400
steps
variance
(b) advantage
variance
A
~
\tilde{A}
A
A
steps
ρ
K
\rho_{K}
(c) critic
calibration
Spearman
AUC
Figure 2:
Sample efficiency and reward density.
(a)
Pass@1 vs. GRPO
steps; ExecuCritic reaches the final RLVR accuracy after about 240 steps.
(b)
Advantage variance within rollout groups.
(c)
Critic
calibration (Spearman correlation and pass/fail AUC) during joint training.
Figure
2
reports three diagnostics. ExecuCritic reaches the
final accuracy of RLVR with a single coder after roughly
60
%
60\%
of the
policy-gradient steps. Its advantage estimate also becomes less noisy
once
ρ
K
\rho_{K}
exceeds
∼
0.4
{\sim}0.4
, giving a more informative gradient.
Meanwhile, the rank correlation between critic scores and executor
outcomes rises from
0.18
0.18
after SFT to
0.71
0.71
at convergence, suggesting
that the critic learns execution correctness rather than coder style.
4.6
Critic reliability analysis
Table 5:
Reliability of critic variants on validation rollouts. ECE and
Brier measure calibration (lower is better), AUC and Spearman measure
pass/fail discrimination, and Type-F1 measures agreement between the
diagnosed failure type and the executor descriptor.
Critic variant
ECE
↓
\downarrow
Brier
↓
\downarrow
AUC
↑
\uparrow
Spearman
↑
\uparrow
Type-F1
↑
\uparrow
Frozen prompt critic
0.213
0.246
60.4
0.31
38.2
Trained critic reranker
0.124
0.184
67.5
0.52
53.0
Reward model with scalar score
0.108
0.171
68.9
0.54
–
ExecuCritic critic
0.061
0.137
72.8
0.71
64.6
Table
5
makes the calibration claim more explicit.
We compute ECE on validation rollouts from HumanEval+, LiveCodeBench,
APPS and SWE-bench Lite, and Type-F1 only on failed candidates with a
normalised executor descriptor. A frozen prompt critic is fluent but
often over-predicts pass outcomes on plausible wrong programs. Reranking
training improves discrimination, but joint learning further improves
calibration and diagnostic faithfulness. The scalar reward model obtains
reasonable scores but lacks failure-type diagnoses, explaining its weaker
refinement performance in Table
4
.
4.7
Execution budget and scaling
Table 6:
Accuracy versus cost under fixed inference sandbox budgets on
Qwen3-8B: average pass rate over HE+/MBPP+/LCB/BCB-H/APPS/CC given the
number of executions in the column header. This budget is distinct from
the training rollout group size
K
K
.
Method
2
4
8
16
24
Prompted reviewers
39.8
40.7
41.2
41.6
41.8
Self-Refine
40.1
41.0
41.6
42.0
42.2
Trained critic rerank
41.5
42.2
42.5
43.0
43.2
Best of
N
N
execution
40.9
42.6
44.3
45.0
45.4
RLVR without critic
43.2
44.1
44.9
44.9
45.0
ExecuCritic
45.8
47.2
48.3
48.5
48.7
Table
6
fixes the maximum sandbox executions at inference.
ExecuCritic dominates the Pareto frontier: with two executions per prompt
it exceeds RLVR with a single coder using eight executions, and with
eight executions it surpasses exhaustive execution of 24 candidates. This
matters most for repository repair, where each sandbox call may require
dependency installation and full test execution.
Table 7:
Execution budget and backbone scaling. Pass@1 is averaged over
HE+/MBPP+/LCB/BCB-H/APPS/CC. Exec. denotes average sandbox calls per
prompt at inference.
Backbone / method
Params
Exec.
Avg. pass@1
SWE-Lite
Qwen3-4B + RLVR without critic
4B
16.0
39.7
10.8
Qwen3-4B + ExecuCritic
4B
7.2
43.1
13.9
Qwen3-8B + RLVR without critic
8B
16.0
44.9
14.6
Qwen3-8B + ExecuCritic
8B
7.5
48.3
18.3
DS-Coder-V2-Lite + RLVR without critic
16B MoE
16.0
45.9
15.4
DS-Coder-V2-Lite + ExecuCritic
16B MoE
7.9
49.2
19.1
Table
7
shows that ExecuCritic is not simply buying
accuracy with more sampling. Across all three backbones, it uses less
than half as many sandbox calls as executing all
N
N
candidates while
improving pass@1 and repository resolve rate. The relative gain is
slightly larger for Qwen3-4B, where the coder makes more detectable local
mistakes.
4.8
Case study by bug type
Table 8:
Failure types on a stratified 250 problem subset of LiveCodeBench
and APPS. Cells give the fraction of problems failing with that bug type
(%, lower is better); rows do not sum to 100, since a solved problem is
assigned no failure type.
Failure type
B2
B4
B5
B3
Ours
Boundary / index error
18.4
16.9
15.6
14.0
10.2
Import or wrong API
14.1
11.5
10.8
9.7
6.4
Type / numerical precision
9.8
9.2
8.7
7.6
5.5
Assertion mismatch
20.6
19.4
18.9
16.8
13.9
Runtime exception
8.5
7.9
7.5
6.7
4.8
Timeout / complexity
7.2
6.9
6.6
6.1
4.7
Deep logic / algorithmic
22.7
21.0
20.6
18.3
15.1
To examine
which
errors the critic helps fix, we label each error
on a stratified 250-problem subset of LiveCodeBench and APPS, using the
taxonomy of
[
14
,
16
]
and our executor
descriptors.
Table
8
reports the remaining error rate by failure
type. RLVR with a single coder removes many easy bugs but struggles with
deep logic mistakes and rarer runtime failures. ExecuCritic improves all
seven categories, with the largest relative gains on
import/API
(
−
34
%
-34\%
),
runtime exception
(
−
28
%
-28\%
) and
type/numerical
(
−
28
%
-28\%
) errors, which the critic also flags most
reliably in its textual outputs.
4.9
Discussion and limitations
ExecuCritic inherits two limitations of RLVR. First, it needs an executable
test oracle per training prompt; refactoring or documentation would require
synthetic verifiers or a learned test generator. Second, although
ρ
K
\rho_{K}
in Eq. (
2
) limits badly calibrated critic rewards,
weak or out-of-distribution backbones may need a longer SFT phase. We saw
no reward hacking, plausibly because the critic is anchored to executor
verdicts, but adversarial initial critics deserve study, since agents can
be steered by inputs crafted to look
benign
[
36
,
29
]
.
5
Conclusion
We presented ExecuCritic, a joint reinforcement learning framework in which
a coder and an execution-grounded critic share a backbone and are updated
together under verifiable rewards. A calibrated advantage makes sparse RLVR
feedback denser, while critic ranking and failure diagnosis stabilise
training and support efficient inference. Across eight benchmark views and
two open backbones it beats strong RLVR, prompted reviewer, self-refinement
and scalar reward model baselines using fewer policy-gradient steps and
sandbox executions, and our analyses indicate that learning a calibrated
critic alongside the coder is a useful inductive bias. Future work includes
tasks without test oracles, sparse expert backbones, process reward models,
progressively trained smaller backbones
[
25
]
, domains
with weaker verifiers
[
20
,
18
,
52
]
,
and keeping the critic calibrated as the coder
drifts
[
5
,
21
]
.
References
[1]
Y. Bai S. Kadavath
et al.
(2022)
Constitutional ai: harmlessness from ai feedback
.
arXiv:2212.08073
.
Cited by:
§2
.
[2]
B. Chen F. Zhang
et al.
(2022)
Codet: code generation with generated tests
.
arXiv:2207.10397
.
Cited by:
§2
.
[3]
K. Cobbe V. Kosaraju
et al.
(2021)
Training verifiers to solve math word problems
.
arXiv:2110.14168
.
Cited by:
§2
.
[4]
H. Dong K. Jiang
et al.
(2026)
NeuReasoner: towards explainable, controllable, and unified reasoning via mixture-of-neurons
.
In
Proc. ACL
,
Cited by:
§2
.
[5]
Y. Feng H. Wang
et al.
(2026)
FOREVER: forgetting curve-inspired memory replay for language model continual learning
.
In
Proc. ACL
,
Cited by:
§5
.
[6]
A. Grattafiori A. Dubey
et al.
(2024)
The llama 3 herd of models
.
arXiv:2407.21783
.
Cited by:
§1
.
[7]
D. Guo D. Yang
et al.
(2025)
Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning
.
arXiv:2501.12948
.
Cited by:
§1
,
§2
.
[8]
D. Hendrycks S. Basart
et al.
(2021)
Measuring coding challenge competence with apps
.
arXiv:2105.09938
.
Cited by:
§4.1
,
§4.1
.
[9]
M. Hong Z. Lin
et al.
(2026)
Conflict-aware client selection for multi-server federated learning
.
In
Proc. ICASSP
,
Cited by:
§2
.
[10]
S. Hong M. Zhuge
et al.
(2024)
MetaGPT: meta programming for a multi-agent collaborative framework
.
In
Proc. ICLR
,
Cited by:
§1
,
§2
.
[11]
E. J. Hu Y. Shen
et al.
(2022)
Lora: low-rank adaptation of large language models.
.
Proc. ICLR
.
Cited by:
§1
.
[12]
D. Huang J. M. Zhang
et al.
(2023)
Agentcoder: multi-agent-based code generation with iterative testing and optimisation
.
arXiv:2312.13010
.
Cited by:
§1
,
§2
.
[13]
M. A. Islam M. E. Ali
et al.
(2024)
Mapcoder: multi-agent code generation for competitive problem solving
.
In
Proc. ACL
,
Cited by:
§1
,
§2
.
[14]
N. Jain A. Gu
et al.
(2025)
Livecodebench: holistic and contamination free evaluation of large language models for code
.
In
Proc. ICLR
,
Cited by:
§4.1
,
§4.8
.
[15]
E.H. Jiang L. Li
et al.
(2026)
Agent q-mix: selecting the right action for llm multi-agent systems through reinforcement learning
.
In
Proc. COLM
,
Cited by:
§2
.
[16]
K. Jiang H. Dong
et al.
(2026)
FoE: forest of errors makes the first solution the best in large reasoning models
.
In
Proc. ACL
,
Cited by:
§1
,
§2
,
§4.8
.
[17]
C. E. Jimenez J. Yang
et al.
(2024)
Swe-bench: can language models resolve real-world github issues?
.
In
Proc. ICLR
,
Cited by:
§4.1
.
[18]
Z. Kang H. Cai
et al.
(2025)
JurisCTC: enhancing legal judgment prediction via cross-domain transfer and contrastive learning
.
In
Proc. IJCNN
,
Cited by:
§5
.
[19]
Z. Kang J. Gong
et al.
(2026)
Multimodal multi-agent empowered legal judgment prediction
.
In
Proc. ICASSP
,
Cited by:
§2
.
[20]
Z. Kang J. Gong
et al.
(2026)
QuantEval: a benchmark for financial quantitative tasks in large language models
.
arXiv:2601.08689
.
Cited by:
§5
.
[21]
Z. Kang Y. He
et al.
(2026)
How order-sensitive are llms? orderprobe for deterministic structural reconstruction
.
In
Findings of EMNLP
,
Cited by:
§5
.
[22]
Z. Kang Y. Liu
et al.
(2026)
JPO: juris policy optimization for structured legal reasoning in criminal judgment prediction
.
In
Proc. EMNLP
,
Cited by:
§1
,
§2
.
[23]
Y. Li D. Choi
et al.
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
Cited by:
§4.1
,
§4.1
.
[24]
H. Lightman V. Kosaraju
et al.
(2024)
Let’s verify step by step
.
In
Proc. ICLR
,
Cited by:
§2
.
[25]
J. Liu and Z. Kang
(2026)
ReasonAct: progressive training for fine-grained video reasoning in small models
.
In
Proc. AAAI
,
Cited by:
§5
.
[26]
J. Liu C. S. Xia
et al.
(2023)
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
NeurIPS
36
,
pp. 21558–21572
.
Cited by:
§4.1
.
[27]
J. Liu and L. Zhang
(2025)
Code-r1: reproducing r1 for code with reliable rewards
.
arXiv:2503.18470
.
Cited by:
§1
,
§2
.
[28]
Y. Liu L. L. Zhang
et al.
(2026)
RStar-coder: scaling competitive code reasoning with a large-scale verified dataset
.
NeurIPS
38
,
pp. 58780–58807
.
Cited by:
§2
.
[29]
X. Lou J. Xu
et al.
(2026)
When helpers become hazards: a benchmark for analyzing multimodal llm-powered safety in daily life
.
In
Findings of ACL
,
Cited by:
§4.9
.
[30]
Z. Luo C. Xu
et al.
(2024)
Wizardcoder: empowering code large language models with evol-instruct
.
In
Proc. ICLR
,
Cited by:
§3.6
.
[31]
A. Madaan N. Tandon
et al.
(2023)
Self-refine: iterative refinement with self-feedback
.
NeurIPS
36
,
pp. 46534–46594
.
Cited by:
§1
,
§2
,
§4.1
.
[32]
N. McAleese R. M. Pokorny
et al.
(2024)
Llm critics help catch llm bugs
.
arXiv:2407.00215
.
Cited by:
§2
.
[33]
C. Meng P. Feng
et al.
(2026)
Group cognition learning: making everything better through governed two-stage agents collaboration
.
In
Proc. ICML
,
Cited by:
§2
.
[34]
A. Y. Ng D. Harada
et al.
(1999)
Policy invariance under reward transformations: theory and application to reward shaping
.
In
Proc. ICML
,
Cited by:
§2
.
[35]
J. Pan X. Wang
et al.
(2024)
Training software engineering agents and verifiers with swe-gym
.
arXiv:2412.21139
.
Cited by:
§2
,
§4.1
.
[36]
J. Qian and Z. Kang
(2026)
Penny wise, pixel foolish: bypassing price constraints in multimodal agents via visual adversarial perturbations
.
In
Findings of ACL
,
Cited by:
§4.9
.
[37]
J. Schulman F. Wolski
et al.
(2017)
Proximal policy optimization algorithms
.
arXiv:1707.06347
.
Cited by:
§3.1
.
[38]
Z. Shao P. Wang
et al.
(2024)
Deepseekmath: pushing the limits of mathematical reasoning in open language models
.
arXiv:2402.03300
.
Cited by:
§1
.
[39]
Q. Shi Z. Kang
et al.
(2026)
SPADER: step-wise peer advantage with diversity-aware exploration rewards for multi-answer question answering
.
In
Proc. EMNLP
,
Cited by:
§1
,
§2
.
[40]
N. Shinn F. Cassano
et al.
(2023)
Reflexion: language agents with verbal reinforcement learning
.
NeurIPS
36
,
pp. 8634–8652
.
Cited by:
§2
.
[41]
P. Wang L. Li
et al.
(2024)
Math-shepherd: verify and reinforce llms step-by-step without human annotations
.
In
Proc. ACL
,
Cited by:
§2
.
[42]
Y. Wang S. Gao
et al.
(2026)
Beyond n-grams: a hierarchical reward learning framework for clinically-aware medical report generation
.
In
Proc. AAAI
,
Cited by:
§2
.
[43]
Y. Wei O. Duchenne
et al.
(2026)
Swe-rl: advancing llm reasoning via reinforcement learning on open software evolution
.
NeurIPS
38
,
pp. 78500–78525
.
Cited by:
§1
,
§2
.
[44]
Y. Wei Z. Wang
et al.
(2023)
Magicoder: empowering code generation with oss-instruct
.
arXiv:2312.02120
.
Cited by:
§3.6
,
§4.1
.
[45]
Q. Wu G. Bansal
et al.
(2024)
Autogen: enabling next-gen llm applications via multi-agent conversations
.
In
Proc. COLM
,
Cited by:
§2
.
[46]
A. Yang A. Li
et al.
(2025)
Qwen3 technical report
.
arXiv:2505.09388
.
Cited by:
§4.1
.
[47]
W. Yuan R. Y. Pang
et al.
(2024)
Self-rewarding language models
.
arXiv:2401.10020
.
Cited by:
§2
.
[48]
H. Zeng D. Jiang
et al.
(2025)
Acecoder: acing coder rl via automated test-case synthesis
.
In
Proc. ACL
,
Cited by:
§1
,
§2
.
[49]
P. Zhao G. Liu
et al.
(2026)
MAS-bench: a unified benchmark for shortcut-augmented hybrid mobile gui agents
.
In
Proc. ACL
,
Cited by:
§1
.
[50]
L. Zheng J. Su
et al.
(2026)
Gradients know what outcomes don’t: unlocking reinforcement learning for llm reasoning with gradient-aligned rewards
.
In
Proc. EMNLP
,
Cited by:
§1
,
§2
.
[51]
L. Zheng J. Su
et al.
(2026)
SciLENS: rl-driven autonomous agents for scientific localized evidence navigation and synthesis
.
In
Proc. EMNLP
,
Cited by:
§1
.
[52]
L. Zheng J. Zhang
et al.
(2026)
What should i cite? a rag benchmark for academic citation prediction
.
In
Proc. WWW
,
Cited by:
§5
.
[53]
C. Zhu S. Wu
et al.
(2026)
EDIS: diagnosing llm reasoning via entropy dynamics
.
arXiv:2602.01288
.
Cited by:
§1
.
[54]
Q. Zhu D. Guo
et al.
(2024)
Deepseek-coder-v2: breaking the barrier of closed-source models in code intelligence
.
arXiv:2406.11931
.
Cited by:
§4.1
.
[55]
T. Y. Zhuo M. C. Vu
et al.
(2025)
Bigcodebench: benchmarking code generation with diverse function calls and complex instructions
.
In
Proc. ICLR
,
Cited by:
§4.1
.