---
title: Characterizing Overconfident Failure in LLM-Based Code Generation (full text)
id: characterizing-overconfident-failure-in-llm-based-code-generation-full-text
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
created: '2026-11-09T23:10:53.664412Z'
updated: '2026-11-09T23:27:44.665639Z'
source: https://arxiv.org/pdf/2610.11300
status: review
type: note
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv 2610.11300, Rathnasuriya and Yang, 8 Oct 2026). Four 7-8B
  instruct code LLMs (CodeLlama, DeepSeek-Coder, Qwen2.5-Coder, OpenCoder) on HumanEval+,
  MBPP+, BigCodeBench with test-suite labels. Sec 4 Table 3: 17 generation-stage plus
  6 prefill-stage token/sampling uncertainty metrics, best AUC 0.598-0.696, none above
  0.70. Sec 5.5: base vs instruct on OpenCoder and DeepSeek-Coder (MBPP+), instruction
  tuning raises certainty on failures without reliable discrimination gain. Sec 6:
  Platt/isotonic calibration cuts Brier but BSS near 0 (Table 5); prompted abstention
  fails. Sec 7: hidden-state effective rank differs pass vs fail, exploratory only,
  no trained probe, no verbalized confidence. CLOSE occupant for L1/L4 token-level
  overconfidence; partial for L2 base-vs-instruct; does not occupy probe-vs-verbal.'
---

Characterizing Overconfident Failure in LLM-Based Code
Generation

arXiv:2610.11300v1 [cs.SE] 8 Oct 2026

RAVISHKA RATHNASURIYA, University of Texas at Dallas, USA
WEI YANG, Fudan University, China
Large language models (LLMs) are increasingly used for automated code generation, but generated programs
can appear syntactically plausible while still failing execution-based correctness checks. Existing validation
methods, such as testing and program analysis, remain essential but are often incomplete, costly, or applied
only after generation. Model-derived uncertainty is therefore a natural early reliability signal.
This paper studies the dilemma of overconfidence in code LLMs where incorrect programs are often
generated with token-level confidence comparable to correct programs. We study this dilemma across four
open-source code models and three execution-based benchmarks. Our analysis begins by investigating whether
existing uncertainty metrics provide reliable proxies for execution correctness in code generation. We then
characterize overconfidence at both global and local token levels, asking whether incorrect programs remain
indistinguishable from correct ones under confidence and entropy summaries, including selective generation
and the limits of instruction tuning. Finally, we evaluate whether common mitigation strategies reduce this
failure mode, and we examine latent representations as exploratory evidence for future reliability mechanisms.
Our study yields four findings. First, existing uncertainty signals provide only partial and model-dependent
evidence of execution failure. Second, overconfidence persists at both program and token levels, and uncertaintybased selection does not consistently improve accepted-set accuracy. Third, instruction tuning can increase
certainty on failing generations without consistently improving correctness discrimination. Fourth, common
mitigation techniques improve specific aspects of reliability but do not reliably resolve overconfident failure. Our exploratory latent analysis suggests that hidden representations may encode correctness-related
signals that output confidence does not expose. Together, these findings identify overconfident failure as a
software-engineering reliability problem and offer a practical path toward building more reliable LLM-driven
code-generation systems.

1

Introduction

Large language models (LLMs) have become increasingly effective at code generation, synthesizing implementations from natural-language specifications, programming tasks, and partial code
contexts [1–5]. They are now integrated into software development workflows to assist with implementation, debugging, testing, and repair [6–9]. However, generated code is not self-validating.
A program may be syntactically valid, idiomatic, and plausible while still violating the intended
specification, especially on edge cases revealed only through execution. Thus, a central reliability
challenge for LLM-based software engineering is not only whether a model can generate code, but
whether a system can determine when generated code should be trusted.
Existing validation approaches primarily rely on execution-based evaluation [10–13] or program
analysis [14–16]. These techniques are essential, but they do not fully solve the deployment-time
reliability problem. Execution requires tests, input generators, or behavioral oracles, which may be
incomplete, expensive, or unavailable for each generated candidate. Program analysis can identify
specific defect classes, but it is often conservative, property-specific, and does not generally estimate
whether an arbitrary generated program satisfies its specification. Moreover, both execution and
analysis are typically applied after generation. This limits their ability to provide lightweight,
model-intrinsic reliability signals during interactive code generation.
A natural alternative is an uncertainty-aware code-generation system. In an ideal setting, the
system would know whether a generated program generalizes to unseen tests or real user inputs.
Authors’ Contact Information: Ravishka Rathnasuriya, ravishka.rathnasuriya@utdallas.edu, University of Texas at Dallas,
Richardson, USA; Wei Yang, yang_wei@fudan.edu.cn, Institute of Systems for Advanced Computing, Fudan University,
Shanghai, China.

2

Ravishka Rathnasuriya and Wei Yang

Such a generalizability oracle is unavailable in practice, because functional correctness can only be
established through validation against a specification, tests, or downstream behavior. Therefore
practical systems must rely on proxies. The broader machine-learning literature operationalizes this
proxy through uncertainty metrics derived from predictive distributions, confidence scores, entropy,
margins, calibration methods, and related quantities. Such metrics have been extensively studied
in classification tasks [17–27] and more recently in natural language generation (NLG) [28–33],
where they are used as proxies for output correctness, factuality, or risk. These estimates also
support selective abstention [34–36], where high-risk outputs are withheld or routed to additional
validation.
However, uncertainty is less directly related to correctness in code generation than in classification or open-ended NLG. In classification, uncertainty is defined over the label distribution,
and evaluation is performed on the predicted label. In open-ended NLG, uncertainty is commonly
estimated over the generated response and evaluated against response-level properties such as correctness or factuality. In code generation, model probabilities are assigned during token generation,
whereas correctness is determined by the execution behavior of the completed program. Therefore,
a generated program can have high token likelihood and still fail to satisfy its specification. Thus,
token- and sequence-level uncertainty are only proxies for execution correctness.
Using token- and sequence-level uncertainty as proxies for execution correctness creates a
dilemma of overconfidence in code generation. A generated program may receive high model
confidence and still fail execution-based evaluation. This mismatch is consistent with how code
LLMs are trained and evaluated. First, autoregressive training optimizes next-token prediction rather
than whether model confidence reflects execution correctness. Second, standard code-generation
evaluation measures generation success rather than the reliability of model confidence. Pass@1 and
pass@k measure [10–13] whether generated programs pass the evaluation tests, whereas binary
grading gives no credit to abstention [37]. Therefore, such evaluation does not assess whether
failing generations receive lower confidence than passing ones. Testing and program analysis
provide evidence more directly tied to execution correctness, but they require external validation
and may be costly or incomplete. Therefore, model-derived uncertainty remains attractive as an
early reliability signal, despite the possibility of overconfident failures.
There is growing research interest in using uncertainty to support reliable code generation. Existing studies pursue three main directions. First, they evaluate uncertainty estimators as predictors
of code correctness [33, 38]. Second, they calibrate confidence against observed correctness or use
uncertainty to support abstention and other reliability decisions [39–43]. Third, recent studies
examine how uncertainty behaves when it is used to guide candidate selection, correction, or
other generation-time decisions [44, 45]. These studies show that uncertainty can provide useful
information about correctness, but their evaluations mainly measure estimator performance or the
effectiveness of an uncertainty-guided decision rule. However, important questions remain about
the reliability of uncertainty as a proxy for execution correctness. Prior studies demonstrate that
uncertainty can be informative, but they do not fully establish the extent to which it remains reliable
when passing and failing generations receive similar uncertainty scores. It also remains unclear
where this mismatch arises during generation, under which conditions it persists, and whether and
to what extent common mitigation strategies can address it. Addressing these questions requires a
systematic characterization of the reliability limits of model-derived uncertainty in code generation.
To characterize the reliability limits of model-derived uncertainty, we first conduct a preliminary
study of existing uncertainty measures (Section 4). Across 17 generation-stage metrics and six
prefill-stage metrics, no measure provides stable failure ranking across models and benchmarks. We
then examine overconfidence through token confidence and predictive entropy at both program and

Characterizing Overconfident Failure in LLM-Based Code Generation

3

token levels (Section 5). Failing programs often remain highly certain, including within their leastconfident token regions. This misalignment affects selective generation where reducing coverage
does not consistently increase selective accuracy and can decrease it when failures occupy highcertainty regions. Furthermore, instruction tuning can also increase certainty on failing generations
without a corresponding improvement in correctness discrimination. These findings show that
overconfidence is a distinct reliability problem where improvements in generation accuracy do not
necessarily improve the model’s ability to identify which generations are likely correct.
Finally, we evaluate whether common mitigation techniques reduce overconfident failure (Section 6). Post-hoc calibration substantially improves probability alignment, but calibrated scores
provide little predictive skill beyond the benchmark pass rate. Repeated sampling improves recovery
at small budgets, but its improvements diminish and a persistent set of tasks remains unsolved.
Moreover, explicit abstention prompting likewise does not reliably induce deferral on incorrect
generations. As an exploratory analysis, we find systematic pass–fail differences in latent-state
geometry that are not reflected in output-token confidence. These results show that improving
generation success or confidence calibration does not necessarily eliminate overconfident failure.
This paper makes the following contributions:
• We formulate the dilemma of overconfidence in code LLMs as a barrier to practical uncertaintyaware code generation.
• We show that existing uncertainty signals provide only partial and model-dependent evidence of execution failure across both prefill and generation stages.
• We characterize overconfidence at program and token levels, and show that it can persist
under selective generation and after instruction tuning.
• We evaluate post-hoc calibration, repeated sampling, and explicit abstention, showing that
none reliably resolves overconfident failure despite improving specific aspects of reliability.
• We provide exploratory evidence that latent representations contain correctness-related
structure not reflected in output uncertainty, motivating representation-aware reliability
mechanisms.
2

Problem Setup and Scope

This section formalizes code generation as a selective decision problem and introduces the uncertaintyaware system view that motivates our study. We then define the sources of uncertainty signals and
formulate overconfident failure as the central reliability problem.
2.1

Code Generation as a Selective Decision Problem

