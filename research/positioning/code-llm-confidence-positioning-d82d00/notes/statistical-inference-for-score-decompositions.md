---
title: Statistical Inference for Score Decompositions
id: statistical-inference-for-score-decompositions
tags:
- code-llm-confidence-positioning-d82d00
- related
- framing-f
- score-decomposition
- inference
created: '2026-11-09T23:08:40.120368Z'
updated: '2026-11-09T23:27:44.503221Z'
source: https://arxiv.org/html/2603.04275
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:40.119763Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Statistical inference for score decompositions (arXiv 2603.04275, full text
  via HTML, forecast-evaluation econometrics). Decomposes scoring functions into miscalibration,
  discrimination, uncertainty using linear recalibration; yields non-negative finite-sample
  components, asymptotic inference under misspecification, link to Mincer-Zarnowitz
  regression, and tests for equal calibration or discrimination. Applications: survey
  inflation forecasts, volatility and Value-at-Risk. Not about LLMs or code; useful
  for F as a methodological source for decomposition with confidence intervals (MCB/DSC/UNC)
  of Brier-type scores applied to confidence readouts.'
---

Statistical Inference for Score Decompositions
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2603.04275v2 [econ.EM] 15 Sep 2026
Statistical Inference for Score Decompositions
Timo Dimitriadis
†
†
thanks:
Corresponding Author. Faculty of Economics and Business, Goethe University Frankfurt, Campus Westend, Theodor-W.-Adorno-Platz 4, 60629 Frankfurt am Main, Germany, and Heidelberg Institute for Theoretical Studies (HITS),
dimitriadis@econ.uni-frankfurt.de
.
Marius Puke
†
†
thanks:
Institute of Economics, University of Hohenheim, Schloss Hohenheim 1 C, 70593 Stuttgart, Germany,
marius.puke@uni-hohenheim.de
.
September 15, 2026
Abstract
We introduce inference methods for score decompositions, which partition scoring functions for predictive assessment into three interpretable components: miscalibration, discrimination, and uncertainty.
Our estimation and inference relies on a linear recalibration of the forecasts and is applicable to general point forecasts such as means and quantiles due to its validity for non-smooth scoring functions.
This approach ensures non-negative decomposition terms in finite samples, enables asymptotic inference under model misspecification, and establishes a direct connection to the classical Mincer-Zarnowitz regression.
The resulting inference framework facilitates novel tests for equal linearized forecast calibration or discrimination, which yield three key advantages.
They enhance the information content of predictive ability tests by decomposing scores, can improve detection power in scenarios where predictive differences are attributable to specific score components, and formally connect scoring-function-based evaluation to traditional calibration tests, such as financial backtests.
Applications demonstrate the method’s utility.
We find that for survey inflation forecasts, discrimination abilities can differ significantly even when overall predictive ability does not.
In an application to financial risk models, our tests provide deeper insights into the calibration and information content of volatility and Value-at-Risk forecasts.
By disentangling forecast accuracy from backtest performance, the method exposes critical shortcomings in current banking regulation.
Keywords
: Forecast Evaluation, Score Decompositions, Inference, Quantiles, Forecast Calibration, Forecast Discrimination
JEL classification
: C21, C22, C52, C53, C58, G17, E37
1
Introduction
Forecasting—whether of macroeconomic conditions, financial market movements, or other uncertain outcomes—has become an indispensable element of modern economic analysis.
From monetary policy design to investment planning and risk management, economic decisions increasingly rely on the ability to anticipate what lies ahead.
The value of these decisions, however, depends critically on the accuracy and credibility of the underlying forecasts.
Therefore, establishing rigorous standards for evaluating predictions is essential, ensuring that economic forecasts are not only informative but also empirically grounded and verifiable.
Two main concepts have emerged for evaluating a forecast
X
t
X_{t}
of an uncertain future real-valued outcome
Y
t
Y_{t}
.
First, the statistical theory of forecast comparison ranks competing forecasts according to their empirical score (or loss)
(
Savage, 1971
;
Gneiting, 2011
)
.
The appropriate scoring function depends on the forecast target—e.g., whether the aim is to predict the full distribution of
Y
t
Y_{t}
, its mean, or a particular quantile.
For meaningful comparisons, these scoring functions must be
strictly consistent
: the ideal forecast should minimize the expected score, ensuring that lower score values reliably indicate superior predictive performance.
Second, forecasts are evaluated in terms of their alignment with the realized outcomes—a property referred to as
calibration
in statistics
(
Gneiting et al., 2007
;
Gneiting and Resin, 2023
)
,
forecast optimality
,
rationality
or
efficiency
in economics
(
Diebold et al., 1998
;
Elliott et al., 2016
)
, and
backtesting
in finance
(
Basel Committee, 2019a
;
Basel Committee, 2019b
)
.
For example, when forecasting the mean, the average forecast should coincide with the average realized outcome—both unconditionally and conditional on the forecast itself, the latter being referred to as auto-calibration.
In economics, this property is most commonly assessed using the test of
Mincer and Zarnowitz (1969, henceforth MZ)
, which examines whether the forecast
X
t
X_{t}
equals the conditional expectation of
Y
t
Y_{t}
given
X
t
X_{t}
through a linear regression framework.
Extensions to other targets, such as quantiles, follow naturally by replacing the mean regression with the corresponding quantile regression
(
Gaglianone et al., 2011
;
Guler et al., 2017
;
Bayer and Dimitriadis, 2022
)
.
These two evaluation paradigms are known to occasionally produce counterintuitive results, a point illustrated by the following motivational example.
In this paper, we develop asymptotic inference for the components of so-called score decompositions, which provide a transparent link between the two forecast evaluation regimes described above. Beyond delivering a sharper theoretical understanding of the respective strengths and limitations of these approaches, the motivational example underscores their practical relevance by demonstrating how, in applied settings, the two methods can lead to seemingly contradictory conclusions.
1.1
Motivational example
Consider the daily logarithmic returns of the S&P E-mini future as the world’s most actively traded equity index futures contract.
We evaluate one-day ahead forecasts for its variance as well as its
1
%
1\%
-quantile, known as the Value-at-Risk (VaR), between January 1, 2008 and January 1, 2022.
Both forecast types are important tools in banking regulation; see
Basel Committee (2019a, CRE 36.153)
and
Basel Committee (2019b, MAR 32.5 and MAR 99.9 – MAR 99.21)
for volatility and VaR backtesting, respectively.
Section
5.2
provides additional details on this application.
We use the following state of the art forecasting models:
First, the Heterogeneous Auto-Regressive (HAR) model of
Corsi (2009)
uses intraday trading information through the Realized Variance (RV) estimator to forecast the variance through a linear model.
Second, we employ a baseline GARCH model of
Bollerslev (1986)
. For both the HAR and GARCH model, we obtain quantile forecasts through a Gaussianity assumption on the model residuals.
For the case of VaR forecasts, we also consider the basic Historical Simulation (HS) approach, which uses the unconditional quantile of the past 250 trading days as its quantile forecast.
Table 1
:
Mincer and Zarnowitz (1969)
test
p
p
-values, average scores (QLIKE for variance, and check loss for the quantile) and its decomposition terms for variance and VaR forecasts. See Sections
1.1
and
5.2
for details.
Forecast Type
Model
i
i
MZ
p
p
-value
Score
Score Decomposition
𝖲
i
\mathsf{S}_{i}
𝖬𝖢𝖡
i
\mathsf{MCB}_{i}
𝖣𝖲𝖢
i
\mathsf{DSC}_{i}
𝖴𝖭𝖢
\mathsf{UNC}
Variance
HAR
0.001
1.775
0.034
6.732
8.473
8.473
GARCH
0.991
2.522
0.000
5.951
1
%
1\%
-Quantile
HAR
0.003
4.018
0.270
1.831
5.579
5.579
GARCH
0.006
4.089
0.148
1.638
HS
0.321
5.114
0.077
0.543
Table
1
shows that, for both forecast types, the HAR model achieves the lowest average scores. These improvements are statistically significant at the
1
%
1\%
level according to the
Diebold and Mariano (1995, henceforth DM)
test, with the sole exception of the HAR–GARCH comparison for VaR forecasts.
Thus, the HAR forecasts deliver the strongest predictive performance.
At the same time, the MZ test decisively rejects auto-calibration of the HAR forecasts. In contrast, the GARCH variance forecasts yield significantly higher scores, yet auto-calibration cannot be rejected.
A similar pattern emerges for the HS VaR forecasts: they record the largest scores but constitute the only forecasting sequence for which calibration is not rejected.
This example illustrates that superior predictive performance and proper auto-calibration do not necessarily coincide and may diverge sharply. Since both evaluation approaches are widely applied in practice, developing tools to reconcile and interpret these seemingly contradictory conclusions is of central importance.
We shed light on these results by examining the
score decomposition
reported in Table
1
.
Score decompositions have a long tradition in meteorology
(
Murphy, 1973
;
Dawid, 1986
;
Murphy and Winkler, 1987
;
Bröcker, 2009
;
Bentzien and Friederichs, 2014
)
and have recently attracted renewed interest in statistics
(
Dimitriadis et al., 2021
;
Gneiting and Resin, 2023
;
Gneiting et al., 2023
)
, yet they have received comparatively little attention in economics.
In essence, the average score
𝖲
i
\mathsf{S}_{i}
of forecaster
i
i
can be decomposed additively into three non-negative components capturing miscalibration (
𝖬𝖢𝖡
i
\mathsf{MCB}_{i}
), discrimination (
𝖣𝖲𝖢
i
\mathsf{DSC}_{i}
), and uncertainty (
𝖴𝖭𝖢
\mathsf{UNC}
):
𝖲
i
=
𝖬𝖢𝖡
i
−
𝖣𝖲𝖢
i
+
𝖴𝖭𝖢
,
\displaystyle\mathsf{S}_{i}=\mathsf{MCB}_{i}-\mathsf{DSC}_{i}+\mathsf{UNC},
(1)
whose exact specification we explain below around (
11
) and (
13
).
Intuitively, the
𝖬𝖢𝖡
\mathsf{MCB}
component measures the extent of forecast miscalibration by quantifying how much the score improves after recalibrating the forecasts by regressing outcomes on forecasts as in the MZ test.
Likewise, the
𝖣𝖲𝖢
\mathsf{DSC}
component reflects the forecaster’s ability to distinguish (or “discriminate”) between higher and lower outcome realizations by comparing the scores of the linearly recalibrated forecasts with a constant reference forecast.
The remaining
𝖴𝖭𝖢
\mathsf{UNC}
term is forecast-independent and therefore functions as a reference level for the decomposition.
The last columns of Table
1
help reconcile the discrepancies between the score-based and calibration-based assessments. For both forecast types, the HAR model attains the highest (and thus best)
𝖣𝖲𝖢
\mathsf{DSC}
values, which is intuitive given that it incorporates the richest information set through high-frequency returns. However, it also yields the largest (worst)
𝖬𝖢𝖡
\mathsf{MCB}
values, accounting for its rejection in the MZ test.
By contrast, the GARCH model—and even more so the HS model—exhibits weaker discrimination but achieves substantially better calibration.
Yet, despite the clear interpretive value of these decomposition terms, formal inference methods for them are not available, limiting their practical usefulness as reflected in
Elliott and Timmermann (2016, p. 355)
, who point out that “am important limitation of these decompositions is that there are no objective measures for how large or small the terms should be”.
This gap is particularly problematic in settings such as banking regulation under the Basel framework, where calibration-based backtesting plays a central role.
Such procedures risk creating misguided incentives: the best-performing HAR forecasts may be labeled “invalid,” whereas HS forecasts—whose poor discriminatory ability makes them slow to respond to emerging crises—may be deemed acceptable.
These tensions highlight the need for both a deeper understanding of the distinct properties captured by the decomposition and the development of rigorous statistical inference for its components—needs that this paper directly addresses.
1.2
Contributions
In this paper, we propose augmenting scoring-function-based forecast comparisons with the corresponding decomposition terms, as illustrated in Table
1
, and we are the first to develop asymptotic inference for these components.
To estimate the decomposition components in (
1
), we advocate the use of a linear regression—either mean or quantile, depending on the forecast target.
This specification is motivated by several considerations: its stability and resistance to overfitting; its good empirical fit in our applications; its close conceptual connection to the
Mincer and Zarnowitz (1969)
framework; its attractive non-negativity guarantees for the resulting decomposition terms; and, crucially, its tractability for developing valid asymptotic inference procedures under model misspecification.
Recent contributions have suggested nonparametric (isotonic) regression approaches instead
(
Dimitriadis et al., 2021
;
Gneiting and Resin, 2023
;
Arnold et al., 2024
)
. However, their asymptotic properties remain unclear—particularly in time-series settings—and they are prone to overfitting, which can introduce biases that further complicate or even undermine asymptotic inference
(
Roelofs et al., 2022
)
.
We derive the joint asymptotic distribution of the estimated
𝖬𝖢𝖡
\mathsf{MCB}
and
𝖣𝖲𝖢
\mathsf{DSC}
components for competing forecasts allowing for possibly non-smooth scoring functions, thereby enabling new tests of equal miscalibration or equal discrimination for, e.g., mean or quantile forecasts.
These tests extend the classical framework of
Diebold and Mariano (1995)
by incorporating two layers of uncertainty: the sampling variation arising from averaging over time and the additional variation introduced by the (possibly misspecified) linear “recalibration regression” used in constructing the
𝖬𝖢𝖡
\mathsf{MCB}
and
𝖣𝖲𝖢
\mathsf{DSC}
components.
A key complication is that the limiting distribution depends on whether the population values of
𝖬𝖢𝖡
\mathsf{MCB}
or
𝖣𝖲𝖢
\mathsf{DSC}
are zero or strictly positive.
Our testing procedures account for these cases through a
p
p
-value adjustment inspired by a hybrid intersection–union/union–intersection (IU/UI) testing principles
(
Berger, 1997
)
.
Our simulations demonstrate that the proposed tests are valid—though potentially conservative due to the underlying IU/UI principles—under their respective null hypotheses for both mean and quantile forecasting settings.
We also show that the tests exhibit strong power properties.
In particular, we show that the proposed tests can provide increased sensitivity in settings where differences in average scores are driven exclusively by a single component, either
𝖬𝖢𝖡
\mathsf{MCB}
or
𝖣𝖲𝖢
\mathsf{DSC}
.
In such cases, they yield higher rejection frequencies than the classical DM test.
This reflects that our tests isolate a specific aspect of forecast performance—either discrimination or miscalibration—whereas score-based tests aggregate both components into a single, potentially noisier measure.
Our first application compares the predictive performance of two survey forecasts for U.S. inflation—the Survey of Professional Forecasters (SPF) and the Michigan Survey of Consumers. While professional forecasters unsurprisingly attain better average scores than consumers, these differences are typically insignificant
(
Ehm et al., 2016
;
Patton, 2020
)
. In contrast, the score decomposition shows that both groups exhibit similar calibration, whereas our new tests detect a significant difference in discrimination. This finding is consistent with the higher rejection frequencies observed in the corresponding simulation designs. Given that professional forecasters draw on a richer information set, their superior discrimination is a natural consequence.
The second application extends the motivating example of Section
1.1
and clarifies the relationship between scoring-function-based forecast evaluation and backtests for both, variance and VaR forecasts.
Moreover, we disentangle several widely used VaR backtests by characterizing them through the conditioning sets they implicitly impose within the framework of conditional quantile calibration, thereby revealing the precise properties they actually test.
1.3
Literature
Early approaches to score decompositions resembling (
1
) date back to
Sanders (1963)
,
Theil (1966)
, and
Murphy (1973)
, and primarily focus on the squared error in the context of probability forecasts for binary outcomes, which can be interpreted as a mean.
DeGroot and Fienberg (1981)
and
Bröcker (2009)
demonstrated that such decompositions can be derived for any strictly proper scoring rule, including those for full distributional forecasts.
More recently,
Gneiting and Resin (2023)
developed a general framework for score decompositions for scoring functions, extending these concepts to point forecasts.
This line of research has spurred a growing body of both theoretical and applied work; see, for example,
Bentzien and Friederichs (2014)
;
Siegert (2017)
;
Pohle (2020)
;
Fissler et al. (2022)
;
Wüthrich et al. (2025)
;
Brehmer et al. (2024)
.
For a more detailed historical overview of score decompositions, see
Mitchell (2019, Section 1.1)
.
In practice, the score decompositions rely on estimates of recalibrated forecasts, and the choice of recalibration method remains an active area of research. Recently, isotonic regression—which estimates, for example, a conditional mean nonparametrically under a monotonicity constraint—has been widely used for both point and distributional forecasts
(
Dimitriadis et al., 2021
;
Gneiting et al., 2023
;
Dimitriadis et al., 2024b
;
Arnold et al., 2024
;
Allen et al., 2025
)
. A key reason for its popularity is that it satisfies attractive finite-sample non-negativity conditions, which facilitate the interpretation of the decomposition terms; these conditions are generally not satisfied by alternative methods such as binning or kernel regressions
(
Dimitriadis et al., 2021
)
. We show that, under mild conditions, these non-negativity properties are also preserved when recalibration is performed using (possibly misspecified) linear regressions.
As we develop asymptotic inference methods for the estimated decomposition terms on the right-hand side of (
1
), our approach is closely related to statistical tests for predictive performance, which focus on the sampling variability of the left-hand side of (
1
). The seminal contribution of
Diebold and Mariano (1995)
laid the foundation for a large econometric literature on testing for equal forecast performance. Numerous extensions have since been proposed, including methods for model-based forecasts
(
West, 1996
;
Clark and McCracken, 2001
)
, multiple forecast comparisons
(
Hansen, 2005
;
Hansen et al., 2011
)
, conditional predictive ability
(
Giacomini and White, 2006
;
Li et al., 2022
)
, and anytime-valid procedures
(
Henzi and Ziegel, 2022
;
Choe and Ramdas, 2024
)
. For comprehensive surveys of this literature, see, for example,
West (2006)
,
Clark and McCracken (2013)
, and
Diebold (2015)
.
In contrast, the assessment of sampling uncertainty for the right-hand side of (
1
) has received relatively little attention. Existing contributions, such as
Siegert (2014)
and
Gneiting and Resin (2023)
, propose ad-hoc (resampling) methods to quantify the uncertainty for a single forecaster, but they do not provide tools for comparative inference across multiple forecasters.
We address this gap by developing a unified framework for inference on the decomposition components.
VaR backtests are widely used to evaluate the reliability, i.e., the calibration, of risk models via their quantile forecasts.
Classic procedures include the unconditional coverage test of
Kupiec (1995)
, which underlies the traffic-light system of
Basel Committee (1996)
;
Basel Committee (2019b)
, as well as the conditional coverage test of
Christoffersen (1998)
, which additionally assesses the independence of exceedances.
A large body of subsequent work tests slightly differing notions of conditional calibration
(
Berkowitz et al., 2011
;
Gaglianone et al., 2011
;
Berkowitz et al., 2011
;
Hoga and Demetrescu, 2023
;
Fosten et al., 2024
;
Wang et al., 2025
)
; see
He et al. (2022)
for a recent overview.
Our score decompositions—and in particular the application in Section
5.2
—show that well-calibrated forecasts do not necessarily exhibit strong predictive performance.
This underscores the importance of evaluating VaR forecasts through both calibration and discrimination, rather than relying solely on traditional backtesting metrics; also see Section
3.5
.
A growing strand of the macroeconomic literature—including, among many others,
Coibion and Gorodnichenko (2015)
,
Bordalo et al. (2020)
,
Kohlhas and Walther (2021)
,
Angeletos et al. (2021)
,
Broer and Kohlhas (2024)
, and
Farmer et al. (2024)
—examines how forecast errors respond to observable information.
This line of work effectively tests necessary conditions for conditional calibration, asking whether forecast errors are linearly predictable given specific observable information available at the time forecasts are made.
Our methodology suggests a natural refinement of these approaches by additionally assessing forecast discrimination, since calibration captures only one dimension of predictive performance.
This refinement is relevant because forecasts that discriminate well are often found to be miscalibrated, and thus deviate from rational expectations more frequently.
1.4
Plan of the article
Section
2
introduces key concepts of forecast evaluation.
The theory in Section
3
develops asymptotic inference under high-level conditions, which are subsequently verified for mean and quantile forecast.
Section
4
contains simulations and we present two applications in Section
5
.
Section
6
concludes.
In the supplementary material, Appendix
A
contains all proofs and we discuss the relation to further decompositions in Appendix
B
.
Appendix
C
presents technical details for the simulations and Appendix
D
contains additional figures.
We provide replication material at
https://github.com/marius-cp/SDI_replications
for the simulations and applications, which draws on the
SDI
package for the statistical software
R
(
R Core Team, 2026
)
, available at
https://github.com/marius-cp/SDI
.
2
Fundamentals of forecast evaluation
After fixing notation in Section
2.1
, we discuss relative and absolute forecast evaluation in Sections
2.2
and
2.3
.
2.1
Setup and notation
We follow
Gneiting (2011)
and
Hoga and Dimitriadis (2023)
and consider a complete probability space
(
Ω
,
ℱ
,
ℙ
)
(\Omega,\mathcal{F},\mathbb{P})
with a series of stationary random variables
Y
t
:
Ω
→
𝖮
⊆
ℝ
Y_{t}:\Omega\to\mathsf{O}\subseteq\mathbb{R}
,
t
∈
ℕ
t\in\mathbb{N}
, that take values in the interval-valued observation domain
𝖮
\mathsf{O}
.
For some information set (sigma-algebra)
ℱ
t
⊂
ℱ
\mathcal{F}_{t}\subset\mathcal{F}
, where
Y
t
Y_{t}
is in general not
ℱ
t
\mathcal{F}_{t}
-measurable, we denote the conditional distribution of
Y
t
Y_{t}
given
ℱ
t
\mathcal{F}_{t}
by
F
t
∈
𝒫
F_{t}\in\mathcal{P}
for some convex class of distributions
𝒫
\mathcal{P}
taking values in
𝖮
\mathsf{O}
.
1
1
1
Formally, the conditional distributions are random variables
F
t
(
∙
,
ω
)
=
ℙ
(
Y
t
≤
∙
∣
ℱ
t
)
(
ω
)
F_{t}(\bullet,\omega)=\mathbb{P}(Y_{t}\leq\bullet\mid\mathcal{F}_{t})(\omega)
, where we assume that
F
t
​
(
∙
,
ω
)
∈
𝒫
F_{t}(\bullet,\omega)\in\mathcal{P}
for all
ω
∈
Ω
\omega\in\Omega
, for some convex class of distributions
𝒫
\mathcal{P}
taking values in
𝖮
\mathsf{O}
, which contains the Dirac measures
δ
y
\delta_{y}
for all
y
∈
𝖮
y\in\mathsf{O}
.
We write
F
t
​
(
∙
)
F_{t}(\bullet)
for the random variable defined by
ω
↦
F
t
​
(
ω
,
∙
)
\omega\mapsto F_{t}(\omega,\bullet)
.
The information set
ℱ
t
\mathcal{F}_{t}
represents the full information that could be used for forecast
Y
t
Y_{t}
, but competing forecasters might have less information at hand.
We deliberately use the notation
ℱ
t
\mathcal{F}_{t}
(opposed to e.g.,
ℱ
t
−
1
\mathcal{F}_{t-1}
) to allow for both time series (where
t
t
represents time points) as well as cross-sectional (where
t
t
represents cross-sectional units) applications.
For an interval-valued action domain
𝖠
⊆
ℝ
\mathsf{A}\subseteq\mathbb{R}
, we consider a stationary sequence of forecasts for some target functional
Γ
:
𝒫
→
𝖠
\Gamma:\mathcal{P}\to\mathsf{A}
of the conditional distribution
F
t
F_{t}
.
Prominent functionals are the conditional expectation
𝔼
⁡
[
Y
t
∣
ℱ
t
]
\mathbb{E}[Y_{t}\mid\mathcal{F}_{t}]
, or a conditional
α
\alpha
-quantile
Q
α
​
(
Y
t
∣
ℱ
t
)
Q_{\alpha}(Y_{t}\mid\mathcal{F}_{t})
for some
α
∈
(
0
,
1
)
\alpha\in(0,1)
, which is assumed to be unique for simplicity.
We sometimes abuse notation and write
Γ
⁡
(
Y
t
∣
ℱ
t
)
\Gamma(Y_{t}\mid\mathcal{F}_{t})
instead of
Γ
⁡
(
F
t
)
\Gamma({F}_{t})
for a functional of the conditional distribution.
The point forecasts are denoted by
X
i
​
t
X_{it}
where the index
i
=
1
,
2
i=1,2
denotes a pair of competing forecasts.
These forecasts are assumed to be
ℱ
t
\mathcal{F}_{t}
-measurable throughout the article but they are in general based on less information,
ℐ
i
​
t
⊆
ℱ
t
\mathcal{I}_{it}\subseteq\mathcal{F}_{t}
, or might be misspecified through other aspects such as model mispecification or estimation noise.
Throughout, (in)equalities of random variables are meant to hold almost surely (a.s.) unless stated otherwise, and for a vector
𝐳
∈
ℝ
k
\mathbf{z}\in\mathbb{R}^{k}
,
k
∈
ℕ
k\in\mathbb{N}
,
∥
𝐳
∥
\lVert\mathbf{z}\rVert
denotes the Euclidean norm and
𝐳
⊤
\mathbf{z}^{\top}
its transpose.
We write
∇
𝐳
f
\nabla_{\mathbf{z}}f
for the (column-vector) gradient of the mapping
𝐳
↦
f
⁡
(
𝐳
)
∈
ℝ
\mathbf{z}\mapsto f(\mathbf{z})\in\mathbb{R}
and
∇
𝐳𝐳
f
\nabla_{\mathbf{z}\mathbf{z}}f
for its second derivative, the Hessian matrix.
In the univariate case,
f
′
​
(
z
)
f^{\prime}(z)
denotes the derivative of
f
⁡
(
z
)
f(z)
with respect to
z
∈
ℝ
z\in\mathbb{R}
. For functions with multiple
real-valued arguments, a prime indicates partial differentiation with respect to the first argument, and multiple primes denote higher-order derivatives.
2.2
Forecast comparison through scoring functions
Following
Gneiting (2011)
, point forecasts are evaluated using strictly
consistent scoring (or loss) functions
𝖲
:
𝖠
×
𝖮
→
ℝ
\mathsf{S}:\mathsf{A}\times\mathsf{O}\to\mathbb{R}
, where lower values indicate better
predictive performance. A scoring function is
(strictly) consistent
for
a functional
Γ
\Gamma
if the expected score is (uniquely) minimized by the
optimal forecast. A functional is called
elicitable
if it admits a
strictly consistent scoring function.
Holzmann and Eulert (2014, Theorem 1)
extend this
concept to conditional information sets
𝒢
t
⊆
ℱ
t
\mathcal{G}_{t}\subseteq\mathcal{F}_{t}
, yielding
𝔼
⁡
[
𝖲
⁡
(
Γ
⁡
(
Y
t
∣
𝒢
t
)
,
Y
t
)
∣
𝒢
t
]
≤
𝔼
⁡
[
𝖲
⁡
(
X
~
t
,
Y
t
)
∣
𝒢
t
]
,
\displaystyle\mathbb{E}\big[\mathsf{S}\big(\Gamma(Y_{t}\mid\mathcal{G}_{t}),Y_{t}\big)\mid\mathcal{G}_{t}\big]\leq\mathbb{E}\big[\mathsf{S}(\widetilde{X}_{t},Y_{t})\mid\mathcal{G}_{t}\big],
(2)
for every
𝒢
t
\mathcal{G}_{t}
-measurable random variable
X
~
t
\widetilde{X}_{t}
, with
almost sure equality if and only if
X
~
t
=
Γ
⁡
(
Y
t
∣
𝒢
t
)
\widetilde{X}_{t}=\Gamma(Y_{t}\mid\mathcal{G}_{t})
almost surely.
If the target functional
Γ
\Gamma
is the conditional mean, under mild regularity conditions, all strictly consistent scoring functions are characterized by the so-called
Bregman class
,
𝖲
⁡
(
x
,
y
)
=
ϕ
⁡
(
y
)
−
ϕ
⁡
(
x
)
−
ϕ
′
​
(
x
)
​
(
y
−
x
)
\displaystyle\mathsf{S}(x,y)=\phi(y)-\phi(x)-\phi^{\prime}(x)(y-x)
(3)
parametrized by a strictly convex function
ϕ
\phi
with subgradient
ϕ
′
\phi^{\prime}
(
Gneiting, 2011
, Theorem 7)
.
The omnipresent squared error
𝖲
SE
​
(
x
,
y
)
=
(
x
−
y
)
2
.
\displaystyle\mathsf{S}_{\textsf{SE}}(x,y)=(x-y)^{2}.
(4)
arises for
ϕ
SE
​
(
x
)
=
x
2
\phi_{\textsf{SE}}(x)=x^{2}
.
For
ϕ
QL
​
(
x
)
=
−
log
⁡
(
x
)
\phi_{\textsf{QL}}(x)=-\log(x)
we obtain the QLIKE scoring function,
𝖲
QL
​
(
x
,
y
)
=
y
x
−
log
⁡
(
y
x
)
−
1
,
\displaystyle\mathsf{S}_{\textsf{QL}}(x,y)=\frac{y}{x}-\log\left(\frac{y}{x}\right)-1,
(5)
which is regularly used for the evaluation of variance forecasts in financial econometrics with positive action and observation domain,
𝖠
=
𝖮
=
(
0
,
∞
)
\mathsf{A}=\mathsf{O}=(0,\infty)
; see e.g.,
Patton (2011)
.
Under the standard assumption of a zero conditional mean, the variance coincides with the second moment, thereby rendering the Bregman class applicable.
If the target functional is the conditional
α
\alpha
-quantile,
α
∈
(
0
,
1
)
\alpha\in(0,1)
, strictly consistent scoring functions are given by the class of generalized piecewise linear (GPL) loss functions
𝖲
(
x
,
y
)
=
(
𝟙
{
y
≤
x
}
−
α
)
(
g
(
x
)
−
g
(
y
)
)
,
\displaystyle\mathsf{S}(x,y)=(\mathds{1}\{y\leq x\}-\alpha)(g(x)-g(y)),
(6)
where the function
g
g
is strictly increasing on
𝖠
=
𝖮
⊆
ℝ
\mathsf{A}=\mathsf{O}\subseteq\mathbb{R}
(
Gneiting, 2011
, Theorem 9)
.
The GPL loss functions are generally non-differentiable at
x
=
y
x=y
due to the indicator function.
The check loss
𝖲
CL
(
x
,
y
)
=
(
𝟙
{
y
≤
x
}
−
α
)
(
x
−
y
)
\mathsf{S}_{\textsf{CL}}(x,y)=(\mathds{1}\{y\leq x\}-\alpha)(x-y)
as the most popular candidate arises for
g
CL
​
(
x
)
=
x
g_{\textsf{CL}}(x)=x
.
In practice, scoring functions are employed to compare forecast sequences
X
i
​
t
X_{it}
,
i
=
1
,
2
i=1,2
,
t
=
1
,
…
,
T
t=1,\dots,T
, for the target variable
Y
t
Y_{t}
through their
average scores
𝖲
^
i
​
T
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
X
i
​
t
,
Y
t
)
\widehat{\mathsf{S}}_{iT}=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(X_{it},Y_{t})
.
The sample average serves as an empirical approximation to the
expectation appearing in (
2
).
Following
Diebold and Mariano (1995)
, a rich body of asymptotic inference methods is available for constructing tests based on such average score differences.
2.3
Forecast validation and calibration assessment
A known practical limitation of purely score-based forecast evaluations lies in their inability to identify specific deficiencies of the forecasts, such as systematic biases, which we formalize through the theory of forecast calibration.
A forecast
X
i
​
t
X_{it}
for
Γ
⁡
(
Y
t
)
\Gamma(Y_{t})
is said to be
conditionally calibrated
with respect to the information set
𝒢
i
​
t
⊆
ℱ
t
\mathcal{G}_{it}\subseteq\mathcal{F}_{t}
if
X
i
​
t
=
Γ
⁡
(
Y
t
∣
𝒢
i
​
t
)
a.s.
\displaystyle X_{it}=\Gamma(Y_{t}\mid\mathcal{G}_{it})\qquad\text{a.s.}
(7)
This property asserts a certain compatibility of the forecast
X
i
​
t
X_{it}
with its forecasting target
Γ
⁡
(
Y
t
∣
𝒢
i
​
t
)
\Gamma(Y_{t}\mid\mathcal{G}_{it})
.
A conditionally calibrated forecast w.r.t. the full information set
ℱ
t
\mathcal{F}_{t}
minimizes the
ℱ
t
\mathcal{F}_{t}
-conditional expectation of the scoring function by (
2
), such that the econometric literature also calls it
optimal
or
efficient
(
Elliott and Timmermann, 2016
, Chapter 15)
.
As the forecast might not have used—or even have access to—all information in
ℱ
t
\mathcal{F}_{t}
, it is, however, often more appropriate to consider calibration based on some reduced information set
𝒢
i
​
t
⊂
ℱ
t
\mathcal{G}_{it}\subset\mathcal{F}_{t}
in (
7
).
An important special case is that of an
auto-calibrated
forecast, obtained for
𝒢
i
​
t
=
σ
⁡
{
X
i
​
t
}
\mathcal{G}_{it}=\sigma\{X_{it}\}
, i.e.,
X
i
​
t
=
Γ
⁡
(
Y
t
∣
X
i
​
t
)
,
a.s.
\displaystyle X_{it}=\Gamma(Y_{t}\mid X_{it}),\qquad\text{a.s.}
(8)
Conditioning on the forecast itself guarantees that the information encoded in the forecast was indeed used, and it remains feasible even when the evaluator does not have access to the full information set of the forecaster
ℐ
i
​
t
\mathcal{I}_{it}
.
A common tool to assess auto-calibration is to plot
x
∈
𝖠
x\in\mathsf{A}
against an estimate of
Γ
⁡
(
Y
t
∣
X
i
​
t
=
x
)
\Gamma(Y_{t}\mid X_{it}=x)
, where deviations from the diagonal indicate miscalibration.
In the meteorological literature, this is known as a
reliability diagram
, typically estimated nonparametrically
(
Murphy and Winkler, 1992
;
Pohle, 2020
;
Dimitriadis et al., 2021
)
.
In economic mean forecast evaluation, this idea goes back to
Mincer and Zarnowitz (1969)
, who regress
Y
t
Y_{t}
on
X
i
​
t
X_{it}
and test whether the intercept is zero and the slope is one—essentially a linear reliability diagram.
Gaglianone et al. (2011)
;
Guler et al. (2017)
;
Bayer and Dimitriadis (2022)
cover extensions to other functionals.
A useful alternative characterization of calibration is based on
identification functions
, which, under suitable smoothness conditions,
correspond to derivatives of strictly consistent scoring functions
(
Nolde and Ziegel, 2017
)
. An identification function
𝖵
:
𝖠
×
𝖮
→
ℝ
\mathsf{V}:\mathsf{A}\times\mathsf{O}\to\mathbb{R}
is
strict
if
𝔼
Y
∼
F
​
[
𝖵
⁡
(
x
,
Y
)
]
=
0
\mathbb{E}_{Y\sim F}[\mathsf{V}(x,Y)]=0
if and only if
x
=
Γ
⁡
(
F
)
x=\Gamma(F)
. Subject to regularity
conditions, given
𝒢
i
​
t
⊇
σ
⁡
{
X
i
​
t
}
\mathcal{G}_{it}\supseteq\sigma\{X_{it}\}
, conditional calibration in (
7
) is
equivalent to
𝔼
⁡
[
𝖵
⁡
(
X
i
​
t
,
Y
t
)
∣
𝒢
i
​
t
]
=
0
,
a.s.
,
\displaystyle\mathbb{E}\big[\mathsf{V}(X_{it},Y_{t})\mid\mathcal{G}_{it}\big]=0,\qquad\text{a.s.},
(9)
which reduces to auto-calibration when
𝒢
i
​
t
=
σ
⁡
{
X
i
​
t
}
\mathcal{G}_{it}=\sigma\{X_{it}\}
. Taking unconditional expectations in (
9
) yields the notion of
unconditional calibration
,
𝔼
⁡
[
𝖵
⁡
(
X
i
​
t
,
Y
t
)
]
=
0
\mathbb{E}[\mathsf{V}(X_{it},Y_{t})]=0
.
3
Theory
We introduce linear score decompositions in Section
3.1
, develop asymptotic inference in Section
3.2
, discuss testable hypotheses in Section
3.3
, derive low-level inference conditions for mean and quantile forecasts in Section
3.4
, and discuss connections to VaR backtests in Section
3.5
.
3.1
Score decompositions based on linear recalibration
For our score decomposition, let
Γ
\Gamma
be an elicitable functional and
𝖲
\mathsf{S}
a corresponding strictly consistent scoring function. We introduce the
recalibration variables
𝑾
i
​
t
=
(
1
,
X
i
​
t
,
…
)
⊤
∈
ℝ
k
\bm{W}_{it}=(1,X_{it},\dots)^{\top}\in\mathbb{R}^{k}
, which generate the
recalibration information set
𝒲
i
​
t
=
σ
⁡
{
𝑾
i
​
t
}
\mathcal{W}_{it}=\sigma\{\bm{W}_{it}\}
, where
σ
⁡
{
X
i
​
t
}
⊆
𝒲
i
​
t
⊆
ℱ
t
\sigma\{X_{it}\}\subseteq\mathcal{W}_{it}\subseteq\mathcal{F}_{t}
.
The standard specification is
𝑾
i
​
t
=
(
1
,
X
i
​
t
)
\bm{W}_{it}=(1,X_{it})
. More generally,
𝑾
i
​
t
\bm{W}_{it}
may include higher-order transformations of
X
i
​
t
X_{it}
(e.g.,
polynomial terms) as well as additional variables on which conditioning is of
interest. The canonical auto-calibration case, in the sense of
Mincer and Zarnowitz (1969)
, corresponds to
𝒲
i
​
t
=
σ
⁡
{
X
i
​
t
}
\mathcal{W}_{it}=\sigma\{X_{it}\}
.
Enlarging the information set
𝒲
i
​
t
\mathcal{W}_{it}
naturally accommodates
stronger notions of calibration and establishes connections to VaR backtesting
and related macroeconomic applications
(
Coibion and Gorodnichenko, 2015
)
.
We impose the following standard assumption in the field of misspecified regressions
(
White, 1980
;
Kim and White, 2003
;
Komunjer, 2005
;
Angrist et al., 2006
)
.
Assumption 3.1
.
𝖲
\mathsf{S}
is a strictly consistent scoring function for the functional
Γ
\Gamma
, the random variables
Y
t
Y_{t}
,
X
i
​
t
X_{it}
and
𝐖
i
​
t
\bm{W}_{it}
are strictly stationary for all
t
∈
ℕ
t\in\mathbb{N}
, and the pseudo-true parameter
𝜽
¯
i
=
arg
⁡
min
𝜽
∈
𝚯
​
𝔼
​
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\displaystyle\bar{\bm{\theta}}_{i}=\underset{\bm{\theta}\in\bm{\Theta}}{\arg\min}\;\mathbb{E}\left[\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big)\right]
(10)
is unique and in the interior of
𝚯
⊆
ℝ
k
\bm{\Theta}\subseteq\mathbb{R}^{k}
, where
𝚯
\bm{\Theta}
is convex and compact, the points
(
0
,
1
,
0
,
…
)
⊤
(0,1,0,\dots)^{\top}
and
(
Γ
⁡
(
Y
t
)
,
0
,
…
)
⊤
(\Gamma(Y_{t}),0,\dots)^{\top}
are in the interior of
𝚯
\bm{\Theta}
, and
𝐖
i
​
t
⊤
​
𝛉
∈
𝖠
\bm{W}_{it}^{\top}\bm{\theta}\in\mathsf{A}
for all
𝛉
∈
𝚯
\bm{\theta}\in\bm{\Theta}
.
Besides stationarity and some technicalities on
𝚯
\bm{\Theta}
, Assumption
3.1
crucially imposes the existence of a unique pseudo-true parameter
𝜽
¯
i
\bar{\bm{\theta}}_{i}
for the linearly
reCalibrated forecast
X
i
​
t
𝖢
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
X_{it}^{\mathsf{C}}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
, which we later estimate through linear (e.g., mean or quantile) regression.
The forecast
X
i
​
t
𝖢
X_{it}^{\mathsf{C}}
is a recalibrated version of the original forecast that exploits the information contained in the original forecast.
Under correct specification of the linear recalibration,
X
i
​
t
𝖢
=
Γ
⁡
(
Y
t
∣
𝑾
i
​
t
)
X_{it}^{\mathsf{C}}=\Gamma(Y_{t}\mid\bm{W}_{it})
is
𝒲
i
​
t
\mathcal{W}_{it}
-conditional calibrated by definition; see (
7
).
Under model misspecification,
X
i
​
t
𝖢
X_{it}^{\mathsf{C}}
satisfies the interpretation of a
linearly
recalibrated forecast in the sense of a best linear predictor for
Γ
⁡
(
Y
t
∣
𝑾
i
​
t
)
\Gamma(Y_{t}\mid\bm{W}_{it})
.
Notice that the linear model is motivated by the benchmark case of calibrated forecasts, for which the linear model is correctly specified
(
Mincer and Zarnowitz, 1969
)
; throughout, however, we allow for possible misspecification.
We denote the expected score of the original forecasts
X
i
​
t
X_{it}
by
𝖲
¯
i
:=
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
,
Y
t
)
]
\overline{\mathsf{S}}_{i}:=\mathbb{E}\big[\mathsf{S}(X_{it},Y_{t})\big]
.
Based on the linearly recalibrated forecast
X
i
​
t
𝖢
X_{it}^{\mathsf{C}}
, the corresponding linearly
reCalibrated score
is denoted by
𝖲
¯
i
𝖢
=
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
𝖢
,
Y
t
)
]
\overline{\mathsf{S}}_{i}^{\mathsf{C}}=\mathbb{E}\big[\mathsf{S}(X_{it}^{\mathsf{C}},Y_{t})\big]
.
We further define the
Reference
forecast
r
¯
=
Γ
⁡
(
Y
t
)
\bar{r}=\Gamma(Y_{t})
, which is unconditionally calibrated but constant, and the corresponding
Reference score
𝖲
¯
𝖱
=
𝔼
⁡
[
𝖲
⁡
(
r
¯
,
Y
t
)
]
\overline{\mathsf{S}}^{\mathsf{R}}=\mathbb{E}\big[\mathsf{S}(\bar{r},Y_{t})\big]
.
With these ingredients, the (linearized)
population
score decomposition (with non-negative components) is given by
𝖲
¯
i
\displaystyle\overline{\mathsf{S}}_{i}
=
(
𝖲
¯
i
−
𝖲
¯
i
𝖢
)
⏟
𝖬𝖢𝖡
¯
i
−
(
𝖲
¯
𝖱
−
𝖲
¯
i
𝖢
)
⏟
𝖣𝖲𝖢
¯
i
+
𝖲
¯
𝖱
⏟
𝖴𝖭𝖢
¯
,
\displaystyle=\underbrace{\big(\overline{\mathsf{S}}_{i}-\overline{\mathsf{S}}_{i}^{\mathsf{C}}\big)}_{\overline{\mathsf{MCB}}_{i}}-\underbrace{\big(\overline{\mathsf{S}}^{\mathsf{R}}-\overline{\mathsf{S}}_{i}^{\mathsf{C}}\big)}_{\overline{\mathsf{DSC}}_{i}}+\underbrace{\overline{\mathsf{S}}^{\mathsf{R}}}_{\overline{\mathsf{UNC}}},
(11)
whose intuition we explain in the following.
In the canonical case
𝑾
i
​
t
=
(
1
,
X
i
​
t
)
\bm{W}_{it}=(1,X_{it})
and under correct specification of the linear model, the component
𝖬𝖢𝖡
¯
i
=
𝖲
¯
i
−
𝖲
¯
i
𝖢
\overline{\mathsf{MCB}}_{i}=\overline{\mathsf{S}}_{i}-\overline{\mathsf{S}}_{i}^{\mathsf{C}}
quantifies the increase in the score’s predictive ability that can be achieved by recalibration, hence providing a measure of miscalibration such that low
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
values are desirable.
As the recalibrated forecast is a measurable transformation of
X
i
​
t
X_{it}
, it incorporates no additional information; thus, any score gains stem purely from improved calibration.
If
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
, recalibration yields no score improvement, indicating that the original forecast was already calibrated.
The component
𝖣𝖲𝖢
¯
i
=
𝖲
¯
𝖱
−
𝖲
¯
i
𝖢
\overline{\mathsf{DSC}}_{i}=\overline{\mathsf{S}}^{\mathsf{R}}-\overline{\mathsf{S}}_{i}^{\mathsf{C}}
compares the scores of two recalibrated forecasts:
𝖲
¯
i
𝖢
\overline{\mathsf{S}}_{i}^{\mathsf{C}}
based on information in
X
i
​
t
X_{it}
, and
𝖲
¯
𝖱
\overline{\mathsf{S}}^{\mathsf{R}}
unconditionally without additional information.
As this “controls for calibration”, the remaining score improvement in
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
reflects the forecast’s information content, that is, its discrimination ability.
Larger values are therefore desirable.
The final component
𝖴𝖭𝖢
¯
=
𝖲
¯
𝖱
\overline{\mathsf{UNC}}=\overline{\mathsf{S}}^{\mathsf{R}}
is forecast-independent and serves as a normalizing constant.
In case of a misspecified linear recalibration model, the population score decomposition in (
11
) can be understood as a “linearized” version, similar to the “isotonized” score decomposition of
Allen et al. (2025)
.
In the misspecified case,
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
quantifies the increase in the score’s predictive ability that can be achieved by
linear
recalibration.
As linearity holds under the desirable case of auto-calibration where
X
i
​
t
𝖢
=
Γ
⁡
(
Y
t
∣
𝑾
i
​
t
)
=
(
1
,
X
i
​
t
)
​
𝜽
¯
i
X_{it}^{\mathsf{C}}=\Gamma(Y_{t}\mid\bm{W}_{it})=(1,X_{it})\bar{\bm{\theta}}_{i}
, we do not expect substantial departures from linearity for reasonably well-specified forecasts.
Indeed, in our empirical applications we find no evidence against the linear specification; the corresponding diagnostic results are reported in Appendix
D
.
Otherwise, non-linear recalibration could be captured in our framework by including higher powers of
X
i
​
t
X_{it}
in
𝑾
i
​
t
\bm{W}_{it}
.
In practice, the components in (
11
) require estimated versions of both the recalibrated and reference forecasts.
While estimating the reference forecast as the unconditional functional is straightforward, the estimation of the recalibrated forecast remains debated, with proposals including binning methods
(
Murphy and Winkler, 1987
)
, kernel regression
(
Pohle, 2020
)
, and isotonic regressions
(
Dimitriadis et al., 2021
;
Gneiting and Resin, 2023
)
.
Instead, we propose using linear regression, which mitigates the overfitting bias associated with nonparametric methods that can invalidate inference, particularly in settings close to auto-calibration
(
Roelofs et al., 2022
)
.
Moreover, the linear specification is consistent with
Mincer and Zarnowitz (1969)
and readily accommodates additional covariates beyond the forecasts themselves.
For the finite-sample guarantees of Theorem
3.2
below, it is crucial that we use M-estimation for the regression parameters using the
same
scoring function that is used for the decomposition
2
2
2
While
Dimitriadis et al. (2024a)
show that strictly consistent loss functions (and only these) produce consistent parameter estimates, the resulting estimates generally differ in value across loss functions
(
Elliott et al., 2016
;
Mühlemann, 2021
)
, motivating the need to employ the
same
scoring function in (
11
) and (
12
).
𝜽
^
i
​
T
=
arg
⁡
min
𝜽
∈
𝚯
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
,
\displaystyle\widehat{\bm{\theta}}_{iT}=\underset{\bm{\theta}\in\bm{\Theta}}{\arg\min}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big),
(12)
where we assume for simplicity that the arg min in (
12
) is unique.
Moreover, the empirical reference forecast
r
^
T
\widehat{r}_{T}
is the unconditional functional
Γ
\Gamma
of the sample
Y
1
,
…
,
Y
T
Y_{1},\dots,Y_{T}
.
Then, the
empirical counterpart
of the score decomposition in (
11
) is given by
𝖲
^
i
​
T
=
𝖬𝖢𝖡
^
i
​
T
−
𝖣𝖲𝖢
^
i
​
T
+
𝖴𝖭𝖢
^
T
:=
(
𝖲
^
i
​
T
−
𝖲
^
i
​
T
𝖢
)
−
(
𝖲
^
T
𝖱
−
𝖲
^
i
​
T
𝖢
)
+
𝖲
^
T
𝖱
,
\displaystyle\widehat{\mathsf{S}}_{iT}=\widehat{\mathsf{MCB}}_{iT}-\widehat{\mathsf{DSC}}_{iT}+\widehat{\mathsf{UNC}}_{T}:=\left(\widehat{\mathsf{S}}_{iT}-\widehat{\mathsf{S}}^{\mathsf{C}}_{iT}\right)-\left(\widehat{\mathsf{S}}^{\mathsf{R}}_{T}-\widehat{\mathsf{S}}^{\mathsf{C}}_{iT}\right)+\widehat{\mathsf{S}}^{\mathsf{R}}_{T},
(13)
where
𝖲
^
i
​
T
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
X
i
​
t
,
Y
t
)
,
𝖲
^
i
​
T
𝖢
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
,
𝖲
^
T
𝖱
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
^
T
,
Y
t
)
.
\displaystyle\widehat{\mathsf{S}}_{iT}=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(X_{it},Y_{t}),\qquad\widehat{\mathsf{S}}^{\mathsf{C}}_{iT}=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t}),\qquad\widehat{\mathsf{S}}^{\mathsf{R}}_{T}=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\widehat{r}_{T},Y_{t}).
The following theorem ensures (strict) positivity of the sampling versions of the decomposition in (
13
).
Theorem 3.2
.
Assume that the recalibrated forecasts are obtained by (
12
) using the same strictly consistent score
𝖲
\mathsf{S}
as used in (
13
).
Furthermore, let
𝐖
i
​
t
\bm{W}_{it}
contain a constant and the forecast
X
i
​
t
X_{it}
, and let
(
r
^
T
,
0
,
…
)
⊤
∈
𝚯
(\widehat{r}_{T},0,\dots)^{\top}\in\bm{\Theta}
almost surely.
Then, for the decomposition in (
13
), it holds that:
(a)
𝖬𝖢𝖡
^
i
​
T
≥
0
\widehat{\mathsf{MCB}}_{iT}\geq 0
, which holds with equality if
X
i
​
t
=
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
X_{it}=\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}
a.s. for all
t
=
1
,
…
,
T
t=1,\dots,T
.
(b)
If the
arg
⁡
min
\arg\,\min
in (
12
) is unique, then
𝖬𝖢𝖡
^
i
​
T
=
0
\widehat{\mathsf{MCB}}_{iT}=0
a.s. implies
X
i
​
t
=
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
X_{it}=\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}
a.s. for all
t
=
1
,
…
,
T
t=1,\dots,T
.
(c)
𝖣𝖲𝖢
^
i
​
T
≥
0
\widehat{\mathsf{DSC}}_{iT}\geq 0
, which holds with equality if
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
=
r
^
T
\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}=\widehat{r}_{T}
a.s. for all
t
=
1
,
…
,
T
t=1,\dots,T
.
(d)
If the
arg
⁡
min
\arg\,\min
in (
12
) and
r
^
T
\widehat{r}_{T}
are unique, then
𝖣𝖲𝖢
^
i
​
T
=
0
\widehat{\mathsf{DSC}}_{iT}=0
a.s. implies
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
=
r
^
T
\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}=\widehat{r}_{T}
a.s. for all
t
=
1
,
…
,
T
t=1,\dots,T
.
The non-negativity guarantees of Theorem
3.2
are essential, as zero miscalibration and discrimination components are routinely interpreted as perfect (linear) calibration and no (linear) discrimination, respectively
(
Dimitriadis et al., 2021
;
Gneiting and Resin, 2023
;
Allen et al., 2025
)
.
The proof of Theorem
3.2
applies to any recalibration method estimated by global score minimization and which is flexible enough to nest both a constant and the identity line, such as isotonic regression
(
Dimitriadis et al., 2021
;
Gneiting and Resin, 2023
)
.
In contrast, kernel regressions
(
Pohle, 2020
)
, logistic regressions and Beta-CDF models for binary events
(
Siegert, 2017
;
Ranjan and Gneiting, 2010
)
do not offer such guarantees.
Although kernels can represent constants and the identity line, they are not fitted via global score minimization; Beta-CDFs, being strictly increasing, cannot produce constants; and logistic regressions generally cannot reproduce the identity line.
3.2
Asymptotic approximations
We now provide new distributional convergence results for the considered linear score decomposition, which are derived under the following high-level regularity conditions, for which we derive more explicit conditions for mean and quantile forecasts in Section
3.4
.
Assumption 3.3
.
The following conditions hold for
i
=
1
,
2
i=1,2
:
(i)
The parametric estimators are of rate
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
=
𝒪
ℙ
​
(
1
)
\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)=\mathcal{O}_{\mathbb{P}}(1)
and
T
​
(
r
^
T
−
r
¯
)
=
𝒪
ℙ
​
(
1
)
\sqrt{T}\big(\widehat{r}_{T}-\bar{r}\big)=\mathcal{O}_{\mathbb{P}}(1)
.
(ii)
The following central limit theorem (CLT) holds,
T
−
1
/
2
𝛀
T
−
1
/
2
∑
t
=
1
T
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
⟶
d
𝒩
(
0
,
I
5
)
,
\displaystyle T^{-1/2}\bm{\Omega}_{T}^{-1/2}\sum_{t=1}^{T}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,I_{5}),
where
a
i
​
t
:=
𝖲
⁡
(
X
i
​
t
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
,
Y
t
)
]
a_{it}:=\mathsf{S}(X_{it},Y_{t})-\mathbb{E}[\mathsf{S}(X_{it},Y_{t})]
,
c
i
​
t
:=
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
c_{it}:=\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})-\mathbb{E}[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})]
,
e
t
:=
𝖲
⁡
(
r
¯
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
r
¯
,
Y
t
)
]
e_{t}:=\mathsf{S}(\bar{r},Y_{t})-\mathbb{E}[\mathsf{S}(\bar{r},Y_{t})]
and where
𝛀
T
=
Var
(
T
−
1
/
2
∑
t
=
1
T
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
)
.
\displaystyle\bm{\Omega}_{T}=\operatorname{Var}\left(T^{-1/2}\sum_{t=1}^{T}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right).
(14)
(iii)
The expected score
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big]
is continuously differentiable in
𝜽
\bm{\theta}
for all
𝜽
∈
int
⁡
(
𝚯
)
\bm{\theta}\in\operatorname{int}(\bm{\Theta})
.
(iv)
The empirical process
ν
i
​
T
(
𝜽
)
:=
T
−
1
/
2
∑
t
=
1
T
(
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
−
𝔼
[
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
]
)
\displaystyle\nu_{iT}(\bm{\theta}):=T^{-1/2}\sum_{t=1}^{T}\Big(\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})-\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big]\Big)
(15)
is stochastically equicontinuous, i.e., for all
ε
>
0
\varepsilon>0
and
η
>
0
\eta>0
, there exists
δ
>
0
\delta>0
such that
lim
sup
T
→
∞
ℙ
(
sup
{
𝜽
,
𝝉
∈
𝚯
:
∥
𝜽
−
𝝉
∥
≤
δ
}
|
ν
i
​
T
(
𝜽
)
−
ν
i
​
T
(
𝝉
)
|
≥
η
)
<
ε
.
\displaystyle\underset{T\to\infty}{\lim\sup}\;\mathbb{P}\left(\sup_{\{\bm{\theta},\bm{\tau}\in\bm{\Theta}:\,\|\bm{\theta}-\bm{\tau}\|\leq\delta\}}\big|\nu_{iT}(\bm{\theta})-\nu_{iT}(\bm{\tau})\big|\geq\eta\right)<\varepsilon.
(16)
Assumption
3.3
provides high-level conditions on the scoring function and the parametric estimators. These conditions can accommodate a wide range of settings, including various estimation methods, target functionals, and forms of temporal dependence. They are verified for the mean and quantile cases in Section
3.4
below, and their generality allows for straightforward extensions to other functionals.
In a nutshell, conditions
(i)
and
(ii)
can be verified based on classical dependence and moment conditions on the forecast-realization pairs.
Conditions
(iii)
and
(iv)
ensure applicability to non-smooth scoring functions, such as the check loss, by imposing smoothness on the
expected
score and controlling empirical deviations via stochastic equicontinuity
(
Andrews, 1994
;
van der Vaart and Wellner, 1996
)
.
Theorem 3.4
.
Let Assumptions
3.1
and
3.3
hold and assume that
𝖬𝖢𝖡
¯
i
,
𝖣𝖲𝖢
¯
i
>
0
\overline{\mathsf{MCB}}_{i},\overline{\mathsf{DSC}}_{i}>0
for
i
=
1
,
2
i=1,2
.
Then, as
T
→
∞
T\rightarrow\infty
,
T
(
𝚵
𝛀
T
𝚵
⊤
)
−
1
/
2
(
𝖬𝖢𝖡
^
1
​
T
−
𝖬𝖢𝖡
¯
1
𝖣𝖲𝖢
^
1
​
T
−
𝖣𝖲𝖢
¯
1
𝖬𝖢𝖡
^
2
​
T
−
𝖬𝖢𝖡
¯
2
𝖣𝖲𝖢
^
2
​
T
−
𝖣𝖲𝖢
¯
2
)
⟶
d
𝒩
(
0
,
I
4
)
,
with
𝚵
=
(
1
−
1
0
0
0
0
−
1
0
0
1
0
0
1
−
1
0
0
0
0
−
1
1
)
.
\displaystyle\sqrt{T}\,\big(\mathbf{\Xi}\mathbf{\Omega}_{T}\mathbf{\Xi}^{\top}\big)^{-1/2}\begin{pmatrix}{\widehat{\mathsf{MCB}}}_{1T}-\overline{\mathsf{MCB}}_{1}\\
{\widehat{\mathsf{DSC}}}_{1T}-\overline{\mathsf{DSC}}_{1}\\
{\widehat{\mathsf{MCB}}}_{2T}-\overline{\mathsf{MCB}}_{2}\\
{\widehat{\mathsf{DSC}}}_{2T}-\overline{\mathsf{DSC}}_{2}\end{pmatrix}\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,I_{4}),\quad\text{with}\quad\mathbf{\Xi}=\begin{pmatrix}1&-1&0&0&0\\
0&-1&0&0&1\\
0&0&1&-1&0\\
0&0&0&-1&1\end{pmatrix}.
The joint asymptotic approximation of Theorem
3.4
is required for the construction of “comparative” confidence intervals and hypothesis tests—for instance, tests for equal miscalibration or discriminatory ability across the two forecast sequences.
Notably, the resulting asymptotic distribution—with covariance matrix
𝛀
T
\bm{\Omega}_{T}
from (
14
)—is unaffected by the estimation uncertainty of
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
and
r
^
T
\widehat{r}_{T}
,
owing to an orthogonality between these estimators and the sampling error arising from replacing expected scores by their empirical counterparts. This robustness is particularly appealing in the presence of potential misspecification of the linear recalibration regression, as it obviates the need to estimate the more complex covariance structure that typically arises under misspecification.
Theorem
3.4
however requires strict positivity of the population values
𝖬𝖢𝖡
¯
i
,
𝖣𝖲𝖢
¯
i
>
0
\overline{\mathsf{MCB}}_{i},\overline{\mathsf{DSC}}_{i}>0
, hence excluding the boundary cases
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
and
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
, which necessitate a separate treatment.
We now derive the asymptotic distribution of
𝖬𝖢𝖡
i
^
T
\widehat{\mathsf{MCB}_{i}}_{T}
and
𝖣𝖲𝖢
i
^
T
\widehat{\mathsf{DSC}_{i}}_{T}
given their population counterparts are zero, which however requires
smooth
scoring functions.
For
non-smooth
scoring functions as for quantile forecasts, we provide an alternative treatment based on MZ-type regressions, which we describe after Theorem
3.6
.
Assumption 3.5
.
Assume that the following conditions hold for
i
=
1
,
2
i=1,2
:
(i)
If
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
, the estimator
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
satisfies the asymptotic expansion
T
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
=
−
(
1
T
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
−
1
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
,
\displaystyle\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)=-\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1),
(17)
where
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}
satisfies a CLT
and
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}
is invertible for
T
T
large enough and satisfies a law of large numbers (LLN).
Furthermore, if
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
(such that
r
¯
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
\bar{r}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
), the estimators
r
^
T
\widehat{r}_{T}
and
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
satisfy
T
(
r
^
T
−
r
¯
𝜽
^
i
​
T
−
𝜽
¯
i
)
=
−
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
,
𝟎
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
)
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
+
o
ℙ
(
1
)
,
\displaystyle\sqrt{T}\begin{pmatrix}\widehat{r}_{T}-\bar{r}\\
\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\end{pmatrix}=-\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1},&\mathbf{0}\\
\lx@intercol\hfil\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}\hfil\lx@intercol\end{pmatrix}T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}+o_{\mathbb{P}}(1),
(18)
where
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}
satisfies a CLT
and the terms
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})
and
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}
are invertible for
T
T
large enough and satisfy LLNs.
(ii)
The scoring function
𝖲
\mathsf{S}
is three times continuously differentiable in its first argument and for
h
T
​
(
𝜽
)
:=
1
T
​
∑
t
=
1
T
|
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
​
‖
𝑾
i
​
t
‖
3
h_{T}(\bm{\theta}):=\frac{1}{T}\sum_{t=1}^{T}\big|\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big|\|\bm{W}_{it}\|^{3}
, we have that
T
−
1
/
2
sup
‖
𝜽
−
𝜽
¯
i
‖
≤
δ
|
h
T
(
𝜽
)
−
h
T
(
𝜽
¯
i
)
|
=
o
ℙ
(
1
)
and
T
−
1
/
2
h
T
(
𝜽
¯
i
)
=
o
ℙ
(
1
)
.
\displaystyle T^{-1/2}\sup_{\|\bm{\theta}-\bar{\bm{\theta}}_{i}\|\leq\delta}\big|h_{T}(\bm{\theta})-h_{T}(\bar{\bm{\theta}}_{i})\big|=o_{\mathbb{P}}(1)\qquad\text{and}\qquad T^{-1/2}h_{T}(\bar{\bm{\theta}}_{i})=o_{\mathbb{P}}(1).
As before, the high-level conditions in Assumption
3.5
allow for case-by-case verifications for specific functionals, scoring functions, and estimators as exemplified in Section
3.4
.
Condition
(i)
provides misspecification-robust asymptotic linear representations of the estimators, slightly strengthening Assumption
3.3
(i)
.
While auto-calibration (
8
) implies (linearized)
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
, the reverse is not true as there might exist a non-linear recalibration function that improves the score.
This necessitates a misspecification-robust formulation of the terms in (
17
)–(
18
).
Condition
(ii)
applies to smooth loss functions and imposes a uniform LLN type requirement, although this condition is substantially weakened by the
T
−
1
/
2
T^{-1/2}
scaling factor.
Theorem 3.6
.
Suppose that Assumptions
3.1
and
3.5
hold.
Then, as
T
→
∞
T\rightarrow\infty
,
•
if
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
, then
T
​
𝖬𝖢𝖡
i
^
T
⟶
d
1
2
​
𝑵
i
⊤
​
𝚼
i
−
1
​
𝑵
i
T\,\widehat{\mathsf{MCB}_{i}}_{T}\stackrel{{\scriptstyle d}}{{\longrightarrow}}\frac{1}{2}\bm{N}_{i}^{\top}\bm{\Upsilon}_{i}^{-1}\bm{N}_{i}
; and
•
if
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
, then
T
​
𝖣𝖲𝖢
^
i
​
T
⟶
d
1
2
​
𝑵
i
⊤
​
𝑯
i
−
1
​
𝑵
i
T\,\widehat{\mathsf{DSC}}_{iT}\stackrel{{\scriptstyle d}}{{\longrightarrow}}\frac{1}{2}\bm{N}_{i}^{\top}\bm{H}_{i}^{-1}\bm{N}_{i}
,
where
𝚼
i
:=
𝔼
⁡
[
𝖲
′′
​
(
𝐖
i
​
t
⊤
​
𝛉
¯
i
,
Y
t
)
​
𝐖
i
​
t
​
𝐖
i
​
t
⊤
]
\bm{\Upsilon}_{i}:=\mathbb{E}\left[\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right]
,
𝐇
i
−
1
:=
(
𝔼
​
[
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝐖
i
​
t
​
𝐖
i
​
t
⊤
]
−
1
−
(
𝔼
​
[
𝖲
′′
​
(
r
¯
,
Y
t
)
]
−
1
0
0
0
)
)
\bm{H}^{-1}_{i}:=\left(\mathbb{E}\big[\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\big]^{-1}-\begin{pmatrix}\mathbb{E}[\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})]^{-1}&0\\
0&0\end{pmatrix}\right)
,
and
𝐍
i
∼
𝒩
⁡
(
0
,
𝚷
i
)
\bm{N}_{i}\sim\mathcal{N}(0,\bm{\Pi}_{i})
with
𝚷
i
:=
lim
T
→
∞
Var
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝐖
i
​
t
⊤
𝛉
¯
i
,
Y
t
)
𝐖
i
​
t
)
\bm{\Pi}_{i}:=\lim_{T\to\infty}\operatorname{Var}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)
.
Theorem
3.6
shows for
smooth
scoring functions that when the population quantities
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
or
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
attain their boundary value of zero, the non-negative test statistics
T
​
𝖬𝖢𝖡
^
i
​
T
T\,\widehat{\mathsf{MCB}}_{iT}
and
T
​
𝖣𝖲𝖢
^
i
​
T
T\,\widehat{\mathsf{DSC}}_{iT}
(see Theorem
3.2
) converge to generalized
χ
2
\chi^{2}
-distributions.
We treat the boundary cases differently for
non-smooth
scoring functions, such as those used for quantile forecasts.
As the proof of Theorem
3.6
illustrates that
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
implies
X
i
​
t
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
X_{it}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
, i.e.,
𝜽
i
=
(
0
,
1
,
0
,
…
)
⊤
\bm{\theta}_{i}=(0,1,0,\dots)^{\top}
, we test the case
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
through the quantile-specific MZ-type test of
Gaglianone et al. (2011)
using misspecification-robust covariance estimation.
We adapt this test to the case
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
(which implies
r
¯
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
\bar{r}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
, i.e.,
𝜽
i
=
(
r
¯
,
0
,
0
,
…
)
⊤
\bm{\theta}_{i}=(\bar{r},0,0,\dots)^{\top}
) by testing whether all slope coefficients in the MZ regression are equal to zero. We pursue this alternative approach as extending Theorem
3.6
to
non-smooth
scoring functions via the proof strategy of Theorem
3.4
would necessitate establishing stochastic equicontinuity of
T
​
ν
i
​
T
​
(
𝜽
)
=
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\sqrt{T}\,\nu_{iT}(\bm{\theta})=\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})-\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big]
.
To the best of our knowledge, no established method exists to derive stochastic equicontinuity of the
T
\sqrt{T}
-scaled version of
ν
i
​
T
​
(
𝜽
)
\nu_{iT}(\bm{\theta})
in this setting.
Recall that the asymptotic variance in the Gaussian case of Theorem
3.4
is unaffected by the estimation error in
r
^
T
\widehat{r}_{T}
and
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
; it depends solely on the sampling uncertainty from approximating expected scores by empirical averages, as captured by
𝛀
T
\bm{\Omega}_{T}
in (
14
).
In contrast, the limiting distributions in Theorem
3.6
depend exclusively on the estimation effects, as summarized by
𝚼
i
\bm{\Upsilon}_{i}
,
𝑯
i
\bm{H}_{i}
, and
𝚷
i
\bm{\Pi}_{i}
, which correspond to the population counterparts of the asymptotic expansion in (
18
).
Technically, this distinction arises because the asymptotic distribution in Theorem
3.4
is driven by
first-order
Taylor expansion terms, whereas the distributions in Theorem
3.6
are governed by
second-order
terms; see the proofs for details.
Feasible inference requires consistent estimators of the misspecification-robust population matrices
𝛀
T
\bm{\Omega}_{T}
,
𝚷
i
\bm{\Pi}_{i}
,
𝚼
i
−
1
\bm{\Upsilon}_{i}^{-1}
, and
𝑯
i
−
1
\bm{H}_{i}^{-1}
so that the asymptotic results in Theorems
3.4
and
3.6
remain valid when replacing population quantities by their estimates.
While
𝚼
i
−
1
\bm{\Upsilon}_{i}^{-1}
and
𝑯
i
−
1
\bm{H}^{-1}_{i}
admit consistent estimation via sample averages, we use HAC estimators for the long-run covariance matrices
𝛀
T
\bm{\Omega}_{T}
and
𝚷
i
\bm{\Pi}_{i}
to accommodate serial dependence
(
Newey and West, 1987
;
Andrews, 1991
)
.
Consistency follows by standard arguments, see e.g.,
White (2001, Chapter 6.4)
for smooth and
Galvao and Yoon (2024)
for non-smooth scoring functions.
3.3
Testable hypotheses
For “one-sample” hypotheses of the form
𝖬𝖢𝖡
¯
i
=
c
\overline{\mathsf{MCB}}_{i}=c
or
𝖣𝖲𝖢
¯
i
=
c
\overline{\mathsf{DSC}}_{i}=c
for some
c
≥
0
c\geq 0
, the appropriate asymptotic distribution—Gaussian or generalized
χ
2
\chi^{2}
—can be selected directly based on the value of
c
c
.
Under “two-sample” hypotheses such as
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}
or
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
, however, the
population
values
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
may be either zero or strictly positive, so it is
a priori
unclear whether the Gaussian or the generalized
χ
2
\chi^{2}
approximation applies.
A valid testing procedure must therefore remain robust to both possibilities. We achieve this by employing a hybrid of intersection–union and union–intersection testing principles
(
Berger, 1997
)
.
For example, consider the hypothesis
ℋ
𝖬𝖢𝖡
:
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
\mathcal{H}_{\mathsf{MCB}}:\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}
, which we can rewrite as
ℋ
𝖬𝖢𝖡
\displaystyle\mathcal{H}_{\mathsf{MCB}}
=
{
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
}
\displaystyle=\left\{\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}\right\}
=
{
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
>
0
}
∪
{
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
=
0
}
\displaystyle=\left\{\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}>0\right\}\cup\left\{\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}=0\right\}
=
{
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
>
0
}
∪
(
{
𝖬𝖢𝖡
¯
1
=
0
}
∩
{
𝖬𝖢𝖡
¯
2
=
0
}
)
\displaystyle=\left\{\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}>0\right\}\cup\left(\left\{\overline{\mathsf{MCB}}_{1}=0\right\}\cap\left\{\overline{\mathsf{MCB}}_{2}=0\right\}\right)
=
:
ℋ
𝖬𝖢𝖡
+
∪
(
ℋ
𝖬𝖢𝖡
1
0
∩
ℋ
𝖬𝖢𝖡
2
0
)
.
\displaystyle=:\mathcal{H}^{+}_{\mathsf{MCB}}\cup\big(\mathcal{H}^{0}_{{\mathsf{MCB}}_{1}}\cap\mathcal{H}^{0}_{{\mathsf{MCB}}_{2}}\big).
(19)
For the hypothesis
ℋ
𝖬𝖢𝖡
+
\mathcal{H}^{+}_{\mathsf{MCB}}
, we employ the
selection vector
𝝎
=
(
1
,
0
,
−
1
,
0
)
⊤
\bm{\omega}=(1,0,-1,0)^{\top}
such that Theorem
3.4
yields
(
𝝎
⊤
𝚵
𝛀
T
𝚵
⊤
𝝎
)
−
1
/
2
T
(
(
𝖬𝖢𝖡
^
1
​
T
−
𝖬𝖢𝖡
^
2
​
T
)
−
(
𝖬𝖢𝖡
¯
1
−
𝖬𝖢𝖡
¯
2
)
)
⟶
d
𝒩
(
0
,
1
)
,
\displaystyle\left(\bm{\omega}^{\top}\mathbf{\Xi}\mathbf{\Omega}_{T}\mathbf{\Xi}^{\top}\bm{\omega}\right)^{-1/2}\sqrt{T}\left(\big(\widehat{\mathsf{MCB}}_{1T}-\widehat{\mathsf{MCB}}_{2T}\big)-\big(\overline{\mathsf{MCB}}_{1}-\overline{\mathsf{MCB}}_{2}\big)\right)\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,1),
(20)
which immediately gives an asymptotically valid
p
p
-value called
p
𝖬𝖢𝖡
+
p^{+}_{\mathsf{MCB}}
.
We propose tests for the hypothesis
ℋ
𝖬𝖢𝖡
i
0
\mathcal{H}^{0}_{{\mathsf{MCB}}_{i}}
for both smooth and non-smooth scoring functions.
In the smooth case, we use the test statistic
T
​
𝖬𝖢𝖡
^
i
​
T
T\,\widehat{\mathsf{MCB}}_{iT}
and the asymptotic approximation from Theorem
3.6
.
For a realized value of
T
​
𝖬𝖢𝖡
^
i
​
T
T\,\widehat{\mathsf{MCB}}_{iT}
, we compute the associated
p
p
-values
p
𝖬𝖢𝖡
i
0
=
ℙ
⁡
(
0.5
​
𝑵
i
⊤
​
𝚼
i
−
1
​
𝑵
i
>
T
​
𝖬𝖢𝖡
^
i
​
T
)
p^{0}_{{\mathsf{MCB}_{i}}}=\mathbb{P}\bigl(0.5\bm{N}_{i}^{\top}\bm{\Upsilon}_{i}^{-1}\bm{N}_{i}>T\,\widehat{\mathsf{MCB}}_{iT}\bigr)
by using the method of
Imhof (1961)
, which uses an inversion formula to express the probability as a definite integral of the characteristic function that is solved via numerical integration by using the
R
package
CompQuadForm
(
Duchesne and Lafaye De Micheaux, 2010
)
.
For non-smooth scoring functions as the GPL score from (
6
), we test the hypothesis
ℋ
𝖬𝖢𝖡
i
0
\mathcal{H}^{0}_{{\mathsf{MCB}}_{i}}
by using the MZ-type “VQR” test of
Gaglianone et al. (2011)
and denote its
p
p
-value by
p
𝖬𝖢𝖡
i
0
p^{0}_{{\mathsf{MCB}_{i}}}
.
Using (
19
), an asymptotically valid
p
p
-value for the combined null hypothesis
ℋ
𝖬𝖢𝖡
\mathcal{H}_{\mathsf{MCB}}
is
p
𝖬𝖢𝖡
:=
min
⁡
(
1
,
max
⁡
(
p
𝖬𝖢𝖡
+
,
2
​
min
⁡
(
p
𝖬𝖢𝖡
1
0
,
p
𝖬𝖢𝖡
2
0
)
)
)
.
\displaystyle p_{\mathsf{MCB}}:=\min\left(1,\max\left(p^{+}_{\mathsf{MCB}},\,2\min\left(p^{0}_{{\mathsf{MCB}_{1}}},p^{0}_{{\mathsf{MCB}_{2}}}\right)\right)\right).
(21)
Similarly, we obtain an asymptotically valid
p
p
-value,
p
𝖣𝖲𝖢
p_{\mathsf{DSC}}
, for testing equal discrimination,
ℋ
𝖣𝖲𝖢
=
{
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
}
=
{
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
>
0
}
∪
(
{
𝖣𝖲𝖢
¯
1
=
0
}
∩
{
𝖣𝖲𝖢
¯
2
=
0
}
)
,
\displaystyle\mathcal{H}_{\mathsf{DSC}}=\left\{\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}\right\}=\left\{\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}>0\right\}\cup\left(\left\{\overline{\mathsf{DSC}}_{1}=0\right\}\cap\left\{\overline{\mathsf{DSC}}_{2}=0\right\}\right),
(22)
by adapting (
19
) and (
21
).
The
p
p
-value from the Gaussian approximation follows from (
20
) by setting
𝝎
=
(
0
,
1
,
0
,
−
1
)
⊤
\bm{\omega}=(0,1,0,-1)^{\top}
, while for smooth scoring functions, the corresponding generalized
χ
2
\chi^{2}
-probability is computed analogously using the method of
Imhof (1961)
.
For non-smooth scoring functions, we test
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
through the MZ-type regression of the VQR test, but by simply testing the hypothesis of zero slopes.
A classical DM test for equal expected scores,
ℋ
𝖲
=
{
𝖲
¯
1
=
𝖲
¯
2
}
\mathcal{H}_{\mathsf{S}}=\left\{\overline{\mathsf{S}}_{1}=\overline{\mathsf{S}}_{2}\right\}
, arises as a special case of Theorem
3.4
for
𝝎
=
(
1
,
−
1
,
−
1
,
1
)
⊤
\bm{\omega}=(1,-1,-1,1)^{\top}
.
Confidence intervals for the individual decomposition terms as well as their differences can be obtained by inverting the above tests.
3.4
Low-level inference conditions for mean and quantile forecasts
We begin with mean forecasts, where
Γ
\Gamma
corresponds to the expectation.
In this case, all strictly consistent scoring functions belong to the Bregman class given in (
3
).
For this class, we verify the high-level Assumptions
3.3
and
3.5
—and hence the validity of Theorems
3.4
and
3.6
—in a general time-series setting with potential model misspecification.
Assumption 3.7
.
The following holds for
i
=
1
,
2
i=1,2
:
(i)
The function
ϕ
⁡
(
z
)
\phi(z)
in (
3
) is five times continuously differentiable with
ϕ
′′
​
(
z
)
>
0
\phi^{\prime\prime}(z)>0
for all
z
∈
𝖠
=
𝖮
z\in\mathsf{A}=\mathsf{O}
.
(ii)
(
Y
t
,
𝑾
1
​
t
⊤
,
𝑾
2
​
t
⊤
)
t
∈
ℕ
(Y_{t},\bm{W}^{\top}_{1t},\bm{W}^{\top}_{2t})_{t\in\mathbb{N}}
is strong mixing of size
−
(
s
−
k
~
)
/
(
k
~
s
)
-(s-\tilde{k})/(\tilde{k}s)
for some
s
>
k
~
>
k
≥
2
s>\tilde{k}>k\geq 2
, and where
k
k
is the dimensionality of
𝚯
\bm{\Theta}
from Assumption
3.1
.
(iii)
The matrix
𝔼
⁡
[
𝑾
i
​
t
​
𝑾
i
​
t
⊤
]
\mathbb{E}\big[\bm{W}_{it}\bm{W}_{it}^{\top}\big]
is positive definite.
(iv)
The Hessian matrix
𝔼
⁡
[
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
+
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
−
Y
t
)
]
\mathbb{E}\left[\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}+\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}-Y_{t})\right]
is invertible and
the matrix
𝐕
T
:=
Var
(
T
−
1
/
2
∑
t
=
1
T
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
𝑾
i
​
t
⊤
𝜽
¯
i
−
Y
t
)
)
\mathbf{V}_{T}:=\operatorname{Var}\left(T^{-1/2}\sum_{t=1}^{T}\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}-Y_{t})\right)
is uniformly positive definite for
T
T
large enough.
(v)
The following moments exist and are finite for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
,
t
∈
ℕ
t\in\mathbb{N}
, and
s
>
2
s>2
from condition
(ii)
:
𝔼
⁡
[
|
ϕ
⁡
(
Y
t
)
|
2
​
s
]
\mathbb{E}\left[\left|\phi(Y_{t})\right|^{2s}\right]
;
𝔼
⁡
[
|
ϕ
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
|
2
​
s
]
\mathbb{E}\left[\left|\phi(\bm{W}_{it}^{\top}\bm{\theta})\right|^{2s}\right]
;
𝔼
⁡
[
|
ϕ
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
)
|
s
]
\mathbb{E}\Big[\left|\phi^{\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\left(Y_{t}-\bm{W}_{it}^{\top}\bm{\theta}\right)\right|^{s}\Big]
;
𝔼
⁡
[
sup
𝜽
∈
𝚯
‖
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
‖
s
]
\mathbb{E}\Big[\sup\limits_{\bm{\theta}\in\bm{\Theta}}\left\|\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\left(Y_{t}-\bm{W}_{it}^{\top}\bm{\theta}\right)\bm{W}_{it}\right\|^{s}\Big]
;
𝔼
⁡
[
sup
𝜽
∈
𝚯
‖
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
‖
]
\mathbb{E}\Big[\sup\limits_{\bm{\theta}\in\bm{\Theta}}\left\|\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right\|\Big]
;
𝔼
⁡
[
sup
𝜽
∈
𝚯
|
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
​
‖
𝑾
i
​
t
‖
3
]
\mathbb{E}\Big[\sup\limits_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\right|\|\bm{W}_{it}\|^{3}\Big]
;
𝔼
⁡
[
sup
𝜽
∈
𝚯
|
ϕ
′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
​
|
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
|
​
‖
𝑾
i
​
t
‖
3
]
\mathbb{E}\Big[\sup\limits_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\right|\left|\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right|\|\bm{W}_{it}\|^{3}\Big]
;
𝔼
⁡
[
sup
𝜽
∈
𝚯
|
ϕ
′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
​
‖
𝑾
i
​
t
‖
4
]
\mathbb{E}\Big[\sup\limits_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\right|\|\bm{W}_{it}\|^{4}\Big]
;
and
𝔼
⁡
[
sup
𝜽
∈
𝚯
|
ϕ
′′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
​
‖
𝑾
i
​
t
‖
4
|
]
\mathbb{E}\Big[\sup\limits_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\left(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right)\|\bm{W}_{it}\|^{4}\right|\Big]
.
Assumption
3.7
resembles standard time series conditions for mean regression.
Item
(i)
is a smoothness and convexity condition on the scoring function.
For the SE scoring function, we often use
𝖠
=
𝖮
=
ℝ
\mathsf{A}=\mathsf{O}=\mathbb{R}
, whereas the QLIKE score requires positive values such as
𝖠
=
𝖮
=
(
0
,
∞
)
\mathsf{A}=\mathsf{O}=(0,\infty)
.
Item
(ii)
is a classical mixing condition that ensures that suitable LLNs, CLTs and stochastic equicontinuity (using
Hansen (1996)
) apply.
Items
(iii)
and
(iv)
are standard in M-estimation
(
Newey and McFadden, 1994
, Chapter 3.1)
.
The invertibility of the Hessian is required for the asymptotic theory under misspecification and is naturally guaranteed for the squared error loss or under correct model specification.
In either case, the latter term involving
ϕ
′′′
\phi^{\prime\prime\prime}
vanishes.
Item
(v)
collects moment conditions, which simplify considerably for the common choices
ϕ
SE
​
(
z
)
=
z
2
\phi_{\textsf{SE}}(z)=z^{2}
and
ϕ
QL
​
(
z
)
=
−
log
⁡
(
z
)
\phi_{\textsf{QL}}(z)=-\log(z)
of the SE and QLIKE scores in (
4
) and (
5
).
Assumption 3.8
.
The matrix
𝛀
T
\bm{\Omega}_{T}
from (
14
) is uniformly positive definite for
T
T
large enough.
Positive definiteness of
𝛀
T
\bm{\Omega}_{T}
is stated in the separate Assumption
3.8
as it is required for the asymptotic normality result in Theorem
3.4
, but is violated in the cases
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
and
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
, and is as such not required for the verification of the conditions of Theorem
3.6
.
The positive definiteness of
𝛀
T
\bm{\Omega}_{T}
essentially imposes non-collinearity conditions for the (sum over time of the) original, recalibrated, and reference scores.
Violations arise, for instance, if the recalibrated score is a constant multiple of the original score for all
t
∈
ℕ
t\in\mathbb{N}
, such as if
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
.
Proposition 3.9
.
Consider a Bregman score from (
3
) for the decomposition, which is also used in (
12
). Then:
•
Assumptions
3.1
,
3.7
, and
3.8
imply Assumption
3.3
such that Theorem
3.4
holds; and
•
Under
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
or
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
,
Assumptions
3.1
,
3.7
and imply Assumption
3.5
such that Theorem
3.6
holds.
We continue with the case where
Γ
\Gamma
is the
α
\alpha
-quantile for some
α
∈
(
0
,
1
)
\alpha\in(0,1)
, where all strictly consistent loss functions are given by the GPL class in (
6
).
For a linear GPL score decomposition, we employ (generalized) quantile regression by combining the estimator (
12
) with the loss in (
6
) and impose the following conditions.
Assumption 3.10
.
The following holds for
i
=
1
,
2
i=1,2
:
(i)
The function
g
g
from (
6
) is twice continuously differentiable with
0
<
g
′
​
(
z
)
≤
C
<
∞
0<g^{\prime}(z)\leq C<\infty
for all
z
∈
𝖠
=
𝖮
z\in\mathsf{A}=\mathsf{O}
.
(ii)
The sequence
(
Y
t
,
𝑾
1
​
t
⊤
,
𝑾
2
​
t
⊤
)
t
∈
ℕ
(Y_{t},\bm{W}^{\top}_{1t},\bm{W}^{\top}_{2t})_{t\in\mathbb{N}}
is strong mixing of size
−
(
s
−
k
~
)
/
(
k
~
s
)
-(s-\tilde{k})/(\tilde{k}s)
for some
s
>
k
~
>
k
≥
2
s>\tilde{k}>k\geq 2
, and where
k
k
is the dimensionality of
𝚯
\bm{\Theta}
from Assumption
3.1
.
(iii)
For all
t
∈
ℕ
t\in\mathbb{N}
,
F
i
​
t
F_{it}
, the conditional distribution of
Y
t
Y_{t}
given
𝒲
i
​
t
\mathcal{W}_{it}
, belongs to a class of distributions that possess a positive and continuous Lebesgue density
f
i
​
t
f_{it}
with
0
<
f
i
​
t
​
(
x
)
≤
K
<
∞
0<f_{it}(x)\leq K<\infty
, uniformly on the support of
F
i
​
t
F_{it}
.
(iv)
The matrix
𝔼
⁡
[
𝑾
i
​
t
​
𝑾
i
​
t
⊤
]
\mathbb{E}\left[\bm{W}_{it}\bm{W}_{it}^{\top}\right]
is positive definite.
(v)
The matrix
𝐕
T
:=
Var
(
T
−
1
/
2
∑
t
=
1
T
g
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
(
𝟙
{
Y
t
≤
𝑾
i
​
t
⊤
𝜽
¯
i
}
−
α
)
𝑾
i
​
t
)
\mathbf{V}_{T}:=\operatorname{Var}\left(T^{-1/2}\sum_{t=1}^{T}g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\big(\mathds{1}\{Y_{t}\leq\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\}-\alpha\big)\bm{W}_{it}\right)
is uniformly positive definite for
T
T
large enough.
(vi)
𝔼
⁡
[
(
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
​
{
g
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
(
F
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
−
α
)
+
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
f
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
}
]
\mathbb{E}\Big[(\bm{W}_{it}\bm{W}_{it}^{\top})\left\{g^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\big(F_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})-\alpha\big)+g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})f_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\right\}\Big]
is invertible.
(vii)
𝔼
​
|
Y
t
|
<
∞
\mathbb{E}|Y_{t}|<\infty
,
𝔼
​
|
g
⁡
(
Y
t
)
|
<
∞
\mathbb{E}|g(Y_{t})|<\infty
,
𝔼
​
‖
𝑾
i
​
t
‖
s
<
∞
\mathbb{E}\big\|\bm{W}_{it}\big\|^{s}<\infty
,
𝔼
​
|
g
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
−
g
⁡
(
Y
t
)
|
s
<
∞
\mathbb{E}\big|g(\bm{W}_{it}^{\top}\bm{\theta})-g(Y_{t})\big|^{s}<\infty
, and
there exist integrable functions
G
G
and
G
′
G^{\prime}
,
G
2
′
G_{2}^{\prime}
,
G
′′
G^{\prime\prime}
such that
‖
𝑾
i
​
t
​
g
​
(
𝑾
i
​
t
⊤
​
𝜽
)
‖
≤
G
⁡
(
𝑾
i
​
t
)
\|\bm{W}_{it}g(\bm{W}_{it}^{\top}\bm{\theta})\|\leq G(\bm{W}_{it})
,
‖
𝑾
i
​
t
​
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
‖
≤
G
′
​
(
𝑾
i
​
t
)
\|\bm{W}_{it}g^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})\|\leq G^{\prime}(\bm{W}_{it})
,
‖
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
‖
≤
G
2
′
​
(
𝑾
i
​
t
)
\|\bm{W}_{it}\bm{W}_{it}^{\top}g^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})\|\leq G_{2}^{\prime}(\bm{W}_{it})
, and
‖
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
g
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
‖
≤
G
′′
​
(
𝑾
i
​
t
)
\|\bm{W}_{it}\bm{W}_{it}^{\top}g^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\|\leq G^{\prime\prime}(\bm{W}_{it})
, where
s
s
is from condition
(ii)
.
(viii)
The matrix
𝛀
T
\bm{\Omega}_{T}
from (
14
) is uniformly positive definite for
T
T
large enough.
The conditions of Assumption
3.10
are standard regularity conditions for (misspecified) quantile regression, but also cover the case of estimation through the more general GPL loss functions, similar to
Komunjer (2005)
.
The required moments of order
s
>
k
s>k
are required for the derivation of stochastic equicontinuity for strong mixing processes through
Hansen (1996)
.
As we consider low dimensionalities of
𝚯
⊂
ℝ
k
\bm{\Theta}\subset\mathbb{R}^{k}
such as
k
=
2
k=2
in our applications, this is not overly restrictive.
Condition (vi) is required under model misspecification, and holds naturally if either the tick loss is used (implying
g
′′
=
0
g^{\prime\prime}=0
), or under correct specification (implying
F
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
=
α
F_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})=\alpha
).
Compared to Assumption
3.7
, the conditions in Assumption
3.10
require the conditional distribution to be absolutely continuous, as specified in item
(iii)
; this is a standard requirement for quantile regression frameworks.
Furthermore, item
(viii)
is included here because the subsequent proposition specifically verifies the conditions for the asymptotic normality result established in Theorem
3.4
, but does not treat the case of Theorem
3.6
.
Proposition 3.11
.
Consider a GPL score from (
6
) for the decomposition, that is also used in (
12
). Then, Assumptions
3.1
and
3.10
imply Assumption
3.3
such that Theorem
3.4
holds.
Proposition
3.11
verifies the high-level conditions of Theorem
3.4
through standard conditions from (time series) quantile regression.
As discussed above, Theorem
3.6
only applies to smooth loss functions, and hence, the cases
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
and
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
are captured through the quantile-specific MZ-test of
Gaglianone et al. (2011)
.
3.5
Relation to Value-at-Risk backtests
VaR backtesting is a fundamental pillar of financial risk management, used to assess whether a model accurately predicts the frequency and magnitude of potential losses.
Traditional backtests such as by
Kupiec (1995)
and the traffic light system of
Basel Committee (1996)
;
Basel Committee (2019b)
typically focus on unconditional counts for the “violations” or “hits”, where realized losses exceed the VaR predictions as captured through the quantile identification functions,
𝖵
i
​
t
=
𝖵
(
X
i
​
t
,
Y
t
)
=
𝟙
{
Y
t
≤
X
i
​
t
}
−
α
\mathsf{V}_{it}=\mathsf{V}(X_{it},Y_{t})=\mathds{1}\{Y_{t}\leq X_{it}\}-\alpha
, from (
9
).
These unconditional tests, however, remain insensitive to the clustering of violations—a phenomenon particularly critical during financial crises, when consecutive days of unpredicted losses can lead to rapid capital depletion.
Table 2
:
Summary of prominent VaR backtests, including the underlying hypothesis, methodology and relation to conditional calibration in (
9
) through
𝒢
i
​
t
=
σ
⁡
(
𝑮
i
​
t
)
\mathcal{G}_{it}=\sigma(\bm{G}_{it})
.
We use the shorthand
𝖵
i
​
t
−
l
:=
𝖵
⁡
(
X
i
​
t
−
l
,
Y
t
−
l
)
\mathsf{V}_{it-l}:=\mathsf{V}(X_{it-l},Y_{t-l})
for
l
≥
0
l\geq 0
.
Reference
Label
Covariates/Instruments
𝑮
i
​
t
\bm{G}_{it}
Method
Hypothesis
ℋ
0
\mathcal{H}_{0}
Two-sided backtests
Kupiec (1995)
UC
𝑮
i
​
t
=
1
\bm{G}_{it}=1
𝔼
⁡
[
𝖵
⁡
(
X
i
​
t
,
Y
t
)
∣
𝑮
i
​
t
]
=
𝑮
i
​
t
⊤
​
𝜷
¯
i
\mathbb{E}\left[\mathsf{V}(X_{it},Y_{t})\mid\bm{G}_{it}\right]=\bm{G}_{it}^{\top}\bar{\bm{\beta}}_{i}
𝜷
¯
i
=
𝟎
\bar{\bm{\beta}}_{i}=\bm{0}
Christoffersen (1998)
CC
𝑮
i
​
t
=
(
1
,
𝖵
i
​
t
−
1
)
⊤
\bm{G}_{it}=\left(1,\mathsf{V}_{it-1}\right)^{\top}
𝔼
⁡
[
𝖵
⁡
(
X
i
​
t
,
Y
t
)
∣
𝑮
i
​
t
]
=
𝑮
i
​
t
⊤
​
𝜷
¯
i
\mathbb{E}\left[\mathsf{V}(X_{it},Y_{t})\mid\bm{G}_{it}\right]=\bm{G}_{it}^{\top}\bar{\bm{\beta}}_{i}
𝜷
¯
i
=
𝟎
\bar{\bm{\beta}}_{i}=\bm{0}
Engle and Manganelli (2004)
DQ
𝑮
i
​
t
=
(
1
,
𝖵
i
​
t
−
1
,
…
,
𝖵
i
​
t
−
4
)
⊤
\bm{G}_{it}=\left(1,\mathsf{V}_{it-1},\dots,\mathsf{V}_{it-4}\right)^{\top}
𝔼
⁡
[
𝖵
⁡
(
X
i
​
t
,
Y
t
)
∣
𝑮
i
​
t
]
=
𝑮
i
​
t
⊤
​
𝜷
¯
i
\mathbb{E}\left[\mathsf{V}(X_{it},Y_{t})\mid\bm{G}_{it}\right]=\bm{G}_{it}^{\top}\bar{\bm{\beta}}_{i}
𝜷
¯
i
=
𝟎
\bar{\bm{\beta}}_{i}=\bm{0}
Kuester et al. (2005)
DQX
𝑮
i
​
t
=
(
1
,
X
i
​
t
,
𝖵
i
​
t
−
1
,
…
,
𝖵
i
​
t
−
4
)
⊤
\bm{G}_{it}=\left(1,X_{it},\mathsf{V}_{it-1},\dots,\mathsf{V}_{it-4}\right)^{\top}
𝔼
⁡
[
𝖵
⁡
(
X
i
​
t
,
Y
t
)
∣
𝑮
i
​
t
]
=
𝑮
i
​
t
⊤
​
𝜷
¯
i
\mathbb{E}\left[\mathsf{V}(X_{it},Y_{t})\mid\bm{G}_{it}\right]=\bm{G}_{it}^{\top}\bar{\bm{\beta}}_{i}
𝜷
¯
i
=
𝟎
\bar{\bm{\beta}}_{i}=\bm{0}
Gaglianone et al. (2011)
VQR
𝑮
i
​
t
=
(
1
,
X
i
​
t
)
⊤
\bm{G}_{it}=\left(1,X_{it}\right)^{\top}
Q
α
​
(
Y
t
∣
𝑮
i
​
t
)
=
𝑮
i
​
t
⊤
​
𝜷
¯
i
Q_{\alpha}(Y_{t}\mid\bm{G}_{it})=\bm{G}_{it}^{\top}\bar{\bm{\beta}}_{i}
𝜷
¯
i
=
(
0
,
1
)
⊤
\bar{\bm{\beta}}_{i}=(0,1)^{\top}
One-sided backtests
Basel Committee (1996)
Basel
𝑮
i
​
t
=
1
\bm{G}_{it}=1
Binomial CDF
𝔼
⁡
[
𝖵
i
​
t
]
≤
0
\mathbb{E}[\mathsf{V}_{it}]\leq 0
Nolde and Ziegel (2017)
NZ
𝑮
i
​
t
=
(
1
,
X
i
​
t
)
⊤
\bm{G}_{it}=(1,X_{it})^{\top}
Moment Condition
𝔼
⁡
[
𝑮
i
​
t
⊤
​
𝖵
i
​
t
]
≤
0
\mathbb{E}[\bm{G}_{it}^{\top}\mathsf{V}_{it}]\leq 0
Following the seminal work of
Christoffersen (1998)
, a plethora of
conditional
backtests has been proposed over the past decades.
See e.g.,
Campbell (2007)
and
Nieto and Ruiz (2016)
for comprehensive reviews on VaR backtesting.
Most of these methods test hypotheses closely related to the conditional calibration property in (
9
) by utilizing varying information sets
𝒢
i
​
t
=
σ
⁡
(
𝑮
i
​
t
)
\mathcal{G}_{it}=\sigma(\bm{G}_{it})
.
Table
2
provides a non-exhaustive list of prominent VaR backtests, illustrating the intrinsic connection between their choice of covariates (or instruments)
𝑮
i
​
t
\bm{G}_{it}
and our recalibration variables
𝑾
i
​
t
\bm{W}_{it}
.
Notably, the equivalence between (
7
) and (
9
) permits specifications based on either quantile regressions for
Y
t
Y_{t}
, or mean regressions for the respective identification function.
As a canonical case of assessing auto-calibration, the quantile-specific adaptation of the MZ backtest by
Gaglianone et al. (2011)
utilizes the same recalibration technique as our linear score decomposition when
𝑾
i
​
t
⊤
=
(
1
,
X
i
​
t
)
\bm{W}_{it}^{\top}=(1,X_{it})
.
By matching the recalibration variables
𝑾
i
​
t
\bm{W}_{it}
with the covariates
𝑮
i
​
t
\bm{G}_{it}
, both the score decompositions and the underlying inference can be tailored to the specific notion of conditional calibration underlying the other backtests presented in Table
2
.
4
Simulations
We now assess the finite-sample performance of the proposed tests from Section
3.3
.
Section
4.1
describes the simulation setup and Section
4.2
reports the results.
4.1
Simulation setup
To empirically validate our tests for equal miscalibration, with null hypothesis
ℋ
𝖬𝖢𝖡
:
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
\mathcal{H}_{\mathsf{MCB}}:\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}
, or for equal discrimination, with
ℋ
𝖣𝖲𝖢
:
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
\mathcal{H}_{\mathsf{DSC}}:\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
, between competing mean or quantile forecasts, we use the following data-generating process (DGP) for the realizations,
Y
t
=
𝐕
t
⊤
​
𝜸
+
ε
Y
,
t
,
with
𝐕
t
=
(
K
t
,
L
t
,
M
t
,
N
t
)
⊤
and
𝜸
=
(
γ
K
,
γ
L
,
γ
M
,
γ
N
)
⊤
,
\displaystyle Y_{t}=\mathbf{V}_{t}^{\top}\bm{\gamma}+\varepsilon_{Y,t},\quad\text{with}\quad\mathbf{V}_{t}=(K_{t},L_{t},M_{t},N_{t})^{\top}\quad\text{and}\quad\bm{\gamma}=(\gamma_{K},\gamma_{L},\gamma_{M},\gamma_{N})^{\top},
(23)
with
ε
Y
,
t
∼
iid
𝒩
⁡
(
0
,
1
)
\varepsilon_{Y,t}\stackrel{{\scriptstyle\text{iid}}}{{\sim}}\mathcal{N}(0,1)
.
The predictor variables in
𝐕
t
\mathbf{V}_{t}
follow independent autoregressive AR(1) processes
K
t
=
β
​
K
t
−
1
+
ε
K
,
t
,
L
t
=
β
​
L
t
−
1
+
ε
L
,
t
,
M
t
=
β
​
M
t
−
1
+
ε
M
,
t
,
N
t
=
β
​
N
t
−
1
+
ε
N
,
t
K_{t}=\beta K_{t-1}+\varepsilon_{K,t},\ L_{t}=\beta L_{t-1}+\varepsilon_{L,t},\ M_{t}=\beta M_{t-1}+\varepsilon_{M,t},\ N_{t}=\beta N_{t-1}+\varepsilon_{N,t}
, with fixed
β
=
0.25
\beta=0.25
and
ε
K
,
t
,
ε
L
,
t
,
ε
M
,
t
,
ε
N
,
t
​
∼
iid
​
𝒩
​
(
0
,
1
)
\varepsilon_{K,t},\varepsilon_{L,t},\varepsilon_{M,t},\varepsilon_{N,t}\overset{\text{iid}}{\sim}\mathcal{N}(0,1)
, which are all mutually independent.
Forecaster
X
1
​
t
X_{1t}
has exclusive access to
K
t
K_{t}
and forecaster
X
2
​
t
X_{2t}
to
L
t
L_{t}
, while both forecasters share information on
M
t
M_{t}
and
N
t
N_{t}
as formalized by
ℐ
1
​
t
=
σ
⁡
{
K
t
,
M
t
,
N
t
}
\mathcal{I}_{1t}=\sigma\left\{K_{t},M_{t},N_{t}\right\}
and
ℐ
2
​
t
=
σ
⁡
{
L
t
,
M
t
,
N
t
}
\mathcal{I}_{2t}=\sigma\left\{L_{t},M_{t},N_{t}\right\}
.
Notice that our setup requires both “joint” predictors
M
t
M_{t}
and
N
t
N_{t}
in order to construct non-collinear forecasts with equal
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
and/or
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
values.
Based on the distinct information sets
ℐ
1
​
t
\mathcal{I}_{1t}
and
ℐ
2
​
t
\mathcal{I}_{2t}
, the forecasters issue
mean
forecasts
X
1
​
t
\displaystyle X_{1t}
=
δ
0
+
𝐕
t
⊤
​
𝜹
,
with
𝜹
=
(
δ
K
,
0
,
δ
M
,
δ
N
)
⊤
∈
ℝ
4
,
\displaystyle=\delta_{0}+\mathbf{V}_{t}^{\top}\bm{\delta},\qquad\text{with}\qquad\bm{\delta}=(\delta_{K},0,\delta_{M},\delta_{N})^{\top}\in\mathbb{R}^{4},
(24)
X
2
​
t
\displaystyle X_{2t}
=
ξ
0
+
𝐕
t
⊤
​
𝝃
,
with
𝝃
=
(
0
,
ξ
L
,
ξ
M
,
ξ
N
)
⊤
∈
ℝ
4
,
\displaystyle=\xi_{0}+\mathbf{V}_{t}^{\top}\bm{\xi},\qquad\text{with}\qquad\bm{\xi}=(0,\xi_{L},\xi_{M},\xi_{N})^{\top}\in\mathbb{R}^{4},
(25)
and
δ
0
,
ξ
0
∈
ℝ
\delta_{0},\xi_{0}\in\mathbb{R}
.
The imposed zeros in
𝜹
\bm{\delta}
and
𝝃
\bm{\xi}
reflect the absence of the corresponding predictor variables in the information sets of the respective forecaster.
The coefficients
(
δ
0
,
𝜹
⊤
)
(\delta_{0},\bm{\delta}^{\top})
and
(
ξ
0
,
𝝃
⊤
)
(\xi_{0},\bm{\xi}^{\top})
and their relation to
𝜸
\bm{\gamma}
allows to generate forecasts with different calibration and discrimination properties, as formalized in the following proposition for the squared error score from (
4
).
Proposition 4.1
.
For realizations
Y
t
Y_{t}
and forecasts
X
1
​
t
X_{1t}
and
X
2
​
t
X_{2t}
following (
23
)–(
25
) with
𝛅
≠
0
\bm{\delta}\not=0
and
𝛏
≠
0
\bm{\xi}\not=0
, and given the recalibration information
𝒲
i
​
t
=
σ
⁡
{
𝐖
i
​
t
}
\mathcal{W}_{it}=\sigma\{\bm{W}_{it}\}
, with
𝐖
i
​
t
=
(
1
,
X
i
​
t
)
⊤
\bm{W}_{it}=(1,X_{it})^{\top}
,
i
=
1
,
2
i=1,2
,
the population squared error score decomposition of the forecasts
X
1
​
t
X_{1t}
is
𝖬𝖢𝖡
¯
1
=
δ
0
2
+
ς
⋅
(
𝜹
⊤
​
𝜹
−
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
,
𝖣𝖲𝖢
¯
1
=
ς
⋅
(
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
,
𝖴𝖭𝖢
¯
=
ς
⋅
𝜸
⊤
​
𝜸
+
1
,
\displaystyle\overline{\mathsf{MCB}}_{1}=\delta_{0}^{2}+\varsigma\cdot\frac{(\bm{\delta}^{\top}\bm{\delta}-\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}},\qquad\overline{\mathsf{DSC}}_{1}=\varsigma\cdot\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}},\qquad\overline{\mathsf{UNC}}=\varsigma\cdot\bm{\gamma}^{\top}\bm{\gamma}+1,
(26)
where
ς
=
1
1
−
β
2
\varsigma=\frac{1}{1-\beta^{2}}
is the variance of the zero-mean AR(1) processes
K
t
,
L
t
,
M
t
,
N
t
K_{t},L_{t},M_{t},N_{t}
. For
𝖬𝖢𝖡
¯
2
\overline{\mathsf{MCB}}_{2}
and
𝖣𝖲𝖢
¯
2
\overline{\mathsf{DSC}}_{2}
interchange
δ
0
2
\delta_{0}^{2}
and
𝛅
\bm{\delta}
with
ξ
0
2
\xi_{0}^{2}
and
𝛏
\bm{\xi}
, respectively.
The expressions in Proposition
4.1
illustrate that for non-constant forecasts,
𝖬𝖢𝖡
¯
1
=
0
\overline{\mathsf{MCB}}_{1}=0
holds if and only if
𝜹
⊤
​
𝜹
=
𝜹
⊤
​
𝜸
\bm{\delta}^{\top}\bm{\delta}=\bm{\delta}^{\top}\bm{\gamma}
and
δ
0
=
0
\delta_{0}=0
.
Hence, perfect calibration,
𝖬𝖢𝖡
¯
1
=
0
\overline{\mathsf{MCB}}_{1}=0
, can be achieved even if the forecaster omits relevant variables.
However, satisfying the condition
𝜹
⊤
​
𝜹
=
𝜹
⊤
​
𝜸
\bm{\delta}^{\top}\bm{\delta}=\bm{\delta}^{\top}\bm{\gamma}
generally requires the forecaster to correctly weigh the signals they do include.
Absent a coincidental combination of perfectly offsetting coefficient errors, using an incorrect parameter value or incorporating an irrelevant predictor (e.g.,
δ
M
≠
0
\delta_{M}\neq 0
when
γ
M
=
0
\gamma_{M}=0
) will violate this equality and cause miscalibration.
The
𝖣𝖲𝖢
¯
1
\overline{\mathsf{DSC}}_{1}
component is unaffected by the intercept
δ
0
\delta_{0}
that does not carry any information.
𝖣𝖲𝖢
¯
1
\overline{\mathsf{DSC}}_{1}
is positive whenever
𝜹
⊤
​
𝜸
≠
0
\bm{\delta}^{\top}\bm{\gamma}\neq 0
, that is, whenever
X
1
​
t
X_{1t}
reacts to the signal in
Y
t
Y_{t}
, even incorrectly such as in the wrong direction.
Moreover, by Cauchy-Schwarz,
(
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
≤
𝜸
⊤
​
𝜸
\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}}\leq\bm{\gamma}^{\top}\bm{\gamma}
, such that the unconstrained theoretical upper bound for discrimination is
ς
​
𝜸
⊤
​
𝜸
\varsigma\bm{\gamma}^{\top}\bm{\gamma}
.
This global bound would be attained if and only if a forecaster could choose parameters
𝜹
\bm{\delta}
proportionally to the full signal
𝜸
\bm{\gamma}
, i.e.,
𝜹
=
c
​
𝜸
\bm{\delta}=c\bm{\gamma}
for some
c
∈
ℝ
c\in\mathbb{R}
as then,
(
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
=
c
2
​
(
𝜸
⊤
​
𝜸
)
2
c
2
​
𝜸
⊤
​
𝜸
=
𝜸
⊤
​
𝜸
\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}}=\frac{c^{2}(\bm{\gamma}^{\top}\bm{\gamma})^{2}}{c^{2}\bm{\gamma}^{\top}\bm{\gamma}}=\bm{\gamma}^{\top}\bm{\gamma}
.
Hence, maximal discrimination can arise even for miscalibrated forecasts.
If only some relevant variables are observed, the best achievable discrimination is obtained when the available predictors are used correctly.
Analogous conclusions hold for the second forecaster
X
2
​
t
X_{2t}
by replacing
𝜹
\bm{\delta}
with
𝝃
\bm{\xi}
.
Table 3
:
Twelve
mean forecasting
specifications of the parameters
𝜸
,
δ
0
,
𝜹
,
ξ
0
,
𝝃
\bm{\gamma},\delta_{0},\bm{\delta},\xi_{0},\bm{\xi}
in (
23
)–(
25
) based on a flexible
k
∈
{
0
,
0.05
,
…
,
0.45
,
0.5
}
k\in\{0,0.05,\ldots,0.45,0.5\}
.
All setups guarantee non-collinear forecasts and generate different relations of the
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
and
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
values as given in the numbered rows and the last column termed “Implications”.
Realization
Forecaster
X
1
​
t
X_{1t}
Forecaster
X
2
​
t
X_{2t}
γ
K
\gamma_{K}
γ
L
\gamma_{L}
γ
M
\gamma_{M}
γ
N
\gamma_{N}
δ
0
\delta_{0}
δ
K
\delta_{K}
δ
L
\delta_{L}
δ
M
\delta_{M}
δ
N
\delta_{N}
ξ
0
\xi_{0}
ξ
K
\xi_{K}
ξ
L
\xi_{L}
ξ
M
\xi_{M}
ξ
N
\xi_{N}
Implications
(A) Parameterization of
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
difference
1)
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
=
8
​
k
2
15
\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)=\frac{8k^{2}}{15}
0
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
0
0
0
k
2
+
1
4
\frac{k}{\sqrt{2}}+\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
<
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}<\overline{\mathsf{DSC}}_{2}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
0
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
2)
𝖬𝖢𝖡
¯
1
=
0
\overline{\mathsf{MCB}}_{1}=0
and
𝖬𝖢𝖡
¯
2
​
(
k
)
=
8
​
k
2
15
\overline{\mathsf{MCB}}_{2}(k)=\frac{8k^{2}}{15}
0
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
0
0
0
1
4
\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
<
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}<\overline{\mathsf{DSC}}_{2}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
0
1
4
\frac{1}{4}
0
1
4
\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
3)
𝖬𝖢𝖡
¯
1
​
(
k
)
=
2
​
𝖬𝖢𝖡
¯
2
​
(
k
)
=
16
​
k
2
15
{\overline{\mathsf{MCB}}}_{1}(k)=2\,{\overline{\mathsf{MCB}}}_{2}(k)=\frac{16k^{2}}{15}
0
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
0
0
0
k
+
1
4
k+\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
<
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}<\overline{\mathsf{DSC}}_{2}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
0
k
2
+
1
4
\frac{k}{\sqrt{2}}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{\sqrt{2}}+\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
(B) Parameterization of
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
difference
4)
𝖣𝖲𝖢
¯
1
​
(
k
)
=
𝖣𝖲𝖢
¯
2
​
(
k
)
=
8
​
k
2
15
\overline{\mathsf{DSC}}_{1}(k)=\overline{\mathsf{DSC}}_{2}(k)=\frac{8k^{2}}{15}
0
0
0
k
k
0
k
2
+
1
4
​
2
\frac{k}{2}+\frac{1}{4\sqrt{2}}
0
0
k
2
+
1
4
​
2
\frac{k}{2}+\frac{1}{4\sqrt{2}}
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
<
𝖬𝖢𝖡
¯
2
0<\overline{\mathsf{MCB}}_{1}<\overline{\mathsf{MCB}}_{2}
0
0
0
k
k
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
0<\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}
5)
𝖣𝖲𝖢
¯
1
=
0
\overline{\mathsf{DSC}}_{1}=0
and
𝖣𝖲𝖢
¯
2
​
(
k
)
=
8
​
k
2
15
\overline{\mathsf{DSC}}_{2}(k)=\frac{8k^{2}}{15}
0
0
0
k
k
0
0
0
1
4
\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
<
𝖬𝖢𝖡
¯
2
0<\overline{\mathsf{MCB}}_{1}<\overline{\mathsf{MCB}}_{2}
0
0
0
k
k
0
1
4
\frac{1}{4}
0
1
4
\frac{1}{4}
0
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
0<\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}
6)
𝖣𝖲𝖢
¯
1
​
(
k
)
=
2
​
𝖣𝖲𝖢
¯
2
​
(
k
)
=
16
​
k
2
15
{\overline{\mathsf{DSC}}}_{1}(k)=2\,{\overline{\mathsf{DSC}}}_{2}(k)=\frac{16k^{2}}{15}
0
0
0
k
k
0
0
0
0
k
+
1
4
k+\frac{1}{4}
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
<
𝖬𝖢𝖡
¯
2
0<\overline{\mathsf{MCB}}_{1}<\overline{\mathsf{MCB}}_{2}
0
0
0
k
k
1
15
\frac{1}{\sqrt{15}}
0
0
0
k
+
1
4
k+\frac{1}{4}
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
0<\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}
The closed-form expressions in Proposition
4.1
enable diverse specifications of
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
, allowing us to study the size and power of our proposed tests across different settings by appropriately choosing the parameters
𝜸
\bm{\gamma}
,
(
δ
0
,
𝜹
⊤
)
(\delta_{0},\bm{\delta}^{\top})
, and
(
ξ
0
,
𝝃
⊤
)
(\xi_{0},\bm{\xi}^{\top})
.
In detail, Table
3
specifies twelve different parameterizations that result in illustrative settings for
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
as given in the facet labels of Figure
1
.
To analyze test size and power, we vary a parameter
k
>
0
k>0
that affects
𝜸
,
(
δ
0
,
𝜹
⊤
)
\bm{\gamma},(\delta_{0},\bm{\delta}^{\top})
, and
(
ξ
0
,
𝝃
⊤
)
(\xi_{0},\bm{\xi}^{\top})
, which continuously shifts the DGPs either along or away from their respective null hypotheses.
The specifications of Table
3
are chosen to guarantee that either
𝖬𝖢𝖡
¯
2
​
(
k
)
\overline{\mathsf{MCB}}_{2}(k)
or
𝖣𝖲𝖢
¯
2
​
(
k
)
\overline{\mathsf{DSC}}_{2}(k)
depend on
k
k
and equal
8
​
k
2
15
\frac{8k^{2}}{15}
for all
k
≥
0
k\geq 0
.
Figure
D.1
in Appendix
D
plots the population values
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
,
i
=
1
,
2
i=1,2
as functions of
k
k
for all twelve setups.
For example, we generate the scenario
𝖬𝖢𝖡
¯
1
=
0
\overline{\mathsf{MCB}}_{1}=0
and
𝖬𝖢𝖡
¯
2
​
(
k
)
=
8
​
k
2
15
\overline{\mathsf{MCB}}_{2}(k)=\tfrac{8k^{2}}{15}
while maintaining
0
<
𝖣𝖲𝖢
¯
1
<
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}<\overline{\mathsf{DSC}}_{2}
independent of
k
k
by setting
𝜸
⊤
=
(
0
,
1
4
,
1
4
,
0
)
\bm{\gamma}^{\top}=(0,\tfrac{1}{4},\tfrac{1}{4},0)
as well as
(
δ
0
,
𝜹
⊤
)
=
(
0
,
0
,
0
,
1
4
,
0
)
(\delta_{0},\bm{\delta}^{\top})=(0,0,0,\tfrac{1}{4},0)
and
(
ξ
0
,
𝝃
⊤
)
=
(
0
,
0
,
1
4
+
k
2
,
1
4
+
k
2
,
0
)
(\xi_{0},\bm{\xi}^{\top})=(0,0,\tfrac{1}{4}+\tfrac{k}{2},\tfrac{1}{4}+\tfrac{k}{2},0)
.
Here, the realizations are only driven by
L
t
L_{t}
and
M
t
M_{t}
with equal magnitudes,
γ
L
=
γ
M
\gamma_{L}=\gamma_{M}
.
The first forecaster
X
1
​
t
X_{1t}
does not have access to
L
t
L_{t}
, but she correctly uses
M
t
M_{t}
through
δ
M
=
γ
M
\delta_{M}=\gamma_{M}
such that her forecasts are perfectly calibrated,
𝖬𝖢𝖡
¯
1
=
0
\overline{\mathsf{MCB}}_{1}=0
.
The sole access to
M
t
M_{t}
however limits her discrimination to
𝖣𝖲𝖢
¯
1
=
1
15
\overline{\mathsf{DSC}}_{1}=\tfrac{1}{15}
.
By contrast, the second forecaster
X
2
​
t
X_{2t}
uses both relevant variables
L
t
L_{t}
and
M
t
M_{t}
, and hence achieves a higher discrimination
𝖣𝖲𝖢
¯
2
=
2
15
>
𝖣𝖲𝖢
¯
1
\overline{\mathsf{DSC}}_{2}=\tfrac{2}{15}>\overline{\mathsf{DSC}}_{1}
for any
k
≥
0
k\geq 0
.
However, for values
k
>
0
k>0
, she uses the information incorrectly with
𝝃
≠
𝜸
\bm{\xi}\not=\bm{\gamma}
such that
𝖬𝖢𝖡
¯
2
​
(
k
)
=
8
​
k
2
15
\overline{\mathsf{MCB}}_{2}(k)=\tfrac{8k^{2}}{15}
increases with
k
k
.
Table 4
:
Four
quantile forecasting
specifications of the parameters
𝜸
,
δ
0
,
𝜹
,
ξ
0
,
𝝃
\bm{\gamma},\delta_{0},\bm{\delta},\xi_{0},\bm{\xi}
in (
23
) and (
27
) based on a flexible
k
∈
{
0
,
0.05
,
…
,
0.95
,
1
}
k\in\{0,0.05,\ldots,0.95,1\}
.
All setups guarantee non-collinear forecasts and generate different relations of the
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
and
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
values as given in the numbered rows and the last column termed “Implications”.
The values of
ξ
0
​
(
k
,
α
)
\xi_{0}(k,\alpha)
are chosen numerically such that
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)
holds; see Appendix
C
and Figure
C.1
for details.
Realization
Forecaster
X
1
​
t
α
X_{1t}^{\alpha}
Forecaster
X
2
​
t
α
X_{2t}^{\alpha}
γ
K
\gamma_{K}
γ
L
\gamma_{L}
γ
M
\gamma_{M}
γ
N
\gamma_{N}
δ
0
\delta_{0}
δ
K
\delta_{K}
δ
L
\delta_{L}
δ
M
\delta_{M}
δ
N
\delta_{N}
ξ
0
\xi_{0}
ξ
K
\xi_{K}
ξ
L
\xi_{L}
ξ
M
\xi_{M}
ξ
N
\xi_{N}
Implications
(A) Parameterization of
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
difference
1)
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)
increasing with
k
≥
0
k\geq 0
, starting from
0
0
1
4
\frac{1}{4}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
(
16
15
−
1
)
​
z
α
(\sqrt{\tfrac{16}{15}}-1)z_{\alpha}
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
0
(
16
15
−
1
)
​
z
α
(\sqrt{\tfrac{16}{15}}-1)z_{\alpha}
0
k
2
+
1
4
\frac{k}{{2}}+\frac{1}{4}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
2)
𝖬𝖢𝖡
¯
1
=
0
\overline{\mathsf{MCB}}_{1}=0
and
𝖬𝖢𝖡
¯
2
​
(
k
)
\overline{\mathsf{MCB}}_{2}(k)
increasing with
k
≥
0
k\geq 0
, starting from
0
0
1
4
\frac{1}{4}
1
4
\frac{1}{4}
1
4
\frac{1}{4}
0
(
16
15
−
1
)
​
z
α
(\sqrt{\tfrac{16}{15}}-1)z_{\alpha}
1
4
\frac{1}{4}
0
1
4
\frac{1}{4}
0
(
16
15
−
1
)
​
z
α
(\sqrt{\tfrac{16}{15}}-1)z_{\alpha}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
<
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
0<\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
(B) Parameterization of
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
difference
4)
𝖣𝖲𝖢
¯
1
​
(
k
)
=
𝖣𝖲𝖢
¯
2
​
(
k
)
\overline{\mathsf{DSC}}_{1}(k)=\overline{\mathsf{DSC}}_{2}(k)
increasing with
k
≥
0
k\geq 0
, starting from
0
0
0
0
0
k
k
(
1
+
8
15
​
k
2
−
1
)
​
z
α
(\sqrt{1+\tfrac{8}{15}k^{2}}-1)z_{\alpha}
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
(
1
+
8
15
​
k
2
−
1
)
​
z
α
(\sqrt{1+\tfrac{8}{15}k^{2}}-1)z_{\alpha}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
0<\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)
5)
𝖣𝖲𝖢
¯
1
=
0
\overline{\mathsf{DSC}}_{1}=0
and
𝖣𝖲𝖢
¯
2
​
(
k
)
\overline{\mathsf{DSC}}_{2}(k)
increasing with
k
≥
0
k\geq 0
, starting from
0
0
0
0
0
k
k
1
2
\frac{1}{2}
1
4
\frac{1}{4}
0
1
4
\frac{1}{4}
0
ξ
0
​
(
k
,
α
)
\xi_{0}(k,\alpha)
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
k
2
+
1
4
\frac{k}{2}+\frac{1}{4}
0
<
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
0<\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)
For the evaluation of our tests for
quantile forecasts
, we use the same DGP in (
23
).
As the information in
𝐕
t
\mathbf{V}_{t}
only affects the conditional mean of
Y
t
Y_{t}
in (
23
), we generate the quantile forecasts at level
α
∈
(
0
,
1
)
\alpha\in(0,1)
as
X
1
​
t
α
=
𝐕
t
⊤
​
𝜹
+
δ
0
+
z
α
,
and
X
2
​
t
α
=
𝐕
t
⊤
​
𝝃
+
ξ
0
+
z
α
,
\displaystyle X_{1t}^{\alpha}=\mathbf{V}_{t}^{\top}\bm{\delta}+\delta_{0}+z_{\alpha},\qquad\text{and}\qquad X_{2t}^{\alpha}=\mathbf{V}_{t}^{\top}\bm{\xi}+\xi_{0}+z_{\alpha},
(27)
using standard normal quantiles, denoted by
z
α
=
Φ
−
1
​
(
α
)
z_{\alpha}=\Phi^{-1}(\alpha)
.
We deliberately use the pure location process (
23
) for quantile forecasts, allowing us to explicitly control the population miscalibration and discrimination values for the check loss in Proposition
C.1
, albeit these closed-form expressions become much more complicated as for the squared error.
Due to this additional complication, we only consider four informative parameterizations as given in Table
4
.
For these, Appendix
C
provides the closed-form expressions for
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
as explicit functions of
k
,
α
k,\alpha
and the parameters of the DGP.
Notably, for the last parametrization, (approximate) equality of the miscalibration values is achieved by a numerical choice for the values of
ξ
0
=
ξ
0
​
(
k
,
α
)
\xi_{0}=\xi_{0}(k,\alpha)
; see Figure
C.1
and the text of Appendix
C
.
4.2
Simulation results
Figure 1
:
Empirical rejection rates for mean forecasts and the squared error score for the proposed tests of equal miscalibration (in blue) in the upper panel a), equal discrimination (in orange) in the lower panel b), and of the DM test of equal predictive performance (in gray) in the lower plots rows of both panels.
We generate the data according to (
23
)–(
25
) with the twelve parameterizations of Table
3
, which depend on the parameter
k
≥
0
k\geq 0
that is displayed on the
x
x
-axes.
We use
T
=
500
T=500
and a nominal level of
10
%
10\%
.
All results are based on 5000 Monte Carlo replications, a nominal significance level of
10
%
10\%
and
T
=
500
T=500
.
We estimate all long-run covariance matrices by the HAC estimator of
Andrews (1991)
, adapted to quantile regressions by
Galvao and Yoon (2024)
.
For the implementation, we follow the default
vcovHAC
procedure from the
R
package
sandwich
of
Zeileis (2004)
.
For
mean forecasts
and the associated squared error score, Figure
1
shows the rejection rates of the test for equal miscalibration
ℋ
𝖬𝖢𝖡
:
𝖬𝖢𝖡
¯
1
=
𝖬𝖢𝖡
¯
2
\mathcal{H}_{\mathsf{MCB}}:\overline{\mathsf{MCB}}_{1}=\overline{\mathsf{MCB}}_{2}
in the upper panel in blue color, and of the test for equal discrimination
ℋ
𝖣𝖲𝖢
:
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
\mathcal{H}_{\mathsf{DSC}}:\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
in orange color in the lower panel.
For comparison, we also show rejection rates of the DM test of equal predictive power
ℋ
𝖲
:
𝖲
¯
1
=
𝖲
¯
2
\mathcal{H}_{\mathsf{S}}:\overline{\mathsf{S}}_{1}=\overline{\mathsf{S}}_{2}
with gray and dotted lines.
We only show these rejection rates when the underlying population score difference coincides with the respective difference in
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
or
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
values.
E.g., in the lower row of panel a), we ensure
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}
such that
𝖲
¯
1
−
𝖲
¯
2
=
𝖬𝖢𝖡
¯
1
−
𝖬𝖢𝖡
¯
2
\overline{\mathsf{S}}_{1}-\overline{\mathsf{S}}_{2}=\overline{\mathsf{MCB}}_{1}-\overline{\mathsf{MCB}}_{2}
.
Figure 2
:
Empirical rejection rates for
α
\alpha
-quantile forecasts and the check loss for the proposed tests of equal miscalibration (in blue) in the left two columns, equal discrimination (in orange) in the right two columns, and of the DM test of equal predictive performance (in gray) in all subplots.
We generate the data according to (
23
) and (
27
) with the four parameterizations of Table
4
, which depend on the parameter
k
≥
0
k\geq 0
that is displayed on the
x
x
-axes.
We use
T
=
500
T=500
and a nominal level of
10
%
10\%
.
Throughout the four plots in the left column, as well as for
k
=
0
k=0
in all twelve plots, the data is generated under the respective null hypotheses of equal miscalibration in panel a), and equal discrimination in panel b).
Here, we find correct or conservative rejection rates below the nominal level of
10
%
10\%
for our tests, which is to be expected given the Bonferroni-type corrections from Section
3.3
.
In the left panel, our tests approach the correct size for larger values of
k
k
as e.g., for the
𝖬𝖢𝖡
\mathsf{MCB}
-test, miscalibration of both forecasts increases with
k
k
such that
2
​
min
⁡
{
p
𝖬𝖢𝖡
1
0
,
p
𝖬𝖢𝖡
2
0
}
2\min\{p^{0}_{\mathsf{MCB}_{1}},p^{0}_{\mathsf{MCB}_{2}}\}
becomes much smaller than
p
𝖬𝖢𝖡
+
p^{+}_{\mathsf{MCB}}
, which operates under its null hypothesis and hence generates asymptotically exact size control.
The middle and right plot columns show that power increases with
k
k
across all subplots, illustrating the robustness of the proposed component tests to zero or positive values of the remaining population
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
components.
In the scenarios where score differences are driven exclusively by differences in
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
(upper panel) or
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
(lower panel), the corresponding component test rejects more frequently than the DM test.
While the underlying null hypotheses differ and the rejection frequencies are therefore not directly comparable, this finding reflects that the DM test is affected by variability from both score components, whereas the component tests isolate the relevant source of predictive differences.
This increased sensitivity is also reflected in the results of the empirical applications in Section
5
.
Figure
2
displays rejection rates for quantile forecasts at levels
α
∈
{
0.01
,
0.05
,
0.1
,
0.25
,
0.5
}
\alpha\in\{0.01,0.05,0.1,0.25,0.5\}
and within the four most informative parameterizations that allow for comparison with the DM test.
These four scenarios correspond to the lower left and middle plots in panels a) and b) from Figure
1
.
The results for median forecasts with
α
=
0.5
\alpha=0.5
are comparable to the mean forecasting results from Figure
1
: The tests are conservative under the null, develop power with
k
>
0
k>0
and despite their conservative size
3
3
3
In unreported simulations, we find that the elevated type I error of the DSC test in the third column for
α
=
0.01
\alpha=0.01
does not increase with
k
k
and declines as the sample size grows. This pattern suggests that the distortion is attributable to finite-sample effects.
, our tests reject more frequency than the DM test.
For more extreme quantile levels, power naturally declines.
Importantly, especially for the DSC test, this difference in rejection frequencies becomes even more pronounced for extreme quantile levels.
5
Applications
Here, we apply the proposed tests for equal miscalibration and discrimination in two central forecasting domains: inflation rates in Section
5.1
and financial risks in Section
5.2
.
Replication code and details on the data are available at
https://github.com/marius-cp/SDI_replications
.
5.1
Survey forecasts of U.S. annual CPI inflation
Inflation is renowned for being difficult to forecast, and survey forecasts often outperform sophisticated econometric models
(
Faust and Wright, 2013
)
.
We compare two popular one-year-ahead survey forecasts for quarterly U.S. consumer price index (CPI) inflation: the Survey of Professional Forecasters (SPF) of the Federal Reserve Bank of Philadelphia, and the Michigan Survey of Consumers.
4
4
4
Data sources: SPF forecasts (
Individual_CPI.xlsx
) from
Philadelphia Fed
; Michigan forecasts (Table 32) from their
data site
; and CPI data (
cpiQvMd.xlsx
) from
Philadelphia Fed
.
The SPF is considered an expert forecast, as its panelists are professionals with extensive macroeconomic forecasting experience.
In contrast, the Michigan survey randomly samples U.S. cell phone numbers, without targeting professionals.
One might therefore expect the experts to outperform consumers, yet overall forecast comparisons are often inconclusive as e.g., in the empirical applications of
Ehm et al. (2016)
and
Patton (2020)
.
The aim of this application is to demonstrate that, even when inference on the overall scores is inconclusive, the improved test power of the individual
𝖬𝖢𝖡
\mathsf{MCB}
and
𝖣𝖲𝖢
\mathsf{DSC}
decomposition terms illustrated in Section
4
can produce significant results with clear and interpretable insights while being applicable in general multi-step ahead forecast environments.
Figure 3
:
Quarterly year-over-year CPI inflation rate together with the SPF and Michigan forecasts. For details, see the text in Section
5.1
.
We replicate the analyses of
Ehm et al. (2016)
and
Patton (2020)
, comparing the predictive performance of the SPF and Michigan survey forecasts, and extend their approach by applying our novel tests for equal forecast calibration and discrimination.
Our evaluation sample covers
T
=
154
T=154
quarters, from 1982:Q3 to 2020:Q4, thereby excluding the high-inflation period following the COVID-19 pandemic.
Figure
3
displays the forecasts alongside the corresponding realizations.
5
5
5
The validity of our inference methods could be generalized to non-stationary data at the expense of a more involved notation as long as suitable CLTs and LLNs in Assumption
3.3
hold.
Michigan survey respondents report their expectations of the percentage change in prices over the next 12 months. To ensure comparability, we follow
Ehm et al. (2016)
and
Patton (2020)
and construct a corresponding SPF measure by averaging the one- to four-quarter-ahead consensus forecasts (where the consensus is defined as the median across respondents). Averaging is appropriate because SPF forecasts are stated in terms of annualized quarter-over-quarter inflation rates.
As the evaluation target
Y
t
Y_{t}
, we use the four-quarter logarithmic growth rate of the CPI, based on the 2023:Q3 vintage, over the year following the forecast date.
Figure 4
:
Inflation forecast evaluation results for the SPF and Michigan forecasts using the squared error scoring function.
The left “
𝖬𝖢𝖡
\mathsf{MCB}
–
𝖣𝖲𝖢
\mathsf{DSC}
” plots show the average score as iso-lines together with its decomposition into miscalibration and discrimination components for the four competing forecasts.
The gray boxes in the right panels display the
p
p
-values of tests for zero miscalibration and discrimination, respectively.
The white box displays the average score, miscalibration and discrimination differences, together with 0 to 3 stars indicating significance at the 10%, 5%, and 1% levels.
The left panel of Figure
4
reports the average squared error score together with its decomposition into miscalibration and discrimination components for the two competing forecasts.
Calibration appears broadly similar across the two surveys.
In contrast, the SPF forecasts display a markedly higher degree of discrimination—a difference that is not visible in the purely scoring-function-based analyses of
Ehm et al. (2016)
and
Patton (2020)
.
The right panel corroborates their main finding: the overall difference in predictive performance is statistically insignificant, with a
p
p
-value of 0.284.
Consistent with the visual impression from the left panel, the difference in miscalibration is not statistically significant. However, the SPF forecasts exhibit significantly stronger discrimination, with a
p
p
-value of 0.037. For the Michigan survey forecasts, we cannot even reject the null hypothesis of no discrimination.
These findings suggest that professional forecasters’ predictions contain more information about future inflation outcomes, which is plausible given their field-specific expertise and experience.
Figure
D.3
in Appendix
D
reports diagnostic checks for the linear recalibration regression and reveals no evidence of misspecification, supporting the use of linear recalibration for inference on score decompositions.
From a methodological perspective, this application underscores the utility of our proposed inference framework.
Beyond partitioning forecast performance into interpretable economic components, our tests can exhibit superior statistical power compared to the DM test in these settings.
Furthermore, the framework is applicable in general time-series environments, including multi-step-ahead forecasting horizons.
5.2
Financial volatility and Value-at-Risk forecast performance
Here, we extend the motivational example from Section
1.1
and consider one-day-ahead forecasts of the variance and the
α
\alpha
-quantiles (
α
\alpha
-VaR), with
α
∈
{
1
%
,
5
%
}
\alpha\in\{1\%,5\%\}
, of financial log returns
R
t
R_{t}
.
This application demonstrates the value of inference based on score decompositions, as it helps reconcile the partly contradictory findings that often arise between traditional backtests reviewed in Section
3.5
and scoring-function-based forecast evaluations in applied work such as in Section
1.1
.
Given the standard assumption
𝔼
⁡
[
R
t
]
=
0
\mathbb{E}[R_{t}]=0
such that
Var
⁡
(
R
t
)
=
𝔼
⁡
[
R
t
2
]
\operatorname{Var}(R_{t})=\mathbb{E}[R_{t}^{2}]
, the variance forecasts can be treated as forecasts for the expectation of
R
t
2
R_{t}^{2}
, or as introduced below, the expectation of an unbiased RV estimator.
Hence, we follow
Patton (2011)
and evaluate the forecasts with the squared error and QLIKE loss functions that are special cases of the Bregman class (
3
), considered in Proposition
3.9
.
For the VaR forecasts, we use the check loss from (
6
), as covered by Proposition
3.11
.
For
R
t
R_{t}
, we use logarithmic returns of the S&P 500 E-mini futures, a highly liquid instrument central to practical portfolio management, which is widely used in the financial variance forecasting literature
(
Corsi, 2009
;
Liu et al., 2015
;
Bollerslev et al., 2018
)
.
E-mini contracts trade almost continuously from Sunday evening to Friday afternoon, with brief daily interruptions from 3:15–3:30 p.m. and 4:00–5:00 p.m. CT.
A trading day is defined as the interval spanning from 5:00 p.m. CT of the preceding calendar day to 4:59 p.m. CT.
We use intraday price observations from the data provider Refinitiv (ticker: ESc1), spanning the period from January 1, 2000, to January 1, 2022.
From this, we compute the daily open-to-close return
R
t
R_{t}
and the 5-minute realized variance,
RV
t
:=
∑
m
=
1
M
r
t
​
m
2
\operatorname{RV}_{t}:=\sum_{m=1}^{M}r_{tm}^{2}
, where
r
t
​
m
r_{tm}
is the
m
m
-th intraday return on day
t
t
and
M
M
denotes the number of equally spaced observations per trading day.
We employ several standard models to generate one-step-ahead variance forecasts.
We first consider the standard GARCH(1,1) model with Gaussian innovations of
Bollerslev (1986)
.
Second, we employ an asymmetric extension, the GJR-GARCH model of
Glosten et al. (1993)
with Student’s
t
t
residuals, given by
R
t
=
σ
t
2
​
ε
t
,
with
ε
t
​
∼
iid
​
t
ν
,
σ
t
2
=
α
0
+
α
1
σ
t
−
1
2
+
α
2
R
t
−
1
2
+
α
3
R
t
−
1
2
𝟙
{
R
t
−
1
<
0
}
.
\displaystyle\begin{split}R_{t}&=\sqrt{\sigma_{t}^{2}}\,\varepsilon_{t},\qquad\text{with}\qquad\varepsilon_{t}\overset{\text{iid}}{\sim}t_{\nu},\\
\sigma_{t}^{2}&=\alpha_{0}+\alpha_{1}\sigma_{t-1}^{2}+\alpha_{2}R_{t-1}^{2}+\alpha_{3}R_{t-1}^{2}\mathds{1}\{R_{t-1}<0\}.\end{split}
(28)
We further use two models that use high-frequency information through the RV estimator.
The third model is the Heterogeneous Autoregressive (HAR) model proposed by
Corsi (2009)
,
RV
t
1
/
2
=
β
0
+
β
1
​
RV
t
−
1
1
/
2
+
β
2
​
RV
¯
w
,
t
−
1
1
/
2
+
β
3
​
RV
¯
m
,
t
−
1
1
/
2
+
ε
t
,
with
ε
t
​
∼
iid
​
𝒩
​
(
0
,
σ
2
)
,
\displaystyle{\operatorname{RV}_{t}^{1/2}}=\beta_{0}+\beta_{1}{\operatorname{RV}_{t-1}^{1/2}}+\beta_{2}\overline{\operatorname{RV}}_{{w},t-1}^{1/2}+\beta_{3}\overline{\operatorname{RV}}_{{m},t-1}^{1/2}+\varepsilon_{t},\qquad\text{with}\qquad\varepsilon_{t}\overset{\text{iid}}{\sim}\mathcal{N}(0,\sigma^{2}),
where
RV
¯
w
,
t
1
/
2
:=
1
5
​
∑
j
=
0
4
RV
t
−
j
1
/
2
\overline{\operatorname{RV}}_{w,t}^{1/2}:=\frac{1}{5}\sum_{j=0}^{4}{\operatorname{RV}_{t-j}^{1/2}}
and
RV
¯
m
,
t
1
/
2
:=
1
22
​
∑
j
=
0
21
RV
t
−
j
1
/
2
\overline{\operatorname{RV}}_{m,t}^{1/2}:=\frac{1}{22}\sum_{j=0}^{21}{\operatorname{RV}}_{t-j}^{1/2}
are weekly and monthly averages, respectively.
Fourth, we employ the MIDAS model of
Ghysels et al. (2006)
;
Ghysels et al. (2016)
, where
RV
t
1
/
2
{\operatorname{RV}_{t}^{1/2}}
is predicted based on a weighted average of its lagged values,
RV
t
1
/
2
=
ϕ
0
+
∑
l
=
1
20
w
l
​
RV
t
−
l
1
/
2
+
ε
t
,
with
ε
t
​
∼
iid
​
𝒩
​
(
0
,
σ
2
)
,
\displaystyle\operatorname{RV}_{t}^{1/2}=\phi_{0}+\sum_{l=1}^{20}w_{l}\operatorname{RV}_{t-l}^{1/2}+\varepsilon_{t},\quad\text{with}\quad\varepsilon_{t}\overset{\text{iid}}{\sim}\mathcal{N}(0,\sigma^{2}),
where the MIDAS weights
w
l
w_{l}
are parameterized through the exponential Almon polynomial.
We construct VaR forecasts for these four models by multiplying the square root of the respective variance forecast with the
α
\alpha
-quantile of the imposed Gaussian residual distribution for all models but the GJR-GARCH, where we use a
t
t
-distribution.
For quantile forecasts, we additionally use the classical Historical Simulation (HS) method, that uses the empirical
α
\alpha
-quantile of the preceding 250 trading days as a quantile forecast.
For the first four models, we estimate the parameters by maximum likelihood using the imposed residual distributions, based on a fixed estimation window from January 1, 2000, to December 31, 2007, corresponding to approximately the first third of the sample.
The subsequent period from January 1, 2008 to January 1, 2022 serves as evaluation period, yielding
T
=
3617
T=3617
one-step ahead forecasts and corresponding realizations.
Figure
D.2
in Appendix
D
shows the variance and VaR forecasts together with their evaluation targets.
Figure 5
:
Variance forecast evaluation results for the E-mini futures using a) the QLIKE and b) the squared error scoring functions.
The left “
𝖬𝖢𝖡
\mathsf{MCB}
–
𝖣𝖲𝖢
\mathsf{DSC}
” plots show the average score as iso-lines together with its decomposition into miscalibration and discrimination components for the four competing forecasts.
The gray boxes in the right panels display the
p
p
-values of tests for zero miscalibration and discrimination, respectively.
The white boxes display the average score, miscalibration and discrimination differences, together with 0 to 3 stars indicating significance at the 10%, 5%, and 1% levels.
Figure
5
presents the evaluation of variance forecasts under the QLIKE and SE scoring functions. The left panels, following
Dimitriadis et al. (2024b)
, plot the estimated miscalibration and discrimination of the four forecasting methods along the axes. Gray iso-lines represent average score levels, with observations closer to the upper-left corner indicating superior performance.
We find that the RV-based forecasting methods exhibit markedly stronger discrimination, which translates into better overall predictive accuracy as reflected in the average scores.
The right panel of Figure
5
reports the corresponding test results:
Gray-shaded boxes display
p
p
-values for tests of zero miscalibration and zero discrimination. While all models show significantly positive discrimination, the null of correct calibration is rejected more frequently for the RV-based models than for the two GARCH-type specifications.
The remaining off-diagonal panels present pairwise differences in average scores (
Δ
​
𝖲
^
\Delta\widehat{\mathsf{S}}
), miscalibration (
Δ
​
𝖬𝖢𝖡
^
\Delta\widehat{\mathsf{MCB}}
), and discrimination (
Δ
​
𝖣𝖲𝖢
^
\Delta\widehat{\mathsf{DSC}}
), with significance indicated by 0 to 3 stars corresponding to the 10%, 5%, and 1% levels.
Focusing on the lower column, which compares the GARCH model to the three alternatives, most differences are highly significant.
In particular, the inferior performance of the GARCH model is primarily driven by its significantly weaker discrimination, consistent with the informational advantage of RV-based models that exploit high-frequency data.
Table 5
:
Backtesting results for
1
%
1\%
and
5
%
5\%
VaR forecasts. The first panel displays the
p
p
-values of the backtests summarized in Table
2
.
The column “Basel” also displays the colors of their traffic light system.
The last column reports the relative frequencies of hits, i.e., how often the realizations exceed the VaR forecasts.
p-values backtests
Model
UC
Basel
CC
NZ
VQR
DQ
DQX
hit freq.
1
%
1\%
-VaR
HS
0.137
0.024
0.149
0.124
0.321
0.002
0.004
1.3
%
1.3\%
GARCH
0.001
0.000
0.002
0.000
0.006
0.023
0.016
1.8
%
1.8\%
GJR
0.000
0.000
0.000
0.000
0.000
0.002
0.001
2.0
%
2.0\%
HAR
0.000
0.000
0.000
0.000
0.003
0.000
0.000
2.3
%
2.3\%
MIDAS
0.000
0.000
0.000
0.000
0.000
0.000
0.000
2.3
%
2.3\%
5
%
5\%
-VaR
HS
0.700
0.303
0.006
0.416
0.013
0.000
0.000
5.2%
GARCH
0.266
0.117
0.543
0.140
0.452
0.066
0.052
5.4%
GJR
0.161
0.069
0.313
0.073
0.360
0.207
0.534
5.5%
HAR
0.298
0.132
0.588
0.159
0.518
0.190
0.132
5.4%
MIDAS
0.266
0.117
0.544
0.145
0.568
0.183
0.134
5.4%
Turning to the VaR evaluation results, Table
5
reports the
p
p
-values of seven standard VaR backtests—described in Section
3.5
and Table
2
—along with the unconditional hit frequency in the final column.
Strikingly, particularly at the 1% level, the simple HS model appears to be the best calibrated, whereas all competing models are consistently rejected across the backtests.
Although evidence at the 5% level and for conditional calibration backtests is weak or inconclusive, the 1% level remains the most relevant for risk management
(
Basel Committee, 2019b
, p. 81)
.
Figure 6
:
VaR forecast evaluation results for the E-mini futures at quantile levels a)
1
%
1\%
and b)
5
%
5\%
for the check loss function and its decomposition terms.
For details, see the caption of Figure
5
.
Score decompositions with their associated inference help explain the seemingly superior performance of the HS model. Figure
6
presents these decompositions, analogous to Figure
5
, using the check loss function for 1% and 5% VaR forecasts.
At the 1% level, the
𝖬𝖢𝖡
\mathsf{MCB}
–
𝖣𝖲𝖢
\mathsf{DSC}
plot in Figure
6
shows that, although the HS model exhibits the best calibration, it has by far the weakest discrimination.
This results in clearly inferior predictive performance according to the check loss, as further confirmed by the strongly significant results in the right panel.
These findings resolve the seemingly contradictory results highlighted in the motivational example from Section
1.1
and underscore the risk of evaluating forecasts solely on calibration.
As such, they point to a potentially serious shortcoming in current banking regulation.
At the 5% level, the HS model shows markedly poorer
conditional
calibration, as reflected both in the backtest results in Table
5
and in the score decomposition in Figure
6
.
The relative ordering of the other four models, however, is similar to that observed at the 1% level, with generally stronger significance, which can be attributed to lower noise at less extreme probability levels.
A general pattern evident in the
𝖬𝖢𝖡
\mathsf{MCB}
–
𝖣𝖲𝖢
\mathsf{DSC}
plot at the 1% level—and, to a lesser extent, at the 5% level and for the variance forecasts in Figure
5
—is that models incorporating more information can convert it into higher discrimination.
However, this often comes at the cost of increased miscalibration.
Notably, achieving auto-calibration conditional on
𝑾
i
​
t
=
(
1
,
X
i
​
t
)
\bm{W}_{it}=(1,X_{it})
is relatively easy when forecasts
X
i
​
t
X_{it}
are nearly constant, but much more difficult for highly discriminating forecasts that vary substantially over time.
This observation calls into question the common practice of evaluating risk measure forecasts primarily through MZ-type backtests
(
Gaglianone et al., 2011
;
Guler et al., 2017
;
Bayer and Dimitriadis, 2022
)
, which focus on auto-calibration.
Figures
D.4
–
D.5
in Appendix
D
present diagnostic checks for the linear recalibration regressions underlying the score decompositions of the variance and VaR forecasts.
The pointwise confidence bands largely cover the null specification, providing no evidence against correct model specification.
This supports the use of linear recalibration for score decompositions in these applications, combining robustness and adequate fit with the ability to conduct inference, which is essential in the settings considered.
6
Conclusion
This paper has established a comprehensive inferential framework for score decompositions, enabling a more granular assessment of predictive performance through the lenses of miscalibration, discrimination, and uncertainty.
By utilizing a linear recalibration technique, we have shown that it is possible to derive misspecification-robust inference for a wide range of point forecasts—including those governed by non-smooth loss functions—while maintaining attractive finite sample non-negativity conditions and a formal bridge to the classical
Mincer and Zarnowitz (1969)
regression.
Our results demonstrate that this decomposition approach enriches the informational content of traditional predictive ability tests.
Through our empirical applications, we have highlighted how these methods can reveal significant latent differences in forecast discrimination and, crucially, identify systemic deficiencies in financial risk backtesting that current banking regulations fail to capture.
The linear recalibration specification is exact under the null hypotheses of perfect calibration or zero discrimination and provides a stable and flexible approximation more generally.
It naturally accommodates additional recalibration variables, facilitating extensions to, for example, cross-calibration
(
Strähl and Ziegel, 2017
)
and links to VaR backtesting and macroeconomic survey forecasts
(
Coibion and Gorodnichenko, 2015
)
.
Compared with nonparametric alternatives, the linear specification is also less susceptible to overfitting, particularly in the small-to-moderate sample sizes considered here. Moreover, the appendix reports no empirical evidence against the linearity assumption in our applications.
Nonetheless, particularly in data-rich environments, semiparametric extensions that estimate the recalibration curve nonparametrically—using kernel, spline, or isotonic regression—represent promising avenues for future research.
Such developments could build on the seminal work of
Newey (1994)
regarding two-step semiparametric inference and more recent advances in isotonic plug-in estimation, such as
Xu (2022)
.
We treat the possibly model-based forecasts as the finalized output of a specific sequence of modeling choices, including parameter estimation.
Consequently, we formulate our hypotheses based on the realized quality of these forecasts rather than on the properties of the underlying models themselves.
In contrast, the framework of
West (1996)
assesses whether two forecasting
models
based on their pseudo-true parameters would exhibit equal predictive accuracy, hence requiring that the test statistic’s standardization explicitly accounts for the asymptotic noise introduced by parameter estimation.
This extension can be integrated into our framework by redefining the population
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
and
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
components in a model-based environment and replacing the central limit theorem in Assumption
3.3
(ii)
with the asymptotic approximations of
West (1996)
, or with the numerous refinements and generalizations proposed in subsequent work.
Generalizations of our framework to other elicitable functionals, such as expectiles, are straightforward.
However, functionals that are merely jointly or multi-objective elicitable following
Fissler and Ziegel (2016)
and
Fissler and Hoga (2024)
—such as the variance (when the mean is unknown), the Expected Shortfall, or the systemic risk measures Co-Value-at-Risk and Marginal Expected Shortfall—require additional care.
In these cases, the underlying recalibration regressions necessitate the estimation of conditional models for the associated nuisance components, such as the mean or the VaR
(
Patton et al., 2019
;
Bayer and Dimitriadis, 2022
;
Dimitriadis and Hoga, 2026
)
.
The propagation of estimation risk from these nuisance quantities into the final score decomposition represents a non-trivial extension of the current inferential framework.
In conclusion, the contributions of this paper extend beyond their immediate applications in econometrics and finance. The principles of score decomposition and linear recalibration constitute a versatile toolkit for any domain where predictive accuracy is paramount, from meteorology to machine learning. The framework proposed herein represents a fundamental shift in perspective: from merely asking
which
forecast is better to diagnosing
why
it is better. As the complexity of our models and the richness of our data continue to grow, this diagnostic approach will be essential for robust and reliable decision-making.
Acknowledgments
Timo Dimitriadis acknowledges funding by the German Research Foundation (DFG) through the projects 502572912 and 568876076.
We gratefully acknowledge the Hohenheim Datalab (DALAHO) for providing access to Refinitiv TickHistory.
We thank all seminar and conference participants who provided feedback on earlier versions of this paper.
In particular, we are grateful to Sam Allen, Tillman Gneiting, Daniel Gutknecht, Alexander Jordan, Robert Jung, Fabian Krüger, Andrew Patton, Winfried Pohlmeier, Johannes Resin, Karsten Schweikert, and Johanna Ziegel for their valuable comments and suggestions.
Declaration of generative AI use
During the preparation of this work, the authors used the AI tools ChatGPT and Gemini for language editing, code generation, and assistance in setting up the simulation process for quantile forecasts described in Appendix
C
.
After using these tools, the authors reviewed and edited the content as needed and take full responsibility for the content of the article.
References
Allen
et al.
(2025)
S. Allen, J. Burnello, and J. Ziegel
Assessing the conditional calibration of interval forecasts using decompositions of the interval score
.
Preprint
.
Note:
https://arxiv.org/abs/2508.18034
Cited by:
§1.3
,
§3.1
,
§3.1
.
Andrews (1991)
D. W. K. Andrews
Heteroskedasticity and autocorrelation consistent covariance matrix estimation
.
Econometrica
59
(
3
),
pp. 817–858
.
External Links:
ISSN 00129682, 14680262
,
Link
Cited by:
§3.2
,
§4.2
.
Andrews (1994)
D. Andrews
Empirical process methods in econometrics
.
In
Handbook of Econometrics
,
R. Engle and D. McFadden (Eds.)
,
Vol.
4
,
pp. 2247–2294
.
Cited by:
§3.2
.
Angeletos
et al.
(2021)
G. Angeletos, Z. Huo, and K. A. Sastry
Imperfect macroeconomic expectations: evidence and theory
.
NBER Macroeconomics Annual
35
(
),
pp. 1–86
.
External Links:
Document
,
Link
,
https://doi.org/10.1086/712313
Cited by:
§1.3
.
Angrist
et al.
(2006)
J. Angrist, V. Chernozhukov, and I. Fernandez-Val
Quantile regression under misspecification, with an application to the u.s. wage structure
.
Econometrica
74
(
2
),
pp. 539–563
.
Cited by:
§3.1
.
Arnold
et al.
(2024)
S. Arnold, E. Walz, J. Ziegel, and T. Gneiting
Decompositions of the mean continuous ranked probability score
.
Electronic Journal of Statistics
18
(
2
),
pp. 4992–5044
.
Cited by:
§1.2
,
§1.3
.
Basel Committee (1996)
Basel Committee
Overview of the amendment to the capital accord to incorporate market risks
.
Technical report
Bank for International Settlements
.
Note:
http://www.bis.org/publ/bcbs23.pdf
Cited by:
§1.3
,
§3.5
,
Table 2
.
Basel Committee (2019a)
Basel Committee
CRE: Calculation of RWA for credit risk
.
Technical report
Bank for International Settlements
.
Note:
https://www.bis.org/basel_framework/chapter/CRE/36.htm?inforce=20191215&published=20191215&export=pdf
Cited by:
§1.1
,
§1
.
Basel Committee (2019b)
Basel Committee
Minimum capital requirements for market risk
.
Technical report
Bank for International Settlements
.
Note:
https://www.bis.org/bcbs/publ/d457.pdf
Cited by:
§1.1
,
§1.3
,
§1
,
§3.5
,
§5.2
.
Bayer and Dimitriadis (2022)
S. Bayer and T. Dimitriadis
Regression-based Expected Shortfall backtesting
.
Journal of Financial Econometrics
20
(
3
),
pp. 437–471
.
External Links:
ISSN 1479-8409
,
Document
,
Link
,
https://academic.oup.com/jfec/article-pdf/20/3/437/43974203/nbaa013.pdf
Cited by:
§1
,
§2.3
,
§5.2
,
§6
.
Bentzien and Friederichs (2014)
S. Bentzien and P. Friederichs
Decomposition and graphical portrayal of the quantile score
.
Quarterly Journal of the Royal Meteorological Society
140
(
683
),
pp. 1924–1934
.
Cited by:
§1.1
,
§1.3
.
Berger (1997)
R. L. Berger
Likelihood ratio tests and intersection-union tests
.
In
Advances in Statistical Decision Theory and Applications
,
S. Panchapakesan and N. Balakrishnan (Eds.)
,
pp. 225–237
.
External Links:
ISBN 978-1-4612-2308-5
,
Document
,
Link
Cited by:
§1.2
,
§3.3
.
Berkowitz
et al.
(2011)
J. Berkowitz, P. Christoffersen, and D. Pelletier
Evaluating Value-at-Risk models with desk-level data
.
Management Science
57
(
12
),
pp. 2213–2227
.
External Links:
ISSN 00251909, 15265501
,
Link
Cited by:
§1.3
.
Bollerslev
et al.
(2018)
T. Bollerslev, B. Hood, J. Huss, and L. H. Pedersen
Risk everywhere: modeling and managing volatility
.
The Review of Financial Studies
31
(
7
),
pp. 2729–2773
.
External Links:
ISSN 0893-9454
,
Document
,
Link
,
https://academic.oup.com/rfs/article-pdf/31/7/2729/25102779/hhy041.pdf
Cited by:
§5.2
.
Bollerslev (1986)
T. Bollerslev
Generalized autoregressive conditional heteroskedasticity
.
Journal of Econometrics
31
(
3
),
pp. 307–327
.
External Links:
ISSN 0304-4076
,
Document
,
Link
Cited by:
§1.1
,
§5.2
.
Bordalo
et al.
(2020)
P. Bordalo, N. Gennaioli, Y. Ma, and A. Shleifer
Overreaction in macroeconomic expectations
.
American Economic Review
110
(
9
),
pp. 2748–82
.
External Links:
Document
,
Link
Cited by:
§1.3
.
Brehmer
et al.
(2024)
J. R. Brehmer, K. Kraus, T. Gneiting, M. Herrmann, and W. Marzocchi
Enhancing the statistical evaluation of earthquake forecasts—an application to Italy
.
Seismological Research Letters
96
(
3
),
pp. 1966–1988
.
External Links:
ISSN 0895-0695
,
Document
,
Link
,
https://pubs.geoscienceworld.org/ssa/srl/article-pdf/96/3/1966/7068564/srl-2024209.1.pdf
Cited by:
§1.3
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
Appendix B
.
Bröcker (2009)
J. Bröcker
Reliability, sufficiency, and the decomposition of proper scores
.
Quarterly Journal of the Royal Meteorological Society
135
(
643
),
pp. 1512–1519
.
Cited by:
§1.1
,
§1.3
.
Broer and Kohlhas (2024)
T. Broer and A. N. Kohlhas
Forecaster (mis-)behavior
.
Review of Economics and Statistics
106
(
5
),
pp. 1334–1351
.
Cited by:
§1.3
.
Campbell (2007)
S. D. Campbell
A review of backtesting and backtesting procedures
.
Journal of Risk
9
(
2
),
pp. 1–17
.
External Links:
Document
,
Link
Cited by:
§3.5
.
Choe and Ramdas (2024)
Y. J. Choe and A. Ramdas
Comparing sequential forecasters
.
Operations Research
72
(
4
),
pp. 1368–1387
.
Cited by:
§1.3
.
Christoffersen (1998)
P. Christoffersen
Evaluating interval forecasts
.
International Economic Review
39
(
4
),
pp. 841–862
.
External Links:
ISSN 00206598, 14682354
,
Link
Cited by:
§1.3
,
§3.5
,
Table 2
.
Clark and McCracken (2001)
T. E. Clark and M. W. McCracken
Tests of equal forecast accuracy and encompassing for nested models
.
Journal of Econometrics
105
(
1
),
pp. 85–110
.
Cited by:
§1.3
.
Clark and McCracken (2013)
T. Clark and M. McCracken
Advances in forecast evaluation
.
In
Handbook of Economic Forecasting
,
G. Elliott and A. Timmermann (Eds.)
,
Handbook of Economic Forecasting
, Vol.
2
,
pp. 1107–1201
.
External Links:
ISSN 1574-0706
,
Document
,
Link
Cited by:
§1.3
.
Coibion and Gorodnichenko (2015)
O. Coibion and Y. Gorodnichenko
Information rigidity and the expectations formation process: a simple framework and new facts
.
American Economic Review
105
(
8
),
pp. 2644–2678
.
External Links:
ISSN 00028282
,
Link
Cited by:
§1.3
,
§3.1
,
§6
.
Corsi (2009)
F. Corsi
A simple approximate long-memory model of Realized Volatility
.
Journal of Financial Econometrics
7
(
2
),
pp. 174–196
.
External Links:
ISSN 1479-8409
,
Document
,
Link
,
https://academic.oup.com/jfec/article-pdf/7/2/174/2543795/nbp001.pdf
Cited by:
§1.1
,
§5.2
,
§5.2
.
Davidson (1994)
J. Davidson
Stochastic limit theory: an introduction for econometricians
.
Advanced Texts in Econometrics
,
Oxford Univerity Press
,
Oxford
.
External Links:
ISBN 9780191525049
,
Link
Cited by:
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
.
Dawid (1986)
A. P. Dawid
Probability forecasting
.
In
Encyclopedia of Statistical Sciences
,
S. Kotz, N. L. Johnson, and C. B. Read. (Eds.)
,
Vol.
7
,
pp. 210–218
.
External Links:
Document
,
Link
,
https://onlinelibrary.wiley.com/doi/pdf/10.1002/0471667196.ess2064
Cited by:
§1.1
.
DeGroot and Fienberg (1981)
M. H. DeGroot and S. E. Fienberg
Assessing probability assessors: calibration and refinement
.
Technical report
Cited by:
§1.3
.
Diebold and Mariano (1995)
F. X. Diebold and R. S. Mariano
Comparing predictive accuracy
.
Journal of Business & Economic Statistics
20
(
1
),
pp. 134–144
.
External Links:
Document
,
Link
,
https://doi.org/10.1198/073500102753410444
Cited by:
§1.1
,
§1.2
,
§1.3
,
§2.2
.
Diebold
et al.
(1998)
F. X. Diebold, T. A. Gunther, and A. S. Tay
Evaluating density forecasts with applications to financial risk management
.
International Economic Review
39
(
4
),
pp. 863–883
.
External Links:
Document
Cited by:
§1
.
Diebold (2015)
F. X. Diebold
Comparing predictive accuracy, twenty years later: a personal perspective on the use and abuse of Diebold–Mariano tests
.
Journal of Business & Economic Statistics
33
(
1
),
pp. 1–9
.
Cited by:
§1.3
.
Dimitriadis
et al.
(2024a)
T. Dimitriadis, T. Fissler, and J. Ziegel
Characterizing M-estimators
.
Biometrika
111
(
1
),
pp. 339–346
.
Cited by:
footnote 2
.
Dimitriadis
et al.
(2024b)
T. Dimitriadis, T. Gneiting, A. I. Jordan, and P. Vogel
Evaluating probabilistic classifiers: the triptych
.
International Journal of Forecasting
40
(
3
),
pp. 1101–1122
.
External Links:
ISSN 0169-2070
,
Document
,
Link
Cited by:
§1.3
,
§5.2
.
Dimitriadis
et al.
(2021)
T. Dimitriadis, T. Gneiting, and A. I. Jordan
Stable reliability diagrams for probabilistic classifiers
.
Proceedings of the National Academy of Sciences
118
(
8
),
pp. 1–10
.
External Links:
Document
Cited by:
§1.1
,
§1.2
,
§1.3
,
§2.3
,
§3.1
,
§3.1
.
Dimitriadis and Hoga (2026)
T. Dimitriadis and Y. Hoga
Regressions under adverse conditions
.
Journal of Business & Economic Statistics
44
(
1
),
pp. 227–241
.
Cited by:
Appendix D
,
§6
.
Duchesne and Lafaye De Micheaux (2010)
P. Duchesne and P. Lafaye De Micheaux
Computing the distribution of quadratic forms: further comparisons between the Liu-Tang-Zhang approximation and exact methods
.
Computational Statistics and Data Analysis
54
,
pp. 858–862
.
Cited by:
§3.3
.
Ehm
et al.
(2016)
W. Ehm, T. Gneiting, A. Jordan, and F. Krüger
Of quantiles and expectiles: consistent scoring functions, choquet representations and forecast rankings
.
Journal of the Royal Statistical Society Series B: Statistical Methodology
78
(
3
),
pp. 505–562
.
External Links:
ISSN 1369-7412
,
Document
,
Link
,
https://academic.oup.com/jrsssb/article-pdf/78/3/505/49236469/jrsssb_78_3_505.pdf
Cited by:
§1.2
,
§5.1
,
§5.1
,
§5.1
,
§5.1
.
Elliott
et al.
(2016)
G. Elliott, D. Ghanem, and F. Krüger
Forecasting conditional probabilities of binary outcomes under misspecification
.
Review of Economics and Statistics
98
(
4
),
pp. 742–755
.
Cited by:
§1
,
footnote 2
.
Elliott and Timmermann (2016)
G. Elliott and A. Timmermann
Economic forecasting
.
Princeton University Press
.
Cited by:
Appendix B
,
§1.1
,
§2.3
.
Engle and Manganelli (2004)
R. F. Engle and S. Manganelli
CAViaR: conditional autoregressive value at risk by regression quantiles
.
Journal of Business & Economic Statistics
22
(
4
),
pp. 367–381
.
External Links:
Document
,
Link
,
https://doi.org/10.1198/073500104000000370
Cited by:
Table 2
.
Farmer
et al.
(2024)
L. E. Farmer, E. Nakamura, and J. Steinsson
Learning about the long run
.
Journal of Political Economy
132
(
10
),
pp. 3334–3377
.
External Links:
Document
Cited by:
§1.3
.
Faust and Wright (2013)
J. Faust and J. H. Wright
Forecasting inflation
.
In
Handbook of Economic Forecasting
,
G. Elliott and A. Timmermann (Eds.)
,
Vol.
2
,
pp. 2–56
.
External Links:
ISSN 1574-0706
,
Document
,
Link
Cited by:
§5.1
.
Fissler and Hoga (2024)
T. Fissler and Y. Hoga
Backtesting systemic risk forecasts using multi-objective elicitability
.
Journal of Business & Economic Statistics
42
(
2
),
pp. 485–498
.
Cited by:
§6
.
Fissler
et al.
(2022)
T. Fissler, C. Lorentzen, and M. Mayer
Model comparison and calibration assessment: user guide for consistent scoring functions in machine learning and actuarial practice
.
Preprint
.
Note:
https://arxiv.org/abs/2202.12780
Cited by:
§1.3
.
Fissler and Ziegel (2016)
T. Fissler and J. F. Ziegel
Higher order elicitability and Osband’s principle
.
The Annals of Statistics
44
(
4
),
pp. 1680 – 1707
.
External Links:
Document
,
Link
Cited by:
§6
.
Fosten
et al.
(2024)
J. Fosten, D. Gutknecht, and M. Pohle
Testing quantile forecast optimality
.
Journal of Business & Economic Statistics
42
(
4
),
pp. 1367–1378
.
Cited by:
§1.3
.
Gaglianone
et al.
(2011)
W. P. Gaglianone, L. R. Lima, O. Linton, and D. R. Smith
Evaluating Value-at-Risk models via quantile regression
.
Journal of Business & Economic Statistics
29
(
1
),
pp. 150–160
.
Cited by:
§1.3
,
§1
,
§2.3
,
§3.2
,
§3.3
,
§3.4
,
§3.5
,
Table 2
,
§5.2
.
Galvao and Yoon (2024)
A. F. Galvao and J. Yoon
HAC covariance matrix estimation in quantile regression
.
Journal of the American Statistical Association
119
(
547
),
pp. 2305–2316
.
External Links:
Document
Cited by:
§3.2
,
§4.2
.
Ghysels
et al.
(2016)
E. Ghysels, V. Kvedaras, and V. Zemlys
Mixed frequency data sampling regression models: the R package midasr
.
Journal of Statistical Software
72
(
4
),
pp. 1–35
.
External Links:
Link
,
Document
Cited by:
§5.2
.
Ghysels
et al.
(2006)
E. Ghysels, P. Santa-Clara, and R. Valkanov
Predicting volatility: getting the most out of return data sampled at different frequencies
.
Journal of Econometrics
131
(
1
),
pp. 59–95
.
External Links:
ISSN 0304-4076
,
Document
,
Link
Cited by:
§5.2
.
Giacomini and White (2006)
R. Giacomini and H. White
Tests of conditional predictive ability
.
Econometrica
74
(
6
),
pp. 1545–1578
.
Cited by:
§1.3
.
Glosten
et al.
(1993)
L. R. Glosten, R. Jagannathan, and D. E. Runkle
On the relation between the expected value and the volatility of the nominal excess return on stocks
.
The Journal of Finance
48
(
5
),
pp. 1779–1801
.
Cited by:
§5.2
.
Gneiting
et al.
(2007)
T. Gneiting, F. Balabdaoui, and A. E. Raftery
Probabilistic forecasts, calibration and sharpness
.
Journal of the Royal Statistical Society Series B: Statistical Methodology
69
(
2
),
pp. 243–268
.
Cited by:
§1
.
Gneiting and Resin (2023)
T. Gneiting and J. Resin
Regression diagnostics meets forecast evaluation: Conditional calibration, reliability diagrams, and coefficient of determination
.
Electronic Journal of Statistics
17
(
2
),
pp. 3226–3286
.
External Links:
Document
,
Link
Cited by:
Appendix B
,
§1.1
,
§1.2
,
§1.3
,
§1.3
,
§1
,
§3.1
,
§3.1
.
Gneiting
et al.
(2023)
T. Gneiting, D. Wolffram, J. Resin, K. Kraus, J. Bracher, T. Dimitriadis, V. Hagenmeyer, A. I. Jordan, S. Lerch, K. Phipps, and M. Schienle
Model diagnostics and forecast evaluation for quantiles
.
Annual Review of Statistics and Its Application
10
(
1
),
pp. 597–621
.
External Links:
Document
,
Link
,
https://doi.org/10.1146/annurev-statistics-032921-020240
Cited by:
§1.1
,
§1.3
.
Gneiting (2011)
T. Gneiting
Making and evaluating point forecasts
.
Journal of the American Statistical Association
106
(
494
),
pp. 746–762
.
External Links:
Document
,
Link
,
https://doi.org/10.1198/jasa.2011.r10138
Cited by:
§1
,
§2.1
,
§2.2
,
§2.2
,
§2.2
.
Guler
et al.
(2017)
K. Guler, P. T. Ng, and Z. Xiao
Mincer-Zarnowitz quantile and expectile regressions for forecast evaluations under aysmmetric loss functions
.
Journal of Forecasting
36
(
6
),
pp. 651–679
.
Cited by:
§1
,
§2.3
,
§5.2
.
Hansen (1996)
B. E. Hansen
Stochastic equicontinuity for unbounded dependent heterogeneous arrays
.
Econometric Theory
12
(
2
),
pp. 347–359
.
Cited by:
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
§3.4
,
§3.4
.
Hansen
et al.
(2011)
P. R. Hansen, A. Lunde, and J. M. Nason
The model confidence set
.
Econometrica
79
(
2
),
pp. 453–497
.
External Links:
Document
,
Link
,
https://onlinelibrary.wiley.com/doi/pdf/10.3982/ECTA5771
Cited by:
§1.3
.
Hansen (2005)
P. R. Hansen
A test for superior predictive ability
.
Journal of Business & Economic Statistics
23
(
4
),
pp. 365–380
.
Cited by:
§1.3
.
He
et al.
(2022)
X. D. He, S. Kou, and X. Peng
Risk measures: robustness, elicitability, and backtesting
.
Annual Review of Statistics and Its Application
9
,
pp. 141–166
.
External Links:
Document
,
Link
,
ISSN 2326-831X
Cited by:
§1.3
.
Henzi and Ziegel (2022)
A. Henzi and J. F. Ziegel
Valid sequential inference on probability forecast performance
.
Biometrika
109
(
3
),
pp. 647–663
.
Cited by:
§1.3
.
Hoga and Demetrescu (2023)
Y. Hoga and M. Demetrescu
Monitoring Value-at-Risk and Expected Shortfall forecasts
.
Management Science
69
(
5
),
pp. 2954–2971
.
External Links:
Document
,
Link
Cited by:
§1.3
.
Hoga and Dimitriadis (2023)
Y. Hoga and T. Dimitriadis
On testing equal conditional predictive ability under measurement error
.
Journal of Business & Economic Statistics
41
(
2
),
pp. 364–376
.
Cited by:
§2.1
.
Holzmann and Eulert (2014)
H. Holzmann and M. Eulert
The role of the information set for forecasting—with applications to risk management
.
The Annals of Applied Statistics
8
(
1
),
pp. 595 – 621
.
External Links:
Document
,
Link
Cited by:
§2.2
,
footnote 6
,
footnote 7
.
Imhof (1961)
J. P. Imhof
Computing the distribution of quadratic forms in normal variables
.
Biometrika
48
(
3/4
),
pp. 419–426
.
External Links:
ISSN 00063444, 14643510
,
Link
Cited by:
§3.3
,
§3.3
.
Kim and White (2003)
T. Kim and H. White
Estimation, inference, and specification testing for possibly misspecified quantile regression
.
In
Maximum Likelihood Estimation of Misspecified Models: Twenty Years Later
,
pp. 107–132
.
External Links:
Document
,
Link
,
https://www.emeraldinsight.com/doi/pdf/10.1016/S0731-9053%2803%2917005-3
Cited by:
§3.1
.
Kohlhas and Walther (2021)
A. N. Kohlhas and A. Walther
Asymmetric attention
.
American Economic Review
111
(
9
),
pp. 2879–2925
.
Cited by:
§1.3
.
Komunjer (2005)
I. Komunjer
Quasi-maximum likelihood estimation for conditional quantiles
.
Journal of Econometrics
128
(
1
),
pp. 137–164
.
External Links:
Link
Cited by:
§3.1
,
§3.4
.
Kuester
et al.
(2005)
K. Kuester, S. Mittnik, and M. S. Paolella
Value-at-Risk prediction: a comparison of alternative strategies
.
Journal of Financial Econometrics
4
(
1
),
pp. 53–89
.
External Links:
ISSN 1479-8409
,
Document
,
Link
,
https://academic.oup.com/jfec/article-pdf/4/1/53/2481517/nbj002.pdf
Cited by:
Table 2
.
Kupiec (1995)
P. H. Kupiec
Techniques for verifying the accuracy of risk measurement models
.
The Journal of Derivatives
3
(
2
),
pp. 73–84
.
External Links:
Document
,
ISSN 1074-1240
,
Link
,
https://jod.pm-research.com/content/3/2/73.full.pdf
Cited by:
§1.3
,
§3.5
,
Table 2
.
Li
et al.
(2022)
J. Li, Z. Liao, and R. Quaedvlieg
Conditional superior predictive ability
.
The Review of Economic Studies
89
(
2
),
pp. 843–875
.
Cited by:
§1.3
.
Liu
et al.
(2015)
L. Y. Liu, A. J. Patton, and K. Sheppard
Does anything beat 5-minute RV? A comparison of realized measures across multiple asset classes
.
Journal of Econometrics
187
(
1
),
pp. 293–311
.
External Links:
ISSN 0304-4076
,
Document
,
Link
Cited by:
§5.2
.
Mincer and Zarnowitz (1969)
J. Mincer and V. Zarnowitz
The evaluation of economic forecasts
.
In
Economic Forecasts and Expectations: Analysis of Forecasting Behavior and Performance
,
J. Mincer (Ed.)
,
pp. 3–46
.
Cited by:
Appendix B
,
Appendix B
,
Appendix B
,
§1.2
,
Table 1
,
§1
,
§2.3
,
§3.1
,
§3.1
,
§3.1
,
§6
.
Mitchell (2019)
K. Mitchell
Score decompositions in forecast verification
.
Ph.D. Thesis
,
University of Exeter
,
Exeter, United Kingdom
.
Cited by:
§1.3
.
Mühlemann (2021)
A. Mühlemann
The role of loss functions in regression problems
.
Ph.D. Thesis
,
University of Bern
,
Bern, Switzerland
.
Cited by:
footnote 2
.
Murphy and Winkler (1992)
A. H. Murphy and R. L. Winkler
Diagnostic verification of probability forecasts
.
International Journal of Forecasting
7
(
4
),
pp. 435–455
.
Cited by:
§2.3
.
Murphy and Winkler (1987)
A. H. Murphy and R. L. Winkler
A general framework for forecast verification
.
Monthly Weather Review
115
(
7
),
pp. 1330 – 1338
.
External Links:
Document
Cited by:
§1.1
,
§3.1
.
Murphy (1973)
A. H. Murphy
A new vector partition of the probability score
.
Journal of Applied Meteorology and Climatology
12
(
4
),
pp. 595–600
.
Cited by:
Appendix B
,
§1.1
,
§1.3
.
Newey and McFadden (1994)
W. K. Newey and D. McFadden
Large sample estimation and hypothesis testing
.
In
Handbook of Econometrics
,
R. Engle and D. McFadden (Eds.)
,
Vol.
4
,
pp. 2111–2245
.
External Links:
ISSN 1573-4412
Cited by:
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
§3.4
.
Newey and West (1987)
W. K. Newey and K. D. West
A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix
.
Econometrica
55
(
3
),
pp. 703–708
.
Cited by:
§3.2
.
Newey (1994)
W. K. Newey
The asymptotic variance of semiparametric estimators
.
Econometrica
,
pp. 1349–1382
.
Cited by:
§6
.
Nieto and Ruiz (2016)
M. R. Nieto and E. Ruiz
Frontiers in VaR forecasting and backtesting
.
International Journal of Forecasting
32
(
2
),
pp. 475–501
.
Cited by:
§3.5
.
Nolde and Ziegel (2017)
N. Nolde and J. F. Ziegel
Elicitability and backtesting: perspectives for banking regulation
.
The Annals of Applied Statistics
11
(
4
),
pp. 1833–1874
.
External Links:
Document
,
Link
Cited by:
§2.3
,
Table 2
.
Patton
et al.
(2019)
A. J. Patton, J. F. Ziegel, and R. Chen
Dynamic semiparametric models for Expected Shortfall (and Value-at-Risk)
.
Journal of Econometrics
211
(
2
),
pp. 388–413
.
Cited by:
§6
.
Patton (2011)
A. J. Patton
Volatility forecast comparison using imperfect volatility proxies
.
Journal of Econometrics
160
(
1
),
pp. 246–256
.
External Links:
ISSN 0304-4076
,
Document
,
Link
Cited by:
§2.2
,
§5.2
.
Patton (2020)
A. J. Patton
Comparing possibly misspecified forecasts
.
Journal of Business & Economic Statistics
38
(
4
),
pp. 796–809
.
External Links:
Document
,
Link
,
https://doi.org/10.1080/07350015.2019.1585256
Cited by:
§1.2
,
§5.1
,
§5.1
,
§5.1
,
§5.1
.
Pohle
et al.
(2024)
M. Pohle, M. Demetrescu, T. Dimitriadis, and J. Wermuth
Generalised residual diagnostics
.
Note:
Mimeo
Cited by:
Appendix D
.
Pohle (2020)
M. Pohle
The Murphy decomposition and the calibration-resolution principle: a new perspective on forecast evaluation
.
Preprint
.
Note:
https://arxiv.org/abs/2005.01835
Cited by:
Appendix B
,
§1.3
,
§2.3
,
§3.1
,
§3.1
.
R Core Team (2026)
R Core Team
R: a language and environment for statistical computing
.
R Foundation for Statistical Computing
,
Vienna, Austria
.
External Links:
Link
Cited by:
§1.4
.
Ranjan and Gneiting (2010)
R. Ranjan and T. Gneiting
Combining probability forecasts
.
Journal of the Royal Statistical Society Series B: Statistical Methodology
72
(
1
),
pp. 71–91
.
Cited by:
§3.1
.
Roelofs
et al.
(2022)
R. Roelofs, N. Cain, J. Shlens, and M. C. Mozer
Mitigating bias in calibration error estimation
.
In
International Conference on Artificial Intelligence and Statistics
,
pp. 4036–4054
.
Cited by:
§1.2
,
§3.1
.
Sanders (1963)
F. Sanders
On subjective probability forecasting
.
Journal of Applied Meteorology and Climatology
2
(
2
),
pp. 191–201
.
Cited by:
§1.3
.
Savage (1971)
L. J. Savage
Elicitation of personal probabilities and expectations
.
Journal of the American Statistical Association
66
(
336
),
pp. 783–801
.
External Links:
Document
,
Link
,
https://www.tandfonline.com/doi/pdf/10.1080/01621459.1971.10482346
Cited by:
§1
.
Siegert (2014)
S. Siegert
Variance estimation for Brier score decomposition
.
Quarterly Journal of the Royal Meteorological Society
140
(
682
),
pp. 1771–1777
.
External Links:
Document
,
Link
,
https://rmets.onlinelibrary.wiley.com/doi/pdf/10.1002/qj.2228
Cited by:
§1.3
.
Siegert (2017)
S. Siegert
Simplifying and generalising Murphy’s Brier score decomposition
.
Quarterly Journal of the Royal Meteorological Society
143
(
703
),
pp. 1178–1183
.
External Links:
Document
,
Link
,
https://rmets.onlinelibrary.wiley.com/doi/pdf/10.1002/qj.2985
Cited by:
§1.3
,
§3.1
.
Strähl and Ziegel (2017)
C. Strähl and J. Ziegel
Cross-calibration of probabilistic forecasts
.
Electronic Journal of Statistics
11
(
1
),
pp. 608–639
.
External Links:
Document
,
Link
Cited by:
§6
.
Theil (1966)
H. Theil
Applied economic forecasting
.
North-Holland
,
Amsterdam
.
Cited by:
§1.3
.
van der Vaart and Wellner (1996)
A. W. van der Vaart and J. A. Wellner
Weak convergence and empirical processes: with applications to statistics
.
Springer Science & Business Media
.
Cited by:
§3.2
.
Wang
et al.
(2025)
Q. Wang, R. Wang, and J. Ziegel
E-backtesting
.
Management Science
.
Note:
https://doi.org/10.1287/mnsc.2023.01659
Cited by:
§1.3
.
West (1996)
K. D. West
Asymptotic inference about predictive ability
.
Econometrica
64
(
5
),
pp. 1067–1084
.
Cited by:
§1.3
,
§6
.
West (2006)
K. D. West
Forecast evaluation
.
Handbook of Economic Forecasting
1
,
pp. 99–134
.
Cited by:
§1.3
.
White (1980)
H. White
Using least squares to approximate unknown regression functions
.
International Economic Review
21
(
1
),
pp. 149–70
.
External Links:
Link
Cited by:
§3.1
.
White (2001)
H. White
Asymptotic theory for econometricians
.
2nd edition
,
Academic Press, San Diego
.
Cited by:
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
Appendix A
,
§3.2
.
Wüthrich
et al.
(2025)
M. V. Wüthrich, R. Richman, B. Avanzi, M. Lindholm, M. Maggi, M. Mayer, J. Schelldorfer, and S. Scognamiglio
AI tools for actuaries
.
Preprint
.
Note:
https://ssrn.com/abstract=5162304
Cited by:
§1.3
.
Xu (2022)
M. Xu
Semiparametric estimation with plug-in isotonic estimator
.
Preprint
.
Note:
https://drive.google.com/file/d/1jAPyEKur8s3ZlWFLuFBg5gEwYpF3DX_n/view?usp=sharing
Cited by:
§6
.
Zeileis (2004)
A. Zeileis
Econometric computing with HC and HAC covariance matrix estimators
.
Journal of Statistical Software
11
(
10
),
pp. 1–17
.
External Links:
Link
,
Document
Cited by:
§4.2
.
Supplementary Material
The supplementary material contains all proofs in Appendix
A
,
a discussion of related score decompositions in Appendix
B
,
details on the quantile simulation DGP in Appendix
C
,
and additional figures for the simulations and applications in Appendix
D
.
The references refer to the bibliography provided in the main paper.
Appendix A
Proofs
Proof of Theorem
3.2
.
For item
(a)
, notice that by the definition of the M-estimator in (
12
), we have that
𝖬𝖢𝖡
^
i
​
T
=
𝖲
^
i
​
T
−
𝖲
^
i
​
T
𝖢
\displaystyle\widehat{\mathsf{MCB}}_{iT}=\widehat{\mathsf{S}}_{iT}-\widehat{\mathsf{S}}^{\mathsf{C}}_{iT}
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
X
i
​
t
,
Y
t
)
−
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
\displaystyle=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(X_{it},Y_{t}\big)-\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t}\big)
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
X
i
​
t
,
Y
t
)
−
min
𝜽
∈
𝚯
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
≥
0
,
\displaystyle=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(X_{it},Y_{t}\big)-\underset{\bm{\theta}\in\bm{\Theta}}{\min}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big)\geq 0,
since
𝑾
i
​
t
\bm{W}_{it}
is assumed to contain an intercept and the forecast
X
i
​
t
X_{it}
.
If
X
i
​
t
=
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
X_{it}=\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}
almost surely,
𝖬𝖢𝖡
^
i
​
T
=
0
\widehat{\mathsf{MCB}}_{iT}=0
is immediate.
For item
(b)
, let
X
i
​
t
≠
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
X_{it}\not=\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}
for some
t
∈
{
1
,
…
,
T
}
t\in\{1,\dots,T\}
with positive probability.
Then, we get that
1
T
​
∑
t
=
1
T
𝖲
⁡
(
X
i
​
t
,
Y
t
)
>
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
=
min
𝜽
∈
𝚯
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
,
\displaystyle\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(X_{it},Y_{t}\big)>\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t}\big)=\underset{\bm{\theta}\in\bm{\Theta}}{\min}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big),
with positive probability, where the inequality holds as the latter minimum is assumed to be unique and
(
0
,
1
,
0
,
…
)
⊤
∈
𝚯
(0,1,0,\dots)^{\top}\in\bm{\Theta}
, for which
𝑾
i
​
t
⊤
​
(
0
,
1
,
0
,
…
)
⊤
=
X
i
​
t
\bm{W}_{it}^{\top}(0,1,0,\dots)^{\top}=X_{it}
.
Thus,
𝖬𝖢𝖡
^
i
​
T
>
0
\widehat{\mathsf{MCB}}_{iT}>0
with positive probability follows.
For item
(c)
, first notice that the empirical distribution of the sample
Y
1
,
…
,
Y
T
Y_{1},\dots,Y_{T}
is contained in
𝒫
\mathcal{P}
as the convex combination of Dirac measures at
Y
1
,
…
,
Y
T
Y_{1},\dots,Y_{T}
, such that the strict consistency of
𝖲
\mathsf{S}
implies that the unconditional functional
r
^
T
\widehat{r}_{T}
coincides with the M-estimator
arg
​
min
r
∈
𝖠
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
,
Y
t
)
\underset{r\in\mathsf{A}}{\argmin}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(r,Y_{t}\big)
.
Hence, we have that
𝖣𝖲𝖢
^
i
​
T
=
𝖲
^
i
​
T
𝖱
−
𝖲
^
i
​
T
𝖢
\displaystyle\widehat{\mathsf{DSC}}_{iT}=\widehat{\mathsf{S}}^{\mathsf{R}}_{iT}-\widehat{\mathsf{S}}^{\mathsf{C}}_{iT}
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
^
T
,
Y
t
)
−
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
\displaystyle=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\widehat{r}_{T},Y_{t}\big)-\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t}\big)
=
min
r
∈
𝖠
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
,
Y
t
)
−
min
𝜽
∈
𝚯
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
≥
0
,
\displaystyle=\underset{r\in\mathsf{A}}{\min}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(r,Y_{t}\big)-\underset{\bm{\theta}\in\bm{\Theta}}{\min}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big)\geq 0,
as
𝑾
i
​
t
\bm{W}_{it}
is assumed to contain an intercept, which nests the first minimization over all
r
∈
𝖠
r\in\mathsf{A}
.
If
r
^
T
=
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
\widehat{r}_{T}=\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}
almost surely,
𝖣𝖲𝖢
^
i
​
T
=
0
\widehat{\mathsf{DSC}}_{iT}=0
is immediate.
For item
(d)
, assume that
r
^
T
≠
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
\widehat{r}_{T}\not=\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}
for some
t
∈
{
1
,
…
,
T
}
t\in\{1,\dots,T\}
with positive probability.
Then,
min
r
∈
𝖠
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
,
Y
t
)
=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
^
T
,
Y
t
)
>
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
=
min
𝜽
∈
𝚯
​
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
,
\displaystyle\underset{r\in\mathsf{A}}{\min}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(r,Y_{t}\big)=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\widehat{r}_{T},Y_{t}\big)>\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t}\big)=\underset{\bm{\theta}\in\bm{\Theta}}{\min}\;\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big),
with positive probability, where the strict inequality holds as the latter minimum is assumed to be unique and
(
r
^
T
,
0
,
…
)
⊤
∈
𝚯
(\widehat{r}_{T},0,\dots)^{\top}\in\bm{\Theta}
, for which
𝑾
i
​
t
⊤
​
(
r
^
T
,
0
,
…
)
⊤
=
r
^
T
\bm{W}_{it}^{\top}(\widehat{r}_{T},0,\dots)^{\top}=\widehat{r}_{T}
.
Thus,
𝖣𝖲𝖢
^
i
​
T
>
0
\widehat{\mathsf{DSC}}_{iT}>0
with positive probability follows, which concludes the proof.
∎
Proof Theorem
3.4
.
We start by decomposing
𝖬𝖢𝖡
^
i
​
T
−
𝖬𝖢𝖡
¯
i
=
A
i
​
T
−
B
i
​
T
−
C
i
​
T
and
𝖣𝖲𝖢
^
i
​
T
−
𝖣𝖲𝖢
¯
i
=
−
B
i
​
T
−
C
i
​
T
+
D
T
+
E
T
\displaystyle\widehat{\mathsf{MCB}}_{iT}-\overline{\mathsf{MCB}}_{i}=A_{iT}-B_{iT}-C_{iT}\qquad\text{ and }\qquad{\widehat{\mathsf{DSC}}}_{iT}-\overline{\mathsf{DSC}}_{i}=-B_{iT}-C_{iT}+D_{T}+E_{T}
where
A
i
​
T
\displaystyle A_{iT}
:
=
1
T
​
∑
t
=
1
T
a
i
​
t
:=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
X
i
​
t
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
,
Y
t
)
]
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}a_{it}:=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(X_{it},Y_{t})-\mathbb{E}[\mathsf{S}(X_{it},Y_{t})]
B
i
​
T
\displaystyle B_{iT}
:
=
1
T
​
∑
t
=
1
T
b
i
​
t
​
T
:=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
−
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}b_{itT}:=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t})-\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})
C
i
​
T
\displaystyle C_{iT}
:
=
1
T
​
∑
t
=
1
T
c
i
​
t
:=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}c_{it}:=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})-\mathbb{E}[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})]
D
T
\displaystyle D_{T}
:
=
1
T
​
∑
t
=
1
T
d
t
​
T
:=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
^
T
,
Y
t
)
−
𝖲
⁡
(
r
¯
,
Y
t
)
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}d_{tT}:=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\hat{r}_{T},Y_{t})-\mathsf{S}(\bar{r},Y_{t})
E
T
\displaystyle E_{T}
:
=
1
T
​
∑
t
=
1
T
e
t
:=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
r
¯
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
r
¯
,
Y
t
)
]
.
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}e_{t}:=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bar{r},Y_{t})-\mathbb{E}[\mathsf{S}(\bar{r},Y_{t})].
Here,
A
i
​
T
A_{iT}
,
C
i
​
T
C_{iT}
and
E
T
E_{T}
capture the difference between sample and population versions of the scores of the original forecasts, the (population) recalibrated and the (population) reference forecasts, respectively.
The terms
B
i
​
T
B_{iT}
and
D
T
D_{T}
capture the estimation effect of the recalibrated and reference forecast, respectively.
We start to show that the estimation effects captured in
T
​
B
i
​
T
\sqrt{T}B_{iT}
(and similarly, in
T
​
D
T
\sqrt{T}D_{T}
) vanish in probability.
For this, we define for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
,
Q
^
i
​
T
​
(
𝜽
)
:=
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
and
Q
¯
i
​
T
​
(
𝜽
)
:=
1
T
​
∑
t
=
1
T
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
,
\displaystyle\widehat{Q}_{iT}(\bm{\theta}):=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\qquad\text{ and }\qquad\overline{Q}_{iT}(\bm{\theta}):=\frac{1}{T}\sum_{t=1}^{T}\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big],
(29)
such that
ν
i
​
T
​
(
𝜽
)
=
T
​
(
Q
^
i
​
T
​
(
𝜽
)
−
Q
¯
i
​
T
​
(
𝜽
)
)
\nu_{iT}(\bm{\theta})=\sqrt{T}\big(\widehat{Q}_{iT}(\bm{\theta})-\overline{Q}_{iT}(\bm{\theta})\big)
for
ν
i
​
T
​
(
𝜽
)
\nu_{iT}(\bm{\theta})
defined in (
15
).
Then, we employ a mean-value theorem in the third equality below to get for some (possibly random)
𝜽
~
i
​
T
\widetilde{\bm{\theta}}_{iT}
that is on the line between
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
and
𝜽
¯
i
\bar{\bm{\theta}}_{i}
that
T
​
B
i
​
T
=
T
​
Q
^
i
​
T
​
(
𝜽
^
i
​
T
)
−
T
​
Q
^
i
​
T
​
(
𝜽
¯
i
)
=
T
​
(
Q
¯
i
​
T
​
(
𝜽
^
i
​
T
)
−
Q
¯
i
​
T
​
(
𝜽
¯
i
)
)
+
(
ν
i
​
T
​
(
𝜽
^
i
​
T
)
−
ν
i
​
T
​
(
𝜽
¯
i
)
)
=
∇
𝜽
Q
¯
i
​
T
​
(
𝜽
~
i
​
T
)
⋅
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
+
(
ν
i
​
T
​
(
𝜽
^
i
​
T
)
−
ν
i
​
T
​
(
𝜽
¯
i
)
)
=
o
ℙ
​
(
1
)
⋅
𝒪
ℙ
​
(
1
)
+
o
ℙ
​
(
1
)
=
o
ℙ
​
(
1
)
.
\displaystyle\begin{aligned} \sqrt{T}B_{iT}&=\sqrt{T}\widehat{Q}_{iT}(\widehat{\bm{\theta}}_{iT})-\sqrt{T}\widehat{Q}_{iT}(\bar{\bm{\theta}}_{i})\\
&=\sqrt{T}\left(\overline{Q}_{iT}(\widehat{\bm{\theta}}_{iT})-\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})\right)+\left(\nu_{iT}(\widehat{\bm{\theta}}_{iT})-\nu_{iT}(\bar{\bm{\theta}}_{i})\right)\\
&=\nabla_{\bm{\theta}}\overline{Q}_{iT}(\widetilde{\bm{\theta}}_{iT})\cdot\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)+\left(\nu_{iT}(\widehat{\bm{\theta}}_{iT})-\nu_{iT}(\bar{\bm{\theta}}_{i})\right)\\
&=o_{\mathbb{P}}(1)\cdot\mathcal{O}_{\mathbb{P}}(1)+o_{\mathbb{P}}(1)=o_{\mathbb{P}}(1).\end{aligned}
(30)
We now provide more details on the derivation of the order terms in the last line of (
30
).
For the last summand, we use the stochastic equicontinuity imposed in Assumption
3.3
(iv)
:
For any
η
>
0
\eta>0
and
ε
>
0
\varepsilon>0
, there exists a
δ
>
0
\delta>0
such that
lim
sup
T
→
∞
​
ℙ
​
(
|
ν
i
​
T
​
(
𝜽
^
i
​
T
)
−
ν
i
​
T
​
(
𝜽
¯
i
)
|
>
η
)
\displaystyle\underset{T\to\infty}{\lim\sup}\;\mathbb{P}\left(\big|\nu_{iT}(\widehat{\bm{\theta}}_{iT})-\nu_{iT}(\bar{\bm{\theta}}_{i})\big|>\eta\right)
≤
lim
sup
T
→
∞
​
ℙ
​
(
|
ν
i
​
T
​
(
𝜽
^
i
​
T
)
−
ν
i
​
T
​
(
𝜽
¯
i
)
|
>
η
,
‖
𝜽
^
i
​
T
−
𝜽
¯
i
‖
≤
δ
)
+
lim
sup
T
→
∞
​
ℙ
​
(
‖
𝜽
^
i
​
T
−
𝜽
¯
i
‖
>
δ
)
\displaystyle\qquad\leq\underset{T\to\infty}{\lim\sup}\;\mathbb{P}\left(\big|\nu_{iT}(\widehat{\bm{\theta}}_{iT})-\nu_{iT}(\bar{\bm{\theta}}_{i})\big|>\eta,\;\;\|\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\|\leq\delta\right)+\underset{T\to\infty}{\lim\sup}\;\mathbb{P}\left(\|\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\|>\delta\right)
≤
lim
sup
T
→
∞
ℙ
(
sup
{
𝜽
∈
𝚯
:
‖
𝜽
−
𝜽
¯
i
‖
≤
δ
}
|
ν
i
​
T
(
𝜽
)
−
ν
i
​
T
(
𝜽
¯
i
)
|
>
η
)
+
o
(
1
)
\displaystyle\qquad\leq\underset{T\to\infty}{\lim\sup}\;\mathbb{P}\left(\sup_{\{\bm{\theta}\in\bm{\Theta}:\,\|\bm{\theta}-\bar{\bm{\theta}}_{i}\|\leq\delta\}}\big|\nu_{iT}(\bm{\theta})-\nu_{iT}(\bar{\bm{\theta}}_{i})\big|>\eta\right)+o(1)
<
ε
,
\displaystyle\qquad<\varepsilon,
where we have used that
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
is a consistent estimator for
𝜽
¯
i
\bar{\bm{\theta}}_{i}
.
For the first order term in the last line of (
30
), notice that
𝜽
~
i
​
T
⟶
ℙ
𝜽
¯
i
\widetilde{\bm{\theta}}_{iT}\stackrel{{\scriptstyle\mathbb{P}}}{{\longrightarrow}}\bar{\bm{\theta}}_{i}
as
𝜽
~
i
​
T
\widetilde{\bm{\theta}}_{iT}
is between
𝜽
¯
i
\bar{\bm{\theta}}_{i}
and the consistent estimator
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
.
As by Assumption
3.3
(iii)
, the map
𝜽
↦
g
⁡
(
𝜽
)
=
∇
𝜽
𝔼
​
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\bm{\theta}\mapsto g(\bm{\theta})=\nabla_{\bm{\theta}}\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big]
is continuous.
The Continuous Mapping Theorem hence implies that
∇
𝜽
Q
¯
i
​
T
​
(
𝜽
~
i
​
T
)
=
g
⁡
(
𝜽
~
i
​
T
)
=
∇
𝜽
𝔼
​
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
+
o
ℙ
​
(
1
)
=
o
ℙ
​
(
1
)
,
\displaystyle\nabla_{\bm{\theta}}\overline{Q}_{iT}(\widetilde{\bm{\theta}}_{iT})=g(\widetilde{\bm{\theta}}_{iT})=\nabla_{\bm{\theta}}\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\big]+o_{\mathbb{P}}(1)=o_{\mathbb{P}}(1),
as
∇
𝜽
𝔼
​
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
=
0
\nabla_{\bm{\theta}}\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\big]=0
by (
10
) in Assumption
3.1
.
An equivalent reasoning shows that
T
​
D
T
=
o
ℙ
​
(
1
)
\sqrt{T}D_{T}=o_{\mathbb{P}}(1)
(by simply setting
𝑾
i
​
t
=
1
\bm{W}_{it}=1
in (
29
) and the following.)
Hence, using
T
​
B
i
​
T
=
o
ℙ
​
(
1
)
\sqrt{T}B_{iT}=o_{\mathbb{P}}(1)
and
T
​
D
T
=
o
ℙ
​
(
1
)
\sqrt{T}D_{T}=o_{\mathbb{P}}(1)
, we can write
T
(
𝖬𝖢𝖡
^
1
​
T
−
𝖬𝖢𝖡
¯
1
𝖣𝖲𝖢
^
1
​
T
−
𝖣𝖲𝖢
¯
1
𝖬𝖢𝖡
^
2
​
T
−
𝖬𝖢𝖡
¯
2
𝖣𝖲𝖢
^
2
​
T
−
𝖣𝖲𝖢
¯
2
)
=
(
1
−
1
0
0
0
0
−
1
0
0
1
0
0
1
−
1
0
0
0
0
−
1
1
)
T
−
1
/
2
∑
t
=
1
T
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
+
o
ℙ
(
1
)
,
\displaystyle\sqrt{T}\begin{pmatrix}{\widehat{\mathsf{MCB}}}_{1T}-\overline{\mathsf{MCB}}_{1}\\
{\widehat{\mathsf{DSC}}}_{1T}-\overline{\mathsf{DSC}}_{1}\\
{\widehat{\mathsf{MCB}}}_{2T}-\overline{\mathsf{MCB}}_{2}\\
{\widehat{\mathsf{DSC}}}_{2T}-\overline{\mathsf{DSC}}_{2}\end{pmatrix}=\begin{pmatrix}1&-1&0&0&0\\
0&-1&0&0&1\\
0&0&1&-1&0\\
0&0&0&-1&1\end{pmatrix}T^{-1/2}\sum_{t=1}^{T}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}+o_{\mathbb{P}}(1),
and as
T
−
1
/
2
𝛀
T
−
1
/
2
∑
t
=
1
T
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
⟶
d
𝒩
(
0
,
I
5
)
\displaystyle T^{-1/2}\bm{\Omega}_{T}^{-1/2}\sum_{t=1}^{T}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,I_{5})
satisfies a CLT by assumption, the result of the theorem follows.
∎
Proof of Theorem
3.6
.
We start to show the distribution of
T
​
𝖬𝖢𝖡
^
i
​
T
T\,\widehat{\mathsf{MCB}}_{iT}
under
𝖬𝖢𝖡
¯
i
=
0
\overline{\mathsf{MCB}}_{i}=0
.
For this, we have that
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
,
Y
t
)
]
=
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
∀
t
∈
ℕ
.
\displaystyle\mathbb{E}\big[\mathsf{S}(X_{it},Y_{t})\big]=\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\big]\qquad\forall t\in\mathbb{N}.
(31)
Hence, by the uniqueness in (
10
), this implies that
X
i
​
t
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
X_{it}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
a.s. (e.g., with similar arguments as in the proof of part
(b)
of Theorem
3.2
).
Then, by using the definitions from (
29
) and arguments as in (
30
), we get that
T
⁡
(
𝖬𝖢𝖡
i
^
T
−
𝖬𝖢𝖡
¯
i
)
=
∑
t
=
1
T
(
𝖲
⁡
(
X
i
​
t
,
Y
t
)
−
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
)
=
−
∑
t
=
1
T
(
𝖲
(
𝑾
i
​
t
⊤
𝜽
^
i
​
T
,
Y
t
)
−
𝖲
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
)
=
−
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
(
𝑾
i
​
t
⊤
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
−
1
2
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
(
𝑾
i
​
t
⊤
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
2
−
1
6
∑
t
=
1
T
𝖲
′
′
′
(
𝑾
i
​
t
⊤
𝜽
~
i
​
T
,
Y
t
)
(
𝑾
i
​
t
⊤
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
3
=
:
−
T
​
B
i
​
T
(
1
)
−
T
​
B
i
​
T
(
2
)
−
T
​
B
i
​
T
(
3
)
,
\displaystyle\begin{aligned} T\left(\widehat{\mathsf{MCB}_{i}}_{T}-\overline{\mathsf{MCB}}_{i}\right)&=\sum_{t=1}^{T}\left(\mathsf{S}\big(X_{it},Y_{t}\big)-\mathsf{S}\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t}\big)\right)\\
&=-\sum_{t=1}^{T}\left(\mathsf{S}\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t}\big)-\mathsf{S}\big(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t}\big)\right)\\
&=-\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\big)\\
&\qquad-\frac{1}{2}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\big)^{2}\\
&\qquad-\frac{1}{6}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}}_{iT},Y_{t})\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\big)^{3}\\
&=:-TB_{iT}^{(1)}-TB_{iT}^{(2)}-TB_{iT}^{(3)},\end{aligned}
(32)
for some random variable
𝜽
~
i
​
T
\widetilde{\bm{\theta}}_{iT}
between
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
and
𝜽
¯
i
\bar{\bm{\theta}}_{i}
by a second-order Taylor expansion and a mean-value theorem.
In the following, we show that
T
​
B
i
​
T
(
3
)
=
o
ℙ
​
(
1
)
TB_{iT}^{(3)}=o_{\mathbb{P}}(1)
, whereas
T
​
B
i
​
T
(
1
)
=
𝒪
ℙ
​
(
1
)
TB_{iT}^{(1)}=\mathcal{O}_{\mathbb{P}}(1)
and
T
​
B
i
​
T
(
2
)
=
𝒪
ℙ
​
(
1
)
TB_{iT}^{(2)}=\mathcal{O}_{\mathbb{P}}(1)
contribute to the asymptotic distribution of
T
⁡
(
𝖬𝖢𝖡
^
i
​
T
−
𝖬𝖢𝖡
¯
i
)
T\big(\widehat{\mathsf{MCB}}_{iT}-\overline{\mathsf{MCB}}_{i}\big)
.
By Assumption
3.5
(i)
, equation (
17
), it holds that
T
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
=
−
(
1
T
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
−
1
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
.
\displaystyle\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)=-\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1).
(33)
Hence, for
B
i
​
T
(
1
)
B_{iT}^{(1)}
, by using (
33
), we get that
−
T
​
B
i
​
T
(
1
)
\displaystyle-TB_{iT}^{(1)}
=
−
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
⊤
×
T
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
\displaystyle=-T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}^{\top}\times\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)
=
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
⊤
×
(
1
T
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
−
1
\displaystyle=\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)^{\top}\times\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}
×
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
.
\displaystyle\qquad\times\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1).
Similarly, for
B
i
​
T
(
2
)
B_{iT}^{(2)}
, using (
33
) twice, we get that
−
T
​
B
i
​
T
(
2
)
\displaystyle-TB_{iT}^{(2)}
=
−
1
2
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
(
𝑾
i
​
t
⊤
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
2
\displaystyle=-\frac{1}{2}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\big)^{2}
=
−
1
2
(
T
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
⊤
×
(
1
T
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
×
(
T
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
\displaystyle=-\frac{1}{2}\big(\sqrt{T}(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i})\big)^{\top}\times\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)\times\big(\sqrt{T}(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i})\big)
=
−
1
2
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
⊤
×
(
1
T
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
−
1
\displaystyle=-\frac{1}{2}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)^{\top}\times\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}
×
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
.
\displaystyle\qquad\times\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1).
Finally, for the absolute value of
T
​
B
i
​
T
(
3
)
TB_{iT}^{(3)}
, we get that
|
T
​
B
i
​
T
(
3
)
|
\displaystyle\big|TB_{iT}^{(3)}\big|
=
|
1
6
​
∑
t
=
1
T
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
~
i
​
T
,
Y
t
)
​
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
3
|
\displaystyle=\left|\frac{1}{6}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}}_{iT},Y_{t})\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\big)^{3}\right|
≤
1
6
​
∑
t
=
1
T
|
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
~
i
​
T
,
Y
t
)
|
×
|
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
​
𝜽
¯
i
|
3
\displaystyle\leq\frac{1}{6}\sum_{t=1}^{T}\big|\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}}_{iT},Y_{t})\big|\times\big|\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\big|^{3}
≤
1
6
T
−
1
/
2
1
T
∑
t
=
1
T
|
𝖲
′
′
′
(
𝑾
i
​
t
⊤
𝜽
~
i
​
T
,
Y
t
)
|
∥
𝑾
i
​
t
∥
3
×
∥
T
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
∥
3
\displaystyle\leq\frac{1}{6}T^{-1/2}\frac{1}{T}\sum_{t=1}^{T}\big|\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}}_{iT},Y_{t})\big|\|\bm{W}_{it}\|^{3}\times\|\sqrt{T}(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i})\|^{3}
=
o
ℙ
​
(
1
)
×
𝒪
ℙ
​
(
1
)
=
o
ℙ
​
(
1
)
,
\displaystyle={o}_{\mathbb{P}}(1)\times\mathcal{O}_{\mathbb{P}}(1)={o}_{\mathbb{P}}(1),
where we now provide details for the first
o
ℙ
​
(
1
)
{o}_{\mathbb{P}}(1)
term.
For
h
T
​
(
𝜽
)
:=
1
T
​
∑
t
=
1
T
|
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
​
‖
𝑾
i
​
t
‖
3
h_{T}(\bm{\theta}):=\frac{1}{T}\sum_{t=1}^{T}\big|\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big|\|\bm{W}_{it}\|^{3}
, we have that for any
ε
>
0
\varepsilon>0
small enough
ℙ
(
T
−
1
/
2
h
T
(
𝜽
~
i
​
T
)
>
ε
)
≤
ℙ
(
T
−
1
/
2
|
h
T
(
𝜽
~
i
​
T
)
−
h
T
(
𝜽
¯
i
)
|
>
ε
/
2
)
+
ℙ
(
T
−
1
/
2
h
T
(
𝜽
¯
i
)
>
ε
/
2
)
≤
ℙ
(
T
−
1
/
2
sup
‖
𝜽
−
𝜽
¯
i
‖
≤
δ
|
h
T
(
𝜽
)
−
h
T
(
𝜽
¯
i
)
|
>
ε
/
2
)
+
ℙ
(
T
−
1
/
2
h
T
(
𝜽
¯
i
)
>
ε
/
2
)
+
ℙ
(
∥
𝜽
~
i
​
T
−
𝜽
¯
i
∥
>
δ
)
=
o
⁡
(
1
)
,
\displaystyle\begin{aligned} &\mathbb{P}\left(T^{-1/2}h_{T}(\widetilde{\bm{\theta}}_{iT})>\varepsilon\right)\\
&\qquad\leq\mathbb{P}\left(T^{-1/2}\big|h_{T}(\widetilde{\bm{\theta}}_{iT})-h_{T}(\bar{\bm{\theta}}_{i})\big|>\varepsilon/2\right)+\mathbb{P}\left(T^{-1/2}h_{T}(\bar{\bm{\theta}}_{i})>\varepsilon/2\right)\\
&\qquad\leq\mathbb{P}\left(T^{-1/2}\sup_{\|\bm{\theta}-\bar{\bm{\theta}}_{i}\|\leq\delta}\big|h_{T}(\bm{\theta})-h_{T}(\bar{\bm{\theta}}_{i})\big|>\varepsilon/2\right)+\mathbb{P}\left(T^{-1/2}h_{T}(\bar{\bm{\theta}}_{i})>\varepsilon/2\right)+\mathbb{P}\left(\|\widetilde{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\|>\delta\right)\\
&\qquad=o(1),\end{aligned}
(34)
where the first two terms above are
o
⁡
(
1
)
o(1)
by Assumption
3.5
(ii)
and the third is
o
⁡
(
1
)
o(1)
by the consistency of
𝜽
~
i
​
T
\widetilde{\bm{\theta}}_{iT}
.
Combining the previous three terms, we get that
T
⁡
(
𝖬𝖢𝖡
^
i
​
T
−
𝖬𝖢𝖡
¯
i
)
\displaystyle T\big(\widehat{\mathsf{MCB}}_{iT}-{\overline{\mathsf{MCB}}_{i}}\big)
=
1
2
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
⊤
×
(
1
T
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
−
1
\displaystyle=\frac{1}{2}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)^{\top}\times\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}
×
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
.
\displaystyle\qquad\times\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1).
Then, given a Gaussian random variable
𝑵
i
∼
𝒩
⁡
(
0
,
𝚷
i
)
\bm{N}_{i}\sim\mathcal{N}(0,\bm{\Pi}_{i})
, the quantity of interest
T
⁡
(
𝖬𝖢𝖡
^
i
​
T
−
𝖬𝖢𝖡
¯
i
)
T\big(\widehat{\mathsf{MCB}}_{iT}-{\overline{\mathsf{MCB}}_{i}}\big)
is approximated in distribution by
T
⁡
(
𝖬𝖢𝖡
^
i
​
T
−
𝖬𝖢𝖡
¯
i
)
⟶
d
1
2
​
𝑵
i
⊤
​
𝚼
i
−
1
​
𝑵
i
,
\displaystyle T\left(\widehat{\mathsf{MCB}}_{iT}-\overline{\mathsf{MCB}}_{i}\right)\stackrel{{\scriptstyle d}}{{\longrightarrow}}\frac{1}{2}\bm{N}_{i}^{\top}\bm{\Upsilon}_{i}^{-1}\bm{N}_{i},
which concludes the first part of the proof.
We continue with the second part, the asymptotic distribution of
T
​
𝖣𝖲𝖢
^
i
​
T
T\,\widehat{\mathsf{DSC}}_{iT}
if
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
.
We then have that
𝔼
⁡
[
𝖲
⁡
(
r
¯
,
Y
t
)
]
=
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
∀
t
∈
ℕ
.
\displaystyle\mathbb{E}\big[\mathsf{S}(\bar{r},Y_{t})\big]=\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\big]\qquad\forall t\in\mathbb{N}.
By the uniqueness in (
10
), we obtain
r
¯
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
\bar{r}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
a.s. for all
t
∈
ℕ
t\in\mathbb{N}
, which will be used below.
Hence, we have that
T
⁡
(
𝖣𝖲𝖢
^
i
​
T
−
𝖣𝖲𝖢
¯
i
)
\displaystyle T\big({\widehat{\mathsf{DSC}}}_{iT}-\overline{\mathsf{DSC}}_{i}\big)
=
∑
t
=
1
T
(
𝖲
⁡
(
r
^
T
,
Y
t
)
−
𝖲
⁡
(
r
¯
,
Y
t
)
)
+
∑
t
=
1
T
(
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
−
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
,
Y
t
)
)
\displaystyle=\sum_{t=1}^{T}\big(\mathsf{S}(\widehat{r}_{T},Y_{t})-\mathsf{S}(\bar{r},Y_{t})\big)+\sum_{t=1}^{T}\left(\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})-\mathsf{S}(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t})\right)
=
T
​
D
T
−
T
​
B
i
​
T
.
\displaystyle=TD_{T}-TB_{iT}.
A third order Taylor expansion of
T
​
D
T
TD_{T}
gives that for some
r
~
T
\widetilde{r}_{T}
on the line between
r
^
T
\widehat{r}_{T}
and
r
¯
\bar{r}
,
T
​
D
T
\displaystyle TD_{T}
=
∑
t
=
1
T
𝖲
⁡
(
r
^
T
,
Y
t
)
−
𝖲
⁡
(
r
¯
,
Y
t
)
\displaystyle=\sum_{t=1}^{T}\mathsf{S}(\widehat{r}_{T},Y_{t})-\mathsf{S}(\bar{r},Y_{t})
=
∑
t
=
1
T
𝖲
′
​
(
r
¯
,
Y
t
)
​
(
r
^
T
−
r
¯
)
+
1
2
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
(
r
^
T
−
r
¯
)
2
+
1
6
​
∑
t
=
1
T
𝖲
′′′
​
(
r
~
T
,
Y
t
)
​
(
r
^
T
−
r
¯
)
3
\displaystyle=\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\big(\widehat{r}_{T}-\bar{r}\big)+\frac{1}{2}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\big(\widehat{r}_{T}-\bar{r}\big)^{2}+\frac{1}{6}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime\prime}(\widetilde{r}_{T},Y_{t})\big(\widehat{r}_{T}-\bar{r}\big)^{3}
=
:
T
​
D
T
(
1
)
+
T
​
D
T
(
2
)
+
T
​
D
T
(
3
)
.
\displaystyle=:TD_{T}^{(1)}+TD_{T}^{(2)}+TD_{T}^{(3)}.
Together with the expansion of
B
i
​
T
B_{iT}
in (
32
), this implies
T
⁡
(
𝖣𝖲𝖢
^
i
​
T
−
𝖣𝖲𝖢
¯
i
)
\displaystyle T\big({\widehat{\mathsf{DSC}}}_{iT}-\overline{\mathsf{DSC}}_{i}\big)
=
T
⁡
(
D
T
(
1
)
−
B
i
​
T
(
1
)
)
+
T
⁡
(
D
T
(
2
)
−
B
i
​
T
(
2
)
)
+
T
⁡
(
D
T
(
3
)
−
B
i
​
T
(
3
)
)
.
\displaystyle=T\big(D_{T}^{(1)}-B_{iT}^{(1)}\big)+T\big(D_{T}^{(2)}-B_{iT}^{(2)}\big)+T\big(D_{T}^{(3)}-B_{iT}^{(3)}\big).
(35)
For the vector consisting of the first terms in (
35
), using (
18
) in Assumption
3.5
(i)
, we get
T
⁡
(
D
T
(
1
)
−
B
i
​
T
(
1
)
)
\displaystyle T\big(D_{T}^{(1)}-B_{iT}^{(1)}\big)
=
(
1
−
1
)
×
(
T
​
D
T
(
1
)
T
​
B
i
​
T
(
1
)
)
\displaystyle=\begin{pmatrix}1&-1\end{pmatrix}\times\begin{pmatrix}TD_{T}^{(1)}\\
TB_{iT}^{(1)}\end{pmatrix}
=
(
1
−
1
)
×
∑
t
=
1
T
(
𝖲
′
​
(
r
¯
,
Y
t
)
​
(
r
^
T
−
r
¯
)
𝖲
′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
⊤
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
\displaystyle=\begin{pmatrix}1&-1\end{pmatrix}\times\sum_{t=1}^{T}\begin{pmatrix}\mathsf{S}^{\prime}(\bar{r},Y_{t})(\widehat{r}_{T}-\bar{r})\\
\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i})\\
\end{pmatrix}
=
(
1
−
1
)
×
T
−
1
/
2
∑
t
=
1
T
(
𝖲
′
​
(
r
¯
,
Y
t
)
𝟎
0
𝖲
′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
⊤
)
×
T
(
r
^
T
−
r
¯
𝜽
^
i
​
T
−
𝜽
¯
i
)
\displaystyle=\begin{pmatrix}1&-1\end{pmatrix}\times T^{-1/2}\sum_{t=1}^{T}\begin{pmatrix}\mathsf{S}^{\prime}(\bar{r},Y_{t})&\bm{0}\\
0&\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\end{pmatrix}\times\sqrt{T}\begin{pmatrix}\widehat{r}_{T}-\bar{r}\\
\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\\
\end{pmatrix}
=
−
(
1
−
1
)
×
T
−
1
/
2
∑
t
=
1
T
(
𝖲
′
​
(
r
¯
,
Y
t
)
𝟎
0
𝖲
′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
⊤
)
\displaystyle=-\begin{pmatrix}1&-1\end{pmatrix}\times T^{-1/2}\sum_{t=1}^{T}\begin{pmatrix}\mathsf{S}^{\prime}(\bar{r},Y_{t})&\bm{0}\\
0&\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\end{pmatrix}
×
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
+
o
ℙ
​
(
1
)
𝟎
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
+
o
ℙ
​
(
1
)
)
×
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
\displaystyle\qquad\times\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1}+o_{\mathbb{P}}(1)&\bm{0}\\
\lx@intercol\hfil\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}+o_{\mathbb{P}}(1)\hfil\lx@intercol\end{pmatrix}\times T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}
=
−
T
−
1
/
2
∑
t
=
1
T
(
𝖲
′
​
(
r
¯
,
Y
t
)
,
−
𝖲
′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
⊤
)
\displaystyle=-T^{-1/2}\sum_{t=1}^{T}\begin{pmatrix}\mathsf{S}^{\prime}(\bar{r},Y_{t}),&-\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\end{pmatrix}
×
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
𝟎
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
)
×
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
+
o
ℙ
(
1
)
\displaystyle\qquad\times\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1}&\bm{0}\\
\lx@intercol\hfil\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}\hfil\lx@intercol\end{pmatrix}\times T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}+o_{\mathbb{P}}(1)
=
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
⊤
)
\displaystyle=\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\right)
(36)
×
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
−
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
𝟎
𝟎
𝟎
)
)
\displaystyle\qquad\times\left(\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}-\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1}&\bm{0}\\
\bm{0}&\bm{0}\end{pmatrix}\right)
×
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
.
\displaystyle\qquad\times\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1).
In the last step, we have used the fact that for any (column vector)
𝒂
∈
ℝ
k
\bm{a}\in\mathbb{R}^{k}
and matrix
𝑩
∈
ℝ
k
×
k
\bm{B}\in\mathbb{R}^{k\times k}
with first/upper-left entries
a
1
,
B
11
∈
ℝ
a_{1},B_{11}\in\mathbb{R}
, respectively, it holds that
−
(
a
1
−
𝒂
⊤
)
×
(
B
11
​
0
𝐁
)
×
𝒂
=
𝒂
⊤
×
(
𝐁
−
(
B
11
𝟎
𝟎
𝟎
)
)
×
𝒂
,
\displaystyle-\begin{pmatrix}a_{1}&-\bm{a}^{\top}\end{pmatrix}\times\begin{pmatrix}B_{11}\;\;\bm{0}\\
\mathbf{B}\end{pmatrix}\times\bm{a}=\bm{a}^{\top}\times\left(\mathbf{B}-\begin{pmatrix}B_{11}&\bm{0}\\
\bm{0}&\bm{0}\end{pmatrix}\right)\times\bm{a},
(37)
where the
𝟎
\bm{0}
entries have the appropriate dimensions.
This reformulation allows to express the term above as a quadratic form.
For the second terms in (
35
), similar derivations yield that
T
\displaystyle T
(
D
T
(
2
)
−
B
i
​
T
(
2
)
)
\displaystyle\big(D_{T}^{(2)}-B_{iT}^{(2)}\big)
=
(
1
−
1
)
×
(
T
​
D
T
(
2
)
T
​
B
i
​
T
(
2
)
)
\displaystyle=\begin{pmatrix}1&-1\end{pmatrix}\times\begin{pmatrix}TD_{T}^{(2)}\\
TB_{iT}^{(2)}\end{pmatrix}
=
1
2
​
(
1
−
1
)
×
∑
t
=
1
(
𝖲
′′
​
(
r
¯
,
Y
t
)
​
(
r
^
T
−
r
¯
)
2
𝖲
′′
​
(
r
¯
,
Y
t
)
​
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
2
)
\displaystyle=\frac{1}{2}\begin{pmatrix}1&-1\end{pmatrix}\times\sum_{t=1}\begin{pmatrix}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\big(\widehat{r}_{T}-\bar{r}\big)^{2}\\
\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\big)^{2}\end{pmatrix}
=
1
2
​
(
1
−
1
)
×
(
(
T
​
(
r
^
T
−
r
¯
)
)
×
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
×
(
T
​
(
r
^
T
−
r
¯
)
)
(
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
⊤
×
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
×
(
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
)
\displaystyle=\frac{1}{2}\begin{pmatrix}1&-1\end{pmatrix}\times\begin{pmatrix}\left(\sqrt{T}\left(\widehat{r}_{T}-\bar{r}\right)\right)\times\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)\times\left(\sqrt{T}\left(\widehat{r}_{T}-\bar{r}\right)\right)\\
\left(\sqrt{T}\left(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\right)\right)^{\top}\times\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)\times\left(\sqrt{T}\left(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\right)\right)\end{pmatrix}
=
1
2
​
(
1
−
1
)
×
(
T
​
(
r
^
T
−
r
¯
)
𝟎
0
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
⊤
)
\displaystyle=\frac{1}{2}\begin{pmatrix}1&-1\end{pmatrix}\times\begin{pmatrix}\sqrt{T}\big(\widehat{r}_{T}-\bar{r}\big)&\bm{0}\\
0&\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)^{\top}\end{pmatrix}
×
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
𝟎
𝟎
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
×
(
T
​
(
r
^
T
−
r
¯
)
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
\displaystyle\qquad\times\begin{pmatrix}\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})&\bm{0}\\
\bm{0}&\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\end{pmatrix}\times\begin{pmatrix}\sqrt{T}\big(\widehat{r}_{T}-\bar{r}\big)\\
\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)\end{pmatrix}
=
1
2
×
(
T
​
(
r
^
T
−
r
¯
)
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
⊤
×
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
𝟎
𝟎
−
1
T
∑
t
=
1
T
𝖲
′′
(
r
¯
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
×
(
T
​
(
r
^
T
−
r
¯
)
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
)
\displaystyle=\frac{1}{2}\times\begin{pmatrix}\sqrt{T}\big(\widehat{r}_{T}-\bar{r}\big)\\
\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)\end{pmatrix}^{\top}\times\begin{pmatrix}\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})&\bm{0}\\
\bm{0}&-\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\end{pmatrix}\times\begin{pmatrix}\sqrt{T}\big(\widehat{r}_{T}-\bar{r}\big)\\
\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)\end{pmatrix}
=
1
2
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
⊤
×
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
𝟎
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
)
⊤
\displaystyle=\frac{1}{2}T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\times\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1}&\bm{0}\\
\lx@intercol\hfil\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}\hfil\lx@intercol\end{pmatrix}^{\top}
×
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
𝟎
𝟎
−
1
T
∑
t
=
1
T
𝖲
′′
(
r
¯
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
\displaystyle\qquad\times\begin{pmatrix}\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})&\bm{0}\\
\bm{0}&-\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\end{pmatrix}
×
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
𝟎
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
)
×
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
+
o
ℙ
(
1
)
\displaystyle\qquad\times\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1}&\bm{0}\\
\lx@intercol\hfil\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}\hfil\lx@intercol\end{pmatrix}\times T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}+o_{\mathbb{P}}(1)
=
−
1
2
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
⊤
)
\displaystyle=-\frac{1}{2}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\right)
×
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
−
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
𝟎
𝟎
𝟎
)
)
\displaystyle\qquad\times\left(\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}-\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1}&\bm{0}\\
\bm{0}&\bm{0}\end{pmatrix}\right)
×
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
⊤
)
+
o
ℙ
(
1
)
.
\displaystyle\qquad\times\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\right)+o_{\mathbb{P}}(1).
In the penultimate equality, we have plugged in the (joint) asymptotic expansion of the estimators from (
18
).
In the last equality above, we have used the fact that for a (column) vector
𝒃
=
(
b
1
,
0
)
⊤
∈
ℝ
k
{\bm{b}}=(b_{1},\;\bm{0})^{\top}\in\mathbb{R}^{k}
with first entry
b
1
∈
ℝ
b_{1}\in\mathbb{R}
,
b
1
≠
0
b_{1}\not=0
and an invertible matrix
𝑩
∈
ℝ
k
×
k
\bm{B}\in\mathbb{R}^{k\times k}
, we have that
(
𝒃
𝑩
)
×
(
b
1
−
1
𝟎
𝟎
−
𝑩
−
1
)
×
(
𝒃
⊤
𝑩
)
=
(
b
1
−
1
​
𝒃
−
𝑰
k
)
×
(
𝒃
⊤
𝑩
)
=
b
1
−
1
​
𝒃
​
𝒃
⊤
−
𝑩
=
(
b
1
𝟎
𝟎
𝟎
)
−
𝑩
.
\displaystyle\begin{pmatrix}{\bm{b}}&\bm{B}\end{pmatrix}\times\begin{pmatrix}{b}_{1}^{-1}&\bm{0}\\
\bm{0}&-\bm{B}^{-1}\end{pmatrix}\times\begin{pmatrix}{\bm{b}^{\top}}\\
\bm{B}\end{pmatrix}=\begin{pmatrix}{b}_{1}^{-1}{\bm{b}}&-\bm{I}_{k}\end{pmatrix}\times\begin{pmatrix}{\bm{b}}^{\top}\\
\bm{B}\end{pmatrix}={b}_{1}^{-1}{\bm{b}}{\bm{b}}^{\top}-\bm{B}=\begin{pmatrix}{b}_{1}&\bm{0}\\
\bm{0}&\bm{0}\end{pmatrix}-\bm{B}.
For the third term in (
35
), we get that
|
(
T
​
D
T
(
3
)
T
​
B
i
​
T
(
3
)
)
|
\displaystyle\left|\begin{pmatrix}TD_{T}^{(3)}\\
TB_{iT}^{(3)}\end{pmatrix}\right|
=
1
6
​
(
|
∑
t
=
1
T
𝖲
′′′
​
(
r
~
T
,
Y
t
)
​
(
r
^
T
−
r
¯
)
3
|
|
∑
t
=
1
T
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
~
i
​
T
,
Y
t
)
​
(
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
3
|
)
\displaystyle=\dfrac{1}{6}\begin{pmatrix}\left|\sum_{t=1}^{T}\mathsf{S}^{\prime\prime\prime}(\widetilde{r}_{T},Y_{t})(\widehat{r}_{T}-\bar{r})^{3}\right|\\
\left|\sum_{t=1}^{T}\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}}_{iT},Y_{t})(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})^{3}\right|\end{pmatrix}
≤
1
6
​
(
∑
t
=
1
T
|
𝖲
′′′
​
(
r
~
T
,
Y
t
)
|
⋅
|
r
^
t
−
r
¯
|
3
∑
t
=
1
T
|
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
~
i
​
T
,
Y
t
)
|
⋅
|
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
−
𝑾
i
​
t
⊤
​
𝜽
¯
i
|
3
)
\displaystyle\leq\dfrac{1}{6}\begin{pmatrix}\sum_{t=1}^{T}\left|\mathsf{S}^{\prime\prime\prime}(\widetilde{r}_{T},Y_{t})\right|\cdot\left|\widehat{r}_{t}-\bar{r}\right|^{3}\\
\sum_{t=1}^{T}\left|\mathsf{S}^{\prime\prime\prime}(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}}_{iT},Y_{t})\right|\cdot\left|\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right|^{3}\\
\end{pmatrix}
≤
1
6
T
−
1
/
2
{
1
T
∑
t
=
1
T
(
|
𝖲
′′′
​
(
r
~
T
,
Y
t
)
|
0
0
|
𝖲
′′′
​
(
𝜽
~
i
​
T
,
Y
t
)
|
⋅
‖
𝑾
i
​
t
⊤
‖
3
)
}
(
(
T
​
‖
r
^
t
−
r
¯
‖
)
3
(
T
​
‖
𝜽
^
i
​
T
−
𝜽
¯
i
‖
)
3
)
\displaystyle\leq\dfrac{1}{6}T^{-1/2}\left\{\dfrac{1}{T}\sum_{t=1}^{T}\begin{pmatrix}|\mathsf{S}^{\prime\prime\prime}(\widetilde{r}_{T},Y_{t})|&0\\
0&|\mathsf{S}^{\prime\prime\prime}(\widetilde{\bm{\theta}}_{iT},Y_{t})|\cdot\|\bm{W}_{it}^{\top}\|^{3}\end{pmatrix}\right\}\begin{pmatrix}\big(\sqrt{T}\|\widehat{r}_{t}-\bar{r}\|\big)^{3}\\
\big(\sqrt{T}\big\|\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big\|\big)^{3}\end{pmatrix}
=
o
ℙ
​
(
1
)
×
(
𝒪
ℙ
​
(
1
)
𝒪
ℙ
​
(
1
)
)
\displaystyle=o_{\mathbb{P}}(1)\times\begin{pmatrix}\mathcal{O}_{\mathbb{P}}(1)\\
\mathcal{O}_{\mathbb{P}}(1)\end{pmatrix}
=
o
ℙ
​
(
1
)
,
\displaystyle=o_{\mathbb{P}}(1),
(38)
where the proof of the
o
ℙ
​
(
1
)
o_{\mathbb{P}}(1)
-term follows analogously to (
34
).
Notice for this that as
𝑾
i
​
t
\bm{W}_{it}
contains a constant by assumption, the procedure in (
34
) together with Assumption
3.5
(ii)
also implies that
T
−
1
/
2
1
T
∑
t
=
1
T
|
𝖲
′
′
′
(
r
~
T
,
Y
t
)
|
=
o
ℙ
(
1
)
T^{-1/2}\frac{1}{T}\sum_{t=1}^{T}|\mathsf{S}^{\prime\prime\prime}(\widetilde{r}_{T},Y_{t})|=o_{\mathbb{P}}(1)
.
Hence, from the above three derivations together with (
35
), we obtain
T
⁡
(
𝖣𝖲𝖢
^
i
​
T
−
𝖣𝖲𝖢
¯
i
)
\displaystyle T\left({\widehat{\mathsf{DSC}}}_{iT}-\overline{\mathsf{DSC}}_{i}\right)
=
1
2
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
⊤
)
\displaystyle=\frac{1}{2}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}^{\top}\right)
×
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
−
1
−
(
(
1
T
​
∑
t
=
1
T
𝖲
′′
​
(
r
¯
,
Y
t
)
)
−
1
𝟎
𝟎
𝟎
)
)
\displaystyle\qquad\times\left(\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}-\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bar{r},Y_{t})\right)^{-1}&\bm{0}\\
\bm{0}&\bm{0}\end{pmatrix}\right)
×
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
r
¯
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
,
\displaystyle\qquad\times\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bar{r},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1),
such that the claim of the theorem follows by applying a CLT to the outer terms and a law of large numbers to the inner one.
∎
Proof of Proposition
3.9
.
After laying out some preliminaries, we first show the statement on Assumption
3.3
, followed by the second statement on the verification of Assumption
3.5
.
Notice that
ϕ
⁡
(
Y
t
)
\phi(Y_{t})
and
ϕ
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
\phi(\bm{W}_{it}^{\top}\bm{\theta})
are measurable functions of
α
\alpha
-mixing processes of size
−
s
/
(
s
−
2
)
,
s
>
2
-s/(s-2),s>2
, and thus itself mixing of the same size by
White (2001, Theorem 3.49)
together with Assumption
3.7
(ii)
. Next, consider the objective functions
Q
^
i
​
T
​
(
𝜽
)
\displaystyle\widehat{Q}_{iT}(\bm{\theta})
:
=
1
T
∑
t
=
1
T
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
and
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\qquad\text{ and }\qquad
Q
¯
i
​
T
​
(
𝜽
)
\displaystyle\overline{Q}_{iT}(\bm{\theta})
:
=
𝔼
⁡
[
Q
^
i
​
T
​
(
𝜽
)
]
=
𝔼
⁡
[
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
=
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
.
\displaystyle:=\mathbb{E}\left[\widehat{Q}_{iT}(\bm{\theta})\right]=\mathbb{E}\left[\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right]=\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right].
The first and second derivatives of the objective functions with respect to
𝜽
\bm{\theta}
are
∇
𝜽
Q
^
i
​
T
​
(
𝜽
)
\displaystyle\nabla_{\bm{\theta}}\widehat{Q}_{iT}(\bm{\theta})
:
=
1
T
​
∑
t
=
1
T
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
,
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}),
∇
𝜽
Q
¯
i
​
T
​
(
𝜽
)
\displaystyle\nabla_{\bm{\theta}}\overline{Q}_{iT}(\bm{\theta})
:
=
𝔼
⁡
[
∇
𝜽
Q
^
i
​
T
​
(
𝜽
)
]
=
𝔼
⁡
[
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
]
\displaystyle:=\mathbb{E}\left[\nabla_{\bm{\theta}}\widehat{Q}_{iT}(\bm{\theta})\right]=\mathbb{E}\left[\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})\right]
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
)
\displaystyle\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}(\bm{\theta})
:
=
1
T
​
∑
t
=
1
T
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
+
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
,
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}\bm{W}_{it}^{\top}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})+\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}\bm{W}_{it}^{\top},
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
)
\displaystyle\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bm{\theta})
:
=
𝔼
⁡
[
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
)
]
=
𝔼
⁡
[
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
+
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
]
.
\displaystyle:=\mathbb{E}\left[\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}(\bm{\theta})\right]=\mathbb{E}\left[\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}\bm{W}_{it}^{\top}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})+\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}\bm{W}_{it}^{\top}\right].
Notice, when working with the derivatives of the objective function at the population level, we interchange differentiation and expectation, i.e.,
𝔼
⁡
[
∇
𝜽
Q
^
i
​
T
​
(
𝜽
)
]
=
∇
𝜽
𝔼
​
[
Q
^
i
​
T
​
(
𝜽
)
]
\mathbb{E}\left[\nabla_{\bm{\theta}}\widehat{Q}_{iT}(\bm{\theta})\right]=\nabla_{\bm{\theta}}\mathbb{E}\left[\widehat{Q}_{iT}(\bm{\theta})\right]
, using a measure-theoretic version of the Leibniz rule, which requires the derivative to exist and to be absolutely bounded by an integrable function independent of
𝜽
\bm{\theta}
.
For
∇
𝜽
Q
¯
i
​
T
​
(
𝜽
)
\nabla_{\bm{\theta}}\overline{Q}_{iT}(\bm{\theta})
and
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
)
\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bm{\theta})
, this is ensured by
d
1
​
(
𝑾
i
​
t
,
Y
t
)
\displaystyle d_{1}(\bm{W}_{it},Y_{t})
=
sup
𝜽
∈
𝚯
‖
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
)
𝑾
i
​
t
(
𝑾
i
​
t
⊤
𝜽
−
Y
t
)
‖
and
\displaystyle=\sup_{\bm{\theta}\in\bm{\Theta}}\left\|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})\right\|\quad\text{and}
d
2
​
(
𝑾
i
​
t
,
Y
t
)
\displaystyle d_{2}(\bm{W}_{it},Y_{t})
=
sup
𝜽
∈
𝚯
‖
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
+
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
‖
,
\displaystyle=\sup_{\bm{\theta}\in\bm{\Theta}}\left\|\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}\bm{W}_{it}^{\top}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})+\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}\bm{W}_{it}^{\top}\right\|,
together with the moment conditions in Assumption
3.7
(v)
.
Note, throughout the proof, the
L
s
L_{s}
vector norm is denoted by
∥
⋅
∥
s
\|\cdot\|_{s}
for
s
>
0
s>0
. In particular, for
s
=
2
s=2
, we denote the Euclidean norm by
∥
⋅
∥
:=
∥
⋅
∥
2
\|\cdot\|:=\|\cdot\|_{2}
.
We proceed to verify the high-level assumptions from Section
3.2
, following the order in which they are presented.
Verification of Assumption
3.3
:
For Assumption
3.3
(i)
, we start to show consistency and convergence of the M-estimators using Theorems 2.1 and 3.1 of
Newey and McFadden (1994)
. This directly implies the statement in high level Assumption
3.3
(i)
.
We start by confirming conditions (i)–(iv) of
Newey and McFadden (1994, Theorem 2.1)
for the parameter
𝜽
\bm{\theta}
.
Condition (i) of
Newey and McFadden (1994, Theorem 2.1)
holds as
𝜽
¯
i
\bar{\bm{\theta}}_{i}
is the unique minimizer of
Q
¯
i
​
T
​
(
𝜽
)
\overline{Q}_{iT}(\bm{\theta})
by Assumption
3.1
.
Condition (ii) of
Newey and McFadden (1994, Theorem 2.1)
, i.e., compactness of
𝚯
\bm{\Theta}
, holds by imposing Assumption
3.1
and condition (iii) requires continuity of the objective function
Q
¯
i
​
T
​
(
𝜽
)
\overline{Q}_{iT}(\bm{\theta})
which is fulfilled as per Assumption
3.7
(i)
.
Condition (iv) of
Newey and McFadden (1994, Theorem 2.1)
requires
sup
𝜽
∈
𝚯
|
Q
^
i
​
T
​
(
𝜽
)
−
Q
¯
i
​
T
​
(
𝜽
)
|
=
o
ℙ
​
(
1
)
\sup_{\bm{\theta}\in\bm{\Theta}}\left|\widehat{Q}_{iT}(\bm{\theta})-\overline{Q}_{iT}(\bm{\theta})\right|=o_{\mathbb{P}}(1)
which follows from
Davidson (1994, Theorem 21.9)
given that
(a)
Q
^
i
​
T
​
(
𝜽
)
−
Q
¯
i
​
T
​
(
𝜽
)
=
o
ℙ
​
(
1
)
\widehat{Q}_{iT}(\bm{\theta})-\overline{Q}_{iT}(\bm{\theta})=o_{\mathbb{P}}(1)
for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
, and
(b)
{
Q
^
i
​
T
​
(
⋅
)
−
Q
¯
i
​
T
​
(
⋅
)
}
\big\{\widehat{Q}_{iT}(\cdot)-\overline{Q}_{iT}(\cdot)\big\}
is stochastically equicontinuous.
We first prove the point-wise law of large numbers for the objective function in (a).
From
White (2001, Theorem 3.49)
, it follows that
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})
is stationary and
α
\alpha
-mixing of size
−
s
/
(
s
−
2
)
,
s
>
2
,
-s/(s-2),\;s>2,
by Assumptions
3.1
and
3.7
(ii)
.
Further, as of
White (2001, Proposition 3.44)
,
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})
is ergodic because it is a measurable function of
(
Y
t
,
𝑾
i
​
t
⊤
)
(Y_{t},\bm{W}_{it}^{\top})
.
Since
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
\displaystyle\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right|
=
𝔼
​
|
ϕ
⁡
(
Y
t
)
−
ϕ
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
−
ϕ
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
)
|
\displaystyle=\mathbb{E}\left|\phi(Y_{t})-\phi(\bm{W}_{it}^{\top}\bm{\theta})-\phi^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})(Y_{t}-\bm{W}_{it}^{\top}\bm{\theta})\right|
≤
𝔼
​
|
ϕ
⁡
(
Y
t
)
|
+
𝔼
​
|
ϕ
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
|
+
𝔼
​
|
ϕ
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
)
|
<
∞
,
\displaystyle\leq\mathbb{E}\left|\phi\left(Y_{t}\right)\right|+\mathbb{E}\left|\phi\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\right|+\mathbb{E}\left|\phi^{\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\left(Y_{t}-\bm{W}_{it}^{\top}\bm{\theta}\right)\right|<\infty,
(39)
the ergodicity Theorem 3.34 in
White (2001)
is verified and the pointwise law of large numbers in (a) follows.
Concerning condition (b) of
Davidson (1994, Theorem 21.9)
, we show that
|
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
−
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
~
,
Y
t
)
|
≤
B
T
​
‖
𝜽
−
𝜽
~
‖
for all
​
𝜽
,
𝜽
~
∈
𝚯
,
\left|\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\left(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\right)-\mathsf{S}\left(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}},Y_{t}\right)\right|\leq B_{T}\left\|\bm{\theta}-\widetilde{\bm{\theta}}\right\|\quad\text{for all \penalty\ }\bm{\theta},\widetilde{\bm{\theta}}\in\bm{\Theta},
where
B
T
>
0
B_{T}>0
is a stochastic sequence independent of
𝜽
\bm{\theta}
and
𝜽
~
\widetilde{\bm{\theta}}
, for which we have
B
T
=
𝒪
ℙ
​
(
1
)
B_{T}=\mathcal{O}_{\mathbb{P}}(1)
.
By the mean value theorem, which can be applied due to convexity of
𝚯
\bm{\Theta}
as per Assumption
3.1
, together with triangle inequality, we get for some mean value
𝜽
∗
\bm{\theta}^{*}
on the line joining
𝜽
~
\widetilde{\bm{\theta}}
and
𝜽
\bm{\theta}
, that
|
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
−
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
~
,
Y
t
)
|
=
|
1
T
​
∑
t
=
1
T
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
∗
)
​
𝑾
i
​
t
⊤
​
(
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
∗
)
​
(
𝜽
−
𝜽
~
)
|
≤
1
T
​
∑
t
=
1
T
|
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
∗
)
|
⋅
‖
𝑾
i
​
t
‖
⋅
|
𝑾
i
​
t
⊤
​
𝜽
∗
−
Y
t
|
⋅
‖
𝜽
−
𝜽
~
‖
≤
B
T
​
‖
𝜽
−
𝜽
~
‖
,
\displaystyle\begin{split}&\left|\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\left(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\right)-\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}\left(\bm{W}_{it}^{\top}\widetilde{\bm{\theta}},Y_{t}\right)\right|=\left|\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta}^{*})\bm{W}_{it}^{\top}(Y_{t}-\bm{W}_{it}^{\top}\bm{\theta}^{*})\left(\bm{\theta}-\widetilde{\bm{\theta}}\right)\right|\\
&\leq\frac{1}{T}\sum_{t=1}^{T}\left|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta}^{*})\right|\cdot\left\|\bm{W}_{it}\right\|\cdot\left|\bm{W}^{\top}_{it}\bm{\theta}^{*}-Y_{t}\right|\cdot\left\|\bm{\theta}-\widetilde{\bm{\theta}}\right\|\\
&\leq B_{T}\left\|\bm{\theta}-\widetilde{\bm{\theta}}\right\|,\end{split}
(40)
where
B
T
:=
1
T
​
∑
t
=
1
T
sup
𝜽
∈
𝚯
|
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
​
‖
𝑾
i
​
t
‖
⋅
|
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
|
.
\displaystyle B_{T}:=\frac{1}{T}\sum_{t=1}^{T}\sup_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\right|\left\|\bm{W}_{it}\right\|\cdot\left|\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right|.
(41)
Then,
B
T
=
𝒪
ℙ
​
(
1
)
B_{T}=\mathcal{O}_{\mathbb{P}}(1)
follows from
Davidson (1994, Theorem 12.11)
as
sup
T
∈
ℕ
𝔼
⁡
[
B
T
]
<
∞
\sup_{T\in\mathbb{N}}\mathbb{E}[B_{T}]<\infty
is implied by Assumption
3.7
(v)
.
It follows that
{
Q
^
i
​
T
​
(
⋅
)
−
Q
¯
i
​
T
​
(
⋅
)
}
\big\{\widehat{Q}_{iT}(\cdot)-\overline{Q}_{iT}(\cdot)\big\}
is stochastically equicontinuous.
Hence, we can apply Theorem 2.1 of
Newey and McFadden (1994)
to conclude that the M-estimator is consistent, i.e.
𝜽
^
i
​
T
⟶
ℙ
𝜽
¯
i
\widehat{\bm{\theta}}_{iT}\stackrel{{\scriptstyle\mathbb{P}}}{{\longrightarrow}}\bar{\bm{\theta}}_{i}
.
Secondly, we check conditions (i)–(v) of
Newey and McFadden (1994, Theorem 3.1)
.
Since
𝜽
¯
i
∈
int
⁡
(
𝚯
)
\bar{\bm{\theta}}_{i}\in\operatorname{int}(\bm{\Theta})
by Assumption
3.1
, condition (i) holds.
By Assumption
3.7
(i)
, the objective function
Q
^
i
​
T
​
(
𝜽
)
\widehat{Q}_{iT}(\bm{\theta})
is twice continuously differentiable, ensuring that condition (ii) is fulfilled.
To verify condition (iii), we have to show that a central limit theorem holds for
T
​
∇
𝜽
Q
^
i
​
T
​
(
𝜽
¯
i
)
\sqrt{T}\nabla_{\bm{\theta}}\widehat{Q}_{iT}(\bar{\bm{\theta}}_{i})
.
By the Cramér–Wold device, this reduces to show univariate convergence, i.e.,
T
−
1
/
2
𝝀
⊤
𝐕
T
−
1
/
2
∑
t
=
1
T
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
Y
t
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
⟶
d
𝒩
(
0
,
1
)
,
T
→
∞
,
\displaystyle T^{-1/2}\bm{\lambda}^{\top}\mathbf{V}_{T}^{-1/2}\sum_{t=1}^{T}\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\bm{W}_{it}\left(Y_{t}-\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}\right)\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,1),\qquad T\to\infty,
(42)
for any
𝝀
∈
ℝ
k
\bm{\lambda}\in\mathbb{R}^{k}
satisfying
𝝀
⊤
​
𝝀
=
1
\bm{\lambda}^{\top}\bm{\lambda}=1
.
We show this by verifying the required conditions of the CLT in
White (2001, Theorem 5.20)
.
Note that by
White (2001, Theorem 3.49)
and Assumption
3.7
(ii)
, the sequences
{
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
(
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
}
\left\{\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\bm{W}_{it}\left(Y_{t}-\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}\right)\right\}
and
{
𝝀
⊤
𝐕
T
−
1
/
2
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
Y
t
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
}
\left\{\bm{\lambda}^{\top}\mathbf{V}_{T}^{-1/2}\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\bm{W}_{it}\left(Y_{t}-\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}\right)\right\}
are
α
\alpha
-mixing of size
−
s
/
(
s
−
2
)
-s/(s-2)
,
s
>
2
s>2
.
Since
𝜽
=
𝜽
¯
i
\bm{\theta}=\bar{\bm{\theta}}_{i}
uniquely minimizes the population objective,
𝟎
=
∇
𝜽
Q
¯
i
​
T
​
(
𝜽
¯
i
)
\displaystyle\bm{0}=\nabla_{\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})
=
𝔼
⁡
[
1
T
​
∑
t
=
1
T
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
−
Y
t
)
]
,
\displaystyle=\mathbb{E}\left[\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}-Y_{t})\right],
which further implies that
𝔼
[
𝝀
⊤
𝐕
T
−
1
/
2
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
Y
t
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
]
=
𝟎
\mathbb{E}\left[\bm{\lambda}^{\top}\mathbf{V}_{T}^{-1/2}\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\bm{W}_{it}\left(Y_{t}-\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}\right)\right]=\bm{0}
.
By sub-multiplicativity of norms and Assumption
3.7
(v)
, we get that
𝔼
[
|
𝝀
⊤
𝐕
T
−
1
/
2
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
Y
t
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
|
s
]
\displaystyle\mathbb{E}\left[\left|\bm{\lambda}^{\top}\mathbf{V}_{T}^{-1/2}\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\bm{W}_{it}\left(Y_{t}-\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}\right)\right|^{s}\right]
≤
∥
𝝀
⊤
𝐕
T
−
1
/
2
∥
s
𝔼
[
‖
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
Y
t
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
‖
s
]
\displaystyle\leq\|\bm{\lambda}^{\top}\mathbf{V}_{T}^{-1/2}\|^{s}\mathbb{E}\left[\left\|\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\bm{W}_{it}\left(Y_{t}-\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\right\|^{s}\right]
is finite for
s
>
2
,
∀
t
s>2,\;\forall t
.
Therefore, given Assumption
3.7
(iv)
, the univariate convergence result in (
42
) follows. Further, by the Cramér–Wold device, the conditions of the univariate central limit theorem for mixing series hold for all linear combinations, leading to the desired result
T
−
1
/
2
𝐕
T
−
1
/
2
∑
t
=
1
T
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
Y
t
−
𝑾
i
​
t
⊤
𝜽
¯
i
)
=
−
𝐕
T
−
1
/
2
T
∇
𝜽
Q
^
i
​
T
(
𝜽
¯
i
)
⟶
d
𝒩
(
0
,
I
k
)
.
\displaystyle T^{-1/2}\mathbf{V}_{T}^{-1/2}\sum_{t=1}^{T}\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\right)\bm{W}_{it}\left(Y_{t}-\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}\right)=-\mathbf{V}_{T}^{-1/2}\sqrt{T}\nabla_{\bm{\theta}}\widehat{Q}_{iT}(\bar{\bm{\theta}}_{i})\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,I_{k}).
(43)
For the fourth condition of
Newey and McFadden (1994, Theorem 3.1)
, we use
Newey and McFadden (1994, Lemma 2.4)
to show uniform convergence in probability for the Hessian, i.e.
sup
𝜽
∈
𝚯
‖
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
)
−
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
)
‖
⟶
ℙ
0
.
\displaystyle\sup_{\bm{\theta}\in\bm{\Theta}}\left\|\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}(\bm{\theta})-\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bm{\theta})\right\|\stackrel{{\scriptstyle\mathbb{P}}}{{\longrightarrow}}0.
(44)
Since we consider stationary random variables, a compact
𝚯
\bm{\Theta}
by Assumption
3.1
, and the objective function is continuous for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
by Assumption
3.7
(i)
, we are left to show that there exists a dominating function
d
3
​
(
𝑾
i
​
t
,
Y
t
)
≥
‖
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
)
‖
d_{3}(\bm{W}_{it},Y_{t})\geq\left\|\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}(\bm{\theta})\right\|
for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
, with
𝔼
⁡
[
d
3
​
(
𝑾
i
​
t
,
Y
t
)
]
<
∞
\mathbb{E}\left[d_{3}(\bm{W}_{it},Y_{t})\right]<\infty
, which holds for
d
3
​
(
𝑾
i
​
t
,
Y
t
)
:
=
sup
𝜽
∈
𝚯
(
|
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
⋅
‖
𝑾
i
​
t
‖
2
⋅
|
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
|
)
+
sup
𝜽
∈
𝚯
|
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
⋅
‖
𝑾
i
​
t
‖
2
,
\displaystyle\begin{split}d_{3}(\bm{W}_{it},Y_{t})&:=\sup_{\bm{\theta}\in\bm{\Theta}}\left(\left|\phi^{\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\right|\cdot\left\|\bm{W}_{it}\right\|^{2}\cdot\left|\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right|\right)+\sup_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\right|\cdot\left\|\bm{W}_{it}\right\|^{2},\end{split}
(45)
whose expectation is finite by Assumption
3.7
(v)
.
Hence, the desired convergence result in (
44
) follows.
Moreover, the non-singular expected Hessian,
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
¯
i
)
=
𝔼
⁡
[
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
−
Y
t
)
+
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
]
\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})=\mathbb{E}\left[\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}-Y_{t})+\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}\right]
, required in condition (v) of
Newey and McFadden (1994, Theorem 3.1)
holds by Assumption
3.7
(iv)
.
We conclude the verification of Assumption
3.3
(i)
by noting that the above results generalize to the case where the reference forecast is considered, which corresponds to the setting
𝑾
i
​
t
=
1
\bm{W}_{it}=1
.
We continue to verify the high-level Assumption
3.3
(ii)
, which invokes a CLT for the vector of scores
T
−
1
/
2
∑
t
=
1
T
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
T^{-1/2}\sum_{t=1}^{T}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)
.
For this, we use the Cramér-Wold Device under which the problem reduces to showing that
T
−
1
/
2
𝝀
⊤
𝛀
T
−
1
/
2
∑
t
=
1
T
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
⟶
d
𝒩
(
0
,
1
)
,
\displaystyle T^{-1/2}\bm{\lambda}^{\top}\bm{\Omega}_{T}^{-1/2}\sum_{t=1}^{T}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,1),
(46)
for all
𝝀
∈
ℝ
5
\bm{\lambda}\in\mathbb{R}^{5}
with
𝝀
⊤
​
𝝀
=
1
\bm{\lambda}^{\top}\bm{\lambda}=1
.
Since the scores are measurable functions of the
α
\alpha
-mixing variables by Assumption
3.7
(ii)
, it follows from
White (2001, Theorem 3.49)
that the components of the vector
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)
are also
α
\alpha
-mixing of size
−
s
/
(
s
−
2
)
-s/(s-2)
for
s
>
2
s>2
.
Thus, we can apply the standard central limit theorem for mixing variables in
White (2001, Theorem 5.20)
.
To do so, note that
a
i
​
t
,
c
i
​
t
,
e
t
a_{it},c_{it},e_{t}
,
i
=
1
,
2
i=1,2
, are defined as difference in scores between the sample and population values. Hence these terms are centered around zero by construction and thus
𝔼
⁡
[
𝝀
⊤
​
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
]
=
0
\mathbb{E}\left[\bm{\lambda}^{\top}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right]=0
.
It further holds that
𝔼
|
𝝀
⊤
𝛀
T
−
1
/
2
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
|
s
≤
‖
𝝀
⊤
𝛀
T
−
1
/
2
‖
s
𝔼
‖
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
‖
s
<
∞
,
\displaystyle\mathbb{E}\left|\bm{\lambda}^{\top}\bm{\Omega}_{T}^{-1/2}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right|^{s}\leq\left\|\bm{\lambda}^{\top}\bm{\Omega}_{T}^{-1/2}\right\|^{s}\mathbb{E}\left\|\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)\right\|^{s}<\infty,
(47)
which validates the required moment conditions for
White (2001, Theorem 5.20)
.
Since
‖
𝝀
⊤
𝛀
T
−
1
/
2
‖
s
\left\|\bm{\lambda}^{\top}\bm{\Omega}_{T}^{-1/2}\right\|^{s}
is finite by Assumption
3.8
, we particularly analyze the vector
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
(a_{1t},c_{1t},a_{2t},c_{2t},e_{t})
and note that by linearity of expectations
𝔼
​
‖
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
‖
s
s
=
𝔼
​
|
a
1
​
t
|
s
+
𝔼
​
|
c
1
​
t
|
s
+
𝔼
​
|
a
2
​
t
|
s
+
𝔼
​
|
c
2
​
t
|
s
+
𝔼
​
|
e
t
|
s
<
∞
,
\displaystyle\mathbb{E}\left\|\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right\|_{s}^{s}=\mathbb{E}|a_{1t}|^{s}+\mathbb{E}|c_{1t}|^{s}+\mathbb{E}|a_{2t}|^{s}+\mathbb{E}|c_{2t}|^{s}+\mathbb{E}|e_{t}|^{s}<\infty,
(48)
provided that each
𝔼
​
|
a
i
​
t
|
s
,
𝔼
​
|
c
i
​
t
|
s
,
𝔼
​
|
e
t
|
s
<
∞
\mathbb{E}|a_{it}|^{s},\mathbb{E}|c_{it}|^{s},\mathbb{E}|e_{t}|^{s}<\infty
. To verify this, we detail the bound for
𝔼
​
|
c
i
​
t
|
s
\mathbb{E}|c_{it}|^{s}
and show that it is finite by applying the
c
s
c_{s}
-inequality:
𝔼
​
|
c
i
​
t
|
s
\displaystyle\mathbb{E}|c_{it}|^{s}
=
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
−
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
|
s
\displaystyle=\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})-\mathbb{E}[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})]\right|^{s}
≤
2
s
−
1
​
(
𝔼
⁡
[
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
s
]
+
|
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
|
s
)
<
∞
.
\displaystyle\leq 2^{s-1}\bigg(\mathbb{E}\left[|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})|^{s}\right]+\left|\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right]\right|^{s}\bigg)<\infty.
(49)
Finiteness of the sum in (
49
) follows from the moment conditions in Assumptions
3.7
(v)
by again applying the
c
s
c_{s}
-inequality, i.e.,
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
s
≤
3
2
​
s
−
1
​
(
𝔼
⁡
[
|
ϕ
⁡
(
Y
t
)
|
s
]
+
𝔼
⁡
[
|
ϕ
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
|
s
]
+
𝔼
⁡
[
|
ϕ
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
)
|
s
]
)
<
∞
.
\displaystyle\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right|^{s}\leq 3^{2s-1}\left(\mathbb{E}\left[\left|\phi(Y_{t})\right|^{s}\right]+\mathbb{E}\left[\left|\phi(\bm{W}_{it}^{\top}\bm{\theta})\right|^{s}\right]+\mathbb{E}\left[\left|\phi^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})\left(Y_{t}-\bm{W}_{it}^{\top}\bm{\theta}\right)\right|^{s}\right]\right)<\infty.
The same reasoning applies to
𝔼
​
|
a
i
​
t
|
s
\mathbb{E}|a_{it}|^{s}
and
𝔼
​
|
e
t
|
s
\mathbb{E}|e_{t}|^{s}
. Since all norms on a finite-dimensional space are equivalent, there exists a constant
K
>
0
K>0
such that, for the vector
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
(a_{1t},c_{1t},a_{2t},c_{2t},e_{t})
, the Euclidean norm is at most
K
K
times the
L
s
L_{s}
-norm, i.e., we can write
‖
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
‖
≤
K
​
‖
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
‖
s
\left\|\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right\|\leq K\left\|\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right\|_{s}
.
Raising this expression to the
s
s
-th power, taking expectations, and using (
48
), we get that
𝔼
​
‖
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
‖
s
≤
K
s
​
𝔼
​
‖
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
‖
s
s
≤
K
s
​
[
𝔼
​
|
a
1
​
t
|
s
+
…
+
𝔼
​
|
e
t
|
s
]
<
∞
,
\displaystyle\mathbb{E}\left\|\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right\|^{s}\leq K^{s}\mathbb{E}\left\|\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\right\|_{s}^{s}\leq K^{s}\Big[\mathbb{E}|a_{1t}|^{s}+\ldots+\mathbb{E}|e_{t}|^{s}\Big]<\infty,
because
K
s
K^{s}
is a constant. Hence, the moment condition of
White (2001, Theorem 5.20)
is fulfilled and the univariate convergence result in (
46
) follows, given Assumption
3.8
. Further, by the Cramér–Wold device, the conditions of the univariate central limit theorem for mixing series hold for all linear combinations, leading to the desired result,
T
−
1
/
2
𝛀
T
−
1
/
2
∑
t
=
1
T
(
a
1
​
t
,
c
1
​
t
,
a
2
​
t
,
c
2
​
t
,
e
t
)
⊤
⟶
d
𝒩
(
0
,
I
5
)
.
\displaystyle T^{-1/2}\bm{\Omega}_{T}^{-1/2}\sum_{t=1}^{T}\big(a_{1t},c_{1t},a_{2t},c_{2t},e_{t}\big)^{\top}\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,I_{5}).
(50)
For the verification of the high-level Assumption
3.3
(iii)
, we notice that by Assumption
3.7
(i)
,
ϕ
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
\phi(\bm{W}_{it}^{\top}\bm{\theta})
is continuously differentiable in
𝜽
\bm{\theta}
,
implying that
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})
is also continuously differentiable in
𝜽
\bm{\theta}
with derivative
∇
𝜽
𝖲
​
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
=
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
,
\displaystyle\nabla_{\bm{\theta}}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})=\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}),
which can be bounded by
‖
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
‖
≤
sup
𝜽
∈
𝚯
‖
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
𝑾
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
‖
,
\displaystyle\|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})\|\leq\sup_{\bm{\theta}\in\bm{\Theta}}\|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\bm{W}_{it}(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t})\|,
whose expectation is finite by Assumption
3.7
(v)
.
Hence, differentiability carries over to the expectation by the Leibniz integral rule.
Moreover, under the same assumptions and reasoning, both the first- and second-order derivatives of the expected
score with respect to
𝜽
\bm{\theta}
remain continuously differentiable.
For the verification of high-level Assumption
3.3
(iv)
, and similar to Lemma
A.2
below, we get Lipschitz continuity,
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
−
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝝉
,
Y
t
)
|
≤
b
¯
t
​
‖
𝜽
−
𝝉
‖
\displaystyle\left|\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big)-\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\tau},Y_{t}\big)\right|\leq\bar{b}_{t}\big\|\bm{\theta}-\bm{\tau}\big\|
where
b
¯
t
:=
sup
𝜽
∈
𝚯
|
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
​
‖
𝑾
i
​
t
‖
⋅
|
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
|
.
\displaystyle\bar{b}_{t}:=\sup_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\right|\left\|\bm{W}_{it}\right\|\cdot\left|\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right|.
Hence, we employ
Hansen (1996, Theorem 3)
for mixing arrays, for which we verify his Assumption 4 using the function space
F
:=
{
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
:
𝜽
∈
𝚯
}
F:=\big\{\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}):\;\bm{\theta}\in\bm{\Theta}\big\}
.
First, the mixing condition from Assumption
3.7
implies the first condition of
Hansen (1996, Assumption 4)
.
The second condition of
Hansen (1996, Assumption 4)
holds by stationarity and
lim sup
T
→
∞
{
1
T
​
∑
t
=
1
T
(
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
s
)
2
/
s
}
1
/
2
=
(
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
s
)
1
/
s
<
∞
.
\displaystyle\limsup_{T\to\infty}\left\{\frac{1}{T}\sum_{t=1}^{T}\left(\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right|^{s}\right)^{2/s}\right\}^{1/2}=\left(\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right|^{s}\right)^{1/s}<\infty.
Third, a similar condition holds for the Lipschitz constant
lim sup
T
→
∞
{
1
T
​
∑
t
=
1
T
(
𝔼
​
|
sup
𝜽
∈
𝚯
|
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
​
‖
𝑾
i
​
t
‖
⋅
|
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
|
|
s
)
2
/
s
}
1
/
2
<
∞
,
\displaystyle\limsup_{T\to\infty}\left\{\frac{1}{T}\sum_{t=1}^{T}\left(\mathbb{E}\left|\sup_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\right|\left\|\bm{W}_{it}\right\|\cdot\left|\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right|\right|^{s}\right)^{2/s}\right\}^{1/2}<\infty,
as
𝔼
​
|
sup
𝜽
∈
𝚯
|
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
​
‖
𝑾
i
​
t
‖
⋅
|
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
|
|
s
<
∞
\mathbb{E}\left|\sup_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\right|\left\|\bm{W}_{it}\right\|\cdot\left|\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right|\right|^{s}<\infty
by assumption.
Hence, we can employ
Hansen (1996, Theorem 3)
to conclude that their Condition 1 holds with the
L
q
L_{q}
-norm
ρ
q
(
⋅
)
=
(
𝔼
|
⋅
|
q
)
1
/
q
\rho_{q}(\cdot)=\left(\mathbb{E}\big|\cdot\big|^{q}\right)^{1/q}
(see the proof of Lemma
A.2
for further details).
Thus, we have shown that Assumption
3.3
holds such that Theorem
3.4
applies under the given conditions.
We now continue to verify the high-level conditions in Assumption
3.5
.
Verification of Assumption
3.5
:
For the verification of the high-level Assumption
3.5
(ii)
, recall that
h
T
​
(
𝜽
)
=
1
T
​
∑
t
=
1
T
|
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
​
‖
𝑾
i
​
t
‖
3
=
1
T
​
∑
t
=
1
T
|
2
​
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
+
ϕ
′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
𝑾
i
​
t
​
𝜽
−
Y
t
)
|
⋅
‖
𝑾
i
​
t
‖
3
=
:
1
T
​
∑
t
=
1
T
g
t
​
(
𝜽
)
,
\displaystyle\begin{split}h_{T}(\bm{\theta})&=\frac{1}{T}\sum_{t=1}^{T}\left|\mathsf{S}^{\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\right)\right|\left\|\bm{W}_{it}\right\|^{3}\\
&=\frac{1}{T}\sum_{t=1}^{T}\left|2\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})+\phi^{\prime\prime\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})(\bm{W}_{it}\bm{\theta}-Y_{t})\right|\cdot\left\|\bm{W}_{it}\right\|^{3}\\
&=:\frac{1}{T}\sum_{t=1}^{T}g_{t}(\bm{\theta}),\end{split}
(51)
and note that
h
T
′
​
(
𝜽
)
=
1
T
​
∑
t
=
1
T
sgn
⁡
{
𝖲
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
}
⋅
(
ϕ
′′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
+
3
​
ϕ
′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
)
⋅
𝑾
i
​
t
⋅
‖
𝑾
i
​
t
‖
3
=
:
1
T
​
∑
t
=
1
T
g
t
′
​
(
𝜽
)
.
\displaystyle\begin{split}h_{T}^{\prime}(\bm{\theta})&=\frac{1}{T}\sum_{t=1}^{T}\operatorname{sgn}\left\{\mathsf{S}^{\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\right)\right\}\cdot\left(\phi^{\prime\prime\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\left(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right)+3\phi^{\prime\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\right)\cdot\bm{W}_{it}\cdot\left\|\bm{W}_{it}\right\|^{3}\\
&=:\frac{1}{T}\sum_{t=1}^{T}g^{\prime}_{t}(\bm{\theta}).\end{split}
Concerning the first part of the high level Assumption
3.5
(ii)
, we use that
h
T
​
(
𝜽
)
h_{T}(\bm{\theta})
is Lipschitz-continuous with (random) Lipschitz constant
L
=
sup
𝜽
∈
𝚯
‖
h
T
′
​
(
𝜽
)
‖
L=\sup_{\bm{\theta}\in\bm{\Theta}}\|h_{T}^{\prime}(\bm{\theta})\|
as
ϕ
\phi
is assumed to be five times differentiable with bounded derivatives; see Assumption
3.7
(v)
. Therefore, we get that
T
−
1
/
2
sup
‖
𝜽
−
𝜽
¯
i
‖
≤
δ
|
h
T
(
𝜽
)
−
h
T
(
𝜽
¯
i
)
|
≤
T
−
1
/
2
sup
‖
𝜽
−
𝜽
¯
i
‖
≤
δ
L
∥
𝜽
−
𝜽
¯
i
∥
≤
T
−
1
/
2
L
δ
.
\displaystyle T^{-1/2}\sup_{\|\bm{\theta}-\bar{\bm{\theta}}_{i}\|\leq\delta}\big|h_{T}(\bm{\theta})-h_{T}(\bar{\bm{\theta}}_{i})\big|\;\leq\;T^{-1/2}\sup_{\|\bm{\theta}-\bar{\bm{\theta}}_{i}\|\leq\delta}L\big\|\bm{\theta}-\bar{\bm{\theta}}_{i}\big\|\;\leq\;T^{-1/2}L\delta.
To establish that
T
−
1
/
2
L
δ
=
o
ℙ
(
1
)
T^{-1/2}L\delta=o_{\mathbb{P}}(1)
, it suffices to verify a uniform law of large numbers for
‖
h
T
′
​
(
𝜽
)
‖
\|h_{T}^{\prime}(\bm{\theta})\|
. By taking the supremum of
‖
g
t
′
​
(
𝜽
)
‖
\|g^{\prime}_{t}(\bm{\theta})\|
, we obtain the dominating function
d
4
​
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
:=
sup
𝜽
∈
𝚯
|
ϕ
′′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
⋅
(
𝑾
i
​
t
⊤
​
𝜽
−
Y
t
)
+
3
​
ϕ
′′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
|
⋅
‖
𝑾
i
​
t
‖
4
,
\displaystyle d_{4}\left(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\right):=\sup_{\bm{\theta}\in\bm{\Theta}}\left|\phi^{\prime\prime\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\cdot\left(\bm{W}_{it}^{\top}\bm{\theta}-Y_{t}\right)+3\phi^{\prime\prime\prime\prime}\left(\bm{W}_{it}^{\top}\bm{\theta}\right)\right|\cdot\left\|\bm{W}_{it}\right\|^{4},
which is bounded in expectation, i.e.,
𝔼
⁡
[
d
4
​
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
<
∞
\mathbb{E}\left[d_{4}\left(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\right)\right]<\infty
, given Assumptions
3.7
(v)
.
By Assumption
3.1
the data is stationary and the parameter space
𝚯
\bm{\Theta}
is compact. As the function
‖
g
t
′
​
(
𝜽
)
‖
\|g^{\prime}_{t}(\bm{\theta})\|
is continuous for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
by Assumption
3.7
(i)
, we can apply the uniform law of large numbers in
Newey and McFadden (1994, Lemma 2.4)
to get that
sup
𝜽
∈
𝚯
‖
1
T
​
∑
t
=
1
T
‖
g
t
′
​
(
𝜽
)
‖
−
𝔼
⁡
[
‖
g
t
′
​
(
𝜽
)
‖
]
‖
⟶
ℙ
0
.
\displaystyle\sup_{\bm{\theta}\in\bm{\Theta}}\left\|\frac{1}{T}\sum_{t=1}^{T}\|g^{\prime}_{t}(\bm{\theta})\|-\mathbb{E}\big[\|g^{\prime}_{t}(\bm{\theta})\|\big]\right\|\stackrel{{\scriptstyle\mathbb{P}}}{{\longrightarrow}}0.
(52)
Hence, the desired stochastic Lipschitz bound follows.
Concerning the second part of the high level Assumption
3.5
(ii)
, we show that
T
−
1
/
2
h
T
(
𝜽
¯
i
)
=
o
ℙ
(
1
)
T^{-1/2}h_{T}(\bar{\bm{\theta}}_{i})=o_{\mathbb{P}}(1)
by establishing that
h
T
​
(
𝜽
¯
i
)
h_{T}(\bar{\bm{\theta}}_{i})
satisfies the pointwise law of large numbers.
Under Assumptions
3.1
and
3.7
(v)
,
White (2001, Theorem 3.49)
implies that
g
t
​
(
𝜽
¯
i
)
g_{t}(\bar{\bm{\theta}}_{i})
is stationary and
α
\alpha
-mixing of size
−
s
/
(
s
−
2
)
,
s
>
2
-s/(s-2),s>2
.
Moreover, ergodicity of
g
t
​
(
𝜽
¯
i
)
g_{t}(\bar{\bm{\theta}}_{i})
follows since the function itself is a measurable transformation of
(
𝑾
i
​
t
⊤
,
Y
t
)
\left(\bm{W}_{it}^{\top},Y_{t}\right)
(
White, 2001
, Proposition 3.44)
. We apply the triangle inequality to
|
g
t
​
(
𝜽
¯
i
)
|
\left|g_{t}(\bar{\bm{\theta}}_{i})\right|
which, together with Assumption
3.7
(v)
results in
𝔼
⁡
[
g
t
​
(
𝜽
)
]
≤
𝔼
⁡
[
|
ϕ
′′′
​
(
𝑾
i
​
t
​
𝜽
¯
i
)
|
​
‖
𝑾
i
​
t
‖
3
]
+
𝔼
⁡
[
|
ϕ
′′′′
​
(
𝑾
i
​
t
​
𝜽
¯
i
)
|
⋅
|
𝑾
i
​
t
​
𝜽
¯
i
−
Y
t
|
⋅
‖
𝑾
i
​
t
‖
3
]
<
∞
.
\displaystyle\mathbb{E}\left[g_{t}(\bm{\theta})\right]\leq\mathbb{E}\left[\left|\phi^{\prime\prime\prime}\left(\bm{W}_{it}\bar{\bm{\theta}}_{i}\right)\right|\left\|\bm{W}_{it}\right\|^{3}\right]+\mathbb{E}\left[\left|\phi^{\prime\prime\prime\prime}\left(\bm{W}_{it}\bar{\bm{\theta}}_{i}\right)\right|\cdot\left|\bm{W}_{it}\bar{\bm{\theta}}_{i}-Y_{t}\right|\cdot\left\|\bm{W}_{it}\right\|^{3}\right]<\infty.
(53)
Given (
53
), Theorem 3.34 in
White (2001)
implies the point-wise law of large numbers and we have that
h
T
​
(
𝜽
¯
i
)
=
𝔼
⁡
[
g
t
​
(
𝜽
¯
i
)
]
+
o
ℙ
​
(
1
)
h_{T}(\bar{\bm{\theta}}_{i})=\mathbb{E}\left[g_{t}(\bar{\bm{\theta}}_{i})\right]+o_{\mathbb{P}}(1)
. Hence,
T
−
1
/
2
h
T
(
𝜽
¯
i
)
=
o
ℙ
(
1
)
T^{-1/2}h_{T}(\bar{\bm{\theta}}_{i})=o_{\mathbb{P}}(1)
, as
T
→
∞
T\to\infty
.
For the verification of the high-level Assumption
3.5
(i)
, first note that the true parameter
𝜽
¯
i
\bar{\bm{\theta}}_{i}
lies in
int
⁡
(
𝚯
)
\operatorname{int}(\bm{\Theta})
such that consistency ensures that
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
is in the interior of the parameter space with probability approaching one as
T
→
∞
T\to\infty
and the first-order condition
𝟎
=
∇
𝜽
Q
^
i
​
T
​
(
𝜽
^
i
​
T
)
\bm{0}=\nabla_{\bm{\theta}}\widehat{Q}_{iT}(\widehat{\bm{\theta}}_{iT})
holds with probability approaching one.
6
6
6
For
correctly specified
models, the uniqueness of the minimizer in (
10
) follows naturally. Since the score is strictly consistent for the mean,
Holzmann and Eulert (2014, Theorem 1)
implies that under correct model specification,
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
≤
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\right]\leq\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right]
for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
,
with equality if and only if
𝑾
i
​
t
⊤
​
𝜽
¯
i
​
=
a.s.
​
𝑾
i
​
t
⊤
​
𝜽
\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}\overset{\text{a.s.}}{=}\bm{W}^{\top}_{it}\bm{\theta}
,
which implies
(
𝜽
¯
i
−
𝜽
)
⊤
​
𝔼
​
[
𝑾
i
​
t
​
𝑾
i
​
t
⊤
]
​
(
𝜽
¯
i
−
𝜽
)
=
0
\left(\bar{\bm{\theta}}_{i}-\bm{\theta}\right)^{\top}\mathbb{E}\left[\bm{W}_{it}\bm{W}^{\top}_{it}\right]\left(\bar{\bm{\theta}}_{i}-\bm{\theta}\right)=0
.
As the matrix
𝔼
⁡
[
𝑾
i
​
t
​
𝑾
i
​
t
⊤
]
\mathbb{E}\left[\bm{W}_{it}\bm{W}^{\top}_{it}\right]
is positive definite, this can hold only if
𝜽
¯
i
−
𝜽
=
𝟎
\bar{\bm{\theta}}_{i}-\bm{\theta}=\bm{0}
such that
𝜽
=
𝜽
¯
i
\bm{\theta}=\bar{\bm{\theta}}_{i}
is the
unique
minimizer of
Q
¯
i
​
T
​
(
𝜽
)
\overline{Q}_{iT}(\bm{\theta})
.
We apply the mean-value theorem to get that
𝟎
\displaystyle\bm{0}
=
∇
𝜽
Q
^
i
​
T
​
(
𝜽
^
i
​
T
)
=
∇
𝜽
Q
^
i
​
T
​
(
𝜽
¯
i
)
+
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
~
i
​
T
)
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
,
\displaystyle=\nabla_{\bm{\theta}}\widehat{Q}_{iT}(\widehat{\bm{\theta}}_{iT})=\nabla_{\bm{\theta}}\widehat{Q}_{iT}\left(\bar{\bm{\theta}}_{i}\right)+\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}\left(\widetilde{\bm{\theta}}_{iT}\right)\left(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\right),
(54)
where
𝜽
~
i
​
T
\widetilde{\bm{\theta}}_{iT}
is a (component-wise differing) mean value between
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
and
𝜽
¯
i
\bar{\bm{\theta}}_{i}
, such that
‖
𝜽
~
i
​
T
−
𝜽
¯
i
‖
≤
‖
𝜽
^
i
​
T
−
𝜽
¯
i
‖
\left\|\widetilde{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\right\|\leq\left\|\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\right\|
.
Thus, consistency of
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
and continuous mapping implies
[
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
~
i
​
T
)
]
−
1
=
[
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
¯
i
)
]
−
1
+
o
ℙ
​
(
1
)
\left[\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}\left(\widetilde{\bm{\theta}}_{iT}\right)\right]^{-1}=\left[\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}\left(\bar{\bm{\theta}}_{i}\right)\right]^{-1}+o_{\mathbb{P}}(1)
.
Notice that the empirical Hessian
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
~
i
​
T
)
\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}\left(\widetilde{\bm{\theta}}_{iT}\right)
is invertible for
T
T
large enough as
𝜽
~
i
​
T
⟶
ℙ
𝜽
¯
i
\widetilde{\bm{\theta}}_{iT}\stackrel{{\scriptstyle\mathbb{P}}}{{\longrightarrow}}\bar{\bm{\theta}}_{i}
and the empirical Hessian converges to the expected Hessian
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
¯
i
)
\displaystyle\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})
=
𝔼
⁡
[
ϕ
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
+
ϕ
′′′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
−
Y
t
)
]
\displaystyle=\mathbb{E}\left[\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}+\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}-Y_{t})\right]
at the pseudo-true parameter, which is invertible by Assumption
3.7
(iv)
.
Therefore, rearranging (
54
) gives
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
=
−
(
[
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
¯
i
)
]
−
1
+
o
ℙ
​
(
1
)
)
​
T
​
∇
𝜽
Q
^
i
​
T
​
(
𝜽
¯
i
)
=
−
[
∇
𝜽
​
𝜽
Q
^
i
​
T
​
(
𝜽
¯
i
)
]
−
1
​
T
​
∇
𝜽
Q
^
i
​
T
​
(
𝜽
¯
i
)
+
o
ℙ
​
(
1
)
=
−
(
1
T
∑
t
=
1
T
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
𝑾
i
​
t
⊤
+
ϕ
′
′
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
𝑾
i
​
t
⊤
(
𝑾
i
​
t
⊤
𝜽
¯
i
−
Y
t
)
)
−
1
×
T
−
1
/
2
∑
t
=
1
T
ϕ
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
(
𝑾
i
​
t
⊤
𝜽
¯
i
−
Y
t
)
+
o
ℙ
(
1
)
=
−
(
1
T
∑
t
=
1
T
𝖲
′′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
𝑾
i
​
t
⊤
)
−
1
(
T
−
1
/
2
∑
t
=
1
T
𝖲
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
,
Y
t
)
𝑾
i
​
t
)
+
o
ℙ
(
1
)
.
\displaystyle\begin{split}\sqrt{T}\left(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\right)&=-\left(\left[\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}\left(\bar{\bm{\theta}}_{i}\right)\right]^{-1}+o_{\mathbb{P}}(1)\right)\sqrt{T}\nabla_{\bm{\theta}}\widehat{Q}_{iT}\left(\bar{\bm{\theta}}_{i}\right)\\
&=-\left[\nabla_{\bm{\theta}\bm{\theta}}\widehat{Q}_{iT}\left(\bar{\bm{\theta}}_{i}\right)\right]^{-1}\sqrt{T}\nabla_{\bm{\theta}}\widehat{Q}_{iT}\left(\bar{\bm{\theta}}_{i}\right)+o_{\mathbb{P}}(1)\\
&=-\left(\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}+\phi^{\prime\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\bm{W}_{it}^{\top}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}-Y_{t})\right)^{-1}\times\\
&\qquad\qquad T^{-1/2}\sum_{t=1}^{T}\phi^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}-Y_{t})+o_{\mathbb{P}}(1)\\
&=-\left(\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}^{\prime\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\bm{W}_{it}^{\top}\right)^{-1}\left(T^{-1/2}\sum_{t=1}^{T}\mathsf{S}^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\bm{W}_{it}\right)+o_{\mathbb{P}}(1).\end{split}
(55)
For the case
𝖣𝖲𝖢
¯
i
=
0
\overline{\mathsf{DSC}}_{i}=0
, we first note that
r
¯
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
\bar{r}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
as in the proof of Theorem
3.6
.
The asymptotic behavior of the unconditional expectation
r
¯
\bar{r}
follows as above for
𝑾
i
​
t
=
1
\bm{W}_{it}=1
and by noting that
1
T
​
∑
t
=
1
T
ϕ
′′′
​
(
r
¯
)
​
(
r
¯
−
Y
t
)
⟶
ℙ
0
\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime\prime}(\bar{r})(\bar{r}-Y_{t})\stackrel{{\scriptstyle\mathbb{P}}}{{\longrightarrow}}0
.
Based on this, we stack the estimators emerging from (
55
) to get that
T
​
(
r
^
T
−
r
¯
𝜽
^
i
​
T
−
𝜽
¯
i
)
=
−
(
(
1
T
​
∑
t
=
1
T
ϕ
′′
​
(
r
¯
)
)
−
1
,
0
(
1
T
​
∑
t
=
1
T
ϕ
′′
​
(
r
¯
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
+
ϕ
′′′
​
(
r
¯
)
​
𝑾
i
​
t
​
𝑾
i
​
t
⊤
​
(
r
¯
−
Y
t
)
)
−
1
)
×
T
−
1
/
2
∑
t
=
1
T
ϕ
′′
(
r
¯
)
𝑾
i
​
t
(
r
¯
−
Y
t
)
+
o
ℙ
(
1
)
.
\displaystyle\begin{split}\sqrt{T}\begin{pmatrix}\widehat{r}_{T}-\bar{r}\\
\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\end{pmatrix}&=-\begin{pmatrix}\left(\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime}(\bar{r})\right)^{-1},&0\\
\lx@intercol\hfil\left(\frac{1}{T}\sum_{t=1}^{T}\phi^{\prime\prime}(\bar{r})\bm{W}_{it}\bm{W}_{it}^{\top}+\phi^{\prime\prime\prime}(\bar{r})\bm{W}_{it}\bm{W}_{it}^{\top}(\bar{r}-Y_{t})\right)^{-1}\hfil\lx@intercol\end{pmatrix}\times\\
&\qquad T^{-1/2}\sum_{t=1}^{T}\phi^{\prime\prime}(\bar{r})\bm{W}_{it}(\bar{r}-Y_{t})+o_{\mathbb{P}}(1).\end{split}
(56)
The law of large numbers established in (
44
) ensures convergence of the first terms in (
55
) and (
56
) and invertibility follows from Assumption
3.7
(iii)
for
T
T
large enough.
Asymptotic normality of the second terms in (
55
) and (
56
) follows from the central limit theorem in (
43
).
This verifies Assumption
3.5
(i)
and hence concludes this proof.
∎
Proof of Proposition
3.11
.
We check the conditions of Assumption
3.3
, for which we use
Q
^
i
​
T
​
(
𝜽
)
\displaystyle\widehat{Q}_{iT}(\bm{\theta})
:
=
1
T
∑
t
=
1
T
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
and
\displaystyle:=\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\qquad\text{ and }\qquad
Q
¯
i
​
T
​
(
𝜽
)
\displaystyle\overline{Q}_{iT}(\bm{\theta})
:
=
𝔼
⁡
[
Q
^
i
​
T
​
(
𝜽
)
]
=
𝔼
⁡
[
1
T
​
∑
t
=
1
T
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
=
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
,
\displaystyle:=\mathbb{E}\left[\widehat{Q}_{iT}(\bm{\theta})\right]=\mathbb{E}\left[\frac{1}{T}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right]=\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right],
with
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
=
(
𝟙
{
𝑾
i
​
t
⊤
𝜽
≥
Y
t
}
−
α
)
(
g
(
𝑾
i
​
t
⊤
𝜽
)
−
g
(
Y
t
)
)
.
\displaystyle\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})=\big(\mathds{1}\{\bm{W}_{it}^{\top}\bm{\theta}\geq Y_{t}\}-\alpha\big)\big(g(\bm{W}_{it}^{\top}\bm{\theta})-g(Y_{t})\big).
While the scoring function
𝖲
\mathsf{S}
itself is non-smooth (at
Y
t
=
𝑾
i
​
t
⊤
​
𝜽
Y_{t}=\bm{W}_{it}^{\top}\bm{\theta}
), we show that its expectation is twice (as required below) continuously differentiable everywhere, which implies condition
(iii)
of Assumption
3.3
.
For this, we use the law of iterated expectations and write
Q
¯
i
​
T
​
(
𝜽
)
\displaystyle\overline{Q}_{iT}(\bm{\theta})
=
𝔼
[
𝔼
[
(
𝟙
{
Y
t
≤
𝑾
i
​
t
⊤
𝜽
}
−
α
)
(
g
(
𝑾
i
​
t
⊤
𝜽
)
−
g
(
Y
t
)
)
∣
𝒲
i
​
t
]
]
\displaystyle=\mathbb{E}\Big[\mathbb{E}\big[(\mathds{1}\{Y_{t}\leq\bm{W}_{it}^{\top}\bm{\theta}\}-\alpha)(g(\bm{W}_{it}^{\top}\bm{\theta})-g(Y_{t}))\mid\mathcal{W}_{it}\big]\Big]
=
𝔼
⁡
[
(
F
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
)
−
α
)
​
g
​
(
𝑾
i
​
t
⊤
​
𝜽
)
]
−
𝔼
⁡
[
∫
−
∞
𝑾
i
​
t
⊤
​
𝜽
g
⁡
(
y
)
​
f
i
​
t
​
(
y
)
​
𝑑
y
]
+
α
​
𝔼
​
[
g
⁡
(
Y
t
)
]
.
\displaystyle=\mathbb{E}\Big[\big(F_{it}(\bm{W}_{it}^{\top}\bm{\theta})-\alpha\big)g(\bm{W}_{it}^{\top}\bm{\theta})\Big]-\mathbb{E}\left[\int_{-\infty}^{\bm{W}_{it}^{\top}\bm{\theta}}g(y)f_{it}(y)\mathrm{d}y\right]+\alpha\mathbb{E}[g(Y_{t})].
(57)
We interchange expectation and differentiation by the dominated convergence theorem as there exist functions
G
G
and
G
′
G^{\prime}
such that
‖
𝑾
i
​
t
​
g
​
(
𝑾
i
​
t
⊤
​
𝜽
)
‖
≤
G
⁡
(
𝑾
i
​
t
)
\|\bm{W}_{it}g(\bm{W}_{it}^{\top}\bm{\theta})\|\leq G(\bm{W}_{it})
with
𝔼
​
|
G
⁡
(
𝑾
i
​
t
)
|
<
∞
\mathbb{E}|G(\bm{W}_{it})|<\infty
(as
0
<
f
i
​
t
​
(
⋅
)
≤
K
<
∞
0<f_{it}(\cdot)\leq K<\infty
on its support) and
‖
𝑾
i
​
t
​
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
‖
≤
G
′
​
(
𝑾
i
​
t
)
\|\bm{W}_{it}g^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})\|\leq G^{\prime}(\bm{W}_{it})
with
𝔼
​
|
G
′
​
(
𝑾
i
​
t
)
|
<
∞
\mathbb{E}|G^{\prime}(\bm{W}_{it})|<\infty
.
The first term in (
57
) is continuously differentiable as
F
i
​
t
F_{it}
and
g
g
are continuously differentiable, and has derivative
𝔼
⁡
[
𝑾
i
​
t
​
f
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
g
​
(
𝑾
i
​
t
⊤
​
𝜽
)
+
𝑾
i
​
t
​
(
F
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
)
−
α
)
​
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
]
\mathbb{E}\big[\bm{W}_{it}f_{it}(\bm{W}_{it}^{\top}\bm{\theta})g(\bm{W}_{it}^{\top}\bm{\theta})+\bm{W}_{it}(F_{it}(\bm{W}_{it}^{\top}\bm{\theta})-\alpha)g^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})\big]
,
and the third term does not depend on
𝜽
\bm{\theta}
.
For the middle term, as
g
g
and
f
i
​
t
f_{it}
are continuous, the fundamental theorem of calculus implies
∇
𝜽
𝔼
​
[
∫
−
∞
𝑾
i
​
t
⊤
​
𝜽
g
⁡
(
y
)
​
f
i
​
t
​
(
y
)
​
𝑑
y
]
=
𝔼
⁡
[
𝑾
i
​
t
​
g
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
f
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
)
]
\nabla_{\bm{\theta}}\mathbb{E}\left[\int_{-\infty}^{\bm{W}_{it}^{\top}\bm{\theta}}g(y)f_{it}(y)\mathrm{d}y\right]=\mathbb{E}\left[\bm{W}_{it}g(\bm{W}_{it}^{\top}\bm{\theta})f_{it}(\bm{W}_{it}^{\top}\bm{\theta})\right]
.
Hence, we obtain differentiability such that condition
(iii)
of Assumption
3.3
is satisfied and get that
∇
𝜽
Q
¯
i
​
T
​
(
𝜽
)
=
𝔼
⁡
[
𝑾
i
​
t
​
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
F
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
)
−
α
)
]
.
\displaystyle\nabla_{\bm{\theta}}\overline{Q}_{iT}(\bm{\theta})=\mathbb{E}\left[\bm{W}_{it}g^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})\big(F_{it}(\bm{W}_{it}^{\top}\bm{\theta})-\alpha\big)\right].
(58)
For the second derivative, which will be used below, we similarly get that
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
)
=
𝔼
⁡
[
(
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
​
{
g
′′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
(
F
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
)
−
α
)
+
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
)
​
f
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
)
}
]
,
\displaystyle\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bm{\theta})=\mathbb{E}\Big[(\bm{W}_{it}\bm{W}_{it}^{\top})\left\{g^{\prime\prime}(\bm{W}_{it}^{\top}\bm{\theta})\big(F_{it}(\bm{W}_{it}^{\top}\bm{\theta})-\alpha\big)+g^{\prime}(\bm{W}_{it}^{\top}\bm{\theta})f_{it}(\bm{W}_{it}^{\top}\bm{\theta})\right\}\Big],
(59)
which is positive definite at
𝜽
=
𝜽
¯
i
\bm{\theta}=\bar{\bm{\theta}}_{i}
by assumption.
(Under correct model specification, we have
F
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
=
α
F_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})=\alpha
, and using the tick loss, we have
g
′′
​
(
z
)
=
0
g^{\prime\prime}(z)=0
. In either of these cases, we obtain the simplification
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
¯
i
)
=
𝔼
⁡
[
(
𝑾
i
​
t
​
𝑾
i
​
t
⊤
)
​
g
′
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
​
f
i
​
t
​
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
)
]
\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})=\mathbb{E}\left[(\bm{W}_{it}\bm{W}_{it}^{\top})g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})f_{it}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\right]
.)
We next show condition
(iv)
of Assumption
3.3
, i.e., stochastic equicontinuity of the empirical process
ν
i
​
T
​
(
𝜽
)
\nu_{iT}(\bm{\theta})
from (
15
).
For this, we first show the following lemma:
Lemma A.1
.
Given that the function
g
g
is Lipschitz with constant
L
g
L_{g}
, the GPL loss (
6
) is Lipschitz with constant
L
g
​
max
⁡
(
α
,
1
−
α
)
L_{g}\max(\alpha,1-\alpha)
.
Proof of Lemma
A.1
.
We start to write the function
𝖲
\mathsf{S}
from (
6
) as
𝖲
⁡
(
x
,
y
)
=
ρ
⁡
(
g
⁡
(
x
)
,
g
⁡
(
y
)
)
\mathsf{S}(x,y)=\rho(g(x),g(y))
with
ρ
⁡
(
u
,
v
)
=
{
α
(
v
−
u
)
,
u
≤
v
,
(
1
−
α
)
(
u
−
v
)
,
u
>
v
,
\displaystyle\rho(u,v)=\begin{cases}\alpha(v-u),\quad&u\leq v,\\
(1-\alpha)(u-v),\quad&u>v,\end{cases}
(60)
which is a piecewise linear function with slopes
α
\alpha
and
1
−
α
1-\alpha
, respectively.
Hence, we get that for all
u
1
,
u
2
,
v
∈
ℝ
u_{1},u_{2},v\in\mathbb{R}
that
|
ρ
⁡
(
u
1
,
v
)
−
ρ
⁡
(
u
2
,
v
)
|
≤
max
⁡
(
α
,
1
−
α
)
​
|
u
1
−
u
2
|
\big|\rho(u_{1},v)-\rho(u_{2},v)\big|\leq\max(\alpha,1-\alpha)\big|u_{1}-u_{2}\big|
and as a direct consequence,
|
𝖲
⁡
(
x
1
,
y
)
−
𝖲
⁡
(
x
2
,
y
)
|
\displaystyle\big|\mathsf{S}(x_{1},y)-\mathsf{S}(x_{2},y)\big|
=
|
ρ
⁡
(
g
⁡
(
x
1
)
,
g
⁡
(
y
)
)
−
ρ
⁡
(
g
⁡
(
x
2
)
,
g
⁡
(
y
)
)
|
\displaystyle=\big|\rho(g(x_{1}),g(y))-\rho(g(x_{2}),g(y))\big|
≤
max
⁡
(
α
,
1
−
α
)
​
|
g
⁡
(
x
1
)
−
g
⁡
(
x
2
)
|
\displaystyle\leq\max(\alpha,1-\alpha)\big|g(x_{1})-g(x_{2})\big|
≤
L
g
​
max
⁡
(
α
,
1
−
α
)
​
|
x
1
−
x
2
|
\displaystyle\leq L_{g}\max(\alpha,1-\alpha)\big|x_{1}-x_{2}\big|
holds for all
x
1
,
x
2
,
y
∈
ℝ
x_{1},x_{2},y\in\mathbb{R}
, which concludes the proof of the lemma.
∎
The following lemma shows equicontinuity of
ν
i
​
T
​
(
𝜽
)
\nu_{iT}(\bm{\theta})
from (
15
).
Lemma A.2
.
Assume that the function
g
g
from (
6
) is Lipschitz continuous,
(
Y
t
,
𝐖
i
​
t
⊤
)
(Y_{t},\bm{W}^{\top}_{it})
is
α
\alpha
-mixing of size
−
(
s
−
k
~
)
/
(
k
~
s
)
-(s-\tilde{k})/(\tilde{k}s)
for some
s
>
k
~
>
k
≥
2
s>\tilde{k}>k\geq 2
(where
𝚯
⊆
ℝ
k
\bm{\Theta}\subseteq\mathbb{R}^{k}
), and
𝔼
​
‖
𝐖
i
​
t
‖
s
<
∞
\mathbb{E}\big\|\bm{W}_{it}\big\|^{s}<\infty
,
𝔼
​
|
g
⁡
(
𝐖
i
​
t
⊤
​
𝛉
)
−
g
⁡
(
Y
t
)
|
s
<
∞
\mathbb{E}\big|g(\bm{W}_{it}^{\top}\bm{\theta})-g(Y_{t})\big|^{s}<\infty
.
Then, the empirical process
ν
i
​
T
​
(
𝛉
)
\nu_{iT}(\bm{\theta})
from (
15
) based on the GPL loss
𝖲
\mathsf{S}
from (
6
) is stochastically equicontinuous; see (
16
).
Proof of Lemma
A.2
.
Using Lemma
A.1
, we get for all
𝜽
,
𝝉
∈
𝚯
\bm{\theta},\bm{\tau}\in\bm{\Theta}
that
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
−
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝝉
,
Y
t
)
|
\displaystyle\left|\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}\big)-\mathsf{S}\big(\bm{W}_{it}^{\top}\bm{\tau},Y_{t}\big)\right|
≤
|
𝑾
i
​
t
⊤
​
𝜽
−
𝑾
i
​
t
⊤
​
𝝉
|
​
L
g
​
max
⁡
(
α
,
1
−
α
)
\displaystyle\leq\big|\bm{W}_{it}^{\top}\bm{\theta}-\bm{W}_{it}^{\top}\bm{\tau}\big|L_{g}\max(\alpha,1-\alpha)
≤
L
g
​
max
⁡
(
α
,
1
−
α
)
​
‖
𝑾
i
​
t
‖
​
‖
𝜽
−
𝝉
‖
\displaystyle\leq L_{g}\max(\alpha,1-\alpha)\big\|\bm{W}_{it}\big\|\big\|\bm{\theta}-\bm{\tau}\big\|
is Lipschitz continuous.
Hence, we employ
Hansen (1996, Theorem 3)
for mixing arrays, for which we verify his Assumption 4.
For this, we choose
the function space
F
:=
{
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
:
𝜽
∈
𝚯
}
F:=\big\{\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t}):\;\bm{\theta}\in\bm{\Theta}\big\}
.
First, the mixing condition from Assumption
3.10
implies the first condition of
Hansen (1996, Assumption 4)
.
The second condition of
Hansen (1996, Assumption 4)
holds as we impose stationarity and
𝔼
​
|
g
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
−
g
⁡
(
Y
t
)
|
s
<
∞
\mathbb{E}\big|g(\bm{W}_{it}^{\top}\bm{\theta})-g(Y_{t})\big|^{s}<\infty
such that for any
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
∈
F
\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\in F
,
lim sup
T
→
∞
{
1
T
​
∑
t
=
1
T
(
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
s
)
2
/
s
}
1
/
2
=
(
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
s
)
1
/
s
<
∞
.
\displaystyle\limsup_{T\to\infty}\left\{\frac{1}{T}\sum_{t=1}^{T}\left(\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right|^{s}\right)^{2/s}\right\}^{1/2}=\left(\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right|^{s}\right)^{1/s}<\infty.
Third, a similar condition holds for the Lipschitz constant
lim sup
T
→
∞
{
1
T
​
∑
t
=
1
T
(
𝔼
​
|
L
g
​
max
⁡
(
α
,
1
−
α
)
​
‖
𝑾
i
​
t
‖
|
s
)
2
/
s
}
1
/
2
<
∞
,
\displaystyle\limsup_{T\to\infty}\left\{\frac{1}{T}\sum_{t=1}^{T}\left(\mathbb{E}\left|L_{g}\max(\alpha,1-\alpha)\big\|\bm{W}_{it}\big\|\right|^{s}\right)^{2/s}\right\}^{1/2}<\infty,
as
𝔼
​
‖
𝑾
i
​
t
‖
s
<
∞
\mathbb{E}\big\|\bm{W}_{it}\big\|^{s}<\infty
by assumption.
Hence, we can employ
Hansen (1996, Theorem 3)
to conclude that their Condition 1 holds with the
L
q
L_{q}
-norm
ρ
q
(
⋅
)
=
(
𝔼
|
⋅
|
q
)
1
/
q
\rho_{q}(\cdot)=\left(\mathbb{E}\big|\cdot\big|^{q}\right)^{1/q}
.
To see that the formulation of stochastic equicontinuity in
Hansen (1996, Condition 1)
implies (
16
), notice that
{
f
1
,
f
2
∈
F
:
ρ
q
(
f
1
−
f
2
)
<
δ
}
\displaystyle\Big\{f_{1},f_{2}\in F:\;\rho_{q}(f_{1}-f_{2})<\delta\Big\}
=
{
𝜽
,
𝝉
∈
𝚯
:
ρ
q
(
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
−
𝖲
(
𝑾
i
​
t
⊤
𝝉
,
Y
t
)
)
<
δ
}
\displaystyle=\Big\{\bm{\theta},\bm{\tau}\in\bm{\Theta}:\;\rho_{q}\big(\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})-\mathsf{S}(\bm{W}_{it}^{\top}\bm{\tau},Y_{t})\big)<\delta\Big\}
=
{
𝜽
,
𝝉
∈
𝚯
:
𝔼
|
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
−
𝖲
(
𝑾
i
​
t
⊤
𝝉
,
Y
t
)
|
q
<
δ
q
}
\displaystyle=\Big\{\bm{\theta},\bm{\tau}\in\bm{\Theta}:\;\mathbb{E}\big|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})-\mathsf{S}(\bm{W}_{it}^{\top}\bm{\tau},Y_{t})\big|^{q}<\delta^{q}\Big\}
⊇
{
𝜽
,
𝝉
∈
𝚯
:
∥
𝜽
−
𝝉
∥
q
<
δ
q
L
g
q
​
max
⁡
(
α
,
1
−
α
)
q
​
𝔼
​
‖
𝑾
i
​
t
‖
q
}
,
\displaystyle\supseteq\left\{\bm{\theta},\bm{\tau}\in\bm{\Theta}:\;\big\|\bm{\theta}-\bm{\tau}\big\|^{q}<\frac{\delta^{q}}{L_{g}^{q}\max(\alpha,1-\alpha)^{q}\mathbb{E}\|\bm{W}_{it}\|^{q}}\right\},
such that the supremum over the the left-hand side (in
Hansen (1996)
) is larger or equal than the supremum over the right-hand side (in (
16
)).
Furthermore, Markov’s inequality can be used to transfer the
L
q
L_{q}
-statement in
Hansen (1996)
to the probability statement in (
16
), which concludes this proof.
∎
We continue to show consistency of
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
through
Newey and McFadden (1994, Theorem 2.1)
, which is required for the verification of Assumption
3.3
(i)
.
Notice that
𝚯
\bm{\Theta}
is compact by assumption and that the population objective
Q
¯
i
​
T
​
(
𝜽
)
\overline{Q}_{iT}(\bm{\theta})
is continuous on
𝚯
\bm{\Theta}
as shown above.
The objective function
𝜽
↦
Q
¯
i
​
T
​
(
𝜽
)
=
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\bm{\theta}\mapsto\overline{Q}_{iT}(\bm{\theta})=\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right]
is
uniquely
minimized by
𝜽
¯
i
\bar{\bm{\theta}}_{i}
by Assumption
3.1
.
7
7
7
Under correct specification of the linear quantile regression, the uniqueness follows immediately:
As the GPL scoring function
𝖲
\mathsf{S}
from (
6
) is strictly consistent for the
α
\alpha
-quantile, we employ
Holzmann and Eulert (2014, Theorem 1)
to conclude that
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
¯
i
,
Y
t
)
]
≤
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i},Y_{t})\right]\leq\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right]
,
with equality if and only if
𝑾
i
​
t
⊤
​
𝜽
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
\bm{W}_{it}^{\top}\bm{\theta}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
, which is equivalent to
𝜽
=
𝜽
¯
i
\bm{\theta}=\bar{\bm{\theta}}_{i}
as shown in footnote
6
in the proof of Proposition
3.9
.
Thus, the objective function
𝜽
↦
Q
¯
i
​
T
​
(
𝜽
)
=
𝔼
⁡
[
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
]
\bm{\theta}\mapsto\overline{Q}_{iT}(\bm{\theta})=\mathbb{E}\left[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right]
is
uniquely
minimized by
𝜽
¯
i
\bar{\bm{\theta}}_{i}
.
It remains to show the ULLN,
sup
𝜽
∈
𝚯
|
Q
^
i
​
T
​
(
𝜽
)
−
Q
¯
i
​
T
​
(
𝜽
)
|
=
o
ℙ
​
(
1
)
\sup_{\bm{\theta}\in\bm{\Theta}}\left|\widehat{Q}_{iT}(\bm{\theta})-\overline{Q}_{iT}(\bm{\theta})\right|=o_{\mathbb{P}}(1)
through
Davidson (1994, Theorem 21.9)
.
For this, the pointwise LLN,
Q
^
i
​
T
​
(
𝜽
)
−
Q
¯
i
​
T
​
(
𝜽
)
=
o
ℙ
​
(
1
)
\widehat{Q}_{iT}(\bm{\theta})-\overline{Q}_{iT}(\bm{\theta})=o_{\mathbb{P}}(1)
for all
𝜽
∈
𝚯
\bm{\theta}\in\bm{\Theta}
, follows by
White (2001, Theorem 3.34)
as
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})
is ergodic by
White (2001, Proposition 3.44)
and as
𝔼
​
|
𝖲
⁡
(
𝑾
i
​
t
⊤
​
𝜽
,
Y
t
)
|
≤
𝔼
|
g
⁡
(
𝑾
i
​
t
⊤
​
𝜽
)
​
|
+
𝔼
|
​
g
​
(
Y
t
)
|
<
∞
\mathbb{E}\left|\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\right|\leq\mathbb{E}\big|g(\bm{W}_{it}^{\top}\bm{\theta})\big|+\mathbb{E}\big|g(Y_{t})\big|<\infty
by assumption.
Furthermore, the second condition of
Davidson (1994, Theorem 21.9)
, that
{
Q
^
i
​
T
​
(
𝜽
)
−
Q
¯
i
​
T
​
(
𝜽
)
}
\big\{\widehat{Q}_{iT}(\bm{\theta})-\overline{Q}_{iT}(\bm{\theta})\big\}
is stochastically equicontinuous, follows immediately as
ν
i
​
T
(
𝜽
)
=
T
−
1
/
2
∑
t
=
1
T
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
−
𝔼
[
𝖲
(
𝑾
i
​
t
⊤
𝜽
,
Y
t
)
]
=
T
1
/
2
(
Q
^
i
​
T
(
𝜽
)
−
Q
¯
i
​
T
(
𝜽
)
)
\displaystyle\nu_{iT}(\bm{\theta})=T^{-1/2}\sum_{t=1}^{T}\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})-\mathbb{E}\big[\mathsf{S}(\bm{W}_{it}^{\top}\bm{\theta},Y_{t})\big]=T^{1/2}\left(\widehat{Q}_{iT}(\bm{\theta})-\overline{Q}_{iT}(\bm{\theta})\right)
is shown to be stochastically equicontinuous in Lemma
A.2
above.
Thus, consistency holds and we continue to show asymptotic normality through
Newey and McFadden (1994, Theorem 7.1)
.
The conditions
Q
^
i
​
T
​
(
𝜽
^
i
​
T
)
≤
inf
𝜽
∈
𝚯
Q
^
i
​
T
​
(
𝜽
)
−
o
P
​
(
T
−
1
)
\widehat{Q}_{iT}(\widehat{\bm{\theta}}_{iT})\leq\inf_{\bm{\theta}\in\bm{\Theta}}\widehat{Q}_{iT}(\bm{\theta})-o_{P}(T^{-1})
is satisfied as
𝜽
^
i
​
T
\widehat{\bm{\theta}}_{iT}
is defined as the minimizer of
Q
^
i
​
T
​
(
𝜽
)
\widehat{Q}_{iT}(\bm{\theta})
over
𝚯
\bm{\Theta}
.
Item (i) of
Newey and McFadden (1994, Theorem 7.1)
holds as
Q
¯
i
​
T
​
(
𝜽
)
\overline{Q}_{iT}(\bm{\theta})
is minimized on
𝚯
\bm{\Theta}
at
𝜽
¯
i
\bar{\bm{\theta}}_{i}
.
Item (ii) of
Newey and McFadden (1994, Theorem 7.1)
,
𝜽
¯
i
∈
int
⁡
(
𝚯
)
\bar{\bm{\theta}}_{i}\in\operatorname{int}(\bm{\Theta})
holds by assumption, and item (iii),
twice continuous differentiability of
Q
¯
i
​
T
​
(
𝜽
)
\overline{Q}_{iT}(\bm{\theta})
with second derivative
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
¯
i
)
\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})
(at
𝜽
¯
i
\bar{\bm{\theta}}_{i}
), is shown above around (
59
) and the matrix
∇
𝜽
​
𝜽
Q
¯
i
​
T
​
(
𝜽
¯
i
)
\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})
is non-singular by assumption.
We continue to show item (iv), i.e., that a multivariate CLT holds for
T
D
^
i
​
T
(
𝜽
¯
i
)
=
T
−
1
/
2
∑
t
=
1
T
𝑾
i
​
t
g
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
(
𝟙
{
Y
t
≤
𝑾
i
​
t
⊤
𝜽
¯
i
}
−
α
)
,
\displaystyle\sqrt{T}\widehat{D}_{iT}(\bar{\bm{\theta}}_{i})=T^{-1/2}\sum_{t=1}^{T}\bm{W}_{it}g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\big(\mathds{1}\{Y_{t}\leq\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\}-\alpha\big),
(61)
which is the derivative of
Q
^
i
​
T
​
(
𝜽
¯
i
)
\widehat{Q}_{iT}(\bar{\bm{\theta}}_{i})
almost surely (except when
Y
t
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
Y_{t}=\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}
).
We use the time-series CLT in
White (2001, Theorem 5.20)
and note that
∇
𝜽
Q
¯
i
​
T
​
(
𝜽
¯
i
)
=
𝔼
⁡
[
D
^
i
​
T
​
(
𝜽
¯
i
)
]
=
0
\nabla_{\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})=\mathbb{E}[\widehat{D}_{iT}(\bar{\bm{\theta}}_{i})]=0
; see (
58
).
For this, let
𝝀
∈
ℝ
k
\bm{\lambda}\in\mathbb{R}^{k}
with
𝝀
⊤
​
𝝀
=
1
\bm{\lambda}^{\top}\bm{\lambda}=1
and consider
𝝀
⊤
​
T
​
D
^
i
​
T
​
(
𝜽
¯
i
)
\bm{\lambda}^{\top}\sqrt{T}\widehat{D}_{iT}(\bar{\bm{\theta}}_{i})
through the Cramér-Wold device.
First, by the mixing condition from Assumption
3.10
with mixing coefficients
α
m
\alpha_{m}
, we have that
∑
m
=
1
∞
α
m
(
s
−
k
~
)
/
(
k
~
​
s
)
<
∞
\sum_{m=1}^{\infty}\alpha_{m}^{(s-\tilde{k})/(\tilde{k}s)}<\infty
for
s
>
k
~
>
k
≥
2
s>\tilde{k}>k\geq 2
.
As
s
−
k
~
k
~
​
s
<
s
−
2
s
\frac{s-\tilde{k}}{\tilde{k}s}<\frac{s-2}{s}
for any
s
>
2
s>2
and
k
~
>
2
\tilde{k}>2
, and
α
m
<
1
\alpha_{m}<1
, we also have that
∑
m
=
1
∞
α
m
(
s
−
2
)
/
s
<
∞
\sum_{m=1}^{\infty}\alpha_{m}^{(s-2)/{s}}<\infty
, such that the sequence
(
Y
t
,
𝑾
i
​
t
⊤
)
t
∈
ℕ
(Y_{t},\bm{W}^{\top}_{it})_{t\in\mathbb{N}}
is also strong mixing of size
−
s
/
(
s
−
2
)
-s/(s-2)
.
White (2001, Theorem 3.49)
further implies that the sequences
𝝀
⊤
𝑾
i
​
t
g
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
(
𝟙
{
Y
t
≤
𝑾
i
​
t
⊤
𝜽
¯
i
}
−
α
)
\bm{\lambda}^{\top}\bm{W}_{it}g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\big(\mathds{1}\{Y_{t}\leq\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\}-\alpha\big)
are mixing of the same size as the underlying random variables.
Furthermore, for
s
>
2
s>2
, we have
𝔼
[
|
g
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝝀
⊤
𝑾
i
​
t
(
𝟙
{
Y
t
≤
𝑾
i
​
t
⊤
𝜽
¯
i
}
−
α
)
|
s
]
≤
𝔼
[
|
g
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝝀
⊤
𝑾
i
​
t
|
s
]
≤
𝔼
[
∥
g
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
𝑾
i
​
t
∥
s
]
,
\displaystyle\mathbb{E}\left[\left|g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{\lambda}^{\top}\bm{W}_{it}\big(\mathds{1}\{Y_{t}\leq\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\}-\alpha\big)\right|^{s}\right]\leq\mathbb{E}\left[\left|g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{\lambda}^{\top}\bm{W}_{it}\right|^{s}\right]\leq\mathbb{E}\left[\|g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\bm{W}_{it}\|^{s}\right],
which is finite by assumption, as
g
′
g^{\prime}
is bounded from above.
Using that
𝝀
⊤
𝐕
T
𝝀
=
Var
(
T
−
1
/
2
∑
t
=
1
T
g
′
(
𝑾
i
​
t
⊤
𝜽
¯
i
)
(
𝟙
{
Y
t
≤
𝑾
i
​
t
⊤
𝜽
¯
i
}
−
α
)
𝝀
⊤
𝑾
i
​
t
)
\displaystyle\bm{\lambda}^{\top}\mathbf{V}_{T}\bm{\lambda}=\operatorname{Var}\left(T^{-1/2}\sum_{t=1}^{T}g^{\prime}(\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i})\big(\mathds{1}\{Y_{t}\leq\bm{W}_{it}^{\top}\bar{\bm{\theta}}_{i}\}-\alpha\big)\bm{\lambda}^{\top}\bm{W}_{it}\right)
is uniformly bounded away from zero by assumption,
White (2001, Theorem 5.20)
together with the Cramér-Wold device yields that
T
𝐕
i
​
T
−
1
/
2
D
^
i
​
T
(
𝜽
¯
i
)
⟶
d
𝒩
(
0
,
I
k
)
.
\displaystyle\sqrt{T}\,\mathbf{V}_{iT}^{-1/2}\widehat{D}_{iT}(\bar{\bm{\theta}}_{i})\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,I_{k}).
(62)
Finally, item (v) of
Newey and McFadden (1994, Theorem 7.1)
is implied by stochastic equicontinuity of the process
ν
i
​
T
\nu_{iT}
shown in Lemma
A.2
; see the discussion on page 2187 of
Newey and McFadden (1994)
.
Hence, we can conclude that
T
(
(
∇
𝜽
​
𝜽
Q
¯
i
​
T
(
𝜽
¯
i
)
)
−
1
𝐕
i
​
T
(
∇
𝜽
​
𝜽
Q
¯
i
​
T
(
𝜽
¯
i
)
)
−
1
)
−
1
/
2
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
⟶
d
𝒩
(
0
,
I
k
)
,
\displaystyle\sqrt{T}\Big(\big(\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})\big)^{-1}\mathbf{V}_{iT}\big(\nabla_{\bm{\theta}\bm{\theta}}\overline{Q}_{iT}(\bar{\bm{\theta}}_{i})\big)^{-1}\Big)^{-1/2}\left(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\right)\stackrel{{\scriptstyle d}}{{\longrightarrow}}\mathcal{N}(0,I_{k}),
which particularly implies
T
​
(
𝜽
^
i
​
T
−
𝜽
¯
i
)
=
𝒪
ℙ
​
(
1
)
\sqrt{T}\big(\widehat{\bm{\theta}}_{iT}-\bar{\bm{\theta}}_{i}\big)=\mathcal{O}_{\mathbb{P}}(1)
.
Invoking
𝑾
i
​
t
=
1
\bm{W}_{it}=1
, this also implies
T
​
(
r
^
T
−
r
¯
)
=
𝒪
ℙ
​
(
1
)
\sqrt{T}\big(\widehat{r}_{T}-\bar{r}\big)=\mathcal{O}_{\mathbb{P}}(1)
such that condition (i) of Assumption
3.3
holds.
The high-level Assumption
3.3
(ii)
holds by the same arguments following (
46
), applied to the GPL loss function and using the respective moment conditions from Assumption
3.10
.
∎
Proof of Proposition
4.1
.
Consider the squared error scoring function and notice that
𝖬𝖢𝖡
¯
i
=
𝔼
[
𝖲
(
X
i
​
t
,
Y
t
)
−
𝖲
(
𝔼
[
Y
t
∣
𝑾
i
​
t
]
,
Y
t
)
]
=
𝔼
[
(
X
i
​
t
−
Y
t
)
2
−
(
𝔼
[
Y
t
∣
𝑾
i
​
t
]
−
Y
t
)
2
]
=
𝔼
⁡
[
X
i
​
t
2
]
−
𝔼
⁡
[
𝔼
​
[
Y
t
∣
𝑾
i
​
t
]
2
]
−
2
​
𝔼
​
[
X
i
​
t
​
Y
t
]
+
2
​
𝔼
​
[
Y
t
​
𝔼
​
[
Y
t
∣
𝑾
i
​
t
]
]
=
𝔼
⁡
[
X
i
​
t
2
]
+
𝔼
⁡
[
𝔼
​
[
Y
t
∣
𝑾
i
​
t
]
2
]
−
2
​
𝔼
​
[
X
i
​
t
​
Y
t
]
,
\displaystyle\begin{split}\overline{\mathsf{MCB}}_{i}&=\mathbb{E}\Bigr[\mathsf{S}(X_{it},Y_{t})-\mathsf{S}(\mathbb{E}[Y_{t}\mid\bm{W}_{it}],Y_{t})\Bigr]\\
&=\mathbb{E}\Bigr[(X_{it}-Y_{t})^{2}-(\mathbb{E}[Y_{t}\mid\bm{W}_{it}]-Y_{t})^{2}\Bigr]\\
&=\mathbb{E}[X_{it}^{2}]-\mathbb{E}[\mathbb{E}[Y_{t}\mid\bm{W}_{it}]^{2}]-2\mathbb{E}[X_{it}Y_{t}]+2\mathbb{E}[Y_{t}\mathbb{E}[Y_{t}\mid\bm{W}_{it}]]\\
&=\mathbb{E}[X_{it}^{2}]+\mathbb{E}[\mathbb{E}[Y_{t}\mid\bm{W}_{it}]^{2}]-2\mathbb{E}[X_{it}Y_{t}],\end{split}
(63)
and
𝖣𝖲𝖢
¯
i
=
𝔼
[
𝖲
(
𝔼
[
Y
t
]
,
Y
t
)
]
−
𝔼
[
𝖲
(
𝔼
[
Y
t
∣
𝑾
i
​
t
]
,
Y
t
)
]
=
𝔼
[
(
𝔼
[
Y
t
]
−
Y
t
)
2
−
(
𝔼
[
Y
t
∣
𝑾
i
​
t
]
−
Y
t
)
2
]
=
−
𝔼
[
𝔼
[
Y
t
∣
𝑾
i
​
t
]
2
]
+
2
𝔼
[
Y
t
𝔼
[
Y
t
∣
𝑾
i
​
t
]
]
=
𝔼
[
𝔼
[
Y
t
∣
𝑾
i
​
t
]
2
]
,
\displaystyle\begin{split}\overline{\mathsf{DSC}}_{i}&=\mathbb{E}\Bigr[\mathsf{S}(\mathbb{E}[Y_{t}],Y_{t})\Bigr]-\mathbb{E}\Bigr[\mathsf{S}(\mathbb{E}[Y_{t}\mid\bm{W}_{it}],Y_{t})\Bigr]\\
&=\mathbb{E}\Bigr[(\mathbb{E}[Y_{t}]-Y_{t})^{2}-(\mathbb{E}[Y_{t}\mid\bm{W}_{it}]-Y_{t})^{2}\Bigr]\\
&=-\mathbb{E}\Bigr[\mathbb{E}[Y_{t}\mid\bm{W}_{it}]^{2}\Bigr]+2\mathbb{E}\Bigr[Y_{t}\mathbb{E}[Y_{t}\mid\bm{W}_{it}]\Bigr]\\
&=\mathbb{E}\Bigr[\mathbb{E}[Y_{t}\mid\bm{W}_{it}]^{2}\Bigr],\end{split}
(64)
where the final equality follows from the law of iterated expectations.
Recall that
ς
=
Var
⁡
(
M
t
)
=
Var
⁡
(
K
t
)
=
Var
⁡
(
L
t
)
=
Var
⁡
(
N
t
)
=
1
1
−
β
2
\varsigma=\operatorname{Var}(M_{t})=\operatorname{Var}(K_{t})=\operatorname{Var}(L_{t})=\operatorname{Var}(N_{t})=\dfrac{1}{1-\beta^{2}}
.
As the processes
M
t
,
K
t
,
L
t
,
N
t
M_{t},K_{t},L_{t},N_{t}
are independent, it also follows that
𝔼
⁡
[
M
t
​
K
t
]
=
𝔼
⁡
[
M
t
​
L
t
]
=
𝔼
⁡
[
M
t
​
N
t
]
=
𝔼
⁡
[
K
t
​
L
t
]
=
𝔼
⁡
[
K
t
​
N
t
]
=
𝔼
⁡
[
L
t
​
N
t
]
=
0
\mathbb{E}[M_{t}K_{t}]=\mathbb{E}[M_{t}L_{t}]=\mathbb{E}[M_{t}N_{t}]=\mathbb{E}[K_{t}L_{t}]=\mathbb{E}[K_{t}N_{t}]=\mathbb{E}[L_{t}N_{t}]=0
.
Hence, for forecaster
i
=
1
i=1
, we have
𝔼
⁡
[
X
1
​
t
]
=
δ
0
\mathbb{E}[X_{1t}]=\delta_{0}
and
𝔼
⁡
[
X
1
​
t
2
]
\displaystyle\mathbb{E}[X_{1t}^{2}]
=
δ
0
2
+
(
δ
M
2
+
δ
K
2
+
δ
N
2
)
​
ς
=
δ
0
2
+
ς
⋅
𝜹
⊤
​
𝜹
,
and
\displaystyle=\delta_{0}^{2}+(\delta_{M}^{2}+\delta_{K}^{2}+\delta_{N}^{2})\varsigma=\delta_{0}^{2}+\varsigma\cdot\bm{\delta}^{\top}\bm{\delta},\qquad\text{and}
(65)
𝔼
⁡
[
X
1
​
t
​
Y
t
]
\displaystyle\mathbb{E}[X_{1t}Y_{t}]
=
(
δ
K
​
γ
K
+
γ
M
​
δ
M
+
γ
N
​
δ
N
)
​
ς
=
ς
⋅
𝜹
⊤
​
𝜸
.
\displaystyle=(\delta_{K}\gamma_{K}+\gamma_{M}\delta_{M}+\gamma_{N}\delta_{N})\varsigma=\varsigma\cdot\bm{\delta}^{\top}\bm{\gamma}.
(66)
For forecaster
i
=
2
i=2
, we accordingly have
𝔼
⁡
[
X
2
​
t
]
=
ξ
0
\mathbb{E}[X_{2t}]=\xi_{0}
and
𝔼
⁡
[
X
2
​
t
2
]
\displaystyle\mathbb{E}[X_{2t}^{2}]
=
ξ
0
2
+
(
ξ
M
2
+
ξ
L
2
+
ξ
N
2
)
​
ς
=
ξ
0
2
+
ς
⋅
𝝃
⊤
​
𝝃
,
and
\displaystyle=\xi_{0}^{2}+(\xi_{M}^{2}+\xi_{L}^{2}+\xi_{N}^{2})\varsigma=\xi_{0}^{2}+\varsigma\cdot\bm{\xi}^{\top}\bm{\xi},\qquad\text{and}
(67)
𝔼
⁡
[
X
2
​
t
​
Y
t
]
\displaystyle\mathbb{E}[X_{2t}Y_{t}]
=
(
ξ
M
​
γ
M
+
γ
L
​
ξ
L
+
ξ
N
​
γ
N
)
​
ς
=
ς
⋅
𝝃
⊤
​
𝜸
.
\displaystyle=(\xi_{M}\gamma_{M}+\gamma_{L}\xi_{L}+\xi_{N}\gamma_{N})\varsigma=\varsigma\cdot\bm{\xi}^{\top}\bm{\gamma}.
(68)
For the term
𝔼
[
𝔼
[
Y
t
∣
𝑾
i
​
t
]
2
]
\mathbb{E}\bigr[\mathbb{E}[Y_{t}\mid\bm{W}_{it}]^{2}\bigr]
, with
𝑾
i
​
t
=
(
1
,
X
i
​
t
)
⊤
\bm{W}_{it}=(1,X_{it})^{\top}
, we use
𝔼
⁡
[
Y
t
∣
𝑾
i
​
t
]
=
𝔼
⁡
[
Y
t
∣
X
i
​
t
]
\mathbb{E}[Y_{t}\mid\bm{W}_{it}]=\mathbb{E}[Y_{t}\mid X_{it}]
.
Given the linearity of our DGP in (
23
) and as
𝔼
⁡
[
Y
t
]
=
0
\mathbb{E}[Y_{t}]=0
, we get that
𝔼
⁡
[
Y
t
∣
𝑾
i
​
t
]
=
𝑾
i
​
t
⊤
​
𝜽
¯
i
=
k
¯
i
+
ϑ
¯
i
​
X
i
​
t
,
\displaystyle\mathbb{E}[Y_{t}\mid\bm{W}_{it}]=\bm{W}^{\top}_{it}\bar{\bm{\theta}}_{i}=\bar{k}_{i}+\bar{\vartheta}_{i}X_{it},
with
ϑ
¯
i
=
Cov
(
X
i
​
t
,
Y
t
)
/
Var
(
X
i
​
t
)
and
k
¯
i
=
−
ϑ
¯
i
⋅
𝔼
[
X
i
​
t
]
.
\displaystyle\bar{\vartheta}_{i}=\operatorname{Cov}(X_{it},Y_{t})/\operatorname{Var}(X_{it})\quad\text{and}\quad\bar{k}_{i}=-\bar{\vartheta}_{i}\cdot\mathbb{E}[X_{it}].
Using the expressions (
65
)–(
68
), we get
𝔼
⁡
[
𝔼
​
[
Y
t
∣
𝑾
1
​
t
]
2
]
\displaystyle\mathbb{E}\big[\mathbb{E}[Y_{t}\mid\bm{W}_{1t}]^{2}\big]
=
𝔼
⁡
[
(
𝜹
⊤
​
𝜸
𝜹
⊤
​
𝜹
)
2
​
(
X
1
​
t
−
δ
0
)
2
]
=
ς
⋅
(
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
,
\displaystyle=\mathbb{E}\left[\left(\frac{\bm{\delta}^{\top}\bm{\gamma}}{\bm{\delta}^{\top}\bm{\delta}}\right)^{2}(X_{1t}-\delta_{0})^{2}\right]=\varsigma\cdot\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}},
(69)
𝔼
⁡
[
𝔼
​
[
Y
t
∣
𝑾
2
​
t
]
2
]
\displaystyle\mathbb{E}\big[\mathbb{E}[Y_{t}\mid\bm{W}_{2t}]^{2}\big]
=
𝔼
⁡
[
(
𝝃
⊤
​
𝜸
𝝃
⊤
​
𝝃
)
2
​
(
X
2
​
t
−
ξ
0
)
2
]
=
ς
⋅
(
𝝃
⊤
​
𝜸
)
2
𝝃
⊤
​
𝝃
.
\displaystyle=\mathbb{E}\left[\left(\frac{\bm{\xi}^{\top}\bm{\gamma}}{\bm{\xi}^{\top}\bm{\xi}}\right)^{2}(X_{2t}-\xi_{0})^{2}\right]=\varsigma\cdot\frac{(\bm{\xi}^{\top}\bm{\gamma})^{2}}{\bm{\xi}^{\top}\bm{\xi}}.
(70)
Hence, the expression for
𝖬𝖢𝖡
¯
1
\overline{\mathsf{MCB}}_{1}
from (
26
) follows by substituting (
65
), (
66
) and (
69
) into (
63
) and by using the identity
a
+
b
2
/
a
−
2
​
b
=
(
a
−
b
)
2
/
a
a+b^{2}/a-2b=(a-b)^{2}/a
with
a
=
𝜹
⊤
​
𝜹
a=\bm{\delta}^{\top}\bm{\delta}
and
b
=
𝜹
⊤
​
𝜸
b=\bm{\delta}^{\top}\bm{\gamma}
.
The formula for forecaster
X
2
​
t
X_{2t}
follows analogously.
For the uncertainty component under squared error loss
𝖴𝖭𝖢
¯
=
𝔼
⁡
[
(
𝔼
⁡
[
Y
t
]
−
Y
t
)
2
]
=
𝔼
⁡
[
Y
t
2
]
\overline{\mathsf{UNC}}=\mathbb{E}\big[(\mathbb{E}[Y_{t}]-Y_{t})^{2}\big]=\mathbb{E}[Y^{2}_{t}]
since
𝔼
⁡
[
Y
t
]
=
0
\mathbb{E}[Y_{t}]=0
.
Since
ε
Y
,
t
∼
𝒩
⁡
(
0
,
1
)
\varepsilon_{Y,t}\sim\mathcal{N}(0,1)
and
Var
⁡
(
ε
Y
,
t
)
=
𝔼
⁡
[
ε
Y
,
t
2
]
=
1
\operatorname{Var}(\varepsilon_{Y,t})=\mathbb{E}[\varepsilon_{Y,t}^{2}]=1
, the uncertainty component is given by
𝖴𝖭𝖢
¯
\displaystyle\overline{\mathsf{UNC}}
=
𝔼
⁡
[
Y
t
2
]
\displaystyle=\mathbb{E}[Y^{2}_{t}]
=
γ
K
2
​
𝔼
​
[
K
t
2
]
+
γ
L
2
​
𝔼
​
[
L
t
2
]
+
γ
M
2
​
𝔼
​
[
M
t
2
]
+
γ
N
2
​
𝔼
​
[
N
t
2
]
+
𝔼
⁡
[
ε
Y
,
t
2
]
\displaystyle=\gamma_{K}^{2}\mathbb{E}[K_{t}^{2}]+\gamma_{L}^{2}\mathbb{E}[L_{t}^{2}]+\gamma_{M}^{2}\mathbb{E}[M_{t}^{2}]+\gamma_{N}^{2}\mathbb{E}[N_{t}^{2}]+\mathbb{E}[\varepsilon_{Y,t}^{2}]
=
(
γ
K
2
+
γ
L
2
+
γ
M
2
+
γ
N
2
)
​
ς
+
1
\displaystyle=(\gamma_{K}^{2}+\gamma_{L}^{2}+\gamma_{M}^{2}+\gamma_{N}^{2})\varsigma+1
=
ς
⋅
𝜸
⊤
​
𝜸
+
1
,
\displaystyle=\varsigma\cdot\bm{\gamma}^{\top}\bm{\gamma}+1,
which concludes the proof.
∎
Appendix B
Relation to other decompositions
Several early contributions to the forecast evaluation literature propose score decompositions that are structurally similar to the one employed in this paper.
First, the population decomposition of the squared error score in
Murphy (1973)
coincides with the population score decomposition in (
11
).
For the squared error score, (
11
) simplifies to
𝖲
¯
i
=
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
,
X
i
​
t
C
)
]
−
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
C
,
r
¯
)
]
+
𝖴𝖭𝖢
¯
\overline{\mathsf{S}}_{i}=\mathbb{E}\!\left[\mathsf{S}(X_{it},X^{\textsf{C}}_{it})\right]-\mathbb{E}\!\left[\mathsf{S}(X^{\textsf{C}}_{it},\bar{r})\right]+\overline{\mathsf{UNC}}
.
Murphy (1973)
labels these components calibration, resolution, and uncertainty.
This representation is prevalent in the literature and it is often applied to the
Brier (1950)
score, which describes the squared error in the context of probability forecasts for binary outcomes; see e.g.,
Elliott and Timmermann (2016)
and
Pohle (2020)
.
As such, our paper augments the original
Murphy (1973)
decomposition with inference under linear recalibration.
Second, the squared error score decomposition of
Mincer and Zarnowitz (1969, Equation 5a)
reads as
Average Score
=
Mean Component
+
Slope Component
+
Residual Component
.
\displaystyle\text{Average Score}=\text{Mean Component}+\text{Slope Component}+\text{Residual Component}.
(71)
In terms of our notation, and the refinement of unconditional and conditional miscalibration terms of
Gneiting and Resin (2023)
, the components in (
71
) are
𝖲
¯
i
=
𝗎𝖬𝖢𝖡
¯
i
+
𝖼𝖬𝖢𝖡
¯
i
+
(
𝖴𝖭𝖢
¯
−
𝖣𝖲𝖢
¯
i
)
\overline{\mathsf{S}}_{i}\;=\;\overline{\mathsf{uMCB}}_{i}\;+\;\overline{\mathsf{cMCB}}_{i}\;+\;\left(\overline{\mathsf{UNC}}\;-\;\overline{\mathsf{DSC}}_{i}\right)
,
where
𝗎𝖬𝖢𝖡
¯
i
\overline{\mathsf{uMCB}}_{i}
and
𝖼𝖬𝖢𝖡
¯
i
\overline{\mathsf{cMCB}}_{i}
are denoted as unconditional and conditional miscalibration components, which are non-negative and satisfy
𝖬𝖢𝖡
¯
i
=
𝗎𝖬𝖢𝖡
¯
i
+
𝖼𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}=\overline{\mathsf{uMCB}}_{i}+\overline{\mathsf{cMCB}}_{i}
given that they are obtained from
𝗎𝖬𝖢𝖡
¯
i
=
𝖲
¯
i
−
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
+
c
,
Y
t
)
]
and
𝖼𝖬𝖢𝖡
¯
i
=
𝔼
⁡
[
𝖲
⁡
(
X
i
​
t
+
c
,
Y
t
)
]
−
𝖲
¯
i
C
,
\displaystyle\overline{\mathsf{uMCB}}_{i}=\overline{\mathsf{S}}_{i}\;-\;\mathbb{E}[\mathsf{S}(X_{it}+c,Y_{t})]\qquad\text{and}\qquad\overline{\mathsf{cMCB}}_{i}=\mathbb{E}\left[\mathsf{S}(X_{it}+c,Y_{t})\right]\;-\;\overline{\mathsf{S}}_{i}^{\textsf{C}},
with constant
c
c
chosen such that
X
i
​
t
+
c
X_{it}+c
is unconditionally calibrated, i.e.,
𝔼
⁡
[
X
i
​
t
+
c
]
=
𝔼
⁡
[
Y
t
]
\mathbb{E}[X_{it}+c]=\mathbb{E}[Y_{t}]
.
In this sense, the score decomposition in
Mincer and Zarnowitz (1969)
closely mirrors the structure considered here.
Although the residual component in (
71
) conflates uncertainty and discrimination, this is unproblematic for comparative evaluation, as the uncertainty term is forecast-invariant and cancels out in pairwise comparisons.
Accordingly, the residual component can be viewed as a re-normalized version of discrimination.
Mincer and Zarnowitz (1969)
however place little emphasis on this residual component, referring to it merely as a residual term without further interpretation or diagnostic use.
In summary, the aforementioned decompositions can be viewed as special cases of the general score decomposition in (
11
). The asymptotic theory developed in this paper is sufficiently general to be readily applicable to these alternative representations.
For example, in the case of the
Mincer and Zarnowitz (1969)
decomposition, inference for the combined term
(
𝖴𝖭𝖢
¯
−
𝖣𝖲𝖢
¯
i
)
\left(\overline{\mathsf{UNC}}-\overline{\mathsf{DSC}}_{i}\right)
follows directly from our results, and inference for
𝗎𝖬𝖢𝖡
¯
i
\overline{\mathsf{uMCB}}_{i}
and
𝖼𝖬𝖢𝖡
¯
i
\overline{\mathsf{cMCB}}_{i}
only requires one additional unconditional estimation step for the constant
c
c
.
Appendix C
Details on the simulation setup for quantile forecasts
Here, we provide detailed calculations for the population
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
components on the check loss decomposition for quantile forecasts for the simulations from Section
4
.
Proposition C.1
.
Consider the DGP in (
23
) and (
27
). For
α
∈
(
0
,
1
)
\alpha\in(0,1)
, define
z
α
=
Φ
−
1
​
(
α
)
z_{\alpha}=\Phi^{-1}(\alpha)
.
Using
𝒲
i
​
t
=
σ
⁡
{
𝐖
i
​
t
}
\mathcal{W}_{it}=\sigma\{\bm{W}_{it}\}
with
𝐖
i
​
t
=
(
1
,
X
i
​
t
α
)
⊤
\bm{W}_{it}=(1,X^{\alpha}_{it})^{\top}
and the check loss
𝖲
α
(
x
,
y
)
=
(
𝟙
{
x
≥
y
}
−
α
)
(
x
−
y
)
\mathsf{S}_{\alpha}(x,y)=(\mathds{1}\{x\geq y\}-\alpha)(x-y)
, we get
𝖬𝖢𝖡
¯
1
\displaystyle\overline{\mathsf{MCB}}_{1}
=
m
1
​
(
Φ
⁡
(
κ
1
)
+
α
−
1
)
+
s
1
​
ϕ
​
(
κ
1
)
−
σ
1
|
X
​
ϕ
​
(
z
α
)
,
\displaystyle=m_{1}\Bigl(\Phi(\kappa_{1})+\alpha-1\Bigr)+s_{1}\,\phi(\kappa_{1})-\sigma_{1\mid X}\,\phi(z_{\alpha}),
(72)
𝖣𝖲𝖢
¯
1
\displaystyle\overline{\mathsf{DSC}}_{1}
=
ϕ
⁡
(
z
α
)
​
(
σ
Y
−
σ
1
|
X
)
,
\displaystyle=\phi(z_{\alpha})\bigl(\sigma_{Y}-\sigma_{1\mid X}\bigr),
(73)
and
𝖴𝖭𝖢
¯
=
σ
Y
​
ϕ
​
(
z
α
)
\overline{\mathsf{UNC}}=\sigma_{Y}\,\phi(z_{\alpha})
.
In the above,
σ
Y
2
=
Var
⁡
(
Y
t
)
=
ς
​
𝛄
⊤
​
𝛄
+
1
\sigma_{Y}^{2}=\operatorname{Var}(Y_{t})=\varsigma\,\bm{\gamma}^{\top}\bm{\gamma}+1
with
ς
=
1
1
−
β
2
\varsigma=\frac{1}{1-\beta^{2}}
, and
σ
1
|
X
2
\displaystyle\sigma_{1\mid X}^{2}
:
=
Var
⁡
(
Y
t
∣
X
1
​
t
α
)
=
σ
Y
2
−
ς
​
(
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
\displaystyle:=\operatorname{Var}(Y_{t}\mid X^{\alpha}_{1t})=\sigma_{Y}^{2}-\varsigma\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}}
m
1
\displaystyle m_{1}
:
=
𝔼
⁡
[
Y
t
−
X
i
​
t
α
]
=
−
(
δ
0
+
z
α
)
,
\displaystyle:=\mathbb{E}[Y_{t}-X^{\alpha}_{it}]=-(\delta_{0}+z_{\alpha}),
s
1
2
\displaystyle s_{1}^{2}
:
=
Var
⁡
(
Y
t
−
X
i
​
t
α
)
=
1
+
ς
⁡
(
𝜸
⊤
​
𝜸
+
𝜹
⊤
​
𝜹
−
2
​
𝜹
⊤
​
𝜸
)
,
\displaystyle:=\operatorname{Var}(Y_{t}-X^{\alpha}_{it})=1+\varsigma\bigl(\bm{\gamma}^{\top}\bm{\gamma}+\bm{\delta}^{\top}\bm{\delta}-2\bm{\delta}^{\top}\bm{\gamma}\bigr),
κ
1
\displaystyle\kappa_{1}
:
=
m
1
s
1
.
\displaystyle:=\frac{m_{1}}{s_{1}}.
It further holds that
𝖣𝖲𝖢
¯
1
\overline{\mathsf{DSC}}_{1}
is increasing with
(
𝛅
⊤
​
𝛄
)
2
𝛅
⊤
​
𝛅
\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}}
and
𝖬𝖢𝖡
¯
1
\overline{\mathsf{MCB}}_{1}
is increasing in
s
1
s_{1}
and in
(
𝛅
⊤
​
𝛄
)
2
𝛅
⊤
​
𝛅
\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}}
.
For the second forecaster
X
2
​
t
α
X_{2t}^{\alpha}
, equivalent statements hold with
(
δ
0
,
𝛅
)
(\delta_{0},\bm{\delta})
replaced by
(
ξ
0
,
𝛏
)
(\xi_{0},\bm{\xi})
.
For the four parameterizations given in Table
4
, we continue to simplify the closed-form expressions for
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
from Proposition
C.1
as functions of
k
k
,
α
\alpha
, and
ς
\varsigma
such that the
𝖬𝖢𝖡
¯
\overline{\mathsf{MCB}}
and
𝖣𝖲𝖢
¯
\overline{\mathsf{DSC}}
relations from Table
4
can be verified.
Notice that in the following, the expressions for
κ
⁡
(
k
)
\kappa(k)
vary for the different DGPs denoted 1), 2), 4) and 5).
First, for the check loss decomposition for DGP 1) in Table
4
, we have
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
=
m
⁡
(
Φ
⁡
(
m
s
⁡
(
k
)
)
+
α
−
1
)
+
s
⁡
(
k
)
​
ϕ
​
(
m
s
⁡
(
k
)
)
−
1
+
ς
16
​
ϕ
​
(
z
α
)
,
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
=
ϕ
⁡
(
z
α
)
​
(
1
+
3
​
ς
16
−
1
+
ς
16
)
,
m
=
−
1
+
ς
16
​
z
α
,
s
⁡
(
k
)
=
Var
⁡
(
Y
t
−
X
i
​
t
α
)
=
1
+
ς
⁡
(
k
2
2
+
1
16
)
.
\displaystyle\begin{aligned} \overline{\mathsf{MCB}}_{1}(k)&=\overline{\mathsf{MCB}}_{2}(k)=m\Bigl(\Phi\!\Bigl(\tfrac{m}{s(k)}\Bigr)+\alpha-1\Bigr)+s(k)\,\phi\!\Bigl(\tfrac{m}{s(k)}\Bigr)-\sqrt{1+\tfrac{\varsigma}{16}}\,\phi(z_{\alpha}),\\
\overline{\mathsf{DSC}}_{1}&=\overline{\mathsf{DSC}}_{2}=\phi(z_{\alpha})\left(\sqrt{1+\tfrac{3\varsigma}{16}}-\sqrt{1+\tfrac{\varsigma}{16}}\right),\\
m&=-\sqrt{1+\frac{\varsigma}{16}}z_{\alpha},\\
s(k)&=\sqrt{\operatorname{Var}(Y_{t}-X^{\alpha}_{it})}=\sqrt{\,1+\varsigma\left(\tfrac{k^{2}}{2}+\tfrac{1}{16}\right)\,}.\end{aligned}
(74)
Here,
s
⁡
(
k
)
s(k)
is increasing in
k
k
, such that
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)
are increasing in
k
k
.
𝖬𝖢𝖡
¯
1
​
(
0
)
=
𝖬𝖢𝖡
¯
2
​
(
0
)
\overline{\mathsf{MCB}}_{1}(0)=\overline{\mathsf{MCB}}_{2}(0)
can be obtained by simplifying the above formula for
k
=
0
k=0
.
Furthermore,
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
>
0
\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}>0
does not depend on
k
k
.
Second, for the check loss decomposition for DGP 2) in Table
4
, we have
𝖬𝖢𝖡
¯
1
=
0
,
𝖬𝖢𝖡
¯
2
​
(
k
)
=
m
2
​
(
Φ
⁡
(
m
2
s
2
​
(
k
)
)
+
α
−
1
)
+
s
2
​
(
k
)
​
ϕ
​
(
m
2
s
2
​
(
k
)
)
−
1
+
ς
16
​
ϕ
​
(
z
α
)
,
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
=
ϕ
⁡
(
z
α
)
​
(
1
+
3
​
ς
16
−
1
+
ς
16
)
,
m
2
=
−
1
+
ς
16
​
z
α
,
s
2
​
(
k
)
=
Var
⁡
(
Y
t
−
X
2
​
t
α
)
=
1
+
ς
16
+
ς
​
k
2
2
.
\displaystyle\begin{aligned} \overline{\mathsf{MCB}}_{1}&=0,\\[2.15277pt]
\overline{\mathsf{MCB}}_{2}(k)&=m_{2}\Bigl(\Phi\!\Bigl(\tfrac{m_{2}}{s_{2}(k)}\Bigr)+\alpha-1\Bigr)+s_{2}(k)\,\phi\!\Bigl(\tfrac{m_{2}}{s_{2}(k)}\Bigr)-\sqrt{1+\tfrac{\varsigma}{16}}\,\phi(z_{\alpha}),\\[4.30554pt]
\overline{\mathsf{DSC}}_{1}&=\overline{\mathsf{DSC}}_{2}=\phi(z_{\alpha})\left(\sqrt{1+\tfrac{3\varsigma}{16}}-\sqrt{1+\tfrac{\varsigma}{16}}\right),\\[4.30554pt]
m_{2}&=-\sqrt{1+\frac{\varsigma}{16}}z_{\alpha},\\
s_{2}(k)&=\sqrt{\operatorname{Var}(Y_{t}-X^{\alpha}_{2t})}=\sqrt{\,1+\tfrac{\varsigma}{16}+\tfrac{\varsigma k^{2}}{2}\,}.\end{aligned}
(75)
As before,
s
2
​
(
k
)
s_{2}(k)
is increasing in
k
k
, such that
𝖬𝖢𝖡
¯
2
​
(
k
)
\overline{\mathsf{MCB}}_{2}(k)
is increasing in
k
k
, and
𝖣𝖲𝖢
¯
1
=
𝖣𝖲𝖢
¯
2
>
0
\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{DSC}}_{2}>0
are independent of
k
k
.
𝖬𝖢𝖡
¯
2
​
(
0
)
\overline{\mathsf{MCB}}_{2}(0)
can again be obtained by simplifying the above formula for
k
=
0
k=0
.
Third, for the check loss decomposition for DGP 4) in Table
4
, we have
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
=
m
α
​
(
k
)
​
(
Φ
⁡
(
m
α
​
(
k
)
s
⁡
(
k
)
)
+
α
−
1
)
+
s
⁡
(
k
)
​
ϕ
​
(
m
α
​
(
k
)
s
⁡
(
k
)
)
−
ς
​
k
2
2
+
1
​
ϕ
​
(
z
α
)
,
𝖣𝖲𝖢
¯
1
​
(
k
)
=
𝖣𝖲𝖢
¯
2
​
(
k
)
=
ϕ
⁡
(
z
α
)
​
(
ς
​
k
2
+
1
−
ς
​
k
2
2
+
1
)
,
m
α
​
(
k
)
=
−
1
+
8
15
​
k
2
​
z
α
,
s
⁡
(
k
)
=
Var
⁡
(
Y
t
−
X
i
​
t
α
)
=
1
+
ς
​
k
2
2
+
ς
8
.
\displaystyle\begin{aligned} \overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)&=m_{\alpha}(k)\Bigl(\Phi\!\Bigl(\tfrac{m_{\alpha}(k)}{s(k)}\Bigr)+\alpha-1\Bigr)+s(k)\,\phi\!\Bigl(\tfrac{m_{\alpha}(k)}{s(k)}\Bigr)-\sqrt{\tfrac{\varsigma k^{2}}{2}+1}\,\phi(z_{\alpha}),\\
\overline{\mathsf{DSC}}_{1}(k)=\overline{\mathsf{DSC}}_{2}(k)&=\phi(z_{\alpha})\left(\sqrt{\varsigma k^{2}+1}-\sqrt{\tfrac{\varsigma k^{2}}{2}+1}\right),\\
m_{\alpha}(k)&=-\sqrt{1+\frac{8}{15}k^{2}}z_{\alpha},\\
s(k)&=\sqrt{\operatorname{Var}(Y_{t}-X^{\alpha}_{it})}=\sqrt{\,1+\tfrac{\varsigma k^{2}}{2}+\tfrac{\varsigma}{8}\,}.\end{aligned}
(76)
Here,
𝖣𝖲𝖢
¯
1
​
(
k
)
=
𝖣𝖲𝖢
¯
2
​
(
k
)
\overline{\mathsf{DSC}}_{1}(k)=\overline{\mathsf{DSC}}_{2}(k)
are increasing in
k
k
(as
k
2
k^{2}
grows faster than
k
2
/
2
k^{2}/2
) and we have
𝖣𝖲𝖢
¯
1
​
(
0
)
=
𝖣𝖲𝖢
¯
2
​
(
0
)
=
0
\overline{\mathsf{DSC}}_{1}(0)=\overline{\mathsf{DSC}}_{2}(0)=0
.
Furthermore,
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
>
0
\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)>0
holds by (
76
).
Fourth, for the check loss decomposition for DGP 5) in Table
4
with
ξ
0
=
ξ
0
​
(
k
,
α
)
\xi_{0}=\xi_{0}(k,\alpha)
, we have
𝖣𝖲𝖢
¯
1
=
0
,
𝖣𝖲𝖢
¯
2
​
(
k
)
=
ϕ
⁡
(
z
α
)
​
(
ς
​
k
2
+
1
−
ς
​
k
2
2
+
1
)
,
𝖬𝖢𝖡
¯
1
​
(
k
)
=
−
(
δ
0
+
z
α
)
​
(
Φ
⁡
(
−
(
δ
0
+
z
α
)
s
1
​
(
k
)
)
+
α
−
1
)
+
s
1
​
(
k
)
​
ϕ
​
(
−
(
δ
0
+
z
α
)
s
1
​
(
k
)
)
−
ς
​
k
2
+
1
​
ϕ
​
(
z
α
)
,
𝖬𝖢𝖡
¯
2
​
(
k
)
=
−
(
ξ
0
+
z
α
)
​
(
Φ
⁡
(
−
(
ξ
0
+
z
α
)
s
2
​
(
k
)
)
+
α
−
1
)
+
s
2
​
(
k
)
​
ϕ
​
(
−
(
ξ
0
+
z
α
)
s
2
​
(
k
)
)
−
ς
​
k
2
2
+
1
​
ϕ
​
(
z
α
)
,
s
1
​
(
k
)
:
=
Var
⁡
(
Y
t
−
X
1
​
t
α
)
=
1
+
ς
​
k
2
+
ς
8
,
s
2
​
(
k
)
:
=
Var
⁡
(
Y
t
−
X
2
​
t
α
)
=
1
+
ς
​
k
2
2
+
ς
8
.
\displaystyle\begin{aligned} \overline{\mathsf{DSC}}_{1}&=0,\\
\overline{\mathsf{DSC}}_{2}(k)&=\phi(z_{\alpha})\left(\sqrt{\varsigma k^{2}+1}-\sqrt{\tfrac{\varsigma k^{2}}{2}+1}\right),\\
\overline{\mathsf{MCB}}_{1}(k)&=-(\delta_{0}+z_{\alpha})\Bigl(\Phi\!\Bigl(\tfrac{-(\delta_{0}+z_{\alpha})}{s_{1}(k)}\Bigr)+\alpha-1\Bigr)+s_{1}(k)\,\phi\!\Bigl(\tfrac{-(\delta_{0}+z_{\alpha})}{s_{1}(k)}\Bigr)-\sqrt{\varsigma k^{2}+1}\,\phi(z_{\alpha}),\\
\overline{\mathsf{MCB}}_{2}(k)&=-(\xi_{0}+z_{\alpha})\Bigl(\Phi\!\Bigl(\tfrac{-(\xi_{0}+z_{\alpha})}{s_{2}(k)}\Bigr)+\alpha-1\Bigr)+s_{2}(k)\,\phi\!\Bigl(\tfrac{-(\xi_{0}+z_{\alpha})}{s_{2}(k)}\Bigr)-\sqrt{\tfrac{\varsigma k^{2}}{2}+1}\,\phi(z_{\alpha}),\\
s_{1}(k)&:=\sqrt{\operatorname{Var}(Y_{t}-X^{\alpha}_{1t})}=\sqrt{\,1+\varsigma k^{2}+\tfrac{\varsigma}{8}\,},\\
s_{2}(k)&:=\sqrt{\operatorname{Var}(Y_{t}-X^{\alpha}_{2t})}=\sqrt{\,1+\tfrac{\varsigma k^{2}}{2}+\tfrac{\varsigma}{8}\,}.\end{aligned}
(77)
As before,
𝖣𝖲𝖢
¯
2
​
(
k
)
\overline{\mathsf{DSC}}_{2}(k)
is increasing in
k
k
(as
k
2
k^{2}
grows faster than
k
2
/
2
k^{2}/2
) and we have
𝖣𝖲𝖢
¯
2
​
(
0
)
=
0
\overline{\mathsf{DSC}}_{2}(0)=0
.
Notice for this that the choice of
ξ
0
\xi_{0}
does not affect the discrimination of the second forecast at all.
Figure C.1
:
Values for
ξ
0
​
(
k
,
α
)
\xi_{0}(k,\alpha)
used for the quantile DGP 5) in Table
4
for
k
∈
[
0
,
1
]
k\in[0,1]
and
α
∈
{
0.01
,
0.05
,
0.1
,
0.25
,
0.5
}
\alpha\in\{0.01,0.05,0.1,0.25,0.5\}
, such that
𝖬𝖢𝖡
¯
1
​
(
k
)
=
𝖬𝖢𝖡
¯
2
​
(
k
)
\overline{\mathsf{MCB}}_{1}(k)=\overline{\mathsf{MCB}}_{2}(k)
holds as accurately as possible for all
k
k
and
α
\alpha
for the quantities from (
77
).
Equality of the
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
,
i
=
1
,
2
i=1,2
terms in (
77
) is difficult to obtain analytically.
Hence, we choose
ξ
0
=
ξ
0
​
(
k
,
α
)
\xi_{0}=\xi_{0}(k,\alpha)
depending on
α
∈
{
0.01
,
0.05
,
0.1
,
0.25
,
0.5
}
\alpha\in\{0.01,\,0.05,\,0.1,\,0.25,\,0.5\}
and a sequence of values of
k
∈
[
0
,
1
]
k\in[0,1]
numerically such that
𝖬𝖢𝖡
¯
1
​
(
k
,
α
)
=
𝖬𝖢𝖡
¯
2
​
(
k
,
α
)
\overline{\mathsf{MCB}}_{1}(k,\alpha)=\overline{\mathsf{MCB}}_{2}(k,\alpha)
holds as accurately as possible.
Figure
C.1
displays these numeric solutions for
ξ
0
=
ξ
0
​
(
k
,
α
)
\xi_{0}=\xi_{0}(k,\alpha)
as functions of
k
k
and
α
\alpha
.
Figure C.2
:
Population values of
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
,
i
=
1
,
2
i=1,2
from (
74
)–(
77
) for a range of values for
k
k
, our five choices of
α
\alpha
, and the parameter values
ξ
0
​
(
k
,
α
)
\xi_{0}(k,\alpha)
displayed in Figure
C.1
.
Figure
C.2
displays the expressions of
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
,
i
=
1
,
2
i=1,2
from (
74
)–(
77
) for the considered values of
k
k
and
α
\alpha
, which confirms the properties of our simulation setup discussed above.
In particular, Figure
C.2
confirms that the numeric choices of
ξ
0
​
(
k
,
α
)
\xi_{0}(k,\alpha)
yield the desired results.
Proof of Proposition
C.1
.
We prove the claims for
i
=
1
i=1
; the case
i
=
2
i=2
follows by replacing
(
δ
0
,
𝜹
)
(\delta_{0},\bm{\delta})
with
(
ξ
0
,
𝝃
)
(\xi_{0},\bm{\xi})
.
First, under (
23
), the vector
𝐕
t
\mathbf{V}_{t}
has mean zero and covariance matrix
ς
​
I
4
\varsigma I_{4}
, hence
𝜸
⊤
​
𝐕
t
∼
𝒩
⁡
(
0
,
ς
​
𝜸
⊤
​
𝜸
)
\bm{\gamma}^{\top}\mathbf{V}_{t}\sim\mathcal{N}(0,\varsigma\,\bm{\gamma}^{\top}\bm{\gamma})
and
Y
t
=
𝜸
⊤
​
𝐕
t
+
ε
Y
,
t
∼
𝒩
⁡
(
0
,
σ
Y
2
)
,
σ
Y
2
=
ς
​
𝜸
⊤
​
𝜸
+
1
.
Y_{t}=\bm{\gamma}^{\top}\mathbf{V}_{t}+\varepsilon_{Y,t}\sim\mathcal{N}(0,\sigma_{Y}^{2}),\qquad\sigma_{Y}^{2}=\varsigma\,\bm{\gamma}^{\top}\bm{\gamma}+1.
Moreover, with
X
1
​
t
α
=
𝐕
t
⊤
​
𝜹
+
δ
0
+
z
α
X_{1t}^{\alpha}=\mathbf{V}_{t}^{\top}\bm{\delta}+\delta_{0}+z_{\alpha}
we have
Var
⁡
(
X
1
​
t
α
)
=
ς
​
𝜹
⊤
​
𝜹
,
and
Cov
⁡
(
Y
t
,
X
1
​
t
α
)
=
ς
​
𝜹
⊤
​
𝜸
.
\displaystyle\operatorname{Var}(X_{1t}^{\alpha})=\varsigma\,\bm{\delta}^{\top}\bm{\delta},\qquad\text{ and }\qquad\operatorname{Cov}(Y_{t},X_{1t}^{\alpha})=\varsigma\,\bm{\delta}^{\top}\bm{\gamma}.
Since
(
Y
t
,
X
1
​
t
α
)
(Y_{t},X_{1t}^{\alpha})
is jointly Gaussian,
Y
t
|
X
1
​
t
α
Y_{t}\mid X_{1t}^{\alpha}
is Gaussian with constant conditional variance
σ
1
|
X
2
=
Var
⁡
(
Y
t
)
−
Cov
⁡
(
Y
t
,
X
1
​
t
α
)
2
Var
⁡
(
X
1
​
t
α
)
=
σ
Y
2
−
ς
​
(
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
.
\displaystyle\sigma_{1\mid X}^{2}=\operatorname{Var}(Y_{t})-\frac{\operatorname{Cov}(Y_{t},X_{1t}^{\alpha})^{2}}{\operatorname{Var}(X_{1t}^{\alpha})}=\sigma_{Y}^{2}-\varsigma\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}}.
(78)
We continue by deriving the formula for
𝖴𝖭𝖢
¯
\overline{\mathsf{UNC}}
.
Since the
α
\alpha
-quantile functional is strictly consistent for the check loss, the expected loss
𝔼
⁡
[
𝖲
α
​
(
x
,
Y
t
)
]
\mathbb{E}[\mathsf{S}_{\alpha}(x,Y_{t})]
is uniquely minimized at the true conditional quantile
Q
α
​
(
Y
t
)
=
σ
Y
​
z
α
=
σ
Y
​
Φ
−
1
​
(
α
)
Q_{\alpha}(Y_{t})=\sigma_{Y}z_{\alpha}=\sigma_{Y}\Phi^{-1}(\alpha)
.
To obtain an explicit formula for the check loss at the true quantile, let
Y
t
=
σ
Y
​
Z
t
Y_{t}=\sigma_{Y}Z_{t}
with
Z
t
∼
𝒩
⁡
(
0
,
1
)
Z_{t}\sim\mathcal{N}(0,1)
.
Then,
𝔼
⁡
[
𝖲
α
​
(
σ
Y
​
z
α
,
Y
t
)
]
\displaystyle\mathbb{E}[\mathsf{S}_{\alpha}(\sigma_{Y}z_{\alpha},Y_{t})]
=
𝔼
[
(
α
−
𝟙
{
Z
t
≤
z
α
}
)
(
σ
Y
Z
t
−
σ
Y
z
α
)
]
\displaystyle=\mathbb{E}\big[(\alpha-\mathds{1}\{Z_{t}\leq z_{\alpha}\})(\sigma_{Y}Z_{t}-\sigma_{Y}z_{\alpha})\big]
=
σ
Y
𝔼
[
(
α
−
𝟙
{
Z
t
≤
z
α
}
)
(
Z
t
−
z
α
)
]
\displaystyle=\sigma_{Y}\mathbb{E}\big[(\alpha-\mathds{1}\{Z_{t}\leq z_{\alpha}\})(Z_{t}-z_{\alpha})\big]
=
σ
Y
(
α
𝔼
[
Z
t
−
z
α
]
−
𝔼
[
(
Z
t
−
z
α
)
𝟙
{
Z
t
≤
z
α
}
]
)
.
\displaystyle=\sigma_{Y}\left(\alpha\mathbb{E}[Z_{t}-z_{\alpha}]-\mathbb{E}\big[(Z_{t}-z_{\alpha})\mathds{1}\{Z_{t}\leq z_{\alpha}\}\big]\right).
Since
𝔼
⁡
[
Z
t
]
=
0
\mathbb{E}[Z_{t}]=0
, the first term becomes
−
α
​
z
α
-\alpha z_{\alpha}
.
For the second term,
𝔼
[
(
Z
t
−
z
α
)
𝟙
{
Z
t
≤
z
α
}
]
=
∫
−
∞
z
α
(
z
−
z
α
)
ϕ
(
z
)
d
z
=
−
ϕ
(
z
α
)
−
z
α
α
,
\mathbb{E}\big[(Z_{t}-z_{\alpha})\mathds{1}\{Z_{t}\leq z_{\alpha}\}\big]=\int_{-\infty}^{z_{\alpha}}(z-z_{\alpha})\phi(z)\,dz=-\phi(z_{\alpha})-z_{\alpha}\alpha,
which yields
𝔼
⁡
[
𝖲
α
​
(
σ
Y
​
z
α
,
Y
t
)
]
=
σ
Y
​
[
−
α
​
z
α
+
ϕ
⁡
(
z
α
)
+
z
α
​
α
]
=
σ
Y
​
ϕ
​
(
z
α
)
.
\displaystyle\mathbb{E}[\mathsf{S}_{\alpha}(\sigma_{Y}z_{\alpha},Y_{t})]=\sigma_{Y}\big[-\alpha z_{\alpha}+\phi(z_{\alpha})+z_{\alpha}\alpha\big]=\sigma_{Y}\phi(z_{\alpha}).
(79)
We continue to derive the close-form expression for the discrimination component.
Because
(
Y
t
,
X
1
​
t
α
)
(Y_{t},X_{1t}^{\alpha})
is jointly Gaussian, the conditional distribution
Y
t
|
X
1
​
t
α
Y_{t}\mid X_{1t}^{\alpha}
is normal with conditional variance
σ
1
|
X
2
=
Var
⁡
(
Y
t
∣
X
1
​
t
α
)
\sigma_{1\mid X}^{2}=\operatorname{Var}(Y_{t}\mid X_{1t}^{\alpha})
from (
78
) that does not depend on
X
1
​
t
α
X_{1t}^{\alpha}
.
Hence,
Y
t
|
X
1
​
t
α
∼
𝒩
⁡
(
𝔼
⁡
[
Y
t
∣
X
1
​
t
α
]
,
σ
1
|
X
2
)
and
Q
α
​
(
Y
t
∣
X
1
​
t
α
)
=
𝔼
⁡
[
Y
t
∣
X
1
​
t
α
]
+
σ
1
|
X
​
z
α
.
Y_{t}\mid X_{1t}^{\alpha}\sim\mathcal{N}\big(\mathbb{E}[Y_{t}\mid X_{1t}^{\alpha}],\;\sigma_{1\mid X}^{2}\big)\qquad\text{and}\qquad Q_{\alpha}(Y_{t}\mid X_{1t}^{\alpha})=\mathbb{E}[Y_{t}\mid X_{1t}^{\alpha}]+\sigma_{1\mid X}z_{\alpha}.
By the check loss identity for Gaussian distribution from (
79
), we obtain
𝔼
⁡
[
𝖲
α
​
(
Q
α
​
(
Y
t
∣
X
1
​
t
α
)
,
Y
t
)
∣
X
1
​
t
α
]
=
σ
1
|
X
​
ϕ
​
(
z
α
)
a.s.
,
\mathbb{E}\!\bigl[\mathsf{S}_{\alpha}\big(Q_{\alpha}(Y_{t}\mid X_{1t}^{\alpha}),Y_{t}\big)\mid X_{1t}^{\alpha}\bigr]=\sigma_{1\mid X}\phi(z_{\alpha})\quad\text{a.s.},
and therefore also
𝔼
⁡
[
𝖲
α
​
(
Q
α
​
(
Y
t
∣
X
1
​
t
α
)
,
Y
t
)
]
=
σ
1
|
X
​
ϕ
​
(
z
α
)
.
\mathbb{E}\!\bigl[\mathsf{S}_{\alpha}\bigl(Q_{\alpha}(Y_{t}\mid X_{1t}^{\alpha}),Y_{t}\bigr)\bigr]=\sigma_{1\mid X}\phi(z_{\alpha}).
Consequently,
𝖣𝖲𝖢
¯
1
=
𝖴𝖭𝖢
¯
−
𝔼
⁡
[
𝖲
α
​
(
Q
α
​
(
Y
t
∣
X
1
​
t
α
)
,
Y
t
)
]
=
σ
Y
​
ϕ
​
(
z
α
)
−
σ
1
|
X
​
ϕ
​
(
z
α
)
,
\overline{\mathsf{DSC}}_{1}=\overline{\mathsf{UNC}}-\mathbb{E}\!\bigl[\mathsf{S}_{\alpha}\bigl(Q_{\alpha}(Y_{t}\mid X_{1t}^{\alpha}),Y_{t}\bigr)\bigr]=\sigma_{Y}\phi(z_{\alpha})-\sigma_{1\mid X}\phi(z_{\alpha}),
which is (
73
),
and
𝖬𝖢𝖡
¯
1
=
𝔼
⁡
[
𝖲
α
​
(
X
1
​
t
α
,
Y
t
)
]
−
𝔼
⁡
[
𝖲
α
​
(
Q
α
​
(
Y
t
∣
X
1
​
t
α
)
,
Y
t
)
]
=
𝔼
⁡
[
𝖲
α
​
(
X
1
​
t
α
,
Y
t
)
]
−
σ
1
|
X
​
ϕ
​
(
z
α
)
,
\overline{\mathsf{MCB}}_{1}=\mathbb{E}[\mathsf{S}_{\alpha}(X_{1t}^{\alpha},Y_{t})]-\mathbb{E}[\mathsf{S}_{\alpha}(Q_{\alpha}(Y_{t}\mid X_{1t}^{\alpha}),Y_{t})]=\mathbb{E}[\mathsf{S}_{\alpha}(X_{1t}^{\alpha},Y_{t})]-\sigma_{1\mid X}\phi(z_{\alpha}),
for which we derive a closed form for
𝔼
⁡
[
𝖲
α
​
(
X
1
​
t
α
,
Y
t
)
]
\mathbb{E}[\mathsf{S}_{\alpha}(X_{1t}^{\alpha},Y_{t})]
in the following.
For this, define the forecast error
E
1
​
t
:=
Y
t
−
X
1
​
t
α
E_{1t}:=Y_{t}-X_{1t}^{\alpha}
.
Then
E
1
​
t
E_{1t}
is Gaussian with mean
m
1
=
𝔼
⁡
[
E
1
​
t
]
=
𝔼
⁡
[
Y
t
]
−
𝔼
⁡
[
X
1
​
t
α
]
=
−
(
δ
0
+
z
α
)
,
m_{1}=\mathbb{E}[E_{1t}]=\mathbb{E}[Y_{t}]-\mathbb{E}[X_{1t}^{\alpha}]=-(\delta_{0}+z_{\alpha}),
and variance
s
1
2
\displaystyle s_{1}^{2}
=
Var
⁡
(
Y
t
−
X
1
​
t
α
)
=
Var
⁡
(
Y
t
)
+
Var
⁡
(
X
1
​
t
α
)
−
2
​
Cov
⁡
(
Y
t
,
X
1
​
t
α
)
\displaystyle=\operatorname{Var}(Y_{t}-X_{1t}^{\alpha})=\operatorname{Var}(Y_{t})+\operatorname{Var}(X_{1t}^{\alpha})-2\operatorname{Cov}(Y_{t},X_{1t}^{\alpha})
=
1
+
ς
⁡
(
𝜸
⊤
​
𝜸
+
𝜹
⊤
​
𝜹
−
2
​
𝜹
⊤
​
𝜸
)
,
\displaystyle=1+\varsigma\bigl(\bm{\gamma}^{\top}\bm{\gamma}+\bm{\delta}^{\top}\bm{\delta}-2\bm{\delta}^{\top}\bm{\gamma}\bigr),
To compute
𝔼
⁡
[
𝖲
α
​
(
X
1
​
t
α
,
Y
t
)
]
\mathbb{E}[\mathsf{S}_{\alpha}(X_{1t}^{\alpha},Y_{t})]
, note that for
U
=
x
+
E
U=x+E
,
𝖲
α
(
x
,
U
)
=
(
𝟙
{
U
<
x
}
−
α
)
(
x
−
U
)
=
(
α
−
𝟙
{
E
<
0
}
)
E
.
\mathsf{S}_{\alpha}(x,U)=(\mathds{1}\{U<x\}-\alpha)(x-U)=(\alpha-\mathds{1}\{E<0\})E.
Hence,
𝔼
[
𝖲
α
(
x
,
U
)
]
=
α
𝔼
[
E
]
−
𝔼
[
E
1
{
E
<
0
}
]
.
\mathbb{E}[\mathsf{S}_{\alpha}(x,U)]=\alpha\,\mathbb{E}[E]-\mathbb{E}\!\bigl[E\,\mathds{1}\{E<0\}\bigr].
For
E
∼
𝒩
⁡
(
m
,
s
2
)
E\sim\mathcal{N}(m,s^{2})
, a direct calculation yields
𝔼
[
E
1
{
E
<
0
}
]
=
m
Φ
(
−
m
/
s
)
−
s
ϕ
(
m
/
s
)
,
\mathbb{E}\!\bigl[E\,\mathds{1}\{E<0\}\bigr]=m\,\Phi(-m/s)-s\,\phi(m/s),
and therefore
𝔼
⁡
[
𝖲
α
​
(
x
,
U
)
]
=
m
⁡
(
Φ
⁡
(
m
/
s
)
+
α
−
1
)
+
s
​
ϕ
​
(
m
/
s
)
.
\mathbb{E}[\mathsf{S}_{\alpha}(x,U)]=m\bigl(\Phi(m/s)+\alpha-1\bigr)+s\,\phi(m/s).
Applying this with
x
=
X
1
​
t
α
x=X^{\alpha}_{1t}
and
U
=
Y
t
U=Y_{t}
and using
κ
1
=
m
1
/
s
1
\kappa_{1}=m_{1}/s_{1}
gives
𝔼
⁡
[
𝖲
α
​
(
X
1
​
t
α
,
Y
t
)
]
=
m
1
​
(
Φ
⁡
(
κ
1
)
+
α
−
1
)
+
s
1
​
ϕ
​
(
κ
1
)
.
\mathbb{E}[\mathsf{S}_{\alpha}(X^{\alpha}_{1t},Y_{t})]=m_{1}\bigl(\Phi(\kappa_{1})+\alpha-1\bigr)+s_{1}\,\phi(\kappa_{1}).
We continue to establish monotonicity of
𝖬𝖢𝖡
¯
1
\overline{\mathsf{MCB}}_{1}
and
𝖣𝖲𝖢
¯
1
\overline{\mathsf{DSC}}_{1}
with respect to
κ
1
\kappa_{1}
and
R
1
=
(
𝜹
⊤
​
𝜸
)
2
𝜹
⊤
​
𝜹
R_{1}=\frac{(\bm{\delta}^{\top}\bm{\gamma})^{2}}{\bm{\delta}^{\top}\bm{\delta}}
.
For
𝖣𝖲𝖢
¯
1
\overline{\mathsf{DSC}}_{1}
, it is immediate that
σ
1
|
X
\sigma_{1|X}
is decreasing in
R
1
R_{1}
, such that
𝖣𝖲𝖢
¯
1
\overline{\mathsf{DSC}}_{1}
is increasing in
R
1
R_{1}
.
The same argument applies to
𝖬𝖢𝖡
¯
1
\overline{\mathsf{MCB}}_{1}
being increasing in
R
1
R_{1}
as only the latter part in (
72
) depends on
σ
1
|
X
\sigma_{1|X}
.
From (
72
), only the first two terms of
𝖬𝖢𝖡
¯
1
\overline{\mathsf{MCB}}_{1}
depend on
s
1
s_{1}
.
Define
g
⁡
(
s
1
)
:=
m
1
​
(
Φ
⁡
(
κ
1
)
+
α
−
1
)
+
s
1
​
ϕ
​
(
κ
1
)
,
κ
1
=
m
1
s
1
.
g(s_{1}):=m_{1}\bigl(\Phi(\kappa_{1})+\alpha-1\bigr)+s_{1}\,\phi(\kappa_{1}),\qquad\kappa_{1}=\frac{m_{1}}{s_{1}}.
Differentiating with respect to
s
1
s_{1}
and using
d
​
κ
1
d
​
s
1
=
−
κ
1
/
s
1
\frac{d\kappa_{1}}{ds_{1}}=-\kappa_{1}/s_{1}
, we obtain
d
​
g
​
(
s
1
)
d
​
s
1
\displaystyle\frac{dg(s_{1})}{ds_{1}}
=
m
1
​
ϕ
​
(
κ
1
)
​
d
​
κ
1
d
​
s
1
+
ϕ
⁡
(
κ
1
)
+
s
1
​
ϕ
′
​
(
κ
1
)
​
d
​
κ
1
d
​
s
1
\displaystyle=m_{1}\phi(\kappa_{1})\frac{d\kappa_{1}}{ds_{1}}+\phi(\kappa_{1})+s_{1}\phi^{\prime}(\kappa_{1})\frac{d\kappa_{1}}{ds_{1}}
=
−
m
1
​
κ
1
s
1
​
ϕ
​
(
κ
1
)
+
ϕ
⁡
(
κ
1
)
+
κ
1
2
​
ϕ
​
(
κ
1
)
\displaystyle=-\frac{m_{1}\kappa_{1}}{s_{1}}\phi(\kappa_{1})+\phi(\kappa_{1})+\kappa_{1}^{2}\phi(\kappa_{1})
=
ϕ
⁡
(
κ
1
)
>
0
,
\displaystyle=\phi(\kappa_{1})>0,
where we used
ϕ
′
​
(
x
)
=
−
x
​
ϕ
​
(
x
)
\phi^{\prime}(x)=-x\phi(x)
and
κ
1
=
m
1
/
s
1
\kappa_{1}=m_{1}/s_{1}
.
Since the remaining term
−
σ
1
|
X
​
ϕ
​
(
z
α
)
-\sigma_{1\mid X}\phi(z_{\alpha})
does not depend on
s
1
s_{1}
,
𝖬𝖢𝖡
¯
1
\overline{\mathsf{MCB}}_{1}
is strictly increasing in
s
1
s_{1}
.
∎
Appendix D
Additional Figures
Figure D.1
:
Population values of
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
,
i
=
1
,
2
i=1,2
for the mean forecasts from the DGP in (
23
)–(
25
) for the twelve parametrizations from Table
3
, following the close-form expressions of Proposition
4.1
.
Figure
D.1
plots the population values for
𝖬𝖢𝖡
¯
i
\overline{\mathsf{MCB}}_{i}
and
𝖣𝖲𝖢
¯
i
\overline{\mathsf{DSC}}_{i}
,
i
=
1
,
2
i=1,2
for the mean forecasts for the twelve DGPs from Table
3
.
Figure D.2
:
Daily E-mini returns (right) and Realized Variances (left) in gray, together with the corresponding variance forecasts in blue (left) and VaR forecast at levels
1
%
1\%
in orange and
5
%
5\%
in purple (right) for the forecasting models considered in Section
5.2
and the time period after the year 2019.
Figure
D.2
plots the time series of the variance and VaR forecasts together with their corresponding evaluation targets for the application of Section
5.2
.
Figure D.3
:
Model diagnostics for the linear recalibration regression for the inflation rate forecasts in Section
5.1
. We plot the model residuals against the forecasts (as the covariates of the underlying recalibration regression) together with a nonparametric polynomial regression and its
95
%
95\%
confidence bands.
The zero-line being mostly contained in the confidence bands implies no evidence against correct model specification. For further details, see the text of Appendix
D
.
Figure D.4
:
Model diagnostics for the linear recalibration regression for the variance forecasts in Section
5.2
. We plot the model residuals against the forecasts (as the covariates of the underlying recalibration regression) on a log-transformed
x
x
-axis together with a nonparametric polynomial regression and its
95
%
95\%
confidence bands.
The zero-line being mostly contained in the confidence bands implies no evidence against correct model specification. For further details, see the text of Appendix
D
.
Figure D.5
:
Model diagnostics for the linear recalibration regression for the VaR forecasts in Section
5.2
. We plot the generalized model residuals against the forecasts (as the covariates of the underlying recalibration regression) together with a nonparametric polynomial regression and its
95
%
95\%
confidence bands.
The zero-line being mostly contained in the confidence bands implies no evidence against correct model specification. For further details, see the text of Appendix
D
.
Figures
D.3
–
D.5
show model diagnostics for the linear recalibration regressions that are used for the score decompositions for the forecasts of the applications of Sections
5.1
–
5.2
.
For the mean forecasts in Figures
D.3
–
D.4
, we plot the model residuals
Y
t
−
𝑾
i
​
t
⊤
​
𝜽
^
i
​
T
Y_{t}-\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}
on the
y
y
-axis against the forecasts
X
i
​
t
X_{it}
(as the covariates of the underlying recalibration regressions) on the
x
x
-axis.
The blue curve and its pointwise
95
%
95\%
confidence band are obtained from a local polynomial mean regression, implemented via the
loess
function in the statistical software
R
, with automatically selected tuning parameters.
The black-dashed zero-line being inside these confidence bands for the majority of forecast values indicates no evidence against correct specification of the linear recalibration regressions.
In Figure
D.5
, we follow
Pohle et al. (2024)
and
Dimitriadis and Hoga (2026, Figures 4 and 6)
and plot the generalized quantile residuals, i.e., the identification functions,
𝖵
(
𝑾
i
​
t
⊤
𝜽
^
i
​
T
,
Y
t
)
=
𝟙
{
Y
t
≤
𝑾
i
​
t
⊤
𝜽
^
i
​
T
}
−
α
\mathsf{V}\big(\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT},Y_{t})=\mathds{1}\{Y_{t}\leq\bm{W}_{it}^{\top}\widehat{\bm{\theta}}_{iT}\}-\alpha
, against the quantile forecasts
X
i
​
t
X_{it}
together with a corresponding nonparametric mean regression and their pointwise 95% confidence bands.
The zero-line being mostly contained in the confidence bands again does not provide evidence against correct specification of the linear recalibration regressions.