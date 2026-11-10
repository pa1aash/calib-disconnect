---
title: 'Uncertainty Evaluation: Bridging Machine Learning and Measurement Science
  (full text)'
id: uncertainty-evaluation-bridging-machine-learning-and-measurement-science-full-te
tags:
- code-llm-confidence-positioning-d82d00
- full-text
created: '2026-11-09T23:28:13.869007Z'
updated: '2026-11-09T23:31:28.770475Z'
source: https://arxiv.org/pdf/2610.18066
status: draft
type: note
content_type: paper
deprecated: false
summary: 'Petri and Mari (arXiv 2610.18066): conceptual metrology (GUM) analogies
  for ML uncertainty evaluation; critiques aleatoric/epistemic dichotomy; explicitly
  excludes generative ML; no experiments.'
---

1



               Uncertainty Evaluation: Bridging Machine
                 Learning and Measurement Science1
                                                         Dario Petri, Fellow IEEE and Luca Mari 2


Abstract — Reliable uncertainty evaluation is essential for assessing                     decision making and enhance the explainability of the ML
the trustworthiness of machine learning (ML) predictions,                                 system behavior through the systematic evaluation of the
particularly in safety-critical applications. This paper explores                         uncertainty of ML predictions 3 [12]. Accordingly, the evaluation
conceptual analogies between uncertainty evaluation in ML and                             of uncertainty is assuming an increasingly important role in a
measurement science, drawing on the evolution of metrology from
                                                                                          range of different scenarios, including active learning, robustness
error-based approaches to the framework established by the
Guide to the Expression of Uncertainty in Measurement (GUM).                              to data distribution shifts, out-of-distribution detection, and
Particular attention is devoted to the distinction between process-                       learning under data scarcity [10]-[13]. In these contexts, the
level and result-level quality and to the limitations of the                              ability of a ML system to recognize when to defer a decision,
conventional classification of ML uncertainty into aleatoric and                          abstain from prediction, or request additional information is often
epistemic components. It is argued that this dichotomy, similarly                         at least as critical as achieving high predictive accuracy.
to the traditional distinction between random and systematic                                  Once trained, an ML system implements a mapping from
measurement errors, is inherently model-dependent and provides                            input data to inferred class labels or values of a quantity (we do
an insufficient basis for a unified uncertainty evaluation framework.                     not consider here generative ML systems, which would deserve
Further analogies between machine learning and measurement
                                                                                          a different treatment). The trustworthiness of this input-output
field of knowledge are identified concerning distribution shifts,
anomalous operating conditions, and the validity of uncertainty                           relationship is affected by several sources of uncertainty,
evaluation. Building on the proposed considerations, the paper                            including uncertainties in the input data, model parameters and
advocates a metrology-inspired approach based on the systematic                           hyperparameters, limitations inherent in the model architecture,
identification, quantification, and propagation of uncertainty                            and potential weaknesses in the training procedure. This
contributions. By extending the methodology already established                           process exhibits some conceptual analogies with a
in measurement science to ML, this approach could offer a                                 measurement [15]-[17], in which a set of input quantities is
potentially rigorous, consistent, and transferable framework for                          mapped to a measured value, with the resulting output being
evaluating the trustworthiness of individual predictions.
                                                                                          affected by several sources of uncertainty. These analogies can
                                                                                          provide a useful framework for systematically identifying,
Index Terms — Uncertainty, Machine learning, Measurement,
Conceptual analogies, Aleatoric, Epistemic.                                               characterizing, and quantifying the uncertainty contributions
                                                                                          that arise in ML models. Indeed, in the context of measurement
                              I. INTRODUCTION                                             science the trustworthiness of measurement results has been a
                                                                                          widely investigated subject: traditionally addressed in terms of
    In recent years, machine learning (ML) systems have been
                                                                                          measurement errors, more recent approaches have focused on
applied across a wide range of domains involving high-stakes
                                                                                          the evaluation of measurement uncertainty. This evolution is
decision-making, including autonomous driving [1], healthcare
                                                                                          witnessed by the well-established Guide to the Expression of
and medical diagnosis [2]-[4], and climate science [5], [6]. ML
                                                                                          Uncertainty in Measurement (GUM) [18], which provides a
systems have also increasingly become integral components of
                                                                                          general framework for evaluating, and expressing measurement
measuring systems [7]-[9]. In all these application fields it is
                                                                                          uncertainty.
critical to assess and mitigate the risk associated with wrong
                                                                                              This paper is aimed to draw on the lessons learned on this
decisions, and therefore quantifying the trustworthiness of the
                                                                                          matter in the field of metrology and to provide insights and,
