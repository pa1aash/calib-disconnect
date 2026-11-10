---
title: 'Wired for Overconfidence: A Mechanistic Perspective on Inflated Verbalized
  Confidence in LLMs (full text)'
id: wired-for-overconfidence-a-mechanistic-perspective-on-inflated-verbalized-confid
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
created: '2026-11-09T23:10:54.453711Z'
updated: '2026-11-09T23:27:44.668546Z'
source: https://arxiv.org/pdf/2604.01457
status: review
type: note
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv 2604.01457 v3, COLM 2026, Zhao et al., UVA). Circuit-level
  causal analysis of inflated verbalized confidence (0-99) in Qwen2.5-3B-Instruct
  and Llama-3.2-3B-Instruct on PopQA, NQOpen, MMLU: TSLD proxy, edge attribution patching,
  74-79% completeness drop (Table 2), steering/ablation cuts ECE (e.g. 0.647 to 0.068
  on Qwen2.5-7B PopQA). Factual QA only, instruct models only, no code, no execution
  labels, no probe-vs-verbal comparison. CLOSE for L2 causal-intervention component
  outside code.'
---

Published as a conference paper at COLM 2026

Wired for Overconfidence: A Mechanistic Perspective on Inflated Verbalized Confidence in LLMs
Tianyi Zhao, Yinhan He, Wendy Zheng, Yujie Zhang, Chen Chen
University of Virginia
{abs4dj,nee7ne,ncd9cf,qrk9jt,zrh6du}@virginia.edu

arXiv:2604.01457v3 [cs.CL] 27 Jul 2026

Abstract
Large language models are often not just wrong, but confidently wrong: when
they produce factually incorrect answers, they tend to verbalize overly high
confidence rather than signal uncertainty. Such verbalized overconfidence
can mislead users and weaken confidence scores as a reliable uncertainty
signal, yet its internal mechanisms remain poorly understood. We present
a circuit-level mechanistic analysis of this inflated verbalized confidence in
LLMs, organized around three axes: capturing verbalized confidence as a
differentiable internal signal, identifying the circuits that causally inflate
it, and leveraging these insights for targeted inference-time recalibration.
Across two instruction-tuned LLMs on three datasets, we find that a compact set of MLP blocks and attention heads, concentrated in middle-to-late
layers, consistently writes the confidence-inflation signal at the final token position. We further show that targeted inference-time interventions
on these circuits substantially improve calibration. Together, our results
suggest that verbalized overconfidence in LLMs is driven by identifiable
internal circuits and can be mitigated through targeted intervention.

1

Introduction

Large language models are increasingly deployed in high-stakes settings, where an incorrect answer delivered with unwarranted certainty can cause real harm. When asked to
self-assess, these models are not merely wrong; they are often confidently wrong, systematically producing inflated verbalized confidence scores that fail to distinguish reliable
answers from unreliable ones (see Figure 6). Although prior work indicates that LLMs can
express their own uncertainty (Kadavath et al., 2022; Xiong et al., 2023; Lin et al., 2022), their
verbalized confidence remains poorly calibrated to factual accuracy (Ji et al., 2025). Meanwhile, the broader calibration literature has mostly treated this as an output-level symptom,
emphasizing post-hoc correction rather than understanding the internal mechanisms. A
fundamental question therefore remains: what specific internal mechanisms causally drive this
inflated verbalized confidence, and can they be intervened upon to recalibrate the model?
Mechanistic interpretability (Rai et al., 2024; Conmy et al., 2023) offers a natural framework
for answering this question, having successfully localized circuits for tasks such as name
prediction (Wang et al., 2022), mathematical reasoning (Hanna et al., 2023), and entity knowledge (Ferrando et al., 2024). We bring this lens to verbalized overconfidence, organizing
our study around three complementary challenges. First, capture: how can we represent
output-level verbalized confidence as a differentiable internal proxy? Second, discover:
given such a proxy, how can we identify and validate the internal circuits responsible
for inflated verbalized confidence? Third, mitigate: how can we convert the mechanistic
insights into practical inference-time interventions that recalibrate verbal confidence?
We study this problem under a two-step confidence elicitation setup. To address the
first challenge, we introduce the Target Set Logit Difference (TSLD), a metric that computes
the mean logit gap between predefined high-confidence and low-confidence sets. We
empirically show that TSLD reliably captures the model’s internal confidence propensity,
yielding a stable and differentiable metric compatible with subsequent gradient-based
attribution. For the second challenge, we devise a Truth-Injection Counterfactual Design for
1

Published as a conference paper at COLM 2026

Step 1 — Factual answer

Clean Input

