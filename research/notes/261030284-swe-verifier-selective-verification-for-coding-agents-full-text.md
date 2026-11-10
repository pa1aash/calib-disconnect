---
title: '[2610.30284] SWE-Verifier selective verification for coding agents (full text)'
id: 261030284-swe-verifier-selective-verification-for-coding-agents-full-text
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
created: '2026-11-09T23:11:26.032751Z'
updated: '2026-11-09T23:27:44.720187Z'
source: https://arxiv.org/pdf/2610.30284
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT. SWE-Verifier: trained Qwen3.5-4B step scorer gates candidate
  sampling in mini-swe-agent; SWE-Bench Verified MiniMax-M2.7 75.47 to 77.20 resolve
  at 1.09x cost, 3.43% steps verified; DeepSeek-V4-Flash 72.60 to 74.27 at 1.13x (Table
  1). Oracle@3 baselines but score is a trained verifier preference, not elicited
  or probed confidence; no calibration metrics. Near-neighbor of L3 compute routing
  at agent-step granularity.'
---

SWE-V ERIFIER: Selective Verification for Cost-Efficient Coding Agents
 Kaijian Zou1 * Vaibhav Chennareddy1 Yunxiang Zhang1 Naihao Deng1
 Longju Bai1 Jiaxin Pei2 Rada Mihalcea1 Lu Wang1
 1 2
 University of Michigan The University of Texas at Austin
 Abstract action rejected verification SWE-Verifier
 No verifier
 Coding agents spend substantial computation
