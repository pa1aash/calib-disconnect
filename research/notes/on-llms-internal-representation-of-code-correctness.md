---
title: On LLMs’ Internal Representation of Code Correctness
id: on-llms-internal-representation-of-code-correctness
tags:
- code-llm-confidence-positioning-d82d00
- probe
- code-correctness
- l2-occupant
- close-occupant
created: '2026-11-09T23:08:43.900464Z'
updated: '2026-11-09T23:27:44.516513Z'
source: https://arxiv.org/html/2512.07404
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:43.899879Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv HTML v3, ICSE 2026). Ribeiro, Spiess, Devanbu, Nadi adapt
  Representation Engineering (LAT: PCA over hidden-state differences of correct vs
  incorrect code at the last token) to pick the correct implementation among 4 candidates.
  Four 7-8B Instruct models (Mistral-7B-Instruct-v0.3, Qwen2.5-Coder-7B-Instruct,
  OpenCoder-8B-Instruct, CodeLlama-7B-Instruct); HumanEval (151 tasks) and BigCodeBench
  (457 tasks); labels are unit tests. Tables 3-4: LAT(Val) beats intrinsic likelihood
  and verbalized (Regular, True/False) by +13.3 to +29.0 pp (BCB) and +8.7 to +26.2
  pp (HE); BCB in-distribution 50.3-56.3% vs random 27.5% (Mistral). RQ2 ranks 10
  self-samples (pass@rank-k) and matches or beats RankEF without execution. Not present:
  any calibration metric (ECE/AUROC/Brier), base-vs-instruct pairs, reasoning models,
  contamination/release-date control, causal steering, per-requirement granularity.
  OOD fitting is erratic (Qwen 12.2%, CodeLlama 22.2% below random on BCB). Close
  occupant of L2 probe-beats-verbal at whole-solution granularity.'
---

On LLMs’ Internal Representation of Code Correctness
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2512.07404v3 [cs.SE] 21 Jan 2026
On LLMs’ Internal Representation of Code Correctness
Francisco Ribeiro
email:
francisco.ribeiro@nyu.edu
Affiliation:
New York University Abu Dhabi
,
Abu Dhabi
,
United Arab Emirates
,
Claudio Spiess
email:
cvspiess@ucdavis.edu
Affiliation:
UC Davis
,
USA
,
Prem Devanbu
email:
ptdevanbu@ucdavis.edu
Affiliation:
UC Davis
,
USA
and
Sarah Nadi
email:
sarah.nadi@nyu.edu
Affiliation:
New York University Abu Dhabi
,
Abu Dhabi
,
United Arab Emirates
© none
Abstract.
Despite the effectiveness of large language models (LLMs) for code generation, they often output incorrect code.

One reason is that model output probabilities are often not well-correlated with correctness, and reflect only the final output of the generation process.
Inspired by findings that LLMs internally encode concepts like truthfulness, this paper explores if LLMs similarly represent code correctness.

Specifically, we identify a correctness representation
inside LLMs by contrasting the hidden states between pairs of correct and incorrect code for the same programming tasks.

By experimenting on four LLMs, we show that exploiting this extracted correctness representation outperforms standard log-likelihood ranking, as well as verbalized model confidence.

Furthermore, we explore how this internal correctness signal can be used to select higher-quality code samples, without requiring test execution.