Given a prompt 𝑥, a code-generation model 𝑀 produces a candidate program 𝑦. A task-specific test
suite evaluates 𝑦, yielding an execution outcome 𝑍 (𝑥, 𝑦) ∈ {pass, fail}. We use this outcome as the
operational correctness signal.
Standard code-generation evaluation measures whether a model can generate correct solutions,
commonly through pass@𝑘. This measures generation capability, but does not indicate whether
the model can distinguish its passing generations from its failing ones. We formulate the latter as a
selective decision problem. Let 𝑆 (𝑥, 𝑦) ∈ R denote a reliability score for candidate 𝑦, where larger
values indicate a greater estimated likelihood of passing. A selective system uses this score to apply
a decision rule
𝜋 (𝑥, 𝑦, 𝑆) ∈ {ACCEPT, ABSTAIN}.
Thus, generation capability and reliability estimation are distinct. We study whether modelderived uncertainty scores provide reliable proxies for generation correctness.

4

Ravishka Rathnasuriya and Wei Yang
Ideal system

Practical system

Ideal system

Specification
Specification
Ideal system

CodeLLM
LLM
Code
Generalization
Generalization
Code
OracleLLM
Oracle

Specification

Practical system

Accept
Accept
/ /
Abstain
Abstain
Not
Available
Priori
Not
Available
a a
Priori
Accept /
Abstain

Generalization
(a) Ideal oracle-based
generNot A
Available
a Priori
Oracle system.

Specification
Specification
Practical system

Code LLM
Code LLM
Uncertainty
Uncertainty
Code
LLM
Estimator
Estimator

/
AcceptAccept
/
AbstainAbstain

Accept /
Abstain
Uncertainty
(b) Practical uncertainty-aware
system.
Estimator
Specification

