---
title: 'When Calibration Rankings Reverse: Accuracy-Controlled Evaluation for Fair
  Comparison of LLMs'
id: when-calibration-rankings-reverse-accuracy-controlled-evaluation-for-fair-compar
tags:
- code-llm-confidence-positioning-d82d00
- f-measurement-framing
created: '2026-11-10T08:24:09.586024Z'
updated: '2026-11-10T08:27:08.278271Z'
source: https://arxiv.org/html/2606.30814
source_domain: arxiv.org
fetched_at: '2026-11-10T08:24:09.585351Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: arXiv 2606.30814. ACE accuracy-controlled calibration comparison; raw ECE
  gaps correlate with accuracy gaps (rho -0.670, n 40); 265 ranking reversals for
  small-vs-large and thinking-vs-non-thinking. Non-code QA benchmarks; verbalized,
  P(True), SC. Bears on F measurement validity, not code. Full text.
---

When Calibration Rankings Reverse: Accuracy-Controlled Evaluation for Fair Comparison of LLMs
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2606.30814v2 [cs.CL] 31 Aug 2026
When Calibration Rankings Reverse:
Accuracy-Controlled Evaluation for Fair Comparison of LLMs
Zhichao Yang
†
†
thanks:
Equal contribution. †Corresponding author.
Affiliation:
Fudan University
Caiqi Zhang
1
1
footnotemark:
1
Affiliation:
University of Cambridge
{zcyang25, rhyang21}@m.fudan.edu.cn, {cz391}@cam.ac.uk
Ruihan Yang
1
1
footnotemark:
1
Affiliation:
Fudan University
Chengzu Li
Affiliation:
University of Cambridge
{zcyang25, rhyang21}@m.fudan.edu.cn, {cz391}@cam.ac.uk
Nigel Collier
Affiliation:
University of Cambridge
{zcyang25, rhyang21}@m.fudan.edu.cn, {cz391}@cam.ac.uk
Deqing Yang
Abstract
Calibration evaluates whether a model’s confidence aligns with its empirical accuracy. Existing studies often compare the calibration of different large language models using global calibration metrics such as Expected Calibration Error and Brier Score.
We begin by showing, both theoretically and empirically, that such comparisons are confounded by differences in model accuracy.
For fairer cross-model comparison, we then propose ACE, an accuracy-controlled evaluation framework with three complementary views: Instance-Aligned, Distribution-Aligned, and Candidate-Aligned calibration. Across multiple benchmarks, model families, and confidence elicitation methods, we use ACE to study two practically important comparison axes, small versus large models and thinking versus non-thinking models. We find that many previously reported calibration advantages under raw global metrics weaken substantially after accuracy control. We also find that ranking reversal is frequent: models favored by raw metrics often cease to be favored once accuracy is controlled. Our results show that raw global calibration metrics are not robust for cross-model comparison, and that fair calibration comparison requires accuracy-aware evaluation.
1
1
1
Project page:
https://github.com/chaochaoxx/ACE
.
1
Introduction
Figure 1:
Accuracy differences strongly confound raw ECE comparison.
Each point is one dataset-level average for a model pair (
ρ
=
−
0.670
\rho\!=\!-0.670
,
n
=
40
n\!=\!40
, 95% CI
[
−
0.81
,
−
0.45
]
[-0.81,-0.45]
,
p
<
10
−
5
p<10^{-5}
; Appendix
A.2
). Larger accuracy gaps correspond to larger raw calibration gaps;
our accuracy-controlled views reduce this confound, most substantially under the Instance-Aligned (IA) and Distribution-Aligned (DA).
Large Language Models (LLMs) have achieved remarkable capabilities, making their reliable deployment in high-stakes domains a critical priority
(
Wang et al., 2023
;
Huang et al., 2024
;
Zhang et al., 2024
;
Zhang et al., 2025b
;
Yang et al., 2025b
;
Yang et al., 2025c
)
. In such settings, it is not enough for a model to achieve high average accuracy; it must also indicate how likely its prediction is to be correct
(
Zhang et al., 2026a
;
Zhang et al., 2026b
)
. This has made calibration, the alignment between a model’s confidence and its empirical correctness, a central topic in recent work on trustworthy language models
(
Xiong et al., 2024
;
Geng et al., 2024
;
Zhou et al., 2025
;
Zhang et al., 2025a
;
Hu et al., 2026
;
Li et al., 2025
)
. Global metrics such as Expected Calibration Error (ECE) and Brier Score (BS) are now widely used to quantify the calibration level of an LLM.
A common but underexamined assumption behind this practice is that
global calibration scores are directly comparable across models
. Under this view, if one model achieves lower ECE/BS than another, it is natural to conclude that the former is better calibrated
(
Zeng et al., 2025
;
Mei et al., 2025
;
Yoon et al., 2025
;
Lacombe et al., 2025
)
. However, we argue that this interpretation becomes problematic when the models being compared differ substantially in task accuracy. A model with higher accuracy can achieve a better global calibration score for two different reasons: it may be truly better calibrated, or it may simply make fewer mistakes. For example, if two models both assign confidence 1.0 to every answer, the more accurate one will automatically score better on ECE/BS, despite identical confidence behavior. In Section
3
, we first show that global calibration metrics are confounded by model accuracy, and therefore do not reflect calibration quality alone. This raises a basic but important question:
when two models operate at different accuracy levels, are their calibration scores really being compared on equal footing?
In this work, we argue that naïve cross-model comparisons based on raw global calibration metrics can be misleading.
When models differ greatly in accuracy, raw global metrics can systematically favor the stronger model even when the underlying confidence behavior is not correspondingly better. More importantly, this confound can produce what we term
ranking reversal
: a model that appears better calibrated under raw global metrics can become
less
calibrated once accuracy is controlled. We argue that ranking reversal is a particularly revealing diagnostic for calibration evaluation, because it makes the failure of naïve cross-model comparison directly observable. Rather than merely shifting the magnitude of a calibration gap, controlling for accuracy can overturn the conclusion about which model is better calibrated.
We therefore propose
ACE
(
A
ccuracy-
C
ontrolled
E
valuation), a framework for fairer cross-model calibration analysis. ACE compares models under matched or partially matched correctness conditions before drawing calibration conclusions. It includes three complementary views. First,
Instance-Aligned
(IA) calibration compares models only on examples where they share the same outcome, providing strict instance-level control. Second,
Distribution-Aligned
(DA) calibration matches the aggregate outcome composition of the compared models, enabling a broader distribution-level comparison. Third,
Candidate-Aligned
(CA) calibration extends the same principle to evaluative settings with a shared answer space, where models judge a common pool of candidate answers. Together, these three views disentangle calibration quality from task accuracy, which raw global metrics conflate.
Using ACE across multiple benchmarks, model families, calibration metrics, and confidence elicitation methods, we find that many raw calibration conclusions are substantially less stable than they appear. Apparent calibration advantages often shrink once accuracy is controlled, and ranking reversal occurs frequently in both scale-based and thinking-versus-non-thinking model comparisons. These findings do not imply that calibration metrics such as ECE or BS are uninformative. Rather, they show that
raw
global calibration scores are not always apples-to-apples across models with different accuracies. When the goal is fair cross-model comparison, accuracy control is not a minor refinement; it can change the conclusion itself.
•
We show that raw comparisons of calibration across models can be misleading when models differ in accuracy, and identify a key
ranking reversal
phenomenon.
•
We propose
ACE
, an accuracy-controlled evaluation framework with three complementary views for fairer comparison.
•
Across multiple datasets, model families, and confidence elicitation methods, we show that many apparent calibration advantages weaken substantially under ACE, and that ranking reversals are common enough to materially change model-level conclusions.
2
Related Work
Calibration Metrics and Calibration Methods.
Existing work studies calibration using both visualization-based and scalar metrics. Common examples include the
reliability diagram
and
Expected Calibration Error
(ECE), which summarize the gap between confidence and empirical accuracy across bins
(
Niculescu-Mizil and Caruana, 2005
;
Naeini et al., 2015
)
, as well as probabilistic scoring rules such as the
Brier Score
and
negative log-likelihood
(NLL)
(
Brier, 1950
;
Lakshminarayanan et al., 2017
)
. Prior work has also examined the sensitivity of ECE-style analysis to evaluation design, including equal-mass, adaptive, and class-conditional variants
(
Nguyen and O’Connor, 2015
;
Nixon et al., 2019
)
. To improve calibration, widely used post-hoc methods include
temperature scaling
,
Platt scaling
, and
isotonic regression
(
Platt and others, 1999
;
Zadrozny and Elkan, 2002
;
Guo et al., 2017
)
, while training-time approaches such as
label smoothing
and
deep ensembles
have also been explored
(
Pereyra et al., 2017
;
Lakshminarayanan et al., 2017
)
. These methods are complementary to our work: rather than proposing a new way to recalibrate model confidences, we study whether calibration comparisons themselves are fair when models differ in task accuracy.
Fairness in Calibration Comparison.
Recent work has shown that calibration evaluation itself can be sensitive to how it is defined and aggregated
(
Nixon et al., 2019
;
Vaicenavicius et al., 2019
)
. In particular, prior studies have shown that calibration conclusions may change with the choice of metric, binning scheme, and aggregation rule, and that standard ECE-style evaluation may reward confidence assignments that reduce aggregate error without improving the separation between correct and incorrect predictions
(
Si et al., 2022
)
. Other work further suggests that calibration scores should not be interpreted independently of model accuracy, since more accurate models can obtain systematically more favorable scores under standard global metrics
(
Minderer et al., 2021
;
Chidambaram and Ge, 2024
)
. Recent proposals such as
CKCE
highlight that relative calibration comparison can be distorted by differences in predictive marginals
(
Moskvichev and Sejdinovic, 2025
)
. However, these studies overlook a critical question: when models differ in accuracy, how can we fairly compare their calibration to ensure results reflect genuine confidence quality rather than mere task success? Our work addresses this gap by making accuracy the explicit control variable in cross-model calibration comparison and by showing that such control can change not only calibration gaps but also model rankings.
3
Background and Motivation
Reliable confidence estimation is central to the safe deployment of LLMs. A standard lens for studying this property is
calibration
, which asks whether confidence estimates match empirical correctness probabilities. In practice, calibration is often summarized by global metrics such as Expected Calibration Error (ECE) and Brier Score (BS). However, when models differ substantially in task accuracy, such comparisons become problematic. This section introduces the notation and shows, analytically and empirically, why accuracy confounds cross-model calibration comparisons, motivating our accuracy-controlled evaluation framework.
Notation and Standard Metrics.
Let
D
=
{
(
x
i
,
y
i
)
}
i
=
1
N
D=\{(x_{i},y_{i})\}_{i=1}^{N}
be an evaluation set, where
x
i
x_{i}
is an input and
y
i
y_{i}
is its gold label. Given a model
M
M
, let
y
^
i
\hat{y}_{i}
denote its prediction and
c
i
∈
[
0
,
1
]
c_{i}\in[0,1]
the confidence assigned to that prediction.
We define the correctness indicator
z
i
=
𝟏
[
y
^
i
=
y
i
]
z_{i}=\mathbf{1}[\hat{y}_{i}=y_{i}]
,
and the empirical accuracy
Acc
⁡
(
M
)
=
1
N
​
∑
i
=
1
N
z
i
.
\mathrm{Acc}(M)=\frac{1}{N}\sum_{i=1}^{N}z_{i}.
To measure calibration, we consider two standard global metrics.
First, ECE partitions the confidence range into bins
{
I
b
}
b
=
1
B
\{I_{b}\}_{b=1}^{B}
and computes
ECE
⁡
(
M
)
=
∑
b
=
1
B
|
S
b
|
N
​
|
acc
⁡
(
S
b
)
−
conf
⁡
(
S
b
)
|
,
\mathrm{ECE}(M)=\sum_{b=1}^{B}\frac{|S_{b}|}{N}\left|\mathrm{acc}(S_{b})-\mathrm{conf}(S_{b})\right|,
where
S
b
=
{
i
:
c
i
∈
I
b
}
S_{b}\!=\!\{i\!:\!c_{i}\in I_{b}\}
,
acc
⁡
(
S
b
)
=
1
|
S
b
|
​
∑
i
∈
S
b
z
i
\mathrm{acc}(S_{b})=\frac{1}{|S_{b}|}\sum_{i\in S_{b}}z_{i}
, and
conf
⁡
(
S
b
)
=
1
|
S
b
|
​
∑
i
∈
S
b
c
i
\mathrm{conf}(S_{b})=\frac{1}{|S_{b}|}\sum_{i\in S_{b}}c_{i}
.
Second, the Brier Score is
BS
⁡
(
M
)
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
\mathrm{BS}(M)=\frac{1}{N}\sum_{i=1}^{N}(c_{i}-z_{i})^{2}.
Both metrics are meaningful summaries of confidence quality for a fixed model on a fixed prediction set. Our concern is different:
directly comparing these global scores across models with different accuracies can be severely confounded
.
Why Accuracy Is a Confounder.
The core problem is that global calibration metrics depend not only on how confidence is distributed, but also on the proportion of correct versus incorrect predictions. When a stronger model answers more questions correctly, its global ECE or BS can improve mechanically, even if its confidence behavior is not intrinsically better.
Intuitively, global metrics average over correct and incorrect predictions, so changing their mixture can change the score even when confidence behavior is fixed. This can be seen in a simple toy (with more rigorous discussion in Appendix
A.1
) setting where all predictions receive the same confidence
q
∈
[
0
,
1
]
q\in[0,1]
. Let
a
=
Acc
⁡
(
M
)
a=\mathrm{Acc}(M)
. Then
ECE
⁡
(
M
)
\displaystyle\mathrm{ECE}(M)
=
|
a
−
q
|
,
\displaystyle=|a-q|,
BS
⁡
(
M
)
\displaystyle\mathrm{BS}(M)
=
a
​
(
1
−
q
)
2
+
(
1
−
a
)
​
q
2
\displaystyle=a(1-q)^{2}+(1-a)q^{2}
=
q
2
+
a
⁡
(
1
−
2
​
q
)
.
\displaystyle=q^{2}+a(1-2q).
Thus, BS depends linearly on accuracy. In the practically relevant high-confidence regime
q
>
0.5
q>0.5
,
BS
⁡
(
M
)
\mathrm{BS}(M)
decreases as
a
a
increases. Likewise, ECE is piecewise linear in
a
a
; under the common overconfident regime
a
≤
q
a\leq q
, it simplifies to
ECE
⁡
(
M
)
=
q
−
a
,
\mathrm{ECE}(M)=q-a,
which also decreases as accuracy increases. Therefore, even when two models exhibit the same nominal confidence level, the more accurate one can obtain a better global calibration score simply because it has more correct predictions.
Empirical Evidence and Motivation.
This controlled example motivates an empirical diagnostic. As shown in the “Raw” panel of Figure
1
, experiments across mainstream LLM families and benchmark tasks reveal a strong negative correlation (
ρ
=
−
0.670
\rho=-0.670
) between global calibration scores and task accuracy.
Models with higher accuracy mechanically appear better calibrated under raw ECE, even when they remain highly overconfident. This pattern validates our concern: a substantial part of the reported “calibration advantage” of stronger models may simply reflect outcome composition rather than genuinely superior uncertainty estimation. This empirical trend motivates the central question of our paper:
how should we compare calibration fairly when models have different cognitive capabilities?
4
ACE: Accuracy-Controlled Evaluation
We introduce
ACE
(
A
ccuracy-
C
ontrolled
E
valuation), a framework for fairer cross-model calibration comparison. The key idea is simple: when two models differ in task accuracy, their raw global calibration scores are not directly comparable because they are computed over prediction sets with different outcome compositions.
ACE
addresses this by constructing comparison protocols in which predictive success is explicitly controlled before calibration is measured. These views are intended to be read jointly rather than as interchangeable metrics: agreement indicates a stable conclusion, while disagreement identifies the relevant alignment choice. The framework contains two views for
generative calibration
, where models score their own answers, and one complementary view for
evaluative calibration
, where they judge a shared answer space.
Setup.
Consider two models,
M
A
M_{A}
and
M
B
M_{B}
, evaluated on the same dataset
D
=
{
(
x
i
,
y
i
)
}
i
=
1
N
D=\{(x_{i},y_{i})\}_{i=1}^{N}
.
For each example
x
i
x_{i}
, model
M
m
M_{m}
produces a prediction
y
^
i
(
m
)
\hat{y}_{i}^{(m)}
, a confidence score
c
i
(
m
)
∈
[
0
,
1
]
c_{i}^{(m)}\in[0,1]
, and a correctness indicator
z
i
(
m
)
=
[
y
^
i
(
m
)
=
y
i
]
,
m
∈
{
A
,
B
}
.
z_{i}^{(m)}=\mathbf{1}\!\left[\hat{y}_{i}^{(m)}=y_{i}\right],\quad m\in\{A,B\}.
Let
Acc
⁡
(
M
m
)
=
1
N
​
∑
i
=
1
N
z
i
(
m
)
\mathrm{Acc}(M_{m})=\frac{1}{N}\sum_{i=1}^{N}z_{i}^{(m)}
denote the model’s accuracy. We focus on binary correctness here; Appendix
E.7
extends the formulation to graded correctness. A naive evaluation would directly compare global scores like
ECE
⁡
(
M
A
)
\mathrm{ECE}(M_{A})
and
ECE
⁡
(
M
B
)
\mathrm{ECE}(M_{B})
over the full dataset
D
D
.
However, as established in Section
3
, such comparisons are inherently confounded when
Acc
⁡
(
M
A
)
≠
Acc
⁡
(
M
B
)
\mathrm{Acc}(M_{A})\neq\mathrm{Acc}(M_{B})
. To address this,
ACE
evaluates cross-model calibration strictly under controlled accuracy conditions.
4.1
Instance-Aligned (IA) Calibration
Our first view enforces
instance-level alignment
.
We compare two models only on examples where they have the same outcome,
i
.
e
., both are correct or both are wrong. Formally, we define
D
both
​
-
​
right
\displaystyle D_{\mathrm{both\mbox{-}right}}
=
{
i
:
z
i
(
A
)
=
1
∧
z
i
(
B
)
=
1
}
,
\displaystyle=\left\{i:z_{i}^{(A)}=1\land z_{i}^{(B)}=1\right\},
D
both
​
-
​
wrong
\displaystyle D_{\mathrm{both\mbox{-}wrong}}
=
{
i
:
z
i
(
A
)
=
0
∧
z
i
(
B
)
=
0
}
,
\displaystyle=\left\{i:z_{i}^{(A)}=0\land z_{i}^{(B)}=0\right\},
and
D
IA
=
D
both
​
-
​
right
∪
D
both
​
-
​
wrong
D_{\mathrm{IA}}=D_{\mathrm{both\mbox{-}right}}\cup D_{\mathrm{both\mbox{-}wrong}}
.
By construction, the two models have identical empirical accuracy on
D
IA
D_{\mathrm{IA}}
:
Acc
D
IA
​
(
M
A
)
=
Acc
D
IA
​
(
M
B
)
=
|
D
both
​
-
​
right
|
|
D
IA
|
.
\mathrm{Acc}_{D_{\mathrm{IA}}}(M_{A})=\mathrm{Acc}_{D_{\mathrm{IA}}}(M_{B})=\frac{|D_{\mathrm{both\mbox{-}right}}|}{|D_{\mathrm{IA}}|}.
This makes
D
IA
D_{\text{IA}}
a particularly clean comparison set: because correctness is aligned
instance by instance
, calibration differences can be interpreted more directly as differences in confidence assignment rather than differences in task success. IA retains substantial coverage in our experiments (median 78.0%, IQR [66.3%, 82.2%], min 55.2%; Appendix
E.4
).
We then compute calibration metrics (
e
.
g
., ECE and BS) on
D
IA
D_{\mathrm{IA}}
. A useful feature of IA is its decomposition.
D
both
​
-
​
right
D_{\mathrm{both\mbox{-}right}}
captures shared competence, while
D
both
​
-
​
wrong
D_{\mathrm{both\mbox{-}wrong}}
captures shared blind spots.
The latter is especially informative: if a stronger model still assigns systematically higher confidence on
D
both-wrong
D_{\text{both-wrong}}
, then its apparent global calibration advantage may partly mask a more severe form of overconfidence on questions that neither model actually understands. Unlike comparing calibration separately on each model’s correct and incorrect predictions, this decomposition holds both the outcome and the evaluated instances fixed across models. This instance-aligned analysis therefore reveals
where
calibration differences come from, not merely whether one global score is lower than another.
4.2
Distribution-Aligned (DA) Calibration
Our second view enforces
distribution-level alignment
. Instead of matching models instance by instance, DA matches the overall outcome composition so that calibration is compared under a common effective accuracy level. Concretely, rather than requiring the two models to agree on the same instances, DA only requires them to be compared under the same aggregate proportion of correct and incorrect predictions.
A natural way to achieve this is to rebalance one model’s predictions to match the empirical accuracy of the other. One implementation is resampling, which selectively discards observations until the target outcome composition is reached. While simple, this approach introduces sampling variance and reduces effective sample size. We therefore consider a more rigorous alternative that retains all
observations:
Distribution-Aligned
(DA). DA uses importance weighting, a technique widely used in causal inference to correct for confounded comparisons
(
Rosenbaum and Rubin, 1983
)
, to reweight each
prediction so that the weighted outcome composition matches a target accuracy (see Appendix
B
for a detailed justification).
Let
a
A
=
Acc
⁡
(
M
A
)
a_{A}=\mathrm{Acc}(M_{A})
,
a
B
=
Acc
⁡
(
M
B
)
a_{B}=\mathrm{Acc}(M_{B})
with
a
A
>
a
B
a_{A}>a_{B}
.
To evaluate
M
A
M_{A}
at the accuracy level of
M
B
M_{B}
, we define
w
i
(
A
)
=
{
a
B
/
a
A
if
​
z
i
(
A
)
=
1
(
1
−
a
B
)
/
(
1
−
a
A
)
if
​
z
i
(
A
)
=
0
,
w_{i}^{(A)}=\begin{cases}a_{B}/a_{A}&\text{if }z_{i}^{(A)}=1\\[4.0pt]
(1-a_{B})/(1-a_{A})&\text{if }z_{i}^{(A)}=0\end{cases},
which satisfies
∑
i
w
i
(
A
)
​
z
i
(
A
)
/
∑
i
w
i
(
A
)
=
a
B
\sum_{i}w_{i}^{(A)}z_{i}^{(A)}\big/\sum_{i}w_{i}^{(A)}\!=\!a_{B}
. Thus, the weighted correctness composition of
M
A
M_{A}
matches the target accuracy
a
B
a_{B}
. The resulting DA calibration metrics are computed as:
DA
​
-
​
BS
a
A
→
B
\displaystyle\mathrm{DA\mbox{-}BS}_{a_{A\to B}}
=
1
W
​
∑
i
w
i
(
A
)
​
(
c
i
(
A
)
−
z
i
(
A
)
)
2
,
\displaystyle=\frac{1}{W}\sum_{i}w_{i}^{(A)}\left(c_{i}^{(A)}-z_{i}^{(A)}\right)^{2},
DA
​
-
​
ECE
a
A
→
B
\displaystyle\mathrm{DA\mbox{-}ECE}_{a_{A\to B}}
=
∑
b
=
1
B
W
b
W
​
|
acc
w
​
(
S
b
)
−
conf
w
​
(
S
b
)
|
,
\displaystyle=\sum_{b=1}^{B}\frac{W_{b}}{W}\left|\mathrm{acc}_{w}(S_{b})\!-\!\mathrm{conf}_{w}(S_{b})\right|,
where
W
=
∑
i
w
i
(
A
)
W\!=\!\sum_{i}w_{i}^{(A)}
is the total weight,
W
b
=
∑
i
∈
S
b
w
i
(
A
)
W_{b}=\sum_{i\in S_{b}}w_{i}^{(A)}
is the bin weight, and
acc
w
\mathrm{acc}_{w}
and
conf
w
\mathrm{conf}_{w}
are weighted bin-level accuracy and confidence.
DA trades the strictness of IA for broader coverage. Rather than enforcing agreement on the same individual instances, it aligns only the overall distribution of correct and incorrect outcomes, allowing comparison on a larger effective sample. This makes DA a useful test of whether an apparent calibration advantage persists once differences in aggregate outcome composition are removed.
4.3
Candidate-Aligned (CA) Calibration
The two views above concern
generative calibration
: each model generates its own answer and reports confidence on that answer. Our third view removes this asymmetry by aligning the
candidate answer space
.
For each input
x
i
x_{i}
, let
s
i
(
A
)
s_{i}^{(A)}
and
s
i
(
B
)
s_{i}^{(B)}
be the answers generated by
M
A
M_{A}
and
M
B
M_{B}
, and define the shared candidate pool
U
i
=
{
s
i
(
A
)
,
s
i
(
B
)
}
U_{i}=\{s_{i}^{(A)},\,s_{i}^{(B)}\}
.
More generally,
U
i
U_{i}
can include any set of candidate answers under consideration. Each model then evaluates every candidate in the same pool. Let
e
i
(
m
)
​
(
s
)
∈
[
0
,
1
]
e_{i}^{(m)}(s)\in[0,1]
denote model
M
m
M_{m}
’s confidence that candidate
s
∈
U
i
s\in U_{i}
is correct, and let
y
i
​
(
s
)
∈
{
0
,
1
}
y_{i}(s)\in\{0,1\}
be the ground-truth correctness label of candidate
s
s
.
CA is then computed at the
candidate level
: each pair
(
x
i
,
s
)
(x_{i},s)
is treated as one evaluation instance, and calibration compares
e
i
(
m
)
​
(
s
)
e_{i}^{(m)}(s)
against
y
i
​
(
s
)
y_{i}(s)
over all
i
i
and all
s
∈
U
i
s\in U_{i}
. For example,
CA
​
-
​
BS
​
(
M
m
)
=
1
∑
i
|
U
i
|
​
∑
i
∑
s
∈
U
i
(
e
i
(
m
)
​
(
s
)
−
y
i
​
(
s
)
)
2
\mathrm{CA\mbox{-}BS}(M_{m})\!=\!\frac{1}{\sum_{i}|U_{i}|}\!\sum_{i}\!\sum_{s\in U_{i}}\left(e_{i}^{(m)}(s)\!-\!y_{i}(s)\right)^{2}
with CA-ECE defined analogously by binning the values
e
i
(
m
)
​
(
s
)
e_{i}^{(m)}(s)
across all candidate-level instances.
As both models score the same candidates, CA controls for differences in generation space and isolates calibration in evaluation mode. It also exposes
self-preference bias
: a model may assign higher confidence to its own answer than to a competing answer, even when the competing answer is better supported.
5
Experiments
5.1
Experiment Setup
Models.
We study models along two comparison axes:
small vs. large
and
thinking vs. non-thinking
. For scale-based comparison, we evaluate Qwen2.5 (7B and 72B)
(
Qwen et al., 2025
)
, LLaMA 3.1 (8B and 70B)
(
Grattafiori et al., 2024
)
, and GPT-OSS (20B and 120B)
(
OpenAI et al., 2025
)
. For reasoning-mode comparison, we evaluate Qwen3 (8B and 32B)
(
Yang et al., 2025a
)
and GPT-OSS (20B and 120B) under different reasoning settings
(
OpenAI et al., 2025
)
. These comparison axes are motivated by prior findings that larger models often produce better calibrated confidence estimates than smaller ones, although the gains can be task-dependent
(
Xiong et al., 2024
;
Fang et al., 2025
)
. Prior work also suggests that reasoning-enabled models often calibrate better than non-reasoning models on reasoning-intensive tasks, while the picture is more mixed on factual knowledge tasks
(
Yoon et al., 2025
;
Zeng et al., 2025
)
. Additional inference settings and answer-generation prompts are provided in Appendix
C
and Appendix
D.1
.
Datasets.
We evaluate on five datasets spanning two categories:
knowledge-based
and
reasoning-based
tasks. The knowledge-based datasets are FreshQA and TriviaQA
(
Vu et al., 2023
;
Joshi et al., 2017
)
, both in an open-ended factual QA format. The reasoning-based datasets are GPQA Diamond, LiveBench, and MMLU-Pro
(
Rein et al., 2023
;
White et al., 2025
;
Wang et al., 2024
)
, which cover expert-level multiple-choice reasoning, general reasoning, and academic problem solving, respectively. The answer formats include both open-ended and multiple-choice settings. Additional dataset details are provided in Appendix
D.2
.
Confidence Elicitation Methods.
We consider three representative confidence elicitation methods:
verbalized confidence
(
Tian et al., 2023
)
,
P(True)
(
Kadavath et al., 2022
)
, and
self-consistency
(
Wang et al., 2022
;
Manakul et al., 2023
)
. Additional prompting templates and implementation details are provided in Appendix
D.3
.
5.2
Main Results
Figure 2:
Calibration gap between small and large models within the same family, plotted before (
x
-axis,
Raw
) and after accuracy alignment (
y
-axis). Each point represents one (dataset, calibration metric, confidence elicitation method) combination. Points in
Quadrants II and IV
(
reversal
) indicate cases where the raw and alignment-based rankings disagree: the model favored by raw ECE/BS is no longer favored after accuracy control.
Figure 3:
Calibration gap between non-thinking and thinking models, using the same setup as Figure
2
.
Ranking reversal occurs frequently
, and this pattern is robust across metrics and confidence elicitation methods.
We define a
ranking reversal
as a case where the model that appears better calibrated under the raw comparison becomes less calibrated after ACE. In Figures 2 and 3, such reversals correspond to points falling in the second and fourth quadrants, where the raw and ACE-based comparisons disagree in sign. We widely observe ranking reversals under both ECE and BS, and across confidence estimates. Across the 265 reversals in the original
estimates, the median probability that the Raw and aligned gaps retain opposite signs under paired bootstrap resampling is 91.9%
(Appendix
E.6
). This means that calibration conclusions drawn from raw global metrics can be misleading when the compared models differ in accuracy.
For scale-based comparisons, the calibration advantage of larger models weakens markedly after ACE.
Figure 2 shows that, when comparing Qwen2.5, LLaMA 3.1, and GPT-OSS model pairs, reversal rates are common across all three confidence elicitation methods and both metrics. Depending on the setting, the reversal rate ranges from 0% to 53%, with the strongest effects typically appearing under Distribution-Alignment and Instance-Alignment. For example, under verbalized confidence, the reversal rate reaches 53% for ECE under DA, and under
P
⁡
(
true
)
P(\mathrm{true})
it reaches 53% in some settings. These results indicate that part of the apparent calibration advantage of larger models under raw global metrics is attributable to their higher task accuracy rather than to uniformly better confidence quality.
For thinking-versus-non-thinking comparisons, controlled evaluation also overturns many raw rankings.
Figure 3 shows the same qualitative pattern when comparing thinking and non-thinking modes within the same model family. Here, reversal remains frequent after accuracy alignment, and in some settings becomes even more pronounced: for instance, under self-consistency, the reversal rate reaches 65% when Candidate-Aligned, while several Distribution-Aligned settings fall in the 30%–60% range. Even under verbalized confidence, where CA can be relatively conservative, DA and IA still produce substantial reversal rates such as 60% and 50%. This suggests that some of the raw calibration gains attributed to thinking are mediated by improved answer accuracy, rather than reflecting a purely metacognitive improvement in confidence estimation.
Taken together, the results show that raw global calibration scores are often not apples-to-apples across models with different accuracies.
Our main empirical finding is therefore not that larger or thinking models are poorly calibrated, but that raw global calibration metrics can confound confidence quality with outcome composition. Once accuracy is explicitly controlled, several widely reported calibration advantages shrink substantially, and in many cases the ranking itself changes. These findings support the use of ACE-style evaluation as a standard companion to raw calibration reporting when the goal is fair cross-model comparison.
6
Analysis
Figure 4:
Overall reversal-combination distribution relative to the raw ECE winner.
The figure highlights that Dist.-Aligned and Inst.-Aligned agree in 79.2% of cases, whereas Cand.-Aligned more often behaves as a separate comparison axis.
Distribution-Aligned (DA) and Instance-Aligned (IA) usually overturn raw winners together, while Candidate-Aligned (CA) more often acts alone.
As shown in Figure
4
, the dominant
reversal structure is not arbitrary: across all 120 cases, the three most
common patterns are no reversal (28.3%), CA-only reversal
(20.8%), and joint DA+IA reversal (20.0%),
which together account for 69.2% of all comparisons. More importantly,
DA and IA share the same reversal status in 79.2% of cases, whereas
CA more often departs from them as a separate comparison axis. This suggests
that DA and IA often capture related corrections to the raw ranking, even
though the structure
is not fully binary, since all-three reversal still occurs in 10.0% of cases.
The same asymmetry also appears in the knowledge-versus-reasoning split:
across method-level reversal rates, DA and IA generally move in more similar
directions, whereas CA is more likely to diverge.
This asymmetry is also
consistent with the definitions of the three views. DA and IA both still
evaluate confidence on each model’s own answers and mainly differ in how they
align accuracy, whereas CA changes the candidate answer pool itself and
therefore more easily yields a separate ranking.
The source of reversal depends strongly on the confidence method.
Table
1
shows that the three confidence methods do not share a single reversal signature. Verbalized
confidence is dominated by joint DA+IA
reversal (35.0%), suggesting that its raw ranking is especially sensitive to
distribution-aligned and instance-aligned comparison. SC follows a different
pattern: CA-only reversal is the most common outcome (35.0%), indicating substantially greater sensitivity to candidate-pool alignment than to DA or IA comparison. P(True), in contrast, shows the most diffuse profile, with substantial mass on both DA-only (22.5%) and CA-only (20.0%) reversals rather than a single dominant pattern. The key point is not merely that reversal frequencies differ, but that different methods are destabilized by
different kinds of alignment.
Method
Exclusive RR (%)
NRR
(%)
IA
DA
CA
Verbalized
7.5
2.5
7.5
27.5
P(True)
2.5
22.5
20.0
30.0
SC
10.0
2.5
35.0
27.5
Table 1:
Method-level ranking reversal rates (RR). IA, DA, and CA columns report the
fraction of cases where
exclusively
that view overturns the
Raw ECE winner. NRR (no-reversal rate) is the fraction of cases where
no view overturns the Raw ECE winner.
Dataset structure determines which kind of reversal becomes dominant.
As illustrated in Table
2
, reversal
consistency is also highly dataset-dependent. MMLU-Pro exhibits the highest
no-reversal rate (50.0%), indicating comparatively stable raw rankings. By
contrast, FreshQA and TriviaQA are more often dominated by CA
reversals (45.8% and 33.3%, respectively), suggesting that candidate-pool
alignment plays a larger role in open-ended knowledge QA. GPQA
Diamond has the highest all-three-reversal rate (16.7%), meaning that its raw
winner is more likely to be overturned jointly by all three aligned views.
LiveBench Reasoning shows the most diffuse pattern, with mass spread across
several reversal types rather than concentrated in a single dominant
signature. Taken together, these dataset-level differences indicate that the
stability of raw ECE ranking depends not only on the confidence method, but
also on task format and evaluation structure.
Dataset
Exclusive RR (%)
NRR
(%)
IA
DA
CA
FreshQA
8.3
4.2
45.8
25.0
GPQA
0.0
16.7
12.5
25.0
LiveBench
16.7
12.5
8.3
20.8
TriviaQA
8.3
8.3
33.3
20.8
MMLU-Pro
0.0
4.2
4.2
50.0
Table 2:
Dataset-level ranking reversal rates (RR). IA, DA, and CA columns report the
fraction of cases where
exclusively
that view overturns the
Raw ECE winner.
Additional analyses on reversal patterns and confidence distributions are in Appendix
E
.
Practical Recommendations.
We recommend using DA as the default reporting metric, as it retains the full sample and agrees with IA in 79.2% of cases (Figure
4
). IA should serve as a corroborating check; their agreement indicates a stable conclusion. Finally, treat CA as a diagnostic tool: if CA diverges from DA and IA, the ranking is likely sensitive to candidate-pool alignment rather than indicating a robust reversal.
7
Conclusion
We introduced
ACE
, an accuracy-controlled evaluation framework for fairer calibration comparison in large language models. Our analysis shows that standard global calibration metrics can be substantially confounded by differences in task accuracy, making raw cross-model comparisons misleading. To address this,
ACE
provides three complementary views that compare models under matched or partially matched correctness conditions.
Across model families, datasets, and confidence elicitation methods, we find that many apparent calibration advantages weaken once accuracy is controlled, and that ranking reversals are common, suggesting that standard evaluation can overstate the metacognitive advantage of stronger models.
Our results highlight the importance of accuracy-aware calibration analysis and position
ACE
as a useful companion to conventional calibration reporting for more reliable assessment of LLM confidence quality.
Limitations
Our study also has several limitations that suggest directions for future work. First, our experiments focus on open-source models, which allow controlled and reproducible evaluation across model families, but further validation on proprietary systems would be valuable to assess how broadly the observed trends extend. Second, while
ACE
provides three complementary views for accuracy-controlled comparison, each view has its own tradeoff: IA offers strict instance-level control but depends on shared-outcome coverage, DA retains the full sample through reweighting but relies on distributional alignment, and CA exposes candidate-pool and self-preference effects but should be read as diagnostic rather than as a replacement for own-output calibration. Accordingly, we interpret the three views jointly rather than treating any single view as a complete solution. Third,
ACE
is intended as a diagnostic framework, and connecting its accuracy-controlled rankings to downstream applications such as selective prediction, abstention, or routing remains future work. Finally, our main experiments use a binary correctness variable,
z
i
∈
{
0
,
1
}
z_{i}\in\{0,1\}
, which is a natural fit for multiple-choice and exact-match benchmarks but less directly applicable to tasks where performance is graded with partial credit or other continuous measures.
In the Appendix, we extend the framework to graded correctness and evaluate this extension on two datasets. Broader evaluation in such settings remains an important direction for future research.
Ethics Statement
Our research adheres to strict ethical guidelines. We verified the licenses of all software and datasets used in this study to ensure full compliance with their terms. No privacy concerns have been identified. We have conducted a thorough assessment of the project and do not anticipate any further risks. We only use LLMs for grammar checking during the paper writing.
Acknowledgments
This work was supported by the Chinese NSF General Program (No. 62572129).
References
Brier (1950)
G. W. Brier
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
§2
.
Chidambaram and Ge (2024)
M. Chidambaram and R. Ge
Reassessing how to compare and improve the calibration of machine learning models
.
arXiv preprint arXiv:2406.04068
.
Cited by:
§2
.
Fang
et al.
(2025)
K. Fang, T. Zhao, and L. Cheng
Credence calibration game? calibrating large language models through structured play
.
arXiv preprint arXiv:2508.14390
.
Cited by:
§5.1
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
pp. 6577–6595
.
Cited by:
§1
.
Grattafiori
et al.
(2024)
A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan, A. Yang, A. Fan, A. Goyal, A. Hartshorn, A. Yang, A. Mitra, A. Sravankumar, A. Korenev, A. Hinsvark, A. Rao, A. Zhang, A. Rodriguez, A. Gregerson, A. Spataru, B. Roziere, B. Biron, B. Tang, B. Chern, C. Caucheteux, C. Nayak, C. Bi, C. Marra, C. McConnell, C. Keller, C. Touret, C. Wu, C. Wong, C. C. Ferrer, C. Nikolaidis, D. Allonsius, D. Song, D. Pintz, D. Livshits, D. Wyatt, D. Esiobu, D. Choudhary, D. Mahajan, D. Garcia-Olano, D. Perino, D. Hupkes, E. Lakomkin, E. AlBadawy, E. Lobanova, E. Dinan, E. M. Smith, F. Radenovic, F. Guzmán, F. Zhang, G. Synnaeve, G. Lee, G. L. Anderson, G. Thattai, G. Nail, G. Mialon, G. Pang, G. Cucurell, H. Nguyen, H. Korevaar, H. Xu, H. Touvron, I. Zarov, I. A. Ibarra, I. Kloumann, I. Misra, I. Evtimov, J. Zhang, J. Copet, J. Lee, J. Geffert, J. Vranes, J. Park, J. Mahadeokar, J. Shah, J. van der Linde, J. Billock, J. Hong, J. Lee, J. Fu, J. Chi, J. Huang, J. Liu, J. Wang, J. Yu, J. Bitton, J. Spisak, J. Park, J. Rocca, J. Johnstun, J. Saxe, J. Jia, K. V. Alwala, K. Prasad, K. Upasani, K. Plawiak, K. Li, K. Heafield, K. Stone, K. El-Arini, K. Iyer, K. Malik, K. Chiu, K. Bhalla, K. Lakhotia, L. Rantala-Yeary, L. van der Maaten, L. Chen, L. Tan, L. Jenkins, L. Martin, L. Madaan, L. Malo, L. Blecher, L. Landzaat, L. de Oliveira, M. Muzzi, M. Pasupuleti, M. Singh, M. Paluri, M. Kardas, M. Tsimpoukelli, M. Oldham, M. Rita, M. Pavlova, M. Kambadur, M. Lewis, M. Si, M. K. Singh, M. Hassan, N. Goyal, N. Torabi, N. Bashlykov, N. Bogoychev, N. Chatterji, N. Zhang, O. Duchenne, O. Çelebi, P. Alrassy, P. Zhang, P. Li, P. Vasic, P. Weng, P. Bhargava, P. Dubal, P. Krishnan, P. S. Koura, P. Xu, Q. He, Q. Dong, R. Srinivasan, R. Ganapathy, R. Calderer, R. S. Cabral, R. Stojnic, R. Raileanu, R. Maheswari, R. Girdhar, R. Patel, R. Sauvestre, R. Polidoro, R. Sumbaly, R. Taylor, R. Silva, R. Hou, R. Wang, S. Hosseini, S. Chennabasappa, S. Singh, S. Bell, S. S. Kim, S. Edunov, S. Nie, S. Narang, S. Raparthy, S. Shen, S. Wan, S. Bhosale, S. Zhang, S. Vandenhende, S. Batra, S. Whitman, S. Sootla, S. Collot, S. Gururangan, S. Borodinsky, T. Herman, T. Fowler, T. Sheasha, T. Georgiou, T. Scialom, T. Speckbacher, T. Mihaylov, T. Xiao, U. Karn, V. Goswami, V. Gupta, V. Ramanathan, V. Kerkez, V. Gonguet, V. Do, V. Vogeti, V. Albiero, V. Petrovic, W. Chu, W. Xiong, W. Fu, W. Meers, X. Martinet, X. Wang, X. Wang, X. E. Tan, X. Xia, X. Xie, X. Jia, X. Wang, Y. Goldschlag, Y. Gaur, Y. Babaei, Y. Wen, Y. Song, Y. Zhang, Y. Li, Y. Mao, Z. D. Coudert, Z. Yan, Z. Chen, Z. Papakipos, A. Singh, A. Srivastava, A. Jain, A. Kelsey, A. Shajnfeld, A. Gangidi, A. Victoria, A. Goldstand, A. Menon, A. Sharma, A. Boesenberg, A. Baevski, A. Feinstein, A. Kallet, A. Sangani, A. Teo, A. Yunus, A. Lupu, A. Alvarado, A. Caples, A. Gu, A. Ho, A. Poulton, A. Ryan, A. Ramchandani, A. Dong, A. Franco, A. Goyal, A. Saraf, A. Chowdhury, A. Gabriel, A. Bharambe, A. Eisenman, A. Yazdan, B. James, B. Maurer, B. Leonhardi, B. Huang, B. Loyd, B. D. Paola, B. Paranjape, B. Liu, B. Wu, B. Ni, B. Hancock, B. Wasti, B. Spence, B. Stojkovic, B. Gamido, B. Montalvo, C. Parker, C. Burton, C. Mejia, C. Liu, C. Wang, C. Kim, C. Zhou, C. Hu, C. Chu, C. Cai, C. Tindal, C. Feichtenhofer, C. Gao, D. Civin, D. Beaty, D. Kreymer, D. Li, D. Adkins, D. Xu, D. Testuggine, D. David, D. Parikh, D. Liskovich, D. Foss, D. Wang, D. Le, D. Holland, E. Dowling, E. Jamil, E. Montgomery, E. Presani, E. Hahn, E. Wood, E. Le, E. Brinkman, E. Arcaute, E. Dunbar, E. Smothers, F. Sun, F. Kreuk, F. Tian, F. Kokkinos, F. Ozgenel, F. Caggioni, F. Kanayet, F. Seide, G. M. Florez, G. Schwarz, G. Badeer, G. Swee, G. Halpern, G. Herman, G. Sizov, Guangyi, Zhang, G. Lakshminarayanan, H. Inan, H. Shojanazeri, H. Zou, H. Wang, H. Zha, H. Habeeb, H. Rudolph, H. Suk, H. Aspegren, H. Goldman, H. Zhan, I. Damlaj, I. Molybog, I. Tufanov, I. Leontiadis, I. Veliche, I. Gat, J. Weissman, J. Geboski, J. Kohli, J. Lam, J. Asher, J. Gaya, J. Marcus, J. Tang, J. Chan, J. Zhen, J. Reizenstein, J. Teboul, J. Zhong, J. Jin, J. Yang, J. Cummings, J. Carvill, J. Shepard, J. McPhie, J. Torres, J. Ginsburg, J. Wang, K. Wu, K. H. U, K. Saxena, K. Khandelwal, K. Zand, K. Matosich, K. Veeraraghavan, K. Michelena, K. Li, K. Jagadeesh, K. Huang, K. Chawla, K. Huang, L. Chen, L. Garg, L. A, L. Silva, L. Bell, L. Zhang, L. Guo, L. Yu, L. Moshkovich, L. Wehrstedt, M. Khabsa, M. Avalani, M. Bhatt, M. Mankus, M. Hasson, M. Lennie, M. Reso, M. Groshev, M. Naumov, M. Lathi, M. Keneally, M. Liu, M. L. Seltzer, M. Valko, M. Restrepo, M. Patel, M. Vyatskov, M. Samvelyan, M. Clark, M. Macey, M. Wang, M. J. Hermoso, M. Metanat, M. Rastegari, M. Bansal, N. Santhanam, N. Parks, N. White, N. Bawa, N. Singhal, N. Egebo, N. Usunier, N. Mehta, N. P. Laptev, N. Dong, N. Cheng, O. Chernoguz, O. Hart, O. Salpekar, O. Kalinli, P. Kent, P. Parekh, P. Saab, P. Balaji, P. Rittner, P. Bontrager, P. Roux, P. Dollar, P. Zvyagina, P. Ratanchandani, P. Yuvraj, Q. Liang, R. Alao, R. Rodriguez, R. Ayub, R. Murthy, R. Nayani, R. Mitra, R. Parthasarathy, R. Li, R. Hogan, R. Battey, R. Wang, R. Howes, R. Rinott, S. Mehta, S. Siby, S. J. Bondu, S. Datta, S. Chugh, S. Hunt, S. Dhillon, S. Sidorov, S. Pan, S. Mahajan, S. Verma, S. Yamamoto, S. Ramaswamy, S. Lindsay, S. Lindsay, S. Feng, S. Lin, S. C. Zha, S. Patil, S. Shankar, S. Zhang, S. Zhang, S. Wang, S. Agarwal, S. Sajuyigbe, S. Chintala, S. Max, S. Chen, S. Kehoe, S. Satterfield, S. Govindaprasad, S. Gupta, S. Deng, S. Cho, S. Virk, S. Subramanian, S. Choudhury, S. Goldman, T. Remez, T. Glaser, T. Best, T. Koehler, T. Robinson, T. Li, T. Zhang, T. Matthews, T. Chou, T. Shaked, V. Vontimitta, V. Ajayi, V. Montanez, V. Mohan, V. S. Kumar, V. Mangla, V. Ionescu, V. Poenaru, V. T. Mihailescu, V. Ivanov, W. Li, W. Wang, W. Jiang, W. Bouaziz, W. Constable, X. Tang, X. Wu, X. Wang, X. Wu, X. Gao, Y. Kleinman, Y. Chen, Y. Hu, Y. Jia, Y. Qi, Y. Li, Y. Zhang, Y. Zhang, Y. Adi, Y. Nam, Yu, Wang, Y. Zhao, Y. Hao, Y. Qian, Y. Li, Y. He, Z. Rait, Z. DeVito, Z. Rosnbrick, Z. Wen, Z. Yang, Z. Zhao, and Z. Ma
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
Proceedings of the 34th International Conference on Machine Learning,
ICML 2017, Sydney, NSW, Australia, 6-11 August 2017
,
D. Precup and Y. W. Teh (Eds.)
,
Proceedings of Machine Learning Research
, Vol.
70
,
pp. 1321–1330
.
External Links:
Link
Cited by:
§2
.
Hendrycks
et al.
(2021)
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song,
et al.
Measuring coding challenge competence with apps
.
arXiv preprint arXiv:2105.09938
.
Cited by:
§E.7
.
Horvitz and Thompson (1952)
D. G. Horvitz and D. J. Thompson
A generalization of sampling without replacement from a finite universe
.
Journal of the American Statistical Association
47
(
260
),
pp. 663–685
.
Cited by:
Appendix B
.
Hu
et al.
(2026)
T. Hu, C. Zhang, D. Hovy, and N. Collier
Position: large language model failures from hallucination to homogenization are different facets of miscalibration
.
TechRxiv
2026
(
0217
),
pp.
.
External Links:
Document
,
Link
,
https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.177130685.57616643/v1
Cited by:
§1
.
Huang
et al.
(2024)
Y. Huang, L. Sun, H. Wang, S. Wu, Q. Zhang, Y. Li, C. Gao, Y. Huang, W. Lyu, Y. Zhang,
et al.
Trustllm: trustworthiness in large language models
.
arXiv preprint arXiv:2401.05561
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
§5.1
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson, S. Johnston, S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen, Y. Bai, S. Bowman, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion, S. Kravec, L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei, T. Brown, J. Clark, N. Joseph, B. Mann, S. McCandlish, C. Olah, and J. Kaplan
Language models (mostly) know what they know
.
External Links:
2207.05221
Cited by:
§5.1
.
Kwon
et al.
(2023)
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica
Efficient Memory Management for Large Language Model Serving with PagedAttention
.
External Links:
2309.06180
,
Link
Cited by:
§D.1
.
Lacombe
et al.
(2025)
R. Lacombe, K. Wu, and E. Dilworth
Don’t think twice! over-reasoning impairs confidence calibration
.
arXiv preprint arXiv:2508.15050
.
Cited by:
§1
.
Lakshminarayanan
et al.
(2017)
B. Lakshminarayanan, A. Pritzel, and C. Blundell
Simple and scalable predictive uncertainty estimation using deep ensembles
.
In
Advances in Neural Information Processing Systems 30: Annual Conference
on Neural Information Processing Systems 2017, December 4-9, 2017,
Long Beach, CA, USA
,
I. Guyon, U. von Luxburg, S. Bengio, H. M. Wallach, R. Fergus, S. V. N. Vishwanathan, and R. Garnett (Eds.)
,
pp. 6402–6413
.
External Links:
Link
Cited by:
§2
.
Li
et al.
(2025)
C. Li, H. Zhou, G. Glavaš, A. Korhonen, and I. Vulić
Large language models are miscalibrated in-context learners
.
In
Findings of the Association for Computational Linguistics: ACL 2025
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 11575–11596
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-256-5
Cited by:
§1
.
Manakul
et al.
(2023)
P. Manakul, A. Liusie, and M. J. Gales
Selfcheckgpt: zero-resource black-box hallucination detection for generative large language models
.
arXiv preprint arXiv:2303.08896
.
Cited by:
§5.1
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
Minderer
et al.
(2021)
M. Minderer, J. Djolonga, R. Romijnders, F. Hubis, X. Zhai, N. Houlsby, D. Tran, and M. Lucic
Revisiting the calibration of modern neural networks
.
Advances in neural information processing systems
34
,
pp. 15682–15694
.
Cited by:
§2
.
Moskvichev and Sejdinovic (2025)
P. Moskvichev and D. Sejdinovic
All models are miscalibrated, but some less so: comparing calibration with conditional mean operators
.
In
Australasian Joint Conference on Artificial Intelligence
,
pp. 274–287
.
Cited by:
§2
.
Naeini
et al.
(2015)
M. P. Naeini, G. F. Cooper, and M. Hauskrecht
Obtaining well calibrated probabilities using bayesian binning
.
In
Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence,
January 25-30, 2015, Austin, Texas, USA
,
B. Bonet and S. Koenig (Eds.)
,
pp. 2901–2907
.
External Links:
Link
Cited by:
§2
.
Nguyen and O’Connor (2015)
K. Nguyen and B. O’Connor
Posterior calibration and exploratory analysis for natural language processing models
.
In
Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing
,
pp. 1587–1598
.
Cited by:
§2
.
Niculescu-Mizil and Caruana (2005)
A. Niculescu-Mizil and R. Caruana
Predicting good probabilities with supervised learning
.
In
Proceedings of the 22nd International Conference on Machine Learning
,
pp. 625–632
.
External Links:
Document
Cited by:
§2
.
Nixon
et al.
(2019)
J. Nixon, M. W. Dusenberry, L. Zhang, G. Jerfel, and D. Tran
Measuring calibration in deep learning.
.
In
CVPR workshops
,
Vol.
2
.
Cited by:
§2
,
§2
.
OpenAI
et al.
(2025)
OpenAI, :, S. Agarwal, L. Ahmad, J. Ai, S. Altman, A. Applebaum, E. Arbus, R. K. Arora, Y. Bai, B. Baker, H. Bao, B. Barak, A. Bennett, T. Bertao, N. Brett, E. Brevdo, G. Brockman, S. Bubeck, C. Chang, K. Chen, M. Chen, E. Cheung, A. Clark, D. Cook, M. Dukhan, C. Dvorak, K. Fives, V. Fomenko, T. Garipov, K. Georgiev, M. Glaese, T. Gogineni, A. Goucher, L. Gross, K. G. Guzman, J. Hallman, J. Hehir, J. Heidecke, A. Helyar, H. Hu, R. Huet, J. Huh, S. Jain, Z. Johnson, C. Koch, I. Kofman, D. Kundel, J. Kwon, V. Kyrylov, E. Y. Le, G. Leclerc, J. P. Lennon, S. Lessans, M. Lezcano-Casado, Y. Li, Z. Li, J. Lin, J. Liss, Lily, Liu, J. Liu, K. Lu, C. Lu, Z. Martinovic, L. McCallum, J. McGrath, S. McKinney, A. McLaughlin, S. Mei, S. Mostovoy, T. Mu, G. Myles, A. Neitz, A. Nichol, J. Pachocki, A. Paino, D. Palmie, A. Pantuliano, G. Parascandolo, J. Park, L. Pathak, C. Paz, L. Peran, D. Pimenov, M. Pokrass, E. Proehl, H. Qiu, G. Raila, F. Raso, H. Ren, K. Richardson, D. Robinson, B. Rotsted, H. Salman, S. Sanjeev, M. Schwarzer, D. Sculley, H. Sikchi, K. Simon, K. Singhal, Y. Song, D. Stuckey, Z. Sun, P. Tillet, S. Toizer, F. Tsimpourlas, N. Vyas, E. Wallace, X. Wang, M. Wang, O. Watkins, K. Weil, A. Wendling, K. Whinnery, C. Whitney, H. Wong, L. Yang, Y. Yang, M. Yasunaga, K. Ying, W. Zaremba, W. Zhan, C. Zhang, B. Zhang, E. Zhang, and S. Zhao
Gpt-oss-120b & gpt-oss-20b model card
.
External Links:
2508.10925
,
Link
Cited by:
§5.1
.
Pereyra
et al.
(2017)
G. Pereyra, G. Tucker, J. Chorowski, Ł. Kaiser, and G. Hinton
Regularizing neural networks by penalizing confident output distributions
.
arXiv preprint arXiv:1701.06548
.
Cited by:
§2
.
Platt
et al.
(1999)
J. Platt
et al.
Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods
.
Advances in large margin classifiers
10
(
3
),
pp. 61–74
.
Cited by:
§2
.
Pyatkin
et al.
(2025)
V. Pyatkin, S. Malik, V. Graf, H. Ivison, S. Huang, P. Dasigi, N. Lambert, and H. Hajishirzi
Generalizing verifiable instruction following
.
External Links:
2507.02833
,
Link
Cited by:
§E.7
.
Qwen
et al.
(2025)
Qwen, :, A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, H. Lin, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Lin, K. Dang, K. Lu, K. Bao, K. Yang, L. Yu, M. Li, M. Xue, P. Zhang, Q. Zhu, R. Men, R. Lin, T. Li, T. Tang, T. Xia, X. Ren, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Wan, Y. Liu, Z. Cui, Z. Zhang, and Z. Qiu
Qwen2.5 technical report
.
External Links:
2412.15115
,
Link
Cited by:
§5.1
.
Rein
et al.
(2023)
D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman
GPQA: a graduate-level google-proof q&a benchmark
.
External Links:
2311.12022
,
Link
Cited by:
§5.1
.
Rosenbaum and Rubin (1983)
P. R. Rosenbaum and D. B. Rubin
The central role of the propensity score in observational studies for causal effects
.
Biometrika
70
(
1
),
pp. 41–55
.
Cited by:
Appendix B
,
§4.2
.
Si
et al.
(2022)
C. Si, C. Zhao, S. Min, and J. Boyd-Graber
Re-examining calibration: the case of question answering
.
In
Findings of the Association for Computational Linguistics: EMNLP 2022
,
pp. 2814–2829
.
Cited by:
§2
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
pp. 5433–5442
.
Cited by:
§5.1
.
Vaicenavicius
et al.
(2019)
J. Vaicenavicius, D. Widmann, C. Andersson, F. Lindsten, J. Roll, and T. Schön
Evaluating model calibration in classification
.
In
The 22nd international conference on artificial intelligence and statistics
,
pp. 3459–3467
.
Cited by:
§2
.
Vu
et al.
(2023)
T. Vu, M. Iyyer, X. Wang, N. Constant, J. Wei, J. Wei, C. Tar, Y. Sung, D. Zhou, Q. Le, and T. Luong
FreshLLMs: refreshing large language models with search engine augmentation
.
External Links:
2310.03214
,
Link
Cited by:
§5.1
.
Wang
et al.
(2023)
B. Wang, W. Chen, H. Pei, C. Xie, M. Kang, C. Zhang, C. Xu, Z. Xiong, R. Dutta, R. Schaeffer,
et al.
DecodingTrust: a comprehensive assessment of trustworthiness in
{
\{
gpt
}
\}
models
.
Cited by:
§1
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
§5.1
.
Wang
et al.
(2024)
Y. Wang, X. Ma, G. Zhang, Y. Ni, A. Chandra, S. Guo, W. Ren, A. Arulraj, X. He, Z. Jiang, T. Li, M. Ku, K. Wang, A. Zhuang, R. Fan, X. Yue, and W. Chen
MMLU-pro: a more robust and challenging multi-task language understanding benchmark
.
External Links:
2406.01574
,
Link
Cited by:
§5.1
.
White
et al.
(2025)
C. White, S. Dooley, M. Roberts, A. Pal, B. Feuer, S. Jain, R. Shwartz-Ziv, N. Jain, K. Saifullah, S. Dey, Shubh-Agrawal, S. S. Sandha, S. Naidu, C. Hegde, Y. LeCun, T. Goldstein, W. Neiswanger, and M. Goldblum
LiveBench: a challenging, contamination-limited llm benchmark
.
External Links:
2406.19314
,
Link
Cited by:
§5.1
.
Xiong
et al.
(2024)
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi
Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms
.
In
The Twelfth International Conference on Learning Representations,
ICLR 2024, Vienna, Austria, May 7-11, 2024
,
External Links:
Link
Cited by:
§1
,
§5.1
.
Yang
et al.
(2025a)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu
Qwen3 technical report
.
External Links:
2505.09388
,
Link
Cited by:
§5.1
.
Yang
et al.
(2025b)
R. Yang, C. Zhang, Z. Zhang, X. Huang, S. Yang, N. Collier, D. Yu, and D. Yang
LoGU: long-form generation with uncertainty expressions
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 18947–18968
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-251-0
Cited by:
§1
.
Yang
et al.
(2025c)
R. Yang, C. Zhang, Z. Zhang, X. Huang, D. Yu, N. Collier, and D. Yang
UNCLE: benchmarking uncertainty expressions in long-form generation
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 30328–30344
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§1
.
Yoon
et al.
(2025)
D. Yoon, S. Kim, S. Yang, S. Kim, S. Kim, Y. Kim, E. Choi, Y. Kim, and M. Seo
Reasoning models better express their confidence
.
arXiv preprint arXiv:2505.14489
.
Cited by:
§1
,
§5.1
.
Zadrozny and Elkan (2002)
B. Zadrozny and C. Elkan
Transforming classifier scores into accurate multiclass probability estimates
.
In
Proceedings of the eighth ACM SIGKDD international conference on Knowledge discovery and data mining
,
pp. 694–699
.
Cited by:
§2
.
Zeng
et al.
(2025)
Q. Zeng, W. Xuan, L. Cui, and R. Voigt
Thinking out loud: do reasoning models know when they’re right?
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
pp. 1394–1407
.
Cited by:
§1
,
§5.1
.
Zhang
et al.
(2024)
C. Zhang, F. Liu, M. Basaldella, and N. Collier
LUQ: long-text uncertainty quantification for LLMs
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 5244–5262
.
External Links:
Link
,
Document
Cited by:
§1
.
Zhang
et al.
(2025a)
C. Zhang, C. Shu, E. Shareghi, and N. Collier
All roads lead to Rome: graph-based confidence estimation for large language model reasoning
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 31814–31824
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§1
.
Zhang
et al.
(2025b)
C. Zhang, R. Yang, Z. Zhang, X. Huang, S. Yang, D. Yu, and N. Collier
Atomic calibration of LLMs in long-form generations
.
In
Proceedings of the 14th International Joint Conference on Natural Language Processing and the 4th Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics
,
K. Inui, S. Sakti, H. Wang, D. F. Wong, P. Bhattacharyya, B. Banerjee, A. Ekbal, T. Chakraborty, and D. P. Singh (Eds.)
,
Mumbai, India
,
pp. 148–169
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-303-6
Cited by:
§1
.
Zhang
et al.
(2026a)
C. Zhang, R. Yang, X. Zhu, C. Li, T. Hu, Y. R. Dong, D. Yang, and N. Collier
Confidence estimation for LLMs in multi-turn interactions
.
In
Findings of the Association for Computational Linguistics: ACL 2026
,
M. Liakata, V. P. Moreira, J. Zhang, and D. Jurgens (Eds.)
,
San Diego, California, United States
,
pp. 25661–25676
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-395-1
Cited by:
§1
.
Zhang
et al.
(2026b)
C. Zhang, X. Zhu, C. Li, N. Collier, and A. Vlachos
LoVeC: reinforcement learning for better verbalized confidence in long-form generation
.
In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
M. Liakata, V. P. Moreira, J. Zhang, and D. Jurgens (Eds.)
,
San Diego, California, United States
,
pp. 33336–33363
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-390-6
Cited by:
§1
.
Zhou
et al.
(2025)
E. Zhou, C. Zhang, T. Hu, C. Li, N. Collier, I. Vulić, and A. Korhonen
Beyond the final layer: intermediate representations for better multilingual calibration in large language models
.
External Links:
2510.03136
,
Link
Cited by:
§1
.
Appendix A
General Analysis
A.1
Theoretical Analysis
Why accuracy is a confounder
Global calibration metrics depend not only on how confidence is distributed, but also on the proportion of correct versus incorrect predictions.
We formalize this mechanism in a deliberately controlled limit case, which is weaker than requiring uniform confidence across all predictions but is not intended as a full model of real LLM behavior.
Assumption 1
(Shared Conditional Confidence)
Two models
M
A
M_{A}
and
M
B
M_{B}
, evaluated on the same dataset, share identical conditional confidence distributions:
•
Correct
(
z
=
1
z=1
): confidence
c
∼
P
1
​
(
c
)
c\sim P_{1}(c)
, with mean
μ
1
=
𝔼
⁡
[
c
∣
z
=
1
]
\mu_{1}=\mathbb{E}[c\mid z=1]
and variance
σ
1
2
=
Var
⁡
(
c
∣
z
=
1
)
\sigma_{1}^{2}=\mathrm{Var}(c\mid z=1)
.
•
Incorrect
(
z
=
0
z=0
): confidence
c
∼
P
0
​
(
c
)
c\sim P_{0}(c)
, with mean
μ
0
=
𝔼
⁡
[
c
∣
z
=
0
]
\mu_{0}=\mathbb{E}[c\mid z=0]
and variance
σ
0
2
=
Var
⁡
(
c
∣
z
=
0
)
\sigma_{0}^{2}=\mathrm{Var}(c\mid z=0)
.
The two models differ solely in their accuracy
a
=
Acc
⁡
(
M
)
a=\mathrm{Acc}(M)
.
Under this assumption, the two models exhibit identical confidence
behavior
conditioned on correctness, differing only in how often they are right.
This isolates accuracy as the only source of variation: any resulting calibration difference is attributable to accuracy rather than to intrinsic differences in uncertainty estimation. We use this as an illustrative sufficient case, not as a claim that real LLMs differ only in accuracy.
Proposition 1
(Limit-case: BS Linear in Accuracy)
Under Assumption
1
, the Brier Score is a linear
function of accuracy
a
a
. Let
L
0
=
σ
0
2
+
μ
0
2
L_{0}=\sigma_{0}^{2}+\mu_{0}^{2}
,
Δ
L
=
σ
1
2
+
(
1
−
μ
1
)
2
−
σ
0
2
−
μ
0
2
\Delta_{L}=\sigma_{1}^{2}+(1-\mu_{1})^{2}-\sigma_{0}^{2}-\mu_{0}^{2}
. Then
BS
⁡
(
a
)
=
L
0
+
a
⋅
Δ
L
.
\mathrm{BS}(a)=L_{0}+a\cdot\Delta_{L}.
Proof.
By the law of total expectation, decompose the Brier Score by correctness:
BS
\displaystyle\mathrm{BS}
=
𝔼
⁡
[
(
c
−
z
)
2
]
=
a
⋅
𝔼
⁡
[
(
c
−
1
)
2
∣
z
=
1
]
\displaystyle=\mathbb{E}\!\left[(c-z)^{2}\right]=a\cdot\mathbb{E}\!\left[(c-1)^{2}\mid z=1\right]
+
(
1
−
a
)
⋅
𝔼
[
c
2
∣
z
=
0
]
.
\displaystyle+(1-a)\cdot\mathbb{E}\!\left[c^{2}\mid z=0\right].
For the two conditional terms, applying the bias-variance decomposition gives
𝔼
⁡
[
(
c
−
1
)
2
∣
z
=
1
]
\displaystyle\mathbb{E}\!\left[(c-1)^{2}\mid z=1\right]
=
Var
⁡
(
c
∣
z
=
1
)
\displaystyle=\mathrm{Var}(c\mid z=1)
+
(
𝔼
⁡
[
c
∣
z
=
1
]
−
1
)
2
\displaystyle+\bigl(\mathbb{E}[c\mid z=1]-1\bigr)^{2}
=
σ
1
2
+
(
1
−
μ
1
)
2
,
\displaystyle=\sigma_{1}^{2}+(1-\mu_{1})^{2},
𝔼
⁡
[
c
2
∣
z
=
0
]
\displaystyle\mathbb{E}\!\left[c^{2}\mid z=0\right]
=
Var
⁡
(
c
∣
z
=
0
)
\displaystyle=\mathrm{Var}(c\mid z=0)
+
(
𝔼
⁡
[
c
∣
z
=
0
]
)
2
=
σ
0
2
+
μ
0
2
.
\displaystyle+\bigl(\mathbb{E}[c\mid z=0]\bigr)^{2}=\sigma_{0}^{2}+\mu_{0}^{2}.
Substituting into Equation (
A.1
), we have
BS
⁡
(
a
)
=
a
⁡
[
σ
1
2
+
(
1
−
μ
1
)
2
]
+
(
1
−
a
)
​
[
σ
0
2
+
μ
0
2
]
\displaystyle\mathrm{BS}(a)=a\bigl[\sigma_{1}^{2}+(1-\mu_{1})^{2}\bigr]+(1-a)\bigl[\sigma_{0}^{2}+\mu_{0}^{2}\bigr]
=
[
σ
0
2
+
μ
0
2
]
+
a
⁡
[
σ
1
2
+
(
1
−
μ
1
)
2
−
σ
0
2
−
μ
0
2
]
\displaystyle=\bigl[\sigma_{0}^{2}+\mu_{0}^{2}\bigr]+a\bigl[\sigma_{1}^{2}+(1-\mu_{1})^{2}-\sigma_{0}^{2}-\mu_{0}^{2}\bigr]
=
L
0
+
a
⋅
Δ
L
.
\displaystyle=L_{0}+a\cdot\Delta_{L}.
□
\square
Remark 1
(Slope condition is easily satisfied)
The condition
Δ
L
<
0
\Delta_{L}<0
holds when correct predictions
deviate less from their ideal confidence than incorrect ones.
Since the ideal confidence is
1
1
for correct predictions and
0
0
for incorrect ones, this reduces to
σ
1
2
+
(
1
−
μ
1
)
2
<
σ
0
2
+
μ
0
2
,
\sigma_{1}^{2}+(1-\mu_{1})^{2}<\sigma_{0}^{2}+\mu_{0}^{2},
which is readily satisfied in practice: well-functioning models
assign higher confidence to correct predictions (
μ
1
>
μ
0
\mu_{1}>\mu_{0}
),
making
(
1
−
μ
1
)
2
(1-\mu_{1})^{2}
small, while overconfidence on incorrect
predictions keeps
μ
0
2
\mu_{0}^{2}
substantial. Consequently, higher
accuracy mechanically improves BS even when the underlying
confidence behavior is identical.
Remark 2
(Constant-confidence case)
When
P
1
P_{1}
and
P
0
P_{0}
both degenerate to a point mass at
q
q
,
i.e.,
μ
1
=
μ
0
=
q
\mu_{1}=\mu_{0}=q
and
σ
1
=
σ
0
=
0
\sigma_{1}=\sigma_{0}=0
, Proposition
1
simplifies to
BS
⁡
(
a
)
=
q
2
+
a
⁡
(
1
−
2
​
q
)
,
\mathrm{BS}(a)=q^{2}+a(1-2q),
recovering the toy example of Section
3
.
Extension to ECE.
Unlike the Brier Score, ECE includes binning and absolute values, so its dependence on accuracy is not globally linear. Under a fixed binning and a common overconfidence regime, however, the mechanism can be stated formally.
Proposition 2
(ECE confound under overconfidence)
Suppose Assumption
1
holds,
a
B
≥
a
A
a_{B}\geq a_{A}
, and a fixed binning is used. If every populated bin is overconfident for both models, then
ECE
A
−
ECE
B
=
(
a
B
−
a
A
)
​
(
1
−
μ
1
+
μ
0
)
≥
0
.
\mathrm{ECE}_{A}-\mathrm{ECE}_{B}=(a_{B}-a_{A})(1-\mu_{1}+\mu_{0})\geq 0.
Thus, with identical confidence behavior conditioned on correctness, higher accuracy alone cannot increase ECE under this sufficient condition.
Proof.
Since every populated bin is overconfident, the absolute value in each bin can be removed in the same direction. Therefore,
ECE
⁡
(
a
)
\displaystyle\mathrm{ECE}(a)
=
∑
b
Pr
⁡
(
S
b
)
​
(
conf
⁡
(
S
b
)
−
acc
⁡
(
S
b
)
)
\displaystyle=\sum_{b}\Pr(S_{b})\bigl(\mathrm{conf}(S_{b})-\mathrm{acc}(S_{b})\bigr)
=
𝔼
⁡
[
c
]
−
𝔼
⁡
[
z
]
\displaystyle=\mathbb{E}[c]-\mathbb{E}[z]
=
a
​
μ
1
+
(
1
−
a
)
​
μ
0
−
a
\displaystyle=a\mu_{1}+(1-a)\mu_{0}-a
=
μ
0
−
a
⁡
(
1
−
μ
1
+
μ
0
)
.
\displaystyle=\mu_{0}-a(1-\mu_{1}+\mu_{0}).
Taking the difference between models
A
A
and
B
B
gives
ECE
A
−
ECE
B
=
(
a
B
−
a
A
)
​
(
1
−
μ
1
+
μ
0
)
.
\mathrm{ECE}_{A}-\mathrm{ECE}_{B}=(a_{B}-a_{A})(1-\mu_{1}+\mu_{0}).
The result is nonnegative because
a
B
≥
a
A
a_{B}\geq a_{A}
,
μ
1
≤
1
\mu_{1}\leq 1
, and
μ
0
≥
0
\mu_{0}\geq 0
.
□
\square
Remark 3
(Constant-confidence ECE case)
When
P
1
P_{1}
and
P
0
P_{0}
both degenerate to a point mass at
q
q
, we have
μ
1
=
μ
0
=
q
\mu_{1}=\mu_{0}=q
. Under the overconfident regime
a
≤
q
a\leq q
considered in Section
3
, Proposition
2
reduces to
ECE
⁡
(
a
)
=
q
−
a
,
\mathrm{ECE}(a)=q-a,
recovering the ECE toy example in Section
3
. Consequently, for two models satisfying
a
A
≤
a
B
≤
q
a_{A}\leq a_{B}\leq q
,
ECE
A
−
ECE
B
=
a
B
−
a
A
≥
0
.
\mathrm{ECE}_{A}-\mathrm{ECE}_{B}=a_{B}-a_{A}\geq 0.
When ranking reversal occurs
For the Brier Score, let
L
m
,
z
=
𝔼
⁡
[
(
c
−
z
)
2
∣
z
]
L_{m,z}=\mathbb{E}\!\left[(c-z)^{2}\mid z\right]
denote model
m
m
’s conditional loss for outcome
z
z
, and let
R
m
​
(
t
)
=
t
​
L
m
,
1
+
(
1
−
t
)
​
L
m
,
0
R_{m}(t)=tL_{m,1}+(1-t)L_{m,0}
be its loss under a common target accuracy
t
t
. Define
Δ
raw
\displaystyle\Delta_{\mathrm{raw}}
=
R
A
​
(
a
A
)
−
R
B
​
(
a
B
)
,
\displaystyle=R_{A}(a_{A})-R_{B}(a_{B}),
Δ
t
\displaystyle\Delta_{t}
=
R
A
​
(
t
)
−
R
B
​
(
t
)
.
\displaystyle=R_{A}(t)-R_{B}(t).
Direct expansion gives
Δ
raw
=
Δ
t
+
C
t
,
\Delta_{\mathrm{raw}}=\Delta_{t}+C_{t},
where
C
t
=
\displaystyle C_{t}={}
(
a
A
−
t
)
​
(
L
A
,
1
−
L
A
,
0
)
\displaystyle(a_{A}-t)(L_{A,1}-L_{A,0})
−
(
a
B
−
t
)
​
(
L
B
,
1
−
L
B
,
0
)
.
\displaystyle-(a_{B}-t)(L_{B,1}-L_{B,0}).
When
Δ
t
≠
0
\Delta_{t}\neq 0
, a strict ranking reversal occurs exactly when
sign
⁡
(
C
t
)
\displaystyle\operatorname{sign}(C_{t})
=
−
sign
⁡
(
Δ
t
)
,
\displaystyle=-\operatorname{sign}(\Delta_{t}),
|
C
t
|
\displaystyle|C_{t}|
>
|
Δ
t
|
.
\displaystyle>|\Delta_{t}|.
Thus, a reversal occurs when the contribution from the models’
different outcome compositions opposes and exceeds their loss gap at
the common target accuracy.
For ECE, the result above exhibits the same qualitative mechanism
under its stated condition: changing the mixture of correct and
incorrect outcomes can change ECE even when conditional confidence
behavior is held fixed, so its ranking may likewise change after
accuracy alignment.
A.2
Empirical Analysis
Empirical Setup.
We verify this empirically in Figure
1
. Across five
benchmarks spanning knowledge-based (TriviaQA, FreshQA) and
reasoning-based tasks (MMLU-Pro, GPQA, LiveBench), we compare the ECE gap against the accuracy gap between stronger models and weaker models, covering both scale-based pairs (Qwen2.5 7B vs. 72B, LLaMA 3.1 8B vs. 70B, GPT-OSS 20B vs. 120B) and thinking vs. non-thinking pairs (Qwen3-8B and GPT-OSS under
high/low reasoning settings). The results reveal a strong negative correlation (
ρ
=
−
0.670
\rho=-0.670
,
n
=
40
n=40
, 95% CI
[
−
0.81
,
−
0.45
]
[-0.81,-0.45]
,
p
<
10
−
5
p<10^{-5}
) between accuracy differences and raw ECE differences, consistent with our theoretical analysis: models with higher accuracy mechanically obtain better ECE scores even when their underlying confidence behavior is not correspondingly superior.
Appendix B
Justification of Distribution-Aligned Calibration
The importance-weighting principle underlying Distribution-Aligned (DA) originates in survey sampling
(
Horvitz and Thompson, 1952
)
and is widely used in causal inference to correct for confounded comparisons between treatments and outcomes
(
Rosenbaum and Rubin, 1983
)
. We briefly justify its application in our setting by making the analogy explicit.
Standard causal inference formulation.
Consider a binary treatment
T
∈
{
0
,
1
}
T\in\{0,1\}
, an outcome
Y
Y
, and a confounder
X
X
that influences both
T
T
and
Y
Y
. The naïve comparison
𝔼
⁡
[
Y
∣
T
=
1
]
−
𝔼
⁡
[
Y
∣
T
=
0
]
\mathbb{E}[Y\mid T=1]-\mathbb{E}[Y\mid T=0]
is biased whenever the distribution of
X
X
differs across treatment groups. DA removes this bias by reweighting each observation by the inverse of its treatment probability (propensity score), so that the weighted confounder distribution is balanced across groups.
Mapping to calibration comparison.
In our setting, the role of the
treatment
T
T
is played by model identity
m
∈
{
A
,
B
}
m\in\{A,B\}
: comparing calibration across models is analogous to comparing outcomes across treatment arms.
The
confounder
X
X
corresponds to instance-level correctness
z
i
(
m
)
z_{i}^{(m)}
, which aggregates to model accuracy
a
m
=
Acc
⁡
(
M
m
)
a_{m}=\mathrm{Acc}(M_{m})
; just as a covariate that differs across treatment groups biases the naïve comparison, differing accuracy compositions confound the raw calibration comparison. The
outcome
Y
Y
maps to the per-instance calibration loss,
e
.
g
.,
(
c
i
(
m
)
−
z
i
(
m
)
)
2
(c_{i}^{(m)}-z_{i}^{(m)})^{2}
for the Brier Score.
The
propensity score
P
⁡
(
T
∣
X
)
P(T\mid X)
corresponds to the probability of each correctness status in the source model, namely
a
A
a_{A}
for correct predictions (
z
=
1
z=1
) and
1
−
a
A
1-a_{A}
for incorrect predictions (
z
=
0
z=0
).
Finally, the
target population
is the accuracy level of the reference model
a
B
a_{B}
, to which we wish to adjust the distribution of the results of the source model.
Under this mapping, the weights
w
i
(
A
)
=
{
a
B
/
a
A
if
​
z
i
(
A
)
=
1
,
(
1
−
a
B
)
/
(
1
−
a
A
)
if
​
z
i
(
A
)
=
0
,
w_{i}^{(A)}=\begin{cases}a_{B}\,/\,a_{A}&\text{if }z_{i}^{(A)}=1,\\[4.0pt]
(1-a_{B})\,/\,(1-a_{A})&\text{if }z_{i}^{(A)}=0,\end{cases}
are standard importance weights that transform the correctness distribution of
M
A
M_{A}
to match the target accuracy
a
B
a_{B}
. For each correctness class
z
∈
{
0
,
1
}
z\in\{0,1\}
, the weight equals the target proportion divided by the source proportion, which is precisely the density ratio form used in classical importance weighting.
Assumptions.
The validity of DA here requires two standard conditions:
1)
Positivity
:
0
<
a
m
<
1
0<a_{m}<1
, which holds trivially on any nontrivial benchmark; and
2)
Conditional exchangeability
: conditioned on correctness status
z
z
, the confidence distribution is comparable across the accuracy shift.
Appendix C
Instruction Prompt Examples
Answer Generation Prompts
All models share the same answer-generation prompt family, with template selection determined by task type; reasoning behavior is controlled via model parameters rather than prompt wording. Specifically, we apply the multiple-choice template to GPQA Diamond and MMLU-Pro, the reasoning template to LiveBench, and the open-ended template to FreshQA and TriviaQA. The method-specific confidence-elicitation templates and their use are described in Appendix
D.3
.
I: MULTIPLE-CHOICE TEMPLATE
Task: Solve the following multiple-choice problem.
The answer should be a single letter (A, B, C, D, etc.).
Provide your final answer in the following format:
\boxed{A}
Problem:
{problem}
II: REASONING TEMPLATE
Task: Solve the following reasoning problem.
Provide your final answer in the following XML format:
<answer>final answer here</answer>
Problem:
{problem}
III: OPEN-ENDED TEMPLATE
Task: Answer the following factual question directly.
This is NOT a multiple-choice question. Provide a direct factual answer.
Provide your final answer in the following XML format:
<answer>final answer here</answer>
Question:
{problem}
Table 3:
Three prompt templates used for generation across different task types.
Appendix D
Implementation Details
D.1
Model and Inference Details
We evaluate 14 locally deployed models spanning four families: Qwen2.5, LLaMA 3.1, Qwen3, and GPT-OSS. Table
12
lists all models. Qwen3 and GPT-OSS each expose a reasoning-intensity control: for Qwen3, the
enable_thinking
flag in the chat template switches between thinking (
True
) and non-thinking (
False
) modes; for GPT-OSS, the
reasoning_effort
parameter selects between
high
and
low
settings. This yields 14 model configurations in total.
All models are served locally via vLLM
(
Kwon et al., 2023
)
in
bfloat16
precision.
Both answer-generation and confidence-estimation stages share the same decoding configuration: temperature
=
1.0
=1.0
, top-
p
=
1.0
p=1.0
, and top-
k
=
−
1
k=-1
, with
max_tokens
set to
max_model_len
. Context lengths are 32,768 tokens for Qwen2.5 and Qwen3, 40,960 for LLaMA 3.1, and 131,072 for GPT-OSS.
D.2
Dataset Details and Evaluation Protocol
We evaluate on five datasets: FreshQA, TriviaQA, GPQA Diamond, LiveBench, and MMLU-Pro.
Dataset
Type
Size
FreshQA
Knowledge
600
TriviaQA
Knowledge
1,500
GPQA Diamond
Reasoning
198
LiveBench (reasoning subset)
Reasoning
200
MMLU-Pro
Reasoning
2,841
Table 4:
Summary of the evaluation datasets used in our experiments.
FreshQA.
We use the
2025-10-07
version of FreshQA and evaluate on 600 questions. This dataset is treated as an open-ended factual QA benchmark. Correctness is determined by LLM-based grading.
TriviaQA.
We sample 1,500 examples from the
unfiltered-nocontent
validation split of TriviaQA. This dataset is treated as open-ended factual QA. We use alias-aware exact match, where a prediction is counted as correct if it matches any acceptable alias.
GPQA Diamond.
We use the standard GPQA Diamond split, containing 198 examples. This dataset is treated as an expert-level multiple-choice benchmark. Correctness is determined by exact matching between the extracted option letter and the gold answer.
LiveBench.
We evaluate on 200 examples from the reasoning subset of LiveBench. This benchmark is treated as a reasoning / fill-in task. Correctness is determined by rule-based matching.
MMLU-Pro.
We evaluate on 2,841 examples from the computer science, chemistry, and physics domains of MMLU-Pro. This dataset is treated as a multiple-choice benchmark. Correctness is determined by exact matching between the extracted option letter and the gold answer.
D.3
Confidence Elicitation Details
We consider three confidence estimation methods: verbalized confidence, P(True), and self-consistency. The answer-generation prompts used to produce the responses evaluated here are listed in Appendix
C
.
Verbalized Confidence.
The model is presented with the original question alongside its own full response and asked to assign a confidence score from 0 to 100. We use the full
model_response
rather than the extracted short answer as the answer source. We extract the numeric value inside
\boxed{}
and normalize it to
[
0
,
1
]
[0,1]
by dividing by 100.
VANILLA-VERB TEMPLATE
{Question}
Proposed Answer: {Answer}
How confident are you that the proposed answer is correct?
The confidence score should be a number from 0 (completely unsure) to 100 (absolutely certain).
Your response MUST strictly adhere to this format:
### Confidence: \boxed{Your confidence score from 0-100.}
Now it is your turn to give a response:
Table 5:
Vanilla verbalized confidence estimation template.
P(True).
The model is presented with the original question alongside its own full response and asked to judge whether the proposed answer is true or false. Confidence is defined as the probability assigned to token
A
(“True”): we request
logprobs=20
, extract the log-probability of token
A
, and convert it to a linear probability.
BINARY VERIFICATION TEMPLATE
{Question}
Proposed Answer: {Answer}
Is the proposed answer:
A. True
B. False
Output format: A or B only
(single uppercase letter; no spaces, punctuation, or explanation):
Table 6:
Binary verification template for answer correctness judgment.
Self-Consistency.
For self-consistency, we generate 10 independent responses for each question using the same answer-generation prompt and decoding setup. The confidence of an example is defined as the fraction of runs whose extracted answer matches the extracted answer from the first run:
c
i
=
∑
k
=
1
10
𝟏
[
a
^
k
=
a
^
1
]
10
.
c_{i}=\frac{\sum_{k=1}^{10}\mathbf{1}[\hat{a}_{k}=\hat{a}_{1}]}{10}.
Here,
a
^
1
\hat{a}_{1}
denotes the extracted answer from the first run and
a
^
k
\hat{a}_{k}
denotes the extracted answer from run
k
k
. If an example is marked as
is_attempted=False
in the first run, we skip it. If the answer is missing in later runs, the denominator remains 10.
Appendix E
Additional Analyses
E.1
Reversal Rates on Knowledge and Reasoning Benchmarks
We further investigate whether ranking reversals are more prevalent on reasoning than knowledge benchmarks. Table
7
shows this pattern holds consistently under the DA and IA views, but varies under CA. Specifically, verbalized confidence yields higher reasoning reversal rates across all alignment views, whereas SC and
P
⁡
(
true
)
P(\mathrm{true})
diverge under CA.
Additionally, Table
8
indicates that, aggregated across all methods and views, this reasoning-knowledge gap is driven primarily by mode/effort differences between evaluated models, rather than size differences.
Method
View
KRR
RRR
Δ
\Delta
(RRR
−
-
KRR)
SC
DA
0
6.2
41.7
+
+
35.4
IA
18.8
41.7
+
+
22.9
CA
56.2
41.7
−
-
14.6
Verbalized
DA
43.8
58.3
+
+
14.6
IA
50.0
62.5
+
+
12.5
CA
18.8
33.3
+
+
14.6
P
⁡
(
true
)
P(\text{true})
DA
37.5
54.2
+
+
16.7
IA
25.0
25.0
+
+
0.0
CA
50.0
20.8
−
-
29.2
Table 7:
Knowledge reversal rate (KRR) and reasoning reversal rate (RRR) broken down by confidence method and alignment view. For
Δ
⁡
(
RRR
−
KRR
)
\Delta(\text{RRR}-\text{KRR})
, positive values indicate reversal is more frequent on reasoning datasets.
Pair type
KRR
RRR
Δ
\Delta
(RRR
−
-
KRR)
#Pairs
mode/effort
33.3
45.2
+
+
11.9
5
size
35.2
37.0
+
+
1.9
3
Table 8:
Average reversal gap by pair type after merging all confidence methods and aligned
views. Positive
Δ
\Delta
values indicate that reversal is more frequent on reasoning datasets.
E.2
Reversal Rates Across Accuracy-Gap Bins
Figure 5:
Reversal rate by accuracy-gap bin. The combined figure presents the same pattern from two complementary perspectives: grouped by confidence method and grouped by aligned view. In both views, reversal increases once the accuracy gap exceeds 0.1, but does not exhibit a clear monotonic increase across higher bins.
We further examine how reversal rates change as the accuracy gap between the
two compared models increases. Figure
5
shows that the pattern is better described as threshold-like than monotonic.
More concretely, when the accuracy gap is below 0.1, reversal rates are
generally much lower across both the method-grouped and view-grouped panels.
Once the gap exceeds 0.1, reversal becomes noticeably more common and remains
at a substantially higher level. This indicates that reversal is much more
likely once the two models are separated by a non-trivial gap in task
accuracy.
At the same time, the figure does not support the stronger claim that
reversal keeps increasing as the accuracy gap becomes larger and larger. After
crossing the 0.1 threshold, the higher-gap bins fluctuate rather than rising
monotonically. In other words, the key empirical dividing line is whether the
accuracy gap is above 0.1, not which larger bin it falls into.
E.3
Both-Wrong and Both-Right Confidence Distributions
Figure
6
reveals several consistent
patterns across methods and datasets. First, all three confidence methods show
substantial separation between both-wrong and both-right examples: both-right
mass is generally concentrated toward the high-confidence end, while both-wrong
mass is shifted to the left. In this sense, all three methods preserve a
meaningful distinction between clearly correct and clearly incorrect shared
outcomes.
At the same time, the three methods differ in how sharply and how reliably
they make this distinction. Verbalized confidence and
P
⁡
(
true
)
P(\mathrm{true})
are
more polarized, with much of their mass pushed toward the two extremes. This
produces visually sharp distributions, but it also reveals substantial
overconfidence: both methods still assign considerable probability mass near
the high-confidence end even on both-wrong examples. Among the three,
verbalized confidence appears to show the weakest separation overall, with the
red and blue mean lines often relatively close to each other, indicating that
incorrect shared outcomes still receive fairly high confidence.
P
⁡
(
true
)
P(\mathrm{true})
shows a similar but somewhat less severe pattern.
SC behaves differently. Its distributions are broader and less concentrated at
the extremes, so the distinction between both-wrong and both-right is less
“all-or-nothing” but often more conservative. In particular, SC places less
mass on extremely high confidence for both-wrong examples, making its
overconfidence visibly weaker than that of verbalized confidence and
P
⁡
(
true
)
P(\mathrm{true})
. This does not mean that SC is free of overconfidence—some
datasets still show substantial overlap—but the figure suggests that its
errors are less driven by extreme high-confidence mistakes.
Figure 6:
Histogram comparison of confidence distributions on both-wrong and both-right examples across three confidence elicitation methods and five datasets. The figure is intended as a descriptive view of how well the two shared-outcome regions are separated, and where overconfidence on both-wrong examples may appear.
E.4
Instance-Aligned Retention
Since IA compares models only on shared-outcome examples, one concern is that
the retained subset might become too small to support stable conclusions. We
therefore report the retained sample size for each model-pair–dataset cell.
Retention is defined as
|
D
IA
|
/
|
D
|
|D_{\mathrm{IA}}|/|D|
, where
D
IA
=
D
both
​
-
​
right
∪
D
both
​
-
​
wrong
D_{\mathrm{IA}}=D_{\mathrm{both\mbox{-}right}}\cup D_{\mathrm{both\mbox{-}wrong}}
.
As shown in Table
9
, IA retains substantial coverage
across all 40 model-pair–dataset cells: the median retention is 78.0%,
the IQR is [66.3%, 82.2%], and the minimum is 55.2%. No cell falls below
50%, indicating that the IA results are not driven by narrow retained subsets. Together with the aggregate correlation in Figure
1
, this suggests that the observed reversals reflect a systematic accuracy-related confound rather than sampling noise.
Pair
Type
FreshQA
GPQA
LiveBench
TriviaQA
MMLU-Pro
Qwen3-8B T/N
Mode
474 (79.0)
135 (68.2)
113 (56.5)
1181 (78.7)
2263 (79.7)
Qwen3-14B T/N
Mode
474 (79.0)
130 (65.7)
120 (60.0)
1229 (81.9)
2360 (83.1)
Qwen3-32B T/N
Mode
469 (78.2)
142 (71.7)
115 (57.5)
1208 (80.5)
2369 (83.4)
GPT-OSS-120B H/L
Effort
524 (87.3)
159 (80.3)
144 (72.0)
1356 (90.4)
2574 (90.6)
GPT-OSS-20B H/L
Effort
498 (83.0)
137 (69.2)
128 (64.0)
1215 (81.0)
2377 (83.7)
Qwen2.5 72B/7B
Size
446 (74.3)
123 (62.1)
133 (66.5)
1003 (66.9)
1797 (63.3)
LLaMA3.1 70B/8B
Size
331 (55.2)
124 (62.6)
154 (77.0)
1119 (74.6)
1706 (60.0)
GPT-OSS 120B/20B H
Size
480 (80.0)
168 (84.8)
179 (89.5)
1168 (77.9)
2654 (93.4)
Table 9:
Instance-Aligned retained sample sizes across model-pair–dataset cells. Each cell reports
|
D
IA
|
|D_{\mathrm{IA}}|
with the retention percentage in parentheses. Dataset sizes are 600 for FreshQA, 198 for GPQA Diamond, 200 for LiveBench Reasoning, 1,500 for TriviaQA, and 2,841 for MMLU-Pro. T/N denotes thinking versus non-thinking, and H/L denotes high versus low reasoning effort.
E.5
DA Effective Sample Size
Although DA uses all observed instances, concentrated weights can reduce
its effective precision. Using the Kish effective sample size,
ESS
=
(
∑
i
w
i
)
2
/
∑
i
w
i
2
\mathrm{ESS}=(\sum_{i}w_{i})^{2}/\sum_{i}w_{i}^{2}
, we obtain a median
ESS
/
N
\mathrm{ESS}/N
of
0.897
0.897
across 120 method–pair–dataset cells.
Overall,
115
/
120
115/120
cells have
ESS
/
N
≥
0.5
\mathrm{ESS}/N\geq 0.5
; the remaining
five fall below this diagnostic threshold, with a minimum of
0.144
0.144
. Thus, DA retains high effective precision in most comparisons, with a few cases substantially affected by weight concentration.
E.6
Bootstrap Analysis of Ranking Reversals
We assess sampling uncertainty using 2,000 paired bootstrap samples of
the evaluated questions. For each combination of confidence method,
model pair, and dataset, questions are resampled jointly for the two
models. We then recompute the Raw comparison and all three aligned
views from each resample. IA rebuilds the subset on which the models
share the same outcome, DA re-estimates the outcome proportions and
importance weights, and CA keeps each question together with its
candidate pool. The 2.5th and 97.5th percentiles form the 95%
confidence intervals for the Raw and aligned gaps.
For each reversal in the original estimates, we also record the
proportion of bootstrap samples in which the Raw and aligned gaps
remain opposite in sign. Among the 720 comparisons, 265 show a
reversal in the original estimates. Their median retention probability
is 91.9%, and 122 of the 265 remain reversals in at least 95% of the
bootstrap samples.
Metric
Point estimate
Strict criterion
ECE
86 (71.7)
31 (25.8)
Brier Score
84 (70.0)
45 (37.5)
Table 10:
Bootstrap results aggregated over 120 cells. Each cell
corresponds to one combination of confidence method, model pair,
and dataset. Each entry reports the number of cells, with the
percentage in parentheses. The point estimate column counts cells
containing a reversal in at least one of CA, IA, or DA. The strict
criterion additionally requires, for at least one view, that the
Raw and aligned 95% confidence intervals both exclude zero and
have opposite signs.
E.7
Extension to Graded Correctness
The binary formulation extends naturally to tasks with partial credit.
Let
z
i
∈
[
0
,
1
]
z_{i}\in[0,1]
denote the graded correctness of prediction
i
i
, and
interpret the confidence score
c
i
∈
[
0
,
1
]
c_{i}\in[0,1]
as the model’s predicted
degree of correctness. The functional forms of the Brier Score and ECE
remain unchanged:
BS
\displaystyle\mathrm{BS}
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
,
\displaystyle=\frac{1}{N}\sum_{i=1}^{N}(c_{i}-z_{i})^{2},
ECE
\displaystyle\mathrm{ECE}
=
∑
b
=
1
B
|
S
b
|
N
​
|
z
¯
b
−
c
¯
b
|
,
\displaystyle=\sum_{b=1}^{B}\frac{|S_{b}|}{N}\left|\bar{z}_{b}-\bar{c}_{b}\right|,
where
S
b
=
{
i
:
c
i
∈
I
b
}
S_{b}=\{i:c_{i}\in I_{b}\}
, and
z
¯
b
\bar{z}_{b}
and
c
¯
b
\bar{c}_{b}
denote the
mean graded correctness and mean confidence in bin
b
b
, respectively.
The binary setting is recovered when
z
i
∈
{
0
,
1
}
z_{i}\in\{0,1\}
.
IA, DA, and CA extend naturally by replacing binary outcomes with graded
outcomes in their respective constructions. For graded IA, let
h
h
be a
prespecified mapping from graded scores to matching labels, and define
D
IA
graded
​
(
h
)
=
{
i
:
h
⁡
(
z
i
(
A
)
)
=
h
⁡
(
z
i
(
B
)
)
}
.
D_{\mathrm{IA}}^{\mathrm{graded}}(h)=\left\{i:h\!\left(z_{i}^{(A)}\right)=h\!\left(z_{i}^{(B)}\right)\right\}.
Setting
h
⁡
(
z
)
=
z
h(z)=z
gives exact score matching. If
h
h
instead assigns scores
to prespecified bins, it provides coarser alignment that can increase
sample retention. The choice of
h
h
controls the trade-off between
alignment granularity and sample retention.
For graded DA, let
g
:
[
0
,
1
]
→
{
1
,
…
,
K
}
g:[0,1]\rightarrow\{1,\ldots,K\}
map each graded
outcome to an outcome stratum, and let
p
m
,
k
p_{m,k}
denote the empirical
proportion of model
m
m
’s outcomes falling in stratum
k
k
. Given a common
target distribution
q
=
(
q
1
,
…
,
q
K
)
q=(q_{1},\ldots,q_{K})
over these strata, the importance
weight assigned to example
i
i
for model
m
m
is
w
i
(
m
)
=
q
k
p
m
,
k
,
k
=
g
⁡
(
z
i
(
m
)
)
,
w_{i}^{(m)}=\frac{q_{k}}{p_{m,k}},\qquad k=g\!\left(z_{i}^{(m)}\right),
assuming
p
m
,
k
>
0
p_{m,k}>0
whenever
q
k
>
0
q_{k}>0
. These weights align each model’s
graded-outcome distribution with the common target
q
q
before computing
the calibration metrics.
For graded CA, the shared candidate pool and aggregation procedure remain
unchanged. The existing candidate correctness label
y
i
​
(
s
)
y_{i}(s)
is extended
from
{
0
,
1
}
\{0,1\}
to
[
0
,
1
]
[0,1]
, and
e
i
(
m
)
​
(
s
)
e_{i}^{(m)}(s)
represents model
m
m
’s
predicted degree of correctness for candidate
s
s
. The candidate-level
Brier Score and ECE are then computed as in binary CA using these graded
quantities.
Experimental setup.
To evaluate the graded extension while keeping inference cost manageable,
we compare Qwen2.5-7B and Qwen2.5-72B using verbalized confidence. We use
500 examples from each dataset and normalize the elicited 0–100 confidence
scores to
[
0
,
1
]
[0,1]
.
Datasets and graded correctness.
We evaluate on two datasets with different forms of partial credit:
IF-multi
(
Pyatkin et al., 2025
)
and APPS
(
Hendrycks et al., 2021
)
. IF-multi consists of instruction-following
prompts with multiple automatically verifiable constraints. We use prompts
containing three to five constraints and define graded correctness as the
fraction of constraints satisfied by the response, as determined by the
accompanying rule-based verifiers. APPS is a code-generation benchmark
evaluated through test cases. We sample problems from its official test
split across all three difficulty levels and define graded correctness as
the fraction of official test cases passed by the generated program. In
both datasets, verbalized confidence is elicited for the same quantity used
to define graded correctness: the expected fraction of satisfied constraints
or passed test cases.
Alignment implementation.
We evaluate graded IA and DA, whose alignments are constructed directly
from graded correctness outcomes and do not require the additional
cross-model candidate evaluation used by CA. For IA, we use exact score
matching on both datasets, corresponding to
h
⁡
(
z
)
=
z
h(z)=z
in the definition
above. For DA, the empirical graded-outcome distribution of Qwen2.5-7B
serves as the target. Because IF-multi has a small discrete set of scores
determined by three to five constraints, we align its exact graded-score
levels. APPS has a denser score distribution because the number of test
cases varies across problems, so we partition
[
0
,
1
]
[0,1]
into 10 equal-width
outcome strata. Every stratum with positive target mass has positive
empirical support under both models, satisfying the support condition
required by graded DA.
Results.
Qwen2.5-72B achieves higher mean graded correctness than Qwen2.5-7B
on both IF-multi (55.1% vs. 44.1%) and APPS (53.2% vs. 31.7%).
Table
11
reports the corresponding calibration gaps,
defined as the score of Qwen2.5-72B minus that of Qwen2.5-7B. Under Raw
evaluation, both the Brier Score and ECE favor Qwen2.5-72B on both
datasets. On both datasets, IA and DA reverse the Raw ordering for both
metrics, favoring Qwen2.5-7B. These results show that the reversal
phenomenon is not specific to binary correctness and can also arise when
outcomes receive partial credit.
Dataset
Metric
Raw
Δ
\Delta
IA
Δ
\Delta
DA
Δ
\Delta
IF-multi
Brier Score
−
6.0
-6.0
+
1.4
+1.4
+
1.5
+1.5
ECE
−
5.8
-5.8
+
3.2
+3.2
+
3.1
+3.1
APPS
Brier Score
−
6.3
-6.3
+
6.7
+6.7
+
9.8
+9.8
ECE
−
8.0
-8.0
+
5.9
+5.9
+
8.5
+8.5
Table 11:
Calibration gaps under graded correctness.
Δ
\Delta
denotes
Qwen2.5-72B minus Qwen2.5-7B, and all values are multiplied by 100.
Because lower scores indicate better calibration, negative values favor
Qwen2.5-72B and positive values favor Qwen2.5-7B.
Appendix F
Calibration Metrics
Tables
12
–
16
present the full calibration metrics underlying the trends visualized in Figures
2
and
3
. For each of the five evaluation datasets (FreshQA, TriviaQA, GPQA Diamond, LiveBench Reasoning, and MMLU-Pro), we report accuracy and two calibration measures (
i
.
e
., Brier Score and ECE), across three confidence elicitation methods (Verbalize, P(True), and Self-Consistency) and four evaluation views:
Raw
,
CA
,
DA
and
IA
. All accuracy values are computed from a single run with temperature
=
1
=1
. Each model pair is followed by a
Δ
\Delta
row showing the difference (Model
1
−
-
Model
2
), where
green
indicates the better-performing direction and
red
the worse.
Model
Acc
Raw
CA
DA
IA
Brier
ECE
Brier
ECE
Brier
ECE
Brier
ECE
Verbalize
Qwen2.5-7B
21.4
53.3
53.3
49.5
45.9
52.2
56.8
49.6
54.6
Qwen2.5-72B
38.7
44.6
42.3
41.2
38.7
54.5
58.4
52.1
56.1
Δ
\Delta
-17.3
+8.7
+11.0
+8.3
+7.2
-2.3
-1.6
-2.5
-1.5
Llama3.1-8B
32.1
48.5
50.7
44.9
44.2
45.1
47.2
43.7
46.6
Llama3.1-70B
49.3
32.1
32.9
32.6
31.6
50.5
51.9
49.0
50.5
Δ
\Delta
-17.2
+16.3
+17.9
+12.3
+12.5
-5.4
-4.7
-5.3
-3.9
Qwen3-8B-nothink
26.8
57.0
60.7
53.8
56.7
57.1
61.0
57.6
61.7
Qwen3-8B-think
36.1
42.4
46.4
35.8
42.3
61.3
65.5
60.8
65.3
Δ
\Delta
-9.3
+14.6
+14.3
+18.0
+14.4
-4.1
-4.5
-3.2
-3.6
Qwen3-32B-nothink
31.3
36.5
37.6
43.3
44.9
36.5
37.6
33.6
34.9
Qwen3-32B-think
41.6
50.7
52.8
45.0
47.6
59.5
62.4
57.4
60.5
Δ
\Delta
-10.3
-14.2
-15.2
-1.7
-2.7
-23.0
-24.8
-23.8
-25.6
GPT-OSS-20B-low
35.8
39.5
42.0
31.2
32.4
39.5
42.0
39.3
43.1
GPT-OSS-20B-high
40.1
44.2
47.8
26.5
27.5
47.6
51.8
46.6
51.1
Δ
\Delta
-4.3
-4.7
-5.7
+4.7
+4.9
-8.1
-9.7
-7.3
-8.0
GPT-OSS-120B-low
46.3
33.1
35.0
32.7
33.4
33.1
35.0
32.4
35.6
GPT-OSS-120B-high
47.8
33.6
37.2
32.8
34.4
34.5
38.4
33.8
38.3
Δ
\Delta
-1.5
-0.5
-2.2
-0.1
-1.0
-1.4
-3.4
-1.4
-2.6
GPT-OSS-20B-high
40.1
44.2
47.8
26.5
27.5
47.6
51.8
46.6
51.1
GPT-OSS-120B-high
47.8
33.6
37.2
32.8
34.4
34.5
38.4
33.8
38.3
Δ
\Delta
-7.7
+10.6
+10.5
-6.2
-6.9
+13.1
+13.3
+12.8
+12.9
P(True)
Qwen2.5-7B
21.4
39.7
40.5
39.0
39.1
39.7
40.5
39.3
40.0
Qwen2.5-72B
38.7
31.4
31.6
26.0
25.6
38.7
41.4
36.8
39.8
Δ
\Delta
-17.3
+8.3
+8.8
+13.0
+13.4
+1.0
-0.9
+2.6
+0.2
Llama3.1-8B
32.1
40.6
39.8
36.0
38.0
41.3
44.2
41.0
44.4
Llama3.1-70B
49.3
35.6
36.0
38.2
36.9
61.1
62.4
59.4
61.3
Δ
\Delta
-17.2
+5.0
+3.7
-2.2
+1.1
-19.8
-18.1
-18.4
-17.0
Qwen3-8B-nothink
26.8
50.3
51.2
50.5
51.6
50.3
51.2
50.5
51.6
Qwen3-8B-think
36.1
66.5
66.7
65.5
65.8
66.5
66.7
65.5
65.8
Δ
\Delta
-9.3
-16.2
-15.5
-14.9
-14.1
-16.2
-15.5
-14.9
-14.1
Qwen3-32B-nothink
31.3
33.6
36.5
40.8
42.1
33.6
36.5
32.7
36.0
Qwen3-32B-think
41.6
47.1
47.0
38.0
37.6
53.4
53.5
52.5
52.7
Δ
\Delta
-10.3
-13.4
-10.5
+2.8
+4.5
-19.7
-17.0
-19.8
-16.7
GPT-OSS-20B-low
35.8
44.0
44.1
46.9
46.9
44.0
44.1
44.6
44.6
GPT-OSS-20B-high
40.1
51.7
51.7
46.5
46.6
55.4
55.5
54.8
54.8
Δ
\Delta
-4.3
-7.6
-7.7
+0.4
+0.4
-11.4
-11.4
-10.2
-10.2
GPT-OSS-120B-low
46.3
39.6
39.6
43.0
43.1
39.6
39.6
39.1
39.1
GPT-OSS-120B-high
47.8
45.1
45.1
40.5
40.5
46.2
46.2
45.2
45.2
Δ
\Delta
-1.5
-5.5
-5.5
+2.6
+2.6
-6.6
-6.6
-6.1
-6.1
GPT-OSS-20B-high
40.1
51.7
51.7
46.5
46.6
55.4
55.5
54.8
54.8
GPT-OSS-120B-high
47.8
45.1
45.1
40.5
40.5
46.2
46.2
45.2
45.2
Δ
\Delta
-7.7
+6.6
+6.7
+6.0
+6.1
+9.2
+9.3
+9.5
+9.6
Self-Consistency
Qwen2.5-7B
21.4
27.4
24.4
17.5
14.5
27.4
24.4
25.2
21.2
Qwen2.5-72B
38.7
33.5
29.9
24.5
14.7
38.0
38.2
36.1
36.5
Δ
\Delta
-17.3
-6.1
-5.5
-7.0
-0.2
-10.6
-13.8
-10.9
-15.3
Llama3.1-8B
32.1
21.9
14.1
19.5
13.3
21.9
14.1
23.7
16.0
Llama3.1-70B
49.3
28.5
23.5
29.8
24.9
24.9
18.4
24.5
18.8
Δ
\Delta
-17.2
-6.6
-9.4
-10.3
-11.6
-3.0
-4.2
-0.7
-2.8
Qwen3-8B-nothink
26.8
26.2
22.6
17.8
11.5
26.1
22.5
23.5
19.7
Qwen3-8B-think
36.1
23.0
15.0
23.1
16.2
20.8
14.3
19.8
14.1
Δ
\Delta
-9.3
+3.3
+7.6
-5.3
-4.7
+5.3
+8.2
+3.8
+5.7
Qwen3-32B-nothink
31.3
24.7
18.4
20.2
14.0
24.7
18.4
24.5
17.5
Qwen3-32B-think
41.6
23.9
16.8
26.3
21.5
21.3
14.2
20.9
14.1
Δ
\Delta
-10.3
+0.7
+1.6
-6.1
-7.5
+3.3
+4.3
+3.6
+3.4
GPT-OSS-20B-low
35.8
21.9
14.7
21.4
15.6
21.9
14.7
22.9
15.9
GPT-OSS-20B-high
40.1
25.6
18.3
26.2
19.9
23.6
16.7
23.7
17.8
Δ
\Delta
-4.3
-3.7
-3.6
-4.8
-4.3
-1.8
-2.0
-0.8
-1.9
GPT-OSS-120B-low
46.3
29.4
23.7
28.3
22.7
29.4
23.7
30.6
25.1
GPT-OSS-120B-high
47.8
31.2
26.5
32.3
27.1
31.3
27.0
30.5
26.1
Δ
\Delta
-1.5
-1.9
-2.8
-4.0
-4.4
-1.9
-3.3
+0.1
-1.1
GPT-OSS-20B-high
40.1
25.6
18.3
26.2
19.9
23.6
16.7
23.7
17.8
GPT-OSS-120B-high
47.8
31.2
26.5
32.3
27.1
31.3
27.0
30.5
26.1
Δ
\Delta
-7.7
-5.7
-8.2
-6.0
-7.2
-7.7
-10.3
-6.8
-8.3
Table 12:
Calibration metrics on
FreshQA
. For calibration metrics (Brier, ECE), lower is better (
↓
\downarrow
).
Δ
\Delta
rows show the difference (Model
1
−
-
Model
2
).
Green
: better;
Red
: worse.
Model
Acc
Raw
CA
DA
IA
Brier
ECE
Brier
ECE
Brier
ECE
Brier
ECE
Verbalize
Qwen2.5-7B
41.4
31.2
32.8
27.9
28.4
31.2
32.8
25.7
27.0
Qwen2.5-72B
71.7
20.5
20.6
18.3
18.6
38.7
40.0
26.7
27.6
Δ
\Delta
-30.3
+10.7
+12.2
+9.6
+9.8
-7.5
-7.2
-1.0
-0.6
Llama3.1-8B
59.9
29.8
29.9
24.5
23.6
29.8
29.9
18.7
18.3
Llama3.1-70B
79.1
19.0
18.9
18.9
18.8
29.5
29.5
18.4
18.3
Δ
\Delta
-19.2
+10.8
+11.0
+5.6
+4.8
+0.2
+0.4
+0.3
-0.1
Qwen3-8B-nothink
45.3
42.9
45.2
38.6
40.3
42.9
45.2
37.6
39.6
Qwen3-8B-think
60.3
32.4
33.8
30.1
32.5
44.5
47.4
37.5
40.2
Δ
\Delta
-15.0
+10.5
+11.4
+8.5
+7.8
-1.5
-2.3
+0.2
-0.6
Qwen3-32B-nothink
54.1
24.7
25.1
27.2
27.7
24.7
25.1
21.3
21.7
Qwen3-32B-think
64.5
28.7
28.9
25.7
26.4
36.6
37.7
30.6
31.7
Δ
\Delta
-10.4
-4.0
-3.8
+1.4
+1.3
-11.9
-12.6
-9.3
-10.0
GPT-OSS-20B-low
52.0
21.9
22.2
22.0
22.3
21.9
22.2
18.9
19.1
GPT-OSS-20B-high
60.3
24.3
25.0
25.3
25.7
29.1
31.1
24.6
27.0
Δ
\Delta
-8.3
-2.4
-2.7
-3.3
-3.4
-7.2
-8.9
-5.6
-8.0
GPT-OSS-120B-low
74.9
12.0
10.8
12.4
11.0
12.0
10.8
10.4
8.6
GPT-OSS-120B-high
78.8
12.9
11.8
12.3
11.4
17.2
17.0
12.1
11.4
Δ
\Delta
-3.9
-0.9
-0.9
+0.1
-0.4
-5.2
-6.2
-1.7
-2.8
GPT-OSS-20B-high
60.3
24.3
25.0
25.3
25.7
29.1
31.1
24.6
27.0
GPT-OSS-120B-high
78.8
12.9
11.8
12.3
11.4
17.2
17.0
12.1
11.4
Δ
\Delta
-18.5
+11.4
+13.2
+13.0
+14.3
+11.9
+14.1
+12.5
+15.7
P(True)
Qwen2.5-7B
41.4
25.9
25.9
26.0
25.7
25.9
25.9
22.7
22.6
Qwen2.5-72B
71.7
17.9
17.4
15.4
14.7
31.8
32.5
21.6
21.9
Δ
\Delta
-30.3
+8.0
+8.4
+10.6
+11.0
-5.9
-6.6
+1.1
+0.7
Llama3.1-8B
59.9
26.0
25.0
21.9
19.1
26.0
25.0
17.3
14.4
Llama3.1-70B
79.1
17.1
15.6
17.2
15.9
29.5
29.8
18.2
17.9
Δ
\Delta
-19.2
+9.0
+9.5
+4.8
+3.2
-3.4
-4.8
-0.9
-3.5
Qwen3-8B-nothink
45.3
38.2
38.6
34.8
34.9
38.2
38.6
35.1
35.3
Qwen3-8B-think
60.3
34.6
34.7
30.1
30.2
46.6
46.9
39.3
39.8
Δ
\Delta
-15.0
+3.6
+3.9
+4.8
+4.8
-8.4
-8.4
-4.3
-4.5
Qwen3-32B-nothink
54.1
22.7
22.1
25.1
24.6
22.7
22.1
20.8
20.2
Qwen3-32B-think
64.5
29.6
29.5
24.2
24.0
35.8
35.8
30.1
30.1
Δ
\Delta
-10.4
-6.9
-7.5
+0.9
+0.6
-13.1
-13.7
-9.3
-9.9
GPT-OSS-20B-low
52.0
25.0
25.1
26.8
26.8
25.0
25.1
22.3
22.3
GPT-OSS-20B-high
60.3
31.2
31.2
27.3
27.4
36.4
36.4
31.4
31.4
Δ
\Delta
-8.3
-6.1
-6.2
-0.5
-0.5
-11.4
-11.4
-9.1
-9.1
GPT-OSS-120B-low
74.9
14.7
14.7
16.2
16.2
14.7
14.7
12.7
12.7
GPT-OSS-120B-high
78.8
19.1
19.1
16.9
16.9
24.8
24.8
18.1
18.1
Δ
\Delta
-3.9
-4.3
-4.3
-0.6
-0.6
-10.1
-10.1
-5.4
-5.4
GPT-OSS-20B-high
60.3
31.2
31.2
27.3
27.4
36.4
36.4
31.4
31.4
GPT-OSS-120B-high
78.8
19.1
19.1
16.9
16.9
24.8
24.8
18.1
18.1
Δ
\Delta
-18.5
+12.1
+12.1
+10.5
+10.5
+11.6
+11.7
+13.2
+13.2
Self-Consistency
Qwen2.5-7B
41.4
17.9
8.9
13.6
7.8
17.9
8.9
18.1
12.2
Qwen2.5-72B
71.7
17.1
11.7
21.5
22.4
25.1
22.7
19.2
14.2
Δ
\Delta
-30.3
+0.9
-2.7
-7.9
-14.6
-7.2
-13.8
-1.1
-2.1
Llama3.1-8B
59.9
23.8
19.4
23.3
21.6
23.8
19.4
26.8
28.0
Llama3.1-70B
79.1
18.8
17.0
25.2
30.0
18.7
11.8
17.0
13.9
Δ
\Delta
-19.2
+5.0
+2.4
-1.9
-8.4
+5.1
+7.6
+9.7
+14.1
Qwen3-8B-nothink
45.3
19.8
11.9
14.8
4.9
19.8
11.9
17.4
9.0
Qwen3-8B-think
60.3
14.5
7.4
19.2
17.9
14.3
4.7
13.0
4.5
Δ
\Delta
-15.0
+5.3
+4.4
-4.4
-13.0
+5.5
+7.2
+4.4
+4.5
Qwen3-32B-nothink
54.1
17.6
9.5
14.7
7.4
17.6
9.5
15.9
8.5
Qwen3-32B-think
64.5
14.7
11.3
18.2
18.2
13.8
7.3
13.3
8.2
Δ
\Delta
-10.4
+2.9
-1.8
-3.5
-10.8
+3.8
+2.2
+2.6
+0.3
GPT-OSS-20B-low
52.0
17.4
13.3
17.6
15.9
17.4
13.3
18.0
14.7
GPT-OSS-20B-high
60.3
17.9
12.8
19.8
18.3
16.9
9.0
16.5
9.9
Δ
\Delta
-8.3
-0.5
+0.4
-2.2
-2.4
+0.5
+4.2
+1.4
+4.8
GPT-OSS-120B-low
74.9
13.7
9.7
13.9
11.1
13.7
9.7
13.1
10.4
GPT-OSS-120B-high
78.8
14.6
10.8
15.7
13.1
15.1
9.9
14.1
10.2
Δ
\Delta
-3.9
-0.9
-1.0
-1.8
-1.9
-1.4
-0.2
-0.9
+0.3
GPT-OSS-20B-high
60.3
17.9
12.8
19.8
18.3
16.9
9.0
16.5
9.9
GPT-OSS-120B-high
78.8
14.6
10.8
15.7
13.1
15.1
9.9
14.1
10.2
Δ
\Delta
-18.5
+3.3
+2.1
+4.1
+5.2
+1.8
-0.9
+2.5
-0.2
Table 13:
Calibration metrics on
TriviaQA
. For calibration metrics (Brier, ECE), lower is better (
↓
\downarrow
).
Δ
\Delta
rows show the difference (Model
1
−
-
Model
2
).
Green
: better;
Red
: worse.
Model
Acc
Raw
CA
DA
IA
Brier
ECE
Brier
ECE
Brier
ECE
Brier
ECE
Verbalize
Qwen2.5-7B
33.3
52.5
54.8
48.6
49.3
54.7
57.1
50.1
52.1
Qwen2.5-72B
50.0
41.8
41.2
41.7
42.4
54.7
57.1
52.0
54.6
Δ
\Delta
-16.7
+10.8
+13.6
+6.9
+6.9
0.0
0.0
-1.9
-2.5
Llama3.1-8B
18.7
61.9
63.7
54.6
54.9
61.9
63.7
62.9
64.8
Llama3.1-70B
39.9
43.6
45.5
39.7
40.8
47.0
50.4
53.3
56.6
Δ
\Delta
-21.2
+18.3
+18.2
+14.9
+14.1
+14.9
+13.3
+9.5
+8.2
Qwen3-8B-nothink
46.0
41.9
42.5
32.5
29.5
45.5
45.5
38.0
36.7
Qwen3-8B-think
61.6
26.8
25.9
31.5
32.8
45.1
46.4
38.3
37.8
Δ
\Delta
-15.6
+15.2
+16.6
+0.9
-3.3
+0.4
-0.9
-0.3
-1.1
Qwen3-32B-nothink
51.5
38.5
39.2
34.0
33.8
38.5
39.2
29.5
28.9
Qwen3-32B-think
67.7
31.9
31.9
35.9
35.8
45.4
46.2
35.8
36.0
Δ
\Delta
-16.2
+6.6
+7.3
-1.9
-2.0
-6.9
-7.1
-6.3
-7.1
GPT-OSS-20B-low
56.6
24.2
19.7
25.8
20.0
24.2
19.7
12.8
7.6
GPT-OSS-20B-high
74.2
12.7
9.2
22.8
19.3
33.7
34.3
11.3
8.7
Δ
\Delta
-17.6
+11.5
+10.5
+3.0
+0.7
-9.5
-14.6
+1.5
-1.1
GPT-OSS-120B-low
64.6
17.5
11.6
20.9
14.5
17.5
11.6
12.9
8.6
GPT-OSS-120B-high
81.3
14.5
11.2
15.5
12.9
26.3
26.1
15.6
14.2
Δ
\Delta
-16.7
+2.9
+0.5
+5.4
+1.6
-8.8
-14.5
-2.7
-5.5
GPT-OSS-20B-high
74.2
12.7
9.2
22.8
19.3
33.7
34.3
11.3
8.7
GPT-OSS-120B-high
81.3
14.5
11.2
15.5
12.9
26.3
26.1
15.6
14.2
Δ
\Delta
-7.1
-1.8
-2.0
+7.3
+6.4
+7.4
+8.2
-4.2
-5.5
P(True)
Qwen2.5-7B
33.3
34.7
33.5
39.5
37.5
34.7
33.5
31.1
30.1
Qwen2.5-72B
50.0
40.3
39.1
34.8
32.0
47.4
48.2
46.4
48.8
Δ
\Delta
-16.7
-5.6
-5.6
+4.8
+5.5
-12.7
-14.7
-15.3
-18.7
Llama3.1-8B
18.7
38.2
40.4
36.1
34.3
38.2
40.4
39.4
43.0
Llama3.1-70B
39.9
39.8
37.3
37.5
35.4
49.2
52.0
51.3
55.9
Δ
\Delta
-21.2
-1.6
+3.1
-1.4
-1.2
-11.1
-11.6
-12.0
-12.9
Qwen3-8B-nothink
46.0
40.6
39.3
32.5
29.5
40.6
39.3
41.7
40.2
Qwen3-8B-think
61.6
26.8
25.9
31.5
32.8
47.5
47.9
43.4
43.6
Δ
\Delta
-15.6
+13.8
+13.4
+0.9
-3.3
-6.9
-8.6
-1.7
-3.4
Qwen3-32B-nothink
51.5
32.1
28.8
32.0
28.9
32.1
28.8
28.8
25.2
Qwen3-32B-think
67.7
38.1
38.1
38.2
38.1
47.8
47.7
41.4
41.4
Δ
\Delta
-16.2
-6.0
-9.3
-6.2
-9.2
-15.7
-18.9
-12.6
-16.2
GPT-OSS-20B-low
56.6
29.9
30.2
36.8
37.0
29.9
30.2
23.9
24.2
GPT-OSS-20B-high
74.2
17.4
17.6
22.5
22.7
38.7
38.8
17.4
17.4
Δ
\Delta
-17.6
+12.5
+12.7
+14.4
+14.3
-8.8
-8.6
+6.5
+6.8
GPT-OSS-120B-low
64.6
28.5
28.5
27.2
27.0
28.5
28.5
19.4
19.4
GPT-OSS-120B-high
81.3
25.2
25.2
25.0
25.0
39.5
39.5
25.2
25.2
Δ
\Delta
-16.7
+3.2
+3.3
+2.2
+1.9
-11.0
-10.9
-5.7
-5.8
GPT-OSS-20B-high
74.2
17.4
17.6
22.5
22.7
38.7
38.8
17.4
17.4
GPT-OSS-120B-high
81.3
25.2
25.2
25.0
25.0
39.5
39.5
25.2
25.2
Δ
\Delta
-7.1
-7.8
-7.7
-2.5
-2.3
-0.7
-0.7
-7.7
-7.7
Self-Consistency
Qwen2.5-7B
33.3
55.5
56.2
32.5
34.7
55.5
56.2
52.5
54.1
Qwen2.5-72B
50.0
32.4
34.1
32.5
34.7
32.4
34.1
32.5
34.7
Δ
\Delta
-16.7
+23.2
+22.1
0.0
0.0
+23.2
+22.1
+19.9
+19.3
Llama3.1-8B
18.7
18.9
17.5
17.2
20.2
18.9
17.5
17.2
20.2
Llama3.1-70B
39.9
28.3
32.5
28.7
34.0
28.3
32.5
28.7
34.0
Δ
\Delta
-21.2
-9.4
-14.9
-11.5
-13.9
-9.4
-14.9
-11.5
-13.9
Qwen3-8B-nothink
46.0
23.2
12.8
20.1
13.5
23.2
14.6
24.1
15.4
Qwen3-8B-think
61.6
23.2
18.0
22.0
12.7
29.4
27.5
26.4
24.4
Δ
\Delta
-15.6
0.0
-5.2
-1.9
+0.8
-6.2
-12.9
-2.3
-9.0
Qwen3-32B-nothink
51.5
20.3
13.7
15.2
10.5
20.3
13.7
17.8
10.6
Qwen3-32B-think
67.7
18.8
14.8
17.8
9.2
26.1
26.0
20.5
20.5
Δ
\Delta
-16.2
+1.5
-1.1
-2.6
+1.3
-5.8
-12.3
-2.8
-9.9
GPT-OSS-20B-low
56.6
18.4
14.8
12.2
10.4
18.4
14.8
16.9
13.5
GPT-OSS-20B-high
74.2
15.7
13.0
15.8
6.9
22.1
22.5
16.8
18.4
Δ
\Delta
-17.6
+2.7
+1.8
-3.6
+3.5
-3.7
-7.7
+0.1
-4.9
GPT-OSS-120B-low
64.6
19.5
15.2
13.0
10.0
19.5
15.2
14.3
10.9
GPT-OSS-120B-high
81.3
11.0
9.9
12.3
7.2
15.4
16.0
11.0
10.1
Δ
\Delta
-16.7
+8.5
+5.2
+0.6
+2.8
+4.0
-0.9
+3.3
+0.8
GPT-OSS-20B-high
74.2
15.7
13.0
15.8
6.9
22.1
22.5
16.8
18.4
GPT-OSS-120B-high
81.3
11.0
9.9
12.3
7.2
15.4
16.0
11.0
10.1
Δ
\Delta
-7.1
+4.6
+3.1
+3.5
-0.3
+6.7
+6.5
+5.8
+8.2
Table 14:
Calibration metrics on
GPQA Diamond
. For calibration metrics (Brier, ECE), lower is better (
↓
\downarrow
).
Δ
\Delta
rows show the difference (Model
1
−
-
Model
2
).
Green
: better;
Red
: worse.
Model
Acc
Raw
CA
DA
IA
Brier
ECE
Brier
ECE
Brier
ECE
Brier
ECE
Verbalize
Qwen2.5-7B
17.0
70.6
74.1
64.5
67.0
73.0
76.8
71.2
75.7
Qwen2.5-72B
36.5
55.9
57.9
60.5
64.8
73.0
76.8
74.2
78.4
Δ
\Delta
-19.5
+14.7
+16.2
+4.0
+2.3
0.0
0.0
-3.1
-2.7
Llama3.1-8B
9.5
70.5
73.0
65.1
66.8
70.5
73.0
70.7
73.9
Llama3.1-70B
22.5
52.1
53.8
44.7
47.8
57.1
60.3
59.0
62.5
Δ
\Delta
-13.0
+18.4
+19.2
+20.4
+19.0
+13.4
+12.7
+11.7
+11.5
Qwen3-8B-nothink
38.5
55.6
55.4
21.3
19.1
53.5
55.1
31.5
30.8
Qwen3-8B-think
77.0
17.3
16.0
37.6
38.5
49.4
53.4
29.0
30.7
Δ
\Delta
-38.5
+38.3
+39.4
-16.3
-19.4
+4.1
+1.8
+2.4
+0.0
Qwen3-32B-nothink
47.0
43.7
44.5
27.7
27.8
43.7
44.5
18.9
17.3
Qwen3-32B-think
85.5
12.0
11.7
27.4
27.8
40.7
43.1
17.3
18.1
Δ
\Delta
-38.5
+31.7
+32.8
+0.3
0.0
+3.0
+1.4
+1.6
-0.7
GPT-OSS-20B-low
59.5
16.5
8.9
23.8
20.8
16.5
8.9
8.5
16.3
GPT-OSS-20B-high
89.5
2.2
6.3
16.9
14.9
13.7
14.8
2.2
7.4
Δ
\Delta
-30.0
+14.3
+2.6
+7.0
+5.9
+2.8
-5.9
+6.3
+8.8
GPT-OSS-120B-low
69.0
9.1
6.5
23.8
20.8
9.1
6.5
6.0
13.2
GPT-OSS-120B-high
93.0
3.0
6.4
8.5
5.2
9.4
11.0
2.5
5.2
Δ
\Delta
-24.0
+6.1
+0.1
+15.4
+15.5
-0.3
-4.6
+3.4
+8.0
GPT-OSS-20B-high
89.5
2.2
6.3
16.9
14.9
13.7
14.8
2.2
7.4
GPT-OSS-120B-high
93.0
3.0
6.4
8.5
5.2
9.4
11.0
2.5
5.2
Δ
\Delta
-3.5
-0.8
-0.1
+8.4
+9.7
+4.3
+3.7
-0.3
+2.2
P(True)
Qwen2.5-7B
17.0
59.1
61.4
57.6
59.2
59.1
61.4
57.2
59.6
Qwen2.5-72B
36.5
54.1
54.3
52.7
54.6
69.8
71.6
72.3
73.5
Δ
\Delta
-19.5
+5.0
+7.1
+5.0
+4.6
-10.7
-10.2
-15.1
-13.9
Llama3.1-8B
9.5
34.9
45.9
38.8
46.9
34.9
45.9
34.4
47.8
Llama3.1-70B
22.5
52.1
53.8
44.7
47.8
62.2
69.9
64.7
73.3
Δ
\Delta
-13.0
-17.2
-7.9
-5.9
-0.9
-27.3
-24.1
-30.3
-25.6
Qwen3-8B-nothink
38.5
45.1
45.5
34.0
33.3
45.1
45.5
34.0
33.3
Qwen3-8B-think
77.0
29.0
30.0
29.0
30.0
46.9
49.5
29.0
30.0
Δ
\Delta
-38.5
+16.1
+15.5
+5.0
+3.3
-1.9
-4.1
+5.0
+3.3
Qwen3-32B-nothink
47.0
30.3
28.0
19.5
17.4
30.3
28.0
22.5
24.6
Qwen3-32B-think
85.5
12.8
13.0
21.3
21.0
40.0
40.6
18.7
19.0
Δ
\Delta
-38.5
+17.4
+15.0
-1.8
-3.7
-9.7
-12.6
+3.8
+5.6
GPT-OSS-20B-low
59.5
21.9
22.2
15.3
15.7
21.9
22.2
12.7
12.8
GPT-OSS-20B-high
89.5
6.2
6.2
12.7
13.0
23.3
23.3
3.9
3.9
Δ
\Delta
-30.0
+15.7
+16.0
+2.6
+2.8
-1.4
-1.1
+8.8
+8.9
GPT-OSS-120B-low
69.0
15.0
15.0
9.4
9.3
15.0
15.0
12.5
12.5
GPT-OSS-120B-high
93.0
4.5
4.5
5.0
5.0
16.2
16.2
3.5
3.5
Δ
\Delta
-24.0
+10.5
+10.5
+4.4
+4.3
-1.2
-1.3
+9.0
+9.0
GPT-OSS-20B-high
89.5
6.2
6.2
12.7
13.0
23.3
23.3
3.9
3.9
GPT-OSS-120B-high
93.0
4.5
4.5
5.0
5.0
16.2
16.2
3.5
3.5
Δ
\Delta
-3.5
+1.8
+1.7
+7.7
+8.0
+7.1
+7.0
+0.4
+0.4
Self-Consistency
Qwen2.5-7B
17.0
20.0
18.8
12.3
16.0
20.0
18.8
19.5
20.2
Qwen2.5-72B
36.5
14.5
11.8
12.3
16.0
14.5
11.8
12.3
16.0
Δ
\Delta
-19.5
+5.5
+7.0
0.0
0.0
+5.5
+7.0
+7.2
+4.2
Llama3.1-8B
9.5
7.8
5.3
6.5
7.0
7.8
5.3
6.5
7.0
Llama3.1-70B
22.5
8.5
8.8
7.2
11.9
8.5
8.8
7.2
11.9
Δ
\Delta
-13.0
-0.7
-3.5
-0.8
-4.9
-0.7
-3.5
-0.8
-4.9
Qwen3-8B-nothink
38.5
17.0
7.6
11.8
10.1
17.0
8.6
21.9
21.9
Qwen3-8B-think
77.0
12.5
15.3
22.4
33.7
9.8
9.0
9.2
8.8
Δ
\Delta
-38.5
+4.5
-7.8
-10.6
-23.6
+7.2
-0.4
+12.7
+13.1
Qwen3-32B-nothink
47.0
16.4
8.8
9.1
10.1
16.4
8.8
20.9
27.0
Qwen3-32B-think
85.5
11.8
17.4
22.0
33.5
10.0
8.0
9.4
9.3
Δ
\Delta
-38.5
+4.6
-8.7
-12.8
-23.4
+6.4
+0.8
+11.5
+17.7
GPT-OSS-20B-low
59.5
16.1
18.1
13.2
19.0
16.3
18.7
26.6
43.6
GPT-OSS-20B-high
89.5
16.9
27.2
26.6
43.7
12.3
9.3
10.7
19.2
Δ
\Delta
-30.0
-0.7
-9.0
-13.3
-24.6
+4.0
+9.4
+15.8
+24.3
GPT-OSS-120B-low
69.0
19.2
17.4
16.9
20.1
19.6
18.9
24.2
35.7
GPT-OSS-120B-high
93.0
10.6
18.6
18.4
31.7
8.4
8.7
10.4
17.3
Δ
\Delta
-24.0
+8.5
-1.3
-1.5
-11.6
+11.1
+10.2
+13.8
+18.4
GPT-OSS-20B-high
89.5
16.9
27.2
26.6
43.7
12.3
9.3
10.7
19.2
GPT-OSS-120B-high
93.0
10.6
18.6
18.4
31.7
8.4
8.7
10.4
17.3
Δ
\Delta
-3.5
+6.2
+8.5
+8.2
+12.0
+3.9
+0.7
+0.3
+1.9
Table 15:
Calibration metrics on
LiveBench
. For calibration metrics (Brier, ECE), lower is better (
↓
\downarrow
).
Δ
\Delta
rows show the difference (Model
1
−
-
Model
2
).
Green
: better;
Red
: worse.
Model
Acc
Raw
CA
DA
IA
Brier
ECE
Brier
ECE
Brier
ECE
Brier
ECE
Verbalize
Qwen2.5-7B
49.0
43.6
44.8
33.9
34.2
43.6
44.8
28.4
28.3
Qwen2.5-72B
71.6
23.9
23.0
30.9
31.1
42.1
43.6
27.7
28.0
Δ
\Delta
-22.6
+19.7
+21.8
+3.1
+3.0
+1.5
+1.2
+0.8
+0.3
Llama3.1-8B
31.6
56.7
57.3
47.3
47.5
57.0
57.7
48.8
49.4
Llama3.1-70B
57.6
28.3
28.5
28.3
28.5
39.5
40.2
33.3
34.1
Δ
\Delta
-26.0
+28.4
+28.8
+19.0
+19.0
+17.5
+17.4
+15.6
+15.3
Qwen3-8B-nothink
70.9
25.2
25.1
19.2
19.1
25.2
25.1
12.6
11.4
Qwen3-8B-think
85.6
13.1
12.6
16.5
16.3
25.9
26.1
13.0
12.7
Δ
\Delta
-14.7
+12.1
+12.5
+2.7
+2.8
-0.6
-0.9
-0.5
-1.3
Qwen3-32B-nothink
76.6
18.7
18.1
14.4
13.7
18.7
18.1
9.6
8.0
Qwen3-32B-think
88.6
11.2
10.5
15.2
14.4
21.2
21.0
10.6
10.0
Δ
\Delta
-12.0
+7.5
+7.6
-0.8
-0.7
-2.5
-2.9
-1.0
-2.0
GPT-OSS-20B-low
74.8
15.9
12.1
12.8
9.1
16.0
12.2
9.1
4.9
GPT-OSS-20B-high
86.7
10.5
7.9
12.4
9.7
20.3
19.0
10.1
7.7
Δ
\Delta
-11.9
+5.3
+4.2
+0.4
-0.6
-4.3
-6.9
-1.0
-2.9
GPT-OSS-120B-low
85.2
10.6
6.6
10.0
6.7
10.6
6.6
7.3
3.2
GPT-OSS-120B-high
88.2
8.9
6.3
9.1
6.1
11.2
9.0
7.4
5.0
Δ
\Delta
-3.0
+1.7
+0.3
+0.9
+0.7
-0.6
-2.4
-0.1
-1.8
GPT-OSS-20B-high
86.7
10.5
7.9
12.4
9.7
20.3
19.0
10.1
7.7
GPT-OSS-120B-high
88.2
8.9
6.3
9.1
6.1
11.2
9.0
7.4
5.0
Δ
\Delta
-1.5
+1.7
+1.6
+3.3
+3.7
+9.1
+10.1
+2.7
+2.8
P(True)
Qwen2.5-7B
49.0
33.7
32.7
29.4
28.3
33.7
32.7
26.1
25.3
Qwen2.5-72B
71.6
20.6
19.2
21.1
19.5
31.4
30.6
20.9
20.0
Δ
\Delta
-22.6
+13.0
+13.5
+8.3
+8.8
+2.2
+2.1
+5.2
+5.3
Llama3.1-8B
31.6
28.6
25.6
28.9
19.9
28.6
25.6
25.8
18.9
Llama3.1-70B
57.6
27.5
26.0
28.3
28.1
40.6
43.2
34.6
37.0
Δ
\Delta
-26.0
+1.1
-0.4
+0.6
-8.2
-11.9
-17.6
-8.9
-18.2
Qwen3-8B-nothink
70.9
23.4
21.3
20.3
19.2
23.4
21.3
16.2
15.2
Qwen3-8B-think
85.6
19.7
19.6
20.3
19.8
30.3
29.2
19.5
19.4
Δ
\Delta
-14.7
+3.7
+1.7
+0.0
-0.6
-6.9
-7.8
-3.3
-4.2
Qwen3-32B-nothink
76.6
14.9
11.3
13.0
10.7
14.9
11.3
12.2
11.6
Qwen3-32B-think
88.6
13.0
13.1
15.3
15.2
22.9
22.8
12.7
12.7
Δ
\Delta
-12.0
+1.9
-1.7
-2.3
-4.5
-8.0
-11.5
-0.5
-1.1
GPT-OSS-20B-low
74.8
20.1
19.9
30.1
30.0
20.1
19.9
13.6
13.6
GPT-OSS-20B-high
86.7
16.1
16.2
14.7
14.7
25.3
25.3
15.6
15.7
Δ
\Delta
-11.9
+4.0
+3.7
+15.4
+15.2
-5.2
-5.4
-2.1
-2.1
GPT-OSS-120B-low
85.2
14.5
14.6
15.4
15.3
14.5
14.6
10.0
10.0
GPT-OSS-120B-high
88.2
21.7
21.8
17.2
17.3
23.4
23.5
20.2
20.2
Δ
\Delta
-3.0
-7.2
-7.2
-1.8
-2.0
-8.9
-8.9
-10.2
-10.2
GPT-OSS-20B-high
86.7
16.1
16.2
14.7
14.7
25.3
25.3
15.6
15.7
GPT-OSS-120B-high
88.2
21.7
21.8
17.2
17.3
23.4
23.5
20.2
20.2
Δ
\Delta
-1.5
-5.6
-5.6
-2.5
-2.5
+1.9
+1.8
-4.5
-4.5
Self-Consistency
Qwen2.5-7B
49.0
19.5
13.6
11.0
8.9
19.5
13.6
16.2
6.1
Qwen2.5-72B
71.6
12.8
6.3
14.6
9.7
19.3
19.4
13.6
13.4
Δ
\Delta
-22.6
+6.7
+7.3
-3.6
-0.8
+0.2
-5.9
+2.6
-7.2
Llama3.1-8B
31.6
16.1
6.8
9.9
7.4
16.1
6.7
14.9
5.7
Llama3.1-70B
57.6
13.1
5.0
16.5
13.1
14.9
15.8
12.5
14.5
Δ
\Delta
-26.0
+3.0
+1.8
-6.6
-5.7
+1.2
-9.1
+2.4
-8.8
Qwen3-8B-nothink
70.9
11.5
4.8
7.8
4.5
11.5
4.8
9.1
5.3
Qwen3-8B-think
85.6
9.2
6.9
9.7
5.7
17.0
16.9
8.9
8.9
Δ
\Delta
-14.7
+2.3
-2.0
-1.9
-1.2
-5.5
-12.1
+0.2
-3.6
Qwen3-32B-nothink
76.6
9.0
4.1
6.3
3.5
9.0
4.1
7.6
4.9
Qwen3-32B-think
88.6
7.1
5.0
7.7
4.6
13.3
12.9
6.9
6.3
Δ
\Delta
-12.0
+1.9
-0.9
-1.5
-1.1
-4.3
-8.8
+0.8
-1.4
GPT-OSS-20B-low
74.8
10.1
4.6
7.2
4.4
10.1
4.6
8.8
5.5
GPT-OSS-20B-high
86.7
8.3
6.5
8.6
4.7
14.7
14.6
8.3
8.0
Δ
\Delta
-11.9
+1.8
-1.9
-1.4
-0.2
-4.6
-10.0
+0.5
-2.5
GPT-OSS-120B-low
85.2
9.0
6.3
7.2
5.1
9.0
6.3
7.3
5.2
GPT-OSS-120B-high
88.2
7.5
6.5
7.6
5.0
9.2
8.6
6.6
6.5
Δ
\Delta
-3.0
+1.6
-0.2
-0.4
+0.0
-0.2
-2.2
+0.8
-1.2
GPT-OSS-20B-high
86.7
8.3
6.5
8.6
4.7
14.7
14.6
8.3
8.0
GPT-OSS-120B-high
88.2
7.5
6.5
7.6
5.0
9.2
8.6
6.6
6.5
Δ
\Delta
-1.5
+0.8
0.0
+1.0
-0.4
+5.4
+6.1
+1.7
+1.6
Table 16:
Calibration metrics on
MMLU-Pro
. For calibration metrics (Brier, ECE), lower is better (
↓
\downarrow
).
Δ
\Delta
rows show the difference (Model
1
−
-
Model
2
).
Green
: better;
Red
: worse.