User: "Question: What is
John Mayne's occupation?
Please provide your answer as
concisely as possible.
Example: {\"answer\":
\"Paris\"}"
Assistant: "{\"answer\":
"\architect\"}"

User: What is John Mayne's occupation?
Assistant: architect (Incorrect Answer
Predicted by the Model)
User: Now, evaluate
your previous answer. How confident are
you that your answer is factually
correct? Your response must be an
integer from 0 to 99.
Assistant: [Model predicts confidence
here]

Step 2 — Self-evaluation
User: "Now, evaluate your
previous answer. How confident
are you that your answer is
factually correct? The
confidence value must be an
integer from 0 to 99. Do not
explain, just provide the
confidence score. Example: 65"

[model outputs: e.g., "85"]

Corrupted Input
User: What is John Mayne's occupation?
Assistant: journalist (Forced Ground
Truth Replacement)
User: Now, evaluate
your previous answer. How confident are
you that your answer is factually
correct? Your response must be an
integer from 0 to 99.
Assistant: [Model predicts confidence
here]

Figure 1: Left: Two-step elicitation. The model answers a factual question, then self-reports
confidence as an integer (0–99). Center: Truth-injection counterfactual design. For each
confidently-wrong record, the clean prompt retains the model’s incorrect answer, while the
corrupted prompt substitutes the ground truth, keeping all other tokens identical. Right:
∆TSLD distributions and ∆TSLD vs. ∆confidence scatter plots for Qwen2.5-3B (top) and
Llama-3.2-3B (bottom) on PopQA.
constructing clean and corrupted pairs. By using ∆TSLD as the stratification criterion, we
partition the data to isolate cases in which truth injection suppresses the inflated confidence.
We then apply Edge Attribution Patching with Integrated Gradients (Hanna et al., 2024) to
discover internal circuits that causally mediate the overconfidence signal, and validate them
at both the edge and component levels. Finally, we intervene on a small set of top-ranked
components identified as drivers of overconfidence in LLMs. Specifically, we study two
intervention strategies, mean ablation and activation steering, applied during confidence
inference, and evaluate calibration performance over the full dataset.
Across two models and three factual QA benchmarks, we find that a compact set of MLP
blocks and attention heads, primarily in the middle-to-late layers, consistently write the
confidence-inflation signal at the final token position. The strong cross-dataset conservation
of the identified circuits indicates that verbalized overconfidence is driven by a stable modelinternal mechanism rather than a task-specific artifact. Intervening on these components
substantially improves model calibration with respect to verbalized confidence, establishing
mechanistic recalibration as a viable complement to post-hoc calibration methods.

2

From Verbal Confidence to Internal Signals

Models, Datasets, and Confidence Elicitation Setup. We conduct experiments on Qwen2.53B-Instruct (Team, 2024) and Llama-3.2-3B-Instruct (Grattafiori et al., 2024) across three
factual QA benchmarks: PopQA (Mallen et al., 2022), MMLU (Hendrycks et al., 2021), and
NQOpen (Lee et al., 2019)1 . Verbalized confidence is elicited through a two-step setup
(Figure 1, left): the model first answers the question, then reports a confidence score (0–99)
for its own answer. This separation isolates confidence verbalization as a distinct stage of
computation, allowing us to trace it to internal activations during the Step 2 forward pass.
Truth-Injection Counterfactual Design. For each incorrect record, we construct a corrupted
prompt by replacing the Step 1 assistant turn with the ground-truth answer, keeping all
other tokens identical (Figure 1, center). This yields a counterfactual pair ( xclean , xcorrupt )
and isolates the causal effect of answer correctness on subsequent confidence generation.
We use the ground truth, rather than a random or out-of-vocabulary token, as the corrupted
answer to keep both prompts on the natural data manifold; injecting meaningless tokens
might contaminate the activation differences with distributional-anomaly signals unrelated
to confidence processing.
1 See model and dataset details in Appendix A

2

PopQA

0

4

8
12

3

20
24

Layer

8
12
16
20

2

24

2

28

28

1

32

Head / MLP

1

32

0

0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 MLP

Head / MLP

1
0

2
3

8

12

16

16

24

24

0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23MLP

Head / MLP

0.50
0.25
0.00

0.25

0

0.50

4

0.75
1.00

8

12

20

0.75

28

Head / MLP

8

20

1.00

24

0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 MLP

2

4

20

0

Layer

4

16

32

1

0

Layer

Layer

4

8

16

MMLU

0

12

0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 MLP

Llama­3.2­3B­Instruct

NQOpen

4

Attribution Score

0

Layer

Layer

Qwen2.5­3B­Instruct

Published as a conference paper at COLM 2026

12

16

20

24

0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23MLP

Head / MLP

0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23MLP

Head / MLP

Figure 2: Attribution heatmaps across all six model×dataset configurations.
Target-Set Logit Difference as Metric. Unlike standard circuit analysis tasks, verbalized
confidence has no single golden token to track: it is expressed as integers spanning a
continuous range. We therefore introduce Target-Set Logit Difference (TSLD), defined as
the gap between predefined high-confidence and low-confidence sets at the confidence
prediction position:
LTSLD ( x ) =

1
1
logits[−1, c1 ] −
∑ logits[−1, c1 ] ,
|H| c∑
|L|
∈H
c∈L

(1)

where H = {70, 75, 80, 85, 90, 99} and L = {0, 10, 15, 20, 25, 30} are fixed integer sets, c1
denotes the first token of candidate c, and logits are read at the final prompt position
(POS END) in a single forward pass. TSLD captures the model’s internal preference for
high versus low confidence before decoding, while remaining fully differentiable and
thus compatible with subsequent gradient-based attribution. Here, we track the difference
Mean(H) − Mean(L), rather than Mean(H) alone, for two reasons. First, because raw
logits are unnormalized, subtracting the low-confidence mean neutralizes global shifts in
activation magnitude and captures relative confidence preference. Second, it avoids an
inhibition trap: an intervention might suppress Mean(H) simply by disrupting the model’s
generation capability, not by resolving overconfidence. A genuine confidence shift should
simultaneously decrease high-confidence logits and increase low-confidence logits, which
the difference captures directly. For a clean-corrupted pair, we further define
∆TSLD = LTSLD ( xcorrupt ) − LTSLD ( xclean )

(2)

which measures how truth injection shifts the model’s confidence propensity. As shown
in Figure 1 (right, panels B), ∆TSLD correlates strongly with the change in raw verbalized
confidence (r = 0.815 for Qwen2.5-3B, r = 0.734 for Llama-3.2-3B), indicating that TSLD
serves as a reliable internal proxy for the confidence signal of interest. We emphasize that
TSLD is a proxy for the model’s verbalized confidence, not for epistemic uncertainty; the
misalignment between the two is precisely the phenomenon under study.
Data Stratification. Incorrect records are heterogeneous in how they respond to truth
injection: some exhibit overconfident suppression (∆TSLD ≪ 0), others show truth-sensitive
increases in confidence (∆TSLD ≫ 0), still others remain near-neutral and are uninformative
(∆TSLD ≈ 0). Running attribution on this mixed set can cause gradient cancellation, as
oppositely directed response types average toward zero and obscure the circuits of interest.
To improve attribution fidelity, we therefore stratify records into three buckets, as shown in
Figure 1 (right, panels A) and Table 10. Bucket 1 forms the key discovery subset: records in
3

Published as a conference paper at COLM 2026

Qwen2.5-3B-Instruct

Llama-3.2-3B-Instruct

Rank

PopQA

MMLU

NQOpen

Rank

PopQA

MMLU

NQOpen

1
2
3
4
5
6
7
8
9
10

m30
m35
m26
m31
m25
m27
m0
m28
m24
a24.h5

m35
m30
m27
a24.h5
m24
m28
m26
m25
a27.h1
m34

m30
m35
m31
m26
m25
m27
m24
a24.h5
m28
a24.h0

1
2
3
4
5
6
7
8
9
10

a14.h3
m0
m27
a13.h18
m23
m25
m1
m2
m14
m15

m0
a14.h3
m4
m25
m2
a13.h18
m14
m23
m27
m26

a14.h3
m0
a13.h18
m4
m27
m25
m23
m3
m14
m15

Table 1: Top-10 components by attribution score. Components in blue are shared across all
three datasets. Prefix m: MLP layer; prefix a: attention head (e.g. a14.h3 = layer 14, head 3).
which the model is initially confidently wrong, but truth injection sharply suppresses that
confidence. We use this subset for subsequent attribution, since it most cleanly correlates
with the mechanism underlying inflated verbalized confidence.

3

Locate and Validate Confidence Mover Circuits

3.1

Circuit Attribution via EAP-IG

With target records selected and the computation graph (Appendix B) constructed, we
instantiate the EAP-IG framework (Appendix C) for overconfidence circuit discovery. LTSLD
(Eq. 1) defines both the discovery subset (via ∆TSLD ) and the attribution objective, aligning
sample selection with the signal being attributed and ensuring the attribution specifically
locates components responsible for the overconfidence suppression. Concretely, for each
Bucket 1 record and each edge ea→b in the computation graph, the attribution score is:
EAP-IG(ea→b ) =


1 m−1 ∂LTSLD
· outa ( xclean ) − outa ( xcorrupt ) ,
m k∑
∂
input
b x
=0

(3)

k

where xk interpolates between the corrupted and clean activations as defined in Eq. 12,
and we use m = 5 integration steps. The gradient term captures how sensitive LTSLD is to
perturbations at component b’s input; the activation difference term captures how much
component a’s output shifts between the two counterfactual conditions. We then aggregate
edge-level attributions to the component level by summing the scores of edges incident on
each node, and average the resulting component scores across all Bucket 1 examples. We
refer to the resulting subcircuit as the Confidence Mover Circuit (CMC).
Inflated verbalized confidence is localized to mid-to-late-layer components. Across all
six model×dataset settings, high attribution components are concentrated primarily in
middle-to-late layers (Figure 2; Table 1), although the attribution pattern differs across
models. Qwen2.5-3B-Instruct shows a strongly MLP-dominant circuit: the top-ranked
components are almost exclusively MLP layers in layers 24–35, with only a few attention
heads (e.g., L24H5 and L27H1) entering the top-10 on individual datasets. Llama-3.2-3BInstruct initially appears more distributed, with attention heads L14H3 and L13H18 and
several early- and mid-layer MLPs ranking highly. However, subsequent single-component
ablation (§3.2) shows that many of the early-layer MLPs (M0–M4) yield approximately
zero individual TSLD reduction, indicating that they function as relay nodes rather than
causal bottlenecks. After this causal disambiguation, the Llama circuit also concentrates
in middle-to-late layers, with M27, M25, M23, M14, L14H3, and L13H18 emerging as the
individually necessary components. Thus, despite model-specific differences in attribution
footprint, the causally validated picture is consistent across models: inflated verbalized
confidence is primarily supported by a compact set of mid-to-late-layer components.
4

2000

4000

0.6

0.2

6000

1.0

0.8

0.4
2000

4000

6000

0.6
0.4
0.2
2000

4000

Faithfulness

70%

0.6

90%

0.75

70%

0.2

0.25

Top­k Edges Retained

2000

4000

2.5

20

0.0

0

6000

10.0
7.5

Joint all­10
Baseline
Individual | TSLD|

(a) Faithfulness Curves.

60

20

0 5 6 5 4 1 5 0 7 8
M3 M3 M2L24H M2 M3 M2L24H M2 M2

Top­k Edges Retained

80

40

0.0

4

0

Joint all­10
Baseline
Individual | TSLD|

120
100
80
60

2

40
20

0

H3 27 18 14 23 25 15 M1 M2 M0
L14 ML13H M M M M

0

NQOpen + Llama­3.2­3B­Instruct

100

5.0
2.5

6

% baseline

60

NQOpen + Qwen2.5­3B­Instruct

0.50

6000

80

40

0 5 6 5 1 4 5 7 8 0
M3 M3 M2L24H M3 M2 M2 M2 M2 M

0.4

1.00
90%

0.8

5.0

PopQA + Llama­3.2­3B­Instruct
100

4

Joint all­10
Baseline
Individual | TSLD|

120
100
80
60

2

% baseline

0.2

70%

7.5

Joint all­10
Baseline
Individual | TSLD|

|TSLD Reduction|

0.4

0.8

10.0

|TSLD Reduction|

0.6

|TSLD Reduction|

70%

90%

|TSLD Reduction|

0.8

Faithfulness

Faithfulness

90%

PopQA + Qwen2.5­3B­Instruct

NQOpen

1.0

Faithfulness

PopQA

1.0

Faithfulness

Llama­3.2­3B­Instruct Qwen2.5­3B­Instruct

Published as a conference paper at COLM 2026

40
20

0

H3 27 18 25 14 23 15 M3 M0 M4
L14 ML13H M M M M

0

(b) Single-component Ablation.

Figure 3: (a) Faithfulness as a function of retained top-k edges. (b) TSLD reduction when
each of the top-10 components is individually ablated.
Cross-dataset evaluation reveals a shared, compact circuit underlying overconfidence,
indicating a conserved model-internal mechanism. Despite differences in dataset format
and content, the overconfidence circuit is strongly conserved within each model. Figure 2
shows that high-attribution regions exhibit similar spatial patterns across all three datasets,
while Table 1 reveals a substantial shared core among the top-ranked components. For
Qwen2.5-3B-Instruct, 8 of the 10 PopQA components recur in the top-10 on both NQOpen
and MMLU. For Llama-3.2-3B-Instruct, a consistent set of attention heads and MLP blocks
is shared across datasets. This ≥80% cross-dataset overlap across both model families
suggests that verbalized overconfidence is supported by stable model-internal circuit rather
than task-specific artifact. The same locus recurs at larger scale: on Qwen2.5-7B-Instruct,
9 of the top-10 components, again mid-to-late MLP blocks, are shared across PopQA and
NQOpen, and steering on this circuit reduces ECE from 0.647 to 0.068 on PopQA and from
0.626 to 0.109 on NQOpen at α = 0.6 (Appendix J).
3.2

Causal Validation

Edge-level validation: The discovered circuits are both sufficient and necessary. We
evaluate along two standard dimensions, corresponding to the two central questions:
• Faithfulness (Sufficiency): Can the model reproduce the specific behavior (e.g.,
overconfidence) relying solely on the isolated sub-circuit with top-k edges retained?
Faithfulness =

∆circuit only − ∆corrupt
∆clean − ∆corrupt

× 100%

(4)

• Completeness (Necessity): To what extent does severing the sub-circuit remove the
signal, rather than allowing it to persist through alternative pathways?
Completeness =

∆clean − ∆ablate circuit
× 100%
∆clean

(5)

Sufficiency. The full computation graph contains 527,743 possible edges for Qwen2.5-3BInstruct and 693,267 for Llama-3.2-3B-Instruct. Retaining only the top-3,000 edges isolates
an extremely sparse subcircuit - less than 0.6% of all possible edges for Qwen and less than
0.5% for Llama. Despite this sparsity, as shown in Figure 3a, all faithfulness curves cross 70%
by k ≈ 2,000–3,000 and plateau above 85%.This characteristic S-shaped saturation confirms
that the overconfidence signal is concentrated in a compact edge-level circuit rather than
diffusely distributed across the network.
Necessity. Completeness provides the converse test: we remove the top-3,000 circuit edges
from the full computation graph and measure how much of the original TSLD remains.
If substantial backup pathways existed, the model could still produce the overconfidence
5

Published as a conference paper at COLM 2026

Model

Dataset

Baseline TSLD

Compl. Drop

Completeness%

Qwen2.5-3B-Instruct

PopQA
NQOpen

10.05
9.68

7.92
7.25

78.8%
74.9%

Llama-3.2-3B-Instruct

PopQA
NQOpen

4.79
4.55

3.56
3.37

74.3%
74.1%

Table 2: Completeness validation. Completeness drop = full-model TSLD − ablated-subnetwork TSLD, where the ablated sub-network retains all edges except the top-3,000.
Qwen2.5­3B­Instruct
MMLU

4

8
6
4

10.5
10.0
9.5
9.0
8.5
8.0

1

2

3

4

5

6

7

8

# Components

9 10

1

2

3

4

5

6

7

8

# Components

9 10

Llama­3.2­3B­Instruct
PopQA

Llama­3.2­3B­Instruct
NQ­Open

4

4

5

Mean TSLD

6

Mean TSLD

8

2

11.5
11.0

Mean TSLD

Mean TSLD

10

Qwen2.5­3B­Instruct
NQ­Open

3
2
1
0

2

3

4

5

6

7

8

# Components

9 10

1

Clean (before)

3
2
1
0

1
1

Mean TSLD

10

Mean TSLD

Qwen2.5­3B­Instruct
PopQA

2

3

4

5

6

7

8

# Components

9 10

Llama­3.2­3B­Instruct
MMLU
1.8
1.6
1.4
1.2

1

2

3

4

5

6

7

8

# Components

9 10

1

2

3

4

5

6

7

8

# Components

9 10

Ablated (after)

Figure 4: Incremental component ablation: mean TSLD as the top-k components are jointly
ablated, for k = 1 to 10. Dashed lines mark the clean (pre-ablation) mean TSLD.

behavior through these alternative routes, and the completeness drop would be small.
Table 2 shows that this is not the case. Ablating the circuit eliminates 74–79% of the baseline
TSLD across all four settings. This provides strong evidence that the discovered circuits
are not merely correlated with overconfidence but carry the bulk of the causal signal in the
studied settings.
Component-level validation: Individual and incremental ablation confirm a small causal
core. Edge-level validation establishes that the overconfidence signal concentrates in a
sparse subgraph, but edges are abstractions of the computational graph formalism rather
than actual units within the model. Moreover, edge attribution can highlight both causal
bottlenecks and relay pathways, so high edge-level importance does not necessarily imply
that a component actually drives overconfidence. We therefore complement edge-level
validation with component-level analyses, ablating the top-ranked CMC components one at
a time and then incrementally to test whether these top components are genuinely causal
drivers of the behavior. Specifically, we adopt a paired resample ablation procedure: for each
record, the target component’s activation at POS END in the clean forward pass is replaced
with the corresponding activation from the corrupted forward pass. The resulting TSLD
change, averaged across Bucket 1 examples, quantifies the component’s causal contribution:
a strongly negative value indicates active contribution, whereas a near-zero value indicates
a relay node that does not independently drive the behavior.
Single-component ablation. Ablating the top-10 components individually reveals a concentrated causal core (Figure 3b). For Qwen, M30 produces the largest TSLD reduction on both
PopQA and NQOpen, followed by M35 and M26; for Llama, L14H3 is the dominant component, followed by M27 and L13H18, with the same ordering on both datasets. In contrast,
several top-ranked early-layer MLPs, M1, M2, and M0 on PopQA, and M3, M0, and M4
on NQOpen, yield zero individual reduction, indicating that they function as relay nodes
rather than causal bottlenecks for inflated verbalized confidence. Joint ablation of all top-10
components yields a much larger effect than any single ablation, but remains markedly
sub-additive relative to the sum of individual effects (e.g., ∼20.3 vs. 8.5 for Qwen/PopQA).
This non-additivity suggests that the discovered components operate as an interconnected
ensemble with shared pathways, rather than as independent parallel channels.
Incremental joint ablation. We progressively ablate the top-ranked components, from the top-1
up to the top-10, and track the resulting mean TSLD (Figure 4). Across all six model×dataset
settings, the curves show a clear diminishing-return pattern: ablating the first few components produces the largest drop in TSLD, while additional components contribute progres6

Model

Method

α

ECE

Brier

ECE Impr.

Brier Impr.

Qwen2.5-3B-Instruct

baseline
mean ablation
steering
steering
steering
steering
steering
steering

–
–
0.3
0.4
0.5
0.6
0.7
0.8

0.492
0.295
0.245
0.166
0.111
0.145
0.167
0.170

0.430
0.244
0.193
0.148
0.130
0.146
0.166
0.170

–
40.0%
50.3%
66.4%
77.5%
70.7%
66.0%
65.5%

–
43.1%
55.1%
65.7%
69.7%
66.1%
61.4%
60.5%

Llama-3.2-3B-Instruct

Published as a conference paper at COLM 2026

baseline
mean ablation
steering
steering
steering
steering
steering
steering

–
–
0.3
0.4
0.5
0.6
0.7
0.8

0.570
0.018
0.338
0.196
0.063
0.020
0.027
0.031

0.495
0.161
0.287
0.189
0.146
0.161
0.163
0.163

–
96.9%
40.7%
65.6%
88.9%
96.5%
95.3%
94.6%

–
67.5%
42.0%
61.9%
70.5%
67.4%
67.0%
67.1%

Table 3: Intervention results on PopQA. Best ECE and Brier per model in bold.
sively smaller gains. This confirms that the overconfidence signal is concentrated in a small
causal core rather than distributed uniformly across many components.

4

Targeted Circuit Intervention for Confidence Recalibration

Having identified and validated the compact set of components that drive overconfidence,
we now ask: can intervening on these components at inference time recalibrate the model’s
verbalized confidence? We study two simple intervention strategies applied to the top-10
CMC components and evaluate their effect on the full dataset using Expected Calibration
Error (ECE) (Pavlovic, 2025), Brier score (Glenn et al., 1950), and reliability curves2 . Importantly, although the intervention references are estimated from a small set of Bucket 1
examples, evaluation is performed on the full dataset, allowing us to test whether circuitlevel intervention generalizes beyond the overconfident discovery subset. Both strategies
share the same deployment principle: a global reference is computed once from a small
set of Bucket 1 examples and then applied uniformly at inference time. As a result, neither
method requires constructing per-sample counterfactuals during deployment. Calibration
results before and after intervention are reported in Tables 3, 11, and 12. Reliability curves
under different intervention strategies are presented in Figures 5 and 7.
Mean ablation suppresses the contribution of a target component by replacing its activation
at POS END with a global reference mean computed from corrupted-prompt activations:
ĥout ( x, POS END ) ← µref =

1 N
(i )
hout ( xcorrupt , POS END ).
N i∑
=1

(6)

Activation steering provides a softer and tunable alternative. Instead of overwriting the
activation, it shifts the target component along a precomputed overconfidence direction:
vconf =


1 N
(i )
(i )
hout ( xclean , POS END ) − hout ( xcorrupt , POS END ) .
N i∑
=1

(7)

During confidence inference, we subtract a scaled version of it from each target activation:
ĥout ( x, POS END ) ← hout ( x, POS END ) − α · vconf ,

(8)

where α ∈ [0, 1] controls the intervention strength. Unlike mean ablation, which fully
replaces the activation, steering preserves the instance-specific signal while nudging it away
from the overconfident direction, providing a continuous recalibration knob.
2 See illustrations in Appendix F and Appendix G

7

Published as a conference paper at COLM 2026

PopQA
Fraction Correct

1.0

Baseline
ECE=0.570

Mean Abl.
ECE=0.018

=0.2
ECE=0.456

=0.3
ECE=0.338

=0.4
ECE=0.196

=0.5
ECE=0.063

=0.6
ECE=0.020

=0.7
ECE=0.027

Baseline
ECE=0.171

Mean Abl.
ECE=0.166

=0.2
ECE=0.124

=0.3
ECE=0.112

=0.4
ECE=0.104

=0.5
ECE=0.095

=0.6
ECE=0.087

=0.7
ECE=0.079

Baseline
ECE=0.507

Mean Abl.
ECE=0.245

=0.2
ECE=0.394

=0.3
ECE=0.318

=0.4
ECE=0.233

=0.5
ECE=0.145

=0.6
ECE=0.088

=0.7
ECE=0.090

0.8

0.6

0.4

0.2

0.0

MMLU
Fraction Correct

1.0

0.8

0.6

0.4

0.2

0.0

NQOpen
Fraction Correct

1.0

0.8

0.6

0.4

0.2

0.0
0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

Figure 5: Reliability curves for Llama-3.2-3B-Instruct across all three datasets under
baseline (before intervention), mean ablation, and steering at α ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7}.