results of the inference process performed by trained ML
                                                                                          possibly, guidelines for the evaluation of uncertainty in ML
systems is an important task, which has become an active and
                                                                                          systems, hopefully contributing to the establishment of a
rapidly growing area of research within the ML community
                                                                                          conceptual link between metrology and ML. Section 2
[10]-[14]. Possibly also by taking what has been learned on the
                                                                                          introduces the general problem of evaluating the quality of a
subject in the context of measurement science, an emerging
                                                                                          product from the quality of the process by which it is produced,
trend in ML is about modeling trustworthiness in terms of
                                                                                          considering both measurement and ML prediction as instances
uncertainty: the aim is mainly to support both risk-aware

1
    This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.
2
    This paper was submitted for review on October 12, 2026.
    Dario Petri is with the Department of Industrial Engineering of the Università di Trento, Trento, Italy (e-mail: dario.petri@unitn.it).
    Luca Mari is with the Department of Philosophy of the Università Cattolica di Milano, Milano, Italy (e-mail: luca.mari@unicatt.it).
3
    A linguistic note: in ML, the term “prediction” is used independently of a temporal connotation, thus also for past or present events, and for referring to both the
    process of a trained system and the results it produces; in the present paper the context is sufficient to make the intended meaning clear.
                                                                                                                                        2

of such processes. Sections 3 and 4 discuss how measurement          be carefully observed. This enables the quality of both the
science has addressed this issue, with emphasis on the evolution     process and of its individual products to be reliably evaluated
from the traditional distinction between random and systematic       by comparing the observed outcomes with the corresponding
measurement errors, highlighting the reasons that led to the         reference values or expected outcomes. Under field or
transition from the error-based approach to one based on             deployment conditions, however, the references required to
measurement uncertainty, as established in the International         apply such a comparative evaluation to any individual product
Vocabulary of Metrology (VIM) [19]. Section 5 reviews and            are usually not available. Consequently, the quality of that
critically analyzes the basic criteria adopted for uncertainty       product cannot, in general, be assessed using the same
modeling and evaluation in ML, highlighting the analogies with       reference-based strategy.
the traditional distinction between random and systematic                This leads us to a distinction that is central to the present
errors. Section 6 discusses the parallels between measurement        analysis:
and ML prediction when operating conditions differ from those        – process-level quality: information about a process, obtained
expected. Section 7 summarizes the main findings emerging                by studying its behavior under a specified set of controlled,
from the comparison between the two bodies of knowledge.                 calibration, validation, or test conditions;
Finally, Section 8 proposes some relevant concluding remarks.        – product-level quality: information about a product, which
                                                                         must be obtained, at least partly, from the specific
                 II. A GENERAL PROBLEM:                                  conditions under which it is actually generated.
        FROM PROCESS QUALITY TO PRODUCT QUALITY?                         Although the two levels are closely related, they are distinct
                                                                     and should not be conflated.
    When a process is designed and operated to generate
products – either material or informational –, it may be                      III. MEASUREMENT AS A PARADIGMATIC CASE
appropriate to obtain not only the product itself but also
information about its quality. This creates a general problem,           Measurement provides a particularly clear instance of this
with both epistemic and operational dimensions: how can the          problem. A measuring system is expected to be calibrated and
information about the quality of a process be translated into        tested by comparison with suitable measurement standards
information about the quality of each individual product             under controlled conditions. These procedures contribute to set
generated by that process?                                           and characterize the behavior of the system and provide
    Indeed, the quality characteristics of a process provide         information about features such as system sensitivity, selectivity,
information about the quality of every individual product            and stability, which collectively contribute to its accuracy. For
obtained by that process, but they do not fully determine it. A      a measurement performed under field conditions, however, a
process can be studied under controlled and repeatable               reference value for the measurand (ideally its “true value”) is
conditions, thereby enabling the characterization of its typical     usually unavailable. Indeed, establishing such a reference would
behavior, intrinsic limitations, and sensitivity to relevant         require a higher-quality measurement of the same measurand, a
influence factors. In contrast, each individual product is           condition that is seldom fulfilled as it may be technically
obtained under specific operating conditions, and its quality        infeasible or just too costly. Hence, although the notion of
depends both on the process and on the particular input,             accuracy (and the error) of a measurement result remains
environment, operating state, and other contingent conditions        theoretically meaningful, it cannot generally be operationalized.
under which it is produced. Such factors may cause the quality           For this reason, in the last few decades measurement science
of an individual product to fall below what would be expected        has developed a different approach towards the evaluation of
from the characteristics of the process. Hence, though               the quality of measurement results. Rather than considering the
exceptions may occur, process quality can generally be               unknown, and usually unknowable, error, this approach focuses
regarded as an upper bound on product quality. Information           on how strongly, and on what evidential basis, a measurement
about process quality must therefore be transferred to the           result is warranted by the available prior information, about
individual product and, where appropriate, revised to account        both the process and the measurand, as well as that acquired
for the specific conditions under which the product is generated:    through the measurement itself. Taken together, these sources
nominal or reference characteristics of the process are relevant     of information contribute to establishing the trustworthiness of
evidence for assessing the quality of an individual product, but     the result, without reducing it to a matter of subjective trust. Most
are not, by themselves, sufficient to provide a complete             probably for continuity with the tradition about measurement
characterization of it.                                              error – which is inherently a “negative” concept – such concept
    The case of accuracy is especially instructive in this regard.   of trustworthiness has been called “measurement uncertainty”
