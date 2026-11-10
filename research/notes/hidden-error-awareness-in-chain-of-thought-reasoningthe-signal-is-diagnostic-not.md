---
title: Hidden Error Awareness in Chain-of-Thought Reasoning:The Signal Is Diagnostic,
  Not Causal
id: hidden-error-awareness-in-chain-of-thought-reasoningthe-signal-is-diagnostic-not
tags:
- code-llm-confidence-positioning-d82d00
- hidden-state-probe
- verbalized-confidence
- causal-intervention
- reasoning-models
created: '2026-11-09T23:07:40.531717Z'
updated: '2026-11-09T23:27:44.371392Z'
source: https://arxiv.org/html/2605.09502
source_domain: arxiv.org
fetched_at: '2026-11-09T23:07:40.531301Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'CLOSE for L2 methodology (probe vs verbal, reasoning models, causal interventions)
  but on MATH-500 math, not code. Full text (arXiv HTML). arXiv 2605.09502, full text.
  Logistic-regression probes on hidden states during chain-of-thought predict trace
  correctness: 0.95 AUROC (Table 2: probe 0.953 vs self-consistency N=5 0.823, verbalized
  0.67, CCS 0.72) versus verbalized confidence 4.55/5 for wrong vs 4.87/5 for correct
  traces; first-step probe 0.79 vs text classifier 0.59. Nine models 1.5B-72B (Qwen2.5,
  Llama-3.1-8B, Phi-3.5-mini, DeepSeek-R1-Distill-Qwen-7B at 0.852 eval AUROC); Table
  1 shows non-monotone scale (Qwen2.5-7B CV 0.669, 14B 0.762, 72B 0.977). Trains on
  100 MATH-500 problems, evaluates on 200 held-out. Four interventions (activation
  steering, probe-guided best-of-N, self-correction, activation patching) all fail:
  ''The signal is diagnostic, not causal.'' Limitation: MATH-500 only, up to 72B,
  no fine-tuning on probe signals. No code, no execution labels, no base/instruct
  contrast, no release-date split. Occupies probe-beats-verbal in reasoning and the
  diagnostic-not-causal intervention result for math; not for code.'
---

