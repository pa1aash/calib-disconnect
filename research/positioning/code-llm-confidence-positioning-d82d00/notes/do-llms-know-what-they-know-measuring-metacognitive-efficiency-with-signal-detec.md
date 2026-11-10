---
title: Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal
  Detection Theory
id: do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec
tags:
- code-llm-confidence-positioning-d82d00
- metrology-framing
- calibration-metrics
- sdt
created: '2026-11-09T23:07:23.244516Z'
updated: '2026-11-09T23:27:44.349752Z'
source: https://arxiv.org/html/2603.25112
source_domain: arxiv.org
fetched_at: '2026-11-09T23:07:23.244196Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'CLOSE for F (metrology/instrument framing): applies Signal Detection Theory
  Type-2 analysis to LLM confidence on factual QA (not code). Full text (arXiv HTML
  v3). Cacioli (independent), arXiv 2603.25112v3 (28 Jul 2026), full text. Argues
  ECE/Brier conflate Type-1 accuracy with Type-2 metacognitive sensitivity; applies
  Signal Detection Theory to token-level normalised log-probability as confidence
  on factual QA (224,000 trials; Llama-3-8B-Instruct, Mistral-7B-Instruct-v0.3, Llama-3-8B-Base,
  Gemma-2-9B-Instruct; TriviaQA, Natural Questions). Introduces model-free meta-I_2r
  = I(correct;confidence)/H(correct) after retracting meta-d''/M-ratio as ill-defined
  for open QA. Findings: 1.98-fold cross-model range, z-ROC slopes 0.78-1.18 invisible
  to calibration metrics, temperature dissociates accuracy from metacognitive information,
  rho=+1.00 with abstention gain. v3 retracts v1/v2 inverse accuracy-efficiency coupling
  after a length-biased automated scorer was found (agreement with human labels 0.76
  to 0.86): a label-validity cautionary tale. NOT code, no probes, no execution labels;
  occupies ''psychophysics/SDT framing of LLM confidence'' for F but not code or execution
  ground truth.'
