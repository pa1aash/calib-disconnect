---
title: '[2607.04430 Full Text/PDF] Uncertainty-Aware Abstention in Large Language
  Models with Provable Alignment Guarantees'
id: 260704430-cic-full-text-uncertainty-aware-abstention
tags:
- code-llm-calibration-aaai27-eabf3f
- locus-fallback-utility-of-collapsed-confidence
- conformal-abstention
- selective-generation
created: '2026-07-17T19:02:26.235657Z'
source: https://arxiv.org/pdf/2607.04430
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Full-text PDF extraction of the CIC paper (companion to the abstract-only
  stub). Contains exact risk-coverage tables: 7 LLMs x {CommonsenseQA, TriviaQA} x
  alpha in {0.05..0.25} x {UCB-HFD, UCB-CP}, using semantic entropy (10 samples) as
  the sole uncertainty estimator despite abstract''s ''multiple estimators'' framing.
  At alpha=0.10 with UCB-CP, coverage/power ranges 0.52-1.00 (TriviaQA) and 0.61-0.87
  (CommonsenseQA); alpha=0.05 is frequently UNATTAINABLE (Fail=34-100/100 splits)
  for weaker models (Vicuna-7B/13B, Qwen2.5-3B). Calibration set SIZE (absolute N)
  is never reported, only a 1:1 default split ratio with 100-trial mean+-std, shown
  robust down to a 1:9 ratio. No code-generation benchmark is tested -- purely general
  QA (CommonsenseQA, TriviaQA).'
---

*Suggested by [[260704430-uncertainty-aware-abstention-in-large-language-models-with-provable-al]] — Full-text follow-up fetch of the PDF; the original note only captured the arXiv abstract page. This note extracts the concrete risk-coverage result tables.*

## Structured Claims Extraction (full-text, PDF-sourced)

**Paper**: Sijin Dong, Hiroyuki Shinnou (Ibaraki University). "Uncertainty-Aware Abstention in Large Language Models with Provable Alignment Guarantees" (CIC framework). arXiv:2607.04430, submitted 5 Jul 2026.

**Method summary**: CIC (Confidence-Interval-based Calibration) is a post-hoc wrapper: given ANY uncertainty score `U`, on a held-out calibration set it computes, for each candidate threshold `t`, an upper confidence bound (Hoeffding-style `UCB-HFD` or Clopper-Pearson `UCB-CP`) on the acceptance-conditioned error rate `R(t) = P(E=1 | U<=t)`, then selects the LARGEST threshold whose UCB stays below the user's risk level `alpha`, maximizing answering rate under the finite-sample constraint. If no threshold is feasible, it returns NULL ("risk level unattainable") — a real, non-trivial failure mode reported empirically.

**Benchmarks tested — general QA only, NO code-generation task**:
- CommonsenseQA (closed-ended, multiple-choice commonsense reasoning; correctness = exact match to ground-truth option)
- TriviaQA (open-ended free-form QA; correctness = sentence-similarity >= 0.6 threshold to reference answer, following prior work)
- The paper explicitly frames its contribution as a "practical and statistically grounded mechanism for deploying LLMs in reliability-sensitive QA workflows" — no mention of code, SWE, or program-synthesis benchmarks anywhere in the text.

**7 LLMs tested**: Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct, OpenChat-3.5, Vicuna-7B-v1.5, Vicuna-13B-v1.5, LLaMA-3.1-8B-Instruct.

**Uncertainty estimator**: semantic entropy (Kuhn et al. 2023) is the ONLY estimator used in the main result tables (10 sampled responses per question). The abstract's claim of "multiple uncertainty estimators" is not reflected in Tables 1-4 — those all use semantic entropy only; no ablation with alternative estimators (e.g., SAR, WSE mentioned in related work) appears in the extracted tables.

**Calibration protocol / calibration-set size**: NOT reported as an absolute N. The paper only specifies a calibration:test SPLIT RATIO, default 1:1 (50%/50%), repeated over 100 random splits with mean±std reported (delta/confidence level for the split-repeat is not separately stated as a fixed delta value in the main results — only alpha in {0.05,0.10,0.15,0.20,0.25} is swept). A sensitivity study (Fig. 2, CommonsenseQA + Qwen2.5-3B-Instruct only) varies the split ratio across 1:1, 2:3, 3:7, 1:4, 1:9 (calibration proportions 0.5/0.4/0.3/0.2/0.1) and finds the empirical alignment proportion stays in [0.9190, 0.9290] against a target of 0.90 — i.e. CIC is robust down to a 10% calibration fraction, but the ABSOLUTE dataset sizes of CommonsenseQA/TriviaQA splits used are never stated in the extracted text (no N given, e.g. "N=1221 calibration examples").

**Exact risk-coverage numbers (Table 1, CommonsenseQA, test-time FDR, mean over 100 splits; "Fail" = number of the 100 splits where no feasible threshold was found, i.e., abstention was forced to 100%/coverage 0)**:

| Model (Base Error Rate) | UCB | alpha=0.05: FDR / Fail | alpha=0.10: FDR / Fail |
|---|---|---|---|
| Qwen2.5-3B-Instruct (0.239) | HFD | — / 100 | 0.128 / 0 |
| Qwen2.5-3B-Instruct | CP | 0.040 / 34 | 0.090 / 0 |
| Qwen2.5-7B-Instruct (0.212) | HFD | 0.024 / 89 | 0.079 / 0 |
| Qwen2.5-7B-Instruct | CP | 0.043 / 0 | 0.092 / 0 |
| OpenChat-3.5 (0.182) | HFD | 0.023 / 7 | 0.079 / 0 |
| OpenChat-3.5 | CP | 0.043 / 0 | 0.092 / 0 |
| Vicuna-7b-v1.5 (0.410) | HFD | — / 100 | — / 100 |
| Vicuna-7b-v1.5 | CP | — / 100 | 0.080 / 66 |
| LLaMA-3.1-8B-Instruct (0.271) | HFD | — / 100 | 0.074 / 0 |
| LLaMA-3.1-8B-Instruct | CP | 0.041 / 0 | 0.090 / 0 |
| Vicuna-13b-v1.5 (0.347) | HFD | — / 100 | — / 100 |
| Vicuna-13b-v1.5 | CP | 0.055 / 86 | 0.071 / 0 |
| Qwen2.5-14B-Instruct (0.168) | HFD | 0.023 / 19 | 0.080 / 0 |
| Qwen2.5-14B-Instruct | CP | 0.044 / 0 | 0.092 / 0 |

**Corresponding coverage/answering-power (Table 4, CommonsenseQA, mean power = fraction of test samples accepted)**:

| Model | UCB | alpha=0.05 Power | alpha=0.10 Power |
|---|---|---|---|
| Qwen2.5-3B-Instruct | HFD | — (infeasible) | 0.502 |
| Qwen2.5-3B-Instruct | CP | 0.176 | 0.623 |
| Qwen2.5-7B-Instruct | HFD | 0.345 | 0.720 |
| Qwen2.5-7B-Instruct | CP | 0.572 | 0.766 |
| OpenChat-3.5 | HFD | 0.488 | 0.802 |
| OpenChat-3.5 | CP | 0.655 | 0.839 |
| LLaMA-3.1-8B-Instruct | HFD | — (infeasible) | 0.551 |
| LLaMA-3.1-8B-Instruct | CP | 0.391 | 0.608 |
| Vicuna-13b-v1.5 | HFD | — (infeasible) | — (infeasible) |
| Vicuna-13b-v1.5 | CP | 0.041 | 0.132 |
| Qwen2.5-14B-Instruct | HFD | 0.446 | 0.833 |
| Qwen2.5-14B-Instruct | CP | 0.661 | 0.865 |

**TriviaQA (Table 2 FDR / Table 3 Power, same alpha grid), best- and worst-case highlights**:
- Best (Qwen2.5-14B-Instruct, UCB-CP): alpha=0.05 -> FDR=0.040, Fail=0, Power=0.621; alpha=0.10 -> FDR=0.088, Fail=0, Power=0.999.
- Worst usable (Vicuna-7b-v1.5, UCB-CP): alpha=0.05 -> FDR=0.057 but Fail=99/100 splits (i.e., ~99% of the time no threshold is certifiable at all — essentially non-functional at this alpha); alpha=0.10 -> FDR=0.086, Fail=0, Power=0.567.
- Qwen2.5-3B-Instruct (weaker/smaller model), UCB-CP: alpha=0.05 -> FDR=0.038, Fail=34 (i.e., fails on 34% of splits); alpha=0.10 -> FDR=0.086, Fail=0, Power=0.517.

