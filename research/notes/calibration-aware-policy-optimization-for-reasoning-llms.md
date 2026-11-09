---
title: Calibration-Aware Policy Optimization for Reasoning LLMs
id: calibration-aware-policy-optimization-for-reasoning-llms
tags:
- code-llm-calibration-aaai27-eabf3f
- locus-collapse-proof-training-objective
created: '2026-07-17T18:57:47.920454Z'
updated: '2026-07-17T19:00:56.508233Z'
source: https://arxiv.org/html/2604.12632
source_domain: arxiv.org
fetched_at: '2026-07-17T18:57:47.919786Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Full text of Wang, Lou, Wu, Wen, Zhang (CASIA/Tsinghua), CAPO (arXiv:2604.12632v1).
  NOT a joint scalar reward: CAPO replaces GRPO''s reward-only group-relative advantage
  with an uncertainty-aware advantage derived from a pairwise logistic AUC surrogate
  phi_tau(t)=log(1+exp(-t/tau)) applied to t=(lpm(o1)-lpm(o2))(R1-R2), where lpm is
  mean log-probability (perplexity-based) confidence -- i.e. a ranking/discrimination
  surrogate, not a proper scoring rule like Brier/log-score. Central theorem (Thm
  3): the GRPO gradient is mathematically equivalent to AUC optimization with surrogate
  phi(t)=-t, which is PROVEN INCONSISTENT for AUC (via Gao & Zhou 2012''s consistency
  theorem, requiring convex, differentiable, non-increasing phi with phi''(0)<0 --
  linear phi fails this), formally explaining why GRPO improves accuracy while degrading
  relative calibration (AUC). CAPO''s logistic surrogate satisfies the consistency
  theorem and admits a regret bound (Thm 2). Adds a reference-model-based PPL noise-masking
  term m(o) to exclude likely-lucky-guess correct responses and likely-near-correct
  incorrect responses, stabilizing training. Models: Qwen2.5-Math-1.5B and 7B, full
  RL fine-tuning (no LoRA mentioned) via the verl framework on 8xA100 GPUs; 24h (1.5B)
  / 48h (7B) to convergence -- NOT single-GPU feasible as reported. Metrics: AUC-mean
  (relative/discriminative calibration, explicitly NOT ECE -- the paper argues absolute
  calibration/ECE ''does not ensure instance-level discrimination'', e.g. assigning
  0.5 to everything satisfies ECE but is useless) and mean@k/mean@16 accuracy, tracked
  jointly/separately (never fused into one number). Results: AUC-mean improves up
  to 15% (1.5B) / 25% (7B) on AIME2025 with accuracy matching or beating GRPO; inference-time
  scaling accuracy +5% over GRPO. No explicit discussion of confidence-distribution
  collapse to a narrow range, but the masking ablation shows removing it causes entropy
  to keep rising and accuracy to stagnate/degrade -- an adjacent instability failure
  mode.'
---

*Suggested by [[260412632-calibration-aware-policy-optimization-for-reasoning-llms]] — full-text HTML version of previously abstract-only vault note*