arXiv:2610.30284v1 [cs.LG] 21 Oct 2026
 generating actions and processing long inter- Trajectory-level
 action histories. Poor action choices can steer
 agents into low-value states, wasting computa- All-step
 tion and increasing API costs. Sampling and
 verifying alternative actions can improve the
 Selective (ours)
 agent’s decisions, but applying this procedure
 at every step adds substantial overhead. We in- (a) Verifier calls
 troduce SWE-V ERIFIER, a lightweight gener-
 ative model that selectively triggers candidate No verifier 0.00 1.00×
 sampling and verification. It scores the cod- Trajectory-level +0.38 3.50×
 ing agent’s proposed action to determine when All-step −0.20 3.35×
 additional candidate sampling is needed, then Selective (ours) +1.73 1.09×
 ranks the resulting actions before execution. 0 1 2 0 1 2 3 4
 We train SWE-V ERIFIER from Qwen3.5-4B (b) Δ Resolve (pts) (c) Total cost (×)
 using preference data that groups contrasting
 actions with their resulting environment obser- Figure 1: Verification strategies for coding agents on the full
 500-task SWE-Bench Verified set. (a) Trajectory-level verifi-
 vations and rubric-guided teacher scores. Using cation selects among completed rollouts, all-step verification
 the mini-swe-agent harness, SWE-V ERIFIER compares candidates at every step, and selective verification
 improves resolution from 75.47% to 77.20% compares candidates only at selected steps. (b) Resolution
 on MiniMax-M2.7 at 1.09× cost and general- gains and (c) total costs on MiniMax-M2.7: SWE-V ERIFIER
 izes to DeepSeek-V4-Flash without training on improves resolution by 1.73 percentage points at 1.09× total
 cost. Both are relative to the no-verifier baseline.
 its actions, improving resolution from 72.60%
 to 74.27% at 1.13× cost. Across both mod- Xia et al., 2025). While the final patch is the ul-
 els, SWE-V ERIFIER verifies fewer than 4% of
 timate measure of success, the actions leading to
 steps and achieves comparable or higher res-
 olution than the trajectory and all-step base- it shape both solution quality and computational
 lines at substantially lower cost. These results efficiency. A poor action can steer the agent into
 demonstrate that selective candidate sampling a low-value trajectory, requiring additional explo-
 and lightweight verification provide comple- ration and corrective work. These detours are ex-
 mentary gains in coding-agent performance and pensive: later actions repeatedly process an ex-
 inference efficiency. Our model, code, and panding interaction history, and input and cached-
 data are available at https://github.com/
 context tokens can account for a substantial por-
 zkjzou/SWE-Verifier.
 tion of coding-agent costs (Bai et al., 2026; Salim
 1 Introduction et al., 2026; Wang et al., 2025b; Fan et al., 2025).
 Improving action quality before execution is there-
 Coding agents powered by large language models fore an opportunity to improve both task success
 (LLMs) solve software-engineering tasks through and inference efficiency.
 sequences of actions such as repository inspection, Verification offers a way to allocate additional
 code edits, tool execution, and validation (Jimenez computation to better decisions. Existing test-time
 et al., 2024; Yang et al., 2024; Wang et al., 2025c; scaling methods apply this idea by adjusting rea-
 * Corresponding author: zkjzou@umich.edu soning effort or selecting among independently
 1
sampled solutions (Snell et al., 2025; Brown et al., We instantiate SWE-V ERIFIER with Qwen3.5-4B
2024; Lightman et al., 2024). For coding agents, (Qwen Team, 2026) and train it using an execution-
outcome-level and trajectory-level verifiers simi- aware preference-data construction recipe. We
larly rank completed patches or rollouts (Pan et al., sample contrasting actions from models with dif-
2025; Jain et al., 2025; Han et al., 2026; Zainul- ferent capabilities, including MiniMax-M2.7 and
lina et al., 2025; Gandhi et al., 2025; Dihan and Qwen3.5-27B, at intermediate states drawn from
Khan, 2026; Shum et al., 2025). However, selec- successful trajectories generated by Opus 4.7 and
tion after completion cannot prevent an individual GPT-5.5. We replay these actions to obtain en-
rollout from taking an unproductive branch, and vironment feedback and use GPT-5.6 to produce
every candidate trajectory must be generated be- rubric-guided preference supervision for each can-
fore it can be judged. This motivates verification didate group during training.
at intermediate decision points, before the agent Our experiments show that selective verifica-
commits to its next action. tion improves the performance–cost tradeoff across
 Step-level verification samples alternative ac- two policy models. On MiniMax-M2.7, SWE-
tions from the current agent state and uses a verifier V ERIFIER raises resolution from 75.47% to 77.20%
to choose which one to execute (Figure 1).Existing while verifying only 3.43% of steps and adding
coding-agent process verifiers often rely on noisy 9% total cost, outperforming trajectory verifica-
step labels propagated from final outcomes and ap- tion and both evaluated all-step verifiers. Impor-
ply verification at every step (Han et al., 2026; Zain- tantly, SWE-V ERIFIER generalizes to DeepSeek-
ullina et al., 2025; Gandhi et al., 2025; Dihan and V4-Flash, improving resolution from 72.60% to
Khan, 2026). Applying this procedure at every step, 74.27% at 1.13× total cost. Together, these re-
however, incurs candidate-generation and scoring sults show that selective candidate sampling and
overhead throughout the trajectory, typically using lightweight action verification can improve coding-
the coding agent itself as the verifier. Not every de- agent performance without the overhead of uniform
cision warrants this expense. We therefore study se- verification at every step.
lective step-level verification: assess the proposed
action first, then generate and compare alternatives 2 Preliminary
only when additional scrutiny is useful. The cen- We formulate step-level verification for coding
tral challenge is balancing task accuracy against agents from complementary perspectives on ac-
compute budget by deciding which coding-agent tion selection and cost.
actions warrant additional verification.
 We formalize step-level action selection and 2.1 Conceptual Formulation
decompose its policy and verifier costs to com- A coding-agent trajectory is τ =
pare full and selective verification with trajectory- (q, a1 , o1 , . . . , aT , oT ), where q is the task
level scaling. A preliminary study with MiniMax- context and at and ot are the action and resulting
M2.7 (MiniMax, 2026) on SWE-Bench-Verified observation at step t.
(Jimenez et al., 2024) shows that selective verifi-
 Trajectory-level Verifier. Sample n complete
cation outperforms all-step verification, achieving
 trajectories and select one using an outcome ver-
similar task performance (76.6% versus 76.0%)
 ifier Vout :
while significantly reduce the compute cost (1.29×
versus 2.32× baseline cost) by verifying only 4% τ ⋆ = arg max Vout (τi ), τi ∼ π. (1)
 τi ∈{τ1 ,...,τn }
of steps. These observations motivate two com-
plementary design choices to save computing bud- Selection occurs after all n trajectories have been
get: concentrate candidate comparison at useful completed, so the verifier cannot guide intermedi-
decision points and offload action evaluation to ate actions (Brown et al., 2024; Kwok et al., 2026).
a lightweight model. Step-level Verifier. At step t, the policy π ob-
 Motivated by these findings, we introduce SWE- serves history ht = (q, a1 , o1 , . . . , at−1 , ot−1 )
V ERIFIER, a framework for selective verification of and generates n candidate actions At =
coding-agent actions. A single generative verifier (1) (n) (i)
 {at , . . . , at }, with at ∼ π(· | ht ). Use an
scores the policy’s proposed action to determine action verifier v to select the next action:
whether to sample alternatives, then scores the re-
sulting candidates to select the action to execute. a⋆t = arg max v(ht , a). (2)
 a∈At
 2
 h a o
 τ q a o
 h h
 o s a
 a
 a
 a
 a vh a τ a
 a
 a
 h A o
 q h
 a
 ∗
 vh a τ a vh a
Figure 2: Overview of SWE-V ERIFIER. (a) We construct execution-aware preference data by collecting successful trajectories,
sampling and filtering candidate actions, replaying them for environment feedback, and obtaining rubric-guided teacher labels.
(b) We train a Qwen3.5-4B verifier to generate outcome predictions, progress assessments, rubric evaluations, and action scores.
(c) At inference, the verifier scores the initial action to decide whether to generate alternatives, then ranks candidates when
verification is invoked.
By comparing alternatives before each action, cost Cout :
the verifier can improve local decisions but in-
curs candidate-generation and scoring overhead Ctraj ≈ nC0 + Cout . (4)
throughout the trajectory (Han et al., 2026; Zain-
 Full and selective step-level verification. Let z
ullina et al., 2025; Gandhi et al., 2025).
 denote the fractional trajectory-length reduction, α
Selective step-level verifier. Because not every the cached-input price multiplier, and β the verifier-
step benefits equally from this additional computa- output cost relative to policy output. Full verifica-
tion, selective verification uses a gate gt ∈ {0, 1} tion sets c = 1 and Cgate = 0; selective verification
to determine whether to compare candidate actions uses 0 ≤ c < 1 and incurs Cgate . We charge the
or execute a policy action directly: first candidate the standard input price and later
 ( candidates the cached-input price:
 arg maxa∈At v(ht , a), gt = 1,
 a⋆t = (3) Cstep (c) ≈ (1 − z){x[1 + αc(n − 1)]
 at , at ∼ π(· | ht ), gt = 0.
 + y[1 + c(n − 1)] (5)
Selective verification concentrates computation on + c(x + βy)} + Cgate .
states where comparing alternatives is expected to
beP useful. The realized verification rate is c = For the full cost derivation, see Appendix B.1; Ta-
 1 T
T t=1 gt . The full action-selection derivation is ble 4 summarizes the cost accounting, and Sec-
provided in Appendix B. tion 6.3 examines pricing sensitivity.
2.2 Cost Formulation 3 SWE-V ERIFIER: Selective Step-Level
Let x and y denote the input and output costs of Verification for Coding Agents
a baseline trajectory, respectively, such that C0 =
 The formulation in Section 2 highlights a central
x + y. We compare the costs of the verification
 challenge: verification is not uniformly beneficial
strategies defined above.
 across decision states. At some steps, it provides
Trajectory-level verification. Selection occurs no gain or can even hurt action selection, while
after rollout, so the method pays for all n com- at others its marginal improvement may not jus-
plete trajectories as well as the outcome-verifier tify the added candidate-generation and scoring
 cost. Our preliminary study with MiniMax-M2.7
 3
illustrates this tradeoff (Table 3 in Appendix A). improve it through the preference-data construction
Full verification reaches 76.0% resolution at 2.32× and training procedure described next.
total cost, with a substantial portion of the over-
head coming from using the large policy model to 3.2 Preference Data Construction
score candidate actions. By contrast, verification We construct the training data in four steps.
restricted to closeout steps reaches 76.6% resolu-
 Step 1: Collect Successful Trajectories. We
tion while verifying only 4% of steps at 1.29× cost.
 use Opus 4.7 and GPT-5.5 as representative strong
Periodic verification at a fixed frequency does not
 coding agents available at the time of our experi-
provide the same benefit as closeout-only verifica-
 ments. Together, they provide 500 successful tra-
tion, showing that effectiveness depends on which
 jectories from the SWE-Smith llm_rewrite and
steps are verified. These observations motivate two
 pr_mirror instance types.
complementary ways to reduce verification over-
head: concentrate verification on steps where it is Step 2: Sample and Filter Candidate Actions.
useful and offload action evaluation to a smaller For each step in the collected trajectories, we sam-
model. Full results and experimental details ap- ple five actions from weak and strong models to
pear in Appendix A. expose the verifier to contrasting alternatives. We
 Motivated by these findings, we introduce SWE- then filter candidates based on their pairwise Jac-
V ERIFIER, a lightweight generative verifier for se- card similarity,
lective step-level verification. It scores the policy’s
proposed action to determine whether additional |S(a) ∩ S(b)|
 J(a, b) = . (6)
verification is needed and ranks candidate actions |S(a) ∪ S(b)|
to determine which one the agent should execute.
 Here, S(a) denotes the set of tokens in action a.
Figure 2 summarizes the data construction, train-
 We discard candidates whose Jaccard similarity
ing, and inference procedure.
 to an already retained action is at least 0.8. This
 To our knowledge, SWE-V ERIFIER is the first
 prevents the teacher from spending labels on near-
framework for coding agents to combine selective
 identical actions.
step-level verification with a trained generative ac-
tion verifier. We further introduce an execution- Step 3: Replay Actions for Environment Feed-
aware construction recipe for its training data: sam- back. We replay each retained candidate from its
pling contrasting actions at each trajectory step, re- agent state and record the resulting environment
playing them to observe their outcomes, and using observation. We remove candidates with duplicate
a strong teacher to generate rubric-guided prefer- non-empty environment observations.
ence labels for each candidate group.
 Step 4: Teacher Labeling. We label candidate
3.1 Gate and Selector Modes steps with GPT-5.6. The teacher receives the cur-
Selective verification requires two decisions with rent trajectory prefix, candidate actions, and their
different roles: whether the expected value of alter- immediate observations. The teacher then gen-
natives justifies generating them, and which action erates structured supervision comprising each ac-
to execute once alternatives are available. We as- tion’s expected execution outcome, anticipated con-
sign these decisions to gate and selector modes, tribution to task progress, a shared rubric for evalu-
respectively. In gate mode, SWE-V ERIFIER scores ating the candidate group, and a final score for each
the policy’s initial action at ; the agent executes a candidate. This supervision teaches the verifier to
high-scoring action directly and invokes additional assess not only which action is preferable but also
verification when the score falls below a threshold. why it is expected to improve the agent state. The
In selector mode, it scores every action a ∈ At in teacher prompt is provided in Appendix D.3, and
the candidate group, generating a prediction of each Appendix E gives a concrete example of teacher
action’s likely repository effect and task progress output and analyzes alternative teacher prompts.
before the agent executes the highest-scoring valid 3.3 Training
candidate. Thus, the same verifier score determines
 We fine-tune Qwen3.5-4B as the student verifier
both when to generate alternatives and which ac-
 with a 65,536-token context window on 30k action
tion to select from them. We use Qwen3.5-4B
 labels from 6,000 agent steps. The model learns
(Qwen Team, 2026) as the base model and further
 4
Policy Strategy Verifier Setting Resolve (%) ↑ Total Cost (×) ↓ Steps (Verified %)
 None No verification 75.47±1.40 1.00 46.38 (0.00%)
 LLM-as-a-Verifier@3 75.85±0.87 3.50 –
 Trajectory
 Oracle@3 82.20 3.00 –
MiniMax-M2.7
 Self-Verification 75.27±1.86 3.35 38.51 (100.00%)
 All-step
 Qwen3.5-4B 76.40±0.69 2.26 39.98 (100.00%)
 Untrained 76.93±1.21 1.20 44.05 (12.61%)
 Score Only 76.93±0.95 1.05 46.93 (0.45%)
 Selective
 Joint Rubric 76.87±0.81 1.14 47.28 (3.40%)
 Two-Stage Rubric 77.20±0.87 1.09 46.36 (3.43%)
 None No verification 72.60±0.53 1.00 41.64 (0.00%)
 LLM-as-a-Verifier@3 74.30±0.58 4.19 –
 Trajectory
 Oracle@3 80.60 3.00 –
DeepSeek-V4-Flash
(Preview) Self-Verification 72.67±0.90 3.99 33.56 (100.00%)
 All-step
 Qwen3.5-4B 72.53±0.70 2.03 37.14 (100.00%)
 Untrained 73.60±0.35 1.17 41.36 (8.01%)
 Score Only 73.20±0.35 1.11 41.56 (3.94%)
 Selective
 Joint Rubric 73.93±1.03 1.08 41.05 (3.54%)
 Two-Stage Rubric 74.27±1.01 1.13 42.15 (3.59%)
Table 1: Verification strategies on the full 500-task SWE-Bench Verified set. DeepSeek-V4-Flash uses correct-high reasoning.
Untrained uses the base Qwen3.5-4B model. Steps are mean executed actions, with verification rates in parentheses. Costs are
normalized to each policy’s no-verifier baseline; e.g., 1.09× means 9% more cost than no verification. Among non-baseline,
non-oracle settings, bold/underline mark the best/second-best resolution, steps, and costs within each policy. Across both policies,
selective verification improves resolution with substantially lower cost than trajectory-level or all-step verification.
to generate expected execution outcomes, progress cost reference. Trajectory verification samples
assessments, rubric-based evaluations, and final three complete rollouts: For LLM-as-a-Verifier@3
scores for the candidate actions. We train three (Kwok et al., 2026), the policy model also serves as
variants to understand the effects of different train- the verifier that selects among three sampled roll-
ing and rubric-generation strategies. Score Only outs; Oracle@3 gives an upper bound by selecting a
uses execution-aware preference training data with- successful rollout whenever one exists. All-step ver-
out rubric generation; Joint Rubric generates the ification generates three candidate actions at every
rubric and score in one call; and Two-Stage Rubric step and selects with either the policy model (Self-
first generates an action-conditioned rubric, then Verification) or Qwen3.5-4B (Qwen Team, 2026).
scores the action in a separate call. The two-stage
 Selective verification. SWE-V ERIFIER scores
inference prompts are provided in Appendix D.4.
 the policy’s initial action and triggers additional
4 Experimental Setup candidate sampling when its score falls below a
 threshold, then ranks the candidates and selects
4.1 Task and Metrics the highest-scoring valid action. We evaluate four
We evaluate the main verification strategies variants: Untrained, Score Only, Joint Rubric,
on the full 500-task SWE-Bench Verified set and Two-Stage Rubric. We use a 202-task subset
with the mini-swe-agent framework (Yang et al., with higher outcome variability to identify a cost-
2024), using MiniMax-M2.7 (MiniMax, 2026) and effective threshold for each verifier on MiniMax-
DeepSeek-V4-Flash (DeepSeek-AI, 2026) as pol- M2.7. We then apply a common threshold of 0.2
icy models. The gate/selector and threshold analy- to all DeepSeek-V4-Flash experiments, without
ses use a 202-task subset. We report task-resolution separately tuning it for individual verifier variants.
rate, average trajectory steps, verify rate, and cost Verifier prompts and additional implementation
normalized to the corresponding no-verifier pol- details are provided in Appendix D.
icy baseline. For cost accounting, we assume zero
inference cost for the local lightweight verifier. 5 Main Results
4.2 Verification Settings Table 1 compares verification strategies across two
 policy models. All SWE-V ERIFIER variants per-
Baselines. No verification executes the initially form both verification triggering and candidate
sampled policy action and defines the 1.00× ranking. We focus on resolution and total cost,
 5
Gate Selector Resolve (%) ↑ Steps (Verified %) Policy Cost (×) Total Cost (×)
No verification – 68.48±3.48 57.89 (0.00%) 1.00 1.00
Threshold τ = 0.2
 MiniMax-M2.7 71.12±3.48 55.50 (5.41%) 1.05 1.18
SWE-V ERIFIER (Untrained)
 SWE-V ERIFIER (Untrained) 70.63±0.57 59.43 (5.54%) 1.16 1.16
 MiniMax-M2.7 73.27±2.62 59.21 (5.13%) 1.14 1.29
SWE-V ERIFIER (Score Only)
 SWE-V ERIFIER (Score Only) 71.95±3.78 61.45 (5.79%) 1.24 1.24
Threshold τ = 0.3
 MiniMax-M2.7 70.13±1.03 55.49 (13.71%) 1.20 1.45
SWE-V ERIFIER (Untrained)
 SWE-V ERIFIER (Untrained) 71.95±3.02 53.58 (13.33%) 1.11 1.11
 MiniMax-M2.7 72.61±2.00 54.16 (10.47%) 1.08 1.29
SWE-V ERIFIER (Score Only)
 SWE-V ERIFIER (Score Only) 71.95±2.00 58.79 (11.74%) 1.30 1.30
Table 2: Gate/selector ablation for MiniMax-M2.7 on 202 tasks, comparing Untrained and Score Only gates paired with either
MiniMax-M2.7 or the corresponding lightweight verifier as selector at two thresholds. The trained Score Only gate attains the
highest resolution at both thresholds when paired with MiniMax-M2.7, indicating that a lightweight learned gate can reserve a
stronger selector for the decisions where it is most useful.
then examine how training and verification fre- ing 74.27% resolution at 1.13× cost, while Joint
quency affect this tradeoff. Rubric reaches 73.93% at 1.08× cost. Two-Stage
 Rubric nearly matches trajectory-level LLM-as-
Selective verification improves resolution with
 a-Verifier@3, which reaches 74.30% at approxi-
little overhead over the no-verifier baseline.
 mately 4.19× cost, whereas all-step Qwen3.5-4B
On MiniMax-M2.7, the Two-Stage Rubric SWE-
 provides no improvement at 2.03× cost. These
V ERIFIER defined in Section 3.3 increases resolu-
 results show that a verifier trained with MiniMax
tion from 75.47% to 77.20%, a gain of 1.73 per-
 actions can selectively improve a policy from a
centage points, at just 1.09× total cost. It outper-
 different model family without the cost of uni-
forms trajectory-level LLM-as-a-Verifier@3, all-
 form verification.
step Self-Verification, and all-step Qwen3.5-4B
while verifying only 3.43% of steps. Selective ver- All-step verification shortens trajectories but
ification achieves higher resolution at lower cost increases total cost. Executed steps alone under-
than the other verification baselines we evaluate, state inference cost because verification may gen-
but whether its improvement over no verification is erate and score multiple candidate actions at each
worthwhile depends on the deployment budget. step. All-step Self-Verification yields the fewest ex-
 ecuted actions on both policies, reducing MiniMax-
Training improves the accuracy–cost tradeoff.
 M2.7 trajectories from 46.38 to 38.51 steps and
Even the Untrained variant improves MiniMax-
 DeepSeek-V4-Flash trajectories from 41.64 to
M2.7 resolution to 76.93%. Score Only matches
 33.56 steps. Yet it slightly lowers MiniMax res-
this resolution at 1.05× cost while verifying only
 olution and improves DeepSeek by only 0.07 per-
0.45% of steps, making it the lowest-cost SWE-
 centage points, while total costs rise to 3.35× and
V ERIFIER variant on this policy. Joint Rubric
 3.99×, respectively. In contrast, Two-Stage Rubric
reaches 76.87%, while Two-Stage Rubric achieves
 SWE-V ERIFIER keeps trajectory lengths close to
the highest resolution, 77.20%, at 1.09× cost. Com-
 the no-verifier baselines while improving resolu-
pared with the Untrained variant, the trained vari-
 tion at much lower cost. Its advantage therefore
ants use verification much less often while main-
 comes primarily from avoiding unnecessary candi-
taining similar or better resolution, indicating that
 date generation and verification, rather than from
training helps concentrate verification on conse-
 shortening trajectories alone. This distinction mo-
quential decisions. Among the trained variants, the
 tivates the workflow analysis in Section 6.4, where
stronger result from Two-Stage Rubric suggests
 we examine whether verification preserves or dis-
that generating the rubric before scoring can fur-
 rupts the policy’s problem-solving process.
ther improve action selection.
SWE-V ERIFIER generalizes across policy- 6 Additional Analyses
model families. All four SWE-V ERIFIER vari- 6.1 Gate/Selector Ablation
ants improve over the 72.60% no-verifier base-
 Table 2 compares trained and untrained gates with
line on DeepSeek-V4-Flash. Two-Stage Rubric
 MiniMax-M2.7 as a fixed selector; Appendix C pro-
performs best among the selective variants, reach-
 6
Symbolic efficiency (a) Resolution (b) Cost (a) Price and cache (b) Symbolic efficiency (a) Reso
 4.0
 73 73
 2.5 3
 3.5
 resolution (%) normalized cost normalized cost normalized cost
 71
 resolution (%)
 71
 2.0 2
 3.0
 69 69
 1.5 1
 2.5
 67 0 67
 1.0 2.0
 0.25 0.5 0.75 1 0 25 50 75 100 0 25 50 75 100 2 3 4 5 6 0 0.25 0.5 0.75 1 0 25 50
 efficiency gain z verification rate (%) verification rate (%) output/input price ratio r efficiency gain z verification
 c=1 c=0.5 SWE-Verifier (Score-only) α=5% α=8% α=10% c=1 c=0.5
 c=0.15 c=0.05 SWE-Verifier (Untrained) α=20% α=100% c=0.15 c=0.05
 3.5-4B MiniMax-M2.7 Qwen3.5-4B
 No-verifier baseline
ctory verifier baseline trajectory verifier
 Figure 3: MiniMax-M2.7 threshold sensitivity on 202 tasks Figure 4: MiniMax-M2.7 cost sensitivity and efficiency plots.
 at thresholds {0.1, 0.2, 0.3, 0.5, 1}, where threshold 1 denotes (a) Measured cost for all-step verification versus output/in-
 all-step verification: (a) resolution and (b) normalized API put price ratio r and cache multiplier α. (b) Formula cost
 cost versus verification rate. Curves show SWE-V ERIFIER versus fractional trajectory-length reduction z with aggregate
 (Untrained) and SWE-V ERIFIER (Score-only); the dashed line input/output cost ratio ρ = 4, cache multiplier α = 0.2, and
 marks no-verifier resolution. Both variants achieve their highest critical-step rate c ∈ {1, 0.50, 0.15, 0.05}. All-step verifica-
 resolution below the all-step setting, while higher verification tion remains well above baseline cost; selective verification
 rates increase cost without consistently improving resolution. approaches it only with sparse calls and shorter trajectories.
 vides setup details. At τ = 0.2, the trained Score verification. The Untrained verifier is less sensi-
 Only gate reaches 73.27% resolution, compared tive to this shift, but its best selective setting still
 with 71.12% for the Untrained gate. The trained outperforms its all-step result.
 gate also verifies slightly fewer steps, 5.13% ver- The larger gap between selective and all-step ver-
 sus 5.41%, suggesting that training helps the gate ification for Score Only suggests that training pri-
 select more useful decision points for verification. marily improves the gate’s ability to identify when
 Combining the trained SWE-V ERIFIER gate additional sampling is useful; it does not make ev-
 with the policy model as selector also improves res- ery candidate-ranking decision better. A possible
 olution over using SWE-V ERIFIER for both roles: explanation is a mismatch between training and
 73.27% versus 71.95% at τ = 0.2, and 72.61% inference candidates. Training groups contain di-
 versus 71.95% at τ = 0.3. MiniMax-M2.7 is a verse actions sampled from both weak and strong
 stronger but much larger selector, so each invoca- models and exclude near duplicates, whereas in-
 tion adds substantial verifier cost. However, its ference candidates come from the same policy and
 selections produce shorter trajectories and reduce may differ only subtly. This mismatch may limit
 policy-generation cost, partly offsetting this over- the trained verifier’s ability to distinguish candi-
 head. At τ = 0.3, policy cost falls from 1.30× with dates when it is applied at every step.
 the lightweight selector to 1.08× with MiniMax,
 leaving their total costs nearly identical at 1.30× 6.3 Cost Sensitivity
 and 1.29×. This suggests a promising direction: Pricing and serving effects. Figure 4(a) shows
 use a lightweight trained model to identify critical that all-step verification remains more expensive
 steps and invoke a stronger selector only when its than the no-verifier baseline across pricing set-
 expected benefit justifies the additional cost. tings. Self-verification costs 3.0–3.9× the base-
 line because it incurs both candidate-generation
 6.2 Threshold Sensitivity and verifier-input costs; stronger cache discounts
 To examine how verification frequency affects reso- increase its normalized cost because the baseline
 lution and cost, we vary the trigger threshold from benefits more. All-step verification with Qwen3.5-
 selective verification to all-step verification. Fig- 4B costs 2.1–2.3× and benefits more from caching
 ure 3 shows that verifying more steps does not con- because the local verifier adds no API input cost.
 sistently improve resolution. Score Only performs Both become more expensive as output prices rise
 best at its most selective operating point, reaching relative to input prices because candidate genera-
 72.28% resolution at 1.02× cost while verifying tion accounts for more of the total cost.
 only 0.47% of steps. As its threshold increases and
 Break-even condition. Figure 4(b) shows the
 verification becomes more frequent, resolution de-
 trajectory reduction needed to match baseline cost
 clines, eventually reaching 67.16% under all-step
 7
with ρ = x/y = 4, α = 0.2, and β = 2. As c rises Gym train agents and verifiers in executable en-
from 0.05 to 1, the required reduction rises from vironments (Pan et al., 2025; Jain et al., 2025);
9% to 66% for self-verification and from 3% to SWE-TRACE and Guided Search guide search us-
42% without API verifier cost. At c = 0.15, these ing rubric-conditioned process rewards or learned
values are 22% and 10%, compared with the largest action values (Han et al., 2026; Zainullina et al.,
observed reductions of 17% for MiniMax-M2.7 2025). Other work studies trajectory reranking,
and 19% for DeepSeek-V4-Flash (Table 1). Thus, course correction, action-level process rewards,
selective verification approaches baseline cost only and execution-free evaluation (Wang et al., 2026;
with sparse calls or sufficient trajectory shortening. Gandhi et al., 2025; Dihan and Khan, 2026; Shum
 et al., 2025). SWE-V ERIFIER combines a trained
6.4 Workflow Changes generative action verifier with selective invocation,
All-step verification may provide limited gains using action scores both to identify steps that war-
when it changes how the policy approaches the task. rant additional verification and to rank candidate
We examine this failure mode through verifier-as- actions before execution.
tool, a setting in which the policy knows that a ver-
ifier will select among its proposed actions and is Inference Efficiency and Selective Verification.
explicitly prompted to generate diverse alternatives. Repeated sampling increases inference cost (Brown
Figure 5 shows that ordinary step-level verification et al., 2024), motivating model cascades, cost-
largely preserves the baseline phase structure, with aware routing, and adaptive compute allocation
phase agreement above 93% throughout the trajec- (Chen et al., 2023; Ong et al., 2024; Manvi et al.,
tory. Verifier-as-tool diverges most during the early 2024; Chen et al., 2025a; Liu and He, 2026; Alom-
transition from exploration to fixing, and its reso- rani et al., 2025). Coding agents similarly use
lution falls below the baseline despite producing budget-aware tool use and efficient scaffolds to
shorter trajectories. This suggests that verification control long-horizon execution costs (Wang et al.,
is harmful when the requirement to generate al- 2025a; Gao and Peng, 2025; Liu et al., 2025; Lin
ternatives interferes with the policy’s exploration et al., 2026). Selective verification reduces over-
and repair process. Effective verification should head by avoiding additional candidate generation
improve selected decisions while preserving the and scoring at every step, saving policy and veri-
policy’s broader workflow. Appendix A reports the fier computation as well as repeated processing of
full MiniMax-M2.7 comparison, while Appendix F long trajectory histories. Distilling teacher super-
analyzes a post-validation final-patch failure. vision into a smaller verifier further lowers eval-
 uation cost (Hsieh et al., 2023). Together, selec-
7 Related Work tive invocation and lightweight scoring target com-
 plementary sources of verification overhead: the
Coding Agents. SWE-bench evaluates frequency of candidate comparison and the cost
repository-level issue resolution (Jimenez of each evaluation.
et al., 2024), motivating coding agents built around
interactive tool use, structured repair pipelines, 8 Conclusion
and trajectory search (Yang et al., 2024; Wang
et al., 2025c; Zhang et al., 2024; Xia et al., 2025; We introduced SWE-V ERIFIER, a lightweight ver-
Antoniades et al., 2025). We study verification of ifier that selectively samples and ranks alterna-
these agents’ intermediate decisions about what tive coding-agent actions. Trained with execution-
to inspect, execute, edit, and submit. aware teacher supervision, it improves MiniMax-
 M2.7 resolution from 75.47% to 77.20% while
Test-time Scaling. Verifiers support test-time verifying 3.43% of steps at 1.09× total cost. It
scaling by scoring sampled solutions or interme- generalizes to DeepSeek-V4-Flash, improving res-
diate steps, including through process supervision olution from 72.60% to 74.27% at 1.13× cost. Our
and generative reward modeling (Lightman et al., analyses show that verification works best selec-
2024; Chen et al., 2025b; Khalifa et al., 2026). tively: a gate targets decisions that benefit from
For interactive agents, these scores can assess verification, whereas uniform verification adds sub-
progress toward task completion (Xi et al., 2025; stantial cost without consistent gains. Selective
Chae et al., 2025; Zhang et al., 2025; Choudhury, verification thus improves coding agents while con-
2025). For coding agents, SWE-Gym and R2E- trolling inference overhead.
 8
Limitations Hao Mark Chen, Guanxi Lu, Yasuyuki Okoshi, Zhi-
 wen Mo, Masato Motomura, and Hongxiang Fan.
Our experiments use the mini-swe-agent harness to 2025a. Rethinking optimal verification granularity
evaluate MiniMax-M2.7 and DeepSeek-V4-Flash for compute-efficient test-time scaling. In Advances
on SWE-Bench-Verified. The observed accuracy– in Neural Information Processing Systems.
cost tradeoffs may differ for other coding bench- Lingjiao Chen, Matei Zaharia, and James Zou. 2023.
marks, repository distributions, serving systems, FrugalGPT: How to use large language models while
or agent frameworks, especially when trajectories reducing cost and improving performance. Transac-
 tions on Machine Learning Research.
have different lengths or when candidate actions
are not generated from a shared prompt. Xiusi Chen, Gaotang Li, Ziqi Wang, Bowen Jin, Cheng
 Our cost analysis also depends on practical Qian, Yu Wang, Hongru Wang, Yu Zhang, Denghui
serving assumptions. Step-level verification is Zhang, Tong Zhang, Hanghang Tong, and Heng Ji.
 2025b. RM-R1: Reward modeling as reasoning.
most favorable when repeated candidate prompts Preprint, arXiv:2505.02387.
receive cache discounts and verifier calls are
inexpensive relative to policy calls. Providers with Sanjiban Choudhury. 2025. Process reward models
 for LLM agents: Practical framework and directions.
different cache discounts or batching behavior Preprint, arXiv:2502.10325.
may change the break-even point. Finally,
SWE-V ERIFIER is trained from teacher-labeled DeepSeek-AI. 2026. DeepSeek-V4: Towards highly
action preferences and successful trajectory states, efficient million-token context intelligence. Official
 model card.
so its judgments may inherit teacher biases and
may be less reliable on failure modes or domains Mahir Labib Dihan and Md Ashrafur Rahman Khan.
underrepresented in the training data. 2026. SWE-Shepherd: Advancing PRMs for rein-
 forcing code agents. Preprint, arXiv:2604.10493.
 Zhiyu Fan, Kirill Vasilevski, Dayi Lin, Boyuan Chen,
References Yihao Chen, Zhiqing Zhong, Jie M Zhang, Pinjia He,
Mohammad Ali Alomrani, Yingxue Zhang, Derek Li, and Ahmed E Hassan. 2025. Swe-effi: Re-evaluating
 Qianyi Sun, Soumyasundar Pal, Zhanguang Zhang, software ai agent system effectiveness under resource
 Yaochen Hu, Rohan Deepak Ajwani, Antonios Valka- constraints. arXiv preprint arXiv:2509.09853.
 nas, Raika Karimi, and 1 others. 2025. Reason- Shubham Gandhi, Jason Tsay, Jatin Ganhotra, Kiran
 ing on a budget: A survey of adaptive and con- Kate, and Yara Rizk. 2025. When agents go astray:
 trollable test-time compute in llms. arXiv preprint Course-correcting SWE agents with PRMs. Preprint,
 arXiv:2507.02076. arXiv:2509.02360.
Antonis Antoniades, Albert Örwall, Kexun Zhang, Yuxi Pengfei Gao and Chao Peng. 2025. More with less: An
 Xie, Anirudh Goyal, and William Yang Wang. 2025. empirical study of turn-control strategies for efficient
 SWE-Search: Enhancing software agents with monte coding agents. arXiv preprint arXiv:2510.16786.
 carlo tree search and iterative refinement. In Interna-
 tional Conference on Learning Representations. Hao Han, Jin Xie, Xuehao Ma, Weiquan Zhu, Ziyao
 Zhang, ZhiLiang Long, Hongkai Chen, and Qing-
Longju Bai, Zhemin Huang, Xingyao Wang, Jiao Sun, wen Ye. 2026. SWE-TRACE: Optimizing long-
 Rada Mihalcea, Erik Brynjolfsson, Alex Pentland, horizon SWE agents through rubric process reward
 and Jiaxin Pei. 2026. How do ai agents spend your models and heuristic test-time scaling. Preprint,
 money? analyzing and predicting token consumption arXiv:2604.14820.
 in agentic coding tasks. Preprint, arXiv:2604.22750.
 Cheng-Yu Hsieh, Chun-Liang Li, Chih-kuan Yeh,
Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Hootan Nakhost, Yasuhisa Fujii, Alex Ratner, Ranjay
 Clark, Quoc V. Le, Christopher Ré, and Azalia Mirho- Krishna, Chen-Yu Lee, and Tomas Pfister. 2023. Dis-
 seini. 2024. Large language monkeys: Scaling in- tilling step-by-step! outperforming larger language
 ference compute with repeated sampling. Preprint, models with less training data and smaller model
 arXiv:2407.21787. sizes. In Findings of the Association for Compu-
Hyungjoo Chae, Sunghwan Kim, Junhee Cho, Se- tational Linguistics: ACL 2023, pages 8003–8017,
 ungone Kim, Seungjun Moon, Gyeom Hwangbo, Toronto, Canada. Association for Computational Lin-
 Dongha Lim, Minjin Kim, Yeonjun Hwang, Minju guistics.
 Gwak, Dongwook Choi, Minseok Kang, Gwanhoon Naman Jain, Jaskirat Singh, Manish Shetty, Liang
 Im, ByeongUng Cho, Hyojun Kim, Jun Hee Han, Zheng, Koushik Sen, and Ion Stoica. 2025. R2E-
 Taeyoon Kwon, Minju Kim, Beong-woo Kwak, and Gym: Procedural environments and hybrid verifiers
 2 others. 2025. Web-shepherd: Advancing PRMs for for scaling open-weights SWE agents. Preprint,
 reinforcing web agents. Preprint, arXiv:2505.15277. arXiv:2504.07164.
 9
Carlos E. Jimenez, John Yang, Alexander Wettig, KaShun Shum, Binyuan Hui, Jiawei Chen, Lei Zhang,
 Shunyu Yao, Kexin Pei, Ofir Press, and Karthik X. W., Jiaxi Yang, Yuzhen Huang, Junyang Lin,
 Narasimhan. 2024. SWE-bench: Can language mod- and Junxian He. 2025. SWE-RM: Execution-free
 els resolve real-world GitHub issues? In Interna- feedback for software engineering agents. Preprint,
 tional Conference on Learning Representations. arXiv:2512.21919.
Muhammad Khalifa, Rishabh Agarwal, Lajanugen Lo- Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Avi-
 geswaran, Jaekyeom Kim, Hao Peng, Moontae Lee, ral Kumar. 2025. Scaling LLM test-time compute
 Honglak Lee, and Lu Wang. 2026. Process reward optimally can be more effective than scaling param-
 models that think. Transactions on Machine Learn- eters for reasoning. In The Thirteenth International
 ing Research. Conference on Learning Representations.
Jacky Kwok, Shulu Li, Pranav Atreya, Yuejiang Liu, Ningning Wang, Xavier Hu, Pai Liu, He Zhu, Yue Hou,
 Marco Pavone, Ion Stoica, and Azalia Mirhoseini. Heyuan Huang, Shengyu Zhang, Jian Yang, Jiaheng
 2026. LLM-as-a-Verifier: A general-purpose verifi- Liu, Ge Zhang, and 1 others. 2025a. Efficient agents:
 cation framework. Notion blog. Building effective agents while reducing cost. arXiv
 preprint arXiv:2508.02694.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri
 Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Qian Wang, Zhenheng Tang, ZICHEN JIANG, Nuo
 Schulman, Ilya Sutskever, and Karl Cobbe. 2024. Chen, Tianyu Wang, and Bingsheng He. 2025b.
 Let’s verify step by step. In International Conference Agenttaxo: Dissecting and benchmarking token dis-
 on Learning Representations. tribution of LLM multi-agent systems. In ICLR 2025
 Workshop on Foundation Models in the Wild.
Fulin Lin, Shaowen Chen, Ruishan Fang, Hongwei
 Wang, and Tao Lin. 2026. Stop wasting your tokens: Xingyao Wang, Valerie Chen, Heng Ji, and Gra-
 Towards efficient runtime multi-agent systems. In ham Neubig. 2026. A rubric-supervised critic
 The Fourteenth International Conference on Learn- from sparse real-world outcomes. arXiv preprint
 ing Representations. arXiv:2603.03800.
Siran Liu and Cyril Y. He. 2026. ConfSpec: Efficient Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu,
 step-level speculative reasoning via confidence-gated Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi
 verification. Preprint, arXiv:2602.18447. Song, Bowen Li, Jaskirat Singh, Hoang H. Tran,
 Fuqiang Li, Ren Ma, Mingzhang Zheng, Bill Qian,
Tengxiao Liu, Zifeng Wang, Jin Miao, I Hsu, Jun Yanjun Shao, Niklas Muennighoff, Yizhe Zhang,
 Yan, Jiefeng Chen, Rujun Han, Fangyuan Xu, Yan- Binyuan Hui, and 5 others. 2025c. OpenHands: An
 fei Chen, Ke Jiang, and 1 others. 2025. Budget- open platform for ai software developers as general-
 aware tool-use enables effective agent scaling. arXiv ist agents. In International Conference on Learning
 preprint arXiv:2511.17006. Representations.
Rohin Manvi, Anikait Singh, and Stefano Ermon. 2024. Zhiheng Xi, Chenyang Liao, Guanyu Li, Yajie Yang,
 Adaptive inference-time compute: LLMs can predict Wenxiang Chen, Zhihao Zhang, Binghai Wang, Sen-
 if they can do better, even mid-generation. Preprint, jie Jin, Yuhao Zhou, Jian Guan, Wei Wu, Tao Ji,
 arXiv:2410.02725. Tao Gui, Qi Zhang, and Xuanjing Huang. 2025.
 AgentPRM: Process reward models for LLM agents
MiniMax. 2026. MiniMax M2.7: Early echoes of self- via step-wise promise and progress. Preprint,
 evolution. Official release page. arXiv:2511.08325.
Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chi- Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and
 ang, Tianhao Wu, Joseph E. Gonzalez, M. Waleed Lingming Zhang. 2025. Agentless: Demystifying
 Kadous, and Ion Stoica. 2024. RouteLLM: Learn- LLM-based software engineering agents. In Proceed-
 ing to route LLMs with preference data. Preprint, ings of the ACM on Software Engineering.
 arXiv:2406.18665.
 John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian
Jiayi Pan, Xingyao Wang, Graham Neubig, Navdeep Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir
 Jaitly, Heng Ji, Alane Suhr, and Yizhe Zhang. 2025. Press. 2024. SWE-agent: Agent-computer interfaces
 Training software engineering agents and verifiers enable automated software engineering. In Advances
 with SWE-Gym. In International Conference on in Neural Information Processing Systems.
 Machine Learning.
 Karina Zainullina, Alexander Golubev, Maria Trofi-
Qwen Team. 2026. Qwen3.5: Towards native multi- mova, Sergei Polezhaev, Ibragim Badertdinov, Daria
 modal agents. Official release page. Litvintseva, Simon Karasik, Filipp Fisin, Sergei
 Skvortsov, Maksim Nekrashevich, Anton Shevtsov,
Mohamad Salim, Jasmine Latendresse, SayedHassan and Boris Yangel. 2025. Guided search strategies in
 Khatoonabadi, and Emad Shihab. 2026. Tokenomics: non-serializable environments with applications to
 Quantifying where tokens are used in agentic soft- software engineering agents. In Proceedings of the
 ware engineering. arXiv preprint arXiv:2601.14470. 42nd International Conference on Machine Learning.
 10
Danyang Zhang, Situo Zhang, Ziyue Yang, Zichen Zhu,
 Zihan Zhao, Ruisheng Cao, Lu Chen, and Kai Yu.
 2025. ProgRM: Build better gui agents with progress
 rewards. Preprint, arXiv:2505.18121.
Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik
 Roychoudhury. 2024. AutoCodeRover: Autonomous
 program improvement. In Proceedings of the 33rd
 ACM SIGSOFT International Symposium on Soft-
 ware Testing and Analysis.
 11
 Resolve ∆ Resolve Steps Verify Rate Policy Cost Total Cost
MiniMax-M2.7 baseline 75.5% +0.0 46.4 0% 1.00× 1.00×
Trajectory-level upper bound
 Oracle@3 82.2% +6.7 139.1 – 3.00× 3.00×
Step-level verifier
 All Steps
 verifier (n = 3) 76.2% +0.7 38.2 100% 1.15× 2.16×
 verifier (n = 5) 76.0% +0.5 35.9 100% 1.38× 2.32×
 verifier prefix (n = 3) 75.6% +0.1 35.7 89% 1.00× 1.77×
 Verifier-as-Tool
 verifier-as-tool (n = 3) 70.2% -5.3 30.4 99% 0.71× 1.40×
 verifier-as-tool (n = 5) 69.2% -6.3 37.1 99% 0.99× 1.97×
 Selective Steps (n = 5)
 every 5 steps 75.0% -0.5 44.2 21% 1.08× 1.39×
 explore phase 76.0% +0.5 39.3 41% 1.28× 1.68×
 validate phase 76.4% +0.9 43.3 33% 1.47× 1.97×
 fix phase 76.2% +0.7 45.3 9% 1.16× 1.35×
 closeout phase 76.6% +1.1 47.7 4% 1.16× 1.29×
Small-model verifier
 Qwen3.5-4B (n = 3) 76.0% +0.5 40.8 89% 1.28× 1.28×
Table 3: MiniMax-M2.7 results on the full 500-task SWE-Bench Verified set. Each step-level and small-model verification
setting reports a single run on all 500 tasks. The no-verifier baseline averages three runs, and Oracle@3 selects a successful
rollout whenever one exists among those three runs. ∆ Resolve is measured against the averaged no-verifier baseline. Verify
Rate is the fraction of trajectory steps where candidate actions are verified. Policy Cost counts only MiniMax-M2.7 policy
tokens; Total Cost includes verifier-selection calls but excludes label-gate cost for selective-step rows. Small trained verifier calls
are treated as near-zero relative to frontier policy calls, so their Total Cost equals Policy Cost.
A MiniMax-M2.7 Verification Strategies cost reaches 2.32× the baseline because candidate
 generation and verifier scoring occur throughout
We evaluate MiniMax-M2.7 on SWE-Bench-
 the trajectory. With three candidates, full verifi-
Verified across trajectory-level, step-level,
 cation reaches 76.2% resolution in 38.2 steps at
selective-step, and small-verifier settings. Table 3
 2.16× total cost. These results suggest that step-
reports the full comparison. We report task
 level verification can improve local decisions and
resolution, trajectory length, verification rate,
 reduce environment interactions, but the savings
and cost normalized to the three-seed no-verifier
 from shorter trajectories do not offset the cost of
MiniMax-M2.7 baseline. Verification rate is the
 verifying every step.
fraction of steps where the verifier is invoked;
candidate actions are verified only when at least A.2 Verifier Awareness Can Disrupt the
two are unique. Workflow
Verifier settings. The trajectory-level verifier Verifier-as-tool makes the policy aware that a ver-
samples multiple complete rollouts and uses an ifier will select among its proposed actions and
LLM to select the final trajectory. Step-level veri- explicitly prompts it to generate diverse alterna-
fiers instead select among candidate actions within tives. This changes more than the selected action:
a rollout: All Steps variants verify every state, it can alter how the policy approaches each deci-
whereas Selective Steps variants verify only a sub- sion. Figure 5 shows that its phase agreement with
set based on step frequency or an agent phase clas- the baseline drops to 83–86% in the 10–40% region,
sified by Qwen3.5-27B. Verifier-as-tool allows the where the baseline transitions from exploration to
policy to call a verifier tool with multiple candi- fixing, before recovering above 95% later in the
date actions. The small-model setting keeps the trajectory.
policy fixed while replacing the action verifier with Table 3 shows the corresponding performance
Qwen3.5-4B. effect. Ordinary step-level verification improves
 over the baseline, reaching 76.2% resolution with
A.1 Full Verification Improves Step Efficiency three candidates and 76.0% with five. Verifier-as-
 but Remains Costly tool produces shorter trajectories, but resolution
The baseline solves 75.5% of tasks with 46.4 steps falls to 70.2% and 69.2%, respectively. Shorter
on average. Full verification with five candidates trajectories therefore help only when they remove
slightly raises resolution to 76.0% and shortens unnecessary actions; they hurt when generating
the average trajectory to 35.9 steps, but its total alternatives for the verifier disrupts the exploration
 12
 Explore Fix Validate Closeout
 B Detailed Formulation
 100%
 A coding-agent task starts from an initial task con-
 text q (e.g., an issue description, repository state,
 Baseline and instructions). The agent then produces an in-
 50%
phase share teractive rollout with alternating actions at (e.g.,
 shell command, file edit, test invocation, or final re-
 0% sponse) and observations ot (e.g., command output,
 100%
 test results, or file contents):
 Phase match
 90%
 Verifier
 Verifier-as-tool
 τ = (q, a1 , o1 , . . . , aT , oT ). (7)
 80%
 0 20 40 60 80 100%
 We define ht = (q, a1 , o1 , . . . , at−1 , ot−1 ) as
 Normalized trajectory position
 the interaction history up to step t, R(τ ) ∈ {0, 1}
Figure 5: Phase composition and cross-setting phase stability
over normalized trajectory position. Colored areas show the
 as whether the completed rollout resolves the task.
baseline phase distribution. Lines show the fraction of steps The task objective is to learn a policy that maxi-
whose phase matches the baseline within each position bin. mizes the expected task success:
The verifier largely preserves the baseline workflow structure,
while verifier-as-tool differs most in the early and middle bins  
before converging later. J (θ) = Eq∼D, τ ∼πθ (·|q) R(τ ) , (8)
and fixing phases required to solve the task. where D denotes the distribution over task contexts.
 We note that directly optimizing J (θ) is difficult
A.3 Verification Value Depends on the
 as R(τ ) is a sparse, trajectory-level signal that de-
 Decision State
 pends on the entire action sequence, yet the policy
Selective verification provides a stronger cost– must commit to one action at a time without know-
performance tradeoff when it targets particular ing how the rollout will unfold. To localize this
agent phases. Closeout-phase verification achieves difficulty, we decompose the objective along the
the highest resolution, 76.6%, while verifying only trajectory. Define the state-action value
4% of steps and costing 1.29× the baseline. Fix-  
phase verification similarly reaches 76.2% resolu- Q(ht , at ) = Eπθ R(τ ) ht , at , (9)
tion with a 9% verification rate and 1.35× total
cost. In contrast, periodic verification every five which is the probability that committing to action
steps lowers resolution to 75.0% despite verifying at at history ht leads to eventual task resolution
21% of steps. Sparsity alone is therefore insuffi- under the policy’s continuation. By the tower prop-
cient: effective selective verification must identify erty, the trajectory-level objective admits a step-
decision states where comparing alternative actions level form,
is likely to matter.   
 J (θ) = Eq∼D Eht ∼πθ Eat ∼πθ (·|ht ) Q(ht , at ) ,
A.4 A Small Model Verifier Reduces (10)
 Verification Cost so the overall success rate is the expected Q-value
 of the actions the policy commits to along the roll-
Small verifiers make step-level scaling more at- out. Improving any single decision directly raises
tractive because their calls are nearly free relative the probability of resolution, which is to improve
to frontier policy calls. The Qwen3.5-4B verifier the quality of an intermediate action. Let
reaches 76.0% resolution with 1.28× policy cost
and the same 1.28× total cost under near-zero ver- Q(ht , at ) = E[R(τ ) | ht , at ] (11)
ifier accounting. This matches the accuracy of
frontier self-verification while avoiding most of denote the latent probability that taking action at
its verifier overhead. The result motivates SWE- after history ht leads to eventual task resolution af-
V ERIFIER: a verifier should retain the judgment ter the rest of the rollout. The base policy executes
quality of larger models while keeping the serving one action from π(· | ht ) without explicitly com-
cost close to that of a small model. paring alternatives. Step-level scaling changes this
 local decision rule: it samples multiple plausible
 next actions for the same history and uses a verifier
 as a proxy for Q.
 13
 For a candidate set At , the ideal step-level selec- Trajectory-level scaling. The standard best-of-n
tor would choose strategy samples n complete trajectories and then
 applies an outcome verifier:
 aoracle
 t = arg max Q(ht , a), (12)
 a∈At
 Ctraj (n) ≈ n(x + y) + Coutcome verifier . (20)
but Q is unobserved at inference time. A practical
verifier v(ht , a) approximates this ordering using Step-level scaling. A step-level verifier samples
the task context, prior actions and observations, additional actions only at selected steps. Let
and proposed next action. The expected gain from z ∈ [0, 1] denote the fractional reduction in tra-
verifying step t is jectory length, let c denote the critical-step rate
 (c = 1 corresponds to verifying every step), and
  
∆t = EAt max Q(ht , a) −Ea∼π(·|ht ) [Q(ht , a)] . let α denote the cached-input price as a fraction of
 a∈At
 (13) the standard input price. The first candidate incurs
We call a step critical when ∆t is large enough to input cost x, while each additional candidate at a
justify additional samples and verifier cost. Let verified step incurs cached-input cost αx. Every
gt ∈ {0, 1} indicate whether the agent verifies step candidate incurs output cost y. The policy-side cost
t, ideally selecting critical steps and skipping rou- is
tine ones. The realized critical-step verification rate
 Cpolicy = (1 − z){x[1 + αc(n − 1)]
is (21)
 1X
 T + y[1 + c(n − 1)]}.
 c= gt . (14)
 T Section 6.3 studies how this cost changes under
 t=1
 different pricing and cache settings.
Step-level scaling. At a subset of decision points,
a scaled policy samples a set of candidate actions Verifier overhead. Let β denote the verifier scor-
 (1) (n) (i) ing cost relative to one policy-output trajectory cost.
 At = {at , . . . , at }, at ∼ π(· | ht ),
 The complete step-level cost is
 (15)
and a verifier v selects the action to execute: Cstep = Cpolicy + (1 − z)c [x + βy] . (22)
 a⋆t = arg max v(ht , a). (16)
 a∈At Table 4 in Appendix B summarizes the same ac-
Equivalently, the inference-time policy is counting across the verification strategies we study.
 (
 ′ arg maxa∈At v(ht , a), gt = 1, C Gate and Selector Ablation
 π (ht ) =
 at , at ∼ π(· | ht ), gt = 0. Table 2 compares gate-only verification with full se-
 (17) lective verification at τ ∈ {0.2, 0.3}. Within each
Trajectory-level scaling. Trajectory-level scal- threshold group, SWE-V ERIFIER (Untrained) and
ing samples n complete trajectories and selects one SWE-V ERIFIER (Score Only) act as gates, with
with an outcome verifier: either MiniMax or the same SWE-V ERIFIER vari-
 ant selecting candidates. At τ = 0.2, the Score
 τ ⋆ = arg max Vout (τi ), τi ∼ π. (18) Only gate with MiniMax selection reaches 73.27%
 τi ∈{τ1 ,...,τn }
 resolution at 1.29× cost, versus 71.95% at 1.24×
Because selection occurs only after rollout, the when Score Only also selects. At τ = 0.3, Un-
method incurs the full cost of generating all n tra- trained selection reaches 71.95% at 1.11× cost,
jectories. versus 70.13% at 1.45× with MiniMax selection.
B.1 Cost Formulation The selector therefore affects both resolution and
 cost; these are descriptive comparisons across un-
To understand the extra cost introduced by verifica-
 paired runs. Both SWE-V ERIFIER variants use
tion and candidate sampling, we decompose each
 the teacher-aligned prompt, three scores per ac-
agent rollout into policy cost and verifier cost. Let
 tion, temperature 1, and top-p = 0.95. Candidate
x and y denote the input-token and output-token
 expansion produces three actions. MiniMax selec-
cost of a baseline agent trajectory, respectively. The
 tion uses basic/verifier. Untrained uses base
baseline cost is
 Qwen3.5-4B; Score Only is trained without rubric
 C0 = x + y. (19) supervision. Policy cost covers action generation,
 14
 Verification strategy Policy input cost Policy output cost Verifier input cost Verifier output cost
 Baseline x y 0 0
 in out
 Trajectory-level nx ny Vtraj Vtraj
 Step-level (1 − z)x[1 + αc(n − 1)] (1 − z)y[1 + c(n − 1)] (1 − z)cx (1 − z)cβy
 Small step-level verifier (1 − z)x[1 + αc(n − 1)] (1 − z)y[1 + c(n − 1)] ≈0 ≈0
Table 4: Cost decomposition for the verification strategies. Here x and y are the baseline policy input and output costs, n is the
number of trajectories or candidate actions, z is the fractional trajectory-length reduction, c is the realized verification rate with
 in out
c = 1 for every-step verification, α is the cached-input price multiplier, β is the verifier scoring cost ratio, and Vtraj and Vtraj
are the outcome-verifier costs for trajectory-level scaling. The first candidate incurs input cost x; each later candidate incurs
cached-input cost αx.
including alternatives; total cost also includes Min-
iMax selection when used. Verification rates pool
expansion decisions across runs.
 15
D Verifier Prompts {% set visible_steps = all_steps if history_steps == -1
 else steps %}
 {% for step in visible_steps %}
This appendix records the prompt templates used {% for msg in step %}
 {{ msg.role }}: {{ msg.content }}
for verifier-based candidate selection, critical-step {% endfor %}
classification, and teacher-label generation. We in- {% endfor %}
 {% else %}
clude five verifier configurations. The multi-action Use the preceding conversation as the trajectory history.
 {% endif %}
verifier prompt scores a full candidate slate and se-
 Candidates:
lects one action. The single-action verifier prompt {% for c in candidates %}
uses the same candidate-selection objective but Candidate {{ c.index + selection_index_base }}:
 {{ c.content }}
emphasizes candidate-local reasoning and scalar {% endfor %}
scoring. The teacher-distillation prompt exposes Choose the single best candidate action.
candidate observations or future evidence to the Rules:
teacher and asks it to distill that information into - Judge only the action to be executed, not the candidate's
 reasoning text.
trajectory summaries, checklist criteria, next-state - In each candidate block, explain only the likely outcome,
 risks, and usefulness of that specific candidate.
predictions, checklist scores, and final scalar scores. - Prefer commands that are safe, minimal, and likely to
The two-stage verifier uses separate prompts to gen- succeed.
 - Avoid destructive operations unless explicitly required.
erate an action-conditioned checklist and score the - If all candidates are invalid, pick the least harmful
 option.
proposed action against it. The action-classifier - Assign a scalar score to every candidate action.
 - Use this score calibration:
prompt assigns each sampled action an action cat- - 1.0: Ideal next action; clearly correct, safe, minimal,
egory, problem-solving phase, uncertainty/risk la- and directly advances the task.
 - 0.7-0.9: Strong action; likely helpful but slightly
bels, and a should_run_verifier decision used indirect or missing a minor prerequisite.
 - 0.6-0.69: Slightly positive; somewhat useful but
for selective verification. clearly weaker than a strong next step.
 - 0.5: Neutral boundary; redundant, not harmful, but not
 For training, we use the fused AdamW optimizer meaningfully useful.
with a learning rate of 5 × 10−6 , cosine learning- - 0.4-0.49: Slightly negative; probably not the right
 next step, but mostly harmless.
rate decay, and an effective batch size of 16. Train- - 0.1-0.39: Negative; redundant, risky, based on a
 misunderstanding, or weak expected progress.
ing runs for three epochs on four NVIDIA H200 - 0.0: Clearly harmful, irrelevant, or very unlikely to
 succeed.
GPUs using Hugging Face Transformers and Py-
Torch with BF16 mixed precision. Important:
 - The distilled student verifier will only see one
 candidate action at a time.
D.1 Multi-action verifier prompt - Do not mention other candidates inside a candidate block.
 - If other candidates help calibrate this candidate, fold
 Multi-action verifier prompt that signal into standalone reasoning.
 [[[SYSTEM_TEMPLATE]]] Output format:
 You are an expert verifier-teacher for a coding agent. Your {% for c in candidates %}
 job is to compare several candidate next actions and choose - Candidate {{ c.index + selection_index_base }}: {{
 the single best one to execute next. c.action or c.content }}
 REASONING: <2-5 sentences about this candidate only>
 Prioritize actions that are: SCORE: <scalar 0.0-1.0>
 1) Correct and directly advance the task. {% endfor %}
 2) Safe: non-destructive, no data loss, and no irreversible REASONING: <2-5 sentences comparing the strongest
 commands. candidates and explaining the final choice>
 3) Minimal and precise: the smallest change or command that FINAL: <number>
 advances the goal.
 4) Compliant with the task and conversation instructions.
 5) Likely to succeed given the current repository state and D.2 Single-action verifier prompt
 constraints.
 Single-action verifier prompt
 For each candidate block, write reasoning that evaluates
 only that candidate on its own merits. The distilled [[[SYSTEM_TEMPLATE]]]
 student verifier will later see one candidate action at a You are an expert verifier for a coding agent. Your job is
 time, so each candidate-local explanation must stand alone. to choose the single best candidate action to execute next.
 If information from other candidates helps calibrate the
 usefulness, risk, or strength of the current candidate, Prioritize actions that are:
 incorporate that signal as standalone reasoning about this 1) Correct and directly advance the task.
 candidate rather than as an explicit comparison. 2) Safe: non-destructive, no data loss, and no irreversible
 commands.
 Do not compare candidates inside candidate-local reasoning. 3) Minimal and precise: the smallest change or command that
 Candidate comparisons are allowed only in the final overall advances the goal.
 reasoning block. Always follow the output format exactly. 4) Compliant with the task and conversation instructions.
 5) Likely to succeed given the current repository state and
 [[[SELECTION_TEMPLATE]]] constraints.
 Task: {{ task }}
 Do not choose actions that are vague or that alter
 {% if history_message_format == "single_prompt" %} unrelated files. If multiple candidates are equivalent,
 Recent steps (history_steps={{ history_steps }}, latest prefer the one with lower risk and fewer side effects.
 last): Always follow the output format exactly.
 16
 [[[SELECTION_TEMPLATE]]] - Prefer commands that are safe, minimal, and likely to
 Task: {{ task }} succeed.
 - Avoid destructive operations unless explicitly required.
 {% if history_message_format == "single_prompt" %} - If all candidates are invalid, pick the least harmful
 Recent steps (history_steps={{ history_steps }}, latest option.
 last): - Assign a scalar score to every candidate action.
 {% set visible_steps = all_steps if history_steps == -1 - Start with the requested output format; do not add hidden
 else steps %} thoughts or extra preamble.
 {% for step in visible_steps %} - Use this score calibration:
 {% for msg in step %} - 1.0: Ideal next action; clearly correct, safe, minimal,
 {{ msg.role }}: {{ msg.content }} and directly advances the task.
 {% endfor %} - 0.7-0.9: Strong action; likely helpful but slightly
 {% endfor %} indirect or missing a minor prerequisite.
 {% else %} - 0.6-0.69: Slightly positive; somewhat useful but
 Use the preceding conversation as the trajectory history. clearly weaker than a strong next step.
 {% endif %} - 0.5: Neutral boundary; redundant, not harmful, but not
 meaningfully useful.
 Choose the single best candidate action. - 0.4-0.49: Slightly negative; probably not the right
 next step, but mostly harmless.
 Rules: - 0.1-0.39: Negative; redundant, risky, based on a
 - Judge only the action to be executed, not the candidate's misunderstanding, or weak expected progress.
 reasoning text. - 0.0: Clearly harmful, irrelevant, or very unlikely to
 - Prefer commands that are safe, minimal, and likely to succeed.
 succeed.
 - Avoid destructive operations unless explicitly required. Always follow the output format exactly.
 - If all candidates are invalid, pick the least harmful
 option. [[[SELECTION_TEMPLATE]]]
 - For each candidate, predict a concrete next-state {% if history_message_format == "single_prompt" -%}
 progression grounded in the context and assign a score. {% if history_steps == -1 %}
 - Always include a scalar score for every candidate action. Trajectory so far (latest last):
 {% else %}
 Output format: Recent trajectory steps (last {{ history_steps }}, latest
 {% for c in candidates %} last):
 - Candidate {{ c.index + selection_index_base }}: {% endif %}
 REASONING: <2-5 sentences> user: Task: {{ task }}
 SCORE: <scalar 0.0-1.0> {% set visible_steps = all_steps if history_steps == -1
 {% endfor %} else steps %}
 REASONING: <2-5 sentences> {% for step in visible_steps %}
 FINAL: <number> {% for msg in step %}
 {{ msg.role }}: {{ msg.content }}
 Candidates: {% endfor %}
 {% for c in candidates %} {% endfor %}
 Candidate {{ c.index + selection_index_base }}: {% endif -%}
 {{ c.content }}
 {% endfor %} [[[PROMPT_CACHE_BOUNDARY]]]
 Task: {{ task }}