Targeted intervention substantially improves calibration. Direct intervention on the topranked CMC components yields substantial calibration gains across models and datasets.
This improvement is evident both in aggregate metrics and in bin-level calibration behavior.
In terms of ECE and Brier score (Tables 3, 11, 12), both mean ablation and activation steering
are most effective on PopQA and NQOpen, where the best settings reduce ECE by roughly
78–97% on PopQA and 81–83% on NQOpen; improvements on MMLU are smaller but still
consistent, reaching about 33% for Qwen and 57% for Llama. Reliability curves provide a
complementary and more intuitive view. For Llama-3.2-3B-Instruct (Figure 5), both interventions move the confidence–accuracy curves substantially closer to the perfect calibration
diagonal on PopQA and NQOpen. On MMLU, the curves improve more gradually, consistent with the weaker metric gains. Together, these results show that the discovered CMCs
are not merely descriptive artifacts, but practical intervention targets for recalibration.
Steering provides more precise and controllable recalibration than mean ablation. Both
interventions improve calibration, but steering is more controllable. Mean ablation fully
overwrites the target activation, which can be highly effective when the overconfidence
signal is tightly concentrated, but brittle otherwise: for example, it yields a 96.9% ECE
reduction for Llama/PopQA but only 3.1% for Llama/MMLU. Steering instead subtracts
only the overconfidence direction while preserving the instance-specific residual. As a
result, it exhibits a consistent dose–response pattern: ECE improves from α = 0.3 to
an optimum around 0.5–0.6, then degrades as stronger intervention suppresses useful
confidence-related signals. This optimal range is stable across four of six configurations,
making α a practical hyperparameter requiring minimal tuning. Steering therefore provides
a more stable recalibration mechanism overall. The full calibration curves over steering
strengths are provided in Appendix H.
Comparison with post-hoc calibration baselines. Appendix I compares our interventions with temperature scaling (Guo et al., 2017), Platt scaling (Platt et al., 1999), isotonic
regression (Zadrozny & Elkan, 2002), and histogram binning (Zadrozny & Elkan, 2001).
More specifically, our aim is not to outperform existing calibration methods but to establish
circuit-level recalibration as a mechanistic complement that edits the internal computation
rather than remapping outputs, and whose full-dataset ECE reduction from editing only the
discovered components is itself further causal evidence for the discovered circuit.