**Headline takeaway for a fallback-utility comparison**: at the standard alpha=0.10 (10% risk) with the exact/Clopper-Pearson bound (UCB-CP, generally the safer choice for small accepted subsets), CIC achieves ~0% "Fail" rate for most of the 7 models and delivers coverage/answering-power in the range **0.52–1.00 on TriviaQA and 0.61–0.87 on CommonsenseQA**, while keeping realized FDR close to but under 0.10 (e.g., 0.086–0.092). At the stricter alpha=0.05, several models (Vicuna-7B, Vicuna-13B, Qwen2.5-3B) either fail outright (Fail=100) or fail on a large fraction of splits (34-99%), showing alpha=0.05 is often UNATTAINABLE for weaker models/estimators — this is the paper's own stated finding, not a caveat added here. For a fallback target this suggests alpha~0.10-0.15 (not 0.05) is the realistic operating point for comparable single-signal semantic-entropy-style calibration.

**No calibration-set-size ablation with hard numbers** beyond the ratio-based robustness study; no code-generation results; only semantic entropy is evaluated end-to-end despite the abstract's "multiple uncertainty estimators" framing.

---

## Full Extracted Text (PDF, pdfplumber)

--- PAGE 1 ---
Uncertainty-Aware Abstention in Large Language
Models with Provable Alignment Guarantees
Sijin Dong1* and Hiroyuki Shinnou1
1Ibaraki University, Japan.
*Corresponding author(s). E-mail(s): dong8529278@gmail.com;
Abstract
Largelanguagemodels(LLMs)areincreasinglyusedinquestionanswering(QA)
systems,buttheycanstillproducehallucinatedormisalignedresponseswithout
reliable confidence estimates. Uncertainty quantification (UQ) enables selective
answering, where a system responds only when its prediction appears reliable
and abstains otherwise. However, uncertainty scores alone are often heuristic,
and thresholding them does not provide statistical guarantees on the error rate
among accepted answers. We propose CIC, a confidence-interval-based calibra-
tion framework that converts arbitrary uncertainty scores into risk-controlled
selective answering rules. Using a held-out calibration set, CIC assigns each
generated response an uncertainty score and a binary error label based on an
application-specific alignment criterion. For each candidate threshold, CIC esti-
mates the error rate among accepted answers and constructs a high-probability
upper confidence bound using Hoeffding-style or Clopper–Pearson intervals. It
then selects the threshold with the highest answering rate whose upper bound
remains below a user-specified risk level α. Under exchangeability, CIC guaran-
teeswithprobabilityatleast1−δ thattheselectednon-nullthresholdcontrols
theaccepted-answererrorrateatlevelα.Experimentsonclosed-endedandopen-
ended QA benchmarks across seven LLMs and multiple uncertainty estimators
showthatCICachievesvalidriskcontrolwhilemaintainingstrongansweringeffi-
ciency.TheseresultsdemonstratethatCICprovidesapracticalandstatistically
grounded mechanism for reliable LLM deployment in QA workflows.
Keywords:largelanguagemodels,questionanswering,selectiveanswering,
uncertaintyquantification,upperconfidencebound
1
6202
luJ
5
]LC.sc[
1v03440.7062:viXra
--- PAGE 2 ---
1 Introduction
Largelanguagemodels(LLMs)haveachievedremarkableprogressinnaturallanguage
understandingandgeneration[1,2],andareincreasinglydeployedasquestionanswer-
ing(QA)systems,conversationalassistants[3],anddecision-supporttools[4].Despite
theirstrongempiricalperformance,LLMscanstillgeneratehallucinated,unsupported,
or semantically misaligned responses [5–10]. This issue is particularly problematic in
reliability-sensitiveapplications,whereanincorrectanswermaybemoreharmfulthan
no answer at all. Therefore, beyond improving the average accuracy of LLMs, it is
crucialtodevelopprincipledmechanismsthatdeterminewhenamodeloutputshould
be trusted and when the system should abstain [8, 11–17].
Uncertainty quantification (UQ) provides a natural route toward this goal [18].
Given a query and a generated response, an uncertainty estimator assigns a score
intended to reflect the reliability of the output. Such scores can be used for selec-
tive answering: the system accepts a response when its uncertainty is sufficiently low
and abstains otherwise. A wide range of uncertainty signals have been proposed for
LLMs, including entropy-based scores, sampling-based disagreement measures, and
semantic-consistency metrics [19–22]. However, these scores are often heuristic. They
may correlate with correctness on average, but they do not perfectly separate correct
from incorrect answers. As a result, choosing an uncertainty threshold by intuition
or empirical accuracy alone does not provide a statistical guarantee on the error rate
among the answers that the system actually returns [23–25].
This limitation motivates the central question of this work: given an arbitrary
uncertainty score for an LLM output, can we calibrate a test-time answering rule
that accepts as many responses as possible while provably controlling the risk among
accepted answers? This question differs from standard accuracy evaluation, which
measures model performance over all test samples, regardless of whether the system
chooses to answer. It also differs from classical split conformal prediction [26–28],
which typically constructs prediction sets with coverage guarantees. In many QA
deployments, however, the system is expected to return a single answer when con-
fident and abstain otherwise [23]. The relevant reliability target is therefore not set
coverage [22, 29–31], but the error rate conditioned on acceptance.
In this paper, we propose CIC, a confidence-interval-based calibration framework
forrisk-controlledselectiveansweringwithLLMs.WeconsiderafrozenLLMequipped
with any user-chosen uncertainty estimator. On a held-out calibration set, each gen-
erated response is evaluated by an application-specific alignment criterion, producing
a binary label that indicates whether the response is aligned with the ground truth.
CIC then links the uncertainty score of each response to its empirical correctness and
learns an uncertainty threshold for deployment. Figure 1 provides an overview of the
proposed calibration and selective deployment pipeline.
The key idea is simple: for any candidate threshold, the system accepts calibra-
tion examples whose uncertainty scores fall below the threshold, and estimates the
errorrateamongtheseacceptedexamples.Sincethisempiricalerrorrateiscomputed
from finite calibration data, directly using it may lead to unreliable threshold choices.
CICthereforeconstructsahigh-probabilityupperconfidenceboundonthethreshold-
conditioned error rate, using either a Hoeffding-style confidence bound or an exact
2
--- PAGE 3 ---
Fig. 1 OverviewoftheCICframeworkforrisk-controlledselectiveanswering.CICusesaheld-out
calibrationsettoassociateeachLLMresponsewithanuncertaintyscoreandanalignmentlabel.It
thenscanscandidateuncertaintythresholds,computesanupperconfidenceboundontheerrorrate
amongacceptedresponses,andselectsthelargestthresholdsatisfyingthetargetrisklevelα.During
deployment,thecalibratedthresholdactsasanuncertaintygate:responsesbelowthethresholdare
accepted, while high-uncertainty responses are abstained from, yielding finite-sample risk control
underexchangeability.
Clopper–Pearson confidence interval [32]. The final threshold is chosen as the largest
candidate threshold whose upper confidence bound does not exceed a user-specified
risklevelα.Thischoicemaximizestheansweringrateamongcertifiedthresholdswhile
maintaining a finite-sample safety constraint.
At deployment time, the calibrated threshold acts as an uncertainty gate. For a
new query, the LLM generates an answer and the uncertainty estimator computes its
score.Thesystemreturnstheansweronlyifthescoreisbelowthecalibratedthreshold;
otherwise, it abstains. Under an exchangeability assumption between calibration and
deployment data, CIC guarantees that, with probability at least 1−δ, the selected
threshold,ifnon-null,controlstheacceptance-conditionederrorrateatthetargetlevel
α. In the one-answer-per-query setting, this quantity is equivalent to the marginal
false discovery rate of the selective answering policy.
We evaluate CIC on both closed-ended and open-ended QA benchmarks across
multiple LLMs and uncertainty estimators. The experimental results show that
CIC consistently controls the error rate among accepted answers across a range of
user-specified risk levels, while preserving strong answering efficiency. These results
demonstrate that confidence-interval calibration can serve as a practical statistical
layer on top of heuristic LLM uncertainty scores, enabling more reliable deployment
of LLM-based QA systems.
Our main contributions are summarized as follows:
• We formulate risk-controlled selective answering for LLM-based QA as the prob-
lem of controlling the acceptance-conditioned error rate under an uncertainty-
thresholding policy.
• We propose CIC, a confidence-interval-based calibration framework that converts
arbitrary uncertainty scores into statistically certified abstention rules.
3
--- PAGE 4 ---
• We establish finite-sample, high-probability guarantees for the calibrated thresh-
old under exchangeability, with both Hoeffding-style and Clopper–Pearson upper
confidence bounds.
• WeempiricallyvalidateCIConclosed-endedandopen-endedQAbenchmarksacross
multiple LLMs, showing reliable risk control with strong answering efficiency.
2 Related Work
Uncertainty Quantification.
Uncertaintyquantification(UQ)aimstoassessthereliabilityofmodelpredictionsand
provideuserswithsignalsindicatingwhenamodeloutputislikelytobeincorrect[18].
For LLM-based generation, recent studies have developed various uncertainty estima-
tors, including semantic entropy (SE) [20], shift attention to relevance (SAR) [19],
andword-sequenceentropy(WSE)[21].Thesemethodsprovideusefulrankingsignals
for identifying unreliable responses and can be naturally used for selective answer-
ing. However, LLM uncertainty estimates remain largely heuristic: hallucinated or
unsupported responses may still be produced with high confidence, leading to low
uncertainty despite being incorrect [24, 25]. Therefore, directly thresholding such
scores does not provide a statistical guarantee on the error rate among accepted
answers. In contrast, our work treats UQ scores as black-box reliability signals and
calibrates them into risk-controlled decision rules with finite-sample guarantees.
Split Conformal Prediction.
Split conformal prediction (SCP) provides distribution-free and model-agnostic cov-
erage guarantees by calibrating nonconformity scores on a held-out calibration
set [27, 28]. It has been widely used to construct prediction sets that contain the
ground-truth label with user-specified probability, including applications to classifica-
tion[26]andsegmentation[33].RecentworkhasextendedconformalmethodstoLLMs
and natural language processing [34], including admission coverage [22, 29, 30, 35],
conformal factuality [36], and conformal alignment [23]. These approaches mainly
focus on coverage-style guarantees, often through set-valued prediction or conformal-
ized output selection. Our setting is different: instead of constructing a prediction set
that covers an admissible answer, we study abstention-aware point prediction, where
the system either returns a single LLM response or abstains. Accordingly, our target
is to control the acceptance-conditioned error rate among retained outputs.
Selective Prediction.
Selective prediction allows a model to abstain from answering when its prediction
is considered unreliable, which is especially important in high-stakes or reliability-
sensitive applications. For LLM-based QA, selective answering can reduce harmful
hallucinations by returning responses only when the model is sufficiently confident.
However, a practical selective system should not merely improve average accuracy
after filtering; it should provide a user-specified reliability guarantee for the subset of
answers that are actually returned. Recent studies have explored abstention and risk
control for foundation models, showing that uncertainty-based selection can improve
4
--- PAGE 5 ---
reliability when combined with proper statistical calibration [24, 25, 37]. Our work
follows this direction but focuses on a simple and general confidence-interval-based
calibrationrule.Givenanyuncertaintyscore,CICestimatesthethreshold-conditioned
error rate on a calibration set, constructs an upper confidence bound, and selects the
largest threshold satisfying the target risk level. This yields a deployable selective
answering policy with finite-sample, high-probability control of the error rate among
accepted responses.
3 Methodology
3.1 Notation and Problem Formulation
Let (X,Y⋆) ∼ P denote an input–ground-truth pair, where X ∈ X is a query and
Y⋆ ∈Y isitsreferenceanswer.WeconsiderafrozendeployedLLML,whichproduces
a response
Yˆ =L(X;ξ),
whereξdenotesthemodel’sgenerationrandomness;deterministicdecodingisaspecial
case.
To evaluate whether the generated answer is acceptable for deployment, we
introduce an application-specific alignment criterion
A:Y ×Y →{0,1},
where A(Y⋆,Yˆ) = 1 indicates that the generated answer is aligned with the ground
truth, and A(Y⋆,Yˆ)=0 otherwise. We define the corresponding error indicator as
E =1−A(Y⋆,Yˆ)∈{0,1}. (1)
Given a user-chosen uncertainty measure M, we compute an uncertainty score
U =U(X,Yˆ;M)∈R, (2)
where smaller values indicate more reliable predictions. For a threshold t ∈ R, we
define the thresholding gate
g (X,Yˆ)=1{U ≤t}. (3)
t
A prediction is accepted when g (X,Yˆ)=1, and otherwise the system abstains.
t
Our target is to control the selection-conditioned error rate under threshold t,
defined as
E[E·1{U ≤t}]
R(t):=P(E =1|U ≤t)= , whenever P(U ≤t)>0.
E[1{U ≤t}]
This quantity measures the error proportion among accepted predictions. In the one-
prediction-per-queryselectiveansweringsetting,R(t)alsocoincideswiththemarginal
false discovery rate (mFDR) of the thresholding policy.
5
--- PAGE 6 ---
Let
π(t):=P(U ≤t)
denote the acceptance probability. The deployment objective is to learn a threshold
that accepts as many samples as possible while ensuring
R(t)≤α
for a user-specified risk level α∈(0,1).
We assume access to a held-out calibration set
D ={(X ,Y⋆)}N ,
cal i i i=1
which is exchangeable with future deployment data. Running the frozen LLM on D
cal
yields
{(X ,Y⋆,Yˆ,U ,E )}N ,
i i i i i i=1
where
Yˆ =L(X ;ξ ), U =U(X ,Yˆ;M), E =1−A(Y⋆,Yˆ).
i i i i i i i i i
3.2 UCB-Based Risk Calibration
For any threshold t, define the calibration acceptance count
N
(cid:88)
n(t)= 1{U ≤t}, (4)
i
i=1
and the number of false discoveries among accepted samples
N
(cid:88)
FD(t)= 1{U ≤t, E =1}. (5)
i i
i=1
The empirical selection-conditioned error rate is

 FD(t), n(t)>0,
n(t)
R(cid:98)(t)=
1, n(t)=0.
Toobtainafinite-samplesafetycertificate,weconstructaone-sidedUCBforR(t).
We consider two instantiations.
Hoeffding-style UCB.
For confidence level 1−γ,
 (cid:113)
R(cid:98)(t)+ log(1/γ), n(t)>0,
2n(t)
B (t;γ)=
H
1, n(t)=0.
6
--- PAGE 7 ---
Clopper–Pearson-style UCB.
For confidence level 1−γ,

BetaInv(1−γ; FD(t)+1, n(t)−FD(t)), n(t)>0,
B (t;γ)=
CP
1, n(t)=0,
where BetaInv(q;a,b) denotes the q-quantile of the Beta(a,b) distribution. The
Clopper–Pearsonboundisexactforbinomialproportionsandisoftenlessconservative
than Hoeffding when the accepted subset is small.
Tohandleadaptivethresholdselectionrigorously,weconsiderapre-specified finite
threshold grid
T ={t <t <···<t },
1 2 K
chosen before observing calibration outcomes. For example, T may be a uniform grid
over the score range, or a fixed quantile grid obtained from a pilot split.
For each candidate threshold t ∈ T, we compute a UCB B(t;δ/K), where B can
be either B or B , and δ ∈ (0,1) is the target miscoverage probability. We then
H CP
select the largest threshold whose UCB is below the desired risk level:
(cid:110) (cid:111)
tˆ=max t∈T : B(t;δ/K)≤α . (6)
If the feasible set is empty, we return NULL, indicating that the requested risk level is
unattainable under the current model and uncertainty signal.
Atdeploymenttime,foranewqueryX ,themodeloutputsYˆ anduncertainty
test test
score U . The system returns the answer only if
test
U ≤tˆ; (7)
test
otherwise, it abstains.
3.3 Framework Summary
Our framework converts an arbitrary uncertainty score into a statistically certified
decision rule for selective answering. The procedure consists of three stages:
First, on a held-out calibration set, we compute for each sample an uncertainty
score and an alignment label, thereby linking uncertainty to empirical correctness.
Second, for each candidate threshold, we evaluate the accepted subset induced
by that threshold and construct an upper confidence bound on the corresponding
selection-conditioned error rate.
Third,wechoosethelargestthresholdwhoseUCBremainsbelowtheuser-specified
target risk level, and deploy this threshold as a test-time uncertainty gate.
Thisdesignpreservestheflexibilityofheuristicuncertaintyestimatorswhileadding
a finite-sample safety layer on top of them.
7
--- PAGE 8 ---
3.4 Theoretical Guarantees
We now formalize the validity of the proposed calibration rule.
Assumption 3.1 (Exchangeability) The calibration tuples
{(U ,E )}N
i i i=1
andafuturedeploymentpair(U ,E )areexchangeable.Equivalently,thecalibration
N+1 N+1
and deployment data are identically distributed, and the deployed model together with its
decoding randomness is fixed across samples.
Theorem 3.2 (Fixed-threshold validity) Under Assumption 1, fix any threshold t∈R such
that π(t)=P(U ≤t)>0. Let
N N
(cid:88) (cid:88)
n(t)= 1{U ≤t}, FD(t)= 1{U ≤t, E =1}.
i i i
i=1 i=1
Then conditional on n(t)=n>0,
FD(t)|n(t)=n∼Binomial(n,R(t)). (8)
Consequently, for any γ ∈(0,1),
P(R(t)≤B (t;γ))≥1−γ, (9)
CP
and
P(R(t)≤B (t;γ))≥1−γ. (10)
H
Proof.
For each calibration point, define three mutually exclusive categories:

0, U >t (rejected),
 i
C = 1, U ≤t, E =0 (accepted and correct),
i i i
2,
U ≤t, E =1 (accepted and incorrect).
i i
Because (U ,E ) are i.i.d., the category variables {C }N are i.i.d. multinomial with
i i i i=1
probabilities
P(C =2)=π(t)R(t), P(C =1)=π(t)(1−R(t)), P(C =0)=1−π(t).
i i i
Let N =FD(t) and N +N =n(t). Standard multinomial conditioning yields
2 1 2
N |(N +N =n)∼Binomial(n,R(t)).
2 1 2
This proves the first claim.
TheClopper–Pearsonboundistheexactone-sided(1−γ)upperconfidencebound
for a binomial success probability, hence
P(R(t)≤B (t;γ)|n(t)=n)≥1−γ (11)
CP
8
--- PAGE 9 ---
for every n>0, and therefore also unconditionally.
FortheHoeffdingbound,conditionalonn(t)=n>0,theacceptederrorindicators
are i.i.d. Bernoulli with mean R(t). Applying Hoeffding’s inequality to their empirical
mean R(cid:98)(t) gives
(cid:32) (cid:114) (cid:12) (cid:33)
log(1/γ) (cid:12)
P R(t)>R(cid:98)(t)+ (cid:12)n(t)=n ≤γ. (12)
2n (cid:12)
(cid:12)
Again, averaging over n yields the unconditional statement. □
Theorem 3.3 (Adaptive threshold guarantee) Under Assumption 1, let T = {t ,...,t }
1 K
be a fixed finite threshold grid, and let
(cid:110) (cid:111)
tˆ=max t∈T : B(t;δ/K)≤α , (13)
where B is either B or B . Then
H CP
P(cid:0) tˆ=NULL or R(tˆ)≤α (cid:1) ≥1−δ. (14)
Equivalently,withprobabilityatleast1−δ,everynon-nullthresholdreturnedbythealgorithm
satisfies the desired selection-conditioned risk guarantee.
Proof.
For each fixed t∈T, Theorem 3.2 gives
P(R(t)≤B(t;δ/K))≥1−δ/K. (15)
Define the simultaneous validity event
(cid:92)
E = {R(t)≤B(t;δ/K)}. (16)
t∈T
By the union bound,
(cid:88) δ
P(E)≥1− =1−δ. (17)
K
t∈T
On the event E, every candidate threshold satisfying B(t;δ/K)≤α also satisfies
R(t)≤B(t;δ/K)≤α. (18)
Therefore, if the algorithm returns a non-null threshold tˆ, then necessarily
R(tˆ)≤α. (19)
If no threshold is feasible, the algorithm returns NULL, which is also covered by the
theorem statement. Hence
P(cid:0) tˆ=NULL or R(tˆ)≤α (cid:1) ≥1−δ. (20)
9
--- PAGE 10 ---
Algorithm 1 Upper Confidence Bound Computation and Threshold Calibration
1: Input: Deployed LLM L, N calibration data points {(x i ,y i ∗,yˆ i )}N i=1 , uncertainty
measure M, alignment criterion A, risk level α, significance level δ
2: Output: An FDR-controlled threshold tˆ
3: Quantify the uncertainty score of yˆ i for all i∈[N]: u i ←U(x i ;G);
4: Evaluatewhetheryˆ i isaligedwithy i ∗basedonAforalli∈[N]:a i ←1{A(y i ∗,yˆ i )=
1};
5: Sort uncertainty scores u (1) ≤···≤u (N) , with corresponding a (1) ,...,a (N) ;
6: Initialize tˆ← NULL;
7: for i=1 to N do
8: Let t←u (i) ;
9: Count the number of accepted answers: n←
(cid:80)N
j=1 1{u (j) ≤t};
10: Count the number of misaligned answers among all accepted ones (i.e., false
discovery): FD ←
(cid:80)N
1{u ≤t∧a =0};
j=1 (j) (j)
11: Compute the Hoeffding-style (1 − δ)-upper confidence bound: B ← FD +
n
(cid:113)
log(1/δ);
2n
12: Remark: Or compute the Clopper–Pearson-style exact (1−δ)-upper confi-
dence bound: B←BetaInv(1−δ; FD+1, n−FD);
13: if B≤α then
14: Update tˆ←t;
15: end if
16: end for
17: if tˆ= NULL then
18: Return “Risk level α is unattainable”
19: else
20: Return tˆ
21: end if
□
Proposition 3.4 (Maximal acceptance among certified thresholds) Let
T ={t∈T : B(t;δ/K)≤α}. (21)
safe
If T is non-empty, then the selected threshold
safe
tˆ=maxT (22)
safe
maximizes the acceptance probability π(t) over all certified candidate thresholds:
π(tˆ)= max π(t). (23)
t∈Tsafe
Proof.
For any t ≤t , we have
1 2
1{U ≤t }≤1{U ≤t }, (24)
1 2
hence π(t )≤π(t ). Therefore, among all thresholds in T , the largest one has the
1 2 safe
largest acceptance probability. □
10
--- PAGE 11 ---
3.5 Practical Remarks
Choice of UCB.
The Hoeffding-style bound is closed-form and simple, while the Clopper–Pearson
boundisexactforbinomialproportionsandisgenerallypreferablewhentheaccepted
subset is small. In practice, both can be implemented with the same calibration
pipeline.
Unattainable risk levels.
If no threshold satisfies the UCB constraint, the target risk level α is unattainable
for the current model–uncertainty pair at confidence level 1−δ. This is an intrinsic
limitation of the underlying model quality and uncertainty discriminability, rather
than a failure of the calibration procedure itself.
On implementation with empirical score grids.
For theoretical strictness, the candidate threshold grid should be fixed in advance. In
practice, one may scan all unique calibration scores for finer resolution; however, the
exact guarantee in Theorem 3.3 is most cleanly stated for a pre-specified finite grid,
or alternatively with an additional split / simultaneous testing correction.
Interpretation.
Our method does not require the uncertainty score itself to be calibrated. Instead,
it treats the uncertainty estimator as a ranking signal, and calibrates a statistically
valid operating threshold on top of it. In this sense, the proposed framework converts
arbitrary heuristic uncertainty into a deployable abstention policy with finite-sample
reliability guarantees.
Implementation.
Since the selection-conditioned risk is near-monotonic, i.e., it tends to decrease as the
threshold increases, we adopt fixed-sequence testing instead of Bonferroni correction
(i.e., δ instead of δ/K) [24, 38]. The pseudocode for our calibration framework is
presented by Algorithm 1.
4 Experiments
4.1 Experimental Settings
Base Models.
We evaluate CIC on seven widely used instruction-tuned LLMs with different model
families and scales, including Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct, Qwen2.5-
14B-Instruct [39], OpenChat-3.5 [40], Vicuna-7B-v1.5, Vicuna-13B-v1.5 [41], and
LLaMA-3.1-8B-Instruct [42]. These models cover both relatively small and stronger
instruction-following LLMs, allowing us to examine whether the proposed calibration
framework is robust across different base error rates and uncertainty-quality regimes.
11
--- PAGE 12 ---
Table 1 Test-timeFDR(mean±stdacross100splits)onCommonsenseQA.
0.05 0.10 0.15 0.20 0.25
LLMs UCBs/α BaseER
FDR Fail FDR Fail FDR Fail FDR Fail FDR Fail
UCB-HFD - 100 0.074±0.009 0 0.128±0.008 0 0.180±0.009 0 0.230±0.009 0
Qwen2.5-3B-Instruct 0.239
UCB-CP 0.040±0.008 34 0.090±0.008 0 0.139±0.009 0 0.188±0.009 0 0.237±0.007 0
UCB-HFD 0.024±0.004 89 0.079±0.008 0 0.131±0.008 0 0.183±0.008 0 0.211±0.004 0 0.212
Qwen2.5-7B-Instruct
UCB-CP 0.043±0.006 0 0.092±0.007 0 0.142±0.008 0 0.192±0.008 0 0.211±0.004 0 0.212
UCB-HFD 0.023±0.006 7 0.079±0.007 0 0.131±0.008 0 0.180±0.005 0 0.182±0.004 0 0.182
OpenChat-3.5
UCB-CP 0.043±0.006 0 0.092±0.007 0 0.140±0.008 0 0.182±0.004 0 0.182±0.004 0 0.182
UCB-HFD - 100 - 100 0.121±0.020 97 0.156±0.021 3 0.220±0.014 0 0.410
Vicuna-7b-v1.5
UCB-CP - 100 0.080±0.024 66 0.113±0.029 7 0.178±0.016 0 0.233±0.012 0 0.410
UCB-HFD - 100 0.074±0.008 0 0.128±0.008 0 0.180±0.009 0 0.231±0.009 0 0.271
LLaMA-3.1-8B-Instruct
UCB-CP 0.041±0.008 0 0.090±0.008 0 0.140±0.008 0 0.190±0.009 0 0.238±0.008 0 0.271
UCB-HFD - 100 - 100 0.117±0.014 0 0.174±0.011 0 0.227±0.010 0 0.347
Vicuna-13b-v1.5
UCB-CP 0.055±0.010 86 0.071±0.023 0 0.135±0.014 0 0.185±0.011 0 0.237±0.010 0 0.347
UCB-HFD 0.023±0.005 19 0.080±0.006 0 0.131±0.007 0 0.168±0.004 0 0.168±0.004 0 0.168
Qwen2.5-14B-Instruct
UCB-CP 0.044±0.006 0 0.092±0.007 0 0.141±0.007 0 0.168±0.004 0 0.168±0.004 0 0.168
Benchmarks.
Followingpriorwork[24,25],weconductexperimentsontworepresentativeQAbench-
marks: CommonsenseQA [43] and TriviaQA [44]. CommonsenseQA is a closed-ended
commonsense reasoning benchmark, where each question is associated with a set of
candidateanswersandthemodelisexpectedtoselectthecorrectone.TriviaQAisan
open-endedquestionansweringbenchmarkthatrequiresmodelstogeneratefree-form
answersbasedonfactualknowledge.Together,thesetwodatasetsallowustoevaluate
CIC under both constrained answer selection and open-ended generation settings.
Uncertainty Estimators.
WeusesemanticentropyasthemainuncertaintyestimatorforLLMoutputs[20].For
each input question, we sample multiple responses from the base LLM and estimate
semantic-level uncertainty by measuring the dispersion of generated answers after
accounting for semantic equivalence. Unless otherwise specified, we use 10 sampled
responsesperquestion.Theresultinguncertaintyscoreisusedastherankingsignalfor
selectiveanswering,whereloweruncertaintyindicatesamorereliablemodelresponse.
Alignment Evaluation.
For CommonsenseQA, correctness is evaluated by comparing the model-selected
answer with the ground-truth option. For TriviaQA, because the model output is
free-form, we evaluate whether the generated answer is semantically aligned with the
reference answer. Following prior work [19, 21], we use sentence similarity with a
threshold of 0.6 to determine whether a response should be treated as correct. The
resulting binary correctness label is then converted into an error indicator and used
for confidence-interval calibration.
Calibration Protocol.
For each dataset and model, we randomly split the data into calibration and test
subsets. The calibration set is used only to select the uncertainty threshold, while the
12
--- PAGE 13 ---
Table 2 Test-timeFDR(mean±stdacross100splits)atvarioususer-specifiedrisklevelson
TriviaQAwithsevenLLMs,utilizingsemanticentropy(10samplesperquestion).Weemploy
sentencesimilaritywithathresholdof0.6forcorrectnessevaluation.
0.05 0.1 0.15 0.2 0.25
LLMs UCBs/α BaseER
FDR Fail FDR Fail FDR Fail FDR Fail FDR Fail
UCB-HFD – 100 0.064±0.012 0 0.124±0.008 0 0.163±0.004 0 0.163±0.004 0 0.163
Qwen2.5-3B-Instruct
UCB-CP 0.038±0.004 34 0.086±0.010 0 0.136±0.008 0 0.163±0.004 0 0.163±0.004 0
UCB-HFD – 100 0.077±0.007 0 0.125±0.004 0 0.125±0.004 0 0.125±0.004 0 0.125
Qwen2.5-7B-Instruct
UCB-CP 0.037±0.007 4 0.091±0.007 0 0.125±0.004 0 0.125±0.004 0 0.125±0.004 0
UCB-HFD – 100 0.078±0.008 0 0.118±0.004 0 0.118±0.004 0 0.118±0.004 0 0.118
OpenChat-3.5
UCB-CP 0.039±0.009 0 0.092±0.008 0 0.118±0.004 0 0.118±0.004 0 0.118±0.004 0
UCB-HFD – 100 0.065±0.012 0 0.126±0.009 0 0.169±0.004 0 0.169±0.004 0 0.169
Vicuna-7b-v1.5
UCB-CP 0.057±0.000 99 0.086±0.009 0 0.138±0.009 0 0.169±0.004 0 0.169±0.004 0
UCB-HFD 0.025±0.002 52 0.078±0.006 0 0.115±0.003 0 0.115±0.003 0 0.115±0.003 0 0.115
LLaMA-3.1-8B-Instruct
UCB-CP 0.042±0.006 0 0.090±0.007 0 0.115±0.003 0 0.115±0.003 0 0.115±0.003 0
UCB-HFD – 100 0.077±0.008 0 0.116±0.004 0 0.116±0.004 0 0.116±0.004 0 0.116
Vicuna-13b-v1.5
UCB-CP 0.037±0.009 0 0.090±0.007 0 0.116±0.004 0 0.116±0.004 0 0.116±0.004 0
UCB-HFD – 100 0.079±0.006 0 0.088±0.003 0 0.088±0.003 0 0.088±0.003 0 0.088
Qwen2.5-14B-Instruct
UCB-CP 0.040±0.007 0 0.088±0.004 0 0.088±0.003 0 0.088±0.003 0 0.088±0.003 0
test set is used only for evaluation. Following prior work, we repeat the calibration-
test split 100 times and report the mean and standard deviation over 100 trials. By
default,weuseacalibration-testsplitratioof0.5.Weevaluatemultipleuser-specified
risk levels, α∈{0.05,0.10,0.15,0.20,0.25}.
Compared UCBs.
WeinstantiateCICwithtwoupperconfidencebounds:aHoeffding-styleUCB,denoted
as UCB-HFD, and a Clopper–Pearson-style UCB, denoted as UCB-CP. UCB-HFD
provides a simple closed-form bound, while UCB-CP gives an exact binomial confi-
dence upper bound and is often more suitable when the accepted subset is small. For
each risk level, CIC selects the largest threshold whose UCB does not exceed α. If
no threshold satisfies the constraint, CIC returns no feasible threshold; we report the
number of such failed calibration trials as “Fail”.
Evaluation Metrics.
We report two main metrics. First, we evaluate the empirical false discovery rate
(FDR), defined as the proportion of incorrect responses among accepted outputs on
the test set. This corresponds to the acceptance-conditioned error rate studied in our
theoreticalanalysis.Second,wereportpower,definedastheproportionoftestsamples
accepted by the calibrated threshold. A reliable selective answering system should
keep FDR below the target risk level while achieving high power.
4.2 Empirical Results
Risk Control on CommonsenseQA.
Table 1 reports the test-time FDR on CommonsenseQA under different risk levels.
Across most models and risk levels, both UCB-HFD and UCB-CP successfully keep
the empirical FDR below the user-specified target α. This confirms that CIC can
convertheuristicuncertaintyscoresintostatisticallyreliableselectiveansweringrules.
As α increases, the calibrated threshold becomes less conservative, and the observed
FDRcorrespondinglyincreasestowardthetargetlevel.Thistrendisexpected:alarger
13
--- PAGE 14 ---
Table 3 Test-timePower(meanacross100splits)atvarioususer-specifiedrisklevelsonTriviaQA
withsevenLLMs,utilizingsemanticentropy(10samplesperquestion).
0.05 0.1 0.15 0.2 0.25
LLMs UCBs/α
Power Fail Power Fail Power Fail Power Fail Power Fail
UCB-HFD – 100 0.381 0 0.769 0 1.000 0 1.000 0
Qwen2.5-3B-Instruct
UCB-CP 0.238 34 0.517 0 0.845 0 1.000 0 1.000 0
UCB-HFD – 100 0.741 0 0.999 0 1.000 0 1.000 0
Qwen2.5-7B-Instruct
UCB-CP 0.390 4 0.833 0 1.000 0 1.000 0 1.000 0
UCB-HFD – 100 0.889 0 1.000 0 1.000 0 1.000 0
OpenChat-3.5
UCB-CP 0.670 0 0.929 0 1.000 0 1.000 0 1.000 0
UCB-HFD – 100 0.425 0 0.802 0 1.000 0 1.000 0
Vicuna-7b-v1.5
UCB-CP 0.299 99 0.567 0 0.857 0 1.000 0 1.000 0
UCB-HFD 0.534 52 0.904 0 1.000 0 1.000 0 1.000 0
LLaMA-3.1-8B-Instruct
UCB-CP 0.716 0 0.937 0 1.000 0 1.000 0 1.000 0
UCB-HFD – 100 0.835 0 1.000 0 1.000 0 1.000 0
Vicuna-13b-v1.5
UCB-CP 0.567 0 0.891 0 1.000 0 1.000 0 1.000 0
UCB-HFD – 100 0.970 0 1.000 0 1.000 0 1.000 0
Qwen2.5-14B-Instruct
UCB-CP 0.621 0 0.999 0 1.000 0 1.000 0 1.000 0
risk budget allows the system to accept more uncertain responses, leading to higher
answering coverage but also a higher error rate among accepted outputs.
The results also show that the feasibility of strict risk control depends on the
underlying model and uncertainty estimator. For very small risk levels such as α =
0.05, some model–UCB combinations fail to find a feasible threshold in a subset of
calibrationsplits.Thisdoesnotindicateafailureofthecalibrationprocedure;rather,
it means that the given model and uncertainty signal cannot certify such a strict risk
level with the available calibration data. In contrast, when the target risk level is
moderatelyrelaxed,CICusuallyfindsfeasiblethresholdsandmaintainsvalidempirical
FDR control.
Risk Control on TriviaQA.
Table 2 presents the test-time FDR results on TriviaQA. Compared with Common-
senseQA, TriviaQA involves open-ended generation and semantic answer matching,
making the evaluation more challenging. Nevertheless, CIC still achieves reliable risk
control across the evaluated LLMs. For most models, the empirical FDR remains
below or close to the target risk level across all tested values of α. This demonstrates
that CIC is not limited to closed-ended answer selection, but can also be applied to
open-ended QA when an appropriate alignment criterion is available.
We further observe that when the base model already has a relatively low error
rate, the FDR may saturate at the base error rate for larger α. In such cases, the
calibrated threshold can accept nearly all test samples while still satisfying the target
risk constraint. This explains why some entries at larger risk levels have FDR values
close to the base error rate and power close to one.
Answering Power on TriviaQA.
Table3reportstheansweringpoweronTriviaQA.Theresultsshowaclearmonotonic
trend:asthetargetrisklevelαincreases,CICacceptsalargerfractionoftestsamples.
14
--- PAGE 15 ---
Table 4 Test-timePower(meanacross100splits)atvarioususer-specifiedrisklevelson
CommonsenseQAwithsevenLLMs,
Risk level (α)
LLMs UCBs/α
0.05 0.10 0.15 0.20 0.25
UCB-HFD - 0.502 0.774 0.895 0.984
Qwen2.5-3B-Instruct
UCB-CP 0.176 0.623 0.805 0.909 0.995
UCB-HFD 0.345 0.720 0.858 0.952 1.000
Qwen2.5-7B-Instruct
UCB-CP 0.572 0.766 0.882 0.970 1.000
UCB-HFD 0.488 0.802 0.921 0.999 1.000
OpenChat-3.5
UCB-CP 0.655 0.839 0.940 1.000 1.000
UCB-HFD - 0.551 0.740 0.860 0.941
LLaMA-3.1-8B-Instruct
UCB-CP 0.391 0.608 0.770 0.874 0.955
UCB-HFD - - 0.384 0.617 0.763
Vicuna-13b-v1.5
UCB-CP 0.041 0.132 0.468 0.646 0.794
UCB-HFD 0.446 0.833 0.942 1.000 1.000
Qwen2.5-14B-Instruct
UCB-CP 0.661 0.865 0.959 1.000 1.000
At strict risk levels, the method abstains more frequently to maintain reliability; at
relaxed risk levels, it returns more answers and often reaches full or near-full power.
This behavior reflects the central trade-off in selective answering: lower risk requires
more abstention, while higher risk permits broader coverage.
Comparing the two UCB variants, UCB-HFD and UCB-CP exhibit different con-
servativeness patterns. UCB-CP is often more effective when the accepted subset
is small, because it directly models the binomial error proportion and can produce
sharper confidence bounds in low-count regimes. However, the relative advantage
variesacrossmodelsanddatasets,dependingonthecalibrationsamplesize,baseerror
rate, and discriminative quality of the uncertainty estimator.
Answering Power on CommonsenseQA.
Table 4 reports the answering power on CommonsenseQA. The same risk–coverage
trade-off can be observed. For stronger models or settings where semantic entropy
better separates correct from incorrect predictions, CIC achieves high power even
underrelativelystrictrisklevels.Forweakermodelsorlessdiscriminativeuncertainty
scores,themethodbecomesmoreconservativeandmayabstainfromalargerfraction
of samples. This is desirable in reliability-sensitive deployment, because the system
shouldavoidansweringwhenthecalibrationdatacannotcertifythedesirederrorlevel.
Across both datasets, the empirical results support the main design principle of
CIC:uncertaintyscoresneednotbeperfectlycalibratedbythemselves,aslongasthey
15
--- PAGE 16 ---
Fig. 2 Sensitivity analysis under different calibration-test split ratios on CommonsenseQA using
Qwen2.5-3B-Instruct.Thex-axisreportsthecalibration:testsplitratio,where1:1,2:3,3:7,1:4,and
1:9 correspond to calibration proportions of 0.5, 0.4, 0.3, 0.2, and 0.1, respectively. The dashed line
indicatesthetargetalignmentproportionof0.90.
provideausefulrankingsignal.Theconfidence-intervalcalibrationlayerthenconverts
this ranking signal into a threshold with finite-sample risk control.
Sensitivity to Calibration-Test Split Ratios.
WefurtherevaluatetherobustnessofCICunderdifferentcalibration-testsplitratios.
By default, we use a 1:1 split between calibration and test data. To examine whether
the empirical reliability is sensitive to the calibration size, we additionally vary the
calibration-test ratio from 1:1 to 2:3, 3:7, 1:4, and 1:9, corresponding to calibration
proportionsof0.5,0.4,0.3,0.2,and0.1,respectively.Weconductthissensitivitystudy
on CommonsenseQA using Qwen2.5-3B-Instruct.
As shown in Figure 2, CIC remains stable across all evaluated split ratios. The
empiricalalignmentproportionstaysabovethetargetlevelof0.90,withvaluesranging
from 0.9190 to 0.9290. Although smaller calibration sets may in principle lead to
wider confidence intervals and more conservative threshold selection, the observed
performance does not degrade substantially in this experiment. These results suggest
that CIC is empirically robust to moderate changes in the calibration-test split ratio.
Discussion.
Overall, the experiments demonstrate three key findings. First, CIC provides reliable
control of the error rate among accepted answers across closed-ended and open-
ended QA benchmarks. Second, the calibrated threshold naturally adapts to the
user-specified risk level, yielding a smooth trade-off between reliability and answer-
ingefficiency.Third,infeasiblecasesmainlyoccurunderverystrictriskrequirements,
especially when the base model error rate is high or the uncertainty estimator
has limited discriminative power. These findings are consistent with the theoretical
interpretation of CIC: the method can certify reliable thresholds when the model–
uncertainty pair supports the desired risk level, and otherwise correctly reports that
the requested risk level is unattainable.
16
--- PAGE 17 ---
5 Conclusion
In this paper, we proposed CIC, a confidence-interval-based calibration framework
for risk-controlled selective answering with large language models. Instead of assum-
ing that heuristic uncertainty scores are intrinsically calibrated, CIC treats them as
black-boxrankingsignalsandlearnsastatisticallycertifiedabstentionthresholdfrom
a held-out calibration set. By estimating the error rate among accepted responses
and constructing a high-probability upper confidence bound, CIC selects the largest
threshold satisfying a user-specified risk level, thereby balancing answering efficiency
and deployment reliability.
Theoretically, we established finite-sample, high-probability guarantees under
exchangeability, showing that the selected threshold, if feasible, controls the
acceptance-conditionederrorrateatthetargetlevel.Empirically,experimentsonboth
closed-endedandopen-endedQAbenchmarksdemonstratethatCICachievesreliable
risk control across multiple LLMs and uncertainty settings, while maintaining strong
answeringpower.Thesensitivityanalysisfurthersuggeststhattheframeworkremains
stable under different calibration-test split ratios.
Overall, CIC provides a simple, model-agnostic, and practically deployable statis-
tical layer for converting heuristic LLM uncertainty estimates into reliable selective
answering policies. Future work may extend this framework to multi-answer gener-
ation, multi-risk constraints, adaptive threshold selection with sharper simultaneous
guarantees, and more complex deployment scenarios such as retrieval-augmented
generation and human-AI collaborative decision-making.
Declarations
Ethics approval and consent to participate
Not applicable.
Consent for publication
Not applicable.
Clinical trial number
Not applicable.
Funding
The authors received no specific funding for this work.
Author contributions
Sijin Dong conceived the study, developed the methodology, conducted the experi-
ments, analyzed the results, and wrote the manuscript. Hiroyuki Shinnou supervised
the study and reviewed and revised the manuscript. All authors read and approved
the final manuscript.
17
--- PAGE 18 ---
Conflict of interest
The authors declare that they have no conflict of interest or competing interests.
Data availability
The datasets used in this study are publicly available benchmarks. CommonsenseQA
and TriviaQA are available from their respective public repositories. Additional
experimental details are provided in the manuscript.
References
[1] Wang,S.,Xu,T.,Li,H.,Zhang,C.,Liang,J.,Tang,J.,Yu,P.S.,Wen,Q.:Large
language models for education: A survey and outlook. IEEE Signal Processing
Magazine 42(6), 51–63 (2026)
[2] Jiang, J., Wang, F., Shen, J., Kim, S., Kim, S.: A survey on large language
models for code generation. ACM Transactions on Software Engineering and
Methodology 35(2), 1–72 (2026)
[3] Eldem, A., Eldem, H.: The development and evaluation of agricultural question-
answeringsystemsbasedonlargelanguagemodels.ScientificReports16(1),5357
(2026)
[4] Song, Z., Xu, N., Ding, H.: Decision-making framework for autonomous vehicles
in complex scenarios using large language models. Automotive Innovation, 1–21
(2026)
[5] Bi, J., Yan, D., Wang, Y., Huang, W., Chen, H., Wan, G., Ye, M., Xiao, X.,
Schuetze,H.,Tresp,V.,Ma,Y.:CoT-Kinetics:ATheoreticalModelingAssessing
LRM Reasoning Process (2025)
[6] Huang,X.,Rishabh,Franke,G.,Yang,Z.,Bai,J.,Bai,W.,Bi,J.,Ding,Z.,Duan,
Y., Fan, C., Fan, W., Gao, X., Guo, R., He, Y., He, Z., Hu, X., Johnson, N.,
Li, B., Lin, F., Lin, S., Liu, T., Ma, Y., Shen, H., Sun, H., Wang, B., Wang, F.,
Wang,H.,Wang,H.,Wang,Y.,Wang,Y.,Wang,Z.,Wang,Z.,Wu,Y.,Xiao,Z.,
Xie,C.,Yang,F.,Yang,J.,Ye,Q.,Ye,Z.,Zeng,G.,Zhang,Y.E.,Zhang,Z.,Zhu,
Z., Ghanem, B., Torr, P., Li, G.: Loong: Synthesize Long Chain-of-Thoughts at
Scale through Verifiers (2025)
[7] Wan, G., Fu, L., Liu, H., Jin, Y., Leong, H.Y., Jiang, E.H., Geng, H., Bi, J., Ma,
Y.,Tang,X.,Prakash,B.A.,Sun,Y.,Wang,W.:BeyondMagicWords:Sharpness-
Aware Prompt Evolving for Robust Large Language Models with TARE (2025)
[8] Tian, Y., Chen, S., Xu, Z., Wang, Y., Bi, J., Han, P., Wang, W.: Reinforcement
Mid-Training (2025)
18
--- PAGE 19 ---
[9] Rong, X., Huang, W., Liang, J., Bi, J., Xiao, X., Li, Y., Du, B., Ye, M.: Back-
door cleaning without external guidance in mllm fine-tuning. arXiv preprint
arXiv:2505.16916 (2025)
[10] Wang,Y.,Bi,J.,Ma,Y.,Pirk,S.:Ascd:Attention-steerablecontrastivedecoding
for reducing hallucination in mllm. arXiv preprint arXiv:2506.14766 (2025)
[11] Bi, J., Wang, Y., Chen, H., Xiao, X., Hecker, A., Tresp, V., Ma, Y.: LLaVA
steering: Visual instruction tuning with 500x fewer parameters through modality
linear representation-steering. In: Che, W., Nabende, J., Shutova, E., Pilehvar,
M.T. (eds.) Proceedings of the 63rd Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers), pp. 15230–15250 (2025)
[12] Bi, J., Wang, Y., Yan, D., Aniri, Huang, W., Jin, Z., Ma, X., Hecker, A., Ye, M.,
Xiao,X.,Schuetze,H.,Tresp,V.,Ma,Y.:PRISM:Self-PruningIntrinsicSelection
Method for Training-Free Multimodal Data Selection (2025)
[13] Jiang, K., Jiang, N., Du, Y., Ren, Y., Li, Y., Gao, Y., Bi, J., Ma, Y., Liu, Q.,
Wang,X.,Jia,Y.,Jiang,H.,Hu,Y.,Li,B.,Liu,L.:MINED:ProbingandUpdat-
ing with Multimodal Time-Sensitive Knowledge for Large Multimodal Models
(2025)
[14] Jiang, K., Jiang, H., Jiang, N., Gao, Z., Bi, J., Ren, Y., Li, B., Du, Y., Liu, L.,
Li,Q.:KORE:EnhancingKnowledgeInjectionforLargeMultimodalModelsvia
Knowledge-Oriented Augmentations and Constraints (2025)
[15] Zhang, G., Bi, J., Gu, J., Chen, Y., Tresp, V.: Spot! revisiting video-language
models for event understanding. arXiv preprint arXiv:2311.12919 (2023)
[16] Peng, T., Du, Y., Ji, P., Dong, S., Jiang, K., Ma, M., Tian, Y., Bi, J., Li, Q.,
Du, W., Xiao, F., Cui, L.: Can Visual Input Be Compressed? A Visual Token
Compression Benchmark for Large Multimodal Models (2025)
[17] Li,Z.,Wu,X.,Wang,Z.,Li,J.,Tian,Y.,Bi,J.,Ma,Y.,Ye,Y.,Zhang,C.:Graph
is a Substrate Across Data Modalities (2026)
[18] Gawlikowski, J., Tassi, C.R.N., Ali, M., Lee, J., Humt, M., Feng, J., Kruspe, A.,
Triebel, R., Jung, P., Roscher, R., et al.: A survey of uncertainty in deep neural
networks. Artificial intelligence review 56, 1513–1589 (2023)
[19] Duan, J., Cheng, H., Wang, S., Zavalny, A., Wang, C., Xu, R., Kailkhura,
B., Xu, K.: Shifting attention to relevance: Towards the predictive uncertainty
quantification of free-form large language models. In: Proceedings of the 62nd
Annual Meeting of the Association for Computational Linguistics (Volume 1:
Long Papers), pp. 5050–5063 (2024)
[20] Kuhn, L., Gal, Y., Farquhar, S.: Semantic uncertainty: Linguistic invariances
19
--- PAGE 20 ---
for uncertainty estimation in natural language generation. In: The Eleventh
International Conference on Learning Representations (2023)
[21] Wang, Z., Duan, J., Yuan, C., Chen, Q., Chen, T., Zhang, Y., Wang, R., Shi,
X., Xu, K.: Word-sequence entropy: Towards uncertainty estimation in free-form
medical question answering applications and beyond. Engineering Applications
of Artificial Intelligence 139, 109553 (2025)
[22] Wang, Z., Duan, J., Cheng, L., Zhang, Y., Wang, Q., Shi, X., Xu, K., Shen,
H.T., Zhu, X.: Conu: Conformal uncertainty in large language models with cor-
rectness coverage guarantees. In: Findings of the Association for Computational
Linguistics: EMNLP 2024, pp. 6886–6898 (2024)
[23] Gui,Y.,Jin,Y.,Ren,Z.:Conformalalignment:Knowingwhentotrustfoundation
modelswithguarantees.AdvancesinNeuralInformationProcessingSystems37,
73884–73919 (2024)
[24] Wang, Z., Duan, J., Wang, Q., Zhu, X., Chen, T., Shi, X., Xu, K.: Coin:
Uncertainty-guarding selective question answering for foundation models with
provable risk guarantees. Proceedings of the AAAI Conference on Artificial
Intelligence 40(40), 33764–33772 (2026)
[25] Wang, Z., Chen, T., Zhang, Y., Shen, H.T., Shi, X., Xu, K., et al.: Lec: Lin-
ear expectation constraints for false-discovery control in selective prediction and
routing systems. arXiv preprint arXiv:2512.01556 (2025)
[26] Angelopoulos, A.N., Bates, S., Jordan, M., Malik, J.: Uncertainty sets for image
classifiers using conformal prediction. In: International Conference on Learning
Representations (2021)
[27] Angelopoulos, A.N., Bates, S.: Conformal prediction: A gentle introduction.
Foundations and Trends in Machine Learning 16(4), 494–591 (2023)
[28] Angelopoulos,A.N.,Barber,R.F.,Bates,S.:Theoreticalfoundationsofconformal
prediction. arXiv preprint arXiv:2411.11824 (2024)
[29] Wang, Z., Wang, Q., Zhang, Y., Chen, T., Zhu, X., Shi, X., Xu, K.: Sconu:
Selective conformal uncertainty in large language models. In: Proceedings of the
63rd Annual Meeting of the Association for Computational Linguistics (Volume
1: Long Papers), pp. 19052–19075 (2025)
[30] Wang,Q.,Geng,T.,Wang,Z.,Wang,T.,Fu,B.,Zheng,F.:Samplethenidentify:
Ageneralframeworkforriskcontrolandassessmentinmultimodallargelanguage
models.In:TheThirteenthInternationalConferenceonLearningRepresentations
(2025)
[31] Li, Y., Hu, A., Ye, Y., Tong, S., Wang, Z., Fu, B.: Set-valued prediction for
20
--- PAGE 21 ---
large language models with feasibility-aware coverage guarantees. arXiv preprint
arXiv:2603.22966 (2026)
[32] Clopper, C.J., Pearson, E.S.: The use of confidence or fiducial limits illustrated
in the case of the binomial. Biometrika 26(4), 404–413 (1934)
[33] Tan, B., Wang, Z., Duan, J., Xu, K., Shen, H.T., Shi, X., Shen, F.: Confor-
mal lesion segmentation for 3d medical images. arXiv preprint arXiv:2510.17897
(2025)
[34] Campos, M., Farinhas, A., Zerva, C., Figueiredo, M.A., Martins, A.F.: Confor-
mal prediction for natural language processing: A survey. Transactions of the
Association for Computational Linguistics 12, 1497–1516 (2024)
[35] Quach,V.,Fisch,A.,Schuster,T.,Yala,A.,Sohn,J.H.,Jaakkola,T.S.,Barzilay,
R.: Conformal language modeling. In: The Twelfth International Conference on
Learning Representations (2024)
[36] Mohri,C.,Hashimoto,T.:Languagemodelswithconformalfactualityguarantees.
In: Proceedings of the 41st International Conference on Machine Learning, pp.
36029–36047 (2024)
[37] Jia, Z.,Ye, Y., Jia,S., Qian, Y., Wang, H., Chen, B.,Tang, D., Yu, J., Wang, Z.:
Balancerag: Joint risk calibration for cascaded retrieval-augmented generation.
arXiv preprint arXiv:2605.20084 (2026)
[38] Jung, J., Brahman, F., Choi, Y.: Trust or escalate: LLM judges with provable
guaranteesforhumanagreement.In:TheThirteenthInternationalConferenceon
Learning Representations (2025)
[39] Bai, J., Bai, S., Chu, Y., Cui, Z., Dang, K., Deng, X., Fan, Y., Ge, W., Han, Y.,
Huang,F.,etal.:Qwentechnicalreport.arXivpreprintarXiv:2309.16609(2023)
[40] Wang, G., Cheng, S., Zhan, X., Li, X., Song, S., Liu, Y.: Openchat: Advanc-
ing open-source language models with mixed-quality data. In: International
Conference on Learning Representations, vol. 2024, pp. 57021–57040 (2024)
[41] Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z.,
Li, Z., Li, D., Xing, E., et al.: Judging llm-as-a-judge with mt-bench and chat-
bot arena. Advances in neural information processing systems 36, 46595–46623
(2023)
[42] Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T.,
Rozi`ere, B., Goyal, N., Hambro, E., Azhar, F., et al.: Llama: Open and efficient
foundation language models. arXiv preprint arXiv:2302.13971 (2023)
[43] Talmor, A., Herzig, J., Lourie, N., Berant, J.: CommonsenseQA: A question
21
--- PAGE 22 ---
answering challenge targeting commonsense knowledge. In: Burstein, J., Doran,
C., Solorio, T. (eds.) Proceedings of the 2019 Conference of the North Ameri-
can Chapter of the Association for Computational Linguistics: Human Language
Technologies, Volume 1 (Long and Short Papers), pp. 4149–4158 (2019)
[44] Joshi, M., Choi, E., Weld, D., Zettlemoyer, L.: TriviaQA: A large scale dis-
tantly supervised challenge dataset for reading comprehension. In: Barzilay, R.,
Kan,M.-Y.(eds.)Proceedingsofthe55thAnnualMeetingoftheAssociationfor
Computational Linguistics (Volume 1: Long Papers), pp. 1601–1611 (2017)
22