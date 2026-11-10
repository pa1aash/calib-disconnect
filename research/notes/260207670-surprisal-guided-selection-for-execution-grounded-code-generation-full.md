---
title: '[2602.07670] Surprisal-guided selection for execution-grounded code generation
  (full text)'
id: 260207670-surprisal-guided-selection-for-execution-grounded-code-generation-full
tags:
- code-llm-confidence-positioning-d82d00
- related
created: '2026-11-09T23:11:30.390167Z'
updated: '2026-11-09T23:27:44.735527Z'
source: https://arxiv.org/pdf/2602.07670
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT. KernelBench GPU kernels with GPT-OSS-120B: highest-surprisal
  correct sample 80% vs most-confident 50%; Best-of-N 90% at K=64; TTT 30.6%. Execution-grounded
  selection but not code-correctness calibration. Related-only to L3.'
---

Surprisal-Guided Selection: Compute-Optimal Test-Time Strategies
 for Execution-Grounded Code Generation
 Jarrod Barnes 1
 Abstract
 Test-time training (TTT) adapts language mod-
arXiv:2602.07670v1 [cs.LG] 7 Feb 2026
 els through gradient-based updates at inference.
 But is adaptation the right strategy? We study
 compute-optimal test-time strategies for verifiable
 execution-grounded (VEG) tasks, domains like
 GPU kernel optimization where a deterministic
 evaluator provides dense, continuous reward sig-
 nals.
 Using KernelBench as our testbed and a 120B-
 parameter model (GPT-OSS-120B with LoRA
 adaptation), we find that search outperforms
 minimal adaptation (1-5 gradient steps): Best- Figure 1. Test-time strategy comparison. Best-of-N scaling
 of-N sampling achieves 90% task success (18/20 (gray) saturates at K = 16. At K = 64, TTT (31%, red) is
 tasks) at K = 64 across the full KernelBench L1 2× worse than random selection (59%); surprisal-guided (blue)
 eval set while TTT’s best checkpoint reaches only matches oracle. The +30% bracket: confidence (50%) vs. surprisal
 (80%).
 30.6% (3-seed mean), with TTT’s “equivalent K”
 falling below 1, worse than single-sample infer-
 ence. The failure mode is over-sharpening: gra-
 1. Introduction
 dient updates collapse diversity toward mediocre
 solutions rather than discovering optimal ones. This paper studies compute-optimal test-time strategies for
 verifiable execution-grounded (VEG) tasks, domains where
 Our main contribution is surprisal-guided se- a deterministic evaluator provides ground-truth feedback on
 lection: selecting the highest-surprisal (lowest- model outputs. GPU kernel optimization exemplifies VEG:
 confidence) correct sample yields 80% success KernelBench (Ouyang et al., 2025) evaluates 250 PyTorch
 vs. 50% for most-confident selection, a 30% im- ML workloads on both functional correctness and runtime
 provement. Extending to surprisal-guided-top3 speedup, with the CUDA compiler and hardware providing
 matches oracle performance at 100%. This zero- an unambiguous, continuous reward signal. The defining
 cost strategy, validated through length-controlled characteristic is that the evaluator provides ground-truth
 analysis, recovers oracle performance. feedback; no human labeler or AI teacher is needed to judge
 output quality.
 For dense-reward VEG tasks, compute should
 be allocated to sample diversity and intelligent Why VEG tasks are the ideal testbed. Unlike binary
 selection rather than gradient adaptation. The pass/fail benchmarks, KernelBench provides continuous
 surprisal-guided selection principle may general- speedup signals (0x to 10x+). This density enables us to
 ize to other execution-grounded domains where detect subtle performance regressions during adaptation that
 optimal solutions occupy the distribution tail. binary rewards would mask. When TTT over-sharpens, we
 observe the decline in a continuous metric; papers with
 sparse rewards may miss this entirely.
 1
 Arc Intelligence. Correspondence to: Jarrod Barnes <jar-
 rod@arc.computer>. Recent work on test-time training (TTT) has shown im-
 pressive results through extended gradient-based adaptation.
 Preprint. February 10, 2026. TTT-Discover (Yuksekgonul et al., 2026) reports costs of
 1
 Surprisal-Guided Selection
“a few hundred dollars per problem” using ∼50 adaptation lies in the distribution tail; gradient updates collapse
steps on discovery tasks. This raises a fundamental question: toward the mode, missing the tail entirely.
is adaptation the right strategy for dense-reward VEG
tasks, or does simple search suffice? For execution-grounded domains with dense rewards, com-
We answer this question through controlled experiments pute should be allocated to sample diversity and intelligent
comparing Best-of-N sampling against batch test-time train- selection rather than gradient adaptation. The surprisal-
ing under matched compute budgets. Using GPT-OSS-120B guided selection principle (that the model’s best solutions
(a 120B-parameter frontier model) with LoRA adaptation, occupy high-surprisal regions) may generalize to other VEG
we evaluate all 20 KernelBench L1 eval tasks. The results domains where rare, high-quality solutions exist in low-
are decisive. Best-of-N at K = 64 achieves 90% task success probability regions of the model’s distribution.
(18/20 tasks, finding at least one fast correct kernel per task)
while TTT’s best checkpoint (Best-of-Adaptation) reaches 2. Related Work
only 30.6% (3-seed mean). Computing TTT’s “equivalent
K” (the Best-of-N budget needed to match TTT perfor- Test-Time Training vs. Search. TTT-Discover (Yuksek-
mance) yields K < 1, meaning TTT underperforms single- gonul et al., 2026) demonstrates impressive results using
sample inference (K = 1). ∼50 adaptation steps on discovery tasks, reporting costs
 of “a few hundred dollars per problem.” We find different
