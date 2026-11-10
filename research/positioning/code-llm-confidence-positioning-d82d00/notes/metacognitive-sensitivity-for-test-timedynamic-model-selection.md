---
title: Metacognitive Sensitivity for Test-TimeDynamic Model Selection
id: metacognitive-sensitivity-for-test-timedynamic-model-selection
tags:
- code-llm-confidence-positioning-d82d00
- metacognition
created: '2026-11-09T23:08:22.749271Z'
updated: '2026-11-09T23:27:44.440366Z'
source: https://arxiv.org/html/2512.10451
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:22.748669Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv html). CogInterp workshop paper: meta-d'' metacognitive
  sensitivity feeds a LinUCB/LinTS bandit arbiter selecting between two image models;
  CIFAR-10 gains +7.1..8.2% at 300 trials, 1.4-3.5% at 1000 (Table 1). Not code, not
  LLM text; metrology-adjacent only via meta-d'' (candidate F near, not occupant for
  code).'
---

Metacognitive Sensitivity for Test-TimeDynamic Model Selection
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2512.10451v1 [cs.LG] 11 Dec 2025
\workshoptitle
CogInterp: Interpreting Cognition in Deep Learning Models
Metacognitive Sensitivity for Test-Time
Dynamic Model Selection
Le Tuan Minh Trinh
Affiliation:
University College London
Affiliation:
London, United Kingdom
Email:
minh.trinh.23@ucl.ac.uk
Le Minh Vu Pham
Affiliation:
FPT University
Affiliation:
Hanoi, Vietnam
Email:
vuplmhe180526@fpt.edu.vn
Thi Minh Anh Pham
Affiliation:
Queen Mary University of London
Affiliation:
London, United Kingdom
Email:
t.pham@se22.qmul.ac.uk
Duc An Nguyen
Affiliation:
University of Oxford
Affiliation:
Oxford, United Kingdom
Email:
annguyen@robots.ox.ac.uk
Abstract
A key aspect of human cognition is metacognition - the ability to assess one’s own knowledge and judgment reliability. While deep learning models can express confidence in their predictions, they often suffer from poor calibration, a cognitive bias where expressed confidence does not reflect true competence. Do models truly know what they know? Drawing from human cognitive science, we propose a new framework for evaluating and leveraging AI metacognition. We introduce
meta-d’
, a psychologically-grounded measure of metacognitive sensitivity, to characterise how reliably a model’s confidence predicts its own accuracy. We then use this dynamic sensitivity score as context for a bandit-based arbiter that performs test-time model selection, learning which of several expert models to trust for a given task. Our experiments across multiple datasets and deep learning model combinations (including CNNs and VLMs) demonstrate that this metacognitive approach improves joint-inference accuracy over constituent models. This work provides a novel behavioural account of AI models, recasting ensemble selection as a problem of evaluating both short-term signals (confidence prediction scores) and medium-term traits (metacognitive sensitivity).
1
Introduction
Deep learning research is characterised by increasing specialisation. Convolutional Neural Networks (CNNs) are widely used for perceptual tasks such as image recognition; Transformers and Large Language Models (LLMs) dominate natural language processing; and Vision-Language Models (VLMs) integrate across modalities
Hu and Frank (2024)
;
Gadetsky et al. (2025)
;
McCoy et al. (2024)
;
Steyvers et al. (2025)
. This specialisation improves performance on benchmark tasks but also reflects the "No Free Lunch" theorem: no single architecture is optimal across all problems
Bigelow et al. (2023)
. As a result, systems rely on multiple specialised models, raising the arbitration problem - determining which model should be used for a given input. This is the focus of dynamic model selection, which develops methods for assigning tasks to the most appropriate model.
A central obstacle in this area is the unreliability of model confidence. Deep neural networks produce probabilistic outputs that are often miscalibrated, meaning confidence does not align with true prediction accuracy. Research has shown that this miscalibration arises from the same architectural and training practices that enable high accuracy
Guo et al. (2017)
;
Geirhos et al. (2018)
;
Steyvers and Peters (2025)
;
Song et al. (2025a)
.
Cognitive science has long studied the analogous human ability, termed
metacognition
, providing theoretical and mathematical tools for assessing how well an agent can evaluate its own knowledge
Rouault et al. (2019)
;
Fleming (2021)
;
Lee et al. (2025)
. Concepts such as metacognitive sensitivity are increasingly viewed as necessary for developing AI systems that can self-monitor, detect errors, and adjust behaviour based on uncertainty
Yedetore et al. (2023)
;
Kurvers et al. (2023)
;
Kuribayashi et al. (2025)
;
Nguyen et al. (2025)
. Recent work has applied the
meta-d’
framework to AI, introducing "AI metacognitive sensitivity" as a performance dimension. Findings suggest that in human-AI collaboration, an AI with lower accuracy but higher metacognitive sensitivity can be a more effective partner, as its confidence signals are more reliable for guiding when its advice should be followed.
While the literature has started to recognise the importance of AI metacognition as a diagnostic tool
Gandhi et al. (2024)
;
Ivanova et al. (2024)
;
Gandhi et al. (2025)
;
Song et al. (2025c)
;
Murthy et al. (2025)
;
Song et al. (2025b)
;
Hu et al. (2025)
, the work reviewed here represents a critical next step: operationalising this concept as a functional component within an adaptive algorithm for a concrete engineering problem like dynamic model selection at test-time. It moves the idea of AI metacognition from a desirable property to be measured to a dynamic signal to be actively leveraged.
In this work, we embed metacognitive sensitivity into a bandit-based framework for dynamic model selection, demonstrating accuracy gains compared to individual constituent models. Beyond these improvements, our results suggest that leveraging metacognition as a functional signal can enable ensemble systems that adapt more flexibly and reliably.
2
Related Work
Given a pool of expert models, a system must decide how to aggregate their outputs to arrive at a final prediction. The paradigms for combining and selecting models are summarised as follows:
Static Ensembles:
combine predictions from all models using fixed rules, such as majority voting for classification or averaging for regression
Ganaie et al. (2022)
.
Static ensembles reduce variance but are non-adaptive, treating all models as equally competent and using all of them for every input, which can be computationally inefficient when models have localised competence
Ju et al. (2018)
;
Su et al. (2021)
;
Jiang et al. (2024)
.
Dynamic Ensembles Selection:
selects a model or subset of models for each test instance, based on the idea that different classifiers perform best in different regions of the feature space
Cruz et al. (2015)
;
Liu et al. (2023)
;
Piwko et al. (2025)
;
Vasheghani and Sharifi (2025)
.
Mixture of Experts (MoE):
consists of expert networks and a gating network
Chen et al. (2022)
. The gating network assigns weights to experts for each input, and the final prediction is a weighted sum of expert outputs. Unlike Dynamic Selection, which uses pre-trained models with an external selection mechanism, MoE is trained end-to-end, with experts and gating network co-adapting during training
Shazeer et al. (2017)
;
Li et al. (2024)
;
Li et al. (2025)
;
Mu and Lin (2025)
.
The shift from static ensembles to dynamic selection, and MoE methods underscores the need for adaptive mechanisms. Existing methods rely on fixed heuristics like local accuracy rather than learned policies. Reinforcement learning, particularly contextual bandits, offers a framework for adaptive selection by balancing exploration and exploitation across models. However, current approaches lack metacognition-aware feedback. They either depend on miscalibrated raw confidence or on noisy, static heuristics such as local accuracy. None leverage measures of metacognitive sensitivity
to guide adaptive selection.
3
Problem Formulation
The central problem is to perform
test-time dynamic model selection
for an image classification task. Given a pair of pre-trained models,
M
=
{
M
A
,
M
B
}
M=\{M_{A},M_{B}\}
, and a sequence of images,
D
=
{
x
1
,
…
,
x
N
}
D=\{x_{1},\dots,x_{N}\}
, the objective is to create a framework that, for each image
x
t
x_{t}
, selects the model whose prediction is most likely to be correct.
Since models often vary in performance across domains, particularly on out-of-distribution data, a static choice is suboptimal. We propose a dynamic selection agent that chooses between models per sample, informed by both immediate confidence and a cognitively inspired, dynamically updated measure of
metacognitive sensitivity
Fleming and Daw (2017)
.
The goal is to learn a selection policy
π
\pi
that maximises the cumulative reward, which is equivalent to maximising the total classification accuracy of the framework over the dataset:
max
⁡
∑
t
=
1
N
π
⁡
R
t
=
max
⁡
∑
t
=
1
N
π
⁡
𝕀
⁡
(
y
^
a
t
,
t
=
y
t
)
\max_{\pi}\sum_{t=1}^{N}R_{t}=\max_{\pi}\sum_{t=1}^{N}\mathbb{I}(\hat{y}_{a_{t},t}=y_{t})
(1)
where
a
t
=
π
⁡
(
s
t
)
a_{t}=\pi(s_{t})
is the model selected at time
t
t
based on context
s
t
s_{t}
,
y
^
a
t
,
t
\hat{y}_{a_{t},t}
is its prediction, and
y
t
y_{t}
is the ground truth label.
4
Dynamic Model Selection Framework
Algorithm 1
Test-Time Dynamic Model Selection
1:
Require:
Model set
M
=
{
M
A
,
M
B
}
M=\{M_{A},M_{B}\}
, Dataset
D
=
{
x
1
,
…
,
x
N
}
D=\{x_{1},\dots,x_{N}\}
, Burn-in size
B
=
100
B=100
, Window size
W
=
100
W=100
, Update frequency
F
=
50
F=50
.
2:
Initialise:
Contextual Bandit (LinUCB or LinTS).
3:
Initialise:
Total Reward
R
t
​
o
​
t
​
a
​
l
←
0
R_{total}\leftarrow 0
.
4:
⊳
\triangleright
Burn-in Phase
5:
Collect performance data (confidence, reward)
H
k
=
{
(
c
k
,
i
,
r
k
,
i
)
}
i
=
1
B
H_{k}=\{(c_{k,i},r_{k,i})\}_{i=1}^{B}
for each model
M
k
∈
M
M_{k}\in M
on the first
B
B
trials.
6:
for
each model
M
k
∈
M
M_{k}\in M
do
7:
μ
k
,
B
←
meta-d’
​
(
H
k
)
\mu_{k,B}\leftarrow\text{meta-d'}(H_{k})
⊳
\triangleright
Compute initial metacognitive score
8:
end
for
9:
⊳
\triangleright
Dynamic Selection Phase
10:
for
t
=
B
+
1
t=B+1
to
N
N
do
11:
for
each model
M
k
∈
M
M_{k}\in M
do
⊳
\triangleright
Context Formulation
12:
Get confidence
c
k
,
t
c_{k,t}
on image
x
t
x_{t}
.
13:
if
(
t
−
B
)
(
mod
F
)
=
1
(t-B)\pmod{F}=1
then
14:
Collect past performance
H
k
←
{
(
c
k
,
i
,
r
k
,
i
)
}
i
=
t
−
W
t
−
1
H_{k}\leftarrow\{(c_{k,i},r_{k,i})\}_{i=t-W}^{t-1}
.
15:
Update metacognitive score:
μ
k
,
t
←
meta-d’
​
(
H
k
)
\mu_{k,t}\leftarrow\text{meta-d'}(H_{k})
.
16:
else
17:
Keep previous score:
μ
k
,
t
←
μ
k
,
t
−
1
\mu_{k,t}\leftarrow\mu_{k,t-1}
.
18:
end
if
19:
end
for
20:
Construct context vector
s
t
=
[
c
A
,
t
,
μ
A
,
t
,
c
B
,
t
,
μ
B
,
t
]
s_{t}=[c_{A,t},\mu_{A,t},c_{B,t},\mu_{B,t}]
(2)
21:
⊳
\triangleright
Bandit Action & Reward
22:
Select model
a
t
a_{t}
using bandit policy on
s
t
s_{t}
.
23:
a
t
←
arg
⁡
max
k
∈
{
A
,
B
}
​
π
t
​
(
s
t
,
k
)
a_{t}\leftarrow\arg\max_{k\in\{A,B\}}\pi_{t}(s_{t},k)
⊳
\triangleright
π
t
​
(
s
t
,
k
)
\pi_{t}(s_{t},k)
: a specific bandit selection in Appendix
24:
Get prediction
y
^
a
t
,
t
\hat{y}_{a_{t},t}
from model
M
a
t
M_{a_{t}}
.
25:
Observe true label
y
t
y_{t}
and calculate reward
R
t
=
𝕀
⁡
(
y
^
a
t
,
t
=
y
t
)
R_{t}=\mathbb{I}(\hat{y}_{a_{t},t}=y_{t})
.
26:
R
t
​
o
​
t
​
a
​
l
←
R
t
​
o
​
t
​
a
​
l
+
R
t
R_{total}\leftarrow R_{total}+R_{t}
.
27:
Update bandit policy with
(
s
t
,
a
t
,
R
t
)
(s_{t},a_{t},R_{t})
.
⊳
\triangleright
Learning
28:
end
for
29:
return
Overall Accuracy:
R
t
​
o
​
t
​
a
​
l
/
(
N
−
B
)
R_{total}/(N-B)
.
We propose a framework in which a contextual bandit serves as the dynamic selection agent. At each time step
t
t
, the bandit observes a context vector from two candidate models, selects one to act (the “arm”), receives a reward based on prediction correctness, and updates its policy. For each input
x
t
x_{t}
, models
M
A
M_{A}
and
M
B
M_{B}
produce predictions and confidence scores, which are combined into a 4-dimensional context vector as shown in Equation. 2.
The
short-term signal (
c
k
,
t
c_{k,t}
)
is the model’s raw
confidence
on the current image
x
t
x_{t}
, taken as the maximum value of its softmax output probability; and the
metacognitive sensitivity (
μ
k
,
t
\mu_{k,t}
)
is the score representing the model’s recent historical ability to know when it knows. This is a more stable, medium-term trait, which was operationalised using the
meta-d’
values.
Sensitivity scores are initialised using the first 100 trials and updated every 50 trials via a 100-trial sliding window. To address the computational demands of hierarchical Bayesian inference, we developed a GPU-parallelised package for efficient
meta-d’
estimation.
For learning and decision-making, we employ the contextual bandit algorithms
(Further bandit algorithmic details are provided in the Appendix).
5
Results
We evaluate our framework using four diverse pre-trained models: AlexNet, GoogleNet (classical CNN), EfficientNet (efficiently scaled CNN), and Vision Transformer (ViT) (transformer-based model). This selection captures both convolutional and attention-based models, enabling the assessment of the adaptability of our framework across fundamentally different design choices. We evaluate accuracy at three checkpoints corresponding to
the number of trials indicates how many images have been processed up to that point.
Table 1:
Accuracy of the best individual image models and the joint framework on the CIFAR10.
Model Pair
300 trials
700 trials
1000 trials
Model
Comb.
Model
Comb.
Model
Comb.
AlexNet-ViT
62.4
69.5
(+7.1%)
64.8
66.2
(+1.4%)
62.4
65.9
(+3.5%)
AlexNet-GoogleNet
62.7
70.6
(+7.9%)
57.7
57.5
(-0.2%)
56.8
58.4
(+1.6%)
EfficientNet-ViT
67.7
75.9
(+8.2%)
66.4
68.0
(+1.6%)
66.4
67.8
(+1.4%)
EfficientNet-GoogleNet
54.8
59.0
(+4.8%)
53.6
55.8
(+2.2%)
54.8
57.3
(+2.5%)
Table
1
shows that the joint framework’s accuracy is significantly improved in the early trials and then stabilises at 1.4%–3.5% higher than that of the individual models. At certain points, however, the joint framework underperforms relative to the best individual model in the pair. This effect can be attributed to correlated errors: performance is limited when both models misclassify the same sample, a pattern more common among architecturally similar models that share inductive biases from pre-training. For example, in one pairing (Figure.
1
), the metacognitive sensitivity of AlexNet dropped (at trial 700), but the bandit quickly adapted by shifting selection toward GoogleNet. (Learning dynamics graphs are detailed in the Appendix
A
.)
Despite these challenges, architectural diversity enhances complementarity. Heterogeneous pairings, such as CNN-Transformer models, exhibit fewer correlated errors and achieve higher accuracy. This highlights the importance of inductive-bias diversity for effective dynamic model selection.
Table 2:
Performance of the best individual VLM and the joint framework on the CIFAR10 - PACS.
Model Pair
1500 trials
2500 trials
4000 trials
Model
Comb.
Model
Comb.
Model
Comb.
MetaCLIP-SigLIP
98.7
99.0
(+0.3%)
98.7
98.6
(0.0%)
98.4
98.5
(+0.1%)
CLIP-ALIGN
94.2
96.0
(+1.8%)
94.8
96.2
(+1.6%)
94.8
95.8
(+1.0%)
To further probe the framework’s robustness, we evaluated it under domain shift using Vision-Language Models (CLIP, ALIGN, SigLIP and MetaCLIP). To process the OOD bias in VLMs evaluation, we augment PACS
Xu et al. (2019)
with CIFAR-10. PACS exhibits a 1:5 imbalance between photographic and non-photographic styles, which may skew the results. Adding CIFAR-10 introduces additional photographic diversity, yielding a more balanced and robust combined dataset for benchmarking.
Table
2
shows that while individual model performance declines under more demanding conditions, the framework leverages complementary strengths across models. This results in an initial accuracy improvement of 0.3%–1.8%, though because VLMs are already so accurate on their own, the gains are noticeable but modest compared to what had been seen with image models. However these potential suggest that metacognition-aware selection holds promise for addressing challenging, test-time distributional shifts in prediction tasks.
6
Conclusion
In this work, we presented a metacognition-inspired framework for dynamic model selection, introducing
meta-d’
as a measure of how reliably a model’s confidence predicts its accuracy.
Our experiments show that embedding metacognitive sensitivity in a bandit-based framework for dynamic model selection yields accuracy gains compared to individual constituent models. Future directions include extending the framework to large language model ensembles and exploring richer reinforcement learning strategies for selection. Overall, this work provides a first step toward incorporating metacognition-inspired feedback into adaptive model selection, with the goal of creating more reliable and interpretable ensemble systems.
References
Bigelow
et al.
(2023)
E. J. Bigelow, E. S. Lubana, R. P. Dick, H. Tanaka, and T. D. Ullman
In-context learning dynamics with random binary sequences
.
arXiv preprint arXiv:2310.17639
.
Cited by:
§1
.
Chen
et al.
(2022)
Z. Chen, Y. Deng, Y. Wu, Q. Gu, and Y. Li
Towards understanding the mixture-of-experts layer in deep learning
.
Advances in neural information processing systems
35
,
pp. 23049–23062
.
Cited by:
§2
.
Cruz
et al.
(2015)
R. M. Cruz, R. Sabourin, and G. D. Cavalcanti
META-des. h: a dynamic ensemble selection technique using meta-learning and a dynamic weighting approach
.
In
2015 International Joint Conference on Neural Networks (IJCNN)
,
pp. 1–8
.
Cited by:
§2
.
Fleming and Lau (2014)
S. M. Fleming and H. C. Lau
How to measure metacognition
.
Frontiers in Human Neuroscience
8
,
pp. 443
.
Cited by:
§A.1
.
Fleming and Daw (2017)
S. M. Fleming and N. D. Daw
Self-evaluation of decision-making: a general bayesian framework for metacognitive computation.
.
Psychological Review
124
(
1
),
pp. 91–114
.
Cited by:
§A.1
,
§3
.
Fleming (2017)
S. M. Fleming
HMeta-d: hierarchical bayesian estimation of metacognitive efficiency from confidence ratings
.
Neuroscience of consciousness
2017
(
1
),
pp. nix007
.
Cited by:
§A.1
.
Fleming (2021)
S. M. Fleming
Know thyself: the new science of self-awareness
.
Hachette UK
.
Cited by:
§1
.
Gadetsky
et al.
(2025)
A. Gadetsky, A. Atanov, Y. Jiang, Z. Gao, G. H. Mighan, A. Zamir, and M. Brbic
Large (vision) language models are unsupervised in-context learners
.
In
International Conference on Learning Representations
,
Cited by:
§1
.
Ganaie
et al.
(2022)
M. A. Ganaie, M. Hu, A. K. Malik, M. Tanveer, and P. N. Suganthan
Ensemble deep learning: a review
.
Engineering Applications of Artificial Intelligence
115
,
pp. 105151
.
Cited by:
§2
.
Gandhi
et al.
(2025)
K. Gandhi, A. Chakravarthy, A. Singh, N. Lile, and N. D. Goodman
Cognitive behaviors that enable self-improving reasoners, or, four habits of highly effective stars
.
arXiv preprint arXiv:2503.01307
.
Cited by:
§1
.
Gandhi
et al.
(2024)
K. Gandhi, Z. Lynch, J. Fränken, K. Patterson, S. Wambu, T. Gerstenberg, D. C. Ong, and N. D. Goodman
Human-like affective cognition in foundation models
.
arXiv preprint arXiv:2409.11733
.
Cited by:
§1
.
Geirhos
et al.
(2018)
R. Geirhos, P. Rubisch, C. Michaelis, M. Bethge, F. A. Wichmann, and W. Brendel
ImageNet-trained cnns are biased towards texture; increasing shape bias improves accuracy and robustness
.
In
International conference on learning representations
,
Cited by:
§1
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
.
Hu and Frank (2024)
J. Hu and M. C. Frank
Auxiliary task demands mask the capabilities of smaller language models
.
arXiv preprint arXiv:2404.02418
.
Cited by:
§1
.
Hu
et al.
(2025)
J. Hu, F. Sosa, and T. Ullman
Re-evaluating Theory of Mind evaluation in large language models
.
Philosophical Transactions of the Royal Society B: Biological Sciences
380
(
1932
),
pp. 20230499
.
Note:
Publisher: Royal Societydoi: 10.1098/rstb.2023.0499
External Links:
Link
,
Document
Cited by:
§1
.
Ivanova
et al.
(2024)
A. A. Ivanova, A. Sathe, B. Lipkin, U. Kumar, S. Radkani, T. H. Clark, C. Kauf, J. Hu, R. T. Pramod, G. Grand, V. Paulun, M. Ryskina, E. Akyurek, E. Wilcox, N. Rashid, L. Choshen, R. Levy, E. Fedorenko, J. Tenenbaum, and J. Andreas
Elements of World Knowledge (EWOK): A cognition-inspired framework for evaluating basic world knowledge in language models
.
External Links:
Link
Cited by:
§1
.
Jiang
et al.
(2024)
K. Jiang, Z. Xiong, Q. Yang, J. Chen, and G. Chen
An interpretable ensemble method for deep representation learning
.
Engineering Reports
6
(
3
),
pp. e12725
.
Cited by:
§2
.
Ju
et al.
(2018)
C. Ju, A. Bibaut, and M. van der Laan
The relative performance of ensemble methods with deep convolutional neural networks for image classification
.
Journal of applied statistics
45
(
15
),
pp. 2800–2818
.
Cited by:
§2
.
Kuribayashi
et al.
(2025)
T. Kuribayashi, Y. Oseki, S. B. Taieb, K. Inui, and T. Baldwin
Large language models are human-like internally
.
arXiv preprint arXiv:2502.01615
.
Cited by:
§1
.
Kurvers
et al.
(2023)
R. H. Kurvers, A. G. Nuzzolese, A. Russo, G. Barabucci, S. M. Herzog, and V. Trianni
Automating hybrid collective intelligence in open-ended medical diagnostics
.
Proceedings of the National Academy of Sciences
120
(
34
),
pp. e2221473120
.
Cited by:
§1
.
Lee
et al.
(2025)
D. Lee, J. Pruitt, T. Zhou, J. Du, and B. Odegaard
Metacognitive sensitivity: the key to calibrating trust and optimal decision making with ai
.
PNAS nexus
4
(
5
),
pp. pgaf133
.
Cited by:
§1
.
Li
et al.
(2024)
J. Li, X. Wang, S. Zhu, C. Kuo, L. Xu, F. Chen, J. Jain, H. Shi, and L. Wen
Cumo: scaling multimodal llm with co-upcycled mixture-of-experts
.
Advances in Neural Information Processing Systems
37
,
pp. 131224–131246
.
Cited by:
§2
.
Li
et al.
(2025)
Y. Li, S. Jiang, B. Hu, L. Wang, W. Zhong, W. Luo, L. Ma, and M. Zhang
Uni-moe: scaling unified multimodal llms with mixture of experts
.
IEEE Transactions on Pattern Analysis and Machine Intelligence
.
Cited by:
§2
.
Liu
et al.
(2023)
L. Liu, J. Wu, X. Li, and H. Huang
Dynamic ensemble selection with reinforcement learning
.
In
International Conference on Intelligent Computing
,
pp. 629–640
.
Cited by:
§2
.
Macmillan (2002)
N. A. Macmillan
Signal detection theory
.
Stevens’ handbook of experimental psychology: Methodology in experimental psychology
3
,
pp. 43–90
.
Cited by:
§A.1
.
McCoy
et al.
(2024)
R. T. McCoy, S. Yao, D. Friedman, M. D. Hardy, and T. L. Griffiths
Embers of autoregression show how large language models are shaped by the problem they are trained to solve
.
Proceedings of the National Academy of Sciences
121
(
41
),
pp. e2322420121
.
Cited by:
§1
.
Mu and Lin (2025)
S. Mu and S. Lin
A comprehensive survey of mixture-of-experts: algorithms, theory, and applications
.
arXiv preprint arXiv:2503.07137
.
Cited by:
§2
.
Murthy
et al.
(2025)
S. K. Murthy, R. Zhao, J. Hu, S. Kakade, M. Wulfmeier, P. Qian, and T. Ullman
Inside you are many wolves: using cognitive models to interpret value trade-offs in llms
.
External Links:
Link
Cited by:
§1
.
Nguyen
et al.
(2025)
D. Nguyen, R. Bhattacharyya, C. Colombatto, S. Fleming, I. Posner, and N. Hawes
Joint decision-making in robot teleoperation: when are two heads better than one?
.
arXiv preprint arXiv:2503.15510
.
Cited by:
§1
.
Piwko
et al.
(2025)
J. Piwko, J. Ruciński, D. Płudowski, A. Zajko, P. Żak, M. Zacharecki, A. Kozak, and K. Woźnica
Divide, specialize, and route: a new approach to efficient ensemble learning
.
arXiv preprint arXiv:2506.20814
.
Cited by:
§2
.
Rouault
et al.
(2019)
M. Rouault, P. Dayan, and S. M. Fleming
Forming global estimates of self-performance from local confidence
.
Nature communications
10
(
1
),
pp. 1141
.
Cited by:
§1
.
Shazeer
et al.
(2017)
N. Shazeer, A. Mirhoseini, K. Maziarz, A. Davis, Q. Le, G. Hinton, and J. Dean
Outrageously large neural networks: the sparsely-gated mixture-of-experts layer
.
arXiv preprint arXiv:1701.06538
.
Cited by:
§2
.
Song
et al.
(2025a)
S. Song, J. Hu, and K. Mahowald
Language models fail to introspect about their knowledge of language
.
arXiv preprint arXiv:2503.07513
.
Cited by:
§1
.
Song
et al.
(2025b)
S. Song, J. Hu, and K. Mahowald
Language models fail to introspect about their knowledge of language
.
In
Proceedings of the Conference on Language Modeling
,
External Links:
Link
Cited by:
§1
.
Song
et al.
(2025c)
S. Song, H. Lederman, J. Hu, and K. Mahowald
Privileged self-access matters for introspection in ai
.
External Links:
Link
Cited by:
§1
.
Steyvers and Peters (2025)
M. Steyvers and M. A. Peters
Metacognition and uncertainty communication in humans and large language models
.
arXiv preprint arXiv:2504.14045
.
Cited by:
§1
.
Steyvers
et al.
(2025)
M. Steyvers, H. Tejeda, A. Kumar, C. Belem, S. Karny, X. Hu, L. W. Mayer, and P. Smyth
What large language models know and what people think they know
.
Nature Machine Intelligence
7
(
2
),
pp. 221–231
.
Cited by:
§1
.
Su
et al.
(2021)
K. Su, J. Wu, D. Gu, S. Yang, S. Deng, and A. K. Khakimova
An adaptive deep ensemble learning method for dynamic evolving diagnostic task scenarios
.
Diagnostics
11
(
12
),
pp. 2288
.
Cited by:
§2
.
Vasheghani and Sharifi (2025)
S. Vasheghani and S. Sharifi
Dynamic ensemble learning for robust image classification: a model-specific selection strategy
.
Available at SSRN 5215134
.
Cited by:
§2
.
Xu
et al.
(2019)
J. Xu, L. Xiao, and A. López
Self-supervised domain adaptation for computer vision tasks
.
Cited by:
§5
.
Yedetore
et al.
(2023)
A. Yedetore, T. Linzen, R. Frank, and R. T. McCoy
How poor is the stimulus? evaluating hierarchical generalization in neural networks trained on child-directed speech
.
arXiv preprint arXiv:2301.11462
.
Cited by:
§1
.
Appendix A
Appendix
A.1
Metacognitive Sensitivity (
meta-d’
)
To implement the metacognitive sensitivity score
μ
k
\mu_{k}
, we adopt the ‘meta-d’‘ framework developed by
Fleming and Lau
and detailed in
Fleming and Daw (2017)
. Metacognition refers to the ability to monitor one’s own cognitive processes, and in this context, how well a model’s confidence relates to its actual success.
Meta-d’
is a metric derived from
Signal Detection Theory (SDT)
by
Macmillan
that quantifies this ability. Its primary advantage is that it provides a measure of metacognitive sensitivity that is independent of the model’s task performance and overall confidence bias.
We calculates
meta-d’
by fitting a hierarchical Bayesian model to the observed distributions of confidence ratings for correct and incorrect trials
Fleming (2017)
. For our framework, the score
μ
k
,
t
\mu_{k,t}
for a model
M
k
M_{k}
at time
t
t
is its calculated meta-d’ value.
A.2
Dynamic Update Mechanism
A key feature of our framework is that the metacognitive sensitivity score,
μ
k
\mu_{k}
, is not static but dynamically updated to reflect recent performance.
1.
Initialisation
: A burn-in set of the first 100 trials is used to compute the initial scores,
μ
A
,
0
\mu_{A,0}
and
μ
B
,
0
\mu_{B,0}
.
2.
Sliding Window Update
: During the selection process, the
meta-d’
score for each model is recalculated every 50 trials using a
sliding window
of the 100 most recent trials.
This updating mechanism enables the framework to adapt to non-stationarity in model performance, such as when the underlying data distribution shifts.
A.3
Contextual Bandit Selection
The learning and decision-making core of our framework is a contextual bandit. We adopt two well-established algorithms: Algorithm.
2
:
LinUCB
(Linear Upper Confidence Bound) and Algorithm.
3
:
LinTS
(Linear Thompson Sampling).
The bandit’s interaction at each step
t
t
is as follows:
1.
Observe Context
: Receives the context vector
s
t
s_{t}
.
2.
Select Action
: The algorithm’s policy selects an action
a
t
∈
{
A
,
B
}
a_{t}\in\{A,B\}
.
3.
Receive Reward
: The framework executes the chosen model
M
a
t
M_{a_{t}}
. The reward
R
t
R_{t}
is 1 if the model’s prediction is correct, and 0 otherwise.
4.
Update Policy
: The bandit uses the tuple
(
s
t
,
a
t
,
R
t
)
(s_{t},a_{t},R_{t})
to update its internal model, improving its policy for future decisions.
Algorithm 2
Linear Contextual Upper Confidence Bound
1:
Number of arms
K
K
, observe context
s
t
s_{t}
with dimension
d
d
, exploration parameter
α
\alpha
2:
Initialise
A
a
←
I
d
A_{a}\leftarrow I_{d}
and
b
a
←
𝟎
d
b_{a}\leftarrow\mathbf{0}_{d}
for all
k
∈
{
A
,
B
}
k\in\{A,B\}
3:
for
each round
t
=
1
,
2
,
…
t=1,2,\dots
do
4:
Observe context vector
s
t
∈
ℝ
d
s_{t}\in\mathbb{R}^{d}
5:
for
each arm
k
∈
{
A
,
B
}
k\in\{A,B\}
do
6:
Compute
θ
^
k
←
A
k
−
1
​
b
k
\hat{\theta}_{k}\leftarrow A_{k}^{-1}b_{k}
7:
Compute
π
t
​
(
s
t
,
k
)
←
θ
^
k
⊤
​
s
t
+
α
​
s
t
⊤
​
A
k
−
1
​
s
t
\pi_{t}(s_{t},k)\leftarrow\hat{\theta}_{k}^{\top}s_{t}+\alpha\sqrt{s_{t}^{\top}A_{k}^{-1}s_{t}}
8:
end
for
9:
Choose arm
k
t
←
arg
⁡
max
k
∈
{
A
,
B
}
​
π
t
​
(
s
t
,
k
)
k_{t}\leftarrow\arg\max_{k\in\{A,B\}}\pi_{t}(s_{t},k)
10:
Observe reward
r
t
r_{t}
11:
Update:
A
k
t
←
A
k
t
+
s
t
​
s
t
⊤
,
b
k
t
←
b
k
t
+
r
t
​
s
t
A_{k_{t}}\leftarrow A_{k_{t}}+s_{t}s_{t}^{\top},\quad b_{k_{t}}\leftarrow b_{k_{t}}+r_{t}s_{t}
12:
end
for
Algorithm 3
Linear Contextual Thompson Sampling
1:
Number of arms
K
K
, observe context
s
t
s_{t}
with dimension
d
d
, prior variance parameter
σ
\sigma
2:
Initialise
A
a
←
I
d
A_{a}\leftarrow I_{d}
,
b
a
←
𝟎
d
b_{a}\leftarrow\mathbf{0}_{d}
for all
k
∈
{
A
,
B
}
k\in\{A,B\}
3:
for
each round
t
=
1
,
2
,
…
t=1,2,\dots
do
4:
Observe context vector
s
t
∈
ℝ
d
s_{t}\in\mathbb{R}^{d}
5:
for
each arm
k
∈
{
A
,
B
}
k\in\{A,B\}
do
6:
Compute
A
k
−
1
←
(
A
k
+
ϵ
​
I
d
)
−
1
A_{k}^{-1}\leftarrow(A_{k}+\epsilon I_{d})^{-1}
7:
Compute posterior mean:
θ
^
k
←
A
k
−
1
​
b
k
\hat{\theta}_{k}\leftarrow A_{k}^{-1}b_{k}
8:
Sample
θ
~
k
∼
𝒩
⁡
(
θ
^
k
,
σ
2
​
A
k
−
1
)
\tilde{\theta}_{k}\sim\mathcal{N}(\hat{\theta}_{k},\sigma^{2}A_{k}^{-1})
9:
Compute sampled reward:
π
t
​
(
s
t
,
k
)
←
θ
~
k
​
s
t
⊤
\pi_{t}(s_{t},k)\leftarrow\tilde{\theta}_{k}s_{t}^{\top}
10:
end
for
11:
Choose arm
k
t
←
arg
⁡
max
k
∈
{
A
,
B
}
​
π
t
​
(
s
t
,
k
)
k_{t}\leftarrow\arg\max_{k\in\{A,B\}}\pi_{t}(s_{t},k)
→
\rightarrow
Observe reward
r
t
r_{t}
12:
Update:
A
k
t
←
A
k
t
+
s
t
​
s
t
⊤
,
b
k
t
←
b
k
t
+
r
t
​
s
t
A_{k_{t}}\leftarrow A_{k_{t}}+s_{t}s_{t}^{\top},\quad b_{k_{t}}\leftarrow b_{k_{t}}+r_{t}s_{t}
13:
end
for
A.4
Learning Dynamics Graphs
Figure 1:
Figure of GoogleNet and AlexNet with Framework Accuracy (using LinTS with
σ
\sigma
= 0.5)
Figure 2:
Figure of ViT and EfficientNet with Framework Accuracy (using LinTS with
σ
\sigma
= 1.0)
Figure 3:
Figure of ALIGN and CLIP with Framework Accuracy (using LinUCB with
α
\alpha
= 1.0)
Figure 4:
Figure of MetaCLIP and SigLIP with Framework Accuracy (using LinUCB with
α
\alpha
= 0.5)