Hidden Error Awareness in Chain-of-Thought Reasoning:The Signal Is Diagnostic, Not Causal
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2605.09502v1 [cs.CL] 10 May 2026
Hidden Error Awareness in Chain-of-Thought Reasoning:
The Signal Is Diagnostic, Not Causal
Aojie Yuan
Affiliation:
University of Southern California, Los Angeles, CA, USA
Zhiyuan Julian Su
Affiliation:
University of Southern California, Los Angeles, CA, USA
Haiyue Zhang
Affiliation:
University of Southern California, Los Angeles, CA, USA
Yi Nian
Affiliation:
University of Southern California, Los Angeles, CA, USA
Yue Zhao
Affiliation:
University of Southern California, Los Angeles, CA, USA
Abstract
Chain-of-thought (CoT) prompting assumes that generated reasoning reflects a model’s internal computation.
We show this assumption is wrong in a specific, measurable way:
models internally detect their own reasoning errors but outwardly express confidence in them
.
A linear probe on hidden states predicts trace correctness with 0.95 AUROC—from the
very first reasoning step
(0.79)—while verbalized confidence for wrong traces is 4.55/5, nearly identical to correct ones (4.87/5).
A text-surface classifier achieves only 0.59 on the same data, confirming a 0.20-point gap invisible in the generated text.
This
hidden error awareness
holds across three model families (Qwen, Llama, Phi), 1.5B–72B parameters, and RL-trained reasoning models (DeepSeek-R1, 0.852 AUROC).
The natural question is whether this signal can fix the errors it detects. It cannot.
Four interventions—activation steering, probe-guided best-of-N, self-correction, and activation patching—all fail; patching
destroys
output coherence entirely.
The signal is
diagnostic, not causal
: a readout of computation quality, not a lever to redirect it.
This delineates a boundary for mechanistic interpretability: error representations during reasoning are fundamentally different from the factual knowledge representations that prior work has successfully edited.
†
†
affiliationnotice:
Correspondence to: Aojie Yuan
<aojieyua@usc.edu>
.
1
Introduction
Chain-of-thought (CoT) prompting
(
Wei et al., 2022
)
rests on an implicit contract: the model’s written reasoning reflects its internal computation.
If the text says “
3
×
5
=
15
3\times 5=15
,” the model computed this and will build on it.
Prior work has questioned this contract through behavioral tests—showing that CoT explanations can be steered by irrelevant cues
(
Turpin et al., 2023
)
or truncated without changing the answer
(
Lanham et al., 2023
)
—but these interventions operate on the text surface.
A direct comparison between what models
say
and what they
internally represent
during reasoning has been missing.
We provide this comparison by training linear probes on hidden states extracted during CoT generation (Figure
1
).
The results tell a story in three acts, each raising the stakes of the previous finding.
Act I: The signal exists, and it is early.
A logistic regression probe achieves 0.95 AUROC for predicting trace correctness—far exceeding verbalized confidence (0.67), self-consistency (0.82), and CCS
(
Burns et al., 2023
)
(0.72).
The signal is present from the very first reasoning step (0.79 AUROC), before any error appears in text (§
3
).
Act II: The model conceals what it knows.
Wrong traces express confidence of 4.55/5 (correct: 4.87/5).
A text classifier on the same first step achieves only 0.59 AUROC—a 0.20 gap confirming genuine concealment.
Fully 65% of wrong traces fall in an
unfaithful region
: high confidence
and
high internal error score (§
4
).
Act III: The signal cannot fix the errors it detects.
Four intervention strategies all fail (§
5
).
Activation patching of correct hidden states into wrong traces destroys output coherence (accuracy
→
0
%
\to 0\%
), revealing that the error signal is a
diagnostic readout, not a causal lever
—in stark contrast to factual knowledge representations
(
Meng et al., 2022
)
, which can be localized and edited.
Contributions.
(1) We identify
hidden error awareness
—a 0.20 AUROC gap between hidden-state and text-surface detection—robust across 9 models (1.5B–72B), three families, and RL-trained reasoning models.
(2) We establish the
diagnostic–causal distinction
via four interventions, demonstrating that error signals occupy a fundamentally different role than factual knowledge representations.
(3) We characterize two temporal regimes of error encoding (
front-loaded
vs.
accumulating
), providing mechanistic insight into how models commit to flawed trajectories.
Figure 1:
Overview.
(1. Hidden State Probing)
A linear probe achieves 0.95 AUROC; verbalized confidence is uninformative.
(2. Textual Indistinguishability)
First-step probe (0.79) vs. text classifier (0.59): a 0.20 gap invisible on the surface.
(3. Intervention Failure)
Four interventions fail; the signal is diagnostic, not causal.
2
Related Work
CoT faithfulness.
Turpin et al. (2023)
show that CoT explanations can be steered by irrelevant features, and
Lanham et al. (2023)
find that perturbing CoT steps often does not change the answer.
These studies diagnose unfaithfulness via
behavioral
interventions.
We provide a complementary
representational
perspective: directly comparing what hidden states encode with what the text expresses, and quantifying the gap.
Probing internal representations.
Burns et al. (2023)
discover “truth directions” via unsupervised CCS;
Azaria and Mitchell (2023)
train classifiers to detect falsehoods;
Li et al. (2023)
use probes for inference-time intervention.
Concurrent work by
Zhang et al. (2025)
probes hidden states in reasoning models for self-verification, demonstrating best-of-N selection.
Our work reaches a fundamentally different conclusion: where they show the signal aids
selection
, we show it cannot improve
the reasoning itself
.
We further establish a 0.20 AUROC gap between hidden-state and text-surface classifiers that verification-focused work does not measure.
Self-correction and causal analysis.
Huang et al. (2024)
find that intrinsic self-correction remains limited.
Our activation patching experiments extend causal mediation analysis
(
Meng et al., 2022
;
Vig et al., 2020
)
from factual recall to multi-step reasoning, revealing that the causal structure of error representations differs qualitatively from that of factual associations.
3
The Error Signal Exists
3.1
Method
Given a model
ℳ
\mathcal{M}
with
L
L
layers, we extract the hidden state
𝐡
T
(
l
)
∈
ℝ
d
\mathbf{h}^{(l)}_{T}\in\mathbb{R}^{d}
at layer
l
l
and the last token position
T
T
of a complete CoT trace.
We train a logistic regression probe:
p
⁡
(
error
∣
𝐡
)
=
σ
⁡
(
𝐰
⊤
​
𝐡
+
b
)
p(\text{error}\mid\mathbf{h})=\sigma(\mathbf{w}^{\top}\mathbf{h}+b)
(1)
where
𝐡
\mathbf{h}
is standardized (zero mean, unit variance per dimension) and the label
y
=
1
y=1
if the trace reaches an incorrect answer.
The training objective is regularized log-likelihood:
ℒ
=
−
1
N
∑
i
=
1
N
[
y
i
log
p
^
i
+
(
1
−
y
i
)
log
(
1
−
p
^
i
)
]
+
1
2
​
C
∥
𝐰
∥
2
\mathcal{L}=-\frac{1}{N}\sum_{i=1}^{N}\left[y_{i}\log\hat{p}_{i}+(1{-}y_{i})\log(1{-}\hat{p}_{i})\right]+\frac{1}{2C}\|\mathbf{w}\|^{2}
(2)
with
C
=
0.1
C=0.1
.
Training uses 100 MATH-500 problems
(
Hendrycks et al., 2021
)
, disjoint from all evaluation sets.
We select the best layer by 5-fold cross-validated AUROC; no other hyperparameters are tuned.
Algorithm
1
summarizes the full pipeline.
Algorithm 1
Hidden Error Awareness Probe
0:
Model
ℳ
\mathcal{M}
, training set
𝒟
train
\mathcal{D}_{\text{train}}
, candidate layers
ℒ
\mathcal{L}
0:
Best probe
(
f
∗
,
l
∗
)
(f^{*},l^{*})
1:
for
each problem
x
i
∈
𝒟
train
x_{i}\in\mathcal{D}_{\text{train}}
do
2:
r
i
←
GenerateCoT
​
(
ℳ
,
x
i
)
r_{i}\leftarrow\text{GenerateCoT}(\mathcal{M},x_{i})
// greedy
3:
y
i
←
𝟏
[
answer
(
r
i
)
≠
ref
(
x
i
)
]
y_{i}\leftarrow\mathbf{1}[\text{answer}(r_{i})\neq\text{ref}(x_{i})]
4:
for
each layer
l
∈
ℒ
l\in\mathcal{L}
do
5:
𝐡
i
(
l
)
←
ExtractHidden
​
(
ℳ
,
x
i
⊕
r
i
,
l
)
\mathbf{h}^{(l)}_{i}\leftarrow\text{ExtractHidden}(\mathcal{M},x_{i}\oplus r_{i},l)
6:
end
for
7:
end
for
8:
for
each layer
l
∈
ℒ
l\in\mathcal{L}
do
9:
𝐗
(
l
)
←
Standardize
​
(
[
𝐡
1
(
l
)
,
…
,
𝐡
N
(
l
)
]
)
\mathbf{X}^{(l)}\leftarrow\text{Standardize}([\mathbf{h}^{(l)}_{1},\ldots,\mathbf{h}^{(l)}_{N}])
10:
a
l
←
CV-AUROC
​
(
LogReg
​
(
𝐗
(
l
)
,
𝐲
)
,
k
=
5
)
a_{l}\leftarrow\text{CV-AUROC}(\text{LogReg}(\mathbf{X}^{(l)},\mathbf{y}),k{=}5)
11:
end
for
12:
l
∗
←
arg
⁡
max
l
⁡
a
l
l^{*}\leftarrow\arg\max_{l}a_{l}
13:
f
∗
←
LogReg
​
(
𝐗
(
l
∗
)
,
𝐲
)
f^{*}\leftarrow\text{LogReg}(\mathbf{X}^{(l^{*})},\mathbf{y})
// fit on all data
14:
return
(
f
∗
,
l
∗
)
(f^{*},l^{*})
3.2
Results across models and scales
Table
1
shows that the probe achieves
>
>
0.9 AUROC for five of nine models—including at 72B scale (0.977).
The signal is weaker at intermediate scales (7B: 0.669, 14B: 0.762) but recovers at 32B and 72B, suggesting the dip reflects training dynamics rather than a scaling limitation (§
7
).
The RL-distilled reasoning model DeepSeek-R1-7B also shows strong hidden error awareness (0.852), despite 76% base accuracy.
Model
Type
Acc
Lyr
CV
Eval
Qwen2.5-1.5B
std
.35
27
.918
.724
Qwen2.5-3B
std
.53
27
.953
.956
Phi-3.5-mini
std
.39
8
.936
–
Qwen2.5-7B
std
.62
16
.669
.737
Llama-3.1-8B
std
.46
16
.703
.811
Qwen2.5-14B
std
.65
39
.762
–
Qwen2.5-32B
std
.53
32
.956
–
Qwen2.5-72B
std
.41
64
.977
–
DS-R1-7B
reas.
.76
12
.884
.852
Table 1:
Probe error detection. CV: 5-fold cross-validated AUROC on 100 training problems; Eval: held-out AUROC on 200 separate problems. DS-R1-7B = DeepSeek-R1-Distill-Qwen-7B (RL-distilled reasoning model).
Comparison with baselines.
Table
2
compares the probe against established detection methods on 200 held-out problems.
The probe outperforms all baselines at minimal cost, including self-consistency (5
×
\times
generation cost) and CCS (same hidden states, unsupervised).
The signal is linearly encoded: a linear probe (0.955) matches an MLP (0.944) and exceeds a random forest (0.893).
It is also data-efficient: 20 training problems yield 0.956 AUROC.
Method
AUROC
Cost
Hidden State Probe (ours)
0.953
1 fwd pass
Self-Consistency (
N
N
=5)
0.823
5
×
\times
gen
CCS
(
Burns et al., 2023
)
0.718
1 fwd pass
P
P
(
True
)
0.721
1 query
Verbalized Confidence
0.674
1 query
Sequence Log-prob
0.676
free
Table 2:
Error detection baselines (Qwen2.5-3B,
n
n
=200).
Difficulty control.
A key concern is confounding with problem difficulty.
For 50 problems, we generate 5 traces each (temperature
=
0.7
=0.7
) and compare probe scores for correct vs. wrong traces
on the same problem
(Table
3
).
Wrong traces score significantly higher (
p
<
0.05
p<0.05
,
d
=
0.55
d=0.55
–
0.83
0.83
), confirming trace-level detection.
Model
Mixed
Correct
Wrong
d
d
Qwen2.5-3B
18
0.278
0.481
0.55
Qwen2.5-7B
13
0.154
0.391
0.63
Qwen2.5-14B
18
0.454
0.502
0.13
Llama-3.1-8B
24
0.363
0.561
0.69
Table 3:
Within-problem difficulty control. Mixed = problems with both correct and wrong traces;
d
d
= Cohen’s
d
d
.
Layer analysis.
Figure
2
shows the error signal concentrates in the upper layers (70–85% depth), suggesting encoding in abstract, higher-level representations rather than early syntactic processing.
Figure 2:
Probe AUROC across layers. The error signal peaks in the upper third of the network across all model families.
4
The Signal Is Early and Hidden
4.1
First-step prediction
The first-step hidden state alone achieves 0.787 AUROC—98% of full-trace performance (Table
4
).
For DS-R1-7B, first-step AUROC is 0.686, still well above chance.
The model “knows” from Step 1 whether its reasoning will succeed, yet proceeds to generate multiple incorrect steps.
Hidden State Used
AUROC
95% CI
First step only
0.787
[0.634, 0.840]
Last step only
0.754
–
Max score across steps
0.800
[0.696, 0.883]
Mean score across steps
0.827
–
Full trace (last token)
0.800
–
Table 4:
AUROC from different trace positions (Qwen2.5-3B,
n
n
=89). The first step captures 98% of full-trace performance.
Two temporal regimes.
Step-level probe scores (Figure
3
) reveal distinct dynamics.
Qwen2.5-3B shows
front-loaded
awareness: maximum separation at Step 1 (gap = 0.41), suggesting early commitment to a flawed trajectory.
Qwen2.5-7B shows
accumulating
awareness: separation grows from 0.11 to 0.38 as error evidence builds.
Neither pattern is consistent with the probe merely reading post-hoc text quality.
Figure 3:
Step-level probe trajectories. 3B (left): front-loaded—the model commits early. 7B (right): accumulating—error signals build through the trace.
4.2
Textual indistinguishability
If the signal is in hidden states, is it also in the text?
We formalize this with a
textual indistinguishability test
: train a TF-IDF + logistic regression classifier on first-step
text
and compare with the hidden-state probe.
Let
s
text
s_{\text{text}}
and
s
hidden
s_{\text{hidden}}
denote the AUROC of the text and hidden-state classifiers, respectively. We define the
concealment gap
:
Δ
conceal
=
s
hidden
−
s
text
\Delta_{\text{conceal}}=s_{\text{hidden}}-s_{\text{text}}
(3)
A positive
Δ
conceal
\Delta_{\text{conceal}}
indicates information present in hidden states but absent from text.
Table
5
:
Δ
conceal
=
0.197
\Delta_{\text{conceal}}=0.197
, with no significant surface differences (length
p
=
0.211
p=0.211
, number density
p
=
0.726
p=0.726
,
<
<
1% hedging).
Signal
AUROC
p
p
-value
TF-IDF + LR (text)
0.590
–
Hidden-state probe
0.787
–
Surface statistics (correct vs. wrong):
Length (tokens)
–
p
=
0.211
p=0.211
Number density
–
p
=
0.726
p=0.726
Hedging language
0% vs. 1%
–
Vocab. Jaccard
0.322
–
Table 5:
Textual indistinguishability (Qwen2.5-3B,
n
n
=200).
Δ
conceal
=
0.197
\Delta_{\text{conceal}}=0.197
.
4.3
The unfaithful region
We define a trace as
unfaithful
when it simultaneously exhibits high verbalized confidence (
≥
4
\geq 4
) and high probe error score (
>
0.5
>0.5
).
Fully 65% of wrong traces fall in this region.
Figure
4
visualizes the separation: probe scores cleanly distinguish correct from wrong traces, while verbalized confidence does not.
Figure 4:
Probe score distributions for correct (green) vs. wrong (red) traces. The distributions are well-separated in hidden-state space despite near-identical verbalized confidence (4.87 vs. 4.55 out of 5).
5
The Signal Cannot Fix What It Detects
If models internally detect errors, can we leverage this for self-improvement?
We test four strategies spanning the intervention spectrum and find that
none meaningfully improve accuracy
.
5.1
Activation steering
Following
Zou et al. (2023)
, we define the
error direction
𝐰
^
=
𝐰
/
‖
𝐰
‖
\hat{\mathbf{w}}=\mathbf{w}/\|\mathbf{w}\|
from the probe weight vector and subtract it during generation:
𝐡
′
=
𝐡
−
α
⋅
(
𝐡
⋅
𝐰
^
)
⋅
𝐰
^
\mathbf{h}^{\prime}=\mathbf{h}-\alpha\cdot(\mathbf{h}\cdot\hat{\mathbf{w}})\cdot\hat{\mathbf{w}}
(4)
The intuition: if error is a direction in representation space, removing it should yield “correct reasoning.”
Table
6
: at most
+
4
%
+4\%
improvement; aggressive steering (
α
=
8
\alpha=8
) degrades the 3B model by
−
6
%
-6\%
.
The error direction and the “correct reasoning” direction are not opposites.
3B
7B
α
\alpha
Acc
Δ
\Delta
Acc
Δ
\Delta
0
.53
–
.60
–
0.5
.56
+.03
.60
.00
1.0
.55
+.02
.61
+.01
2.0
.55
+.02
.62
+.02
5.0
.56
+.03
.60
.00
8.0
.47
−
.06
-.06
.64
+.04
Table 6:
Activation steering. Gains are modest; aggressive steering degrades the smaller model.
5.2
Probe-guided best-of-N
We generate
N
N
traces (temperature
=
0.7
=0.7
) and select by lowest probe score:
r
∗
=
arg
⁡
min
r
∈
{
r
1
,
…
,
r
N
}
​
f
∗
​
(
r
)
r^{*}=\arg\min_{r\in\{r_{1},\ldots,r_{N}\}}f^{*}(r)
(5)
Table
7
: probe selection matches random and substantially underperforms majority vote.
The oracle upper bound (88–91% at
N
N
=12) confirms correct traces exist—the bottleneck is selection quality.
N
N
Greedy
Random
MV
Probe
Oracle
Qwen2.5-3B
3
.60
.59
.63
.58
.73
8
.60
.60
.67
.63
.84
12
.60
.56
.75
.62
.88
Qwen2.5-7B
3
.70
.71
.71
.71
.84
8
.70
.70
.76
.73
.91
12
.70
.72
.75
.70
.91
Table 7:
Probe-guided best-of-N. MV = majority vote. Despite large oracle headroom, the probe cannot outperform majority vote.
5.3
Self-correction
We use the probe to flag likely errors (
f
∗
​
(
r
)
>
τ
f^{*}(r)>\tau
), then prompt the model to revise.
Table
8
: retry
hurts
accuracy (
−
3
%
-3\%
).
Even oracle-triggered correction gains only
+
1
%
+1\%
.
The model generates its correction using the same flawed computation that produced the original error.
Strategy
3B
7B
Greedy (no retry)
0.60
0.70
Always retry
0.57 (
−
3
%
-3\%
)
0.67 (
−
3
%
-3\%
)
Best-of-two (probe)
0.60
0.70
Oracle-triggered
0.61 (
+
1
%
+1\%
)
0.71 (
+
1
%
+1\%
)
Table 8:
Self-correction. Retry degrades accuracy; even an oracle trigger gains only
+
1
%
+1\%
.
5.4
Activation patching: the causal test
The strongest test of causality.
For mixed-outcome problems, we extract hidden states from a correct trace and patch them into a new generation:
𝐡
wrong
′
=
(
1
−
α
)
​
𝐡
wrong
+
α
​
𝐡
correct
\mathbf{h}^{\prime}_{\text{wrong}}=(1{-}\alpha)\,\mathbf{h}_{\text{wrong}}+\alpha\,\mathbf{h}_{\text{correct}}
(6)
If the error signal is causal, patching should improve accuracy.
Table
9
: it does not.
At
α
=
0.5
\alpha=0.5
, 3B accuracy drops to 0%—the patched states are incompatible with surrounding computation.
Patching Method
3B
7B
Baseline (no patch)
0.65
0.33
Replace with correct HS
0.35
0.33
Blend (
α
\alpha
=0.3)
0.52
0.20
Blend (
α
\alpha
=0.5)
0.00
0.07
Subtract error (
α
\alpha
=0.5)
0.65
0.47
Subtract error (
α
\alpha
=2.0)
0.61
0.47
Table 9:
Activation patching on mixed-outcome problems. Replacing or blending destroys accuracy; the error direction is not a causal lever.
These four experiments converge on a single conclusion: the error signal is a
diagnostic readout
—a summary statistic of computation quality—not a causal component that can be edited to redirect reasoning.
Figure
5
summarizes the results.
Figure 5:
Intervention summary. (a) Steering: marginal gains, degradation at high
α
\alpha
. (b) Best-of-N: probe underperforms majority vote despite large oracle headroom. (c) Self-correction: retry hurts both models.
6
Does RL Training Close the Gap?
DeepSeek-R1-Distill-Qwen-7B achieves 76% accuracy (vs. 46% for Llama-3.1-8B) but still exhibits 0.852 AUROC hidden error awareness (Table
1
).
Its first-step AUROC (0.686) is lower than Qwen-3B’s (0.787), consistent with reasoning models distributing computation across longer traces.
The difficulty control effect is weaker (
p
=
0.447
p=0.447
,
d
=
−
0.30
d=-0.30
), likely because 76% accuracy leaves too few mixed-outcome problems (
n
n
=14).
But the core finding stands:
RL training does not close the diagnostic–causal gap
.
7
Discussion
Why diagnostic but not causal?
The thermometer analogy: a thermometer reads body temperature but cannot cure fever.
The probe reads computation quality but cannot redirect reasoning.
Patching provides the strongest evidence: transplanting hidden states from correct traces does not produce correct reasoning—it produces incoherent output.
Reasoning quality emerges from distributed, multi-layer computation, not from a single editable feature.
Contrast with factual editing.
Meng et al. (2022)
and
Li et al. (2023)
edit localized representations to reliably change outputs.
Error signals during reasoning are different: they are
epiphenomenal readouts
of a distributed process.
The tools that work for factual knowledge (ROME, ITI) should not be expected to work for reasoning quality.
Non-monotonic scaling.
The 7B/14B AUROC dip followed by recovery at 32B/72B suggests a
capability–separability trade-off
: intermediate models produce fewer but less systematic errors, creating harder linear separation.
Larger models develop more linearly structured error representations—the 72B achieves 0.977 AUROC despite lower raw accuracy.
Implications.
(1) CoT trace auditing is unreliable for safety monitoring: error signals are invisible in text.
(2) Self-correction needs mechanistic grounding beyond surface prompting.
(3) Process reward models
(
Lightman et al., 2024
)
may capture the same diagnostic signal but lack causal leverage.
Limitations.
We test up to 72B across three families plus one reasoning model, using MATH-500 as the primary benchmark.
We do not test fine-tuning on probe signals or RL from probe feedback, which could potentially close the gap through training-time intervention.
8
Conclusion
LLMs encode error-predictive signals in their hidden states during CoT reasoning—signals that emerge early, are concealed from text, and persist across model families and scales.
Four mechanistic interventions fail to leverage these signals, establishing that they are diagnostic rather than causal.
This reveals a boundary: mechanistic interpretability can detect reasoning failures but cannot fix them with the tools that succeed for factual knowledge.
Closing this gap likely requires training objectives that teach models to
act on
their internal error signals, not merely harbor them.
References
Azaria and Mitchell (2023)
A. Azaria and T. Mitchell
The internal state of an LLM knows when it’s lying
.
Findings of EMNLP
.
Cited by:
§2
.
Burns
et al.
(2023)
C. Burns, H. Ye, D. Klein, and J. Steinhardt
Discovering latent knowledge in language models without supervision
.
International Conference on Learning Representations
.
Cited by:
§1
,
§2
,
Table 2
.
Clark
et al.
(2018)
P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord
Think you have solved question answering? Try ARC, the AI2 reasoning challenge
.
arXiv preprint arXiv:1803.05457
.
Cited by:
Appendix G
.
Hendrycks
et al.
(2021)
D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
Measuring mathematical problem solving with the MATH dataset
.
NeurIPS Datasets and Benchmarks Track
.
Cited by:
§3.1
.
Huang
et al.
(2024)
J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou
Large language models cannot self-correct reasoning yet
.
International Conference on Learning Representations
.
Cited by:
§2
.
Lanham
et al.
(2023)
T. Lanham, A. Chen, A. Radhakrishnan, B. Steiner, C. Denison, D. Hernandez, D. Li, E. Durmus, E. Hubinger, J. Kernion,
et al.
Measuring faithfulness in chain-of-thought reasoning
.
arXiv preprint arXiv:2307.13702
.
Cited by:
§1
,
§2
.
Li
et al.
(2023)
K. Li, O. Patel, F. Viégas, H. Pfister, and M. Wattenberg
Inference-time intervention: eliciting truthful answers from a language model
.
Advances in Neural Information Processing Systems
36
.
Cited by:
§2
,
§7
.
Lightman
et al.
(2024)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and C. Szegedy
Let’s verify step by step
.
International Conference on Learning Representations
.
Cited by:
§7
.
Meng
et al.
(2022)
K. Meng, D. Bau, A. Andonian, and Y. Belinkov
Locating and editing factual associations in GPT
.
Advances in Neural Information Processing Systems
35
,
pp. 17359–17372
.
Cited by:
§1
,
§2
,
§7
.
Turpin
et al.
(2023)
M. Turpin, J. Michael, E. Perez, and S. Bowman
Language models don’t always say what they think: unfaithful explanations in chain-of-thought prompting
.
Advances in Neural Information Processing Systems
36
.
Cited by:
§1
,
§2
.
Vig
et al.
(2020)
J. Vig, S. Gehrmann, Y. Belinkov, S. Qian, D. Nevo, Y. Singer, and S. Shieber
Investigating gender bias in language models using causal mediation analysis
.
In
Advances in Neural Information Processing Systems
,
Vol.
33
,
pp. 12388–12401
.
Cited by:
§2
.
Wei
et al.
(2022)
J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, and D. Zhou
Chain-of-thought prompting elicits reasoning in large language models
.
Advances in Neural Information Processing Systems
35
,
pp. 24824–24837
.
Cited by:
§1
.
Zhang
et al.
(2025)
A. Zhang, Y. Chen, J. Pan,
et al.
Reasoning models know when they’re right: probing hidden states for self-verification
.
arXiv preprint arXiv:2504.05419
.
Cited by:
§2
.
Zou
et al.
(2023)
A. Zou, L. Phan, S. Chen, J. Campbell, P. Guo, R. Ren, A. Pan, X. Yin, M. Mazeika, A. Dombrowski,
et al.
Representation engineering: a top-down approach to AI transparency
.
arXiv preprint arXiv:2310.01405
.
Cited by:
§5.1
.
Appendix A
Prompt Templates
All models use the following prompts, wrapped in each model’s chat template.
CoT Generation
Solve the following math problem step by step.
Number each step as ‘Step 1:’, ‘Step 2:’, etc.
End with ‘ANSWER: <your final answer>’.
Problem: {problem}
Solution:
Verbalized Confidence
Rate your confidence in the above answer on a scale from 1 (very uncertain) to 5 (very confident). Reply with just the number.
Self-Correction
Review your solution carefully. If you find any errors, correct them. Provide your final answer after ‘ANSWER:’.
External Verifier (GPT-4o-mini)
Solve this math problem step by step. End with ‘ANSWER: <your final answer>’.
Problem: {problem}
Appendix B
Probe Training Code
Core probe training and hidden state extraction (simplified from our full pipeline):
⬇
#
---
Hidden
state
extraction
---
def
extract_hidden
(
model
,
tokenizer
,
text
,
layer
):
inputs
=
tokenizer
(
text
,
return_tensors
=
"pt"
)
with
torch
.
no_grad
():
out
=
model
(**
inputs
,
output_hidden_states
=
True
)
#
Last
token
of
the
specified
layer
return
out
.
hidden_states
[
layer
][0,
-1].
cpu
()
#
---
Probe
training
---
def
train_probe
(
hidden_states
,
labels
,
C
=0.1):
best_auroc
,
best_layer
=
0,
None
for
layer
,
vecs
in
hidden_states
.
items
():
X
=
np
.
stack
(
vecs
)
scaler
=
StandardScaler
()
X_s
=
scaler
.
fit_transform
(
X
)
clf
=
LogisticRegression
(
C
=
C
,
max_iter
=2000)
scores
=
cross_val_score
(
clf
,
X_s
,
labels
,
cv
=5,
scoring
=
’roc_auc’
)
if
scores
.
mean
()
>
best_auroc
:
best_auroc
=
scores
.
mean
()
best_layer
=
layer
best_clf
=
clf
.
fit
(
X_s
,
labels
)
best_scaler
=
scaler
return
best_clf
,
best_scaler
,
best_layer
#
---
Activation
steering
---
def
steer
(
h
,
w
,
alpha
):
""
"Subtract
error
direction
from
h."
""
w_hat
=
w
/
np
.
linalg
.
norm
(
w
)
return
h
-
alpha
*
np
.
dot
(
h
,
w_hat
)
*
w_hat
#
---
Activation
patching
---
def
patch
(
h_wrong
,
h_correct
,
alpha
):
""
"Blend
correct
hidden
states
into
wrong."
""
return
(1
-
alpha
)
*
h_wrong
+
\
alpha
*
h_correct
Appendix C
Hyperparameters
Parameter
Value
Probe classifier
Logistic Regression
Regularization (
C
C
)
0.1 (
L
2
L_{2}
)
Max iterations
2000
Feature scaling
StandardScaler (per-dim)
CV strategy
5-fold stratified
Training set
100 MATH-500 problems
Evaluation set
200 MATH-500 problems
Generation
Greedy (temp=0)
Max new tokens
512 (CoT), 1024 (full)
Hidden state position
Last token of trace
Best-of-N temperature
0.7
Best-of-N top-
p
p
0.95
Steering
α
\alpha
range
0.5, 1.0, 2.0, 5.0, 8.0
Patching
α
\alpha
range
0.3, 0.5 (blend); 0.5, 2.0 (sub)
External verifier
GPT-4o-mini
Routing threshold
Top-
r
r
by probe score
Table 10:
Hyperparameters across all experiments.
Appendix D
Per-Layer Probe Results
Model
Layers
Best
AUROC
Depth
Qwen2.5-1.5B
28
27
0.918
96%
Qwen2.5-3B
36
27
0.953
75%
Phi-3.5-mini
32
8
0.936
25%
Qwen2.5-7B
28
16
0.669
57%
Llama-3.1-8B
32
16
0.703
50%
Qwen2.5-14B
48
39
0.762
81%
Qwen2.5-32B
64
32
0.956
50%
Qwen2.5-72B
80
64
0.977
80%
DS-R1-7B
28
12
0.884
43%
Table 11:
Best probe layer by model. Depth = best layer / total layers.
Appendix E
Ablation Studies
Probe architecture.
We compare probe architectures on Qwen2.5-3B (layer 27,
n
n
=100):
Classifier
CV AUROC
Logistic Regression
0.955
2-layer MLP (256 hidden)
0.944
Random Forest (100 trees)
0.893
Table 12:
Probe architecture comparison. Linear probes match or exceed nonlinear alternatives, confirming the signal is linearly encoded.
Training set size.
Probe AUROC as a function of training set size (Qwen2.5-3B):
Training problems
CV AUROC
10
0.917
20
0.956
50
0.949
100
0.953
Table 13:
Data efficiency. 20 problems suffice for near-peak performance.
Appendix F
Example Traces
Two representative traces from Qwen2.5-3B on MATH-500, illustrating hidden error awareness.
The correct trace receives a low probe score; the wrong trace receives a high probe score
and
high verbalized confidence (the unfaithful region).
Correct trace
— Probe score: 0.004, Confidence: 5/5
Problem:
One ticket to a show costs $20 at full price. Susan buys 4 tickets with a 25% discount. Pam buys 5 tickets with a 30% discount. How many more dollars did Pam pay than Susan?
Step 1: Susan’s discounted price = $20
×
\times
0.75 = $15
Step 2: Susan’s total = 4
×
\times
$15 = $60
Step 3: Pam’s discounted price = $20
×
\times
0.70 = $14
Step 4: Pam’s total = 5
×
\times
$14 = $70
Step 5: Difference = $70
−
-
$60 = $10
ANSWER: $10
Correct
(ref: 10)
Wrong trace
— Probe score: 0.932, Confidence: 5/5
Problem:
A farmer has 52 cows. Each cow gives 5 liters of milk per day. How many liters of milk does the farmer collect in a week?
Step 1: Daily milk = 52
×
\times
5 = 260 liters
Step 2: Weekly milk = 260
×
\times
30 = 7800 liters
ANSWER: 7800
Wrong
(ref: 1820, i.e. 260
×
\times
7)
The wrong trace uses “30” instead of “7” for days in a week—a clear arithmetic error—yet the model expresses 5/5 verbalized confidence.
The probe detects the error (score 0.932) from hidden states alone.
No hedging, uncertainty markers, or surface-level cues distinguish this trace from a correct one.
This is the defining pattern of
hidden error awareness
: the model knows it is wrong but does not say so.
Appendix G
Cross-Domain Generalization
To test whether error detection extends beyond mathematics, we evaluate on ARC-Challenge
(
Clark et al., 2018
)
(commonsense reasoning).
Domain
Setting
3B
7B
ARC
Native CV
0.63
0.65
ARC
Native eval
0.54
0.69
ARC
MATH
→
\to
ARC
0.54
0.55
Table 14:
Cross-domain probe AUROC on ARC-Challenge. Native probes achieve above-chance detection; cross-domain transfer from MATH is weaker, suggesting domain-specific error directions.
Native ARC probes achieve 0.63–0.69 AUROC, confirming hidden error awareness extends to commonsense reasoning.
Cross-domain transfer (MATH-trained probe applied to ARC) is weaker (0.54–0.55), indicating that error signals occupy
different directions
in representation space across domains—a finding consistent with domain-specific feature encoding.