Ultimately, this work demonstrates how leveraging internal representations can enhance code generation systems and make LLMs more reliable, thus improving confidence in automatically generated code.
1.
Introduction
Large language models (LLMs) are increasingly integrated into software development workflows
Barke et al., 2023
, from code completion in IDEs
Nguyen and Nadi, 2022
;
Mo et al., 2025
to automated code generation systems
Li et al., 2024c
. As LLMs continue to improve, we can expect an increasing reliance on generated code in production systems
Lo, 2023
.
While developers are expected to review and test generated code before deployment, this ideal scenario does not always occur in practice
Zampetti et al., 2019
;
Mcintosh et al., 2016
. Studies have documented cases where incorrect or vulnerable model-generated code has made it into production systems
Fu et al., 2025
;
Majdinasab et al., 2024
.
Real-world incidents such as GitHub Copilot generating a fix for a .NET runtime exception that merely adds superficial bounds checking without addressing the underlying algorithmic issue
Github-Copilot, 2025
, further demonstrate how LLMs can produce functionally inadequate solutions despite appearing reasonable.
Given this reality, it becomes essential to ensure the correctness of LLM-generated code. In this work, we define
code correctness
as adherence to a given problem specification, which can be verified through test execution—the standard measure used in code generation benchmarks and in practice.
Currently, LLMs typically output the most probable code according to their learned token distributions
Svyatkovskiy et al., 2020
;
Zhu et al., 2024
;
Chen et al., 2021
;
Welleck et al., 2024
. However, multiple studies
Spiess et al., 2024
;
Zhang et al., 2023a
;
Zhang et al., 2023b
show that the most probable code often fails to meet correctness, as model probabilities are not always well-correlated with correctness.
Consider the programming task in
Figure 1
, where we show an incorrect and correct solution for the task.
When we compute the probability of CodeLlama 7B generating each solution (
i.e.
, scoring both implementations under the model), the incorrect implementation actually receives a higher probability. In other words, if we rank the solutions based on the probability of CodeLlama 7B producing this code, the wrong version would be ranked higher. Moreover, even if we were to ask the model for its verbalized confidence in the solutions
Tian et al., 2023
(
i.e.
, its articulated certainty about each implementation, such as “Very confident” or “Not confident”), this also failed to prioritize the correct implementation. If LLMs cannot reliably differentiate between correct and incorrect code based on what the model explicitly generates or says, then we cannot be confident in the correctness of their outputs.
⬇
def
solution
(
lst
):
sum_of_odd_elements
=
0
for
i
in
range
(1,
len
(
lst
),
2):
if
lst
[
i
]
%
2
!=
0:
sum_of_odd_elements
+=
lst
[
i
]
return
sum_of_odd_elements
(a)
Incorrect: iterates odd indices
⬇
def
solution
(
lst
):
return
sum
([
x
for
idx
,
x
in
enumerate
(
lst
)
if
idx
%2==0
and
x
%2==1])
(b)
Correct: sums odd elements at even indices
Figure 1
.
Comparison of two candidate solutions for the task
“Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions.”
But what if the true signal of correctness does not lie in what the model shows or tells us, but in what it computes internally? Looking into internal mechanisms for how LLMs interpret different concepts relates to AI interpretability and transparency, an area that has seen a lot of active research in the natural language (NL)
Templeton et al., 2024
;
Bills et al., 2023
;
Mikolov et al., 2013
;
Bolukbasi et al., 2016
;
Schramowski et al., 2019
;
Radford et al., 2017
and computer vision
Hernandez et al., 2022
;
Chen et al., 2023
;
Oquab et al., 2024
domains.
The growing evidence that LLMs internally encode rich conceptual information motivates us to look beyond the probabilistic favoring of outputs and examine the internal mechanisms at work during code generation.
To this end, we turn to representation engineering (RepE)
Zou et al., 2023
, a recent approach in the area of AI transparency. RepE offers a systematic approach for understanding how LLMs encode concepts by analyzing their internal representation spaces. In NL tasks, this approach showed that LLMs possess internal representations of concepts such as truthfulness
Zou et al., 2023
, and importantly, that these internal representations may not always align with the probabilities assigned to the model’s generated outputs. Building on the idea that software, like NL, exhibits statistical regularities that models can learn
Hindle et al., 2012
, it is reasonable to hypothesize that LLMs may also develop internal representations related to code correctness.
Accordingly, this paper addresses the following question:
do LLMs develop internal representations of code correctness that could provide early signals about whether generated code will pass tests, signals that are not necessarily evident from the final output probabilities?
We investigate this question by examining whether we can capture an internal representation of code correctness that can differentiate correct implementations from incorrect ones. Specifically, we aim to answer the following research questions (RQs):
RQ1
Do LLMs possess an internal representation of code correctness?
RQ2
Can leveraging internal correctness representations lead to more effective correctness ranking?
To address these RQs, we extend RepE beyond its original NL setting and adapt it to a programming language domain. We validate our efforts on
HumanEval
Chen et al., 2021
and
BigCodeBench
Zhuo et al., 2024
. Specifically, we compare this technique against standard likelihood-based
Chen et al., 2021
;
Li et al., 2022
;
Spiess et al., 2024
and reflective methods
Tian et al., 2023
;
Lin et al., 2022a
;
Zhou et al., 2023
;
Spiess et al., 2024
;
Kadavath et al., 2022
, demonstrating that RepE outperforms these baselines in identifying correct implementations. Furthermore, we introduce a ranking method based on correctness representations that allows for repeated sampling from an LLM and using RepE to get the most promising solution without running tests.
In this ranking setup, we also compare to an existing learning-based code ranking method, RankEF
Sun et al., 2024
.
In
HumanEval
, applying our strongest correctness-representation ranking variant improves direct pass@1 by 21.3% on average, compared to 17.7% for the strongest existing baseline (RankEF)—a roughly 20% relative gain. In
BigCodeBench
, our strongest ranking variant delivers a 51.1% average improvement over pass@1 compared to 32.5% for random selection (which for
BigCodeBench
surpasses other baselines). In both benchmarks, we close in on the pass@10 upper bound.
To summarize, our contributions are:
1)
Adapting RepE for code, demonstrating its effectiveness across four state-of-the-art LLMs on both
HumanEval
and
BigCodeBench
;
2)
Empirically validating that LLMs encode correctness internally, with representation-based scores outperforming likelihood and reflective metrics in distinguishing correct from incorrect implementations;
3)
a ranking framework that leverages correctness representations that boosts pass@1 by up to 51% without test-time overhead;
4)
A public release of a replication package to facilitate future research:
https://github.com/sanadlab/code-repe
2.
Background
This section presents the foundational concepts for our work: RepE
Zou et al., 2023
for analyzing LLM internals, the question-answering framework we use, and confidence metrics for assessing LLM generations.
2.1.
Representation Engineering (RepE)
RepE
Zou et al., 2023
aims to improve LLM transparency by understanding
how
concepts (
e.g.
, truthfulness) and functions (
e.g.
, honesty) are encoded within neural networks. To do this, RepE analyzes the
inner workings
of these models by examining their hidden states to isolate patterns corresponding to specific concepts or functions.
RepE is a
top-down
approach
Leveson, 2012
that starts with a high-level concept (like
truthfulness
or, in our case,
correctness
) and seeks to find
how
that concept is represented within the model’s global representation space. In contrast,
bottom-up
approaches,
e.g.
, mechanistic interpretability
Conmy et al., 2024
, typically begin by examining the function of individual neurons or small circuits and build an understanding from there. RepE is like studying a city by looking at its neighborhoods and infrastructure (top-down) rather than reverse-engineering each brick and wire (bottom-up).
RepE has been shown to be effective at detecting and controlling issues like dishonesty and bias
Zou et al., 2023
. Crucial to RepE is Linear Artificial Tomography (LAT): a framework for analyzing hidden states in an LLM and extracting meaningful representations. At a high level, imagine LAT as a tool to scan the LLM’s “brain” and identify patterns related to human-understandable concepts such as truthfulness.
By revealing these human-level concepts in LLMs, RepE can be a useful tool for effectively understanding the driving processes behind LLM generations. LAT involves three key steps:
Step 1: Designing the Stimulus and Task
The core of this step is to design stimuli and tasks that elicit distinct neural activity within the LLM. To extract a concept, we want to present stimuli that vary in the amount of that concept and inquire about it. For example, when extracting the concept of truthfulness, we would use scenarios that are definitively true or false to represent contrasting levels.
shows the template underlying this step:
⬇
Consider
the
amount
of
{concept}
in
the
following
:
{stimulus}
The
amount
of
{concept}
is
␣
Listing 1:
Eliciting neural activity – prompt template
Consider
which shows an instantiation of the template for the concept of truthfulness:
⬇
Consider
the
amount
of
truthfulness
in
the
following
:
Question: What is the capital of France?
Answer: Paris.
The
amount
of
truthfulness
is
␣
Listing 2:
Prompt for a correct response (P
c
) – truthfulness
P
c
In
, the answer “Paris” is truthful, as it correctly identifies the capital of France. Conversely,
shows an instantiation of a prompt with an incorrect response where the answer “Marseille” is untruthful since it incorrectly identifies the capital of France.
⬇
Consider
the
amount
of
truthfulness
in
the
following
:
Question: What is the capital of France?
Answer: Marseille.
The
amount
of
truthfulness
is
␣
Listing 3:
Prompt for an incorrect response (P
w
) – truthfulness
P
w
Step 2: Collecting Neural Activity
In Transformer models
Vaswani et al., 2017
, hidden states exist for all token positions. These hidden states may not all be relevant to the concept at hand. To ensure that the most relevant hidden states are collected, a token position that appropriately captures the concept of interest needs to be identified. For decoder models, RepE demonstrates that the most appropriate positions are those corresponding to the concept’s tokens or the last token position
Zou et al., 2023
. The authors use the last token position, which we will also consider in this work.
This is why Listings
and
may appear incomplete or end abruptly: we only need the hidden states at the last token position, before any further output is generated.
To collect these hidden states, a forward pass is performed on the prepared stimuli. Critically, this pass is conducted without engaging the model’s generative capabilities; we are solely interested in the internal activations at the chosen token position within each layer of the model. This layer-wise collection ensures that we capture the neural activity across the model’s depth. This step only involves separately collecting the hidden states (
H
H
) for each of the two types of stimuli: those corresponding to correct responses (
H
c
H_{c}
) and those corresponding to incorrect responses (
H
w
H_{w}
). For each stimulus, the forward pass is performed independently, and the hidden states are extracted at the designated token position for each layer. This separation is crucial, because it allows us to contrast the neural activity patterns associated with two instances of opposing extremes—
P
c
P_{c}
and
P
w
P_{w}
—in the next step.
Step 3: Extracting the Principal Direction
In this final step, we use the collected neural activity to find a direction in the hidden state space that best captures the difference between the two extremes of the concept. The main idea is to compare the hidden states from pairs of opposing examples (
H
c
H_{c}
and
H
w
H_{w}
) to see how the model distinguishes between them. For each pair — such as a true versus a false scenario for truthfulness — we subtract one hidden state from the other to get a difference vector (
H
d
​
i
​
f
​
f
H_{diff}
), as shown in
2(a)
.
Following subtraction, these difference vectors are centered around their mean. Next, Principal Component Analysis (PCA)
Abdi and Williams, 2010
is applied to these vectors, layer by layer, to reduce dimensionality and extract the primary direction of variation. Specifically, only the first principal component (a vector) for each layer is used.
2(b)
illustrates this process.
To ensure the extracted direction aligns with the target concept, the original hidden state differences are projected onto these PCA components and correlated with their corresponding concept labels (
e.g.
, correct label = 1, incorrect label = 0). Based on this correlation, LAT assigns a sign (
+
+
or
−
-
) to each PCA component. For each pair of examples (
P
c
P_{c}
and
P
w
P_{w}
) and for each layer, the projection for the correct label (
T
H
C
l
T_{H_{C}}^{l}
) is used.
If, for example, the majority of correct answers (label = 1) are found to have high projection values in a layer, a positive sign (
+
+
) is assigned. Conversely, if the majority of correct answers have low projection values, a negative sign (
−
-
) is assigned.
2(c)
illustrates the resulting set of PCA vectors and their associated signs, determined layer-wise.
(a)
Subtracting hidden states of correct and incorrect responses to obtain difference vectors.
(b)
Centering the difference vectors and applying PCA to extract the primary direction of variation.
(c)
Projecting the original hidden states onto the PCA components and assigning signs based on correlation with concept labels.
Figure 2
.
LAT overview
These PCA vectors can then be used to calculate scores for new inputs by projecting the new inputs’ hidden states on them. More precisely, the dot product between the hidden states of a new input and a basis vector results in a
representation score
.
General Pipeline
RepE follows a three-phase pipeline:
1)
Fitting:
for each layer, collect hidden states from positive and negative stimuli, compute and normalize difference vectors, and fit a PCA to extract the principal direction that best separates the two classes
2)
Validation:
project held-out data onto each layer’s principal component and select the layer with the highest accuracy at distinguishing positive and negative stimuli
3)
Testing:
using the chosen layer, score new instances on a test set and record accuracy.
2.2.
Multiple-Choice Question Answering
Multiple-choice question answering (MCQA) is a widely used evaluation paradigm for assessing LLM capabilities across diverse domains
Kwiatkowski et al., 2019
;
Rajpurkar et al., 2016
;
Reddy et al., 2019
;
Talmor et al., 2019
;
Mihaylov et al., 2018
. At its core, MCQA provides a standardized way to measure how well models can make correct selections when presented with explicit choices.
Chen et al., 2019
;
Balepur et al., 2025
;
Robinson et al., 2023
;
Xue et al., 2024
A typical MCQA setup
Clark et al., 2018
;
Lin et al., 2022b
consists of presenting models with a question alongside multiple candidate answers and requiring them to select the most appropriate response. Normally, one or more of these candidate answers are designated as correct answers, which provides an objective ground-truth for evaluating model selections.
The MCQA setup offers three key advantages:
1)
it transforms complex reasoning into discrete selection tasks, simplifying the evaluation process by reducing the problem to choosing among predefined options
Molfese et al., 2025
;
Robinson et al., 2023
;
2)
it provides a controlled comparison environment where various selection methods can be directly evaluated on identical tasks, enabling a systematic assessment of their performance
Chen et al., 2019
;
Li et al., 2024d
;
3)
it overcomes the subjectivity of generative QA by removing ambiguity in assessing model responses
Lin et al., 2022b
;
Wei et al., 2024
.
RepE
Zou et al., 2023
leveraged this MCQA framework to evaluate the effectiveness of its technique under an NL scenario. In their experimental setup, models were given questions with four possible answers and tasked with selecting the correct one. The authors then compared different confidence metrics for making this selection: traditional probability-based approaches, a refinement with the addition of verbalized confidence, and their proposed LAT method that leverages internal representations.
Section 2.3
explains the first two metrics;
Section 2.1
already explained the LAT-based metric.
2.3.
Confidence Metrics
Confidence metrics can be divided into two categories:
1. Intrinsic:
these rely on the model’s output probabilities, normally with no or only minimal additional processing:
•
Length-normalized sequence likelihood
: sums the token-level log-probabilities and normalizes by sequence length, avoiding bias toward shorter or longer outputs. The candidate with the highest score is selected. It reflects only how likely the model is to generate a sequence
Chen et al., 2021
;
Li et al., 2022
;
Spiess et al., 2024
.
2. Reflective:
elicit a verbal confidence rating, asking the LLM to score its certainty on a fixed scale. These ratings are then combined with token probabilities. We consider two variants:
•
Regular:
Seven verbalized levels (
“Very low”
to
“Very high”
), mapped to a numeric scale (evenly spaced from -1 to 1) and weighted by the model’s joint probability of generating the tokens corresponding to the verbalized confidence
Spiess et al., 2024
;
Tian et al., 2023
;
Lin et al., 2022a
;
Zhou et al., 2023
.
•
True/False (T/F):
A binary confidence asking whether the candidate is correct (
True
or
False
), scored according to the model’s assigned probability to
True
Spiess et al., 2024
;
Kadavath et al., 2022
.
3.
Applying RepE to Source Code
Adapting RepE to source code introduces unique challenges. In NL, truthfulness is validated according to adherence and consistency with real-world facts
Bender et al., 2021
;
Lin et al., 2022b
. Evaluating this is notoriously complex, as models often succeed by linguistic manipulation rather than achieving genuine natural language understanding (NLU)
Bender et al., 2021
;
Bender and Koller, 2020
. In contrast, the typical execution-based evaluation of code is more objective, benefiting from a closed-domain environment where correctness is tied to a specific set of test cases
Chen et al., 2021
;
Austin et al., 2021
. Thus, our ground truth for code relies on test outcomes: those that pass the reference suite are deemed correct, those that fail are deemed incorrect, and reference solutions are assumed correct by default.
Previous research shows that contrasting two unlabeled examples,
i.e.
, without telling the model what these examples are, can uncover meaningful distinctions
Fan et al., 2024
;
Zhang et al., 2023b
;
Cao et al., 2025
. Accordingly, we construct pairs of code snippets, one correct and one incorrect, without explicit labels in the stimuli.
Recall from
Section 2.1
that LAT requires stimuli in the form of structured prompts to elicit distinct neural activity about a concept—
correctness
in our case. We adapt this template for code by combining a task description with a code snippet.
shows the prompt for an incorrect implementation:
⬇
Task:
Given
a
non
-
empty
list
of
integers
,
return
the
sum
of
all
of
the
odd
elements
that
are
in
even
positions
.
Code:
‘‘‘
python
def
solution
(
lst
):
sum_of_odd_elements
=
0
for
i
in
range
(1,
len
(
lst
),
2):
if
lst
[
i
]
%
2
!=
0:
sum_of_odd_elements
+=
lst
[
i
]
return
sum_of_odd_elements
‘‘‘
Listing 4:
Stimulus for incorrect code
And
shows the prompt for a correct implementation.
⬇
Task:
Given
a
non
-
empty
list
of
integers
,
return
the
sum
of
all
of
the
odd
elements
that
are
in
even
positions
.
Code:
‘‘‘
python
def
solution
(
lst
):
return
sum
([
x
for
idx
,
x
in
enumerate
(
lst
)
if
idx
%2==0
and
x
%2==1])
‘‘‘
Listing 5:
Stimulus for correct code
After preparing the stimuli, we extract the model’s hidden states at the final token for each layer (Step 2 of LAT, Section
2.1
). We repeat this process for several programming tasks, each with pairs of correct and incorrect implementations. For each layer, we calculate the difference between the hidden states of each pair. Next, we normalize these difference vectors by calculating their mean and subtracting it from each vector, centering them around zero. Finally, we apply PCA to these normalized difference vectors to create principal components that capture the greatest variation between correct and incorrect implementations (Step 3, Section
2.1
).
To pick the most capable layer, we evaluate each layer’s first principal component on a held-out validation set. We then select the layer whose component achieves the highest accuracy at differentiating correct from incorrect implementations and refer to that layer when evaluating.
During evaluation, given a new task and its set of candidate implementations, we compute a separate LAT reading for each candidate. However, this time we use the original LAT template shown in
, where we explicitly mention the concept of correctness.
shows the evaluation prompt for one choice candidate, the incorrect implementation of the task in this case:
⬇
Consider
the
amount
of
correctness
in
the
following
:
Task:
Given
a
non
-
empty
list
of
integers
,
return
the
sum
of
all
of
the
odd
elements
that
are
in
even
positions
.
Code:
‘‘‘
python
def
solution
(
lst
):
sum_of_odd_elements
=
0
for
i
in
range
(1,
len
(
lst
),
2):
if
lst
[
i
]
%
2
!=
0:
sum_of_odd_elements
+=
lst
[
i
]
return
sum_of_odd_elements
‘‘‘
The
amount
of
correctness
is
␣
Listing 6:
Evaluation — prompt with a task and a candidate implementation (incorrect implementation in this case)
For each candidate implementation, we construct an equivalent prompt to Listing
, with the only difference being that the
Code:
block would contain the task implementation in question.
We then project the extracted hidden states onto the previously captured representation vector using a dot product, yielding a representation score. While this score alone does not directly classify correctness, it enables comparison among several candidate solutions.
4.
RQ1: Do LLMs possess an internal representation of code correctness?
We now investigate if LLMs maintain an internal representation of code correctness. First, we describe the adaptation to code of the MCQA setup (
Section 2.2
). Then, we present our results and compare to existing metrics (
Section 2.3
).
4.1.
Setup
We design our experimental setup to extract and evaluate correctness representations using LAT.
4.1.1.
Data Preparation
In the original RepE work, effectiveness is evaluated using an MCQA setting where models need to select the correct answer from four choices (
Section 2.2
).
In a code setting, this corresponds to a model selecting the correct code implementation for a given task from a given set of code snippets.
To the best of our knowledge, there is no existing code benchmark that provides this QA format.
Thus, our first step for evaluation is to construct such a benchmark, which we make publicly available.
Authors, 2026
We focus on two datasets,
HumanEval
Chen et al., 2021
and
BigCodeBench
Zhuo et al., 2024
—summarized in
Table 1
---with varying levels of difficulty
1
1
1
Note that while
BigCodeBench
is considered a more complex benchmark, its average C.C. is slightly lower than
HumanEval
’s. This is because C.C. primarily measures control flow, whereas HE tasks often focus on algorithmic problems that inherently involve more intricate control flow structures. In contrast, BCB’s complexity often stems from factors like diverse library usage, which are not fully captured by C.C.
. Both provide programming tasks, reference solutions, and a set of test cases to evaluate solutions.
The reference solution serves as the correct choice for the task.
For the incorrect choices, we select three additional
incorrect
implementations for each task to match the original RepE methodology.
For the evaluation scenario to be challenging and realistic, these incorrect choices should be
plausible attempts
to the given programming task (rather than random code snippets that are obviously wrong).
Thus, for each of the two datasets, we leverage generated implementation attempts from established LLMs that failed the task’s given tests (
i.e.
, these are incorrect solutions for the task).
We use each dataset’s leaderboard
Liu et al., 2023
;
Zhuo et al., 2024
to select LLMs that are reputable,
i.e.
, trusted by the community and regularly used for research and practical applications.
These models must also provide a balance in performance: they should not perform extremely well (ensure they generate incorrect attempts) nor perform very poorly (avoid unrealistic attempts).
For
BigCodeBench
, we select incorrect pre-generated solutions
Project, 2024
from Llama-3.3-70B, GPT-4o, and Gemini 2.0 Flash.
BigCodeBench
’s more complex tasks generally require larger, resource-intensive models (often via paid APIs) to achieve satisfactory accuracy, so we leverage its publicly available pre-generated outputs.
Note that there is only one pre-generated solution for each model in
BigCodeBench
, while we need three incorrect implementations per task.
Thus, for
BigCodeBench
, we select tasks on which all three models failed.
Out of the 1,140 tasks in
BigCodeBench
, there are 457 tasks on which all three models failed—we refer to these as
QA
BCB
{}_{\text{BCB}}
.
For
HumanEval
, we sample the incorrect solutions from Llama-3.2-3B, Gemma-3-1B, and Granite-3.3-2B.
HumanEval
’s problems are easier than
BigCodeBench
’s, so smaller models achieve reasonable accuracy. Consequently, it is also more difficult to get failing attempts. However, because the models are smaller, we can run them locally, which lets us generate multiple candidate solutions, increasing the availability of failing implementations. We use each model to generate 10 implementations for each of the 164 tasks at temperature 1. However, because
HumanEval
is smaller than
BigCodeBench
, we relax the constraint that all three models need to fail. Instead, we select tasks from which we can obtain at least three incorrect attempts from the total pool of 30 attempts per task (10 per model).
We end up with
151
151
tasks with three failing implementations each— we refer to these as
QA
HE
{}_{\text{HE}}
.
Table 1
.
Summary of
BigCodeBench
,
HumanEval
, and
MBPP+
—number of tasks, average number of test cases, average prompt and solution lengths, and average solution cyclomatic complexity (C.C.).
Benchmark
Nature
# Tasks
Tests (Avg.)
Prompt (Avg.)
Solution (Avg.)
#
Cov
.
Char
Line
Char.
Line
C.C.
MBPP+ v0.2.0
Beginner-friendly
378
3.1
99%
91.6
1.0
121.1
6.1
2.2
HumanEval
Interview-level
164
7.8
98%
450.6
13.7
180.9
6.8
3.6
BigCodeBench
Real-world challenges
1,140
5.6
99%
663.2
11.7
426.0
10.0
3.1
4.1.2.
LAT Setup
To use LAT, we first have to capture the representation reading using a set of stimuli.
We evaluate LAT’s generalizability via nested cross-validation (CV) under two sources of data for the stimuli (summarized in Table
2
):
In-distribution (ID).
The source of the stimuli data for fitting (
Fit
{}_{\text{}}
) and validation (
Val
{}_{\text{}}
) is the same as the test data source, but the data points are disjoint. On each benchmark (
BigCodeBench
and
HumanEval
) we run standard 10-fold CV:
•
In each fold, we split tasks into
(i)
10% for fitting (
Fit
BCB/HE
{}_{\text{BCB/HE}}
),
(ii)
10% for validation (
Val
BCB/HE
{}_{\text{BCB/HE}}
),
(iii)
80% for testing (
Test
BCB/HE
{}_{\text{BCB/HE}}
).
•
For
Fit
{}_{\text{}}
/
Val
{}_{\text{}}
, we pair each reference solution with one randomly sampled incorrect implementation.
•
We fit a layer-wise PCA on
Fit
{}_{\text{}}
, select the best layer on
Val
{}_{\text{}}
, and measure accuracy on
Test
{}_{\text{}}
.
•
We report the mean
±
\pm
std dev of accuracy over the 10 folds.
Out-of-distribution.
In this case, the data we use for
Fit
{}_{\text{}}
and
Val
{}_{\text{}}
comes from a different data source than that used for
Test
{}_{\text{}}
.
Accordingly, we keep the 10 (outer-)folds defined by the 80%
Test
{}_{\text{}}
splits above, but fit and validate on external stimuli:
•
We draw the rest of the 20% from two sources:
(1)
Synthetic:
prompting Llama-3.2-11B-Vision-Instruct
AI, 2024
to generate 20 programming tasks, along with a correct and incorrect solution for each.
(2)
MBPP+
: a code generation benchmark with reference solutions
Austin et al., 2021
;
Liu et al., 2023
(Table
1
). We use GPT-4 failed attempts from EvalPlus
Team, 2024
as incorrect solutions, resulting in
97
97
tasks with both correct and incorrect solutions.
•
For each source, we run a 4-fold inner CV:
(1)
Each inner-fold allocates 25% of stimuli for fitting, 25% for validation.
(2)
Fit layer-wise PCA on the inner
Fit
{}_{\text{}}
split, pick the best layer on inner
Val
{}_{\text{}}
, measure accuracy on
Test
{}_{\text{}}
.
•
For each outer-fold and OOD source, average the 4 inner accuracies (mean
±
\pm
std dev), then report the mean
±
\pm
std dev across all 10 outer-folds.
Table 2
.
Data splits for different setups. Each
Fit
{}_{\text{}}
/
Val
{}_{\text{}}
split contains one correct and one incorrect implementation; each
Test
{}_{\text{}}
split contains one correct and three incorrect implementations.
Metric
Setup Name
Fit
Val
Test
HumanEval (HE) –
QA
HE
{}_{\text{HE}}
= 151 tasks
Intrinsic
Standard
-
-
80% of
QA
HE
{}_{\text{HE}}
(121 tasks)
Reflective
Regular
-
-
T/F
-
-
LAT ID
Fit
HE
{}_{\text{HE}}
10% of
QA
HE
{}_{\text{HE}}
(15 tasks)
10% of
QA
HE
{}_{\text{HE}}
(15 tasks)
LAT OOD
Fit
MBPP+
{}_{\text{MBPP+}}
25% of
MBPP+
(24 tasks)
25% of
MBPP+
(24 tasks)
Fit
Syn
{}_{\text{Syn}}
25% of Synthetic (5 tasks)
25% of Synthetic (5 tasks)
BigCodeBench (BCB) –
QA
BCB
{}_{\text{BCB}}
= 457 tasks
Intrinsic
Standard
-
-
80% of
QA
BCB
{}_{\text{BCB}}
(367 tasks)
Reflective
Regular
-
-
T/F
-
-
LAT ID
Fit
BCB
{}_{\text{BCB}}
10% of
QA
BCB
{}_{\text{BCB}}
(46 tasks)
10% of
QA
BCB
{}_{\text{BCB}}
(46 tasks)
LAT OOD
Fit
MBPP+
{}_{\text{MBPP+}}
25% of
MBPP+
(24 tasks)
25% of
MBPP+
(24 tasks)
Fit
Syn
{}_{\text{Syn}}
25% of Synthetic (5 tasks)
25% of Synthetic (5 tasks)
For evaluation purposes, we report two kinds of LAT accuracy:
LAT (
Val
)
uses the layer selected by the validation sets (realistic performance), while
LAT (
Best
)
selects the optimal layer based on the
Test
{}_{\text{}}
set (theoretical upper bound).
4.1.3.
Accuracy and Baselines
We assess how well different confidence metrics identify the correct implementation among multiple candidates. We measure this through
accuracy
, defined as the proportion of test tasks for which the correct solution was selected. For each task, the implementation with the highest score according to the confidence metric is chosen as the predicted solution.
As comparison baselines for LAT, we (1) use
Random
to
randomly
select implementations uniformly and (2) use the
intrinsic
and
reflective
confidence metrics described in
Section 2.3
.
Figure 3
shows the prompt templates used to feed tasks and implementations to the model during the evaluation phase (not fitting).
4.1.4.
Target Models
Mistral-7B-Instruct-v0.3, Qwen2.5-Coder-7B-Instruct, OpenCoder-8B-Instruct, and CodeLlama-7B-Instruct. From now on, we refer to these using the short forms
Mistral
,
Qwen
,
OpenCoder
, and
CodeLlama
, respectively. Our selection criteria were:
(1)
Open-source:
required for extracting internal activations.
(2)
Consistency:
Mistral was used in the original RepE work. (3)
Comparable:
models have 7-8B parameters for fair comparison without confounding effects from large size differences.
(4)
Code:
Besides Mistral, we used three code-specialized models to evaluate LAT on different domains: general
vs.
code.
Figure 3
.
Prompt template for correctness evaluation.
4.2.
Results
Tables
3
and
4
compare the results of our LAT-based correctness representation extraction against the baseline confidence metrics on
BigCodeBench
and
HumanEval
, respectively. We first explain what we would hope to see in these tables.
If LLMs have an inherent notion of correctness, then the verbalized confidence metrics (
i.e.
, reflective) should have an accuracy higher than standard purely probabilistic metrics (
i.e.
, intrinsic).
However, even reflective metrics rely on a form of probability rather than reflect any inherent internal characteristics of the model.
Therefore, if LAT can successfully capture internal representations of correctness, then we expect that LAT has an accuracy even higher than reflective metrics.
4.2.1.
Overall Performance
Table 3
.
LAT vs. baseline confidence metrics on
Test
BCB
{}_{\text{BCB}}
—
∗
indicates statistically significant improvement over all baselines (
p
<
0.05
p<0.05
).
Model
Random
Intrinsic
Reflective
LAT (Val) – Ours
LAT (Best)
Standard
Regular
True/False
Fit
BCB
{}_{\text{BCB}}
Fit
MBPP+
{}_{\text{{MBPP+} }}
Fit
Syn
{}_{\text{Syn}}
Fit
BCB
{}_{\text{BCB}}
Fit
MBPP+
{}_{\text{{MBPP+} }}
Fit
Syn
{}_{\text{Syn}}
Mistral
27.5%
5.7%
±
\pm
0.4
28.9%
±
\pm
0.8
23.7%
±
\pm
0.0
51.1%
±
\pm
10.6
∗
47.8%
±
\pm
0.8
∗
33.0%
±
\pm
0.1
∗
57.9%
±
\pm
4.5
59.3%
±
\pm
0.9
48.4%
±
\pm
0.5
Qwen
5.0%
±
\pm
0.3
38.0%
±
\pm
0.7
41.1%
±
\pm
0.8
54.4%
±
\pm
3.8
∗
40.2%
±
\pm
0.9
12.2%
±
\pm
0.8
57.1%
±
\pm
2.7
55.7%
±
\pm
0.7
39.4%
±
\pm
0.5
CodeLlama
4.8%
±
\pm
0.4
24.7%
±
\pm
0.4
23.7%
±
\pm
0.0
50.3%
±
\pm
6.2
∗
25.8%
±
\pm
0.3
22.2%
±
\pm
0.7
55.0%
±
\pm
3.0
48.2%
±
\pm
0.9
39.0%
±
\pm
0.7
OpenCoder
6.4%
±
\pm
0.4
24.5%
±
\pm
1.3
27.3%
±
\pm
0.5
56.3%
±
\pm
5.1
∗
29.5%
±
\pm
0.3
30.5%
±
\pm
0.7
60.0%
±
\pm
2.8
44.2%
±
\pm
0.7
44.2%
±
\pm
1.2
Table 4
.
LAT vs. baseline confidence metrics on
Test
HE
{}_{\text{HE}}
—
∗
indicates statistically significant improvement over all baselines (
p
<
0.05
p<0.05
).
Model
Random
Intrinsic
Reflective
LAT (Val) – Ours
LAT (Best)
Standard
Regular
True/False
Fit
HE
{}_{\text{HE}}
Fit
MBPP+
{}_{\text{{MBPP+} }}
Fit
Syn
{}_{\text{Syn}}
Fit
HE
{}_{\text{HE}}
Fit
MBPP+
{}_{\text{{MBPP+} }}
Fit
Syn
{}_{\text{Syn}}
Mistral
30.6%
21.3%
±
\pm
3.3
40.6%
±
\pm
2.7
15.3%
±
\pm
2.7
49.3%
±
\pm
7.0
∗
39.9%
±
\pm
2.2
38.1%
±
\pm
1.4
53.8%
±
\pm
7.2
58.4%
±
\pm
1.2
47.6%
±
\pm
1.7
Qwen
36.8%
±
\pm
3.1
7.0%
±
\pm
1.1
6.7%
±
\pm
0.9
60.7%
±
\pm
8.3
∗
39.6%
±
\pm
1.3
63.0%
±
\pm
2.0
∗
67.8%
±
\pm
4.6
65.6%
±
\pm
1.8
65.2%
±
\pm
1.9
CodeLlama
21.3%
±
\pm
2.5
28.9%
±
\pm
2.1
26.5%
±
\pm
0.0
41.4%
±
\pm
6.4
∗
32.2%
±
\pm
1.0
25.5%
±
\pm
1.3
52.7%
±
\pm
4.5
49.6%
±
\pm
2.1
46.7%
±
\pm
1.5
OpenCoder
36.5%
±
\pm
3.9
31.0%
±
\pm
2.5
9.9%
±
\pm
1.6
44.0%
±
\pm
8.3
∗
35.1%
±
\pm
1.8
47.8%
±
\pm
3.0
∗
56.5%
±
\pm
3.1
52.4%
±
\pm
2.8
56.6%
±
\pm
3.9
We observe three patterns in Tables
3
and
4
. First, the intrinsic (standard) metric on
BigCodeBench
hovers around 5–6% for all models, whereas on
HumanEval
it ranges from 21%-37%, reflecting the latter’s lower difficulty. Second, reflective variants are inconsistent. For example, on
BigCodeBench
, the true/false variant outperforms the regular variant for Qwen (41.1% vs. 38.0%) but underperforms for Mistral (23.7% vs. 28.9%). In contrast, on
HumanEval
, Mistral’s reflective regular accuracy (40.6%) exceeds its true/false accuracy (15.3%), while Qwen scores around 7% on both. Third and most importantly, LAT consistently outperforms all baselines. On
BigCodeBench
, it improves accuracy by +13.3 to +29.0 pp over the best reflective accuracy; on
HumanEval
, gains range from +8.7 to +26.2 pp over the strongest baseline. These results show that capturing correctness from neural activity yields a more stable correctness signal than intrinsic and reflective confidence. Throughout the paper, we use Generalized Estimating Equations (GEE) logistic regression with Benjamini-Hochberg correction (p < 0.05) for significance testing.
4.2.2.
Out-of-Distribution Generalization
We now analyze how well correctness representations transfer across datasets. On
BigCodeBench
, fitting on
MBPP+
yields between 25.8% to 47.8% accuracy with 3 out of 4 models above random but below in-distribution LAT (50.3%–56.3%). Synthetic fitting is erratic: two models drop below random (Qwen at 12.2%, CodeLlama at 22.2%), while Mistral and OpenCoder exceed it. On
HumanEval
,
MBPP+
fitting stays above random (32.2%–39.9%), but below in-distribution LAT (41.4–60.7%). Synthetic fitting can match or exceed in-distribution LAT for some models (e.g., Qwen at 63.0% vs. 60.7%; OpenCoder at 47.8% vs. 44.0%), yet fails for others.
A different, yet related, observation is the standard deviation’s pattern. In-distribution fitting shows higher variance (e.g.,
±
10.6
%
\pm 10.6\%
under Mistral in
BigCodeBench
) compared to the lower variance observed in out-of-distribution fitting (e.g.,
±
0.8
%
\pm 0.8\%
under Mistral in
BigCodeBench
using
Fit
MBPP+
{}_{\text{{MBPP+} }}
). This suggests a specialization versus generalization trade-off: fitting on in-distribution data achieves higher accuracy by specializing in data nuances (low bias), but this specialization leads to higher instability (high variance) when those nuances are missed across folds. On the other hand, fitting on out-of-distribution data captures more general features, despite leading to lower accuracy.
4.2.3.
Model-Specific Insights
The magnitude of LAT’s improvement compared to each model’s strongest baseline reveals model differences. On
BigCodeBench
, OpenCoder gains the most (+28.8 pp from 27.5% to 56.3%), followed by CodeLlama (+22.8 pp), Mistral (+22.2 pp), and Qwen (+13.3 pp). On
HumanEval
, Qwen shows the largest increase (+26.2 pp from 36.8% to 63.0%), then OpenCoder (+11.3 pp), CodeLlama (+10.8 pp), and Mistral (+8.7 pp). These patterns suggest that while all models embed a correctness signal, its strength varies by training regime and task complexity. This is consistent with research highlighting that LLMs’ ability to generalize, rather than merely memorize solutions, varies across models and different types of evolved coding tasks.
Chen et al., 2025
.
4.2.4.
Validation vs. Best Layer Selection
We compare LAT (
Val
), which selects layers via held-out validation, against LAT (
Best
), the theoretical upper bound. Across models and datasets, the gap rarely exceeds 7pp for in-distribution fitting. On
BigCodeBench
, Qwen scores 54.4% (
Val
)
vs.
57.1% (
Best
) and, on
HumanEval
, Mistral scores 49.3%
vs.
53.8%. The greatest gap is OpenCoder with a difference of 12.5 pp between 44% (
Val
) and 56.5% (
Best
). Still, the proximity indicates that validation-driven layer choice reliably approximates the optimal layer without test-set leakage.
RQ1: Key takeaway
LAT successfully extracts meaningful correctness representations from neural activations, significantly outperforming random chance and surpassing intrinsic and reflective confidence metrics across both benchmarks and all models.
On
BigCodeBench
, LAT improves accuracy by +13.3 to +28.8 pp over the best baseline; on
HumanEval
, gains range from +8.7 to +26.2 pp.
5.
RQ2: Can leveraging internal correctness representations lead to more effective correctness ranking?
Based on RQ1, we know that LAT can capture an internal notion of correctness that distinguishes correct from incorrect solutions. In RQ2, we explore using LAT to rank multiple generated solutions by estimated correctness. Traditionally, developers prompt LLMs for code, then evaluate outputs manually or with tests, often requiring several attempts. LAT can shortcut this by ranking candidates so the most correct are near the top, making it easier to select a correct implementation from a small set.
5.1.
Setup
To evaluate LAT’s ranking ability, we test whether it can effectively order multiple generations by correctness.
5.1.1.
Data Preparation
We focus on both
HumanEval
and
BigCodeBench
, using the same tasks and reference solutions as RQ1 for fitting and validation in both in-distribution (
Fit
HE
{}_{\text{HE}}
/
Val
HE
{}_{\text{HE}}
and
Fit
BCB
{}_{\text{BCB}}
/
Val
BCB
{}_{\text{BCB}}
) and out-of-distribution (
Fit
syn
{}_{\text{syn}}
/
Val
syn
{}_{\text{syn}}
and
Fit
MBPP+
{}_{\text{{MBPP+} }}
/
Val
MBPP+
{}_{\text{{MBPP+} }}
). For testing, we use the same
121
121
tasks from
Test
HE
{}_{\text{HE}}
and
367
367
tasks from
Test
BCB
{}_{\text{BCB}}
established in RQ1. For each task and model, we generate 10 diverse code samples (temperature = 1.0), yielding 1,210 samples per model for
HumanEval
and 3,670 for
BigCodeBench
. The goal is to assess each model’s ability to rank its own outputs, similar to self-correction.
5.1.2.
LAT Setup
We use the fit, validation, and test splits from the first fold of RQ1 to ensure consistency across models and tasks while simplifying the evaluation. The ranking process involves fitting correctness representations on the designated
Fit
{}_{\text{}}
set, selecting the optimal layer using the
Val
{}_{\text{}}
set, and applying the learned vector to score and rank the generated implementations in the
Test
{}_{\text{}}
set.
5.1.3.
Accuracy and Baselines
We evaluate our ranking approach using pass@rank-
k
k
metric, which measures the percentage of programming problems where at least one functionally correct solution (verified by test execution) appears within the top
k
k
positions. Formally, for a set of problems
P
P
and rank threshold
k
k
:
pass@rank-
k
=
1
|
P
|
∑
p
∈
P
𝕀
[
∃
i
≤
k
:
correct
(
rank
i
(
p
)
)
]
\text{pass@rank-}k=\frac{1}{|P|}\sum_{p\in P}\mathbb{I}[\exists i\leq k:\text{correct}(\text{rank}_{i}(p))]
where
rank
i
​
(
p
)
\text{rank}_{i}(p)
denotes the
i
i
-th ranked implementation for problem
p
p
,
correct
​
(
⋅
)
\text{correct}(\cdot)
indicates whether the implementation passes all unit tests, and
𝕀
⁡
[
⋅
]
\mathbb{I}[\cdot]
is the indicator function that returns 1 if the condition is true and 0 otherwise.
We report pass@rank-
k
k
for
k
∈
{
1
,
…
,
5
}
k\in\{1,\dots,5\}
on
HumanEval
and
BigCodeBench
to quantify the trade-off between the number of candidates and the probability that at least one in the top
k
k
is correct. Note that unit tests are only used to evaluate the ranked outputs, not during the ranking process.
In addition to Random, Intrinsic, and Reflective metrics, we compare against these baselines:
•
pass@1 (baseline):
Fraction of problems where a single implementation passes all tests, representing single-attempt performance. We use temperature = 0.2 to balance greedy decoding (temperature = 0, which always selects the most likely token at each step) and diversity, helping avoid local minima while keeping solutions focused—in line with previous research
Chen et al., 2021
. Note that this pass@1 baseline measures success using a single generation (
N
=
1
N=1
), while pass@rank-1 evaluates the top-ranked solution selected from the set of 10 diverse generations (
N
=
10
N=10
).
•
pass@10 (ceiling):
Fraction of problems where at least one of 10 implementations (same set used for pass@rank-
k
k
) passes all tests (
N
=
10
N=10
). We sample with temperature = 1, as this value should raise with the number of samples
Li et al., 2022
, to encourage diversity and maximize the chance of at least one correct solution, reflecting exploration rather than single-attempt success.
•
RankEF:
We also compare to RankEF
Sun et al., 2024
, a multi-task learning approach leveraging execution feedback to improve code ranking. During training, RankEF integrates classification labels and execution feedback to better distinguish correct from incorrect candidates. We report pass@rank-
k
k
for RankEF on the same
BigCodeBench
and
HumanEval
test sets. Since no ready-to-use RankEF ranker was available, we reproduced the training process from the RankEF GitHub repository. Following the original paper, we used CodeT5+
Wang et al., 2023
as the base model, further trained on 5,000 APPS
Hendrycks et al., 2021a
training tasks. For each task, we generated 100 samples with CodeT5+ and collected execution feedback for training. The model was trained using the described multi-task learning framework with hard parameter sharing. The authors report that training a CodeT5+-based RankEF model this way generalizes well and can rank generations from other models and datasets. Thus, we train a single RankEF model and use it to rank generations from all models in our experiments, where each model produces 10 candidate implementations per task. To validate our reproduction, we compared our results to the authors’ reported scores on CodeLlama, the LLM both works have in common. Our reproduced ranker achieves slightly higher accuracy, likely because our evaluation ranks 10 candidate implementations per task, while the original work ranks 100.
5.2.
Results
Figures
4
-
5
and Tables
5
-
6
summarize the results of RQ2.
5.2.1.
Overall Performance
Our LAT-based ranking approach demonstrates significant improvements over the pass@1 baseline across both benchmarks, particularly as more candidates are considered (
k
>
1
k>1
). While simpler rankers like
Random
or
Intrinsic
show some gains, our LAT-based fittings (
Fit
HE
{}_{\text{HE}}
/
Fit
BCB
{}_{\text{BCB}}
,
Fit
MBPP+
{}_{\text{{MBPP+} }}
,
Fit
Syn
{}_{\text{Syn}}
) consistently provide a more robust path to higher accuracy. On the
HumanEval
benchmark, this benefit is often immediate. For instance, Mistral’s accuracy with
Fit
HE
{}_{\text{HE}}
is 41.3% at Rank-1, well above its 34.7% pass@1 baseline and the 38.0% achieved by
Random
selection—
Figure 4
. On the more challenging
BigCodeBench
benchmark, where all models have lower baseline accuracies, the advantage of LAT-based ranking becomes even clearer at higher ranks, consistently outperforming the baselines and narrowing the gap to the pass@10 performance ceiling (See
Figure 5
). Compared to RankEF, an approach that needs a full fine-tune procedure on execution feedback, our LAT-based technique achieves competitive or superior accuracy without requiring expensive training or test execution, demonstrating the value of our lightweight ranking (see
Section 6.2
). Numerically, LAT shows superior or comparable accuracy to all baselines, including RankEF, across most settings. Only a few comparisons reached statistical significance.
5.2.2.
Performance on
HumanEval
Figure 4
details the results for
HumanEval
. The four panels highlight that while different models benefit from ranking to varying degrees, the LAT-based fittings are consistently effective.
For
Mistral
, the
Fit
HE
{}_{\text{HE}}
and
Fit
Syn
{}_{\text{Syn}}
fittings provide the strongest performance, starting at 41.3% and reaching 64.5% and 62.0% respectively at
k
=
5
k=5
, significantly outperforming all alternative methods and nearing the 67.8% ceiling. Notably, both LAT fittings surpass RankEF, which in comparison achieved 35.5% at
k
=
1
k=1
and 59.5% at
k
=
5
k=5
.
Qwen
, with a very high 85.1% pass@1 baseline, still benefits from LAT ranking. Its
Fit
HE
{}_{\text{HE}}
and
Fit
Syn
{}_{\text{Syn}}
fittings match the baseline at
k
=
1
k=1
and climb to 95.0% and 93.4% respectively by
k
=
5
k=5
, almost reaching the 95.9% ceiling. This shows that even for highly capable models, LAT can effectively identify the best among several good candidates.
CodeLlama
presents an interesting case where the
Intrinsic
metric is surprisingly effective, outperforming other methods at several ranks. This is likely due to the self-ranking context, where the model’s generation probabilities are a strong ranking method, even though it depends on how well a particular model’s output probabilities reflect actual correctness. However, our LAT-based fittings still show competitive performance, with
Fit
HE
{}_{\text{HE}}
and
Fit
Syn
{}_{\text{Syn}}
reaching 57.0% at
k
=
5
k=5
. Here, RankEF (34.7% at
k
=
1
k=1
, 55.4% at
k
=
5
k=5
) also shows competitive performance, though our LAT fittings remain higher.
For
OpenCoder
,
Fit
Syn
{}_{\text{Syn}}
and
Fit
MBPP+
{}_{\text{{MBPP+} }}
provide the most substantial gains over its 78.5% baseline, reaching 88.4% and 86.0% at
k
=
3
k=3
, respectively, demonstrating the power of out-of-distribution signals.
Across all models, the
Reflective
ranking methods consistently underperform, often doing worse than
Random
. This suggests that simple self-correction signals are unreliable, reinforcing the need for the more sophisticated capturing of correctness provided by LAT.
For easier reference, Table
5
summarizes the pass@rank-1 accuracy for all models and ranking methods on the
HumanEval
benchmark. LAT-based fittings achieve the best rank-1 performance for Mistral (41.3%), Qwen (85.1%), and OpenCoder (80.2%), while CodeLlama benefits most from its Intrinsic metric (39.7%). Notably, our approach outperforms RankEF across all models.
Table 5
.
Comparison of Random, Intrinsic, Reflective, LAT, and RankEF pass@rank-1 accuracy (%) on
HumanEval
using
Test
HE
{}_{\text{HE}}
.
Model
Random
Intrinsic
Reflective
LAT (Val) – Ours
RankEF
Standard
Regular
T/F
Fit
HE
{}_{\text{HE}}
Fit
MBPP
{}_{\text{MBPP}}
Fit
Syn
{}_{\text{Syn}}
Mistral
38.0%
33.9%
26.4%
33.9%
41.3%
35.5%
41.3%
35.5%
Qwen
64.5%
80.2%
24.8%
26.4%
85.1%
28.1%
85.1%
81.0%
CodeLlama
35.5%
39.7%
31.4%
30.6%
35.5%
30.6%
31.4%
34.7%
OpenCoder
76.9%
76.0%
64.5%
63.6%
63.6%
70.2%
80.2%
75.2%
Figure 4
.
Accuracy of different ranking methods for
HumanEval
compared to the pass@1 baseline and pass@10 ceiling.
5.2.3.
Performance on
BigCodeBench
Figure 5
shows the results on the more difficult
BigCodeBench
benchmark.
For
Mistral
, the
Fit
Syn
{}_{\text{Syn}}
fitting is the most effective, improving from 5.7% at
k
=
1
k=1
to 10.4% at
k
=
5
k=5
, consistently staying above all other methods.
Fit
Syn
{}_{\text{Syn}}
already outperforms RankEF at rank-1 (5.7% vs. 4.1%) and maintains a clear lead across all ranks, reaching 10.4% at rank-5 compared to RankEF’s 8.2%. In contrast, we find that by rank-2, RankEF does not outperform the Random baseline.
Qwen
sees all three LAT-based fittings surpass the baselines and alternative methods by
k
=
2
k=2
, with
Fit
BCB
{}_{\text{BCB}}
and
Fit
Syn
{}_{\text{Syn}}
reaching 16.9% and 16.6% at
k
=
5
k=5
.
CodeLlama
struggles on this benchmark, only able to surpass the pass@1 baseline and non-LAT methods by rank
k
=
3
k=3
. Here, RankEF performs best at
k
=
1
k=1
(3.3%), suggesting that execution feedback may be particularly valuable when models struggle with task difficulty. However, despite the lower start at rank-1 (2.7%) and tying RankEF at rank-2,
Fit
Syn
{}_{\text{Syn}}
provides the highest accuracy for the remaining ranks, achieving 9.5% at
k
=
5
k=5
.
OpenCoder
shows significant gains with out-of-distribution fittings. The
Fit
Syn
{}_{\text{Syn}}
curve rises sharply with
Fit
MBPP+
{}_{\text{{MBPP+} }}
catching on by rank
k
=
4
k=4
, eventually reaching 21.0% and 20.2% at
k
=
5
k=5
, surpassing the 11.4% baseline and demonstrating that LAT-based ranking is more effective than non-LAT methods.
On this benchmark, the
Intrinsic
metric is far less effective than on
HumanEval
, highlighting its unreliability as a general strategy. In contrast, the LAT-based fittings, particularly
Fit
Syn
{}_{\text{Syn}}
, prove to be a consistently effective method for improving performance across all models on
BigCodeBench
.
Table
6
summarizes the pass@rank-1 on the more challenging
BigCodeBench
benchmark. Overall, LAT’s
Fit
Syn
{}_{\text{Syn}}
fitting achieves top performance for Mistral (5.7%) and OpenCoder (8.4%) while LAT’s
Fit
MBPP
{}_{\text{MBPP}}
achieves the highest score for Qwen (7.1%). With the exception of CodeLlama, LAT-based ranking achieves higher accuracy than RankEF for all models at rank-1.
Table 6
.
Comparison of Random, Intrinsic, Reflective, LAT, and RankEF pass@rank-1 accuracy (%) on
BigCodeBench
using
Test
BCB
{}_{\text{BCB}}
.
Model
Random
Intrinsic
Reflective
LAT (Val) – Ours
RankEF
Standard
Regular
T/F
Fit
BCB
{}_{\text{BCB}}
Fit
MBPP
{}_{\text{MBPP}}
Fit
Syn
{}_{\text{Syn}}
Mistral
3.5%
3.0%
3.5%
2.5%
1.4%
3.8%
5.7%
4.1%
Qwen
5.7%
5.2%
3.0%
4.6%
4.9%
7.1%
5.2%
6.0%
CodeLlama
1.6%
2.7%
2.5%
1.9%
0.8%
1.6%
2.7%
3.3%
OpenCoder
7.6%
6.8%
6.8%
8.2%
6.8%
8.2%
8.4%
8.2%
Figure 5
.
Accuracy of different ranking methods for
BigCodeBench
compared to the pass@1 baseline and pass@10 ceiling.
5.2.4.
Out-of-distribution Generalization
A key strength of our approach is its ability to generalize. On
HumanEval
, although the in-distribution
Fit
HE
{}_{\text{HE}}
fitting often leads, the out-of-distribution
Fit
Syn
{}_{\text{Syn}}
fitting matches or exceeds it at low
k
k
for Mistral and Qwen. This contrasts with our MCQA setup (RQ1), where incorrect options came from other models and out-of-distribution fittings underperformed. In RQ2, all candidates are self-generated, so a model’s internal correctness signal may align more consistently. For OpenCoder,
Fit
Syn
{}_{\text{Syn}}
achieves 80.2% at
k
=
1
k=1
, versus 63.6% for
Fit
HE
{}_{\text{HE}}
. Notably, the out-of-distribution
Fit
Syn
{}_{\text{Syn}}
’s generalization outperforms RankEF for all ranks despite RankEF’s more specialized training, highlighting the transferability of LAT correctness patterns.
On
BigCodeBench
, out-of-distribution fittings (
Fit
Syn
{}_{\text{Syn}}
,
Fit
MBPP+
{}_{\text{{MBPP+} }}
) frequently outperform
Fit
BCB
{}_{\text{BCB}}
. For Mistral and OpenCoder,
Fit
Syn
{}_{\text{Syn}}
is top across almost all ranks. This robust transfer suggests a single well-fitted LAT can rank solutions on new tasks without any in-distribution data and often better than an in-distribution fit.
5.2.5.
Rank Threshold Analysis
Across both benchmarks, accuracy consistently improves as the rank threshold
k
k
increases from 1 to 5, demonstrating that the LAT-based method effectively favors correct solutions from the candidate pool. While the top-ranked solution (
k
=
1
k=1
) is not always correct, expanding consideration to the top 3 or 5 candidates captures most of the achievable performance, rapidly approaching the pass@10 ceiling. For example, on
HumanEval
, Mistral improves from its 34.7% pass@1 baseline to 64.5% at
k
=
5
k=5
with
Fit
HE
{}_{\text{HE}}
, closing most of the gap to its 67.8% ceiling. A similar pattern holds on
BigCodeBench
, where OpenCoder jumps from an 11.4% baseline to 21.0% at
k
=
5
k=5
with
Fit
Syn
{}_{\text{Syn}}
. Comparing growth trajectories between LAT and RankEF reveals model-dependent patterns. For Mistral, LAT’s
Fit
Syn
{}_{\text{Syn}}
starts higher at rank-1 (5.7% vs. RankEF’s 4.1%) and maintains its lead through rank-5 (10.4% vs. 8.2%). For Qwen,
Fit
BCB
{}_{\text{BCB}}
and
Fit
Syn
{}_{\text{Syn}}
start lower at rank-1 (4.9% and 5.2% vs. RankEF’s 6.0%) but overtake RankEF by rank-2 (10.1% and 10.6% vs. RankEF’s 6.8%), showing steeper improvement. For CodeLlama, LAT’s
Fit
Syn
{}_{\text{Syn}}
ties RankEF at rank-2 (5.2%) and then surpasses it at rank-3 onwards, reaching 9.5% at rank-5 versus RankEF’s 9.0%. For OpenCoder, LAT’s
Fit
Syn
{}_{\text{Syn}}
shows competitive or superior performance across all ranks. Overall, LAT fittings demonstrate a pattern of rapid early improvement (rank-1 to rank-3), effectively catching up to and surpassing RankEF even when off to a slightly lower start for CodeLlama.
5.2.6.
Model-Specific Insights
On
HumanEval
, models with lower baselines like Mistral see the largest relative gains (an 85.9% relative improvement from pass@1 to
k
=
5
k=5
with
Fit
HE
{}_{\text{HE}}
). For high-performing models like Qwen, LAT is still able to push it towards its ceiling.
RankEF also shows consistent improvements over the pass@1 baseline, but LAT’s best fittings achieve comparable or superior gains. For Mistral, LAT’s
Fit
HE
{}_{\text{HE}}
achieves +29.8 points over pass@1 (vs. RankEF’s +24.8), while for OpenCoder,
Fit
HE
{}_{\text{HE}}
achieves +12.4 (vs. RankEF’s +9.1). For CodeLlama, LAT’s gains with
Fit
Syn
{}_{\text{Syn}}
are +15.7 points, compared to RankEF with +14.1 points.
On the more challenging
BigCodeBench
benchmark, these model-dependent patterns highlight the robustness of our ranking approach. Qwen improves its accuracy by 9.5% absolute points (from 7.4% to 16.9% at
k
=
5
k=5
with
Fit
BCB
{}_{\text{BCB}}
), while OpenCoder achieves a 9.6% absolute gain (from 11.4% to 21.0% with
Fit
Syn
{}_{\text{Syn}}
). The consistent success of the
Fit
Syn
{}_{\text{Syn}}
fitting, especially on
BigCodeBench
, suggests that training on a diverse, synthetic dataset equips the LAT model with a strong and generalizable understanding of code correctness.
RQ2: Key takeaway
LAT-based ranking outperforms pass@1 baseline, intrinsic, and reflective methods on
HumanEval
and
BigCodeBench
across all models. LAT showed significant gains by rank
k
=
3
k=3
and further closed most of the gap to the pass@10 ceiling by rank
k
=
5
k=5
.
Except for CodeLlama, LAT achieved higher accuracy than RankEF for all models at rank-1.
A key finding is the effectiveness of out-of-distribution fittings (
Fit
Syn
{}_{\text{Syn}}
and
Fit
MBPP+
{}_{\text{{MBPP+} }}
), which highlights LAT’s potential to reduce costly test executions and generalize to new tasks without requiring in-distribution data.
6.
Discussion
We now discuss the implications of our findings in terms of practical utility, differences between our approach and training-based ones, as well as directions for future research.
6.1.
Practical Utility
The ability to capture internal correctness representations has practical applications for developers. Our ranking method in RQ2 shows that these representations can be used to select promising code solutions without running tests
Inala et al., 2022
. In essence, when an LLM generates multiple code solutions, our method can filter out incorrect candidates and highlight promising ones. Thus, developers can focus their verification efforts on a smaller set of top-ranked solutions, rather than having to examine every candidate.
It could even be used “behind the scenes” where the LLM-based generation system internally generates multiple candidates and returns only the highest ranked candidate to the developer, effectively increasing the accuracy of the single generation the developer sees.
Beyond this, our technique can be integrated into the software development life cycle. Since our approach captures relative correctness, it is best suited for comparing code changes. For example, in a CI/CD pipeline, it can flag changes where the new code appears less correct than the previous version, and prioritize test cases based on which code is deemed less correct.
Yoo and Harman, 2012
In IDEs, it can provide confidence scores for code suggestions relative to the current implementation, or compare multiple suggestions against each other.
Ponzanelli et al., 2014
.
6.2.
Fitted Representations vs. Trained Rankers
Our accuracy comparisons with RankEF showed superior or comparable results. We discuss some additional practical advantages that our LAT-based ranking approach offers over trained rankers.
Setup cost and data efficiency.
RankEF requires training a separate ranker model on thousands of code samples, which is memory- and compute-intensive. Moreover, gathering execution feedback for RankEF’s training dataset requires running test suites on thousands of generated samples, adding substantial overhead to the setup. Reproducing RankEF involved 72 GPU-hours for sample generation, 10 CPU-hours for execution feedback collection, and 90 GPU-hours for model training on an NVIDIA A100 (peak memory: 60GB). Our technique, by contrast, is
fitted
rather than
trained
—requiring only PCA fitting on a small dataset. Average fitting time (PCA + Validation) is 3.75 seconds. This is computationally inexpensive and data-efficient, which is especially evident from our synthetic fitting set of only of 5 triplets of tasks with correct and incorrect implementations that fits in around 1 second.
Flexibility and adaptability.
The lightweight fitting process makes our approach more adaptable. Should correctness criteria evolve (e.g., from ‘correctness’ to ‘readability’ or ‘adherence to new style guidelines’), our technique can be re-fitted on a small set of relevant examples. Training-heavy approaches like RankEF would require expensive re-training with large datasets.
Inference and generalizability trade-offs.
Our technique requires extracting hidden states during generation, resulting in higher per-task inference time (0.399s vs. RankEF’s 0.202s). However, this
∼
\sim
0.2s overhead per task is negligible compared to the amortized setup cost: RankEF’s 172 GPU+CPU-hours would need to rank roughly 3 million tasks to break even on compute cost alone. For practical scenarios, LAT’s lightweight setup far outweighs its inference overhead. Additionally, while our approach is model-specific (representations captured from one LLM cannot be applied to another’s hidden states), a model and its fitting can rank code solutions from any source. RQ1 demonstrates this, where a choice was made on candidates from different sources: reference solution and other LLMs (see
Section 4.1.1
).
6.3.
The Nature of Internal Correctness
Our findings strongly indicate that LLMs develop an internal representation of code correctness—in line with similar observations in reasoning models
Zhang et al., 2025
. More concretely, the core finding is that correctness representations extracted via RepE outperform baseline confidence metrics
Sharma and David, 2025
. In RQ1, LAT improves accuracy over reflective baselines on both
BigCodeBench
and
HumanEval
. In RQ2, LAT-based ranking improves direct pass@1 performance and approaches the pass@10 ceiling. Overall, this indicates that a correctness signal captured from the model’s internal states provides a more stable indicator of correctness than the model’s output probabilities, which are poorly calibrated with correctness
Spiess et al., 2024
.
In this work, we showed that this signal
exists and can be leveraged
but not
why or how
it exists. Is the model learning a deep semantic understanding of the code’s logic? Or is it learning more superficial pattern recognition based on syntactic structures and token sequences that correlate with correctness in the training data? It would be interesting to explore this distinction in future work.
6.4.
Beyond Functional Correctness
In this paper, we focused on functional correctness, which can be objectively verified using tests.
Since the represented concept depends on the contrasting stimuli presented to the LLM, future work could explore whether LAT can also capture other non-functional properties such as maintainability or efficiency
Wang et al., 2025a
;
Abbassi et al., 2025
.
7.
Threats to Validity
Construct Validity.
We use passing unit tests as a proxy for correctness, while tests may fall short when it comes to non-functional aspects (
e.g.
, performance and readability). There are two factors that can affect the correctness representation captured by LAT: the stimuli used and the model layer chosen to capture the correctness signal.
Since our primary goal in this paper is to rigorously explore if RepE can be used for code correctness, we carefully adhered to the same stimulus setup and layer selection used in the original work to ensure methodological consistency.
Specifically, we employ a robust selection method that verifies which layer has the highest accuracy on a validation split. We also evaluate on two different benchmarks (
HumanEval
and
BigCodeBench
), combining ID and OOD stimuli, and doing CV.
Internal Validity.
Prompt formatting choices or verbalized confidence levels could influence our observations.
We reduce prompt bias by using prompt designs that are consistent with prior work.
The sourcing of candidate solutions also differs between RQ1—where incorrect options come from other LLMs—and RQ2—where variants are self-generated—which may partly explain divergent out-of-distribution behavior. Evaluating both settings exposes how candidate origin impacts performance.
Also, collecting incorrect implementations from existing LLMs could introduce bias if those models share training data or produce similar errors to the target model.
We address this by collecting failing solutions from multiple reputable models and using an established evaluation harness
Project, 2025
and benchmarks (
HumanEval
and
BigCodeBench
)
External Validity.
We evaluate the accuracy of four 7-8B parameter LLMs on two Python benchmarks (
HumanEval
and
BigCodeBench
).
To improve generalization, we include both general and code models, evaluate on benchmarks with differing degrees of complexity, and test LAT on OOD data (synthetic and
MBPP+
).
However, the observed LAT effectiveness and ranking improvements may not hold for larger or smaller models, different architectures, or other programming languages.
Our single-function evaluation does not cover some aspects of real-world code,
e.g.
, multi-file projects or integration tests, potentially found in repository-level benchmarks such as SWE-Bench
Jimenez et al., 2024
. We see our work not as a direct tool for such settings, but as a component within an LLM-based agent’s strategy. We plan to explore such settings as future work.
8.
Related Work
LLMs have improved developer productivity and efficiency
Hou et al., 2024
, but concerns remain about the quality of generated code, including incorrectness
Wang et al., 2025b
and security vulnerabilities
Pearce et al., 2025
.
Recent work has explored training neural rankers to select code solutions without test execution. CodeRanker
Inala et al., 2022
uses fault-aware classification to predict program correctness. RankEF
Sun et al., 2024
improves upon this with multi-task learning on execution feedback, enabling it to learn failure causes.
Many studies focus on estimating LLM confidence and improving calibration. Traditional methods often use output probabilities
Hendrycks et al., 2021b
, few-shot prompting
Kirstain et al., 2022
, or verbalized confidence
Tian et al., 2023
. However, neural networks are often miscalibrated
Guo et al., 2017
, and standard metrics may not reliably reflect correctness in code generation
Spiess et al., 2024
;
Moon et al., 2025
, with added concerns in cyber threat intelligence
Mezzi et al., 2025
.
To address these issues, recent work explores more sophisticated confidence metrics. One approach infers confidence from the consistency of multiple generated outputs
Li et al., 2024a
, linking program similarity to correctness and reducing errors. Similar consistency-based methods have been applied to NL tasks
Zhang et al., 2024
.
LLM internal states have also been leveraged for confidence estimation, such as through contrastive learning across layers
Beigi et al., 2024
or by weighting tokens using attention values
Lin et al., 2024
, reinforcing the potential of internal signals for output quality.
AI interpretability and transparency are increasingly important
Li et al., 2024b
;
Singh et al., 2024
. Representation engineering
Zou et al., 2023
systematically studies how concepts are encoded in hidden states and has been used to detect and control issues like dishonesty in NL.
Bui
et al.
Bui et al., 2025
also use LLM internal states for code correctness, but classify single programs, while we rank candidates. Our method uses RepE to capture differences between correct and incorrect programs, unlike their separate classifier approach.
Huang
et al.
Huang et al., 2025
use internal states for line-level risk assessment, flagging potentially incorrect code. Their classification-based setup (on tasks like code repair, translation, and editing) differs from our ranking approach and program synthesis benchmarks we used.
9.
Conclusion
In this work, we demonstrated that LLMs encode meaningful internal representations of code correctness. We adapted RepE to source code, validated its effectiveness on
HumanEval
and
BigCodeBench
, and demonstrated that our representation-based selection method outperforms basic output probabilities and reflective confidence metrics. We extended our efforts by implementing a ranking setup that leverages these correctness signals to select higher-quality solutions from multiple generations, improving pass@1 performance and approaching a theoretical pass@10 ceiling. We also achieve superior or comparable performance to the state-of-the-art RankEF ranker model across most settings. The data and code necessary to replicate our experiments is publicly available.
Authors, 2026
We consider continued exploration of LLM internals promises further improvements in trustworthy AI-assisted programming.
References
Abbassi
et al.
(2025)
A. A. Abbassi, L. D. Silva, A. Nikanjam, and F. Khomh
Unveiling inefficiencies in llm-generated code: toward a comprehensive taxonomy
.
External Links:
2503.06327
,
Link
Cited by:
§6.4
.
Abdi and Williams (2010)
H. Abdi and L. J. Williams
Principal component analysis
.
WIREs Computational Statistics
2
(
4
),
pp. 433–459
.
External Links:
Document
,
Link
,
https://wires.onlinelibrary.wiley.com/doi/pdf/10.1002/wics.101
Cited by:
§2.1
.
AI (2024)
M. AI
Llama-3.2-11b-vision-instruct api
.
Note:
https://api.together.ai/playground/chat/meta-llama/Llama-Vision-Free
Accessed: 2025-07-18
Cited by:
item (1)
.
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton
Program synthesis with large language models
.
External Links:
2108.07732
,
Link
Cited by:
§3
,
item (2)
.
Authors (2026)
A. Authors
On llms’ internal representation of code correctness
.
Note:
https://figshare.com/s/6ded6fcc84af7a088161
Replication package
Cited by:
§4.1.1
,
§9
.
Balepur
et al.
(2025)
N. Balepur, R. Rudinger, and J. L. Boyd-Graber
Which of these best describes multiple choice evaluation with llms? a) forced b) flawed c) fixable d) all of the above
.
External Links:
2502.14127
,
Link
Cited by:
§2.2
.
Barke
et al.
(2023)
S. Barke, M. B. James, and N. Polikarpova
Grounded copilot: how programmers interact with code-generating models
.
Proc. ACM Program. Lang.
7
(
OOPSLA1
).
External Links:
Link
,
Document
Cited by:
§1
.
Beigi
et al.
(2024)
M. Beigi, Y. Shen, R. Yang, Z. Lin, Q. Wang, A. Mohan, J. He, M. Jin, C. Lu, and L. Huang
InternalInspector
I
2
I^{2}
: robust confidence estimation in LLMs through internal states
.
In
Findings of the Association for Computational Linguistics: EMNLP 2024
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 12847–12865
.
External Links:
Link
,
Document
Cited by:
§8
.
Bender
et al.
(2021)
E. M. Bender, T. Gebru, A. McMillan-Major, and S. Shmitchell
On the dangers of stochastic parrots: can language models be too big?
.
In
Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency
,
FAccT ’21
,
New York, NY, USA
,
pp. 610–623
.
External Links:
ISBN 9781450383097
,
Link
,
Document
Cited by:
§3
.
Bender and Koller (2020)
E. M. Bender and A. Koller
Climbing towards NLU: On meaning, form, and understanding in the age of data
.
In
Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics
,
D. Jurafsky, J. Chai, N. Schluter, and J. Tetreault (Eds.)
,
Online
,
pp. 5185–5198
.
External Links:
Link
,
Document
Cited by:
§3
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
§1
.
Bolukbasi
et al.
(2016)
T. Bolukbasi, K. Chang, J. Zou, V. Saligrama, and A. Kalai
Man is to computer programmer as woman is to homemaker? debiasing word embeddings
.
In
Proceedings of the 30th International Conference on Neural Information Processing Systems
,
NIPS’16
,
Red Hook, NY, USA
,
pp. 4356–4364
.
External Links:
ISBN 9781510838819
Cited by:
§1
.
Bui
et al.
(2025)
T. Bui, T. T. Vu, T. Nguyen, S. Nguyen, and H. D. Vo
Correctness assessment of code generated by large language models using internal representations
.
External Links:
2501.12934
,
Link
Cited by:
§8
.
Cao
et al.
(2025)
Z. Cao, S. Apel, A. Singla, and V. Demberg
Pragmatic reasoning improves llm code generation
.
External Links:
2502.15835
,
Link
Cited by:
§3
.
Chen
et al.
(2019)
A. Chen, G. Stanovsky, S. Singh, and M. Gardner
Evaluating question answering evaluation
.
In
Proceedings of the 2nd Workshop on Machine Reading for Question Answering
,
A. Fisch, A. Talmor, R. Jia, M. Seo, E. Choi, and D. Chen (Eds.)
,
Hong Kong, China
,
pp. 119–124
.
External Links:
Link
,
Document
Cited by:
item 2)
,
§2.2
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba
Evaluating large language models trained on code
.
External Links:
2107.03374
,
Link
Cited by:
§1
,
§1
,
1st item
,
§3
,
§4.1.1
,
1st item
.
Chen
et al.
(2025)
W. Chen, L. Zhang, L. Zhong, L. Peng, Z. Wang, and J. Shang
Memorize or generalize? evaluating llm code generation with evolved questions
.
External Links:
2503.02296
,
Link
Cited by:
§4.2.3
.
Chen
et al.
(2023)
Y. Chen, F. Viégas, and M. Wattenberg
Beyond surface statistics: scene representations in a latent diffusion model
.
External Links:
2306.05720
,
Link
Cited by:
§1
.
Clark
et al.
(2018)
P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord
Think you have solved question answering? try arc, the AI2 reasoning challenge
.
CoRR
abs/1803.05457
.
External Links:
Link
,
1803.05457
Cited by:
§2.2
.
Conmy
et al.
(2024)
A. Conmy, A. N. Mavor-Parker, A. Lynch, S. Heimersheim, and A. Garriga-Alonso
Towards automated circuit discovery for mechanistic interpretability
.
In
Proceedings of the 37th International Conference on Neural Information Processing Systems
,
NIPS ’23
,
Red Hook, NY, USA
.
Cited by:
§2.1
.
Fan
et al.
(2024)
Z. Fan, H. Ruan, S. Mechtaev, and A. Roychoudhury
Oracle-guided program selection from large language models
.
In
Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis
,
ISSTA 2024
,
New York, NY, USA
,
pp. 628–640
.
External Links:
ISBN 9798400706127
,
Link
,
Document
Cited by:
§3
.
Fu
et al.
(2025)
Y. Fu, P. Liang, A. Tahir, Z. Li, M. Shahin, J. Yu, and J. Chen
Security weaknesses of copilot-generated code in github projects: an empirical study
.
ACM Trans. Softw. Eng. Methodol.
.
Note:
Just Accepted
External Links:
ISSN 1049-331X
,
Link
,
Document
Cited by:
§1
.
Github-Copilot (2025)
Github-Copilot
Pull Request: Fix IndexOutOfRangeException in RegexInterpreter.Backtrack method
.
External Links:
https://github.com/dotnet/runtime/pull/115733
,
Link
Cited by:
§1
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
Proceedings of the 34th International Conference on Machine Learning - Volume 70
,
ICML’17
,
pp. 1321–1330
.
Cited by:
§8
.
Hendrycks
et al.
(2021a)
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song, and J. Steinhardt
Measuring coding challenge competence with APPS
.
In
Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)
,
External Links:
Link
Cited by:
3rd item
.
Hendrycks
et al.
(2021b)
D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt
Measuring massive multitask language understanding
.
In
International Conference on Learning Representations
,
External Links:
Link
Cited by:
§8
.
Hernandez
et al.
(2022)
E. Hernandez, S. Schwettmann, D. Bau, T. Bagashvili, A. Torralba, and J. Andreas
Natural language descriptions of deep visual features
.
External Links:
2201.11114
,
Link
Cited by:
§1
.
Hindle
et al.
(2012)
A. Hindle, E. T. Barr, Z. Su, M. Gabel, and P. Devanbu
On the naturalness of software
.
In
Proceedings of the 34th International Conference on Software Engineering
,
ICSE ’12
,
pp. 837–847
.
External Links:
ISBN 9781467310673
Cited by:
§1
.
Hou
et al.
(2024)
X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy, and H. Wang
Large language models for software engineering: a systematic literature reviewLarge language models for software engineering: a systematic literature review
.
ACM Trans. Softw. Eng. Methodol.
33
(
8
).
External Links:
ISSN 1049-331X
,
Link
,
Document
Cited by:
§8
.
Huang
et al.
(2025)
Y. Huang, L. Ma, K. Nishikino, and T. Akazaki
Risk Assessment Framework for Code LLMs via Leveraging Internal States
.
arXiv e-prints
,
pp. arXiv:2504.14640
.
External Links:
Document
,
2504.14640
Cited by:
§8
.
Inala
et al.
(2022)
J. P. Inala, C. Wang, M. Yang, A. Codas, M. Encarnación, S. K. Lahiri, M. Musuvathi, and J. Gao
Fault-aware neural code rankers
.
External Links:
2206.03865
,
Link
Cited by:
§6.1
,
§8
.
Jimenez
et al.
(2024)
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. R. Narasimhan
SWE-bench: can language models resolve real-world github issues?
.
In
The Twelfth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§7
.
Kadavath
et al.
(2022)
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson, S. Johnston, S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen, Y. Bai, S. Bowman, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion, S. Kravec, L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei, T. Brown, J. Clark, N. Joseph, B. Mann, S. McCandlish, C. Olah, and J. Kaplan
Language models (mostly) know what they know
.
External Links:
2207.05221
,
Link
Cited by:
§1
,
2nd item
.
Kirstain
et al.
(2022)
Y. Kirstain, P. Lewis, S. Riedel, and O. Levy
A few more examples may be worth billions of parameters
.
In
Findings of the Association for Computational Linguistics: EMNLP 2022
,
Y. Goldberg, Z. Kozareva, and Y. Zhang (Eds.)
,
Abu Dhabi, United Arab Emirates
,
pp. 1017–1029
.
External Links:
Link
,
Document
Cited by:
§8
.
Kwiatkowski
et al.
(2019)
T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, A. Parikh, C. Alberti, D. Epstein, I. Polosukhin, J. Devlin, K. Lee, K. Toutanova, L. Jones, M. Kelcey, M. Chang, A. M. Dai, J. Uszkoreit, Q. Le, and S. Petrov
Natural questions: a benchmark for question answering research
.
Transactions of the Association for Computational Linguistics
7
,
pp. 452–466
.
External Links:
Link
,
Document
Cited by:
§2.2
.
Leveson (2012)
N. G. Leveson
Engineering a safer world: systems thinking applied to safety
.
The MIT Press
.
External Links:
ISBN 9780262298247
,
Document
,
Link
,
https://direct.mit.edu/book-pdf/2280500/book_9780262298247.pdf
Cited by:
§2.1
.
Li
et al.
(2024a)
J. Li, Y. Zhu, Y. Li, G. Li, and Z. Jin
Showing llm-generated code selectively based on confidence of llms
.
External Links:
2410.03234
,
Link
Cited by:
§8
.
Li
et al.
(2024b)
J. Li, Y. Zhang, Z. Karas, C. McMillan, K. Leach, and Y. Huang
Do machines and humans focus on similar code? exploring explainability of large language models in code summarization
.
In
Proceedings of the 32nd IEEE/ACM International Conference on Program Comprehension
,
ICPC ’24
,
New York, NY, USA
,
pp. 47–51
.
External Links:
ISBN 9798400705861
,
Link
,
Document
Cited by:
§8
.
Li
et al.
(2024c)
S. Li, Y. Cheng, J. Chen, J. Xuan, S. He, and W. Shang
Assessing the performance of ai-generated code: a case study on github copilot
.
In
2024 IEEE 35th International Symposium on Software Reliability Engineering (ISSRE)
,
Vol.
,
pp. 216–227
.
External Links:
Document
Cited by:
§1
.
Li
et al.
(2024d)
W. Li, L. Li, T. Xiang, X. Liu, W. Deng, and N. Garcia
Can multiple-choice questions really be useful in detecting the abilities of LLMs?
.
In
Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)
,
N. Calzolari, M. Kan, V. Hoste, A. Lenci, S. Sakti, and N. Xue (Eds.)
,
Torino, Italia
,
pp. 2819–2834
.
External Links:
Link
Cited by:
item 2)
.
Li
et al.
(2022)
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy, C. de Masson d’Autume, I. Babuschkin, X. Chen, P. Huang, J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S. Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals
Competition-level code generation with alphacodeCompetition-level code generation with alphacode
.
Science
378
(
6624
),
pp. 1092–1097
.
External Links:
Document
,
Link
,
https://www.science.org/doi/pdf/10.1126/science.abq1158
Cited by:
§1
,
1st item
,
2nd item
.
Lin
et al.
(2022a)
S. Lin, J. Hilton, and O. Evans
Teaching models to express their uncertainty in words
.
Trans. Mach. Learn. Res.
2022
.
External Links:
Link
Cited by:
§1
,
1st item
.
Lin
et al.
(2022b)
S. Lin, J. Hilton, and O. Evans
TruthfulQA: measuring how models mimic human falsehoods
.
In
Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
S. Muresan, P. Nakov, and A. Villavicencio (Eds.)
,
Dublin, Ireland
,
pp. 3214–3252
.
External Links:
Link
,
Document
Cited by:
item 3)
,
§2.2
,
§3
.
Lin
et al.
(2024)
Z. Lin, S. Trivedi, and J. Sun
Contextualized sequence likelihood: enhanced confidence scores for natural language generation
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 10351–10368
.
External Links:
Link
,
Document
Cited by:
§8
.
Liu
et al.
(2023)
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
Is your code generated by chatGPT really correct? rigorous evaluation of large language models for code generation
.
In
Thirty-seventh Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
item (2)
,
§4.1.1
.
Lo (2023)
D. Lo
Trustworthy and Synergistic Artificial Intelligence for Software Engineering: Vision and Roadmaps
.
In
2023 IEEE/ACM International Conference on Software Engineering: Future of Software Engineering (ICSE-FoSE)
,
Vol.
,
Los Alamitos, CA, USA
,
pp. 69–85
.
External Links:
ISSN
,
Document
,
Link
Cited by:
§1
.
Majdinasab
et al.
(2024)
V. Majdinasab, M. J. Bishop, S. Rasheed, A. Moradidakhel, A. Tahir, and F. Khomh
Assessing the security of github copilot’s generated code - a targeted replication study
.
In
2024 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER)
,
Vol.
,
pp. 435–444
.
External Links:
Document
Cited by:
§1
.
Mcintosh
et al.
(2016)
S. Mcintosh, Y. Kamei, B. Adams, and A. E. Hassan
An empirical study of the impact of modern code review practices on software quality
.
Empirical Softw. Engg.
21
(
5
),
pp. 2146–2189
.
External Links:
ISSN 1382-3256
,
Link
,
Document
Cited by:
§1
.
Mezzi
et al.
(2025)
E. Mezzi, F. Massacci, and K. Tuma
Large language models are unreliable for cyber threat intelligence
.
External Links:
2503.23175
,
Link
Cited by:
§8
.
Mihaylov
et al.
(2018)
T. Mihaylov, P. Clark, T. Khot, and A. Sabharwal
Can a suit of armor conduct electricity? a new dataset for open book question answering
.
In
Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing
,
E. Riloff, D. Chiang, J. Hockenmaier, and J. Tsujii (Eds.)
,
Brussels, Belgium
,
pp. 2381–2391
.
External Links:
Link
,
Document
Cited by:
§2.2
.
Mikolov
et al.
(2013)
T. Mikolov, W. Yih, and G. Zweig
Linguistic regularities in continuous space word representations
.
In
Proceedings of the 2013 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies
,
L. Vanderwende, H. Daumé III, and K. Kirchhoff (Eds.)
,
Atlanta, Georgia
,
pp. 746–751
.
External Links:
Link
Cited by:
§1
.
Mo
et al.
(2025)
R. Mo, D. Wang, W. Zhan, Y. Jiang, Y. Wang, Y. Zhao, Z. Li, and Y. Ma
Assessing and analyzing the correctness of github copilot’s code suggestions
.
ACM Trans. Softw. Eng. Methodol.
.
Note:
Just Accepted
External Links:
ISSN 1049-331X
,
Link
,
Document
Cited by:
§1
.
Molfese
et al.
(2025)
F. M. Molfese, L. Moroni, L. Gioffrè, A. Scirè, S. Conia, and R. Navigli
Right answer, wrong score: uncovering the inconsistencies of llm evaluation in multiple-choice question answering
.
External Links:
2503.14996
,
Link
Cited by:
item 1)
.
Moon
et al.
(2025)
J. Moon, Y. Hwang, D. Lee, T. Kang, Y. Kim, and K. Jung
Don’t judge code by its cover: exploring biases in llm judges for code evaluation
.
External Links:
2505.16222
,
Link
Cited by:
§8
.
Nguyen and Nadi (2022)
N. Nguyen and S. Nadi
An empirical evaluation of github copilot’s code suggestions
.
In
Proceedings of the 19th International Conference on Mining Software Repositories
,
MSR ’22
,
New York, NY, USA
,
pp. 1–5
.
External Links:
ISBN 9781450393034
,
Link
,
Document
Cited by:
§1
.
Oquab
et al.
(2024)
M. Oquab, T. Darcet, T. Moutakanni, H. V. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby, M. Assran, N. Ballas, W. Galuba, R. Howes, P. Huang, S. Li, I. Misra, M. Rabbat, V. Sharma, G. Synnaeve, H. Xu, H. Jégou, J. Mairal, P. Labatut, A. Joulin, and P. Bojanowski
DINOv2: learning robust visual features without supervision
.
Trans. Mach. Learn. Res.
2024
.
External Links:
Link
Cited by:
§1
.
Pearce
et al.
(2025)
H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri
Asleep at the keyboard? assessing the security of github copilot’s code contributions
.
Commun. ACM
68
(
2
),
pp. 96–105
.
External Links:
ISSN 0001-0782
,
Link
,
Document
Cited by:
§8
.
Ponzanelli
et al.
(2014)
L. Ponzanelli, G. Bavota, M. D. Penta, R. Oliveto, and M. Lanza
Prompter: a self-confident recommender system
.
In
2014 IEEE International Conference on Software Maintenance and Evolution
,
Vol.
,
pp. 577–580
.
External Links:
Document
Cited by:
§6.1
.
Project (2024)
B. Project
BigCodeBench v0.2.4
.
Note:
https://github.com/bigcode-project/bigcodebench/releases/tag/v0.2.4
Accessed: 2025-07-18
Cited by:
§4.1.1
.
Project (2025)
B. Project
BigCode evaluation harness
.
Note:
Accessed: 2025-07-18
External Links:
Link
Cited by:
§7
.
Radford
et al.
(2017)
A. Radford, R. Jozefowicz, and I. Sutskever
Learning to generate reviews and discovering sentiment
.
External Links:
1704.01444
,
Link
Cited by:
§1
.
Rajpurkar
et al.
(2016)
P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang
SQuAD: 100,000+ questions for machine comprehension of text
.
External Links:
1606.05250
,
Link
Cited by:
§2.2
.
Reddy
et al.
(2019)
S. Reddy, D. Chen, and C. D. Manning
CoQA: a conversational question answering challenge
.
External Links:
1808.07042
,
Link
Cited by:
§2.2
.
Robinson
et al.
(2023)
J. Robinson, C. M. Rytting, and D. Wingate
Leveraging large language models for multiple choice question answering
.
External Links:
2210.12353
,
Link
Cited by:
item 1)
,
§2.2
.
Schramowski
et al.
(2019)
P. Schramowski, C. Turan, S. Jentzsch, C. Rothkopf, and K. Kersting
BERT has a moral compass: improvements of ethical and moral values of machines
.
External Links:
1912.05238
,
Link
Cited by:
§1
.
Sharma and David (2025)
A. Sharma and C. David
Assessing correctness in llm-based code generation via uncertainty estimation
.
External Links:
2502.11620
,
Link
Cited by:
§6.3
.
Singh
et al.
(2024)
C. Singh, J. P. Inala, M. Galley, R. Caruana, and J. Gao
Rethinking interpretability in the era of large language models
.
External Links:
2402.01761
,
Link
Cited by:
§8
.
Spiess
et al.
(2024)
C. Spiess, D. Gros, K. S. Pai, M. Pradel, M. R. I. Rabin, A. Alipour, S. Jha, P. Devanbu, and T. Ahmed
Calibration and correctness of language models for code
.
External Links:
2402.02047
,
Link
Cited by:
§1
,
§1
,
1st item
,
1st item
,
2nd item
,
§6.3
,
§8
.
Sun
et al.
(2024)
Z. Sun, Y. Wan, J. Li, H. Zhang, Z. Jin, G. Li, and C. Lyu
Sifting through the chaff: on utilizing execution feedback for ranking the generated code candidates
.
In
Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering
,
ASE ’24
,
New York, NY, USA
,
pp. 229–241
.
External Links:
ISBN 9798400712487
,
Link
,
Document
Cited by:
§1
,
3rd item
,
§8
.
Svyatkovskiy
et al.
(2020)
A. Svyatkovskiy, S. K. Deng, S. Fu, and N. Sundaresan
IntelliCode compose: code generation using transformer
.
ESEC/FSE 2020
,
New York, NY, USA
,
pp. 1433–1443
.
External Links:
ISBN 9781450370431
,
Link
,
Document
Cited by:
§1
.
Talmor
et al.
(2019)
A. Talmor, J. Herzig, N. Lourie, and J. Berant
CommonsenseQA: a question answering challenge targeting commonsense knowledge
.
In
Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)
,
J. Burstein, C. Doran, and T. Solorio (Eds.)
,
Minneapolis, Minnesota
,
pp. 4149–4158
.
External Links:
Link
,
Document
Cited by:
§2.2
.
Team (2024)
E. Team
EvalPlus mbpp+ release v0.2.0
.
Note:
https://github.com/evalplus/mbppplus_release/releases/tag/v0.2.0
Accessed: 2025-07-18
Cited by:
item (2)
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
Tian
et al.
(2023)
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. Manning
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
H. Bouamor, J. Pino, and K. Bali (Eds.)
,
Singapore
,
pp. 5433–5442
.
External Links:
Link
,
Document
Cited by:
§1
,
§1
,
1st item
,
§8
.
Vaswani
et al.
(2017)
A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin
Attention is all you need
.
In
Advances in Neural Information Processing Systems
,
I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett (Eds.)
,
Vol.
30
,
pp.
.
External Links:
Link
Cited by:
§2.1
.
Wang
et al.
(2025a)
Y. Wang, T. Jiang, M. Liu, J. Chen, M. Mao, X. Liu, Y. Ma, and Z. Zheng
Beyond functional correctness: investigating coding style inconsistencies in large language models
.
External Links:
2407.00456
,
Link
Cited by:
§6.4
.
Wang
et al.
(2023)
Y. Wang, H. Le, A. Gotmare, N. Bui, J. Li, and S. Hoi
CodeT5+: open code large language models for code understanding and generation
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
H. Bouamor, J. Pino, and K. Bali (Eds.)
,
Singapore
,
pp. 1069–1088
.
External Links:
Link
,
Document
Cited by:
3rd item
.
Wang
et al.
(2025b)
Z. Wang, Z. Zhou, D. Song, Y. Huang, S. Chen, L. Ma, and T. Zhang
Towards Understanding the Characteristics of Code Generation Errors Made by Large Language Models
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)
,
Vol.
,
Los Alamitos, CA, USA
,
pp. 2587–2599
.
External Links:
ISSN
,
Document
,
Link
Cited by:
§8
.
Wei
et al.
(2024)
F. Wei, X. Chen, and L. Luo
Rethinking generative large language model evaluation for semantic comprehension
.
External Links:
2403.07872
,
Link
Cited by:
item 3)
.
Welleck
et al.
(2024)
S. Welleck, A. Bertsch, M. Finlayson, H. Schoelkopf, A. Xie, G. Neubig, I. Kulikov, and Z. Harchaoui
From decoding to meta-generation: inference-time algorithms for large language models
.
External Links:
2406.16838
,
Link
Cited by:
§1
.
Xue
et al.
(2024)
M. Xue, Z. Hu, L. Liu, K. Liao, S. Li, H. Han, M. Zhao, and C. Yin
Strengthened symbol binding makes large language models reliable multiple-choice selectors
.
In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
,
L. Ku, A. Martins, and V. Srikumar (Eds.)
,
Bangkok, Thailand
,
pp. 4331–4344
.
External Links:
Link
,
Document
Cited by:
§2.2
.
Yoo and Harman (2012)
S. Yoo and M. Harman
Regression testing minimization, selection and prioritization: a survey
.
Software Testing, Verification and Reliability
22
(
2
),
pp. 67–120
.
External Links:
Document
,
Link
,
https://onlinelibrary.wiley.com/doi/pdf/10.1002/stvr.430
Cited by:
§6.1
.
Zampetti
et al.
(2019)
F. Zampetti, G. Bavota, G. Canfora, and M. D. Penta
A study on the interplay between pull request review and continuous integration builds
.
In
2019 IEEE 26th International Conference on Software Analysis, Evolution and Reengineering (SANER)
,
Vol.
,
pp. 38–48
.
External Links:
Document
Cited by:
§1
.
Zhang
et al.
(2025)
A. Zhang, Y. Chen, J. Pan, C. Zhao, A. Panda, J. Li, and H. He
Reasoning models know when they’re right: probing hidden states for self-verification
.
External Links:
2504.05419
,
Link
Cited by:
§6.3
.
Zhang
et al.
(2024)
C. Zhang, F. Liu, M. Basaldella, and N. Collier
LUQ: long-text uncertainty quantification for LLMs
.
In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 5244–5262
.
External Links:
Link
,
Document
Cited by:
§8
.
Zhang
et al.
(2023a)
S. Zhang, Z. Chen, Y. Shen, M. Ding, J. B. Tenenbaum, and C. Gan
Planning with large language models for code generation
.
External Links:
2303.05510
,
Link
Cited by:
§1
.
Zhang
et al.
(2023b)
T. Zhang, T. Yu, T. B. Hashimoto, M. Lewis, W. Yih, D. Fried, and S. I. Wang
Coder reviewer reranking for code generation
.
In
Proceedings of the 40th International Conference on Machine Learning
,
ICML’23
.
Cited by:
§1
,
§3
.
Zhou
et al.
(2023)
K. Zhou, D. Jurafsky, and T. Hashimoto
Navigating the grey area: how expressions of uncertainty and overconfidence affect language models
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
,
H. Bouamor, J. Pino, and K. Bali (Eds.)
,
Singapore
,
pp. 5506–5524
.
External Links:
Link
,
Document
Cited by:
§1
,
1st item
.
Zhu
et al.
(2024)
Y. Zhu, J. Li, G. Li, Y. Zhao, J. Li, Z. Jin, and H. Mei
Hot or cold? adaptive temperature sampling for code generation with large language models
.
Proceedings of the AAAI Conference on Artificial Intelligence
38
(
1
),
pp. 437–445
.
External Links:
Link
,
Document
Cited by:
§1
.
Zhuo
et al.
(2024)
T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf, H. Zhan, J. He, I. Paul,
et al.
BigCodeBench: benchmarking code generation with diverse function calls and complex instructions
.
arXiv preprint arXiv:2406.15877
.
Cited by:
§1
,
§4.1.1
.
Zou
et al.
(2023)
A. Zou, L. Phan, S. Chen, J. Campbell, P. Guo, R. Ren, A. Pan, X. Yin, M. Mazeika, A. Dombrowski, S. Goel, N. Li, M. J. Byun, Z. Wang, A. Mallen, S. Basart, S. Koyejo, D. Song, M. Fredrikson, J. Z. Kolter, and D. Hendrycks
Representation engineering: a top-down approach to ai transparency
.
External Links:
2310.01405
,
Link
Cited by:
§1
,
§2.1
,
§2.1
,
§2.1
,
§2.2
,
§2
,
§8
.