In general terms, accuracy concerns the degree of agreement          instead of, for example, “measurement certainty” or
between an actual process behavior or product and the                “measurement public trust”. It is important, however, to
corresponding expected or reference process behavior or              emphasize that the concepts of error and uncertainty should not
product. Accuracy thus plays an inverse role with respect to         be conflated, as they refer to fundamentally different notions.
error: accuracy is generally improved by reducing or removing        Indeed, unlike error, measurement uncertainty is currently defined
causes of error. Under laboratory or validation conditions,          by the VIM as a “non-negative parameter that characterizes the
suitable references may be available and the actual products can     dispersion of quantity values that can reasonably be attributed
                                                                                                                                     3

to the measurand, on the basis of the available information”         temperature. As long as the influence of temperature on the
[19]. Thus, measurement uncertainty quantifies the extent to         sensor output is not explicitly modeled, the resulting effect may
which the information obtained about the measurand is supported      be considered as a random contribution. Once this dependence
by the available evidence: as such, it is acknowledged to be an      is taken into account in the measurement model and the
essential component of the measurement result.                       temperature is measured, the corresponding effect becomes
    In summary, the accuracy of a measurement (regarded here         systematic and can, at least in principle, be compensated for.
as a process-level quality feature) contributes, inversely, to       The residual effect due to uncertainties in both the
measurement uncertainty (intended as a product-level quality         compensation relationship and the measured temperature can be
feature). This contribution is sometimes referred to as              classified as a random contribution. As another example,
“instrumental measurement uncertainty”. For an individual            consider an ideal quantizer driven by a pure sine wave. Since
measurement, performed under specific here-and-now                   both the input signal and the applied transformation are
conditions, however, instrumental uncertainty is only one of the     deterministic, the quantization error can, in principle, be
several sources contributing to measurement uncertainty,             determined exactly and thus it exhibits systematic behavior. In
though sometimes dominating.                                         practice, however, it is often advantageous to model the
                                                                     quantizer using a simple linear input/output transformation and
IV. THE METROLOGICAL TRANSITION FROM ERROR TO UNCERTAINTY            to treat the error as a random quantity [20].
    The transition from an error-centered approach to an                 For these reasons, and following a seminal recommendation
uncertainty-centered approach did not merely entail a                of a working group convened in 1980 by the Bureau
replacement of one numerical indicator with another: rather it       International des Poids et Mesures (BIPM) and then revised
involved a change in the conceptual framework used to model          and adopted by the Comité International des Poids et Mesures
and organize the quantification of measurement                       (CIPM), the GUM uncertainty framework reverses the strategy.
trustworthiness. This change is characterized in terms of three      Specifically, it first establishes a requirement for a common
main structural components of a quality-evaluation framework:        quantitative representation of partial indicators (and hence for
C1. identification of the sources that may affect the quality of     C2), typically expressed as standard deviations or more
     the result;                                                     generally as probability distributions. Indeed, as stated in [18],
C2. for each source, evaluation of its contribution to the quality   “categorizing the methods of evaluating uncertainty
     of the result;                                                  components rather than the components themselves avoids [the
C3. combination of the individual contributions into an overall      mentioned] ambiguity. At the same time, it does not preclude
     indicator characterizing the quality of the result.             collecting individual components that have been evaluated [...]
                                                                     into designated groups to be used for a particular purpose”.
    The traditional approach focused on C1 by interpreting               The GUM subsequently classifies uncertainty contributions