alization oracle would determine whether
The oracle is replaced by an uncertainty esgenerated
code
should
be
trusted,
but
such
timator that assigns a reliability score from
SPECIFICATION
(HUMANEVAL
#0)
SPECIFICATION (HUMANEVAL #0)
Check
if
in
given
list
of
numbers,
any
two
numbers
are
closer
to
each
other
than
given
threshold.
an oracle
is
not
available
a
priori.
model
orthan
generation
behavior.
Check if in given list of numbers, any two numbers are closer to each
other
given
threshold.
SPECIFICATION (HUMANEVAL #0)
passes test suites

avg. token confidence: 0.93

fails test suites

avg. token confidence: 0.94

Check
if insuites
given list of numbers, any avg.
twotoken
numbers
are0.93
closer to each
than given threshold.
passes test
confidence:
failsother
test suites
def has_close_elements(numbers: List[float], threshold: float) -> bool:

defor
has_close_elements(numbers:
i in range(len(numbers) - 1): List[float], threshold: float) -> bool:
avg. token confidence: 0.92
passes
test
forfor
i inj in
range(len(numbers)
- 1):
range(i
+
1,suites
len(numbers)):
forif jabs(numbers[i]
in range(i + 1, -len(numbers)):
numbers[j]) < threshold:
def has_close_elements(numbers: List[float], threshold: float) -> bool:
True
if return
abs(numbers[i]
- numbers[j]) < threshold:
for i in range(len(numbers) - 1):
return False
return True
for j in range(i + 1, len(numbers)):
return False
if abs(numbers[i] - numbers[j]) < threshold:
return True
return False

avg. token confidence: 0.94

def has_close_elements(numbers: List[float], threshold: float) -> bool:
has_close_elements(numbers:
List[float], threshold: float) -> bool:
fordef
i in range(len(numbers)
- 1):
fails
test
suitesavg.
token confidence: 0.94
i in
range(len(numbers)
1):
if for
abs(numbers[i]
numbers[i + 1])
< threshold:
if
abs(numbers[i]
numbers[i
+
1]) < threshold:
return True
def has_close_elements(numbers: List[float], threshold: float) -> bool:
return False
return True
for i in range(len(numbers) - 1):
return False
if abs(numbers[i] - numbers[i + 1]) < threshold:
return True
return False

(c) Overconfident failure. Two solutions for the same task receive similar mean token confidence, although
one passes the test suite and the other fails by checking only adjacent elements on CodeLllama Model.
Fig. 1. Motivation for uncertainty-aware code generation. Since generalization oracle cannot be known a
priori, practical systems use model-derived uncertainty as a proxy reliability signal. The example illustrates
the failure mode studied in this paper: an incorrect program can receive confidence comparable to a passing
program.

2.2

Uncertainty-Aware Code Generation

Uncertainty-aware systems use model-derived evidence to decide whether an output should be
trusted. In an ideal code-generation system (Figure 1a), a generalization oracle would determine
whether a generated program generalizes to unseen tests, real inputs, or downstream use. Such
an oracle is not available a priori, because functional correctness must be established through
validation against specifications, tests, formal properties, or observed behavior.
Therefore, a practical uncertainty-aware system uses an estimated reliability signal as a proxy
for unavailable correctness information. Figure 1b illustrates this setting, where an uncertainty
estimator assigns a score 𝑆 (𝑥, 𝑦) to generated code. The key assumption is that this score is
informative about the execution outcome: higher-scoring candidates should be more likely to pass
than lower-scoring candidates. Overconfident failure arises when this assumption breaks, such that
a failing program receives a high reliability score and may therefore be accepted by the selective
system.
2.3

Sources of Uncertainty Signals

We define an uncertainty-derived reliability signal as a measurable score 𝑆 (𝑥, 𝑦) attached to a
generated candidate 𝑦 for prompt 𝑥. The score is intended to approximate the likelihood that 𝑦 will
pass the task’s tests. We consider three sources of model-derived reliability signals. White-box
signals use information from the model’s generation process, including token probabilities, entropy,
sequence likelihood, and hidden states. Black-box signals use variation across multiple sampled
generations without requiring access to model internals. Judge-based signals use an external
model to estimate the reliability of a generated program without executing it.

Characterizing Overconfident Failure in LLM-Based Code Generation

5

We also distinguish when the signal is measured. Prefill-stage signals are computed before any
code tokens are emitted, using only the prompt and the model’s initial processing. They may capture
prompt difficulty, ambiguity, or underspecification, but they cannot observe implementation-specific
errors. Decoding-stage signals are computed from generated tokens, token distributions, hidden
states, or sampled candidates. These signals are closer to the final program, but they may still reflect
local fluency or memorized coding patterns rather than functional correctness.
2.4

The Problem: Overconfident Failure

We define an overconfident failure as a failing generation that receives a high reliability score.
Formally, for prompt 𝑥, candidate 𝑦, execution outcome 𝑍 (𝑥, 𝑦), and reliability score 𝑆 (𝑥, 𝑦), overconfident failure occurs when 𝑍 (𝑥, 𝑦) = fail while 𝑆 (𝑥, 𝑦) lies in a high-reliability region. Because
score distributions vary across models and metrics, we do not assume a universal threshold. Instead, we examine whether failing generations receive reliability scores comparable to passing
generations.
The underlying challenge is that model confidence and program correctness characterize different properties. Token-level confidence reflects the probability assigned to decoding decisions,
whereas execution evaluates the semantics of the completed program. Therefore, a semantically incorrect implementation can receive high token-level confidence despite failing execution. Figure 1c
illustrates this mismatch under the same specification: the passing implementation compares all
element pairs, whereas the failing implementation checks only adjacent pairs. Despite this semantic
difference, both generations receive comparable token confidence.
3

Empirical Overview

This section summarizes the study design, including the evaluated models, benchmarks, and
research questions. Detailed experimental setups are described in the corresponding sections.
3.1

Benchmarks

We evaluate generated code on three execution-based benchmarks: HumanEval+, MBPP+, and
BigCodeBench. HumanEval+ [46, 47] and MBPP+ [47, 48] extend widely used function-level
code-generation benchmarks with stronger test suites from EvalPlus [4]. HumanEval+ contains
164 programming tasks specified by function signatures and natural-language descriptions. The
MBPP+ evaluation set contains 378 tasks derived from introductory programming problems. These
two benchmarks provide controlled function-level settings for evaluating execution correctness.
BigCodeBench [49] broadens the evaluation to programming tasks with richer contexts, more
complex instructions, and greater use of library APIs. It contains 1,140 Python tasks spanning
723 function calls from 139 libraries across seven domains. We include BigCodeBench to examine
whether overconfident failure persists beyond controlled function-level tasks.
Models. We study four code-specialized, open-source instruction-tuned LLMs: CodeLlama-7BInstruct, DeepSeek-Coder-7B-Instruct, Qwen2.5-Coder-7B-Instruct, and OpenCoder-8B-Instruct [1, 2,
50]. These models have been used in prior code-generation evaluations and provide comparable
open-source baselines in the 7-8B parameter range [47, 51, 52].
We select these models based on four criteria. First, their open-source availability enables access
to token-level statistics, prefill-stage signals, and internal representations. Second, restricting the
models to 7-8B parameters reduces variation attributable to model scale. Third, all models are
specialized and instruction-tuned for code generation. Fourth, the models originate from different
development lineages, reducing the risk that the observed behavior is specific to one training
pipeline. For the post-training analysis in Section 5.5, we additionally compare base and instructiontuned variants of OpenCoder and DeepSeekCoder. Table 1 reports the pass@1 accuracy of the

6

Ravishka Rathnasuriya and Wei Yang

primary models on each benchmark. All experiments were conducted on a server equipped with
an Intel(R) Xeon(R) w5-2545 CPU and four NVIDIA RTX 6000 Ada GPUs.
Table 1. Pass@1 Accuracy for Each Benchmark and Models
Model
CodeLlama DeepSeek-Coder OpenCoder QwenCoder
HumanEval+
34.1
70.1
78.0
71.3
MBPP+
46.0
66.1
71.2
65.9
BigCodeBench
6.5
20.6
23.8
8.2

3.2

Research Questions

We investigate overconfident failure through the following research questions.
RQ1: To what extent do existing uncertainty signals reflect the likelihood of generation correctness?
RQ2: How does overconfident failure manifest, and under what conditions does it persist in code
generation?
RQ3: To what extent do existing mitigation strategies reduce overconfident failure?
RQ4: Do latent representations contain correctness information not exposed by output uncertainty?
4

Reliability of Standard Uncertainty Signals for Failure Detection

This section addresses RQ1 in Section 3.2 by examining to what extent standard uncertainty signals
reliably indicate the likelihood that generated code will fail. This research question serves as an
initial diagnostic analysis: if existing metrics consistently separate passing from failing programs,
then overconfident failure would be less concerning for selective code generation.
Evaluation Setup. For each generated solution, we compute 17 generation-stage uncertainty
scores. We also compute six prefill scores: end-of-prompt next-token MSP, entropy, margin, energy, mean token entropy, and mean negative log-likelihood. Table 2 summarizes the evaluated
metrics. For metrics that require multiple generations, we sample up to 10 candidates per prompt
at temperature 1.0.
We evaluate each score using AUC, with fail as the positive class, and orient the scores so
that larger values indicate greater estimated failure risk. An AUC of 0.5 corresponds to random
ranking. We focus on HumanEval+ and MBPP+ because both passing and failing generations
are sufficiently represented across the studied models. We exclude BigCodeBench because its
substantially lower pass rates leave few passing generations for several models, making pass-fail
discrimination estimates less stable. Full metric definitions and implementation details are available
on the project website [60].
Results. Table 3 reports the generation and prefill results. For generation-stage uncertainty,
the best AUC in each model-benchmark pairs ranges from 0.598 to 0.696. No metric exceeds 0.70,
and several remain close to random ranking. The strongest metric also changes across models and
benchmarks where no metric family consistently provides the best separation.
Prefill uncertainty shows the same limitation. The highest AUC is 0.70 for CodeLlama on
HumanEval+, whereas most model–benchmark settings fall between 0.52 and 0.62. Several scores
are close to random ranking, particularly on MBPP+, and no prefill metric is consistently strongest
across models.
Finding. The limited failure discrimination is not specific to one uncertainty formulation or one
stage of inference. Across 17 generation-stage signals and six prefill signals, no uncertainty measure
provides stable failure ranking across models and benchmarks.

Characterizing Overconfident Failure in LLM-Based Code Generation

7

Table 2. Uncertainty signals evaluated in the preliminary study.
Family

Metrics

Signal captured

White-box
token scores

MSP, Perplexity, Entropy, PMI,
CPMI, R-Div, F-R Dist [28, 53–
56]
MCEnt, MSPS, RMI, Ens, MI[28,
57]

Measure token likelihood, surprise, distributional concentration, and prompt dependence.

White-box
multi-sample
scores
Black-box out- LexSim, EigV, DegGlobal [56,
put similarity
58]
Judge-based
scores

Judge, M_Judge [28, 59]

Measure probability support and distributional
disagreement across sampled candidates.
Measure diversity or disagreement among sampled programs without using model probabilities.
Measure LLM-estimated pass likelihood from
the prompt and generated solution.

Table 3. AUC (↑) results of prefill-stage and generative uncertainty metrics.
HumanEval+

MBPP+

Metric
CodeLlama

DeepSeek

OpenCoder

QwenCoder

CodeLlama

DeepSeek

OpenCoder

QwenCoder

0.690
0.700
0.690
0.590
0.600
0.610

0.590
0.590
0.590
0.420
0.580
0.590

0.530
0.530
0.520
0.540
0.540
0.580

0.530
0.540
0.520
0.560
0.430
0.440

0.460
0.470
0.470
0.530
0.560
0.590

0.490
0.600
0.450
0.540
0.570
0.600

0.480
0.500
0.480
0.510
0.540
0.570

0.610
0.540
0.620
0.520
0.540
0.550

0.623
0.623
0.615
0.510
0.589
0.619
0.614
0.553
0.554
0.542
0.628
0.629
0.629
0.632
0.568
0.514
0.514

0.630
0.630
0.639
0.501
0.503
0.640
0.627
0.622
0.622
0.617
0.624
0.618
0.611
0.609
0.521
0.601
0.601

0.617
0.617
0.635
0.557
0.681
0.625
0.640
0.594
0.589
0.599
0.615
0.634
0.536
0.532
0.574
0.507
0.506

0.568
0.568
0.570
0.589
0.578
0.573
0.513
0.517
0.507
0.582
0.598
0.596
0.568
0.563
0.578
0.542
0.542

0.561
0.561
0.567
0.572
0.509
0.567
0.543
0.598
0.599
0.578
0.696
0.691
0.589
0.585
0.561
0.538
0.538

0.517
0.517
0.524
0.546
0.551
0.519
0.533
0.588
0.589
0.638
0.660
0.651
0.615
0.609
0.556
0.631
0.631

0.622
0.622
0.629
0.569
0.546
0.623
0.629
0.529
0.533
0.511
0.565
0.600
0.515
0.516
0.514
0.522
0.522

Prefill uncertainty
MSP
Entropy
Margin
Energy
MeanTokenEntropy
NLL

Generative uncertainty
MSP
Perplexity
Entropy
PMI
CPMI
R-Div
F-R Dist
MCEnt
MSPS
RMI
Ens
MI
LexSim
EigV
DegGlobal
Judge
M_Judge

0.670
0.670
0.630
0.521
0.506
0.662
0.568
0.630
0.623
0.508
0.579
0.577
0.596
0.597
0.576
0.530
0.530

Implication. The results do not support a model- and task-independent mapping from standard
uncertainty scores to code correctness. Furthermore, an uncertainty signal that is useful in one
setting cannot be assumed to provide the same failure evidence in another.
SE Takeaway. Code-generation tools should not reuse uncertainty thresholds across models or
workloads. Acceptance and validation policies should be re-evaluated for each deployment setting
because the same uncertainty signal can provide different failure discrimination across settings.
5

Characterizing Overconfidence During Code Generation

In this section, we answer RQ2 by characterizing how overconfidence manifests across the codegeneration process. We examine whether failing programs remain highly confident overall, whether
local token behavior exposes regions of uncertainty, and whether predictive entropy provides
additional evidence of failure. We further study the effect of these uncertainty signals on selective
accuracy and examine whether overconfidence persists after instruction tuning.

8

Ravishka Rathnasuriya and Wei Yang

Table 4. Statistics on average and bottom-10% token confidence for passing and failing generated programs.
Sample Size
Task

Average Confidence

Bottom-10% Confidence

Model
Correct
Correct 𝑛

Incorrect

Correct

Incorrect 𝑛

t-value

Incorrect
t-value

p-value

HumanEval+

CodeLlama
DeepSeek
OpenCoder
QwenCoder

56
115
128
117

108
49
36
47

0.962 ± 0.012
0.951 ± 0.021
0.956 ± 0.024
0.947 ± 0.025

0.965
0.957
0.960
0.953

0.956 ± 0.014
0.943 ± 0.021
0.948 ± 0.023
0.935 ± 0.036

0.957
0.946
0.953
0.943

3.194
2.233
1.941
2.047

0.002
0.028
0.057
0.045

0.703 ± 0.076
0.642 ± 0.090
0.675 ± 0.119
0.619 ± 0.101

0.721
0.658
0.677
0.640

0.651 ± 0.083
0.607 ± 0.075
0.631 ± 0.090
0.559 ± 0.116

0.654
0.610
0.635
0.570

4.054
2.548
2.403
3.106

0.000
0.012
0.019
0.003

MBPP+

CodeLlama
DeepSeek
OpenCoder
QwenCoder

174
250
269
249

204
128
109
129

0.925 ± 0.025
0.944 ± 0.023
0.924 ± 0.024
0.901 ± 0.035

0.930
0.947
0.927
0.902

0.919 ± 0.026
0.938 ± 0.026
0.922 ± 0.028
0.881 ± 0.049

0.921
0.940
0.924
0.886

2.312
2.301
0.515
4.100

0.021
0.022
0.607
0.000

0.542 ± 0.081
0.609 ± 0.096
0.550 ± 0.080
0.480 ± 0.086

0.543
0.606
0.549
0.473

0.525 ± 0.083
0.589 ± 0.102
0.542 ± 0.095
0.439 ± 0.117

0.522
0.586
0.540
0.440

1.991
1.843
0.797
3.485

0.047
0.067
0.426
0.001

BigCodeBench

CodeLlama
DeepSeek
OpenCoder
QwenCoder

75
235
272
94

1065
905
868
1046

0.943 ± 0.020
0.913 ± 0.030
0.936 ± 0.025
0.897 ± 0.041

0.946
0.917
0.938
0.897

0.956 ± 0.039
0.909 ± 0.031
0.934 ± 0.027
0.920 ± 0.068

0.959
0.914
0.937
0.931

-5.171
1.587
0.908
-4.746

0.000
0.113
0.365
0.000

0.602 ± 0.094
0.511 ± 0.080
0.580 ± 0.099
0.455 ± 0.122

0.585
0.507
0.575
0.434

0.730 ± 0.204
0.498 ± 0.079
0.577 ± 0.095
0.574 ± 0.223

0.668
0.501
0.572
0.516

-10.249
2.289
0.428
-8.366

0.000
0.023
0.669
0.000

Mean ± Std.

Median

Mean ± Std.

Median

p-value
Mean ± Std.

Median

Mean ± Std.

Median

𝑝 = 0.000 indicates 𝑝 < 0.001 due to rounding.

5.1

Program-Level Confidence Remains High for Failing Generations

Evaluation Setup. We next measure confidence over the generated code. For each solution, we
compute average token confidence as the mean probability assigned to emitted tokens. To test
whether failures are exposed by localized uncertainty, we also compute bottom-10% confidence,
defined as the mean confidence of the least confident 10% of generated tokens. We compare passing
and failing generations using mean, standard deviation, median, and Welch’s two-sample (t)-test.
Results. Table 4 shows that both correct and incorrect programs receive high average token
confidence. On HumanEval+ and MBPP+, average confidence is typically above 0.90 for both groups.
Although correct solutions often have slightly higher confidence, the absolute gaps are small. For
example, on HumanEval+, the correct–incorrect average-confidence gap ranges from 0.007 to 0.012
across models. On MBPP+, the gap is even smaller for several models, including OpenCoder, where
correct and incorrect generations have nearly identical average confidence.
The pattern becomes more striking on BigCodeBench. For CodeLlama and QwenCoder, incorrect
generations have higher average confidence than correct generations. CodeLlama assigns mean
confidence 0.956 to incorrect generations and 0.943 to correct generations, while QwenCoder assigns
0.920 to incorrect generations and 0.897 to correct generations. These negative 𝑡-statistics, which
are statistically significant under standard two-sample 𝑡-tests, indicate that the observed differences
are unlikely to be due to random variation; rather, they reveal a systematic confidence–failure
mismatch, where the models are most confident precisely when they are wrong.
Finding. Generation-time confidence is high for both passing and failing programs. On controlled
benchmarks, confidence gaps are small; on BigCodeBench, some models are more confident on
failures than on correct solutions.
5.2

Local Token Confidence Provides Limited Failure Evidence

Program-level confidence may hide isolated generation steps at which the model is uncertain.
Therefore, we examine the least-confident tokens (i.e., the bottom 10% by confidence) within each
generated program to determine whether failures contain localized uncertainty that is not reflected
in the overall confidence score.
Table 4 shows that bottom-10% confidence is lower than average confidence, as expected, but it
still does not reliably separate correct and incorrect programs. On HumanEval+, correct solutions
have higher bottom-10% confidence than incorrect solutions, but the distributions remain close.
On MBPP+, the difference is weak for several models and statistically insignificant for OpenCoder.
On BigCodeBench, the trend reverses for CodeLlama and QwenCoder: incorrect generations have
substantially higher bottom-10% confidence than correct generations.Thus, local token confidence

Characterizing Overconfident Failure in LLM-Based Code Generation

(a) Average token entropy

9

(b) Top-10% token entropy

Fig. 2. Entropy distributions for OpenCoder on MBPP+.
QwenCoder

70
60
50
40

CodeLlama

10

25

50

Coverage (%)

75

90

100

DeepSeek

OpenCoder

QwenCoder

80
70
60
50
40

CodeLlama

10

25

50

Coverage (%)

75

90

100

DeepSeek

OpenCoder

QwenCoder

30

20

10

0

CodeLlama

Selective Accuracy (%)

OpenCoder

Selective Accuracy (%)

DeepSeek

Selective Accuracy (%)

Selective Accuracy (%)

CodeLlama

80

10

25

50

75

90

Coverage (%)

100

DeepSeek

OpenCoder

50

75

QwenCoder

30

20

10

0

10

25

90

100

Coverage (%)

(a) MBPP+ with avg. con- (b) MBPP+ with avg. en- (c) BigCodeBench with (d) BigCodeBench with
fidence
tropy
avg. confidence
avg. entropy
Fig. 3. Selective accuracy under uncertainty-based ranking. At each coverage level, we retain the most certain
generations according to average confidence or average entropy and report their execution accuracy. Lower
coverage corresponds to accepting a smaller subset of generations.

provides evidence in some settings, but many incorrect programs remain locally confident even at
their least confident tokens.
Finding. Local token confidence is insufficient: incorrect programs can remain confident even in
their least confident token regions.
5.3

Predictive Entropy Provides Limited Pass-Fail Separation

We further examine predictive entropy as a complementary measure of generation-time uncertainty.
At each generation step, predictive entropy is computed from the model’s probability distribution
over all possible next tokens. Entropy is low when probability mass is concentrated on a small
set of candidates and high when it is distributed more broadly across alternatives. Unlike token
confidence, which considers only the probability assigned to the emitted token, predictive entropy
accounts for the full next-token distribution. We test whether this broader uncertainty signal better
distinguishes failing from passing generations. If predictive entropy reflects functional correctness,
failing generations should exhibit systematically higher entropy than passing generations.
Figure 2 presents representative entropy distributions for OpenCoder on MBPP+. Both average
entropy and top-10% entropy show substantial overlap between correct and incorrect generations.
Although the mean entropy for incorrect outputs is marginally higher, the distributions are not
clearly separable. This observation aligns with the confidence analysis such that entropy captures
some uncertainty, but not enough to reliably identify failing programs.
Finding. Entropy provides the same qualitative picture as confidence. Failing programs often remain
in low-uncertainty regions, and local high-entropy scores do not consistently isolate failures.

10

Ravishka Rathnasuriya and Wei Yang
Average
Average Confidence
Confidence
Pass
Pass

1.2
1.2

Fail
Fail

0.8
0.8
0.6
0.6
0.4
0.4
0.2
0.2
0.0
0.0

Average
Average Entropy
Entropy
Pass
Pass

Fail
Fail

1.0
1.0

Average Entropy
Entropy
Average

Average Confidence
Confidence
Average

1.0
1.0

0.8
0.8
0.6
0.6
0.4
0.4
0.2
0.2

Base
Base

Instruction-tuned
Instruction-tuned

0.0
0.0

Base
Base

Instruction-tuned
Instruction-tuned

(a) OpenCoder with avg. (b) OpenCoder with avg. (c) DeepSeekCoder with (d) DeepSeekCoder with
confidence
entropy
avg. confidence
avg. entropy
Fig. 4. Uncertainty before and after instruction tuning on MBPP+. Each plot compares the distributions of
passing and failing generations for the corresponding base and instruction-tuned model.

5.4

Uncertainty-Based Selective Generation

We next evaluate whether uncertainty-based ranking can identify subsets of generated programs
with higher execution accuracy. This analysis investigates whether overconfident failures persist
among the generations assigned the highest certainty and therefore remain eligible for acceptance.
Evaluation Setup. For each generated program, we use average confidence and average entropy
as selection scores. We rank generations from most to least certain and retain the top 𝑐% at coverage
𝑐 ∈ {10, 25, 50, 75, 90, 100}. For example, 10% coverage accepts only the 10% most certain generations
and rejects the remaining 90%. We measure execution accuracy among the accepted programs.
Therefore, selective generation trades coverage for accuracy. If uncertainty reflects functional
correctness, removing uncertain generations should increase the accuracy of the accepted subset
relative to the model’s original accuracy. If high-certainty failures remain, reducing coverage may
provide little improvement or even reduce accuracy.
Results. Figure 3 shows different selection behavior across models and benchmarks. On MBPP+,
uncertainty identifies more accurate subsets for CodeLlama, DeepSeekCoder, and QwenCoder. For
CodeLlama, confidence increases accuracy from 46.0% at 100% coverage to 65.79% at 10% coverage.
QwenCoder increases from 65.9% to 80.00% at 25% coverage. Entropy produces a similar behavior for
QwenCoder, reaching 78.95% at both 10% and 25% coverage. DeepSeekCoder shows only a marginal
increase. However, for OpenCoder its original accuracy is 71.2%, yet confidence yields 71.05% at
10% coverage and 67.37% at 25%. Likewise, entropy provides similarly marginal improvement.
BigCodeBench shows that this behavior does not persist across benchmarks. DeepSeekCoder and
OpenCoder achieve modest accuracy improvements after uncertainty-based filtering. In contrast,
the 10% most certain generations from CodeLlama and QwenCoder contain no passing solutions
under either confidence or entropy where their original accuracies are 6.5% and 8.2%, respectively.
For CodeLlama, no generation in the top 25% by confidence passes either. In these cases, uncertaintybased filtering reduces accuracy rather than improving it.
The comparison further separates uncertainty-ranking quality from generation accuracy. OpenCoder has the highest original accuracy on MBPP+ but receives little accuracy improvement from
selective generation. Conversely, models with lower original accuracy can obtain substantially
more accurate retained subsets.
Finding. Overconfident failures can occupy the high-certainty region of the uncertainty ranking.
As a result, decreasing coverage does not consistently improve execution accuracy and can reduce
it when uncertainty is misaligned with functional correctness. This misalignment is model- and
benchmark-dependent and does not follow the model’s original generation accuracy.

Characterizing Overconfident Failure in LLM-Based Code Generation

5.5

11

Instruction Tuning Increases Certainty in Failing Generations

We next examine how instruction tuning changes overconfidence relative to the corresponding base
model. Specifically, we distinguish changes in the certainty assigned to failing generations from
changes in how well uncertainty separates passing from failing programs. This distinction allows us
to determine whether post-training improves uncertainty-based self-assessment or merely changes
the magnitude of model certainty.
Evaluation Setup. We compare base and instruction-tuned variants of OpenCoder and DeepSeekCoder on MBPP+. We evaluate average confidence and average entropy for passing and failing
generations and quantify their separation using AUC. To assess whether the change in discrimination after instruction tuning is stable across tasks, we compute a paired task-level bootstrap 95%
confidence interval for ΔAUC, defined as the instruction-tuned AUC minus the base-model AUC.
Results. Figure 4 shows how instruction tuning changes the confidence and entropy distributions
of passing and failing generations for OpenCoder and DeepSeekCoder. Instruction tuning increases
certainty on failing generations for both model families. For OpenCoder, the average confidence
of failing programs increases from 0.8685 to 0.9224, while their average entropy decreases from
0.4754 to 0.2401. Passing generations exhibit a comparable shift. As a result, the additional certainty
does not increase pass–fail separation. Confidence AUC changes from 0.5230 to 0.5094, with ΔAUC
= −0.0136 and a 95% confidence interval of [−0.0911, 0.0652]. Entropy AUC changes from 0.4915
to 0.5237, with ΔAUC = +0.0323 and an interval of [−0.0473, 0.1135]. These intervals provide no
evidence of a systematic change in discrimination.
For DeepSeekCoder, instruction tuning also increases certainty on failing programs, but the
uncertainty- correctness ordering changes. In the base model, confidence and entropy AUCs are
0.4391 and 0.4415, indicating that greater estimated certainty is associated with failing generations.
After instruction tuning, the AUCs increase to 0.5654 and 0.5672. The corresponding ΔAUC values
are +0.1263 for confidence and +0.1257 for entropy, with 95% confidence intervals of [0.0447, 0.2089]
and [0.0442, 0.2081], respectively. Therefore, instruction tuning changes the ordering from negatively aligned to positively aligned with correctness. However, the resulting AUCs remain below
0.57, indicating substantial pass-fail overlap.
Finding. Instruction tuning can increase overconfidence relative to the base model by increasing
certainty on failing generations. However, this change in certainty does not determine whether
uncertainty becomes more or less informative about functional correctness. For example, DeepSeekCoder becomes more certain on failing generations while its pass-fail discrimination improves.
Thus, post-training can increase confidence in incorrect code independently of the reliability of
uncertainty as a correctness signal.

5.6

Implications of Overconfidence Characterization

Our characterization separates three properties of reliability-aware code generation: functional
accuracy, uncertainty-based correctness discrimination, and its stability after post-training. Pass/fail
evaluation measures only the first and the latter two determine whether model uncertainty remains
informative for reliability decisions.
Reliability evaluation should measure correctness discrimination separately from task
accuracy. A model can achieve higher Pass@1 without becoming better at identifying which of its
generations are correct. Therefore, evaluation should report whether uncertainty separates passing
from failing programs in addition to reporting functional accuracy. Coverage-accuracy analysis
provides a corresponding view by showing whether uncertainty ranking yields more accurate
accepted subsets.

12

Ravishka Rathnasuriya and Wei Yang

Post-training objectives for correctness do not necessarily improve self-assessment.
Our base-instruction comparison shows that model certainty and correctness discrimination can
change independently after instruction tuning. Therefore, improving generation quality does not
impose a corresponding constraint on confidence assigned to remaining failures. Reliability oriented
post-training should treat generation correctness and uncertainty-based self-assessment as separate
optimization targets.
Uncertainty behavior should be re-evaluated after model updates. Post-training can alter
both the magnitude and the ordering of uncertainty scores. An uncertainty-based selection mechanism validated for one model version may no longer exhibit the same correctness discrimination
after the model is updated. Model evolution should include regression evaluation of both functional
accuracy and uncertainty-correctness alignment.
SE Takeaway. Overconfidence is not reduced automatically by improving code-generation accuracy.
Post-training can increase functional performance while high-certainty failures persist, making
overconfidence a distinct reliability property that must be assessed independently.
6

Limits of Mitigating Overconfident Failure

This section answers RQ3 on the effectiveness of common mitigation techniques for reducing
overconfident failure. We evaluate three practical responses: post-hoc calibration, repeated sampling,
and explicit abstention prompting. These strategies address different parts of the reliability problem
where calibration rescales scores, sampling increases the chance of finding a correct candidate, and
abstention prompting gives the model an explicit option to defer.
6.1

Calibration Improves Probability Alignment but Provides Limited Predictive Skill

Evaluation Setup. We examine to what extent post-hoc calibration mitigates overconfidence by
mapping uncertainty scores to estimated probabilities of execution correctness. For confidence,
we use average token confidence and bottom-10% token confidence. For entropy, we use average
token entropy and top-10% token entropy. We calibrate each score using Platt scaling (PS) [39]
which fits a logistic mapping from each original uncertainty score to an estimated probability
of correctness and isotonic regression [17] which fits a monotonic non-parametric mapping from
uncertainty scores to empirical correctness.
We estimate calibrated probabilities using five-fold stratified cross-validation to avoid evaluating
a calibrator on the generations used to fit it. Each calibrator is trained on 80% of the generations
and applied to the held-out 20%. For the uncalibrated baseline, we use confidence measures directly
as confidence proxies and transform entropy 𝐻 to 𝑒 −𝐻 .
We use Brier score (BS) to measure the error between predicted pass probability and execution
outcome [28, 39, 53–58, 61–63]. Lower BS indicates better probability alignment. Because a constant
predictor equal to the benchmark pass rate can also achieve a low BS, we additionally report Brier
Skill Score (BSS) [39]. For pass rate 𝑝𝑟 , the reference score is 𝐵 ref = 𝑝𝑟 (1 − 𝑝𝑟 ), and the skill score is
𝐵𝑆𝑆 = (𝐵 ref − 𝐵𝑆)/𝐵 ref . Positive BSS indicates improvement over the base-rate predictor, whereas
zero indicates equivalent performance.
Results. Table 5 reports the calibration results on MBPP+ and BigCodeBench. Across both
benchmarks, calibration substantially reduces Brier score, but the resulting Brier Skill Scores
remain minimal. On MBPP+, calibration substantially reduces BS, but the calibrated probabilities
provide little skill beyond the benchmark pass rate. For CodeLlama, PS reduces the BS of average
token confidence from 0.459 to 0.248, while BSS is approximately 0.001. DeepSeekCoder shows a
similar pattern where BS decreases from 0.300 to 0.224, but BSS remains approximately 0.001. For
OpenCoder, BS decreases from 0.250 to 0.205 while BSS remains near zero. QwenCoder obtains

Characterizing Overconfident Failure in LLM-Based Code Generation

13

Table 5. Calibration results measured by Brier Score (BS; ↓) and Brier Skill Score (BSS; ↑). Each entry reports
BS / BSS. For each model and metric, the lowest BS and highest BSS across Before, PS, and Iso are shown in
bold.
MBPP+
Avg. Conf.

Avg. Ent.

Bottom-10% Conf.

BigCodeBench

Model

Method

Top-10% Ent.

Avg. Conf.

Avg. Ent.

Bottom-10% Conf.

Top-10% Ent.

CodeLlama

Before
PS
Iso

0.459 / -0.849 0.345 / -0.387
0.248 / +0.001 0.247 / +0.005
0.253 / -0.020 0.251 / -0.012

0.252 / -0.015
0.248 / +0.004
0.257 / -0.035

0.284 / -0.142 0.856 / -12.926 0.699 / -10.379
0.246 / +0.008 0.061 / +0.001 0.061 / -0.000
0.255 / -0.025 0.062 / -0.002 0.062 / -0.001

0.548 / -7.922
0.060 / +0.017
0.062 / -0.001

0.343 / -4.578
0.062 / -0.002
0.061 / +0.002

Before
DeepSeekCoder PS
Iso

0.300 / -0.341 0.253 / -0.130
0.224 / +0.001 0.222 / +0.007
0.226 / -0.010 0.223 / +0.004

0.228 / -0.019
0.223 / +0.004
0.228 / -0.017

0.321 / -0.435 0.659 / -3.024 0.481 / -1.940
0.222 / +0.008 0.164 / +0.000 0.163 / +0.001
0.221 / +0.013 0.162 / +0.010 0.164 / -0.001

0.252 / -0.541
0.163 / +0.003
0.164 / -0.004

0.169 / -0.035
0.163 / +0.001
0.164 / -0.002

OpenCoder

Before
PS
Iso

0.250 / -0.219 0.213 / -0.039
0.205 / -0.000 0.205 / +0.001
0.210 / -0.025 0.205 / -0.000

0.236 / -0.149
0.205 / -0.000
0.205 / +0.000

0.378 / -0.840 0.666 / -2.667 0.532 / -1.931
0.203 / +0.008 0.182 / +0.000 0.182 / +0.000
0.209 / -0.016 0.183 / -0.006 0.183 / -0.005

0.305 / -0.677
0.182 / -0.000
0.182 / -0.003

0.200 / -0.099
0.182 / -0.001
0.183 / -0.006

QwenCoder

Before
PS
Iso

0.273 / -0.214 0.218 / +0.031
0.223 / +0.010 0.217 / +0.036
0.218 / +0.029 0.220 / +0.022

0.254 / -0.128
0.219 / +0.024
0.216 / +0.041

0.426 / -0.896 0.781 / -9.318 0.535 / -6.068
0.219 / +0.024 0.075 / +0.003 0.076 / -0.003
0.224 / +0.005 0.076 / +0.000 0.076 / -0.003

0.374 / -3.941
0.074 / +0.016
0.076 / -0.002

0.152 / -1.004
0.076 / +0.002
0.076 / -0.005

higher positive skill in some settings, although its largest BSS is only 0.041 for bottom-10% token
confidence after isotonic regression.
On BigCodeBench, calibration produces large reductions in BS while BSS remains near zero across
models. For CodeLlama, PS reduces the BS of average token confidence from 0.856 to 0.061, but the
corresponding BSS is approximately 0.001. Therefore, the calibrated BS is nearly equivalent to the
error of the base-rate predictor. The remaining models exhibit the same pattern, with calibrated
BSS values generally close to zero and the largest values reaching only about 0.01–0.02.
The BS and BSS results show that calibration primarily corrects the scale of the uncertainty
scores rather than providing substantial predictive information about individual generations.
This interpretation is consistent with our selective-accuracy analysis, where passing and failing
generations remain overlapping in the uncertainty space. Post-hoc calibration can remap these
scores to better-aligned probabilities, but it cannot remove the underlying overlap between correct
and incorrect generations.
Finding. Post-hoc calibration corrects the magnitude of overconfidence but does not resolve
overconfident failures. Although calibration substantially improves probability alignment, the
calibrated scores provide little skill beyond the benchmark pass rate and remain unable to reliably
distinguish passing from failing generations.
6.2

Reliability Under Finite Sampling Budgets

Evaluation Setup. We next evaluate whether repeated sampling can compensate for overconfident
single generations. We run four code models on MBPP+ and generate up to (K=50) candidate
programs per task using temperature sampling with (T=0.8). Each candidate is executed against
the task test suite. For each task, we record whether a passing solution appears within the first (k)
samples and how many passing candidates appear within the full budget.
Results. Figure 5 shows that sampling reduces the number of unsolved tasks quickly at small
budgets, but the curves flatten as (K) increases. Even after 50 attempts, many tasks remain unsolved, i.e., roughly 90 for CodeLlama, about 57 for DeepSeek, and around 45–50 for OpenCoder
and QwenCoder. Figure 5b shows that sampling mostly separates tasks into reliably solved and
persistently unsolved groups, with fewer partially recoverable cases.
These results characterize sampling as a bounded recovery mechanism rather than a reliability
mechanism. Additional samples can recover failures that are sensitive to decoding variation, but
the flattening curves show that many tasks remain unresolved even after substantial retry budget.
In a software-engineering workflow, each retry also incurs generation cost, latency, and additional

14

Ravishka Rathnasuriya and Wei Yang
EvalPlus+: tasks still failing vs k

225

175
150
125
100
75

CodeLlama
DeepSeek
QwenCoder
OpenCoder

120

number of tasks

# tasks still failing

200

EvalPlus+: per-task pass-count distribution

140

CodeLlama
DeepSeek
QwenCoder
OpenCoder

100
80
60
40
20

50

0
1

6

11

16

21

26

31

36

41

number of generated samples considered

(a) Tasks still failing vs. 𝑘.

46

0

5

10

15

20

25

30

number of plus-passes

35

40

45

50

(b) Per-task pass-count distribution
(𝐾=50).

Fig. 5. Sampling outcomes under EvalPlus+. (a) Remaining-unsolved tasks after the first 𝑘 generations. (b)
Distribution of how many successes each task attains within 𝐾=50 generations.

validation effort. Thus, sampling does not remove the accept-or-defer decision; it shifts the decision
to budget allocation. A practical system must decide when another sample is likely to help, when
a task should be escalated, and how to identify which candidate is trustworthy when multiple
candidates are available.
Finding. Sampling expands the candidate set but does not solve candidate selection or persistent
failure.
6.3

Explicit Abstention Prompting Does Not Reliably Induce Deferral

Evaluation Setup. We test whether explicit prompting can make a model defer when it is unlikely
to be correct. We use a penalty-aware prompt that instructs the model to answer only when it is
more than 95% confident and to otherwise output “I don’t know”. This tests whether a code LLM
can convert uncertainty into abstention without additional control logic.
Results. Figure 6 shows a representative failure on MBPP/72 for OpenCoder. The prompt
instructs the model to answer only when confident and assigns a high penalty to mistakes, while
allowing “I don’t know” as a zero-cost response. Nevertheless, the model generates code rather
than deferring. The generated program checks whether the input can be represented as a sum
of two squares (line 5), while the task asks for the difference of two squares. We observe the
same qualitative pattern across the subject models: even when abstention is explicitly allowed,
the standard code-LLMs behavior favors producing a concrete program instead of deferring. In SE
terms, the model continues to behave as a generator rather than as a reliability-aware component.
Finding. Prompt-level abstention does not reliably induce deferral; models can still generate
incorrect code even when an IDK option is provided.
6.4

Implications

Our results suggest that generation quality and correctness-sensitive confidence are distinct reliability properties. Improving the probability of generating correct code does not necessarily improve
the separation between correct and incorrect generations in confidence. Overconfidence exposes
this gap because incorrect generations can remain highly confident even when generation quality
or probability alignment improves.
SE Takeaway. Code-generation reliability should be evaluated along both dimensions. Pass rate
measures whether a model produces correct programs, whereas overconfident failure captures
whether incorrect programs remain highly trusted by the model’s confidence signal. Improvement
in generation quality should not be interpreted as a corresponding reduction in overconfidence.
Research Insight. Overconfidence motivates treating correctness-sensitive confidence as an
explicit learning objective rather than an expected consequence of better code generation. Future

Prompt-conditioned hidden-state
metrics forhidden-state
passing vs failing
generated
c
Prompt-conditioned
for passing
Input: prompt + generated solution;
metrics computed
only overmetrics
generated
soluti

10

Pass
Fail
20 30

0.90
80
0.85
70
0.80
60
0.75
50
00

Layer

Fig. 6. Ablation: Explicit abstention prompting still yields
incorrect code instead of deferral on MBPP/72 for OpenCoder.

Effective
EntropyRank

Anisotropy
Effective
Rank

80.20

Pass
Pass
Fail
Fail
10 20
10
20 30

Layer
Layer

(a) CodeLlama.

0.15
0.10

70

Pass
Fail

Pass
Fail
0 0 1010 2020

Layer
Layer

Intr
Ani

0.20 7.5 Pa
Fa
0.15 5.0

0.10 2.5
30
0 0 10

(b) QwenCoder.

Fig. 7. Layerwise effective rank for CodeLlama
and QwenCoder on HumanEval+.

techniques should aim to reduce confidence on incorrect generations while preserving confidence
on correct generations. This formulation extends the reliability objective from producing correct
code to distinguishing which generated code can be trusted.
7

Intrinsic Dimension

Entropy

0

1. def dif_Square(n) :
2.
i=0
3.
j = int(n ** 0.5)
4.
while i <= j:
5.
if i * i + j * j == n:
6.
return True
7.
elif i * i + j * j < n:
8.
i += 1
9.
else:
10.
j -= 1
11. return False

Anisotropy

Entropy

#Code

0.90
0.85
Write a python function to check whether the given number can be represented as
the difference of two squares or not.
0.80
assert dif_Square(5) == True
0.75
Final answer is:

Entropy
Effective Rank

#Prompt:
Answer only if you are more than 95% confident.
Mistakes are penalized by 100 points.
A correct answer receives 1 point.
An answer of "I don't know" receives 0 points.

Effective
Rank
Anisotropy

Characterizing Overconfident Failure in LLM-Based Code Generation Input: prompt + generated solution; metrics 15
computed only

Latent-Space Evidence of Overconfident Failure

This section addresses RQ4 by investigating overconfident failure signals in latent representationspace of code-LLMs.
Evaluation Setup. Inspired by recent latent-space analyses of reasoning models [64], we analyze
the latent representation space across transformer layers. For each generated solution, we feed the
prompt and generated code to the model and compute hidden-state statistics only over the generated
solution tokens. We focus on effective rank [65], which summarizes how many representation
directions are effectively used at a layer. Given a hidden-state matrix (𝐻 ℓ ) at layer (ℓ), effective rank
is computed from the normalized singular-value spectrum of (𝐻 ℓ ). Higher effective rank indicates a
more dispersed representation, while lower effective rank indicates a more compact representation.
Results. Figure 7 compares layerwise effective rank for CodeLlama and QwenCoder on HumanEval+. Although the models operate at different pass@1 levels, both show the same pattern:
failing generations have higher effective rank than passing generations across many middle and
later layers. This indicates that failing generations induce a less compact hidden-state geometry.
This contrasts with RQ2, where output-token confidence often failed to separate passing from
failing programs. The result suggests that correctness-related variation may be partially encoded
internally but not exposed through token probabilities.
Finding. Passing and failing generations differ in latent representation-space geometry even when
output confidence remains unreliable.
SE Takeaway. A confident decoding trace should not be interpreted as a low-risk program.
Representation-level signals may help future tools identify candidates that appear reliable from
token probabilities but still require validation.
Research Insight. The effective-rank separation suggests a representation-aware direction for
mitigating overconfident failure. If failing generations occupy a different latent-state regime, then
correctness risk is partially represented internally but not coupled to decoding behavior. Future SE
research should therefore study such objectives that make these internal risk signals operational:
lowering confidence, triggering deferral, or routing candidates to validation when hidden-state
geometry indicates likely failure. This shifts uncertainty from an external post-hoc score to a
learned mapping from representations to reliability actions.

L

16

8

Ravishka Rathnasuriya and Wei Yang

Discussion

Our findings suggest three directions for reducing overconfident failure: training, inference-time
control, and reliability evaluation.
1) Train models to recognize likely failures. Our post-training results show that better
generation does not imply better discrimination between passing and failing programs. Instruction
tuning increases certainty on failing generations for both model families, while its effect on pass–fail
discrimination is inconsistent. Therefore, future post-training should optimize not only whether the
model generates correct code, but also whether it lowers confidence or defers when its generated
code is likely incorrect.
This direction requires execution-grounded training data. Each training example should connect
a task and generated candidate to an execution outcome, so that high-confidence failures can be
identified explicitly. Matched passing and failing candidates for the same task are particularly useful
because they control for differences in task difficulty. Such data can support objectives that penalize
confident failures and reward appropriate deferral. Our latent-space analysis provides an additional
opportunity where passing and failing generations exhibit different internal representations even
when output confidence overlaps, suggesting that these internal signals may support learned failure
prediction rather than relying only on token probabilities.
2) Couple model confidence with external evidence at inference time. Our selectivegeneration results show that high confidence alone is not sufficient for acceptance. In some settings,
the most certain generations contain disproportionately many failures. Therefore, inference-time
systems should not map confidence directly to “accept” or “defer.” Instead, confidence should be
one input to a control policy that determines what additional evidence is needed.
At inference time, the system should determine what additional evidence is needed before accepting generated code. We distinguish three such cases. First, when the task specification is incomplete
or ambiguous, the system should seek clarification from the developer. Second, when correctness
depends on missing external information, the system should retrieve or verify that information.
Third, when the risk lies in the generated implementation, the system should obtain programlevel evidence through testing, analysis, or an independent evaluator. Repeated generation can
support this process, but our results show that sampling alone does not resolve candidate selection
and eventually reaches persistent failures. Therefore, an inference-time controller should choose
among clarification, validation, regeneration, and deferral according to the expected reliability
improvement and its cost.
3) Evaluate reliability through system decisions. Our results show that score-level improvements can overstate practical reliability. Calibration substantially reduces BS while BSS remains
near zero in many settings, and explicit IDK prompting does not reliably induce deferral. Thus,
future evaluation should assess whether uncertainty leads to better acceptance and validation
decisions rather than only whether a confidence score is numerically well aligned.
A reliability benchmark should evaluate an end-to-end policy that can accept generated code,
obtain additional validation, retry generation, or defer. The evaluation should vary the cost of
accepting incorrect code and the available validation budget. The central outcome is whether the
system reduces false acceptance without relying on indiscriminate deferral or unlimited validation. Such evaluation would measure whether a code-generation system uses reliability evidence
appropriately under deployment constraints, rather than only whether it produces a calibrated
score.
These three directions target different causes of overconfident failure. Training determines
whether the model identifies likely failures, inference-time control determines how the system
responds to uncertain evidence, and evaluation determines whether those responses reduce false