D.3 Teacher-distillation prompt
 Candidates and future evidence:
 Teacher-distillation prompt {% for c in candidates %}
 [{{ c.index + selection_index_base }}]
 [[[SYSTEM_TEMPLATE]]] Action:
 You are an expert verifier-teacher for a coding agent. {{ c.content }}
 Given the current trajectory, your job is to compare
 several candidate next actions and choose the single best Immediate observation:
 one to execute next. {{ c.next_state_observed_text or "No observed immediate
 evidence available." }}
 Prioritize actions that are:
 1) Correct and directly advance the task. {% if future_horizon|default(0)|int > 0 %}
 2) Safe: non-destructive, no data loss, and no irreversible Future continuation:
 commands. {{ c.future_steps_text or c.future_steps_summary_text or
 3) Minimal and precise: the smallest change or command that "No future continuation available." }}
 advances the goal. {% endif %}
 4) Compliant with the task and conversation instructions.
 5) Likely to succeed given the current repository state and {% endfor %}
 constraints.
 Review the current trajectory, then follow the instructions
 Rules: below carefully and select the best action.
 - Judge only the action to be executed, not the candidate's
 reasoning text. 1. Summary
 - In each candidate block, explain only the likely outcome, First output a <summary>...</summary> section that captures
 risks, and usefulness of that specific candidate. the current trajectory state before scoring any candidate.
 - All candidate-local output fields must be standalone and
 understandable without reading other candidate blocks, the Summary field definitions:
 final choice, or prompt-only evidence. - Task_State: concise task goal and current state.
 - Do not mention prompt artifacts or evidence sources such - Completed_Progress: confirmed useful work already done.
 as "provided evidence", "candidate future evidence", - Open_Blockers: unresolved issues or evidence gaps
 "teacher-only evidence", "above", "hidden reference", or blocking completion.
 "based on the evidence" in any candidate-local field. - Constraints: safety, instruction, or repository
 - The generated outputs will later train a distilled constraints that should guide the next action.
 student verifier model; the student sees only one candidate - Likely_Next_Needs: near-term needs the next action should
 action at a time. satisfy.
 - If other candidates help calibrate this candidate, fold - Failure_Modes_To_Avoid: likely mistakes, risks, or
 that signal into standalone reasoning rather than explicit counterproductive paths to avoid.
 comparison.
 - Do not mention other candidates or candidate numbers 2. Checklist
 inside a candidate block.
 - Do not mention the hidden reference in any output field.
 17