5

Discussion

Verbalized overconfidence likely reflects a mismatch between confidence verbalization
and factual uncertainty. Our results can be interpreted in light of Teplica et al. (2025),
which argues that a model’s actual uncertainty is generated largely in the same parts in
LLMs that support factuality. If verbal confidence faithfully reported this uncertainty, one
would expect the circuit underlying verbal confidence to align closely with factual retrieval
8

Published as a conference paper at COLM 2026

circuit and to vary with the task-dependent computation that supports answering. Instead,
the circuit driving inflated verbal confidence is highly conserved across datasets within
each model, and the answer-substitution controls (Application E) show that it responds to
the committed answer largely independently of that answer’s correctness, consistent with
behavioral evidence that verbal confidence is largely answer-independent (Seo et al., 2026).
The direct circuit comparison (Figure 9) reinforces this mismatch: the verbal confidence
circuit is more concentrated in middle-to-late layers and denser near the logits, whereas the
factual retrieval circuit spans a longer pathway through earlier and middle layers. Taken
together, these findings suggest that verbalized overconfidence arises from a compact,
correctness-insensitive confidence-writing core that is structurally misaligned with the
model’s factuality-sensitive computation and may impose a default high-confidence bias.
CMCs form a compact causal core of verbalized overconfidence, but not the full
confidence-estimation system. The intervention results show that the discovered CMCs
account for a substantial share of verbalized overconfidence: manipulating only the top-10
components already yields large calibration gains. At the same time, the best results occur
at moderate steering strengths rather than under maximal intervention. One interpretation is that these components form only part of a broader confidence-estimation system,
so stronger intervention begins to disrupt other useful confidence-related computation.
Another is that the steering direction vconf , estimated as an average over Bucket 1 samples,
only approximates the true per-example overconfidence axis, so excessive scaling amplifies
this approximation error. Under either interpretation, the CMCs are best understood as a
compact causal core that disproportionately biases the model toward inflated confidence,
while the full system of confidence estimation remains an open question.
Post-training may strengthen a prior toward overconfident behavior. The models studied
here are instruction-tuned variants, raising the possibility that post-training contributes to
the overconfidence mechanism we identify. Prior work shows that RLHF can exacerbate
verbalized overconfidence and that aligned language models are often more overconfident
than their pretrained counterparts (Leng et al., 2025; He et al., 2023). A natural next step
is to compare pretrained, supervised fine-tuned, and RLHF-tuned checkpoints, or to track
how verbal confidence-related circuits emerge over the course of post-training.

6

Related Work

