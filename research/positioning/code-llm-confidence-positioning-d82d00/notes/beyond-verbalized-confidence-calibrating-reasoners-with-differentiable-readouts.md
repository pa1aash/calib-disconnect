---
title: 'Beyond Verbalized Confidence: Calibrating Reasoners with Differentiable Readouts'
id: beyond-verbalized-confidence-calibrating-reasoners-with-differentiable-readouts
tags:
- code-llm-confidence-positioning-d82d00
- trained-stated-confidence
- cc-1-gapfill
created: '2026-11-10T08:55:06.932417Z'
updated: '2026-11-10T08:58:10.790411Z'
source: https://arxiv.org/html/2609.34857
source_domain: arxiv.org
fetched_at: '2026-11-10T08:55:06.931847Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'CREDO (arXiv 2609.34857, FULL TEXT via arXiv HTML): RLVR-trained confidence
  for Qwen3-8B on math (DeepScaleR) and code (DeepCoder train; eval on DeepCoder test,
  LiveCodeBench v5/v6, HumanEval+). Baselines RLCR and DCPO train a verbalized numeral
  against execution-graded correctness; CREDO reads confidence from a reserved token
  pair and trains it by differentiable regression. Table 1 reports Acc/ECE/AUROC/Brier
  on code; in-domain code CREDO AUROC .850 vs RLCR .815, DCPO .776, GRPO .753, base
  .690. No probe or hidden-state comparison (searched: probe, hidden state, residual:
  0 hits). Bears on gap cc-1/1: trained stated confidence on code with execution labels
  and AUROC reported EXISTS (one model, no probe, no base/instruct pair), so the L2
  claim ''no code study reports discrimination after training stated confidence''
  is NOT clean; pivot 3 not triggered (no probe arm).'
---

