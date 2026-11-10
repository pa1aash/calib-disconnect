---
title: Zero-Overhead Introspectionfor Adaptive Test-Time Compute
id: zero-overhead-introspectionfor-adaptive-test-time-compute
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:07:48.780386Z'
updated: '2026-11-09T23:27:44.384381Z'
source: https://arxiv.org/html/2512.01457
source_domain: arxiv.org
fetched_at: '2026-11-09T23:07:48.780054Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Full text. ZIP-RC repurposes reserved logits to predict joint distribution
  over final reward and remaining length per token; adaptive sampling beats majority
  voting up to 12% at equal cost on AIME/AMC/MATH-500/GSM8K (Qwen3). Math only. RELATED
  to L3 (confidence-driven compute allocation, trained head).
---

Zero-Overhead Introspectionfor Adaptive Test-Time Compute
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2512.01457v4 [cs.LG] 23 Dec 2025
Zero-Overhead Introspection
for Adaptive Test-Time Compute
Rohin Manvi
2
2
footnotemark:
2
4
4
footnotemark:
4
†
†
thanks:
Corresponding author,
rohinm@berkeley.edu
Joey Hong
2
2
footnotemark:
2
†
†
thanks:
UC Berkeley
Tim Seyde
3
3
footnotemark:
3
4
4
footnotemark:
4
†
†
thanks:
MIT CSAIL
†
†
thanks:
Liquid AI
Maxime Labonne
4
4
footnotemark:
4
Mathias Lechner
3
3
footnotemark:
3
4
4
footnotemark:
4
Sergey Levine
2
2
footnotemark:
2
Abstract
Large language models excel at reasoning but lack key aspects of
introspection
, including the ability to anticipate their own success and the computation required to achieve it. Humans use real-time introspection to decide how much effort to invest, when to make multiple attempts, when to stop, and when to signal success or failure. Without this ability, LLMs struggle to make intelligent meta-cognition decisions. Test-time scaling methods such as Best-of-N drive up cost and latency by using a fixed budget of samples regardless of the marginal benefit of each one at any point in generation, and the absence of confidence signals can mislead people, prevent appropriate escalation to better tools, and undermine trustworthiness. Learned verifiers or reward models can provide confidence estimates, but do not enable adaptive inference and add substantial inference cost by requiring extra models or forward passes. We present ZIP-RC, which equips models with
z
ero-overhead
i
ntrospective
p
redictions of
r
eward and
c
ost. At every token during generation, ZIP-RC reuses reserved or unused logits in the same forward pass as next-token prediction to output a joint distribution over final reward and remaining length—no extra models, architecture change, or inference overhead. This full joint distribution is used to compute a sampling utility which is the linear combination of the expected maximum reward, total compute, and latency of set of samples if generated to completion. During inference, we maximize this utility with meta-actions that determine which prefix of tokens to continue or initiate sampling from. On mixed-difficulty mathematical benchmarks, ZIP-RC improves accuracy by up to
12
%
12\%
over majority voting at equal or lower average cost, and traces smooth Pareto frontiers between quality, compute, and latency. By providing real-time reward–cost introspection, ZIP-RC allows models to reason adaptively and more efficiently.
Figure 1:
Top left shows how ZIP repurposes reserved or unused logits in the output head of a language model to instantiate auxiliary predictions, such as the grid mapping for the joint reward-cost distribution that ZIP-RC uses. Top right demonstrates how ZIP-RC can provide real-time expected reward and remaining length predictions. Finally, the bottom shows the joint distributions from ZIP-RC and how they indicate optimal sampling strategies. ZIP-RC sampling uses these joint distributions to calculate a sampling utility to autonomously select meta-actions for optimal test-time compute allocation.
1
Introduction
The rapid evolution of large language models (LLMs) has enabled unprecedented capabilities in complex tasks ranging from general question-answering to automated coding and mathematical reasoning
(
Brown et al., 2020
;
Kojima et al., 2022
;
Wei et al., 2022
)
. To become truly reliable, however, LLMs must develop a capacity for
introspection
: the ability to assess their own progress and anticipate the effort required to succeed. Humans can be instrospective and can effectively act upon this information to make better decisions. If a model could predict its future success (reward)
and
the resources needed to achieve it (cost), it could allocate compute more effectively, expose likely failure modes before they occur, and provide transparent signals about confidence and anticipated “thinking time.” A key obstacle has been that such introspection typically requires auxiliary mechanisms that add nontrivial computational overhead and complexity.
The need for introspection is growing more urgent as reasoning traces continue to lengthen. Recent work shows that scaling
test-time
compute through reasoning often yields larger performance gains than simply increasing model size
(
Wang et al., 2023b
;
Yao et al., 2023
;
Jaech et al., 2024
;
Snell et al., 2024
;
Guo et al., 2025
)
. But performance has scaled only logarithmically with additional computation, forcing models to produce ever longer chains of thought—sometimes tens of thousands of tokens today and plausibly orders of magnitude more in the future
(
Wu et al., 2024
)
. With time as a fundamental limiting resource, a critical question is how to use a fixed wall-clock budget to achieve the highest performance possible.
A promising approach is the canonical test-time scaling method
Best-of-N
(BoN) sampling, which generates
N
N
candidates and selects the best using a learned verifier, reward model, or majority vote
(
Cobbe et al., 2021
;
Zheng et al., 2023
;
Kwon et al., 2023
;
Lightman et al., 2023b
;
Wang et al., 2023b
)
. While appealing in theory due to its parallelism, BoN is not adaptive: every trajectory is carried to completion regardless of promise. On easy tasks this wastes computation, and on hard tasks it inflates latency, since wall-clock time is governed by the longest generation and both length and total compute grow with
N
N
(
Leviathan et al., 2023
)
. What is missing is a way for models to anticipate which samples are worth continuing and which should be paused or abandoned, so that parallel effort is concentrated on trajectories most likely to succeed and fastest to complete.
Early-stopping and pruning methods aim to reduce BoN’s inefficiency by terminating unpromising samples mid-generation
(
Fu et al., 2025
;
Huang et al., 2025
)
. These approaches are valuable first steps toward adaptivity, but they typically rely on
scalar
signals—such as a confidence score from a classifier—or on simple heuristics. This creates two limitations. First, a scalar cannot capture the central reward–cost trade-off: a low-confidence trajectory may be worthwhile if nearly finished, while a high-confidence one may be impractical if it implies a long, costly continuation. Second, these methods do not quantify the marginal benefit of drawing more samples, which depends on the entire reward distribution rather than its expectation. As a result, such strategies can reduce compute in some cases but often fail to improve wall-clock time, falling short of the broader goal of enabling models to allocate compute adaptively—expending more effort on difficult queries and less on easy ones
(
Manvi et al., 2024
;
Graves, 2016
)
.
We introduce ZIP-RC, which addresses these limitations by training language models to provide zero-overhead introspective predictions of the
joint distribution
over reward and cost. At each decoding step, unused vocabulary logits parameterize a joint distribution over final reward and remaining generation length (see
fig.
1
). Access to the full joint—not just a scalar—enables order-statistic calculations that quantify the marginal utility of continuing partial samples or spawning additional samples. For example, when the predicted reward distribution has high variance, allocating more samples can substantially increase the expected maximum reward. We maximize a
sampling utility
that explicitly balances accuracy, compute, and latency through a linear combination of their expectations. The coefficients of the linear combination can be tuned to the desired balance of reward, compute, and latency. Optimizing this utility produces the behaviors observed in our experiments: when latency is prioritized, ZIP-RC spawns larger pools of samples and schedules early pruning to chase an early finisher; when compute is prioritized, it deprioritizes low-value trajectories aggressively and allocates more samples only when they are likely to pay off.
Experiments on mixed-difficulty mathematical benchmarks show that ZIP-RC improves accuracy by up to
12
%
12\%
over majority voting while using less average cost. By adjusting the utility coefficients, it traces smooth Pareto frontiers between accuracy, compute, and latency. We contribute ZIP and ZIP-RC which enable models to be introspective for more interpretable generations and maximize a sampling utility to improve performance with fixed compute and latency.
2
Related Work
Improving the efficiency and reliability of LLM reasoning requires both new methods for guiding generation and principled strategies for allocating computational resources at inference time. Our work builds on three key areas of research: the use of verifiers for response selection, process-level rewards for fine-grained feedback, and adaptive inference strategies for efficient computation.
Verifiers and reward models for output selection.
A common approach to enhancing LLM performance is to train an external verifier or reward model (RM) to assess the quality of complete responses. Such models provide outcome-based feedback, typically assigning a scalar score or probability of correctness to an entire output sequence. Outcome RMs have been widely used in reasoning and alignment works, from math problem solving to preference-based fine-tuning
(
Cobbe et al., 2021
;
Yu et al., 2023
;
Stiennon et al., 2020
)
. They can be integrated during training, as in reinforcement learning settings
(
Ouyang et al., 2022
;
Bai et al., 2022
)
, or applied at inference time through selection strategies such as Best-of-N sampling
(
Cobbe et al., 2021
;
Li et al., 2022
)
. Recent work has explored unifying the generator and verifier, using the model’s own logits for certain tokens as a proxy for a reward model
(
Ren et al., 2023
)
. Our work extends this introspective direction, moving beyond scalar correctness prediction to modeling a joint distribution over the expected future reward and computational cost at every token.
Process-based rewards for fine-grained feedback.
A limitation of outcome-supervision is its reliance on a sparse reward signal that makes credit assignment challenging, especially for long reasoning chains. Process-based reward models (PRMs) instead score intermediate steps via human annotation
(
Lightman et al., 2023b
)
, LLM-as-judge
(
Zheng et al., 2023
)
, or automated token-level value estimates. These automated estimates can be generated by propagating final outcome rewards back to individual tokens (Liu et al., 2024) or through other value estimation techniques
(
Uesato et al., 2022
;
Luo et al., 2024
)
. While most PRMs aim to improve the training signal, our goal is distinct: we use predictive feedback in real time to guide inference itself. Closest to the calibration side of this literature,
Damani et al. (2025)
augment a binary correctness reward with a confidence score to improve model calibration. Our approach is complementary: rather than training for calibrated confidence, we predict a joint distribution over future reward and future cost, turning process-level signals into a direct control knob for utility-aware inference.
Adaptive inference and introspective models.
Our work enables a form of adaptive inference, a long-standing goal in machine learning
(
Graves, 2016
;
Bengio et al., 2015
)
that has become increasingly critical for large models
(
Snell et al., 2024
)
. Adaptive methods that use multiple models or sequential sampling have been explored
(
Damani et al., 2024
;
Wang et al., 2024
)
. A more recent direction has involved parallel sampling that includes the pruning of unpromising generation paths. For instance, recent methods terminate samples based on mid-generation confidence scores
(
Manvi et al., 2024
;
Fu et al., 2025
)
or prune exploration based on step-wise consistency checks
(
Aggarwal et al., 2023
)
. We advance this line of work with a more general formulation: instead of relying on simple heuristics for pruning, we use our joint reward-cost predictions to explicitly optimize a utility function. This enables a richer set of meta-actions, such as dynamically resizing the sample pool and reallocating budget across trajectories. Conceptually, our approach parallels the integration of value functions with search in reinforcement learning
(
Silver et al., 2016
)
, where predictive signals guide exploration. It is also complementary to inference optimization techniques like speculative decoding
(
Leviathan et al., 2023
)
, which accelerate generation at the token level. By providing real-time estimates of success and cost, the predictions from ZIP-RC contribute to a broader vision of introspective models that report their internal states
(
Binder et al., 2024
;
Kadavath et al., 2022
)
, enhancing efficiency and interpretability.
3
Preliminaries
Generation as a token-level MDP.
We formalize text generation as a finite-horizon Markov Decision Process (MDP), following
Ramamurthy et al. (2022)
. The MDP is defined by the tuple
M
=
(
𝒮
,
𝒜
,
R
,
P
,
γ
,
H
)
M=(\mathcal{S},\mathcal{A},R,P,\gamma,H)
over a finite vocabulary
𝒱
\mathcal{V}
, where
𝒮
\mathcal{S}
is the state space, and
𝒜
\mathcal{A}
the action space,
R
R
the reward function,
P
P
the transition function,
γ
∈
[
0
,
1
]
\gamma\in[0,1]
the discount factor, and
H
H
the horizon. Given an input prompt
𝐱
=
(
x
0
,
…
,
x
m
)
\mathbf{x}=(x_{0},\ldots,x_{m})
consisting of tokens in the vocabulary
x
i
∈
𝒱
x_{i}\in\mathcal{V}
, the initial state is
s
0
=
𝐱
s_{0}=\mathbf{x}
. At timestep
t
t
, the LLM acts as a policy
π
⁡
(
a
t
|
s
t
)
\pi(a_{t}|s_{t})
that outputs the probability distribution over actions
a
t
∈
𝒱
a_{t}\in\mathcal{V}
. The transition function
P
P
deterministically appends
a
t
a_{t}
to state
s
t
s_{t}
, yielding next state
s
t
+
1
=
(
x
0
,
…
,
x
m
,
a
0
,
…
,
a
t
)
s_{t+1}=(x_{0},\ldots,x_{m},a_{0},\ldots,a_{t})
. The episode terminates when the model emits an end-of-sequence token
<EOS>
or the length of the generated sequence reaches the horizon
H
H
. Upon termination at timestep
T
T
, the environment returns a terminal reward
R
⁡
(
s
T
)
R(s_{T})
. The discount factor is defined as
γ
=
1
\gamma=1
and the value of any state
s
t
s_{t}
under policy
π
\pi
is the expected terminal reward from that state onward
V
⁡
(
s
t
)
=
𝔼
π
​
[
R
⁡
(
s
T
)
∣
s
t
]
V(s_{t})=\mathbb{E}_{\pi}\left[R(s_{T})\mid s_{t}\right]
where
s
T
s_{T}
is a random variable.
Best-of-
𝐍
\mathbf{N}
.
Best-of-
N
N
(BoN) is an inference-time selection mechanism that decouples generation from evaluation to improve output quality. Given a prompt
𝐱
\mathbf{x}
and a generator policy
π
\pi
, the method draws
N
N
independent and identically distributed (i.i.d.) terminated states
s
T
(
1
)
,
…
,
s
T
(
N
)
s_{T}^{(1)},\dots,s_{T}^{(N)}
from the policy. A learned verifier
V
^
:
𝒱
∗
→
ℝ
\hat{V}:\mathcal{V}^{*}\to\mathbb{R}
, typically a reward model, then assigns a scalar score to each terminated state. The final output is the state with the highest score, selected as
s
T
∗
∈
arg
⁡
max
i
∈
[
N
]
​
V
^
​
(
s
T
(
i
)
)
.
s_{T}^{*}\in\arg\max_{i\in[N]}\hat{V}(s_{T}^{(i)})\,.
(1)
The selection depends only on the relative ordering of scores from
V
^
​
(
⋅
)
\hat{V}(\cdot)
, ties are broken arbitrarily.
4
Zero-Overhead Introspective Prediction of Reward & Cost
We introduce Zero-overhead Introspective Prediction (ZIP), a method for extracting auxiliary signals during inference without extra models, architectural changes, or forward passes. ZIP repurposes the logits of a small set of reserved tokens to parameterize these auxiliary predictions within the same forward pass that generates the next-token probabilities. We then instantiate ZIP for reward and cost prediction (ZIP-RC).
Zero-overhead introspective prediction (ZIP).
Let
𝒱
\mathcal{V}
be the vocabulary and
ℛ
⊂
𝒱
\mathcal{R}\subset\mathcal{V}
a fixed contiguous set of
reserved tokens
.
At decoding step
t
t
, the model produces logits
z
t
∈
ℝ
|
𝒱
|
z_{t}\in\mathbb{R}^{|\mathcal{V}|}
. ZIP interprets logits over
ℛ
\mathcal{R}
as parameters of an auxiliary predictor (e.g. via a softmax). A rough visualization of this is shown in the top right of
fig.
1
. Before sampling, these logits are masked to remove probability mass:
π
θ
​
(
a
t
∣
s
t
)
=
{
exp
⁡
(
z
t
​
[
a
t
]
)
∑
v
∈
𝒱
∖
ℛ
exp
⁡
(
z
t
​
[
v
]
)
,
a
t
∈
𝒱
∖
ℛ
,
0
,
a
t
∈
ℛ
.
\pi_{\theta}(a_{t}\mid s_{t})=\begin{cases}\dfrac{\exp(z_{t}[a_{t}])}{\sum_{v\in\mathcal{V}\setminus\mathcal{R}}\exp(z_{t}[v])},&a_{t}\in\mathcal{V}\setminus\mathcal{R},\\[10.0pt]
0,&a_{t}\in\mathcal{R}.\end{cases}
(2)
Thus, each forward pass yields both (i) the decoding distribution on
𝒱
∖
ℛ
\mathcal{V}\setminus\mathcal{R}
and (ii) auxiliary predictions from
z
t
​
[
ℛ
]
z_{t}[\mathcal{R}]
, incurring zero additional cost at inference time.
During training, we supervise the auxiliary head via a task-specific loss
ℒ
aux
\mathcal{L}_{\text{aux}}
applied to
z
t
​
[
ℛ
]
z_{t}[\mathcal{R}]
(e.g., cross-entropy for categorical targets, Bernoulli NLL for binary targets, MSE for continuous targets), while regularizing the policy toward a frozen copy of the original policy
π
\pi
:
ℒ
(
s
t
)
=
ℒ
aux
(
s
t
)
+
α
KL
KL
(
π
(
⋅
∣
s
t
)
∥
π
θ
(
⋅
∣
s
t
)
)
.
\mathcal{L}(s_{t})=\mathcal{L}_{\text{aux}}(s_{t})+\alpha_{\mathrm{KL}}\;\mathrm{KL}\!\left(\pi(\cdot\mid s_{t})\;\middle\|\;\pi_{\theta}(\cdot\mid s_{t})\right).
(3)
ZIP is agnostic to the prediction target or loss, it simply standardizes how auxiliary predictions are produced during inference, with zero inference overhead. An alternative that keeps the model frozen is discussed in
section
A.3
.
ZIP-RC: joint reward-cost distribution prediction.
We use ZIP to predict a
joint distribution
over the (expected) reward and remaining length of a rollout using
π
\pi
starting from any prefix
s
t
s_{t}
. We can define the random variables
Z
π
​
(
s
t
)
=
V
⁡
(
s
T
)
=
𝔼
⁡
[
R
⁡
(
s
T
)
]
,
L
π
​
(
s
t
)
=
|
s
T
|
−
|
s
t
|
,
Z^{\pi}(s_{t})=V(s_{T})=\mathbb{E}\left[R(s_{T})\right],\qquad L^{\pi}(s_{t})=|s_{T}|-|s_{t}|\,,
(4)
that denote the expected terminal reward and the remaining length. In practice, we approximate
V
⁡
(
s
T
)
V(s_{T})
with a realized
V
^
​
(
s
T
)
\hat{V}(s_{T})
from a learned verifier.
We discretize the range of values into
B
V
B_{V}
bins with boundaries
{
v
b
}
b
=
1
B
V
+
1
\{v_{b}\}_{b=1}^{B_{V}+1}
and lengths into
B
T
B_{T}
bins with boundaries
{
t
ℓ
}
ℓ
=
1
B
T
+
1
\{t_{\ell}\}_{\ell=1}^{B_{T}+1}
, assigning one reserved token per
(
b
,
ℓ
)
(b,\ell)
using index in the
output vocabulary
𝒱
\mathcal{V}
given by
i
b
,
ℓ
=
i
ℛ
+
(
b
−
1
)
​
B
T
+
(
ℓ
−
1
)
i_{b,\ell}=i_{\mathcal{R}}+(b-1)B_{T}+(\ell-1)
, where
i
ℛ
i_{\mathcal{R}}
is the index of the
first reserved token. Let
z
t
aux
​
(
b
,
ℓ
)
≡
z
t
​
[
r
b
,
ℓ
]
z_{t}^{\text{aux}}(b,\ell)\equiv z_{t}[r_{b,\ell}]
. The joint distribution is
p
θ
​
(
b
,
ℓ
∣
s
t
)
=
exp
⁡
(
z
t
aux
​
(
b
,
ℓ
)
)
∑
b
′
=
1
B
V
∑
ℓ
′
=
1
B
T
exp
⁡
(
z
t
aux
​
(
b
′
,
ℓ
′
)
)
.
p_{\theta}(b,\ell\mid s_{t})=\frac{\exp(z_{t}^{\text{aux}}(b,\ell))}{\sum_{b^{\prime}=1}^{B_{V}}\sum_{\ell^{\prime}=1}^{B_{T}}\exp(z_{t}^{\text{aux}}(b^{\prime},\ell^{\prime}))}.
(5)
A rough visual representation of the grid mapping and examples of this learned distribution is shown in
fig.
1
. Given a completed trajectory
s
T
s_{T}
, for each timestep we construct training targets for each prefix
s
t
s_{t}
by computing
(
b
∗
,
ℓ
∗
)
(b^{*},\ell^{*})
such that
V
^
​
(
s
T
)
∈
[
v
b
∗
,
v
b
∗
+
1
)
,
|
s
T
|
−
|
s
t
|
∈
[
t
ℓ
∗
,
t
ℓ
∗
+
1
)
.
\hat{V}(s_{T})\in[v_{b^{*}},\,v_{b^{*}+1}),\qquad|s_{T}|-|s_{t}|\in[t_{\ell^{*}},\,t_{\ell^{*}+1}).
(6)
Finally, we train with cross-entropy
ℒ
aux
​
(
s
t
)
=
−
log
⁡
p
θ
​
(
b
∗
,
ℓ
∗
∣
s
t
)
\mathcal{L}_{\text{aux}}(s_{t})=-\log p_{\theta}(b^{*},\ell^{*}\mid s_{t})
,
together with the policy-preserving KL above. Other practical implementation details are discussed in
section
A.1
.
Why expected reward instead of realized reward?
It may initially seem unnatural to use an estimated value
V
^
​
(
s
T
)
\hat{V}(s_{T})
by a trained critic rather than the realized reward.
To explain this choice, let
s
T
(
1
)
,
…
,
s
T
(
N
)
∼
i.i.d.
π
θ
(
⋅
∣
s
0
)
s_{T}^{(1)},\dots,s_{T}^{(N)}\stackrel{{\scriptstyle\text{i.i.d.}}}{{\sim}}\pi_{\theta}(\cdot\mid s_{0})
be completions for a prompt, and
V
^
\hat{V}
the estimated value function used in BoN selection. The chosen index
s
T
∗
=
arg
⁡
max
i
​
V
^
​
(
s
T
(
i
)
)
s_{T}^{*}=\arg\max_{i}\hat{V}(s_{T}^{(i)})
yields score
V
^
​
(
s
T
∗
)
=
max
i
∈
[
N
]
⁡
V
^
​
(
s
T
(
i
)
)
\hat{V}(s_{T}^{*})=\max_{i\in[N]}\hat{V}(s_{T}^{(i)})
.
Modeling the distribution of possible terminal values
V
π
​
(
s
T
)
V^{\pi}(s_{T})
via
V
^
​
(
s
T
)
\hat{V}(s_{T})
rather than possible terminal rewards
R
⁡
(
s
T
)
R(s_{T})
: (i) aligns with the actual selection objective, and (ii) admits closed-form order-statistic expectations since noisy environment rewards from
R
⁡
(
s
T
)
R(s_{T})
cannot be assumed to be independent but its expectation
V
⁡
(
s
T
)
V(s_{T})
can.
ZIP-RC for sample selection and interpretability.
Using the learned joint distribution, we can also compute individual marginal distributions:
q
θ
V
​
(
b
∣
s
t
)
=
∑
ℓ
=
1
B
T
p
θ
​
(
b
,
ℓ
∣
s
t
)
,
q
θ
L
​
(
ℓ
∣
s
t
)
=
∑
b
=
1
B
V
p
θ
​
(
b
,
ℓ
∣
s
t
)
,
q_{\theta}^{V}(b\mid s_{t})=\sum_{\ell=1}^{B_{T}}p_{\theta}(b,\ell\mid s_{t}),\qquad q_{\theta}^{L}(\ell\mid s_{t})=\sum_{b=1}^{B_{V}}p_{\theta}(b,\ell\mid s_{t}),
(7)
which can be used to estimate the value and the expected remaining tokens to completion
V
π
​
(
s
t
)
=
𝔼
⁡
[
Z
π
​
(
s
t
)
]
≈
∑
b
=
1
B
V
v
b
+
v
b
+
1
2
​
q
θ
V
​
(
b
∣
s
t
)
,
𝔼
⁡
[
L
π
​
(
s
t
)
]
≈
∑
ℓ
=
1
B
T
t
ℓ
+
t
ℓ
+
1
2
​
q
θ
L
​
(
ℓ
∣
s
t
)
.
V^{\pi}(s_{t})=\mathbb{E}\!\left[Z^{\pi}(s_{t})\right]\approx\sum_{b=1}^{B_{V}}\frac{v_{b}+v_{b+1}}{2}\;q_{\theta}^{V}(b\mid s_{t}),\qquad\mathbb{E}\!\left[L^{\pi}(s_{t})\right]\approx\sum_{\ell=1}^{B_{T}}\frac{t_{\ell}+t_{\ell+1}}{2}\;q_{\theta}^{L}(\ell\mid s_{t}).
(8)
Here, the value estimation can be used for final sample selection and both the value and the expected remaining tokens to completion act as confidence and “thinking time” signals. A rough visualization of the interpretable signals is shown in the top right of
fig.
1
.
5
Test-time Compute using ZIP-RC (ZIP-RC sampling)
While large language models are post-trained to maximize the likelihood of high-reward generations, they remain imperfect policies due to finite data and compute. Low-reward completions are often sampled even when their deficiencies are apparent—either implicitly through low likelihood or explicitly via external reward models. Even greedy decoding (temperature 0) does not guarantee high-likelihood or high-reward outputs. Thus, one-shot sampling is insufficient for reliably accomplishing tasks. Test-time methods such as majority voting, BoN, Weighted BoN, and Pass@k show the alternative: by actively searching across multiple trajectories, they substantially outperform single-sample decoding. The performance gap highlights that the gain comes from active
search
.
Existing test-time methods, however, are heuristic and often inefficient. BoN can, in principle, explore as much as all other approaches with a large enough
N
N
, but this is impractical given compute and latency constraints. While more sophisticated search strategies like beam search try to explore more efficiently by allowing for intermediate branching and pruning at intervals, one could imagine removing constraints on search further. Though the goal of test-time search is clear—maximize task success while minimizing generation cost—prior methods do not achieve this in a principled way. Our goal is to propose a method that does. In this section, we introduce
ZIP-RC sampling
, which leverages predictions from ZIP-RC to explicitly optimize generations for both success and cost.
5.1
Search as Decision-Making Under a Meta-MDP.
We first formalize the problem of test-time search as decision-making under a high-level MDP that we dub a
meta-MDP
. We describe the components of the meta-MDP in detail below:
Meta-states.
At timestep
t
t
, the meta-state is a prefix tree (trie)
S
t
S_{t}
rooted at the prompt
𝐱
\mathbf{x}
. Formally,
S
t
=
(
𝒩
t
,
ℰ
t
,
r
)
S_{t}=(\mathcal{N}_{t},\mathcal{E}_{t},r)
where
ℰ
t
⊆
𝒩
t
×
𝒱
×
𝒩
t
\mathcal{E}_{t}\subseteq\mathcal{N}_{t}\times\mathcal{V}\times\mathcal{N}_{t}
is the set of directed edges
(
s
,
a
,
s
′
)
(s,a,s^{\prime})
labeled by tokens
a
∈
𝒱
a\in\mathcal{V}
,
r
r
is the root corresponding to the prompt, and each node
s
∈
𝒩
t
s\in\mathcal{N}_{t}
represents the prefix given by the concatenation of the root and the token labels along the path from
r
r
to
s
s
. Each node also corresponds to a state in the base MDP as it is a sequence of tokens that the base policy has generated. A prefix is finished if its last edge is the special token
<EOS>
, corresponding to the terminal state in the base MDP. Initially,
S
0
=
(
{
r
}
,
∅
,
r
)
S_{0}=(\{r\},\emptyset,r)
where
r
r
is the root containing the prompt. Conceptually, the meta-state therefore encodes all prefixes processed or generated by the policy. In practice, the trie only requires space on the order of the total tokens generated to represent all sequences, and their corresponding prefixes can be stored in the KV cache.
Meta-actions.
At step
t
t
, the meta-action selects a finite multiset of prefixes (nodes)
A
t
⊆
𝕄
⁡
(
𝒩
t
)
A_{t}\subseteq\mathbb{M}(\mathcal{N}_{t})
to continue sampling from. Multiplicity encodes branching: if prefix
s
s
appears
r
r
times in
A
t
A_{t}
, then
s
s
is sampled from
r
r
times independently. This definition encodes any viable single-token sampling and any strategy one might want to perform. If
s
∈
A
t
−
1
s\in A_{t-1}
but none of its children appear in
A
t
A_{t}
, this is equivalent to pausing or pruning. If
s
∈
A
t
s\in A_{t}
already has children, this is equivalent to backtracking.
Meta-transition function.
Given
(
S
t
,
A
t
)
(S_{t},A_{t})
, for each occurrence of
s
∈
A
t
s\in A_{t}
we sample
a
∼
π
(
⋅
∣
s
)
a\sim\pi(\cdot\mid s)
and add the edge
(
s
,
a
,
s
′
)
(s,a,s^{\prime})
and its child
s
′
s^{\prime}
to the trie, yielding
S
t
+
1
S_{t+1}
. For notational simplicity, we treat
π
\pi
as part of the transition dynamics of the meta-MDP so the transition function
P
⁡
(
S
t
+
1
∣
S
t
,
A
t
)
P(S_{t+1}\mid S_{t},A_{t})
implicitly includes sampling from
π
\pi
. The process terminates at horizon
T
T
, corresponding to the maximum allowed search steps.
Meta-reward function.
At each step we incur a cost
C
⁡
(
S
t
,
A
t
)
=
β
⁡
(
α
​
|
supp
⁡
(
A
t
)
|
+
(
1
−
α
)
)
C(S_{t},A_{t})=\beta\big(\alpha\,|\mathrm{supp}(A_{t})|+(1-\alpha)\big)
,
where
supp
⁡
(
A
t
)
\mathrm{supp}(A_{t})
is the set of distinct prefixes chosen in
A
t
A_{t}
(one forward pass per unique prefix) and the second term accounts for step latency. The parameter
α
∈
[
0
,
1
]
\alpha\in[0,1]
balances compute versus latency, and
β
>
0
\beta>0
sets the trade-off between reward and cost. At the terminal timestep
T
T
, one completed generation
s
T
∗
s_{T}^{*}
is selected, and the reward is the base MDP reward
R
⁡
(
s
T
∗
)
R(s_{T}^{*})
. Including this cost term is essential, since otherwise one could trivially maximize reward by always branching.
Search strategies as meta-policies.
A strategy
μ
\mu
is a policy in this meta-MDP: at each timestep it maps the current prefix tree
S
t
S_{t}
to a multiset
A
t
=
μ
⁡
(
S
t
)
A_{t}=\mu(S_{t})
of nodes to expand, and at horizon
T
T
selects a finished
f
∗
f^{*}
. BoN corresponds to placing
N
N
copies of the root in
A
0
A_{0}
and thereafter always expanding every unfinished leaf until completion, finally selecting the highest-scoring candidate. Beam search with width
B
B
instead enforces
|
A
t
|
=
B
|A_{t}|=B
at all times: at most steps
A
t
A_{t}
is just the
B
B
current leaves, but at pruning intervals of length
k
k
it ranks leaves by a score, discards the weakest
p
p
, and duplicates stronger ones so that the frontier is refilled back to
B
B
, thereby pruning and branching in a controlled manner before ultimately selecting the best finished prefix at
T
T
.
5.2
Computing an Optimal Zero-overhead Search Strategy
It is clear from our formalism what an optimal search strategy should be: at every timestep
t
t
, the optimal strategy
μ
∗
\mu^{*}
should choose the meta-action that maximizes:
μ
∗
​
(
S
t
)
=
arg
⁡
max
A
t
​
Q
μ
∗
​
(
S
t
,
A
t
)
,
\mu^{*}(S_{t})=\arg\max_{A_{t}}Q^{\mu^{*}}(S_{t},A_{t}),
(9)
where we define a
meta
Q-function over the meta-MDP for a strategy
μ
\mu
as,
Q
μ
(
S
t
,
A
t
)
=
𝔼
μ
[
R
(
s
T
∗
)
−
∑
t
′
=
t
T
−
1
C
(
S
t
′
,
A
t
′
)
∣
S
t
,
A
t
]
.
Q^{\mu}(S_{t},A_{t})=\mathbb{E}_{\mu}\!\left[R(s_{T}^{*})-\sum_{t^{\prime}=t}^{T-1}C(S_{t^{\prime}},A_{t^{\prime}})\mid S_{t},A_{t}\right].
(10)
However, computing
Q
μ
Q^{\mu}
for arbitrary strategies
μ
\mu
is often intractable, primarily because we cannot generate on-policy trajectories from
μ
\mu
without incurring too much computational overhead.
The sampling utility.
To avoid having to generate rollouts, we consider a class of
predefined
strategies at any timestep
t
t
as follows:
M
t
=
{
μ
:
μ
(
⋅
∣
S
t
′
)
=
f
(
{
π
(
⋅
∣
s
t
)
}
s
t
∈
𝒩
t
)
,
∀
t
′
≥
t
}
,
M_{t}=\left\{\mu:\mu(\cdot\mid S_{t^{\prime}})=f\left(\{\pi(\cdot\mid s_{t})\}_{s_{t}\in\mathcal{N}_{t}}\right)\,,\ \forall t^{\prime}\geq t\right\}\,,
(11)
where
f
f
denotes any function of the set of next-token distributions for every prefix in the meta-state. Concretely,
M
t
M_{t}
consists of all strategies where future meta-actions are determined entirely from generation behavior at timestep
t
t
. This essentially means for
μ
∈
M
t
\mu\in M_{t}
, we can compute its value
Q
μ
Q^{\mu}
without explicitly executing
μ
\mu
over future timesteps.
For any meta-state and meta-action at timestep
t
t
, we define the
sampling utility
to be the value of some strategy in the aforementioned class of strategies
M
t
M_{t}
. Because each strategy performs worse than optimal strategy
μ
∗
\mu^{*}
due to the imposed constraint, we choose the best-performing strategy in
M
t
M_{t}
to act as the tightest possible lower-bound
𝒰
⁡
(
S
t
,
A
t
)
=
max
μ
∈
M
t
⁡
Q
μ
​
(
S
t
,
A
t
)
≤
Q
μ
∗
​
(
S
t
,
A
t
)
.
\mathcal{U}(S_{t},A_{t})\;=\;\max_{\mu\in M_{t}}Q^{\mu}(S_{t},A_{t})\;\leq\;Q^{\mu^{*}}(S_{t},A_{t})\,.
(12)
We show later how this maximization over
M
t
M_{t}
, as well as computation of
Q
μ
Q^{\mu}
for
μ
∈
M
t
\mu\in M_{t}
, can be done tractably using the quantities obtained via ZIP-RC,
without any additional forward passes, auxiliary models, or architectural modifications
beyond standard decoding.
Finally, ZIP-RC sampling is defined as the strategy that maximizes our proposed sampling utility:
μ
ZIP-RC
​
(
S
t
)
=
arg
⁡
max
A
t
⁡
𝒰
⁡
(
S
t
,
A
t
)
.
\mu^{\text{ZIP-RC}}(S_{t})\;=\;\arg\max_{A_{t}}\ \mathcal{U}(S_{t},A_{t})\,.
(13)
Intuitively, we can derive the following property of our learned strategy:
Theorem 5.1
.
At every timestep
t
t
, our strategy
μ
ZIP-RC
\mu^{\text{ZIP-RC}}
performs better than any predefined strategy
μ
∈
M
t
\mu\in M_{t}
. Namely, for any meta-state
S
t
S_{t}
, we have
Q
ZIP-RC
​
(
S
t
,
μ
ZIP-RC
​
(
S
t
)
)
≥
Q
μ
​
(
S
t
,
μ
⁡
(
S
t
)
)
,
∀
μ
∈
M
t
.
Q^{\text{ZIP-RC}}(S_{t},\mu^{\text{ZIP-RC}}(S_{t}))\;\geq\;Q^{\mu}(S_{t},\mu(S_{t}))\,,\ \forall\mu\in M_{t}\,.
(14)
Proof.
We can prove this via induction on
t
t
. Naively, this holds for terminal timestep
t
=
T
t=T
. For any
μ
∈
M
t
\mu\in M_{t}
, we let
A
t
ZIP-RC
=
μ
ZIP-RC
​
(
S
t
)
A_{t}^{\text{ZIP-RC}}=\mu^{\text{ZIP-RC}}(S_{t})
and
A
t
μ
=
μ
⁡
(
S
t
)
A_{t}^{\mu}=\mu(S_{t})
. Then, we have
Q
ZIP-RC
​
(
S
t
,
A
t
ZIP-RC
)
\displaystyle Q^{\text{ZIP-RC}}(S_{t},A_{t}^{\text{ZIP-RC}})
=
Q
ZIP-RC
​
(
S
t
+
1
,
A
t
+
1
ZIP-RC
)
−
C
⁡
(
S
t
,
A
t
ZIP-RC
)
.
\displaystyle=Q^{\text{ZIP-RC}}(S_{t+1},A_{t+1}^{\text{ZIP-RC}})-C(S_{t},A_{t}^{\text{ZIP-RC}})\,.
(15)
∎
Therefore, ZIP-RC sampling is a powerful test-time search strategy that explicitly optimizes for reward and generation cost by adaptively reallocating compute at each step.
Approximating the sampling utility.
To approximate the sampling utility, we aim to answer two questions: (1) for every meta-state
S
t
S_{t}
and action
A
t
A_{t}
, how do we search for a strategy
μ
∈
M
t
\mu\in M_{t}
that achieves a high value
Q
μ
​
(
S
t
,
A
t
)
Q^{\mu}(S_{t},A_{t})
, and (2) how do we compute
Q
μ
​
(
S
t
,
A
t
)
Q^{\mu}(S_{t},A_{t})
tractably using only predictions by ZIP-RC.
First, let us consider the naive strategy
μ
Rollouts
\mu^{\mathrm{Rollouts}}
of always selecting the unfinished leaf-node descendants of the prefixes in the current action
A
t
A_{t}
, or in other words, obtaining
rollouts
or generations using
π
\pi
starting from each selected prefix. At the end,
μ
Rollouts
\mu^{\mathrm{Rollouts}}
selects the generation with the highest value
V
π
​
(
s
T
)
V^{\pi}(s_{T})
, similar to BoN. Its meta-MDP state-action value is exactly given by:
Q
Rollouts
​
(
S
t
,
A
t
)
\displaystyle Q^{\mathrm{Rollouts}}(S_{t},A_{t})
=
𝔼
μ
Rollouts
[
R
(
s
T
∗
)
−
∑
t
′
=
t
T
−
1
C
(
S
t
′
,
A
t
′
)
∣
S
t
,
A
t
]
\displaystyle=\mathbb{E}_{\mu^{\mathrm{Rollouts}}}\!\left[R(s_{T}^{*})-\sum_{t^{\prime}=t}^{T-1}C(S_{t^{\prime}},A_{t^{\prime}})\mid S_{t},A_{t}\right]
(16)
=
𝔼
⁡
[
max
s
∈
A
t
⁡
Z
π
​
(
s
)
−
β
⁡
(
α
​
∑
s
∈
A
t
L
π
​
(
s
)
+
(
1
−
α
)
​
max
s
∈
A
t
​
L
π
​
(
s
)
)
]
\displaystyle=\mathbb{E}\!\left[\max_{s\in A_{t}}Z^{\pi}(s)-\beta\!\left(\alpha\sum_{s\in A_{t}}L^{\pi}(s)+(1-\alpha)\max_{s\in A_{t}}L^{\pi}(s)\right)\right]
=
𝔼
⁡
[
max
s
∈
A
t
⁡
Z
π
​
(
s
)
]
−
β
⁡
(
α
​
∑
s
∈
A
t
𝔼
⁡
[
L
π
​
(
s
)
]
+
(
1
−
α
)
​
𝔼
​
[
max
s
∈
A
t
⁡
L
π
​
(
s
)
]
)
.
\displaystyle=\mathbb{E}\!\left[\max_{s\in A_{t}}Z^{\pi}(s)\right]-\beta\!\left(\alpha\,\sum_{s\in A_{t}}\mathbb{E}\!\left[L^{\pi}(s)\right]+(1-\alpha)\,\mathbb{E}\!\left[\max_{s\in A_{t}}L^{\pi}(s)\right]\right).
(17)
We can observe that the expression
Q
Rollouts
Q^{\mathrm{Rollouts}}
contains several interpretable quantities. Namely, the expected maximum value quantifies the marginal benefit of branching or pruning; the incremental gain from increasing
N
N
is large when the value distribution has high variance, and conversely, the marginal loss of pruning is small under low variance.
Furthermore, the expected maximum remaining tokens and the expected total tokens capture the marginal cost of branching; increasing
N
N
always increases the expected total remaining tokens and the maximum remaining length, which drives up latency, and pruning will always reduce the cost.
While
μ
Rollouts
\mu^{\mathrm{Rollouts}}
has several nice properties, the strategy itself is naive as it assigns maximum cost for every new sample and does not consider that those samples can be pruned in the future.
This is exacerbated further by the empirical correlation between the length of reasoning traces and the likelihood that they are incorrect. Being able to “bet” on an early finishing sample that has high reward is crucial.
To remedy this problem, we introduce an additional parameter into the meta-value that enables the
μ
Rollouts
\mu^{\mathrm{Rollouts}}
strategy to prune each sample in the future at a predefined horizon.
Formally, let
Q
Rollouts
​
(
S
t
,
A
t
,
ℋ
t
)
Q^{\mathrm{Rollouts}}(S_{t},A_{t};\mathcal{H}_{t})
be the value of executing
μ
Rollouts
\mu^{\mathrm{Rollouts}}
, with the additional capability that each active prefix
s
∈
A
t
s\in A_{t}
will stop generating upon reaching length
h
s
∈
ℋ
t
h_{s}\in\mathcal{H}_{t}
, where
ℋ
t
\mathcal{H}_{t}
is a set of lengths of size
|
A
t
|
|A_{t}|
.
We can now define an improved lower bound by maximizing over
ℋ
t
\mathcal{H}_{t}
:
Q
Rollouts
​
(
S
t
,
A
t
,
ℋ
t
∗
)
=
max
ℋ
t
⁡
Q
Rollouts
​
(
S
t
,
A
t
,
ℋ
t
)
≥
Q
Rollouts
​
(
S
t
,
A
t
)
,
Q^{\mathrm{Rollouts}}(S_{t},A_{t};\mathcal{H}_{t}^{*})=\max_{\mathcal{H}_{t}}Q^{\mathrm{Rollouts}}(S_{t},A_{t};\mathcal{H}_{t})\;\geq\;Q^{\mathrm{Rollouts}}(S_{t},A_{t})\,,
(18)
where it is easy to see that the our new meta-value is monotonically better than the value of the naive
μ
Rollouts
\mu^{\mathrm{Rollouts}}
strategy without pruning capabilities.
We use this to approximate the sampling utility:
𝒰
⁡
(
S
t
,
A
t
)
=
Q
Rollouts
​
(
S
t
,
A
t
,
ℋ
t
∗
)
.
\mathcal{U}(S_{t},A_{t})\;=\;Q^{\mathrm{Rollouts}}(S_{t},A_{t};\mathcal{H}_{t}^{*})\,.
(19)
Tractable computation of expectations.
Next, we show how our sampling utility in Equation
19
can be computed tractably using only predictions by ZIP-RC.
Predicting
Q
Rollouts
Q^{\mathrm{Rollouts}}
is straightforward since we can estimate distributions over the value
q
θ
V
(
⋅
|
s
t
)
q_{\theta}^{V}(\cdot|s_{t})
and remaining-tokens
q
θ
L
(
⋅
|
s
t
)
q_{\theta}^{L}(\cdot|s_{t})
conditioned on each prefix
s
t
s_{t}
using our previously proposed ZIP-RC. Hence, we can estimate by computing:
𝔼
⁡
[
max
s
∈
A
t
⁡
Z
π
​
(
s
)
]
\displaystyle\mathbb{E}\!\left[\max_{s\in A_{t}}Z^{\pi}(s)\right]
≈
∑
b
=
1
B
V
v
b
+
v
b
+
1
2
​
(
F
θ
V
,
max
​
(
b
∣
A
t
)
−
F
θ
V
,
max
​
(
b
−
1
∣
A
t
)
)
,
\displaystyle\approx\sum_{b=1}^{B_{V}}\frac{v_{b}+v_{b+1}}{2}\big(F_{\theta}^{V,\max}(b\mid A_{t})-F_{\theta}^{V,\max}(b-1\mid A_{t})\big),
(20)
𝔼
​
[
L
π
​
(
s
)
]
\displaystyle\mathbb{E}\!\left[L^{\pi}(s)\right]
≈
∑
ℓ
=
1
B
T
t
ℓ
+
t
ℓ
+
1
2
​
q
θ
L
​
(
ℓ
∣
s
)
,
\displaystyle\approx\sum_{\ell=1}^{B_{T}}\frac{t_{\ell}+t_{\ell+1}}{2}\,q_{\theta}^{L}(\ell\mid s),
(21)
𝔼
⁡
[
max
s
∈
A
t
⁡
L
π
​
(
s
)
]
\displaystyle\mathbb{E}\!\left[\max_{s\in A_{t}}L^{\pi}(s)\right]
≈
∑
ℓ
=
1
B
T
t
ℓ
+
t
ℓ
+
1
2
​
(
F
θ
L
,
max
​
(
ℓ
∣
A
t
)
−
F
θ
L
,
max
​
(
ℓ
−
1
|
A
t
)
)
,
\displaystyle\approx\sum_{\ell=1}^{B_{T}}\frac{t_{\ell}+t_{\ell+1}}{2}\big(F_{\theta}^{L,\max}(\ell\mid A_{t})-F_{\theta}^{L,\max}(\ell-1|A_{t})\big),
(22)
where
F
θ
V
,
max
​
(
b
∣
A
t
)
\displaystyle F_{\theta}^{V,\max}(b\mid A_{t})
=
∏
s
∈
A
t
F
θ
V
​
(
b
∣
s
)
,
\displaystyle=\prod_{s\in A_{t}}F^{V}_{\theta}(b\mid s),
F
θ
L
,
max
​
(
ℓ
∣
A
t
)
\displaystyle F_{\theta}^{L,\max}(\ell\mid A_{t})
=
∏
s
∈
A
t
F
θ
L
​
(
ℓ
∣
s
)
,
\displaystyle=\prod_{s\in A_{t}}F_{\theta}^{L}(\ell\mid s),
(23)
F
θ
V
​
(
b
∣
s
)
\displaystyle F_{\theta}^{V}(b\mid s)
=
∑
j
≤
b
q
θ
V
​
(
j
∣
s
)
,
\displaystyle=\sum_{j\leq b}q_{\theta}^{V}(j\mid s),
F
θ
L
​
(
ℓ
∣
s
)
\displaystyle F_{\theta}^{L}(\ell\mid s)
=
∑
j
≤
ℓ
q
θ
L
​
(
j
∣
s
)
.
\displaystyle=\sum_{j\leq\ell}q_{\theta}^{L}(j\mid s).
(24)
Now, to incorporate the predefined horizons
ℋ
t
\mathcal{H}_{t}
over all prefixes
A
t
A_{t}
, we modify the joint distribution
p
θ
​
(
b
,
ℓ
|
s
)
p_{\theta}(b,\ell|s)
to a
capped
joint
p
θ
(
b
,
ℓ
|
s
;
h
s
)
p_{\theta}(b,\ell|s;h_{s})
that collapses probability mass beyond the cap
h
s
h_{s}
into a designated “clipped” state
(
b
0
,
h
s
)
(b_{0},h_{s})
:
p
θ
(
b
,
ℓ
∣
s
;
h
s
)
=
{
p
θ
​
(
b
,
ℓ
∣
s
)
,
ℓ
≤
h
s
,
𝟏
​
{
b
=
b
0
,
ℓ
=
h
s
}
​
∑
b
′
∑
ℓ
′
>
h
s
p
θ
​
(
b
′
,
ℓ
′
∣
s
)
,
ℓ
>
h
s
.
p_{\theta}(b,\ell\mid s;h_{s})=\begin{cases}p_{\theta}(b,\ell\mid s),&\ell\leq h_{s},\\[6.0pt]
\mathbf{1}\{b=b_{0},\,\ell=h_{s}\}\displaystyle\sum_{b^{\prime}}\sum_{\ell^{\prime}>h_{s}}p_{\theta}(b^{\prime},\ell^{\prime}\mid s),&\ell>h_{s}~.\end{cases}
(25)
This construction ensures that all probability mass corresponding to continuations exceeding the allowed horizon is reassigned to a truncated state at
ℓ
=
h
s
\ell=h_{s}
, while the value component is collapsed to the designated base bin
b
0
b_{0}
to reflect the forfeited reward from pruning.
From the capped joints, we can recover the corresponding marginal distributions:
q
θ
V
​
(
b
∣
s
;
h
s
)
\displaystyle q_{\theta}^{V}(b\mid s;h_{s})
=
∑
ℓ
=
1
B
T
p
θ
(
b
,
ℓ
∣
s
;
h
s
)
,
\displaystyle=\sum_{\ell=1}^{B_{T}}p_{\theta}(b,\ell\mid s;h_{s}),
q
θ
L
​
(
ℓ
∣
s
;
h
s
)
\displaystyle q_{\theta}^{L}(\ell\mid s;h_{s})
=
∑
b
=
1
B
V
p
θ
(
b
,
ℓ
∣
s
;
h
s
)
.
\displaystyle=\sum_{b=1}^{B_{V}}p_{\theta}(b,\ell\mid s;h_{s}).
(26)
These capped marginals directly encode the expected effect of planned pruning on both value and remaining length for each prefix. Notice that this is only possible by modeling the joint distribution as ZIP-RC is defined and is not possible with only the two marginal distributions. Thus, we demonstrate that we are able to compute our sampling utility in Equation
19
using only our zero-overhead predictions from ZIP-RC.
Summary.
ZIP-RC sampling defines a meta-policy that, at each meta-state
S
t
S_{t}
, selects the meta-action
A
t
A_{t}
—a multiset of prefixes to expand for one decoding step—that maximizes the
sampling utility
in
eq.
19
. This utility is the state–action value of the best policy in the predefined strategy class
M
t
M_{t}
, whose future behavior is fixed. Because ZIP-RC sampling re-optimizes
A
t
A_{t}
at every timestep, it adapts online to the stochastic evolution of the prefix tree: if current trajectories are projected to be costly or low-value, it can immediately redirect computation elsewhere. As formalized in
eq.
14
, this dynamic strategy is guaranteed to perform at least as well as any predefined policy in
M
t
M_{t}
.
To approximate the sampling utility tractably, we use the value of the best rollouts-with-pruning strategy
Q
Rollouts
​
(
S
t
,
A
t
,
ℋ
t
∗
)
Q^{\mathrm{Rollouts}}(S_{t},A_{t};\mathcal{H}_{t}^{*})
, in which each prefix may continue only up to an optimized (and possibly distinct) horizon. This value can be computed in closed form using ZIP-RC’s joint reward–cost predictions. Concretely, for every prefix
s
∈
A
t
s\in A_{t}
, we: (i) obtain its predicted joint distribution
p
θ
​
(
b
,
ℓ
∣
s
)
p_{\theta}(b,\ell\mid s)
; (ii) apply the prefix-specific horizon using the capped construction in
eq.
26
; and (iii) compute the expectations of the required order statistics using
eq.
22
. This yields a fully tractable, zero-overhead estimate of the sampling utility for any candidate meta-action.
Practical considerations.
Prompts differ widely in their typical reasoning-trace lengths, so the cost coefficient
β
\beta
may be normalized per prompt using the procedure in
section
A.2
to ensure stable reward–cost tradeoffs. Because the full meta-action space is large and joint optimization over per-prefix horizons is combinatorial, we use several practical reductions—restricting candidate prefixes, prioritizing high-value/low-length nodes, and employing a shared horizon—as detailed in
section
A.2
. Finally, ZIP-RC predictions incur zero additional
model
compute; ZIP-RC sampling adds only lightweight CPU-side computation to evaluate the sampling utility.
6
Experiments
Our experiments aim to test the following hypotheses:
(1)
ZIP-RC can accurately predict the joint reward-cost distribution.
(2)
ZIP-RC sampling can be tuned to balance between output quality, and compute cost and latency, tracing a Pareto frontier over the quantities over strong inference baselines.
(3)
ZIP-RC sampling is adaptive and generalizes across tasks of varying difficulty and across models of varying size.
We will describe and present results that provide positive evidence for each hypothesis individually.
Figure 2:
Predictions and ground truth for the initial joint distributions of 10 questions randomly sampled from the AMC 2023 benchmark and 10 questions from the AIME 2024 benchmark. The ground truth for each prompt was estimated with 256 rollouts from Qwen3-1.7B, and predictions were made using ZIP-RC trained with the same model. This shows that the joint distribution from ZIP-RC is calibrated and relatively accurate in forecasting the outcomes of its own rollouts.
Beginning (Reward+Cost)
End (Reward)
Model
Total Variation
F1 Score
Accuracy
Recall (Incorrect)
Qwen3-1.7B
0.46
0.91
0.88
0.82
LFM2-1.2B
0.45
0.91
0.87
0.69
LFM2-350M
0.48
0.80
0.82
0.87
Table 1:
Prediction accuracy of ZIP-RC at the beginning and end of generation. At the beginning, no ground-truth reward or remaining-length label exists due to stochastic decoding, so we evaluate the joint reward-cost prediction using Total Variation. At the end of generation, the ground-truth reward is known, allowing us to report F1 score, accuracy, and incorrect-answer recall using a threshold of 0.5.
Figure 3:
Performance of ZIP-RC sampling and baselines across all models and benchmarks. The top half demonstrates the latency bound setting where
α
=
0.1
\alpha=0.1
, and the bottom half demonstrates the compute bound setting where
α
=
1.0
\alpha=1.0
. Adjusting
β
\beta
in ZIP-RC sampling allows it to trade generation cost for higher performance (similar to increasing
N
N
in BoN) while adjusting
α
\alpha
allows it to adjust the prioritization of compute and latency. By navigating the Pareto frontier and allocating generation cost adaptively, ZIP-RC sampling significantly outperforms majority voting and other baselines.
Model
Method
Gen. Cost
AIME2024
AMC2023
MATH-500
GSM8K
Mixed
Qwen3-1.7B
ZIP-RC sampling
1.43
65.8
90.9
94.1
92.2
92.2
Majority Voting
1.40
53.1
87.9
93.0
91.2
91.0
MV length-prune
1.46
25.1
58.5
84.7
91.6
88.0
Weighted BoN ext. RM
1.43
54.7
86.5
92.6
91.4
91.0
Weighted BoN Self-eval
1.40
59.4
89.1
93.6
91.6
91.6
ZIP-RC reward prune
1.33
43.3
86.0
90.3
89.6
88.9
LFM2-1.2B
ZIP-RC sampling
1.35
60.9
93.5
93.4
83.6
86.0
Majority Voting
1.60
49.6
90.6
91.8
81.4
83.8
MV length-prune
1.70
51.3
89.8
91.6
83.0
84.9
Weighted BoN ext. RM
1.53
50.3
89.0
91.1
79.8
82.5
Weighted BoN Self-eval
1.60
55.1
91.8
92.6
82.5
84.9
ZIP-RC reward prune
1.49
57.5
90.2
92.5
83.8
85.8
LFM2-350M
ZIP-RC sampling
1.49
38.8
83.9
86.1
70.1
74.1
Majority Voting
1.70
26.9
74.5
82.7
64.4
68.8
MV length-prune
1.66
28.3
74.8
83.6
66.5
70.6
Weighted BoN ext. RM
1.59
28.5
73.4
81.9
63.2
67.8
Weighted BoN Self-eval
1.70
31.4
77.6
84.4
66.8
71.1
ZIP-RC reward prune
1.27
21.7
69.7
83.2
63.0
67.8
Table 2:
Performance and generation cost at
α
=
0.1
\alpha=0.1
under matched-cost configurations. ZIP-RC sampling uses
β
=
0.01
\beta=0.01
and a maximum of eight samples. MV uses three samples; MV length-prune uses four; Weighted Bo
N
N
Self-eval (GenRM) uses three; Weighted Bo
N
N
with external RM uses two; and ZIP-RC reward prune uses a
0.4
0.4
threshold with eight samples.
6.1
Experimental Setup
Models.
We use three open models spanning capability and scale:
Qwen3-1.7B
(Alibaba) in reasoning mode
(
Yang et al., 2025
)
;
LFM2-1.2B Math
(Liquid AI), a compact mathematical-reasoning model
(
LiquidAI, 2025
)
; and
LFM2-350M Math
, a smaller variant targeting efficient math reasoning. Unless stated otherwise, decoding is identical across methods; ZIP-RC modifies only the sampling policy at inference time.
Training data for ZIP-RC and baselines.
We construct a mathematical training corpus by combining DeepScaleR
(
Luo et al., 2025
)
, the MATH training split
(
Hendrycks et al., 2021
)
, and the GSM8K training split
(
Cobbe et al., 2021
)
. For each prompt, we generate two on-policy rollouts per model, yielding roughly 100k rollouts in total. We then label each rollout for correctness against the ground-truth answer. These labeled rollouts are used to train model-specific ZIP-RC predictors as well as any learned baselines.
Baselines.
We evaluate against the following baselines that consist of popular sampling strategies that fall under the parallel sampling paradigm where multiple candidate samples are generated in parallel and there is some selection method. Other notable paradigms include beam search or self-refinement. However, we use parallel sampling methods, which are the most commonly used and reported as they do not suffer from collapsing diversity issues that arise from branching and generating with similar prefixes or the ballooning latency issues from methods that generate samples sequentially. We use stronger adaptations of Best-of-
N
N
(Bo
N
N
), and an ablation of ZIP-RC that performs pruning without the sampling utility optimization and instead uses the expected reward directly.:
(1)
Majority Voting (MV)
(self-consistency), which selects the most frequent final answer, breaking ties uniformly at random
(
Wang et al., 2023a
)
. This is an extremely common method since it does not require any learned verifier.
(2)
MV with length-based pruning
, which discards very long, potentially looping samples (cut at 8k tokens). This baseline acts as a sanity check to see if our latency gains only come from preventing looping samples from generating to the maximum 32k generation length.
(3)
Weighted Bo
N
N
with external RM
, which scores each sample with a separate reward model trained on the same math corpus; because the RM reprocesses the full sequence without KV cache, FLOPs roughly double relative to generation alone
(
Li et al., 2023
)
. This baseline demonstrates strong performance that goes beyond Best-of-N sampling.
(4)
Weighted Bo
N
N
with self-evaluation (GenRM)
, which replaces the external RM with trained self-evaluations derived from the generator
(
Manvi et al., 2024
;
Zhang et al., 2025
;
Mahan et al., 2024
)
. We specifically include this baseline as it is another method that uses less compute than external reward models for selection.
(5)
ZIP-RC with reward-based pruning
, which starts with a fixed pool and prunes any trajectory whose predicted expected reward falls below a threshold using ZIP-RC’s real-time signal. This acts as a natural and strong ablation to our sampling utility optimization as it directly prunes weak samples that have less promise than those with high expected reward.
Benchmarks.
We report performance on
AIME 2024
,
AMC 2023
,
MATH-500
(
Lightman et al., 2023a
)
, and
GSM8K
. We additionally evaluate on a
Concatenated Mixed-Difficulty Benchmark
formed by concatenating the above, which probes adaptive allocation across difficulties.
Metrics.
First and foremost we measure accuracy on each benchmark as it is an obvious and good measure for performance and high-quality responses. Beyond performance, we measure efficiency and latency.
Normalized compute
reports total FLOPs per prompt normalized by the FLOPs of a single-sample generation for that prompt. We compute FLOPs with the standard
2
​
N
2N
rule (proportional to the sum of input and generated tokens) and account for KV caching where applicable.
Normalized best-case latency
measures the lower bound on wall-clock time as the maximum number of sequential forward passes across the candidate set; with unconstrained data-parallel sampling, latency is governed by the longest trajectory.
Generation cost
aggregates these via a linear combination,
GenCost
=
α
⋅
NormCompute
+
(
1
−
α
)
⋅
NormLatency
\text{GenCost}=\alpha\cdot\text{NormCompute}+(1-\alpha)\cdot\text{NormLatency}
. Unless otherwise specified, we use
α
=
0.1
\alpha=0.1
, which roughly balances compute and latency in typical parallel regimes (e.g., eight parallel samples often behave like two to three serial generations in practice). For ZIP-RC sampling we sweep
β
\beta
, which trades off expected quality against cost in the utility; when reporting matched-cost comparisons we set
β
=
0.005
\beta=0.005
and cap the pool at
8
8
samples for fair comparison to other baselines.
6.2
Accuracy of ZIP-RC’s real-time predictions
ZIP provides auxiliary predictions with zero overhead, but for this to be useful they must be reliable. We first visually validate whether the joint reward-cost distribution predictions from ZIP-RC are reasonable. To do so, we first obtain ground truth estimates of the joint distributions at the start of generation on AMC 2023 + AIME 2024, which exhibit nontrivial error rates and diverse reasoning trace lengths. The ground truth estimates are derived with 256 rollouts from Qwen3-1.7B and the predictions are made using ZIP-RC trained with the same model. From the 10 random examples from each benchmark in
fig.
2
we can see that the predictions are calibrated and relatively accurate in forecasting the distribution of outcomes.
To quantitatively validate the accuracy of the predictions, we measure the total variation at the beginning of generation using the same ground truth joint distribution estimates, as well as standard classification metrics for reward prediction using a threshold of
0.5
0.5
. As seen in
table
1
, the total variations from the ground truth confirm the visual validation that the predicted distributions are relatively close to the ground truth, and the reward prediction at the end of generation further confirms this; it demonstrates high accuracy in terms of F1 Score, accuracy, and recall for incorrect answers (using a threshold of 0.5). Overall, these results indicate that ZIP-RC and ZIP predictions can be calibrated and accurate despite being done in the same forward pass as next-token prediction.
6.3
Tracing the quality–compute–latency frontier
We next test whether maximizing the sampling utility with specific cost coefficients achieves controllable tradeoffs. At each decision point, ZIP-RC evaluates meta-actions that serve three complementary purposes. First, initiating new samples only when necessary and avoiding continuing to generate low-value trajectories saves compute, which is reflected in the compute bound setting in the bottom half of
fig.
3
(
α
=
1.0
\alpha=1.0
), where ZIP-RC achieves compute savings. Second, penalizing the continued sampling of long outliers avoids samples that would dominate latency. Third, expanding the initial pool of samples while planning to use a near-term maximum horizon enables the search to pursue early finishers without paying the full wall-clock cost of long runs. These mechanisms together drive the latency savings observed in the top half of
fig.
3
(
α
=
0.0
\alpha=0.0
). In both settings
β
\beta
is successfully used similar to
N
N
in BoN in order to increase performance for more generation cost. Parameters
α
\alpha
and
β
\beta
together thus provide simple control knobs over compute–latency emphasis and quality–cost trade-off.
Across both
α
\alpha
regimes, ZIP-RC sampling traces smooth Pareto frontiers that strictly dominate MV across benchmarks and scales validating that a single utility can jointly improve quality, compute, and latency. When
α
=
0.1
\alpha=0.1
(latency-emphasis), it substantially reduces cost, with the largest relative reduction observed on LFM2-350M (up to roughly 40%). Because we cap at eight samples, the frontier saturates once pass@8 performance is reached for a given
β
\beta
.
6.4
Adaptive inference with ZIP-RC sampling
Finally, we compare ZIP-RC sampling against all baselines at matched generation cost with
α
=
0.1
\alpha=0.1
in
table
2
. Two patterns emerge: (i) at fixed cost, ZIP-RC improves accuracy relative to MV and weighted Bo
N
N
baselines; (ii) it allocates more samples to harder instances (AIME/AMC) and to weaker models, while pruning aggressively on easier problems or stronger models.
At matched cost, ZIP-RC sampling improves accuracy over MV and weighted Bo
N
N
on all models and benchmarks. On harder subsets such as AIME 2024, gains reach up to 12% absolute while using less average cost. The adaptive policy naturally uses more samples when the predicted reward distribution is high-variance—where the expected benefit of best-of-
N
N
is greatest—and conserves compute when one trajectory is expected to be dominant. This pattern is evident on the mixed-difficulty benchmark (left-most column in
fig.
3
) and across model scales: weaker models and harder tasks receive more samples, leading to higher overall accuracy.
Takeaways.
ZIP-RC’s real-time predictions are accurate and reliable enough to enable principled search during decoding. This yields (i) reliable mid-generation detection of weak or overlong trajectories, (ii) smooth and tunable Pareto frontiers between quality, compute, and latency, and (iii) adaptive allocation that consistently outperforms fixed-budget Best-of-
N
N
at the same or lower cost.
7
Conclusion
We introduced ZIP-RC, a zero-overhead framework for introspective inference that predicts future reward and cost by repurposing existing logits. This enables principled, real-time decoding search during inference, yielding up to
12
%
12\%
absolute accuracy gains over strong Best-of-N baselines at a lower average cost, while tracing a smooth Pareto frontier between quality, compute, and latency. These findings open natural extensions, such as applying it to diverse domains and testing fully dynamic resource allocation across different models and reasoning modes. Ultimately, ZIP-RC marks a conceptual shift from rigid, heuristic-based scaling to principled, utility-aware inference. By empowering models to anticipate their success and computational cost, our work is a key step toward more autonomous, reliable, and efficient LLMs. A limitation of our method is that we rely on LLMs achieving sufficient diversity of samples during inference; namely, if we double the number of initial samples, but the new samples are not sufficiently different, then our method and any similar test-time compute method like BoN is unable to achieve higher performance.
We believe an important direction of future work is investigating how to improve diversity of samples during inference, potentially by using a mixture of prompts or even models.
Overall, we believe ZIP-RC establishes a strong foundation for the next generation of introspective models and provides a timely, impactful contribution to adaptive test-time scaling.
References
Aggarwal
et al.
(2023)
P. Aggarwal, A. Madaan, Y. Yang,
et al.
Let’s sample step by step: adaptive-consistency for efficient reasoning and coding with llms
.
arXiv preprint arXiv:2305.11860
.
Cited by:
§2
.
Bai
et al.
(2022)
Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli, T. Henighan,
et al.
Training a helpful and harmless assistant with reinforcement learning from human feedback
.
arXiv preprint arXiv:2204.05862
.
Cited by:
§2
.
Bengio
et al.
(2015)
E. Bengio, P. Bacon, J. Pineau, and D. Precup
Conditional computation in neural networks for faster models
.
arXiv preprint arXiv:1511.06297
.
Cited by:
§2
.
Binder
et al.
(2024)
F. J. Binder, J. Chua, T. Korbak, H. Sleight, J. Hughes, R. Long, E. Perez, M. Turpin, and O. Evans
Looking inward: language models can learn about themselves by introspection
.
arXiv preprint arXiv:2410.13787
.
Cited by:
§2
.
Brown
et al.
(2020)
T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell,
et al.
Language models are few-shot learners
.
Advances in neural information processing systems
33
,
pp. 1877–1901
.
Cited by:
§1
.
Cobbe
et al.
(2021)
K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano,
et al.
Training verifiers to solve math word problems
.
arXiv preprint arXiv:2110.14168
.
Cited by:
§1
,
§2
,
§6.1
.
Damani
et al.
(2025)
M. Damani, I. Puri, S. Slocum, I. Shenfeld, L. Choshen, Y. Kim, and J. Andreas
Beyond binary rewards: training lms to reason about their uncertainty
.
arXiv preprint arXiv:2507.16806
.
Cited by:
§2
.
Damani
et al.
(2024)
M. Damani, I. Shenfeld, A. Peng, A. Bobu, and J. Andreas
Learning how hard to think: input-adaptive allocation of lm computation
.
External Links:
2410.04707
,
Link
Cited by:
§2
.
Fu
et al.
(2025)
Y. Fu, X. Wang, Y. Tian, and J. Zhao
Deep think with confidence
.
arXiv preprint arXiv:2508.15260
.
Cited by:
§1
,
§2
.
Graves (2016)
A. Graves
Adaptive computation time for recurrent neural networks
.
arXiv preprint arXiv:1603.08983
.
Cited by:
§1
,
§2
.
Guo
et al.
(2025)
D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi,
et al.
Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning
.
arXiv preprint arXiv:2501.12948
.
Cited by:
§1
.
Hendrycks
et al.
(2021)
D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
Measuring mathematical problem solving with the math dataset
.
NeurIPS
.
Cited by:
§6.1
.
Huang
et al.
(2025)
C. Huang, L. Huang, J. Leng, J. Liu, and J. Huang
Efficient test-time scaling via self-calibration
.
arXiv preprint arXiv:2503.00031
.
Cited by:
§1
.
Jaech
et al.
(2024)
A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney,
et al.
Openai o1 system card
.
arXiv preprint arXiv:2412.16720
.
Cited by:
§1
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson,
et al.
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Cited by:
§2
.
Kojima
et al.
(2022)
T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa
Large language models are zero-shot reasoners
.
Advances in neural information processing systems
35
,
pp. 22199–22213
.
Cited by:
§1
.
Kwon
et al.
(2023)
M. Kwon, S. M. Xie, K. Bullard, and D. Sadigh
Reward design with language models
.
arXiv preprint arXiv:2303.00001
.
Cited by:
§1
.
Leviathan
et al.
(2023)
Y. Leviathan, M. Kalman, and Y. Matias
Fast inference from transformers via speculative decoding
.
In
International Conference on Machine Learning
,
pp. 19274–19286
.
Cited by:
§1
,
§2
.
Li
et al.
(2023)
Y. Li, Z. Lin, S. Zhang, Q. Fu, B. Chen, J. Lou, and W. Chen
Making large language models better reasoners with step-aware verifier
.
External Links:
2206.02336
,
Link
Cited by:
item (3)
.
Li
et al.
(2022)
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago,
et al.
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
§2
.
Lightman
et al.
(2023a)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
Let’s verify step by step
.
arXiv preprint arXiv:2305.20050
.
Cited by:
§6.1
.
Lightman
et al.
(2023b)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
Let’s verify step by step
.
In
The Twelfth International Conference on Learning Representations
,
Cited by:
§1
,
§2
.
LiquidAI (2025)
LiquidAI
Introducing lfm2: the fastest on-device foundation models on the market
.
External Links:
Link
Cited by:
§6.1
.
Luo
et al.
(2024)
L. Luo, Y. Liu, R. Liu, S. Phatale, M. Guo, H. Lara, Y. Li, L. Shu, Y. Zhu, L. Meng,
et al.
Improve mathematical reasoning in language models by automated process supervision
.
arXiv preprint arXiv:2406.06592
.
Cited by:
§2
.
Luo
et al.
(2025)
M. Luo, S. Tan, J. Wong, X. Shi, W. Y. Tang, M. Roongta, C. Cai, J. Luo, L. E. Li, R. A. Popa, and I. Stoica
DeepScaleR: surpassing o1-preview with a 1.5b model by scaling rl
.
Note:
https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2
Notion Blog
Cited by:
§6.1
.
Mahan
et al.
(2024)
D. Mahan, D. V. Phung, R. Rafailov, C. Blagden, N. Lile, L. Castricato, J. Fränken, C. Finn, and A. Albalak
Generative reward models
.
External Links:
2410.12832
,
Link
Cited by:
item (4)
.
Manvi
et al.
(2024)
R. Manvi, A. Singh, and S. Ermon
Adaptive inference-time compute: llms can predict if they can do better, even mid-generation
.
arXiv preprint arXiv:2410.02725
.
Cited by:
§1
,
§2
,
item (4)
.
Ouyang
et al.
(2022)
L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray,
et al.
Training language models to follow instructions with human feedback
.
Advances in neural information processing systems
35
,
pp. 27730–27744
.
Cited by:
§2
.
Ramamurthy
et al.
(2022)
R. Ramamurthy, P. Ammanabrolu, K. Brantley, J. Hessel, R. Sifa, C. Bauckhage, H. Hajishirzi, and Y. Choi
Is reinforcement learning (not) for natural language processing: benchmarks, baselines, and building blocks for natural language policy optimization
.
arXiv preprint arXiv:2210.01241
.
Cited by:
§3
.
Ren
et al.
(2023)
J. Ren, Y. Zhao, T. Vu, P. J. Liu, and B. Lakshminarayanan
Self-evaluation improves selective generation in large language models
.
In
Proceedings on
,
pp. 49–64
.
Cited by:
§2
.
Silver
et al.
(2016)
D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. Van Den Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam, M. Lanctot,
et al.
Mastering the game of go with deep neural networks and tree search
.
nature
529
(
7587
),
pp. 484–489
.
Cited by:
§2
.
Snell
et al.
(2024)
C. Snell, J. Lee, K. Xu, and A. Kumar
Scaling llm test-time compute optimally can be more effective than scaling model parameters
.
arXiv preprint arXiv:2408.03314
.
Cited by:
§1
,
§2
.
Stiennon
et al.
(2020)
N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss, A. Radford, D. Amodei, and P. F. Christiano
Learning to summarize with human feedback
.
Advances in neural information processing systems
33
,
pp. 3008–3021
.
Cited by:
§2
.
Uesato
et al.
(2022)
J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang, A. Creswell, G. Irving, and I. Higgins
Solving math word problems with process-and outcome-based feedback
.
arXiv preprint arXiv:2211.14275
.
Cited by:
§2
.
Wang
et al.
(2024)
X. Wang, S. Feng, Y. Li, P. Yuan, Y. Zhang, B. Pan, H. Wang, Y. Hu, and K. Li
Make every penny count: difficulty-adaptive self-consistency for cost-efficient reasoning
.
In
North American Chapter of the Association for Computational Linguistics
,
External Links:
Link
Cited by:
§2
.
Wang
et al.
(2023a)
X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou
Self-consistency improves chain of thought reasoning in language models
.
External Links:
2203.11171
,
Link
Cited by:
item (1)
.
Wang
et al.
(2023b)
X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou
Self-consistency improves chain of thought reasoning in language models
.
In
The Eleventh International Conference on Learning Representations
,
Cited by:
§1
,
§1
.
Wei
et al.
(2022)
J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou,
et al.
Chain-of-thought prompting elicits reasoning in large language models
.
Advances in neural information processing systems
35
,
pp. 24824–24837
.
Cited by:
§1
.
Wu
et al.
(2024)
Y. Wu, Z. Sun, S. Li, S. Welleck, and Y. Yang
Inference scaling laws: an empirical analysis of compute-optimal inference for problem-solving with language models
.
arXiv preprint arXiv:2408.00724
.
Cited by:
§1
.
Yang
et al.
(2025)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu
Qwen3 technical report
.
External Links:
2505.09388
,
Link
Cited by:
§6.1
.
Yao
et al.
(2023)
S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan
Tree of thoughts: deliberate problem solving with large language models
.
Advances in neural information processing systems
36
,
pp. 11809–11822
.
Cited by:
§1
.
Yu
et al.
(2023)
F. Yu, A. Gao, and B. Wang
Ovm, outcome-supervised value models for planning in mathematical reasoning
.
arXiv preprint arXiv:2311.09724
.
Cited by:
§2
.
Zhang
et al.
(2025)
L. Zhang, A. Hosseini, H. Bansal, M. Kazemi, A. Kumar, and R. Agarwal
Generative verifiers: reward modeling as next-token prediction
.
External Links:
2408.15240
,
Link
Cited by:
item (4)
.
Zheng
et al.
(2023)
L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing,
et al.
Judging llm-as-a-judge with mt-bench and chatbot arena
.
Advances in neural information processing systems
36
,
pp. 46595–46623
.
Cited by:
§1
,
§2
.
Appendix A
Appendix
A.1
ZIP-RC Implementation Details
Remaining-token discretization.
For the joint ZIP-RC head, we discretize the remaining-length variable
L
T
π
​
(
s
t
)
L_{T}^{\pi}(s_{t})
using logarithmic bins. Let
{
t
ℓ
}
ℓ
=
1
B
T
+
1
\{t_{\ell}\}_{\ell=1}^{B_{T}+1}
denote the bin boundaries, and define bin
ℓ
\ell
as
[
t
ℓ
,
t
ℓ
+
1
)
[t_{\ell},\,t_{\ell+1})
with representative value
(
t
ℓ
+
t
ℓ
+
1
)
/
2
(t_{\ell}+t_{\ell+1})/2
. To obtain fine resolution for short continuations while keeping
B
T
B_{T}
small, we collapse all very short lengths into a single initial “startup” bin and set the remaining boundaries to grow as powers of two. This construction preserves precision where it matters while limiting the number of reserved tokens required for ZIP-RC.
KL weight.
In practice, the KL term is a very small component of the total loss because the policy remains close to the original policy as seen in
fig.
4
. Accordingly, we use a relatively large coefficient
α
KL
\alpha_{\mathrm{KL}}
, typically in the range
10
10
–
100
100
.
Figure 4:
KL divergence from the original policy during training of ZIP-RC with and without the KL term. Using
α
KL
=
10
\alpha_{\mathrm{KL}}=10
keeps the KL nearly zero throughout training, stabilizing around
0.005
0.005
. Without the KL term, the policy eventually changes, emphasizing the importance and effectiveness of this component of the ZIP objective. We used the same training data as in our main experiments.
Temporal smoothing.
Token-level ZIP-RC predictions can be noisy. At inference time we optionally smooth the joint by averaging the last
W
W
predictions along the current trajectory: for a prefix
s
t
s_{t}
we set
p
¯
θ
​
(
b
,
ℓ
∣
s
t
)
=
1
W
​
∑
w
=
0
W
−
1
p
θ
​
(
b
,
ℓ
∣
s
t
−
w
)
,
\bar{p}_{\theta}(b,\ell\mid s_{t})=\frac{1}{W}\sum_{w=0}^{W-1}p_{\theta}(b,\ell\mid s_{t-w}),
(27)
where the sum runs over the previous non-terminal prefixes on the same path. We use
p
¯
θ
\bar{p}_{\theta}
in place of
p
θ
p_{\theta}
when computing the ZIP-RC marginals and the sampling utility.
A.2
ZIP-RC sampling Implementation Details
Normalization of cost term
β
\beta
.
Because rollout lengths can differ by orders of magnitude across prompts, we rescale the cost coefficient
β
\beta
by a per-prompt estimate of the typical total token count. At decision step
t
t
, we use the normalized coefficient
β
~
t
=
β
B
¯
t
,
where
B
¯
t
=
1
|
A
t
|
​
∑
s
∈
A
t
(
|
s
|
+
𝔼
⁡
[
L
T
π
​
(
s
)
]
)
.
\tilde{\beta}_{t}\;=\;\frac{\beta}{\bar{B}_{t}},\qquad\text{where}\qquad\bar{B}_{t}\;=\;\frac{1}{|A_{t}|}\sum_{s\in A_{t}}\big(|s|+\mathbb{E}[L_{T}^{\pi}(s)]\big).
(28)
Here
|
s
|
|s|
is the current length of prefix
s
s
, and
𝔼
​
[
L
T
π
​
(
s
)
]
\mathbb{E}[L_{T}^{\pi}(s)]
is its predicted remaining tokens from ZIP-RC. This keeps the reward–cost tradeoff stable across prompts with very short or very long generations.
Practical reduction of the search space.
The full meta-action space over multisets of nodes in the prefix tree is extremely large, and jointly optimizing per-prefix horizons is combinatorial. In our implementation we therefore operate within a structured subclass of meta-actions and horizons. First, at timestep
t
t
we restrict candidate meta-actions to multisets over the root and the unfinished leaves of
S
t
S_{t}
with multiplicity only allowed at the root, and further downselect to a small set of prefixes prioritized by higher predicted value and lower predicted remaining length under ZIP-RC. Second, when computing the sampling utility we use a single shared horizon
h
t
h_{t}
for all active prefixes, rather than independent horizons per prefix, reducing the search over pruning schedules to a one-dimensional search over
h
t
h_{t}
. Finally, instead of recomputing
μ
ZIP-RC
​
(
S
t
)
\mu^{\text{ZIP-RC}}(S_{t})
at every token, we update the meta-action only at fixed intervals and simply continue all currently active prefixes in between. These design choices substantially reduce the search space while preserving an expressive and adaptive family of strategies. This represents just one concrete instantiation of our framework; many other reductions are possible.
A.3
ZIP-RC-Lite
We add an ablation we refer to as ZIP-RC-Lite where we use the ZIP-RC objective described in
eq.
3
with the KL term removed, keeping only the output head of the language model trainable while freezing the rest of the model. As shown in
fig.
5
and
table
3
, we find that ZIP-RC-Lite is able to non-trivially predict the joint distribution but unsurprisingly struggles to do so as accurately as ZIP-RC. Its predictions are poorly calibrated and may not be suitable for interpretability of the generation process and output. Despite this, we find that ZIP-RC-Lite search provides substantial gains with respect to baselines in the latency-bound setting with
α
=
0.1
\alpha=0.1
, suggesting that predicting the expected reward and remaining length to any degree is useful for pruning overly long trajectories as seen in the first row of
fig.
6
. However, we do find that ZIP-RC-Lite substantially over-allocates compute in the compute-bound setting with
α
=
1.0
\alpha=1.0
due to overestimating the variance of the expected reward, resulting in poor efficiency as seen in the second row of
fig.
6
. Overall, while ZIP-RC is clearly more calibrated and accurate, ZIP-RC-Lite is a compelling alternative if one does not want to keep the whole model trainable.
Figure 5:
Similar to the demonstration of ZIP-RC’s joint distribution prediction in
fig.
2
, we visualize the joint distribution predictions from ZIP-RC-Lite and compare them with ground truth estimates. While the predictions correlate with the ground truth, ZIP-RC-Lite tends to produce more similar-looking distributions across prompts and overestimates variance compared to ZIP-RC.
Beginning (Reward+Cost)
End (Reward)
Method
Total Variation
F1 Score
Accuracy
Recall (Incorrect)
ZIP-RC
0.46
0.91
0.88
0.82
ZIP-RC-Lite
0.63
0.82
0.71
0.12
Table 3:
Similar to the evaluation of ZIP-RC in
table
1
, we show the prediction accuracy of ZIP-RC-Lite at the beginning and end of generation. The results indicate that ZIP-RC-Lite predicts the joint distribution non-trivially, but less accurately than ZIP-RC.
Figure 6:
Similar to the demonstration of ZIP-RC sampling in
fig.
3
, we present results with ZIP-RC-Lite search in green, indicating it is able to provide significant gains, albeit lower than ZIP-RC sampling, especially in the compute-bound setting. This suggests that predicting the joint reward-cost distribution to any non-trivial degree is helpful in allocating test-time compute more optimally. However, the results in the compute-bound setting indicate that ZIP-RC-Lite’s overestimation of variation in the expected reward distribution results in over-allocation of compute.