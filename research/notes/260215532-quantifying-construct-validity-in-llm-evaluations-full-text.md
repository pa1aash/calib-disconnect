---
title: '[2602.15532] Quantifying construct validity in LLM evaluations (full text)'
id: 260215532-quantifying-construct-validity-in-llm-evaluations-full-text
tags:
- code-llm-confidence-positioning-d82d00
- related
created: '2026-11-09T23:11:27.933920Z'
updated: '2026-11-09T23:27:44.725328Z'
source: https://arxiv.org/pdf/2602.15532
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT. Oxford MSc thesis (Kearns, 2026): structured capabilities model
  separating capability from scale and measurement error on OpenLLM Leaderboard; measurement-theory
  construct validity at benchmark level, not confidence calibration. Related-only
  for framing F.'
---

U NIVERSITY OF OXFORD
 Quantifying construct validity in large language model evaluations
arXiv:2602.15532v1 [cs.AI] 17 Feb 2026
 Ryan Othniel Kearns
 St Catherine’s College
 Supervisor: Prof. Adam Mahdi
 Thesis submitted in partial fulfilment of the requirement for the degree of MSc in Social
 Data Science at the Oxford Internet Institute at the University of Oxford.
 Trinity Term 2025 12348 words
 Abstract
The large language model research community often reports benchmark results as
if they are synonymous with general model capabilities. For example, an LLM per-
forming well on a mathematics benchmark is taken to have a general mathematical
reasoning ability. However, benchmarks can have problems that distort performance,
like test set contamination and annotator error. How can we know that a benchmark
is a reliable indicator of some capability that we want to measure? This question con-
cerns the construct validity of LLM benchmarks, and it requires separating bench-
mark results from capabilities when we model and predict LLM performance.
Both social scientists and computer scientists propose formal models for identifying
the capabilities underlying benchmark scores. Social scientists adapt latent factor
models, used for modelling human cognitive capabilities, to explain LLM bench-
mark performance. Computer scientists adapt neural scaling laws, used for predict-
ing LLM performance from model size, to model capabilities. These techniques
approach the problem from opposite ends, and both can produce capability estimates
that are more robust than individual benchmark scores. However, neither technique
is satisfactory for construct validity. The social science models ignore scaling laws,
and as a result, the capabilities they extract often proxy model size. The computer
science models ignore measurement error, and as a result, the capabilities they extract
are both uninterpretable and overfit to the observed benchmarks.
This thesis presents the structured capabilities model, the first model to extract in-
terpretable and generalisable capabilities from a large collection of LLM benchmark
results. I fit this model and its two alternatives on a large sample of results from the
OpenLLM Leaderboard. Compared to latent factor models, the structured capabil-
ities model performs better according to parsimonious fit indices, and it removes a
problematic dominant factor that appears to be a proxy for model scale. Compared
to scaling law models, the structured capabilities model fits capability estimates that
generalise to out-of-distribution benchmarks with higher predictive accuracy. These
improvements are possible because neither existing approach separates model scale
from capabilities in the appropriate way. Model scale should inform capabilities, as
in scaling laws, and these capabilities should inform observed results up to measure-
ment error, as in latent factor models. In combining these two insights, structured
capabilities demonstrate better explanatory and predictive power for quantifying con-
struct validity in LLM evaluations.
Contents
1 Introduction 1
 1.1 Large language models: A “superhuman” intelligence? . . . . . . . . . . 1
 1.2 The evaluation crisis . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
 1.3 Can construct validity solve the evaluation crisis? . . . . . . . . . . . . . 2
 1.4 The gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
 1.5 My contribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
2 Background 7
 2.1 Scaling laws and LLM capabilities . . . . . . . . . . . . . . . . . . . . . 7
 2.2 Quantifying construct validity . . . . . . . . . . . . . . . . . . . . . . . 10
 2.3 Related work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
 2.4 Research questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
3 Methods 19
 3.1 Experimental design . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
 3.2 Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
 3.3 Techniques and models . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
 3.4 Validation and experimentation . . . . . . . . . . . . . . . . . . . . . . . 27
4 Results 31
 4.1 Preliminary data analysis . . . . . . . . . . . . . . . . . . . . . . . . . . 31
 4.2 Comparison to exploratory factor analysis . . . . . . . . . . . . . . . . . 36
 4.3 Comparison to observational scaling laws . . . . . . . . . . . . . . . . . 39
5 Discussion 44
 5.1 Principal findings . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 44
 5.2 Interpretation of results . . . . . . . . . . . . . . . . . . . . . . . . . . . 44
 5.3 Relation to other studies . . . . . . . . . . . . . . . . . . . . . . . . . . 46
 5.4 Limitations and future work . . . . . . . . . . . . . . . . . . . . . . . . 47
 5.5 Implications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 48
6 Conclusion 50
References 51
A List of mentioned benchmarks 68
B Default mathematical notation 70
C BIG-Bench Hard task descriptions 73
D Transformed matrix derivation 81
E Parameter scaling laws for all BBH subtasks 82
List of Figures
 1 High-level picture of my contribution . . . . . . . . . . . . . . . . . . . 6
 2 The scale of language model training, 2010 to 2025 . . . . . . . . . . . . 8
 3 Illustrated three-parameter item response curve . . . . . . . . . . . . . . 24
 4 Raw BBH score correlation matrix . . . . . . . . . . . . . . . . . . . . . 32
 5 Logistic scaling law fits for two subtasks . . . . . . . . . . . . . . . . . . 33
 6 BBH score residuals correlation matrix . . . . . . . . . . . . . . . . . . . 34
 7 Scree plots for BBH score matrices . . . . . . . . . . . . . . . . . . . . . 35
 8 Linear latent factor model results . . . . . . . . . . . . . . . . . . . . . . 37
 9 Structured capabilities model results . . . . . . . . . . . . . . . . . . . . 38
 10 Parameter estimates for the observational scaling law model . . . . . . . 41
 11 Parameter estimates for the structured capabilities model . . . . . . . . . 42
 12 Variance explained by estimated capabilities . . . . . . . . . . . . . . . . 43
 13 Raw BBH scores against log-parameter size . . . . . . . . . . . . . . . . 83
List of Tables
 1 BIG-Bench Hard subtasks in our dataset . . . . . . . . . . . . . . . . . . 22
 2 Fit measures for the four tested EFA models . . . . . . . . . . . . . . . . 36
 3 Prediction errors for held-out subtasks . . . . . . . . . . . . . . . . . . . 40
 4 All mentioned benchmark datasets, with citations . . . . . . . . . . . . . 69
1 INTRODUCTION
1 Introduction
1.1 Large language models: A “superhuman” intelligence?
When we claim that large language models (LLMs) possess ‘scientific knowledge,’ or
‘mathematical reasoning abilities,’ how do we justify these claims?1 One method is anec-
dotal: individuals can ask an LLM some science or mathematics questions and come
away with an impression of the model’s abilities. This justification is neither very scal-
able nor scientific. A more robust method, and the standard method for modern AI
systems, is to use a benchmark dataset: a curated selection of questions and answers
that gives an objective measure of an LLM’s performance. Popular benchmarks measure
LLM performance on mathematics problems (Cobbe et al., 2021; Hendrycks et al., 2021;
Glazer et al., 2024), scientific questions (Rein et al., 2024; Wang et al., 2025), common-
sense language puzzles (Talmor et al., 2019; Sakaguchi et al., 2021), and code generation
tasks (Chen et al., 2021; Jimenez et al., 2024). On many benchmarks, LLMs achieve “su-
perhuman” performance, eclipsing the average human accuracy on these questions (Wang
et al., 2019). In fact, LLMs perform at superhuman levels on so many benchmarks
that some researchers worry we are running out of difficult tasks to benchmark. Others
claim that LLMs demonstrate the “sparks of artificial general intelligence” (Bubeck et al.,
2023), and recently published benchmarks feature dramatic names, like “Humanity’s Last
Exam” (Phan et al., 2025).
Benchmarks play an essential role in orienting progress in AI (Liang et al., 2023). Most
benchmarks are public artefacts, making LLM performance reproducible and indepen-
dently verifiable. Their clear, objective metrics signal current model performance to
policymakers and unsolved gaps to researchers (Potts, 2021). For the most part, AI re-
searchers report benchmark results as if they are synonymous with model capabilities:
if a model performs well on a benchmark of mathematics problems, it is taken to have
a mathematical problem-solving or reasoning capability (Kojima et al., 2022; Wei et al.,
2022; Srivastava et al., 2023).
1.2 The evaluation crisis
Unfortunately, benchmarks often give unreliable accounts of LLM capabilities. Datasets
can suffer contamination, which occurs when a model is exposed to benchmark data
 1
 In this thesis, I intend ‘single quotations’ to be read as scare quotes. “Double quotations” will indicate
direct quotation from a cited source. I will also use boldface to signify definitions for terms and italics for
general emphasis.
 1
1 INTRODUCTION 1.3 Can construct validity solve the evaluation crisis?
during training. Models can achieve unrealistic benchmark results by memorising data
through such exposure (Zhou et al., 2023b; Yang et al., 2023). Popular benchmarks can
be gamified by influential model providers. For example, Singh et al. (2025) show that
selective reporting of commercial model results has distorted model comparisons on the
Chatbot Arena leaderboard (Chiang et al., 2024). Benchmark scores can also give er-
roneous performance estimates simply due to human error when labelling the correct
answers (Kocijan et al., 2023). Even different choices of evaluation metrics can lead to
conflicting accounts of whether LLM capabilities are “emergent” in certain benchmark
results (Schaeffer et al., 2023; Burnell et al., 2023b). Finally, even when datasets are la-
belled correctly, reported fairly, and withheld from contamination, LLM performance can
challenge our expectations. Several studies show that seemingly meaningless alterations
to questions, like paraphrases, or changing names in arithmetic problems, can drastically
shift benchmark performance (Jiang et al., 2024; Mizrahi et al., 2024; Mirzadeh et al.,
2025).
This situation is paradoxical. LLMs appear “superhuman” across many tasks, and there
is strong anecdotal evidence that this technology represents a powerful and compelling
advancement in AI. Yet our ability to benchmark these systems seems to suffer from a
growing list of failures. Some researchers call the current moment an “evaluation crisis”
for LLMs (Karpathy, 2025).
An evaluation crisis affects not just the AI research community, but also policymakers and
society at large. Misplaced estimates of these capabilities can cause medical harms if AI
systems are deployed prematurely (Bean et al., 2025) and can obscure the labour market
impact of this transformative technology, hindering our possible economic and policy
responses (Frey & Osborne, 2023). Accurate capability measurements play an essential
role in the fairness and governance of AI systems (Jacobs & Wallach, 2021; Jacobs, 2021;
European Parliament, 2024).
1.3 Can construct validity solve the evaluation crisis?
Given all of the problems facing benchmarks, what can be done to secure reliable esti-
mates of LLM capabilities? According to one emerging narrative in AI research, the so-
lution can come from approaching the problem like social scientists (Wallach et al., 2024;
Salaudeen et al., 2025). To see this possibility, we must first observe that problems like
contamination, gamification, and annotator error affect the reliability of benchmarks—but
reliable benchmarks are not, in themselves, our ultimate goal. We seek reliable estimates
of LLM capabilities, and our benchmarks only serve to estimate these capabilities. Users
 2
1 INTRODUCTION 1.4 The gap
and policymakers do not really care whether a system performs well on any particular
mathematical benchmark. They care whether the system can do mathematics, as ulti-
mately this general capability determines if an LLM can file our taxes, price our insur-
ance, or teach mathematics to our children. If we had only one mathematical benchmark,
we would indeed be in trouble, but this is not our situation. We have many benchmarks
that claim to measure mathematical reasoning. Even if individual benchmarks have prob-
lems, though many separate measurements, we should be able to improve our estimation
of mathematical reasoning capabilities simply by the law of large numbers.
It is in this respect that the social sciences can help LLM evaluation. Our problem is
similar to one faced in disciplines like psychology. Psychology studies abstract phenom-
ena, like personality traits, and their measurement tools (like survey questions) are often
noisy and underspecified for these phenomena. As a result, psychological measurements
prioritise a condition called construct validity, which determines whether measurements
accurately reflect the phenomena (or constructs) they intend to measure (Cronbach &
Meehl, 1955). Measurement theory, the basis for construct validity, provides psycholo-
gists with formal models to assess and iteratively refine the validity of their measurement
tools (Clark & Watson, 2019). Central modern psychological concepts, like the Big Five
personality traits (Digman, 1990), are predicated on a literature of construct valid mea-
surements (Goldberg, 1992). Several AI position papers argue that LLM benchmarks
should justify and improve their connection to their own abstract phenomena, like mathe-
matical reasoning capabilities, in a similarly rigorous way (Raji et al., 2021; Wang et al.,
2023; Wallach et al., 2024; Alaa et al., 2025; Salaudeen et al., 2025). These formal stan-
dards could provide robustness against the varied issues of contamination, gamification,
and human annotator error, giving our evaluations the explanatory and predictive power
we need to trust LLM capabilities in the real world.
Construct validity offers us an escape from the evaluation crisis, though for it to work, we
need to apply measurement theory’s formal models to our LLM benchmark results. My
thesis addresses a gap in this application. Both social scientists and computer scientists
have published attempts at formal models of LLM capabilities, but to date no attempt
approaches the problem with the proper interdisciplinary perspective.
1.4 The gap
Formal models for construct validity amount to opinionated versions of dimensionality
reduction: they aim to relate a large number of indicators (benchmark scores) to a smaller
number of constructs (capability estimates). Separate studies from social scientists and
 3
1 INTRODUCTION 1.4 The gap
computer scientists try their hand at this modelling challenge with existing LLM bench-
mark results. The social scientists (Burnell et al., 2023a; Ilić & Gignac, 2024) attempt to
directly apply latent factor models, the models of human cognitive capabilities already
in use for construct validity (Fabrigar & Wegener, 2012; Kline, 2016). In parallel, com-
puter scientists approach this problem with their own established methods for predicting
LLM performance. Ruan et al. (2024) introduce observational scaling laws, adapting
the neural scaling laws that predict LLM performance as a function of their size (Ka-
plan et al., 2020; Henighan et al., 2020; Hoffmann et al., 2022). In place of size, Ruan
et al. (2024) use principal component analysis (PCA) to reduce a collection of benchmark
scores down to “capability vectors” that they plug into scaling laws to predict novel task
performance.
Both latent factor models (Burnell et al., 2023a; Ilić & Gignac, 2024) and observational
scaling laws (Ruan et al., 2024) succeed at translating LLM benchmark results into es-
timates for LLM capabilities. Unfortunately, though, both present deficiencies making
them unable to demonstrate construct validity. These deficiencies mostly arise because
they ignore something the other model does correctly. Latent factor models assume that
the only variables are the observed benchmark scores and the latent capabilities behind
them—they ignore the model size parameters at work in scaling laws. In human popu-
lations, there are no such scaling laws, and so pure latent models tend to be appropriate.
However, as we shall see, scale is such a dominant predictor of LLM performance that it
causes latent LLM capability estimates to effectively collapse into proxies for the LLM’s
parameter count. Modelling an observable design parameter is not ideal when the inten-
tion was to capture a latent capability. Yet, observational scaling laws fare no better with
their capability estimates. Ruan et al.’s approach proposes to extract capabilities from
benchmark scores with PCA, then to relate these capabilities to downstream performance
with scaling laws. Yet, again, since scale is the dominant predictor of LLM performance,
the principal component extracted proves to be another proxy for model scale. Moreover,
since PCA explains all variance in a ‘greedy’ fashion that we will explore, it proves to be
suboptimal for producing capabilities that generalise to novel tasks.
There should be a way to improve upon these initial attempts. Despite originating in
separate disciplines, we will show that their mathematical models differ by only a few
small assumptions. They also fail for the same reason: neither separates an LLM’s scale
from its capabilities in an appropriate way.
 4
1 INTRODUCTION 1.5 My contribution
1.5 My contribution
This thesis presents the structured capabilities model, the first model to extract inter-
pretable and generalisable capabilities from a large collection of LLM benchmark results.
The structured capabilities model combines latent factor models with observational scal-
ing laws, avoiding the deficiencies that both approaches present on their own.
In fitting this model to benchmark results from the OpenLLM Leaderboard, I observe
improvements that are communicable to both social scientists and computer scientists
interested in modelling LLM capabilities. To social scientists interested in formal models
of LLM capabilities, I demonstrate a more parsimonious model, with better fit statistics,
than the common latent factor model for extracting capabilities from benchmark results.
To computer scientists interested in predicting future model performance, I demonstrate
improved out-of-distribution generalisation for benchmark score prediction compared to
existing approaches based on observational scaling laws. My high-level approach and
contributions are depicted in Figure 1.
 5
1 INTRODUCTION 1.5 My contribution
Figure 1: High-level picture of my contribution. My proposed model, the structured
capabilities model, addresses problems in both latent factor and observational scaling
law approaches. These existing approaches do not sufficiently separate model scale from
capability estimates, which harms both their explanatory and their predictive power.
 6
2 BACKGROUND
2 Background
2.1 Scaling laws and LLM capabilities
This thesis concerns valid measurements of LLM capabilities. We observe these capabili-
ties in an LLM’s ‘behaviour.’ Despite appearances, we should not begin by assuming that
LLM behaviour aligns with our intuitions for human behaviour. We first have to under-
stand what LLMs are, which begins with the language modelling task they are trained to
perform (McCoy et al., 2023).
A language model is any model for producing natural language (Blank, 2023).2 In nat-
ural language processing (NLP), a subfield of AI, language models are machine learning
systems optimised to predict the next word in a sequence. This predictive task is called
the language modelling task (Jurafsky & Martin, 2025). Systems succeed at the lan-
guage modelling task if their predicted next words match the distributional features of
real natural language. As with other machine learning applications, success is determined
by splitting an empirical distribution into separate segments for training and testing, up-
dating the model’s parameters through training on the former, then reporting predictive
accuracy on the latter. This evaluation setting is called the “common task” method (Liber-
man, 2010) or the Common Task Framework, and has been a convention for evaluating
progress in AI systems since its adoption by DARPA in the late 1980s (Donoho, 2017).
What makes a language model large is the number of parameters it can optimise for
the language modelling task. LLMs are a contemporary phenomenon in NLP. Today,
practically all language models are neural networks built with the Transformer architec-
ture (Vaswani et al., 2017). The largest of these models have billions and now possibly
trillions of parameters. This development was unforeseen and unprecedented at the time
of the Transformer’s introduction, when Vaswani et al. (2017) proposed the architecture
specifically for the task of machine translation.
Two factors explain the Transformer’s dominance in modern NLP. First, the architecture
allows training in a highly parallel fashion on consumer hardware, allowing model devel-
opers to scale extremely large networks (Radford et al., 2019). Second, massive natural
language corpora, in the form of Internet text data from websites like Wikipedia and Red-
dit, are readily available for training (Brown et al., 2020; Villalobos et al., 2024). The
fusion of these two resources, scalable compute and abundant data, drove an empirical
 2
 This definition encompasses models for the human production of language that are not machine learn-
ing models, e.g., formal models used in linguistics. A natural language, like English, contrasts with a
formal language, like a mathematical or programming language—although this definition is porous, since
we know large language models are capable of producing code!
 7
2 BACKGROUND 2.1 Scaling laws and LLM capabilities
Figure 2: The scale of language model training, 2010 to 2025. The dashed black line
shows the introduction of the Transformer in 2017. The solid red lines show trends for
training compute before the Transformer (order of magnitude increase every 5 years) and
after the Transformer (order of magnitude increase every 1.2 years). Influential LLMs are
annotated on the plot with red points. Data from Epoch AI (Epoch AI, 2025).
breakthrough. For Transformer language models on general Internet text data, it happens
that increasing the number of parameters, the training dataset size, and the amount of com-
putation—in the correct ratios—yields smooth improvements at the language modelling
task according to a power-law relationship. These findings are known as neural scaling
laws (Kaplan et al., 2020; Henighan et al., 2020; Hoffmann et al., 2022), and faith in their
predictive power is largely responsible for the explosion in AI capital investment so far
through the 2020s.
In their original formulation (Kaplan et al., 2020), scaling laws are situated squarely in
the language of the Common Task Framework. Increased scale at training time yields
power-law improvements in predictive accuracy at testing time, specifically on data from
the same distribution as seen in training. However, the original ambition of AI research
lies in not merely test-set predictive accuracy, but in the simulation of actually intelli-
gent behaviour (McCarthy et al., 2006). The distribution of Internet text is remarkably
domain-general, and sequences of Internet text are not arbitrary data: they represent the
outputs of human cognitive processes, like political argumentation, mathematical reason-
ing, or historical fact retrieval. An LLM improving at test-time predictive accuracy on this
distribution is also improving at modelling these outputs of human cognitive processes.
McCann et al. (2018) propose that a wide range of natural language tasks beyond transla-
 8
