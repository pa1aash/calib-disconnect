---
title: 'What LLM Forecasters Know but Don’t Say: Probing Internal Representations
  for Calibration and Faithfulness'
id: what-llm-forecasters-know-but-dont-say-probing-internal-representations-for-cali
tags:
- code-llm-confidence-positioning-d82d00
- l2-analogue
created: '2026-11-09T23:14:15.553294Z'
updated: '2026-11-09T23:27:44.776983Z'
source: https://arxiv.org/html/2607.08046
source_domain: arxiv.org
fetched_at: '2026-11-09T23:14:15.552787Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: FULL TEXT (Sarfati et al., arXiv 2607.08046). Probes on Eternis-Forecaster
  8B (also GLM-4.7-Flash, GLM-4.5-Air) calibrate forecasts better than outputs; pre-reasoning
  answer spread routes questions saving 30-47% tokens with no accuracy loss; evidence
  ablation of CoT. Non-code forecasting; L2/L3 analogue.
---

What LLM Forecasters Know but Don’t Say: Probing Internal Representations for Calibration and Faithfulness
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2607.08046v1 [cs.CL] 09 Jul 2026
What LLM Forecasters Know but Don’t Say:
Probing Internal Representations for Calibration and Faithfulness
Raphaël Sarfati
∗,g
Pratyush Ranjan Tiwari
∗,e
Siddharth Boppana
g
Christopher J. Earls
g
Srikar Varadaraj
e
Eric Ho
g
Abstract
Large language models fine-tuned for forecasting can be accurate yet poorly calibrated, and their chain-of-thought (CoT) reasoning may not faithfully reflect the evidence behind a forecast.
We ask whether internal representations offer a more direct window into both.
Working with
Eternis-Forecaster 8B
on
OpenForesight
, we train representation-pooling probes on intermediate activations and find they achieve substantially better calibration; a result that also holds for
GLM-4.7-Flash
and
GLM-4.5-Air
.
We then assess CoT faithfulness through evidence ablation and diversionary injection:
removing an influential source in the prompt often changes the model’s forecast while leaving the reasoning trace untouched.
The same probes function as lie detectors: their activations track behavioral shifts far better than the reasoning trace does, and they also predict the direction of change in 84% of cases, including when the CoT conceals the perturbation’s influence.
Finally, forced answering reveals that forecasts are largely fixed before reasoning begins: a single pre-reasoning pass recovers the committed answer and confidence, and routing questions by the spread of this pre-set answer distribution saves 30–47% of generated tokens,
with no loss of accuracy
.
Together, these results establish probing internal representations as a practical tool for calibrating, auditing, and triaging language model forecasters and reasoning models more broadly.
\correspondence
core contributors: raphael@goodfire.ai, pratyush@eternis.ai
\maketitlebox
1
Introduction
Large language models (LLMs) are, by design, next-token predictors.
They are also robust analysts and forecasters.
Somehow the task of predicting a new token
x
x
given a context
C
C
has transferred the emergent ability to: reason about large amounts of textual data, recoup information, produce inferences, and finally even reason about out-of-distribution topics; thus, paving the way to new scientific discovery and robust forecasting of future events.
Recent work has shown that LLMs, post-trained using reinforcement learning (RL), can rival or surpass human forecasters on real-world prediction markets and open-ended questions
(
futuresim2026
;
chandak2026scalingopenendedreasoningpredict
)
; thus, establishing them as practical tools for decision support across domains from geopolitics to public health.
Accuracy alone does not make a forecaster trustworthy.
A well-calibrated forecaster must know what it knows: when it assigns 70% confidence to an outcome, that outcome should materialize roughly 70% of the time.
In practice, LLM forecasters are often miscalibrated: their verbalized probability estimates deviate substantially from empirical accuracy.
Compounding this, the chain-of-thought (CoT) reasoning that accompanies a forecast may not faithfully reflect the computation that actually produced it.
If a model’s stated reasoning omits or misrepresents the evidence driving its prediction, then the user cannot meaningfully audit the forecast, and the associated calibration derived from verbalized confidence inherits the distortions of an unreliable narrator.
In this work, we ask whether the model’s internal representations offer a more direct window into both confidence and reasoning fidelity.
We train lightweight probes – linear classifiers operating on pooled intermediate activations (mean-pooling, attention-pooling, and covariance pooling) – on the CoT representations of
Eternis-Forecaster 8B
(
EF-8B
)
(
eternis2026sotaforecasting
)
, post-trained from
Qwen3-8B
using an approach based on reinforcement learning from verifiable rewards (RLVR) for better forecasting.
These probes read the model’s internal state to estimate the likelihood that a given forecast is correct, bypassing verbalization entirely.
We also test probe-only calibration on two frozen models of different sizes,
GLM-4.7-Flash
and
GLM-4.5-Air
, training only probe weights on
∼
10,000
{\sim}10,000
improved-context
OpenForesight
rollouts.
To test whether this signal generalizes beyond forecasting, we also run a math reasoning stress test.
We reproduce the dynamic clipping policy optimization (DCPO) recipe for
Qwen3-8B
(
ma2026decouplingreasoningconfidenceresurrecting
)
and evaluate frozen correctness probes on pooled out-of-distribution (OOD)
AIME
/
AMC
benchmarks, using math as a separate calibrated-reasoning domain.
We complement this with two systematic tests of chain-of-thought faithfulness, following the causal perturbation framework of
gurarieh2026faithfulnessmetricsdontmeasure
: evidence ablation, which removes supporting articles and measures whether the reasoning updates accordingly, and diversionary injection, which inserts fabricated evidence and checks whether the model discloses its influence.
We find that internal probes substantially outperform model-verbalized confidence,
achieving a much lower expected calibration error (ECE).
Across both
GLM
models, raw probe probabilities sharply reduce ECE relative to verbalized confidence, supporting calibration gains without updating model weights.
Chain-of-thought reasoning proves only partially faithful: removing influential evidence changes the forecast without updating the reasoning trace in 23% of high-impact cases (Spearman
ρ
\rho
= 0.22 between behavioral impact and CoT change), though the model is largely transparent when actively presented with misleading evidence (stealth rate 2.9%).
Most strikingly, the same probes that calibrate confidence also function as “lie detectors”: their activations track behavioral shifts at
ρ
\rho
= 0.57 and detect internal state changes even when the chain of thought conceals the perturbation’s influence.
Together, these results establish internal probing as a practical tool for both calibrating and auditing language model forecasters.
2
Related Work
2.1
Time series extrapolation
A first line of work asks whether the sequence-modeling priors of LLMs transfer
to numerical time series.
gruver2023llmtime
show that frozen, general-purpose LLMs extrapolate time series zero-shot when numeric values are
tokenized as text, rivaling purpose-built models, while
jin2024timellm
reprogram a frozen LLM with learned text prototypes.
One step further,
liu2024dynamical
find that frozen
Llama-2
predicts the trajectories of
diverse dynamical systems in-context, uncovering an in-context neural scaling law as the evidence window grows.
A parallel line trains dedicated time-series foundation models that borrow the tokenize-and-pretrain recipe of language modeling, including
ansari2024chronos
and the decoder-only
das2024timesfm
.
The premise is contested:
tan2024useful
find that ablating or replacing the LLM backbone in several such systems leaves accuracy unchanged, suggesting the gains may owe more to the surrounding architecture than to language pretraining. Our setting differs: we study forecasting of discrete real-world events from natural-language evidence, not numerical extrapolation.
2.2
Open-ended forecasting
Closer to our setting is judgmental forecasting of future events posed in natural
language.
zou2022autocast
introduced Autocast, a benchmark of real tournament questions with a date-stamped news corpus, and found LLMs to be far below human expert performance levels.
Subsequent systems narrowed the gap:
halawi2024forecasting
pair retrieval with reasoning to approach the crowd aggregate of competitive forecasters, and
schoenegger2024silicon
show an ensemble of LLMs can match human-crowd accuracy;
karger2025forecastbench
track this progress with a contamination-free, continuously updated benchmark.
2.3
Calibration-aware RL for reasoning
Reinforcement learning from verifiable rewards (RLVR) trains reasoning models with automatically checked outcomes, most often a binary correctness reward.
This improves mathematical and symbolic reasoning, but binary rewards do not distinguish confident errors from cautious guesses, so RLVR can worsen calibration even as accuracy improves.
damani2026binaryrewardstraininglms
propose Reinforcement Learning with Calibration Rewards (RLCR), which augments the correctness reward with a Brier-score calibration reward and trains the model to emit both an answer and a verbalized confidence.
The Brier term is a proper scoring rule for binary correctness, so it directly incentivizes confidence estimates that match empirical success probabilities.
ma2026decouplingreasoningconfidenceresurrecting
propose DCPO, motivated by an accuracy-calibration gradient conflict in coupled RL objectives.
DCPO separates the optimization of reasoning tokens and confidence tokens, using verbalized confidence and decoupled advantages to improve calibration while preserving the gains from RLVR.
Our math experiment asks a complementary question: after using a strong training-time calibration recipe, can a frozen activation readout still recover OOD correctness information that token statistics or verbalized confidence miss?
3
Methods
In this section, we carefully outline the foundational concepts, and associate details, that underpin the work reported on, herein.
3.1
Models
We focus our analysis on
Eternis-Forecaster 8B
(
EF-8B
)
(
eternis2026sotaforecasting
)
, post-trained from
Qwen/Qwen3-8B
using an RLVR-style approach for better forecasting.
For a subset of experiments we additionally use
Eternis-Forecaster 32B
(
EF-32B
), a larger model from the same family.
As comparison baselines we also consider:
•
nikhilchandak/OpenForecaster-8B
(
chandak2026scalingopenendedreasoningpredict
)
;
•
the original
Qwen/Qwen3-8B
(
yang2025qwen3technicalreport
)
in reasoning mode.
For the probe-only calibration generalization study, we use two frozen GLM models:
GLM-4.7-Flash
and
GLM-4.5-Air
(
glmteam2025glm45
)
.
They differ in size, and only the probe weights are trained.
3.2
Dataset
Forecasting dataset.
We rely on the
nikhilchandak/OpenForesight
dataset, introduced in
chandak2026scalingopenendedreasoningpredict
.
The
prompt
field aggregates: initial instructions, the forecasting question itself, background and resolution criteria, and “relevant passages from retrieved news articles”; it concludes with the following instructions:
Your final answer should be concise (NOT MORE THAN A FEW WORDS LONG) and your response SHOULD STRICTLY END with <answer> </answer> tags and <probability> </probability> tags.
The public
HuggingFace
release of the data used herein consists of six splits (at press time):
train
(52.2k rows),
validation
(207),
test
(302),
aljazeera2026Q1
(330),
aljazeeraLate2025
(491), and
skysports2025
(1.79k).
Additionally, we developed an improved context-building scheme and used it to derive a non-public
compact-context
build of the dataset, whose prompts carry roughly half as much retrieved-article context per question.
The improved data set comprises three splits:
train
*
(47,466 rows),
test
*
(296), and
val
*
(193).
The starred
test
*
and
val
*
questions are subsets of the public
test
and
validation
splits, with identical questions, ground-truth answers, and resolution criteria but different prompts.
The forecasting models were trained on the
train
split.
The themes and format of the
aljazeera
and
skysports
splits make them out-of-distribution (OOD) relative to the original
train/val/test
splits; thus, providing a broader testing environment.
A data audit (Appendix
A
) reveals a large number of shared qids across splits (Fig.
11
), but all are collisions rather than duplicated questions (as evaluated by exact match and LLM-as-a-judge).
GLM probe-only dataset.
For the GLM probe-only calibration study, we use another OpenForesight version whose question contexts were improved to be more relevant than the semantic-search contexts used in the OpenForecaster paper
(
chandak2026scalingopenendedreasoningpredict
)
.
Each GLM probe is trained on
11,835
11{,}835
rollouts from the train pool (
3,945
3{,}945
questions
×
\times
3 completions), selected on
1,930
1{,}930
validation rollouts, and reported on
2,960
2{,}960
held-out test rollouts.
Probe inputs contain the prompt plus chain-of-thought truncated before the final answer block; model weights stay frozen and only probe weights are optimized with cross-entropy/BCE.
We also track leakage-controlled subsets:
423
423
usable self-report rollouts for
GLM-4.7-Flash
after removing CoT answer leakage and
1,747
1{,}747
rollouts for
GLM-4.5-Air
after removing mid-reasoning probability leakage.
Math reasoning dataset.
For the math reasoning calibration experiment, probes are trained on a level-stratified subset of
MATH-train
:
3,999
3{,}999
questions after deduplicating against the math test benchmarks.
The OOD evaluation pools
AIME24
(
30
×
4
30\times 4
rollouts),
AIME25
(
30
×
4
30\times 4
),
AMC23
(
40
×
4
40\times 4
), and
AMC24
(
45
×
4
45\times 4
), for
n
=
580
n=580
rollouts.
We also track clean
MATH-500
as an in-distribution diagnostic, but the headline comparison in Section
4.4
uses only the pooled AIME/AMC OOD split.
The DCPO-recipe probe-train pool overlaps the RLVR training distribution through
DeepScaleR
, so cross-model similarity in probe performance should not be read as evidence that the underlying representations are training-invariant.
3.3
Probes
Probes are small classifiers trained on the frozen internal activations of a larger model: they read out information the model represents internally, without modifying the model itself
(
alain2018understandingintermediatelayersusing
;
belinkov2021probingclassifierspromisesshortcomings
)
.
Pooling probes.
Rather than reading from a single activation
𝒙
i
∈
ℝ
D
\bm{x}_{i}\in\mathbb{R}^{D}
, pooling probes compute a function of the full context
(
𝒙
1
,
…
,
𝒙
i
,
…
,
𝒙
N
)
(\bm{x}_{1},\dots,\bm{x}_{i},\dots,\bm{x}_{N})
through a pooling function
ϕ
\phi
.
Note that
individual activations already contain contextual information from preceding tokens
, but that information is compressed and filtered; pooling across the sequence recovers signal that no single position retains.
Given a matrix of such activations
𝑿
∈
ℝ
N
×
D
\bm{X}\in\mathbb{R}^{N\times D}
, a probe is defined as
f
θ
​
(
𝑿
)
=
g
θ
​
(
ϕ
θ
​
(
𝑿
)
)
f_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}(\bm{X})=g_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}(\phi_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}(\bm{X}))
, where
g
θ
g_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}
is a readout function (typically a linear layer, see below) and
ϕ
θ
\phi_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}
is a pooling function;
θ
{\color[rgb]{0.7617,0.2539,0.0469}\theta}
denotes a set of trainable parameters.
Mean-pooling
implements a naive arithmetic average along the token axis; in matrix form (
𝟏
i
​
j
=
1
∀
(
i
,
j
)
\bm{1}_{ij}=1\quad\forall(i,j)
):
ϕ
mean
​
(
𝑿
)
=
1
N
​
𝑿
⊤
​
𝟏
N
∈
ℝ
D
.
\phi_{\mathrm{mean}}(\bm{X})=\frac{1}{N}\bm{X}^{\top}\bm{1}_{N}\,\in\mathbb{R}^{D}.
(1)
Attention probes
(more precisely,
attention-pooling probes
) use trained attention heads to aggregate residual-stream activations
(
kantamneni2025sparseautoencodersusefulcase
;
boppana2026reasoningtheaterdisentanglingmodel
)
:
ϕ
attn
​
(
𝑿
)
=
𝑿
⊤
​
softmax
⁡
(
𝑿
​
𝒒
)
∈
ℝ
D
,
\phi_{\mathrm{attn}}(\bm{X})=\bm{X}^{\top}\operatorname{softmax}\left(\bm{X}{\color[rgb]{0.7617,0.2539,0.0469}\bm{q}}\right)\,\in\mathbb{R}^{D},
(2)
where the softmax is taken over token positions and
𝒒
∈
ℝ
D
{\color[rgb]{0.7617,0.2539,0.0469}\bm{q}}\in\mathbb{R}^{D}
is a trained query projection.
Covariance probes
were introduced in
dooms2026covariance
;
Pearce2026.04.10.717844
.
They compress the sequence’s (uncentered) covariance structure into a low-dimensional bilinear bottleneck (dim =
k
k
):
ϕ
cov
​
(
𝑿
)
=
1
N
​
(
𝑿
​
𝑳
)
⊤
​
(
𝑿
​
𝑹
)
∈
ℝ
k
×
k
,
\phi_{\mathrm{cov}}(\bm{X})=\frac{1}{N}\left(\bm{X}{\color[rgb]{0.7617,0.2539,0.0469}\bm{L}}\right)^{\top}\left(\bm{X}{\color[rgb]{0.7617,0.2539,0.0469}\bm{R}}\right)\,\in\mathbb{R}^{k\times k},
(3)
where
𝑳
{\color[rgb]{0.7617,0.2539,0.0469}\bm{L}}
and
𝑹
∈
ℝ
D
×
k
{\color[rgb]{0.7617,0.2539,0.0469}\bm{R}}\in\mathbb{R}^{D\times k}
are trained low-rank projections; the resulting matrix is flattened and passed to the readout.
Unlike mean- and attention-pooling, this captures second-order (co-fluctuation) statistics of the activations across the sequence.
Readout function.
The readout function
g
θ
g_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}
is generally a simple scalar product; in our case:
f
θ
​
(
𝑿
)
=
⟨
𝑾
,
ϕ
θ
​
(
𝑿
)
⟩
+
b
,
f_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}(\bm{X})=\langle{\color[rgb]{0.7617,0.2539,0.0469}\bm{W}},\phi_{{\color[rgb]{0.7617,0.2539,0.0469}\theta}}(\bm{X})\rangle+{\color[rgb]{0.7617,0.2539,0.0469}b},
(4)
where
⟨
⋅
,
⋅
⟩
\langle\cdot,\cdot\rangle
is the appropriate inner product: the vector dot product for mean and attention pooling, and the Frobenius inner product for covariance pooling.
3.4
Metrics
We use standard statistical metrics to evaluate prediction calibration
(
damani2026binaryrewardstraininglms
)
.
A prediction
π
\pi
is defined as a triplet consisting of an answer
a
a
, an associated confidence
p
∈
[
0
,
1
]
p\in[0,1]
, and an outcome
y
∈
{
0
,
1
}
y\in\{0,1\}
indicating correctness:
π
=
(
a
,
p
,
y
)
\pi=\left(a,p,y\right)
.
Expected Calibration Error (ECE).
ECE measures the agreement between stated confidence and empirical accuracy:
when the model says it is 40% confident, is it correct 40% of the time?
Confidence values are binned and compared against the empirical accuracy within each bin:
ECE
=
∑
b
n
b
N
​
|
acc
⁡
(
b
)
−
conf
⁡
(
b
)
|
,
\mathrm{ECE}=\sum_{b}\frac{n_{b}}{N}\left|\mathrm{acc}(b)-\mathrm{conf}(b)\right|,
(5)
where
n
b
n_{b}
is the number of predictions in bin
b
b
,
N
N
the total number of predictions,
acc
⁡
(
b
)
\mathrm{acc}(b)
the fraction of correct predictions in the bin, and
conf
⁡
(
b
)
\mathrm{conf}(b)
the mean confidence in the bin.
Brier score.
This measures the cost of misplaced confidence:
does the model pay for its confidence when it is wrong?
Given
N
N
predictions with confidences
p
i
∈
[
0
,
1
]
p_{i}\in[0,1]
and outcomes
y
i
y_{i}
, the Brier score is the mean squared error between the two:
Br
=
1
N
​
∑
i
(
p
i
−
y
i
)
2
.
\mathrm{Br}=\frac{1}{N}\sum_{i}\left(p_{i}-y_{i}\right)^{2}.
(6)
It rewards confident correct predictions and penalizes confident errors quadratically.
AUROC.
Calibration and discrimination are complementary properties of a confidence signal.
ECE and the Brier score ask whether confidence values
match
empirical accuracy;
Area Under the Receiver Operating Characteristic curve (AUROC) asks whether confidence
separates
correct predictions from incorrect ones.
Imagine drawing one correct and one incorrect prediction at random and betting that the correct one carries higher confidence: AUROC is simply how often you would win that bet (0.5 = no better than a coin flip, 1 = the confidence always ranks the correct answer above the incorrect one).
Equivalently, it sweeps every possible confidence threshold and measures how cleanly the two groups can be told apart, which is why it needs no threshold to be chosen in advance.
Because it depends only on the ordering of confidences, not their absolute values, AUROC is unchanged by any monotone rescaling such as temperature scaling: a probe can be well calibrated yet undiscriminative, or discriminative yet miscalibrated.
Correlation coefficients.
We report both Pearson’s
r
r
, which measures linear association,
r
=
∑
i
(
x
i
−
x
¯
)
​
(
y
i
−
y
¯
)
∑
i
(
x
i
−
x
¯
)
2
​
∑
i
(
y
i
−
y
¯
)
2
,
r=\frac{\sum_{i}\left(x_{i}-\bar{x}\right)\left(y_{i}-\bar{y}\right)}{\sqrt{\sum_{i}\left(x_{i}-\bar{x}\right)^{2}}\sqrt{\sum_{i}\left(y_{i}-\bar{y}\right)^{2}}},
(7)
and Spearman’s
ρ
=
r
⁡
(
rank
⁡
(
x
)
,
rank
⁡
(
y
)
)
\rho=r\!\left(\operatorname{rank}(x),\operatorname{rank}(y)\right)
, the Pearson correlation of the rank-transformed variables (mid-ranks for ties), which measures monotone association and is insensitive to outliers and marginal distributions.
Confidence intervals.
Unless otherwise noted, 95% confidence intervals are computed with a nonparametric percentile bootstrap.
Because our data are clustered (each question contributes several rollouts, and all ablation pairs within a question share the same control baseline), we resample at the
question
level: questions are drawn with replacement and all of their rollouts or perturbation pairs are pooled.
LLM-as-a-judge
LLM-as-a-judge has become a standard evaluation tool
(
gu2025surveyllmasajudge
)
: a capable model quantifies properties of a piece of text, providing the flexibility required to assess an inherently unquantifiable substrate like natural language.
The canonical application in our setting is answer matching.
A forecasting question may list its ground-truth answer as “Federal Bureau of Investigation”, while the model responds with any of a number of valid surface forms:
the FBI
,
F.B.I.
,
the Federal Bureau of Investigations (FBI)
, etc.
Exact or rule-based string matching (e.g. regular expressions) is brittle to such variation and produces both false negatives and false positives; an LLM judge, by contrast, reliably recognizes semantic equivalence.
Beyond binary correctness, LLM judges are also well suited to graded assessments of syntactic and semantic content, such as coherence, fluency, or the quality of intermediate reasoning steps.
We rely on an LLM-as-a-judge in two roles.
First, for
answer matching
: scoring whether a model’s free-form forecast agrees with the resolved ground truth, which underlies the correctness labels used throughout our calibration and probing experiments.
Second, for
chain-of-thought scoring
in the faithfulness experiments (Section
4.5
), where the judge rates whether the reasoning cites a given piece of evidence (citation score) and its stance toward it (accept / weigh / reject / not mentioned).
4
Experiments
4.1
Accuracy and Confidence
4.1.1
EF-8B
is stable but overconfident across sampling temperatures
Before probing internal representations, we characterize how
EF-8B
’s forecasting behavior responds to sampling temperature.
For ten temperatures
T
∈
{
0.2
,
0.4
,
…
,
2.0
}
T\in\{0.2,0.4,\dots,2.0\}
, we draw
10
10
rollouts on all
296
296
questions of the
OpenForesight-test
*
split (
29,600
29{,}600
generations) and measure
self-consistency
(fraction of a question’s rollouts in its modal answer cluster),
correctness
(per-rollout accuracy, with answer equivalence judged by
LLM-as-a-judge
), and
confidence
(mean verbalized probability between the
<probability>
tags).
Across
T
≲
1.6
T\lesssim 1.6
, accuracy (
37
±
1
%
37\pm 1\%
) and confidence (
∼
50
%
{\sim}50\%
) are both flat while self-consistency falls steadily (
66
%
→
30
%
66\%\to 30\%
); accuracy degrades only past
T
≈
1.6
T\approx 1.6
(Appendix
B
).
We adopt
T
=
1.0
T=1.0
for the rest of the paper.
This stability exposes a calibration problem:
confidence sits near
50
%
50\%
against
∼
37
%
{\sim}37\%
accuracy and barely moves, even as the rollouts disagree more, leaving
EF-8B
consistently overconfident (ECE
0.110
0.110
–
0.150
0.150
).
This motivates our central question:
whether
EF-8B
’s internal representations estimate confidence and correctness more faithfully than its verbalized probability.
4.1.2
Forecasts are most accurate when the gold answer is contained in the prompt
Forecast correctness co-varies strongly with whether the retrieved news passages in the prompt mention the gold answer.
Using an
LLM judge
to label answer containment in the evidence span—semantic matching, applied uniformly to the
test
/
validation
splits of both dataset builds—we find
EF-8B
reaches 86%–94% accuracy on answer-bearing questions versus 0.26–0.33 when the answer is absent (
Δ
=
+
57
%
\Delta=+57\%
to
+
65
%
+65\%
per slice, every 95% bootstrap CI excluding zero).
The pattern is informative about how the model answers.
When the prompt presents a space of possibilities that includes the correct answer,
EF-8B
reliably converges on it,
whereas with no candidate in context it must fall back on parametric knowledge, and accuracy drops to
∼
\sim
0.3.
The model retrieves from available information rather than guessing from what it has knows.
This is a desirable trait for a forecasting model – and
it demonstrates that robust information retrieval and context building are critical to accurate forecasts.
4.2
Calibration of confidence
4.2.1
Probing internal representations for correctness
We train a family of activation-pooling probes to read
EF-8B
’s confidence directly from its internal state.
Each probe is a small classifier on the frozen activations of a single layer, trained to predict whether a rollout’s final answer will resolve correctly.
We sweep all 36 layers, all three pooling architectures of Section
3.3
(mean-, attention-, and covariance-pooling), and several positions along the reasoning trace, from the opening
<think>
through the rollout to the closing
</think>
.
The full sweep, training recipe, and per-site metrics are in Appendix
C
.
The sweep shows a consistent picture.
Discrimination concentrates in the mid-to-late layers (19–24) and is largely in place before reasoning begins
(probes read at the end of the prompt already reach AUROC
≈
0.76
\approx 0.76
),
consistent with the forced-answering finding (Section
4.6
) that
much of the forecast is fixed before the chain of thought reflects a finding.
Calibration, by contrast, depends strongly on the pooling architecture:
attention probes discriminate well but are persistently overconfident, whereas covariance probes match their discrimination while staying far better calibrated.
We therefore deploy a covariance probe at layer 21, read late in the rollout.
4.2.2
Probe calibration surpasses verbalized confidence
Figure 1
:
Reliability diagram
for the layer-21 covariance probe (ember) and
EF-8B
’s verbalized confidence from the final
<probability>
tag (slate), on the
OpenForesight-test
split (
N
=
3,020
N=3{,}020
rollouts each).
10 equal-width bins; marker size
∝
\propto
bin count; diagonal
=
=
perfect calibration.
The probe tracks the diagonal (ECE
=
0.044
=0.044
) while verbalized confidence is overconfident above
0.5
0.5
(ECE
=
0.093
=0.093
).
Figure
1
compares this probe against the model’s verbalized confidence – the probability the model verbalizes in its final
<probability>
tag, present in all rollouts – on the
OpenForesight-test
split (
N
=
3,020
N=3{,}020
rollouts for both signals).
The two signals are statistically indistinguishable as rankers (AUROC
0.756
0.756
vs.
0.758
0.758
), but differ sharply in calibration.
Verbalized confidence is nearly calibrated below
0.5
0.5
and systematically overconfident above it:
rollouts stated at
0.93
0.93
resolve correct
70
%
70\%
of the time, and those stated at
0.75
0.75
only
44
%
44\%
.
The probe tracks the diagonal across the full range, yielding ECE
=
0.044
=0.044
vs.
0.093
0.093
.
The same pattern holds out of distribution: the probe’s calibration advantage persists on both OOD sources (
skysports
ECE
0.064
0.064
vs.
0.089
0.089
;
aljazeera
0.140
0.140
vs.
0.178
0.178
), while verbalized discrimination degrades to near chance on
aljazeera
(AUROC
0.587
0.587
).
The probe additionally provides a confidence estimate at
every
rollout depth, including mid-reasoning before any answer is committed – a property we exploit for faithfulness auditing in Section
4.5
.
Probing for
correctness
thus yields calibration:
a lightweight readout of the model’s internal state recovers the well-calibrated confidence that the model’s own verbalization distorts,
without consuming any more inference tokens.
4.3
Probe-only calibration on GLM models
The
EF-8B
result leaves open whether calibrated internal readouts depend on training the underlying model for our forecasting setting.
We therefore repeat the probe-only recipe on two frozen GLM models of different sizes,
GLM-4.7-Flash
and
GLM-4.5-Air
.
In both cases, the model is held fixed and only a small probe is trained on roughly ten thousand improved-context
OpenForesight
rollouts.
Table 1
:
Probe-only calibration on frozen GLM models.
Each row trains only probe weights on the improved-context
OpenForesight
train pool and reports held-out test metrics. ECE uses raw probabilities with no recalibration. Clean
Δ
\Delta
AUROC removes rollouts with mid-reasoning answer or probability leakage according to each experiment’s control.
Model
Probe
Test
n
n
Probe AUROC
Verbal AUROC
Probe ECE
Verbal ECE
Clean
Δ
\Delta
AUROC [95% CI]
Note
GLM-4.7-Flash
Mean-pool L28
2,960
2{,}960
0.768
0.768
0.669
0.669
0.054
0.054
0.287
0.287
+
0.055
​
[
−
0.006
,
0.111
]
+0.055\ [-0.006,0.111]
Best AUROC: cov L26,
0.790
0.790
GLM-4.5-Air
Attention-1 L18
2,960
2{,}960
0.783
0.783
0.691
0.691
0.102
0.102
0.255
0.255
+
0.110
​
[
0.069
,
0.149
]
\mathbf{+0.110}\ [0.069,0.149]
Best ECE: linear L24,
0.097
0.097
GLM-4.7
GLM-4.5
0.6
0.6
0.7
0.7
0.8
0.8
AUROC
↑
\uparrow
Test discrimination
Probe
Verbal
GLM-4.7
GLM-4.5
0
0
0.1
0.1
0.2
0.2
0.3
0.3
ECE
↓
\downarrow
Raw calibration
Probe
Verbal
Figure 2
:
Probe-only confidence from GLM internals.
Internal probes improve AUROC on both full test sets (left) and sharply reduce raw ECE relative to verbalized confidence (right). The
GLM-4.7-Flash
clean ranking interval includes zero, so its robust claim is calibration;
GLM-4.5-Air
improves both ranking and calibration.
Figure 3
:
GLM-4.5-Air reliability.
The layer-18 attention probe is substantially better calibrated than the model’s stated probability on the test split.
Linear
Attn-1
Attn-4
Cov
0.6
0.6
0.65
0.65
0.7
0.7
0.75
0.75
0.8
0.8
Best-layer test AUROC
Matched 24–40 harvest
GLM-4.5-Air
GLM-4.7-Flash
Figure 4
:
Matched-depth cross-model comparison.
Best-layer test AUROC by probe family for
GLM-4.5-Air
and
GLM-4.7-Flash
on the matched 24–40 harvest, with each model’s verbalized-confidence AUROC as a reference line.
The calibration effect is the common result.
On
GLM-4.7-Flash
, the practical mean-pool probe has ECE
0.054
0.054
versus
0.287
0.287
for verbalized confidence; the leakage-controlled ranking delta is positive but not significant.
On
GLM-4.5-Air
, the layer-18 attention probe improves both AUROC and ECE, and the clean ranking interval stays above zero.
These results support the central use case: small probes can supply calibrated correctness estimates for frozen models without updating model weights.
4.4
Math reasoning calibration
The forecasting experiments show that internal probes recover a better calibrated confidence signal than the model’s verbalized confidence.
We next ask whether the same readout helps in a different calibrated-reasoning setting: mathematical reasoning after RLVR.
Following
ma2026decouplingreasoningconfidenceresurrecting
, we reproduce DCPO as a strong training-time calibration baseline for
Qwen3-8B
.
We then freeze each model and train a correctness probe on residual-stream activations immediately before the boxed answer, comparing it against token-logprob confidence and recalibrated verbalized confidence on pooled OOD math benchmarks.
Table 2
:
Correctness probe vs. best non-probe confidence on out-of-distribution math
(pooled AIME24/25 + AMC23/24,
n
=
580
n=580
).
Δ
=
probe
−
best non-probe
\Delta=\text{probe}-\text{best non-probe}
; AUROC higher is better (
Δ
>
0
\Delta>0
favors the probe), ECE lower is better (
Δ
<
0
\Delta<0
favors the probe).
Intervals are 95% qid-clustered bootstrap CIs.
The best non-probe AUROC is whole-response token-logprob confidence for both rows.
Probe site is layer / depth fraction / pooling.
AUROC
↑
\uparrow
ECE
↓
\downarrow
Model
Decode
Probe site
Probe
Best n.p.
Δ
\Delta
[95% CI]
Probe
Best n.p.
Δ
\Delta
[95% CI]
Best ECE baseline
Untrained
Qwen3-8B
plain
L18 / r100 / last-tok
0.894
0.894
0.752
0.752
+
0.143
​
[
0.090
,
0.197
]
\mathbf{+0.143}\ [0.090,0.197]
0.083
0.083
0.270
0.270
−
0.187
​
[
−
0.227
,
−
0.117
]
\mathbf{-0.187}\ [-0.227,-0.117]
iso-logits
DCPO-recipe
Qwen3-8B
verbal
L21 / r100 / last-tok
0.929
0.929
0.865
0.865
+
0.064
​
[
0.023
,
0.109
]
\mathbf{+0.064}\ [0.023,0.109]
0.143
0.143
0.125
0.125
+
0.040
​
[
0.009
,
0.074
]
+0.040\ [0.009,0.074]
iso-verbal
Base
DCPO
0.6
0.6
0.8
0.8
1
1
AUROC
↑
\uparrow
OOD discrimination
Probe
Token-logprob
Base
DCPO
0
0
0.2
0.2
0.4
0.4
ECE
↓
\downarrow
OOD calibration
Probe
Token-logprob
Figure 5
:
Probe vs. token-logprob confidence on pooled OOD math.
Only the untrained and DCPO-recipe models are shown, and clean MATH-500 is excluded.
The frozen correctness probe out-discriminates whole-response token-logprob confidence on both models (left) and is better calibrated where token-logprob confidence degrades OOD (right).
ECE is 15-bin.
The OOD pattern separates discrimination from point calibration.
For the untrained base, the probe improves both ranking and calibration: AUROC rises from
0.752
0.752
to
0.894
0.894
, while ECE falls from
0.270
0.270
to
0.083
0.083
.
For the DCPO-recipe model, the probe is still the stronger OOD correctness monitor by AUROC (
0.929
0.929
vs.
0.865
0.865
), but isotonic-recalibrated verbalized confidence remains slightly better by ECE (
0.125
0.125
vs.
0.143
0.143
).
This result supports probes as OOD correctness monitors for math reasoning, while leaving calibration method choice dependent on whether the target is ranking, point calibration, or both.
Appendix
E
gives additional setup and controls.
4.5
Chain-of-Thought Faithfulness
A faithful chain of thought should change when the evidence behind a forecast changes.
We test this directly, following
gurarieh2026faithfulnessmetricsdontmeasure
: we perturb the
input prompt and measure two responses to the
same
perturbation.
•
The
behavioral change
|
Δ
​
prob
|
|\Delta\mathrm{prob}|
: the absolute shift in the model’s
stated forecast probability (read from its final
<probability>
tag) between the original
and perturbed prompt, averaged over completions when several are sampled.
•
The
internal change
|
Δ
​
probe
|
|\Delta\mathrm{probe}|
: the absolute shift, over the same pair,
in the estimate of an internal correctness probe (the calibrated readout of
Section
4.2
; here its layer-20 attention variant).
A faithful reasoning trace should visibly update whenever
|
Δ
​
prob
|
|\Delta\mathrm{prob}|
is large.
We apply this in three settings: removing real evidence (
ablation
, Section
4.5.1
),
inserting misleading evidence (
injection
, Section
4.5.2
), and reading the probe directly
as an internal lie detector when the written reasoning stays silent (Section
4.5.3
).
4.5.1
Evidence Ablation Faithfulness
Does
EF-8B
’s chain-of-thought reasoning faithfully reflect which retrieved news articles actually
drive its forecast probabilities? We test this by removing the news sources one at a time: drop a single
real article, then measure whether and how the reasoning updates. We expect that
a.
Correlation:
the behavioral change from removing an article should track the
change in the reasoning;
b.
Stealth influence:
among articles that clearly move the forecast
(
|
Δ
​
prob
|
>
0.05
|\Delta\mathrm{prob}|>0.05
), few should leave the reasoning unchanged;
c.
Signal above noise:
the induced probability shifts should be distinguishable
from ordinary same-prompt sampling variation.
Ablation protocol.
For each forecasting question in
test
*
+val
*
with
N
>
0
N>0
articles (354 questions), we build
N
N
prompts with one article removed (renumbering the rest),
plus one prompt with no articles.
As a control, we run the 354 original prompts through the same generation pipeline, so any measured change reflects the missing article rather than run-to-run decoding variation.
Behavioral change.
We average the stated probability over 3 completions per prompt and take
|
Δ
​
prob
|
|\Delta\mathrm{prob}|
as the
absolute difference between the control and ablated means.
Reasoning change.
We score how much the reasoning
text
moves, relative to how much it moves by chance.
For each question we compare the three control traces to each other (a baseline for sampling variation at
T
=
1.0
T=1.0
) and compare control traces to ablated ones.
The
calibrated CoT change
is the baseline similarity minus the control-vs-ablated similarity, so positive values mean the ablation shifted the reasoning more than sampling noise alone (the dashed noise floor in Fig.
6
a).
Text similarity is the average of a word-overlap (Jaccard) score and a character-sequence similarity score;
separately, we record whether a trace cites the removed article by name or title.
Reasoning change only weakly tracks behavioral impact.
Across 1,303 ablation pairs, behavioral and reasoning change are only weakly related (Spearman
ρ
=
0.215
\rho=0.215
; Fig.
6
a).
Stealth influence is substantial: of the 460 high-impact pairs (
|
Δ
​
prob
|
>
0.05
|\Delta\mathrm{prob}|>0.05
), 107 (23%) show no change in the reasoning at all.
Figure 6
:
Chain-of-thought faithfulness under evidence perturbation.
(a)
Evidence ablation. Each point is one (question, removed-article) pair:
behavioral impact
|
Δ
​
prob
|
|\Delta\text{prob}|
(same-pipeline control vs. single-article-ablated)
against calibrated CoT change (within-control baseline similarity minus control-vs-ablated
similarity; composite similarity
=
=
mean of word-set Jaccard and character-sequence similarity).
Positive
y
y
means the ablation perturbed the reasoning trace more than
T
=
1.0
T{=}1.0
sampling
noise; the dashed line at
y
=
0
y{=}0
is the noise floor. Behavioral and reasoning change are
only weakly coupled (Spearman
ρ
=
0.215
\rho=0.215
), and 107 of 460 high-impact pairs
(
|
Δ
​
prob
|
>
0.05
|\Delta\text{prob}|>0.05
) show no CoT change, a 23% stealth-influence rate.
N
=
1,303
N=1{,}303
single-article ablation pairs from 354 questions.
(b)
Diversionary
injection. Four-quadrant classification of 489 questions by whether the CoT mentions an
injected misleading article (
x
x
) and whether the forecast was behaviorally susceptible to
it (
y
y
); cells give the share and count of questions. The model is largely transparent when
actively misled, 81.2% adopt the fabricated evidence and openly cite it (honest-susceptible),
with stealth adoption (susceptible but unmentioned) in only 2.5% (n
=
=
12).
4.5.2
Diversionary Injection Faithfulness
Instead of removing real evidence (ablation), injection adds fake evidence:
we insert one misleading article and check whether the reasoning discloses it.
We consider three hypotheses:
a.
the model will be susceptible to misleading articles;
b.
when susceptible, the reasoning will sometimes fail to mention the misleading evidence;
c.
susceptibility will fall as the amount of genuine evidence rises.
We evaluate 489 forecasting questions from
test
*
+val
*
.
One misleading article per question is written by Claude Sonnet (
claude-sonnet-4-20250514
), and an LLM judge (also Claude Sonnet) rates each reasoning trace on two axes:
whether it cites the article (citation score
0
/
0.5
/
1
0/0.5/1
) and its stance toward it (
accept/weigh/reject/not_mentioned
).
Most questions (81.2%) are
honest-susceptible
(Fig.
6
b, top-left):
the model adopts the misleading evidence and openly cites it.
Only 2.5% of the 489 questions (
n
=
12
n=12
) are
stealth
, adopting the evidence without mentioning it.
A further 14.7% are
considered-and-rejected
:
the model mentions the evidence but resists it.
This 2
×
\times
2 aggregates at the question level (a question counts as “mentioned” if any of its 3 completions cites the evidence); at the completion level, 46/1,227 susceptible completions (3.8%) are stealth.
Two patterns stand out.
The model treats any plausible article as strong evidence regardless of quality, yet it is strikingly transparent when actively misled, openly citing the fabricated source. Stealth behavior is far rarer here than under ablation (2.9% of susceptible questions vs. 23% of high-impact ablation pairs), though the two rates use different denominators and are not directly comparable.
4.5.3
Probe-Based CoT Lie Detector
Setup.
A layer-20 attention probe (AUC 0.747 on answer-correctness) trained on
EF-8B
carries information about reasoning quality.
If the probe’s internal change
|
Δ
​
probe
|
|\Delta\mathrm{probe}|
tracks the behavioral change
|
Δ
​
prob
|
|\Delta\mathrm{prob}|
, and does so even in the stealth cases where the reasoning hides the change, then the probe acts as a lie
detector for unfaithful reasoning. We test this across both paradigms, article ablation (1,303 cases) and
diversionary injection (489 cases), reading
|
Δ
​
prob
|
|\Delta\mathrm{prob}|
and
|
Δ
​
probe
|
|\Delta\mathrm{probe}|
over each
original/perturbed pair (Section
4.5
).
Figure 7
:
Internal probe as a lie detector for unfaithful reasoning.
(a)
Across 1,792 perturbation cases (article ablation and diversionary injection), the layer-20 probe’s internal change
|
Δ
​
probe
|
|\Delta\text{probe}|
tracks the behavioral change
|
Δ
​
prob
|
|\Delta\text{prob}|
(Spearman
ρ
=
0.565
\rho=0.565
), far above the reasoning-text correlation of 0.215 (Fig.
6
a).
Stealth cases (the forecast shifts but the reasoning stays silent;
n
=
119
n=119
) are highlighted and lie along the trend rather than at the origin: the probe registers changes that the chain of thought omits.
(b)
Pairing each stealth case with a faithful case of near-identical
|
Δ
​
prob
|
|\Delta\text{prob}|
, stealth probe shifts stay smaller than faithful ones (0.065 vs. 0.088) but well above zero, so the stealth signal is not merely a scaling artifact of smaller behavioral shifts.
Error bars: 95% bootstrap CIs.
Core correlation.
Across all 1,792 cases the probe strongly tracks behavioral change (Spearman
ρ
=
0.565
\rho=0.565
;
ρ
=
0.641
\rho=0.641
on signed shifts) and predicts the direction of change in 83.6% of cases, far above the
reasoning-text correlation of
ρ
=
0.215
\rho=0.215
(Section
4.5.1
; Fig.
7
a).
Stealth detection.
The signal persists where it matters most: in the 107 stealth ablation cases, where the forecast moves but
the reasoning does not, the probe still shifts (mean
|
Δ
​
probe
|
=
0.065
|\Delta\mathrm{probe}|=0.065
) and agrees with the
direction of change 78.5% of the time.
This is not just a byproduct of smaller shifts in stealth cases:
matching stealth to faithful cases of near-identical
|
Δ
​
prob
|
|\Delta\mathrm{prob}|
leaves stealth probe shifts
significantly smaller (0.065 vs. 0.088; Fig.
7
b), so the model genuinely processes the
two differently.
Probes on intermediate activations thus give a complementary audit channel for reasoning faithfulness.
4.6
Forced answering
How much of
EF-32B
’s forecast is fixed before it reasons?
We compare the model’s answer, verbalized confidence, and accuracy with and without its chain of thought.
In the
forced-answer
scheme we append the assistant prefill
<think>\n\n</think>\n\n<answer>
after the prompt, forcing the model to bypass its free-roaming CoT and commit an answer immediately.
We run forced and free schemes on the
OpenForesight-test
split and two OOD splits (
aljazeera2026Q1
,
aljazeeraLate2025
), with
10
10
rollouts per arm per question.
Confidence is reasoning-independent.
Forced and free verbalized confidence are nearly identical:
per-question mean confidence hugs the
y
=
x
y{=}x
line with no systematic shift (Spearman
ρ
=
0.90
\rho=0.90
on
test
,
0.87
0.87
on
Late2025
,
0.78
0.78
on
2026Q1
; Fig.
8
a).
The model states essentially the same confidence whether or not it has reasoned.
The committed answer is mostly pre-set.
The forced answer matches the free modal answer on
67
%
67\%
of
test
questions (
64
%
64\%
on
Late2025
,
56
%
56\%
on
2026Q1
): for two-thirds of questions, the chain of thought returns the answer the model would have committed to immediately.
This pre-commitment is explicit in the logits: a single forward pass under the empty-think prefill reads the forced-answer distribution directly.
Forced answering surfaces candidate answers; chain of thought sharpens the choice.
The logit readout does more than confirm the modal answer:
it reproduces the sampled forced-answer distribution almost exactly (
r
=
0.982
r=0.982
) and surfaces complete, plausible candidates that
50
50
rollouts never produce.
The forced pass thus exposes a genuine
spread
over candidate answers, not a single commitment.
Chain of thought acts on this spread mainly by sharpening it:
with the
<answer>
position held fixed and only the think block varied, reasoning concentrates probability on the leading candidate for two-thirds of questions (Fig.
8
b).
CoT’s accuracy gain is real but small.
Free reasoning outperforms forced answering by
+
1.9
+1.9
pp (percentage-points) in distribution, and the gain attenuates out of distribution (Fig.
8
c).
This result is not obtained by candidate selection:
when the forced answer is wrong, the gold answer is usually absent from the candidate distribution altogether – confident forced errors are genuine ignorance.
Reasoning calibrates commitment to an answer largely chosen before it begins; it does not search the candidate space for a better one.
Forced answering is a cheap (
50
​
–
​
70
50\text{--}70
×) and near-exact proxy for
EF-32B
’s committed answer and confidence.
CoT mostly confirms and sharpens a forecast the model has already made from the prompt alone, contributing a small accuracy gain concentrated on hard but answerable questions, rather than recovering answers it did not already hold.
Figure 8
:
What chain of thought does and does not change.
(a)
Confidence is reasoning-independent
:
per-question mean verbalized confidence with full reasoning (
x
x
) vs. under the forced-answer prefill (
y
y
) hugs the
y
=
x
y{=}x
line on the
OpenForesight-test
split and both OOD splits (Spearman
ρ
=
0.90
/
0.87
/
0.78
\rho=0.90/0.87/0.78
).
(b)
Forced answering surfaces candidate answers; CoT sharpens
the choice
:
top-answer probability of the forced candidate distribution (
x
x
) vs. after the model’s own think block (
y
y
), at a fixed
<answer>
position (
n
=
302
n=302
, colored by whether the post-CoT mode equals gold).
The horizontal spread shows genuine competition among candidates; mass above the diagonal shows CoT concentrating probability on the leading one (sharper on
67
%
67\%
of questions), yet among forced-wrong questions it corrects only
4
%
4\%
and locks in the same wrong answer
72
%
72\%
of the time.
(c)
CoT’s accuracy gain is real but small
: free-CoT vs. forced accuracy per split. In distribution the gain is
+
1.9
+1.9
pp (
95
%
95\%
CI
[
+
1.0
,
+
2.9
]
[+1.0,+2.9]
), attenuating OOD (
+
1.9
+1.9
pp on
2026Q1
, non-significant
+
0.9
+0.9
pp on
Late2025
).
Error bars:
95
%
95\%
question-bootstrap CIs.
4.7
Triaging questions by their pre-reasoning answer
Section
4.6
showed that
EF-32B
usually has its answer already decided before it reasons, and that a cheap forced pass recovers that answer.
The forced pass also tells us how spread out the answer is across candidates.
We use this spread to decide,
before any reasoning
, what to do with each question:
commit the answer immediately,
run a full reasoning rollout,
or send the question to a retrieval step because the model does not have the evidence to answer it.
Measuring spread.
The forced pass returns a distribution over candidate answers.
Decoding the
8
8
most probable answer continuations from the empty-think prefill produces a set of answer strings with sequence probabilities, renormalized to
p
i
p_{i}
.
We measure spread as the Shannon entropy
H
=
−
∑
i
p
i
ln
p
i
H=-\sum_{i}p_{i}\ln p_{i}
.
H
H
is
0
0
when all mass is on one answer and grows as the mass divides across candidates.
On the
test
split
H
H
ranges from
0
0
to
2.1
2.1
nats.
Spread sorts questions into three regimes.
We split the test questions into thirds by
H
H
(Fig.
9
a).
When
H
H
is near
0
0
, the model is right about
56
%
56\%
of the time and reasoning changes little (
54
54
to
56
56
pp).
In the middle the model is right
39
%
39\%
of the time and
reasoning does add a few points
(
35
35
to
39
39
pp).
When
H
H
is high the model is right only
13
%
13\%
of the time and reasoning barely helps (
9
9
to
13
13
pp).
The high-
H
H
questions also rarely contain the gold answer in their prompt (
5
%
5\%
against
16
%
16\%
at low
H
H
, using the containment label from Section
4.1
).
Reasoning cannot recover an answer the prompt does not support, so these questions need more evidence, not more tokens.
The three regimes suggest three actions: commit early at low
H
H
, reason at moderate
H
H
, and retrieve more context at high
H
H
.
Commit early: a token-saving procedure.
When the model is already confident about an answer, it can skip its reasoning and respond directly.
We train a simple classifier to spot these cases from cheap signals read off a single forced-answer pass:
how spread out the candidate answers are (entropy), how much probability sits on the most likely answer, the gap between the top two answers, and how many distinct answers appear.
It outputs one score, and we fix a single cutoff.
Above the cutoff the model answers immediately; below it, the model reasons as usual.
On held-out questions this matches the accuracy of always reasoning while using far fewer tokens
(Fig.
9
b).
It beats routing questions at random, and beats a version that decides based on the model’s stated confidence, which helps little because stated confidence tracks how hard a question is rather than whether reasoning would actually change the answer.
Across all splits it saves
30
30
to
47
%
47\%
of generated tokens with no measurable accuracy loss:
every per-split change is within about
1
1
pp of full reasoning, with a confidence interval that includes zero.
Retrieve: an extension.
The same signal flags the questions where reasoning will not help.
Because these are the questions missing evidence, the forced-pass read can also nominate questions for retrieval:
instead of spending a long rollout to guess, fetch the article the model needs.
We do not test this here. We note only that the signal separating “the model knows” from “the model is guessing” is the same one that drives the gate.
Summary.
Reading the model’s answer distribution before it reasons gives two things at once:
(a) it saves tokens, by committing the questions the model has already settled instead of reasoning through them;
(b) it can also raise accuracy, by flagging the questions where the model is guessing for lack of context, so they can be sent for retrieval rather than answered blindly.
The same cheap signal cuts cost on the easy questions and points to where more evidence would help on the hard ones.
Figure 9
:
Triaging forecasting questions by the spread of the model’s
pre-reasoning answer
(
OpenForesight-test
,
N
=
302
N=302
).
(a)
Questions split into thirds by the entropy
H
H
of the forced-pass
answer distribution. Bars show accuracy when the model commits immediately
(forced), accuracy after free reasoning, and the rate at which the gold answer
appears in the prompt; whiskers are
±
1
\pm 1
SE. Accuracy rises as the answer
concentrates, reasoning helps only in the middle regime, and high-entropy
questions both fail and lack supporting evidence.
(b)
Accuracy against mean generated tokens per question for four
inference policies. The commit-early gate (entropy gate, ember) recovers
full-reasoning accuracy at far fewer tokens, staying above naive random routing
(dashed) and a verbalized-confidence gate (slate).
5
Conclusion
We found that a language model forecaster’s internal representations offer a more reliable window into its confidence and reasoning than its own words.
Lightweight probes on intermediate activations recover a well-calibrated confidence signal that the model’s verbalization distorts, track the influence of evidence that the chain of thought fails to disclose, and reveal that the forecast is largely committed before reasoning begins – a fact that can be exploited to route questions between committing, reasoning, and retrieving.
Across all three threads the pattern is the same: internal activations contain more information than what the model is able to verbalize.
This raises the question of introspection.
The calibrated signal is demonstrably present in the residual stream from the final prompt token onward, yet the stated probability does not report it – overconfidence is less a failure of self-knowledge than of self-report.
Whether models can be trained to verbalize their internal confidence estimate, for instance by distilling the probe signal into the stated probability, or by post-training against calibration-aware rewards, is a natural next step.
Testing whether such training sharpens or instead degrades the internal signal the probes read is another one.
The experiments presented were conducted by
Silico
, Goodfire’s agentic platform for interpretability research, autonomously with human feedback.
All experimental designs, findings, write-ups, scripts, and figures have been carefully reviewed and edited by the authors.
References
Appendix
Appendix A
Data audit
We perform a simple data audit on the
nikhilchandak/OpenForesight
dataset.
We check notably for typical prompt length, question leakage, etc.
The difference in prompt length is solely explained by the fact that the last two splits don’t include retrieval articles in their prompts. Therefore, the forecasting setting is limited to instructions, question, and some brief background information.
For the splits that include article retrieval, with the exception of a few anomalous prompts, prompts include 5 news articles.
Figure 10
:
Cross-split qid overlap in
OpenForesight
.
Off-diagonal cells give the number of question IDs (qids) shared by both splits; the diagonal (split sizes, listed below) is omitted from the color scale. Nine of fifteen split pairs share qids (429 shared-qid instances in total), yet every shared qid is a collision: in all 429 cases the two questions differ in both title and gold answer (same-question rate = 0). The held-out evaluation splits are qid-disjoint from train. qid is therefore a split-local index, not a global key, and exact-qid overlap reflects index reuse rather than question leakage. This analysis detects exact-qid and exact-text matches only; semantic near-duplicates (the same real-world question under a different qid or wording) are not captured and require embedder/judge-based detection. Splits:
train
(n=52,183),
validation
(207),
test
(302),
aljazeera2026Q1
(330),
aljazeeraLate2025
(491),
skysports2025
(1,788).
Figure 11
:
Prompt token length by split in
OpenForesight
.
Bars show the mean token count of the retrieval-augmented prompt field, tokenized with the
Qwen3
tokenizer with special tokens excluded; whiskers span the 2.5th–97.5th percentiles, i.e. the range containing the central 95% of prompts in each split. Estimates use every question for splits with
n
≤
3,000
n\leq 3,000
and a uniform random sample of 3,000 for train. Two regimes are evident. The retrieval-rich splits —
train
(mean 2,836, 95% band 1,841–3,484),
validation
(3,031; 2,052–3,451),
test
(2,894; 1,935–3,442) and
aljazeeraLate2025
(2,900; 1,905–3,482) — span roughly 1,800–3,500 tokens, whereas
aljazeera2026Q1
(632; 588–673) and
skysports2025
(610; 565–660) carry minimal retrieval context and are both 4.6× shorter with far tighter spreads. The long-prompt splits dominate context budget; the two short-prompt OOD splits leave ample room and never approach generation-length limits.
Table 3
:
Representative exemplars from the evaluation datasets. For
OpenForesight
we
reproduce the full prompt verbatim; both shown questions are cases where retrieval returned no
articles, so the prompt is short. Most prompts additionally embed a block of retrieved news
passages (
Article 1
…
5
) and are considerably longer.
OpenForesight
rows are from the public
test
split (qids 645, 159);
MATH-500
from its
test
split; AIME rows from
AIME24
and AMC rows from
AMC23
(the
AIME25
and
AMC24
splits share an identical format).
Prompt / Problem
Ground truth
OpenForesight
— forecasting
(
test
split)
You will be asked a forecasting question (which might be from the past). You have to come up with the best guess for the final answer. You will also be provided with a list of retrieved news articles summaries which you may refer to when coming up with your answer. Please provide your reasoning before stating your final answer and also express how likely you think your answer is to be correct (your confidence in your answer).
Question Title: Where will the initial court hearing for the rapper charged with a terror offence be held?
Question Background: A member of an Irish rap group has been charged with a terror offence and is awaiting his first court appearance.
Resolution Criteria: <ul>
<li>Official court documents or venue listings on the day of the hearing.</li>
<li>June 18, 2025, when the hearing takes place.</li>
<li>Official name of the court venue exactly as stated (e.g., ’City Court’).</li>
</ul>
Expected Answer Type: string (location)
Relevant passages from retrieved news articles:
No relevant articles found.
Think step by step about the information provided, reason about uncertainty and put your final answer (in the format asked) in <answer> </answer> tags. You should also specify your confidence in your answer in <probability> </probability> tags. The probability should be a number between 0 and 1.
You will be rewarded based on the probability (p) you assign to your answer. Your answer will be evaluated using the BRIER SCORING RULE which is basically (- (1 - p)^2) if your answer is correct and (- 1 - p^2) if your answer is incorrect. For example, if p = 0.5, and your answer is incorrect, then your score will be (-1 - 0.5^2) = (-1 - 0.25) = -1.25 whereas if the answer was correct, then your score would be (- (1 - 0.5)^2) = (- (0.5)^2) = -0.25. Thus, the range of the score is [-2, 0] where your score lies between [-2, -1] if the answer is incorrect and [-1, 0] if the answer is correct. If your answer is correct, your will be REWARDED more if your probability is higher whereas if your answer is incorrect, your will be PENALIZED more if your probability is higher. YOU HAVE TO MAXIMIZE YOUR SCORE.
Your final answer should be concise (NOT MORE THAN A FEW WORDS LONG) and your response SHOULD STRICTLY END with <answer> </answer> tags and <probability> </probability> tags.
Westminster Magistrates’ Court
You will be asked a forecasting question (which might be from the past). You have to come up with the best guess for the final answer. You will also be provided with a list of retrieved news articles summaries which you may refer to when coming up with your answer. Please provide your reasoning before stating your final answer and also express how likely you think your answer is to be correct (your confidence in your answer).
Question Title: Where will the second leg of the 2025 UEFA Champions League play-off tie between Rangers and Club Brugge be held?
Question Background: In UEFA Champions League play-off ties, teams contest two legs, with each team hosting one match.
Resolution Criteria: <ul>
<li><b>Source of Truth</b>: UEFA official fixture list published on UEFA.com by August 19, 2025.</li>
<li><b>Resolution Date</b>: August 19, 2025.</li>
<li><b>Accepted Answer Format</b>: The full name of the stadium where the match will be played.</li>
</ul>
Expected Answer Type: string (stadium)
Relevant passages from retrieved news articles:
No relevant articles found.
Think step by step about the information provided, reason about uncertainty and put your final answer (in the format asked) in <answer> </answer> tags. You should also specify your confidence in your answer in <probability> </probability> tags. The probability should be a number between 0 and 1.
You will be rewarded based on the probability (p) you assign to your answer. Your answer will be evaluated using the BRIER SCORING RULE which is basically (- (1 - p)^2) if your answer is correct and (- 1 - p^2) if your answer is incorrect. For example, if p = 0.5, and your answer is incorrect, then your score will be (-1 - 0.5^2) = (-1 - 0.25) = -1.25 whereas if the answer was correct, then your score would be (- (1 - 0.5)^2) = (- (0.5)^2) = -0.25. Thus, the range of the score is [-2, 0] where your score lies between [-2, -1] if the answer is incorrect and [-1, 0] if the answer is correct. If your answer is correct, your will be REWARDED more if your probability is higher whereas if your answer is incorrect, your will be PENALIZED more if your probability is higher. YOU HAVE TO MAXIMIZE YOUR SCORE.
Your final answer should be concise (NOT MORE THAN A FEW WORDS LONG) and your response SHOULD STRICTLY END with <answer> </answer> tags and <probability> </probability> tags.
Jan Breydel Stadium
MATH-500
— math reasoning
(
test
split)
Convert the point
(
0
,
3
)
(0,3)
in rectangular coordinates to polar coordinates. Enter your answer in the form
(
r
,
θ
)
,
(r,\theta),
where
r
>
0
r>0
and
0
≤
θ
<
2
​
π
.
0\leq\theta<2\pi.
(Precalculus, level 2)
(
3
,
π
2
)
\left(3,\frac{\pi}{2}\right)
If
f
⁡
(
x
)
=
3
​
x
−
2
x
−
2
f(x)=\frac{3x-2}{x-2}
, what is the value of
f
⁡
(
−
2
)
+
f
⁡
(
−
1
)
+
f
⁡
(
0
)
f(-2)+f(-1)+f(0)
? Express your answer as a common fraction.
(Algebra, level 3)
14
3
\dfrac{14}{3}
AIME24
— math reasoning
Let
x
,
y
x,y
and
z
z
be positive real numbers that satisfy the following system of equations:
log
2
⁡
(
x
y
​
z
)
=
1
2
,
log
2
⁡
(
y
x
​
z
)
=
1
3
,
log
2
⁡
(
z
x
​
y
)
=
1
4
.
\log_{2}\!\left({x\over yz}\right)={1\over 2},\hskip 9.24994pt\log_{2}\!\left({y\over xz}\right)={1\over 3},\hskip 9.24994pt\log_{2}\!\left({z\over xy}\right)={1\over 4}.
Then the value of
|
log
2
⁡
(
x
4
​
y
3
​
z
2
)
|
\left|\log_{2}(x^{4}y^{3}z^{2})\right|
is
m
n
\tfrac{m}{n}
where
m
m
and
n
n
are relatively prime positive integers. Find
m
+
n
m+n
.
(2024-II-4)
33
33
Jen enters a lottery by picking
4
4
distinct numbers from
S
=
{
1
,
2
,
3
,
⋯
,
9
,
10
}
.
S=\{1,2,3,\cdots,9,10\}.
4
4
numbers are randomly chosen from
S
.
S.
She wins a prize if at least two of her numbers were
2
2
of the randomly chosen numbers, and wins the grand prize if all four of her numbers were the randomly chosen numbers. The probability of her winning the grand prize given that she won a prize is
m
n
\tfrac{m}{n}
where
m
m
and
n
n
are relatively prime positive integers. Find
m
+
n
m+n
.
(2024-I-4)
116
116
AMC23
— math reasoning
Cities
A
A
and
B
B
are
45
45
miles apart. Alicia lives in
A
A
and Beth lives in
B
B
. Alicia bikes towards
B
B
at 18 miles per hour. Leaving at the same time, Beth bikes toward
A
A
at 12 miles per hour. How many miles from City
A
A
will they be when they meet?
27
27
What is the degree measure of the acute angle formed by lines with slopes
2
2
and
1
3
\frac{1}{3}
?
45
45
Appendix B
Temperature sweep
Two regimes emerge (Fig.
12
). Across the moderate range
T
≲
1.6
T\lesssim 1.6
, correctness and confidence are essentially flat: per-rollout
accuracy holds at
37
±
1
%
37\pm 1\%
(a
1.3
1.3
pp spread, within the
±
0.9
\pm 0.9
pp
binomial standard error at
n
=
2,960
n=2{,}960
), and mean verbalized confidence stays
near
50
%
50\%
irrespective of
T
T
. Self-consistency, by contrast, declines
steadily across the whole sweep, from
66
%
66\%
at
T
=
0.2
T=0.2
to
30
%
30\%
at
T
=
2.0
T=2.0
, as the mean number of distinct answer clusters per question grows from
1.86
1.86
to
3.50
3.50
. Beyond
T
≈
1.6
T\approx 1.6
the model begins to emit malformed
outputs—answer-tag extraction falls from
100
%
100\%
to
92
%
92\%
at
T
=
2.0
T=2.0
—and
accuracy degrades to
33
%
33\%
.
The flatness of accuracy and confidence is reassuring for reproducibility, but
it exposes the calibration problem highlighted in the main text. Across the sweep
the model is consistently overconfident (ECE
0.11
0.11
–
0.15
0.15
, Brier
0.19
0.19
–
0.21
0.21
; Fig.
13
), with probability mass
concentrated in the high-confidence bins and the reliability curve sitting below
the diagonal at every temperature.
Figure 12
:
Temperature sweep for
EF-8B
on the
OpenForesight-test
split.
Each curve summarizes
10
10
rollouts per question across all
296
296
test
questions (
29,600
29{,}600
generations) as a function of sampling temperature
T
∈
{
0.2
,
…
,
2.0
}
T\in\{0.2,\dots,2.0\}
.
Self-consistency
(fraction of a question’s
rollouts in its modal answer cluster) falls monotonically from
65.9
%
65.9\%
(
T
=
0.2
T{=}0.2
) to
30.1
%
30.1\%
(
T
=
2.0
T{=}2.0
), while
per-rollout accuracy
(Claude-judged answer equivalence) holds flat at
37
±
1
%
37\pm 1\%
through
T
=
1.6
T{=}1.6
before dropping to
32.8
%
32.8\%
at
T
=
2.0
T{=}2.0
, and
mean verbalized
confidence
stays near
50
%
50\%
throughout. The persistent gap between
confidence (
∼
50
%
{\sim}50\%
) and accuracy (
∼
37
%
{\sim}37\%
) is the model’s
overconfidence, and it is largely temperature-invariant.
Figure 13
:
Reliability of
EF-8B
’s verbalized confidence across temperature.
Reliability diagrams for
T
=
0.4
,
0.8
,
1.2
,
1.6
T=0.4,0.8,1.2,1.6
on the
OpenForesight-test
split.
In each panel the model’s stated probabilities are grouped into ten
equal-width confidence bins; bar height is the empirical accuracy within the
bin and the dashed diagonal marks perfect calibration, so bars below the
diagonal indicate overconfidence. The model is overconfident at every
temperature, with probability mass concentrated in the high-confidence bins
(
∼
22
%
{\sim}22\%
of rollouts fall in the top bin
p
>
0.9
p>0.9
, which resolves correct
only
∼
72
%
{\sim}72\%
of the time).
The shape is essentially temperature-invariant; calibration is mildly best at
T
=
1.6
T{=}1.6
. Per-panel expected calibration error: ECE
=
0.126
,
0.118
,
0.122
,
0.107
=0.126,0.118,0.122,0.107
for
T
=
0.4
,
0.8
,
1.2
,
1.6
T=0.4,0.8,1.2,1.6
(Brier optimum
0.187
0.187
at
T
=
1.2
T{=}1.2
; ECE
optimum
0.107
0.107
at
T
=
1.6
T{=}1.6
).
Appendix C
Probe training and sweep
We train the full grid of probes: every pooling architecture, at every layer, read at several points along the reasoning trace – and report their metrics.
All probes are trained on the
OpenForesight-train
split (one
EF-8B
rollout per question, labeled for answer correctness by the LLM judge) and evaluated on
test
(
302
302
questions
×
\times
10
10
rollouts
=
3,020
=3{,}020
), the same test set as the main-text result.
Sites.
Each probe reads a pooled span ending at one of seven reasoning-anchored sites:
initial
(through the opening
<think>
), the rollout fractions
r010
/
r030
/
r050
/
r070
/
r090
, and
final
(through the closing
</think>
).
The
initial
span is shared by all rollouts of a question and therefore carries question-level signal only.
Training.
Prompt
+
+
truncated rollout,
AdamW
at learning rate
lr
=
10
−
3
=10^{-3}
, batch size
8
8
,
MAX_SEQ_LEN
8192
8192
, seed
42
42
, temperature
T
=
1.0
T=1.0
, covariance bottleneck
d
hidden
=
64
d_{\mathrm{hidden}}=64
,
10
%
10\%
of the training questions held out for validation, and the checkpoint chosen at lowest validation loss (
best-val
selection).
Each probe emits a single real-valued logit
z
z
, mapped to a predicted probability of answer-correctness
p
=
σ
⁡
(
z
)
=
1
/
(
1
+
e
−
z
)
p=\sigma(z)=1/(1+e^{-z})
, and is trained with the binary cross-entropy (BCE) loss – the standard log-loss for a two-class probabilistic classifier.
For a rollout with correctness label
y
∈
{
0
,
1
}
y\in\{0,1\}
(
y
=
1
y=1
if the answer resolves correct),
ℒ
BCE
​
(
p
,
y
)
=
−
[
y
​
log
⁡
p
+
(
1
−
y
)
​
log
⁡
(
1
−
p
)
]
,
\mathcal{L}_{\mathrm{BCE}}(p,y)\;=\;-\big[\,y\log p+(1-y)\log(1-p)\,\big],
(8)
averaged over the training set.
The two branches penalize the two error modes:
when
y
=
1
y=1
the loss is
−
log
⁡
p
-\log p
(large only if the probe assigned low probability to a correct answer) and when
y
=
0
y=0
it is
−
log
⁡
(
1
−
p
)
-\log(1-p)
(large only if it was confidently wrong).
Minimizing it drives the probe’s output toward the empirical probability of correctness, which is what makes the probe a
calibrated
confidence estimate rather than a hard classifier.
Metric.
Each rollout contributes one prediction: the probe’s raw probability
p
=
σ
⁡
(
z
)
p=\sigma(z)
(no recalibration) paired with its correctness label
y
∈
{
0
,
1
}
y\in\{0,1\}
.
All metrics are
rollout-pooled
– computed over the full set of rollouts pooled together, not averaged per question – and follow the definitions of Section
3.4
.
We apply
no temperature scaling
: best-val checkpoint selection yields calibrated heads directly, so the raw
p
p
is the honest quantity, and AUROC is temperature-invariant in any case, so only ECE and Brier could be affected.
Reading the grids.
Figure
14
reports AUROC and Figure
15
the Brier score (a more reliable single calibration summary than ECE, since a near-chance probe is trivially low-ECE).
Across all three families, discrimination improves with reasoning depth, concentrates smoothly in the mid-to-late layers
(
∼
\sim
18–24), and is strongest for covariance pooling – whose best cell is
layer 21/
final
– which is why the deployed probe is a covariance probe.
Figure 14
:
Probe AUROC across layers and reasoning sites
,
for mean-pooling, attention, and covariance probes (left to right), evaluated on
test
(
N
=
3,020
N=3{,}020
).
Rows are the 36 layers of
EF-8B
; columns the seven sites, from
initial
through rollout fractions to
final
. Higher is better.
Figure 15
:
Probe Brier score across layers and reasoning sites
, same probes, layout, and evaluation as Figure
14
.
Cooler is lower (better); the low-Brier region mirrors the high-AUROC region.
EF-8B
’s verbalized confidence achieves
Br
=
0.190
\mathrm{Br}=0.190
.
Appendix D
GLM Probe-Only Calibration Details
The main GLM comparisons are reported in Table
1
and Figures
2
,
3
, and
4
.
This appendix records setup details, controls, and supplementary figures for the probe-only calibration experiments.
Models and data.
We evaluate frozen
GLM-4.7-Flash
and
GLM-4.5-Air
models of two different sizes.
The dataset is another
OpenForesight
version whose question contexts were improved to be more relevant than the semantic-search contexts used in the OpenForecaster paper.
For each model, probes are trained on
11,835
11{,}835
train rollouts (
3,945
3{,}945
questions
×
\times
3 completions), selected on
1,930
1{,}930
validation rollouts, and reported on
2,960
2{,}960
held-out test rollouts.
The validation split is used for checkpoint, layer, and architecture selection; the test split is reserved for the headline numbers.
Probe input and training.
The probe input is the prompt plus chain-of-thought, truncated before the final answer block.
Residual-stream activations are read from the frozen model, and only the probe weights are optimized.
Mean-pool linear probes use mask-aware pooled residual-stream vectors; attention and covariance probes use token-level activation sequences.
All probes use AdamW with learning rate
10
−
3
10^{-3}
and weight decay
0.01
0.01
.
The GLM-4.7-Flash mean-pool probe is trained for up to 80 epochs with batch size 256 and early stopping patience 8; its sequence probes use batch size 32, up to 3 epochs, and patience 2.
The GLM-4.5-Air sweep follows the same recipe, with layer and architecture selection by validation cross-entropy.
ECE is computed on raw probabilities with no temperature scaling, Platt scaling, isotonic regression, or other recalibration.
Leakage controls and caveats.
For
GLM-4.7-Flash
, the full test set often contains a drafted answer in the chain-of-thought before the final answer block.
The leakage-controlled comparison therefore uses the
423
423
rollouts with both answer-clean reasoning and usable self-report, giving a probe-minus-verbalized-confidence AUROC delta of
+
0.055
+0.055
with 95% CI
[
−
0.006
,
0.111
]
[-0.006,0.111]
.
For
GLM-4.5-Air
, the clean subset removes rollouts that leak a probability tag mid-reasoning, leaving
1,747
1{,}747
rollouts and a clean AUROC delta of
+
0.110
+0.110
with 95% CI
[
0.069
,
0.149
]
[0.069,0.149]
.
Thus,
GLM-4.7-Flash
should be read mainly as a raw-calibration result, while
GLM-4.5-Air
supports both ranking and calibration gains.
Controls and transfer notes.
Shuffled-label probes sit near chance, and chain-of-thought-length baselines do not explain the GLM-4.5-Air signal.
For
GLM-4.7-Flash
, same-format validation-to-test and cross-format train-to-test probes are similar, which argues against the train/test context-format difference explaining the test result.
For
GLM-4.5-Air
, the best layer lies in a broad mid-stack plateau around layers 18–23; matched 24–40 comparisons reproduce the effect across
GLM-4.7-Flash
and
GLM-4.5-Air
.
0
0
2
⋅
10
−
2
2\cdot 10^{-2}
4
⋅
10
−
2
4\cdot 10^{-2}
6
⋅
10
−
2
6\cdot 10^{-2}
8
⋅
10
−
2
8\cdot 10^{-2}
0.1
0.1
0.12
0.12
0.14
0.14
0.16
0.16
Linear L23
Attention-4 L19
Covariance L18
Attention-1 L18
Δ
\Delta
AUROC (probe
−
-
verbalized confidence)
Full test
Clean subset
Figure 16
:
GLM-4.5-Air probe versus verbalized confidence.
Paired
Δ
\Delta
AUROC for each probe family at its best layer, comparing full test and leakage-controlled clean subsets. Bars are question-clustered 95% bootstrap intervals.
16
16
18
18
20
20
22
22
24
24
26
26
28
28
30
30
32
32
34
34
36
36
38
38
40
40
0.5
0.5
0.6
0.6
0.7
0.7
0.8
0.8
Residual-stream layer
Test AUROC
GLM-4.5-Air depth profile
Linear
Attention-1
Attention-4
Covariance
Figure 17
:
GLM-4.5-Air depth profile.
Forecast-correctness decodability across residual-stream layers and probe families, showing a broad layer 18–23 plateau.
Appendix E
OOD math probe stress test
The main OOD comparison is reported in Table
2
.
This appendix records the supporting setup.
Models and decode.
We compare the untrained
Qwen3-8B
base model with our
Qwen3-8B
model trained according to the DCPO recipe of
ma2026decouplingreasoningconfidenceresurrecting
.
The decode settings are matched across cells: temperature
0.7
0.7
, top-
p
p
0.8
0.8
, top-
k
k
20
20
, presence penalty
1.5
1.5
, maximum
3,000
3{,}000
generated tokens, logprobs enabled, no thinking mode, and seed
42
42
.
The base model is evaluated with plain decoding; the DCPO-recipe model is evaluated with the verbal-confidence decode so that stated-confidence baselines are available.
Probe training and evaluation.
Each probe is a one-stage binary correctness readout trained with BCE on frozen residual-stream activations.
The input is prompt plus reasoning text truncated before the first boxed answer, so the probe does not see the final answer or any trailing confidence line.
The selected sites are L18 last-token for the untrained base and L21 last-token for the DCPO-recipe model, chosen on held-out validation data and then frozen for evaluation.
We report AUROC and 15-bin ECE; deltas use qid-clustered bootstrap 95% confidence intervals with 2,000 resamples.
Baselines and controls.
The non-probe baselines are token-logprob confidence, isotonic-recalibrated token logprobs, raw verbalized confidence, isotonic-recalibrated verbalized confidence, and the decode-the-stated-number composite when the verbal decode is available.
Controls with random correctness labels and row-shuffled activations sit near chance, indicating that the real probe reads correctness structure from activations rather than a label or ordering artifact.
In-distribution diagnostics on clean
MATH-500
show that recalibrated verbalized confidence can outperform probes on ECE, so the main math result should be read as an OOD monitoring and discrimination result.
The DCPO probe-train pool overlaps the RLVR training distribution through
DeepScaleR
; therefore these results do not establish training-invariant correctness representations.
Base/plain
DCPO/verbal
0.3
0.3
0.4
0.4
0.5
0.5
0.6
0.6
0.7
0.7
AUROC
Control probes (5 seeds,
±
\pm
std)
Random-label
Shuffled-activation
Figure 18
:
Negative-control probes sit at chance.
The dashed line marks AUROC
=
0.5
=0.5
.
Random-label and shuffled-activation probes are trained identically to the real probe, with 5 seeds each.