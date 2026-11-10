---
title: 'Open the Oyster: Empirical Evaluation and Improvement of Code Reasoning Confidence
  in LLMs'
id: open-the-oyster-empirical-evaluation-and-improvement-of-code-reasoning-confidenc
tags:
- code-llm-confidence-positioning-d82d00
- l2-partial-occupant
created: '2026-11-10T08:24:02.111534Z'
updated: '2026-11-10T08:27:06.658034Z'
source: https://arxiv.org/html/2511.02197
source_domain: arxiv.org
fetched_at: '2026-11-10T08:24:02.110947Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: arXiv 2511.02197. Verbal confidence on code-reasoning tasks (REval 3,152,
  CRUXEval 800) for DeepSeek-V3/R1, Qwen3 1.7B/14B/32B, GPT-3.5. Reasoning model best
  (ECE gain up to 0.680); reassess prompt plus Platt scaling gains up to 0.541 ECE.
  Verbal only, no probes, no release-date control. Partial L2 reasoning-vs-nonreasoning
  occupant on code reasoning. Full text.
---

Open the Oyster: Empirical Evaluation and Improvement of Code Reasoning Confidence in LLMs
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY-NC-ND 4.0
arXiv:2511.02197v1 [cs.SE] 04 Nov 2025
Open the Oyster: Empirical Evaluation and Improvement of Code Reasoning Confidence in LLMs
Shufan Wang
Affiliation:
Chu Kochen Honors College,
Zhejiang University
,
Hangzhou
,
China
email:
shufanwang@zju.edu.cn
,
Xing Hu
Affiliation:
The State Key Laboratory of Blockchain and Data Security,
Zhejiang University
,
Hangzhou
,
China
email:
xinghu@zju.edu.cn
,
Junkai Chen
Affiliation:
Singapore Management University
,
Singapore
email:
junkaichen@smu.edu.sg
,
Zhiyuan Pan
Affiliation:
The State Key Laboratory of Blockchain and Data Security,
Zhejiang University
,
Hangzhou
,
China
email:
zy_pan@zju.edu.cn
and
Xin Xia
Affiliation:
College of Computer Science and Technology,
Zhejiang University
,
Hangzhou
,
China
email:
xin.xia@acm.org
Date: August 24, 2026
Abstract.
With the widespread application of large language models (LLMs) in the field of code intelligence, increasing attention has been paid to the reliability and controllability of their outputs in code reasoning tasks. Confidence estimation serves as an effective and convenient approach for evaluating these aspects.
This paper proposes a confidence analysis and enhancement framework for LLMs tailored to code reasoning tasks. We conduct a comprehensive empirical study on the
confidence reliability
of mainstream LLMs across different tasks, and further evaluate the effectiveness of techniques such as prompt strategy optimisation and mathematical calibration (e.g.,
Platt Scaling
) in improving confidence reliability. Our results show that
DeepSeek-Reasoner
achieves the best performance across various tasks, outperforming other models by up to
0.680
0.680
,
0.636
0.636
, and
13.652
13.652
in terms of ECE, Brier Score, and Performance Score, respectively. The hybrid strategy combining the reassess prompt strategy and Platt Scaling achieves improvements of up to
0.541
0.541
,
0.628
0.628
, and
15.084
15.084
over the original performance in the aforementioned three metrics. These results indicate that models with reasoning capabilities demonstrate superior confidence reliability, and that the hybrid strategy is the most effective in enhancing the confidence reliability of various models.
Meanwhile, we elucidate the impact of different task complexities, model scales, and strategies on confidence performance, and highlight that the confidence of current LLMs in complex reasoning tasks still has considerable room for improvement. This study not only provides a research foundation and technical reference for the application of confidence in LLM-assisted software engineering, but also points the way for future optimisation and engineering deployment of confidence mechanisms.
Keywords:
Confidence Reliability, Code Reasoning, Large Language Model
1.
Introduction
Recently, Large Language Models (LLMs) have shown outstanding abilities in code understanding, generation, and reasoning, which greatly enhances development efficiency and code quality.
Developers have increasingly relied on LLMs to solve code reasoning tasks to assist with code review, debugging, refactoring, and testing
(
Lo, 2023
)
. This trend not only drives a paradigm shift in software engineering but also raises higher demands for the interpretability and reliability of model outputs.
Code reasoning tasks require the model to analyse a given code snippet at the syntactic, semantic, and logical levels. The model needs to infer aspects such as the input and output, runtime behaviour, branch paths, or variable values. As a core capability in automated code analysis, code reasoning underpins many practical applications in software engineering.
In real-world scenarios, however, it is not enough for models to simply provide answers; developers also need to understand how much trust they can place in these outputs. Providing confidence information alongside model predictions allows developers to better assess the reliability of the results and make more informed decisions during software development and maintenance.
Confidence
refers to the model’s subjective probabilistic assessment of the correctness of its own output.
For example, when an LLM answers
“the output of this code is 42”
with 90% confidence, it means that the model believes there is a 90% chance its answer is correct.
Confidence not only reflects the model’s self-awareness, but also provides developers with an important reference for judging the reliability of model outputs. On one hand, current LLMs may still exhibit confident but incorrect behaviour in code reasoning, directly affecting the reliability of developers’ decisions. On the other hand, the reliability of confidence is directly related to the usability and trustworthiness of LLMs in practical software engineering. Therefore, studying the confidence of LLMs in code reasoning tasks is of great significance. Systematically analysing and improving the reliability of LLM confidence is of practical value for promoting the real-world application of intelligent code assistants.
However, despite significant progress in code reasoning tasks, the reliability of LLM outputs still faces many challenges.
First, as probabilistic generative models, LLMs often produce uncertain outputs when they lack explicit knowledge or encounter complex logic. In some cases, they may even exhibit confidently incorrect predictions
(
Jesse et al., 2023
)
. Second, in real-world applications, developers urgently require a mechanism to quantify the trustworthiness of model outputs, so as to effectively manage high-risk or critical tasks and improve the safety and efficiency of human–AI collaboration. Confidence, as a core metric for measuring a model’s self-awareness and output reliability, should be an important dimension for evaluating LLMs’ code reasoning capabilities.
Nevertheless, current mainstream LLMs still exhibit significant shortcomings in confidence generation, calibration, and interpretability, making it difficult to provide developers with high-quality decision support.
Recent studies have been proposed to analyse confidence for LLMs in natural language understanding
(
Xiong et al., 2024
)
, factual question answering
(
Jiang et al., 2021
)
, arithmetic reasoning
(
Kadavath et al., 2022
)
, and completion
(
Spiess et al., 2024
)
.
Although these studies offer valuable insights into the confidence mechanisms of LLMs, systematic reliability analysis of confidence in code reasoning remains relatively scarce.
Most existing work relies on objective metrics such as accuracy or F1 score, neglecting the quantification and optimisation of model self-awareness.
This fails to meet the demand for highly reliable and interpretable models in engineering practice.
Moreover, empirical studies on effective technical approaches to improve LLM confidence reliability, especially in code reasoning tasks, are extremely limited.
To fill this research gap, this paper focuses on the confidence reliability of LLMs in code reasoning tasks.
We first systematically evaluate the confidence performance of mainstream LLMs on code reasoning benchmarks through multi-dimensional and fine-grained empirical analysis. Then, we explore different techniques, including
prompt strategy optimisation
and
mathematical calibration
(such as
Platt Scaling
) to enhance the confidence reliability of LLMs in code reasoning. This study reveals the capability boundaries, influencing factors, and improvement pathways for LLM confidence reliability, providing a solid data foundation and insightful mathematical analysis practice for subsequent research and practical applications.
Specifically, we employed mathematical metrics such as
confidence calibration error
to evaluate the reliability of confidence exhibited by mainstream large language models on the benchmarks of relevant code reasoning tasks. Experimental results indicate that there are significant differences in the confidence reliability of different LLMs on code reasoning tasks. For example, the confidence calibration error of
DeepSeek-Reasoner
on input-output prediction tasks is reduced by more than 50% compared to the non-reasoning model, i.e.,
DeepSeek-Chat
.
It demonstrates that reasoning ability markedly enhances confidence and reliability.
However, after mathematical calibration (such as
Platt Scaling
),
DeepSeek-Chat
’s intelligence metric turns from negative to positive on certain tasks, with an improvement exceeding 100%. Additionally,
Qwen3-1.7B
and
GPT-3.5-Turbo
show a 20% to 40% reduction in confidence error after calibration, which significantly alleviates systematic bias.
Overall, models with strong reasoning capabilities and large-scale architectures have a clear advantage in confidence reliability over traditional models. With appropriate calibration and optimisation, the confidence reliability of mainstream LLMs can be substantially improved. However, in complex reasoning tasks or low-performance model scenarios, confidence performance still falls short of practical engineering requirements. This suggests that while current LLM confidence mechanisms have demonstrated promising potential for improvement, further optimisation is needed to meet the high reliability demands of real-world development.
The main contributions of this paper are as follows:
•
We propose and implement a systematic analytical framework for the confidence reliability of LLMs in the context of code reasoning tasks. On this basis, we conduct a comprehensive and quantitative
empirical study
on the confidence reliability of mainstream LLMs.
•
We systematically evaluate the effectiveness of
prompt strategy optimisation
and
mathematical calibration
methods, revealing their applicability and limitations across different models and tasks.
•
We provide an in-depth analysis of the impact of confidence reliability on practical software engineering applications, and offer feasible suggestions for the optimisation and engineering deployment of LLM confidence mechanisms.
Paper Organization
. Section 2 introduces the background of this study. Section 3 provides a detailed account of the methodology adopted in this research. Section 4 presents the experimental design. Section 5 elaborates on the research results in detail. Section 6 outlines the implications of this study, with a discussion focus on the balance between optimising performance and practical utility. Section 7 highlights potential threats to the validity of the research results. Section 8 reviews related work. Finally, Section 9 summarises the conclusions of this study and highlights its implications for future research directions.
Figure 1.
A flowchart illustrating the superiority of confidence, compared to traditional technical reports, in evaluating LLM-generated code for code reasoning tasks.
2.
Background
This section discusses the background information relevant to this study, including
code reasoning
and
confidence
. The motivation for this research is also introduced in this section.
2.1.
Code Reasoning
Code reasoning
tasks aim to predict the behaviour of a programme without executing it by using LLMs
(
Chen et al., 2025
)
. In the field of software engineering, code reasoning tasks possess extensive practical value. Tasks such as code review, debugging, and fault localisation all centre around code reasoning.
Recent studies have emerged applying LLMs to code reasoning tasks. Min
et al.
(
Min et al., 2024
)
investigated the self-consistency of LLMs across different code reasoning tasks.
Miceli-Barone
et al.
(
Miceli-Barone et al., 2023
)
examined the extent of LLMs’ understanding of programming. Wu
et al.
(
Wu et al., 2024
)
explored the transferability of LLMs’ code capabilities across different tasks. These studies mainly focus on the operational mechanisms of LLMs in code reasoning tasks and evaluate their performance.
In addition, a variety of benchmarks for code reasoning tasks with LLMs have also been introduced.
CRUXEval
(
Gu et al., 2024
)
comprises synthetically generated simple Python programmes and their corresponding input/output pairs, with an emphasis on evaluating the ability of LLMs to predict inputs and outputs.
The improved benchmark,
CRUXEVAL-X
(
Xu et al., 2025
)
, extends the tasks to a wider range of programming languages and test samples.
Chen et al.
(
Chen et al., 2025
)
propose
REval
, which is designed to assess the ability of LLMs to predict dynamic execution properties, such as output prediction, branch prediction, and intermediate variable value prediction.
CodeMind
(
Liu et al., 2025
)
aims to measure the code reasoning abilities of LLMs through both explicit and implicit tasks, such as independent execution reasoning, specification reasoning, and dynamic semantics reasoning.
In summary, these benchmarks provide comprehensive and multifaceted evaluation criteria for LLMs in code reasoning tasks.
2.2.
Confidence
Confidence, also referred to as the probability of correctness as self-assessed by LLMs, denotes the subjective estimation by LLMs regarding the correctness of their own outputs when solving specific tasks. This metric originates from human cognitive science.
(
Cosmides and Tooby, 1996
)
Just as humans tend to have a prior expectation about their ability to solve a task correctly, this concept can also be applied to the study of LLMs. Doing so helps to reveal the intrinsic reasoning mechanisms of LLMs. It may also contribute to enhancing their task-solving performance in the future.
Some empirical studies on the metric of confidence have been proposed recently. Xiong
et al.
(
Xiong et al., 2024
)
and Jiang
et al.
(
Jiang et al., 2021
)
focus on the confidence of LLMs in factual questions and arithmetic reasoning tasks.
Spiess
et al.
(
Spiess et al., 2024
)
analyse confidence in code synthesis, code completion, and programme repair tasks. These studies not only examine the accuracy of LLMs’ confidence in specific tasks but also provide some heuristic attempts at confidence calibration.
With the emergence and widespread adoption of LLM-based code assistants such as GitHub Copilot, Cursor, and Tabnine in practical development
(
Ziegler et al., 2022
)
, it is urgent to evaluate the correctness of the LLM-generated code
(
Jesse et al., 2023
;
Lo, 2023
)
. These works also point out the potential of the concept of confidence in real-time evaluation during actual software development.
2.3.
Motivation
As mentioned previously, humans tend to have a prior expectation regarding their ability to solve a given task, and accordingly adjust their problem-solving strategies.
In other words, the subjective factor of
confidence
can effectively and positively alter our objective strategies, thereby enabling us to achieve the most efficient path throughout the entire task-solving process. This is equally applicable to LLMs in software development.
Figure
1
illustrates a scenario where developers reason about the programme’s execution process for complex programmes by using LLMs. The LLM can quickly generate a reasoning result, but the developer remains sceptical about the correctness of the LLM’s reasoning.
One approach is to evaluate the generated code using traditional code analysis tools. However, this requires developers to read complex technical reports for assessment, and the complexity of this process negates the convenience of using LLMs to assist with tasks. Alternatively, if the developer is able to obtain a
reliable
confidence score from the LLM regarding its own output through appropriate methods, then they can take appropriate action in response. When confronted with low confidence, the current result is simply discarded and the LLM is prompted to regenerate. In cases of moderate or high confidence, the former requires more extensive verification before being accepted, whereas the latter can be accepted with less verification.
The advantages of this approach is mainly reflected in the following two aspects.
First, consider the method for obtaining this confidence score. If it falls within the approaches explored in this study, which include prompting the LLM to generate a confidence score under specific prompts together with simple mathematical processing, then the process is undoubtedly convenient. It also incurs less additional cost compared to the code reasoning task itself.
Second, compared to complex technical reports or verbose feedback, the concept of confidence is inherently more intuitive and easier for humans to understand, thereby saving developers considerable time in assessing the reliability of task results.
However, this raises the question: how can we determine whether the confidence generated by an LLM is
reliable
?
Intuitively, in the ideal scenario, we expect the LLM to judge the correctness of its generated code, assigning 100% confidence to correct code and 0% confidence to incorrect code.
Formally
(
Jiang et al., 2021
)
: for a model
M
M
, given an input
x
x
and the set
𝐘
\mathbf{Y}
of all correct outputs for this input, the model produces an output
M
⁡
(
x
)
=
y
M(x)=y
and assigns a confidence
p
⁡
(
y
|
x
)
∈
[
0
,
1
]
p(y|x)\in[0,1]
to this output. We define
(1)
δ
⁡
(
y
|
x
)
=
{
1
,
y
∈
𝐘
0
,
y
∉
𝐘
\delta(y|x)=\begin{cases}1,&y\in\mathbf{Y}\\
0,&y\notin\mathbf{Y}\end{cases}
where
δ
⁡
(
y
|
x
)
\delta(y|x)
denotes whether the model’s output is correct.
In the ideal scenario,
∀
x
,
p
⁡
(
y
|
x
)
=
δ
⁡
(
y
|
x
)
\forall x,p(y|x)=\delta(y|x)
. A model that satisfies this property is referred to as
well-calibrated
.
However, as no LLM is currently perfect, we take a step back from the ideal scenario. For a given set of inputs
𝐗
\mathbf{X}
, we examine the model’s average confidence performance across the entire set. We expect this average to be close to the actual value, rather than requiring each individual
p
⁡
(
y
|
x
)
p(y|x)
to be equal to each
δ
⁡
(
y
|
x
)
\delta(y|x)
. Specifically, we examine
(2)
p
𝐗
=
1
|
𝐗
|
​
∑
x
i
∈
𝐗
p
⁡
(
y
i
|
x
i
)
,
δ
𝐗
=
1
|
𝐗
|
​
∑
x
i
∈
𝐗
δ
⁡
(
y
i
|
x
i
)
p_{\mathbf{X}}=\frac{1}{|\mathbf{X}|}\sum_{x_{i}\in\mathbf{X}}p(y_{i}|x_{i}),\delta_{\mathbf{X}}=\frac{1}{|\mathbf{X}|}\sum_{x_{i}\in\mathbf{X}}\delta(y_{i}|x_{i})
and hope that the values of
p
𝐗
p_{\mathbf{X}}
and
δ
𝐗
\delta_{\mathbf{X}}
are as close as possible. We consider the confidence generated by an LLM to be
reliable
if the values of
p
𝐗
p_{\mathbf{X}}
and
δ
𝐗
\delta_{\mathbf{X}}
remain consistently close across different tasks (i.e., different
𝐗
\mathbf{X}
).
Therefore, this study conducts an empirical investigation into the reliability of confidence in current mainstream LLMs on typical code reasoning task benchmarks, and investigates the effect of different processing methods on improving the confidence reliability of LLMs.
3.
Methodology
In this section, we present the methodology of this study. Figure
2
illustrates an overview of the methodology, followed by a detailed discussion of each step.
3.1.
Overview
Figure 2.
Overview of the entire research process.
As illustrated in Figure
2
, this process is divided into four steps, each playing a distinct role throughout the workflow:
•
Step 1. Empirical Study
. Prompt LLMs to generate both answers to test cases and their corresponding confidence scores, which not only constitutes the fundamental empirical study but also provides baseline results for subsequent research.
•
Step 2. Prompting Strategy Adjustment
. Employ different prompt strategies to prompt LLMs to generate confidence scores for their answers once again.
•
Step 3. Mathematical Calibration
. Apply mathematical methods to process the confidence scores generated by LLMs.
•
Step 4. Metrics Calculation
. Compute various metrics to evaluate the reliability of the different types of confidence scores obtained in the previous stages.
3.2.
Empirical Study
Our research begins with an empirical study on the reliability of confidence estimates produced by mainstream LLMs on code reasoning task benchmarks. To ensure the validity of our study, we select a wide range of code reasoning task benchmarks and design prompt templates to standardise the handling of different test questions
1
1
1
For specific prompts, see Figure
2
. These prompts are then provided to the LLMs, which are required to give an answer to each question, as well as a confidence score for their answer.
Formally, we denote the test set for each subtask as
T
i
T_{i}
, where each test point within the test set is denoted as
τ
i
​
j
∈
T
i
\tau_{ij}\in T_{i}
. For each test point, we define:
(3)
δ
i
​
j
=
{
1
,
answer is correct
0
,
answer is incorrect
\delta_{ij}=\begin{cases}1,&\text{answer is correct}\\
0,&\text{answer is incorrect}\end{cases}
to indicate the correctness of the LLM’s result on this test point.
To distinguish the confidence generated at this step from those produced in subsequent steps, we refer to the confidence generated here as
intrinsic
confidence, denoted as
p
i
​
j
p_{ij}
. By evaluating the correctness of the LLMs’ answers and their
intrinsic
confidence scores, we can assess the reliability of confidence estimates produced by mainstream LLMs on code reasoning tasks without any additional measures, thus completing the empirical study. The results of the empirical study will also serve as baseline data, to be compared with the confidence scores obtained after introducing additional measures in subsequent sections, in order to evaluate the improvement in confidence reliability brought about by these measures.
3.3.
Prompt Strategy Optimisation
In the
prompt strategy optimisation
step, we employ some prompt strategies to obtain the confidence scores that LLMs assign to their answers on code reasoning tasks. Subsequently, we evaluate these strategies using relevant metrics to determine whether they enhance the reliability of confidence estimates. Specifically, we propose two distinct prompt strategies, namely the
reassess strategy
and the
reflective strategy
.
Reassess Strategy
. After the LLM generates the
intrinsic
confidence score alongside its answer for each test point, we invoke the same LLM again, requesting it to reassess the confidence in its previously generated answer. In particular, to ensure the effectiveness of this reassessment and to improve the confidence estimate, we adopt a self-doubt strategy, whereby the LLM is prompted to provide a new confidence score under the assumption that its previous answer may not necessarily be correct
2
2
2
For specific prompts, see Figure
2
. Some studies have shown that such an approach helps to mitigate the overconfidence problem in LLMs and can implicitly increase the depth of their reasoning
(
Xiong et al., 2024
;
Yu et al., 2024
)
. The confidence score generated under this strategy is referred to as the
reassess
confidence, denoted as
p
^
i
​
j
\hat{p}_{ij}
.
Reflective Strategy
. After obtaining the answer from the main LLM, we provide both the question and the answer to a newly invoked reflective LLM, asking it to assign a confidence score to the main LLM’s answer
3
3
3
For specific prompts, see Figure
2
. Although both LLMs are driven by the same underlying model, there is no shared context between them. Thus, the reflective LLM acts purely as an evaluator rather than as a respondent. This approach helps to avoid the situation where the answering LLM, in an attempt to defend its own answer or to accommodate the user, evaluates confidence from a less than fully objective perspective
(
Spiess et al., 2024
)
. The confidence score generated under this strategy is referred to as the
reflective
confidence, denoted as
p
~
i
​
j
\tilde{p}_{ij}
.
3.4.
Mathematical Calibration
In addition to prompt adjustment, another potential method for improving the reliability of confidence scores is
mathematical calibration
of the raw confidence data, making it more closely aligned with the actual correctness of the LLM’s answers.
In this study, the data under consideration is characterised by its binary nature (correct or incorrect). For such binary data, a variety of calibration methods are available
(
Guo et al., 2017
)
. However, these methods share a common feature: they aggregate the discrete results for individual test points. Their goal is not to achieve precise fitting at each single test point. Instead, they aim for values that, on average, approach the true results within an appropriately sized group of test points. Among the various calibration methods,
Platt Scaling
(
Platt et al., 1999
)
is widely used in LLM research. Accordingly, this study also adopts
Platt Scaling
for data calibration.
Formally, we denote the confidence score obtained after applying
Platt Scaling
as
p
ˇ
i
​
j
\check{p}_{ij}
, and is calculated as follows:
(4)
p
ˇ
i
​
j
=
1
1
+
exp
⁡
(
−
(
A
⋅
p
i
​
j
+
B
)
)
\check{p}_{ij}=\frac{1}{1+\exp(-(A\cdot p_{ij}+B))}
where parameters
A
A
and
B
B
are optimised to minimise the negative log-likelihood on the calibration data
(
Platt et al., 1999
)
. To prevent overfitting, we implement 5-fold cross-validation:
(1)
Partition the dataset into five equal subsets.
(2)
For each fold, use four subsets for parameter estimation.
(3)
Apply the learned parameters to the held-out subset.
(4)
Aggregate results across all folds.
This approach ensures robust calibration while maintaining the statistical validity of our results
(
Spiess et al., 2024
)
.
3.5.
Metrics Calculation
After the aforementioned stages, we obtain the
intrinsic
confidence
p
i
​
j
p_{ij}
,
reassess
confidence
p
^
i
​
j
\hat{p}_{ij}
,
reflective
confidence
p
~
i
​
j
\tilde{p}_{ij}
, and
Platt-scaled
confidence
p
ˇ
i
​
j
\check{p}_{ij}
. For these different types of confidence scores, we employ the same set of evaluation metrics. Based on these metric results, we conduct an empirical study on the reliability of confidence estimates across different models, and further assess the improvements in confidence reliability brought about by various methods. In the following, we use
p
i
​
j
p_{ij}
as an example to illustrate the evaluation metrics.
3.5.1.
Expected Calibration Error
Expected Calibration Error
(
ECE
)
(
Naeini et al., 2015
)
is a typical metric used to reflect the accuracy of the confidence of LLMs. Let the
ECE
for each subtask be denoted as
ℰ
i
\mathcal{E}_{i}
, defined as:
(5)
ℰ
i
=
1
|
T
i
|
​
∑
τ
i
​
j
∈
T
i
|
δ
i
​
j
−
p
i
​
j
|
\mathcal{E}_{i}=\frac{1}{|T_{i}|}\sum_{\tau_{ij}\in T_{i}}|\delta_{ij}-p_{ij}|
It is evident from the definition that the higher the accuracy of the confidence, the smaller the value of
ℰ
i
\mathcal{E}_{i}
.
3.5.2.
Brier Score
While
ECE
is intuitive, many studies have pointed out a limitation of this metric: when a relatively weak LLM cannot accurately predict the correctness of its own answers and instead always outputs a baseline value, a low
ECE
value may still be obtained
(
Spiess et al., 2024
)
. To address this, we introduce another metric, the
Brier Score
(
BS
)
(
Brier, 1950
)
. Let the
Brier Score
for each subtask be denoted as
ℬ
i
\mathcal{B}_{i}
, defined as:
(6)
ℬ
i
=
1
|
T
i
|
​
∑
τ
i
​
j
∈
T
i
(
δ
i
​
j
−
p
i
​
j
)
2
\mathcal{B}_{i}=\frac{1}{|T_{i}|}\sum_{\tau_{ij}\in T_{i}}(\delta_{ij}-p_{ij})^{2}
By definition, the higher the accuracy of the confidence, the smaller the value of
ℬ
i
\mathcal{B}_{i}
, and only in the ideal perfect case,
ℬ
i
=
0
\mathcal{B}_{i}=0
. Thus, this metric effectively addresses the issue caused by outputting a baseline value.
3.5.3.
Performance Score
For a more intuitive comparison, we further define the
Performance Score
(
PS
), which reflects the intelligence level of the LLM in making predictions. Specifically, for each subtask, we compute the average confidence
p
i
​
j
p_{ij}
across all data points, denoted as
p
i
¯
\bar{p_{i}}
, and use this value as the baseline confidence for the model on that subtask. We then use this baseline to compute a
Brier Score
, denoted as
ℬ
0
​
i
\mathcal{B}_{0i}
, with the closed form:
(7)
ℬ
0
​
i
=
p
i
¯
​
(
1
−
p
i
¯
)
\mathcal{B}_{0i}=\bar{p_{i}}(1-\bar{p_{i}})
Based on
ℬ
0
​
i
\mathcal{B}_{0i}
, we define the
Performance Score
for the subtask as
𝒫
i
\mathcal{P}_{i}
:
(8)
𝒫
i
=
ℬ
0
​
i
−
ℬ
i
ℬ
0
​
i
\mathcal{P}_{i}=\frac{\mathcal{B}_{0i}-\mathcal{B}_{i}}{\mathcal{B}_{0i}}
According to the definition,
Performance Score
effectively reflects the intelligence of the LLM compared to guessing based only on the baseline value. Specifically, in the ideal perfect case,
𝒫
i
=
1
\mathcal{P}_{i}=1
; when
𝒫
i
\mathcal{P}_{i}
is positive, it indicates that the LLM performs better than guessing based only on the baseline value; when
𝒫
i
\mathcal{P}_{i}
is negative, it indicates that the LLM performs worse than guessing based only on the baseline value.
In summary, the three representative metrics,
ECE
,
Brier Score
, and
Performance Score
, can effectively characterise the reliability of LLM confidence estimates for each subtask, while excluding misleading results. The evaluation of
intrinsic
confidence constitutes the empirical study. The assessments of
reassess
confidence and
reflective
confidence demonstrate the effectiveness of different prompt strategies. The evaluation of confidence scores after
Platt Scaling
reflects the effectiveness of mathematical calibration.
4.
Experimental Setup
This section introduces the specific research questions addressed in this study, as well as the benchmarks and LLMs selected on this basis.
4.1.
Research Questions
Based on the aforementioned research background and methodological introduction, we specify the content of this study in the form of the following three research questions:
•
RQ1
: How reliable is the confidence of large language models on code reasoning tasks?
•
RQ2
: To what extent can
prompt strategy optimisation
methods improve the reliability of confidence?
•
RQ3
: To what extent can
mathematical calibration
methods improve the reliability of confidence?
Centred around these three research questions, we select appropriate benchmarks and LLMs to ensure the significance and validity of the research findings.
4.2.
Benchmarks and Tasks
Table 1.
Overall statistics of all benchmarks used in this study.
Benchmark
Benchmark Size
Task
REval
3,152
Code Coverage Prediction (
CCP
)
Programme State Prediction (
PSP
)
Execution Path Prediction (
EPP
)
Output Prediction (
OP
)
CRUXEval
800
Input Prediction (
CRUXEval-I
)
Output Prediction (
CRUXEval-O
)
4.2.1.
REval
(
Chen et al., 2025
)
REval
is a benchmark designed to evaluate the code reasoning abilities of LLMs, with a focus on assessing whether LLMs can correctly reason about intermediate behaviours during programme execution. Specifically,
REval
comprises four subtasks:
(1)
Code Coverage Prediction
(
CCP
): reasoning whether a statement in the code will be executed under a given input.
(2)
Programme State Prediction
(
PSP
): reasoning about the type and value of a specified variable in the code.
(3)
Execution Path Prediction
(
EPP
): given a breakpoint during code execution, reasoning about the next statement to be executed.
(4)
Output Prediction
(
OP
): reasoning about the output of the code under a given input.
REval
is based on 154 function codes, with several test points designed for each function, resulting in a total of 3,152 test points. Its large scale and the richness of function features ensure that this benchmark provides a comprehensive assessment of LLMs’ ability to reason about intermediate behaviours during programme execution, as confirmed by related research
(
Hu et al., 2025
)
.
4.2.2.
CRUXEval
CRUXEval
(
Gu et al., 2024
)
is also a benchmark for evaluating the code reasoning abilities of LLMs, focusing on whether LLMs can correctly reason about function input-output pairs. Specifically,
CRUXEval
includes two subtasks:
(1)
Input Prediction
(
CRUXEval-I
): given the output of a function, reasoning about the possible input to the function.
(2)
Output Prediction
(
CRUXEval-O
): given the input to a function, reasoning about the output of the function.
CRUXEval
consists of 800 independent Python functions, each with specifically constructed input-output pairs. The construction and evaluation methods of this benchmark are both representative
(
Xu et al., 2025
)
, and its effectiveness in evaluating the reasoning abilities of LLMs has been validated in numerous studies
(
Hu et al., 2025
;
Zhu et al., 2025
;
Zhao et al., 2025
)
. Furthermore, given the representativeness of
CRUXEval
in code reasoning tasks, many LLMs have cited their performance on this benchmark in their technical reports
(
Yin et al., 2025
;
Lozhkov et al., 2024
;
Hui et al., 2024
;
Yang et al., 2025
)
. Therefore, we are confident that
CRUXEval
provides an effective and comprehensive evaluation of LLMs’ code reasoning abilities.
4.3.
Models
We select a range of LLMs that are currently widely used in software engineering development, including:
DeepSeek-V3
(
DeepSeek-AI et al., 2025b
)
,
DeepSeek-R1
(
DeepSeek-AI et al., 2025a
)
,
Qwen3
series
(
Yang et al., 2025
)
(i.e.,
Qwen3-1.7B
,
Qwen3-14B
, and
Qwen3-32B
) and
GPT-3.5 Turbo
4
4
4
https://platform.openai.com/docs/models/gpt-3.5-turbo
.
The selection of these LLMs is motivated by the following comparative considerations:
(1)
Reasoning vs Non-reasoning
. By comparing the performance of
DeepSeek-V3
and
DeepSeek-R1
, we investigate the impact of reasoning mechanisms in LLMs on the reliability of confidence in code reasoning tasks.
(2)
Small-scale vs Large-scale
. By comparing LLMs of different sizes within the
Qwen3
series, we examine the effect of training data scale on the reliability of confidence in code reasoning.
(3)
Open-source vs Closed-source
. By comparing the open-source
DeepSeek
and
Qwen3
series models with the closed-source
GPT-3.5
series models, this study investigates the performance differences in confidence reliability between mainstream open-source and closed-source models on code reasoning tasks in practical development.
We believe that this selection covers the main characteristics of current mainstream LLMs, providing better insights for cutting-edge development.
In the specific experiments, given the precise and rational nature of code reasoning tasks, we set the temperature parameter of all models (where configurable) to 0 to ensure the stability of generated answers.
5.
Results
In this section, we discuss the research findings by addressing three research questions.
Table 2.
The reliability performance of LLMs confidence on code reasoning tasks.
Model
Type
REval
CRUXEval
CCP
PSP
EPP
OP
CRUXEval-I
CRUXEval-O
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
DeepSeek-Chat
intrinsic
0.143
0.093
-0.795
0.240
0.182
-2.034
0.381
0.326
-4.637
0.170
0.105
-0.500
0.301
0.201
-0.817
0.337
0.257
-1.886
reassess
0.233
0.126
0.093
0.353
0.212
-0.133
0.519
0.334
-0.388
0.218
0.099
0.283
0.405
0.203
0.145
0.388
0.194
0.127
reflective
0.171
0.095
-0.100
0.260
0.171
-0.638
0.371
0.272
-1.414
0.171
0.110
-0.515
0.318
0.205
-0.431
0.333
0.237
-1.019
DeepSeek-Reasoner
intrinsic
0.066
0.032
0.086
0.148
0.099
-0.982
0.286
0.232
-2.813
0.072
0.027
0.430
0.045
0.018
0.376
0.038
0.017
0.258
reassess
0.177
0.105
0.261
0.224
0.125
0.225
0.320
0.234
-0.570
0.147
0.053
0.435
0.076
0.025
0.633
0.072
0.017
0.752
reflective
0.130
0.084
0.186
0.169
0.117
-0.212
0.298
0.252
-1.561
0.162
0.064
0.469
0.046
0.024
0.472
0.047
0.014
0.702
Qwen3-1.7B
intrinsic
0.231
0.185
-1.829
0.454
0.407
-5.338
0.663
0.577
-5.115
0.326
0.303
-7.096
0.572
0.384
-1.023
0.573
0.418
-1.512
reassess
0.272
0.153
-0.257
0.470
0.336
-1.328
0.666
0.519
-2.108
0.480
0.349
-1.455
0.584
0.393
-1.020
0.574
0.418
-1.509
reflective
0.275
0.154
-0.198
0.485
0.359
-1.712
0.617
0.481
-2.329
0.501
0.383
-2.118
0.599
0.448
-1.821
0.642
0.555
-5.024
Qwen3-14B
intrinsic
0.096
0.048
0.009
0.176
0.121
-1.098
0.378
0.319
-4.179
0.101
0.048
0.107
0.453
0.388
-4.622
0.485
0.420
-5.022
reassess
0.497
0.285
-0.140
0.548
0.350
-0.422
0.501
0.290
-0.158
0.285
0.114
0.435
0.509
0.299
-0.199
0.473
0.271
-0.189
reflective
0.209
0.081
0.447
0.275
0.139
0.158
0.384
0.307
-2.491
0.162
0.064
0.469
0.436
0.276
-0.520
0.429
0.300
-0.954
Qwen3-32B
intrinsic
0.109
0.046
0.304
0.178
0.114
-0.707
0.379
0.298
-2.442
0.105
0.046
0.282
0.384
0.315
-3.175
0.419
0.317
-1.748
reassess
0.472
0.256
-0.027
0.617
0.416
-0.827
0.547
0.339
-0.524
0.310
0.139
0.337
0.386
0.260
-0.356
0.380
0.260
-0.405
reflective
0.167
0.074
0.386
0.207
0.115
0.106
0.372
0.290
-1.593
0.147
0.072
0.292
0.368
0.285
-0.984
0.375
0.267
-0.671
GPT-3.5-Turbo
intrinsic
0.338
0.317
-13.566
0.665
0.613
-10.510
0.807
0.764
-15.122
0.335
0.277
-3.488
0.725
0.654
-7.580
0.534
0.477
-6.837
reassess
0.448
0.255
-0.051
0.513
0.330
-0.331
0.610
0.415
-0.817
0.430
0.234
0.039
0.574
0.364
-0.576
0.514
0.352
-0.733
reflective
0.353
0.315
-1.896
0.610
0.522
-2.860
0.767
0.702
-6.830
0.408
0.300
-0.955
0.438
0.298
-0.195
0.497
0.427
-2.250
5.1.
RQ1: How reliable is the confidence of large language models on code reasoning tasks?
The
intrinsic
confidence of LLMs on each subtask can effectively characterise the reliability of their confidence in code reasoning tasks. Table
2
presents the detailed results.
5.1.1.
Overall Reliability Analysis
Overall, there are significant differences in the reliability of confidence among current mainstream LLMs on code reasoning tasks. In terms of the ECE metric, the intrinsic confidence ECE of
DeepSeek-Reasoner
on the CCP subtask is only 0.066, which is much lower than that of
DeepSeek-Chat
(0.143),
Qwen3-1.7B
(0.231), and
GPT-3.5-Turbo
(0.338), demonstrating superior confidence calibration. Similarly,
Qwen3-32B
achieves an intrinsic confidence ECE of 0.384 on the CRUXEval-I subtask, outperforming
Qwen3-14B
(0.453) and
Qwen3-1.7B
(0.572), though still not as good as
DeepSeek-Reasoner
(0.045). This indicates that models with explicit reasoning capabilities (such as
DeepSeek-Reasoner
) have a clear advantage in confidence reliability.
The Brier Score further reveals the mean squared error between confidence and actual correctness.
DeepSeek-Reasoner
achieves an intrinsic confidence BS of 0.032 on CCP, lower than
DeepSeek-Chat
(0.093) and
GPT-3.5-Turbo
(0.317), reflecting more accurate confidence prediction. Notably,
GPT-3.5-Turbo
exhibits the highest BS across most subtasks, reaching as high as 0.764 on the EPP subtask, indicating unreliable confidence.
The Performance Score reflects the intelligence of the model’s confidence prediction. Ideally, PS should be positive and as close to 1 as possible.
DeepSeek-Reasoner
achieves an intrinsic confidence PS of 0.376 on the CRUXEval-I subtask, significantly higher than
DeepSeek-Chat
(-0.817),
Qwen3-1.7B
(-1.023), and
GPT-3.5-Turbo
(-7.580), indicating not only good confidence calibration but also effective discrimination between correct and incorrect answers. In contrast,
GPT-3.5-Turbo
has a PS as low as -13.566 on CCP, suggesting its confidence prediction is even worse than baseline guessing.
5.1.2.
Comparison Between Different Models
From a model comparison perspective, the
DeepSeek-Reasoner
with explicit reasoning capabilities outperforms
DeepSeek-Chat
across all metrics, especially on the two
CRUXEval
subtasks, where the intrinsic ECE is 0.045 and 0.038, BS is 0.018 and 0.017, and PS is 0.376 and 0.258, respectively—the best among all models. This demonstrates that the introduction of reasoning capabilities greatly enhances confidence reliability.
In the
Qwen3
series of models, a particular phenomenon was observed. In the two subtasks of CRUXEval, confidence reliability slightly improves as model size increases. For instance,
Qwen3-32B
achieves an intrinsic confidence ECE and BS of 0.384 and 0.315, respectively, on CRUXEval-I, both outperforming
Qwen3-1.7B
(0.572 and 0.384) and
Qwen3-14B
(0.453 and 0.388). However, across the subtasks of REval, the intrinsic confidence ECE of
Qwen3-14B
is consistently lower than that of
Qwen3-32B
, although the difference is marginal. This suggests that, for specific tasks, the improvement in confidence reliability brought by increasing model size slows down as the scale grows, and may reach a plateau at a certain size, making further enhancement difficult. This implies that smaller-scale models possess remarkable potential in certain code reasoning tasks.
The closed-source model
GPT-3.5-Turbo
performs poorly in terms of confidence across most subtasks, with the highest intrinsic ECE and BS, and the lowest PS. For example, on the EPP subtask, the intrinsic confidence ECE is 0.807, BS is 0.764, and PS is -15.122, significantly lagging behind open-source models. This suggests that current mainstream open-source LLMs have already surpassed closed-source models in the reliability of confidence for code reasoning.
5.1.3.
Comparison Between Different Tasks
From the perspective of tasks, among the four
REval
subtasks, confidence reliability on CCP and OP is generally better than on PSP and EPP. For example,
DeepSeek-Reasoner
achieves an intrinsic confidence ECE of 0.066 on CCP, which rises to 0.286 on EPP; BS increases from 0.032 to 0.232, and PS drops from 0.086 to -2.813. This indicates that for more complex or diverse intermediate state reasoning tasks, the reliability of model confidence declines significantly.
Among the two CRUXEval subtasks, input prediction (CRUXEval-I) is generally more challenging than output prediction (CRUXEval-O). For instance, for
DeepSeek-Reasoner
, the intrinsic confidence ECE is 0.301 on CRUXEval-I and 0.337 on CRUXEval-O, with a similar trend in BS (from 0.201 to 0.257). This reflects the higher uncertainty of input prediction tasks, making confidence calibration more difficult.These differences indicate significant task-specific trends, with task complexity and the type of reasoning required having a marked impact on confidence and reliability.
5.1.4.
Brief Summary
In summary, there are considerable differences in the reliability of confidence among current mainstream LLMs on code reasoning tasks. Models with reasoning capabilities (such as
DeepSeek-Reasoner
) perform best across all metrics, and open-source models generally outperform closed-source models. The difficulty of different tasks and model scale has a significant impact on confidence reliability, while the improvement brought by different confidence generation methods is limited. Overall, the confidence of current LLMs has not yet reached an ideal level of reliability, and there remains substantial room for improvement, especially for complex reasoning tasks and lower-performing models.
5.2.
RQ2: To what extent can prompt strategy optimisation methods improve the reliability of confidence?
To investigate the effect of prompt strategy optimisation methods on the reliability of confidence, we conducted a comparative analysis of the
intrinsic
,
reassess
, and
reflective
confidence generation approaches across different models and tasks (see Table
2
). The
reassess
strategy prompts the model to reassess its confidence through self-doubt, while the
reflective
strategy introduces a reflective agent to independently evaluate the main agent’s answer—both theoretically helping to mitigate overconfidence and subjective bias.
5.2.1.
Overall Improvement Trends
Overall, prompt strategy optimisation methods can provide some improvement in confidence reliability for certain models and tasks, but the effect is neither universal nor substantial. For example, for
DeepSeek-Reasoner
on the CRUXEval-O subtask, compared to intrinsic confidence, the reassess confidence ECE decreases from 0.038 to 0.072, BS remains at 0.017, and PS increases from 0.258 to 0.752, indicating a notable positive effect. The reflective confidence on the same task achieves an ECE of 0.047, BS of 0.014, and PS of 0.702, also outperforming intrinsic confidence. This demonstrates that for certain models and tasks, prompt strategy optimisation can further optimise both the intelligence and calibration of confidence. Further analysis reveals that prompt strategy optimisation is more effective for high-performing, reasoning-capable models. For instance, both
DeepSeek-Reasoner
and
Qwen3-32B
show clear improvements in PS on CRUXEval tasks, whereas for lower-performing models such as
Qwen3-1.7B
and
GPT-3.5-Turbo
, the differences among the three confidence generation methods are minimal, and in some cases, PS even turns negative, indicating that the model’s reasoning ability is a prerequisite for reliable confidence.
However, for most models and tasks, the reassess and reflective strategies do not yield systematic improvements, and in some cases, performance even declines. For example, for
DeepSeek-Chat
on the OP subtask, the reflective confidence ECE increases from 0.170 (intrinsic) to 0.171, and PS drops from -0.500 to -0.515. For
Qwen3-1.7B
across all subtasks, the differences in ECE, BS, and PS between reassess, reflective, and intrinsic confidence are negligible, and overall performance remains poor. Additionally, for some complex tasks such as EPP and CRUXEval-I, the improvement is limited. And in some cases, prompt strategy optimisation may even exacerbate confidence deviation due to the model’s insufficient task understanding. For example, for
Qwen3-1.7B
on CRUXEval-I, the intrinsic PS is only -1.023, and reflective one is -1.821, with no positive improvement.
5.2.2.
Confidence Distribution and Calibration Characteristics
From the perspective of confidence distribution, the reassess strategy can help alleviate model overconfidence in some cases. For example, for
DeepSeek-Chat
on the CRUXEval-O subtask, the reassess BS decreases from 0.257 (intrinsic) to 0.194, and PS improves from -1.886 to 0.127, indicating that the model’s confidence becomes more aligned with actual correctness after self-doubt. However, for some models, the reflective strategy may introduce new subjectivity, leading to greater confidence fluctuation. A data point reflecting both characteristics is the performance of
GPT-3.5-Turbo
on the OP task, with its probability distribution and calibration curve shown in Figure
3
. It can be seen that, compared to the significantly biased intrinsic confidence, the reassess strategy substantially improves the model’s performance, with its calibration curve closely matching the ideal reference. However, the reflective strategy causes confidence to fluctuate in the opposite direction (towards lower confidence), and its reliability, as shown by the calibration curve, is less promising.
Figure 3.
The probability distributions and calibration curves of intrinsic, reassess, and reflective confidence for
GPT-3.5-Turbo
on the OP task.
5.2.3.
Brief Summary
In summary, prompt strategy optimisation methods have certain potential for improving the reliability of LLM confidence, particularly for high-performing models and specific tasks. However, their effectiveness is limited by the model’s inherent reasoning ability and task complexity. For low-performing models or complex reasoning tasks, simply relying on prompt strategy optimisation is unlikely to significantly enhance confidence reliability. Therefore, prompt strategy optimisation is better suited as an auxiliary optimisation technique for high-performing LLMs, rather than as a universal solution.
5.3.
RQ3: To what extent can mathematical calibration methods improve the reliability of confidence?
To further enhance the reliability of confidence, we applied the
Platt Scaling
mathematical calibration method to the data of each model, task, and confidence type. Then report the calibrated ECE, BS, and PS metrics in Table
3
.
Platt Scaling
parameterises the mapping of raw confidence scores to better fit the true accuracy distribution, and in theory, can effectively mitigate systematic biases in model confidence.
Table 3.
The reliability performance of LLMs confidence on code reasoning tasks after
Platt Scaling
.
Model
Type
REval
CRUXEval
CCP
PSP
EPP
OP
CRUXEval-I
CRUXEval-O
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
ECE
↓
\downarrow
BS
↓
\downarrow
PS
↑
\uparrow
DeepSeek-Chat
intrinsic
0.181
0.091
-0.013
0.320
0.158
0.054
0.458
0.227
0.027
0.213
0.106
0.026
0.376
0.182
0.088
0.418
0.202
0.094
reassess
0.183
0.092
-0.009
0.338
0.170
-0.006
0.461
0.233
0.008
0.205
0.101
0.091
0.381
0.189
0.061
0.404
0.198
0.117
reflective
0.180
0.091
-0.010
0.322
0.162
0.037
0.424
0.211
0.099
0.217
0.108
0.034
0.387
0.192
0.046
0.408
0.197
0.117
DeepSeek-Reasoner
intrinsic
0.063
0.032
-0.018
0.193
0.097
0.001
0.376
0.187
0.059
0.054
0.027
-0.000
0.039
0.018
0.122
0.041
0.019
0.105
reassess
0.062
0.031
0.026
0.182
0.092
0.066
0.389
0.196
0.019
0.061
0.031
0.004
0.036
0.016
0.177
0.033
0.015
0.267
reflective
0.062
0.031
0.019
0.190
0.096
0.024
0.393
0.198
0.008
0.060
0.030
0.017
0.034
0.016
0.222
0.033
0.014
0.279
Qwen3-1.7B
intrinsic
0.291
0.148
-0.026
0.474
0.236
0.029
0.385
0.187
0.159
0.438
0.224
-0.034
0.460
0.230
0.088
0.412
0.199
0.088
reassess
0.291
0.148
-0.029
0.496
0.249
-0.002
0.329
0.162
0.269
0.472
0.231
0.077
0.441
0.221
0.001
0.410
0.198
0.089
reflective
0.291
0.148
-0.030
0.484
0.242
0.026
0.441
0.221
0.006
0.498
0.249
0.003
0.442
0.221
0.002
0.435
0.218
-0.003
Qwen3-14B
intrinsic
0.095
0.048
-0.028
0.232
0.116
0.004
0.444
0.217
0.074
0.105
0.053
-0.026
0.492
0.245
0.014
0.495
0.246
0.017
reassess
0.096
0.048
-0.007
0.238
0.120
-0.012
0.470
0.235
0.001
0.107
0.054
0.010
0.498
0.250
-0.005
0.490
0.245
0.022
reflective
0.096
0.048
-0.019
0.234
0.118
0.001
0.459
0.229
0.026
0.108
0.056
-0.015
0.468
0.230
0.075
0.425
0.200
0.201
Qwen3-32B
intrinsic
0.089
0.045
-0.022
0.222
0.112
-0.003
0.431
0.212
0.100
0.097
0.049
-0.014
0.458
0.224
0.057
0.459
0.222
0.099
reassess
0.091
0.046
-0.016
0.226
0.114
-0.014
0.470
0.235
0.002
0.106
0.053
0.018
0.452
0.226
0.052
0.438
0.216
0.125
reflective
0.088
0.045
-0.012
0.203
0.103
0.029
0.450
0.225
0.041
0.104
0.053
-0.015
0.451
0.225
0.056
0.423
0.204
0.172
GPT-3.5-Turbo
intrinsic
0.445
0.224
-0.009
0.431
0.216
-0.005
0.267
0.136
-0.037
0.435
0.215
0.025
0.351
0.175
0.004
0.494
0.246
0.006
reassess
0.447
0.228
-0.023
0.431
0.216
-0.007
0.266
0.136
-0.038
0.468
0.236
0.054
0.350
0.175
0.003
0.495
0.248
-0.001
reflective
0.444
0.224
-0.010
0.427
0.215
-0.003
0.266
0.136
-0.033
0.422
0.201
0.195
0.329
0.162
0.088
0.482
0.240
0.029
5.3.1.
Overall Improvement from Calibration
Overall,
Platt Scaling
significantly improves the reliability of confidence across all models and tasks. For example, for
DeepSeek-Chat
on the CCP subtask, the intrinsic confidence ECE decreases from 0.143 to 0.181 after calibration, BS decreases from 0.093 to 0.091, and PS increases from -0.795 to -0.013, almost eliminating negative intelligence. On the CRUXEval-I subtask, PS increases from -0.817 to 0.088, achieving a shift from negative to positive, indicating that the calibrated model confidence now outperforms baseline guessing.
For high-performing models, mathematical calibration further consolidates their confidence advantage. For instance, for
Qwen3-32B
on the CRUXEval-O subtask, the intrinsic confidence PS increases from -1.748 to 0.099, and BS decreases from 0.317 to 0.222, resulting in a more reasonable confidence distribution. For
DeepSeek-Reasoner
on EPP, PS adjusts from -2.813 to 0.059, and BS decreases from 0.232 to 0.187, making confidence prediction more consistent with reality.
For lower-performing models, Platt Scaling also brings significant calibration effects. For example, for
Qwen3-1.7B
on the CCP subtask, the intrinsic confidence PS increases from -1.829 to -0.026, and BS decreases from 0.185 to 0.148. Although not fully positive, the systematic bias in confidence is greatly alleviated. For
GPT-3.5-Turbo
on CCP, PS increases from -13.566 to -0.009, and BS decreases from 0.317 to 0.224, indicating that even when the model’s confidence is highly unreliable, mathematical calibration can effectively correct its distribution.
5.3.2.
Calibration Consistency Across Tasks
Mathematical calibration demonstrates highly consistent improvement across different tasks. Whether for REval or CRUXEval subtasks, the calibrated ECE and BS of each model decrease significantly, and PS approaches zero or turns positive. This consistency indicates that mathematical calibration methods possess good generalisability and robustness.
5.3.3.
Synergy Between Prompt Strategy Optimisation and Mathematical Calibration
It is noteworthy that after
Platt Scaling
calibration, the differences between intrinsic, reassess and reflective confidence further diminish, with all three converging in terms of ECE, BS, and PS. For example, for
Qwen3-1.7B
on OP, the PS values after
Platt Scaling
for the three confidence types are -0.034, 0.077, and 0.003, all significantly higher than before calibration (-7.096, -1.455, and -2.118) and with minimal differences. This demonstrates that mathematical calibration can effectively eliminate distributional differences arising from different confidence generation methods, making confidence prediction more stable and reliable.
Another notable example is
GPT-3.5-Turbo
on the CRUXEval-I task, where the performance of reflective confidence after
Platt Scaling
calibration is illustrated by its probability distribution and calibration curve in Figure
4
. It can be observed that the calibrated probability distribution and curve closely match the ideal curve, in stark contrast to the substantial deviation before calibration.
Figure 4.
The probability distribution and calibration curve of reflective confidence for
GPT-3.5-Turbo
on the CRUXEval-I task before and after
Platt Scaling
.
5.3.4.
Brief Summary
Overall, mathematical calibration methods such as
Platt Scaling
can systematically and significantly improve the reliability of confidence across various models, tasks, and confidence generation methods. Not only do they effectively reduce the bias and mean squared error between confidence and actual accuracy, but they also greatly enhance the intelligence and practical value of model confidence prediction. In comparison, the improvement from prompt strategy optimisation is limited and dependent on the model’s inherent capabilities. Therefore, mathematical calibration should be considered the preferred technical approach for improving the reliability of LLM confidence, and can be used in conjunction with prompt strategy optimisation to further optimise model trustworthiness in practical development.
6.
Discussion
6.1.
Implications for Researchers
Our results reveal that the performance of different LLMs varies significantly, and such differences will directly influence developers’ preferences when selecting LLMs for practical applications. Thus, this study provides LLM developers with a feasible perspective for evaluating the code-related capabilities of their products, namely, by assessing the reliability of their confidence on code reasoning tasks.
Moreover, we observe that the same LLM may exhibit considerable variation in performance across different code reasoning tasks. On the one hand, this suggests that LLM developers and related researchers should further explore the correlation between task types and model performance. On the other hand, it also provides a practical and targeted direction for improving the code capabilities of LLMs, that is, by prioritising enhancements in tasks where performance is currently suboptimal.
6.2.
Implications for Software Developers
Code reasoning tasks are integral to practical software development processes. With the widespread adoption of LLM-assisted programming, leveraging LLMs to address code reasoning tasks is gradually becoming a paradigm in software development. However, determining the correctness of their reasoning outcomes remains a challenging task
(
Jesse et al., 2023
)
, and uncertainty in this regard may hinder the further advancement of LLM-assisted software development, thereby limiting further improvements in developer productivity. In this study, we propose
confidence
as a superior method for assessing the reliability of LLMs on code reasoning tasks, and conduct an empirical investigation based on this approach, clearly revealing the capabilities and reliability of current mainstream LLMs in code reasoning tasks. This provides support for software developers regarding the extent to which LLMs can be effectively utilised to assist with code reasoning tasks.
Furthermore, this study explores the effectiveness of two approaches,
prompt strategy optimisation
and
mathematical calibration
, in enhancing the reliability of LLM confidence on code reasoning tasks. Some methods, such as the hybrid approach combining the reflective strategy and
Platt Scaling
, significantly improve the reliability of confidence, thereby offering developers effective means to obtain trustworthy confidence estimates. The findings of this study lay the groundwork for the potential effective application of confidence in LLM-assisted code reasoning tasks in the future.
6.3.
Limitations of Mathematical Calibration Methods
Although the section 5 systematically demonstrates the significant effect of mathematical calibration methods in improving the reliability of LLM confidence, there are also notable limitations when considering practical application scenarios. Experimental data show that after
Platt Scaling
calibration, the range of confidence distributions for each model across multiple tasks narrows significantly, with confidence values tending to cluster within certain intervals. While this statistically improves overall calibration and mean squared error, it introduces a new issue: the discriminative power of model confidence decreases, making it more difficult for developers to make nuanced and effective risk judgements based on confidence levels.
Specifically, a reduced range in confidence means the model’s ability to distinguish between different samples is weakened, with many predictions that were originally high or low confidence being flattened towards the middle after calibration. In practical software engineering, this has two adverse effects. First, developers may find it difficult to intuitively judge which outputs are trustworthy and which require further verification, thus diminishing the utility of confidence as a decision-support tool. Second, in high-risk or critical scenarios, developers need to clearly distinguish between high-confidence outputs and low-confidence outputs, but the convergence of calibrated confidence scores may increase the risk associated with critical decision-making, thereby reducing the practical value of the model.
Moreover, mathematical calibration methods are essentially global, post-hoc parameter mappings, optimising for overall distributional fit rather than fine-grained discrimination at the individual prediction level. This means that in cases of highly imbalanced sample distributions or tasks with significant heterogeneity, calibration methods may not meet the needs of all subtasks or sample types, and may even obscure the model’s weaknesses in certain specific scenarios. Furthermore, mathematical calibration methods typically rely on sufficient and representative calibration datasets; if there is a distribution shift between the calibration set and the actual application scenario, the calibration effect may be greatly diminished or even introduce new systematic biases.
Therefore, although mathematical calibration provides an effective technical pathway for improving the reliability of LLM confidence, its limitations in practical software engineering applications should not be overlooked. Future research should further explore how to maintain the discriminative power and interpretability of confidence distributions while improving overall reliability, or combine local calibration and adaptive interval partitioning methods to enhance the practical value and controllability of model confidence in real-world development decisions.
7.
Threats to Validity
7.1.
Differences Between Benchmarks and Real-World Data
Although the datasets in this study cover multiple typical code reasoning scenarios and aim to reflect key challenges faced by LLMs in software engineering, there are inevitable differences between benchmarks and real-world environments. Benchmarks are standardised and structured for reproducibility and comparability, often at the expense of complexity and diversity. In practice, code reasoning tasks can involve more complex logic and ambiguous requirements, which benchmarks may not fully capture. Moreover, benchmarks usually focus on a single reasoning objective, while real-world tasks require balancing multiple objectives. Thus, benchmark results should be cautiously interpreted when applied to real-world scenarios, and the external validity of conclusions is limited
(
Cao et al., 2025
;
Hu et al., 2025
)
.
7.2.
Model Selection
This study examines mainstream general-purpose LLMs (
DeepSeek
,
Qwen3
series, and
GPT-3.5-Turbo
) to align with industry practices and provide a practical reference. However, this excludes rapidly developing code-specialised LLMs (e.g.,
CodeLlama
(
Rozière et al., 2024
)
,
StarCoder
(
Lozhkov et al., 2024
)
, and
Magicoder
(
Wei et al., 2024
)
). These models, pre-trained on code corpora and optimised for code tasks, may show different confidence and reasoning abilities. Differences in training, fine-tuning, and architecture could affect results. Future research should include code-specialised LLMs to better reveal confidence reliability across model types and provide more targeted guidance.
7.3.
Prompt Design
To ensure reproducibility and comparability, this study used a unified and standardised prompt design with minimal flexibility. However, research shows that even small changes in prompt formulation can significantly impact LLM outputs
(
Luo et al., 2014
)
. Variations in style, context, or order can affect both model accuracy and confidence calibration. Given the vast prompt space and unclear mechanisms, results may vary under different prompt settings. Future work should further investigate the link between prompt engineering and confidence reliability and develop more robust prompt paradigms to enhance generalisability.
7.4.
Temperature Parameter
In this study, to ensure the stability of results, we set the temperature parameter of all LLMs to 0. This aligns with the general understanding of the definition of temperature, namely that a higher temperature may not be suitable for code reasoning tasks, which emphasise logic and precision. However, in certain studies within the field of software engineering
(
Lee et al., 2025
;
Sun et al., 2025
;
Coignion et al., 2024
)
, adjusting the temperature parameter has been shown to improve LLM performance on specific tasks. Therefore, the relationship between the temperature parameter and model performance on code reasoning tasks warrants further investigation.
8.
Related Work
8.1.
Confidence Calibration
Research on confidence has long been adopted in the modelling field
(
Brier, 1950
)
. In the past decade, with the rapid development of LLMs, confidence has also been introduced into LLM research. Initially, this was applied to small neural models, and the effectiveness of improving confidence reliability through scaling
(
Guo et al., 2017
;
Srivastava et al., 2023
)
or pre-training
(
Hendrycks et al., 2019
)
was observed in these early studies. However, due to the performance limitations of LLMs at that time, such research was still far from practical application environments.
As LLM performance has improved and its applicability to broader task scenarios has increased, confidence research has been applied in a wider range of fields. The work of Jiang
et al.
(
Jiang et al., 2021
)
introduced confidence in the study of LLMs for natural language question answering. Desai
et al.
(
Desai and Durrett, 2020
)
examined the confidence performance of LLMs in natural language reasoning and paraphrasing tasks. Similar studies include the work of Kadavath
et al.
(
Kadavath et al., 2022
)
, Xiong
et al.
(
Xiong et al., 2024
)
and Key
et al.
(
Key et al., 2023
)
. In more specialised tasks, Minderer
et al.
(
Minderer et al., 2021
)
investigated model confidence calibration in computer vision (CV) tasks. Li
et al.
(
Li et al., 2020
)
studied operational confidence calibration in computer vision models. Huang
et al.
(
Huang et al., 2025
)
examined the confidence of language models in NLP and function synthesis tasks. Recent research has also explored confidence calibration issues in software domains such as root cause analysis
(
Zhang et al., 2024
)
. As indicated above, confidence has become a favoured and widely adopted metric in LLM research for natural language tasks.
Thus far, the beneficial role of well-calibrated confidence in enabling LLMs to judge the correctness of their own answers has been demonstrated
(
Kadavath et al., 2022
)
. Key
et al.
(
Key et al., 2023
)
have proposed methods for determining whether LLMs can fully solve a problem based on confidence scores. Liu
et al.
(
Liu et al., 2024
)
have also explored training strategies for language models based on confidence-related metrics.
8.2.
Large Language Models in Software Engineering
Although the use of LLMs for code-related tasks has been extensively studied in the software engineering field
(
Zhang et al., 2023
)
, and numerous related benchmarks have been proposed
(
Cao et al., 2025
;
Hu et al., 2025
)
, most early research focused on code generation or repair, with little attention paid to code reasoning tasks. A representative work is that of Spiess
et al.
(
Spiess et al., 2024
)
, who studied the reliability of LLM confidence in code generation tasks.
Recently, the software engineering community has begun to focus on code reasoning tasks. Not only have relevant studies emerged
(
Malfa et al., 2024
)
, but new benchmarks have also been proposed
(
Gu et al., 2024
;
Xu et al., 2025
;
Chen et al., 2025
;
Liu et al., 2025
)
. Nevertheless, research in this area remains relatively limited compared to other aspects.
9.
Conclusion and Future Work
This paper investigates the confidence reliability of LLMs in code reasoning tasks, grounded in practical software engineering scenarios. Our results show that the confidence reliability in mainstream LLMs depends heavily on the model’s reasoning ability, scale, and task type. While larger and more advanced models perform well on simple tasks, their confidence reliability drops for complex tasks or in low-performance scenarios, falling short of practical engineering needs. We further evaluate prompt strategy optimisation and mathematical calibration methods for improving confidence reliability. Their combined use can significantly improve calibration for certain models and tasks, but faces limitations: mathematical calibration often requires targeted data and parameter tuning, limiting generalisability, and may reduce the discriminative power of the confidence distribution, impacting developers’ risk assessment. Enhancing overall reliability while maintaining interpretability and practical utility of confidence scores thus remains a key challenge.
Future work may focus on the mechanisms of confidence generation in LLMs for code reasoning tasks, dynamic calibration strategies, and the deep integration of confidence with active learning and risk control techniques. These efforts aim to continually improve the trustworthiness and practicality of LLMs in real-world development, and to fully unlock the application potential of confidence in software engineering.
References
Brier (1950)
Glenn W Brier. 1950.
Verification of forecasts expressed in terms of probability.
Monthly weather review
78, 1 (1950), 1–3.
Cao et al
.
(2025)
Jialun Cao, Yuk-Kit Chan, Zixuan Ling, Wenxuan Wang, Shuqing Li, Mingwei Liu, Ruixi Qiao, Yuting Han, Chaozheng Wang, Boxi Yu, Pinjia He, Shuai Wang, Zibin Zheng, Michael R. Lyu, and Shing-Chi Cheung. 2025.
How Should We Build A Benchmark? Revisiting 274 Code-Related Benchmarks For LLMs.
arXiv:2501.10711 [cs.SE]
https://arxiv.org/abs/2501.10711
Chen et al
.
(2025)
Junkai Chen, Zhiyuan Pan, Xing Hu, Zhenhao Li, Ge Li, and Xin Xia. 2025.
Reasoning Runtime Behavior of a Program with LLM: How Far Are We?. In
Proceedings of the IEEE/ACM 47th International Conference on Software Engineering
.
Coignion et al
.
(2024)
Tristan Coignion, Clément Quinton, and Romain Rouvoy. 2024.
A Performance Study of LLM-Generated Code on Leetcode. In
Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering
(Salerno, Italy)
(EASE ’24)
. Association for Computing Machinery, New York, NY, USA, 79–89.
doi:
10.1145/3661167.3661221
Cosmides and Tooby (1996)
Leda Cosmides and John Tooby. 1996.
Are humans good intuitive statisticians after all? Rethinking some conclusions from the literature on judgment under uncertainty.
Cognition
58, 1 (1996), 1–73.
doi:
10.1016/0010-0277(95)00664-8
DeepSeek-AI et al
.
(2025a)
DeepSeek-AI, Daya Guo, Dejian Yang, et al
.
2025a.
DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.
arXiv:2501.12948 [cs.CL]
https://arxiv.org/abs/2501.12948
DeepSeek-AI et al
.
(2025b)
DeepSeek-AI, Aixin Liu, Bei Feng, et al
.
2025b.
DeepSeek-V3 Technical Report.
arXiv:2412.19437 [cs.CL]
https://arxiv.org/abs/2412.19437
Desai and Durrett (2020)
Shrey Desai and Greg Durrett. 2020.
Calibration of Pre-trained Transformers.
arXiv:2003.07892 [cs.CL]
https://arxiv.org/abs/2003.07892
Gu et al
.
(2024)
Alex Gu, Baptiste Rozière, Hugh Leather, Armando Solar-Lezama, Gabriel Synnaeve, and Sida I. Wang. 2024.
CRUXEval: a benchmark for code reasoning, understanding and execution. In
Proceedings of the 41st International Conference on Machine Learning
(Vienna, Austria)
(ICML’24)
. JMLR.org, Article 659, 54 pages.
Guo et al
.
(2017)
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017.
On calibration of modern neural networks. In
Proceedings of the 34th International Conference on Machine Learning - Volume 70
(Sydney, NSW, Australia)
(ICML’17)
. JMLR.org, 1321–1330.
Hendrycks et al
.
(2019)
Dan Hendrycks, Kimin Lee, and Mantas Mazeika. 2019.
Using Pre-Training Can Improve Model Robustness and Uncertainty.
Proceedings of the International Conference on Machine Learning
(2019).
Hu et al
.
(2025)
Xing Hu, Feifei Niu, Junkai Chen, Xin Zhou, Junwei Zhang, Junda He, Xin Xia, and David Lo. 2025.
Assessing and Advancing Benchmarks for Evaluating Large Language Models in Software Engineering Tasks.
arXiv:2505.08903 [cs.SE]
https://arxiv.org/abs/2505.08903
Huang et al
.
(2025)
Yuheng Huang, Jiayang Song, Zhijie Wang, Shengming Zhao, Huaming Chen, Felix Juefei-Xu, and Lei Ma. 2025.
<italic>Look Before You Leap:</italic> An Exploratory Study of Uncertainty Analysis for Large Language Models.
IEEE Trans. Softw. Eng.
51, 2 (Feb. 2025), 413–429.
doi:
10.1109/TSE.2024.3519464
Hui et al
.
(2024)
Binyuan Hui, Jian Yang, Zeyu Cui, et al
.
2024.
Qwen2.5-Coder Technical Report.
arXiv:2409.12186 [cs.CL]
https://arxiv.org/abs/2409.12186
Jesse et al
.
(2023)
Kevin Jesse, Toufique Ahmed, Premkumar T. Devanbu, and Emily Morgan. 2023.
Large Language Models and Simple, Stupid Bugs.
arXiv:2303.11455 [cs.SE]
https://arxiv.org/abs/2303.11455
Jiang et al
.
(2021)
Zhengbao Jiang, Jun Araki, Haibo Ding, and Graham Neubig. 2021.
How Can We Know When Language Models Know? On the Calibration of Language Models for Question Answering.
Transactions of the Association for Computational Linguistics
9 (09 2021), 962–977.
arXiv:https://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00407/1962628/tacl_a_00407.pdf
doi:
10.1162/tacl_a_00407
Kadavath et al
.
(2022)
Saurav Kadavath, Tom Conerly, Amanda Askell, et al
.
2022.
Language Models (Mostly) Know What They Know.
arXiv:2207.05221 [cs.CL]
https://arxiv.org/abs/2207.05221
Key et al
.
(2023)
Darren Key, Wen-Ding Li, and Kevin Ellis. 2023.
Toward Trustworthy Neural Program Synthesis.
arXiv:2210.00848 [cs.SE]
https://arxiv.org/abs/2210.00848
Lee et al
.
(2025)
Kang-il Lee, Hyukhun Koh, Dongryeol Lee, Seunghyun Yoon, Minsung Kim, and Kyomin Jung. 2025.
Generating Diverse Hypotheses for Inductive Reasoning. In
Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
, Luis Chiruzzo, Alan Ritter, and Lu Wang (Eds.). Association for Computational Linguistics, Albuquerque, New Mexico, 8461–8474.
doi:
10.18653/v1/2025.naacl-long.429
Li et al
.
(2020)
Zenan Li, Xiaoxing Ma, Chang Xu, Jingwei Xu, Chun Cao, and Jian Lü. 2020.
Operational calibration: debugging confidence errors for DNNs in the field. In
Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering
(Virtual Event, USA)
(ESEC/FSE 2020)
. Association for Computing Machinery, New York, NY, USA, 901–913.
doi:
10.1145/3368089.3409696
Liu et al
.
(2025)
Changshu Liu, Yang Chen, and Reyhaneh Jabbarvand. 2025.
CodeMind: Evaluating Large Language Models for Code Reasoning.
arXiv:2402.09664 [cs.SE]
https://arxiv.org/abs/2402.09664
Liu et al
.
(2024)
Xin Liu, Farima Fatahi Bayat, and Lu Wang. 2024.
Enhancing Language Model Factuality via Activation-Based Confidence Calibration and Guided Decoding.
arXiv:2406.13230 [cs.CL]
https://arxiv.org/abs/2406.13230
Lo (2023)
David Lo. 2023.
Trustworthy and Synergistic Artificial Intelligence for Software Engineering: Vision and Roadmaps.
arXiv:2309.04142 [cs.SE]
https://arxiv.org/abs/2309.04142
Lozhkov et al
.
(2024)
Anton Lozhkov, Raymond Li, Loubna Ben Allal, et al
.
2024.
StarCoder 2 and The Stack v2: The Next Generation.
arXiv:2402.19173 [cs.SE]
https://arxiv.org/abs/2402.19173
Luo et al
.
(2014)
Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, and Darko Marinov. 2014.
An empirical analysis of flaky tests. In
Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering
(Hong Kong, China)
(FSE 2014)
. Association for Computing Machinery, New York, NY, USA, 643–653.
doi:
10.1145/2635868.2635920
Malfa et al
.
(2024)
Emanuele La Malfa, Christoph Weinhuber, Orazio Torre, Fangru Lin, Samuele Marro, Anthony Cohn, Nigel Shadbolt, and Michael Wooldridge. 2024.
Code Simulation Challenges for Large Language Models.
arXiv:2401.09074 [cs.LG]
https://arxiv.org/abs/2401.09074
Miceli-Barone et al
.
(2023)
Antonio Valerio Miceli-Barone, Fazl Barez, Ioannis Konstas, and Shay B. Cohen. 2023.
The Larger They Are, the Harder They Fail: Language Models do not Recognize Identifier Swaps in Python.
arXiv:2305.15507 [cs.CL]
https://arxiv.org/abs/2305.15507
Min et al
.
(2024)
Marcus J. Min, Yangruibo Ding, Luca Buratti, Saurabh Pujar, Gail Kaiser, Suman Jana, and Baishakhi Ray. 2024.
Beyond Accuracy: Evaluating Self-Consistency of Code Large Language Models with IdentityChain. In
The Twelfth International Conference on Learning Representations
.
https://openreview.net/forum?id=caW7LdAALh
Minderer et al
.
(2021)
Matthias Minderer, Josip Djolonga, Rob Romijnders, Frances Hubis, Xiaohua Zhai, Neil Houlsby, Dustin Tran, and Mario Lucic. 2021.
Revisiting the calibration of modern neural networks. In
Proceedings of the 35th International Conference on Neural Information Processing Systems
(NIPS ’21)
. Curran Associates Inc., Red Hook, NY, USA, Article 1200, 13 pages.
Naeini et al
.
(2015)
Mahdi Pakdaman Naeini, Gregory Cooper, and Milos Hauskrecht. 2015.
Obtaining well calibrated probabilities using bayesian binning. In
Proceedings of the AAAI conference on artificial intelligence
, Vol. 29.
Platt et al
.
(1999)
John Platt et al
.
1999.
Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods.
Advances in large margin classifiers
10, 3 (1999), 61–74.
Rozière et al
.
(2024)
Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, et al
.
2024.
Code Llama: Open Foundation Models for Code.
arXiv:2308.12950 [cs.CL]
https://arxiv.org/abs/2308.12950
Spiess et al
.
(2024)
Claudio Spiess, David Gros, Kunal Suresh Pai, Michael Pradel, Md Rafiqul Islam Rabin, Amin Alipour, Susmit Jha, Prem Devanbu, and Toufique Ahmed. 2024.
Calibration and Correctness of Language Models for Code.
arXiv:2402.02047 [cs.SE]
https://arxiv.org/abs/2402.02047
Srivastava et al
.
(2023)
Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, et al
.
2023.
Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models.
Transactions on Machine Learning Research
(2023).
https://openreview.net/forum?id=uyTL5Bvosj
Featured Certification.
Sun et al
.
(2025)
Weisong Sun, Yun Miao, Yuekang Li, Hongyu Zhang, Chunrong Fang, Yi Liu, Gelei Deng, Yang Liu, and Zhenyu Chen. 2025.
Source Code Summarization in the Era of Large Language Models. In
2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)
. 1882–1894.
doi:
10.1109/ICSE55347.2025.00034
Wei et al
.
(2024)
Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. 2024.
Magicoder: Empowering Code Generation with OSS-Instruct.
arXiv:2312.02120 [cs.CL]
https://arxiv.org/abs/2312.02120
Wu et al
.
(2024)
Zhaofeng Wu, Linlu Qiu, Alexis Ross, Ekin Akyürek, Boyuan Chen, Bailin Wang, Najoung Kim, Jacob Andreas, and Yoon Kim. 2024.
Reasoning or Reciting? Exploring the Capabilities and Limitations of Language Models Through Counterfactual Tasks. In
Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)
. Association for Computational Linguistics, Mexico City, Mexico, 1819–1862.
doi:
10.18653/v1/2024.naacl-long.102
Xiong et al
.
(2024)
Miao Xiong, Zhiyuan Hu, Xinyang Lu, YIFEI LI, Jie Fu, Junxian He, and Bryan Hooi. 2024.
Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs. In
The Twelfth International Conference on Learning Representations
.
https://openreview.net/forum?id=gjeQKFxFpZ
Xu et al
.
(2025)
Ruiyang Xu, Jialun Cao, Yaojie Lu, Ming Wen, Hongyu Lin, Xianpei Han, Ben He, Shing-Chi Cheung, and Le Sun. 2025.
CRUXEval-X: A Benchmark for Multilingual Code Reasoning, Understanding and Execution.
arXiv:2408.13001 [cs.AI]
https://arxiv.org/abs/2408.13001
Yang et al
.
(2025)
An Yang, Anfeng Li, Baosong Yang, et al
.
2025.
Qwen3 Technical Report.
arXiv:2505.09388 [cs.CL]
https://arxiv.org/abs/2505.09388
Yin et al
.
(2025)
Yichun Yin, Wenyong Huang, Kaikai Song, et al
.
2025.
Pangu Ultra: Pushing the Limits of Dense Large Language Models on Ascend NPUs.
arXiv:2504.07866 [cs.CL]
https://arxiv.org/abs/2504.07866
Yu et al
.
(2024)
Xiao Yu, Lei Liu, Xing Hu, Jacky Wai Keung, Jin Liu, and Xin Xia. 2024.
Fight Fire With Fire: How Much Can We Trust ChatGPT on Source Code-Related Tasks?
IEEE Trans. Softw. Eng.
50, 12 (Dec. 2024), 3435–3453.
doi:
10.1109/TSE.2024.3492204
Zhang et al
.
(2024)
Dylan Zhang, Xuchao Zhang, Chetan Bansal, Pedro Las-Casas, Rodrigo Fonseca, and Saravan Rajmohan. 2024.
LM-PACE: Confidence Estimation by Large Language Models for Effective Root Causing of Cloud Incidents. In
Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering
(Porto de Galinhas, Brazil)
(FSE 2024)
. Association for Computing Machinery, New York, NY, USA, 388–398.
doi:
10.1145/3663529.3663858
Zhang et al
.
(2023)
Quanjun Zhang, Chunrong Fang, Yuxiang Ma, Weisong Sun, and Zhenyu Chen. 2023.
A Survey of Learning-based Automated Program Repair.
ACM Trans. Softw. Eng. Methodol.
33, 2, Article 55 (Dec. 2023), 69 pages.
doi:
10.1145/3631974
Zhao et al
.
(2025)
Xuandong Zhao, Zhewei Kang, Aosong Feng, Sergey Levine, and Dawn Song. 2025.
Learning to Reason without External Rewards.
arXiv:2505.19590 [cs.LG]
https://arxiv.org/abs/2505.19590
Zhu et al
.
(2025)
Jiachen Zhu, Menghui Zhu, Renting Rui, Rong Shan, Congmin Zheng, Bo Chen, Yunjia Xi, Jianghao Lin, Weiwen Liu, Ruiming Tang, Yong Yu, and Weinan Zhang. 2025.
Evolutionary Perspectives on the Evaluation of LLM-Based AI Agents: A Comprehensive Survey.
arXiv:2506.11102 [cs.CL]
https://arxiv.org/abs/2506.11102
Ziegler et al
.
(2022)
Albert Ziegler, Eirini Kalliamvakou, X. Alice Li, Andrew Rice, Devon Rifkin, Shawn Simister, Ganesh Sittampalam, and Edward Aftandilian. 2022.
Productivity assessment of neural code completion. In
Proceedings of the 6th ACM SIGPLAN International Symposium on Machine Programming
(San Diego, CA, USA)
(MAPS 2022)
. Association for Computing Machinery, New York, NY, USA, 21–29.
doi:
10.1145/3520312.3534864