The failure mode is over-sharpening: gradient updates col- dynamics for dense-reward VEG tasks: search outperforms
lapse the policy toward mediocre solutions that happened 1-5 step adaptation, with TTT’s best checkpoint underper-
to succeed early, destroying the diversity needed to find forming even random sampling. The difference likely stems
optimal kernels in the distribution tail. Ji et al. (Ji et al., from reward density: TTT-Discover targets sparse-reward
2026) predict that RL gains arise from distribution sharpen- scientific discovery where extended exploration may shift
ing rather than discovering new strategies; our failure mode the distribution. Kernel optimization has dense rewards;
confirms this. optimal solutions already exist in the base distribution’s tail
Our main contribution is surprisal-guided selection. (see Section 5.6 for detailed comparison).
Probing the relationship between model confidence (log- Distribution Sharpening and Over-Fitting. Scalable
probability) and kernel quality reveals a surprising inverse Power Sampling (Ji et al., 2026) argues that RL gains arise
correlation: the model is least confident about its best so- from distribution sharpening rather than discovering qualita-
lutions. We operationalize this as surprisal-guided selec- tively new strategies. Our TTT failure mode provides em-
tion: selecting the highest-surprisal (lowest log-probability) pirical evidence: gradient updates concentrate probability
correct sample. This achieves 80% success (fast and cor- on early successes (typically mediocre solutions), collaps-
rect) versus 50% for confidence-guided selection, a 30% ing diversity. “Towards Execution-Grounded Automated
improvement with zero additional compute. Extending to AI Research” (Si et al., 2026) notes that RL from execu-
surprisal-guided-top3 (evaluating the 3 highest-surprisal tion rewards can collapse to narrow ideas, exactly the over-
correct samples and selecting the fastest) matches oracle sharpening we observe. Our results extend this analysis: in
performance at 100%. dense execution-grounded optimization, the best solutions
Three contributions emerge from our experiments (Fig- occupy the low-probability tail of the model’s distribution,
ure 1): so sharpening toward high-confidence modes moves in the
 wrong direction. The compute-optimal strategy is sampling
 for diversity plus intelligent selection, not further sharpen-
 1. Search outperforms minimal adaptation (1-5 GRPO
 ing.
 steps) for dense-reward VEG tasks. Best-of-N scal-
 ing saturates at K = 16 (99.9% success on 5-task sub- Selection Strategies and Model Confidence. Prior work
 sets; 90% on the full 20-task L1 eval), while TTT on selection typically favors highest-confidence outputs or
 equivalent K < 1. Practitioners should invest in sam- uses reward models for reranking. Snell et al. (Snell et al.,
 ple diversity, not gradient updates. 2024) establish that compute-optimal test-time strategies
 outperform naive Best-of-N through intelligent selection.
 2. Surprisal-guided selection recovers oracle perfor-
 Khatri et al. (Khatri et al., 2025) characterize how to opti-
 mance. Selecting from the high-surprisal tail (solu-
 mally scale RL compute for LLMs, providing a framework
 tions the model “didn’t expect to find”) provides a
 for understanding compute allocation trade-offs. S* (Li
 practical, zero-cost selection strategy.
 et al., 2025a) achieves state-of-the-art code test-time scal-
 3. Mechanistic explanation for TTT failure. Over- ing through Adaptive Input Synthesis (generating new test
 sharpening destroys diversity, confirmed by direct cor- cases to differentiate candidates), but this requires addi-
 relation probing. The optimum for kernel optimization tional LLM calls. For kernel optimization, we find that
 2
 Surprisal-Guided Selection
Figure 2. Dual-loop architecture. The outer loop (blue) trains a base policy via reinforcement learning from verifiable rewards (RLVR)
on 80 KernelBench tasks. The inner loop (green) compares test-time strategies under matched compute. The selection mechanism
(dashed box) determines how to choose among correct samples. Both loops share the same evaluator (orange).
surprisal-guided selection (highest-surprisal, i.e., lowest Dr. Kernel (Liu et al., 2026) introduces KernelGYM with
log-probability, among correct samples) outperforms stan- reward hacking checks and TRLOO, a debiased alterna-
dard approaches by 30 percentage points with zero addi- tive to GRPO, achieving 31.6% Fast@1.2 on KernelBench
tional compute. The model’s probability distribution al- L2 through sequential multi-turn refinement; CUDA-L1 (Li
ready encodes this signal in the high-surprisal tail. This et al., 2025b) trains a contrastive RL model achieving 3.12×
inverse relationship between confidence and quality has average speedup across all 250 KernelBench tasks; QiMeng-
precedent in calibration literature. Guo et al. (Guo et al., Kernel (Zhu et al., 2025) decouples strategy from imple-
2017) show modern neural networks are often miscalibrated, mentation via hierarchical RL. These works optimize how
but this has not been operationalized as a selection strategy to train kernel-generating policies. We study a different
for execution-grounded code generation. question: given a capable policy, how should test-time com-
 pute be allocated between sampling, selection, and gradient
Verifiable Execution-Grounded Tasks. We focus on
 adaptation?
VEG tasks: domains where a deterministic evaluator pro-
vides ground-truth feedback without human judgment.
GPU kernel optimization is the primary example: Kernel- 3. Method
Bench (Ouyang et al., 2025) evaluates 250 workloads on
 3.1. Dual-Loop Architecture
correctness and speedup, with speedup ranging continuously
from 0x to 10x+. Related VEG domains include assembly To answer “is adaptation the right strategy for dense-reward
superoptimization (Wei et al., 2025) and formal theorem VEG tasks?”, we require controlled comparison between
proving. The VEG setting enables our surprisal-guided gradient-based adaptation and pure search strategies. We
selection strategy: execution feedback allows filtering to address this through a dual-loop architecture (Figure 2):
correct samples before applying surprisal-based selection.
 Outer Loop (Train-Time RLVR). The outer loop uses
Kernel Optimization. Prior work on LLM-based kernel reinforcement learning from verifiable rewards (RLVR) to
optimization has not studied selection strategies. Kevin (Ba- establish generalization across tasks. We train a base policy
ronio et al., 2025) achieves 82% correctness through multi- on 80 KernelBench L1 training tasks using Group Relative
turn train-time RL but keeps weights frozen at inference. Policy Optimization (GRPO) (Shao et al., 2024) with LoRA
CUDA-L2 (Su et al., 2025) surpasses cuBLAS by 19.2% adaptation. This produces a capable checkpoint (98.4%
through two-stage GRPO. Magellan (Chen et al., 2026) re- correctness, 0.87x mean speedup) that serves as the shared
quires ∼1.5 days of evolutionary search. AccelOpt (Zhang starting point for all test-time strategies.
et al., 2025) uses “Optimization Memory” for kernel search.
 Inner Loop (Test-Time Strategies). The inner loop is the
Concurrent work develops richer training-time RL pipelines:
 3
 Surprisal-Guided Selection
experimental arena. Given the trained base policy and a Algorithm 1 BoA with In-Batch Validation
held-out evaluation set (5 tasks), we compare three test- Require: Tasks T , checkpoint θ0 , steps S, rollouts K
time strategies under matched compute budgets: Best-of- 1: scores[0] ← evaluate(θ0 , T )
N search, which samples K candidates and selects via 2: for s = 1 to S do
oracle, surprisal-guided, or random selection; batch TTT 3: rollouts ← sample(θs−1 , T, K)
adaptation, which performs gradient updates with Best-of- 4: θs ← gradient update(θs−1 , rollouts)
Adaptation (BoA) checkpoint selection; and Self-Distilled 5: scores[s] ← aggregate fast 1(rollouts)
Policy Optimization (SDPO), which applies token-level 6: end for
distillation with or without execution feedback. 7: return θarg max(scores)
All strategies use the same base checkpoint, temperature
(0.25), and maximum tokens (1024). The key variable is the rank-16 LoRA adapter is updated in-place. Unlike TTT-
how test-time compute is allocated: sampling diversity vs. Discover’s ∼50-step full RL, we use minimal adaptation
gradient adaptation. (1–5 steps) to enable controlled comparison with search
 baselines under matched sample budgets.
