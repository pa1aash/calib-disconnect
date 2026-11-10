---
title: Effectiveness of Hidden-State Probesfor Localizing Reasoning Failures
id: effectiveness-of-hidden-state-probesfor-localizing-reasoning-failures
tags:
- code-llm-confidence-positioning-d82d00
- w3-3
created: '2026-11-10T08:23:55.549605Z'
updated: '2026-11-10T08:25:58.167640Z'
source: https://arxiv.org/html/2610.22046
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:55.547719Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2610.22046 full text: hidden-state probes on Qwen3-4B and 8B in thinking
  mode over DeepMath-103k and Hendrycks MATH, with Monte Carlo rollout labels distinguishing
  capability gap, recoverable failure, and single-step unrecoverable failure. Calibrated
  correctness probe misses 81% of single-step unrecoverable cases and 47% of retry-would-succeed
  cases on 8B; no tested probe localizes the failing step better than a trace-length
  rule. Math, not code; no execution labels. Bears on L4 (localization) and L2 (probe
  limits) outside code.'
---

Effectiveness of Hidden-State Probesfor Localizing Reasoning Failures
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2610.22046v1 [cs.LG] 15 Oct 2026
\workshoptitle
Interpretability as a Science
Effectiveness of Hidden-State Probes
for Localizing Reasoning Failures
Shubham Subhnil
†
†
thanks:
Work done during an internship at IBM Research.
Affiliation:
Trinity College Dublin, Ireland
Email:
subhnils@tcd.ie
Yannis Belkhiter
†
†
thanks:
Also a PhD student at Trinity College Dublin, Ireland.
Affiliation:
IBM Research, Dublin, Ireland
Email:
belkhity@tcd.ie
Erik Miehling
Affiliation:
IBM Research, Dublin, Ireland
Email:
Erik.Miehling@ibm.com
Adam Dahlgren Lindström
Affiliation:
Umeå University, Sweden
Email:
dali@cs.umu.se
Elizabeth M. Daly
Affiliation:
IBM Research, Dublin, Ireland
Email:
elizabeth.daly@ie.ibm.com
Abstract
Verifying the final answer of a long reasoning trace may show that the trace is wrong but it does not distinguish three cases. The problem may lie beyond the model’s capability, another attempt would succeed, or one step in an otherwise recoverable trace made the trace fail. Standard hidden-state probes are trained on final-answer correctness, a label that conflates these cases. Monte Carlo rollouts distinguish the cases and locate the failing step at additional inference cost. We test the hidden states of 4B and 8B reasoning models for the failure type and the failing step and compare each probe with the strongest baseline that uses no hidden states. On incorrect 8B traces, the confidence probe, a calibrated correctness probe at a midpoint cutoff, misses 81% of cases in which a single step makes the trace unrecoverable and 47% of cases in which another attempt would succeed. A probe with a different training design over the same states reverses the ordering of these two kinds of failure, so either ordering can be read from those states. At both scales, no single tested probe locates the failing step more accurately than a rule based only on trace length, and at 4B a probe trained to predict that step fails to outperform this rule in any of 10 runs on identical traces. The confidence probe therefore indicates that an answer is wrong, but its failure-type ordering depends on its training design.
github.com/SSubhnil/Reasoning-Failures
huggingface.co/datasets/ssubhnil/Reasoning-Failures
1
Introduction
Reasoning models can produce long traces that end in an incorrect answer
(
DeepSeek-AI, 2025
;
Yang et al., 2025
)
. For these incorrect traces, the appropriate intervention depends on the cause of the failure. Some problems remain unsolved across many sampled attempts
(
Yue et al., 2025
)
; others are solved on another attempt
(
Wen et al., 2026
)
; and some traces remain recoverable until one step makes all later continuations fail
(
Hwang et al., 2024
)
. A final label does not distinguish these failure types, and a model’s stated confidence is an unreliable guide to correctness: instruction-tuned models asked for a confidence score often assign high scores to incorrect answers
(
Zhao et al., 2026a
)
. A monitor therefore needs to identify the failure type and, for a trace that becomes unrecoverable, the step at which recovery is lost.
A
trace
is the reasoning the model generates in one attempt at a problem, and a
prefix
is a trace up to a given step. A prefix is
recoverable
if a correct answer remains reachable from it. Monte Carlo rollouts from each evaluated prefix estimate the probability that a continuation from it reaches a correct answer. An incorrect trace is termed a
capability gap
if it is unrecoverable from the initial problem state, and a
near miss
if it remains recoverable at every evaluated prefix. A
pit
is an incorrect trace whose first unrecoverable prefix occurs partway through
(
Setlur et al., 2024
, cf.)
; the step that ends that prefix is its
pit
step
. We test the ability of hidden-state probes to distinguish these failure types and locate the
pit
step without additional rollouts at deployment time.
Hidden states carry information about the truth of a statement or an answer
(
Azaria and Mitchell, 2023
;
Marks and Tegmark, 2024
;
Kadavath et al., 2022
)
, and a probe on the hidden states of a language model can estimate the correctness of its reasoning steps
(
Ni et al., 2026
)
. Final labels record only final-answer correctness and do not directly supervise the failure type or the
pit
step. We train probes on the hidden states at a fixed set of layers, the
read site
, with three kinds of supervision: final labels;
rollout rates
, the fraction of rollouts from a prefix that reach a correct answer; and the
pit
step itself (Table
3
).
We evaluate Qwen3 in thinking mode at 4B and 8B on hard mathematics problems from DeepMath-103k
(
He et al., 2026
)
and the training split of Hendrycks MATH
(
Hendrycks et al., 2021
)
. We use this model family because it provides open-weight reasoning models at two scales with a thinking mode
(
Yang et al., 2025
)
. Appendix
B
gives the difficulty levels, the sampling parameters, and the seed and interval conventions of each measurement.
Findings.
1.
The confidence probe, trained on final labels, misses capability gaps and
pit
s more often than near misses.
At the final step, the probe predicts the final label and remains calibrated at both model scales, but it misses
81
%
81\%
of
pit
s and
47
%
47\%
of near misses at 8B; a trace is missed when its predicted correctness at the final step is at or above a
cutoff
of
0.5
0.5
. After controls for four variables of the trace and the problem, the difference between
pit
s and near misses exceeds the prespecified minimum effect of
0.08
0.08
at 8B. At 4B the difference is nonzero and below the minimum effect (Section
3
).
2.
The combined probe reverses the failure-type ordering.
The combined probe, trained on rollout rates of incorrect traces, reads the same hidden states at the same read site. At 8B the confidence probe gives a randomly chosen
pit
a higher final-step score than a randomly chosen near miss with probability
0.76
0.76
(the AUROC of
pit
s against near misses), and the combined probe does so with probability
0.40
0.40
. The two probes differ in training labels, attention mask, step weighting and training schedule, so the reversal cannot be attributed to the labels alone (Section
3
).
3.
At 8B, a failure-type classifier on transcoder activations meets the margin.
The failure-type classifier reads the transcoder activations of one completed incorrect trace per problem and separates problems labelled capability gap from problems labelled
pit
. It exceeds the strongest tested baseline that uses no hidden states by
0.055
0.055
AUROC at 8B and
0.049
0.049
at 4B, so the 8B result meets the prespecified margin of
0.05
0.05
and the 4B result does not (Section
3
).
4.
No single probe exceeds the length rule at locating the
pit
step.
The length rule predicts a late step from trace length alone. At 4B, the pointer probe, trained to predict the
pit
step, exceeds the length rule in 0 of 10 runs on identical held-out
pit
s. The ensemble, the average of the five pointer probes, exceeds the length rule under one of the two weightings of its failure-type loss. At 8B only the value probe, trained on rollout rates of recoverable traces, was tested, and it is below the length rule in each of five training seeds (Section
4
).
The localization finding is limited to the probe designs, training labels, read site, and the two collections of rollouts specified in Table
3
and Section
2
.
2
Failure types
We describe the two collections of rollouts that supply the labels, define the continuation value of a prefix and the best reachable value, use a threshold
θ
\theta
on the best reachable value to assign each incorrect trace a failure type and each
pit
its
pit
step, and state the evaluation protocol.
Collections of rollouts.
Two collections of rollouts supply the labels. The
broad collection
labels every incorrect trace at both scales. It evaluates steps 0, 1 and 2 and then every second step of a trace with 8 rollouts, and evaluates some of these prefixes with 16 rollouts in a refinement stage (Appendix
B
). The
gold collection
applies the same scan to a set of 4B traces with 4 rollouts and refines with 8, half as many as the broad collection. The
pit
steps of its 818
pit
s are the
reference
pit
steps
for localization. Each comparison is scored on one collection, because the two collections use different numbers of rollouts. Table
9
gives the size of each population and the comparisons that use each population.
Figure 1:
The three failure types (Definition
1
) on three Qwen3-4B traces from the gold collection. Each panel shows, for one trace, the rollout rates
p
^
t
\hat{p}_{t}
at the evaluated prefixes and the envelope, which is the best reachable value
V
t
∗
V^{*}_{t}
at each step. For a capability gap, the envelope is at or below
θ
=
0.1
\theta=0.1
from step 0. For a
pit
, the envelope first falls to
θ
\theta
or below partway through the trace, at the
pit
step. For a near miss, the envelope stays above
θ
\theta
at every step.
Step-level value.
We split each trace at blank lines and merge adjacent blocks until every step contains at least 400 tokens. For problem
𝐱
\mathbf{x}
, model
π
\pi
produces steps
y
^
1
,
…
,
y
^
T
\hat{y}_{1},\dots,\hat{y}_{T}
, and the prefix
s
t
=
(
𝐱
,
y
^
1
:
t
)
s_{t}=(\mathbf{x},\hat{y}_{1:t})
contains the problem and the steps through
t
t
. The final label
Y
∈
{
0
,
1
}
Y\in\{0,1\}
records the correctness of the answer generated after the reasoning. Following prior work on mathematical reasoning
(
Setlur et al., 2024
;
Yu et al., 2024
;
Kazemnejad et al., 2025
;
Wang et al., 2024
)
, we define the
continuation value
V
t
π
V^{\pi}_{t}
of a prefix as the probability that a continuation sampled from it ends with a correct answer. We estimate it by the rollout rate
p
^
t
\hat{p}_{t}
, the fraction of
K
K
rollouts from
s
t
s_{t}
that end with a correct answer:
V
t
π
=
𝔼
π
​
[
Y
∣
s
t
]
,
p
^
t
=
1
K
​
∑
j
=
1
K
Y
(
j
)
.
V^{\pi}_{t}=\mathbb{E}_{\pi}\big[\,Y\mid s_{t}\,\big],\qquad\hat{p}_{t}=\frac{1}{K}\sum_{j=1}^{K}Y^{(j)}.
(1)
We call predicting the final label
detection
, estimating
V
t
π
V^{\pi}_{t}
value estimation
, and locating the
pit
step
localization
.
Pit-step definition.
Process reward models trained on human step labels target local validity, the correctness of each step judged on its own
(
Lightman et al., 2024
;
Uesato et al., 2022
)
. Correct traces can contain locally flawed steps
(
Zheng et al., 2025
)
, and in long traces that revise earlier work a local checker can flag a different step from the
pit
step. We therefore define the
pit
step from the continuation value in Equation
1
.
Definition 1
(Best reachable value and the
pit
step)
.
For an incorrect trace, the
best reachable value
at step
t
t
is
V
t
∗
=
max
t
′
≥
t
⁡
V
t
′
π
V^{*}_{t}=\max_{t^{\prime}\geq t}V^{\pi}_{t^{\prime}}
, which is non-increasing in
t
t
, and the
envelope
of the trace is the sequence
V
0
∗
,
…
,
V
T
∗
V^{*}_{0},\dots,V^{*}_{T}
. Step
0
0
denotes the problem before any reasoning, with
s
0
=
(
𝐱
)
s_{0}=(\mathbf{x})
. Let
t
pit
t_{\textsc{pit}}
be the first step at which the envelope is at or below the threshold
θ
\theta
:
t
pit
=
min
⁡
{
t
∈
{
0
,
1
,
…
,
T
}
:
V
t
∗
≤
θ
}
,
θ
=
0.1
.
t_{\textsc{pit}}=\min\{\,t\in\{0,1,\dots,T\}:V^{*}_{t}\leq\theta\,\},\qquad\theta=0.1.
(2)
An incorrect trace is a capability gap if
t
pit
=
0
t_{\textsc{pit}}=0
, a
pit
if
1
≤
t
pit
≤
T
1\leq t_{\textsc{pit}}\leq T
, in which case
t
pit
t_{\textsc{pit}}
is its
pit
step, and a near miss if the envelope stays above
θ
\theta
at every step, written
t
pit
=
∞
t_{\textsc{pit}}=\infty
. Failure types are assigned to incorrect traces only. The running maximum
V
∗
V^{*}
is defined along one sampled trace and differs from the optimal value of a policy.
In the collections, the envelope is computed from the rollout rates
p
^
t
\hat{p}_{t}
at the evaluated prefixes, with the maximum taken over the evaluated prefixes at or after step
t
t
, so the
pit
step is always the last step of an evaluated prefix.
V
t
∗
V^{*}_{t}
gives the highest continuation value available at the current or any later step in the sampled trace. For example, a trace can establish a valid approach, introduce a sign error, and then develop the resulting wrong branch. Its envelope is high before the sign error and near zero afterward, so its
pit
step is the step that introduces the sign error.
The threshold
θ
=
0.1
\theta=0.1
exceeds
1
/
16
=
0.0625
1/16=0.0625
, the rollout rate of a single success among 16 rollouts, the largest
K
K
used to assign labels. At a prefix where the envelope is at or below
θ
\theta
, the rollout rate there and at every later evaluated prefix therefore reflects at most one success in 16 rollouts and no success in 8 or fewer. Self-Explore treats a prefix as unrecoverable only if no sampled continuation succeeds
(
Hwang et al., 2024
)
; the threshold relaxes this test so that a single success in 16 rollouts does not make a prefix recoverable.
Figure 2:
Failure types and
pit
steps in the broad collection at both model scales (Table
9
).
Left:
Shares of capability gaps,
pit
s and near misses among incorrect traces.
Center:
The relative depth of the
pit
step, the
pit
step divided by the number of steps in the trace, with the medians marked. The late median depths of the
pit
step motivate a baseline that predicts a late step.
Right:
The best reachable value immediately before the
pit
step,
V
t
pit
−
1
∗
V^{*}_{t_{\textsc{pit}}-1}
, with the share above
0.25
0.25
marked.
V
t
pit
−
1
∗
V^{*}_{t_{\textsc{pit}}-1}
depends on later sampled states, so a probe that reads only the steps generated so far need not determine it (Section
4
).
Setlur et al. (2024)
select the first step with the lowest estimated value in an incorrect trace,
arg
⁡
min
t
⁡
V
^
t
\arg\min_{t}\hat{V}_{t}
. With few rollouts per prefix, zero estimates are common and a zero estimate can be followed by a rate above
θ
\theta
, so the
arg
⁡
min
\arg\min
step and the
pit
step rarely coincide at either scale (Table
10
); all
pit
steps in this paper follow Definition
1
.
A capability gap has no recoverable prefix; it is related to problems that remain unsolved across repeated attempts
(
Yue et al., 2025
)
and to difficulty regions in which accuracy is at most 10 percent and does not rise with more sampled reasoning paths
(
Chen et al., 2024
)
. A near miss remains recoverable at every evaluated prefix although the trace ends with a wrong answer; it is related to problems that are solved on another attempt
(
Wen et al., 2026
)
. A
pit
is recoverable before its
pit
step and unrecoverable from it onward (Figure
1
). Near misses and
pit
s are the incorrect traces whose prefix at step 0 is recoverable; we call them
recoverable traces
.
Capability gaps are the most frequent failure type at both scales, followed by
pit
s and near misses, and fewer than half of the incorrect traces are recoverable (Figure
2
). The shares of the failure types change by less than two percentage points for
θ
\theta
between
0.05
0.05
and
0.10
0.10
, and raising
θ
\theta
to
0.15
0.15
moves some
pit
s to capability gaps (Table
1
). The shares depend weakly on problem type (Appendix
E
). The best reachable value immediately before the
pit
step is usually low but has a right-skewed tail: some
pit
s retain a best reachable value above
0.25
0.25
until their
pit
step (Figure
2
).
pit
steps occur late in the trace, so localization is compared with the length rule, which predicts a late step (Section
4
).
The behavioral taxonomies reviewed in Section
6
group near misses and
pit
s together, as failures that resampling fixes. Capability gaps, near misses and
pit
s are the evaluation targets of the remaining experiments.
Evaluation protocol.
The two scales share the problem set, but the traces, and therefore the incorrect traces and their failure types, differ between scales, so no comparison between scales is paired. Each point estimate has a 95% bootstrap interval obtained by resampling problems. We report no detected difference when the interval contains zero. Two decision thresholds were fixed before the probes were evaluated. First, a probe counts as using information in the hidden states only if its AUROC exceeds that of the strongest tested baseline for its task that uses no hidden states by
0.05
0.05
, the
margin
, with an interval of the difference that excludes zero. Second, the difference between
pit
s and near misses after controls in Section
3
counts as an effect only above
0.08
0.08
, the
minimum effect
.
3
Confidence predictions by failure type
A probe trained on hidden states and final labels needs no rollouts at deployment time. We train the confidence probe, validate its detection AUROC and calibration, and then evaluate its predictions at the final step.
Probe inputs.
The probes read the hidden states of the frozen model at the read site, on traces that are generated once and reused for every probe (Table
3
). For each step, a probe reads the hidden states at the read site at one token position, which lies at or before the last token of the step. For about half of the traces, the position read for the final step lies in an earlier step (Appendix
D
). We selected the read site, layers
{
23
,
24
}
\{23,24\}
at both scales, from the detection AUROC of a probe at each layer, using the final label only and no failure type or
pit
step (Table
10
; Appendix
D
).
Confidence probe.
We call the probe trained on final labels the
confidence probe
. Every confidence score in this paper is an output of the confidence probe. Our confidence probe is a causal transformer encoder over the steps of a trace. At step
t
t
it reads the hidden states
h
1
,
…
,
h
t
h_{1},\dots,h_{t}
at the read site and outputs the predicted correctness
c
t
=
σ
(
g
(
h
1
:
t
)
)
=
Pr
^
(
Y
=
1
∣
h
1
:
t
)
c_{t}=\sigma(g(h_{1:t}))=\widehat{\Pr}(Y{=}1\mid h_{1:t})
. We broadcast the trace’s final label to every valid step and minimize per-step Bernoulli loss. The same final label supervises every prefix, so the objective estimates
𝔼
[
Y
∣
h
1
:
t
]
\mathbb{E}[Y\mid h_{1:t}]
(
Yu et al., 2024
)
, which equals
V
t
π
V^{\pi}_{t}
only when
h
1
:
t
h_{1:t}
retains all the information in the prefix about the final label (Proposition
1
, Section
4
). We calibrate held-out scores by temperature scaling
(
Guo et al., 2017
)
. Training and validation traces are split by problem, so no problem contributes traces to both; we call this the
problem split
. Appendix
B
gives the architecture and training details and reports a split by trace for comparison.
On held-out problems, the confidence probe predicts the final label and is calibrated before temperature scaling at both scales (Table
13
). Trace length, answer form and problem difficulty also predict the final label, so a probe can score well without using information beyond these variables; format variables have been shown to account for probe accuracy on a different prediction target
(
Sahoo et al., 2026
)
. Table
13
therefore also reports the detection AUROC of the probe’s score after five such variables are regressed out, and a variant of the probe trained with the Brier loss, which gives similar detection AUROC and calibration.
Text baseline.
Among the baselines that use no hidden states, the strongest we tested for detection is the
text baseline
, a gradient-boosted classifier that predicts the final label from eleven features of the trace text, such as the frequency of verification and backtracking sentences, the position of the final answer, and the number and length of sentences (Appendix
B
). A logistic regression on the same features has a lower detection AUROC, so a linear classifier understates the predictive power of these features (Table
13
). The confidence probe reaches a detection AUROC of
0.81
0.81
at both scales, against
0.78
0.78
at 4B and
0.77
0.77
at 8B for the text baseline. The interval of the difference excludes zero and lies below the margin at both scales, so the confidence probe exceeds the text baseline without meeting the margin. Adding the confidence probe’s score to the text baseline’s features raises the detection AUROC, with an interval that excludes zero (Table
13
).
Failure-type pattern.
The confidence probe misses capability gaps and
pit
s more often than near misses at both scales (Figure
3
A; Table
11
); a trace is missed when its predicted correctness at the final step is at least the cutoff of
0.5
0.5
. Overall calibration is compatible with this pattern by failure type, because incorrect traces are the minority of the calibration population.
Controlled comparison.
We test the hypothesis that the best reachable value at step 0,
V
0
∗
V^{*}_{0}
, trace length, answer position and problem difficulty account for the higher miss rate of
pit
s than of near misses. We first compare the two failure types within bins of
V
0
∗
V^{*}_{0}
(Figure
3
B), and then fit a logistic model of trace misses on the failure type and the four variables. The
difference between
pit
s and near misses after controls
is the average marginal effect of changing a trace’s failure type from near miss to
pit
in this model (Appendix
B
). It exceeds the minimum effect at 8B, at
+
0.125
​
[
+
0.104
,
+
0.143
]
+0.125\,[+0.104,+0.143]
. At 4B the difference is nonzero and below the minimum effect, at
+
0.037
​
[
+
0.012
,
+
0.064
]
+0.037\,[+0.012,+0.064]
(Table
11
). Capability gaps have
V
0
∗
≤
θ
V^{*}_{0}\leq\theta
by definition and
pit
s have
V
0
∗
>
θ
V^{*}_{0}>\theta
, so the two failure types occupy disjoint ranges of
V
0
∗
V^{*}_{0}
, and their miss rates are compared without controls.
Combined probe.
We call the probe trained on rollout rates of incorrect traces the
combined probe
. It reads the confidence probe’s input, the hidden states at the read site, and keeps the final label as the target on correct traces. At the final step, the confidence probe gives
pit
s higher scores than near misses at both scales, and the combined probe gives
pit
s lower scores than near misses (Figure
3
C); each probe is scored on its own held-out traces. The two probes differ in training labels, attention mask, step weighting and training schedule (Table
3
; Appendix
B
), so this reversal cannot be attributed to the labels alone.
Failure-type classifier.
The confidence probe’s miss rates for capability gaps and
pit
s differ by less than two percentage points at both scales (Table
11
), so we test the separation of the two failure types from a completed incorrect trace. A transcoder is a fixed sparse approximation of an MLP sublayer
(
Dunefsky et al., 2024
;
Paulo et al., 2025
)
. The
failure-type classifier
differs from the confidence probe in input and in scoring problems instead of traces: it reads the transcoder activations at layers 19 to 24 of one completed incorrect trace per problem and separates problems labelled capability gap from problems labelled
pit
(Appendix
B.1
). It exceeds the strongest tested baseline that uses no hidden states by
0.055
0.055
AUROC at 8B and
0.049
0.049
at 4B. The margin is applied to the mean over six repetitions of five-fold cross-validation on the same problems, so the 8B result meets the margin and the 4B result does not. At both scales the interval of the difference excludes zero and contains the margin in each of the six repetitions. The same classifier on the hidden states at these layers scores lower at both scales (Appendix
B.1
). Our intuition is that the width of the transcoder input, 40 to 64 times that of the hidden states, accounts for part of this gap; a random encoding of equal width was not tested. The failure-type classifier reads a completed trace and predicts a label of its problem, so it applies only after a trace has ended incorrectly. Appendix
B.1
reports the baselines, the six repetitions, and the differences after removing problems whose labels may be defective.
Predicted correctness at the
pit
step.
At both scales, the confidence probe’s predicted correctness is lower at the
pit
step than at the other steps of the trace. The
position-matched steps
of a trace are its other steps whose scaled position
t
/
(
L
−
1
)
t/(L-1)
, for step
t
t
of a trace with
L
L
steps, lies within
0.15
0.15
of the
pit
step’s. Against these steps the decrease remains at 8B. At 4B, where the comparison uses about a tenth as many
pit
s, there is no detected difference (Table
10
).
Figure 3:
Confidence-probe predictions at the final step, on the broad collection at both model scales, with training and validation split by problem.
(A)
The miss rates for capability gaps,
pit
s, and near misses.
(B)
The miss rates of
pit
s and near misses within four bins of the best reachable value at step 0,
V
0
∗
V^{*}_{0}
, at 4B (solid) and 8B (dashed); the star marks the miss rate of capability gaps at their mean
V
0
∗
V^{*}_{0}
. The incorrect traces differ between scales, so no comparison between scales is paired. Bands and bars are 95% problem-clustered bootstrap intervals at both scales.
(C)
AUROC of
pit
s against near misses: the confidence probe ranks
pit
s above near misses and the combined probe ranks
pit
s below near misses, each by its final-step score on its own held-out traces. Table
11
gives the values, intervals and trace counts.
4
Locating the
pit
step
We compare probes that locate the
pit
step with the strongest tested baselines that use no hidden states.
Identifiability.
A training signal identifies a quantity when the population optimum of its objective determines that quantity. The
pit
step is defined through
V
t
∗
V^{*}_{t}
, a maximum over current and later prefix values. At generation time a probe observes only the prefix, so the later values can remain random conditional on its input.
Proposition 1
(Population optimum of outcome supervision)
.
Let
N
N
be the number of valid steps in a trace and assume
0
<
𝔼
π
​
[
N
]
<
∞
0<\mathbb{E}_{\pi}[N]<\infty
. Under a strictly proper per-step Bernoulli objective with final label
Y
Y
broadcast to every valid step, the population risk minimizer over measurable
[
0
,
1
]
[0,1]
-valued functions of the hidden prefix is
g
⋆
(
h
1
:
t
)
=
𝔼
ℚ
[
Y
∣
h
1
:
t
]
g^{\star}(h_{1:t})=\mathbb{E}_{\mathbb{Q}}[Y\mid h_{1:t}]
. Here
ℚ
\mathbb{Q}
is the step-weighted training law, which counts each trace once per valid step. Moreover,
g
⋆
(
h
1
:
t
)
=
𝔼
ℚ
[
V
t
π
∣
h
1
:
t
]
g^{\star}(h_{1:t})=\mathbb{E}_{\mathbb{Q}}[V^{\pi}_{t}\mid h_{1:t}]
, and it equals
V
t
π
V^{\pi}_{t}
under representation sufficiency.
Proposition 2
(Exact recovery from a prefix)
.
Under the completed-incorrect-trace law, fix step
t
t
, condition on
T
≥
t
T\geq t
, and let
s
t
s_{t}
denote the prefix. A measurable function
f
f
with
f
⁡
(
s
t
)
=
V
t
∗
f(s_{t})=V^{*}_{t}
almost surely exists if and only if
Var
⁡
(
V
t
∗
∣
s
t
)
=
0
\mathrm{Var}(V^{*}_{t}\mid s_{t})=0
almost surely. No function of
s
t
s_{t}
returns the realized
V
t
∗
V^{*}_{t}
exactly where that variance is positive, regardless of training label or loss.
t
pit
t_{\textsc{pit}}
is a function of
s
t
s_{t}
if and only if its conditional law given
s
t
s_{t}
is a point mass. For
m
t
=
V
t
∗
−
V
t
π
m_{t}=V^{*}_{t}-V^{\pi}_{t}
,
Var
⁡
(
m
t
∣
s
t
)
=
Var
⁡
(
V
t
∗
∣
s
t
)
\mathrm{Var}(m_{t}\mid s_{t})=\mathrm{Var}(V^{*}_{t}\mid s_{t})
.
A hidden-state probe is no stronger than a probe of
s
t
s_{t}
, since
h
1
:
t
h_{1:t}
is a deterministic function of
s
t
s_{t}
. The claim concerns exact recovery of the realized quantity; a probe may still estimate its conditional mean. Proposition
2
applies only where
Var
⁡
(
V
t
∗
∣
s
t
)
>
0
\mathrm{Var}(V^{*}_{t}\mid s_{t})>0
. We do not measure this variance, and
0
<
V
t
π
<
1
0<V^{\pi}_{t}<1
does not determine it, so Proposition
2
does not explain the localization results below. The values along a completed trace determine
t
pit
t_{\textsc{pit}}
(Lemma
1
); the probes below estimate those values or predict the
pit
step directly. Both propositions are proved in Appendix
C
.
Length rule.
The
length rule
predicts the
pit
step
t
=
round
⁡
(
f
⁡
(
L
−
1
)
)
t=\mathrm{round}(f\,(L-1))
of a trace with
L
L
steps, with one parameter
f
f
.
pit
steps occur late in a trace: the median relative depth of the
pit
step is
0.70
0.70
at 4B and
0.75
0.75
at 8B (Figure
2
). We score the probes and the length rule by Hit@
±
2
\pm 2
, the fraction of
pit
s for which the predicted step lies within two steps of the
pit
step. In each comparison,
f
f
is fitted to maximize Hit@
±
2
\pm 2
on
pit
s of problems outside the evaluation set. The length rule is therefore refitted for each evaluation set, because its score depends on that set’s trace lengths and on the relative depths of its
pit
steps (Appendix
B
).
Pointer probe.
We call the probe trained to predict the
pit
step the
pointer probe
. It differs from the confidence probe in input and target: it reads a completed trace, which Proposition
2
, a statement about prefixes, does not cover, and is trained on the
pit
step itself. The pointer probe is a transformer encoder with bidirectional attention over the steps of a completed trace. At each step it reads that step’s hidden states at the read site together with those of the final step, and it outputs a distribution over the steps of the trace, whose most probable step is its prediction. The distribution is trained on the
pit
steps of the broad collection’s
pit
s. It is trained jointly on three further outputs, among them the failure type, which is trained on all incorrect traces with one of two weightings of its loss, inverse-frequency or uniform (Appendix
B
); only the step distribution is evaluated.
Paired localization results.
At 4B, the pointer probe is trained on the broad-collection traces of 80% of the problems and evaluated on the
2,289
2{,}289
pit
s of the remaining problems; the same problem split is used for every seed and both weightings of the failure-type loss. The pointer probe exceeds the length rule in 0 of 10 runs on identical held-out
pit
s (Table
12
). Each comparison is paired on the same
pit
s, with intervals that resample problems. In a second comparison, on the reference
pit
steps of the gold collection, a pointer probe trained without any problem that contributes a gold trace does not exceed the length rule in any of five seeds. The length rule in this comparison is fitted on broad-collection
pit
s that exclude the gold problems (Table
12
).
An untrained
distance score
, the distance of each step’s stored hidden state from the pooled step states of correct traces of the same problem, has an AUROC for the
pit
step near
0.5
0.5
at every layer tested on 76
pit
traces at 4B (Figure
4
, right). At the read site it is below
t
/
(
L
−
1
)
t/(L-1)
used as a score (Table
10
).
The pointer probe and the length rule disagree on about a third of the held-out
pit
s in every run, about equally in each direction (Table
10
). Averaging the pointer probes across seeds, separately for each weighting of the failure-type loss, gives the
ensemble
. With inverse-frequency weights, the ensemble exceeds the length rule with an interval of the difference that excludes zero; with uniform weights, the interval of the difference contains zero (Table
12
).
Value probe.
We call the probe trained on rollout rates of recoverable traces the
value probe
; it has the combined probe’s design, restricted to recoverable traces (Appendix
B
). Its predicted
pit
step is the
pit
step of Definition
1
computed from its predicted values at the evaluated prefixes in place of the rollout rates. The value probe’s prediction at the last evaluated prefix separates held-out near misses from
pit
s with an AUROC of
0.91
0.91
at both scales (Table
10
). The comparison of near misses with
pit
s was not run for a baseline that uses no hidden states. By Definition
1
, a near miss has a rollout rate above
θ
\theta
at its last evaluated prefix and a
pit
does not, so the value probe’s training target itself separates the two failure types and this AUROC measures the probe’s fit to that target. The value probe’s per-step mean absolute error exceeds the error from predicting zero in every seed, so rollout supervision does not yield accurate per-step values in this experiment.
Localization at 8B.
At 8B, where no gold collection exists, the value probe is the only probe tested for localization. In each seed it is scored on the
pit
steps of the broad collection for that seed’s held-out problems, on the same
pit
s as the length rule. The comparison is through the five seed means, without a paired interval, and the value probe is below the length rule in every seed with both input sets (Table
10
).
Final-label comparison.
We compare the value probe with the
final-label probe
, a transformer encoder over the steps trained on final labels with a causal attention mask, a value output and a confidence output; its predicted
pit
step is the step with the largest drop in its value output from the preceding step (Appendix
B
). The two probes differ in training label, attention mask, output head and step rule, so the comparison changes the label together with these design choices. Each probe is run with five seeds and two input sets, hidden states alone and hidden states with five next-token statistics, on the reference
pit
steps. The value probe is trained on broad-collection traces, which include most gold
pit
traces, so we evaluate each seed on the reference
pit
steps of the problems held out from the value probe’s training. The final-label probe’s training traces are not recorded, so some of these
pit
s may be among them. On these
pit
steps, both probes are below the length rule in every seed with both input sets (Table
12
). The value probe’s advantage over the final-label probe has an interval that excludes zero in one of the five seeds with hidden states alone and in none with hidden states with the next-token statistics (Table
10
). The value probe therefore gives no consistent improvement over the final-label probe on these
pit
steps, and neither probe exceeds the length rule on these
pit
steps or in a pooled evaluation over all reference
pit
steps (Appendix
B
).
Figure 4:
Localization at 4B.
Left:
Hit@
±
2
\pm 2
on the reference
pit
steps for the five pointer probes trained without any problem that contributes a gold trace. Vertical lines mark the uniform-step baseline (dotted, no interval) and two fits of the length rule: the fit on broad-collection
pit
s outside the gold problems (solid, interval shaded), with which each pointer probe is paired, and the fit by five-fold cross-validation within the gold collection (dashed). Bars and the shaded band are 95% bootstrap intervals.
Right:
AUROC of the distance score for the
pit
step against the other steps of the trace, by layer, on 76
pit
traces. Points are midpoints and bars the range over four distance measures, not confidence intervals. The horizontal line is the detection AUROC of the confidence probe, a different task, shown for reference.
Rollout search.
The
pit
step can also be located with rollouts instead of a probe
(
Luo et al., 2024
)
. We replay such a search offline on the stored rollout rates of the gold collection: it reads every second step of a trace and then bisects the interval that contains the first prefix at which the envelope is at or below
θ
\theta
. The search finds the reference
pit
step within two steps for
80.4
%
80.4\%
of the gold
pit
s while reading
6.6
6.6
evaluated prefixes per trace (Table
10
). The search reads the rollout rates that define the reference
pit
steps, so its agreement with them is a different quantity from a probe’s Hit@
±
2
\pm 2
and is reported separately.
5
Discussion and limitations
The confidence probe misses capability gaps and
pit
s more often than near misses at both scales (Figure
3
). At detection it exceeds the strongest baseline we tested that uses no hidden states, but it does not meet the margin (Section
3
). The text baseline’s miss rates by failure type were not measured, so the pattern is established for the confidence probe only.
Either ordering of
pit
s and near misses can be read from the hidden states that the confidence probe reads. The combined probe reads the same hidden states and gives
pit
s lower final-step scores than near misses at both scales, the opposite of the confidence probe (Figure
3
C). We think the training target itself produces the combined probe’s order: by Definition
1
a near miss keeps a rollout rate above
θ
\theta
at its last evaluated prefix and a
pit
does not, so a probe fitted to these rates is trained toward ranking near misses above
pit
s. The confidence probe and the combined probe differ in more than their labels, and we did not isolate the contribution of the labels (Section
3
).
At 4B, no single probe exceeds the length rule at locating the
pit
step on held-out
pit
s, and at 8B the one tested probe, the value probe, is below the length rule in every seed (Section
4
). The hidden states may still carry the
pit
step; the tested probes do not recover it. Two limits bear directly on the localization result. First, each step’s hidden states were read at a position at or before the step’s last token, and for about half of the traces the position read for the final step lies in an earlier step (Section
3
). No result was re-scored with corrected positions, so the localization result holds for these stored hidden states. Second, the
pit
steps are assigned from a small number of rollouts at each evaluated step, and the two collections assign different failure types to some traces they share (Appendix
B
). The highest score that any predictor could reach against these labels is therefore unknown. We think the second limit dominates: the ensemble exceeds the length rule under one weighting, so the pointer probes read some information beyond trace length, and
pit
steps assigned from 4 to 16 rollouts at every second step may be too noisy for that information to raise Hit@
±
2
\pm 2
.
All results in this paper come from one model family, Qwen3 in thinking mode at two scales, on hard mathematics problems. The failure types depend on the rollout protocol, including the number of rollouts, the threshold and the token limits (Appendix
B
). Under this protocol, a capability gap records only that no sampled continuation reached a correct answer. A rollout counts as successful when its final answer is correct, so a continuation that reaches the answer through an invalid argument counts as a success. Such cases are reported for base models
(
Wen et al., 2026
)
. The final labels contain grading errors, and correcting them leaves capability gaps and
pit
s missed more often than near misses at both scales (Appendix
B
).
6
Related work
Correctness probes.
Probes on hidden states predict the truth of a statement or an answer
(
Azaria and Mitchell, 2023
;
Marks and Tegmark, 2024
;
Kadavath et al., 2022
;
Orgad et al., 2025
)
, and on reasoning models the correctness of an intermediate answer
(
Zhang et al., 2025a
)
.
Orgad et al. (2025)
also define error types by resampling the answers to a question and show that probes predict them; their types are defined per question from sampled final answers, and ours per trace from rollouts at each step. A related study trains correctness probes on instruction-tuned models and one distilled reasoning model
(
Yuan et al., 2026
)
; the signal is decodable in all of these models. Steering along the probe direction in two instruction-tuned models does not raise accuracy consistently, which the authors read as a diagnostic signal. The internal signal is useful because verbal reports can differ from the model’s computation
(
Turpin et al., 2023
;
Zhao et al., 2026a
)
. This paper measures the failure types that a correctness probe distinguishes.
Failure taxonomies.
Uncertainty work commonly separates epistemic from aleatoric uncertainty
(
Ahdritz et al., 2024
;
Abbasi Yadkori et al., 2024
)
or data from model uncertainty
(
Ren et al., 2026
)
, and a recent account separates input ambiguity, knowledge gaps and decoding randomness
(
Taparia et al., 2026
)
; decoding randomness is closest in definition to our near misses. Behavioral work separates failures that resampling fixes from failures it does not
(
Islah et al., 2026
)
, and a similar division is hypothesized for self-correction
(
Li, 2026
)
. Under our taxonomy, the failures that resampling fixes combine near misses with
pit
s. Concurrent work predicts, from the output log-probabilities of failed rollouts, which intervention rescues a problem
(
Islah et al., 2026
)
.
Pit-step targets.
Process benchmarks label the first locally invalid step
(
Zheng et al., 2025
)
or every erroneous section of a long trace
(
He et al., 2025
)
, which differs from the
pit
step, and annotators can disagree about which step is wrong
(
Jacovi et al., 2024
)
. State geometry can identify a first local error
(
Alvarez and Baheri, 2026
)
, and attribution graphs can recover local validity
(
Zhao et al., 2026b
)
. Both targets differ from the
pit
step, which depends on the model’s continuations from each prefix, so an oracle for local validity need not locate it.
Cui et al. (2026)
and
Yuan et al. (2025)
infer step credit from final outcomes, which is a different target from the best reachable value (Proposition
1
).
Merrill and Srivastava (2026)
locate commitment junctures by counterfactual resampling in strategic-deception settings. Among the definitions reviewed here, that counterfactual procedure is closest to the definition used in this study. Appendix
A
compares each claim with the nearest prior result.
7
Conclusion
We assigned each incorrect trace of a reasoning model one of three failure types from rollouts and tested the recovery of these types and of the
pit
step from the model’s hidden states. The confidence probe predicts the final label, and at the cutoff it misses capability gaps and
pit
s more often than near misses. The combined probe ranks
pit
s and near misses in the opposite order to the confidence probe, so an ordering of failure types read from a probe depends on the probe’s training design. The failure-type classifier, which reads transcoder activations of a completed incorrect trace, separates capability gaps from
pit
s. It meets the margin at 8B and not at 4B. At 4B no single probe exceeds the length rule at locating the
pit
step, and the ensemble exceeds it under one of the two weightings of its failure-type loss. At 8B only the value probe was tested, and it is below the length rule in every seed. The localization results concern the tested probes and read site; a probe that locates the
pit
step from the hidden states remains possible.
Acknowledgments and Disclosure of Funding
This work was funded in part by the EU Horizon project ELIAS (#101120237). Views and opinions expressed are those of the author(s) only and do not necessarily reflect those of the European Union or The European Research Executive Agency. This publication has partly emanated from research conducted with the financial support of Taighde Éireann – Research Ireland under Frontiers for the Future grant number 21/FFP-A/8957 and grant number 18/CRT/6223. For the purpose of Open Access, the author has applied a CC BY public copyright licence to any Author Accepted Manuscript version arising from this submission. This work was partially supported by the Knut and Alice Wallenberg Foundation. Experiments were run on the Cognitive Compute Cluster (CCC) at IBM Research.
References
Abbasi Yadkori et al. [2024]
Yasin Abbasi Yadkori, Ilja Kuzborskij, András György, and Csaba
Szepesvári.
To believe or not to believe your LLM: Iterative prompting for
estimating epistemic uncertainty.
In
Advances in Neural Information Processing Systems
(NeurIPS)
, pages 58077–58117, 2024.
URL
https://proceedings.neurips.cc/paper_files/paper/2024/hash/6aebba00fff5b6de7b488e496f80edd7-Abstract-Conference.html
.
Ahdritz et al. [2024]
Gustaf Ahdritz, Tian Qin, Nikhil Vyas, Boaz Barak, and Benjamin L. Edelman.
Distinguishing the knowable from the unknowable with language models.
In
International Conference on Machine Learning (ICML)
, pages
503–549, 2024.
URL
https://proceedings.mlr.press/v235/ahdritz24a.html
.
Alvarez and Baheri [2026]
Tyler Alvarez and Ali Baheri.
Where does reasoning break? step-level hallucination detection via
hidden-state transport geometry, 2026.
URL
https://arxiv.org/abs/2605.13772
.
Azaria and Mitchell [2023]
Amos Azaria and Tom Mitchell.
The internal state of an LLM knows when it’s lying.
In
Findings of the Association for Computational Linguistics:
EMNLP
, pages 967–976, 2023.
doi:
10.18653/v1/2023.findings-emnlp.68
.
URL
https://arxiv.org/abs/2304.13734
.
Burns et al. [2023]
Collin Burns, Haotian Ye, Dan Klein, and Jacob Steinhardt.
Discovering latent knowledge in language models without supervision.
In
International Conference on Learning Representations
(ICLR)
, 2023.
URL
https://arxiv.org/abs/2212.03827
.
Chen et al. [2024]
Qiguang Chen, Libo Qin, Jiaqi Wang, Jinxuan Zhou, and Wanxiang Che.
Unlocking the capabilities of thought: A reasoning boundary framework
to quantify and optimize chain-of-thought.
In
Advances in Neural Information Processing Systems
(NeurIPS)
, pages 54872–54904, 2024.
URL
https://arxiv.org/abs/2410.05695
.
Oral.
Cui et al. [2026]
Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Yuchen Zhang, Jiacheng Chen,
Wendi Li, Bingxiang He, Yuchen Fan, Tianyu Yu, Qixin Xu, Weize Chen, Jiarui
Yuan, Huayu Chen, Kaiyan Zhang, Xingtai Lv, Shuo Wang, Yuan Yao, Xu Han, Hao
Peng, Yu Cheng, Zhiyuan Liu, Maosong Sun, Bowen Zhou, and Ning Ding.
Process reinforcement through implicit rewards.
Transactions on Machine Learning Research (TMLR)
, 2026.
URL
https://openreview.net/forum?id=9SkkifLopZ
.
DeepSeek-AI [2025]
DeepSeek-AI.
DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement
learning.
Nature
, 645(8081):633–638, 2025.
doi:
10.1038/s41586-025-09422-z
.
URL
https://arxiv.org/abs/2501.12948
.
Dunefsky et al. [2024]
Jacob Dunefsky, Philippe Chlenski, and Neel Nanda.
Transcoders find interpretable LLM feature circuits.
In
Advances in Neural Information Processing Systems
(NeurIPS)
, pages 24375–24410, 2024.
URL
https://openreview.net/forum?id=J6zHcScAo0
.
Ethayarajh et al. [2022]
Kawin Ethayarajh, Yejin Choi, and Swabha Swayamdipta.
Understanding dataset difficulty with
𝒱
\mathcal{V}
-usable
information.
In
International Conference on Machine Learning (ICML)
, pages
5988–6008, 2022.
URL
https://proceedings.mlr.press/v162/ethayarajh22a.html
.
Gallifant et al. [2025]
Jack Gallifant, Shan Chen, Kuleen Sasse, Hugo Aerts, Thomas Hartvigsen, and
Danielle Bitterman.
Sparse autoencoder features for classifications and transferability.
In
Proceedings of the 2025 Conference on Empirical Methods in
Natural Language Processing
, pages 29939–29963, 2025.
doi:
10.18653/v1/2025.emnlp-main.1521
.
URL
https://aclanthology.org/2025.emnlp-main.1521/
.
Gneiting and Raftery [2007]
Tilmann Gneiting and Adrian E. Raftery.
Strictly proper scoring rules, prediction, and estimation.
Journal of the American Statistical Association
, 102(477):359–378, 2007.
doi:
10.1198/016214506000001437
.
Guo et al. [2017]
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger.
On calibration of modern neural networks.
In
International Conference on Machine Learning (ICML)
,
volume 70, pages 1321–1330, 2017.
URL
https://proceedings.mlr.press/v70/guo17a.html
.
He et al. [2025]
Yancheng He, Shilong Li, Jiaheng Liu, Weixun Wang, Xingyuan Bu, Ge Zhang, Z.Y.
Peng, Zhaoxiang Zhang, Zhicheng Zheng, Wenbo Su, and Bo Zheng.
Can large language models detect errors in long chain-of-thought
reasoning?
In
Proceedings of the 63rd Annual Meeting of the Association
for Computational Linguistics (Volume 1: Long Papers)
, pages 18468–18489,
2025.
doi:
10.18653/v1/2025.acl-long.905
.
URL
https://aclanthology.org/2025.acl-long.905/
.
He et al. [2026]
Zhiwei He, Tian Liang, Jiahao Xu, Qiuzhi Liu, Xingyu Chen, Yue Wang, Linfeng
Song, Dian Yu, Zhenwen Liang, Wenxuan Wang, Zhuosheng Zhang, Rui Wang,
Zhaopeng Tu, Haitao Mi, and Dong Yu.
DeepMath-103K: A large-scale, challenging, decontaminated, and
verifiable mathematical dataset for advancing reasoning.
In
International Conference on Learning Representations
(ICLR)
, 2026.
URL
https://arxiv.org/abs/2504.11456
.
Hendrycks et al. [2021]
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric
Tang, Dawn Song, and Jacob Steinhardt.
Measuring mathematical problem solving with the MATH dataset.
In
Advances in Neural Information Processing Systems (NeurIPS)
Datasets and Benchmarks Track
, 2021.
URL
https://arxiv.org/abs/2103.03874
.
Hewitt et al. [2021]
John Hewitt, Kawin Ethayarajh, Percy Liang, and Christopher D. Manning.
Conditional probing: measuring usable information beyond a baseline.
In
Conference on Empirical Methods in Natural Language
Processing (EMNLP)
, pages 1626–1639, 2021.
doi:
10.18653/v1/2021.emnlp-main.122
.
URL
https://aclanthology.org/2021.emnlp-main.122/
.
Hwang et al. [2024]
Hyeonbin Hwang, Doyoung Kim, Seungone Kim, Seonghyeon Ye, and Minjoon Seo.
Self-Explore: Enhancing mathematical reasoning in language models
with fine-grained rewards.
In
Findings of EMNLP
, pages 1444–1466, 2024.
doi:
10.18653/v1/2024.findings-emnlp.78
.
URL
https://aclanthology.org/2024.findings-emnlp.78/
.
Islah et al. [2026]
Nizar Islah, Istabrak Abbes, Irina Rish, Sarath Chandar, and Eilif B. Muller.
Failed reasoning traces tell you what is fixable (but not by reading
them), 2026.
URL
https://arxiv.org/abs/2606.05145
.
Jacovi et al. [2024]
Alon Jacovi, Yonatan Bitton, Bernd Bohnet, Jonathan Herzig, Or Honovich,
Michael Tseng, Michael Collins, Roee Aharoni, and Mor Geva.
A chain-of-thought is as strong as its weakest link: A benchmark for
verifiers of reasoning chains.
In
Annual Meeting of the Association for Computational
Linguistics (ACL)
, pages 4615–4634, 2024.
doi:
10.18653/v1/2024.acl-long.254
.
URL
https://aclanthology.org/2024.acl-long.254/
.
Kadavath et al. [2022]
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan
Perez, et al.
Language models (mostly) know what they know.
arXiv preprint arXiv:2207.05221
, 2022.
URL
https://arxiv.org/abs/2207.05221
.
Kantamneni et al. [2025]
Subhash Kantamneni, Joshua Engels, Senthooran Rajamanoharan, Max Tegmark, and
Neel Nanda.
Are sparse autoencoders useful? a case study in sparse probing.
In
International Conference on Machine Learning (ICML)
, pages
29018–29049, 2025.
URL
https://openreview.net/forum?id=rNfzT8YkgO
.
Kazemnejad et al. [2025]
Amirhossein Kazemnejad, Milad Aghajohari, Eva Portelance, Alessandro Sordoni,
Siva Reddy, Aaron Courville, and Nicolas Le Roux.
VinePPO: Refining credit assignment in RL training of LLMs.
In
International Conference on Machine Learning (ICML)
, pages
29557–29590, 2025.
URL
https://proceedings.mlr.press/v267/kazemnejad25a.html
.
Li [2026]
Yin Li.
Decomposing LLM self-correction: The accuracy-correction paradox
and error depth hypothesis, 2026.
URL
https://arxiv.org/abs/2601.00828
.
Lightman et al. [2024]
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker,
Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
Let’s verify step by step.
In
International Conference on Learning Representations
(ICLR)
, 2024.
URL
https://openreview.net/forum?id=v8L0pN6EOi
.
Lu et al. [2024]
Jianqiao Lu, Zhiyang Dou, Hongru Wang, Zeyu Cao, Jianbo Dai, Yingjia Wan,
Yunlong Feng, and Zhijiang Guo.
AutoPSV: Automated process-supervised verifier.
In
Advances in Neural Information Processing Systems
(NeurIPS)
, pages 79935–79962, 2024.
URL
https://proceedings.neurips.cc/paper_files/paper/2024/hash/9246aa822579d9b29a140ecdac36ad60-Abstract-Conference.html
.
Luo et al. [2024]
Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat Phatale, Meiqi Guo, Harsh Lara,
Yunxuan Li, Lei Shu, Yun Zhu, Lei Meng, Jiao Sun, and Abhinav Rastogi.
Improve mathematical reasoning in language models by automated
process supervision.
arXiv preprint arXiv:2406.06592
, 2024.
URL
https://arxiv.org/abs/2406.06592
.
Ma et al. [2026]
George Ma, Zhongyuan Liang, Irene Y. Chen, and Somayeh Sojoudi.
Do sparse autoencoders identify reasoning features in language
models?
In
International Conference on Machine Learning (ICML)
, 2026.
URL
https://arxiv.org/abs/2601.05679
.
Marks and Tegmark [2024]
Samuel Marks and Max Tegmark.
The geometry of truth: Emergent linear structure in large language
model representations of true/false datasets.
In
Conference on Language Modeling (COLM)
, 2024.
URL
https://arxiv.org/abs/2310.06824
.
Merrill and Srivastava [2026]
Scott Merrill and Shashank Srivastava.
The point of no return: Counterfactual localization of deceptive
commitment in language-model reasoning, 2026.
URL
https://arxiv.org/abs/2605.17113
.
Nadaf [2026]
Mohammed Suhail B Nadaf.
Steerable but not decodable: Function vectors operate beyond the
logit lens.
In
ICML Workshop on Mechanistic Interpretability
, 2026.
URL
https://arxiv.org/abs/2604.02608
.
Ni et al. [2026]
Jingwei Ni, Ekaterina Fadeeva, Tianyi Wu, Mubashara Akhtar, Jiaheng Zhang,
Elliott Ash, Markus Leippold, Timothy Baldwin, See-Kiong Ng, Artem Shelmanov,
and Mrinmaya Sachan.
ReProbe: Efficient test-time scaling of multi-step reasoning by
probing internal states of large language models.
In
Annual Meeting of the Association for Computational
Linguistics (ACL)
, pages 11667–11689, 2026.
doi:
10.18653/v1/2026.acl-long.536
.
URL
https://arxiv.org/abs/2511.06209
.
O’Neill et al. [2025]
Charles O’Neill, Sviatoslav Chalnev, Rune Chi Zhao, Max Kirkby, and Mudith
Jayasekara.
A single direction of truth: An observer model’s linear residual
probe exposes and steers contextual hallucinations.
In
ICML Workshop on Actionable Interpretability
, 2025.
URL
https://arxiv.org/abs/2507.23221
.
Orgad et al. [2025]
Hadas Orgad, Michael Toker, Zorik Gekhman, Roi Reichart, Idan Szpektor, Hadas
Kotek, and Yonatan Belinkov.
LLMs know more than they show: On the intrinsic representation of
LLM hallucinations.
In
International Conference on Learning Representations
(ICLR)
, 2025.
URL
https://arxiv.org/abs/2410.02707
.
Paulo et al. [2025]
Gonçalo Paulo, Stepan Shabalin, and Nora Belrose.
Transcoders beat sparse autoencoders for interpretability.
arXiv preprint arXiv:2501.18823
, 2025.
URL
https://arxiv.org/abs/2501.18823
.
Pimentel et al. [2020]
Tiago Pimentel, Josef Valvoda, Rowan Hall Maudslay, Ran Zmigrod, Adina
Williams, and Ryan Cotterell.
Information-theoretic probing for linguistic structure.
In
Annual Meeting of the Association for Computational
Linguistics (ACL)
, pages 4609–4622, 2020.
doi:
10.18653/v1/2020.acl-main.420
.
URL
https://aclanthology.org/2020.acl-main.420/
.
Ren et al. [2026]
Jingyi Ren, Ante Wang, Yunghwei Lai, Xiaolong Wang, Linlu Gong, Weitao Li,
Weizhi Ma, and Yang Liu.
Beyond “I don’t know”: Evaluating LLM self-awareness in
discriminating data and model uncertainty.
In
Annual Meeting of the Association for Computational
Linguistics (ACL)
, pages 11911–11929, 2026.
doi:
10.18653/v1/2026.acl-long.547
.
URL
https://arxiv.org/abs/2604.17293
.
Sahoo et al. [2026]
Subramanyam Sahoo, Vinija Jain, Aman Chadha, and Divya Chaudhary.
Linear probes detect task format, not reasoning mode in language
model hidden states.
In
Proceedings of the 6th Workshop on Trustworthy NLP
(TrustNLP 2026)
, pages 227–239, San Diego, California, July 2026.
Association for Computational Linguistics.
doi:
10.18653/v1/2026.trustnlp-main.12
.
URL
https://aclanthology.org/2026.trustnlp-main.12/
.
Setlur et al. [2024]
Amrith Setlur, Saurabh Garg, Xinyang Geng, Naman Garg, Virginia Smith, and
Aviral Kumar.
RL on incorrect synthetic data scales the efficiency of LLM math
reasoning by eight-fold.
In
Advances in Neural Information Processing Systems
(NeurIPS)
, pages 43000–43031, 2024.
URL
https://openreview.net/forum?id=9m87e9Keq1
.
Taparia et al. [2026]
Aditya Taparia, Ransalu Senanayake, Kowshik Thopalli, and Vivek Narayanaswamy.
The anatomy of uncertainty in LLMs, 2026.
URL
https://arxiv.org/abs/2603.24967
.
ICBINB Workshop @ ICLR 2026 (non-archival).
Turpin et al. [2023]
Miles Turpin, Julian Michael, Ethan Perez, and Samuel Bowman.
Language models don’t always say what they think: Unfaithful
explanations in chain-of-thought prompting.
In
Advances in Neural Information Processing Systems
(NeurIPS)
, pages 74952–74965, 2023.
URL
https://proceedings.neurips.cc/paper_files/paper/2023/hash/ed3fea9033a80fea1376299fa7863f4a-Abstract-Conference.html
.
Uesato et al. [2022]
Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa
Wang, Antonia Creswell, Geoffrey Irving, and Irina Higgins.
Solving math word problems with process-based and outcome-based
feedback.
In
NeurIPS Workshop on Mathematical Reasoning and AI
(MATH-AI)
, 2022.
URL
https://arxiv.org/abs/2211.14275
.
Wang et al. [2024]
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen,
Yu Wu, and Zhifang Sui.
Math-Shepherd: Verify and reinforce LLMs step-by-step without
human annotations.
In
Annual Meeting of the Association for Computational
Linguistics (ACL)
, pages 9426–9439, 2024.
doi:
10.18653/v1/2024.acl-long.510
.
URL
https://aclanthology.org/2024.acl-long.510/
.
Wen et al. [2026]
Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye, Zhirong Wu, Yang Wang, Zhijian
Xu, Xiao Liang, Junjie Li, Ziming Miao, Jiang Bian, and Mao Yang.
Reinforcement learning with verifiable rewards implicitly
incentivizes correct reasoning in base LLMs.
In
International Conference on Learning Representations
(ICLR)
, 2026.
URL
https://iclr.cc/virtual/2026/poster/10007896
.
Williams [1991]
David Williams.
Probability with Martingales
.
Cambridge Mathematical Textbooks. Cambridge University Press,
Cambridge, 1991.
doi:
10.1017/CBO9780511813658
.
Xu et al. [2020]
Yilun Xu, Shengjia Zhao, Jiaming Song, Russell Stewart, and Stefano Ermon.
A theory of usable information under computational constraints.
In
International Conference on Learning Representations
(ICLR)
, 2020.
URL
https://openreview.net/forum?id=r1eBeyHFDH
.
Yang et al. [2025]
An Yang et al.
Qwen3 technical report.
arXiv preprint arXiv:2505.09388
, 2025.
URL
https://arxiv.org/abs/2505.09388
.
Yu et al. [2024]
Fei Yu, Anningzhe Gao, and Benyou Wang.
OVM, outcome-supervised value models for planning in mathematical
reasoning.
In
Findings of the Association for Computational Linguistics:
NAACL 2024
, pages 858–875, 2024.
doi:
10.18653/v1/2024.findings-naacl.55
.
URL
https://aclanthology.org/2024.findings-naacl.55/
.
Yuan et al. [2026]
Aojie Yuan, Zhiyuan Julian Su, Haiyue Zhang, Yi Nian, and Yue Zhao.
Hidden error awareness in chain-of-thought reasoning: The signal is
diagnostic, not causal.
In
ICML Workshop on Mechanistic Interpretability
, 2026.
URL
https://arxiv.org/abs/2605.09502
.
Yuan et al. [2025]
Lifan Yuan, Wendi Li, Huayu Chen, Ganqu Cui, Ning Ding, Kaiyan Zhang, Bowen
Zhou, Zhiyuan Liu, and Hao Peng.
Free process rewards without process labels.
In
International Conference on Machine Learning (ICML)
, pages
73511–73525, 2025.
URL
https://proceedings.mlr.press/v267/yuan25c.html
.
Yue et al. [2025]
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song,
and Gao Huang.
Does reinforcement learning really incentivize reasoning capacity in
LLMs beyond the base model?
In
Advances in Neural Information Processing Systems
(NeurIPS)
, pages 57654–57689, 2025.
URL
https://openreview.net/forum?id=4OsgYD7em5
.
Oral.
Zhang et al. [2025a]
Anqi Zhang, Yulin Chen, Jane Pan, Chen Zhao, Aurojit Panda, Jinyang Li, and
He He.
Reasoning models know when they’re right: Probing hidden states for
self-verification.
In
Conference on Language Modeling (COLM)
, 2025a.
URL
https://arxiv.org/abs/2504.05419
.
Zhang et al. [2025b]
Qingjie Zhang, Yujia Fu, Yang Wang, Liu Yan, Tao Wei, Ke Xu, Minlie Huang, and
Han Qiu.
Stop before you fail: Operational capability boundaries for
mitigating unproductive reasoning in large reasoning models,
2025b.
URL
https://arxiv.org/abs/2509.24711
.
Zhao et al. [2026a]
Tianyi Zhao, Yinhan He, Wendy Zheng, Yujie Zhang, and Chen Chen.
Wired for overconfidence: A mechanistic perspective on inflated
verbalized confidence in LLMs.
In
Conference on Language Modeling (COLM)
, 2026a.
URL
https://arxiv.org/abs/2604.01457
.
Zhao et al. [2026b]
Zheng Zhao, Yeskendir Koishekenov, Xianjun Yang, Naila Murray, and Nicola
Cancedda.
Verifying chain-of-thought reasoning via its computational graph.
In
International Conference on Learning Representations
(ICLR)
, 2026b.
URL
https://openreview.net/forum?id=CxiNICq0Rr
.
Oral.
Zheng et al. [2025]
Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu,
Dayiheng Liu, Jingren Zhou, and Junyang Lin.
ProcessBench: Identifying process errors in mathematical reasoning.
In
Annual Meeting of the Association for Computational
Linguistics (ACL)
, pages 1009–1024, 2025.
doi:
10.18653/v1/2025.acl-long.50
.
URL
https://aclanthology.org/2025.acl-long.50/
.
Appendix A
Claims, evidence, and prior work
Table
1
states each claim at the scope supported by the experiments, reports the decisive measurements, records failed and inconclusive comparisons, and identifies the nearest prior work. The detailed tables provide sample sizes, seed axes, and confidence intervals. A probe counts as using information in the hidden states only when it meets the margin defined in Section
2
. Differences below the margin are recorded as failures even when their intervals exclude zero.
Claim
Supporting evidence
Verdict
Nearest prior work
Contribution
Best reachable value partitions incorrect traces into capability gaps,
pit
s, and near misses
0.56
/
0.39
/
0.05
0.56/0.39/0.05
(4B) and
0.53
/
0.38
/
0.09
0.53/0.38/0.09
(8B); recoverable
44.5
44.5
and
46.8
%
46.8\%
; the shares change by less than two percentage points for
θ
\theta
between
0.05
0.05
and
0.10
0.10
, while
θ
=
0.15
\theta{=}0.15
raises the share of capability gaps to
0.68
0.68
and
0.65
0.65
Descriptive result under one decoding setting
[
Hwang et al., 2024
,
Setlur et al., 2024
,
Li, 2026
,
Ahdritz et al., 2024
]
Separates
pit
s from near misses among recoverable traces
The confidence probe predicts final correctness and remains calibrated
Detection AUROC
0.814
0.814
and
0.809
0.809
over 5 seeds; after controls
0.729
0.729
and
0.722
0.722
; ECE
0.014
0.014
/
0.024
0.024
(Table
13
); the text baseline reaches
0.7783
0.7783
at 4B and
0.7725
0.7725
at 8B
Supported for prediction and calibration; the probe exceeds the text baseline by less than the margin
[
Azaria and Mitchell, 2023
,
Kadavath et al., 2022
,
Yuan et al., 2025
,
Yuan et al., 2026
]
A step-level probe with a causal attention mask and surface-feature controls
Miss rates at the cutoff differ by failure type
Miss rates
0.717
/
0.714
/
0.490
0.717/0.714/0.490
(4B) and
0.797
/
0.815
/
0.466
0.797/0.815/0.466
(8B); difference between
pit
s and near misses after controls
+
0.037
+0.037
and
+
0.125
+0.125
(Table
11
)
Supported at 8B;
partial at 4B
, where the difference between
pit
s and near misses after controls is nonzero, its interval
[
+
0.012
,
+
0.064
]
[+0.012,+0.064]
does not reach the minimum effect, and the confidence probe trained with the Brier loss gives
+
0.052
+0.052
[
Yuan et al., 2026
]
Breaks down misses by failure type
Probes with different training designs recover opposite failure-type orderings
AUROC of
pit
s against near misses: confidence probe
0.67
/
0.76
0.67/0.76
, combined probe
0.36
/
0.40
0.36/0.40
(4B/8B), each on its own held-out traces
Opposite orderings under partially matched training designs; the contribution of the target alone is open
[
Yu et al., 2024
,
Lu et al., 2024
]
Compares two training designs on the same hidden states at the same read site
A failure-type classifier on transcoder activations of one completed incorrect trace per problem separates capability-gap problems from
pit
problems
Difference from the strongest tested baseline that uses no hidden states
+
0.055
+0.055
(8B) and
+
0.049
+0.049
(4B), mean over six repetitions of five-fold cross-validation; every interval excludes zero and contains the margin; the same classifier on hidden states scores lower (Appendix
B.1
)
Meets the margin at 8B, not at 4B; a difference between the scales is not established; applies after a trace has ended
[
Orgad et al., 2025
,
Zhang et al., 2025b
,
Kantamneni et al., 2025
]
Separates capability gaps from
pit
s; the confidence probe’s miss rates do not separate these two types
No single tested probe exceeds the length rule at locating the
pit
step; at 8B only the value probe was tested
Pointer probe
0.463
0.463
versus length rule
0.469
0.469
, above the length rule in
0
0
of
10
10
runs; pointer probe trained without gold problems
0.429
0.429
versus
0.446
0.446
,
0
0
of
5
5
; ensemble
+
0.026
+0.026
[
+
0.002
,
+
0.050
]
[+0.002,+0.050]
with inverse-frequency weights on the failure-type loss, interval containing zero with uniform weights; final-label comparison: the value probe and the final-label probe are below the length rule in every seed on the problems held out from the value probe’s training; pooled over all reference
pit
steps, which include training traces, the two probes score above the length rule in
0
0
of
20
20
runs (Table
12
); 8B value probe with the two input sets
0.429
0.429
and
0.405
0.405
versus length rule
0.503
0.503
, above the length rule in
0
0
of
5
5
seeds for each input set (Table
10
)
Negative result at 4B, paired on identical
pit
s, and at 8B, compared through seed means against the
pit
steps of the broad collection. Earlier configurations evaluated on
55
55
to
134
134
pit
s are inconclusive
[
Zheng et al., 2025
,
Alvarez and Baheri, 2026
,
Zhao et al., 2026b
,
Cui et al., 2026
,
Nadaf, 2026
]
Uses a continuation-based
pit
-step target and refits the length rule for each evaluation set
At 4B, a rollout search replayed on the gold collection’s stored estimates reproduces the reference
pit
steps
Within two steps for
80.4
%
80.4\%
of the gold
pit
s while reading
6.6
6.6
evaluated prefixes per trace; refinement-depth agreement
0.754
0.754
Supported at 4B in an offline replay against the estimates that define the reference
pit
steps; not comparable with a probe’s Hit@
±
2
\pm 2
; no interval
[
Luo et al., 2024
]
Measures the share of the collection’s evaluated prefixes that the search reads
Table 1:
Claims, supporting evidence, verdicts, nearest prior work, and contributions. Among the reviewed studies, none combines a three-way recovery taxonomy, probes on hidden states, and a continuation-based
pit
-step target.
Appendix B
Experimental protocols
Problem set and sampling.
The two scales share one problem set of
35,854
35{,}854
problems. Of these problems,
32,031
32{,}031
come from DeepMath-103k at difficulty at least 7, and
3,823
3{,}823
come from levels 4 and 5 of the training split of Hendrycks MATH. Each problem has four sampled traces, except 146 problems with eight, which gives
144,000
144{,}000
traces at each scale. The traces were sampled at temperature
0.7
0.7
with a 16k-token budget.
No problem in the problem set matches a MATH-500, MATH-Perturb or AIME 2024–2025 problem after whitespace and case normalization (0 of
35,854
35{,}854
problems). The exact-match check does not detect paraphrased or reformatted duplicates.
Monte Carlo collections.
The two collections use different numbers of rollouts, and every result identifies its source collection (Table
2
). The broad collection labels all incorrect traces and supplies the failure-type shares in Section
2
. In a scan, it evaluates steps 0, 1 and 2 and then every second step with 8 rollouts, and in a refinement it re-evaluates some of these prefixes with 16 rollouts. More than 80% of its evaluated prefixes have 8 rollouts, and more than 70% of its
pit
steps were evaluated with 16 (Table
2
). About half of the 16-rollout prefixes of
pit
s lie within two evaluated steps of the
pit
step. The collection evaluates about 60% of the steps of a trace.
Each set of
K
K
rollouts contains one greedy rollout and
K
−
1
K-1
independent samples at temperature
0.7
0.7
, so its success count is not binomial. Writing
G
t
∈
{
0
,
1
}
G_{t}\in\{0,1\}
for the greedy result and
p
t
p_{t}
for the temperature-
0.7
0.7
success probability, the count is
G
t
+
X
t
G_{t}+X_{t}
, where
X
t
∼
Bin
⁡
(
K
−
1
,
p
t
)
X_{t}\sim\mathrm{Bin}(K-1,p_{t})
. Thus
𝔼
⁡
[
p
^
t
∣
s
t
]
=
[
G
t
+
(
K
−
1
)
​
p
t
]
/
K
\mathbb{E}[\hat{p}_{t}\mid s_{t}]=[G_{t}+(K-1)p_{t}]/K
, a
K
K
-dependent protocol mean rather than
p
t
p_{t}
. Rollout rates at
K
=
8
K=8
and
K
=
16
K=16
therefore differ in mixture weight as well as sampling variance under the recorded protocol. Conditional on the greedy outcome, the remaining
K
−
1
K-1
samples give rate standard deviations of
0.099
0.099
at
K
=
8
K{=}8
and
0.073
0.073
at
K
=
16
K{=}16
near
p
=
0.1
p{=}0.1
. A depth sweep reports refinement-depth agreement of
0.754
0.754
at
K
=
16
K{=}16
against
0.638
0.638
at
K
=
8
K{=}8
. The two agreement values are point estimates against a deeper reference, with no interval.
The envelope is computed over the prefixes evaluated by a collection (Section
2
). Rollouts continue from the final recorded prefix, so the value of that prefix is estimated from rollouts and is not set equal to the final label.
The rollout search, replayed offline on the gold collection’s stored rollout rates, reads every second step and then bisects the interval that contains the first prefix at which the envelope is at or below
θ
\theta
. No 8B replay exists.
Each rollout is capped at
4,096
4{,}096
tokens, a cap read from the stored rollouts at both scales. The temperature of
0.7
0.7
is taken from our experiment records. The temperature, nucleus-sampling parameter, random seed and stop strings cannot be recovered from the stored rollouts, and the script that generated the rollouts was not retained.
Table 2:
The two collections of rollouts. A dash marks a quantity that was not computed for the gold collection. The refinement re-evaluates some prefixes with more rollouts than the scan.
broad collection
gold collection
4B
8B
4B
evaluated steps
0, 1, 2, then every second step
rollouts per prefix in the scan
8
8
4
rollouts per prefix in the refinement
16
16
8
evaluated prefixes with the scan’s rollouts
82.3
%
82.3\%
83.3
%
83.3\%
81.4
%
81.4\%
evaluated prefixes with the refinement’s rollouts
17.7
%
17.7\%
16.7
%
16.7\%
18.6
%
18.6\%
pit
steps evaluated with the refinement’s rollouts
8,270
8{,}270
6,895
6{,}895
448
pit
steps evaluated with the scan’s rollouts
2,990
2{,}990
2,613
2{,}613
370
mean share of a trace’s steps evaluated
0.620
0.620
0.612
0.612
0.623
0.623
cap on each rollout, tokens
4,096
4{,}096
4,096
4{,}096
—
The gold collection contains
5,380
5{,}380
Qwen3-4B traces and supplies 818
pit
s, whose
pit
steps are the reference
pit
steps. It scans with 4 rollouts and refines with 8 (Table
2
), so no step in it receives the 16 rollouts of the broad collection’s refinement. At
K
=
4
K{=}4
and
K
=
8
K{=}8
, a rollout rate at or below
θ
\theta
means zero successes.
The gold collection overlaps the broad collection. Of its
5,380
5{,}380
traces,
2,760
2{,}760
are also broad-collection traces, including 815 of the 818 gold
pit
traces. For 84 of these 815 traces, the broad collection assigns a different failure type: 76 capability gaps and 8 near misses.
This overlap restricts the traces that can be evaluated at 4B. For the pointer probe evaluated on the reference
pit
steps, we exclude every trace from every problem that contributes a gold
pit
. The value probe is trained on broad-collection traces, which include 815 of the gold
pit
traces. For a given seed, 528 to 565 of the gold
pit
s are therefore training traces of the value probe. The final-label probe’s training traces and problem split are not recorded. Section
4
reports an evaluation of each seed on the problems held out from the value probe’s training, with 205 to 242
pit
s per seed. Pooled over all reference
pit
steps, about two thirds of each seed’s evaluations are on training traces of the value probe. In this pooled evaluation the value probe scores higher than the final-label probe, and both probes are below the length rule in all 20 runs (two probes, two input sets, five seeds; Table
12
).
At 8B, where no gold collection exists, the value probe is scored on the
pit
steps of the broad collection within each seed’s held-out problems,
2,805
2{,}805
to
2,918
2{,}918
per seed. The length rule is refitted on each seed’s training problems. The 8B comparison uses the five seed means and reports sample standard deviations over seeds in place of a bootstrap interval on the difference.
Label corrections.
The stored final labels mark some correct answers as incorrect. The mislabelled answers are yes/no answers given as their true/false synonyms, and answers to true-or-false questions whose reference answer is coded as a letter. The reported numbers use the stored labels, and the probes are trained on them.
Correcting these labels changes the 8B capability-gap miss rate under the problem split, from
0.797
0.797
to
0.779
0.779
, which is the largest change among the reported quantities. The 8B
pit
miss rate moves from
0.815
0.815
to
0.800
0.800
. The shares of the failure types move by at most
0.006
0.006
, detection AUROC by at most
+
0.004
+0.004
, and the difference between
pit
s and near misses after controls by at most
+
0.005
+0.005
.
The stored labels also mark as incorrect the answers that the grader could not parse. There are
2,853
2{,}853
such capability-gap and
pit
traces at 4B and
2,994
2{,}994
at 8B. Removing these unparsed traces leaves capability gaps and
pit
s missed more often than near misses at both scales.
Removing instead every problem whose reference answer is a yes/no answer or a letter removes 47% of the incorrect 4B traces. On the remaining traces, the interval of the 4B difference between
pit
s and near misses after controls on the problem split is
[
+
0.009
,
+
0.085
]
[+0.009,+0.085]
, which contains the minimum effect. On all traces the interval is
[
+
0.012
,
+
0.064
]
[+0.012,+0.064]
, which lies below the minimum effect.
Seeds and intervals.
The confidence probe, combined probe, value probe, and pointer probe each use five seeds, with new weights for each seed and a new problem split for each seed, except the pointer probe, whose problem split is the same for every seed. The final-label probe uses the same five seeds; its problem split is not recorded. The value probe, the final-label probe, and the pointer probe use the common set
{
42,137,271,314,577
}
\{42,137,271,314,577\}
. The combined probe also uses the common set; the confidence probe uses seeds
0
0
to
4
4
. Read-site selection uses bootstrap intervals without a seed axis.
The comparison of the confidence probe’s predicted correctness at the
pit
step with other steps uses, for each trace, only the seeds that held it out. The failure-type classifier uses six repetitions of five-fold cross-validation grouped by problem, with the same folds for the classifier and every baseline; the margin is applied to the mean difference over the six repetitions, and each repetition has its own bootstrap interval (Appendix
B.1
). Every bootstrap resamples problems and uses between
1,000
1{,}000
and
2,000
2{,}000
replicates, except the read-site intervals, which use
1,000
1{,}000
resamples of held-out traces, and the pooled differences of the final-label comparison in Table
10
, which use
10,000
10{,}000
resamples of traces.
Residualization.
For Section
3
, we fit a logistic model of trace misses on failure type, trace length, answer position, difficulty, and best reachable value at step 0,
V
0
∗
V^{*}_{0}
. The difference between
pit
s and near misses after controls is the average marginal effect obtained by changing the failure type from near miss to
pit
while holding each other variable at its observed value, then averaging over traces. For the detection AUROC after controls, we regress trace length, difficulty, problem source, answer length, and numeric-answer status out of the confidence probe’s log odds. We score the residual on held-out traces and average over five seeds. As a stratified check, we also compare the miss rates of
pit
s and near misses within cells of
V
0
∗
V^{*}_{0}
bin by trace-length tertile that hold at least 30 near misses. The
pit
miss rate minus the near-miss miss rate is positive in all five such cells at 4B and in seven of eight at 8B, where the exception holds 33 near misses.
Table 3:
Training configuration of every probe and of the failure-type classifier. The four probes read hidden states at the read site (Appendix
D
); the failure-type classifier reads transcoder activations at layers 19 to 24 (Appendix
B.1
). The pointer probe was trained at 4B only.
model
target
training traces
mask
scales
confidence probe
final label
Y
Y
, broadcast to every step
all
144,000
144{,}000
traces
causal
4B, 8B
value probe
rollout rate
p
^
t
\hat{p}_{t}
at each step
recoverable traces
bidirectional
4B, 8B
combined probe
Y
Y
on correct traces,
p
^
t
\hat{p}_{t}
on incorrect ones
143,979
143{,}979
traces (21 incorrect traces without rollout rates dropped)
bidirectional
4B, 8B
pointer probe
pit
step; further outputs, including the failure type
22,877
22{,}877
incorrect traces of the broad collection, of which
8,971
8{,}971
pit
s
bidirectional
4B
failure-type classifier
failure type of the problem, capability gap or
pit
one scored trace per problem
—
4B, 8B
Confidence probe.
The confidence probe is a causal transformer encoder over the steps of a trace, with a learned positional embedding and a two-layer sigmoid head. The two scales use the same architecture and training settings and differ only in input width and number of parameters (Table
4
). For each step, the input concatenates the hidden states of the two read-site layers (Appendix
D
) at one token position.
The objective broadcasts the trace’s final label
Y
Y
to every valid step and minimizes per-step Bernoulli loss, averaged over the valid steps in the batch:
ℒ
conf
=
−
1
∑
i
T
i
∑
i
∑
t
=
1
T
i
[
Y
i
log
c
i
,
t
+
(
1
−
Y
i
)
log
(
1
−
c
i
,
t
)
]
,
c
i
,
t
=
σ
(
g
(
h
i
,
1
:
t
)
)
.
\mathcal{L}_{\text{conf}}=-\frac{1}{\sum_{i}T_{i}}\sum_{i}\sum_{t=1}^{T_{i}}\big[\,Y_{i}\log c_{i,t}+(1-Y_{i})\log(1-c_{i,t})\,\big],\qquad c_{i,t}=\sigma(g(h_{i,1:t})).
(3)
Here
h
i
,
1
:
t
h_{i,1:t}
is the sequence of hidden states read at the read site for steps 1 to
t
t
of trace
i
i
,
g
g
is the encoder’s scalar logit output, and
σ
\sigma
is the logistic function. A Brier-loss robustness variant remains within the BCE variant’s seed spread on every detection and calibration measurement (Table
13
). The experiment establishes no difference between the two objectives, which were not compared pairwise.
Each model trains on all traces with the problem split, which holds out about 30% of the traces, so no problem contributes traces to both training and validation. We fit one temperature on held-out logits. Expected calibration error uses ten equal-width bins and is reported before temperature scaling, which reduces it (Table
13
).
As a leakage comparison, we also train with a 70/30 split by trace, stratified to preserve the base correctness rate, which we call the
trace split
. Under that split,
97.6
%
97.6\%
of validation traces share a problem with at least one training trace. Table
5
gives the trace-split results; the 4B difference between
pit
s and near misses after controls is
+
0.085
+0.085
under the trace split and
+
0.037
+0.037
under the problem split. The trace split also gives 4B
pit
s a higher miss rate than capability gaps (
0.742
0.742
against
0.717
0.717
, Table
5
); under the problem split the
pit
miss rate minus the capability-gap miss rate is
−
0.003
​
[
−
0.018
,
+
0.012
]
-0.003\,[-0.018,+0.012]
.
Table 4:
Architecture and training settings of the confidence probe. A value spanning both columns applies at both scales.
4B
8B
pre-norm encoder layers
4
width
512
attention heads
8
maximum number of steps
48
input dimension per step
5,120
5{,}120
8,192
8{,}192
parameters
15.5M
17.1M
optimizer and learning rate
AdamW,
10
−
4
10^{-4}
batch size
64
maximum epochs, with early stopping
20
numeric precision
bf16
Table 5:
The confidence probe under the trace split, the leakage comparison. Table
13
and Table
11
give the same quantities under the problem split.
4B
8B
detection AUROC
0.8165
0.8165
0.8165
0.8165
AUROC after controls
0.7322
0.7322
0.7267
0.7267
ECE
0.027
0.027
0.019
0.019
miss rate, capability gap
0.717
0.717
0.795
0.795
miss rate,
pit
0.742
0.742
0.823
0.823
miss rate, near miss
0.469
0.469
0.522
0.522
pit
s
−
-
near misses, after controls
+
0.085
​
[
+
0.061
,
+
0.110
]
+0.085\,[+0.061,+0.110]
+
0.119
​
[
+
0.099
,
+
0.137
]
+0.119\,[+0.099,+0.137]
Text baseline.
The text baseline is a gradient-boosted model on eleven features of the trace text: the densities of sentence roles such as verification, derivation and backtracking, assigned by cue-word lists, statistics of the transitions between roles, the position of the final answer, and the number and mean length of sentences. On the problem split, a logistic regression on the same features reaches a detection AUROC of
0.7548
0.7548
at 4B and
0.7379
0.7379
at 8B. Adding the confidence probe’s score to the text baseline’s features raises the detection AUROC by
+
0.034
+0.034
to
+
0.041
+0.041
across the two scales and the two training losses, with intervals that exclude zero.
Combined probe.
Table
3
sets out the target, training traces, mask and model scales of every probe. The combined probe, compared with the confidence probe in Figure
3
C, has the confidence probe’s architecture, input and optimizer (Table
4
). Its attention mask is bidirectional. It trains on correct and incorrect traces, taking the final label as the target at every step of a correct trace and the rollout rate
p
^
t
\hat{p}_{t}
as the target at each evaluated prefix of an incorrect trace; the other steps of an incorrect trace carry no loss. It weights each evaluated prefix by its rollout count and each step of a correct trace by one, and the confidence probe weights every step equally. It trains for a fixed 8 epochs, and the confidence probe trains for at most 20 epochs with early stopping. The combined probe has a lower detection AUROC than the confidence probe on held-out problems at both scales (Table
10
). Training the confidence probe’s design on the combined probe’s labels may help isolate the contribution of the labels; we did not run this experiment.
B.1
Failure-type classifier
Input and population.
The failure-type classifier reads the transcoder activations at the input of the MLP block of each of layers 19 to 24, from the publicly released transcoders for both models
1
1
1
mwhanna/qwen3-4b-transcoders
and
mwhanna/qwen3-8b-transcoders
on Hugging Face.
. For each problem it takes one completed incorrect trace, the one with the lowest trace index, which we call the scored trace.
Each latent’s rectified activation is summed over the trace’s tokens, at most 16,384, and binarized at that latent’s 90th percentile over the problems of the training folds. The binarized vector is projected to 256 dimensions by truncated singular value decomposition and passed to a class-balanced logistic regression.
Gallifant et al. [2025]
sum each sparse-autoencoder latent over the tokens of a text and binarize the sum at a fixed threshold before a logistic regression. The failure-type classifier uses the same summation and binarization with a threshold set for each latent.
The label of a problem is its failure type in the broad collection, capability gap or
pit
. At 4B the population is a class-balanced sample of 1,722 problems within the difficulty range 7.0 to 9.5: 839 capability gaps and 883
pit
s. At 8B it is all 6,372 such problems: 2,749 capability gaps and 3,623
pit
s.
The scored trace is not always the trace that set the problem’s label. At 4B it differs from that trace for 971 of the 1,722 problems. The scored trace is not a verified failure for 13.6% of problems at 4B and 20.3% at 8B, because of the grading defects described under Label corrections.
Baselines and evaluation.
The baselines use no hidden states. They are built from six feature sets: the question text with problem difficulty, trace counts and lengths, the question text with difficulty and the counts and lengths combined, the text of the scored trace, five statistics of the model’s own token log-probabilities on that trace, and the first five sets together, each fitted by logistic regression and by gradient-boosted trees. The strongest of these twelve baselines is taken in each repetition. Every model uses the same five folds grouped by problem, and the five-fold cross-validation is repeated with six seeds; the margin is applied to the mean over the six repetitions of the difference from the strongest baseline, and each repetition has a problem-clustered bootstrap interval. The same pipeline applied to the rectified hidden states at layers 19 to 24, summed over tokens, gives the comparison with hidden states; the transcoder input has
983,040
983{,}040
dimensions against
15,360
15{,}360
(4B) and
24,576
24{,}576
(8B) for the hidden states, and no random encoding of equal width was tested. Reordering the rows of identical inputs moves a baseline’s AUROC by about
0.01
0.01
. The text baselines and the comparison with hidden states address two results on probes of sparse features. Between 45 and 90 percent of the sparse-autoencoder features that activate more on reasoning text than on other text also activate when a few associated tokens are inserted into non-reasoning text
[
Ma et al., 2026
]
. Probes on sparse-autoencoder features do not improve on logistic regression on the dense activations, on average over 113 classification datasets
[
Kantamneni et al., 2025
]
. A linear probe on the hidden state of the last prompt token separates competition problems that a reasoning model fails under greedy decoding from those it solves, before the trace begins
[
Zhang et al., 2025b
]
. A problem that one greedy run fails can be a capability gap, a near miss or a
pit
under the failure types defined here.
Results and label sensitivity.
With the stored labels, the failure-type classifier meets the margin at 8B and not at 4B (Table
6
). The difference from the strongest baseline is
+
0.055
+0.055
at 8B, with every repetition at or above the margin. It is
+
0.049
+0.049
at 4B, with three of six repetitions at or above the margin. Every interval excludes zero and contains the margin (Table
7
). The same classifier on hidden states at the same layers scores lower at both scales. No probe in Table
3
is trained on this label.
Removing problems whose scored trace may carry a wrong label raises the difference at both scales. The removal covers every problem whose scored trace carries a grading defect and, at 4B, every problem whose scored trace has a different failure type from its label. The removal leaves 1,294 problems at 4B and 5,078 at 8B and raises the difference to
+
0.065
+0.065
and
+
0.083
+0.083
. With these problems removed, every repetition is at or above the margin at both scales.
The removed problems are 62% (4B) and 65% (8B) capability gaps, and the baselines lose more AUROC on the remaining problems than the classifier does. The rise in the difference is consistent with two explanations that this analysis does not separate: grading defects that the question text identifies, and a subset of capability gaps that the question text identifies.
The transcoders reconstruct the MLP outputs at layers 19 to 24 with a fraction of variance explained, pooled over tokens, of 0.338 to 0.525 at 4B and 0.366 to 0.564 at 8B.
Table 6:
Failure-type classifier on one completed incorrect trace per problem, capability-gap problems against
pit
problems. AUROCs are means over six repetitions of five-fold cross-validation; the difference is the classifier’s AUROC minus that of the strongest baseline that uses no hidden states, mean
±
\pm
standard deviation over repetitions. The hidden-state column is the same classifier on hidden states at the same layers. The last two rows remove the problems whose scored trace carries a grading defect and, at 4B, those whose scored trace has a different failure type from its label.
labels
scale
problems
classifier
hidden
states
strongest
baseline
difference
repetitions
≥
0.05
\geq 0.05
stored
4B
1,722
0.667
0.580
0.618
+
0.0488
±
0.0071
+0.0488\pm 0.0071
3 of 6
stored
8B
6,372
0.721
0.646
0.666
+
0.0549
±
0.0026
+0.0549\pm 0.0026
6 of 6
defects removed
4B
1,294
0.643
0.581
0.578
+
0.0648
±
0.0074
+0.0648\pm 0.0074
6 of 6
defects removed
8B
5,078
0.700
0.638
0.617
+
0.0830
±
0.0049
+0.0830\pm 0.0049
6 of 6
Table 7:
Difference between the failure-type classifier and the strongest baseline that uses no hidden states, per repetition of five-fold cross-validation, with stored labels. Each cell is the AUROC difference with its 95% problem-clustered bootstrap interval.
repetition
4B
8B
1
+
0.0364
+0.0364
[
+
0.0040
+0.0040
,
+
0.0690
+0.0690
]
+
0.0581
+0.0581
[
+
0.0468
+0.0468
,
+
0.0698
+0.0698
]
2
+
0.0558
+0.0558
[
+
0.0278
+0.0278
,
+
0.0845
+0.0845
]
+
0.0550
+0.0550
[
+
0.0426
+0.0426
,
+
0.0667
+0.0667
]
3
+
0.0505
+0.0505
[
+
0.0218
+0.0218
,
+
0.0814
+0.0814
]
+
0.0537
+0.0537
[
+
0.0413
+0.0413
,
+
0.0671
+0.0671
]
4
+
0.0491
+0.0491
[
+
0.0189
+0.0189
,
+
0.0794
+0.0794
]
+
0.0553
+0.0553
[
+
0.0425
+0.0425
,
+
0.0675
+0.0675
]
5
+
0.0463
+0.0463
[
+
0.0158
+0.0158
,
+
0.0797
+0.0797
]
+
0.0506
+0.0506
[
+
0.0377
+0.0377
,
+
0.0637
+0.0637
]
6
+
0.0547
+0.0547
[
+
0.0222
+0.0222
,
+
0.0879
+0.0879
]
+
0.0568
+0.0568
[
+
0.0442
+0.0442
,
+
0.0686
+0.0686
]
B.2
Localization
Localization baselines.
The length rule predicts
t
=
round
⁡
(
f
⁡
(
L
−
1
)
)
t=\mathrm{round}(f(L-1))
, and we fit the single parameter
f
f
on training traces by maximizing Hit@
±
2
\pm 2
and score the length rule out of sample; Hit@
±
2
\pm 2
is also the evaluation metric of the probes. The median of
t
/
(
L
−
1
)
t/(L-1)
at the
pit
step
t
t
, the length rule’s scale, is
0.75
0.75
at 4B and
0.79
0.79
at 8B. Figure
4
shows two fits on the reference
pit
steps, one by five-fold cross-validation within the gold collection and one on broad-collection
pit
s outside the gold problems; the Hit@
±
2
\pm 2
of the two fits differs by
0.005
0.005
. The uniform-step baseline, a step drawn uniformly from the trace, is computed in closed form for each evaluation set.
Pointer probe.
The pointer probe predicts the
pit
step of a
pit
trace directly. It is a four-layer transformer encoder with bidirectional attention over the steps; at each step it reads that step’s hidden states at the read site together with those of the final step, and it assigns a softmax score to every step. Training minimizes the cross-entropy to the labelled
pit
step smoothed by a Gaussian of width one step, and inference selects the most probable step. The encoder has three further outputs trained jointly, a three-way failure type, a per-step estimate of the envelope and a confidence output, with loss weights 1, 0.25 and 0.5 against 1 for the step distribution; only the step distribution is evaluated in this paper. All 22,877 incorrect training traces (8,971
pit
s, 12,692 capability gaps and 1,214 near misses) supervise the failure-type and envelope outputs, and only the
pit
traces supervise the step distribution. The two weightings of the failure-type loss are inverse-frequency weights (0.85 for
pit
s, 0.60 for capability gaps, 6.28 for near misses) and uniform weights; the step loss is the same under both. A held-out
pit
trace counts as a hit when the most probable step lies within two steps of the labelled
pit
step; held-out traces of the other failure types are not scored for localization. The run that excludes the gold problems trains on 17,143 traces.
Value probe.
The value probe uses the combined probe’s design, trains only on recoverable traces, and predicts the raw rollout rate
p
^
t
\hat{p}_{t}
. A second input set appends to each step’s hidden states five statistics of the model’s next-token distribution at the step’s read position: the entropy, the varentropy, the probability of the most probable token, the difference between the probabilities of the two most probable tokens, and the probability mass of the five most probable tokens. With rollout count
K
t
K_{t}
at step
t
t
, the value probe minimizes count-weighted Bernoulli cross entropy:
ℒ
val
=
∑
t
K
t
​
[
−
p
^
t
​
log
⁡
V
^
t
−
(
1
−
p
^
t
)
​
log
⁡
(
1
−
V
^
t
)
]
∑
t
K
t
.
\mathcal{L}_{\text{val}}=\frac{\sum_{t}K_{t}\big[\,-\hat{p}_{t}\log\widehat{V}_{t}-(1-\hat{p}_{t})\log(1-\widehat{V}_{t})\,\big]}{\sum_{t}K_{t}}.
(4)
A step estimated with
K
=
16
K{=}16
therefore receives twice the weight of a step estimated with
K
=
8
K{=}8
. The value probe’s predicted
pit
step applies Definition
1
to its predicted values at the evaluated prefixes: it is the first evaluated step at which the maximum of the predictions at that and every later evaluated prefix is at or below
θ
\theta
, and a
pit
whose predictions never meet this condition counts as a miss. The final-label probe is a transformer encoder over the steps with a causal attention mask, a value output and a confidence output, trained on final labels; it predicts the step with the largest drop in its value output
q
t
q_{t}
from the preceding step,
arg
⁡
min
t
⁡
(
q
t
−
q
t
−
1
)
\arg\min_{t}\,(q_{t}-q_{t-1})
. Prior work trains a verifier on final labels to estimate, without sampling, each prefix’s probability of reaching a correct answer
[
Lu et al., 2024
]
.
Distance score.
The distance score in Figure
4
uses the 76
pit
traces, from 74 problems, that have at least one correct trace of the same problem, at layers 8 to 36, under four distance measures; it was computed from hidden states of an earlier extraction whose read positions were not checked. The distance score in Table
10
is computed at the read site, from the stored hidden states that the probes read, on every
pit
trace with at least one correct trace of the same problem. Its AUROC pools the steps of these traces, and
t
/
(
L
−
1
)
t/(L-1)
for step
t
t
of a trace with
L
L
steps is scored in the same way.
Decodability and behavior.
In a study of in-context learning on three model families at 7B to 9B parameters, function vectors steered the output in 5 of 72 task and model cells in which the logit lens, a tuned lens and a two-layer probe all failed to decode the answer
[
Nadaf, 2026
]
. A representation can therefore affect behavior without being decodable by a tested probe.
Appendix C
Proofs
Preliminaries.
A prefix is a finite sequence of tokens, so
s
t
s_{t}
takes values in a countable set and every conditional expectation below conditions on an event of the form
{
s
t
=
s
}
\{s_{t}=s\}
;
h
1
:
t
h_{1:t}
is a deterministic function of
s
t
s_{t}
, so the same holds for it.
Strict propriety pins the population minimizer of the loss in Proposition
1
pointwise, so that minimizer is
𝔼
[
Y
∣
h
1
:
t
]
\mathbb{E}[Y\mid h_{1:t}]
under the law the training set draws from. Reading it as the step’s on-policy value needs one further condition, representation sufficiency:
𝔼
⁡
[
Y
∣
s
t
]
\mathbb{E}[Y\mid s_{t}]
has to be a function of
h
1
:
t
h_{1:t}
, so that the read site keeps whatever the prefix carries about the outcome. This paper does not test that condition, and a last-token read at two fixed layers can discard prefix information that predicts the outcome. Calibration is checked empirically (Table
13
); subject to sufficiency, one final label per trace suffices to supervise the detection task in Section
3
.
Both directions of Proposition
2
’s equivalence follow from the
L
2
L^{2}
projection of
V
t
∗
V^{*}_{t}
onto
σ
⁡
(
s
t
)
\sigma(s_{t})
, the
σ
\sigma
-algebra generated by
s
t
s_{t}
, and the projection is the best square-integrable function of
s
t
s_{t}
, the conditional mean
𝔼
⁡
[
V
t
∗
∣
s
t
]
\mathbb{E}[V^{*}_{t}\mid s_{t}]
; a function of
h
1
:
t
h_{1:t}
does no better, since
σ
(
h
1
:
t
)
⊆
σ
(
s
t
)
\sigma(h_{1:t})\subseteq\sigma(s_{t})
.
Figure
2
shows that
V
∗
V^{*}
immediately before the
pit
step is low and right-skewed, and its excess over
V
t
π
V^{\pi}_{t}
,
m
t
m_{t}
, need not be fixed by the current prefix. The threshold event also depends on the greedy outcome, as Lemma
1
states.
Proof of Proposition
1
.
Throughout,
ℚ
\mathbb{Q}
is the step-weighted law named in the statement: the training set contains every valid step of every trace, so a trace with
n
n
valid steps contributes
n
n
rows, and
ℚ
\mathbb{Q}
is the trace law reweighted by that row count. The weighting changes the marginal over prefixes and nothing else. A prefix
s
t
s_{t}
carries its own step index, so each trace whose prefix at that index is
s
t
s_{t}
contributes exactly one row there; conditioning on
s
t
s_{t}
therefore returns the trace law
π
\pi
given that prefix, and
𝔼
ℚ
​
[
Y
∣
s
t
]
=
𝔼
π
​
[
Y
∣
s
t
]
=
V
t
π
\mathbb{E}_{\mathbb{Q}}[Y\mid s_{t}]=\mathbb{E}_{\pi}[Y\mid s_{t}]=V^{\pi}_{t}
. Conditioning on
h
1
:
t
h_{1:t}
instead gives the corresponding hidden-state conditional mean under the step-weighted law.
Fix a value
h
h
of the hidden prefix and write
q
h
=
𝔼
ℚ
[
Y
∣
h
1
:
t
=
h
]
q_{h}=\mathbb{E}_{\mathbb{Q}}[Y\mid h_{1:t}=h]
. Conditional on
h
1
:
t
=
h
h_{1:t}=h
the label is Bernoulli with mean
q
h
q_{h}
, so the population risk of a candidate
g
g
under a scoring rule
ℓ
\ell
is
R
(
g
)
=
𝔼
ℚ
[
ℓ
(
g
(
h
1
:
t
)
,
Y
)
]
=
𝔼
h
∼
ℚ
[
𝔼
Y
∼
Bern
⁡
(
q
h
)
[
ℓ
(
g
(
h
)
,
Y
)
]
]
.
R(g)=\mathbb{E}_{\mathbb{Q}}\big[\,\ell(g(h_{1:t}),Y)\,\big]=\mathbb{E}_{h\sim\mathbb{Q}}\Big[\;\mathbb{E}_{Y\sim\mathrm{Bern}(q_{h})}\big[\ell(g(h),Y)\big]\;\Big].
The minimization runs over measurable functions, which place no constraint tying the value of
g
g
at one
h
h
to its value at another, so
R
R
is minimized by minimizing the inner expectation separately at each
h
h
.
For the log loss the excess conditional risk at
h
h
is
−
q
h
log
g
⁡
(
h
)
q
h
−
(
1
−
q
h
)
log
1
−
g
⁡
(
h
)
1
−
q
h
=
D
KL
(
Bern
(
q
h
)
∥
Bern
(
g
(
h
)
)
)
≥
0
,
-q_{h}\log\frac{g(h)}{q_{h}}-(1-q_{h})\log\frac{1-g(h)}{1-q_{h}}=D_{\mathrm{KL}}\big(\mathrm{Bern}(q_{h})\,\big\|\,\mathrm{Bern}(g(h))\big)\;\geq\;0,
which is zero only at
g
⁡
(
h
)
=
q
h
g(h)=q_{h}
. The Brier rule is strictly proper as well and has the same minimizer, its excess conditional risk being
(
g
⁡
(
h
)
−
q
h
)
2
(g(h)-q_{h})^{2}
. Both are instances of a strictly proper scoring rule pinning the conditional minimizer at the conditional mean
[
Gneiting and Raftery, 2007
]
. The conditional minimizer equals
q
h
q_{h}
at every
h
h
, so the risk minimizer is
g
⋆
(
h
1
:
t
)
=
𝔼
ℚ
[
Y
∣
h
1
:
t
]
=
Pr
ℚ
(
Y
=
1
∣
h
1
:
t
)
g^{\star}(h_{1:t})=\mathbb{E}_{\mathbb{Q}}[Y\mid h_{1:t}]=\Pr_{\mathbb{Q}}(Y{=}1\mid h_{1:t})
.
The hidden states are a deterministic function of the prefix, so
σ
(
h
1
:
t
)
⊆
σ
(
s
t
)
\sigma(h_{1:t})\subseteq\sigma(s_{t})
, and the tower property gives
g
⋆
(
h
1
:
t
)
=
𝔼
ℚ
[
𝔼
ℚ
[
Y
∣
s
t
]
|
h
1
:
t
]
=
𝔼
ℚ
[
V
t
π
∣
h
1
:
t
]
g^{\star}(h_{1:t})=\mathbb{E}_{\mathbb{Q}}\big[\,\mathbb{E}_{\mathbb{Q}}[Y\mid s_{t}]\,\big|\,h_{1:t}\big]=\mathbb{E}_{\mathbb{Q}}[V^{\pi}_{t}\mid h_{1:t}]
, so
g
⋆
(
h
1
:
t
)
=
V
t
π
g^{\star}(h_{1:t})=V^{\pi}_{t}
almost surely if and only if
𝔼
⁡
[
Y
∣
s
t
]
\mathbb{E}[Y\mid s_{t}]
is
σ
(
h
1
:
t
)
\sigma(h_{1:t})
-measurable up to null sets, which is the representation-sufficiency condition.
∎
Proof of Proposition
2
.
Write
p
=
V
t
π
p=V^{\pi}_{t}
, which is a function of
s
t
s_{t}
, and recall
m
t
=
V
t
∗
−
V
t
π
≥
0
m_{t}=V^{*}_{t}-V^{\pi}_{t}\geq 0
.
The projection identity below holds for every
σ
⁡
(
s
t
)
\sigma(s_{t})
-measurable
f
∈
L
2
f\in L^{2}
, since
V
t
∗
∈
[
0
,
1
]
V^{*}_{t}\in[0,1]
; the projection of
V
t
∗
V^{*}_{t}
onto
σ
⁡
(
s
t
)
\sigma(s_{t})
splits the squared error into the part no such
f
f
can remove and the part that measures the distance of
f
f
from the conditional mean
[
Williams, 1991
, Ch. 9]
:
𝔼
⁡
[
(
V
t
∗
−
f
⁡
(
s
t
)
)
2
]
=
𝔼
⁡
[
Var
⁡
(
V
t
∗
∣
s
t
)
]
⏟
irreducible
+
𝔼
⁡
[
(
𝔼
⁡
[
V
t
∗
∣
s
t
]
−
f
⁡
(
s
t
)
)
2
]
⏟
choice of
​
f
.
\mathbb{E}\big[(V^{*}_{t}-f(s_{t}))^{2}\big]=\underbrace{\mathbb{E}\big[\mathrm{Var}(V^{*}_{t}\mid s_{t})\big]}_{\text{irreducible}}+\underbrace{\mathbb{E}\big[(\mathbb{E}[V^{*}_{t}\mid s_{t}]-f(s_{t}))^{2}\big]}_{\text{choice of }f}.
If
Var
⁡
(
V
t
∗
∣
s
t
)
=
0
\mathrm{Var}(V^{*}_{t}\mid s_{t})=0
almost surely, take
f
=
𝔼
⁡
[
V
t
∗
∣
s
t
]
f=\mathbb{E}[V^{*}_{t}\mid s_{t}]
: both terms vanish, the left side is zero, and so
f
⁡
(
s
t
)
=
V
t
∗
f(s_{t})=V^{*}_{t}
almost surely. Conversely, if some
f
f
makes the left side zero, then both non-negative terms vanish;
𝔼
⁡
[
Var
⁡
(
V
t
∗
∣
s
t
)
]
=
0
\mathbb{E}[\mathrm{Var}(V^{*}_{t}\mid s_{t})]=0
with a non-negative integrand gives
Var
⁡
(
V
t
∗
∣
s
t
)
=
0
\mathrm{Var}(V^{*}_{t}\mid s_{t})=0
almost surely.
The projection uses only the measurability of
f
f
with respect to
σ
⁡
(
s
t
)
\sigma(s_{t})
. A training label and loss select one function from that class but do not add information. The squared-loss optimum over functions of the hidden prefix, where
σ
(
h
1
:
t
)
⊆
σ
(
s
t
)
\sigma(h_{1:t})\subseteq\sigma(s_{t})
, is the projection
𝔼
[
V
t
∗
∣
h
1
:
t
]
\mathbb{E}[V^{*}_{t}\mid h_{1:t}]
, with the same or greater irreducible error.
The same equivalence holds for the discrete
t
pit
t_{\textsc{pit}}
: it takes values in
ℕ
0
∪
{
∞
}
\mathbb{N}_{0}\cup\{\infty\}
, so the argument runs through its conditional law. If
t
pit
=
f
⁡
(
s
t
)
t_{\textsc{pit}}=f(s_{t})
almost surely for a
σ
⁡
(
s
t
)
\sigma(s_{t})
-measurable
f
f
, then conditionally on
s
t
s_{t}
the variable
t
pit
t_{\textsc{pit}}
equals the constant
f
⁡
(
s
t
)
f(s_{t})
almost surely, so its conditional law is the point mass at
f
⁡
(
s
t
)
f(s_{t})
. Conversely, if that conditional law is the point mass at some
c
⁡
(
s
t
)
c(s_{t})
, then
Pr
⁡
(
t
pit
=
c
⁡
(
s
t
)
∣
s
t
)
=
1
\Pr(t_{\textsc{pit}}=c(s_{t})\mid s_{t})=1
almost surely, and taking expectations gives
t
pit
=
c
⁡
(
s
t
)
t_{\textsc{pit}}=c(s_{t})
almost surely, and countability makes the unique-atom selector
c
c
measurable.
Subtracting
V
t
π
V^{\pi}_{t}
does not change conditional variance, because
V
t
π
V^{\pi}_{t}
is
σ
⁡
(
s
t
)
\sigma(s_{t})
-measurable:
Var
⁡
(
m
t
∣
s
t
)
=
Var
⁡
(
V
t
∗
∣
s
t
)
\mathrm{Var}(m_{t}\mid s_{t})=\mathrm{Var}(V^{*}_{t}\mid s_{t})
. The condition
0
<
V
t
π
<
1
0<V^{\pi}_{t}<1
by itself does not imply that either variance is positive. For example, suppose every future reasoning prefix reachable from
s
t
s_{t}
has the same value
p
∈
(
0
,
1
)
p\in(0,1)
until the final answer is sampled. Then a fresh continuation outcome remains random, while
V
t
∗
=
p
V^{*}_{t}=p
and
m
t
=
0
m_{t}=0
are fixed by
s
t
s_{t}
. Positive conditional variance instead requires continuation paths of positive probability that produce different future maxima. In that case, the first term in the projection identity is the irreducible mean-squared error of every prefix-state predictor. A hidden-state predictor can have additional error because
h
1
:
t
h_{1:t}
may discard information from
s
t
s_{t}
. Thus the proposition gives a conditional obstruction to exact recovery. The size of that obstruction depends on
Var
⁡
(
V
t
∗
∣
s
t
)
\mathrm{Var}(V^{*}_{t}\mid s_{t})
;
V
t
π
V^{\pi}_{t}
alone does not determine it.
∎
Lemma 1
(The completed path determines the
pit
)
.
Fix the inclusive crossing test
V
t
∗
≤
θ
V^{*}_{t}\leq\theta
of Definition
1
.
(i)
Let
V
0
π
,
…
,
V
T
π
V^{\pi}_{0},\dots,V^{\pi}_{T}
be the exact value path over the recorded reasoning prefixes used to compute the envelope for a completed incorrect trace, and let
L
=
max
⁡
{
u
∈
{
0
,
…
,
T
}
:
V
u
π
>
θ
}
L=\max\{u\in\{0,\dots,T\}:V^{\pi}_{u}>\theta\}
with
max
⁡
∅
=
−
1
\max\emptyset=-1
. Then
t
pit
=
0
t_{\textsc{pit}}=0
(capability gap) if
L
=
−
1
L=-1
,
t
pit
=
L
+
1
t_{\textsc{pit}}=L+1
(
pit
) if
−
1
<
L
<
T
-1<L<T
, and
t
pit
=
∞
t_{\textsc{pit}}=\infty
(near miss) if
L
=
T
L=T
.
(ii)
Let
G
t
∈
{
0
,
1
}
G_{t}\in\{0,1\}
be the greedy-continuation outcome and
X
t
∼
Bin
⁡
(
K
−
1
,
p
t
)
X_{t}\sim\mathrm{Bin}(K-1,p_{t})
count successes among the independent temperature-
0.7
0.7
rollouts. Then
p
^
t
=
(
G
t
+
X
t
)
/
K
\hat{p}_{t}=(G_{t}+X_{t})/K
and
p
^
t
≤
θ
⇔
X
t
≤
⌊
θ
​
K
⌋
−
G
t
\hat{p}_{t}\leq\theta\iff X_{t}\leq\lfloor\theta K\rfloor-G_{t}
.
Proof.
(i) If
L
=
−
1
L=-1
, every value is at most
θ
\theta
, so the envelope crosses at step
0
0
. If
−
1
<
L
<
T
-1<L<T
, the envelope exceeds
θ
\theta
through
L
L
and is at most
θ
\theta
afterward, so the first crossing is
L
+
1
L+1
. If
L
=
T
L=T
, every candidate crossing has a later value above
θ
\theta
, so the envelope never crosses and
t
pit
=
∞
t_{\textsc{pit}}=\infty
. The three cases of
L
L
correspond one-to-one to the capability-gap,
pit
and near-miss cases of Definition
1
. Under the strict test
V
t
∗
<
θ
V^{*}_{t}<\theta
, the same cases hold with
L
L
taken over
{
u
:
V
u
π
≥
θ
}
\{u:V^{\pi}_{u}\geq\theta\}
.
(ii) The total count is
G
t
+
X
t
G_{t}+X_{t}
, so the threshold equivalence follows by multiplying by
K
K
and using that
X
t
X_{t}
is integer-valued. At
θ
=
0.1
\theta=0.1
, a
K
=
8
K=8
crossing requires
G
t
=
0
G_{t}=0
and
X
t
=
0
X_{t}=0
. At
K
=
16
K=16
, it requires
X
t
≤
1
X_{t}\leq 1
when
G
t
=
0
G_{t}=0
and
X
t
=
0
X_{t}=0
when
G
t
=
1
G_{t}=1
. Thus the mixed rollout design changes both the threshold grid and the sampling law of the success count across depths.
∎
Appendix D
Read-site selection
The confidence, value, combined and pointer probes read hidden states at the read site
𝒮
⋆
=
{
23
,
24
}
\mathcal{S}^{\star}=\{23,24\}
. We select the read site by the detection AUROC of a probe at each layer, using the final label
Y
Y
only. The selection measure is the detection AUROC in the middle step bin, computed within each difficulty group and then averaged, with a probe of the confidence probe’s architecture trained on the hidden states of each layer. The middle bin reduces both the difficulty prior present in early steps and the answer commitment present in the final step. Figure
5
A also shows the same measure for transcoder activations, obtained by applying the published per-layer transcoders to the residual stream before the layer normalization that precedes the MLP, with their activations projected to the width of the hidden states by a fixed random matrix. The transcoders were trained on the output of that normalization, so the transcoder curves do not describe the transcoders at their training site. No result in this paper uses the transcoder curves. We also record predictive
𝒱
\mathcal{V}
-information
[
Xu et al., 2020
,
Ethayarajh et al., 2022
]
; predictive
𝒱
\mathcal{V}
-information peaks at layer 28 at 4B and at layer 18 at 8B and was not used for the selection. We record a usable-information measure because raw mutual information cannot order deterministic layers
[
Pimentel et al., 2020
,
Xu et al., 2020
]
.
Layer selection.
The detection AUROC forms a broad upper-middle-layer plateau and peaks at layer 23 for both model scales, at
0.7264
0.7264
[
0.7079
,
0.7445
]
[0.7079,0.7445]
for 4B and
0.7124
0.7124
[
0.6933
,
0.7295
]
[0.6933,0.7295]
for 8B (Figure
5
A); the interval at the peak overlaps those of most neighbouring layers. The read site
{
23
,
24
}
\{23,24\}
is not distinguishable from layer 23 alone because the four bootstrap intervals, the two at layer 23 above and the two read-site intervals in Table
10
, overlap. This selection uses one measurement per scale with no seed spread, and the two scales, selected separately, peak at the same layer. The upper-middle location is consistent with prior truth and correctness probes
[
Azaria and Mitchell, 2023
,
Marks and Tegmark, 2024
,
Burns et al., 2023
]
. Prior work also reports that the best probe layer tends to be deeper in larger models
[
O’Neill et al., 2025
]
, so we repeat the selection at each scale. Conditional probing measures only the information added beyond a baseline such as the first layer
[
Hewitt et al., 2021
]
, and adjacent residual-stream layers are expected to be redundant. The layer-count sweep tests 2, 3, 5 and 8 adjacent layers centred on the peak. Two layers is the smallest tested layer count whose interval overlaps the interval of the best-scoring layer count, and adding a third changes the score by less than the interval width at both scales (Figure
5
B).
Figure 5:
Read-site selection for Qwen3-4B and Qwen3-8B.
(A)
Detection AUROC of a probe at each layer, on hidden states and on transcoder activations (not used by any result in this paper; see the text of this appendix); on hidden states it forms a broad upper-middle-layer plateau and peaks at layer 23.
(B)
Detection AUROC of a probe on 2, 3, 5 and 8 adjacent layers centred on layer 23; the gain from a third layer over two is smaller than the interval width. Bands and bars are 95% bootstrap intervals that resample held-out traces. We select hidden states from
𝒮
⋆
=
{
23
,
24
}
\mathcal{S}^{\star}=\{23,24\}
.
Read position.
Each read lies at or before the step’s last token. The stored step positions come from tokenizing each step on its own, and the hidden states were extracted in left-padded batches without shifting those positions. Each read therefore lies earlier than the step’s last token by the padding width of its trace, at most 512 tokens. For the final step, the read lies inside the intended step for
51.0
%
51.0\%
of traces at 4B and
51.6
%
51.6\%
at 8B. Tokenizing the steps separately adds a smaller drift, with a median of 3 tokens over 820 step reads in a 40-trace 4B sample. No result was re-scored with corrected positions.
Appendix E
Failure types by problem type
Table
8
reports the capability-gap share of incorrect traces for each problem type in the broad collection. A problem’s type is its DeepMath topic at the second level of that dataset’s hierarchy, or its Hendrycks MATH subject. The association between failure type and problem type is weak at both scales, with Cramér’s
V
V
of
0.095
0.095
at 4B and
0.101
0.101
at 8B over traces with the stored labels, and
0.099
0.099
and
0.110
0.110
with corrected labels (Appendix
B
). The DeepMath topics span a narrow range of capability-gap shares, with Discrete Mathematics above the pooled share and Calculus and Number Theory below it at both scales. The Hendrycks MATH subjects have higher capability-gap shares. The two sources also differ in difficulty scale, so this table does not separate source from topic, and the pooled
V
V
carries the same limitation.
Table 8:
Capability-gap share of incorrect traces by problem type in the broad collection at both model scales, with the stored labels and
95
%
95\%
problem-clustered bootstrap intervals. The pooled shares are
0.5555
0.5555
at 4B and
0.5321
0.5321
at 8B. DeepMath topics and Hendrycks MATH subjects are listed separately because the two sources differ in difficulty scale.
problem type
4B problems
4B share
8B problems
8B share
DeepMath topics
Algebra
4,136
0.563 [0.549, 0.577]
3,728
0.537 [0.522, 0.552]
Calculus
2,564
0.511 [0.494, 0.530]
2,256
0.477 [0.457, 0.497]
Other
928
0.542 [0.513, 0.572]
826
0.510 [0.478, 0.541]
Discrete Mathematics
890
0.603 [0.573, 0.632]
801
0.599 [0.564, 0.627]
Geometry
856
0.555 [0.524, 0.584]
769
0.535 [0.506, 0.569]
Applied Mathematics
586
0.561 [0.523, 0.596]
524
0.533 [0.491, 0.571]
Number Theory
424
0.495 [0.447, 0.538]
405
0.469 [0.424, 0.513]
Differential Equations
239
0.512 [0.448, 0.570]
195
0.487 [0.418, 0.549]
Precalculus
178
0.483 [0.406, 0.554]
154
0.488 [0.408, 0.566]
Hendrycks MATH subjects
geometry
163
0.772 [0.722, 0.818]
159
0.789 [0.737, 0.839]
intermediate algebra
84
0.566 [0.454, 0.670]
83
0.635 [0.534, 0.733]
counting and probability
78
0.810 [0.734, 0.876]
64
0.803 [0.725, 0.872]
precalculus
68
0.587 [0.458, 0.693]
56
0.561 [0.443, 0.671]
number theory
60
0.641 [0.532, 0.745]
57
0.655 [0.529, 0.757]
prealgebra
38
0.768 [0.660, 0.859]
30
0.706 [0.560, 0.844]
algebra
18
0.880 [0.756, 0.967]
16
0.682 [0.488, 0.837]
Appendix F
Supporting tables
Table 9:
Sizes of the trace sets and of the populations drawn from them, and the use of each population. The broad collection labels every incorrect trace at both model scales. The gold collection is a 4B collection with half as many rollouts per evaluated prefix, and the
pit
steps of its
pit
s are the reference
pit
steps. A later table reports a separate
n
n
when its evaluation population differs from the corresponding row here.
set
population
used for
4B
8B
all traces
every sampled trace (35,854 problems)
training the confidence and combined probes
144,000
144,000
held-out traces
traces whose problems were held out by at least one of the five training seeds
detection and calibration of the confidence probe
119,736
119,756
broad collection
every incorrect trace
shares of the failure types (Figure
2
)
28,699
24,871
held-out incorrect traces
incorrect traces among the held-out traces
miss rates by failure type (Section
3
)
23,837
20,590
held-out
pit
s
pit
s of problems outside the training split
pointer probe (4B); value probe, per seed (8B)
2,289
2,805–2,918
classifier problems
one incorrect trace per problem, capability gaps and
pit
s
failure-type classifier (Appendix
B.1
)
1,722
6,372
gold collection
every trace of the collection
reference
pit
steps
5,380
not collected
pit
s
reference
pit
steps
pointer probe trained without gold problems; final-label comparison
818
not collected
Table 10:
Supporting measurements cited in the main text, at both model scales. Intervals are 95% bootstrap intervals that resample problems unless a note says otherwise, and
±
\pm
values are sample standard deviations over seeds (seed axes in Appendix
B
).
measurement
4B
8B
interpretation
Failure types and detection
detection AUROC of the read site
a
0.7245 [0.7047, 0.7432]
0.7149 [0.6960, 0.7326]
read site chosen from the final label only
share of
pit
s whose
pit
step equals
arg
⁡
min
t
⁡
V
^
t
\arg\min_{t}\hat{V}_{t}
0.154
0.125
the
arg
⁡
min
\arg\min
step equals the
pit
step for a minority of
pit
s
combined probe
−
-
confidence probe, detection AUROC on held-out problems
−
0.026
-0.026
[
−
0.029
-0.029
,
−
0.022
-0.022
]
−
0.025
-0.025
[
−
0.029
-0.029
,
−
0.021
-0.021
]
the confidence probe has the higher detection AUROC
confidence probe’s predicted correctness at the
pit
step minus other steps
b
−
0.0206
-0.0206
[
−
0.0272
-0.0272
,
−
0.0140
-0.0140
]
−
0.0351
-0.0351
[
−
0.0372
-0.0372
,
−
0.0327
-0.0327
]
lower at the
pit
step
same difference against the position-matched steps
b
−
0.0018
-0.0018
[
−
0.0055
-0.0055
,
+
0.0022
+0.0022
]
−
0.0051
-0.0051
[
−
0.0062
-0.0062
,
−
0.0040
-0.0040
]
8B: the decrease remains; 4B: no detected difference
Localization
final-label comparison, value probe
−
-
final-label probe, pooled over all reference
pit
steps (two input sets)
c
+
0.0609
+0.0609
[
+
0.0293
+0.0293
,
+
0.0929
+0.0929
]
;
+
0.0433
+0.0433
[
+
0.0137
+0.0137
,
+
0.0731
+0.0731
]
not evaluated
pooled evaluation includes training traces of the value probe; on the problems held out from its training the interval excludes zero in 1 of 5 seeds (first input set) and 0 of 5 (second)
value probe, AUROC of near misses against
pit
s by its prediction at the last evaluated step
0.9148
±
0.0054
0.9148\pm 0.0054
0.9062
±
0.0079
0.9062\pm 0.0079
separates near misses from
pit
s
value probe, per-step absolute error versus predicting zero and a monotone fit
e
0.1227
±
0.0052
0.1227\pm 0.0052
versus
0.1040
±
0.0019
0.1040\pm 0.0019
and
0.0830
±
0.0014
0.0830\pm 0.0014
0.1261
±
0.0040
0.1261\pm 0.0040
versus
0.1091
±
0.0034
0.1091\pm 0.0034
and
0.0962
±
0.0024
0.0962\pm 0.0024
predicting zero and the monotone fit each have lower error than the value probe in every seed
value probe versus length rule, Hit@
±
2
\pm 2
on each seed’s held-out
pit
s, two input sets
d
Table
12
0.4293
±
0.0223
0.4293\pm 0.0223
and
0.4046
±
0.0162
0.4046\pm 0.0162
versus
0.5028
±
0.0108
0.5028\pm 0.0108
; 0 of 5 seeds each
below the length rule at 8B
pit
s located within two steps by exactly one of the pointer probe and the length rule, 10 runs
723 to 857 of 2,289
pit
s (31.6 to 37.4%)
not evaluated
about a third of
pit
s in each run
distance score at the read site versus
t
/
(
L
−
1
)
t/(L-1)
, AUROC of the
pit
step against the other steps
f
0.55 versus 0.63 (gold); 0.55 versus 0.69 (broad)
0.56 versus 0.74 (broad)
lower than
t
/
(
L
−
1
)
t/(L-1)
in each collection and at each scale
rollout search replay, reference
pit
step within two steps at
6.6
6.6
evaluated prefixes per trace
0.804
not evaluated
reads the estimates that define the labels; not comparable with a probe’s Hit@
±
2
\pm 2
refinement-depth agreement
0.754 (0.638 at
K
=
8
K{=}8
)
not evaluated
point estimates against a deeper reference; no interval
Notes.
a
Intervals resample held-out traces.
b
Each trace uses only the seeds that held it out, and
pit
steps at the first or last step of a trace are excluded; the rows cover 682 reference
pit
steps at 4B and 7,277
pit
s of the broad collection at 8B, so the two scales are not a matched comparison.
c
The final-label comparison is evaluated only at 4B; intervals of the pooled evaluation resample traces.
d
At 8B, the row compares seed means on 2,805 to 2,918 held-out
pit
s of the broad collection per seed and has no per-trace interval. The value-probe rows use the first input set except where two input sets are named.
e
The monotone fit is the best non-increasing least-squares fit to each trace’s rollout rates.
f
The distance score takes the highest of four distance measures; the comparison scores step
t
t
of a trace with
L
L
steps by
t
/
(
L
−
1
)
t/(L-1)
. The row uses the
pit
traces with at least one correct trace of the same problem: 593 in the gold collection, 7,987 in the broad collection at 4B and 6,881 at 8B.
Table 11:
Values behind Figure
3
: confidence-probe predictions at the final step, on the broad collection at both model scales, on held-out problems of the problem split. An incorrect trace is missed when its predicted correctness is at least the cutoff,
0.5
0.5
. The binned rows give the miss rates of
pit
s and near misses within bins of the best reachable value at step 0,
V
0
∗
V^{*}_{0}
, with the number of traces in each bin in parentheses. The AUROC rows score each probe by its final-step score on its own held-out traces. The last block is the difference between
pit
s and near misses after controls, from a logistic model of trace misses on failure type, trace length, answer position, difficulty and
V
0
∗
V^{*}_{0}
(Appendix
B
). Intervals are 95% problem-clustered bootstraps.
quantity
4B
8B
miss rate, capability gap
0.717
​
[
0.706
,
0.729
]
0.717\ [0.706,0.729]
0.797
​
[
0.785
,
0.808
]
0.797\ [0.785,0.808]
miss rate,
pit
0.714
​
[
0.703
,
0.724
]
0.714\ [0.703,0.724]
0.815
​
[
0.805
,
0.824
]
0.815\ [0.805,0.824]
miss rate, near miss
0.490
​
[
0.460
,
0.521
]
0.490\ [0.460,0.521]
0.466
​
[
0.442
,
0.490
]
0.466\ [0.442,0.490]
n
n
(incorrect traces)
23,837
20,590
V
0
∗
≤
0.25
V^{*}_{0}\leq 0.25
,
pit
s
0.707
​
[
0.690
,
0.723
]
0.707[0.690,0.723]
(3,160)
0.787
​
[
0.770
,
0.804
]
0.787[0.770,0.804]
(2,548)
near misses
0.436
​
[
0.329
,
0.547
]
0.436[0.329,0.547]
(78)
0.449
​
[
0.357
,
0.549
]
0.449[0.357,0.549]
(118)
0.25
<
V
0
∗
≤
0.50
0.25<V^{*}_{0}\leq 0.50
,
pit
s
0.720
​
[
0.701
,
0.737
]
0.720[0.701,0.737]
(2,931)
0.834
​
[
0.818
,
0.849
]
0.834[0.818,0.849]
(2,415)
near misses
0.424
​
[
0.357
,
0.491
]
0.424[0.357,0.491]
(205)
0.468
​
[
0.410
,
0.526
]
0.468[0.410,0.526]
(299)
0.50
<
V
0
∗
≤
0.75
0.50<V^{*}_{0}\leq 0.75
,
pit
s
0.722
​
[
0.699
,
0.745
]
0.722[0.699,0.745]
(1,591)
0.822
​
[
0.801
,
0.841
]
0.822[0.801,0.841]
(1,359)
near misses
0.481
​
[
0.410
,
0.548
]
0.481[0.410,0.548]
(216)
0.430
​
[
0.371
,
0.487
]
0.430[0.371,0.487]
(323)
0.75
<
V
0
∗
0.75<V^{*}_{0}
,
pit
s
0.709
​
[
0.687
,
0.734
]
0.709[0.687,0.734]
(1,682)
0.823
​
[
0.803
,
0.843
]
0.823[0.803,0.843]
(1,568)
near misses
0.517
​
[
0.479
,
0.556
]
0.517[0.479,0.556]
(722)
0.479
​
[
0.449
,
0.511
]
0.479[0.449,0.511]
(1,047)
AUROC of
pit
s against near misses, confidence probe
0.670
​
[
0.653
,
0.687
]
0.670\ [0.653,0.687]
0.760
​
[
0.746
,
0.773
]
0.760\ [0.746,0.773]
n
n
(
pit
s; near misses)
9,364; 1,221
7,890; 1,787
AUROC of
pit
s against near misses, combined probe
0.364
​
[
0.349
,
0.378
]
0.364\ [0.349,0.378]
0.403
​
[
0.390
,
0.416
]
0.403\ [0.390,0.416]
n
n
(
pit
s; near misses)
9,344; 1,254
7,903; 1,805
pit
s
−
-
near misses, after controls
+
0.0372
​
[
+
0.0116
,
+
0.0641
]
+0.0372\ [+0.0116,+0.0641]
+
0.1246
​
[
+
0.1043
,
+
0.1428
]
+0.1246\ [+0.1043,+0.1428]
n
n
(traces in the logistic model)
a
23,820
20,590
pit
s
−
-
near misses, after controls, Brier loss
+
0.052
​
[
+
0.028
,
+
0.076
]
+0.052\ [+0.028,+0.076]
+
0.123
​
[
+
0.103
,
+
0.143
]
+0.123\ [+0.103,+0.143]
Notes.
a
The model omits 17 traces at 4B that contain no final answer, for which answer position is undefined.
Table 12:
Paired comparisons with the length rule, at 4B throughout. Each comparison scores the probe and the length rule on the same
pit
s; intervals are 95% problem-clustered bootstraps of the per-trace difference where given.
comparison
pit
s
probe
length rule
difference
runs above rule
pointer probe, held-out
pit
s of the broad collection
a
2,289
0.4632
±
0.0134
0.4632\pm 0.0134
0.4692
−
0.0060
-0.0060
[
−
0.0260
-0.0260
,
+
0.0141
+0.0141
]
0 of 10
pointer probe trained without gold problems
818
0.4293
±
0.0120
0.4293\pm 0.0120
0.4462
−
0.0169
-0.0169
[
−
0.0473
-0.0473
,
+
0.0131
+0.0131
]
0 of 5
final-label comparison, held-out: value probe
b
205–242
0.3640; 0.3402
0.4812
−
0.166
-0.166
to
−
0.084
-0.084
;
−
0.182
-0.182
to
−
0.113
-0.113
0 of 10
final-label comparison, held-out: final-label probe
b
205–242
0.3041; 0.3423
0.4812
−
0.216
-0.216
to
−
0.124
-0.124
;
−
0.170
-0.170
to
−
0.116
-0.116
0 of 10
final-label comparison, pooled, training traces included
c
818
0.3186–0.3795
0.4462
−
0.128
-0.128
to
−
0.067
-0.067
0 of 20
Notes.
All retraining uses seeds
{
42,137,271,314,577
}
\{42,137,271,314,577\}
.
a
Ten runs, five seeds under each of two weightings of the failure-type loss; the probe and difference cells report the inverse-frequency weights, and the uniform weights score
0.4524
±
0.0111
0.4524\pm 0.0111
. The ensemble, the average of the five pointer probes of one weighting, exceeds the length rule by
+
0.0262
​
[
+
0.0022
,
+
0.0495
]
+0.0262\,[+0.0022,+0.0495]
with inverse-frequency weights and by
+
0.0166
​
[
−
0.0065
,
+
0.0400
]
+0.0166\,[-0.0065,+0.0400]
, an interval that contains zero, with uniform weights.
b
Each seed is scored on the reference
pit
steps of the problems held out from the value probe’s training for that seed; the difference column gives the range of the five per-seed differences, each with an interval below zero. The two values in a cell are the two input sets.
c
Every seed is scored on all reference
pit
steps, which include that seed’s training traces; every per-seed interval in this row lies below zero.
Table 13:
Detection by the confidence probe at the final step and comparison with the text baseline, on held-out problems of the problem split at both model scales. The upper block reports the mean
±
\pm
standard deviation over five seeds. AUROC after controls scores the same five-seed predictions after the five control variables of Appendix
B
are removed from them. Expected calibration error uses ten equal-width bins on held-out scores, before and after temperature scaling. The lower block gives the held-out detection AUROC of the text baseline and of a logistic regression on the same features, the paired difference between the confidence probe and the text baseline, and the gain from adding the confidence probe’s score to the text baseline’s features; the lower block’s intervals are 95% problem-clustered bootstraps. Appendix
B
reports the trace split as a leakage comparison.
scale
loss
AUROC
AUROC after controls
ECE
ECE after scaling
4B
BCE (main)
0.8136
±
0.0049
0.8136\pm 0.0049
0.7291
±
0.0042
0.7291\pm 0.0042
0.0143
±
0.0040
0.0143\pm 0.0040
0.0103
0.0103
8B
BCE (main)
0.8088
±
0.0084
0.8088\pm 0.0084
0.7221
±
0.0149
0.7221\pm 0.0149
0.0243
±
0.0111
0.0243\pm 0.0111
0.0092
0.0092
4B
Brier (robustness)
0.8107
±
0.0046
0.8107\pm 0.0046
0.7297
±
0.0036
0.7297\pm 0.0036
0.0273
±
0.0103
0.0273\pm 0.0103
0.0215
0.0215
8B
Brier (robustness)
0.8085
±
0.0047
0.8085\pm 0.0047
0.7345
±
0.0029
0.7345\pm 0.0029
0.0229
±
0.0061
0.0229\pm 0.0061
0.0107
0.0107
4B
8B
text baseline (gradient-boosted), AUROC
0.7783
0.7783
0.7725
0.7725
logistic regression on the same features, AUROC
0.7548
​
[
0.7488
,
0.7609
]
0.7548\ [0.7488,0.7609]
0.7379
​
[
0.7312
,
0.7442
]
0.7379\ [0.7312,0.7442]
confidence probe
−
-
text baseline, BCE
+
0.0353
​
[
+
0.0319
,
+
0.0387
]
+0.0353\ [+0.0319,+0.0387]
+
0.0362
​
[
+
0.0324
,
+
0.0403
]
+0.0362\ [+0.0324,+0.0403]
confidence probe
−
-
text baseline, Brier
+
0.0324
​
[
+
0.0290
,
+
0.0357
]
+0.0324\ [+0.0290,+0.0357]
+
0.0359
​
[
+
0.0323
,
+
0.0397
]
+0.0359\ [+0.0323,+0.0397]
gain from adding the probe’s score to the text baseline, BCE
+
0.0369
​
[
+
0.0335
,
+
0.0402
]
+0.0369\ [+0.0335,+0.0402]
+
0.0406
​
[
+
0.0369
,
+
0.0445
]
+0.0406\ [+0.0369,+0.0445]
gain from adding the probe’s score to the text baseline, Brier
+
0.0338
​
[
+
0.0305
,
+
0.0370
]
+0.0338\ [+0.0305,+0.0370]
+
0.0393
​
[
+
0.0357
,
+
0.0430
]
+0.0393\ [+0.0357,+0.0430]
Notes.
The confidence probe’s seed identities are not recorded, so the overlap between its seeds and the value probe’s seeds is unknown.