2 BACKGROUND 2.1 Scaling laws and LLM capabilities
tion—sentiment analysis, summarisation, and inference, among others—can be reframed
as language modelling tasks using question-answer pairs, and Radford et al. (2019) show
that scaling LLMs with Internet text data appears to improve performance on all of these
tasks. All of a sudden, our AI systems appear to possess a broad and increasingly useful
set of linguistic skills. Bommasani et al. (2022) name this new class of systems “foun-
dation models” to reflect their generality of application,3 and provides some of the first
commentary on the societal prospects of such domain-general AI systems.
The introduction of “foundation models” as a term represents an important step away from
the Common Task Framework, and with it a focus on LLMs’ test-time predictive accuracy.
From here, attention shifts towards a focus on LLM capabilities as something like gen-
uine cognitive capabilities (Srivastava et al., 2023). Correspondingly, evaluation efforts
shift away from distributionally-equivalent test partitions and towards more adversarial
and task-specific datasets intended to encircle the limits of LLM performance (Bowman
& Dahl, 2021). Also around this time, critical discussion begins as to whether training
for domain-general language modelling imbues any kind of true natural language “under-
standing” capability (Bender & Koller, 2020), or whether LLMs’ modelling the form of
natural language represents a different capability, or no capability at all (Bender et al.,
2021). These developments—the isolation of specific tasks for evaluation, and the cri-
tique of the connection between these tasks and true LLM capabilities—represent the
beginning of the construct validity challenge for LLM evaluation (Raji et al., 2021).
The distinction between general scaling performance and specific capabilities intensifies
with the claim that certain capabilities are not smoothly predictable with scale, but are in-
stead “emergent” at certain large model sizes (Ganguli et al., 2022; Wei et al., 2022). For
example, smaller language models appear incapable of performing the BIG-bench mod-
ular arithmetic task, but accuracy on this task begins to suddenly increase after 1022 float-
ing point operations in training (Wei et al., 2022, 4). The same holds for TruthfulQA, a
task involving the discernment of false statements (Lin et al., 2022). Ganguli et al. (2022)
pose this distinction as one between “predictability” and “surprise”: scaling laws outline
the general improvements to language modelling that researchers expect to arrive through
scale, while “emergent capabilities” surprise even the designers of these systems. Ganguli
et al. also highlight the policy implications of this finding: unpredictable capabilities pose
a deployment and governance challenge, especially if the capabilities include deception
or other possibly harmful qualities. These policy implications will soon be grounded in
 3
 It is worth a footnote’s recognition that the term “foundation model” encompasses not just language
models, but AI systems for other modalities, such as vision and speech modelling systems. Henighan et al.
(2020)’s scaling law results apply to this general class of “autoregressive generative models.” For simplicity,
I am presenting these results only as they apply to language models.
 9
2 BACKGROUND 2.2 Quantifying construct validity
the way that LLM capabilities are—literally—written into law: Article 51 the European
Union’s Artificial Intelligence Act, entering into force in August 2025, specifies that
 [a] general-purpose AI model shall be classified as a general-purpose AI
 model with systemic risk if... it has high impact capabilities evaluated on the
 basis of appropriate technical tools and methodologies, including indicators
 and benchmarks. (European Parliament, 2024)
The scope of “high impact capabilities” is thus handed over for the technical experts to
decide. We still face Ganguli et al. (2022)’s dichotomy—predictable improvements from
scale on one hand, emergent capabilities on the other—and critiques in the form of Bender
& Koller (2020) and Raji et al. (2021) about the validity of their evaluation techniques.
It is time to address “high impact capabilities” using tools and techniques from the social
sciences (Wallach et al., 2024).
2.2 Quantifying construct validity
In social science language, an LLM capability is a construct—a theoretical quantity that
cannot be directly measured (in the way a person’s height can be directly measured). Core
to measurement theory in the social sciences is the separation between the measurements
for constructs and the constructs themselves (Cronbach & Meehl, 1955; Messick, 1998;
Salaudeen et al., 2025). The objects of study in the social sciences—the constructs—can
be abstract. Psychology studies constructs like openness to experience; sociology studies
constructs like radicalisation. A core assumption to the methodological practice of each
field is that such constructs cannot be measured exhaustively or without error. Where
these constructs are quantified, they are modelled to be latent variables whose values
are informed by observable indicators, typically responses to surveys or behavioural tests.
Ideally, an indicator would be perfectly calibrated to the construct it intends to measure. In
reality, we do not expect a singular survey question to give a perfectly calibrated account
of an individual’s openness to experience or their radicalisation. Errors can arise from
particularities of the question, like confusing phrasing (an item-specific error), or ex-
traneous circumstances, like a participant being tired (a measurement error). However,
many survey questions together can overcome these errors. Multiple measurements for
the same construct should share some signal related to the construct apart from their own
item-specific and measurement errors. More specifically, we expect measurements for the
same construct (or theoretically similar constructs) to correlate, and to correlate more than
measurements for separate constructs. Returning to our example from Section 1.3, there
are many benchmarks for measuring mathematical reasoning—MATH, FrontierMath,
 10
2 BACKGROUND 2.2 Quantifying construct validity
AIME 2024, MathBench, and more.4 For these benchmarks to be identifiably mea-
suring the same thing—mathematical reasoning—there should be some degree of conver-
gence in their scores. If MATH and FrontierMath both measure mathematical skill,
and some LLM performs above average on MATH, we should expect it to perform above
average on FrontierMath. However, this convergence in scores should be to some
degree localised. If every benchmark score correlates highly with every other score—that
is, if MATH performance is no better correlated to FrontierMath than any arbitrary
benchmark for geography or history trivia—then we will struggle to justify that MATH
and FrontierMath benchmark any specific ‘mathematical’ attribute of LLMs in place
of some more general ‘benchmark performance’ attribute. In other words, even if an
LLM can recognisably solve mathematical problems, we do not have the evidence to give
a mathematical reasoning capability any independent theoretical standing.
If our collection of benchmarks has both of these criteria—convergent correlations be-
tween scores, and discriminating power in those correlations—we can better trust that
our benchmarks collectively estimate some general capability. These guarantees put our
evaluation techniques in a much more powerful position: with reference to an LLM’s ca-
pabilities, we can explain how the LLM is capable of certain tasks, and we can predict
whether the LLM will be capable of novel, related tasks. If we want fair and accurate AI
capability regulation—or if we ever want an LLM to file our taxes—we need these guar-
antees. In measurement theory, these criteria are called convergent and discriminant
validity, respectively, and they are the core of construct validity in its original formula-
tion (Cronbach & Meehl, 1955).
The simplest mathematical model for expressing these criteria is the latent factor model
(Everitt, 1984). Suppose that we have k latent constructs and, since we cannot measure
them directly, have p > k indicator variables we believe to measure these constructs.
These indicator variables might be questions in a p-question survey. The basic latent
factor model assumes that
 x = Lf + e (1)
holds for each survey participant.5 Here x is a p × 1-vector of observed responses, f is a
k × 1-vector of latent factor scores, L is a p × k matrix of pattern coefficients (also called
factor loadings), and e is a p × 1-vector of error terms (Kline, 2016). Equation (1) states
that observed responses (x) result from some influence (L) of underlying latent constructs
 4
 In several places, I am going to list many benchmarks in succession, and it hinders readability to include
all of the necessary inline citations. Readers should consult Appendix A for a description and citation of all
benchmarks mentioned in this thesis.
 5
 All of my mathematical notation will follow Goodfellow et al.’s textbook, Deep Learning (2016).
Appendix B contains a table of the notation copied over from the textbook.
 11
2 BACKGROUND 2.2 Quantifying construct validity
(f ) mediated by some error (e). This model is the simplest possible model for connecting
measurements to the constructs they purport to measure. Given empirical survey data, we
could estimate the latent factor values with techniques including likelihood optimisation.
The survey demonstrates construct validity if the indicators and latent constructs have
suitable convergent and discriminant correlations. If indicators xa and xb should both
measure construct fc , and indicator xd should not, we should expect both La,c > 0 and
Lb,c > 0 (convergent validity) and Ld,c < La,c and Ld,c < Lb,c (discriminant validity) to
result from the model estimates.
Factor analysis models can be exploratory (Fabrigar & Wegener, 2012) or confirma-
tory (Kline, 2016). An exploratory model freely estimates all pattern coefficients in
L, while a confirmatory model sets Li,j ← 0 for particular coefficients. Thus, in an
exploratory model, constructs are mostly unsupervised discoveries made by the model,
more akin to an unsupervised dimensionality reduction, whereas in a confirmatory model,
the researcher hypothesises the constructs that inform specific indicators. Burnell et al.
(2023a) use an exploratory factor model, while Ilić & Gignac (2024) fit a confirmatory
factor model, specifying their LLM capabilities in advance to resemble human cognitive
constructs.
In LLM evaluation, we similarly want to separate indicators for constructs from the con-
structs themselves. Again, returning to our mathematics example: today’s best LLMs
recently achieved gold-medal performance on the International Mathematics Olympiad
(IMO) (Luong & Lockhart, 2025; Cai & Singh, 2025). This performance indicates a la-
tent capability which, if observed in humans, we would call mathematical reasoning or
problem-solving. Do these IMO gold-medallist LLMs have the same capability? We have
seen that subjective arguments either way are controversial, but the formal definition of
construct validity provides a foothold. Given a population of LLMs and performances
across different mathematical benchmarks, we could fit a latent factor model to help bol-
ster the connection between the IMO and LLMs’ mathematical capability.
We do have sizeable datasets of LLM performances on benchmarks, including HELM
(Liang et al., 2023), Chatbot Arena (Chiang et al., 2024), and the OpenLLM Leader-
board (Fourrier et al., 2024b). Unfortunately, there are reasons to suspect that the standard
inferential statistics behind latent factor models will not apply to LLMs in the same way
that they apply to human populations. In general, when you conduct inferential statistics
on a sample, you assume that sample to be representative of some greater population,
such that your findings on the sample will generalise to the population. However, the par-
ticular dynamics and history of LLMs suggests that the very idea of an LLM ‘population’
could be flawed. One reason is survivorship bias: commercial model providers might
 12
2 BACKGROUND 2.3 Related work
only release LLMs that perform well in internal testing. Studies like Singh et al. (2025)
have already shown how such selective reporting can distort the statistical properties of
benchmark results. Another reason is the temporal variance of such a population. While
estimates of human capabilities, like IQ, do drift slowly over time (Trahan et al., 2014),
the population of LLMs is more volatile and competitive, making it difficult to identify
stable and reproducible factors (Zhou et al., 2025). A third reason is the scaling laws
reviewed above. Unlike humans, LLMs have observable design parameters that strongly
influence their performance on most tasks. These scaling parameters are not capabilities,
but they can affect significant variance in observed benchmark scores. Statistical mod-
els using latent factors to capture LLM capabilities should be wary to account for these
effects, as they can easily capture proxies for scaling parameters by accident.
2.3 Related work
Latent factor models of LLM capabilities
In the first application of latent factor modelling for LLM capabilities, Burnell et al.
(2023a) fit an exploratory factor model using performance on the HELM benchmark, utils-
ing a sample of 29 LLMs. Models in their sample range in size from 410 million pa-
rameters (Cohere small v20220720 (Cohere, 2022)) to 530 billion parameters (TNLG
v2 (Smith et al., 2022)) and were released between June 2021 and January 2023. The
first author, a cognitive scientist, annotated each of the 34 HELM tasks with the capability
the task elicited, including cognitive abilities like “Inductive reasoning,” “Domain knowl-
edge,” and “Comprehension” (5). Fitting three latent factors to explain their benchmark
results, Burnell et al.’s model fit statistics are below the conventionally acceptable thresh-
old in social science,6 though the authors note that they expect this from the small size
of their sample. Nonetheless, the authors identify and discuss three separable factors rep-
resenting LLM capabilities. The first, which they label “Language modeling,” loads7 on
tasks all annotated as “Language modeling,” including sentence completion for The Pile
(Gao et al., 2020) and the International Corpus of English (Greenbaum, 1991). The sec-
ond, which they label “Reasoning,” loads on benchmarks annotated “Mathematical rea-
 6
 Specifically, Burnell et al.’s model achieves CFI = 0.70, TLI = 0.61, RMSEA = 0.26, and latent
factor models are considered acceptable at CFI ≥ 0.90, TLI ≥ 0.90, RMSEA ≤ 0.10 and excellent at
CFI ≥ 0.95, TLI ≥ 0.95, RMSEA ≤ 0.06 (Finch & West, 1997; Hu & Bentler, 1998, 1999; Clark &
Watson, 2019). While the specific interpretations of these statistics is not necessary for this overview, they
will be described in Section 3.4 for validating my own models.
 7
 For latent factor models, to say that a factor (or capability) j “loads” on a benchmark i means that
the model fit a significant positive coefficient at Li,j in the pattern coefficient matrix L, as I introduced in
Section 2.2. A larger loading means a larger coefficient Li,j , which also means that factor j explains more
of the observed variance in benchmark i.
 13
2 BACKGROUND 2.3 Related work
soning,” like GSM8K and MATH, and “Inductive reasoning,” like BBQ, among others. The
final factor they label “Comprehension,” and it loads on a diverse set of annotated cogni-
tive capabilities, including “Domain knowledge” (HellaSwag; WikiFact), “Compre-
hension” (NaturalQuestions; XSUM), “Commonsense reasoning,” (OpenbookQA)
and “Deductive reasoning” (bAbI; Dyck). The “Comprehension” capability explains the
largest proportion of communal variance in the measured scores (33%) and it correlates
the largest with other factors (0.43 with Language modeling; 0.51 with Reasoning) and
with the log of the LLM parameter count (0.70).8 Notably, Burnell et al. also observe
a largely positive correlation manifold across their benchmarks, with the mean inter-task
correlation r = 0.56, meaning that each pair of benchmark results is moderately corre-
lated on average.
Ilić & Gignac (2024) conduct a second experiment with latent factor models, this time
using a confirmatory factor analytic approach. Their experiment uses the same LLM
sample as ours: HuggingFace models evaluated on the OpenLLM Leaderboard, a much
larger collection than Burnell et al. (2023a)’s HELM results. They begin with the leader-
board’s full population as of 8 March 2024—3, 862 models—but reduce this number to
591 using a combination of clustering techniques like DBSCAN (Ester et al., 1996) and
subjective criteria to remove redundant models. Ilić & Gignac hypothesise cognitive fac-
tors inherited from the Cattell-Horn-Carroll theory of human cognitive abilities (Cattell
& Horn, 1978; Carroll, 1997; Schneider & McGrew, 2018), including fluid reasoning,
quantitative knowledge, reading/writing, and domain-specific knowledge. They allocate
different OpenLLM Leaderboard tasks to these different cognitive capabilities using de-
scriptions of the tasks. Ultimately, the authors are unable to fit an acceptable model
partitioning OpenLLM Leaderboard subtasks according to these capability dimensions.
They instead find a two-factor model with acceptable fit.9 This model includes one mixed
factor for reading/writing and domain-specific knowledge, plus a factor that loads heav-
ily on every benchmark indicator. The authors name this factor an “Artificial General
Ability” (AGA) factor, in reference to the famous “g-factor” hypothesised to be a general
measure of human intelligence (Spearman, 1904). This AGA factor has a large average
loading of 0.81 and accounts for 65.6% of the variance in benchmark results. The au-
thors fit a LOESS regression for the AGA factor against model parameter size, finding a
“curvilinear” relationship explaining 25% of variance in the factor value (7). Like Burnell
et al. (2023a), this study finds a large positive correlation manifold with mean inter-test
correlation r = 0.73 across benchmarks.
 8
 All correlations are Pearson correlations.
 9
 Their model fit statistics are CFI = 0.984, TLI = 0.977, RMSEA = 0.089.
 14
2 BACKGROUND 2.3 Related work
Observational scaling laws
In parallel, Ruan et al. (2024) develop a method for estimating LLM capabilities that
generalises neural scaling laws. The original scaling laws apply to test-set predictive
error—specifically, the cross-entropy loss on the test set (Kaplan et al., 2020). This error
is an unbounded positive quantity where lower is better. Our subject matter, benchmarks,
are instead scored on the interval [0, 1] where higher is better. Previous studies resolve this
discrepancy (Finnveden, 2020; Owen, 2024), adapting scaling laws to predict individual
benchmark scores. Owen (2024) finds that a logistic link function between model scale
and benchmark performance is the most accurate. For a model i trained with ci total
floating point operations (FLOps), Owen (2024) estimates a benchmark score bi ∈ [0, 1]
as
 bi = σ(β log(ci ) + α).
Ruan et al. (2024)’s observational scaling laws take the same logistic form as the bench-
mark scaling laws in Owen (2024). However, in place of scale, observational scaling laws
model benchmark performance for model i as a function of k distinct capabilities via a
“capability vector” si ∈ Rk , such that
 bi ≈ σ(β ⊤ si + α)
instead. As with scaling laws, each model’s capability vector is a function of the model’s
scale, except that the vector coefficients for converting scale into capabilities are shared
across the entire model family. If model i belongs to family f , si is given by
 si ≈ tf log(ci ) + vf .
For example, Llama 3.1 8B and Llama 3.1 405B would share the vectors tf and vf in
virtue of belonging to the same “Llama 3.1” model family, despite having different values
of training compute ci . What makes these scaling laws “observational” is that the capa-
bility vectors are estimated using a shared, low-dimensional representation of observed
benchmark scores. In traditional scaling laws, the coefficients mapping model scale to
test-set error are estimated individually for each model family.
Ruan et al. collect 7 benchmark scores for 77 models using data from the OpenLLM
Leaderboard and EvalPlus (Liu et al., 2023). To convert these scores to capabilities, they
directly set the capability vectors to be the first k = 3 principal components of their
benchmark score matrix. Specifically, if bi is a p × 1-vector of model i’s benchmark
 15
2 BACKGROUND 2.3 Related work
scores, Ruan et al. set
 si ← W bi , (2)
where W is a k × p-matrix of principal component weights for all benchmark scores
across the sample of 77 LLMs. The authors find that k = 3 delivers the best results, equal
to the number of latent factors in Burnell et al. (2023a). These first three components
explain 96.7% of the variance in Ruan et al.’s observed results, with the first component
explaining ~80%. They show that their derived principal component scores can be used
to fit observational scaling laws for complex tasks beyond the 7 benchmarks included in
their score matrix, including some of the “emergent” capabilities in Wei et al. (2022).
Their method uses only scores from the lower end of the performance distribution, al-
lowing their model to extrapolate future performance. These observational scaling laws
outperform conventional, compute- and parameter count-based scaling laws in terms of
predictive accuracy.
Latent factor models and PCA
The latent factor modelling approaches, Burnell et al. (2023b) and Ilić & Gignac (2024),
seem to have mostly explanatory goals—they aim to find clear representations of LLM
capabilities that reflect benchmark data. By contrast, Ruan et al. have a mostly predic-
tive goal—they aim to find representations of LLM capabilities that generalise to other
benchmarks.
Nonetheless, there is a remarkable similarity between the latent factor models of capabil-
ities in Burnell et al. (2023a) and Ilić & Gignac (2024) (Equation (1)) and Ruan et al.’s
PCA decomposition approach (Equation (2)). Say that B is the p×m-matrix representing
p benchmarks scores for a population of m LLMs. In matrix formulation, the latent factor
model assumes
 B = LF + E, (3)
where pattern coefficients L are unchanged from Equation (1), F is a k × m matrix
alternative for factor scores f , and E is a p × m-matrix alternative for error terms e. PCA
instead utilises the decomposition
 B⊤W = T ⊤
 B = WT,
where W is a p × p matrix of principal component weights and T is a p × m matrix of
principal component scores. The columns of W are the eigenvectors of B ⊤ B, and the
 16
2 BACKGROUND 2.4 Research questions
first column vector W:,1 maximises the explained variance in B by satisfying
 X
 W:,1 = arg max (B:,i · w)2
 ∥w∥=1
 i
and is therefore the first principal component (Gewers et al., 2022). For dimensionality
reduction, we can use the approximation
 B ≈ W:,:k T:k,: (5)
which represents B using the top k principal components.10 This is how Ruan et al.
(2024) achieve their version of pattern coefficients in the p × k matrix W:,:k . Since W:,:k
resembles the pattern coefficient matrix L, we can see Equation (2) as equivalent to Equa-
tion (1) with E = 0.11 In other words, construed as a model of common factors, PCA
implicitly assumes that all variance is common variance and that there are no item-specific
errors, including measurement errors. In the context of LLM benchmarks, this assumption
states that LLM performances are not distorted by the unique phrasing of instructions or
output format requirements in individual benchmarks. In contrast, the latent factor model
allows for item-specific errors with the matrix E. To be precise, the model will estimate
p separate covariance parameters for each benchmark, then represent each row of E us-
ing normally-distributed random errors according to these covariances (Kline, 2016). If
benchmarks have specific formatting quirks that cause performance errors—for example,
prompt phrasings that we know influence performance (Mizrahi et al., 2024; Voronov
et al., 2024)—this assumption provides a ‘home’ for the error in the statistical model. It
does not force the capability estimates to pick up this error variance, while PCA decom-
position does.
2.4 Research questions
I have now explained latent factor models and observational scaling laws in some math-
ematical detail. Both techniques can take a collection of LLM benchmark scores and
estimate the capabilities behind these scores. Given benchmark scores B, latent factor
models provide factor scores F as capabilities, while observational scaling laws provide
principal component scores T:k,: . It should also be apparent that each approach deploys
some domain knowledge that the other is missing. Observational scaling laws leverage
 10
 The term W:,:k represents a minor abuse of Goodfellow et al. (2016)’s matrix notation. The intended
reading is Pythonic: W:,:k represents all rows and the first k columns of the matrix W . It is the p × k slice
of a p × p matrix.
 11
 This reformulation applies with the caveat that the pattern coefficient vectors W:,j for each ‘factor’ j
are orthonormal, which is not necessary for general latent factor models.
 17
2 BACKGROUND 2.4 Research questions
model scale, including the results from Finnveden (2020) and Owen (2024) that show that
benchmark performance is decently explained by model scale on its own. Latent factor
models ignore scaling laws, so they lose out on this predictive utility. Yet, latent factor
models appear to capture a correct assumption about the individual error signals in bench-
marks: the model’s error terms capture these signals, providing the factors with cleaner
estimates of general capabilities.
From these observations, I would like to determine if these are real deficiencies in these
models, and if the supposed advantages of each approach can be conferred to the other. I
propose two research questions:
 A. Does providing latent factor models with information about model scale improve
 their fit and explanatory power?
 B. Does providing observational scaling laws with latent factor capability estimates
 improve their predictions for novel benchmarks?
 18