LLM calibration and verbal confidence. LLMs can be prompted to verbalize confidence,
sometimes with reasonable calibration (Lin et al., 2022; Tian et al., 2023), but subsequent
work found that verbalized confidence is often miscalibrated (Xiong et al., 2023; Yona et al.,
2024), a problem that post-training and RLHF can further exacerbate (He et al., 2023; Leng
et al., 2025). We complement this literature by asking what internal mechanism causally drives
inflated verbal confidence, and whether intervening on it can improve calibration.
Mechanistic interpretability seeks to reverse-engineer the internal circuits that support
model behavior. Prior work has localized circuits for behaviors such as indirect object
identification, mathematical reasoning, and factual/entity knowledge (Wang et al., 2022;
Hanna et al., 2023; Ferrando et al., 2024; Conmy et al., 2023). More recent work has emphasized scalable or practical workflows for applications to larger models and more realistic
tasks (Rai et al., 2024; Hanna et al., 2024). We build on this line of work methodologically:
our pipeline integrates EAP-IG (Hanna et al., 2024) for circuit attribution.
Mechanistic studies of uncertainty and verbal confidence. Teplica et al. (2025) studies the
mechanistic basis of actual uncertainty and argues that it is generated in largely the same
parts of the network that support factuality. Relatedly, Orgad et al. (2024) show that LLMs
internally encode more truthfulness information than they externally reveal. On verbal
confidence specifically, Ji et al. (2025) characterize verbal uncertainty as a linear feature
and intervene on it to reduce hallucinations. Kumaran et al. (2026) analyze how verbal
confidence is computed and argue for a cached-retrieval account, while Stolfo et al. (2024)
identify neurons that regulate next-token confidence more generally. Our work focuses
on a failure mode: the tendency of LLMs to be confidently wrong. We identify the compact
9

Published as a conference paper at COLM 2026

circuit that drives this inflated verbalized confidence, validate its causal role, and show that
targeted intervention on these circuits yields substantial calibration improvement.

7

Conclusion

We present a circuit-level mechanistic analysis of inflated verbalized confidence in LLMs. By
capturing output-level verbal confidence as a differentiable internal proxy, we identify compact Confidence Mover Circuits that causally drive the model’s overconfident behavior. These
circuits are causally validated and substantially conserved across datasets, suggesting that
verbalized overconfidence is supported by a stable model-internal mechanism rather than a
benchmark-specific artifact. We further show that targeted inference-time intervention on
only a small set of top-ranked components substantially improves calibration, establishing
that the discovered circuits are not only interpretable but also actionable. Overall, our results
suggest that verbalized overconfidence is rooted in identifiable internal circuit, and that
circuit-level intervention offers a promising complement to post-hoc calibration methods.

References
Arthur Conmy, Augustine Mavor-Parker, Aengus Lynch, Stefan Heimersheim, and Adrià
Garriga-Alonso. Towards automated circuit discovery for mechanistic interpretability.
Advances in Neural Information Processing Systems, 36:16318–16352, 2023.
Javier Ferrando, Oscar Obeso, Senthooran Rajamanoharan, and Neel Nanda. Do i know
this entity? knowledge awareness and hallucinations in language models. arXiv preprint
arXiv:2411.14257, 2024.
W Brier Glenn et al. Verification of forecasts expressed in terms of probability. Monthly
weather review, 78(1):1–3, 1950.
Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian,
Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The
llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q Weinberger. On calibration of modern neural
networks. In International conference on machine learning, pp. 1321–1330. PMLR, 2017.
Michael Hanna, Ollie Liu, and Alexandre Variengien. How does gpt-2 compute greaterthan?: Interpreting mathematical abilities in a pre-trained language model. Advances in
Neural Information Processing Systems, 36:76033–76060, 2023.
Michael Hanna, Sandro Pezzelle, and Yonatan Belinkov. Have faith in faithfulness: Going
beyond circuit overlap when finding model mechanisms. arXiv preprint arXiv:2403.17806,
2024.
Guande He, Peng Cui, Jianfei Chen, Wenbo Hu, and Jun Zhu. Investigating uncertainty
calibration of aligned language models under the multiple-choice setting. arXiv preprint
arXiv:2310.11732, 2023.
Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and
Jacob Steinhardt. Measuring massive multitask language understanding. Proceedings of
the International Conference on Learning Representations (ICLR), 2021.
Ziwei Ji, Lei Yu, Yeskendir Koishekenov, Yejin Bang, Anthony Hartshorn, Alan Schelten,
Cheng Zhang, Pascale Fung, and Nicola Cancedda. Calibrating verbal uncertainty as a
linear feature to reduce hallucinations. In Proceedings of the 2025 Conference on Empirical
Methods in Natural Language Processing, pp. 3769–3793, 2025.
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez,
Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, et al. Language
models (mostly) know what they know. arXiv preprint arXiv:2207.05221, 2022.
10

Published as a conference paper at COLM 2026

Dharshan Kumaran, Arthur Conmy, Federico Barbero, Simon Osindero, Viorica Patraucean, and Petar Velickovic. How do llms compute verbal confidence. arXiv preprint
arXiv:2603.17839, 2026.
Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. Latent retrieval for weakly supervised open domain question answering. In Anna Korhonen, David Traum, and Lluı́s
Màrquez (eds.), Proceedings of the 57th Annual Meeting of the Association for Computational
Linguistics, pp. 6086–6096, Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1612. URL https://aclanthology.org/P19-1612/.
Jixuan Leng, Chengsong Huang, Banghua Zhu, and Jiaxin Huang. Taming overconfidence
in LLMs: Reward calibration in RLHF. In The Thirteenth International Conference on Learning
Representations, 2025. URL https://openreview.net/forum?id=l0tg0jzsdL.
Stephanie Lin, Jacob Hilton, and Owain Evans. Teaching models to express their uncertainty
in words. arXiv preprint arXiv:2205.14334, 2022.
Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Hannaneh Hajishirzi, and Daniel
Khashabi. When not to trust language models: Investigating effectiveness and limitations
of parametric and non-parametric memories. arXiv preprint, 2022.
Kevin Meng, David Bau, Alex Andonian, and Yonatan Belinkov. Locating and editing factual
associations in gpt. Advances in neural information processing systems, 35:17359–17372, 2022.
Neel Nanda. Attribution patching: Activation patching at industrial scale. URL: https://www.
neelnanda. io/mechanistic-interpretability/attribution-patching, 2023.
Hadas Orgad, Michael Toker, Zorik Gekhman, Roi Reichart, Idan Szpektor, Hadas Kotek,
and Yonatan Belinkov. Llms know more than they show: On the intrinsic representation
of llm hallucinations. arXiv preprint arXiv:2410.02707, 2024.
Maja Pavlovic. Understanding model calibration–a gentle introduction and visual
exploration of calibration and the expected calibration error (ece). arXiv preprint
arXiv:2501.19047, 2025.
John Platt et al. Probabilistic outputs for support vector machines and comparisons to
regularized likelihood methods. Advances in large margin classifiers, 10(3):61–74, 1999.
Daking Rai, Yilun Zhou, Shi Feng, Abulhair Saparov, and Ziyu Yao. A practical review
of mechanistic interpretability for transformer-based language models. arXiv preprint
arXiv:2407.02646, 2024.
KiJung Seo, Sehun Lim, and Taeuk Kim. Advice: Answer-dependent verbalized confidence
estimation. In Proceedings of the 64th Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), pp. 23942–23962, 2026.
Alessandro Stolfo, Ben Wu, Wes Gurnee, Yonatan Belinkov, Xingyi Song, Mrinmaya Sachan,
and Neel Nanda. Confidence regulation neurons in language models. Advances in Neural
Information Processing Systems, 37:125019–125049, 2024.
Qwen Team. Qwen2.5: A party of foundation models, September 2024. URL https:
//qwenlm.github.io/blog/qwen2.5/.
Carter Teplica, Yixin Liu, Arman Cohan, and Tim GJ Rudner. Sciurus: Shared circuits
for interpretable uncertainty representations in language models. In Proceedings of the
2025 Conference of the Nations of the Americas Chapter of the Association for Computational
Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 12451–12469, 2025.
Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao,
Chelsea Finn, and Christopher D Manning. Just ask for calibration: Strategies for eliciting
calibrated confidence scores from language models fine-tuned with human feedback. In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp.
5433–5442, 2023.
11

Published as a conference paper at COLM 2026

Kevin Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, and Jacob Steinhardt.
Interpretability in the wild: a circuit for indirect object identification in gpt-2 small. arXiv
preprint arXiv:2211.00593, 2022.
Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan Hooi. Can
llms express their uncertainty? an empirical evaluation of confidence elicitation in llms.
arXiv preprint arXiv:2306.13063, 2023.
Gal Yona, Roee Aharoni, and Mor Geva. Can large language models faithfully express their
intrinsic uncertainty in words? In Proceedings of the 2024 Conference on Empirical Methods
in Natural Language Processing, pp. 7752–7764, 2024.
Bianca Zadrozny and Charles Elkan. Obtaining calibrated probability estimates from
decision trees and naive bayesian classifiers. In Proceedings of the Eighteenth International
Conference on Machine Learning, pp. 609–616, 2001.
Bianca Zadrozny and Charles Elkan. Transforming classifier scores into accurate multiclass
probability estimates. In Proceedings of the eighth ACM SIGKDD international conference on
Knowledge discovery and data mining, pp. 694–699, 2002.

