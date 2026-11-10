---
title: Latent Programming Horizons in Coding Agents
id: latent-programming-horizons-in-coding-agents
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
created: '2026-11-09T23:12:34.449365Z'
updated: '2026-11-09T23:27:44.752532Z'
source: https://arxiv.org/html/2607.05188
source_domain: arxiv.org
fetched_at: '2026-11-09T23:12:34.448743Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: FULL TEXT (arXiv 2607.05188, Silva, Tu, Monperrus, KTH). Logistic-regression
  probes on residual streams of Qwen3.6-35B-A3B and Laguna-XS.2 under mini-swe-agent
  decode parses/passes-tests/reduces-failing-tests/regression with AUC up to 0.83
  on SWE-Bench Verified and Pro; future-edit outcome predictable up to ~25 steps ahead.
  No verbal or sampled readout comparison, no ECE, no causal steering (Limitations).
  Close citer of Ribeiro; probe-on-code at agent-step granularity.
---

Latent Programming Horizons in Coding Agents
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY-SA 4.0
arXiv:2607.05188v1 [cs.LG] 06 Jul 2026
Latent Programming Horizons in Coding Agents
André Silva
Affiliation:
KTH Royal Institute of Technology
Han Tu
Affiliation:
Stockholm, Sweden
Martin Monperrus
Affiliation:
{andreans, htu, monperrus}@kth.se
Abstract
A coding agent solving a software-engineering task spends dozens of steps reasoning, editing code, and running tests, yet little is known about what the underlying language model internally represents about the program it is working on.
We show that the residual streams of language models under coding agents linearly encode properties of the evolving program: a logistic-regression probe on hidden states is able to decode whether the current code parses, passes its test suite, reduces the number of failing tests, and introduces regressions, reaching AUC up to
0.83
0.83
for correctness across two models and two benchmarks.
Our second finding is more surprising: these representations run ahead of the agent’s own edits.
Probes trained to predict the outcome of future edits (before they are materialized and written on disk) achieve performance above chance up to roughly 25 steps in advance.
We call this the agent’s
latent programming horizon
.
As a proof of external validity, we show that the probes transfer across benchmarks without retraining.
Our positive results open calls for more research in mechanistic interpretability of coding agents.
Code
|
Data
1
Introduction
Coding agents are increasingly used to solve complex software engineering tasks.
Over many steps, they read files, reason about the problem, edit code, run tests, and revise their changes, iterating until the task is complete.
Despite intense interest in building such agents, strikingly little is known about how the underlying language model represents the code it is working on.
In this paper, we study the following question:
what does a coding agent internally represent about the program it is editing?
Prior work in other domains gives reason to expect a rich answer.
Transformers trained on board games develop linearly decodable internal representations of the game state
(
Li et al., 2023
;
Nanda et al., 2023
;
Karvonen, 2024
)
.
Models trained on synthetic grid-world programs encode both the current and future semantic state of those programs
(
Jin & Rinard, 2024
)
.
In the software domain, prior work
(
Ribeiro et al., 2025
;
Bui et al., 2025
;
Vu et al., 2025
)
has established that the correctness of a single generated function is linearly decodable from a model’s hidden states.
Yet, these papers assume single-step generation where the full program sits in context and never changes.
None of them is about coding agents iteratively editing an only partially observed real codebase, over dozens of steps, where the model’s hidden state shifts with every edit. This is the problem we address in this paper.
To study this arguably difficult question, we proceed as follows.
We systematically collect agentic trajectories, extract the residual stream of the model at each agentic step, and train linear probes to decode properties of the program being edited.
We consider two open-weight models running
mini-swe-agent
(
Yang et al., 2024
)
on two benchmarks (
SWE-Bench-Verified
(
Jimenez et al., 2024
)
and
SWE-Bench-Pro
(
Deng et al., 2025
)
).
Two main findings emerge.
Coding agents encode the current program.
Linear probes recover hard program properties. We show that the probes capture whether the current program parses, passes its test suite, reduces the number of failing tests, and introduces regressions, all well above a sound shuffled-label control.
The signal persists throughout the trajectory and is strongest in the model’s intermediate layers.
Coding agents anticipate future programs.
Beyond tracking the present, the agents represent programs that have not yet materialized.
Probes trained to predict the outcome of a future edit succeed up to roughly 25 steps in advance.
This is the coding analogue of learned look-ahead in game-playing networks
(
Jenner et al., 2024
;
Taufeeque et al., 2024
)
.
Coding agents have an idea of the shape of the future programs they will write, well before those changes are materialized with edits.
To the best of our knowledge, we are the first to show that coding agents maintain and continually update latent representations of programs and their semantic properties (
). Furthermore, we are the first to report on a long-term programming horizon in the latent space, with strong evidence from ahead-of-chance prediction capabilities.
Contributions.
•
We propose a novel experimental protocol to study how coding agents maintain a representation of programs in the latent space.
•
We show that linear probes on the hidden states of coding agents are able to decode four hard properties of programs. Our experimental results are based on real-world codebases and multi-step trajectories (median = 52 steps). We demonstrate that these probes are calibrated and transfer across benchmarks without retraining.
•
We show that the latent space captures the programming horizon. The latent program representation grounds future edit prediction: probes can predict the outcome of an edit
k
k
steps ahead, and this holds for up to
k
=
25
k=25
steps.
2
Latent Program Representations
Consider a coding agent solving a programming task by iteratively searching and reasoning about the codebase, making edits, running tests, and using the feedback to guide its next steps.
Beyond the tokens the underlying model emits and observes, such an agent may encode a latent program representation, an internal account of the program that it updates and revises. This representation, invisible to the harness and the user at the token level, is the object we study in this paper.
This representation, if it exists, lives somewhere in the internal calculation of the model.
Indeed, transformer models maintain a running hidden-state vector, called the residual stream, which each layer reads from and writes an additive update back to, carrying information from the input through to the output.
We write
𝐡
t
ℓ
∈
ℝ
d
\mathbf{h}_{t}^{\ell}\in\mathbb{R}^{d}
for the residual stream at token position
t
t
after layer
ℓ
\ell
. Because every layer communicates through it, the residual stream is the standard target for probing what a model internally represents
(
Elhage et al., 2021
)
.
In this paper, we study whether the residual stream contains latent program representations.
Definition 1
(Latent program representation)
.
A latent program representation is what is encoded about a program in the residual stream
𝐡
t
ℓ
\mathbf{h}_{t}^{\ell}
. It is captured independently from the surface tokens the agent has emitted or will emit.
The residual stream does not only contain the latent program representation. It also carries information about the task at hand and the past conversation, so the latent program representation is tangled with other signals in the hidden state, and recovering it is the job of the probes we introduce later, see
subsection 3.4
.
Definition 2
(Latent program space)
.
The latent program space is the manifold of the hidden-state space
ℝ
d
\mathbb{R}^{d}
along which latent program representations are encoded. As the agent edits code and runs tests, the hidden state moves along this manifold, forming a latent program representation trajectory.
At each step, the hidden state is the point on this manifold, it captures the current program. A capable agent, however, might not only reason about the present. If the model is planning ahead, its current hidden state should also encode properties of the future programs, the ones it might write several steps ahead. We call the reach of this planning in the latent space the “latent programming horizon”.
Definition 3
(Latent programming horizon)
.
The latent programming horizon is the extent to which future edits are already encoded in the current residual stream.
We define the latent programming horizon as the capability of predicting program properties of the program at
t
t
+
k
k
steps in advance, only based on
𝐡
t
ℓ
\mathbf{h}_{t}^{\ell}
. We refer to it as the programming horizon at
k
k
.
The horizon
k
k
captures the depth of future planning. Any prediction about the program at
k
=
0
k=0
means that the properties of the current program are represented in the latent space
For small
k
k
(a short-term horizon), prediction success means the current hidden state already carries properties of edits that are a few steps away, for example, a sequence of edits in the same file.
For large
k
k
(a long-term horizon), prediction success means the agent anticipates programs that it will write only much later in the trajectory.
While language models are not explicitly trained to encode program representations in their hidden states, several training signals may push them in that direction.
Next-token prediction implicitly rewards learning program syntax and semantics, as predicting the next line of a function is easier if those are understood.
Beyond next-token training objectives, modern code models are also post-trained with signals based on execution traces
(
Copet et al., 2025
)
or feedback from compilers and test suites
(
Ye et al., 2022
)
, particularly during reinforcement learning
(
Wei et al., 2026
)
. Basically, both pre-training and post-training should contribute to having semantically rich latent representations of the program a coding agent is working on.
In this paper, we are the first to study whether latent program representations have emerged in the latent space of coding models and how coding agents maintain them during software engineering tasks.
3
Methods
Figure 1:
Our method to train probes to predict program properties.
A residual-stream vector
𝐡
t
\mathbf{h}_{t}
, taken at step
t
t
of an agentic editing trajectory, is processed by linear probes, parameterized with a lookahead programming horizon
k
k
.
Each probe predicts whether the program
k
k
steps ahead one of four binary properties (
▲
\blacktriangle
Well-formedness
,
∙
\bullet
Full Correctness
,
■
\blacksquare
Partial Correctness
,
⧫
\blacklozenge
Regression
); ground-truth labels are computed at each edit event by checking out that program version and evaluating it.
At
k
=
0
k{=}0
the probe evaluates whether the latent space maps the program as it currently stands, while probes at larger
k
k
measure how far ahead
𝐡
t
\mathbf{h}_{t}
anticipates the program the agent will eventually write: its latent programming horizon.
Filled cells mark a property observed in the program (true), light cells an unsatisfied one (false); all computed symbolically from the training trajectories. At inference time, the probes predict future properties, and we measure the prediction accuracy.
We study what coding agents do during multi-step agentic editing of real codebases, in the latent space.
3.1
Overview
We need a way to capture program representations in the hidden state.
For this, we follow the probing literature
(
Alain & Bengio, 2017
;
Zhang et al., 2025
)
and train linear probes to classify program properties from hidden states.
Figure
1
shows an overview of our setup.
If such probes predict program properties above chance, it shows the model actually encodes those properties in its residual stream.
3.2
Formal Setup
Let
ℳ
\mathcal{M}
be a language model with
L
L
transformer layers.
An agentic trajectory
𝒯
\mathcal{T}
for a coding task consists of
S
S
interaction steps.
At each step
s
s
, the agent generates a response
A
s
A_{s}
given the accumulated context; the tool then produces an output
O
s
O_{s}
.
The full trajectory is the linearised concatenation:
𝒯
=
C
1
⊕
A
1
⊕
O
1
⊕
⋯
⊕
A
S
⊕
O
S
\mathcal{T}=C_{1}\oplus A_{1}\oplus O_{1}\oplus\cdots\oplus A_{S}\oplus O_{S}
where
C
1
C_{1}
is the initial context (typically system and user prompts), and
⊕
\oplus
denotes token-sequence concatenation.
For each position
t
t
in the generated portions
⋃
s
=
1
S
A
s
\bigcup_{s=1}^{S}A_{s}
, let
𝐡
t
ℓ
∈
ℝ
d
\mathbf{h}_{t}^{\ell}\in\mathbb{R}^{d}
denote the residual stream after layer
ℓ
\ell
.
We index layers from
1
1
, so that
𝐡
t
1
\mathbf{h}_{t}^{1}
is the residual stream after the first transformer block and
𝐡
t
L
\mathbf{h}_{t}^{L}
after the final block.
An
edit event
occurs at step
s
s
when
A
s
A_{s}
includes a tool call that modifies the codebase.
Let
e
1
<
e
2
<
⋯
e_{1}<e_{2}<\cdots
denote the token indices of successive edit
events within
𝒯
\mathcal{T}
.
The edits capture the trial-and-error process of the model to perform the task at hand.
In this paper, a
program property
ϕ
\phi
is a function that assigns to each edit event
e
i
e_{i}
a binary label
y
i
ϕ
∈
{
0
,
1
}
y_{i}^{\phi}\in\{0,1\}
reflecting a property of the resulting program version.
For example, the property ‘compilability’ captures whether a program at a given edit compiles, see
Section
3.3
for the list of properties considered in this paper.
Labels are computed externally only at each event, and then kept until the next edit:
every generated token position
t
t
with
e
i
≤
t
<
e
i
+
1
e_{i}\leq t<e_{i+1}
receives the label of edit
e
i
e_{i}
.
We also evaluate
ϕ
\phi
on the initial program version and treat it as a phantom edit
e
0
e_{0}
preceding the trajectory, so every position
t
t
has a well-defined label even before the first agent edit.
It is convenient to index labels by step rather than by token: let
σ
⁡
(
t
)
\sigma(t)
be the step in which token
t
t
is generated (so
t
∈
A
σ
⁡
(
t
)
t\in A_{\sigma(t)}
), and let
y
s
ϕ
y_{s}^{\phi}
denote the label in effect at step
s
s
, that is, the label of the most recent edit at or before step
s
s
. The token-level label is then
y
t
ϕ
=
y
σ
⁡
(
t
)
ϕ
y_{t}^{\phi}=y_{\sigma(t)}^{\phi}
.
3.3
Program Properties
We define four program properties to study through probing.
We will train probes to predict both current and future values of these properties from the hidden states of the model while working on a program.
▲
\blacktriangle
Well-formedness
Well-formedness is a necessary precondition for code to execute.
We operationally define it by parsing or compiling the program at a given version.
The label is
1
1
if it succeeds and
0
0
otherwise.
∙
\bullet
Full Correctness
Full correctness tracks the functional behavior of the program, which is the ultimate goal of code generation and repair.
The label is
1
1
if the program passes the benchmark’s test suite oracle, and
0
0
otherwise.
■
\blacksquare
Partial Correctness
Rather than asking whether the code is fully correct, this probe captures partial correctness, whether the program is moving in the right direction.
The label is
1
1
if the number of failing tests is strictly less than at the beginning of the task, and
0
0
otherwise.
⧫
\blacklozenge
Regression
A capable agent must attend not only to the tests it is trying to fix but also to those it must not break.
This probe tests whether hidden states carry a signal about side effects of an edit.
The label is
1
1
if any test that passed at the beginning of the task now fails, and
0
0
otherwise.
Together, these four properties span what a coding agent must track to resolve a task: the well-formedness of an edit (
▲
\blacktriangle
Well-formedness
), its functional correctness (
∙
\bullet
Full Correctness
), its directional progress per the test suite outcomes (
■
\blacksquare
Partial Correctness
), and its collateral effect on the rest of the repository (
⧫
\blacklozenge
Regression
).
3.4
Probing Program Poperties
For each layer
ℓ
∈
{
1
,
11
,
21
,
31
,
40
}
\ell\in\{1,11,21,31,40\}
, we collect all hidden states
𝐡
t
ℓ
\mathbf{h}_{t}^{\ell}
together with their labels
y
t
ϕ
y_{t}^{\phi}
.
To test whether hidden states at layer
ℓ
\ell
carry information about
ϕ
\phi
, we train a logistic regression classifier,
𝐰
∈
ℝ
d
\mathbf{w}\in\mathbb{R}^{d}
, to predict
y
t
ϕ
y_{t}^{\phi}
from the residual stream
𝐡
t
ℓ
\mathbf{h}_{t}^{\ell}
.
We split trajectories, for training and testing, based on task identifier, ensuring no trajectories of the same task appear in more than one split.
As a sanity check, to verify that the probes decode a signal already present in the hidden states rather than fit it themselves
(
Hewitt & Liang, 2019
)
, we also retrain each probe on randomly permuted labels.
The classifiers trained on one benchmark are further used to probe the hidden states of another to check if the signal they extract transfers across benchmarks.
Probe hyperparameters are selected via random search sweeps based on mean validation AUC.
3.5
Programming Horizon
To study whether coding agents have a programming horizon, we study whether one can predict the outcome of a future edit before that particular edit appears in their output.
Concretely, we train probes to predict program properties at varying lookahead horizons.
For each property
ϕ
\phi
and horizon
k
≥
0
k\geq 0
(in steps), we train a probe on the hidden state
𝐡
t
ℓ
\mathbf{h}_{t}^{\ell}
to predict
y
σ
⁡
(
t
)
+
k
ϕ
y_{\sigma(t)+k}^{\phi}
, the label of the program
k
k
steps later.
We fit a separate probe at each
k
k
.
We sweep
k
k
from
0
0
(equivalent to the current-state probe) to
k
max
=
50
k_{\max}=50
, excluding the final
k
max
k_{\max}
steps of each trajectory to hold the token population constant across horizons.
If the probe discriminative performance is higher than chance for a given
k
k
, it means that the coding agent has a programming horizon of length
k
k
.
Table 1:
Dataset statistics per model and benchmark. #Traj. counts all agent runs;
≥
\geq
50 counts trajectories reaching that step threshold (the length filter used in the lookahead experiments). Med. steps is the median number of steps per trajectory. #Edits is the total number of code edits across all trajectories.
≥
\geq
2 edits counts trajectories with at least two edits. Med. edits is the median number of edits per trajectory.
#
​
h
t
\#h_{t}
is the total number of collected hidden-state vectors. The full trajectory dataset is publicly available:
Data
.
Model
Benchmark
#Traj.
≥
\geq
50 steps
Med. steps
#Edits
≥
\geq
2 edits
Med. edits
#
​
h
t
\#h_{t}
Laguna
Verified
4,991
2,837
55
14,545
2,974
2
7.5M
Pro
6,921
4,159
56
36,648
5,273
4
7.6M
Qwen3.6
Verified
4,998
2,001
39
9,730
2,161
1
3.8M
Pro
5,804
3,186
54
18,557
3,682
2
3.5M
Total
22,714
12,183
52
79,480
14,090
2
22.4M
3.6
Dataset
We consider two coding agents on two benchmarks.
For agents, we run
mini-swe-agent
v2.2.8
(
Yang et al., 2024
)
with two state-of-the-art medium-sized models,
Qwen3.6-35B-A3B
(
Qwen Team, 2026
)
and
Laguna-XS.2
(
Abadji et al., 2026
)
.
Both models have a hidden-state dimension of
d
=
2048
d=2048
.
Regarding benchmarks, we use
SWE-Bench-Verified
(
Jimenez et al., 2024
)
(all 500 tasks) and
SWE-Bench-Pro
(
Deng et al., 2025
)
(all 731 tasks).
For each task, we attempt to generate up to
n
=
10
n=10
trajectories.
Agent hyperparameters, including limits, are listed in
Table
2
.
For each trajectory, we record the full program version after every tool call that modifies the codebase, and the results of evaluating the considered program properties.
For each trajectory, we record the hidden states every 5 tokens, for the sake of space.
Table
1
summarises the resulting dataset; trajectory length distributions (a median of 36k tokens per trajectory) and label prevalence per probe are shown in the Appendix (
Figure
6
).
Table
1
clearly shows that our trajectories are multistep, with a median number of two and a mean of 3.5 edits per trajectory.
4
Results
4.1
Coding agents encode the current program
Figure 2:
Best-layer AUC for each probe, model, and dataset. Each bar shows the peak AUC across layers. Probes trained on randomly shuffled labels collapse to
0.50
0.50
, confirming that the signal is in the representation rather than an artefact of probe capacity. Full per-layer results are in
Table
5
in the appendix.
Figure
2
reports our first main finding.
Every probe, on both models, is able to decode its corresponding program property well above chance.
For example, considering
▲
\blacktriangle
Well-formedness
, the best-trained probe is for
Laguna-XS.2
, with an AUC of
0.78
0.78
well above the random baseline of
0.5
0.5
.
In other words, the hidden state of the model encodes the program properties of the program it is working on.
Predicting semantic properties is generally stronger.
The signal is strongest for
∙
\bullet
Full Correctness
(AUC up to
0.83
0.83
) and
■
\blacksquare
Partial Correctness
(AUC up to
0.84
0.84
) for
Qwen3.6-35B-A3B
.
Similar results can be observed for
Laguna-XS.2
, where
∙
\bullet
Full Correctness
is the strongest on
SWE-Bench-Verified
(AUC up to
0.73
0.73
) and where
⧫
\blacklozenge
Regression
reaches an AUC up to
0.75
0.75
on
SWE-Bench-Pro
.
This means that the model’s hidden states capture the semantic changes implied by every edit.
This holds consistently across both benchmarks: the similar scores on
SWE-Bench-Verified
and
SWE-Bench-Pro
indicate the signal is not specific to a single task distribution.
▲
\blacktriangle
Well-formedness
on
SWE-Bench-Verified
is a clear exception, with probes collapsing to near chance (AUC always below
0.60
0.60
).
This happens because trajectories in
SWE-Bench-Verified
contain mostly compilable Python programs (positive label rate above
0.92
0.92
) – the considered models excel in this language.
In the case of
SWE-Bench-Pro
, which includes three additional programming languages in its tasks (e.g. C++, TypeScript), and a far richer mix of compilation failures (positive rate between
0.52
0.52
and
0.57
0.57
) in our training datasets, we observe higher training data balance and higher signal (AUC up to
0.78
0.78
).
To sum up, as a coding agent edits a real codebase, its residual stream carries a linearly decodable representation of current program properties: whether it compiles, whether it passes its tests, and how its edits move the test suite relative to the initial repository.
Those results have strong external validity, based on 22714 trajectories collected over 1231 different coding tasks.
Figure 3:
AUC-ROC by transformer layer for all four probes at
k
=
0
k=0
:
▲
\blacktriangle
Well-formedness
(top left),
∙
\bullet
Full Correctness
(top right),
■
\blacksquare
Partial Correctness
(bottom left),
⧫
\blacklozenge
Regression
(bottom right). Each panel shows both models (
Laguna-XS.2
and
Qwen3.6-35B-A3B
) across both datasets (
SWE-Bench-Verified
and
SWE-Bench-Pro
), with separate lines per model–dataset combination. The inverted-U pattern, weakest at layer 1, peaking in the intermediate layers, slightly lower at the final layer, is consistent across all probes and both models except
▲
\blacktriangle
Well-formedness
.
Layer localization of program properties.
Figure
3
shows a consistent inverted-U across layer depth.
Performance on program property prediction is lowest at the shallowest layer, rises to a peak at intermediate layers, and falls again slightly at the final layer.
This pattern holds across all probes, models, and datasets, all indicating that the program signal is most concentrated in the middle layers.
At layer 1, the probe is almost always the weakest of any depth, in some cases near or at the random baseline.
This is consistent with previous work in mechanistic interpretability outside the coding domain
(
Jin et al., 2025
)
.
The mid-layer peaks match previous results on natural language tasks, showing that intermediate layers often encode richer representations
(
Skean et al., 2025
)
.
While better than the first layer, the final layer shows a slight drop in signal, suggesting that final layers trade abstract features for features closer to the next token prediction task.
Full per-layer results are in
Table
6
in the appendix.
Model comparison.
Per
Figure
2
,
Qwen3.6-35B-A3B
consistently encodes program properties more strongly than
Laguna-XS.2
.
The gap is roughly
0.10
0.10
AUC on
∙
\bullet
Full Correctness
and
■
\blacksquare
Partial Correctness
across both benchmarks (
0.83
0.83
vs.
0.73
0.73
and
0.81
0.81
/
0.84
0.84
vs.
0.71
0.71
/
0.72
0.72
), and roughly
0.04
0.04
–
0.05
0.05
on
⧫
\blacklozenge
Regression
.
Crucially, the layer finding holds, with both models exhibiting an inverted-U peaking in the middle layers, and the final layer slightly below the peak.
The two models therefore differ in how linearly decodable the program representation is but not in where it is encoded.
This suggests that mechanistic interpretability tasks might be more appropriate on
Qwen3.6-35B-A3B
than with
Laguna-XS.2
.
Probes transfer across datasets.
Figure
4
tests whether the probes trained on one benchmark can, without retraining, retrieve program properties from trajectories on another dataset.
For both models, all semantic probes transfer substantially.
For example,
∙
\bullet
Full Correctness
and
■
\blacksquare
Partial Correctness
retain AUC of
0.63
0.63
–
0.78
0.78
at the best layer under cross-dataset evaluation, compared to
0.71
0.71
–
0.84
0.84
in-distribution, a drop of only
0.04
0.04
–
0.09
0.09
units.
These results confirm that our probes extract real signal related to program properties from hidden states, adding further evidence to the hypothesis that coding agents maintain latent program representations.
Figure 4:
Cross-dataset transfer AUC at the best layer for each probe and model. Gray bars show in-distribution performance; colored bars show transfer performance when probe weights trained on one benchmark are applied to the other without retraining.
∙
\bullet
Full Correctness
and
■
\blacksquare
Partial Correctness
transfer with small drops for both models;
▲
\blacktriangle
Well-formedness
collapses near chance in both directions due to the distributional mismatch in syntactic failure rates between
SWE-Bench-Verified
(near-constant compilability) and
SWE-Bench-Pro
(multi-language, richer failure modes).
4.2
Coding agents have a long-term programming horizon
Figure 5:
Lookahead AUC for the two strongest properties on
Laguna-XS.2
, across both benchmarks:
∙
\bullet
Full Correctness
(top) and
■
\blacksquare
Partial Correctness
(bottom);
SWE-Bench-Verified
(left) and
SWE-Bench-Pro
(right). A probe at token position
t
t
predicts a program property
k
k
steps later; the horizon
k
k
runs from the edit itself (
k
=
0
k=0
, left of each plot) out to 50 steps ahead (right). Each line is a layer; the dashed line is the
0.50
0.50
random baseline. AUC is highest at the edit, falls steeply over the first
∼
25
{\sim}25
steps, and plateaus above chance thereafter. The hockey-stick pattern is consistent across both benchmarks. Full per-probe results are in
Figures
7
and
9
in the appendix.
We have shown that the hidden state encodes the current properties of the program.
Now, we demonstrate that it also encodes the properties of the future programs to come, that one can predict the outcome of future edits before those edits have materialized.
We train each probe to predict a program property
k
k
steps in the future,
y
^
σ
⁡
(
t
)
+
k
ϕ
=
probe
⁡
(
𝐡
t
ℓ
)
\hat{y}_{\sigma(t)+k}^{\phi}=\mathrm{probe}(\mathbf{h}_{t}^{\ell})
, and sweep the horizon
k
k
from
0
0
(at the state to predict) out to
50
50
steps ahead.
Figure
5
plots the two strongest properties (
∙
\bullet
Full Correctness
and
■
\blacksquare
Partial Correctness
) on
Laguna-XS.2
across both benchmarks; each curve is a layer.
First, we see that the predictive signal decays smoothly with horizon (and drops most sharply after the initial edit which captures the present state of the program).
At the edit (
k
=
0
k=0
) the best-layer probe recovers
∙
\bullet
Full Correctness
at AUC
∼
0.77
{\sim}0.77
on
SWE-Bench-Verified
and
∼
0.82
{\sim}0.82
on
SWE-Bench-Pro
(a slightly different figure than in
Section
4.1
, because this is a different test set).
For almost all layers, prediction remains above 0.5 for at least 25 steps.
As the horizon lengthens this falls, reaching
∼
0.55
{\sim}0.55
and
∼
0.65
{\sim}0.65
respectively around
k
=
25
k=25
, before flattening into a plateau that persists out to
k
=
50
k=50
.
The plateau actually sits above the
0.50
0.50
control on both benchmarks (
∼
0.52
{\sim}0.52
on Verified,
∼
0.60
{\sim}0.60
on Pro): even 50 steps ahead, an edit’s eventual outcome is weakly predictable.
To our knowledge, this is the first evidence of long-term horizon by coding agents.
5
Related Work
Probing internal representations.
Probing, the method of training supervised classifiers on frozen hidden states to test for a target property, is a standard interpretability tool
(
Alain & Bengio, 2017
;
Tenney et al., 2019
;
Belinkov, 2022
)
.
For example,
Li et al. (2023)
probe a GPT-style model trained on Othello game transcripts and find an internal representation of the game board, which
Nanda et al. (2023)
show is recoverable with a linear probe.
Beyond game state,
Shai et al. (2024)
show that a transformer trained only on next-token prediction linearly encodes a belief-state geometry of the process that generated its training data.
Park et al. (2024)
give formal foundations to linear probing as a tool for interpreting internal representations.
Elhage et al. (2022)
explain, through the theory of superposition, why many features remain linearly accessible even in high-dimensional residual streams.
The recommended best practice
(
Hewitt & Liang, 2019
)
is to use linear probes of limited capacity and compare every probe against a control to ensure the signal lies in the representation rather than the probe.
Predicting future states.
Existing work finds that a single hidden state carries information about tokens not yet generated
(
Pal et al., 2023
;
Belrose et al., 2023
;
Lindsey et al., 2025
;
Pfau et al., 2024
)
.
At a higher level of abstraction,
Jenner et al. (2024)
find that a chess-playing network represents future optimal moves, while
Taufeeque et al. (2024)
show that a recurrent Sokoban agent encodes its planned actions up to roughly 50 steps ahead.
Closest to our correctness horizon, hidden states taken during chain-of-thought reasoning have been shown to encode the final answer and whether it will be correct.
Zhang et al. (2025)
and
Afzal et al. (2025)
decode answer correctness mid-reasoning,
David (2025)
track how this signal sharpens as reasoning proceeds, and
Cencerrado et al. (2025)
predict answer accuracy from a probe on the question alone, before any answer is generated.
These are all demonstrations of learned horizon capabilities.
We show the same for coding agents, where the decoded outcome is the result of an edit made many steps of tool use and test execution later.
Code representations in LLMs.
A line of work probes code models for the structure they encode.
Jin & Rinard (2024)
train a Transformer model on Karel-grid programs and show that linear probes on its hidden states recover both current and future program execution states.
Wan et al. (2022)
find that attention patterns of BERT-style code models highly align with the syntactic structure of the input, and that an unlabeled binary constituency tree can be constructed from the models’ hidden states in an unsupervised, training-free manner.
Hernández López et al. (2022)
further show that these models encode the full labeled abstract syntax tree of code input within a compact syntactic, orthogonally-extracted subspace of their token-level residual stream.
Moving toward semantics,
Karmakar & Robbes (2021)
;
Karmakar & Robbes (2023)
assemble a battery of probing tasks and report that code models capture semantic properties like type validity more readily as syntactic properties than structural ones such as cyclomatic complexity.
Troshin & Chirkova (2022)
probe a range of syntactic, namespace, data-flow and semantic properties, finding that code models encode syntactic structure and identifiers well but capture little about deep semantics such as computational equivalence. Ma et al.
Ma et al. (2024)
separately measure how well models recover data-dependency, control-dependency and control-flow graphs across layers and additionally prove that decoder-only transformer, which is adopted by most LLMs today, possesses the same capability of extracting coding representation as BERT.
Correctness probing.
Closer to our target, a recent line probes hidden states for the correctness of generated programs.
Ribeiro et al. (2025)
,
Bui et al. (2025)
, and
Vu et al. (2025)
aim at decoding whether a single generated function is correct, the last by selecting the most informative layer per input;
Di Cicco (2026)
finds correctness is linearly readable even before the code is generated.
He et al. (2026)
predict correctness from attribution graphs instead of a linear probe.
Gros & Devanbu (2025)
use model calibration data to focus future patching edits towards a minimal repair.
Tahimic & Cheng (2025)
use sparse autoencoders to find a correctness direction that is causally necessary for generating correct code, finding directions that predict errors but failing to do so for correctness.
All of this work studies a synthetic domain-specific language, isolated snippets, or a single step of generation. We instead probe models working on real-world programs, as coding agents rewrite them over many steps. To our knowledge, we are the first to study the outcome of future edits down the programming horizon.
Latent program spaces.
A separate line of work explicitly constructs latent program spaces as part of the neural network modeling.
Early neural program induction represents and executes programs through latent operation embeddings, as in Neural Programmer-Interpreter
(
Reed & De Freitas, 2015
)
and Neural Programmer
(
Neelakantan et al., 2015
)
.
Subsequent methods build continuous program spaces and search them, for program synthesis
(
Hong et al., 2021
;
Balog et al., 2020
;
Macfarlane & Bonnet, 2026
;
Macfarlane et al., 2026
)
and for program repair
(
Silva et al., 2025
)
.
We instead operate on off-the-shelf LLMs. We show, through linear probing, that language models trained to act as coding agents encode latent program representations. These representations have emerged as a byproduct of training, without any explicit latent space training objective.
Coding agents.
Coding agents combine a language model with a harness that lets it autonomously edit and execute code to solve software engineering tasks, such as SWE-agent
(
Yang et al., 2024
)
, OpenHands
(
Wang et al., 2025
)
, CodeAct
(
Wang et al., 2024
)
, and AutoCodeRover
(
Zhang et al., 2024
)
.
Dedicated benchmarks evaluate them on real-world tasks, including SWE-bench
(
Jimenez et al., 2024
)
, SWE-bench Pro
(
Deng et al., 2025
)
, and Multi-SWE-bench
(
Zan et al., 2026
)
.
Analyses of agent trajectories
(
Bouzenia & Pradel, 2025
)
show that successful and failed runs are structurally distinguishable in the token space, with failed trajectories being consistently longer and more variable in step and token count.
Like us,
Sui et al. (2026)
probe the residual stream of coding agents for early detection of failures. They do not study the properties of programs in the latent program space.
To the best of our knowledge, we are the first to demonstrate that coding agents maintain a latent representation of the program throughout their past changes and future editing horizon.
6
Limitations
Decodability is not causality.
Our probes establish that program properties are linearly decodable from hidden states; they do not establish that the agent uses this information when surfacing actions.
Our claims are about what is represented, not about causal mechanisms.
Demonstrating causality would require steering along a probe direction and measuring the effect on the resulting edit and we leave it to future work.
Effect of label imbalance.
∙
\bullet
Full Correctness
and
■
\blacksquare
Partial Correctness
probes achieve the highest AUC across both models, while
▲
\blacktriangle
Well-formedness
consistently achieves the lowest.
We attribute this to label imbalance.
▲
\blacktriangle
Well-formedness
is overwhelmingly positive in the collected trajectories because today’s models excel at producing syntactically valid programs.
The same imbalance explains why the Brier score for
▲
\blacktriangle
Well-formedness
is low despite its low AUC, since a near-constant predictor scores well on Brier by matching the label base rate. Overall, it is most interesting to predict the hardest program properties, i.e., the ones that often flip and take the longest to achieve.
Scope.
We study two open-weight models under a single agent scaffold (
mini-swe-agent
) on two benchmarks.
We believe that the same representation evidence and horizons appear in frontier models, under different scaffolds, or on tasks beyond the ones present in these datasets, but this remains to be demonstrated empirically.
7
Conclusion
Coding agents encode properties of the program they are working on in their residual streams.
We demonstrated that linear probes trained on hidden states decode whether the code compiles, passes its test suite, reduces failing tests, and introduces regressions, reaching AUC up to
0.83
0.83
for full correctness.
This latent representation captures both the present program properties, but also can ground predictions on what the agent has not yet written:
probes predicting the outcome of future edits succeed above chance up to 25 steps before the edit is made.
These results have external validity, they hold across two models and two benchmarks and transfer across datasets without retraining.
These findings open novel research directions towards monitoring and steering coding agents from within the latent space.
Acknowledgments
This work was partially supported by the Wallenberg AI, Autonomous Systems and Software Program (WASP) funded by the Knut and Alice Wallenberg Foundation.
Computational resources were provided on the Berzelius system funded by the Knut and Alice Wallenberg foundation and operated by NAISS.
We acknowledge compute support from Modal.
References
Abadji et al. (2026)
Julien Abadji, Marah Abdin, Connor Adams, Eric Alcaide, Mustafa Altun, Michele Artoni, Junze Bao, Uday Barar, Vassilis Bekiaris, Arkadii Bessonov, et al.
Laguna m. 1/xs. 2 technical report.
arXiv preprint arXiv:2605.27605
, 2026.
Afzal et al. (2025)
Anum Afzal, Florian Matthes, Gal Chechik, and Yftah Ziser.
Knowing before saying: Llm representations encode information about chain-of-thought success before completion.
In
Findings of the Association for Computational Linguistics: ACL 2025
, pp.  12791–12806, 2025.
Alain & Bengio (2017)
Guillaume Alain and Yoshua Bengio.
Understanding intermediate layers using linear classifier probes.
In
5th International Conference on Learning Representations, ICLR 2017, Workshop Track Proceedings
, 2017.
URL
https://openreview.net/forum?id=HJ4-rAVtl
.
Balog et al. (2020)
Matej Balog, Rishabh Singh, Petros Maniatis, and Charles Sutton.
Neural program synthesis with a differentiable fixer.
arXiv preprint arXiv:2006.10924
, 2020.
Belinkov (2022)
Yonatan Belinkov.
Probing classifiers: Promises, shortcomings, and advances.
Computational Linguistics
, 48(1):207–219, 2022.
Belrose et al. (2023)
Nora Belrose, Igor Ostrovsky, Lev McKinney, Zach Furman, Logan Smith, Danny Halawi, Stella Biderman, and Jacob Steinhardt.
Eliciting latent predictions from transformers with the tuned lens.
arXiv preprint arXiv:2303.08112
, 2023.
Bouzenia & Pradel (2025)
Islem Bouzenia and Michael Pradel.
Understanding software engineering agents: A study of thought-action-result trajectories.
In
2025 40th IEEE/ACM International Conference on Automated Software Engineering (ASE)
, pp.  2846–2857. IEEE, 2025.
Bui et al. (2025)
Tuan-Dung Bui, Thanh Trong Vu, Thu-Trang Nguyen, Son Nguyen, and Hieu Dinh Vo.
Correctness assessment of code generated by large language models using internal representations.
Journal of Systems and Software
, pp.  112570, 2025.
Cencerrado et al. (2025)
Iván Vicente Moreno Cencerrado, Arnau Padrés Masdemont, Anton Gonzalvez Hawthorne, David Demitri Africa, and Lorenzo Pacchiardi.
No answer needed: Predicting llm answer accuracy from question-only linear probes.
arXiv preprint arXiv:2509.10625
, 2025.
Copet et al. (2025)
Jade Copet, Quentin Carbonneaux, Gal Cohen, Jonas Gehring, Jacob Kahn, Jannik Kossen, Felix Kreuk, Emily McMilin, Michel Meyer, Yuxiang Wei, et al.
Cwm: An open-weights llm for research on code generation with world models.
arXiv preprint arXiv:2510.02387
, 2025.
David (2025)
Joey David.
Temporal predictors of outcome in reasoning language models.
arXiv preprint arXiv:2511.14773
, 2025.
URL
https://arxiv.org/abs/2511.14773
.
Deng et al. (2025)
Xiang Deng, Jeff Da, Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, Niklas Lauffer, Andrew Park, Nitin Pasari, Chetan Rane, et al.
Swe-bench pro: Can ai agents solve long-horizon software engineering tasks?
arXiv preprint arXiv:2509.16941
, 2025.
Di Cicco (2026)
Carlo Di Cicco.
Code correctness signals in llm hidden states: Pre-generation probing and repair geometry.
arXiv preprint arXiv:2606.14530
, 2026.
Elhage et al. (2021)
Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, et al.
A mathematical framework for transformer circuits.
Transformer Circuits Thread
, 1(1):12, 2021.
Elhage et al. (2022)
Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain, Carol Chen, et al.
Toy models of superposition.
arXiv preprint arXiv:2209.10652
, 2022.
Gros & Devanbu (2025)
David Gros and Prem Devanbu.
Localized calibrated uncertainty in code language models.
arXiv preprint arXiv:2512.24560
, 2025.
He et al. (2026)
Yicheng He, Zheng Zhao, Zhou Kaiyu, Bryan Dai, Jie Fu, and Yonghui Yang.
Codecircuit: Toward inferring llm-generated code correctness via attribution graphs.
arXiv preprint arXiv:2602.07080
, 2026.
Hernández López et al. (2022)
José Antonio Hernández López, Martin Weyssow, Jesús Sánchez Cuadrado, and Houari Sahraoui.
Ast-probe: Recovering abstract syntax trees from hidden representations of pre-trained language models.
In
Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering
, pp.  1–11, 2022.
Hewitt & Liang (2019)
John Hewitt and Percy Liang.
Designing and interpreting probes with control tasks.
In
Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (emnlp-ijcnlp)
, pp.  2733–2743, 2019.
Hong et al. (2021)
Joey Hong, David Dohan, Rishabh Singh, Charles Sutton, and Manzil Zaheer.
Latent programmer: Discrete latent codes for program synthesis.
In
International Conference on Machine Learning
, pp.  4308–4318. PMLR, 2021.
Jenner et al. (2024)
Erik Jenner, Shreyas Kapur, Vasil Georgiev, Cameron Allen, Scott Emmons, and Stuart Russell.
Evidence of learned look-ahead in a chess-playing neural network.
Advances in Neural Information Processing Systems
, 37:31410–31437, 2024.
Jimenez et al. (2024)
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
Swe-bench: Can language models resolve real-world github issues?
In
International Conference on Learning Representations
, volume 2024, pp.  54107–54157, 2024.
Jin & Rinard (2024)
Charles Jin and Martin Rinard.
Emergent representations of program semantics in language models trained on programs.
In
International Conference on Machine Learning
, pp.  22160–22184. PMLR, 2024.
Jin et al. (2025)
Mingyu Jin, Qinkai Yu, Jingyuan Huang, Qingcheng Zeng, Zhenting Wang, Wenyue Hua, Haiyan Zhao, Kai Mei, Yanda Meng, Kaize Ding, et al.
Exploring concept depth: How large language models acquire knowledge and concept at different layers?
In
Proceedings of the 31st international conference on computational linguistics
, pp.  558–573, 2025.
Karmakar & Robbes (2021)
Anjan Karmakar and Romain Robbes.
What do pre-trained code models know about code?
In
2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE)
, pp.  1332–1336. IEEE, 2021.
Karmakar & Robbes (2023)
Anjan Karmakar and Romain Robbes.
Inspect: Intrinsic and systematic probing evaluation for code transformers.
IEEE Transactions on Software Engineering
, 50(2):220–238, 2023.
Karvonen (2024)
Adam Karvonen.
Emergent world models and latent variable estimation in chess-playing language models.
In
First Conference on Language Modeling
, 2024.
URL
https://openreview.net/forum?id=PPTrmvEnpW
.
Li et al. (2023)
Kenneth Li, Aspen K Hopkins, David Bau, Fernanda Viégas, Hanspeter Pfister, and Martin Wattenberg.
Emergent world representations: Exploring a sequence model trained on a synthetic task.
ICLR
, 2023.
Lindsey et al. (2025)
Jack Lindsey, Wes Gurnee, Emmanuel Ameisen, Brian Chen, Adam Pearce, Nicholas L. Turner, Craig Citro, David Abrahams, Shan Carter, Basil Hosmer, Jonathan Marcus, Michael Sklar, Adly Templeton, Trenton Bricken, Callum McDougall, Hoagy Cunningham, Thomas Henighan, Adam Jermyn, Andy Jones, Andrew Persic, Zhenyi Qi, T. Ben Thompson, Sam Zimmerman, Kelley Rivoire, Thomas Conerly, Chris Olah, and Joshua Batson.
On the biology of a large language model.
Transformer Circuits Thread
, 2025.
URL
https://transformer-circuits.pub/2025/attribution-graphs/biology.html
.
Ma et al. (2024)
Wei Ma, Shangqing Liu, Mengjie Zhao, Xiaofei Xie, Wenhang Wang, Qiang Hu, Jie Zhang, and Yang Liu.
Unveiling code pre-trained models: Investigating syntax and semantics capacities.
ACM Transactions on Software Engineering and Methodology
, 33(7):1–29, 2024.
Macfarlane & Bonnet (2026)
Matthew Macfarlane and Clem Bonnet.
Searching latent program spaces.
Advances in Neural Information Processing Systems
, 38:103463–103520, 2026.
Macfarlane et al. (2026)
Matthew Macfarlane, Clément Bonnet, Herke van Hoof, and Levi Lelis.
Gradient-based program synthesis with neurally interpreted languages.
In
The Fourteenth International Conference on Learning Representations
, 2026.
URL
https://openreview.net/forum?id=NAORIWBaoO
.
Nanda et al. (2023)
Neel Nanda, Andrew Lee, and Martin Wattenberg.
Emergent linear representations in world models of self-supervised sequence models.
In
Proceedings of the 6th BlackboxNLP Workshop: Analyzing and Interpreting Neural Networks for NLP
, pp.  16–30, 2023.
Neelakantan et al. (2015)
Arvind Neelakantan, Quoc V Le, and Ilya Sutskever.
Neural programmer: Inducing latent programs with gradient descent.
arXiv preprint arXiv:1511.04834
, 2015.
Pal et al. (2023)
Koyena Pal, Jiuding Sun, Andrew Yuan, Byron C Wallace, and David Bau.
Future lens: Anticipating subsequent tokens from a single hidden state.
In
Proceedings of the 27th Conference on Computational Natural Language Learning (CoNLL)
, pp.  548–560, 2023.
Park et al. (2024)
Kiho Park, Yo Joong Choe, and Victor Veitch.
The linear representation hypothesis and the geometry of large language models.
In
Proceedings of the 41st International Conference on Machine Learning
, pp.  39643–39666, 2024.
Pfau et al. (2024)
Jacob Pfau, William Merrill, and Samuel R. Bowman.
Let’s think dot by dot: Hidden computation in transformer language models.
In
First Conference on Language Modeling
, 2024.
URL
https://openreview.net/forum?id=NikbrdtYvG
.
Qwen Team (2026)
Qwen Team.
Qwen3.6-Plus: Towards real world agents, April 2026.
URL
https://qwen.ai/blog?id=qwen3.6
.
Reed & De Freitas (2015)
Scott Reed and Nando De Freitas.
Neural programmer-interpreters.
arXiv preprint arXiv:1511.06279
, 2015.
Ribeiro et al. (2025)
Francisco Ribeiro, Claudio Spiess, Prem Devanbu, and Sarah Nadi.
On llms’ internal representation of code correctness.
arXiv preprint arXiv:2512.07404
, 2025.
Shai et al. (2024)
Adam S Shai, Sarah E Marzen, Lucas Teixeira, Alexander G Oldenziel, and Paul M Riechers.
Transformers represent belief state geometry in their residual stream.
Advances in Neural Information Processing Systems
, 37:75012–75034, 2024.
Silva et al. (2025)
André Silva, Gustav Thorén, and Martin Monperrus.
Gradient-based program repair: Fixing bugs in continuous program spaces.
arXiv preprint arXiv:2505.17703
, 2025.
Skean et al. (2025)
Oscar Skean, Md Rifat Arefin, Dan Zhao, Niket Nikul Patel, Jalal Naghiyev, Yann Lecun, and Ravid Shwartz-Ziv.
Layer by layer: Uncovering hidden representations in language models.
In
International Conference on Machine Learning
, pp.  55854–55875. PMLR, 2025.
Sui et al. (2026)
Yuan Sui, Yulin Chen, Yibo Li, Xue Jiang, Yufei He, Yihong Dong, Xiaoxin He, Tianyu Gao, and Bryan Hooi.
Tact: Mitigating overthinking and overacting in coding agents via activation steering.
arXiv preprint arXiv:2605.05980
, 2026.
Tahimic & Cheng (2025)
Kriz Tahimic and Charibeth Cheng.
Mechanistic interpretability of code correctness in llms via sparse autoencoders.
arXiv preprint arXiv:2510.02917
, 2025.
Taufeeque et al. (2024)
Mohammad Taufeeque, Philip Quirke, Maximilian Li, Chris Cundy, Aaron David Tucker, Adam Gleave, and Adrià Garriga-Alonso.
Planning in a recurrent neural network that plays sokoban.
arXiv preprint arXiv:2407.15421
, 2024.
Tenney et al. (2019)
Ian Tenney, Dipanjan Das, and Ellie Pavlick.
Bert rediscovers the classical nlp pipeline.
In
Proceedings of the 57th annual meeting of the association for computational linguistics
, pp.  4593–4601, 2019.
Troshin & Chirkova (2022)
Sergey Troshin and Nadezhda Chirkova.
Probing pretrained models of source codes.
In
Proceedings of the Fifth BlackboxNLP Workshop on Analyzing and Interpreting Neural Networks for NLP
, pp.  371–383, 2022.
Vu et al. (2025)
Thanh Trong Vu, Tuan-Dung Bui, Thu-Trang Nguyen, Son Nguyen, and Hieu Dinh Vo.
Model-agnostic correctness assessment for llm-generated code via dynamic internal representation selection.
arXiv preprint arXiv:2510.02934
, 2025.
Wan et al. (2022)
Yao Wan, Wei Zhao, Hongyu Zhang, Yulei Sui, Guandong Xu, and Hai Jin.
What do they capture? a structural analysis of pre-trained language models for source code.
In
Proceedings of the 44th international conference on software engineering
, pp.  2377–2388, 2022.
Wang et al. (2024)
Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and Heng Ji.
Executable code actions elicit better llm agents.
In
Proceedings of the 41st International Conference on Machine Learning
, pp.  50208–50232, 2024.
Wang et al. (2025)
Xingyao Wang, Boxuan Li, Yufan Song, Frank F Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, et al.
Openhands: An open platform for ai software developers as generalist agents.
In
International Conference on Learning Representations
, volume 2025, pp.  65882–65919, 2025.
Wei et al. (2026)
Yuxiang Wei, Olivier Duchenne, Jade Copet, Quentin Carbonneaux, Lingming Zhang, Daniel Fried, Gabriel Synnaeve, Rishabh Singh, and Sida Wang.
Swe-rl: Advancing llm reasoning via reinforcement learning on open software evolution.
Advances in Neural Information Processing Systems
, 38:78500–78525, 2026.
Yang et al. (2024)
John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik R Narasimhan, and Ofir Press.
SWE-agent: Agent-computer interfaces enable automated software engineering.
In
The Thirty-eighth Annual Conference on Neural Information Processing Systems
, 2024.
URL
https://openreview.net/forum?id=mXpq6ut8J3
.
Ye et al. (2022)
He Ye, Matias Martinez, Xiapu Luo, Tao Zhang, and Martin Monperrus.
Selfapr: Self-supervised program repair with test execution diagnostics.
In
Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering
, pp.  1–13, 2022.
Zan et al. (2026)
Daoguang Zan, Zhirong Huang, Wei Liu, Hanwu Chen, Shulin Xin, Linhao Zhang, Qi Liu, Li Aoyan, Lu Chen, Xiaojian Zhong, et al.
Multi-swe-bench: A multilingual benchmark for issue resolving.
Advances in Neural Information Processing Systems
, 38, 2026.
Zhang et al. (2025)
Anqi Zhang, Yulin Chen, Jane Pan, Chen Zhao, Aurojit Panda, Jinyang Li, and He He.
Reasoning models know when they’re right: Probing hidden states for self-verification.
In
Second Conference on Language Modeling
, 2025.
URL
https://openreview.net/forum?id=O6I0Av7683
.
Zhang et al. (2024)
Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury.
Autocoderover: Autonomous program improvement.
In
Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis
, pp.  1592–1604, 2024.
Appendix A
Appendix
A.1
Dataset Statistics
Figure 6:
Left: distribution of trajectory lengths (in agent steps) per (model, dataset) combination. Dashed vertical lines mark the
k
max
=
15
k_{\max}=15
and
k
max
=
50
k_{\max}=50
lookahead thresholds; the former is nearly lossless (90–99% of trajectories), while the latter retains 40–60%. Middle: distribution of tokens per trajectory (median 36k). Right: positive label rate
P
⁡
(
y
=
1
)
P(y=1)
per probe and (model, dataset) combination.
▲
\blacktriangle
Well-formedness
is nearly always positive, which suppresses its AUC despite a real signal being present (see Limitations);
∙
\bullet
Full Correctness
and
■
\blacksquare
Partial Correctness
are more balanced, consistent with their higher AUC.
Table 2:
Agent hyperparameters used during trajectory generation, following the recommended settings provided by each model vendor. Temperature and top-
p
p
control sampling; context is the maximum sequence length; max steps is the step limit per trajectory; and step timeout is the wall-clock limit per tool call.
Model
Temp.
Top-
p
p
Context
Max steps
Step timeout
Laguna-XS.2
0.7
0.95
256k
100
180 s
Qwen3.6-35B-A3B
0.6
0.95
256k
100
180 s
A.2
Probe Hyperparameters
Hyperparameter
Distribution
Values
Learning rate
Log-uniform
[
10
−
4
,
10
−
1
]
[10^{-4},\ 10^{-1}]
Weight decay
Log-uniform
[
10
−
5
,
10
−
1
]
[10^{-5},\ 10^{-1}]
Batch size
Categorical
{
256
,
512
,
1024
}
\{256,\ 512,\ 1024\}
Patience
Categorical
{
10
,
25
,
50
}
\{10,\ 25,\ 50\}
Table 3:
Hyperparameter search space used in the random search sweeps with 20 trials each. The best configurations, maximising validation AUC per probe per layer per model per dataset are used for training the final probes.
Table 4:
Chosen hyperparameters for each model and benchmark, selected by 20-trial random search maximising mean validation AUC. Sweeps were run independently per probe and per layer; table shows the middle probed layer as representative.
Dataset
Model
Probe
Learning rate
Weight decay
Batch size
Patience
Verified
Laguna-XS.2
▲
\blacktriangle
Well-formedness
8.58
×
10
−
3
8.58\times 10^{-3}
1.18
×
10
−
3
1.18\times 10^{-3}
512
50
∙
\bullet
Full Correctness
5.19
×
10
−
4
5.19\times 10^{-4}
3.81
×
10
−
3
3.81\times 10^{-3}
512
10
⧫
\blacklozenge
Regression
2.95
×
10
−
2
2.95\times 10^{-2}
5.19
×
10
−
5
5.19\times 10^{-5}
256
50
■
\blacksquare
Partial Correctness
2.66
×
10
−
2
2.66\times 10^{-2}
2.13
×
10
−
3
2.13\times 10^{-3}
1024
50
Qwen3.6-35B-A3B
▲
\blacktriangle
Well-formedness
3.33
×
10
−
3
3.33\times 10^{-3}
4.20
×
10
−
2
4.20\times 10^{-2}
512
25
∙
\bullet
Full Correctness
1.17
×
10
−
2
1.17\times 10^{-2}
4.10
×
10
−
4
4.10\times 10^{-4}
1024
25
⧫
\blacklozenge
Regression
3.11
×
10
−
4
3.11\times 10^{-4}
1.91
×
10
−
4
1.91\times 10^{-4}
512
50
■
\blacksquare
Partial Correctness
3.39
×
10
−
3
3.39\times 10^{-3}
1.75
×
10
−
4
1.75\times 10^{-4}
1024
10
Pro
Laguna-XS.2
▲
\blacktriangle
Well-formedness
1.40
×
10
−
3
1.40\times 10^{-3}
3.93
×
10
−
4
3.93\times 10^{-4}
512
25
∙
\bullet
Full Correctness
2.09
×
10
−
4
2.09\times 10^{-4}
6.05
×
10
−
4
6.05\times 10^{-4}
256
25
■
\blacksquare
Partial Correctness
1.52
×
10
−
3
1.52\times 10^{-3}
1.64
×
10
−
3
1.64\times 10^{-3}
1024
50
⧫
\blacklozenge
Regression
1.13
×
10
−
4
1.13\times 10^{-4}
1.49
×
10
−
2
1.49\times 10^{-2}
1024
10
Qwen3.6-35B-A3B
▲
\blacktriangle
Well-formedness
2.30
×
10
−
4
2.30\times 10^{-4}
1.46
×
10
−
5
1.46\times 10^{-5}
512
10
∙
\bullet
Full Correctness
4.15
×
10
−
4
4.15\times 10^{-4}
2.27
×
10
−
4
2.27\times 10^{-4}
1024
10
⧫
\blacklozenge
Regression
2.74
×
10
−
3
2.74\times 10^{-3}
2.00
×
10
−
4
2.00\times 10^{-4}
512
50
■
\blacksquare
Partial Correctness
1.26
×
10
−
3
1.26\times 10^{-3}
8.97
×
10
−
5
8.97\times 10^{-5}
1024
50
A.3
Full Probe Results
Table 5:
AUC per probe, model, and benchmark across transformer layers.
Bold
marks the best layer per row.
Shuffled
uses label-permuted data as a sanity baseline.
AUC
↑
\uparrow
Shuffled
Probe
1
11
21
31
40
(best layer)
SWE-bench Verified
Laguna-XS.2
▲
\blacktriangle
Well-formedness
0.502
0.560
0.566
0.571
0.548
0.500
∙
\bullet
Full Correctness
0.591
0.705
0.727
0.705
0.649
0.501
■
\blacksquare
Partial Correctness
0.615
0.682
0.708
0.680
0.641
0.500
⧫
\blacklozenge
Regression
0.548
0.645
0.678
0.661
0.603
0.500
Qwen3.6-35B-A3B
▲
\blacktriangle
Well-formedness
0.499
0.576
0.553
0.587
0.584
0.501
∙
\bullet
Full Correctness
0.648
0.806
0.820
0.828
0.751
0.501
■
\blacksquare
Partial Correctness
0.646
0.796
0.807
0.808
0.739
0.501
⧫
\blacklozenge
Regression
0.533
0.594
0.721
0.721
0.681
0.501
SWE-bench Pro
Laguna-XS.2
▲
\blacktriangle
Well-formedness
0.760
0.779
0.741
0.754
0.759
0.501
∙
\bullet
Full Correctness
0.587
0.692
0.732
0.712
0.673
0.500
■
\blacksquare
Partial Correctness
0.655
0.700
0.722
0.700
0.665
0.500
⧫
\blacklozenge
Regression
0.682
0.736
0.737
0.745
0.725
0.501
Qwen3.6-35B-A3B
▲
\blacktriangle
Well-formedness
0.727
0.719
0.715
0.722
0.737
0.502
∙
\bullet
Full Correctness
0.664
0.797
0.825
0.832
0.777
0.502
■
\blacksquare
Partial Correctness
0.740
0.832
0.841
0.831
0.792
0.502
⧫
\blacklozenge
Regression
0.713
0.778
0.792
0.778
0.732
0.507
Table 6:
Cross-dataset transfer AUC. Gray rows show in-distribution reference performance. Transfer rows show AUC when probe weights trained on one dataset are evaluated on the other; the subscript shows the delta relative to the in-distribution baseline on the
same
evaluation set.
Layer 1
Layer 11
Layer 21
Layer 31
Layer 40
▲
\blacktriangle
Well-formedness
Laguna-XS.2
In-dist (Verified)
0.502
0.560
0.566
0.571
0.548
In-dist (Pro)
0.760
0.779
0.741
0.754
0.759
Verified
→
\rightarrow
Pro
0.508
−
0.251
-0.251
0.527
−
0.252
-0.252
0.532
−
0.210
-0.210
0.523
−
0.231
-0.231
0.508
−
0.251
-0.251
Pro
→
\rightarrow
Verified
0.484
−
0.018
-0.018
0.521
−
0.040
-0.040
0.553
−
0.013
-0.013
0.528
−
0.043
-0.043
0.498
−
0.050
-0.050
Qwen3.6-35B-A3B
In-dist (Verified)
0.499
0.576
0.553
0.587
0.584
In-dist (Pro)
0.727
0.719
0.715
0.722
0.737
Verified
→
\rightarrow
Pro
0.564
−
0.163
-0.163
0.516
−
0.202
-0.202
0.516
−
0.199
-0.199
0.516
−
0.206
-0.206
0.480
−
0.257
-0.257
Pro
→
\rightarrow
Verified
0.509
+
0.010
+0.010
0.527
−
0.049
-0.049
0.531
−
0.021
-0.021
0.503
−
0.083
-0.083
0.447
−
0.137
-0.137
∙
\bullet
Full Correctness
Laguna-XS.2
In-dist (Verified)
0.591
0.705
0.727
0.705
0.649
In-dist (Pro)
0.587
0.692
0.732
0.712
0.673
Verified
→
\rightarrow
Pro
0.502
−
0.085
-0.085
0.630
−
0.062
-0.062
0.645
−
0.086
-0.086
0.643
−
0.069
-0.069
0.542
−
0.132
-0.132
Pro
→
\rightarrow
Verified
0.531
−
0.060
-0.060
0.634
−
0.071
-0.071
0.669
−
0.057
-0.057
0.636
−
0.069
-0.069
0.594
−
0.055
-0.055
Qwen3.6-35B-A3B
In-dist (Verified)
0.648
0.806
0.820
0.828
0.751
In-dist (Pro)
0.664
0.797
0.825
0.832
0.777
Verified
→
\rightarrow
Pro
0.615
−
0.048
-0.048
0.730
−
0.068
-0.068
0.748
−
0.076
-0.076
0.767
−
0.064
-0.064
0.702
−
0.076
-0.076
Pro
→
\rightarrow
Verified
0.587
−
0.061
-0.061
0.764
−
0.042
-0.042
0.781
−
0.039
-0.039
0.778
−
0.049
-0.049
0.699
−
0.052
-0.052
■
\blacksquare
Partial Correctness
Laguna-XS.2
In-dist (Verified)
0.615
0.682
0.708
0.680
0.641
In-dist (Pro)
0.655
0.700
0.722
0.700
0.665
Verified
→
\rightarrow
Pro
0.519
−
0.136
-0.136
0.622
−
0.078
-0.078
0.648
−
0.074
-0.074
0.625
−
0.075
-0.075
0.556
−
0.109
-0.109
Pro
→
\rightarrow
Verified
0.517
−
0.097
-0.097
0.574
−
0.109
-0.109
0.615
−
0.093
-0.093
0.577
−
0.104
-0.104
0.551
−
0.090
-0.090
Qwen3.6-35B-A3B
In-dist (Verified)
0.646
0.796
0.807
0.808
0.739
In-dist (Pro)
0.740
0.832
0.841
0.831
0.792
Verified
→
\rightarrow
Pro
0.623
−
0.117
-0.117
0.774
−
0.058
-0.058
0.773
−
0.068
-0.068
0.776
−
0.055
-0.055
0.720
−
0.072
-0.072
Pro
→
\rightarrow
Verified
0.605
−
0.041
-0.041
0.754
−
0.042
-0.042
0.766
−
0.041
-0.041
0.771
−
0.037
-0.037
0.699
−
0.040
-0.040
⧫
\blacklozenge
Regression
Laguna-XS.2
In-dist (Verified)
0.548
0.645
0.678
0.661
0.603
In-dist (Pro)
0.682
0.736
0.737
0.745
0.725
Verified
→
\rightarrow
Pro
0.459
−
0.223
-0.223
0.500
−
0.237
-0.237
0.626
−
0.110
-0.110
0.618
−
0.127
-0.127
0.540
−
0.185
-0.185
Pro
→
\rightarrow
Verified
0.560
+
0.012
+0.012
0.612
−
0.033
-0.033
0.620
−
0.058
-0.058
0.601
−
0.059
-0.059
0.560
−
0.043
-0.043
Qwen3.6-35B-A3B
In-dist (Verified)
0.533
0.594
0.721
0.721
0.681
In-dist (Pro)
0.713
0.778
0.792
0.778
0.732
Verified
→
\rightarrow
Pro
0.575
−
0.139
-0.139
0.593
−
0.185
-0.185
0.750
−
0.042
-0.042
0.724
−
0.053
-0.053
0.641
−
0.091
-0.091
Pro
→
\rightarrow
Verified
0.557
+
0.024
+0.024
0.664
+
0.070
+0.070
0.667
−
0.054
-0.054
0.661
−
0.060
-0.060
0.613
−
0.067
-0.067
A.4
Lookahead Analysis
The main lookahead experiment uses a maximum
k
k
of 50, which excludes tokens within 50 steps of the end of a trajectory, including all trajectories shorter than 50 steps.
Figure
8
replicates the analysis at
k
≤
15
k\leq 15
, which imposes a smaller constraint.
The monotonic rise in AUC as
k
→
0
k\to 0
and the layer-ordering are consistent with the main results, confirming that the hockey-stick pattern is not an artifact of the reduced sample.
Figure 7:
Lookahead AUC for all four probes on
Laguna-XS.2
(
SWE-Bench-Verified
),
k
≤
50
k\leq 50
. Panels show
∙
\bullet
Full Correctness
(top left),
▲
\blacktriangle
Well-formedness
(top right),
■
\blacksquare
Partial Correctness
(bottom left), and
⧫
\blacklozenge
Regression
(bottom right). A probe at token position
t
t
predicts the program property
k
k
steps later; each line is a transformer layer; the dashed line marks the
0.50
0.50
random baseline. AUC rises as
k
→
0
k\to 0
across all probes.
Figure 8:
Lookahead AUC for all four probes on
Laguna-XS.2
(
SWE-Bench-Verified
),
k
≤
15
k\leq 15
, using the full trajectory sample without the length filter required for
k
≤
50
k\leq 50
. Panel layout matches
Figure
7
. The monotonic rise in AUC as
k
→
0
k\to 0
and the layer ordering replicate the
k
≤
50
k\leq 50
results, confirming the hockey-stick pattern is not an artifact of the trajectory length filter.
Figure 9:
Lookahead AUC for all four probes on
Laguna-XS.2
(
SWE-Bench-Pro
),
k
≤
50
k\leq 50
. Panel layout matches
Figure
7
. The hockey-stick pattern replicates across this harder, multi-language benchmark.
Figure 10:
Lookahead AUC for all four probes on
Laguna-XS.2
(
SWE-Bench-Pro
),
k
≤
15
k\leq 15
, using the full trajectory sample without the length filter. Panel layout matches
Figure
7
. Results are consistent with the
k
≤
50
k\leq 50
analysis on this benchmark.
Figure 11:
Lookahead AUC for all four probes on
Qwen3.6-35B-A3B
(
SWE-Bench-Verified
),
k
≤
50
k\leq 50
. Panel layout matches
Figure
7
. The hockey-stick pattern and layer ordering replicate at larger model scale.
Figure 12:
Lookahead AUC for all four probes on
Qwen3.6-35B-A3B
(
SWE-Bench-Verified
),
k
≤
15
k\leq 15
, using the full trajectory sample without the length filter. Panel layout matches
Figure
7
. Results are consistent with the
k
≤
50
k\leq 50
analysis for this model.
Figure 13:
Lookahead AUC for all four probes on
Qwen3.6-35B-A3B
(
SWE-Bench-Pro
),
k
≤
50
k\leq 50
. Panel layout matches
Figure
7
. The hockey-stick pattern and layer ordering replicate at larger model scale on this harder, multi-language benchmark.
Figure 14:
Lookahead AUC for all four probes on
Qwen3.6-35B-A3B
(
SWE-Bench-Pro
),
k
≤
15
k\leq 15
, using the full trajectory sample without the length filter. Panel layout matches
Figure
7
. Results are consistent with the
k
≤
50
k\leq 50
analysis on this benchmark.
A.5
Example Latent Trajectories
Figure 15:
Two example resolved trajectories, hand-selected from a small set of long (many-edit), resolved rollouts for legibility, shown at layer 20 (best or near-best by probe validation AUC for both models). Left:
Laguna-XS.2
on
sphinx-doc/sphinx-9602
. Right:
Qwen3.6-35B-A3B
on
sympy/sympy-14531
. Each trajectory is reduced from its dense, stride-5 token-level activations to one point per code edit plus a start and an end marker, obtained by mean-pooling all captured hidden states within each corresponding span (before the first edit, between consecutive edits, and after the last edit). Color encodes step order (light = earlier, dark = later) in each model’s palette color; the white circle marks the start and the star marks the final, resolved state. These examples are illustrative only and are not intended as quantitative evidence.