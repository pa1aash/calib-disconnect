---
title: 'LLMs as Signal Detectors: Sensitivity, Bias, and the Temperature-Criterion
  Analogy (full text; arXiv companion of OSF qpk9a)'
id: llms-as-signal-detectors-sensitivity-bias-and-the-temperature-criterion-analogy
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
created: '2026-11-09T23:11:02.361526Z'
updated: '2026-11-09T23:27:44.702650Z'
source: https://arxiv.org/pdf/2603.14893
status: review
type: note
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv 2603.14893, Cacioli, 16 Mar 2026), arXiv companion of OSF
  10.17605/osf.io/qpk9a (OSF itself not reachable: redirect to osf.io). Preregistered
  SDT analysis of Llama-3-8B-Instruct, Mistral-7B-Instruct-v0.3, Llama-3-8B-Base on
  TriviaQA/NQ-Open, 168,000 trials; ECE conflates sensitivity and bias; z-ROC slopes
  0.52-0.84, instruct 0.52-0.63 vs base 0.77-0.87; temperature changes both d'' and
  criterion. Factual QA only, no code. Close for F in general-LLM metrology; code
  not occupied.'
---

LLMs as Signal Detectors: Sensitivity, Bias, and the
Temperature–Criterion Analogy

arXiv:2603.14893v1 [cs.CL] 16 Mar 2026

Jon-Paul Cacioli
Independent Researcher, Melbourne, Australia
synthium@hotmail.com
ORCID: 0009-0000-7054-2014

1

Abstract

Introduction

When a large language model (LLM) answers a factual question, two things matter: can the model discriminate correct from incorrect responses, and does
its expressed confidence reflect that discrimination?
These are fundamentally different problems requiring
different interventions. A model that cannot discriminate needs better training data or architectural improvements. A model that discriminates well but expresses confidence poorly needs recalibration, not retraining. Current evaluation practice does not make
this distinction.
Expected Calibration Error (ECE; Guo et al.,
2017), the standard metric, computes the average
discrepancy between confidence and accuracy within
binned intervals. A model achieves low ECE by being accurate at the rate it claims, regardless of its
discriminative ability. ECE says nothing about discrimination per se: a model that is uniformly wrong
at a rate matching its confidence achieves perfect calibration with zero sensitivity. The Brier score decomposes into reliability, resolution, and uncertainty,
but not into sensitivity and bias. Semantic entropy
(Kuhn et al., 2023) measures uncertainty without decomposing its sources. Confidence elicitation methods (Tian et al., 2023) and post-hoc recalibration approaches (Shen et al., 2024) improve calibration but
likewise operate on the composite metric.
Signal Detection Theory (SDT; Green and Swets,
1966; Macmillan and Creelman, 2005) provides
exactly this decomposition.
Developed in psychophysics to characterise perceptual decisions under
uncertainty, SDT separates performance into sensitivity (d′ or da ) and criterion (c). These parameters
are mathematically independent: changing the payoff
structure shifts c without affecting d′ , while degrading stimulus quality reduces d′ without shifting c.
SDT-derived metrics are already entering the LLM
evaluation literature, though typically in limited

Large language models (LLMs) are evaluated for calibration using metrics such as Expected Calibration
Error that conflate two distinct components: the
model’s ability to discriminate correct from incorrect
answers (sensitivity) and its tendency toward confident or cautious responding (bias). Signal Detection
Theory (SDT) decomposes these components. While
SDT-derived metrics such as AUROC are increasingly used, the full parametric framework — unequalvariance model fitting, criterion estimation, z-ROC
analysis — has not been applied to LLMs as signal detectors. In this pre-registered study, we treat
three LLMs as observers performing factual discrimination across 168,000 trials and test whether temperature functions as a criterion shift analogous to
payoff manipulations in human psychophysics. Critically, this analogy may break down because temperature changes the generated answer itself, not only
the confidence assigned to it. Our results confirm the
breakdown with temperature simultaneously increasing sensitivity (AUC) and shifting criterion. All models exhibited unequal-variance evidence distributions
(z-ROC slopes 0.52–0.84), with instruct models showing more extreme asymmetry (0.52–0.63) than the
base model (0.77–0.87) or human recognition memory (∼0.80). The SDT decomposition revealed that
models occupying distinct positions in sensitivity–
bias space could not be distinguished by calibration
metrics alone, demonstrating that the full parametric
framework provides diagnostic information unavailable from existing metrics.
Keywords: signal detection theory, large language
models, calibration, sensitivity, temperature, ROC
analysis
1