A

Models and Datasets

Models. We experiment on two open-weight instruction-tuned model families with distinct
architectures: Qwen2.5-3B-Instruct (Team, 2024) (36 layers, 16 query heads, GQA with 2 KV
heads) and Llama-3.2-3B-Instruct (Grattafiori et al., 2024) (28 layers, 24 query heads, GQA
with 8 KV heads).
Datasets. We evaluate on three knowledge-intensive QA benchmarks spanning different
question formats: PopQA (Mallen et al., 2022) (14,267 open-domain factoid questions with
associated Wikipedia-popularity scores), MMLU (Hendrycks et al., 2021) (14,042 multiplechoice knowledge questions across 57 subjects), and NQOpen (Lee et al., 2019) (3,610
open-domain questions derived from Google search queries). PopQA and NQOpen test
free-form factual recall; MMLU introduces a constrained multiple-choice format. For each
model×dataset combination, we run the two-step elicitation pipeline (§2), retain only
incorrect predictions, and stratify into three buckets for circuit discovery.

B

LLM as a Computational Graph

We conceptualize the LLM as a Directed Acyclic Graph (DAG), denoted as G = (V , E ),
following the standard view in circuit-level mechanistic interpretability. In this graph, nodes
V correspond to computational modules, and edges E represent information flow between
modules through the residual stream. This formulation provides a convenient abstraction
for identifying the subgraph that causally supports a target behavior.
Nodes (V ). To enable fine-grained circuit discovery, we decompose the standard Transformer
blocks into the atomic linear projections of the models:
(l,h)

(l,h)

V = {WQ , WK

(l,h)

, WV

(l,h)

, WO

(l )

, WMLP | l ∈ [1, L], h ∈ [1, H ]}

(9)

where L is the number of layers and H is the number of heads per layer. WQ , WK , WV
represent the query, key, and value projections for the h-th head in layer l, WO is the output
projection, and WMLP represents the two-layer feed-forward network.
Edges (E ). An edge eu→v exists if the output of module u contributes to the input of module
v via the residual stream. Intuitively, edges capture how intermediate representations are
transmitted and transformed across the network. Our goal is to identify the subset of edges
whose activations are causally responsible for the target behavior of interest, namely inflated
verbalized confidence.
Behavioral metric. Given an input x, let f ( x ) denote the scalar behavior of interest. In this
work, f ( x ) is instantiated as the Target-Set Logit Difference (TSLD) defined in Section 2,
12

Published as a conference paper at COLM 2026

which serves as a differentiable proxy for verbalized confidence. Circuit attribution is
therefore performed with respect to changes in this scalar signal.

C

Edge Attribution Patching with Integrated Gradients (EAP-IG)

To identify the subgraph responsible for a target behavior, we require a method that attributes changes in the behavioral metric to specific internal edges. Standard methods like
Activation Patching (Meng et al., 2022) are faithful but computationally expensive, while
vanilla gradient attribution is efficient but can be unreliable in deep nonlinear networks
due to gradient saturation. To balance fidelity and efficiency, we employ Edge Attribution
Patching with Integrated Gradients (EAP-IG) (Hanna et al., 2024).
Vanilla EAP (Nanda, 2023) approximates the importance of an edge e using the product of
its activation xe and the gradient of the scalar objective L with respect to that activation:
ϕEAP = xe ·

∂L
∂xe

(10)

where, in our setting, L is the confidence-related signal induced by TSLD. While requiring
only one backward pass, this method can fail under saturation effect. When a neuron is
fully activated, the local gradient is near zero, even if that neuron is critically important for
the output, leading to incomplete or fragmented circuits.
To overcome saturation, EAP-IG (Hanna et al., 2024) accumulates gradients along a linear
path between a corrupted baseline input (Icorrupt ) and the clean target input (Iclean ). Let xe
corrupt

corrupt

denote the activation along edge e. A path is defined as xe (γ) = xe
+ γ( xeclean − xe
for γ ∈ [0, 1]. The attribution score ϕ(e) for an edge e is calculated as:
corrupt

ϕ(e) = ( xeclean − xe

)×

Z 1

∂L( x (γ))
dγ
γ=0 ∂xe ( γ )

)

(11)

By accumulating gradients along the interpolation path rather than relying on a single local
derivative, EAP-IG yields more reliable edge attributions under saturation. In practice, this
integral is approximated using a Riemann sum with m steps:
corrupt

ϕ(e) ≈ ( xeclean − xe

D

)×

1 m ∂L( x ( mk ))
m k∑
∂xe
=1

(12)

Raw Verbal Confidence Distributions

Figure 6 shows the distribution of verbalized confidence scores across all six model×dataset
configurations, separated by answer correctness. These distributions vividly illustrate the
core phenomenon studied in this paper: the models are not merely wrong, but confidently
wrong, systematically assigning high confidence scores that poorly discriminate between
correct and incorrect answers.

E

Robustness Controls for Circuit Discovery

E.1

Answer-Substitution Control

The truth-injection counterfactual replaces the model’s incorrect Step 1 answer with the
ground-truth answer. Although this intervention changes the factual status of the committed
answer, it may also alter semantic content, surface form, token identity, and sequence length.
To test whether these factors account for the recovered circuit, we repeat EAP-IG circuit
discovery on Qwen2.5-3B-Instruct/PopQA using four Step 1 answer substitutions:
1. the ground-truth answer used in the main experiment;
13

Published as a conference paper at COLM 2026

Qwen2.5-3B-Instruct
Count

PopQA

MMLU

N=14267
Acc=17.0%
Mean Confidence=66.10

8000

5000

N=3610
Acc=20.9%
Mean Confidence=75.88

2000

4000

6000

1500
3000

4000

1000
2000

2000

500

1000

0

Llama-3.2-3B-Instruct
Count

NQOpen

N=14042
Acc=62.5%
Mean Confidence=90.57

0

8000

0

10000

N=14267
Acc=20.4%
Mean Confidence=77.03

N=14042
Acc=59.0%
Mean Confidence=75.83

8000

N=3610
Acc=28.6%
Mean Confidence=79.31

2000
1750
1500

6000

6000

1250
1000

4000

4000

2000

750
500

2000

250
0

0

20

40

60

Confidence Score (0-99)

80

100

0

0

20

40

60

Confidence Score (0-99)
Correct

80

100

0

0

20

40

60

Confidence Score (0-99)

80

100

Incorrect

Figure 6: Raw verbalized confidence distributions across all six model×dataset configurations. Green: correct predictions; red: incorrect predictions.

2. a same-meaning paraphrase, implemented as a different valid PopQA gold alias;
3. a type-matched plausible-wrong answer, sampled from another answer associated
with the same relation type; and
4. a length-matched distractor with comparable token length but unrelated semantic
content.
For example, when the question is “What is Henry Feilden’s occupation?” and the model
answers “architect,” the four substitutions are “politician,” “political leader,” “priest,” and
“board game,” respectively.
We evaluate each condition using the mean ∆TSLD and the overlap between its top-10
attributed components and those recovered under the original ground-truth substitution.
Substituted Step 1 answer
Ground truth
Same-meaning gold alias
Type-matched plausible-wrong answer
Length-matched distractor

Mean ∆TSLD

Top-10 overlap

−8.50
−8.24
−7.71
−8.68

10/10
9/10
10/10
7/10

Table 4: Answer-substitution controls on Qwen2.5-3B-Instruct/PopQA. Mean ∆TSLD measures the change relative to the original incorrect-answer context, with more negative values
indicating a larger confidence decrease. Top-10 overlap is measured against the circuit
recovered using ground-truth substitution.
As shown in Table 4, all four substitutions produce confidence decreases of similar magnitude and recover substantially overlapping component sets. The same-meaning alias result
shows that the circuit is not tied to the exact surface form of the ground-truth answer. The
length-matched control indicates that answer length alone does not explain the attribution
pattern. More importantly, the plausible-wrong condition produces a confidence shift and
component ranking comparable to those obtained with the ground truth. Therefore, the
discovered circuit cannot be interpreted as selectively detecting whether the substituted
answer is factually correct.
The results instead support a more precise interpretation: the CMC writes verbalized confidence conditioned on the model’s committed answer, while remaining largely insensitive to
14

Published as a conference paper at COLM 2026