Beyond Verbalized Confidence: Calibrating Reasoners with Differentiable Readouts
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2609.34857v1 [cs.LG] 28 Sep 2026
Beyond Verbalized Confidence: Calibrating Reasoners with Differentiable Readouts
Chenxiao Fan
Affiliation:
University of Science and Technology of China
Affiliation:
Qwen Business Unit of Alibaba
Email:
simonfan@mail.ustc.edu.cn
Chongming Gao
Affiliation:
University of Science and Technology of China
Gangyi Zhang
Affiliation:
Qwen Business Unit of Alibaba
Leyang Shen
Affiliation:
National University of Singapore
Yaxin Gong
Affiliation:
University of Science and Technology of China
Jiamin Wang
Affiliation:
University of Science and Technology of China
Jiakai Wang
Affiliation:
Qwen Business Unit of Alibaba
Dong Wang
Affiliation:
Qwen Business Unit of Alibaba
Yang Liu
Affiliation:
Qwen Business Unit of Alibaba
Fuli Feng
Affiliation:
University of Science and Technology of China
Xiangnan He
Affiliation:
University of Science and Technology of China
Abstract
Reinforcement learning with verifiable rewards (RLVR) trains reasoning models
to produce correct answers, but does not ensure that their stated confidence
is calibrated. The resulting models are systematically overconfident.
Recent methods train calibration inside the RLVR loop by having the model
state a numerical confidence alongside its answer, but they all obtain the
confidence by sampling it as text.
This choice imposes two costs: a sampled confidence introduces variance and in
practice collapses to a handful of distinct values, and sampling makes the
confidence non-differentiable, forcing the calibration loss through a scalar
reward.
We propose
CREDO
(Confidence REaDOut) to replace sampling with a
deterministic readout. While RLVR optimizes correctness, CREDO reads the
confidence from a dedicated token pair in the model’s output distribution and
trains it by differentiable regression.
CREDO further turns the trained confidence into a signal for accuracy,
weighting rollouts by how far confidence and outcome disagree, so that
accuracy and calibration improve together.
Across mathematical and code reasoning, CREDO attains the best accuracy and
calibration, and the gains extend to abstention and selective prediction.
1
Introduction
Reinforcement learning with verifiable rewards (RLVR) has become the standard
recipe for training reasoning models
(
Shao et al., 2024
;
Guo et al., 2025
)
.
Answers in mathematics and code can be checked automatically, so the training
reward is simply whether the answer is correct.
This produces strong reasoners, but the reward carries no signal about how
confident the model should be in any particular answer. Models trained this way
are systematically overconfident
(
Yang et al., 2024
;
Bereket and Leskovec, 2025
;
Mei et al., 2025
)
.
Overconfidence has practical costs: downstream systems route answers by their
stated confidence, so a confidently wrong answer passes through the filters
meant to catch it
(
Geifman and El-Yaniv, 2017
;
Kirichenko et al., 2025
)
.
The remedy is calibration: a model’s stated confidence should match how
often it is actually correct, so that when it reports 0.9, roughly nine in ten
of those answers are right
(
DeGroot and Fienberg, 1983
;
Guo et al., 2017
)
.
Calibration does not emerge from a correctness reward, so it has to be trained
for.
For calibration to be trainable, the model must produce a confidence estimate
alongside each answer (Figure
1
a).
One approach reads confidence from the model’s generation probabilities
(
Fomicheva et al., 2020
)
, but these reflect the likelihood
of the generated text rather than the probability of being correct.
Recent methods instead ask the model to state a numerical confidence after its
answer, scored by a reward based on a proper scoring rule
(
Gneiting and Raftery, 2007
)
.
Several methods along this route have refined the reward design and the balance
between correctness and calibration
(
Damani et al., 2026
;
Ma et al., 2026
;
Xu et al., 2024
;
Bani-Harouni et al., 2026
;
Leng et al., 2025
)
.
Despite their differences, these methods share one choice: the confidence
is a
numeral sampled as text
, which forces the calibration loss to work
through a scalar reward (Figure
1
b).
Figure 1:
(a)
The calibration task: a model answers and reports a
confidence; calibration means the reported probability matches observed
correctness.
(b)
Verbalized methods sample the confidence as text and
train it through a scalar reward. CREDO reads the relative probability of a
pair of reserved tokens and trains it by direct regression from the calibration
loss.
(c)
Confidence distributions on code. Verbalized reports (GRPO, RLCR, DCPO)
concentrate on a few values shared by correct and incorrect answers, even when
calibration is trained explicitly (RLCR, DCPO). The readout (CREDO) spreads
across the full range.
This choice imposes two costs. First, a sampled confidence introduces variance
that persists as long as the report is stochastic. In practice, the reported
confidence collapses to a handful of distinct values, and correct and incorrect
answers end up sharing the same confidence (Figure
1
c).
Second, sampling makes the confidence non-differentiable, forcing the
calibration loss to work through a scalar reward rather than a direct gradient.
The resulting gradient estimate carries additional variance from the report,
making calibration harder to learn.
Both costs follow from verbalizing the confidence; redesigning the reward
cannot remove them.
We propose CREDO (Confidence REaDOut),
1
1
1
The name also reads as the Latin
credo
, “I believe.”
which reads the confidence directly from the
output distribution rather than sampling it.
While RLVR optimizes correctness, CREDO sets aside a pair of reserved tokens
and takes their relative probability as the confidence, trained by
differentiable regression (Figure
1
b).
The readout is deterministic and directly differentiable, so the calibration
loss trains it by gradient descent.
CREDO further turns the trained confidence into a signal for accuracy.
A confident mistake or an unexpected success is more informative than a rollout
where confidence and outcome already agree, so CREDO weights learning on the
answer by the size of the discrepancy.
Accuracy and calibration improve together in both domains.
Our main contributions are as follows:
•
We show that sampling the confidence as text imposes two costs: the
report introduces variance and in practice collapses to a handful of distinct
values, and the sampling step makes the confidence non-differentiable, forcing
the calibration loss through a scalar reward.
•
We propose CREDO, which reads the confidence as the relative probability
between a pair of reserved tokens and trains it by differentiable regression,
giving the calibration loss a direct gradient path. The policy gradient
continues to handle correctness and credit assignment.
•
We turn the trained confidence into a signal for accuracy, weighting
each rollout by the gap between confidence and outcome. The weighting improves
accuracy in both domains.
•
Across mathematical and code reasoning, CREDO attains the best accuracy
and calibration. Ablations isolate the contributions of the readout and the
weighting, and the improved calibration pays off downstream in abstention and
selective prediction.
2
Confidence channels and their costs
We start from the RLVR setup and the calibration objective
(§
2.1
). The rest of the section identifies the channel choice
behind verbalized confidence (§
2.2
), analyzes its two costs
(§
2.3
), and derives three requirements for removing them
(§
2.4
).
2.1
Setup: RLVR and the calibration objective
We work in the GRPO form of RLVR
(
Shao et al., 2024
)
.
For a question
x
x
, the policy
π
θ
\pi_{\theta}
samples a group of
G
G
rollouts
o
1
,
…
,
o
G
o_{1},\dots,o_{G}
, and a verifier scores each one for correctness,
a
i
=
𝟙
[
y
i
≡
y
∗
]
a_{i}=\mathbb{1}[y_{i}\equiv y^{\ast}]
, where
y
i
y_{i}
is the answer extracted from
o
i
o_{i}
and
y
∗
y^{\ast}
the reference answer. The policy maximizes the clipped
objective of
Schulman et al. (2017)
, using the group as the baseline:
𝒥
⁡
(
θ
)
=
𝔼
⁡
[
1
G
​
∑
i
=
1
G
1
|
o
i
|
​
∑
k
∈
o
i
min
⁡
(
ρ
i
,
k
​
A
^
i
,
k
,
clip
⁡
(
ρ
i
,
k
,
1
±
ϵ
)
​
A
^
i
,
k
)
]
,
A
^
i
,
k
=
A
^
i
=
r
i
−
r
¯
std
⁡
(
r
)
.
\mathcal{J}(\theta)=\mathbb{E}\Big[\tfrac{1}{G}\sum_{i=1}^{G}\tfrac{1}{|o_{i}|}\sum_{k\in o_{i}}\min\big(\rho_{i,k}\hat{A}_{i,k},\ \mathrm{clip}(\rho_{i,k},1\pm\epsilon)\,\hat{A}_{i,k}\big)\Big],\quad\hat{A}_{i,k}=\hat{A}_{i}=\frac{r_{i}-\bar{r}}{\mathrm{std}(r)}.
(1)
Here
ρ
i
,
k
\rho_{i,k}
is the token-level importance ratio,
ϵ
\epsilon
the clipping
range, and
r
¯
\bar{r}
and
std
⁡
(
r
)
\mathrm{std}(r)
the mean and standard deviation of the group’s
rewards. The reward is the correctness score,
r
i
=
a
i
r_{i}=a_{i}
. In standard GRPO every
token of a rollout shares the same
A
^
i
\hat{A}_{i}
.
The verifier’s signal is not differentiable in the parameters, so training on
it runs through the policy gradient.
A calibrated model must also report a scalar
q
∈
[
0
,
1
]
q\in[0,1]
alongside its answer,
and the report must be right as often as it claims:
𝔼
⁡
[
a
∣
q
=
v
]
=
v
,
∀
v
∈
[
0
,
1
]
.
\mathbb{E}[a\mid q=v]=v,\qquad\forall v\in[0,1].
(2)
The standard way to train toward equation
2
is a strictly proper scoring
rule, whose expectation is uniquely minimized at
𝔼
⁡
[
a
∣
q
]
\mathbb{E}[a\mid q]
(
Gneiting and Raftery, 2007
)
; the Brier score
(
q
−
a
)
2
(q-a)^{2}
is the canonical example
(
Brier, 1950
)
.
RLVR on its own does not target equation
2
. Its reward depends only on correctness and is indifferent to the model’s
confidence, so nothing in the objective pushes a confident error down
(
Damani et al., 2026
)
.
2.2
The verbalized channel
A confidence report has two design choices: where the confidence comes from
and how it is trained.
Definition 1
(confidence channel)
.
A
confidence channel
is a pair
(
ℰ
,
𝒯
)
(\mathcal{E},\mathcal{T})
: an emission map
ℰ
\mathcal{E}
from the rollout prefix to a scalar report, and a training path
𝒯
\mathcal{T}
, the route by which the calibration objective reaches the
report’s value.
The methods that train a model to state its confidence inside RLVR make the
same pair of choices. The confidence is written out as a numeral in the text,
ℰ
verb
:
q
^
=
parse
(
s
)
,
s
∼
π
θ
(
⋅
∣
h
)
,
\mathcal{E}^{\mathrm{verb}}:\quad\hat{q}=\mathrm{parse}(s),\qquad s\sim\pi_{\theta}(\cdot\mid h),
(3)
where
h
=
(
x
,
y
,
…
)
h=(x,y,\dots)
is the rollout prefix up to the confidence slot. The
model generates a rollout containing a solution
y
y
to
x
x
, samples a numeral
s
s
(say “0.9”) at the confidence slot, and parses it into a
report
q
^
\hat{q}
. We call a channel whose emission includes a sampling step a
verbalized channel
.
This choice of
ℰ
\mathcal{E}
determines
𝒯
\mathcal{T}
. Sampling makes the
realized value of
q
^
\hat{q}
non-differentiable in the parameters, so the
calibration signal can only enter equation
1
as a scalar reward.
RLCR
(
Damani et al., 2026
)
and DCPO
(
Ma et al., 2026
)
are the two representative methods
along this route,
r
RLCR
\displaystyle r^{\mathrm{RLCR}}
=
a
−
(
q
^
−
a
)
2
,
\displaystyle=a-(\hat{q}-a)^{2},
(4)
r
reason
DCPO
\displaystyle r^{\mathrm{DCPO}}_{\mathrm{reason}}
=
a
,
r
DCPO
conf
=
−
|
q
^
−
R
I
​
G
|
,
R
I
​
G
=
λ
R
~
G
+
(
1
−
λ
)
a
,
\displaystyle=a,\qquad r^{\mathrm{DCPO}}_{\mathrm{conf}}=-\big|\hat{q}-R_{IG}\big|,\qquad R_{IG}=\lambda\tilde{R}_{G}+(1-\lambda)a,
where
R
~
G
\tilde{R}_{G}
is the group’s mean accuracy and
λ
\lambda
its
mixing weight.
The first couples the calibration term into a single reward; the second scores
the two segments separately and mixes the target. The disagreements are all
internal to the reward, but the channel is shared: every verbalized variant
uses the same emission and training path
(
Xu et al., 2024
;
Bani-Harouni et al., 2026
;
Leng et al., 2025
;
Stengel-Eskin et al., 2024
;
Zhang et al., 2026
)
.
In both analyses, the optimal report is calibrated and the calibration term
does not hurt accuracy
(
Damani et al., 2026
;
Ma et al., 2026
)
.
These analyses validate the reward design but leave the channel unexamined.
2.3
Costs of the verbalized channel
Each component of the verbalized channel carries a cost.
The first falls on the emission
ℰ
\mathcal{E}
(proofs of all propositions are in Appendix
A
).
Proposition 1
(a verbalized report pays a variance tax or determinizes)
.
Fix a rollout prefix and let
q
^
\hat{q}
be the parsed report of equation
3
,
with conditional mean
q
¯
\bar{q}
and variance
v
v
. Every verbalized policy either
pays a per-prefix tax that persists as long as the report is stochastic, or
determinizes its per-prefix report distribution. Under the squared loss the tax
is exactly
v
v
, since
𝔼
⁡
[
(
q
^
−
t
)
2
]
=
(
q
¯
−
t
)
2
+
v
\mathbb{E}[(\hat{q}-t)^{2}]=(\bar{q}-t)^{2}+v
for any target
t
∈
[
0
,
1
]
t\in[0,1]
; under any strictly convex loss
ℓ
\ell
, Jensen’s inequality gives
𝔼
⁡
[
ℓ
⁡
(
q
^
,
t
)
]
−
ℓ
⁡
(
q
¯
,
t
)
>
0
\mathbb{E}[\ell(\hat{q},t)]-\ell(\bar{q},t)>0
.
Proposition
1
leaves two outcomes: variance or
determinization. Determinization avoids the tax but does not by itself prevent
different prefixes from using different values.
Empirically, however, reports cluster onto a handful of values,
so correct and incorrect answers share the same confidence
(Figure
2
). The collapse is visible already in an untrained
base model, and training does not spread the values out: GRPO, RLCR, and DCPO
all have effective levels in single digits.
Figure 2:
Collapse of the verbalized channel, with CREDO for contrast. Effective levels
=
1
/
∑
v
p
v
2
=1/\sum_{v}p_{v}^{2}
(equiprobable-level
equivalent); top-value share = pool fraction of the most frequent value; tie
tax = AUROC lost to exactly equal reports.
The variance can be avoided if the report is not sampled but computed. We call
a channel whose report is a
deterministic functional of the output distribution a
readout channel
(the rightmost group of Figure
2
).
Even the conditional mean of a verbalized channel is such a functional and
removes the variance, but it cannot be optimized through the reward, which only
observes sampled values. Removing the variance is not enough; the
calibration loss must also reach the report directly.
The second cost falls on
𝒯
\mathcal{T}
: how the calibration loss trains the
report.
Proposition 2
(gradient availability)
.
Fix a calibration loss
ℓ
\ell
. A sampled report admits no unbiased pathwise
gradient estimator, so
ℓ
\ell
can be queried only through its value. If instead
the report
c
c
is a differentiable function of the parameters at a single
position, the exact derivative
∂
ℓ
∂
c
​
∇
θ
​
c
\frac{\partial\ell}{\partial c}\nabla_{\theta}c
is available, with zero estimator variance given the rollout. Exact pathwise
training also requires the report to be computable inside the forward pass that
generates the rollout. A verbalized numeral does not satisfy this: its realized
value is a sample, and its conditional mean requires marginalizing over the
numeral span.
For the same loss
ℓ
\ell
, the two kinds of report give gradient estimators
g
^
SF
=
(
ℓ
(
q
^
,
t
)
−
b
)
∇
θ
log
π
θ
(
q
^
∣
⋅
)
⏟
sampled report: zero-order query
vs.
g
^
PW
=
∂
ℓ
⁡
(
c
,
t
)
∂
c
​
∇
θ
c
⏟
deterministic report: exact derivative
\underbrace{\ \hat{g}_{\mathrm{SF}}=\big(\ell(\hat{q},t)-b\big)\,\nabla_{\theta}\log\pi_{\theta}(\hat{q}\mid\cdot)\ }_{\text{sampled report: zero-order query}}\qquad\text{vs.}\qquad\underbrace{\ \hat{g}_{\mathrm{PW}}=\frac{\partial\ell(c,t)}{\partial c}\,\nabla_{\theta}c\ }_{\text{deterministic report: exact derivative}}
(5)
where
b
b
is a baseline. The left side is the score-function estimator of
Williams (1992)
; the right is the pathwise form, available when the report
is differentiable in the parameters
(
Kingma and Welling, 2014
;
Mohamed et al., 2020
)
.
The two costs reinforce each other: once the grid collapses, the channel can no
longer express fine-grained values, and the scalar reward provides no direct gradient to recover them.
2.4
Design requirements
The two costs come from a single choice. A report is either sampled, and then
the calibration signal reaches it only through a score-function estimate, or
computed deterministically, and then the calibration gradient reaches it
directly.
The two costs then convert into three requirements, two on
ℰ
\mathcal{E}
and one
on
𝒯
\mathcal{T}
:
(i)
the report is a deterministic functional of the
output distribution rather than a sample from it, removing the variance term of
Proposition
1
;
(ii)
its value is not confined to the vocabulary grid,
removing the tie tax of Figure
2
;
(iii)
the calibration loss is differentiable in the
report, and the report is computable exactly in the forward pass that
generates the rollout, which yields the right-hand branch
of equation
5
.
A pair of reserved tokens and their relative probability is a simple
functional of the output distribution that meets all three. The next section
develops such a channel and trains its report directly.
3
CREDO: instantiating the readout channel
CREDO operates within the RLVR loop of §
2.1
(Figure
3
), changing the confidence channel. It takes the
report from a pair of reserved tokens (§
3.1
) and trains it by a
regression that uses the calibration gradient directly (§
3.2
),
meeting the three requirements of §
2.4
. The policy gradient keeps
the verifier’s correctness judgment and the credit assignment over the text
(§
3.3
), and the trained readout weights learning on the
answer (§
3.4
).
Figure 3:
Overview of CREDO. Each rollout contains an answer,
a confidence analysis, and a confidence slot. The readout
c
c
is the
relative probability of two reserved tokens at the slot. The calibration
loss trains
c
c
by differentiable regression toward a hybrid target
t
t
.
The policy gradient scores the answer and analysis segments through
their text. Discrepancy weighting gives more weight to rollouts where
the outcome and the readout disagree.
3.1
Rollout format and the readout
A rollout ends in a fixed format with three segments: an answer, a confidence
analysis, and the confidence slot.
At the first generated position inside the slot, a pair of reserved tokens
{
H
,
L
}
\{H,L\}
set aside in the vocabulary serves as the two events of the readout
(
Chuang et al., 2025
)
.
Writing
h
′
h^{\prime}
for the prefix up to the slot, we
restrict the next-token distribution to the pair and renormalize,
c
=
π
θ
​
(
H
∣
h
′
)
π
θ
​
(
H
∣
h
′
)
+
π
θ
​
(
L
∣
h
′
)
=
σ
⁡
(
z
H
−
z
L
)
∈
(
0
,
1
)
,
c\;=\;\frac{\pi_{\theta}(H\mid h^{\prime})}{\pi_{\theta}(H\mid h^{\prime})+\pi_{\theta}(L\mid h^{\prime})}\;=\;\sigma(z_{H}-z_{L})\ \in(0,1),
(6)
where
z
H
z_{H}
and
z
L
z_{L}
are the logits of the two tokens and
σ
\sigma
is the
logistic function.
c
c
depends on the output distribution alone and varies continuously, which
gives
(i)
and
(ii)
.
Because the readout is finished inside the forward pass that generates the
rollout, the second half of
(iii)
holds as well. The training in §
3.2
gives
c
c
its meaning as a confidence.
3.2
The calibration loss
The readout is differentiable, which gives the first half
of
(iii)
. We train it by a regression whose target takes the
within-group hybrid form of
Ma et al. (2026)
,
ℒ
cal
=
1
|
𝒱
|
​
∑
i
∈
𝒱
(
c
i
−
t
i
)
2
,
t
i
=
γ
​
a
i
+
(
1
−
γ
)
​
a
¯
group
,
\mathcal{L}_{\mathrm{cal}}=\frac{1}{|\mathcal{V}|}\sum_{i\in\mathcal{V}}\big(c_{i}-t_{i}\big)^{2},\qquad t_{i}=\gamma\,a_{i}+(1-\gamma)\,\bar{a}_{\mathrm{group}},
(7)
where
𝒱
\mathcal{V}
collects the rollouts whose readout is available,
γ
∈
[
0
,
1
]
\gamma\in[0,1]
is the mixing weight, and
a
¯
group
\bar{a}_{\mathrm{group}}
is the mean
correctness over all
G
G
rollouts. The group term shrinks the binary target toward
the group mean, reducing target variance conditional on the question.
The gradient follows the right-hand branch of equation
5
into the
readout position:
∇
θ
ℒ
cal
∝
2
​
(
c
−
t
)
​
c
​
(
1
−
c
)
​
∇
θ
(
z
H
−
z
L
)
\nabla_{\theta}\mathcal{L}_{\mathrm{cal}}\propto 2(c-t)\,c(1-c)\,\nabla_{\theta}(z_{H}-z_{L})
,
one term per sample, with no estimator variance given the rollout.
Proposition 3
(the Bayes-optimal readout)
.
Fix the rollout policy and assume independent rollouts given
x
x
.
Let
ℐ
\mathcal{I}
comprise
x
x
and this rollout’s prefix up to the readout,
and
μ
=
𝔼
⁡
[
a
∣
ℐ
]
\mu=\mathbb{E}[a\mid\mathcal{I}]
the conditional correctness probability.
The Bayes-optimal readout for the unfiltered per-rollout risk of equation
7
is
c
∗
=
λ
​
μ
+
(
1
−
λ
)
​
p
​
(
x
)
c^{\ast}=\lambda\mu+(1-\lambda)\,p(x)
,
λ
=
γ
+
(
1
−
γ
)
/
G
\lambda=\gamma+(1{-}\gamma)/G
, and
𝔼
⁡
[
c
∗
∣
x
]
=
p
⁡
(
x
)
\mathbb{E}[c^{\ast}\mid x]=p(x)
for every
γ
\gamma
.
Here
p
⁡
(
x
)
=
𝔼
π
θ
​
[
a
∣
x
]
p(x)=\mathbb{E}_{\pi_{\theta}}[a\mid x]
is prompt-level accuracy under the
current policy.
Decreasing
γ
\gamma
reduces target variance conditional on the question but
shrinks
c
∗
c^{\ast}
toward
p
⁡
(
x
)
p(x)
, biasing it relative to
μ
\mu
.
Prompt-level mean consistency does not, in general, imply calibration as
defined in equation
2
, so we treat the hybrid target as regularized
correctness supervision. §
4.3
evaluates sensitivity to
γ
\gamma
;
Appendix
A
contains the proof and quantifies target variance and shrinkage.
3.3
Policy losses and credit assignment
With the report’s value trained by the regression, the policy gradient is left
with two jobs: whether the answer is right, and whether the confidence
analysis deserves reinforcement.
The answer and analysis segments are scored separately, on the token sets
ans
i
\mathrm{ans}_{i}
and
conf
i
\mathrm{conf}_{i}
, and
F
i
∈
{
0
,
1
}
F_{i}\in\{0,1\}
records whether all
three segments are present and parseable,
r
i
ans
=
β
​
F
i
+
a
i
,
r
i
conf
=
F
i
​
(
1
−
(
t
i
−
c
i
)
2
)
,
r^{\mathrm{ans}}_{i}\;=\;\beta\,F_{i}+a_{i},\qquad r^{\mathrm{conf}}_{i}\;=\;F_{i}\,\big(1-(t_{i}-c_{i})^{2}\big),
(8)
where
β
\beta
weights the format term.
Each reward is standardized within its own group into
A
^
ans
\hat{A}^{\mathrm{ans}}
and
A
^
conf
\hat{A}^{\mathrm{conf}}
, each acting only on its own segment; the segmented
credit assignment is inherited from
Ma et al. (2026)
.
The policy gradient thus scores the two text segments, while the slot’s value
is trained by the exact derivative of
ℒ
cal
\mathcal{L}_{\mathrm{cal}}
; the policy gradient and the calibration loss
share parameters but no credit.
3.4
Discrepancy weighting: the readout as a training signal
A rollout whose outcome falls far from what the model expected has more to teach
about the answer.
We therefore turn that distance into a per-sample weight.
Discrepancy weighting
centers it within the group and lets the
high-discrepancy rollouts count for more in the answer segment,
s
i
=
|
a
i
−
c
i
|
,
w
i
=
clip
⁡
(
1
+
κ
⁡
(
s
i
−
s
¯
group
)
,
w
−
,
w
+
)
,
A
^
i
ans
←
w
i
​
A
^
i
ans
,
s_{i}=\lvert a_{i}-c_{i}\rvert,\qquad w_{i}=\mathrm{clip}\big(1+\kappa\,(s_{i}-\bar{s}_{\mathrm{group}}),\ w_{-},\ w_{+}\big),\qquad\hat{A}^{\mathrm{ans}}_{i}\;\leftarrow\;w_{i}\,\hat{A}^{\mathrm{ans}}_{i},
(9)
where
s
i
=
|
a
i
−
c
i
|
s_{i}=|a_{i}-c_{i}|
is the discrepancy,
κ
≥
0
\kappa\geq 0
sets the strength,
s
¯
group
\bar{s}_{\mathrm{group}}
is its group mean, and
w
±
w_{\pm}
are clipping bounds
with
w
−
>
0
w_{-}>0
.
The standardization uses the unweighted rewards, and the weights have group
mean one before clipping, so the weighting redistributes learning within the group.
Calibration information thus becomes a per-sample signal inside the training
loop.
The training objective is
ℒ
=
−
𝒥
+
α
ℒ
cal
,
A
^
i
,
k
=
1
[
k
∈
ans
i
]
w
i
A
^
i
ans
+
1
[
k
∈
conf
i
]
A
^
i
conf
,
\mathcal{L}\;=\;-\,\mathcal{J}\;+\;\alpha\,\mathcal{L}_{\mathrm{cal}},\qquad\hat{A}_{i,k}\;=\;\mathbb{1}[k\in\mathrm{ans}_{i}]\,w_{i}\hat{A}^{\mathrm{ans}}_{i}\;+\;\mathbb{1}[k\in\mathrm{conf}_{i}]\,\hat{A}^{\mathrm{conf}}_{i},
(10)
where
𝒥
\mathcal{J}
is the objective of equation
1
,
α
\alpha
weights the
calibration loss, and the per-token advantage
A
^
i
,
k
\hat{A}_{i,k}
of equation
1
now takes the form on the right.
4
Experiments
We compare the methods in and out of domain
(§
4.2
), locate the gain by removing one component at a time
(§
4.3
), and measure what the calibration is worth to a user
who can abstain (§
4.4
).
4.1
Experimental setup
Datasets and metrics.
Mathematics trains on DeepScaleR
(
Luo et al., 2025b
)
and is evaluated on
seven sets: its in-distribution split, MATH-500
(
Hendrycks et al., 2021
;
Lightman et al., 2024
)
, AIME 2024–2026, and AMC
2023–2024. Code trains on DeepCoder
(
Luo et al., 2025a
)
and is evaluated on
four: its in-distribution split, LiveCodeBench v5 and v6
(
Jain et al., 2025
)
, and HumanEval+
(
Liu et al., 2023
)
. We report
accuracy and three calibration measures: ECE
(
Guo et al., 2017
)
on the
reported values, AUROC on the ranking they induce, and Brier
(
Brier, 1950
)
on both.
Baselines and training.
On Qwen3-8B
(
Yang et al., 2025a
)
we compare the untrained base model with GRPO
(
Shao et al., 2024
)
, which trains no calibration term, and with RLCR
(
Damani et al., 2026
)
and
DCPO
(
Ma et al., 2026
)
, which train one. Training runs for two
epochs at learning rate
2
×
10
−
6
2\times 10^{-6}
with eight rollouts per question and
temperature 1.0. Every run uses seed 43, and the main comparisons add seeds 44
and 45.
Appendix
B
provides prompt templates, training hyperparameters, the evaluation protocol, and other implementation details.
4.2
Accuracy and calibration in and out of domain
Table 1:
Accuracy and calibration in and out of domain, each entry
macro-averaged over evaluation sets and training seeds. Column groups are the evaluation domain. Baselines are read through their
own verbalized numeral and again through a digit expectation (Appendix
B.3
), in the
rows
named
-d
;
CREDO
is read
through its readout.
Bold
marks the best mean in each column and any
within one joint standard error of it.
Mathematics
Code
Method
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Base
.439
±
\pm
.001
.472
±
\pm
.002
.644
±
\pm
.004
.453
±
\pm
.002
.455
±
\pm
.001
.418
±
\pm
.001
.690
±
\pm
.004
.395
±
\pm
.002
GRPO
.706
±
\pm
.009
.199
±
\pm
.027
.775
±
\pm
.062
.204
±
\pm
.029
.581
±
\pm
.007
.182
±
\pm
.070
.753
±
\pm
.061
.205
±
\pm
.066
RLCR
.682
±
\pm
.010
.159
±
\pm
.012
.831
±
\pm
.009
.171
±
\pm
.009
.553
±
\pm
.013
.075
±
\pm
.005
.815
±
\pm
.014
.146
±
\pm
.006
DCPO
.722
±
\pm
.008
.217
±
\pm
.008
.848
±
\pm
.012
.198
±
\pm
.003
.576
±
\pm
.003
.153
±
\pm
.024
.776
±
\pm
.025
.153
±
\pm
.024
Base-d
.439
±
\pm
.001
.442
±
\pm
.001
.765
±
\pm
.010
.424
±
\pm
.001
.455
±
\pm
.001
.389
±
\pm
.002
.782
±
\pm
.003
.373
±
\pm
.002
GRPO-d
.706
±
\pm
.009
.192
±
\pm
.025
.864
±
\pm
.020
.203
±
\pm
.023
.581
±
\pm
.007
.155
±
\pm
.022
.833
±
\pm
.034
.184
±
\pm
.025
RLCR-d
.682
±
\pm
.010
.163
±
\pm
.005
.852
±
\pm
.006
.171
±
\pm
.009
.553
±
\pm
.013
.080
±
\pm
.004
.818
±
\pm
.011
.145
±
\pm
.005
DCPO-d
.722
±
\pm
.008
.188
±
\pm
.010
.858
±
\pm
.006
.191
±
\pm
.013
.576
±
\pm
.003
.152
±
\pm
.025
.849
±
\pm
.027
.152
±
\pm
.025
In domain
CREDO
.752
±
\pm
.013
.103
±
\pm
.013
.933
±
\pm
.007
.086
±
\pm
.004
.600
±
\pm
.018
.064
±
\pm
.020
.850
±
\pm
.027
.127
±
\pm
.016
GRPO
.564
±
\pm
.003
.335
±
\pm
.019
.734
±
\pm
.030
.325
±
\pm
.020
.495
±
\pm
.004
.315
±
\pm
.041
.721
±
\pm
.032
.308
±
\pm
.040
RLCR
.515
±
\pm
.011
.170
±
\pm
.004
.815
±
\pm
.016
.186
±
\pm
.007
.502
±
\pm
.002
.228
±
\pm
.014
.792
±
\pm
.005
.229
±
\pm
.010
DCPO
.548
±
\pm
.003
.205
±
\pm
.021
.755
±
\pm
.024
.205
±
\pm
.020
.508
±
\pm
.014
.330
±
\pm
.040
.746
±
\pm
.038
.318
±
\pm
.032
GRPO-d
.564
±
\pm
.003
.311
±
\pm
.017
.826
±
\pm
.004
.308
±
\pm
.015
.495
±
\pm
.004
.298
±
\pm
.028
.792
±
\pm
.026
.299
±
\pm
.028
RLCR-d
.515
±
\pm
.011
.172
±
\pm
.006
.833
±
\pm
.014
.184
±
\pm
.006
.502
±
\pm
.002
.232
±
\pm
.013
.816
±
\pm
.003
.226
±
\pm
.011
DCPO-d
.548
±
\pm
.003
.203
±
\pm
.020
.835
±
\pm
.004
.203
±
\pm
.020
.508
±
\pm
.014
.275
±
\pm
.027
.778
±
\pm
.021
.283
±
\pm
.017
Out of domain
CREDO
.560
±
\pm
.007
.117
±
\pm
.030
.855
±
\pm
.013
.142
±
\pm
.013
.504
±
\pm
.021
.138
±
\pm
.016
.836
±
\pm
.009
.165
±
\pm
.008
Table
1
compares each method three ways: in its own domain, with
only the readout replaced, and on the other domain with nothing adapted.
In domain, CREDO leads on all four metrics in both mathematics and code. Among the
baselines, DCPO is the most accurate on mathematics but still trails CREDO on calibration;
RLCR trades accuracy for a tighter ECE on code, where it is the only baseline to match CREDO on any calibration metric.
All baselines use the verbalized channel and incur both costs of
§
2.3
(Figure
2
).
The
-d
rows replace the sampled numeral with the expectation over
each baseline’s digit distribution, giving a continuous confidence without
retraining. Every swap improves ranking metrics such as AUROC,
confirming that sampling adds noise to an otherwise informative signal. None of
the swaps closes the calibration gap to CREDO: the reported values were shaped
by the training path, and changing the emission alone does not recalibrate them.
The
out of domain
rows move each checkpoint to the other domain.
Accuracy is comparable across methods, but CREDO’s calibration
advantage persists and remains the largest.
RLCR was the only baseline to match CREDO’s code ECE in domain; that match
does not survive the domain shift. The calibration advantage transfers across domains.
Appendix
C.1
repeats the mathematics comparison at 1.7B and
4B. CREDO leads on all four metrics at every scale, and its calibration
advantage widens as models grow larger. Per-set breakdowns and calibration
curves appear in Appendices
D
and
C.5
.
4.3
Ablation and attribution
Table 2:
Leave-one-out ablation of CREDO (seed 43).
Mathematics
Code
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
CREDO
.753
.094
.933
.088
.614
.052
.869
.117
w/o differentiable regression (
α
=
0
\alpha{=}0
)
.696
.241
.880
.232
.611
.172
.857
.172
w/o uncertainty-analysis segment
.709
.096
.902
.107
.587
.048
.868
.117
w/o confidence-segment advantage (
A
^
conf
≡
0
\hat{A}^{\mathrm{conf}}{\equiv}0
)
.696
.099
.909
.102
.576
.047
.867
.126
w/o discrepancy weighting (
κ
=
0
\kappa{=}0
)
.721
.122
.904
.102
.572
.051
.843
.132
Figure 4:
Accuracy and Brier for the two evaluation domains as each
coefficient (
κ
\kappa
,
α
\alpha
,
γ
\gamma
) of §
3
is varied on seed 43, the others held fixed.
Exact values are in Table
D.2
.
Table
2
removes one component at a time. Setting
α
=
0
\alpha{=}0
disables the calibration loss entirely: ECE and Brier degrade sharply in both
domains, and accuracy drops on mathematics. Without differentiable regression
the readout loses its direct supervision and calibration collapses. The next two rows
restore the regression but remove the confidence reasoning: dropping the
analysis text, or keeping it but withholding its policy-gradient credit, both
lower accuracy in both domains while calibration is largely unaffected. This
suggests that reasoning about confidence improves the model’s answers, not only
its confidence estimates. Appendix
C.2
goes further,
independently swapping the emission and training path; neither axis alone
recovers the full method’s performance.
Discrepancy weighting is the only component feeding the readout back into
the answer segment. Removing it causes the largest accuracy drop on code and a
substantial drop on mathematics. Calibration also degrades on mathematics,
though the weighting acts only on the answer advantage. The confidence and
answer channels are therefore not independent: the readout
shapes how the model learns from its answers.
Appendix
C.3
adds the same weighting to RLCR and DCPO,
driven by the parsed numeral or a continuous digit expectation; in
neither case are the gains as large or as consistent as CREDO’s.
Figure
4
varies each coefficient in turn. Any moderate
discrepancy weight
κ
\kappa
outperforms
κ
=
0
\kappa{=}0
, confirming that the
weighting itself, not just the readout, contributes to accuracy. The calibration
weight
α
\alpha
has a threshold effect:
α
=
0
\alpha{=}0
disables calibration
training and both ECE and Brier collapse, while all tested positive values restore
calibration. The target mixture
γ
\gamma
trades variance against shrinkage (§
3.2
);
among tested values,
γ
=
0.5
\gamma{=}0.5
gives the best accuracy and Brier in both domains, though
γ
=
1
\gamma{=}1
achieves lower code ECE.
Appendix
C.4
compares two alternative reward shapes;
the additive form is the best or tied in mathematics and competitive in code.
4.4
Downstream benefits of calibration
Table 3:
AURC, selective accuracy at three coverages, and the number of
operable thresholds.
AURC (%)
↓
\downarrow
acc@50
↑
\uparrow
acc@80
↑
\uparrow
acc@90
↑
\uparrow
Thr.
↑
\uparrow
Mathematics
CREDO
2.62
±
\pm
0.04
.986
±
\pm
.001
.962
±
\pm
.001
.927
±
\pm
.002
372
DCPO
4.98
±
\pm
0.65
.958
±
\pm
.006
.941
±
\pm
.002
.909
±
\pm
.005
22
RLCR
5.88
±
\pm
0.67
.952
±
\pm
.009
.910
±
\pm
.009
.878
±
\pm
.007
15
GRPO
7.92
±
\pm
0.67
.927
±
\pm
.003
.915
±
\pm
.023
.888
±
\pm
.011
21
Base
29.64
±
\pm
0.30
.712
±
\pm
.001
.705
±
\pm
.005
.666
±
\pm
.001
34
Code
CREDO
16.80
±
\pm
1.57
.885
±
\pm
.013
.686
±
\pm
.025
.617
±
\pm
.019
932
DCPO
21.26
±
\pm
0.95
.863
±
\pm
.016
.679
±
\pm
.003
.611
±
\pm
.003
10
RLCR
21.36
±
\pm
1.00
.809
±
\pm
.015
.608
±
\pm
.014
.562
±
\pm
.014
12
GRPO
21.50
±
\pm
3.08
.797
±
\pm
.081
.652
±
\pm
.041
.599
±
\pm
.023
17
Base
45.10
±
\pm
0.50
.572
±
\pm
.005
.478
±
\pm
.002
.437
±
\pm
.002
16
Figure 5:
Risk–coverage frontiers, pooled over three seeds; Base omitted.
Figure
5
plots the error among answered questions as the model
keeps only its most confident fraction
(
Geifman and El-Yaniv, 2017
)
. In mathematics CREDO
is below every baseline throughout. In code RLCR is lower at very low coverage; above
it CREDO is lowest. At the evaluated coverage budgets
(Table
5
), CREDO answers the most accurately and has the lowest
aggregate error in both domains; only the two tightest code budgets are
statistically tied with DCPO.
Selective prediction relies on setting a confidence threshold, and the channel’s granularity determines how finely it can be tuned.
Verbalized reports concentrate on a few values
(Figure
2
), leaving a threshold policy only a dozen or two
operating points (Table
5
); the readout supplies hundreds. On
code, DCPO’s most confident value already covers half the pool.
5
Related work
Confidence estimation.
The most direct way to obtain a confidence estimate is to ask for one:
Lin et al. (2022)
fine-tune a model to state a number, but such numbers
are systematically overconfident
(
Xiong et al., 2024
;
Tian et al., 2023
)
.
Instead of asking, the confidence can be read from the model’s own probabilities
or internal representations
(
Fomicheva et al., 2020
;
Kadavath et al., 2022
;
Azaria and Mitchell, 2023
;
Orgad et al., 2025
)
, or
estimated from sample agreement
(
Kuhn et al., 2023
;
Aichberger et al., 2025
;
Geng et al., 2024
)
.
A dedicated readout can also be trained directly:
Chuang et al. (2025)
learn a
confidence-token readout under supervised finetuning, applied to routing
and rejection. CREDO trains the same form of readout on-policy inside
RLVR, against a hybrid calibration target, and feeds it back as a signal
for answer learning.
Calibration in RLVR.
Inside RLVR, one line of work incorporates confidence derived from response
likelihood or token-level statistics into policy optimization
(
Wang et al., 2026
;
Liu et al., 2025
;
Zhao et al., 2026
)
. Another trains the model to state a numerical
confidence and scores it with a reward.
RLCR
(
Damani et al., 2026
)
folds a proper scoring rule into the reward, while
DCPO
(
Ma et al., 2026
)
separates credit by scoring answer and confidence tokens; other work extends to question answering, preference
tuning, and generative recommendation
(
Xu et al., 2024
;
Bani-Harouni et al., 2026
;
Stengel-Eskin et al., 2024
;
Leng et al., 2025
;
Fan et al., 2026
)
.
In the numerical-report methods, the confidence is sampled as text and
trained through a scalar reward (§
2
).
A dedicated readout can also serve as a self-reward signal:
LaSeR
(
Yang et al., 2025b
)
aligns a last-token score with verifier rewards
during RLVR and mixes score-derived advantages into policy updates.
CREDO targets calibration rather than self-reward: it regresses a
normalized two-token readout toward a hybrid calibration target and
uses confidence–outcome discrepancies to rescale answer advantages.
6
Conclusion
In this work, we examined the confidence channel shared by all verbalized
calibration methods. We analyzed the variance cost of sampling the report,
observed that it collapses to a handful of values in the baselines we
evaluated, and showed that sampling forces the calibration loss through a
scalar reward.
We therefore proposed CREDO, which reads the confidence as a deterministic
function of the output distribution and trains it by differentiable regression,
while the policy gradient optimizes correctness.
The same readout also serves as a training signal: it weights learning on the
answer by how far each outcome departs from the model’s own confidence, and
this improves accuracy in both domains.
On mathematical and code reasoning tasks CREDO attains the best accuracy and
calibration, and its confidence translates into finer abstention control.
Because CREDO trains confidence by regression, it is not tied to binary
correctness labels; open-ended tasks with graded reward models are a natural
next step.
Looking further, feeding the confidence signal back during generation would let
uncertain steps be reconsidered before the answer is finalized, moving toward
reasoners that know when they are right.
References
Aichberger
et al.
(2025)
L. Aichberger, K. Schweighofer, M. Ielanskyi, and S. Hochreiter
Improving uncertainty estimation through semantically diverse language generation
.
In
International Conference on Learning Representations
,
Cited by:
§5
.
Azaria and Mitchell (2023)
A. Azaria and T. Mitchell
The internal state of an LLM knows when it’s lying
.
In
Findings of the Association for Computational Linguistics: EMNLP 2023
,
Singapore
,
pp. 967–976
.
External Links:
Document
,
Link
Cited by:
§5
.
Bani-Harouni
et al.
(2026)
D. Bani-Harouni, C. Pellegrini, P. Stangel, E. Özsoy, K. Zaripova, N. Navab, and M. Keicher
Rewarding doubt: a reinforcement learning approach to calibrated confidence expression of large language models
.
In
International Conference on Learning Representations
,
Cited by:
§1
,
§2.2
,
§5
.
Bereket and Leskovec (2025)
M. Bereket and J. Leskovec
Uncalibrated reasoning: GRPO induces overconfidence for stochastic outcomes
.
arXiv preprint arXiv:2508.11800
.
Cited by:
§1
.
Brier (1950)
G. W. Brier
Verification of forecasts expressed in terms of probability
.
Monthly Weather Review
78
(
1
),
pp. 1–3
.
External Links:
Document
Cited by:
3rd item
,
§2.1
,
§4.1
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
et al.
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
Cited by:
§B.3
.
Chuang
et al.
(2025)
Y. Chuang, P. K. Sarma, P. Gopalan, J. Boccio, S. Bolouki, X. Hu, and H. Zhou
Learning to route LLMs with confidence tokens
.
In
International Conference on Machine Learning
,
Cited by:
§3.1
,
§5
.
Damani
et al.
(2026)
M. Damani, I. Puri, S. Slocum, I. Shenfeld, L. Choshen, Y. Kim, and J. Andreas
Beyond binary rewards: training LMs to reason about their uncertainty
.
In
International Conference on Learning Representations
,
Cited by:
§1
,
§2.1
,
§2.2
,
§2.2
,
§4.1
,
§5
.
DeGroot and Fienberg (1983)
M. H. DeGroot and S. E. Fienberg
The comparison and evaluation of forecasters
.
The Statistician
32
(
1/2
).
External Links:
Document
Cited by:
§1
.
Fan
et al.
(2026)
C. Fan, C. Gao, Y. Gong, H. Liu, F. Feng, and X. He
Uncertainty-aware generative recommendation
.
In
Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining
,
pp. 1015–1026
.
External Links:
Document
Cited by:
§5
.
Fomicheva
et al.
(2020)
M. Fomicheva, S. Sun, L. Yankovskaya, F. Blain, F. Guzmán, M. Fishel, N. Aletras, V. Chaudhary, and L. Specia
Unsupervised quality estimation for neural machine translation
.
Transactions of the Association for Computational Linguistics
8
,
pp. 539–555
.
External Links:
Document
Cited by:
§1
,
§5
.
Geifman and El-Yaniv (2017)
Y. Geifman and R. El-Yaniv
Selective classification for deep neural networks
.
In
Advances in Neural Information Processing Systems
,
Vol.
30
.
Cited by:
5th item
,
§1
,
§4.4
.
Geng
et al.
(2024)
J. Geng, F. Cai, Y. Wang, H. Koeppl, P. Nakov, and I. Gurevych
A survey of confidence estimation and calibration in large language models
.
In
Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
,
Mexico City, Mexico
,
pp. 6577–6595
.
External Links:
Document
,
Link
Cited by:
§5
.
Gneiting and Raftery (2007)
T. Gneiting and A. E. Raftery
Strictly proper scoring rules, prediction, and estimation
.
Journal of the American Statistical Association
102
(
477
),
pp. 359–378
.
External Links:
Document
Cited by:
§1
,
§2.1
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
International Conference on Machine Learning
,
Cited by:
2nd item
,
§1
,
§4.1
.
Guo
et al.
(2025)
D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu,
et al.
DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning
.
Nature
645
(
8081
),
pp. 633–638
.
External Links:
Document
Cited by:
§1
.
Hanley and McNeil (1982)
J. A. Hanley and B. J. McNeil
The meaning and use of the area under a receiver operating characteristic (ROC) curve
.
Radiology
143
(
1
),
pp. 29–36
.
External Links:
Document
Cited by:
4th item
.
Hendrycks
et al.
(2021)
D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
Measuring mathematical problem solving with the MATH dataset
.
In
Advances in Neural Information Processing Systems Track on Datasets and Benchmarks
,
Cited by:
§4.1
.
Hugging Face (2025)
Hugging Face
Math-Verify: a robust mathematical expression evaluation system
.
Note:
https://github.com/huggingface/Math-Verify
Cited by:
§B.3
.
Jain
et al.
(2025)
N. Jain, K. Han, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica
LiveCodeBench: holistic and contamination free evaluation of large language models for code
.
In
International Conference on Learning Representations
,
Cited by:
§4.1
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson, S. Johnston, S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen, Y. Bai, S. Bowman, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion, S. Kravec, L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei, T. Brown, J. Clark, N. Joseph, B. Mann, S. McCandlish, C. Olah, and J. Kaplan
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Cited by:
§5
.
Kingma and Welling (2014)
D. P. Kingma and M. Welling
Auto-encoding variational bayes
.
In
International Conference on Learning Representations
,
Cited by:
§A.2
,
§2.3
.
Kirichenko
et al.
(2025)
P. Kirichenko, M. Ibrahim, K. Chaudhuri, and S. J. Bell
AbstentionBench: reasoning LLMs fail on unanswerable questions
.
In
Advances in Neural Information Processing Systems
,
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
International Conference on Learning Representations
,
Cited by:
§5
.
Kwon
et al.
(2023)
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica
Efficient memory management for large language model serving with PagedAttention
.
In
Proceedings of the 29th Symposium on Operating Systems Principles
,
Cited by:
§B.2
.
Leng
et al.
(2025)
J. Leng, C. Huang, B. Zhu, and J. Huang
Taming overconfidence in LLMs: reward calibration in RLHF
.
In
International Conference on Learning Representations
,
Cited by:
§1
,
§2.2
,
§5
.
Lightman
et al.
(2024)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
Let’s verify step by step
.
In
International Conference on Learning Representations
,
Cited by:
§4.1
.
Lin
et al.
(2022)
S. Lin, J. Hilton, and O. Evans
Teaching models to express their uncertainty in words
.
Transactions on Machine Learning Research
.
External Links:
Link
Cited by:
§5
.
Liu
et al.
(2025)
H. Liu, S. Wang, and H. Xu
C
2
{}^{2}
GSPG: confidence-calibrated group sequence policy gradient towards self-aware reasoning
.
arXiv preprint arXiv:2509.23129
.
Cited by:
§5
.
Liu
et al.
(2023)
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
Is your code generated by ChatGPT really correct? rigorous evaluation of large language models for code generation
.
In
Advances in Neural Information Processing Systems
,
Cited by:
§4.1
.
Loshchilov and Hutter (2019)
I. Loshchilov and F. Hutter
Decoupled weight decay regularization
.
In
International Conference on Learning Representations
,
Cited by:
§B.2
.
Luo
et al.
(2025a)
M. Luo, S. Tan, R. Huang, A. Patel, A. Ariyak, Q. Wu, X. Shi, R. Xin, C. Cai, M. Weber, C. Zhang, L. E. Li, R. A. Popa, and I. Stoica
DeepCoder: a fully open-source 14B coder at O3-mini level
.
Note:
https://pretty-radio-b75.notion.site/DeepCoder-A-Fully-Open-Source-14B-Coder-at-O3-mini-Level-1cf81902c14680b3bee5eb349a512a51
Notion Blog
Cited by:
§4.1
.
Luo
et al.
(2025b)
M. Luo, S. Tan, J. Wong, X. Shi, W. Y. Tang, M. Roongta, C. Cai, J. Luo, L. E. Li, R. A. Popa, and I. Stoica
DeepScaleR: surpassing O1-preview with a 1.5B model by scaling RL
.
Note:
https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2
Notion Blog
Cited by:
§4.1
.
Ma
et al.
(2026)
Z. Ma, X. Wen, B. Cao, Y. Lu, H. Lin, J. Yang, M. He, X. Han, and L. Sun
Decoupling reasoning and confidence: resurrecting calibration in reinforcement learning from verifiable rewards
.
In
International Conference on Machine Learning
,
Cited by:
§1
,
§2.2
,
§2.2
,
§3.2
,
§3.3
,
§4.1
,
§5
.
Mei
et al.
(2025)
Z. Mei, C. Zhang, T. Yin, J. Lidard, O. Shorinwa, and A. Majumdar
Reasoning about uncertainty: do reasoning models know when they don’t know?
.
arXiv preprint arXiv:2506.18183
.
Cited by:
§1
.
Mohamed
et al.
(2020)
S. Mohamed, M. Rosca, M. Figurnov, and A. Mnih
Monte carlo gradient estimation in machine learning
.
Journal of Machine Learning Research
21
(
132
),
pp. 1–62
.
Cited by:
§2.3
.
Orgad
et al.
(2025)
H. Orgad, M. Toker, Z. Gekhman, R. Reichart, I. Szpektor, H. Kotek, and Y. Belinkov
LLMs know more than they show: on the intrinsic representation of LLM hallucinations
.
In
International Conference on Learning Representations
,
Cited by:
§5
.
Pakdaman Naeini
et al.
(2015)
M. Pakdaman Naeini, G. Cooper, and M. Hauskrecht
Obtaining well calibrated probabilities using bayesian binning
.
In
Proceedings of the AAAI Conference on Artificial Intelligence
,
Vol.
29
.
External Links:
Document
Cited by:
2nd item
.
Schulman
et al.
(2017)
J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov
Proximal policy optimization algorithms
.
arXiv preprint arXiv:1707.06347
.
Cited by:
§2.1
.
Shao
et al.
(2024)
Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, and D. Guo
DeepSeekMath: pushing the limits of mathematical reasoning in open language models
.
arXiv preprint arXiv:2402.03300
.
Cited by:
§1
,
§2.1
,
§4.1
.
Stengel-Eskin
et al.
(2024)
E. Stengel-Eskin, P. Hase, and M. Bansal
LACIE: listener-aware finetuning for calibration in large language models
.
In
Advances in Neural Information Processing Systems
,
Vol.
37
,
pp. 43080–43106
.
External Links:
Document
Cited by:
§2.2
,
§5
.
Tian
et al.
(2023)
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. D. Manning
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
Singapore
.
Cited by:
§5
.
Wang
et al.
(2026)
Z. Wang, X. Lou, M. Wu, Z. Wen, and J. Zhang
Calibration-aware policy optimization for reasoning LLMs
.
In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
San Diego, California, United States
,
pp. 18375–18390
.
External Links:
Document
,
Link
Cited by:
§5
.
Williams (1992)
R. J. Williams
Simple statistical gradient-following algorithms for connectionist reinforcement learning
.
Machine Learning
8
(
3–4
),
pp. 229–256
.
External Links:
Document
Cited by:
§A.2
,
§2.3
.
Wilson (1927)
E. B. Wilson
Probable inference, the law of succession, and statistical inference
.
Journal of the American Statistical Association
22
(
158
),
pp. 209–212
.
External Links:
Document
Cited by:
§C.5
.
Xiong
et al.
(2024)
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi
Can LLMs express their uncertainty? an empirical evaluation of confidence elicitation in LLMs
.
In
International Conference on Learning Representations
,
Cited by:
§5
.
Xu
et al.
(2024)
T. Xu, S. Wu, S. Diao, X. Liu, X. Wang, Y. Chen, and J. Gao
SaySelf: teaching LLMs to express confidence with self-reflective rationales
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
Miami, Florida, USA
,
pp. 5985–5998
.
External Links:
Document
,
Link
Cited by:
§1
,
§2.2
,
§5
.
Yang
et al.
(2025a)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng,
et al.
Qwen3 technical report
.
arXiv preprint arXiv:2505.09388
.
Cited by:
§B.1
,
§4.1
.
Yang
et al.
(2024)
D. Yang, Y. H. Tsai, and M. Yamada
On verbalized confidence scores for LLMs
.
arXiv preprint arXiv:2412.14737
.
Cited by:
§1
.
Yang
et al.
(2025b)
W. Yang, W. Liu, R. Xie, Y. Guo, L. Wu, S. Yang, and Y. Lin
LaSeR: reinforcement learning with last-token self-rewarding
.
arXiv preprint arXiv:2510.14943
.
Cited by:
§5
.
Zhang
et al.
(2026)
C. Zhang, X. Zhu, C. Li, N. Collier, and A. Vlachos
LoVeC: reinforcement learning for better verbalized confidence in long-form generation
.
In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
San Diego, California, United States
,
pp. 33336–33363
.
External Links:
Document
,
Link
Cited by:
§2.2
.
Zhao
et al.
(2026)
Q. Zhao, C. Yang, J. Jing, Y. Zhang, X. Ren, L. Yu, S. Zhang, and H. Yin
Know what you know: metacognitive entropy calibration for verifiable RL reasoning
.
arXiv preprint arXiv:2602.22751
.
Cited by:
§5
.
Appendix A
Proofs
For the verbalized channel,
h
h
denotes the rollout prefix up to the confidence
slot, and the report is
q
^
=
parse
⁡
(
s
)
\hat{q}=\mathrm{parse}(s)
for a numeral
s
∼
π
θ
(
⋅
∣
h
)
s\sim\pi_{\theta}(\cdot\mid h)
sampled from the policy, taking values in a
finite set
𝒬
⊂
[
0
,
1
]
\mathcal{Q}\subset[0,1]
. Expectations are conditional on
h
h
and
on the other rollouts of the group, which fixes any target
t
∈
[
0
,
1
]
t\in[0,1]
determined by them.
A.1
Proof of Proposition
1
Fix a rollout prefix and let
q
^
\hat{q}
be the parsed report
of equation
3
, with conditional mean
q
¯
\bar{q}
and variance
v
v
. Every
verbalized policy either pays a per-prefix tax that persists as long as the report is stochastic, or
determinizes its per-prefix report distribution.
Under the squared loss the tax is exactly
v
v
, since
𝔼
⁡
[
(
q
^
−
t
)
2
]
=
(
q
¯
−
t
)
2
+
v
\mathbb{E}[(\hat{q}-t)^{2}]=(\bar{q}-t)^{2}+v
for any target
t
∈
[
0
,
1
]
t\in[0,1]
; under any strictly convex
loss
ℓ
\ell
, Jensen’s inequality gives
𝔼
⁡
[
ℓ
⁡
(
q
^
,
t
)
]
−
ℓ
⁡
(
q
¯
,
t
)
>
0
\mathbb{E}[\ell(\hat{q},t)]-\ell(\bar{q},t)>0
.
Proof.
The tax is the excess of scoring the sampled report over scoring the same
policy’s conditional mean,
τ
=
𝔼
⁡
[
ℓ
⁡
(
q
^
,
t
)
]
−
ℓ
⁡
(
q
¯
,
t
)
\tau=\mathbb{E}[\ell(\hat{q},t)]-\ell(\bar{q},t)
.
Under the squared loss,
t
t
and
q
¯
\bar{q}
are fixed given
h
h
, and expanding
about
q
¯
\bar{q}
gives
𝔼
⁡
[
(
q
^
−
t
)
2
]
=
𝔼
⁡
[
(
q
^
−
q
¯
)
2
]
+
2
​
(
q
¯
−
t
)
​
𝔼
​
[
q
^
−
q
¯
]
+
(
q
¯
−
t
)
2
=
v
+
(
q
¯
−
t
)
2
,
\mathbb{E}\big[(\hat{q}-t)^{2}\big]=\mathbb{E}\big[(\hat{q}-\bar{q})^{2}\big]+2(\bar{q}-t)\,\mathbb{E}\big[\hat{q}-\bar{q}\big]+(\bar{q}-t)^{2}=v+(\bar{q}-t)^{2},
(11)
where the middle term vanishes. So the tax is the conditional variance itself,
τ
=
v
\tau=v
, and it does not involve the target. Changing calibration moves
q
¯
\bar{q}
, and with it only the
(
q
¯
−
t
)
2
(\bar{q}-t)^{2}
term.
For a strictly convex
ℓ
\ell
, Jensen’s inequality gives
𝔼
⁡
[
ℓ
⁡
(
q
^
,
t
)
]
≥
ℓ
⁡
(
q
¯
,
t
)
\mathbb{E}[\ell(\hat{q},t)]\geq\ell(\bar{q},t)
, with equality only if
q
^
\hat{q}
is almost surely
constant given
h
h
.
Both branches follow. A non-degenerate per-prefix report distribution pays
τ
>
0
\tau>0
. A degenerate one concentrates the report on a single element of
𝒬
\mathcal{Q}
and pays nothing — the determinized case.
∎
A.2
Proof of Proposition
2
Fix a calibration loss
ℓ
\ell
. A sampled report admits no unbiased pathwise
gradient estimator, so
ℓ
\ell
can be queried only through its value. If instead
the report
c
c
is a differentiable function of the parameters at a single
position, the exact derivative
∂
ℓ
∂
c
​
∇
θ
​
c
\frac{\partial\ell}{\partial c}\nabla_{\theta}c
is available, with zero estimator variance given the rollout. Exact pathwise
training also requires the report to be computable inside the forward pass that
generates the rollout. A verbalized numeral does not satisfy this: its realized
value is a sample, and its conditional mean requires marginalizing over the
numeral span.
Proof.
A pathwise estimator
(
Kingma and Welling, 2014
)
writes the draw as
s
=
S
θ
​
(
ξ
)
s=S_{\theta}(\xi)
,
with noise
ξ
\xi
whose law does not depend on
θ
\theta
, and differentiates the composition,
∂
ℓ
∂
q
^
​
∇
θ
parse
​
(
S
θ
​
(
ξ
)
)
\frac{\partial\ell}{\partial\hat{q}}\nabla_{\theta}\,\mathrm{parse}(S_{\theta}(\xi))
.
The map
θ
↦
parse
​
(
S
θ
​
(
ξ
)
)
\theta\mapsto\mathrm{parse}(S_{\theta}(\xi))
takes values in the finite
set
𝒬
\mathcal{Q}
, so it is locally constant wherever it is continuous and its
gradient is zero wherever it exists. The estimator is therefore zero, while the
gradient
∇
θ
𝔼
​
[
ℓ
⁡
(
q
^
,
t
)
]
=
∑
s
ℓ
⁡
(
parse
⁡
(
s
)
,
t
)
​
∇
θ
π
θ
​
(
s
∣
h
)
\nabla_{\theta}\,\mathbb{E}\big[\ell(\hat{q},t)\big]=\sum_{s}\ell\big(\mathrm{parse}(s),t\big)\,\nabla_{\theta}\pi_{\theta}(s\mid h)
(12)
is not whenever two values in
𝒬
\mathcal{Q}
carry different losses and the
policy can shift probability between them. In this identity
ℓ
\ell
enters only
through its values on
𝒬
\mathcal{Q}
, never through
∂
ℓ
/
∂
q
^
\partial\ell/\partial\hat{q}
. Equivalently, the same gradient has the
score-function form
(
Williams, 1992
)
𝔼
⁡
[
ℓ
⁡
(
q
^
,
t
)
​
∇
θ
​
log
⁡
π
θ
​
(
s
∣
h
)
]
\mathbb{E}[\ell(\hat{q},t)\,\nabla_{\theta}\log\pi_{\theta}(s\mid h)]
, the
left-hand branch of equation
5
.
Now let
c
c
be differentiable in
θ
\theta
at a single position, with
ℓ
\ell
differentiable in the report. Given the rollout,
c
c
is a deterministic
function of
θ
\theta
, so the chain-rule derivative
∇
θ
ℓ
​
(
c
,
t
)
=
∂
ℓ
∂
c
​
∇
θ
c
\nabla_{\theta}\ell(c,t)=\frac{\partial\ell}{\partial c}\nabla_{\theta}c
is
exact and carries no variance.
Exact pathwise training also needs a differentiable value inside the pass that
generates the rollout, and a verbalized numeral has none. Its realized value is
a sample, which carries no pathwise derivative. Its conditional mean,
q
¯
=
∑
s
π
θ
​
(
s
∣
h
)
​
parse
​
(
s
)
,
\bar{q}=\sum_{s}\pi_{\theta}(s\mid h)\,\mathrm{parse}(s),
(13)
is differentiable in
θ
\theta
, but the sum ranges over every string the numeral
span can produce, because
parse
\mathrm{parse}
couples the span’s positions. The
generating pass produces one of those strings, not the sum. A report read at a
single position is instead a function of that position’s logits, which the same
pass has already computed.
∎
A.3
Proof of Proposition
3
Fix the rollout policy and assume independent rollouts given
x
x
.
Let
ℐ
\mathcal{I}
comprise
x
x
and this rollout’s prefix up to the readout,
and
μ
=
𝔼
⁡
[
a
∣
ℐ
]
\mu=\mathbb{E}[a\mid\mathcal{I}]
the conditional correctness probability.
The Bayes-optimal readout for the unfiltered per-rollout risk of equation
7
is
c
∗
=
λ
​
μ
+
(
1
−
λ
)
​
p
​
(
x
)
c^{\ast}=\lambda\mu+(1-\lambda)\,p(x)
,
λ
=
γ
+
(
1
−
γ
)
/
G
\lambda=\gamma+(1{-}\gamma)/G
, and
𝔼
⁡
[
c
∗
∣
x
]
=
p
⁡
(
x
)
\mathbb{E}[c^{\ast}\mid x]=p(x)
for every
γ
\gamma
.
Proof.
We analyze the unfiltered per-rollout population risk
R
⁡
(
c
)
=
𝔼
⁡
[
(
c
⁡
(
ℐ
)
−
t
)
2
]
R(c)=\mathbb{E}[(c(\mathcal{I})-t)^{2}]
, which coincides with the expected
loss of equation
7
when every rollout has an available readout.
Expectations are over the group drawn at a question
x
x
, and
p
⁡
(
x
)
=
𝔼
⁡
[
a
∣
x
]
p(x)=\mathbb{E}[a\mid x]
denotes the current policy’s accuracy on it.
The target is
t
=
γ
​
a
+
(
1
−
γ
)
​
a
¯
group
t=\gamma a+(1-\gamma)\bar{a}_{\mathrm{group}}
, with
a
¯
group
\bar{a}_{\mathrm{group}}
the mean correctness over all
G
G
rollouts. Each
squared error is minimized pointwise by the conditional mean of its target, so
the best readout among functions of
ℐ
\mathcal{I}
is
c
∗
=
𝔼
⁡
[
t
∣
ℐ
]
c^{\ast}=\mathbb{E}[t\mid\mathcal{I}]
.
By definition
𝔼
⁡
[
a
∣
ℐ
]
=
μ
\mathbb{E}[a\mid\mathcal{I}]=\mu
. The other rollouts are drawn
independently given
x
x
, and
ℐ
\mathcal{I}
is a function of
x
x
and this
rollout alone, so each of the other
G
−
1
G-1
scores has conditional mean
p
⁡
(
x
)
p(x)
,
and
𝔼
⁡
[
a
¯
group
∣
ℐ
]
=
μ
G
+
G
−
1
G
​
p
​
(
x
)
=
p
⁡
(
x
)
+
μ
−
p
⁡
(
x
)
G
.
\mathbb{E}\big[\bar{a}_{\mathrm{group}}\mid\mathcal{I}\big]=\frac{\mu}{G}+\frac{G-1}{G}\,p(x)=p(x)+\frac{\mu-p(x)}{G}.
(14)
Therefore
c
∗
=
γ
​
μ
+
(
1
−
γ
)
​
p
​
(
x
)
+
(
1
−
γ
)
​
μ
−
p
⁡
(
x
)
G
=
λ
​
μ
+
(
1
−
λ
)
​
p
​
(
x
)
,
λ
=
γ
+
1
−
γ
G
.
c^{\ast}=\gamma\,\mu+(1-\gamma)\,p(x)+(1-\gamma)\,\frac{\mu-p(x)}{G}=\lambda\mu+(1-\lambda)\,p(x),\qquad\lambda=\gamma+\frac{1-\gamma}{G}.
(15)
Averaging over rollouts at the same question,
𝔼
⁡
[
μ
∣
x
]
=
𝔼
⁡
[
𝔼
⁡
[
a
∣
ℐ
]
∣
x
]
=
p
⁡
(
x
)
\mathbb{E}[\mu\mid x]=\mathbb{E}[\mathbb{E}[a\mid\mathcal{I}]\mid x]=p(x)
, so
𝔼
⁡
[
c
∗
∣
x
]
=
λ
​
p
​
(
x
)
+
(
1
−
λ
)
​
p
​
(
x
)
=
p
⁡
(
x
)
\mathbb{E}[c^{\ast}\mid x]=\lambda\,p(x)+(1-\lambda)\,p(x)=p(x)
for
every
γ
\gamma
.
∎
Target variance and shrinkage bias.
Writing
t
i
=
λ
​
a
i
+
1
−
γ
G
​
∑
j
≠
i
a
j
t_{i}=\lambda a_{i}+\frac{1-\gamma}{G}\sum_{j\neq i}a_{j}
and using
conditional independence given
x
x
:
Target variance.
Var
⁡
(
t
i
∣
x
)
=
[
γ
2
+
1
−
γ
2
G
]
​
p
​
(
x
)
​
(
1
−
p
⁡
(
x
)
)
.
\operatorname{Var}(t_{i}\mid x)=\left[\gamma^{2}+\frac{1-\gamma^{2}}{G}\right]p(x)\bigl(1-p(x)\bigr).
(16)
At
G
=
8
G{=}8
and
γ
=
0.5
\gamma{=}0.5
the bracketed coefficient is
0.344
0.344
, compared
with
1
1
at
γ
=
1
\gamma{=}1
.
This is a reduction in marginal target variance conditional on the question;
it does not by itself establish lower prediction error or gradient variance.
Shrinkage bias.
Relative to the conditional correctness
probability
μ
\mu
,
c
γ
∗
−
μ
=
(
1
−
λ
)
​
(
p
⁡
(
x
)
−
μ
)
.
c^{\ast}_{\gamma}-\mu=(1-\lambda)\bigl(p(x)-\mu\bigr).
(17)
For fixed
γ
<
1
\gamma{<}1
, the limit as
G
→
∞
G\to\infty
is
(
1
−
γ
)
​
(
p
​
(
x
)
−
μ
)
(1{-}\gamma)(p(x){-}\mu)
: increasing the group size does not generally
eliminate the bias.
Brier cost.
Because
μ
\mu
minimizes Brier risk over
ℐ
\mathcal{I}
-measurable predictors and the cross term vanishes
(
𝔼
⁡
[
a
−
μ
∣
ℐ
]
=
0
\mathbb{E}[a{-}\mu\mid\mathcal{I}]=0
),
𝔼
⁡
[
(
c
γ
∗
−
a
)
2
]
−
𝔼
⁡
[
(
μ
−
a
)
2
]
=
(
1
−
λ
)
2
​
𝔼
​
[
(
μ
−
p
⁡
(
x
)
)
2
]
.
\mathbb{E}\bigl[(c^{\ast}_{\gamma}-a)^{2}\bigr]-\mathbb{E}\bigl[(\mu-a)^{2}\bigr]=(1-\lambda)^{2}\,\mathbb{E}\bigl[(\mu-p(x))^{2}\bigr].
(18)
The hybrid target thus reduces target variance conditional on
x
x
while
introducing a population-level Brier cost relative to
μ
\mu
.
Whether this regularization improves the learned readout under finite data
and limited optimization is an empirical question
(§
4.3
).
Appendix B
Experimental setup and implementation details
B.1
Model and prompts
All experiments use Qwen3-8B
(
Yang et al., 2025a
)
. The reserved tokens
H
H
and
L
L
of
§
3.1
are added to the vocabulary as special tokens, with
embeddings copied from the rows of “high” and “low”.
The system prompts of the two channels fix the three-segment format of
§
3.1
: they differ only in the slot instruction, and the coding
versions differ only in carrying the answer in a
python
block.
Verbalized channel.
A conversation between User and Assistant. The
user asks a question, and the Assistant solves it. Solve the problem step by
step, and put your final answer within
\boxed{}
. After
the final answer, analyze the uncertainty of your solution within
<analysis>
</analysis>
tags. This analysis is the basis for
the confidence level you will report next, and must follow these rules: (1)
point out specific steps that could be wrong or ambiguous, including alternative
approaches that might lead to different answers; (2) do not solve the problem
again and do not revise or change your answer; (3) be specific — if you cannot
find more uncertainties, say so explicitly. Then provide your confidence that
the final answer is correct, as a decimal number between 0 and 1 (e.g. 0.3 or
0.8), within
<confidence>
</confidence>
tags. The final format
that must be followed is: {step-by-step solution with
\boxed{final answer}
}
<analysis>
uncertainty
analysis here
</analysis>
<confidence>
confidence here
</confidence>
Readout channel (CREDO).
A conversation between User and Assistant.
The user asks a question, and the Assistant solves it. Solve the problem step by
step, and put your final answer within
\boxed{}
. After
the final answer, analyze the uncertainty of your solution within
<analysis>
</analysis>
tags. This analysis is the basis for
the confidence level you will report next, and must follow these rules: (1)
point out specific steps that could be wrong or ambiguous, including alternative
approaches that might lead to different answers; (2) do not solve the problem
again and do not revise or change your answer; (3) be specific — if you cannot
find more uncertainties, say so explicitly. Then, within
<confidence>
</confidence>
tags, output exactly one token:
<CONF_HIGH>
if
your final answer is more likely correct than not, otherwise
<CONF_LOW>
. The final format that must be followed is:
{step-by-step solution with
\boxed{final answer}
}
<analysis>
uncertainty analysis here
</analysis>
<confidence><CONF_HIGH></confidence>
B.2
Training
Table 4:
Training configuration. Values that differ by domain are given
as mathematics / code. Rollouts are generated with vLLM
(
Kwon et al., 2023
)
.
Shared
Base model
Qwen3-8B
Precision
bf16
Seeds
43
43
,
44
44
,
45
45
Rollouts per question
G
G
8
8
Learning rate
2
×
10
−
6
2\times 10^{-6}
Per-device batch size
2
2
Schedule
constant, no warmup
Gradient accumulation
64
64
Optimizer
AdamW
(
Loshchilov and Hutter, 2019
)
Epochs
2
2
Rollout temperature
1.0
1.0
Rollout top-
k
k
50
50
Prompt budget
1,024
1{,}024
/
2,048
2{,}048
Clipping range
ϵ
\epsilon
0.2
0.2
Completion budget
8,192
8{,}192
/
6,144
6{,}144
KL coefficient
0
0
CREDO
Target mixture
γ
\gamma
0.5
0.5
Weighting strength
κ
\kappa
0.25
0.25
/
0.50
0.50
Calibration weight
α
\alpha
0.03
0.03
Weight clip
[
w
−
,
w
+
]
[w_{-},w_{+}]
[
0.5
,
2.0
]
[0.5,\,2.0]
Format weight
β
\beta
0.5
0.5
Warmup for
α
\alpha
and
κ
\kappa
30
30
steps
B.3
Evaluation and metrics
Mathematics trains on DeepScaleR, code on DeepCoder, and each domain is
evaluated on the sets of Table
B.3
. We evaluate at temperature
0.7
0.7
, generating each trained run under its own training seed; the base model
has no training seed, so its error bars come from the three evaluation seeds.
Table 5:
Datasets.
n
n
is the number of samples drawn per problem at
evaluation. AIME and AMC are the corresponding years’ competition problems;
HumanEval+ strengthens the tests of HumanEval
(
Chen et al., 2021
)
.
Mathematics
Code
Set
Problems
n
n
Set
Problems
n
n
DeepScaleR (train)
9,500
9{,}500
—
DeepCoder (train)
9,500
9{,}500
—
DeepScaleR test
500
500
4
DeepCoder test
500
500
4
MATH-500
500
500
4
HumanEval+
163
163
4
AIME 2024
30
30
8
LiveCodeBench v5
279
279
4
AIME 2025
30
30
8
LiveCodeBench v6
131
131
4
AIME 2026
30
30
8
AMC 2023
46
46
8
AMC 2024
45
45
8
Write
{
(
c
i
,
a
i
)
}
i
=
1
n
\{(c_{i},a_{i})\}_{i=1}^{n}
for an evaluation pool, with
c
i
c_{i}
the reported
confidence and
a
i
∈
{
0
,
1
}
a_{i}\in\{0,1\}
the correctness, decided by symbolic equivalence
in mathematics
(
Hugging Face, 2025
)
and by executing the program against the
problem’s tests in code.
Digit-probability expectation.
The
-d
rows throughout the paper replace the
sampled numeral with a continuous value derived from the model’s token
probabilities at the confidence slot. Given the verbalized format
<confidence>0.
d
</confidence>
, we teacher-force the prefix up
to the confidence position and read the logits at two slots:
•
Integer position
(candidates “0” and “1”), renormalized:
p
^
0
,
p
^
1
\hat{p}_{0},\;\hat{p}_{1}
.
•
Decimal position
(candidates “0” through “9”), renormalized:
q
^
d
\hat{q}_{d}
for
d
=
0
,
…
,
9
d=0,\dots,9
.
The confidence is a mixture over the two integer outcomes:
c
=
p
^
1
⋅
1.0
+
p
^
0
⋅
𝔼
⁡
[
d
]
10
,
𝔼
⁡
[
d
]
=
∑
d
=
0
9
d
​
q
^
d
.
c\;=\;\hat{p}_{1}\cdot 1.0\;+\;\hat{p}_{0}\cdot\frac{\mathbb{E}[d]}{10},\qquad\mathbb{E}[d]=\sum_{d=0}^{9}d\,\hat{q}_{d}\,.
(19)
The mixture covers
[
0
,
1
]
[0,1]
continuously. Probabilities are renormalized
within each candidate set, and the logits are read from the existing rollout
without an additional forward pass.
We report the following metrics over each evaluation pool:
•
Accuracy
is the mean of
a
i
a_{i}
.
•
ECE
uses ten equal-width bins
B
1
,
…
,
B
10
B_{1},\dots,B_{10}
(
Pakdaman Naeini et al., 2015
;
Guo et al., 2017
)
, with
0
0
and
1
1
falling in the first and last bin:
ECE
=
∑
b
=
1
10
|
B
b
|
n
​
|
a
¯
B
b
−
c
¯
B
b
|
,
\mathrm{ECE}=\sum_{b=1}^{10}\frac{|B_{b}|}{n}\,\big|\overline{a}_{B_{b}}-\overline{c}_{B_{b}}\big|,
(20)
where
a
¯
B
\overline{a}_{B}
and
c
¯
B
\overline{c}_{B}
are the bin’s mean correctness and
mean confidence.
•
Brier
is the mean squared error,
1
n
​
∑
i
(
c
i
−
a
i
)
2
\frac{1}{n}\sum_{i}(c_{i}-a_{i})^{2}
(
Brier, 1950
)
.
•
AUROC
is the area under the ROC curve
(
Hanley and McNeil, 1982
)
obtained
by scoring
a
a
with
c
c
.
•
Selective prediction
(AURC, acc@
τ
\tau
, Thr.)
(
Geifman and El-Yaniv, 2017
)
answers questions
in decreasing order of
c
c
. Equal confidences cannot be separated by a
threshold, so the achievable coverages are the boundaries of the tie groups:
for the distinct values
v
1
>
⋯
>
v
K
v_{1}>\dots>v_{K}
of
c
c
,
cov
k
=
|
{
i
:
c
i
≥
v
k
}
|
n
,
acc
k
=
1
|
{
i
:
c
i
≥
v
k
}
|
∑
i
:
c
i
≥
v
k
a
i
,
\mathrm{cov}_{k}=\frac{|\{i:c_{i}\geq v_{k}\}|}{n},\qquad\mathrm{acc}_{k}=\frac{1}{|\{i:c_{i}\geq v_{k}\}|}\sum_{i:\,c_{i}\geq v_{k}}a_{i},
(21)
and Thr. is the number
K
K
of achievable points. AURC integrates the risk
1
−
acc
1-\mathrm{acc}
against coverage over
[
0
,
1
]
[0,1]
by the trapezoid rule, extended
as a constant below
cov
1
\mathrm{cov}_{1}
, and
acc
​
@
​
τ
\mathrm{acc}@\tau
interpolates
(
cov
k
,
acc
k
)
(\mathrm{cov}_{k},\mathrm{acc}_{k})
linearly in coverage.
Appendix C
Additional analyses
C.1
Additional model scales
The main table uses Qwen3-8B. Table
C.1
runs the same mathematics
comparison at 1.7B and 4B (seed 43), with the 8B seed-43 run included for
direct comparison; three-seed averages for 8B appear in Table
1
.
Accuracy grows with model size for every method. CREDO leads on all four
metrics at every scale, and its calibration advantage widens as models grow
larger. The digit-expectation rows (-d) consistently outrank their verbalized
counterparts in AUROC at all three scales, indicating that sampling noise is not
specific to 8B.
Table 6:
Mathematics results at three model scales (seed 43). All
methods follow the same protocol as Table
1
.
-d
rows evaluate through the digit expectation;
CREDO
through its logit readout.
Bold
marks the best in each column.
Qwen3-1.7B
Qwen3-4B
Qwen3-8B
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Base
.268
.531
.691
.477
.425
.468
.641
.447
.440
.474
.640
.455
GRPO
.460
.391
.782
.357
.660
.221
.813
.220
.717
.174
.820
.179
RLCR
.494
.145
.853
.155
.663
.186
.836
.185
.682
.167
.837
.181
DCPO
.501
.203
.823
.189
.651
.220
.797
.196
.715
.222
.846
.195
Base-d
.268
.557
.717
.495
.425
.446
.765
.428
.440
.443
.772
.425
GRPO-d
.460
.379
.806
.350
.660
.208
.851
.211
.717
.170
.886
.184
RLCR-d
.494
.152
.867
.154
.663
.191
.866
.190
.682
.164
.855
.180
DCPO-d
.501
.214
.873
.191
.651
.183
.871
.186
.715
.184
.852
.180
CREDO
.514
.115
.905
.122
.689
.116
.884
.128
.753
.094
.933
.088
C.2
Emission and training-path decomposition
Table
2
removes one component at a time while keeping the rest
of CREDO intact. To disentangle the emission from the training path, we fill
the two remaining cells of the
2
×
2
2{\times}2
design space
(Table
C.2
) and add one fully decoupled reference. All arms
follow the protocol of Table
1
.
Table 7:
Design space for the confidence channel.
Score-function reward
Differentiable regression
Verbalized numeral
RLCR / DCPO (Table
1
)
Digit-exp. emission
{
H
,
L
}
\{H,L\}
readout
Readout + reward only
CREDO (Table
1
)
•
Digit-expectation emission.
The confidence slot produces a
verbalized numeral, but the value used for training and evaluation is the
continuous expectation over the digit probabilities rather than the {H,L}
logit readout. The regression loss, target, and discrepancy weighting are all
kept; only the emission differs from CREDO.
•
Readout + reward only.
The {H,L} readout is kept, but
differentiable regression is removed and the readout tokens are trained through
the reward signal via policy gradient, as in verbalized methods. Only the
training path differs from CREDO.
•
GRPO + auxiliary head.
A standard GRPO model whose answer reward
uses accuracy alone. The confidence channel plays no role in policy training; a
separate BCE head at the readout position learns to predict per-rollout
correctness.
Changing either axis alone degrades performance. Replacing the dedicated token
pair with a digit-probability expectation while keeping the regression causes
the largest drop: the verbalized digit distribution, though continuous, provides
a weaker training signal. Keeping the readout but training it only through the
reward also hurts, which confirms that differentiable regression is what drives
the calibration gains. A standalone BCE head on top of GRPO provides a natural
lower bound; it achieves reasonable calibration, but CREDO outperforms it on
every metric—optimizing the readout inside the training loop works better than
attaching a head afterward.
Table 8:
Emission and training-path decomposition (seed 43).
Bold
marks the best in each column.
Mathematics
Code
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
CREDO (full)
.753
.094
.933
.088
.614
.052
.869
.117
Digit-exp. emission
.676
.251
.671
.218
.587
.180
.724
.229
Readout + reward only
.695
.262
.869
.252
.588
.187
.818
.186
GRPO + auxiliary head
.702
.106
.902
.111
.599
.125
.832
.155
C.3
Discrepancy weighting on verbalized baselines
Table
2
shows that discrepancy weighting contributes
substantially to accuracy. A natural question is whether the same weighting
transfers to verbalized baselines. Table
C.3
adds it to RLCR
and DCPO, varying the source of the confidence value
c
c
in the weight
w
∝
|
a
−
c
|
w\propto|a-c|
:
•
Parsed numeral.
The weight uses each baseline’s own parsed
confidence value. With only a handful of distinct values per group, rollouts
within a group share one of only a few distinct weights.
•
Digit-probability expectation.
The weight uses the continuous
expectation over each baseline’s own digit logits, so that rollouts within a
group receive distinct weights even when their verbalized reports coincide.
Adding discrepancy weighting to RLCR or DCPO does not reproduce the accuracy
improvement that CREDO obtains from the same mechanism
(Table
2
), because the verbalized channel cannot supply the
per-rollout confidence variation the weighting needs. With parsed numerals,
collapsed values leave rollouts in a group sharing one of only a few
distinct weights, so the reweighting barely acts. Digit-expectation confidence gives the weights more
variation, but does not close the gap either: for DCPO, accuracy drops in both
domains, and calibration worsens in mathematics though it improves on
several code metrics. Whether the confidence is read as a parsed numeral or as a
continuous expectation, the verbalized channel does not give the weighting
enough signal to redistribute learning. CREDO’s readout varies continuously
across rollouts, which lets the weighting concentrate updates on those where
confidence and outcome disagree most—and that is where the accuracy gains
come from.
Table 9:
Verbalized baselines with discrepancy weighting (seed 43).
The Eval column indicates the confidence source at evaluation.
Shaded rows
evaluate through the digit-probability
expectation;
CREDO
through its logit readout; unshaded rows
through the parsed verbalized numeral.
Bold
marks the best in each
column.
Mathematics
Code
Eval
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
RLCR
verbalized
.682
.167
.837
.181
.539
.070
.820
.144
RLCR + weighting (parsed)
verbalized
.701
.142
.837
.152
.545
.104
.818
.155
RLCR + weighting (digit-exp)
verbalized
.697
.141
.847
.148
.542
.085
.810
.149
RLCR
digit-exp
.682
.164
.855
.180
.539
.078
.822
.144
RLCR + weighting (parsed)
digit-exp
.701
.151
.857
.152
.545
.108
.823
.153
RLCR + weighting (digit-exp)
digit-exp
.697
.152
.866
.147
.542
.090
.813
.147
DCPO
verbalized
.715
.222
.846
.195
.579
.180
.747
.179
DCPO + weighting (parsed)
verbalized
.716
.223
.816
.203
.581
.150
.791
.154
DCPO + weighting (digit-exp)
verbalized
.690
.277
.780
.262
.560
.153
.801
.153
DCPO
digit-exp
.715
.184
.852
.180
.579
.179
.842
.178
DCPO + weighting (parsed)
digit-exp
.716
.187
.865
.187
.581
.147
.850
.151
DCPO + weighting (digit-exp)
digit-exp
.690
.221
.785
.233
.560
.149
.818
.147
CREDO
readout
.753
.094
.933
.088
.614
.052
.869
.117
C.4
Shape of the answer reward
We compare the answer-segment reward with two variants of it:
•
additive
(CREDO, equation
8
):
r
ans
=
β
​
F
+
a
r^{\mathrm{ans}}=\beta F+a
;
•
gated
:
r
ans
=
F
⁡
(
β
+
a
)
r^{\mathrm{ans}}=F\,(\beta+a)
;
•
no format term
:
r
ans
=
a
r^{\mathrm{ans}}=a
.
The additive form is best or tied on every metric in mathematics, and neither
variant dominates it in code (Table
C.4
).
Under the gated form, a format failure zeroes out the entire reward including
the correctness signal, which slows accuracy learning. Removing the format term
has a milder effect on accuracy but yields mixed results on calibration.
Table 10:
Answer-reward shapes on seed 43; all else follows
Table
B.2
.
Mathematics
Code
r
ans
r^{\mathrm{ans}}
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
β
​
F
+
a
\beta F+a
.753
.094
.933
.088
.614
.052
.869
.117
F
⁡
(
β
+
a
)
F\,(\beta+a)
.714
.105
.910
.110
.589
.038
.871
.113
a
a
.723
.113
.924
.091
.583
.042
.889
.102
C.5
Calibration curves
Figure
C.5
shows calibration curves for all methods in both
domains. The verbalized baselines resolve only a handful of points, reflecting
the collapse documented in Figure
2
: with few distinct
confidence values, each bin absorbs a large share of the evaluation pool. Most
of these points fall below the diagonal, indicating systematic overconfidence.
CREDO’s readout, by contrast, populates the full confidence range and tracks the
diagonal closely. We use equal-mass bins here so that every marker represents a
comparable number of samples; the quantitative ECE in Table
1
uses
the standard ten equal-width bins defined in Appendix
B.3
.
Figure 6:
Calibration curves, pooled over the three seeds and over
each domain’s evaluation sets. Baselines report through their verbalized
numeral, CREDO through its readout. Equal-mass bins; bars are Wilson 95%
intervals
(
Wilson, 1927
)
.
Appendix D
Extended quantitative results
D.1
Per-set results
Tables
D.1
–
D.1
decompose
Table
1
by evaluation set, in domain and under transfer. Entries
are mean
±
\pm
std over the three seeds. The Average column reproduces
Table
1
. DeepScaleR and DeepCoder name the in-distribution test
splits.
Table 11:
Per-set results on mathematics.
DeepScaleR
MATH-500
AIME-24
AIME-25
AIME-26
AMC-23
AMC-24
Average
Accuracy
↑
\uparrow
Base
.603
±
\pm
.005
.821
±
\pm
.004
.240
±
\pm
.013
.172
±
\pm
.009
.136
±
\pm
.002
.599
±
\pm
.010
.503
±
\pm
.008
.439
±
\pm
.001
GRPO
.836
±
\pm
.006
.939
±
\pm
.001
.610
±
\pm
.021
.451
±
\pm
.021
.475
±
\pm
.030
.856
±
\pm
.014
.779
±
\pm
.014
.706
±
\pm
.009
RLCR
.821
±
\pm
.011
.932
±
\pm
.006
.564
±
\pm
.021
.382
±
\pm
.010
.465
±
\pm
.039
.851
±
\pm
.021
.762
±
\pm
.008
.682
±
\pm
.010
DCPO
.845
±
\pm
.003
.944
±
\pm
.007
.624
±
\pm
.035
.478
±
\pm
.009
.521
±
\pm
.019
.864
±
\pm
.018
.780
±
\pm
.029
.722
±
\pm
.008
Base-d
.603
±
\pm
.005
.821
±
\pm
.004
.240
±
\pm
.013
.172
±
\pm
.009
.136
±
\pm
.002
.599
±
\pm
.010
.503
±
\pm
.008
.439
±
\pm
.001
GRPO-d
.836
±
\pm
.006
.939
±
\pm
.001
.610
±
\pm
.021
.451
±
\pm
.021
.475
±
\pm
.030
.856
±
\pm
.014
.779
±
\pm
.014
.706
±
\pm
.009
RLCR-d
.821
±
\pm
.011
.932
±
\pm
.006
.564
±
\pm
.021
.382
±
\pm
.010
.465
±
\pm
.039
.851
±
\pm
.021
.762
±
\pm
.008
.682
±
\pm
.010
DCPO-d
.845
±
\pm
.003
.944
±
\pm
.007
.624
±
\pm
.035
.478
±
\pm
.009
.521
±
\pm
.019
.864
±
\pm
.018
.780
±
\pm
.029
.722
±
\pm
.008
CREDO
.850
±
\pm
.003
.953
±
\pm
.002
.682
±
\pm
.032
.504
±
\pm
.015
.561
±
\pm
.042
.909
±
\pm
.015
.801
±
\pm
.008
.752
±
\pm
.013
ECE
↓
\downarrow
Base
.317
±
\pm
.005
.118
±
\pm
.004
.660
±
\pm
.011
.714
±
\pm
.018
.751
±
\pm
.005
.329
±
\pm
.009
.416
±
\pm
.013
.472
±
\pm
.002
GRPO
.093
±
\pm
.017
.028
±
\pm
.007
.254
±
\pm
.054
.396
±
\pm
.066
.388
±
\pm
.037
.083
±
\pm
.019
.149
±
\pm
.028
.199
±
\pm
.027
RLCR
.054
±
\pm
.003
.078
±
\pm
.033
.196
±
\pm
.029
.345
±
\pm
.030
.266
±
\pm
.032
.103
±
\pm
.017
.072
±
\pm
.024
.159
±
\pm
.012
DCPO
.129
±
\pm
.002
.048
±
\pm
.006
.279
±
\pm
.039
.388
±
\pm
.014
.379
±
\pm
.029
.107
±
\pm
.015
.189
±
\pm
.019
.217
±
\pm
.008
Base-d
.276
±
\pm
.005
.113
±
\pm
.006
.626
±
\pm
.015
.694
±
\pm
.010
.731
±
\pm
.005
.284
±
\pm
.010
.374
±
\pm
.011
.442
±
\pm
.001
GRPO-d
.058
±
\pm
.012
.076
±
\pm
.011
.252
±
\pm
.036
.390
±
\pm
.047
.368
±
\pm
.021
.088
±
\pm
.053
.109
±
\pm
.018
.192
±
\pm
.025
RLCR-d
.070
±
\pm
.005
.101
±
\pm
.017
.201
±
\pm
.002
.336
±
\pm
.025
.256
±
\pm
.024
.107
±
\pm
.014
.073
±
\pm
.011
.163
±
\pm
.005
DCPO-d
.065
±
\pm
.012
.083
±
\pm
.012
.249
±
\pm
.021
.359
±
\pm
.037
.329
±
\pm
.029
.121
±
\pm
.021
.108
±
\pm
.015
.188
±
\pm
.010
CREDO
.033
±
\pm
.016
.051
±
\pm
.021
.128
±
\pm
.017
.129
±
\pm
.021
.171
±
\pm
.007
.111
±
\pm
.029
.099
±
\pm
.026
.103
±
\pm
.013
AUROC
↑
\uparrow
Base
.619
±
\pm
.018
.663
±
\pm
.018
.674
±
\pm
.015
.653
±
\pm
.025
.641
±
\pm
.011
.620
±
\pm
.024
.640
±
\pm
.017
.644
±
\pm
.004
GRPO
.699
±
\pm
.044
.732
±
\pm
.031
.820
±
\pm
.090
.826
±
\pm
.072
.840
±
\pm
.069
.787
±
\pm
.102
.722
±
\pm
.031
.775
±
\pm
.062
RLCR
.737
±
\pm
.021
.843
±
\pm
.008
.863
±
\pm
.029
.871
±
\pm
.003
.877
±
\pm
.037
.848
±
\pm
.018
.781
±
\pm
.017
.831
±
\pm
.009
DCPO
.752
±
\pm
.009
.813
±
\pm
.037
.913
±
\pm
.033
.882
±
\pm
.017
.921
±
\pm
.024
.863
±
\pm
.042
.793
±
\pm
.049
.848
±
\pm
.012
Base-d
.703
±
\pm
.007
.829
±
\pm
.009
.791
±
\pm
.020
.779
±
\pm
.020
.768
±
\pm
.021
.770
±
\pm
.007
.711
±
\pm
.039
.765
±
\pm
.010
GRPO-d
.768
±
\pm
.027
.866
±
\pm
.013
.900
±
\pm
.029
.900
±
\pm
.013
.906
±
\pm
.024
.907
±
\pm
.024
.804
±
\pm
.024
.864
±
\pm
.020
RLCR-d
.754
±
\pm
.011
.870
±
\pm
.009
.877
±
\pm
.020
.891
±
\pm
.010
.901
±
\pm
.024
.877
±
\pm
.019
.798
±
\pm
.007
.852
±
\pm
.006
DCPO-d
.749
±
\pm
.009
.847
±
\pm
.038
.903
±
\pm
.028
.903
±
\pm
.007
.938
±
\pm
.019
.887
±
\pm
.053
.776
±
\pm
.043
.858
±
\pm
.006
CREDO
.846
±
\pm
.011
.926
±
\pm
.017
.961
±
\pm
.002
.941
±
\pm
.027
.968
±
\pm
.007
.954
±
\pm
.009
.935
±
\pm
.013
.933
±
\pm
.007
Brier
↓
\downarrow
Base
.326
±
\pm
.004
.150
±
\pm
.002
.608
±
\pm
.010
.657
±
\pm
.018
.691
±
\pm
.006
.336
±
\pm
.010
.406
±
\pm
.011
.453
±
\pm
.002
GRPO
.133
±
\pm
.009
.051
±
\pm
.002
.251
±
\pm
.053
.359
±
\pm
.071
.348
±
\pm
.045
.116
±
\pm
.015
.172
±
\pm
.021
.204
±
\pm
.029
RLCR
.130
±
\pm
.009
.057
±
\pm
.005
.214
±
\pm
.012
.291
±
\pm
.024
.250
±
\pm
.018
.106
±
\pm
.011
.151
±
\pm
.006
.171
±
\pm
.009
DCPO
.130
±
\pm
.001
.047
±
\pm
.006
.250
±
\pm
.029
.345
±
\pm
.005
.330
±
\pm
.048
.104
±
\pm
.014
.181
±
\pm
.012
.198
±
\pm
.003
Base-d
.304
±
\pm
.004
.143
±
\pm
.003
.565
±
\pm
.013
.619
±
\pm
.010
.648
±
\pm
.006
.310
±
\pm
.008
.376
±
\pm
.009
.424
±
\pm
.001
GRPO-d
.127
±
\pm
.008
.054
±
\pm
.001
.262
±
\pm
.041
.360
±
\pm
.054
.340
±
\pm
.029
.111
±
\pm
.017
.169
±
\pm
.015
.203
±
\pm
.023
RLCR-d
.129
±
\pm
.008
.059
±
\pm
.004
.218
±
\pm
.015
.288
±
\pm
.022
.245
±
\pm
.016
.107
±
\pm
.011
.150
±
\pm
.004
.171
±
\pm
.009
DCPO-d
.122
±
\pm
.002
.050
±
\pm
.004
.249
±
\pm
.019
.339
±
\pm
.045
.308
±
\pm
.048
.106
±
\pm
.011
.165
±
\pm
.006
.191
±
\pm
.013
CREDO
.093
±
\pm
.004
.030
±
\pm
.003
.091
±
\pm
.007
.122
±
\pm
.010
.114
±
\pm
.007
.060
±
\pm
.012
.092
±
\pm
.007
.086
±
\pm
.004
Table 12:
Per-set results on code, models trained on mathematics.
Accuracy
↑
\uparrow
ECE
↓
\downarrow
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
GRPO
.389
±
\pm
.015
.852
±
\pm
.003
.400
±
\pm
.002
.338
±
\pm
.007
.495
±
\pm
.004
.418
±
\pm
.058
.086
±
\pm
.011
.360
±
\pm
.042
.396
±
\pm
.057
.315
±
\pm
.041
RLCR
.388
±
\pm
.006
.858
±
\pm
.003
.400
±
\pm
.009
.365
±
\pm
.007
.502
±
\pm
.002
.311
±
\pm
.027
.054
±
\pm
.017
.271
±
\pm
.017
.276
±
\pm
.022
.228
±
\pm
.014
DCPO
.394
±
\pm
.022
.861
±
\pm
.004
.415
±
\pm
.025
.363
±
\pm
.019
.508
±
\pm
.014
.436
±
\pm
.059
.153
±
\pm
.017
.344
±
\pm
.047
.387
±
\pm
.049
.330
±
\pm
.040
GRPO-d
.389
±
\pm
.015
.852
±
\pm
.003
.400
±
\pm
.002
.338
±
\pm
.007
.495
±
\pm
.004
.405
±
\pm
.040
.050
±
\pm
.002
.345
±
\pm
.031
.391
±
\pm
.042
.298
±
\pm
.028
RLCR-d
.388
±
\pm
.006
.858
±
\pm
.003
.400
±
\pm
.009
.365
±
\pm
.007
.502
±
\pm
.002
.315
±
\pm
.022
.056
±
\pm
.011
.270
±
\pm
.016
.285
±
\pm
.023
.232
±
\pm
.013
DCPO-d
.394
±
\pm
.022
.861
±
\pm
.004
.415
±
\pm
.025
.363
±
\pm
.019
.508
±
\pm
.014
.384
±
\pm
.036
.050
±
\pm
.021
.304
±
\pm
.031
.361
±
\pm
.039
.275
±
\pm
.027
CREDO
.401
±
\pm
.025
.853
±
\pm
.016
.406
±
\pm
.030
.357
±
\pm
.018
.504
±
\pm
.021
.178
±
\pm
.019
.062
±
\pm
.010
.148
±
\pm
.016
.165
±
\pm
.025
.138
±
\pm
.016
AUROC
↑
\uparrow
Brier
↓
\downarrow
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
GRPO
.765
±
\pm
.033
.611
±
\pm
.036
.733
±
\pm
.026
.777
±
\pm
.041
.721
±
\pm
.032
.390
±
\pm
.058
.127
±
\pm
.005
.349
±
\pm
.039
.365
±
\pm
.059
.308
±
\pm
.040
RLCR
.832
±
\pm
.005
.717
±
\pm
.025
.795
±
\pm
.003
.826
±
\pm
.011
.792
±
\pm
.005
.279
±
\pm
.017
.118
±
\pm
.003
.263
±
\pm
.011
.255
±
\pm
.015
.229
±
\pm
.010
DCPO
.776
±
\pm
.052
.626
±
\pm
.058
.784
±
\pm
.025
.799
±
\pm
.031
.746
±
\pm
.038
.415
±
\pm
.047
.153
±
\pm
.018
.338
±
\pm
.036
.366
±
\pm
.044
.318
±
\pm
.032
GRPO-d
.827
±
\pm
.029
.702
±
\pm
.035
.794
±
\pm
.019
.846
±
\pm
.024
.792
±
\pm
.026
.380
±
\pm
.041
.122
±
\pm
.003
.338
±
\pm
.028
.358
±
\pm
.042
.299
±
\pm
.028
RLCR-d
.850
±
\pm
.006
.754
±
\pm
.026
.821
±
\pm
.006
.838
±
\pm
.017
.816
±
\pm
.003
.281
±
\pm
.015
.110
±
\pm
.002
.258
±
\pm
.011
.255
±
\pm
.017
.226
±
\pm
.011
DCPO-d
.803
±
\pm
.023
.688
±
\pm
.022
.807
±
\pm
.026
.812
±
\pm
.030
.778
±
\pm
.021
.366
±
\pm
.025
.119
±
\pm
.004
.309
±
\pm
.019
.337
±
\pm
.027
.283
±
\pm
.017
CREDO
.869
±
\pm
.010
.735
±
\pm
.033
.858
±
\pm
.013
.883
±
\pm
.003
.836
±
\pm
.009
.191
±
\pm
.008
.120
±
\pm
.011
.176
±
\pm
.009
.173
±
\pm
.010
.165
±
\pm
.008
Table 13:
Per-set results on code.
Accuracy
↑
\uparrow
ECE
↓
\downarrow
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
Base
.318
±
\pm
.004
.829
±
\pm
.007
.345
±
\pm
.012
.330
±
\pm
.007
.455
±
\pm
.001
.558
±
\pm
.005
.105
±
\pm
.008
.503
±
\pm
.012
.506
±
\pm
.001
.418
±
\pm
.001
GRPO
.475
±
\pm
.006
.882
±
\pm
.011
.522
±
\pm
.008
.443
±
\pm
.007
.581
±
\pm
.007
.229
±
\pm
.070
.113
±
\pm
.098
.187
±
\pm
.083
.199
±
\pm
.036
.182
±
\pm
.070
RLCR
.449
±
\pm
.008
.872
±
\pm
.019
.480
±
\pm
.017
.412
±
\pm
.016
.553
±
\pm
.013
.049
±
\pm
.014
.111
±
\pm
.017
.068
±
\pm
.010
.071
±
\pm
.016
.075
±
\pm
.005
DCPO
.477
±
\pm
.016
.878
±
\pm
.016
.525
±
\pm
.013
.422
±
\pm
.010
.576
±
\pm
.003
.167
±
\pm
.031
.112
±
\pm
.015
.178
±
\pm
.041
.156
±
\pm
.013
.153
±
\pm
.024
Base-d
.318
±
\pm
.004
.829
±
\pm
.007
.345
±
\pm
.012
.330
±
\pm
.007
.455
±
\pm
.001
.528
±
\pm
.004
.074
±
\pm
.017
.474
±
\pm
.012
.481
±
\pm
.003
.389
±
\pm
.002
GRPO-d
.475
±
\pm
.006
.882
±
\pm
.011
.522
±
\pm
.008
.443
±
\pm
.007
.581
±
\pm
.007
.218
±
\pm
.038
.040
±
\pm
.019
.150
±
\pm
.022
.213
±
\pm
.030
.155
±
\pm
.022
RLCR-d
.449
±
\pm
.008
.872
±
\pm
.019
.480
±
\pm
.017
.412
±
\pm
.016
.553
±
\pm
.013
.056
±
\pm
.013
.115
±
\pm
.014
.066
±
\pm
.012
.082
±
\pm
.017
.080
±
\pm
.004
DCPO-d
.477
±
\pm
.016
.878
±
\pm
.016
.525
±
\pm
.013
.422
±
\pm
.010
.576
±
\pm
.003
.164
±
\pm
.031
.112
±
\pm
.015
.176
±
\pm
.041
.157
±
\pm
.013
.152
±
\pm
.025
CREDO
.509
±
\pm
.027
.881
±
\pm
.006
.563
±
\pm
.016
.448
±
\pm
.024
.600
±
\pm
.018
.049
±
\pm
.012
.062
±
\pm
.046
.069
±
\pm
.009
.076
±
\pm
.017
.064
±
\pm
.020
AUROC
↑
\uparrow
Brier
↓
\downarrow
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
DeepCoder
HumanEval+
LCB v5
LCB v6
Average
Base
.701
±
\pm
.010
.628
±
\pm
.019
.695
±
\pm
.006
.735
±
\pm
.012
.690
±
\pm
.004
.513
±
\pm
.006
.146
±
\pm
.006
.464
±
\pm
.009
.454
±
\pm
.007
.395
±
\pm
.002
GRPO
.791
±
\pm
.094
.605
±
\pm
.033
.794
±
\pm
.083
.822
±
\pm
.057
.753
±
\pm
.061
.237
±
\pm
.067
.156
±
\pm
.097
.215
±
\pm
.074
.211
±
\pm
.035
.205
±
\pm
.066
RLCR
.845
±
\pm
.003
.763
±
\pm
.028
.825
±
\pm
.017
.825
±
\pm
.020
.815
±
\pm
.014
.156
±
\pm
.003
.110
±
\pm
.004
.166
±
\pm
.008
.150
±
\pm
.012
.146
±
\pm
.006
DCPO
.834
±
\pm
.032
.603
±
\pm
.040
.829
±
\pm
.040
.839
±
\pm
.017
.776
±
\pm
.025
.168
±
\pm
.030
.113
±
\pm
.014
.177
±
\pm
.041
.155
±
\pm
.014
.153
±
\pm
.024
Base-d
.796
±
\pm
.010
.719
±
\pm
.022
.782
±
\pm
.006
.832
±
\pm
.006
.782
±
\pm
.003
.482
±
\pm
.004
.141
±
\pm
.006
.437
±
\pm
.009
.432
±
\pm
.006
.373
±
\pm
.002
GRPO-d
.874
±
\pm
.033
.713
±
\pm
.047
.861
±
\pm
.031
.884
±
\pm
.027
.833
±
\pm
.034
.230
±
\pm
.036
.098
±
\pm
.010
.192
±
\pm
.024
.214
±
\pm
.030
.184
±
\pm
.025
RLCR-d
.848
±
\pm
.001
.775
±
\pm
.027
.826
±
\pm
.017
.821
±
\pm
.018
.818
±
\pm
.011
.155
±
\pm
.001
.110
±
\pm
.003
.165
±
\pm
.008
.151
±
\pm
.012
.145
±
\pm
.005
DCPO-d
.883
±
\pm
.034
.730
±
\pm
.081
.887
±
\pm
.051
.896
±
\pm
.031
.849
±
\pm
.027
.165
±
\pm
.031
.112
±
\pm
.015
.175
±
\pm
.041
.155
±
\pm
.013
.152
±
\pm
.025
CREDO
.889
±
\pm
.025
.736
±
\pm
.045
.888
±
\pm
.023
.887
±
\pm
.029
.850
±
\pm
.027
.131
±
\pm
.012
.115
±
\pm
.037
.132
±
\pm
.010
.129
±
\pm
.010
.127
±
\pm
.016
Table 14:
Per-set results on mathematics, models trained on code.
DeepScaleR
MATH-500
AIME-24
AIME-25
AIME-26
AMC-23
AMC-24
Average
Accuracy
↑
\uparrow
GRPO
.743
±
\pm
.004
.892
±
\pm
.005
.374
±
\pm
.016
.276
±
\pm
.009
.288
±
\pm
.004
.728
±
\pm
.003
.644
±
\pm
.010
.564
±
\pm
.003
RLCR
.701
±
\pm
.016
.873
±
\pm
.009
.324
±
\pm
.009
.233
±
\pm
.026
.207
±
\pm
.016
.688
±
\pm
.024
.579
±
\pm
.025
.515
±
\pm
.011
DCPO
.721
±
\pm
.009
.894
±
\pm
.002
.357
±
\pm
.010
.240
±
\pm
.024
.253
±
\pm
.013
.727
±
\pm
.004
.644
±
\pm
.017
.548
±
\pm
.003
GRPO-d
.743
±
\pm
.004
.892
±
\pm
.005
.374
±
\pm
.016
.276
±
\pm
.009
.288
±
\pm
.004
.728
±
\pm
.003
.644
±
\pm
.010
.564
±
\pm
.003
RLCR-d
.701
±
\pm
.016
.873
±
\pm
.009
.324
±
\pm
.009
.233
±
\pm
.026
.207
±
\pm
.016
.688
±
\pm
.024
.579
±
\pm
.025
.515
±
\pm
.011
DCPO-d
.721
±
\pm
.009
.894
±
\pm
.002
.357
±
\pm
.010
.240
±
\pm
.024
.253
±
\pm
.013
.727
±
\pm
.004
.644
±
\pm
.017
.548
±
\pm
.003
CREDO
.717
±
\pm
.021
.888
±
\pm
.013
.401
±
\pm
.038
.268
±
\pm
.017
.269
±
\pm
.023
.737
±
\pm
.020
.642
±
\pm
.027
.560
±
\pm
.007
ECE
↓
\downarrow
GRPO
.178
±
\pm
.010
.048
±
\pm
.009
.496
±
\pm
.035
.587
±
\pm
.038
.571
±
\pm
.033
.200
±
\pm
.012
.263
±
\pm
.007
.335
±
\pm
.019
RLCR
.034
±
\pm
.002
.102
±
\pm
.010
.249
±
\pm
.014
.306
±
\pm
.020
.328
±
\pm
.019
.055
±
\pm
.018
.117
±
\pm
.003
.170
±
\pm
.004
DCPO
.224
±
\pm
.006
.092
±
\pm
.009
.237
±
\pm
.044
.197
±
\pm
.061
.237
±
\pm
.034
.216
±
\pm
.015
.228
±
\pm
.023
.205
±
\pm
.021
GRPO-d
.133
±
\pm
.011
.063
±
\pm
.019
.468
±
\pm
.032
.569
±
\pm
.023
.551
±
\pm
.022
.165
±
\pm
.014
.227
±
\pm
.008
.311
±
\pm
.017
RLCR-d
.049
±
\pm
.005
.115
±
\pm
.007
.250
±
\pm
.008
.308
±
\pm
.015
.331
±
\pm
.018
.056
±
\pm
.014
.098
±
\pm
.020
.172
±
\pm
.006
DCPO-d
.224
±
\pm
.006
.091
±
\pm
.008
.234
±
\pm
.039
.196
±
\pm
.059
.238
±
\pm
.031
.214
±
\pm
.016
.225
±
\pm
.023
.203
±
\pm
.020
CREDO
.127
±
\pm
.071
.109
±
\pm
.086
.100
±
\pm
.036
.146
±
\pm
.071
.126
±
\pm
.067
.118
±
\pm
.073
.093
±
\pm
.063
.117
±
\pm
.030
AUROC
↑
\uparrow
GRPO
.682
±
\pm
.037
.739
±
\pm
.048
.773
±
\pm
.014
.780
±
\pm
.039
.767
±
\pm
.035
.682
±
\pm
.046
.712
±
\pm
.028
.734
±
\pm
.030
RLCR
.734
±
\pm
.013
.857
±
\pm
.005
.837
±
\pm
.029
.889
±
\pm
.041
.843
±
\pm
.017
.747
±
\pm
.020
.797
±
\pm
.032
.815
±
\pm
.016
DCPO
.686
±
\pm
.025
.747
±
\pm
.027
.769
±
\pm
.037
.837
±
\pm
.050
.815
±
\pm
.008
.711
±
\pm
.022
.720
±
\pm
.035
.755
±
\pm
.024
GRPO-d
.755
±
\pm
.003
.857
±
\pm
.015
.848
±
\pm
.024
.887
±
\pm
.009
.841
±
\pm
.004
.819
±
\pm
.014
.776
±
\pm
.015
.826
±
\pm
.004
RLCR-d
.748
±
\pm
.010
.876
±
\pm
.007
.856
±
\pm
.018
.907
±
\pm
.036
.861
±
\pm
.025
.762
±
\pm
.018
.819
±
\pm
.027
.833
±
\pm
.014
DCPO-d
.750
±
\pm
.005
.859
±
\pm
.028
.818
±
\pm
.019
.916
±
\pm
.047
.866
±
\pm
.016
.830
±
\pm
.022
.803
±
\pm
.036
.835
±
\pm
.004
CREDO
.736
±
\pm
.022
.874
±
\pm
.011
.900
±
\pm
.009
.944
±
\pm
.013
.850
±
\pm
.026
.845
±
\pm
.028
.834
±
\pm
.049
.855
±
\pm
.013
Brier
↓
\downarrow
GRPO
.207
±
\pm
.006
.090
±
\pm
.006
.452
±
\pm
.036
.525
±
\pm
.042
.510
±
\pm
.039
.220
±
\pm
.011
.268
±
\pm
.008
.325
±
\pm
.020
RLCR
.176
±
\pm
.008
.090
±
\pm
.002
.217
±
\pm
.011
.216
±
\pm
.011
.234
±
\pm
.012
.177
±
\pm
.008
.191
±
\pm
.008
.186
±
\pm
.007
DCPO
.228
±
\pm
.005
.091
±
\pm
.008
.235
±
\pm
.043
.197
±
\pm
.060
.237
±
\pm
.031
.216
±
\pm
.015
.229
±
\pm
.024
.205
±
\pm
.020
GRPO-d
.193
±
\pm
.007
.087
±
\pm
.007
.426
±
\pm
.031
.503
±
\pm
.028
.485
±
\pm
.030
.208
±
\pm
.005
.257
±
\pm
.006
.308
±
\pm
.015
RLCR-d
.175
±
\pm
.007
.089
±
\pm
.002
.213
±
\pm
.012
.214
±
\pm
.009
.232
±
\pm
.013
.175
±
\pm
.009
.186
±
\pm
.006
.184
±
\pm
.006
DCPO-d
.227
±
\pm
.006
.091
±
\pm
.008
.232
±
\pm
.039
.195
±
\pm
.059
.235
±
\pm
.030
.213
±
\pm
.015
.226
±
\pm
.023
.203
±
\pm
.020
CREDO
.188
±
\pm
.034
.092
±
\pm
.042
.130
±
\pm
.007
.111
±
\pm
.025
.153
±
\pm
.019
.155
±
\pm
.032
.164
±
\pm
.029
.142
±
\pm
.013
D.2
Sensitivity to the coefficients
Table
D.2
gives every evaluated setting of the three coefficients.
Table 15:
Every evaluated setting of the three coefficients
of §
3
, all on seed 43.
Mathematics
Code
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Acc
↑
\uparrow
ECE
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
Weighting strength
κ
\kappa
0
0
.721
.122
.904
.102
.572
.051
.843
.132
0.25
0.25
.753
.094
.933
.088
.584
.044
.854
.124
0.5
0.5
.749
.093
.924
.101
.614
.052
.869
.117
1
1
.730
.108
.924
.100
.591
.049
.858
.124
Calibration weight
α
\alpha
0
0
.696
.241
.880
.232
.611
.172
.857
.172
0.01
0.01
.715
.123
.912
.115
.581
.044
.851
.123
0.03
0.03
.753
.094
.933
.088
.614
.052
.869
.117
0.05
0.05
.708
.103
.910
.107
.583
.042
.857
.123
0.10
0.10
.716
.089
.915
.098
.577
.042
.867
.117
Target mixture
γ
\gamma
0
0
.732
.130
.918
.098
.593
.054
.854
.125
0.5
0.5
.753
.094
.933
.088
.614
.052
.869
.117
1
1
.738
.101
.924
.100
.587
.034
.855
.120