---
title: 'TCE: A Test-Based Approach to Measuring Calibration Error'
id: tce-a-test-based-approach-to-measuring-calibration-error
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:27:56.563731Z'
updated: '2026-11-09T23:31:27.704247Z'
source: https://arxiv.org/html/2306.14343
source_domain: arxiv.org
fetched_at: '2026-11-09T23:27:56.563403Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'TCE (arXiv 2306.14343): hypothesis-test-based calibration error for binary
  classifiers, imbalance-robust scale, optimal binning; shows ECE/ACE misleading under
  imbalance; no LLM content.'
---

TCE: A Test-Based Approach to Measuring Calibration Error
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2306.14343v1 [stat.ML] 25 Jun 2023
TCE: A Test-Based Approach to Measuring Calibration Error
Takuo Matsubara
Affiliation:
The Alan Turing Institute
Affiliation:
Newcastle University
Niek Tax
Affiliation:
Meta Platforms, Inc.
Richard Mudd
Affiliation:
Meta Platforms, Inc.
Ido Guy
Affiliation:
Meta Platforms, Inc.
Abstract
This paper proposes a new metric to measure the calibration error of probabilistic binary classifiers, called
test-based calibration error
(TCE).
TCE incorporates a novel loss function based on a statistical test to examine the extent to which model predictions differ from probabilities estimated from data.
It offers (i) a clear interpretation, (ii) a consistent scale that is unaffected by class imbalance, and (iii) an enhanced visual representation with repect to the standard reliability diagram.
In addition, we introduce an optimality criterion for the binning procedure of calibration error metrics based on a minimal estimation error of the empirical probabilities.
We provide a novel computational algorithm for optimal bins under bin-size constraints.
We demonstrate properties of TCE through a range of experiments, including multiple real-world imbalanced datasets and ImageNet 1000.
1
Introduction
In recent years, it has become ubiquitous to deploy complex machine learning models in real-world production systems.
Many of these systems rely on probabilistic classifiers that predict the probability that some target outcome occurs.
For such systems, it is often crucial that their predictive probabilities are
well-calibrated
, meaning that the predictive probability accurately reflects the true frequency that the target outcome occurs.
In some contexts, failures to achieve calibration can lead to negative consequences.
In applications like medical diagnoses
[
Topol, 2019
]
and autonomous driving
[
Grigorescu et al., 2020
]
, associated risks are often assessed based on model predictions and the consequences of a misguided risk evaluation can be severe.
In online advertising auctions
[
Li et al., 2015
]
, it is common to incorporate a prediction of the probability of some outcome of interest (e.g., a click on an advert) when calculating an advertiser’s bid.
While a number of metrics—such as log-likelihood, user-specified scoring functions, and the area under the receiver operating characteristic (ROC) curve—are used to assess the quality of probabilistic classifiers, it is usually hard or even impossible to gauge whether predictions are well-calibrated from the values of these metrics.
For assessment of calibration, it is typically necessary to use a metric that measures
calibration error
, that is, a deviation between model predictions and probabilities of target occurrences estimated from data.
The importance of assessing calibration error has been long emphasised in machine learning
[
Nixon et al., 2019
,
Minderer et al., 2021
]
and in probabilistic forecasting more broadly
[
Dawid, 1982
,
Degroot and Fienberg, 1983
]
.
However, existing metrics of calibration error have several drawbacks that in certain scenarios can mean that their values do not appropriately reflect true calibration performance.
In particular, we will demonstrate that values of existing calibration error metrics have an inconsistent scale that is influenced by the target class proportion.
In applications such as fraud detection
[
Abdallah et al., 2016
,
Tax et al., 2021
]
and advertising conversion prediction
[
Yang and Zhai, 2022
]
, the prevalence, i.e., the proportion of instances belonging to the target class, is often very low.
This leads to situations where one may be unable to identify whether the values of calibration error metrics are small due to good calibration performance or due to the low prevalence.
This is also problematic for monitoring applications aimed at tracking the calibration performance of a model in a production system, where the prevalence can change over time (i.e.,
prior probability shift
[
Storkey et al., 2009
]
) and that makes it difficult to understand whether to attribute changes in the metric to an actual change in calibration performance or to the change in prevalence.
Furthermore,
binning
of model predictions—an essential component of most calibration error metrics
[
Naeini et al., 2015
]
—is often based on heuristics and lacks clear design principles.
For calibration error metrics, empirical probabilities of target occurrences are typically estimated by clustering data into several subsets based on binning of the associated model predictions.
The design of the binning scheme is a vital factor in the accurate estimation of the empirical probabilities, yet few principles guiding the design of binning schemes have emerged to date.
In this paper, we elaborate on the issues of existing calibration error metrics in
Section
2
.
We establish a simple yet novel metric that counterbalances the issues in
Section
3
.
Section
4
empirically demonstrates properties of the proposed metric by experiments based on various datasets.
Related works are discussed in
Section
5
, followed by the conclusion in
Section
6
.
This paper focuses on the methodological aspects of the proposed new metric for binary classification, while theoretical development is left for future research.
Our contributions are summarised as follows:
Contributions
•
Our primary contribution is a novel calibration error metric called
test-based calibration error
(TCE). TCE is based on statistical hypothesis testing and is interpretable as a percentage of model predictions that deviate significantly from estimated empirical probabilities. TCE produces values in a normalised, comparable range
[
0,100
]
[0,100]
regardless of the class prevalence.
•
We propose an explanatory visual representation of TCE called the
test-based reliability diagram
. It carries more information than the standard reliability diagram and facilitates a better understanding of calibration performance (See
Figure
1
).
•
We introduce an optimality criterion for bins under which optimal bins minimise an estimation error of the empirical probabilities. We then propose a novel algorithm to compute optimal bins approximately under the constraints of the minimum and maximum size of each bin.
2
Background
In this section, we introduce the definition of
calibration
and recap one of the most common
calibration error
metrics.
We then outline several critical challenges of existing calibration error metrics.
The basic notation used in this paper is introduced below.
Denote input and output spaces respectively by
𝒳
\mathcal{X}
and
𝒴
\mathcal{Y}
.
We focus on probabilistic binary classification, i.e.
𝒴
=
{
0
,
1
}
\mathcal{Y}=\{0,1\}
, in which a probabilistic classifier
P
θ
:
𝒳
→
[
0
,
1
]
P_{\theta}:\mathcal{X}\to[0,1]
models a conditional probability of
Y
=
1
Y=1
given an input
x
∈
𝒳
x\in\mathcal{X}
.
The data
𝒟
:=
{
x
i
,
y
i
}
i
=
1
N
\mathcal{D}:=\{x_{i},y_{i}\}_{i=1}^{N}
are assumed to be i.i.d. realisations from a random variable
(
X
,
Y
)
∼
ℙ
(X,Y)\sim\mathbb{P}
.
To simplify notation, for any data subset
𝒮
⊆
𝒟
\mathcal{S}\subseteq\mathcal{D}
, we denote by
𝒮
x
\mathcal{S}^{x}
a set of all inputs
x
x
in
𝒮
\mathcal{S}
and by
𝒮
y
\mathcal{S}^{y}
a set of all outputs
y
y
in
𝒮
\mathcal{S}
.
By “a set of bins” or simply “bins”, we mean a set of arbitrary disjoint intervals whose union is the unit interval
[
0
,
1
]
[0,1]
.
For example, a set
{
Δ
b
}
b
=
1
2
\{\Delta_{b}\}_{b=1}^{2}
of intervals
Δ
1
=
[
0.0
,
0.4
)
\Delta_{1}=[0.0,0.4)
and
Δ
2
=
[
0.4
,
1.0
]
\Delta_{2}=[0.4,1.0]
is a set of bins.
2.1
Calibration Error
A probabilistic classifier
P
θ
:
𝒳
→
[
0
,
1
]
P_{\theta}:\mathcal{X}\to[0,1]
is said to be
calibrated
[
Dawid, 1982
,
Bröcker, 2009
]
if
ℙ
⁡
(
Y
=
1
∣
P
θ
​
(
X
)
=
Q
)
=
Q
\displaystyle\mathbb{P}(Y=1\mid P_{\theta}(X)=Q)=Q
(1)
for all
Q
∈
[
0
,
1
]
Q\in[0,1]
s.t. the conditional probability is well-defined.
Informally, this criterion implies that the model prediction coincides with the actual probability of
Y
=
1
Y=1
for all inputs.
Any deviation between the actual probabilities and the model predictions in
eq.
1
is often referred to as
calibration error
, which quantifies to what degree the classifier
P
θ
P_{\theta}
is calibrated.
The empirical computation of such a deviation involves estimating conditional probability
ℙ
⁡
(
Y
=
1
|
P
θ
​
(
X
)
=
Q
)
\mathbb{P}(Y=1|P_{\theta}(X)=Q)
from data.
For given bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
, define disjoint subsets
{
𝒟
b
}
b
=
1
B
\{\mathcal{D}_{b}\}_{b=1}^{B}
of data
𝒟
\mathcal{D}
by
𝒟
b
:=
{
(
x
i
,
y
i
)
∈
𝒟
∣
P
θ
​
(
x
i
)
∈
Δ
b
}
.
\displaystyle\mathcal{D}_{b}:=\{(x_{i},y_{i})\in\mathcal{D}\mid P_{\theta}(x_{i})\in\Delta_{b}\}.
(2)
Simply put,
𝒟
b
\mathcal{D}_{b}
is a subset of data whose model predictions have similar values.
The conditional probability
ℙ
⁡
(
Y
=
1
∣
P
θ
​
(
X
)
=
Q
)
\mathbb{P}(Y=1\mid P_{\theta}(X)=Q)
for any
Q
∈
Δ
b
Q\in\Delta_{b}
can then be estimated by the empirical mean of the labels in subset
𝒟
b
\mathcal{D}_{b}
:
ℙ
⁡
(
Y
=
1
∣
P
θ
​
(
X
)
=
Q
)
≈
P
^
b
:=
1
N
b
​
∑
y
i
∈
𝒟
b
y
y
i
\displaystyle\mathbb{P}(Y=1\mid P_{\theta}(X)=Q)\approx\widehat{P}_{b}:=\frac{1}{N_{b}}\sum_{y_{i}\in\mathcal{D}_{b}^{y}}y_{i}
(3)
where we denote by
P
^
b
\widehat{P}_{b}
the estimated conditional probability in
𝒟
b
\mathcal{D}_{b}
and by
N
b
N_{b}
the sample size of
𝒟
b
\mathcal{D}_{b}
.
One of the most common metrics to measure calibration error is
expected calibration error
(ECE)
[
Naeini et al., 2015
]
.
ECE uses equispaced bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
over
[
0
,
1
]
[0,1]
for a given number
B
B
and measures an absolute difference between the averaged model predictions and the estimated conditional probability
P
^
b
\widehat{P}_{b}
within each data subset
𝒟
b
\mathcal{D}_{b}
.
The value of ECE is defined as
ECE
:=
∑
b
=
1
B
N
b
N
​
|
P
^
b
−
1
N
b
​
∑
x
i
∈
𝒟
b
x
P
θ
​
(
x
i
)
|
.
\displaystyle\text{ECE}:=\sum_{b=1}^{B}\frac{N_{b}}{N}\left|\widehat{P}_{b}-\frac{1}{N_{b}}\sum_{x_{i}\in\mathcal{D}_{b}^{x}}P_{\theta}(x_{i})\right|.
(4)
ECE has an associated practical visual representation known as the
reliability diagram
[
Degroot and Fienberg, 1983
,
Niculescu-Mizil and Caruana, 2005
]
, which aligns the averaged model prediction and the estimated conditional probability in each
𝒟
b
\mathcal{D}_{b}
(see Figure
1
).
The reliability diagram is a powerful tool to intuitively grasp the deviation between the model and the estimated probability in ECE.
2.2
Challenges in Calibration Error
Calibration error metrics, such as ECE, are widely used in real-world applications.
There nonetheless exist several challenges that may cause a misassessment of calibration.
These problems become evident especially when a distribution of model predictions
{
P
θ
​
(
x
i
)
}
i
=
1
N
\{P_{\theta}(x_{i})\}_{i=1}^{N}
is not well-dispersed.
This scenario often arises in imbalanced classification where model predictions tend to be severely skewed towards either
0
0
or
1
1
.
The following paragraphs illustrate challenges of existing calibration error metrics, which we aim to address.
Challenge 1 (Scale-Dependent Interpretation)
In most calibration error metrics, the deviation between the model prediction and the estimated probability
P
^
b
\widehat{P}_{b}
in each
𝒟
b
\mathcal{D}_{b}
is measured by the absolute difference as in
eq.
4
.
However, the use of the absolute difference can result in values that have an inconsistent scale influenced by the class prevalence.
To illustrate this problem, consider an estimated probability
P
^
b
\widehat{P}_{b}
and an averaged model prediction denoted
Q
¯
b
\overline{Q}_{b}
for some
b
b
in
eq.
4
.
If
P
^
b
=
0.50
\widehat{P}_{b}=0.50
and
Q
¯
b
=
0.49
\overline{Q}_{b}=0.49
, their absolute difference is
0.01
0.01
.
On the other hand, if
P
^
b
=
0.01
\widehat{P}_{b}=0.01
and
Q
¯
b
=
0.0001
\overline{Q}_{b}=0.0001
, their absolute difference is
0.0099
0.0099
.
Despite the comparison under the absolute difference suggesting that the probability
Q
¯
b
=
0.0001
\overline{Q}_{b}=0.0001
with respect to
P
^
b
=
0.01
\widehat{P}_{b}=0.01
in the latter case is better calibrated than in the former case, one may reasonably argue that the latter is not well-calibrated—or at least not comparable to the former—given the stark difference in the order of magnitude.
Similarly to this illustration, the values of existing calibration metrics built on the absolute difference can be proportionally small whenever the scales of
P
^
b
\widehat{P}_{b}
and
Q
¯
b
\overline{Q}_{b}
are small.
This issue makes it difficult to distinguish whether the metric values are low due to good calibration performance or due to the small scale of the probabilities as in imbalanced classification.
Challenge 2 (Lack of Normalised Range)
The range of values of calibration error metrics built on absolute differences is not normalised.
The range can vary depending on the choice of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
.
To illustrate this problem, consider a bin
Δ
b
\Delta_{b}
for some
b
b
.
If
Δ
b
=
[
0.4
,
0.6
]
\Delta_{b}=[0.4,0.6]
, the absolute difference between
P
^
b
\widehat{P}_{b}
and
Q
¯
b
\overline{Q}_{b}
falls into a range
[
0.0
,
0.6
]
[0.0,0.6]
because
P
^
b
\widehat{P}_{b}
is the estimated probability in
[
0.0
,
1.0
]
[0.0,1.0]
and the averaged model prediction
Q
¯
b
\overline{Q}_{b}
in the bin
Δ
b
\Delta_{b}
takes the value within
Δ
b
\Delta_{b}
.
Similarly, a different choice of bin
Δ
b
\Delta_{b}
leads to a different range of the absolute difference.
Consequently, the choice of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
impacts the range of the final value of calibration error metrics that are built on the absolute difference.
To assure rigorous comparability of the final value of a calibration error metric, it is desirable to establish a measurement of the deviation whose value has a fixed, normalised range independent of the choice of bins.
Challenge 3 (Arbitrary Choice of Bins)
An appropriate choice of bins is critical because it meaningfully impacts on final values of calibration error metrics.
Equispaced bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
over
[
0
,
1
]
[0,1]
for a given number
B
B
are one of the most common choices of bins in practice, as used in ECE.
However, equispaced bins can often cause a situation where a few particular bins contain the majority of the model predictions when they are not well-dispersed over
[
0
,
1
]
[0,1]
, as often happens in imbalanced classification.
If some bin
Δ
b
\Delta_{b}
contains the majority of model predictions, the corresponding estimated probability
P
^
b
\widehat{P}_{b}
coincides approximately with the empirical mean of all labels.
On the other hand, estimated probabilities of the bins other than
Δ
b
\Delta_{b}
become unreliable due to the small size of samples contained.
A potential solution to this problem is to use bins that adapt based on the dispersion of model predictions.
Nixon et al. [2019]
proposed
adaptive calibration error
(ACE) that computes the value of
eq.
4
using bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
based on
B
B
-quantiles of model predictions
{
P
θ
​
(
x
i
)
}
i
=
1
N
\{P_{\theta}(x_{i})\}_{i=1}^{N}
for given
B
B
.
However, questions remain regarding the optimal number
B
B
of bins and the appropriate quantile to use for each bin.
To the best of our knowledge, there is no established notion of what makes bins optimal, nor do clear design principles for bins exist.
3
Calibration Error Based on Test and Optimal Bins
We propose a new calibration error metric that offers a simple yet novel solution to the challenges outlined in
Section
2.2
.
First, in
Section
3.1
, we present a general formulation of calibration error metrics that encompasses most metrics used in practice.
This general formulation allows for a structured understanding of the design of calibration error metrics.
In
Section
3.2
, we derive from the general formulation a new calibration error metric, called TCE, which incorporates a loss based on a statistical test to compare model predictions with estimated empirical probabilities.
TCE produces a value that has a clear interpretation as a percentage of model predictions determined to deviate significantly from estimated empirical probabilities, which leads to a normalised range of possible values
[
0,100
]
[0,100]
regardless of the choice of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
.
In
Section
3.3
, we consider an optimal criterion of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
from the perspective of minimising an estimation error of the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
.
We then develop a practical regularisation approach that ensures a minimum and maximum sample size in each subset
𝒟
b
\mathcal{D}_{b}
.
3.1
General Calibration Error
The following definition presents an abstract formulation of calibration error metrics, which we call
general calibration error
(GCE) for terminological convenience.
Denote by
2
𝒟
2^{\mathcal{D}}
a power set of
𝒟
\mathcal{D}
, i.e. a space of all subsets of
𝒟
\mathcal{D}
and by
ℳ
\mathcal{M}
a space of all probabilistic classifiers below.
Definition 1
.
(GCE)
Let
L
:
2
𝒟
×
ℳ
→
ℝ
L:2^{\mathcal{D}}\times\mathcal{M}\to\mathbb{R}
be a loss of any probabilistic classifier evaluated for any data subset.
Let
ℬ
\mathcal{B}
be a set of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
that define data subsets
{
𝒟
b
}
b
=
1
B
\{\mathcal{D}_{b}\}_{b=1}^{B}
as in
eq.
2
.
Let
∥
⋅
∥
\|\cdot\|
be a norm of a
B
B
-dimensional vector space.
For a given probabilistic classifier
P
θ
:
𝒳
→
[
0
,
1
]
P_{\theta}:\mathcal{X}\to[0,1]
, define a scalar
GCE
b
∈
ℝ
\text{GCE}_{b}\in\mathbb{R}
for each
b
=
1
,
⋯
,
B
b=1,\cdots,B
by
GCE
b
:=
L
⁡
(
𝒟
b
,
P
θ
)
.
\displaystyle\text{GCE}_{b}:=L\left(\mathcal{D}_{b},P_{\theta}\right).
(5)
Then, GCE of the probabilistic classifier
P
θ
P_{\theta}
is defined by
GCE
=
‖
(
GCE
1
,
⋯
,
GCE
B
)
‖
.
\displaystyle\text{GCE}=\|(\text{GCE}_{1},\cdots,\text{GCE}_{B})\|.
(6)
This formulation translates the problem of designing a calibration error metric into a problem of choosing the tuple
(
L
,
ℬ
,
∥
⋅
∥
)
(L,\mathcal{B},\|\cdot\|)
.
Most existing calibration error metrics used in practice can be derived by selecting an appropriate tuple of the loss
L
L
, the bins
ℬ
\mathcal{B}
, and the norm
∥
⋅
∥
\|\cdot\|
in GCE.
See
Example
1
below for the case of ECE.
It is also immediate to show that ACE can be recovered from GCE.
Example 1
.
Let
ℬ
\mathcal{B}
be equispaced bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
over
[
0
,
1
]
[0,1]
, let
L
L
be
L
⁡
(
𝒟
b
,
P
θ
)
=
|
1
N
b
​
∑
y
∈
𝒟
b
y
y
−
1
N
b
​
∑
x
∈
𝒟
b
x
P
θ
​
(
x
)
|
L(\mathcal{D}_{b},P_{\theta})=|\frac{1}{N_{b}}\sum_{y\in\mathcal{D}_{b}^{y}}y-\frac{1}{N_{b}}\sum_{x\in\mathcal{D}_{b}^{x}}P_{\theta}(x)|
, and let
∥
⋅
∥
\|\cdot\|
be a weighted 1-norm
‖
v
‖
=
∑
b
=
1
B
N
b
N
×
|
v
b
|
\|v\|=\sum_{b=1}^{B}\frac{N_{b}}{N}\times|v_{b}|
.
The ECE corresponds to the GCE under this tuple.
We aim to choose the tuple
(
L
,
ℬ
,
∥
⋅
∥
)
(L,\mathcal{B},\|\cdot\|)
so that it addresses the aforementioned challenges in
Section
2.2
.
Section
3.2
addresses a loss
L
L
based on a statistical test and presents the resulting TCE.
Subsequently,
Section
3.3
addresses a choice of bins
ℬ
\mathcal{B}
that is obtained through optimisation to minimise an estimation error of the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
.
All norms
∥
⋅
∥
\|\cdot\|
are equivalent in finite dimensions, and hence we do not focus on any particular choice.
As with ECE, we use the weighted 1-norm
∥
⋅
∥
\|\cdot\|
in
Example
1
for TCE.
3.2
Test-based Calibration Errors
We present our main contribution, a new calibration error metric called TCE, that is derived from GCE by specifying a novel loss
L
L
based on a statistical test.
Our proposed loss
L
L
summarises the percentage of model predictions that deviate significantly from the empirical probabilities in each subset
𝒟
b
\mathcal{D}_{b}
.
We effectively test a null hypothesis “the probability of
Y
=
1
Y=1
is equal to
P
θ
​
(
x
)
P_{\theta}(x)
” at each
x
∈
𝒟
b
x
x\in\mathcal{D}_{b}^{x}
using the output data
𝒟
b
y
\mathcal{D}_{b}^{y}
.
A rigorous formulation of this loss
L
L
is provided below, combined with the definition of the TCE.
Note that the bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
and the norm
∥
⋅
∥
\|\cdot\|
of TCE are arbitrary, while the weighted 1-norm is our default choice of
∥
⋅
∥
\|\cdot\|
.
Definition 2
.
(TCE)
Given a statistical test and its significance level
α
∈
[
0
,
1
]
\alpha\in[0,1]
, let
R
R
be a function of any observed dataset of random variable
Y
∈
{
0
,
1
}
Y\in\{0,1\}
and any probability
Q
∈
[
0
,
1
]
Q\in[0,1]
, which returns
1
1
if a hypothesis
P
⁡
(
Y
=
1
)
=
Q
P(Y=1)=Q
is rejected based on the dataset and returns
0
0
otherwise.
In
Definition
1
, let
L
L
be an average rejection percentage s.t.
L
(
𝒟
b
,
P
θ
)
=
100
×
1
N
b
∑
x
∈
𝒟
b
x
R
(
𝒟
b
y
,
P
θ
(
x
)
)
.
\displaystyle L(\mathcal{D}_{b},P_{\theta})=100\times\frac{1}{N_{b}}\sum_{x\in\mathcal{D}_{b}^{x}}R\left(\mathcal{D}_{b}^{y},P_{\theta}(x)\right).
(7)
GCE in
Definition
1
is then called TCE.
In contrast to existing metrics that examine the difference between averaged model predictions and empirical probabilities in each bin, TCE examines each prediction
P
θ
​
(
x
)
P_{\theta}(x)
and summarises the rejection percentage in each bin.
The procedure of TCE can be intuitively interpreted as follows.
Remark 1
.
Informally speaking, TCE examines whether each model prediction
P
θ
​
(
x
)
P_{\theta}(x)
can be regarded as an outlier relative to the empirical probability of the corresponding data
𝒟
b
y
\mathcal{D}_{b}^{y}
, where the test in function
R
R
acts as a criterion for determining outliers.
The level of model-calibration is then measured by the rate of outliers produced by the model.
In this paper, we use the Binomial test as the
de facto
standard statistical test to define
R
R
in the TCE.
TCE based on other tests, including Bayesian testing approaches, is an open direction for future research.
Algorithm
1
summarises the computational procedure of TCE.
There are multiple advantages of TCE as follows.
Algorithm 1
Computation of TCE
data
𝒟
\mathcal{D}
, model
P
θ
P_{\theta}
, norm
∥
⋅
∥
\|\cdot\|
, bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
, function
R
R
based on a chosen test and significant level
a value
TCE
∈
ℝ
\text{TCE}\in\mathbb{R}
for
b
=
1
,
…
,
B
b=1,\dots,B
do
𝒟
b
←
{
(
x
i
,
y
i
)
∈
𝒟
∣
P
θ
​
(
x
i
)
∈
Δ
b
}
\mathcal{D}_{b}\leftarrow\{(x_{i},y_{i})\in\mathcal{D}\mid P_{\theta}(x_{i})\in\Delta_{b}\}
⊳
\triangleright
make subset
TCE
b
←
0
\text{TCE}_{b}\leftarrow 0
for
x
i
∈
𝒟
b
x
x_{i}\in\mathcal{D}_{b}^{x}
do
TCE
b
←
TCE
b
+
R
⁡
(
𝒟
b
y
,
P
θ
​
(
x
i
)
)
\text{TCE}_{b}\leftarrow\text{TCE}_{b}+R(\mathcal{D}_{b}^{y},P_{\theta}(x_{i}))
⊳
\triangleright
test each
end
for
TCE
b
←
100
/
N
b
×
TCE
b
\text{TCE}_{b}\leftarrow 100/N_{b}\times\text{TCE}_{b}
end
for
TCE
←
‖
(
TCE
1
,
…
,
TCE
B
)
‖
\text{TCE}\leftarrow\|(\text{TCE}_{1},\dots,\text{TCE}_{B})\|
Advantage 1 (Clear Interpretation)
The final value of TCE has a clear interpretation as a percentage of model predictions that are determined by the test of choice (here the Binomial test) to deviate significantly from estimated empirical probabilities.
Because the value is a percentage, the range of the value is normalised to
[
0,100
]
[0,100]
.
Figure 1
:
Comparison of two visual representations both applied for a gradient boosting model trained on the
abalone
dataset used in
Section
4.2
. (Left) A new visual representation, which we call the
test-based reliability diagram
. The central plot shows a violin plot of model predictions in each bin, whose estimated probability is presented by a red line. The bottom plot shows by grey bar the sample size of each bin and by red bar the percentage of model predictions that deviate significantly from the estimated probability in each bin. The right plot shows a histogram of all model predictions. (Right) The standard reliability diagram with the bin-size plot on the bottom and the histogram plot on the right added for comparison.
Advantage 2 (Consistent Scale)
The test evaluates the statistical deviation of data from a model prediction
P
θ
​
(
x
)
P_{\theta}(x)
adaptively and appropriately for each scale of
P
θ
​
(
x
)
P_{\theta}(x)
and data size
N
b
N_{b}
.
Informally, TCE is the number of relative outliers determined for each
P
θ
​
(
x
)
P_{\theta}(x)
adaptively.
This endows the value with a consistent scale robust to class imbalance.
Advantage 3 (Enhanced Visualisation)
TCE leads to a new visual representation that shows the distribution of model predictions, and the proportion of model predictions that deviate significantly from an empirical probability in each bin.
See
Figure
1
for the description and comparison with the standard reliability diagram.
Our interest is in the aggregated rejection percentage of all the tests performed, and so multiple testing corrections—e.g., the Bonferroni correction to offer a frequentist guarantee to control the familywise error rate—are not considered.
If all the null hypotheses were simultaneously true, TCE would simply coincide with the false positive rate which equals in expectation to type I error specified by the significant level of the test.
Full discussion on when and how adjustments for multiple hypotheses tests should be made may be found in
Bender and Lange [2001]
.
Given that TCE is based on a statistical testing procedure, it may be possible to apply ideas from power analysis to inform the desired sample size in each
𝒟
b
\mathcal{D}_{b}
.
Such analysis may also benefit the algorithm in the next subsection to compute optimal bins under the bin-size constraints, providing insights on what bin-size should be used as the constraints.
Finally, it is worth noting that TCE can be extended to multi-class classification.
The following remark presents one straightforward approach to the extension.
Remark 2
.
Any calibration error metric defined for binary classification can be extended to multi-class classification by considering classwise-calibration
[
Kull et al., 2019
, e.g.]
, where the calibration error metric is applied for one-vs-rest classification of each class independently.
A modification of TCE in multi-class classification settings can then be defined as an average of TCEs applied for one-vs-rest classification of each class.
3.3
Optimal Bins by Monotonic Regressor and Bin-Size Constraints
It is a fundamental challenge to establish a practical and theoretically sound mechanism to design bins used in calibration error metrics.
Ideally designed bins provides accurate probability estimates
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
from data
𝒟
\mathcal{D}
while keeping the size of each bin reasonable.
To this end, we propose a novel algorithm to compute bins that aim to minimise an estimation error of the probability estimates
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
under the constraint of the size of each bin.
Recently,
Dimitriadis et al. [2021]
pointed out that an existing quadratic programming algorithm, called pool-adjacent-violators algorithm (PAVA), can be directly applied to compute “optimal” bins in the context of obtaining a better reliability diagram.
The bins are designed in a manner that minimises the
Brier score
[
Brier, 1950
]
of resulting empirical probabilities by virtue of PAVA.
Forging ahead with this observation, we introduce the following definition that makes explicit in what sense bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
can be considered optimal given an arbitrary estimation error
D
\mathrm{D}
of the probability estimates
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
from data
𝒟
\mathcal{D}
.
Definition 3
.
(Optimal Bins)
Let
Π
\Pi
be a space of all sets of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
for any
B
B
, with associated data subsets denoted by
{
𝒟
b
}
b
=
1
B
\{\mathcal{D}_{b}\}_{b=1}^{B}
and probability estimates from
{
𝒟
b
y
}
b
=
1
B
\{\mathcal{D}_{b}^{y}\}_{b=1}^{B}
denoted by
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
.
Let
D
\mathrm{D}
be any error function between an observed dataset of random variable
Y
∈
{
0
,
1
}
Y\in\{0,1\}
and a given probability
Q
∈
[
0
,
1
]
Q\in[0,1]
.
Any set of bins that satisfies
min
⁡
∑
b
=
1
B
{
Δ
b
}
b
=
1
B
∈
Π
⁡
W
b
×
D
⁡
(
𝒟
b
y
,
P
^
b
)
\displaystyle\min_{\{\Delta_{b}\}_{b=1}^{B}\in\Pi}\penalty\ \sum_{b=1}^{B}W_{b}\times\mathrm{D}(\mathcal{D}_{b}^{y},\widehat{P}_{b})
subject to
​
P
^
1
≤
⋯
≤
P
^
B
\displaystyle\hskip 100.0pt\text{\emph{subject to}}\penalty\ \widehat{P}_{1}\leq\dots\leq\widehat{P}_{B}
(8)
can be considered an optimal set of bins under the estimation error
D
\mathrm{D}
, where
W
b
:=
N
b
/
N
W_{b}:=N_{b}/N
is the weight associated with the error of subset
𝒟
b
y
\mathcal{D}_{b}^{y}
of size
N
b
N_{b}
.
The monotonic constraint
P
^
1
≤
⋯
≤
P
^
B
\widehat{P}_{1}\leq\cdots\leq\widehat{P}_{B}
of the probability estimates
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
is a natural requirement because the choice of bins becomes trivial otherwise.
For example, consider bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
with
B
=
N
B=N
such that
Δ
b
\Delta_{b}
contains one single point
y
b
y_{b}
and the probability estimate
P
^
b
=
y
b
\widehat{P}_{b}=y_{b}
for each
b
b
.
This clearly achieves that
∑
b
=
1
B
W
b
×
D
⁡
(
𝒟
b
y
,
P
^
b
)
=
1
N
​
∑
b
=
1
N
D
⁡
(
{
y
b
}
,
y
b
)
=
0
\sum_{b=1}^{B}W_{b}\times\mathrm{D}(\mathcal{D}_{b}^{y},\widehat{P}_{b})=\frac{1}{N}\sum_{b=1}^{N}\mathrm{D}(\{y_{b}\},y_{b})=0
.
Under the monotonic constraint, the choice of bins becomes non-trivial.
Under some choices of the estimation error
D
\mathrm{D}
, the optimisation of
eq.
8
can be solved as a monotonic regression problem.
Given an ordered dataset
{
y
i
}
i
=
1
N
\{y_{i}\}_{i=1}^{N}
, a monotonic regression algorithm finds
N
N
monotonically increasing values
y
^
1
≤
⋯
≤
y
^
N
\widehat{y}_{1}\leq\cdots\leq\widehat{y}_{N}
that minimise some loss between
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
and
{
y
i
}
i
=
1
N
\{y_{i}\}_{i=1}^{N}
.
There exist algorithms for various losses, including the
l
p
l_{p}
loss, the Huber loss, and the Chebyshev loss
[
de Leeuw et al., 2009
]
.
PAVA solves a monotonic regression problem under the squared error
∑
i
=
1
N
(
y
^
i
−
y
i
)
2
\sum_{i=1}^{N}(\widehat{y}_{i}-y_{i})^{2}
.
If we choose the error
D
\mathrm{D}
as the variance of each
𝒟
b
y
\mathcal{D}_{b}^{y}
, i.e.,
D
⁡
(
𝒟
b
y
,
P
^
b
)
=
1
N
b
​
∑
i
=
1
N
b
(
y
i
−
P
^
b
)
2
\displaystyle\mathrm{D}(\mathcal{D}_{b}^{y},\widehat{P}_{b})=\frac{1}{N_{b}}\sum_{i=1}^{N_{b}}(y_{i}-\widehat{P}_{b})^{2}
(9)
the optimal set of bins under
D
\mathrm{D}
can be obtained using PAVA, which corresponds to the case of
Dimitriadis et al. [2021]
.
See
Appendix
A
for the proof that the optimisation criterion of
eq.
8
is indeed minimised at bins obtained using PAVA.
The approach using PAVA is a highly appealing solution to the design of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
because it achieves a fully-automated design of the bins based on the clear criterion of
eq.
8
.
However, such a fully-automated design can occasionally generate a bin that contains an excessively small or large number of data for the sake of minimising the aggregated estimation error over all
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
.
Imposing a certain regularisation on the minimum and maximum size of each
𝒟
b
\mathcal{D}_{b}
can aid in keeping some baseline quality of the estimation of each individual
P
^
b
\widehat{P}_{b}
.
Algorithm 2
PAVA-BC (PAVA with Block Constraints)
ordered scalars
{
y
i
}
i
=
1
N
\{y_{i}\}_{i=1}^{N}
, size constraints
N
min
N_{\text{min}}
and
N
max
N_{\text{max}}
s.t.
0
≤
N
min
≤
N
max
≤
N
0\leq N_{\text{min}}\leq N_{\text{max}}\leq N
.
sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
B
←
0
B\leftarrow 0
for
i
=
1
,
…
,
N
−
N
m
​
i
​
n
i=1,\dots,N-N_{min}
do
B
←
B
+
1
B\leftarrow B+1
Y
B
←
y
i
Y_{B}\leftarrow y_{i}
W
B
←
1
W_{B}\leftarrow 1
while
B
>
1
B>1
do
if
W
B
−
1
+
W
B
>
N
m
​
i
​
n
W_{B-1}+W_{B}>N_{min}
then
If
W
B
−
1
+
W
B
>
N
m
​
a
​
x
W_{B-1}+W_{B}>N_{max}
then
Break
If
Y
B
−
1
/
W
B
−
1
<
Y
B
/
W
B
Y_{B-1}/W_{B-1}<Y_{B}/W_{B}
then
Break
end
if
Y
B
−
1
←
Y
B
−
1
+
Y
B
Y_{B-1}\leftarrow Y_{B-1}+Y_{B}
W
B
−
1
←
W
B
−
1
+
W
B
W_{B-1}\leftarrow W_{B-1}+W_{B}
B
←
B
−
1
B\leftarrow B-1
end
while
end
for
if
W
B
+
N
m
​
i
​
n
≤
N
m
​
a
​
x
W_{B}+N_{min}\leq N_{max}
then
Y
B
←
Y
B
+
∑
i
=
N
−
N
min
+
1
N
y
i
Y_{B}\leftarrow Y_{B}+\sum_{i=N-N_{\text{min}+1}}^{N}y_{i}
W
B
←
W
B
+
N
m
​
i
​
n
W_{B}\leftarrow W_{B}+N_{min}
else
B
←
B
+
1
B\leftarrow B+1
Y
B
←
∑
i
=
N
−
N
min
+
1
N
y
i
Y_{B}\leftarrow\sum_{i=N-N_{\text{min}}+1}^{N}y_{i}
W
B
←
N
m
​
i
​
n
W_{B}\leftarrow N_{min}
end
if
s
←
0
s\leftarrow 0
for
j
=
1
,
…
,
B
j=1,\dots,B
do
for
k
=
1
,
…
,
W
j
k=1,\dots,W_{j}
do
y
^
s
+
k
←
Y
j
/
W
j
\widehat{y}_{s+k}\leftarrow Y_{j}/W_{j}
end
for
s
←
s
+
W
j
s\leftarrow s+W_{j}
end
for
Algorithm 3
Near-Optimal Bins Based on PAVA-BC
data
𝒟
\mathcal{D}
, model
P
θ
P_{\theta}
, size constraints
N
min
N_{\text{min}}
and
N
max
N_{\text{max}}
s.t.
0
≤
N
min
≤
N
max
≤
N
0\leq N_{\text{min}}\leq N_{\text{max}}\leq N
.
a set of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
{
y
i
}
i
=
1
N
←
Sort
​
(
𝒟
,
P
θ
)
\{y_{i}\}_{i=1}^{N}\leftarrow\text{Sort}(\mathcal{D},P_{\theta})
{
y
^
i
}
i
=
1
N
←
PAVA-BC
​
(
{
y
i
}
i
=
1
N
,
N
min
,
N
max
)
\{\widehat{y}_{i}\}_{i=1}^{N}\leftarrow\text{PAVA-BC}(\{y_{i}\}_{i=1}^{N},N_{\text{min}},N_{\text{max}})
B
←
1
B\leftarrow 1
L
←
0
L\leftarrow 0
R
←
0
R\leftarrow 0
for
i
=
2
,
…
,
N
i=2,\dots,N
do
if
y
^
i
−
1
≠
y
^
i
\widehat{y}_{i-1}\neq\widehat{y}_{i}
then
R
←
(
P
θ
​
(
x
i
−
1
)
+
P
θ
​
(
x
i
)
)
/
2
R\leftarrow(P_{\theta}(x_{i-1})+P_{\theta}(x_{i}))/2
Δ
B
←
[
L
,
R
)
\Delta_{B}\leftarrow[L,R)
L
←
R
L\leftarrow R
B
←
B
+
1
B\leftarrow B+1
end
if
end
for
Δ
B
←
[
L
,
1.0
]
\Delta_{B}\leftarrow[L,1.0]
Therefore, we propose a modified version of PAVA that regularises based on the given minimum and maximum size of each subset
𝒟
b
y
\mathcal{D}_{b}^{y}
.
Algorithm
2
summarises the full algorithm, which we call
PAVA with block constraints
(PAVA-BC), followed by
Algorithm
3
that summarises how to compute bins using PAVA-BC accordingly, where
Sort
​
(
𝒟
,
P
θ
)
\text{Sort}(\mathcal{D},P_{\theta})
in
Algorithm
3
denotes any algorithm that sorts labels
{
y
i
}
i
=
1
N
\{y_{i}\}_{i=1}^{N}
in acending order of model predictions
{
P
θ
​
(
x
i
)
}
i
=
1
N
\{P_{\theta}(x_{i})\}_{i=1}^{N}
.
By
Algorithm
3
, we can obtain bins that satisfy the given minimum and maximum size constraints
N
min
N_{\text{min}}
and
N
max
N_{\text{max}}
in each
𝒟
b
\mathcal{D}_{b}
, while benefitting from the automated design of bins by PAVA.
A set of bins based on PAVA can be recovered by replacing PAVA-BC with PAVA in
Algorithm
3
.
In general, the introduction of the regularisation can cause mild violation of the monotonicity
P
^
1
≤
⋯
≤
P
^
B
\widehat{P}_{1}\leq\cdots\leq\widehat{P}_{B}
, meaning that there may exist a few values
P
^
b
\widehat{P}_{b}
that is smaller than
P
^
b
−
1
\widehat{P}_{b-1}
.
See
Appendix
B
for each example where mild violation of the monotonicity by PAVA-BC occured and did not occur.
In practice, mild violation of the monotonicity can often be a reasonable cost to achieve better properties of bins.
For example,
Tibshirani et al. [2011]
studied settings where the monotonicity is only “nearly" satisfied.
See
Figure
2
for a comparison of the bins computed by three different approaches: PAVA, PAVA-BC, and binning based on
10
10
-quantiles.
The bins produced by PAVA-BC interpolate between the optimal bins produced by PAVA and the well-sized bins produced by binning based on quantiles.
This is further confirmed by
Table
1
which shows the total estimation error in
eq.
8
and the estimation error within each bin in
eq.
9
for each approach.
The total estimation error is minimised by PAVA, while an average of the estimation error within each bin is minimised by binning based on quantiles.
In contrast, PAVA-BC takes a balance between the total and individual estimation error.
Figure 2
:
Comparison of bins for a random forest model on the
satimage
dataset used in
Section
4.2
based on (top) PAVA, (middle) PAVA-BC, (bottom) binning based on
10
10
-quantiles. The dotted line represents the boundary of each bin and the grey bar represents the size of each bin.
Table 1
:
The total estimation error and an average of the estimation error within each bin for the bins in
Figure
2
.
PAVA
PAVA-BC
Quantile
Total Error
0.040
0.042
0.048
Averaged Within-Bin Error
0.132
0.077
0.047
4
Empirical Evaluation
In this section, we demonstrate the properties of TCE via three experiments.
The first experiment uses synthetic data to examine the properties of TCE under controlled class imbalance.
The second experiment involves ten real-world datasets from the University of California Irvine (UCI) machine learning repository
[
Dua and Graff, 2017
]
, where nine are designed as benchmark tasks of imbalanced classification, and one is a well-balanced classification task for comparison.
In the second experiment, we also demonstrate that ECE and ACE may produce misleading assessments of calibration performance under class imbalance.
TCE has the potential to reduce such misinterpretation risks.
The final experiment uses the ImageNet1000 dataset to illustrate that TCE is applicable to large-scale settings.
In all experiments, models are fitted to training data first and any calibration error metric are computed using validation data.
Source code to reproduce the experiments is available in
https://github.com/facebookresearch/tce
.
We compute TCE with bins based on PAVA-BC unless otherwise stated.
The minimum and maximum size of each bin for PAVA-BC are set to
N
/
20
N/20
and
N
/
5
N/5
for a given dataset size
N
N
.
Under these constraints, the number of bins based on PAVA-BC falls into a range between 5 and 20.
In addition to ECE and ACE, we include the maximum calibration error (MCE)
[
Naeini et al., 2015
]
for comparison.
MCE is defined by replacing the weighted 1-norm with the supremum norm over
b
=
1
,
…
,
B
b=1,\dots,B
in
Example
1
.
We denote, by TCE(Q) and MCE(Q), TCE and MCE each with bins based on
B
B
-quantiles.
For all metrics,
B
B
-equispaced bins and
B
B
-quantiles bins are computed with
B
=
10
B=10
.
4.1
Synthetic Data with Controlled Class Imbalance
We first examine TCE using synthetic data from a simulation model considered in
Vaicenavicius et al. [2019]
.
The data are simulated from a Gaussian discriminant analysis model
(
x
,
y
)
∼
P
⁡
(
x
∣
y
)
​
P
​
(
y
)
(x,y)\sim P(x\mid y)P(y)
.
The output
y
∈
{
0
,
1
}
y\in\{0,1\}
is first sampled from a Bernoulli distribution
P
⁡
(
y
)
P(y)
with parameter
π
\pi
and the input
x
∈
ℝ
x\in\mathbb{R}
is then sampled from a Gaussian distribution
P
⁡
(
x
∣
y
)
=
𝒩
⁡
(
m
y
,
s
y
)
P(x\mid y)=\mathcal{N}(m_{y},s_{y})
with mean
m
y
m_{y}
and scale
s
y
s_{y}
dependent of
y
y
.
We set
m
y
=
(
2
×
y
−
1
)
m_{y}=(2\times y-1)
and
s
y
=
2
s_{y}=2
, and change the parameter
π
\pi
for each setting below.
By Bayes’ theorem, the conditional probability of
y
y
given
x
x
corresponds to a logistic model:
P
⁡
(
y
∣
x
)
=
1
/
(
1
+
exp
⁡
(
β
0
+
β
1
×
x
)
)
P(y\mid x)=1/(1+\exp(\beta_{0}+\beta_{1}\times x))
where
β
0
=
log
⁡
(
π
/
(
1
−
π
)
)
\beta_{0}=\log(\pi/(1-\pi))
and
β
1
=
4
\beta_{1}=4
.
A logistic model is therefore capable of reproducing the probability
P
⁡
(
y
∣
x
)
P(y\mid x)
of this synthetic data perfectly.
We consider two baseline cases of (i) well-balanced classification and (ii) imbalanced classification in this experiment.
We train a logistic model for the training data simulated with the parameter
π
=
0.5
\pi=0.5
(i.e. 50% prevalence) in case (i) and with
π
=
0.01
\pi=0.01
(i.e. 1% prevalence) in case (ii).
In each case (i) and (ii), we generate three different test datasets to create situations where the trained model is (a) well-calibrated, (b) over-calibrated, and (c) under-calibrated.
We examine the performance of TCE under these senarios.
Test datasets for senarios (a), (b), and (c) are generated from the simulation model with prevalences
50
%
50\%
,
40
%
40\%
, and
60
%
60\%
in case (i) and with prevalences
1
%
1\%
,
0
%
0\%
, and
2
%
2\%
in case (ii).
We generate 20000 data points in total, of which 70% are training data and 30% are test data.
Table
2
shows the values of four calibration error metrics applied to the logistic regression model in each scenario.
Table
2
demonstrates that all values of ECE and ACE in imbalanced case (ii) can be smaller than—or very close to—values for well-calibrated senario (a) in well-balanced case (i).
For example, the ECE value for case (ii)-(b) was smaller than that for case (i)-(a).
In contrast, TCE provides values with a consistent scale in both well-balanced and imbalanced cases.
More simulation studies of TCE with different hyperparameters are presented in
Section
C.1
.
Table 2
:
Comparison of four calibration error metrics under senarios (a) - (c) in each case (i) and (ii).
Prevalence
TCE
TCE(Q)
ECE
ACE
50% vs 50%
7.28%
10.88%
0.0138
0.0150
50% vs 40%
96.10%
96.47%
0.0963
0.0951
50% vs 60%
98.83%
98.93%
0.1097
0.1096
1% vs 1%
3.40%
0.18%
0.0017
0.0031
1% vs 0%
95.50%
68.73%
0.0094
0.0094
1% vs 2%
92.32%
89.73%
0.0139
0.0139
4.2
Imbalanced UCI Datasets
Next, we compare calibration error metrics using real-world datasets in the regime of severe class imbalance.
We use nine UCI datasets that were preprocessed by
Lemaître et al. [2017]
as benchmark tasks of imbalanced classification.
We also use one additional UCI dataset with a well-balanced prevalence for comparison.
For each dataset, 70% of samples are used as training data and 30% of samples are kept as validation data.
We train five different algorithms: logistic regression (LR), support vector machine (SVM), random forest (RF), gradient boosting (GB), and multi-layer perceptron (MLP).
We evaluate the calibration performance of each model by five different calibration error metrics in the following tables.
Tables
3
and
4
show results for the imbalanced datasets,
abalone
and
webpage
[
Dua and Graff, 2017
]
, respectively.
Results for all the other datasets are presented in
Section
C.2
.
In
Table
3
, the best model ranked by TCE and ACE agree with each other while ECE identifies RF as the best model.
It can be observed from the reliability diagram of ECE for both the datasets in
Section
C.2
that a large majority of model predictions are contained in a single bin of ECE.
In such cases, ECE becomes essentially equivalent to a comparison of global averages of all labels and all model predictions.
Table
4
demonstrates a situation where ECE and ACE risk misleading assessments of calibration performance.
Several values of ECE and ACE are all sufficiently small in
Table
4
, by which one may conclude that it is reasonable to use a model with the smallest calibration error.
However, the values of TCE indicate that no model has a good calibration performance.
In fact, relatively large statistical deviations between model predictions and empirical probabilities can be observed from the test-based reliability diagram for the webpage dataset in
Section
C.2
.
Table 3
:
Comparison of five calibration error metrics for five different algorithms trained on the abalone dataset.
TCE
ECE
ACE
MCE
MCE(Q)
LR
7.26%
0.0140
0.0252
0.0946
0.0851
SVM
47.21%
0.0436
0.0473
0.8302
0.1170
RF
33.89%
0.0127
0.0177
0.0670
0.0547
GB
4.86%
0.0182
0.0160
0.2965
0.0418
MLP
3.83%
0.0167
0.0122
0.0806
0.0540
Table 4
:
Comparison of five calibration error metrics for five different algorithms trained on the webpage dataset.
TCE
ECE
ACE
MCE
MCE(Q)
LR
40.16%
0.0044
0.0034
0.3134
0.0214
SVM
59.83%
0.0043
0.0057
0.5402
0.0239
RF
99.66%
0.0234
0.0241
0.5980
0.1189
GB
71.12%
0.0086
0.0107
0.2399
0.0436
MLP
49.81%
0.0090
0.0018
0.4344
0.0076
4.3
K-vs-Rest on ImageNet1000
Finally, we demonstrate that TCE is applicable for a large-scale binary classification task using ImageNet1000 data.
We consider a K-vs-rest classification problem by using a set of all dog-kind classes (from class 150 to class 275) as a positive class and the rest as a negative class.
Under this setting, 12.5% of validation samples belong to the positive class.
We used 5 different trained models: AlexNet, VGG19, ResNet18, ResNet50, and ResNet152.
Their calibration errors were measured based on the ImageNet1000 validation dataset consisting of 50000 data points.
Table
5
demonstrates that TCE produces interpretable values, with model rankings that largely agree with other metrics in this setting.
The last row of
Table
5
shows the average computational time of each metric.
Computation of all the procedures in TCE required only 71.78 seconds for 50000 data points with 1 CPU on average.
The reliability diagrams corresponding to the results are presented in
Section
C.3
.
Table 5
:
Comparison of five calibration error metrics for five different deep learning models on ImageNet1000 data.
TCE
ECE
ACE
MCE
MCE(Q)
AlexNet
42.74%
0.0070
0.0070
0.1496
0.0528
VGG19
23.57%
0.0028
0.0028
0.2148
0.0247
Res18
29.93%
0.0042
0.0042
0.2368
0.0350
Res50
24.60%
0.0020
0.0018
0.1911
0.0152
Res152
16.09%
0.0012
0.0013
0.1882
0.0102
Time (s)
71.78
0.4873
0.4221
0.0046
0.0063
5
Related Work
Several calibration error metrics have been proposed, including the aforementioned ECE.
MCE is a widely used variant of ECE that replaces the summation over
b
=
1
,
…
,
B
b=1,\dots,B
in (
4
) with the supremum over
b
=
1
,
…
,
B
b=1,\dots,B
.
[
Kumar et al., 2019
]
introduce a more general
l
p
l_{p}
calibration error, which includes both ECE and MCE.
ACE replaces the equispaced bins in ECE with bins designed based on quantiles of model predictions, which prevents high concentration of data in one bin when data is imbalanced
[
Nixon et al., 2019
]
.
These calibration error metrics can be extended to multi-class classification
[
Kumar et al., 2019
]
.
Other than calibration error, scoring functions
[
Gneiting et al., 2007
]
are commonly used measurements to evaluate a probabilistic classifier.
[
Wallace and Dahabreh, 2014
]
reported a limitation of the Brier score for imbalanced classification, and proposed the
stratified
Brier score that aggregates multiple Brier scores.
This paper designed a new calibration error metric based on a statistical test.
While statistical tests have been used in the context of calibration, we are the first to incorporate a statistical test into the design of a calibration error metric.
Vaicenavicius et al. [2019]
performed a statistical test on whether ECE computed for synthetic data generated from predictive probabilities is significantly different from ECE computed for actual data.
Similarly,
Widmann et al. [2019]
proposed a statistical test of the value of their calibration error metric built on kernel methods.
In contrast to existing works which considered a test for final values of calibration error metrics, our approach incorporates a test into the metric itself.
While the use of binning is vital in the vast majority of calibration metrics, there are a few works on the
binning-free
design of calibration error metrics.
The main idea is to use an cumulative distribution function (CDF) of predictive probabilities, which can be estimated without binning, and evaluate how significantly it differs from an ideal CDF that occurs if the predictive probabilities are all well-calibrated.
For example,
Gupta et al. [2021]
and
Arrieta-Ibarra et al. [2022]
considered the Kolmogorov-Smirnov test for the empirical CDF, where
Gupta et al. [2021]
further proposed a spline interpolation to obtain a continuous approximation of the CDF.
An approach proposed by
Kull et al. [2017]
can also be regarded as binning-free.
It uses a continuous CDF of the beta distribution produced by their calibration method, mentioned below, rather than the empirical CDF.
Calibration methods
refer to algorithms used to improve the calibration performance of a model
P
θ
P_{\theta}
.
Usually, they learn some ‘post-hoc’ function
φ
:
[
0
,
1
]
→
[
0
,
1
]
\varphi:[0,1]\to[0,1]
to be applied to each model predictio so that the new prediction
φ
​
(
P
θ
​
(
x
)
)
\varphi(P_{\theta}(x))
is better calibrated.
Various calibration algorithms have been proposed in parallel to the development of calibration error metrics.
Platt scaling uses a logistic function for the post-hoc function
φ
\varphi
[
Platt, 1999
]
.
Alternatively,
Kull et al. [2017]
,
Kull et al. [2019]
proposed to use a beta distribution in binary classification and a Dirichlet distribution in multi-class classification.
Isotonic regression is a powerful non-parametric approach to find a monotonically increasing function
φ
\varphi
that minimises the Brier score
[
Zadrozny and Elkan, 2002
]
.
Finally, Bayesian Binning into Quantiles by
Naeini et al. [2015]
extends a classical histogram-based calibration
[
Zadrozny and Elkan, 2001
]
to an ensemble of histogram-based calibrations based on Bayesian model averaging.
6
Conclusion
In this paper, we proposed a new calibration error metric TCE that incorporates a novel loss function based on a statistical test.
TCE has (i) a clear interpretation as a percentage of model predictions determined to deviate significantly from estimated empirical probabilities, (ii) a consistent scale that is robust to class imbalance, and (iii) an informative visual representation that facilitates a better understanding of calibration performance of probabilistic classifiers.
We further introduced an optimality criterion of bins associated with a minimal estimation error of the empirical probabilities and a new algorithm to compute optimal bins approximately under the constraint of the size of each bin.
Our proposal opens up room for new research directions in the context of calibration.
This paper focuses on the methodological development of TCE.
There are various directions to investigate in terms of theoretical properties of TCE.
These include the convergence properties of TCE in the limit of data size
N
N
, understanding the minimum number of data points that should be contained in each subset
𝒟
b
\mathcal{D}_{b}
, and a rigorous theoretical analysis of PAVA-BC.
By continuing to investigate these areas, we can refine and expand our understanding of the capabilities of TCE.
Acknowledgements.
The authors would like to thank Abbas Zaidi, Michael Gill, and Will Bullock for their useful feedback on early work of this paper.
TM is supported by The Alan Turing Institute under the EPSRC grant EP/N510129/1.
References
Abdallah et al. [2016]
Aisha Abdallah, Mohd Aizaini Maarof, and Anazida Zainal.
Fraud detection system: A survey.
Journal of Network and Computer Applications
, 68:90–113, 2016.
ISSN 1084-8045.
Arrieta-Ibarra et al. [2022]
Imanol Arrieta-Ibarra, Paman Gujral, Jonathan Tannen, Mark Tygert, and Cherie
Xu.
Metrics of calibration for probabilistic predictions.
Journal of Machine Learning Research
, 23(351):1–54, 2022.
Bender and Lange [2001]
Ralf Bender and Stefan Lange.
Adjusting for multiple testing—when and how?
Journal of Clinical Epidemiology
, 54(4):343–349, 2001.
ISSN 0895-4356.
Brier [1950]
Glen W. Brier.
Verification of forecasts expressed in terms of probability.
Monthly Weather Review
, 78(1):1 – 3,
1950.
Bröcker [2009]
Jochen Bröcker.
Reliability, sufficiency, and the decomposition of proper scores.
Quarterly Journal of the Royal Meteorological Society
,
135(643):1512–1519, 2009.
Dawid [1982]
Philip Dawid.
The well-calibrated bayesian.
Journal of the American Statistical Association
, 77(379):605–610, 1982.
de Leeuw et al. [2009]
Jan de Leeuw, Kurt Hornik, and Patrick Mair.
Isotone optimization in r: Pool-adjacent-violators algorithm (pava)
and active set methods.
Journal of Statistical Software
, 32(5):1–24, 2009.
Degroot and Fienberg [1983]
Morris H. Degroot and Stephen E. Fienberg.
The comparison and evaluation of forecasters.
The Statistician
, 32:12–22, 1983.
Dimitriadis et al. [2021]
Timo Dimitriadis, Tilmann Gneiting, and Alexander I. Jordan.
Stable reliability diagrams for probabilistic classifiers.
Proceedings of the National Academy of Sciences
, 118(8), 2021.
Dua and Graff [2017]
Dheeru Dua and Casey Graff.
UCI machine learning repository, 2017.
URL
http://archive.ics.uci.edu/ml
.
Elter et al. [2007]
M Elter, R Schulz-Wendtland, and T Wittenberg.
The prediction of breast cancer biopsy outcomes using two cad
approaches that both emphasize an intelligible decision process.
Medical Physics
, 34(11), 2007.
Gneiting et al. [2007]
Tilmann Gneiting, Fadoua Balabdaoui, and Adrian E. Raftery.
Probabilistic forecasts, calibration and sharpness.
Journal of the Royal Statistical Society: Series B (Statistical
Methodology)
, 69(2):243–268, 2007.
Grigorescu et al. [2020]
Sorin Grigorescu, Bogdan Trasnea, Tiberiu Cocias, and Gigel Macesanu.
A survey of deep learning techniques for autonomous driving.
Journal of Field Robotics
, 37(3):362–386,
2020.
Gupta et al. [2021]
Kartik Gupta, Amir Rahimi, Thalaiyasingam Ajanthan, Thomas Mensink, Cristian
Sminchisescu, and Richard Hartley.
Calibration of neural networks using splines.
In
International Conference on Learning Representations
, 2021.
Henzi et al. [2022]
Alexander Henzi, Alexandre Mösching, and Lutz Dümbgen.
Accelerating the Pool-Adjacent-Violators Algorithm for Isotonic
Distributional Regression.
Methodology and Computing in Applied Probability
, 24(4):2633–2645, 2022.
Kull et al. [2017]
Meelis Kull, Telmo M. Silva Filho, and Peter Flach.
Beyond sigmoids: How to obtain well-calibrated probabilities from
binary classifiers with beta calibration.
Electronic Journal of Statistics
, 11(2):5052 – 5080, 2017.
Kull et al. [2019]
Meelis Kull, Miquel Perello Nieto, Markus Kängsepp, Telmo Silva Filho, Hao
Song, and Peter Flach.
Beyond temperature scaling: Obtaining well-calibrated multi-class
probabilities with dirichlet calibration.
In
Advances in Neural Information Processing Systems
,
volume 32, 2019.
Kumar et al. [2019]
Ananya Kumar, Percy S Liang, and Tengyu Ma.
Verified uncertainty calibration.
In
Advances in Neural Information Processing Systems
,
volume 32, 2019.
Lemaître et al. [2017]
Guillaume Lemaître, Fernando Nogueira, and Christos K. Aridas.
Imbalanced-learn: A python toolbox to tackle the curse of imbalanced
datasets in machine learning.
Journal of Machine Learning Research
, 18(17):1–5, 2017.
Li et al. [2015]
Cheng Li, Yue Lu, Qiaozhu Mei, Dong Wang, and Sandeep Pandey.
Click-through prediction for advertising in twitter timeline.
In
Proceedings of the 21th ACM SIGKDD International Conference
on Knowledge Discovery and Data Mining
, pages 1959–1968, 2015.
Minderer et al. [2021]
Matthias Minderer, Josip Djolonga, Rob Romijnders, Frances Ann Hubis, Xiaohua
Zhai, Neil Houlsby, Dustin Tran, and Mario Lucic.
Revisiting the calibration of modern neural networks.
In
Advances in Neural Information Processing Systems
, 2021.
Naeini et al. [2015]
M. P. Naeini, G. F. Cooper, and M. Hauskrecht.
Obtaining well calibrated probabilities using bayesian binning.
In
Proceedings of the AAAI Conference on Artificial
Intelligence
, pages 2901––2907, 2015.
Niculescu-Mizil and Caruana [2005]
Alexandru Niculescu-Mizil and Rich Caruana.
Predicting good probabilities with supervised learning.
In
Proceedings of the 22nd International Conference on Machine
Learning
, page 625–632, 2005.
Nixon et al. [2019]
Jeremy Nixon, Michael W. Dusenberry, Linchuan Zhang, Ghassen Jerfel, and Dustin
Tran.
Measuring calibration in deep learning.
In
Proceedings of the IEEE/CVF Conference on Computer Vision
and Pattern Recognition (CVPR) Workshops
, June 2019.
Platt [1999]
John C. Platt.
Probabilistic outputs for support vector machines and comparisons to
regularized likelihood methods.
Advances in Large Margin Classifiers
, 10(3), 1999.
Storkey et al. [2009]
Amos Storkey et al.
When training and test sets are different: characterizing learning
transfer.
Dataset shift in machine learning
, 30:3–28, 2009.
Tax et al. [2021]
Niek Tax, Kees Jan de Vries, Mathijs de Jong, Nikoleta Dosoula, Bram van den
Akker, Jon Smith, Olivier Thuong, and Lucas Bernardi.
Machine learning for fraud detection in e-commerce: A research
agenda.
In
Proceedings of the KDD International Workshop on Deployable
Machine Learning for Security Defense (MLHat)
, pages 30–54. Springer, 2021.
Tibshirani et al. [2011]
Ryan J. Tibshirani, Holger Hoefling, and Robert Tibshirani.
Nearly-isotonic regression.
Technometrics
, 53(1):54–61, 2011.
Topol [2019]
Eric Topol.
High-performance medicine: the convergence of human and artificial
intelligence.
Nature Medicine
, 25:44–56, 2019.
Vaicenavicius et al. [2019]
Juozas Vaicenavicius, David Widmann, Carl R. Andersson, Fredrik Lindsten, Jacob
Roll, and Thomas Bo Schön.
Evaluating model calibration in classification.
In
Proceedings of the 22nd International Conference on
Artificial Intelligence and Statistics
, 2019.
van der Putten and van Someren [2000-2009]
Peter van der Putten and Maarten van Someren.
Coil challenge 2000: The insurance company case.
Technical report, Sentient Machine Research, Amsterdam and Leiden
Institute of Advanced Computer Science, 2000-2009.
Wallace and Dahabreh [2014]
Byron C Wallace and Issa J Dahabreh.
Improving class probability estimates for imbalanced data.
Knowledge and Information Systems
, 41(1):33–52, 2014.
Widmann et al. [2019]
David Widmann, Fredrik Lindsten, and Dave Zachariah.
Calibration tests in multi-class classification: A unifying
framework.
In
Advances in Neural Information Processing Systems
,
volume 32, 2019.
Yang and Zhai [2022]
Yanwu Yang and Panyu Zhai.
Click-through rate prediction in online advertising: A literature
review.
Information Processing & Management
, 59(2):102853, 2022.
Zadrozny and Elkan [2001]
Bianca Zadrozny and Charles Elkan.
Obtaining calibrated probability estimates from decision trees and
naive bayesian classifiers.
In
Proceedings of the Eighteenth International Conference on
Machine Learning
, page 609–616, 2001.
Zadrozny and Elkan [2002]
Bianca Zadrozny and Charles Elkan.
Transforming classifier scores into accurate multiclass probability
estimates.
In
Proceedings of the Eighth ACM SIGKDD International
Conference on Knowledge Discovery and Data Mining
, page 694–699, 2002.
TCE: A Test-Based Approach to Measuring Calibration Error
(Supplementary Material)
This supplement contains all the additional results referred to in the main text.
Appendix
A
contains the proof that the optimisation criterion of
eq.
8
is indeed minimised using PAVA.
Appendix
B
shows an example of bins obtained using PAVA-BC that caused mild violation of the monotonic constraint of the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
.
Finally, additional experimental results are presented in
Appendix
C
.
Appendix A
Optimal Bins Based on PAVA
The optimal bins defined by
Definition
3
can be exactly computed under the error function
D
\mathrm{D}
specified by
eq.
9
which corresponds to the variance of each
𝒟
b
y
\mathcal{D}_{b}^{y}
.
The optimal bins result in minimisation of a weighted average of the variance of each
𝒟
b
y
\mathcal{D}_{b}^{y}
over all
b
b
, where the weights are proportional to the size of each bin.
The following proposition shows that
Algorithm
3
with PAVA-BC replaced by PAVA generates the optimal bins under the error function
D
\mathrm{D}
.
In what follows, we assume a standard setting where the solution of
eq.
8
is at least not a set of only one single bin, i.e.,
{
Δ
b
}
b
=
1
1
=
{
[
0
,
1
]
}
\{\Delta_{b}\}_{b=1}^{1}=\{[0,1]\}
.
Proposition 1
.
The minimum of
eq.
8
in
Definition
3
under the error function
D
\mathrm{D}
in
eq.
9
is attained at bins computed by
Algorithm
3
with PAVA-BC replaced by PAVA.
Proof.
First, we show that the optimasation problem of
eq.
8
in
Definition
3
under the loss function
D
\mathrm{D}
in
eq.
9
is equivalent to the monotonic regression problem under the squared error.
Recall that, given a choice of bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
, each label subset
𝒟
b
y
\mathcal{D}_{b}^{y}
is defined by
𝒟
b
y
:=
{
y
i
∈
𝒟
y
∣
P
θ
​
(
x
i
)
∈
Δ
b
}
\mathcal{D}_{b}^{y}:=\{y_{i}\in\mathcal{D}^{y}\mid P_{\theta}(x_{i})\in\Delta_{b}\}
.
The input of
Algorithm
3
is a set of labels
𝒟
y
=
{
y
i
}
i
=
1
N
\mathcal{D}^{y}=\{y_{i}\}_{i=1}^{N}
ordered by in ascending order of
{
P
θ
​
(
x
i
)
}
i
=
1
N
\{P_{\theta}(x_{i})\}_{i=1}^{N}
.
This means that each label subset
𝒟
b
y
\mathcal{D}_{b}^{y}
is a set of consecutive elements in the ordered set
{
y
i
}
i
=
1
N
\{y_{i}\}_{i=1}^{N}
.
Therefore, there exist corresponding indices
n
b
n_{b}
and
n
b
+
1
n_{b+1}
s.t. each label subset
𝒟
b
y
\mathcal{D}_{b}^{y}
can expressed by
𝒟
b
y
=
{
y
i
∈
𝒟
y
∣
P
θ
(
x
i
)
∈
Δ
b
}
=
{
y
i
∈
𝒟
y
∣
i
s.t.
n
b
≤
i
<
n
b
+
1
}
.
\displaystyle\mathcal{D}_{b}^{y}=\{y_{i}\in\mathcal{D}^{y}\mid P_{\theta}(x_{i})\in\Delta_{b}\}=\{y_{i}\in\mathcal{D}^{y}\mid i\penalty\ \penalty\ \text{s.t.}\penalty\ \penalty\ n_{b}\leq i<n_{b+1}\}.
Accordingly, with the ordered labels
𝒟
y
\mathcal{D}^{y}
, each empirical probability
P
^
b
\widehat{P}_{b}
in
𝒟
b
y
\mathcal{D}_{b}^{y}
can be expressed by
P
^
b
=
1
N
b
​
∑
y
∈
𝒟
b
y
y
=
1
n
b
+
1
−
n
b
​
∑
j
=
n
b
n
b
+
1
−
1
y
j
.
\displaystyle\widehat{P}_{b}=\frac{1}{N_{b}}\sum_{y\in\mathcal{D}_{b}^{y}}y=\frac{1}{n_{b+1}-n_{b}}\sum_{j=n_{b}}^{n_{b+1}-1}y_{j}.
Define a set of scalars
{
g
i
}
i
=
1
N
\{g_{i}\}_{i=1}^{N}
whose element
g
i
∈
[
0
,
1
]
g_{i}\in[0,1]
corresponds to the empirical probability
P
^
b
\widehat{P}_{b}
of the bin index
b
b
if
n
b
≤
i
<
n
b
+
1
n_{b}\leq i<n_{b+1}
.
Namely,
g
i
:=
P
^
b
=
1
n
b
+
1
−
n
b
​
∑
j
=
n
b
n
b
+
1
−
1
y
j
for each
i
s.t.
n
b
≤
i
<
n
b
+
1
.
\displaystyle g_{i}:=\widehat{P}_{b}=\frac{1}{n_{b+1}-n_{b}}\sum_{j=n_{b}}^{n_{b+1}-1}y_{j}\quad\text{for each}\quad i\quad\text{s.t.}\quad n_{b}\leq i<n_{b+1}.
(10)
Under these notations, the optimisation criterion in
eq.
8
can be rewritten as
∑
b
=
1
B
W
b
×
D
⁡
(
𝒟
b
,
P
^
b
)
\displaystyle\sum_{b=1}^{B}W_{b}\times\mathrm{D}(\mathcal{D}_{b},\widehat{P}_{b})
=
1
N
​
∑
b
=
1
B
∑
y
∈
𝒟
b
(
y
−
P
^
b
)
2
=
1
N
​
∑
b
=
1
B
∑
i
=
n
b
n
b
+
1
−
1
(
y
i
−
P
^
b
)
2
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
y
i
−
g
i
)
2
.
\displaystyle=\frac{1}{N}\sum_{b=1}^{B}\sum_{y\in\mathcal{D}_{b}}\left(y-\widehat{P}_{b}\right)^{2}=\frac{1}{N}\sum_{b=1}^{B}\sum_{i=n_{b}}^{n_{b+1}-1}\left(y_{i}-\widehat{P}_{b}\right)^{2}=\frac{1}{N}\sum_{i=1}^{N}(y_{i}-g_{i})^{2}.
(11)
This formulation translates a problem of choosing bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
into a problem of finding a monotonically increasing sequence
{
g
i
}
i
=
1
N
\{g_{i}\}_{i=1}^{N}
that is determined by the choice of indices
{
n
b
}
b
=
1
B
\{n_{b}\}_{b=1}^{B}
, so that
eq.
11
is minimised.
Therefore the optimasation problem of
eq.
8
in
Definition
3
under the loss function
D
\mathrm{D}
in
eq.
9
is equivalent to the monotonic regression problem under the squared error whose solution sequence
{
g
i
}
i
=
1
N
\{g_{i}\}_{i=1}^{N}
is restriced to a form of
eq.
10
.
Next, consider a standard monotonic regression problem under the square error
∑
i
=
1
N
(
y
i
−
y
^
i
)
2
\sum_{i=1}^{N}(y_{i}-\widehat{y}_{i})^{2}
for the ordered set
{
y
i
}
i
=
1
N
\{y_{i}\}_{i=1}^{N}
.
PAVA finds a monotonically increasing sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
that minimises the square error.
The solution sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
by PAVA is given in a form of
eq.
10
; see e.g.
[
de Leeuw et al., 2009
,
Henzi et al., 2022
]
.
This means that there exists a set of indices
{
n
b
∗
}
b
=
1
B
\{n_{b}^{*}\}_{b=1}^{B}
s.t. the solution sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
by PAVA is expressed as
y
^
i
=
1
n
b
+
1
∗
−
n
b
∗
​
∑
j
=
n
b
∗
n
b
+
1
∗
y
j
for each
i
s.t.
n
b
∗
≤
i
<
n
b
+
1
∗
\displaystyle\widehat{y}_{i}=\frac{1}{n_{b+1}^{*}-n_{b}^{*}}\sum_{j=n_{b}^{*}}^{n_{b+1}^{*}}y_{j}\quad\text{for each}\quad i\quad\text{s.t.}\quad n_{b}^{*}\leq i<n_{b+1}^{*}
and the sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
satisfies the monotonic constraint
y
^
1
≤
⋯
≤
y
^
N
\widehat{y}_{1}\leq\dots\leq\widehat{y}_{N}
holds.
We can obtain such a solution sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
by applying any standard implementation of PAVA.
An output of most implementations of PAVA is the solution sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
rather than the associated indices
{
n
b
∗
}
b
=
1
B
\{n_{b}^{*}\}_{b=1}^{B}
.
However, the indices
{
n
b
∗
}
b
=
1
B
\{n_{b}^{*}\}_{b=1}^{B}
can be easily recovered from a given solution sequence
{
y
^
i
}
i
=
1
N
\{\widehat{y}_{i}\}_{i=1}^{N}
of PAVA by simply finding all indeces
i
i
s.t.
y
^
i
≠
y
^
i
+
1
\widehat{y}_{i}\neq\widehat{y}_{i+1}
.
Finally, we consider constructing bins
{
Δ
b
}
b
=
1
B
\{\Delta_{b}\}_{b=1}^{B}
based on the recovered indices
{
n
b
∗
}
b
=
1
B
\{n_{b}^{*}\}_{b=1}^{B}
.
Recall that the set of labels
𝒟
y
=
{
y
i
}
i
=
1
N
\mathcal{D}^{y}=\{y_{i}\}_{i=1}^{N}
are ordered in ascending order of
{
P
θ
​
(
x
i
)
}
i
=
1
N
\{P_{\theta}(x_{i})\}_{i=1}^{N}
.
If we construct each bin
Δ
b
\Delta_{b}
by
Δ
b
:=
[
P
θ
​
(
x
n
b
∗
−
1
)
+
P
θ
​
(
x
n
b
∗
)
2
,
P
θ
​
(
x
n
b
+
1
∗
−
1
)
+
P
θ
​
(
x
n
b
+
1
∗
)
2
]
,
\displaystyle\Delta_{b}:=\left[\frac{P_{\theta}(x_{n_{b}^{*}-1})+P_{\theta}(x_{n_{b}^{*}})}{2},\frac{P_{\theta}(x_{n_{b+1}^{*}-1})+P_{\theta}(x_{n_{b+1}^{*}})}{2}\right],
it is sufficient to generate each label subset
𝒟
b
y
\mathcal{D}_{b}^{y}
that corresponds to
𝒟
b
y
=
{
y
i
∈
𝒟
y
∣
P
θ
(
x
i
)
∈
Δ
b
}
=
{
y
i
∈
𝒟
y
∣
i
s.t.
n
b
∗
≤
i
<
n
b
+
1
∗
}
.
\displaystyle\mathcal{D}_{b}^{y}=\{y_{i}\in\mathcal{D}^{y}\mid P_{\theta}(x_{i})\in\Delta_{b}\}=\{y_{i}\in\mathcal{D}^{y}\mid i\penalty\ \penalty\ \text{s.t.}\penalty\ \penalty\ n_{b}^{*}\leq i<n_{b+1}^{*}\}.
Then the optimisation criterion in
eq.
8
, which is translated to the error of the monotonic regression problem of PAVA, is minimised by the choice of bins produced in this procedure.
Observing that
Algorithm
3
with PAVA-BC replaced by PAVA performs this procedure concludes the proof.
∎
Appendix B
Mild Violation of Monotonicity by PAVA-BC
A monotonic regression algorithm finds a monotonically increasing sequence
y
^
1
≤
⋯
≤
y
^
N
\widehat{y}_{1}\leq\cdots\leq\widehat{y}_{N}
that minimises some error
D
⁡
(
{
y
^
i
}
i
=
1
N
,
{
y
i
}
i
=
1
N
)
\mathrm{D}(\{\widehat{y}_{i}\}_{i=1}^{N},\{y_{i}\}_{i=1}^{N})
for a given ordered set
{
y
i
}
i
=
1
N
\{y_{i}\}_{i=1}^{N}
.
PAVA is one of the most common monotonic regression algorithms that uses the square error
∑
i
=
1
N
(
y
^
i
−
y
i
)
2
\sum_{i=1}^{N}(\widehat{y}_{i}-y_{i})^{2}
.
For some partition
𝒜
\mathcal{A}
of indices
I
=
{
1
,
…
,
N
}
I=\{1,\dots,N\}
whose element
A
∈
𝒜
A\in\mathcal{A}
is a set of consequentive indices in
I
I
, PAVA produces a solution sequence s.t. each element
y
^
i
\widehat{y}_{i}
is given by
y
^
i
=
(
1
/
|
A
|
)
​
∑
i
∈
A
y
i
\widehat{y}_{i}=(1/|A|)\sum_{i\in A}y_{i}
for
A
A
in which
i
∈
A
i\in A
.
We refer to each element
A
A
in the partition
𝒜
\mathcal{A}
of indices
I
I
as
block
.
PAVA-BC produces a solution sequence that approximates the solution sequence by PAVA under the contraints of the minimum and maximum size of each block.
For some partition
𝒜
′
\mathcal{A}^{\prime}
of indices
I
I
, each element
y
^
i
\widehat{y}_{i}
of the solution sequence is given by
y
^
i
=
(
1
/
|
A
′
|
)
​
∑
i
∈
A
′
y
i
\widehat{y}_{i}=(1/|A^{\prime}|)\sum_{i\in A^{\prime}}y_{i}
for
A
′
A^{\prime}
in which
i
∈
A
′
i\in A^{\prime}
in the same manner as PAVA.
PAVA-BC meets the minimum and maximum size constraints of each block
A
′
∈
𝒜
′
A^{\prime}\in\mathcal{A}^{\prime}
at the cost of the possibility of mild violation of the monotonic constraint.
It depends on the minimum and maximum size constraints, data, and models whether violation of the monotonic constraint occurs by PAVA-BC.
Figure
3
shows an example where bins based on PAVA-BC did not violate the monotonicity of the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
.
Figure
3
was computed using a random forest model trained on the
satimage
dataset used in
Section
4.2
, and corresponds to
Figure
2
presented in
Section
3
.
The total estimation error in
eq.
8
and an average of the estimation error within each bin in
eq.
9
for each set of the bins in
Figure
3
were summerised in
Table
1
presented in
Section
3
.
Figure
4
shows an example where bins based on PAVA-BC violated the monotonic constraint of the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
.
Figure
4
was computed using a random forest model trained on the
coil_2000
dataset used in
Section
4.2
.
The total estimation error in
eq.
8
for each set of the bins in
Figure
4
was
0.0509
0.0509
,
0.0517
0.0517
, and
0.0521
0.0521
for PAVA, PAVA-BC, binning based on
10
10
-quantiles, respectively.
An average of the estimation error within each bin in
eq.
9
for each set of the bins in
Figure
3
was
0.0834
0.0834
,
0.0627
0.0627
, and
0.0520
0.0520
for PAVA, PAVA-BC, binning based on
10
10
-quantiles, respectively.
Figure 3
:
Comparison of bins based on three different approaches for a random forest model on the satimage dataset: (top) PAVA, (middle) PAVA-BC, (bottom) binning based on
10
10
-quantiles. The dotted line in the left and right panels represents the boundary of each bin. The grey bar in the left panel repsents the size of each bin. The red line in the right panel repsents the empirical probability of each bin.
Figure 4
:
Comparison of bins based on three different approaches for a random forest model on the satimage dataset: (top) PAVA, (middle) PAVA-BC, (bottom) binning based on
10
10
-quantiles. Each xaxis is restricted to a range
[
0.0
,
0.1
]
[0.0,0.1]
as the majority of bins were contained in the range in this example. The dotted line in the left and right panels represents the boundary of each bin. The grey bar in the left panel repsents the size of each bin. The red line in the right panel repsents the empirical probability of each bin. A random forest model trained on the coil_2000 dataset was used.
Appendix C
Additional Experiments
We present additional experiments in each section that complement the experiments illustrated in the main text.
We use the same settings as the main text for the minimum and maximum size for bins based on PAVA-BC as well as the bin number
B
B
for equi-spaced and quantile-based bins.
C.1
Simulation Study of TCE
We perform detailed simulation studies of TCE in the same simplified setting as Section 4.1.
We demonstarate sensitivity of TCE to its hyperparameters, an impact of different dataset size and prevalence, and sensitivity to a small purtabation to model predictions.
In all experiments, we generated training and test data from the Gaussian discriminant analysis in Section 4.1, each with the prevalence
P
training
​
(
y
)
P_{\text{training}}(y)
and
P
test
​
(
y
)
P_{\text{test}}(y)
, and compute TCE of a logistic model fitted to the training data.
In all experiments except ones on an impact of different dataset size and prevalence, we set the training data size to
14000
14000
and set the test data size to
6000
6000
.
We then examine two cases where the model is calibated and miscalibrated synthetically, setting
P
training
​
(
y
)
=
0.5
P_{\text{training}}(y)=0.5
and
P
test
​
(
y
)
=
0.5
P_{\text{test}}(y)=0.5
for the first case and setting
P
training
​
(
y
)
=
0.5
P_{\text{training}}(y)=0.5
and
P
test
​
(
y
)
=
0.4
P_{\text{test}}(y)=0.4
for the second case.
In summary, we present the following experimental analyses:
•
Sensitivity to the minimum bin size
N
min
N_{\text{min}}
in PAVA-BC from
N
min
=
1
N_{\text{min}}=1
to
N
min
=
3000
N_{\text{min}}=3000
;
•
Sensitivity to the maximum bin size
N
min
N_{\text{min}}
in PAVA-BC from
N
max
=
6
N_{\text{max}}=6
to
N
max
=
6000
N_{\text{max}}=6000
;
•
Sensitivity to a pair of
(
N
min
,
N
max
)
(N_{\text{min}},N_{\text{max}})
in PAVA-BC chosen so that each binsize fall into selected ranges;
•
Sensitivity to a small purtabation of predictions by a logit-normal noise with scale
σ
\sigma
from
σ
=
0.0
\sigma=0.0
to
σ
=
1.0
\sigma=1.0
;
•
Sensitivity to a choice of significance level
α
\alpha
in the Binomial test from
α
=
0.0001
\alpha=0.0001
to
α
=
0.1
\alpha=0.1
;
•
Comparison of TCE by different choices of test, binomial test and t-test;
•
Comparison of TCE by different total sizes
N
N
of test dataset from
N
=
30
N=30
to
N
=
60000
N=60000
;
•
Comparison of TCE by different prevalences
P
P
of dataset from
P
=
0.5
P=0.5
to
P
=
0.02
P=0.02
.
Tables
6
,
7
,
8
,
9
,
10
,
11
,
12
and
13
presents the result of each experiment above in order.
In each table, TCE(P) denotes TCE based on PAVA-BC, TCE(Q) denotes TCE based on quantile-binning, and TCE(V) denotes TCE based on PAVA.
For reference, we include values of ECE, ACE, MCE, and MCE(Q), where MCE(Q) denotes MCE based on quantile-binning.
Observations from each result in are summarised as follows.
•
Table
6
: The performance of TCE(P) to evidence the well-calibrated model was consistently reasonable for any minimum binsize constaint between
N
max
=
1
N_{\text{max}}=1
and
N
max
=
600
N_{\text{max}}=600
, while there was a breakdown point between
N
min
=
600
N_{\text{min}}=600
and
N
min
=
3000
N_{\text{min}}=3000
where TCE(P) was no longer able to do so. This is likely because the number of bins produced under the contraint
N
min
=
3000
N_{\text{min}}=3000
for the total datasize
6000
6000
was
2
2
at maximum, which was too small to estimate the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
accurately.
•
Table
7
: The performance of TCE(P) to evidence the miscalibrated model was consistently reasonable for any maximum binsize constaint between
N
max
=
300
N_{\text{max}}=300
and
N
max
=
6000
N_{\text{max}}=6000
, while there was a breakdown point between
N
min
=
60
N_{\text{min}}=60
and
N
min
=
300
N_{\text{min}}=300
where TCE(P) was no longer able to do so. This is likely because the number of bins produced under the contraint
N
max
=
60
N_{\text{max}}=60
for the total datasize
6000
6000
was
100
100
at minimum, which is too large to estimate the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
accurately.
•
Table
8
: The performance of TCE(P) to evidence both the well-calibrated and miscalibrated models was arguably the most reasonable when
(
N
min
,
N
max
)
(N_{\text{min}},N_{\text{max}})
was chosen so that the number of bins produced falls into the range
[
5
,
20
]
[5,20]
. This suggests a huristic to use such
(
N
min
,
N
max
)
(N_{\text{min}},N_{\text{max}})
for other experiments.
•
Table
9
: At each model prediction
P
θ
​
(
x
)
P_{\theta}(x)
, we sample a new prediction from a logit-normal distribution centred at
P
θ
​
(
x
)
P_{\theta}(x)
with scale
σ
\sigma
to generate a perturbed prediction by a small noise. All calibration error metrics were shown to have similar sensitivities to the noise. The scale between
σ
=
0.10
\sigma=0.10
and
σ
=
0.50
\sigma=0.50
was the breakdown point where each metric started to produce an unreasonable score for the well-calibrated model.
•
Table
10
: The performance of TCE(P) to evidence both the well-calibrated and miscalibrated models was consistently reasonable for any significant level between
α
=
0.001
\alpha=0.001
and
α
=
0.1
\alpha=0.1
, while there was a breakdown point between
α
=
0.1
\alpha=0.1
and
α
=
0.5
\alpha=0.5
where TCE(P) was no longer able to do so for the well-calibrated model.
•
Table
11
: TCE based on the Binomial test outperformed one based on the t-test in the majority of the settings. It is possible that the Binomial test produces more accurate outcomes than the t-test, given that it is an exact test whose test statistics does not involve any apporoximation.
•
Table
12
: The performance of TCE(P) to evidence both the well-calibrated and miscalibrated models was consistently reasonable for any dataset size between
N
test
=
3000
N_{\text{test}}=3000
and
N
test
=
60000
N_{\text{test}}=60000
, while there was a breakdown point between
N
test
=
600
N_{\text{test}}=600
and
N
test
=
3000
N_{\text{test}}=3000
where TCE(P) was no longer able to do so for the well-calibrated model. This is likely because the dataset size
N
test
=
600
N_{\text{test}}=600
was not big enough to estimate the empirical probabilities
{
P
^
b
}
b
=
1
B
\{\widehat{P}_{b}\}_{b=1}^{B}
accurately. This result may be improved by using different settings of the minimnum and maximum binsize constaints.
•
Table
13
: The performance of TCE(P) on both the well-calibrated and miscalibrated models was reasonable for any prevalence. While there was a fluctuation in values of TCE(P) for different values of prevalence, TCE(P) overall produced better values than TCE(Q and TCE(V).
Table 6
:
Sensitivity to the minimum binsize
N
min
=
1
,
6
,
30
,
300
,
600
,
3000
N_{\text{min}}=1,6,30,300,600,3000
in PAVA-BC. For comparison purpose, the number of bins
B
B
of quantile-binning and equispaced-binning was varied as
B
=
1000,500,100
,
50
,
10
,
5
,
1
B=1000,500,100,50,10,5,1
along with
N
min
N_{\text{min}}
. Note that TCE(V) is a constant across all the row because PAVA does not involve any binsize constraint.
Test Prevalence
Min Binsize
TCE(P)
TCE(Q)
TCE(V)
ECE
ACE
MCE
MCE(Q)
50%
(Calibrated)
1
3.4500
5.1000
3.4500
0.1143
0.1651
0.8767
0.6392
6
3.3833
4.2000
3.4500
0.0839
0.1142
0.8767
0.5016
30
2.3500
4.3000
3.4500
0.0382
0.0457
0.8767
0.1705
60
2.6333
3.5667
3.4500
0.0271
0.0370
0.2533
0.1189
300
7.2833
10.8833
3.4500
0.0138
0.0150
0.1020
0.0528
600
13.5667
38.7500
3.4500
0.0116
0.0086
0.1020
0.0236
3000
92.2000
92.2000
3.4500
0.0021
0.0021
0.0021
0.0021
40%
(Miscalibrated)
1
88.0667
6.6667
88.0667
0.1417
0.1847
0.8767
0.6111
6
88.0667
8.7000
88.0667
0.1179
0.1389
0.8767
0.4811
30
88.3333
32.2833
88.0667
0.0993
0.0992
0.8767
0.2264
60
87.8667
56.7667
88.0667
0.0971
0.0964
0.2426
0.1827
300
96.1000
96.4667
88.0667
0.0963
0.0951
0.1466
0.1314
600
96.6000
96.7833
88.0667
0.0963
0.0951
0.1099
0.1092
3000
93.9500
93.9500
88.0667
0.0951
0.0951
0.0951
0.0951
Table 7
:
Sensitivity to the maximum binsize
N
max
=
6
,
30
,
300
,
600
,
3000
,
6000
N_{\text{max}}=6,30,300,600,3000,6000
in PAVA-BC. For comparison purpose, the number of bins
B
B
of quantile-binning and equispaced-binning was varied as
B
=
1000,500,100
,
50
,
10
,
5
,
1
B=1000,500,100,50,10,5,1
along with
N
max
N_{\text{max}}
. Note that TCE(V) is a constant across all the row because PAVA does not involve any binsize constraint.
Test Prevalence
Max Binsize
TCE(P)
TCE(Q)
TCE(V)
ECE
ACE
MCE
MCE(Q)
50%
(Calibrated)
6
5.8500
5.1000
3.4500
0.1143
0.1651
0.8767
0.6392
30
3.0000
4.2000
3.4500
0.0839
0.1142
0.8767
0.5016
60
2.3667
4.3000
3.4500
0.0382
0.0457
0.8767
0.1705
300
3.7667
3.5667
3.4500
0.0271
0.0370
0.2533
0.1189
600
3.3833
10.8833
3.4500
0.0138
0.0150
0.1020
0.0528
3000
3.4500
38.7500
3.4500
0.0116
0.0086
0.1020
0.0236
6000
3.4500
92.2000
3.4500
0.0021
0.0021
0.0021
0.0021
40%
(Miscalibrated)
6
5.5000
6.6667
88.0667
0.1417
0.1847
0.8767
0.6111
30
9.1000
8.7000
88.0667
0.1179
0.1389
0.8767
0.4811
60
14.3833
32.2833
88.0667
0.0993
0.0992
0.8767
0.2264
300
79.6667
56.7667
88.0667
0.0971
0.0964
0.2426
0.1827
600
85.6500
96.4667
88.0667
0.0963
0.0951
0.1466
0.1314
3000
88.0667
96.7833
88.0667
0.0963
0.0951
0.1099
0.1092
6000
88.0667
93.9500
88.0667
0.0951
0.0951
0.0951
0.0951
Table 8
:
Sensitivity to the pairs
(
N
max
,
N
min
)
(N_{\text{max}},N_{\text{min}})
in PAVA-BC selected so that the number of bins produced falls into ranges
[
250
,
1000
]
,
[
50,200
]
,
[
25,100
]
,
[
10
,
20
]
,
[
3
,
10
]
[250,1000],[50,200],[25,100],[10,20],[3,10]
. For comparison purpose, the number of bins
B
B
of quantile-binning and equispaced-binning was varied as
B
=
1000,500,100
,
50
,
10
,
5
,
1
B=1000,500,100,50,10,5,1
along with
(
N
max
,
N
min
)
(N_{\text{max}},N_{\text{min}})
. Note that TCE(V) is a constant across all the row because PAVA does not involve any binsize constraint.
Test Prevalence
Binsize Range
TCE(P)
TCE(Q)
TCE(V)
ECE
ACE
MCE
MCE(Q)
50%
(Calibrated)
[250, 1000]
3.8000
4.2000
3.4500
0.0839
0.1142
0.8767
0.5016
[50, 200]
1.8333
4.3000
3.4500
0.0382
0.0457
0.8767
0.1705
[25, 100]
0.2833
3.5667
3.4500
0.0271
0.0370
0.2533
0.1189
[5, 20]
7.2833
10.8833
3.4500
0.0138
0.0150
0.1020
0.0528
[3, 10]
13.5667
38.7500
3.4500
0.0116
0.0086
0.1020
0.0236
40%
(Miscalibrated)
[250, 1000]
7.7333
8.7000
88.0667
0.1179
0.1389
0.8767
0.4811
[50, 200]
45.7667
32.2833
88.0667
0.0993
0.0992
0.8767
0.2264
[25, 100]
66.1833
56.7667
88.0667
0.0971
0.0964
0.2426
0.1827
[10, 20]
96.1000
96.4667
88.0667
0.0963
0.0951
0.1466
0.1314
[3, 10]
96.6000
96.7833
88.0667
0.0963
0.0951
0.1099
0.1092
Table 9
:
Sensitivity to a small purtabation to model predictions by a logit-normal noise with scale
σ
=
0.01
,
0.05
,
0.10
,
0.50
,
1.00
\sigma=0.01,0.05,0.10,0.50,1.00
. The maximum and minimum binsize of PAVA-BC were set to
1200
1200
and
300
300
. The number of bins of quantile-binning and equispaced-binning was set
10
10
.
Test Prevalence
Noise Level
TCE(P)
TCE(Q)
TCE(V)
ECE
ACE
MCE
MCE(Q)
50%
(Calibrated)
0.00
7.2833
10.8833
3.4500
0.0138
0.0150
0.1020
0.0528
0.01
8.7167
9.6167
4.8000
0.0113
0.0125
0.0923
0.0527
0.05
12.8833
11.9000
7.7667
0.0136
0.0156
0.1198
0.0589
0.10
8.3500
13.0500
3.5500
0.0109
0.0164
0.1143
0.0587
0.50
61.9500
65.0500
56.1000
0.0615
0.0618
0.3601
0.1498
1.00
86.1833
84.1000
88.3833
0.1470
0.1478
0.3364
0.2621
40%
(Miscalibrated)
0.00
96.1000
96.4667
88.0667
0.0963
0.0951
0.1466
0.1314
0.01
96.4000
96.4000
89.6167
0.0962
0.0951
0.1511
0.1332
0.05
94.7667
95.5333
89.1667
0.0962
0.0951
0.1496
0.1420
0.10
93.8500
95.9667
86.5833
0.0967
0.0951
0.1852
0.1412
0.50
86.6667
83.9000
81.2667
0.1071
0.1055
0.2513
0.2203
1.00
90.3167
88.8500
91.2167
0.1713
0.1698
0.4577
0.3648
Table 10
:
Sensitivity to a choice of significance level
α
=
0.001
,
0.005
,
0.01
,
0.05
,
0.1
,
0.5
\alpha=0.001,0.005,0.01,0.05,0.1,0.5
. The maximum and minimum binsize of PAVA-BC were set to
1200
1200
and
300
300
. The number of bins of quantile-binning and equispaced-binning was set
10
10
.
Test Prevalence
Significant Level
TCE(P)
TCE(Q)
TCE(V)
ECE
ACE
MCE
MCE(Q)
50%
(Calibrated)
0.001
1.4500
4.6833
0.1833
0.0138
0.0150
0.1020
0.0528
0.005
2.4667
5.5667
1.1333
0.0138
0.0150
0.1020
0.0528
0.010
3.0500
6.2000
1.6500
0.0138
0.0150
0.1020
0.0528
0.050
7.2833
10.8833
3.4500
0.0138
0.0150
0.1020
0.0528
0.100
12.8500
15.2000
6.8667
0.0138
0.0150
0.1020
0.0528
0.500
53.1000
55.3333
46.5667
0.0138
0.0150
0.1020
0.0528
40%
(Miscalibrated)
0.001
77.8000
83.3833
76.1000
0.0963
0.0951
0.1466
0.1314
0.005
86.3000
92.8000
80.0833
0.0963
0.0951
0.1466
0.1314
0.010
90.1833
95.2167
83.1167
0.0963
0.0951
0.1466
0.1314
0.050
96.1000
96.4667
88.0667
0.0963
0.0951
0.1466
0.1314
0.100
97.2167
96.9167
90.1667
0.0963
0.0951
0.1466
0.1314
0.500
99.3000
98.7167
97.7500
0.0963
0.0951
0.1466
0.1314
Table 11
:
Comparison of TCE based on the Binomial test and the t-test. TCE(Q)-B denotes TCE(Q) based on the Binomial test and TCE(Q)-T denotes TCE(Q) based on the t-test; the same applies for the other columns. The maximum and minimum binsize of PAVA-BC and the number of bins of quantile-binning and equispaced-binning were varied as in
Table
8
.
Test Prevalence
Binsize Range
TCE(P)-B
TCE(P)-T
TCE(Q)-B
TCE(Q)-T
TCE(V)-B
TCE(V)-T
50%
(Calibrated)
[250, 1000]
3.8000
33.6667
4.2000
31.9167
3.4500
34.2167
[50, 200]
1.8333
36.0000
4.3000
31.4333
3.4500
34.2167
[25, 100]
0.2833
31.3667
3.5667
40.4333
3.4500
34.2167
[5, 20]
7.2833
37.8000
10.8833
41.8500
3.4500
34.2167
[3, 10]
13.5667
46.5000
38.7500
68.8167
3.4500
34.2167
40%
(Miscalibrated)
[250, 1000]
7.7333
50.2833
8.7000
45.1833
88.0667
97.7333
[50, 200]
45.7667
73.2667
32.2833
71.1667
88.0667
97.7333
[25, 100]
66.1833
96.5333
56.7667
85.3833
88.0667
97.7333
[5, 20]
96.1000
99.2667
96.4667
98.4833
88.0667
97.7333
[3, 10]
96.6000
98.6333
96.7833
98.4833
88.0667
97.7333
Table 12
:
Comparison of TCE by different total sizes
N
test
=
30
,
60
,
300
,
600
,
3000
,
6000
,
30000
,
60000
N_{\text{test}}=30,60,300,600,3000,6000,30000,60000
of test dataset. The training prevalence was
P
training
​
(
y
)
=
0.5
P_{\text{training}}(y)=0.5
for all datasets. The maximum and minimum binsize of PAVA-BC were set by
N
max
=
N
test
/
20
N_{\text{max}}=N_{\text{test}}/20
and
N
min
=
N
test
/
5
N_{\text{min}}=N_{\text{test}}/5
. The number of bins of quantile-binning and equispaced-binning was set
10
10
.
Test Prevalence
Data Size
TCE(P)
TCE(Q)
TCE(V)
ECE
ACE
MCE
MCE(Q)
50%
(Calibrated)
30
0.0000
0.0000
0.0000
0.2293
0.2631
0.4164
0.5660
60
0.0000
3.3333
0.0000
0.0923
0.2158
0.7148
0.4208
300
5.3333
11.0000
6.3333
0.0774
0.0867
0.1971
0.2057
600
1.0000
4.5000
1.6667
0.0368
0.0445
0.3404
0.1270
3000
8.0667
4.6333
4.7667
0.0190
0.0182
0.1209
0.0304
6000
7.2833
10.8833
3.4500
0.0138
0.0150
0.1020
0.0528
30000
16.1633
31.7167
0.7833
0.0036
0.0061
0.9045
0.0164
60000
19.1483
45.7600
4.4417
0.0035
0.0043
0.0949
0.0100
40%
(Miscalibrated)
30
13.3333
6.6667
36.6667
0.3164
0.3377
0.6569
0.6338
60
0.0000
3.3333
0.0000
0.1072
0.1611
0.7148
0.4208
300
27.3333
37.3333
48.3333
0.1240
0.1368
0.1971
0.2665
600
14.1667
8.0000
26.5000
0.0694
0.0685
0.5824
0.1350
3000
92.2333
91.7667
76.7667
0.0964
0.0958
0.1495
0.1358
6000
96.1000
96.4667
88.0667
0.0963
0.0951
0.1466
0.1314
30000
99.4700
99.2300
97.4433
0.0907
0.0906
0.9045
0.1064
60000
99.7783
99.6600
98.9000
0.0923
0.0923
0.0972
0.1065
Table 13
:
Comparison of TCE by different prevalences
P
P
of training and test dataset. The training data size was
14000
14000
and the test data size was
6000
6000
. The maximum and minimum binsize of PAVA-BC were set to
1200
1200
and
300
300
. The number of bins of quantile-binning and equispaced-binning was set
10
10
.
Train - Test Prevalence
TCE(P)
TCE(Q)
TCE(V)
ECE
ACE
MCE
MCE(Q)
Calibrated
50% - 50%
7.2833
10.8833
3.4500
0.0138
0.0150
0.1020
0.0528
40% - 40%
7.5500
16.2167
8.5667
0.0137
0.0191
0.1632
0.0365
30% - 30%
8.1667
12.8833
2.8167
0.0125
0.0134
0.1042
0.0313
20% - 20%
15.9500
22.2167
15.9167
0.0173
0.0153
0.6238
0.0370
10% - 10%
11.9833
16.7833
15.2333
0.0096
0.0114
0.4361
0.0218
8% - 8%
15.7000
18.5167
23.1500
0.0087
0.0107
0.0700
0.0234
6% - 6%
11.5333
17.5500
13.9833
0.0035
0.0109
0.3064
0.0195
4% - 4%
18.5000
15.6667
20.5833
0.0046
0.0074
0.2240
0.0177
2% - 2%
13.1167
11.5500
20.7667
0.0052
0.0059
0.0052
0.0131
Miscalibrated
50% - 40%
96.1000
96.4667
88.0667
0.0963
0.0951
0.1466
0.1314
40% - 30%
96.5667
96.1833
82.7500
0.0872
0.0869
0.1485
0.1262
30% - 20%
94.9500
94.6667
88.5833
0.0846
0.0846
0.2146
0.1247
20% - 10%
95.8833
95.5833
96.4333
0.0868
0.0868
0.6238
0.1500
10% - 8%
32.3500
26.7000
42.5667
0.0151
0.0173
0.4361
0.0502
8% - 6%
42.3167
38.7833
45.8333
0.0164
0.0186
0.3259
0.0477
6% - 4%
47.0833
39.9500
65.9500
0.0167
0.0188
0.3064
0.0440
4% - 2%
56.5833
42.4333
72.4500
0.0142
0.0142
0.2240
0.0337
2% - 0%
99.9167
96.9000
100.0000
0.0181
0.0181
0.0181
0.0382
C.2
Results on Other UCI Datasets
Algorithms in Section 4.2 are all trained with the default hyperparameters in the scikit-learn package, except that the maximum depth in the random forest is set to 10 and the number of hidden layers in the multiple perceptron is set to 1 with 1000 units.
For better comparison, we add TCE based on quantile bins, denoted TCE(Q) in each table, to five metrics presented in the main text.
The following
Table
14
compares six different calibration error metrics computed for eight UCI datasets that were not presented in the main text: coil_2000, isolet, letter_img, mammography, optimal_degits, pen_degits, satimage, spambase
[
Dua and Graff, 2017
,
van der Putten and van Someren, 2000-2009
,
Elter et al., 2007
]
.
The prevalence of the spambase dataset is well-balanced and that of the rest is imbalanced.
The following
Figures
5
and
6
shows the visual representations of TCE, ECE, and ACE—the test-based reliability diagram and the standard reliability diagram—each for the logistic regression and the gradient boosting algorithm.
We selected four datasets, abalone, coil_2000, isolet, and webpage, to produce the visual representations in
Figures
5
and
6
.
C.3
Reliability Diagrams of Results on ImageNet1000
The following
Figure
7
shows the viaual representations of TCE, ECE, and ACE—the test-based reliability diagram and the standard reliability diagram—for four different deep learning models presented in the main text, where we omit the model ResNet50 whose result sufficiently resembles that of ResNet18.
Table 14
:
Comparison of six calibration error metrics for five algorithms trained on eight UCI datasets. The same setting of TCE presented in
Section
4
is used. TCE(Q) and MCE(Q) denotes TCE and MCE each based on quantile bins where the number of bins is set to
10
10
.
Data
Algorithm
TCE
TCE(Q)
ECE
ACE
MCE
MCE(Q)
coil_2000
LR
8.6189
11.7408
0.0047
0.0111
0.8558
0.0326
SVM
17.0003
28.9447
0.0071
0.0216
0.4860
0.0381
RF
22.2260
6.1758
0.0027
0.0125
0.2465
0.0439
GB
20.8687
12.6569
0.0052
0.0098
0.3738
0.0259
MLP
98.7445
98.7784
0.0652
0.0578
0.7900
0.1649
isolet
LR
28.8462
27.3932
0.0131
0.0051
0.2183
0.0286
SVM
11.5812
13.2479
0.0064
0.0028
0.1969
0.0194
RF
66.4530
52.5214
0.0524
0.0507
0.3635
0.2137
GB
25.2991
16.6667
0.0198
0.0174
0.4463
0.1123
MLP
9.8291
17.5641
0.0049
0.0031
0.4173
0.0232
letter_img
LR
10.5167
12.0500
0.0025
0.0008
0.1617
0.0042
SVM
11.8667
14.8167
0.0019
0.0017
0.6257
0.0146
RF
26.5000
20.2500
0.0097
0.0033
0.5179
0.0131
GB
25.9500
18.7333
0.0067
0.0029
0.3653
0.0109
MLP
19.9833
9.9833
0.0010
0.0001
0.4550
0.0007
mammography
LR
25.0671
26.7660
0.0027
0.0065
0.3594
0.0208
SVM
20.2683
20.1490
0.0067
0.0088
0.6741
0.0353
RF
19.4039
9.2996
0.0047
0.0016
0.4465
0.0043
GB
14.5156
15.4098
0.0061
0.0034
0.5355
0.0124
MLP
20.5663
26.9747
0.0042
0.0027
0.4351
0.0113
optical_digits
LR
11.6251
27.1649
0.0098
0.0037
0.2251
0.0135
SVM
4.8043
10.6762
0.0042
0.0028
0.6608
0.0157
RF
49.6441
38.3155
0.0451
0.0433
0.5432
0.2271
GB
13.0486
11.2693
0.0181
0.0168
0.5639
0.1122
MLP
4.6856
12.1590
0.0037
0.0034
0.5992
0.0306
pen_digits
LR
20.4063
23.1049
0.0121
0.0060
0.1652
0.0252
SVM
9.7635
10.2790
0.0017
0.0010
0.4735
0.0068
RF
29.6240
22.8623
0.0152
0.0132
0.4535
0.0592
GB
9.9151
13.0988
0.0077
0.0058
0.6543
0.0303
MLP
9.4603
10.0061
0.0014
0.0004
0.6457
0.0037
satimage
LR
23.6665
23.0968
0.0215
0.0223
0.7312
0.0767
SVM
10.2020
21.8540
0.0229
0.0163
0.1666
0.0870
RF
29.1041
20.1450
0.0265
0.0214
0.2084
0.1328
GB
23.2004
19.8861
0.0154
0.0235
0.2101
0.0902
MLP
58.0528
58.4671
0.0352
0.0328
0.5049
0.1384
spambase
LR
33.6713
56.1188
0.0256
0.0267
0.1539
0.0895
SVM
12.8168
34.5402
0.0177
0.0227
0.2207
0.0465
RF
66.0391
49.4569
0.0635
0.0601
0.2056
0.1616
GB
20.2028
20.4200
0.0295
0.0277
0.1409
0.0891
MLP
60.9703
67.1253
0.0413
0.0397
0.2931
0.1076
(a)
abalone
(b)
coil_2000
(c)
isolet
(d)
webpage
Figure 5
:
Comparison of visual representations of TCE, ECE and ACE for the logistic regression algorithm. (Left) The test-based reliability diagram of TCE. (Middle) The reliability diagram of ECE. (Right) The reliability diagram of ACE. Each row corresponds to a result on the dataset: (a) abalone, (b) coil_2000, (c) isolet, and (d) webpage.
(a)
abalone
(b)
coil_2000
(c)
isolet
(d)
isolet
Figure 6
:
Comparison of visual representations of TCE, ECE and ACE for the logistic regression algorithm. (Left) The test-based reliability diagram of TCE. (Middle) The reliability diagram of ECE. (Right) The reliability diagram of ACE. Each row corresponds to a result on the dataset: (a) abalone, (b) coil_2000, (c) isolet, and (d) webpage.
(a)
AlexNet
(b)
VGG19
(c)
ResNet 18
(d)
ResNet 152
Figure 7
:
Comparison of visual representations of TCE, ECE, and ACE on the ImageNet 1000 dataset. (Left) The test-based reliability diagram of TCE, (Middle) The reliability diagram of ECE (Right) The reliability diagram of ACE. Each row corresponds to a result for the model: (a) AlexNet, (b) VGG19, (c) ResNet 18, and (d) ResNet 152.