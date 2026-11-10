---
title: 'Poison Valleys: Diagnosing Path-Dependent Failure in LLM Code Repair'
id: poison-valleys-diagnosing-path-dependent-failure-in-llm-code-repair
tags:
- code-llm-confidence-positioning-d82d00
- code-repair
- obligation-level-diagnosis
- failure-localization
created: '2026-11-09T23:08:03.305486Z'
updated: '2026-11-09T23:27:44.411235Z'
source: https://arxiv.org/html/2610.21514
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:03.304454Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'RELATED for L4: obligation-level diagnostic coordinates for code repair
  failures; synthetic tasks, no confidence. Full text. Poison Valleys, arXiv 2610.21514,
  full text. 1,844 model requests on two synthetic Python repair tasks (PersistQueue
  atomic batch claiming; Dijkstra source-sensitive filtering). Injects plausible but
  incorrect software mechanisms in hypothesis, plan, or both; Oracle PASS/FAIL plus
  targeted diagnostic coordinates (violated obligations). Moving the misconception
  from hypothesis to plan increased failure by 32.2% (PersistQueue) and 28.9% (Dijkstra).
  Models include GPT-5.6 Luna, GPT-5.4 Nano, Claude Haiku 4.5, Claude Sonnet 5, Qwen
  3.8 Flash (model names as written in the paper). Per-obligation diagnosis is the
  closest to per-requirement or per-test-group localization, but there is no confidence
  estimation, no real repository benchmark, and synthetic tasks only.'
---