measurement error as the deviation of the measured value from        according to the methods used for their evaluation: Type A
the true value and by classifying its contributing sources as        evaluation uses statistical analysis of series of measured values,
random errors or systematic errors, according to their behavior.     whereas Type B evaluation employs methods other than those for
However, this source-behavior based categorization was               Type A evaluation, and then typically relies on prior available
subsequently abandoned for at least two main reasons. First,         information, such as calibration certificates, specifications,
when measuring, the true value of the measurand could not be         previous data, models, or expert knowledge [18]. Accordingly,
unique, as occurs when the definitional uncertainty is non-null.     Type A and Type B do not identify two different kinds of
Moreover, it is usually unknown and in practice unknowable           uncertainty, nor do they reproduce the distinction between
with certainty, making the evaluation of measurement error           random and systematic errors: rather, they distinguish the
infeasible. Second, as acknowledged by the GUM (even if the          methods used for evaluating uncertainty sources / components.
quoted text already considers uncertainty, not error), “such             Hence, within the GUM framework, C1 and C2 lead to the
categorization of components of [error] can be ambiguous when        construction of an uncertainty budget, which provides the basis
generally applied. For example, a ‘random’ component of              for C3. At this stage, the individual uncertainty contributions
[error] in one measurement may become a ‘systematic’                 are combined through the law of propagation of uncertainty,
component of [error] in another measurement in which the             often based on a first-order Taylor approximation, or by
result of the first measurement is used as an input datum.” [18].    propagating the associated probability distributions, typically
Moreover, distinguishing between ‘being random’ and ‘being           by means of Monte Carlo methods. Thus, classifying
systematic’ revealed to be a problematic starting point to           uncertainty contributions according to the methods used for
consistently derive general solutions to C2 and then C3. Indeed,     their evaluation, rather than according to their behaviors,
the random-systematic categorization is not an inherent              provides an effective and operational means of avoiding the
property of an error source, as it may depend on the model           ambiguities discussed above. A further important feature of this
adopted to describe the measurement and its context.                 framework is that prior information concerning the
    Some examples may explain how an error source can                measurement process is retained and employed into the
exhibit either random or systematic behavior depending on how        uncertainty evaluation: calibration results, instrument
it enters on the adopted measurement model. Consider an              specifications, and knowledge of typical measurement-system
accelerometer whose response depends on the environmental            behavior become inputs to the evaluation of the uncertainty for
                                                                                                                                              4

a particular measurement result by integrating them with result-            probabilistic prediction, Bayesian inference, ensemble
specific information about the actual measurement conditions.               methods, prediction intervals, conformal prediction, calibration
Measurement uncertainty can thus be regarded as a result-specific           techniques, and out-of-distribution detection already address
synthesis of heterogeneous, but relevant sources of information.            several important aspects of the problem. Rather, the open issue
    This does not preclude the identification of contributions              is whether these methods can be integrated into a more general,
according to whether they affect the variability of the measured            process-aware but result-centered framework, analogous to the
values in either a random or systematic way, a distinction that             one developed in measurement science for the modeling,
remains useful for supporting practical decisions concerning                evaluation, and expression of uncertainty. In this context, the
uncertainty-reduction strategies. For example, the effect of                conceptual evolution of measurement science from the traditional
contributions exhibiting random behavior can be mitigated                   error-based approach to the current uncertainty-based paradigm
through averaging, whereas those exhibiting systematic                      may provide useful insights and possibly methodological
behavior can be reduced through calibration, compensation, or               guidelines for developing a systematic framework for the
redesign of the measuring system.                                           characterization of the quality of individual ML prediction results.
                                                                                To quantify and, where possible, reduce predictive uncertainty,
 V. THE AN ANALOGY BETWEEN MEASUREMENT AND MACHINE                          considerable attention in the ML literature has been devoted to
                       LEARNING INFERENCE                                   distinguishing distinct sources of uncertainty according to their
    The transition from development to deployment of ML                     underlying nature. This approach is analogous, to some extent,
