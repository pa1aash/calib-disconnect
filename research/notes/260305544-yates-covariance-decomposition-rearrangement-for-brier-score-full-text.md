---
title: '[2603.05544] Yates covariance decomposition rearrangement for Brier score
  (full text)'
id: 260305544-yates-covariance-decomposition-rearrangement-for-brier-score-full-text
tags:
- code-llm-confidence-positioning-d82d00
- related
created: '2026-11-09T23:11:23.839694Z'
updated: '2026-11-09T23:27:44.711103Z'
source: https://arxiv.org/pdf/2603.05544
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT (via curl+pdftotext; short theory note, 1,901 words). Vieira:
  Brier = (sigma_F - sigma_Y)^2 + 2(sigma_F sigma_Y - sigma_FY) + (mu_F - mu_Y)^2.
  No LLM or code content. Reference for F decomposition only.'
---

An intuitive rearranging of the Yates covariance decomposition for
 probabilistic verification of forecasts with the Brier score
 Bruno Hebling Vieira
arXiv:2603.05544v2 [stat.ME] 22 Jun 2026
 Methods of Plasticity Research, Department of Psychology, University of Zurich, Zurich,
 Switzerland
 Orcid: 0000-0002-8770-7396
 bruno.heblingvieira@uzh.ch
 Abstract score measures the mean squared error between pre-
 dicted probabilities and the actual binary outcomes.
 Proper scoring rules are essential for evaluating prob- For forecast–outcome pairs, the Brier score is defined
 abilistic forecasts. We propose a simple algebraic as:
 rearrangement of the Yates covariance decomposi-
 tion of the Brier score into three independently non- BS = E[(𝐹 − 𝑌 )2 ]
 negative terms: a variance mismatch term, a cor-
 relation deficit term, and a calibration-in-the-large where 𝐹 is the random variable representing the
 term. This rearrangement makes the optimality con- predicted probability of the event, 𝑌 ∈ {0, 1} is the
 ditions for perfect forecasting transparent: the opti- random variable representing the binary outcome (1
 mal forecast must simultaneously match the variance if the event occurs, 0 otherwise), and E[⋅] denotes
 of outcomes, achieve perfect positive correlation with the expectation over the joint distribution of (𝐹 , 𝑌 ).
 outcomes, and match the mean of outcomes. Any The Brier score ranges from 0 to 1, with lower values
 deviation from these conditions results in a positive indicating better predictive accuracy.
 contribution to the Brier score. Decompositions of the Brier score are useful be-
 cause they provide insights into different aspects of
 forecast performance. By breaking down the Brier
 1 Introduction score into components, we can better understand the
 sources of forecast errors and identify areas for im-
 Proper scoring rules are a fundamental concept in the provement.
 evaluation of probabilistic forecasts [1]. They pro- In this note, we will adopt the nomenclature of
 vide a principled way to assess the accuracy of pre- Mitchell [3].
 dicted probabilities by assigning a numerical score Multiple decompositions of the Brier score have
 based on the predicted probability and the actual been proposed in the literature [4–7].
 outcome. A scoring rule is considered proper if it
 encourages truthful reporting of probabilities, mean- 1.1 Uncertainty, Resolution & Relia-
 ing that the expected score is maximized when the
 bility
 predicted probabilities match the true probabilities.
 One of the most widely used proper scoring rules First, the Brier Score was decomposed into Sharp-
 is the Brier score, introduced by Brier [2]. The Brier ness & Reliability components by Sanders [4] by con-
 1