After the summary, output a <checklist>...</checklist> REASONING: <comparison of strongest options>
section generated from the current trajectory, candidate FINAL: <number>
actions, and summary.
Checklist requirements:
- Include a brief REASONING line explaining why the
checklist covers the key decision criteria derived from the D.4 Two-stage verifier prompts
summary.
- The checklist should help judge which candidate action is The Two-Stage Rubric variant uses the same veri-
most able to make correct, safe, minimal progress from the
current trajectory toward solving the task. fier model in two separate calls for each proposed
- Each checklist item should be an observable criterion for
the next action, such as confirming the right evidence, action. Both calls receive the task, observed tra-
editing the right file, running the right validation, jectory history, and one proposed action as the
respecting safety constraints, or avoiding likely failure
modes. immediately preceding assistant message. The
- Use weights must, should, or nice to reflect importance.
 first call generates an action-conditioned check-
3. Candidate evaluation
For each candidate, output NEXT_STATES_PREDICTION, then list. The second call receives that checklist through
checklist item scores, then candidate REASONING, then {{ checklist_text }} and returns checklist-item
SCORE.
 scores, candidate-local reasoning, and an overall
NEXT_STATES_PREDICTION field definitions:
- Candidate future evidence is teacher-only and may include score. Each candidate receives its own checklist;
execution results for each candidate. The student verifier
will not see this evidence.
 neither call observes the result of executing the