Characterizing Overconfident Failure in LLM-Based Code Generation

17

acceptance. Ultimately, an intervention addresses overconfidence only to the extent that it reduces
failing programs that remain eligible for acceptance, without relying on indiscriminate deferral or
unbounded validation.
9

Limitations

Our study has three main limitations. First, we evaluate four open-source code LLMs in the 7–8B
range because our analyses require token probabilities and hidden representations and whether
the findings extend to larger proprietary models remains open. Second, we study single-generation
code synthesis rather than repository-scale or agentic workflows, where tool use and iterative
feedback may change how overconfidence emerges. Third, our evaluation is limited to Python
benchmarks with execution-based test suites. These provide practical correctness labels but do not
establish complete semantic correctness or cover other languages and development settings.
10

Threats to Validity

This section discusses potential threats to validity in our study, organized into four standard
categories: internal, external, construct, and conclusion validity. These categories address risks
pertaining to our experimental design and methodology, as well as the generalizability of our
findings.
Internal validity. Our results depend on the correct implementation of uncertainty metrics,
calibration methods, sampling procedures, and execution-based evaluation. We mitigate this threat
by following standard definitions from prior work [28, 53–58, 61, 62], reusing established implementations when available, and applying the same evaluation pipeline across models and benchmarks.
For stochastic procedures, such as sampling-based uncertainty and repeated generation, we use
fixed decoding settings within each experiment and compare trends across multiple models. Nevertheless, implementation details such as token filtering, sequence truncation, and score orientation
may affect individual metric values.
External validity. We evaluate four open-source code LLMs on HumanEval+, MBPP+, and BigCodeBench analyses. These benchmarks provide executable correctness labels and allow controlled
comparison of uncertainty signals, but they do not cover all software-engineering settings. Our
findings may not fully generalize to larger proprietary models, project-level development tasks,
other programming languages, or agentic workflows with tool use and iterative repair. Metrics
requiring token probabilities or hidden states also assume white-box model access, which may not
be available for API-only models. Extending this analysis to closed models and repository-scale
tasks remains future work.
Construct validity. We operationalize correctness using benchmark test suites. Although HumanEval+ and MBPP+ strengthen the original tests, execution outcomes may still miss untested
behaviors. Thus, our labels approximate functional correctness rather than prove semantic equivalence. We also treat token confidence, entropy, calibration scores, sampling behavior, abstention,
and latent effective rank as proxies for reliability-related evidence. These constructs do not directly
measure program correctness; they measure whether model-derived signals align with execution
outcomes. This distinction is central to our study, but it limits claims about absolute correctness.
Conclusion validity. Our conclusions are based on trends observed across multiple models,
benchmarks, uncertainty families, and mitigation strategies. The main findings do not depend on
a single metric: weak failure detection, high-confidence failures, limited local-token separation,
bounded sampling gains, and unreliable prompt-level abstention appear across settings. However,
exact effect sizes may vary with decoding parameters, calibration splits, thresholds, and benchmark
composition. We therefore avoid claiming that uncertainty is useless. Our conclusion is more

