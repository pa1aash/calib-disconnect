---
title: 'When Words Fall Short: Iterative Synergy Between Verbalized Reasoning and
  Hidden Features for LLM Confidence Estimation'
id: when-words-fall-short-iterative-synergy-between-verbalized-reasoning-and-hidden
tags:
- code-llm-confidence-positioning-d82d00
- w3-3
created: '2026-11-10T08:23:52.115806Z'
updated: '2026-11-10T08:25:57.622820Z'
source: https://arxiv.org/html/2609.34454
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:52.115192Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2609.34454 full text: argues a dedicated hidden-state confidence estimator
  (linear head on last-token hidden state, trained with Brier loss) substantially
  outperforms RL-trained verbalized confidence, and proposes IPoET, alternating policy
  optimization with estimator updates. Qwen and Llama backbones (incl. Qwen3-8B-Base,
  Llama-3.1-8B-Instruct); HotpotQA and Big-Math training, in-domain and OOD eval;
  AUROC and Brier. Code generation appears only as an intro example; no code evaluation
  or execution labels. Bears on L2 (estimator beats verbal) outside code.'
---

When Words Fall Short: Iterative Synergy Between Verbalized Reasoning and Hidden Features for LLM Confidence Estimation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2609.34454v1 [cs.CL] 28 Sep 2026
When Words Fall Short: Iterative Synergy Between Verbalized Reasoning and Hidden Features for LLM Confidence Estimation
Yekun Xu   Ante Wang   Jingyi Ren   Xuanyi Chen
Weizhi Ma
Yang Liu
†
†
thanks:
Corresponding authors.
Email:
{mawz, liuyang2011}@tsinghua.edu.cn
Affiliation:
College of AI, Tsinghua University, Beijing, China
Affiliation:
Institute for AI Industry Research (AIR), Tsinghua University, Beijing, China
Affiliation:
Dept. of Comp. Sci. & Tech., Institute for AI, Tsinghua University, Beijing, China
Abstract
Confidence estimation is crucial for developing trustworthy large language models (LLMs), with most methods following estimator-based or verbalization-based paradigms. While recent research increasingly focuses on improving verbalized self-reports of confidence, we challenge the prevailing view that this approach surpasses independent confidence estimators. Our empirical study shows that a dedicated confidence estimator can substantially outperform verbalized confidence, indicating that LLMs’ internal representations contain richer confidence signals. Building on this finding, we propose
I
terative
Po
licy-
E
stimator
T
raining (
IPoET
), a framework that synergizes the complementary strengths of verbalized reasoning traces and informative representations. IPoET alternates policy optimization with estimator updating, integrating estimator-derived confidence feedback into policy learning and refreshing the estimator on new policy rollouts. Experiments across diverse datasets and Qwen and Llama backbones demonstrate that, by iteratively exploiting richer hidden features and adapting to the evolving policy distribution, IPoET consistently outperforms both estimator- and verbalization-based baselines in-domain and achieves superior or comparable results across all out-of-domain metrics. For more details, refer to
https://github.com/xyk829/ipoet
.
1
Introduction
Large language models (LLMs) have become increasingly capable across a wide range of challenging tasks, such as reasoning, code generation, and planning
(
Jaech et al., 2024
;
Guo et al., 2025
;
Jimenez et al., 2024
;
Xiao et al., 2024
)
. However, higher accuracy does not necessarily mean that models can correctly assess whether their outputs should be trusted. LLMs frequently generate hallucinated or incorrect answers with unwarranted confidence
(
Xiong et al., 2024
;
Anh-Hoang et al., 2025
)
. This lack of reliable confidence estimation severely limits the practical deployment of LLMs in high-stakes domains such as medicine, law, and finance, where decision-making errors carry significant consequences
(
Li et al., 2024
;
Siino et al., 2025
;
Li et al., 2023
;
Kumaran et al., 2026b
)
.
Existing research on confidence estimation can generally be categorized into two paradigms:
(i)
Estimator-based methods
. These methods train independent models or lightweight probing heads to exploit features embedded within the model’s hidden states
(
Beigi et al., 2024
;
Mahaut et al., 2024
)
.
(ii)
Verbalization-based methods
. This paradigm leverages the linguistic reasoning of LLMs and derives verbalized confidence scores through prompting or training
(
Yang et al., 2024
;
Li et al., 2026b
)
. Recent work on this task has increasingly focused on RL-based verbalization methods, with several studies reporting that verbalized confidence outperforms estimator-based methods
(
Damani et al., 2025
;
Bani-Harouni et al., 2025
;
Ma et al., 2026
;
Zhang et al., 2026a
)
.
However, revisiting this comparison leads us to a different finding: with validation-based checkpoint selection, an independent confidence estimator can substantially outperform state-of-the-art verbalized confidence in both in-domain and out-of-domain evaluations, as shown in Figure
1(a)
. We find that estimator overfitting can bias comparisons in favor of verbalized confidence, as continued optimization can reduce training error while degrading confidence estimation on unseen data. These results establish estimators trained with overfitting control as a strong confidence estimation paradigm that deserves further attention.
This finding also highlights the complementary strengths and limitations of estimator- and verbalization-based approaches. Hidden features within model representations are essential for accurate confidence estimation, yet they cannot be easily translated into natural language
(
Kumaran et al., 2026a
)
. At the same time, decoupling the estimator from the main policy limits its ability to fully utilize the advanced reasoning capabilities of contemporary LLMs, which have proven effective for confidence estimation and various other tasks. This raises a central question:
Can we harness the advantages of both paradigms to achieve more reliable confidence estimation?
To answer this, we propose
I
terative
Po
licy-
E
stimator
T
raining (
IPoET
) for confidence estimation. It alternates between two stages:
(i) optimizing the policy with an objective that incorporates estimator feedback while preserving task accuracy, and
(ii) updating the estimator to leverage hidden states encoding reasoning traces from the current policy.
This process enables policy reasoning to provide richer confidence signals that the estimator can extract from its hidden representations, while keeping the estimator aligned with the evolving policy distribution. Consequently, this co-adaptation yields stronger confidence estimation than isolated optimization.
We evaluate IPoET across multiple mathematical reasoning and question-answering datasets using different backbone models. Compared to both estimator- and verbalization-based approaches, our method consistently achieves superior or competitive performance on confidence estimation metrics while preserving task performance. Furthermore, IPoET generalizes effectively to out-of-domain tasks. We also investigate algorithmic variants, such as joint training, to provide deeper insights into the underlying effectiveness of our method.
Our contributions are summarized as follows:
•
We revisit the comparison between estimator- and verbalization-based paradigms, showing that estimators can substantially outperform verbalized confidence and revealing estimator overfitting as an important factor underlying prior discrepancies.
•
We propose IPoET, an iterative training framework that harnesses the complementary advantages of LLM verbalized reasoning and rich hidden features for confidence estimation.
•
Across diverse datasets and backbone models, IPoET outperforms baselines on in-domain confidence estimation while achieving superior or comparable out-of-domain performance.
(a)
(b)
Figure 1:
(a) In-domain and out-of-domain comparison of confidence estimator and verbalized confidence using AUROC and Brier score. Percentages denote relative improvements over verbalized confidence.
(b) Estimator performance across training budgets: Brier scores on a training subset, an in-domain validation set, and an out-of-domain test set illustrate overfitting with extended training.
2
Empirical Study
In this section, we revisit two confidence estimation paradigms: estimator-based and verbalization-based. We begin by highlighting their implementations in Section
2.1
, before examining how estimator training dynamics affect their relative performance in Section
2.2
.
2.1
Preliminaries
Task Definition
: Given a prompt
x
x
from a dataset
𝒟
\mathcal{D}
, an LLM
π
θ
\pi_{\theta}
generates a response
y
y
consisting of an optional reasoning trace
τ
\tau
and a final answer
a
a
. We define the correctness label as
z
=
𝕀
[
a
≡
a
∗
]
z=\mathbb{I}[a\equiv a^{*}]
, where
a
∗
a^{*}
is the ground-truth answer. Confidence estimation aims to assign a score
c
∈
[
0
,
1
]
c\in[0,1]
representing the likelihood that
a
a
is correct.
Estimator-based approaches.
These approaches utilize an independent confidence estimator
s
ϕ
s_{\phi}
. While prior work typically employs either a lightweight probing head or an entire model as the estimator, we follow
Malladi et al. (2023)
and adopt the latter for its superior performance
(
Ni et al., 2025
)
. Specifically,
s
ϕ
s_{\phi}
processes the input
x
x
and response
y
y
to predict a confidence score
c
c
by applying a linear head to the hidden state of the last non-padding token, denoted as
h
h
:
c
=
s
ϕ
​
(
x
,
y
)
=
clip
⁡
(
𝐰
⊤
​
h
+
b
,
0
,
1
)
c=s_{\phi}(x,y)=\operatorname{clip}(\mathbf{w}^{\top}h+b,0,1)
, where
𝐰
\mathbf{w}
and
b
b
denote the weights and bias.
We train the estimator on collected rollouts
𝒟
est
=
{
(
x
,
y
,
z
)
}
\mathcal{D}_{\mathrm{est}}=\{(x,y,z)\}
using a mean squared error (MSE) loss:
ℒ
est
=
𝔼
(
x
,
y
,
z
)
∼
𝒟
est
​
[
(
s
ϕ
​
(
x
,
y
)
−
z
)
2
]
.
\mathcal{L}_{\mathrm{est}}=\mathbb{E}_{(x,y,z)\sim\mathcal{D}_{\mathrm{est}}}\left[(s_{\phi}(x,y)-z)^{2}\right].
(1)
Previous studies show that critical features for confidence estimation are distributed across intermediate layers
(
Azaria and Mitchell, 2023
;
Subramani et al., 2025
)
.
Through end-to-end gradient optimization, the final hidden state learns to distill and consolidate these confidence signals scattered throughout the network.
Verbalization-based approaches.
These approaches leverage the strong capabilities of recent LLMs to generate an answer
a
a
alongside verbalized confidence
c
c
via a natural language reasoning trace
τ
\tau
. To jointly optimize both variables, this paradigm typically employs RL to search for reasoning traces
τ
\tau
that provide a more rigorous rationale for inferring a precise confidence
c
c
. Following RLCR
(
Damani et al., 2025
)
, we augment the correctness reward in conventional RLVR
(
Shao et al., 2024
)
with a Brier-style term over the verbalized confidence:
𝒥
verb
(
θ
)
=
𝔼
x
∼
𝒟
,
(
y
,
c
)
∼
π
θ
(
⋅
|
x
)
[
z
−
(
c
−
z
)
2
]
.
\mathcal{J}_{\mathrm{verb}}(\theta)=\mathbb{E}_{x\sim\mathcal{D},\,(y,c)\sim\pi_{\theta}(\cdot|x)}\left[z-(c-z)^{2}\right].
(2)
Recent studies have claimed that RL-trained verbalized confidence outperforms independently trained confidence estimators
(
Ma et al., 2026
;
Zhang et al., 2026a
)
.
For example, in comparisons with their respective estimator baselines, RLCR highlights calibration gains, particularly under distribution shift
(
Damani et al., 2025
)
, while Rewarding Doubt emphasizes improved discrimination and generalization
(
Bani-Harouni et al., 2025
)
.
2.2
Estimator-Based vs. Verbalization-Based
We next revisit the comparison between estimator-based and verbalization-based confidence estimation. We hypothesize that estimator overfitting may explain the previously claimed advantage of verbalized confidence. An evaluation at a single training endpoint may obscure this effect, as it does not reveal how training and validation performance evolve during optimization. To investigate this possibility, we examine checkpoints throughout full-parameter tuning, testing whether continued optimization yields sustained improvements or reverses earlier gains in generalization. We use the HotpotQA training set and track Brier scores on a 5K training subset, a held-out in-domain validation set, and the out-of-domain benchmarks described in Section
4.1
.
As shown in Figure
1(b)
, the training Brier score decreases continuously, while the in-domain validation score first decreases and then rises. The out-of-domain score exhibits a more pronounced deterioration, increasing from an early minimum of 0.184 to 0.258 with extended training. This divergence provides evidence of overfitting. For subsequent estimator training, we adopt the
1
×
1\times
configuration without additional checkpoint selection, as it achieves in-domain validation performance close to that of
2
×
2\times
with half the budget. Consistent with this analysis, the full-scale experiments in Section
4.2
further demonstrate strong estimator performance with overfitting control.
Our comparison shows that estimator-based confidence estimation can substantially outperform RL-trained verbalized confidence. As shown in Figure
1(a)
, the confidence estimator improves AUROC by 0.161 in-domain and 0.078 out-of-domain, while reducing Brier score by 0.049 and 0.020, respectively. These results challenge the view that verbalized confidence is inherently stronger than hidden-state estimation, highlighting the value of representation-level confidence evidence.
Beyond clarifying the relative performance of the two paradigms, this finding also leads us to examine their complementary capabilities. While estimators extract features from hidden states, RL-based verbalized methods connect confidence expression with the reasoning process
(
Tao et al., 2024
)
. These distinct advantages suggest a natural opportunity to combine both approaches, which we explore through iterative updates of generation and confidence estimation in the next section.
Figure 2:
Overview of IPoET. The framework alternates between policy and estimator optimization.
In the policy-update stage
, the confidence estimator is frozen and provides confidence estimates to form an estimator-derived term, combined with format and accuracy rewards for GRPO.
In the estimator-update stage
, the policy is frozen to generate correctness-labeled rollouts for updating the estimator via supervised regression. Across iterations, the policy refines reasoning-oriented generation while the estimator adapts to the evolving policy distribution.
3
Method
We propose IPoET, an iterative framework that connects reasoning-oriented policy training with hidden-state confidence estimation, as illustrated in Figure
2
. To better transfer confidence signals into policy learning, we adopt reinforcement learning as the optimization mechanism, enabling estimator-derived reward to directly shape the model’s generated reasoning. We describe the training procedure in Section
3.1
, and then define the estimator-derived reward in Section
3.2
.
3.1
Iterative Policy-Estimator Training
Let
π
θ
0
\pi_{\theta_{0}}
denote the base model. We first apply standard RLVR
(
Lambert et al., 2024
)
to obtain an initial policy
π
θ
1
\pi_{\theta_{1}}
. This warm-up stage provides a stable output format for answer extraction and correctness verification. Rollouts from
π
θ
1
\pi_{\theta_{1}}
are then used to train the confidence estimator
s
ϕ
1
s_{\phi_{1}}
with the supervised regression objective in Eq.
1
.
After initialization, IPoET proceeds in alternating rounds. At iteration
t
t
, it performs two steps.
Step 1:
Freeze estimator
s
ϕ
t
s_{\phi_{t}}
, update policy
π
θ
t
\pi_{\theta_{t}}
.
The estimator
s
ϕ
t
s_{\phi_{t}}
is held fixed while the policy
π
θ
t
\pi_{\theta_{t}}
is updated to
π
θ
t
+
1
\pi_{\theta_{t+1}}
with GRPO
(
Shao et al., 2024
)
using a reward that combines format, accuracy, and an estimator-derived confidence term, as detailed in Section
3.2
. This step incorporates representation-level confidence feedback into policy learning, encouraging the policy to generate reasoning that makes answer correctness easier to infer from the estimator’s hidden representations.
Step 2:
Freeze policy
π
θ
t
+
1
\pi_{\theta_{t+1}}
, update estimator
s
ϕ
t
s_{\phi_{t}}
.
Since the updated policy may induce a different response distribution, we sample fresh rollouts from
π
θ
t
+
1
\pi_{\theta_{t+1}}
, assign correctness labels using task-specific answer verification, and update the estimator to
s
ϕ
t
+
1
s_{\phi_{t+1}}
with the same regression objective in Eq.
1
. Across estimator updates, we use the fixed training budget established in Section
2.2
to reduce overfitting and maintain estimator reliability on the evolving policy distribution.
Rather than relying on a static estimator, IPoET alternates policy improvement with estimator refinement on current-policy rollouts, allowing the policy and estimator to co-adapt across rounds. The estimator serves both as a confidence predictor and as a source of feedback for reasoning generation.
3.2
Reward Function
Following the notation in Section
2.1
, IPoET optimizes the policy using a reward with three components:
R
IPoET
​
(
x
,
y
,
z
,
ϕ
)
=
R
fmt
​
(
y
)
+
R
acc
​
(
z
)
+
R
est
​
(
x
,
y
,
z
,
ϕ
)
.
R_{\mathrm{IPoET}}(x,y,z;\phi)=R_{\mathrm{fmt}}(y)+R_{\mathrm{acc}}(z)+R_{\mathrm{est}}(x,y,z;\phi).
(3)
Here,
R
fmt
R_{\mathrm{fmt}}
maintains the required output structure, and
R
acc
​
(
z
)
=
z
R_{\mathrm{acc}}(z)=z
rewards responses whose final answers match the ground-truth answer.
The key component is the estimator-derived reward
R
est
R_{\mathrm{est}}
, which introduces hidden-state confidence estimation into policy training. For each rollout, the current estimator produces a confidence score from its internal representation. IPoET converts this representation-level estimate into a policy reward through a negative Brier-style objective:
R
est
​
(
x
,
y
,
z
,
ϕ
)
=
−
(
s
ϕ
​
(
x
,
y
)
−
z
)
2
.
R_{\mathrm{est}}(x,y,z;\phi)=-\left(s_{\phi}(x,y)-z\right)^{2}.
(4)
This term gives higher reward when estimated confidence matches correctness, thereby discouraging overconfidence and underconfidence. Thus, the estimator directly guides policy optimization using hidden-state confidence estimates, without requiring the policy to verbalize a confidence score.
4
Experiments
4.1
Experimental Setup
Datasets.
We focus on tasks with well-defined correctness criteria to support reliable confidence evaluation across diverse reasoning and knowledge settings. Following the experimental setup of RLCR
(
Damani et al., 2025
)
, we utilize the processed HotpotQA and Big-Math datasets as our training data, derived respectively from the modified HotpotQA distractor data
(
Yang et al., 2018
)
and the filtered Big-Math problems
(
Albalak et al., 2025
)
. For evaluation, we consider benchmarks that reflect different sources of uncertainty in confidence estimation. They fall into three categories: (i) factual question answering, including HotpotQA, TriviaQA
(
Joshi et al., 2017
)
, and SimpleQA
(
Wei et al., 2024
)
; (ii) commonsense and expert-level knowledge reasoning, including CommonsenseQA
(
Talmor et al., 2019
)
and GPQA
(
Rein et al., 2023
)
; and (iii) mathematical reasoning, including MATH-500
(
Hendrycks et al., 2021
)
, GSM8K
(
Cobbe et al., 2021
)
, and Big-Math.
Evaluation Metrics.
We evaluate each method along two dimensions (details in Appendix
B
). For task performance, we report Accuracy, computed using dataset-specific evaluation procedures, including exact match,
math_verify
, and LLM-as-a-judge
(
Zheng et al., 2023
)
evaluation. Given the short and objective answer formats of these benchmarks, we use automated evaluation without additional human annotation. For confidence estimation, we report Area Under the Receiver Operating Characteristic Curve (AUROC)
(
Bradley, 1997
)
, Brier score
(
Glenn and others, 1950
)
, and Expected Calibration Error (ECE)
(
Guo et al., 2017
)
. AUROC evaluates how confidence scores order correct and incorrect predictions, reflecting the ranking quality of confidence estimates. Brier score averages the squared error between the predicted confidence and the binary correctness label, capturing how accurate each confidence estimate is at the instance level. ECE measures the mismatch between predicted confidence and empirical accuracy after grouping predictions into confidence bins.
Baselines.
We compare with the initial model and the following representative baselines, focusing on single-pass confidence estimation without additional inference-time sampling.
RLVR
optimizes the policy with a binary answer reward
(
Shao et al., 2024
)
and verbalizes confidence only during evaluation.
Answer-Prob
averages the generation probabilities of all tokens in the final answer
(
Jiang et al., 2021
)
, while
P(True)
prompts the model to judge whether its own answer is correct and uses the probability of the positive label as confidence
(
Kadavath et al., 2022
)
.
RLVR + Estimator
trains a confidence estimator on RLVR-generated outputs and correctness labels, following the training protocol in Section
2
.
RLCR
trains the model to generate both an answer and verbalized confidence by optimizing a reward that combines answer correctness with a negative Brier score
(
Damani et al., 2025
)
.
RLCR (Step-aligned)
uses the RLCR objective with the same number of training steps as IPoET, serving as a control for the effect of additional training.
RLCR + Estimator
applies a confidence estimator to RLCR-generated outputs. We also evaluate commercial frontier models and observe limitations in their verbalized confidence estimation; see Appendix
C
.
Implementation Details.
Our method is built on the verl framework
(
Sheng et al., 2025
)
, with GRPO as the RL algorithm
(
Shao et al., 2024
)
. We use Qwen3-8B-Base
(
Yang et al., 2025
)
as the main backbone and evaluate Llama-3.1-8B-Instruct
(
Grattafiori et al., 2024
)
to assess generality. For a fair comparison, we reimplement the RL-based baselines in the same training pipeline while preserving their objectives and core design. All methods use the same training data within each setting. For each trainable baseline, we report results from the checkpoint with the best held-out in-domain validation performance. Following common practice in RL training for reasoning models
(
Guo et al., 2025
;
Hu et al., 2026
)
, we initialize the policy from the backbone model and train it without KL regularization. Training details, including the prompt template, are provided in Appendix
A
.
Table 1:
Main results for models trained on HotpotQA and Big-Math. We report accuracy and confidence-estimation metrics, including AUROC, Brier score, and ECE, for Qwen and Llama backbones. For models trained on HotpotQA, we report results on HotpotQA and a six-dataset OOD average.
For models trained on Big-Math, we report a Math average over MATH-500, GSM8K, and Big-Math, together with a five-dataset OOD average. Best and second-best results for all metrics under each backbone are marked in
bold
and
underlined
, respectively.
HotpotQA
OOD Averaged
Acc.
↑
\uparrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
ECE
↓
\downarrow
Acc.
↑
\uparrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
ECE
↓
\downarrow
Qwen3-8B-Base
51.6%
0.555
0.363
0.343
56.5%
0.556
0.359
0.345
⌞
\llcorner
RLVR
62.2%
0.523
0.376
0.376
62.3%
0.518
0.357
0.358
⌞
\llcorner
Answer-Prob
62.2%
0.661
0.359
0.360
62.3%
0.548
0.340
0.327
⌞
\llcorner
P(True)
62.2%
0.543
0.308
0.260
62.3%
0.588
0.304
0.314
⌞
\llcorner
RLVR + Estimator
62.2%
0.757
0.195
0.087
62.3%
0.724
0.184
0.184
⌞
\llcorner
RLCR
61.0%
0.596
0.244
0.100
61.4%
0.646
0.204
0.171
⌞
\llcorner
RLCR (Step-aligned)
65.3%
0.606
0.263
0.205
61.6%
0.690
0.210
0.188
⌞
\llcorner
RLCR + Estimator
61.0%
0.753
0.201
0.081
61.4%
0.719
0.207
0.224
⌞
\llcorner
IPoET (ours)
63.3%
0.800
0.184
0.107
62.3%
0.738
0.170
0.146
Llama-3.1-8B-Instruct
45.9%
0.577
0.461
0.469
45.9%
0.606
0.413
0.424
⌞
\llcorner
RLVR + Estimator
61.6%
0.772
0.198
0.110
51.0%
0.746
0.180
0.161
⌞
\llcorner
RLCR
59.1%
0.603
0.248
0.121
50.2%
0.674
0.217
0.175
⌞
\llcorner
IPoET (ours)
64.6%
0.781
0.188
0.101
51.5%
0.737
0.182
0.152
Math
OOD Averaged
Acc.
↑
\uparrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
ECE
↓
\downarrow
Acc.
↑
\uparrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
ECE
↓
\downarrow
Qwen3-8B-Base
62.8%
0.568
0.313
0.290
51.9%
0.562
0.389
0.382
⌞
\llcorner
RLVR
74.4%
0.517
0.255
0.255
52.9%
0.569
0.417
0.424
⌞
\llcorner
Answer-Prob
74.4%
0.709
0.235
0.239
52.9%
0.576
0.420
0.424
⌞
\llcorner
P(True)
74.4%
0.490
0.366
0.380
52.9%
0.645
0.275
0.237
⌞
\llcorner
RLVR + Estimator
74.4%
0.862
0.107
0.037
52.9%
0.684
0.217
0.197
⌞
\llcorner
RLCR
73.7%
0.625
0.184
0.115
52.8%
0.600
0.282
0.272
⌞
\llcorner
RLCR (Step-aligned)
73.8%
0.633
0.181
0.120
41.7%
0.536
0.361
0.347
⌞
\llcorner
RLCR + Estimator
73.7%
0.828
0.126
0.068
52.8%
0.662
0.249
0.249
⌞
\llcorner
IPoET (ours)
74.2%
0.878
0.100
0.040
50.9%
0.698
0.206
0.183
Llama-3.1-8B-Instruct
42.7%
0.591
0.501
0.512
43.7%
0.611
0.410
0.423
⌞
\llcorner
RLVR + Estimator
53.8%
0.789
0.167
0.085
45.3%
0.616
0.235
0.216
⌞
\llcorner
RLCR
50.6%
0.570
0.246
0.165
44.6%
0.616
0.219
0.179
⌞
\llcorner
IPoET (ours)
56.5%
0.824
0.152
0.061
45.2%
0.622
0.226
0.191
4.2
Main Results
IPoET achieves strong overall in-domain performance.
Table
1
shows that IPoET achieves the highest AUROC and the lowest Brier score across all four in-domain settings, covering both datasets and backbone models. Compared with RLVR + Estimator, IPoET achieves AUROC gains and Brier score reductions of up to 0.043 and 0.015, respectively, highlighting its strengths in confidence discrimination and calibration. A paired bootstrap test on the Qwen3-8B-Base HotpotQA setting shows statistically significant improvements over RLVR + Estimator in both AUROC (
p
=
0.0006
p=0.0006
) and Brier score (
p
=
0.0317
p=0.0317
). IPoET also achieves the highest task accuracy and the lowest ECE in both Llama settings, with competitive results on both measures for Qwen3. Together, these results support the value of iterative policy–estimator interaction for improving confidence estimation. The baseline comparisons further corroborate our empirical study: with validation-based checkpoint selection, RLVR + Estimator outperforms RLCR in AUROC, Brier score, and ECE across all four in-domain settings, suggesting that hidden-state estimators can exploit correctness-related information not fully captured by explicit self-reports. Despite the additional verbalized confidence analysis in RLCR-generated outputs, RLCR + Estimator is worse than RLVR + Estimator on most metrics. One possible explanation is that explicit self-assessment may dilute correctness-related signals in the original reasoning trace and introduce extra noise into the estimator’s hidden representations.
IPoET achieves competitive out-of-domain performance.
On benchmarks outside the training domain, IPoET ranks first or second on all confidence-estimation metrics. Under both HotpotQA and Big-Math training, it achieves the highest out-of-domain AUROC and lowest Brier score and ECE on Qwen. On Llama, IPoET achieves the lowest ECE under HotpotQA training and the highest AUROC under Big-Math training, while remaining close to the best baseline results on the other metrics. These results suggest that the benefits of IPoET extend beyond the training domain, although improvements over existing methods vary across evaluation settings.
IPoET’s gains stem from iterative policy-estimator coupling rather than additional training alone.
RLCR (Step-aligned) extends RLCR to the same number of training updates as IPoET, providing a controlled comparison for assessing continued optimization. Additional RLCR training does not yield consistent gains and can degrade out-of-domain performance under Big-Math training. This contrast suggests that the benefit of additional optimization depends on how the policy and confidence estimator are jointly refined, rather than on the number of updates alone. IPoET therefore makes more effective use of the extra training budget for confidence estimation.
Table 2:
Comparison between joint and iterative training on HotpotQA. Iterative training improves accuracy, AUROC, and Brier score in both in-domain and out-of-domain settings. Values in parentheses denote changes relative to joint training.
Setting
Strategy
Accuracy
↑
\uparrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
In-domain
Joint
60.5%
0.773
0.209
Iterative
63.3%
(+2.8 pp)
0.800
(+0.027)
0.184
(-0.025)
Out-of-domain
Joint
58.4%
0.737
0.180
Iterative
62.3%
(+3.9 pp)
0.738
(+0.001)
0.170
(-0.010)
4.3
Ablation and Analysis
Effect of Estimator Feedback and Iterative Updates.
We first analyze how the two stages of IPoET contribute to its performance. As shown in Figure
4.3
, with the estimator
s
ϕ
1
s_{\phi_{1}}
fixed, updating the policy from
π
θ
1
\pi_{\theta_{1}}
to
π
θ
2
\pi_{\theta_{2}}
increases AUROC and reduces Brier score in both in-domain and out-of-domain evaluations. ECE also decreases in both settings, with the in-domain score falling from 0.087 to 0.055. Alongside these gains, in-domain accuracy increases by 1.1 percentage points, while out-of-domain accuracy is preserved. The first-stage results are consistent with the intended role of estimator feedback: rather than treating confidence estimation solely as a prediction task over given responses, IPoET uses the fixed estimator’s prediction errors to shape response generation, encouraging outputs that better support reliable correctness assessment. Moreover, computing this reward from estimator predictions rather than verbalized confidence allows IPoET to guide policy optimization with the more accurate confidence estimates observed in our empirical study. With the policy held fixed, the subsequent estimator update further improves confidence quality, especially out of domain. These step-wise gains indicate complementary roles of the two stages: policy optimization incorporates estimator feedback into generation behavior, while estimator refinement adapts confidence estimation to the updated policy distribution. Together, these results support the iterative interaction between policy and estimator underlying IPoET.
Figure 3:
Step-wise effects of IPoET, showing that both policy and estimator
updates progressively improve confidence estimation.
Table 3:
Effect of alternating-update granularity under Big-Math training
with the same update budget and data allocation.
Best results are shown in
bold
.
Iteration
[-0.5pt]
Setting
In-domain
Out-of-domain
AUROC
↑
\uparrow
Brier
↓
\downarrow
AUROC
↑
\uparrow
Brier
↓
\downarrow
2
×
200
2{\times}200
0.878
0.100
0.698
0.206
4
×
100
4{\times}100
0.873
0.102
0.696
0.198
Joint vs. Iterative Training.
We next examine how estimator feedback should be incorporated into policy optimization by comparing two training designs developed in our work. Table
2
shows that iterative training yields higher AUROC and lower Brier score than joint training across both evaluation settings, indicating better confidence estimation. More importantly, joint optimization degrades answer accuracy relative to the starting policy, whereas iterative training improves task performance, further supporting the design of IPoET. In joint training, the estimator must learn from a changing policy distribution while the policy is guided by an under-adapted estimator, potentially introducing interference between policy learning and estimator fitting. IPoET instead separates these roles across rounds: the estimator adapts to current policy outputs before being used to construct the confidence term in the next policy update, enabling more stable confidence-aware training.
Inference Efficiency and Estimator Overhead.
IPoET introduces an additional confidence estimator with the same backbone architecture as the policy. To assess its practical computational cost, we measure total end-to-end inference time on 1,000 HotpotQA examples. IPoET requires 500.38 s, compared with 554.60 s for RLCR, representing a 9.8% reduction. Although the estimator increases the parameter count, it scores each response in a single forward pass, whereas RLCR performs additional autoregressive generation for confidence-related reasoning. Overall, this trade-off allows IPoET to remain inference-efficient in practice despite the additional model component.
Granularity of Alternating Updates.
A natural question is whether IPoET benefits from more frequent alternation between policy and estimator updates. To isolate this factor, we compare two schedules with the same update budget and data allocation:
2
×
200
2{\times}200
uses two longer update phases, while
4
×
100
4{\times}100
splits each corresponding phase into two shorter ones. Table
4.3
shows that more frequent alternation does not consistently improve confidence estimation. The
2
×
200
2{\times}200
schedule performs better in three of the four comparisons, including AUROC in both in-domain and out-of-domain evaluations and in-domain Brier score. These results suggest that sustained optimization within each phase better supports policy–estimator adaptation than switching more often. When each phase becomes too short, the policy may not fully absorb the estimator feedback before the estimator is updated again, yielding smaller gains in confidence estimation.
Figure 4:
Round-wise comparison of in-domain and out-of-domain AUROC and Brier score under Big-Math training. Blue shading marks the configuration used in our main experiments (Round 2).
Impact of Iteration Rounds.
We finally examine whether extending IPoET to additional rounds further improves confidence estimation. The trend in Figure
4
shows that the transition from Round 1 to Round 2 substantially improves both AUROC and Brier score on in-domain and out-of-domain evaluations, confirming the benefit of the first complete policy–estimator refinement cycle. Round 3 brings only a marginal improvement in out-of-domain AUROC, while in-domain AUROC remains unchanged and Brier score slightly increases in both settings. This pattern suggests diminishing returns from further alternation in this setting. We therefore adopt the Round 2 configuration for our main experiments, balancing confidence discrimination and calibration quality while avoiding an additional training round.
5
Related Work
Confidence Estimation from Implicit Information.
These methods estimate confidence from implicit information produced during inference or internal computation. One line of work studies model-internal representations for confidence estimation. LLM hidden activations have been shown to encode factuality and truthfulness-related information
(
Chen et al., 2024
)
, motivating lightweight probes or classifiers trained on internal states
(
Azaria and Mitchell, 2023
;
Servedio et al., 2025
)
. Subsequent work extends this view to reasoning settings, including hidden-state verification of reasoning steps and perturbation-based confidence probing
(
Zhang et al., 2025
;
Khanmohammadi et al., 2025
)
. Recent work exploits internal representations by aggregating hidden-state information across multiple layers during self-evaluation for uncertainty estimation
(
Xiao et al., 2026
)
. Another line derives implicit confidence from output probabilities or self-evaluation signals: Answer-Prob uses token likelihoods or answer probabilities as confidence proxies
(
Jiang et al., 2021
;
Gupta et al., 2024
)
, while P(True) asks the model to judge whether its own answer is correct and uses the probability of a positive judgment
(
Kadavath et al., 2022
)
. However, these signals are usually used to score fixed outputs, whereas IPoET converts internal-representation estimates into feedback for policy training.
Verbalized Confidence Estimation.
Verbalized methods require the model to express confidence explicitly through natural language. Prompting-based approaches elicit numerical or linguistic confidence alongside generated answers or reasoning
(
Xiong et al., 2024
;
Yang et al., 2024
)
. Training-based approaches further teach models to produce uncertainty rationales or calibrated confidence scores, such as self-reflective rationales in SaySelf
(
Xu et al., 2024
)
, listener-aware confidence markers in LACIE
(
Stengel-Eskin et al., 2024
)
, and calibration-aware on-policy distillation
(
Zhang et al., 2026b
)
. Studies of reasoning models show that chain-of-thought generation can improve confidence expression
(
Yoon et al., 2026
)
, motivating recent RL-based methods that optimize verbalized confidence with calibration-oriented rewards, such as Brier-style or logarithmic scoring objectives
(
Damani et al., 2025
;
Bani-Harouni et al., 2025
)
. However, expressed confidence remains sensitive to prompt formulation, answer-dependent self-assessment, and placement of confidence statements relative to the answer
(
Xia et al., 2025
;
Seo et al., 2025
;
Guo et al., 2026
;
Li et al., 2026a
)
. IPoET avoids relying on such explicit confidence expression by deriving confidence from an internal-representation estimator, while still benefiting from reasoning-oriented generation.
6
Conclusion
This work revisits two major paradigms for LLM confidence estimation: estimator-based and verbalization-based methods. We demonstrate that estimators can substantially outperform verbalized confidence when overfitting is controlled, partly explaining the differing conclusions in prior comparisons. Nevertheless, traditional estimators fail to utilize the strong reasoning capabilities of contemporary LLMs. To combine the strengths of both paradigms, we propose IPoET (Iterative Policy-Estimator Training). This framework enables the estimator to extract richer features from its hidden states using policy-generated reasoning traces, while the policy learns to produce more informative content for the estimator. Compared with the baselines, IPoET shows improved in-domain confidence estimation, comparable or better out-of-domain performance, and competitive task accuracy across multiple reasoning and question-answering datasets. These results highlight the value of internal representations for reliable confidence estimation and suggest that iterative policy-estimator training is a promising direction for building more trustworthy reasoning models.
AI use statement
We used generative AI tools to improve the wording, grammar, and fluency of the manuscript and refine the presentation of scientific figures. These tools were not used to implement the proposed method, generate datasets, or prove mathematical claims. All reported numerical results and the data underlying the figures were obtained from experiments conducted by the authors. We reviewed all AI-assisted work. Specifically, we checked textual revisions for technical accuracy and consistency with our intended meaning. The revised figures were also verified against the underlying experimental data. We take responsibility for the final content of this work, including text, claims or artifacts produced with the aid of generative AI.
Ethics statement
We are committed to adhering to the ICLR Code of Ethics. Our study relies solely on publicly available benchmark datasets for mathematical reasoning and question answering, without recruiting human participants or collecting private personal data. We believe this work raises no direct ethical risks beyond standard concerns associated with LLM research and use.
Reproducibility statement
To support reproducibility, we provide our source code at
https://github.com/xyk829/ipoet
. The training procedure and reward function are described in Sections
3.1
and
3.2
, respectively. Our experiments use publicly available backbone models and benchmark datasets, with the experimental setup described in Section
4.1
. Additional training details and the prompt template are provided in Appendix
A
, while evaluation procedures and metric definitions are detailed in Appendix
B
.
References
Albalak
et al.
(2025)
A. Albalak, D. Phung, N. Lile, R. Rafailov, K. Gandhi, L. Castricato, A. Singh, C. Blagden, V. Xiang, D. Mahan,
et al.
Big-math: a large-scale, high-quality math dataset for reinforcement learning in language models
.
arXiv preprint arXiv:2502.17387
.
Cited by:
§4.1
.
Anh-Hoang
et al.
(2025)
D. Anh-Hoang, V. Tran, and L. Nguyen
Survey and analysis of hallucinations in large language models: attribution to prompting strategies or model behavior
.
Frontiers in Artificial Intelligence
8
,
pp. 1622292
.
Cited by:
§1
.
Anthropic (2025)
Anthropic
The claude 4 model family: opus, sonnet, and haiku
.
Note:
https://www.anthropic.com/research/claude-haiku-4-5
Cited by:
Appendix C
.
Azaria and Mitchell (2023)
A. Azaria and T. Mitchell
The internal state of an llm knows when it’s lying
.
In
Findings of the Association for Computational Linguistics: EMNLP 2023
,
pp. 967–976
.
Cited by:
§2.1
,
§5
.
Bani-Harouni
et al.
(2025)
D. Bani-Harouni, C. Pellegrini, P. Stangel, E. Özsoy, K. Zaripova, N. Navab, and M. Keicher
Rewarding doubt: a reinforcement learning approach to calibrated confidence expression of large language models
.
arXiv preprint arXiv:2503.02623
.
Cited by:
§1
,
§2.1
,
§5
.
Beigi
et al.
(2024)
M. Beigi, Y. Shen, R. Yang, Z. Lin, Q. Wang, A. Mohan, J. He, M. Jin, C. Lu, and L. Huang
Internalinspector i2: robust confidence estimation in llms through internal states
.
In
Findings of the association for computational linguistics: EMNLP 2024
,
pp. 12847–12865
.
Cited by:
§1
.
Bereket and Leskovec (2025)
M. Bereket and J. Leskovec
Uncalibrated reasoning: grpo induces overconfidence for stochastic outcomes
.
arXiv preprint arXiv:2508.11800
.
Cited by:
Appendix A
.
Bradley (1997)
A. P. Bradley
The use of the area under the roc curve in the evaluation of machine learning algorithms
.
Pattern recognition
30
(
7
),
pp. 1145–1159
.
Cited by:
§4.1
.
Chen
et al.
(2024)
C. Chen, K. Liu, Z. Chen, Y. Gu, Y. Wu, M. Tao, Z. Fu, and J. Ye
INSIDE: llms’ internal states retain the power of hallucination detection
.
arXiv preprint arXiv:2402.03744
.
Cited by:
§5
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
§4.1
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
Appendix A
,
Appendix B
,
§1
,
§2.1
,
§2.1
,
§4.1
,
§4.1
,
§5
.
DeepSeek (2026)
DeepSeek
DeepSeek v4 preview release
.
Note:
https://api-docs.deepseek.com/news/news260424
Cited by:
Appendix C
.
Glenn
et al.
(1950)
W. B. Glenn
et al.
Verification of forecasts expressed in terms of probability
.
Monthly weather review
78
(
1
),
pp. 1–3
.
Cited by:
§4.1
.
Google DeepMind (2025)
Google DeepMind
Gemini 3 flash
.
Note:
https://deepmind.google/models/gemini/flash/
Model description page
Cited by:
Appendix C
.
Grattafiori
et al.
(2024)
A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan,
et al.
The llama 3 herd of models
.
arXiv preprint arXiv:2407.21783
.
Cited by:
§4.1
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
§4.1
.
Guo
et al.
(2025)
D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi,
et al.
Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning
.
arXiv preprint arXiv:2501.12948
.
Cited by:
§1
,
§4.1
.
Guo
et al.
(2026)
J. Guo, S. Gu, M. Jin, C. Spanos, and J. Lavaei
LLMs should express uncertainty explicitly
.
arXiv preprint arXiv:2604.05306
.
Cited by:
§5
.
Gupta
et al.
(2024)
N. Gupta, H. Narasimhan, W. Jitkrittum, A. S. Rawat, A. K. Menon, and S. Kumar
Language model cascades: token-level uncertainty and beyond
.
arXiv preprint arXiv:2404.10136
.
Cited by:
§5
.
Hendrycks
et al.
(2021)
D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
Measuring mathematical problem solving with the math dataset
.
arXiv preprint arXiv:2103.03874
.
Cited by:
§4.1
.
Hu
et al.
(2026)
J. Hu, Y. Zhang, Q. Han, D. Jiang, X. Zhang, and H. Shum
Open-reasoner-zero: an open source approach to scaling up reinforcement learning on the base model
.
Advances in Neural Information Processing Systems
38
,
pp. 162239–162262
.
Cited by:
§4.1
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
Jiang
et al.
(2021)
Z. Jiang, J. Araki, H. Ding, and G. Neubig
How can we know when language models know? on the calibration of language models for question answering
.
Transactions of the Association for Computational Linguistics
9
,
pp. 962–977
.
Cited by:
§4.1
,
§5
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
.
Joshi
et al.
(2017)
M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer
Triviaqa: a large scale distantly supervised challenge dataset for reading comprehension
.
In
Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 1601–1611
.
Cited by:
§4.1
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
§4.1
,
§5
.
Khanmohammadi
et al.
(2025)
R. Khanmohammadi, E. Miahi, M. Mardikoraem, S. Kaur, I. Brugere, C. Smiley, K. S. Thind, and M. M. Ghassemi
Calibrating llm confidence by probing perturbed representation stability
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
pp. 10459–10525
.
Cited by:
§5
.
Kumaran
et al.
(2026a)
D. Kumaran, A. Conmy, F. Barbero, S. Osindero, V. Patraucean, and P. Velickovic
How do llms compute verbal confidence
.
arXiv preprint arXiv:2603.17839
.
Cited by:
§1
.
Kumaran
et al.
(2026b)
D. Kumaran, S. M. Fleming, L. Markeeva, J. Heyward, A. Banino, M. Mathur, R. Pascanu, S. Osindero, B. De Martino, P. Veličković,
et al.
Competing biases underlie overconfidence and underconfidence in llms
.
Nature Machine Intelligence
,
pp. 1–14
.
Cited by:
§1
.
Lambert
et al.
(2024)
N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu,
et al.
Tulu 3: pushing frontiers in open language model post-training
.
arXiv preprint arXiv:2411.15124
.
Cited by:
§3.1
.
Li
et al.
(2026a)
C. Li, X. Hu, S. Zheng, J. Zhou, and C. Chen
ORCE: order-aware alignment of verbalized confidence in large language models
.
arXiv preprint arXiv:2605.12446
.
Cited by:
§5
.
Li
et al.
(2024)
J. Li, Y. Lai, W. Li, J. Ren, M. Zhang, X. Kang, S. Wang, P. Li, Y. Zhang, W. Ma,
et al.
Agent hospital: a simulacrum of hospital with evolvable medical agents
.
arXiv preprint arXiv:2405.02957
.
Cited by:
§1
.
Li
et al.
(2026b)
Y. Li, M. Xiong, J. Wu, and B. Hooi
Conftuner: training large language models to express their confidence verbally
.
Advances in Neural Information Processing Systems
38
,
pp. 53484–53513
.
Cited by:
§1
.
Li
et al.
(2023)
Y. Li, S. Wang, H. Ding, and H. Chen
Large language models in finance: a survey
.
In
Proceedings of the fourth ACM international conference on AI in finance
,
pp. 374–382
.
Cited by:
§1
.
Ma
et al.
(2026)
Z. Ma, X. Wen, B. Cao, Y. Lu, H. Lin, J. Yang, M. He, X. Han, and L. Sun
Decoupling reasoning and confidence: resurrecting calibration in reinforcement learning from verifiable rewards
.
arXiv preprint arXiv:2603.09117
.
Cited by:
§1
,
§2.1
.
Mahaut
et al.
(2024)
M. Mahaut, L. Aina, P. Czarnowska, M. Hardalov, T. Müller, and L. Màrquez
Factual confidence of llms: on reliability and robustness of current estimators
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 4554–4570
.
Cited by:
§1
.
Malladi
et al.
(2023)
S. Malladi, T. Gao, E. Nichani, A. Damian, J. D. Lee, D. Chen, and S. Arora
Fine-tuning language models with just forward passes
.
Advances in Neural Information Processing Systems
36
,
pp. 53038–53075
.
Cited by:
§2.1
.
Ni
et al.
(2025)
S. Ni, K. Bi, J. Guo, M. Tang, J. Wu, Z. Han, and X. Cheng
Annotation-efficient universal honesty alignment
.
arXiv preprint arXiv:2510.17509
.
Cited by:
§2.1
.
OpenAI (2025)
OpenAI
GPT-5 system card
.
Note:
https://openai.com/index/gpt-5-system-card
Cited by:
Appendix C
.
Rein
et al.
(2023)
D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman
Gpqa: a graduate-level google-proof q&a benchmark
.
arXiv preprint arXiv:2311.12022
.
Cited by:
§4.1
.
Seo
et al.
(2025)
K. J. Seo, S. Lim, and T. Kim
ADVICE: answer-dependent verbalized confidence estimation
.
arXiv preprint arXiv:2510.10913
.
Cited by:
§5
.
Servedio
et al.
(2025)
G. Servedio, A. De Bellis, D. Di Palma, V. W. Anelli, and T. Di Noia
Are the hidden states hiding something? testing the limits of factuality-encoding capabilities in llms
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 6089–6104
.
Cited by:
§5
.
Shao
et al.
(2024)
Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu,
et al.
Deepseekmath: pushing the limits of mathematical reasoning in open language models
.
arXiv preprint arXiv:2402.03300
.
Cited by:
§2.1
,
§3.1
,
§4.1
,
§4.1
.
Sheng
et al.
(2025)
G. Sheng, C. Zhang, Z. Ye, X. Wu, W. Zhang, R. Zhang, Y. Peng, H. Lin, and C. Wu
Hybridflow: a flexible and efficient rlhf framework
.
In
Proceedings of the Twentieth European Conference on Computer Systems
,
pp. 1279–1297
.
Cited by:
§4.1
.
Siino
et al.
(2025)
M. Siino, M. Falco, D. Croce, and P. Rosso
Exploring llms applications in law: a literature review on current legal nlp approaches
.
IEEE Access
13
,
pp. 18253–18276
.
Cited by:
§1
.
Stengel-Eskin
et al.
(2024)
E. Stengel-Eskin, P. Hase, and M. Bansal
LACIE: listener-aware finetuning for calibration in large language models
.
Advances in Neural Information Processing Systems
37
,
pp. 43080–43106
.
Cited by:
§5
.
Subramani
et al.
(2025)
N. Subramani, J. Eisner, J. Svegliato, B. Van Durme, Y. Su, and S. Thomson
MICE for cats: model-internal confidence estimation for calibrating agents with tools
.
In
Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
,
pp. 12362–12375
.
Cited by:
§2.1
.
Talmor
et al.
(2019)
A. Talmor, J. Herzig, N. Lourie, and J. Berant
Commonsenseqa: a question answering challenge targeting commonsense knowledge
.
In
Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)
,
pp. 4149–4158
.
Cited by:
§4.1
.
Tao
et al.
(2024)
S. Tao, L. Yao, H. Ding, Y. Xie, Q. Cao, F. Sun, J. Gao, H. Shen, and B. Ding
When to trust llms: aligning confidence with response quality
.
In
Findings of the Association for Computational Linguistics: ACL 2024
,
pp. 5984–5996
.
Cited by:
§2.2
.
Turtel
et al.
(2025)
B. Turtel, D. Franklin, K. Skotheim, L. Hewitt, and P. Schoenegger
Outcome-based reinforcement learning to predict the future
.
arXiv preprint arXiv:2505.17989
.
Cited by:
Appendix A
.
Wei
et al.
(2024)
J. Wei, N. Karina, H. W. Chung, Y. J. Jiao, S. Papay, A. Glaese, J. Schulman, and W. Fedus
Measuring short-form factuality in large language models
.
arXiv preprint arXiv:2411.04368
.
Cited by:
§4.1
.
Xia
et al.
(2025)
Y. Xia, P. H. L. De Araujo, K. Zaporojets, and B. Roth
Influences on llm calibration: a study of response agreement, loss functions, and prompt styles
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 3740–3761
.
Cited by:
§5
.
Xiao
et al.
(2024)
R. Xiao, W. Ma, K. Wang, Y. Wu, J. Zhao, H. Wang, F. Huang, and Y. Li
Flowbench: revisiting and benchmarking workflow-guided planning for llm-based agents
.
In
Findings of the Association for Computational Linguistics: EMNLP 2024
,
pp. 10883–10900
.
Cited by:
§1
.
Xiao
et al.
(2026)
Z. Xiao, D. Dou, B. Xiong, Y. Chen, and G. Chen
Enhancing uncertainty estimation in llms with expectation of aggregated internal belief
.
In
Proceedings of the AAAI Conference on Artificial Intelligence
,
Vol.
40
,
pp. 34043–34051
.
Cited by:
§5
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
§1
,
§5
.
Xu
et al.
(2024)
T. Xu, S. Wu, S. Diao, X. Liu, X. Wang, Y. Chen, and J. Gao
Sayself: teaching llms to express confidence with self-reflective rationales
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
pp. 5985–5998
.
Cited by:
§5
.
Yang
et al.
(2025)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv,
et al.
Qwen3 technical report
.
arXiv preprint arXiv:2505.09388
.
Cited by:
§4.1
.
Yang
et al.
(2024)
D. Yang, Y. H. Tsai, and M. Yamada
On verbalized confidence scores for llms
.
arXiv preprint arXiv:2412.14737
.
Cited by:
§1
,
§5
.
Yang
et al.
(2018)
Z. Yang, P. Qi, S. Zhang, Y. Bengio, W. Cohen, R. Salakhutdinov, and C. D. Manning
HotpotQA: a dataset for diverse, explainable multi-hop question answering
.
In
Proceedings of the 2018 conference on empirical methods in natural language processing
,
pp. 2369–2380
.
Cited by:
§4.1
.
Yoon
et al.
(2026)
D. Yoon, S. Kim, S. Yang, S. Kim, S. Kim, Y. Kim, E. Choi, Y. Kim, and M. Seo
Reasoning models better express their confidence
.
Advances in Neural Information Processing Systems
38
,
pp. 103869–103896
.
Cited by:
§5
.
Zhang
et al.
(2025)
A. Zhang, Y. Chen, J. Pan, C. Zhao, A. Panda, J. Li, and H. He
Reasoning models know when they’re right: probing hidden states for self-verification
.
arXiv preprint arXiv:2504.05419
.
Cited by:
§5
.
Zhang
et al.
(2026a)
C. Zhang, Z. Zhu, Y. Wei, B. Tian, J. Liu, H. Wang, W. Xavier, and Y. Liu
Confidence-calibrated small-large language model collaboration for cost-efficient reasoning
.
In
Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 4480–4501
.
Cited by:
§1
,
§2.1
.
Zhang
et al.
(2026b)
J. Zhang, X. Peng, Q. Chen, Q. Ye, C. Xiong, and C. Wu
The illusion of certainty: decoupling capability and calibration in on-policy distillation
.
arXiv preprint arXiv:2604.16830
.
Cited by:
§5
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
Appendix B
,
§4.1
.
Appendix A
Training Details
All experiments are conducted on a server equipped with 8 NVIDIA A100 GPUs, each with 80GB of memory. For both HotpotQA and Big-Math, the overall training time is approximately 15 hours.
For policy training, we use the same hyperparameters in both rounds. Specifically, we use GRPO with 8 sampled responses per prompt and a sampling temperature of 0.7. The policy learning rate is set to 1e-6 for both HotpotQA and Big-Math. In line with
Damani et al. (2025)
, we use a training batch size of 64 for HotpotQA and 72 for Big-Math. The maximum prompt and response lengths are set to 3072 and 1536 for HotpotQA, and 1024 and 4096 for Big-Math, respectively. We do not normalize GRPO advantages by their group standard deviation, following prior practice
(
Bereket and Leskovec, 2025
;
Turtel et al., 2025
)
, thereby preserving reward-scale information for examples with large calibration errors.
For estimator training, we use a per-device batch size of 1 with gradient accumulation over 8 steps. We reduce the second-round learning rate to support stable refinement and avoid overfitting or excessive drift from the first-round estimator. Specifically, the learning rate decreases from
5
×
10
−
6
5\times 10^{-6}
to
1
×
10
−
6
1\times 10^{-6}
across the two HotpotQA rounds and from
5
×
10
−
6
5\times 10^{-6}
to
5
×
10
−
7
5\times 10^{-7}
across the two Big-Math rounds.
The prompt template used for policy training is shown in Figure
5
.
A conversation between User and Assistant. The user asks a question, and the Assistant solves it. The assistant first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning process and answer are enclosed within
<reason> </reason>
and
<answer> </answer>
tags, respectively, i.e.,
<reason>
reasoning process here
</reason><answer>
answer here
</answer>
.
Figure 5:
Policy training prompt template.
Appendix B
Details of Evaluation Metrics
We follow the notation defined in the main text.
Accuracy.
We compute accuracy using dataset-specific correctness criteria. For HotpotQA and HotpotQA-Modified, we use exact match. For GSM8K, MATH-500, and Big-Math, we use the
math_verify
library. For CommonsenseQA, GPQA, SimpleQA, and TriviaQA, we use an LLM-as-a-judge
(
Zheng et al., 2023
)
evaluation. To keep the judge model family separate from the evaluated backbone, we use Llama-3.1-8B-Instruct for Qwen-based methods and Qwen3-8B for Llama-based methods. Following
Damani et al. (2025)
, we run the judge with temperature set to 0 and provide it with the question, the ground-truth answer, and the extracted answer. The judge is instructed to output only “YES” or “NO” according to whether the answer is correct. Since these datasets contain short and objective answers, we do not condition the judge on thinking traces, avoiding potential bias from generated rationales.
AUROC.
We compute AUROC by sweeping the confidence threshold and integrating the resulting ROC curve:
AUROC
=
∫
0
1
TPR
⁡
(
FPR
−
1
​
(
x
)
)
​
𝑑
x
,
\mathrm{AUROC}=\int_{0}^{1}\mathrm{TPR}\left(\mathrm{FPR}^{-1}(x)\right)\,dx,
where TPR and FPR denote the true positive rate and false positive rate, respectively.
Brier score.
Given confidence scores
c
i
c_{i}
and correctness labels
z
i
z_{i}
, we compute
Brier
​
score
=
1
N
​
∑
i
=
1
N
(
c
i
−
z
i
)
2
.
\mathrm{Brier\ score}=\frac{1}{N}\sum_{i=1}^{N}(c_{i}-z_{i})^{2}.
ECE.
We partition predictions into
M
=
10
M=10
confidence bins
{
B
m
}
m
=
1
M
\{B_{m}\}_{m=1}^{M}
. For each bin, we compute the average correctness and average confidence:
z
¯
m
=
1
|
B
m
|
​
∑
i
∈
B
m
z
i
.
\bar{z}_{m}=\frac{1}{|B_{m}|}\sum_{i\in B_{m}}z_{i}.
c
¯
m
=
1
|
B
m
|
​
∑
i
∈
B
m
c
i
.
\bar{c}_{m}=\frac{1}{|B_{m}|}\sum_{i\in B_{m}}c_{i}.
The ECE is then computed as
ECE
=
∑
m
=
1
M
|
B
m
|
N
​
|
z
¯
m
−
c
¯
m
|
.
\mathrm{ECE}=\sum_{m=1}^{M}\frac{|B_{m}|}{N}\left|\bar{z}_{m}-\bar{c}_{m}\right|.
Table 4:
Comparison between IPoET and frontier commercial models. IPoET is trained on HotpotQA for the HotpotQA results and on Big-Math for the math average over MATH-500, GSM8K, and Big-Math. Best and second-best results are marked in
bold
and
underlined
, respectively.
(a) HotpotQA
Model
AUROC
↑
\uparrow
Brier
↓
\downarrow
ECE
↓
\downarrow
GPT-5 mini
0.603
0.306
0.298
Claude Haiku 4.5
0.671
0.279
0.266
DeepSeek-V4-Flash
0.537
0.332
0.328
Gemini 3 Flash
0.509
0.357
0.357
IPoET (ours)
0.800
0.184
0.107
(b) Math average
Model
AUROC
↑
\uparrow
Brier
↓
\downarrow
ECE
↓
\downarrow
GPT-5 mini
0.638
0.189
0.181
Claude Haiku 4.5
0.584
0.309
0.300
DeepSeek-V4-Flash
0.686
0.137
0.136
Gemini 3 Flash
0.557
0.150
0.150
IPoET (ours)
0.878
0.100
0.040
Appendix C
Commercial Model Comparison
We further compare IPoET with commercial models in Table
4
. We evaluate GPT-5 mini
(
OpenAI, 2025
)
, Claude Haiku 4.5
(
Anthropic, 2025
)
, DeepSeek-V4-Flash
(
DeepSeek, 2026
)
, and Gemini 3 Flash
(
Google DeepMind, 2025
)
.
1
1
1
Model versions used:
gpt-5-mini-2025-08-07
,
claude-haiku-4-5-20251001
,
deepseek-v4-flash
, and
gemini-3-flash-preview-nothinking
.
For the HotpotQA results, IPoET is trained on HotpotQA; for the math results, IPoET is trained on Big-Math and evaluated using the Math average over MATH-500, GSM8K, and Big-Math. Across both settings, IPoET obtains the best results on AUROC, Brier score, and ECE among the evaluated models. Commercial models demonstrate reasonable ability to estimate confidence, but their verbalized confidence remains less reliable in these settings. These results indicate that strong general-purpose models can still struggle to align expressed confidence with correctness on reasoning tasks, highlighting the need for task-oriented training objectives that explicitly target confidence reliability.