3 METHODS
3 Methods
3.1 Experimental design
In this section, I propose two experiments to address my two research questions. The first
experiment compares latent factor models against an alternative model; the second exper-
iment compares observational scaling laws against an alternative model. The alternative
model in each case is my structured capabilities model, a hybrid of the two. I will define
the structured capabilities model in Section 3.3.
Experiment A: Parameter size as an upstream cause of LLM capabilities
Following Burnell et al. (2023a) and Ilić & Gignac (2024), my model uses factor analytic
methods from the social sciences to decompose observed benchmark results into common
capability scores. Adopting factor analysis from social science provides a measured and
proven explanatory basis for the estimated capabilities. However, I believe that the omis-
sion of learnings from the AI scaling law literature makes these models deficient in some
testable ways.
First, both Burnell et al. and Ilić & Gignac’s experiments share the ‘pure measurement’
modelling assumption embodied in Equation (3), where the only variables influencing
benchmark scores are the latent capability parameters F and L and the error terms E.
Both experiments report a large positive correlation between benchmarks and a dominant
singular latent factor that correlates strongly with model size. These results look suspi-
ciously like the models are fitting proxies for model size in place of an actual capability.
I believe that these results suggest the pure measurement methodology is flawed, and that
model size should be considered an exogenous upstream cause of LLM capabilities within
the model itself.12 To test this hypothesis, I will compare a pure exploratory factor analy-
sis (EFA) model before and after factors are constrained to depend on a single upstream
variable: the log of the number of LLM model parameters, a measure of model scale used
in Owen (2024)’s scaling laws. I hypothesise that including the single upstream variable
will provide a better explanation of my benchmark data. I suspect I will see the same
dominant factor in my pure EFA model that occurs in Burnell et al. (2023a) and Ilić &
Gignac (2024), and that in the presence of model size, this factor will be revealed as an
illusory proxy for scale.
 12
 While I use the phrase “exogenous upstream cause” as a motivation for my modelling approach, the
structured capabilities model does not allow for causal inference. We discuss this distinction in the limita-
tions in Section 5.4.
 19
3 METHODS 3.1 Experimental design
Second, standard factor analysis models as in Burnell et al. and Ilić & Gignac explain
indicator variables (e.g., benchmark performances) as linear responses to upstream latent
factors. However, we know from Owen (2024) that linear functions fare poorly for pre-
dicting benchmark performance. If I hypothesise that model size is a common upstream
cause of model capabilities, I should also expect that the shape of this response is not
linear, but logistic. I will transform my benchmark data to model a logistic relationship to
see if the model fit improves.
Experiment B: Latent factors as generalisable LLM capabilities
The structured capabilities model proposed above resembles observational scaling laws:
it explains LLM capabilities with using model size, and it does so with logistic relation-
ships. However, the approach differs in estimating capability scores as latent factor scores
instead of principal component weights.
In Section 2.3, I covered how latent factor and PCA decomposition encode different as-
sumptions about communal and item-specific variance. The social sciences advocate mea-
surement models like factor analysis models over data-driven techniques like PCA for the
explanation of common causes. This preference is grounded in the improved hypothesis
testing abilities and theoretical grounding of the measurement models. However, I also
suspect that latent factor modelling offers an improvement over PCA more desirable in
computer science literature, which is an improved generalisation of capabilities to unseen,
out-of-distribution benchmarks.
I suspect improved generalisation for two reasons. First, as covered in Section 2.3, PCA
implicitly estimates the item-specific error to be 0 for every indicator variable. Isolating
no benchmark-specific variance will presumably overfit capability estimates to the partic-
ular benchmarks included in the PCA decomposition, harming the generalisation of these
capabilities to novel settings. Second, as principal components must be extracted before
modelling the contribution of model size, observational scaling laws are forced to incor-
porate variance due to model size in the principal component scores. These components
are supposed to indicate capabilities independent from model size, yet seeing the results
from Ruan et al. (2024), I expect the first principal component to proxy model size just
like the dominant factors in the latent factor models.
I will test this hypothesis using a similar experimental setup to Ruan et al. (2024). I will fit
both the observational scaling law and structured capabilities models to a subset of bench-
marks, then I will use the estimated capabilities to extrapolate performance on a held-out
benchmark. I will use prediction error as a measure of each technique’s generalisation.
 20
3 METHODS 3.2 Data
3.2 Data
The OpenLLM Leaderboard
I source benchmark results from the OpenLLM Leaderboard, a popular leaderboard pro-
viding standardised and open-source evaluation of LLMs (Fourrier et al., 2024b). The
v2 rendition of the OpenLLM Leaderboard evaluates LLMs on six popular benchmarks:
BIG-Bench Hard (BBH), IFEval, MATH, GPQA, MuSR, and MMLU-PRO. As of 13
March 2025, the OpenLLM Leaderboard v2 is no longer taking submissions. The creators
cite its obsolescence in the face of improving LLM reasoning and agentic capabilities,
which their chosen six benchmarks do not assess (Fourrier, 2025). At the time of closure,
the v2 Leaderboard reported evaluations for 4, 576 LLMs across the aforementioned six
benchmarks.
The OpenLLM Leaderboard v2 represents a complete and thorough experiment in pub-
lic LLM evaluation. The 4, 576 LLMs represent 64 distinct architectures and range in
size from below 1 to above 140 billion parameters. All evaluated models are open-source
and the results of evaluation are publicly inspectable. The leaderboard itself is a popular
public resource within the AI community: as of July 2025 it remains the largest ‘Space’
on the HuggingFace website, having amassed ~13,300 likes (HuggingFace, 2025). Many
academic studies use the leaderboard to understand LLM performance, including both of
Ilić & Gignac (2024) and Ruan et al. (2024). Alongside HELM (Liang et al., 2023) and
Chatbot Arena (Chiang et al., 2024), the OpenLLM Leaderboard is one of the most pop-
ular sources for LLM evaluation results, and almost certainly the largest public database
of such results.
Following claims about gamification and unfair reporting on other popular leaderboards
(Singh et al., 2025), one might be wary that the leaderboard’s popularity comes at the
expense of its scientific utility. However, the OpenLLM Leaderboard team takes several
measures to ensure the fairness of their reporting. All OpenLLM Leaderboard evalua-
tions are conducted using a public fork of the Eleuther AI Language Model Evaluation
Harness (Gao et al., 2024), ensuring independent reproducibility of results. Once sub-
mitted for evaluation, an LLM’s results are made public and immutable to discourage
selective reporting (Fourrier et al., 2024a).
BIG-Bench Hard
Of the six benchmarks on the OpenLLM Leaderboard, I take scores on the BBH bench-
mark for my experiments. BBH, short for BIG-Bench Hard (Suzgun et al., 2023), is a
 21
3 METHODS 3.2 Data
 Subtask # Questions # Multiple-choice options
 Boolean expressions 250 2
 Causal judgement 187 2
 Date understanding 250 6
 Disambiguation QA 250 3
 Formal fallacies 250 2
 Geometric shapes 250 11
 Hyperbaton 250 2
 2 Logical deduction 750 7
 Movie recommendation 250 6
 Navigate 250 2
 Object counting 250 19
 Penguins in a table 146 5
 Snarks 178 2
 Sports understanding 250 2
 Temporal sequences 250 4
 Tracking shuffled objects 750 7
 Reasoning about colored objects 250 18
 Ruin names 250 6
 Web of lies 250 2
 Table 1: BIG-Bench Hard subtasks in my dataset.
curated subset of the most challenging tasks from the BIG-bench dataset (Srivastava
et al., 2023). BIG-bench is the result of a broad community effort spanning teams from
OpenAI and Google as well as the greater AI and software communities. 450 authors,
representing 132 institutions, contributed 204 tasks (Srivastava et al., 2023, 2). These
tasks are diverse in both difficulty and scope, including problems drawn from biology and
physics, common-sense reasoning and logic puzzles, and problems designed to test social
bias. All BIG-bench tasks are evaluated by a team of relevant human experts to both
validate problem construction and provide a human baseline.
To create BBH, Suzgun et al. select 23 BIG-bench tasks where no LLM outperformed
the average human rater, filtering additionally for sufficiently large sample sizes (>100
examples) and straightforward evaluation metrics (either exact match or multiple choice).
The authors take a random subsample of up to 250 questions from each subtask, resulting
in a benchmark dataset with 23 partitions and 6,511 total questions. These tasks are simi-
larly diverse. For example, “Geometric shapes” asks the LLM to predict the shape drawn
from some SVG code, while “Boolean expressions” gives the LLM a logical formula to
parse, and “Snarks” asks the LLM to detect sarcasm. Table 1 lists the subtasks that I use,
and Appendix C provides descriptions and example problems.
 22
3 METHODS 3.2 Data
BBH is a popular benchmark that has enjoyed considerable attention in the scaling law lit-
erature. Wei et al. (2022)’s claims of “emergent capabilities” in LLMs used BBH subtasks
for their experiments, and Owen (2024)’s scaling laws predicted performance on BBH
subtasks. In addition, Ruan et al. (2024) used BBH data to fit their observational scaling
laws, while Burnell et al. (2023a) and Ilić & Gignac (2024) used related collections of
benchmark tasks (HELM and mostly MMLU, respectively).
Data collection
The OpenLLM Leaderboard itself reports only one aggregate BBH score. The leader-
board attempts to normalise each task by difficulty, though in a previous experiment I
showed that subtasks remain a significant fixed effect for individual question scores, even
after their contributions are normalised (Kearns, 2025). I therefore collect and aggregate
subtask accuracies from the raw evaluation results available on HuggingFace.
On the OpenLLM Leaderboard, four original BBH tasks are not reported for all mod-
els (Dyck languages, Multi-step arithmetic, Salient translation error detection, and Word
sorting). Two are split into three separate tasks based on their complexity level (Logi-
cal deduction and Tracking shuffled objects). I recombine these results, yielding a final
dataset of p = 19 benchmark indicator variables instead of 23. I also find that 181 of
the 4, 576 models included in the leaderboard are missing complete results. Finding no
relationship to model size, publication date, or overall performance to explain these miss-
ing values, I simply drop these models from the dataset, yielding a final sample size of
m = 4, 395 LLMs.
Formal notation and scoring
As in Section 2.3, I will write the p×m matrix B to represent the performance across p =
19 benchmarks for each of m = 4, 395 models. Each benchmark score is a real number
in the interval [0, 1] representing the average accuracy across all subtask questions. All
BBH tasks on the OpenLLM Leaderboard are presented as multiple choice questions.
Subtasks range from having 2 to 19 possible options (see Table 1). The evaluation harness
scores the model according to the multiple choice letter that the model assigns the highest
probability, meaning that LLMs never fail to provide an answer.
For each of the m models, I also collect the available metadata for the model’s parameter
size. I denote parameter size with the variable n, such that model j with benchmark scores
B:,j has nj parameters.
 23
3 METHODS 3.3 Techniques and models
Figure 3: Illustrated three-parameter item response curve. This curve represents
Equation (7). “Difficulty” (β = 0) represents how difficult an item is relative to others
by affecting a lateral transformation in p(θ) across all ability scores. “Discrimination”
(α = 1) represents the item’s ability to differentiate a narrow range of ability scores by
 d
affecting the slope of the sigmoidal curve dθ p(θ). “Guessing probability” (c = 1/5 = 0.2)
represents the rate of success at limθ→0 p(θ), which for multiple-choice questions will be
the odds of guessing correctly from 1/c options.
3.3 Techniques and models
The logistic model
Specifying the logistic model for experiment A requires unpacking the assumptions be-
hind Owen (2024)’s logistic model in more detail. Benchmark scores Bi,j are bounded by
[0, 1], but since LLMs always provide one answer, even random guessing achieves an ex-
pected accuracy above 0 on multiple choice questions. Thus, Owen does not predict raw
scores with a form as simple as Bi,j = σ(α + β log(nj )), because this relationship will
predict Bi,j → 0 for the smallest models. Instead, for a subtask i with #MC multiple-
choice options, the worst models should achieve an expected accuracy of ci := 1/#MC
through random guessing. Owen (2024) fixes this problem by subtracting ci from ob-
served performances and fitting a logistic function with a linear offset to compensate for
adjusting the range. This model takes the form
 
 Bi,j = σ ki (log(nj ) − x0i ) + y0i + ci . (6)
However, I want to adapt a more elegant model from the social sciences to achieve the
same estimation within the original interval [0, 1]. This model is the three-parameter
logistic model from Item Response Theory (Embretson & Reise, 2013), which gives the
probability of correctly answering a singular multiple choice question, accounting for
random guessing. Typically, this model depends on an individual j’s latent ability score,
 24
3 METHODS 3.3 Techniques and models
θj :
 1 − ci
 pi (θj ) = ci + (7)
 1 + exp[−αi (θj − βi )]
In the case that i represents a singular test item (that is, a singular multiple choice ques-
tion), the parameters βi , αi , and ci have specific interpretations. Figure 3 illustrates the
effects of these parameters on the item’s response curve, pi . Observing the similarity
between Owen (2024)’s Equation (6) and item response theory’s Equation (7), I would
like to substitute log(nj ) for θj in Equation (7) to predict the entire subtask score Bi,j .
Even though Equation (7) is defined for singular questions, I can adapt it to entire average
scores with some simplifying assumptions.
Individual multiple choice question scores are dichotomous: the model either answers
correctly or it does not. Thus, in item response theory, a model j’s score on a given
question i is a Bernoulli random variable with p = pi (θj ), where p reflects the question’s
difficulty. On the simplifying assumption that all q questions in each subtask are equally
difficult, if we weigh all q questions equally, then a model’s total score is given by
 Binom(q, pi (θj ))
 ,
 q
with expected value  
 Binom(q, pi (θj ))
 E = pi (θj ),
 q
meaning that Equation (7) can be utilised to represent model j’s expected score across an
entire subtask as a function of the ability parameter θj . Thus, we can simply swap log(nj )
in for θj to get a logistic model similar to Owen (2024)’s:
 1 − ci
 Bi,j = ci + . (8)
 1 + exp[−αi (log(nj ) − βi )]
Equation (8) has the advantage of ranging over the original interval [0, 1] without any
offset, plus the nice interpretations for βi , αi , and ci described in Figure 3 as applied to
BBH subtasks.
The structured capabilities model
At this stage, I can formally define the structured capabilities model that I will use for
the two experiments. The structured capabilities model resembles the fully latent model
in Equation (3), except it allows model size to directly influence the latent capability
 25
3 METHODS 3.3 Techniques and models
estimates. The model replaces the factor value matrix F like so:
 B = L[wn log n] + E (9)
Here n = [n1 , . . . , nm ] is a vector of each model’s parameter size and log is the natural
logarithm applied elementwise. wn is a k × 1-vector of regression coefficients that deter-
mine how model size affects each LLM capability. Under this model, each LLM j will
have a vector of capability scores equal to wn log(nj ) + ϵ, where ϵ is a residual error term
that occurs because of E. Thus, model size affects each model capability, as in a scaling
law, but model- and capability-specific errors affect this relationship, as in a measurement
model.
This relationship is not yet entirely faithful to scaling laws, however, since the relationship
between model size and performance is linear. I hypothesised that a logistic relationship
will better fit the data. Above, I provided an adapted three-parameter logistic model
(Equation (8)) that uses model size nj as the predictor for subtask performance. Now, I
would like to use the structured capability estimates from Equation (9) in place of model
size.
Equation (9) is a type of structural equation model, and the best available software pack-
age for estimating such a model is the lavaan package in R (Rosseel, 2012). Ideally, I
could model each vector of subtask scores Bi,: directly with the logistic relationship
 1 − ci
 Bi,: = ci + . (10)
 1 + exp[−αi (Li,: [wn log n] + Ei,: − βi )]
Unfortunately, lavaan does not support this kind of nonlinearity in its model syntax.
This model also resembles a multidimensional item-response theory model (Reckase,
2009), which handles nonlinearity and is definable in R with the mirt package (Chalmers,
2012). To my knowledge, though, this package cannot handle the structural coefficients
that I need. Thus, I instead apply the inverse operation to the data matrix B, yielding a
transformed matrix B ′ . It is equivalent to Equation (10) to represent each row Bi,: with
  
 ′ 1 Bi,: − ci
 Bi,: = βi + log , (11)
 αi 1 − Bi,:
and then to use the structural equation
 B ′ = L[wn log n] + E (12)
 26
3 METHODS 3.4 Validation and experimentation
to model the logistic relationship between capabilities and benchmark scores.13 I apply
the transformation from Equation (11) on the OpenLLM Leaderboard data matrix before
loading the data into R, where I can then model the linear response in Equation (12) with
lavaan syntax. This final equation represents the structured capabilities model that I
propose to combine latent factor models and observational scaling laws.
3.4 Validation and experimentation
Experiment A: Parameter size as an upstream cause of LLM capabilities
My hypotheses for experiment A are testable by comparing the structured capabilities
model against a pure latent factor model. In Section 3.3, I show how to introduce the struc-
tural parameter for model size (Equation (9)), and also how to transform the data matrix
to model the logistic relationship between capabilities and performance (Equation (11)
and Equation (12)). To consolidate my equations into one place, I will be comparing the
following four models to test these two alterations:
 B = LF + E (13a)
 B = L[wn log n] + E (13b)
 B ′ = LF + E (13c)
 B ′ = L[wn log n] + E (13d)
I believe that the pure latent factor models, Equation (13a) and Equation (13c), will fit
a dominant factor serving as a proxy for model size. As these measurement models are
unconstrained, likelihood optimisation should compel them to fit a parameter to the fea-
ture explaining the greatest variance in the data, and this feature will turn out to be model
size. I believe that this occurs for the pure measurement models in the studies by Burnell
et al. (2023a) and Ilić & Gignac (2024), specifically Burnell et al.’s “Comprehension”
factor and Ilić & Gignac’s “Artificial General Ability” factor. In this model comparison,
the effect should be visually apparent in the values of the pattern coefficient matrix L.
The pure measurement models should estimate factors with a high pattern coefficients on
all indicators; that is, large values of L:,k′ for the offending factor k ′ . I can compare the
variance explained by each factor using the sum of squared factor loadings ∥L:,k′ ∥ (Kline,
2016), where I expect a single factor to dominate the explained variance.
I propose specifically that the structural models Equation (13b) and Equation (13d) will
 13
 In Appendix D, I provide the derivation for Equation (11) beginning from Equation (10).
 27
3 METHODS 3.4 Validation and experimentation
be better explanatory models in virtue of being more parsimonious than their unrestricted
equivalents. ‘Parsimonious’ has a precise definition for statistical models—a more likely
model with a simpler structure is more parsimonious. This criterion balances model fit
with model complexity. My hypothesis is directly testable by comparing parsimonious
fit indices between each pair of models. I will compare the Akaike (Akaike, 1974) and
Bayesian (Schwarz, 1978) information criteria (AIC and BIC), each of which balances
model fit against complexity to quantify parsimony. These are defined as
 AIC := 2d − 2 ln(ℓ̂)
 BIC := d ln(m) − 2 ln(ℓ̂),
where d is the number of parameters estimated by the model, m is the sample size, and
ℓ̂ is the maximised value of the likelihood function for the model. Lower values of both
criteria are better. The latent factor models Equation (13a) and Equation (13c) estimate
k factor loadings for each of the p benchmarks, plus p unique error variances for each
benchmark and k2 covariance terms between factor pairs. So, these models estimate a
 
total of  
 k
 d=k×p+p+ parameters.
 2
Our structured models Equation (13b) and Equation (13d) estimate the same parameters,
plus an additional k for the regression coefficients in wn . For these structural models to
be more parsimonious, the improvement to the likelihood ℓ̂ must be great enough to offset
this increase in parameters d.
I also hypothesise that a logistic relationship between LLM capabilities and benchmark
scores should outperform a linear relationship, which is the typical standard for latent
factor models. If my software packages allowed me to model the logistic relationship di-
rectly on the raw data B, I could compare the model fits with a likelihood-ratio test. Un-
fortunately, since I must instead apply the inverse transformation in Equation (11) to get
B ′ , the likelihoods will not be directly comparable, since transforming B to B ′ changes
the null model and the likelihood landscape. Therefore, I can only compare the model
fit using the conventional heuristics for global fit indices, like the χ2 value, the com-
parative fit index (CFI (Bentler, 1990)), the root-mean squared error of approximation
(RMSEA (Steiger, 1990)), and the standardized root mean squared residual (SRMR (Hu
& Bentler, 1999)). CFI is a comparative metric that compares a model against its null
model, with values bound between 0 and 1 where higher values are better. RMSEA and
RSMR are both estimation error measures where values closer to 0 are better. While these
 28
3 METHODS 3.4 Validation and experimentation
metrics respond differently to features of the experimental setup, like sample size,14 social
science literature generally advises that models are acceptable at CFI ≥ 0.9; RMSEA ≤
0.10; SRMR ≤ 0.10, and excellent at CFI ≥ 0.95; RMSEA ≤ 0.06; SRMR ≤ 0.06 (Finch
& West, 1997; Hu & Bentler, 1998, 1999; Clark & Watson, 2019).
Experiment B: Latent factors as generalisable LLM capabilities
In experiment A above, I test my model’s assumptions that differ from latent factor mod-
els: the structural parameter for model size and the logistic relationship between capabil-
ities and benchmark scores. In experiment B, I want to test how the model’s assumptions
compare to observational scaling laws. This involves comparing latent variables to prin-
cipal components as representations of LLM capability dimensions. For two reasons, I
cannot use a comparative fit test for this comparison. First, while latent factors provide a
testable model of the observed benchmark data, PCA is not testable. Second, computer
science literature tends to prefer improvements to predictive accuracy over explanatory
measures like fit indices, so I will prefer to demonstrate improvement in predictive accu-
racy.
I will compare the two models using an out-of-fold prediction procedure. For each of
p′ ∈ {1, . . . , 19}, I withhold Bp′ ′ ,: , the transformed scores for BBH subtask number p′ . I
can fit both a structural model and a PCA decomposition on this data:15
 Bi̸′=p′ ,: = L[wn log n] + E (15a)
 Bi̸=p′ ,: = W:,:k T:k,: (15b)
