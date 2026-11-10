---
title: Hard Issue, Weak Model, or Bad Run?Rethinking Failure Prediction for Coding
  Agents
id: hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents
tags:
- code-llm-confidence-positioning-d82d00
- w3-forward-citation
created: '2026-11-10T08:23:44.224159Z'
updated: '2026-11-10T08:25:30.204874Z'
source: https://arxiv.org/html/2611.08285
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:44.223555Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Agent failure predictors on SWE-bench Verified trajectories mostly predict
  issue difficulty (reference score 0.92 AUROC vs trajectory predictors about 0.62)
  and model ability, not the run; gain beyond difficulty and ability is statistically
  equivalent to zero (TOST +/-0.02, Holm over 50 comparisons). Oracle gap and per-issue
  model switching show no gain on held-out runs. Bears on L3 (routing) and F (evaluation
  validity) by analogy; no calibration of code-LLM confidence, no hidden-state probes
  (full text read: abstract, intro, setup).'
---

Hard Issue, Weak Model, or Bad Run?Rethinking Failure Prediction for Coding Agents
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2611.08285v1 [cs.SE] 05 Nov 2026
Hard Issue, Weak Model, or Bad Run?
Rethinking Failure Prediction for Coding Agents
Xingyue Shi
Affiliation:
NC State University
Raleigh, NC, USA
xshi22@ncsu.edu
Wesley K. G. Assunção
Affiliation:
NC State University
Raleigh, NC, USA
wguezas@ncsu.edu
Abstract
Trajectory-based failure predictors for software engineering (SE) agents read the partial trajectory of a run to flag whether it is going right or wrong.
If it is going wrong, the run can be stopped, retried, or switched to another model. We ask whether these predictors learn anything about the run itself.
On public SWE-bench Verified trajectories, where each model attempts each issue once, two run-independent factors dominate predictor performance.
The first is issue difficulty: a reference score that never looks at the run, only at how hard the issue is for other models, reaches 0.92 AUROC, whereas trajectory predictors reach about 0.62.
The second is model ability: within an issue, knowing which model ran predicts failure better than our predictors do, and the predictors largely reproduce the overall ability ranking of the models.
Beyond difficulty and ability, what predictors gain from the trajectory is statistically equivalent to zero.
This confusion carries over to the actions taken after a prediction.
Model switching is often motivated by the gap between the best single model’s resolution rate and an any-model oracle.
This gap is no larger than random variation alone produces.
Per-issue switching gains nothing on held-out runs.
In a repeated-run pilot, the same model often solves an issue in some runs and fails it in others.
Retrying thus has real room to repair failures, but it rescues only failures caused by a bad run, not those on an issue beyond the model’s ability.
Current predictors cannot tell the causes apart, as they mostly predict the issue and the model, not the run.
We call for failure prediction that explains why a run fails, evaluated on repeated-run benchmarks and in closed-loop, equal-budget settings.
Index Terms:
SE agents, failure prediction, trajectory monitoring, model routing, evaluation methodology
I
Introduction
Software engineering (SE) agents resolve repository issues by inspecting code, editing files, and running tests
[
1
,
2
]
.
Agent runs are usually long and often fail
[
3
,
4
]
.
A growing line of work therefore predicts failure while a run is still in progress and acts on the prediction: it stops the run to save tokens
[
5
,
6
]
, restarts the same model
[
3
]
, or hands the issue to another model
[
7
,
8
]
.
We focus on
trajectory-based
predictors, which read only what the agent has produced so far (its reasoning, commands, and tool outputs) and therefore apply to closed frontier models.
A prediction can guide the choice of action only if it explains why the current run is likely to fail, using evidence from that run.
A run can fail for three different reasons.
The
issue may be hard
, so that most models fail it;
the
model may be weak
, so that it fails many issues;
or this particular attempt may have gone wrong, a
bad run
, in which case the same model solves the same issue in other attempts.
This decomposition follows item response theory, which explains each outcome by the difficulty of the item and the ability of the respondent
[
9
,
10
,
11
]
, and the run-to-run variation observed when the same agent repeats a task
[
12
,
13
,
14
]
.
Each reason calls for a different action: a hard issue for stopping or human intervention, a weak model for switching to a stronger one, and only a bad run for retrying.
Existing work, however, rarely tells these three reasons apart.
We trace this to three assumptions that current practice takes for granted:
(i) that a predictor with a high AUROC has learned run-specific information, that is, it predicts failure from the state of the current run;
(ii) that the
oracle gap
, the success rate of any model minus that of the best single model, reflects issue-specific strengths that switching can exploit
[
15
]
; and
(iii) that an alarm marks a bad run, so that acting on it, for example by retrying, pays off
[
3
]
.
We question whether these assumptions hold.
Standard evaluations cannot test them: predictors are usually scored with metrics pooled over many issues, and often over many models
[
3
,
5
,
16
,
17
]
.
Such a score mixes issue difficulty and model ability into one number, so a high value does not show that the predictor has learned anything from the run.
Even with repeated runs, the score is dominated by comparisons between different issues
[
14
]
.
That work separates issue difficulty from run-level failure within each model but does not examine model ability as a cause of failure or test the evidence for switching.
On public leaderboard trajectories, each model attempts each issue once, so a bad run cannot be told from a hard issue or a weak model.
Easy
Hard
0
.5
1
.90
.10
(a) Hard issue?
P(success)
A
B
Any
AA
0
.5
1
.70
.60
.88
.91
(b) Weak model?
Flagged
(hard)
Missed
(easy)
0
.5
1
.10
.90
(c) Bad run?
Fig. 1:
A toy world in which each outcome depends only on the issue, the model, and a coin flip; values are probabilities, not empirical results. (a) Success on easy and hard issues. (b) Success with model A, model B, either model (Any), and A run twice (AA). (c) Retry success after a failure that a difficulty score flags (hard issue) or misses (easy issue, a bad run).
Fig.
1
shows how all three assumptions can fail in a toy world where each run is a coin flip whose success probability is set only by the issue and the model.
There is thus nothing run-specific to learn, and no model is better than another on particular issues, yet the usual evidence for each assumption still appears.
(a)
A high pooled AUROC does not require learning about the run.
Suppose a model succeeds with probability 0.9 on easy issues and 0.1 on hard ones, and the two kinds are equally common.
A score that only knows whether an issue is hard reaches 0.90 pooled AUROC, yet it cannot rank two runs of the same issue (0.50).
(b)
An oracle gap does not require issue-specific strengths.
Suppose model A succeeds with probability 0.7 and model B with 0.6 on every issue.
Taking whichever model succeeds solves
1
−
(
0.3
×
0.4
)
=
0.88
1-(0.3\times 0.4)=0.88
of the issues, 18 percentage points (pp) more than A alone, although A is the better choice on every issue.
With the same two attempts, running A twice does even better (0.91): the gap comes from a second attempt, not from a better-suited model.
(c)
An alarm need not mark a bad run.
In the world of (a), 90% of failures occur on hard issues (
0.45
0.45
of
0.50
0.50
), where a retry succeeds only 10% of the time; failures on easy issues are bad runs, which a retry fixes 90% of the time.
The difficulty score from (a) raises alarms on hard issues, so it flags the failures a retry rarely fixes and misses those it usually fixes.
We ask whether real agents behave like this toy world, turning each assumption into a research question:
RQ1:
Do failure predictors learn about the run, beyond issue difficulty and model ability?
RQ2:
Does the oracle gap reflect issue-specific strengths that switching can exploit?
RQ3:
Do alarms mark bad runs that a retry can fix?
On trajectories of seven recent models, outcomes of 23 models, and a public corpus with repeated runs, we find that real agents largely behave like the toy world, and the data support none of the three assumptions.
Beyond issue difficulty and model ability, what predictors gain from the trajectory is statistically equivalent to zero (RQ1).
The oracle gap is no larger than chance alone produces, and choosing a model for each issue from past runs brings no measurable gain on new runs (RQ2).
Bad runs are common enough for retrying to pay off, but current predictors can hardly target them (RQ3).
Rather than proposing another predictor, we question what current predictors predict.
Our answer is that they mostly predict the issue and the model, not the run, and that the evidence for acting on their alarms, whether by switching or by retrying, inherits the same confusion.
We show how each assumption can be tested with existing data (Section
IV
) and call for failure prediction that explains why a run fails, so that each failure is met with the action that can fix it.
II
Methodology
Data.
To study predictors where they are usually built, we use public leaderboard-style trajectories: mini-swe-agent runs on the 500 issues of SWE-bench Verified, in which each model attempts each issue once
[
18
,
19
]
.
They include 3,492 runs with known outcomes from seven models (Claude Haiku 4.5, Claude Opus 4.5 and 4.6, Gemini 3 Flash, GLM-5, GPT-5-mini, and MiniMax-M2.5), 994 of which fail.
We use the released resolved labels as failure labels and exclude two GPT-5.2 sources that contain identical transcripts with conflicting labels.
A companion release covers 25 models on the same issues
[
20
]
.
After the same exclusion, it gives the outcomes of 23 models (the 23-model data), to test whether the findings hold for a larger, more diverse set of models, and 16 models outside the seven, used only to estimate issue difficulty.
Predictors.
Our predictors mirror the design of Fail-Fast
[
3
]
.
A predictor reads a run’s trajectory after
t
∈
{
10
,
20
,
40
}
t\in\{10,20,40\}
completed steps, either the last eight steps (R8) or the full prefix (ALL), and outputs a failure score.
Earlier observation points leave more runs to act on but give less evidence, and the two windows contrast recent context with the full history.
Unlike Fail-Fast, a predictor in this work sees neither the issue text nor the name of the model, so whatever it learns comes from the trajectory alone, which may still reveal the issue and the model implicitly.
We train TF-IDF logistic regression, a choice also used in
[
14
]
, with issue-grouped five-fold cross-validation.
To check that the findings are not specific to a simple text model, we also fine-tune Qwen3-0.6B with LoRA on one fold, and pair each neural predictor with a logistic model on the same truncated text.
This yields 18 configurations: ten TF-IDF variants, covering the observation points, the windows, and the run subsets used to compare observation points, and four neural predictors with their paired logistic models.
All configurations enter the tests, and Table
I
shows two representative ones.
Unless noted, we report the 2,840 runs still running at step 20 (t20), since a predictor can act only on such runs.
Run-blind references.
To measure how much of a predictor’s performance requires the run at all, we compare it with scores that ignore what the agent did.
Issue difficulty
(
D
ext
D_{\mathrm{ext}}
) is the fraction of the 16 outside models that fail the issue, so it assigns every run of an issue the same score; since it relies on outcomes unavailable at deployment, it serves as a diagnostic rather than a practical predictor.
Model identity
(
M
M
) scores a run by its model’s failure rate on training issues, that is, by the model’s overall ability.
Length +
M
M
adds only the prefix length to
M
M
, testing whether a predictor learns more than how long the run has lasted.
Pairs.
To see where a predictor’s AUROC comes from, we decompose it by pair: AUROC is the fraction of failed–successful pairs that a predictor ranks correctly, that is, in which it scores the failed run higher.
We split these pairs into
cross-issue
pairs and
within-issue
pairs (same issue, different models), and call a within-issue pair
consistent
if the failed run comes from the overall weaker model and an
upset
otherwise.
A predictor that tracks the run should rank both kinds of within-issue pairs above chance, whereas a predictor that merely follows the ability ranking of the models ranks consistent pairs correctly and upsets incorrectly.
Tests.
Three of the claims rely on dedicated tests.
To claim that a predictor adds nothing beyond
D
ext
D_{\mathrm{ext}}
and
M
M
, we require the 90% interval of its AUROC gain to lie within a pre-specified
±
0.02
\pm 0.02
(equivalence test, Holm-corrected over 50 comparisons
[
21
,
22
]
).
To claim that it cannot tell which runs of an issue failed, we use a conditional logit
[
23
]
, which holds issue difficulty fixed and tests whether the score adds to
M
M
.
To claim that the oracle gap (issues solved by some model but not the best one) and the upset rate, often read as evidence of issue-specific strengths, do not exceed chance, we build a
no-specialization reference
.
It simulates outcomes in a world that matches the real models’ abilities and the issues’ difficulties, but in which every issue ranks the models identically, so that upsets and the gap arise only by chance.
We fit this world with the Rasch model
[
9
]
, which gives each model one ability and each issue one difficulty, and with the two-parameter logistic (2PL) model
[
24
]
, which also lets some issues separate the models more sharply and so leaves less to chance.
Repeated-run pilot.
Single-run data cannot tell specialization from luck, nor show what a retry brings.
We therefore use a public SWE-agent corpus with repeated runs
[
25
]
: two Llama models (70B and 8B), each run at least four times on each of 522 issues from SWE-bench-extra and SWE-bench dev.
To judge a choice on runs it has not seen, we split the runs of each model on each issue into two halves: half A is used to choose a model for each issue or to find upsets, and half B to measure success or check whether the upsets recur.
Because a single split is arbitrary, we average over 200 random splits, and we bootstrap issues, repeating the choice in every resample, to obtain intervals.
III
Preliminary Findings
TABLE I:
AUROC by type of pair, on 2,840 runs still running at step 20.
Within-issue pairs
Pooled
All
Consistent
Upset
Run-blind references
Issue difficulty (
D
ext
D_{\mathrm{ext}}
)
0.924
0.500
0.500
0.500
Model identity (
M
M
)
0.567
0.724
1.000
0.000
D
ext
D_{\mathrm{ext}}
+
M
M
0.929
0.718
0.869
0.317
Length +
M
M
0.607
0.648
0.756
0.373
Trajectory-based predictors
TF-IDF, last 8 steps (R8)
0.624
0.604
0.678
0.415
TF-IDF, full prefix (ALL)
0.630
0.610
0.687
0.416
III-A
Predictors Learn Mostly the Issue and the Model (RQ1)
A high AUROC is taken to mean that a predictor has learned run-specific information, yet the toy world in Fig.
1
(a) shows that a score can reach a high AUROC without learning anything about the run.
We therefore compare the predictors with run-blind references for issue difficulty and model ability (Table
I
) and test what they add beyond both.
Issue difficulty explains pooled AUROC.
Pooled AUROC is almost entirely a cross-issue measure.
Of the 494,109 failed–successful pairs in the test folds, 99.66% compare different issues, as also observed on repeated-run benchmarks
[
14
]
.
A score that recognizes hard issues can therefore score highly without seeing the run.
The difficulty score
D
ext
D_{\mathrm{ext}}
reaches 0.92 pooled AUROC, whereas the predictors reach only 0.62–0.63 and are not significantly better than length plus
M
M
(all ten 95% intervals of the difference contain 0).
Model ability explains within-issue AUROC.
Within an issue, the question becomes which model’s run failed, and knowing the model answers it better than the trajectory-based predictors do.
Model identity
M
M
reaches 0.72 within-issue AUROC, above both predictors (0.60–0.61), and 0.82 on the 23-model data.
By construction,
D
ext
D_{\mathrm{ext}}
scores 0.5 within an issue, and
M
M
scores 1 on consistent pairs and 0 on upsets.
The predictors are never told the model, yet they show the same pattern in weaker form.
They score 0.68–0.69 on consistent pairs but 0.42 on upsets, and all ten distinct TF-IDF configurations fall below 0.5 on upsets.
A predictor that follows the run should instead exceed 0.5 on both.
Ability matters more when models differ more, explaining 2.5% of outcome variance with seven models but about 10% with 23.
The trajectory adds nothing measurable beyond both.
Adding a predictor’s score to
D
ext
D_{\mathrm{ext}}
and
M
M
changes pooled AUROC by an amount equivalent to zero in all 18 configurations (e.g.,
−
0.001
-0.001
for the full-prefix predictor in Table
I
, 90% interval [
−
0.003
-0.003
, 0.000]).
Within issues, a conditional logit that holds issue difficulty fixed shows that adding the score to
M
M
does not help identify which runs of an issue failed in any configuration (e.g.,
−
0.011
-0.011
within-issue AUROC for the same predictor, 95% interval [
−
0.024
-0.024
, 0.002]).
Rasch
2PL
Observed
15
15
20
20
25
25
30
30
23 models
7 models
(a) Upset rate (%)
8
8
12
12
16
16
20
20
(b) Oracle gap (pp)
Fig. 2:
Observed values (red) versus the no-specialization reference, simulated with Rasch and 2PL models in which every issue ranks the models identically. Bars show the middle 95% of 500 simulations. (a) Upset rate, the share of one-success model pairs won by the weaker model. (b) Oracle gap, the resolution rate of any model minus that of the best single model.
III-B
The Oracle Gap Is Not a Gain from Switching (RQ2)
Switching presumes that a model failing an issue can be rescued by another model that is better on it, and the usual evidence is the oracle gap.
Fig.
1
(b) shows that such a gap can arise without issue-specific strengths; we test whether the real one does, and whether switching can turn it into a gain.
The oracle gap is not evidence of specialization.
The best single model solves 76.8% of the issues, whereas some model solves 86.8%, an oracle gap of 10.0 pp (12.4 pp with 23 models).
Upsets are also common.
When exactly one of two models solves an issue, the overall weaker model succeeds in 24.6% of cases (17.7% with 23 models).
Fig.
2
compares both quantities with the range that chance alone produces in the no-specialization reference.
For 7 and 23 models, the observed values lie within the 2PL range, and with 23 models the Rasch range lies even above them.
In none of the eight comparisons (oracle gap and upset rate, 7 and 23 models, Rasch and 2PL) is an observed value significantly above its reference after Holm correction.
The gap is therefore no evidence of specialization, though this does not show that specialization is absent.
The oracle gap is not an attainable gain.
For 45% of all failures (448 of 994) there is no model to switch to, since they occur on the 64 issues that none of the seven models solves.
Moreover, the oracle picks a model after seeing the outcomes, whereas a router must pick before.
Choosing before the run gains little, even with the issue’s own history.
In the repeated-run pilot, choosing for each issue the model that did better on its past runs (half A) gains only
+
0.09
+0.09
pp on new runs (half B) over always using the model that is better overall (Table
II
).
It gains little on new issues either.
A router trained on other issues predicts each model’s chance of solving a new issue from the model’s identity and the issue text, before any run, and picks the most promising model, yet it gains only
+
0.41
+0.41
pp over the best single model, the one with the highest resolution rate on the training issues.
Specialization is real but sparse.
If upsets were pure chance, an upset found in half A of the runs in the repeated-run pilot would recur in half B only at the rate the no-specialization reference predicts (19%).
Instead, 44% recur (
p
=
0.004
p=0.004
), indicating that some models are better on particular issues.
These recurring upsets, however, occur on only about 15 of the 522 issues.
We decompose the variation in outcomes across repeated runs into parts due to the issue, the model, their combination (specialization), and run-to-run variation.
Specialization accounts for only 4.6%, against 53% for issue difficulty and 42% for run-to-run variation.
Escalation gains come from the extra attempt.
On the seven-model data, escalating every failure to one fixed second model gains
+
6.91
+6.91
pp (Table
II
), and no other pair of models chosen in hindsight does better.
Because this policy makes no issue-specific choice, its gain comes from the second attempt, not from picking a better-suited model; choosing a model per issue alone adds only
+
0.41
+0.41
pp.
The gain also assumes a perfect failure detector.
RQ3 further asks what a second attempt with the same model can fix.
TABLE II:
Resolution rate of strategy A minus that of B (pp).
A vs. B
A
−
-
B [95% CI]
One attempt: choose a model per issue?
Choice from the issue’s past runs vs. one model
+
0.09
+0.09
[
−
0.36
-0.36
, 0.63]
Router for new issues vs. best single model
+
0.41
+0.41
[
−
1.83
-1.83
, 2.85]
One vs. two attempts: escalate after failure?
Escalation vs. best single model
+
6.91
+6.91
[
−
-
4.67, 9.15]
III-C
Alarms Miss the Runs a Retry Can Fix (RQ3)
Retrying after an alarm assumes that the failure is a bad run, that is, that the model can solve the issue and only this attempt went wrong.
If instead the issue is hard or the model is weak, a second run will likely fail again, and stopping, switching to a stronger model, or asking a human is the better action.
An alarm can therefore guide a retry only if it tells a bad run from a hard issue or a weak model.
In Fig.
1
(c), a difficulty score flags mostly hard issues; we test whether real alarms do too.
Bad runs are common.
If failures came only from hard issues and weak models, a model would fail an issue on every run.
In the repeated-run pilot, this is not the case.
The same model often solves an issue in some runs and fails it in others; this run-to-run variation accounts for 42% of the variation in outcomes, far more than specialization (4.6%; RQ2).
Each such failure is a bad run, since the same model solves the issue in other attempts, so a retry has a real chance to fix it.
Alarms cannot tell a bad run from a hard issue or a weak model.
An alarm should not only flag a likely failure but also indicate whether a retry can fix it.
The predictors’ scores, however, carry nothing measurable beyond issue difficulty and model identity (RQ1), and 64–82% of the variance of their scores lies between issues rather than within them.
Much like the difficulty score in Fig.
1
(c), a high score thus signals a hard issue or a weak model, where a retry is less likely to succeed, and says little about whether this run went wrong.
This is consistent with Fail-Fast
[
3
]
, in which a cold restart triggered by its predictor adds only 0.2 pp.
IV
Discussion
Rethinking failure prediction.
Our findings challenge three assumptions that current work on failure prediction for coding agents takes for granted.
A high AUROC, a large oracle gap, and an alarm can each look like evidence that prediction helps, yet each can arise from issue difficulty, model ability, or chance alone.
What these assumptions overlook is the
cause
of a failure, which decides whether stopping, switching, or retrying can help.
Future work can evaluate predictors more rigorously with three tests designed in this work that need only existing data.
First, report within-issue AUROC next to pooled AUROC and compare it with run-blind references for issue difficulty, model ability, and length.
Second, compare any oracle gap with a no-specialization reference and evaluate routers on held-out runs.
Third, judge an alarm by whether the action it triggers, such as a retry, fixes the failure, and compare actions at equal numbers of attempts.
Threats to validity.
The evidence comes mainly from released labels on one benchmark and scaffold, from trajectory-based predictors only, and partly from the repeated-run pilot with older models and a router with shallow issue features.
We have not yet measured how much specialization the no-specialization reference can detect, so non-rejection does not prove that specialization is absent.
V
Future Plans
These findings suggest that failure prediction should target the cause of a failure, not only the failure itself.
We plan three steps toward this goal.
First, we will collect repeated runs of recent models across more benchmarks and scaffolds, so that run-to-run variation can be separated from issue difficulty and model ability.
Second, we will build predictors that tell why a run fails, because each cause calls for a different action.
They will separate a hard issue, a weak model, and a bad run, so that an alarm can trigger stopping, switching, or retrying accordingly.
Third, we will evaluate predictors in a closed loop at equal budgets, counting false alarms and the cost of monitoring, and judge each by the decisions it improves rather than by its pooled AUROC.
References
[1]
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan,
“SWE-bench: Can language models resolve real-world GithHub issues?”
in
International Conference on Learning Representations
, 2024,
pp. 54 107–54 157.
[2]
OpenAI, “Introducing SWE-bench verified,”
https://openai.com/index/introducing-swe-bench-verified/
, 2024,
accessed: 2026.
[3]
C. Wang, Y. Lyu, J. He, Z. Yang, C. Zhong, Y. Harel, and D. Lo, “Fail-Fast,
Restart-Smart: Early failure prediction and restart for SWE agentic
tasks,”
arXiv preprint arXiv:2608.03222
, 2026.
[4]
T. Mehtiyev and W. Assunção, “Beyond resolution rates: Behavioral
drivers of coding agent success and failure,”
arXiv preprint
arXiv:2604.02547
, 2026.
[5]
D. Pham, K. Katevas, A. S. Shamsabadi, and H. Haddadi, “AgentStop:
Terminating local AI agents early to save energy in consumer devices,” in
Proceedings of the ACM Conference on AI and Agentic Systems
. Association for Computing Machinery, 2026, pp.
1051–1069.
[6]
Y. Shi, Z. Sun, J. Dong, C. Wan, D. Lo, and X. Gu, “EarlyEval: Cheaper agent
evaluation via early outcome prediction,”
arXiv preprint
arXiv:2609.02783
, 2026.
[7]
N. Kim and S. Yoo, “Atropos: Improving cost-benefit trade-off of LLM-based
agents under self-consistency with early termination and model hotswap,”
Proceedings of the ACM on Software Engineering
, vol. 3, no. ISSTA, pp.
1492–1512, 2026.
[8]
S. Son, S. Yoon, J. Tang, S. Wang, L. Wolf, and I. Bogunovic, “SWE-Router:
Routing in multi-turn agentic software engineering tasks,”
arXiv
preprint arXiv:2607.00053
, 2026.
[9]
G. Rasch,
Probabilistic models for some intelligence and attainment
tests.
Chicago: MESA Press, 1993.
[10]
P. Rodriguez, J. Barrow, A. Hoyle, J. P. Lalor, R. Jia, and J. Boyd-Graber,
“Evaluation examples are not equally informative: How should that change
NLP leaderboards?” in
Proceedings of the 59th Annual Meeting of the
Association for Computational Linguistics and the 11th International
Joint Conference on Natural Language Processing (Volume 1: Long Papers)
,
2021, pp. 4486–4503.
[11]
C. Ge, D. Kryvosheieva, D. Fried, U. Girit, and K. Hariharan, “Agent
psychometrics: Task-level performance prediction in agentic coding
benchmarks,”
arXiv preprint arXiv:2604.00594
, 2026.
[12]
S. Yao, N. Shinn, P. Razavi, and K. Narasimhan, “
τ
\tau
-bench: A benchmark for
tool-agent-user interaction in real-world domains,” in
The Thirteenth
International Conference on Learning Representations
, 2025, pp.
74 824–74 876.
[13]
B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, and
A. Mirhoseini, “Large language monkeys: Scaling inference compute with
repeated sampling,”
arXiv preprint arXiv:2407.21787
, 2024.
[14]
M. EsfandyariDoulabi, L. Arkoh, B. Tadesse, V. Patel, M. Sharma, M. d’Amorim,
and W. Assunção, “Disentangling task difficulty from run-level
failure in agent failure prediction,”
arXiv preprint
arXiv:2610.05572
, 2026.
[15]
K. Zhang, W. Yao, Z. Liu, Y. Feng, Z. Liu, R. R. N. Murthy, T. Lan, L. Li,
R. Lou, J. Xu, B. Pang, Y. Zhou, S. Heinecke, S. Savarese, H. Wang, and
C. Xiong, “Diversity empowers intelligence: Integrating expertise of
software engineering agents,” in
The Thirteenth International
Conference on Learning Representations
, 2025, pp. 86 691–86 714.
[16]
K. Ruan, Z. Huang, Z. Zhou, Q. Wei, J. Lin, X. Wang, and H. Sun, “Doomed from
the start: Early abort of LLM agent episodes via a recall-controlled probe
cascade,”
arXiv preprint arXiv:2607.06503
, 2026.
[17]
A. Silva, H. Tu, and M. Monperrus, “Latent programming horizons in coding
agents,”
arXiv preprint arXiv:2607.05188
, 2026.
[18]
SWE-agent contributors, “mini-swe-agent,”
https://github.com/SWE-agent/mini-swe-agent
, accessed: 2026.
[19]
tarsur385, “swebench-verified-trajectories,”
https://huggingface.co/datasets/tarsur385/swebench-verified-trajectories
,
accessed: 2026.
[20]
——, “swev-trm-trajectories-25models,”
https://huggingface.co/datasets/tarsur385/swev-trm-trajectories-25models
,
accessed: 2026.
[21]
D. J. Schuirmann, “A comparison of the two one-sided tests procedure and the
power approach for assessing the equivalence of average bioavailability,”
Journal of Pharmacokinetics and Biopharmaceutics
, vol. 15, no. 6, pp.
657–680, 1987.
[22]
S. Holm, “A simple sequentially rejective multiple test procedure,”
Scandinavian Journal of Statistics
, pp. 65–70, 1979.
[23]
G. Chamberlain, “Analysis of covariance with qualitative data,”
The
Review of Economic Studies
, vol. 47, no. 1, pp. 225–238, 1980.
[24]
A. Birnbaum, “Some latent trait models and their use in inferring an
examinee’s ability,”
Statistical Theories of Mental Test Scores
,
1968.
[25]
Nebius, “SWE-agent-trajectories,”
https://huggingface.co/datasets/nebius/SWE-agent-trajectories
,
accessed: 2026.