18

Ravishka Rathnasuriya and Wei Yang

specific: the evaluated model-derived signals are insufficient as standalone reliability mechanisms
for deciding that generated code is likely to pass execution-based validation.
11

Related Work

Uncertainty estimation in ML and NLG. Uncertainty estimation has been widely studied in
classification, using confidence scores, entropy, Bayesian approximations, ensembles, and calibration methods to identify unreliable predictions [17–27]. Recent work extends these ideas to
natural-language generation through token uncertainty, sequence likelihood, sample diversity,
semantic uncertainty, and judge-based estimates [28–33, 57, 66–70]. Code generation differs because correctness is determined by executable program behavior rather than textual plausibility
or subjective quality. Our work studies whether these uncertainty signals remain useful under
execution-based correctness.
Uncertainty and calibration for code models. Prior work has studied uncertainty, calibration,
and reliability signals for code models [10–13, 33, 38–45, 71, 72]. These studies show that code
models can be miscalibrated and that post-hoc methods can improve confidence alignment. Our
focus is different: we study whether model-derived uncertainty can support reliability decisions
for generated code, such as identifying likely failures, abstaining, or deciding when additional
validation is needed. This setting is distinct from uncertainty in non-generative SE tasks such as
defect prediction or vulnerability detection [72, 73], where predictions are labels over existing
artifacts rather than generated programs whose correctness is observed only after execution.
Code-generation evaluation and mitigation. Code-generation research commonly evaluates
models with pass@1, pass@k, execution feedback, repair, and prompting strategies [10–13, 50, 51].
These methods measure or improve the ability to produce correct code, but they do not fully address
whether a model can recognize when its own output is likely to fail. Sampling can increase the
chance that a correct candidate exists, but does not identify which candidate should be trusted.
Prompt-level abstention can expose a deferral option, but does not guarantee safe generate-or-defer
behavior. We evaluate these techniques as responses to overconfident failure rather than as general
performance-improvement methods.
Summary. Our work provides a rigorous characterization of the dilemma of overconfidence
in code LLMs: model-derived uncertainty is available during generation, but it does not reliably
identify generated programs that fail execution-based evaluation. The results position overconfident
failure as a deployment-facing SE reliability problem and motivate future mechanisms that connect
model self-assessment to execution-grounded correctness.
12