forms. Steyvers and Peters (2025) review LLM
metacognition through the lens of metacognitive sensitivity, using AUROC and the meta-d′ framework
(Maniscalco and Lau, 2012, 2014) to quantify how
well models’ confidence discriminates correct from incorrect answers. Steyvers et al. (2025) demonstrate
that implicit confidence measures (token likelihoods)
exhibit greater metacognitive sensitivity than verbalised confidence. Earlier, Kadavath et al. (2022)
established that LLMs can discriminate questions
they answer correctly from those they do not, providing the empirical foundation for treating LLMs as
signal detectors. These important advances establish that SDT-adjacent measures reveal meaningful
structure in LLM confidence. However, they stop
short of applying the full parametric framework: fitting unequal-variance Gaussian SDT models to multipoint ROC data, independently estimating criterion
placement, testing specific predictions about how experimental manipulations affect the ROC, and validating with converging forced-choice paradigms. The
present work takes this next step.
The analogy between temperature scaling and criterion manipulation motivates a specific, testable prediction. In human SDT experiments, manipulating
payoffs shifts the criterion without changing the observer’s sensory capacity. Temperature scaling performs a formally analogous operation on the logit
distribution, changing the mapping from evidence to
response probability without changing the evidence
(logits) themselves. If this analogy holds, temperature should shift the LLM’s criterion while leaving
sensitivity unchanged.
However, there is a critical disanalogy that we flag
from the outset: in human experiments, the stimulus is identical regardless of the observer’s criterion
setting. In LLMs, temperature affects the sampling
process, meaning the generated answer, and therefore the trial outcome, can change. The model may
follow a different generative path, producing a different answer entirely. This "stimulus dependence
on criterion" breaks a core assumption of the payoffmanipulation analogy. Our study was designed to
test whether and where this breakdown occurs: does
temperature behave as a criterion shift despite the
disanalogy, and if not, what is the nature of the departure?
We report a pre-registered study applying the full
SDT framework to three LLMs performing factual
question-answering across seven temperatures. The
study comprises 168,000 confidence-rating trials and
6,000 forced-choice trials across two datasets. All hypotheses, analyses, and preprocessing decisions were
registered on the Open Science Framework before

data collection.
The study makes three core contributions:
1. Temperature is not a pure criterion manipulation. It simultaneously changes sensitivity and
criterion, a dual effect revealing that the payoff analogy breaks down because the "stimulus"
(generated answer) depends on the "criterion"
(temperature).
2. LLMs exhibit unequal-variance evidence distributions. z-ROC slopes range from 0.52 to 0.84,
with instruct models showing more extreme unequal variance than the base model. This parallels but exceeds findings in human recognition
memory (typically s ≈ 0.80; Mickes et al., 2007).
3. The SDT decomposition reveals structure invisible to calibration metrics. Models with different sensitivity and bias profiles cannot be distinguished by ECE alone, demonstrating the practical value of the decomposition for targeted intervention.

2

Signal Detection Theory Applied to LLMs

2.1

The SDT Framework

The SDT framework is well established within the
psychophysics literature. On each trial, the observer
receives evidence drawn from either a noise distribution (signal absent) or a signal distribution (signal present) and applies a criterion to generate a
response. Sensitivity (d′ ) is the standardised distance between distribution means; criterion (c) is
the threshold location. In the unequal-variance SDT
(UVSD) model, the signal distribution has greater
variance than the noise distribution, parameterised
by the ratio s = σnoise /σsignal . The z-ROC slope directly estimates s, and z-ROC slopes below 1.0 indicate unequal variance. The sensitivity measure da =
p
2/(1 + s2 ) × (s × z(HR) – z(FAR)) accounts for
the variance asymmetry (Macmillan and Creelman,
2005).
Confidence-rating ROC data provide richer information than binary responses: each confidence level
acts as a virtual criterion, generating multiple ROC
points (Macmillan and Creelman, 2005, Chapter 3).
The area under the ROC (AUC) provides a nonparametric sensitivity measure requiring no distributional assumptions.
2

2.2

The LLM-as-Observer Mapping

Temperature is the criterion manipulation. At
temperature T, softmax probability is pi = exp(zi /T)
/ Σ exp(zj /T). Lower temperatures sharpen the distribution (conservative responding); higher temperatures flatten it (liberal responding). This is formally
analogous to payoff manipulation, but with the crucial disanalogy that higher temperatures also change
which tokens are sampled, potentially changing the
answer itself.

We map SDT onto LLM question-answering as follows. Each factual question is a trial. The model
is the observer. The question has a correct answer (signal) or the model produces an incorrect
answer (noise). The evidence variable is the normalised log-probability
P (NLP) of the generated answer: NLP = (1/L) log p(ti | t<i ), where L is the
answer length in tokens. Higher NLP indicates the
model assigns greater probability to its answer, analogous to stronger sensory evidence.
This mapping is functional, not literal. SDT is
applied here as a measurement framework for decomposing performance, not as a cognitive model of
LLM processing. Unlike human perception, where
the evidence variable is a latent sensory representation, NLP is directly observable. Unlike human signal
detection, where the observer passively receives stimuli, the LLM generates the response it then evaluates. SDT has precedent for application beyond perception, including medical diagnosis (Swets, 1996),
eyewitness identification (Wixted and Mickes, 2014),
and automated system trust (Bartlett and McCarley, 2017). In each case, the value of SDT lies not
in literal equivalence to sensory detection but in the
decomposition it provides.
We note that our multi-point ROC curves are constructed from NLP confidence bins at a fixed temperature, what Maniscalco and Lau (2014) would
term "pseudo type-1" ROC curves, built from confidence ratings rather than true criterion manipulations. Temperature variation across conditions does
provide something closer to a true criterion manipulation, but it serves as our independent variable
rather than the basis for ROC construction. This
is methodologically standard in recognition memory,
where multi-point ROCs are routinely constructed
from confidence ratings (Mickes et al., 2007).
Why NLP as the evidence variable? NLP captures the model’s internal probability assessment
of the generated sequence, normalised for answer
length. It is the natural analogue of the sensory
evidence on which human observers base their responses, the continuous variable underlying the binary correct/incorrect decision. Alternative evidence
variables exist (e.g., first-token logit, softmax probability). A pre-registered exploratory analysis comparing NLP with first-token logit evidence was specified
(Amendment 2) but is deferred to a companion analysis; we address the implications of this choice below
(§5.2). NLP was chosen because it integrates information across the full answer sequence rather than
relying on a single token position.