The structured capabilities model Equation (15a) fits a k × m matrix of model capability
scores equal to wn log n + ϵ. The PCA model fits a k × m matrix of principal component
‘capability’ scores equal to T:k,: . Which estimate of capabilities generalises better to the
unseen subtask p′ ? To answer, I will split the held-out scores Bp′ ′ ,: into separate training
and test sets, btrain
 p′ and btest train
 p′ , where bp′ consists of the bottom 80% of scores. I will use
 14
 For example, RSMR appears more robust in situations where residuals are correlated (Montoya &
Edwards, 2021) and scales differently with sample size compared to RMSEA (Shi et al., 2020).
 15
 Note that the PCA approach uses Bi̸=p′ ,: , not Bi̸′=p′ ,: . Ruan et al. (2024)’s observational scaling laws
fit the PCA decomposition directly to the raw benchmark scores, then predict downstream performances
with a logistic link function. To be equivalent, my approach fits the principal components using B, then
predicts the transformed scores B ′ .
 29
3 METHODS 3.4 Validation and experimentation
the training set to fit k-length vectors of coefficients via linear regression:
 btrain
 p′ = lp′ wn log n (16a)
 btrain
 p′ = wp′ T:k,: (16b)
The vectors lp′ and wp′ , like the row vectors of L and W:,:k , encode the importance of
each of the k capabilities for subtask p′ . I can use each of these and the learned capability
scores to predict the held-out performances btestp′ . To match the presentation in Ruan et al.
(2024), I will compare each approach using its mean-squared error (MSE). I will also
compare a simple scaling law approach, per Owen (2024), as a baseline predictive model:
 btrain
 p′ = α + β log n (17)
 30
4 RESULTS
4 Results
4.1 Preliminary data analysis
Inter-item correlations
For an initial investigation into the relationship between subtask performances, I plot the
inter-item correlation between subtask scores in Figure 4. Consistent with Burnell et al.
(2023a) and Ilić & Gignac (2024), there is a strong positive manifold to my dataset—the
average inter-item Spearman correlation is ρ = 0.64.16 Similar tasks like Penguins in a
table and Reasoning about colored objects, both of which involve recalling attributes from
structured lists, have correlations as high as ρ = 0.93. At the opposite extreme, dissimilar
tasks like Sports understanding and Web of lies have correlations as low as ρ = 0.11,
though due to the large sample size, all correlations are significant.
Predicting subtask performance with model size
Next, to observe the baseline of Owen (2024)’s logistic scaling law model on my dataset,
I fit Equation (8) to each collection of raw subtask scores Bi,: . R2 values range from very
mild values—0.12 for the Web of lies task—to moderate values—0.52 for the Ruin names
task. Tasks also show a spread of different difficulty βi and discrimination coefficients αi ,
demonstrating different rates of improvement from scale. Figure 5 provides a side-by-side
comparison of Web of lies and Ruin names, and Appendix E displays the logistic fits for
all 19 subtasks.
Inter-item residual correlations
My next step investigates correlations between benchmarks alongside the impact of model
scale. I reinvestigate the inter-item correlation by rank-correlating the residuals of the esti-
mates from Equation (8). In subtracting the best-fit explanation of performance according
to log-parameter size, I can effectively control for the parameter size, and can informally
depict the residual relationship between subtasks. I display the updated correlation matrix
in Figure 6. The average inter-item correlation reduces from ρ = 0.64 to ρ = 0.48, and
 16
 Burnell et al. (2023a) and Ilić & Gignac (2024) both report Pearson instead of Spearman correlation.
However, I am not interested in any parametric relationships at this stage. Owen (2024)’s sigmoidal scal-
ing laws suggest that model subtask performances might not relate in a linear fashion, and in any case,
I am interested in whether the same models perform better across all subtasks, which is a nonparametric
relationship.
 31
4 RESULTS 4.1 Preliminary data analysis
Figure 4: Raw BBH score correlation matrix. The correlation metric is Spearman’s rank
correlation ρ. The labels along the y-axis are acronym abbreviations for the full subtask
names, which are given along the x-axis.
 32
4 RESULTS 4.1 Preliminary data analysis
Figure 5: Logistic scaling law fits for two subtasks. Ruin names has the highest ob-
served correlation with the logistic fit (R2 = 0.52); Web of lies has the lowest correlation
(R2 = 0.12).
some item pairs are now slightly anti-correlated. However, ρ = 0.48 remains a moderately
positive correlation manifold.
Parallel analysis for the number of factors
I next conduct Horn’s parallel analysis on the raw score and residual matrices from the
previous processing steps. Horn’s parallel analysis compares the eigenvalues of each real
data matrix to the eigenvalues of Monte Carlo-simulated matrices of the same size. On
the assumption that the Monte Carlo-simulated eigenvalues represent a component of the
variance attributable to sampling error, subtracting these and retaining the positive ranks
can provide an estimate for the correct number of latent factors for the dataset (Horn,
1965). In other words, this process calculates an estimate for the ‘dimensionality’ of
the benchmark data, as in the number of separable factors that may be contributing to
observed scores. I utilise this technique to determine k, the number of latent factors my
models will estimate. Burnell et al. (2023a) uses the same technique to determine their
number of latent factors. As pictured in Figure 7 (a), this analysis suggests the retention
of 5 factors for the raw scores. In Figure 7 (b), the residual data provides support for an
additional sixth factor, and the principal eigenvalue drops from 11.70 to 9.34.
Since the sixth factor for the score residuals is marginally above the level of the sixth
Monte Carlo-simulated eigenvalue, and since not all of my models will control for pa-
rameter size, I select k = 5 as the number of latent factors for all subsequent experiments.
 33
4 RESULTS 4.1 Preliminary data analysis
Figure 6: BBH score residuals correlation matrix. Score residuals are taken from the
logistic fits against the log-parameter size displayed in Figure 13. The correlation metric
is Spearman’s rank correlation coefficient, ρ. The labels along the y-axis are acronym
abbreviations for the full subtask names, which are given along the x-axis.
 34
4 RESULTS 4.1 Preliminary data analysis
 (a) Scree plot for raw score matrix, recommending to retain 5 factors.
 (b) Scree plot for score residuals after controlling for parameter size, recommending to retain 6 factors.
 Figure 7: Scree plots for BBH score matrices.
 35
4 RESULTS 4.2 Comparison to exploratory factor analysis
 Eq. Str. Log. χ2 ↓ CFI ↑ RMSEA ↓ SRMR ↓ AIC ↓ BIC ↓
 (13a) ✗ ✗ 2984 0.9737 0.0876 0.0134 -217242 -216578
 (13b) ✓ ✗ 3615 0.9680 0.0894 0.0163 -220369 -219673
 (13c) ✗ ✓ 1547 0.9836 0.0623 0.0110 222038 222703
 (13d) ✓ ✓ 2127 0.9782 0.0679 0.0135 218743 219439
Table 2: Fit measures for the four tested EFA models. The Str. column indicates
whether the model includes model parameter size log(n) as a structural regression param-
eter. The Log. column indicates whether the dataset uses the transformed matrix B ′ in
place of B. The fourth row, with Equation (13d), shows the structured capabilities model.
Highlighted boldface values for χ2 , CFI, RMSEA, and SRMR indicate the best overall
model, since these absolute model fit metrics share the same range. Highlighted boldface
values for AIC and BIC indicate the most parsimonious model for a given data matrix,
either B or B ′ , where the likelihood is comparable.
4.2 Comparison to exploratory factor analysis
For experiment A, Table 2 summarises the fit statistics for the four models I compare.
All four models provide acceptable fit according to the conventional interpretation from
Hu & Bentler (1999), with CFI ≥ 0.95, RMSEA ≤ 0.10, and SRMR ≤ 0.06. The
best-fit model is (13c), which utilises the logit-transformed data B ′ but not the structural
parameter wn log n. Modelling the transformed data B ′ in place of B results in better
fit statistics, as shown by the reduction in χ2 , RMSEA, and SRMR and the increase in
CFI from models (13a) and (13b) to models (13c) and (13d). The fit measures are better
for pure measurement models (13a) and (13c) compared to their structured counterparts
(13b) and (13d). However, in both cases, the structured models perform better according
to parsimonious fit indices AIC and BIC.
Figures 8 and 9 provide a visual comparison of the parameter estimates for models (13a)
and (13d). Equation (13a) fits a single dominant factor explaining 72% of the commu-
nal variance. This factor has the largest loading coefficients for 15 of the 19 subtasks.
Per model, factor scores for this factor correlate moderately with the log-parameter size
(R2 = 0.474, according to a logistic relationship). The next largest factor has the largest
coefficients for the remaining 4 of 19 subtasks, explains 16% of the communal variance,
and also correlates moderately with the log-parameter size (R2 = 0.419). In contrast,
Equation (13d) fits two large factors explaining 41% and 36% of the communal variance
respectively. These factor scores also correlate with parameter size (R2 = 0.379 and
R2 = 0.554). The third largest factor loads on similar subtasks to the secondary factor
from model (13a). This third factor explains 14% of communal variance and correlates
 36
4 RESULTS 4.2 Comparison to exploratory factor analysis
 (a) Heatmap of pattern coefficients per factor.
 (b) Proportions of communal variance explained by each factor.
 (c) Logistic relationship between log-parameter size and factor scores for each factor.
Figure 8: Linear latent factor model results. This model corresponds to Equation (13a)
from Experiment A. Factor 1 dominates, explaining the largest proportion of the total
variance (0.72) and correlating strongest with parameter size (R2 = 0.474). Factor 2
loads strongest on some more challenging subtasks (like Tracking shuffled objects) and
also correlates strongly with model size (R2 = 0.419).
 37
4 RESULTS 4.2 Comparison to exploratory factor analysis
 (a) Heatmap of pattern coefficients per factor.
 (b) Proportions of communal variance explained by each factor.
 (c) Logistic relationship between log-parameter size and factor scores for each factor.
Figure 9: Structured capabilities model results. This model corresponds to Equa-
tion (13d) from Experiment A. Factors 1 and 2 share appreciable proportions of the total
variance (0.41 and 0.36), followed by factor 3 (0.14). All three of these factors correlate
strongly with parameter size (R2 = 0.379, 0.554, 0.416).
 38
4 RESULTS 4.3 Comparison to observational scaling laws
moderately with model size (R2 = 0.416).17
Model (13c) is not depicted, though it learns a similar factor structure and coefficients to
(13d), which is the same logistic model with the structural model size parameter. Model
(13c)’s three dominant factors explain 41%, 37%, and 14% of the communal variance, and
correlate with model size at R2 = 0.534, 0.372, and 0.385. Like model (13d), this model’s
two remaining factors have minimal correlation with model size and minimal communal
variance explained.
4.3 Comparison to observational scaling laws
Table 3 lists the mean-squared prediction errors for the structured capability estimates
(Equation (16a)), the observational scaling law capability estimates (Equation (16b)), and
the pure scaling law model (Equation (17)). We list the error on the training set btrainp′
as MSEtrain , and on the test set btest
 p′ as MSEtest . All three methods perform worse at
predicting the held-out bp′ than they do on btrain
 test
 p′ . The pure scaling law model is the
worst performing out-of-fold prediction model with an average MSEtrain of 1.699 and
an average MSEtest of 3.561. Between the structured capabilities and the observational
scaling law capability estimates, the former approach outperforms the latter on 15 of the
19 heldout subtasks in terms of MSEtrain . The same holds for MSEtest , where structured
capability estimates achieve a lower prediction error on 12 of 19 held-out subtasks. The
average MSEtrain is 0.860 for the structured capabilities approach and 0.907 for the ob-
servational scaling law approach, while the average MSEtest is 1.156 for the structured
capability approach and 1.473 for the observational scaling law approach. In both cases,
the structured capabilities approach outperforms in terms of predictive accuracy, how-
ever, according to a two-sided t-test on these samples, the improvement is not statistically
significant (p = 0.776 for MSEtrain , p = 0.637 for MSEtest ).
Figures 10 and 11 show the parameter estimates for each model when predicting the
held-out Geometric shapes subtask. On this subtask, the structured capabilities model
outperforms the observational scaling law model with MSEtest values of 0.370 and 0.467,
respectively. The observational scaling law model uses k = 5 principal components as
capability dimensions, though only the first principal component has a positive weight on
all subtasks (Figure 10 (a)), or exhibits meaningful variance compared to the Geometric
shapes subtask accuracy (Figure 10 (b)), or appears to bear a logistic relationship with log-
parameter size (Figure 10 (c)). By comparison, the structured capabilities model estimates
factors with clusters of positive loadings on distinct tasks (Figure 11 (a)). My model
 17
 The order of the factors is arbitrary, so as a visual aid, I order them by descending variance explained.
 39
4 RESULTS 4.3 Comparison to observational scaling laws
 MSEtrain MSEtest
 Withheld subtask SC OSL Size SC OSL Size
 Boolean expressions 1.056 1.153 2.487 0.206 0.239 1.144
 Causal judgement 0.476 0.469 0.846 0.338 0.293 0.687
 Date understanding 0.464 0.462 1.419 0.250 0.149 1.022
 Disambiguation QA 1.536 1.519 2.592 0.608 0.680 1.764
 Formal fallacies 0.961 0.984 1.490 0.862 1.092 4.411
 Geometric shapes 0.937 0.965 1.891 0.370 0.467 1.277
 Hyperbaton 0.994 0.993 1.921 2.472 2.339 4.394
 Logical deduction 0.147 0.156 0.945 0.096 0.103 1.326
 Movie recommendation 0.348 0.362 0.964 0.958 0.966 1.328
 Navigate 1.877 2.034 2.617 0.504 1.260 3.926
 Object counting 0.707 0.737 1.336 0.661 0.470 0.783
 Penguins in a table 0.423 0.435 1.455 0.082 0.094 1.112
 Reasoning about colored objects 0.324 0.331 1.241 0.146 0.096 1.682
 Ruin names 0.902 1.169 2.008 0.351 0.974 1.816
 Snarks 1.248 1.274 2.106 0.528 0.527 3.260
 Sports understanding 1.099 1.197 2.433 1.612 1.379 2.041
 Temporal sequences 1.691 1.746 3.068 5.879 10.087 25.289
 Tracking shuffled objects 0.681 0.717 0.907 1.205 1.278 3.310
 Web of lies 0.477 0.528 0.556 4.835 5.500 7.084
 Average 0.860 0.907 1.699 1.156 1.473 3.561
Table 3: Prediction errors for held-out subtasks. Each column shows the mean-
squared error for predicting held-out subtasks with each different capability estimation
method. SC refers to my structured capabilities model with latent factor capability esti-
mates (Equation (16a)). OSL refers to the PCA decomposition approach from Ruan et al.
(2024)’s observational scaling laws (Equation (16b)). Size refers to Owen (2024)’s logis-
tic scaling laws using model parameter size (Equation (17)). Highlighted boldface values
indicate the lowest errors for each of MSEtrain and MSEtest .
estimates that Geometric shapes loads similarly on the first and second factors, each of
which shows a mild positive correlation with Geometric shapes scores (Figure 11 (b)).
Finally, multiple factors show a logistic shape when compared with log-parameter size
(Figure 11 (c)).
We also compare the proportions of variance explained in each model when predicting
held-out Geometric shapes subtask scores (Figure 12). In the observational scaling law
model, the first principal component dominates, explaining 76% of the variance in the
observed benchmark scores (Figure 12 (a)). Across all 18 other out-of-fold experiments,
this first principal component variance is never lower than 73%. In the structured capabil-
ities model, the factor loadings are more evenly spread. The largest three factors together
explain 84% of the variance (Figure 12 (b)).
 40
4 RESULTS 4.3 Comparison to observational scaling laws
(a) Heatmap of principal component weights per subtask, including held-out Geometric shapes task. The
weights for the held-out Geometric shapes task are estimated using the training set btrain
 p′ .
 (b) Models’ principal component scores against their raw Geometric Shapes subtask accuracy.
 (c) Models’ log-parameter sizes against their principal component scores.
Figure 10: Parameter estimates for the observational scaling law model. The heldout
task to predict is Geometric shapes.
 41
4 RESULTS 4.3 Comparison to observational scaling laws
(a) Heatmap of latent factor loadings per subtask. The factor loadings for the held-out Geometric shapes task
are estimated using the training set btrain
 p′ .
 (b) Models’ latent factor scores against their raw Geometric shapes subtask accuracy.
 (c) Models’ log-parameter sizes against their latent factor scores.
Figure 11: Parameter estimates for the structured capabilities model. The held-out
task to predict is Geometric shapes.
 42
4 RESULTS 4.3 Comparison to observational scaling laws
 (a) Proportion of variance explained per principal component.
(b) Proportion of communal variance explained per latent factor, equivalent to the proportional sum of
squared factor loadings.
Figure 12: Variance explained by estimated capabilities. For both models the held-out
task to predict is Geometric Shapes.
 43
5 DISCUSSION
5 Discussion
5.1 Principal findings
My results highlight the shortcomings of existing models for LLM capabilities. Both la-
tent factor models and observational scaling laws mistake LLM scale for a capability, and
this mistake limits their explanatory and predictive power. In comparison, the novel struc-
tured capabilities model outperforms both alternatives, providing a more parsimonious fit
than latent factor models and better predictive generalisation than observational scaling
laws.
5.2 Interpretation of results
Latent factor models and observational scaling laws conflate scale with capabilities.
In two experiments, latent factor models and observational scaling laws both fit a dom-
inant factor or principal component that correlates with LLMs’ log-parameter size. In
experiment A, the pure latent factor model estimates a single dominant factor explaining
72% of the communal variance across factor loadings. This factor bears a logistic rela-
tionship to the log-parameter size, with R2 = 0.474—a larger correlation than any other
estimated factor. This correlation appears moderate, but it is close to the highest corre-
lations between log-parameter size and individual benchmark performance I observed in
Figure 13, which are the basis for the effectiveness of Owen (2024)’s scaling laws. In
experiment B, the observational scaling law model consistently finds the first principal
component to explain over 73% of the total variance, and in one typical model, this prin-
cipal component also bears the strongest logistic relationship to the log-parameter size
(R2 = 0.528). In neither case is the model given explicit information about the parameter
sizes of the LLM sample: they are only given the observed benchmark scores. How-
ever, the dynamics behind each model’s parameter estimation lead them both to discover
a proxy for model size. For the latent factor model, I suspect that likelihood maximisa-
tion discovers the strong positive correlation between benchmark scores and parameter
size and consolidates this information in a single factor to improve the fit. For the ob-
servational scaling law model, PCA’s variance-maximising decomposition method leads
to the model capturing most of the variance due to parameter size in the largest principal
component.
The structured capabilities model outperforms both alternatives. My experimental
results show that the two previous models of LLM capabilities are more than just theoret-
 44
5 DISCUSSION 5.2 Interpretation of results
ically inelegant—they are statistically suboptimal on the metrics that their designers care
about. In experiment A, replacing the standard linear latent factor model with a logistic
model improves the absolute fit indices, and adding a structural parameter for parameter
size improves the Akaike and Bayesian information criteria. In simpler terms, the stan-
dard latent factor model is both a worse fit and a less parsimonious model of the LLM
benchmark data. The same structural regression model that outperforms the latent factor
model also beats observational scaling laws at predicting out-of-distribution performance.
In experiment B, across 19 out-of-fold prediction experiments for each of our BBH sub-
tasks, the structured capabilities model beats observational scaling laws on the majority of
subtasks and achieves lower average mean-squared errors on both training and test data.
The structured capabilities model captures capabilities with explanatory and predic-
tive power. Beyond objective improvements to model fit and predictive performance,
the structured capabilities model gives an interpretable picture of how the capabilities be-
hind BBH subtask performance emerge with scale. I consider these to be construct valid
capability estimates as far as we can estimate these from BBH benchmark tasks alone.
Figure 9 shows the factor loadings and factor scores for 5 capabilities across the BBH
subtasks. There are three major factors that explain descending proportions of variance.
These factors all correlate with parameter size, but they do so according to logistic curves
with different difficulty and discrimination parameters. Specifically, each next factor
shows a steeper curve that begins increasing at a larger parameter size than the previous
factor. These factors also load on thematically-related clusters of BBH subtasks. The first
capability, the quickest to increase with model scale, loads strongest on tasks involving
simple enumeration (Object counting, Penguins in a table), simple formula parsing (Date
understanding, Boolean expressions), and sentiment detection (Movie recommendation).
The second capability arises later with scale, and loads moderately on tasks that require
reasoning steps (Logical deduction, Formal fallacies) and strongly on tasks that seem to
require some semantic intuition, like sarcasm or common-sense causal reasoning (Snarks,
Ruin names, Causal judgement). The third capability is mostly present in the largest mod-
els, and loads on tasks requiring multiple steps of reasoning and state-tracking (Temporal
sequences, Tracking shuffled objects).
These capabilities are able to categorise and predict how performance will translate to
novel tasks. For example, the Geometric shapes task appears to require some formulaic
parsing, as well as some spatial reasoning and common-sense understanding. One expects
that the first two factors affect performance on this task, and indeed, these capabilities
appear relevant for predicting the held-out Geometric shapes scores in Figure 11 (a).
 45