ditioning on the predicted probabilities 𝐹 . instead of the predicted probabilities. First, by condi-
 tioning on the actual outcomes 𝑌 , we can decompose
 the Brier score into Excess & Correctness components
 2
 BS = E[(𝐹 − 𝑌 ) ] as
 2
 = ⏟⏟⏟
 E[Var(𝑌
 ⏟∣ 𝐹⏟
 ⏟⏟ )] + ⏟⏟
 E[(𝐹 − E[𝑌 ∣⏟
 ⏟⏟⏟⏟ 𝐹⏟⏟
 ]) ]
 2
 Sharpness Reliability BS = E[(𝐹 − 𝑌 ) ]
 2
 The Sharpness component measures the average =⏟
 E[Var(𝐹
 ⏟⏟⏟⏟ ∣⏟
 𝑌⏟)] + ⏟⏟
 E[(E[𝐹
 ⏟⏟⏟⏟∣ 𝑌 ] −⏟𝑌⏟⏟
 ) ].
width of the predicted probabilities. It is defined Excess Correctness
as the mean squared difference between the pre-
dicted probabilities and the climatological probabil- Excess measures the average width of the pre-
ities. The climatological probabilities are the long- dicted probabilities, conditional on the actual out-
term average of the actual outcomes. The Sharpness comes, and it can be further decomposed into Re-
component is a measure of the informativeness of the finement & Discrimination components using the law
predictions. of total variance as
 The Reliability component measures the calibra-
tion of the predicted probabilities. It is defined as the
 Excess = E[Var(𝐹 ∣ 𝑌 )]
mean squared difference between the predicted prob-
abilities and the empirical frequencies of the actual = Var(𝐹
 ⏟) − ⏟Var(E[𝐹
 ⏟⏟⏟⏟ ∣⏟
 𝑌⏟]) .
outcomes. The empirical frequencies are the observed Refinement Discrimination
proportions of the actual outcomes. The Reliability This results in the Refinement, Discrimination,
component is a measure of the accuracy of the pre- Correctness decomposition of the Brier score [3, 7].
dictions. Refinement measures the variance of the probabili-
 Sharpness can be further decomposed into Resolu- ties. Discrimination measures the conditional vari-
tion & Uncertainty components using the law of total ance of the predicted probabilities given the actual
variance. outcomes. Correctness measures the squared differ-
 ence between the true outcomes and the predicted
 probabilities, conditional on the actual outcomes.
 Sharpness = E[Var(𝑌 ∣ 𝐹 )]
 = Var(𝑌
 ⏟) − ⏟Var(E[𝑌
 ⏟⏟⏟⏟ ∣⏟
 𝐹⏟])
 1.3 Yates Covariance Decomposition
 Uncertainty Resolution
 Starting from the bias–variance decomposition of the
 Uncertainty measures the variance of the climato- Brier score,
logical probabilities. Resolution measures the con-
ditional variance of the actual outcomes given the BS = ⏟⏟⏟⏟⏟
 Var(𝐹 − 𝑌 ) + (𝜇⏟⏟ 𝐹⏟− 𝜇𝑌⏟⏟ )2 ,
predicted probabilities. variance term squared bias term
 Together, Uncertainty, Resolution and Reliability
form the URR decomposition of the Brier score [3, where 𝜇𝐹 = E[𝐹 ] and 𝜇𝑌 = E[𝑌 ], one can fur-
5]. ther expand the variance term using Var(𝐹 − 𝑌 ) =
 Var(𝐹 ) + Var(𝑌 ) − 2 Cov(𝐹 , 𝑌 ) to obtain
1.2 Refinement, Discrimination, Cor-
 rectness BS = E[(𝐹 − 𝑌 )2 ]
 = Var(𝐹 − 𝑌 ) + (𝜇𝐹 − 𝜇𝑌 )2
An alternative decomposition of the Brier score can
be obtained by conditioning on the actual outcomes = 𝜎𝐹2 + 𝜎𝑌2 − 2𝜎𝐹 𝑌 + (𝜇𝐹 − 𝜇𝑌 )2 ,
 2
 where 𝜎𝐹2 = Var(𝐹 ) is the variance of the predicted score can be rearranged as
probabilities, 𝜎𝑌2 = Var(𝑌 ) is the variance of the
outcomes, 𝜎𝐹 𝑌 = Cov(𝐹 , 𝑌 ) is the covariance be- BS = (𝜎
 ⏟𝐹 − 𝜎𝑌
 ⏟⏟ ⏟⏟)2