2.3

What SDT Adds Beyond ROC
Analysis

AUROC is widely computed in the LLM calibration
literature (Steyvers et al., 2025; Geng et al., 2024;
Liu et al., 2025; Shorinwa et al., 2025). The full SDT
framework adds four things:
First, independent criterion estimation. AUROC
collapses the ROC to a single number, discarding information about where on the ROC the model operates. The criterion parameter c captures where on
the ROC the model operates. Two models with identical AUROC can have very different criteria, and the
appropriate intervention differs accordingly.
Second, the unequal-variance model. Fitting the
UVSD model reveals whether signal and noise evidence distributions have different variances, a structural property of the model’s internal representations
that has no analogue in AUROC or ECE. The variance ratio s has direct theoretical interpretation: it
reflects how variably the model represents correct versus incorrect answers.
Third, specific, testable predictions. SDT generates precise predictions about how experimental manipulations should affect the ROC. The temperaturecriterion hypothesis predicts AUC invariance with
criterion shift, a prediction testable by equivalence
testing (TOST), not possible with AUROC alone.
Fourth, connection to 70 years of psychophysical
theory. The decomposition connects LLM evaluation to a mature theoretical framework with established methodology for diagnosing performance and
prescribing interventions.

2.4

Pre-Registered Hypotheses

H1 (Temperature-as-Criterion-Shift). For T ∈ 0.1,
0.3, 0.5, 0.7, 1.0, AUC remains constant (within
simulation-derived equivalence bounds) while c varies
monotonically with T.
H2 (Hidden Structure). Models with similar ECE
occupy different positions in (da , c) space.
H3 (Paradigm Convergence). da from confidencerating data converges with d′4AFC from forced choice
3

across domains.
H4 (Unequal Variance). z-ROC slope < 1.0, indicating σsignal > σnoise .
H5 (Domain-Specific Sensitivity). da varies across
knowledge domains.
H6 (High-Temperature Degradation). At T > 1.0,
da decreases due to generative-path divergence.

3

Method

3.1

Models

sensitivity). The relative ordering of conditions is unaffected: the same questions produce the same verbose answers at every temperature. The scoring robustness check across similarity thresholds 0.80, 0.85,
0.90 confirmed max |∆da | = 0.081.

3.4

Paradigm B: 4-Alternative Forced
Choice

For 2,000 TriviaQA questions, each model chose
among four options (correct answer plus three distractors selected by domain matching, token-length
matching, and embedding cosine similarity filtering).
Proportion correct was converted to d′4AFC via the
mAFC integral (Green and Dai, 1991).