systems raises issues that are structurally similar to those                to the traditional classification of random and systematic error
encountered in measurement, particularly regarding the                      contributions adopted in measurement science. In fact,
requirement of shifting from process-level to product-level                 predictive uncertainty is commonly categorized into two main
quality of information. Indeed, during the development stage,               components [21]:
in particular training and validation, the results produced by a            – aleatoric or data uncertainty, which refers to the variability
ML system can be compared against reference data,                               of outcomes that remains even when the input-output
analogously to the comparison with reference values performed                   relationship is adequately known, typically modeled as
during the metrological characterization and calibration of a                   stochastic variability in the data-generating process;
measuring instrument. Performance indexes such as accuracy,                 – epistemic or model uncertainty, which arises from
precision, sensitivity, and specificity can then be exploited to                incomplete or inadequate knowledge of the underlying
evaluate the overall quality of the system over a validation                    input-output relationship; this component may result from
dataset, under assumptions concerning the representativeness                    limitations in the availability or quality of training data,
of that dataset. At deployment time, however, the system                        restrictions imposed by the adopted model class or architecture,
produces a result for a new case, precisely because the correct                 deficiencies in the training process, such as underfitting, or
label or value is typically unavailable. Consequently, the accuracy,            discrepancies between the conditions represented in the
or the error, of that particular result cannot generally be                     training data and those encountered during prediction.
computed. Although aggregate performance indexes obtained                       The rationale behind this categorization is that it should
during validation remain informative, they are insufficient to              provide useful guidance to support predictive confidence
determine the quality of the provided information. Indeed, the              assessment and model refinement by distinguishing between
quality of a result may be affected by input ambiguity, atypical            potentially reducible and inherently irreducible uncertainty
observations, data acquisition problems, or discrepancies                   sources. Specifically, epistemic uncertainty is considered
between the operating conditions encountered during deployment              reducible, at least in principle, through the acquisition of
and those considered in the training data.                                  additional training data or the adoption of a more suitable model
    The parallel between calibration and measurement on the                 class. Conversely, aleatoric uncertainty is generally regarded as
one hand and ML training and prediction 4 on the other hand is              irreducible because it is assumed to be intrinsic to the
then manifest:                                                              considered data [10], [11], thus under the assumption that the
– under calibration/training and validation conditions,                     inputs to be processed are given, instead of being a sample
    reference values (i.e., values operationally accepted as true           whose cardinality could be increased.
    labels or true values) are available, so enabling the                       However, despite its widespread adoption, this categorization
    evaluation of process-level information quality;                        has not yet led to the establishment of a unified framework for
– under field/deployment conditions, the reference value                    uncertainty evaluation in ML, and it remains conceptually
    associated with each individual result is generally                     ambiguous and has been subject to several criticism, including
    unavailable, so that the quality of the provided information            the following:
    can only be characterized indirectly.                                   – analogously to the classical distinction between random and
   The distinction does not imply that ML lacks established                     systematic errors in metrology, this categorization is not
methods for uncertainty evaluation. Approaches such as                          inherent to uncertainty sources themselves, but it depends
                                                                                on the chosen model, the training procedure, and the

   4
     Note that both training and prediction are inferential processes, of
a model and a result respectively.
                                                                                                                                             5

  information used; this dependence leaves room for arbitrary           remains unchanged [22], [23]. In this case, the input data may
  interpretations and inconsistent applications [14]; for               still remain within the support of the training distribution, but it
  example, the assumption that aleatoric uncertainty is                 could be shifted toward lower data density regions, potentially
  inherently irreducible overlooks the model-dependent                  resulting in higher epistemic uncertainty. Typical examples of
  nature of its propagation through the system [10], [11];              distribution shift include language models applied to texts
– the absence of universally accepted definitions of the two            exhibiting writing styles insufficiently represented in the
  types of uncertainty has led to the development of a wide             training corpus, or computer vision systems trained primarily
  variety of statistical indexes for their quantification [14];         on daytime images and subsequently deployed under nighttime
  this lack of standardization makes it difficult, if not infeasible,   conditions. In both cases, the input data remains within the
  to establish meaningful comparisons among the various                 same semantic domain as the training data, and nevertheless the
  uncertainty evaluation methods proposed in the literature,            prediction could be biased.
  thereby hindering their systematic assessment and further                  In these scenarios, the assumed measurement or ML model
  advancement;                                                          remains fundamentally valid and the information provided is
– the aleatoric–epistemic categorization may not adequately             still meaningful. Nevertheless, the associated confidence may
  capture the reducible and irreducible components of                   decrease due to uncompensated systematic effects in measurement
  prediction uncertainty, highlighting the need for more                or distribution shift–induced uncertainty in ML.
  refined uncertainty classifications that explicitly include the
  influence of the adopted model and training procedure [14];           B. Anomalous operating conditions
– the conventional interpretation of aleatoric uncertainty as
                                                                            Another conceptual analogy between measurement and ML
  inherently irreducible may encourage premature acceptance
                                                                        emerges when anomalous inputs (i.e., observations that are
  of existing uncertainty levels, potentially discouraging
                                                                        inconsistent with the assumed model) occur. In metrology, such
  deeper investigation into their underlying causes and
                                                                        observations are commonly associated with gross errors, whereas
  limiting opportunities for model refinement and
                                                                        in ML they correspond to out-of-distribution (OOD) inputs.
  performance improvement.
                                                                            In the measurement practice, a gross error typically arises
    Further interesting uncertainty-related analogies between           from instrument malfunction, human mistakes, or an incorrect
