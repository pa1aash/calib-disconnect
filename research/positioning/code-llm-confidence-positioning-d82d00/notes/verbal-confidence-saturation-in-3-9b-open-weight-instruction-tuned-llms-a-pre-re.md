---
title: 'Verbal Confidence Saturation in 3-9B Open-Weight Instruction-Tuned LLMs: A
  Pre-Registered Psychometric Validity Screen'
id: verbal-confidence-saturation-in-3-9b-open-weight-instruction-tuned-llms-a-pre-re
tags:
- code-llm-confidence-positioning-d82d00
- f-measurement-framing
created: '2026-11-10T08:24:30.321738Z'
updated: '2026-11-10T08:27:08.854530Z'
source: https://arxiv.org/abs/2604.22215
status: draft
type: note
deprecated: false
summary: 'arXiv 2604.22215 (Cacioli). Pre-registered psychometric validity screen:
  7/7 instruct models 3-9B Invalid on numeric verbal confidence, mean ceiling 91.7%,
  524 TriviaQA items, 8,384 trials; logprob does not predict verbal (R2<0.01). F psychometric
  framing, non-code. Full text via PDF (HTML fetch hit AUTH_REQUIRED false positive).'
---

Verbal Confidence Saturation in 3–9B Open-Weight
                                                                Instruction-Tuned LLMs:
                                                     A Pre-Registered Psychometric Validity Screen
                                                                               Jon-Paul Cacioli
                                                                  Independent Researcher, Melbourne, Australia
                                                                          ORCID: 0009-0000-7054-2014