whether that answer is factually correct. That is, the model is confident in what it said, not
in what is true.
E.2

Elicitation-Prompt Control

The main experiments use a fixed Step 2 prompt to elicit verbalized confidence. To test
whether the recovered components depend on this exact wording, we repeat circuit discovery on Qwen2.5-3B-Instruct/PopQA using three semantically related prompt variants.
Step 2 confidence prompt
Original prompt
“How certain are you that it is correct?”
“On a scale from 0 to 100, how sure are you?”
“How likely is it that your answer is accurate?”

Mean ∆TSLD

Top-5 overlap

Top-10 overlap

−7.07
−10.63
−3.75
−3.35

5/5
4/5
3/5
4/5

10/10
8/10
7/10
6/10

Table 5: Confidence-prompt robustness on Qwen2.5-3B-Instruct/PopQA. The circuit remains partially conserved under three semantically related Step 2 prompt variants.
The top-ranked components remain conserved across all prompt variants, suggesting that
the discovered circuits are properties of the models rather than artifacts of a single elicitation
template.
E.3

TSLD Set Sensitivity

We vary the high- and low-confidence sets used in Eq. 1 and measure the Jaccard similarity between the resulting top-10 components and those discovered with the default sets
(Table 6).
High/low target sets

Top-10 Jaccard vs. default

H = {70, 75, 80, 85, 90, 99}; L = {0, 10, 15, 20, 25, 30}
H = {80, 85, 90, 99}; L = {0, 10, 20}
H = {60, 65, 70, 75, 80, 85, 90, 95, 99}; L = {0, 5, 10, 15, 20, 25, 30, 35, 40}
H = {80, 90, 99}; L = {0, 15, 30}
H = {75, 80, 85, 90, 95, 99}; L = {5, 10, 15, 20, 25, 35}

1.00
1.00
0.82
0.82
0.82

Table 6: Sensitivity of Qwen2.5-3B-Instruct/PopQA circuit discovery to TSLD target sets.
The recovered top-10 components remain stable across narrower, wider, coarser, and shifted
target sets.

E.4

Bucket-2 Contrast

Running the same EAP-IG discovery on Bucket 2 (the opposite-sign contrast in which truth
injection increases confidence) yields an attention-heavy circuit whose top components
(L26H3, L28H4, M13, M19, L35H3, and others) share none of the Bucket 1 top-10 (Jaccard
0.00). A distinct circuit is expected for an opposite-sign phenomenon; the disjointness
confirms that the Bucket 1 circuit is specific to overconfident collapse rather than a byproduct of the stratification.

F

Calibration Metrics

We evaluate recalibration using two standard metrics.
Expected Calibration Error (ECE) (Pavlovic, 2025) measures the average gap between
predicted confidence and observed accuracy. Predictions are partitioned into B equalwidth bins by confidence score, and ECE is computed as the weighted average of per-bin
15

Published as a conference paper at COLM 2026

calibration gaps:
B

nb
acc(b) − conf(b) ,
N
b =1

ECE = ∑

(13)

where nb is the number of samples in bin b, N is the total number of samples, acc(b) is the
empirical accuracy within the bin, and conf(b) is the mean predicted confidence. A perfectly
calibrated model has ECE = 0. We use B = 10 bins throughout.
Brier Score (Glenn et al., 1950) provides a complementary assessment by measuring the
mean squared error between the predicted confidence (normalized to [0, 1]) and the binary
correctness indicator:
Brier =

2
1 N
ci − yi ,
∑
N i =1

(14)

where ci ∈ [0, 1] is the predicted confidence for sample i and yi ∈ {0, 1} indicates whether
the answer is correct. Unlike ECE, which captures only calibration, the Brier score jointly
penalizes miscalibration and poor discrimination (inability to separate correct from incorrect
predictions), providing a more holistic measure of confidence quality. Lower values indicate
better performance for both metrics.

G

Reliability Curves

Reliability curves provide a bin-level view of calibration. They plot empirical accuracy
against mean predicted confidence over confidence bins, with the diagonal corresponding to
perfect calibration: if the model reports confidence p, it should be correct approximately p
fraction of the time. Curves below the diagonal indicate overconfidence, meaning that the
model is less accurate than its stated confidence suggests, while curves above the diagonal
indicate underconfidence. Compared with aggregate metrics such as ECE and Brier score,
reliability curves provide a more fine-grained and interpretable view of calibration by
showing where miscalibration occurs across the confidence range and whether it takes
the form of overconfidence or underconfidence. The shaded area between the curve and
the diagonal visualizes the total calibration gap, which ECE summarizes as a single scalar.
Intuitively, the closer the curve lies to the diagonal, the better calibrated the model is.
Figures 7 and 5 show reliability curves for Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct
respectively, across all three datasets under baseline (before intervention), mean ablation,
and steering at α ∈ {0.2, . . . , 0.7}.

PopQA
Fraction Correct

1.0

Baseline
ECE=0.492

Mean Abl.
ECE=0.295

=0.2
ECE=0.349

=0.3
ECE=0.245

=0.4
ECE=0.166

=0.5
ECE=0.111

=0.6
ECE=0.144

=0.7
ECE=0.167

Baseline
ECE=0.281

Mean Abl.
ECE=0.261

=0.2
ECE=0.266

=0.3
ECE=0.250

=0.4
ECE=0.230

=0.5
ECE=0.196

=0.6
ECE=0.188

=0.7
ECE=0.197

Baseline
ECE=0.551

Mean Abl.
ECE=0.374

=0.2
ECE=0.403

=0.3
ECE=0.295

=0.4
ECE=0.201

=0.5
ECE=0.140

=0.6
ECE=0.103

=0.7
ECE=0.142

0.8

0.6

0.4

0.2

0.0

MMLU
Fraction Correct

1.0

0.8

0.6

0.4

0.2

0.0

NQOpen
Fraction Correct

1.0

0.8

0.6

0.4

0.2

0.0
0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

0.0

0.2

0.4

0.6

0.8

Mean Pred. Conf.

1.0

Figure 7: Reliability curves for Qwen2.5-3B-Instruct across PopQA (top), MMLU (middle),
and NQOpen (bottom) under baseline (before intervention), mean ablation, and steering at
α ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7}.

16

Published as a conference paper at COLM 2026

PopQA

MMLU
0.35

0.40
0.30

0.30

0.25

0.26

0.30

0.24

0.29

0.20

0.35

0.22

0.28

0.20

0.27

0.25

0.15

0.20

0.1

0.10
0.3

0.4

0.5

0.6

Steering Alpha

0.7

0.8

0.9

1.0

0.1

0.2

0.3

0.4

0.5

0.6

Steering Alpha

0.7

0.8

0.9

1.0

0.3

0.30

0.2

0.25

0.252

0.14

0.250

0.12

0.248

0.5

0.6

Steering Alpha

0.7

0.8

0.9

1.0

0.400
0.375

0.4

0.350

0.3

0.300
0.275

0.246

0.10

0.2

0.250

0.244

0.20

0.1

0.4

0.325

ECE

0.35

0.3

0.5
0.16

0.40

0.4

0.2

0.254

0.45

0.5

0.15

0.1

Brier

0.2

ECE

0.1

Llama-3.2-3B-Instruct
ECE

0.30

0.3

0.2

0.15

0.0

0.40

0.5

0.4

0.25
0.20

0.31

Brier

0.35

NQOpen

0.28

ECE

0.45

ECE

Qwen2.5-3B-Instruct
ECE

0.50

0.225

0.08
0.242

0.15

0.1

0.2

0.3

0.4

0.5

0.6

Steering Alpha

ECE

0.7

0.8

0.9

1.0

Brier Score

0.1

0.2

0.3

0.4

0.5

0.6

Steering Alpha

Baseline ECE

0.7

0.8

0.9

1.0

0.1

0.200

0.1

Mean Ablation ECE

0.2

0.3

0.4

0.5

0.6

Steering Alpha

0.7

0.8

0.9

1.0

Best ECE alpha

Figure 8: Steering α sweep across all six configurations. ECE (teal, left axis) and Brier score
(purple, right axis) as a function of steering strength α. Dashed grey: baseline ECE; dashed
yellow: mean ablation ECE; star: optimal α.

H

Full Steering Strength Sweep from 0.1 to 1

Figure 8 shows ECE (left axis) and Brier score (right axis) as a function of steering strength α.
Across all six model×dataset settings, steering exhibits a clear dose-response pattern: both
ECE and Brier score improve substantially as α increases from small values, indicating that
progressively stronger suppression of the overconfidence direction yields better calibration.
However, this improvement is not monotonic. In most settings, performance reaches an
optimum at a moderate intervention strength and then plateaus or degrades as α becomes
too large. Overall, the sweep confirms that activation steering provides a robust and tunable
recalibration mechanism. It also shows that the intervention is not simply “the stronger, the
better”: calibration improves most when the overconfidence direction is attenuated to an
intermediate degree rather than fully suppressed.