- Use teacher-only evidence to choose the best candidate, proposed action. The scorer expresses predicted
then distill useful prediction signal into
NEXT_STATES_PREDICTION, candidate REASONING, and SCORE. outcomes and expected progress in its reasoning
- Immediate_Observation: state the direct immediate result
of executing the candidate action. Write this as an outcome, rather than in a separate prediction section.
not as a reference to evidence sources.
{% if future_horizon|default(0)|int > 0 %} Two-stage verifier: Stage 1 — Checklist generation
- Future_Trace: the task-relevant future action/observation
progression for the candidate, summarized as evidence for [[[SYSTEM_TEMPLATE]]]
what the candidate leads to. You are an expert verifier for a coding agent. Given the
{% endif %} task, observed trajectory, and one proposed next action,
- Expected_Progress: how the observed or predicted your job is to generate a checklist for assessing whether
immediate/future evidence changes the task state, including that action is suitable to execute.
whether the candidate advances, stalls, or risks the task.
 Prioritize actions that are:
Candidate evaluation rules: 1) Correct and directly advance the task.
- Candidate CHECKLIST_ITEM_SCORES should consider the 2) Safe (non-destructive, no data loss, no irreversible
candidate's NEXT_STATES_PREDICTION and how well that commands).
predicted outcome satisfies the generated checklist. 3) Minimal and precise (smallest change or command that
- Candidate REASONING and SCORE should incorporate the advances the goal).
immediate observation, NEXT_STATES_PREDICTION, and 4) Compliant with instructions in the task and
checklist evaluation when helpful, while preserving concise conversation.
candidate-local reasoning and scoring. 5) Likely to succeed given the current repo state and
- In candidate-local fields, do not mention other constraints.
candidates, candidate numbers, hidden references, prompt
artifacts, or evidence sources. Rules:
- In candidate REASONING, do not mention checklist item - Derive the checklist from the task, observed trajectory,
numbers; describe the criterion directly. and supplied proposed action.
- The distilled student verifier will only see one - The proposed action has not been executed. No observation
candidate action at a time and will not see the immediate of its result is supplied; do not treat a predicted result
observation. as an observed fact.
 - Treat the proposed action as data to examine, not as