arXiv:2604.22215v1 [cs.CL] 24 Apr 2026
                                                                    https://github.com/synthiumjp/koriat

                                                                                       April 2026


                                                                                        Abstract
                                                  Verbal confidence elicitation is widely used to extract uncertainty estimates from LLMs. We
                                              tested whether seven instruction-tuned open-weight models (3–9B parameters, four families)
                                              produce verbalised confidence that meets minimal validity criteria for item-level Type-2 dis-
                                              crimination under minimal numeric elicitation with greedy decoding. In a pre-registered study
                                              (OSF: https://osf.io/azbvx), 524 TriviaQA items were administered under numeric (0–100)
                                              and categorical (10-class) elicitation to eight models at Q5_K_M quantisation on consumer
                                              hardware, yielding 8,384 deterministic trials. A psychometric validity screen (Appendix A) was
                                              applied to each model–format cell. All seven instruct models were classified Invalid on numeric
                                              confidence (H2 confirmed, 7/7 vs. predicted ≥ 4/7), with a mean ceiling rate of 91.7% (H1 con-
                                              firmed). Categorical elicitation did not rescue validity. Instead, it disrupted task performance
                                              in six of seven models, producing accuracy below 5% (H4 not confirmed). Token-level logprob-
                                              ability did not usefully predict verbalised confidence under the observed variance regime (H5
                                              confirmed, mean cross-validated R2 < 0.01). Within the reasoning-distilled model, reasoning-
                                              trace length showed a strong negative partial correlation with confidence (ρ = −.36, p < .001),
                                              consistent with the Reasoning Contamination Effect. These results do not imply that internal
                                              uncertainty representations are absent. They show that minimal verbal elicitation fails to pre-
                                              serve internal signals at the output interface in this model-size regime. Psychometric screening
                                              should precede any downstream use of such signals.


                                         1    Introduction
                                         Verbal confidence elicitation is widely used to extract uncertainty estimates from large language
                                         models [Xiong et al., 2023, Tian et al., 2023, Steyvers and Peters, 2025]. The premise is that the
                                         verbalised number reflects an internal signal that discriminates correct from incorrect responses.
                                         Recent mechanistic work supports this in part. Kumaran et al. [2026] showed that verbal confidence
                                         in Gemma 3 27B is computed via cached retrieval at answer-adjacent positions and contains variance
                                         not explained by token log-probabilities.
                                             The practical utility of verbal confidence depends on whether the elicited signal carries item-
                                         level information in the deployment context. Three concurrent lines of evidence establish a readout
                                         problem. Miao and Ungar [2026] showed that calibration and verbalised confidence are encoded in
                                         orthogonal directions in the residual stream. Wang and Stengel-Eskin [2026] documented confidence
                                         saturation on TriviaQA and SimpleQA. Seo et al. [2026] identified answer-dependent confidence

                                                                                             1
generation as a driver of overconfidence. Yang [2024] found that verbalised confidence in small
open-weight models can be near-independent from accuracy, though this depends strongly on the
elicitation method.
     Most calibration work assumes the confidence distribution spans the scale and varies with cor-
rectness [Geng et al., 2024, Steyvers et al., 2025]. This study tests that assumption directly. We
apply a psychometric validity screen to classify model–format combinations as Invalid, Indetermi-
nate, or Valid before any calibration is attempted. The question is not how miscalibrated the signal
is, but whether it meets minimal criteria for item-level Type-2 use.
     We treat saturation as a validity failure rather than a calibration failure. A distribution collapsed
to the ceiling cannot support item-level discrimination because the ordinal relationships between
trials have been lost at elicitation. No post-hoc rescaling can recover what was never emitted.
     This study evaluates default interface behaviour under minimal elicitation with greedy decoding.
It does not test the capacity of these models to express uncertainty under structured or scaffolded
prompts. A model that fails the screen here may produce a valid signal under a richer elicitation
regime. That is a separate empirical question. Validity is a property of the model–probe–task
interaction [Cacioli, 2026e, Rust et al., 2021], not an intrinsic property of the model.

1.1   Hypotheses
Four confirmatory hypotheses were pre-registered (OSF: https://osf.io/azbvx).
    H1 (saturation prevalence). The mean proportion of trials with numeric confidence ≥ 95%
across seven instruct models exceeds 60%.
    H2 (validity screening). At least four of seven instruct models are classified Invalid on
numeric confidence under the validity protocol (Appendix A).
    H4 (format rescue). Among models classified Invalid under numeric elicitation, at least two
are reclassified as non-Invalid under categorical elicitation.
    H5 (logprob–confidence independence). Mean cross-validated R2 of ridge regression pre-
dicting verbal confidence from length-normalised logprobability is below 0.20 in both conditions,
indicating no usable predictive relationship.
    H3 was retired pre-registration after sanity data showed the base model does not produce ver-
balised confidence under continuation prompting (see pre-registration §10).


2     Methods
2.1   Models
Eight open-weight LLMs were evaluated, all run as Q5_K_M GGUF quantisations via llama-cpp-
python 0.3.16 with Vulkan backend on an AMD RX 7900 GRE 16 GB (Table 1).
   M1 is a base model retained for one exploratory analysis (E-base) comparing logprob distri-
butions between the base and instruct versions of Llama-3-8B. M1 does not contribute to any
confirmatory hypothesis.

2.2   Substrate and design
524 items from TriviaQA rc.nocontext validation split [Joshi et al., 2017], drawn deterministically
with numpy.random.default_rng(seed=42). Design: 8 models × 2 conditions (NUM, CAT) × 524
items = 8,384 trials. Confirmatory sample: 7 instruct models × 2 × 524 = 7,336 trials. Inference



                                                    2
                                     Table 1: Model sample.
       ID    Model                            Family               Params             Role
       M1    Meta-Llama-3-8B                  Llama 3 base         8B         Exploratory
       M2    Meta-Llama-3-8B-Instruct         Llama 3 instruct     8B        Confirmatory
       M3    Meta-Llama-3.1-8B-Instruct       Llama 3.1 instruct   8B        Confirmatory
       M4    Mistral-7B-Instruct-v0.3         Mistral              7B        Confirmatory
       M5    Qwen2.5-3B-Instruct              Qwen 2.5             3B        Confirmatory
       M6    Qwen2.5-7B-Instruct              Qwen 2.5             7B        Confirmatory
       M7    Gemma-2-9b-it                    Gemma 2              9B        Confirmatory
       M8    DeepSeek-R1-Distill-Llama-8B     DeepSeek R1          8B        Confirmatory


was greedy (temperature = 0), deterministic (seed = 42), with logprobs collected for the top 5
tokens at each position.
    Greedy decoding isolates the model’s maximum-likelihood output. Sampling introduces stochas-
tic variance that conflates confidence-expression behaviour with sampling noise. Many real deploy-
ments do not use pure greedy decoding. The findings characterise default interface behaviour, not
model capacity.

2.3   Elicitation conditions
Numeric (NUM). System prompt: “You are answering trivia questions. After your answer, state
your confidence as a percentage from 0 to 100.”
    Categorical (CAT). System prompt: “Classify your confidence into one of the following classes
based on how likely the answer above is to be correct (NO REASONING OR EXPLANATION):”
followed by a 10-class ordinal scale from “No chance” (0.0–0.1) to “Almost certain” (0.9–1.0).
    M1 used a continuation prompt (Q: {question} / A:) with no confidence elicitation.

2.4   Validity screening protocol
Each model–condition cell was screened using a psychometric validity protocol adapted from clinical
assessment practice (MMPI-3: Ben-Porath and Tellegen 2020; PAI: Morey 1991). The full protocol
is provided in Appendix A. Criterion validity was demonstrated in Cacioli [2026f], where Invalid-
classified models showed mean AUROC2 = .357 versus .624 for Valid-classified models (d = 2.81).
    Continuous confidence values are binarised at 0.50, producing a 2×2 contingency table. Three
indices are computed: L = P (high confidence | incorrect), Fp = P (low confidence | correct), and
RBS = Fp − (1 − L). A degeneracy pre-check classifies any cell with > 95% of binarised responses
in a single category as Invalid without further analysis.

2.5   Analysis plan
All analyses were pre-registered (OSF: https://osf.io/azbvx, locked 15 April 2026). Cells with
> 30% parse failure are excluded from confirmatory analyses. Parse failure is treated as missing
at random. The MAR assumption is evaluated in E8 and the H1 sensitivity analysis (A8) tests
robustness directly.




                                                3
2.6                                                               Pre-registration deviations
One deviation occurred. The original ParquetWriter class inferred its schema from the first flushed
batch. When batches contained entirely null values in nullable columns, pyarrow inferred mis-
matched types. The fix replaced inferred schema with an explicit pyarrow schema. No collection
logic, seeds, prompts, parsing, or records were affected.


3                                            Results
3.1                                                               Confirmatory hypotheses
H1: Saturation prevalence, confirmed. Across the seven instruct models on numeric elicitation,
the mean proportion of parse-success trials with confidence ≥ 95% was 91.7% (range 72.4–96.8%).
All seven exceeded the 60% threshold individually (Figure 1). The sensitivity analysis (A8), coding
parse failures as non-variable responses, yielded 92.7%.

                                                                                                & R Q I L G H Q F H  F H L O L Q J  U D W H V  E \  P R G H O  D Q G  H O L F L W D W L R Q  I R U P D W
                                                                                                                                                                                                    1 8 0        
                                                                                                                                                                                                                           & $ 7      F O D V V 
                                                                               




       W U L D O V  Z L W K  F R Q I L G H Q F H      
                                                                     
                                                                                                                                                                                                                                  

                                                                                                                                                                                                                     +   W K U H V K R O G      
                                                                     


                                                                     


                                                                                                                                                                                                           
                                                                                                                                                                                                                                             
                                                                                                                
                                                                                                                                                        
                                                                      
                                                                                  0                     0                     0                     0                     0                     0                              0 
                                                                                                                                                   0 R G H O

Figure 1: Confidence ceiling rates by model and elicitation format. The dashed line shows the H1
threshold (60%). All seven instruct models exceed 72% on NUM. CAT ceiling rates are near zero
for most models.

    H2: Validity screening, confirmed. All seven instruct models were classified Invalid on
numeric confidence, exceeding the pre-registered threshold of ≥ 4. Five models were classified
Invalid via the degeneracy criterion (> 95% of binarised responses in a single category) with L
values ranging from 0.949 to 0.986. Two models (M2, M7) showed complete degeneracy: TRIN =
1.0, L = 1.0, zero low-confidence observations across 500+ trials.
    H4: Format rescue, not confirmed. Zero models were reclassified from Invalid (NUM) to
non-Invalid (CAT). Categorical elicitation introduced a different failure mode: task-performance
collapse (Table 2).

                                                                                                                                              4
                   Table 2: Accuracy and parse rates under categorical elicitation.
           Model     n success   n correct   Accuracy   Parse rate   Validity tier
           M2             504          10       2.0%        96.2%    Insufficient
           M3             161         105      65.2%        30.7%    Insufficient (§6.6)
           M4             523          13       2.5%        99.8%    Insufficient
           M5             503          21       4.2%        96.0%    Insufficient
           M6             521           4       0.8%        99.4%    Insufficient
           M7             523           1       0.2%        99.8%    Invalid (degeneracy)
           M8              71          18      25.4%        13.5%    Insufficient


    The specific 10-class categorical prompt disrupted question-answering behaviour. Models that
achieved 59–76% accuracy under NUM dropped to 0.2–4.2% under CAT. Whether simpler categor-
ical formats would avoid this interaction failure is an open question [Yang, 2024].
    H5: Logprob–confidence independence, confirmed. Mean cross-validated R2 was −0.60
on NUM and 0.03 on CAT, both well below the 0.20 threshold. The negative NUM mean is driven
by M5 (RCV2 = −4.61), where near-zero confidence variance produces degenerate folds. The median
  2
RCV   on NUM was 0.06. Token-level logprobability does not usefully predict verbalised confidence
under the observed variance regime.

3.2   Type-2 AUROC2
Despite universal validity failure on NUM, AUROC2 values were modestly above chance (Fig-
ure 2), ranging from 0.527 (M5) to 0.683 (M3). This does not contradict the validity classification.
AUROC2 is a ranking metric driven by 3–13% residual non-ceiling responses. A deployment system
cannot act on a signal identical for 97% of inputs.

3.3   Exploratory analyses
E5: Reasoning contamination probe. Within M8 NUM (n = 409), reasoning-trace length
showed a negative zero-order Spearman correlation with verbalised confidence (ρ = −.41, p < .001).
After controlling for item difficulty, the partial correlation remained strong (ρ = −.36, p < .001;
Figure 3). This is consistent with Miao and Ungar’s (2026) Reasoning Contamination Effect and
with a simpler account where difficult items require more tokens and receive lower confidence.
    E3: Item-level sensitivity. Item difficulty correlated with mean confidence across instruct
models at ρ = .50 (p < .001, n = 524). The models carry item-level information. It does not survive
the verbalised readout under minimal elicitation.
    E8: MAR plausibility check. Parse failure was higher for correct trials (18.8%) than incorrect
(10.1%), indicating the MAR assumption is not strictly met. The A8 sensitivity analysis is consistent
with the saturation pattern being conservative (mean ceiling rate increased from 91.7% to 92.7%).
Non-random missingness remains a limitation.
    E9: Split-half stability. Validity classifications agreed across random half-splits on 14/14
instruct model–condition cells. 100% agreement at 262 items per split.




                                                  5
                                   7 \ S H    $ 8 5 2 &   E \  P R G H O  D Q G  F R Q G L W L R Q   E R R W V W U D S      & , 
                                                     F K D Q F H
          0   1 8 0                                                                                                   Q     
           0   & $ 7                                                                             Q     

          0   1 8 0                                                                                                           Q     
           0   & $ 7                                                                                     Q     

          0   1 8 0                                                                    Q     
           0   & $ 7                                                                                                                              Q     

          0   1 8 0                                               Q     
           0   & $ 7                                                                                                                                                    Q     

          0   1 8 0                                                                    Q     
           0   & $ 7                                                                                                                                                                      Q     

          0   1 8 0                                                                         Q     
           0   & $ 7                                                                Q     

          0   1 8 0                                                                                                   Q     
                                                                                                                                                                                         1 8 0
           0   & $ 7                                                                                                          Q                                                      & $ 7
                                                                                                                                                                       
                                                                                                   $ 8 5 2 & 

Figure 2: Type-2 AUROC2 by model and condition (bootstrap 95% CI). NUM values are modestly
above chance with tight CIs. CAT values for M4, M5, M6, M8 show wide CIs reflecting unreliable
estimates from extreme base-rate imbalance.

4     Discussion
4.1   Summary
Under minimal numeric elicitation with greedy decoding, verbal confidence from seven instruction-
tuned open-weight models in the 3–9B range fails to meet minimal validity criteria. Every model
was classified Invalid on numeric confidence. A 10-class categorical prompt did not rescue validity.
It disrupted task performance. Token-level logprobability did not usefully predict the verbalised
signal. These findings hold across four model families and a reasoning-distilled model.

4.2   Saturation as validity failure
The descriptive pattern is stark before any protocol is invoked. Six of seven instruct models assigned
confidence ≥ 95% on more than 87% of parse-success trials. Two models (M2, M7) produced zero
low-confidence responses across 500+ trials. The confidence output was a constant. The validity
protocol (Appendix A) formalises what the raw distributions already show.
    This is a validity failure, not a calibration failure. The qualification is important: this applies to
the elicited readout under these conditions, not to internal representations. E3 confirms that these
models carry item-level information correlated with confidence (ρ = .50). The information exists.


                                                                                                   6
                                                               0    ' H H S 6 H H N  5   ' L V W L O O    U H D V R Q L Q J  O H Q J W K  Y V  F R Q I L G H Q F H   1 8 0 
                                                                                                                                                                                             ] H U R  R U G H U 
                                                                                                                                                  S D U W L D O   F R Q W U R O O L Q J  L W H P  G L I I L F X O W \ 
                                                                                                                                                                                                                 Q       

                                                        




         9 H U E D O L V H G  F R Q I L G H Q F H
                                                        



                                                        



                                                        
                                                                   & R U U H F W
                                                                   , Q F R U U H F W
                                                                                                                                                                                  
                                                                                                 5 H D V R Q L Q J  W U D F H  O H Q J W K   W R N H Q V 

Figure 3: M8 (DeepSeek-R1-Distill): reasoning-trace length vs. verbalised confidence (NUM). Points
coloured by correctness. The negative slope persists after controlling for item difficulty (ρpartial =
−.36).


It does not survive the verbalised readout under minimal elicitation.
    The saturation observed here is not an intrinsic property of 3–9B models. It is a property of the
model–probe–task interaction under these conditions. Whether richer elicitation can unlock a valid
signal is a separate question.

4.3   Two failure modes
The H4 result reveals two distinct failure modes. Saturation failure (NUM): the model produces
answers and confidence ratings, but confidence is compressed to the ceiling. L ≥ 0.95 in most models.
Interaction failure (CAT): the specific 10-class categorical prompt disrupted question-answering
behaviour. Models that achieve 59–76% accuracy on NUM dropped to 0.2–4.2% on CAT. This is
not evidence that categorical elicitation is inherently flawed. M3 maintained 65.2% accuracy under
the same prompt. This particular prompt is poorly tolerated by most models in this size range.

4.4   AUROC2 and validity
AUROC2 values on NUM range from 0.527 to 0.683. This does not contradict the Invalid classifica-
tion. When 87–97% of trials sit at the ceiling, ranking is driven by 3–13% residual responses. The
validity indices decompose what AUROC2 aggregates over.



                                                                                                                       7
4.5    Deployment implications
Any system using verbal confidence from small open-weight instruct models for abstention, routing,
or safety decisions under minimal elicitation is building on a degenerate signal. Verbal confidence
signals should be screened for validity before calibration or selective prediction metrics are computed.
The protocol (Appendix A) requires only the raw confidence outputs and correctness labels already
available in any benchmark evaluation.

4.6    Limitations
Elicitation regime. One minimal numeric prompt and one 10-class categorical prompt under
greedy decoding. Many real deployments do not use pure greedy decoding. Temperature > 0 may
produce more variable confidence distributions.
    Model scale. 3–9B parameters only. Kumaran et al. [2026] reported graded confidence distri-
butions in Gemma 3 27B.
    Substrate. TriviaQA factual QA only.
    Quantisation. All models at Q5_K_M. Cacioli [2026g] showed AUROC2 is robust to quanti-
sation.
    Categorical prompt. The accuracy collapse may be specific to the 10-class format, its anchor
wordings, or the “NO REASONING” instruction.


5     Pre-registration and data availability
Pre-registered on OSF (registration: https://osf.io/azbvx, locked 15 April 2026; project: https:
//osf.io/xgt73). All data, code, and pre-registration document available on OSF and GitHub
(https://github.com/synthiumjp/koriat). One deviation is disclosed (§2.6). No hypotheses,
thresholds, or decision rules were modified post-registration.


A     Validity Screening Protocol
This appendix provides a self-contained specification of the psychometric validity screening protocol.
The protocol was developed in Cacioli [2026d], specified as a portable procedure in Cacioli [2026e],
and criterion-validated in Cacioli [2026f].

A.1    Input and binarisation
The protocol operates on trials with a correctness label and a confidence value. Continuous confi-
dence is binarised at 0.50, producing a 2×2 contingency table:

                                                        Correct   Incorrect
                           High confidence (≥ 0.50)        a           b
                           Low confidence (< 0.50)         c           d

A.2    Degeneracy pre-check
If the confidence signal has fewer than 3 distinct values or more than 95% of binarised responses
fall in a single category, the signal is classified Invalid (degenerate) without further analysis.



                                                   8
A.3    Validity indices
L = b/(b + d) = P (high confidence | incorrect). L ≥ 0.95: at most 5% error-detection rate.
   Fp = c/(a + c) = P (low confidence | correct). Fp ≥ 0.50: majority of correct trials receive low
confidence.
   RBS = Fp − (1 − L). Positive values indicate directional inversion.
   TRIN = max(nhigh , nlow )/N . Structural indicator; does not trigger Invalid alone.
   r(confidence, correct) = point-biserial correlation. Diagnostic statistic; no classification action.

A.4    Ordered screening sequence
  1. Degeneracy pre-check. If triggered, Invalid.

  2. Cell counts. If any cell < 5, Insufficient.

  3. TRIN. Report value. If ≥ 0.95, structural warning.

  4. Fp . If ≥ 0.50 with Wilson CI lower bound > 0.40, Invalid.

  5. L. If ≥ 0.95 with Wilson CI lower bound > 0.90, Invalid.

  6. RBS. If > 0 with CI excluding zero and point > 0.05, Invalid.

  7. r(confidence, correct). Report value, p, 95% CI.

A.5    Three-tier classification
Invalid. Clear threshold violation. Signal uninformative.
   Indeterminate. Threshold violated but CI includes valid values. Interpret with caution.
   Valid. No threshold violations. Proceed to substantive analysis.


References
Ben-Porath, Y. S. and Tellegen, A. (2020). MMPI-3: Manual for administration, scoring, and
  interpretation. University of Minnesota Press.

Cacioli, J. P. (2026a). Type-2 signal detection for LLM metacognition. arXiv:2603.14893.

Cacioli, J. P. (2026b). Meta-d′ and M-ratio for LLM metacognition. arXiv:2603.25112.

Cacioli, J. P. (2026c). The metacognitive monitoring battery: A cross-domain benchmark for LLM
  self-monitoring. arXiv:2604.15702.

Cacioli, J. P. (2026d). Before you interpret the profile: Validity scaling for LLM metacognitive
  self-report. arXiv:2604.17707.

Cacioli, J. P. (2026e). Screen before you interpret: A portable validity protocol for benchmark-based
  LLM confidence signals. arXiv:2604.17714.

Cacioli, J. P. (2026f). Concurrent criterion validation of a validity screen for LLM confidence signals
  via selective prediction. arXiv:2604.17716.

Cacioli, J. P. (2026g). AUROC2 is format-stable; M-ratio is not. arXiv:2604.08976.

                                                   9
Geng, J. et al. (2024). A survey of confidence estimation and calibration in large language models.
 arXiv:2311.08298.

Joshi, M., Choi, E., Weld, D. S., and Zettlemoyer, L. (2017). TriviaQA: A large scale distantly
  supervised challenge dataset for reading comprehension. In Proceedings of ACL.

Kim, S. (2026). Knowing before speaking: In-computation metacognition precedes verbal confidence
  in large language models. Preprints.org, doi:10.20944/preprints202604.0078.v2.

Kumaran, V. et al. (2026). How do LLMs compute verbal confidence? arXiv:2603.17839.

Miao, N. and Ungar, L. (2026). Closing the confidence-faithfulness gap. arXiv:2603.25052.

Morey, L. C. (1991). Personality Assessment Inventory professional manual. Psychological Assess-
 ment Resources.

Rust, J., Kosinski, M., and Stillwell, D. (2021). Modern Psychometrics (4th ed.). Routledge.

Seo, J. et al. (2026).         ADVICE: Answer-dependent verbalized confidence estimation.
  arXiv:2510.10913.

Steyvers, M. and Peters, M. A. K. (2025). Metacognition and uncertainty communication in humans
  and large language models. Current Directions in Psychological Science.

Steyvers, M., Belem, C., and Smyth, P. (2025). Calibration of LLM confidence. Manuscript.

Tian, K. et al. (2023). Just ask for calibration. arXiv:2305.14975.

Wang, A. and Stengel-Eskin, E. (2026). Calibrating verbalized confidence with self-generated dis-
 tractors (DiNCo). arXiv:2509.25532.

Xiong, M. et al. (2023). Can LLMs express their uncertainty? arXiv:2306.13063.

Yang, Z. (2024). Can LLMs express confidence? The impact of prompt and generation on verbalized
  confidence. arXiv:2412.14737.

Zhao, Y. et al. (2026). Wired for overconfidence. arXiv:2604.01457.




                                                10