tween the predicted probabilities and the outcomes, variance mismatch
and (𝜇𝐹 − 𝜇𝑌 )2 is the squared difference between the + 2(𝜎
 ⏟⏟𝐹 𝜎𝑌
 ⏟⏟⏟− 𝜎𝐹
 ⏟⏟𝑌)
mean predicted probability and the mean outcome, covariance deficit
often referred to as calibration-in-the-large. This is 2
 + (𝜇
 ⏟⏟ 𝐹 −
 ⏟ 𝜇𝑌
 ⏟)⏟ .
known as the Yates (covariance) decomposition of the
 calibration-in-the-large
Brier score [6].
 The optimal forecast is the one that minimizes the Proof. Expanding the first two terms of the right-
Brier score. However, it is not the case that min- hand side:
imizing each component individually minimizes the
Brier score itself. This can be seen in 𝜎𝐹2 , where the
 (𝜎𝐹 − 𝜎𝑌 )2 + 2(𝜎𝐹 𝜎𝑌 − 𝜎𝐹 𝑌 )
optimal forecast necessarily does not minimize this
term. This was previously noted by Yates himself, = 𝜎𝐹2 − 2𝜎𝐹 𝜎𝑌 + 𝜎𝑌2 + 2𝜎𝐹 𝜎𝑌 − 2𝜎𝐹 𝑌
who stated [6] that = 𝜎𝐹2 + 𝜎𝑌2 − 2𝜎𝐹 𝑌 ,
 which, together with the calibration-in-the-large
 the aim of the forecaster should be to min- term (𝜇𝐹 − 𝜇𝑌 )2 , recovers the original Yates decom-
 imize the variance of his or her forecasts, position.
 𝑆𝑓2 . There is an obvious qualification on
 this advice, however. The only way 𝑆𝑓2 can Corollary 1 (Non-negativity). All three terms in
 take on its absolute minimum possible value Theorem 1 are non-negative.
 of zero is when the forecaster offers con-
 stant forecasts. This strategy would make Proof. The first and third terms are squares and
 the covariance term zero, too. So the proper hence non-negative. For the second term, the
 objective of the forecaster should be to min- Cauchy–Schwarz inequality gives |𝜎𝐹 𝑌 | ≤ 𝜎𝐹 𝜎𝑌 , so
 imize 𝑆𝑓2 , given that he or she exercises his 2(𝜎𝐹 𝜎𝑌 − 𝜎𝐹 𝑌 ) ≥ 0.
 or her fundamental forecasting abilities, as
 represented by 𝑆𝑓𝑑 . Corollary 2 (Optimality conditions). BS = 0 if and
 only if 𝐹 = 𝑌 almost surely. Equivalently, each of
We believe that the conventional presentation of the the following conditions must hold simultaneously:
decomposition does not allow for an intuitive com-
munication of why this is the case, and we propose 1. 𝜎𝐹 = 𝜎𝑌 (variance matching),
a new decomposition arrangement that makes this
 2. 𝜎𝐹 𝑌 = 𝜎𝐹 𝜎𝑌 (perfect positive correlation),
more explicit.
 3. 𝜇𝐹 = 𝜇𝑌 (no bias).
 Proof. By Corollary 1, all three terms are non-
2 Alternative arrangement of negative, so BS = 0 if and only if each term vanishes
 the covariance decomposition individually.
 vanishes iff 𝜎
 Term 1 vanishes iff 𝜎𝐹 = 𝜎𝑌 ; term 2
 = 𝜎 𝜎 (i.e., 𝜌 = 1 when the
 𝐹𝑌 𝐹 𝑌 𝐹𝑌
 standard deviations are non-zero); term 3 vanishes
Theorem 1 (Alternative Yates Decomposition). iff 𝜇𝐹 = 𝜇𝑌 . These three conditions together are
The Yates covariance decomposition of the Brier equivalent to 𝐹 = 𝑌 almost surely.
 3