Shared Evaluator. Both loops use the identical Kernel-
Bench execution-grounded evaluator (Section 3.2). This
ensures that “correct” and “speedup” mean the same thing 3.5. Best-of-Adaptation (BoA)
across all strategies, eliminating confounds from evaluation We define Best-of-Adaptation (BoA) as checkpoint selec-
protocol differences. tion over an adaptation trajectory. Instead of assuming the
 final checkpoint is best, BoA selects arg max(fast 1) across
3.2. Execution-Grounded Environment all steps.
Both train-time and test-time phases share KernelBench’s Early Stopping Variant: Stop when validation regresses
deterministic evaluator, which provides dense scalar rewards for P consecutive steps. In our experiments, P = 1 matched
through a five-stage pipeline. Model output is first inserted oracle selection; the first regression signaled the optimal
into a scaffolded kernel template, then compiled with CUDA checkpoint.
error capture. Correct samples are those that pass functional
equivalence tests against the reference implementation. For 3.6. SDPO: Execution-Grounded Self-Distillation
correct samples, timing is measured via CUDA events with
median taken over multiple trials. The reward is computed We extend batch adaptation with Self-Distilled Policy Opti-
as speedup = baseline time/kernel time, with incorrect mization (SDPO) (Hübotter et al., 2026), replacing scalar
samples receiving zero reward. reward advantages with token-level self-distillation signal
 conditioned on execution feedback. The teacher scores the
The continuous nature of the speedup reward (ranging from student’s sampled tokens:
0x for incorrect to 10x+ for highly optimized kernels) dis-
tinguishes this domain from preference-based tasks where At = β · (log pteacher (xt |context) − log pstudent (xt |prompt))
rewards are binary or sparse. Every sample provides gra- (1)
dient signal proportional to its quality, enabling efficient where β = 1.0 controls the distillation strength. Full SDPO
gradient aggregation across diverse rollouts. methodology and results are presented in Appendix F.
3.3. Train-Time: RLVR (Outer Loop) 4. Experimental Setup
Training uses normalized rewards (baseline-relative speedup 4.1. Equal-Budget Protocol
per task) for stability across tasks with varying baseline per-
formance. See Appendix A for the full outer loop specifica- The key methodological contribution is rigorous budget
tion. matching. All parameters are held constant between Best-
 of-N and batch TTT: 320 total rollouts, temperature 0.25,
3.4. Test-Time Strategies (Inner Loop) max tokens 1024, fast evaluation mode, the final RLVR
 checkpoint, and the optimized system prompt. The only
At test time, we adapt the trained checkpoint to held-out variable is how the 320 rollouts are used: independently
evaluation tasks using batch updates inspired by Test-Time (Best-of-N) or as gradient signal (TTT).
Reinforcement Learning (TTRL) (Zuo et al., 2025). Each
adaptation step processes N = 5 tasks jointly, sampling 4.2. Baselines
K = 32 rollouts per task to produce 160 samples per step. A
GRPO gradient update is computed across all rollouts, and We evaluate against three baselines. Best-of-N (K = 64)
 samples 64 candidates per task and selects the highest fast 1,
 4
 Surprisal-Guided Selection
 Table 1. Selection strategies for Best-of-N samples.
Strategy Selection Rule Cost
best-correct (Oracle) Max speedup, correct only Post-hoc
random-correct Random correct sample Baseline
confidence-guided Max logprob, correct only Zero
surprisal-guided Min logprob, correct only Zero
surprisal-guided-top3 Best of 3 min-logprob 3 evals
All strategies share correctness-checking of all K samples. The “Cost” column shows
additional speedup timing evaluations beyond shared filtering.
 Figure 3. Best-of-N scaling curve. Performance saturates at
totaling 320 rollouts across 5 tasks. The base policy uses K = 16 (99.9%). TTT BoA at 30.6% falls below K = 1 random
the RLVR checkpoint without test-time adaptation (step 0). sampling (53.3%).
SDPO variants (feedback and prompt-only self-distillation) Table 2. Best-of-N scaling (Subset 1, 2 seeds).
are reported in Appendix F.
 K pass@1 std 95% CI
4.3. Metrics
 1 53.3% 3.2% [20%, 100%]
We report three metrics. fast 1 measures the fraction of sam- 2 72.4% 4.1% [40%, 100%]
ples that are both correct and achieve speedup > 1x; this is 4 89.5% 2.8% [60%, 100%]
our primary metric as it captures both functional validity and 8 98.2% 0.8% [80%, 100%]
performance improvement. Correctness measures the frac- 16 99.9% 0.1% [100%, 100%]
tion passing functional equivalence tests. Mean speedup 32 100% 0% [100%, 100%]
reports the average speedup across correct samples. 64 100% 0% [100%, 100%]
 pass@1 denotes the probability that a randomly drawn sample is both correct and
 achieves speedup > 1× (i.e., fast 1 as defined in Section 4.3).
4.4. Tasks
Subset 1 (Primary): Tasks {4, 5, 12, 14, 15} from Kernel- 5. Results
Bench L1 eval split.
 5.1. Main Result: Search Outperforms Minimal
Subset 2 (Robustness): Tasks {18, 28, 29, 30, 32} (off- Adaptation
set=5).
 The central finding is that Best-of-N search decisively out-
Extended Eval (Full L1): Tasks {36, 55, 65, 70, 76, 82, performs test-time training under matched compute budgets.
87, 89, 95, 98} complete the full 20-task L1 eval set (seed This section presents the scaling curve comparison (Fig-
42). Best-of-N, per-sample evaluation, and logprob analysis ure 3); Section 5.2 presents our surprisal-guided selection
reported; selection strategy analysis in Section 5.2. strategy that achieves oracle-matching performance.
4.5. Selection Strategies Performance saturates at K = 16 with 99.9% success. Be-
 yond this point, marginal gains are near-zero, establishing
We compare five selection strategies for choosing among that modest sampling budgets suffice for dense-reward VEG
K = 64 samples per task: tasks.
The surprisal-guided strategies are motivated by probing TTT Equivalent K < 1: TTT’s Best-of-Adaptation
experiments (Section 5.2) showing an inverse correlation achieves 30.6% fast 1 (3-seed mean). Interpolating on the
between model confidence and kernel quality. The intuition: scaling curve, this falls below K = 1 (53.3%), meaning TTT
the model’s highest-surprisal correct samples are solutions is worse than drawing a single sample (K = 1). Best-of-N
it “didn’t expect to find,” often the creative, hardware-aware at K = 64 achieves 100% (oracle upper bound).
optimizations that yield maximum speedup.
 Why TTT Fails: Over-Sharpening. The failure mode
 is distribution collapse. TTT gradient updates concentrate
4.6. Compute Accounting
 probability mass on solutions that succeeded early in adap-