5 DISCUSSION 5.3 Relation to other studies
5.3 Relation to other studies
My results comment directly on previous studies Burnell et al. (2023a) and Ilić & Gignac
(2024) that used latent factor models to estimate LLM capabilities. I replicated Burnell
et al.’s exploratory factor analysis method on the BBH benchmark dataset. I find their
technique underperforms the structured capabilities model in terms of both model fit and
parsimony. Burnell et al.’s model achieves acceptable fit on our dataset. Their own re-
ported model fit is poor, though I expect the improved result is due to the much larger
sample size—4, 395 in place of 29 models. However, an analysis of our replicated model
reveals the same deficiencies I hypothesised: the pure latent factor model fits a singular
factor with a large proportion of variance explained, a high loading across all benchmarks,
and a strong correlation with model size. In the structured capabilities model, the explicit
inclusion of parameter size as a variable shows this factor to be illusory. This point is most
significant when comparing these findings to Ilić & Gignac (2024). A central claim of Ilić
& Gignac’s study is the identification of an “Artificial General Ability” factor loading on
all indicator variables. My results suggest that this general factor is best explained as a
proxy for model scale, and that contrary to Ilić & Gignac’s finding, modelling a latent
general capability actually harms the explanatory power of the model.
Compared to observational scaling laws, my results show that allowing for measurement
error—which lowers the variance explained by the capability estimates—can result in
capabilities that are more interpretable and that generalise better to other tasks. This result
should be taken only tenuously as a critique of observational scaling laws for their purpose
as scaling laws for particular model families. In Ruan et al. (2024), a highlight of their
approach is that they can fit more precise scaling laws for model families—extrapolating
performance for larger versions of the same model—using a shared, low-dimensional
capability space. However, I do show that Ruan et al.’s choice to use PCA for extracting
these capabilities is flawed, and that a switch to latent factor estimates could improve their
model’s predictive generalisation.
This thesis also offers a concrete direction to answer calls made by AI position papers
like Wallach et al. (2024), Salaudeen et al. (2025), and others. These papers advocate
for the LLM research community to prioritise the construct validity of LLM benchmarks.
Many suggestions for improving construct validity—limiting contamination through ca-
nary strings, or reporting standard errors, for example—target specific problems in LLM
benchmarking outside the scope of capability modelling. Yet core aspects of construct
validity, like convergent and discriminant validity, are best justified through a quantitative
approach like the one I consider in this thesis.
 46
5 DISCUSSION 5.4 Limitations and future work
5.4 Limitations and future work
This experimental setup has several limitations that I must discuss in context with the
results.
First, I only estimate latent factors through exploratory factor analysis—I do not conduct
a confirmatory factor analysis. This choice places notable limitations on the interpretabil-
ity of my identified capabilities. In exploratory factor analysis, beyond deciding on the
number of factors with Horn’s parallel test (Section 3.2), my factors are free to estimate
any relationships supported by the data. Ilić & Gignac (2024)’s experiment instead uses
confirmatory factor analysis, and this approach allows for a stricter kind of hypothesis
testing that incorporates real theories about cognitive capabilities. If I want my latent
factors to represent capabilities in a more theory-driven fashion, future work should move
from an exploratory to a confirmatory approach following the best social scientific prac-
tices (Simms & Watson, 2007).
My modelling approach also presents limitations for the causal interpretation of my re-
sults. In some parts of this thesis I reference LLM capabilities ‘causing’ the benchmark
scores observed in the OpenLLM Leaderboard data. These scare quotes must stay in
place—there is no rigorous basis on which I can claim causality from my results. My
structured capabilities model is a purely observational model. Future studies could move
beyond this limitation with interventional techniques, like mechanistic interpretability
techniques for affecting the neural circuits linked to capabilities (Mayne et al., 2024).
My findings are also limited in scope by the choice to use only BIG-Bench Hard (BBH)
questions. These questions share particular formatting constraints, like their use of multi-
ple choice scoring, which can limit the experiments’ relevance to other benchmarking do-
mains, like open-ended response questions. Research shows that these different response
formats can produce different interpretations of LLM performance (Burnell et al., 2023b;
Schaeffer et al., 2023; Molfese et al., 2025). BIG-Bench Hard subtasks also present quite
contrived scenarios. These tasks test abstract skills, but they certainly fall short in terms of
their resemblance to real-world scenarios—an aspect called ecological validity in the lit-
erature on construct validity (Schmuckler, 2001). For another relevant domain limitation,
I should note that BIG-Bench Hard subtasks do nothing to assess the safety and align-
ment of AI systems to user intentions, another critical domain of LLM evaluation (Reuel
et al., 2025). Future work could extend these model comparisons to a more diverse range
of benchmarks, including benchmarks assessing safety capabilities, where the need to
understand the origins and the gaps in LLM performance is much more urgent.
 47
5 DISCUSSION 5.5 Implications
5.5 Implications
In this thesis, I demonstrate a statistical model that can extract interpretable and general-
isable capabilities from LLM benchmark results. This contribution has implications for
anyone interested in solving the LLM evaluation crisis. My new method provides the
first viable option for quantifying construct validity for LLM evaluations in a reputable
fashion.
Given the fluency with which modern LLMs produce natural language, and the rich cog-
nitive science theories we possess around ‘intelligence’ and ‘reasoning’ in humans, we
may be tempted to apply our cognitive theories to LLMs in a kind of ‘top-down’ fashion.
We might think that a mathematics benchmark measures a ‘mathematical reasoning’ ca-
pability in LLMs because we would recognise this proficiency in humans who performed
well on the benchmark. Yet LLMs and humans are different cognitive systems. Humans
are not trained on data in a way that risks contamination, and humans do not have scaling
laws that predict their performance. For these reasons and others, a ‘top-down’ approach
to LLM capabilities is misguided. We cannot expect to port entire systems from cognitive
science to LLMs, like the Cattell-Horn-Carroll model of cognitive capabilities (Cattell &
Horn, 1978; Carroll, 1997; Schneider & McGrew, 2018), without distorting these models
in the process. This limitation applies also to our measurement tools. We cannot expect
that latent factor models apply directly to LLM benchmarks in the way that they apply
to human standardised tests and personality surveys. Allowances should be made for the
unique challenges posed by LLM evaluation. My experiments provide a modelling ap-
proach that incorporates one unique element of LLM evaluation—the impact of scaling
laws—and shows the penalty of ignoring these allowances: existing models are misfit and
they generalise worse to new benchmarks.
For researchers at the intersection of cognitive science and AI, my methods point to-
wards a more constructive, ‘bottom-up’ approach to LLM capabilities and the problem of
construct validity in LLM evaluations. Given their predictive success, we know that we
cannot ignore neural scaling laws. At the same time, we should retain the benefits that
measurement theory affords models in the social sciences. The combination of these two,
in the form of a structured capabilities model, provides a method that should be familiar
enough to both cognitive scientists and computer scientists to provide a basis for formal
models of construct validity. I advocate that future experiments answering the calls of
Wallach et al. (2024) and Salaudeen et al. (2025) utilise similar approaches when trying
to demonstrate construct validity in LLM benchmarks. Further, I hope that future bench-
mark designers take construct validity more seriously, and that they are inspired by the
provided formal toolkit to design evaluations with better validity guarantees. Studies like
 48
5 DISCUSSION 5.5 Implications
Polo et al. (2024) show the potential benefits of successful social science techniques ap-
plied to benchmarks: we can run smaller evaluations with better statistical guarantees, and
we can provide stronger safety and alignment guarantees for frontier systems in health-
care, education, and judicial settings.
For AI policymakers, these experiments highlight the importance of cross-disciplinary
collaboration when it comes to understanding large language models. From both a cogni-
tive science and a computer science perspective, these new AI systems are unprecedented
and exciting. As Ganguli et al. (2022) argue, their surprising behaviours should be cause
for policy and governance concerns. If siloed approaches to understanding their capabil-
ities will be suboptimal, it is essential that the scientific community’s recommendations
involve all relevant disciplines. My aim in this thesis is to provide one small example
of what a cross-disciplinary approach can achieve. I hope to provoke larger and more
ambitious crossovers for understanding artificial intelligence.
 49
6 CONCLUSION
6 Conclusion
LLM evaluation faces an ongoing crisis. To trust our evaluations—whether to understand
LLM capabilities, or to predict how benchmarks will translate to the real world—we need
formal models that identify general capabilities from our benchmark scores. This thesis
presents the structured capabilities model, first model capable of extracting interpretable
and generalisable capabilities. Two experiments demonstrate the model’s improvements
over existing alternatives from both social science and computer science.
I sample the largest publicly available population of LLMs, 4, 395 models uploaded to the
OpenLLM Leaderboard, and collect performances on 19 subtasks from the BBH dataset.
I use this collection of benchmark scores to fit three formal models of LLM capabili-
ties. Two models represent the latest developments in separate subdisciplines of AI re-
search—latent factor models, inspired by cognitive science techniques, and observational
scaling laws, inspired by computer science techniques. The third model is the structured
capabilities model, my novel hybrid of the previous two.
In one experiment, the structured capabilities model outperforms a latent factor model in
terms of both model fit and parsimony. In a second experiment, the structured capabilities
model outperforms an observational scaling law model at predicting out-of-distribution
subtask accuracies. Put together, I argue that combining these two techniques improves
our explanatory and predictive power when estimating LLM capabilities.
The AI research community believes that construct validity is essential for escaping the
evaluation crisis. To ensure fair and effective AI governance, policymakers need clear
descriptions of LLM capabilities from AI researchers. AI researchers need trustworthy
measurements of these capabilities, and for that, they need access to formal methods that
clarify the capabilities behind benchmark performances. My approach provides evidence
that the best model for such a task combines insights across the social science and com-
puter science disciplines.
 50
REFERENCES
References
H. Akaike. A new look at the statistical model identification. IEEE Transactions on
 Automatic Control, 19(6):716–723, 1974. doi: 10.1109/TAC.1974.1100705.
Ahmed Alaa, Thomas Hartvigsen, Niloufar Golchini, Shiladitya Dutta, Frances Dean,
 Inioluwa Deborah Raji, and Travis Zack. Medical large language model bench-
 marks should prioritize construct validity, 2025. URL https://arxiv.org/abs/
 2503.10694. arXiv: 2503.10694 [cs.CL].
Andrew M. Bean, Rebecca Payne, Guy Parsons, Hannah Rose Kirk, Juan Ciro, Rafael
 Mosquera, Sara Hincapié Monsalve, Aruna S. Ekanayaka, Lionel Tarassenko, Luc
 Rocher, and Adam Mahdi. Clinical knowledge in LLMs does not translate to human
 interactions, 2025. URL https://arxiv.org/abs/2504.18919.
Emily M. Bender and Alexander Koller. Climbing towards NLU: On Meaning, Form, and
 Understanding in the Age of Data. In Proceedings of the 58th Annual Meeting of the
 Association for Computational Linguistics, pp. 5185–5198, Online, 2020. Association
 for Computational Linguistics. doi: 10.18653/v1/2020.acl-main.463. URL https:
 //www.aclweb.org/anthology/2020.acl-main.463.
Emily M. Bender, Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell.
 On the dangers of stochastic parrots: Can language models be too big? In Proceedings
 of the 2021 ACM Conference on Fairness, Accountability, and Transparency, FAccT
 ’21, pp. 610–623, New York, NY, USA, 2021. Association for Computing Machinery.
 ISBN 9781450383097. doi: 10.1145/3442188.3445922. URL https://doi.org/
 10.1145/3442188.3445922.
Peter M Bentler. Comparative fit indexes in structural models. Psychological bulletin,
 107(2):238, 1990.
Idan A. Blank. What are large language models supposed to model? Trends in Cognitive
 Sciences, 27(11):987–989, November 2023. ISSN 1364-6613. doi: 10.1016/j.tics.
 2023.08.006. URL https://doi.org/10.1016/j.tics.2023.08.006.
Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney
 von Arx, Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill,
 Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon, Niladri Chatterji,
 Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora Demszky, Chris Donahue,
 Moussa Doumbouya, Esin Durmus, Stefano Ermon, John Etchemendy, Kawin Etha-
 yarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren Gillespie, Karan Goel, Noah
 Goodman, Shelby Grossman, Neel Guha, Tatsunori Hashimoto, Peter Henderson, John
 Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas Icard, Saahil
 Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling, Fereshte
 Khani, Omar Khattab, Pang Wei Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi,
 Ananya Kumar, Faisal Ladhak, Mina Lee, Tony Lee, Jure Leskovec, Isabelle Levent,
 Xiang Lisa Li, Xuechen Li, Tengyu Ma, Ali Malik, Christopher D. Manning, Suvir
 Mirchandani, Eric Mitchell, Zanele Munyikwa, Suraj Nair, Avanika Narayan, Deepak
 51
REFERENCES
 Narayanan, Ben Newman, Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan, Julian
 Nyarko, Giray Ogut, Laurel Orr, Isabel Papadimitriou, Joon Sung Park, Chris Piech,
 Eva Portelance, Christopher Potts, Aditi Raghunathan, Rob Reich, Hongyu Ren, Frieda
 Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher Ré, Dorsa Sadigh, Shiori
 Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, Alex Tamkin, Rohan
 Taori, Armin W. Thomas, Florian Tramèr, Rose E. Wang, William Wang, Bohan Wu,
 Jiajun Wu, Yuhuai Wu, Sang Michael Xie, Michihiro Yasunaga, Jiaxuan You, Matei
 Zaharia, Michael Zhang, Tianyi Zhang, Xikun Zhang, Yuhui Zhang, Lucia Zheng, Kait-
 lyn Zhou, and Percy Liang. On the opportunities and risks of foundation models, 2022.
 URL https://arxiv.org/abs/2108.07258.
Samuel R. Bowman and George Dahl. What Will it Take to Fix Benchmarking in Nat-
 ural Language Understanding? In Proceedings of the 2021 Conference of the North
 American Chapter of the Association for Computational Linguistics: Human Language
 Technologies, pp. 4843–4855. Association for Computational Linguistics, 2021. doi:
 10.18653/v1/2021.naacl-main.385. URL https://aclanthology.org/2021.
 naacl-main.385.
Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Pra-
 fulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
 Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Re-
 won Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris
 Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
 Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever,
 and Dario Amodei. Language models are few-shot learners. In H. Larochelle,
 M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (eds.), Advances in neural in-
 formation processing systems, volume 33, pp. 1877–1901. Curran Associates, Inc.,
 2020. URL https://proceedings.neurips.cc/paper_files/paper/
 2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf.
Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz,
 Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid
 Palangi, Marco Tulio Ribeiro, and Yi Zhang. Sparks of Artificial General Intelli-
 gence: Early experiments with GPT-4, April 2023. URL http://arxiv.org/
 abs/2303.12712. arXiv:2303.12712 [cs].
Ryan Burnell, Han Hao, Andrew R. A. Conway, and Jose Hernandez Orallo. Revealing
 the structure of language model capabilities, 2023a. URL http://arxiv.org/
 abs/2306.10062.
Ryan Burnell, Wout Schellaert, John Burden, Tomer D. Ullman, Fernando Martinez-
 Plumed, Joshua B. Tenenbaum, Danaja Rutar, Lucy G. Cheke, Jascha Sohl-Dickstein,
 Melanie Mitchell, Douwe Kiela, Murray Shanahan, Ellen M. Voorhees, Anthony G.
 Cohn, Joel Z. Leibo, and Jose Hernandez-Orallo. Rethink reporting of evaluation re-
 sults in AI. Science, 380(6641):136–138, 2023b. doi: 10.1126/science.adf6369. URL
 https://www.science.org/doi/abs/10.1126/science.adf6369.
 tex.eprint: https://www.science.org/doi/pdf/10.1126/science.adf6369.
 52
REFERENCES
Kenrick Cai and Jaspreet Singh. Google clinches milestone gold at global math com-
 petition, while OpenAI also claims win. Reuters, July 2025. URL https://www.
 reuters.com/world/asia-pacific/.
John B. Carroll. Psychometrics, intelligence, and public perception. Intelligence,
 24(1):25–52, January 1997. ISSN 0160-2896. doi: 10.1016/s0160-2896(97)
 90012-x. URL https://linkinghub.elsevier.com/retrieve/pii/
 S016028969790012X.
Raymond B. Cattell and John L. Horn. A check on the theory of fluid and crystal-
 lized intelligence with description of new subtest designs. Journal of Educational
 Measurement, 15(3):139–164, 1978. ISSN 00220655, 17453984. URL http:
 //www.jstor.org/stable/1433661.
R. Philip Chalmers. Mirt: A Multidimensional Item Response Theory Package for the
 R Environment. Journal of Statistical Software, 48(6), 2012. ISSN 1548-7660. doi:
 10.18637/jss.v048.i06. URL http://www.jstatsoft.org/v48/i06/.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto,
 Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray,
 Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
 Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power,
 Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Pet-
 roski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes,
 Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak,
 Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christo-
 pher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa,
 Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter
 Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wo-
 jciech Zaremba. Evaluating large language models trained on code, 2021. URL
 https://arxiv.org/abs/2107.03374.
Wei-Lin Chiang, Lianmin Zheng, Ying Sheng, Anastasios Nikolas Angelopoulos, Tianle
 Li, Dacheng Li, Hao Zhang, Banghua Zhu, Michael Jordan, Joseph E. Gonzalez, and
 Ion Stoica. Chatbot arena: An open platform for evaluating LLMs by human prefer-
 ence, 2024. URL https://arxiv.org/abs/2403.04132. arXiv: 2403.04132
 [cs.AI].
Lee Anna Clark and David Watson. Constructing validity: New developments in creat-
 ing objective measuring instruments. Psychological Assessment, 31(12):1412–1427,
 2019. ISSN 1939-134X, 1040-3590. doi: 10.1037/pas0000626. URL https:
 //doi.apa.org/doi/10.1037/pas0000626.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz
 Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher
 Hesse, and John Schulman. Training Verifiers to Solve Math Word Problems, 2021.
 URL https://arxiv.org/abs/2110.14168. Version Number: 2.
Cohere. Introduction to Large Language Models, 2022. URL https://docs.
 cohere.ai/docs/introduction-to-large-language-models.
 53
REFERENCES
Lee J Cronbach and Paul E Meehl. Construct validity in psychological tests. Psychologi-
 cal bulletin, 52(4):281, 1955. Publisher: American Psychological Association.
J M Digman. Personality Structure: Emergence of the Five-Factor Model. Annual Re-
 view of Psychology, 41(1):417–440, January 1990. ISSN 0066-4308, 1545-2085. doi:
 10.1146/annurev.ps.41.020190.002221. URL https://www.annualreviews.
 org/doi/10.1146/annurev.ps.41.020190.002221.
David Donoho. 50 Years of Data Science. Journal of Computational and Graphi-
 cal Statistics, 26(4):745–766, October 2017. ISSN 1061-8600, 1537-2715. doi: 10.
 1080/10618600.2017.1384734. URL https://www.tandfonline.com/doi/
 full/10.1080/10618600.2017.1384734.
Susan E. Embretson and Steven P. Reise. Item Response Theory for Psychologists.
 Psychology Press, 1st edition, September 2013. ISBN 978-1-4106-0526-9. doi:
 10.4324/9781410605269. URL https://www.taylorfrancis.com/books/
 9781135681470.
Epoch AI. Data on AI models, 2025. URL https://epoch.ai/data/
 ai-models. Accessed: 2025-07-25.
Martin Ester, Hans-Peter Kriegel, Jörg Sander, and Xiaowei Xu. A density-based algo-
 rithm for discovering clusters in large spatial databases with noise. In Proceedings
 of the Second International Conference on Knowledge Discovery and Data Mining,
 KDD’96, pp. 226–231. AAAI Press, 1996.
Council of the European Union European Parliament. Article 51: Classification of
 General-Purpose AI Models as General-Purpose AI Models with Systemic Risk. In
 Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June
 2024 laying down harmonised rules on artificial intelligence and amending Regula-
 tions, June 2024.
Brian Everitt. An Introduction to Latent Variable Models. Monographs on Statistics and
 Applied Probability. Chapman and Hall, 1984. ISBN 978-0-412-25310-2.
Leandre R. Fabrigar and Duane T. Wegener (eds.). Exploratory Factor Analysis. Series
 in Understanding Statistics. Oxford University Press, 2012. ISBN 978-0-19-973417-7
 978-0-19-981351-3 978-1-283-62144-1.
John F. Finch and Stephen G. West. The Investigation of Personality Structure: Sta-
 tistical Models. Journal of Research in Personality, 31(4):439–485, December 1997.
 ISSN 0092-6566. doi: 10.1006/jrpe.1997.2194. URL https://linkinghub.
 elsevier.com/retrieve/pii/S0092656697921942.
Lukas Finnveden. Extrapolating GPT-N performance, December 2020. URL
 https://www.lesswrong.com/posts/k2SNji3jXaLGhBeYP/
 extrapolating-gpt-n-performance.
Clementine Fourrier, Nathan Habib, Alina Lozovskaya, Konrad Szafer, and Thomas Wolf.
 Performances are plateauing, let’s make the leaderboard steep again, June 2024a. URL
 https://huggingface.co/spaces/open-llm-leaderboard/blog.
 54
REFERENCES
Clémentine Fourrier. It’s been a wild ride, folks :) (end of the Open LLM
 Leaderboard), 2025. URL https://huggingface.co/spaces/
 open-llm-leaderboard/open_llm_leaderboard/discussions/
 1135.
Clémentine Fourrier, Nathan Habib, Alina Lozovskaya, Konrad Szafer, and Thomas Wolf.
 Open LLM leaderboard v2, 2024b. URL https://huggingface.co/spaces/
 open-llm-leaderboard/open_llm_leaderboard.
Carl Benedikt Frey and Michael Osborne. Generative AI and the Future of Work: A
 Reappraisal. The Brown Journal of World Affairs, XXX(1):1–17, 2023.