Conclusion

This paper characterizes the dilemma of overconfidence in execution-grounded code generation.
We show that model-derived uncertainty often fails to identify incorrect programs, even under
calibration, sampling, and abstention prompting. These results motivate behavior-aware evaluation
that measures high-confidence failures, generate-or-defer behavior, and reliability under limited
validation budgets.

Characterizing Overconfident Failure in LLM-Based Code Generation

19

References
[1] B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez et al., “Code llama:
Open foundation models for code,” arXiv preprint arXiv:2308.12950, 2023.
[2] D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. Li et al., “Deepseek-coder: When the
large language model meets programming–the rise of code intelligence,” arXiv preprint arXiv:2401.14196, 2024.
[3] X. Jiang, Y. Dong, L. Wang, Z. Fang, Q. Shang, G. Li, Z. Jin, and W. Jiao, “Self-planning code generation with large
language models,” ACM Transactions on Software Engineering and Methodology, vol. 33, no. 7, pp. 1–30, 2024.
[4] J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is your code generated by chatGPT really correct? rigorous evaluation
of large language models for code generation,” in Thirty-seventh Conference on Neural Information Processing
Systems, 2023. [Online]. Available: https://openreview.net/forum?id=1qvx610Cu7
[5] J. Liu, S. Xie, J. Wang, Y. Wei, Y. Ding, and L. Zhang, “Evaluating language models for efficient code generation,” in
First Conference on Language Modeling, 2024. [Online]. Available: https://openreview.net/forum?id=IBCBMeAhmC
[6] GitHub, “GitHub Copilot: Your AI pair programmer,” 2021, accessed: 2025-07-18. [Online]. Available: https:
//github.com/features/copilot
[7] OpenAI, “OpenAI Codex,” 2021, accessed: 2025-07-18. [Online]. Available: https://openai.com/blog/openai-codex
[8] DeepMind, “AlphaEvolve: Evolutionary Algorithm Synthesis with LLMs,” 2025.
[9] ——, “AlphaCode: Competitive Programming with AI,” 2022, accessed: 2025-07-18. [Online]. Available: https:
//www.deepmind.com/research/highlighted-research/alphacode
[10] H.-S. Li, P. Fernandes, I. Gurevych, and A. F. Martins, “Doce: Finding the sweet spot for execution-based code
generation,” arXiv preprint arXiv:2408.13745, 2024.
[11] Y. Peng, A. D. Gotmare, M. R. Lyu, C. Xiong, S. Savarese, and D. Sahoo, “Perfcodegen: Improving performance of
llm generated code with execution feedback,” in 2025 IEEE/ACM Second International Conference on AI Foundation
Models and Software Engineering (Forge). IEEE, 2025, pp. 1–13.
[12] A. Ni, S. Iyer, D. Radev, V. Stoyanov, W.-t. Yih, S. Wang, and X. V. Lin, “Lever: Learning to verify language-to-code
generation with execution,” in International Conference on Machine Learning. PMLR, 2023, pp. 26 106–26 128.
[13] Z. Tian, J. Chen, and X. Zhang, “Fixing large language models’ specification misunderstanding for better code
generation,” in 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE). IEEE Computer
Society, 2025, pp. 645–645.
[14] F. Yao, Z. Wang, L. Liu, J. Cui, L. Zhong, X. Fu, H. Mai, V. Krishnan, J. Gao, and J. Shang, “Training language models to
generate quality code with program analysis feedback,” arXiv preprint arXiv:2505.22704, 2025.
[15] D. Shaikhelislamov, M. Drobyshevskiy, and A. Belevantsev, “Codepatchllm: Configuring code generation using a static
analyzer,” GenAI Evaluation KDD2024, 2024.
[16] P. J. Chapman, C. Rubio-González, and A. V. Thakur, “Interleaving static analysis and llm prompting,” in Proceedings
of the 13th ACM SIGPLAN International Workshop on the State Of the Art in Program Analysis, 2024, pp. 9–17.
[17] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, “On calibration of modern neural networks,” 2017.
[18] H. Wang, J. Xu, C. Xu, X. Ma, and J. Lu, “Dissector: Input validation for deep learning applications by crossinglayer dissection,” in Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering, 2020, pp.
727–738.
[19] D. Hendrycks and K. Gimpel, “A baseline for detecting misclassified and out-of-distribution examples in neural
networks,” 2018.
[20] Y. Gal and Z. Ghahramani, “Dropout as a bayesian approximation: Representing model uncertainty in deep learning,”
in international conference on machine learning. PMLR, 2016, pp. 1050–1059.
[21] U. Alon, M. Zilberstein, O. Levy, and E. Yahav, “code2vec: Learning distributed representations of code,” Proceedings
of the ACM on Programming Languages, vol. 3, no. POPL, pp. 1–29, 2019.
[22] Y. Xiao and W. Y. Wang, “Quantifying uncertainties in natural language processing tasks,” in Proceedings of the AAAI
conference on artificial intelligence, vol. 33, no. 01, 2019, pp. 7322–7329.
[23] V. T. Vasudevan, A. Sethy, and A. R. Ghias, “Towards better confidence estimation for neural models,” in ICASSP
2019-2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2019, pp.
7335–7339.
[24] C. Corbière, N. Thome, A. Bar-Hen, M. Cord, and P. Pérez, “Addressing failure prediction by learning model confidence,”
Advances in Neural Information Processing Systems, vol. 32, 2019.
[25] R. M. Monarch, Human-in-the-Loop Machine Learning: Active learning and annotation for human-centered AI. Simon and Schuster, 2021.
[26] J. Steinhardt and P. S. Liang, “Unsupervised risk estimation using only conditional independence structure,” Advances
in Neural Information Processing Systems, vol. 29, 2016.
[27] C. E. Shannon, “A mathematical theory of communication,” The Bell system technical journal, vol. 27, no. 3, pp.
379–423, 1948.

