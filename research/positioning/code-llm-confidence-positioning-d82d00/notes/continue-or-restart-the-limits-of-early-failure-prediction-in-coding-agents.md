---
title: Continue or Restart? The Limits of Early Failure Prediction in Coding Agents
id: continue-or-restart-the-limits-of-early-failure-prediction-in-coding-agents
tags:
- code-llm-confidence-positioning-d82d00
- w3-forward-citation
created: '2026-11-10T08:23:45.696114Z'
updated: '2026-11-10T08:25:30.954259Z'
source: https://arxiv.org/html/2610.35971
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:45.695776Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Mines 147,002 released SWE-rebench/Open-SWE-Traces execution traces (4 model-framework
  settings): early prefixes give near-chance within-task discrimination (AUC_within
  about 0.50) even though 87.51% of runs already invoked tests by 20k tokens; learned
  stopping beats random restarts by at most 1.98 pp via between-task allocation; uninterrupted
  continuation beats restart policies in 216 of 224 budget configurations. Bears on
  L3 (budgeted routing vs random) by analogy; agent traces, not code-LLM confidence.'
---

Continue or Restart? The Limits of Early Failure Prediction in Coding Agents
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2610.35971v1 [cs.SE] 26 Oct 2026
Continue or Restart? The Limits of Early Failure Prediction in Coding Agents
Srinath Srinivasan
Affiliation:
NC State University
Raleigh, NC, USA
ssrini27@ncsu.edu
Lunxiao Li
Affiliation:
NC State University
Raleigh, NC, USA
lli66@ncsu.edu
Tim Menzies
Affiliation:
NC State University
Raleigh, NC, USA
timm@ieee.org
Wesley Assunção
Affiliation:
NC State University
Raleigh, NC, USA
wguezas@ncsu.edu
Abstract
Early stopping promises to reduce the computational cost of autonomous coding agents by terminating unpromising runs before completion. Evaluating when to abandon an active run, however, requires separating the baseline difficulty of a software issue from the trajectory of an individual attempt. We study this distinction across 147,002 execution traces from two public corpora spanning four model-framework settings. Comparing pre-execution issue context against early execution prefixes, we evaluate linear count models, initial-turn text embeddings, task-conditional rankers, and a fine-tuned Qwen3-0.6B monitor. Although early prefixes modestly improve cross-task outcome ranking, within-task discrimination remains near chance across early landmarks (5k-20k tokens): initial-turn embeddings and 20k-token task-conditional models yield AUCs around 0.50, and three-seed neural evaluations across 32,406 attempts at 20k tokens achieve a mean within-task AUC of 0.50 [0.48, 0.51] across tasks of varying solve rates. To evaluate how these predictions translate into stopping decisions, we replay score-guided and matched random restarts under shared token budgets alongside uninterrupted continuation. Under a 75k-token cap, learned restarting improves resolution over matched random restarting by up to 1.98 percentage points. An exact algebraic decomposition resolves this paradox: the gain over random restarting stems almost entirely from between-task stopping allocation (avoiding stops on easy issues), whereas attempt-level selection within a task contributes near zero (-0.11 to +0.24 percentage points). Across all four settings at the 75k cap (and 216 of 224 tested budget-threshold configurations overall), uninterrupted continuation achieves higher solve rates at lower mean token cost than both restart policies. Practical evaluations of early stopping must therefore establish attempt-level discrimination and demonstrate net compute savings relative to continuation.
Index Terms:
coding agents, early failure prediction, early stopping, restart policies, mining execution traces, empirical study
I
Introduction
Consider a coding agent that has consumed 20,000 (20k) transcript tokens investigating a repository issue. By this point, the agent has inspected repository files and invoked initial test or edit commands, yet whether its trajectory will ultimately resolve the issue remains unknown. Suppose a failure monitor assigns the active attempt a low probability of success. Under a 75,000 (75k) token budget, aborting the run to start a fresh attempt leaves only 55k tokens for the replacement and discards all prior repository exploration. Whenever an aborted run would have succeeded within the full budget, or whenever its replacement exhausts the residual 55k budget before finishing, restarting degrades overall resolution. Evaluating early stopping therefore requires determining whether early trajectory signals justify abandoning an active attempt.
Autonomous coding agents pair language models with execution scaffolds to navigate codebases, modify source files, and run verification tests
[
1
,
2
,
3
]
. Throughout this study, a
task
denotes a repository issue, and a
run
(or
attempt
) denotes a single execution trajectory on that task. At any decision landmark, the
prefix
comprises the interaction sequence of assistant turns and tool observations recorded up to that transcript-token count, prior to final patch evaluation.
Evaluating early failure predictors presents two methodological challenges. First, baseline task solvability confounds attempt-level progress. If an agent consistently resolves one issue and fails another, a monitor that estimates static task difficulty will achieve strong corpus-wide ranking even if it assigns identical scores to every attempt on the same issue. We therefore separate
pooled prediction
, which ranks outcomes across all eligible runs, from
within-task discrimination
, which compares successful and failed attempts on the exact same task using area under the ROC curve (
AUC
within
\mathrm{AUC}_{\mathrm{within}}
, where
0.50
0.50
indicates random ranking).
Second, predictive ranking does not directly establish the resource efficiency of a stopping policy. Mid-execution interventions can follow two distinct regimes:
abort-only termination
, which abandons low-scoring runs without replacement to save tokens at the expense of forfeiting any late resolutions, and
restart-based stopping
, which terminates a stalled attempt to reallocate the remaining budget to a fresh attempt on the same issue. If an early monitor captures only static issue difficulty (
AUC
within
≈
0.50
\mathrm{AUC}_{\mathrm{within}}\approx 0.50
), abort-only termination at
20
​
k
20\text{k}
tokens merely executes a delayed task filter after burning
20
​
k
20\text{k}
tokens (which is strictly dominated by pre-execution filtering at zero token cost), so we focus our policy evaluation on whether trajectory-based stopping improves resolution via cold restarts. Aborting an active run to restart improves outcomes only when a replacement attempt is more likely to solve the task within the residual budget than the original run is via continuation. Stopping rules must therefore be evaluated against both
matched random restarting
(aborting the same fraction of active runs without using predictions) and uninterrupted
continuation
under a shared token cap.
While prior work proposes monitors based on token probabilities, behavioral states, internal activations, and state-preserving recovery
[
4
,
5
,
6
,
7
]
, recent studies show that task identity confounds pooled trajectory metrics
[
8
,
9
]
and that continuation often outperforms cold restarts in mathematical reasoning
[
10
]
. However, prior work has not tested whether task-conditional training or end-to-end neural monitors recover attempt-level signal, nor explained why score-guided policies still beat random restarts in replay. We mine
147,002
147,002
released execution traces from Nebius SWE-rebench and NVIDIA Open-SWE-Traces
[
11
,
12
]
across four model-framework combinations (
settings
). Across landmarks from
5
​
k
5\text{k}
to
60
​
k
60\text{k}
tokens (focusing on
20
​
k
20\text{k}
, where nearly all runs remain active), we compare pre-execution issue features against early prefixes using action-count regressions, frozen text embeddings, task-conditional rankers, and a fine-tuned Qwen3-0.6B monitor adapted from prior work
[
7
]
. Using recorded-attempt replay under shared token caps, we answer three research questions:
RQ1.
How much does observing an early execution prefix improve outcome prediction beyond pre-execution task context?
RQ2.
Do early execution prefixes distinguish successful from failed attempts on the same task?
RQ3.
What drives the performance difference between learned and random restarting, and how do both policies compare with uninterrupted continuation under a shared token budget?
Across all four settings, we make three main contributions. First, we show via unseen-repository cross-validation, permutation controls, and equivalence testing (TOST) that while static context supports cross-task ranking, early prefixes yield near-chance within-task discrimination (
AUC
within
≈
0.50
\mathrm{AUC}_{\mathrm{within}}\approx 0.50
) across
5
​
k
5\text{k}
embeddings as well as
20
​
k
20\text{k}
count models, task-conditional rankers, and the three-seed neural monitor, even though
87.51
%
87.51\%
of primary-corpus runs have already invoked tests and
32.80
%
32.80\%
have edited code by
20
​
k
20\text{k}
tokens. Second, in budget-constrained replay under a
75
​
k
75\text{k}
cap, we derive an exact decomposition proving that learned stopping’s gain over matched random restarting (up to
1.98
1.98
percentage points) stems from between-task stopping allocation rather than within-task attempt selection. Third, we show across
224
224
budget-threshold configurations that uninterrupted continuation achieves higher solve rates at lower mean token cost than both restart policies across the
75
​
k
75\text{k}
and
100
​
k
100\text{k}
frontiers (
111
111
of
112
112
configurations, and
216
216
of
224
224
overall).
II
Related Work
Mining coding-agent execution traces
Benchmarks such as SWE-bench evaluate autonomous agents on real-world repository issues
[
1
]
, using execution frameworks like SWE-agent
[
2
]
and OpenHands
[
3
]
to orchestrate repository exploration and patch verification. Large-scale public corpora now capture complete execution traces from these workflows
[
11
,
12
]
. These datasets extend classical mining of developer interaction histories
[
13
]
to autonomous software engineering, recording fine-grained sequences of tool invocations and environment observations. Recent empirical studies mining these traces show that issue-level properties strongly shape trajectory metrics. Mehtiyev and Assunção demonstrate that the apparent relationship between trajectory length and failure shifts substantially once task identity is controlled
[
8
]
. Complementary analyses examine how failure cascades develop during execution
[
14
]
and whether behavioral features carry consistent predictive weights across issues and repeated trials
[
15
]
. These findings motivate mining multi-attempt corpora to test whether early trajectory observations capture attempt-specific progress beyond static issue difficulty.
Early failure prediction in agent runs
Prior work proposes diverse signals to anticipate unsuccessful agent runs before completion. Trajectory-based approaches mine historical execution experience to terminate unpromising patch generation
[
16
]
or model agent behavior through state transitions and late-emerging failure indicators
[
5
,
17
]
. A second line of work monitors execution sequentially by estimating residual resource requirements
[
18
]
or applying sequential statistical testing to intermediate verifier scores
[
19
]
. A third family extracts signals directly from the underlying language model, using generated token probabilities
[
4
]
or probing internal representations to predict edit outcomes and likely failures
[
20
,
6
]
. Whereas existing monitors are primarily evaluated on pooled benchmark accuracy or total token reduction, we evaluate whether early prefixes rank competing attempts on the exact same software issue.
Restart strategies and state recovery
Restart policies originate in randomized algorithms, where Luby et al. established optimal and universal restart schedules for heavy-tailed runtime distributions based on elapsed execution time
[
21
]
. In autonomous coding workflows, mid-episode interventions can either start fresh or transfer accumulated context. Scrouting uses an initial repository exploration phase to route the issue and its gathered context to a downstream solver
[
22
]
.
FailFast–RestartSmart
pairs a 0.6B failure monitor, trained on terminal outcomes and intermediate test supervision, with a recovery mechanism that retains code edits from aborted runs
[
7
]
. Across four coding-agent policies, their system reports 14.6–20.4% execution-token savings at a 5% false-positive target. Notably, at a 25% false-positive target with Qwen3.6-27B, transferring saved edits raises resolution from 66.6% to 71.8%, whereas restarting cold reaches only 66.8%. That sharp gap between state-preserving recovery and cold restarting highlights the cost of discarding prior exploration. Building on this insight, we adapt their 0.6B terminal-outcome monitor to evaluate cold replacement attempts under shared token budgets and isolate how sunk exploration tokens affect the restart tradeoff.
Disentangling task difficulty from stopping policies
Two concurrent studies examine the gap between problem difficulty and attempt-level intervention. Investigating the Nebius OpenHands corpus
[
11
]
alongside additional benchmarks, EsfandyariDoulabi et al. show that high pooled AUROC largely reflects cross-task difficulty even when within-task discrimination remains near chance, concluding that cross-task budget allocation is more effective than abort-only stopping in this regime
[
9
]
. In mathematical reasoning, Bulut similarly finds that early prefix predictions offer minimal within-problem discrimination and that continuing an active trace outperforms cold restarts under matched token budgets
[
10
]
.
Our work extends this emerging perspective across four coding-agent settings by connecting within-task evaluation directly to the mechanics of restart policies. First, we evaluate whether task-conditional training or a fine-tuned neural monitor recovers attempt-level signal that count features and frozen embeddings miss, including across tasks stratified by empirical solvability. Second, we explain the apparent paradox in which a learned stopping rule beats a matched random restart baseline despite near-chance within-task ranking. By decomposing replay outcomes into between-task and within-task selection and accounting for both replacement credit and forfeited original successes, we show how task selection drives the gain over random restarting while uninterrupted continuation dominates both policies across the shared-budget frontier.
III
Data and Method
Our methodology comprises four stages: curating multi-attempt execution traces across four model-framework settings, extracting prefix representations at fixed token landmarks, evaluating cross-task and within-task predictive discrimination, and replaying stopping policies under shared token budgets.
III-A
Released runs and labels
We analyze 147,002 execution traces drawn from two public corpora of autonomous coding agents solving benchmark repository issues. Each trace represents a single
run
(or
attempt
)
i
i
by an agent assigned to resolve a specific repository issue, which we term a
task
t
t
, belonging to a source code
repository
. We define a
setting
as a unique combination of an underlying large language model and an agent execution framework.
Our primary corpus, released by Nebius
[
11
]
, executes OpenHands with Qwen3-Coder-480B-A35B-Instruct
[
23
]
on SWE-rebench tasks
[
24
]
. To evaluate generalization across architectures and scaffolding, we incorporate three slices from NVIDIA Open-SWE-Traces
[
12
]
: SWE-agent with Qwen3.5-122B-A10B
[
25
]
, OpenHands with Qwen3.5-122B-A10B, and OpenHands with MiniMax-M2.5
[
26
]
. Table
I
summarizes the corpus statistics across all four settings. Because individual benchmark issues can appear in multiple corpora, task counts overlap across settings.
Each completed run terminates with a binary
outcome label
Y
i
∈
{
0
,
1
}
Y_{i}\in\{0,1\}
produced by the benchmark evaluation harness, which applies the agent’s final code patch to the repository and executes the verification test suite. We set
Y
i
=
1
Y_{i}=1
if the patch resolves the issue and
Y
i
=
0
Y_{i}=0
if the issue remains unresolved, excluding unlabelled records from our analysis.
TABLE I:
Summary of released execution-trace settings. OH: OpenHands; SA: SWE-agent. ICC measures within-task outcome clustering on the binary scale.
Setting
Runs
Tasks
Repositories
ICC
OH / Qwen3-Coder
67,074
6,306
1,823
0.797
SA / Qwen3.5
15,098
7,885
1,815
0.768
OH / Qwen3.5
30,957
14,142
2,234
0.713
OH / MiniMax-M2.5
33,873
14,716
2,275
0.815
III-B
Trace representation and decision landmarks
During execution, an agent interacts with its environment through an alternating sequence of assistant turns and tool observations. To establish a uniform measure of computational progress within each setting, we measure trajectory length in
transcript tokens
, counted across all recorded messages using that setting’s native model tokenizer, and denote the total transcript length of completed run
i
i
by
L
i
L_{i}
. We also normalize raw tool invocations into standard behavioral categories covering file inspection, codebase search, code editing, and test execution.
A
decision landmark
b
b
is a fixed transcript-token threshold at which a monitor evaluates an ongoing run. At landmark
b
b
, the cohort of
eligible
(or
active
) runs consists exclusively of attempts whose total token length exceeds the threshold (
L
i
>
b
L_{i}>b
), ensuring that a stopping intervention remains actionable. For each eligible run, the predictor observes only the execution
prefix
completed up to token
b
b
. We evaluate predictions across seven landmarks (
b
∈
{
5
​
k
,
10
​
k
,
15
​
k
,
20
​
k
,
30
​
k
,
40
​
k
,
60
​
k
}
b\in\{5\text{k},10\text{k},15\text{k},20\text{k},30\text{k},40\text{k},60\text{k}\}
tokens). Because shorter runs terminate as
b
b
increases, we report the
surviving fraction
(the proportion of initial runs satisfying
L
i
>
b
L_{i}>b
) at each landmark to characterize the active population. We designate
b
=
20
​
k
b=20\text{k}
tokens as our primary decision point because agents have already engaged in substantial environment interaction by this stage while nearly all runs remain active (Fig.
1
, right). On the primary corpus at
20
​
k
20\text{k}
tokens,
87.51
%
87.51\%
of active runs have already executed a detected test command and
32.80
%
32.80\%
have a detected edit action.
III-C
Evaluation metrics and task clustering
Before assessing individual predictors, we quantify the degree to which trial outcomes cluster by task using the
intraclass correlation
(ICC), computed via an analysis-of-variance estimator for binary outcomes
[
27
]
across tasks with repeated attempts. Values of ICC approaching
1.0
1.0
indicate that attempts on the same issue predominantly share the same terminal outcome.
At a given landmark
b
b
, a failure monitor assigns each eligible run
i
i
a scalar
success score
s
i
∈
[
0
,
1
]
s_{i}\in[0,1]
, where higher values indicate a higher predicted probability of resolving the task. We evaluate the calibration and sharpness of probability estimates using
log loss
[
28
]
(the mean negative log-likelihood of the true outcome
Y
i
Y_{i}
, where lower values reflect superior probabilistic accuracy) and evaluate ranking discrimination using two formulations of the area under the ROC curve (AUC)
[
29
]
:
1) Pooled AUC
pairs every successful eligible run with every failed eligible run across the entire setting, computing the fraction of pairs in which the successful run receives a higher score (with half credit for ties, where
0.50
0.50
represents random ranking). Because pooled pairs span different issues, pooled AUC captures both cross-task difficulty and attempt-level differences.
2) Within-task AUC
(
AUC
within
\mathrm{AUC}_{\mathrm{within}}
) isolates attempt-level discrimination by restricting comparisons to pairs of runs executed on the exact same task. We define a
mixed-outcome task
at landmark
b
b
as a task whose active runs include at least one success and at least one failure. Let
P
t
P_{t}
and
F
t
F_{t}
denote the sets of successful and failed active runs on task
t
t
, respectively. Aggregating across all mixed-outcome tasks, within-task AUC is defined as:
AUC
within
=
∑
t
∑
i
∈
P
t
,
j
∈
F
t
[
𝟏
​
(
s
i
>
s
j
)
+
1
2
​
𝟏
​
(
s
i
=
s
j
)
]
∑
t
|
P
t
|
​
|
F
t
|
,
\mathrm{AUC}_{\mathrm{within}}=\frac{\sum_{t}\sum_{i\in P_{t},\,j\in F_{t}}\!\left[\mathbf{1}(s_{i}>s_{j})+\tfrac{1}{2}\mathbf{1}(s_{i}=s_{j})\right]}{\sum_{t}|P_{t}|\,|F_{t}|},
(1)
where
𝟏
​
(
⋅
)
\mathbf{1}(\cdot)
is the indicator function. Each valid within-task pair carries equal weight in Eq. (
1
); for instance, a mixed-outcome task with two active successes and three active failures contributes
|
P
t
|
​
|
F
t
|
=
6
|P_{t}|\,|F_{t}|=6
pairs.
To account for hierarchical dependence in our data during uncertainty estimation, we compute 95% cluster-bootstrap confidence intervals that resample whole clustering units with replacement
[
30
]
from saved out-of-fold predictions. Specifically, pooled and replay metrics resample repositories (and training seeds for the neural monitor), whereas within-task AUC resamples tasks.
III-D
Prediction models for RQ1 and RQ2
To measure how much early execution trajectories improve outcome prediction over static issue descriptions (RQ1) and whether they distinguish competing attempts on the same task (RQ2), we train linear and conditional models using five-fold
unseen-repository cross-validation
. In this splitting protocol, all tasks belonging to a given repository are assigned to the same fold, ensuring that models are evaluated exclusively on repositories held out during training.
Our
issue baseline
extracts eight pre-execution count features from the problem statement covering text length, code blocks, error and reproduction indicators, URLs, and referenced file paths. Our
issue-plus-prefix model
augments these eight issue features with 18 behavioral count features extracted from the observed prefix up to landmark
b
b
, capturing distinct files inspected, repeated shell commands, error outputs, cumulative text volume, code edits, and test invocations (two fine-grained test-output features are specific to the primary corpus trace schema, yielding 16 prefix features for the Open-SWE settings). Both models use L2-regularized logistic regression fit on log-transformed, standardized feature counts. Comparing the issue-plus-prefix model against the issue baseline isolates the predictive gain contributed by observing execution.
Because pooled logistic regression fits weights to variation both across tasks and within tasks, we also train a
task-conditional logistic model
[
31
]
restricted to mixed-outcome tasks. By conditioning on task identity, this formulation eliminates the task-level intercept and estimates feature weights solely from differences between successful and failed attempts on the same issue using prefix features. We also evaluate cross-setting transfer at
20
​
k
20\text{k}
tokens by applying the
16
16
-feature conditional model trained on one setting directly to another after holding out overlapping repositories and tasks. To verify that our conditional estimation pipeline remains unbiased under the null, we validate the estimator against a permutation control that shuffles outcome labels within each task. To quantify how tightly within-task AUC concentrates around chance (
0.50
0.50
), we evaluate equivalence bounds of
[
0.45
,
0.55
]
[0.45,0.55]
and
[
0.47
,
0.53
]
[0.47,0.53]
using two one-sided tests (TOST) at the
α
=
0.05
\alpha=0.05
level via 90% task-bootstrap confidence intervals
[
32
,
33
]
.
Beyond standard count regressions, we evaluate three supplementary designs to test alternative sources of predictive signal:
Task metadata and solvability stratification
We test whether augmenting count models with Open-SWE-Traces task categories (
bug fix
,
enhancement
,
feature request
,
other
)
[
12
]
and programming language under unseen-repository cross-validation improves cross-task and within-task discrimination. To test whether attempt-level discrimination is stronger on easier issues, we also stratify mixed-outcome tasks at the 20k landmark into low (
<
25
%
<25\%
), medium (
25
​
–
​
75
%
25\text{--}75\%
), and high (
>
75
%
>75\%
) empirical solve-rate tiers (Table
III
).
Frozen text embeddings
To test whether dense lexical representations capture early trajectory signals missed by summary counts, we encode the truncated issue description, the initial assistant turn, and the first tool observation on the primary corpus using the frozen
all-MiniLM-L6-v2
sentence encoder
[
34
,
35
]
, concatenating these embeddings with initial prompt-context metadata as inputs to a regularized linear classifier.
Task-rate oracle
To establish an upper bound on task-level predictability and test whether prefix features add value when baseline task solvability is already known, we construct a diagnostic
task-rate oracle
on tasks with at least four active attempts. Across repeated random splits, we hold out half of a task’s attempts to compute its empirical solve fraction and supply that fraction as a feature when scoring the remaining half, both standalone and combined with prefix counts.
III-E
Adapted neural monitor
To test whether end-to-end representation learning extracts fine-grained within-task trajectory cues that count models and frozen embeddings miss (RQ2), we adapt the neural failure monitor architecture from FailFast–RestartSmart
[
7
]
. Specifically, we fine-tune Qwen3-0.6B
[
36
]
using low-rank adaptation (LoRA)
[
37
]
and a linear classification head to predict terminal task resolution at the 20k-token landmark under a
4,096
4,096
-token input limit. We compare two input configurations trained and evaluated on identical data splits: an
issue-only arm
that receives the problem description, and an
issue-plus-prefix arm
that receives the problem description alongside the most recent transcript messages completed by
20
​
k
20\text{k}
tokens. When present in the preceding prefix, the issue-plus-prefix input also includes the latest earlier message matching an editor-tool heuristic (which captures editor-tool invocations including file-viewing and modification operations, and is simply omitted when no prior message matches).
To prevent static task difficulty from dominating gradient updates and isolate attempt-level discrimination for RQ2, each optimization step samples a matched pair consisting of one successful and one failed attempt from the same mixed-outcome task, minimizing a composite objective that combines binary cross-entropy (BCE) loss with a pairwise ranking loss
[
38
]
that rewards assigning a higher score to the successful attempt. By construction, balanced within-task pair sampling fixes the training prevalence of every task at
0.50
0.50
. For the issue-only arm, where both attempts in a pair share identical input text, the BCE objective has an analytical minimum at a constant prediction of
0.50
0.50
(yielding a baseline log loss of
ln
⁡
2
≈
0.693
\ln 2\approx 0.693
and
AUC
within
=
0.500
\mathrm{AUC}_{\mathrm{within}}=0.500
because all attempts on a task receive identical scores), providing a null reference for measuring attempt-level signal in the issue-plus-prefix arm.
We conduct our neural evaluation across all primary-corpus tasks with at least 11 active attempts at the 20k landmark, sampling 11 attempts per task uniformly without outcome stratification to form a cohort of 32,406 attempts across 2,946 tasks. We partition this cohort using three-fold unseen-repository cross-validation so that every task is scored out-of-fold, and we train three random seeds per fold with checkpoint selection governed by validation within-task AUC. Because the three seeds evaluate on identical held-out repository folds, we report mean metrics aggregated across seeds and construct joint repository-and-seed bootstrap intervals.
III-F
Budget-constrained restart replay for RQ3
To determine how early failure scores translate into operational stopping decisions and resource consumption (RQ3), we perform
recorded-attempt replay
across all tasks with at least two recorded attempts. In each replay trial, an initial attempt
i
i
executes until landmark
b
=
20
​
k
b=20\text{k}
. If a
stopping policy
π
\pi
terminates run
i
i
at landmark
b
b
, the system initiates a cold replacement attempt
j
j
selected uniformly at random from the remaining recorded attempts on the same task, and we compute expected outcomes over all valid replacement choices while giving each starting attempt equal weight. Using out-of-fold success scores
s
i
s_{i}
from the pooled issue-plus-prefix count logistic regression model (which spans all four settings and reflects the combined task and prefix signal deployed in standard monitors), we compare three primary policies: (1)
Learned restart (
L
L
)
, which terminates an active run at landmark
b
b
if its out-of-fold success score
s
i
s_{i}
falls below a fixed percentile threshold (evaluated across seven thresholds spanning the 2nd to 98th score percentiles); (2)
Matched random restart (
R
R
)
, which terminates the exact same overall fraction of active runs at landmark
b
b
as the corresponding learned threshold, selecting runs uniformly at random without consulting
s
i
s_{i}
; and (3)
Continuation
, which permits the initial attempt
i
i
to proceed to completion without intervention. (Terminating active runs at landmark
b
b
without replacement, fixed truncation, corresponds to setting replacement credit
R
j
≡
0
R_{j}\equiv 0
, which upper-bounds solve rate by the pre-landmark completion rate and cannot improve resolution over continuation.)
We first evaluate policies in an
uncapped replay
regime where initial and replacement runs execute until their recorded completion lengths. To model realistic compute constraints, we then enforce a shared hard
token cap
B
∈
{
30
​
k
,
50
​
k
,
75
​
k
,
100
​
k
}
B\in\{30\text{k},50\text{k},75\text{k},100\text{k}\}
governing the combined token expenditure of the initial run and any subsequent replacement. When a policy aborts run
i
i
at landmark
b
b
, the replacement attempt
j
j
(with recorded length
L
j
L_{j}
and outcome
Y
j
∈
{
0
,
1
}
Y_{j}\in\{0,1\}
) receives a
residual token budget
of
B
−
b
B-b
. Its resulting
replacement success credit
R
j
R_{j}
and combined
transcript-token cost
K
j
K_{j}
are given by:
R
j
\displaystyle R_{j}
=
Y
j
​
1
​
(
L
j
≤
B
−
b
)
,
\displaystyle=Y_{j}\,\mathbf{1}(L_{j}\leq B-b),
(2)
K
j
\displaystyle K_{j}
=
b
+
min
⁡
(
L
j
,
B
−
b
)
.
\displaystyle=b+\min(L_{j},B-b).
(3)
Under Eqs. (
2
)–(
3
), a replacement attempt earns resolution credit only if it solves the issue and completes within the remaining
B
−
b
B-b
tokens. For example, stopping at
b
=
20
​
k
b=20\text{k}
under a
B
=
75
​
k
B=75\text{k}
cap leaves
55
​
k
55\text{k}
tokens: a successful replacement requiring
50
​
k
50\text{k}
tokens earns full credit (
R
j
=
1
R_{j}=1
) at a total cost of
K
j
=
70
​
k
K_{j}=70\text{k}
tokens, whereas a replacement requiring
60
​
k
60\text{k}
tokens exhausts the cap at
K
j
=
75
​
k
K_{j}=75\text{k}
and earns
R
j
=
0
R_{j}=0
. A policy’s overall
solve rate
V
⁡
(
π
)
V(\pi)
is the mean resolution credit achieved across all starting attempts and replacement draws.
Decomposing learned versus random stopping
When a learned restart policy achieves a higher solve rate than matched random restart (
V
⁡
(
L
)
>
V
⁡
(
R
)
V(L)>V(R)
), that advantage can arise from two distinct mechanisms:
between-task selection
(concentrating stops on tasks where restarting yields a more favorable expected return) and
within-task selection
(preferentially aborting the weaker attempts on a given task). To isolate how much of the policy difference stems from attempt-level failure detection
[
39
]
, we derive an exact algebraic decomposition of
V
⁡
(
L
)
−
V
⁡
(
R
)
V(L)-V(R)
.
Under a fixed cap
B
B
, let
C
i
=
Y
i
​
𝟏
​
(
L
i
≤
B
)
C_{i}=Y_{i}\mathbf{1}(L_{i}\leq B)
indicate whether continuing starting attempt
i
i
resolves the task within budget, and let
G
i
G_{i}
denote the expected replacement credit obtained by averaging
R
j
R_{j}
in Eq. (
2
) over all other recorded attempts
j
j
on the same task. Defining
v
i
=
G
i
−
C
i
v_{i}=G_{i}-C_{i}
as the net expected solve-rate gain of restarting attempt
i
i
, and letting
S
i
π
∈
[
0
,
1
]
S_{i}^{\pi}\in[0,1]
denote policy
π
\pi
’s stopping indicator (or stopping probability under random restart, with
S
i
π
=
0
S_{i}^{\pi}=0
for runs that finished prior to
b
b
), the replay solve rate across all
N
N
starting attempts is:
V
⁡
(
π
)
=
1
N
​
∑
i
=
1
N
[
C
i
+
S
i
π
​
(
G
i
−
C
i
)
]
.
V(\pi)=\frac{1}{N}\sum_{i=1}^{N}\left[C_{i}+S_{i}^{\pi}(G_{i}-C_{i})\right].
(4)
Equation (
4
) shows that the net effect of stopping attempt
i
i
equals the replacement success credited (
S
i
π
​
G
i
S_{i}^{\pi}G_{i}
) minus the original continuation success forfeited (
S
i
π
​
C
i
S_{i}^{\pi}C_{i}
). Let
D
i
=
S
i
L
−
S
i
R
D_{i}=S_{i}^{L}-S_{i}^{R}
denote the stopping differential between the learned and matched random policies on attempt
i
i
, and let
A
t
=
{
i
∈
t
:
L
i
>
b
}
A_{t}=\{i\in t:L_{i}>b\}
denote the set of
n
t
=
|
A
t
|
n_{t}=|A_{t}|
active starting attempts on task
t
t
at landmark
b
b
, with
D
¯
t
\bar{D}_{t}
and
v
¯
t
\bar{v}_{t}
denoting the task-level means of
D
i
D_{i}
and
v
i
v_{i}
over
A
t
A_{t}
. The solve-rate differential
V
⁡
(
L
)
−
V
⁡
(
R
)
V(L)-V(R)
decomposes exactly into:
Δ
between
\displaystyle\Delta_{\mathrm{between}}
=
∑
t
:
n
t
>
0
n
t
N
D
¯
t
v
¯
t
,
\displaystyle=\sum_{t:\,n_{t}>0}\frac{n_{t}}{N}\bar{D}_{t}\bar{v}_{t},
(5)
Δ
within
\displaystyle\Delta_{\mathrm{within}}
=
1
N
∑
t
:
n
t
>
0
∑
i
∈
A
t
(
D
i
−
D
¯
t
)
(
v
i
−
v
¯
t
)
.
\displaystyle=\frac{1}{N}\sum_{t:\,n_{t}>0}\sum_{i\in A_{t}}(D_{i}-\bar{D}_{t})(v_{i}-\bar{v}_{t}).
(6)
Here,
Δ
between
\Delta_{\mathrm{between}}
quantifies the solve-rate difference attributable to task-level stopping rates (
D
¯
t
\bar{D}_{t}
), whereas
Δ
within
\Delta_{\mathrm{within}}
captures the covariance between policy stopping decisions and attempt-level restart value within the same task.
Cost-solve efficiency frontier
To evaluate practical resource efficiency at the 20k landmark, we compare the mean solve rate and mean transcript-token cost of every policy across all four settings, four token caps, and seven stopping thresholds. Within a given setting and token cap
B
B
, a policy configuration is
Pareto-dominated
if an alternative policy achieves at least as high a solve rate at less than or equal mean token cost, with strict improvement on at least one dimension. Mapping dominance across the complete 224-configuration grid characterizes the empirical efficiency frontier of cold restarts relative to uninterrupted continuation.
IV
Results
IV-A
Baseline task clustering across settings
Across all four settings, terminal outcomes cluster strongly by task, with observed-scale intraclass correlation (ICC) reaching
0.71
0.71
or higher in every corpus (Table
I
). Consequently, repeated attempts on the same repository issue predominantly share the same outcome.
Comparing the two Qwen3.5 settings across their
7,102
7,102
shared tasks further illustrates how intrinsic issue difficulty persists across agent scaffolding. The empirical task solve rates of SWE-agent and OpenHands exhibit a Spearman rank correlation of
0.67
0.67
, confirming that issues that are more tractable under one framework remain more tractable under the other. Weighting each shared task equally, SWE-agent achieves a mean solve rate of
47.30
%
47.30\%
compared to
33.24
%
33.24\%
for OpenHands, yielding a framework difference of
14.06
14.06
percentage points (
95
%
95\%
repository-bootstrap CI:
[
12.26
,
15.95
]
[12.26,15.95]
). Together, high within-task outcome clustering and cross-framework rank agreement establish that static task properties account for a substantial share of outcome variation.
IV-B
RQ1: Value of observing an early prefix
To evaluate whether early execution trajectories improve outcome prediction beyond pre-execution context (RQ1), we compare pooled performance at early landmarks across models trained on the empirical task distribution. At
5
​
k
5\text{k}
tokens on the primary corpus, augmenting the issue baseline with prefix action counts increases pooled AUC from
0.56
0.56
to
0.58
0.58
, while log loss remains nearly unchanged (
0.69
0.69
in both arms). By
20
​
k
20\text{k}
tokens, prefix action counts increase pooled AUC from
0.57
0.57
to
0.61
0.61
, reflecting that cumulative early interaction rates correlate with underlying issue difficulty across tasks. For frozen text embeddings of the initial turn at
5
​
k
5\text{k}
tokens, pooled AUC remains at
0.62
0.62
in both the issue-only and issue-plus-prefix arms (with the paired gain interval spanning zero and log loss remaining at
0.67
0.67
).
Supplementary checks confirm that static task context drives this cross-task ranking while leaving attempt-level discrimination unchanged. Even when restricting comparisons to pairs of runs from different tasks within the same repository on the primary corpus, eliminating repository-level confounding, issue-plus-prefix scores rank cross-task pairs with an AUC of
0.56
0.56
[
0.55
,
0.59
]
[0.55,0.59]
at
20
​
k
20\text{k}
tokens (
0.62
0.62
[
0.59
,
0.66
]
[0.59,0.66]
at
40
​
k
40\text{k}
), compared to
0.49
0.49
(
0.54
0.54
at
40
​
k
40\text{k}
) for attempts on the exact same task. Similarly, adding Open-SWE task categories under unseen-repository cross-validation increases issue-baseline pooled AUC by approximately
0.02
0.02
across landmarks while leaving within-task AUC unchanged (
Δ
​
AUC
within
<
0.01
\Delta\mathrm{AUC}_{\mathrm{within}}<0.01
, with no statistically significant gains across task-category or language subgroups after Holm–Bonferroni multiplicity correction
[
40
]
).
Answer to RQ1:
Early action counts and static metadata yield modest gains in cross-task pooled ranking (
0.02
​
–
​
0.04
0.02\text{--}0.04
AUC), whereas initial-turn text embeddings provide no consistent pooled improvement over pre-execution issue text alone.
IV-C
RQ2: Ranking attempts at the same task
IV-C
1
Early action counts and frozen embeddings
We next evaluate whether prefix representations separate successful from failed attempts on the same issue. At
5
​
k
5\text{k}
tokens on the primary corpus, the issue-plus-prefix count model achieves a within-task AUC of
0.50
0.50
[
0.49
,
0.51
]
[0.49,0.51]
, indicating chance-level attempt discrimination despite the pooled gain observed in RQ1. At the primary
20
​
k
20\text{k}
decision point, within-task AUC remains near
0.49
​
–
​
0.50
0.49\text{--}0.50
across all four settings (Fig.
1
, left). At intermediate landmarks of
30
​
k
30\text{k}
and
40
​
k
40\text{k}
tokens, within-task AUC remains indistinguishable from chance across all three Open-SWE settings and rises only modestly on the primary corpus to
0.52
0.52
[
0.51
,
0.53
]
[0.51,0.53]
at
30
​
k
30\text{k}
(
93
%
93\%
of runs active) and
0.54
0.54
[
0.53
,
0.55
]
[0.53,0.55]
at
40
​
k
40\text{k}
(
69
%
69\%
active), a stage at which aborting a run forfeits
30
​
k
–
​
40
​
k
30\text{k}\text{--}40\text{k}
sunk tokens and compresses the residual budget available for a replacement attempt. By
60
​
k
60\text{k}
tokens, within-task AUC on the primary corpus reaches
0.56
0.56
, but the surviving fraction drops to
23
%
23\%
of initial runs (Fig.
1
, right), reflecting both longer observation horizons and selective attrition of shorter trajectories.
5
5
20
20
40
40
60
60
0.4
0.4
0.5
0.5
0.6
0.6
Transcript tokens (thousands)
Within-task AUC
(a) Ranking within tasks
OH / Qwen3-Coder
SA / Qwen3.5
OH / Qwen3.5
OH / MiniMax
5
5
20
20
40
40
60
60
0
0
0.5
0.5
1
1
Transcript tokens (thousands)
Fraction still active
(b) Remaining population
Fig. 1:
Prediction across fixed token landmarks. Left: within-task AUC for issue-plus-prefix count models, with 95% task-bootstrap confidence intervals at each landmark. The dashed line indicates random ranking (0.50). Right: surviving fraction of initial runs still active at each landmark. OH: OpenHands; SA: SWE-agent.
The diagnostic task-rate oracle demonstrates how near-perfect pooled discrimination can coexist with chance-level within-task ranking. Because task solvability is heavily polarized across issues (
ICC
≥
0.71
\mathrm{ICC}\geq 0.71
), predicting outcomes solely from the empirical solve fraction of a task’s reserved attempts at
5
​
k
5\text{k}
tokens achieves a mean pooled AUC of
0.97
0.97
while yielding a within-task AUC of
0.50
0.50
by construction. Combining prefix action counts with the task-rate oracle leaves pooled AUC at
0.97
0.97
and yields a within-task AUC of
0.50
0.50
at
5
​
k
5\text{k}
tokens (rising to
0.53
0.53
at
60
​
k
60\text{k}
tokens), confirming that early prefix features add negligible discrimination once baseline task solvability is known. Figure
2
contrasts pooled and within-task AUC across four predictors at
5
​
k
5\text{k}
tokens: whereas pooled AUC spans
0.58
0.58
to
0.97
0.97
, within-task AUC clusters tightly around
0.50
0.50
, including for frozen text embeddings (
0.49
0.49
[
0.48
,
0.50
]
[0.48,0.50]
).
0.4
0.4
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
1
1
Counts
Embeddings
Task rate
Task rate + counts
0.577
0.623
0.966
0.966
0.497
0.492
0.500
0.501
AUC at 5k tokens (primary corpus)
Pooled AUC
Within-task AUC
Fig. 2:
Comparison of pooled AUC and within-task AUC at 5k tokens on the primary corpus. Each horizontal line connects a predictor’s pooled and within-task performance. Counts: issue features plus prefix action counts. Embeddings: frozen sentence embeddings of the issue and initial step. Task rate: empirical solve fraction computed from a reserved half of each task’s attempts (evaluated across tasks with at least four attempts and averaged over three random splits). The dashed line marks random ranking (0.50).
IV-C
2
Task-conditional and cross-setting training
To test whether removing between-task variance during training uncovers attempt-level signal, we evaluate task-conditional logistic regression fit directly on mixed-outcome tasks. At
20
​
k
20\text{k}
tokens on the primary corpus, the conditional model achieves a within-task AUC of
0.50
0.50
[
0.49
,
0.51
]
[0.49,0.51]
across
38,447
38,447
successful-failed pairs drawn from
1,737
1,737
mixed-outcome tasks. The conditional model’s
90
%
90\%
task-bootstrap interval
[
0.49
,
0.51
]
[0.49,0.51]
falls entirely inside both the
[
0.45
,
0.55
]
[0.45,0.55]
and
[
0.47
,
0.53
]
[0.47,0.53]
TOST equivalence bounds, while the within-task label-permutation control remains centered at chance (
0.50
0.50
[
0.49
,
0.51
]
[0.49,0.51]
).
Across the three Open-SWE settings at
20
​
k
20\text{k}
tokens, conditional within-task AUC is
0.50
0.50
[
0.48
,
0.52
]
[0.48,0.52]
for OpenHands/Qwen3.5,
0.51
0.51
[
0.49
,
0.53
]
[0.49,0.53]
for OpenHands/MiniMax-M2.5, and
0.48
0.48
[
0.45
,
0.52
]
[0.45,0.52]
for SWE-agent/Qwen3.5, with all three
95
%
95\%
confidence intervals spanning
0.50
0.50
. Both OpenHands settings pass the within-task permutation control and have
90
%
90\%
confidence intervals falling strictly within the
[
0.47
,
0.53
]
[0.47,0.53]
equivalence bound (we refrain from formal TOST equivalence claims on SWE-agent/Qwen3.5 because its permutation control deviated from
0.50
0.50
). Evaluating cross-setting transfer at
20
​
k
20\text{k}
tokens, with overlapping repositories and task identifiers held out, likewise yields within-task AUCs of at most
0.50
0.50
across all three transfer pairs (SWE-agent/Qwen3.5 to OpenHands/Qwen3.5, and the primary setting to both SWE-agent/Qwen3.5 and OpenHands/MiniMax-M2.5).
IV-C
3
Adapted neural monitor
Table
II
reports the three-seed evaluation of the LoRA-adapted Qwen3-0.6B monitor across
32,406
32,406
attempts at the
20
​
k
20\text{k}
landmark. Across
16,818
16,818
successful-failed pairs from
859
859
mixed-outcome tasks, the issue-plus-prefix monitor achieves a mean within-task AUC of
0.50
0.50
[
0.48
,
0.51
]
[0.48,0.51]
. Performance remains near
0.50
0.50
within every individual repository fold and training seed, and weighting each mixed-outcome task equally produces identical results. As expected under balanced within-task pair sampling, the issue-only reference arm converges to the analytical baseline (
AUC
within
=
0.500
\mathrm{AUC}_{\mathrm{within}}=0.500
, log loss
=
0.693
=0.693
).
The neural monitor’s
90
%
90\%
repository-and-seed bootstrap interval
[
0.48
,
0.51
]
[0.48,0.51]
lies strictly within the
[
0.45
,
0.55
]
[0.45,0.55]
equivalence bound.
TABLE II:
Three-seed LoRA-adapted Qwen3-0.6B evaluation at 20k tokens across three repository-disjoint folds (311, 285, and 263 mixed-outcome tasks). Metrics are averaged across seeds rather than pooled across seed scores; brackets show 95% repository-and-seed bootstrap intervals for
AUC
within
\mathrm{AUC}_{\mathrm{within}}
. Lower log loss is better.
Fold
Input
Pooled AUC
Within-task AUC
Log loss
1
Issue
0.526
0.500 [0.499, 0.501]
0.693
1
Issue + prefix
0.523
0.500 [0.476, 0.526]
1.788
2
Issue
0.513
0.500 [0.499, 0.500]
0.693
2
Issue + prefix
0.504
0.496 [0.475, 0.517]
1.012
3
Issue
0.527
0.500 [0.497, 0.501]
0.693
3
Issue + prefix
0.469
0.490 [0.467, 0.513]
0.879
IV-C
4
Stratification by task solvability and late-trajectory signals
To test whether early attempt-level discrimination emerges on easier issues where failures might reflect avoidable early missteps, Table
III
stratifies mixed-outcome tasks at
20
​
k
20\text{k}
tokens into low (
<
25
%
<25\%
), medium (
25
​
–
​
75
%
25\text{--}75\%
), and high (
>
75
%
>75\%
) empirical solve-rate tiers. Across all three tiers, within-task AUC ranges from
0.49
0.49
to
0.51
0.51
for the count-based model and from
0.49
0.49
to
0.50
0.50
for the three-seed neural monitor, with every confidence interval containing
0.50
0.50
. High-solvability tasks therefore show the same near-chance early ranking as harder tasks.
TABLE III:
Within-task AUC at 20k tokens stratified by empirical task solve rate
p
p
: low (
p
<
0.25
p<0.25
), medium (
0.25
≤
p
≤
0.75
0.25\leq p\leq 0.75
), and high (
p
>
0.75
p>0.75
). Count denotes the primary-corpus issue-plus-prefix count model (95% task-bootstrap CIs); Neural denotes the three-seed Qwen3-0.6B mean (95% repository-and-seed CIs). All intervals contain
0.50
0.50
. Strata are descriptive post-hoc tiers.
Predictor
Stratum
Tasks
Pairs
AUC [95% interval]
Count
Low-pass
373
5,545
0.513 [0.484, 0.541]
Count
Medium-pass
800
23,378
0.488 [0.476, 0.502]
Count
High-pass
564
9,524
0.496 [0.475, 0.519]
Neural
Low-pass
170
2,188
0.504 [0.464, 0.544]
Neural
Medium-pass
405
10,966
0.491 [0.473, 0.509]
Neural
High-pass
284
3,664
0.503 [0.475, 0.532]
To verify that successful and failed trajectories on the same task do eventually diverge by completion, we compute an oracle end-of-run diagnostic measuring
reference-hunk recall
(the fraction of ground-truth patch diff hunks overlapped by the agent’s final edits, scored as
0
0
when no patch is produced). At run termination, reference-hunk recall achieves a within-task AUC of
0.62
0.62
[
0.61
,
0.64
]
[0.61,0.64]
, confirming that attempt-level divergence materializes over the full episode even though it remains undetectable from prefix representations at
20
​
k
20\text{k}
tokens.
Answer to RQ2:
Across initial-turn frozen embeddings (5k tokens) as well as 20k-token action-count models, task-conditional rankers, cross-setting transfers, and the three-seed Qwen3-0.6B neural evaluation (
AUC
within
=
0.50
\mathrm{AUC}_{\mathrm{within}}=0.50
[
0.48
,
0.51
]
[0.48,0.51]
), early prefixes provide near-chance discrimination between successful and failed attempts on the same task across all solvability tiers.
IV-D
RQ3: Evaluating restart policies under shared token budgets
To understand how early failure scores behave when deployed as stopping rules (RQ3), Table
IV
compares learned restart (stopping active runs scoring below the median eligible score at
20
​
k
20\text{k}
tokens) against matched random restart. In the uncapped replay regime, solve-rate differences between learned and random restarting are negligible across all four settings (within
0.20
0.20
percentage points): because unconstrained replacement attempts run to completion without budget truncation and within-task ranking is near chance, replacing an active attempt on a given task preserves the task’s expected solve rate. Under a shared
75
​
k
75\text{k}
-token cap, however, the solve-rate differential
V
⁡
(
L
)
−
V
⁡
(
R
)
V(L)-V(R)
spans
−
0.66
-0.66
to
+
1.98
+1.98
percentage points, favoring learned restart in both Qwen3.5 settings (
+
1.98
+1.98
and
+
0.77
+0.77
percentage points) while favoring random restart in the primary and MiniMax settings. Figure
3
contrasts these
75
​
k
75\text{k}
learned-versus-random differentials (blue) against the corresponding comparisons with uninterrupted continuation (red).
TABLE IV:
Restart replay at the 20k-token landmark using the median eligible-score threshold. Solve rates are percentages;
Δ
\Delta
is learned minus matched random restart in percentage points, with 95% repository-bootstrap confidence intervals.
Setting
Continue
Learned
Δ
\Delta
[95% interval]
OH / Qwen3-Coder
46.15
41.53
−
0.458
-0.458
[
−
0.677
-0.677
,
−
0.219
-0.219
]
SA / Qwen3.5
28.71
20.66
+
1.984
+1.984
[
+
1.313
+1.313
,
+
2.600
+2.600
]
OH / Qwen3.5
27.19
20.16
+
0.768
+0.768
[
+
0.302
+0.302
,
+
1.221
+1.221
]
OH / MiniMax-M2.5
41.05
35.76
−
0.663
-0.663
[
−
1.014
-1.014
,
−
0.333
-0.333
]
Fig. 3:
Solve-rate difference (in percentage points) between median-threshold learned restart and matched random restart (blue), and between learned restart and uninterrupted continuation (red), evaluated at the 20k-token landmark under a shared 75k-token cap. Error bars indicate 95% repository-bootstrap confidence intervals (5,000 draws), with positive values favoring learned restart. While learned restart outperforms random restart in the two Qwen3.5 settings, uninterrupted continuation outperforms learned restart across all four settings.
IV-D
1
Between-task selection drives the 75k learned-versus-random differential
Applying the exact decomposition from Eqs. (
4
)–(
6
) at the median threshold explains how learned restarting can outperform matched random restarting despite near-chance within-task AUC. As shown in Table
V
, the between-task selection term
Δ
between
\Delta_{\mathrm{between}}
(
−
0.70
-0.70
to
+
1.75
+1.75
percentage points) matches the sign of the total differential
V
⁡
(
L
)
−
V
⁡
(
R
)
V(L)-V(R)
and exceeds the magnitude of the within-task term
Δ
within
\Delta_{\mathrm{within}}
in every setting. By contrast,
Δ
within
\Delta_{\mathrm{within}}
remains small across all four corpora (
−
0.11
-0.11
to
+
0.24
+0.24
percentage points) and never determines the direction of the overall policy difference.
TABLE V:
Exact decomposition of learned minus matched random solve rate (in percentage points) at the 20k landmark under a 75k-token cap. Task means center over attempts active at 20k and normalize by all starting attempts. Between-task selection (
Δ
between
\Delta_{\mathrm{between}}
) governs the sign in every setting; components are rounded independently.
Setting
Total
Between
Within
OH / Qwen3-Coder
−
0.458
-0.458
−
0.494
-0.494
+
0.036
+0.036
OH / MiniMax-M2.5
−
0.663
-0.663
−
0.704
-0.704
+
0.042
+0.042
OH / Qwen3.5
+
0.768
+0.768
+
0.881
+0.881
−
0.113
-0.113
SA / Qwen3.5
+
1.984
+1.984
+
1.749
+1.749
+
0.235
+0.235
The task-level net gain
v
¯
t
=
G
¯
t
−
C
¯
t
\bar{v}_{t}=\bar{G}_{t}-\bar{C}_{t}
in Eq. (
5
) clarifies why
Δ
between
\Delta_{\mathrm{between}}
changes sign across settings. Because the learned policy assigns lower scores to harder tasks, it concentrates stops on tasks where both the replacement success rate within the remaining
55
​
k
55\text{k}
tokens (
G
¯
t
\bar{G}_{t}
) and the original continuation success rate (
C
¯
t
\bar{C}_{t}
) are lower than the corpus average. Consequently, learned stopping yields less replacement credit than random stopping, but it also forfeits fewer original continuation successes. In the two Qwen3.5 settings, the reduction in forfeited continuation successes outweighs the reduction in replacement credit, producing a net positive
Δ
between
\Delta_{\mathrm{between}}
purely through task-level stopping allocation.
IV-D
2
Uninterrupted continuation dominates the efficiency frontier
Whereas comparing learned against random restart evaluates how a fixed stopping quota is distributed across runs, comparing against uninterrupted continuation tests whether cold restarting saves compute or improves resolution overall. Extending replay across all seven score-percentile thresholds, four settings, and four hard token caps yields
224
224
learned and random restart configurations at the
20
​
k
20\text{k}
decision point (Table
VI
). Under the primary
75
​
k
75\text{k}
-token cap, where replacement runs receive
55
​
k
55\text{k}
residual tokens, uninterrupted continuation achieves both a strictly higher solve rate and a strictly lower mean transcript-token cost than every learned and random restart configuration across all four settings (
56
56
of
56
56
configurations). In SWE-agent/Qwen3.5, for example, continuation resolves
28.71
%
28.71\%
of starting attempts within the
75
​
k
75\text{k}
cap (down from
47.30
%
47.30\%
uncapped across shared tasks, as many SWE-agent runs exceed
75
​
k
75\text{k}
tokens) at a mean expenditure of
68.10
​
k
68.10\text{k}
tokens, whereas median learned restart resolves
20.66
%
20.66\%
at a mean expenditure of
69.93
​
k
69.93\text{k}
tokens. This dominance persists at the
100
​
k
100\text{k}
-token cap (
80
​
k
80\text{k}
residual tokens), where continuation Pareto-dominates
55
55
of
56
56
configurations, leaving only a single boundary point for OpenHands/MiniMax (
2
2
nd-percentile threshold, which adds less than
0.01
0.01
percentage points in solve rate at an added cost of
376
376
mean tokens). Across all
224
224
tested configurations spanning
B
∈
{
30
​
k
,
50
​
k
,
75
​
k
,
100
​
k
}
B\in\{30\text{k},50\text{k},75\text{k},100\text{k}\}
, continuation Pareto-dominates
216
216
configurations, with the other seven non-dominated cases being exact ties at the
30
​
k
30\text{k}
cap.
TABLE VI:
Cost-solve comparisons against uninterrupted continuation at the 20k-token landmark (56 restart configurations per cap across seven thresholds, four settings, and learned vs. matched random policies). Ties match continuation in both cost and solve rate. The sole non-dominated point is learned restart for OH/MiniMax at 100k (2nd-percentile threshold:
+
0.0033
+0.0033
percentage points at
+
376
+376
mean tokens).
Cap
Dominated
Tied
Distinct trade-offs
30k
49
7
0
50k
56
0
0
75k
56
0
0
100k
55
0
1
Two coupled budget mechanics explain why cold restarts simultaneously lower solve rates and increase mean token consumption under a shared cap
B
B
. First, terminating a run at landmark
b
=
20
​
k
b=20\text{k}
restricts the replacement attempt to a residual budget of
B
−
b
B-b
tokens (
R
j
=
Y
j
​
𝟏
​
(
L
j
≤
B
−
b
)
R_{j}=Y_{j}\mathbf{1}(L_{j}\leq B-b)
), whereas continuation permits the initial run to utilize the full cap
B
B
. At tighter caps (
B
=
30
​
k
B=30\text{k}
and
50
​
k
50\text{k}
, leaving
10
​
k
10\text{k}
and
30
​
k
30\text{k}
residual tokens), Fig.
1
(right) shows that
91
%
​
–
​
100
%
91\%\text{--}100\%
of coding trajectories require more than
B
−
b
B-b
tokens to finish, rendering cold replacements nearly guaranteed to truncate prior to patch submission. Even at
B
=
75
​
k
B=75\text{k}
and
100
​
k
100\text{k}
, replacement trajectories that would have succeeded between
B
−
b
B-b
and
B
B
tokens are forfeited. Second, aborting an active run at
b
b
forfeits the initial
20
​
k
20\text{k}
tokens invested in repository exploration and forces the replacement attempt to repeat setup and localization from scratch, driving combined token expenditure
K
j
=
b
+
min
⁡
(
L
j
,
B
−
b
)
K_{j}=b+\min(L_{j},B-b)
above the cost of allowing moderate-length original attempts to finish naturally.
Answer to RQ3:
Under a shared
75
​
k
75\text{k}
-token cap, learned stopping outperforms matched random restart by up to
1.98
1.98
percentage points through between-task stopping selection, while attempt-level selection contributes minimally. Against uninterrupted continuation, however, cold restarts achieve lower solve rates at higher mean token costs across the
75
​
k
75\text{k}
and
100
​
k
100\text{k}
frontiers (
111
111
of
112
112
configurations, and
216
216
of
224
224
configurations across all tested caps), showing that improvements over random restart do not establish compute savings.
V
Discussion
Evaluating runtime interventions in autonomous software engineering requires connecting task-level difficulty with attempt-level discrimination and budget-constrained policy mechanics. Our findings explain why strong cross-task ranking does not translate into effective cold restarts under shared token budgets.
The timing bottleneck of trajectory-level signals
Comparing early prefixes with later checkpoints clarifies why attempt-level discrimination is difficult in repository-level coding. On the primary corpus,
87.51
%
87.51\%
of active runs have already executed a detected test command and
32.80
%
32.80\%
have a detected edit action by
20
​
k
20\text{k}
transcript tokens. Thus, the near-chance within-task discrimination observed at
20
​
k
20\text{k}
tokens (
AUC
within
≈
0.50
\mathrm{AUC}_{\mathrm{within}}\approx 0.50
) cannot be explained simply by an absence of early test execution. Rather, detecting an early test invocation or edit action does not establish whether the interaction was diagnostic or whether its outcome distinguished eventual task resolution from failure. Measurable within-task separation emerges only at later landmarks, rising from
0.52
0.52
at
30
​
k
30\text{k}
tokens and
0.54
0.54
at
40
​
k
40\text{k}
tokens to
0.56
0.56
at
60
​
k
60\text{k}
tokens, and at run completion, where reference-hunk recall reaches a within-task AUC of
0.62
0.62
. By those later stages, however, either a substantial fraction of the token budget has been spent or most runs have already terminated. Early failure prediction therefore faces a fundamental timing tension: at landmarks early enough to leave ample residual budget for a replacement attempt, observed prefix signals do not separate competing runs on the same issue.
Why task-level selection confounds stopping baselines
When a monitor primarily captures static issue difficulty, score thresholding acts as an implicit task filter. Under a shared cap, learned stopping concentrates aborts on hard tasks where continuation rarely succeeds, whereas matched random stopping aborts easy and hard tasks alike, forfeiting impending successes on tractable issues (
Δ
between
>
0
\Delta_{\mathrm{between}}>0
) despite near-chance attempt ranking (
AUC
within
≈
0.50
\mathrm{AUC}_{\mathrm{within}}\approx 0.50
). For the same reason, mid-run
abort-only
termination wastes
20
​
k
20\text{k}
tokens executing a task filter that could be applied pre-execution at zero token cost. Against uninterrupted continuation, forfeiting initial exploration while compressing the residual budget causes cold restarts to underperform across the budget frontier.
Designing compute-efficient agent interventions
Separating task difficulty from attempt progress points to two compute-management strategies:
1) Pre-execution routing and budgeting:
Because static signals rank difficulty before execution, they naturally support up-front token provisioning
[
9
]
and solver routing
[
22
]
. On shared Qwen3.5 tasks, scaffold choice alone shifts solve rates by
14.06
14.06
percentage points (SWE-agent
47.30
%
47.30\%
vs. OpenHands
33.24
%
33.24\%
), dwarfing the at most
1.98
1.98
percentage-point gain of mid-run restarts and motivating pre-execution routing across frameworks.
2) State-preserving recovery:
Because cold prefixes lack attempt-level signal, retaining intermediate edits and test diagnostics is essential to avoid repeating exploration, explaining why state-preserving recovery substantially outperforms cold restarts
[
7
]
and motivating cross-framework context transfer when runs stall.
Evaluation standards for mining agent traces
As public corpora of agent trajectories grow
[
11
,
12
]
, runtime monitoring studies should evaluate both attempt-level discrimination and net compute efficiency. Specifically, predictive evaluations should report within-task AUC (
AUC
within
\mathrm{AUC}_{\mathrm{within}}
) across repeated attempts alongside pre-execution issue baselines and permutation controls. Policy evaluations under shared token budgets should compare proposed stopping rules against both matched random stopping and uninterrupted continuation, decomposing outcomes into between-task and within-task selection to verify genuine attempt-level value.
VI
Threats to Validity
Internal validity
Because our study mines public execution corpora
[
11
,
12
]
, outcome labels and trajectory contents reflect the original benchmark harnesses and execution environments. To guard against data-cleaning artifacts or estimation bias, we audited source task identifiers for text consistency and evaluated within-task label-permutation controls across all conditional modeling pipelines; permutation controls centered at chance (
0.50
0.50
) in the primary and OpenHands settings and identified the calibration deviation in SWE-agent/Qwen3.5, where we refrained from formal equivalence claims.
Construct validity
We measure computational progress in transcript tokens to standardize comparisons across corpora; however, transcript length abstracts away provider-level caching discounts and wall-clock tool execution latency. Our neural monitor adapts the single-landmark terminal-outcome classifier from FailFast–RestartSmart
[
7
]
, omitting intermediate test supervision and state-preserving edit transfer to isolate the predictive signal of raw execution prefixes and the mechanics of cold restarts; additionally, the editor-tool heuristic used to include an earlier prefix message can match file-view operations alongside code modifications. Recorded-attempt replay evaluates binary task resolution under hard token caps, assigning zero credit to partial edits that exceed the residual budget, and released task-category labels in Open-SWE-Traces may reflect post-hoc curation rather than metadata available at issue creation.
External validity
Our findings are scoped to four open-weight model-framework settings on Python-centric repository benchmarks evaluated with linear count and embedding classifiers alongside a
0.6
​
B
0.6\text{B}
-parameter neural monitor. Within-task discrimination requires mixed-outcome tasks by definition. Monitors that probe internal model representations
[
20
,
6
]
or incorporate sequential verifier feedback and state-preserving recovery
[
19
,
7
]
may exhibit different discrimination profiles.
Conclusion validity
Cluster-bootstrap confidence intervals resample out-of-fold predictions at the cluster level rather than refitting models per bootstrap draw. Subgroup and multi-landmark sensitivity checks apply Holm–Bonferroni multiplicity adjustments
[
40
]
, whereas confidence intervals at the primary
20
​
k
20\text{k}
landmark are reported unadjusted. Finally, Pareto dominance across the
224
224
budget-threshold configurations is evaluated on empirical replay point estimates.
VII
Conclusion
Early failure prediction benefits autonomous coding agents only when it helps decide whether to abandon an active attempt, rather than merely identifying which software issues are difficult. Mining
147,002
147,002
execution traces across four model-framework settings, we find that early execution prefixes add minimal predictive signal beyond static task context. Across early decision points, initial-turn frozen embeddings (
5
​
k
5\text{k}
tokens) as well as
20
​
k
20\text{k}
-token action-count models, task-conditional rankers, and a three-seed LoRA-adapted Qwen3-0.6B monitor (
32,406
32,406
attempts) all yield within-task discrimination near chance (
AUC
within
≈
0.50
\mathrm{AUC}_{\mathrm{within}}\approx 0.50
), including across high-solvability tasks.
Evaluating stopping rules through budget-constrained replay shows why predictive ranking and policy efficiency must be assessed together. Under a shared
75
​
k
75\text{k}
-token cap, learned stopping outperforms matched random restart by up to
1.98
1.98
percentage points in two settings, but exact decomposition reveals that this gain is driven by between-task stopping allocation rather than within-task failure detection. More importantly, uninterrupted continuation achieves higher solve rates at lower mean token cost than cold restarts across the
75
​
k
75\text{k}
and
100
​
k
100\text{k}
frontiers (
111
111
of
112
112
configurations, and
216
216
of
224
224
configurations across all tested caps). Future early-stopping and recovery methods should therefore evaluate discrimination within repeated attempts on the same task and demonstrate net compute savings relative to uninterrupted continuation.
References
[1]
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan
(2024)
Swe-bench: can language models resolve real-world github issues?
.
In
International Conference on Learning Representations
,
Vol.
2024
,
pp. 54107–54157
.
Cited by:
§I
,
§II
.
[2]
J. Yang, C. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press
(2024)
Swe-agent: agent-computer interfaces enable automated software engineering
.
Advances in Neural Information Processing Systems
37
,
pp. 50528–50652
.
Cited by:
§I
,
§II
.
[3]
X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan, Y. Song, B. Li, J. Singh,
et al.
(2025)
Openhands: an open platform for ai software developers as generalist agents, 2024
.
URL https://arxiv. org/abs/2407.16741
2
(
5
).
Cited by:
§I
,
§II
.
[4]
D. Pham, K. Katevas, A. S. Shamsabadi, and H. Haddadi
(2026)
AgentStop: terminating local AI agents early to save energy in consumer devices
.
Note:
arXiv:2605.15206v1
External Links:
Link
Cited by:
§I
,
§II
.
[5]
S. Cho, F. C. Fernandez, U. Mohammed, Z. Wu, K. D. Costa, I. Wicaksono, and A. Koshiyama
(2026)
Automata from agent traces: failure and next-step prediction
.
Note:
arXiv:2608.23670v1
External Links:
Link
Cited by:
§I
,
§II
.
[6]
A. Silva, H. Tu, and M. Monperrus
(2026)
Latent programming horizons in coding agents
.
Note:
arXiv:2607.05188v1
External Links:
Link
Cited by:
§I
,
§II
,
§VI
.
[7]
C. Wang, Y. Lyu, J. He, Z. Yang, C. Zhong, Y. Harel, and D. Lo
(2026)
Fail-fast, restart-smart: early failure prediction and restart for SWE agentic tasks
.
Note:
arXiv:2608.03222v1
External Links:
Link
Cited by:
§I
,
§II
,
§III-E
,
§V
,
§VI
,
§VI
.
[8]
T. Mehtiyev and W. Assunção
(2026)
Beyond resolution rates: behavioral drivers of coding agent success and failure
.
Note:
arXiv:2604.02547v1
External Links:
Link
Cited by:
§I
,
§II
.
[9]
M. EsfandyariDoulabi, L. Arkoh, B. Tadesse, V. Patel, M. Sharma, M. d’Amorim, and W. Assunção
(2026)
Disentangling task difficulty from run-level failure in agent failure prediction
.
Note:
arXiv:2610.05572v1
External Links:
Link
Cited by:
§I
,
§II
,
§V
.
[10]
Y. U. Bulut
(2026)
It’s the problem, not the path: budget and difficulty confounds in LLM reasoning trajectories
.
Note:
arXiv:2609.03436v1
External Links:
Link
Cited by:
§I
,
§II
.
[11]
Nebius
(2026)
SWE-rebench OpenHands Trajectories
.
Note:
Hugging Face dataset
External Links:
Link
Cited by:
§I
,
§II
,
§II
,
§III-A
,
§V
,
§VI
.
[12]
NVIDIA
(2026)
Open-SWE-Traces
.
Note:
Hugging Face dataset
External Links:
Link
Cited by:
§I
,
§II
,
§III-A
,
§III-D
,
§V
,
§VI
.
[13]
R. Robbes, T. Matricon, T. Degueule, A. Hora, and S. Zacchiroli
(2026)
Promises, perils, and (timely) heuristics for mining coding agent activity
.
In
Proceedings of the 23rd International Conference on Mining Software Repositories
,
pp. 496–507
.
Cited by:
§II
.
[14]
X. Zhao, H. Li, S. Li, T. Zhao, E. T. Barr, F. Sarro, and H. Ye
(2026)
Failure as a process: an anatomy of CLI coding agent trajectories
.
Note:
arXiv:2607.09510v1
External Links:
Link
Cited by:
§II
.
[15]
A. Banerjee and P. Raichura
(2026)
Measuring cross-task behavioral consistency in language model agents
.
Note:
arXiv:2608.13598v1
External Links:
Link
Cited by:
§II
.
[16]
Y. Guo, Y. Xiao, J. M. Zhang, M. Harman, Y. Lou, Y. Liu, and Z. Chen
(2026)
EET: experience-driven early termination for cost-efficient software engineering agents
.
Note:
arXiv:2601.05777v2
External Links:
Link
Cited by:
§II
.
[17]
A. Baidya, X. Liang, R. Guo, X. Gao, and K. Das
(2026)
When evidence is sparse: weakly supervised early failure alerting in dialogs and LLM-agent trajectories
.
Note:
arXiv:2606.05414v1
External Links:
Link
Cited by:
§II
.
[18]
Y. Lin, Z. Wang, M. Liu, Y. Shan, L. Bai, J. Zhang, X. Jin, B. Chen, J. Su, X. Wang, J. Pei, and M. Li
(2026)
BAGEN: are LLM agents budget-aware?
.
Note:
arXiv:2606.00198v1
External Links:
Link
Cited by:
§II
.
[19]
S. Sadhuka, D. Prinster, C. Fannjiang, G. Scalia, B. Berger, A. Regev, and H. Wang
(2026)
E-valuator: reliable agent verifiers with sequential hypothesis testing
.
Note:
arXiv:2512.03109v2
External Links:
Link
Cited by:
§II
,
§VI
.
[20]
K. Ruan, Z. Huang, Z. Zhou, Q. Wei, J. Lin, X. Wang, and H. Sun
(2026)
Doomed from the start: early abort of LLM agent episodes via a recall-controlled probe cascade
.
Note:
arXiv:2607.06503v2
External Links:
Link
Cited by:
§II
,
§VI
.
[21]
M. Luby, A. Sinclair, and D. Zuckerman
(1993)
Optimal speedup of las vegas algorithms
.
Information Processing Letters
47
(
4
),
pp. 173–180
.
Cited by:
§II
.
[22]
I. Bhola, A. Krishnan, and Mukunda NS
(2026)
Scrouting: cost-aware routing of coding agents by scouting the repository first
.
Note:
arXiv:2608.04804v1
External Links:
Link
Cited by:
§II
,
§V
.
[23]
Qwen Team
(2025)
Qwen3-Coder-480B-A35B-Instruct
.
Note:
Hugging Face model card
External Links:
Link
Cited by:
§III-A
.
[24]
I. Badertdinov, A. Golubev, M. Nekrashevich, A. Shevtsov, S. Karasik, A. Andriushchenko, M. Trofimova, D. Litvintseva, and B. Yangel
(2026)
Swe-rebench: an automated pipeline for task collection and decontaminated evaluation of software engineering agents
.
Advances in Neural Information Processing Systems
38
.
Cited by:
§III-A
.
[25]
Qwen Team
(2026)
Qwen3.5-122B-A10B
.
Note:
Hugging Face model card
External Links:
Link
Cited by:
§III-A
.
[26]
MiniMax
(2026)
MiniMax-M2.5
.
Note:
Hugging Face model card
External Links:
Link
Cited by:
§III-A
.
[27]
M. S. Ridout, C. G. Demétrio, and D. Firth
(1999)
Estimating intraclass correlation for binary data
.
Biometrics
55
(
1
),
pp. 137–148
.
Cited by:
§III-C
.
[28]
T. Gneiting and A. E. Raftery
(2007)
Strictly proper scoring rules, prediction, and estimation
.
Journal of the American statistical Association
102
(
477
),
pp. 359–378
.
Cited by:
§III-C
.
[29]
J. A. Hanley and B. J. McNeil
(1982)
The meaning and use of the area under a receiver operating characteristic (roc) curve.
.
Radiology
143
(
1
),
pp. 29–36
.
Cited by:
§III-C
.
[30]
C. A. Field and A. H. Welsh
(2007)
Bootstrapping clustered data
.
Journal of the Royal Statistical Society Series B: Statistical Methodology
69
(
3
),
pp. 369–390
.
Cited by:
§III-C
.
[31]
N. E. Breslow, N. E. Day, and E. Heseltine
(1980)
Statistical methods in cancer research
.
Cited by:
§III-D
.
[32]
D. J. Schuirmann
(1987)
A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability
.
Journal of pharmacokinetics and biopharmaceutics
15
(
6
),
pp. 657–680
.
Cited by:
§III-D
.
[33]
D. Lakens
(2017)
Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. social psychological and personality science, 8 (4), 355–362
.
Cited by:
§III-D
.
[34]
N. Reimers and I. Gurevych
(2019)
Sentence-bert: sentence embeddings using siamese bert-networks
.
In
Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (EMNLP-IJCNLP)
,
pp. 3982–3992
.
Cited by:
§III-D
.
[35]
W. Wang, F. Wei, L. Dong, H. Bao, N. Yang, and M. Zhou
(2020)
Minilm: deep self-attention distillation for task-agnostic compression of pre-trained transformers
.
Advances in neural information processing systems
33
,
pp. 5776–5788
.
Cited by:
§III-D
.
[36]
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv,
et al.
(2025)
Qwen3 technical report
.
arXiv preprint arXiv:2505.09388
.
Cited by:
§III-E
.
[37]
E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen
(2021)
Lora: low-rank adaptation of large language models
.
arXiv preprint arXiv:2106.09685
.
Cited by:
§III-E
.
[38]
D. Sculley
(2010)
Combined regression and ranking
.
In
Proceedings of the 16th ACM SIGKDD international conference on Knowledge discovery and data mining
,
pp. 979–988
.
Cited by:
§III-E
.
[39]
E. M. Kitagawa
(1955)
Components of a difference between two rates
.
Journal of the american statistical association
50
(
272
),
pp. 1168–1194
.
Cited by:
§III-F
.
[40]
S. Holm
(1979)
A simple sequentially rejective multiple test procedure
.
Scandinavian journal of statistics
,
pp. 65–70
.
Cited by:
§IV-B
,
§VI
.