---
title: 'Rethinking Early Stopping: Refine, Then Calibrate'
id: rethinking-early-stopping-refine-then-calibrate
tags:
- code-llm-confidence-positioning-d82d00
- paper-related-f
created: '2026-11-09T23:08:45.240078Z'
updated: '2026-11-09T23:27:44.526947Z'
source: https://arxiv.org/html/2501.19195
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:45.239612Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Berta, Holzmuller, Jordan, Bach (arXiv 2501.19195v2). Variational formulation
  of the calibration-refinement decomposition of proper losses; calibration and refinement
  errors are not minimized simultaneously in training; proposes minimizing refinement
  during training then recalibrating post hoc; recalibration risk gives refinement
  error, risk difference gives calibration error. General ML classification, no LLM
  or code. Supports separating calibration from discrimination in F. Full text (HTML).
---

Rethinking Early Stopping: Refine, Then Calibrate
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2501.19195v2 [cs.LG] 25 Jun 2025
Rethinking Early Stopping: Refine, Then Calibrate
Eugène Berta
†
†
thanks:
eugene.berta@inria.fr
Affiliation:
INRIA, Paris
Affiliation:
Ecole Normale Supérieure, PSL Research University, Paris
David Holzmüller
†
†
thanks:
david.holzmuller@inria.fr
Affiliation:
INRIA, Paris
Affiliation:
Ecole Normale Supérieure, PSL Research University, Paris
Michael I. Jordan
Affiliation:
INRIA, Paris
Affiliation:
University of California, Berkeley
Francis Bach
Affiliation:
INRIA, Paris
Affiliation:
Ecole Normale Supérieure, PSL Research University, Paris
Abstract
Machine learning classifiers often produce probabilistic predictions that are critical for accurate and interpretable decision-making in various domains.
The quality of these predictions is generally evaluated with proper losses, such as cross-entropy, which decompose into two components:
calibration error
assesses general under/overconfidence, while
refinement error
measures the ability to distinguish different classes.
In this paper, we present a novel variational formulation of the calibration-refinement decomposition that sheds new light on post-hoc calibration, and enables rapid estimation of the different terms.
Equipped with this new perspective, we provide theoretical and empirical evidence that calibration and refinement errors are not minimized simultaneously during training.
Selecting the best epoch based on validation loss thus leads to a compromise point that is suboptimal for both terms.
To address this, we propose minimizing refinement error only during training (
Refine,…
), before minimizing calibration error post hoc, using standard techniques (
…then Calibrate
).
Our method integrates seamlessly with any classifier and consistently improves performance across diverse classification tasks.
Keywords
Classification
⋅
\cdot
Early stopping
⋅
\cdot
Calibration
⋅
\cdot
Proper Scoring Rules
1
Introduction
Accurate classification lies at the heart of many machine learning applications, from medical diagnosis and fraud detection to autonomous driving and weather forecasting.
Modern classifiers predict not only a class label but also a probability vector reflecting the model’s confidence that the instance belongs to each class.
These probabilistic outputs are essential for informed downstream decision-making, especially in high-stakes scenarios where uncertainty must be explicitly accounted for.
Despite their widespread use, many machine learning models, especially complex models such as neural networks, tend to produce poorly calibrated probabilities
(
Guo et al., 2017
)
, meaning that the predicted scores do not align with real-world probabilities, leading to overconfident or underconfident predictions that can undermine reliability and trustworthiness.
This issue has mostly been considered through the lens of post-hoc calibration, which consists in adjusting the predicted probabilities after training, using a small held-out portion of the dataset. An overlooked aspect of the problem is that the calibration error contributes to the total loss of a classifier
(
Bröcker, 2009
)
. In
Figure
1
, we plot the decomposition into calibration error and refinement error of the classification loss (here cross-entropy) on the validation set during training for a deep neural network. We observe that the two errors are not minimized simultaneously. The resulting loss minimizer thus has a non-zero calibration error and is suboptimal for refinement. This accords with a recent empirical observation of
Ranjan et al. (2024)
, who noted that selecting the training epoch at which to stop based on classification loss after post-hoc transformations yields large performance gains. In this paper, we provide a general theoretical understanding of this phenomenon by introducing a novel variational formulation of the calibration-refinement decomposition. Our analysis reveals that there is room for improvement in the way we train probabilistic classifiers in general.
Figure 1:
Calibration-refinement decomposition during training.
We plot the calibration (blue curve) and refinement (red curve) terms of the validation cross-entropy loss (green curve)—measured with our estimator from
Section
4
—for a deep neural network (ResNet-18) trained on a computer vision dataset (CIFAR-10). Calibration error and refinement error are not minimized simultaneously, the loss minimizer (green dot) is thus suboptimal for both. See
Appendix
E
for more details on the training procedure.
In
Section
3
, we introduce novel variational formulations of the different terms in the classical decompositions of proper losses (calibration, refinement, sharpness). We first show that the refinement error of a probabilistic classifier
f
f
can be written variationally as
min
g
⁡
Risk
​
(
g
∘
f
)
\min_{g}\text{Risk}(g\circ f)
, where the minimum is taken over all measurable functions. Since risk is calibration plus refinement, we also have that calibration error is
Risk
​
(
f
)
−
min
g
⁡
Risk
​
(
g
∘
f
)
\text{Risk}(f)-\min_{g}\text{Risk}(g\circ f)
.
This reformulation sheds light on post-hoc calibration in general, demonstrating that selecting the recalibration function
g
∗
g^{*}
that minimizes the empirical risk of
g
∘
f
g\circ f
in a class of post-hoc calibration functions
g
∈
𝒢
g\in\mathcal{G}
is a principled way to remove the calibration error.
The resulting risk after recalibration is a simple refinement error estimator while the risk difference before and after recalibration is a calibration error estimator.
The contributions of calibration and refinement errors to the total classification loss can thus be estimated simply by fitting a recalibration function.
In
Section
4
we propose using the loss after temperature scaling as a refinement estimator, which applies to both binary and multiclass classifiers.
To track calibration and refinement errors during training, our estimator requires fitting a recalibration function after each epoch.
We make this approach practical by developing an efficient implementation based on temperature scaling that yields an efficient proxy for minimization over all measurable functions.
Equipped with the ability to track calibration and refinement errors during training (as in
Figure
1
), we observe empirically for a variety of machine learning models that these two terms are not minimized simultaneously. The traditional validation loss minimizer selected by early stopping therefore does not minimize either the calibration error or the refinement error.
To address this limitation of the standard training paradigm, we propose minimizing only the refinement error during training, preventing the variations in calibration error from contaminating our early stopping metric, and taking advantage of the fact that it can be minimized after training.
In
Section
5
, we show empirically that early stopping based on refinement error, as estimated by fitting a simple recalibration function after each iteration, yields smaller loss at test time across various architectures and data modalities.
Far from restricting classification performance, carefully dealing with refinement and calibration errors allows for smaller loss at test time, whatever the proper score of interest.
We also initiate the theoretical study of this phenomenon in Sections
6
and
7
, which focuses in the simplified setting of high-dimensional regularized logistic regression.
In this setting, we demonstrate theoretically that calibration and refinement errors are minimized for different values of the regularization parameter. Thus, refinement-based early stopping provably achieves significant loss reduction by minimizing both refinement error (during training) and calibration error (post hoc).
Our mathematical model allows us to study the impact of problem parameters on calibration and refinement minimizers, and we uncover the existence of different regimes exhibiting differential rates of convergence for these two minimizers depending on the nature of the problem.
The estimated refinement error can also be used for tuning hyper-parameters, or as a stopping metric in any iterative machine learning algorithm, making our method broadly applicable.
To facilitate practical adoption, we make our refinement estimator available in the package
github.com/dholzmueller/probmetrics
.
2
Related work
Proper scoring rules.
Proper scoring rules are fundamental tools for assessing the quality of probabilistic forecasts. For a comprehensive overview, see
Gneiting and Raftery (2007)
.
From a decision-theoretic perspective, proper scoring rules arise naturally: the loss incurred by choosing the Bayes optimal action under the predictive distribution is an instance of a proper scoring rule
(
Grünwald and Dawid, 2004
)
.
This framework enables the properization of scoring rules that are not inherently proper
(
Brehmer and Gneiting, 2020
)
.
Decompositions of proper scores.
For the Brier score
(
Brier, 1950
)
, the calibration-refinement decomposition (
1
) was introduced by
Sanders (1963)
and the calibration-sharpness decomposition (
2
) was introduced by
Murphy (1973)
.
Bröcker (2009)
extended these ideas to general proper scoring rules.
Kull and Flach (2015)
reformulated these decompositions purely in terms of divergences between different random variables and introduced additional components such as irreducible, epistemic, and grouping loss.
Alternative formulations have also been proposed by
Pohle (2020)
.
However, none of these prior works provide a variational interpretation of such decompositions.
Calibration.
Calibration has been the focus of renewed attention after
Guo et al. (2017)
observed that neural networks often exhibit miscalibration.
They also noted that logloss tends to overfit earlier than accuracy during training.
Later studies
(
Minderer et al., 2021
;
Tao et al., 2024
)
emphasized that model calibration can vary significantly with architectural and training choices.
To address miscalibration, a wide range of post-hoc methods have been developed.
These include variants of logistic regression, such as Platt scaling
(
Platt, 1999
)
, Temperature/Vector/Matrix scaling
(
Guo et al., 2017
)
, Beta calibration
(
Kull et al., 2017
)
, and Dirichlet calibration
(
Kull et al., 2019
)
.
Another family of methods stems from isotonic regression
(
Robertson et al., 1988
;
Zadrozny and Elkan, 2002
;
Oron and Flournoy, 2017
;
Vovk et al., 2015
;
Manokhin, 2017
;
Berta et al., 2024
)
.
Binning-based techniques also exist
(
Naeini et al., 2015
, e.g.,)
, though these are more commonly used for estimating calibration error than for recalibration itself.
Wang et al. (2021)
demonstrate that changing the training loss function can improve calibration before, but not after post-hoc calibration.
Post-hoc calibration and proper scores.
Several recent works relate post-hoc calibration to proper scoring rules.
Gruber and Buettner (2022)
evaluate post-hoc methods using a quantity akin to loss, and
Gruber and Bach (2025)
propose a variational formulation for optimizing squared calibration error estimators.
Dimitriadis et al. (2021)
evaluate miscalibration and discrimination for binary classifiers using the Brier score after Isotonic Regression.
Ranjan et al. (2024)
propose using the loss after post-hoc transformation for selecting the best epoch, without making the link with refinement error or proper scores.
Ferrer and Ramos (2024)
propose assessing calibration quality via the loss reduction achieved through recalibration.
The importance of optimizing the total loss and not only calibration error is emphasized, for example, by
Perez-Lebel et al. (2023)
,
Chidambaram and Ge (2024)
, and
Ferrer and Ramos (2024)
.
While our method employs a refinement estimator,
Perez-Lebel et al. (2023)
propose a grouping loss estimator that could be applicable in our case, given that the irreducible loss component is independent of
f
f
. However, grouping loss is more challenging to estimate than refinement loss, since the former can also capture the irreducible risk
inf
f
Risk
⁡
(
f
)
\inf_{f}\Risk(f)
.
High dimensional asymptotics of classification.
Our asymptotic analysis of classification and refinement errors for regularized logistic regression in high dimensions builds on a well-established line of work.
Dobriban and Wager (2018)
;
Mai et al. (2019)
study classification error under the same data model and provide asymptotic results that are directly relevant to our setting. Related scenarios have also been analyzed by
Couillet et al. (2018)
;
Salehi et al. (2019)
.
More recently,
Bach (2024)
provides a novel perspective on these high-dimensional results through the lens of self-induced regularization, which may help interpret our expressions for calibration and refinement errors.
3
Calibration-Refinement decomposition
We begin with an overview of the classical decompositions of proper losses into calibration and refinement errors, or calibration, sharpness and uncertainty. We then present variational formulations of these decompositions that allow new interpretations of the various terms. Notably, the calibration error measures how much the loss can be decreased by optimal post-processing and the refinement error measures the remaining loss after this optimal post-processing.
Notation.
Consider classification with
k
k
classes. Let
Δ
k
\Delta_{k}
denote the probability simplex
{
p
∈
[
0
,
1
]
k
|
1
⊤
​
p
=
1
}
\{p\in[0,1]^{k}\;|\;\mathbf{1}^{\top}p=1\}
and
𝒴
k
⊂
Δ
k
\mathcal{Y}_{k}\subset\Delta_{k}
the space of one-hot encoded labels
y
∈
{
0
,
1
}
k
y\in\{0,1\}^{k}
with
y
i
=
1
y_{i}=1
if the true class is
i
i
and
y
i
=
0
y_{i}=0
otherwise. Assume we have a random variable
X
∈
𝒳
X\in\mathcal{X}
(the feature vector), such that there is an unknown joint probability distribution
𝒟
\mathcal{D}
on
(
X
,
Y
)
(X,Y)
. We make probabilistic predictions
p
∈
Δ
k
p\in\Delta_{k}
for the value of the true label
Y
Y
using a statistical model
f
:
𝒳
→
Δ
k
f:\mathcal{X}\rightarrow\Delta_{k}
.
3.1
Proper losses
We evaluate predictions with a loss function
ℓ
:
Δ
k
×
𝒴
k
→
ℝ
+
\ell:\Delta_{k}\times\mathcal{Y}_{k}\rightarrow\mathbb{R}_{+}
.
ℓ
\ell
is a nonnegative function of
p
p
and
y
y
such that
ℓ
⁡
(
p
,
y
)
\ell(p,y)
assesses the quality of prediction
p
p
for label
y
y
.
Well-known examples include the Brier score
(
Brier, 1950
)
,
ℓ
⁡
(
p
,
y
)
=
‖
y
−
p
‖
2
2
\ell(p,y)=\|y-p\|_{2}^{2}
, and the cross-entropy (logloss)
(
Shannon, 1948
)
,
ℓ
(
p
,
y
)
=
−
∑
i
=
1
k
y
i
log
(
p
i
)
\ell(p,y)=-\sum_{i=1}^{k}y_{i}\log(p_{i})
.
Suppose the label
Y
Y
follows a categorical distribution
q
∈
Δ
k
q\in\Delta_{k}
, we denote
ℓ
⁡
(
p
,
q
)
\ell(p,q)
the expected loss
𝔼
Y
∼
q
​
[
ℓ
​
(
p
,
Y
)
]
\mathbb{E}_{Y\sim q}[\ell(p,Y)]
obtained with forecast
p
p
.
A natural requirement for our loss function
ℓ
\ell
is that it should be minimized when the predicted distribution
p
p
matches the true target distribution
q
q
. Losses that verify this property are called
proper
.
Formally, we follow
Gneiting and Raftery (2007)
but reverse the sign such that proper losses should be minimized instead of maximized:
Definition 3.1
(Proper loss function)
.
We consider losses
ℓ
:
Δ
k
×
𝒴
k
→
ℝ
∪
{
∞
}
\ell:\Delta_{k}\times\mathcal{Y}_{k}\to\mathbb{R}\cup\{\infty\}
such that for any
p
∈
Δ
k
p\in\Delta_{k}
,
ℓ
⁡
(
p
,
⋅
)
\ell(p,\cdot)
is measurable and quasi-integrable with respect to any
q
∈
Δ
k
q\in\Delta_{k}
. This allows to define
ℓ
⁡
(
p
,
q
)
≔
𝔼
Y
∼
q
​
[
ℓ
⁡
(
p
,
Y
)
]
\ell(p,q)\coloneqq\mathbb{E}_{Y\sim q}[\ell(p,Y)]
, taking values in
ℝ
∪
{
∞
}
\mathbb{R}\cup\{\infty\}
. If
ℓ
⁡
(
q
,
q
)
≤
ℓ
⁡
(
p
,
q
)
\ell(q,q)\leq\ell(p,q)
for all
p
p
and
q
q
,
ℓ
\ell
is said to be
proper
.
If the inequality holds with equality only for
p
=
q
p=q
,
ℓ
\ell
is
strictly proper
.
The integrability conditions could be further relaxed to use convex subsets of
Δ
k
\Delta_{k}
, which we omit for simplicity.
Leaving aside the technical details, the important takeaway is that loss functions generally used in machine learning such as the Brier score and logloss are strictly proper.
3.2
Decompositions
Let
d
ℓ
​
(
p
,
q
)
≔
ℓ
⁡
(
p
,
q
)
−
ℓ
⁡
(
q
,
q
)
d_{\ell}(p,q)\coloneqq\ell(p,q)-\ell(q,q)
and
e
ℓ
​
(
q
)
≔
ℓ
⁡
(
q
,
q
)
e_{\ell}(q)\coloneqq\ell(q,q)
be the divergence and entropy associated with loss function
ℓ
\ell
(we refer to these as
ℓ
\ell
-divergence and
ℓ
\ell
-entropy). For different choices of
ℓ
\ell
, we recover well-known entropy and divergence functions.
Loss
ℓ
\ell
Divergence
d
ℓ
d_{\ell}
Entropy
e
ℓ
e_{\ell}
Logloss
KL divergence
Shannon entropy
−
∑
i
y
i
log
(
p
i
)
-\sum_{i}y_{i}\log(p_{i})
∑
i
q
i
​
log
⁡
q
i
p
i
\sum_{i}q_{i}\log\frac{q_{i}}{p_{i}}
−
∑
i
q
i
log
q
i
-\sum_{i}q_{i}\log q_{i}
Brier score
Squared distance
Gini index
‖
y
−
p
‖
2
2
\|y-p\|_{2}^{2}
‖
p
−
q
‖
2
2
\|p-q\|_{2}^{2}
∑
i
q
i
​
(
1
−
q
i
)
\sum_{i}q_{i}(1-q_{i})
Given a probabilistic classifier
f
f
, let
C
≔
𝔼
𝒟
​
[
Y
|
f
⁡
(
X
)
]
C\coloneqq\mathbb{E}_{\mathcal{D}}[Y|f(X)]
denote the conditional expectation of
Y
Y
given the prediction
f
⁡
(
X
)
f(X)
. We refer to values of
C
C
as
calibrated scores
.
The risk of
f
f
is measured with a proper loss
ℓ
\ell
satisfies the following “calibration-refinement decomposition”
(
Bröcker, 2009
)
:
Risk
⁡
(
f
)
=
𝔼
⁡
[
ℓ
⁡
(
f
⁡
(
X
)
,
Y
)
]
=
𝔼
⁡
[
d
ℓ
​
(
f
⁡
(
X
)
,
C
)
]
⏟
𝒦
ℓ
​
(
f
)
+
𝔼
​
[
e
ℓ
​
(
C
)
]
⏟
ℛ
ℓ
​
(
f
)
.
\Risk(f)=\mathbb{E}[\ell(f(X),Y)]=\underbrace{\mathbb{E}[d_{\ell}(f(X),C)]}_{\mathcal{K}_{\ell}(f)}+\underbrace{\mathbb{E}[e_{\ell}(C)]}_{\mathcal{R}_{\ell}(f)}.
(1)
The first term in decomposition (
1
) is the
calibration error
𝒦
ℓ
​
(
f
)
\mathcal{K}_{\ell}(f)
associated with
ℓ
\ell
. The second term, denoted
ℛ
ℓ
​
(
f
)
\mathcal{R}_{\ell}(f)
, is the
refinement error
for
ℓ
\ell
.
The refinement term can be further decomposed into the
uncertainty
𝒰
ℓ
​
(
Y
)
\mathcal{U}_{\ell}(Y)
of
Y
Y
(notice that it is independent of
f
f
) and a
sharpness
term
𝒮
ℓ
​
(
f
)
\mathcal{S}_{\ell}(f)
, yielding the “calibration-sharpness decomposition”
(
Bröcker, 2009
)
:
Risk
⁡
(
f
)
=
𝔼
⁡
[
ℓ
⁡
(
f
⁡
(
X
)
,
Y
)
]
=
𝔼
⁡
[
d
ℓ
​
(
f
⁡
(
X
)
,
C
)
]
⏟
𝒦
ℓ
​
(
f
)
+
e
ℓ
​
(
𝔼
​
[
Y
]
)
⏟
𝒰
ℓ
​
(
Y
)
−
OPEN
𝔼
⁡
[
d
ℓ
​
(
𝔼
⁡
[
Y
]
,
C
)
]
)
⏟
𝒮
ℓ
​
(
f
)
⏟
ℛ
ℓ
​
(
f
)
.
\Risk(f)=\mathbb{E}[\ell(f(X),Y)]=\underbrace{\mathbb{E}[d_{\ell}(f(X),C)]}_{\mathcal{K}_{\ell}(f)}+\underbrace{\underbrace{e_{\ell}(\mathbb{E}[Y])}_{\mathcal{U}_{\ell}(Y)}-\underbrace{\mathbb{E}[d_{\ell}(\mathbb{E}[Y],C)])}_{\mathcal{S}_{\ell}(f)}}_{\mathcal{R}_{\ell}(f)}~.
(2)
Alternatively, refinement error can be decomposed into the irreducible loss (risk of the optimal classifier
f
∗
f^{*}
), and the grouping loss
(
Bröcker, 2009
;
Kull and Flach, 2015
;
Perez-Lebel et al., 2023
)
; see
Appendix
A
for more details.
3.3
Calibration error
Calibration has been the subject of a significant body of research on its own, not only in the context of the calibration-refinement decomposition. A classifier
f
f
is said to be
calibrated
if
f
⁡
(
X
)
=
C
f(X)=C
almost surely. When this is satisfied, for a given prediction
f
⁡
(
X
)
=
p
f(X)=p
, the expected outcome
𝔼
𝒟
​
[
Y
|
f
​
(
X
)
=
p
]
\mathbb{E}_{\mathcal{D}}[Y|f(X)=p]
is aligned with
p
p
. This is a desirable property in that it yields model predictions that are interpretable as the probabilities that
Y
Y
belongs to each of the
k
k
classes.
Remark 3.2
.
Calibration is traditionally defined as
ℙ
𝒟
​
(
Y
|
f
⁡
(
X
)
)
=
f
⁡
(
X
)
\mathbb{P}_{\mathcal{D}}(Y|f(X))=f(X)
almost surely.
Notice that since labels
Y
∈
{
0
,
1
}
k
Y\in\{0,1\}^{k}
are one-hot encoded, the conditional expectation
C
=
𝔼
𝒟
​
[
Y
|
f
​
(
X
)
]
C=\mathbb{E}_{\mathcal{D}}[Y|f(X)]
matches the conditional class probabilities
ℙ
𝒟
​
(
Y
|
f
​
(
X
)
)
\mathbb{P}_{\mathcal{D}}(Y|f(X))
.
Calibration error.
Model miscalibration is measured by the expected gap between
f
⁡
(
X
)
f(X)
and
C
C
. The choice of a distance or divergence function
d
d
gives rise to different notions of
calibration error
:
𝒦
(
d
)
​
(
f
)
=
𝔼
⁡
[
d
⁡
(
f
⁡
(
X
)
,
C
)
]
\mathcal{K}^{(d)}(f)=\mathbb{E}[d(f(X),C)]
. A popular choice for
d
d
is the
L
1
L^{1}
distance, resulting in the expected calibration error
(
Naeini et al., 2015
, ECE,)
. Note that when choosing the
L
2
L^{2}
distance or KL divergence, we recover “proper” calibration errors
(
Gruber and Buettner, 2022
)
that appear in the decomposition of the Brier score and the logloss.
In practice, the distribution
𝒟
\mathcal{D}
is only known via a finite set of samples,
(
x
i
,
y
i
)
1
≤
i
≤
n
(x_{i},y_{i})_{1\leq i\leq n}
, and
f
f
makes continuous predictions
f
⁡
(
x
i
)
∈
Δ
k
f(x_{i})\in\Delta_{k}
. To compute the calibration error,
C
C
is often estimated by binning predictions on the simplex, resulting in estimators that are biased and inconsistent
(
Kumar et al., 2019
;
Vaicenavicius et al., 2019
;
Roelofs et al., 2022
)
. In the multi-class case, the curse of dimensionality makes estimation even more difficult. Weaker notions such as class-wise or top-label calibration error are often used
(
Kumar et al., 2019
;
Kull et al., 2019
)
.
Post-hoc calibration.
Many machine learning classifiers suffer from calibration issues, which has given rise to a family of techniques known as “post-hoc calibration.” These methods reduce calibration error after training using a reserved set of samples
𝒞
\mathcal{C}
called a “calibration set.” Well-known examples include isotonic regression and temperature scaling.
Isotonic regression
(
Zadrozny and Elkan, 2002
, IR,)
finds the monotonic function
g
∗
g^{*}
that minimizes the risk of
g
∘
f
g\circ f
on the calibration set. It is a popular calibration technique for binary classifiers. However, the multi-class extensions come with important drawbacks.
Temperature scaling
(
Guo et al., 2017
, TS,)
optimizes a scalar parameter
β
\beta
to rescale the log-probabilities. Formally, it learns the function
g
β
∗
g_{\beta^{*}}
on the calibration set with
β
∗
\displaystyle\beta^{*}
≔
\displaystyle\coloneqq
argmin
β
∈
ℝ
+
⁡
ℒ
⁡
(
β
)
,
\displaystyle\argmin_{\beta\in\mathbb{R}_{+}}\mathcal{L}(\beta),
ℒ
⁡
(
β
)
\displaystyle\mathcal{L}(\beta)
≔
\displaystyle\coloneqq
∑
(
x
,
y
)
∈
𝒞
ℓ
⁡
(
g
β
​
(
f
⁡
(
x
)
)
,
y
)
,
\displaystyle\sum_{(x,y)\in\mathcal{C}}\ell(g_{\beta}(f(x)),y),
(3)
g
β
​
(
p
)
\displaystyle g_{\beta}(p)
≔
\displaystyle\coloneqq
softmax
⁡
(
β
​
log
⁡
(
p
)
)
.
\displaystyle\softmax(\beta\log(p))~.
For neural networks, this comes down to rescaling the last layer by
β
∗
\beta^{*}
. TS has many advantages: it is efficient, applies to multi-class problems, does not affect accuracy, and is robust to overfitting since it only has one parameter.
We refer the interested reader to
Silva Filho et al. (2023)
for a detailed review of calibration.
3.4
Refinement error
Given the appeal of calibrated predictions, significant effort has been devoted to estimating and reducing calibration error. The fact that it interacts with another term to form the overall risk of the classifier, however, has received much less attention. This is partly due to the fact that refinement error is not well known. So what exactly is refinement?
In decomposition (
1
), refinement appears as the expected
ℓ
\ell
-entropy of
Y
Y
given
f
⁡
(
X
)
f(X)
:
ℛ
ℓ
​
(
f
)
=
𝔼
⁡
[
e
ℓ
​
(
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
)
]
\mathcal{R}_{\ell}(f)=\mathbb{E}[e_{\ell}(\mathbb{E}[Y|f(X)])]
. We see that if
Y
Y
is fully determined by
f
⁡
(
X
)
f(X)
,
Y
|
f
⁡
(
X
)
Y|f(X)
has no entropy and the refinement error is null. In contrast, if
Y
|
f
⁡
(
X
)
Y|f(X)
is as random as
Y
Y
, it is maximal. Refinement error thus quantifies how much of the variability in
Y
Y
is captured by
f
⁡
(
X
)
f(X)
, with a lower error indicating greater information. Just like classification error, it assesses the ability to distinguish between classes independently of calibration issues such as over/under-confidence. It provides a much more comprehensive measure, however, as it considers the entire distribution of
f
⁡
(
X
)
f(X)
rather than a single discretization. This comes at a cost; in particular, as with the calibration error, it is much harder to estimate.
Remark 3.3
.
As we have seen in decomposition (
2
), refinement can be further decomposed into the uncertainty
𝒰
ℓ
​
(
Y
)
\mathcal{U}_{\ell}(Y)
of
Y
Y
minus a sharpness term
𝒮
ℓ
​
(
f
)
=
𝔼
⁡
[
d
ℓ
​
(
𝔼
⁡
[
Y
]
,
C
)
]
\mathcal{S}_{\ell}(f)=\mathbb{E}[d_{\ell}(\mathbb{E}[Y],C)]
, which quantifies the expected gap between the calibrated scores and the best constant predictor
𝔼
⁡
[
Y
]
\mathbb{E}[Y]
.
Intuitively, we see that the more information
f
⁡
(
X
)
f(X)
contains about
Y
Y
, the more
C
C
will deviate from
𝔼
⁡
[
Y
]
\mathbb{E}[Y]
, the larger the sharpness. Sharpness and refinement both measure the discrimination power of the classifier
f
f
; note, however that larger sharpness corresponds to smaller refinement.
For a fixed data distribution
𝒟
\mathcal{D}
, the uncertainty
𝒰
ℓ
​
(
Y
)
\mathcal{U}_{\ell}(Y)
is constant, so sharpness and refinement are the same up to a constant term.
In this paper, we choose to consider refinement error, to avoid the need to include an additional constant term in the loss decomposition, but our methods apply directly to sharpness.
3.5
A variational formulation
0
0
Risk
⁡
(
f
∗
)
\displaystyle\Risk(f^{*})
=
min
f
⁡
Risk
⁡
(
f
)
\displaystyle=\min_{f}\Risk(f)
Risk
⁡
(
g
∗
∘
f
)
\displaystyle\Risk(g^{*}\circ f)
=
min
g
⁡
Risk
⁡
(
g
∘
f
)
\displaystyle=\min_{g}\Risk(g\circ f)
Risk
⁡
(
f
)
\Risk(f)
Risk
⁡
(
c
∗
)
\displaystyle\Risk(c^{*})
=
min
c
​
constant
⁡
Risk
⁡
(
c
)
\displaystyle=\min_{c\text{ constant}}\Risk(c)
cal. err.
grp. loss
irred. loss
refinement error
reducible loss
sharpness
Figure 2:
Relation between different terms relating to proper scoring rules, proven in
Theorem
3.4
. Here, infima are over measurable functions. A line
A
u
B
A\stackrel{{\scriptstyle u}}{{\rule[2.15277pt]{20.00003pt}{0.4pt}}}B
means
u
=
B
−
A
u=B-A
. “irred.” stands for irreducible and “grp.” for grouping. For the definitions, see
Remark
A.1
.
We introduce novel variational formulations of the terms in decompositions (
1
) and (
2
).
Figure
2
illustrates the relation between terms in these decompositions under this variational perspective (proofs and additional details are deferred to
Appendix
A
).
Theorem 3.4
.
Let
k
≥
2
k\geq 2
, let
ℓ
:
Δ
k
×
𝒴
k
→
ℝ
∪
{
∞
}
\ell:\Delta_{k}\times\mathcal{Y}_{k}\to\mathbb{R}\cup\{\infty\}
be a proper loss, and let
f
:
𝒳
→
Δ
k
f:\mathcal{X}\to\Delta_{k}
be measurable, where
Δ
k
\Delta_{k}
is equipped with the Borel
σ
\sigma
-algebra. Then,
ℛ
ℓ
​
(
f
)
\displaystyle\mathcal{R}_{\ell}(f)
=
\displaystyle=
min
g
⁡
Risk
⁡
(
g
∘
f
)
,
\displaystyle\min_{g}\Risk(g\circ f)~,
𝒦
ℓ
​
(
f
)
\displaystyle\mathcal{K}_{\ell}(f)
=
\displaystyle=
Risk
⁡
(
f
)
−
min
g
⁡
Risk
⁡
(
g
∘
f
)
,
\displaystyle\Risk(f)-\min_{g}\Risk(g\circ f)~,
𝒮
ℓ
​
(
f
)
\displaystyle\mathcal{S}_{\ell}(f)
=
\displaystyle=
min
c
​
constant
⁡
Risk
⁡
(
c
)
−
min
g
⁡
Risk
⁡
(
g
∘
f
)
,
\displaystyle\min_{c\text{ constant}}\Risk(c)-\min_{g}\Risk(g\circ f)~,
𝒰
ℓ
​
(
Y
)
\displaystyle\mathcal{U}_{\ell}(Y)
=
\displaystyle=
min
c
​
constant
⁡
Risk
⁡
(
c
)
.
\displaystyle\min_{c\text{ constant}}\Risk(c)~.
Here, the minima are over measurable functions
g
:
Δ
k
→
Δ
k
g:\Delta_{k}\to\Delta_{k}
and
c
:
𝒳
→
Δ
k
c:\mathcal{X}\to\Delta_{k}
. They are attained by
g
∗
​
(
q
)
≔
𝔼
⁡
[
Y
|
f
⁡
(
X
)
=
q
]
g^{*}(q)\coloneqq\mathbb{E}[Y|f(X)=q]
and
c
∗
​
(
x
)
≔
𝔼
​
[
Y
]
c^{*}(x)\coloneqq\mathbb{E}[Y]
. If
ℓ
\ell
is strictly proper, the minimizers are unique up to
P
f
⁡
(
X
)
P_{f(X)}
-null sets.
This variational formulation provides a new perspective on post-hoc calibration, showing that minimizing the risk of
g
∘
f
g\circ f
is a principled way to remove the calibration error of
f
f
.
Indeed, we see that calibration error evaluates the difference between the original risk and the risk after optimal recalibration.
This optimal relabeling is given by the calibrated score
C
=
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
C=\mathbb{E}[Y|f(X)]
.
Refinement error thus measures the risk that remains after optimal re-labeling, in other words the risk of the calibrated scores.
This suggests that the refinement error can be estimated using the risk after post-hoc calibration by the difference between risk before and risk after recalibration.
Note that this yields simple calibration (and refinement) error estimators even in the multi-class case, which to the best of our knowledge, is a problem with no satisfactory answer in the existing literature.
4
Our method: refinement-based stopping
Figure 3:
risk-based versus refinement-based early stopping, before and after post-hoc calibration. Dots denote risk (green), refinement (red) and calibration (blue) errors.
4.1
Refinement-based early stopping: the intuition
Two distinct minimizers.
Minimizing the risk of a classifier comes down to minimizing simultaneously refinement and calibration errors. Empirically, these two errors are not minimized simultaneously during training, as in
Figure
1
. One possible scenario, archetypal in deep learning, is that the training set becomes well separated, forcing the model to make very confident predictions to keep training calibration error small. In case of a train-test generalization gap, the model becomes over-confident on test data
(
Carrell et al., 2022
)
while refinement error could still decrease. Empirically, as we will see, we observe separate minimizers for the two errors across various machine learning models, whether through iterative training or when tuning a regularization parameter. In
Section
7
, we analyze this phenomenon theoretically for high-dimensional logistic regression, showing that it arises even in very simple settings. The consequence is that risk-based early stopping finds a compromise point between two conflicting objectives: calibration error minimization and refinement error minimization. This corroborates the widely recognized observation that many models are poorly calibrated after training
(
Guo et al., 2017
)
.
Refine, then calibrate.
The question that now arises is: how do we find a model that is optimal for both calibration and refinement? In general, strictly increasing post-hoc calibration techniques such as TS leave refinement unchanged.
Berta et al. (2024)
showed that binary isotonic regression preserves the ROC convex hull, a proxy for refinement. Given that calibration error is minimized after training, with no impact on refinement, we argue that training should be dedicated to the latter only. We propose selecting the best epoch based on validation refinement error instead of validation loss as a new training paradigm for machine learning classifiers. As illustrated in
Figure
3
this procedure leads to smaller loss after post-hoc calibration. Compared with the standard paradigm that minimizes both refinement and calibration during training, we propose
refining
during training, then
calibrating
post hoc.
Early stopping
Training minimizes
Post hoc minimizes
Risk
Cal. + Ref.
Cal.
Refinement
Ref.
Cal.
4.2
Refinement-based stopping made practical
Refinement estimation.
As discussed earlier, calibration error estimators are biased, inconsistent, and break in the multi-class case. Since refinement is risk minus calibration, these issues carry over to refinement estimation. One could circumvent this by using proxies like validation accuracy.
Theorem
3.4
provides a better alternative: refinement error equals risk after optimal relabeling
g
∗
∘
f
g^{*}\circ f
. We thus need to estimate how small the validation risk can be by re-labeling predictions. Since the validation set
(
x
i
,
y
i
)
1
≤
i
≤
n
(x_{i},y_{i})_{1\leq i\leq n}
is finite, minimizing over all measurable functions
g
:
Δ
k
→
Δ
k
g:\Delta_{k}\rightarrow\Delta_{k}
would lead to drastic overfitting. However, given a class of functions
𝒢
\mathcal{G}
that we intend to use for post-hoc calibration, we can estimate refinement error by solving:
ℛ
ℓ
^
​
(
f
)
=
min
g
∈
𝒢
⁡
1
n
​
∑
i
=
1
n
ℓ
⁡
(
g
⁡
(
f
⁡
(
x
i
)
)
,
y
i
)
\hat{\mathcal{R}_{\ell}}(f)=\min_{g\color[rgb]{1,0,0}\in\color[rgb]{1,0,0}\mathcal{G}}\frac{1}{n}\sum_{i=1}^{n}\ell(g(f(x_{i})),y_{i})
(4)
after every epoch. This comes down to selecting the best training epoch based on “validation loss after post-hoc calibration.” Although this is a biased estimator of refinement error, the fact that it can improve performance accords with a recent study by
Ranjan et al. (2024)
, who report performance gains when selecting the best training epoch based on losses after different post-hoc transformations.
Our observation that calibration and refinement errors are not minimized simultaneously, and our variational formulation of refinement, provide a theoretical grounding for understanding this kind of empirical observation.
Returning to
Equation
4
, note that when compared with
Theorem
3.4
, in
Equation
4
we limit ourselves to functions in class
𝒢
\mathcal{G}
. A trade-off arises vis-a-vis the size of
𝒢
\mathcal{G}
. Larger function classes can detect more complex mis-calibration patterns but are more prone to overfitting the validation set, resulting in poor estimation of the true refinement error.
For our method to work, we need to choose a small class
𝒢
\mathcal{G}
that comes as close as possible to the optimal re-mapping
g
∗
​
(
f
)
=
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
g^{*}(f)=\mathbb{E}[Y|f(X)]
.
TS-refinement for neural nets.
We let “TS-refinement” refer to the estimator obtained when
𝒢
\mathcal{G}
is the class of functions generated by temperature scaling. It is parametrized by a single scalar parameter, limiting the danger of overfitting the validation set. Moreover, TS is very effective at reducing the calibration error of neural networks (however large it is) while leaving refinement unchanged. This is supported by a plethora of empirical evidence
(
Guo et al., 2017
;
Wang et al., 2021
)
. Finally, we demonstrate in
Section
6
that under assumptions on the logit distribution, the optimal re-mapping
g
∗
g^{*}
is attained by TS, making TS-refinement a consistent estimator.
In practice, when training a neural network, we recommend selecting the best epoch in terms of validation loss after temperature scaling. Going back to the example in
Figure
1
, this procedure would select a later epoch (red dot), for which validation loss (green curve) is larger but validation loss after TS (red curve) is smaller. Given that we envisage using TS for post-hoc calibration anyway, this simple procedure guarantees a smaller validation risk.
Figure 4:
Runtime versus mean benchmark scores of different TS implementations.
Runtimes are averaged over validation sets with 10K+ samples. Evaluation is on XGBoost models trained with default parameters, using the epoch with the best validation accuracy.
Improving TS implementations.
Using TS-refinement for early stopping requires a fast and robust temperature-scaling implementation. Surveying existing codebases made it clear that there was room for improvement in terms of speed and even performance.
For the logloss, the objective
ℒ
⁡
(
β
)
\mathcal{L}(\beta)
in Eq. (
3
) is convex. Most existing implementations apply L-BFGS
Liu and Nocedal (1989)
to optimize
ℒ
⁡
(
1
/
T
)
\mathcal{L}(1/T)
, which is unimodal but nonconvex. Additionally, the step-size choice for L-BFGS sometimes led to suboptimal performance. Instead, since
ℒ
′
\mathcal{L}^{\prime}
is increasing by convexity of
ℒ
\mathcal{L}
, we propose using bisection to find a zero of
ℒ
′
\mathcal{L}^{\prime}
.
Figure
4
shows that on the benchmark from
Section
5
, our implementation achieves equal or lower test loss and is faster than alternatives from
Guo et al. (2017)
, TorchUncertainty, TorchCal
(
Ranjan, 2023
;
Feinman, 2021
)
, and AutoGluon
(
Erickson et al., 2020
)
. We provide details in
Appendix
D
.
Other estimators.
Our method applies to a wide range of machine learning models. It can help select the best step in any iterative training procedure (e.g., boosting) or the level of regularization for non-iterative models. Refinement does not have to be estimated with TS-refinement; any proxy available can be selected. Outside of the neural network setting, TS may be less effective. In the binary setting, using risk after isotonic regression (IR-refinement) might be a good option. It is consistent for a larger class of functions than TS-refinement since the class
𝒢
\mathcal{G}
contains all monotonic functions. The risk of overfitting becomes larger, however, and must be considered carefully.
5
Experiments
Computer Vision.
We benchmark our method by training a ResNet-18
(
He et al., 2016
)
and WideResNet (WRN)
(
Zagoruyko, 2016
)
on CIFAR-10, CIFAR-100 and SVHN datasets
(
Krizhevsky and Hinton, 2009
;
Netzer et al., 2011
)
. We reserve 10% of the training set for validation. We train for 300 epochs using SGD with momentum, weight decay, and a step learning rate scheduler. We use random cropping, horizontal flips, and cutout
(
DeVries, 2017
)
. For reference, this training procedures allows us to reach
95
%
95\%
accuracy on CIFAR-10 with the ResNet-18 and over
96
%
96\%
with the WRN. We train the models ten times on each dataset. The code to run the benchmark is available at
github.com/eugeneberta/RefineThenCalibrate-Vision
. On NVIDIA V100 GPUs, the benchmark took around 300 GPU hours to run.
In
Figure
5
we report the relative differences in test logloss obtained with different training procedures. After early stopping on validation loss (first column), using TS results in significant improvement (second column). Early stopping on TS-refinement instead of validation loss leads to even better results (third column). We also compare with validation-accuracy-based early stopping (fourth column), another refinement proxy, showing that TS-refinement more consistently yields smaller loss.
We observed empirically that the learning rate scheduler and regularization strength have an influence on the behavior of calibration error during training. This has consequences on the effect observed with our method. In general though, validation TS-refinement remains the best estimator available for test loss after temperature scaling. Brier score, another proper loss, is less sensitive than logloss to sharp variations in calibration error and can be a good alternative for early stopping for practitioners who want to avoid fitting TS every epoch. We refer the interested reader to
Appendix
E
for details on our training procedure and complete results.
Figure 5:
Relative differences in test logloss (lower is better) between logloss+TS and other procedures on vision datasets.
“+TS” indicates temperature scaling applied to the final model. Each dot represents a training run on one dataset. Box-plots show the 10%, 25%, 50%, 75%, and 90% quantiles. Relative differences (y-axis) are plotted using a log scale.
Tabular data
, where
X
X
is a vector of heterogeneous numerical and/or categorical features, is ubiquitous in ML applications. We take 196 binary and multi-class classification datasets from the benchmark from
Ye et al. (2024)
, containing between 1K and 100K samples after subsampling the largest datasets; see
Appendix
F
. We evaluate three methods:
•
XGBoost
(
Chen and Guestrin, 2016
)
is a popular implementation of gradient-boosted decision trees, with strong performance on tabular benchmarks
(
Grinsztajn et al., 2022
)
. Due to its iterative optimization, early stopping is relevant for XGBoost as well.
•
MLP
is a simple multilayer perceptron, similar to the popular MLP baseline by
Gorishniy et al. (2021)
.
•
RealMLP
(
Holzmüller et al., 2024
)
is a recent state-of-the-art deep learning model for tabular data
(
Ye et al., 2024
;
Erickson et al., 2025
)
, improving the standard MLP in many aspects.
For each dataset, we report the mean loss over five random splits into 64% training, 16% validation, and 20% test data. For each split, we run 30 random hyperparameter configurations and select the one with the best validation score. The validation set is also used for stopping and post-hoc calibration. Computations took around 40 hours on a 32-core CPU (for XGBoost) and four RTX 3090 GPUs (for NNs).
Figure 6:
Relative differences in test logloss (lower is better) between logloss+TS and other procedures on tabular datasets.
“+TS” indicates temperature scaling applied to the final model. Each dot represents one dataset from
Ye et al. (2024)
, using the 65 datasets with 10K+ samples. Percentages are clipped to
[
−
100,100
]
[-100,100]
due to one outlier with almost zero loss. Box-plots show the 10, 25, 50, 75, and 90% quantiles. Relative differences (y-axis) are plotted using a log scale.
Figure
6
shows the results on datasets with at least 10K samples. Generally, we observe that TS as well as stopping/tuning on TS-Refinement helps on most datasets, while stopping on accuracy often yields poor logloss even after TS. Our extended analysis in
Appendix
F
shows that results are more noisy and unclear for small or easy datasets. However, stopping on TS-Refinement frequently yields better accuracy and AUC than stopping on logloss, and hence strikes an excellent balance between different metrics.
6
Decomposition in the Gaussian data model
In this section and the next, we embark on a theoretical analysis that provides insight into the calibration-refinement decomposition. We demonstrate that even with a simple data model and predictor, calibration and refinement errors are not minimized simultaneously. This highlights the relevance of refinement-based early stopping and underscores the broad impact of the problem we address.
We use the following stylized model. Consider the feature and label random variables
X
∈
ℝ
p
,
Y
∈
{
−
1
,
1
}
X\in\mathbb{R}^{p},Y\in\{-1,1\}
under the two-class Gaussian model
X
∼
𝒩
⁡
(
μ
,
Σ
)
X\sim\mathcal{N}(\mu,\Sigma)
if
Y
=
1
Y=1
and
X
∼
𝒩
⁡
(
−
μ
,
Σ
)
X\sim\mathcal{N}(-\mu,\Sigma)
if
Y
=
−
1
Y=-1
for some mean
μ
∈
ℝ
p
\mu\in\mathbb{R}^{p}
and covariance
Σ
∈
ℝ
p
×
p
\Sigma\in\mathbb{R}^{p\times p}
. We further assume balanced classes,
ℙ
⁡
(
Y
=
1
)
=
ℙ
⁡
(
Y
=
−
1
)
=
1
2
\mathbb{P}(Y=1)=\mathbb{P}(Y=-1)=\frac{1}{2}
. Under this data model,
ℙ
⁡
(
Y
=
1
|
X
=
x
)
=
σ
⁡
(
w
∗
⊤
​
x
)
\mathbb{P}(Y=1|X=x)=\sigma({w^{*}}^{\top}x)
with
w
∗
=
2
​
Σ
−
1
​
μ
w^{*}=2\Sigma^{-1}\mu
and
σ
⁡
(
x
)
=
1
1
+
e
−
x
\sigma(x)=\frac{1}{1+e^{-x}}
denotes the sigmoid function. The sigmoid function’s shape is well suited to describe the posterior probability of
Y
Y
given
X
X
. Note that this holds for any pair
P
⁡
(
X
|
Y
=
±
1
)
P(X|Y=\pm 1)
from the same exponential family
(
Jordan, 1995
)
. Proofs for this section are deferred to
Appendix
B
.
We are interested in the calibration and refinement errors of the linear model
f
⁡
(
x
)
=
σ
⁡
(
w
⊤
​
x
)
f(x)=\sigma(w^{\top}x)
.
The weight vector
w
w
can be learned with techniques such as logistic regression or linear discriminant analysis
(
Fisher, 1936
)
. Denoting
a
w
=
⟨
w
,
w
∗
⟩
Σ
/
‖
w
‖
Σ
a_{w}=\langle w,w^{*}\rangle_{\Sigma}/\|w\|_{\Sigma}
with
⟨
w
,
w
∗
⟩
Σ
=
w
⊤
​
Σ
​
w
∗
\langle w,w^{*}\rangle_{\Sigma}=w^{\top}\Sigma w^{*}
and
‖
w
‖
Σ
=
w
⊤
​
Σ
​
w
\|w\|_{\Sigma}=\sqrt{w^{\top}\Sigma w}
, the error rate of the linear model can be written as
err
⁡
(
w
)
=
Φ
⁡
(
−
a
w
2
)
\err(w)=\Phi(-\frac{a_{w}}{2})
where
Φ
⁡
(
x
)
=
1
2
​
π
​
∫
−
∞
x
exp
⁡
(
−
t
2
2
)
​
𝑑
t
\Phi(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^{x}\exp(-\frac{t^{2}}{2})dt
is the cumulative distribution function of the standard normal distribution. Notice that
a
w
a_{w}
is invariant by rescaling of
w
w
. It measures the alignment with the best model
w
∗
w^{*}
independently of the weight vector’s norm. We refer to
a
w
a_{w}
as the “expertise level” of our model
f
f
. Interestingly,
a
w
a_{w}
also appears in the calibration and refinement errors for this simple model.
Proposition 6.1
.
For proper loss
ℓ
\ell
, the calibration and refinement errors of our model are
𝒦
ℓ
​
(
w
)
\displaystyle\mathcal{K}_{\ell}(w)
=
𝔼
⁡
[
d
ℓ
​
(
σ
⁡
(
‖
w
‖
Σ
​
(
z
+
a
w
2
)
)
,
σ
⁡
(
a
w
​
(
z
+
a
w
2
)
)
)
]
\displaystyle=\mathbb{E}\Big[d_{\ell}\Big(\sigma\Big(\|w\|_{\Sigma}\Big(z+\frac{a_{w}}{2}\Big)\Big),\sigma\Big(a_{w}\Big(z+\frac{a_{w}}{2}\Big)\Big)\Big)\Big]
ℛ
ℓ
​
(
w
)
\displaystyle\mathcal{R}_{\ell}(w)
=
𝔼
⁡
[
e
ℓ
​
(
σ
⁡
(
a
w
​
(
z
+
a
w
2
)
)
)
]
,
\displaystyle=\mathbb{E}\Big[e_{\ell}\Big(\sigma\Big(a_{w}\Big(z+\frac{a_{w}}{2}\Big)\Big)\Big)\Big]\,,
where the expectation is taken with respect to
z
∼
𝒩
⁡
(
0
,
1
)
z\sim\mathcal{N}(0,1)
.
Notice that the refinement error is a decreasing function of
a
w
a_{w}
, just like the error rate. Moreover, it depends on
w
w
via
a
w
a_{w}
only and so it is invariant by rescaling of the weight vector. In contrast, calibration error is not invariant by rescaling
w
w
. It is minimized, and reaches zero, when
‖
w
‖
Σ
=
a
w
\|w\|_{\Sigma}=a_{w}
. The larger the norm of the weight vector
‖
w
‖
Σ
\|w\|_{\Sigma}
, the larger the predicted probabilities
σ
⁡
(
w
⊤
​
x
)
\sigma(w^{\top}x)
, so
‖
w
‖
Σ
\|w\|_{\Sigma}
can be interpreted as the model’s “confidence level.”
The model is calibrated when this confidence level equals the expertise level
a
w
a_{w}
. A consequence is that there always exists a rescaling of the weight vector for which the calibration error cancels.
Proposition 6.2
.
The re-scaled weight vector
w
s
←
s
​
w
w_{s}\leftarrow sw
with
s
=
⟨
w
,
w
∗
⟩
Σ
/
‖
w
‖
Σ
2
s=\langle w,w^{*}\rangle_{\Sigma}/\|w\|_{\Sigma}^{2}
yields null calibration error
𝒦
⁡
(
w
s
)
=
0
\mathcal{K}(w_{s})=0
while preserving the refinement error
ℛ
⁡
(
w
s
)
=
ℛ
⁡
(
w
)
\mathcal{R}(w_{s})=\mathcal{R}(w)
.
Note that such rescaling of the weight vector exactly corresponds to temperature scaling. For classifiers such as logistic regression or neural nets that use a sigmoid to produce probabilities,
Proposition
6.2
establishes that, under the assumption that the logit distribution is a mixture of Gaussians, TS sets calibration error to zero while preserving refinement. An immediate corollary of this and
Theorem
3.4
is that refinement error equals risk after temperature scaling:
ℛ
⁡
(
w
)
=
min
s
∈
ℝ
⁡
Risk
⁡
(
s
​
w
)
\mathcal{R}(w)=\min_{s\in\mathbb{R}}\Risk(sw)
.
Remark 6.3
.
For non-centered or imbalanced data, adding an intercept parameter to TS is necessary to achieve the same result. A similar analysis can be derived for the multi-class case, leading to post-hoc calibration with matrix scaling.
This supports the idea that we should minimize refinement during training. Rescaling the weight vector to the correct confidence level is enough to remove the calibration error after training. From our analysis, it seems clear that calibration and refinement error minimizers do not have to match. The confidence level
‖
w
‖
Σ
\|w\|_{\Sigma}
is not constrained to equal the expertise
a
w
a_{w}
in any way. We observed empirically that loss and refinement minimizers can be separated. Can we push the analysis further to exhibit this theoretically?
7
High dimensional asymptotics of logistic regression
In this section, we place ourselves in the setting of regularized logistic regression to study the impact of calibration and refinement on the risk during training. Proofs and missing technical details are provided in
Appendix
C
.
Figure 7:
Cross-entropy, calibration and refinement errors when
λ
\lambda
varies. The spectral distribution
F
F
is uniform (
α
=
β
=
1
\alpha=\beta=1
),
e
∗
=
10
%
e^{*}=10\%
, and
r
=
1
2
r=\frac{1}{2}
. We fit a logistic regression on 2000 random samples from our data model to obtain
w
^
λ
\hat{w}_{\lambda}
. We compute the resulting calibration and refinement errors using
Proposition
6.1
and plot
95
%
95\%
error bars after 50 seeds. Theory closely matches empirical observations.
Consider
n
n
pairs
(
x
i
,
y
i
)
1
≤
i
≤
n
(x_{i},y_{i})_{1\leq i\leq n}
from the bimodal data model of
Section
6
and let
w
λ
w_{\lambda}
denote the weight vector learned by solving regularized logistic regression
min
w
∈
ℝ
p
⁡
1
n
​
∑
i
=
1
n
log
⁡
(
1
+
exp
⁡
(
−
y
i
​
w
⊤
​
X
i
)
)
+
λ
2
​
‖
w
‖
2
,
\min_{w\in\mathbb{R}^{p}}\frac{1}{n}\sum_{i=1}^{n}\log(1+\exp(-y_{i}w^{\top}X_{i}))+\frac{\lambda}{2}\|w\|^{2}\;,
for a given regularization strength
λ
∈
ℝ
+
\lambda\in\mathbb{R}_{+}
.
We will exploit known results on
w
λ
w_{\lambda}
in the high-dimensional asymptotic setting where
n
,
p
→
∞
n,p\rightarrow\infty
with a constant ratio
p
/
n
→
r
>
0
p/n\rightarrow r>0
. We assume that the class means on each dimension
(
μ
i
)
1
≤
i
≤
p
(\mu_{i})_{1\leq i\leq p}
are sampled i.i.d. from a distribution satisfying
𝔼
⁡
[
μ
i
2
]
=
c
2
p
\mathbb{E}[\mu_{i}^{2}]=\frac{c^{2}}{p}
, such that
‖
μ
‖
2
→
p
→
∞
c
\|\mu\|_{2}\xrightarrow{p\rightarrow\infty}c
for some constant
c
>
0
c>0
that controls the class separability of the problem. To simplify the formulas, we assume that
Σ
\Sigma
is diagonal. We further assume its eigenvalues
(
σ
i
)
1
≤
i
≤
p
(\sigma_{i})_{1\leq i\leq p}
are sampled i.i.d. from a positive, bounded spectral distribution
F
F
.
Mai et al. (2019)
provide the following characterization of
w
λ
w_{\lambda}
w
λ
∼
𝒩
⁡
(
η
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
​
μ
,
γ
n
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
​
Σ
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
)
,
w_{\lambda}\sim\mathcal{N}\Big(\eta(\lambda I_{p}+\tau\Sigma)^{-1}\mu,\frac{\gamma}{n}(\lambda I_{p}+\tau\Sigma)^{-1}\Sigma(\lambda I_{p}+\tau\Sigma)^{-1}\Big),
where
τ
,
η
,
γ
\tau,\eta,\gamma
are the unique solutions to a non-linear system of equations, parametrized by
r
,
c
,
λ
r,c,\lambda
and
F
F
.
To compute calibration and refinement errors that appear in
Proposition
6.1
, we are interested in
⟨
w
λ
,
w
∗
⟩
Σ
\langle w_{\lambda},w^{*}\rangle_{\Sigma}
and
‖
w
λ
‖
Σ
\|w_{\lambda}\|_{\Sigma}
.
Proposition 7.1
.
For
n
,
p
→
∞
n,p\to\infty
,
⟨
w
λ
,
w
∗
⟩
Σ
→
𝑃
𝔼
σ
∼
F
​
[
2
​
η
​
c
2
λ
+
τ
​
σ
]
,
\langle w_{\lambda},w^{*}\rangle_{\Sigma}\xrightarrow{P}\mathbb{E}_{\sigma\sim F}\Big[\frac{2\eta c^{2}}{\lambda+\tau\sigma}\Big]\,,
‖
w
λ
‖
Σ
2
→
𝑃
𝔼
σ
∼
F
​
[
γ
​
r
​
σ
2
+
η
2
​
c
2
​
σ
(
λ
+
τ
​
σ
)
2
]
,
\|w_{\lambda}\|_{\Sigma}^{2}\xrightarrow{P}\mathbb{E}_{\sigma\sim F}\Big[\frac{\gamma r\sigma^{2}+\eta^{2}c^{2}\sigma}{(\lambda+\tau\sigma)^{2}}\Big]\,,
where the convergence is in probability.
Remark 7.2
.
Results from
Dobriban and Wager (2018)
allow us to derive similar results for regularized LDA and Ridge, leading to simpler formulations of refinement and calibration errors. We omit these results due to space constraints.
The data separability parameter
c
c
is hard to interpret; instead, we work with
e
∗
e^{*}
, the error rate of the optimal classifier
w
∗
w^{*}
.
Proposition 7.3
.
As
n
,
p
→
∞
n,p\rightarrow\infty
,
e
∗
→
a
.
s
.
Φ
⁡
(
−
c
​
𝔼
σ
∼
F
​
[
σ
−
1
]
)
.
e^{*}\xrightarrow{a.s.}\Phi\big(-c\sqrt{\mathbb{E}_{\sigma\sim F}[\sigma^{-1}]}\big)\,.
e
∗
e^{*}
provides a common and interpretable scale for the problem difficulty, whatever the shape of the spectral distribution. Given a spectral distribution
F
F
,
Proposition
7.3
gives a simple relation between
e
∗
e^{*}
and
c
c
. We can choose any bounded and positive distribution
F
F
in our formulas to compute
⟨
w
λ
,
w
∗
⟩
Σ
\langle w_{\lambda},w^{*}\rangle_{\Sigma}
and
‖
w
λ
‖
Σ
2
\|w_{\lambda}\|_{\Sigma}^{2}
. We pick
σ
=
ε
+
B
⁡
(
α
,
β
)
\sigma=\varepsilon+B(\alpha,\beta)
where
B
B
denotes a Beta distribution with shape parameters
(
α
,
β
)
(\alpha,\beta)
and
ε
\varepsilon
is a small shift parameter to make
F
F
strictly positive (we fix
ε
=
10
−
3
\varepsilon=10^{-3}
). This allows us to explore a variety of spectral distribution shapes with a single mathematical model, by tweaking
α
\alpha
and
β
\beta
. Using propositions
7.1
and
7.3
, we obtain formulas for
⟨
w
λ
,
w
∗
⟩
Σ
,
‖
w
λ
‖
Σ
2
\langle w_{\lambda},w^{*}\rangle_{\Sigma},\|w_{\lambda}\|_{\Sigma}^{2}
and
e
∗
e^{*}
, see
Appendix
C
.
For a given regularization strength
λ
\lambda
, dimensions-to-samples ratio
r
r
, optimal error rate
e
∗
e^{*}
and spectral distribution
F
F
(controlled by
α
,
β
\alpha,\beta
), we can compute
η
,
τ
,
γ
\eta,\tau,\gamma
by solving the system provided by
Mai et al. (2019)
. Using
Proposition
7.1
and
Proposition
6.1
we obtain the calibration and refinement errors. We provide a fast implementation of this method at
github.com/eugeneberta/RefineThenCalibrate-Theory
. For a fixed set of parameters
F
,
r
,
e
∗
F,r,e^{*}
, we can plot a learning curve for logistic regression by varying the amount of regularization
λ
\lambda
. We observe the contributions of calibration and refinement errors to the total logloss of the model, as in
Figure
7
.
In this example, calibration and refinement errors are not minimized jointly, resulting in a loss minimizer somewhere between the two that is suboptimal for both errors. Given that we can easily set the calibration error to zero (
Proposition
6.2
), our mathematical model predicts that refinement-based early stopping yields a
2
%
2\%
decrease in downstream cross-entropy on this example.
We can explore the impact of problem parameters on this phenomenon. We investigate three spectral distribution shapes (first row). For each of these,
Figure
8
displays the gap between the calibration error minimizer and the refinement error minimizer (second row) and the relative cross-entropy gains (
%
\%
) obtained when stopping on refinement instead of loss (third row) as a function of the ratio
r
=
p
/
n
r=p/n
(x-axis) and problem difficulty
e
∗
e^{*}
(y-axis).
Figure 8:
Influence of problem parameters on calibration and refinement minimizers.
First row: spectral distribution shape. Second row: log gap between the two minimizers. In green regions, calibration is minimized earlier, while in red regions it is refinement. Third row: relative logloss gain (
%
\%
) obtained with refinement-based early stopping.
To interpret the spectral distribution shapes, note that a small eigenvalue translates to a small “within class variance” and thus more separable data on the corresponding axis. Smaller eigenvalues correspond to more informative features. The left column depicts a scenario where most features are equally informative. The central column has a wide spread of good and bad features. In the right column, most features are bad while there are a few “hidden” good components. In the first scenario, calibration converges earlier almost everywhere on the parameter space, this corresponds to the regime we observe in computer vision. When informative features are scarce on the other hand, refinement is minimized earlier (right column), which may be an appropriate expectation for sparse problems in genomics or histopathology. When the spectral distribution is more balanced, the scenarios are co-existing, depending on problem parameters. Refinement-based early stopping always yields smaller loss, and in the regions where the two minimizers are far apart (whichever error is minimized first), the gains are significant with up to
25
%
25\%
loss decrease.
Remark 7.4
.
Bartlett et al. (2020)
establish that benign overfitting occurs for linear regression in a similar data model under some condition on the spectral distribution of the covariance matrix. An avenue for future work is to study how this translates to classification and how it links with the calibration-refinement decomposition.
8
Conclusion
We have demonstrated that selecting the best epoch and hyperparameters based on refinement error solves an issue that arises when using the validation loss. We established that refinement error can be estimated by the loss after post-hoc calibration. This allowed us to use TS-refinement for early stopping, yielding improvement in test loss on various machine learning problems. Our estimator is available in the probmetrics package
github.com/dholzmueller/probmetrics
and can be used seamlessly with any architecture.
One limitation is that TS-refinement can be more sensitive to overfitting on small validation sets. In this case, cross-validation, ensembling, and regularized post-hoc calibrators could be useful. Moreover, we did not explore the utility of TS-refinement when training with cross-validation instead of holdout validation. Another little-explored area is the influence of training parameters—such as optimizers, schedulers, and regularization—on the calibration and refinement errors during training.
While refinement-based stopping is relevant in data-constrained settings prone to overfitting, it could also prove useful for the fine-tuning of foundation models, where training long past the loss minimum can be beneficial
(
Ouyang et al., 2022
;
Carlsson et al., 2024
)
. Additionally, while we explore its utility for model optimization, our refinement estimator could be a valuable diagnostic metric, especially in imbalanced multi-class settings where accuracy and area under the ROC curve are less appropriate.
Acknowledgements
The authors would like to thank Sacha Braun, Etienne Gauthier, Sebastian Gruber, Alexandre Perez-Lebel, Gaël Varoquaux, and Lennart Purucker for fruitful discussions regarding this work.
This publication is part of the Chair “Markets and Learning”, supported by Air Liquide, BNP PARIBAS ASSET MANAGEMENT Europe, EDF, Orange and SNCF, sponsors of the Inria Foundation.
This work received support from the French government, managed by the National Research Agency, under the France 2030 program with the reference “PR[AI]RIE-PSAI” (ANR-23-IACL-0008).
Funded by the European Union (ERC-2022-SYG-OCEAN-101071601). Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council Executive Agency. Neither the European Union nor the granting authority can be held responsible for them.
References
Guo et al. [2017]
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger.
On calibration of modern neural networks.
In
International Conference on Machine Learning
, 2017.
Bröcker [2009]
Jochen Bröcker.
Reliability, sufficiency, and the decomposition of proper scores.
Quarterly Journal of the Royal Meteorological Society
, 135(643):1512–1519, 2009.
Ranjan et al. [2024]
Rishabh Ranjan, Saurabh Garg, Mrigank Raman, Carlos Guestrin, and Zachary Lipton.
Post-hoc reversal: Are we selecting models prematurely?
arXiv preprint arXiv:2404.07815
, 2024.
Gneiting and Raftery [2007]
Tilmann Gneiting and Adrian E. Raftery.
Strictly proper scoring rules, prediction, and estimation.
Journal of the American statistical Association
, 102(477):359–378, 2007.
Grünwald and Dawid [2004]
Peter D. Grünwald and A. Philip Dawid.
Game theory, maximum entropy, minimum discrepancy and robust bayesian decision theory.
The Annals of Statistics
, 32(4):1367–1433, 2004.
Brehmer and Gneiting [2020]
Jonas R. Brehmer and Tilmann Gneiting.
Properization: constructing proper scoring rules via Bayes acts.
Annals of the Institute of Statistical Mathematics
, 72:659–673, 2020.
Brier [1950]
Glenn W. Brier.
Verification of forecasts expressed in terms of probability.
Monthly Weather Review
, 78(1):1–3, 1950.
Sanders [1963]
Frederick Sanders.
On subjective probability forecasting.
Journal of Applied Meteorology and Climatology
, 2(2):191–201, 1963.
Murphy [1973]
Allan H. Murphy.
A new vector partition of the probability score.
Journal of Applied Meteorology and Climatology
, 12(4):595–600, 1973.
Kull and Flach [2015]
Meelis Kull and Peter Flach.
Novel decompositions of proper scoring rules for classification: Score adjustment as precursor to calibration.
In
European Conference on Machine Learning and Knowledge Discovery in Databases
, 2015.
Pohle [2020]
Marc-Oliver Pohle.
The Murphy decomposition and the calibration-resolution principle: A new perspective on forecast evaluation.
arXiv:2005.01835
, 2020.
Minderer et al. [2021]
Matthias Minderer, Josip Djolonga, Rob Romijnders, Frances Hubis, Xiaohua Zhai, Neil Houlsby, Dustin Tran, and Mario Lucic.
Revisiting the calibration of modern neural networks.
Advances in Neural Information Processing Systems
, 2021.
Tao et al. [2024]
Linwei Tao, Younan Zhu, Haolan Guo, Minjing Dong, and Chang Xu.
A benchmark study on calibration.
In
International Conference on Learning Representations
, 2024.
Platt [1999]
John C. Platt.
Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods.
Advances in Large Margin Classifiers
, 10(3):61–74, 1999.
Kull et al. [2017]
Meelis Kull, Telmo Silva Filho, and Peter Flach.
Beta calibration: a well-founded and easily implemented improvement on logistic calibration for binary classifiers.
In
International Conference on Artificial Intelligence and Statistics
, 2017.
Kull et al. [2019]
Meelis Kull, Miquel Perello Nieto, Markus Kängsepp, Telmo Silva Filho, Hao Song, and Peter Flach.
Beyond temperature scaling: Obtaining well-calibrated multi-class probabilities with dirichlet calibration.
In
Advances in Neural Information Processing Systems
, 2019.
Robertson et al. [1988]
T. Robertson, F.T. Wright, and R. Dykstra.
Order Restricted Statistical Inference
.
Probability and Statistics Series. Wiley, 1988.
ISBN 978-0-471-91787-8.
Zadrozny and Elkan [2002]
Bianca Zadrozny and Charles Elkan.
Transforming classifier scores into accurate multiclass probability estimates.
In
Proceedings of the International Conference on Knowledge Discovery and Data Mining
, 2002.
Oron and Flournoy [2017]
Assaf P. Oron and Nancy Flournoy.
Centered isotonic regression: point and interval estimation for dose–response studies.
Statistics in Biopharmaceutical Research
, 9(3):258–267, 2017.
Vovk et al. [2015]
Vladimir Vovk, Ivan Petej, and Valentina Fedorova.
Large-scale probabilistic predictors with and without guarantees of validity.
Advances in Neural Information Processing Systems
, 2015.
Manokhin [2017]
Valery Manokhin.
Multi-class probabilistic classification using inductive and cross venn–abers predictors.
In
Conformal and Probabilistic Prediction and Applications
, 2017.
Berta et al. [2024]
Eugene Berta, Francis Bach, and Michael Jordan.
Classifier calibration with roc-regularized isotonic regression.
In
International Conference on Artificial Intelligence and Statistics
, 2024.
Naeini et al. [2015]
Mahdi Pakdaman Naeini, Gregory Cooper, and Milos Hauskrecht.
Obtaining well calibrated probabilities using bayesian binning.
In
Proceedings of the AAAI Conference on Artificial Intelligence
, 2015.
Wang et al. [2021]
Deng-Bao Wang, Lei Feng, and Min-Ling Zhang.
Rethinking calibration of deep neural networks: Do not be afraid of overconfidence.
In
Advances in Neural Information Processing Systems
, 2021.
Gruber and Buettner [2022]
Sebastian Gruber and Florian Buettner.
Better uncertainty calibration via proper scores for classification and beyond.
Advances in Neural Information Processing Systems
, 2022.
Gruber and Bach [2025]
Sebastian Gregor Gruber and Francis Bach.
Optimizing Estimators of Squared Calibration Errors in Classification.
Transactions on Machine Learning Research
, 2025.
Dimitriadis et al. [2021]
Timo Dimitriadis, Tilmann Gneiting, and Alexander I. Jordan.
Stable reliability diagrams for probabilistic classifiers.
Proceedings of the National Academy of Sciences
, 118(8), 2021.
Ferrer and Ramos [2024]
Luciana Ferrer and Daniel Ramos.
Evaluating posterior probabilities: Decision theory, proper scoring rules, and calibration.
arXiv:2408.02841
, 2024.
Perez-Lebel et al. [2023]
Alexandre Perez-Lebel, Marine Le Morvan, and Gael Varoquaux.
Beyond calibration: estimating the grouping loss of modern neural networks.
In
International Conference on Learning Representations
, 2023.
Chidambaram and Ge [2024]
Muthu Chidambaram and Rong Ge.
Reassessing how to compare and improve the calibration of machine learning models.
arXiv:2406.04068
, 2024.
Dobriban and Wager [2018]
Edgar Dobriban and Stefan Wager.
High-dimensional asymptotics of prediction: Ridge regression and classification.
The Annals of Statistics
, 46(1):247–279, 2018.
Mai et al. [2019]
Xiaoyi Mai, Zhenyu Liao, and Romain Couillet.
A large scale analysis of logistic regression: Asymptotic performance and new insights.
In
International Conference on Acoustics, Speech and Signal Processing
, 2019.
Couillet et al. [2018]
Romain Couillet, Zhenyu Liao, and Xiaoyi Mai.
Classification asymptotics in the random matrix regime.
In
European Signal Processing Conference
, 2018.
Salehi et al. [2019]
Fariborz Salehi, Ehsan Abbasi, and Babak Hassibi.
The impact of regularization on high-dimensional logistic regression.
Advances in Neural Information Processing Systems
, 2019.
Bach [2024]
Francis Bach.
High-dimensional analysis of double descent for linear regression with random projections.
SIAM Journal on Mathematics of Data Science
, 6(1):26–50, 2024.
Shannon [1948]
Claude E. Shannon.
A mathematical theory of communication.
The Bell System Technical Journal
, 27(3):379–423, 1948.
Kumar et al. [2019]
Ananya Kumar, Percy S. Liang, and Tengyu Ma.
Verified uncertainty calibration.
In
Advances in Neural Information Processing Systems
, 2019.
Vaicenavicius et al. [2019]
Juozas Vaicenavicius, David Widmann, Carl Andersson, Fredrik Lindsten, Jacob Roll, and Thomas Schön.
Evaluating model calibration in classification.
In
International Conference on Artificial Intelligence and Statistics
, 2019.
Roelofs et al. [2022]
Rebecca Roelofs, Nicholas Cain, Jonathon Shlens, and Michael C. Mozer.
Mitigating bias in calibration error estimation.
In
International Conference on Artificial Intelligence and Statistics
, 2022.
Silva Filho et al. [2023]
Telmo Silva Filho, Hao Song, Miquel Perello-Nieto, Raul Santos-Rodriguez, Meelis Kull, and Peter Flach.
Classifier calibration: a survey on how to assess and improve predicted class probabilities.
Machine Learning
, 112(9):3211–3260, 2023.
Carrell et al. [2022]
A Michael Carrell, Neil Mallinar, James Lucas, and Preetum Nakkiran.
The calibration generalization gap.
arXiv:2210.01964
, 2022.
Liu and Nocedal [1989]
Dong C. Liu and Jorge Nocedal.
On the limited memory bfgs method for large scale optimization.
Mathematical programming
, 45(1):503–528, 1989.
Ranjan [2023]
Rishabh Ranjan.
torchcal: post-hoc calibration on GPU, 2023.
URL
github.com/rishabh-ranjan/torchcal
.
Feinman [2021]
Reuben Feinman.
Pytorch-minimize: a library for numerical optimization with autograd, 2021.
URL
github.com/rfeinman/pytorch-minimize
.
Erickson et al. [2020]
Nick Erickson, Jonas Mueller, Alexander Shirkov, Hang Zhang, Pedro Larroy, Mu Li, and Alexander Smola.
Autogluon-tabular: Robust and accurate automl for structured data.
arXiv:2003.06505
, 2020.
He et al. [2016]
Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
Deep residual learning for image recognition.
In
Proceedings of the Conference on Computer Vision and Pattern Recognition
, 2016.
Zagoruyko [2016]
Sergey Zagoruyko.
Wide residual networks.
arXiv:1605.07146
, 2016.
Krizhevsky and Hinton [2009]
Alex Krizhevsky and Geoffrey Hinton.
Learning multiple layers of features from tiny images.
2009.
Netzer et al. [2011]
Yuval Netzer, Tao Wang, Adam Coates, Alessandro Bissacco, Baolin Wu, and Andrew Y Ng.
Reading digits in natural images with unsupervised feature learning.
In
NIPS workshop on deep learning and unsupervised feature learning
, 2011.
DeVries [2017]
Terrance DeVries.
Improved regularization of convolutional neural networks with cutout.
arXiv:1708.04552
, 2017.
Ye et al. [2024]
Han-Jia Ye, Si-Yang Liu, Hao-Run Cai, Qi-Le Zhou, and De-Chuan Zhan.
A closer look at deep learning methods on tabular datasets.
arXiv:2407.00956
, 2024.
Chen and Guestrin [2016]
Tianqi Chen and Carlos Guestrin.
XGBoost: A scalable tree boosting system.
In
Proceedings of the International Conference on Knowledge Discovery and Data Mining
, 2016.
Grinsztajn et al. [2022]
Léo Grinsztajn, Edouard Oyallon, and Gaël Varoquaux.
Why do tree-based models still outperform deep learning on typical tabular data?
Advances in Neural Information Processing Systems
, 2022.
Gorishniy et al. [2021]
Yury Gorishniy, Ivan Rubachev, Valentin Khrulkov, and Artem Babenko.
Revisiting deep learning models for tabular data.
Advances in Neural Information Processing Systems
, 2021.
Holzmüller et al. [2024]
David Holzmüller, Léo Grinsztajn, and Ingo Steinwart.
Better by default: Strong pre-tuned mlps and boosted trees on tabular data.
Advances in Neural Information Processing Systems
, 2024.
Erickson et al. [2025]
Nick Erickson, Lennart Purucker, Andrej Tschalzev, David Holzmüller, Prateek Mutalik Desai, David Salinas, and Frank Hutter.
Tabarena: A living benchmark for machine learning on tabular data, 2025.
Jordan [1995]
Michael I Jordan.
Why the logistic function? a tutorial discussion on probabilities and neural networks.
Computational Cognitive Science Technical Report 9503
, 1995.
Fisher [1936]
Ronald A Fisher.
The use of multiple measurements in taxonomic problems.
Annals of Eugenics
, 7(2):179–188, 1936.
Bartlett et al. [2020]
Peter L. Bartlett, Philip M. Long, Gábor Lugosi, and Alexander Tsigler.
Benign overfitting in linear regression.
Proceedings of the National Academy of Sciences
, 117(48), 2020.
Ouyang et al. [2022]
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F Christiano, Jan Leike, and Ryan Lowe.
Training language models to follow instructions with human feedback.
In
Advances in Neural Information Processing Systems
, 2022.
Carlsson et al. [2024]
Fredrik Carlsson, Fangyu Liu, Daniel Ward, Murathan Kurfali, and Joakim Nivre.
The hyperfitting phenomenon: Sharpening and stabilizing llms for open-ended text generation.
arXiv:2412.04318
, 2024.
Blasiok et al. [2024]
Jaroslaw Blasiok, Parikshit Gopalan, Lunjia Hu, and Preetum Nakkiran.
When does optimizing a proper loss yield calibration?
Advances in Neural Information Processing Systems
, 2024.
Kechris [1995]
Alexander S. Kechris.
Classical Descriptive Set Theory
, volume 156 of
Graduate Texts in Mathematics
.
Springer, 1995.
Boyd and Vandenberghe [2004]
Stephen Boyd and Lieven Vandenberghe.
Convex Optimization.
Cambridge University Press
, 2004.
Orseau and Hutter [2023]
Laurent Orseau and Marcus Hutter.
Line search for convex minimization.
arXiv:2307.16560
, 2023.
Pedregosa et al. [2011]
Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron Weiss, Vincent Dubourg, Jake Vanderplas, Alexandre Passos, David Cournapeau, Matthieu Brucher, Matthieu Perrot, and Édouard Duchesnay.
Scikit-learn: Machine Learning in Python.
Journal of Machine Learning Research
, 12(85):2825–2830, 2011.
Błasiok and Nakkiran [2024]
Jarosław Błasiok and Preetum Nakkiran.
Smooth ECE: Principled reliability diagrams via kernel smoothing.
In
International Conference on Learning Representations
, 2024.
McElfresh et al. [2024]
Duncan McElfresh, Sujay Khandagale, Jonathan Valverde, Vishak Prasad C, Ganesh Ramakrishnan, Micah Goldblum, and Colin White.
When do neural nets outperform boosted trees on tabular data?
Advances in Neural Information Processing Systems
, 2024.
Appendix A
Calibration, Refinement, and Sharpness
In this section we first prove our main theoretical result, the variational reformulation of proper loss decompositions.
We then discuss an alternative decomposition and present additional results.
See
3.4
Proof.
Let
g
C
​
(
q
)
≔
𝔼
⁡
[
Y
|
f
⁡
(
X
)
=
q
]
g_{C}(q)\coloneqq\mathbb{E}[Y|f(X)=q]
, such that
C
=
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
=
g
C
​
(
f
⁡
(
X
)
)
C=\mathbb{E}[Y|f(X)]=g_{C}(f(X))
almost surely. Then,
ℛ
ℓ
​
(
f
)
\displaystyle\mathcal{R}_{\ell}(f)
=
\displaystyle=
𝔼
⁡
[
e
ℓ
​
(
C
)
]
=
𝔼
⁡
[
ℓ
⁡
(
C
,
C
)
]
=
𝔼
⁡
[
ℓ
⁡
(
g
C
​
(
f
⁡
(
X
)
)
,
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
)
]
\displaystyle\mathbb{E}[e_{\ell}(C)]=\mathbb{E}[\ell(C,C)]=\mathbb{E}[\ell(g_{C}(f(X)),\mathbb{E}[Y|f(X)])]
(by definition)
=
\displaystyle=
𝔼
⁡
[
ℓ
⁡
(
g
C
​
(
f
⁡
(
X
)
)
,
Y
)
]
\displaystyle\mathbb{E}[\ell(g_{C}(f(X)),Y)]
(by
Lemma
A.5
)
=
\displaystyle=
min
g
⁡
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
f
⁡
(
X
)
)
,
Y
)
]
.
\displaystyle\min_{g}\mathbb{E}[\ell(g(f(X)),Y)]~.
(by
Lemma
A.6
with
Z
=
f
⁡
(
X
)
Z=f(X)
)
This shows the representation of the refinement error, and
Lemma
A.6
also shows that
g
∗
g^{*}
is a minimizer, which is almost surely unique. The representation of the calibration error follows directly from the calibration-refinement decomposition
Risk
⁡
(
f
)
=
ℛ
ℓ
​
(
f
)
+
𝒦
ℓ
​
(
f
)
\Risk(f)=\mathcal{R}_{\ell}(f)+\mathcal{K}_{\ell}(f)
[
Bröcker, 2009
]
.
Now, let
Z
∈
Δ
k
Z\in\Delta_{k}
be the uniform distribution (to be interpreted as a constant random variable). Then, for
p
¯
≔
𝔼
⁡
[
Y
]
\bar{p}\coloneqq\mathbb{E}[Y]
e
ℓ
​
(
𝔼
​
[
Y
]
)
\displaystyle e_{\ell}(\mathbb{E}[Y])
=
\displaystyle=
ℓ
⁡
(
𝔼
⁡
[
Y
]
,
𝔼
⁡
[
Y
]
)
=
ℓ
⁡
(
p
¯
,
𝔼
⁡
[
Y
]
)
\displaystyle\ell(\mathbb{E}[Y],\mathbb{E}[Y])=\ell(\bar{p},\mathbb{E}[Y])
=
\displaystyle=
𝔼
⁡
[
ℓ
⁡
(
p
¯
,
Y
)
]
\displaystyle\mathbb{E}[\ell(\bar{p},Y)]
(
ℓ
\ell
is affine in the second argument)
=
\displaystyle=
min
g
⁡
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
Y
)
]
\displaystyle\min_{g}\mathbb{E}[\ell(g(Z),Y)]
(by
Lemma
A.6
)
=
\displaystyle=
min
c
​
constant
⁡
𝔼
⁡
[
ℓ
⁡
(
c
⁡
(
f
⁡
(
X
)
)
,
Y
)
]
.
\displaystyle\min_{c\text{ constant}}\mathbb{E}[\ell(c(f(X)),Y)]~.
Again,
Lemma
A.6
shows that the minimizer is
c
∗
​
(
q
)
=
𝔼
⁡
[
Y
|
Z
]
=
𝔼
⁡
[
Y
]
c^{*}(q)=\mathbb{E}[Y|Z]=\mathbb{E}[Y]
.
For the sharpness, we have
𝒮
ℓ
​
(
f
)
\displaystyle\mathcal{S}_{\ell}(f)
=
\displaystyle=
𝔼
⁡
[
d
ℓ
​
(
𝔼
⁡
[
Y
]
,
C
)
]
=
𝔼
⁡
[
ℓ
⁡
(
𝔼
⁡
[
Y
]
,
C
)
]
−
𝔼
⁡
[
ℓ
⁡
(
C
,
C
)
]
=
𝔼
⁡
[
ℓ
⁡
(
𝔼
⁡
[
Y
]
,
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
)
]
−
ℛ
ℓ
​
(
f
)
\displaystyle\mathbb{E}[d_{\ell}(\mathbb{E}[Y],C)]=\mathbb{E}[\ell(\mathbb{E}[Y],C)]-\mathbb{E}[\ell(C,C)]=\mathbb{E}[\ell(\mathbb{E}[Y],\mathbb{E}[Y|f(X)])]-\mathcal{R}_{\ell}(f)
by definition. We already showed above that
ℛ
ℓ
​
(
f
)
=
min
g
⁡
Risk
⁡
(
g
∘
f
)
\mathcal{R}_{\ell}(f)=\min_{g}\Risk(g\circ f)
. For the other term, we exploit that
ℓ
\ell
is affine in its second argument to obtain
𝔼
⁡
[
ℓ
⁡
(
𝔼
⁡
[
Y
]
,
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
)
]
\displaystyle\mathbb{E}[\ell(\mathbb{E}[Y],\mathbb{E}[Y|f(X)])]
=
\displaystyle=
ℓ
⁡
(
𝔼
⁡
[
Y
]
,
𝔼
⁡
[
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
]
)
=
e
ℓ
​
(
𝔼
⁡
[
Y
]
)
.
\displaystyle\ell(\mathbb{E}[Y],\mathbb{E}[\mathbb{E}[Y|f(X)]])=e_{\ell}(\mathbb{E}[Y])~.
∎
Remark A.1
(Alternative decompositions by
Kull and Flach [2015]
)
.
Kull and Flach [2015]
provide a slightly different calibration-refinement decomposition:
𝔼
⁡
[
d
ℓ
​
(
f
⁡
(
X
)
,
Y
)
]
=
𝔼
⁡
[
d
ℓ
​
(
f
⁡
(
X
)
,
C
)
]
⏟
𝒦
ℓ
​
(
f
)
+
𝔼
​
[
d
ℓ
​
(
C
,
Y
)
]
⏟
≕
ℛ
~
ℓ
​
(
f
)
.
\mathbb{E}[d_{\ell}(f(X),Y)]=\underbrace{\mathbb{E}[d_{\ell}(f(X),C)]}_{\mathcal{K}_{\ell}(f)}+\underbrace{\mathbb{E}[d_{\ell}(C,Y)]}_{\eqqcolon\tilde{\mathcal{R}}_{\ell}(f)}~.
The alternative refinement error
ℛ
~
ℓ
​
(
f
)
=
𝔼
⁡
[
d
ℓ
​
(
C
,
Y
)
]
\displaystyle\tilde{\mathcal{R}}_{\ell}(f)=\mathbb{E}[d_{\ell}(C,Y)]
=
\displaystyle=
𝔼
⁡
[
ℓ
⁡
(
C
,
Y
)
]
−
𝔼
⁡
[
ℓ
⁡
(
Y
,
Y
)
]
=
ℛ
ℓ
​
(
f
)
−
𝔼
⁡
[
ℓ
⁡
(
Y
,
Y
)
]
\displaystyle\mathbb{E}[\ell(C,Y)]-\mathbb{E}[\ell(Y,Y)]=\mathcal{R}_{\ell}(f)-\mathbb{E}[\ell(Y,Y)]
equals
ℛ
ℓ
​
(
f
)
\mathcal{R}_{\ell}(f)
if
𝔼
⁡
[
ℓ
⁡
(
Y
,
Y
)
]
=
0
\mathbb{E}[\ell(Y,Y)]=0
, which is the case for logloss and Brier loss. In this case, the irreducible and grouping loss in
Figure
2
also equal the definitions of
Kull and Flach [2015]
in their decomposition
𝔼
⁡
[
d
ℓ
​
(
C
,
Y
)
]
=
𝔼
⁡
[
d
ℓ
​
(
C
,
𝔼
⁡
[
Y
|
X
]
)
]
⏟
grouping loss
+
𝔼
⁡
[
d
ℓ
​
(
𝔼
⁡
[
Y
|
X
]
,
Y
)
]
⏟
irreducible loss
.
\mathbb{E}[d_{\ell}(C,Y)]=\underbrace{\mathbb{E}[d_{\ell}(C,\mathbb{E}[Y|X])]}_{\text{grouping loss}}+\underbrace{\mathbb{E}[d_{\ell}(\mathbb{E}[Y|X],Y)]}_{\text{irreducible loss}}~.
Intuitively, the grouping loss describes the loss that occurs when
f
⁡
(
x
1
)
=
f
⁡
(
x
2
)
f(x_{1})=f(x_{2})
but
𝔼
⁡
[
Y
|
X
=
x
1
]
≠
𝔼
⁡
[
Y
|
X
=
x
2
]
\mathbb{E}[Y|X=x_{1}]\neq\mathbb{E}[Y|X=x_{2}]
.
The reducible loss in
Figure
2
is called
epistemic loss
in
Kull and Flach [2015]
.
Remark A.2
(Extending the definitions of calibration, refinement, and sharpness)
.
Theorem
3.4
shows that for proper losses, calibration error is not only a divergence relative to a desired target (
C
C
), but also a potential reduction in loss through post-processing.
The latter perspective has been suggested by
Ferrer and Ramos [2024]
without showing equivalence to the former perspective.
On the one hand, an advantage of the former perspective is that it extends to non-divergences like the
L
1
L^{1}
distance. On the other hand, an advantage of the latter perspective is that it can be used to extend the notion of calibration error, refinement error, and sharpness to non-proper losses (changing the desired target) or even non-probabilistic settings such as regression with MSE loss. Moreover, refinement error and sharpness can even be defined when
f
⁡
(
X
)
f(X)
is not in the right space for the loss function, for example because it is a hidden-layer representation in a neural network. The variational formulation also allows to define more related quantities by using various function classes
𝒢
\mathcal{G}
and considering
inf
g
∈
𝒢
Risk
⁡
(
g
∘
f
)
.
\displaystyle\inf_{g\in\mathcal{G}}\Risk(g\circ f)~.
For example, considering the corresponding variant of calibration error for 1-Lipschitz functions, we obtain the post-processing gap from
Blasiok et al. [2024]
. In the binary case, using increasing functions, we obtain the best possible risk attainable by isotonic regression.
Theorem
3.4
also implies some further properties of calibration, refinement, and sharpness:
Corollary A.3
.
Let
k
≥
2
k\geq 2
, let
ℓ
:
Δ
k
×
𝒴
k
→
ℝ
∪
{
∞
}
\ell:\Delta_{k}\times\mathcal{Y}_{k}\to\mathbb{R}\cup\{\infty\}
be a proper loss, and let
f
:
𝒳
→
Δ
k
f:\mathcal{X}\to\Delta_{k}
be measurable, where
Δ
k
\Delta_{k}
is equipped with the Borel
σ
\sigma
-algebra.
1.
If
f
f
is calibrated, then its population risk cannot be reduced by post-pocessing, i.e.,
Risk
⁡
(
f
)
=
inf
g
Risk
⁡
(
g
∘
f
)
\Risk(f)=\inf_{g}\Risk(g\circ f)
. The converse holds if
ℓ
\ell
is strictly proper
[
Blasiok et al., 2024
]
.
2.
Let
g
:
Δ
k
→
Δ
k
g:\Delta_{k}\to\Delta_{k}
be measurable. Then,
ℛ
ℓ
​
(
g
∘
f
)
≥
ℛ
ℓ
​
(
f
)
\mathcal{R}_{\ell}(g\circ f)\geq\mathcal{R}_{\ell}(f)
, and
𝒮
ℓ
​
(
g
∘
f
)
≤
𝒮
ℓ
​
(
f
)
\mathcal{S}_{\ell}(g\circ f)\leq\mathcal{S}_{\ell}(f)
.
3.
Let
g
:
Δ
k
→
Δ
k
g:\Delta_{k}\to\Delta_{k}
be measurable and injective. Then,
ℛ
ℓ
​
(
g
∘
f
)
=
ℛ
ℓ
​
(
f
)
\mathcal{R}_{\ell}(g\circ f)=\mathcal{R}_{\ell}(f)
, and
𝒮
ℓ
​
(
g
∘
f
)
=
𝒮
⁡
(
f
)
\mathcal{S}_{\ell}(g\circ f)=\mathcal{S}(f)
. (A similar result has been shown in Proposition 4.5 of
Gruber and Buettner [2022]
.)
4.
Suppose
f
f
is injective with a measurable left inverse (see
Theorem
A.4
for a sufficient condition). Then, the grouping loss is zero, that is,
ℛ
ℓ
​
(
f
)
=
inf
f
~
ℛ
ℓ
​
(
f
~
)
\mathcal{R}_{\ell}(f)=\inf_{\tilde{f}}\mathcal{R}_{\ell}(\tilde{f})
and
𝒮
ℓ
​
(
f
)
=
sup
f
~
ℛ
ℓ
​
(
f
~
)
\mathcal{S}_{\ell}(f)=\sup_{\tilde{f}}\mathcal{R}_{\ell}(\tilde{f})
.
Proof.
1.
By definition,
f
f
is calibrated iff
f
⁡
(
X
)
=
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
f(X)=\mathbb{E}[Y|f(X)]
almost surely. By
Theorem
3.4
,
Risk
⁡
(
g
∘
f
)
\Risk(g\circ f)
is minimized by
g
∗
​
(
q
)
=
𝔼
⁡
[
Y
|
f
⁡
(
X
)
=
q
]
=
q
g^{*}(q)=\mathbb{E}[Y|f(X)=q]=q
, where the equality holds
P
f
⁡
(
X
)
P_{f(X)}
-almost surely. Hence,
Risk
⁡
(
f
)
=
inf
g
Risk
⁡
(
g
∘
f
)
\Risk(f)=\inf_{g}\Risk(g\circ f)
. For the converse, by
Theorem
3.4
, if
ℓ
\ell
is strictly proper, the minimizer of
Risk
⁡
(
g
∘
f
)
\Risk(g\circ f)
is unique up to
P
f
⁡
(
X
)
P_{f(X)}
-null sets, hence
𝔼
⁡
[
Y
|
f
⁡
(
X
)
=
q
]
=
g
∗
​
(
q
)
=
q
\mathbb{E}[Y|f(X)=q]=g^{*}(q)=q
for
P
f
⁡
(
X
)
P_{f(X)}
-almost all
q
q
, hence
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
=
f
⁡
(
X
)
\mathbb{E}[Y|f(X)]=f(X)
almost surely.
2.
Since
h
∘
g
h\circ g
is measurable for all measurable
h
h
, we have
ℛ
ℓ
​
(
g
∘
f
)
=
inf
h
Risk
⁡
(
(
h
∘
g
)
∘
f
)
≥
inf
h
Risk
⁡
(
h
∘
f
)
=
ℛ
ℓ
​
(
f
)
.
\mathcal{R}_{\ell}(g\circ f)=\inf_{h}\Risk((h\circ g)\circ f)\geq\inf_{h}\Risk(h\circ f)=\mathcal{R}_{\ell}(f)~.
The sharpness inequality follows analogously.
Then,
ℛ
ℓ
​
(
g
∘
f
)
≤
Risk
⁡
(
(
h
∗
∘
g
−
1
)
∘
(
g
∘
f
)
)
=
Risk
⁡
(
h
∗
∘
f
)
=
ℛ
ℓ
​
(
f
)
,
\mathcal{R}_{\ell}(g\circ f)\leq\Risk((h^{*}\circ g^{-1})\circ(g\circ f))=\Risk(h^{*}\circ f)=\mathcal{R}_{\ell}(f)~,
which, together with (b), yields the claim for the refinement. The argument for sharpness is analogous.
3.
This follows analogously to (c). ∎
Theorem A.4
(Existence of measurable left inverses)
.
Let
(
X
,
ℬ
X
)
,
(
Y
,
ℬ
Y
)
(X,\mathcal{B}_{X}),(Y,\mathcal{B}_{Y})
be complete separable metric spaces with their associated Borel
σ
\sigma
-Algebra, and let
f
:
X
→
Y
f:X\to Y
be measurable and injective. Then, there exists
g
:
Y
→
X
g:Y\to X
measurable with
g
∘
f
=
id
g\circ f=\operatorname{id}
.
Proof.
Using Corollary 15.2 by
Kechris [1995]
,
f
f
is a Borel isomorphism from
X
X
to
f
⁡
(
X
)
f(X)
, so its inverse
f
−
1
:
f
⁡
(
X
)
→
X
f^{-1}:f(X)\to X
is measurable. But then, for a fixed
y
0
∈
Y
y_{0}\in Y
,
g
:
Y
→
X
,
y
↦
{
f
−
1
​
(
y
)
,
y
∈
f
(
X
)
y
0
,
y
∉
f
(
X
)
g:Y\to X,y\mapsto\begin{cases}f^{-1}(y)&,y\in f(X)\\
y_{0}&,y\not\in f(X)\end{cases}
is a measurable left-inverse to
f
f
, proving the claim.
∎
Lemma A.5
.
Let
(
Z
,
Y
)
∈
𝒵
×
𝒴
k
(Z,Y)\in\mathcal{Z}\times\mathcal{Y}_{k}
be random variables with distribution
P
P
and let
ℓ
\ell
be proper. Then,
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
𝔼
⁡
[
Y
|
Z
]
)
]
=
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
Y
)
]
.
\mathbb{E}[\ell(g(Z),\mathbb{E}[Y|Z])]=\mathbb{E}[\ell(g(Z),Y)]~.
Proof.
Since
𝒴
k
\mathcal{Y}_{k}
is a Radon space, there exists a regular conditional probability distribution
P
Y
|
Z
P_{Y|Z}
, using which we obtain
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
𝔼
⁡
[
Y
|
Z
]
)
]
\displaystyle\mathbb{E}[\ell(g(Z),\mathbb{E}[Y|Z])]
=
\displaystyle=
∫
ℓ
⁡
(
g
⁡
(
z
)
,
∫
y
​
P
Y
|
Z
​
(
𝑑
y
|
z
)
)
​
d
​
P
Z
​
(
z
)
\displaystyle\int\ell(g(z),\int yP_{Y|Z}(\,\mathrm{d}y|z))\,\mathrm{d}P_{Z}(z)
=
\displaystyle=
∬
ℓ
⁡
(
g
⁡
(
z
)
,
y
)
​
P
Y
|
Z
​
(
𝑑
y
|
z
)
​
d
​
P
Z
​
(
z
)
\displaystyle\iint\ell(g(z),y)P_{Y|Z}(\,\mathrm{d}y|z)\,\mathrm{d}P_{Z}(z)
(since
ℓ
\ell
is affine in the second argument)
=
\displaystyle=
∫
ℓ
⁡
(
g
⁡
(
z
)
,
y
)
​
𝑑
P
​
(
y
,
z
)
\displaystyle\int\ell(g(z),y)\,\mathrm{d}P(y,z)
=
\displaystyle=
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
Y
)
]
.
\displaystyle\mathbb{E}[\ell(g(Z),Y)]~.
∎
The following lemma, used in the proof of
Theorem
3.4
, provides a formal version of a well-known result.
Lemma A.6
.
Let
(
Z
,
Y
)
∈
𝒵
×
𝒴
k
(Z,Y)\in\mathcal{Z}\times\mathcal{Y}_{k}
be random variables and let
ℓ
\ell
be proper. Then, for measurable
g
:
𝒵
→
𝒴
g:\mathcal{Z}\to\mathcal{Y}
,
Risk
⁡
(
g
)
≔
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
Y
)
]
\displaystyle\Risk(g)\coloneqq\mathbb{E}[\ell(g(Z),Y)]
is minimized by
g
∗
​
(
z
)
≔
𝔼
⁡
[
Y
|
Z
=
z
]
g^{*}(z)\coloneqq\mathbb{E}[Y|Z=z]
. If
ℓ
\ell
is strictly proper, then
g
∗
g^{*}
is the unique minimizer up to
P
Z
P_{Z}
-null sets.
Proof.
We have
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
Y
)
]
\displaystyle\mathbb{E}[\ell(g(Z),Y)]
=
\displaystyle=
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
Z
)
,
𝔼
⁡
[
Y
|
Z
]
)
]
\displaystyle\mathbb{E}[\ell(g(Z),\mathbb{E}[Y|Z])]
(by
Lemma
A.5
)
≥
\displaystyle\geq
𝔼
⁡
[
ℓ
⁡
(
𝔼
⁡
[
Y
|
Z
]
,
𝔼
⁡
[
Y
|
Z
]
)
]
\displaystyle\mathbb{E}[\ell(\mathbb{E}[Y|Z],\mathbb{E}[Y|Z])]
(
ℓ
\ell
is proper)
=
\displaystyle=
𝔼
⁡
[
ℓ
⁡
(
𝔼
⁡
[
Y
|
Z
]
,
Y
)
]
\displaystyle\mathbb{E}[\ell(\mathbb{E}[Y|Z],Y)]
(by
Lemma
A.5
)
=
\displaystyle=
𝔼
⁡
[
ℓ
⁡
(
g
∗
​
(
Z
)
,
Y
)
]
.
\displaystyle\mathbb{E}[\ell(g^{*}(Z),Y)]~.
If
Risk
⁡
(
g
)
=
Risk
⁡
(
g
∗
)
\Risk(g)=\Risk(g^{*})
, the inequality above can only be strict for
z
z
in a
P
Z
P_{Z}
-null set. If
ℓ
\ell
is strictly proper, then the inequality is violated whenever
g
∗
​
(
z
)
≠
g
​
(
z
)
g^{*}(z)\neq g(z)
.
∎
Appendix B
Proofs for
Section
6
Under the data model introduced in
Section
6
,
ℙ
⁡
(
Y
=
1
|
X
=
x
)
=
σ
⁡
(
w
∗
⊤
​
x
)
\mathbb{P}(Y=1|X=x)=\sigma({w^{*}}^{\top}x)
with
w
∗
=
2
​
Σ
−
1
​
μ
w^{*}=2\Sigma^{-1}\mu
and
σ
⁡
(
x
)
=
1
1
+
e
−
x
\sigma(x)=\frac{1}{1+e^{-x}}
.
Proof.
ℙ
⁡
(
Y
=
1
|
X
=
x
)
\displaystyle\mathbb{P}(Y=1|X=x)
=
ℙ
⁡
(
X
=
x
|
Y
=
1
)
​
ℙ
​
(
Y
=
1
)
ℙ
⁡
(
X
=
x
)
using Bayes’ theorem.
\displaystyle=\frac{\mathbb{P}(X=x|Y=1)\mathbb{P}(Y=1)}{\mathbb{P}(X=x)}\quad\text{using Bayes' theorem.}
=
ℙ
⁡
(
X
=
x
|
Y
=
1
)
​
ℙ
​
(
Y
=
1
)
ℙ
⁡
(
X
=
x
|
Y
=
1
)
​
ℙ
​
(
Y
=
1
)
+
ℙ
⁡
(
X
=
x
|
Y
=
−
1
)
​
ℙ
​
(
Y
=
−
1
)
using the law of total probability.
\displaystyle=\frac{\mathbb{P}(X=x|Y=1)\mathbb{P}(Y=1)}{\mathbb{P}(X=x|Y=1)\mathbb{P}(Y=1)+\mathbb{P}(X=x|Y=-1)\mathbb{P}(Y=-1)}\quad\text{using the law of total probability.}
=
𝒩
⁡
(
x
|
μ
,
Σ
)
𝒩
⁡
(
x
|
μ
,
Σ
)
+
𝒩
⁡
(
x
|
−
μ
,
Σ
)
using that
ℙ
⁡
(
Y
=
1
)
=
ℙ
⁡
(
Y
=
−
1
)
and our data model.
\displaystyle=\frac{\mathcal{N}(x|\mu,\Sigma)}{\mathcal{N}(x|\mu,\Sigma)+\mathcal{N}(x|-\mu,\Sigma)}\quad\text{using that $\mathbb{P}(Y=1)=\mathbb{P}(Y=-1)$ and our data model.}
=
σ
(
1
2
(
x
⊤
Σ
−
1
μ
+
μ
⊤
Σ
−
1
x
+
x
⊤
Σ
−
1
μ
+
μ
⊤
Σ
−
1
x
)
)
dividing up and down by
𝒩
⁡
(
x
|
μ
,
Σ
)
.
\displaystyle=\sigma\Big(\frac{1}{2}(x^{\top}\Sigma^{-1}\mu+\mu^{\top}\Sigma^{-1}x+x^{\top}\Sigma^{-1}\mu+\mu^{\top}\Sigma^{-1}x)\Big)\quad\text{dividing up and down by $\mathcal{N}(x|\mu,\Sigma)$.}
=
σ
⁡
(
2
​
μ
⊤
​
Σ
−
1
​
x
)
=
σ
⁡
(
w
∗
⊤
​
x
)
\displaystyle=\sigma(2\mu^{\top}\Sigma^{-1}x)=\sigma({w^{*}}^{\top}x)
With
w
∗
=
2
​
Σ
−
1
​
μ
w^{*}=2\Sigma^{-1}\mu
.
∎
We now prove the following lemmas that we will use to demonstrate
Proposition
6.1
.
Lemma B.1
.
ℙ
⁡
(
Y
=
1
|
f
⁡
(
X
)
=
σ
⁡
(
z
)
)
=
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
​
z
)
\mathbb{P}(Y=1|f(X)=\sigma(z))=\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}^{2}}z\Big)
.
Lemma B.2
.
ℙ
⁡
(
f
⁡
(
X
)
=
σ
⁡
(
z
)
)
=
1
2
​
𝒩
​
(
z
|
⟨
w
,
w
∗
⟩
Σ
2
,
‖
w
‖
Σ
2
)
+
1
2
​
𝒩
​
(
z
|
−
⟨
w
,
w
∗
⟩
Σ
2
,
‖
w
‖
Σ
2
)
\mathbb{P}(f(X)=\sigma(z))=\frac{1}{2}\mathcal{N}(z|\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2})+\frac{1}{2}\mathcal{N}(z|-\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2})
.
Proof.
ℙ
⁡
(
Y
=
1
|
f
⁡
(
X
)
=
σ
⁡
(
z
)
)
\displaystyle\mathbb{P}(Y=1|f(X)=\sigma(z))
=
ℙ
⁡
(
Y
=
1
|
σ
⁡
(
w
⊤
​
X
)
=
σ
⁡
(
z
)
)
\displaystyle=\mathbb{P}(Y=1|\sigma(w^{\top}X)=\sigma(z))
=
ℙ
⁡
(
Y
=
1
|
w
⊤
​
X
=
z
)
\displaystyle=\mathbb{P}(Y=1|w^{\top}X=z)
=
ℙ
⁡
(
w
⊤
​
X
=
z
|
Y
=
1
)
​
ℙ
​
(
Y
=
1
)
ℙ
⁡
(
w
⊤
​
X
=
z
)
\displaystyle=\frac{\mathbb{P}(w^{\top}X=z|Y=1)\mathbb{P}(Y=1)}{\mathbb{P}(w^{\top}X=z)}
=
ℙ
⁡
(
w
⊤
​
X
=
z
|
Y
=
1
)
​
ℙ
​
(
Y
=
1
)
ℙ
⁡
(
w
⊤
​
X
=
z
|
Y
=
1
)
​
ℙ
​
(
Y
=
1
)
+
ℙ
⁡
(
w
⊤
​
X
=
z
|
Y
=
−
1
)
​
ℙ
​
(
Y
=
−
1
)
\displaystyle=\frac{\mathbb{P}(w^{\top}X=z|Y=1)\mathbb{P}(Y=1)}{\mathbb{P}(w^{\top}X=z|Y=1)\mathbb{P}(Y=1)+\mathbb{P}(w^{\top}X=z|Y=-1)\mathbb{P}(Y=-1)}
Using that the affine transformation of a multivariate normal dist. is a normal dist. (
w
⊤
​
X
∼
𝒩
⁡
(
±
w
⊤
​
μ
,
w
⊤
​
Σ
​
w
)
w^{\top}X\sim\mathcal{N}(\pm w^{\top}\mu,w^{\top}\Sigma w)
)
=
𝒩
⁡
(
z
|
w
⊤
​
μ
,
w
⊤
​
Σ
​
w
)
𝒩
⁡
(
z
|
w
⊤
​
μ
,
w
⊤
​
Σ
​
w
)
+
𝒩
⁡
(
z
|
−
w
⊤
​
μ
,
w
⊤
​
Σ
​
w
)
\displaystyle=\frac{\mathcal{N}(z|w^{\top}\mu,w^{\top}\Sigma w)}{\mathcal{N}(z|w^{\top}\mu,w^{\top}\Sigma w)+\mathcal{N}(z|-w^{\top}\mu,w^{\top}\Sigma w)}
=
σ
⁡
(
(
z
+
w
⊤
​
μ
)
2
−
(
z
−
w
⊤
​
μ
)
2
2
​
w
⊤
​
Σ
​
w
)
=
σ
⁡
(
2
​
w
⊤
​
μ
w
⊤
​
Σ
​
w
​
z
)
=
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
​
z
)
\displaystyle=\sigma\Bigg(\frac{(z+w^{\top}\mu)^{2}-(z-w^{\top}\mu)^{2}}{2w^{\top}\Sigma w}\Bigg)=\sigma\Bigg(\frac{2w^{\top}\mu}{w^{\top}\Sigma w}z\Bigg)=\sigma\Bigg(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}^{2}}z\Bigg)
Along the way, we derived the distribution of
f
⁡
(
X
)
f(X)
:
ℙ
⁡
(
f
⁡
(
X
)
=
σ
⁡
(
z
)
)
\displaystyle\mathbb{P}(f(X)=\sigma(z))
=
ℙ
⁡
(
w
⊤
​
X
=
z
|
Y
=
1
)
​
ℙ
​
(
Y
=
1
)
+
ℙ
⁡
(
w
⊤
​
X
=
z
|
Y
=
−
1
)
​
ℙ
​
(
Y
=
−
1
)
\displaystyle=\mathbb{P}(w^{\top}X=z|Y=1)\mathbb{P}(Y=1)+\mathbb{P}(w^{\top}X=z|Y=-1)\mathbb{P}(Y=-1)
=
1
2
​
𝒩
​
(
z
|
w
⊤
​
μ
,
w
⊤
​
Σ
​
w
)
+
1
2
​
𝒩
​
(
z
|
−
w
⊤
​
μ
,
w
⊤
​
Σ
​
w
)
\displaystyle=\frac{1}{2}\mathcal{N}(z|w^{\top}\mu,w^{\top}\Sigma w)+\frac{1}{2}\mathcal{N}(z|-w^{\top}\mu,w^{\top}\Sigma w)
=
1
2
​
𝒩
​
(
z
|
⟨
w
,
w
∗
⟩
Σ
2
,
‖
w
‖
Σ
2
)
+
1
2
​
𝒩
​
(
z
|
−
⟨
w
,
w
∗
⟩
Σ
2
,
‖
w
‖
Σ
2
)
\displaystyle=\frac{1}{2}\mathcal{N}(z|\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2})+\frac{1}{2}\mathcal{N}(z|-\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2})
∎
See
6.1
Proof.
The refinement error writes
ℛ
⁡
(
w
)
=
𝔼
f
⁡
(
X
)
​
[
e
ℓ
​
(
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
)
]
\mathcal{R}(w)=\mathbb{E}_{f(X)}[e_{\ell}(\mathbb{E}[Y|f(X)])]
Using
Lemma
B.1
and
Lemma
B.2
,
ℛ
⁡
(
w
)
=
\displaystyle\mathcal{R}(w)=
1
2
​
∫
e
ℓ
​
(
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
​
z
)
)
​
𝒩
​
(
z
|
⟨
w
,
w
∗
⟩
Σ
2
,
‖
w
‖
Σ
2
)
​
𝑑
z
\displaystyle\frac{1}{2}\int e_{\ell}\Bigg(\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}^{2}}z\Big)\Bigg)\mathcal{N}\Big(z\Big|\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2}\Big)dz
+
1
2
∫
e
ℓ
(
σ
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
z
)
)
𝒩
(
z
|
−
⟨
w
,
w
∗
⟩
Σ
2
,
∥
w
∥
Σ
2
)
d
z
.
\displaystyle+\frac{1}{2}\int e_{\ell}\Bigg(\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}^{2}}z\Big)\Bigg)\mathcal{N}\Big(z\Big|-\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2}\Big)dz\,.
Taking
u
=
(
z
−
⟨
w
,
w
∗
⟩
Σ
2
)
/
‖
w
‖
Σ
u=(z\!-\!\frac{\langle w,w^{*}\rangle_{\Sigma}}{2})/\|w\|_{\Sigma}
in the first integral and
u
=
(
z
+
⟨
w
,
w
∗
⟩
Σ
2
)
/
‖
w
‖
Σ
u=(z\!+\!\frac{\langle w,w^{*}\rangle_{\Sigma}}{2})/\|w\|_{\Sigma}
in the second, we get
ℛ
⁡
(
w
)
=
\displaystyle\mathcal{R}(w)=
1
2
​
∫
e
ℓ
​
(
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
​
u
+
⟨
w
,
w
∗
⟩
Σ
2
2
​
‖
w
‖
Σ
2
)
)
​
𝒩
​
(
u
|
0
,
1
)
​
𝑑
u
\displaystyle\frac{1}{2}\int e_{\ell}\Bigg(\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}}u+\frac{\langle w,w^{*}\rangle_{\Sigma}^{2}}{2\|w\|_{\Sigma}^{2}}\Big)\Bigg)\mathcal{N}(u|0,1)du
+
1
2
∫
e
ℓ
(
σ
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
u
−
⟨
w
,
w
∗
⟩
Σ
2
2
​
‖
w
‖
Σ
2
)
)
𝒩
(
u
|
0
,
1
)
d
u
.
\displaystyle+\frac{1}{2}\int e_{\ell}\Bigg(\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}}u-\frac{\langle w,w^{*}\rangle_{\Sigma}^{2}}{2\|w\|_{\Sigma}^{2}}\Big)\Bigg)\mathcal{N}(u|0,1)du\,.
σ
\sigma
is anti-symmetric around zero, assuming
e
ℓ
e_{\ell}
symmetric around
1
2
\frac{1}{2}
the two terms are equal, which simplifies the expression,
ℛ
⁡
(
w
)
=
𝔼
z
∼
𝒩
⁡
(
0
,
1
)
​
[
e
ℓ
​
(
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
​
(
z
+
⟨
w
,
w
∗
⟩
Σ
2
​
‖
w
‖
Σ
)
)
)
]
.
\mathcal{R}(w)=\mathbb{E}_{z\sim\mathcal{N}(0,1)}\Big[e_{\ell}\Big(\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}}\Big(z+\frac{\langle w,w^{*}\rangle_{\Sigma}}{2\|w\|_{\Sigma}}\Big)\Big)\Big)\Big]\,.
Similarly for the calibration error
𝒦
⁡
(
w
)
\displaystyle\mathcal{K}(w)
=
𝔼
f
⁡
(
X
)
​
[
d
ℓ
​
(
f
⁡
(
X
)
,
𝔼
⁡
[
Y
|
f
⁡
(
X
)
]
)
]
\displaystyle=\mathbb{E}_{f(X)}[d_{\ell}(f(X),\mathbb{E}[Y|f(X)])]
=
1
2
​
∫
d
ℓ
​
(
σ
⁡
(
z
)
,
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
​
z
)
)
​
𝒩
​
(
z
|
⟨
w
,
w
∗
⟩
Σ
2
,
‖
w
‖
Σ
2
)
​
𝑑
z
\displaystyle=\frac{1}{2}\int d_{\ell}\Big(\sigma(z),\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}^{2}}z\Big)\Big)\mathcal{N}\Big(z\Big|\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2}\Big)dz
+
1
2
∫
d
ℓ
(
σ
(
z
)
,
σ
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
z
)
)
𝒩
(
z
|
−
⟨
w
,
w
∗
⟩
Σ
2
,
∥
w
∥
Σ
2
)
d
z
\displaystyle+\frac{1}{2}\int d_{\ell}\Big(\sigma(z),\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}^{2}}z\Big)\Big)\mathcal{N}\Big(z\Big|-\frac{\langle w,w^{*}\rangle_{\Sigma}}{2},\|w\|_{\Sigma}^{2}\Big)dz
=
1
2
​
∫
d
ℓ
​
(
σ
⁡
(
‖
w
‖
Σ
​
z
+
⟨
w
,
w
∗
⟩
Σ
2
)
,
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
​
z
+
⟨
w
,
w
∗
⟩
Σ
2
2
​
‖
w
‖
Σ
2
)
)
​
𝒩
​
(
z
|
0
,
1
)
​
𝑑
z
\displaystyle=\frac{1}{2}\int d_{\ell}\Big(\sigma\Big(\|w\|_{\Sigma}z+\frac{\langle w,w^{*}\rangle_{\Sigma}}{2}\Big),\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}}z+\frac{\langle w,w^{*}\rangle_{\Sigma}^{2}}{2\|w\|_{\Sigma}^{2}}\Big)\Bigg)\mathcal{N}(z|0,1)dz
+
1
2
∫
d
ℓ
(
σ
(
∥
w
∥
Σ
z
−
⟨
w
,
w
∗
⟩
Σ
2
)
,
σ
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
z
−
⟨
w
,
w
∗
⟩
Σ
2
2
​
‖
w
‖
Σ
2
)
)
𝒩
(
z
|
0
,
1
)
d
z
\displaystyle+\frac{1}{2}\int d_{\ell}\Big(\sigma\Big(\|w\|_{\Sigma}z-\frac{\langle w,w^{*}\rangle_{\Sigma}}{2}\Big),\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}}z-\frac{\langle w,w^{*}\rangle_{\Sigma}^{2}}{2\|w\|_{\Sigma}^{2}}\Big)\Big)\mathcal{N}(z|0,1)dz
σ
\sigma
is anti-symmetric around zero, assuming
d
ℓ
d_{\ell}
symmetric around
1
2
\frac{1}{2}
the two terms are equal,
𝒦
⁡
(
w
)
=
𝔼
z
∼
𝒩
⁡
(
0
,
1
)
​
[
d
ℓ
​
(
σ
⁡
(
‖
w
‖
Σ
​
(
z
+
⟨
w
,
w
∗
⟩
Σ
2
​
‖
w
‖
Σ
)
)
,
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
​
(
z
+
⟨
w
,
w
∗
⟩
Σ
2
​
‖
w
‖
Σ
)
)
)
]
.
\mathcal{K}(w)=\mathbb{E}_{z\sim\mathcal{N}(0,1)}\Big[d_{\ell}\Big(\sigma\Big(\|w\|_{\Sigma}\Big(z+\frac{\langle w,w^{*}\rangle_{\Sigma}}{2\|w\|_{\Sigma}}\Big)\Big),\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}}\Big(z+\frac{\langle w,w^{*}\rangle_{\Sigma}}{2\|w\|_{\Sigma}}\Big)\Big)\Big)\Big]\,.
∎
See
6.2
Proof.
a
w
=
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
a_{w}=\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|_{\Sigma}}
is invariant by rescaling. Given
s
∈
ℝ
,
w
s
=
s
​
w
s\in\mathbb{R},w_{s}=sw
, we have that
a
w
s
=
⟨
s
​
w
,
w
∗
⟩
Σ
‖
s
​
w
‖
Σ
=
s
​
⟨
w
,
w
∗
⟩
Σ
s
​
‖
w
‖
Σ
=
a
w
a_{w_{s}}=\frac{\langle sw,w^{*}\rangle_{\Sigma}}{\|sw\|_{\Sigma}}=\frac{s\langle w,w^{*}\rangle_{\Sigma}}{s\|w\|_{\Sigma}}=a_{w}
. The expression of refinement error in
Proposition
6.1
depends on
w
w
only via
a
w
a_{w}
so the refinement is invariant by rescaling.
The calibration error writes:
𝒦
⁡
(
w
)
=
𝔼
z
∼
𝒩
⁡
(
0
,
1
)
​
[
d
ℓ
​
(
σ
⁡
(
‖
w
‖
Σ
​
(
z
+
a
w
2
)
)
,
σ
⁡
(
a
w
​
(
z
+
a
w
2
)
)
)
]
\mathcal{K}(w)=\mathbb{E}_{z\sim\mathcal{N}(0,1)}\Big[d_{\ell}\Big(\sigma\Big(\|w\|_{\Sigma}\Big(z+\frac{a_{w}}{2}\Big)\Big),\sigma\Big(a_{w}\Big(z+\frac{a_{w}}{2}\Big)\Big)\Big)\Big]
Since
a
w
a_{w}
is invariant by rescaling, taking
w
s
=
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
​
w
w_{s}=\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|^{2}_{\Sigma}}w
yields
𝒦
⁡
(
w
s
)
\displaystyle\mathcal{K}(w_{s})
=
𝔼
z
∼
𝒩
⁡
(
0
,
1
)
​
[
d
ℓ
​
(
σ
⁡
(
⟨
w
,
w
∗
⟩
Σ
‖
w
‖
Σ
2
​
‖
w
‖
Σ
​
(
z
+
a
w
2
)
)
,
σ
⁡
(
a
w
​
(
z
+
a
w
2
)
)
)
]
\displaystyle=\mathbb{E}_{z\sim\mathcal{N}(0,1)}\Big[d_{\ell}\Big(\sigma\Big(\frac{\langle w,w^{*}\rangle_{\Sigma}}{\|w\|^{2}_{\Sigma}}\|w\|_{\Sigma}\Big(z+\frac{a_{w}}{2}\Big)\Big),\sigma\Big(a_{w}\Big(z+\frac{a_{w}}{2}\Big)\Big)\Big)\Big]
=
𝔼
z
∼
𝒩
⁡
(
0
,
1
)
​
[
d
ℓ
​
(
σ
⁡
(
a
w
​
(
z
+
a
w
2
)
)
,
σ
⁡
(
a
w
​
(
z
+
a
w
2
)
)
)
]
\displaystyle=\mathbb{E}_{z\sim\mathcal{N}(0,1)}\Big[d_{\ell}\Big(\sigma\Big(a_{w}\Big(z+\frac{a_{w}}{2}\Big)\Big),\sigma\Big(a_{w}\Big(z+\frac{a_{w}}{2}\Big)\Big)\Big)\Big]
=
0
since
ℓ
is a proper score (
d
ℓ
​
(
p
,
p
)
=
0
).
\displaystyle=0\quad\text{since $\ell$ is a proper score ($d_{\ell}(p,p)=0$).}
∎
Appendix C
Proofs for
Section
7
For this section, we rely heavily on the following result by
Mai et al. [2019]
, on the limit distribution of the weight vector for regularized logistic regression, with regularization strength
λ
\lambda
, when
n
,
p
→
∞
n,p\rightarrow\infty
with a fixed ratio
p
/
n
→
r
p/n\rightarrow r
:
w
λ
∼
𝒩
⁡
(
η
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
​
μ
,
γ
n
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
​
Σ
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
)
.
w_{\lambda}\sim\mathcal{N}\Big(\eta(\lambda I_{p}+\tau\Sigma)^{-1}\mu,\frac{\gamma}{n}(\lambda I_{p}+\tau\Sigma)^{-1}\Sigma(\lambda I_{p}+\tau\Sigma)^{-1}\Big).
See
7.1
Proof.
⟨
w
λ
,
w
∗
⟩
Σ
\langle w_{\lambda},w^{*}\rangle_{\Sigma}
follows a normal distribution with mean
2
​
η
​
μ
⊤
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
​
μ
2\eta\mu^{\top}(\lambda I_{p}+\tau\Sigma)^{-1}\mu
and variance
4
​
γ
n
​
μ
⊤
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
​
Σ
​
(
λ
​
I
p
+
τ
​
Σ
)
−
1
​
μ
\frac{4\gamma}{n}\mu^{\top}(\lambda I_{p}+\tau\Sigma)^{-1}\Sigma(\lambda I_{p}+\tau\Sigma)^{-1}\mu
.
Looking at the variance first:
𝕍
⁡
(
⟨
w
λ
,
w
∗
⟩
Σ
)
=
4
​
γ
n
​
∑
i
=
1
p
σ
i
​
μ
i
2
(
λ
+
τ
​
σ
i
)
2
.
\mathbb{V}(\langle w_{\lambda},w^{*}\rangle_{\Sigma})=\frac{4\gamma}{n}\sum_{i=1}^{p}\frac{\sigma_{i}\mu_{i}^{2}}{(\lambda+\tau\sigma_{i})^{2}}\quad.
Using independence between
μ
i
\mu_{i}
and
σ
i
\sigma_{i}
and the strong law of large numbers
𝕍
⁡
(
⟨
w
λ
,
w
∗
⟩
Σ
)
→
p
→
∞
\displaystyle\mathbb{V}(\langle w_{\lambda},w^{*}\rangle_{\Sigma})\xrightarrow{p\rightarrow\infty}
4
​
γ
n
​
p
​
𝔼
​
[
μ
i
2
]
​
𝔼
​
[
σ
i
(
λ
+
τ
​
σ
i
)
2
]
\displaystyle\frac{4\gamma}{n}p\mathbb{E}[\mu_{i}^{2}]\mathbb{E}\Big[\frac{\sigma_{i}}{(\lambda+\tau\sigma_{i})^{2}}\Big]
=
\displaystyle=
4
​
γ
​
c
2
n
​
𝔼
​
[
σ
i
(
λ
+
τ
​
σ
i
)
2
]
→
n
→
∞
0
.
\displaystyle\frac{4\gamma c^{2}}{n}\mathbb{E}\Big[\frac{\sigma_{i}}{(\lambda+\tau\sigma_{i})^{2}}\Big]\xrightarrow{n\rightarrow\infty}0\quad.
So
⟨
w
λ
,
w
∗
⟩
Σ
\langle w_{\lambda},w^{*}\rangle_{\Sigma}
concentrates on its mean:
𝔼
⁡
(
⟨
w
λ
,
w
∗
⟩
Σ
)
=
2
​
η
​
∑
i
=
1
p
μ
i
2
λ
+
τ
​
σ
i
→
p
→
∞
2
​
η
​
p
​
𝔼
​
[
μ
i
2
]
​
𝔼
​
[
1
λ
+
τ
​
σ
i
]
=
2
​
η
​
c
2
​
𝔼
​
[
1
λ
+
τ
​
σ
i
]
.
\mathbb{E}(\langle w_{\lambda},w^{*}\rangle_{\Sigma})=2\eta\sum_{i=1}^{p}\frac{\mu_{i}^{2}}{\lambda+\tau\sigma_{i}}\xrightarrow{p\rightarrow\infty}2\eta p\mathbb{E}[\mu_{i}^{2}]\mathbb{E}\Big[\frac{1}{\lambda+\tau\sigma_{i}}\Big]=2\eta c^{2}\mathbb{E}\Big[\frac{1}{\lambda+\tau\sigma_{i}}\Big]\quad.
Studying
w
λ
⊤
​
Σ
​
w
λ
w_{\lambda}^{\top}\Sigma w_{\lambda}
requires a bit more work. Denoting
ε
=
𝒩
⁡
(
0
,
1
)
\varepsilon=\mathcal{N}(0,1)
,
w
λ
⊤
​
Σ
​
w
λ
\displaystyle w_{\lambda}^{\top}\Sigma w_{\lambda}
∼
∑
i
=
1
p
σ
i
​
w
λ
i
2
\displaystyle\sim\sum_{i=1}^{p}\sigma_{i}{w_{\lambda}}_{i}^{2}
=
∑
i
=
1
p
σ
i
​
(
η
​
μ
i
λ
+
τ
​
σ
i
+
ε
​
γ
​
σ
i
n
​
(
λ
+
τ
​
σ
i
)
2
)
2
\displaystyle=\sum_{i=1}^{p}\sigma_{i}\Big(\frac{\eta\mu_{i}}{\lambda+\tau\sigma_{i}}+\varepsilon\sqrt{\frac{\gamma\sigma_{i}}{n(\lambda+\tau\sigma_{i})^{2}}}\Big)^{2}
=
∑
i
=
1
p
η
2
​
μ
i
2
​
σ
i
(
λ
+
τ
​
σ
i
)
2
+
∑
i
=
1
p
2
​
η
​
μ
i
​
γ
​
σ
i
3
/
2
n
​
(
λ
+
τ
​
σ
i
)
2
​
ε
+
∑
i
=
1
p
γ
​
σ
i
2
n
​
(
λ
+
τ
​
σ
i
)
2
​
ε
2
\displaystyle=\sum_{i=1}^{p}\frac{\eta^{2}\mu_{i}^{2}\sigma_{i}}{(\lambda+\tau\sigma_{i})^{2}}+\sum_{i=1}^{p}\frac{2\eta\mu_{i}\sqrt{\gamma}\sigma_{i}^{3/2}}{\sqrt{n}(\lambda+\tau\sigma_{i})^{2}}\varepsilon+\sum_{i=1}^{p}\frac{\gamma\sigma_{i}^{2}}{n(\lambda+\tau\sigma_{i})^{2}}\varepsilon^{2}
→
p
→
∞
p
​
η
2
​
c
2
p
​
𝔼
​
[
σ
(
λ
+
τ
​
σ
)
2
]
+
0
+
p
​
γ
n
​
𝔼
​
[
σ
2
(
λ
+
τ
​
σ
)
2
]
\displaystyle\xrightarrow{p\rightarrow\infty}p\eta^{2}\frac{c^{2}}{p}\mathbb{E}\Big[\frac{\sigma}{(\lambda+\tau\sigma)^{2}}\Big]+0+p\frac{\gamma}{n}\mathbb{E}\Big[\frac{\sigma^{2}}{(\lambda+\tau\sigma)^{2}}\Big]
=
η
2
​
c
2
​
𝔼
​
[
σ
(
λ
+
τ
​
σ
)
2
]
+
γ
​
r
​
𝔼
​
[
σ
2
(
λ
+
τ
​
σ
)
2
]
.
\displaystyle=\eta^{2}c^{2}\mathbb{E}\Big[\frac{\sigma}{(\lambda+\tau\sigma)^{2}}\Big]+\gamma r\mathbb{E}\Big[\frac{\sigma^{2}}{(\lambda+\tau\sigma)^{2}}\Big]\quad.
∎
See
7.3
Proof.
err
⁡
(
w
∗
)
=
Φ
⁡
(
−
⟨
w
∗
,
w
∗
⟩
Σ
2
​
‖
w
∗
‖
Σ
)
=
Φ
⁡
(
−
w
∗
⊤
​
Σ
​
w
∗
2
)
=
Φ
⁡
(
−
μ
⊤
​
Σ
−
1
​
μ
)
→
a
.
s
Φ
⁡
(
−
p
​
𝔼
​
[
μ
2
]
​
𝔼
​
[
1
σ
]
)
=
Φ
⁡
(
−
c
​
𝔼
⁡
[
σ
−
1
]
)
\err(w^{*})=\Phi(-\frac{\langle w^{*},w^{*}\rangle_{\Sigma}}{2\|w^{*}\|_{\Sigma}})=\Phi(-\frac{\sqrt{{w^{*}}^{\top}\Sigma w^{*}}}{2})=\Phi(-\sqrt{\mu^{\top}\Sigma^{-1}\mu})\xrightarrow{a.s}\Phi(-\sqrt{p\mathbb{E}[\mu^{2}]\mathbb{E}[\frac{1}{\sigma}]})=\Phi(-c\sqrt{\mathbb{E}[\sigma^{-1}]})
∎
Deriving formulas for
err
⁡
(
w
∗
)
\err(w^{*})
,
⟨
w
λ
,
w
∗
⟩
Σ
\langle w_{\lambda},w^{*}\rangle_{\Sigma}
and
‖
w
λ
‖
Σ
\|w_{\lambda}\|_{\Sigma}
𝔼
⁡
[
σ
−
1
]
\displaystyle\mathbb{E}[\sigma^{-1}]
=
∫
0
1
1
u
+
ε
​
u
α
−
1
​
(
1
−
u
)
β
−
1
B
⁡
(
α
,
β
)
​
𝑑
u
\displaystyle=\int_{0}^{1}\frac{1}{u+\varepsilon}\frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha,\beta)}du
=
1
ε
​
B
​
(
α
,
β
)
​
∫
0
1
(
1
+
u
ε
)
−
1
​
u
α
−
1
​
(
1
−
u
)
β
−
1
​
𝑑
u
\displaystyle=\frac{1}{\varepsilon B(\alpha,\beta)}\int_{0}^{1}(1+\frac{u}{\varepsilon})^{-1}u^{\alpha-1}(1-u)^{\beta-1}du
=
F
1
2
​
(
1
,
α
,
α
+
β
,
−
1
ε
)
ε
.
\displaystyle=\frac{{}_{2}F_{1}(1,\alpha,\alpha+\beta,-\frac{1}{\varepsilon})}{\varepsilon}\quad.
Altogether
err
⁡
(
w
∗
)
=
Φ
⁡
(
−
c
​
1
ε
​
F
1
2
​
(
1
,
α
,
α
+
β
,
−
1
ε
)
)
.
\err(w^{*})=\Phi\Bigg(-c\sqrt{\frac{1}{\varepsilon}{}_{2}F_{1}(1,\alpha,\alpha+\beta,-\frac{1}{\varepsilon})}\Bigg)\quad.
Lemma C.1
.
Denoting
F
1
2
{}_{2}F_{1}
the hyper-geometric function,
ℬ
\mathcal{B}
the Beta distribution and
B
B
the beta function,
𝔼
u
∼
ℬ
⁡
(
α
,
β
)
​
[
1
λ
+
τ
⁡
(
ε
+
u
)
]
\displaystyle\mathbb{E}_{u\sim\mathcal{B}(\alpha,\beta)}\Big[\frac{1}{\lambda+\tau(\varepsilon+u)}\Big]
=
∫
0
1
1
λ
+
τ
⁡
(
ε
+
u
)
​
u
α
−
1
​
(
1
−
u
)
β
−
1
B
⁡
(
α
,
β
)
​
𝑑
u
\displaystyle=\int_{0}^{1}\frac{1}{\lambda+\tau(\varepsilon+u)}\frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha,\beta)}du
=
1
(
λ
+
τ
​
ε
)
​
B
​
(
α
,
β
)
​
∫
0
1
(
1
+
τ
λ
+
τ
​
ε
​
u
)
−
1
​
u
α
−
1
​
(
1
−
u
)
β
−
1
​
𝑑
u
\displaystyle=\frac{1}{(\lambda+\tau\varepsilon)B(\alpha,\beta)}\int_{0}^{1}(1+\frac{\tau}{\lambda+\tau\varepsilon}u)^{-1}u^{\alpha-1}(1-u)^{\beta-1}du
=
F
1
2
​
(
1
,
α
,
α
+
β
,
−
(
λ
τ
+
ε
)
−
1
)
λ
+
τ
​
ε
\displaystyle=\frac{{}_{2}F_{1}(1,\alpha,\alpha+\beta,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})}{\lambda+\tau\varepsilon}
𝔼
u
∼
ℬ
⁡
(
α
,
β
)
​
[
1
(
λ
+
τ
⁡
(
ε
+
u
)
)
2
]
\displaystyle\mathbb{E}_{u\sim\mathcal{B}(\alpha,\beta)}\Big[\frac{1}{(\lambda+\tau(\varepsilon+u))^{2}}\Big]
=
∫
0
1
1
(
λ
+
τ
⁡
(
ε
+
u
)
)
2
​
u
α
−
1
​
(
1
−
u
)
β
−
1
B
⁡
(
α
,
β
)
​
𝑑
u
\displaystyle=\int_{0}^{1}\frac{1}{(\lambda+\tau(\varepsilon+u))^{2}}\frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha,\beta)}du
=
1
(
λ
+
τ
​
ε
)
2
​
B
​
(
α
,
β
)
​
∫
0
1
(
1
+
τ
λ
+
τ
​
ε
​
u
)
−
2
​
u
α
−
1
​
(
1
−
u
)
β
−
1
​
𝑑
u
\displaystyle=\frac{1}{(\lambda+\tau\varepsilon)^{2}B(\alpha,\beta)}\int_{0}^{1}(1+\frac{\tau}{\lambda+\tau\varepsilon}u)^{-2}u^{\alpha-1}(1-u)^{\beta-1}du
=
F
1
2
​
(
2
,
α
,
α
+
β
,
−
(
λ
τ
+
ε
)
−
1
)
(
λ
+
τ
​
ε
)
2
\displaystyle=\frac{{}_{2}F_{1}(2,\alpha,\alpha+\beta,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})}{(\lambda+\tau\varepsilon)^{2}}
𝔼
u
∼
ℬ
⁡
(
α
,
β
)
​
[
u
(
λ
+
τ
⁡
(
ε
+
u
)
)
2
]
\displaystyle\mathbb{E}_{u\sim\mathcal{B}(\alpha,\beta)}\Big[\frac{u}{(\lambda+\tau(\varepsilon+u))^{2}}\Big]
=
∫
0
1
u
(
λ
+
τ
⁡
(
ε
+
u
)
)
2
​
u
α
−
1
​
(
1
−
u
)
β
−
1
B
⁡
(
α
,
β
)
​
𝑑
u
\displaystyle=\int_{0}^{1}\frac{u}{(\lambda+\tau(\varepsilon+u))^{2}}\frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha,\beta)}du
=
1
(
λ
+
τ
​
ε
)
2
​
B
​
(
α
,
β
)
​
∫
0
1
(
1
+
τ
λ
+
τ
​
ε
​
u
)
−
2
​
u
α
​
(
1
−
u
)
β
−
1
​
𝑑
u
\displaystyle=\frac{1}{(\lambda+\tau\varepsilon)^{2}B(\alpha,\beta)}\int_{0}^{1}(1+\frac{\tau}{\lambda+\tau\varepsilon}u)^{-2}u^{\alpha}(1-u)^{\beta-1}du
=
B
⁡
(
α
+
1
,
β
)
B
⁡
(
α
,
β
)
​
(
λ
+
τ
​
ε
)
2
​
F
1
2
​
(
2
,
α
+
1
,
α
+
β
+
1
,
−
(
λ
τ
+
ε
)
−
1
)
\displaystyle=\frac{B(\alpha+1,\beta)}{B(\alpha,\beta)(\lambda+\tau\varepsilon)^{2}}{}_{2}F_{1}(2,\alpha+1,\alpha+\beta+1,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})
𝔼
u
∼
ℬ
⁡
(
α
,
β
)
​
[
u
2
(
λ
+
τ
⁡
(
ε
+
u
)
)
2
]
\displaystyle\mathbb{E}_{u\sim\mathcal{B}(\alpha,\beta)}\Big[\frac{u^{2}}{(\lambda+\tau(\varepsilon+u))^{2}}\Big]
=
∫
0
1
u
2
(
λ
+
τ
⁡
(
ε
+
u
)
)
2
​
u
α
−
1
​
(
1
−
u
)
β
−
1
B
⁡
(
α
,
β
)
​
𝑑
u
\displaystyle=\int_{0}^{1}\frac{u^{2}}{(\lambda+\tau(\varepsilon+u))^{2}}\frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha,\beta)}du
=
1
(
λ
+
τ
​
ε
)
2
​
B
​
(
α
,
β
)
​
∫
0
1
(
1
+
τ
λ
+
τ
​
ε
​
u
)
−
2
​
u
α
+
1
​
(
1
−
u
)
β
−
1
​
𝑑
u
\displaystyle=\frac{1}{(\lambda+\tau\varepsilon)^{2}B(\alpha,\beta)}\int_{0}^{1}(1+\frac{\tau}{\lambda+\tau\varepsilon}u)^{-2}u^{\alpha+1}(1-u)^{\beta-1}du
=
B
⁡
(
α
+
2
,
β
)
B
⁡
(
α
,
β
)
​
(
λ
+
τ
​
ε
)
2
​
F
1
2
​
(
2
,
α
+
2
,
α
+
β
+
2
,
−
(
λ
τ
+
ε
)
−
1
)
.
\displaystyle=\frac{B(\alpha+2,\beta)}{B(\alpha,\beta)(\lambda+\tau\varepsilon)^{2}}{}_{2}F_{1}(2,\alpha+2,\alpha+\beta+2,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})\quad.
Using the equations in
Lemma
C.1
and the linearity of the expectation we get that
⟨
w
λ
,
w
∗
⟩
Σ
→
(
n
,
p
)
→
∞
2
​
η
​
c
2
​
𝔼
​
[
1
λ
+
τ
​
σ
]
=
2
​
η
​
c
2
​
F
1
2
​
(
1
,
α
,
α
+
β
,
−
(
λ
τ
+
ε
)
−
1
)
λ
+
τ
​
ε
.
\langle w_{\lambda},w^{*}\rangle_{\Sigma}\xrightarrow{(n,p)\rightarrow\infty}2\eta c^{2}\mathbb{E}\Big[\frac{1}{\lambda+\tau\sigma}\Big]=2\eta c^{2}\frac{{}_{2}F_{1}(1,\alpha,\alpha+\beta,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})}{\lambda+\tau\varepsilon}\quad.
Similarly,
‖
w
λ
‖
Σ
2
\displaystyle\|w_{\lambda}\|_{\Sigma}^{2}
→
(
n
,
p
)
→
∞
η
2
​
c
2
​
𝔼
​
[
σ
(
λ
+
τ
​
σ
)
2
]
+
γ
​
r
​
𝔼
​
[
σ
2
(
λ
+
τ
​
σ
)
2
]
\displaystyle\xrightarrow{(n,p)\rightarrow\infty}\eta^{2}c^{2}\mathbb{E}\Big[\frac{\sigma}{(\lambda+\tau\sigma)^{2}}\Big]+\gamma r\mathbb{E}\Big[\frac{\sigma^{2}}{(\lambda+\tau\sigma)^{2}}\Big]
=
η
2
​
c
2
(
λ
+
τ
​
ε
)
2
​
(
ε
​
F
1
2
​
(
2
,
α
,
α
+
β
,
−
(
λ
τ
+
ε
)
−
1
)
+
B
⁡
(
α
+
1
,
β
)
B
⁡
(
α
,
β
)
​
F
1
2
​
(
2
,
α
+
1
,
α
+
β
+
1
,
−
(
λ
τ
+
ε
)
−
1
)
)
\displaystyle=\frac{\eta^{2}c^{2}}{(\lambda+\tau\varepsilon)^{2}}\Bigg(\varepsilon{}_{2}F_{1}(2,\alpha,\alpha+\beta,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})+\frac{B(\alpha+1,\beta)}{B(\alpha,\beta)}{}_{2}F_{1}(2,\alpha+1,\alpha+\beta+1,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})\Bigg)
+
γ
​
r
(
λ
+
τ
​
ε
)
2
​
(
B
⁡
(
α
+
2
,
β
)
B
⁡
(
α
,
β
)
​
F
1
2
​
(
2
,
α
+
2
,
α
+
β
+
2
,
−
(
λ
τ
+
ε
)
−
1
)
CLOSE
\displaystyle+\frac{\gamma r}{(\lambda+\tau\varepsilon)^{2}}\Bigg(\frac{B(\alpha+2,\beta)}{B(\alpha,\beta)}{}_{2}F_{1}(2,\alpha+2,\alpha+\beta+2,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})
OPEN
+
2
​
ε
​
B
⁡
(
α
+
1
,
β
)
B
⁡
(
α
,
β
)
​
F
1
2
​
(
2
,
α
+
1
,
α
+
β
+
1
,
−
(
λ
τ
+
ε
)
−
1
)
+
ε
2
​
F
1
2
​
(
2
,
α
,
α
+
β
,
−
(
λ
τ
+
ε
)
−
1
)
)
.
\displaystyle+2\varepsilon\frac{B(\alpha+1,\beta)}{B(\alpha,\beta)}{}_{2}F_{1}(2,\alpha+1,\alpha+\beta+1,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})+\varepsilon^{2}{}_{2}F_{1}(2,\alpha,\alpha+\beta,-(\frac{\lambda}{\tau}+\varepsilon)^{-1})\Bigg)\quad.
Solving the non-linear system in
Mai et al. [2019]
also requires computing
κ
\kappa
:
κ
\displaystyle\kappa
→
(
n
,
p
)
→
∞
r
​
𝔼
​
[
σ
λ
−
e
​
σ
]
\displaystyle\xrightarrow{(n,p)\rightarrow\infty}r\mathbb{E}\Big[\frac{\sigma}{\lambda-e\sigma}\Big]
=
r
​
𝔼
u
∼
ℬ
⁡
(
α
,
β
)
​
[
u
+
ε
λ
−
e
⁡
(
ε
+
u
)
]
\displaystyle=r\mathbb{E}_{u\sim\mathcal{B}(\alpha,\beta)}\Big[\frac{u+\varepsilon}{\lambda-e(\varepsilon+u)}\Big]
=
r
⁡
(
∫
0
1
u
λ
−
e
⁡
(
ε
+
u
)
​
u
α
−
1
​
(
1
−
u
)
β
−
1
B
⁡
(
α
,
β
)
​
𝑑
u
+
ε
​
∫
0
1
1
λ
−
e
⁡
(
ε
+
u
)
​
u
α
−
1
​
(
1
−
u
)
β
−
1
B
⁡
(
α
,
β
)
​
𝑑
u
)
\displaystyle=r\Bigg(\int_{0}^{1}\frac{u}{\lambda-e(\varepsilon+u)}\frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha,\beta)}du+\varepsilon\int_{0}^{1}\frac{1}{\lambda-e(\varepsilon+u)}\frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha,\beta)}du\Bigg)
=
r
B
​
(
α
,
β
)
​
(
λ
−
e
​
ε
)
​
(
∫
0
1
(
1
−
e
λ
−
e
​
ε
​
u
)
−
1
​
u
α
​
(
1
−
u
)
β
−
1
​
𝑑
u
+
ε
​
∫
0
1
(
1
−
e
λ
−
e
​
ε
​
u
)
−
1
​
u
α
−
1
​
(
1
−
u
)
β
−
1
​
𝑑
u
)
\displaystyle=\frac{r}{B(\alpha,\beta)(\lambda-e\varepsilon)}\Bigg(\int_{0}^{1}(1-\frac{e}{\lambda-e\varepsilon}u)^{-1}u^{\alpha}(1-u)^{\beta-1}du+\varepsilon\int_{0}^{1}(1-\frac{e}{\lambda-e\varepsilon}u)^{-1}u^{\alpha-1}(1-u)^{\beta-1}du\Bigg)
=
r
λ
−
e
​
ε
​
(
B
⁡
(
α
+
1
,
β
)
B
⁡
(
α
,
β
)
​
F
1
2
​
(
1
,
α
+
1
,
α
+
β
+
1
,
(
λ
e
−
ε
)
−
1
)
+
ε
⋅
F
1
2
​
(
1
,
α
,
α
+
β
,
(
λ
e
−
ε
)
−
1
)
)
.
\displaystyle=\frac{r}{\lambda-e\varepsilon}\Bigg(\frac{B(\alpha+1,\beta)}{B(\alpha,\beta)}{}_{2}F_{1}(1,\alpha+1,\alpha+\beta+1,(\frac{\lambda}{e}-\varepsilon)^{-1})+\varepsilon\cdot{}_{2}F_{1}(1,\alpha,\alpha+\beta,(\frac{\lambda}{e}-\varepsilon)^{-1})\Bigg)\quad.
We provide an efficient implementation of the non-linear system solver with our particular data model and functions to compute the resulting calibration and refinement errors at
github.com/eugeneberta/RefineThenCalibrate-Theory
.
Appendix D
Temperature scaling implementation and TS-refinement
For the logloss, the objective
ℒ
(
β
)
=
∑
(
x
,
y
)
∈
𝒟
−
y
⊤
log
(
softmax
(
β
log
(
f
(
x
)
)
)
\mathcal{L}(\beta)=\sum_{(x,y)\in\mathcal{D}}-y^{\top}\log(\softmax(\beta\log(f(x)))
is convex, which follows from the fact that
−
log
⁡
(
softmax
⁡
(
x
)
)
=
logsumexp
⁡
(
x
)
−
x
-\log(\softmax(x))=\logsumexp(x)-x
is convex
[
Boyd and Vandenberghe, 2004
]
.
Specifically, we use 30 bisection steps to approximate
b
∗
≔
argmin
b
∈
[
−
16
,
16
]
⁡
ℒ
⁡
(
exp
⁡
(
b
)
)
b^{*}\coloneqq\argmin_{b\in[-16,16]}\mathcal{L}(\exp(b))
and then find
β
∗
≔
exp
⁡
(
b
∗
)
\beta^{*}\coloneqq\exp(b^{*})
.
If even faster implementations are desired, more advanced line search for convex functions
[
Orseau and Hutter, 2023
]
, second-order methods, stochastic optimization, or warm-starting could be helpful.
To guard against overfitting in cases with 100% validation accuracy, where bisection can efficiently approach
β
∗
=
∞
\beta^{*}=\infty
, we introduce a form of Laplace smoothing (LS) as
g
⁡
(
p
)
≔
N
cal
N
cal
+
1
​
g
β
∗
​
(
p
)
+
1
N
cal
+
1
​
u
g(p)\coloneqq\frac{N_{\mathrm{cal}}}{N_{\mathrm{cal}}+1}g_{\beta^{*}}(p)+\frac{1}{N_{\mathrm{cal}}+1}u
,
where
u
u
is the uniform distribution and
N
cal
N_{\mathrm{cal}}
is the number of samples in the calibration set. This version is used for our main experiments except for
Figure
4
.
Extended comparison.
Figure
D.1
shows a comparison of more post-hoc calibration methods. While
Figure
4
uses mean logloss for simplicity, this can over-emphasize multi-class datasets while imbalanced datasets get less weight. To compensate for this, in
Figure
D.1
we divide the loss (logloss or Brier loss) for each dataset by the loss of the best constant predictor, which can be written as
e
ℓ
​
(
𝔼
​
[
Y
]
)
e_{\ell}(\mathbb{E}[Y])
.
Our inclusion of Laplace smoothing (LS) to TS brings a small benefit for logloss. We also compare our results to isotonic regression, where we include LS to avoid infinite logloss since IR can predict a probability of zero.
1
1
1
IVAP
[
Vovk et al., 2015
]
is a variant of isotonic regression that does not predict zero probabilities but we found it to be roughly two orders of magnitude slower than isotonic regression, so we did not consider it very attractive as a component of a refinement estimator.
While the IR implementation from scikit-learn
[
Pedregosa et al., 2011
]
is almost as fast as our TS implementation, it performs considerably worse on our benchmark. For Brier loss, the benefit of TS in general is less pronounced, and only good implementations improve results compared to no post-hoc calibration.
Figure D.1:
Runtime vs. mean benchmark scores of different TS implementations and isotonic regression for logloss (left) and Brier loss (right).
Runtimes are averaged over validation sets with at least 10K samples. The evaluation is on XGBoost models trained with default parameters, using the epoch with the best validation accuracy. The
y
y
-axis shows the mean of normalized logloss (left) or Brier loss (right), where normalizing means dividing by the loss
e
ℓ
​
(
𝔼
​
[
Y
]
)
e_{\ell}(\mathbb{E}[Y])
of the best constant predictor on each dataset.
Validation.
We are interested in minimizing the population risk of calibrated estimators. To faithfully estimate the population risk, it is possible to use cross-validation or the holdout method, fitting the calibrator on a part of the validation set while using its loss on the remaining part as a refinement estimate. However, we experimentally observe in
Figure
F.2
that fitting and evaluating temperature scaling on the entire validation set works equally well, perhaps because it only fits a single parameter. We use the latter approach in the following since it is more efficient compared to cross-validation.
Appendix E
Computer vision experiments
We train a ResNet-18
[
He et al., 2016
]
and WideResNet
[
Zagoruyko, 2016
]
on CIFAR-10, CIFAR-100 and SVHN datasets
[
Krizhevsky and Hinton, 2009
,
Netzer et al., 2011
]
. We train for 300 epochs using SGD with momentum
=
0.9
=0.9
, weight decay
=
10
−
4
=10^{-4}
and a learning rate scheduler that divides the learning rate by ten every 100 epochs. We use random cropping (
32
×
32
32\times 32
crops after paddind images by
4
4
pixels), horizontal flips (pytorch default) and cutout
[
DeVries, 2017
]
(one
16
×
16
16\times 16
hole per image during training). We train each model ten times on each dataset. 10% of the training set is kept for validation. We select the best epoch based on different metrics evaluated on the validation set: logloss, Brier score, accuracy and logloss after temperature scaling (TS-refinement). On
Table
E.1
(ResNet-18) and
Table
E.2
(WideResNet) we report average logloss, brier score, accuracy, ECE and smooth ECE
[
Błasiok and Nakkiran, 2024
]
obtained for each stopping metric.
Figure
1
is generated with the same training recipe with a cosine annealing scheduler instead to avoid big jumps in the loss landscape and no weight decay to exacerbate the effect of calibration overfitting. See
github.com/eugeneberta/RefineThenCalibrate-Vision
.
Table E.1:
Benchmark results for ResNet-18. We plot means obtained over the 10 runs and 95% confidence intervals computed using the t-distribution. Stopping metrics are evaluated on the validation set (10% of training data). All metrics are reported for the best model as selected by the corresponding stopping metric, after TS (fitted using the validation set).
Logloss
Brier
Accuracy
ECE
smECE
Dataset
Stopping metric
CIFAR-10
Logloss
0.161
0.161
±
0.004
\pm 0.004
0.080
0.080
±
0.002
\pm 0.002
94.6
%
94.6\%
±
0.2
\pm 0.2
0.006
\bf 0.006
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
Brier score
0.154
\bf 0.154
±
0.005
\pm 0.005
0.073
\bf 0.073
±
0.003
\pm 0.003
95.1
%
\bf 95.1\%
±
0.2
\pm 0.2
0.007
0.007
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
Accuracy
0.155
0.155
±
0.005
\pm 0.005
0.074
0.074
±
0.003
\pm 0.003
95.1
%
\bf 95.1\%
±
0.2
\pm 0.2
0.007
0.007
±
0.001
\pm 0.001
0.009
0.009
±
0.001
\pm 0.001
TS-refinement
0.154
\bf 0.154
±
0.005
\pm 0.005
0.074
0.074
±
0.003
\pm 0.003
95.1
%
\bf 95.1\%
±
0.2
\pm 0.2
0.007
0.007
±
0.002
\pm 0.002
0.008
\bf 0.008
±
0.001
\pm 0.001
CIFAR-100
Logloss
1.015
1.015
±
0.008
\pm 0.008
0.367
0.367
±
0.003
\pm 0.003
73.2
%
\bf 73.2\%
±
0.3
\pm 0.3
0.019
0.019
±
0.002
\pm 0.002
0.019
0.019
±
0.001
\pm 0.001
Brier score
1.014
1.014
±
0.007
\pm 0.007
0.367
0.367
±
0.002
\pm 0.002
73.1
%
73.1\%
±
0.3
\pm 0.3
0.020
0.020
±
0.002
\pm 0.002
0.019
0.019
±
0.001
\pm 0.001
Accuracy
1.001
1.001
±
0.012
\pm 0.012
0.366
\bf 0.366
±
0.003
\pm 0.003
73.1
%
73.1\%
±
0.3
\pm 0.3
0.018
0.018
±
0.001
\pm 0.001
0.018
0.018
±
0.001
\pm 0.001
TS-refinement
0.983
\bf 0.983
±
0.008
\pm 0.008
0.366
\bf 0.366
±
0.003
\pm 0.003
73.0
%
73.0\%
±
0.2
\pm 0.2
0.016
\bf 0.016
±
0.001
\pm 0.001
0.016
\bf 0.016
±
0.001
\pm 0.001
SVHN
Logloss
0.120
0.120
±
0.003
\pm 0.003
0.048
\bf 0.048
±
0.001
\pm 0.001
96.9
%
96.9\%
±
0.1
\pm 0.1
0.006
\bf 0.006
±
0.001
\pm 0.001
0.007
\bf 0.007
±
0.001
\pm 0.001
Brier score
0.118
\bf 0.118
±
0.002
\pm 0.002
0.048
\bf 0.048
±
0.001
\pm 0.001
97.0
%
\bf 97.0\%
±
0.1
\pm 0.1
0.006
\bf 0.006
±
0.001
\pm 0.001
0.007
\bf 0.007
±
0.001
\pm 0.001
Accuracy
0.124
0.124
±
0.005
\pm 0.005
0.049
0.049
±
0.002
\pm 0.002
96.9
%
96.9\%
±
0.1
\pm 0.1
0.006
\bf 0.006
±
0.001
\pm 0.001
0.008
0.008
±
0.001
\pm 0.001
TS-refinement
0.119
0.119
±
0.002
\pm 0.002
0.048
\bf 0.048
±
0.001
\pm 0.001
97.0
%
\bf 97.0\%
±
0.1
\pm 0.1
0.006
\bf 0.006
±
0.001
\pm 0.001
0.007
\bf 0.007
±
0.001
\pm 0.001
Table E.2:
Benchmark results for WideResNet. We plot means obtained over the 10 runs and 95% confidence intervals computed using the t-distribution. Stopping metrics are evaluated on the validation set (10% of training data). All metrics are reported for the best model as selected by the corresponding stopping metric, after TS (fitted using the validation set).
Logloss
Brier
Accuracy
ECE
smECE
Dataset
Stopping metric
CIFAR-10
Logloss
0.123
0.123
±
0.004
\pm 0.004
0.061
0.061
±
0.002
\pm 0.002
95.9
%
95.9\%
±
0.2
\pm 0.2
0.006
\bf 0.006
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.000
\pm 0.000
Brier score
0.121
0.121
±
0.002
\pm 0.002
0.056
\bf 0.056
±
0.001
\pm 0.001
96.4
%
\bf 96.4\%
±
0.1
\pm 0.1
0.006
\bf 0.006
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
Accuracy
0.122
0.122
±
0.002
\pm 0.002
0.056
\bf 0.056
±
0.001
\pm 0.001
96.4
%
\bf 96.4\%
±
0.1
\pm 0.1
0.006
\bf 0.006
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
TS-refinement
0.120
\bf 0.120
±
0.002
\pm 0.002
0.056
\bf 0.056
±
0.001
\pm 0.001
96.3
%
96.3\%
±
0.1
\pm 0.1
0.007
0.007
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
CIFAR-100
Logloss
0.798
0.798
±
0.007
\pm 0.007
0.300
0.300
±
0.002
\pm 0.002
78.4
%
78.4\%
±
0.3
\pm 0.3
0.020
0.020
±
0.002
\pm 0.002
0.020
0.020
±
0.002
\pm 0.002
Brier score
0.803
0.803
±
0.003
\pm 0.003
0.298
\bf 0.298
±
0.001
\pm 0.001
78.8
%
\bf 78.8\%
±
0.1
\pm 0.1
0.021
0.021
±
0.002
\pm 0.002
0.020
0.020
±
0.001
\pm 0.001
Accuracy
0.791
0.791
±
0.011
\pm 0.011
0.300
0.300
±
0.002
\pm 0.002
78.6
%
78.6\%
±
0.2
\pm 0.2
0.020
0.020
±
0.003
\pm 0.003
0.019
0.019
±
0.002
\pm 0.002
TS-refinement
0.771
\bf 0.771
±
0.004
\pm 0.004
0.298
\bf 0.298
±
0.002
\pm 0.002
78.5
%
78.5\%
±
0.2
\pm 0.2
0.016
\bf 0.016
±
0.002
\pm 0.002
0.016
\bf 0.016
±
0.001
\pm 0.001
SVHN
Logloss
0.109
\bf 0.109
±
0.002
\pm 0.002
0.043
0.043
±
0.001
\pm 0.001
97.3
%
\bf 97.3\%
±
0.1
\pm 0.1
0.007
\bf 0.007
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
Brier score
0.110
0.110
±
0.003
\pm 0.003
0.042
\bf 0.042
±
0.001
\pm 0.001
97.3
%
\bf 97.3\%
±
0.1
\pm 0.1
0.007
\bf 0.007
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
Accuracy
0.112
0.112
±
0.002
\pm 0.002
0.042
\bf 0.042
±
0.001
\pm 0.001
97.3
%
\bf 97.3\%
±
0.1
\pm 0.1
0.008
0.008
±
0.001
\pm 0.001
0.009
0.009
±
0.001
\pm 0.001
TS-refinement
0.109
\bf 0.109
±
0.001
\pm 0.001
0.042
\bf 0.042
±
0.000
\pm 0.000
97.3
%
\bf 97.3\%
±
0.1
\pm 0.1
0.007
\bf 0.007
±
0.001
\pm 0.001
0.008
\bf 0.008
±
0.001
\pm 0.001
Appendix F
Tabular experiments
In the following, we provide more details and analyses for our tabular experiments. The experiments took around 40 hours to run on a workstation with a 32-core AMD Threadripper PRO 3975WX CPU and four NVidia RTX 3090 GPUs. The benchmark code is available at
github.com/dholzmueller/pytabkit
.
F.1
Dataset size dependency
Figure
F.1
shows how the relative performance of refinement-based stopping vs logloss stopping depends on the dataset size. While the situation for small datasets is very noisy, for larger datasets the deterioration in the worst case is much less severe than the improvements in the best case. The advantages of TS-refinement become apparent at roughly 10K samples, which corresponds to a validation set size of 1,600. For XGB and MLP, there is one large outlier dataset where refinement-based stopping and logloss stopping both achieve low loss but the loss ratio is high.
Figure F.1:
Relative differences in logloss of using TS-Refinement vs. Logloss for selecting the best epoch and hyperparameters.
Each method applies temperature scaling on the final model. Each dot represents one dataset. Values below zero mean that TS-refinement performs better. A light color indicates datasets where methods achieve very low loss.
F.2
Other stopping metrics
In
Figure
F.2
, we show results for more stopping metrics like AUROC, Brier loss, Brier loss after temperature scaling, and a 5-fold cross-validation version of TS-Refinement from
Appendix
D
. TS-Refinement and its more expensive cross-validation version perform best. Out of the other metrics, Brier loss before or after temperature scaling performs comparably to logloss, while AUROC performs worse than logloss for RealMLP.
Figure
F.3
shows the same stopping metrics on the Brier loss instead. Here, stopping on Brier loss and refinement-based metrics perform well.
Figure F.2:
Relative differences in logloss for different stopping methods compared to Logloss+TS.
Brier-Ref. refers to Brier loss after temperature scaling. AUROC uses the one-vs-rest version for multiclass datasets. TS-Ref.-5CV is the metric from
Appendix
D
computing the out-of-fold loss after temperature scaling in a five-fold crossvalidation setup. Methods labeled “+TS” use temperature scaling on the final model. Each dot represents one dataset from
Ye et al. [2024]
, using only the 65 datasets with at least 10K samples. Percentages are clipped to
[
−
100,100
]
[-100,100]
. Box-plots show the 10%, 25%, 50%, 75%, and 90% quantiles.
Figure F.3:
Relative differences in
Brier loss
for different stopping methods compared to Logloss+TS.
Brier-Ref. refers to Brier loss after temperature scaling. AUROC uses the one-vs-rest version for multiclass datasets. TS-Ref.-5CV is the metric from
Appendix
D
computing the out-of-fold loss after temperature scaling in a five-fold crossvalidation setup. Methods labeled “+TS” use temperature scaling on the final model. Each dot represents one dataset from
Ye et al. [2024]
, using only the 65 datasets with at least 10K samples. Percentages are clipped to
[
−
100,100
]
[-100,100]
. Box-plots show the 10%, 25%, 50%, 75%, and 90% quantiles.
F.3
Effect on other metrics
Figure
F.4
shows that tuning TS-Refinement can, on average, improve downstream accuracy compared to tuning logloss, and sometimes even compared to tuning accuracy directly. The same holds for AUROC in
Figure
F.5
, where tuning accuracy often performs very badly. Performing temperature scaling does not affect downstream accuracy, but can affect downstream AUROC on multiclass datasets.
Figure F.4:
Differences in downstream
classification error
between logloss + TS and other procedures on tabular datasets.
Each dot represents one dataset from
Ye et al. [2024]
, using only the 65 datasets with at least 10K samples. Percentages are clipped to
[
−
100,100
]
[-100,100]
. Box-plots show the 10%, 25%, 50%, 75%, and 90% quantiles.
Figure F.5:
Differences in downstream
AUROC
(one-vs-rest for multiclass datasets) between logloss + TS and other procedures on tabular datasets.
Each dot represents one dataset from
Ye et al. [2024]
, using only the 65 datasets with at least 10K samples. Percentages are clipped to
[
−
100,100
]
[-100,100]
. Box-plots show the 10%, 25%, 50%, 75%, and 90% quantiles.
F.4
Stopping times
Figure
F.6
shows the best epochs or iterations found for different metrics for the models with default parameters. We can see several tendencies across models:
•
Logloss stops first on average.
•
Brier loss stops later than logloss, also when considering the loss after temperature scaling.
•
Loss after temperature scaling stopps later than loss before temperature scaling.
•
Accuracy stops late and AUROC somewhere in the middle.
(a)
RealMLP (default)
(b)
MLP (default)
(c)
XGBoost (default)
Figure F.6:
Best epochs/iterations in default models for different stopping metrics.
Each point represents one model trained on one of five training-validation splits on one of the 65 datasets with at least 10K samples. Brier-Ref. refers to Brier loss after temperature scaling. AUROC uses the one-vs-rest version for multiclass datasets. The multiple clusters in the RealMLP stopping epochs are likely due to the use of a multi-cycle loss schedule.
F.5
Methods
From a single training of a method, we extract results for the best epoch (for NNs) or iteration (for XGBoost) with respect to all considered metrics. To achieve this, we always train for the maximum number of epochs/iterations and do not stop the training early based on one of the metrics.
Default parameters.
For the MLP, we slightly simplify the default parameters of
Gorishniy et al. [2021]
as shown in
Table
F.3
. For XGBoost, we take the library default parameters. For RealMLP, we take the default parameters from
Holzmüller et al. [2024]
but deactivate label smoothing since it causes the loss to be non-proper.
Hyperparameter tuning.
For hyperparameter tuning, we employ 30 steps of random search, comparable to
McElfresh et al. [2024]
. Using random search allows us to train the 30 random models once and then pick the best one for each metric. For the MLP, we choose a small search space, shown in
Table
F.4
to cover the setting of a simple baseline. For XGBoost, we choose a typical, relatively large search space, shown in
Table
F.1
. For RealMLP, we slightly modify the original search space from
Holzmüller et al. [2024]
.
Table F.1:
Hyperparameter search space for XGBoost, adapted from
Grinsztajn et al. [2022]
. We use the
hist
method, which is the new default in XGBoost 2.0 and supports native handling of categorical values, while the old
auto
method selection is not available in XGBoost 2.0. We disable early stopping as we want to select the best epoch for different metrics in the same training run. Some search spaces are adapted based on previous experiences.
Hyperparameter
Distribution
tree_method
hist
n_estimators
1000
early_stopping_rounds
1000
max_depth
UniformInt[1, 11]
learning_rate
LogUniform[1e-3, 0.7]
subsample
Uniform[0.5, 1]
colsample_bytree
Uniform[0.5, 1]
colsample_bylevel
Uniform[0.5, 1]
min_child_weight
LogUniformInt[1e-5, 100]
alpha
LogUniform[1e-5, 5]
lambda
LogUniform[1e-5, 5]
gamma
LogUniform[1e-5, 5]
Table F.2:
Hyperparameter search space for RealMLP, adapted from
Holzmüller et al. [2024]
. Compared to the original search space, we make the option without label smoothing more likely since it optimizes a proper loss, and we insert a third option for weight decay.
Hyperparameter
Distribution
Num. embedding type
Choice([None, PBLD, PL, PLR])
Use scaling layer
Choice([True, False], p=[0.6, 0.4])
Learning rate
LogUniform([2e-2, 3e-1])
Dropout prob.
Choice([0.0, 0.15, 0.3], p=[0.3, 0.5, 0.2])
Activation fct.
Choice([ReLU, SELU, Mish])
Hidden layer sizes
Choice([[256, 256, 256], [64, 64, 64, 64, 64], [512]], p=[0.6, 0.2, 0.2])
Weight decay
Choice([0.0, 2e-3, 2e-2])
Num. emb. init std.
LogUniform([0.05, 0.5])
Label smoothing
ε
\varepsilon
Choice([0.0, 0.1])
Table F.3:
Default hyperparameters for MLP, adapted from
Gorishniy et al. [2021]
.
Hyperparameter
Distribution
Number of layers
4
Hidden size
256
Activation function
ReLU
Learning rate
1e-3
Dropout
0.0
Weight decay
0.0
Optimizer
AdamW
Preprocessing
Quantile transform + one-hot encoding
Batch size
256
Number of epochs
256
Learning rate schedule
constant
Table F.4:
Hyperparameter search space for MLP.
Hyperparameter
Distribution
Learning rate
LogUniform[1e-4, 1e-2]
Dropout
Choice([0.0, 0.1, 0.2, 0.3])
Weight decay
Choice([0.0, 1e-5, 1e-4, 1e-3])
F.6
Datasets
We take the datasets from
Ye et al. [2024]
and apply the following modifications:
•
Samples that contain missing values in numerical features are removed since not all methods natively support the handling of these values.
•
Datasets that contain less than 1K samples after the previous steps are removed. The following datasets are removed:
analcatdata_authorship
,
Pima_Indians_Diabetes_Database
,
vehicle
,
mice_protein_expression
, and
eucalyptus
. The latter two datasets contained samples with missing numerical features.
•
Datasets with more than 100K samples are subsampled to 100K samples.