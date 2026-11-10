---
title: 'Decomposing Probabilistic Scores: Reliability, Information Loss and Uncertainty(Supplementary
  Material)'
id: decomposing-probabilistic-scores-reliability-information-loss-and-uncertaintysup
tags:
- code-llm-confidence-positioning-d82d00
- calibration-theory
- proper-scoring-rules
- f-related
- grouping-loss
created: '2026-11-09T23:08:33.769057Z'
updated: '2026-11-09T23:27:44.470855Z'
source: https://arxiv.org/html/2603.15232
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:33.768715Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv HTML v2, Mar 2026; Charpentier and Fernandes Machado).
  Decomposition identities for arbitrary proper losses: expected loss at information
  level A = proper regret (reliability) + conditional entropy; nested levels give
  a chain decomposition; for classifier score S=s(X) a three-term identity miscalibration
  + grouping (information loss X to S) + irreducible uncertainty (Thm 2.1-2.6, Def
  3.1 perfect calibration P(Y|S)=S, Prop 3.2). Explicit Brier/log-loss forms, post-hoc
  recalibration, aggregation (calibration not preserved), boosting; synthetic plus
  GermanCredit case study. No LLM, code, or execution content. CLOSE to F only as
  a theoretical vocabulary (calibration relative to information level); does not occupy
  a metrology framing for code-LLM confidence. Companion abstract note: 260315232-decomposing-probabilistic-scores-reliability-information-loss-and-unce.'
---