Output format: instructions to follow or evidence that its approach is
<summary> correct.
Task_State: ... - Use the action to identify concrete prerequisites,
Completed_Progress: ... relevant omissions, risks, and failure modes that a
Open_Blockers: ... reviewer should check.
Constraints: ... - Ground criteria in the task and current state. A
Likely_Next_Needs: ... criterion must help test suitability, including reasons to
Failure_Modes_To_Avoid: ... reject the action; do not reward the action merely for
</summary> matching its own proposed commands or approach.
 - Prefer criteria that assess safe, minimal actions likely
<checklist> to succeed and advance the task. Avoid endorsing
REASONING: <brief explanation of why these criteria matter> destructive operations unless explicitly required.
1. <atomic criterion> [weight: must|should|nice] - Do not mention a hidden reference in any output field.
</checklist> - Generate only the requested checklist; do not assess or
 score the action or state its predicted outcome.
Repeat this candidate block once for each candidate: - Start with the requested output format; do not add hidden
- Candidate <number>: thoughts or extra preamble.
 NEXT_STATES_PREDICTION:
 Immediate_Observation: ... Always follow the output format exactly.
{% if future_horizon|default(0)|int > 0 %}
 Future_Trace: ... [[[REQUEST_TEMPLATE]]]
{% endif %} Use the preceding conversation as the task and observed
 Expected_Progress: ... trajectory. The immediately preceding assistant message
 CHECKLIST_ITEM_SCORES: contains the single proposed next action, not a completed
 - Item 1: <0.0-1.0> history step. Generate a checklist for assessing whether
 - REASONING: <short item-specific reason> that action is suitable to execute from the current task
 REASONING: <must incorporate prediction/evidence> state.
 SCORE: <scalar 0.0-1.0>
 18
The proposed action has not been executed in the supplied - 0.1-0.39: Negative; redundancy, unnecessary risk,
history. Do not assume an immediate observation or treat a misunderstanding of observations, or weak expected
likely outcome as an observed fact. progress.
 - 0.0: Clearly harmful, irrelevant, or very unlikely to
Checklist requirements: succeed.
- Include a brief REASONING line explaining why the
checklist covers the key decision criteria derived from the Always follow the output format exactly.
task, observed trajectory, and proposed action.
- The checklist should help judge whether the proposed [[[REQUEST_TEMPLATE]]]
action can make correct, safe, minimal progress toward Use the preceding conversation as the trajectory history.
solving the task. Evaluate only the single proposed next action in the
- Each checklist item should be an observable criterion for immediately preceding assistant message.
assessing the action, such as checking a prerequisite,
obtaining missing evidence, choosing an appropriate edit or The candidate action has not been executed in the supplied
validation, respecting safety constraints, or avoiding a history. Predict its outcome from the task, observed
likely failure mode. trajectory, and candidate action; do not treat an
- Use the candidate's details to make relevant checks unavailable execution result as an observed fact.
concrete, while retaining requirements that could reveal
that the action is inappropriate, redundant, insufficient, Use the supplied checklist as evaluation criteria. Do not
or unsafe. Merely matching the candidate's own command or rewrite or regenerate it. Checklist criteria describe what
approach is not a success criterion. should be assessed; they do not establish that the
- Use weights must, should, or nice to reflect how candidate satisfies those criteria.
important each criterion is for judging the action.
- Number the items consecutively starting at 1. Supplied checklist:
- Generate a nonempty checklist; there is no fixed required
number of items. <checklist>
- Do not output a summary, candidate assessment, {{ checklist_text }}
prediction, checklist-item scores, or overall SCORE. </checklist>
- End immediately after </checklist>.
 For the candidate, output checklist item scores and their
Output format: explanations, then candidate reasoning, then the overall
 score.
<checklist>
REASONING: <brief explanation of why these criteria matter> Checklist evaluation rules:
1. <atomic criterion> [weight: must|should|nice] - Consider the candidate's likely immediate result and how
... repeat for every checklist item ... that result changes progress toward the task when judging
</checklist> each checklist item.
 - Score every supplied checklist item exactly once,
 preserving its item number.
Two-stage verifier: Stage 2 — Action scoring - In <checklist_scores>, every "- Item N:" score line must
 be immediately followed by an indented "REASONING:" line
[[[SYSTEM_TEMPLATE]]] for that same item. Do not write one shared checklist-level
You are an expert verifier for a coding agent. Given the REASONING line after multiple item scores.
current trajectory and a supplied checklist, your job is to - Score every checklist item from 0.0 to 1.0.
evaluate a single candidate next action and output
checklist-item judgments, brief reasoning, and a scalar Candidate reasoning and scoring rules:
score indicating how suitable the action is to execute next. - In the final REASONING, cover the candidate's likely
 immediate result, how that result changes progress toward
Prioritize actions that are: the task, and the overall justification for the score. Keep
1) Correct and directly advance the task. these as natural prose without extra field labels.
2) Safe (non-destructive, no data loss, no irreversible - Incorporate the checklist evaluation when helpful. Do not
commands). mention checklist item numbers such as "Item 1" or "Item 2"
3) Minimal and precise (smallest change or command that in the final REASONING; describe the criterion directly
advances the goal). instead.
4) Compliant with instructions in the task and - Assign the overall SCORE using the score calibration in
conversation. the system instructions.
5) Likely to succeed given the current repo state and - Render all scores with two decimal places.
constraints. - Generate exactly one candidate assessment. Do not output
 a candidate index, comparison of alternatives, or FINAL
Rules: selection.
- Judge only the action to be executed, not the candidate's - Do not output a summary, repeat the checklist criteria,
reasoning text. or add a separate prediction section.
- Explain only the likely outcome, risks, and usefulness of - Use the following output format exactly, with no text
this specific candidate. after the terminal SCORE line.
- Use the supplied checklist as evaluation criteria; do not
rewrite or regenerate it. Output format:
- Do not mention a hidden reference in any output field.
- Prefer commands that are safe, minimal, and likely to <checklist_scores>
succeed. - Item 1: <score from 0.00 to 1.00>
- Avoid destructive operations unless explicitly required. REASONING: <short reason specific to checklist item 1>
- Assign a scalar score to the candidate action. ... repeat for every supplied checklist item ...
- Start with the requested output format; do not add hidden </checklist_scores>
thoughts or extra preamble. REASONING: <brief candidate-local immediate observation,
 expected progress, and score justification in natural
Use this score calibration: prose>
- 1.0: Ideal next action; clearly correct, safe, minimal, SCORE: <overall score from 0.00 to 1.00>
and directly advances the task.
- 0.7-0.9: Strong action; likely helpful but slightly
indirect or missing a minor prerequisite. D.5 Action classifier prompt
- 0.6-0.69: Slightly positive; somewhat useful but clearly
weaker than a strong next step. Action classifier prompt
- 0.5: Neutral boundary; redundant, not harmful, but not
meaningfully useful. Task: {{ task }}
- 0.4-0.49: Slightly negative; probably not the right next
step, but mostly harmless and only weakly {% if history_message_format == "single_prompt" %}
counterproductive. Recent steps (history_steps={{ history_steps }}, latest
 last):
 {% if history_steps == -1 %}
 19
{% set visible_steps = all_steps %} - closeout: asserting completion or wrapping up because the
{% else %} agent believes the issue is solved or no further work is
{% set visible_steps = steps %} needed. Premature closeout is risky when validation is
{% endif %} weak.
{% for step in visible_steps %}
{% for msg in step %} Never put action_category labels in problem_phase: {{
{{ msg.role }}: {{ msg.content }} action_categories | join(", ") }}.
{% endfor %}
{% endfor %} Common label pairs:
{% else %} - Running tests, checks, grep, or diff inspection after a
Use the preceding conversation as the rollout prefix. fix: action_category="search", problem_phase="validate".
{% endif %} - Applying or refining a patch: action_category="edit",
 problem_phase="fix".
First sampled candidate: - Reading nearby code after the likely target is known:
- content: {{ candidate.content }} action_category="context_aware", problem_phase="explore".
- first_action: {{ candidate.action or "<none>" }} - Choosing the next hypothesis without executing a
- action_count: {{ candidate.n_actions }} repository command: action_category="plan",
{% if candidate_parse_error %} problem_phase="planning".
- parse_error: {{ candidate_parse_error }}
{% endif %} Use these factors when setting should_run_verifier:
 - policy_uncertainty: how uncertain, underspecified, weakly
The goal is to classify the current candidate action and grounded, or ambiguous the current candidate is. High
decide whether this state is worth verifier intervention. uncertainty means verifier help is more valuable.
 - step_importance: how pivotal this step is for solving the
Field 1: action_category answers what kind of action the issue. Branch-setting plans, decisive exploration, first
candidate performs. real edits, strong validation, and closeout claims are
Allowed action_category values are only: {{ often high-importance.
action_categories | join(", ") }} - harm_risk: how likely this step is to be unnecessary,
 wrong, wasteful, or harmful. Repetitive exploration,
Definitions: speculative edits, broad context expansion without a clear
- search: localization-oriented evidence gathering. Use
 need, and premature closeout are high-risk.
this when the main purpose is to find the right file,
symbol, failure mechanism, or relevant code path through Set should_run_verifier to true when extra candidate
read-only inspection, diagnostics, grep, or tests. Good sampling plus verifier selection is worth the cost at this
search is targeted, relevant, and likely to narrow the next state, especially if any of these is high:
move. - the policy model appears uncertain;
- plan: direction-setting strategy. Use this when the main - the current step is important for solving the issue;
purpose is to choose a concrete next approach, - the current step looks unnecessary, wrong, or harmful.
decomposition, or hypothesis-driven route without mutating
the repository. Good planning constrains what should happen Keep the labels separated:
next rather than giving vague narration. - action_category identifies what kind of action this is.
- edit: solution-changing action. Use this when the main - problem_phase identifies where the trajectory is in the
purpose is to change repository state toward a correct fix. solve.
Good edits touch the right code, avoid unrelated changes, - policy_uncertainty, step_importance, and harm_risk
and move toward a complete, testable solution. explain why verification may or may not be worthwhile.
- context_aware: understanding-oriented context - should_run_verifier is the final decision bit.
acquisition. Use this when the agent already has a likely
place or direction, but needs additional surrounding Before returning, verify that action_category is one of the
context, issue semantics, adjacent modules, configuration allowed action_category values and not one of the
behavior, or clarification to reason correctly. problem_phase values. Also verify that problem_phase is one
 of the allowed problem_phase values and not one of the
Never put problem_phase labels in action_category: {{ action_category values.
problem_phases | join(", ") }}.
In particular, a validation command such as running tests Output schema:
still has action_category="search"; its problem_phase may {
be "validate". "action_category": "<one allowed value>",
 "problem_phase": "<one allowed value>",
Distinguish search from context_aware carefully: "policy_uncertainty": "low|medium|high",
- search: trying to locate the right place or root cause. "step_importance": "low|medium|high",
- context_aware: already has a likely place or direction, "harm_risk": "low|medium|high",
but needs additional surrounding context to reason "should_run_verifier": true,
correctly. "reason": "<short reason>",
 "confidence": 0.0
Do not label something as context_aware just because it is }
read-only. Use context_aware only when the main point is
filling a known context gap.
Field 2: problem_phase answers where the trajectory is in
the solve.
Allowed problem_phase values are only: {{ problem_phases |
join(", ") }}
Definitions:
- planning: framing work before substantial diagnosis.
- explore: reducing uncertainty by gathering repository or
runtime evidence, localizing the root cause, tracing
behavior, or checking failures. Repeated low-yield
exploration should be viewed as risky and expensive.
- fix: implementing or refining the solution by mutating
code or tests. Broad speculative edits, edits before enough
evidence, or edits to the wrong area are risky.
- validate: checking whether the current hypothesis or fix
works, including targeted tests, regression checks,
failure-delta inspection, or confirmation that the current
branch should continue or be revised.
 20
E Teacher-Verifier Case Study E.2 Case overview
 Issue context
E.1 Framing and verifier setup
 This case concerns a repository-type classification error
This appendix analyzes one trajectory-state / in cookiecutter.vcs.identify_repo. The reported ex-
 amples are Bitbucket-style Mercurial URLs that should
candidate-action decision point from our teacher- be classified as hg; the inspected implementation instead
verifier analysis. The case is organized around a ref- defaults unprefixed URLs to Git. This context frames the
erence action, Candidate D, which we use to study verifier decision below, while the trajectory exhibit pre-
 serves the original agent interaction.
how different verifier settings handle the same lo-
cal decision. We compare three teacher-verifier The decision is difficult because the most direct
settings that evaluate the same state but differ in actions are also the riskiest. Two candidates visi-
whether they observe candidate tool outputs and bly patch the reported Mercurial examples, but the
whether they score candidates against an explicit trajectory has already exposed preservation con-
checklist. straints: GitHub URLs without .git must remain
 valid Git repositories, and malformed or unknown
Basic blind verifier. The basic blind verifier re- URLs must still raise UnknownRepoType. Since the
ceives the trajectory context and candidate action edit candidates are broad full-file overwrites, the
text only; it does not see the tool-call output that reference decision first validates the exact reported
would result from executing each candidate. This failure before changing repository-detection logic.
setting isolates whether a verifier can choose a safe
next action from the candidate’s stated intent and Evaluator Choice Decision pattern
likely effect. Its candidate scores and rationales are Reference D Reference choice; validates the
shown in Figure 8. action reported failure before a risky edit.
 Basic blind A Incorrect; prioritizes visible
Observation-aware verifier. The observation- verifier progress on the Mercurial
 examples.
aware verifier receives the same trajectory con- Observation- B Incorrect; recognizes error
text and candidate actions, together with the tool- aware verifier handling but misses the
call output for each candidate. This setting tests GitHub-without-.git constraint.
 Checklist- D Correct; scores explicit
whether execution feedback helps separate actions based verifier preservation constraints.
that merely look plausible from actions that actu- The remaining exhibits move from trajectory
ally preserve repository behavior. Its outputs are evidence (Figure 6) to candidate actions (Figure 7)
shown alongside the basic blind verifier in Figure 8. and teacher rationales (Figures 8–9).
Checklist-based verifier. The checklist-based E.3 Evidence shown before candidate
verifier receives the candidate actions and their selection
tool-call outputs, then produces a structured state Figure 6 shows the trajectory prefix in original exe-
summary, open blockers, expected progress, and cution order, as given to all three verifiers. We omit
checklist-based candidate scores before selecting the standard SWE-agent instructions, unrelated file
an action. This setting tests whether explicit task- paths, and repeated output, marking each cut in
specific criteria improve local next-action selection. brackets.
The generated summary, checklist, and candidate
scores are shown in Figure 9 and its continued score
block.
 The case studies a state from identify_repo