Deep Ganguli, Danny Hernandez, Liane Lovitt, Amanda Askell, Yuntao Bai, Anna
 Chen, Tom Conerly, Nova Dassarma, Dawn Drain, Nelson Elhage, Sheer El Showk,
 Stanislav Fort, Zac Hatfield-Dodds, Tom Henighan, Scott Johnston, Andy Jones,
 Nicholas Joseph, Jackson Kernian, Shauna Kravec, Ben Mann, Neel Nanda, Ka-
 mal Ndousse, Catherine Olsson, Daniela Amodei, Tom Brown, Jared Kaplan, Sam
 McCandlish, Christopher Olah, Dario Amodei, and Jack Clark. Predictability and
 Surprise in Large Generative Models. In 2022 ACM Conference on Fairness, Ac-
 countability, and Transparency, pp. 1747–1764, Seoul Republic of Korea, June 2022.
 ACM. ISBN 978-1-4503-9352-2. doi: 10.1145/3531146.3533229. URL https:
 //dl.acm.org/doi/10.1145/3531146.3533229.
Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster,
 Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al. The pile: An 800gb
 dataset of diverse text for language modeling. arXiv preprint arXiv:2101.00027, 2020.
Leo Gao, Jonathan Tow, Baber Abbasi, Stella Biderman, Sid Black, Anthony DiPofi,
 Charles Foster, Laurence Golding, Jeffrey Hsu, Alain Le Noac’h, Haonan Li, Kyle
 McDonell, Niklas Muennighoff, Chris Ociepa, Jason Phang, Laria Reynolds, Hailey
 Schoelkopf, Aviya Skowron, Lintang Sutawika, Eric Tang, Anish Thite, Ben Wang,
 Kevin Wang, and Andy Zou. The language model evaluation harness, 07 2024. URL
 https://zenodo.org/records/12608602.
Felipe L. Gewers, Gustavo R. Ferreira, Henrique F. De Arruda, Filipi N. Silva, Cesar H.
 Comin, Diego R. Amancio, and Luciano Da F. Costa. Principal Component Analysis:
 A Natural Approach to Data Exploration. ACM Computing Surveys, 54(4):1–34, May
 2022. ISSN 0360-0300, 1557-7341. doi: 10.1145/3447755. URL https://dl.
 acm.org/doi/10.1145/3447755.
Elliot Glazer, Ege Erdil, Tamay Besiroglu, Diego Chicharro, Evan Chen, Alex Gunning,
 Caroline Falkman Olsson, Jean-Stanislas Denain, Anson Ho, Emily de Oliveira San-
 tos, Olli Järviniemi, Matthew Barnett, Robert Sandler, Matej Vrzala, Jaime Sevilla,
 Qiuyu Ren, Elizabeth Pratt, Lionel Levine, Grant Barkley, Natalie Stewart, Bogdan
 Grechuk, Tetiana Grechuk, Shreepranav Varma Enugandla, and Mark Wildon. Fron-
 tierMath: A benchmark for evaluating advanced mathematical reasoning in AI, 2024.
 URL https://arxiv.org/abs/2411.04872.
Lewis R Goldberg. The development of markers for the big-five factor structure. Psycho-
 logical assessment, 4(1):26, 1992.
 55
REFERENCES
Ian Goodfellow, Yoshua Bengio, Aaron Courville, and Yoshua Bengio. Deep learning,
 volume 1. MIT Press, 2016.
Ben Goodrich, Vinay Rao, Peter J Liu, and Mohammad Saleh. Assessing the factual
 accuracy of generated text. In proceedings of the 25th ACM SIGKDD international
 conference on knowledge discovery & data mining, pp. 166–175, 2019.
Sidney Greenbaum. ICE: The international corpus of english. English Today, 7(4):3–7,
 1991.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang,
 Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the
 MATH dataset. In Thirty-fifth Conference on Neural Information Processing Systems
 Datasets and Benchmarks Track (Round 2), 2021.
Tom Henighan, Jared Kaplan, Mor Katz, Mark Chen, Christopher Hesse, Jacob Jackson,
 Heewoo Jun, Tom B. Brown, Prafulla Dhariwal, Scott Gray, Chris Hallacy, Benjamin
 Mann, Alec Radford, Aditya Ramesh, Nick Ryder, Daniel M. Ziegler, John Schulman,
 Dario Amodei, and Sam McCandlish. Scaling laws for autoregressive generative mod-
 eling, 2020. URL https://arxiv.org/abs/2010.14701.
Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai,
 Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan
 Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan
 Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Oriol Vinyals,
 Jack W. Rae, and Laurent Sifre. Training compute-optimal large language models. In
 Proceedings of the 36th International Conference on Neural Information Processing
 Systems. Curran Associates Inc., 2022. ISBN 978-1-71387-108-8.
John L. Horn. A Rationale and Test for the Number of Factors in Factor Analy-
 sis. Psychometrika, 30(2):179–185, June 1965. ISSN 0033-3123, 1860-0980. doi:
 10.1007/bf02289447. URL https://www.cambridge.org/core/product/
 identifier/S003331230004165X/type/journal_article.
Li-tze Hu and Peter M. Bentler. Fit indices in covariance structure modeling: Sensitivity
 to underparameterized model misspecification. Psychological Methods, 3(4):424–453,
 December 1998. ISSN 1939-1463, 1082-989X. doi: 10.1037/1082-989x.3.4.424. URL
 https://doi.apa.org/doi/10.1037/1082-989X.3.4.424.
Li-tze Hu and Peter M. Bentler. Cutoff criteria for fit indexes in covariance structure
 analysis: Conventional criteria versus new alternatives. Structural Equation Model-
 ing: A Multidisciplinary Journal, 6(1):1–55, January 1999. ISSN 1070-5511, 1532-
 8007. doi: 10.1080/10705519909540118. URL http://www.tandfonline.
 com/doi/abs/10.1080/10705519909540118.
HuggingFace. HuggingFace Spaces, July 2025. URL https://huggingface.co/
 spaces?sort=likes.
 56
REFERENCES
David Ilić and Gilles E. Gignac. Evidence of interrelated cognitive-like capabilities
 in large language models: Indications of artificial general intelligence or achieve-
 ment? Intelligence, 106:101858, 2024. ISSN 01602896. doi: 10.1016/j.intell.2024.
 101858. URL https://linkinghub.elsevier.com/retrieve/pii/
 S0160289624000527.
Abigail Z. Jacobs. Measurement as governance in and for responsible AI, 2021. URL
 https://arxiv.org/abs/2109.05658.
Abigail Z. Jacobs and Hanna Wallach. Measurement and Fairness. In Proceedings of the
 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 375–385.
 ACM, March 2021. ISBN 978-1-4503-8309-7. doi: 10.1145/3442188.3445901. URL
 https://dl.acm.org/doi/10.1145/3442188.3445901.
Bowen Jiang, Yangxinyu Xie, Zhuoqun Hao, Xiaomeng Wang, Tanwi Mallick, Weijie J
 Su, Camillo Jose Taylor, and Dan Roth. A Peek into Token Bias: Large Language Mod-
 els Are Not Yet Genuine Reasoners. In Proceedings of the 2024 Conference on Empir-
 ical Methods in Natural Language Processing, pp. 4722–4756, Miami, Florida, USA,
 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.emnlp-main.
 272. URL https://aclanthology.org/2024.emnlp-main.272.
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and
 Karthik R Narasimhan. SWE-bench: Can language models resolve real-world github
 issues? In The Twelfth International Conference on Learning Representations, 2024.
 URL https://openreview.net/forum?id=VTF8yNQM66.
Daniel Jurafsky and James H. Martin. N-Gram Language Models, chapter 3, pp. 1–26.
 Online manuscript, 3rd edition, January 2025. URL https://web.stanford.
 edu/~jurafsky/slp3/.
Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Re-
 won Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling Laws
 for Neural Language Models, 2020. URL https://arxiv.org/abs/2001.
 08361.
Andrej Karpathy. My reaction is that there is an evaluation crisis. I don’t really know what
 metrics to look at right now., March 2025. URL https://x.com/karpathy/
 status/1896266683301659068.
Ryan Othniel Kearns. Testlet effects in the difficulty of BIG-Bench Hard tasks, January
 2025. Summative assessment for Applied Analytical Statistics, Michaelmas 2024, Ox-
 ford Internet Institute, University of Oxford.
Rex B. Kline. Specification and Identification of Confirmatory Factor Analysis Models,
 pp. 188–211. Principles and Practice of Structural Equation Modeling. The Guilford
 Press, fourth edition, 2016. ISBN 978-1-4625-2336-8.
Vid Kocijan, Ernest Davis, Thomas Lukasiewicz, Gary Marcus, and Leora Morgenstern.
 The defeat of the Winograd Schema Challenge. Artificial Intelligence, 325:103971,
 57
REFERENCES
 December 2023. ISSN 00043702. doi: 10.1016/j.artint.2023.103971. URL https:
 //linkinghub.elsevier.com/retrieve/pii/S0004370223001170.
Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa.
 Large language models are zero-shot reasoners. Advances in neural information pro-
 cessing systems, 35:22199–22213, 2022.
Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh,
 Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Nat-
 ural questions: A benchmark for question answering research. Transactions of the
 Association for Computational Linguistics, 7:453–466, 2019.
Percy Liang, Rishi Bommasani, Tony Lee, Dimitris Tsipras, Dilara Soylu, Michihiro Ya-
 sunaga, Yian Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Kumar, Benjamin New-
 man, Binhang Yuan, Bobby Yan, Ce Zhang, Christian Alexander Cosgrove, Christo-
 pher D Manning, Christopher Re, Diana Acosta-Navas, Drew Arad Hudson, Eric Ze-
 likman, Esin Durmus, Faisal Ladhak, Frieda Rong, Hongyu Ren, Huaxiu Yao, Jue
 WANG, Keshav Santhanam, Laurel Orr, Lucia Zheng, Mert Yuksekgonul, Mirac Suz-
 gun, Nathan Kim, Neel Guha, Niladri S. Chatterji, Omar Khattab, Peter Henderson,
 Qian Huang, Ryan Andrew Chi, Sang Michael Xie, Shibani Santurkar, Surya Ganguli,
 Tatsunori Hashimoto, Thomas Icard, Tianyi Zhang, Vishrav Chaudhary, William Wang,
 Xuechen Li, Yifan Mai, Yuhui Zhang, and Yuta Koreeda. Holistic evaluation of lan-
 guage models. Transactions on Machine Learning Research, 2023. ISSN 2835-8856.
 URL https://openreview.net/forum?id=iO4LZibEqW.
Mark Liberman. Obituary: Fred Jelinek. Computational Linguistics, 36(4):595–599,
 December 2010. doi: 10.1162/coli_a_00032. URL https://aclanthology.
 org/J10-4001/.
Stephanie Lin, Jacob Hilton, and Owain Evans. TruthfulQA: Measuring how models
 mimic human falsehoods. In Smaranda Muresan, Preslav Nakov, and Aline Villavi-
 cencio (eds.), Proceedings of the 60th annual meeting of the association for compu-
 tational linguistics (volume 1: Long papers), pp. 3214–3252, Dublin, Ireland, 2022.
 Association for Computational Linguistics. doi: 10.18653/v1/2022.acl-long.229. URL
 https://aclanthology.org/2022.acl-long.229/. tex.join_key: 248.
Hongwei Liu, Zilong Zheng, Yuxuan Qiao, Haodong Duan, Zhiwei Fei, Fengzhe Zhou,
 Wenwei Zhang, Songyang Zhang, Dahua Lin, and Kai Chen. MathBench: Eval-
 uating the theory and application proficiency of LLMs with a hierarchical mathe-
 matics benchmark. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.),
 Findings of the Association for Computational Linguistics: ACL 2024, pp. 6884–
 6915, Bangkok, Thailand, August 2024. Association for Computational Linguistics.
 doi: 10.18653/v1/2024.findings-acl.411. URL https://aclanthology.org/
 2024.findings-acl.411/.
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is your code gener-
 ated by ChatGPT really correct? rigorous evaluation of large language models for code
 generation. In Thirty-seventh Conference on Neural Information Processing Systems,
 2023. URL https://openreview.net/forum?id=1qvx610Cu7.
 58
REFERENCES
Thang Luong and Edward Lockhart. Advanced version of Gemini with Deep Think offi-
 cially achieves gold-medal standard at the International Mathematical Olympiad, July
 2025. URL https://deepmind.google/discover/blog/.
Mathematical Association of America. American invitational mathematics examina-
 tion - AIME, February 2024. URL https://maa.org/math-competitions/
 american-invitational-mathematics-examination-aime.
Harry Mayne, Yushi Yang, and Adam Mahdi. Can sparse autoencoders be used to decom-
 pose and interpret steering vectors? In MINT: Foundation Model Interventions, 2024.
 URL https://openreview.net/forum?id=QRpzG4b5dz.
Bryan McCann, Nitish Shirish Keskar, Caiming Xiong, and Richard Socher. The natural
 language decathlon: Multitask learning as question answering, 2018. URL https:
 //arxiv.org/abs/1806.08730.
John McCarthy, Marvin L. Minsky, Nathaniel Rochester, and Claude E. Shannon.
 A proposal for the Dartmouth Summer Research Project on Artificial Intelligence,
 August 31, 1955. AI Magazine, 27(4):12, December 2006. doi: 10.1609/
 aimag.v27i4.1904. URL https://ojs.aaai.org/aimagazine/index.
 php/aimagazine/article/view/1904.
R. Thomas McCoy, Shunyu Yao, Dan Friedman, Matthew Hardy, and Thomas L. Grif-
 fiths. Embers of Autoregression: Understanding Large Language Models Through the
 Problem They are Trained to Solve, September 2023. URL http://arxiv.org/
 abs/2309.13638. arXiv:2309.13638 [cs].
Samuel Messick. Test Validity: A Matter of Consequence. Social Indicators Research,
 45(1/3):35–44, 1998. ISSN 03038300. doi: 10.1023/A:1006964925094. URL http:
 //link.springer.com/10.1023/A:1006964925094.
Todor Mihaylov, Peter Clark, Tushar Khot, and Ashish Sabharwal. Can a suit of ar-
 mor conduct electricity? Anew dataset for open book question answering. In Ellen
 Riloff, David Chiang, Julia Hockenmaier, and Jun’ichi Tsujii (eds.), Proceedings of the
 2018 Conference on Empirical Methods in Natural Language Processing, pp. 2381–
 2391, Brussels, Belgium, October-November 2018. Association for Computational
 Linguistics. doi: 10.18653/v1/D18-1260. URL https://aclanthology.org/
 D18-1260/.
Seyed Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio,
 and Mehrdad Farajtabar. GSM-Symbolic: Understanding the limitations of mathemat-
 ical reasoning in large language models. In The thirteenth international conference on
 learning representations, 2025. URL https://openreview.net/forum?id=
 AjXkRZIvjB.
Moran Mizrahi, Guy Kaplan, Dan Malkin, Rotem Dror, Dafna Shahaf, and Gabriel
 Stanovsky. State of what art? A call for multi-prompt LLM evaluation. Transactions of
 the Association for Computational Linguistics, 12:933–949, 2024. doi: 10.1162/tacl_
 a_00681. URL https://aclanthology.org/2024.tacl-1.52/.
 59
REFERENCES
Francesco Maria Molfese, Luca Moroni, Luca Gioffré, Alessandro Scirè, Simone Co-
 nia, and Roberto Navigli. Right answer, wrong score: Uncovering the inconsistencies
 of LLM evaluation in multiple-choice question answering. In Wanxiang Che, Joyce
 Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (eds.), Findings of the
 Association for Computational Linguistics: ACL 2025, pp. 18477–18494, Vienna, Aus-
 tria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-256-5.
 URL https://aclanthology.org/2025.findings-acl.950/.
Amanda K. Montoya and Michael C. Edwards. The Poor Fit of Model Fit for Selecting
 Number of Factors in Exploratory Factor Analysis for Scale Evaluation. Educational
 and Psychological Measurement, 81(3):413–440, June 2021. ISSN 0013-1644, 1552-
 3888. doi: 10.1177/0013164420942899. URL https://journals.sagepub.
 com/doi/10.1177/0013164420942899.
Shashi Narayan, Shay B. Cohen, and Mirella Lapata. Don’t give me the details, just
 the summary! Topic-aware convolutional neural networks for extreme summariza-
 tion. In Ellen Riloff, David Chiang, Julia Hockenmaier, and Jun’ichi Tsujii (eds.),
 Proceedings of the 2018 Conference on Empirical Methods in Natural Language
 Processing, pp. 1797–1807, Brussels, Belgium, October-November 2018. Associa-
 tion for Computational Linguistics. doi: 10.18653/v1/D18-1206. URL https:
 //aclanthology.org/D18-1206/.
David Owen. How predictable is language model benchmark performance? arXiv
 preprint arXiv:2401.04757, 2024.
Alicia Parrish, Angelica Chen, Nikita Nangia, Vishakh Padmakumar, Jason Phang, Jana
 Thompson, Phu Mon Htut, and Samuel Bowman. BBQ: A hand-built bias benchmark
 for question answering. In Smaranda Muresan, Preslav Nakov, and Aline Villavicen-
 cio (eds.), Findings of the Association for Computational Linguistics: ACL 2022, pp.
 2086–2105, Dublin, Ireland, May 2022. Association for Computational Linguistics.
 doi: 10.18653/v1/2022.findings-acl.165. URL https://aclanthology.org/
 2022.findings-acl.165/.
Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhang, Sean Shi,
 Michael Choi, Anish Agrawal, Arnav Chopra, Adam Khoja, Ryan Kim, Jason Hausen-
 loy, Oliver Zhang, Mantas Mazeika, Daron Anderson, Tung Nguyen, Mobeen Mah-
 mood, Fiona Feng, Steven Y. Feng, Haoran Zhao, Michael Yu, Varun Gangal, Chelsea
 Zou, Zihan Wang, Jessica P. Wang, Pawan Kumar, Oleksandr Pokutnyi, Robert Ger-
 bicz, Serguei Popov, John-Clark Levin, Mstyslav Kazakov, Johannes Schmitt, Geoff
 Galgon, Alvaro Sanchez, Yongki Lee, Will Yeadon, Scott Sauers, Marc Roth, Chi-
 dozie Agu, Søren Riis, Fabian Giska, Saiteja Utpala, Zachary Giboney, Gashaw M.
 Goshu, Joan of Arc Xavier, Sarah-Jane Crowson, Mohinder Maheshbhai Naiya, Noah
 Burns, Lennart Finke, Zerui Cheng, Hyunwoo Park, Francesco Fournier-Facio, John
 Wydallis, Mark Nandor, Ankit Singh, Tim Gehrunger, Jiaqi Cai, Ben McCarty, Dar-
 ling Duclosel, Jungbae Nam, Jennifer Zampese, Ryan G. Hoerr, Aras Bacho, Gau-
 tier Abou Loume, Abdallah Galal, Hangrui Cao, Alexis C. Garretson, Damien Sileo,
 Qiuyu Ren, Doru Cojoc, Pavel Arkhipov, Usman Qazi, Lianghui Li, Sumeet Mot-
 wani, Christian Schröder de Witt, Edwin Taylor, Johannes Veith, Eric Singer, Tay-
 60
REFERENCES
 lor D. Hartman, Paolo Rissone, Jaehyeok Jin, Jack Wei Lun Shi, Chris G. Willcocks,
 Joshua Robinson, Aleksandar Mikov, Ameya Prabhu, Longke Tang, Xavier Alapont,
 Justine Leon Uro, Kevin Zhou, Emily de Oliveira Santos, Andrey Pupasov Maksimov,
 Edward Vendrow, Kengo Zenitani, Julien Guillod, Yuqi Li, Joshua Vendrow, Vladyslav
 Kuchkin, and Ng Ze-An. Humanity’s last exam. CoRR, abs/2501.14249, January 2025.
 URL https://doi.org/10.48550/arXiv.2501.14249.
Felipe Maia Polo, Lucas Weber, Leshem Choshen, Yuekai Sun, Gongjun Xu, and Mikhail
 Yurochkin. tinyBenchmarks: Evaluating LLMs with fewer examples. In Proceedings
 of the 41st international conference on machine learning, ICML’24. JMLR.org, 2024.
 Place: Vienna, Austria Number of pages: 24 tex.articleno: 1396.
Chris Potts. Reliable characterizations of NLP systems as a social responsibility. Keynote
 talk, ACL-IJCNLP, August 2021. URL https://youtu.be/t_A36DDcG_0?
 si=XK7V7zBf8p38B5PY.
Alec Radford, Jeffery Wu, Rewon Child, David Luan, Dario Amodei, and Ilya
 Sutskever. Language Models are Unsupervised Multitask Learners, Febru-
 ary 2019. URL https://cdn.openai.com/better-language-models/
 language_models_are_unsupervised_multitask_learners.pdf.
Inioluwa Deborah Raji, Emily Denton, Emily M. Bender, Alex Hanna, and Amanda-
 lynne Paullada. AI and the everything in the whole wide world benchmark. In Thirty-
 Fifth Conference on Neural Information Processing Systems Datasets and Bench-
 marks Track (Round 2), 2021. URL https://openreview.net/forum?id=
 j6NxpQbREA1.
M.D. Reckase. Multidimensional Item Response Theory. Springer New York, 2009. ISBN
 978-0-387-89975-6 978-0-387-89976-3. doi: 10.1007/978-0-387-89976-3. URL
 http://link.springer.com/10.1007/978-0-387-89976-3.
David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang,
 Julien Dirani, Julian Michael, and Samuel R. Bowman. GPQA: A graduate-level
 google-proof q&a benchmark. In First Conference on Language Modeling, 2024. URL
 https://openreview.net/forum?id=Ti67584b98.