---

Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2603.25112v3 [cs.CL] 28 Jul 2026
Do LLMs Know What They Know?
Measuring Metacognitive Efficiency with Signal Detection Theory
Jon-Paul Cacioli
Affiliation:
Independent Researcher
Affiliation:
Melbourne, Australia
Email:
synthium@hotmail.com
Affiliation:
ORCID: 0009-0000-7054-2014
Abstract
Standard evaluation of LLM confidence relies on calibration metrics (ECE, Brier score) that conflate two distinct capacities: how much a model knows (Type-1 accuracy) and how well its confidence signal tracks that knowledge (Type-2 metacognitive sensitivity). We apply Signal Detection Theory (SDT) to decompose these capacities in large language models, treating token-level normalised log-probability as a graded confidence variable and answer correctness as the state to be discriminated. We characterise the Type-2 ROC of this signal, including its unequal-variance structure via z-ROC analysis, and—because the meta-
d
′
d^{\prime}
efficiency ratio is not well defined for open-ended QA, which lacks a two-alternative Type-1 decision—quantify metacognitive efficiency with a model-free information measure, normalised metacognitive information (meta-
I
2
​
r
I_{2r}
). Applied to four LLMs (Llama-3-8B-Instruct, Mistral-7B-Instruct-v0.3, Llama-3-8B-Base, Gemma-2-9B-Instruct) across 224,000 factual QA trials, we find: (1) metacognitive information varies by a factor of 1.98 across models and is not predicted by accuracy—the rank correlation is
−
0.80
{-}0.80
on TriviaQA and
+
0.00
{+}0.00
on Natural Questions, and Gemma-2 is reliably the least informative on both; (2) the confidence signal has model-specific unequal-variance structure (z-ROC slopes from 0.78 to 1.18) that is invisible to calibration metrics, with the slope ordering replicating on Natural Questions; (3) metacognitive information is domain-specific, weakest in Science & Technology for every model; (4) temperature dissociates Type-1 accuracy from metacognitive information, which stays near-flat for three of four models while accuracy falls; and (5) metacognitive information tracks the accuracy gain from confidence-based abstention exactly (
ρ
=
+
1.00
\rho={+}1.00
) while accuracy does not. All estimates carry permutation nulls and bootstrap confidence intervals.
This version (v3) corrects a differential length bias in the automated correctness scorer; the inverse accuracy–efficiency coupling reported in v1 and v2 does not survive that correction. See the version note.
Pre-registered analysis; code and data publicly available.
1
1
footnotetext:
Version note (v3).
The correctness labels used in
v1 and v2 were produced by an automated scorer (exact match against verified
aliases, then a string-similarity threshold) that has since been found to be
differentially
length-biased. Validated against 1,200 human
adjudications, the scorer missed 53% of one model’s human-correct answers and
26% of another’s, because it fails on answers that contain the correct alias
inside a longer sentence and the models differ substantially in verbosity. A
containment fallback — accepting a match when the normalised token sequence of
any alias appears contiguously in the normalised answer — raises agreement
with human labels from 0.76 to 0.86 at a false-positive cost of 1.4%
(adjudicated on a further 630 blinded responses). All analyses in this version
are recomputed on the corrected labels.
What changes.
Accuracy rises for every model, by between 2.7 and 13.3
points, and the accuracy ordering changes. The cross-model efficiency ordering
does not survive: Mistral moves from the highest meta-
I
2
​
r
I_{2r}
to the third of
four, and the inverse coupling with accuracy weakens from
ρ
=
−
1.00
\rho={-}1.00
to
ρ
=
−
0.80
\rho={-}0.80
on TriviaQA and disappears on Natural Questions
(
ρ
=
+
0.00
\rho={+}0.00
). The two-fold cross-model range becomes 1.98-fold. Section 4.3
is rewritten accordingly.
What survives.
The Type-2 SDT structure and
its slope ordering, replicating on NQ; the NLP monotonicity and z-ROC linearity
checks; domain-specificity, with Science & Technology weakest for all four
models; the temperature dissociation; and the selective-prediction result,
which strengthens (
ρ
=
+
1.00
\rho={+}1.00
between meta-
I
2
​
r
I_{2r}
and abstention gain,
against
+
0.80
{+}0.80
in v2). Residual differential scoring error remains, so the
corrected values should be treated as better than v2’s rather than as final.
An earlier version of this paper estimated metacognitive efficiency using meta-
d
′
d^{\prime}
/
M
M
-ratio. That estimator requires a two-alternative Type-1 detection decision, which open-ended factual QA does not provide; forcing the mapping makes
d
′
d^{\prime}
and meta-
d
′
d^{\prime}
functions of the same correctness-by-confidence table, so
M
M
-ratio is pinned near 1 by construction and reported cross-model
M
M
-ratio differences reflect departures from the equal-variance assumption rather than metacognitive efficiency. This version replaces
M
M
-ratio throughout with a model-free measure (meta-
I
2
​
r
I_{2r}
) and reports the Type-2 SDT structure (AUROC
2
, z-ROC slope,
d
a
d_{a}
) directly. All analyses were re-run on the same 224,000-trial dataset. The domain-specificity and temperature-dissociation findings are unchanged; the direction of the cross-model efficiency finding reverses under the corrected measure.
1
Introduction
When a large language model (LLM) answers a factual question, two capacities determine the reliability of its output: its ability to discriminate correct from incorrect responses, and its ability to
monitor
that discrimination through its confidence signal. These are fundamentally different problems requiring different interventions. A model that cannot discriminate needs better training data or architectural improvements. A model that discriminates well but monitors poorly needs recalibration, not retraining. Current evaluation practice does not make this distinction.
Consider two hypothetical models evaluated on the same factual QA benchmark. Model A reports 90% confidence on every trial and achieves 90% accuracy; its Expected Calibration Error (ECE) is near zero. Model B reports 95% confidence when correct and 60% when incorrect, but its average confidence overshoots its 80% accuracy; its ECE is worse than Model A’s. Yet Model B’s confidence is
far more useful
: it tells you which specific answers to trust. Model A’s confidence, despite perfect calibration, carries no information about correctness. The standard ECE metric rewards the wrong model.
This example illustrates a well-known limitation of ECE
(
Guo et al., 2017
)
: it measures the average alignment between confidence and accuracy, conflating the
resolution
of the confidence signal (how well it separates correct from incorrect) with its
bias
(the overall level of confidence). The Brier score decomposes into reliability, resolution, and uncertainty, but not into the model’s discriminative capacity and its metacognitive sensitivity controlling for that capacity. The Area Under the Type-2 ROC (AUROC
2
) of the confidence–accuracy curve
(
Steyvers and Peters, 2025
)
improves on ECE by measuring ranking quality. It does not normalise for the base rate of correct responses; the information-theoretic measure we adopt does, though we note (§
4
) that on a sample whose accuracies yield near-identical base-rate entropies the normalisation is numerically inert and the two measures coincide.
Signal Detection Theory (SDT;
Green and Swets 1966
;
Macmillan and Creelman 2005
) provides the natural framework for this decomposition. Developed over seven decades of psychophysical research, SDT separates performance into
sensitivity
(how well an observer discriminates two states) and
criterion
(the observer’s threshold for responding).
Cacioli (2026)
demonstrated that the parametric SDT framework—ROC analysis, unequal-variance model fitting, criterion estimation—reveals structure in LLM confidence invisible to calibration metrics alone.
The present work applies SDT at the
Type-2
level: how well does a model’s confidence signal discriminate its own correct from incorrect answers? We treat token-level normalised log-probability (NLP) as a graded confidence variable and characterise the Type-2 ROC it produces, including its unequal-variance structure. For the
efficiency
question—how much of the available correctness information the confidence signal captures—we use a model-free information-theoretic measure rather than the meta-
d
′
d^{\prime}
ratio, for reasons we make explicit in §
2.3
: open-ended QA has no two-alternative Type-1 decision, so meta-
d
′
d^{\prime}
is not well defined without reintroducing assumptions the data do not support.
We quantify metacognitive efficiency using the mutual-information approach of
Dayan (2023)
, who introduced meta-
I
I
(the mutual information between choice accuracy and confidence) and normalised variants that quantify efficiency. We use the accuracy-entropy normalisation, which we denote meta-
I
2
​
r
I_{2r}
:
1
1
1
Notation ours.
Dayan (2023)
defines meta-
I
I
and several normalisations; meta-
I
2
​
r
I_{2r}
here refers specifically to the ratio of transmitted information to accuracy entropy in Eq.
1
.
Fitousi (2025)
empirically validates this family of information-theoretic efficiency measures.
meta-
​
I
2
​
r
=
I
⁡
(
correct
,
confidence
)
H
⁡
(
correct
)
,
\text{meta-}I_{2r}=\frac{I(\text{correct}\,;\,\text{confidence})}{H(\text{correct})},
(1)
the mutual information between binary correctness and the discretised confidence variable, normalised by the entropy of accuracy. meta-
I
2
​
r
I_{2r}
is 0 when confidence is uninformative about correctness and approaches its ceiling when confidence fully resolves the correct/incorrect distinction. It is model-free: it assumes no Gaussian evidence distribution, requires no Type-1 decision, and is defined identically for two-way,
n
n
-way, and open-ended tasks. Because plug-in mutual information is upward biased at finite sample sizes, every estimate is bias-corrected against a permutation null and reported with a bootstrap confidence interval.
Our contributions are:
1.
We give a Type-2 SDT characterisation of the LLM confidence signal—AUROC
2
, z-ROC slope, and unequal-variance sensitivity
d
a
d_{a}
—and show the signal has model-specific variance structure invisible to ECE.
2.
We introduce meta-
I
2
​
r
I_{2r}
as a model-free metacognitive-efficiency measure for LLM confidence, appropriate where meta-
d
′
d^{\prime}
is undefined, and show it reveals a model that has the lowest accuracy yet the highest metacognitive information.
3.
We show metacognitive efficiency is domain-specific, and that temperature dissociates Type-1 accuracy from metacognitive information.
4.
All analyses are pre-registered, with permutation nulls, bootstrap CIs, and a Natural Questions replication; code and data are public.
The contribution is an evaluation methodology, not a dataset or benchmark. Limitations of scope—four open-weight 7–9B models, two factual QA datasets, quantised inference—are detailed in §
5.4
.
2
Background: Type-2 Signal Detection Theory
2.1
The confidence signal as a Type-2 detector
In the Type-1 SDT framework applied to LLM factual QA
(
Cacioli, 2026
)
, each question is a trial in which the model generates an answer. The normalised log-probability (NLP) of the generated answer serves as the evidence variable:
NLP
=
(
1
/
L
)
​
∑
i
=
1
L
log
⁡
p
⁡
(
t
i
∣
t
<
i
)
\text{NLP}=(1/L)\sum_{i=1}^{L}\log p(t_{i}\mid t_{<i})
, where
L
L
is the answer length in tokens. Higher NLP indicates greater model confidence.
The Type-2 question
(
Galvin et al., 2003
)
is how well this confidence signal discriminates the model’s own correct from incorrect responses. Given the binary correctness of each trial and the graded NLP, the Type-2 ROC plots the hit rate (proportion of correct answers above a confidence criterion) against the false-alarm rate (proportion of incorrect answers above it), swept across criteria. The area under this curve, AUROC
2
, is a non-parametric measure of how well confidence separates correct from incorrect answers, and requires no distributional assumptions.
2.2
Unequal-variance structure via z-ROC
The
shape
of the Type-2 ROC carries information beyond its area. Under the Gaussian SDT model, plotting the ROC in
z
z
-coordinates (probit-transformed hit and false-alarm rates) yields a straight line whose slope
s
s
equals the ratio of the standard deviations of the two underlying evidence distributions
(
Green and Swets, 1966
;
Macmillan and Creelman, 2005
)
. A slope
s
=
1
s=1
indicates equal variance;
s
<
1
s<1
indicates the correct-answer evidence distribution is more variable than the incorrect-answer distribution, and
s
>
1
s>1
the reverse. The unequal-variance sensitivity index
d
a
=
2
/
(
1
+
s
2
)
⋅
(
z-intercept
)
d_{a}=\sqrt{2/(1+s^{2})}\,\cdot\,(\text{z-intercept})
summarises sensitivity while respecting this asymmetry. These are properties of the empirical ROC, estimated directly by regression on the z-ROC, and involve no ideal-observer inversion.
2.3
Why not meta-
d
′
d^{\prime}
?
The standard Type-2 efficiency measure is meta-
d
′
d^{\prime}
(
Maniscalco and Lau, 2012
;
Maniscalco and Lau, 2014
)
, which asks what Type-1 sensitivity an ideal observer would need to reproduce an observed pattern of confidence ratings, normalised as the ratio
M
=
meta-
​
d
′
/
d
′
M=\text{meta-}d^{\prime}/d^{\prime}
(
Fleming and Lau, 2014
)
. meta-
d
′
d^{\prime}
is defined for a two-alternative detection task: it requires a Type-1 decision (respond “S1” vs “S2”) whose sensitivity
d
′
d^{\prime}
supplies the denominator, and a confidence report layered on that decision. Free-form factual QA has neither. There is no signal-absent trial and no binary Type-1 response; the model always emits an answer, and NLP is the only graded internal signal. Forcing the mapping—treating correctness as the S1/S2 variable and confidence bins as the rating—makes the estimated
d
′
d^{\prime}
and meta-
d
′
d^{\prime}
functions of the
same
correctness-by-confidence table, so
M
M
is pinned near 1 by construction and reflects only departures from the equal-variance assumption rather than metacognitive efficiency. This is not a limitation of SDT but of one Type-2 estimator applied outside its domain; recent measurement work reaches the same conclusion for
n
n
-choice tasks generally
(
Rahnev, 2025
)
. Our own data make the point concrete: the
M
M
-ratio values a naive application produces are rank-ordered almost perfectly by the z-ROC slope
s
s
of the same models (Spearman
ρ
=
+
0.95
\rho=+0.95
; §
2.2
, Table
2
), confirming that in this paradigm
M
M
tracks the unequal-variance structure of the confidence ROC and not a metacognitive-efficiency quantity. We therefore report the Type-2 ROC structure directly (§
2.2
) and use a model-free efficiency measure (§
2.4
).
2.4
Metacognitive information as a model-free efficiency measure
Normalised metacognitive information (Eq.
1
;
Dayan 2023
) measures how much the confidence signal reduces uncertainty about correctness, as a fraction of the total uncertainty in correctness. It is model-free and defined for any task, and has been validated as a metacognition measure with explicit multi-alternative applicability
(
Fitousi, 2025
)
. We report it with a permutation null (shuffling confidence against correctness) to control the upward bias of plug-in mutual information, and with trial-level bootstrap confidence intervals.
2.5
Why NLP is a valid confidence variable
Verbalised confidence—prompting a model to report a numerical certainty score—is the dominant paradigm for LLM uncertainty estimation in black-box settings
(
Xiong et al., 2024
)
. However,
Dai (2026)
demonstrate that verbalised confidence suffers from severe discretisation: more than 78% of responses on a 0–100 scale concentrate on three round-number values, producing sparse and unreliable estimates. Token-level log-probabilities, by contrast, provide a continuous confidence variable that is a direct output of the model’s generative process. NLP is not a pure “metacognitive signal” in any cognitive sense; it is a fluency measure that reflects both the quality of the generated answer and the model’s distributional properties
(
Cacioli, 2026
)
. We adopt a
functional
operationalisation: metacognitive monitoring is the discriminability of an internal signal for correctness, without requiring a distinct second-order system. This parallels the use of Type-2 measures in animal metacognition research
(
Smith et al., 2014
)
. As an empirical validation, we verify that NLP is monotonically related to accuracy across all conditions (§
4
, Appendix
A
).
3
Method
3.1
Models and Data
Four LLMs spanning three model families were evaluated: Llama-3-8B-Instruct and Llama-3-8B-Base (Meta;
Meta AI 2024
), Mistral-7B-Instruct-v0.3
(
Jiang and others, 2023
)
, and Gemma-2-9B-Instruct (Google;
Gemma Team 2024
). All were run as Q5_K_M quantisations via
llama-cpp-python
0.3.16 with Vulkan backend on an AMD RX 7900 GRE (16 GB VRAM).
Table 1:
Model summary. All models run as Q5_K_M GGUF quantisations.
Model
Family
Params
Instruct
Quant size
Llama-3-8B-Instruct
Meta
8B
Yes
5.7 GB
Llama-3-8B-Base
Meta
8B
No
5.7 GB
Mistral-7B-Instruct-v0.3
Mistral AI
7B
Yes
5.1 GB
Gemma-2-9B-Instruct
Google
9B
Yes
6.7 GB
Two factual question-answering datasets were used.
TriviaQA
(
Joshi et al., 2017
)
: 5,000 questions from the unfiltered set (seed = 42), classified into four knowledge domains: History & Politics (1,248), Arts & Literature (1,167), Geography (667), Science & Technology (634), plus Unclassified (1,284; excluded from domain analyses).
Natural Questions
(
Kwiatkowski and others, 2019
)
: 3,000 short-answer questions from NQ-Open, a replication dataset. Each model answered each question at seven temperatures
T
∈
{
0.1
,
0.3
,
0.5
,
0.7
,
1.0
,
1.5
,
2.0
}
T\in\{0.1,0.3,0.5,0.7,1.0,1.5,2.0\}
, yielding 224,000 trials. Per trial we recorded the generated answer, NLP, and binary correctness (exact match against verified aliases,
difflib.SequenceMatcher
≥
0.85
\geq 0.85
fallback). Data for the three original models were collected under a prior pre-registration
(
Cacioli, 2026
)
; Gemma-2 was added post-registration following the identical protocol.
3.2
Pipeline
Confidence binning.
NLP values are binned into
2
​
K
2K
ordered categories (
K
=
4
K=4
), with edges at the
{
12.5
,
…
,
87.5
}
\{12.5,\ldots,87.5\}
th quantiles of the NLP distribution at
T
=
1.0
T=1.0
within each model
×
\times
dataset condition, held constant across temperatures.
Measures.
For each analysis cell we compute (i) AUROC
2
; (ii) the z-ROC slope
s
s
and
d
a
d_{a}
by linear regression on the probit-transformed empirical Type-2 ROC (§
2.2
); and (iii) meta-
I
2
​
r
I_{2r}
(Eq.
1
), bias-corrected against a permutation null of 2,000 confidence–correctness shuffles.
Inference.
All confidence intervals are 95% bootstrap percentile intervals from 2,000 trial-level resamples (seed = 42); each resample recomputes the full pipeline.
3.3
Pre-Registered Hypotheses
Analyses for the three original models were pre-registered (OSF:
https://osf.io/5q7mt
); Gemma-2 is a post-registration generalisability test. Hypotheses are tested at
T
=
1.0
T=1.0
on TriviaQA.
H1
(cross-model variation): metacognitive efficiency varies across models.
H2
(domain-specificity): efficiency varies across TriviaQA domains.
H3
(temperature dissociation): metacognitive efficiency is stable while Type-1 accuracy varies across
T
∈
{
0.3
,
0.5
,
0.7
,
1.0
}
T\in\{0.3,0.5,0.7,1.0\}
.
H4
(efficiency not determined by accuracy): the ranking of models by metacognitive efficiency differs from their ranking by accuracy. (The pre-registration specified these hypotheses in terms of meta-
d
′
d^{\prime}
/
M
M
-ratio; we test the identical conceptual claims with meta-
I
2
​
r
I_{2r}
, for the reasons in §
2.3
.)
4
Results
4.1
Validation
All eight model
×
\times
dataset conditions at
T
=
1.0
T{=}1.0
passed the NLP monotonicity check: accuracy increased strictly across NLP quartiles (Appendix
A
). All z-ROC fits were highly linear (
R
2
≥
0.98
R^{2}\geq 0.98
), supporting the Gaussian SDT model for the confidence signal.
4.2
SDT structure of the confidence signal (H1, structure)
Table 2:
SDT structure of the Type-2 (correct/incorrect) confidence ROC at
T
=
1.0
T{=}1.0
,
corrected labels
.
s
s
is the z-ROC slope (ratio of incorrect-to-correct evidence SD);
s
<
1
s<1
indicates the correct-answer evidence distribution is more variable.
d
a
d_{a}
is the unequal-variance sensitivity index. Slopes from linear regression on the empirical z-ROC (
R
2
=
0.988
R^{2}=0.988
–
1.000
1.000
across cells); the ordering of
s
s
replicates on NQ. Values in v2 are given in parentheses.
Model
AUROC
2
z-ROC slope
s
s
𝒅
𝒂
\boldsymbol{d_{a}}
s
s
(NQ)
Llama-3-Instruct
0.833
(0.831)
0.905
(0.863)
1.354
(1.385)
0.936
(0.852)
Mistral-Instruct
0.792
(0.855)
0.779
(0.812)
1.123
(1.475)
0.869
(0.644)
Llama-3-Base
0.847
(0.839)
1.182
(1.179)
1.472
(1.463)
1.297
(1.243)
Gemma-2-Instruct
0.760
(0.747)
1.014
(0.992)
0.996
(0.964)
1.176
(1.181)
Table
2
and Figure
1
report the Type-2 SDT structure. The confidence signal has pronounced, model-specific unequal-variance structure. Mistral and Llama-3-Instruct have z-ROC slopes below 1 (0.81, 0.86; bootstrap CIs exclude 1), indicating the correct-answer evidence distribution is more variable than the incorrect. Llama-3-Base has the opposite structure (
s
=
1.18
s=1.18
, CI excludes 1) and Gemma-2 is close to equal variance (
s
=
0.99
s=0.99
). The ordering of slopes replicates on NQ (Table
2
, final column). This structure is a genuine property of how each model represents correct versus incorrect answers, and is invisible to ECE and to AUROC
2
alone.
Figure 1:
Type-2 z-ROC (TriviaQA,
T
=
1.0
T{=}1.0
), corrected labels. Points are empirical (hit, false-alarm) pairs in probit coordinates; lines are SDT fits (
R
2
=
0.988
R^{2}=0.988
–
1.000
1.000
). Slopes below 1 (Mistral 0.78, Llama-3-Instruct 0.91) indicate greater variance in correct-answer evidence; Llama-3-Base is above 1 (1.18) and Gemma-2 near equal variance (1.01). The ordering replicates on Natural Questions.
4.3
Metacognitive information varies across models and co-varies with accuracy (H1, H4)
Table 3:
Aggregate metacognition at
T
=
1.0
T{=}1.0
,
corrected labels
, ordered by accuracy. meta-I
2r
is bias-corrected (permutation null subtracted); 95% bootstrap CIs from 2,000 trial-level resamples. All meta-I
2r
exceed the permutation null (
p
<
0.001
p<0.001
). Values reported in v2 are given in parentheses; see the version note for why they differ.
Model
Acc
meta-I
2r
95% CI
AUROC
2
meta-I
2r
(NQ)
Llama-3-Base
0.478
(0.428)
0.300
(0.292)
[0.282, 0.322]
0.847
0.145
(0.140)
Mistral-Instruct
0.560
(0.427)
0.206
(0.328)
[0.189, 0.226]
0.792
0.085
(0.243)
Llama-3-Instruct
0.584
(0.543)
0.263
(0.276)
[0.244, 0.284]
0.833
0.157
(0.192)
Gemma-2-Instruct
0.627
(0.600)
0.151
(0.143)
[0.135, 0.170]
0.760
0.108
(0.108)
Metacognitive information varies by a factor of 1.98 across models
(meta-
I
2
​
r
I_{2r}
0.151–0.300 on TriviaQA; Table
3
). All four
estimates exceed their permutation null (
p
<
0.001
p<0.001
).
In v2, computed on the uncorrected labels, this section reported that the least
accurate model (Mistral) had the most informative confidence and the most
accurate (Gemma-2) the least, with meta-
I
2
​
r
I_{2r}
and accuracy perfectly
inversely rank-ordered (
ρ
=
−
1.00
\rho={-}1.00
). That finding does not survive label
correction. Mistral’s accuracy was understated by 13.3 points, and on corrected
labels it falls from the highest meta-
I
2
​
r
I_{2r}
(0.328) to the third of four
(0.206). The ordering is now Llama-3-Base
>
>
Llama-3-Instruct
>
>
Mistral
>
>
Gemma-2. The rank correlation with accuracy weakens to
ρ
=
−
0.80
\rho={-}0.80
on
TriviaQA and vanishes on Natural Questions (
ρ
=
+
0.00
\rho={+}0.00
), where the ordering
is different again.
What remains is that cross-model variation in confidence informativeness is
substantial and permutation-significant, that Gemma-2 is reliably the least
informative on both datasets, and that the ordering is not predicted by
accuracy. We no longer claim an inverse coupling. The caveat raised in v2 —
that a more accurate model’s residual errors are harder near-misses and
therefore intrinsically less detectable — is not needed to explain an effect
that is largely absent once the labels are corrected; the apparent coupling was
substantially an artefact of a scorer that penalised the most verbose model.
Figure 2:
Metacognitive information vs. accuracy, both datasets, corrected
labels. Error bars are 95% bootstrap CIs. The monotone inverse relationship
reported in v2 is not present: the rank correlation is
−
0.80
{-}0.80
on TriviaQA
and
+
0.00
{+}0.00
on Natural Questions.
meta-
I
2
​
r
I_{2r}
remains rank-identical to AUROC
2
on both datasets
(
ρ
=
+
1.00
\rho={+}1.00
). The explanation offered in v2 — that the four base-rate
entropies fall within 2.4% of one another — no longer holds on corrected
labels, where the spread is 4.6% on TriviaQA and 23.3% on NQ. The two
measures coincide here despite that spread; we report meta-
I
2
​
r
I_{2r}
because it
is the model-free efficiency measure defined where meta-
d
′
d^{\prime}
is not
(§
2.3
), and note that AUROC
2
would support the same
conclusions on this sample.
4.4
Domain-specific metacognitive information (H2)
Table 4:
Domain-specific meta-
I
2
​
r
I_{2r}
at
T
=
1.0
T{=}1.0
on TriviaQA,
corrected labels
, all six classified domains. Boldface: weakest domain per model;
underlined
: strongest. v2 reported only the four domains above the rule and stated that Arts & Literature was strongest for every model; that holds within those four but not once Pop Culture and Sports are included.
Domain
Llama-Inst
Mistral
Base
Gemma
History & Politics
0.244
0.192
0.297
0.143
Arts & Literature
0.314
0.213
0.324
0.191
Geography
0.241
0.184
0.284
0.084
Science & Technology
0.140
0.148
0.256
0.079
Pop Culture & Ent.
0.345
0.303
0.331
0.275
Sports
0.350
0.213
0.269
0.127
Figure 3:
Domain-specific meta-
I
2
​
r
I_{2r}
at
T
=
1.0
T{=}1.0
on TriviaQA, corrected labels, all six classified domains (95% bootstrap CIs). Science & Technology is the weakest domain for every model. The strongest is Pop Culture & Entertainment for three models and Sports for Llama-3-Instruct; v2 reported Arts & Literature as strongest, which holds only among the four domains it tabulated.
Metacognitive information varies systematically across domains within each model (Table
4
, Figure
3
). Science & Technology is the weakest domain for all four models on corrected labels — a stronger and more uniform result than v2 reported, which had Geography weakest for Gemma-2. The strongest domain is Pop Culture & Entertainment for three models and Sports for Llama-3-Instruct. v2 stated that Arts & Literature was strongest for every model; that holds among the four domains v2 tabulated, but not once Pop Culture and Sports are included, and we correct the claim here. Domain ranges remain model-dependent (Gemma-2 spans 0.079–0.275, Llama-3-Base 0.256–0.331). A model whose confidence is informative in one domain and uninformative in another poses a deployment risk that aggregate metrics conceal.
4.5
Temperature dissociates accuracy from metacognitive information (H3)
Figure 4:
meta-
I
2
​
r
I_{2r}
(coloured, dashed) and accuracy (grey, solid) vs. temperature on TriviaQA, corrected labels. Accuracy falls with temperature for all four models, monotonically for Llama-3-Base and Llama-3-Instruct and near-monotonically for the other two; metacognitive information is near-flat for three of four, dissociating the two. Llama-3-Base is the exception, its confidence becoming markedly more informative as accuracy falls.
Temperature dissociates Type-1 accuracy from metacognitive information (Figure
4
). Accuracy decreases with temperature for all four models, monotonically for
Llama-3-Base and Llama-3-Instruct (
ρ
⁡
(
acc
,
T
)
=
−
1.00
\rho(\text{acc},T)=-1.00
) and near-monotonically
for Gemma-2 (
−
0.93
-0.93
) and Mistral (
−
0.82
-0.82
); v2 reported
−
1.00
-1.00
for all four,
which does not hold on corrected labels. Metacognitive information is near-flat
for three of four (meta-
I
2
​
r
I_{2r}
range 0.009 for Mistral, 0.016 for
Llama-3-Instruct and 0.027 for Gemma-2 across
T
∈
{
0.3
,
0.5
,
0.7
,
1.0
}
T\in\{0.3,0.5,0.7,1.0\}
),
moving in a different direction from accuracy. Llama-3-Base is again the
exception (range 0.103), the only model whose confidence informativeness
changes materially with temperature. Temperature reshapes what a model gets right without, for most models, changing how well its confidence tracks correctness.
4.6
Selective prediction (deployment consequence)
The cross-model variation in confidence informativeness has a direct deployment consequence for selective prediction, where a system abstains on low-confidence responses. What metacognitive information predicts is the
gain
from confidence-based selection, not the absolute accuracy attained—the latter is dominated by base accuracy. This is also where the accuracy confound above matters less: gain is measured within each model, so it is not driven by the cross-model accuracy differences that confound the aggregate ordering. At 50% coverage (accepting the top half of responses ranked by NLP),
Llama-3-Base improves from 47.8% to 74.0% (
+
26.3
+26.3
points) and
Llama-3-Instruct from 58.4% to 82.8% (
+
24.4
+24.4
), while Gemma-2, with the least
informative confidence, gains least (62.7% to 80.1%,
+
17.4
+17.4
). Across the
four models, meta-
I
2
​
r
I_{2r}
tracks the selective-prediction gain exactly on
corrected labels (Spearman
ρ
=
+
1.00
\rho={+}1.00
, against
+
0.80
+0.80
in v2) and not the
accuracy level (
ρ
=
−
0.40
\rho={-}0.40
), which follows base accuracy instead. This is the
one result that strengthens under correction. A model with high accuracy but low metacognitive information (Gemma-2) reaches a high accuracy level under selection yet extracts little additional value from its own confidence; a model with lower accuracy but informative confidence (Mistral) benefits most from abstention. Neither pattern is visible from accuracy or ECE alone (full accuracy–coverage curves in Appendix
B
).
5
Discussion
5.1
What an SDT analysis adds to LLM evaluation
Confidence evaluation operates at three tiers.
Tier 1
(ECE, Brier score) measures alignment, conflates sensitivity with bias, and is unstable under discretisation.
Tier 2
(AUROC
2
, rank correlations) measures ranking quality; it does not normalise for the base rate, though on this sample the two measures rank identically regardless.
Tier 3
(meta-
I
2
​
r
I_{2r}
, and the z-ROC structure of the confidence signal) measures how informative the confidence signal is about correctness with a model-free estimator valid where meta-
d
′
d^{\prime}
is not. Our results make the practical consequence concrete: the confidence signals of different models have qualitatively different variance structure (
s
s
from 0.78 to 1.18), and confidence informativeness varies by a factor of 1.98 across models—both invisible to ECE. On corrected labels the cross-model ordering is not predicted by accuracy (§
4
); the contributions that survive relabelling are the demonstrated variance structure, the domain and temperature effects, and the selective-prediction result.
5.2
Temperature, criterion, and metacognitive capacity
The dissociation between temperature and metacognitive information has implications for temperature tuning. For three of four models, temperature moves Type-1 accuracy without changing how well confidence tracks correctness. If a model’s confidence is uninformative, lowering temperature to raise accuracy will not make its confidence more useful for selective prediction. For Llama-3-Base, where the dissociation does not hold, temperature does change the information content of confidence itself.
5.3
Connections to human metacognition
The phenomena parallel human metacognition, where metacognitive efficiency is domain-specific
(
Rouault et al., 2018
)
, dissociable from Type-1 performance
(
Fleming et al., 2010
)
, and neurally distinct from perceptual decisions
(
Fleming and Dolan, 2012
)
. Our findings parallel these results functionally, not mechanistically: we do not claim LLMs possess metacognition phenomenologically. The measure differs from the human meta-
d
′
d^{\prime}
literature because open-ended QA lacks a Type-1 decision (§
2.3
); the value lies in the decomposition, consistent with the use of SDT in medical diagnosis
(
Swets, 1996
)
and automated system evaluation
(
Bartlett and McCarley, 2017
)
.
5.4
Limitations
Residual scoring error.
The containment correction applied in this
version recovers roughly half the gap to human accuracy and halves the
cross-model differential, but does not remove it: adjudicating a further 630
blinded responses across seven models, 18.4% of trials the corrected scorer
still rejects are in fact correct, and this residual rate remains
model-dependent by a factor of 2.4. The values reported here are therefore
better than v2’s but should not be treated as final, and fine-grained
cross-model orderings should be read with that in mind.
Four open-weight 7–9B models; generalisability to frontier scale is unknown. API models that do not expose token-level log-probabilities cannot be evaluated with internal NLP; the verbal-confidence approach of
Dai (2026)
is a complementary path. All models ran as Q5_K_M quantisations; however, all measures depend on the
ordinal
relationship between NLP and accuracy, which quantisation preserves, and the monotonicity check confirms this in all conditions. meta-
I
2
​
r
I_{2r}
belongs to a family of information-theoretic metacognition measures
(
Dayan, 2023
;
Fitousi, 2025
)
with several normalisation choices; we use normalisation by accuracy entropy and report permutation nulls throughout to guard against the small-sample bias of plug-in mutual information. NLP is a fluency measure, not a pure metacognitive signal; a high meta-
I
2
​
r
I_{2r}
does not imply the model “knows that it knows” in any deep sense.
5.5
Recommendations for practice
1.
Report meta-
I
2
​
r
I_{2r}
(with a permutation null) alongside ECE; they are complementary.
2.
Report the z-ROC slope of the confidence signal: unequal variance is a real, model-specific property.
3.
Disaggregate by domain; aggregate metrics hide domain-specific metacognitive deficits.
4.
For confidence-dependent systems, prefer higher metacognitive information over lower ECE.
5.
Evaluate temperature effects on metacognitive information, not just calibration.
6
Conclusion
We have applied Signal Detection Theory to LLM confidence, characterising the Type-2 ROC of the confidence signal and its unequal-variance structure, and—because the meta-
d
′
d^{\prime}
efficiency ratio is undefined for open-ended QA—quantifying metacognitive efficiency with a model-free information measure, meta-
I
2
​
r
I_{2r}
. Across four models and 224,000 trials, metacognitive information varies by a
factor of 1.98 and is not predicted by accuracy: the inverse coupling reported
in earlier versions of this paper was substantially an artefact of a
differentially length-biased correctness scorer, and does not survive
relabelling. The confidence signal has model-specific variance structure, efficiency is domain-specific, and temperature dissociates accuracy from metacognitive information. Current practice treats confidence as monolithic; an SDT decomposition shows this is insufficient. All analyses are pre-registered, with code and data publicly available.
2
2
2
Pre-registration:
https://osf.io/5q7mt
. Code and data:
https://github.com/synthiumjp/sdt_calibration
. The corrected scorer, the
1,830 human adjudications used to validate it, and the recomputation scripts
for this version:
https://github.com/synthiumjp/metacognition-audit
.
Use of Generative AI.
Claude (Anthropic) was used as a research assistant for analysis pipeline design and code generation. All scientific decisions, hypothesis formulation, and interpretive judgments were made by the author.
References
Bartlett and McCarley (2017)
M. L. Bartlett and J. S. McCarley
Signal detection theory analysis of automated system performance
.
Human Factors
59
(
7
),
pp. 1010–1030
.
Cited by:
§5.3
.
Cacioli (2026)
J. Cacioli
LLMs as signal detectors: sensitivity, bias, and the temperature–criterion analogy
.
arXiv preprint arXiv:2603.14893
.
Cited by:
§1
,
§2.1
,
§2.5
,
§3.1
.
Dai (2026)
Y. Dai
Rescaling confidence: what scale design reveals about LLM metacognition
.
arXiv preprint arXiv:2603.09309
.
Cited by:
§2.5
,
§5.4
.
Dayan (2023)
P. Dayan
Metacognitive information theory
.
Open Mind
7
,
pp. 392–411
.
External Links:
Document
Cited by:
§1
,
§2.4
,
§5.4
,
footnote 1
.
Fitousi (2025)
D. Fitousi
Information-theoretic measures of metacognitive efficiency: empirical validation with the face matching task
.
Entropy
27
(
4
),
pp. 353
.
External Links:
Document
Cited by:
§2.4
,
§5.4
,
footnote 1
.
Fleming and Dolan (2012)
S. M. Fleming and R. J. Dolan
The neural basis of metacognitive ability
.
Philosophical Transactions of the Royal Society B
367
,
pp. 1338–1349
.
Cited by:
§5.3
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
§2.3
.
Fleming
et al.
(2010)
S. M. Fleming, R. S. Weil, Z. Nagy, R. J. Dolan, and G. Rees
Relating introspective accuracy to individual differences in brain structure
.
Science
329
(
5998
),
pp. 1541–1543
.
Cited by:
§5.3
.
Galvin
et al.
(2003)
S. J. Galvin, J. V. Podd, V. Drga, and J. Whitmore
Type 2 tasks in the theory of signal detectability: discrimination between correct and incorrect decisions
.
Psychonomic Bulletin & Review
10
(
4
),
pp. 843–876
.
Cited by:
§2.1
.
Gemma Team (2024)
Gemma Team
Gemma 2: improving open language models at a practical size
.
arXiv preprint arXiv:2408.00118
.
Cited by:
§3.1
.
Green and Swets (1966)
D. M. Green and J. A. Swets
Signal detection theory and psychophysics
.
Wiley
.
Cited by:
§1
,
§2.2
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
ICML
,
pp. 1321–1330
.
Cited by:
§1
.
Jiang
et al.
(2023)
A. Q. Jiang
et al.
Mistral 7B
.
arXiv preprint arXiv:2310.06825
.
Cited by:
§3.1
.
Joshi
et al.
(2017)
M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer
TriviaQA: a large scale distantly supervised challenge dataset for reading comprehension
.
In
ACL
,
Cited by:
§3.1
.
Kwiatkowski
et al.
(2019)
T. Kwiatkowski
et al.
Natural questions: a benchmark for question answering research
.
TACL
7
,
pp. 453–466
.
Cited by:
§3.1
.
Macmillan and Creelman (2005)
N. A. Macmillan and C. D. Creelman
Detection theory: a user’s guide
.
2nd edition
,
Lawrence Erlbaum
.
Cited by:
§1
,
§2.2
.
Maniscalco and Lau (2012)
B. Maniscalco and H. Lau
A signal detection theoretic approach for estimating metacognitive sensitivity from confidence ratings
.
Consciousness and Cognition
21
(
1
),
pp. 422–430
.
Cited by:
§2.3
.
Maniscalco and Lau (2014)
B. Maniscalco and H. Lau
Signal detection theory analysis of type 1 and type 2 data: meta-d’, response-specific meta-d’, and the unequal variance sdt model
.
In
The Cognitive Neuroscience of Metacognition
,
pp. 25–66
.
Cited by:
§2.3
.
Meta AI (2024)
Meta AI
Llama 3 model card
.
Note:
https://github.com/meta-llama/llama3
Cited by:
§3.1
.
Rahnev (2025)
D. Rahnev
A comprehensive assessment of current methods for measuring metacognition
.
Nature Communications
16
(
1
),
pp. 701
.
External Links:
Document
Cited by:
§2.3
.
Rouault
et al.
(2018)
M. Rouault, A. McWilliams, M. G. Allen, and S. M. Fleming
Human metacognition across domains: insights from individual differences and neuroimaging
.
Personality Neuroscience
1
,
pp. e17
.
Cited by:
§5.3
.
Smith
et al.
(2014)
J. D. Smith, J. J. Couchman, and M. J. Beran
Animal metacognition: a tale of two comparative psychologies
.
Journal of Comparative Psychology
128
(
2
),
pp. 115–131
.
Cited by:
§2.5
.
Steyvers and Peters (2025)
M. Steyvers and M. A. K. Peters
Metacognition and uncertainty communication in humans and large language models
.
Current Directions in Psychological Science
.
Cited by:
§1
.
Swets (1996)
J. A. Swets
Signal detection theory and roc analysis in psychology and diagnostics
.
Lawrence Erlbaum
.
Cited by:
§5.3
.
Xiong
et al.
(2024)
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi
Can LLMs express their uncertainty? an empirical evaluation of confidence elicitation in LLMs
.
arXiv preprint arXiv:2306.13063
.
Cited by:
§2.5
.
Appendix A
NLP Monotonicity Check
Accuracy increases strictly across NLP quartiles in all eight model
×
\times
dataset conditions at
T
=
1.0
T{=}1.0
(e.g., Gemma-2 on TriviaQA:
Q
1
=
0.314
Q_{1}{=}0.314
,
Q
2
=
0.539
Q_{2}{=}0.539
,
Q
3
=
0.690
Q_{3}{=}0.690
,
Q
4
=
0.859
Q_{4}{=}0.859
), validating NLP as a graded evidence variable.
Appendix B
Selective Prediction: Accuracy–Coverage
Accuracy as a function of coverage (fraction of queries answered), abstaining on lowest-confidence responses. Models with higher meta-
I
2
​
r
I_{2r}
obtain a larger accuracy
gain
from confidence-based abstention (Spearman
ρ
=
+
0.80
\rho={+}0.80
between meta-
I
2
​
r
I_{2r}
and the accuracy gain at 50% coverage), while the absolute accuracy level under selection is governed by base accuracy. This confirms that metacognitive information predicts the value extracted from a model’s own confidence signal, not the accuracy ceiling.