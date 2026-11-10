---
title: Disentangling Task Difficulty from Run-Level Failure in Agent Failure Prediction
id: disentangling-task-difficulty-from-run-level-failure-in-agent-failure-prediction
tags:
- code-llm-confidence-positioning-d82d00
- w3-forward-citation
created: '2026-11-10T08:23:47.886500Z'
updated: '2026-11-10T08:25:31.437310Z'
source: https://arxiv.org/html/2610.05572
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:47.886020Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Decomposes pooled AUROC of agent failure predictors: more than 99.93% of
  positive-negative pairs are cross-unit; a difficulty oracle reaches AUROC up to
  0.945 while at chance within task; early run-level discrimination is weak for trajectory
  predictors, released monitors, and hidden-state probes (stronger later and for weaker
  agents). Bears on F (evaluation validity of discrimination metrics; frames as measurement)
  and on L2 probes only for agent trajectories, not code correctness.'
---

Disentangling Task Difficulty from Run-Level Failure in Agent Failure Prediction
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2610.05572v1 [cs.LG] 04 Oct 2026
Disentangling Task Difficulty from Run-Level Failure in Agent Failure Prediction
CCS:
Software and its engineering Software verification and validation
CCS:
Software and its engineering Software testing and debugging
CCS:
Computing methodologies Machine learning
Mohsen EsfandyariDoulabi
email:
mesfand@ncsu.edu
Affiliation:
North Carolina State University
,
Raleigh
,
North Carolina
,
USA
,
Lawrence Arkoh
email:
larkoh@ncsu.edu
Affiliation:
North Carolina State University
,
Raleigh
,
North Carolina
,
USA
,
Biruk Tadesse
email:
batadess@ncsu.edu
Affiliation:
North Carolina State University
,
Raleigh
,
North Carolina
,
USA
,
Vaishvi Patel
email:
vpatel34@ncsu.edu
Affiliation:
North Carolina State University
,
Raleigh
,
North Carolina
,
USA
,
Mehul Sharma
email:
msharm34@ncsu.edu
Affiliation:
North Carolina State University
,
Raleigh
,
North Carolina
,
USA
,
Marcelo d’Amorim
email:
mdamori@ncsu.edu
Affiliation:
North Carolina State University
,
Raleigh
,
North Carolina
,
USA
and
Wesley Assunção
email:
wguezas@ncsu.edu
Affiliation:
North Carolina State University
,
Raleigh
,
North Carolina
,
USA
Abstract.
Predicting whether an LLM agent will eventually fail has emerged as a promising direction for supporting intervention during agent’s run. Recent approaches report strong predictive performance, often with AUROC values between
0.85
0.85
and
0.94
0.94
. However, the predictors are typically trained combining agent’s runs (also called, trajectories or traces) from many different tasks. We hypothesized that the strong performance may come partly from recognizing that some tasks are harder than others, rather than from detecting whether a particular run is heading toward failure. This distinction matters operationally because task-level difficulty supports decisions about where to allocate computation, whereas run-level failure prediction is needed to decide whether to intervene in an ongoing trajectory. To disentangle task-level difficulty from run-level failure signals, we conducted a study to analyze benchmarks containing repeated attempts of the same task by the same LLM agent.
We separate comparisons across different agents and task units from comparisons between successful and failed runs of the same unit.
Across the evaluated corpora, pooled AUROC is dominated by comparisons across different agent–task units: more than 99.93% of the underlying positive–negative pairs are cross-unit. Accordingly, predictors that never observe the current run can achieve high pooled performance, including a difficulty oracle with AUROC up to 0.945, while remaining at chance within task. This means that strong pooled performance may be more informative for deciding where to allocate computation than for deciding whether to intervene in a particular run. In contrast, early run-level discrimination is consistently weak across trajectory predictors, published and released monitors, and hidden-state probes, although it improves later in run and is stronger for weaker agents. Consistent with this distinction, under fixed token budgets, task-level allocation outperforms abort-only strategies, while early stopping becomes beneficial only when within-task AUROC reaches roughly 0.84–0.93, far above the 0.50–0.55 range observed for early monitors.
These findings highlight that failure prediction should be evaluated not only by how accurately it predicts outcomes, but by whether the captured signal supports the deployment decision the predictor is intended to make.
Keywords:
LLM agents, failure prediction, evaluation validity, measurement,
empirical software engineering
1.
Introduction
Large Language Model (LLM)-based agents increasingly support multi-step tasks in software engineering and other domains
(
Liu et al., 2026
;
Jin et al., 2024
)
. Unlike conventional LLM applications that primarily generate a response from a fixed input context, LLM-based agents operate through multi-step interactions in which they take actions, invoke tools, and incorporate observations from the environment while attempting to complete a task
(
Yao et al., 2023
;
Yang et al., 2024
)
. This increased autonomy enables agents to solve complex problems, but it also introduces substantial execution risk. Recent studies report failure rates ranging from
41
%
41\%
to
86.7
%
86.7\%
across seven agentic frameworks
(
Cemri et al., 2025
)
. Such failures are costly because an unsuccessful run may consume considerable time, tokens, and computational resources before its eventual outcome becomes known
(
Du et al., 2026
;
Bai et al., 2026
;
Khanna, 2026
)
.
These costs have motivated growing interest in
agent failure prediction
: determining, during execution, whether an ongoing agent run is likely to fail
(
Barke et al., 2026
;
Zhang et al., 2025
;
Wang et al., 2026
)
. An accurate failure predictor could support early intervention and avoid wasting resources. For example, by terminating an unpromising execution, requesting human assistance, or changing the agent’s strategy before additional resources are consumed.
Existing work commonly formulates the prediction problem as trajectory classification
(
Vasudev et al., 2026
;
Shi et al., 2026
;
Cho et al., 2026
)
. They collect successful and failed agent trajectories, train predictors on their trajectories, and use the resulting models to estimate the failure risk of new runs while they are still in progress. These predictors are commonly evaluated using the Area Under the Receiver Operating Characteristic Curve (AUROC), which measures how well a predictor discriminates failed executions from successful ones
(
Vasudev et al., 2026
;
Cho et al., 2026
)
. Within a benchmark and evaluation condition, a common practice is to pool predictions from executions of different task instances and compute AUROC over the resulting successful and failed runs
(
Cho et al., 2026
;
Vasudev et al., 2026
;
Pham et al., 2026
)
. We refer to this aggregate measure as
pooled AUROC
. High pooled AUROC values are commonly interpreted as evidence that a predictor can identify executions that are likely to fail. However, this interpretation overlooks an important possibility: the predictor may distinguish tasks with different baseline failure rates rather than distinguish successful and failed executions of the
same task
.
This distinction matters because agent outcomes depend on both the task and the particular execution
(
Bjarnason et al., 2026
;
Krsteski and Meyer, 2026
;
Lee, 2026
)
. Some tasks may fail substantially more often than others. When runs from many tasks are pooled together, a predictor can therefore obtain a high AUROC by assigning higher failure scores to tasks with high baseline failure rates and lower scores to tasks with low baseline failure rates
(
Janes et al., 2009
;
Borkan et al., 2019
)
. Such a predictor can rank failures above successes across the benchmark even if it cannot distinguish a successful run from a failed run of the
same task
.
Evidence from prior work suggests that this possibility is realistic. A predictor of task success
before execution begins
, using only static task properties, reaches AUROC of
0.841
0.841
on held-out SWE-bench Verified instances
(
Ge et al., 2026
)
, within the range reported by systems that observe agent trajectories heavily. This does not imply that trajectories contain no useful information. Rather, it exposes an ambiguity in pooled evaluation: strong discrimination may arise from between-task differences, run-specific execution signals, or both.
Conflating task-level difficulty and run-level failure can therefore misrepresent a predictor’s suitability for runtime intervention. Task-level difficulty can help determine where to allocate computation, which LLM to use, or whether a task should be attempted. A runtime monitor must answer a different question:
given that the agent is already executing this task, does the evidence from this particular run indicate that it is heading toward failure?
The latter decision requires information that separates different outcomes of the same task.
Our study investigates how strongly the distinction between task-level difficulty and run-level failure affects the evaluation and use of agent failure predictors. Building on the distinction between pooled and conditional discrimination studied in statistics
(
Pepe, 2003
;
Janes and Pepe, 2009
)
and recent evidence of task-level confounds in agent evaluation
(
Mehtiyev and Assunção, 2026
;
Bulut, 2026
)
, we ask three questions: (RQ1) how much reported predictive performance reflects differences between tasks rather than the state of the current execution, (RQ2) whether run-specific signals are available early enough to support intervention, and (RQ3) whether separating these signals changes the deployment decisions suggested by failure predictors. To answer these questions, we exploit repeated agent executions, in which a fixed agent configuration attempts the same task multiple times. Because the task and agent remain constant while the execution varies, successful
and failed attempts within the same model–task unit provide a setting for isolating run-level discrimination from between-unit differences. We analyze repeated-attempt corpora from SWE-agent
(
Yang et al., 2024
)
, SWE-rebench
(
Badertdinov et al., 2025
)
, LiveClawBench
(
Long et al., 2026
)
, and Latent Programming Horizons
(
Silva et al., 2026
)
, spanning different agent scaffolds, models, and domains. Empirically, we decompose pooled AUROC into within-unit and cross-unit comparisons; compare run-blind baselines with trajectory-based predictors, published and released monitoring systems, and hidden-state probes at online-computable execution prefixes; and measure within-task discrimination while holding the task and acting model fixed. Finally, we evaluate the practical consequences of these signals through replay experiments under fixed token budgets, comparing task-level resource allocation, run-level aborting, and their combination.
Our results reveal a consistent progression across the three research questions. For RQ1, we find that pooled AUROC is dominated by cross-unit comparisons: more than 99.93% of the underlying positive–negative pairs compare different model–task units, allowing a difficulty oracle to reach pooled AUROC of 0.945 while remaining at 0.500 within task. For RQ2, early run-level discrimination is consistently weak across trajectory-based predictors, published and released monitoring systems, and hidden-state probes, although the signal becomes stronger later in execution and is more pronounced for weaker agents. For RQ3, this distinction changes the practical value of prediction: under fixed token budgets, task-level allocation outperforms abort-only strategies, while run-level monitoring becomes beneficial only when within-task AUROC reaches roughly 0.84–0.93, far above the 0.50–0.55 range observed for early monitors. These results show that high aggregate predictive performance can reflect task-level difficulty without implying effective runtime failure detection, and that separating these signals is necessary to determine which decisions they can support.
Our study makes three main contributions:
•
A measurement framework for agent failure prediction.
We separate task-level difficulty from run-level failure prediction by decomposing pooled AUROC into within-unit and cross-unit components and by evaluating within-task discrimination on repeated executions.
•
An empirical characterization of run-level failure signals.
Across multiple benchmarks, models, agent scaffolds, trajectory predictors, published monitoring systems, and hidden-state probes, we assess when run-specific information becomes available and whether it is strong enough to support intervention.
•
Decision-oriented guidance for evaluation and deployment.
We connect predictive performance to operational use by comparing task-level allocation with run-level aborting under fixed compute budgets, yielding practical guidance for researchers, tool builders, and practitioners on how failure predictors should be evaluated and used.
Taken together, our contributions change how failure-prediction performance should be interpreted for LLM agents. A high pooled AUROC can be useful evidence that failures are associated with predictable differences across tasks, but it does not by itself establish that a monitor can recognize which particular execution of a task will fail. The distinction matters operationally: task-level information supports decisions about
where to spend computation
, whereas run-level information supports decisions about
whether to stop the execution currently in progress
.
2.
Motivating Example
Consider two SWE-bench Verified tasks from Django, each attempted ten times by the same agent and model. This gives
20
20
runs in total. The agent solves
django-10914
nine times but solves
django-10973
only once. Now consider a predictor that never observes the trajectory and simply assigns each task its observed failure rate:
0.1
0.1
for every run of the first task and
0.9
0.9
for every run of the second. Evaluated across all
20
20
runs, this predictor achieves AUROC
0.900
0.900
. In either task, however, its AUROC is exactly
0.500
0.500
because every attempt at the same task receives the same score. The predictor therefore distinguishes which task is harder, but not which particular run will fail.
At benchmark scale, this distinction becomes substantial: in C4-L (presented in Table
1
), only about
0.07
%
0.07\%
of the comparisons underlying pooled AUROC come from runs of the same task. This helps explain why strong pooled performance can coexist with weak run-level discrimination, and why task-level information may be more useful for allocating computation than for deciding whether to abort the current run.
3.
Related Work
Research on agent failure prediction spans three questions: what makes a task likely to fail before execution, what an ongoing trajectory reveals about its eventual outcome, and whether acting on a prediction improves system behavior. These questions rely on different information and support different decisions. Several runtime predictors evaluate executions from multiple tasks together
(
Cho et al., 2026
;
Vasudev et al., 2026
;
Wang et al., 2026
)
, potentially mixing task-level difficulty with run-specific failure signals. We review these lines of work to clarify what existing evaluations establish about run-level monitoring.
3.1.
Task difficulty as a source of predictive performance
Pre-execution prediction is well established in software engineering, from defect-risk estimation using static software features
(
EsfandyariDoulabi et al., 2025
)
to LLM reliability analyses showing sensitivity to task difficulty and repeated evaluation
(
Sun et al., 2026
)
. More directly, Ge et al.
(
Ge et al., 2026
)
estimate agent task difficulty using Item Response Theory (IRT) and task features. Their model reaches AUROC
0.841
0.841
on held-out SWE-bench Verified tasks, while a problem-statement-only variant reaches
0.786
0.786
, showing that substantial discrimination is possible before observing the current execution. Krsteski and Meyer
(
Krsteski and Meyer, 2026
)
similarly predict IRT-derived difficulty across 17 agentic benchmarks and show that aggregate AUC can remain high even when task-level scores do not distinguish individual outcomes. Our work, in contrast, asks whether high aggregate failure-prediction performance also captures run-specific information within repeated attempts of the same model–task pair, and whether task-level and run-level signals support different deployment decisions.
Mehtiyev and Assunção
(
Mehtiyev and Assunção, 2026
)
further show that trajectory-based associations depend on what is held fixed. Across 9,374 coding-agent trajectories, failed runs are longer when outcomes are compared within an agent, whereas the relationship often reverses when different agents are compared on the same task. Their results highlight the importance of conditioning when interpreting trajectory-level associations. We extend this idea by holding both the acting model and task fixed, allowing direct measurement of discrimination between successful and failed executions of the same model–task unit.
Bulut
(
Bulut, 2026
)
provides the closest measurement precedent to
our study. In LLM reasoning trajectories, Bulut shows that pooled
correctness-prediction AUROC can largely reflect problem difficulty rather
than attempt-specific information, motivating question-only baselines and
within-problem evaluation. Our work studies the analogous issue in runtime
failure prediction for tool-using LLM agents. We evaluate repeated
model–task executions across multiple agent benchmarks, behavioral
predictors, published and released monitoring systems, and hidden-state
probes, and then examine whether task-level and run-level information support
different deployment decisions under fixed compute budgets.
3.2.
Failure prediction during agent execution
Recent systems predict eventual success or failure from partial or complete agent trajectories. Cho et al.
(
Cho et al., 2026
)
abstract trajectories into finite-state representations and report full-trajectory AUROC of
0.941
0.941
on Tau2-Bench telecom and
0.799
0.799
on SWE-agent. Shi et al.
(
Shi et al., 2026
)
train predictors from partial trajectories and report 13–26% fewer execution steps while maintaining high prediction accuracy. Ruan et al.
(
Ruan et al., 2026
)
instead use hidden-state probes to trigger early aborts, substantially reducing generated tokens on TextCraft and WebShop.
Wang et al.
(
Wang et al., 2026
)
propose FailFast–RestartSmart, which predicts failure from partial trajectories and restarts unpromising runs, reducing token usage by 14.6–20.4% at a 5% false-positive rate. Their training objective includes successful–failed pairs from the same task to control instance difficulty. Our study addresses a complementary evaluation question: how much of a monitor’s measured discrimination remains when successful and failed executions are compared within the same model–task unit.
3.3.
Evaluation metrics and deployment decisions
Raghu et al.
(
Raghu et al., 2026
)
show that AUROC does not assess whether predicted success probabilities remain meaningful across trajectory prefixes and propose a trajectory proper score. Their concern is calibration across time; ours is complementary. We instead ask what source of variation produces the observed discrimination by separating comparisons across model–task units from comparisons between successful and failed executions of the same unit. Prediction quality also does not guarantee useful intervention. Vasudev et al.
(
Vasudev et al., 2026
)
show that a critic with strong offline failure-prediction performance can reduce task success when interventions disrupt trajectories that would otherwise succeed. This motivates evaluating monitors not only by predictive performance, but also by whether the captured signal supports the intended deployment decision.
3.4.
Synthesis and Research Gap
Taken together, prior work shows that task difficulty is predictable, trajectories can contain failure-related information, and prediction-guided intervention can help or harm depending on how that information is used. What remains unclear is whether strong aggregate failure-prediction performance reflects task/model difficulty or genuine discrimination between successful and failed executions of the same model–task unit. We address this gap by decomposing pooled AUROC into within-unit and cross-unit components, evaluating predictors at online-computable prefixes, and testing whether run-level signals improve decisions under a fixed compute budget.
4.
Study Design
Following the Goal–Question–Metric (GQM) framework
(
Basili et al., 1994
)
, the
goal
of our study is to analyze failure prediction for LLM agents
for the purpose of
understanding what reported predictive performance captures and whether the captured information supports useful deployment decisions,
with respect to
the distinction between task-level difficulty and run-level failure,
from the perspective of
researchers, tool builders, and practitioners,
in the context of
repeated-attempt agent benchmarks. We define a unit as a
(
model
,
task
)
(\text{model},\text{task})
pair. We use
within-task AUROC
as shorthand for discrimination within a fixed model–task unit, so both the task and acting model are held fixed. The following sections present the research questions (RQs) and details of each step of our study.
Figure
1
summarizes the study design and the relationship between the three research questions.
4.1.
Research Questions
The gaps observed in related work motivate three RQs:
RQ1
(
Estimand
)
What does pooled failure-prediction
AUROC measure in benchmarks that record repeated attempts?
We examine the contributions of within-unit and cross-unit comparisons
and assess how much pooled discrimination is achievable without
observing the current execution.
RQ2
(
Run-level signal
)
How much run-specific
information is available at online-computable prefixes, across
predictors, models, corpora, and hidden-state probes?
We compare successful and failed attempts with the task and model
held fixed to establish the strength and timing of run-level
discrimination.
RQ3
(
Deployment
)
Does separating task-level
from run-level discrimination change intervention and
resource-allocation conclusions?
We compare task allocation, trajectory-triggered aborting, and their
combination under fixed token budgets, and examine when monitoring
provides additional value.
Main corpora
C1
SWE-agent 3 LLMs
C2
SWE-rebench 1 LLM
C3
LiveClawBench 17 LLMs
C4
Latent Prog. Horizons
C4
(hidden states) 2 LLMs
Repeated attempts of a unit
u
=
(
model
,
task
)
u=(\text{model},\text{task})
unit
u
u
unit
v
v
same-unit comparisons
→
\rightarrow
A
within
A_{\mathrm{within}}
cross-unit comparisons
→
\rightarrow
A
cross
A_{\mathrm{cross}}
success
failure
A
pool
=
w
​
A
within
+
(
1
−
w
)
​
A
cross
A_{\mathrm{pool}}=w\,{\color[rgb]{0,0.4037,0.292}A_{\mathrm{within}}}+(1-w)\,{\color[rgb]{0.4805,0.2836,0.3938}A_{\mathrm{cross}}}
,
w
w
= share of same-unit pairs.
A
within
A_{\mathrm{within}}
asks
which run of this task fails
;
A
cross
A_{\mathrm{cross}}
can reflect differences in baseline difficulty across units. A run-blind score is constant within
a unit, so
A
within
=
0.5
A_{\mathrm{within}}=0.5
.
External scope check:
τ
2
\tau^{2}
-bench
RQ1
⋅
\cdot
Estimand
RQ2
⋅
\cdot
Run-level signal
RQ3
⋅
\cdot
Deployment
What does pooled AUROC measure?
Run-blind predictors (e.g., difficulty oracle) vs. trajectory predictors
Measures:
w
w
,
A
pool
A_{\mathrm{pool}}
,
A
within
A_{\mathrm{within}}
Is run-specific signal available early?
Behavioral predictors
Published and released monitors
Hidden-state probes (C4)
Measure:
A
within
A_{\mathrm{within}}
after turn
k
k
How should the signal be used?
Task-level allocation
Run-level aborting
Allocation + monitoring
Measure:
tasks solved under a fixed token budget (replay)
observed:
k
k
turns
final
T
T
unknown
Figure 1.
Overview of the study design.
Repeated attempts within fixed model-task units allow pooled AUROC to be separated into
same-unit (
A
within
A_{\mathrm{within}}
)
and
cross-unit (
A
cross
A_{\mathrm{cross}}
)
discrimination. We use this distinction to examine what pooled failure prediction measures, when run specific signal emerges, and how the resulting information supports deployment decisions.
4.2.
Corpora
The behavioral analyses of our study use three public corpora with repeated attempts and permissive licences. They differ in benchmark, scaffold, model family, domain, and failure rate. Table
1
summarizes their repeat structure. Failure rate is the fraction of trajectories labelled as failures; a mixed unit contains at least one success and one failure; and the number of within-unit positive–negative pairs is
∑
u
|
S
u
|
​
|
F
u
|
\sum_{u}|S_{u}||F_{u}|
.
Observed mixedness depends on the number of attempts recorded for a unit. For latent success probability
q
q
and
r
r
attempts, the probability of observing both outcomes is
1
−
q
r
−
(
1
−
q
)
r
.
1-q^{r}-(1-q)^{r}.
Thus, the mixed-outcome rates in Table
1
describe the observed repeat structure rather than intrinsic task flakiness.
Table 1.
Corpora used in the study. C1–C3 support the main behavioral analyses, while C4-L and C4-Q support the hidden-state analyses. Mixed-outcome is the share of units containing both a successful and a failed run.
C1
C2
C3
C4-L
C4-Q
Source
SWE-agent
(
Yang et al., 2024
)
SWE-rebench
(
Badertdinov et al., 2025
)
LiveClawBench
(
Long et al., 2026
)
Latent Programming Horizons
(
Silva et al., 2026
)
Scaffold
SWE-agent
OpenHands
OpenClaw
–
–
Trajectories
80,036
67,074
6,834
5,000
5,000
Tasks
3,591
6,306
134
500
500
Model(s)
3 (Llama-3 8B–405B)
Qwen3-Coder-480B
17
Laguna-XS.2
Qwen3.6-35B-A3B
Attempts/task
–
–
–
10
10
Failure rate
0.833
0.521
0.582
–
–
Mixed-outcome
22.0%
27.6%
21.9%
40.6%
34.8%
Same-unit weight
w
w
2.5
×
10
−
4
2.5{\times}10^{-4}
3.4
×
10
−
5
3.4{\times}10^{-5}
8.8
×
10
−
5
8.8{\times}10^{-5}
–
–
Mixed units
926
1,741
500
203
174
Within-unit pairs
220,055
38,576
1,000
–
–
C1 contains SWE-agent coding trajectories from three Llama-3 models. C2 was generated with OpenHands v0.54.0 using a single Qwen3-Coder-480B model; its
6,306
6{,}306
tasks span
1,823
1{,}823
repositories. C3 contains trajectories from
17
17
models across ten domains. Of its
6,834
6{,}834
recorded trajectories,
6,727
6{,}727
can be parsed into
2,269
2{,}269
units;
488
488
of the
500
500
mixed units remain parseable and are used for analyses requiring parsed trajectories.
C3 additionally provides difficulty tiers and domain labels assigned by the benchmark authors rather than derived from our outcomes. Failure rates increase from
0.313
0.313
to
0.710
0.710
to
0.962
0.962
across the three tiers, consistent with their intended ordering. We therefore use these labels as outcome-independent task-level information available before execution.
The hidden-state analysis requires access to the model that produced each trajectory, which is unavailable for most public agent corpora. We therefore use the
Latent Programming Horizons
corpus
(
Silva et al., 2026
)
as C4. It contains SWE-bench trajectories from two open mixture-of-experts models:
Laguna-XS.2
(C4-L) and
Qwen3.6-35B-A3B
(C4-Q). Both provide ten attempts for each of the same 500 SWE-bench tasks.
Laguna-XS.2
has
40
40
layers with
d
model
=
2048
d_{\mathrm{model}}=2048
. Each C4 record stores the exact token identifiers consumed by the model and message offsets, allowing us to replay the original token sequence directly rather than reconstructing the chat template.
For hidden-state probing, C4-L retains
142
142
mixed units after applying a
16,000
16{,}000
-token eligibility criterion, while C4-Q retains all
174
174
mixed units. The threshold is imposed for activation-memory feasibility rather than as a modelling choice. Runs above the threshold are excluded whole rather than truncated, preventing the observed prefix from becoming a function of final trajectory length.
4.3.
Evaluation Metrics
We evaluate predictors using pooled and within-task AUROC. Pooled AUROC,
A
pool
A_{\mathrm{pool}}
, compares successful and failed runs drawn from the full evaluation set. Within-task AUROC,
A
within
A_{\mathrm{within}}
, instead compares successful and failed runs from the same unit. For unit
u
u
, let
S
u
S_{u}
and
F
u
F_{u}
denote its successful and failed runs and let
A
u
A_{u}
be its within-unit AUROC. We define
(1)
A
within
=
∑
u
|
S
u
|
​
|
F
u
|
​
A
u
∑
u
|
S
u
|
​
|
F
u
|
.
A_{\mathrm{within}}=\frac{\sum_{u}|S_{u}||F_{u}|A_{u}}{\sum_{u}|S_{u}||F_{u}|}.
Only units containing both a success and a failure contribute to
A
within
A_{\mathrm{within}}
. A predictor that is constant within a unit therefore receives
A
within
=
0.5
A_{\mathrm{within}}=0.5
.
Pooled AUROC decomposition.
The positive–negative pairs underlying pooled AUROC can be partitioned into same-unit and cross-unit pairs. Let
w
w
denote the fraction of all such pairs that come from the same unit. Then
(2)
A
pool
=
w
​
A
within
+
(
1
−
w
)
​
A
cross
,
w
=
∑
u
P
u
​
N
u
(
∑
u
P
u
)
​
(
∑
u
N
u
)
,
A_{\mathrm{pool}}=wA_{\mathrm{within}}+(1-w)A_{\mathrm{cross}},\qquad w=\frac{\sum_{u}P_{u}N_{u}}{(\sum_{u}P_{u})(\sum_{u}N_{u})},
where
P
u
P_{u}
and
N
u
N_{u}
are the numbers of failed and successful runs in unit
u
u
, respectively, and
A
cross
A_{\mathrm{cross}}
is AUROC over cross-unit pairs. We use
w
w
to quantify how much of pooled AUROC is determined by comparisons within the same model–task unit.
Cross-unit pairs need not be cross-task: they may differ in task, acting model, or both. For single-model corpora (C2, C4-L, and C4-Q), units and tasks coincide. For the multi-model corpora C1 and C3, we report the same-unit weight and separately examine task- and model-level contributions rather than equating cross-unit variation with task variation. For the comparison of task-history and trajectory-based predictors, we additionally report Brier score and log loss to assess probabilistic prediction quality
(
Gneiting and Raftery, 2007
)
; lower values are better.
4.4.
Prediction Conditions
We vary the information available to each predictor, separating information that is constant within a unit from information that changes across repeated attempts.
Run-Blind Predictors
Our main control is a predictor that never observes the current trajectory. The
difficulty oracle
assigns each run the failure rate of its unit. In multi-model corpora, this oracle reflects the baseline difficulty of the model-task unit and may therefore contain both task- and model-level variation. For pooled evaluation, that rate is computed with the current run left out so that its own outcome cannot predict itself. For within-task evaluation we use the ordinary unit mean, which is constant across runs and therefore yields
A
within
=
0.5
A_{\mathrm{within}}=0.5
.
We also evaluate deployable run-blind predictors that do not use target-unit outcome history. On C1 and C2, a pre-execution predictor uses issue-text TF-IDF features
(
Salton and Buckley, 1988
)
and repository identity, with tasks held out across folds. On C3, we evaluate three run-blind conditions: task metadata (difficulty tier and domain), acting-model identity, and their combination. All are available before execution.
Trajectory Predictors
Trajectory predictors use the first
k
k
turns of the current execution. Behavioral features include turn counts, message and observation lengths and their dispersion, error tokens, repetition, tool diversity, and TF-IDF text features
(
Salton and Buckley, 1988
)
. We fit logistic regression
(
Cox, 1958
)
and gradient boosting
(
Friedman, 2001
)
and generate out-of-fold predictions using
GroupKFold
(
Pedregosa et al., 2011
)
grouped by task. Thus, a task never appears in both training and test portions of a fold. We compute
A
pool
A_{\mathrm{pool}}
and
A
within
A_{\mathrm{within}}
from the same cross-fitted predictions so that the estimands differ only in the pairs being compared. C3 supports an additional decomposition of task history and current-run information.
M
0
M_{0}
uses only the unit’s failure rate estimated from its other runs,
M
1
M_{1}
uses only the current trajectory, and
M
2
M_{2}
combines both. The difference between
M
2
M_{2}
and
M
0
M_{0}
therefore measures what the current trajectory adds once outcomes from previous attempts on the same model–task unit are known.
Published and Released Systems
To determine whether our findings are specific to our predictors, we also evaluate systems developed independently of our pipeline. We reimplement Automata
(
Cho et al., 2026
)
because it reports the highest pooled AUROC in our survey (
0.941
0.941
) and is evaluated on SWE-agent (C1), allowing a same-corpus comparison. We first verify that our reconstruction matches its published SWE-agent result (
0.799
0.799
) on complete trajectories, then evaluate fixed prefixes under both
A
pool
A_{\mathrm{pool}}
and
A
within
A_{\mathrm{within}}
. The reconstruction uses the published activity-abstracted automaton with gradient boosting; additional implementation checks are reported in the supplementary material
(
Anonymous, 2026
)
.
We also evaluate released systems directly. EarlyEval
(
Shi et al., 2026
)
is particularly relevant because it targets early failure prediction, reports
13
13
–
26
%
26\%
fewer execution steps at
89
89
–
97
%
97\%
accuracy, and requires no reconstruction. We run its released features on the pre-registered five-fold C2 split, where each of the
6,306
6{,}306
instances appears in test data once. Its step-
0
0
checkpoint predicts before the agent acts, providing a direct measure of pre-execution discrimination. We additionally evaluate the released one-class monitor of
Dubey (2026)
on the same C2 folds and run EarlyEval on C1’s three Llama-3 models to test whether the pattern extends across acting models.
4.5.
Hidden-State Probes
Observable trajectory features may miss outcome information encoded internally by the acting model. C4 allows us to test this possibility because its weights and exact trajectory tokens are available for replay.
We cut each trajectory after assistant turn
k
∈
{
1
,
3
,
5
,
10
}
k\in\{1,3,5,10\}
and extract the hidden state of the last emitted token from layers
{
10
,
20
,
30
,
40
}
\{10,20,30,40\}
, sampling the 40-layer model at approximately quarter-depth intervals. Each retained prefix is replayed in full. We fit an
ℓ
2
\ell_{2}
-regularized linear logistic probe to the raw
2048
2048
-dimensional activation. The probe is deliberately linear so that we test whether outcome information is directly recoverable from the representation without introducing substantial additional predictive capacity.
Each probe uses
GroupKFold
grouped by task. Regularization strength is selected with a nested
GroupKFold
inside each training fold and never using test data. We compare these probes with a three-feature length baseline consisting of absolute token position, its logarithm, and assistant-turn count.
We validate the probing pipeline in four ways: (1) we verify model loading with teacher-forced accuracy; (2) replay stored token identifiers directly; (3) compare the within-task AUROC estimator with an independent implementation to
10
−
9
10^{-9}
agreement; and (4) evaluate positive and negative controls using an outcome-encoding feature, Gaussian noise, and shuffled labels. Numerical validation results are reported with the probe results.
4.6.
Prefix Definition and Leakage Control
All trajectory-based predictors satisfy the same deployment constraint: they may use only information available when the prediction is made. In particular, final trajectory length is unknown while an execution is still running.
We therefore define checkpoints by absolute turn count rather than by a fraction of the completed trajectory. Fractional checkpoints depend on final length
T
T
and therefore introduce information unavailable online. For Automata, we evaluate both its original fractional checkpoint and deployment-valid checkpoints based on observed turns and tokens, allowing us to quantify the effect of this leakage.
Later checkpoints create a separate selection issue because runs that terminate early disappear from evaluation. To distinguish increasing predictive signal from changing cohort composition, we additionally evaluate a fixed C1 cohort containing only trajectories that reach at least ten turns, so the same runs are compared across early checkpoints.
4.7.
Analysis by Research Question
RQ1: Pooled versus Within-Unit Evaluation
RQ1 first computes the same-unit pair weight
w
w
from Section
4.3
, which measures the share of positive–negative comparisons underlying pooled AUROC that come from the same unit. We then evaluate the difficulty oracle, deployable pre-execution predictors, and the C3 run-blind conditions under both
A
pool
A_{\mathrm{pool}}
and
A
within
A_{\mathrm{within}}
, comparing them with trajectory-based predictors. This determines how much pooled discrimination can be obtained without observing the current execution and how much remains once comparisons are restricted to repeated attempts from the same model–task unit.
RQ2: Run-Level Discrimination
RQ2 evaluates
A
within
A_{\mathrm{within}}
at online-computable prefixes for behavioral predictors, published and released systems, and hidden-state probes. On C3, the
M
0
M_{0}
,
M
1
M_{1}
, and
M
2
M_{2}
conditions quantify the incremental information provided by the current trajectory after accounting for previous outcomes from the same unit.
We additionally examine trajectory depth and acting-model capability. For depth, we use the fixed C1 cohort from Section
4.6
and evaluate a pre-registered same-unit conditional-logit ranker trained directly on within-unit comparisons. For capability, we compare within-task discrimination across C3’s
17
17
models and within same-family model pairs. Because models differ in factors other than capability, this analysis is interpreted as associative rather than causal.
RQ3: Deployment Decisions
RQ3 evaluates whether task-level and run-level information support different decisions under a fixed compute budget. We use replay so that both cost and outcome come from recorded executions. At each decision, a policy selects a task and samples uniformly with replacement from its recorded runs. The sampled run contributes its recorded cost and outcome, and solved tasks are removed from further selection. The primary outcome is the number of distinct tasks solved within the budget.
We compare round-robin, static difficulty ranking transferred from another model, and Budgeted Thompson Sampling
(
Xia et al., 2015
)
. For each cost-aware policy, the mean token cost of a task is computed once from all recorded runs of the target model and held fixed throughout replay. The static transferred ranking orders tasks by donor-model success rate divided by target model mean cost. Thompson Sampling treats each task as a Beta- Bernoulli arm and selects the task with the largest sampled success probability divided by its target-model mean cost. The uninformative prior is
Beta
⁡
(
1
,
1
)
\mathrm{Beta}(1,1)
. For transferred priors,
(3)
α
u
=
1
+
λ
​
s
u
other
,
β
u
=
1
+
λ
⁡
(
n
u
other
−
s
u
other
)
,
\alpha_{u}=1+\lambda s^{\mathrm{other}}_{u},\qquad\beta_{u}=1+\lambda\left(n^{\mathrm{other}}_{u}-s^{\mathrm{other}}_{u}\right),
where
s
u
other
s^{\mathrm{other}}_{u}
and
n
u
other
n^{\mathrm{other}}_{u}
are successful and total runs from the donor model. We use
λ
=
1
\lambda=1
on C4 and
λ
=
0.5
\lambda=0.5
on C2; neither value is selected on evaluation data, and sensitivity to
λ
\lambda
is reported in the supplementary material. Allocation results use
200
200
budget realizations per setting.
For reference, an oracle policy selects the unsolved task with the highest target-model success rate divided by target-model mean cost, with both quantities computed from the complete target run set. It therefore differs from the non-oracle policies by knowing the target task success rates in advance. Because target mean costs are computed from the complete replay corpus, the cost-aware policies are not directly deployable as cold-start policies. We use the same target-side cost data for all cost-aware policies to isolate differences in task-success information.
We then compare allocation with run-level aborting on C4-L under a held-out protocol. Tasks are split evenly into tuning and evaluation sets, giving
250
250
evaluation tasks. Abort thresholds are tuned separately for each policy and budget using only the tuning set. Final evaluation uses
150
150
paired replay trials with matched random seeds. The allocation prior is transferred from C4-Q and never uses outcomes from the replayed C4-L tasks. The aborting policy uses the cross-fitted Automata predictor at
k
=
5
k=5
. If a run is stopped, we charge only the tokens consumed through the stopping point, so a run that would later succeed incurs no further cost; this convention favors the aborting policy. We compare round-robin, static transferred ranking, Budgeted Thompson Sampling with uninformative or transferred priors, abort-only, and allocation with monitoring.
Finally, we perform a pre-registered semi-synthetic sweep over monitors with controlled
A
within
A_{\mathrm{within}}
at
k
=
5
k=5
. Using the same held-out threshold-selection procedure, we determine how much within-task discrimination is required before adding an abort decision improves the number of tasks solved. C4 is the primary replay corpus because it records token cost directly. We repeat the C2 allocation analysis using trajectory length as cost and task-level information transferred from C1.
4.8.
Statistical Analysis
Repeated runs from the same
(
model
,
task
)
(\text{model},\text{task})
unit are dependent, so the unit is our primary clustering and resampling level.
Uncertainty and between-unit variation.
We report
95
%
95\%
bootstrap confidence intervals by resampling units rather than individual runs. For the acting-model capability analysis, we instead resample models. We also report the intraclass correlation (ICC), with a finite-repeat correction for small unit sizes, as a descriptive measure of how much outcome variation lies between units
(
Shrout and Fleiss, 1979
)
.
Early-prefix tests.
At intervention-relevant prefixes, we test
H
0
:
A
within
=
0.5
H_{0}\!:A_{\mathrm{within}}=0.5
using within-unit permutation tests on out-of-fold predictions. Outcomes are shuffled within each unit while preserving its numbers of successful and failed runs. Non-significant results are interpreted as limited detectable signal rather than evidence that the true effect is exactly zero.
We additionally report the standard deviation of the permutation null,
(4)
∑
u
P
u
​
N
u
​
(
P
u
+
N
u
+
1
)
/
12
∑
u
P
u
​
N
u
,
\frac{\sqrt{\sum_{u}P_{u}N_{u}(P_{u}+N_{u}+1)/12}}{\sum_{u}P_{u}N_{u}},
where
P
u
P_{u}
and
N
u
N_{u}
are the failed and successful runs in unit
u
u
. This quantity summarizes the statistical resolution supported by the observed repeat structure.
Resolution and sensitivity analyses.
For the C4 probe, we convert uncertainty in
A
within
A_{\mathrm{within}}
into a minimum detectable effect. At
80
%
80\%
power for a two-sided test with
α
=
0.05
\alpha=0.05
, the boundary is
0.5
+
2.80
​
σ
0.5+2.80\,\sigma
. On C4-L,
σ
=
0.0193
\sigma=0.0193
gives a resolution boundary of
0.554
0.554
, allowing us to distinguish weak early signal from evidence of its complete absence.
We additionally test robustness to alternative weighting and label noise.
A
within
A_{\mathrm{within}}
is recomputed under unit-uniform macro averaging, task-demeaned scoring, minimum-repeat thresholds, and posterior-predictive weighting over units. Label-noise sensitivity is calibrated by corrupting known fractions of success labels, refitting the predictor, and measuring attenuation. Full sensitivity grids are reported in the replication package.
Predictor comparisons and multiple testing.
When predictors are evaluated on the same runs, we use shared bootstrap resamples to estimate AUROC differences and confidence intervals. Families of within-task hypothesis tests use Holm–Bonferroni correction at
α
=
0.05
\alpha=0.05
(
Holm, 1979
)
.
5.
Results
This section presents the results for RQ1 and RQ2. Section
5.1
examines what pooled AUROC measures,
Section
5.2
evaluates how much run-level signal is available during execution. RQ3, which concerns deployment decisions, is evaluated separately in Section
6
.
5.1.
RQ1: What Pooled AUROC Measures
Table 2.
C1 results at fixed-turn checkpoints (Section
4.6
).
n
n
is the number of evaluated trajectories,
A
pool
A_{\mathrm{pool}}
and
A
within
A_{\mathrm{within}}
are pooled and within-task AUROC,
gap
is their difference, and
units
is the number of mixed model–task pairs.
Condition
n
n
A
pool
A_{\mathrm{pool}}
A
within
A_{\mathrm{within}}
gap
units
k
=
2
k=2
79,929
0.6435
0.5169
+
0.127
+0.127
926
k
=
5
k=5
77,951
0.6863
0.5428
+
0.144
+0.144
920
k
=
10
k=10
63,657
0.7219
0.5987
+
0.123
+0.123
885
k
=
20
k=20
35,554
0.7463
0.6527
+
0.094
+0.094
620
Difficulty oracle
80,036
0.9454
0.5000
+
0.445
+0.445
926
Pooled AUROC is computed from failed–successful run pairs. We call a pair
same-unit
when both runs come from the same model–task pair. These same-unit pairs directly test whether a predictor can distinguish successful from failed runs of the same task and model.
These pairs make up only a tiny fraction of pooled AUROC. On C2 and C4-L, the same-unit pair weights are
3.4
×
10
−
5
3.4\times 10^{-5}
and
6.8
×
10
−
4
6.8\times 10^{-4}
, respectively. Thus, more than
99.93
%
99.93\%
of pooled comparisons are between different units. Because C2 and C4-L each contain only one acting model, different units also correspond to different tasks in these corpora. Their pooled AUROC is therefore dominated by cross-task comparisons. Figure
2
summarizes representative conditions from RQ1 and RQ2 and relates their within-task discrimination to the deployment threshold estimated in RQ3.
0.5
0.5
0.6
0.6
0.7
0.7
0.8
0.8
0.9
0.9
1.0
1.0
AUROC
chance
A
within
A_{\mathrm{within}}
needed for early aborting to improve throughput (RQ3, C4-L)
Run-blind predictors
Difficulty oracle, C2
Difficulty oracle, C1
Task history
M
0
M_{0}
, C3
Task metadata, C3
EarlyEval, step 0, C2
†
Issue text + repo, C2
Issue text + repo, C1
Predictors that read the run
Trajectory features, C1,
k
=
20
k{=}20
Trajectory features, C3
Length baseline, C4-L,
k
=
1
k{=}1
Trajectory features, C1,
k
=
2
k{=}2
Trajectory features, C2,
k
=
2
k{=}2
–
20
20
Automata (reimpl.), C1,
k
=
1
k{=}1
pooled AUROC (
A
pool
A_{\mathrm{pool}}
)
within-task AUROC (
A
within
A_{\mathrm{within}}
)
reported as a range
†
Highest step-0 pooled AUROC among the 14 EarlyEval configurations evaluated on C2.
Figure 2.
Pooled versus within-task AUROC across representative prediction conditions.
Run-blind predictors can achieve high pooled discrimination while remaining at chance within task, whereas predictors using current-run information show substantially weaker within-task discrimination. The shaded band marks the approximate within-task AUROC required for early aborting to improve throughput on C4-L.
C3 contains
17
17
acting models, so cross-unit comparisons can differ in task, model, or both. We therefore separate these sources. Task metadata alone reaches pooled AUROC
0.826
0.826
, while model identity alone reaches
0.568
0.568
. Combining the two increases AUROC only to
0.845
0.845
, so the cross-unit discrimination on C3 comes from differences between tasks rather than differences between models.
Table
2
shows what this means for prediction performance. On C1, the trajectory predictor reaches within-task AUROC
0.5169
0.5169
after two turns and
0.5428
0.5428
after five turns, while its pooled AUROC is substantially higher. In contrast, the difficulty oracle, which does not observe the current run, reaches pooled AUROC
0.9454
0.9454
but exactly
0.5000
0.5000
within task. A deployable run-blind predictor based on issue text and repository identity shows the same pattern, reaching pooled AUROC
0.598
0.598
on C1 and
0.616
0.616
on C2 while remaining at
0.500
0.500
within task.
C3 again shows the same pattern. A per-model task oracle reaches a median pooled AUROC of
0.985
0.985
, whereas trajectory predictors reach only
0.498
0.498
-
0.542
0.542
within task despite pooled AUROC of
0.732
0.732
-
0.752
0.752
. Approximately
70
%
70\%
of C3’s outcome variance lies between units, although this is descriptive rather than a bound on achievable run-level prediction.
Does the effect extend beyond coding corpora?
Because three of our four corpora are software engineering benchmarks, we test whether the same structural pattern holds on tau2-bench
(
Barres et al., 2025
)
, a non-coding tool-use benchmark. We compute two run-blind references. The
difficulty-only ceiling
is an analytic pooled-AUROC ceiling computed from each unit’s failure rate using the complete outcome table; it therefore uses the scored run’s outcome and is not a deployable predictor. Same-unit comparisons are ties, giving within-task AUROC
0.5
0.5
. The
leave-one-out oracle
instead scores each run using the failure rate of the unit’s other runs; units with only one run fall back to the global failure rate.
At the domain level, across four domains,
2,708
2{,}708
units, and
10,832
10{,}832
runs, mixed-outcome rates (
28.9
%
28.9\%
–
40.8
%
40.8\%
), same-unit weights (
2.2
×
10
−
4
2.2\times 10^{-4}
–
1.6
×
10
−
3
1.6\times 10^{-3}
), and difficulty-only ceilings (
0.941
0.941
–
0.976
0.976
) are comparable to those in our coding corpora. For a finer-grained analysis, we form
26
26
cells defined by domain, acting model, and agent configuration and retain the
18
18
cells with at least
30
30
mixed-outcome units. The retained cells cover retail, telecom, and telecom-workflow; all airline cells fall below this threshold. Across these
18
18
cells, difficulty-only ceilings range from
0.927
0.927
to
0.975
0.975
(median
0.954
0.954
), while leave one-out oracle AUROCs range from
0.752
0.752
to
0.901
0.901
(median
0.855
0.855
).
Answer to RQ1.
Pooled AUROC is dominated by comparisons between different model–task units. In our corpora, same-unit comparisons contribute no more than
6.8
×
10
−
4
6.8\times 10^{-4}
of the pair mass. As a result, a predictor can achieve high pooled AUROC by identifying difficult tasks without distinguishing successful from failed runs of the same task. This is visible in the difficulty oracle, which reaches pooled AUROC
0.9454
0.9454
on C1 while remaining at chance (
0.5000
0.5000
) within task. Pooled AUROC therefore does not by itself establish run-level failure discrimination.
5.2.
RQ2: Run-Level Information at Deployable Prefixes
Trajectory-Based Predictors
We first measure the incremental value of the current trajectory using the predictors from Section
4.4
. On C3, with
6,727
6{,}727
runs and
2,269
2{,}269
units,
M
0
M_{0}
achieves pooled AUROC, Brier score, and log loss of
0.894
0.894
,
0.103
0.103
, and
0.350
0.350
; the corresponding values are
0.726
0.726
,
0.211
0.211
, and
0.606
0.606
for
M
1
M_{1}
, and
0.923
0.923
,
0.103
0.103
, and
0.340
0.340
for
M
2
M_{2}
. Thus, the task-level predictor alone already falls within the published AUROC range of
0.85
0.85
–
0.94
0.94
.
Because
M
0
M_{0}
uses previous attempts from the same unit, adding the full current trajectory increases pooled AUROC by only
0.029
0.029
, improves log loss by
0.0101
0.0101
, and changes Brier score by only
+
0.0007
+0.0007
. Most of the gain therefore comes from ranking rather than probability estimation. Within task,
M
0
M_{0}
is
0.5
0.5
by construction, while trajectory features alone reach
0.587
0.587
; a within-task score for
M
2
M_{2}
is not identifiable under leave-one-out task scoring.
C2 provides the clearest null result. Across
67,074
67{,}074
trajectories from
1,823
1{,}823
repositories, within-task AUROC remains between
0.4935
0.4935
and
0.5014
0.5014
from two to twenty turns, with all intervals covering
0.50
0.50
. Median unit AUROC is exactly
0.500
0.500
, and only
46
%
46\%
–
48
%
48\%
of units exceed chance. In contrast, pooled AUROC remains
0.660
0.660
–
0.672
0.672
, yielding a pooled–within gap of
+
0.16
+0.16
to
+
0.18
+0.18
, while the difficulty oracle reaches
0.974
0.974
.
C1 behaves differently: within-task AUROC increases from
0.517
0.517
to
0.653
0.653
, whereas C2 remains near chance (
0.494
0.494
–
0.497
0.497
). Re-running C1 with C2’s eight features changes the curve by at most
0.035
0.035
, suggesting that feature choice does not explain the difference. After Holm correction, no permutation test rejects the null that within-task AUROC equals
0.5
0.5
; C3 has one nominal result at five turns (
p
=
0.027
p=0.027
), but it does not survive correction. Nevertheless, C3’s task-metadata predictor exceeds the trajectory predictor by
+
0.134
+0.134
pooled AUROC (
[
+
0.120
,
+
0.148
]
[+0.120,+0.148]
), showing that pooled evaluation can favor a predictor with no run-level discrimination.
Hidden-State and Length Signals
We test whether hidden states contain run-specific failure information using cross-fitted probes on C4. The signal remains weak: mean within-task AUROC is
0.509
0.509
on C4-Q, with only one configuration reaching
0.551
0.551
after Holm correction, and
0.513
0.513
on C4-L, where no configuration is significant.
At the same time, hidden states strongly encode trajectory length (
R
2
R^{2}
up to
0.98
0.98
) and repository identity (AUROC up to
1.00
1.00
). Control experiments confirm that the probing pipeline can recover genuine signal: an outcome-encoding feature reaches AUROC
1.000
1.000
, while noise and shuffled labels remain near chance. Thus, the weak within-task results are not explained by an incapable probe. This contrasts with recent evidence that hidden-state probes can predict eventual failure from the first interaction round
(
Ruan et al., 2026
)
. Our findings are consistent with Bulut
(
Bulut, 2026
)
, whose main reconstruction shows that strong pooled hidden-state prediction drops to near-chance performance after conditioning on problem identity. Together, these results suggest that early hidden-state predictability can reflect task or problem difficulty rather than run-specific outcome information.
1
3
5
10
0.5
0.5
0.55
0.55
0.6
0.6
0.65
0.65
0.7
0.7
0.75
0.75
chance
+
0.071
+0.071
+
0.093
+0.093
+
0.055
+0.055
+
0.029
+0.029
Observed assistant turns
k
k
AUROC
Length baseline, pooled
Best activation probe, pooled
Length baseline, within-task
Figure 3.
Length baseline versus activation probe on C4-L.
Figure
3
makes this distinction especially clear. Across one, three, five, and ten turns, the three-feature length baseline exceeds the best
2048
2048
-dimensional activation probe in pooled AUROC by
+
0.071
+0.071
,
+
0.093
+0.093
,
+
0.055
+0.055
, and
+
0.029
+0.029
, respectively, yet achieves only
0.502
0.502
–
0.503
0.503
within-task AUROC. Extending the observation of
Mehtiyev and Assunção (2026)
, trajectory length therefore remains strongly predictive in pooled evaluation while providing essentially no within-task discrimination once both the acting model and task are fixed. A non-significant result does not imply zero signal, so we quantify the resolution of C4-L. Across
142
142
mixed units, the bootstrap standard error is
0.0193
0.0193
. At
80
%
80\%
power, effects of about
0.054
0.054
are detectable, allowing us to rule out within-task AUROC values of roughly
0.554
0.554
or higher while leaving smaller effects such as
0.53
0.53
possible. The pooled–within gap is
+
0.107
+0.107
with a
90
%
90\%
interval of
[
+
0.046
,
+
0.165
]
[+0.046,+0.165]
. The pattern is also stable under alternative weighting schemes and plausible label noise: C1 remains above chance, C2 remains near chance, and the observed mislabelling rate is insufficient to hide effects near
0.60
0.60
or explain the pooled–within gap. Thus, modest run-level signal cannot be excluded, but strong early discrimination is inconsistent with the observed data.
Published and Released Monitors
To test whether stronger existing methods recover run-level signal that our predictors miss, we first reimplement Automata. On SWE-agent, the original work reports pooled AUROC
0.799
0.799
, while our reconstruction reaches
0.806
0.806
. Despite reproducing the published result, early within-task discrimination remains weak: at one turn, Automata reaches
0.507
0.507
within-task AUROC versus
0.565
0.565
pooled.
We also find that fractional checkpoints introduce look-ahead leakage because they depend on final trajectory length. At the
25
%
25\%
checkpoint, Automata reaches
0.6297
0.6297
, compared with
0.5658
0.5658
at a fixed-turn checkpoint observing a similar number of turns. Final trajectory length alone reaches
0.6138
0.6138
, while fixed turn and token checkpoints yield similar scores (
0.5658
0.5658
and
0.5710
0.5710
), indicating that much of the fractional-checkpoint gain comes from leaked length information. To rule out implementation effects, we next evaluate released systems directly. On C2, EarlyEval reaches pooled AUROC up to
0.72
0.72
before the agent acts, while within-task AUROC is exactly
0.500
0.500
across all model–fold combinations. After execution begins, within-task AUROC across
14
14
variants remains
0.49
0.49
–
0.52
0.52
after one step and
0.45
0.45
–
0.52
0.52
through five steps. Even at run end, within-task AUROC stays below 0.58 while pooled AUROC reaches
0.77
0.77
, with 99.9% of comparisons being cross-unit.
The released one-class monitor of
Dubey (2026)
likewise shows weak transfer on C2, with pooled AUROC of
0.44
0.44
–
0.55
0.55
through thirty steps. Its later signal is modest, reaching pooled AUROC
0.58
0.58
–
0.60
0.60
and within-task AUROC
0.55
0.55
–
0.57
0.57
. EarlyEval on C1 again shows stronger run-level signal than on C2. Pre-run within-task AUROC is
0.500
0.500
, rising to
0.49
0.49
–
0.56
0.56
after one step and
0.50
0.50
–
0.57
0.57
after five. Most mixed test units, however, come from one model, and later checkpoints contain too few units for reliable interpretation.
When Does Run-Level Signal Emerge?
Two factors explain much of the variation across corpora: trajectory depth and acting-model capability.
First, run-level signal increases with depth. On a fixed C1 cohort of
63,657
63{,}657
traces that all reach at least ten turns, within-task AUROC rises from
0.509
0.509
at one turn to
0.598
0.598
at ten, showing that the increase is not caused by survivor selection. Training directly for same-unit ranking improves early discrimination only modestly, reaching
0.526
0.526
,
0.535
0.535
, and
0.547
0.547
at one, three, and five turns, still far below the intervention requirements in Section
6.3
. This depth dependence helps reconcile our findings with FailFast–RestartSmart
(
Wang et al., 2026
)
, which reports effective failure-triggered termination on SWE-bench Verified but suppresses alarms during the first
20
20
steps and augments terminal supervision with intermediate test-progress signals. A similar but weaker depth-dependent pattern appears in Bulut
(
Bulut, 2026
)
: their main reconstructed hidden-state probe remains near chance within problem across checkpoints, while a post-hoc problem-centered probe recovers modest within-problem signal at later positions. Together, these results suggest that actionable run-specific information may become more available as trajectories develop, although its strength depends on the task, model, and representation.
Second, failures become less predictable as the acting model strengthens. Across C3’s
17
17
models, within-task AUROC correlates negatively with model capability (
ρ
=
−
0.662
\rho=-0.662
,
p
=
0.0038
p=0.0038
). The weakest model reaches
0.832
0.832
, whereas the two strongest reach only
0.444
0.444
and
0.490
0.490
. The same pattern appears within model families and on C1, where ten-turn AUROC decreases from
0.636
0.636
for Llama-8B to
0.569
0.569
for Llama-405B. We interpret this as an association rather than a causal effect.
These factors also help reconcile the corpora. C2’s stronger model remains near chance across depths (
0.500
0.500
–
0.504
0.504
), whereas C1’s weaker models become more predictable as trajectories develop. C4 shows the same pattern: behavioral features remain near chance at the early prefixes used by the hidden-state probes and reach
0.656
0.656
only on full trajectories. Together, the results suggest that early failures are most legible for weaker agents and become easier to detect later in execution.
Answer to RQ2.
Run-specific failure information is weak at early, online-computable prefixes across the predictors and representations we evaluate. Early within-task AUROC is
0.507
0.507
for Automata after one turn,
0.49
0.49
–
0.52
0.52
for EarlyEval after one step, and
0.509
0.509
on average for C4-Q hidden-state probes. The signal becomes stronger later in execution and is more pronounced for weaker models: on C1, within-task AUROC rises to
0.598
0.598
at ten turns, while across C3’s
17
17
models it decreases with model capability (
ρ
=
−
0.662
\rho=-0.662
). Overall, the available evidence supports weak early run-specific discrimination rather than an absence of run-level information altogether; stronger signal becomes detectable as trajectories develop.
6.
Evaluation: Deployment Decisions (RQ3)
RQ1 and RQ2 examine what failure predictors measure. This section evaluates whether that distinction affects deployment decisions. Using replay under fixed token budgets, we compare task-level allocation with run-level aborting, using recorded costs and outcomes from real executions.
1M
2.5M
5M
10M
0
0
40
40
80
80
120
120
160
160
Token budget
Distinct tasks solved
Static transferred ranking
TS + transferred
TS + transferred + tuned monitor
TS, uninformative
Tuned abort only
Round-robin
Figure 4.
Tasks solved on the 250-task C4-L split under fixed token budgets. Points average 150 paired replay trials; bars show 95% percentile intervals. Abort thresholds are tuned separately. TS denotes budgeted Thompson sampling with task information transferred from C4-Q.
6.1.
Task-Level Allocation
Task-level allocation is most valuable under tight budgets. On C4-Q, allocation solves
162.0
162.0
tasks at
2
2
M tokens, compared with
53.0
53.0
for round-robin and
172.9
172.9
for the oracle, reaching
93.7
%
93.7\%
of the oracle’s throughput (
162.0
/
172.9
162.0/172.9
).
Prior quality matters. On C2, an uninformative prior outperforms a transferred one (
52.5
52.5
vs.
46.1
46.1
tasks at
2
2
M), consistent with differences between the donor and target settings. Static transferred rankings are competitive at scarce budgets, outperforming adaptive allocation on C4-Q (
166.6
166.6
vs.
162.0
162.0
at
2
2
M) and C4-L (
55.2
55.2
vs.
51.9
51.9
at
1
1
M).
Across the
500
500
shared C4 tasks, the per-task success rates of C4-Q and C4-L are strongly correlated (Pearson
r
=
0.863
r=0.863
). The static transferred score is also strongly correlated with the oracle score (Spearman
ρ
=
0.916
\rho=0.916
), although both scores use the same target mean-cost denominator and therefore share cost information.
6.2.
Abort or Reallocate
We compare allocation and aborting on C4-L under a held-out protocol. Tasks are split evenly into tuning and evaluation sets, abort thresholds are selected separately for each budget using only the tuning set, and policies use paired replay seeds. The allocation prior is transferred from C4-Q, while the run-level monitor is the five-turn cross-fitted automaton from Section
5.2
. Aborted runs are charged only the tokens consumed through the stopping point, which favors the aborting policy. Figure
4
compares allocation and aborting across token budgets on held-out C4-L.
Adding the monitor to budgeted Thompson sampling does not improve throughput: across budgets, the paired difference ranges from
−
4.2
-4.2
to
−
0.6
-0.6
tasks, with all
95
%
95\%
intervals spanning zero. Abort-only intervention performs substantially worse than allocation, losing
17.2
17.2
–
49.0
49.0
tasks, and does not outperform round-robin despite threshold tuning. As an additional compute-control baseline, turn caps produce the same qualitative result. On C2, capped round-robin solves 15.7 tasks versus 37.9 for allocation at 2M, and adding caps to allocation lowers throughput.
6.3.
How Good Would a Monitor Have to Be
We next ask how accurate a run-level monitor must be before early stopping becomes useful. Using semi-synthetic monitors with controlled within-task AUROC at five turns, we identify when allocation plus monitoring first outperforms allocation alone.
On C4-L, improvement requires about
0.84
0.84
within-task AUROC at a
10
10
M-token budget and about
0.93
0.93
at
5
5
M. This range is shown as the shaded band in Figure
2
, highlighting the gap between the run-level discrimination achieved by the evaluated monitors and the level required for early aborting to improve throughput. When monitor errors are concentrated on harder tasks, the requirement rises to roughly
0.90
0.90
-
1.00
1.00
. On C2, even perfect discrimination does not improve throughput between
2
2
M and
10
10
M tokens and becomes beneficial only at
25
25
M. Early monitors reach only 0.50–0.55 within-task AUROC, well below the level needed for beneficial aborting.
Answer to RQ3.
Task-level information is substantially more useful for compute allocation than the measured run-level signal is for early aborting under the studied budgets. Static difficulty ranking solves up to
3.5
×
3.5\times
more tasks than round-robin, whereas adding the measured monitor changes throughput by only
−
4.2
-4.2
to
−
0.6
-0.6
tasks. Early aborting becomes useful only around
0.84
0.84
–
0.93
0.93
within-task AUROC, far above the observed range of
0.50
0.50
–
0.55
0.55
.
7.
Discussion
Implications of the findings.
Our results separate task-level predictability from run-level predictability. Pooled AUROC is dominated by cross-unit comparisons, allowing predictors that never observe the current run to achieve strong aggregate performance; for example, a task-difficulty scorer reaches
0.9454
0.9454
pooled AUROC while remaining at
0.5000
0.5000
within task. In contrast, early within-unit discrimination is consistently weak across the monitors and probes we evaluate, and the signal that does emerge tends to appear later and for weaker acting models. This distinction matters operationally: task-level information supports compute allocation, whereas run-level information is required for deciding whether to stop an ongoing execution. Under fixed token budgets, allocation outperforms abort-only strategies, while the monitor does not improve throughput.
Implications for evaluation.
Pooled AUROC alone is therefore insufficient for evaluating runtime monitors. We recommend reporting within-unit AUROC, the same-unit pair weight, and the pooled–within gap alongside the aggregate score. Evaluation checkpoints should also use only information available during execution; fractional checkpoints based on final trajectory length can leak future information and inflate performance. Finally, intervention policies should be compared against task-level allocation baselines under the same compute budget.
Scope of the conclusions.
We do not claim that trajectories contain no run-level information or that monitoring is inherently ineffective. Rather, the early signal we observe is weak, and the evaluated monitors remain far below the roughly
0.84
0.84
–
0.93
0.93
within-task AUROC at which aborting becomes beneficial in our replay. These thresholds depend on the benchmark and budget, and our deployment results are based on recorded-run replay rather than live intervention. For previously unseen tasks with no execution history, task difficulty must instead be estimated from pre execution task features, transferred from related models or settings, or learned from initial attempts. Our strongest allocation results therefore apply most directly when repeated-attempt information or transferable task difficulty estimates are available.
8.
Threats to validity
Construct Validity.
Our analyses rely on benchmark-provided outcome labels, so label errors could weaken the measured relationship between trajectory information and outcome and pull within-task AUROC toward
0.5
0.5
. We therefore test sensitivity to plausible label noise. The observed mislabelling rate is too small to explain the pooled–within gap or to hide effects around
0.6
0.6
or higher, although smaller effects remain possible.
Internal Validity.
Automata is reconstructed from its published description because the original artifacts are unavailable. We mitigate implementation differences by reproducing its published SWE-agent pooled result and by separately evaluating systems with released implementations. We also use fixed observed-turn checkpoints to avoid leakage from final trajectory length, and a fixed C1 cohort to reduce survivor effects at later checkpoints. Because models in the capability analysis differ in more than capability alone, we interpret that result as associative rather than causal.
External Validity.
Our main corpora are coding-heavy, although C3 includes non-coding domains. We therefore examine the same structural quantities on four non-coding tau2-bench domains and observe comparable patterns. This supports the broader relevance of the pooled-versus-within issue, but not the generalization of all trajectory-level findings. Hidden-state results are limited to the two open C4 models, and the deployment analysis uses replay rather than live intervention. The allocation results also apply most directly to settings with repeated attempts.
Statistical Conclusion Validity.
Within-task AUROC is defined only for mixed units, so our estimates are conditional on units containing both successes and failures. Alternative weighting schemes do not materially change the early estimates. Near-chance AUROC should also be interpreted cautiously: failure to reject
H
0
:
A
within
=
0.5
H_{0}:A_{\mathrm{within}}=0.5
does not imply that no run-level signal exists. We therefore describe the early signal as weak rather than absent and report confidence intervals, clustered resampling, within-unit permutation tests, and Holm–Bonferroni correction.
9.
Conclusion
In this paper, we examined what failure-prediction performance measures for LLM agents and whether those predictions support useful deployment decisions. Using benchmarks with repeated attempts of the same model-task unit, we separated task-level discrimination from discrimination between successful and failed runs of the same task. We evaluated run-blind baselines, trajectory predictors, hidden-state probes, and published and released failure-prediction systems, and then used replay experiments to study the consequences for compute allocation.
Our results show that strong pooled AUROC can largely reflect differences between units, and in particular differences in task difficulty, rather than information about the current run.
More than
99.93
%
99.93\%
of the positive–negative pairs underlying pooled AUROC compare runs from different units, allowing predictors that never observe the current trajectory to achieve strong pooled performance while remaining near chance within task. Early within-task discrimination is generally weak across the evaluated predictors and monitoring systems, although the signal becomes stronger later in execution and is more visible for weaker acting models.
This distinction also matters operationally. Under a fixed token budget, task-level allocation outperforms aborting runs with the evaluated monitors, and adding the monitor to an allocation policy does not improve throughput under the studied conditions. In the C4-L sensitivity analysis, within-task AUROC of approximately
0.84
0.84
–
0.93
0.93
is required before aborting becomes beneficial.
Overall, our study shows that failure-prediction evaluation should distinguish task-level predictability from run-level predictability. We recommend reporting within-task AUROC and the same-unit pair weight alongside pooled AUROC, evaluating predictors only at prefixes available during execution, and comparing run-level intervention policies against task-level allocation baselines. Doing so makes clear what information a failure predictor captures and whether that information supports the deployment decision for which the predictor is intended.
Data Availability
All code, scripts, configurations, and additional artifacts used in this study are publicly available at
(
Anonymous, 2026
)
.
References
Anonymous (2026)
Anonymous
Replication package for paper
.
Zenodo
.
External Links:
Document
,
Link
Cited by:
§4.4
,
Data Availability
.
Badertdinov
et al.
(2025)
I. Badertdinov, A. Golubev, M. Nekrashevich, A. Shevtsov, S. Karasik, A. Andriushchenko, M. Trofimova, D. Litvintseva, and B. Yangel
SWE-rebench: an automated pipeline for task collection and decontaminated evaluation of software engineering agents
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Cited by:
§1
,
Table 1
.
Bai
et al.
(2026)
L. Bai, Z. Huang, X. Wang, J. Sun, R. Mihalcea, E. Brynjolfsson, A. Pentland, and J. Pei
How do ai agents spend your money? analyzing and predicting token consumption in agentic coding tasks
.
arXiv preprint arXiv:2604.22750
.
Cited by:
§1
.
Barke
et al.
(2026)
S. Barke, A. Goyal, A. Khare, A. Singh, S. Nath, and C. Bansal
Agentrx: diagnosing ai agent failures from execution trajectories
.
arXiv preprint arXiv:2602.02475
.
Cited by:
§1
.
Barres
et al.
(2025)
V. Barres, H. Dong, S. Ray, X. Si, and K. Narasimhan
τ
2
\tau^{2}
-Bench: evaluating conversational agents in a dual-control environment
.
arXiv preprint arXiv:2506.07982
.
Cited by:
§5.1
.
Basili
et al.
(1994)
V. R. Basili, G. Caldiera, and H. D. Rombach
The goal question metric approach
.
In
Encyclopedia of Software Engineering
,
J. J. Marciniak (Ed.)
,
Vol.
1
,
pp. 528–532
.
Cited by:
§4
.
Bjarnason
et al.
(2026)
B. H. Bjarnason, A. Silva, and M. Monperrus
On randomness in agentic evals
.
arXiv preprint arXiv:2602.07150
.
Cited by:
§1
.
Borkan
et al.
(2019)
D. Borkan, L. Dixon, J. Sorensen, N. Thain, and L. Vasserman
Nuanced metrics for measuring unintended bias with real data for text classification
.
In
Companion proceedings of the 2019 world wide web conference
,
pp. 491–500
.
Cited by:
§1
.
Bulut (2026)
Y. U. Bulut
It’s the problem, not the path: budget and difficulty confounds in llm reasoning trajectories
.
arXiv preprint arXiv:2609.03436
.
Cited by:
§1
,
§3.1
,
§5.2
,
§5.2
.
Cemri
et al.
(2025)
M. Cemri, M. Z. Pan, S. Yang,
et al.
Why do multi-agent LLM systems fail?
.
In
Advances in Neural Information Processing Systems (Datasets and Benchmarks Track)
,
Note:
arXiv:2503.13657
Cited by:
§1
.
Cho
et al.
(2026)
S. Cho, F. C. Fernandez, U. Mohammed, Z. Wu, K. D. Costa, I. Wicaksono, and A. Koshiyama
Automata from agent traces: failure and next-step prediction
.
In
Second Workshop on Agents in the Wild
,
Note:
arXiv:2608.23670
Cited by:
§1
,
§3.2
,
§3
,
§4.4
.
Cox (1958)
D. R. Cox
The regression analysis of binary sequences
.
Journal of the Royal Statistical Society: Series B (Methodological)
20
(
2
),
pp. 215–232
.
External Links:
Document
Cited by:
§4.4
.
Du
et al.
(2026)
S. Du, J. Zhao, J. Shi, Z. Xie, X. Jiang, Y. Bai, and L. He
A survey on the optimization of large language model-based agents
.
ACM Computing Surveys
58
(
9
),
pp. 1–37
.
Cited by:
§1
.
Dubey (2026)
S. Dubey
Real-time detection and repair of llm agent failures
.
External Links:
2608.02464
,
Document
Cited by:
§4.4
,
§5.2
.
EsfandyariDoulabi
et al.
(2025)
M. EsfandyariDoulabi, A. E. Doulabi, and J. Khaligh
Adaptive ensemble learning for software defect prediction: a dynamic weighted hybrid model using svm, dt, and anfis-pso
.
In
2025 15th International Conference on Computer and Knowledge Engineering (ICCKE)
,
pp. 1–7
.
Cited by:
§3.1
.
Friedman (2001)
J. H. Friedman
Greedy function approximation: a gradient boosting machine
.
The Annals of Statistics
29
(
5
),
pp. 1189–1232
.
External Links:
Document
Cited by:
§4.4
.
Ge
et al.
(2026)
C. Ge, D. Kryvosheieva, D. Fried, U. Girit, and K. Hariharan
Agent psychometrics: task-level performance prediction in agentic coding benchmarks
.
In
Conference on Language Modeling (COLM)
,
Note:
arXiv:2604.00594
Cited by:
§1
,
§3.1
.
Gneiting and Raftery (2007)
T. Gneiting and A. E. Raftery
Strictly proper scoring rules, prediction, and estimation
.
Journal of the American Statistical Association
102
(
477
),
pp. 359–378
.
External Links:
Document
,
Link
Cited by:
§4.3
.
Holm (1979)
S. Holm
A simple sequentially rejective multiple test procedure
.
Scandinavian Journal of Statistics
6
(
2
),
pp. 65–70
.
Cited by:
§4.8
.
Janes
et al.
(2009)
H. Janes, G. M. Longton, and M. Pepe
Accommodating covariates in ROC analysis
.
The Stata Journal
9
(
1
),
pp. 17–39
.
Cited by:
§1
.
Janes and Pepe (2009)
H. Janes and M. S. Pepe
Adjusting for covariate effects on classification accuracy using the covariate-adjusted receiver operating characteristic curve
.
Biometrika
96
(
2
),
pp. 371–382
.
Cited by:
§1
.
Jin
et al.
(2024)
H. Jin, L. Huang, H. Cai, J. Yan, B. Li, and H. Chen
From llms to llm-based agents for software engineering: a survey of current, challenges and future
.
arXiv preprint arXiv:2408.02479
.
Cited by:
§1
.
Khanna (2026)
S. Khanna
Zombie agents: detecting semantic livelock in long-horizon autonomous software
.
In
Proceedings of the 3rd ACM International Conference on AI-Powered Software
,
pp. 87–89
.
Cited by:
§1
.
Krsteski and Meyer (2026)
S. Krsteski and C. Meyer
Predicting task difficulty without rollouts
.
External Links:
2608.05797
,
Link
Cited by:
§1
,
§3.1
.
Lee (2026)
W. Y. Lee
Capable but unreliable: canonical path deviation as a causal mechanism of agent failure in long-horizon tasks
.
arXiv preprint arXiv:2602.19008
.
Cited by:
§1
.
Liu
et al.
(2026)
J. Liu, K. Wang, Y. Chen, X. Peng, Z. Chen, L. Zhang, and Y. Lou
Large language model-based agents for software engineering: a survey
.
ACM Transactions on Software Engineering and Methodology
.
External Links:
Document
,
Link
Cited by:
§1
.
Long
et al.
(2026)
X. Long, L. Du, Y. Xu, R. Xu, Q. Lu, Y. Gao, Q. Xie, F. Liu, N. Ding, H. Wang, Z. Li, C. Zhou, J. Guo, and Y. Tang
LiveClawBench: benchmarking LLM agents on complex, real-world assistant tasks
.
arXiv preprint arXiv:2604.13072
.
Cited by:
§1
,
Table 1
.
Mehtiyev and Assunção (2026)
T. Mehtiyev and W. Assunção
Beyond resolution rates: behavioral drivers of coding agent success and failure
.
arXiv preprint arXiv:2604.02547
.
Cited by:
§1
,
§3.1
,
§5.2
.
Pedregosa
et al.
(2011)
F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and É. Duchesnay
Scikit-learn: machine learning in python
.
Journal of Machine Learning Research
12
,
pp. 2825–2830
.
Cited by:
§4.4
.
Pepe (2003)
M. S. Pepe
The statistical evaluation of medical tests for classification and prediction
.
Oxford university press
.
Cited by:
§1
.
Pham
et al.
(2026)
D. Pham, K. Katevas, A. S. Shamsabadi, and H. Haddadi
AgentStop: terminating local ai agents early to save energy in consumer devices
.
In
Proceedings of the ACM Conference on AI and Agentic Systems
,
pp. 1051–1069
.
External Links:
Document
Cited by:
§1
.
Raghu
et al.
(2026)
S. Raghu, S. Pandey, and S. Pandey
Proper scoring rules for agentic uncertainty quantification
.
arXiv preprint arXiv:2605.24756
.
External Links:
Document
,
Link
Cited by:
§3.3
.
Ruan
et al.
(2026)
K. Ruan, Z. Huang, Z. Zhou, Q. Wei, J. Lin, X. Wang, and H. Sun
Doomed from the start: early abort of LLM agent episodes via a recall-controlled probe cascade
.
arXiv preprint arXiv:2607.06503
.
Cited by:
§3.2
,
§5.2
.
Salton and Buckley (1988)
G. Salton and C. Buckley
Term-weighting approaches in automatic text retrieval
.
Information Processing & Management
24
(
5
),
pp. 513–523
.
External Links:
Document
Cited by:
§4.4
,
§4.4
.
Shi
et al.
(2026)
Y. Shi, Z. Sun, J. Dong, C. Wan, D. Lo, and X. Gu
EarlyEval: cheaper agent evaluation via early outcome prediction
.
arXiv preprint arXiv:2609.02783
.
External Links:
Document
,
Link
Cited by:
§1
,
§3.2
,
§4.4
.
Shrout and Fleiss (1979)
P. E. Shrout and J. L. Fleiss
Intraclass correlations: uses in assessing rater reliability
.
Psychological Bulletin
86
(
2
),
pp. 420–428
.
External Links:
Document
Cited by:
§4.8
.
Silva
et al.
(2026)
A. Silva, H. Tu, and M. Monperrus
Latent programming horizons in coding agents
.
External Links:
2607.05188
,
Link
Cited by:
§1
,
§4.2
,
Table 1
.
Sun
et al.
(2026)
H. Sun, A. Uchôa, R. Gheyi, and W. K. Assunção
Evaluating language models on cross-language code functional equivalence
.
arXiv preprint arXiv:2608.23961
.
Cited by:
§3.1
.
Vasudev
et al.
(2026)
R. Vasudev, M. Russak, D. Bikel, and W. Alshikh
Accurate failure prediction in agents does not imply effective failure prevention
.
arXiv preprint arXiv:2602.03338
.
Cited by:
§1
,
§3.3
,
§3
.
Wang
et al.
(2026)
C. Wang, Y. Lyu, J. He, Z. Yang, C. Zhong, Y. Harel, and D. Lo
Fail-fast, restart-smart: early failure prediction and restart for swe agentic tasks
.
External Links:
2608.03222
,
Link
Cited by:
§1
,
§3.2
,
§3
,
§5.2
.
Xia
et al.
(2015)
Y. Xia, H. Li, T. Qin, N. Yu, and T. Liu
Thompson sampling for budgeted multi-armed bandits
.
External Links:
1505.00146
,
Link
Cited by:
§4.7
.
Yang
et al.
(2024)
J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press
SWE-agent: agent-computer interfaces enable automated software engineering
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Cited by:
§1
,
§1
,
Table 1
.
Yao
et al.
(2023)
S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao
ReAct: synergizing reasoning and acting in language models
.
In
International Conference on Learning Representations
,
Cited by:
§1
.
Zhang
et al.
(2025)
S. Zhang, M. Yin, J. Zhang, J. Liu, Z. Han, J. Zhang, B. Li, C. Wang, H. Wang, Y. Chen,
et al.
Which agent causes task failures and when? on automated failure attribution of llm multi-agent systems
.
arXiv preprint arXiv:2505.00212
.
Cited by:
§1
.