20

Ravishka Rathnasuriya and Wei Yang

[28] R. Vashurin, E. Fadeeva, A. Vazhentsev, L. Rvanova, A. Tsvigun, D. Vasilev, R. Xing, A. B. Sadallah, K. Grishchenkov,
S. Petrakov et al., “Benchmarking uncertainty quantification methods for large language models with lm-polygraph,”
arXiv preprint arXiv:2406.15627, 2024.
[29] Q. Xie, Q. Li, Z. Yu, Y. Zhang, Y. Zhang, and L. Yang, “An empirical analysis of uncertainty in large language model
evaluations,” arXiv preprint arXiv:2502.10709, 2025.
[30] Z. Xia, J. Xu, Y. Zhang, and H. Liu, “A survey of uncertainty estimation methods on large language models,” arXiv
preprint arXiv:2503.00172, 2025.
[31] Y. Bakman, D. N. Yaldiz, S. Kang, T. Zhang, B. Buyukates, S. Avestimehr, and S. P. Karimireddy, “Reconsidering llm
uncertainty estimation methods in the wild,” arXiv preprint arXiv:2506.01114, 2025.
[32] M. Ielanskyi, K. Schweighofer, L. Aichberger, and S. Hochreiter, “Addressing pitfalls in the evaluation of uncertainty
estimation methods for natural language generation,” in ICLR Workshop: Quantify Uncertainty and Hallucination in
Foundation Models: The Next Frontier in Reliable AI, 2025.
[33] Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma, “Look before you leap: An exploratory study of
uncertainty analysis for large language models,” IEEE Transactions on Software Engineering, 2025.
[34] J. Xin, R. Tang, Y. Yu, and J. Lin, “The art of abstention: Selective prediction and error regularization for natural language
processing,” in Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th
International Joint Conference on Natural Language Processing (Volume 1: Long Papers), 2021, pp. 1040–1051.
[35] B. Calder, G. Reinman, and D. M. Tullsen, “Selective value prediction,” in Proceedings of the 26th annual international
symposium on computer architecture, 1999, pp. 64–74.
[36] Z. Gu and M. Hopkins, “On the evaluation of neural selective prediction methods for natural language processing,” in
Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
2023, pp. 7888–7899.
[37] A. T. Kalai, O. Nachum, S. S. Vempala, and E. Zhang, “Why language models hallucinate,” arXiv preprint
arXiv:2509.04664, 2025.
[38] H. Vasconcelos, G. Bansal, A. Fourney, Q. V. Liao, and J. W. Vaughan, “Generation probabilities are not enough:
Improving error highlighting for ai code suggestions,” in HCAI Workshop at NeurIPS, 2022.
[39] C. Spiess, D. Gros, K. S. Pai, M. Pradel, M. R. I. Rabin, A. Alipour, S. Jha, P. Devanbu, and T. Ahmed, “Calibration and
correctness of language models for code,” arXiv preprint arXiv:2402.02047, 2024.
[40] Z. Zhou, C. Sha, and X. Peng, “On calibration of pre-trained code models,” in Proceedings of the IEEE/ACM 46th
international conference on software engineering, 2024, pp. 1–13.
[41] A. Sharma and C. David, “Assessing correctness in llm-based code generation via uncertainty estimation,” arXiv
preprint arXiv:2502.11620, 2025.
[42] D. D. Johnson, D. Tarlow, and C. Walder, “R-u-SURE? Uncertainty-aware code suggestions by maximizing utility across
random user intents,” in Proceedings of the 40th International Conference on Machine Learning, ser. Proceedings of
Machine Learning Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt, S. Sabato, and J. Scarlett, Eds., vol. 202.
PMLR, 23–29 Jul 2023, pp. 15 262–15 306. [Online]. Available: https://proceedings.mlr.press/v202/johnson23a.html
[43] R. Rathnasuriya and W. Yang, “When to answer and when to defer: A decision framework for reliable code predictions,”
in Proceedings of the IEEE/ACM 48th International Conference on Software Engineering, 2026, pp. 231–235.
[44] Y. Shi, C. Zhang, Y. Li, H. Wang, Y. Chen, N. Collier, and X. Gu, “Code is more than text: Uncertainty estimation for
code generation,” arXiv preprint arXiv:2606.09577, 2026.
[45] P. Rakasi, M. Lalwani, A. Srivastava, A. S. Palanivel, T. Adeleke, S. Wu, and R. Li, “When uncertainty isn’t enough:
An empirical study of self-correction in code generation,” in ICML 2026 Statistical Frameworks for Uncertainty in
Agentic Systems, 2026.
[46] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto et al., “Evaluating large language models trained on code,” Jul.
2021.
[47] J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is your code generated by chatgpt really correct? rigorous evaluation of large
language models for code generation,” Advances in Neural Information Processing Systems, vol. 36, pp. 21 558–21 572,
2023.
[48] Y. Dong, J. Ding, X. Jiang, G. Li, Z. Li, and Z. Jin, “Codescore: Evaluating code generation by learning code execution,”
ACM Transactions on Software Engineering and Methodology, vol. 34, no. 3, pp. 1–22, 2025.
[49] T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf, H. Zhan, J. He, I. Paul et al., “Bigcodebench:
Benchmarking code generation with diverse function calls and complex instructions,” in International Conference on
Learning Representations, vol. 2025, 2025, pp. 66 602–66 656.
[50] T. Zheng, G. Zhang, T. Shen, X. Liu, B. Y. Lin, J. Fu, W. Chen, and X. Yue, “Opencodeinterpreter: Integrating code
generation with execution and refinement,” arXiv preprint arXiv:2402.14658, 2024.
[51] F. Liu, Y. Liu, L. Shi, H. Huang, R. Wang, Z. Yang, L. Zhang, Z. Li, and Y. Ma, “Exploring and evaluating hallucinations
in llm-powered code generation,” arXiv preprint arXiv:2404.00971, 2024.