Calibration-Aware Policy Optimization for Reasoning LLMs
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2604.12632v1 [cs.LG] 14 Apr 2026
Calibration-Aware Policy Optimization for Reasoning LLMs
Ziqi Wang
1,2
,
Xingzhou Lou
1,2
,
Meiqi Wu
1
,
Zhengqi Wen
3
,
Junge Zhang
1,2
1
National Key Laboratory of Cognition and Decision Intelligence for Complex Systems,
Institution of Automation, Chinese Academy of Sciences
2
School of Artificial Intelligence, University of Chinese Academy of Sciences
3
Beijing National Research Center for Information Science and Technology, Tsinghua University
Correspondence to Junge Zhang:
jgzhang@nlpr.ia.ac.cn
Abstract
Group Relative Policy Optimization (GRPO) enhances LLM reasoning but often induces overconfidence, where incorrect responses yield lower perplexity than correct ones, degrading relative calibration as described by the Area Under the Curve (AUC). Existing approaches either yield limited improvements in calibration or sacrifice gains in reasoning accuracy.
We first prove that this degradation in GRPO-style algorithms stems from their uncertainty-agnostic advantage estimation, which inevitably misaligns optimization gradients with calibration. This leads to improved accuracy at the expense of degraded calibration. We then propose
C
alibration-
A
ware
P
olicy
O
ptimization
(CAPO)
. It adopts a logistic AUC surrogate loss that is theoretically consistent and admits regret bound, enabling uncertainty-aware advantage estimation. By further incorporating a noise masking mechanism, CAPO achieves stable learning dynamics that jointly optimize calibration and accuracy.
Experiments on multiple mathematical reasoning benchmarks show that CAPO-1.5B significantly improves calibration by up to 15% while achieving accuracy comparable to or better than GRPO, and further boosts accuracy on downstream inference-time scaling tasks by up to 5%. Moreover, when allowed to abstain under low-confidence conditions, CAPO achieves a Pareto-optimal precision–coverage trade-off, highlighting its practical value for hallucination mitigation.
Calibration-Aware Policy Optimization for Reasoning LLMs
Ziqi Wang
1,2
,
Xingzhou Lou
1,2
,
Meiqi Wu
1
,
Zhengqi Wen
3
,
Junge Zhang
1,2
1
National Key Laboratory of Cognition and Decision Intelligence for Complex Systems,
Institution of Automation, Chinese Academy of Sciences
2
School of Artificial Intelligence, University of Chinese Academy of Sciences
3
Beijing National Research Center for Information Science and Technology, Tsinghua University
Correspondence to Junge Zhang:
jgzhang@nlpr.ia.ac.cn
1
Introduction
Model calibration is defined as the correlation between a model’s confidence in its answers and the ground truth correctness of those answers
(Geng et al.,
2024
)
. From the era of conventional neural networks to the advent of Large Language Models (LLMs), calibration has consistently been a key focus due to its paramount importance in two aspects
(Xiao et al.,
2025
; Tao et al.,
2024
; Kadavath et al.,
2022
)
.
First, calibration is fundamental to model trustworthiness, enabling reliable uncertainty estimation and abstention to mitigate hallucination—the generation of plausible but factually incorrect assertions. This is particularly vital in high-stakes domains such as finance and healthcare
(Savage et al.,
2025
)
.
Second, confidence estimates are widely used to guide algorithmic decisions.
Multi-agent or cascading systems strengthen model collaboration when a single model is uncertain
(Luo et al.,
2025b
; Warren and Dras,
2025
; Chuang et al.,
2025
)
. Self-paced training prioritizes uncertain samples
(Feng et al.,
2025
; Wang et al.,
2025
)
. And inference-time scaling strategies select candidate responses with high confidence
(Stoisser et al.,
2025
; Vashurin et al.,
2025
; Zhou et al.,
2025b
)
.
All these approaches critically depend on well-calibrated confidence estimates to reflect the true correctness of model outputs.
However, several studies have indicated that Reinforcement Learning from Verifiable Rewards (RLVR) (
Shao et al.,
2024
;
Yu et al.,
2025
;
Zheng et al.,
2025
) can make models overconfident (
Liu et al.,
2025a
;
Kalai et al.,
2025
;
Bereket and Leskovec,
2025
). This often manifests as degradation in relative calibration, where the model outputs fluent but incorrect answers with higher perplexity than correct ones.
Existing efforts to address the overconfidence induced by algorithms such as GRPO
(Shao et al.,
2024
)
and GSPO
(Zheng et al.,
2025
)
primarily rely on heuristic designs. These works often lack quantitative analyses of calibration and, critically, provide no theoretical guarantees for calibration improvement. As a result, they either yield only limited calibration gains, as in CoDaPO
(Zhou et al.,
2025a
)
and CDE
(Dai et al.,
2025
)
, or compromise the model’s overall accuracy, as in SimKO
(Peng et al.,
2025
)
.
To address these issues, we first experimentally show that during the GRPO optimization process, the typical relative calibration metric AUC
(Ling et al.,
2003
; Vashurin et al.,
2025
; Zhou et al.,
2025b
)
progressively worsens as accuracy improves. GRPO-style methods construct advantages from group-wise reward differences. We prove that reward-only sample evaluation induces optimization gradients corresponding to an inconsistent surrogate for calibration optimization
(Gao and Zhou,
2012
)
. Consequently, the learning process is not aligned with calibration improvement, which explains the degradation in experiments.
Building upon this discovery, we propose a novel approach
C
alibration-
A
ware
P
olicy
O
ptimization
(CAPO)
, which (1) adopts uncertainty-aware advantage estimation based on consistent logistic AUC surrogate, enabling joint optimization of calibration and accuracy, and (2) introduces a reference-model-based noise masking mechanism to maintain training stability. In addition to this theoretical justification, a complementary gradient analysis further illustrates how the learning dynamics naturally prioritizes the correction of responses with misaligned confidence, offering additional intuition.
Experimental results on Qwen2.5-Math-1.5B and 7B models demonstrate that CAPO enables stable and joint optimization of both calibration and accuracy. It successfully prevents calibration degradation and attains accuracy that matches or surpasses that of GRPO, as shown in Figure
1
. Our contributions are summarized as follows:
•
We provide
experiment evidence and theoretical explanation
of calibration degradation in GRPO-style algorithms.
•
To address this issue, we introduce a
theoretically grounded and consistent optimization objective
that enables joint optimization of accuracy and calibration.
•
Extensive experiments across six benchmarks
demonstrate significant calibration improvements over GRPO, GSPO, and three additional baselines with preserved accuracy, yielding Pareto-optimal precision–coverage trade-offs for hallucination mitigation and improved inference-time scaling accuracy.
((a))
((b))
((c))
Figure 1:
(a) Comparison of average calibration (measured by AUC-mean) and accuracy (measured by mean@16) across six test benchmarks for our method and all baselines on Qwen2.5-Math-7B; (b)(c) Comparison of calibration dynamics on the validation set during training between our method and GRPO (left) / GSPO (right).
2
Preliminary and Related Work
As our approach builds upon AUC optimization techniques to analyze and mitigate relative calibration degradation in GRPO-style algorithms, this section reviews relevant background on GRPO and calibration, along with related prior work.
2.1
Group Relative Policy Optimization
The reasoning ability of LLMs can be optimized using outcome reward-based Reinforcement Learning, by modeling the generation process as an Markov Decision Process. GRPO achieves this efficiently by computing the advantage value using the reward differences among samples within a group, thereby obviating the need for a value model. For a specific question-answer pair
(
q
,
a
)
(q,a)
, the behavior policy
π
θ
old
\pi_{\theta_{\text{old}}}
samples a group of
G
G
individual responses
{
o
i
}
i
=
1
G
\{o_{i}\}_{i=1}^{G}
. Then, the advantage
A
^
i
,
t
\hat{A}_{i,t}
of the
i
i
-th response is calculated by normalizing the group-level rewards
{
R
i
}
i
=
1
G
\{R_{i}\}_{i=1}^{G}
:
A
^
i
,
t
=
R
i
−
mean
​
(
{
R
i
}
i
=
1
G
)
std
​
(
{
R
i
}
i
=
1
G
)
,
\hat{A}_{i,t}=\frac{R_{i}-\mathrm{mean}(\{R_{i}\}_{i=1}^{G})}{\mathrm{std}(\{R_{i}\}_{i=1}^{G})},
(1)
where
R
=
1
R=1
indicates a correct response and
R
=
0
R=0
indicates an incorrect one.
GRPO adopts a ppo-style clipped objective, together with a directly imposed KL penalty term:
J
GRPO
(
θ
)
=
𝔼
(
q
,
a
)
∼
𝒟
,
{
o
i
}
i
=
1
G
∼
π
θ
old
(
⋅
∣
q
)
[
1
G
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
∑
t
=
1
|
o
i
|
min
⁡
(
r
i
,
t
​
(
θ
)
​
A
^
i
,
t
,
clip
​
(
r
i
,
t
​
(
θ
)
,
1
−
ϵ
,
1
+
ϵ
)
​
A
^
i
,
t
)
−
β
D
KL
(
π
θ
∥
π
ref
)
]
,
\begin{aligned} &J_{\text{GRPO}}(\theta)=\mathbb{E}_{(q,a)\sim\mathcal{D},\,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid q)}\Bigg[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\\
&\qquad\qquad\min\Big(r_{i,t}(\theta)\hat{A}_{i,t},\mathrm{clip}\!\big(r_{i,t}(\theta),1-\epsilon,1+\epsilon\big)\hat{A}_{i,t}\Big)\\
&\qquad\qquad-\beta D_{\mathrm{KL}}\!\left(\pi_{\theta}\,\|\,\pi_{\mathrm{ref}}\right)\Bigg],\end{aligned}
(2)
where
r
i
,
t
​
(
θ
)
=
π
θ
​
(
o
i
,
t
∣
q
,
o
i
,
<
t
)
π
θ
old
​
(
o
i
,
t
∣
q
,
o
i
,
<
t
)
.
r_{i,t}(\theta)=\frac{\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t}\mid q,o_{i,<t})}.
(3)
The clipping operator
clip
​
(
⋅
,
1
−
ϵ
,
1
+
ϵ
)
\mathrm{clip}(\cdot,\,1-\epsilon,\,1+\epsilon)
is introduced
to constrain each policy update, preventing the new policy from drifting too far
away from the previous one by restricting the policy ratio within the interval
[
1
−
ϵ
,
1
+
ϵ
]
[1-\epsilon,\,1+\epsilon]
.
𝔻
KL
​
(
π
θ
∥
π
ref
)
=
π
ref
​
(
o
i
,
t
∣
q
,
o
i
,
<
t
)
π
θ
​
(
o
i
,
t
∣
q
,
o
i
,
<
t
)
−
log
⁡
(
π
ref
​
(
o
i
,
t
∣
q
,
o
i
,
<
t
)
π
θ
​
(
o
i
,
t
∣
q
,
o
i
,
<
t
)
)
−
1
.
\mathbb{D}_{\mathrm{KL}}\!\left(\pi_{\theta}\,\|\,\pi_{\mathrm{ref}}\right)=\frac{\pi_{\mathrm{ref}}(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})}-\log\!\left(\frac{\pi_{\mathrm{ref}}(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})}\right)-1.
(4)
In addition, the KL divergence between the current policy and the reference policy (i.e., the base model) is approximated as Equation (
4
).
While base models are shown to be well-calibrated
(Kalai et al.,
2025
)
, algorithms in the GRPO-like family are observed to cause model calibration collapse, where models generate confident, yet incorrect, responses (
Liu et al.,
2025a
;
Dai et al.,
2025
). Prior RL-based efforts to mitigate this focus on heuristics: reward/advantage shaping (
Dai et al.,
2025
;
Zhou et al.,
2025a
), regularization (
Liu et al.,
2025a
), or label smoothing (
Peng et al.,
2025
).
However, these works rely primarily on qualitative descriptions of calibration degradation. As a result, their heuristic approaches lack theoretical guarantees and generally fail to balance accuracy with calibration preservation.
Our work addresses these deficiencies from a principled quantitative perspective and offers a theoretical justification for calibration optimization, and a proper balance between performance and trustworthiness.
2.2
Calibration Metric
Perplexity (PPL) is a widely used uncertainty indicator in free-form generation
(Stoisser et al.,
2025
; Vashurin et al.,
2025
; Zhou et al.,
2025b
)
:
PPL
​
(
o
)
=
exp
⁡
(
−
1
|
o
|
​
∑
t
=
1
|
o
|
log
⁡
π
​
(
o
t
∣
o
<
t
)
)
.
\text{PPL}(o)=\exp\!\left(-\frac{1}{|o|}\sum_{t=1}^{|o|}\log\pi(o_{t}\mid o_{<t})\right).
(5)
PPL reflects the model’s intrinsic uncertainty without incurring additional computational overhead. In contrast, approaches that elicit explicit confidence via prompting
(Zeng et al.,
2025
; Wen et al.,
2024
; Damani et al.,
2025
)
are often sensitive to prompt design
(Yang et al.,
2024b
)
and self-consistency methods
(Xiong et al.,
2024
; Manakul et al.,
2023
; Tanneru et al.,
2024
)
increase inference costs, making them less general. We therefore consider them outside the scope of this work.
Model calibration can generally be quantified using two families of metrics (
Geng et al.,
2024
):
relative calibration
(e.g., AUC) and
absolute calibration
(e.g., Expected Calibration Error).
Relative calibration emphasizes the model’s ability to
rank
samples—assigning higher confidence to correct responses than to incorrect ones—formalized as (
f
f
denotes the confidence scoring function):
f
​
(
q
,
o
i
)
≤
f
​
(
q
,
o
j
)
⟺
R
i
≤
R
j
,
\displaystyle f(q,{o}_{i})\leq f(q,{o}_{j})\Longleftrightarrow R_{i}\leq R_{j},
(6)
A widely used metric for relative calibration, the Area Under the Curve (AUC)
(Yang and Ying,
2022
; Yuan et al.,
2021
; Zhu et al.,
2022
)
, directly quantifies the probability that a model assigns higher confidence to a correct response than to an incorrect one, thereby capturing the core notion of relative calibration:
AUC
​
(
π
,
q
,
f
)
=
𝔼
o
i
,
o
j
∼
𝒟
​
[
𝕀
​
(
(
R
i
−
R
j
)
​
(
f
​
(
o
i
)
−
f
​
(
o
j
)
)
>
0
)
]
,
\mathrm{AUC}(\pi,q,f)=\mathbb{E}_{o_{i},\,o_{j}\sim\mathcal{D}}\big[\,\mathbb{I}\big((R_{i}-R_{j})(f(o_{i})-f(o_{j}))>0\big)\big],
(7)
where
o
i
o_{i}
and
o
j
o_{j}
denote a randomly sampled pair of responses generated by the model for the same question
q
q
.
We further define AUC-mean as the average AUC score across all questions in a dataset, serving as an overall measure of the model’s calibration performance:
AUC-mean
​
(
π
,
𝒬
,
f
)
=
1
|
𝒬
|
​
∑
q
∈
𝒬
AUC
​
(
π
,
q
,
f
)
,
\text{AUC-mean}(\pi,\mathcal{Q},f)=\frac{1}{|\mathcal{Q}|}\sum_{q\in\mathcal{Q}}\mathrm{AUC}(\pi,q,f),
(8)
where
𝒬
\mathcal{Q}
denotes the set of questions.
Absolute calibration indicates that a model’s returned confidence matches its true correctness likelihood:
P
​
(
R
=
1
∣
f
​
(
q
,
o
)
=
k
)
=
k
.
P(R=1\mid f(q,o)=k)=k.
(9)
In this work, we focus on relative calibration rather than absolute calibration for two reasons: (1) PPL is not directly comparable to correctness probability, making absolute calibration ill-defined, and (2) absolute calibration is an aggregate statistical property that does not ensure instance-level discrimination: for example, assigning identical confidence (e.g., 0.5) to both correct and incorrect responses perfectly satisfy absolute calibration criteria yet fails to distinguish them, limiting its usefulness for downstream tasks such as inference-time scaling. In contrast, relative calibration explicitly enforces pairwise separability.
2.3
Consistency of AUC Optimization
Maximizing the AUC is equivalent to minimizing the risk:
L
​
(
f
)
=
−
AUC
​
(
π
,
q
,
f
)
L(f)=-\mathrm{AUC}(\pi,q,f)
. However, this objective is non-differentiable and non-convex, thus a direct optimization typically results in NP-hard problems (
Gao and Zhou,
2012
).
To address this difficulty, prior work commonly replaces the indicator in Equation (
7
) with a pairwise differentiable surrogate loss:
Ψ
​
(
f
,
o
i
,
o
j
)
=
ϕ
​
[
(
R
i
−
R
j
)
​
(
f
​
(
o
i
)
−
f
​
(
o
j
)
)
]
,
\Psi(f,o_{i},o_{j})=\phi\big[(R_{i}-R_{j})\,(f(o_{i})-f(o_{j}))\big],
(10)
where
ϕ
\phi
is a convex function such as the exponential loss
ϕ
​
(
t
)
=
e
−
t
\phi(t)=e^{-t}
, hinge loss
ϕ
​
(
t
)
=
max
⁡
(
0
,
1
−
t
)
\phi(t)=\max(0,1-t)
,
or squared loss
ϕ
​
(
t
)
=
(
1
−
t
)
2
\phi(t)=(1-t)^{2}
(
Gao et al.,
2013
;
Zhao et al.,
2011
;
Kotlowski et al.,
2011
;
Calders and Jaroszewicz,
2007
;
Charoenphakdee et al.,
2019
).
AUC consistency is defined as follows:
Definition 1
.
The surrogate loss
ϕ
\phi
is said to be
consistent with AUC
if, for every sequence
{
f
⟨
n
⟩
​
(
x
)
}
n
≥
1
\{f^{\langle n\rangle}(x)\}_{n\geq 1}
,
L
ϕ
​
(
f
⟨
n
⟩
)
→
L
ϕ
∗
⇒
L
​
(
f
⟨
n
⟩
)
→
L
∗
,
L_{\phi}\!\left(f^{\langle n\rangle}\right)\to L_{\phi}^{*}\quad\Rightarrow\quad L\!\left(f^{\langle n\rangle}\right)\to L^{*},
where
L
ϕ
L_{\phi}
is the surrogate risk and
L
L
is the true AUC risk.
L
ϕ
∗
L_{\phi}^{*}
and
L
∗
L^{*}
is the corresponding optimal value.
Intuitively, consistency emphasizes the
asymptotic correctness
of a surrogate loss: convergence to the optimal surrogate risk guarantees convergence to the optimal AUC.
For this reason, consistency is widely regarded as one of the most important theoretical properties of surrogate losses.
A sufficient condition for achieving AUC consistency is provided by the following theorem (
Gao and Zhou,
2012
):
Theorem 1
.
The surrogate loss
Ψ
​
(
f
,
o
i
,
o
j
)
\Psi(f,o_{i},o_{j})
is consistent with AUC if
ϕ
:
ℝ
→
ℝ
\phi:\mathbb{R}\rightarrow\mathbb{R}
is a convex, differentiable, and non-increasing function with
ϕ
′
​
(
0
)
<
0
\phi^{\prime}(0)<0
.
It can be readily shown that surrogate losses such as logistic loss and exponential loss are consistent with AUC according to the above theorem.
Furthermore, under the realizable setting where each response is assigned a correct or incorrect label with probability one,
Gao and Zhou (
2012
)
derives the following regret bound, which theoretically guarantees that
minimizing the specified surrogate risk is aligned with optimizing AUC:
Theorem 2
.
For exponential loss, hinge loss, general hinge loss,
q
q
-norm hinge loss, and least square loss, we have
L
​
(
f
)
−
L
∗
≤
L
ϕ
​
(
f
)
−
L
ϕ
∗
,
L(f)-L^{*}\leq L_{\phi}(f)-L_{\phi}^{*},
(11)
and for logistic loss, we have
L
​
(
f
)
−
L
∗
≤
1
ln
⁡
2
​
(
L
ϕ
​
(
f
)
−
L
ϕ
∗
)
.
L(f)-L^{*}\leq\frac{1}{\ln 2}\bigl(L_{\phi}(f)-L_{\phi}^{*}\bigr).
(12)
Prior work on AUC optimization has primarily focused on training better classifiers on static datasets, whereas we study the relationship between reinforcement learning dynamics and relative calibration, and leverage AUC optimization techniques to achieve simultaneous improvements in both calibration and accuracy.
3
Why GRPO-style Objectives Degrade Calibration
Empirical Observation
Prior works (
Yu et al.,
2025
) have shown that the KL regularization term in GRPO is detrimental to optimization, while other studies (
Liu et al.,
2025b
) indicate that removing the standard deviation term in advantage estimation yields an unbiased estimator. Accordingly, we adopt these optimized configurations when implementing GRPO. Empirically, as shown in Figure
1
(b), during GRPO training, the test-set accuracy consistently improves, whereas the AUC-mean steadily deteriorates. Below, we provide a theoretical explanation for this phenomenon.
Theoretical Explanation
At its core, the GRPO gradient is a REINFORCE-style gradient with group relative advantage estimation, as expressed in Equation (
13
).
𝔼
o
1
:
G
∼
𝒟
​
[
1
G
​
∑
i
=
1
G
A
i
^
​
∇
θ
l
​
p
​
m
θ
​
(
o
i
)
]
,
A
i
^
=
R
i
−
R
¯
,
\mathbb{E}_{o_{1:G}\sim\mathcal{D}}\left[\frac{1}{G}\sum_{i=1}^{G}\hat{A_{i}}\nabla_{\theta}lpm_{\theta}(o_{i})\right],\hat{A_{i}}=R_{i}-\bar{R},
(13)
where
l
​
p
​
m
θ
​
(
o
i
)
=
1
|
o
|
​
∑
t
=
1
|
o
|
log
⁡
π
θ
​
(
o
t
∣
o
<
t
)
lpm_{\theta}(o_{i})=\frac{1}{|o|}\sum_{t=1}^{|o|}\log\pi_{\theta}(o_{t}\mid o_{<t})
(see Appendix
A.1
for a detailed derivation).
Consequently, this gradient can be equivalently rewritten as Equation (
14
). Constant scaling factors are omitted for clarity in the subsequent analysis.
𝔼
o
1
:
G
∼
𝒟
​
[
∑
1
≤
i
<
j
≤
G
(
∇
θ
l
​
p
​
m
θ
​
(
o
i
)
−
∇
θ
l
​
p
​
m
θ
​
(
o
j
)
)
​
(
R
i
−
R
j
)
]
.
\mathbb{E}_{o_{1:G}\sim\mathcal{D}}\left[\sum_{1\leq i<j\leq G}\left(\nabla_{\theta}lpm_{\theta}(o_{i})-\nabla_{\theta}lpm_{\theta}(o_{j})\right)\left(R_{i}-R_{j}\right)\right].
(14)
By invoking the unbiasedness property of U-statistics (see Appendix
A.2
for a formal definition), namely that the expectation over a group of samples equals the expectation over a randomly sampled pair, it follows:
𝔼
o
1
,
o
2
∼
𝒟
​
[
(
∇
θ
l
​
p
​
m
θ
​
(
o
1
)
−
∇
θ
l
​
p
​
m
θ
​
(
o
2
)
)
​
(
R
1
−
R
2
)
]
=
∇
θ
𝔼
o
1
,
o
2
∼
𝒟
​
[
(
l
​
p
​
m
θ
​
(
o
1
)
−
l
​
p
​
m
θ
​
(
o
2
)
)
​
(
R
1
−
R
2
)
]
.
\begin{aligned} &\mathbb{E}_{o_{1},o_{2}\sim\mathcal{D}}\Big[(\nabla_{\theta}lpm_{\theta}(o_{1})-\nabla_{\theta}lpm_{\theta}(o_{2}))(R_{1}-R_{2})\Big]\\
=\;&\nabla_{\theta}\mathbb{E}_{o_{1},o_{2}\sim\mathcal{D}}\Big[(lpm_{\theta}(o_{1})-lpm_{\theta}(o_{2}))(R_{1}-R_{2})\Big].\end{aligned}
(15)
Therefore, we have the following result:
Theorem 3
.
The gradient of the GRPO objective coincides with the gradient of the AUC optimization objective with surrogate loss
ϕ
​
(
t
)
=
−
t
\phi(t)=-t
and scoring function
f
=
l
​
p
​
m
f=lpm
(i.e., perplexity). This surrogate loss is inconsistent for AUC optimization (see Appendix
A.3
for the proof).
That is, while optimizing the GRPO objective (which effectively optimizes accuracy), the true AUC is not theoretically guaranteed to improve simultaneously. In practice, GRPO tends to overfit easy samples, leading to a sharpened output distribution, in which the perplexities of both positive and negative samples decrease concurrently, thereby degrading AUC. This theoretical prediction aligns well with our empirical observations shown in Figure
1
(b).
The above analysis extends beyond GRPO to any algorithm relying on reward-only advantage estimator: for instance, Figure
1
(c) demonstrates similar calibration degradation in GSPO, where although optimization is sequence-level, advantage estimation remains reward-based. Evaluating samples
purely based on reward while ignoring uncertainty
inevitably yields an AUC-inconsistent surrogate (proof in Appendix
A.3
), thereby training the model to pursue only high reward values rather than both honesty and accuracy.
4
Method
To address the issues in Section 3, we propose an uncertainty-aware advantage estimation derived from a consistent AUC surrogate.
4.1
Calibration-Aware Policy Optimization
Consistent Surrogate Objective
Building upon the theoretical analysis in Section 3, we propose to replace the inconsistent surrogate loss implicitly induced by GRPO with a
logistic surrogate loss
:
ϕ
τ
​
(
t
)
=
log
⁡
(
1
+
exp
⁡
(
−
t
/
τ
)
)
\phi_{\tau}(t)=\log\big(1+\exp(-t/\tau)\big)
. The temperature parameter
τ
>
0
\tau>0
controls the smoothness of the surrogate. This surrogate is AUC-consistent and admits regret bound (Theorem
2
). It theoretically guarantees that optimizing this surrogate objective leads to an improvement in AUC.
The corresponding policy optimization objective:
J
logistic
​
(
θ
)
=
−
𝔼
o
1
,
o
2
∼
𝒟
​
[
log
⁡
(
1
+
exp
⁡
(
−
t
/
τ
)
)
]
,
J_{\text{logistic}}(\theta)=-\mathbb{E}_{o_{1},o_{2}\sim\mathcal{D}}\Big[\log\big(1+\exp(-t/\tau)\big)\Big],
(16)
where
t
=
(
l
​
p
​
m
θ
​
(
o
1
)
−
l
​
p
​
m
θ
​
(
o
2
)
)
​
(
R
1
−
R
2
)
.
t=\big(lpm_{\theta}(o_{1})-lpm_{\theta}(o_{2})\big)\,\big(R_{1}-R_{2}\big).
(17)
We rewrite the above objective as an expectation over a set of responses and take its gradient:
∇
θ
J
logistic
​
(
θ
)
=
𝔼
o
1
:
G
∼
𝒟
​
[
1
G
​
∑
i
=
1
G
A
i
~
​
∇
θ
l
​
p
​
m
θ
​
(
o
i
)
]
,
\nabla_{\theta}J_{\text{logistic}}(\theta)=\mathbb{E}_{o_{1:G}\sim\mathcal{D}}\left[\frac{1}{G}\sum_{i=1}^{G}\tilde{A_{i}}\nabla_{\theta}lpm_{\theta}(o_{i})\right],
(18)
A
~
i
=
{
−
∑
j
:
R
j
=
0
ϕ
′
​
(
l
​
p
​
m
θ
​
(
o
i
)
−
l
​
p
​
m
θ
​
(
o
j
)
)
,
R
i
=
1
,
∑
j
:
R
j
=
1
ϕ
′
​
(
l
​
p
​
m
θ
​
(
o
j
)
−
l
​
p
​
m
θ
​
(
o
i
)
)
,
R
i
=
0
,
\tilde{A}_{i}=\begin{cases}\displaystyle-\sum_{j:R_{j}=0}\phi^{\prime}\!\big(lpm_{\theta}(o_{i})-lpm_{\theta}(o_{j})\big),&R_{i}=1,\\[6.0pt]
\displaystyle\sum_{j:R_{j}=1}\phi^{\prime}\!\big(lpm_{\theta}(o_{j})-lpm_{\theta}(o_{i})\big),&R_{i}=0,\end{cases}
(19)
where
ϕ
′
​
(
t
)
=
−
σ
​
(
−
t
)
\phi^{\prime}(t)=-\sigma(-t)
, and
σ
​
(
⋅
)
\sigma(\cdot)
denotes the sigmoid function.
Denoising via Reference-Model-Based Masking.
Outcome-based binary rewards fail to assess intermediate reasoning. Consequently, they risk penalizing near-correct logic due to minor errors, while simultaneously reinforcing spurious reasoning that yields correct answers by chance. Such gradient noise can destabilize training or even induce model collapse.
We leverage the inherent calibration of the reference model (i.e., base model) to assess the quality of the reasoning process: high reference-model perplexity (PPL) typically indicates syntactic or logical flaws, whereas low PPL suggests coherence. This approach is that it requires no additional training overhead while significantly improving training stability.
Based on this, we propose a masking strategy to filter noisy signals. Specifically, we exclude correct responses with reference-model PPL exceeding a threshold
ref-high
(likely lucky guesses) and incorrect responses with reference-model PPL below
ref-low
(likely near-correct reasoning penalized as failure). These thresholds are robust and simple to set, empirically corresponding to the upper and lower quartiles of the reference model’s PPL distribution.
Final Objective.
By replacing the advantage estimation in the GRPO objective (
2
) with that in Equation (
19
), and applying noise mask, we obtain the objective under the behavior policy
π
o
​
l
​
d
\pi_{old}
:
J
C
​
A
​
P
​
O
​
(
θ
)
=
𝔼
(
q
,
a
)
∼
𝒟
,
{
o
i
}
i
=
1
G
∼
π
θ
old
(
⋅
∣
q
)
[
1
G
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
∑
t
=
1
|
o
i
|
min
(
r
i
,
t
(
θ
)
A
^
i
C
​
A
​
P
​
O
,
clip
(
r
i
,
t
(
θ
)
,
1
−
ϵ
,
1
+
ϵ
)
A
^
i
C
​
A
​
P
​
O
)
]
,
\begin{aligned} &J_{CAPO}(\theta)\\
&=\mathbb{E}_{(q,a)\sim\mathcal{D},\,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid q)}\Bigg[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\min\\
&\Big(r_{i,t}(\theta)\hat{A}_{i}^{CAPO},\mathrm{clip}\big(r_{i,t}(\theta),1-\epsilon,1+\epsilon\big)\hat{A}_{i}^{CAPO}\Big)\Bigg],\end{aligned}
(20)
where
A
^
i
C
​
A
​
P
​
O
=
m
​
(
o
i
)
​
A
~
i
,
\hat{A}_{i}^{CAPO}=m(o_{i})\tilde{A}_{i}~,
(21)
m
​
(
o
)
=
{
𝕀
​
[
PPL
ref
​
(
o
)
≤
ref-high
]
,
if
​
R
​
(
o
)
=
1
,
𝕀
​
[
PPL
ref
​
(
o
)
≥
ref-low
]
,
if
​
R
​
(
o
)
=
0
.
m(o)=\begin{cases}\mathbb{I}\!\left[\mathrm{PPL}_{\text{ref}}(o)\leq\texttt{ref-high}\right],&\text{if }R(o)=1,\\[6.0pt]
\mathbb{I}\!\left[\mathrm{PPL}_{\text{ref}}(o)\geq\texttt{ref-low}\right],&\text{if }R(o)=0.\end{cases}
(22)
This yields the optimization objective of CAPO. While the PPO-style formulation involves first-order approximation, the core logistic surrogate provides gradients aligned with relative calibration, offering strong theoretical justification. Subsection 4.2 and experiment results further corroborate this alignment.
4.2
Gradient Analysis
Figure 2:
The relationship between advantage and the confidence gap of a correct–wrong response pair.
This subsection conducts a comparative analysis on the gradients between GRPO and our proposed objective function.
The gradient induced by our objective is given by Equation (
18
) (mask term obviated for brevity).
ϕ
′
​
(
t
)
\phi^{\prime}(t)
is illustrated in Figure
2
. As can be seen, its magnitude decreases as the confidence gap between correct and incorrect responses increases. This indicates that the gradient places greater emphasis on correct samples with relatively high PPL and incorrect samples with low PPL, while suppressing the influence of samples that are already confidently and correctly ranked.
Samples near the misranking boundary in terms of reference-model PPL represent instances where the model’s confidence estimates are inaccurate; they also represent highly informative samples in the model’s decision space.
Consequently, these are the key samples for improving both accuracy and AUC. Our method appropriately amplifies their gradients, while the masking mechanism removes update instability caused by extreme noisy samples. In contrast, GRPO assigns the same reward-based advantage to all positive and negative samples within a group, without accounting for their uncertainty or noise.
5
Experiment
Figure 3:
Results of calibration (measured by AUC-mean) and accuracy (measured by mean@16)
for our method and all baselines on Qwen2.5-Math-7B across six test benchmarks.
Model
Ours
GRPO
GSPO
CoDaPO
CDE
SimKO
Qwen2.5-Math-1.5B
25.33
20.33
20.00
21.67
16.67
11.67
Qwen2.5-Math-7B
38.33
33.33
32.21
31.66
31.66
23.33
Table 1:
Inference-time scaling accuracy (%) of different methods on the AIME 2024 and AIME 2025 datasets.
5.1
Setting
Models and Datasets.
We use Qwen2.5-Math-1.5B and Qwen2.5-Math-7B
(Yang et al.,
2024a
)
as the base models. The training and validation sets are constructed by randomly sampling 20k and 240 instances, respectively, from the DeepScaler dataset
(Luo et al.,
2025a
)
. We evaluate all models on six benchmark datasets: AIME 2024, AIME 2025, MATH 500 (
Lightman et al.,
2023
;
Hendrycks et al.,
2021
), AMC 2023, Minerva
(Lewkowycz et al.,
2022
)
, and OlympiadBench
(He et al.,
2024
)
.
Baselines and Methods.
The baselines we compare against fall into two categories: 1) methods designed to improve reasoning capability, including GRPO
(Shao et al.,
2024
)
and GSPO
(Zheng et al.,
2025
)
. 2) methods proposed to address the calibration issues of GRPO, namely CDE
(Dai et al.,
2025
)
, CoDaPO
(Zhou et al.,
2025a
)
, and SimKO
(Peng et al.,
2025
)
. For our method,
τ
\tau
is set to 0.6 for the 1.5B model, and 0.5 for the 7B.
Hyperparameter details are provided in Appendix
B.1
.
Evaluation Metrics.
Following
Yue et al. (
2025
)
, we report mean@8 accuracy on the validation set and mean@16 accuracy on the test set.
Model calibration is evaluated by AUC
(Vashurin et al.,
2025
)
and Hallucination mitigation by the Precision-Coverage curve.
Figure 4:
Precision-Coverage curves of our method and all baselines on six test benchmarks for the Qwen2.5-Math-1.5B (left) and Qwen2.5-Math-7B models (right).
5.2
Main Results
Improved Calibration with Preserved Accuracy
Extensive experiments demonstrate that our method consistently improves calibration (AUC) across all benchmarks without sacrificing accuracy. As shown in Figure
3
and Appendix
B.2
Figure
5
, compared to GRPO and GSPO, our method significantly improves calibration on all test datasets. In particular, on AIME 2025, CAPO increases AUC by approximately 15% for the 1.5B model (from 0.63 to 0.78) and by about 25% for the 7B model (from 0.54 to 0.79). Meanwhile, the mean@8 accuracy achieved by our method is comparable to or even better than that of GRPO, and it attains the highest accuracy on AIME 2024, AIME 2025, and Minerva.
In contrast, other methods aimed at addressing the calibration issue of GRPO provide only limited improvements in AUC and, in some cases, even slightly degrade it on certain datasets. Moreover, none of these methods are able to preserve consistent high accuracy. In particular, SIMKO severely damages accuracy, exhibiting an approximately 12% drop on AMC and a 7.7% drop on AIME 2024 compared to GRPO.
Stable and Consistent Optimization Dynamics
We further present training dynamics to demonstrate the stability and consistency of our method. Figure
1
(b)(c) shows AUC-mean on AIME 2024 and AIME 2025 throughout training. While GRPO and GSPO exhibit a gradual degradation in calibration as optimization proceeds, our method steadily improves AUC over training steps, demonstrating sustained calibration optimization rather than checkpoint-specific effects. Figure
6
in Appendix
B.2
reports validation mean@8 accuracy, where only our method maintains stable performance comparable to GRPO for both 1.5B and 7B models. Together, these results indicate that our approach achieves more stable and reliable optimization behavior throughout training.
Hallucination Mitigation.
We evaluate hallucination mitigation through the precision-coverage trade-off, where a model abstains from answering if its confidence falls below a threshold. Varying this threshold traces a precision-coverage curve that characterizes the fraction of answered questions (coverage) and the accuracy among answered ones (precision). An ideal model should maintain high precision and coverage level. As shown in Figure
4
, our method achieves a Pareto-optimal trade-off, consistently dominating GRPO, GSPO, and other baselines. Notably, while SimKO shows high precision at low coverage due to its ranking capability, its overall lower accuracy causes a sharp precision drop as coverage increases. Conversely, although GRPO matches our accuracy, its inferior calibration leads to consistently lower precision. By simultaneously enhancing calibration and accuracy, our method achieves a more favorable precision–coverage trade-off, enabling reliable hallucination mitigation with minimal abstention.
Impact of Calibration on Inference-Time Scaling
The effectiveness of confidence-based inference-time scaling depends jointly on a model’s accuracy and its calibration quality. We adopt the inference-time scaling algorithm proposed in
Zhou et al. (
2025b
)
(see Appendix
A.4
for implementation details). As shown in Table
1
, our method achieves the highest accuracy under inference-time scaling (5% over GRPO for 1.5B and 7B model), clearly demonstrating the critical role of calibration in inference-time scaling and the effectiveness of our approach.
5.3
Ablation
Sensitivity of Hyperparameters
As detailed in Appendix
B.2
Figure
8
, we conduct sensitivity tests on
τ
∈
{
0.4
,
0.6
,
1.0
}
\tau\in\{0.4,0.6,1.0\}
and different masking intervals. In both cases, the performance impact is marginal, confirming that our method is robust to the specific selection of
τ
\tau
and the
ref-high
/
ref-low
thresholds.
Ablation of the Denoising Strategy
We further compare the performance of our method with and without the masking mechanism. As shown in Appendix
B.2
Figure
9
, removing the masking mechanism causes the model entropy to gradually increase, leading to early stagnation or even degradation in accuracy. In contrast, with the masking mechanism enabled, the model entropy remains stable and accuracy improves steadily. These observations demonstrate that noisy samples can severely disrupt optimization stability, and highlight the effectiveness of the proposed masking mechanism. Furthermore, applying only masking to GRPO fails to improve AUC, demonstrating that a consistent surrogate objective is essential.
6
Conclusion
In this paper, we have quantitatively analyzed and mitigated the calibration degradation induced by GRPO-style algorithms. We show that this degradation stems from reward-only advantage estimation. This estimation causes the gradient unaligned with relative calibration. To address this issue, we propose CAPO, which incorporates uncertainty-aware advantage estimation grounded in a consistent logistic AUC surrogate, together with a denoising mechanism to ensure stable training. Extensive empirical results demonstrate that CAPO trains models that achieve both high accuracy and calibration, leading to superior performance in hallucination mitigation and inference-time scaling.
Limitations
This study mainly evaluates the proposed method on mathematical reasoning benchmarks, which are also the primary focus of GRPO-style Reinforcement Learning with Verifiable Rewards (RLVR) methods. However our method is designed to be broadly applicable to training reasoning models. Its effectiveness on other reasoning tasks such as logical puzzles, commonsense reasoning, and open-domain question answering, remains to be further validated.
Acknowledgment
This work is supported by National Key R&D Program of China (2025ZD0122003), and in part by the Beijing Major Science and Technology Project under Contract no. Z251100008425009.
References
Bereket and Leskovec (2025)
Michael Bereket and Jure Leskovec. 2025.
Uncalibrated reasoning: Grpo induces overconfidence for stochastic outcomes
.
arXiv preprint arXiv:2508.11800
.
Calders and Jaroszewicz (2007)
Toon Calders and Szymon Jaroszewicz. 2007.
Efficient auc optimization for classification
.
In
European Conference on Principles of Data Mining and Knowledge Discovery
, pages 42–53. Springer.
Charoenphakdee et al. (2019)
Nontawat Charoenphakdee, Jongyeong Lee, and Masashi Sugiyama. 2019.
On symmetric losses for learning from corrupted labels
.
In
International Conference on Machine Learning
, pages 961–970.
Chuang et al. (2025)
Yu-Neng Chuang, Prathusha Kameswara Sarma, Parikshit Gopalan, John Boccio, Sara Bolouki, Xia Hu, and Helen Zhou. 2025.
Learning to route llms with confidence tokens
.
Preprint
, arXiv:2410.13284.
Dai et al. (2025)
Runpeng Dai, Linfeng Song, Haolin Liu, Zhenwen Liang, Dian Yu, Haitao Mi, Zhaopeng Tu, Rui Liu, Tong Zheng, Hongtu Zhu, and 1 others. 2025.
Cde: Curiosity-driven exploration for efficient reinforcement learning in large language models
.
arXiv preprint arXiv:2509.09675
.
Damani et al. (2025)
Mehul Damani, Isha Puri, Stewart Slocum, Idan Shenfeld, Leshem Choshen, Yoon Kim, and Jacob Andreas. 2025.
Beyond binary rewards: Training lms to reason about their uncertainty
.
arXiv preprint arXiv:2507.16806
.
Feng et al. (2025)
Qi Feng, Yihong Liu, and Hinrich Schütze. 2025.
Your pretrained model tells the difficulty itself: A self-adaptive curriculum learning paradigm for natural language understanding
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop)
, pages 222–239.
Gao et al. (2013)
Wei Gao, Rong Jin, Shenghuo Zhu, and Zhi-Hua Zhou. 2013.
One-pass auc optimization
.
In
International Conference on Machine Learning
, pages 906–914. PMLR.
Gao and Zhou (2012)
Wei Gao and Zhi-Hua Zhou. 2012.
On the consistency of auc pairwise optimization
.
arXiv preprint arXiv:1208.0645
.
Geng et al. (2024)
Jiahui Geng, Fengyu Cai, Yuxia Wang, Heinz Koeppl, Preslav Nakov, and Iryna Gurevych. 2024.
A survey of confidence estimation and calibration in large language models
.
In
Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
, pages 6577–6595.
He et al. (2024)
Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu, Zhen Thai, Junhao Shen, Jinyi Hu, Xu Han, Yujie Huang, Yuxiang Zhang, and 1 others. 2024.
Olympiadbench: A challenging benchmark for promoting agi with olympiad-level bilingual multimodal scientific problems
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
, pages 3828–3850.
Hendrycks et al. (2021)
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. 2021.
Measuring mathematical problem solving with the math dataset
.
arXiv preprint arXiv:2103.03874
.
Kadavath et al. (2022)
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, and 1 others. 2022.
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Kalai et al. (2025)
Adam Tauman Kalai, Ofir Nachum, Santosh S Vempala, and Edwin Zhang. 2025.
Why language models hallucinate
.
arXiv preprint arXiv:2509.04664
.
Kotlowski et al. (2011)
Wojciech Kotlowski, Krzysztof J Dembczynski, and Eyke Huellermeier. 2011.
Bipartite ranking through minimization of univariate loss
.
In
Proceedings of the 28th International Conference on Machine Learning (ICML-11)
, pages 1113–1120.
Lewkowycz et al. (2022)
Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, and 1 others. 2022.
Solving quantitative reasoning problems with language models
.
Advances in Neural Information Processing Systems
, 35:3843–3857.
Lightman et al. (2023)
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. 2023.
Let’s verify step by step
.
In
The Twelfth International Conference on Learning Representations
.
Ling et al. (2003)
Charles X Ling, Jin Huang, Harry Zhang, and 1 others. 2003.
Auc: a statistically consistent and more discriminating measure than accuracy
.
In
International Joint Conference on Artificial Intelligence
, volume 3, pages 519–524.
Liu et al. (2025a)
Haotian Liu, Shuo Wang, and Hongteng Xu. 2025a.
C
2
GSPG: Confidence-calibrated group sequence policy gradient towards self-aware reasoning
.
arXiv preprint arXiv:2509.23129
.
Liu et al. (2025b)
Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin. 2025b.
Understanding r1-zero-like training: A critical perspective
.
arXiv preprint arXiv:2503.20783
.
Luo et al. (2025a)
Michael Luo, Sijun Tan, Justin Wong, Xiaoxiang Shi, William Y Tang, Manan Roongta, Colin Cai, Jeffrey Luo, Tianjun Zhang, Li Erran Li, and 1 others. 2025a.
Deepscaler: Surpassing o1-preview with a 1.5 b model by scaling rl.
Notion Blog
.
Luo et al. (2025b)
Yichen Luo, Yebo Feng, Jiahua Xu, Paolo Tasca, and Yang Liu. 2025b.
Llm-powered multi-agent system for automated crypto portfolio management
.
Preprint
, arXiv:2501.00826.
Manakul et al. (2023)
Potsawee Manakul, Adian Liusie, and Mark Gales. 2023.
Selfcheckgpt: Zero-resource black-box hallucination detection for generative large language models
.
In
Proceedings of the 2023 conference on empirical methods in natural language processing
, pages 9004–9017.
Peng et al. (2025)
Ruotian Peng, Yi Ren, Zhouliang Yu, Weiyang Liu, and Yandong Wen. 2025.
Simko: Simple pass@ k policy optimization
.
arXiv preprint arXiv:2510.14807
.
Savage et al. (2025)
Thomas Savage, John Wang, Robert Gallo, Abdessalem Boukil, Vishwesh Patel, Seyed Amir Ahmad Safavi-Naini, Ali Soroush, and Jonathan H Chen. 2025.
Large language model uncertainty proxies: discrimination and calibration for medical diagnosis and treatment
.
Journal of the American Medical Informatics Association
, 32(1):139–149.
Schulman et al. (2015)
John Schulman, Sergey Levine, Pieter Abbeel, Michael Jordan, and Philipp Moritz. 2015.
Trust region policy optimization
.
In
International Conference on Machine Learning
, pages 1889–1897. PMLR.
Schulman et al. (2017)
John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. 2017.
Proximal policy optimization algorithms
.
Preprint
, arXiv:1707.06347.
Shao et al. (2024)
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, and 1 others. 2024.
Deepseekmath: Pushing the limits of mathematical reasoning in open language models
.
arXiv preprint arXiv:2402.03300
.
Stoisser et al. (2025)
Josefa Lia Stoisser, Marc Boubnovski Martell, Lawrence Phillips, Gianluca Mazzoni, Lea Mørch Harder, Philip Torr, Jesper Ferkinghoff-Borg, Kaspar Martens, and Julien Fauqueur. 2025.
Towards agents that know when they don’t know: Uncertainty as a control signal for structured reasoning
.
arXiv preprint arXiv:2509.02401
.
Tanneru et al. (2024)
Sree Harsha Tanneru, Chirag Agarwal, and Himabindu Lakkaraju. 2024.
Quantifying uncertainty in natural language explanations of large language models
.
In
International Conference on Artificial Intelligence and Statistics
, pages 1072–1080. PMLR.
Tao et al. (2024)
Shuchang Tao, Liuyi Yao, Hanxing Ding, Yuexiang Xie, Qi Cao, Fei Sun, Jinyang Gao, Huawei Shen, and Bolin Ding. 2024.
When to trust llms: Aligning confidence with response quality
.
arXiv preprint arXiv:2404.17287
.
Vashurin et al. (2025)
Roman Vashurin, Maiya Goloburda, Albina Ilina, Aleksandr Rubashevskii, Preslav Nakov, Artem Shelmanov, and Maxim Panov. 2025.
Uncertainty quantification for llms through minimum bayes risk: Bridging confidence and consistency
.
arXiv preprint arXiv:2502.04964
.
Wang et al. (2025)
Xiaoxuan Wang, Yihe Deng, Mingyu Derek Ma, and Wei Wang. 2025.
Entropy-based adaptive weighting for self-training
.
Preprint
, arXiv:2503.23913.
Warren and Dras (2025)
David Warren and Mark Dras. 2025.
Bi-directional model cascading with proxy confidence
.
Preprint
, arXiv:2504.19391.
Wen et al. (2024)
Bingbing Wen, Chenjun Xu, Robert Wolfe, Lucy Lu Wang, Bill Howe, and 1 others. 2024.
Mitigating overconfidence in large language models: A behavioral lens on confidence estimation and calibration
.
In
NeurIPS 2024 Workshop on Behavioral Machine Learning
.
Xiao et al. (2025)
Jiancong Xiao, Bojian Hou, Zhanliang Wang, Ruochen Jin, Qi Long, Weijie J Su, and Li Shen. 2025.
Restoring calibration for aligned large language models: A calibration-aware fine-tuning approach
.
arXiv preprint arXiv:2505.01997
.
Xiong et al. (2024)
Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan Hooi. 2024.
Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms
.
Preprint
, arXiv:2306.13063.
Yang et al. (2024a)
An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li, Dayiheng Liu, Jianhong Tu, Jingren Zhou, Junyang Lin, Keming Lu, Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang Ren, and Zhenru Zhang. 2024a.
Qwen2.5-math technical report: Toward mathematical expert model via self-improvement
.
Preprint
, arXiv:2409.12122.
Yang et al. (2024b)
Daniel Yang, Yao-Hung Hubert Tsai, and Makoto Yamada. 2024b.
On verbalized confidence scores for llms
.
Preprint
, arXiv:2412.14737.
Yang and Ying (2022)
Tianbao Yang and Yiming Ying. 2022.
Auc maximization in the era of big data and ai: A survey
.
ACM computing surveys
, 55(8):1–37.
Yu et al. (2025)
Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan, Gaohong Liu, Lingjun Liu, and 1 others. 2025.
Dapo: An open-source llm reinforcement learning system at scale
.
arXiv preprint arXiv:2503.14476
.
Yuan et al. (2021)
Zhuoning Yuan, Yan Yan, Milan Sonka, and Tianbao Yang. 2021.
Large-scale robust deep auc maximization: A new surrogate loss and empirical studies on medical image classification
.
In
Proceedings of the IEEE/CVF International Conference on Computer Vision
, pages 3040–3049.
Yue et al. (2025)
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Shiji Song, and Gao Huang. 2025.
Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model?
arXiv preprint arXiv:2504.13837
.
Zeng et al. (2025)
Qingcheng Zeng, Weihao Xuan, Leyang Cui, and Rob Voigt. 2025.
Thinking out loud: Do reasoning models know when they’re right?
arXiv preprint arXiv:2504.06564
.
Zhao et al. (2011)
Peilin Zhao, Steven CH Hoi, Rong Jin, and Tianbo Yang. 2011.
Online auc maximization
.
Zheng et al. (2025)
Chujie Zheng, Shixuan Liu, Mingze Li, Xiong-Hui Chen, Bowen Yu, Chang Gao, Kai Dang, Yuqiong Liu, Rui Men, An Yang, Jingren Zhou, and Junyang Lin. 2025.
Group sequence policy optimization
.
Preprint
, arXiv:2507.18071.
Zhou et al. (2025a)
Zhanke Zhou, Xiangyu Lu, Chentao Cao, Brando Miranda, Tongliang Liu, Bo Han, and Sanmi Koyejo. 2025a.
Codapo: Confidence and difficulty-adaptive policy optimization for post-training language models
.
In
2nd AI for Math Workshop@ ICML 2025
.
Zhou et al. (2025b)
Zhi Zhou, Tan Yuhao, Zenan Li, Yuan Yao, Lan-Zhe Guo, Xiaoxing Ma, and Yu-Feng Li. 2025b.
Bridging internal probability and self-consistency for effective and efficient llm reasoning
.
arXiv preprint arXiv:2502.00511
.
Zhu et al. (2022)
Dixian Zhu, Xiaodong Wu, and Tianbao Yang. 2022.
Benchmarking deep auroc optimization: Loss functions and algorithmic choices
.
arXiv preprint arXiv:2203.14177
.
Appendix A
Additional Proof
A.1
Derivation of the Gradient of the GRPO Objective
Proof idea.
We start from the full PPO clipped surrogate with importance sampling (IS) ratio. As proved by previous works
(Schulman et al.,
2017
,
2015
)
, IS ratio ensures the surrogate uses tokens drawn from the old policy while producing
a unbiased gradient estimate for the current policy (given a fixed state).
The clipping further enforces a trust-region-style constraint, and under a first-order
approximation (small policy update), the clipped surrogate has the same leading-order
gradient direction as the original optimization objective. Hence, PPO’s gradient matches the
REINFORCE-style gradient. GRPO differs from PPO only by replacing the advantage
estimator with a group-wise baseline
A
^
i
=
R
i
−
R
¯
\hat{A}_{i}=R_{i}-\bar{R}
, so substituting this
advantage into the REINFORCE form yields the corresponding GRPO gradient.
Proof
Let
r
t
​
(
θ
)
=
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
π
θ
old
​
(
a
t
∣
s
t
)
r_{t}(\theta)=\frac{\pi_{\theta}(a_{t}\mid s_{t})}{\pi_{\theta_{\mathrm{old}}}(a_{t}\mid s_{t})}
denote the importance sampling ratio.
The PPO clipped objective is
L
PPO
​
(
θ
)
\displaystyle L^{\mathrm{PPO}}(\theta)
=
𝔼
(
s
t
,
a
t
)
∼
π
θ
old
[
min
(
r
t
(
θ
)
A
t
,
\displaystyle=\mathbb{E}_{(s_{t},a_{t})\sim\pi_{\theta_{\mathrm{old}}}}\Big[\min\!\Big(r_{t}(\theta)A_{t},
(23)
clip
(
r
t
(
θ
)
,
1
−
ϵ
,
1
+
ϵ
)
A
t
)
]
.
\displaystyle\qquad\mathrm{clip}(r_{t}(\theta),1-\epsilon,1+\epsilon)\,A_{t}\Big)\Big].
To first order, the gradient of the above off-policy objective reduces to the on-policy REINFORCE-form gradient:
∇
θ
L
PPO
​
(
θ
)
=
∇
θ
𝔼
(
s
t
,
a
t
)
∼
π
θ
​
[
A
t
​
∇
θ
log
⁡
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
]
,
\nabla_{\theta}L^{\mathrm{PPO}}(\theta)=\nabla_{\theta}\mathbb{E}_{(s_{t},a_{t})\sim\pi_{\theta}}\left[A_{t}\,\nabla_{\theta}\log\pi_{\theta}(a_{t}\mid s_{t})\right],
(24)
The GRPO objective is obtained by estimating the advantage in PPO by group-wise reward differences.
Given a group of
G
G
responses
{
o
i
}
i
=
1
G
\{o_{i}\}_{i=1}^{G}
with rewards
{
R
i
}
\{R_{i}\}
, GRPO uses
A
i
~
=
R
i
−
R
¯
,
R
¯
=
1
G
​
∑
i
=
1
G
R
i
.
\tilde{A_{i}}=R_{i}-\bar{R},\qquad\bar{R}=\frac{1}{G}\sum_{i=1}^{G}R_{i}.
(25)
Substituting this
A
i
~
\tilde{A_{i}}
into the REINFORCE-form gradient
24
yields:
𝔼
o
1
:
G
∼
𝒟
​
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
t
=
1
|
o
i
|
(
R
i
−
R
¯
)
​
∇
θ
π
θ
​
(
o
i
,
t
∣
o
i
,
<
t
)
]
.
\mathbb{E}_{o_{1:G}\sim\mathcal{D}}\Bigg[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}(R_{i}-\bar{R})\,\nabla_{\theta}\pi_{\theta}(o_{i,t}\mid o_{i,<t})\Bigg].
(26)
Finally, using the definition
l
​
p
​
m
θ
​
(
o
i
)
=
1
|
o
i
|
​
∑
t
=
1
|
o
i
|
log
⁡
π
θ
​
(
o
i
,
t
∣
o
i
,
<
t
)
,
lpm_{\theta}(o_{i})=\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\log\pi_{\theta}(o_{i,t}\mid o_{i,<t}),
(27)
we can obtain Equation
13
.
A.2
Definition of U-Statistics
Let
{
Z
1
,
Z
2
,
…
,
Z
n
}
\{Z_{1},Z_{2},\dots,Z_{n}\}
be i.i.d. random variables drawn from an underlying distribution
𝒟
\mathcal{D}
.
Consider a symmetric measurable function (kernel)
h
:
𝒵
k
→
ℝ
,
h:\mathcal{Z}^{k}\rightarrow\mathbb{R},
where
k
≥
1
k\geq 1
denotes the order of the kernel and symmetry means that
h
​
(
z
1
,
…
,
z
k
)
=
h
​
(
z
π
​
(
1
)
,
…
,
z
π
​
(
k
)
)
h(z_{1},\dots,z_{k})=h(z_{\pi(1)},\dots,z_{\pi(k)})
for any permutation
π
\pi
of
{
1
,
…
,
k
}
\{1,\dots,k\}
.
Definition (U-statistic).
The
U-statistic
associated with kernel
h
h
is defined as
U
n
≜
(
n
k
)
−
1
​
∑
1
≤
i
1
<
⋯
<
i
k
≤
n
h
​
(
Z
i
1
,
…
,
Z
i
k
)
.
U_{n}\;\triangleq\;\binom{n}{k}^{-1}\sum_{1\leq i_{1}<\dots<i_{k}\leq n}h(Z_{i_{1}},\dots,Z_{i_{k}}).
(28)
The U-statistic
U
n
U_{n}
is an estimator of the population quantity
θ
≜
𝔼
(
Z
1
,
…
,
Z
k
)
∼
𝒟
k
​
[
h
​
(
Z
1
,
…
,
Z
k
)
]
.
\theta\;\triangleq\;\mathbb{E}_{(Z_{1},\dots,Z_{k})\sim\mathcal{D}^{k}}\bigl[h(Z_{1},\dots,Z_{k})\bigr].
(29)
Unbiasedness.
A key property of U-statistics is that they provide unbiased estimators of the target quantity
θ
\theta
.
Proposition 1
(Unbiasedness of U-statistics)
.
For any symmetric kernel
h
h
with finite expectation,
𝔼
​
[
U
n
]
=
θ
.
\mathbb{E}[U_{n}]=\theta.
(30)
Proof.
By linearity of expectation,
𝔼
​
[
U
n
]
\displaystyle\mathbb{E}[U_{n}]
=
(
n
k
)
−
1
​
∑
1
≤
i
1
<
⋯
<
i
k
≤
n
𝔼
​
[
h
​
(
Z
i
1
,
…
,
Z
i
k
)
]
.
\displaystyle=\binom{n}{k}^{-1}\sum_{1\leq i_{1}<\dots<i_{k}\leq n}\mathbb{E}\bigl[h(Z_{i_{1}},\dots,Z_{i_{k}})\bigr].
(31)
Since
{
Z
i
}
\{Z_{i}\}
are i.i.d., each summand has expectation
θ
\theta
.
There are exactly
(
n
k
)
\binom{n}{k}
such terms, which yields
𝔼
​
[
U
n
]
=
(
n
k
)
−
1
⋅
(
n
k
)
⋅
θ
=
θ
.
\mathbb{E}[U_{n}]=\binom{n}{k}^{-1}\cdot\binom{n}{k}\cdot\theta=\theta.
(32)
∎
Relation to the main text.
In the main text, Equation (
14
) can be viewed as a U-statistic with kernel order
k
=
2
k=2
.
Consequently, it is an unbiased estimator of the expectation in Equation (
15
).
A.3
Completion of the Proof of Theorem 3
Inconsistency of
ϕ
​
(
t
)
=
−
t
\phi(t)=-t
for AUC optimization.
AUC depends only on the
ordering
induced by the scoring function.
In particular, for any
α
>
0
\alpha>0
, scaling the scores does not change AUC:
AUC
​
(
f
)
=
AUC
​
(
α
​
f
)
.
\mathrm{AUC}(f)~=~\mathrm{AUC}(\alpha f).
(33)
However, the surrogate risk with
ϕ
​
(
t
)
=
−
t
\phi(t)=-t
is
scale-sensitive
and
unbounded
:
ℒ
−
t
​
(
α
​
f
)
=
−
𝔼
​
[
α
​
f
​
(
Z
+
)
−
α
​
f
​
(
Z
−
)
]
=
α
​
ℒ
−
t
​
(
f
)
.
\mathcal{L}_{-t}(\alpha f)=-\mathbb{E}\bigl[\alpha f(Z^{+})-\alpha f(Z^{-})\bigr]=\alpha\,\mathcal{L}_{-t}(f).
(34)
Take any nontrivial scoring function
f
f
with
ℒ
−
t
​
(
f
)
<
0
\mathcal{L}_{-t}(f)<0
and
A
​
U
​
C
​
(
f
)
<
1
AUC(f)<1
(not optimal). Consider the sequence
f
m
=
α
m
​
f
f_{m}=\alpha_{m}f
with
α
m
↑
+
∞
\alpha_{m}\uparrow+\infty
.
Then
AUC
​
(
f
m
)
=
AUC
​
(
f
)
\mathrm{AUC}(f_{m})=\mathrm{AUC}(f)
for all
m
m
by (
33
),
but
ℒ
−
t
​
(
f
m
)
→
−
∞
\mathcal{L}_{-t}(f_{m})\to-\infty
by (
34
).
Hence, one can drive the surrogate objective arbitrarily close to its infimum
without improving (or even changing) AUC.
Therefore, minimizing the
ϕ
​
(
t
)
=
−
t
\phi(t)=-t
surrogate does not guarantee approaching
an AUC-optimal scorer, i.e., this surrogate is not consistent for AUC optimization.
Generalizing to Reward-Only Advantage Estimators.
It is worth noting that this result is not limited to GRPO, but applies to all algorithms that employ reward-only advantage estimators. Since the objectives induced by this class of advantage estimators are always linear with respect to the confidence function, they necessarily satisfy the property in (
34
). As a result, similar scaling counterexamples can be constructed to show that these objectives are not consistent AUC surrogate losses.
Configuration
Value
train_batch_size
128
ppo_mini_batch_size
64
max_prompt_length
1050
max_response_length
3046
ref-high
2.5
ref-low
1.05
τ
\tau
(1.5B model)
0.6
τ
\tau
(7B model)
0.5
ϵ
\epsilon
0.2
learning rate
1
×
10
−
6
1\times 10^{-6}
entropy_coeff
0
kl_loss_coef
0
rollout.n
8
validation.rollout.n
16
rollout.temperature
1.0
validation.temperature
1.0
total_steps(for 1.5B)
600
total_steps(for 7B)
400
Table 2:
Key hyperparameter settings used in our experiments.
A.4
Pseudocode of the Inference-Time Scaling Algorithm
The inference-time scaling algorithm in Algorithm
1
is a direct instantiation of the
Perplexity Consistency
principle
proposed in prior work
Zhou et al.,
2025b
. In our implementation, N is 16.
The core assumption of Perplexity Consistency is that if the model is well-calibrated, responses corresponding to the correct
answer should, on average, exhibit lower perplexity (higher likelihood)
than incorrect ones.
Instead of selecting the single response with minimum perplexity,
the proposed method aggregates confidence at the
answer level
.
All responses that yield the same extracted final answer are grouped,
and their probabilities are summed to form an aggregated confidence score.
This aggregation achieves two desirable properties:
•
Self-consistency
: answers that are repeatedly produced
by the model with high likelihood are reinforced.
•
Noise robustness
: low-probability or spurious generations
contribute negligibly to the final decision.
Importantly, the entire procedure relies solely on the model’s
endogenous confidence
, quantified by perplexity.
As such, it constitutes a lightweight yet effective form of inference-time
scaling that leverages both the model’s calibration quality and reasoning ability.
Algorithm 1
Perplexity-Consistency Based Inference-Time Scaling
1:
Input:
question
q
q
, number of samples
N
N
, model
π
θ
\pi_{\theta}
2:
Output:
final predicted answer
a
^
\hat{a}
3:
Sample
N
N
independent responses
{
y
i
}
i
=
1
N
∼
π
θ
(
⋅
∣
q
)
\{y_{i}\}_{i=1}^{N}\sim\pi_{\theta}(\cdot\mid q)
4:
for
i
←
1
i\leftarrow 1
to
N
N
do
5:
Extract final answer
a
i
a_{i}
from response
y
i
y_{i}
6:
Compute token-level average log-probability:
7:
ℓ
i
←
1
|
y
i
|
​
∑
t
=
1
|
y
i
|
log
⁡
p
θ
​
(
y
i
,
t
∣
y
i
,
<
t
,
q
)
\ell_{i}\leftarrow\frac{1}{|y_{i}|}\sum_{t=1}^{|y_{i}|}\log p_{\theta}\!\big(y_{i,t}\mid y_{i,<t},q\big)
8:
end
for
9:
Group responses by identical extracted answers:
10:
𝒢
​
(
a
)
←
{
i
∣
a
i
=
a
}
\mathcal{G}(a)\leftarrow\{\,i\mid a_{i}=a\,\}
11:
for all
candidate answers
a
a
do
12:
Compute aggregated confidence:
13:
C
​
(
a
)
←
∑
i
∈
𝒢
​
(
a
)
exp
⁡
(
ℓ
i
)
C(a)\leftarrow\sum_{i\in\mathcal{G}(a)}\exp(\ell_{i})
14:
end
for
15:
a
^
←
arg
⁡
max
a
⁡
C
​
(
a
)
\hat{a}\leftarrow\arg\max_{a}C(a)
16:
return
a
^
\hat{a}
Appendix B
Additional Experiment details
B.1
Experimental Setup
Experimental configurations for the 1.5B and 7B models are detailed in Table
2
. All methods share these identical settings, with method-specific hyperparameters following their original papers. For our method, we set the temperature parameter
τ
\tau
to
0.6
0.6
for 1.5B model and 0.5 for 7B model,
ref-high
and
ref-low
to the lower and upper quartiles of the reference model’s PPL distribution over correct and incorrect responses, respectively. Experiments were conducted using the verl framework on 8
×
\times
A100 GPUs. Training a single CAPO/GRPO run to convergence takes approximately 24 hours for the 1.5B model and 48 hours for the 7B model.
B.2
Additional Experimental Results
Additional Experimental Results of Qwen2.5-Math-1.5B model and Accuracy Curves
Figure
5
demonstrates the complete experimental results of Qwen2.5-Math-1.5B for all methods over six benchmarks. Our method achieves a significant improvement in calibration over all baselines on the 1.5B model, while maintaining accuracy gains that are comparable to or even surpass those of GRPO. In contrast, other methods either yield only limited improvements in calibration or incur a degradation in accuracy. Figure
6
shows the accuracy of all methods on the validation set as a function of training steps. Our method exhibits accuracy improvements comparable to GRPO on both model scales.
Ablation of Hyperparameters
As illustrated in Figure
8
, our method exhibits low sensitivity to the variation of the hyperparameter
τ
\tau
across different values (
τ
=
0.4
,
0.6
,
1.0
\tau=0.4,0.6,1.0
). Similarly, when adjusting the values of
ref-high
and
ref-low
to tighten the masking range from
[
1.05
,
2.5
]
[1.05,2.5]
to
[
1.25
,
2.1
]
[1.25,2.1]
, Figure
9
(b) demonstrates that the performance remains similarly insensitive to these hyperparameter settings.Figure
7
shows that applying the masking mechanism to GRPO alone does not improve calibration, highlighting the importance of the calibration-aware advantage estimator.
Figure 5:
Results of calibration (measured by AUC-mean) and accuracy (measured by mean@16)
for our method and all baselines on Qwen2.5-Math-1.5B across six test benchmarks.
((a))
((b))
Figure 6:
Accuracy trajectories on the validation set over training steps for our method and all baselines on the Qwen2.5-Math-1.5B (left) and Qwen2.5-Math-7B models (right).
((a))
((b))
Figure 7:
Ablation studies on the effectiveness of applying the masking mechanism alone to GRPO. The results show that the mask by itself does not improve calibration, highlighting the necessity of the calibration-aware advantage estimator.
((a))
((b))
Figure 8:
Ablation studies on the sensitivity of accuracy improvement curves (a) and calibration metrics (b) to the hyperparameter
τ
\tau
.
Ablation of Noise Masking mechanism
Comparing the performance of the algorithm with and without the masking mechanism, it can be observed from Figure
9
(a) that removing the mask leads to a gradual increase in model entropy, causing the accuracy (acc) to stagnate prematurely or even decline. In contrast, with the inclusion of the masking mechanism, the model’s entropy remains stable, and the accuracy exhibits a steady improvement. These observations underscore the disruptive impact of noisy data on experimental stability and optimization signals, as well as the effectiveness of the masking mechanism.
((a))
((b))
Figure 9:
Ablation studies on the impact of the noise-masking mechanism on training stability (a)
and the sensitivity to the
ref-high
and
ref-low
hyperparameters (b).