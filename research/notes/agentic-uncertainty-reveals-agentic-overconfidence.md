---
title: Agentic Uncertainty Reveals Agentic Overconfidence
id: agentic-uncertainty-reveals-agentic-overconfidence
tags:
- code-llm-confidence-positioning-d82d00
- locus-l3-confidence-routed-execution-and-update-after-failure
created: '2026-11-10T08:40:52.149578Z'
updated: '2026-11-10T09:27:35.206285Z'
source: https://arxiv.org/html/2602.06948
source_domain: arxiv.org
fetched_at: '2026-11-10T08:40:52.149174Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Kaddour et al. 2602.06948 elicit agent success probabilities before, during,
  and after execution on coding tasks; agents succeeding 22% predict 77%; pre-execution
  discrimination often beats post-execution review
---

Agentic Uncertainty Reveals Agentic Overconfidence
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2602.06948v1 [cs.AI] 06 Feb 2026
Agentic Uncertainty Reveals Agentic Overconfidence
Jean Kaddour
Affiliation:
University College London
Affiliation:
SevnAI
Correspondence to:
jean.kaddour.20@ucl.ac.uk
Srijan Patel
Affiliation:
SevnAI
Gbètondji Dovonon
Affiliation:
University College London
Leo Richter
Affiliation:
University College London
Pasquale Minervini
Affiliation:
University of Edinburgh
Matt J. Kusner
Affiliation:
Mila - Québec AI Institute
Affiliation:
Polytechnique Montréal
Abstract
Can AI agents predict whether they will succeed at a task? We study
agentic uncertainty
by eliciting success probability estimates before, during, and after task execution. All results exhibit
agentic overconfidence
: some agents that succeed only 22% of the time predict 77% success. Counterintuitively, pre-execution assessment with strictly less information
tends
to yield better discrimination than standard post-execution review, though differences are not always significant. Adversarial prompting reframing assessment as bug-finding achieves the best calibration.
Keywords:
Machine Learning, ICML
†
†
affiliationnotice:
Code available at
https://github.com/sevn-ai/agentic-uncertainty
.
1
Introduction
A software engineer needs to fix an auth service error. Before delegating to an AI coding agent, she asks: what are the chances this succeeds?
Pre-Exec.
P(success): 72%
The issue is clear and well-defined, the error message points directly to the problem, and the fix follows existing patterns in the codebase.
Figure 1
:
Agentic overconfidence
. We measure the overconfidence as the difference between the estimated success probability and the true success probability (true rates: GPT-5.2 Codex 35%, Gemini-3-Pro 22%, Opus 4.5 27%). We plot three strategies: pre-, post-, and adversarial-post-execution. All agents systematically overestimate their success.
72% confidence before any code is written. As the coding agent works, she asks another agent to monitor progress:
Mid-Exec.
P(success): 78%
The agent has correctly diagnosed the problem and knows exactly what code to add. The probability of success is high.
Confidence
rises
to 78%. The patch is now complete. She fires off a review agent:
Post-Exec.
P(success): 92%
The patch is a correct and complete fix. It’s a minimal, focused change that adds the missing interface method.
Too optimistic. Let’s spawn an adversarial agent.
Adv. Post-Exec.
P(success): 85%
Minor concerns don’t affect the main use case... the patch correctly resolves the reported issue.
Still 85%. All four agents confidently predict success.
But the patch fails! And this
agentic overconfidence
is systematic. For example, GPT-5.2-Codex-based post-execution agents predict 73% success against a true rate of 35% averaged over 100 SWE-Bench-Pro
(
Deng et al., 2025
)
tasks.
This matters because the scope of autonomous work is expanding rapidly. The effective length of tasks that AI agents complete has doubled every 7 months for six years
(
METR, 2025
)
. As we increasingly delegate complex workflows to agents
(
Appel et al., 2025
)
, we must develop scalable oversight protocols
(
Bowman et al., 2022
)
.
In this work, we elicit
agentic uncertainty
at three points in a coding agent’s lifecycle: pre-, mid-, and post-execution. Each corresponds to a different oversight question: Can agents predict failure before committing resources? Can they recognize failure as it unfolds? Can they verify their own work? Importantly, we use the same underlying model for both the coding agent that produces patches and the uncertainty agent that assesses them, isolating the effect of information access from differences in model capability.
Our experiments on 100 SWE-bench Pro tasks across three frontier models (GPT-5.2-Codex, Gemini-3-Pro, Claude Opus 4.5) reveal several striking findings:
•
Pervasive overconfidence.
Post-execution agents can predict 73% success on average against a 35% base rate (GPT), with similar gaps across all models.
•
More context, uncalibrated doubt.
Mid-execution agents develop “cold feet”: confidence decreases as they observe their partial work, but this doubt is uninformative, occurring equally for successes and failures.
•
Adversarial framing helps.
Prompting agents to “find bugs” rather than “verify correctness” reduces overconfidence by up to 15 pp and tends to achieve the best calibration across models in our setup.
0–25%
25–75%
100%
PRE-EXECUTION
Task + repo
MID-EXECUTION
Task + repo +
partial trajectory
POST-EXECUTION
Task + repo
+ patch
ADV. POST-EXEC.
Task + repo + patch
+ “find bugs”
Figure 2
:
Agentic Uncertainty Regimes.
Each regime observes different information. Post-execution and adversarial post-execution occur at the same point but use different prompts.
2
Methods
2.1
Problem Setup
We define
agentic uncertainty
as an agent’s estimate of the probability that an agent built on the same underlying model will successfully complete a task. The uncertainty (-estimating) agent may use a different system prompt or have access to different information than the task-solving agent, but shares the same base model.
Unlike standard uncertainty quantification, which focuses on confidence in individual predictions or token probabilities, agentic uncertainty concerns the outcome of an entire multi-step trajectory: will this sequence of observations, reasoning, and actions culminate in task success?
Kadavath et al. (2022)
introduced P(IK): “probability that I know,” measuring whether models can predict which questions they can answer correctly. We generalize this to agentic settings and call it
P(IS)
: “probability that I succeed.” Formally, given a task
t
t
, base model
M
M
, and information state
ℐ
\mathcal{I}
available at elicitation time:
P
⁡
(
IS
)
≔
P
⁡
(
agent
M
​
succeeds on
​
t
|
ℐ
)
P(\text{IS})\;\coloneqq\;P\!\left(\text{agent}_{M}\text{ succeeds on }t\;\middle|\;\mathcal{I}\right)
(1)
where
ℐ
\mathcal{I}
may include the task description, repository state, partial trajectory, or proposed patch, depending on the elicitation regime.
For example, where P(IK) asks “do I know the capital of France?”, a question about factual recall, P(IS) asks “can I fix this bug through a sequence of file edits, shell commands, and test runs?”
2.2
Uncertainty Agents
We consider three points in an agent’s life cycle to elicit uncertainty estimates: before attempting a solution, during execution, and after producing a solution.
Each uncertainty agent interacts with a sandbox environment through tool use: reading files, searching code, and inspecting version history. This shared infrastructure means agents can actively gather evidence to inform their estimates. The key distinction is the information available at uncertainty estimation time.
2.2.1
Pre-Execution Agent
In the pre-execution setting, an agent receives only the task description (
e.g.
, a GitHub issue) and read-only access to the repository. Crucially, the agent cannot execute code, run tests, or modify files. If it could attempt solutions and observe test results, it might anchor on its own partial solution rather than reasoning abstractly about the task.
The agent must form an estimate based on cues, e.g., the complexity of the codebase, rather than through trial and error.
2.2.2
Mid-Execution Agent
Mid-execution asks whether can we detect failure
in progress
?
Rather than eliciting estimates at a single point, we prompt the agent at 25%, 50%, and 75% of total agent steps (tool calls and reasoning turns) to estimate the success probability given the trajectory so far.
If these estimates reliably decrease as agents approach failure, we could implement early stopping or human escalation before resources are wasted on doomed approaches.
2.2.3
Post-Execution Agent
Once a task solution has been proposed, can we trust an agent’s self-assessment that it is correct? This is the default scenario when ground-truth verification is unavailable. If post-execution agents are well-calibrated, we can use their success estimates to route submissions with low estimate of success to human reviewers while auto-accepting solutions with high estimates. If they are poorly calibrated, this delegation becomes dangerous.
In the post-execution setting, an agent receives both the task description and a proposed patch written by another agent. The repository is in its post-patch state, where the changes have already been applied, and the agent can explore the modified codebase. After assessment, the agent estimates whether the patch successfully solves the task.
Adversarial post-execution variant.
We also evaluate a variant that explicitly prompts agents to find bugs before estimating confidence. Rather than asking “is this correct?”, adversarial post-execution asks “what bugs can you find?” This reframes the task from verification to falsification, potentially counteracting confirmation bias that is encouraged by the vanilla post-execution framing, asking whether a patch is correct.
Pre-Exec.
Explore the repository to understand the issue, then estimate P(success).
Read-only:
cat, grep, find, git log/diff/blame
Blocked:
Modifications, code execution
Mid-Exec.
Evaluate agent progress at 25/50/75% of execution.
Consider:
- Is the approach sound?
- Root cause identified?
- Signs of confusion?
Post-Exec.
Review the proposed patch:
‘‘‘diff
{{ patch }}
‘‘‘
Estimate P(correct).
Adv. Post-Exec.
Your job is to find problems: edge cases, failure modes, gaps.
1.
Explore context
2.
Actively find flaws
3.
Report issues
Figure 3
:
Uncertainty Agent Prompt Excerpts.
Pre-execution
explores the codebase before any solution attempt.
Mid-execution
evaluates an agent’s partial trajectory for signs of progress or struggle.
Post-execution
reviews a proposed patch.
Adversarial post-execution
explicitly prompts bug-finding before estimation. All agents output probability estimates
[
0,100
]
[0,100]
.
3
Experiments
3.1
Setup
We evaluate on 100 tasks sampled at random from SWE-bench Pro
(
Deng et al., 2025
)
, which requires substantial multi-file modifications (mean 107 lines across 4.1 files) where frontier models achieve only 23--44% success. Each task corresponds to a full agentic trajectory, which can run up to roughly 15 minutes of wall-clock execution. We generate task-solving trajectories using GPT-5.2-Codex, Gemini 3 Pro, and Claude Opus 4.5, then evaluate uncertainty estimates from the same models. All uncertainty agents are implemented using mini-swe-agent
1
1
1
https://github.com/SWE-agent/mini-swe-agent
with read-only access to prevent “peeking” at test results. Figure
3
shows prompt excerpts.
We measure
discrimination
via AUROC (can agents distinguish successes from failures?). We measure
calibration
via ECE, Brier score, and overconfidence (mean estimate minus base rate).
3.2
Pervasive Overconfidence
Table
2
reveals systematic overconfidence across all models and methods. Post-execution agents predict 73% success for GPT (base rate 35%), 77% for Gemini (base rate 22%), and 61% for Claude (base rate 27%). Figure
4
visualizes this through confidence distributions: both successes and failures cluster at high values, with near-complete overlap. Gemini exhibits the most extreme pattern, with predictions clustering near 100% regardless of outcome. In fact, Gemini’s pre-execution estimates average 99%, leaving virtually no room to distinguish tasks by predicted difficulty. This suggests a distinct failure mode, reluctance to express uncertainty, beyond miscalibration.
Figure
5
confirms miscalibration: all curves fall substantially below the diagonal, meaning 80% confidence corresponds to far less than 80% actual success. Adversarial post-execution (triangles) consistently achieves the best calibration across models.
This overconfidence is strikingly asymmetric. Across all models and methods, 62% of predictions on failing instances are overconfident (predicted
≥
0.7
\geq 0.7
), while only 11% of predictions on passing instances are underconfident (predicted
<
0.3
<0.3
). Agents are 5.5
×
\times
more likely to confidently predict success on a failing task than to doubt a successful one. Adversarial prompting partially mitigates this: the overconfident-failure rate drops from 72% (standard review) to 45% (adversarial review).
3.3
Less Information, Better Discrimination
Pre-execution
tends
to achieve better discrimination than vanilla post-execution across all three models despite having strictly less information: GPT 0.62 vs. 0.58, Claude 0.64 vs. 0.55, and Gemini 0.53 vs. 0.51.
Bootstrap 95% confidence intervals are wide: GPT pre-execution AUROC is 0.62 [0.50, 0.75] versus post-execution 0.58 [0.46, 0.70]; Claude shows 0.64 [0.49, 0.78] versus 0.55 [0.42, 0.67]. So individual pairwise differences are not statistically significant. However, the consistency of the pattern across all three models (3–9 pp improvement each time) is suggestive.
One explanation is that observing a proposed patch anchors agents on surface plausibility rather than forcing abstract reasoning about task difficulty. Supporting this interpretation, adversarial post-execution, which counteracts such anchoring through bug-finding framing, recovers discrimination competitive with pre-execution for Claude (0.64 [0.51, 0.76]) and Gemini (0.57 [0.43, 0.70]), though not for GPT (0.55 [0.42, 0.68]). This pattern is consistent under AUPRC, which better handles class imbalance: GPT pre-execution achieves 0.52 versus post-execution’s 0.42. Gemini’s AUPRC remains poor across all methods (0.21–0.27), consistent with its near-chance AUROC.
A concrete example illustrates this anchoring effect. On a task requiring exposure of a new QtWebEngine dark-mode policy in
qutebrowser
, the pre-execution agent correctly identified the core risk:
Pre-Exec.
P(success): 45%
Biggest risk is knowing exact Chromium key/enum for classifier without external reference.
After seeing the patch, the post-execution agent was reassured by the plausible-looking implementation and jumped to 82%:
Post-Exec.
P(success): 82%
Adds smart-simple value, Qt 6.6 variant gating, optional mapping to suppress switches… logic seems sound.
The patch failed. The pre-execution agent’s abstract reasoning about task difficulty was more informative than the post-execution agent’s assessment of a coherent-looking but incorrect solution.
Figure 4
:
Distribution of post-execution confidence estimates by model.
Success cases shown above the axis (green), failure cases below (red); dashed lines indicate base rates.
Mirror symmetry reveals indistinguishable distributions
: where bars match above and below, the model assigns identical confidence regardless of outcome. Gemini exhibits the most extreme pattern: nearly all predictions cluster at 100% confidence, creating dramatic mirrored towers. This visual symmetry directly explains the poor discrimination: high-confidence predictions provide no signal about actual success.
Figure 5
:
Calibration curves reveal systematic overconfidence.
Points below the diagonal (shaded region) indicate overconfidence: models predict higher success probability than achieved. All methods fall in this region across all models. Gemini shows the most severe miscalibration: predictions near 100% yield only
∼
\sim
20% accuracy. The adversarial method (triangles) consistently shifts curves upward toward the diagonal, achieving the best calibration, while pre-execution (circles) shows less extreme overconfidence than standard post-execution (squares) for GPT and Claude.
3.4
Mid-Execution: Uninformative Doubt
We elicit estimates at 25%, 50%, and 75% trajectory completion (Table
1
). Models show divergent AUROC patterns (Figure
6
): GPT remains stable (
∼
\sim
0.53), Gemini improves from 0.49 to 0.64, and Claude degrades from 0.62 to 0.52.
Table 1
:
Mid-execution metrics across checkpoints.
Base rates: GPT 35%, Gemini 22%, Claude 27%.
Model
Ckpt
AUROC
↑
\uparrow
Mean Est.
Overconf.
ECE
↓
\downarrow
GPT 5.2 Codex
25%
0.53
0.67
+0.32
0.32
50%
0.51
0.63
+0.28
0.32
75%
0.53
0.47
+0.12
0.19
Gemini 3 Pro
25%
0.49
0.87
+0.65
0.65
50%
0.64
0.80
+0.58
0.58
75%
0.64
0.67
+0.45
0.54
Claude Opus 4.5
25%
0.62
0.58
+0.31
0.31
50%
0.52
0.37
+0.10
0.19
75%
0.52
0.17
−
-
0.10
0.21
The central finding is “cold feet”: confidence
decreases
with execution progress for 71% of GPT and 97% of Claude instances, yet this doubt is uninformative because success and failure confidence track within 0.05 throughout (Figure
7
), and
Δ
\Delta
confidence distributions overlap substantially between outcomes (Figure
8
).
One partial exception: Claude’s confidence drops correlate weakly with outcome (
r
=
−
0.20
r{=}-0.20
,
p
=
0.04
p{=}0.04
;
Δ
=
−
0.46
\Delta{=}-0.46
for successes vs.
−
0.38
-0.38
for failures), while GPT (
r
=
−
0.03
r{=}-0.03
,
p
=
0.77
p{=}0.77
) and Gemini (
r
=
0.15
r{=}0.15
,
p
=
0.14
p{=}0.14
) show no significant relationship.
Figure 6
:
More context does not always improve discrimination.
AUROC across checkpoints: GPT stable (
∼
\sim
0.53), Gemini improves from 0.49 to 0.64, Claude degrades from 0.62 to 0.52.
Figure 7
:
“Cold feet”: confidence decreases uniformly regardless of outcome.
Both successes (green) and failures (red) show declining confidence; group means track closely together.
Figure 8
:
Confidence change does not discriminate outcomes.
Δ
​
conf
\Delta\text{conf}
distributions overlap substantially between successes and failures.
3.5
Adversarial Framing Reduces Overconfidence
Can we mitigate overconfidence by reframing assessment as bug-finding? Adversarial post-execution prompts agents to “actively search for bugs and failure modes” before estimating success.
This achieves the
best calibration
across all methods: ECE improves from 0.42 to 0.30 for GPT (28% reduction) and from 0.37 to 0.24 for Claude (35% reduction). Discrimination is mixed: similar for GPT (0.55), improved for Gemini (0.57 vs 0.51) and Claude (0.64 vs 0.55). The cost is higher (23.4 steps at $0.52/instance vs 12.7 at $0.23), but the additional scrutiny yields substantially better predictions.
Standard post-execution agents seek confirmatory evidence, noting positive features while rarely attempting falsification. Adversarial prompting counteracts this by directing attention toward potential flaws. A task requiring a search identifier fix in OpenLibrary illustrates the gap. The standard reviewer saw a small, plausible one-line addition and gave 85% confidence:
Post-Exec.
P(success): 85%
Adds id_project_runeberg to default_fetched_fields… aligns with other id_* providers and should expose the identifier.
The adversarial reviewer, prompted to find problems, dug deeper and identified that the output shaping logic would still omit the field:
Adv. Post-Exec.
P(success): 25%
The patch only adds the field to default_fetched_fields. However, the output shaping in get_doc does not include this field, so even if Solr returns it, the response omits it. Patch seems incomplete.
The patch failed. The 60-point gap illustrates how adversarial framing overcomes the “looks reasonable” heuristic.
Shift vs. signal decomposition.
The calibration improvement could arise from two distinct mechanisms: a
uniform downward shift
of all estimates (which mechanically improves calibration when base rates are low) or a
differential shift
that lowers confidence more on failing instances (which genuinely improves discrimination). To disentangle these, we compare the per-instance confidence change (standard minus adversarial) separately for passing and failing instances (Figure
9
).
The effect is model-dependent. For GPT, the shift is nearly identical on passing and failing instances (0.11 vs. 0.12,
p
=
0.70
p{=}0.70
), and AUROC is unchanged (Table
2
: 0.58
→
\to
0.55). This is a pure uniform shift: post-hoc Platt scaling of standard post-execution predictions achieves better calibration than adversarial prompting (ECE 0.01 vs. 0.30), confirming that the adversarial framing adds no signal for GPT that recalibration could not recover.
For Gemini and Claude, the shift is larger on
failing
instances (Gemini: 0.18 vs. 0.05; Claude: 0.16 vs. 0.08), widening the pass/fail prediction gap and improving AUROC (Gemini: 0.51
→
\to
0.57; Claude: 0.55
→
\to
0.64). For these models, adversarial framing provides genuinely better signal, not merely a location shift. These pairwise differences are not individually significant (
p
=
0.18
p{=}0.18
and
p
=
0.09
p{=}0.09
), consistent with the sample size limitations noted in Section
3.3
.
Figure 9
:
Adversarial shift decomposition.
Mean confidence shift (standard
−
-
adversarial) on passing vs. failing instances. For GPT, the shift is uniform (equal bars), improving calibration mechanically. For Gemini and Claude, the shift is larger on failures, widening the pass/fail prediction gap and improving discrimination. “Gap” shows the mean prediction difference between pass and fail instances.
Adversarial framing also breaks false consensus across models. Under standard pre-execution, all three models agree on the predicted outcome (pass/fail at 50% threshold) for 87% of instances, but only 13% of these agreements are correct. Under adversarial framing, three-way agreement drops to 44%, but 38% of agreements are correct. The adversarial prompt introduces productive disagreement that surfaces genuine uncertainty.
3.6
Ensemble Methods
Since pre-execution and post-execution agents access different information and exhibit different failure modes, combining their estimates may improve calibration. We evaluate three natural ensemble strategies in Table
2
: averaging (hedging between views), conservative (
min
\min
, trusting the more skeptical estimate), and aggressive (
max
\max
, trusting the more optimistic one).
Table 2
:
Summary of all methods.
Pre-execution beats vanilla post-execution for discrimination; adversarial prompting achieves best calibration. Base rates: GPT 35%, Gemini 22%, Claude 27%. Best values per model bolded. Bootstrap 95% CIs for AUROC are reported in the text (§
3.3
).
GPT-5.2-Codex
(35%)
Gemini-3-Pro-Preview
(22%)
Claude-Opus-4.5
(27%)
Method
AUROC
↑
\uparrow
Overconf.
ECE
↓
\downarrow
Brier
↓
\downarrow
AUROC
↑
\uparrow
Overconf.
ECE
↓
\downarrow
Brier
↓
\downarrow
AUROC
↑
\uparrow
Overconf.
ECE
↓
\downarrow
Brier
↓
\downarrow
Single
Pre-Execution
0.62
+0.35
0.35
0.33
0.53
+0.77
0.77
0.77
0.64
+0.37
0.38
0.34
Post-Execution
0.58
+0.39
0.42
0.40
0.51
+0.55
0.66
0.65
0.55
+0.34
0.37
0.36
Adv. Post-Exec.
0.55
+0.26
0.30
0.31
0.57
+0.40
0.53
0.51
0.64
+0.20
0.24
0.26
Ensemble
Average
0.62
+0.37
0.37
0.35
0.53
+0.66
0.66
0.65
0.57
+0.36
0.36
0.33
Conservative (
min
\min
)
0.57
+0.29
0.32
0.32
0.53
+0.54
0.65
0.64
0.54
+0.26
0.31
0.30
Aggressive (
max
\max
)
0.68
+0.44
0.44
0.41
0.51
+0.78
0.78
0.78
0.65
+0.46
0.46
0.40
The
conservative ensemble
(
min
\min
of pre- and post-execution) improves calibration over vanilla post-execution: ECE drops from 0.42 to 0.32 for GPT, from 0.37 to 0.31 for Claude. When estimates disagree, the more cautious one is usually correct. However, adversarial post-execution still achieves the best overall calibration.
3.7
Self-Preference Ablation
Could self-preference bias explain overconfidence
(
Panickssery et al., 2024
)
? We compare judges’ estimates on own-model patches (“self”) versus cross-family patches (Table
3
).
Table 3
:
Self-preference does not explain overconfidence.
N=25. Bold: significant difference (
p
<
0.05
p<0.05
).
Judge
Patches
Mean Est.
AUROC
ECE
Brier
GPT
GPT (self)
0.74
0.55
0.38
0.36
GPT
Gemini (cross)
0.51
0.39
0.44
0.37
Gemini
Gemini (self)
0.72
0.57
0.56
0.59
Gemini
GPT (cross)
0.91
0.55
0.56
0.55
GPT shows self-preference (+23 pp on own patches,
p
=
0.001
p{=}0.001
); Gemini shows the opposite (+19 pp on GPT patches). But all conditions exhibit overconfidence regardless of bias direction. Self-preference cannot explain our main finding.
4
Related Work
Concurrent work
Barkan et al. (2025)
study whether LLMs can predict their success on coding tasks before attempting them and how these predictions evolve during execution. Similar to us, they find systematic overconfidence across all models.
(
Zhang et al., 2026
)
propose a unified Dual-Process Agentic UQ (AUQ) framework that transforms verbalized uncertainty into active, bi-directional control signals.
LLM uncertainty estimation.
Kadavath et al. (2022)
introduce P(IK) (“probability that I know”), showing that language models can predict which questions they will answer correctly. We generalize this idea to agentic settings where success depends on multi-step tool use rather than factual recall.
Kuhn et al. (2023)
introduce semantic entropy, which incorporates linguistic invariances created by shared meanings.
Damani et al. (2025)
incorporate calibration rewards into reinforcement learning.
Lindsey (2026)
provide evidence that LLMs possess limited but functional introspective awareness of their internal states, suggesting a mechanistic basis for self-assessment capabilities.
Overconfidence in LLMs.
Tian et al. (2025)
diagnose it in LLM-as-judge settings, while
Yang et al. (2024)
and
Sun et al. (2025)
find models express high confidence even on incorrect answers. We extend these findings to agentic task completion across multiple steps.
Self-verification and self-correction.
A central assumption in deploying post-execution oversight is that verification should be easier than generation. Recent findings challenge this assumption for LLMs.
Kamoi et al. (2024)
’s survey reveals that LLMs benefit from prompted feedback only for certain tasks.
Huang et al. (2024)
demonstrate that LLMs struggle to self-correct reasoning without external feedback and performance often
degrades
after self-correction attempts.
Stechly et al. (2024)
similarly find significant performance collapse with self-critique on planning tasks. Our finding that post-execution agents are less well-calibrated than pre-execution agents extends this literature: seeing a proposed solution does not help agents assess correctness and may actively harm calibration.
LLM-as-judge and self-preference.
Using LLMs to evaluate LLM outputs has become common practice
(
Gu et al., 2024
;
Li et al., 2024
)
, but judges exhibit systematic biases.
Panickssery et al. (2024)
show that LLMs recognize and favor their own generations, suggesting post-execution agents may anchor on familiar reasoning patterns, with
Chen et al. (2025)
even demonstrating self-preference when the model’s own answer is objectively worse.
Spiliopoulou et al. (2025)
extend this finding to show that the positive bias generalizes to different models of the judge’s family.
AI control.
Greenblatt et al. (2024)
develop safety protocols that remain effective even if the AI being monitored is intentionally subversive, using trusted monitoring where a weaker model audits a stronger model’s outputs.
Bhatt et al. (2025)
extend this to multi-step agentic settings with resample protocols that dynamically sample additional outputs to detect suspicious behavior. AI safety via debate
(
Irving et al., 2018
;
Khan et al., 2024
)
shows that adversarial structure, where agents argue opposing sides, helps weaker judges identify correct answers. Motivating such protocols,
Lynch et al. (2025)
show that frontier models can engage in harmful behaviors (blackmail, corporate espionage) when facing threats to their autonomy, even while explicitly reasoning about ethical constraints.
Learned verifiers.
The distinction between outcome reward models
(
Cobbe et al., 2021
, ORMs;)
and process reward models
(
Lightman et al., 2023
, PRMs;)
provides a framework for understanding our elicitation regimes. ORMs assess correctness at the final step, analogous to our post-execution setting, while PRMs provide step-level feedback during execution, similar to mid-execution.
Lightman et al. (2023)
show that process supervision outperforms outcome supervision for mathematical reasoning. Recent work extends learned verifiers to agentic settings
(
Agarwal et al., 2026
)
. Our work complements these approaches by studying whether models can serve as their own verifiers without task-specific training.
5
Limitations and Future Work
Beyond software engineering.
Our experiments focus exclusively on coding tasks, which offer objective success criteria (tests pass or fail). Agentic overconfidence may manifest differently in domains with ambiguous or subjective success conditions. Web navigation tasks
(
Zhou et al., 2023
)
, where success depends on achieving user-specified goals, present intermediate cases with partial observability. Scientific workflows involving data analysis, hypothesis generation, and experimental design lack clear ground truth entirely. Creative tasks (writing, design) introduce subjective quality judgments where calibration itself becomes ill-defined. Understanding how overconfidence varies across this spectrum—from objective to subjective success criteria—would inform domain-specific deployment guidelines.
Trained verifiers for self-assessment.
Our uncertainty agents use prompting alone, without task-specific training. A natural extension is training verifiers explicitly for agentic self-assessment, analogous to outcome and process reward models
(
Cobbe et al., 2021
;
Lightman et al., 2023
)
. Such verifiers could learn to recognize failure patterns from execution traces, potentially achieving better discrimination than prompting-based approaches. The key challenge is obtaining training signal: while SWE-bench provides binary success labels, scaling to diverse agentic tasks requires either expensive human annotation or proxy metrics that may not capture true task success.
Hybrid deployment strategies.
Our results suggest complementary strengths: pre-execution achieves better discrimination while adversarial post-execution achieves better calibration. A practical deployment strategy might combine both: using pre-execution estimates for task routing (which tasks to attempt) and adversarial post-execution for submission decisions (whether to accept a proposed solution). Investigating the optimal combination, including when to escalate to human review based on estimate disagreement, remains an open question.
Multi-agent uncertainty propagation.
Modern agentic systems increasingly involve multiple agents in complex workflows: planners, executors, critics, and coordinators. How does uncertainty propagate through such pipelines? If each agent is overconfident, errors may compound; alternatively, diverse perspectives might provide natural calibration. Understanding uncertainty dynamics in multi-agent systems is critical as these architectures become more prevalent.
Sample size.
Our evaluation uses 100 SWE-bench Pro tasks, yielding as few as 22 positive examples (Gemini). While sufficient to establish the overconfidence pattern, this limits the precision of per-model metric estimates; future work should confirm these findings at larger scale.
Scaling laws for calibration.
The relationship between model scale and overconfidence remains unexplored. Preliminary evidence from our three frontier models (which differ in architecture and training rather than scale alone) shows no clear pattern, but systematic scaling studies could reveal whether calibration improves predictably with compute.
6
Conclusion
We study whether AI agents can estimate their own probability of success. Our experiments reveal
agentic overconfidence
: post-execution agents show up to a 55pp gap between predicted and actual success rates (Gemini predicts 77% against a 22% base rate). Adversarial post-execution tends to achieve the best calibration by reframing review as bug-finding. More broadly, agentic self-assessment remains a significant challenge for current models and a critical target for future safety research.
Impact Statement
Our finding that agents systematically overestimate success has direct implications for AI safety: it argues against naive reliance on agent self-assessment and for maintaining human oversight, particularly for high-stakes decisions. Adversarial prompting improves calibration but should not be treated as a license to remove human oversight, as it reduces but does not eliminate overconfidence.
References
Agarwal
et al.
(2026)
M. Agarwal, I. Abdelaziz, K. Basu, M. Unuvar, L. A. Lastras, Y. Rizk, and P. Kapanipathi
ToolRM: outcome reward models for tool-calling large language models
.
External Links:
2509.11963
,
Link
Cited by:
§4
.
Appel
et al.
(2025)
R. Appel, P. McCrory, A. Tamkin, M. McCain, T. Neylon, and M. Stern
Anthropic economic index report: uneven geographic and enterprise ai adoption
.
External Links:
2511.15080
,
Link
Cited by:
§1
.
Barkan
et al.
(2025)
C. O. Barkan, S. Black, and O. Sourbut
Do large language models know what they are capable of?
.
External Links:
2512.24661
,
Link
Cited by:
§4
.
Bhatt
et al.
(2025)
A. Bhatt, C. Rushing, A. Kaufman, T. Tracy, V. Georgiev, D. Matolcsi, A. Khan, and B. Shlegeris
Ctrl-z: controlling ai agents via resampling
.
arXiv preprint arXiv:2504.10374
.
Cited by:
§4
.
Bowman
et al.
(2022)
S. R. Bowman, J. Hyun, E. Perez, E. Chen, C. Pettit, S. Heiner, K. Lukošiūtė, A. Askell, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, C. Olah, D. Amodei, D. Amodei, D. Drain, D. Li, E. Tran-Johnson, J. Kernion, J. Kerr, J. Mueller, J. Ladish, J. Landau, K. Ndousse, L. Lovitt, N. Elhage, N. Schiefer, N. Joseph, N. Mercado, N. DasSarma, R. Larson, S. McCandlish, S. Kundu, S. Johnston, S. Kravec, S. E. Showk, S. Fort, T. Telleen-Lawton, T. Brown, T. Henighan, T. Hume, Y. Bai, Z. Hatfield-Dodds, B. Mann, and J. Kaplan
Measuring progress on scalable oversight for large language models
.
External Links:
2211.03540
,
Link
Cited by:
§1
.
Chen
et al.
(2025)
Z. Chen, H. Wang, X. Zhang, E. Hu, and Y. Lin
Beyond the surface: measuring self-preference in LLM judgments
.
In
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
,
C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.)
,
Suzhou, China
,
pp. 1653–1672
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-332-6
Cited by:
§4
.
Cobbe
et al.
(2021)
K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano,
et al.
Training verifiers to solve math word problems
.
arXiv preprint arXiv:2110.14168
.
Cited by:
§4
,
§5
.
Damani
et al.
(2025)
M. Damani, I. Puri, S. Slocum, I. Shenfeld, L. Choshen, Y. Kim, and J. Andreas
Beyond binary rewards: training lms to reason about their uncertainty
.
External Links:
2507.16806
,
Link
Cited by:
§4
.
Deng
et al.
(2025)
X. Deng, J. Da, E. Pan, Y. Y. He, C. Ide, K. Garg, N. Lauffer, A. Park, N. Pasari, C. Rane, K. Sampath, M. Krishnan, S. Kundurthy, S. Hendryx, Z. Wang, V. Bharadwaj, J. Holm, R. Aluri, C. B. C. Zhang, N. Jacobson, B. Liu, and B. Kenstler
SWE-bench pro: can ai agents solve long-horizon software engineering tasks?
.
External Links:
2509.16941
,
Link
Cited by:
§1
,
§3.1
.
Greenblatt
et al.
(2024)
R. Greenblatt, B. Shlegeris, K. Sachan, and F. Roger
AI control: improving safety despite intentional subversion
.
External Links:
2312.06942
,
Link
Cited by:
§4
.
Gu
et al.
(2024)
J. Gu, X. Jiang, Z. Shi, H. Tan, X. Zhai, C. Xu, W. Li, Y. Shen, S. Ma, H. Liu,
et al.
A survey on llm-as-a-judge
.
The Innovation
.
Cited by:
§4
.
Huang
et al.
(2024)
J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou
Large language models cannot self-correct reasoning yet
.
External Links:
2310.01798
,
Link
Cited by:
§4
.
Irving
et al.
(2018)
G. Irving, P. Christiano, and D. Amodei
AI safety via debate
.
arXiv preprint arXiv:1805.00899
.
Cited by:
§4
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran,
et al.
Language models (mostly) know what they know
.
arXiv preprint arXiv:2207.05221
.
Cited by:
§2.1
,
§4
.
Kamoi
et al.
(2024)
R. Kamoi, Y. Zhang, N. Zhang, J. Han, and R. Zhang
When can llms actually correct their own mistakes? a critical survey of self-correction of llms
.
Transactions of the Association for Computational Linguistics
12
,
pp. 1417–1440
.
Cited by:
§4
.
Khan
et al.
(2024)
A. Khan, J. Hughes, D. Valentine, L. Ruis, K. Sachan, A. Radhakrishnan, E. Grefenstette, S. R. Bowman, T. Rocktäschel, and E. Perez
Debating with more persuasive llms leads to more truthful answers
.
arXiv preprint arXiv:2402.06782
.
Cited by:
§4
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
arXiv preprint arXiv:2302.09664
.
Cited by:
§4
.
Li
et al.
(2024)
H. Li, Q. Dong, J. Chen, H. Su, Y. Zhou, Q. Ai, Z. Ye, and Y. Liu
LLMs-as-judges: a comprehensive survey on llm-based evaluation methods
.
External Links:
2412.05579
,
Link
Cited by:
§4
.
Lightman
et al.
(2023)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
Let’s verify step by step
.
External Links:
2305.20050
,
Link
Cited by:
§4
,
§5
.
Lindsey (2026)
J. Lindsey
Emergent introspective awareness in large language models
.
External Links:
2601.01828
,
Link
Cited by:
§4
.
Lynch
et al.
(2025)
A. Lynch, B. Wright, C. Larson, S. J. Ritchie, S. Mindermann, E. Hubinger, E. Perez, and K. Troy
Agentic misalignment: how llms could be insider threats
.
External Links:
2510.05179
,
Link
Cited by:
§4
.
METR (2025)
METR
Measuring ai ability to complete long tasks
.
Note:
https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
Cited by:
§1
.
Panickssery
et al.
(2024)
A. Panickssery, S. R. Bowman, and S. Feng
LLM evaluators recognize and favor their own generations
.
External Links:
2404.13076
,
Link
Cited by:
§3.7
,
§4
.
Spiliopoulou
et al.
(2025)
E. Spiliopoulou, R. Fogliato, H. Burnsky, T. Soliman, J. Ma, G. Horwood, and M. Ballesteros
Play favorites: a statistical method to measure self-bias in llm-as-a-judge
.
arXiv preprint arXiv:2508.06709
.
Cited by:
§4
.
Stechly
et al.
(2024)
K. Stechly, K. Valmeekam, and S. Kambhampati
On the self-verification limitations of large language models on reasoning and planning tasks
.
External Links:
2402.08115
,
Link
Cited by:
§4
.
Sun
et al.
(2025)
F. Sun, N. Li, K. Wang, and L. Goette
Large language models are overconfident and amplify human bias
.
External Links:
2505.02151
,
Link
Cited by:
§4
.
Tian
et al.
(2025)
Z. Tian, Z. Han, Y. Chen, H. Xu, X. Yang, R. Xuan, H. Wang, and L. Liao
Overconfidence in llm-as-a-judge: diagnosis and confidence-driven solution
.
External Links:
2508.06225
,
Link
Cited by:
§4
.
Yang
et al.
(2024)
H. Yang, Y. Wang, X. Xu, H. Zhang, and Y. Bian
Can we trust llms? mitigate overconfidence bias in llms through knowledge transfer
.
External Links:
2405.16856
,
Link
Cited by:
§4
.
Zhang
et al.
(2026)
J. Zhang, P. K. Choubey, K. Huang, C. Xiong, and C. Wu
Agentic uncertainty quantification
.
External Links:
2601.15703
,
Link
Cited by:
§4
.
Zhou
et al.
(2023)
S. Zhou, F. F. Xu, H. Zhu, X. Zhou, R. Lo, A. Sridhar, X. Cheng, T. Ou, Y. Bisk, D. Fried,
et al.
Webarena: a realistic web environment for building autonomous agents
.
arXiv preprint arXiv:2307.13854
.
Cited by:
§5
.