Characterizing Overconfident Failure in LLM-Based Code Generation

21

[52] W. Wang, C. Yang, Z. Wang, Y. Huang, Z. Chu, D. Song, L. Zhang, A. R. Chen, and L. Ma, “Testeval: Benchmarking
large language models for test case generation,” arXiv preprint arXiv:2406.04531, 2024.
[53] M. Darrin, P. Piantanida, and P. Colombo, “Rainproof: An umbrella to shield text generators from out-of-distribution
data,” arXiv preprint arXiv:2212.09171, 2022.
[54] L. Van der Poel, R. Cotterell, and C. Meister, “Mutual information alleviates hallucinations in abstractive summarization,”
arXiv preprint arXiv:2210.13210, 2022.
[55] J. Takayama and Y. Arase, “Relevant and informative response generation using pointwise mutual information,” in
Proceedings of the First Workshop on NLP for Conversational AI, 2019, pp. 133–138.
[56] M. Fomicheva, S. Sun, L. Yankovskaya, F. Blain, F. Guzmán, M. Fishel, N. Aletras, V. Chaudhary, and L. Specia,
“Unsupervised quality estimation for neural machine translation,” Transactions of the Association for Computational
Linguistics, vol. 8, pp. 539–555, 2020.
[57] L. Kuhn, Y. Gal, and S. Farquhar, “Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural
language generation,” arXiv preprint arXiv:2302.09664, 2023.
[58] Z. Lin, S. Trivedi, and J. Sun, “Generating with confidence: Uncertainty quantification for black-box large language
models,” arXiv preprint arXiv:2305.19187, 2023.
[59] J. Gu, X. Jiang, Z. Shi, H. Tan, X. Zhai, C. Xu, W. Li, Y. Shen, S. Ma, H. Liu et al., “A survey on llm-as-a-judge,” The
Innovation, 2024.
[60] CodeCalibration, “Codecalibration.” [Online]. Available: https://codeairesearch.github.io/CodeGenUncertainty/
[61] E. Fadeeva, A. Rubashevskii, A. Shelmanov, S. Petrakov, H. Li, H. Mubarak, E. Tsymbalov, G. Kuzmin, A. Panchenko,
T. Baldwin et al., “Fact-checking the output of large language models via token-level uncertainty quantification,” arXiv
preprint arXiv:2403.04696, 2024.
[62] J. Duan, H. Cheng, S. Wang, A. Zavalny, C. Wang, R. Xu, B. Kailkhura, and K. Xu, “Shifting attention to relevance:
Towards the predictive uncertainty quantification of free-form large language models,” arXiv preprint arXiv:2307.01379,
2023.
[63] S. Devic, T. Srinivasan, J. Thomason, W. Neiswanger, and V. Sharan, “From calibration to collaboration: Llm uncertainty
quantification should be more human-centered,” arXiv preprint arXiv:2506.07461, 2025.
[64] H. Du, Y. Dong, and X. Ning, “Latent thinking optimization: Your latent reasoning language model secretly encodes
reward signals in its latent thoughts,” arXiv preprint arXiv:2509.26314, 2025.
[65] L. Wei, Z. Tan, C. Li, J. Wang, and W. Huang, “Diff-erank: A novel rank-based metric for evaluating large language
models,” Advances in Neural Information Processing Systems, vol. 37, pp. 39 501–39 521, 2024.
[66] X. Hu, J. Chen, X. Li, Y. Guo, L. Wen, P. S. Yu, and Z. Guo, “Towards understanding factual knowledge of large language
models,” in The twelfth international conference on learning representations, 2024.
[67] Y. Li, K. Zhou, Q. Qiao, B. Nguyen, Q. Wang, and Q. Li, “Investigating context-faithfulness in large language models:
The roles of memory strength and evidence style,” arXiv preprint arXiv:2409.10955, 2024.
[68] M. Hu, Z. Zhang, S. Zhao, M. Huang, and B. Wu, “Uncertainty in natural language processing: Sources, quantification,
and applications,” arXiv preprint arXiv:2306.04459, 2023.
[69] J. Baan, N. Daheim, E. Ilia, D. Ulmer, H.-S. Li, R. Fernández, B. Plank, R. Sennrich, C. Zerva, and W. Aziz, “Uncertainty
in natural language generation: From theory to applications,” arXiv preprint arXiv:2307.15703, 2023.
[70] A. Niwa and H. Iso, “Ambignlg: Addressing task ambiguity in instruction for nlg,” arXiv preprint arXiv:2402.17717,
2024.
[71] D. D. Johnson, D. Tarlow, and C. Walder, “Ru-sure? uncertainty-aware code suggestions by maximizing utility across
random user intents,” arXiv preprint arXiv:2303.00732, 2023.
[72] R. Rathnasuriya, Z. Zhao, and W. Yang, “Codeimprove: Program adaptation for deep code models,” in 2025 IEEE/ACM
47th International Conference on Software Engineering (ICSE). IEEE Computer Society, 2025, pp. 514–526.
[73] Y. Li, S. Chen, and W. Yang, “Estimating predictive uncertainty under program data distribution shift,” arXiv preprint
arXiv:2107.10989, 2021.