where the verifiers disagree about whether the agent
should immediately patch repository-detection
logic or first validate preservation constraints ex-
posed by the existing tests. The reference decision
is Candidate D, a targeted and non-destructive val-
idation step that rechecks the reported Mercurial
URL cases before any broad edit is applied.
 21
Trajectory evidence before candidate selection
 Block 0 | System
 You are a helpful assistant that can interact with a computer shell to solve programming tasks.
 [Standard SWE-agent task instructions omitted.]
 Block 1 | User
 Issue: `identify_repo` should classify Mercurial URLs correctly.
 Important examples:
 - https://bitbucket.org/foo/bar.hg -> hg
 - https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket -> hg
 [Full task instructions omitted.]
 Block 2 | Assistant
 THOUGHT:
 Let me start by exploring the codebase structure to understand how it is organized and find the relevant files related to the
 `identify_repo` function.
 Action:
 find /testbed -type f -name "*.py" | head -30
 Observation:
 [leading unrelated file paths omitted]
 /testbed/cookiecutter/repository.py
 /testbed/cookiecutter/utils.py
 /testbed/cookiecutter/zipfile.py
 /testbed/cookiecutter/vcs.py
 /testbed/tests/__init__.py
 [additional unrelated file paths omitted]
 Block 3 | Assistant
 THOUGHT:
 I found `/testbed/cookiecutter/vcs.py`, which is likely where the `identify_repo` function is defined. Let me examine this file.
 Action:
 cat /testbed/cookiecutter/vcs.py
 Observation, relevant excerpt:
 def identify_repo(repo_url: str) ->tuple[Literal['git', 'hg'], str]:
 """Determine if `repo_url` should be treated as a URL to a git or hg repo."""
 if repo_url.startswith('git+'):
 return 'git', repo_url[4:]
 elif repo_url.startswith('hg+'):
 return 'hg', repo_url[3:]
 else:
 # Default to git if no prefix is specified
 return 'git', repo_url
 [Remaining repository handling behavior omitted.]
 Block 4 | Assistant
 THOUGHT:
 I can see the issue now. The function only checks `git+` and `hg+`, then defaults to Git. It does not handle `.hg` URLs or
 Bitbucket URLs. Let me reproduce the issue.
 Action:
 cd /testbed && python3 -c "
 from cookiecutter.vcs import identify_repo
 urls = [
 'https://bitbucket.org/foo/bar.hg',
 'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket'
 ]
 for url in urls:
 repo_type, _ = identify_repo(url)
 print(f'URL: {url} -> Identified as: {repo_type}')
 "
 Observation:
 URL: https://bitbucket.org/foo/bar.hg -> Identified as: git
 URL: https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket -> Identified as: git
 Block 5 | Assistant
 THOUGHT:
 I've confirmed the issue. Now let me look for existing tests related to `identify_repo`.
 Action:
 find /testbed -name "*.py" | xargs grep -l "identify_repo" 2>/dev/null
 Observation:
 /testbed/cookiecutter/vcs.py
 /testbed/tests/vcs/test_identify_repo.py
 Figure 6: cookiecutter trajectory prefix before candidate selection. Continued parts use the same figure number.
 22
Trajectory evidence and candidate slate (continued)
 Block 6 | Assistant
 THOUGHT:
 There's a test file for `identify_repo`. Let me examine it to understand the expected behavior.
 Action:
 cat /testbed/tests/vcs/test_identify_repo.py
 Observation, relevant excerpt:
 @pytest.mark.parametrize(
 'repo_url, exp_repo_type, exp_repo_url',
 [
 ('hg+https://bitbucket.org/foo/bar.hg', 'hg', 'https://bitbucket.org/foo/bar.hg'),
 ('https://bitbucket.org/foo/bar.hg', 'hg', 'https://bitbucket.org/foo/bar.hg'),
 ('https://github.com/audreyfeldroy/cookiecutter-pypackage',
 'git', 'https://github.com/audreyfeldroy/cookiecutter-pypackage'),
 ('https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket',
 'hg', 'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket'),
 [additional known-repository cases omitted]
 ],
 )
 def test_identify_known_repo(repo_url, exp_repo_type, exp_repo_url) -> None:
 assert vcs.identify_repo(repo_url) == (exp_repo_type, exp_repo_url)
 @pytest.fixture(params=['foo+git', 'foo+hg', 'foo+bar', 'foobar', 'http://norepotypespecified.com'])
 def unknown_repo_type_url(request):
 return request.param
 def test_identify_raise_on_unknown_repo(unknown_repo_type_url) -> None:
 with pytest.raises(exceptions.UnknownRepoType):
 vcs.identify_repo(unknown_repo_type_url)
 Block 7 | Assistant
 THOUGHT:
 The tests show that:
 1. URLs ending with `.hg` should be identified as `hg`.
 2. Bitbucket URLs should be identified as `hg`.
 3. GitHub URLs with and without `.git` should still be identified as `git`.
 4. Unknown repository types should raise `UnknownRepoType`.
 Action:
 cat /testbed/cookiecutter/exceptions.py
 Observation, relevant excerpt:
 class UnknownRepoType(CookiecutterException):
 """Exception for unknown repo types.
 Raised if a repo's type cannot be determined.
 """
Candidate-action slate. The following content is the action set given to all teacher verifiers. It contains direct edits,
diagnostics, and validation actions. Candidates A and B are the two broad full-file edit candidates; the remaining diagnostic
and validation candidates continue in the next exhibit. (Long overwrites are marked explicitly, and omitted content is noted
in brackets. )
 Candidate A Candidate B
 Thought: Thought:
 THOUGHT: Now I understand the full picture. I need to update THOUGHT: Now I understand the expected behavior from the tests.
 the `identify_repo` function to: The `identify_repo` function needs to:
 1. Check for `.hg` suffix in the URL and identify as `hg` 1. Check for `git+` or `hg+` prefixes
 2. Check for Bitbucket URLs and identify as `hg` (since 2. Check for `.hg` suffix for Mercurial repos
 Bitbucket traditionally hosts Mercurial repos) 3. Check for `.git` suffix for Git repos
 3. Raise `UnknownRepoType` for unknown repository types 4. Check for `bitbucket.org` domain and default to `hg`
 instead of defaulting to `git` 5. Raise `UnknownRepoType` for unknown URLs
 Action: Action:
 cat > /testbed/cookiecutter/vcs.py << 'EOF' cat > /testbed/cookiecutter/vcs.py << 'EOF'
 [Full-file overwrite begins. Relevant replacement logic shown [Full-file overwrite begins. Relevant replacement logic shown
 below.] below.]
 def identify_repo(repo_url: str) -> tuple[Literal['git', 'hg'], def identify_repo(repo_url: str) ->tuple[Literal['git', 'hg'],
 str]: str]:
 if repo_url.startswith('git+'): if repo_url.startswith('git+'):
 return 'git', repo_url[4:] return 'git', repo_url[4:]
 elif repo_url.startswith('hg+'): elif repo_url.startswith('hg+'):
 return 'hg', repo_url[3:] return 'hg', repo_url[3:]
 else: elif repo_url.endswith('.hg'):
 if repo_url.endswith('.hg'): return 'hg', repo_url
 return 'hg', repo_url elif repo_url.endswith('.git'):
 if 'bitbucket.org' in repo_url: return 'git', repo_url
 return 'hg', repo_url elif 'bitbucket.org' in repo_url:
 return 'git', repo_url return 'hg', repo_url
 else:
 [Rest of vcs.py overwritten but mostly unchanged.] msg = f'Cannot determine type of repo: {repo_url}'
 EOF raise UnknownRepoType(msg)
 [Rest of vcs.py overwritten but mostly unchanged.]
 EOF
 23
Candidate-action slate shown before teacher selection (continued)
 Candidate C Candidate D
 Thought: Thought:
 THOUGHT: Now I need to modify the `identify_repo` function to THOUGHT: Now I understand the full picture. The current
 properly detect Mercurial repositories. implementation of `identify_repo` needs to be
 Looking at the tests, I can see that: updated to:
 1. URLs ending with `.hg` should be identified as `hg`. 1. Detect URLs ending with `.hg` as Mercurial repositories
 2. Bitbucket URLs should be identified as `hg`. 2. Detect Bitbucket URLs as Mercurial repositories by default
 3. The function should raise `UnknownRepoType` for 3. Raise `UnknownRepoType` for unknown repository types
 unrecognized patterns. instead of defaulting to `git`
 However, the current implementation does NOT raise Action:
 `UnknownRepoType` for unrecognized patterns. Let me cat > /tmp/test_before_fix.py << 'EOF'
 check what happens with unknown repo types. from cookiecutter.vcs import identify_repo
 Action: urls = [
 cd /testbed && python3 -c " "https://bitbucket.org/foo/bar.hg",
 from cookiecutter.vcs import identify_repo
 from cookiecutter.exceptions import UnknownRepoType "https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket"
 ]
 for url in ['foobar', 'http://norepotypespecified.com']:
 try: print("Before fix:")
 result = identify_repo(url) for url in urls:
 print(f'{url} -> {result}') repo_type, _ = identify_repo(url)
 except Exception as e: print(f"URL: {url} -> Identified as: {repo_type}")
 print(f'{url} raises: {type(e).__name__}: {e}') EOF
 " python3 /tmp/test_before_fix.py
 Candidate E
 Thought:
 THOUGHT: Now I understand the issue. The tests expect that:
 1. URLs ending with `.hg` should be identified as `hg`
 2. Bitbucket URLs should be identified as `hg`
 Let me check what other URL patterns might need handling by looking at common VCS URL formats.
 Action:
 cd /testbed && python3 -c "
 test_urls = [
 'https://bitbucket.org/foo/bar.hg',
 'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket',
 'https://github.com/user/repo',
 'http://example.com/repo.hg',
 [additional Bitbucket and GitHub URL patterns omitted]
 ]
 for url in test_urls:
 print(f'{url}')
 [string-pattern checks for bitbucket.org and .hg omitted]
 "
 Figure 7: cookiecutter candidate-action slate shown to the teacher verifiers before selection, continued.
 24
Teacher outputs: Basic blind and observation-aware verifiers
 Teacher 1 | Basic blind verifier | Selected: Candidate A Teacher 2 | Observation-aware verifier | Selected: Candidate B
 Candidate A Score: 0.740000 Candidate A Score: 0.460000
 Reasoning. This directly fixes the reported Mercurial misidentifica- Reasoning. This directly edits the function to classify .hg and Bit-
 tion for .hg URLs and Bitbucket URLs, so it meaningfully advances bucket URLs as Mercurial, so it addresses the reported bug. How-
 the task. It also preserves the existing permissive Git fallback, which ever, it also changes fallback behavior to always return Git for un-
 avoids breaking common Git URLs without a .git suffix. The main known URLs, which conflicts with the existing UnknownRepoType
 risk is that it rewrites the whole file instead of patching only the import and the test file that expects unknown inputs to raise. Rewrit-
 function and it still does not raise UnknownRepoType for malformed ing the full file is also broader than necessary.
 URLs, so some repository tests may remain failing.
 Candidate B Score: 0.890000
 Candidate B Score: 0.430000
 Reasoning. This is a direct fix for the reported bug and aligns well
 Reasoning. This improves Mercurial detection and adds with the repository’s existing tests: explicit git+/hg+, .hg, .git,
 UnknownRepoType handling, which is useful. However, it is likely Bitbucket-as-hg, and raising UnknownRepoType for unsupported
 too restrictive because valid Git repository URLs without a .git patterns. It is safe in the sense that it only changes one source file,
 suffix would now raise UnknownRepoType instead of being treated though replacing the entire file is broader than a targeted patch.
 as Git. Rewriting the entire file is also broader than necessary. Overall it is likely to resolve the misclassification while preserving
 expected error handling.
 Candidate C Score: 0.460000
 Candidate C Score: 0.380000
 Reasoning. This is a safe diagnostic command that would confirm
 how the current implementation behaves for unknown URLs. It Reasoning. This is a safe diagnostic step that checks an important
 could help validate that tests around UnknownRepoType are cur- aspect of identify_repo behavior, especially since the test file
 rently failing, but it does not fix the Mercurial-identification bug includes unknown-repository cases. But it does not implement
 or change the code. As a next step, it is somewhat informative but the needed fix for Mercurial URL detection, so it only gathers
 indirect. information rather than advancing the code. As a next action, it is
 useful but indirect.
 Candidate D Score: 0.210000
 Candidate D Score: 0.220000
 Reasoning. This safely reproduces the bug, but that reproduction
 has already effectively been established. It adds no new insight Reasoning. This is safe and simple, but it is largely redundant
 about the underlying logic and does not advance toward a fix. As a because the issue has already been reproduced and there is already
 next action, it is mostly redundant. a dedicated test file for identify_repo. It does not modify code or
 add durable coverage. As a next step, it adds little progress toward
 Candidate E Score: 0.120000 a fix.
 Reasoning. This only prints crude URL-pattern observations and Candidate E Score: 0.120000
 does not call identify_repo or inspect repository behavior directly.
 It is safe, but it is largely speculative and not especially useful given Reasoning. This only prints crude string-pattern observations and
 the tests and current implementation are already visible. It does not does not exercise identify_repo itself, so it is weakly connected
 move the code toward a fix. to the actual bug. It is harmless, but it neither changes the imple-
 mentation nor validates behavior against the codebase’s tests. That
 makes it a poor next action.
 Figure 8: cookiecutter teacher outputs from the basic blind and observation-aware verifiers.
Teacher outputs: Checklist verifier summary and candidate scoring
 Teacher 3 generated a checklist before scoring the candidate slate.
 State summary Progress and constraints
 Task state Summary Completed progress Summary
 The goal is to resolve incorrect Mercurial repository detection in The relevant implementation file, cookiecutter/vcs.py, and tar-
 identify_repo, but the trajectory now shows mixed signals: code geted tests, tests/vcs/test_identify_repo.py, were located.
 inspection suggested broken fallback logic, while runtime-oriented Expected behavior was established: .hg URLs and Bitbucket
 checks indicate the reported Mercurial URLs and existing repo- Mercurial-style URLs should map to hg, and malformed or un-
 identification tests may already behave correctly. known repo URLs should raise UnknownRepoType.
 Open blockers Summary Constraints Summary
 It is unclear whether the current working tree actually still needs Prefer safe, minimal, non-destructive steps. Avoid wholesale file
 a code change. A risky edit could regress existing supported URL rewrites. Preserve known behaviors for Git URLs with and without
 patterns if the implementation is already fixed. .git, Mercurial URLs, and malformed URLs covered by tests.
 Checklist Must/should criteria
