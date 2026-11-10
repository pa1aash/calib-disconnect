---
title: 'CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution
  Graphs'
id: codecircuit-toward-inferring-llm-generated-code-correctness-via-attribution-grap
tags:
- code-llm-confidence-positioning-d82d00
- code-probe
created: '2026-11-09T23:08:37.403265Z'
updated: '2026-11-09T23:27:44.490390Z'
source: https://arxiv.org/html/2602.07080
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:37.402853Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: FULL TEXT (2602.07080). Transcoder attribution-graph topology predicts line-level
  code correctness on Gemma-2-2B-it, MBPP and translated Java/C++; baselines MaxProb/PPL/entropy/CoE
  near 50 AUROC; labels from GPT-4o not execution; causal node interventions fix code.
---

CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2602.07080v1 [cs.SE] 06 Feb 2026
CodeCircuit
: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs
Yicheng He
Affiliation:
University of Illinois Urbana-Champaign
Correspondence to:
yh84@uiuc.edu
Zheng Zhao
Affiliation:
University of Edinburgh
Kaiyu Zhou
Affiliation:
Nanyang Technological University
Bryan Dai
Affiliation:
IQuest Research
Jie Fu
Affiliation:
IQuest Research
Yonghui Yang
Affiliation:
National University of Singapore
Abstract
Current paradigms for code verification rely heavily on external mechanisms—such as execution-based unit tests or auxiliary LLM judges—which are often labor-intensive or limited by the judging model’s own capabilities. This raises a fundamental, yet unexplored question: Can an LLM’s functional correctness be assessed purely from its internal computational structure? Our primary objective is to investigate whether the model’s neural dynamics encode internally decodable signals that are predictive of logical validity during code generation. Inspired by mechanistic interpretability, we propose to treat code verification as a mechanistic diagnostic task, mapping the model’s explicit algorithmic trajectory into line-level attribution graphs. By decomposing complex residual flows, we aim to identify the structural signatures that distinguish sound reasoning from logical failure within the model’s internal circuits. Analysis across Python, C++, and Java confirms that intrinsic correctness signals are robust across diverse syntaxes. Topological features from these internal graphs predict correctness more reliably than surface heuristics and enable targeted causal interventions to fix erroneous logic. These findings establish internal introspection as a decodable property for verifying generated code. Our code is at
https://github.com/bruno686/CodeCircuit
.
Keywords:
Machine Learning, ICML
†
†
affiliationnotice:
Equal contribution
1
Introduction
Large language models (LLMs;
Liu et al., 2024a
;
He et al., 2025b
;
Rozière et al., 2023
;
Guo et al., 2024
) have transformed code generation from simple solvers to complex agents
(
Wang et al., 2024a
;
Shinn et al., 2023
;
Madaan et al., 2023
)
. As these models integrate into mission-critical workflows, the demand for functionally correct and maintainable code has intensified
(
Liu et al., 2023
;
Liu et al., 2024b
)
. However, the stochastic nature of LLMs makes reliable assessment a persistent bottleneck. While execution-based verification via unit tests remains the standard
(
Khan et al., 2024
;
Dong et al., 2025
;
Wang et al., 2023b
;
Chen et al., 2021
;
Austin et al., 2021
;
Hendrycks et al., 2021
)
, it is limited by labor-intensive test design and sparse edge-case coverage. Emergent
LLM-as-a-Judge
frameworks offer scalable automation
(
He et al., 2025a
;
Jiang et al., 2025
)
, yet they introduce inference overhead and suffer from recursive dependencies where reliability is bounded by the evaluator’s own reasoning priors.
Given these limitations of external mechanisms, a natural question arises:
Can code correctness be assessed intrinsically, by examining the LLM’s internal computational structure?
Prior work has probed neuron activations and representation dynamics during generation
(
Bui et al., 2025
;
Huang et al., 2025
;
Patel et al., 2025
)
, yet these analyses have not been directly linked to the correctness of the generated code. In parallel, recent advances in mechanistic interpretability
(
Michaud et al., 2024
;
Sharkey et al., 2025
;
Rai et al., 2024a
;
Gao et al., 2025
;
Templeton et al., 2024
)
, specifically the use of attribution graphs to trace reasoning pathways
(
Dunefsky et al., 2024
;
Ameisen et al., 2025
;
Zhao et al., 2025
)
, have shown promise in reasoning domains. We believe that bridging this gap requires a deeper look at how code-specific structures are manifested within the model’s latent space during the generation process.
Unlike natural language or abstract math, code possesses a rigid, objective topology, such as control flow and variable binding. Recent research
(
Zhang et al., 2025
)
demonstrates that LLMs could form internal finite automata rather than relying on superficial statistical shortcuts. Thus, we hypothesize that reliable code generation requires the model to instantiate specific neural circuits that mirror this topology, and that errors manifest as detectable structural collapses within these circuits. By decoding the intrinsic circuits that drive code generation, we gain a window into the model’s internally consistent computational trajectories—bypassing both the opacity of black-box methods and the incompleteness of external verification frameworks, ultimately providing a more robust foundation for assessing model reliability.
Figure 1:
Topological fingerprints of code generation errors. Distributions of five graph features extracted from attribution graphs show differences between correct (blue) and incorrect (orange) code construction steps. These results demonstrate that the attribution topology provides a structural signal for monitoring the integrity of the code generation process.
To operationalize this, we introduce
CodeCircuit
, a white-box verification framework that analyzes the line-level attribution graph of the generated code. We adopt the instrumentation of sparse autoencoders (transcoders) to decompose complex residual flows into a causal graph of interpretable features. Using
CodeCircuit
, we conduct an extensive analysis across diverse programming languages (Python, C++, Java).
Although line-level attribution graphs are computationally demanding, this detail is crucial for exposing failure mechanisms.
CodeCircuit
thus serves as a
scientific instrument
for precise auditing and debugging, providing mechanistic insights into code generation beyond what coarser methods can reveal.
Our results reveal that, within a fixed model, internal attribution structures correlate with code correctness across multiple programming languages.
We find that correct and incorrect code exhibit systematic topological differences in their attribution graphs (Figure
1
). Consequently,
CodeCircuit
consistently outperforms both black-box methods (e.g., Temperature Scaling;
Shih et al., 2023
) and gray-box methods (e.g., Chain-of-Embedding;
Wang et al., 2024b
) in verification performance. Notably, we demonstrate that these signals are not merely correlational: by performing targeted interventions on the graph’s nodes
(
Meng et al., 2022
;
Meng et al., 2023
)
, we can causally correct erroneous code, proving that the attribution graph captures the functional mechanism of generation. Our contributions are summarized as follows:
•
Assessing Generated Code via Internal Computational Structure.
We investigate the feasibility of evaluating LLM-generated code by examining the model’s internal neural dynamics rather than its surface-level output. By extracting line-level attribution graphs, we demonstrate that code correctness appears to be reflected in structured patterns of internal computation, enabling reliability assessment without external supervision or execution.
•
Shared Signals and Causal Debugging.
We provide empirical evidence that these structural correctness signals are robust across multiple programming languages, suggesting that LLMs learn shared computational circuits independent of surface syntax. Furthermore, we establish the causal nature of these features: by intervening on specific nodes within the attribution graph, we demonstrate the ability to patch the model’s internal logic, moving from passive verification to active mechanistic debugging.
2
Preliminary
Mechanistic Interpretability via Attribution Graph.
Attribution Graphs (AGs;
Ameisen et al., 2025
) provide a causal, linear decomposition of a transformer model’s computation for a specific input prompt, enabling the tracing of information flow through interpretable features. The construction of an AG is predicated on the local replacement model, which substitutes the standard Multi-Layer Perceptrons (MLPs) with a set of Per-Layer Transcoders (PLTs). A PLT creates a sparse feature vector
f
(
l
)
f^{(l)}
at layer
l
l
from the residual stream
x
(
l
)
x^{(l)}
via an encoder
W
e
​
n
​
c
(
l
)
W_{enc}^{(l)}
and a non-linearity
σ
\sigma
(e.g., TopK or ReLU):
f
(
l
)
=
σ
⁡
(
W
e
​
n
​
c
(
l
)
​
x
(
l
)
+
b
e
​
n
​
c
(
l
)
)
.
f^{(l)}=\sigma(W_{enc}^{(l)}x^{(l)}+b_{enc}^{(l)}).
(1)
Crucially, these features are trained to reconstruct the local MLP output (or residual update) via decoder weights
W
d
​
e
​
c
(
l
)
W_{dec}^{(l)}
. Unlike standard Autoencoders, PLTs disentangle the superposition of features in the dense activation space:
m
^
(
l
)
=
W
d
​
e
​
c
(
l
)
​
f
(
l
)
+
b
d
​
e
​
c
(
l
)
.
\hat{m}^{(l)}=W_{dec}^{(l)}f^{(l)}+b_{dec}^{(l)}.
(2)
The local replacement model is constructed by replacing the true MLP output
m
(
l
)
m^{(l)}
with an error-corrected PLT output
m
^
a
​
d
​
j
(
l
)
=
m
^
(
l
)
+
(
m
(
l
)
−
m
^
(
l
)
)
\hat{m}^{(l)}_{adj}=\hat{m}^{(l)}+(m^{(l)}-\hat{m}^{(l)})
, where the error term
(
m
(
l
)
−
m
^
(
l
)
)
(m^{(l)}-\hat{m}^{(l)})
is computed on the forward pass and effectively acts as a bias node. This yields a locally linearized computation in which downstream quantities are linear functions of feature activations and residual stream components, with attention outputs and normalization statistics treated as fixed. Linearity therefore holds with respect to the substituted MLP pathways under the frozen forward pass.
The AG is a directed acyclic graph
G
=
(
V
,
E
)
G=(V,E)
where nodes
V
V
include active PLT features, token embeddings, error terms, and output logits. An edge
w
i
​
j
∈
E
w_{ij}\in E
from a source node
i
i
(at layer
l
l
) to a target node
j
j
(at layer
l
′
>
l
l^{\prime}>l
) represents the linear contribution of node
i
i
’s activation to the pre-activation of node
j
j
under the locally linearized computation. Let
a
i
a_{i}
denote the activation of node
i
i
, and let
v
o
​
u
​
t
,
i
v_{out,i}
and
v
i
​
n
,
j
v_{in,j}
denote the residual stream directions associated with the output of node
i
i
and the input of node
j
j
, respectively. The contribution is defined as:
w
i
​
j
=
a
i
​
v
i
​
n
,
j
⊤
​
J
i
​
j
​
v
o
​
u
​
t
,
i
,
w_{ij}=a_{i}\,v_{in,j}^{\top}J_{ij}v_{out,i},
(3)
where
J
i
​
j
J_{ij}
is the Jacobian of the frozen residual stream transformation mapping the output of node
i
i
to the input of node
j
j
, with stop-gradients applied to all nonlinearities. This formulation attributes influence through the residual stream rather than via direct feature-to-feature dependencies.
To enhance interpretability, the graph undergoes a pruning process. Rather than matrix inversion (which is intractable for large feature spaces), nodes are pruned based on their attribution to the final model output. We compute the attribution of every feature node to the correct logit (or a target metric) via a single backward pass. Nodes are retained only if they contribute a significant portion of the total influence relative to a threshold
τ
\tau
. Edges with negligible weights are similarly pruned, resulting in a sparse, mechanistically faithful circuit responsible for the model’s behavior.
Problem Formulation.
We consider the task of verifying the correctness of a code snippet
𝒞
\mathcal{C}
generated by a large language model in response to a natural language specification
𝒮
\mathcal{S}
. Formally, the code snippet is decomposed into a sequence of
N
N
discrete logical steps (e.g., lines of code), denoted as
𝒞
=
{
s
1
,
s
2
,
…
,
s
N
}
\mathcal{C}=\{s_{1},s_{2},\dots,s_{N}\}
. Our objective is to predict the correctness label
y
i
∈
{
0
,
1
}
y_{i}\in\{0,1\}
for each step
s
i
s_{i}
, where
y
i
=
1
y_{i}=1
indicates that the
i
i
-th step is logically sound and consistent with the specification
𝒮
\mathcal{S}
, and
y
i
=
0
y_{i}=0
otherwise.
Unlike traditional verification methods that rely on the execution output of the entire snippet
𝒞
\mathcal{C}
, we formulate code verification as a
mechanistic sequence labeling problem
. For each step
s
i
s_{i}
, the LLM’s internal computation is represented by a high-dimensional activation trace. We map this trace onto an interpretable basis to construct a step-level attribution graph
𝒢
i
=
(
V
i
,
E
i
)
\mathcal{G}_{i}=(V_{i},E_{i})
, which serves as a formal proxy for the model’s latent algorithmic execution. The problem is thus transformed into learning a diagnostic mapping
F
:
𝒢
i
→
y
i
F:\mathcal{G}_{i}\to y_{i}
.
This mapping
F
F
is decomposed into two successive operations. First, a structural encoding function
Φ
\Phi
distills the complex, variable-sized topology of the attribution graph into a fixed-size feature vector
𝐱
i
∈
ℝ
d
\mathbf{x}_{i}\in\mathbb{R}^{d}
:
𝐱
i
=
Φ
⁡
(
𝒢
i
)
,
\mathbf{x}_{i}=\Phi(\mathcal{G}_{i}),
(4)
where
𝐱
i
\mathbf{x}_{i}
captures the structural fingerprints of the computational trajectory, including node composition, information flow density, and topological bottlenecks. Second, a discriminative classifier
h
ϕ
h_{\phi}
, parameterized by
ϕ
\phi
, maps the structural encoding to a correctness probability:
y
^
i
=
h
ϕ
​
(
𝐱
i
)
=
P
⁡
(
y
i
=
1
∣
𝒢
i
;
ϕ
)
.
\hat{y}_{i}=h_{\phi}(\mathbf{x}_{i})=P(y_{i}=1\mid\mathcal{G}_{i};\phi).
(5)
The learning objective is to find the optimal parameters
ϕ
∗
\phi^{*}
that minimize the empirical risk over a dataset of
M
M
labeled code steps:
ϕ
∗
=
arg
⁡
min
ϕ
​
1
M
​
∑
j
=
1
M
ℒ
⁡
(
h
ϕ
​
(
Φ
⁡
(
𝒢
j
)
)
,
y
j
)
,
\phi^{*}=\arg\min_{\phi}\frac{1}{M}\sum_{j=1}^{M}\mathcal{L}(h_{\phi}(\Phi(\mathcal{G}_{j})),y_{j}),
(6)
where
ℒ
\mathcal{L}
is a standard cross-entropy loss function. This formulation enables the detection of logical fallacies at a granular, step-by-step level, grounded in the structural pathologies of the model’s internal reasoning pathways.
3
CodeCircuit
: Mechanistic Code Verification
Figure 2:
Overview of the
CodeCircuit
framework.
CodeCircuit
maps an LLM’s internal dynamics into a line-level Attribution Graph to detect errors. By extracting structural features, including global, topological, and node states, the framework identifies latent structural fingerprints of validity. NL represents the next line.
The fundamental premise of our framework
CodeCircuit
(Figure
2
) is that the correctness of a generated code sequence is intrinsically encoded within the
latent algorithmic trajectory
of the language model. Traditional verification paradigms treat the model as an opaque function, focusing on extrinsic execution outcomes that often fail to capture the underlying causal mechanisms of logical fallacies. In contrast, building upon the mechanistic verification paradigm established by
Zhao et al. (2025)
, we propose a white-box framework that audits the structural integrity of the model’s internal reasoning pathways. By projecting high-dimensional neural activations onto an interpretable basis, we extend their approach to identify the specific structural fingerprints of algorithmic success or failure in code, shifting the diagnostic focus from output observation to internal process auditing.
3.1
Latent Algorithmic Tracing via Attribution Graphs
To expose the hidden computational logic of code generation, we construct a step-level attribution graph
𝒢
i
=
(
V
i
,
E
i
)
\mathcal{G}_{i}=(V_{i},E_{i})
for each discrete logical step
i
i
. This graph serves as a formal causal map of the model’s mechanistic reasoning pathway. As established in the preliminaries, we utilize a local replacement model where standard MLP layers are substituted by PLTs. This transformation projects the residual stream into a sparse, interpretable feature space
f
(
l
)
f^{(l)}
, where individual dimensions correspond to discrete algorithmic primitives. The resulting graph
𝒢
i
\mathcal{G}_{i}
captures the linear flow of information from input embeddings
V
e
​
m
​
b
V_{emb}
through these latent features
V
f
​
e
​
a
​
t
V_{feat}
to the final logit output. To account for the portion of the computation not captured by the interpretable features, we explicitly include error nodes
V
e
​
r
​
r
V_{err}
, defined as the residual difference between the true MLP output and its local PLT reconstruction:
e
(
l
)
=
m
(
l
)
−
(
W
d
​
e
​
c
(
l
)
​
f
(
l
)
+
b
d
​
e
​
c
(
l
)
)
.
e^{(l)}=m^{(l)}-(W_{dec}^{(l)}f^{(l)}+b_{dec}^{(l)}).
(7)
Including
V
e
​
r
​
r
V_{err}
allows for a quantitative assessment of the mechanical faithfulness of the reasoning pathway, where the total influence of error nodes serves as a proxy for the epistemic uncertainty inherent in the model’s latent algorithm.
3.2
Structural Feature Extraction and Pathological Analysis
Inspired by
Zhao et al. (2025)
, we hypothesize that logical errors in code generation manifest as structural anomalies within the attribution graph’s topology. To capture these, we define a comprehensive feature extraction mapping
Φ
:
𝒢
i
→
𝐱
i
\Phi:\mathcal{G}_{i}\to\mathbf{x}_{i}
that distills the complex topology of
𝒢
i
\mathcal{G}_{i}
into a fixed-size diagnostic vector
𝐱
i
\mathbf{x}_{i}
. A complete enumeration of the statistics-, activation-, and topology-based features included in
𝐱
i
\mathbf{x}_{i}
is provided in Appendix
A.3
. This mapping systematically analyzes the circuit across multiple hierarchical dimensions of the computational trajectory.
The first dimension concerns the mechanical composition and faithfulness of the circuit. Beyond simple cardinality measures of the node set
V
i
V_{i}
and edge set
E
i
E_{i}
, we define the
error-to-feature influence ratio
η
i
\eta_{i}
to quantify the model’s reliance on unexplained components. Let
w
u
​
v
w_{uv}
denote the attribution weight of the edge from node
u
u
to node
v
v
; the cumulative error influence is formulated as:
η
i
=
∑
u
∈
V
e
​
r
​
r
∑
v
∈
V
i
|
w
u
​
v
|
∑
u
∈
V
f
​
e
​
a
​
t
∑
v
∈
V
i
|
w
u
​
v
|
.
\eta_{i}=\frac{\sum_{u\in V_{err}}\sum_{v\in V_{i}}|w_{uv}|}{\sum_{u\in V_{feat}}\sum_{v\in V_{i}}|w_{uv}|}.
(8)
A high value of
η
i
\eta_{i}
indicates a computation driven by opaque heuristics rather than interpretable algorithmic steps, suggesting a higher probability of logical fragility.
Furthermore, we analyze the global structure of the reasoning pathway. We compute the graph density
ρ
i
=
|
E
i
|
/
(
|
V
i
|
​
(
|
V
i
|
−
1
)
)
\rho_{i}=|E_{i}|/(|V_{i}|(|V_{i}|-1))
and the number of connected components to evaluate whether the latent algorithm is executing a unified or fragmented process. To capture the hierarchical and modular nature of the computation, we calculate the average clustering coefficient
C
i
C_{i}
, which measures the degree to which nodes in the graph tend to cluster together:
C
i
=
1
|
V
i
|
​
∑
v
∈
V
i
2
​
|
{
(
u
,
w
)
∈
E
i
u
,
w
∈
N
⁡
(
v
)
(
u
,
w
)
∈
E
i
}
|
k
v
​
(
k
v
−
1
)
,
C_{i}=\frac{1}{|V_{i}|}\sum_{v\in V_{i}}\frac{2\left|\left\{\begin{subarray}{c}(u,w)\in E_{i}\\
u,w\in N(v)\\
(u,w)\in E_{i}\end{subarray}\right\}\right|}{k_{v}(k_{v}-1)},
(9)
where
N
⁡
(
v
)
N(v)
is the neighborhood of node
v
v
and
k
v
k_{v}
is its degree. In the context of code generation, high modularity often corresponds to the execution of independent sub-tasks, while the presence of disjoint components may indicate fragmented reasoning where the model fails to integrate necessary context into the program state.
To identify critical information bottlenecks and logical hubs within the trajectory, we analyze the distribution of betweenness centrality
C
B
​
(
v
)
C_{B}(v)
and degree centrality. For a node
v
∈
V
i
v\in V_{i}
, the betweenness centrality represents the fraction of all shortest paths between node pairs that pass through
v
v
, formulated as:
C
B
​
(
v
)
=
∑
s
≠
v
≠
t
∈
V
i
σ
s
​
t
​
(
v
)
σ
s
​
t
,
C_{B}(v)=\sum_{s\neq v\neq t\in V_{i}}\frac{\sigma_{st}(v)}{\sigma_{st}},
(10)
where
σ
s
​
t
\sigma_{st}
is the total number of shortest paths from
s
s
to
t
t
and
σ
s
​
t
​
(
v
)
\sigma_{st}(v)
is the number of those paths passing through
v
v
. We aggregate these values into statistical moments, including the mean
μ
⁡
(
C
B
)
\mu(C_{B})
, standard deviation
σ
⁡
(
C
B
)
\sigma(C_{B})
, and maximum value
max
⁡
(
C
B
)
\max(C_{B})
, to characterize the concentration of information flow. A robust algorithmic execution typically exhibits stable, high-centrality features that coordinate state-tracking, whereas an error-prone step may manifest as a fragmented bottleneck with no clear coordination hub.
Finally, we characterize attribution dynamics using a
total logit attribution score
. Instead of relying on shallow connectivity, we aggregate the gradient-based attribution along all paths from a feature node to the final output logits. We extract the statistical profile of these total influence scores
S
S
, where
S
v
S_{v}
represents the integrated gradient of the target probability with respect to feature
v
v
. This allows us to distinguish between features that merely activate and those that functionally drive the deep algorithmic processing essential for correct code generation.
3.3
Diagnostic Classification and Structural Bug Diagnosis
The final stage of our framework involves the training of a diagnostic classifier
h
ϕ
h_{\phi}
that maps the structural vector
𝐱
i
\mathbf{x}_{i}
to a correctness probability
y
^
i
=
h
ϕ
​
(
𝐱
i
)
\hat{y}_{i}=h_{\phi}(\mathbf{x}_{i})
. We utilize a Gradient Boosting Decision Tree (GBDT;
Ke et al., 2017
) architecture, which is particularly effective for handling the heterogeneous, tabular nature of the extracted topological features. The objective is to minimize the cross-entropy loss over a labeled dataset of correct and incorrect code generations:
ℒ
(
ϕ
)
=
−
∑
i
[
y
i
log
(
y
^
i
)
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
y
^
i
)
]
.
\mathcal{L}(\phi)=-\sum_{i}\left[y_{i}\log(\hat{y}_{i})+(1-y_{i})\log(1-\hat{y}_{i})\right].
(11)
Beyond simple binary classification, the GBDT model provides feature importance rankings that enable
structural bug diagnosis
. By identifying which topological properties are most predictive of failure, we can pinpoint the mechanical cause of a logical error. For instance, a high importance score for the error-to-feature ratio
η
i
\eta_{i}
combined with low betweenness centrality for state-tracking features suggests that the model’s failure stems from a lack of interpretable state maintenance. This transforms code verification from a post-hoc execution test into a proactive, mechanistic audit of the model’s latent computational integrity.
4
Experiments
In this section, we empirically validate our central hypothesis: that
code correctness is intrinsic to the model’s latent computational topology and can be diagnosed without external execution.
We structure our evaluation around five primary research questions:
•
RQ1 (Effectiveness):
Can
CodeCircuit
accurately distinguish between correct and incorrect code across diverse programming languages?
•
RQ2 (Generalization):
Do the identified discriminative signals generalize across different programming syntax?
•
RQ3 (Scalability):
Does predictive power of internal signals remain robust as algorithmic complexity increases?
•
RQ4 (Visualization):
Are there visually distinct topological patterns in the internal circuits of correct versus incorrect code?
•
RQ5 (Causal Intervention):
Can targeted interventions on internal failure modes rectify errors in code generation?
4.1
Evaluation Setup
Datasets and Problem Domains.
To ensure cross-lingual robustness, we evaluate
CodeCircuit
across Python, Java, and C++. We utilize the MBPP dataset
(
Austin et al., 2021
)
as the benchmark for Python and curate semantically equivalent task sets for Java and C++ by translating MBPP specifications and generating solutions via Gemma-2-2B-it
(
Team et al., 2024
)
. We use transcoder trained by
(
Lieberum et al., 2024
)
. This alignment ensures that the model operates on identical algorithmic logic across disparate syntaxes. Ground truth labels are derived from GPT-4o
(
OpenAI and others, 2024
)
, where a step is defined as a correct code line. We emphasize that external supervision is used only to obtain evaluation labels and is not required by CodeCircuit during inference. Any functional or logical deviation within a line is treated as a positive instance of failure. Detailed dataset statistics and label distributions are provided in Appendix
A.1
.
The exact prompt templates used for code generation and line-wise labeling, as well as the attribution-graph extraction configuration, are shown in Appendix
B
and
A.2
.
Baselines.
We compare
CodeCircuit
against a suite of established black-box and gray-box metrics. These include Temperature Scaling
(
Shih et al., 2023
)
, Maximum Softmax Probability (MaxProb), Perplexity (PPL), Energy
(
Liu et al., 2020
)
, and Entropy derived from final token logits as measures of surface-level confidence. We also include Chain-of-Embedding (CoE), such as real-space CoE-R, complex-space CoE-C variants
(
Wang et al., 2024b
)
and CoT-Kinetics
(
Bi et al., 2025
)
, as a competitive gray-box baseline to evaluate the consistency of the reasoning process throughout the generation trajectory.
Evaluation Metrics.
Following
Zhao et al. (2025)
, we evaluate verifier performance using AUROC, FPR@95, and AUPR. Since the task focuses on identifying coding errors, incorrect steps are treated as the positive class throughout. Taken together, these metrics characterize ranking quality, error detection strength, and false alarm behavior.
Table 1:
Performance comparison of methods across different programming languages and baselines.
Paradigm
Method
Python
Java
C++
AUROC
↑
\uparrow
AUPR
↑
\uparrow
FPR@95
↓
\downarrow
AUROC
↑
\uparrow
AUPR
↑
\uparrow
FPR@95
↓
\downarrow
AUROC
↑
\uparrow
AUPR
↑
\uparrow
FPR@95
↓
\downarrow
Black-Box
MaxProb
51.25
29.08
97.20
56.29
46.00
91.20
54.06
27.95
93.39
PPL
51.24
29.08
97.20
56.29
46.00
91.20
54.06
27.94
93.39
Entropy
51.42
29.04
96.88
56.56
46.34
89.96
53.16
27.98
93.39
Temp. Scaling
50.86
28.85
97.20
55.65
45.44
92.08
55.79
28.44
91.49
Energy
49.45
25.63
89.10
57.52
45.38
88.38
42.78
23.42
97.71
Gray-Box
CoE-R
50.75
25.22
93.52
49.68
40.07
94.46
59.07
40.17
92.49
CoE-C
51.10
42.91
93.52
52.46
44.76
94.64
56.40
37.72
92.61
CoT-Kinetics
51.41
29.04
96.88
56.57
46.34
89.96
53.16
27.98
93.39
White-Box
Ours
79.89
54.77
77.84
68.06
56.83
79.66
72.21
64.55
80.51
Table 2:
Performance comparison of different methods across Python, C++, and Java test sets. Results are evaluated using AUROC, AUPR, and FPR@95 metrics.
Test Set
Method (Train Set)
Metrics
AUROC
↑
\uparrow
AUPR
↑
\uparrow
FPR@95
↓
\downarrow
Python
Baseline (MaxProb)
51.25
29.08
97.20
CodeCircuit
(Java)
55.42
34.15
94.10
CodeCircuit
(C++)
53.18
31.50
95.82
CodeCircuit (Python)
79.89
54.77
77.84
Java
Baseline (MaxProb)
56.29
46.00
91.20
CodeCircuit
(Python)
62.15
48.33
88.45
CodeCircuit
(C++)
58.74
47.12
90.15
CodeCircuit (Java)
68.06
56.83
79.66
C++
Baseline (MaxProb)
54.06
27.95
93.39
CodeCircuit
(Java)
59.33
36.80
88.24
CodeCircuit
(Python)
57.10
32.55
91.12
CodeCircuit (C++)
72.21
64.55
80.51
4.2
Main Performance
Effectiveness.
We first evaluate the fundamental efficacy of
CodeCircuit
in identifying code errors. This analysis addresses whether internal circuit pathologies provide a more reliable signal for correctness than surface-level heuristics (RQ1). As shown in Table
1
,
CodeCircuit
outperforms all baseline paradigms across Python, Java, and C++, demonstrating the superior reliability of internal circuit pathologies over surface-level heuristics. Specifically, our approach achieves an AUROC of 79.89 in Python, representing a substantial improvement over the best-performing black-box and gray-box methods, which hover around 51.42. This trend is consistent across other metrics and languages; for instance, we achieve an AUPR of 54.77 in Python and 56.83 in Java, nearly doubling the performance of traditional methods like MaxProb or CoT-Kinetics in many cases. Furthermore, our method markedly reduces the FPR@95, maintaining values as low as 80.51 in C++, whereas baselines frequently exceed 90. These results highlight that by leveraging internal model states, we can distinguish correct from erroneous code with far greater precision than methods relying on output probabilities or chain-of-thought consistency.
Generalization.
We investigate the cross-programming language invariance of these structural signatures by conducting transfer experiments across Python, Java, and C++ (RQ2). As shown in Table
2
, our method exhibits robust zero-shot generalization capabilities, consistently outperforming the surface-level baseline (MaxProb) even when the probe is trained on a different programming language. For instance, when testing on the Java set, the probe trained on Python achieves an AUROC of 62.15, marking a 5.86% absolute improvement over the Java-specific MaxProb baseline (56.29). We observe a nuanced transferability across the three languages; notably, the Java-trained probe generalizes effectively to both C++ (59.33 AUROC) and Python (55.42 AUROC), suggesting that the structural patterns captured from Java may encapsulate more fundamental logic common to imperative languages. While a performance gap naturally exists between cross-domain transfer and in-domain training, the consistent superiority of our method over the baseline confirms that code errors manifest through a set of universal structural pathologies. These results suggest that our white-box approach captures fundamental reasoning inconsistencies that transcend language-specific syntax.
Figure 3:
Predictor performance on Python tasks by difficulty, showing
CodeCircuit
’s advantage as complexity increases.
Figure 4:
Feature distributions after PCA for correct (blue) and incorrect (red) code generation in different programming languages.
Before Intervention (Incorrect)
After Intervention (Correct)
def search_insert(nums, target):
def search_insert(nums, target):
low, high = 0, len(nums) - 1
low, high = 0, len(nums) - 1
while low <= high:
while low <= high:
mid = (low + high) // 2
mid = (low + high) // 2
if nums[mid] == target:
if nums[mid] == target:
return mid
return mid
elif nums[mid] < target:
elif nums[mid] < target:
low = mid + 1
low = mid + 1
else:
else:
high = mid
high = mid - 1
return low
return low
Trace:
The model fails to decrement
high
, leading to a potential infinite loop or incorrect insertion index.
Trace:
Suppressing the “greedy” feature allows the model to correctly update the boundary.
Table 3:
Side-by-side comparison of a code reasoning trace
before
and
after
causal intervention. The highlight indicates the point of divergence where suppressing a single
greedy-matching
transcoder feature corrects the model’s internal computational path and restores logical validity.
Scalability
.
To test the robustness of these signals, we analyze how predictive power scales as code complexity and physical length (number of lines
N
∈
{
10
,
20
,
30
}
N\in\{10,20,30\}
) increase (RQ3). As shown in the Figure
3
, the performance advantage of
CodeCircuit
becomes significantly more pronounced as task difficulty grows, with AUROC rising from approximately 80 to nearly 92. While surface-level baselines like MaxProb remain stagnant, our method capitalizes on the richer internal activations provided by longer sequences to more accurately identify circuit pathologies. This suggests that unlike gray-box methods that struggle with consistency, our white-box approach becomes increasingly reliable in more demanding and complex computational contexts.
4.3
Visual Analysis (RQ4)
To move beyond binary prediction, we conduct a qualitative and fine-grained analysis of the attribution graphs to uncover the “structural fingerprints” of specific failure modes. Following
Zhao et al. (2025)
, we visualize the separation between correct and erroneous computational trajectories using manifold projection techniques and case studies of individual circuits in Figure
4
. The plots reveal that correct steps often form a dense subset within the broader distribution of incorrect steps. This spatial overlap suggests many failures are structural near misses, maintaining similar graph topologies to valid code. Nevertheless, a distinct zone of computational integrity exists where only correct samples reside. This observation is consistent with the findings of
Zhao et al. (2025)
for reasoning tasks. This consistency across languages confirms that our graph features capture universal signatures of correctness that transcend specific programming language.
4.4
Causal Intervention (RQ5)
Finally, we move beyond passive verification to test the causal nature of the identified structural features. Consistent with recent findings by
Zhao et al. (2025)
in the domain of reasoning, we hypothesize that the anomalies detected by
CodeCircuit
are not merely correlational byproducts but active drivers of the model’s generation. To validate this, we perform a “mechanistic patching” experiment—intervening on specific nodes in the attribution graph to correct algorithmic logic in real-time.
We illustrate this via a case study on a classic boundary condition failure. Given a prompt to implement a binary search algorithm, the model generated the incorrect update logic
high = mid
, a common bug that leads to infinite loops, instead of the correct
high = mid - 1
(Table
3
).
CodeCircuit
flagged this step as structurally anomalous. Investigating the attribution graph revealed that the error was driven by a specific transcoder feature in the middle layers, which semantically corresponded to a “greedy matching” heuristic that overrode the precise arithmetic state maintenance required for the loop invariant.
To test causality, we performed a targeted intervention using activation clamping. We re-ran the generation and verified that by placing a forward hook to suppress (zero out) this maladaptive feature, the model’s trajectory was immediately corrected. As shown in Table
3
, the intervention successfully steered the model to generate
high = mid - 1
and proceed to a functionally correct solution. We also observed successful corrections via feature
amplification
, specifically by boosting under-active features associated with variable binding context.
These results corroborate the causal link between latent circuit activation and reasoning correctness established by
Zhao et al. (2025)
, while extending the phenomenon to the strict syntactic and logical constraints of programming. This serves as a proof-of-concept for
latent debugging
: the ability to fix software bugs not by editing the source code, but by modulating the neural circuitry that generates it.
5
Related Work
5.1
Mechanistic Interpretability
Mechanistic interpretability
(
Gao et al., 2025
;
Michaud et al., 2024
;
Rai et al., 2024b
)
aims to reverse-engineer neural networks into their underlying computational algorithms. The field was largely formalized by the “circuits" framework
(
Olah et al., 2020
)
, which posits that features are the fundamental units of representation and are connected by weights to form circuits. In the context of Transformers,
Elhage et al. (2021)
introduced a mathematical framework that identified “induction heads” as the mechanism for in-context learning. This paradigm has enabled the discovery of specific circuits for tasks such as indirect object identification
(
Wang et al., 2022
)
and modular arithmetic
(
Nanda et al., 2023
)
. To address the challenge of polysemanticity, where single neurons represent multiple unrelated concepts
(
Olah et al., 2017
)
, recent research has leveraged the Linear Representation Hypothesis
(
Elhage et al., 2022
)
and Sparse Autoencoders to decompose activations into monosemantic features
(
Bricken et al., 2023
;
Cunningham et al., 2023
)
. Furthermore, to bridge the gap between manual inspection and large-scale models, automated discovery methods such as ACDC
(
Conmy et al., 2023
)
and LLM-based explanations
(
Bills et al., 2023
)
have been proposed.
5.2
LLM-based Code Generation
LLMs have rapidly advanced from basic code completion utilities to sophisticated systems for automated software engineering
(
Liu et al., 2024a
;
He et al., 2025b
;
Li et al., 2023
;
Wang et al., 2023a
;
Hui et al., 2024
)
. The initial phase of this evolution was marked by the development of foundational models, such as CodeLlama
(
Rozière et al., 2023
)
and DeepSeek-Coder
(
Guo et al., 2024
)
, which established new performance baselines. These models were typically trained on massive, high-quality code corpora and leveraged long-context windows to capture extensive code dependencies.
A subsequent research direction has focused on enhancing the functional correctness of generated code, moving beyond conventional open-loop generation. This involves the integration of execution-based feedback and self-debugging mechanisms
(
Chen et al., 2024
;
Jiang et al., 2024
)
, where the model iteratively refines its proposed solution based on signals derived from compilers, linters, or test case execution.
More recently, the scope of LLM-based code generation has expanded from isolated code snippets to full project-level development. The emergence of agentic frameworks, capable of autonomously addressing real-world software issues, has been a significant development. The capabilities of these agents are rigorously evaluated using benchmarks like SWE-bench
(
Jimenez et al., 2023
)
and platforms such as OpenDevin
(
Wang et al., 2024a
)
.
6
Conclusion
This work asks a single question: whether the correctness of LLM-generated code can be inferred from the model’s internal computation, without relying on execution, tests, or external judges. This question is motivated by the growing use of LLMs in settings where external evaluation is costly or incomplete, and where reliability must be assessed from the generation process itself rather than from downstream outcomes.
Through a systematic analysis based on line-level attribution graphs, we show that this is indeed possible. Correct and incorrect code exhibit consistent and distinguishable internal structures across programming languages, indicating that code correctness is encoded in the model’s internal representations. These results suggest that internal analysis provides a viable and general approach to assessing code correctness, and open the door to reliability evaluation methods grounded directly in model behavior rather than external supervision.
Impact Statement
This work contributes to the advancement of reliable and interpretable machine learning, specifically in the domain of automated software engineering. As LLMs are increasingly deployed to generate code for critical infrastructure and applications, ensuring their correctness is of paramount societal importance. Our proposed framework,
CodeCircuit
, advances this goal by shifting verification from opaque, black-box outcomes to transparent, mechanistic processes. By exposing the internal “circuits” of code generation, this work aids in the early detection of logical failures and software vulnerabilities that standard execution-based testing might miss. Furthermore, our focus on interpretability aligns with the broader goal of developing trustworthy AI systems that are understandable by humans. However, we note that while mechanistic verification improves reliability, it should currently serve as an aid to, rather than a replacement for, human review and rigorous software testing protocols.
References
Ameisen
et al.
(2025)
E. Ameisen, J. Lindsey, A. Pearce, W. Gurnee, N. L. Turner, B. Chen, C. Citro, D. Abrahams, S. Carter, B. Hosmer, J. Marcus, M. Sklar, A. Templeton, T. Bricken, C. McDougall, H. Cunningham, T. Henighan, A. Jermyn, A. Jones, A. Persic, Z. Qi, T. Ben Thompson, S. Zimmerman, K. Rivoire, T. Conerly, C. Olah, and J. Batson
Circuit tracing: revealing computational graphs in language models
.
Transformer Circuits Thread
.
External Links:
Link
Cited by:
§1
,
§2
.
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. V. Le,
et al.
Program synthesis with large language models
.
arXiv preprint arXiv:2108.07732
.
Cited by:
§1
,
§4.1
.
Bi
et al.
(2025)
J. Bi, D. Yan, Y. Wang, W. Huang, H. Chen, G. Wan, M. Ye, X. Xiao, H. Schuetze, V. Tresp,
et al.
Cot-kinetics: a theoretical modeling assessing lrm reasoning process
.
arXiv preprint arXiv:2505.13408
.
Cited by:
§4.1
.
Bills
et al.
(2023)
S. Bills, N. Cammarata, D. Mossing, H. Tillman, L. Gao, G. Goh, I. Sutskever, J. Leike, J. Wu, and W. Saunders
Language models can explain neurons in language models
.
Note:
https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html
Cited by:
§5.1
.
Bricken
et al.
(2023)
T. Bricken, A. Templeton, J. Batson, B. Chen, A. Jermyn, T. Conerly, N. Turner, C. Anil, C. Denison, A. Askell,
et al.
Towards monosemanticity: decomposing language models with dictionary learning
.
Transformer Circuits Thread
2
.
Cited by:
§5.1
.
Bui
et al.
(2025)
T. Bui, T. T. Vu, T. Nguyen, S. Nguyen, and H. D. Vo
Correctness assessment of code generated by large language models using internal representations
.
arXiv preprint arXiv:2501.12934
.
Cited by:
§1
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
et al.
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
Cited by:
§1
.
Chen
et al.
(2024)
X. Chen, M. Lin, N. Schärli, and D. Zhou
Teaching large language models to self-debug
.
In
International Conference on Learning Representations (ICLR)
,
Cited by:
§5.2
.
Conmy
et al.
(2023)
A. Conmy, A. Mavor-Parker, A. Lynch, S. Heimersheim, and A. Garriga-Alonso
Towards automated circuit discovery for mechanistic interpretability
.
Advances in Neural Information Processing Systems
36
,
pp. 16318–16352
.
Cited by:
§5.1
.
Cunningham
et al.
(2023)
H. Cunningham, A. Ewart, L. Riggs, R. Huben, and L. Sharkey
Sparse autoencoders find highly interpretable features in language models
.
arXiv preprint arXiv:2309.08600
.
Cited by:
§5.1
.
Dong
et al.
(2025)
Y. Dong, J. Ding, X. Jiang, G. Li, Z. Li, and Z. Jin
Codescore: evaluating code generation by learning code execution
.
ACM Transactions on Software Engineering and Methodology
34
(
3
),
pp. 1–22
.
Cited by:
§1
.
Dunefsky
et al.
(2024)
J. Dunefsky, P. Chlenski, and N. Nanda
Transcoders find interpretable LLM feature circuits
.
In
The Thirty-eighth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.
Elhage
et al.
(2022)
N. Elhage, T. Hume, C. Olsson, N. Nanda, T. Henighan, S. Johnston, S. ElShowk, N. Joseph, N. DasSarma, B. Mann,
et al.
Softmax linear units. transformer circuits thread
.
Cited by:
§5.1
.
Elhage
et al.
(2021)
N. Elhage, N. Nanda, C. Olsson, T. Henighan, N. Joseph, B. Mann, A. Askell, Y. Bai, A. Chen, T. Conerly,
et al.
A mathematical framework for transformer circuits
.
Transformer Circuits Thread
1
(
1
),
pp. 12
.
Cited by:
§5.1
.
Gao
et al.
(2025)
L. Gao, A. Rajaram, J. Coxon, S. V. Govande, B. Baker, and D. Mossing
Weight-sparse transformers have interpretable circuits
.
External Links:
2511.13653
,
Link
Cited by:
§1
,
§5.1
.
Guo
et al.
(2024)
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang,
et al.
DeepSeek-coder: when the large language model meets programming–the rise of code intelligence
.
arXiv preprint arXiv:2401.14196
.
Cited by:
§1
,
§5.2
.
Hanna
et al.
(2025)
M. Hanna, M. Piotrowski, J. Lindsey, and E. Ameisen
Circuit-tracer
.
Note:
https://github.com/safety-research/circuit-tracer
The first two authors contributed equally and are listed alphabetically.
Cited by:
§A.2
.
He
et al.
(2025a)
J. He, J. Shi, T. Y. Zhuo, C. Treude, J. Sun, Z. Xing, X. Du, and D. Lo
LLM-as-a-judge for software engineering: literature review, vision, and the road ahead
.
arXiv preprint arXiv:2510.24367
.
Cited by:
§1
.
He
et al.
(2025b)
Y. He, C. Huang, Z. Li, J. Huang, and Y. Yang
VisPlay: self-evolving vision-language models from images
.
arXiv preprint arXiv:2511.15661
.
Cited by:
§1
,
§5.2
.
Hendrycks
et al.
(2021)
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song,
et al.
Measuring coding challenge competence with APPS
.
In
Advances in Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track
,
Cited by:
§1
.
Huang
et al.
(2025)
Y. Huang, L. Ma, K. Nishikino, and T. Akazaki
Risk assessment framework for code llms via leveraging internal states
.
In
Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering
,
pp. 432–443
.
Cited by:
§1
.
Hui
et al.
(2024)
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Dang,
et al.
Qwen2.5-coder technical report
.
arXiv preprint arXiv:2409.12186
.
Cited by:
§5.2
.
Jiang
et al.
(2025)
H. Jiang, Y. Chen, Y. Cao, H. Lee, and R. T. Tan
Codejudgebench: benchmarking llm-as-a-judge for coding tasks
.
arXiv preprint arXiv:2507.10535
.
Cited by:
§1
.
Jiang
et al.
(2024)
X. Jiang, J. Dong, Y. Wang, Y. Zheng, L. Shang, G. Li, Z. Jin, and L. Jiao
Self-planning code generation with large language models
.
ACM Transactions on Software Engineering and Methodology
33
(
7
).
External Links:
Document
Cited by:
§5.2
.
Jimenez
et al.
(2023)
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Niranjan,
et al.
SWE-bench: can language models resolve real-world github issues?
.
arXiv preprint arXiv:2310.06770
.
Cited by:
§5.2
.
Ke
et al.
(2017)
G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T. Liu
Lightgbm: a highly efficient gradient boosting decision tree
.
Advances in neural information processing systems
30
.
Cited by:
§3.3
.
Khan
et al.
(2024)
M. A. M. Khan, M. S. Bari, X. L. Do, W. Wang, M. R. Parvez, and S. Joty
Xcodeeval: an execution-based large scale multilingual multitask benchmark for code understanding, generation, translation and retrieval
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
pp. 6766–6805
.
Cited by:
§1
.
Li
et al.
(2023)
R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou, M. Marone, C. Akiki, J. Li, J. Chim,
et al.
StarCoder: may the source be with you!
.
arXiv preprint arXiv:2305.06161
.
Cited by:
§5.2
.
Lieberum
et al.
(2024)
T. Lieberum, S. Rajamanoharan, A. Conmy, L. Smith, N. Sonnerat, V. Varma, J. Kramar, A. Dragan, R. Shah, and N. Nanda
Gemma scope: open sparse autoencoders everywhere all at once on gemma 2
.
In
Proceedings of the 7th BlackboxNLP Workshop: Analyzing and Interpreting Neural Networks for NLP
,
Y. Belinkov, N. Kim, J. Jumelet, H. Mohebbi, A. Mueller, and H. Chen (Eds.)
,
Miami, Florida, US
,
pp. 278–300
.
External Links:
Link
,
Document
Cited by:
§4.1
.
Liu
et al.
(2024a)
A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan,
et al.
Deepseek-v3 technical report
.
arXiv preprint arXiv:2412.19437
.
Cited by:
§1
,
§5.2
.
Liu
et al.
(2023)
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
Advances in Neural Information Processing Systems
36
,
pp. 21558–21572
.
Cited by:
§1
.
Liu
et al.
(2024b)
J. Liu, S. Xie, J. Wang, Y. Wei, Y. Ding, and L. Zhang
Evaluating language models for efficient code generation
.
arXiv preprint arXiv:2408.06450
.
Cited by:
§1
.
Liu
et al.
(2020)
W. Liu, X. Wang, J. Owens, and Y. Li
Energy-based out-of-distribution detection
.
Advances in neural information processing systems
33
,
pp. 21464–21475
.
Cited by:
§4.1
.
Madaan
et al.
(2023)
A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, S. Yang,
et al.
Self-refine: iterative refinement with self-feedback
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Cited by:
§1
.
Meng
et al.
(2022)
K. Meng, D. Bau, A. Andonian, and Y. Belinkov
Locating and editing factual associations in GPT
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Cited by:
§1
.
Meng
et al.
(2023)
K. Meng, D. Bau, A. Andonian, and Y. Belinkov
Mass-editing memory in a transformer
.
In
International Conference on Learning Representations (ICLR)
,
Cited by:
§1
.
Michaud
et al.
(2024)
E. J. Michaud, I. Liao, V. Lad, Z. Liu, A. Mudide, C. Loughridge, Z. C. Guo, T. R. Kheirkhah, M. Vukelić, and M. Tegmark
Opening the ai black box: program synthesis via mechanistic interpretability
.
arXiv preprint arXiv:2402.05110
.
Cited by:
§1
,
§5.1
.
Nanda
et al.
(2023)
N. Nanda, L. Chan, T. Lieberum, J. Smith, and J. Steinhardt
Progress measures for grokking via mechanistic interpretability
.
arXiv preprint arXiv:2301.05217
.
Cited by:
§5.1
.
Olah
et al.
(2020)
C. Olah, N. Cammarata, L. Schubert, G. Goh, M. Petrov, and S. Carter
Zoom in: an introduction to circuits
.
Distill
5
(
3
),
pp. e00024–001
.
Cited by:
§5.1
.
Olah
et al.
(2017)
C. Olah, A. Mordvintsev, and L. Schubert
Feature visualization
.
Distill
2
(
11
),
pp. e7
.
Cited by:
§5.1
.
OpenAI
et al.
(2024)
OpenAI
et al.
GPT-4o system card
.
External Links:
2410.21276
,
Link
Cited by:
§4.1
.
Patel
et al.
(2025)
S. Patel, A. Yadavally, H. Dhulipala, and T. Nguyen
Planning a large language model for static detection of runtime errors in code snippets
.
In
Proceedings of the IEEE/ACM 47th International Conference on Software Engineering (ICSE 2025)
,
pp. 872–884
.
External Links:
Document
Cited by:
§1
.
Rai
et al.
(2024a)
D. Rai, Y. Zhou, S. Feng, A. Saparov, and Z. Yao
A practical review of mechanistic interpretability for transformer-based language models
.
arXiv preprint arXiv:2407.02646
.
Cited by:
§1
.
Rai
et al.
(2024b)
D. Rai, Y. Zhou, S. Feng, A. Saparov, and Z. Yao
A practical review of mechanistic interpretability for transformer-based language models
.
arXiv preprint arXiv:2407.02646
.
Cited by:
§5.1
.
Rozière
et al.
(2023)
B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan,
et al.
Code llama: open foundation models for code
.
arXiv preprint arXiv:2308.12950
.
Cited by:
§1
,
§5.2
.
Sharkey
et al.
(2025)
L. Sharkey, B. Chughtai, J. Batson, J. Lindsey, J. Wu, L. Bushnaq, N. Goldowsky-Dill, S. Heimersheim, A. Ortega, J. Bloom,
et al.
Open problems in mechanistic interpretability
.
arXiv preprint arXiv:2501.16496
.
Cited by:
§1
.
Shih
et al.
(2023)
A. Shih, D. Sadigh, and S. Ermon
Long horizon temperature scaling
.
In
International conference on machine learning
,
pp. 31422–31434
.
Cited by:
§1
,
§4.1
.
Shinn
et al.
(2023)
N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao
Reflexion: language agents with verbal reinforcement learning
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Cited by:
§1
.
Team
et al.
(2024)
G. Team, M. Riviere, S. Pathak, P. G. Sessa, C. Hardin, S. Bhupatiraju, L. Hussenot, T. Mesnard, B. Shaber, A. Haber,
et al.
Gemma 2: improving open language models at a practical size
.
arXiv preprint arXiv:2408.00118
.
Cited by:
§4.1
.
Templeton
et al.
(2024)
A. Templeton, T. Conerly, J. Marcus, J. Lindsey, T. Bricken, B. Chen, A. Pearce, C. Citro, E. Ameisen, A. Jones, H. Cunningham, N. L. Turner, C. McDougall, M. MacDiarmid, C. D. Freeman, T. R. Sumers, E. Rees, J. Batson, A. Jermyn, S. Carter, C. Olah, and T. Henighan
Scaling monosemanticity: extracting interpretable features from claude 3 sonnet
.
Transformer Circuits Thread
.
External Links:
Link
Cited by:
§1
.
Wang
et al.
(2022)
K. Wang, A. Variengien, A. Conmy, B. Shlegeris, and J. Steinhardt
Interpretability in the wild: a circuit for indirect object identification in gpt-2 small
.
arXiv preprint arXiv:2211.00593
.
Cited by:
§5.1
.
Wang
et al.
(2024a)
X. Wang, B. Li, and G. Neubig
OpenDevin: an open platform for ai software developers as generalist agents
.
arXiv preprint arXiv:2407.16741
.
Cited by:
§1
,
§5.2
.
Wang
et al.
(2024b)
Y. Wang, P. Zhang, B. Yang, D. F. Wong, and R. Wang
Latent space chain-of-embedding enables output-free llm self-evaluation
.
arXiv preprint arXiv:2410.13640
.
Cited by:
§1
,
§4.1
.
Wang
et al.
(2023a)
Y. Wang, H. Le, A. D. Gotmare, N. D. Bui, J. Li, and S. C. Hoi
CodeT5+: open code large language models for code understanding and generation
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
pp. 1069–1088
.
Cited by:
§5.2
.
Wang
et al.
(2023b)
Z. Wang, S. Zhou, D. Fried, and G. Neubig
Execution-based evaluation for open-domain code generation
.
In
Findings of the Association for Computational Linguistics: EMNLP 2023
,
pp. 1271–1290
.
Cited by:
§1
.
Zhang
et al.
(2025)
Y. Zhang, W. Du, D. Jin, J. Fu, and Z. Jin
Finite state automata inside transformers with chain-of-thought: a mechanistic study on state tracking
.
In
Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL)
,
Cited by:
§1
.
Zhao
et al.
(2025)
Z. Zhao, Y. Koishekenov, X. Yang, N. Murray, and N. Cancedda
Verifying chain-of-thought reasoning via its computational graph
.
arXiv preprint arXiv:2510.09312
.
Cited by:
§1
,
§3.2
,
§3
,
§4.1
,
§4.3
,
§4.4
,
§4.4
.
Appendix A
Experimental Settings
A.1
Dataset Statistic
We report the final statistics of our curated multilingual MBPP incremental datasets in Table
4
. Following our evaluation setup in Section
4.1
, we use MBPP as the Python benchmark and construct semantically equivalent C++ and Java task sets by translating the same specifications, ensuring that the three datasets share comparable underlying algorithmic logic while differing only in surface syntax. Each JSONL instance corresponds to one labeled generation record with a binary correctness label (answer
∈
{
0
,
1
}
\in\{0,1\}
), where
1
1
denotes correct and
0
0
denotes wrong. In total, our corpus contains 1,447 Python instances, 3,423 C++ instances, and 3,126 Java instances. The label distribution exhibits noticeable language-dependent skew: Python has the highest correctness ratio (81.6% correct vs. 18.4% incorrect), while C++ and Java are more challenging with substantially higher error rates (C++: 66.8%/33.2%; Java: 61.7%/38.3%). This imbalance motivates us to evaluate
CodeCircuit
across languages and to study whether attribution-graph structural signatures remain predictive under varying error prevalence and programming syntax.
Dataset
Total Steps
% Correct
% Incorrect
C++
3,423
66.8%
33.2%
Python
1,447
81.6%
18.4%
Java
3,126
61.7%
38.3%
Table 4:
Final statistics of our curated MBPP incremental datasets, showing the number of instances and the distribution of correct/incorrect labels.
A.2
Experimental Hyperparameter
For attribution-graph extraction, we use the ReplacementModel instantiated from the base LLM, Google Gemma-2-2B-IT
1
1
1
https://huggingface.co/google/gemma-2-2b-it
, together with the corresponding GemmaScope transcoder
2
2
2
https://huggingface.co/mntss/gemma-scope-transcoders
, and run all tracing in bfloat16 precision on a single GPU. We use the Circuit-Tracer
(
Hanna et al., 2025
)
library for attribution graph computation. For each input prompt, we construct an attribution graph with the following settings: we attribute at most 10 output logits and target a cumulative logit probability mass of 0.95. To control graph size and memory footprint, we cap the number of retained feature nodes to 8,192 and compute attributions in mini-batches of size 64. We disable parameter offloading and verbose debugging output. Following the preprocessing in our pipeline, we skip prompts longer than 550 characters to avoid excessively long contexts during tracing. Each resulting attribution graph is serialized in PyTorch format (.pt), and we additionally append a per-instance metadata record in JSONL format, including the task identifier, step index, graph path, and the corresponding binary correctness label.
A.3
Detailed Features
For each line-level attribution graph, we extract a fixed-length feature vector from the pruned subgraph to characterize both node composition and circuit topology. Concretely, we first prune the full attribution graph using an influence-based masking rule with a node-threshold of 0.8, which retains only the most influential nodes according to the cumulative influence scores returned by the pruning routine. Let the pruned node set contain (i) transcoder feature nodes, (ii) error nodes (one error node per layer-position pair), as well as (optionally) token and logit nodes if they survive pruning. We then compute three groups of features.
(1) High-level statistics.
We record (a) the total number of active features in the original graph (the length of the activation-value vector), (b) the number of pruned feature nodes, and (c) the number of pruned error nodes. To summarize output uncertainty, we additionally compute (d) the top-1 logit probability and (e) the entropy of the traced logit probability vector. These quantities capture the overall circuit scale and the model’s output confidence for the step.
(2) Aggregated node and activation statistics.
Using the cumulative influence scores restricted to the pruned nodes, we compute (a) the mean influence over all pruned nodes as a global saliency summary. For error nodes, we compute (b) the total error influence (sum over pruned error nodes) and (c) the mean error influence, serving as a proxy for how much of the computation is routed through unexplained residual components. For pruned feature nodes, we gather their activation values and compute (d) mean activation, (e) maximum activation, and (f) activation standard deviation. Finally, to capture where computation concentrates across depth, we construct a (g) layer-wise histogram of pruned feature counts: for each transformer layer, we count how many retained feature nodes originate from that layer. This produces a length-
L
L
vector, where
L
L
is the number of transformer layers.
(3) Topological and edge-based features of the pruned subgraph.
We form a directed weighted graph from the pruned adjacency matrix, where directed edges represent attributed influence and edge weights are inherited from the adjacency matrix. From edge weights, we compute (a) the sum, (b) mean, and (c) standard deviation of all edge weights, together with (d) the number of edges in the pruned subgraph and (e) the graph density. To capture structural fragmentation, we compute (f) the number of weakly connected components. We then compute centrality-based summaries: (g) mean degree centrality, (h) maximum degree centrality, (i) mean betweenness centrality (computed with edge weights), and (j) maximum betweenness centrality. To quantify global connectivity, we compute (k) the average shortest path length within the largest weakly connected component (set to
−
1
-1
if undefined). Finally, we add a task-relevant routing signal: (l) the shortest-path distance from any retained input-token node to any retained logit node (set to
−
1
-1
if no path exists), which measures how directly input evidence can flow to the output decision within the pruned circuit. For degenerate cases where the pruned graph has fewer than two nodes, we return a default feature vector with zeros and sentinel values (e.g.,
−
1
-1
for undefined shortest-path statistics) to preserve a consistent feature dimensionality across all examples.
Appendix B
Prompt Template
Gemma-2-2B-IT Code Generation Prompt Template
You are a code assistant.
You must output ONLY valid code.
Do not include comments, markdown, explanations, or extra text.
Output only code.
Task prompt:
{TASK_PROMPT}
Table 5:
Prompt template used for code generation. The final input is the concatenation of the fixed instruction block above and the task prompt, separated by two newline characters.
Line-wise Code Correctness Checker Prompt Template
You are a code correctness checker.
Review the provided code line by line. For each line, output a score of 1 or 0 according to the following rules:
1. If the line has a syntax error, output 0.
2. If the line is syntactically correct but violates the coding requirements described in the task, output 0 for that line and all subsequent lines. Once a line violates the requirements, all following lines must also be 0.
3. If the line is syntactically correct and meets the coding requirements so far, output 1.
The code has exactly {N_LINES} lines. Output only a list of exactly {N_LINES} integers, e.g., [1, 1, 0, 1]. Do not include any explanation or extra text.
4. Focus solely on whether the substantive code contains issues, ignoring parameter variable names, function names, and so on.
Task Description:
—
{TASK_DESCRIPTION}
—
Code to Check:
—
{CODE_TO_CHECK}
—
Table 6:
Prompt template used for line-wise correctness scoring. {N_LINES} is computed as the number of lines in {CODE_TO_CHECK}; the model is instructed to output a list of exactly {N_LINES} binary integers.
For code generation, we use a fixed instruction block that strictly constrains the model to output only valid code; this block is concatenated with the task prompt (two newline characters in between) to form the final input, as shown in Table
5
. For correctness checking, we use a single user prompt that instructs a judge model to perform line-wise validation and return an integer list of length {N_LINES}, where any violation at a given line forces that line and all subsequent lines to be scored as 0; we then parse the returned list as per-line correctness signals, as shown in Table
6
.
Appendix C
Limitation
The primary limitation of this approach is the computational overhead required to construct attribution graphs. Unlike black-box methods, our framework involves gradient-based backpropagation and feature projections, which increase time and memory complexity relative to standard inference. For extensive code generation tasks, these requirements may limit real-time deployment. Nevertheless, this bottleneck presents a significant opportunity for algorithmic optimization. Future research could focus on sparse attribution techniques that target only critical logical junctions or utilize low-rank approximations to reduce the cost of Jacobian computations. By transitioning from exhaustive circuit tracing to selective structural diagnostics, the computational burden can be substantially mitigated, paving the way for efficient, white-box verification in production environments.