We report rollouts and total tokens (student + teacher) tation, typically mediocre solutions that happened to work.
for each method. See Appendix D for full token accounting. This destroys the diversity needed to find optimal kernels,
 5
 Surprisal-Guided Selection
 50%) corresponds to Cohen’s h = 0.64 (medium-to-large
 effect). On continuous speedup ratios, a paired Wilcoxon
 test on log(speedupsurprisal /speedupconfidence ) across 10 task-
 seed pairs yields p = 0.084 (test statistic = 10.0). On binary
 outcomes, all 3 discordant pairs favor surprisal (exact sign
 test p = 0.125, one-sided). Statistical power is limited at
 n = 10; Section 7 discusses this. The logprob variance
 analysis below characterizes when the selection signal is
Figure 4. Selection strategy comparison. (a) fast 1 success rate available across the full 20-task eval.
and (b) mean speedup. Surprisal-guided achieves 80% vs. 50% for
 Why Does Surprisal-Guided Selection Work? The
confidence-guided (+30%). Surprisal-guided-top3 matches oracle.
 model’s probability distribution is a map of frequency, not
 Table 3. Selection strategy results (Subset 1, 2 seeds). quality. Because naive code is more common than expert-
 optimized code in training data, the model’s “confidence”
 Strategy fast 1 std Mean Speedup (log-probability) is a proxy for how common a strategy is,
 not how fast it is. By selecting for surprisal, we are explic-
 best-correct (Oracle) 100% 0% 226.9x
 itly filtering for what we call the Expert Tail: those rare,
 surprisal-guided-top3 100% 0% 139.0x
 high-performance strategies that the model knows how to
 surprisal-guided 80% 0% 41.2x
 generate but considers statistically unlikely compared to
 random-correct 59.2% 2.7% 30.0x
 naive idioms.
 confidence-guided 50% 14.1% 11.6x
 Concretely, high-quality kernels often require unusual mem-
 ory access patterns, creative loop structures that deviate
which lie in the low-probability tail of the distribution. Ev- from common idioms, and hardware-specific optimizations
idence for over-sharpening includes: (1) non-monotonic not well-represented in training data. These rare solutions
trajectory with performance peaking at step 1–2 then re- occupy high-surprisal regions of the model’s distribution.
gressing (Section 5.3), (2) high variance across seeds (TTT Unlike S* (Li et al., 2025a), which requires additional
BoA std = 11.3% vs. Best-of-N std = 3.2%), (3) task- LLM calls to differentiate candidates, surprisal-guided se-
specific collapse with no consistent optimum across tasks, lection extracts this signal at zero cost from existing log-
and (4) direct negative log-likelihood (NLL) vs. speedup probabilities.
probe confirming progressive anti-calibration (Section 5.4).
 Length-Controlled Analysis. A potential confound: longer
5.2. Surprisal-Guided Selection code might have lower log-probability simply due to accu-
 mulating more token probabilities. Three analyses control
Given that search outperforms minimal adaptation, how for this. The raw Spearman correlation between logprob
should we select among correct samples? Standard practice and speedup is weak (ρ = −0.047, p = 0.27). The partial
is to choose the highest-confidence (lowest-surprisal) output. correlation controlling for code length is essentially zero
We discover that for kernel optimization, the opposite strat- (ρ = 0.003, p = 0.95). And the direct length-speedup cor-
egy works better (Figure 4). Critical distinction: we select relation is negligible (ρ = −0.039). The surprisal-guided
the most surprising correct sample, not the most surpris- effect is not explained by code length.
ing overall (which would be gibberish). The VEG setting
enables this by providing a correctness filter via execution. Why weak correlation coexists with strong selection. The
 near-zero correlation may appear to contradict the 80% vs.
Three findings emerge from this comparison. First, surprisal- 50% selection result, but these measure fundamentally dif-
guided selection beats confidence-guided by 30% (80% vs. ferent things. Correlation measures whether surprisal lin-
50%): selecting the highest-surprisal correct sample out- early predicts speedup across all 550 correct samples, and it
performs the standard confidence-guided approach. Second, does not. Selection operates via per-task argmax: for each
surprisal-guided-top3 matches oracle performance: evalu- task, we pick the single highest-surprisal correct sample.
ating just 3 samples (the 3 highest-surprisal correct ones, Selection operates on the per-task argmax in the tail, not on
after the shared correctness filter) and selecting the fastest the global slope. This succeeds when the highest-surprisal
achieves 100% success, identical to oracle selection over sample within each task tends to be among its best solutions,
all 64 samples. Third, confidence-guided selection exhibits a per-task ordinal property that global linear correlation
high variance (std = 14.1%), indicating unreliable perfor- cannot capture.
mance, while surprisal-guided has std = 0%, consistent
success across all tasks. Quartile Analysis. The full quartile breakdown appears
 in Appendix H (Table 11). Q2 (second-highest surprisal)
