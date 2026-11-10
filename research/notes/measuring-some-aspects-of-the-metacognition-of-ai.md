---
title: Measuring (some aspects of) the metacognition of AI
id: measuring-some-aspects-of-the-metacognition-of-ai
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
- framing-f
- metacognition
- meta-d-prime
created: '2026-11-09T23:08:05.587558Z'
updated: '2026-11-09T23:27:44.415250Z'
source: https://arxiv.org/html/2603.29693
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:05.583559Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Servajean and Servajean (RIKEN/AIST and Paul-Valery Univ., arXiv 2603.29693v4,
  28 Sep 2026, full text via HTML). Methodological paper arguing that common measures
  of AI metacognitive sensitivity (AUROC-style discrimination of correct from incorrect
  via confidence) are confounded by type 1 task performance, and advocating meta-d'
  / M-ratio from signal detection theory plus SDT-based type 1 criterion shifts under
  risk configurations. Demonstrated on GPT-5, DeepSeek-V3.2-Exp, Mistral-Medium-2508
  with three non-code tasks (SST-2 valence, oral vs written, deleted 'the'). Explicitly
  states 'our article is not a benchmark paper' and makes no claims about genuine
  metacognition. Occupies the measurement-theory framing of confidence sensitivity
  as an instrument problem for LLMs generally, but nothing on code, execution ground
  truth, hidden states, or metrology (traceability, uncertainty budgets). Relevant
  to F as the nearest psychometric framing.
---