metrology and ML emerge when changes in the system                      experimental setup. Since these events do not conform to the
operating conditions occur or when the input data deviates from         assumed measurement model, they may invalidate any uncertainty
the assumptions underlying the adopted data-generating model.           evaluation based on that model. Similarly, in ML, OOD inputs
These aspects are discussed in greater detail in the following          are semantically different from the training data. Unlike
Section.                                                                distribution shift considered above, OOD data originates from
                                                                        different semantic domains or involve previously unseen classes,
VI. ANALOGIES BETWEEN MEASUREMENT AND MACHINE LEARNING                  thereby violating the assumptions under which the model was
   INFERENCE UNDER MISMATCHED OPERATING CONDITION                       trained [22], [23]. As a result, the model may confidently
    Both measurement and ML processes may be affected by                provide predictions that are in fact meaningless, given that the
variations in input data, environmental conditions, and/or              model lacks any information basis to interpret such inputs. As
operating conditions. Such variations may challenge the                 an illustrative example, consider an ML system trained
assumptions underlying system development, potentially                  exclusively on sequences of English words: for such a system,
compromising, either partially or completely, the validity and          most Italian sentences constitute OOD inputs, despite being
reliability of the provided information. Some relevant                  syntactically valid linguistic expressions, since their characteristics
conceptual analogies between the issues that arise in the two           are not adequately represented in the training distribution.
knowledge domains are examined in the following Subsections.                Thus, gross errors in measurement and OOD inputs in ML
                                                                        play analogous conceptual roles: both represent violations of the
A. Dataset or operating condition shift                                 assumed data-generating model. Consequently, the identification
                                                                        of uncertainty components (e.g., random vs. systematic effects,
    In the measurement practice, such situations may arise, for         or aleatoric vs. epistemic sources) as well as the uncertainty
example, from uncompensated systematic effects associated               evaluation are meaningless. Also, treating OOD inputs or gross
with influence quantities that exceed their specified allowable         errors merely as highly uncertain but valid data (e.g., by
ranges. Another representative example is the use of a                  modeling them as random effects and averaging them) would
measuring instrument beyond the validity period of its                  lead produce unreliable results that may lead to critical or even
calibration certificate. Under these circumstances, the                 catastrophic failures.
underlying measurement model may remain conceptually valid,                 It follows that, for ensuring the reliability of the information
while its accuracy deteriorates because relevant effects are no         provided by either measurement or ML systems, a two-step
longer properly accounted for.                                          procedure is required [24]:
    A similar situation occurs in ML when prediction is                 1. Model scope verification (i.e., gross errors or OOD detection):
performed on input data whose distribution differs from that of             the goal of this step is the identification of anomalous inputs
the training set, while the underlying data-generating process              that violate the assumptions underlying the adopted model;
                                                                                                                                                       6

   such inputs should be detected and rejected rather than                  Table II. Comparison of the behavior of measurements and machine learning
                                                                            inferences under operating conditions that violate the assumptions underlying
   processed using a model that is not applicable to them;
                                                                            the respective adopted models.
2. System output and uncertainty assessment: only after verifying
   that the input data is consistent with the assumptions and                    operating
   validity domain of the adopted model, the system output                       conditions             measurement            machine learning
   should be provided and its uncertainty evaluated; this ensures                mismatch
   that the resulting uncertainty is meaningfully evaluated.
                                                                                                       uncompensated            distribution shift,
                                                                                dataset or
    Finally, it is worth observing that gross errors in                                               systematic effects,           increased
                                                                                 operating
measurement may indicate not only instrument or procedural                                                 increased                epistemic
                                                                              conditions shift
failures, but also previously unrecognized physical phenomena,                                            uncertainty              uncertainty
potentially motivating the development of new measurement                        anomalous                                     out-of-distribution
models or new theoretical frameworks. Analogously, while                                                 gross error,
                                                                                  operating                                           data,
some OOD inputs should be rejected, others may represent                                                rejected input
                                                                                 conditions                                      rejected input
novel but legitimate data, thereby motivating model extension
or retraining. In both domains, the decision to reject anomalous
                                                                                                      VIII. CONCLUSIONS
observations or incorporate them through model updating depends
on the available prior knowledge, the underlying causes of the                  Limitations of the uncertainty evaluation approach currently
observed deviations and the specific application context.                   applied in ML can be more clearly interpreted when examined
                                                                            through the lens of the metrological framework for uncertainty
                           VII. SUMMARY                                     evaluation. In particular, the widespread aleatoric–epistemic
                                                                            dichotomy exhibits strong conceptual similarities to the
    The preceding analysis about the different approaches                   traditional distinction between random and systematic errors