Statistical strength. The 30-percentage-point gap (80% vs.
 6
 Surprisal-Guided Selection
shows the highest fast 1 (81.0%), while Q4 (lowest sur-
prisal) shows the lowest (43.9%). The high-surprisal half
(Q1+Q2) averages 64.2% fast 1 versus 58.1% for the low-
surprisal half (Q3+Q4). This pattern suggests the optimal
selection point is in the high-surprisal region but not the
extreme tail.
Logprob Variance and Selection Applicability. Expand-
ing logprob analysis to all 20 L1 eval tasks reveals a prereq-
uisite for surprisal-guided selection: sufficient intra-task
logprob variance. Of 20 tasks, 9 exhibit high variance
(logprob std > 1.0)—these include the original Subset 1
and 2 tasks, where diverse solution strategies create a log- Figure 5. Adaptation trajectory. Performance peaks at 1–2 steps
 then regresses. Stars mark BoA-selected checkpoints.
prob gradient for selection to exploit. The remaining 11
tasks produce near-identical logprobs across samples (std
< 0.15 for 7 tasks). These are primarily convolution and
normalization operations where the reference uses cuDNN
(already near-optimal); the model converges to a narrow
template with minimal speedup headroom (sample fast 1
of 7–23%, selected speedup 1.00–1.22x). On such tasks,
all selection strategies degenerate to random. Head-to-head
across the 19 valid tasks (excluding Task 95, 0% correct-
ness), surprisal wins 6/8 on high-variance tasks but only
3/11 on low-variance tasks. The surprisal-guided effect is
concentrated in tasks where diverse optimization strategies
exist—precisely the tasks where selection provides leverage.
5.3. TTT Trajectory: Why Adaptation Fails
 Figure 6. Over-sharpening probe. Spearman ρ(NLL, speedup)
To understand why TTT underperforms, we examine the across TTT steps for 320 fixed samples. The negative correlation
adaptation trajectory (Figure 5). Performance peaks at deepens overall: adaptation makes the model progressively more
step 2 (42.5%) and regresses to 36.3% at step 3, the over- confident about its worst solutions. Bottom-quartile ρ nearly dou-
 bles from −0.24 to −0.44.
sharpening dynamic in action (full per-task breakdown in
Appendix C). Gradient updates collapse diversity toward
 Across all per-task isolated TTT runs (Table 12), 4 of 5 tasks
mediocre solutions.
 peak within the first 2 adaptation steps (Tasks 4, 5, 12, 15);
The per-task breakdown reveals heterogeneous dynamics: only Task 14 shows a delayed peak at step 4.
Task 12 is already saturated at 100% (easy task, no room for
improvement); Task 5 peaks at step 1, then collapses to 3.1% 5.4. Probing Over-Sharpening: Direct Measurement
by step 3; Task 4 peaks at step 2, then regresses. This het-
erogeneity explains why TTT’s aggregate BoA performance The evidence for over-sharpening in Sections 5.3 and the
(30.6% 3-seed mean) underperforms Best-of-N (100% at per-task analysis above is outcomes-based: performance
K = 16): adaptation cannot simultaneously optimize for regresses after step 1–2. To directly measure the probability
tasks with different optima. shift, we probe how the adapted policy’s NLL rankings
 relate to sample quality across TTT steps.
Per-Task Isolated TTT Validation. To confirm that over-
sharpening occurs even without multi-task interference, we We take 320 fixed Best-of-N samples (K = 64, seed 42) with
ran TTT on individual tasks (batch size= 1, K = 32, 5 steps; known speedups and compute each sample’s NLL under
full results in Appendix H, Table 12). The pattern reveals every TTT checkpoint (steps 0–8). This holds the sample set
task-level heterogeneity: Tasks 4, 5, 15 show classic over- constant while varying only the scoring model, isolating the
sharpening (peak at step 1, then regress); Task 14 shows a effect of adaptation on the probability-quality relationship.
late peak at step 4; Task 12 is saturated throughout. This Figure 6 shows the result. The Spearman ρ between NLL
confirms the heterogeneity observed in the batch setting, and speedup deepens overall from −0.198 (step 0, p =
ruling out multi-task interference as the sole cause of over- 3.6 × 10−4 ) to −0.275 (step 8, p = 5.7 × 10−7 ). The
sharpening. bottom-quartile correlation (the performance-critical tail
 where selection operates) nearly doubles from ρ = −0.237
 7
 Surprisal-Guided Selection
 Table 4. Subset 2 results (seed 42).
 Method Rollouts Agg fast 1 Delta
 Best-of-N (K = 64) 320 36.9% baseline
 BoA Step 0 160 17.5% −19.4%
 BoA Step 1 320 16.3% −20.6%
to ρ = −0.442 (step 3, p = 9.8 × 10−17 ).
This is not merely diversity loss. The deepening negative
ρ means TTT assigns progressively higher confidence to
worse solutions: active anti-calibration in exactly the region Figure 7. Regime-dependent benefit of adaptation vs. search.
 Tasks with >30% base coverage (light shading) show smaller BoA
where surprisal-guided selection operates. Meanwhile, the deficits; tasks below this threshold (dark shading) show larger
mean NLL trajectory oscillates non-monotonically (6.71 → deficits, favoring Best-of-N.
6.66 → 6.75 → 6.86), indicating unstable training dynam-
ics rather than smooth convergence.
5.5. Robustness: Second Task Subset (Hard Regime)
To test whether findings generalize, we replicated the com-
parison on Subset 2: tasks {18, 28, 29, 30, 32} (offset=5
from the eval split), a harder 5-task subset.
 signal from diverse rollouts, rapidly compressing execution
On the hard subset, Best-of-N outperforms BoA under feedback into the weights. Additional steps over-sharpen the
equal budget. The contrasting results reveal that adapta- distribution around a narrow subset of solutions, reducing
tion’s deficit is regime-dependent: on Subset 1 (3 seeds), diversity and causing regression.
BoA shows a −9.2% deficit relative to Best-of-N baseline
(39.8%), while on Subset 2 (seed 42), the deficit is larger The following observations support this interpretation.
at −20.6% relative to baseline (36.9%). Adaptation ampli- The BoA peak at 1–2 steps shows compression complet-
fies existing capability rather than creating new capability ing quickly. The step-dependent regression shows over-
(Figure 7). In both regimes, search maintains a diversity compression destroying diversity. SDPO experiments con-
advantage. firm this interpretation (Section 6.5).
Full L1 Eval (20 Tasks). Expanding Best-of-N to all 20 L1 We hypothesize a Reward Compression Principle: gradi-
eval tasks: 18/20 (90%) achieve fast 1= 1 at K = 64. Two ent steps to saturation scale inversely with reward density.
failures are informative edge cases. Task 82 achieves 100% Dense continuous rewards compress in 1–2 steps; sparse
correctness but 1.00x speedup—the reference uses cuDNN, binary rewards require extended adaptation. This princi-
leaving no optimization headroom. Task 95 achieves 0% ple unifies our findings: fast saturation and feedback re-
correctness—the model cannot generate valid kernels. Nei- dundancy are two manifestations of the same underlying
ther reflects a search strategy limitation: Task 82 is a task- dynamic.
level ceiling (no amount of search helps when the reference Cross-Subset Transfer. If adaptation builds generalizable
is already optimal); Task 95 is a model capability gap (no optimization strategies, knowledge should transfer across
correct samples exist to select from). The 90% success rate task subsets. We evaluate cross-subset transfer: checkpoints
across the full eval set, versus 100% on the 10-task subsets, adapted on Subset 1 (tasks {4, 5, 12, 14, 15}) evaluated on
reflects inclusion of tasks at both extremes of difficulty. Subset 2 (tasks {18, 28, 29, 30, 32}) and vice versa.
Evaluation Note. Results use a fast-proxy evaluation proto- Checkpoints adapted on Subset 1 and evaluated on Subset 2
col (5 performance trials per kernel) rather than the full Ker- achieve 7.5% fast 1, down from the unadapted baseline of
nelBench benchmark (50 trials), as our focus is on test-time 17.5% and far below Best-of-N’s 36.9%. The reverse direc-
compute scaling strategies rather than benchmark leader- tion (Subset 2 adapted, Subset 1 evaluated) yields 31.25%,
board performance. also below the unadapted 37.5%.
 Both directions show degradation relative to unadapted base-
5.6. Compression Mechanism: Rapid Signal Distillation
 lines. Adaptation over-fits to training-subset modes rather
We propose a compression view of test-time training in VEG than learning domain-general kernel optimization strategies,
domains. The first 1–2 updates aggregate dense gradient consistent with the over-sharpening interpretation.
 8
 Surprisal-Guided Selection
6. Discussion remains an open question.
6.1. Why VEG Tasks Favor Search Over Adaptation Objective mismatch. TTT-Discover optimizes for “find a
 new SOTA solution” and returns the best solution across all
Verifiable execution-grounded tasks differ fundamentally steps (argmax reward). Our evaluation uses fast 1 (correct
from preference-based or sparse-reward domains. Three and speedup > 1×) on KernelBench L1 with K capped
properties drive this difference. First, VEG tasks provide at 64. These are different targets; our findings apply to
dense scalar rewards; speedup is continuous (0x to 10x+), budgeted inference, not open-ended discovery.
not binary. Second, VEG evaluation is evaluation-bound:
CUDA compilation, warmup runs, and performance timing We swept learning rates across three orders of magnitude
create per-sample overhead. Third, when the world provides (lr ∈ {1e-5, 1e-6, 3e-7}; Appendix G). Over-sharpening
dense continuous feedback, an AI teacher interpreting that persists at all learning rates: lr=1e-6 peaks at step 1 (55.0%)
feedback becomes redundant (Section 6.5). then regresses; lr=3e-7 never exceeds the unadapted baseline
 (31.9%).
These properties suggest VEG may be a distinct regime
for test-time compute allocation. For domains with dense
 6.4. Future Direction: Zero-Evaluation Discovery
continuous rewards from a deterministic evaluator, sample
diversity with intelligent selection (surprisal-guided) may Our findings point toward zero-evaluation discovery: mod-
be more efficient than gradient adaptation. els generating optimal code for novel hardware without
 physical execution. This requires physics-grounded world
6.2. The Minimum Signal Threshold models, internal simulations of how code interacts with
 hardware. From Word to World (Li et al., 2025c) formal-
We introduce a minimum signal threshold: the gradient sig- izes evaluation of implicit world models; SSRL (Fan et al.,
nal needed before over-sharpening degrades diversity. For 2025) proposes LLMs as internal world simulators. Ex-
dense-reward kernel optimization, this threshold is remark- ecution feedback can be efficiently distilled into weights
ably low: 1–2 steps from 160 diverse samples. Scalable through minimal adaptation, a tractable path toward inter-
Power Sampling (Ji et al., 2026) corroborates this (RL gains nalized hardware models.
= sharpening, not discovery), as does Agent RL Scaling
Law (Mai et al., 2025) (models quickly internalize code Implicit hardware world models remain a research direction,
heuristics). The threshold likely depends on reward den- not a demonstrated capability of this work. Our contribution
sity: sparse-reward domains may require more steps, while is the efficiency characterization that makes this direction
dense-reward domains saturate quickly. tractable.
6.3. Relationship to Concurrent Work 6.5. Self-Distillation: Why Feedback Adds No Lift
TTT-Discover (Yuksekgonul et al., 2026) represents the SDPO experiments (Appendix F) show prompt-only self-
strongest case for extended test-time adaptation. Key dif- distillation succeeds at 120B scale, but feedback context
ferences distinguish our findings. First, TTT-Discover provides no lift in VEG domains. When the world provides
uses ∼50 steps while we find 1–2 optimal. Second, continuous gradient signal, feedback interpretation becomes
TTT-Discover does not compare against Best-of-N under redundant.
matched compute. Third, the difference stems from reward
density: sparse-reward discovery may require extended ex- 6.6. Open Questions
ploration, while dense-reward VEG tasks saturate quickly.
 Several open questions remain. First, an entropy-regularized
Our results complement rather than contradict TTT-Discover TTT baseline (closer to TTT-Discover’s entropic objective)
by identifying reward density as the key variable determin- would test whether the over-sharpening failure is funda-
ing optimal adaptation duration. mental to dense-reward VEG domains or specific to vanilla
 GRPO. Second, a deployable surprisal-guided pipeline that
Our TTT experiments use vanilla GRPO without the entropy
 ranks candidates by surprisal before correctness filtering
regularization, reuse buffers, and extended rollout budgets
 (evaluating only the top-m candidates end-to-end) would
(512 per step) employed by TTT-Discover (Yuksekgonul
 transform the selection insight from post-hoc analysis to
et al., 2026). Our total budget is 320 rollouts versus TTT-
 a practical method. Third, reward sparsification experi-
Discover’s 25,600. Whether those mechanisms and budgets
 ments (thresholding the continuous speedup signal) would
prevent over-sharpening in dense-reward VEG domains re-
 test whether the step-optimum shifts upward as reward be-
mains untested. Dr. Kernel’s TRLOO algorithm (Liu et al.,
 comes sparser, directly validating the reward compression
2026) addresses GRPO’s self-inclusion bias; whether TR-
 hypothesis.
LOO prevents over-sharpening in dense-reward VEG TTT
 9
 Surprisal-Guided Selection
7. Limitations 1. Search saturates at modest K. Best-of-N scaling
 shows performance saturates at K = 16 (99.9% suc-
This work has several limitations. Best-of-N evaluation cess). Practitioners should invest in sample diversity,
covers all 20 KernelBench L1 eval tasks (90% task success not gradient updates.
at K = 64). The primary selection experiment uses 10
task-seed pairs (5 tasks × 2 seeds); the 20-task logprob 2. Surprisal-guided selection recovers oracle perfor-
expansion reveals the variance regime boundary but uses a mance. Selecting the highest-surprisal correct sam-
single seed. All experiments use a single 120B-parameter ple achieves 80% success vs. 50% for most-confident,
model; transfer to other sizes and architectures remains a 30% improvement with zero additional compute.
untested. We evaluate only L1 tasks; harder L2 and L3 Extending to surprisal-guided-top3 matches oracle at
levels may exhibit different dynamics. 100%.
Our TTT experiments scope to vanilla GRPO (see Sec- 3. TTT fails due to over-sharpening. Gradient updates
tion 6.3 for discussion of differences from TTT-Discover). collapse the policy toward mediocre solutions, destroy-
 ing the diversity needed to find optimal kernels in the
With n = 10 binary outcomes (5 tasks × 2 seeds), our pri-
 distribution tail.
mary selection comparison (80% vs. 50%) has limited statis-
tical power for binary tests (exact sign test p = 0.125). We
supplement with continuous speedup analysis (Section 5.2). The practical implication is clear: for dense-reward VEG
 tasks, allocate compute to sample diversity and intelligent se-
The surprisal-guided selection strategy requires multiple lection rather than gradient adaptation. The surprisal-guided
correct samples per task; on harder levels (L2/L3) or tasks selection principle (that rare, high-quality solutions occupy
where the base policy has low coverage, the effect may high-surprisal regions) may generalize to other execution-
diminish or vanish. Moreover, surprisal-guided selection grounded domains where the optimum lies in the distribu-
requires sufficient intra-task logprob variance. On 11/20 tion tail.
L1 tasks where the model produces near-identical solutions
(logprob std < 1.0), the selection signal vanishes and all The prevailing assumption that test-time training provides
strategies perform equivalently. universal benefits does not hold in this regime. In domains
 with dense continuous rewards and deterministic evaluation,
Our evaluation uses a fast-proxy protocol (5 timing trials gradient updates that worked for sparse-reward reasoning
per kernel); rankings could shift under the full Kernel- tasks become counterproductive when the goal is finding
Bench protocol (50 trials). We validated selected kernels optimal solutions in a well-sampled distribution’s tail.
on H100 hardware and observed consistent rankings, but a
full-protocol replication on a larger subset would strengthen
 Acknowledgments
these results.
The inverse relationship between confidence and quality We thank Thinking Machines Lab for access to the Tinker
may be domain-specific. In kernel optimization, rare cre- training infrastructure.
ative solutions yield high speedups. In domains where the
mode represents optimal behavior, surprisal-guided selec- References
tion could perform poorly. A formal analysis of the relation-
 Baronio, C., Marsella, P., Pan, B., Guo, S., and Alberti, S.
ship between training distribution coverage and test-time
 Kevin: Multi-turn rl for generating cuda kernels. arXiv
solution quality could strengthen these empirical findings.
 preprint arXiv:2507.11948, 2025.
8. Conclusion Chen, H., Novikov, A., Vũ, N., Alam, H., Zhang, Z.,
 Grossman, A., Trofin, M., and Yazdanbakhsh, A. Mag-
We study compute-optimal test-time strategies for verifiable ellan: Autonomous discovery of novel compiler opti-
execution-grounded tasks, demonstrating across all 20 Ker- mization heuristics with alphaevolve. arXiv preprint
nelBench L1 eval tasks that search outperforms minimal arXiv:2601.21096, 2026.
adaptation (1-5 gradient steps) for GPU kernel optimization.
Best-of-N sampling achieves 90% task success (18/20) at Fan, Y., Zhang, K., Zhou, H., Zuo, Y., Chen, Y., Fu, Y., Long,
K = 64 while TTT’s best checkpoint reaches only 30.6% X., Zhu, X., Jiang, C., Zhang, Y., Kang, L., Chen, G.,
(3-seed mean), with TTT’s “equivalent K” falling below 1, Huang, C., He, Z., Wang, B., Bai, L., Ding, N., and Zhou,
meaning adaptation underperforms single-sample inference. B. SSRL: Self-search reinforcement learning. arXiv
 preprint arXiv:2508.10874, 2025.
Three findings characterize the compute-optimal strategy:
 Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. On cali-
 bration of modern neural networks. In International Con-
 10
 Surprisal-Guided Selection
 ference on Machine Learning (ICML), pp. 1321–1330, Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
 2017. H., Zhang, M., Li, Y. K., Wu, Y., and Guo, D. Deepseek-
 math: Pushing the limits of mathematical reasoning in
Hübotter, J., Lübeck, F., Behric, L., Baumann, A., Bagatella, open language models. arXiv preprint arXiv:2402.03300,
 M., Marta, D., Hakimi, I., Shenfeld, I., Kleine Buening, 2024.
 T., Guestrin, C., and Krause, A. Reinforcement learning
 via self-distillation. arXiv preprint arXiv:2601.20802, Si, C., Yang, Z., Choi, Y., Candès, E., Yang, D., and
 2026. Hashimoto, T. Towards execution-grounded automated
 ai research. arXiv preprint arXiv:2601.14525, 2026.
Ji, X., Tutunov, R., Zimmer, M., and Bou Ammar, H. Scal-
 Snell, C., Lee, J., Xu, K., and Kumar, A. Scaling llm test-
 able power sampling: Unlocking efficient, training-free
 time compute optimally can be more effective than scal-
 reasoning for llms via distribution sharpening. arXiv
 ing model parameters. arXiv preprint arXiv:2408.03314,
 preprint arXiv:2601.21590, 2026.
 2024.
Khatri, D., Madaan, L., Tiwari, R., Bansal, R., Duvvuri, Su, S., Sun, X., Li, X., Wang, A., Li, J., and Shum, C.
 S. S., Zaheer, M., Dhillon, I. S., Brandfonbrener, D., CUDA-L2: Surpassing cuBLAS performance for matrix
 and Agarwal, R. The art of scaling reinforcement learn- multiplication through reinforcement learning. arXiv
 ing compute for llms. arXiv preprint arXiv:2510.13786, preprint arXiv:2512.02551, 2025.
 2025.
 Wei, A., Suresh, T., Tan, H., Xu, Y., Singh, G., Wang, K.,
Li, D., Cao, S., Cao, C., Li, X., Tan, S., Keutzer, K., Xing, and Aiken, A. Supercoder: Assembly program superop-
 J., Gonzalez, J. E., and Stoica, I. S*: Test time scaling timization with large language models. arXiv preprint
 for code generation. arXiv preprint arXiv:2502.14382, arXiv:2505.11480, 2025.
 2025a.
 Yuksekgonul, M., Koceja, D., Li, X., Bianchi, F., McCaleb,
Li, X., Sun, X., Wang, A., Li, J., and Shum, C. Cuda-l1: Im- J., Wang, X., Kautz, J., Choi, Y., Zou, J., Guestrin, C., and
 proving cuda optimization via contrastive reinforcement Sun, Y. Learning to discover at test time. arXiv preprint
 learning. arXiv preprint arXiv:2507.14111, 2025b. arXiv:2601.16175, 2026.
 Zhang, G., Zhu, S., Wei, A., Song, Z., Nie, A., Jia, Z.,
Li, Y., Wang, H., Qiu, J., Yin, Z., Zhang, D., Qian, C., Li, Vijaykumar, N., Wang, Y., and Olukotun, K. Accelopt:
 Z., Ma, P., Chen, G., Ji, H., and Wang, M. From word to A self-improving llm agentic system for ai accelerator
 world: Can large language models be implicit text-based kernel optimization. arXiv preprint arXiv:2511.15915,
 world models? arXiv preprint arXiv:2512.18832, 2025c. 2025.
Liu, W., Xu, J., Li, Y., Zheng, L., Li, T., Liu, Q., and He, J. Zuo, Y., Zhang, K., Sheng, L., Qu, S., Cui, G., Zhu, X.,
 Dr. kernel: Reinforcement learning done right for triton Li, H., Zhang, Y., Long, X., Hua, E., Qi, B., Sun, Y.,
 kernel generations. arXiv preprint arXiv:2602.05885, Ma, Z., Yuan, L., Ding, N., and Zhou, B. Ttrl: Test-time
 2026. reinforcement learning. arXiv preprint arXiv:2504.16084,
 2025. Accepted to NeurIPS 2025.
Mai, X., Xu, H., Li, Z.-Z., Wu, X., Wang, W., Hu, J., Zhang,
 Y., and Zhang, W. Agent rl scaling law: Agent rl with
 spontaneous code execution for mathematical problem A. Experimental Configuration
 solving. arXiv preprint arXiv:2505.07773, 2025.
 # RLVR Training (produces base checkpoint)
 model: openai/gpt-oss-120b
Ouyang, A., Guo, S., Arora, S., Zhang, A. L., Hu, W., Ré, algorithm: GRPO
 lora_rank: 16
 C., and Mirhoseini, A. Kernelbench: Can llms write learning_rate: 1e-5
 efficient gpu kernels? arXiv preprint arXiv:2502.10517, batch_size: 8
 group_size: 8
 2025. training_tasks: 80 (KernelBench L1 train split)
 temperature: 0.25
 max_tokens: 1024
Zhu, X., Peng, S., Guo, J., Chen, Y., Guo, Q., Wen, Y., normalize_reward: true
 Qin, H., Chen, R., Zhou, Q., Gao, K., Wu, Y., Zhao,
 # Test-Time Evaluation
 C., and Li, L. Qimeng-kernel: Macro-thinking micro- checkpoint: RLVR final (step 40,
 coding paradigm for llm-based high-performance gpu ker- 98.4% correct, 0.87x speedup)
 eval_tasks: {4, 5, 12, 14, 15} (subset 1),
 nel generation. arXiv preprint arXiv:2511.20100, 2025. {18, 28, 29, 30, 32} (subset 2)
 Accepted to AAAI 2026.
 11
 Surprisal-Guided Selection
 Table 5. RLVR training progression (outer loop). Table 7. Full compute breakdown (mean across seeds).
Checkpoint Correctness Speedup Notes Method Rolls Student Teacher Total Wall (min)
Step 10 90.6% 0.81x Early training RLVR Base (K = 1) 5 4.0K 0 4.0K —
 Best-of-N (K = 64) 320 313K 0 313K 42
Step 20 95.3% 0.87x —
 BoA Step 1 320 313K 0 313K ∼60†
Step 30 95.3% 0.86x — SDPO (feedback) 320 314K 338K 652K —
Step 40 (final) 98.4% 0.87x Used for all eval SDPO (prompt-only) 320 311K 313K 625K —
 †
 BoA Step 1 matches BoN rollout count but includes backprop overhead; full 9-step
 TTT trajectory takes ∼267 min for 1,440 rollouts.
 Table 6. Batch TTT trajectory (seed 42, Subset 1).
 Table 8. Best-of-N selected speedup (K = 64, Subset 1, Seed 42).
 Step Rollouts Agg T4 T5 T12 T14 T15
 0 160 37.5 9.4 3.1 100 37.5 37.5 Task Selected Speedup
 1 320 40.0 28.1 15.6 100 21.9 34.4 4 859.8x
 2 480 42.5 46.9 6.3 100 18.8 40.6 5 191.7x
 3 640 36.3 25.0 3.1 100 21.9 31.3 12 23.8x
 4 800 36.3 21.9 3.1 100 15.6 40.6 14 15.6x
 5 960 41.3 25.0 9.4 100 40.6 31.3 15 13.6x
# Best-of-N F. SDPO Self-Distillation Experiments
K: 64
total_rollouts: 320 (5 tasks x 64) We extend batch adaptation with Self-Distilled Policy Opti-
# Batch TTT (BoA) mization (SDPO), replacing scalar reward advantages with
K: 32 per task token-level self-distillation signal conditioned on execution
tasks_per_step: 5
learning_rate: 1e-5 feedback.
step_1_rollouts: 320 (5 tasks x 32 x 2)
 Teacher Context Construction. For each student rollout,
 we construct a teacher context containing: (1) the original
B. RLVR Training Progression task prompt, (2) a correct solution from the same batch if
Table 5 shows the outer loop training progression. The available, (3) structured execution feedback (compile status,
final checkpoint (step 40) achieves 98.4% correctness with correctness, speedup, runtime, error traces), and (4) the
0.87x mean speedup, establishing a strong base policy for instruction: “Correctly solve the original question.” The
test-time evaluation. student’s original code is not included; only its execution
 outcome.
C. TTT Trajectory Details Table 9 reports SDPO results across all three seeds on Sub-
 set 1.
Table 6 shows the full per-task breakdown of the batch TTT
adaptation trajectory for seed 42 on Subset 1. The aggre- Key Finding: Feedback provides no lift. SDPO with full
gate performance peaks at step 2 (42.5%) before regress- execution feedback (26.3%) underperforms SDPO prompt-
ing, while individual tasks show heterogeneous dynamics: only (30.4%), consistent across all 3 seeds. In our Ker-
Task 12 saturates at 100% throughout; Tasks 4, 5, 15 peak nelBench L1 setting and SDPO-style feedback construc-
early then regress; Task 14 shows delayed improvement. tion, execution feedback provides no lift over prompt-only
 self-distillation. This is consistent with a reward density
 hypothesis: when the world provides dense continuous
D. Compute Accounting rewards, an AI teacher interpreting that feedback may be
Table 7 provides the full token accounting for each method, redundant. Whether this generalizes beyond our setting (to
enabling compute-matched comparisons. smaller models, harder tasks (L2/L3), or alternative feed-
 back formats) remains open.
E. Speedup Statistics Table 9. SDPO results (Subset 1, 3 seeds).
Raw speedup magnitude varies widely across tasks, reflect- Method Seed 42 Seed 43 Seed 44 Mean ± std
ing task-specific optimization headroom rather than method
 SDPO (feedback) 35.6% 18.8% 24.4% 26.3% ± 8.6%
quality. fast 1 (correct AND speedup > 1x) is the operative
 SDPO (prompt) 38.8% 23.8% 28.8% 30.4% ± 7.6%
metric.
 12
 Surprisal-Guided Selection
Self-Distillation at Frontier Scale. Using a 120B-
parameter model, we find that prompt-only self-distillation
succeeds at frontier scale, but feedback context provides no
lift in VEG domains with dense rewards. This may change
with model scale: at 120B, the model likely already encodes
sufficient knowledge of error traces, making explicit feed-
back redundant. Smaller models or harder tasks (L2/L3)
might benefit more from structured feedback context.
G. Learning Rate Sensitivity
Table 10 shows TTT performance across three learning
rates spanning three orders of magnitude. Over-sharpening
persists at all learning rates.
 Table 10. TTT BoA across learning rates (Subset 1, seed 42).
LR Peak Step BoA fast 1 Pattern
1e-5 (default) 2 42.5% Peak then regress
1e-6 1 55.0% Early peak, regression
3e-7 0 31.9% No improvement
H. Supplementary Tables
 Table 11. Surprisal quartile breakdown.
 Quartile fast 1 Speedup Tokens
 Q1 (high surprisal) 47.4% 37.0x 7
 Q2 81.0% 26.2x 8
 Q3 72.3% 46.8x 10
 Q4 (low surprisal) 43.9% 30.6x 15
Note: Global quartiles conflate task identity with surprisal rank
(Q1 is 79% Task 5; Q2 is 48% Task 12). Surprisal-guided selection
operates per-task, avoiding this confound.
 Table 12. Per-task isolated TTT (seed 42).
 Task Step 0 Step 1 Step 2 Steps 3–5 BoA
 4 (hard) 0% 6.3% 0% 0% Step 1
 5 (mod.) 3.1% 12.5% 12.5% 3.1% Step 1
 12 (ctrl) 100% 100% 100% 100% Step 0
 14 (mod.) 37.5% 34.4% 37.5% 56.3% Step 4
 15 (mod.) 43.8% 46.9% 34.4% 40.6–46.9% Step 1
 13