Measuring (some aspects of) the metacognition of AI
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2603.29693v4 [cs.AI] 28 Sep 2026
Measuring (some aspects of) the metacognition of AI
Richard Servajean
Email:
rservajean@yahoo.fr
Affiliation:
Center for Brain Science, RIKEN, Saitama, Japan
Affiliation:
Current address: National Institute of Advanced Industrial Science and Technology (AIST), Tokyo, Japan
Philippe Servajean
Email:
philippe_gi@hotmail.fr
Affiliation:
Department of Psychology, Paul-Valéry University, Montpellier, France
Abstract
A robust decision-making process must take into account uncertainty, especially when the choice involves inherent risks. Because artificial intelligence (AI) systems are increasingly integrated into decision-making workflows, managing uncertainty relies more and more on the metacognitive capabilities of these systems; i.e, their ability to assess the reliability of and regulate their own decisions. Hence, it is crucial to employ robust methods to measure the metacognitive abilities of AI. This paper is primarily a methodological contribution that highlights a key limitation of commonly used measures of AI
metacognitive sensitivity
—the ability to generate confidence ratings that distinguish correct from incorrect responses. We then draw attention to the meta-
d
′
\mathchar 29028^{\mathchar 560}
framework, a well-established approach from psychology and neuroscience designed to address this limitation. Moreover, we propose to leverage
signal detection theory
(SDT) to measure the ability of AIs to spontaneously regulate their decisions based on uncertainty and risk. To demonstrate the practical utility of these psychophysical frameworks, we conduct two series of experiments on three large language models (LLMs)—GPT-5, DeepSeek-V3.2-Exp, and Mistral-Medium-2508.
†
†
equal-contributors:
These authors contributed equally to this work.
†
†
equal-contributors:
These authors contributed equally to this work.
1
Introduction
It is widely acknowledged that artificial intelligence (AI) is transforming our societies
Makridakis (2017)
;
Stone et al. (2022)
, in fields as diverse as education
Hwang and Chang (2023)
and protein structure prediction
Jumper et al. (2021)
. In particular, since the release of GPT-3.5 in 2022
OpenAI (2022)
, the massive adoption of conversational chatbots based on large language models (LLMs) by the public in their daily lives
Topics (2025)
has reignited debates about the opportunities and risks posed by AI
Weidinger et al. (2021)
;
Rillig et al. (2023)
. This has motivated many researchers to test the current capabilities of AI systems across a broad range of tasks, and specifically those of conversational chatbots
Chang et al. (2024)
.
As AI systems are increasingly deployed across society, we identify three ways in which they can be incorporated into a decision process:
1.
AI decision-making:
The AI system operates alone without any human intervention. An example of this would be autonomous driving at Level 4 or 5 (as defined by the SAE J3016 standard
Committee (2021)
), denoting systems that require no human oversight.
2.
Human-AI joint decision-making:
the AI system and humans take a decision as co-agents. One example is a setting in which the final decision results from a combination of human and AI judgments
Steyvers et al. (2022)
.
3.
AI-assisted decision-making:
the AI system makes recommendations that are ultimately approved, refined, or ignored by a human. An example of this would be AI-powered medical diagnostics, where the system flags potential abnormalities in scans and forwards them to a radiologist who is responsible for making the final medical conclusion
Castilla et al. (2025)
.
It should be noted that these categories only serve as primary landmarks along a broader continuum, reflecting the vast diversity of possible human-AI interaction patterns. See Ref.
Gomez et al. (2025)
for a review of human-AI interaction patterns identified in the literature. Regardless, an effective decision-making process requires taking
uncertainty
into account
Platt and Huettel (2008)
;
Li and Steyvers (2025)
. Here, uncertainty concerns the probability that a judgment or a prediction (e.g., regarding the outcome of a choice) is correct. When uncertainty and risks are high, the most effective strategy is often to suspend judgment and prioritize further data collection before making the final decision (see the
exploration-exploitation dilemma
Berger-Tal et al. (2014)
;
Mehlhorn et al. (2015)
). Furthermore, in some decision-making contexts, the available options may differ considerably in the magnitude of their associated risks and/or benefits. In such cases, accounting for uncertainty becomes critically important. For instance, even a marginal amount of uncertainty regarding a catastrophic outcome can be enough to warrant an alternative choice that is more uncertain but offers lower risks in the failure scenario. Finally, in some multi-agent (human-human, human-AI or AI-AI) joint decision-making, quantifying the uncertainty of each agent’s prediction provides a principled way to arbitrate between divergent forecasts
Bahrami et al. (2010)
;
Steyvers et al. (2022)
;
Nguyen et al. (2025)
;
Bhattacharyya et al. (2024)
;
Koriat (2012)
. Overall, note that researchers from fields as diverse as game theory
Von Neumann and Morgenstern (2007)
, computational neuroscience
Parr et al. (2022)
and machine learning
Vo et al. (2019)
have investigated the question of finding optimal strategies within uncertain contexts.
Crucially, managing uncertainty poses unique challenges, depending on how AI systems are incorporated into decision processes. In the
AI decision-making
scenario, AI systems operate autonomously. The challenges therefore concern the ability of AI systems to estimate uncertainty and adjust their decisions accordingly. Here, the role of humans is limited to providing preliminary information, such as acceptable risk thresholds. In contrast,
human-AI joint
and
AI-assisted
decision-making can involve an additional challenge: the effective communication of uncertainty information between humans and AI
Steyvers et al. (2025a)
;
Steyvers et al. (2025b)
;
Li and Steyvers (2025)
;
Steyvers and Peters (2025)
;
Lee et al. (2025)
. In these collaborative scenarios, AI systems must not only evaluate uncertainty, but also convey it transparently to humans (ideally accompanied by explanations about the sources of that uncertainty in order to determine whether it can be reduced, and, if so, how). For example, this could allow humans to strategically allocate verification efforts only to instances where the AI system identifies—and reports—its outputs as unreliable.
Against this backdrop, the current work examines these uncertainty-related challenges by focusing specifically on LLMs, whose integration into decision-making workflows has become increasingly prevalent. More precisely, we investigate two specific capabilities of LLMs. First, the ability of LLMs to assess and report the reliability of their own predictions or judgments. Second, the ability of LLMs to spontaneously adjust their decisions based on this estimated uncertainty and risk configuration. As previously mentioned, it is worth noting that the relevance of these capabilities varies significantly depending on the decision-making scenario at play. Specifically, the human-AI joint and AI-assisted decision-making scenarios involve both the ability to estimate and report uncertainty. In contrast, the AI decision-making scenario, where the AI operates autonomously, would require only assessing uncertainty without reporting it. Finally, the ability to adjust decisions based on uncertainty and risk would be mainly involved in the AI decision-making scenario.
Two core dimensions underlie the ability of LLMs to assess and report the reliability of their own outcomes:
metacognitive sensitivity
and
metacognitive calibration
(also known as type 2 sensitivity and type 2 bias, respectively). The concepts of metacognitive sensitivity and metacognitive calibration originate from the fields of psychology and neuroscience
Fleming (2017)
;
Maniscalco and Lau (2014)
. They are typically applied in settings where a participant makes a primary judgment followed by a confidence rating—an assessment of the probability that the initial judgment was correct. Metacognitive sensitivity then refers to the individual’s ability to distinguish correct from incorrect responses through confidence ratings
Galvin et al. (2003)
. On the other hand, metacognitive calibration refers to the extent to which these confidence ratings align with objective accuracy. For example, a confidence rating of 80% with respect to a set of predictions is considered to be well calibrated if 80% of those predictions are indeed correct. Importantly, one can certainly possess high metacognitive sensitivity while simultaneously exhibiting poor metacognitive calibration (or conversely). For instance, a participant might
systematically
assign a confidence rating of 100% to correct responses and a confidence rating of 99% to incorrect ones. In such a case, metacognitive sensitivity would be perfect, as confidence ratings perfectly distinguish correct responses from incorrect ones. However, metacognitive calibration would be poor, as the participant is massively overconfident (systematically assigning a confidence level of 99% to incorrect responses). Finally, it is important to stress that both dimensions are vital. Indeed, consider a scenario where an LLM communicates a confidence score regarding its own output. In this context, poor metacognitive calibration would cause the user to misinterpret the confidence score, whereas zero metacognitive sensitivity renders the confidence score entirely uninformative.
Regardless, in what follows, our focus is only on the
metacognitive sensitivity
of LLMs: the ability of LLMs to distinguish their correct responses from their incorrect ones. Existing studies have already explored the metacognitive sensitivity of LLMs
Li and Steyvers (2025)
;
Seo et al. (2026)
;
Cash et al. (2025)
. However, in almost all these studies, the metrics used to quantify metacognitive sensitivity present a fundamental limitation (e.g., see Ref.
Xiong et al. (2023)
). The reason for this is that in order to determine whether an agent has a “good”, “poor”, “optimal”, “sub-optimal”, “better than” or “worse than” metacognitive sensitivity, one must necessarily take into account
cognitive sensitivity
(also known as type 1 sensitivity). Cognitive sensitivity—often quantified by
d
′
\mathchar 29028^{\mathchar 560}
—is the sensitivity associated with the primary task (i.e., the cognitive task targeted by confidence judgments). For the formal definition of
d
′
\mathchar 29028^{\mathchar 560}
, see the Methods section. The key point is that
cognitive sensitivity determines the amount of information available for the subsequent confidence judgment task
. This statement can be derived from
signal detection theory
(SDT) under minimal assumptions about how internal evidence is used for confidence judgments. On the one hand, this means that there is an upper bound on metacognitive sensitivity. Optimal metacognitive sensitivity is reached when confidence judgments are made using all the available information (having said this, in some specific cases, additional information can be accumulated between the primary task and the confidence judgment task, allowing metacognitive sensitivity to become higher than optimal). On the other hand, this means that metacognitive sensitivity is highly dependent on cognitive sensitivity. It is crucial to understand what this means. When two agents exhibit different levels of metacognitive sensitivity, this may be nothing more than a direct byproduct of their difference in cognitive sensitivity. In short, without taking cognitive sensitivity—
d
′
\mathchar 29028^{\mathchar 560}
—into account, one cannot know whether an observed difference in metacognitive sensitivity reflects a genuine difference in metacognitive abilities or merely a difference in cognitive sensitivity.
Crucially, this problem is well known in the fields of psychology and neuroscience. In these areas, the gold standard metric for metacognitive sensitivity is called meta-
d
′
\mathchar 29028^{\mathchar 560}
Maniscalco and Lau (2012)
;
Fleming (2017)
;
Maniscalco and Lau (2014)
;
Rahnev (2025)
, and it has been extensively applied in numerous studies
Mazancieux et al. (2020)
;
Rausch et al. (2015)
;
Meunier-Duperray et al. (2025)
. Meta-
d
′
\mathchar 29028^{\mathchar 560}
has been developed specifically to overcome the problem discussed above in the context of binary tasks (see the Discussion section). Unlike the other measures of metacognitive sensitivity, meta-
d
′
\mathchar 29028^{\mathchar 560}
shares the same units as
d
′
\mathchar 29028^{\mathchar 560}
. Remember that cognitive sensitivity—
d
′
\mathchar 29028^{\mathchar 560}
—determines the amount of information available for the subsequent confidence judgments task. By definition, meta-
d
′
\mathchar 29028^{\mathchar 560}
is the
d
′
\mathchar 29028^{\mathchar 560}
that an
ideal observer
would need to generate the observed confidence ratings
Fleming (2017)
. As we can see, meta-
d
′
\mathchar 29028^{\mathchar 560}
is a
d
′
\mathchar 29028^{\mathchar 560}
. It is precisely for this reason that meta-
d
′
\mathchar 29028^{\mathchar 560}
and the true
d
′
\mathchar 29028^{\mathchar 560}
(i.e., the one inferred directly from the data of the cognitive task) share the same unit, both being expressed in
standard deviation
units. As such, meta-
d
′
\mathchar 29028^{\mathchar 560}
can be compared directly with
d
′
\mathchar 29028^{\mathchar 560}
. To do so, one simply needs to compute the ratio meta-
d
′
\mathchar 29028^{\mathchar 560}
divided by
d
′
\mathchar 29028^{\mathchar 560}
, known as
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
. Note that
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
is a metric of
metacognitive efficiency
, which can be defined as
how much of the available information has been used to perform the confidence judgment task
. When
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
equals 1, this means that all the available information has been used and that metacognitive sensitivity is optimal. On the other hand, when
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
is strictly lower than 1, this means that only a fraction of the available information has been used and that metacognitive sensitivity is suboptimal. Furthermore, because meta-
d
′
\mathchar 29028^{\mathchar 560}
rests on SDT, it remains unaffected by cognitive and metacognitive biases (at least in principle), as the very purpose of SDT is to dissociate
sensitivity
from
bias
. Having said this, the reader should be aware of some limit cases challenging the use of meta-
d
′
\mathchar 29028^{\mathchar 560}
. First, the long-held view that
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
remains entirely decoupled from cognitive sensitivity and metacognitive bias has recently been challenged
Fleming (2024)
;
Guggenmos (2021)
;
Xue et al. (2021)
;
Rausch et al. (2023)
;
Rahnev (2025)
. Second, since this approach relies on SDT, one must assume that the underlying assumptions of SDT are valid, or at least sufficiently tenable to justify the use of meta-
d
′
\mathchar 29028^{\mathchar 560}
. This is why direct extensions of standard SDT have been proposed to relax specific assumptions
Miyoshi et al. (2026)
;
Maniscalco and Lau (2014)
. Otherwise, it is worth noting that a “model-free” alternative to meta-
d
′
\mathchar 29028^{\mathchar 560}
has recently been developed
Dayan (2023)
.
In this paper, we argue for the use of the meta-
d
′
\mathchar 29028^{\mathchar 560}
framework when assessing the metacognitive sensitivity of AI systems, whenever possible. While recent works have begun to explore this metric in the context of LLMs, its application remains fragmented
Cacioli (2026)
. Ref.
Trinh et al. (2025)
applied it to model selection and Ref.
Dai (2026)
investigated the impact of confidence scale design on metacognitive efficiency. Additionally, Ref.
Wang et al. (2025)
utilized a method closely related to meta-
d
′
\mathchar 29028^{\mathchar 560}
but under an alternative terminology instead of adopting the established one, thereby further obscuring connections between the relevant fields.
By leveraging the properties of meta-
d
′
\mathchar 29028^{\mathchar 560}
, we are able to conduct a multi-faceted analysis across three axes of comparison. These comparison axes allow us to highlight the shortcomings of the popular metric type 2 AUROC (AUC2)
Clarke et al. (1959)
and demonstrate the practical relevance of meta-
d
′
\mathchar 29028^{\mathchar 560}
, especially when cognitive sensitivity varies. In the following list, we present these axes and discuss the insights they each provide:
1.
Compare an LLM to optimality.
This is essential to determine whether an LLM’s metacognitive abilities have reached their ceiling or if there remains a significant margin for improvement.
2.
Compare different LLMs.
When it comes to integrating an LLM into a decision-making process, the question of selecting the most appropriate model always arises. As we have seen, an effective decision-making process must take uncertainty into account (particularly when risk is involved). Therefore, selecting the most appropriate model requires evaluating and comparing different LLMs not only on the cognitive task directly related to the decision-making process but also on their ability to quantify uncertainty. In the current paper, we investigated GPT-5 (reasoning efforts set to “Medium” by default
OpenAI (2026)
), DeepSeek-V3.2-Exp (in non-thinking mode
DeepSeek ()
) and Mistral-Medium-2508.
3.
Compare the same LLM in the context of different cognitive tasks.
This is important because if it turns out that metacognitive efficiency differs significantly depending on the targeted cognitive task, then it becomes difficult, if not impossible, to generalize conclusions regarding the LLM’s metacognitive abilities established in the context of a specific cognitive task. Here, we consider three binary discrimination tasks, labeled A, B and C (see Methods for further details):
•
Sentiment analysis task (A).
The AI receives a sentence or piece of sentence, whose binary valence (either positive or negative) has been labeled by a human, and it must guess this valence.
•
Oral vs written classification task (B).
The AI receives a sentence, that originates from either an oral or written source, and it must guess whether it is oral or written.
•
Word depletion detection task (C).
The AI receives a sentence in which a “the” may have been deleted. The AI has to guess whether a “the” has been removed or if the sentence has been directly submitted unchanged.
Note that the experimental setting at play here is always an LLM conducting a cognitive judgment (type 1 task) followed by a confidence rating—an assessment of the probability that the initial judgment was correct (type 2 task).
Finally, as mentioned above, in a second step, we explore the ability of LLMs to spontaneously adjust their decisions based on
uncertainty
and
risk configuration
. In principle, higher stakes are expected to yield more
conservative
behavior. For instance, if the cost of failure with respect to a specific choice is catastrophic, then this path should only be considered when uncertainty is near zero. In the context of SDT
Green et al. (1966)
;
Macmillan and Creelman (2005)
;
Wickens (2001)
, such sensitivity to uncertainty and risk is captured by the shift of the decision criterion
c
\mathchar 29027
.
The question we ask is the following: depending on the risk configuration, does the LLM calibrate accordingly its type 1 criterion
c
\mathchar 29027
? To answer this question, our experiments are straightforward: the AI performs a type 1 task (we use the same as those presented above) under different risk configurations. Calling S1 and S2 the two possible responses to the type 1 task, we refer to the risk configurations “S1” and “S2” the scenarios in which we use a prompt specifying high risk when answering S1 or S2, respectively, and “None” in case of no specification of risk. As previously, we consider GPT-5, DeepSeek-V3.2-Exp and Mistral-Medium-2508. See Methods for further details.
We refer to the experiments in which we estimate meta-
d
′
\mathchar 29028^{\mathchar 560}
as the “meta-
d
′
\mathchar 29028^{\mathchar 560}
experiments”, while those focusing on the calibration of
c
\mathchar 29027
are termed “
c
\mathchar 29027
-calibration experiments” (see Methods for further details).
2
Results
Given the large number of trials in our experiments, which can make even negligible effects statistically significant, we distinguish between statistical significance and
practical
significance by defining
Regions of Practical Equivalence
(ROPEs)
Makowski et al. (2019)
. For more information, see the Methods section. Hence, when a difference is said to be significant without further qualification, it means that it is
both
statistically and practically significant. The meta-
d
′
\mathchar 29028^{\mathchar 560}
experiments reveal that all three LLMs exhibited measurable metacognitive sensitivity, with
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
values ranging from moderate to near-optimal, although some significant variation was observed across models and tasks. Crucially, we systematically compare the conclusions drawn from the meta-
d
′
\mathchar 29028^{\mathchar 560}
approach with those drawn from the widely used metric of metacognitive sensitivity AUC2
Clarke et al. (1959)
. In the
c
\mathchar 29027
-calibration experiments, shifts in decision criterion
c
\mathchar 29027
indicate that all three LLMs were able to spontaneously adjust their decisions in a manner consistent with the specified risk.
Meta-
d
′
\mathchar 29028^{\mathchar 560}
experiments
The results of the meta-
d
′
\mathchar 29028^{\mathchar 560}
experiments are shown in
Figure
1
and given in Table S1. The left column of
Figure
1
shows
d
′
\mathchar 29028^{\mathchar 560}
, meta-
d
′
\mathchar 29028^{\mathchar 560}
,
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
, and AUC2, while the right column shows accuracy (proportion of correct responses) as a function of confidence ratings on a five-point scale. The first, second, and third rows correspond to GPT-5, DeepSeek-V3.2-Exp, and Mistral-Medium-2508, respectively.
Figure 1:
d
′
\mathchar 29028^{\mathchar 560}
and meta-
d
′
\mathchar 29028^{\mathchar 560}
(left column),
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
and AUC2 (middle column) and the accuracy, or
P
⁡
(
correct
|
confidence
=
C
i
)
\mathchar 29008\delimiter 67273472\text{correct}\mathchar 12906\text{confidence}\mathchar 12349\mathchar 28995_{\mathchar 29033}\delimiter 84054785
versus confidence level (right column). The results are shown for GPT-5 (top row), DeepSeek-V3.2-Exp (middle row) and Mistral-Medium-2508 (bottom row) across task A (blue; left bars), task B (orange; middle bars), and task C (yellow; right bars). See the legends on top of panel (a) and in panel (c). Error bars in the left and middle columns denote 95% CI of the posterior or estimated by the Delta method for AUC2 (see the Methods for details). Also, because the chance-level value of AUC2 is 0.5, and that all
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
values are greater than 0.5, we set the range of the y-axis of the middle column to 0.5-1. When computing accuracy versus confidence (right column), GPT-5 reported confidence C1 in one trial of task B and one trial of task C; these observations were excluded, leaving no data points at those confidence levels. The number of trials was
2
×
1
​
0
4
\mathchar 28722\mathchar 8706\mathchar 28721\mathchar 28720^{\mathchar 28724}
for task A and
1
​
0
4
\mathchar 28721\mathchar 28720^{\mathchar 28724}
otherwise (See the Methods for further details).
We start by comparing the models’
d
′
\mathchar 29028^{\mathchar 560}
across the tasks. In task A, no pairwise differences were observed (the 95% Credible Interval [CI] over the posterior of their difference does not overlap zero; see the Methods section for details). In task B, DeepSeek-V3.2-Exp shows a significantly larger
d
′
\mathchar 29028^{\mathchar 560}
than those of the other models, which do not differ significantly from one another. Lastly, in task C, GPT-5’s
d
′
\mathchar 29028^{\mathchar 560}
is larger than those of the other models, which do not differ significantly from one another. Notably, in this latter case, the differences in
d
′
\mathchar 29028^{\mathchar 560}
between GPT-5 and the other models is considerably more pronounced than in the other two tasks (GPT-5’s type 1 sensitivity is
1
​
2
​
6
%
\mathchar 28721\mathchar 28722\mathchar 28726\%
and
1
​
3
​
0
%
\mathchar 28721\mathchar 28723\mathchar 28720\%
larger than those of DeepSeek-V3.2-Exp and Mistral-Medium-2508, respectively).
Regarding differences in
d
′
\mathchar 29028^{\mathchar 560}
across tasks for the same model, every model exhibits significant variations across tasks.
We now turn to confidence ratings. The right column of
Figure
1
shows that, in task A, unlike the other tasks, the models use the full confidence rating scale (see the distributions of confidence ratings in Figure S1). In particular, in panel (i), we observe that Mistral-Medium-2508 essentially uses only two points of the confidence rating scale, which can occur in cases of poor metacognitive calibration, even in the context of optimal metacognitive sensitivity as discussed in the introduction. Also, we note that, for Mistral-Medium-2508 and DeepSeek-V3.2-Exp, the accuracy associated with the lowest confidence level (C1) in task A is lower than 0.5, corresponding to below-chance accuracy. Such below-chance accuracy can be explained by specific configurations of type 1 and type 2 criteria. Regardless, this confidence level only concerns 1.91% and 0.76% of trials, respectively.
In all cases, the models displayed substantial meta-
d
′
\mathchar 29028^{\mathchar 560}
across tasks, but always suboptimal (the 95% CIs of the posteriors over
log
⁡
M
r
​
a
​
t
​
i
​
o
\log\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
do not overlap 0 and fall entirely outside the defined ROPE; see the Methods for details).
In task A, the
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
of GPT-5 is significantly larger than that of DeepSeek-V3.2-Exp (
Δ
​
M
r
​
a
​
t
​
i
​
o
=
0
.
1
​
6
\mathchar 28673\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28721\mathchar 28726
, where
Δ
​
M
r
​
a
​
t
​
i
​
o
\mathchar 28673\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
denotes the difference in
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
). Mistral-Medium-2508’s
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
is larger than that of DeepSeek-V3.2-Exp (
Δ
​
M
r
​
a
​
t
​
i
​
o
=
0
.
2
\mathchar 28673\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28722
), and is not significantly different than that of GPT-5. In task B, GPT-5’s
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
is significantly greater than those of the other two models (
Δ
​
M
r
​
a
​
t
​
i
​
o
=
0
.
2
​
1
\mathchar 28673\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28722\mathchar 28721
for DeepSeek-V3.2-Exp and
Δ
​
M
r
​
a
​
t
​
i
​
o
=
0
.
0
​
9
\mathchar 28673\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28720\mathchar 28729
for Mistral-Medium-2508). However, the difference with Mistral-Medium-2508 is practically inconclusive. Mistral-Medium-2508’s
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
is also significantly larger than that of DeepSeek-V3.2-Exp, yet at a practically inconclusive level. In task C, GPT-5 shows an
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
larger than that of the other models. However, these differences are practically inconclusive. The
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
values of DeepSeek-V3.2-Exp and Mistral-Medium-2508 do not differ significantly.
For these comparisons, AUC2 closely follows
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
(in tasks A and C, the differences in AUC2 between GPT-5 and Mistral-Medium-2508, and between Mistral-Medium-2508 and DeepSeek-V3.2-Exp are statistically significant but practically negligible), suggesting that the possible contamination by
d
′
\mathchar 29028^{\mathchar 560}
does not drive the observed differences in AUC2 between models. This would be expected given that
d
′
\mathchar 29028^{\mathchar 560}
remains relatively similar between models. That said, in task C, GPT-5’s
d
′
\mathchar 29028^{\mathchar 560}
is much larger than that of the other models. However, this gap does not distort the conclusion drawn from AUC2, since differences in metacognitive efficiency—tracked by
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
—already pointed in the same direction (i.e., GPT-5’s
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
is also higher than that of the other models).
Let us now turn to the differences across tasks for the same model which is the dimension where
d
′
\mathchar 29028^{\mathchar 560}
vary the most. Across tasks, the
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
of GPT-5 and DeepSeek-V3.2-Exp do not differ significantly. In contrast, their AUC2 differ significantly in a way that mirrors
d
′
\mathchar 29028^{\mathchar 560}
(see
Figure
1
). Accordingly, AUC2 and
d
′
\mathchar 29028^{\mathchar 560}
were highly correlated as anticipated (Spearman correlation:
r
s
=
0
.
9
\mathchar 29042_{\mathchar 29043}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28729
,
p
<
0
.
0
​
0
​
2
\mathchar 29040\mathchar 12604\mathchar 28720\mathchar 314\mathchar 28720\mathchar 28720\mathchar 28722
). For Mistral-Medium-2508,
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
varies significantly between task A and task B, and between task A and task C, with
Δ
​
M
r
​
a
​
t
​
i
​
o
=
0
.
1
​
3
\mathchar 28673\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28721\mathchar 28723
and
Δ
​
M
r
​
a
​
t
​
i
​
o
=
0
.
2
​
0
\mathchar 28673\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28722\mathchar 28720
, but not between task B and task C. All the corresponding pairwise values of AUC2 differ significantly.
Up to this point, our analyses have followed the standard scientific method by comparing conditions where only a single dimension varies at a time (either across models within the same task or across tasks for the same model). However, given that the primary goal of this paper is methodological, we illustrate the shortcomings of AUC2 by stressing a specific situation where we vary simultaneously the model and the task and where AUC2 and
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
lead to opposite conclusions. Specifically, we compare DeepSeek-V3.2-Exp in Task A against Mistral-Medium-2508 in Task B. In this case, differences in both
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
and AUC2 are statistically significant (a Bonferroni correction with
α
′
=
0
.
0
​
5
/
m
\mathchar 28939^{\mathchar 560}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28720\mathchar 28725\delimiter 68408078\mathchar 29037
and
m
=
3
​
6
\mathchar 29037\mathchar 12349\mathchar 28723\mathchar 28726
was applied to the AUC2 comparisons)
but in opposite directions
: Mistral-Medium-2508 has a larger
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
than DeepSeek-V3.2-Exp, but it has a smaller AUC2, consistent with its lower
d
′
\mathchar 29028^{\mathchar 560}
.
c-calibration experiments
For all models and tasks, we vary the risk configuration (see Introduction and Methods for details).
Figure
2
shows the estimated
c
\mathchar 29027
for each scenario, model and task (see also Table S2).
c
′
=
c
/
d
′
\mathchar 29027^{\mathchar 560}\mathchar 12349\mathchar 29027\delimiter 68408078\mathchar 29028^{\mathchar 560}
is given in Figure S2.
GPT-5 is the only model to exhibit significantly different
c
\mathchar 29027
values across all risk configurations within all tasks. Importantly, these variations in
c
\mathchar 29027
values were logically coherent with the changes in risk configuration, as the model’s decision criterion consistently shifted to become more conservative toward the high-risk response (i.e., a shift to the left under the risk configuration “S1” and a shift to the right under the risk configuration “S2”). Notably, under the risk configuration “S1”,
c
\mathchar 29027
is always below
−
0
.
6
\mathchar 8704\mathchar 28720\mathchar 314\mathchar 28726
, while
c
\mathchar 29027
under the risk configuration “S2” is always greater than
0
.
6
\mathchar 28720\mathchar 314\mathchar 28726
.
For Mistral-Medium-2508 within task B and for DeepSeek-V3.2-Exp within task C, the differences between the risk configurations “None” and “S2” and between the risk configurations “S1” and “None”, respectively, are not significant. Otherwise, all other pairwise comparisons across risk configurations within each tasks are significant and consistent with the specified risk configuration. However, when compared to the defined ROPE (see Methods for details), the differences in task A between the risk configurations “S1” and “None” and between the risk configurations “S2” and “None” for DeepSeek-V3.2-Exp are practically inconclusive. Similarly, in task C, the difference between the risk configurations “S1” and “None” for Mistral-Medium-2508 is inconclusive.
It should be noted that several variations in
d
′
\mathchar 29028^{\mathchar 560}
between risk configurations were found to be significant. Specifically, this is the case for GPT-5 within task B between the risk configurations “None” and “S2” (relative difference of
1
​
8
%
\mathchar 28721\mathchar 28728\%
) and within task C between the risk configurations “None” and “S1” (relative difference of
4
​
1
%
\mathchar 28724\mathchar 28721\%
) and between the risk configurations “S2” and “S1” (relative difference of
3
​
7
%
\mathchar 28723\mathchar 28727\%
). Within task B, DeepSeek-V3.2-Exp also exhibits a significant change in
d
′
\mathchar 29028^{\mathchar 560}
between “S1” and “S2” (relative difference of
1
​
3
%
\mathchar 28721\mathchar 28723\%
). In contrast, all other differences were either non-significant (19 cases) or, while statistically significant, proved to be practically inconclusive (4 cases).
When differences in
d
′
\mathchar 29028^{\mathchar 560}
are significant, the normalized criterion
c
′
=
c
/
d
′
\mathchar 29027^{\mathchar 560}\mathchar 12349\mathchar 29027\delimiter 68408078\mathchar 29028^{\mathchar 560}
is preferable to
c
\mathchar 29027
, as it accounts for the magnitude of the bias
relative to the sensitivity
. We therefore examine the differences in
c
′
\mathchar 29027^{\mathchar 560}
for these specific cases in Figure S2. Notably, the comparisons of
c
′
\mathchar 29027^{\mathchar 560}
mirror those of
c
\mathchar 29027
.
These results show that, in most cases across tasks and models, we were able to induce a conservative behavior toward either S1 or S2 by specifying a risk configuration in natural language through prompt design. In other words this demonstrates a general ability of LLMs to calibrate their type 1 criterion in a context-dependent manner.
Figure 2:
Type 1 criterion
c
\mathchar 29027
across three risk configurations (“S1”, “None” , “S2”) within task A (top row), task B (middle row) and task C (bottom row), for GPT-5 (left column), DeepSeek-V3.2-Exp (middle column), and Mistral-Medium-2508 (right column). Error bars represent 95% confidence intervals estimated via the Delta method. Although the Delta method can be sensitive to extreme proportions (that is, hit rates or false alarm rates close to 0 or 1), as may occur when responses are strongly biased toward S1 or S2, the large trial count (
N
≳
1
​
0
4
\mathchar 29006\gtrsim\mathchar 28721\mathchar 28720^{\mathchar 28724}
) mitigates potential issues. See the Methods for details.
3
Discussion
In this paper, we highlighted a key limitation of commonly used methods for assessing the metacognitive sensitivity of AI, and drew attention to the meta-
d
′
\mathchar 29028^{\mathchar 560}
framework, a well-established approach from psychology and neuroscience specifically designed to address this shortcoming. Moreover, we also proposed to leverage SDT to measure the ability of AIs to spontaneously regulate their decisions based on uncertainty and risk. We showcased these psychophysical approaches by conducting two series of experiments on LLMs. In the first, our multi-faceted application of meta-
d
′
\mathchar 29028^{\mathchar 560}
allowed us to compare LLMs to optimality, compare different LLMs on the same task, and compare the same LLM across different tasks, systematically contrasting the conclusions drawn from the meta-
d
′
\mathchar 29028^{\mathchar 560}
approach with those drawn from the widely used metric AUC2
Clarke et al. (1959)
. Notably, our results reveal that LLMs exhibit measurable metacognitive sensitivity. More precisely, all three models tested—GPT-5, DeepSeek-V3.2-Exp, and Mistral-Medium-2508—exhibited substantial values of meta-
d
′
\mathchar 29028^{\mathchar 560}
, indicating that their confidence judgments meaningfully tracked their type 1 performance, with variable
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
levels, ranging from moderate (
∼
0
.
6
​
5
\mathchar 12824\mathchar 28720\mathchar 314\mathchar 28726\mathchar 28725
) to near-optimal (
∼
0
.
9
​
0
\mathchar 12824\mathchar 28720\mathchar 314\mathchar 28729\mathchar 28720
). Also, we found some variability in
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
across tasks (for the same model) and across models (for the same task). Crucially, in some cases, AUC2 and
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
lead to different—even opposite—conclusions, especially when large variations in type 1 sensitivity
d
′
\mathchar 29028^{\mathchar 560}
contaminate the values of AUC2. This was found to be particularly the case when comparing the same model across tasks.
In sum, the results of the first series of experiments highlight the critical importance of the meta-
d
′
\mathchar 29028^{\mathchar 560}
framework, particularly when cognitive sensitivity (
d
′
\mathchar 29028^{\mathchar 560}
) varies between conditions. That said, it should be noted that the core idea behind the meta-
d
′
\mathchar 29028^{\mathchar 560}
approach—correcting metacognitive metrics for type 1 performance—can be extended to other measures of metacognitive sensitivity
Rahnev (2025)
;
Dayan (2023)
. For example, Rahnev recently proposed the ratio of observed AUC2 to expected AUC2, where the latter is computed from estimated SDT parameters
Rahnev (2025)
. Yet, after comparing several measures of metacognition on task performance and bias dependence, he concludes that
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
remains a good default metric.
The second series of experiments, focused on shifts in
c
\mathchar 29027
, highlighted the remarkable ability of LLMs to become more conservative in their decision-making in a way consistent with the specified risk. Hence, SDT constitutes a promising approach for studying the ability of AI systems to regulate their own decision.
We emphasize that our approach is strictly instrumental and outcome-oriented, making no claims about whether these systems possess genuine self-monitoring—i.e., metacognition—or merely mimic human behavior. While this distinction remains a fascinating question, it lies beyond the scope of this work. From a societal utility and risk-management perspective, what matters is merely the outcome (e.g., whether confidence ratings reliably predict type 1 performance), regardless of the underlying process that generates this outcome (on this topic, see Ref.
Kumaran et al. (2026c)
). Note that there is a large literature on the mechanistic and computational differences between human brains and existing AI systems (e.g., see Ref.
Connell and Lynott (2024)
).
Note that many aspects of our experiments can be tuned in a way that may affect the results. For example, instead of submitting the sentences one by one, we could submit them all at once, or in batches, to see whether this affects their responses as having access to all sentences could potentially impact their cognitive and metacognitive calibration. Similarly, for each trial, we could ask them to perform the type 1 task and the type 2 task in two successive prompts rather than in the same prompt. Also, it has been reported in Ref.
Wang et al. (2025)
that varying the design of confidence scale, as changing the number of confidence levels (e.g.,
[
0
,
1
​
0
]
\delimiter 67482370\mathchar 28720\mathchar 24891\mathchar 28721\mathchar 28720\delimiter 84267779
versus
[
0
,
2
​
0
]
\delimiter 67482370\mathchar 28720\mathchar 24891\mathchar 28722\mathchar 28720\delimiter 84267779
) affects metacognitive efficiency. One can also tune models’ parameters such as the temperature or the level of “reasoning budget”. Finally, remember that our article is not a benchmark paper.
Moreover, although our three tasks involved the discrimination of a single stimulus, psychophysical experiments are frequently carried out using two-alternative forced-choice (2AFC) discrimination tasks, in which the subject chooses between two alternative stimuli
Tyler and Chen (2000)
(we thank Kiyofumi Miyoshi and Hakwan Lau for valuable feedback on this point). The 2AFC paradigm is considered to render the equal variance assumption more tenable
Miyoshi et al. (2022)
. In practice, the meta-
d
′
\mathchar 29028^{\mathchar 560}
framework can also be applied beyond binary tasks (e.g., to open-ended questions) by
relabeling the responses to the cognitive task as “correct” or “incorrect”. However, as it was specifically designed for binary
tasks, doing so may render some underlying assumptions untenable, which has led some authors to prefer not to use it in such settings
Cacioli (2026)
;
Vuorre and Metcalfe (2022)
;
Molenberghs et al. (2016)
. Regardless, whenever applicable, meta-
d
′
\mathchar 29028^{\mathchar 560}
should be preferred. When it is not applicable, authors should exercise caution when drawing conclusions from comparisons across conditions in which type 1 performance and bias vary. As mentioned in the Introduction, there exist versions of SDT that relax specific assumptions, such as the unequal variance SDT model
Maniscalco and Lau (2014)
. Interestingly, unequal variance has been related to neuronal firing, where variance increases with the mean
Miyoshi et al. (2026)
.
Following standard practice in experimental psychology, we explicitly asked the AI—via the prompt—to report its confidence
Xiong et al. (2023)
; this is also a natural choice for
conversational
AIs. An alternative would be to infer confidence from token probabilities
Steyvers et al. (2025b)
. However, these two approaches need not be equivalent
Tian et al. (2023)
;
Kumaran et al. (2026a)
. Note that verbalized confidence and token probabilities are two metrics among many different ones used to discriminate correct from incorrect responses in the field of LLM uncertainty quantification (UQ)
Fadeeva et al. (2023)
;
Shorinwa et al. (2025)
;
Ye et al. (2024)
.
We applied our approach in the context of simple binary discrimination tasks. However, it should be noted that the challenge of evaluating AI metacognition requires not only robust metrics but also the development of adequate tasks—specifically, tasks that actively engage the targeted metacognitive skills. For example, to evaluate the metacognitive competencies at stake in the “AI decision-making” scenario, we advocate for the use of experimental paradigms where the model must manage the exploration-exploitation trade-off (a dimension not addressed in our experiments). The classic paradigm for this is the multi-armed bandit problem
Lattimore and Szepesvári (2020)
. Another compelling example is the
Eleusis Benchmark
recently proposed by David Louapre in Ref.
Louapre (2026)
. In this task, the agent must find a hidden rule behind a sequence of cards. To do so, it samples evidence at each turn by playing a new card and receiving feedback, and then decides whether to commit to an answer. Crucially, the more delayed the successful guess and the more wrong answers, the less points. This creates a critical tension: responding too early leads to errors due to uncertainty, while responding too late costs points. While Louapre identified distinct “player profiles”—ranging from reckless to cautious—our research adds a crucial layer to this observation: we have demonstrated that a single LLM is capable of strategic flexibility. Rather than being locked into one profile, these models can shift their behavior when the cost of error and context change. Finally, integrating such tasks with our psychophysical analysis would allow for a much finer characterization of AI metacognition. In ref.
Kumaran et al. (2026b)
, the authors consider four-option multiple-choice questions plus an abstention option to investigate whether the AI chooses to abstain under low confidence. One possible extension of this setup would be to explicitly manipulate the level of risk specified in the prompt, in order to study whether the AI adjusts its abstention behavior in a context-sensitive manner.
We now turn to the well-known issue of hallucinations
Zhang et al. (2025)
. Hallucinations are typically framed as factual errors communicated as
undisputed
facts. Hence, hallucinations are not merely “cognitive errors”; they also involve a “metacognitive error,” in that the model hallucinates a high confidence level in spite of uncertainty. The present article does not address this pathological regime.
While this study has focused on the ability of AI to estimate (and report) its own confidence, another crucial skill in some collaborative decision-making scenarios is the capacity to integrate confidence signals communicated by other agents—whether human or artificial. Future experiments will consist in providing an LLM with a recommendation accompanied by a confidence score whenever it is about to perform a type 1 task. The question we ask is: does the extent to which the AI takes into account the recommendation depends on the communicated confidence? Such experiments are crucial for evaluating whether AI systems can behave meaningfully when participating in collaborative decision-making processes. Note that a gap in the interpretation of confidence signals may arise between collaborating agents depending on how this information is formulated
Steyvers et al. (2025b)
.
In conclusion, our work highlights the relevance of the meta-
d
′
\mathchar 29028^{\mathchar 560}
and SDT approaches in the study of AI metacognition. Crucially, the growing integration of AI into decision-making workflows makes the characterization of AI metacognition an increasingly pressing need.
4
Methods
Tasks and datasets
In all experiments, the models are asked to perform a binary discrimination task (either the sentiment analysis task [A], the oral vs written classification task [B], or the word depletion detection task [C]; see below). In the meta-
d
′
\mathchar 29028^{\mathchar 560}
experiments, they are also asked to rate their confidence on a scale from 1 to 5. The prompts are available on the GitHub page given below. Prompts for the
c
\mathchar 29027
-calibration experiments may specify a risk configuration (see the Introduction for explanations). In all cases, we submitted one input (e.g., a sentence to discriminate) at a time, each submission effectively corresponding to a new conversation.
Sentiment analysis task (A).
The AI receives a sentence or piece of sentence, whose binary valence (either positive or negative) has been labeled by a human, and it must guess this valence. We used the SST-2 dataset freely available at
https://huggingface.co/datasets/stanfordnlp/sst2
.
Oral vs written classification task (B).
The AI receives a sentence, that originates from either an oral or written source, and it must guess whether it is oral or written. We used a labeled dataset freely available at
https://zenodo.org/records/7694423
.
Word depletion detection task (C).
Using the same dataset from task B, we selected sentences comprising at least one “the”, and deleted one with a probability of 0.5. The AI has to guess whether a “the” has been removed or if the sentence has been directly submitted unchanged.
Metrics
We give a succinct introduction to type 1 sensitivity (
d
′
\mathchar 29028^{\mathchar 560}
), type 1 criterion (
c
\mathchar 29027
), and metacognitive sensitivity (meta-
d
′
\mathchar 29028^{\mathchar 560}
) (see Ref.
Maniscalco and Lau (2014)
for a thorough derivation). Suppose that a subject performs repeated trials of a discrimination task in which the only possible responses are S1 and S2. Given a stimulus, which is either S1 or S2, consider an internal response evaluated along a one-dimensional axis
x
\mathchar 29048
. Let us define
f
⁡
(
x
|
S
​
1
)
\mathchar 29030\delimiter 67273472\mathchar 29048\mathchar 12906\mathchar 29011\mathchar 28721\delimiter 84054785
and
f
⁡
(
x
|
S
​
2
)
\mathchar 29030\delimiter 67273472\mathchar 29048\mathchar 12906\mathchar 29011\mathchar 28722\delimiter 84054785
to be normal distributions with equal unit variance.
d
′
\mathchar 29028^{\mathchar 560}
is then defined as:
d
′
=
z
⁡
(
HR
)
−
z
⁡
(
FAR
)
\mathchar 29028^{\mathchar 560}\mathchar 12349\mathchar 29050\delimiter 67273472\text{HR}\delimiter 84054785\mathchar 8704\mathchar 29050\delimiter 67273472\text{FAR}\delimiter 84054785
(1)
where
z
\mathchar 29050
is the inverse of the normal cumulative distribution function, HR is the hit rate (proportion of successful judgments when S2 was presented), and FAR is the false-alarm rate (proportion of incorrect judgments when S1 was presented).
Notably,
Equation
1
reduces to
d
′
=
μ
S
​
2
−
μ
S
​
1
\mathchar 29028^{\mathchar 560}\mathchar 12349\mathchar 28950_{\mathchar 29011\mathchar 28722}\mathchar 8704\mathchar 28950_{\mathchar 29011\mathchar 28721}
(2)
where
μ
S
​
1
\mathchar 28950_{\mathchar 29011\mathchar 28721}
and
μ
S
​
2
\mathchar 28950_{\mathchar 29011\mathchar 28722}
are the means of
f
⁡
(
x
|
S
​
1
)
\mathchar 29030\delimiter 67273472\mathchar 29048\mathchar 12906\mathchar 29011\mathchar 28721\delimiter 84054785
and
f
⁡
(
x
|
S
​
2
)
\mathchar 29030\delimiter 67273472\mathchar 29048\mathchar 12906\mathchar 29011\mathchar 28722\delimiter 84054785
.
d
′
\mathchar 29028^{\mathchar 560}
quantifies the extent to which the subject is able to discriminate the two types of stimuli—S1 and S2. Consider a decision criterion
c
\mathchar 29027
which is the value of the internal response
x
\mathchar 29048
below and above which the subject responds S1 and S2, respectively. It is possible to write
c
\mathchar 29027
as a function of HR and FAR:
c
=
−
0
.
5
×
(
z
⁡
(
HR
)
+
z
⁡
(
FAR
)
)
.
\mathchar 29027\mathchar 12349\mathchar 8704\mathchar 28720\mathchar 314\mathchar 28725\mathchar 8706\left\delimiter 67273472\mathchar 29050\delimiter 67273472\text{HR}\delimiter 84054785\mathchar 8235\mathchar 29050\delimiter 67273472\text{FAR}\delimiter 84054785\right\delimiter 84054785\mathchar 314
(3)
The smaller
c
\mathchar 29027
, the stronger the internal response required for the subject to respond S1; that is, greater evidence is needed for a S1 response. We also define
c
′
=
c
/
d
′
\mathchar 29027^{\mathchar 560}\mathchar 12349\mathchar 29027\delimiter 68408078\mathchar 29028^{\mathchar 560}
.
After each trial, the subject is asked to rate its confidence on a given scale, from 1 to
H
\mathchar 29000
. Meta-
d
′
\mathchar 29028^{\mathchar 560}
is defined as the
d
′
\mathchar 29028^{\mathchar 560}
that would be expected given confidence ratings only, if they were generated by an ideal observer
Fleming (2017)
. More generally, let us define
θ
=
(
meta-
​
d
′
,
meta-
​
c
,
meta-
c
2
)
\mathchar 28946\mathchar 12349\left\delimiter 67273472\text{meta-}\mathchar 29028^{\mathchar 560}\mathchar 24891\text{meta-}\mathchar 29027\mathchar 24891\text{meta-}\textbf{{\lx@text@underline{c}}}_{\mathchar 28722}\right\delimiter 84054785
where
c
2
\textbf{{\lx@text@underline{c}}}_{\mathchar 28722}
denotes the type 2 criteria
Maniscalco and Lau (2014)
. The estimation of meta-
d
′
\mathchar 29028^{\mathchar 560}
is typically implemented using a maximum likelihood estimation:
UNKNOWN
∗
\displaystyle\mathchar 28946^{\mathchar 8707}
=
arg max
UNDERACCENT
L
(
UNKNOWN
|
confidence ratings
)
, subject to
meta-
c
′
=
c
′
,
(
meta-
c
ascending
)
\displaystyle\mathchar 12349\underset{\mathchar 28946}{\text{arg~max }}\mathchar 29004\delimiter 67273472\mathchar 28946\mathchar 12906\text{confidence ratings}\delimiter 84054785\text{, subject to }\text{meta-}\mathchar 29027^{\mathchar 560}\mathchar 12349\mathchar 29027^{\mathchar 560}\mathchar 24891\,\mathchar 28941\left\delimiter 67273472\text{meta-}\textbf{{\lx@text@underline{c}}}_{\text{ascending}}\right\delimiter 84054785
(4)
where
L
\mathchar 29004
is the log-likelihood and
γ
⁡
(
meta-
c
ascending
)
\mathchar 28941\left\delimiter 67273472\text{meta-}\textbf{{\lx@text@underline{c}}}_{\text{ascending}}\right\delimiter 84054785
is a Boolean function that returns true only if the type 1 and type 2 criteria are ordered appropriately. Metacognitive efficiency is defined as
M
r
​
a
​
t
​
i
​
o
=
meta-
​
d
′
/
d
′
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}\mathchar 12349\text{meta-}\mathchar 29028^{\mathchar 560}\delimiter 68408078\mathchar 29028^{\mathchar 560}
. It is possible to compute meta-
d
′
\mathchar 29028^{\mathchar 560}
using a Bayesian model that outputs a full
posterior
. In the current work, we used the implementation of this approach provided in Ref.
Fleming (2017)
, available at
https://github.com/smfleming/HMeta-d
. Yet, in the
c
\mathchar 29027
-calibration experiments, we directly applied the formula of
c
\mathchar 29027
from type 1 response counts.
Finally, type 2 AUROC (AUC2) corresponds to the Area Under the type 2 Receiver Operating Characteristic curve. The type 2 receiver operating characteristic curve is obtained by varying the confidence criterion used to classify responses as high- or low-confidence and plotting, for each criterion, the proportion of correct responses classified as high-confidence against the proportion of incorrect responses classified as high-confidence.
Number of trials.
For task A, the measured
d
′
\mathchar 29028^{\mathchar 560}
were very large (above 3). Consequently, we submitted
2
×
1
​
0
4
\mathchar 28722\mathchar 8706\mathchar 28721\mathchar 28720^{\mathchar 28724}
sentences for each estimation. This trial count was informed by tests with simulated data (see Figure S3). For all other tasks, the trial count was set to
1
​
0
4
\mathchar 28721\mathchar 28720^{\mathchar 28724}
. These large trial counts also support the use of the Delta method to quantify uncertainty in the estimates (see the next section).
Statistical analysis
Following Ref.
Fleming (2017)
, to assess statistical significance of differences between values of
d
′
\mathchar 29028^{\mathchar 560}
and values of
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
in the meta-
d
′
\mathchar 29028^{\mathchar 560}
experiments, we checked whether the
symmetric 95% credible interval
(CI) of the posterior distribution of their logarithmic difference or log ratio overlap zero using Fleming’s Bayesian model and specifically the function
fit_meta_d_mcmc.m
from Ref.
Fleming (2017)
and freely available on the GitHub page associated with the paper, where we set
mcmc_params.estimate_dprime = 1
. To evaluate the optimality of the models’ metacognition, we checked whether the CI of the posterior distribution of the log
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
overlap zero. To assess the statistical significance of differences in AUC2, we checked whether
|
Z
|
≥
2
.
7
​
7
\delimiter 69640972\mathchar 29018\delimiter 69640972\mathchar 12821\mathchar 28722\mathchar 314\mathchar 28727\mathchar 28727
, where we applied a Bonferroni correction
α
′
=
0
.
0
​
5
/
m
\mathchar 28939^{\mathchar 560}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28720\mathchar 28725\delimiter 68408078\mathchar 29037
with
m
=
9
\mathchar 29037\mathchar 12349\mathchar 28729
pairwise comparisons
Dunn (1961)
, for a Z-test where we computed the variances of the differences using the Delta method
Cox (2005)
. Finally, for the statistical significance of differences in
c
\mathchar 29027
and
d
′
\mathchar 29028^{\mathchar 560}
in the
c
\mathchar 29027
-calibration experiments, we checked whether
|
Z
|
≥
3
.
1
​
1
\delimiter 69640972\mathchar 29018\delimiter 69640972\mathchar 12821\mathchar 28723\mathchar 314\mathchar 28721\mathchar 28721
, where we applied a Bonferroni correction
α
′
=
0
.
0
​
5
/
m
\mathchar 28939^{\mathchar 560}\mathchar 12349\mathchar 28720\mathchar 314\mathchar 28720\mathchar 28725\delimiter 68408078\mathchar 29037
with
m
=
2
​
7
\mathchar 29037\mathchar 12349\mathchar 28722\mathchar 28727
pairwise comparisons
Dunn (1961)
, for a Z-test where we computed the variances of the differences using the Delta method
Cox (2005)
.
Given the large number of trials in our experiments, which can make even negligible effects statistically significant, we defined Regions of Practical Equivalence (ROPEs)
Makowski et al. (2019)
. Hence, to assess the
practical
significance of differences in
log
⁡
M
r
​
a
​
t
​
i
​
o
\log\mathchar 29005_{\mathrm{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}}
and AUC2, we use a ROPE of
[
−
0
.
0
5
,
0
.
0
5
]
\delimiter 67482370\mathchar 8704\mathchar 28720\mathchar 314\mathchar 28720\mathchar 28725\mathchar 24891\,\mathchar 28720\mathchar 314\mathchar 28720\mathchar 28725\delimiter 84267779
(note that an AUC2 of 0.5 means that confidence ratings do not discriminate correct from incorrect responses better than chance while the corresponding chance-level value for
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
is 0). For differences in
d
′
\mathchar 29028^{\mathchar 560}
and
c
\mathchar 29027
, we consider a ROPE of
[
−
0
.
1
,
0
.
1
]
\delimiter 67482370\mathchar 8704\mathchar 28720\mathchar 314\mathchar 28721\mathchar 24891\,\mathchar 28720\mathchar 314\mathchar 28721\delimiter 84267779
. In each case, we considered differences
practically
significant if the 95% CI fell entirely outside the ROPE, and on the contrary negligible if entirely inside, and inconclusive in the case of an overlap.
Code, software and data availability
Our scripts, prompts, and results (data files) are freely available at
https://github.com/sshrichard/metacognition-of-AI
Author contributions
The authors contributed equally to this work. P.S. and R.S. designed the project. R.S. prepared and conducted the experiments. R.S. and P.S. analyzed the results and wrote the manuscript.
Competing interests
All authors declare no financial or non-financial competing interests.
Funding declaration
Not applicable
References
Bahrami
et al.
(2010)
B. Bahrami, K. Olsen, P. E. Latham, A. Roepstorff, G. Rees, and C. D. Frith
Optimally interacting minds
.
Science
329
(
5995
),
pp. 1081–1085
.
Cited by:
§1
.
Berger-Tal
et al.
(2014)
O. Berger-Tal, J. Nathan, E. Meron, and D. Saltz
The exploration-exploitation dilemma: a multidisciplinary framework
.
PloS one
9
(
4
),
pp. e95693
.
Cited by:
§1
.
Bhattacharyya
et al.
(2024)
R. Bhattacharyya, D. A. Nguyen, C. Colombatto, S. Fleming, I. Posner, and N. Hawes
Towards intelligent decision support systems in robotics: investigating the role of self-confidence calibration in joint decision-making
.
In
AAAI Spring Symposium Series
,
Cited by:
§1
.
Cacioli (2026)
J. Cacioli
Do LLMs know what they know? measuring metacognitive efficiency with signal detection theory
.
arXiv preprint arXiv:2603.25112
.
Cited by:
§1
,
§3
.
Cash
et al.
(2025)
T. N. Cash, D. M. Oppenheimer, S. Christie, and M. Devgan
Quantifying uncert-AI-nty: testing the accuracy of LLMs’ confidence judgments
.
Memory & Cognition
,
pp. 1–26
.
Cited by:
§1
.
Castilla
et al.
(2025)
A. C. Castilla, I. d. P. D’Amorim, M. F. B. Wanderley, M. A. Esmeraldo, A. R. Yoshida, A. M. Eigier, and M. Valente Yamada Sawamura
External validation of an artificial intelligence triaging system for chest X-rays: a retrospective independent clinical study
.
Diagnostics
15
(
22
),
pp. 2899
.
Cited by:
item 3
.
Chang
et al.
(2024)
Y. Chang, X. Wang, J. Wang, Y. Wu, L. Yang, K. Zhu, H. Chen, X. Yi, C. Wang, Y. Wang,
et al.
A survey on evaluation of large language models
.
ACM transactions on intelligent systems and technology
15
(
3
),
pp. 1–45
.
Cited by:
§1
.
Clarke
et al.
(1959)
F. R. Clarke, T. G. Birdsall, and W. P. Tanner Jr
Two types of ROC curves and definitions of parameters
.
The Journal of the Acoustical Society of America
31
(
5
),
pp. 629–630
.
Cited by:
§1
,
§2
,
§3
.
Committee (2021)
O. A. D. (. Committee
Taxonomy and definitions for terms related to driving automation systems for on-road motor vehicles
.
SAE international
,
Warrendale, PA, USA
.
Note:
Accessed: 25 February 2026.
External Links:
Link
Cited by:
item 1
.
Connell and Lynott (2024)
L. Connell and D. Lynott
What can language models tell us about human cognition?
.
Current Directions in Psychological Science
33
(
3
),
pp. 181–189
.
Cited by:
§3
.
Cox (2005)
C. Cox
Delta method
.
Encyclopedia of biostatistics
2
.
Cited by:
§4
.
Dai (2026)
Y. Dai
Rescaling confidence: what scale design reveals about LLM metacognition
.
arXiv preprint arXiv:2603.09309
.
Cited by:
§1
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
Cited by:
§1
,
§3
.
[14]
DeepSeek
DeepSeek api documentation: change log
.
Note:
https://api-docs.deepseek.com/updates
Accessed: 24 February 2026.
Cited by:
item 2
.
Dunn (1961)
O. J. Dunn
Multiple comparisons among means
.
Journal of the American statistical association
56
(
293
),
pp. 52–64
.
Cited by:
§4
.
Fadeeva
et al.
(2023)
E. Fadeeva, R. Vashurin, A. Tsvigun, A. Vazhentsev, S. Petrakov, K. Fedyanin, D. Vasilev, E. Goncharova, A. Panchenko, M. Panov,
et al.
LM-polygraph: uncertainty estimation for language models
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations
,
pp. 446–461
.
Cited by:
§3
.
Fleming (2017)
S. M. Fleming
HMeta-d: hierarchical bayesian estimation of metacognitive efficiency from confidence ratings
.
Neuroscience of consciousness
2017
(
1
),
pp. nix007
.
Cited by:
§1
,
§1
,
§4
,
§4
,
§4
,
Figure S3
.
Fleming (2024)
S. M. Fleming
Metacognition and confidence: a review and synthesis
.
Annual Review of Psychology
75
(
1
),
pp. 241–268
.
Cited by:
§1
.
Galvin
et al.
(2003)
S. J. Galvin, J. V. Podd, V. Drga, and J. Whitmore
Type 2 tasks in the theory of signal detectability: discrimination between correct and incorrect decisions
.
Psychonomic bulletin & review
10
(
4
),
pp. 843–876
.
Cited by:
§1
.
Gomez
et al.
(2025)
C. Gomez, S. M. Cho, S. Ke, C. Huang, and M. Unberath
Human-AI collaboration is not very collaborative yet: a taxonomy of interaction patterns in AI-assisted decision making from a systematic review
.
Frontiers in Computer Science
6
,
pp. 1521066
.
Cited by:
§1
.
Green
et al.
(1966)
D. M. Green J. A. Swets
et al.
Signal detection theory and psychophysics
.
Vol.
1
,
Wiley
,
New York
.
Cited by:
§1
.
Guggenmos (2021)
M. Guggenmos
Measuring metacognitive performance: type 1 performance dependence and test-retest reliability
.
Neuroscience of consciousness
2021
(
1
),
pp. niab040
.
Cited by:
§1
.
Hwang and Chang (2023)
G. Hwang and C. Chang
A review of opportunities and challenges of chatbots in education
.
Interactive Learning Environments
31
(
7
),
pp. 4099–4112
.
Cited by:
§1
.
Jumper
et al.
(2021)
J. Jumper, R. Evans, A. Pritzel, T. Green, M. Figurnov, O. Ronneberger, K. Tunyasuvunakool, R. Bates, A. Žídek, A. Potapenko,
et al.
Highly accurate protein structure prediction with alphafold
.
nature
596
(
7873
),
pp. 583–589
.
Cited by:
§1
.
Koriat (2012)
A. Koriat
When are two heads better than one and why?
.
Science
336
(
6079
),
pp. 360–362
.
Cited by:
§1
.
Kumaran
et al.
(2026a)
D. Kumaran, A. Conmy, F. Barbero, S. Osindero, V. Patraucean, and P. Veličković
How do LLMs compute verbal confidence
.
arXiv preprint arXiv:2603.17839
.
Cited by:
§3
.
Kumaran
et al.
(2026b)
D. Kumaran, N. Daw, S. Osindero, P. Veličković, and V. Patraucean
Causal evidence that language models use confidence to drive behavior
.
arXiv preprint arXiv:2603.22161
.
Cited by:
§3
.
Kumaran
et al.
(2026c)
D. Kumaran, V. Patraucean, M. Ovsjanikov, P. Veličković, and N. Daw
The computational basis of confidence in large language models
.
arXiv preprint arXiv:2607.12447
.
Cited by:
§3
.
Lattimore and Szepesvári (2020)
T. Lattimore and C. Szepesvári
Bandit algorithms
.
Cambridge University Press
.
Cited by:
§3
.
Lee
et al.
(2025)
D. Lee, J. Pruitt, T. Zhou, J. Du, and B. Odegaard
Metacognitive sensitivity: the key to calibrating trust and optimal decision making with AI
.
PNAS nexus
4
(
5
),
pp. pgaf133
.
Cited by:
§1
.
Li and Steyvers (2025)
Z. Li and M. Steyvers
Beyond accuracy: how AI metacognitive sensitivity improves AI-assisted decision making
.
arXiv preprint arXiv:2507.22365
.
Cited by:
§1
,
§1
,
§1
.
Louapre (2026)
D. Louapre
Can LLMs play the game of science? the eleusis benchmark
.
Note:
https://huggingface.co/spaces/huggingface/eleusis-benchmark
Open access benchmark on Hugging Face Spaces
Cited by:
§3
.
Macmillan and Creelman (2005)
N. A. Macmillan and Creelman
Detection theory: a user’s guide
.
Lawrence Erlbaum
,
New York
.
Cited by:
§1
.
Makowski
et al.
(2019)
D. Makowski, M. S. Ben-Shachar, and D. Lüdecke
BayestestR: describing effects and their uncertainty, existence and significance within the bayesian framework
.
Journal of open source software
4
(
40
),
pp. 1541
.
Cited by:
§2
,
§4
.
Makridakis (2017)
S. Makridakis
The forthcoming artificial intelligence (AI) revolution: its impact on society and firms
.
Futures
90
,
pp. 46–60
.
Cited by:
§1
.
Maniscalco and Lau (2012)
B. Maniscalco and H. Lau
A signal detection theoretic approach for estimating metacognitive sensitivity from confidence ratings
.
Consciousness and cognition
21
(
1
),
pp. 422–430
.
Cited by:
§1
.
Maniscalco and Lau (2014)
B. Maniscalco and H. Lau
Signal detection theory analysis of type 1 and type 2 data: meta-
d
′
\mathchar 29028^{\mathchar 560}
, response-specific meta-
d
′
\mathchar 29028^{\mathchar 560}
, and the unequal variance SDT model
.
In
The cognitive neuroscience of metacognition
,
pp. 25–66
.
Cited by:
§1
,
§1
,
§3
,
§4
,
§4
.
Mazancieux
et al.
(2020)
A. Mazancieux, C. Dinze, C. Souchay, and C. J. Moulin
Metacognitive domain specificity in feeling-of-knowing but not retrospective confidence
.
Neuroscience of Consciousness
2020
(
1
),
pp. niaa001
.
Cited by:
§1
.
Mehlhorn
et al.
(2015)
K. Mehlhorn, B. R. Newell, P. M. Todd, M. D. Lee, K. Morgan, V. A. Braithwaite, D. Hausmann, K. Fiedler, and C. Gonzalez
Unpacking the exploration–exploitation tradeoff: a synthesis of human and animal literatures.
.
Decision
2
(
3
),
pp. 191
.
Cited by:
§1
.
Meunier-Duperray
et al.
(2025)
L. Meunier-Duperray, A. Mazancieux, C. Souchay, S. M. Fleming, C. Bastin, C. J. Moulin, and L. Angel
Does age affect metacognition? a cross-domain investigation using a hierarchical bayesian framework
.
Cognition
258
,
pp. 106089
.
Cited by:
§1
.
Miyoshi
et al.
(2026)
K. Miyoshi, D. Rahnev, and H. Lau
Correcting for unequal variance in signal detection models using response time
.
iScience
.
Cited by:
§1
,
§3
.
Miyoshi
et al.
(2022)
K. Miyoshi, Y. Sakamoto, and S. Nishida
On the assumptions behind metacognitive measurements: implications for theory and practice
.
Journal of Vision
22
(
10
),
pp. 18–18
.
Cited by:
§3
.
Molenberghs
et al.
(2016)
P. Molenberghs, F. Trautwein, A. Böckler, T. Singer, and P. Kanske
Neural correlates of metacognitive ability and of feeling confident: a large-scale fMRI study
.
Social cognitive and affective neuroscience
11
(
12
),
pp. 1942–1951
.
Cited by:
§3
.
Nguyen
et al.
(2025)
D. Nguyen, R. Bhattacharyya, C. Colombatto, S. Fleming, I. Posner, and N. Hawes
Joint decision-making in robot teleoperation: when are two heads better than one?
.
arXiv preprint arXiv:2503.15510
.
Cited by:
§1
.
OpenAI (2022)
OpenAI
Introducing ChatGPT
.
Note:
https://openai.com/blog/chatgpt
Accessed: 9 Septembre 2026
Cited by:
§1
.
OpenAI (2026)
OpenAI
Create chat completion
.
Note:
https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
Accessed: 27 March 2026
Cited by:
item 2
.
Parr
et al.
(2022)
T. Parr, G. Pezzulo, and K. J. Friston
Active inference: the free energy principle in mind, brain, and behavior
.
MIT Press
,
Cambridge, MA
.
Cited by:
§1
.
Platt and Huettel (2008)
M. L. Platt and S. A. Huettel
Risky business: the neuroeconomics of decision making under uncertainty
.
Nature neuroscience
11
(
4
),
pp. 398–403
.
Cited by:
§1
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
Cited by:
§1
,
§3
.
Rausch
et al.
(2023)
M. Rausch, S. Hellmann, and M. Zehetleitner
Measures of metacognitive efficiency across cognitive models of decision confidence.
.
Psychological Methods
.
Cited by:
§1
.
Rausch
et al.
(2015)
M. Rausch, H. J. Müller, and M. Zehetleitner
Metacognitive sensitivity of subjective reports of decisional confidence and visual experience
.
Consciousness and cognition
35
,
pp. 192–205
.
Cited by:
§1
.
Rillig
et al.
(2023)
M. C. Rillig, M. Ågerstrand, M. Bi, K. A. Gould, and U. Sauerland
Risks and benefits of large language models for the environment
.
Environmental science & technology
57
(
9
),
pp. 3464–3466
.
Cited by:
§1
.
Seo
et al.
(2026)
K. Seo, S. Lim, and T. Kim
ADVICE: answer-dependent verbalized confidence estimation
.
In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 23942–23962
.
Cited by:
§1
.
Shorinwa
et al.
(2025)
O. Shorinwa, Z. Mei, J. Lidard, A. Z. Ren, and A. Majumdar
A survey on uncertainty quantification of large language models: taxonomy, open research challenges, and future directions
.
ACM Computing Surveys
58
(
3
),
pp. 1–38
.
Cited by:
§3
.
Steyvers
et al.
(2025a)
M. Steyvers, C. Belem, and P. Smyth
Improving metacognition and uncertainty communication in language models
.
arXiv preprint arXiv:2510.05126
.
Cited by:
§1
.
Steyvers and Peters (2025)
M. Steyvers and M. A. Peters
Metacognition and uncertainty communication in humans and large language models
.
Current Directions in Psychological Science
,
pp. 09637214251391158
.
Cited by:
§1
.
Steyvers
et al.
(2022)
M. Steyvers, H. Tejeda, G. Kerrigan, and P. Smyth
Bayesian modeling of human–AI complementarity
.
Proceedings of the National Academy of Sciences
119
(
11
),
pp. e2111547119
.
Cited by:
item 2
,
§1
.
Steyvers
et al.
(2025b)
M. Steyvers, H. Tejeda, A. Kumar, C. Belem, S. Karny, X. Hu, L. W. Mayer, and P. Smyth
What large language models know and what people think they know
.
Nature Machine Intelligence
7
(
2
),
pp. 221–231
.
Cited by:
§1
,
§3
,
§3
.
Stone
et al.
(2022)
P. Stone, R. Brooks, E. Brynjolfsson, R. Calo, O. Etzioni, G. Hager, J. Hirschberg, S. Kalyanakrishnan, E. Kamar, S. Kraus,
et al.
Artificial intelligence and life in 2030: the one hundred year study on artificial intelligence
.
arXiv preprint arXiv:2211.06318
.
Cited by:
§1
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
§3
.
Topics (2025)
E. Topics
40+ chatbot statistics (2025)
.
Note:
Accessed 9 September 2025
https://explodingtopics.com/blog/chatbot-statistics
Cited by:
§1
.
Trinh
et al.
(2025)
L. T. M. Trinh, L. M. V. Pham, T. M. A. Pham, and A. D. Nguyen
Metacognitive sensitivity for test-time dynamic model selection
.
arXiv preprint arXiv:2512.10451
.
Cited by:
§1
.
Tyler and Chen (2000)
C. W. Tyler and C. Chen
Signal detection theory in the 2afc paradigm: attention, channel uncertainty and probability summation
.
Vision research
40
(
22
),
pp. 3121–3144
.
Cited by:
§3
.
Vo
et al.
(2019)
N. N. Vo, X. He, S. Liu, and G. Xu
Deep learning for decision making and the optimization of socially responsible investments and portfolio
.
Decision Support Systems
124
,
pp. 113097
.
Cited by:
§1
.
Von Neumann and Morgenstern (2007)
J. Von Neumann and O. Morgenstern
Theory of games and economic behavior
.
In
Theory of games and economic behavior
,
Cited by:
§1
.
Vuorre and Metcalfe (2022)
M. Vuorre and J. Metcalfe
Measures of relative metacognitive accuracy are confounded with task performance in tasks that permit guessing
.
Metacognition and Learning
17
(
2
),
pp. 269–291
.
Cited by:
§3
.
Wang
et al.
(2025)
G. Wang, W. Wu, G. Ye, Z. Cheng, X. Chen, and H. Zheng
Decoupling metacognition from cognition: a framework for quantifying metacognitive ability in LLMs
.
In
Proceedings of the AAAI Conference on Artificial Intelligence
,
Vol.
39
,
pp. 25353–25361
.
Cited by:
§1
,
§3
.
Weidinger
et al.
(2021)
L. Weidinger, J. Mellor, M. Rauh, C. Griffin, J. Uesato, P. Huang, M. Cheng, M. Glaese, B. Balle, A. Kasirzadeh,
et al.
Ethical and social risks of harm from language models
.
arXiv preprint arXiv:2112.04359
.
Cited by:
§1
.
Wickens (2001)
T. D. Wickens
Elementary signal detection theory
.
Oxford university press
,
Oxford
.
Cited by:
§1
.
Xiong
et al.
(2023)
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi
Can LLMs express their uncertainty? an empirical evaluation of confidence elicitation in LLMs
.
arXiv preprint arXiv:2306.13063
.
Cited by:
§1
,
§3
.
Xue
et al.
(2021)
K. Xue, M. Shekhar, and D. Rahnev
Examining the robustness of the relationship between metacognitive efficiency and metacognitive bias
.
Consciousness and Cognition
95
,
pp. 103196
.
Cited by:
§1
.
Ye
et al.
(2024)
F. Ye, M. Yang, J. Pang, L. Wang, D. F. Wong, E. Yilmaz, S. Shi, and Z. Tu
Benchmarking LLMs via uncertainty quantification
.
Advances in Neural Information Processing Systems
37
,
pp. 15356–15385
.
Cited by:
§3
.
Zhang
et al.
(2025)
Y. Zhang, Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, Y. Chen,
et al.
Siren’s song in the AI ocean: a survey on hallucination in large language models
.
Computational Linguistics
51
(
4
),
pp. 1373–1418
.
Cited by:
§3
.
Supplementary material
Figure S1:
Conditional proportion of confidence rating given that the response at the type 1 task was correct (green; right bars) or incorrect (red; left bars), or
P
⁡
(
confidence
=
C
i
|
correct or incorrect at type 1 task
)
\mathchar 29008\delimiter 67273472\text{confidence}\mathchar 12349\mathchar 28995_{\mathchar 29033}\mathchar 12906\text{correct or incorrect at type 1 task}\delimiter 84054785
for task A (first row), task B (middle row) and task C (bottom row). See
Figure
1
for further details.
Figure S2:
c
′
=
c
/
d
′
\mathchar 29027^{\mathchar 560}\mathchar 12349\mathchar 29027\delimiter 68408078\mathchar 29028^{\mathchar 560}
across three risk configurations (“S1”, “None” , “S2”) within task A (top row), task B (middle row) and task C (bottom row), for GPT-5 (left column), DeepSeek-V3.2-Exp (middle column), and Mistral-Medium-2508 (right column). Error bars represent 95% confidence intervals estimated via the Delta method. See the Methods for details.
Figure S3:
Average
d
′
\mathchar 29028^{\mathchar 560}
(a) and meta-
d
′
\mathchar 29028^{\mathchar 560}
(b) versus number of trials. Each data point is the estimated
d
′
\mathchar 29028^{\mathchar 560}
and meta-
d
′
\mathchar 29028^{\mathchar 560}
, averaged over 20 repetitions, where each
d
′
\mathchar 29028^{\mathchar 560}
and meta-
d
′
\mathchar 29028^{\mathchar 560}
is computed with a given number of trials that is tuned in the x-axis. Error bars correspond to standard deviations. In panel (a), the error bars vanish because the simulation procedure deterministically set the type 1 response counts. The data has been generated using the function
exampleFit.m
from Ref.
Fleming (2017)
, available at
https://github.com/smfleming/HMeta-d
, with the true
d
′
\mathchar 29028^{\mathchar 560}
and meta-
d
′
\mathchar 29028^{\mathchar 560}
, indicated by a red horizontal dashed line in each panel, equal to 3.2 and 3 (i.e., very high type 1 sensitivity and high metacognitive efficiency), respectively. Type 1 criterion
c
=
0
\mathchar 29027\mathchar 12349\mathchar 28720
and type 2 criteria are as follows:
c1 = [-2 -1.5 -1 -0.5]
,
c2 = [0.5 1 1.5 2]
.
GPT-5
DeepSeek-V3.2-Exp
Mistral-Medium-2508
Estimation
9
​
5
%
\mathchar 28729\mathchar 28725\%
CI
Estimation
9
​
5
%
\mathchar 28729\mathchar 28725\%
CI
Estimation
9
​
5
%
\mathchar 28729\mathchar 28725\%
CI
Task A
d
′
\mathchar 29028^{\mathchar 560}
3.2396
[
3
.
1
7
7
6
,
3
.
3
0
3
1
]
\delimiter 67482370\mathchar 28723\mathchar 314\mathchar 28721\mathchar 28727\mathchar 28727\mathchar 28726\mathchar 24891\;\mathchar 28723\mathchar 314\mathchar 28723\mathchar 28720\mathchar 28723\mathchar 28721\delimiter 84267779
3.2425
[
3
.
1
8
2
3
,
3
.
3
0
4
0
]
\delimiter 67482370\mathchar 28723\mathchar 314\mathchar 28721\mathchar 28728\mathchar 28722\mathchar 28723\mathchar 24891\;\mathchar 28723\mathchar 314\mathchar 28723\mathchar 28720\mathchar 28724\mathchar 28720\delimiter 84267779
3.2700
[
3
.
2
0
5
8
,
3
.
3
3
5
9
]
\delimiter 67482370\mathchar 28723\mathchar 314\mathchar 28722\mathchar 28720\mathchar 28725\mathchar 28728\mathchar 24891\;\mathchar 28723\mathchar 314\mathchar 28723\mathchar 28723\mathchar 28725\mathchar 28729\delimiter 84267779
meta-
d
′
\mathchar 29028^{\mathchar 560}
2.7738
[
2
.
6
8
3
0
,
2
.
8
6
2
7
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28726\mathchar 28728\mathchar 28723\mathchar 28720\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28728\mathchar 28726\mathchar 28722\mathchar 28727\delimiter 84267779
2.2530
[
2
.
1
5
7
5
,
2
.
3
4
9
9
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28721\mathchar 28725\mathchar 28727\mathchar 28725\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28723\mathchar 28724\mathchar 28729\mathchar 28729\delimiter 84267779
2.9398
[
2
.
8
4
6
2
,
3
.
0
3
3
4
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28728\mathchar 28724\mathchar 28726\mathchar 28722\mathchar 24891\;\mathchar 28723\mathchar 314\mathchar 28720\mathchar 28723\mathchar 28723\mathchar 28724\delimiter 84267779
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
0.8563
[
0
.
8
2
3
2
,
0
.
8
8
8
9
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28722\mathchar 28723\mathchar 28722\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28728\mathchar 28728\mathchar 28729\delimiter 84267779
0.6949
[
0
.
6
6
2
4
,
0
.
7
2
8
3
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28726\mathchar 28726\mathchar 28722\mathchar 28724\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28722\mathchar 28728\mathchar 28723\delimiter 84267779
0.8991
[
0
.
8
6
4
8
,
0
.
9
3
4
4
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28726\mathchar 28724\mathchar 28728\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28729\mathchar 28723\mathchar 28724\mathchar 28724\delimiter 84267779
AUC2
0.8740
[
0
.
8
6
5
9
,
0
.
8
8
2
1
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28726\mathchar 28725\mathchar 28729\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28728\mathchar 28722\mathchar 28721\delimiter 84267779
0.8046
[
0
.
7
9
3
8
,
0
.
8
1
5
4
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28729\mathchar 28723\mathchar 28728\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28721\mathchar 28725\mathchar 28724\delimiter 84267779
0.8517
[
0
.
8
4
3
3
,
0
.
8
6
0
0
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28724\mathchar 28723\mathchar 28723\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28726\mathchar 28720\mathchar 28720\delimiter 84267779
Task B
d
′
\mathchar 29028^{\mathchar 560}
2.3074
[
2
.
2
4
4
2
,
2
.
3
7
0
6
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28722\mathchar 28724\mathchar 28724\mathchar 28722\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28723\mathchar 28727\mathchar 28720\mathchar 28726\delimiter 84267779
2.5217
[
2
.
4
5
5
3
,
2
.
5
8
8
5
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28724\mathchar 28725\mathchar 28725\mathchar 28723\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28725\mathchar 28728\mathchar 28728\mathchar 28725\delimiter 84267779
2.2968
[
2
.
2
3
4
3
,
2
.
3
5
9
6
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28722\mathchar 28723\mathchar 28724\mathchar 28723\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28723\mathchar 28725\mathchar 28729\mathchar 28726\delimiter 84267779
meta-
d
′
\mathchar 29028^{\mathchar 560}
1.9972
[
1
.
8
7
7
2
,
2
.
1
1
3
6
]
\delimiter 67482370\mathchar 28721\mathchar 314\mathchar 28728\mathchar 28727\mathchar 28727\mathchar 28722\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28721\mathchar 28721\mathchar 28723\mathchar 28726\delimiter 84267779
1.6510
[
1
.
4
9
3
9
,
1
.
8
0
1
2
]
\delimiter 67482370\mathchar 28721\mathchar 314\mathchar 28724\mathchar 28729\mathchar 28723\mathchar 28729\mathchar 24891\;\mathchar 28721\mathchar 314\mathchar 28728\mathchar 28720\mathchar 28721\mathchar 28722\delimiter 84267779
1.7743
[
1
.
6
3
8
5
,
1
.
9
1
0
0
]
\delimiter 67482370\mathchar 28721\mathchar 314\mathchar 28726\mathchar 28723\mathchar 28728\mathchar 28725\mathchar 24891\;\mathchar 28721\mathchar 314\mathchar 28729\mathchar 28721\mathchar 28720\mathchar 28720\delimiter 84267779
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
0.8658
[
0
.
8
0
9
4
,
0
.
9
2
2
5
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28720\mathchar 28729\mathchar 28724\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28729\mathchar 28722\mathchar 28722\mathchar 28725\delimiter 84267779
0.6548
[
0
.
5
9
1
1
,
0
.
7
1
7
4
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28725\mathchar 28729\mathchar 28721\mathchar 28721\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28721\mathchar 28727\mathchar 28724\delimiter 84267779
0.7727
[
0
.
7
1
0
4
,
0
.
8
3
5
8
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28721\mathchar 28720\mathchar 28724\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28723\mathchar 28725\mathchar 28728\delimiter 84267779
AUC2
0.7263
[
0
.
7
1
4
3
,
0
.
7
3
8
2
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28721\mathchar 28724\mathchar 28723\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28723\mathchar 28728\mathchar 28722\delimiter 84267779
0.6288
[
0
.
6
1
4
5
,
0
.
6
4
3
2
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28726\mathchar 28721\mathchar 28724\mathchar 28725\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28726\mathchar 28724\mathchar 28723\mathchar 28722\delimiter 84267779
0.6677
[
0
.
6
5
5
2
,
0
.
6
8
0
1
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28726\mathchar 28725\mathchar 28725\mathchar 28722\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28726\mathchar 28728\mathchar 28720\mathchar 28721\delimiter 84267779
Task C
d
′
\mathchar 29028^{\mathchar 560}
2.8414
[
2
.
7
6
8
3
,
2
.
9
1
4
8
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28727\mathchar 28726\mathchar 28728\mathchar 28723\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28729\mathchar 28721\mathchar 28724\mathchar 28728\delimiter 84267779
1.2565
[
1
.
1
9
4
0
,
1
.
3
1
9
2
]
\delimiter 67482370\mathchar 28721\mathchar 314\mathchar 28721\mathchar 28729\mathchar 28724\mathchar 28720\mathchar 24891\;\mathchar 28721\mathchar 314\mathchar 28723\mathchar 28721\mathchar 28729\mathchar 28722\delimiter 84267779
1.2369
[
1
.
1
8
5
0
,
1
.
2
8
8
7
]
\delimiter 67482370\mathchar 28721\mathchar 314\mathchar 28721\mathchar 28728\mathchar 28725\mathchar 28720\mathchar 24891\;\mathchar 28721\mathchar 314\mathchar 28722\mathchar 28728\mathchar 28728\mathchar 28727\delimiter 84267779
meta-
d
′
\mathchar 29028^{\mathchar 560}
2.3522
[
2
.
2
1
7
8
,
2
.
4
8
8
6
]
\delimiter 67482370\mathchar 28722\mathchar 314\mathchar 28722\mathchar 28721\mathchar 28727\mathchar 28728\mathchar 24891\;\mathchar 28722\mathchar 314\mathchar 28724\mathchar 28728\mathchar 28728\mathchar 28726\delimiter 84267779
0.8866
[
0
.
7
8
9
7
,
0
.
9
8
2
4
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28728\mathchar 28729\mathchar 28727\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28729\mathchar 28728\mathchar 28722\mathchar 28724\delimiter 84267779
0.8589
[
0
.
7
1
9
3
,
0
.
9
9
9
0
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28721\mathchar 28729\mathchar 28723\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28729\mathchar 28729\mathchar 28729\mathchar 28720\delimiter 84267779
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
0.8280
[
0
.
7
7
6
0
,
0
.
8
8
0
5
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28727\mathchar 28726\mathchar 28720\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28728\mathchar 28720\mathchar 28725\delimiter 84267779
0.7061
[
0
.
6
2
3
2
,
0
.
7
9
2
5
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28726\mathchar 28722\mathchar 28723\mathchar 28722\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28729\mathchar 28722\mathchar 28725\delimiter 84267779
0.6947
[
0
.
5
7
8
3
,
0
.
8
1
3
4
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28725\mathchar 28727\mathchar 28728\mathchar 28723\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28728\mathchar 28721\mathchar 28723\mathchar 28724\delimiter 84267779
AUC2
0.7719
[
0
.
7
5
6
5
,
0
.
7
8
7
3
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28725\mathchar 28726\mathchar 28725\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28727\mathchar 28728\mathchar 28727\mathchar 28723\delimiter 84267779
0.5651
[
0
.
5
5
6
0
,
0
.
5
7
4
2
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28725\mathchar 28725\mathchar 28726\mathchar 28720\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28725\mathchar 28727\mathchar 28724\mathchar 28722\delimiter 84267779
0.5455
[
0
.
5
3
6
9
,
0
.
5
5
4
0
]
\delimiter 67482370\mathchar 28720\mathchar 314\mathchar 28725\mathchar 28723\mathchar 28726\mathchar 28729\mathchar 24891\;\mathchar 28720\mathchar 314\mathchar 28725\mathchar 28725\mathchar 28724\mathchar 28720\delimiter 84267779
Table S1:
Estimated
d
′
\mathchar 29028^{\mathchar 560}
, meta-
d
′
\mathchar 29028^{\mathchar 560}
,
M
r
​
a
​
t
​
i
​
o
\mathchar 29005_{\mathchar 29042\mathchar 29025\mathchar 29044\mathchar 29033\mathchar 29039}
and AUC2
across models and tasks, and associated 95% confidence intervals (CIs; see the Methods for details). Note that the
9
​
5
%
\mathchar 28729\mathchar 28725\%
CIs of differences mentioned in the main text should not be confused with the individual CIs.
GPT-5
DeepSeek-V3.2-Exp
Mistral-Medium-2508
Estimation
9
​
5
%
\mathchar 28729\mathchar 28725\%
CI
Estimation
9
​
5
%
\mathchar 28729\mathchar 28725\%
CI
Estimation
9
​
5
%
\mathchar 28729\mathchar 28725\%
CI
Task A
S1
-0.6304
±0.0330
0.1356
±0.0291
0.1427
±0.0291
None
0.2532
±0.0308
0.2149
±0.0300
0.3927
±0.0324
S2
0.9289
±0.0452
0.3116
±0.0303
0.6975
±0.0388
Task B
S1
-1.2098
±0.0537
-0.4319
±0.0362
-0.2748
±0.0328
None
-0.1324
±0.0316
0.0465
±0.0324
0.1666
±0.0317
S2
1.0002
±0.0422
0.2301
±0.0324
0.1487
±0.0318
Task C
S1
-1.4297
±0.0644
0.3885
±0.0283
0.1243
±0.0273
None
-0.0265
±0.0360
0.3584
±0.0283
0.2116
±0.0277
S2
0.7668
±0.0465
0.8260
±0.0323
0.5743
±0.0300
Table S2:
Estimated
c
\mathchar 29027
across models, tasks, and risk configurations (“S1”, “None”, “S2’), and associated 95% confidence intervals (CIs; see the Methods for details).