Poison Valleys: Diagnosing Path-Dependent Failure in LLM Code Repair
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2610.21514v1 [cs.SE] 15 Oct 2026
Poison Valleys: Diagnosing Path-Dependent Failure in LLM Code Repair
Veljko Skarich
Abstract
When code-repair agents fail, final tests reveal that a patch is wrong but not
which earlier commitment caused it or which software obligation failed. Poison
Valleys traces this path in 1,844 model requests on two synthetic Python cases:
PersistQueue adds atomic batch claiming to a disk-backed queue, while Dijkstra
adds source-sensitive filtering to shortest-path search. We define plausible
but incorrect software mechanisms, place each in a model’s hypothesis,
implementation plan, or both, and evaluate the generated code with an Oracle
and targeted diagnostic coordinates. Moving the misconception from hypothesis
to plan increased failure by 32.2% in PersistQueue and 28.9% in Dijkstra after
matching the experimental mix. Different misconceptions produced distinct,
model-dependent patterns of violated obligations, although several could
converge on the same behavior. This creates a measured connection from upstream
misconception to code mechanism and failure form. Code, data, and demo:
poisonvalleys.org
.
1
Introduction
1. CONTROL THE IDEA
Poison family placed in
hypothesis
/
plan
/
both
2. GENERATE A REPAIR
Model + reasoning effort
↓
\downarrow
Candidate code mechanism
3. EXECUTE AND DIAGNOSE
Oracle: PASS / FAIL
Coordinates: which obligations?
Figure 1:
From a controlled misconception to executable behavior.
A code-repair agent turns a bug report, test output, and repository context into
an explanation of the problem, an implementation plan, and finally a patch. A
passing test can confirm that the resulting program meets the tested contract.
A failing test, however, usually tells us only that the final patch is wrong.
It does not identify which earlier commitment caused the failure, how that
commitment became an implementation choice about state or control flow, or why two
different misconceptions produce different faulty programs. This missing link
limits both scientific explanations of agent behavior and attempts
to repair it.
Prior work can localize failures within agent trajectories, perturb particular
stages, and test whether changing an earlier step improves the outcome
(
Wang et al., 2026
;
Jaiswal et al., 2026
;
Ma et al., 2026
;
Lin et al., 2026
)
. We ask the
forward question: when a particular software misconception enters at a
particular stage, what code mechanism follows, and which executable software
obligations break?
We begin with
poison families
: specific, plausible but incorrect accounts
of how the target software works, together with the implementation commitments
and executable predictions that follow. We define these families before
generation and place one in the model’s hypothesis, implementation plan, or
both while holding the repair task fixed. We then trace the path from that
misconception to generated code and executable behavior under each model
configuration. We call these paths
Poison Valleys
because the supplied
misconception can channel repairs toward a structured region of failures rather
than merely lowering a single success rate.
We construct two synthetic repair cases on pinned versions of real Python
projects. PersistQueue is a disk-backed queue package
(
Wang, 2025
)
; our synthetic case adds an atomic batch-claim
operation whose failure must restore durable queue state and remain invisible
to other connections. NetworkX is a graph-analysis library
(
Hagberg et al., 2008
)
; our synthetic Dijkstra case extends its
multi-source shortest-path implementation with a filter whose decision depends
on the path’s original source. Neither case is a recovered historical upstream
bug. Both admit locally plausible repairs that violate a nonlocal obligation.
For each reconstructed candidate, an Oracle determines success or failure.
Independent diagnostic checks then identify which obligations survived, such
as rollback, isolation, record identity, route validity, weight correctness, or
API compatibility. These checks describe the form of a failure without
replacing the Oracle’s decision.
The experiment asks three questions. First, does a poison family become more
consequential when it moves from a hypothesis into an implementation plan?
Second, do different poison families produce different patterns of violated
software obligations? Third, does the model and reasoning-effort setting
change how strongly these effects appear? Across
1,844
model requests,
placing the poison family in the plan increased failure by about
30%
relative to placing it only in the hypothesis in
both tasks. Poison families also produced measurably different distributions of failed obligations, and
the size of the plan effect varied across model configurations.
Poison Valleys maps agent-level concepts to software behavior:
upstream misconception
\displaystyle\text{upstream misconception}
→
implementation commitment
\displaystyle\rightarrow\text{implementation commitment}
→
code mechanism
→
violated obligation
.
\displaystyle\rightarrow\text{code mechanism}\rightarrow\text{violated obligation}.
The stage identifies where a safeguard can intervene; the violated obligation
identifies what it must protect. A follow-up can return a model’s own
failed candidate with a repair prompt naming the violated obligations and test
whether the second candidate passes more checks. Because the original model
responses and downstream executable measurements are preserved, the reported
analysis can be inspected and replayed without making another model request.
2
Related Work
Three lines of work frame the experiment: code-repair trajectories, controlled perturbations of agent behavior, and counterfactual failure attribution. They locate errors in an agent trajectory and test whether an intervention changes the outcome. Poison Valleys instead traces a specified misconception at a specified repair stage into generated code and violated software obligations.
Code repair and trajectory analysis.
Code-repair systems transform issue descriptions, test observations, and repository context into localization decisions, repair reasoning, and patches. SWE-bench evaluates repository-level repairs through executable outcomes
(
Jimenez et al., 2024
)
, while SWE-agent, AutoCodeRover, Agentless, and VRpilot expose distinguishable activities such as repository exploration, fault localization, patch generation, and validation
(
Yang et al., 2024
;
Zhang et al., 2024
;
Xia et al., 2024
;
Kulsum et al., 2024
)
. Recent work examines these intermediate activities through failure taxonomies
(
Jiang et al., 2026
)
, reconstructed repair rationales
(
Li et al., 2026
)
, dependency-guided repair context
(
Wu et al., 2026
)
, and assessments of multi-step behavior beyond terminal reward
(
Ma et al., 2024
)
. OAT, TRAJDEBUG, AgentRx, and
Failure as a Process
further analyze anomalous actions, error lifecycles, failure onset, and recovery
(
Yeh et al., 2026
;
Qi et al., 2026
;
Barke et al., 2026
;
Zhao et al., 2026
)
. Together, these studies provide increasingly fine-grained evidence about where a repair trajectory departs from successful behavior. They provide less direct evidence about how a particular upstream software misconception becomes a concrete implementation mechanism and, in turn, determines which executable obligations the resulting program violates. Poison Valleys targets this connection directly.
Stage-wise perturbations and incorrect guidance.
Controlled interventions reveal how errors propagate through agent trajectories. STAR divides root-cause-analysis traces into stages, locates consequential reasoning faults, and replays stage-specific corrections
(
Wang et al., 2026
)
. ToolRobustBench aligns perturbations with tool interfaces, user intent, observations, and runtime environments
(
Zheng et al., 2026
)
. In code repair,
Obey, Diverge, Collapse
finds that incorrect instructions can induce semantic corruption that later self-guided repair does not fix
(
Jaiswal et al., 2026
)
.
Counterfactual attribution and executable consequences.
DoVer, REFLECT, and CausalFlow modify suspected messages, plans, or trajectory steps and replay later behavior
(
Ma et al., 2026
;
Lin et al., 2026
;
Bonagiri et al., 2026
)
. Project Ariadne intervenes on intermediate reasoning to audit causal and faithfulness claims
(
Khanzadeh, 2026
)
. Those methods start from a failure and repair a suspected earlier step. Poison Valleys runs forward from a specified poison family and repair stage. The Oracle determines correctness; diagnostic checks identify preserved and violated obligations.
3
Experimental Setup
3.1
Experimental design
The repair sequence is
O
→
D
→
H
→
P
→
C
O\rightarrow D\rightarrow H\rightarrow P\rightarrow C
(Table
1
). Within each case, the task stays fixed while a
reviewed poison family appears in the hypothesis, plan, or both.
Stage
Name
Definition
𝐎
\mathbf{O}
Observation
The fixed bug report and task requirements shown to the model.
𝐃
\mathbf{D}
Dependency context
Optional information about relevant surrounding code and interfaces.
𝐇
\mathbf{H}
Hypothesis
A proposed explanation of the bug and its underlying software mechanism.
𝐏
\mathbf{P}
Plan
The implementation commitments proposed to repair the bug.
𝐂
\mathbf{C}
Candidate code
The source files returned by the model after receiving the preceding inputs.
Table 1:
Stages in the observed repair sequence.
A poison family is a specific, plausible but incorrect software idea, such as
assigning transaction state to the wrong owner or losing a route’s fixed origin.
Before generation, we align its explanation, implementation commitments,
validating implementation, and executable witness. The validating code is never
shown to the model or used to classify generated code.
HYPOTHESIS (
H
H
)
PLAN (
P
P
)
Role
Explains
why
the bug occurs: a claim about the underlying software mechanism.
Commits to
how
code will change: operations, state ownership, ordering, and error handling.
PersistQueue A02
Restoring each claimed row to ready after failure is equivalent to atomic rollback.
Collect staged row IDs; after a SQLite error, write each status back to ready and then re-raise.
Dijkstra B01
The shortest-path search found the right winner; the defect exists only in result projection.
Run ordinary multi-source Dijkstra, then reject winning paths that fail the source filter.
Table 2:
A hypothesis explains the defect; a plan specifies the code changes.
Condition
Hypothesis (
H
H
)
Plan (
P
P
)
What changes
Canonical
Correct explanation
Correct implementation plan
Neither stage is poisoned.
H-only
Poison-family explanation
Correct implementation plan
The wrong account appears only in the explanation.
P-only
Correct explanation
Poison-family commitments
The wrong account directly specifies code choices.
H+P
Poison-family explanation
Matching commitments
The same wrong account appears at both stages.
Table 3:
Experimental conditions.
Dijkstra also includes no-plan conditions; PersistQueue additionally varies
dependency context. Neither variation defines the main intervention.
Our primary comparison is P-only versus H-only after retaining shared
family–model–dependency combinations and giving both conditions the same mix.
This controls for imbalance across stages. H+P stays separate to show
whether a matching hypothesis further reinforces the plan.
3.2
Controlled repair tasks
Both cases start from real Python packages and add a controlled public feature
plus a faulty implementation. They are not recovered historical
bugs. Table
4
separates what existed upstream from what the
the synthetic extensions add; Appendix
B
shows the colored task
prompts and their test mappings. PersistQueue is pinned at commit
b4fb6d186e375850b2d9ac49fc635779be95f173
; Dijkstra uses NetworkX 3.6.
Both upstream packages are distributed under the BSD 3-Clause license.
Case
Existing package
Synthetic extension
Fault and required repair
PersistQueue
Disk-backed SQLite queue with single-item
get
,
ack
,
nack
, durable IDs, and FIFO/FILO behavior
(
Wang, 2025
)
.
claim_batch
(max_items, *,
raw=False)
, plus a batch-write context and delayed cache publication.
Nested status helpers can commit independently of the apparent outer batch. A correct repair must make selection and every status mutation one rollback unit and publish memory state only after commit.
Dijkstra
NetworkX 3.6 multi-source Dijkstra, whose dominance state is keyed by graph node
(
Hagberg et al., 2008
)
.
source_filter
(origin, u, v,
edge_data)
on the public path, path-length, and main APIs.
The faulty search carries
origin
in the heap but still finalizes by node, discarding a costlier arrival whose origin may permit later edges. A correct repair must preserve origin-specific state until public projection.
Table 4:
Existing package, synthetic addition, and repair contract.
PersistQueue.
Upstream PersistQueue selects and claims one row at a time. The synthetic case adds
SQLiteAckQueue.claim_batch
, a reentrant batch-write context, and a
publish
switch that delays updates to the in-memory unacknowledged
cache and count. The faulty method appears to wrap the loop in one
transaction, but each call to the existing decorated status helper can enter
and commit the SQLite connection independently. If the second row fails, the
the first row can remain durably claimed even though the public call
raised. The repair must use one transaction owner for selection and all status
writes, preserve the exact original row IDs and FIFO/FILO order, hide partial
work from other connections, and update cache/count state only after commit.
Appendix
18
maps each part of that contract to
executable tests; Appendix
12
gives all eleven plausible
but wrong mechanisms.
Dijkstra.
Upstream NetworkX 3.6 accepts several sources but has no source-dependent edge
policy. The synthetic case adds the callback
source_filter(origin, u, v, edge_data)
to three public APIs. Here
origin
is the fixed depot where the complete path began; it is not the
currently expanded node. The faulty helper includes the origin in heap
entries but retains ordinary node-keyed
seen
and
dist
maps.
That is invalid once future edge permissions depend on origin: a cheaper arrival
from one depot can erase a more expensive arrival from another depot that alone
may legally continue. The repair must keep origin-specific search states, then
project the cheapest permitted result by node while preserving ordinary weights,
cutoffs, exceptions, and no-filter behavior. Appendix
16
maps the contract to tests; Appendix
14
defines all eight
wrong mechanisms.
3.3
Intervention and model requests
For each request, only the assigned hypothesis and plan change; the task, source
inventory, response format, and evaluation stay fixed. Each request produces one
candidate, so H-only and P-only name where information was supplied, not
separate calls.
The requested model configuration is the model and reasoning-effort
setting sent to the provider. PersistQueue uses GPT-5.6 Luna, GPT-5.4 Nano, and
Claude Haiku 4.5; Dijkstra uses GPT-5.6 Luna, Claude Sonnet 5, and Qwen 3.8
Flash. The primary comparison uses configurations represented in both
conditions. A unique request identifier joins prompt, response, candidate,
execution, and analysis records.
Assignment records what the model received, not what it believed. Generated code
may copy, transform, compensate for, or ignore the supplied mechanism, so we
measure code behavior independently.
3.4
System design and replay
Saved response
provider response bytes
Reconstruction
complete source tree
Isolated execution
candidate outputs
Oracle
PASS / FAIL
Diagnostic checks
behaviors preserved or violated
Figure 2:
Post-generation evaluation and replay.
Each request UUID joins its prompt, response, source tree, execution, and
analysis row. SHA-256 digests identify the exact records at every handoff.
Replay verifies them, reconstructs the candidate, and reruns execution without
another model call; hashes establish identity, while tests establish behavior.
Reconstruction combines returned files with the expected inventory. Responses
that cannot produce a complete tree remain in request accounting but receive no
generated-code behavior.
3.5
Oracle and diagnostic checks
Measure
What executes
Output
Example
Oracle
The complete task protocol compares the candidate’s public outputs with expected outputs.
One overall success or failure.
PersistQueue must return the correct batch and leave durable queue state correct after success or failure.
Coordinate
One targeted executable scenario tests one software obligation.
One check passes or fails.
A second connection tries to observe a partially completed claim; hidden state passes the isolation coordinate.
Axis
Related coordinates are grouped by the behavior they test.
An interpretable failure dimension.
Dijkstra shared-junction coordinates contribute to the routing axis because edge legality depends on the original source.
Table 5:
Oracle, coordinate, and axis.
The
Oracle
determines whether the repair succeeds or fails. For the main
binary outcome, every reconstructed candidate that does
not finish successfully counts as a failure. This includes an ordinary Oracle
failure, a runtime crash, a timeout, or an incomplete evaluation; the specific
reason is recorded separately. Diagnostic checks then test individual software
obligations. PersistQueue uses
18
selected checks and Dijkstra uses
28
. These checks show how a candidate behaved but never overturn the Oracle’s correctness
decision. Appendix
C
defines the selected coordinates,
and Table
27
reports every terminal failure subtype.
When the required checks complete, their results are reduced to the
four task-specific obligation groups in Table
4
. When they
do not complete, we report incomplete diagnostic evidence rather than inventing
a failure pattern.
Task
Requests
Responses
Candidates
Oracle
Success
Failure
PersistQueue
982
843
835
672
453 (
54.3%
)
382 (
45.7%
)
Dijkstra
862
798
798
668
216 (
27.1%
)
582 (
72.9%
)
Total
1,844
1,641
1,633
1,340
669 (
41.0%
)
964 (
59.0%
)
Table 6:
Request flow and candidate outcomes.
Success and failure percentages are calculated from reconstructed candidates;
every reconstructed candidate that does not finish successfully
counts as a failure. Requests without a response or candidate remain visible
in the flow but cannot describe generated-code behavior. The primary comparison
gives H-only and P-only the same mix of represented poison families, model
configurations, and dependency settings. We compute
95%
intervals by
resampling complete request UUIDs so that all records from one request remain
together.
All model responses used in the analysis are preserved. Offline replay begins
from a saved response, reconstructs the candidate, and reruns the executable
measurements without making another model request. Code, data, and the interactive
demonstration are available at
poisonvalleys.org
; detailed family packages,
prompt templates, model settings, executable checks, and analysis tables are
provided in the appendix.
4
Main Results
4.1
Where the poison family appears
Placing a poison family in the implementation plan caused
substantially more failures than placing it only in the hypothesis. The raw
failure rate rose from
21.9%
to
54.7%
in PersistQueue and
from
53.4%
to
83.0%
in Dijkstra
(Table
7
). Because the two conditions did not
contain exactly the same mix of poison families, model
configurations, and dependency settings, we also compared only combinations
represented in both conditions and gave those combinations the same weight.
Under that comparison, plan-only assignment increased failure by
32.2%
in PersistQueue and
28.9%
in
Dijkstra. The corresponding failure-risk ratios were
2.44 [2.12, 3.23]
and
1.54 [1.35, 1.88]
: after balancing the
experimental mix, plan-only attempts failed about 2.4 and 1.5 times as often.
The intervals in
Table
7
describe uncertainty across repeated
model requests.
Task
Hypothesis only
Plan only
Difference with the same experimental mix
PersistQueue
59/270 (21.9%)
145/265 (54.7%)
+32.2% [27.0%, 38.8%]
Dijkstra
101/189 (53.4%)
156/188 (83.0%)
+28.9% [21.1%, 38.6%]
Table 7:
Failure rates by intervention stage.
Once the poison family was already present in the plan, adding the matching
hypothesis produced a much smaller further change:
6.3%
in
PersistQueue
[0.5%, 12.2%]
and
2.2%
in Dijkstra
[
−
-
4.9%, 8.5%]
. The smaller change is consistent with the plan
acting as the more consequential commitment point;
it does not imply that planning itself is harmful.
4.2
Which poison family is supplied
Poison families changed not only how often candidates failed, but also
which software obligations they violated
. Each diagnostic check tests a
behavior, and related checks are grouped into the eight axes defined
in Table
10
. Table
9
shows selected PersistQueue plan-only distributions. These checks describe
failure form; they do not
override the Oracle’s decision.
The relationship was structured but not deterministic. To summarize its
strength, we use Cramér’s
V
V
, an association score ranging from 0
(no relationship) to 1 (perfect relationship). For plan-only attempts,
the score was
0.475 [0.453, 0.556]
in PersistQueue and
0.314 [0.307, 0.434]
in Dijkstra. Different poison families produced measurably different
distributions of failed obligations, while one family could still produce
several failure patterns and different families could converge on the same
violated obligation.
The fixed-family Dijkstra B01 comparison in
Table
8
illustrates that model configuration
can also change the outcome.
Experiment key held fixed: Dijkstra
⋅
\cdot
B01 post-filter
⋅
\cdot
plan-only
Same poison family and stage; only the model configuration differs.
Model
Oracle
Routing
Weights
API
Compatibility
Dijkstra success
GPT-5.6 Luna, medium
PASS
Preserved
Preserved
Preserved
Preserved
119/340 (
35.0%
)
Qwen 3.8 Flash
FAIL
Violated
Violated
Preserved
Preserved
6/127 (
4.7%
)
Table 8:
The same Dijkstra B01 plan-only intervention produced different behavior across model configurations. The final column reports success across all Dijkstra candidates for each model.
In PersistQueue, a
mechanism that tried to compensate for transaction state in memory was
associated mainly with failures of cross-connection isolation: behavior could
look correct through one connection while another observed the wrong queue
state. In Dijkstra, mechanisms that discarded the fixed route origin while the
search was still running were associated mainly with routing failures at
shared junctions, where the legality of a later edge depends on the path’s
origin, linking the supplied misconception to a state decision and an executable
obligation.
We inspected twelve selected generated patches. Five of six
sampled failures and all six sampled passes made a substantive,
mechanism-relevant code change. Because this was a targeted sample,
it illustrates individual pathways and does not estimate how often models adopted
the supplied mechanism across the full corpus.
4.3
Differences across model configurations
A model configuration is the model and reasoning-effort setting requested
for an attempt. The plan-only versus hypothesis-only difference varied across
these configurations. In PersistQueue, the differences ranged from
−
-
3.8% to +45.1%
; in Dijkstra, they ranged from
+6.6% to +39.1%
.
The same intervention can be expressed differently by different
model configurations. These exploratory comparisons do not provide a general
model ranking and do not establish that one model universally reasons better
than another.
The plan-versus-hypothesis result kept the same direction when we
left out one poison family or one model configuration at a time, and when we
restricted the comparison to combinations represented in both conditions that
completed the Oracle. Missing candidates and incomplete diagnostic evidence
remain reported separately rather than being assigned an invented failure
pattern. Detailed condition tables, the model-level success and failure table
(Table
20
), robustness checks, and complete failure
accounting appear in Appendix
D
and
Appendix
E
.
5
Discussion
The main result is that a poison family becomes more consequential when
it is expressed as an implementation plan rather than only as an explanation
of the bug. A hypothesis still leaves room to reject the explanation or choose
a safe implementation. A plan commits the repair to operations,
owners of state, update order, error handling, and compatibility choices. When
those commitments are wrong, they can pass directly into code. This does not
mean that planning is harmful. It means that a plan is a high-leverage boundary
where a repair system should check whether the proposed operations preserve the
software contract. The experiment records what information the model received,
not what it believed or internally represented.
Failure rate and failure form answer different questions. The Oracle tells us
whether a candidate satisfies the repair
contract. The diagnostic checks identify the particular obligation that did or
did not survive: for example, restoring queue state after failure, hiding
uncommitted state from another connection, or preserving a route’s original
source. Different poison families produced different distributions of
these violated obligations, but the relationship was not one-to-one. One family
could produce several failure patterns, and different families could converge
on the same failed behavior. This is not a classifier that guesses which prompt
input a model saw. It links a specified misconception, through a code mechanism, to an
executable consequence.
Family (
n
n
)
Intact
Isolation only
Recovery + isolation
Broad
Incomplete
A02 (
n
=
25
n=25
)
8%
92%
0%
0%
0%
A08 (
n
=
25
n=25
)
24%
44%
28%
0%
4%
A14 (
n
=
24
n=24
)
17%
0%
38%
17%
29%
Table 9:
Diagnostic outcomes for selected PersistQueue poison families in plan-only attempts. The first column gives the code-bearing attempt count
n
n
; entries are percentages rounded independently.
In Table
9
,
intact
means all
selected diagnostic axes passed;
broad
means failures across several
obligation groups; and
incomplete
means the diagnostic panel did not
yield a phenotype. These diagnostic outcomes are separate from the Oracle
verdict.
Generated source can also reveal how a model engaged with a supplied plan. One
A08 plan-only response left the comment, “
_pop
commits each status
update independently,” and proposed compensating for later claim
failures. That comment is evidence about the mechanism expressed in code, not
a verdict: the Oracle still tests public outputs, and the coordinates still
show which obligations survived.
Axis
Question
PersistQueue
Recovery
After a database error, are the same rows ready again without an observable intermediate claim?
Identity
Does the batch contain the exact selected row IDs, multiplicity, and native order?
Isolation
Can another connection observe or interfere with a claim before it commits?
Durability
Do database rows, cache/count state, and reopen behavior agree after commit or failure?
Dijkstra
Routing
Is every edge legal for the fixed origin that began the path?
Weights
Are graph type, edge weights, hidden edges, cycles, and cutoffs handled correctly?
API
Do public signatures, return shapes, exceptions, and graph immutability remain correct?
Compatibility
Do unfiltered NetworkX behavior and larger branching cases still work?
Table 10:
Diagnostic axes by repair task.
The mapping depends on the task and model. PersistQueue and Dijkstra showed
the same overall increase when the poison family appeared in the plan, but
they exposed different state, routing, and compatibility obligations. The size
of the increase also varied across model and reasoning-effort settings.
This variation is not a global model ranking. It shows why interventions should
be evaluated against the contract of the software being repaired and against
the model configuration that will use them. A universal label such as
reasoning failure
would hide the code-level distinction between repairs.
The plan-to-code boundary is a natural intervention point. A repair system can check
whether the plan assigns state to the right owner, preserves rollback and
isolation, carries forward information needed later in execution, and retains
the existing API contract. Whether those checks improve a second repair remains
untested. A follow-up should give the same model its own failed candidate together with a repair
prompt naming the violated obligations, then test whether the second candidate
passes the Oracle and fails fewer or different diagnostic checks.
6
Limitations
Two controlled repair tasks.
PersistQueue and Dijkstra were designed to expose specific software obligations
under deterministic execution. That control makes the mechanism-to-code link
inspectable, but it does not represent the full diversity of repositories,
languages, naturally occurring bugs, or misleading information that repair
agents encounter. The repeated direction across the two tasks supports the
experimental method; it does not establish a universal effect size.
Uneven and missing evidence.
Not every poison family, model configuration, and dependency setting has the
same number of requests, and some combinations are absent. The primary
comparison therefore uses only combinations represented in both the
hypothesis-only and plan-only conditions and gives those combinations the same
weight. This cannot tell us what would happen in combinations we did not run.
Some requests also returned no response or no reconstructable candidate. They
remain in the request accounting and missing-data checks, but they cannot
contribute evidence about generated-code behavior.
Finite executable checks.
The Oracle and diagnostic checks cover the repair contracts we specified; they
are not complete specifications of PersistQueue or NetworkX. A passing candidate
may contain an untested defect. A failed candidate may stop before every
diagnostic check completes, in which case we report that the failure pattern is
unknown rather than infer one from partial evidence. Visible output and
exception text are even less specific and can make different executable states
look the same.
Assignment, model changes, and uncertainty.
We know which hypothesis and plan each model received, but we did not
ask human reviewers to decide whether every generated patch believed, copied,
or literally implemented the supplied mechanism. The twelve inspected patches
provide individual examples, not a corpus-wide adoption rate. The model names
also refer to the exact provider configurations available during data
collection; provider updates or routing changes may alter future results.
Repeated requests that share a poison family or experimental
setting are related rather than wholly independent. Our uncertainty intervals
keep records from the same request together, but comparisons between individual
model configurations remain exploratory.
7
Conclusion
Poison Valleys connects a specific upstream misconception to the implementation
commitment it creates, the code mechanism that follows, and the executable
obligation it violates. Across
1,844
model requests on two controlled
repair tasks, placing a poison family in the plan increased failure by
32.2%
in PersistQueue and
28.9%
in Dijkstra relative to
placing it only in the hypothesis. Different mechanisms produced different
patterns of violated obligations, and the size of the effect varied across exact
model and reasoning-effort settings.
Inspect a repair after the plan is formed but before it becomes code, and check
the software obligations most at risk. A follow-up should give the same model its own failed candidate plus
a prompt naming the violated obligations, then measure whether the repaired
candidate passes the Oracle and fails fewer diagnostic checks.
References
Barke
et al.
(2026)
S. Barke, A. Goyal, A. Khare, A. Singh, S. Nath, and C. Bansal
AgentRx: diagnosing AI agent failures from execution trajectories
.
arXiv preprint arXiv:2602.02475
.
External Links:
Link
Cited by:
§2
.
Bonagiri
et al.
(2026)
A. Bonagiri, D. Borkar, G. J. Anderias, S. Rafatirad, and H. Homayoun
CausalFlow: causal attribution and counterfactual repair for llm agent failures
.
External Links:
2605.25338
,
Link
Cited by:
§2
.
Hagberg
et al.
(2008)
A. A. Hagberg, D. A. Schult, and P. J. Swart
Exploring network structure, dynamics, and function using NetworkX
.
In
Proceedings of the 7th Python in Science Conference
,
pp. 11–15
.
Cited by:
§1
,
§3.2
.
Jaiswal
et al.
(2026)
R. Jaiswal, A. S. Divy, S. Bhasin, A. Bajpai, T. Ganu, and R. R. Shah
Obey, diverge, collapse: blind obedience to incorrect instructions drives code llms to irrecoverable code semantic collapse
.
External Links:
2607.04537
,
Link
Cited by:
§1
,
§2
.
Jiang
et al.
(2026)
Y. Jiang, Y. Huang, G. Wang, J. Chen, H. Liu, and L. Briand
Characterizing the failure modes of LLMs in resolving real-world GitHub issues
.
arXiv preprint arXiv:2605.12270
.
Cited by:
§2
.
Jimenez
et al.
(2024)
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan
SWE-bench: can language models resolve real-world GitHub issues?
.
In
International Conference on Learning Representations
,
Cited by:
§2
.
Khanzadeh (2026)
S. Khanzadeh
Project ariadne: a structural causal framework for auditing faithfulness in llm agents
.
External Links:
2601.02314
,
Link
Cited by:
§2
.
Kulsum
et al.
(2024)
U. Kulsum, H. Zhu, B. Xu, and M. d’Amorim
A case study of LLM for automated vulnerability repair: assessing impact of reasoning and patch validation feedback
.
arXiv preprint arXiv:2405.15690
.
Cited by:
§2
.
Li
et al.
(2026)
C. Li, Y. Xu, Z. Wang, S. H. Tan, and Tse-Hsun (Peter) Chen
Independent patch verification for coding agents with a bidirectional reconstruct-and-verify framework
.
arXiv preprint arXiv:2608.08950
.
Cited by:
§2
.
Lin
et al.
(2026)
X. Lin, Y. Wang, T. S. T. Kwok, D. Guo, S. A. Nale, C. Fleming, and G. Cheng
REFLECT: intervention-supported error attribution for silent failures in llm agent traces
.
External Links:
2606.09071
,
Link
Cited by:
§1
,
§2
.
Ma
et al.
(2024)
C. Ma, J. Zhang, Z. Zhu, C. Yang, Y. Yang, Y. Jin, Z. Lan, L. Kong, and J. He
AgentBoard: an analytical evaluation board of multi-turn LLM agents
.
In
Advances in Neural Information Processing Systems
,
Vol.
37
.
Cited by:
§2
.
Ma
et al.
(2026)
M. Ma, J. Zhang, F. Yang, Y. Kang, Q. Lin, S. Rajmohan, and D. Zhang
DoVer: intervention-driven auto debugging for LLM multi-agent systems
.
In
The Fourteenth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
,
§2
.
Qi
et al.
(2026)
Y. Qi, Z. Yin, X. Shi, H. Peng, S. Lu, Y. Liu, R. Xuan, Y. Liu, Z. Hu, X. Wang, L. Hou, B. Xu, and J. Li
TRAJDEBUG: tracing error lifecycle to identify critical failures in long-horizon agent trajectories
.
arXiv preprint arXiv:2608.06346
.
Cited by:
§2
.
Wang
et al.
(2026)
J. Wang, X. Liao, and W. Wu
STAR: a stage-attributed triage and repair framework for rca agents in microservices
.
External Links:
2605.15581
,
Link
Cited by:
§1
,
§2
.
Wang (2025)
P. Wang
persist-queue: a thread-safe disk-based persistent queue in python
.
Note:
https://github.com/peter-wangxu/persist-queue/releases/tag/v1.1.0
Version 1.1.0, commit b4fb6d1; BSD-3-Clause software
Cited by:
§1
,
§3.2
.
Wu
et al.
(2026)
L. Wu, Y. Chen, Z. Yang, P. Xue, and D. Hao
CausalRepair: bridging the causality gap in large language model-based automated program repair via dual-slicing
.
arXiv preprint arXiv:2608.10613
.
Cited by:
§2
.
Xia
et al.
(2024)
C. S. Xia, Y. Deng, S. Dunn, and L. Zhang
Agentless: demystifying LLM-based software engineering agents
.
arXiv preprint arXiv:2407.01489
.
Cited by:
§2
.
Yang
et al.
(2024)
J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press
SWE-agent: agent–computer interfaces enable automated software engineering
.
arXiv preprint arXiv:2405.15793
.
Cited by:
§2
.
Yeh
et al.
(2026)
S. Yeh, Y. Zhu, S. Deep, and S. Li
Tracing agentic failure from the flow of success
.
arXiv preprint arXiv:2607.12747
.
Cited by:
§2
.
Zhang
et al.
(2024)
Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury
AutoCodeRover: autonomous program improvement
.
In
Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis
,
pp. 1592–1604
.
External Links:
Document
Cited by:
§2
.
Zhao
et al.
(2026)
X. Zhao, H. Li, S. Li, T. Zhao, E. T. Barr, F. Sarro, and H. Ye
Failure as a process: an anatomy of CLI coding agent trajectories
.
arXiv preprint arXiv:2607.09510
.
External Links:
Link
Cited by:
§2
.
Zheng
et al.
(2026)
Y. Zheng, Y. Wu, and Y. Chang
ToolRobustBench: stage-wise perturbation evaluation and failure diagnosis for tool-calling agents
.
External Links:
2608.23635
,
Link
Cited by:
§2
.
Appendix A
Poison-Family Catalog and Mechanisms
A.1
What a poison family specifies
A poison family is a reviewed, versioned false repair theory, not merely a
short label attached to a prompt. Each family binds four aligned objects: a
plausible false hypothesis about the defect, a plan that operationalizes that
hypothesis, an executable known-wrong realization used during qualification,
and one or more executable witnesses at the public behavioral boundary that
expose the intended mistake. The hypothesis remains diagnosis-only and the plan
remains commitment-only: neither input tells the model that it is poisoned,
names the qualification failure, or explains the contradiction that defeats
it. Exact input bytes and hashes are frozen before use.
The known-wrong realization is a qualification instrument, not a prediction
that generated code will reproduce the same source. It establishes that the
false theory is mechanically coherent, can be implemented without unrelated
syntax or import failure, and is rejected at the intended behavioral boundary.
Under intervention, a model may copy that mechanism, form a hybrid, switch to a
different mechanism, repair the supplied premise, or produce code that cannot
be semantically localized. The empirical object is therefore the complete
attempt-level distribution generated by the prospectively selected family and
stage, not similarity to the known-wrong patch.
A
qualification-witness signature
names the failure pattern that rejects
the known-wrong realization, such as a committed prefix after an exception. It
is not the captured public output, a public-observation vector, or a
public_observation_hash
. We separately use
family behavioral
signature
for the attempt-level distribution over semantic modes generated by
an intervention condition. The former qualifies the false mechanism; the
latter describes what generated repairs actually do.
Family numbers are identifiers rather than an ordering by severity or
difficulty. Gaps reflect mechanisms that were reserved, merged, rejected, or
not admitted after review. Two families can also share a
qualification-witness signature under the present qualification instrument
while remaining causally distinct interventions. In PersistQueue, A01, A05,
and A07 all admit a
committed-prefix failure, but they attribute it respectively to missing outer
rollback, insufficient preflight, and insufficient locking. In Dijkstra, B03
and B06 both erase fixed-origin identity after the first hop, but one does so
through a first-edge policy and the other through a synthetic-super-source
construction. We retain these families separately because their hypotheses,
implementation commitments, and source mechanisms differ. This separation is
essential for asking which false account a model follows; an output cluster
alone cannot supply that answer.
A.2
PersistQueue: transactional poison families
PersistQueue’s correct repair must place selection and status mutation inside
one owned transaction, preserve exact row identity and native FIFO/FILO order,
isolate unrelated actors, and publish cache and count state only after the
database commit. The eleven A-families each relax or mislocate a different part
of that contract. Table
12
records the model-visible
false account and its induced commitment, followed by the distinguishing
failure for which the executable family was qualified.
Family
False hypothesis and plan commitment
Defeating behavioral distinction
A01: outer rollback
The outer batch transaction is assumed to be the only uncommitted unit. The
plan explicitly rolls it back after a database error while leaving the nested
status helpers unchanged.
Nested helpers can already have committed earlier status writes. Rolling back
the wrapper therefore leaves a claimed prefix visible after the call fails.
A02: compensating reset
Returning every staged row from unacknowledged to ready is treated as equivalent
to rollback because the final status values match. The plan performs reverse
status writes after an error.
Compensation is itself committed behavior. An external observer can see
ready–unacknowledged–ready transitions, and concurrent actors can interact
with the transiently claimed rows.
A03: ownerless transaction
Existing instance locks are assumed to imply that every helper called while a
queue-level transaction field is populated belongs to the active batch. The
plan routes selection and writes through that field without binding its owner.
An unrelated same-instance thread can borrow the active transaction, coupling
its write to another caller’s commit or rollback; reopen then exposes the
cross-thread state error.
A04: read visibility
Only writes are considered relevant to transaction ownership. The plan routes
decorated writes into the batch transaction but leaves selection on the stale
reader connection because reads are assumed harmless.
Selection does not see the transaction’s own updates. A successful loop can
repeat or lose record identities, and concurrent claimers cease to be
serializable even though the writes share a transaction.
A05: preflight validation
The batch is diagnosed as entering mutation before every row-level status
statement is known to be admissible. The plan preflights selected statements
with SQL
EXPLAIN
before running the existing per-item loop.
Static preflight cannot predict a later execution or serialization failure.
Once a real later update fails, earlier per-item commits can remain durable.
This shares a qualified committed-prefix witness signature with A01 and A07.
A07: lock-only serialization
Inconsistent lock lifetime is blamed for partial claims. The plan holds the
instance transaction lock across the entire existing claim loop but preserves
the selection and status-helper implementation.
Serialization prevents one class of interleaving but does not make individually
committed writes atomic. A single-threaded later failure still leaves a prefix,
and a second queue instance is outside the instance-local lock.
A08: reinsert compensation
Recovery is defined by the multiset of payload values rather than durable record
identity. The plan deletes staged rows and reinserts their payloads as fresh
records after a later error.
Reinsertion creates replacement IDs and timestamps and can change duplicate and
queue order. Reopen exposes a replacement record rather than restoration of the
original claimed row.
A10: wrong-connection savepoint
The absence of a named rollback checkpoint around the nested calls is treated
as the defect. The plan creates a savepoint on the shared
_putter
connection around the loop and attempts rollback and release during cleanup.
Nested decorated status helpers commit that same connection, invalidating the
savepoint and separating the apparent savepoint scope from the real atomic
groups. Cleanup can then mask the injected failure with missing-savepoint
state.
A11: identity-losing bulk update
Atomically changing exactly
N
N
claimable rows is assumed sufficient. The plan
bulk-updates rows, then reconstructs the returned IDs by querying the first
N
N
unacknowledged rows and pairing them with previously selected payloads.
Preexisting unacknowledged rows, duplicate payloads, smaller batches, and
FIFO/FILO reversal separate mutation count from exact selected identity and
order.
A14: retry after failure
A row-local status error is treated as a transient obstruction rather than a
batch failure. The plan advances past the failing row and continues until the
requested size is reached or no candidate remains.
The exception is swallowed as a control decision: a committed prefix can
precede the retry, while the returned batch skips the failed identity and
changes native order or size.
A16: persistence bypass
The post-exception inconsistency is attributed to in-memory publication. The
plan snapshots and restores cache and count fields while leaving the existing
database mutation path intact.
Restoring memory cannot undo durable SQLite status writes. A fresh instance or
reopen observes claimed rows even when the original object’s cache and counter
appear restored.
Table 12:
PersistQueue poison-family mechanisms.
The corrected P-only and H+P family counts show that these mechanisms do not
form a simple severity ladder; Table
9
gives selected P-only examples. A02 is strongly
isolation-oriented in both stages (23/25 and 23/26). A05 and A10 often combine
recovery and isolation; A11 is also isolation-dominant (21/25 and 19/26). A04
usually lacks a complete coordinate signature (19/24 and 21/24), yet every
terminal failure in those cells still has a specific cause subcategory. This is
a useful counterexample to equating a qualification-witness signature with a
generated-code behavioral signature: the family intervention is known, but the
coordinate instrument need not completely localize every resulting failure.
These distributions clarify what family-level “resistance” means. It is an
executable outcome, not a judgment that the model verbally rejected the prompt:
an intact repair may explicitly contradict the supplied plan, silently replace
it with the canonical mechanism, or reach a different correct implementation.
Likewise, an isolation- or broad-dominant family behavioral signature does not
prove literal copying of the qualified patch. The family defines the
intervention; the semantic mode records the downstream behavior.
A.3
Dijkstra: origin-sensitive search poison families
In multi-source Dijkstra with an origin-dependent edge policy, a state must
retain every dimension that changes the legality of future transitions. A
source-labeled arrival cannot be discarded solely because another source
reaches the same graph node more cheaply; dominance is valid only within the
state identity used by later filtering. The eight B-families target different
places where this fixed-origin identity can be consulted too late, substituted,
stored only partially, or erased. Table
14
gives the
mechanistic catalog.
Family
False hypothesis and plan commitment
Defeating behavioral distinction
B01: post-filter
The core search is assumed correct and only its public projection is blamed.
The plan runs ordinary multi-source Dijkstra, reconstructs winners, and removes
paths that fail
source_filter
afterward.
The node-keyed search may already have pruned a more expensive but permitted
source alternative. Deleting the invalid winner cannot reconstruct the valid
route, in either target or all-target output.
B02: current-node origin
The callback’s first argument is treated as the node whose adjacency is being
expanded rather than the depot that began the path. The plan passes the current
node as both policy source and edge source.
The policy then changes meaning at every hop. A single-source reference route
and a shared-junction route distinguish fixed path origin from current search
location.
B03: first-edge only
The source policy is treated as an admission rule for leaving a depot. The plan
checks only the first edge and runs ordinary Dijkstra for the remainder of the
path.
A later forbidden edge becomes traversable after an allowed first hop. The
source-switching trap exposes this first-hop origin erasure and its effects on
target and all-target routing.
B04: partial source state
Only tentative collisions are blamed. The plan keys provisional distances and
paths by
(
o
​
r
​
i
​
g
​
i
​
n
,
n
​
o
​
d
​
e
)
(origin,node)
but still finalizes and prunes all alternatives by
node.
Finalized dominance remains invalid because origin still changes future edge
permission. A later legal continuation can require the source-labeled arrival
discarded at the shared node.
B05: paths-only state
Distances are assumed correct while reconstructed paths alone are said to lose
the depot. The plan stores source-indexed paths but retains one node-level
distance, finalization decision, and heap entry.
Path identity and distance identity become incoherent: the source used for
filtering or publication need not own the distance that won the node-level
competition. Branching and source-order probes expose the mismatch.
B06: super-source
The search is modeled as a zero-cost synthetic super-source whose branch label
matters only on the first real edge. The plan erases that label afterward and
permits a later edge if any depot would permit it.
Future permission still depends on the original branch. Its qualification
witness signature is grouped with B03 under first-hop origin erasure, but it
reaches the defect by unioning permissions after a synthetic-source
construction.
B12: global edge cache
Filtering is treated as an expensive, stable property of the directed edge.
The plan runs per-source searches but shares a permission cache keyed only by
(
u
,
v
)
(u,v)
.
The first depot to inspect an edge determines its visibility for every later
depot. Source-order invariance and false-success probes expose the omitted
origin dimension in the cache key.
B13: target fallback
The combined search is treated as adequate whenever it returns a target. The
plan retries per source only after a target-mode miss, leaving successful target
answers and all-target dictionaries on the original fast path.
A returned target can still be the wrong permitted route, and an all-target
query never triggers recovery. Target/all-target paired probes expose this
asymmetric projection repair.
Table 14:
Dijkstra poison-family mechanisms.
The corrected Dijkstra family counts keep P-only and H+P separate.
B03 and B13 are the cleanest routing probes:
B03 produces routing phenotypes in 21/25 P-only and 26/26 H+P attempts, while
B13 produces them in 20/23 and 19/23. B02 mixes routing,
weight, intact, and incomplete-panel phenotypes. B04 and B05 likewise show that
partially preserving one component of source state can yield several
downstream forms rather than one family-determined result. Diagnostic
incompleteness remains visible, but it never substitutes for the specific
terminal failure classification.
A.4
How poison families relate to executable checks
A poison family names the wrong idea supplied to the model, and the intervention
stage records where that idea was supplied. After the model generates code, the
Oracle answers the binary question: did the repair work? Diagnostic coordinates
are executable checks that answer a finer question: which specific behaviors
survived? We group those checks into four correctness axes—Recovery, Identity,
Isolation, and Durability for PersistQueue; Routing, Weights, API, and
Compatibility for Dijkstra. Each axis asks one question:
Recovery
After something goes wrong, does the queue recover cleanly?
Identity
Does it claim and return the right records?
Isolation
Can another actor observe or interfere with partial work?
Durability
Does the queue remain correct after commit, failure, and reopen?
Routing
Does it choose a route that is legal for the original source?
Weights
Does it preserve correct graph and weight behavior?
API
Does it preserve the public interface and error behavior?
Compatibility
Does ordinary behavior still work across larger and unfiltered cases?
The first four questions apply to PersistQueue and the second four to Dijkstra.
When the selected panel is complete, the resulting four-axis pattern is the
repair’s
executable phenotype
. Incomplete diagnostic evidence has no
phenotype. The Oracle tells us whether the repair worked; the
coordinates show which obligations survived; and only complete coordinate
evidence supports phenotype reduction.
The connection between poison families and coordinates is intentional but not
deterministic. A poisoned plan prescribes a concrete code-level mechanism, whereas
a coordinate executes a behavioral scenario and checks its consequences. The
coordinate evaluator is therefore treatment-label-blind: it receives no
poison-family label and does not inspect the diagnosis or plan for family-specific
language. The shared coordinate panel is nevertheless mechanism-informed.
Several checks were designed to exercise the same task-contract distinctions that
motivated the poison catalog. Thus a coordinate can directly test a consequence
predicted by a family without recognizing that family, and different mechanisms
can fail the same check.
Compensation versus rollback (A02).
The A02 plan treats returning each staged row from unacknowledged to ready as
equivalent to rollback. The cross-instance failure check instead forces a claim
to fail, pauses the operation while a second queue instance observes and writes
the database, and then checks isolation, rollback, reopen behavior, and later
access. This scenario directly exposes A02’s predicted ready–unacknowledged–ready
transition and its interaction with another actor. It does not search the repair
for a compensating-reset loop: A03’s shared transaction, A07’s instance-local
locking, or another concurrency defect can violate the same executable check.
Payload restoration versus record identity (A08).
The A08 plan deletes claimed rows and reinserts their payloads after failure,
restoring superficially similar contents under new durable identities. The
replacement_compensation
checks seed duplicate payloads, force the
second status update to fail, verify that the original record identities survive,
and verify them again after reopen. These checks are tightly aligned with A08’s
predicted consequence but remain implementation-general: any recovery strategy
that recreates values while losing identity, multiplicity, order, or durable
continuity can fail them.
Fixed origin in filtered Dijkstra (B02, B03, and B06).
B02 substitutes the currently expanded node for the fixed source that began the
route; a single-source reference route distinguishes those callback meanings.
B03 checks only the first edge, while B06 erases synthetic-branch identity and
allows a later edge when any source permits it. The source-switching trap builds a
route that succeeds only if source authority changes or disappears after the
first hop. It can therefore expose both B03 and B06 even though their proposed
code mechanisms differ. These probes test the invariant that every edge is
authorized for one fixed originating source; they do not identify which family,
if any, produced the violation.
This many-to-many relation is the object of measurement rather than a defect in
it. A supplied family may be ignored, partially realized, transformed, or repaired
by the generated program, producing an intact or unexpected complete phenotype.
Conversely, distinct families can converge on the same phenotype because they break
the same correctness axis. RQ2 therefore compares family-associated
distributions over complete executable phenotypes; it does not ask coordinates
to detect a family or infer uptake. The coordinate result is never itself a
poison-family label.
A.5
What the catalog enables
The catalog supports three comparisons that aggregate pass rate cannot. First,
the same stage intervention can be compared across false mechanisms: A02 and
A04 both make PersistQueue fail frequently, but one preserves recovery and
identity while breaking isolation, whereas the other produces broad failure.
Second, the same abstract loss can be compared across concrete mechanisms: B03
and B06 share first-hop origin erasure, yet B03 yields a substantially cleaner
routing-dominant behavioral signature. Third, one mechanism can be compared
across models without assuming that global model quality is the explanation.
These are behavioral signatures of controlled conditions, not claims about
hidden internal states.
The catalog also makes negative and incomplete outcomes informative. A high
intact count is consistent with the supplied theory being escaped or repaired
at the executable boundary, without identifying the source-level response. A
mixed signature says that the same prospective condition supports several
downstream outcomes. A high
NO_COMPLETE_DIAGNOSTIC_SIGNATURE
count means that the coordinate
instrument cannot always assign a complete phenotype; every terminal failure
in those cells still has a specific cause subcategory.
None of these outcomes licenses redefining a family from the generated source,
an exact vector, a hash, or a post-hoc cluster.
Appendix B
Model-Facing Prompt Traceability
The following preserved model-facing prompts establish the task obligations
measured by the case-specific Oracles. Highlight colors identify the prompt
clauses represented in the accompanying non-floating traceability tables;
ellipses occur only in abbreviated table excerpts.
B.1
Dijkstra prompt and tests
NetworkX recently added a
source_filter(origin,
u, v, edge_data)
option
to
multi_source_dijkstra
,
multi_source_dijkstra_path
, and
multi_source_dijkstra_path_length
for routing policies that
depend on the depot where a route began.
origin
remains that fixed depot
for the complete path; a
truthy result permits the adjacency
for that origin
and a
falsey result hides it.
On multigraphs,
edge_data
has the same adjacency-data
shape supplied to a callable weight. The filter must compose with
string or callable weights
, including
hidden edges, cutoff, and target or all-target
results
;
filter exceptions must propagate
unchanged
and
calls must not mutate the graph.
Combined results must return the
cheapest permitted
route
across the supplied sources while
retaining
non-exhaustive shortest-path behavior
on ordinary branching graphs. On a
directed routing graph, a permitted finite route exists from one supplied depot
to a delivery node, but the combined query reports that node as
unreachable.
Calls that
omit
source_filter
must retain NetworkX 3.6 behavior. Investigate.
Prompt Clause
Tests
NetworkX recently added a
source_filter
option to
multi_source_dijkstra
, …
_path
, and
_path_length
…
single_source_reference_route
;
two_junction_all_target_projection
;
graph_and_multigraph_projection
;
source_identity_or_graph_mutation
;
medium_branching_projection
;
callback_exception_propagation
origin
remains that fixed depot for the
complete path …
shared_junction_combined_distances
;
shared_junction_combined_paths
;
shared_junction_source_order_invariance
;
shared_junction_target_projection
;
source_switching_trap
;
two_junction_all_target_projection
;
two_junction_target_projection
;
false_success_all_target_projection
;
false_success_target_projection
;
late_all_origins_denied
A truthy result permits the adjacency …and a
falsey result hides it.
source_switching_trap
;
false_success_all_target_projection
;
false_success_target_projection
;
two_junction_all_target_projection
;
two_junction_target_projection
;
shared_junction_combined_distances
;
shared_junction_combined_paths
;
single_source_reference_route
;
late_all_origins_denied
On multigraphs,
edge_data
has the same
adjacency-data shape supplied to a callable weight.
graph_and_multigraph_projection
, specifically
_graph_classes
and
_parallel_edges
The filter must compose with string or callable
weights, including hidden edges …
weight_and_cutoff_projection
: missing/default and callable weights,
hidden edges, zero weights, and cycles; filtered negative-weight probe
…cutoff …
_cutoff_boundaries
within
weight_and_cutoff_projection
…target or all-target results …
shared_junction_target_projection
;
two_junction_all_target_projection
;
two_junction_target_projection
;
false_success_all_target_projection
;
false_success_target_projection
; path/path-length wrappers; identity
and scaling target calls
Filter exceptions must propagate unchanged.
callback_exception_propagation
, including exact filter- and
weight-callback exception identity
…calls must not mutate the graph.
source_identity_or_graph_mutation
; graph-state portions of scaling,
no-filter, validation-error, callback-error, and negative-weight probes
Combined results must return the cheapest permitted
route across the supplied sources …
competing_route_projection
; shared-junction distance/path checks;
two-junction and false-success checks;
single_source_reference_route
…retaining non-exhaustive shortest-path
behavior on ordinary branching graphs.
medium_branching_projection
On a directed routing graph, a permitted finite route
exists …but the combined query reports that node as unreachable.
single_source_reference_route
;
shared_junction_combined_distances
;
shared_junction_combined_paths
;
shared_junction_target_projection
Calls that omit
source_filter
must
retain NetworkX 3.6 behavior.
networkx_3_6_no_filter_regression
;
networkx_3_6_error_regression
; public validation and unfiltered
negative-weight checks; separate 205-test compatibility panel
Investigate.
No test
Table 16:
Dijkstra prompt-to-test traceability.
B.2
PersistQueue prompt and tests
SQLiteAckQueue.claim_batch(max_items,
raw=False)
should claim up to the requested number of ready records as one
public operation.
If the call raises before
returning a result, no record may have been consumed or left claimed.
A database error during one batch caused the call to
raise without returning records.
Afterwards,
qsize()
and the persisted ready count disagreed.
Reopening with automatic resumption disabled showed
records that were ready before the call but were unavailable to a later batch
claim.
Repair the public behavior while preserving
FIFO
and FILO order
,
duplicate payloads as separate
records
,
durable row and status truth across
reopen
,
same-database isolation between queue
instances
,
safe concurrent claimers
,
compatibility with sibling queue types
and
single-item
get
,
ack
,
nack
, and
ack_failed
operations
, and
each instance’s
qsize()
under the
baseline contract.
Prompt Clause
Tests
SQLiteAckQueue.claim_batch(max_items,
raw=False)
should claim up to the requested number of ready records as one
public operation.
_batch_claim_contract_case
;
_success_case
;
_bulk_identity_case
If the call raises before returning a result, no record
may have been consumed or left claimed.
_replacement_compensation_case
;
_retry_after_failure_case
;
_instance_lock_failure_case
;
_cross_instance_failure_case
;
_concurrency_case
A database error during one batch caused the call to
raise without returning records.
The same injected-database-failure families:
_replacement_compensation_case
;
_retry_after_failure_case
;
_instance_lock_failure_case
;
_cross_instance_failure_case
;
_concurrency_case
Afterwards,
qsize()
and the persisted ready
count disagreed.
_success_case
;
_concurrent_success_case
;
_cross_instance_failure_case
;
_concurrency_case
, especially their persisted-row and public-count
assertions
Reopening with automatic resumption disabled showed
records that were ready before the call but were unavailable to a later batch
claim.
_replacement_compensation_case
;
_retry_after_failure_case
;
_success_case
;
_bulk_identity_case
;
_cross_instance_failure_case
;
_concurrency_case
FIFO and FILO order
Every per-queue function;
_filo_sqlite_order_case
; order portions of
_success_case
and
_bulk_identity_case
duplicate payloads as separate records
_replacement_compensation_case
;
_retry_after_failure_case
;
_success_case
;
_bulk_identity_case
durable row and status truth across reopen
All
reopen portions of the atomic and concurrency functions;
_sqlite_update_persistence_case
;
_sqlite_delete_reopen_case
same-database isolation between queue instances
_concurrent_success_case
;
_instance_lock_failure_case
;
_cross_instance_failure_case
;
_concurrency_case
safe concurrent claimers
_concurrent_success_case
;
_cross_instance_failure_case
;
_concurrency_case
; relevant upstream multithreading tests
compatibility with sibling queue types
_unique_ack_deduplication_case
;
_sqlite_update_persistence_case
;
_sqlite_delete_reopen_case
;
_filo_sqlite_order_case
;
_unique_sqlite_deduplication_case
; 89 upstream regression
coordinates
single-item
get
,
ack
,
nack
, and
ack_failed
operations
_ack_state_regression_case
; preexisting single
get
in
_bulk_identity_case
; upstream ack/get/nack tests
each instance’s
qsize()
under the baseline
contract.
_success_case
;
_bulk_identity_case
; all
concurrency functions;
_ack_state_regression_case
;
_sqlite_delete_reopen_case
; upstream size tests
Table 18:
PersistQueue prompt-to-test traceability.
Appendix C
Executable Diagnostic Catalog
These are the diagnostic checks that enter the four-axis summaries. The Oracle
alone determines overall correctness; each coordinate below executes one
targeted behavior and has no verdict authority. We omit the duplicated listing
of ordinary upstream regression-test names: those tests remain in the released
machine-readable catalog, while Table
25
records their
measurement-audit disposition.
Task
Axis
Selected executable coordinates
PersistQueue
Recovery
Replacement compensation under FIFO and FILO.
Identity
Successful raw/non-raw claims under FIFO/FILO; bulk identity; batch contract; unique-queue acknowledgement.
Isolation
Cross-instance failure under FIFO/FILO; concurrent failure under FILO.
Durability
Ack-state regression; SQLite update and delete/reopen; FILO order; unique SQLite deduplication.
Dijkstra
Routing
Single-source reference; shared-junction distances, paths, source order, and target; source switching; competing routes; two-junction and false-success target/all-target checks; late-edge denial.
Weights
Graph/multigraph shapes; parallel edges; missing/callable weights; zero weights/cycles; cutoff boundaries; filtered and unfiltered negative-weight behavior.
API
Source identity and graph immutability; target-is-source; validation errors; callback exception identity.
Compatibility
Medium branching; NetworkX 3.6 weighted paths, Voronoi cells, group closeness, and Steiner tree without a filter.
Table 19:
Selected coordinates grouped by diagnostic axis.
The complete function names, source hashes, and one-sentence execution
descriptions are available in the public repository at
poisonvalleys.org
.
Appendix D
Design Coverage and Robustness Detail
D.1
Outcomes by model configuration
The table below is descriptive: conditions and poison-family mixtures differ
across rows, so it must not be read as a general model ranking.
Task
Requested model
Candidates
Success
Failure
PersistQueue
Claude Haiku 4.5
174
2 (
1.1%
)
172 (
98.9%
)
GPT-5.4 Nano, medium
322
216 (
67.1%
)
106 (
32.9%
)
GPT-5.6 Luna, medium
339
235 (
69.3%
)
104 (
30.7%
)
Dijkstra
Claude Sonnet 5, medium
331
91 (
27.5%
)
240 (
72.5%
)
GPT-5.6 Luna, medium
340
119 (
35.0%
)
221 (
65.0%
)
Qwen 3.8 Flash
127
6 (
4.7%
)
121 (
95.3%
)
Table 20:
Candidate outcomes by requested model configuration.
D.2
Response availability by stage and requested model
The UUID ledger, not the filesystem inventory, defines every scientific
denominator. Its global funnel is 1,844 planned = 1,633 code-bearing/execution-
reaching + 211 no candidate. The latter divides into 203 response-unavailable
rows and eight response-available rows with no executable candidate; 1,340 of
the 1,633 completed the authoritative Oracle. Separately, the frozen run trees
contain 1,678 response files and 1,815
attempt.json
records. Those
are file inventories, not alternate populations and not terms in the
attrition identities below.
Task
Stage
Requested model
Planned
Code
No candidate
Dijkstra
canonical
not recorded
64
0
64
Dijkstra
canonical
Claude Sonnet 5
9
9
0
Dijkstra
canonical
GPT-5.6 Luna
10
10
0
Dijkstra
canonical
Qwen 3.8 Flash
2
2
0
Dijkstra
H-only
Claude Sonnet 5
80
80
0
Dijkstra
H-only
GPT-5.6 Luna
80
80
0
Dijkstra
H-only
Qwen 3.8 Flash
29
29
0
Dijkstra
P-only
Claude Sonnet 5
76
76
0
Dijkstra
P-only
GPT-5.6 Luna
80
80
0
Dijkstra
P-only
Qwen 3.8 Flash
32
32
0
Dijkstra
H+P
Claude Sonnet 5
79
79
0
Dijkstra
H+P
GPT-5.6 Luna
80
80
0
Dijkstra
H+P
Qwen 3.8 Flash
28
28
0
Dijkstra
no-plan
Claude Sonnet 5
87
87
0
Dijkstra
no-plan
GPT-5.6 Luna
90
90
0
Dijkstra
no-plan
Qwen 3.8 Flash
36
36
0
PersistQueue
canonical
Claude Haiku 4.5
4
4
0
PersistQueue
canonical
GPT-5.4 Nano
11
10
1
PersistQueue
canonical
GPT-5.6 Luna
10
10
0
PersistQueue
H-only
Claude Haiku 4.5
55
52
3
PersistQueue
H-only
GPT-5.4 Nano
118
108
10
PersistQueue
H-only
GPT-5.6 Luna
111
110
1
PersistQueue
P-only
Claude Haiku 4.5
55
54
1
PersistQueue
P-only
GPT-5.4 Nano
116
101
15
PersistQueue
P-only
GPT-5.6 Luna
111
110
1
PersistQueue
H+P
Claude Haiku 4.5
66
64
2
PersistQueue
H+P
GPT-5.4 Nano
164
103
61
PersistQueue
H+P
GPT-5.6 Luna
161
109
52
PersistQueue source absence is concentrated in the H+P cells for GPT-5.4 Nano and GPT-5.6 Luna and is classified by provider-specific terminal subcategories. Dijkstra’s 64 no-candidate rows are legacy canonical rows without requested-model metadata; all designed poison-stage cells are code-bearing.
D.3
Leave-one-group-out sensitivity
Task
Omission
P-only
−
-
H-only RD range
H+P
−
-
P-only RD range
PersistQueue
Omit one family
+28.8 to +36.7 pp
+5.8 to +9.3 pp
PersistQueue
Omit one model
+24.6 to +40.9 pp
+1.9 to +13.2 pp
Dijkstra
Omit one family
+26.9 to +31.8 pp
-1.5 to +3.7 pp
Dijkstra
Omit one model
+22.5 to +33.2 pp
+0.8 to +2.3 pp
The primary P-only contrast remains positive under every leave-one-family and leave-one-model omission in both tasks. The smaller H+P increment is less stable, especially in Dijkstra.
D.4
Diagnostic coverage and fidelity boundary
Task
Complete diagnostic panel
Incomplete panel
No code
PersistQueue
660
175
147
Dijkstra
669
129
64
Diagnostic incompleteness is an evidence state, not a terminal failure class. Every terminal failure still has a specific cause subcategory. The mechanical source screen covers assessable code but has zero adjudicated rows, so literal-realization rates are not estimable and no fidelity bar chart is shown.
Appendix E
Statistical, Measurement, and Reproducibility Detail
E.1
Frozen inputs and regeneration contract
The binary ledger manifest is
f5dba9161a5fc4d7…
; the corrected raw-coordinate manifest is
1b9b7b8a3c0e0e4c…
. The regeneration script verifies those manifests and the exact attempt CSV hashes, reconciles 1,844 UUIDs, rejects any terminal FAIL without a specific subcategory, and writes all tables below deterministically. Family–phenotype intervals use 2,000 attempt-level bootstrap samples with seed 20260903. For stage
s
s
and common-support cell
g
g
, the balanced failure rate is
p
^
s
=
∑
g
w
g
​
p
^
s
,
g
\hat{p}_{s}=\sum_{g}w_{g}\hat{p}_{s,g}
with the same cell weights
w
g
w_{g}
in both stages; we report
p
^
P
−
p
^
H
\hat{p}_{P}-\hat{p}_{H}
and
p
^
P
/
p
^
H
\hat{p}_{P}/\hat{p}_{H}
. Primary intervals come from a dependence-group cluster bootstrap that resamples complete request UUIDs.
E.2
Provider and execution settings
Requested profile
Max tokens
Reasoning
Retries
Timeouts (request/exec.)
Settings SHA prefix
Claude Haiku 4.5
64000
none
0
600/600 s
143903211a84
Claude Sonnet 5
128000
medium
0
600/600 s
0d8cb11824ef
Claude Sonnet 5
128000
medium
0
600/600 s
d76c4a15588a
GPT-5.4 Nano
128000
medium
0
600/600 s
9459a5981a5e
GPT-5.6 Luna
128000
medium
0
600/600 s
89090236fc0b
Qwen 3.8 Flash
131072
unspecified
0
600/600 s
69c09d376571
Table 21:
Provider and execution settings.
The final analysis ledger preserves both the requested API profile and the model
identifier returned by the provider. Table
22
reports these fields separately: they are not Codex task or agent names. The
OpenAI Nano alias is returned as the dated snapshot
gpt-5.4-nano-2026-03-17
. A missing returned identifier is recorded as
NOT_OBSERVED
, never imputed from the request.
Identity field
Recorded value
Rows
Requested
gpt-5.6-luna
733
Requested
gpt-5.4-nano
409
Requested
claude-sonnet-5
331
Requested
claude-haiku-4-5-20251001
180
Requested
qwen3.8-flash
127
Requested
NOT_APPLICABLE
64
Returned
gpt-5.6-luna
679
Returned
gpt-5.4-nano-2026-03-17
327
Returned
claude-sonnet-5
331
Returned
claude-haiku-4-5-20251001
177
Returned
qwen3.8-flash
127
Returned
NOT_OBSERVED
203
Table 22:
Requested and provider-returned model identifiers.
Requests were issued on August 31, 2026 through OpenAI, Anthropic, and Alibaba/Qwen provider
adapters. Provider retries were zero. Anthropic used
standard_only
with storage disabled, OpenAI used the default service
tier with storage disabled, and Qwen sent neither a service tier nor a storage
request. Temperature was not sent for the factorial profiles. The locked
environment specifies Python
≥
\geq
3.13 and
<
3.14
<3.14
, Anthropic SDK 1.2.0,
OpenAI SDK 2.54.0, and HTTPX 0.28.1.
Record type
Files
Provider requests
1,844
Provider responses
1,678
Attempt manifests
1,815
Execution receipts
1,633
Candidate-subprocess records
1,633
Attempt logs
1,844
Run manifests / summaries / finalization records
3 / 3 / 3
Unreadable selected structured artifacts
0
Table 23:
Inventory of the four frozen run trees.
The final analysis ledger is authoritative for scientific denominators: its
1,844 rows are keyed by unique
attempt_id
, and its explicit inclusion
flags reproduce 1,641 provider-available responses, 203 unavailable responses,
1,633 code-bearing and execution-reaching attempts, and 1,340 completed
authoritative-Oracle evaluations. The identities
1,844
=
1,641
+
203
1{,}844=1{,}641+203
and
1,641
=
1,633
+
8
1{,}641=1{,}633+8
hold exactly. By contrast, the 1,678 response artifacts and
1,815 attempt records in Table
23
are filesystem
inventories. Because the surviving response and attempt-record formats do not
consistently expose the paper’s analytical
attempt_id
, those inventory
counts are not silently converted into UUID-level populations.
The attempt manifests contain 1,815 observations of
provider.request_elapsed_seconds
. Table
24
summarizes those preserved receipts. Their durations sum to approximately
218,629 seconds, or 60.73 aggregate provider-request hours. This sum is neither
experiment wall time nor CPU-hours: requests may overlap, and this receipt
population has not been substituted for the final 1,844-row analysis ledger.
Requested profile
n
n
Min. (s)
Median (s)
Max. (s)
Claude Haiku 4.5
177
29.32
33.94
87.04
Claude Sonnet 5
340
197.70
291.27
441.27
GPT-5.4 Nano
409
0.86
79.83
601.91
GPT-5.6 Luna
734
0.90
38.54
604.14
Qwen 3.8 Flash
155
49.62
237.28
482.03
Table 24:
Provider-request latency in preserved attempt receipts.
E.3
Measurement audit
Task
Validated
With limitations
Insufficient
Corrected assignment
PersistQueue
0
18
97
0
Dijkstra
10
12
5
1
Table 25:
Coordinate construct-audit disposition.
The row and reducer pipeline is deterministic and UUID-complete, but construct validity is not uniformly established. PersistQueue’s 18 historical reducer members are all
VALID_WITH_LIMITATIONS
; Dijkstra has ten validated coordinates, twelve validated with limitations, five with insufficient evidence, and one corrected routing-origin assignment. The source-pattern screen supplies a sampling frame, but its adjudicated count is 0; therefore no adoption or rejection rate is reported.
The authority boundary is fixed: selected Oracles determine binary verdicts;
only stated reducer coordinates determine complete phenotypes; descriptive
extensions cannot change either result. The current Dijkstra reducer includes
the versioned corrected routing-origin assignment. PersistQueue reduction stays
within the selected historical panel, and its descriptive extensions remain
outside that boundary.
E.4
Specific terminal failure subcategories
Task
Primary category
Specific subcategory
Count
Dijkstra
NO_CANDIDATE_ARTIFACT
MISSING_CANDIDATE_SOURCE
64
Dijkstra
ORACLE_ASSERTION_FAILURE
false_success_target_projection
1
Dijkstra
ORACLE_ASSERTION_FAILURE
medium_branching_projection
1
Dijkstra
ORACLE_ASSERTION_FAILURE
networkx_3_6_error_regression
166
Dijkstra
ORACLE_ASSERTION_FAILURE
shared_junction_combined_distances
264
Dijkstra
ORACLE_ASSERTION_FAILURE
shared_junction_combined_paths
1
Dijkstra
ORACLE_ASSERTION_FAILURE
single_source_reference_route
11
Dijkstra
ORACLE_ASSERTION_FAILURE
two_junction_all_target_projection
8
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:AttributeError
17
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:ImportError
16
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:KeyError
57
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:NameError
9
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:RecursionError
4
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:TypeError
12
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:UNAVAILABLE
1
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:ValueError
2
Dijkstra
ORACLE_EXECUTION_FAILURE
SUBPROCESS_CRASH:networkx.exception.NetworkXNoPath
9
Dijkstra
ORACLE_EXECUTION_FAILURE
TIMEOUT_600_SECONDS
3
PersistQueue
CANDIDATE_RUNTIME_EXCEPTION
CANDIDATE_RUNTIME_EXCEPTION
29
PersistQueue
EXECUTION_TIMEOUT
PUBLIC_ORACLE_SUBPROCESS_TIMEOUT
1
PersistQueue
NO_CANDIDATE_ARTIFACT
PROVIDER_CONNECTION_ERROR
2
PersistQueue
NO_CANDIDATE_ARTIFACT
PROVIDER_RATE_LIMIT_CREDIT_EXHAUSTED
105
PersistQueue
NO_CANDIDATE_ARTIFACT
PROVIDER_REQUEST_TIMEOUT
32
PersistQueue
ORACLE_CHECK_FAILURE
same_invocation::custom::replacement_compensation::fifo
215
PersistQueue
ORACLE_CHECK_FAILURE
same_invocation::custom::replacement_compensation::filo
4
PersistQueue
ORACLE_EXECUTION_EXCEPTION
PUBLIC_ORACLE_EXCEPTION
133
PersistQueue
RECONSTRUCTION_FAILURE
RECON_INVALID_CODE
7
PersistQueue
RECONSTRUCTION_FAILURE
RECON_SENTINEL_MISMATCH
1
Table 27:
Exhaustive terminal failure taxonomy.
E.5
Complete design cells
The immutable ledger contains every nonempty family
×
\times
stage
×
\times
dependency
×
\times
requested-model cell. Printing hundreds of ledger rows here
duplicates the released data without helping a reader compare conditions.
The exact table, including zero-cell complements and planned/code/failure
counts, is available as
full-design-cells.csv
in the public repository:
poisonvalleys.org
.
The stage-by-model coverage table in Appendix
D
summarizes the imbalance that motivates common-support standardization.