Anka Reuel, Benjamin Bucknall, Stephen Casper, Timothy Fist, Lisa Soder, Onni Aarne,
 Lewis Hammond, Lujain Ibrahim, Alan Chan, Peter Wills, Markus Anderljung, Ben
 Garfinkel, Lennart Heim, Andrew Trask, Gabriel Mukobi, Rylan Schaeffer, Mauricio
 Baker, Sara Hooker, Irene Solaiman, Sasha Luccioni, Nitarshan Rajkumar, Nicolas
 Moës, Jeffrey Ladish, David Bau, Paul Bricman, Neel Guha, Jessica Newman, Yoshua
 Bengio, Tobin South, Alex Pentland, Sanmi Koyejo, Mykel Kochenderfer, and Robert
 Trager. Open problems in technical AI governance. Transactions on Machine Learning
 Research, 2025. ISSN 2835-8856. URL https://openreview.net/forum?
 id=1nO4qFMiS0. Survey Certification.
Yves Rosseel. Lavaan: An R package for structural equation modeling. Journal of
 Statistical Software, 48(2):1–36, 2012. doi: 10.18637/jss.v048.i02. URL https:
 //www.jstatsoft.org/index.php/jss/article/view/v048i02.
 61
REFERENCES
Yangjun Ruan, Chris J. Maddison, and Tatsunori Hashimoto. Observational scaling
 laws and the predictability of langauge model performance. In The Thirty-eighth An-
 nual Conference on Neural Information Processing Systems, 2024. URL https:
 //openreview.net/forum?id=On5WIN7xyD.
Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi. WinoGrande:
 An adversarial winograd schema challenge at scale. Communications of the ACM, 64
 (9):99–106, September 2021. ISSN 0001-0782, 1557-7317. doi: 10.1145/3474381.
 URL https://dl.acm.org/doi/10.1145/3474381.
Olawale Salaudeen, Anka Reuel, Ahmed Ahmed, Suhana Bedi, Zachary Robertson,
 Sudharsan Sundar, Ben Domingue, Angelina Wang, and Sanmi Koyejo. Measure-
 ment to meaning: A validity-centered framework for ai evaluation, 2025. URL
 https://arxiv.org/abs/2505.10573.
Rylan Schaeffer, Brando Miranda, and Sanmi Koyejo. Are emergent abilities of large
 language models a mirage? In A. Oh, T. Naumann, A. Globerson, K. Saenko,
 M. Hardt, and S. Levine (eds.), Advances in neural information processing sys-
 tems, volume 36, pp. 55565–55581. Curran Associates, Inc., 2023. URL https:
 //proceedings.neurips.cc/paper_files/paper/2023/file/
 adc98a266f45005c403b8311ca7e8bd7-Paper-Conference.pdf.
Mark A Schmuckler. What is ecological validity? a dimensional analysis. Infancy, 2(4):
 419–436, 2001.
W. J. Schneider and K. S. McGrew. The Cattell–Horn–Carroll theory of cognitive abil-
 ities. In D. P. Flanagan and E. M. McDonough (eds.), Contemporary Intellectual As-
 sessment: Theories, Tests, and Issues, pp. 73–163. The Guilford Press, 4 edition, 2018.
Gideon Schwarz. Estimating the Dimension of a Model. The Annals of Statis-
 tics, 6(2), March 1978. ISSN 0090-5364. doi: 10.1214/aos/1176344136. URL
 https://projecteuclid.org/journals/annals-of-statistics/
 volume-6/issue-2/Estimating-the-Dimension-of-a-Model/10.
 1214/aos/1176344136.full.
Dexin Shi, Alberto Maydeu-Olivares, and Yves Rosseel. Assessing Fit in Ordinal Factor
 Analysis Models: SRMR vs. RMSEA. Structural Equation Modeling: A Multidisci-
 plinary Journal, 27(1):1–15, January 2020. ISSN 1070-5511, 1532-8007. doi: 10.
 1080/10705511.2019.1611434. URL https://www.tandfonline.com/doi/
 full/10.1080/10705511.2019.1611434.
Leonard J Simms and David Watson. The construct validation approach to personality
 scale construction. Handbook of research methods in personality psychology, pp. 240–
 258, 2007.
Shivalika Singh, Yiyang Nan, Alex Wang, Daniel D’Souza, Sayash Kapoor, Ahmet
 Üstün, Sanmi Koyejo, Yuntian Deng, Shayne Longpre, Noah A. Smith, Beyza Er-
 mis, Marzieh Fadaee, and Sara Hooker. The leaderboard illusion, 2025. URL
 https://arxiv.org/abs/2504.20879.
 62
REFERENCES
Shaden Smith, Mostofa Patwary, Brandon Norick, Patrick LeGresley, Samyam Rajbhan-
 dari, Jared Casper, Zhun Liu, Shrimai Prabhumoye, George Zerveas, Vijay Korthikanti,
 Elton Zhang, Rewon Child, Reza Yazdani Aminabadi, Julie Bernauer, Xia Song, Mo-
 hammad Shoeybi, Yuxiong He, Michael Houston, Saurabh Tiwary, and Bryan Catan-
 zaro. Using DeepSpeed and Megatron to train Megatron-Turing NLG 530B, a large-
 scale generative language model, 2022. URL https://arxiv.org/abs/2201.
 11990.
C. Spearman. “General Intelligence,” Objectively Determined and Measured. The Amer-
 ican Journal of Psychology, 15(2):201, April 1904. ISSN 00029556. doi: 10.2307/
 1412107. URL https://www.jstor.org/stable/1412107?origin=
 crossref.
Zayne Rea Sprague, Xi Ye, Kaj Bostrom, Swarat Chaudhuri, and Greg Durrett. MuSR:
 Testing the limits of chain-of-thought with multistep soft reasoning. In The Twelfth
 International Conference on Learning Representations, 2024. URL https://
 openreview.net/forum?id=jenyYQzue1.
Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar
 Abid, Adam Fisch, Adam R. Brown, Adam Santoro, Aditya Gupta, Adrià Garriga-
 Alonso, Agnieszka Kluska, Aitor Lewkowycz, Akshat Agarwal, Alethea Power, Alex
 Ray, Alex Warstadt, Alexander W. Kocurek, Ali Safaya, Ali Tazarv, Alice Xiang,
 Alicia Parrish, Allen Nie, Aman Hussain, Amanda Askell, Amanda Dsouza, Am-
 brose Slone, Ameet Rahane, Anantharaman S. Iyer, Anders Johan Andreassen, An-
 drea Madotto, Andrea Santilli, Andreas Stuhlmüller, Andrew M. Dai, Andrew La, An-
 drew Kyle Lampinen, Andy Zou, Angela Jiang, Angelica Chen, Anh Vuong, Animesh
 Gupta, Anna Gottardi, Antonio Norelli, Anu Venkatesh, Arash Gholamidavoodi, Arfa
 Tabassum, Arul Menezes, Arun Kirubarajan, Asher Mullokandov, Ashish Sabharwal,
 Austin Herrick, Avia Efrat, Aykut Erdem, Ayla Karakaş, B. Ryan Roberts, Bao Sheng
 Loe, Barret Zoph, Bartłomiej Bojanowski, Batuhan Özyurt, Behnam Hedayatnia,
 Behnam Neyshabur, Benjamin Inden, Benno Stein, Berk Ekmekci, Bill Yuchen Lin,
 Blake Howald, Bryan Orinion, Cameron Diao, Cameron Dour, Catherine Stinson,
 Cedrick Argueta, Cesar Ferri, Chandan Singh, Charles Rathkopf, Chenlin Meng, Chitta
 Baral, Chiyu Wu, Chris Callison-Burch, Christopher Waites, Christian Voigt, Christo-
 pher D Manning, Christopher Potts, Cindy Ramirez, Clara E. Rivera, Clemencia Siro,
 Colin Raffel, Courtney Ashcraft, Cristina Garbacea, Damien Sileo, Dan Garrette, Dan
 Hendrycks, Dan Kilman, Dan Roth, C. Daniel Freeman, Daniel Khashabi, Daniel Levy,
 Daniel Moseguí González, Danielle Perszyk, Danny Hernandez, Danqi Chen, Daphne
 Ippolito, Dar Gilboa, David Dohan, David Drakard, David Jurgens, Debajyoti Datta,
 Deep Ganguli, Denis Emelin, Denis Kleyko, Deniz Yuret, Derek Chen, Derek Tam,
 Dieuwke Hupkes, Diganta Misra, Dilyar Buzan, Dimitri Coelho Mollo, Diyi Yang,
 Dong-Ho Lee, Dylan Schrader, Ekaterina Shutova, Ekin Dogus Cubuk, Elad Segal,
 Eleanor Hagerman, Elizabeth Barnes, Elizabeth Donoway, Ellie Pavlick, Emanuele
 Rodolà, Emma Lam, Eric Chu, Eric Tang, Erkut Erdem, Ernie Chang, Ethan A Chi,
 Ethan Dyer, Ethan Jerzak, Ethan Kim, Eunice Engefu Manyasi, Evgenii Zheltonozh-
 skii, Fanyue Xia, Fatemeh Siar, Fernando Martínez-Plumed, Francesca Happé, Fran-
 cois Chollet, Frieda Rong, Gaurav Mishra, Genta Indra Winata, Gerard de Melo, Ger-
 màn Kruszewski, Giambattista Parascandolo, Giorgio Mariani, Gloria Xinyue Wang,
 63
REFERENCES
 Gonzalo Jaimovitch-Lopez, Gregor Betz, Guy Gur-Ari, Hana Galijasevic, Hannah
 Kim, Hannah Rashkin, Hannaneh Hajishirzi, Harsh Mehta, Hayden Bogar, Henry Fran-
 cis Anthony Shevlin, Hinrich Schuetze, Hiromu Yakura, Hongming Zhang, Hugh Mee
 Wong, Ian Ng, Isaac Noble, Jaap Jumelet, Jack Geissinger, Jackson Kernion, Jacob
 Hilton, Jaehoon Lee, Jaime Fernández Fisac, James B Simon, James Koppel, James
 Zheng, James Zou, Jan Kocon, Jana Thompson, Janelle Wingfield, Jared Kaplan,
 Jarema Radom, Jascha Sohl-Dickstein, Jason Phang, Jason Wei, Jason Yosinski, Jeka-
 terina Novikova, Jelle Bosscher, Jennifer Marsh, Jeremy Kim, Jeroen Taal, Jesse Engel,
 Jesujoba Alabi, Jiacheng Xu, Jiaming Song, Jillian Tang, Joan Waweru, John Bur-
 den, John Miller, John U. Balis, Jonathan Batchelder, Jonathan Berant, Jörg Frohberg,
 Jos Rozen, Jose Hernandez-Orallo, Joseph Boudeman, Joseph Guerr, Joseph Jones,
 Joshua B. Tenenbaum, Joshua S. Rule, Joyce Chua, Kamil Kanclerz, Karen Livescu,
 Karl Krauth, Karthik Gopalakrishnan, Katerina Ignatyeva, Katja Markert, Kaustubh
 Dhole, Kevin Gimpel, Kevin Omondi, Kory Wallace Mathewson, Kristen Chiafullo,
 Ksenia Shkaruta, Kumar Shridhar, Kyle McDonell, Kyle Richardson, Laria Reynolds,
 Leo Gao, Li Zhang, Liam Dugan, Lianhui Qin, Lidia Contreras-Ochando, Louis-
 Philippe Morency, Luca Moschella, Lucas Lam, Lucy Noble, Ludwig Schmidt, Luheng
 He, Luis Oliveros-Colón, Luke Metz, Lütfi Kerem Senel, Maarten Bosma, Maarten
 Sap, Maartje Ter Hoeve, Maheen Farooqi, Manaal Faruqui, Mantas Mazeika, Marco
 Baturan, Marco Marelli, Marco Maru, Maria Jose Ramirez-Quintana, Marie Tolkiehn,
 Mario Giulianelli, Martha Lewis, Martin Potthast, Matthew L Leavitt, Matthias Ha-
 gen, Mátyás Schubert, Medina Orduna Baitemirova, Melody Arnaud, Melvin McEl-
 rath, Michael Andrew Yee, Michael Cohen, Michael Gu, Michael Ivanitskiy, Michael
 Starritt, Michael Strube, Michał Swedrowski, Michele Bevilacqua, Michihiro Ya-
 sunaga, Mihir Kale, Mike Cain, Mimee Xu, Mirac Suzgun, Mitch Walker, Mo Ti-
 wari, Mohit Bansal, Moin Aminnaseri, Mor Geva, Mozhdeh Gheini, Mukund Varma T,
 Nanyun Peng, Nathan Andrew Chi, Nayeon Lee, Neta Gur-Ari Krakover, Nicholas
 Cameron, Nicholas Roberts, Nick Doiron, Nicole Martinez, Nikita Nangia, Niklas
 Deckers, Niklas Muennighoff, Nitish Shirish Keskar, Niveditha S. Iyer, Noah Constant,
 Noah Fiedel, Nuan Wen, Oliver Zhang, Omar Agha, Omar Elbaghdadi, Omer Levy,
 Owain Evans, Pablo Antonio Moreno Casares, Parth Doshi, Pascale Fung, Paul Pu
 Liang, Paul Vicol, Pegah Alipoormolabashi, Peiyuan Liao, Percy Liang, Peter W
 Chang, Peter Eckersley, Phu Mon Htut, Pinyu Hwang, Piotr Miłkowski, Piyush Patil,
 Pouya Pezeshkpour, Priti Oli, Qiaozhu Mei, Qing Lyu, Qinlang Chen, Rabin Banjade,
 Rachel Etta Rudolph, Raefer Gabriel, Rahel Habacker, Ramon Risco, Raphaël Millière,
 Rhythm Garg, Richard Barnes, Rif A. Saurous, Riku Arakawa, Robbe Raymaekers,
 Robert Frank, Rohan Sikand, Roman Novak, Roman Sitelew, Ronan Le Bras, Rosanne
 Liu, Rowan Jacobs, Rui Zhang, Russ Salakhutdinov, Ryan Andrew Chi, Seungjae Ryan
 Lee, Ryan Stovall, Ryan Teehan, Rylan Yang, Sahib Singh, Saif M. Mohammad, Sa-
 jant Anand, Sam Dillavou, Sam Shleifer, Sam Wiseman, Samuel Gruetter, Samuel R.
 Bowman, Samuel Stern Schoenholz, Sanghyun Han, Sanjeev Kwatra, Sarah A. Rous,
 Sarik Ghazarian, Sayan Ghosh, Sean Casey, Sebastian Bischoff, Sebastian Gehrmann,
 Sebastian Schuster, Sepideh Sadeghi, Shadi Hamdan, Sharon Zhou, Shashank Srivas-
 tava, Sherry Shi, Shikhar Singh, Shima Asaadi, Shixiang Shane Gu, Shubh Pachchi-
 gar, Shubham Toshniwal, Shyam Upadhyay, Shyamolima Shammie Debnath, Siamak
 Shakeri, Simon Thormeyer, Simone Melzi, Siva Reddy, Sneha Priscilla Makini, Soo-
 64
REFERENCES
 Hwan Lee, Spencer Torene, Sriharsha Hatwar, Stanislas Dehaene, Stefan Divic, Ste-
 fano Ermon, Stella Biderman, Stephanie Lin, Stephen Prasad, Steven Piantadosi, Stu-
 art Shieber, Summer Misherghi, Svetlana Kiritchenko, Swaroop Mishra, Tal Linzen,
 Tal Schuster, Tao Li, Tao Yu, Tariq Ali, Tatsunori Hashimoto, Te-Lin Wu, Théo Des-
 bordes, Theodore Rothschild, Thomas Phan, Tianle Wang, Tiberius Nkinyili, Timo
 Schick, Timofei Kornev, Titus Tunduny, Tobias Gerstenberg, Trenton Chang, Trishala
 Neeraj, Tushar Khot, Tyler Shultz, Uri Shaham, Vedant Misra, Vera Demberg, Victoria
 Nyamai, Vikas Raunak, Vinay Venkatesh Ramasesh, vinay uday prabhu, Vishakh Pad-
 makumar, Vivek Srikumar, William Fedus, William Saunders, William Zhang, Wout
 Vossen, Xiang Ren, Xiaoyu Tong, Xinran Zhao, Xinyi Wu, Xudong Shen, Yadol-
 lah Yaghoobzadeh, Yair Lakretz, Yangqiu Song, Yasaman Bahri, Yejin Choi, Yichi
 Yang, Sophie Hao, Yifu Chen, Yonatan Belinkov, Yu Hou, Yufang Hou, Yuntao Bai,
 Zachary Seid, Zhuoye Zhao, Zijian Wang, Zijie J. Wang, Zirui Wang, and Ziyi Wu.
 Beyond the imitation game: Quantifying and extrapolating the capabilities of lan-
 guage models. Transactions on Machine Learning Research, 2023. ISSN 2835-8856.
 URL https://openreview.net/forum?id=uyTL5Bvosj. Featured Certifi-
 cation.
James H Steiger. Structural model evaluation and modification: An interval estimation
 approach. Multivariate behavioral research, 25(2):173–180, 1990.
Mirac Suzgun, Sebastian Gehrmann, Yonatan Belinkov, and Stuart M Shieber. Memory-
 augmented recurrent neural networks can learn generalized dyck languages. arXiv
 preprint arXiv:1911.03329, 2019.
Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay,
 Hyung Won Chung, Aakanksha Chowdhery, Quoc V. Le, Ed H. Chi, Denny Zhou,
 and Jason Wei. Challenging big-bench tasks and whether chain-of-thought can solve
 them. In ACL (Findings), pp. 13003–13051, 2023. URL https://doi.org/10.
 18653/v1/2023.findings-acl.824.
Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant. CommonsenseQA:
 A question answering challenge targeting commonsense knowledge. In Jill Burstein,
 Christy Doran, and Thamar Solorio (eds.), Proceedings of the 2019 conference of
 the north American chapter of the association for computational linguistics: Hu-
 man language technologies, volume 1 (long and short papers), pp. 4149–4158, Min-
 neapolis, Minnesota, June 2019. Association for Computational Linguistics. doi:
 10.18653/v1/N19-1421. URL https://aclanthology.org/N19-1421/.
Lisa H. Trahan, Karla K. Stuebing, Jack M. Fletcher, and Merrill Hiscock. The Flynn
 effect: A meta-analysis. Psychological Bulletin, 140(5):1332–1360, 2014. ISSN
 1939-1455, 0033-2909. doi: 10.1037/a0037173. URL http://doi.apa.org/
 getdoi.cfm?doi=10.1037/a0037173.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N
 Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is All you Need. Advances in
 Neural Information Processing Systems, 31, 2017.
 65
REFERENCES
Pablo Villalobos, Anson Ho, Jaime Sevilla, Tamay Besiroglu, Lennart Heim, and Marius
 Hobbhahn. Will we run out of data? Limits of LLM scaling based on human-generated
 data, 2024. URL https://arxiv.org/abs/2211.04325.
Anton Voronov, Lena Wolf, and Max Ryabinin. Mind your format: Towards consis-
 tent evaluation of in-context learning improvements. In Lun-Wei Ku, Andre Mar-
 tins, and Vivek Srikumar (eds.), Findings of the Association for Computational Lin-
 guistics: ACL 2024, pp. 6287–6310, Bangkok, Thailand, August 2024. Associa-
 tion for Computational Linguistics. doi: 10.18653/v1/2024.findings-acl.375. URL
 https://aclanthology.org/2024.findings-acl.375/.
Hanna Wallach, Meera Desai, Nicholas Pangakis, A. Feder Cooper, Angelina Wang,
 Solon Barocas, Alexandra Chouldechova, Chad Atalla, Su Lin Blodgett, Emily Corvi,
 P. Alex Dow, Jean Garcia-Gathright, Alexandra Olteanu, Stefanie Reed, Emily Sheng,
 Dan Vann, Jennifer Wortman Vaughan, Matthew Vogel, Hannah Washington, and Abi-
 gail Z. Jacobs. Evaluating generative AI systems is a social science measurement chal-
 lenge. In NeurIPS 2024 Workshop on Evaluating Evaluations (EvalEval), 2024. URL
 https://arxiv.org/pdf/2411.10939v1.
Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael, Felix
 Hill, Omer Levy, and Samuel Bowman. Superglue: A stickier benchmark for general-
 purpose language understanding systems. Advances in neural information processing
 systems, 32, 2019.
Xiting Wang, Liming Jiang, José Hernández-Orallo, Luning Sun, David Stillwell, Fang
 Luo, and Xing Xie. Evaluating general-purpose AI with psychometrics. CoRR,
 abs/2310.16379, 2023. URL https://doi.org/10.48550/arXiv.2310.
 16379.
Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo,
 Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al. MMLU-Pro: A more robust
 and challenging multi-task language understanding benchmark. Advances in Neural
 Information Processing Systems, 37:95266–95290, 2025.
Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud,
 Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tat-
 sunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus. Emer-
 gent abilities of large language models. Transactions on Machine Learning Re-
 search, 2022. ISSN 2835-8856. URL https://openreview.net/forum?id=
 yzkSU5zdwD.
Jason Weston, Antoine Bordes, Sumit Chopra, Alexander M Rush, Bart Van Merriënboer,
 Armand Joulin, and Tomas Mikolov. Towards AI-complete question answering: A set
 of prerequisite toy tasks. arXiv preprint arXiv:1502.05698, 2015.
Shuo Yang, Wei-Lin Chiang, Lianmin Zheng, Joseph E. Gonzalez, and Ion Stoica. Re-
 thinking Benchmark and Contamination for Language Models with Rephrased Sam-
 ples, 2023. URL https://arxiv.org/abs/2311.04850. Version Number:
 2.
 66