Decomposing Probabilistic Scores: Reliability, Information Loss and Uncertainty(Supplementary Material)
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2603.15232v2 [cs.LG] 22 Mar 2026
Decomposing Probabilistic Scores: Reliability, Information Loss and Uncertainty
(Supplementary Material)
Arthur Charpentier
Affiliation:
UQAM, Montréal, Canada
Affiliation:
Kyoto University, Japan
Correspondence to:
charpentier.arthur@uqam.ca
Agathe Fernandes Machado
Affiliation:
UQAM, Montréal, Canada
Abstract
Calibration is a conditional property that depends on the information retained by a predictor. We develop decomposition identities for arbitrary proper losses that make this dependence explicit. At any information level
𝒜
\mathcal{A}
, the expected loss of an
𝒜
\mathcal{A}
-measurable predictor splits into a proper-regret (reliability) term and a conditional entropy (residual uncertainty) term.
For nested levels
𝒜
⊆
ℬ
\mathcal{A}\subseteq\mathcal{B}
, a chain decomposition quantifies the information gain from
𝒜
\mathcal{A}
to
ℬ
\mathcal{B}
.
Applied to classification with features
𝑿
\boldsymbol{X}
and score
S
=
s
⁡
(
𝑿
)
S=s(\boldsymbol{X})
, this yields a three-term identity: miscalibration, a
grouping
term measuring information loss from
𝑿
\boldsymbol{X}
to
S
S
, and irreducible uncertainty at the feature level. We leverage the framework to analyze post-hoc recalibration, aggregation of calibrated models, and stagewise/boosting constructions, with explicit forms for Brier and log-loss.
1
Introduction
Probabilistic classifiers are increasingly deployed in settings where predicted probabilities directly drive downstream decisions (screening, triage, pricing, resource allocation).
In such pipelines, a number interpreted as a probability should support decision-theoretic reasoning, which motivates
calibration
: informally, among instances assigned probability
s
s
, the empirical frequency of the event should be close to
s
s
.
At the same time, models are trained and compared using
proper scoring rules
, which combine calibration and sharpness/refinement into a single expected loss.
A central message of this paper is that calibration is inherently
relative to an information level
.
A predictor typically compresses features
𝑿
\boldsymbol{X}
into a lower-dimensional score
S
=
s
⁡
(
𝑿
)
S=s(\boldsymbol{X})
.
Even if one post-processes
S
S
to make it calibrated, the compression
𝑿
↦
S
\boldsymbol{X}\mapsto S
can cause unavoidable information loss
[
Tasche, 2021
]
, invisible to calibration diagnostics alone.
Conversely, ensembling procedures (averaging, stacking, stagewise boosting) can improve an overall proper score while creating or amplifying miscalibration.
We develop decomposition identities for arbitrary proper losses making these trade-offs explicit and actionable.
1.1
Setup and notation
We work on a probability space
(
Ω
,
ℱ
,
ℙ
)
(\Omega,\mathcal{F},\mathbb{P})
.
The outcome
Y
:
Ω
→
𝒴
Y:\Omega\to\mathcal{Y}
takes values in a
finite
label set (binary
𝒴
=
{
0
,
1
}
\mathcal{Y}=\{0,1\}
, multi-class
𝒴
=
{
1
,
…
,
K
}
\mathcal{Y}=\{1,\dots,K\}
), and features are given by
𝑿
:
Ω
→
𝒳
\boldsymbol{X}:\Omega\to\mathcal{X}
. We denote by
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
the probability simplex.
A probabilistic classifier is a measurable map
s
:
𝒳
→
Δ
⁡
(
𝒴
)
s:\mathcal{X}\to\Delta(\mathcal{Y})
, and write
S
:=
s
⁡
(
𝑿
)
∈
Δ
⁡
(
𝒴
)
S:=s(\boldsymbol{X})\in\Delta(\mathcal{Y})
the induced random prediction.
Let
ℋ
𝑿
:=
σ
⁡
(
𝑿
)
\mathcal{H}_{\boldsymbol{X}}:=\sigma(\boldsymbol{X})
and
ℋ
S
:=
σ
⁡
(
S
)
⊆
ℋ
𝑿
\mathcal{H}_{S}:=\sigma(S)\subseteq\mathcal{H}_{\boldsymbol{X}}
.
For any sub-
σ
\sigma
-algebra
𝒜
⊆
ℱ
\mathcal{A}\subseteq\mathcal{F}
, we define the conditional law at level
𝒜
\mathcal{A}
by
Q
𝒜
:=
ℙ
(
Y
∈
⋅
∣
𝒜
)
∈
Δ
(
𝒴
)
,
Q_{\mathcal{A}}:=\mathbb{P}(Y\in\cdot\mid\mathcal{A})\in\Delta(\mathcal{Y}),
understood as a
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
-valued
𝒜
\mathcal{A}
-measurable random variable (up to a.s. equality).
We will repeatedly use
{
Q
:=
Q
ℋ
𝑿
=
ℙ
(
Y
∈
⋅
∣
𝑿
)
,
C
:=
Q
ℋ
S
=
ℙ
(
Y
∈
⋅
∣
S
)
,
\begin{cases}Q:=Q_{\mathcal{H}_{\boldsymbol{X}}}=\mathbb{P}(Y\in\cdot\mid\boldsymbol{X}),\\
C:=Q_{\mathcal{H}_{S}}=\mathbb{P}(Y\in\cdot\mid S),\end{cases}
where
Q
Q
is the
true conditional law at the feature level
and
C
C
is the
calibrated version
of the score.
Perfect calibration is the identity
S
=
C
S=C
almost surely (equivalently
ℙ
(
Y
∈
⋅
∣
S
)
=
S
\mathbb{P}(Y\in\cdot\mid S)=S
a.s.).
We evaluate probabilistic predictions with a loss
ℓ
:
Δ
⁡
(
𝒴
)
×
𝒴
→
ℝ
\ell:\Delta(\mathcal{Y})\times\mathcal{Y}\to\mathbb{R}
and its conditional risk (or
expected score
)
L
⁡
(
p
,
q
)
:=
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
,
p
,
q
∈
Δ
⁡
(
𝒴
)
.
L(p,q):=\mathbb{E}_{Y\sim q}\big[\ell(p,Y)\big],\qquad p,q\in\Delta(\mathcal{Y}).
When
ℓ
\ell
is proper, it induces a generalized entropy
ℰ
ℓ
​
(
q
)
:=
L
⁡
(
q
,
q
)
\mathcal{E}_{\ell}(q):=L(q,q)
and a nonnegative regret/divergence
d
ℓ
​
(
p
,
q
)
:=
L
⁡
(
p
,
q
)
−
ℰ
ℓ
​
(
q
)
d_{\ell}(p,q):=L(p,q)-\mathcal{E}_{\ell}(q)
.
Canonical examples include log-loss (yielding Kullback–Leibler divergence) and the Brier score (yielding squared Euclidean distance).
1.2
Related work
Proper scoring rules are classical tools for probabilistic forecasting and decision-theoretic evaluation
[
Gneiting et al., 2007
]
.
Decomposition ideas trace back to Murphy-type reliability–resolution–uncertainty identities and extensions to proper scores and multi-class settings
[
Bröcker, 2009
]
.
In machine learning, post-hoc recalibration methods such as Platt scaling and isotonic regression are widely used
[
Platt, 1999
]
, and recent work emphasizes how calibration interacts with training dynamics, early stopping, and refinement–calibrate phenomena
[
Kull and Flach, 2015
,
Dimitriadis et al., 2023
,
Berta et al., 2025
]
.
Ensembling and stagewise procedures complicate calibration: they may improve expected proper losses while degrading conditional reliability, motivating analysis beyond a single score.
Our key contribution is not the tower property, but an
information-level
view of proper-score decompositions that separates miscalibration from
information loss
induced by compression (e.g.,
𝑿
↦
S
\boldsymbol{X}\mapsto S
), a phenomenon invisible to calibration curves.
1.3
Contributions and organization
Contributions.
Our contributions are as follows.
-
Information-level decompositions for arbitrary proper losses.
We derive level and chain identities for
𝒜
⊆
ℬ
\mathcal{A}\subseteq\mathcal{B}
that split regret from conditional entropy. When applied to
ℋ
S
⊆
ℋ
𝑿
\mathcal{H}_{S}\subseteq\mathcal{H}_{\boldsymbol{X}}
, this specializes to the decomposition of
𝔼
⁡
[
ℓ
⁡
(
S
,
Y
)
]
\mathbb{E}[\ell(S,Y)]
used in
[
Perez-Lebel et al., 2023
]
into miscalibration, a
grouping
term measuring information loss
𝑿
→
S
\boldsymbol{X}\to S
, and irreducible feature-level uncertainty.
-
Implications for recalibration and ensembles.
We view recalibration as projection onto
σ
⁡
(
S
)
\sigma(S)
and characterize when aggregation breaks calibration and how stagewise/boosting trades reliability for refinement.
-
Concrete instantiations.
We derive closed forms for the Brier score and log-loss.
While our proofs rely on standard conditional expectation arguments, the contribution is an operational separation of three failure modes under
any
proper loss: (i)
reliability
(proper regret at the score level), (ii)
information loss
induced by compression
𝑿
→
S
\boldsymbol{X}\!\to\!S
(grouping), and (iii)
irreducible
uncertainty at the feature level. This yields actionable guidance: post-hoc recalibration can only reduce (i); to reduce (ii) one must change the score/representation (retain more information);
and (iii) can only be reduced by richer features or better data.
Organization.
Section
2
presents the one-level and chain decompositions and interprets them for probabilistic classification.
Section
3
discusses global balance versus calibration and practical diagnostics.
Section
4
studies post-hoc recalibration under proper losses.
Section
5
covers aggregation and stagewise/boosting constructions and illustrates the framework
on Brier and log-loss.
2
Decompositions
2.1
General Decompositions
Theorem 2.1
.
Let
𝒜
⊆
ℱ
\mathcal{A}\subseteq\mathcal{F}
and let
T
T
be a
𝒜
\mathcal{A}
-measurable random variable taking values in
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
. Then
𝔼
⁡
[
ℓ
⁡
(
T
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
T
,
Q
𝒜
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Q
𝒜
)
]
.
\mathbb{E}\big[\ell(T,Y)\big]=\mathbb{E}\big[d_{\ell}(T,Q_{\mathcal{A}})\big]+\mathbb{E}\big[\mathcal{E}_{\ell}(Q_{\mathcal{A}})\big].
The first term
𝔼
⁡
[
d
ℓ
​
(
T
,
Q
𝒜
)
]
\mathbb{E}[d_{\ell}(T,Q_{\mathcal{A}})]
is a
measurable regret
at information level
𝒜
\mathcal{A}
(and becomes a calibration/reliability term when
𝒜
=
ℋ
T
\mathcal{A}=\mathcal{H}_{T}
).
The second term
𝔼
⁡
[
ℰ
ℓ
​
(
Q
𝒜
)
]
\mathbb{E}[\mathcal{E}_{\ell}(Q_{\mathcal{A}})]
is the
residual uncertainty
(or Bayes risk) given
𝒜
\mathcal{A}
.
When
ℓ
\ell
is (strictly) proper,
d
ℓ
​
(
⋅
,
⋅
)
≥
0
d_{\ell}(\cdot,\cdot)\geq 0
(and
d
ℓ
​
(
p
,
q
)
=
0
d_{\ell}(p,q)=0
iff
p
=
q
p=q
), so each regret term quantifies a genuine loss relative to the best predictor available at that information level.
Theorem 2.2
(Chain decomposition for nested information levels)
.
Let
𝒜
⊆
ℬ
⊆
ℱ
\mathcal{A}\subseteq\mathcal{B}\subseteq\mathcal{F}
and let
T
T
be a
𝒜
\mathcal{A}
-measurable random variable taking values in
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
. Then
𝔼
⁡
[
ℓ
⁡
(
T
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
T
,
Q
𝒜
)
]
+
𝔼
⁡
[
d
ℓ
​
(
Q
𝒜
,
Q
ℬ
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Q
ℬ
)
]
.
\mathbb{E}[\ell(T,Y)]=\mathbb{E}\big[d_{\ell}(T,Q_{\mathcal{A}})\big]+\mathbb{E}\big[d_{\ell}(Q_{\mathcal{A}},Q_{\mathcal{B}})\big]+\mathbb{E}\big[\mathcal{E}_{\ell}(Q_{\mathcal{B}})\big].
2.2
Back to Calibration
Take
T
=
S
T=S
,
𝒜
=
ℋ
S
\mathcal{A}=\mathcal{H}_{S}
, and
ℬ
=
ℋ
𝑿
\mathcal{B}=\mathcal{H}_{\boldsymbol{X}}
.
Then
Q
𝒜
=
C
Q_{\mathcal{A}}=C
and
Q
ℬ
=
Q
Q_{\mathcal{B}}=Q
, hence
𝔼
⁡
[
ℓ
⁡
(
S
,
Y
)
]
\displaystyle\mathbb{E}[\ell(S,Y)]
=
𝔼
​
[
d
ℓ
​
(
S
,
C
)
]
⏟
calibration / reliability
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
Q
)
]
⏟
grouping (information loss from
𝑿
to
S
)
\displaystyle=\underbrace{\mathbb{E}[d_{\ell}(S,C)]}_{\text{calibration / reliability}}+\underbrace{\mathbb{E}[d_{\ell}(C,Q)]}_{\text{grouping (information loss from $\boldsymbol{X}$ to $S$)}}
+
𝔼
​
[
ℰ
ℓ
​
(
Q
)
]
⏟
irreducible at the
𝑿
level
.
\displaystyle+\underbrace{\mathbb{E}[\mathcal{E}_{\ell}(Q)]}_{\text{irreducible at the $\boldsymbol{X}$ level}}.
(1)
Equation (
1
) is reminiscent of classical reliability–resolution–uncertainty decompositions, but here it arises as a special case of a general
information-level chain rule
valid for arbitrary proper losses, and the middle term admits a direct interpretation as the
information loss
by the compression
𝑿
→
S
\boldsymbol{X}\!\to\!S
, which is precisely what governs what recalibration and ensemble projections can (and cannot) fix, as mentioned in
[
Tasche, 2021
,
Perez-Lebel et al., 2023
]
.
Lemma 2.3
(When does the grouping term vanish?)
.
Assume
ℓ
\ell
is strictly proper. Then
𝔼
⁡
[
d
ℓ
​
(
C
,
Q
)
]
=
0
\mathbb{E}[d_{\ell}(C,Q)]=0
if and only if
C
=
Q
C=Q
almost surely.
Equivalently, the “true” conditional law
Q
=
ℙ
(
Y
∈
⋅
∣
𝐗
)
Q=\mathbb{P}(Y\in\cdot\mid\boldsymbol{X})
is
σ
⁡
(
S
)
\sigma(S)
-measurable
(i.e.,
S
S
is sufficient for
𝐗
\boldsymbol{X}
with respect to predicting
Y
Y
).
Example 2.4
(Perfect calibration does not prevent large information loss)
.
Consider binary
Y
∈
{
0
,
1
}
Y\in\{0,1\}
. Let
X
∈
{
1
,
2
}
X\in\{1,2\}
with
ℙ
⁡
(
X
=
1
)
=
ℙ
⁡
(
X
=
2
)
=
1
/
2
\mathbb{P}(X=1)=\mathbb{P}(X=2)=1/2
,
and
ℙ
⁡
(
Y
=
1
∣
X
=
1
)
=
0.9
,
ℙ
⁡
(
Y
=
1
∣
X
=
2
)
=
0.1
.
\mathbb{P}(Y=1\mid X=1)=0.9,\qquad\mathbb{P}(Y=1\mid X=2)=0.1.
Define the constant score
S
≡
1
/
2
S\equiv 1/2
. Then
C
=
𝔼
⁡
[
Y
∣
S
]
=
1
/
2
=
S
C=\mathbb{E}[Y\mid S]=1/2=S
,
so
S
S
is perfectly calibrated and the reliability term vanishes.
However, the true conditional law
Q
=
𝔼
⁡
[
Y
∣
X
]
Q=\mathbb{E}[Y\mid X]
takes values
0.9
0.9
or
0.1
0.1
,
so the grouping term is strictly positive. For the Brier loss,
𝔼
⁡
[
(
C
−
Q
)
2
]
=
1
2
​
(
0.5
−
0.9
)
2
+
1
2
​
(
0.5
−
0.1
)
2
=
0.16
,
\mathbb{E}[(C-Q)^{2}]=\tfrac{1}{2}(0.5-0.9)^{2}+\tfrac{1}{2}(0.5-0.1)^{2}=0.16,
and for the log-loss,
𝔼
[
KL
(
Q
∥
C
)
]
\displaystyle\mathbb{E}[\mathrm{KL}(Q\|C)]
=
1
2
KL
(
Bern
(
0.9
)
∥
Bern
(
0.5
)
)
\displaystyle=\tfrac{1}{2}\mathrm{KL}(\mathrm{Bern}(0.9)\|\mathrm{Bern}(0.5))
+
1
2
KL
(
Bern
(
0.1
)
∥
Bern
(
0.5
)
)
.
\displaystyle+\tfrac{1}{2}\mathrm{KL}(\mathrm{Bern}(0.1)\|\mathrm{Bern}(0.5)).
Thus, calibration alone is compatible with severe information loss (no discrimination).
Post-hoc recalibration ideally reduces the term
𝔼
​
[
d
ℓ
​
(
S
,
C
)
]
\mathbb{E}[d_{\ell}(S,C)]
, but without changing discrimination, it cannot directly reduce the grouping term
𝔼
​
[
d
ℓ
​
(
C
,
Q
)
]
\mathbb{E}[d_{\ell}(C,Q)]
.
This tension lies at the heart of recent analyses of training dynamics and early stopping
[
Berta et al., 2025
]
.
[
Bröcker, 2009
]
generalizes the reliability/resolution decomposition to the multi-class case and to proper scores.
In our loss-based formalism, one may write an “uncertainty + reliability
−
-
resolution” form by introducing the marginal
Q
¯
:=
ℙ
(
Y
∈
⋅
)
\bar{Q}:=\mathbb{P}(Y\in\cdot)
(coined the “climatology” in
[
Gneiting et al., 2007
]
).
Proposition 2.5
(Uncertainty–resolution–reliability form)
.
Let
S
S
be a prediction and let
C
=
ℙ
(
Y
∈
⋅
∣
S
)
C=\mathbb{P}(Y\in\cdot\mid S)
.
Then
𝔼
⁡
[
ℓ
⁡
(
S
,
Y
)
]
=
ℰ
ℓ
​
(
Q
¯
)
−
𝔼
⁡
[
d
ℓ
​
(
Q
¯
,
C
)
]
+
𝔼
⁡
[
d
ℓ
​
(
S
,
C
)
]
,
\mathbb{E}[\ell(S,Y)]=\mathcal{E}_{\ell}(\bar{Q})-\mathbb{E}\big[d_{\ell}(\bar{Q},C)\big]+\mathbb{E}\big[d_{\ell}(S,C)\big],
where
𝔼
​
[
d
ℓ
​
(
Q
¯
,
C
)
]
\mathbb{E}[d_{\ell}(\bar{Q},C)]
plays the role of resolution (information gain relative to climatology) and
𝔼
​
[
d
ℓ
​
(
S
,
C
)
]
\mathbb{E}[d_{\ell}(S,C)]
that of reliability.
2.3
Fundamental uncertainty
We introduce a latent variable
Z
Z
(state of the world) and the
objective chance
Π
:=
ℙ
(
Y
∈
⋅
∣
Z
)
∈
Δ
(
𝒴
)
.
\Pi:=\mathbb{P}(Y\in\cdot\mid Z)\in\Delta(\mathcal{Y}).
The object
Π
\Pi
formalizes the idea of a “true probability” that may vary across individuals/situations even at fixed
𝑿
\boldsymbol{X}
(unobserved covariates, non-stationarity, partially observed causal mechanisms, etc.).
Taking the nested chain
ℋ
S
⊆
ℋ
𝑿
⊆
ℋ
Z
\mathcal{H}_{S}\subseteq\mathcal{H}_{\boldsymbol{X}}\subseteq\mathcal{H}_{Z}
,
Theorem
2.2
can be iterated and yields a four-term decomposition.
Theorem 2.6
.
Assume
ℋ
S
⊆
ℋ
𝐗
⊆
ℋ
Z
\mathcal{H}_{S}\subseteq\mathcal{H}_{\boldsymbol{X}}\subseteq\mathcal{H}_{Z}
. Then
𝔼
⁡
[
ℓ
⁡
(
S
,
Y
)
]
\displaystyle\mathbb{E}[\ell(S,Y)]
=
𝔼
⁡
[
d
ℓ
​
(
S
,
C
)
]
+
𝔼
⁡
[
d
ℓ
​
(
C
,
Q
)
]
\displaystyle=\mathbb{E}[d_{\ell}(S,C)]+\mathbb{E}[d_{\ell}(C,Q)]
+
𝔼
⁡
[
d
ℓ
​
(
Q
,
Π
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Π
)
]
.
\displaystyle+\mathbb{E}[d_{\ell}(Q,\Pi)]+\mathbb{E}[\mathcal{E}_{\ell}(\Pi)].
We have here the following interpretations,
•
𝔼
​
[
d
ℓ
​
(
S
,
C
)
]
\mathbb{E}[d_{\ell}(S,C)]
:
miscalibration
(lack of reliability).
•
𝔼
​
[
d
ℓ
​
(
C
,
Q
)
]
\mathbb{E}[d_{\ell}(C,Q)]
:
grouping
/ information loss induced by the map
𝑿
↦
S
\boldsymbol{X}\mapsto S
(even if perfectly calibrated,
S
S
may still “collapse” heterogeneity).
•
𝔼
​
[
d
ℓ
​
(
Q
,
Π
)
]
\mathbb{E}[d_{\ell}(Q,\Pi)]
:
chance heterogeneity
remaining at the
𝑿
\boldsymbol{X}
information level (the true probability is not identified by
𝑿
\boldsymbol{X}
).
•
𝔼
​
[
ℰ
ℓ
​
(
Π
)
]
\mathbb{E}[\mathcal{E}_{\ell}(\Pi)]
:
intrinsic noise
at the
Z
Z
level (what cannot be reduced even with
Z
Z
).
This clarifies that the “irreducible” component is relative to the observability level (here
𝑿
\boldsymbol{X}
), as already discussed in epistemic/aleatoric decompositions
[
Kull and Flach, 2015
]
.
Let
k
=
2
k=2
and identify
p
∈
Δ
⁡
(
𝒴
)
p\in\Delta(\mathcal{Y})
with
p
=
ℙ
⁡
(
Y
=
1
)
p=\mathbb{P}(Y=1)
.
We recover the same results as in
[
Tasche, 2021
]
when considering the special case of the Brier loss,
ℓ
⁡
(
p
,
y
)
=
(
p
−
y
)
2
\ell(p,y)=(p-y)^{2}
.
Corollary 2.7
(Variance-type decomposition (Brier))
.
In the binary case, with
C
=
𝔼
⁡
[
Y
∣
S
]
C=\mathbb{E}[Y\mid S]
and
Q
=
𝔼
⁡
[
Y
∣
𝐗
]
Q=\mathbb{E}[Y\mid\boldsymbol{X}]
,
𝔼
⁡
[
(
S
−
Y
)
2
]
=
𝔼
⁡
[
(
S
−
C
)
2
]
+
𝔼
⁡
[
(
C
−
Q
)
2
]
+
𝔼
⁡
[
Q
⁡
(
1
−
Q
)
]
.
\mathbb{E}[(S-Y)^{2}]=\mathbb{E}[(S-C)^{2}]+\mathbb{E}[(C-Q)^{2}]+\mathbb{E}[Q(1-Q)].
If moreover
Π
=
𝔼
⁡
[
Y
∣
Z
]
\Pi=\mathbb{E}[Y\mid Z]
, then
𝔼
⁡
[
Q
⁡
(
1
−
Q
)
]
=
𝔼
⁡
[
(
Q
−
Π
)
2
]
+
𝔼
⁡
[
Π
⁡
(
1
−
Π
)
]
.
\mathbb{E}[Q(1-Q)]=\mathbb{E}[(Q-\Pi)^{2}]+\mathbb{E}[\Pi(1-\Pi)].
In the binary Brier case,
Q
=
𝔼
⁡
[
Y
∣
X
]
Q=\mathbb{E}[Y\mid X]
and
C
=
𝔼
⁡
[
Y
∣
S
]
C=\mathbb{E}[Y\mid S]
satisfy
C
=
𝔼
⁡
[
Q
∣
S
]
C=\mathbb{E}[Q\mid S]
. Hence
𝔼
⁡
[
(
C
−
Q
)
2
]
=
𝔼
⁡
[
Var
⁡
(
Q
∣
S
)
]
,
\mathbb{E}[(C-Q)^{2}]=\mathbb{E}\left[\mathrm{Var}(Q\mid S)\right],
i.e., the grouping term is the expected conditional variance of the Bayes score
Q
Q
after compressing
𝑿
↦
S
\boldsymbol{X}\mapsto S
. Equivalently, by the law of total variance,
𝔼
⁡
[
C
⁡
(
1
−
C
)
]
=
𝔼
⁡
[
Q
⁡
(
1
−
Q
)
]
+
𝔼
⁡
[
(
C
−
Q
)
2
]
,
\mathbb{E}[C(1-C)]=\mathbb{E}[Q(1-Q)]+\mathbb{E}[(C-Q)^{2}],
so moving from
ℋ
X
\mathcal{H}_{X}
to
ℋ
S
\mathcal{H}_{S}
increases residual uncertainty exactly by the information-loss term
𝔼
⁡
[
(
C
−
Q
)
2
]
\mathbb{E}[(C-Q)^{2}]
.
Corollary 2.8
(Log-loss: entropies and information)
.
Assume the log-loss
ℓ
log
​
(
p
,
y
)
:=
−
log
⁡
p
y
\ell_{\log}(p,y):=-\log p_{y}
on a finite label set.
Then the induced divergence and generalized entropy are
d
log
(
p
,
q
)
=
KL
(
q
∥
p
)
d_{\log}(p,q)=\mathrm{KL}(q\|p)
and
E
log
​
(
q
)
=
H
​
(
q
)
\mathrm{E}_{\log}(q)=H(q)
.
For any
𝒜
⊆
ℬ
⊆
ℱ
\mathcal{A}\subseteq\mathcal{B}\subseteq\mathcal{F}
and any
𝒜
\mathcal{A}
-measurable predictor
T
:
Ω
→
Δ
⁡
(
𝒴
)
T:\Omega\to\Delta(\mathcal{Y})
,
𝔼
[
ℓ
log
(
T
,
Y
)
]
=
𝔼
[
KL
(
Q
𝒜
∥
T
)
]
+
𝔼
[
KL
(
Q
ℬ
∥
Q
𝒜
)
]
+
H
(
Y
∣
ℬ
)
,
\mathbb{E}[\ell_{\log}(T,Y)]=\mathbb{E}\left[\mathrm{KL}(Q_{\mathcal{A}}\|T)\right]+\mathbb{E}\left[\mathrm{KL}(Q_{\mathcal{B}}\|Q_{\mathcal{A}})\right]+H(Y\mid\mathcal{B}),
where
H
⁡
(
Y
∣
ℬ
)
:=
𝔼
⁡
[
H
⁡
(
Q
ℬ
)
]
H(Y\mid\mathcal{B}):=\mathbb{E}\left[H(Q_{\mathcal{B}})\right]
.
Moreover,
𝔼
[
KL
(
Q
ℬ
∥
Q
𝒜
)
]
=
I
(
Y
;
ℬ
∣
𝒜
)
.
\mathbb{E}\left[\mathrm{KL}(Q_{\mathcal{B}}\|Q_{\mathcal{A}})\right]=I(Y;\mathcal{B}\mid\mathcal{A}).
In particular, with
𝒜
=
ℋ
S
\mathcal{A}=\mathcal{H}_{S}
and
ℬ
=
ℋ
X
\mathcal{B}=\mathcal{H}_{X}
,
𝔼
[
−
log
S
Y
]
=
𝔼
[
KL
(
C
∥
S
)
]
+
I
(
Y
;
X
∣
S
)
+
H
(
Y
∣
X
)
.
\mathbb{E}[-\log S_{Y}]=\mathbb{E}[\mathrm{KL}(C\|S)]+I(Y;X\mid S)+H(Y\mid X).
For the log-loss (cross-entropy),
d
d
becomes a Kullback–Leibler divergence and
ℰ
ℓ
\mathcal{E}_{\ell}
the Shannon entropy; the chain decomposition therefore links the expected loss to information-theoretic quantities.
This motivates diagnostics (Murphy diagrams, Murphy decomposition, etc.) and the “triptych” view of calibration/discrimination/performance
[
Dimitriadis et al., 2023
]
.
3
Well-calibration
3.1
Global balance (marginal calibration).
We call global balance the weak moment condition
𝔼
⁡
[
S
]
=
𝔼
⁡
[
onehot
⁡
(
Y
)
]
\mathbb{E}[S]=\mathbb{E}[\mathrm{onehot}(Y)]
(binary:
𝔼
⁡
[
S
]
=
𝔼
⁡
[
Y
]
\mathbb{E}[S]=\mathbb{E}[Y]
), where
onehot
⁡
(
Y
)
∈
Δ
⁡
(
𝒴
)
\mathrm{onehot}(Y)\in\Delta(\mathcal{Y})
is the one-hot encoding of
Y
Y
.
It is strictly weaker than calibration since it does not constrain the conditional relationship between
S
S
and
Y
Y
; in particular, intercept-corrections can enforce global balance on a validation split without guaranteeing
ℙ
(
Y
∈
⋅
∣
S
)
=
S
\mathbb{P}(Y\in\cdot\mid S)=S
.
We therefore focus on conditional calibration and proper-loss reliability.
3.2
Calibrated scores and a proper-loss notion of calibration error
Recall
Q
:=
ℙ
(
Y
∈
⋅
∣
𝑿
)
Q:=\mathbb{P}(Y\in\cdot\mid\boldsymbol{X})
and
C
:=
ℙ
(
Y
∈
⋅
∣
S
)
C:=\mathbb{P}(Y\in\cdot\mid S)
.
Perfect calibration holds when
S
=
C
S=C
almost surely.
Definition 3.1
(Perfect calibration)
.
We say that
S
S
is perfectly calibrated if
ℙ
(
Y
∈
⋅
∣
S
)
=
S
a.s.
,
\mathbb{P}(Y\in\cdot\mid S)=S\qquad\text{a.s.},
equivalently
C
=
S
C=S
a.s.
In the binary case, this is
𝔼
⁡
[
Y
∣
S
]
=
S
\mathbb{E}[Y\mid S]=S
a.s.
Proper losses provide a canonical
calibration error
(reliability) through the induced regret.
Recall
L
⁡
(
p
,
q
)
:=
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
L(p,q):=\mathbb{E}_{Y\sim q}[\ell(p,Y)]
,
ℰ
ℓ
​
(
q
)
:=
L
⁡
(
q
,
q
)
\mathcal{E}_{\ell}(q):=L(q,q)
, and
d
ℓ
​
(
p
,
q
)
:=
L
⁡
(
p
,
q
)
−
ℰ
ℓ
​
(
q
)
d_{\ell}(p,q):=L(p,q)-\mathcal{E}_{\ell}(q)
.
Proposition 3.2
(Calibration error as proper regret)
.
Let
ℓ
\ell
be a proper loss. For any score
S
S
and
C
=
ℙ
(
Y
∈
⋅
∣
S
)
C=\mathbb{P}(Y\in\cdot\mid S)
,
𝔼
⁡
[
ℓ
⁡
(
S
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
S
,
C
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
C
)
]
.
\mathbb{E}[\ell(S,Y)]=\mathbb{E}\big[d_{\ell}(S,C)\big]+\mathbb{E}\big[\mathcal{E}_{\ell}(C)\big].
In particular,
𝔼
⁡
[
d
ℓ
​
(
S
,
C
)
]
≥
0
\mathbb{E}[d_{\ell}(S,C)]\geq 0
, and if
ℓ
\ell
is strictly proper then
𝔼
⁡
[
d
ℓ
​
(
S
,
C
)
]
=
0
\mathbb{E}[d_{\ell}(S,C)]=0
iff
S
=
C
S=C
a.s.
Moreover, perfect calibration implies global balance:
𝔼
⁡
[
S
]
=
𝔼
⁡
[
onehot
⁡
(
Y
)
]
\mathbb{E}[S]=\mathbb{E}[\mathrm{onehot}(Y)]
.
3.3
Diagnostics and visualization
Empirical calibration assessment amounts to estimating the map
s
↦
ℙ
(
Y
∈
⋅
∣
S
=
s
)
s\mapsto\mathbb{P}(Y\in\cdot\mid S=s)
(or its binary analogue).
Reliability diagrams (binning
S
S
and plotting empirical frequencies) are intuitive but sensitive to bin choices.
Stable alternatives use a fixed estimation rule (e.g. isotonic regression in the binary case
[
Dimitriadis et al., 2021
]
), and can be combined with proper-score-based comparisons (e.g. Murphy-type diagrams and the “triptych” perspective) to separate reliability from refinement and overall performance.
In our notation, these diagnostics primarily target the reliability term
𝔼
​
[
d
ℓ
​
(
S
,
C
)
]
\mathbb{E}[d_{\ell}(S,C)]
and help distinguish miscalibration from information loss (grouping) and irreducible uncertainty.
Given test data
(
S
i
,
X
i
,
Y
i
)
i
=
1
n
(S_{i},X_{i},Y_{i})_{i=1}^{n}
, we estimate
C
(
s
)
=
P
(
Y
∈
⋅
∣
S
=
s
)
C(s)=P(Y\in\cdot\mid S=s)
by a recalibration fit
C
^
​
(
s
)
=
g
^
​
(
s
)
\widehat{C}(s)=\widehat{g}(s)
(estimated out-of-sample using an independent calibration split, or via cross-fitting). We then estimate reliability by
Rel
^
ℓ
:=
1
n
​
∑
i
=
1
n
d
ℓ
​
(
S
i
,
C
^
​
(
S
i
)
)
.
\widehat{\mathrm{Rel}}_{\ell}:=\frac{1}{n}\sum_{i=1}^{n}d_{\ell}(S_{i},\widehat{C}(S_{i})).
When a proxy
Q
^
(
X
)
≈
P
(
Y
∈
⋅
∣
X
)
\widehat{Q}(X)\approx P(Y\in\cdot\mid X)
is available (oracle in simulations, or a high-capacity reference model), we analogously estimate grouping and irreducible terms by
Grp
^
ℓ
:=
1
n
​
∑
i
d
ℓ
​
(
C
^
​
(
S
i
)
,
Q
^
​
(
X
i
)
)
\widehat{\mathrm{Grp}}_{\ell}:=\frac{1}{n}\sum_{i}d_{\ell}(\widehat{C}(S_{i}),\widehat{Q}(X_{i}))
and
Irr
^
ℓ
:=
1
n
​
∑
i
E
ℓ
​
(
Q
^
​
(
X
i
)
)
\widehat{\mathrm{Irr}}_{\ell}:=\frac{1}{n}\sum_{i}\mathrm{E}_{\ell}(\widehat{Q}(X_{i}))
.
[
Perez-Lebel et al., 2023
]
also propose estimating the lower bound of the grouping loss.
4
Recalibration
A (post-hoc) recalibrator produces an updated score
S
~
\widetilde{S}
that is measurable with respect to the original score information
σ
⁡
(
S
)
\sigma(S)
.
Equivalently, it restricts attention to predictors of the form
S
~
=
g
⁡
(
S
)
\widetilde{S}=g(S)
for a measurable map
g
:
Δ
⁡
(
𝒴
)
→
Δ
⁡
(
𝒴
)
g:\Delta(\mathcal{Y})\to\Delta(\mathcal{Y})
, so that
S
~
:=
g
⁡
(
S
)
,
σ
⁡
(
S
~
)
⊆
σ
⁡
(
S
)
.
\widetilde{S}:=g(S),\qquad\sigma(\widetilde{S})\subseteq\sigma(S).
In the binary case (
S
∈
[
0
,
1
]
S\in[0,1]
), one often restricts to non-decreasing
g
g
to preserve the ranking induced by
S
S
.
Practical note.
In practice
C
=
ℙ
(
Y
∈
⋅
∣
S
)
C=\mathbb{P}(Y\in\cdot\mid S)
is unknown and
g
g
is learned on held-out calibration data (or via cross-fitting); fitting
g
g
on the same data used to train the classifier can lead to overly optimistic calibration assessments.
Proposition 4.1
(Population-optimal recalibration
[
Berta et al., 2025
]
)
.
Assume
ℓ
\ell
is proper and consider the class of predictors that are
σ
⁡
(
S
)
\sigma(S)
-measurable, i.e. of the form
S
~
=
g
⁡
(
S
)
\widetilde{S}=g(S)
.
Then the population risk is minimized by
S
~
⋆
=
C
\widetilde{S}^{\star}=C
:
inf
g
:
Δ
⁡
(
𝒴
)
→
Δ
⁡
(
𝒴
)
{
𝔼
[
ℓ
(
g
(
S
)
,
Y
)
]
}
=
𝔼
[
ℓ
(
C
,
Y
)
]
=
𝔼
[
ℰ
ℓ
(
C
)
]
.
\inf_{g:\Delta(\mathcal{Y})\to\Delta(\mathcal{Y})}\big\{\mathbb{E}[\ell(g(S),Y)]\big\}=\mathbb{E}[\ell(C,Y)]=\mathbb{E}[\mathcal{E}_{\ell}(C)].
Moreover, the excess risk of any recalibrator
g
g
admits the decomposition
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
S
)
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
g
⁡
(
S
)
,
C
)
]
.
\mathbb{E}[\ell(g(S),Y)]-\mathbb{E}[\ell(C,Y)]=\mathbb{E}\big[d_{\ell}(g(S),C)\big].
What recalibration can and cannot fix.
By Proposition
4.1
, post-hoc recalibration can only improve the
reliability
term (it acts within the information level
σ
⁡
(
S
)
\sigma(S)
).
It cannot, without changing the underlying score, directly reduce the
grouping
term
𝔼
​
[
d
ℓ
​
(
C
,
Q
)
]
\mathbb{E}[d_{\ell}(C,Q)]
in (
1
), which quantifies information loss from
𝑿
\boldsymbol{X}
to
S
S
.
Why require
g
g
to be non-decreasing in the binary case?
Beyond reliability, many downstream uses of a score rely on
ranking
rather than on the absolute probability values: thresholding rules, ROC/AUC, or top-
k
k
selection.
Recalibration should ideally fix reliability
without harming discrimination
.
A minimal compatibility constraint is that
g
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
g:[0,1]\to[0,1]
be non-decreasing.
Proposition 4.2
(Monotone recalibration preserves threshold rules and ROC (up to ties))
.
Let
Y
∈
{
0
,
1
}
Y\in\{0,1\}
, let
S
∈
[
0
,
1
]
S\in[0,1]
, and let
g
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
g:[0,1]\to[0,1]
be non-decreasing.
Define
S
~
=
g
⁡
(
S
)
\widetilde{S}=g(S)
.
For any threshold
τ
∈
[
0
,
1
]
\tau\in[0,1]
, there exists
τ
′
∈
[
0
,
1
]
\tau^{\prime}\in[0,1]
such that
{
S
~
≥
τ
}
=
{
S
≥
τ
′
}
a.s.
\{\widetilde{S}\geq\tau\}=\{S\geq\tau^{\prime}\}\quad\text{a.s.}
Consequently, all threshold classifiers induced by
S
~
\widetilde{S}
are also induced by
S
S
, and the ROC curve (hence AUC) is unchanged by
g
g
up to tie-handling conventions.
This motivates isotonic regression and monotone smoothers as
order-consistent
calibrators: monotonicity preserves the weak order of
S
S
, while strict monotonicity on the support of
S
S
additionally avoids large flat regions.
Finite-sample validity (context).
Recalibration is typically justified as risk minimization under a proper loss (hence asymptotic/model-based guarantees).
A complementary line of work provides
finite-sample
validity under minimal assumptions, e.g. conformal prediction for set-valued outputs and Venn–Abers predictors for interval-valued probabilities
[
Vovk et al., 2005
,
Vovk and Petej, 2012
]
.
These methods highlight that formal guarantees often attach to the full object produced (set/interval), and may not be preserved by collapsing it to a single probability.
This reinforces a recurring theme of our analysis: calibration is a conditional property and can be fragile under post-processing and aggregation.
5
Calibration and Ensemble Learning
5.1
Aggregation: calibrated inputs do not imply a calibrated output
A common practice is to combine several probabilistic classifiers
S
(
1
)
,
…
,
S
(
M
)
∈
Δ
⁡
(
𝒴
)
S^{(1)},\dots,S^{(M)}\in\Delta(\mathcal{Y})
into an aggregated score
S
ens
=
A
⁡
(
𝐒
)
S^{\mathrm{ens}}=A(\mathbf{S})
where
𝐒
:=
(
S
(
1
)
,
…
,
S
(
M
)
)
\mathbf{S}:=(S^{(1)},\dots,S^{(M)})
and
A
A
is, e.g., averaging, stacking, or a learned combiner.
Even if each component is perfectly calibrated, calibration is generally
not
preserved by aggregation (see Proposition
5.1
, Figure
1
and
[
Gneiting and Ranjan, 2013
]
).
Building on the chain decomposition from Theorem
2.2
, to understand when calibration can be preserved, define the conditional laws
C
𝐒
:=
ℙ
(
Y
∈
⋅
∣
𝐒
)
,
C
ens
:=
ℙ
(
Y
∈
⋅
∣
S
ens
)
.
C_{\mathbf{S}}:=\mathbb{P}(Y\in\cdot\mid\mathbf{S}),\qquad C_{\mathrm{ens}}:=\mathbb{P}(Y\in\cdot\mid S^{\mathrm{ens}}).
By definition,
S
ens
S^{\mathrm{ens}}
is calibrated if and only if
C
ens
=
S
ens
C_{\mathrm{ens}}=S^{\mathrm{ens}}
almost surely.
Proposition 5.1
(When does an aggregator preserve calibration?)
.
Let
S
ens
=
A
⁡
(
𝐒
)
S^{\mathrm{ens}}=A(\mathbf{S})
and define
C
𝐒
C_{\mathbf{S}}
and
C
ens
C_{\mathrm{ens}}
as above.
If there exists a measurable map
φ
:
Δ
⁡
(
𝒴
)
→
Δ
⁡
(
𝒴
)
\varphi:\Delta(\mathcal{Y})\to\Delta(\mathcal{Y})
s.t.
C
𝐒
=
φ
⁡
(
S
ens
)
a.s.
,
C_{\mathbf{S}}=\varphi(S^{\mathrm{ens}})\quad\text{a.s.},
then
C
ens
=
φ
⁡
(
S
ens
)
C_{\mathrm{ens}}=\varphi(S^{\mathrm{ens}})
a.s. and
S
ens
S^{\mathrm{ens}}
is calibrated if and only if
φ
⁡
(
s
)
=
s
\varphi(s)=s
for
s
s
in the (essential) support of
S
ens
S^{\mathrm{ens}}
.
In the binary case, consider the average
S
¯
=
1
M
​
∑
m
=
1
M
S
(
m
)
\bar{S}=\frac{1}{M}\sum_{m=1}^{M}S^{(m)}
of
M
M
individually calibrated scores.
Then
S
¯
\bar{S}
is calibrated only if
ℙ
⁡
(
Y
=
1
∣
S
(
1
)
,
…
,
S
(
M
)
)
\mathbb{P}(Y=1\mid S^{(1)},\ldots,S^{(M)})
depends on
(
S
(
1
)
,
…
,
S
(
M
)
)
(S^{(1)},\ldots,S^{(M)})
only through
S
¯
\bar{S}
(i.e.,
S
¯
\bar{S}
is sufficient for
Y
Y
under the projection
(
S
(
1
)
,
…
,
S
(
M
)
)
↦
S
¯
(S^{(1)},\ldots,S^{(M)})\mapsto\bar{S}
).
Otherwise, averaging can destroy calibration even when each component is perfectly calibrated (Example
5.2
).
Example 5.2
(Two calibrated scores whose average is miscalibrated)
.
Let
Y
∈
{
0
,
1
}
Y\in\{0,1\}
and let
(
S
(
1
)
,
S
(
2
)
)
∈
{
0.25
,
0.75
}
2
(S^{(1)},S^{(2)})\in\{0.25,0.75\}^{2}
take the four values
(
0.25
,
0.25
)
,
(
0.25
,
0.75
)
,
(
0.75
,
0.25
)
,
(
0.75
,
0.75
)
(0.25,0.25),(0.25,0.75),(0.75,0.25),(0.75,0.75)
each with probability
1
/
4
1/4
.
Conditionally on
(
S
(
1
)
,
S
(
2
)
)
(S^{(1)},S^{(2)})
, let
Y
∼
Bern
⁡
(
m
)
Y\sim\mathrm{Bern}(m)
with
{
m
(
0.25
,
0.25
)
=
0
,
m
⁡
(
0.25
,
0.75
)
=
0.5
,
m
(
0.75
,
0.25
)
=
0.5
,
m
⁡
(
0.75
,
0.75
)
=
1
.
\begin{cases}m(0.25,0.25)=0,\quad&m(0.25,0.75)=0.5,\\
m(0.75,0.25)=0.5,\quad&m(0.75,0.75)=1.\end{cases}
Then one checks that
𝔼
⁡
[
Y
∣
S
(
1
)
]
=
S
(
1
)
\mathbb{E}[Y\mid S^{(1)}]=S^{(1)}
and
𝔼
⁡
[
Y
∣
S
(
2
)
]
=
S
(
2
)
\mathbb{E}[Y\mid S^{(2)}]=S^{(2)}
, so each component is perfectly calibrated.
However, for the average
S
¯
:=
1
2
​
(
S
(
1
)
+
S
(
2
)
)
\bar{S}:=\tfrac{1}{2}(S^{(1)}+S^{(2)})
, we have
ℙ
⁡
(
S
¯
=
0.25
)
=
1
/
4
\mathbb{P}(\bar{S}=0.25)=1/4
and
𝔼
⁡
[
Y
∣
S
¯
=
0.25
]
=
0
≠
0.25
\mathbb{E}[Y\mid\bar{S}=0.25]=0\neq 0.25
, so
S
¯
\bar{S}
is not calibrated. This illustrates that a projection
S
↦
A
⁡
(
S
)
S\mapsto A(S)
can destroy calibration even when each coordinate is calibrated.
If one keeps the full vector
𝐒
\mathbf{S}
, then the Bayes-optimal calibrated prediction at that information level is
C
𝐒
=
ℙ
(
Y
∈
⋅
∣
𝐒
)
C_{\mathbf{S}}=\mathbb{P}(Y\in\cdot\mid\mathbf{S})
(a “stacking” view).
If instead one outputs only
S
ens
S^{\mathrm{ens}}
, then post-hoc recalibration targets
C
ens
=
ℙ
(
Y
∈
⋅
∣
S
ens
)
C_{\mathrm{ens}}=\mathbb{P}(Y\in\cdot\mid S^{\mathrm{ens}})
but cannot recover information lost by the projection
𝐒
↦
S
ens
\mathbf{S}\mapsto S^{\mathrm{ens}}
.
5.2
Sequential ensembles and boosting: refinement as increasing information
Boosting builds predictors sequentially by adding weak learners, denoted
h
t
​
(
𝑿
)
h_{t}(\boldsymbol{X})
at step
t
t
.
A convenient abstraction focuses on the
information revealed across stages
: let
ℱ
t
:=
σ
⁡
(
h
1
​
(
𝑿
)
,
…
,
h
t
​
(
𝑿
)
)
,
\mathcal{F}_{t}:=\sigma\big(h_{1}(\boldsymbol{X}),\dots,h_{t}(\boldsymbol{X})\big),
with
ℱ
0
⊆
ℱ
1
⊆
⋯
⊆
ℱ
T
⊆
ℋ
𝑿
\mathcal{F}_{0}\subseteq\mathcal{F}_{1}\subseteq\cdots\subseteq\mathcal{F}_{T}\subseteq\mathcal{H}_{\boldsymbol{X}}
,
and define the Bayes-optimal prediction at level
ℱ
t
\mathcal{F}_{t}
by
Q
t
:=
ℙ
(
Y
∈
⋅
∣
ℱ
t
)
∈
Δ
(
𝒴
)
.
Q_{t}:=\mathbb{P}(Y\in\cdot\mid\mathcal{F}_{t})\in\Delta(\mathcal{Y}).
Each
Q
t
Q_{t}
is perfectly calibrated (by construction) and becomes more refined as
t
t
increases.
Theorem 5.3
(Telescoping decomposition along a filtration (proper losses))
.
Let
ℓ
\ell
be a proper loss with generalized entropy
ℰ
ℓ
\mathcal{E}_{\ell}
and induced divergence
d
ℓ
d_{\ell}
.
Let
ℱ
0
⊆
⋯
⊆
ℱ
T
\mathcal{F}_{0}\subseteq\cdots\subseteq\mathcal{F}_{T}
be a filtration and define
Q
t
:=
ℙ
(
Y
∈
⋅
∣
ℱ
t
)
Q_{t}:=\mathbb{P}(Y\in\cdot\mid\mathcal{F}_{t})
.
Then for any
ℱ
0
\mathcal{F}_{0}
-measurable predictor
T
:
Ω
→
Δ
⁡
(
𝒴
)
T:\Omega\to\Delta(\mathcal{Y})
,
𝔼
⁡
[
ℓ
⁡
(
T
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
T
,
Q
0
)
]
+
∑
t
=
0
T
−
1
𝔼
⁡
[
d
ℓ
​
(
Q
t
,
Q
t
+
1
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Q
T
)
]
.
\mathbb{E}[\ell(T,Y)]=\mathbb{E}[d_{\ell}(T,Q_{0})]+\sum_{t=0}^{T-1}\mathbb{E}[d_{\ell}(Q_{t},Q_{t+1})]+\mathbb{E}[\mathcal{E}_{\ell}(Q_{T})].
Corollary 5.4
(Log-loss along a filtration: information gains)
.
Under log-loss, increments in Theorem
5.3
satisfy
𝔼
[
d
log
(
Q
t
,
Q
t
+
1
)
]
=
𝔼
[
KL
(
Q
t
+
1
∥
Q
t
)
]
=
I
(
Y
;
ℱ
t
+
1
∣
ℱ
t
)
,
\mathbb{E}[d_{\log}(Q_{t},Q_{t+1})]=\mathbb{E}[\mathrm{KL}(Q_{t+1}\|Q_{t})]=I(Y;\mathcal{F}_{t+1}\mid\mathcal{F}_{t}),
and therefore
𝔼
​
[
ℓ
log
​
(
T
,
Y
)
]
\mathbb{E}[\ell_{\log}(T,Y)]
equals
𝔼
[
KL
(
Q
0
∥
T
)
]
+
∑
t
=
0
T
−
1
I
(
Y
;
ℱ
t
+
1
∣
ℱ
t
)
+
H
(
Y
∣
ℱ
T
)
.
\mathbb{E}[\mathrm{KL}(Q_{0}\|T)]+\sum_{t=0}^{T-1}I(Y;\mathcal{F}_{t+1}\mid\mathcal{F}_{t})+H(Y\mid\mathcal{F}_{T}).
Corollary 5.5
(Brier case: Pythagoras identity)
.
Assume
𝒴
=
{
0
,
1
}
\mathcal{Y}=\{0,1\}
and
ℓ
⁡
(
p
,
y
)
=
(
p
−
y
)
2
\ell(p,y)=(p-y)^{2}
.
Let
η
t
:=
𝔼
⁡
[
Y
∣
ℱ
t
]
∈
[
0
,
1
]
\eta_{t}:=\mathbb{E}[Y\mid\mathcal{F}_{t}]\in[0,1]
. Then
𝔼
⁡
[
(
Y
−
η
t
+
1
)
2
]
=
𝔼
⁡
[
(
Y
−
η
t
)
2
]
−
𝔼
⁡
[
(
η
t
+
1
−
η
t
)
2
]
,
\mathbb{E}[(Y-\eta_{t+1})^{2}]=\mathbb{E}[(Y-\eta_{t})^{2}]-\mathbb{E}[(\eta_{t+1}-\eta_{t})^{2}],
so the Brier risk decreases with
t
t
and the decrease equals the refinement gain
𝔼
⁡
[
(
η
t
+
1
−
η
t
)
2
]
\mathbb{E}[(\eta_{t+1}-\eta_{t})^{2}]
.
Martingale view (Brier).
The process
(
η
t
)
t
=
0
T
(\eta_{t})_{t=0}^{T}
is a bounded martingale with respect to
(
ℱ
t
)
(\mathcal{F}_{t})
since
𝔼
⁡
[
η
t
+
1
∣
ℱ
t
]
=
𝔼
⁡
[
𝔼
⁡
[
Y
∣
ℱ
t
+
1
]
∣
ℱ
t
]
=
𝔼
⁡
[
Y
∣
ℱ
t
]
=
η
t
.
\mathbb{E}[\eta_{t+1}\mid\mathcal{F}_{t}]=\mathbb{E}\big[\mathbb{E}[Y\mid\mathcal{F}_{t+1}]\mid\mathcal{F}_{t}\big]=\mathbb{E}[Y\mid\mathcal{F}_{t}]=\eta_{t}.
Corollary
5.5
is therefore a Doob–Pythagoras identity: each refinement step decomposes the mean squared error into a remaining error plus an orthogonal increment, and the gain
𝔼
⁡
[
(
η
t
+
1
−
η
t
)
2
]
\mathbb{E}[(\eta_{t+1}-\eta_{t})^{2}]
measures how much additional information
ℱ
t
+
1
\mathcal{F}_{t+1}
brings beyond
ℱ
t
\mathcal{F}_{t}
.
Equivalently,
𝔼
⁡
[
(
Y
−
η
t
)
2
]
=
𝔼
⁡
[
Var
⁡
(
Y
∣
ℱ
t
)
]
\mathbb{E}[(Y-\eta_{t})^{2}]=\mathbb{E}[\mathrm{Var}(Y\mid\mathcal{F}_{t})]
and
𝔼
⁡
[
(
η
t
+
1
−
η
t
)
2
]
=
𝔼
⁡
[
Var
⁡
(
Y
∣
ℱ
t
)
−
Var
⁡
(
Y
∣
ℱ
t
+
1
)
]
,
\mathbb{E}[(\eta_{t+1}-\eta_{t})^{2}]=\mathbb{E}[\mathrm{Var}(Y\mid\mathcal{F}_{t})-\mathrm{Var}(Y\mid\mathcal{F}_{t+1})],
so refinement reduces conditional variance in expectation.
In practice, boosting does not produce the Bayes sequence
(
Q
t
)
(Q_{t})
: updates are constrained (e.g., additive logits, shallow trees) and optimization is approximate. Hence, even if weak learners are calibrated in isolation, the final predictor need not be calibrated.
A robust practice is to recalibrate
after
boosting, or to use calibration-aware objectives (cf. the refine–then–calibrate discussion in
[
Berta et al., 2025
]
).
Stagewise recalibration (population view).
Let
S
~
t
∈
Δ
⁡
(
𝒴
)
\widetilde{S}_{t}\in\Delta(\mathcal{Y})
be the (possibly miscalibrated) score at stage
t
t
and define its population recalibration
S
t
:=
ℙ
(
Y
∈
⋅
∣
S
~
t
)
.
S_{t}:=\mathbb{P}(Y\in\cdot\mid\widetilde{S}_{t}).
Then
S
t
S_{t}
is perfectly calibrated with respect to its own output and (strictly) improves any strictly proper loss:
𝔼
⁡
[
ℓ
⁡
(
S
~
t
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
S
~
t
,
S
t
)
]
+
𝔼
⁡
[
ℓ
⁡
(
S
t
,
Y
)
]
.
\mathbb{E}[\ell(\widetilde{S}_{t},Y)]=\mathbb{E}\big[d_{\ell}(\widetilde{S}_{t},S_{t})\big]+\mathbb{E}[\ell(S_{t},Y)].
Crucially
, the projection
S
~
t
↦
S
t
\widetilde{S}_{t}\mapsto S_{t}
can reduce miscalibration but may also reduce resolution if it collapses distinct situations to the same score value; therefore, calibrating at each stage is not automatically beneficial for discrimination, and a final recalibration step is often still required.
6
Empirical illustrations
Our goal is not to optimize predictive performance, but to illustrate how the proposed decompositions separate miscalibration (reliability) from information loss (grouping) and residual uncertainty, and how this separation guides practical interventions such as recalibration and ensembling.
6.1
Synthetic Data
We use a binary data-generating process with two correlated covariates and known conditional probability
Q
⁡
(
𝑿
)
=
ℙ
⁡
(
Y
=
1
∣
𝑿
)
Q(\boldsymbol{X})=\mathbb{P}(Y=1\mid\boldsymbol{X})
; a correlation parameter
ρ
\rho
controls dependence
(
𝑿
\boldsymbol{X}
is generated from a Gaussian copula with correlation
ρ
\rho
and uniform marginals).
Full details and the true probability surface are given in Appendix
D
.
Base models and aggregation.
On a training split, we fit two misspecified logistic models
s
^
1
:=
ℙ
θ
^
1
​
(
Y
=
1
∣
X
1
)
,
and
​
s
^
2
:=
ℙ
θ
^
2
​
(
Y
=
1
∣
X
2
)
,
\widehat{s}_{1}:=\mathbb{P}_{\hat{\theta}_{1}}(Y=1\mid X_{1}),\text{ and }\widehat{s}_{2}:=\mathbb{P}_{\hat{\theta}_{2}}(Y=1\mid X_{2}),
and form their average
s
^
ens
:=
1
2
​
(
s
^
1
+
s
^
2
)
\widehat{s}_{\mathrm{ens}}:=\tfrac{1}{2}(\widehat{s}_{1}+\widehat{s}_{2})
.
On a separate calibration split, we learn monotone smooth recalibration maps
g
^
1
,
g
^
2
,
g
^
ens
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
\widehat{g}_{1},\widehat{g}_{2},\widehat{g}_{\mathrm{ens}}:[0,1]\to[0,1]
and define the recalibrated scores
S
(
1
)
=
g
^
1
​
(
s
^
1
)
S^{(1)}=\widehat{g}_{1}(\widehat{s}_{1})
,
S
(
2
)
=
g
^
2
​
(
s
^
2
)
S^{(2)}=\widehat{g}_{2}(\widehat{s}_{2})
and
S
(
ens
)
=
g
^
ens
​
(
s
^
ens
)
S^{(\mathrm{ens})}=\widehat{g}_{\mathrm{ens}}(\widehat{s}_{\mathrm{ens}})
, see Appendix
E
.
Local calibration score (LCS).
To quantify calibration we use the local calibration score
LCS
⁡
(
S
,
g
^
)
:=
1
n
​
∑
i
=
1
n
(
S
i
−
g
^
​
(
S
i
)
)
2
,
\mathrm{LCS}(S;\widehat{g}):=\frac{1}{n}\sum_{i=1}^{n}\Big(S_{i}-\widehat{g}(S_{i})\Big)^{2},
calculated using local regression as in
[
Austin and Steyerberg, 2019
]
, on an independent test split.
Intuitively,
LCS
\mathrm{LCS}
measures the squared distance between the score and its estimated calibrated version, and serves as a scalar summary complementary to calibration curves. For a proper loss
ℓ
\ell
, the natural reliability estimate is
𝔼
^
​
[
d
ℓ
​
(
S
,
C
^
​
(
S
)
)
]
\widehat{\mathbb{E}}[d_{\ell}(S,\widehat{C}(S))]
; we use LCS only as a compact proxy.
Result.
Figure
1
shows that the two base models can be nearly calibrated (small LCS), while their average exhibits substantially larger miscalibration, especially as
ρ
\rho
varies.
This empirically illustrates that calibration is not generally preserved under aggregation, even when each component
is (approximately) calibrated.
Figure 1:
Left:
learned monotone calibration maps
g
^
​
(
⋅
)
\widehat{g}(\cdot)
for the two base models (
s
^
1
\widehat{s}_{1}
in green,
s
^
2
\widehat{s}_{2}
in blue) and for their average
s
^
ens
\widehat{s}_{\mathrm{ens}}
(red), shown here for
ρ
=
0
\rho=0
. The grey diagonal corresponds to perfect calibration.
Right:
local calibration score as a function of
ρ
\rho
for the two base models (green/blue) and their average (red), computed on an independent test split.
Decomposition.
Figure
2
reports only the
reducible
part of the Brier decomposition, i.e. reliability
𝔼
⁡
[
(
S
−
C
)
2
]
\mathbb{E}[(S-C)^{2}]
and grouping
𝔼
⁡
[
(
C
−
Q
)
2
]
\mathbb{E}[(C-Q)^{2}]
(the irreducible term
𝔼
⁡
[
Q
⁡
(
1
−
Q
)
]
\mathbb{E}[Q(1-Q)]
is omitted for readability).
Across all three scores, post-hoc recalibration drives the reliability component close to zero, while the grouping component remains essentially unchanged.
This confirms the interpretation of recalibration as a projection at information level
σ
⁡
(
S
)
\sigma(S)
: it can remove miscalibration but cannot recover information lost in the compression
𝑿
↦
S
\boldsymbol{X}\mapsto S
.
Moreover, using a richer score (
x
​
12
x12
) substantially reduces grouping, whereas quantization increases it, showing that calibration alone does not prevent large information loss.
Figure 2:
Reducible Brier components on test data.
Bars show reliability
𝔼
^
​
[
(
S
−
C
^
)
2
]
\widehat{\mathbb{E}}[(S-\widehat{C})^{2}]
and grouping
𝔼
^
​
[
(
C
^
−
Q
)
2
]
\widehat{\mathbb{E}}[(\widehat{C}-Q)^{2}]
before and after monotone recalibration, for three scores: a logistic model on
X
1
X_{1}
(left), a logistic model on
(
X
1
,
X
2
)
(X_{1},X_{2})
(middle), and a quantized score (right).
Recalibration eliminates reliability but leaves grouping essentially unchanged.
6.2
Real-data case study: GermanCredit
We complement the synthetic experiments with a real-data case study on
GermanCredit
[
Hofmann, 1994
]
.
We consider two probabilistic classifiers trained on an independent training split:
(i) a logistic regression (GLM) and (ii) a random forest (RF).
We then form two ensembles: (a)
averaging
(arithmetic mean of predicted probabilities) and (b)
stacking
(a meta-logistic model trained on the calibration split using the pair of base scores).
Finally, we fit a
monotone
post-hoc recalibration map on an independent calibration split and evaluate metrics on a held-out test split.
Figure
3
displays monotone-smoothed calibration curves (raw in green, recalibrated in red; the diagonal corresponds to perfect calibration).
While recalibration substantially improves the GLM curve, nonparametric monotone recalibration may introduce distortions for some models (step-like behavior for tree-based scores), which can translate into degraded proper losses on the test set.
This finite-sample phenomenon is consistent with Appendix
C
: population improvements under strict propriety do not automatically carry over to plug-in estimators of
C
C
.
Table
1
and Figure
4
summarize test-set performance under two proper losses (Brier and log-loss), together with the miscalibration proxy LCS.
Proper-loss reliability estimates (for log-loss and Brier) and robustness analyses over repeated splits are reported in Appendix
D
.
Table 1:
GermanCredit
: test-set performance before/after monotone recalibration.
Gains are defined as
Δ
=
raw
−
recal
\Delta=\text{raw}-\text{recal}
(positive is better).
Model
Brier
LogLoss
LCS
raw
recal
Δ
\Delta
raw
recal
Δ
\Delta
GLM
0.19
0.18
0.01
0.73
0.55
0.19
0.012
RF
0.17
0.17
-0.00
0.52
0.63
-0.11
0.014
Average
0.17
0.18
-0.01
0.52
0.75
-0.24
0.013
Stacking
0.17
0.18
-0.00
0.52
0.63
-0.11
0.006
Figure 3:
GermanCredit
: monotone-smoothed calibration curves on the test split.
Green: raw score; red: after monotone post-hoc recalibration fit on a separate calibration split.
The diagonal indicates perfect calibration.
Figure 4:
GermanCredit
: summary metrics on the test split.
Left: miscalibration proxy
LCS
=
𝔼
^
​
(
S
−
C
^
​
(
S
)
)
2
\mathrm{LCS}=\widehat{\mathbb{E}}(S-\widehat{C}(S))^{2}
.
Middle/right: proper losses (Brier and log-loss) before vs. after recalibration.
7
Discussion and conclusion
This paper advocates an
information-level
view of calibration under proper losses.
Our main message is that calibration is inherently conditional: a predictor
S
=
s
⁡
(
𝑿
)
S=s(\boldsymbol{X})
is assessed through the
σ
\sigma
-algebra it generates, and any compression
𝑿
↦
S
\boldsymbol{X}\mapsto S
induces an information loss that cannot be repaired by post-hoc recalibration.
The proper-loss decompositions developed here make this explicit by separating (i) a reliability term (miscalibration), (ii) a grouping term (loss of information from
𝑿
\boldsymbol{X}
to
S
S
), and (iii) residual uncertainty at the feature level.
This separation clarifies what recalibration can and cannot improve, and explains why ensemble procedures may improve overall proper scores while degrading conditional calibration.
Implications for practice.
Our results support a simple workflow: (1) diagnose performance using a proper-loss decomposition rather than a single scalar score, (2) use post-hoc recalibration to reduce the reliability component on held-out data, and (3) if grouping dominates, improve the score itself (features, model class, or ensembling that retains more information, e.g. stacking) rather than relying on calibration alone.
For sequential methods (boosting), the filtration-based viewpoint suggests interpreting stagewise improvements as refinement gains, while recognizing that reliability may drift and typically benefits from a final recalibration step.
Limitations.
Our decomposition identities are population statements; empirical estimates require additional modeling choices, in particular when approximating conditional laws such as
C
=
ℙ
(
Y
∈
⋅
∣
S
)
C=\mathbb{P}(Y\in\cdot\mid S)
(and, beyond simulations,
Q
=
ℙ
(
Y
∈
⋅
∣
𝑿
)
Q=\mathbb{P}(Y\in\cdot\mid\boldsymbol{X})
).
Moreover, calibration is only one desideratum: imposing monotonicity or smoothness stabilizes estimation and can preserve ranking, but may also trade off resolution when the score is coarse or heavily discretized.
A geometric perspective: recalibration as transport on
[
0
,
1
]
[0,1]
(and beyond).
In the binary case, a strictly increasing recalibrator
g
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
g:[0,1]\to[0,1]
can be interpreted as a transport map pushing the distribution of
S
S
forward to that of the calibrated score
C
=
ℙ
⁡
(
Y
=
1
∣
S
)
C=\mathbb{P}(Y=1\mid S)
.
This suggests a geometric lens on recalibration: compare calibrators by the size of the transport they induce (e.g. Wasserstein distances between the distributions of
S
S
and
g
⁡
(
S
)
g(S)
), or view regularized calibration as selecting a map that balances fidelity to empirical calibration with minimal distortion of the score distribution.
Extending this viewpoint to multi-class calibration would naturally involve geometry on the simplex
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
and raises questions about appropriate transport/metric structures for probability vectors.
Outlook.
Several directions appear promising.
First, the information-level framework invites
calibration-aware ensembling
principles: characterize aggregators that preserve calibration (or preserve it after a controlled projection), and quantify the price paid in grouping when compressing a rich ensemble output to a single score.
Second, developing statistical inference tools for decomposition terms could turn these identities into routine model diagnostics, particularly under distribution shift.
Finally, extending the geometric transport viewpoint to multi-class settings, and relating it to proper-loss optimization and monotone/smooth constraints, may yield new calibration methods with explicit control of both reliability and distortion.
Conclusion.
Calibration is not an absolute property of a model output but a conditional statement at a chosen information level.
Proper-loss decompositions provide a unified language to separate reliability, information loss, and residual uncertainty, and to reason about recalibration, aggregation, and sequential ensemble procedures in a common framework.
References
Austin and Steyerberg (2019)
P. C. Austin and E. W. Steyerberg
The integrated calibration index (ICI) and related metrics for quantifying the calibration of logistic regression models
.
Statistics in Medicine
38
,
pp. 4051 – 4065
.
Cited by:
§E.4
,
§6.1
.
Barlow
et al.
(1972)
R. E. Barlow, D. J. Bartholomew, J. M. Bremner, and H. D. Brunk
Statistical inference under order restrictions: the theory and application of isotonic regression
.
John Wiley & Sons
,
New York
.
Cited by:
§E.1
.
Berta
et al.
(2025)
E. Berta, D. Holzmüller, M. I. Jordan, and F. Bach
Rethinking early stopping: refine, then calibrate
.
arXiv preprint arXiv:2501.19195
.
Cited by:
§1.2
,
§2.2
,
Proposition 4.1
,
§5.2
.
Best and Chakravarti (1990)
M. J. Best and N. Chakravarti
Active set algorithms for isotonic regression; a unifying framework
.
Mathematical Programming
47
,
pp. 425–439
.
Cited by:
§E.1
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
ISSN 1520-0493
Cited by:
§E.4
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
§1.2
,
§2.2
.
Bröcker (2018)
J. Bröcker
Reliability, sufficiency, and the decomposition of proper scores
.
arXiv preprint arXiv:0806.0813
.
Cited by:
§A.4
.
Dimitriadis
et al.
(2023)
T. Dimitriadis, T. Gneiting, A. I. Jordan, and P. Vogel
Evaluating probabilistic classifiers: the triptych
.
arXiv preprint arXiv:2301.10803
.
Cited by:
§1.2
,
§2.3
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
pp. e2016191118
.
Cited by:
§3.3
.
Eilers and Marx (1996)
P. H. C. Eilers and B. D. Marx
Flexible smoothing with B-splines and penalties
.
Statistical Science
11
(
2
),
pp. 89–121
.
Cited by:
§E.2
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
§1.2
,
§2.2
.
Gneiting and Ranjan (2013)
T. Gneiting and R. Ranjan
Combining predictive distributions
.
Electronic Journal of Statistics
7
,
pp.
.
External Links:
Document
Cited by:
§5.1
.
Gupta
et al.
(2021)
K. Gupta, A. Rahimi, T. Ajanthan, C. Sminchisescu, T. Mensink, and R. I. Hartley
Calibration of neural networks using splines
.
In
International Conference on Learning Representations (ICLR)
,
Cited by:
§E.4
.
Hofmann (1994)
H. Hofmann
Statlog (german credit data)
.
Note:
UCI Machine Learning Repository
External Links:
Document
Cited by:
§6.2
.
Kull and Flach (2015)
M. Kull and P. A. Flach
Novel decompositions of proper scoring rules for classification: score adjustment as precursor to calibration
.
In
Machine Learning and Knowledge Discovery in Databases (ECML PKDD 2015), Part I
,
Lecture Notes in Computer Science
, Vol.
9284
,
pp. 68–85
.
Cited by:
§1.2
,
§2.3
.
Nadaraya (1964)
E. A. Nadaraya
On estimating regression
.
Theory of Probability and Its Applications
9
(
1
),
pp. 141–142
.
Cited by:
§E.2
.
Perez-Lebel
et al.
(2023)
A. Perez-Lebel, M. L. Morvan, and G. Varoquaux
Beyond calibration: estimating the grouping loss of modern neural networks
.
In
ICLR
,
External Links:
Link
Cited by:
item -
,
§2.2
,
§3.3
.
Platt (1999)
J. Platt
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
§1.2
.
Pya and Wood (2015)
N. Pya and S. N. Wood
Shape constrained additive models
.
Journal of Computational and Graphical Statistics
24
(
1
),
pp. 182–206
.
Cited by:
2nd item
.
Robertson
et al.
(1988)
T. Robertson, F. T. Wright, and R. L. Dykstra
Order restricted statistical inference
.
John Wiley & Sons
,
New York
.
Cited by:
§E.1
.
Tasche (2021)
D. Tasche
Calibrating sufficiently
.
Statistics
55
(
6
),
pp. 1356––1386
.
Cited by:
§1
,
§2.2
,
§2.3
.
Vovk
et al.
(2005)
V. Vovk, A. Gammerman, and G. Shafer
Algorithmic learning in a random world
.
Springer
,
New York
.
Cited by:
§4
.
Vovk and Petej (2012)
V. Vovk and I. Petej
Venn-abers predictors
.
arXiv preprint arXiv:1211.0025
.
Cited by:
§4
.
Wand and Jones (1995)
M. P. Wand and M. C. Jones
Kernel smoothing
.
Chapman & Hall/CRC
,
London
.
Cited by:
§E.2
.
Watson (1964)
G. S. Watson
Smooth regression analysis
.
Sankhyā: The Indian Journal of Statistics, Series A
26
,
pp. 359–372
.
Cited by:
§E.2
.
Zhang
et al.
(2020)
J. Zhang, B. Kailkhura, and T. Y. Han
Mix-n-match : ensemble and compositional methods for uncertainty calibration in deep learning
.
In
Proceedings of the 37th International Conference on Machine Learning
,
H. D. III and A. Singh (Eds.)
,
Proceedings of Machine Learning Research
, Vol.
119
,
pp. 11117–11128
.
Cited by:
§E.4
.
Appendix A
Proofs
A.1
Proof of Theorem
2.1
Proof.
By the tower property of conditional expectation and the definition of
L
L
,
𝔼
⁡
[
ℓ
⁡
(
T
,
Y
)
]
=
𝔼
⁡
[
𝔼
⁡
[
ℓ
⁡
(
T
,
Y
)
∣
𝒜
]
]
=
𝔼
⁡
[
L
⁡
(
T
,
Q
𝒜
)
]
.
\mathbb{E}[\ell(T,Y)]=\mathbb{E}\Big[\mathbb{E}[\ell(T,Y)\mid\mathcal{A}]\Big]=\mathbb{E}\Big[L(T,Q_{\mathcal{A}})\Big].
Adding and subtracting
ℰ
ℓ
​
(
Q
𝒜
)
\mathcal{E}_{\ell}(Q_{\mathcal{A}})
yields
𝔼
⁡
[
L
⁡
(
T
,
Q
𝒜
)
]
\displaystyle\mathbb{E}[L(T,Q_{\mathcal{A}})]
=
𝔼
[
L
(
T
,
Q
𝒜
)
−
ℰ
ℓ
(
Q
𝒜
)
]
+
𝔼
[
ℰ
ℓ
(
Q
𝒜
)
=
𝔼
[
d
ℓ
(
T
,
Q
𝒜
)
]
+
𝔼
[
ℰ
ℓ
(
Q
𝒜
)
]
.
\displaystyle=\mathbb{E}\big[L(T,Q_{\mathcal{A}})-\mathcal{E}_{\ell}(Q_{\mathcal{A}})\big]+\mathbb{E}[\mathcal{E}_{\ell}(Q_{\mathcal{A}})=\mathbb{E}[d_{\ell}(T,Q_{\mathcal{A}})]+\mathbb{E}[\mathcal{E}_{\ell}(Q_{\mathcal{A}})].
∎
A.2
Proof of Theorem
2.2
Proof.
First apply Theorem
2.1
with
𝒜
\mathcal{A}
:
𝔼
⁡
[
ℓ
⁡
(
T
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
T
,
Q
𝒜
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Q
𝒜
)
]
.
\mathbb{E}[\ell(T,Y)]=\mathbb{E}[d_{\ell}(T,Q_{\mathcal{A}})]+\mathbb{E}[\mathcal{E}_{\ell}(Q_{\mathcal{A}})].
It remains to decompose
𝔼
⁡
[
ℰ
ℓ
​
(
Q
𝒜
)
]
\mathbb{E}[\mathcal{E}_{\ell}(Q_{\mathcal{A}})]
through
ℬ
\mathcal{B}
.
Note that
Q
𝒜
Q_{\mathcal{A}}
is
𝒜
\mathcal{A}
-measurable and hence also
ℬ
\mathcal{B}
-measurable since
𝒜
⊆
ℬ
\mathcal{A}\subseteq\mathcal{B}
.
Apply Theorem
2.1
with
T
:=
Q
𝒜
T:=Q_{\mathcal{A}}
and
ℬ
\mathcal{B}
:
𝔼
⁡
[
ℓ
⁡
(
Q
𝒜
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
Q
𝒜
,
Q
ℬ
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Q
ℬ
)
]
.
\mathbb{E}[\ell(Q_{\mathcal{A}},Y)]=\mathbb{E}\big[d_{\ell}(Q_{\mathcal{A}},Q_{\mathcal{B}})\big]+\mathbb{E}\big[\mathcal{E}_{\ell}(Q_{\mathcal{B}})\big].
Moreover,
𝔼
⁡
[
ℓ
⁡
(
Q
𝒜
,
Y
)
]
=
𝔼
⁡
[
𝔼
⁡
[
ℓ
⁡
(
Q
𝒜
,
Y
)
∣
𝒜
]
]
=
𝔼
⁡
[
ℰ
ℓ
​
(
Q
𝒜
)
]
,
\mathbb{E}[\ell(Q_{\mathcal{A}},Y)]=\mathbb{E}\big[\mathbb{E}[\ell(Q_{\mathcal{A}},Y)\mid\mathcal{A}]\big]=\mathbb{E}\big[\mathcal{E}_{\ell}(Q_{\mathcal{A}})\big],
by the definition of
ℰ
ℓ
\mathcal{E}_{\ell}
.
Combining these identities yields the claimed equality.
∎
A.3
Proof of Lemma
2.3
Proof.
Since
d
ℓ
​
(
⋅
,
⋅
)
≥
0
d_{\ell}(\cdot,\cdot)\geq 0
, the condition
𝔼
⁡
[
d
ℓ
​
(
C
,
Q
)
]
=
0
\mathbb{E}[d_{\ell}(C,Q)]=0
implies
d
ℓ
​
(
C
,
Q
)
=
0
d_{\ell}(C,Q)=0
a.s.
By strict propriety,
d
ℓ
​
(
C
,
Q
)
=
0
d_{\ell}(C,Q)=0
a.s. iff
C
=
Q
C=Q
a.s.
Finally,
C
=
ℙ
(
Y
∈
⋅
∣
S
)
C=\mathbb{P}(Y\in\cdot\mid S)
and
Q
=
ℙ
(
Y
∈
⋅
∣
𝑿
)
Q=\mathbb{P}(Y\in\cdot\mid\boldsymbol{X})
satisfy
C
=
Q
C=Q
a.s. iff
Q
Q
admits a
σ
⁡
(
S
)
\sigma(S)
-measurable version, which is exactly
σ
⁡
(
S
)
\sigma(S)
-measurability of
Q
Q
.
∎
A.4
Proof of Proposition
2.5
Proof.
Start from the one-level decomposition with
𝒜
=
ℋ
S
\mathcal{A}=\mathcal{H}_{S}
:
𝔼
⁡
[
ℓ
⁡
(
S
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
S
,
C
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
C
)
]
\mathbb{E}[\ell(S,Y)]=\mathbb{E}[d_{\ell}(S,C)]+\mathbb{E}[\mathcal{E}_{\ell}(C)]
.
It remains to express
𝔼
​
[
ℰ
ℓ
​
(
C
)
]
\mathbb{E}[\mathcal{E}_{\ell}(C)]
relative to the constant
Q
¯
\bar{Q}
.
Applying Theorem
2.1
with
T
=
Q
¯
T=\bar{Q}
(constant, hence
ℋ
S
\mathcal{H}_{S}
-measurable) and
𝒜
=
ℋ
S
\mathcal{A}=\mathcal{H}_{S}
yields
𝔼
⁡
[
ℓ
⁡
(
Q
¯
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
Q
¯
,
C
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
C
)
]
\mathbb{E}[\ell(\bar{Q},Y)]=\mathbb{E}[d_{\ell}(\bar{Q},C)]+\mathbb{E}[\mathcal{E}_{\ell}(C)]
.
But
𝔼
⁡
[
ℓ
⁡
(
Q
¯
,
Y
)
]
=
ℰ
ℓ
​
(
Q
¯
)
\mathbb{E}[\ell(\bar{Q},Y)]=\mathcal{E}_{\ell}(\bar{Q})
, hence
𝔼
⁡
[
ℰ
ℓ
​
(
C
)
]
=
ℰ
ℓ
​
(
Q
¯
)
−
𝔼
⁡
[
d
ℓ
​
(
Q
¯
,
C
)
]
\mathbb{E}[\mathcal{E}_{\ell}(C)]=\mathcal{E}_{\ell}(\bar{Q})-\mathbb{E}[d_{\ell}(\bar{Q},C)]
and the claimed formula follows.
A complete treatment (including “sufficiency” attributes) is developed in
Bröcker [2018]
.
∎
A.5
Proof of Theorem
2.6
Proof.
First apply Theorem
2.2
to the chain
ℋ
S
⊆
ℋ
𝑿
\mathcal{H}_{S}\subseteq\mathcal{H}_{\boldsymbol{X}}
to obtain (
1
).
Next apply Theorem
2.1
with
T
=
Q
T=Q
and
𝒜
=
ℋ
Z
\mathcal{A}=\mathcal{H}_{Z}
to get
𝔼
⁡
[
ℓ
⁡
(
Q
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
Q
,
Π
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Π
)
]
\mathbb{E}[\ell(Q,Y)]=\mathbb{E}[d_{\ell}(Q,\Pi)]+\mathbb{E}[\mathcal{E}_{\ell}(\Pi)]
.
Moreover,
𝔼
⁡
[
ℓ
⁡
(
Q
,
Y
)
]
=
𝔼
⁡
[
ℰ
ℓ
​
(
Q
)
]
\mathbb{E}[\ell(Q,Y)]=\mathbb{E}[\mathcal{E}_{\ell}(Q)]
by the same argument as in the proof of Theorem
2.2
.
Substituting
𝔼
​
[
ℰ
ℓ
​
(
Q
)
]
\mathbb{E}[\mathcal{E}_{\ell}(Q)]
into (
1
) yields the result.
∎
A.6
Proof of Corollary
2.7
Proof.
For the Brier loss one checks directly that
L
⁡
(
p
,
q
)
=
(
p
−
q
)
2
+
q
⁡
(
1
−
q
)
L(p,q)=(p-q)^{2}+q(1-q)
, hence
d
ℓ
​
(
p
,
q
)
=
(
p
−
q
)
2
d_{\ell}(p,q)=(p-q)^{2}
and
ℰ
ℓ
​
(
q
)
=
q
⁡
(
1
−
q
)
\mathcal{E}_{\ell}(q)=q(1-q)
.
Applying Theorem
2.2
to
ℋ
S
⊆
ℋ
𝑿
\mathcal{H}_{S}\subseteq\mathcal{H}_{\boldsymbol{X}}
yields the first equality.
The second follows from Theorem
2.1
with
T
=
Q
T=Q
and
𝒜
=
ℋ
Z
\mathcal{A}=\mathcal{H}_{Z}
, noting that
d
ℓ
​
(
Q
,
Π
)
=
(
Q
−
Π
)
2
d_{\ell}(Q,\Pi)=(Q-\Pi)^{2}
and
ℰ
ℓ
​
(
Π
)
=
Π
⁡
(
1
−
Π
)
\mathcal{E}_{\ell}(\Pi)=\Pi(1-\Pi)
.
∎
A.7
Proof of Corollary
2.8
Proof.
For log-loss,
L
(
p
,
q
)
=
H
(
q
)
+
KL
(
q
∥
p
)
L(p,q)=H(q)+\mathrm{KL}(q\|p)
, hence
d
log
(
p
,
q
)
=
KL
(
q
∥
p
)
d_{\log}(p,q)=\mathrm{KL}(q\|p)
and
E
log
​
(
q
)
=
H
​
(
q
)
\mathrm{E}_{\log}(q)=H(q)
.
Plugging into Theorem
2.2
yields the first display. For the second, note that
I
(
Y
;
ℬ
∣
𝒜
)
=
𝔼
[
KL
(
P
(
Y
∈
⋅
∣
ℬ
)
∥
P
(
Y
∈
⋅
∣
𝒜
)
)
]
=
𝔼
[
KL
(
Q
ℬ
∥
Q
𝒜
)
]
I(Y;\mathcal{B}\mid\mathcal{A})=\mathbb{E}[\mathrm{KL}(P(Y\in\cdot\mid\mathcal{B})\|P(Y\in\cdot\mid\mathcal{A}))]=\mathbb{E}[\mathrm{KL}(Q_{\mathcal{B}}\|Q_{\mathcal{A}})]
.
Finally, when
S
=
s
⁡
(
X
)
S=s(X)
,
P
⁡
(
Y
∣
X
,
S
)
=
P
⁡
(
Y
∣
X
)
P(Y\mid X,S)=P(Y\mid X)
, so
𝔼
[
KL
(
Q
∥
C
)
]
=
I
(
Y
;
X
∣
S
)
\mathbb{E}[\mathrm{KL}(Q\|C)]=I(Y;X\mid S)
and
H
⁡
(
Y
∣
X
)
=
𝔼
⁡
[
H
⁡
(
Q
)
]
H(Y\mid X)=\mathbb{E}[H(Q)]
.
∎
A.8
Proof of Proposition
3.2
Proof.
The decomposition is Theorem
2.1
with
𝒜
=
σ
⁡
(
S
)
\mathcal{A}=\sigma(S)
and
T
=
S
T=S
.
Strict propriety yields
𝔼
⁡
[
d
ℓ
​
(
S
,
C
)
]
=
0
⇒
S
=
C
\mathbb{E}[d_{\ell}(S,C)]=0\Rightarrow S=C
a.s.
Finally, if
S
=
C
S=C
a.s., then
𝔼
⁡
[
onehot
⁡
(
Y
)
∣
S
]
=
S
\mathbb{E}[\mathrm{onehot}(Y)\mid S]=S
a.s., hence
𝔼
⁡
[
onehot
⁡
(
Y
)
]
=
𝔼
⁡
[
S
]
\mathbb{E}[\mathrm{onehot}(Y)]=\mathbb{E}[S]
by the tower property.
∎
A.9
Proof of Proposition
4.1
Proof.
Apply Theorem
2.1
with
𝒜
=
σ
⁡
(
S
)
\mathcal{A}=\sigma(S)
and
T
=
g
⁡
(
S
)
T=g(S)
:
𝔼
⁡
[
ℓ
⁡
(
g
⁡
(
S
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
g
⁡
(
S
)
,
C
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
C
)
]
.
\mathbb{E}[\ell(g(S),Y)]=\mathbb{E}\big[d_{\ell}(g(S),C)\big]+\mathbb{E}\big[\mathcal{E}_{\ell}(C)\big].
The second term does not depend on
g
g
, while the first is minimized at
0
0
, achieved by
g
⁡
(
S
)
=
C
g(S)=C
a.s. (and uniquely if
ℓ
\ell
is strictly proper).
Finally,
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
=
𝔼
⁡
[
ℰ
ℓ
​
(
C
)
]
\mathbb{E}[\ell(C,Y)]=\mathbb{E}[\mathcal{E}_{\ell}(C)]
since
d
ℓ
​
(
C
,
C
)
=
0
d_{\ell}(C,C)=0
.
∎
A.10
Proof of Proposition
4.2
Proof.
For fixed
τ
\tau
, the set
{
s
:
g
⁡
(
s
)
≥
τ
}
\{s:g(s)\geq\tau\}
is an interval
[
t
,
1
]
[t,1]
since
g
g
is non-decreasing.
Let
τ
′
:=
inf
{
s
:
g
⁡
(
s
)
≥
τ
}
\tau^{\prime}:=\inf\{s:g(s)\geq\tau\}
. Then
g
⁡
(
S
)
≥
τ
g(S)\geq\tau
iff
S
≥
τ
′
S\geq\tau^{\prime}
except possibly on flat regions (ties), which only affect ROC through the chosen tie-breaking convention.
∎
A.11
Proof of Theorem
5.3
Proof.
Apply Theorem
2.2
to
(
ℱ
0
,
ℱ
1
)
(\mathcal{F}_{0},\mathcal{F}_{1})
and predictor
T
T
:
𝔼
⁡
[
ℓ
⁡
(
T
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
T
,
Q
0
)
]
+
𝔼
⁡
[
d
ℓ
​
(
Q
0
,
Q
1
)
]
+
𝔼
⁡
[
ℰ
ℓ
​
(
Q
1
)
]
.
\mathbb{E}[\ell(T,Y)]=\mathbb{E}[d_{\ell}(T,Q_{0})]+\mathbb{E}[d_{\ell}(Q_{0},Q_{1})]+\mathbb{E}[\mathcal{E}_{\ell}(Q_{1})].
Then apply the same identity to
𝔼
⁡
[
ℰ
ℓ
​
(
Q
1
)
]
=
𝔼
⁡
[
ℓ
⁡
(
Q
1
,
Y
)
]
\mathbb{E}[\mathcal{E}_{\ell}(Q_{1})]=\mathbb{E}[\ell(Q_{1},Y)]
along
(
ℱ
1
,
ℱ
2
)
(\mathcal{F}_{1},\mathcal{F}_{2})
, and iterate.
The divergence terms telescope, yielding the claim.
∎
A.12
Proof of Corollary
5.4
Proof.
Immediate from Corollary
2.8
applied to each pair
ℱ
t
⊆
ℱ
t
+
1
\mathcal{F}_{t}\subseteq\mathcal{F}_{t+1}
and the definition of conditional mutual information.
∎
A.13
Proof of Corollary
5.5
Proof.
Let
η
t
=
𝔼
⁡
[
Y
∣
ℱ
t
]
\eta_{t}=\mathbb{E}[Y\mid\mathcal{F}_{t}]
. Write
Y
−
η
t
=
(
Y
−
η
t
+
1
)
+
(
η
t
+
1
−
η
t
)
Y-\eta_{t}=(Y-\eta_{t+1})+(\eta_{t+1}-\eta_{t})
and expand the square.
The cross term vanishes since
𝔼
⁡
[
Y
−
η
t
+
1
∣
ℱ
t
+
1
]
=
0
\mathbb{E}[Y-\eta_{t+1}\mid\mathcal{F}_{t+1}]=0
.
∎
Appendix B
Conditional laws as
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
-valued random variables
Throughout,
𝒴
=
{
1
,
…
,
k
}
\mathcal{Y}=\{1,\dots,k\}
is finite and
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
denotes the probability simplex.
For any
σ
\sigma
-algebra
𝒜
⊆
ℱ
\mathcal{A}\subseteq\mathcal{F}
, the conditional law
Q
𝒜
:=
ℙ
(
Y
∈
⋅
∣
𝒜
)
Q_{\mathcal{A}}:=\mathbb{P}(Y\in\cdot\mid\mathcal{A})
can be represented as a
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
-valued random vector.
When
𝒴
\mathcal{Y}
is finite, the conditional law
ℙ
(
Y
∈
⋅
∣
𝒜
)
\mathbb{P}(Y\in\cdot\mid\mathcal{A})
can be identified with the
𝒜
\mathcal{A}
-measurable vector of conditional probabilities
(
ℙ
⁡
(
Y
=
1
∣
𝒜
)
,
…
,
ℙ
⁡
(
Y
=
k
∣
𝒜
)
)
\big(\mathbb{P}(Y=1\mid\mathcal{A}),\dots,\mathbb{P}(Y=k\mid\mathcal{A})\big)
.
More generally, one may view
ω
↦
Q
𝒜
​
(
ω
)
\omega\mapsto Q_{\mathcal{A}}(\omega)
as an
𝒜
\mathcal{A}
-measurable
Markov kernel
from
(
Ω
,
𝒜
)
(\Omega,\mathcal{A})
to
(
𝒴
,
2
𝒴
)
(\mathcal{Y},2^{\mathcal{Y}})
.
All equalities involving
Q
𝒜
Q_{\mathcal{A}}
are understood up to
ℙ
\mathbb{P}
-almost sure equality (versions).
Lemma B.1
(Vector representation)
.
Let
onehot
⁡
(
Y
)
∈
{
0
,
1
}
k
\mathrm{onehot}(Y)\in\{0,1\}^{k}
be the one-hot encoding of
Y
Y
.
Define the
𝒜
\mathcal{A}
-measurable random vector
π
𝒜
:=
𝔼
⁡
[
onehot
⁡
(
Y
)
∣
𝒜
]
∈
ℝ
k
.
\pi_{\mathcal{A}}:=\mathbb{E}[\mathrm{onehot}(Y)\mid\mathcal{A}]\in\mathbb{R}^{k}.
Then
π
𝒜
∈
Δ
⁡
(
𝒴
)
\pi_{\mathcal{A}}\in\Delta(\mathcal{Y})
almost surely and, for each
j
∈
{
1
,
…
,
k
}
j\in\{1,\dots,k\}
,
(
π
𝒜
)
j
=
ℙ
⁡
(
Y
=
j
∣
𝒜
)
a.s.
(\pi_{\mathcal{A}})_{j}=\mathbb{P}(Y=j\mid\mathcal{A})\quad\text{a.s.}
In particular, identifying a distribution
q
∈
Δ
⁡
(
𝒴
)
q\in\Delta(\mathcal{Y})
with its coordinate vector
q
=
(
q
1
,
…
,
q
k
)
q=(q_{1},\dots,q_{k})
, we may view
Q
𝒜
Q_{\mathcal{A}}
as the
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
-valued random variable
Q
𝒜
≡
π
𝒜
Q_{\mathcal{A}}\equiv\pi_{\mathcal{A}}
.
Proof.
For each
j
j
, the coordinate
(
π
𝒜
)
j
=
𝔼
[
𝟏
{
Y
=
j
}
∣
𝒜
]
(\pi_{\mathcal{A}})_{j}=\mathbb{E}[\mathbf{1}_{\{Y=j\}}\mid\mathcal{A}]
is
𝒜
\mathcal{A}
-measurable and lies in
[
0
,
1
]
[0,1]
almost surely.
Moreover, summing over
j
j
gives
∑
j
=
1
k
(
π
𝒜
)
j
=
𝔼
[
∑
j
=
1
k
𝟏
{
Y
=
j
}
∣
𝒜
]
=
1
,
a.s.
,
\sum_{j=1}^{k}(\pi_{\mathcal{A}})_{j}=\mathbb{E}[\sum_{j=1}^{k}\mathbf{1}_{\{Y=j\}}\mid\mathcal{A}]=1,\penalty\ \text{a.s.},
hence
π
𝒜
∈
Δ
⁡
(
𝒴
)
\pi_{\mathcal{A}}\in\Delta(\mathcal{Y})
a.s.
The identity
(
π
𝒜
)
j
=
ℙ
⁡
(
Y
=
j
∣
𝒜
)
(\pi_{\mathcal{A}})_{j}=\mathbb{P}(Y=j\mid\mathcal{A})
is the defining property of conditional probabilities.
∎
Lemma B.2
(Uniqueness up to a.s. equality)
.
Let
U
U
and
V
V
be
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
-valued
𝒜
\mathcal{A}
-measurable random variables such that for every
B
⊆
𝒴
B\subseteq\mathcal{Y}
,
U
⁡
(
B
)
=
ℙ
⁡
(
Y
∈
B
∣
𝒜
)
a.s.
and
V
⁡
(
B
)
=
ℙ
⁡
(
Y
∈
B
∣
𝒜
)
a.s.
U(B)=\mathbb{P}(Y\in B\mid\mathcal{A})\quad\text{a.s.}\qquad\text{and}\qquad V(B)=\mathbb{P}(Y\in B\mid\mathcal{A})\quad\text{a.s.}
Then
U
=
V
U=V
almost surely.
In particular,
Q
𝒜
Q_{\mathcal{A}}
is well-defined as an
𝒜
\mathcal{A}
-measurable
Δ
⁡
(
𝒴
)
\Delta(\mathcal{Y})
-valued random variable up to almost sure equality.
Proof.
Because
𝒴
\mathcal{Y}
is finite, it suffices to check equality on singletons. For each
j
∈
{
1
,
…
,
k
}
j\in\{1,\dots,k\}
we have
U
⁡
(
{
j
}
)
=
V
⁡
(
{
j
}
)
U(\{j\})=V(\{j\})
a.s., hence the coordinate vectors coincide a.s., so
U
=
V
U=V
a.s.
∎
Finally, note that for any
𝒜
⊆
ℬ
⊆
ℱ
\mathcal{A}\subseteq\mathcal{B}\subseteq\mathcal{F}
, the corresponding conditional laws satisfy
Q
𝒜
=
𝔼
⁡
[
Q
ℬ
∣
𝒜
]
Q_{\mathcal{A}}=\mathbb{E}[Q_{\mathcal{B}}\mid\mathcal{A}]
coordinate-wise, i.e. by applying the tower property to each indicator
𝟏
{
Y
=
j
}
\mathbf{1}_{\{Y=j\}}
.
Appendix C
Statistical uncertainty for calibration components
Our decompositions are population identities, but empirical work requires estimating quantities such as
𝔼
​
[
d
ℓ
​
(
S
,
C
)
]
\mathbb{E}[d_{\ell}(S,C)]
,
𝔼
​
[
d
ℓ
​
(
C
,
Q
)
]
\mathbb{E}[d_{\ell}(C,Q)]
, and
𝔼
​
[
ℰ
ℓ
​
(
Q
)
]
\mathbb{E}[\mathcal{E}_{\ell}(Q)]
on finite samples.
A practical question is therefore: how uncertain are these estimates under sampling variability?
Avoiding optimistic bias.
Because
C
=
ℙ
(
Y
∈
⋅
∣
S
)
C=\mathbb{P}(Y\in\cdot\mid S)
is typically estimated from data, evaluating calibration on the same sample used to fit the calibrator can lead to optimistic (downward biased) reliability estimates.
We therefore recommend a train/calibration/test split, or cross-fitting, so that both the predictor and the calibration map are evaluated out-of-sample.
Bootstrap inference (pipeline view).
A simple and broadly applicable approach is resampling-based inference (bootstrap) applied to the entire pipeline: refit the predictor on resampled training data, refit the calibrator (or calibration curve) on resampled calibration data, and evaluate the decomposition terms on held-out test data.
Repeating this procedure yields empirical confidence intervals for reliability, grouping, and total expected loss.
Two sources of uncertainty.
Depending on the scientific question, one may distinguish:
(i)
calibration-only uncertainty
, where the base predictor is treated as fixed and only the calibrator is refit (resampling the calibration split), and
(ii)
end-to-end uncertainty
, where both the predictor and calibrator are refit (resampling train and calibration splits).
The latter is typically wider but better reflects deployment variability.
Parametric calibrators.
For smooth parametric calibrators (e.g. Platt scaling or temperature scaling), asymptotic normality can provide standard errors for low-dimensional summaries (e.g. integrated calibration error), via standard M-estimation theory.
In practice, bootstrap procedures remain robust and easy to implement across model classes and calibration estimators.
Appendix D
Additional experiment details
D.1
Synthetic experiment details
We generate binary outcomes
Y
∈
{
0
,
1
}
Y\in\{0,1\}
from a controlled two-feature model where the true conditional probability
Q
⁡
(
𝑿
)
=
ℙ
⁡
(
Y
=
1
∣
𝑿
)
Q(\boldsymbol{X})=\mathbb{P}(Y=1\mid\boldsymbol{X})
is known in closed form.
Let
(
Z
1
,
Z
2
)
(Z_{1},Z_{2})
be jointly Gaussian with correlation
ρ
∈
(
−
1
,
1
)
\rho\in(-1,1)
and define
X
1
=
Φ
⁡
(
Z
1
)
,
X
2
=
Φ
⁡
(
Z
2
)
,
X_{1}=\Phi(Z_{1}),\qquad X_{2}=\Phi(Z_{2}),
so that
X
1
,
X
2
∈
(
0
,
1
)
X_{1},X_{2}\in(0,1)
have uniform marginals and dependence controlled by
ρ
\rho
.
Let
σ
⁡
(
u
)
=
{
1
+
exp
⁡
(
−
u
)
}
−
1
\sigma(u)=\{1+\exp(-u)\}^{-1}
denote the logistic sigmoid and set
η
⁡
(
𝑿
)
:=
2.5
​
(
(
X
1
+
X
2
)
−
1
)
+
2
​
(
exp
⁡
(
(
X
1
−
X
2
)
3
)
−
1
)
,
Q
⁡
(
𝑿
)
=
σ
⁡
(
η
⁡
(
𝑿
)
)
.
\eta(\boldsymbol{X}):=2.5\big((X_{1}+X_{2})-1\big)+2\big(\exp((X_{1}-X_{2})^{3})-1\big),\qquad Q(\boldsymbol{X})=\sigma\big(\eta(\boldsymbol{X})\big).
We then sample
Y
|
𝑿
∼
Bernoulli
⁡
(
Q
⁡
(
𝑿
)
)
.
Y\mid\boldsymbol{X}\sim\mathrm{Bernoulli}\big(Q(\boldsymbol{X})\big).
We vary
ρ
\rho
to control redundancy between
X
1
X_{1}
and
X
2
X_{2}
.
Unless stated otherwise, we use independent train/calibration/test splits with
n
n
samples each.
Figure 5:
True conditional probability surface
Q
⁡
(
x
1
,
x
2
)
Q(x_{1},x_{2})
for the synthetic model, on the left hand side. Then 3 scatterplots of simulated data, with
ρ
=
−
0.7
\rho=-0.7
(middle left),
ρ
=
0
\rho=0
(middle right), and
ρ
=
0.7
\rho=0.7
(right).
Splits.
Each run uses independent train/calibration/test splits.
Calibration mappings are fit
only
on the calibration split to avoid optimistic bias.
Estimating
C
⁡
(
s
)
=
ℙ
⁡
(
Y
=
1
∣
S
=
s
)
C(s)=\mathbb{P}(Y=1\mid S=s)
.
In the binary case, we fit monotone smooth calibrators of the form
C
^
=
g
^
​
(
S
)
\widehat{C}=\widehat{g}(S)
.
We use (i) Platt scaling, (ii) isotonic regression, and (iii) a monotone spline estimator implemented via constrained GAM/P-splines (SCAM), optionally preceded by kernel pre-smoothing on a grid.
Unless stated otherwise, all reported numbers use isotonic regression as the monotone calibrator; Platt scaling and SCAM yield similar qualitative conclusions. Methodological details are provided in Appendix
E
. An anonymized implementation will be released upon publication.
Estimating decomposition terms.
Because
Q
⁡
(
𝑿
)
Q(\boldsymbol{X})
is known in the simulation, we evaluate
H
ℓ
​
(
Q
)
H_{\ell}(Q)
exactly (plug-in), and compute the grouping term
𝔼
​
[
d
ℓ
​
(
C
,
Q
)
]
\mathbb{E}[d_{\ell}(C,Q)]
by plugging in
C
^
​
(
S
)
\widehat{C}(S)
and the known
Q
⁡
(
𝑿
)
Q(\boldsymbol{X})
on the test set.
Reliability is computed as
𝔼
​
[
d
ℓ
​
(
S
,
C
^
​
(
S
)
)
]
\mathbb{E}[d_{\ell}(S,\widehat{C}(S))]
.
For the Brier score, these become squared differences; for log-loss, they become KL divergences.
D.2
Additional diagnostics and robustness
LCS proxy and reliability diagrams
For completeness we report an
ℓ
2
\ell_{2}
-style proxy for calibration error,
LCS
=
𝔼
^
​
[
(
S
−
C
^
​
(
S
)
)
2
]
,
\mathrm{LCS}\;=\;\widehat{\mathbb{E}}\big[(S-\widehat{C}(S))^{2}\big],
computed by fitting a calibrator
C
^
\widehat{C}
on a held-out fold (or via cross-fitting) and evaluating on the corresponding test fold.
We emphasize that our theoretical decompositions are in terms of proper-loss reliability
Rel
^
ℓ
=
1
n
​
∑
i
=
1
n
d
ℓ
​
(
S
i
,
C
^
​
(
S
i
)
)
\widehat{\mathrm{Rel}}_{\ell}=\frac{1}{n}\sum_{i=1}^{n}d_{\ell}(S_{i},\widehat{C}(S_{i}))
; LCS is reported only as a familiar
ℓ
2
\ell_{2}
proxy.
Reliability diagrams use
B
B
quantile bins on
[
0
,
1
]
[0,1]
(approximately equal-mass bins), plotting
𝔼
^
​
[
Y
∣
S
∈
bin
]
\widehat{\mathbb{E}}[Y\mid S\in\text{bin}]
against the bin-wise mean score.
Uncertainty via repeated splits
To assess variability, we repeat the full pipeline over
R
R
random train/validation/test splits (or seeds).
Table
2
reports mean
±
\pm
sd over
R
=
100
R=100
randomized splits for raw/recalibrated losses and proper-loss reliability.
These averages summarize end-to-end variability of the full pipeline (train
→
\to
calibrate
→
\to
test).
Here,
averaging
denotes the arithmetic mean of base probabilities, while
stacking
denotes a meta-logistic model trained on the calibration split from the pair of base scores.
We report mean
±
\pm
std for log-loss, Brier, and proper-loss reliability.
Table 2:
GermanCredit
robustness over repeated splits (mean
±
\pm
sd over
R
=
100
R=100
seeds). Proper-loss reliability uses the fitted calibrator
C
^
\widehat{C}
trained on the calibration split and evaluated on the test split.
Method
Log-loss (raw)
Log-loss (recal.)
Rel
log
Average
0.496
±
\pm
0.031
0.601
±
\pm
0.093
0.028
±
\pm
0.014
GLM
0.565
±
\pm
0.084
0.640
±
\pm
0.124
0.033
±
\pm
0.026
RF
0.501
±
\pm
0.027
0.549
±
\pm
0.071
0.040
±
\pm
0.014
Stacking
0.504
±
\pm
0.037
0.589
±
\pm
0.085
0.021
±
\pm
0.008
Method
Brier (raw)
Brier (recal.)
Rel
Brier
Average
0.165
±
\pm
0.013
0.171
±
\pm
0.012
0.007
±
\pm
0.003
GLM
0.176
±
\pm
0.016
0.177
±
\pm
0.014
0.008
±
\pm
0.004
RF
0.166
±
\pm
0.012
0.168
±
\pm
0.015
0.012
±
\pm
0.005
Stacking
0.167
±
\pm
0.015
0.171
±
\pm
0.015
0.004
±
\pm
0.002
Table
3
reports a paired, split-wise comparison against the
Average
ensemble over
R
R
randomized train/calibration/test splits.
For each split we compute the recalibrated log-loss and the proper log-loss reliability term
Rel
^
log
\widehat{\mathrm{Rel}}_{\log}
, and report
Δ
=
\Delta=
(method
−
-
Average), so that negative values indicate an improvement over the reference.
In addition to mean
±
\pm
sd of
Δ
\Delta
, we report the win-rate (fraction of splits where the method outperforms Average) and a one-sided Wilcoxon signed-rank test of
H
1
H_{1}
: method
<
<
Average, with Holm correction across methods.
Overall, the results suggest that stacking yields a statistically significant reduction in
Rel
^
log
\widehat{\mathrm{Rel}}_{\log}
(64% win-rate, corrected
p
<
10
−
4
p<10^{-4}
), while differences in recalibrated log-loss are small and not significant after correction.
Table 3:
Paired comparison against
Average
(computed per split/seed).
Δ
\Delta
denotes (method
−
-
reference) so negative values indicate an improvement over the reference. We report win-rate and one-sided Wilcoxon signed-rank tests (
H
1
H_{1}
: method
<
<
reference), with Holm correction across methods.
Method
Δ
\Delta
Log-loss (recal.)
Win%
p
p
(Holm)
Δ
\Delta
Rel
log
Win%
p
p
(Holm)
GLM
0.0281
±
\pm
0.1091
34%
0.996
0.0141
±
\pm
0.0388
39%
1
RF
-0.0184
±
\pm
0.0963
60%
0.056
0.0134
±
\pm
0.0140
15%
1
Stacking
0.0020
±
\pm
0.0753
55%
0.949
-0.0055
±
\pm
0.0109
64%
<
10
−
4
<10^{-4}
Protocol and implementation details
Unless stated otherwise, calibration is estimated out-of-sample, either using an explicit calibration split (as in Section
6.2
) or via K-fold cross-fitting, preventing optimistic bias.
Hyperparameters are selected on validation folds only; test folds are used once per split for reporting.
Appendix E
Shape-constrained smoothing for (re)calibration
We observe pairs
(
x
i
,
y
i
)
i
=
1
n
(x_{i},y_{i})_{i=1}^{n}
with
x
i
∈
[
0
,
1
]
x_{i}\in[0,1]
(uncalibrated scores/probabilities) and
y
i
∈
{
0
,
1
}
y_{i}\in\{0,1\}
(or more generally
y
i
∈
[
0
,
1
]
y_{i}\in[0,1]
). We seek a recalibration map
g
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
g:[0,1]\to[0,1]
, typically required to be
nondecreasing
.
For a discussion of interpretability and order-consistency desiderata (including why monotone
g
g
preserves ROC/AUC), see Section
4
and Proposition
4.2
.
We focus here on estimation aspects under shape constraints.
E.1
Isotonic regression (piecewise-constant monotone baseline)
Let
x
(
1
)
≤
⋯
≤
x
(
n
)
x_{(1)}\leq\cdots\leq x_{(n)}
denote the sorted inputs, with associated responses
y
(
i
)
y_{(i)}
.
The (weighted) isotonic regression estimator solves
min
θ
1
≤
⋯
≤
θ
n
⁡
1
2
​
∑
i
=
1
n
w
i
​
(
θ
i
−
y
(
i
)
)
2
,
w
i
≥
0
.
\min_{\theta_{1}\leq\cdots\leq\theta_{n}}\frac{1}{2}\sum_{i=1}^{n}w_{i}(\theta_{i}-y_{(i)})^{2},\qquad w_{i}\geq 0.
(2)
This yields fitted values
θ
^
i
\hat{\theta}_{i}
at the design points.
A function
g
iso
​
(
x
)
g_{\mathrm{iso}}(x)
is then obtained by a standard interpolation scheme, typically
piecewise constant
(right-continuous steps) over the sorted
x
(
i
)
x_{(i)}
.
Isotonic regression is the Euclidean projection of
(
y
(
i
)
)
(y_{(i)})
onto the isotone cone and can be computed efficiently by the pool-adjacent-violators (PAV) algorithm
[
Barlow et al., 1972
,
Robertson et al., 1988
,
Best and Chakravarti, 1990
]
.
E.2
Unconstrained smoothing baselines (kernel bandwidth
h
h
, spline basis size
k
k
)
This section lists two standard 1D smoothers without monotonicity constraints.
Kernel regression (bandwidth
h
h
).
The Nadaraya–Watson estimator is
g
^
h
​
(
x
)
=
∑
i
=
1
n
K
⁡
(
x
−
x
i
h
)
​
y
i
∑
i
=
1
n
K
⁡
(
x
−
x
i
h
)
,
h
>
0
,
\hat{g}_{h}(x)=\frac{\sum_{i=1}^{n}K\left(\frac{x-x_{i}}{h}\right)y_{i}}{\sum_{i=1}^{n}K\left(\frac{x-x_{i}}{h}\right)},\qquad h>0,
(3)
where
K
K
is a kernel (e.g., a compact “cubic”/triweight kernel
K
(
u
)
=
35
32
(
1
−
u
2
)
3
𝟏
{
|
u
|
≤
1
}
K(u)=\frac{35}{32}(1-u^{2})^{3}\mathbf{1}\{|u|\leq 1\}
). The smoothing level is controlled by
h
h
: smaller
h
h
yields less bias and more variance, and vice versa
[
Nadaraya, 1964
,
Watson, 1964
,
Wand and Jones, 1995
]
.
Cubic
P
P
-splines (basis dimension
k
k
and smoothing parameter
λ
\lambda
).
Let
B
1
,
…
,
B
k
B_{1},\dots,B_{k}
be a cubic B-spline basis on
[
0
,
1
]
[0,1]
(with chosen knots), and write
g
⁡
(
x
)
=
∑
j
=
1
k
β
j
​
B
j
​
(
x
)
g(x)=\sum_{j=1}^{k}\beta_{j}B_{j}(x)
. A standard penalized least squares problem is, for any
λ
≥
0
\lambda\geq 0
,
min
β
∈
ℝ
k
⁡
1
2
​
∑
i
=
1
n
w
i
​
(
y
i
−
∑
j
=
1
k
β
j
​
B
j
​
(
x
i
)
)
2
+
λ
2
​
‖
D
(
2
)
​
β
‖
2
2
,
\min_{\beta\in\mathbb{R}^{k}}\frac{1}{2}\sum_{i=1}^{n}w_{i}\Bigl(y_{i}-\sum_{j=1}^{k}\beta_{j}B_{j}(x_{i})\Bigr)^{2}+\frac{\lambda}{2}\|D^{(2)}\beta\|_{2}^{2},
(4)
where
D
(
2
)
D^{(2)}
is a second-difference matrix on coefficients. Here
k
k
controls the maximum flexibility (resolution) and
λ
\lambda
controls the effective smoothness
[
Eilers and Marx, 1996
]
.
E.3
Monotone
C
2
C^{2}
smoothing (kernel pre-smoothing + monotone cubic splines)
We describe a practical and stable construction yielding a globally nondecreasing and smooth (
C
2
C^{2}
) calibration map.
Step A (kernel pre-smoothing with bandwidth
h
h
).
Fix an increasing grid
t
1
<
⋯
<
t
k
t_{1}<\cdots<t_{k}
in
[
0
,
1
]
[0,1]
(e.g., evenly spaced). Define pseudo-observations
y
~
j
=
g
^
h
(
t
j
)
=
∑
i
=
1
n
K
⁡
(
t
j
−
x
i
h
)
​
y
i
∑
i
=
1
n
K
⁡
(
t
j
−
x
i
h
)
,
j
=
1
,
…
,
k
,
\tilde{y}_{j}=\hat{g}_{h}(t_{j})=\frac{\sum_{i=1}^{n}K\left(\frac{t_{j}-x_{i}}{h}\right)y_{i}}{\sum_{i=1}^{n}K\left(\frac{t_{j}-x_{i}}{h}\right)},\qquad j=1,\dots,k,
(5)
and “information” weights (kernel mass)
v
j
=
∑
i
=
1
n
K
⁡
(
t
j
−
x
i
h
)
.
v_{j}=\sum_{i=1}^{n}K\left(\frac{t_{j}-x_{i}}{h}\right).
(6)
This step is purely nonparametric and controlled by the bandwidth
h
h
.
Step B (monotone cubic spline with basis size
k
k
and smoothing
λ
\lambda
).
Let
B
1
,
…
,
B
k
B_{1},\dots,B_{k}
be a cubic B-spline basis on
[
0
,
1
]
[0,1]
and write
s
⁡
(
x
)
=
∑
ℓ
=
1
k
β
ℓ
​
B
ℓ
​
(
x
)
s(x)=\sum_{\ell=1}^{k}\beta_{\ell}B_{\ell}(x)
(hence
s
∈
C
2
s\in C^{2}
).
A common way to enforce global monotonicity is to impose linear inequality constraints on coefficients (or their differences), abstractly written as
A
​
β
⪰
0
,
A\beta\succeq 0,
(7)
where
A
A
encodes a sufficient condition for
s
′
​
(
x
)
≥
0
s^{\prime}(x)\geq 0
on
[
0
,
1
]
[0,1]
(e.g., using I-spline / integrated M-spline parametrizations or difference constraints in monotone P-spline constructions).
We then solve the convex quadratic program
min
β
∈
ℝ
k
⁡
1
2
​
∑
j
=
1
k
v
j
​
(
y
~
j
−
∑
ℓ
=
1
k
β
ℓ
​
B
ℓ
​
(
t
j
)
)
2
+
λ
2
​
‖
D
(
2
)
​
β
‖
2
2
\displaystyle\min_{\beta\in\mathbb{R}^{k}}\penalty\ \frac{1}{2}\sum_{j=1}^{k}v_{j}\Bigl(\tilde{y}_{j}-\sum_{\ell=1}^{k}\beta_{\ell}B_{\ell}(t_{j})\Bigr)^{2}+\frac{\lambda}{2}\|D^{(2)}\beta\|_{2}^{2}
s.t.
A
​
β
⪰
0
​
and
​
λ
≥
0
.
\displaystyle\quad\text{s.t.}\quad A\beta\succeq 0\text{ and }\lambda\geq 0.
(8)
The resulting map is
g
⁡
(
x
)
=
s
⁡
(
x
)
g(x)=s(x)
, optionally clamped to
[
0
,
1
]
[0,1]
.
Probability range via a logit link (recommended for calibration).
To guarantee
g
⁡
(
x
)
∈
(
0
,
1
)
g(x)\in(0,1)
, we fit a monotone spline on the logit scale:
η
⁡
(
x
)
=
∑
ℓ
=
1
k
β
ℓ
​
B
ℓ
​
(
x
)
,
g
⁡
(
x
)
=
sgmd
​
(
η
⁡
(
x
)
)
=
1
1
+
e
−
η
⁡
(
x
)
.
\eta(x)=\sum_{\ell=1}^{k}\beta_{\ell}B_{\ell}(x),\penalty\ \penalty\ g(x)=\text{sgmd}(\eta(x))=\frac{1}{1+e^{-\eta(x)}}.
(9)
Since
sgmd
is strictly increasing, monotonicity of
η
\eta
implies monotonicity of
g
g
.
Optimization / solver notes.
•
Gaussian/least-squares case:
(
8
) is a convex QP with linear inequalities.
It admits global solutions (no local minima). Uniqueness holds if the quadratic term is strictly convex (e.g., effective design + penalty yields a positive definite Hessian on the feasible set).
Efficient solvers include active-set QP and interior-point methods.
•
Binomial/logit case:
one typically minimizes a penalized negative log-likelihood under the same linear constraints on
β
\beta
, solved by
constrained IRLS
: each IRLS iteration solves a QP of the form (
8
) with updated working responses and weights. Shape-constrained GAM implementations follow this template
[
Pya and Wood, 2015
]
.
Simple properties (easy to state/derive).
•
Global monotonicity:
by construction
A
​
β
^
⪰
0
A\hat{\beta}\succeq 0
implies
s
′
​
(
x
)
≥
0
s^{\prime}(x)\geq 0
(or
η
′
​
(
x
)
≥
0
\eta^{\prime}(x)\geq 0
), hence
g
g
is nondecreasing on
[
0
,
1
]
[0,1]
.
•
C
2
C^{2}
smoothness:
cubic splines are
C
2
C^{2}
by construction; consequently
g
g
is
C
2
C^{2}
(on the link scale, and
g
=
sgmd
∘
η
g=\text{sgmd}\circ\eta
is smooth as well).
•
Convexity and global optimality (least squares):
(
8
) is convex with linear constraints; any feasible KKT point is globally optimal.
•
Limiting regimes:
increasing
λ
\lambda
shrinks curvature, approaching an (almost) affine monotone map; increasing
k
k
increases representational capacity, while
h
h
controls the upstream kernel smoothness.
E.4
Simulations
In order to illustrate, we generated some datasets
(
y
i
,
x
1
,
i
,
x
2
,
i
)
(y_{i},x_{1,i},x_{2,i})
, where
x
1
x_{1}
and
x
2
x_{2}
are obtained from independent
𝒰
⁡
(
[
0
,
1
]
)
\mathcal{U}([0,1])
random variables, where
y
y
is the realization of a Bernoulli random variable with mean
η
⁡
(
x
1
,
x
2
)
=
exp
⁡
[
x
1
+
x
2
+
ψ
⁡
(
x
1
,
x
2
)
]
1
+
exp
⁡
[
x
1
+
x
2
+
ψ
⁡
(
x
1
,
x
2
)
]
,
\eta(x_{1},x_{2})=\displaystyle{\frac{\exp[{x_{1}+x_{2}}+\psi(x_{1},x_{2})]}{1+\exp[{x_{1}+x_{2}}+\psi(x_{1},x_{2})]}},
with some non-linear function
ψ
\psi
, (here
ψ
⁡
(
x
1
,
x
2
)
=
exp
⁡
(
(
x
1
−
x
2
)
3
)
−
1
\psi(x_{1},x_{2})=\exp((x_{1}-x_{2})^{3})-1
). A plain logistic regression is fitted,
π
^
\widehat{\pi}
, on the left of Figure
6
. Then three recalibration mapping are estimated
-
piecewise constant isotonic (Section
E.1
), dark green,
-
standard
𝒞
2
\mathcal{C}^{2}
splines (Section
E.2
), dark red,
-
monotonic
𝒞
2
\mathcal{C}^{2}
splines (Section
E.3
), dark blue.
Figure 6:
Plain-logistic model fitted on simulated data
{
(
x
1
,
i
,
x
2
,
i
,
y
i
)
}
\{(x_{1,i},x_{2,i},y_{i})\}
, on the left, and two estimations
g
^
\hat{g}
, using an isotonic regression (in green), a
𝒞
2
\mathcal{C}^{2}
smoothing mapping (in red) and a monotone
𝒞
2
\mathcal{C}^{2}
smoothing mapping (in blue), on the middle left. On the right, evolution of
h
↦
h\mapsto
integrated calibration index (
ℓ
1
\ell_{1}
) on the middle right, and local calibration score (
ℓ
2
\ell_{2}
) for
g
^
h
\hat{g}_{h}
on the right, as a function of the bandwidth parameter
h
>
0
h>0
, for three values of
k
k
, and using 5-fold cross validation
To check for calibration, classical calibration metrics are
Brier Score
=
1
n
​
∑
i
=
1
n
(
s
^
​
(
𝐱
i
)
−
y
i
)
2
\displaystyle=\frac{1}{n}\sum_{i=1}^{n}\big(\hat{s}(\mathbf{x}_{i})-y_{i}\big)^{2}
Integrated Calibration Index
=
1
n
​
∑
i
=
1
n
|
s
^
​
(
𝐱
i
)
−
g
^
h
​
(
s
^
​
(
𝐱
i
)
)
|
\displaystyle=\frac{1}{n}\sum_{i=1}^{n}\big|\hat{s}(\mathbf{x}_{i})-\hat{g}_{h}\big(\hat{s}(\mathbf{x}_{i})\big)\big|
Local Calibration Score
=
1
n
​
∑
i
=
1
n
[
s
^
​
(
𝐱
i
)
−
g
^
h
​
(
s
^
​
(
𝐱
i
)
)
]
2
\displaystyle=\frac{1}{n}\sum_{i=1}^{n}\big[\hat{s}(\mathbf{x}_{i})-\hat{g}_{h}\big(\hat{s}(\mathbf{x}_{i})\big)\big]^{2}
see
[
Brier, 1950
,
Austin and Steyerberg, 2019
,
Zhang et al., 2020
,
Gupta et al., 2021
]
.