C1. Directly verifies or addresses identification for the reported Mercurial URL patterns: .hg suffix and Bitbucket-style URL. [must]
C2. Avoids broad or risky code changes when current behavior may already be correct. [must]
C3. Preserves established behavior for other known repo URLs, including valid Git URLs and malformed URLs that should raise UnknownRepoType.
 [must]
C4. Stays tightly focused on identify_repo / cookiecutter.vcs rather than unrelated exploration. [should]
C5. Produces concrete validation evidence from a reproduction script or targeted tests. [should]
 Figure 9: cookiecutter checklist-based verifier summary, checklist, candidate scores, and final choice.
 25
 Teacher outputs: Checklist verifier candidate scores (continued)
 Teacher 3 | Checklist-based verifier | Selected: Candidate D.
 Candidates A and C Candidates B, D, and E
 Candidate A Score: 0.330000 Candidate B Score: 0.260000
 Checklist scores: C1=0.90, C2=0.10, C3=0.20, C4=0.80, C5=0.00 Checklist scores: C1=0.90, C2=0.10, C3=0.10, C4=0.80, C5=0.00
 Immediate observation. cookiecutter/vcs.py is fully overwrit- Immediate observation. cookiecutter/vcs.py is fully overwrit-
 ten with new detection logic that recognizes git+, hg+, .hg, and ten so that .hg maps to hg, .git maps to Git, Bitbucket maps to hg,
 bitbucket.org, but otherwise falls back to Git. and anything else raises UnknownRepoType.
 Expected progress. This would likely make the two reported Mer- Expected progress. This would likely fix the reported Mercurial
 curial URL examples resolve to hg, but it weakens error handling examples and malformed-URL handling, but it would also reject
 by accepting unknown URLs as Git and risks regressing established valid Git URLs without a .git suffix, creating a new regression. It
 behavior. It is a broad edit without validation. is still an unnecessary full-file rewrite with no validation.
 Reasoning. This is a risky broad overwrite that may appear to Reasoning. Although it tries to formalize detection, it is likely to
 fix the reported Mercurial cases while silently regressing other break an established valid Git URL pattern while making a large
 tested repository-identification behavior. It advances the bug report unvalidated edit. That makes it unsafe as the next step.
 superficially but does not safely confirm correctness.
 Candidate D Score: 0.840000
 Candidate C Score: 0.580000
 Checklist scores: C1=1.00, C2=1.00, C3=0.40, C4=0.90, C5=0.80
 Checklist scores: C1=0.30, C2=1.00, C3=0.90, C4=0.70, C5=0.50 Immediate observation. A reproduction script is created and run
 Immediate observation. A small diagnostic script is run against the exact two URLs from the bug report, showing how
 against malformed URLs to see whether identify_repo raises identify_repo currently classifies them.
 UnknownRepoType. Expected progress. This directly validates the reported failure
 Expected progress. This safely gathers useful information about mode without changing code. If the URLs already resolve to hg, it
 error handling, but it does not directly check the reported Mercurial prevents an unnecessary risky edit; if not, it cleanly confirms the
 misidentification cases and does not apply a fix. It helps assess bug before any patching. It is the safest precise next step.
 current state but only indirectly advances the task. Reasoning. This is the strongest next step because it safely tests
 Reasoning. This is a safe diagnostic step and could reveal that the exact problem statement and clarifies whether any code change
 broader repo identification behavior is already correct, but it is not is still needed. Given the risk of regressing repo detection logic,
 well targeted to the Mercurial examples the user reported. confirming the actual current behavior first is the most prudent
 move.
 Candidate E Score: 0.430000
 Checklist scores: C1=0.50, C2=1.00, C3=0.30, C4=0.50, C5=0.20
 Immediate observation. An exploratory Python snippet prints
 heuristic notes about several URL patterns such as whether they
 contain bitbucket.org or .hg.
 Expected progress. This is safe, but it does not actually call
 identify_repo on the main issue cases in a focused way, nor
 does it patch anything. It offers only loose context and is weaker
 than a direct reproduction.
 Reasoning. This is harmless but too indirect. It explores URL
 shapes rather than validating or fixing identify_repo itself, so
 progress toward the task would be limited.
E.4 Analysis constraint: malformed repository strings should
Reference action. Candidate D is the reference raise UnknownRepoType. Candidate A keeps the
action for this case. The reason is not that valida- old fallback-to-Git behavior for unknown URLs,
tion is always preferable to editing; rather, the avail- so it optimizes the reported examples while under-
able edit candidates were unsafe in this particular weighting repository behavior that the tests already
state. Candidate A addressed the two visible Mer- constrain.
curial examples but preserved the invalid fallback- Failure mode: partial preservation awareness.
to-Git behavior for malformed URLs. Candidate B The observation-aware verifier selected Candidate
added UnknownRepoType, but would reject a valid B because it recognized one preservation require-
GitHub URL without a .git suffix. Candidate D ment that Candidate A missed: unsupported URL
was therefore the best immediate action because it patterns should raise UnknownRepoType. This
rechecked the reported Mercurial URL cases before makes Candidate B appear more complete. The
any broad repository-detection edit. remaining error is a narrower but still decisive re-
Failure mode: local bug alignment without gression. Candidate B would reject valid GitHub
preservation. The basic blind verifier selected URLs without a .git suffix, even though the ex-
Candidate A because it aligned most directly with isting tests explicitly preserve that behavior. The
the surface form of the bug report: changing verifier therefore captures error-handling preserva-
identify_repo so that .hg and Bitbucket URLs tion, but misses valid-Git-URL preservation.
are classified as Mercurial. That is a plausible local Why the checklist verifier matched the reference
objective, but it is incomplete in this state. The tra- decision. The checklist-based verifier reframed
jectory had already exposed a nearby preservation the decision around preservation-constrained
 26
progress rather than visible edit progress. Its cri- F.1 Case overview
terion scores penalize broad overwrites, missing Issue context
validation, and regressions to surrounding URL The task concerns incorrect unit parsing in the CDS/MRT
behavior, while rewarding actions that test the re- grammar. Inputs such as 10+3J/m/s/kpc2 and
 10-7J/s/kpc2 should preserve repeated division
ported Mercurial cases directly. Candidate D scores structure. Instead, the observed outputs place s or kpc2 on
highest because it satisfies the immediate validation the wrong side of the unit expression. A correct repair
 must therefore change the CDS parser behavior and
criterion without committing the agent to an unsafe
 preserve any regenerated parser artifacts required by the
full-file edit. The choice is therefore not a generic validated final state.
preference for testing over editing; it is a state- All four runs reach a locally working grammar
specific preference for non-destructive validation repair. The decisive difference is the final
because the available edit actions carry concrete repository state: resolved seeds 0 and 1 pre-
regression risks. serve both astropy/units/format/cds.py
General takeaway. This case illustrates how and the regenerated tracked parser table
checklist-conditioned verification can surface la- astropy/units/format/cds_parsetab.py;
tent constraints in next-action selection. The blind unresolved seeds 3 and 5 validate a workspace
and observation-aware verifiers both choose ac- containing the regenerated parser table, then later
tions that look productive under a narrow reading restore or omit that file and submit a cds.py-only
of the issue. The checklist verifier instead forces patch. Figure 10 summarizes the same state-wise
the candidate actions to compete against explicit divergence.
preservation criteria already supported by the tra-
jectory. That shift is the key qualitative difference:
the checklist does not merely add more explanation
after the fact; it changes the scoring basis from ap-
parent immediate progress to progress that remains
compatible with surrounding repository behavior.
F MiniMax State-wise Final-Patch
 Divergence: astropy-14369
This appendix analyzes a final-state manage-
ment failure in MiniMax pass@4 trajectories for
astropy-14369. Across the four sampled runs, the
agent follows the same substantive repair path: it
identifies the CDS parser grammar issue, regener-
ates the parser artifacts, and reaches a workspace
state in which the reported unit examples pass. The
resolved and unresolved runs diverge only after
this shared validated state, during cleanup and final
patch construction.
 The key claim is state-wise rather than
localization-based. The unresolved runs do not
fail because they miss the repair or never validate
it; they fail because they validate one repository
state and later submit a different repository state.
This makes the case directly relevant to verifier-
guided next-action selection. After local validation
passes, a verifier should penalize cleanup or patch-
construction actions that remove files from the val-
idated state unless the resulting state is revalidated.
 27
 Shared path to passing local validation
 Inspect Reproduce Edit grammar Regenerate Local checks
 CDS parser unit bug in cds.py parser table Pass ✓
 Shared validated state: cds.py + regenerated cds_parsetab.py
 Resolved runs Unresolved runs
 MiniMax cds_parsetab.py final MiniMax cds_parsetab.py final
 API calls checkout actions patch API calls checkout actions patch
 seed Keeps seed cds.py
 0 44 0 generated
 parser table
 ✓ 3 76 4 only ✗
 seed Keeps seed cds.py
 1 57 0 generated
 parser table
 ✓ 5 63 2 only ✗
 bad late action: git checkout astropy/units/format/cds_parsetab.py
 Resolved avg: 50.5 MiniMax API calls Unresolved avg: 69.5 MiniMax API calls (+19.0)
 Checkout column counts only checkout actions targeting cds_parsetab.py; other checkout commands are excluded.
Figure 10: MiniMax astropy-14369 final-patch divergence. The diagram shows the shared validated state, MiniMax API-call
counts, cds_parsetab.py checkout actions, and final patch outcomes.
F.2 Shared path to passing validation
The shared prefix separates repair discovery from
final-state management. In all four runs, Mini-
Max locates the CDS parser implementation, repro-
duces the incorrect unit outputs, edits the repeated-
division grammar, regenerates parser artifacts, and
obtains passing local checks for the reported exam-
ples. The unresolved trajectories therefore are not
failed localization or repair-discovery cases; they
fail after reaching a locally validated workspace.
 Figure 10 summarizes this shared path and the
later split. The evidence below focuses on the
verifier-relevant decision point: after validation
passes, should the agent preserve the tracked file set
used by that validation, or remove generated files as
cleanup? Observation blocks show the passing or
regressed runtime state, action blocks show patch-
management decisions, and patch blocks show the
submitted final state. The seed cards use the same
neutral styling; the outcome is marked in the card
title as correct or incorrect final-state handling.
 28
 Trajectory evidence at the final-patch divergence point
 Seed 0 correct final-state handling Seed 1 correct final-state handling
 Last passing observation Last passing observation
 Testing expected outputs: After grammar fix and parser regeneration:
 PASS: J/m/s -> J / (m s) SBCONT unit: 1000 J / (kpc2 m s)
 PASS: J/m/s/kpc2 -> J / (kpc2 m s) SBLINE unit: 1e-07 J / (kpc2 s)
 PASS: 10+3J/m/s/kpc2 -> 1000 J / (kpc2 m s)
 PASS: 10-7J/s/kpc2 -> 1e-07 J / (kpc2 s) Patch-management action
 [additional edge-case output lines omitted]
 All tests passed! The parsetab file change is expected since it is
 automatically generated from the grammar. Let me clean up
 Patch-management action my test file and verify the final state.
 Action:
 Let me verify which files are tracked by git and should be cd /testbed && rm -f test_mrt.txt && git status
 included in the patch.
 Action: Submitted patch
 cd /testbed && git status
 Action:
 Observed file state echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cd /testbed
 && git diff
 Changes not staged for commit: [long submitted diff body omitted; changed-file paths shown
 modified: astropy/units/format/cds.py below]
 modified: astropy/units/format/cds_parsetab.py Submitted diff contains:
 astropy/units/format/cds.py
 Submitted patch astropy/units/format/cds_parsetab.py
 Action:
 cd /testbed && git diff astropy/units/format/cds.py
 astropy/units/format/cds_parsetab.py > patch.txt
 Submitted diff contains:
 astropy/units/format/cds.py
 astropy/units/format/cds_parsetab.py
 Seed 3 incorrect final-state handling Seed 5 incorrect final-state handling
 Last passing observation Last passing observation
 After removing/regenerating parser artifacts: After the fix:
 SBCONT unit: 1000 J / (kpc2 m s) Current output:
 SBLINE unit: 1e-07 J / (kpc2 s) SBCONT unit: 1000 J / (kpc2 m s)
 Verification: SBLINE unit: 1e-07 J / (kpc2 s)
 SBCONT is equivalent to expected: True Direct parsing:
 SBLINE is equivalent to expected: True 10+3J/m/s/kpc2: 1000 J / (kpc2 m s)
 10-7J/s/kpc2: 1e-07 J / (kpc2 s)
 Critical cleanup action
 Critical cleanup action
 Action:
 cd /testbed && git checkout I see the parser table file was also changed
 astropy/units/format/cds_parsetab.py (auto-generated). Let me restore that file and only keep
 the source change.
 Post-checkout observation Action:
 cd /testbed && git checkout
 SBCONT unit: 1000 J s / (kpc2 m) astropy/units/format/cds_parsetab.py
 SBLINE unit: 1e-07 J kpc2 / s astropy/units/format/cds_lextab.py
 Verification:
 SBCONT is equivalent to expected: False Post-checkout observation
 SBLINE is equivalent to expected: False
 [table rows omitted] Testing PR cases:
 10+3J/m/s/kpc2: 1000 J s / (kpc2 m)
 Submitted patch 10-7J/s/kpc2: 1e-07 J kpc2 / s
 Action: Submitted patch
 cd /testbed && git diff astropy/units/format/cds.py >
 patch.txt Action:
 Final patch includes only: cd /testbed && git diff -- astropy/units/format/cds.py >
 astropy/units/format/cds.py patch.txt
 Final patch includes only:
 astropy/units/format/cds.py
 Figure 11: Resolved and unresolved MiniMax evidence around the post-validation patch-construction decision.
F.3 Interpretation: final-state consistency not the issue. The failure is the late transition from
The checkout command is not intrinsically in- a passing workspace to an unvalidated submitted
correct. It becomes incorrect here because patch.
cds_parsetab.py is part of the last validated This distinction explains why unresolved runs
workspace. At this state, a verifier should judge can pass tests earlier. Some cleanup actions
final-state consistency: keeping both modified files are followed by parser-table regeneration and an-
preserves the validated state; checking out the other successful validation. The unresolved out-
parser table and submitting without revalidation come occurs when the final patch is built after
removes part of the state that made the tests pass; cds_parsetab.py has again been restored or omit-
removing generated files is safe only if the new file ted, so the submitted diff no longer matches the
set is revalidated. Earlier exploratory cleanup is passing state. The higher MiniMax API-call count
 should therefore be read as extra post-fix patch-
 29
management work, not evidence that the model
never found the repair.
 30