REFERENCES
Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. HellaSwag:
 Can a machine really finish your sentence? In Anna Korhonen, David Traum, and
 Lluís Màrquez (eds.), Proceedings of the 57th Annual Meeting of the Association
 for Computational Linguistics, pp. 4791–4800, Florence, Italy, July 2019. Associ-
 ation for Computational Linguistics. doi: 10.18653/v1/P19-1472. URL https:
 //aclanthology.org/P19-1472/.
Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan,
 Denny Zhou, and Le Hou. Instruction-following evaluation for large language models,
 2023a. URL https://arxiv.org/abs/2311.07911.
Kun Zhou, Yutao Zhu, Zhipeng Chen, Wentong Chen, Wayne Xin Zhao, Xu Chen, Yankai
 Lin, Ji-Rong Wen, and Jiawei Han. Don’t Make Your LLM an Evaluation Benchmark
 Cheater, 2023b. URL http://arxiv.org/abs/2311.01964.
Lexin Zhou, Lorenzo Pacchiardi, Fernando Martínez-Plumed, Katherine M. Collins,
 Yael Moros-Daval, Seraphina Zhang, Qinlin Zhao, Yitian Huang, Luning Sun,
 Jonathan E. Prunty, Zongqian Li, Pablo Sánchez-García, Kexin Jiang Chen, Pablo
 A. M. Casares, Jiyun Zu, John Burden, Behzad Mehrbakhsh, David Stillwell, Manuel
 Cebrián, Jindong Wang, Peter Henderson, Sherry Tongshuang Wu, Patrick C. Kyl-
 lonen, Lucy Cheke, Xing Xie, and José Hernández-Orallo. General scales unlock
 AI evaluation with explanatory and predictive power. CoRR, abs/2503.06378, March
 2025. URL https://doi.org/10.48550/arXiv.2503.06378. tex.cdate:
 1740787200000 tex.publtype: informal.
 67
APPENDIX
A List of mentioned benchmarks
In some places in the text, it aids readability to enumerate benchmark names without giv-
ing their citations. We style all benchmark names in monospace to make their mentions
visually apparent. Table 4 gives a list of all benchmarks mentioned in this paper along
with their descriptions and citations.
 Benchmark Dataset description Citation
 GSM8K Grade school-level arithmetic word Cobbe et al. (2021)
 problems.
 MATH Challenging high school-level compe- Hendrycks et al. (2021)
 tition mathematics problems.
 FrontierMath Unpublished, expert-level research Glazer et al. (2024)
 mathematics problems.
 GPQA “Google-Proof Q&A.” PhD-level biol- Rein et al. (2024)
 ogy, physics, and chemistry multiple
 choice questions.
 MMLU-Pro Broad knowledge and reasoning bench- Wang et al. (2025)
 mark with questions spanning 14 aca-
 demic subjects.
 Commonsense QA Crowd-sourced multiple choice ques- Talmor et al. (2019)
 tions targeting simple concepts.
 Winogrande Adversarially-sourced ambiguous pro- Sakaguchi et al. (2021)
 noun resolution problems.
 HumanEval Docstring descriptions for generat- Chen et al. (2021)
 ing functionally-correct software pro-
 grams.
 SWE-Bench GitHub issues requiring changes to Jimenez et al. (2024)
 python codebases.
 SuperGLUE General-purpose language understand- Wang et al. (2019)
 ing sourced from 8 NLP tasks.
 Humanity’s Last Exam Difficult multi-modal problems across Phan et al. (2025)
 many academic subjects.
 AIME 2024 Questions from American invitational (Mathematical Associa-
 mathematics competiton. tion of America, 2024)
 MathBench Broadly scoped mathematics questions (Liu et al., 2024)
 in English and Chinese.
 HELM “Holistic Evaluation of Language Liang et al. (2023)
 Models.”
 BIG-bench “Beyond the Imitation Game.” Crowd- Srivastava et al. (2023)
 sourced collection of 204 distinct tasks.
 TruthfulQA Q&A targeting common misconcep- Lin et al. (2022)
 tions and falsehoods.
 BBQ “Bias Benchmark for QA.” Questions Parrish et al. (2022)
 where one of nine social biases over-
 ride the correct choice.
 HellaSwag Sentence completions testing common Zellers et al. (2019)
 natural language inference.
 WikiFact Wikipedia content to test factual accu- Goodrich et al. (2019)
 racy and relation extraction.
 NaturalQuestions Q&A adapted from Google search Kwiatkowski et al.
 queries. (2019)
 68
APPENDIX
 XSUM News summarisation using online arti- Narayan et al. (2018)
 cles from the BBC.
 OpenbookQA Q&A using elementary science facts. Mihaylov et al. (2018)
 bAbI Short stories about characters, followed Weston et al. (2015)
 by reading comprehension questions.
 Dyck Completing Dyck sentences: prop- Suzgun et al. (2019)
 erly nested sequences of characters
 {}[]().
 BBH “BIG-Bench Hard.” 23 difficult tasks Suzgun et al. (2023)
 selected from BIG-bench.
 IFEval “Instruction-Following Evaluation.” Zhou et al. (2023a)
 Prompts with formatting requirements,
 word length, and other verifiable
 instructions.
 MuSR “Multistep Soft Reasoning.” ~1, 000- Sprague et al. (2024)
 word passages, like murder mysteries,
 testing reading comprehension.
 Table 4: All mentioned benchmark datasets, with citations.
 69
APPENDIX
B Default mathematical notation
We utilise the following mathematical notation throughout this work. This table of nota-
tion is copied from the ICLR 2024 submission guidelines, and appears originally in the
textbook Deep Learning (Goodfellow et al., 2016), available at https://github.
com/goodfeli/dlbook_notation/.
 Numbers and Arrays
 a A scalar (integer or real)
 a A vector
 A A matrix
 A A tensor
 In Identity matrix with n rows and n columns
 I Identity matrix with dimensionality implied by
 context
 e(i) Standard basis vector [0, . . . , 0, 1, 0, . . . , 0] with a
 1 at position i
 diag(a) A square, diagonal matrix with diagonal entries
 given by a
 a A scalar random variable
 a A vector-valued random variable
 A A matrix-valued random variable
 Sets and Graphs
 A A set
 R The set of real numbers
 {0, 1} The set containing 0 and 1
 {0, 1, . . . , n} The set of all integers between 0 and n
 [a, b] The real interval including a and b
 (a, b] The real interval excluding a but including b
 A\B Set subtraction, i.e., the set containing the ele-
 ments of A that are not in B
 G A graph
 P aG (xi ) The parents of xi in G
 Indexing
 70
APPENDIX
ai Element i of vector a, with indexing starting at 1
a−i All elements of vector a except for element i
Ai,j Element i, j of matrix A
Ai,: Row i of matrix A
A:,i Column i of matrix A
Ai,j,k Element (i, j, k) of a 3-D tensor A
A:,:,i 2-D slice of a 3-D tensor
ai Element i of the random vector a
 Calculus
dy
 Derivative of y with respect to x
dx
∂y
 Partial derivative of y with respect to x
∂x
∇x y Gradient of y with respect to x
∇X y Matrix derivatives of y with respect to X
∇X y Tensor containing derivatives of y with respect to
 X
∂f
 Jacobian matrix J ∈ Rm×n of f : Rn → Rm
∂x
∇2x f (x) or H(f )(x)The Hessian matrix of f at input point x
Z
 f (x)dx Definite integral over the entire domain of x
Z
 f (x)dx Definite integral with respect to x over the set S
 S
 Probability and Information Theory
 71
APPENDIX
P (a) A probability distribution over a discrete variable
p(a) A probability distribution over a continuous vari-
 able, or over a variable whose type has not been
 specified
a∼P Random variable a has distribution P
Ex∼P [f (x)] or Ef (x)Expectation of f (x) with respect to P (x)
Var(f (x)) Variance of f (x) under P (x)
Cov(f (x), g(x)) Covariance of f (x) and g(x) under P (x)
H(x) Shannon entropy of the random variable x
DKL (P ∥Q) Kullback-Leibler divergence of P and Q
N (x; µ, Σ) Gaussian distribution over x with mean µ and co-
 variance Σ
 Functions
f :A→B The function f with domain A and range B
f ◦g Composition of the functions f and g
f (x; θ) A function of x parametrized by θ. (Sometimes
 we write f (x) and omit the argument θ to lighten
 notation)
log x Natural logarithm of x
 1
σ(x) Logistic sigmoid,
 1 + exp(−x)
ζ(x) Softplus, log(1 + exp(x))
||x||p Lp norm of x
||x|| L2 norm of x
x+ Positive part of x, i.e., max(0, x)
1condition is 1 if the condition is true, 0 otherwise
 72
APPENDIX
C BIG-Bench Hard task descriptions
In the following list, we provide the task descriptions as given in the original BIG-Bench
Hard paper by Suzgun et al. (2023). Our list below is a subset of the list in Appendix A
of Suzgun et al. (2023). Each example is the first example in the OpenLLM Leaderboard
dataset for that subtask.
 1. Boolean Expressions: Evaluate the truth value of a random Boolean expression
 consisting of Boolean constants (True, False) and basic Boolean operators (and,
 or, and not).
 Example: Evaluate the result of a random Boolean expression.
 Q: not ( ( not not True ) ) is
 A: False
 2. Causal Judgement: Given a short story (involving moral, intentional, or counter-
 factual analysis), determine how a typical person would answer a causal question
 about the story.
 Example: Answer questions about causal attribution.
 Q: How would a typical person answer each of the following questions
 about causation?
 Frank T., had an ongoing dispute with his neighbor over a stretch of land
 and one day decided to shoot his neighbor in the body. Frank T. had
 no experience with guns, his hand slipped on the barrel of the gun, and
 the shot went wild. Nonetheless, the bullet bounced off a large boulder
 several feet away and hit the neighbor’s body, causing significant injury.
 Did Frank T. intentionally shoot his neighbor in the body?
 Options:
 - Yes
 - No
 A: No
 3. Date Understanding: Given a small set of sentences about a particular date, answer
 the provided question (e.g., “The concert was scheduled to be on 06/01/1943, but
 was delayed by one day to today. What is the date yesterday in MM/DD/YYYY?”).
 Example: Infer the date from context.
 Q: Today is Christmas Eve of 1937. What is the date 10 days ago in
 MM/DD/YYYY?
 Options:
 73
APPENDIX
 (A) 12/14/2026
 (B) 12/14/1950
 (C) 12/14/2007
 (D) 12/14/1937
 (E) 07/14/1938
 (F) 12/14/1988
 A: (D)
 4. Disambiguation QA: Given a sentence with an “ambiguous” pronoun, either deter-
 mine whether the sentence is inherently ambiguous (i.e., the thing that the pronoun
 refers to cannot be inferred by given information) or, if the pronoun can be im-
 plicitly deduced, state the antecedent of the pronoun (i.e., the noun to which the
 pronoun refers).
 Example: Clarify the meaning of sentences with ambiguous pronouns.
 Q: In the following sentences, explain the antecedent of the pronoun
 (which thing the pronoun refers to), or state that it is ambiguous.
 Sentence: The chief told the counselor that they took the day off.
 Options:
 (A) The chief took the day off
 (B) The counselor took the day off
 (C) Ambiguous
 A: (A)
 5. Formal Fallacies: Given a context involving a set of statements (generated by
 one of the argument schemes), determine whether an argument—presented infor-
 mally—can be logically deduced from the provided context.
 Example: Distinguish deductively valid arguments from formal falla-
 cies.
 Q: “It is not always easy to see who is related to whom – and in which
 ways. The following argument pertains to this question: To begin with,
 Lesley is a close friend of Fernando. Moreover, being a close friend
 of Fernando or a schoolmate of Lowell is sufficient for being a great-
 grandfather of Leroy. It follows that Lesley is a great-grandfather of
 Leroy.”
 Is the argument, given the explicitly stated premises, deductively valid
 or invalid?
 Options:
 - valid
 - invalid
 74
APPENDIX
 A: valid
 6. Geometric Shapes: Given a full SVG path element containing multiple commands,
 determine the geometric shape that would be generated if one were to execute the
 full path element.
 Example: Name geometric shapes from their SVG paths.
 Q: This SVG path element <path d=“M 31.00,73.00 L 32.00,59.00 L
 44.00,50.00 L 49.00,41.00 L 64.00,37.00 L 71.00,55.00 L 64.00,76.00 L
 52.00,61.00 L 31.00,73.00”/> draws a
 Options:
 (A) circle
 (B) heptagon
 (C) hexagon
 (D) kite
 (E) line
 (F) octagon
 (G) pentagon
 (H) rectangle
 (I) sector
 (J) triangle
 A: (F)
 7. Hyperbaton: Given two English-language sentences, determine the one with the
 correct adjective order.
 Example: Order adjectives correctly in English sentences.
 Q: Which sentence has the correct adjective order:
 Options:
 (A) rubber terrible ship
 (B) terrible rubber ship
 A: (B)
 8. Logical Deduction: Deduce the order of a sequence of objects based on the clues
 and information about their spacial relationships and placements.
 Example: A logical deduction task which requires deducing the order of
 a sequence of objects.
 Q: The following paragraphs each describe a set of three objects arranged
 in a fixed order. The statements are logically consistent within each para-
 graph. In a golf tournament, there were three golfers: Amy, Eli, and Eve.
 Eve finished above Amy. Eli finished below Amy.
 75
APPENDIX
 Options:
 (A) Amy finished last
 (B) Eli finished last
 (C) Eve finished last
 A: (B)
 9. Movie Recommendation: Given a list of movies a user might have watched and
 liked, recommend a new, relevant movie to the user out of the four potential choices
 user might have.
 Example: Recommend movies similar to the given list of movies.
 Q: Find a movie similar to Star Wars Episode IV - A New Hope, Indiana
 Jones and the Last Crusade, Star Wars Episode V - The Empire Strikes
 Back, The Big Lebowski:
 Options:
 (A) Tetsuo
 (B) the Ironman
 (C) The Princess Bride
 (D) The Barkley Marathons The Race That Eats Its Young
 (E) Bug
 A: (C)
 10. Navigate: Given a series of navigation steps to an agent, determine whether the
 agent would end up back at its initial starting point.
 Example: Given a series of navigation instructions, determine whether
 one would end up back at the starting point.
 Q: If you follow these instructions, do you return to the starting point?
 Turn left. Turn around. Turn left. Take 7 steps. Take 2 steps. Take 4
 steps. Take 8 steps.
 Options:
 - Yes
 - No
 A: No
 11. Object Counting: Given a collection of possessions that a person has along with
 their quantities (e.g., three pianos, two strawberries, one table, and two watermel-
 ons), determine the number of a certain object/item class (e.g., fruits).
 Example: Questions that involve enumerating objects and asking the
 model to count them.
 76
APPENDIX
 Q: I have a blackberry, a clarinet, a nectarine, a plum, a strawberry, a
 banana, a flute, an orange, and a violin. How many fruits do I have?
 A: 6
 12. Penguins in a Table: Given a unique table of penguins (and sometimes some new
 information), answer a question about the attributes of the penguins.
 Example: Answer questions about a table of penguins and their at-
 tributes.
 Q: Here is a table where the first line is a header and each subsequent
 line is a penguin: name, age, height (cm), weight (kg) Louis, 7, 50, 11
 Bernard, 5, 80, 13 Vincent, 9, 60, 11 Gwen, 8, 70, 15 For example: the
 age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is
 80 cm. We now add a penguin to the table:
 James, 12, 90, 12
 How many penguins are less than 8 years old?
 Options:
 (A) 1
 (B) 2
 (C) 3
 (D) 4
 (E) 5
 A: (B)
 13. Reasoning about Colored Objects: Given a context, answer a simple question
 about the color of an object on a surface.
 Example: Answer extremely simple questions about the colors of ob-
 jects on a surface.
 Q: On the nightstand, there is a red pencil, a purple mug, a burgundy
 keychain, a fuchsia teddy bear, a black plate, and a blue stress ball. What
 color is the stress ball?
 Options:
 (A) red
 (B) orange
 (C) yellow
 (D) green
 (E) blue
 (F) brown
 (G) magenta
 (H) fuchsia
 77
APPENDIX
 (I) mauve
 (J) teal
 (K) turquoise
 (L) burgundy
 (M) silver
 (N) gold
 (O) black
 (P) grey
 (Q) purple
 (R) pink
 A: (E)
 14. Ruin Names: Given an artist, band, or movie name, identify a one-character edit to
 the name that changes the meaning of the input and makes it humorous.
 Example: Select the humorous edit that ‘ruins’ the input movie or mu-
 sical artist name.
 Q: Which of the following is a humorous edit of this artist or movie
 name: ‘whitesnake’?
 Options:
 (A) whitesnape
 (B) whitesnapke
 (C) whitesnuake
 (D) mwhitesnake
 A: (A)
 15. Snarks: Given two nearly-identical sentences, determine which one is sarcastic.
 Example: Determine which of two sentences is sarcastic.
 According to Cambridge University Dictionary, sarcasm is “the use of
 remarks that clearly mean the opposite of what they say, made in or-
 der to hurt someone’s feelings or to criticize something in a humorous
 way.” Sarcastic sentences often contain satirical or ironic utterances, hy-
 perboles, ambivalent or witty remarks.
 Q: Which statement is sarcastic?
 Options:
 (A) Yes, because having interests and actively researching them is a huge
 waste
 (B) Yes, because having interests and actively researching them is a huge
 deal
 A: (A)
 78
APPENDIX
 16. Sports Understanding: Determine whether a factitious sentence related to sports
 is plausible.
 Example: Determine whether an artificially constructed sentence relat-
 ing to sports is plausible or not.
 Q: Is the following sentence plausible? “Bam Adebayo scored a reverse
 layup in the Western Conference Finals.”
 A: yes
 17. Temporal Sequences: Given a series of events and activities a person has com-
 pleted in the course of a day, determine what time, during the day, they might have
 been free to perform another activity.
 Example: Task description: Answer questions about which times certain
 events could have occurred.
 Q: Today, Emily went to the museum. Between what times could they
 have gone?
 We know that:
 Emily woke up at 1pm.
 Elizabeth saw Emily reading at the library from 2pm to 4pm.
 Jessica saw Emily watching a movie at the theater from 4pm to 5pm.
 Leslie saw Emily waiting at the airport from 5pm to 6pm.
 William saw Emily buying clothes at the mall from 6pm to 7pm.
 The museum was closed after 7pm.
 Between what times could Emily have gone to the museum?
 Options:
 (A) 1pm to 2pm
 (B) 6pm to 7pm
 (C) 5pm to 6pm
 (D) 2pm to 4pm
 A: (A)
 18. Tracking Shuffled Objects: Given the initial positions of a set of objects and a
 series of transformations (namely, pairwise swaps) applied to them, determine the
 final positions of the objects.
 Example: A task requiring determining the final positions of a set of
 objects given their initial positions and a description of a sequence of
 swaps.
 Q: Alice, Bob, and Claire are playing a game. At the start of the game,
 they are each holding a ball: Alice has a yellow ball, Bob has a blue ball,
 and Claire has a pink ball.
 79
APPENDIX
 As the game progresses, pairs of players trade balls. First, Claire and
 Alice swap balls. Then, Alice and Bob swap balls. Finally, Claire and
 Bob swap balls. At the end of the game, Bob has the
 Options:
 (A) yellow ball
 (B) blue ball
 (C) pink ball
 A: (A)
 19. Web of Lies: Evaluate the truth value of a random Boolean function expressed as a
 natural-language word problem.
 Example: Evaluate a random boolean function expressed as a word
 problem.
 Q: Question: Fidel tells the truth. Jerry says Fidel tells the truth. Vina
 says Jerry tells the truth. Millicent says Vina lies. Raymond says Milli-
 cent lies. Does Raymond tell the truth?
 A: Yes
 80
APPENDIX
D Transformed matrix derivation
Beginning with
 1 − ci
 Bi,: = ci +
 1 + exp[−αi (Li,: [wn log n] + Ei,: − βi )]
 ′
we set Bi,: = Li,: [wn log n] + Ei,: and solve for this quantity:
 1 − ci
 Bi,: = ci + ′
 
 1 + exp − αi (Bi,: − βi )
 1 − ci
 Bi,: − ci = ′
 
 1 + exp − αi (Bi,: − βi )
 ′
  1 − ci
 1 + exp − αi (Bi,: − βi ) =
 Bi,: − ci
 ′ 1 − ci
 e−αi (Bi,: −βi ) = −1
 Bi,: − ci
  
 ′ 1 − ci
 −αi (Bi,: − βi ) = log −1
 Bi,: − ci
  
 ′ 1 1 − ci
 Bi,: − βi = − log −1
 αi Bi,: − ci
  
 ′ 1 1 − ci
 Bi,: = βi − log −1
 αi Bi,: − ci
  
 ′ 1 1 − ci Bi,: − ci
 Bi,: = βi − log −
 αi Bi,: − ci Bi,: − ci
  
 ′ 1 1 − ci − (Bi,: − ci )
 Bi,: = βi − log
 αi Bi,: − ci
  
 ′ 1 1 − Bi,:
 Bi,: = βi − log
 αi Bi,: − ci
  
 ′ 1 Bi,: − ci
 Bi,: = βi + log
 αi 1 − Bi,:
This equivalence means modelling something like the odds-ratio of expected success on
individual subtask questions instead of the average score itself using a logistic response.
 81
APPENDIX
E Parameter scaling laws for all BBH subtasks
Figure 13 shows the result of fitting logistic scaling law model Equation (8) for all p = 19
BBH subtasks in my dataset.
 82
APPENDIX
Figure 13: Raw BBH scores against log-parameter size. The red line represents a
logistic fit using the functional form of Equation (8). R2 values range from 0.12 (Web of
lies) to 0.52 (Ruin names).
 83