employed in metrology and ML for uncertainty evaluation is                  employed in the pre-GUM metrology framework. The main
summarized in Table I, which provides a comparative overview                weakness of that distinction is that it is not intrinsic to the
of their main characteristics.                                              uncertainty sources, but rather it depends (either implicitly or
                                                                            explicitly) on the adopted model, the training procedure, and
Table I. Comparison of the main characteristics of uncertainty evaluation
approaches adopted in metrology and machine learning.                       the information used. Consequently, individual uncertainty
                                                                            contributions may shift from one class to the other depending
   classification                                                           on changes in the model structure, training methodology, or
                         measurement             machine learning
     criterion                                                              information available, in direct analogy with the context-
                       statistical (type A)      aleatoric or data          dependent interpretation of random and systematic errors in
    uncertainty            evaluation;              uncertainty;            measurement science.
      classes         other than statistical    epistemic or model
                                                                                This situation parallels the one that motivated the GUM to
                      (type B) evaluation           uncertainty
                                                                            move beyond the traditional error-based classification in favor
    theoretical                                                             of a unified probabilistic framework for uncertainty modeling,
                       probability theory        probability theory
    framework
                                                                            evaluation, and expression grounded in the kind of use of the
    criterion                                                               available information rather than the presumed nature of
                           evaluation          evaluation, reduction
 motivated by …                                                             uncertainty sources. In addition, the coexistence in ML of
                     adopted measurement                                    multiple, non-equivalent statistical description for uncertainty
                             model,                                         modeling and evaluation contrasts with the standardized and
  result depends                                adopted data model
                           measuring                                        internally consistent methodology established by the GUM.
      on …                                      and training process
                      instruments quality,
                       calibration process                                  Within this framework, all recognized sources of uncertainty,
                                                                            regardless of their origin, are represented through appropriate
    uncertainty       standard uncertainty,
                                                   not univocally           probability distributions, conditional on the specified
  representation      expanded uncertainty,
                                                      defined               measurement conditions, and propagated through the
     approach                  pdf
                                                                            measurement model to achieve the combined uncertainty of the
  combination of       standardized rules
    uncertainty             based on
                                                   not univocally           measurement result.
                                                      defined                   Finally, the common ML interpretation of aleatoric
   components          probability theory
                                                                            uncertainty as irreducible and epistemic uncertainty as reducible
                                                                            may be seen as an oversimplification when considered from a
    The main findings concerning the conceptual analogies
                                                                            metrological perspective. In metrology, uncertainty reduction is
between the behavior of measurements and ML predictions
                                                                            not simply based on categorical classification, but on a
under operating conditions that violate the assumptions
                                                                            systematic analysis of individual uncertainty contributions and
established during system development are summarized in
                                                                            their propagation through the measurement model. This
Table II.
                                                                            approach enables the identification and quantification of the
                                                                            relevant contributions, as well as the assessment of potential
                                                                                                                                                                 7

strategies for their mitigation, including improved modeling,                       [18] JCGM 100:2008, Evaluation of measurement data – Guide to the expression of
                                                                                         uncertainty in measurement (GUM), 2008 [Online]. Available:
refined calibration procedures, and/or measuring system redesign.                        https://www.bipm.org/en/doi/10.59161/JCGM100-2008E.
    In conclusion, we argue that shifting beyond the binary                         [19] JGCM 200:2012, International Vocabulary of Metrology (VIM) – Basic
classification of aleatoric and epistemic uncertainty toward a                           and General Concepts and Associated Terms, 2012 [Online]. Available:
GUM-inspired framework, grounded on the systematic                                       https://www.bipm.org/en/doi/10.59161/JCGM200-2012.
identification, quantification and propagation of all recognized                    [20] M. Bertocco, C. Narduzzi, P. Paglierani, D. Petri, “A noise model for
                                                                                         digitized data,” IEEE Trans. Instrum. Meas., 49, 1, 2000.
uncertainty contributions, could provide a more rigorous and
consistent basis for uncertainty evaluation in ML. Furthermore,                     [21] E. Hüllermeier, W. Waegeman, “Aleatoric and epistemic uncertainty in
                                                                                         machine learning: an introduction to concepts and methods,” Machine