Remark. When 𝜎𝐹 and 𝜎𝑌 are both non-zero, the References
covariance deficit term can be rewritten in terms
of the Pearson correlation 𝜌𝐹 𝑌 = 𝜎𝐹 𝑌 /(𝜎𝐹 𝜎𝑌 ) = [1] T. Gneiting et al. “Strictly Proper Scoring Rules,
Corr(𝐹 , 𝑌 ) as Prediction, and Estimation”. In: Journal of the
 American Statistical Association 102.477 (2007),
 2(𝜎𝐹 𝜎𝑌 − 𝜎𝐹 𝑌 ) = 2𝜎𝐹 𝜎𝑌 (1 − 𝜌𝐹 𝑌 ), pp. 359–378. issn: 0162-1459. doi: 10 . 1198 /
 016214506000001437.
which is minimized when 𝜌𝐹 𝑌 = 1. This makes ex- [2] G. W. Brier. “Verification of Forecasts Expressed
plicit the point noted by Yates [6]: a forecaster should in Terms of Probability”. In: Monthly Weather
not simply minimize 𝜎𝐹2 , but rather match the vari- Review 78.1 (1950), pp. 1–3. doi: 10 . 1175 /
ability of forecasts to that of outcomes while main- 1520- 0493(1950)078<0001:VOFEIT> 2.0.CO;
taining maximal correlation. 2.
 Under the notation of Mitchell [3], this means that [3] K. Mitchell. “Score Decompositions in Forecast
under the optimality conditions, the Refinement term Verification”. Exeter: University of Exeter, 2019.
𝜎𝐹2 is equal to the Uncertainty term 𝜎𝑌2 , a well known HDL: 10871/40923. url: http://hdl.handle.
result. net/10871/40923.
 [4] F. Sanders. “On Subjective Probability Fore-
 casting”. In: Journal of Applied Meteorology
3 Conclusion and Climatology 2.2 (1963), pp. 191–201. issn:
 1520-0450. doi: 10 . 1175 / 1520 - 0450(1963 )
We have shown that a simple algebraic rearrange-
 002<0191:OSPF>2.0.CO;2.
ment of the Yates covariance decomposition yields
three independently non-negative terms, each with [5] A. H. Murphy. “A New Vector Partition of the
a clear interpretation: variance mismatch, covari- Probability Score”. In: Journal of Applied Mete-
ance deficit, and calibration-in-the-large. The non- orology and Climatology 12.4 (1973), pp. 595–
negativity of the covariance deficit follows directly 600. issn: 1520-0450. doi: 10 . 1175 / 1520 -
from the Cauchy–Schwarz inequality. This decompo- 0450(1973)012<0595:ANVPOT>2.0.CO;2.
sition makes the optimality conditions for the Brier
 [6] J. F. Yates. “External Correspondence: Decom-
score transparent: a perfect forecast must simultane-
 positions of the Mean Probability Score”. In: Or-
ously match the variance of outcomes, achieve per-
 ganizational Behavior and Human Performance
fect positive correlation (𝜌𝐹 𝑌 = 1), and exhibit no
 30.1 (1982), pp. 132–156. issn: 0030-5073. doi:
bias (𝜇𝐹 = 𝜇𝑌 ). In particular, the rearrangement
 10.1016/0030-5073(82)90237-9.
resolves the interpretive diﬀiculty noted by Yates [6]
 2
regarding the role of forecast variance 𝜎𝐹 in the origi- [7] A. H. Murphy et al. “A General Framework
nal decomposition, since the variance mismatch term for Forecast Verification”. In: Monthly Weather
(𝜎𝐹 − 𝜎𝑌 )2 is clearly minimized not by minimizing Review 115.7 (1987), pp. 1330–1338. issn:
the variability of forecasts but by matching it to that 1520-0493, 0027-0644. doi: 10 . 1175 / 1520 -
of outcomes. 0493(1987)115<1330:AGFFFV>2.0.CO;2.
 4