Three models were evaluated: Llama-3-8B-Instruct
(Meta AI, 2024), Mistral-7B-Instruct-v0.3 (Jiang
et al., 2023), and Llama-3-8B-Base (no instruction
tuning). All were run as Q5_K_M quantisations via
3.5 Analysis A: Force-Decode
llama-cpp-python 0.3.16 with Vulkan backend on
an AMD RX 7900 GRE (16 GB VRAM). The two For each model at T = 1.0, we force-decoded both
instruct models served as primary comparisons; the the correct answer (maximum NLP across TriviaQA
base model provided an instruction-tuning contrast. aliases) and the model’s own incorrect generation,
yielding signal and noise NLP distributions from
which da was computed. Because force-decoding uses
3.2 Datasets
fixed token sequences with no sampling, this analysis is temperature-invariant and provides a baseTriviaQA (Joshi et al., 2017): 5,000 questions from
line sensitivity estimate independent of the critethe unfiltered set (seed = 42), classified into five dorion manipulation. A pre-registered robustness check
mains (History & Politics: 1,248; Arts & Literature:
(Amendment 1) replaced model-generated incorrect
1,167; Geography: 667; Science & Technology: 634;
answers with randomly sampled incorrect answers to
Unclassified: 1,284) using an LLM-based classifier
test whether the noise distribution was biased by the
(pre-registered fallback after Wikipedia API lookup
model’s generation tendencies.
failed; see Supplementary Materials, Deviation 1).
Natural Questions (Kwiatkowski et al., 2019):
3,000 short-answer questions from NQ-Open, provid- 3.6 SDT Analysis
ing a replication dataset.
ROC curves were constructed from 20 equal-width
NLP bins (edges from T = 1.0, held constant across
temperatures) with Hautus (1995) log-linear correc3.3 Paradigm A: Confidence-Rating
tion. UVSD models were fit by maximum likelihood
Each model generated an answer at each of seven (L-BFGS-B; z-ROC regression initialisation plus 10
temperatures: T ∈ 0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, perturbation restarts). AUC was computed by trapeyielding 168,000 trials. Each trial recorded the gen- zoidal integration. Bootstrap 95% CIs used 10,000
erated answer, NLP, softmax probability, and binary resamples per condition (≥99.95% convergence in all
correctness (exact match against verified aliases with 42 conditions). Equivalence bounds for H1 were dedifflib.SequenceMatcher ≥ 0.85 fallback, plus pream- rived from a pre-registered Monte Carlo simulation
ble stripping and refusal detection).
(10,000 iterations, 20 parameter combinations).
A human spot-check on a 5% subsample (1,200
A pre-registered robustness check repeated all analjudgments) yielded a false-match rate of 1.3% and a yses with quantile-based (equal-count) bins. Remissed-match rate of 30.1%. The high missed-match sults were stable for Llama-3-Base (mean |∆da | =
rate was driven by verbose generation (32%), alias 0.011) and Llama-3-Instruct (mean |∆da | = 0.064)
incompleteness (57%), and near-threshold similarity but showed substantial divergence for Mistral (mean
(11%), not by scoring logic errors. Because missed |∆da | = 0.453), attributable to bin sparsity at low
matches are correct answers scored as incorrect, they temperatures in the equal-width scheme. For Misdeflate hit rates uniformly across conditions, produc- tral, equal-width da estimates should be interpreted
ing conservative da estimates (lower bounds on true with caution; quantile estimates (da = 1.45–1.59) are
4

4.2

likely more reliable than equal-width estimates (da =
1.68–2.15). AUC, being non-parametric, was robust
across all models and binning schemes.

3.7

H2: SDT Reveals Hidden Structure

The pre-registered ECE similarity criterion (|∆ECE|
≤ 0.03) was not met (ECE range = 0.27), so H2
was tested under the pre-registered fallback: whether
ECE and the SDT operating point provide nonredundant information. At T = 1.0 on TriviaQA,
Llama-3-Instruct (da = 1.39, c = –2.40, ECE = 0.089)
and Mistral (da = 1.97, c = –2.69, ECE = 0.112) occupy distinct positions in SDT space: Mistral has
higher sensitivity but a more liberal criterion. ECE
alone would rank Llama-3 as better calibrated, but
SDT reveals that Mistral is the more capable discriminator operating under a more liberal policy. The
implied intervention differs: Mistral needs criterion
adjustment, not capability improvement.

Pre-Registration and Deviations

All hypotheses and analysis specifications were registered on OSF before data collection. Seven deviations
were documented: (1) domain classification fallback
method, (2) Llama-3-Base source repository, (3) NQ
dataset source, (4) MLE optimisation specification
change, (5) Paradigm B 4AFC implementation, (6)
NLL vectorisation, (7) scoring pipeline missed-match
rate. Full documentation is provided in Supplementary Materials.

4

Results

4.1

H1: Temperature Is Not a Pure The 4AFC paradigm produced near-ceiling performance for instruct models (Llama-3-Instruct: 97.5%
Criterion Shift

4.3

H3: Paradigm Convergence

correct, d′4AFC = 3.31; Mistral: 94.5%, d′4AFC = 2.85;
Base: 80.4%, d′4AFC = 1.91). Within-model domain
correlations between da and d′4AFC were positive but
non-significant: Llama-3-Instruct r = .84 (p = .08),
Mistral r = .82 (p = .09), Base r = .46 (p = .44),
all with N = 5 domains. The non-significance reflects
both low power and compression of d′4AFC variance
by ceiling performance: at 97.5% correct, d′4AFC is
in the steeply nonlinear portion of the psychometric function where small accuracy differences produce
large d′ changes, squashing between-domain variance.
The Bland-Altman plot revealed systematic bias: da
was consistently lower than d′4AFC (mean |∆| = 1.9 d′
units). H3 is not supported as specified. The positive
correlation direction and preserved domain ordering
across paradigms provide qualitative support for the
framework, but ceiling effects prevented a quantitative test.

The prediction that temperature shifts criterion without affecting sensitivity was not supported. AUC
increased monotonically with temperature in all six
conditions (Spearman ρ = 1.0 in four conditions, ρ ≥
0.964 in all six; all p < .001). The simulation-derived
equivalence bounds (max δ(AUC) = 0.016) were far
exceeded: AUC increased by 0.071 to 0.146 from T
= 0.1 to T = 2.0.
Simultaneously, criterion shifted as predicted: c increased monotonically with temperature (ρ = 1.0 in
five of six conditions), moving from strongly liberal
(c ≈ –2.88 at T = 0.1) toward less liberal (c ≈ –1.40
at T = 2.0).
The rejection of H1 is more informative than confirmation would have been. Temperature simultaneously changes both sensitivity and criterion. Crucially, this sensitivity increase reflects a distributional
effect of temperature on the evidence variable: higher
temperatures spread the NLP distribution, producing better separation between correct and incorrect
answer evidence. It does not indicate improved factual knowledge. Accuracy actually decreased with
temperature in all conditions, consistent with Renze’s
(2024) finding that temperature has no significant effect on accuracy in the moderate range (e.g., Llama3-Base TriviaQA: 59.2% at T = 0.1, 33.6% at T =
2.0). AUC is a property of the evidence distribution, not of the model’s epistemic competence. The
dissociation between AUC (increasing) and accuracy
(decreasing) illustrates exactly why the SDT decomposition is needed: aggregate accuracy conflates sensitivity with criterion placement.

4.4

H4: Unequal Variance

z-ROC slope was below 1.0 in all 42 conditions. At
T = 1.0 on TriviaQA: Llama-3-Instruct slope = 0.63
(s = 0.88); Mistral slope = 0.57 (s = 0.57); Llama-3Base slope = 0.78 (s = 1.17). The UVSD model was
preferred by AIC and BIC in all conditions.
The instruct models showed more extreme unequal
variance than the base model, and more extreme
than the modal value in human recognition memory
(s ≈ 0.80; Glanzer et al., 1999; Mickes et al., 2007;
Wixted, 2007). A discrepancy between the z-ROC
slope and the UVSD-fitted s for instruct models indicates some departure from Gaussianity. The base
5

Table 1: SDT parameters at selected temperatures (TriviaQA). Bootstrap 95% CIs from 10,000 resamples.
Model

T

AUC [95% CI]

da [95% CI]

c [95% CI]

Slope

Llama-3-Inst

0.1
0.5
1.0
1.5
2.0

.738 [.726, .750]
.748 [.735, .760]
.773 [.761, .785]
.795 [.783, .806]
.809 [.797, .820]

1.43 [1.32, 1.56]
1.37 [1.27, 1.48]
1.39 [1.31, 1.48]
1.45 [1.37, 1.53]
1.50 [1.42, 1.58]

−2.85 [−2.88, −2.80]
−2.64 [−2.73, −2.56]
−2.40 [−2.49, −2.32]
−2.19 [−2.28, −2.11]
−2.07 [−2.16, −1.99]

0.52
0.56
0.63
0.62
0.65

Mistral-7B-Inst

0.1
0.5
1.0
1.5
2.0

.620 [.610, .629]
.664 [.654, .674]
.713 [.702, .724]
.751 [.740, .762]
.764 [.753, .775]

1.86 [1.51, 4.55]†
2.03 [1.73, 2.57]
1.97 [1.74, 2.31]
2.10 [1.90, 2.38]
2.15 [1.95, 2.46]

−2.88 [−2.88, −2.88]
−2.85 [−2.88, −2.80]
−2.69 [−2.78, −2.61]
−2.67 [−2.76, −2.58]
−2.56 [−2.66, −2.46]

0.56
0.52
0.57
0.55
0.57

Llama-3-Base

0.1
0.5
1.0
1.5
2.0

.751 [.738, .764]
.797 [.785, .808]
.836 [.825, .846]
.850 [.839, .860]
.857 [.847, .867]

1.03 [0.97, 1.09]
1.24 [1.18, 1.30]
1.45 [1.38, 1.51]
1.51 [1.44, 1.58]
1.57 [1.50, 1.64]

−2.51 [−2.58, −2.46]
−2.23 [−2.27, −2.19]
−1.92 [−1.97, −1.86]
−1.62 [−1.70, −1.55]
−1.43 [−1.51, −1.37]

0.77
0.77
0.78
0.79
0.79

†

Wide CI due to bin sparsity at low T; quantile estimate preferred.

Figure 1: ROC curves for three models on TriviaQA across seven temperatures (T = 0.1–2.0). Warmer
colours indicate higher temperatures. Curves shift outward with increasing temperature, indicating increasing AUC.

6

Figure 2: Temperature effects on SDT parameters (TriviaQA). Left: AUC increases monotonically (ρ ≥
0.964). Centre: da trend. Right: Criterion c shifts monotonically from liberal toward less liberal. Shaded
bands: bootstrap 95% CIs.
property of NLP under temperature scaling, not a caTable 2: z-ROC slopes at T = 1.0 and slope × tempability improvement. Kempton et al. (2025) provide
perature correlations (E5). ∗ p < .01.
a formal account of how temperature distorts local
Model
Dataset Slope
s
E5 ρ
normalisation in autoregressive decoding, consistent
∗
with this pattern.
Llama-3-Inst
TQA
0.63
0.88 0.93
Mistral-7B-Inst
Llama-3-Base

NQ
TQA
NQ
TQA
NQ

0.58
0.57
0.54
0.78
0.84

0.75
0.57
0.68
1.17
1.38

0.89∗
0.32
−0.57
0.89∗
−0.71

4.7

E1: Instruction tuning as criterion shift. On TriviaQA at T = 1.0, Llama-3-Instruct and Llama-3-Base
had similar sensitivity (∆da = 0.055) but different
criteria (∆c = 0.480), consistent with instruction tuning primarily adjusting response policy rather than
discriminative capacity.
E2: Prompt criterion manipulation. Liberal and
conservative system prompts did not produce graded
criterion shifts. The conservative prompt induced
modest refusal (10.6% for Llama-3-Instruct, 8.0% for
Mistral) alongside small criterion shifts (∆c = –0.01
to –0.11), but also reduced sensitivity (∆da = –0.11
to –0.25), suggesting the prompt disrupted processing
rather than cleanly shifting criterion.
E5: z-ROC slope × temperature. z-ROC slope increased significantly with temperature for Llama-3Instruct (ρ = 0.93, p = .003) and Llama-3-Base (ρ
= 0.89, p = .007) on TriviaQA, but not for Mistral
(ρ = 0.32, p = .48). Temperature changes the shape
of evidence distributions, not just their location, and
this effect is model-specific.

model showed closer convergence, suggesting more
Gaussian-like evidence distributions without instruction tuning.

4.5

H5: Domain-Specific Sensitivity

da varied across TriviaQA domains at T = 1.0. Science & Technology was consistently the hardest domain (Llama-3-Instruct: da = 1.07; Mistral: 1.43;
Base: 1.33). Mistral showed the widest range (1.43–
2.34). This domain-specific information is invisible
to aggregate ECE.

4.6

Exploratory Analyses

H6: High-Temperature Sensitivity

Contrary to predictions, da did not decrease at T >
1.0. In five of six conditions, da at T = 2.0 exceeded
da at T = 1.0. For Llama-3-Base on TriviaQA, non- 4.8 Robustness
overlapping bootstrap CIs confirmed the increase: da
= 1.03 [0.97, 1.09] at T = 0.1 versus 1.57 [1.50, 1.64] Scoring threshold robustness: max |∆da | = 0.081,
at T = 2.0. As with H1, this reflects a distributional max |∆AUC| = 0.007 across 0.80, 0.85, 0.90.
7

Figure 3: SDT operating points at T = 1.0. Position: (da , c); fill: ECE. Edge colour: model identity. Circles:
TriviaQA; squares: NQ. Models occupy distinct positions invisible to ECE alone.

8

Figure 4: Bland-Altman plot: da (Paradigm A, T = 1.0) versus d′4AFC (Paradigm B) across domains.
Systematic negative bias reflects near-ceiling 4AFC inflating d′4AFC .

9

Figure 5: z-ROC plots (TriviaQA, all temperatures overlaid). Black line: T = 1.0 regression. Slopes < 1.0
confirm unequal variance. Instruct models: 0.52–0.63; base model: 0.78.

Figure 6: Domain-specific da at T = 1.0 (TriviaQA). Science & Technology is consistently hardest. Mistral
shows widest range (1.43–2.34).

10

Figure 7: z-ROC slope as a function of temperature. Slope increases significantly with T for Llama-3 models
(ρ ≥ 0.89, p < .01) but not Mistral, indicating model-specific changes in evidence distribution shape.

Figure 8: NQ replication: AUC and da versus temperature. All primary patterns replicate on Natural
Questions.

11

Quantile-bin robustness: stable for Llama-3 models,
unstable for Mistral (see §3.6). NQ replication: all
primary patterns (AUC increasing with T, criterion
shift, unequal variance) replicated on Natural Questions. Evidence variable robustness: a pre-registered
analysis comparing first-token logit with sequence
NLP as the evidence variable (Amendment 2) was
deferred; we address the implications of the NLP fluency confound in §5.2.

5

Discussion

5.1

Three Core Contributions

The present study establishes three findings through
the application of formal parametric SDT to LLMs
as signal detectors.
First, temperature is not a pure criterion manipulation. The payoff analogy from human psychophysics
breaks down because temperature changes the generated answer, not only the confidence assigned to it.
In human experiments, the stimulus is constant regardless of criterion setting. In LLMs, the evidence
variable (NLP of the generated answer) is not independent of the criterion manipulation (temperature)
because the answer mediates both. This is a structural disanalogy, not a methodological limitation, and
it characterises the boundary of the temperature-ascriterion-shift metaphor.
Importantly, the sensitivity increase observed with
temperature is a distributional effect on the evidence
variable, not evidence of improved factual competence. Accuracy declined with temperature in all conditions. What increased was the separation of NLP
distributions for correct versus incorrect answers, a
property of how temperature affects the mapping
from logits to probabilities, not a change in what the
model knows. This dissociation between AUC (increasing) and accuracy (decreasing) is precisely the
kind of structure that the SDT decomposition is designed to reveal.
Second, LLMs exhibit unequal-variance evidence
distributions. The z-ROC slopes of 0.52–0.84 consistently indicate that correct-answer evidence has
greater variance than incorrect-answer evidence. In
human recognition memory, this is explained by
encoding variability (Ratcliff et al., 1992; Wixted,
2007): well-remembered items produce high, variable evidence, while unstudied items are more uniform. The LLM analogue is natural: some correct
answers are deeply represented in the model’s parameters (high NLP) while others are at the edge of the
model’s knowledge (low NLP, uncertain). Incorrect
12

answers, being the model’s best guess, cluster at intermediate NLP values.
The instruct models showed more extreme unequal variance (slopes 0.52–0.63) than the base model
(0.77–0.87) and than is typically found in human
recognition memory (s ≈ 0.80).
This "hyperunequal" variance may reflect instruction tuning amplifying the distinction between well-known and edgeof-knowledge items, plausibly because RLHF training
teaches the model to express confidence more variably
for correct answers.
Third, the SDT decomposition provides information unavailable from calibration metrics. The H2
and H5 results demonstrate that ECE does not distinguish between models that differ in sensitivity versus criterion, nor between domains that differ in discriminability. The E1 result is particularly instructive. Instruction tuning primarily shifts criterion
with minimal sensitivity change, a pattern invisible
to ECE and directly actionable: it means that if an
instruction-tuned model’s responses are too liberal,
the fix is criterion adjustment (e.g., temperature tuning), not retraining.

5.2

The Fluency–Accuracy Dissociation

The force-decode analysis (Analysis A) produced
a theoretically informative negative result. Forcedecoded correct answers had lower NLP than modelgenerated incorrect answers in most conditions (da ≈
0), yet random incorrect answers (from Amendment
1) produced da of 1.7–3.4 against the same correct
answers. The model has a genuine truth signal, but
it is masked by the high fluency of model-generated
errors. The model generates what it finds probable,
and its confident incorrect answers are more fluent
than externally-sourced correct answers phrased differently from how the model would naturally generate
them.
This fluency–accuracy dissociation has direct implications for the primary analyses. Because NLP
conflates correctness with fluency, the da estimates
from Paradigm A should be understood as reflecting
the model’s ability to discriminate correct from incorrect answers as indexed by their fluency-weighted
probability, not by a pure truth signal. The forcedecode analysis provides partial validation: when the
fluency advantage of self-generated errors is removed
(Amendment 1, random noise), da rises to 1.7–3.4,
confirming that the models do encode a genuine correctness signal that NLP partially captures. The preregistered first-token logit analysis (Amendment 2),
which would construct ROCs from a single-token ev-

idence variable less confounded by fluency, was not
completed in the present study and represents an
important next step for isolating the truth-tracking
component. Despite this limitation, the relative ordering of conditions is unaffected by the fluency confound — the same fluency bias applies at every temperature and across all models — so the comparative
conclusions (H1 rejection, H2 structure, H4 unequal
variance, H5 domain differences) remain valid even if
absolute da values are conservative.

5.3

Connections
SDT

to

Metacognitive

Steyvers and Peters (2025) frame LLM confidence
evaluation through metacognitive SDT, using AUROC and meta-d′ (Maniscalco and Lau, 2012) to
quantify metacognitive sensitivity. Our work complements theirs by moving from descriptive metrics to
the full parametric model. The UVSD model fitting,
criterion estimation, and z-ROC analysis we report
go beyond what AUROC or meta-d′ capture: they
reveal the variance structure of the evidence distributions, the location of the decision threshold, and
how both change under experimental manipulation.
A natural extension would be to compute metad′ from our data and compare it with da from the
UVSD fit. If meta-d′ < da , the model’s metacognitive sensitivity falls short of what the type-1 evidence
supports, indicating metacognitive inefficiency. This
connection between parametric SDT and metacognitive SDT was not pre-registered but represents a productive direction for integrating these two approaches
to LLM confidence evaluation.

5.4

Practical Implications

The decomposition has direct practical value. When
a model performs poorly on a domain, ECE does not
distinguish "can’t discriminate" (low da ) from "discriminates but responds poorly" (wrong c). Our H5
results show Science & Technology consistently has
the lowest da . This domain needs better training,
not recalibration.
The decomposition extends naturally to selective
prediction (Geifman and El-Yaniv, 2017). An abstention threshold is a criterion placement. Given da
for a specific domain, SDT prescribes the optimal criterion for any desired operating point on the ROC.
Current selective prediction methods set thresholds
empirically without reference to the underlying sensitivity.
13

5.5

Limitations

Several limitations constrain interpretation. Only
two model families (Llama-3-8B and Mistral-7B)
were tested, both at 7–8B parameters with Q5_K_M
quantisation. Whether findings generalise to larger
models, different architectures, or full-precision inference is unknown.
The scoring pipeline’s 30.1% missed-match rate,
though producing only conservative bias (underestimating sensitivity uniformly across conditions),
means that absolute da values should not be compared directly with other benchmarks. Relative comparisons within our study remain valid.
The 4AFC paradigm produced near-ceiling performance for instruct models (97.5% correct), limiting
d′4AFC precision and preventing a clean paradigm convergence test. Future work should use more difficult distractors to bring performance into the 70–85%
range where d′ estimation is most precise.
The Mistral da estimates were sensitive to the binning scheme, with equal-width bins inflating da due
to bin sparsity at low temperatures. We report equalwidth results as the pre-registered primary analysis
but note that quantile estimates are preferred for Mistral.
The NLP evidence variable conflates correctness
with fluency (§5.2). The pre-registered first-token
logit comparison (Amendment 2) would partially address this concern but was not completed. The forcedecode analysis provides indirect validation that a
genuine correctness signal underlies the NLP-based
estimates, but a direct comparison of evidence variables remains an important gap. Finally, the evidence
distributions show some departure from Gaussianity
(z-ROC slope vs. UVSD s discrepancy), particularly
for instruct models. This is a known limitation of
parametric SDT. The z-ROC linearity test provides a
direct diagnostic, and non-parametric AUC provides
a robust alternative that requires no distributional
assumptions.

5.6

Future Directions

Several extensions are immediate. The first-token
logit analysis (Amendment 2) is the most pressing:
if ROCs constructed from first-token logits produce
converging da estimates (within the pre-registered
±0.3 bound), this validates the NLP-based results; if
they diverge, it would indicate that fluency contamination materially distorts the SDT decomposition.
The raw data for this analysis are already collected.
Continuous MLE fitting without binning would eliminate bin-sparsity issues. Hierarchical Bayesian SDT
models could estimate parameters across conditions

simultaneously. Application to larger models and
proprietary APIs would test generality. The z-ROC
slope × temperature interaction (E5) warrants mechanistic investigation through analysis of internal representations. And the connection to meta-d′ (§5.3)
would formally bridge parametric and metacognitive
SDT approaches to LLM evaluation.
More broadly, this work demonstrates that classical
psychophysical methods provide genuinely new diagnostic information about AI systems, consistent with
the growing programme of applying psychophysics to
AI (Hernández-Cámara et al., 2025). The unequalvariance finding, the domain-specific sensitivity profiles, and the instruction-tuning-as-criterion-shift result are all invisible to standard calibration metrics.
As LLMs are deployed in high-stakes domains, the
distinction between "can’t discriminate" and "discriminates but responds poorly" becomes practically
critical. SDT provides the principled framework for
making this distinction.

References
M. L. Bartlett and J. S. McCarley. Benchmarking
aided decision making in a signal detection framework. Human Factors, 59(6):881–900, 2017.
Y. Geifman and R. El-Yaniv. Selective classification
for deep neural networks. In Advances in Neural
Information Processing Systems, 2017.
J. Geng, F. Cai, Y. Wang, H. Kober, Y. Bisk, and
G. Neubig. A survey of confidence estimation and
calibration in large language models. In Proceedings of NAACL, 2024.
D. M. Green and H. Dai. Probability of being correct with 1 of M orthogonal signals. Perception &
Psychophysics, 49:100–101, 1991.
D. M. Green and J. A. Swets. Signal Detection Theory
and Psychophysics. Wiley, 1966.
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger. On
calibration of modern neural networks. In Proceedings of ICML, 2017.

Declarations

Funding The author received no funding for this
research. No funds, grants, or other support were M. J. Hautus. Corrections for extreme proportions
received during the preparation of this manuscript.
and their biasing effects on estimated values of d′ .
Behavior Research Methods, 27(1):46–51, 1995.
Competing Interests The author has no relevant
P. Hernández-Cámara et al.
Contrast sensitivfinancial or non-financial interests to disclose.
ity in multimodal large language models: A
psychophysics-inspired evaluation. arXiv preprint
Ethics Approval Not applicable. This study
arXiv:2508.10367, 2025.
involved computational experiments with publicly
available language models and datasets. No human
A. Q. Jiang et al. Mistral 7B. arXiv preprint
participants were involved.
arXiv:2310.06825, 2023.
Data
and
Code
Availability All data, M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer.
analysis code, and raw results are available
TriviaQA: A large scale distantly supervised chalat
https://anonymous.4open.science/r/sdt_
lenge dataset for reading comprehension. In Procalibration-3662/README.md. The study was preceedings of ACL, 2017.
registered at https://osf.io/qpk9a/overview?
S. Kadavath et al. Language models (mostly) know
view_only=28f2894d9fcf4679a8afd2b7d70f6f0b.
what they know. arXiv preprint arXiv:2207.05221,
2022.
Author Contributions JP Cacioli designed the
study, conducted all data collection, performed all
T. Kempton et al. Local normalisation distortion and
analyses, and wrote the manuscript.
the thermodynamic formalism of decoding strategies for large language models. arXiv preprint
Use of Generative AI During the preparation of
arXiv:2503.21929, 2025.
this work, the author used Claude (Anthropic) as
a research assistant for code generation, statistical L. Kuhn, Y. Gal, and S. Farquhar. Semantic unceranalysis scripting, and figure generation. All scientainty: Linguistic invariances for uncertainty estitific decisions, hypothesis formulation, and interpremation in natural language generation. In Proceedtive judgments were made by the author.
ings of ICLR, 2023.
14

T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, M. Steyvers, H. Tejeda, A. Kumar, C. Belem,
A. Parikh, C. Alberti, D. Epstein, I. Polosukhin,
S. Karny, X. Hu, L. W. Mayer, and P. Smyth. What
J. Devlin, K. Lee, et al. Natural questions: A
large language models know and what people think
benchmark for question answering research. Transthey know. Nature Machine Intelligence, 7(2):221–
actions of the Association for Computational Lin231, 2025.
guistics, 7:453–466, 2019.
J. A. Swets. Signal Detection Theory and ROC AnalX. Liu, T. Chen, L. Da, C. Chen, Z. Lin, and H. Wei.
ysis in Psychology and Diagnostics. Lawrence ErlUncertainty quantification and confidence calibrabaum, 1996.
tion in large language models: A survey. In ProK. Tian et al. Just ask for calibration: Strategies
ceedings of KDD, 2025. arXiv:2503.15850.
for eliciting calibrated confidence scores from lanN. A. Macmillan and C. D. Creelman. Detection Theguage models fine-tuned with human feedback. In
ory: A User’s Guide. Lawrence Erlbaum, 2nd ediProceedings of EMNLP, 2023.
tion, 2005.
J. T. Wixted. Dual-process theory and signalB. Maniscalco and H. Lau. A signal detection theodetection theory of recognition memory. Psychoretic approach for estimating metacognitive sensilogical Review, 114:152–176, 2007.
tivity from confidence ratings. Consciousness and
J. T. Wixted and L. Mickes. A signal-detectionCognition, 21:422–430, 2012.
based diagnostic-feature-detection model of eyewitB. Maniscalco and H. Lau. Signal detection theness identification. Psychological Review, 121:262–
ory analysis of type 1 and type 2 data: Meta-d′ ,
276, 2014.
response-specific meta-d′ , and the unequal variance
SDT model. In S. M. Fleming and C. D. Frith, editors, The Cognitive Neuroscience of Metacognition,
pages 25–66. Springer, 2014.
Meta AI. Llama 3 model card. https://github.
com/meta-llama/llama3, 2024.
L. Mickes, J. T. Wixted, and P. E. Wais. A direct
test of the unequal-variance signal detection model
of recognition memory. Psychonomic Bulletin &
Review, 14:858–865, 2007.
R. Ratcliff, C.-F. Sheu, and S. Gronlund. Testing
global memory models using ROC curves. Psychological Review, 99:518–535, 1992.
M. Renze. The effect of sampling temperature on
problem solving in large language models. In Findings of EMNLP, 2024.
Q. Shen et al. Thermometer: Towards universal calibration for large language models. arXiv preprint
arXiv:2403.08819, 2024.
O. Shorinwa, Z. Mei, J. Lidard, A. Z. Ren, and A. Majumdar. A survey on uncertainty quantification of
large language models: Taxonomy, open research
challenges, and future directions. ACM Computing
Surveys, 2025. arXiv:2412.05563.
M. Steyvers and M. A. K. Peters. Metacognition and uncertainty communication in humans
and large language models. Current Directions
in Psychological Science, 2025. doi: 10.1177/
09637214251391158.
15