from this framework ML could draw some pragmatic                                         Learning, 110, 457-506, 2021.
guidelines about the identification of the uncertainty boundaries                   [22] S. Farquhar, Y. Gal, “What ‘Out-of-distribution’ Is and Is Not,” Machine
for an appropriate information-enabled decision-making, as                               Learning Safety Workshop, 36th Conference on Neural Information
modeled in metrology in terms of definitional uncertainty and                            Processing Systems (NeurIPS) 2022.
target uncertainty [19], [25], [26]. Such an approach could                         [23] N. Kotelevskii, et coll., “From Risk to Uncertainty: Generating
                                                                                         Predictive Uncertainty Measures via Bayesian Estimation,” The
promote the development of more reliable, transparent and                                Thirteenth International Conference on Learning Representations, ICLR
transferable uncertainty evaluation methods, while supporting                            2025.
a more systematic assessment of opportunities for uncertainty                       [24] Z. Zhou, et coll., “Fixing Robust Out-of-distribution Detection for Deep
reduction.                                                                               Neural Networks,” IEEE 34th International Symposium on Software
                                                                                         Reliability Engineering (ISSRE), 2023.
                                                                                    [25] D. Petri, P. Carbone, L. Mari, “Quality of measurement information in
                                REFERENCES                                               decision-making,” IEEE Trans. Instr. Meas., 70, 1-16, 2021.
[1]   B. Araújo, J.F. Teixeira, J. Fonseca, R. Cerqueira, S.C. Beco, “The Road      [26] L. Mari, D. Petri, “The metrological culture in the context of big data:
      to Safety: A Review of Uncertainty and Applications to Autonomous                  Managing data-driven decision confidence,” IEEE Instrum. Meas.
      Driving Perception,” Entropy, 26(8), 634, 2024.                                    Magazine, 20, 5, 2017.
[2]   D. Shen, G.Wu, H. Suk, “Deep Learning in Medical Image Analysis,”
      Annual review of biomedical engineering, 19:221-248, 2017.
[3]   G. Litjens, et coll. “A Survey on Deep Learning in Medical Image Analysis,”
      Medical image analysis, 42:60-88, 2017.
[4]   L.J. Lechuga Lopez, et coll., “Uncertainty Quantification for Machine
      Learning in Healthcare: A Survey,” Proc. sixth Conference on Health,
      Inference, and Learning, PMLR 287:862-907, 2025.
[5]   C.O. de Burgh-Day, T. Leeuwenburg, “Machine Learning for Numerical
      Weather and Climate Modelling: A Review,” Geoscientific Model
      Development, 16, 22, 2023.
[6]   K. Kashinath, et coll. “Physics-informed Machine Learning: Case
      Studies for Weather and Climate Modelling.” Philosophical Transactions
      of the Royal Society A, 2021.
[7]   T. Adel, S. Bilson, M. Levene, A. Thompson, “Trustworthy Artificial
      Intelligence in the Context of Metrology,” arXiv:2406.10117v1, 2024.
[8]   H. Rabus, et coll., “Metrology for Artificial Intelligence in Medicine,”
      Measurement: Sensors 38, 2025.
[9]   A. Thompson, et coll., “Uncertainty Evaluation for Machine Learning,”
      NPL Report MS 34, 2021.
[10] W. He, et coll., “A Survey on Uncertainty Quantification Methods for Deep
     Learning,” arXiv:2302.13425v5, 2024.
[11] J. Gawlikowski, et coll., “A Survey of Uncertainty in Deep Neural
     Networks,” Artificial Intelligence Review, 2023.
[12] D. Kaur, S. Uslu, K.J. Rittichier, A. Durresi, “Trustworthy Artificial
     Intelligence: A Review,” ACM Computing Surveys, 55, 2, 39, 2022.
[13] M. Abdar, et coll., “A Review of Uncertainty Quantification in Deep
     Learning: Techniques, Applications and Challenges,” Information
     Fusion, 76, 2021.
[14] F. Bickford Smith, et coll., “Rethinking Aleatoric and Epistemic
     Uncertainty,” 42nd International Conference on Machine Learning,
     2025.
[15] L. Mari, P. Carbone, D. Petri, “Measurement fundamentals: A pragmatic view,”
     IEEE Trans. Instrum. Meas., 61, 8, 2012.
[16] L. Mari, P. Carbone, A. Giordani, D. Petri, "A structural interpretation
     of measurement and some related epistemological issues," Studies in
     History and Philosophy of Science Part A, 65-66, 2017.
[17] D. Petri, L. Mari, “Learning Lessons from the Analogies between
     Measurement and Machine Learning Life Cycles,” IEEE Intern. Instrum.
     Meas. Tech. Conference (I2MTC), Nancy, France, May 25-28, 2026.
