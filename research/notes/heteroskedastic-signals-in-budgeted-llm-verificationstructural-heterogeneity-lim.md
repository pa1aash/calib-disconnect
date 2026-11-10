---
title: Heteroskedastic Signals in Budgeted LLM Verification:Structural Heterogeneity
  Limits Optimization Gains
id: heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim
tags:
- code-llm-confidence-positioning-d82d00
- w3-forward-citation
created: '2026-11-10T08:23:50.050219Z'
updated: '2026-11-10T08:25:31.929461Z'
source: https://arxiv.org/html/2606.15841
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:50.049422Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Budgeted verification on MBPP (N=500, unit-test feedback) and MATH with
  Qwen3-8B, LLaMA3-8B, GPT-4o-mini: token-probability/logit-margin proxy quality is
  heteroskedastic across cost strata; compares Random, Threshold, MP-Adapt, MP-Strat,
  cost-stratified thresholding (CST), Oracle on hit rate; CST gains +3.4 to +17.0
  pp. Closest occupant of L3 confidence-routed execution budgets vs random and oracle
  routing, but with injected 10% label noise, logit-based proxy only (no verbal or
  probe confidence), small MBPP, and no calibration or contamination control.'
---

Heteroskedastic Signals in Budgeted LLM Verification:Structural Heterogeneity Limits Optimization Gains
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2606.15841v2 [cs.AI] 20 Jul 2026
﻿﻿﻿﻿
Heteroskedastic Signals in Budgeted LLM Verification:
Structural Heterogeneity Limits Optimization Gains
Jinlong Yang
Email:
aestalon.young@gmail.com
Abstract
Selective-compute LLM systems decide which outputs merit verification, additional reasoning, tool execution, or human audit under a limited budget. It is natural to expect that stronger online optimization over a shared uncertainty or reward signal should improve these decisions. We take a critical look at this assumption and ask: when does optimizing harder fail because the signal is not decision-comparable across inputs?
In budgeted LLM verification, we find that uncertainty quality is heteroskedastic across cost strata: some regions exhibit near-random discriminability while concentrating many errors. Under an explicit local model, we characterize the resulting distortion of global allocation and show that its upper bound scales with cross-stratum signal-quality dispersion.
To separate weak signals from optimizer instability and structural mismatch, we introduce a controlled intervention hierarchy: Threshold, MP-Adapt, MP-Strat, and cost-stratified thresholding (CST). We then turn the diagnosis into Heterogeneity-Gated Allocation (HGA), which uses a warm-up comparability test to choose between global and cost-stratified allocation. Across MBPP and MATH using Qwen3-8B, LLaMA3-8B, and GPT-4o-mini, global online adaptation yields inconsistent gains over static thresholding; CST improves hit rate by up to 17 percentage points in strongly heterogeneous settings, while HGA preserves most gains and avoids blind stratification when the partition is not useful.
These findings suggest a resource-allocation principle for LLM systems: before optimizing harder over a shared proxy, test whether the proxy is decision-comparable across observable operating regimes, and gate structural specialization on that test.
1
Introduction
Many LLM systems must decide where limited computation should be spent. Verification, test-time scaling, tool execution, model routing, and agent auditing all require policies that rank inputs by uncertainty, confidence, or reward proxies, often adapting from sparse feedback
(
Guo et al. 2017
;
Kadavath et al. 2022
;
Kuhn et al. 2023
;
Hazan 2016
)
. It is therefore tempting to treat selective compute as an optimization problem: given a proxy and a budget, learn a better global allocation rule.
This view hides a stronger assumption. A shared allocation rule is valid only if the same score carries comparable decision value across the inputs competing for budget. We call this the
global signal comparability assumption
. In practice, the assumption can fail: the same uncertainty score may be informative in one cost stratum but near-random in another. Then the bottleneck is not merely that the optimizer is weak; the objective being optimized is structurally conflated.
We study this failure mode through
budgeted LLM verification
, a setting where allocation decisions, costs, and outcomes are measurable. Outputs can be validated through unit tests, sandbox execution, theorem checking, or tool invocation, but limited budgets preclude verifying every candidate
(
Chen et al. 2021
;
Jimenez et al. 2024
)
. This gives a clean test of a broader AI decision question: does stronger global optimization solve selective compute, or is the shared proxy itself locally incomparable?
Figure 1:
Core mechanism and finding.
Left:
a globally shared threshold treats equal score-cost ratios as comparable, even when the proxy has different decision value across stable and weak-signal strata; stratified thresholds decouple these regimes.
Right:
at
β
=
20
%
\beta{=}20\%
, CST exposes when structure helps, while HGA retains positive stratification gains and falls back toward Threshold when fixed stratification is harmful.
To answer this question, we need to distinguish three explanations that look similar in aggregate: weak signals, unstable online optimization, and feedback-structure mismatch. We therefore test a controlled intervention hierarchy that progressively relaxes global sharing. Threshold is the static global reference; MP-Adapt tests stronger global optimization; MP-Strat reduces optimization noise through partial stratification; and CST removes learning while fully stratifying allocation. CST is deliberately weak: if it beats a stronger globally shared learner, the failure is unlikely to be solved by optimizer sophistication alone. We then convert this diagnostic into Heterogeneity-Gated Allocation (HGA): a warm-up comparability test decides whether to trust the global threshold or open a cost-stratified gate. Figure
1
summarizes this mechanism and the resulting empirical pattern.
Across MBPP and MATH with Qwen3-8B, LLaMA3-8B, and GPT-4o-mini, MP-Strat provides partial recovery (
+
2.8
+2.8
pp) by reducing optimization noise, while CST achieves the largest gains (
+
3.4
+3.4
–
+
17.0
+17.0
pp) through structural decoupling in aligned settings. HGA keeps the diagnostic nature of CST but avoids treating stratification as universal: it matches Threshold on Qwen3-MATH, where CST underperforms, while retaining most CST gains on MBPP.
We theoretically analyze this phenomenon under bounded score densities, a locally Lipschitz quantile functional, and an explicit local location model. We show that when signal reliability varies across cost strata, a single global quantile can induce a structural allocation distortion whose bound grows with cross-stratum signal-quality dispersion. This analysis explains why improving a globally shared optimizer need not remove the observed failure.
The main contributions are as follows:
•
We formalize global signal comparability as a hidden assumption in selective-compute decisions and identify its failure as a structural limitation of LLM resource allocation.
•
We develop a controlled diagnostic hierarchy (Threshold
→
\rightarrow
MP-Adapt
→
\rightarrow
MP-Strat
→
\rightarrow
CST) and HGA, a gated allocation rule that selects global or stratified allocation based on warm-up comparability evidence.
•
We bound global-allocation distortion by cross-stratum discriminability dispersion and show across MBPP, MATH, and three model families that structure-aware allocation helps only when feedback is not comparable, motivating gated rather than unconditional stratification.
2
Related Work
Uncertainty in large language models.
Uncertainty estimation in LLMs has been widely studied through token probabilities, logit margins, semantic consistency, and verbalized confidence
(
Guo et al. 2017
;
Kadavath et al. 2022
;
Kuhn et al. 2023
;
Farquhar et al. 2024
;
Huang et al. 2024
)
. Classical selective prediction
(
El-Yaniv and others 2010
;
Geifman and El-Yaniv 2017
)
and conformal prediction
(
Angelopoulos and Bates 2022
;
Cherian et al. 2024
)
offer principled frameworks for abstention with coverage guarantees. Modern instruction-tuned LLMs increasingly use uncertainty as a ranking signal for selective computation. Most existing approaches assume relatively stable uncertainty quality across inputs, enabling globally shared ranking policies. However, recent studies show that uncertainty quality can degrade substantially under distribution shift, task complexity, and instruction tuning
(
Huang et al. 2024
;
Tao et al. 2025
;
Xiong et al. 2024
)
, challenging the robustness of global ranking policies.
Resource allocation in LLM systems.
LLM inference is increasingly framed as a resource-allocation problem. Self-consistency
(
Wang et al. 2022
)
, best-of-N sampling, process-supervised verifiers, and test-time scaling
(
Cobbe et al. 2021
;
Snell et al. 2024
)
allocate computation using globally shared ranking or reward signals. Related routing and tool-use systems similarly decide where costly capabilities should be invoked. Signal reliability, however, varies with input complexity and latent task difficulty
(
Manvi et al. 2024
;
Damani et al. 2025
;
Zhao et al. 2025
)
. We isolate the allocation consequence of this heterogeneity: a shared proxy can be globally useful while still being locally incomparable for budgeted decisions.
Execution-based verification.
Execution-guided decoding, self-refinement, and verifier-based methods leverage runtime feedback to improve generation quality
(
Li et al. 2022
;
Lightman et al. 2024
;
Madaan et al. 2023
;
Ni et al. 2023
)
. While effective for refining individual outputs, these works largely overlook the question of
which
candidates to verify under limited computational budgets
(
Chen et al. 2021
;
Jimenez et al. 2024
)
. Given that execution costs are high and highly variable across samples, principled prioritization via uncertainty signals becomes critical.
Budgeted verification and adaptive allocation.
Budgeted LLM evaluation methods typically rely on uncertainty signals for global ranking or adaptive thresholding under fixed compute constraints
(
Fang et al. 2026
;
Fan et al. 2026
)
, or route queries across models to reduce cost
(
Chen et al. 2023
;
Ong et al. 2024
)
. These approaches assume uniform uncertainty quality across inputs. In practice, however, signal quality often degrades markedly on complex instances
(
Huang et al. 2024
;
Sharma and David 2025
;
Tao et al. 2025
)
.
Unlike prior work assuming uniform signal quality, we study the structural limitations induced by heterogeneous uncertainty through a controlled intervention hierarchy and cost-stratified verification policies. We draw connections to group-conditional selective prediction and per-group thresholding in the multicalibration literature
(
Hébert-Johnson et al. 2018
;
Detommaso et al. 2024
)
. Recent work has further extended these ideas to multi-group risk control with formal guarantees
(
Zhang et al. 2024
)
.
Constrained online decision making.
Our setting is also closely related to constrained and budgeted bandits, bandits with knapsack-style resource constraints
(
Badanidiyuru et al. 2018
;
Agrawal and Devanur 2014
)
, and online resource allocation
(
Badanidiyuru et al. 2014
;
Balseiro et al. 2020
)
. These literatures primarily ask how to optimize reward or regret while respecting scarce-resource constraints. We study a complementary mechanism-level failure mode: the proxy used to allocate the resource can have systematically different reliability across observable cost regimes, so a globally shared learner may optimize a structurally conflated objective. MP-Adapt is therefore not presented as a new bandit algorithm; it is an optimization-focused control used to test whether stronger global adaptation resolves this misspecification.
3
Problem Setup and Methods
Our goal is to diagnose when an allocation policy fails because its feedback structure is misaligned with the operating regimes it serves. We therefore express all policies within the same cost-aware decision framework and vary only the degree of sharing across strata. This design makes the comparison a mechanism test: if a weak structure-aligned policy outperforms a stronger globally shared learner, the bottleneck is not merely optimizer capacity.
3.1
Problem Formulation
Consider a set of
N
N
samples. Each sample
i
i
is associated with a binary error label
y
i
∈
{
0
,
1
}
y_{i}\in\{0,1\}
, a proxy signal vector
𝐡
i
∈
ℝ
d
\mathbf{h}_{i}\in\mathbb{R}^{d}
, and a verification cost
c
i
>
0
c_{i}>0
corresponding to executing slow feedback (e.g., unit tests).
At each step
t
t
, the policy observes proxy signal
𝐡
t
\mathbf{h}_{t}
and observable cost
c
^
t
\hat{c}_{t}
, and decides whether to trigger verification
a
t
∈
{
0
,
1
}
a_{t}\in\{0,1\}
. The system is subject to a budget constraint:
∑
t
=
1
N
a
t
⋅
c
t
≤
β
​
∑
t
=
1
N
c
t
,
\sum_{t=1}^{N}a_{t}\cdot c_{t}\leq\beta\sum_{t=1}^{N}c_{t},
where
β
∈
(
0
,
1
)
\beta\in(0,1)
is the fraction of full-verification cost available. Policies obey the same budget cap and are evaluated by hit rate:
HitRate
=
∑
t
a
t
⋅
y
t
∑
t
a
t
.
\mathrm{HitRate}=\frac{\sum_{t}a_{t}\cdot y_{t}}{\sum_{t}a_{t}}.
Because this ratio can favor under-utilization, we also report audit rates (Section
5.4
) and analyze discovered error mass through
V
⁡
(
π
)
V(\pi)
(Section
4
).
3.2
Unified Decision Framework and Proxy Signals
All policies are expressed via a cost-aware scoring rule:
a
t
=
(
s
θ
​
(
𝐡
t
)
>
λ
⋅
c
^
t
)
,
a_{t}=\mathbf{1}\!\left(s_{\theta}(\mathbf{h}_{t})>\lambda\cdot\hat{c}_{t}\right),
(1)
where
s
θ
​
(
⋅
)
s_{\theta}(\cdot)
maps proxy signals to scores and
λ
\lambda
controls budget pressure. Policies differ along two axes: whether the score is learned or fixed, and whether allocation is global or stratified.
All policies operate on the same token-level uncertainty proxies. Let
m
ℓ
=
log
⁡
P
⁡
(
x
ℓ
(
1
)
)
−
log
⁡
P
⁡
(
x
ℓ
(
2
)
)
m_{\ell}=\log P(x_{\ell}^{(1)})-\log P(x_{\ell}^{(2)})
denote the logit margin at position
ℓ
\ell
; we extract three complementary signals:
h
t
(
1
)
\displaystyle h_{t}^{(1)}
=
−
1
L
∑
ℓ
=
1
L
log
P
(
x
ℓ
∣
x
<
ℓ
)
,
\displaystyle=-\frac{1}{L}\sum_{\ell=1}^{L}\log P(x_{\ell}\mid x_{<\ell}),
h
t
(
2
)
\displaystyle h_{t}^{(2)}
=
−
min
ℓ
⁡
m
ℓ
,
\displaystyle=-\min_{\ell}m_{\ell},
h
t
(
3
)
\displaystyle h_{t}^{(3)}
=
1
L
​
∑
ℓ
=
1
L
exp
⁡
(
−
clip
⁡
(
m
ℓ
,
−
5
,
+
∞
)
)
.
\displaystyle=\frac{1}{L}\sum_{\ell=1}^{L}\exp\left(-\mathrm{clip}(m_{\ell},-5,+\infty)\right).
These capture average uncertainty (
h
t
(
1
)
h_{t}^{(1)}
), worst-case token confidence (
h
t
(
2
)
h_{t}^{(2)}
), and margin dispersion (
h
t
(
3
)
h_{t}^{(3)}
). The composite score is
s
θ
​
(
𝐡
t
)
=
𝜽
⊤
​
𝐡
t
s_{\theta}(\mathbf{h}_{t})=\boldsymbol{\theta}^{\top}\mathbf{h}_{t}
, where
𝐡
t
=
[
h
t
(
1
)
,
h
t
(
2
)
,
h
t
(
3
)
]
\mathbf{h}_{t}=[h_{t}^{(1)},h_{t}^{(2)},h_{t}^{(3)}]
.
3.3
Global Policies: The Limits of Shared Adaptation
We begin with globally shared policies, to isolate whether underperformance stems from insufficient learning or structural limitations of global adaptation.
Threshold.
Threshold is the static global reference: it uses a fixed scoring function
s
⁡
(
𝐡
t
)
=
𝐰
0
⊤
​
𝐡
t
s(\mathbf{h}_{t})=\mathbf{w}_{0}^{\top}\mathbf{h}_{t}
with a running quantile over signal-cost ratios:
a
t
\displaystyle a_{t}
=
(
s
⁡
(
𝐡
t
)
c
^
t
>
τ
t
)
,
\displaystyle=\mathbf{1}\!\left(\frac{s(\mathbf{h}_{t})}{\hat{c}_{t}}>\tau_{t}\right),
τ
t
\displaystyle\tau_{t}
=
Quantile
1
−
β
​
{
s
⁡
(
𝐡
k
)
c
^
k
}
k
<
t
.
\displaystyle=\mathrm{Quantile}_{1-\beta}\!\left\{\frac{s(\mathbf{h}_{k})}{\hat{c}_{k}}\right\}_{k<t}.
MP-Adapt: Global online learning.
MP-Adapt tests whether stronger global adaptation helps, using a mirror-prox learner
(
Nemirovski 2004
;
Fang et al. 2022
)
that jointly optimizes
𝜽
t
\boldsymbol{\theta}_{t}
and a dual budget multiplier
λ
t
\lambda_{t}
.
At step
t
t
, utility is:
u
t
=
𝜽
t
⊤
​
𝐡
t
−
λ
t
​
c
^
t
,
u_{t}=\boldsymbol{\theta}_{t}^{\top}\mathbf{h}_{t}-\lambda_{t}\hat{c}_{t},
and verification is triggered when
u
t
>
0
u_{t}>0
.
Given outcome
y
t
y_{t}
, the scoring parameters are updated via exponentiated gradient
(
Kivinen and Warmuth 1997
)
:
EG
​
(
𝜽
,
𝐠
,
η
)
k
=
θ
k
​
exp
⁡
(
η
​
g
k
)
∑
j
θ
j
​
exp
⁡
(
η
​
g
j
)
,
\mathrm{EG}(\boldsymbol{\theta},\mathbf{g},\eta)_{k}=\frac{\theta_{k}\exp(\eta g_{k})}{\sum_{j}\theta_{j}\exp(\eta g_{j})},
with gradient:
∇
θ
J
t
=
(
y
t
−
σ
⁡
(
u
t
)
)
⋅
𝐡
t
,
\nabla_{\theta}J_{t}=(y_{t}-\sigma(u_{t}))\cdot\mathbf{h}_{t},
where
σ
\sigma
is a sigmoid surrogate used only in the gradient (the decision rule itself is deterministic).
The dual variable is updated on every step:
λ
t
+
1
=
max
⁡
(
0
,
λ
t
+
η
λ
​
(
a
t
⋅
c
t
−
β
/
N
)
)
.
\lambda_{t+1}=\max\!\left(0,\;\lambda_{t}+\eta_{\lambda}(a_{t}\cdot c_{t}-\beta/N)\right).
It represents the strongest globally shared learner; if global sharing is the bottleneck, per-stratum control should recover performance.
MP-Strat: Partial stratification.
MP-Strat tests optimization instability by maintaining independent dual variables
λ
k
\lambda_{k}
per cost stratum and a teacher–student EMA
(
He et al. 2020
)
:
𝜽
k
T
←
γ
​
𝜽
k
T
+
(
1
−
γ
)
​
𝜽
k
S
,
γ
=
0.9
.
\boldsymbol{\theta}^{T}_{k}\leftarrow\gamma\boldsymbol{\theta}^{T}_{k}+(1-\gamma)\boldsymbol{\theta}^{S}_{k},\quad\gamma=0.9.
The teacher
𝜽
k
T
\boldsymbol{\theta}^{T}_{k}
is used for decisions; the student
𝜽
k
S
\boldsymbol{\theta}^{S}_{k}
is updated online.
3.4
Structural Partitioning Without Learning
CST tests structural alignment without online learning. It partitions samples into
K
=
4
K=4
strata by ex-ante cost
c
^
t
\hat{c}_{t}
and applies independent running quantiles:
a
t
\displaystyle a_{t}
=
(
s
⁡
(
𝐡
t
)
c
^
t
>
τ
k
⁡
(
t
)
,
t
)
,
\displaystyle=\mathbf{1}\!\left(\frac{s(\mathbf{h}_{t})}{\hat{c}_{t}}>\tau_{k(t),t}\right),
τ
k
,
t
\displaystyle\tau_{k,t}
=
Quantile
1
−
β
​
{
s
⁡
(
𝐡
j
)
c
^
j
∣
k
⁡
(
j
)
=
k
}
j
<
t
.
\displaystyle=\mathrm{Quantile}_{1-\beta}\!\left\{\frac{s(\mathbf{h}_{j})}{\hat{c}_{j}}\mid k(j)=k\right\}_{j<t}.
Here
k
⁡
(
t
)
k(t)
is the cost stratum index. CST uses Threshold’s fixed score and the same online information stream—no additional labels or gradient updates. Its only difference from Threshold is structural, so their gap isolates stratification.
3.5
Heterogeneity-Gated Allocation
HGA turns the diagnostic into a policy-selection rule rather than a post-hoc oracle over methods. On a warm-up split, it estimates stratum-level signal quality
ρ
k
=
corr
⁡
(
s
,
y
∣
k
)
\rho_{k}=\mathrm{corr}(s,y\mid k)
, base error rates, and the validation hit rates of Threshold and CST. The gate opens only when CST is not worse on warm-up feedback and the cost partition exhibits both discriminability dispersion and base-rate alignment:
Var
k
​
(
ρ
k
)
≥
ϵ
H
,
max
k
⁡
p
^
k
−
min
k
⁡
p
^
k
≥
ϵ
p
.
\mathrm{Var}_{k}(\rho_{k})\geq\epsilon_{H},\qquad\max_{k}\hat{p}_{k}-\min_{k}\hat{p}_{k}\geq\epsilon_{p}.
If the gate opens, HGA deploys CST; otherwise it deploys the global Threshold policy. HGA uses the same score initialization and budget accounting as the candidate policies; only the deployment choice is gated by warm-up comparability evidence. Thus HGA is not a stronger optimizer than CST. It is a guard against blind stratification: the same diagnostic that identifies comparability failure also decides whether structural specialization should be used.
Table 1:
Main results: mean hit rate across 10 seeds (heterogeneous costs). Bold: best non-Oracle per row. The rightmost column reports paired mean CST
−
-
Threshold gain with 95% CI in brackets.
Setting
β
\beta
Rand
Thr
CST
C+M
MP-A
MP-S
Oracle
Δ
\Delta
(CST
−
-
Thr) [95% CI]
MBPP
Qwen3
err=.558
ρ
\rho
=.178
10%
.551
.636
.671
.622
.597
.656
1.00
+
3.4
+3.4
[
−
0.2
,
+
7.0
]
[-0.2,+7.0]
20%
.546
.610
.661
.647
.619
.634
1.00
+
5.1
+5.1
[
+
3.6
,
+
6.6
]
[+3.6,+6.6]
30%
.550
.605
.661
.638
.616
.599
1.00
+
5.6
+5.6
[
+
4.3
,
+
7.0
]
[+4.3,+7.0]
50%
.562
.588
.631
.615
.569
.600
1.00
+
4.3
+4.3
[
+
3.3
,
+
5.3
]
[+3.3,+5.3]
MBPP
LLaMA3
err=.644
ρ
\rho
=.301
10%
.630
.712
.882
.844
.689
.837
1.00
+
17.0
+17.0
[
+
12.8
,
+
21.1
]
[+12.8,+21.1]
20%
.638
.686
.837
.795
.693
.794
1.00
+
15.1
+15.1
[
+
13.2
,
+
17.0
]
[+13.2,+17.0]
30%
.642
.693
.803
.755
.692
.763
1.00
+
11.0
+11.0
[
+
9.2
,
+
12.9
]
[+9.2,+12.9]
50%
.649
.675
.728
.693
.673
.704
1.00
+
5.3
+5.3
[
+
4.1
,
+
6.5
]
[+4.1,+6.5]
MBPP
GPT-4o-mini
err=.528
ρ
\rho
=.174
10%
.513
.511
.592
.592
.524
.552
.99
+
8.1
+8.1
[
+
4.5
,
+
11.7
]
[+4.5,+11.7]
20%
.527
.545
.610
.610
.553
.579
.99
+
6.5
+6.5
[
+
4.3
,
+
8.7
]
[+4.3,+8.7]
30%
.533
.547
.614
.620
.563
.578
1.00
+
6.7
+6.7
[
+
5.6
,
+
7.8
]
[+5.6,+7.8]
50%
.539
.578
.612
.601
.580
.576
1.00
+
3.4
+3.4
[
+
2.5
,
+
4.3
]
[+2.5,+4.3]
MATH
Qwen3
err=.247
ρ
\rho
=.153
10%
.242
.524
.322
.308
.356
.288
1.00
−
20.2
-20.2
[
−
22.3
,
−
18.1
]
[-22.3,-18.1]
20%
.246
.384
.308
.303
.310
.285
1.00
−
7.6
-7.6
[
−
8.4
,
−
6.8
]
[-8.4,-6.8]
30%
.248
.320
.301
.296
.284
.265
.94
−
1.9
-1.9
[
−
2.4
,
−
1.4
]
[-2.4,-1.4]
50%
.248
.264
.283
.272
.250
.252
.53
+
2.0
+2.0
[
+
1.6
,
+
2.3
]
[+1.6,+2.3]
MATH
LLaMA3
err=.613
ρ
\rho
=.201
10%
.605
.848
.799
.744
.734
.730
1.00
−
4.9
-4.9
[
−
6.7
,
−
3.2
]
[-6.7,-3.2]
20%
.608
.774
.758
.718
.681
.699
1.00
−
1.6
-1.6
[
−
2.4
,
−
0.8
]
[-2.4,-0.8]
30%
.615
.719
.734
.698
.653
.671
1.00
+
1.5
+1.5
[
+
1.1
,
+
2.0
]
[+1.1,+2.0]
50%
.616
.655
.693
.668
.615
.632
1.00
+
3.7
+3.7
[
+
3.4
,
+
4.1
]
[+3.4,+4.1]
4
Theoretical Analysis
4.1
Setup
Samples are drawn from
K
K
latent strata with mixture weights
w
k
w_{k}
. Each stratum
k
k
has signal-error correlation
ρ
k
=
corr
⁡
(
s
,
y
∣
k
)
\rho_{k}=\mathrm{corr}(s,y\mid k)
, computed as the point-biserial correlation between continuous scores and binary error labels (significance: two-sided
t
t
-test), and signal variance
σ
k
2
\sigma_{k}^{2}
.
Let
z
=
s
/
c
^
z=s/\hat{c}
denote the cost-normalized ranking score. For the theoretical comparison, define the
error-discovery value
of a policy as
V
⁡
(
π
)
=
𝔼
⁡
[
y
⋅
𝟏
​
{
π
​
verifies the sample
}
]
,
V(\pi)=\mathbb{E}[y\cdot\mathbf{1}\{\pi\text{ verifies the sample}\}],
which measures discovered error mass under a fixed population budget. This differs from the empirical hit-rate ratio; we use it because it admits a transparent decomposition of allocation distortion. The theorem therefore predicts when global and stratified allocation can diverge in error mass; the empirical hit-rate and audit-rate analyses then test whether that divergence appears as useful auditing precision, increased coverage, or harmful over-allocation.
Definition 1
(Global Quantile Policy)
.
π
global
\pi_{\mathrm{global}}
selects the top
β
\beta
-fraction of samples ranked by
s
/
c
^
s/\hat{c}
.
One might expect that a sufficiently powerful global optimizer could learn to account for stratum-specific signal quality—effectively discovering the stratification from data. The following result isolates why a global quantile remains structurally sensitive to heterogeneity even with perfect knowledge of the score distribution: its allocation distortion is controlled by cross-stratum discriminability dispersion.
Proposition 1
(Heteroskedastic Allocation-Distortion Bound)
.
Define per-stratum discriminability
δ
k
\delta_{k}
as the standardized separation between error and correct-sample distributions of
z
z
. Assume:
(A1)
the error-weighted density
g
k
​
(
z
)
=
p
k
​
f
k
​
(
z
∣
y
=
1
)
g_{k}(z)=p_{k}f_{k}(z\mid y{=}1)
satisfies
sup
z
g
k
​
(
z
)
≤
M
\sup_{z}g_{k}(z)\leq M
;
(A2)
the relevant global and stratum quantile maps are locally
ℓ
−
1
\ell^{-1}
-Lipschitz, equivalently the corresponding score densities are lower bounded by
ℓ
>
0
\ell>0
on the quantile neighborhood; and
(A3)
as a concrete local model, strata share error prevalence and scale and differ through the Gaussian location-separation parameter
δ
k
\delta_{k}
. Then:
|
V
⁡
(
π
strat
)
−
V
⁡
(
π
global
)
|
≤
2
​
M
​
p
ℓ
​
2
​
π
​
∑
k
w
k
​
|
δ
k
−
δ
¯
|
,
\begin{split}&\bigl|V(\pi_{\mathrm{strat}})-V(\pi_{\mathrm{global}})\bigr|\\
&\quad\leq\frac{2Mp}{\ell\sqrt{2\pi}}\sum_{k}w_{k}\,|\delta_{k}-\bar{\delta}|,\end{split}
(2)
where
p
p
is the shared error prevalence and
δ
¯
=
∑
k
w
k
​
δ
k
\bar{\delta}=\sum_{k}w_{k}\delta_{k}
. Under (A3), the bound vanishes when
δ
k
=
δ
¯
\delta_{k}=\bar{\delta}
for all
k
k
.
Figure 2:
Signal strength sweep under homogeneous synthetic signals (
h
syn
=
ρ
​
y
~
+
1
−
ρ
2
​
ε
h^{\text{syn}}=\rho\tilde{y}+\sqrt{1{-}\rho^{2}}\,\varepsilon
, uniform
ρ
k
≡
ρ
\rho_{k}\equiv\rho
). MP-Syn (blue curve) vs. Threshold (red dashed); blue diamond: homogeneous MP-Syn at
ρ
=
0.178
\rho{=}0.178
; red cross: actual MP-Adapt. The gap indicates efficiency loss from heterogeneous signal structures.
(A3)’s homogeneous prevalence isolates discriminability heterogeneity from base-rate heterogeneity, analyzed separately as Source B below.
Under the equal-variance location model,
δ
k
\delta_{k}
is monotonically related to the point-biserial correlation
ρ
k
=
corr
⁡
(
s
,
y
∣
k
)
\rho_{k}=\mathrm{corr}(s,y\mid k)
; for weak separation,
δ
k
≈
ρ
k
/
p
k
​
(
1
−
p
k
)
\delta_{k}\approx\rho_{k}/\sqrt{p_{k}(1-p_{k})}
. Thus cross-stratum variation in
ρ
k
\rho_{k}
provides an observable, local diagnostic for the dispersion term. The supplementary proof derives the explicit constant by composing a quantile-perturbation bound with the bounded error-mass density in (A1).
Proposition
1
characterizes allocation distortion induced by heterogeneous discriminability (
Source A
). The bound is diagnostic rather than a universal lower bound on CST’s gain: it controls how far global and stratified allocation values can diverge under a transparent local model, but does not determine the sign of the difference or directly bound the empirical hit-rate ratio. This is distinct from a second empirical mechanism: CST also reallocates budget toward high-error strata whose uncertainty signals are weak but whose base error rates are substantially elevated (
Source B
). For example, in Q4 of MBPP Qwen3,
ρ
Q4
=
0.157
\rho_{\mathrm{Q4}}{=}0.157
(n.s.) yet the error rate is 0.714; CST increases audit coverage from 0.151 to 0.191, trading precision for recall in error-dense regions. Together, the proposition and this coverage analysis explain why structural partitioning helps in strongly heterogeneous settings while correctly allowing negative gains when heterogeneity is weak or poorly aligned.
Cost as a signal-quality proxy.
Per-stratum
ρ
k
\rho_{k}
values (Figure
4
) show that ex-ante cost identifies heterogeneity regimes across all three models. Despite opposite directional patterns—Qwen3 and GPT-4o-mini degrade in Q4 while LLaMA3 rises monotonically—CST improves over Threshold in all three MBPP cases.
5
Experiments
5.1
Setup
Datasets and Models.
We evaluate Qwen3-8B
(
Yang et al. 2025
)
, LLaMA3-8B
(
Grattafiori et al. 2024
)
, and GPT-4o-mini
(
OpenAI et al. 2024
)
on MBPP
(
Austin et al. 2021
)
(
N
=
500
N{=}500
; unit-test feedback) and MATH
(
Hendrycks et al. 2021
)
(
N
=
5000
N{=}5000
; answer matching). Error rates are 55.8%/24.7% for Qwen3 on MBPP/MATH, 64.4%/61.3% for LLaMA3, and 52.8% for GPT-4o-mini on MBPP.
Costs, Noise, and Baselines.
Decisions use an input-length-normalized proxy cost
c
^
t
\hat{c}_{t}
, while budget consumption uses output-length-normalized true cost
c
t
c_{t}
(correlation
≈
0.3
\approx 0.3
). We add 10% Bernoulli label noise and Gaussian proxy noise (
σ
=
0.1
\sigma{=}0.1
). The diagnostic chain is Random, Threshold, MP-Adapt, MP-Strat, CST, and Oracle; Table
1
also reports CST+Memory, with details in the supplementary material.
Hyperparameters.
We use
η
θ
=
0.5
\eta_{\theta}{=}0.5
with decay
0.002
0.002
, EMA momentum
γ
=
0.9
\gamma{=}0.9
, a
λ
k
\lambda_{k}
floor of
0.1
0.1
, and budget-scaled
η
λ
\eta_{\lambda}
. Threshold and CST fix
𝐰
0
\mathbf{w}_{0}
from the first
T
0
=
50
T_{0}{=}50
samples. HGA keeps this same score initialization and uses a separate 50% calibration split for the gate, with
ϵ
H
=
0.002
\epsilon_{H}{=}0.002
,
ϵ
p
=
0.03
\epsilon_{p}{=}0.03
, and nonnegative warm-up gain required before opening the CST gate. All policies use the same stream order, proxy signals, noisy labels, and budget accounting; we report Student-
t
t
95% CIs across 10 seeds.
5.2
Main Result: A Hierarchy of Bottlenecks
Table
1
tests whether failure of global signal comparability, rather than insufficient adaptation, explains global-policy underperformance. If so, the deliberately weaker but structurally aligned CST should outperform both global policies (full results in the supplementary material).
MP-Adapt fails to reliably outperform Threshold, while MP-Strat’s partial recovery shows that optimization instability is present but does not explain the full gap. CST performs best when cross-stratum heterogeneity is strong: less learning yields better allocation once the decision structure matches the feedback regime.
We isolate three potential sources of gain—signal heteroskedasticity, cost heterogeneity, and optimization noise. Homogeneous-cost controls in the supplementary material rule out cost heterogeneity alone, while MP-Strat shows that optimization noise is insufficient to explain the observed differences; together, these controls identify cross-stratum signal heteroskedasticity as the most consistent explanation among the tested mechanisms.
Across MBPP settings, CST improves over Threshold with CIs excluding zero (Table
1
). At
β
=
20
%
\beta{=}20\%
, the gain reaches
+
5.1
+5.1
pp (95% CI
[
+
3.6
,
+
6.6
]
[+3.6,+6.6]
) for Qwen3,
+
15.1
+15.1
pp
[
+
13.2
,
+
17.0
]
[+13.2,+17.0]
for LLaMA3, and
+
6.5
+6.5
pp
[
+
4.3
,
+
8.7
]
[+4.3,+8.7]
for GPT-4o-mini. In contrast, Qwen3-MATH exhibits a negative CST gain (
−
7.6
-7.6
pp at
β
=
20
%
\beta{=}20\%
, 95% CI
[
−
8.4
,
−
6.8
]
[-8.4,-6.8]
). This conditional behavior is consistent with our diagnosis: stratification is useful only when the chosen partition aligns with consequential heterogeneity.
In a calibration reanalysis of the gate, HGA stays close to CST in the MBPP settings where cost-aligned heterogeneity is useful, but recovers Threshold on Qwen3-MATH, where fixed stratification underperforms. At
β
=
20
%
\beta{=}20\%
, HGA obtains .653/.804/.591 on MBPP Qwen3/LLaMA3/GPT-4o-mini and .385/.774 on MATH Qwen3/LLaMA3, respectively (full per-budget results in the supplementary material). This is the intended role of the gate: not to dominate the best fixed policy in every setting, but to avoid committing to stratification when comparability evidence is weak.
Figure
3
summarizes this boundary condition across budgets.
Figure 3:
CST and HGA gain over Threshold (
Δ
\Delta
hit rate, pp) across budgets
β
\beta
in the calibration reanalysis.
Figure 4:
Per-stratum
ρ
k
\rho_{k}
across cost quartiles. Filled markers indicate
p
<
.05
p{<}.05
and open markers indicate n.s.; shaded region marks near-random signal (
ρ
k
<
0.10
\rho_{k}{<}0.10
).
5.3
Signal Quality and Heteroskedasticity
We now diagnose the bottleneck via three hypotheses: weak signal, optimization instability, or cross-stratum heterogeneity.
Signal strength analysis.
We construct synthetic signals:
h
syn
=
ρ
⋅
y
~
+
1
−
ρ
2
⋅
ε
,
ε
∼
𝒩
⁡
(
0
,
1
)
.
h^{\mathrm{syn}}=\rho\cdot\tilde{y}+\sqrt{1-\rho^{2}}\cdot\varepsilon,\quad\varepsilon\sim\mathcal{N}(0,1).
Figure
2
shows MP-Syn improves over Threshold when
ρ
≳
0.20
\rho\gtrsim 0.20
. At the observed
ρ
=
0.178
\rho{=}0.178
, MP-Syn remains above Threshold under homogeneous assumptions, while the actual MP-Adapt result is below—indicating additional inefficiency from heterogeneous signal structures.
Within-stratum heteroskedasticity.
MBPP Qwen3 exhibits substantial per-stratum variation: Q4 combines the highest error rate (0.714) with weak signal (
ρ
=
0.157
\rho{=}0.157
, n.s.), while only Q3 has significant discriminability (
ρ
=
0.256
\rho{=}0.256
,
p
<
.01
p{<}.01
).
Figure
4
extends this analysis across all settings. MBPP models exhibit strong heterogeneity with distinct per-model patterns; MATH exhibits weaker and less structured variation, consistent with its smaller CST gains (Proposition
1
). Because MP-Adapt aggregates gradients globally, low-quality strata dilute informative gradients from high-signal regions.
Hypothesis tests.
Three ablations support this diagnosis. (1)
Partial feedback
: restricting updates to verified samples changes performance by
<
0.5
<0.5
pp, making feedback sparsity an unlikely primary explanation. (2)
Oracle signal
: replacing proxy signals with true labels yields perfect hit rate, showing that the optimization framework is sufficient given reliable signals. (3)
MP-Strat
: stabilization partially recovers (
+
2.8
+2.8
pp), but the remaining gap to CST (
−
1.9
-1.9
pp) points to structural heterogeneity as the largest remaining limitation among the tested hypotheses.
Diagnosing comparability failure.
Optimizer weakness predicts that stronger global learning closes the stratification gap. Comparability failure instead predicts varying stratum-level signal quality, partial MP-Strat recovery, and a weak aligned intervention outperforming global adaptation. Negative-control partitions and Qwen3-MATH support this distinction: structural alignment helps only when the partition captures consequential feedback regimes.
5.4
A Weak Structural Intervention
Having diagnosed comparability failure, we use CST as a deliberately weak intervention to examine how structural alignment changes allocation.
Table
2
illustrates two complementary sources of CST’s improvement.
Table 2:
CST vs. Threshold per-stratum behavior (
β
=
20
%
\beta=20\%
).
Audit rate
Hit rate
Error
Stratum
Thr
CST
Thr
CST
rate
Q1
.306
.189
.412
.429
.423
Q2
.216
.209
.586
.571
.500
Q3
.186
.217
.625
.714
.581
Q4
.151
.191
.947
.833
.714
Source 1 (precision gain in high-signal strata):
In Q3 (
ρ
=
0.256
\rho=0.256
,
p
<
.01
p{<}.01
), CST increases audit rate from 0.186 to 0.217 while hit rate rises from 0.625 to 0.714 (
+
8.9
+8.9
pp).
Source 2 (coverage gain in low-signal strata):
In Q4 (
ρ
=
0.157
\rho=0.157
, n.s., error rate 0.714), CST increases audit rate from 0.151 to 0.191 (
+
26.5
%
+26.5\%
), trading precision for recall: hit rate drops from 0.947 to 0.833, but more total errors are found. Despite near-random signals, the high base error rate makes increased coverage effective.
Negative-control stratification results in the supplementary material show that cost is the only tested ex-ante criterion that improves over global Threshold; random partitions and noisy signal-strength bins degrade performance. Per-stratum split-conformal calibration further confirms that stratification, rather than CST-specific optimization, drives most gains.
5.5
Cross-Task and Cross-Model Analysis
Finally, we characterize the boundary conditions for structural partitioning.
Figure
3
shows that MBPP gains are consistently positive, whereas MATH is conditional on model and budget. HGA follows these boundary conditions rather than treating stratification as universally beneficial; full gate decisions appear in the supplementary material. Table
1
reveals three cross-task patterns.
This evaluation frames HGA as policy selection rather than post-hoc model choice: replace a global comparator with stratum-local comparators only when warm-up feedback supports specialization.
(1) CST gains depend on both cost-error correlation and heteroskedasticity.
LLaMA3-MATH (
r
=
0.309
r=0.309
) shows CST gains at
β
≥
30
%
\beta\geq 30\%
, while Qwen3-MATH (
r
=
0.193
r=0.193
) underperforms. GPT-4o-mini-MBPP achieves higher gains despite lower global correlation due to stronger signal collapse in high-cost strata.
(2) Optimization stabilization has conditional benefits.
MP-Strat improves over MP-Adapt only in moderate-to-high correlation regimes; in low-correlation settings (e.g., Qwen3-MATH), stabilization can reduce performance.
(3) Heteroskedasticity is structural, not model-specific.
Across MBPP, signal degradation occurs in opposite directions yet CST consistently improves. A heterogeneity index
H
=
Var
k
​
(
ρ
k
)
H{=}\mathrm{Var}_{k}(\rho_{k})
captures this: Qwen3 (
H
=
0.0035
H{=}0.0035
) vs. LLaMA3 (
H
=
0.0065
H{=}0.0065
) yields
+
5.1
+5.1
vs.
+
15.1
+15.1
pp; GPT-4o-mini (
H
=
0.0025
H{=}0.0025
) achieves
+
6.5
+6.5
pp via extreme Q4 signal collapse.
A diagnostic protocol for allocation systems.
Before increasing optimizer complexity, practitioners should measure conditional signal quality across observable strata and compare an aligned partition against both the global policy and negative-control partitions. Improvement only under the aligned partition indicates comparability failure; HGA operationalizes this test by gating stratification on warm-up evidence.
6
Conclusion
The intervention hierarchy separates weak signals, optimization instability, and structural heterogeneity: MP-Strat partially recovers performance, while CST exposes when structural alignment matters. HGA turns this diagnosis into a guarded policy choice. The broader principle is to test feedback comparability before trusting stronger global optimization: a failed adaptive allocator may indicate that equal proxy scores have different decision value across operating regimes.
References
Agrawal and Devanur (2014)
S. Agrawal and N. R. Devanur
Bandits with concave rewards and convex knapsacks
.
In
Proceedings of the fifteenth ACM conference on Economics and computation
,
pp. 989–1006
.
Cited by:
§2
.
Angelopoulos and Bates (2022)
A. N. Angelopoulos and S. Bates
A gentle introduction to conformal prediction and distribution-free uncertainty quantification
.
External Links:
2107.07511
,
Link
Cited by:
§2
.
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le,
et al.
Program synthesis with large language models
.
arXiv preprint arXiv:2108.07732
.
Cited by:
§5.1
.
Badanidiyuru
et al.
(2018)
A. Badanidiyuru, R. Kleinberg, and A. Slivkins
Bandits with knapsacks
.
Journal of the ACM (JACM)
65
(
3
),
pp. 1–55
.
Cited by:
§2
.
Badanidiyuru
et al.
(2014)
A. Badanidiyuru, J. Langford, and A. Slivkins
Resourceful contextual bandits
.
In
Conference on Learning Theory
,
pp. 1109–1134
.
Cited by:
§2
.
Balseiro
et al.
(2020)
S. Balseiro, H. Lu, and V. Mirrokni
Dual mirror descent for online allocation problems
.
In
International Conference on Machine Learning
,
pp. 613–628
.
Cited by:
§2
.
Chen
et al.
(2023)
L. Chen, M. Zaharia, and J. Zou
Frugalgpt: how to use large language models while reducing cost and improving performance
.
arXiv preprint arXiv:2305.05176
.
Cited by:
§2
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
et al.
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
Cited by:
§1
,
§2
.
Cherian
et al.
(2024)
J. J. Cherian, I. Gibbs, and E. J. Candès
Large language model validity via enhanced conformal prediction methods
.
Advances in Neural Information Processing Systems
37
,
pp. 114812–114842
.
Cited by:
§2
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
§2
.
Damani
et al.
(2025)
M. Damani, I. Shenfeld, A. Peng, A. Bobu, and J. Andreas
Learning how hard to think: input-adaptive allocation of lm computation
.
In
International Conference on Learning Representations
,
Vol.
2025
,
pp. 102783–102802
.
Cited by:
§2
.
Detommaso
et al.
(2024)
G. Detommaso, M. Bertran, R. Fogliato, and A. Roth
Multicalibration for confidence scoring in llms
.
arXiv preprint arXiv:2404.04689
.
Cited by:
§2
.
El-Yaniv
et al.
(2010)
R. El-Yaniv
et al.
On the foundations of noise-free selective classification.
.
Journal of Machine Learning Research
11
(
5
).
Cited by:
§2
.
Fan
et al.
(2026)
Q. Fan, A. Zou, and Y. Ma
Timebill: time-budgeted inference for large language models
.
In
Proceedings of the AAAI Conference on Artificial Intelligence
,
Vol.
40
,
pp. 30620–30628
.
Cited by:
§2
.
Fang
et al.
(2022)
H. Fang, N. J. Harvey, V. S. Portella, and M. P. Friedlander
Online mirror descent and dual averaging: keeping pace in the dynamic case
.
Journal of Machine Learning Research
23
(
121
),
pp. 1–38
.
Cited by:
§3.3
.
Fang
et al.
(2026)
Z. Fang, S. F. Hu, Z. Chang, Y. Guo, Y. Tao, H. Liu, M. Ruan, J. Huang, and Y. Fang
Inference-time budget control for llm search agents
.
arXiv preprint arXiv:2605.05701
.
Cited by:
§2
.
Farquhar
et al.
(2024)
S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal
Detecting hallucinations in large language models using semantic entropy
.
Nature
630
(
8017
),
pp. 625–630
.
Cited by:
§2
.
Geifman and El-Yaniv (2017)
Y. Geifman and R. El-Yaniv
Selective classification for deep neural networks
.
Advances in neural information processing systems
30
.
Cited by:
§2
.
Grattafiori
et al.
(2024)
A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian,
et al.
The llama 3 herd of models
.
External Links:
2407.21783
,
Link
Cited by:
§5.1
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
International conference on machine learning
,
pp. 1321–1330
.
Cited by:
§1
,
§2
.
Hazan (2016)
E. Hazan
Introduction to online convex optimization
.
Foundations and Trends in Optimization
2
(
3-4
),
pp. 157–325
.
Cited by:
§1
.
He
et al.
(2020)
K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick
Momentum contrast for unsupervised visual representation learning
.
In
Proceedings of the IEEE/CVF conference on computer vision and pattern recognition
,
pp. 9729–9738
.
Cited by:
§3.3
.
Hébert-Johnson
et al.
(2018)
U. Hébert-Johnson, M. Kim, O. Reingold, and G. Rothblum
Multicalibration: calibration for the (computationally-identifiable) masses
.
In
International Conference on Machine Learning
,
pp. 1939–1948
.
Cited by:
§2
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
§5.1
.
Huang
et al.
(2024)
X. Huang, S. Li, M. Yu, M. Sesia, H. Hassani, I. Lee, O. Bastani, and E. Dobriban
Uncertainty in language models: assessment through rank-calibration
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
pp. 284–312
.
Cited by:
§2
,
§2
.
Jimenez
et al.
(2024)
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan
Swe-bench: can language models resolve real-world github issues?
.
In
International Conference on Learning Representations
,
Vol.
2024
,
pp. 54107–54157
.
Cited by:
§1
,
§2
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
§1
,
§2
.
Kivinen and Warmuth (1997)
J. Kivinen and M. K. Warmuth
Exponentiated gradient versus gradient descent for linear predictors
.
Information and computation
132
(
1
),
pp. 1–63
.
Cited by:
§3.3
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
arXiv preprint arXiv:2302.09664
.
Cited by:
§1
,
§2
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
(2024)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
Let’s verify step by step
.
In
International Conference on Learning Representations
,
Vol.
2024
,
pp. 39578–39601
.
Cited by:
§2
.
Madaan
et al.
(2023)
A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang,
et al.
Self-refine: iterative refinement with self-feedback
.
Advances in neural information processing systems
36
,
pp. 46534–46594
.
Cited by:
§2
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
§2
.
Nemirovski (2004)
A. Nemirovski
Prox-method with rate of convergence o (1/t) for variational inequalities with lipschitz continuous monotone operators and smooth convex-concave saddle point problems
.
SIAM Journal on Optimization
15
(
1
),
pp. 229–251
.
Cited by:
§3.3
.
Ni
et al.
(2023)
A. Ni, S. Iyer, D. Radev, V. Stoyanov, W. Yih, S. I. Wang, and X. V. Lin
Lever: learning to verify language-to-code generation with execution
.
In
Proceedings of the 40th International Conference on Machine Learning (ICML’23)
,
Cited by:
§2
.
Ong
et al.
(2024)
I. Ong, A. Almahairi, V. Wu, W. Chiang, T. Wu, J. E. Gonzalez, M. W. Kadous, and I. Stoica
Routellm: learning to route llms with preference data
.
arXiv preprint arXiv:2406.18665
.
Cited by:
§2
.
OpenAI
et al.
(2024)
OpenAI, A. Hurst, A. Lerer, A. P. Goucher, A. Perelman,
et al.
GPT-4o system card
.
External Links:
2410.21276
,
Link
Cited by:
§5.1
.
Sharma and David (2025)
A. Sharma and C. David
Assessing correctness in llm-based code generation via uncertainty estimation
.
arXiv preprint arXiv:2502.11620
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
§2
.
Tao
et al.
(2025)
L. Tao, Y. Yeh, M. Dong, T. Huang, P. Torr, and C. Xu
Revisiting uncertainty estimation and calibration of large language models
.
arXiv preprint arXiv:2505.23854
.
Cited by:
§2
,
§2
.
Wang
et al.
(2022)
X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou
Self-consistency improves chain of thought reasoning in language models
.
arXiv preprint arXiv:2203.11171
.
Cited by:
§2
.
Xiong
et al.
(2024)
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi
Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms
.
In
International Conference on Learning Representations
,
Vol.
2024
,
pp. 23650–23678
.
Cited by:
§2
.
Yang
et al.
(2025)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui,
et al.
Qwen3 technical report
.
arXiv preprint arXiv:2505.09388
.
Cited by:
§5.1
.
Zhang
et al.
(2024)
L. Zhang, A. Roth, and L. Zhang
Fair risk control: a generalized framework for calibrating multi-group fairness risks
.
arXiv preprint arXiv:2405.02225
.
Cited by:
§2
.
Zhao
et al.
(2025)
Z. Zhao, S. Zhang, Z. Wang, H. Wang, Y. Zhao, B. Liang, Y. Zheng, B. Li, K. Wong, and X. Wu
T2: an adaptive test-time scaling strategy for contextual question answering
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
pp. 3731–3756
.
Cited by:
§2
.
Supplementary Material
Appendix A
Proof of the Allocation-Distortion Proposition
Proof.
Let
z
=
s
/
c
^
z=s/\hat{c}
and let the population be partitioned into
K
K
strata with weights
w
k
w_{k}
. Write
F
k
F_{k}
for the within-stratum CDF of
z
z
,
F
=
∑
k
w
k
​
F
k
F=\sum_{k}w_{k}F_{k}
for the mixture CDF, and
g
k
​
(
z
)
=
p
​
f
k
​
(
z
∣
y
=
1
)
g_{k}(z)=pf_{k}(z\mid y{=}1)
for the error-weighted density under the shared prevalence assumption in (A3).
Step 1: Stratum-wise decomposition.
Using the law of total expectation,
V
⁡
(
π
)
=
∑
k
=
1
K
w
k
⋅
𝔼
⁡
[
y
⋅
𝟏
​
(
z
>
τ
)
∣
k
]
.
V(\pi)=\sum_{k=1}^{K}w_{k}\cdot\mathbb{E}[y\cdot\mathbf{1}(z>\tau)\mid k].
Thus the allocation-value gap decomposes into per-stratum contributions.
Step 2: Global threshold as mixture distortion.
The global threshold
τ
\tau
satisfies the mixture budget constraint:
∑
k
w
k
​
ℙ
​
(
z
>
τ
∣
k
)
=
β
.
\sum_{k}w_{k}\mathbb{P}(z>\tau\mid k)=\beta.
Equivalently,
τ
=
Q
1
−
β
​
(
F
)
\tau=Q_{1-\beta}(F)
, and the stratified policy uses
τ
k
=
Q
1
−
β
​
(
F
k
)
\tau_{k}=Q_{1-\beta}(F_{k})
within each stratum. By the local inverse-Lipschitz condition in (A2), the quantile perturbation satisfies
|
τ
−
τ
k
|
≤
1
ℓ
​
sup
z
|
F
k
​
(
z
)
−
F
⁡
(
z
)
|
.
|\tau-\tau_{k}|\leq\frac{1}{\ell}\sup_{z}|F_{k}(z)-F(z)|.
(3)
Step 3: CDF deviation under heterogeneous discriminability.
Under the common-prevalence, common-scale Gaussian location model in (A3), the stratum CDFs differ through
δ
k
\delta_{k}
. Since
‖
Φ
′
‖
∞
=
1
/
2
​
π
\|\Phi^{\prime}\|_{\infty}=1/\sqrt{2\pi}
,
sup
z
|
F
k
​
(
z
)
−
F
j
​
(
z
)
|
≤
p
2
​
π
​
|
δ
k
−
δ
j
|
.
\sup_{z}|F_{k}(z)-F_{j}(z)|\leq\frac{p}{\sqrt{2\pi}}|\delta_{k}-\delta_{j}|.
Because
F
=
∑
j
w
j
​
F
j
F=\sum_{j}w_{j}F_{j}
, combining this inequality with Eq. (
3
) gives
|
τ
−
τ
k
|
≤
p
ℓ
​
2
​
π
​
∑
j
w
j
​
|
δ
k
−
δ
j
|
.
|\tau-\tau_{k}|\leq\frac{p}{\ell\sqrt{2\pi}}\sum_{j}w_{j}|\delta_{k}-\delta_{j}|.
Step 4: Composition into allocation-value gap.
Assumption (A1) implies that changing the threshold within stratum
k
k
changes discovered error mass by at most
|
∫
min
⁡
(
τ
,
τ
k
)
max
⁡
(
τ
,
τ
k
)
g
k
​
(
z
)
​
𝑑
z
|
≤
M
​
|
τ
−
τ
k
|
.
\left|\int_{\min(\tau,\tau_{k})}^{\max(\tau,\tau_{k})}g_{k}(z)\,dz\right|\leq M|\tau-\tau_{k}|.
Therefore,
|
V
⁡
(
π
strat
)
−
V
⁡
(
π
global
)
|
\displaystyle|V(\pi_{\mathrm{strat}})-V(\pi_{\mathrm{global}})|
≤
∑
k
w
k
​
M
​
|
τ
−
τ
k
|
\displaystyle\leq\sum_{k}w_{k}M|\tau-\tau_{k}|
≤
M
​
p
ℓ
​
2
​
π
​
∑
k
,
j
w
k
​
w
j
​
|
δ
k
−
δ
j
|
\displaystyle\leq\frac{Mp}{\ell\sqrt{2\pi}}\sum_{k,j}w_{k}w_{j}|\delta_{k}-\delta_{j}|
≤
2
​
M
​
p
ℓ
​
2
​
π
​
∑
k
w
k
​
|
δ
k
−
δ
¯
|
,
\displaystyle\leq\frac{2Mp}{\ell\sqrt{2\pi}}\sum_{k}w_{k}|\delta_{k}-\bar{\delta}|,
where the final step uses
|
δ
k
−
δ
j
|
≤
|
δ
k
−
δ
¯
|
+
|
δ
j
−
δ
¯
|
|\delta_{k}-\delta_{j}|\leq|\delta_{k}-\bar{\delta}|+|\delta_{j}-\bar{\delta}|
.
This proves the stated bound. Under (A3), equal
δ
k
\delta_{k}
imply identical
F
k
F_{k}
, so
τ
k
=
τ
\tau_{k}=\tau
and the gap vanishes. The result is an upper bound on allocation-value divergence, not a sign guarantee for empirical hit-rate gains.
∎
Appendix B
Full Per-Budget Results on MBPP Qwen3-8B
Table
3
reports mean per-budget results for MBPP Qwen3-8B across 10 seeds, expanding the main-paper summary. CST achieves the best non-Oracle mean hit rate at every budget. The homogeneous-cost version appears in the homogeneous-cost control section below.
Table 3:
Mean hit rate across 10 seeds, MBPP Qwen3-8B (heterogeneous costs,
N
=
500
N=500
).
β
\beta
Rand
Thr
CST
C+M
MP-A
MP-S
Oracle
5%
.549
.616
.679
.666
.601
.642
1.00
10%
.551
.636
.671
.622
.597
.656
1.00
15%
.562
.620
.651
.651
.622
.621
1.00
20%
.546
.610
.661
.647
.619
.634
1.00
25%
.548
.610
.662
.651
.621
.616
1.00
30%
.550
.605
.661
.638
.616
.599
1.00
40%
.564
.591
.645
.625
.586
.608
1.00
50%
.562
.588
.631
.615
.569
.600
1.00
Appendix C
LLaMA3-8B Results on MBPP
Table
4
reports LLaMA3-8B results on MBPP (heterogeneous costs). Despite exhibiting the opposite heterogeneity pattern to Qwen3 (signal rises with cost rather than collapsing), CST gains remain strong, consistent with the diagnosis that cross-stratum dispersion—rather than its direction—creates consequential global-allocation distortion.
Table 4:
Mean LLaMA3-8B hit rate across 10 seeds on MBPP (heterogeneous costs,
N
=
500
N=500
).
β
\beta
Rand
Thr
CST
C+M
MP-A
MP-S
Oracle
5%
.624
.828
.898
.882
.749
.875
1.000
10%
.630
.712
.882
.844
.689
.837
1.000
15%
.629
.692
.855
.822
.698
.839
1.000
20%
.638
.686
.837
.795
.693
.794
1.000
25%
.643
.698
.821
.781
.702
.784
.989
30%
.642
.693
.803
.755
.692
.763
.995
40%
.650
.683
.760
.716
.677
.735
.996
50%
.649
.675
.728
.693
.673
.704
1.000
Appendix D
MATH Full Per-Budget Results
Tables
5
and
6
report full per-budget results on MATH (
N
=
5000
N=5000
). Qwen3-MATH shows Threshold as the dominant policy at
β
≤
30
%
\beta{\leq}30\%
, with CST gaining only at
β
=
50
%
\beta{=}50\%
. LLaMA3-MATH transitions at
β
≥
30
%
\beta{\geq}30\%
due to stronger cost-error correlation (
r
=
0.309
r{=}0.309
vs.
0.193
0.193
). At
β
=
5
%
\beta{=}5\%
, MP-Adapt outperforms CST on Qwen3 but not LLaMA3, reflecting the cross-task boundary condition discussed in the main paper.
Table 5:
Mean Qwen3-8B hit rate across 10 seeds on MATH (heterogeneous costs,
N
=
5000
N=5000
, pass@1=0.753).
β
\beta
Rand
Thr
CST
C+M
MP-A
MP-S
Oracle
5%
.250
.556
.329
.321
.395
.306
1.000
10%
.242
.524
.322
.308
.356
.288
1.000
15%
.244
.443
.314
.308
.330
.290
1.000
20%
.246
.384
.308
.303
.310
.285
.997
25%
.247
.348
.303
.301
.294
.271
.997
30%
.248
.320
.301
.296
.284
.265
.938
40%
.247
.285
.294
.284
.263
.258
.650
50%
.248
.264
.283
.272
.250
.252
.526
Table 6:
Mean LLaMA3-8B hit rate across 10 seeds on MATH (heterogeneous costs,
N
=
5000
N=5000
, pass@1=0.387).
β
\beta
Rand
Thr
CST
C+M
MP-A
MP-S
Oracle
5%
.611
.870
.828
.771
.777
.759
1.000
10%
.605
.848
.799
.744
.734
.730
.999
15%
.603
.810
.776
.727
.698
.710
.999
20%
.608
.774
.758
.718
.681
.699
1.000
25%
.611
.743
.745
.707
.667
.684
.999
30%
.615
.719
.734
.698
.653
.671
.999
40%
.615
.682
.715
.690
.629
.650
1.000
50%
.616
.655
.693
.668
.615
.632
1.000
Appendix E
GPT-4o-mini Results on MBPP
Table
7
reports GPT-4o-mini results on MBPP (heterogeneous costs). Its CST gains coincide with extreme Q4 signal collapse (
ρ
Q4
=
0.059
\rho_{\mathrm{Q4}}{=}0.059
n.s. vs. Qwen3’s 0.157 n.s.), supporting the use of cross-stratum heterogeneity—rather than global correlation alone—as the relevant diagnostic.
Table 7:
Mean GPT-4o-mini hit rate across 10 seeds on MBPP (heterogeneous costs,
N
=
500
N=500
).
β
\beta
Rand
Thr
CST
C+M
MP-A
MP-S
Oracle
5%
.535
.426
.630
.604
.455
.595
.977
10%
.513
.511
.592
.592
.524
.552
.988
15%
.526
.535
.603
.608
.549
.560
.991
20%
.527
.545
.610
.610
.553
.579
.993
25%
.533
.556
.610
.607
.557
.582
.994
30%
.533
.547
.614
.620
.563
.578
.995
40%
.540
.562
.612
.624
.578
.567
.991
50%
.539
.578
.612
.601
.580
.576
.996
Appendix F
Homogeneous Cost Control Experiment
Under homogeneous costs (
c
t
≡
0.5
c_{t}\equiv 0.5
), CST degenerates exactly to Threshold (Table
8
), confirming gains derive from heteroskedasticity correction. MP-Adapt underperforms Threshold (avg.
−
7.5
{-}7.5
pp across budgets), indicating that cost heterogeneity alone does not explain the underperformance of globally shared online adaptation. The primary cause is weak global signal strength (
ρ
≈
0.178
\rho{\approx}0.178
) present under both cost settings.
Table 8:
Hit rate under homogeneous costs (
c
t
≡
0.5
c_{t}\equiv 0.5
, MBPP, Qwen3-8B).
β
\beta
Rand
Thr
CST
C+M
MP-A
MP-S
Oracle
5%
.480
.680
.680
.800
.560
.600
1.000
10%
.440
.740
.740
.660
.580
.580
1.000
20%
.480
.650
.650
.650
.590
.610
1.000
30%
.553
.653
.653
.647
.673
.693
1.000
50%
.576
.669
.669
.658
.612
.636
1.000
Appendix G
Memory Augmentation Ablation
Memory-augmented CST retrieves verified samples within the same stratum as a fourth signal
h
t
(
4
)
h_{t}^{(4)}
. At
β
=
20
%
\beta{=}20\%
, optimal weight
w
≈
0.1
w{\approx}0.1
–
0.3
0.3
yields marginal gains (
+
1.0
+1.0
–
+
3.0
+3.0
pp over CST 0.644), while
w
≥
0.5
w{\geq}0.5
causes collapse (0.515 vs. CST 0.644). The memory signal correlates weakly with errors (
r
=
0.059
r{=}0.059
,
p
=
0.47
p{=}0.47
), confirming that memory amplifies but cannot create signal where none exists. GPT-4o-mini shows similarly weak memory gains (
+
1.4
+1.4
pp max).
Appendix H
Per-Stratum Split-Conformal Baseline
Table
9
reports the negative-control partition comparison used in the main-text diagnosis. Only the ex-ante cost partition improves over global Threshold, while random partitions and noisy signal-strength bins degrade performance.
Table 9:
Stratification criterion comparison (
β
=
20
%
\beta=20\%
).
Criterion
Hit Rate
Δ
\Delta
vs. Global
None (global)
0.604
—
Random partition
0.590
−
-
0.014
By signal strength
0.471
−
-
0.133
By ex-ante cost (CST)
0.644
+
+
0.040
Oracle partition
1.000
+
+
0.396
Table
10
reports per-stratum split-conformal quantile calibration (50% calibration split, fixed thresholds). This group-conditional conformal baseline partitions by cost like CST but uses one-shot calibrated thresholds. Conformal stratification improves over global Threshold universally, confirming stratification is the primary gain driver. CST’s online quantile adaptation adds further gains in most regimes; conformal exceeds CST only at GPT-4o-mini
β
=
10
%
\beta{=}10\%
(
+
9.5
+9.5
pp, where fixed calibration benefits from larger effective calibration samples) and LLaMA3-MATH
β
=
20
%
\beta{=}20\%
(
+
1.5
+1.5
pp).
Table 10:
Per-stratum split-conformal hit rate and
Δ
\Delta
vs. CST (pp, positive = exceeds CST).
β
\beta
Qwen3
LLaMA3
GPT-4o-mini
MBPP
10%
.667 (
−
3.1
-3.1
)
.852 (
−
3.1
-3.1
)
.648 (
+
9.5
+9.5
)
20%
.626 (
−
1.7
-1.7
)
.865 (
+
2.0
+2.0
)
.644 (
+
2.4
+2.4
)
30%
.650 (
−
1.9
-1.9
)
.797 (
−
2.0
-2.0
)
.604 (
−
3.2
-3.2
)
50%
.640 (
−
1.5
-1.5
)
.749 (
+
0.7
+0.7
)
.616 (
+
0.1
+0.1
)
MATH
10%
.315 (
−
0.8
-0.8
)
.822 (
+
0.5
+0.5
)
—
20%
.309 (
−
1.0
-1.0
)
.769 (
+
1.5
+1.5
)
—
30%
.305 (
+
0.8
+0.8
)
.741 (
+
0.3
+0.3
)
—
50%
.289 (
+
0.9
+0.9
)
.704 (
+
0.5
+0.5
)
—
Appendix I
Sensitivity to Number of Strata (
K
K
)
Table
11
reports CST hit rate vs.
K
K
on MATH (
K
=
1
K{=}1
is global Threshold). Qwen3-MATH degrades monotonically with
K
K
under weak heterogeneity (
r
=
0.193
r{=}0.193
); LLaMA3-MATH (
r
=
0.309
r{=}0.309
) peaks at
K
=
3
K{=}3
–
4
4
. Over-partitioning (
K
≥
6
K{\geq}6
) consistently degrades performance, confirming that within-stratum sample sizes must be sufficient for reliable quantile estimation, as predicted by the allocation-distortion analysis.
Table 11:
CST hit rate vs. strata count
K
K
(MATH).
K
=
1
K{=}1
is global Threshold.
Qwen3-8B
LLaMA3-8B
K
K
5%
10%
20%
30%
50%
5%
10%
20%
30%
50%
1
.569
.529
.384
.316
.266
.869
.839
.769
.718
.658
2
.434
.427
.376
.326
.286
.836
.823
.789
.756
.691
3
.380
.373
.336
.327
.284
.856
.794
.769
.744
.694
4
.341
.323
.317
.298
.279
.823
.789
.745
.736
.695
6
.293
.306
.285
.277
.269
.822
.788
.731
.716
.690
8
.295
.260
.257
.259
.253
.785
.751
.707
.699
.670
Appendix J
Full HGA Gate Results
Table
13
reports Heterogeneity-Gated Allocation (HGA) across budgets in the calibration reanalysis. HGA uses the same 50-sample score initialization as Threshold and CST, then uses a separate 50% diagnostic split to decide whether the CST gate should open. The pattern matches the intended role of the gate: HGA stays close to CST on MBPP, where cost-aligned stratification is useful, and reverts to Threshold on Qwen3-MATH, where fixed stratification is harmful at low and medium budgets.
Table
12
summarizes the gate decisions at
β
=
20
%
\beta{=}20\%
. These decisions are made before deployment on the evaluation stream; HGA does not choose the better test-set policy after observing test outcomes.
Table 12:
HGA gate decisions at
β
=
20
%
\beta{=}20\%
in the calibration reanalysis.
Setting
Gate
Policy
Outcome
MBPP-Qwen3
open
CST
retains gain
MBPP-LLaMA3
open
CST
retains gain
MBPP-GPT-4o-mini
open
CST
partial gain
MATH-Qwen3
closed
Threshold
avoids loss
MATH-LLaMA3
closed
Threshold
near Threshold
Table 13:
Full HGA calibration-reanalysis hit rate results across budgets (heterogeneous costs, 10 seeds). Bold indicates the best among Threshold, CST, and HGA.
Setting
β
\beta
Threshold
CST
HGA
MBPP-Qwen3
10%
.616
.681
.677
MBPP-Qwen3
20%
.624
.654
.653
MBPP-Qwen3
30%
.606
.656
.656
MBPP-Qwen3
50%
.579
.631
.631
MBPP-LLaMA3
10%
.689
.847
.826
MBPP-LLaMA3
20%
.677
.813
.804
MBPP-LLaMA3
30%
.686
.787
.770
MBPP-LLaMA3
50%
.674
.725
.725
MBPP-GPT-4o-mini
10%
.495
.571
.568
MBPP-GPT-4o-mini
20%
.533
.610
.591
MBPP-GPT-4o-mini
30%
.553
.614
.603
MBPP-GPT-4o-mini
50%
.572
.605
.598
MATH-Qwen3
10%
.525
.330
.525
MATH-Qwen3
20%
.385
.307
.385
MATH-Qwen3
30%
.321
.300
.316
MATH-Qwen3
50%
.264
.284
.280
MATH-LLaMA3
10%
.844
.798
.835
MATH-LLaMA3
20%
.775
.756
.774
MATH-LLaMA3
30%
.717
.734
.722
MATH-LLaMA3
50%
.656
.695
.668
Appendix K
Budgeted Model Routing Reanalysis
We further reinterpret the MBPP per-instance records as a budgeted model-routing problem. The cheap model is run first, and routing to GPT-4o-mini is valuable only when the cheap model fails and GPT-4o-mini succeeds. Policies use the cheap model’s uncertainty signals and an ex-ante prompt-cost proxy; the metric is routing hit rate among selected examples. This is a reanalysis of existing records, not a new model run.
Table
14
shows a conditional pattern. For Qwen3, routing benefits are sparse (9.6% of examples), and global Threshold is best at
β
=
20
%
\beta{=}20\%
. For LLaMA3, routing benefits are denser (15.8%), and stratified allocation improves over Threshold: MP-Strat reaches .183 and CST .180 vs. .173. Thus the routing setting supports the paper’s diagnostic interpretation rather than a universal claim that CST must dominate: stratification helps when the benefit signal has exploitable conditional structure, and simple global thresholding can remain competitive when the benefit label is too sparse.
Table 14:
Budgeted model-routing reanalysis on MBPP at
β
=
20
%
\beta{=}20\%
. Hit rate measures the fraction of routed examples for which the cheap model fails and GPT-4o-mini succeeds. Bold indicates the best non-oracle policy in each row.
Route
β
\beta
Rand.
Thr.
MP-A
MP-S
CST
Qwen3
→
\rightarrow
GPT-4o-mini
20%
.096
.109
.098
.100
.103
LLaMA3
→
\rightarrow
GPT-4o-mini
20%
.153
.173
.149
.183
.180
Appendix L
Visual Illustration of Global vs. Stratum-Adaptive Thresholding
Figure 5:
Global thresholding under heteroskedastic costs. Synthetic score distributions parameterized by empirical
ρ
k
\rho_{k}
and error rates (MBPP Qwen3-8B,
β
=
20
%
\beta{=}20\%
). Decision scores incorporate the cost denominator: higher cost deflates scores in Q4, inflates in Q1.
Left:
a single global threshold
τ
\tau
under-selects high-cost error-dense strata (Q4, highest error) and strong-signal strata (Q3), while over-selecting low-cost strata (Q1, Q2).
Right:
stratum-adaptive thresholds
τ
k
\tau_{k}
(CST) computed via per-stratum quantiles correct the misallocation.