I

Comparison with Post-Hoc Calibration Baselines

We compare circuit-level intervention against four standard output-level calibrators: temperature scaling (Guo et al., 2017), Platt scaling (Platt et al., 1999), isotonic regression (Zadrozny
& Elkan, 2002), and histogram binning (Zadrozny & Elkan, 2001). Each calibrator is fit on a
labeled 50% split of the verbalized confidence scores and evaluated on the disjoint 50% split;
the Raw ECE column is computed on that evaluation split and therefore deviates slightly
from the full-dataset baselines in Tables 3, 11, and 12. The mean-ablation and best-steering
columns restate our full-dataset results from those tables. The comparison is included
to position circuit-level recalibration as a viable, mechanistic complement to output-level
post-hoc calibration methods, rather than to claim state-of-the-art calibration performance

J

Model Scale Generalization

To test whether the discovered mechanism persists at larger scale within the same model
family, we repeat circuit discovery and the steering sweep on Qwen2.5-7B-Instruct for
PopQA and NQOpen. Table 8 lists the top-10 components: 9 of the top-10 are shared across
the two datasets, and the circuit again consists of mid-to-late MLP blocks, the same locus
as at 3B. Table 9 reports the steering sweep: at α = 0.6, ECE falls from 0.647 to 0.068 on
PopQA and from 0.626 to 0.109 on NQOpen, with the same dose–response pattern as at 3B,
17

Published as a conference paper at COLM 2026

Model / Dataset

Raw ECE Temp. Platt Isotonic Histogram Mean abl. (ours) Best steer (ours)

Llama-3.2-3B / PopQA
Qwen2.5-3B / NQOpen
Llama-3.2-3B / MMLU
Llama-3.2-3B / NQOpen

0.568
0.555
0.176
0.507

0.302
0.304
0.021
0.245

0.008
0.016
0.026
0.036

0.075
0.054
0.078
0.057

0.147
0.033
0.232
0.191

0.018
0.374
0.166
0.245

0.020
0.103
0.074
0.088

Table 7: Comparison with post-hoc calibrators (ECE, 10 bins; lower is better). Calibrators
are fit on a labeled 50% split and evaluated on the disjoint half; Raw ECE is computed on
the evaluation split. Mean ablation and best steering restate our full-dataset results from
Tables 3, 11, and 12.
Rank

PopQA

NQOpen

1
2
3
4
5
6
7
8
9
10

m27
m21
m23
m26
m20
m19
m25
m18
m24
a20.h1

m27
m21
m26
m23
m20
m19
m25
m24
m22
m18

Table 8: Top-10 components by attribution score for Qwen2.5-7B-Instruct. 9 of the top-10
components are shared across PopQA and NQOpen.
while mean ablation is effective on PopQA (0.155) but not on NQOpen (0.615), mirroring
the brittleness observed at 3B. This cross-scale experimental result further complements the
cross-family Qwen2.5-3B vs Llama-3.2-3B result.
Dataset

Baseline

α = 0.2

α = 0.3

α = 0.4

α = 0.5

α = 0.6

Mean ablation

PopQA
NQOpen

0.647
0.626

0.419
0.528

0.312
0.450

0.203
0.347

0.121
0.217

0.068
0.109

0.155
0.615

Table 9: Intervention results (ECE) for Qwen2.5-7B-Instruct. Steering sweep over α and
mean ablation; best ECE per dataset in bold.

18

Published as a conference paper at COLM 2026

Bucket
1
2
3

Criterion

Role

∆TSLD ≤ −τ
∆TSLD ≥ +τ
∆TSLD ≈ 0

Overconfident collapse; circuit discovery target
Truth recognition; excluded
Noise; excluded

Model

Method

α

ECE

Brier

ECE Impr.

Brier Impr.

Qwen2.5-3B-Instruct

baseline
mean ablation
steering
steering
steering
steering
steering
steering

–
–
0.3
0.4
0.5
0.6
0.7
0.8

0.281
0.261
0.250
0.230
0.196
0.188
0.197
0.217

0.310
0.298
0.294
0.284
0.271
0.263
0.265
0.274

–
7.3%
11.1%
18.2%
30.3%
33.1%
29.9%
22.7%

–
3.8%
5.2%
8.3%
12.7%
15.3%
14.6%
11.8%

Llama-3.2-3B-Instruct

Table 10: Three-bucket stratification.

baseline
mean ablation
steering
steering
steering
steering
steering
steering

–
–
0.3
0.4
0.5
0.6
0.7
0.8

0.171
0.166
0.112
0.104
0.095
0.087
0.079
0.074

0.265
0.269
0.246
0.245
0.243
0.242
0.242
0.242

–
3.1%
34.7%
39.4%
44.5%
48.9%
53.7%
57.0%

–
−1.8%
7.0%
7.5%
8.3%
8.4%
8.6%
8.4%

Model

Method

α

ECE

Brier

ECE Impr.

Brier Impr.

Qwen2.5-3B-Instruct

baseline
mean ablation
steering
steering
steering
steering
steering
steering

–
–
0.3
0.4
0.5
0.6
0.7
0.8

0.551
0.374
0.295
0.201
0.141
0.103
0.142
0.201

0.485
0.304
0.244
0.191
0.169
0.159
0.174
0.204

–
32.1%
46.5%
63.5%
74.5%
81.2%
74.2%
63.4%

–
37.3%
49.6%
60.7%
65.1%
67.2%
64.1%
57.9%

Llama-3.2-3B-Instruct

Table 11: Intervention results on MMLU. Best ECE and Brier per model in bold.

baseline
mean ablation
steering
steering
steering
steering
steering
steering

–
–
0.3
0.4
0.5
0.6
0.7
0.8

0.507
0.245
0.318
0.233
0.145
0.088
0.091
0.089

0.453
0.273
0.299
0.249
0.212
0.199
0.207
0.210

–
51.7%
37.4%
54.1%
71.3%
82.6%
82.2%
82.5%

–
39.8%
34.1%
45.0%
53.2%
56.1%
54.3%
53.6%

Table 12: Intervention results on NQOpen. Best ECE and Brier per model in bold.

19

Published as a conference paper at COLM 2026

Confidence
DAG— Qwen2.5-3B-Instruct
Qwen2.5-3B-Instruct / PopQA / PopQA
Confidence
CircuitCircuit
DAG
A24HH7

MLP ( )
Attention head ( )
A0HH4
Output (logits) ( )

CMH edge (score < 0)
CAH edge (score > 0)

A24HH5

A26HH4

A24HH4

A26HH3

A28HH4
A0HH2
M3

M4

M5

M9

M10

M21

M22

M25

M27

A0HH1

A24HH1

A26HH0

M0

A24HH0

M26

A35HH5
A31HH7

A28HH2

M29

M30

M32

M33

A34HH10 A35HH3

Logits

M31
M28

M35

M24

0

3

4

5

9

A0HH5

10

21

Layer

22

24

25

26

27

28

29

30

31

32

33

34

35

37

M35

Logits

35

37

Factual Retrieval
Circuit
DAG— Qwen2.5-3B-Instruct
/ PopQA / PopQA
Factual Retrieval
Circuit
DAG
Qwen2.5-3B-Instruct

A0HH9

MLP ( )
Attention head ( )
Output (logits) ( )

Factual retrieval edge (score < 0)
Positive edge (score > 0)

A34HH8

A27HH11

A31HH7

A34HH14

A0HH4
M3

M4

M5

M7

M8

M9

M10

M11

M13

M14

M17

M20

A27HH10

M28

M30

A31HH1

M32

M33

A34HH12

A0HH2
M27

M31

A34HH10

A0HH1
M34
M0

0

3

4

5

7

8

9

10

11

13

14

17

Layer

20

27

28

30

31

32

33

34

Figure 9: Verbal confidence circuit vs. factual retrieval circuit (Qwen2.5-3B-Instruct, PopQA).
Both circuits are discovered on the same Bucket 1 records with the same EAP-IG machinery;
the factual retrieval circuit uses an answer-logit objective in place of TSLD. The two circuits
are structurally distinct: the Jaccard overlap of their top-10 (top-20) components is 0.18
(0.21), and the cosine similarity between their signed edge-attribution scores on the induced
subgraphs is 0.004 (0.055).

20

