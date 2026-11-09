---
title: Comparing Developer and LLM Biases in Code Evaluation
id: comparing-developer-and-llm-biases-in-code-evaluation
tags:
- aaai-bar-eval-dprc-d78e07
- llm-as-judge
- rubric-evaluation
- code-evaluation
created: '2026-07-19T20:02:16.569767Z'
updated: '2026-07-19T20:07:04.467132Z'
source: https://arxiv.org/html/2603.24586v1
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:16.569153Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'TRACE (Mittal, Shar, Wu, Agarwal, Wu, Donahue, Talwalkar, Chi, Chen; CMU;
  arXiv:2603.24586, Mar 2026, venue not yet confirmed -- likely under review given
  the recency). Evaluates 13 LLM judges (3rd-party general models, specialized fine-tuned
  judges e.g. Prometheus/Atla Selene, and reward models) against human developer preferences
  across three code-interaction modalities: chat-based programming, IDE autocompletion,
  instructed code editing. Headline: best LLM judges underperform human majority agreement
  by 12-23 percentage points on every modality; no judge dominates; specialized fine-tuned
  judges do not reliably beat general-purpose ones. TRACE auto-extracts natural-language
  ''rubric items'' (e.g. Explicitness/Clarity, Functional/Logical Alignment, Domain-Specific
  Detail) from pairwise diffs, trains logistic regression to weight them per-judge
  vs per-human, and finds 35 significant judge-vs-human weighting gaps -- 6 of 11
  rubric themes that map onto established SE code-quality criteria still show significant
  judge-human misalignment. Judges also show strong position bias (8-45pp swing accuracy
  gaps). Relevance to DPRC: this is NOT about competitive-vs-functional all-or-nothing
  correctness (that WebSearch snippet mischaracterized it); rather it is evidence
  that PARTIAL/RUBRIC-BASED evaluation of code is an active, CMU-backed research direction
  distinct from binary pass/fail, and that current LLM-based partial-credit judging
  is itself poorly calibrated to human judgment -- a caution that any downstream ''confidence
  about partial correctness'' claim in DPRC should not lean on LLM-judge rubric scores
  as ground truth without validation. Long source (11,376 words); flagged for potential
  source-analyst deep-dive given density of quantitative misalignment results (Tables
  2-8) not fully captured here.'
---

Comparing Developer and LLM Biases in Code Evaluation
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2603.24586v1 [cs.SE] 25 Mar 2026
Comparing Developer and LLM Biases in Code Evaluation
Aditya Mittal
∗
Ryan Shar
∗
Zichu Wu   Shyam Agarwal
Tongshuang Wu   Chris Donahue   Ameet Talwalkar
Wayne Chi
†
Valerie Chen
†
Carnegie Mellon University
{adityamittal307, ryan.shar01}@gmail.com
Abstract
As LLMs are increasingly used as judges in code applications, they should be evaluated in realistic interactive settings that capture partial context and ambiguous intent.
We present
TRACE
(
T
ool for
R
ubric
A
nalysis in
C
ode
E
valuation), a framework that evaluates LLM judges’ ability to predict human preferences and automatically extracts rubric items to reveal systematic biases in how humans and models weigh each item.
Across three modalities—chat-based programming, IDE autocompletion, and instructed code editing—we use
TRACE
to measure how well LLM judges align with developer preferences.
Among 13 different models, the best judges underperform human annotators by
12-23%
.
TRACE
identifies 35 significant sources of misalignment between humans and judges across interaction modalities, the majority of which correspond to existing software engineering code quality criteria.
For example, in chat-based coding, judges are biased towards longer code explanations while humans prefer shorter ones.
We find significant misalignment on the majority of existing code quality dimensions, showing alignment gaps between LLM judges and human preference in realistic coding applications.
1
Introduction
As LLM-powered tools accelerate software development
[
peng2023impactaideveloperproductivity
]
, there is an increasing need for reliable evaluation methods
[
chen2025surveyevaluatinglargelanguage
]
.
LLM-as-a-judge approaches have emerged as a widely-used, scalable alternative to human evaluation for assessing model outputs
[
li2025generationjudgmentopportunitieschallenges
]
, including in domains like software engineering
[
Wang_2025
]
.
Existing work typically considers static settings, using polished code from well-maintained GitHub repositories
[
li2024evocodebenchevolvingcodegeneration
,
11071936
]
or competitive programming tasks
[
jiang2025codejudgebenchbenchmarkingllmasajudgecoding
,
qing2025effibenchxmultilanguagebenchmarkmeasuring
]
.
While grounded in real software artifacts, these sources fail to capture the messy and underspecified conditions in which developers evaluate and refine code in the course of development, revealing little about whether LLM judges reflect the implicit criteria developers apply in practical engineering contexts.
We ask:
what biases do LLM judges exhibit when evaluating code, and how do they compare to those of developers?
Since real software development rarely occurs in such static settings, evaluation of LLM outputs should capture functional correctness along with developer intent, constraints, and workflow expectations.
Empirical evidence shows that only 25% of GitHub autocompletions are accepted by developers and users often report that models fail to meet specific requirements or match their expectations
[
ziegler2022productivityassessmentneuralcode
,
Liang2023ALS
]
.
To understand these challenges observed in AI-assisted software development, we examine three representative interaction modalities identified in developer-AI taxonomies
[
treude2025developersinteractaitaxonomy
]
: chat-based programming assistance
[
chiang2024chatbotarenaopenplatform
]
, IDE autocompletion
[
chi2025copilotarenaplatformcode
]
, and instructed code editing
[
chi2025editbenchevaluatingllmabilities
]
. By comparing LLM judgments to developers’ preferences across these settings, we analyze how judges weight code quality criteria in practice and where their biases diverge from human preferences.
Figure 1
:
Example of developer–LLM misalignment on a code editing task.
Here, the developer provides a prompt and receives two LLM code solutions. In this example, the user prefers the top response while the LLM judge selects the bottom response. We compare these responses with the extracted rubric items to see that the developer
prefers less robustness and more comments, while LLM judges prefer more robustness and fewer comments.
We propose
TRACE
(
T
ool for
R
ubric
A
nalysis in
C
ode
E
valuation), a framework for evaluating and interpreting LLM-based judges in realistic developer workflows.
TRACE
measures how closely model judgments align with human preferences in the ambiguity of real-world settings.
Beyond aggregate agreement, we focus on cases of divergence between model and human evaluations.
To explain these disagreements,
TRACE
automatically discovers decision criteria that account for judgment differences across samples. Building on prior work in automatic LLM-based criteria discovery
[
Dunlap:2025
,
kim2025evaletevaluatinglargelanguage
,
findeis2025inverseconstitutionalaicompressing
]
, we aggregate differences in responses to create a set of qualitative, interpretable “rubric” items.
We then analyze how both human and model judgments correlate with these rubric items, revealing systematic differences in evaluation behavior and bias across judges and modalities (Figure
1
).
Our results across a diverse set of 13 judges, including general-purpose third-party models, specialized judge models, and reward models, and three interaction modalities show that:
•
LLM judges consistently underperform compared to human developers.
Across the three interaction modalities, the strongest LLM judges underperform the majority human agreement by 12 to 23 percentage points, and no single judge consistently dominates. Notably, fine-tuned judge LLMs do not reliably outperform general-purpose models, suggesting that current shortcomings are not solely due to training data or specialization.
•
In each modality, human and LLM judges are misaligned on different rubric items.
We identify 35 significant gaps across the three modalities.
In code completion, judges tend to overweight whether code is functional and underweight whether it is readable inside a live file. In edits, judges more often discount clarity, while developers expect changes to be precise. In chat, judges typically reward generic explanations, while humans prefer context-aware solutions. These gaps show there are multiple notions of “good code,” depending on modality, and judges are unable to reliably capture these nuances.
•
Judges are misaligned on established software engineering criteria.
Across three interaction modalities in code, we identify 16 recurring evaluation themes, with 11 aligning closely with canonical software engineering criteria like
syntactic correctness
,
formatting
, and
robustness
. We find that LLM judges remain significantly misaligned with human preference on 6 of these 11 themes across modalities, suggesting there exists alignment gaps with human preference on code quality during judge training.
2
Related Work
Interaction Modalities in Software Engineering.
LLMs now support a range of interaction modalities
in software development, from real-time, low-overhead code completion
[
Svyatkovskiy2020IntelliCodeCC
,
Pu2025AssistanceOD
]
, to conversational chat for multi-turn problem solving
[
Ross2023ThePA
]
, to emerging agent systems that autonomously modify codebases
[
Chen2025CodeWM
,
Li2025DeepCodeOA
]
. Prior work shows these modes induce distinct usage patterns
[
Barke2022GroundedCH
,
Weber2024SignificantPG
]
and that adoption hinges on reducing effort and accelerating tasks
[
Vaithilingam2022ExpectationVE
,
Liang2023UnderstandingTU
,
Mozannar2022ReadingBT
]
, while preserving user control, contextual grounding, and trust
[
Chen2025ScreenRP
,
Liang2023ALS
,
Brandebusemeyer2025DevelopersExperienceWG
,
Awad2025PreFilteringCS
,
Kula2025TheSF
,
Lyu2025MyPI
]
.
Our work studies LLM judges across multiple interaction modalities in software engineering to evaluate and compare judges with human preferences in each of these development contexts.
LLM as a Judge.
With the growing adoption of LLM judges, researchers have proposed many techniques to align LLMs with human preferences.
These include fine-tuning approaches
[
wang2025djpo
]
, which produce specialized judge models such as JudgeLM
[
zhu2025judgelm
]
, Prometheus
[
kim2024prometheus
]
, and Atla Selene Mini
[
alexandru2025atlaseleneminigeneral
]
. Additionally, judgment alignment can be improved with inference time methods using multiple LLMs
[
verga2024juries
]
and structured prompting frameworks
[
jung2025trust
]
.
Specialized benchmarks were developed for systematically comparing LLM judges.
For example, JudgeBench
[
judgebench2024
]
uses pairwise questions using objective correctness and Arena-Hard
[
li2024crowdsourceddatahighqualitybenchmarks
]
curates high-quality in-the-wild human prompts for evaluation.
We build on this line of work by evaluating LLM judges on code-specific tasks drawn from in-the-wild developer interactions to place judges in realistic, ambiguous situations developers face in practice.
Figure 2
:
Overview of TRACE.
Given a set of pairwise options,
TRACE
follows a three-step workflow:
(1)
we collect LLM judgments between responses to measure alignment with human preferences;
(2)
we automatically generate rubric criteria capturing differences between responses (e.g.,
error handling
), then aggregate these criteria to form a comprehensive evaluation rubric;
(3)
we construct feature vectors from rubric scores on each sample and train a logistic regression model to predict LLM judgments. We use the learned coefficients to identify which rubric dimensions drive misalignment between LLMs and humans.
Explaining LLM Decisions.
As LLM judges expand across domains, there is a need to explain LLM judgements
[
ryu-etal-2023-retrieval
,
brake-schaaf-2024-comparing
]
.
Existing work like WIMHF
[
movva2025whatshumanfeedbacklearning
]
measures pairwise preferences by training an SAE on embedding differences to encode latent features in responses. Other approaches remove the need for training. VibeCheck
[
Dunlap:2025
]
offers an initial approach to identify evaluation criteria from pairwise differences using LLMs. Evalet
[
kim2025evaletevaluatinglargelanguage
]
provides a method for analyzing LLM judge alignment given a set of evaluation criteria from the user. ICAI
[
findeis2025inverseconstitutionalaicompressing
]
proposes a method to generate explicit instruction criteria for alignment, but these criteria do not generalize across the entire dataset for multiple judges.
We extend these approaches to automatically discover interpretable rubric items to compare human and LLM judge biases across interaction modalities.
3
Methodology
Given a dataset of human preferences and a set of candidate LLM judges, how do we determine which judge best aligns with human preferences and compare human and judge biases?
TRACE
answers these questions in three stages (Figure
2
): (1) we measure whether LLM judges agree with human pairwise preferences; (2) we generate interpretable rubric items that capture the evaluative criteria distinguishing response pairs; (3) we quantify where judges assign different importance to these rubric items relative to humans.
In subsequent sections, we show how to apply
TRACE
to multiple interaction datasets for code evaluation.
3.1
Step 1: Measure Whether Judge Predicts Human Preferences
We begin by measuring whether LLM judges can predict human preferences. Each dataset—see Section
4.1
for examples—consists of
n
n
pairwise preference examples of the form
(
x
,
y
A
,
y
B
,
w
)
(x,y_{A},y_{B},w)
, where
x
x
denotes the input context,
y
A
y_{A}
and
y
B
y_{B}
are candidate responses, and
w
∈
{
−
1
,
1
}
w\in\{-1,1\}
is a binary label indicating human preference (
w
=
1
w=1
for
y
A
y_{A}
,
w
=
−
1
w=-1
for
y
B
y_{B}
).
To perform inference with an LLM judge
J
J
, we provide
(
x
,
y
A
,
y
B
)
(x,y_{A},y_{B})
as input and prompt the judge to select the better answer between
y
A
y_{A}
and
y
B
y_{B}
.
The judge outputs a binary decision
J
​
(
x
,
y
A
,
y
B
)
∈
{
−
1
,
1
}
J(x,y_{A},y_{B})\in\{-1,1\}
indicating which response it prefers, following prior LLM-as-a-judge frameworks
[
zheng2023judgingllmasajudgemtbenchchatbot
]
.
Prior work shows that LLM judges exhibit positional bias. To account for this, we report both overall accuracy and positionally consistent accuracy. We compute positionally consistent accuracy by evaluating each sample twice, once in the original order and once with responses swapped. We then discard cases where the judge’s predictions differ.
Full prompts are provided in Appendix
A.1
.
3.2
Step 2: Identify Rubric Items to Explain Preferences
For each dataset, we construct a rubric
R
R
consisting of natural language criteria that characterize significant differences between pairs of code samples. Each criterion defines a distinct axis where samples diverge. For instance, a rubric item for
robustness and error handling
may capture whether one response incorporates more comprehensive exception handling or more systematically anticipates edge cases than the other. We populate
R
R
using a combination of LLM-generated and human-annotated criteria.
LLM–Generated Rubrics.
We generate rubrics using the procedure described in VibeCheck
[
Dunlap:2025
]
.
We repeatedly sample small batches from the dataset and prompt an LLM to describe the concrete differences between the two responses in each pair.
A subsequent LLM aggregates these results, retaining criteria that recur across batches and merging semantically similar items. The result is a rubric
R
A
R_{A}
of human-interpretable evaluative axes.
Human-Annotated Rubrics.
To incorporate human judgment into rubric construction, we use signals derived from annotator rationales. For each dataset, three engineers review a 30-example overlap set and provide a brief justification explaining why they preferred one response over another. We collect the rationales at the example level, then prompt an LLM to abstract them into general evaluative criteria that apply across examples, yielding a rubric
R
H
R_{H}
.
We combine this with the LLM-generated set
R
A
R_{A}
by passing both through the same aggregation step, which merges them into a final rubric
R
R
.
See Appendix
A.2
for full experimental details.
3.3
Comparing Human and Judge Biases On Rubric Items
To characterize disagreements between humans and LLM judges, we analyze how rubric items
R
R
influence preference decisions. We quantify the contribution of each rubric item by training logistic regression models that predict judge preferences from Section
3.1
using the rubric items introduced in Section
3.2
. To incorporate natural language rubric items into the model, we first map them to numeric features as described below. We then compare the learned coefficients of human and judge-specific models to identify misalignment in how rubric items are weighted.
Preference Modeling.
We describe the process of training a preference model (logistic regression) using rubric items to predict judgment preferences.
For each sample and rubric item, an LLM ranker assigns a score in
{
−
1
,
0
,
1
}
\{-1,0,1\}
indicating whether response
y
A
y_{A}
better satisfies the rubric item (
−
1
-1
),
y
B
y_{B}
does (
1
1
), or both satisfy it equally (
0
). We combine these scores from all samples in the dataset to construct a feature matrix
S
S
, where rows correspond to response pairs and columns correspond to rubric items.
We train separate logistic regression models for humans and each LLM judge using
S
S
as input features. Human judgments define the labels for the human model, while each judge’s judgments define the labels for its corresponding model. This yields a human coefficient vector
β
H
\beta_{H}
and judge-specific vectors
β
J
\beta_{J}
, where
β
(
i
)
\beta^{(i)}
denotes the coefficient for rubric item
R
(
i
)
R^{(i)}
. Differences in these coefficients reflect how humans and LLM judges weigh rubric items using the same input feature representation
S
S
.
Identifying Misalignment.
We quantify misalignment by comparing human and judge coefficients,
β
H
\beta_{H}
and
β
J
\beta_{J}
. For rubric item
R
(
i
)
R^{(i)}
, the signed difference
β
J
(
i
)
−
β
H
(
i
)
\beta_{J}^{(i)}-\beta_{H}^{(i)}
captures relative weighting: positive values indicate that the judge overweights
R
(
i
)
R^{(i)}
relative to humans, while negative values indicate underweighting. A judge–rubric pair is considered significant if the 95% confidence interval for
β
J
(
i
)
\beta_{J}^{(i)}
excludes
β
H
(
i
)
\beta_{H}^{(i)}
, with intervals computed via bootstrap resampling.
See Appendix
A.3
for additional experimental details.
4
Experimental Set-Up
Code and implementation details are available in a public repository.
1
1
1
https://github.com/rShar01/TRACE
4.1
Preference Datasets
We apply
TRACE
to three representative interaction modalities identified in developer-AI taxonomies
[
treude2025developersinteractaitaxonomy
]
: in-file code completion, instructed code editing, and open-ended chat. Table
1
summarizes the differences between these settings.
Table 1
:
Coding modalities differ sharply in context length and output scale.
We summarize three developer interaction settings—code completion, code edits, and chat—each with over 500 samples per dataset.
Natural languages are detected using Lingua
[
stahl2024lingua
]
; programming languages in chat are inferred from code block tags. Edit Distance reports the line-level Levenshtein edit distance between the two candidate responses (after newline normalization; for chat, computed on concatenated code blocks when present).
Code Completion
Code Edit
Chat
# of Natural Languages
23
20
14
# of Programming Languages
39
43
57
Context Length - p50
2,233
3,490
1,013
Context Length - p95
13,984
28,189
12,509
Output Length - p50
108
531
5,491
Output Length - p95
613
3,053
20,156
Lines of Code - p50
78
136
117
Lines of Code - p95
383
744
539
Edit Distance - p50
5
9
123
Edit Distance - p95
20
68
579
Natural Language Instruct
✓
✓
Edits Existing Code
✓
✓
In-IDE
✓
✓
•
Code completions.
We obtain user preferences for code completion from Copilot Arena
[
chi2025copilotarenaplatformcode
]
, which collects pairwise judgments through a VSCode extension. The extension presents two fill-in-the-middle completions from different LLMs, and the user selects the one they prefer to insert into their file. We define
x
x
as the file context in the workspace,
y
A
,
y
B
y_{A},y_{B}
as the two candidate completions, and
w
w
as the label indicating user choice.
•
Instructed code edits.
In instructed code edits, users highlight a region of code and provide instructions describing edits. We source these preferences from EDIT-Bench
[
chi2025editbenchevaluatingllmabilities
]
, where users select their preferred edit from two LLM solutions. In this setting,
x
x
is the user instruction with the highlighted region and file context,
y
A
,
y
B
y_{A},y_{B}
are the two candidate edits, and
w
w
is the user selection.
•
Chat responses.
Developers commonly interact with LLM using chats. We source pairwise preferences from Chatbot Arena
[
chiang2024chatbotarenaopenplatform
]
, where users submit prompts and two LLM assistants generate replies. Since Chatbot Arena is a general-purpose dataset, we filter for 500 code-specific examples (Appendix
B.1
). Here, we define
x
x
as the prompt,
y
A
,
y
B
y_{A},y_{B}
as the two chat responses, and
w
w
is the user selection.
4.2
LLM Judges
We consider 13 different candidate LLM judges from the following categories:
3rd Party Models.
We include widely deployed general-purpose LLMs, including
OpenAI GPT-5
[
singh2025openaigpt5card
]
,
OpenAI GPT-4o
[
ahmad2024gpt4o
]
,
DeepSeek-R1
[
deepseekai2025deepseekr1incentivizingreasoningcapability
]
,
Meta Llama-3.1-70B Instruct
[
grattafiori2024llama3herdmodels
]
, and
Anthropic Claude Sonnet 4
[
claude
]
. We also evaluate smaller variants, such as
OpenAI GPT-5 mini
[
singh2025openaigpt5card
]
and
OpenAI o3-mini (high reasoning effort)
[
openai2025o3o4
]
. These models represent the current frontier of general reasoning systems and serve as baselines for how untuned LLMs perform as judges in code-centric tasks.
Specialized Judge Models.
We also evaluated models designed specifically for judging. Unlike reward models, these systems produce natural language critiques and decisions, but are trained for evaluation rather than generation.
Prometheus 2 (7B)
[
kim2024prometheus
]
is a dedicated evaluator that combines scoring and pairwise comparison objectives.
Atla Selene 1 Mini (Llama-3.1-8B)
[
alexandru2025atlaseleneminigeneral
]
trains on supervised preferences with a DPO-style ranking loss to sharpen separation between preferred and non-preferred outputs.
Atla Selene 1 (Llama-3.3-70B)
scales this design, outperforming frontier models on RewardBench
[
RewardBench
]
.
Skywork Critic (Llama-3.1-70B)
[
skyworkcritic2024
]
generates synthetic critic data during finetuning and ranks among the leading models on RewardBench.
Table 2
:
Automated judges trail human agreement across coding modalities.
We report accuracy (Acc, %) and positional accuracy (
Acc
PC
\text{Acc}_{\text{PC}}
, %) across three modalities.
Acc
PC
\text{Acc}_{\text{PC}}
conditions on valid, positionally consistent decisions (the judge flips its choice when the two candidates are swapped). “Fine-tuned Judge” models are trained for evaluation and output a discrete winner; “3rd Party” models are general-purpose instruction-tuned LLMs used zero-shot as judges; “Reward Models” output scalar preference scores and are inherently order-invariant. Human rows report majority–user agreement on a 30-example overlap set and the absolute-point improvement over the best model.
Code Completion
Instructed Code Edits
Chat-based Coding
Acc
PC
\text{Acc}_{\text{PC}}
↑
\uparrow
Acc
↑
\uparrow
Acc
PC
\text{Acc}_{\text{PC}}
↑
\uparrow
Acc
↑
\uparrow
Acc
PC
\text{Acc}_{\text{PC}}
↑
\uparrow
Acc
↑
\uparrow
Fine-tuned Judge
Atla Selene 1 Mini (Llama-3.1-8B)
59.01
37.67
51.8
31.6
63.76
19.00
Atla Selene 1 (Llama-3.3-70B)
61.99
46.00
54.35
30.4
67.40
24.40
Prometheus 2 (7B)
53.62
29.60
52.21
26.0
58.80
25.40
Skywork Critic (Llama-3.1-70B)
63.28
48.6
56.14
32.00
61.87
51.6
3rd Party
OpenAI GPT-5 mini
62.23
51.40
53.76
41.6
65.60
57.60
OpenAI GPT-5
62.73
54.20
53.40
40.8
62.32
51.6
OpenAI o3-mini (high reasoning)
57.53
46.60
53.20
36.60
66.33
52.00
OpenAI GPT-4o
53.76
38.60
54.06
34.60
63.64
49.00
Anthropic Claude Sonnet 4
68.14
55.60
54.04
38.8
64.53
52.40
DeepSeek-R1
65.71
41.00
52.01
28.6
65.23
45.40
Meta Llama-3.1-70B Instruct
62.03
46.40
51.82
31.80
66.83
27.80
Reward Models
PairRM
50.60
50.60
47.00
47.00
51.80
51.80
GRM-Gemma-2B-rewardmodel-ft
60.80
60.80
45.80
45.80
53.40
53.40
Human
Majority-User Agreement
–
83.3
–
66.7
–
70.0
Annotator Improvement Over Best
–
22.5
–
15.9
–
12.4
Reward Models.
Finally, we evaluate reward models, which output scalar preference scores rather than natural language judgments.
PairRM
[
llm-blender-2023
]
employs a lightweight pairwise comparison architecture at 0.4B parameters.
GRM-Gemma-2B-rewardmodel-ft
[
yang2024regularizing
]
derives from
Gemma-2B
and is fine-tuned on human preference data, reaching state-of-the-art performance for models under 6B parameters on RewardBench.
4.3
Human Baseline
Dataset preference labels typically capture only a single annotator’s judgment and provide a limited view of aggregate human preferences.
We therefore collect additional developer judgments to construct an aggregate human baseline. For each modality, we sampled 30 input pairs (Appendix
B.1
) for additional human annotation. To control for positional effects, we randomized LLM response ordering for
A
A
and
B
B
and did not reveal the original user choice.
Three engineers independently reviewed 30 examples for each dataset, selected the better option, and provided a brief justification for each decision (Appendix
B.2
). We calculate the Majority-User Agreement (MUA) as the average proportion of samples where the majority vote matches the original human label. Additional evaluation metrics and analysis of our human baseline are presented in Appendix
C.3.2
.
5
Results
5.1
How well do LLM judges predict human preferences?
Table
2
reports both overall accuracy and positional accuracy for all models across the three modalities. Performance on established judge benchmarks transfers weakly to our modalities, suggesting that benchmarks do not reliably predict real-world preference alignment in interactive coding settings (Appendix
C.1
).
LLM judges consistently trail human agreement.
Across all three interaction modalities, we observe a gap between model and human judgment, with top judges trailing human agreement by 12-23% on every benchmark and no single model consistently dominating. This gap persists even after controlling for context length (Appendix
C.3.1
). While we expected specialized judges to consistently outperform third-party models, chat-based coding shows the opposite pattern. The largest separation appears in code edits, where the top specialized model outperforms the best third-party model by 5%, suggesting specialization helps in specific settings. Overall, differences among fine-tuned, third-party, and reward models remain small, indicating current judge training strategies do not address the sources of misalignment we observe.
Human annotators agree with original user preference more consistently than judges.
Although human annotators receive the same incomplete context as judges,
they achieve substantially higher agreement and align with the original annotator in the range of 66–84% of cases across datasets. This suggests that, despite imperfect information, humans tend to converge on similar implicit assumptions with the original dataset annotator. We additionally compare model predictions against a majority vote formed from the original annotator and our human annotators (Table
8
). While LLM judges match the majority-vote decision better, they still fall short of human–human agreement, indicating persistent biases in judgment.
Judges exhibit strong position bias.
Across all three datasets, language models exhibit a substantial gap between positional accuracy and overall accuracy. In 3rd-party models, we found that the gap between
Acc
PC
\text{Acc}_{\text{PC}}
and Acc ranges from 8-24%, and even stronger positional bias exists for fine-tuned judge models with gaps ranging from 10-45%. Reward models, by contrast, show no such gap because their pairwise scoring is inherently order-invariant. This gap shows that much of the error arises from sensitivity to input order rather than from disagreement alone.
5.2
How do human and judge biases compare?
Figure 3
:
Judge misalignment reveals distinct rubric biases across interaction modalities.
Each cell shows the signed difference between judge and human preference coefficients (
β
J
(
i
)
−
β
H
(
i
)
\beta_{J}^{(i)}-\beta_{H}^{(i)}
) for selected rubric items within each interaction modality. Positive values (red) indicate that judges overweight a rubric item relative to humans, while negative values (blue) indicate underweighting. Rows show the highest-divergence rubric dimensions within each modality. Bolded values indicate significant judge-human gaps, defined as cases where the 95% confidence interval for
β
J
(
i
)
\beta_{J}^{(i)}
excludes
β
H
(
i
)
\beta_{H}^{(i)}
.
Figure
3
shows rubric misalignment between human preference models and LLM judge preference models across all three modalities. We show the most misaligned rubric items for each modality, see Appendix
C.4
for information about all rubric items.
We discuss insights for each interaction modality:
Table 3:
Example illustrating rubric items in two code completion responses.
In this example, Model 2 explicitly writes the base case, leading to higher
Explicitness and Clarity
under the ranker,
while Model 1 adopts a more minimal control flow, yielding higher
Functional and Logical Alignment
. LLM judges tended to prefer Model 1’s response, while humans selected Model 2. Judge counts include only judges whose preferences were consistent.
Prompt
(paraphrased)
Implement the
stockSpan
method.
Given an array of daily stock prices, compute, for each day, the number of consecutive previous days whose price is less than or equal to the current price.
Model 1
Model 2
Completion
⬇
stockSpan
(
int
[]
stocks
,
int
[]
span
)
{
Stack
<
Integer
>
stack
=
new
Stack
<>();
for
(
int
i
=
0;
i
<
stocks
.
length
;
i
++)
{
...
}
}
⬇
stockSpan
(
int
[]
stocks
,
int
[]
span
)
{
Stack
<
Integer
>
stack
=
new
Stack
<>();
stack
.
push
(0);
span
[0]
=
1;
for
(
int
i
=
1;
i
<
stocks
.
length
;
i
++)
{
...
}
}
Explicitness
and Clarity
↓
\boldsymbol{\downarrow}
Omits initialization for the base case, making first iteration logic implicit.
↑
\boldsymbol{\uparrow}
States the base case directly via
span
[0]
=
1
and starts loop at
i
=
1
.
Functional and
Logical Alignment
↑
\boldsymbol{\uparrow}
Loop covers all indices without special casing.
↓
\boldsymbol{\downarrow}
Adds base case handling and changes loop start, straying from the minimal functional pattern.
Judge Preference
5 out of 8
3 out of 8
Human Preference
–
Selected
In code completion settings, judges overvalue the importance of functional code.
Judges systematically underweight
Explicitness and Clarity
and overweight
Functional and Logical Alignment
. A plausible explanation is that completion judging emphasizes properties that are directly verifiable from the provided code block, such as logical consistency. By contrast, dimensions like clarity depend on longer-term context, such as team conventions, which users implicitly account for when deciding whether to insert a completion into their codebase. We provide a concrete example of this misalignment in Table
5.2
.
In chat contexts, judges undervalue the importance of domain-aware solutions.
In chat, the dominant gaps shift toward response framing. Judges overweight
Code Explanation and Clarity
while humans penalize it, and underweight
Domain-Specific Detail and Technical Creativity
despite humans weighing it positively. This suggests human users prioritize responses that demonstrate domain awareness and adaptation to their specific problem without excessive explanation. Chat responses provide richer natural language context than code blocks, but judges still struggle to assess whether a solution considers domain-specific details.
In edits, judges undervalue the importance of clear, unambiguous code.
The same underweighting of
Explicitness and Clarity
exists in edits, while other statistically detectable gaps are not as pronounced, such as
Data and Type Management
and
Conformance to Standards
. This pattern suggests that judges treat edits primarily as constraint satisfaction tasks, focusing on whether the requested change was applied correctly and minimally. Human users, however, appear to treat edits as opportunities to improve code quality, valuing clearer structure and improved readability.
5.3
How do rubric items map to code quality criteria?
Table 4:
A majority of generated rubric items align with existing software engineering criteria.
The orange-highlighted metrics align with established code quality frameworks
[
10.1145/2999541.2999555
,
Nilson2019DoIS
,
AlGhuwairi2023VisualizingSR
,
Messer2024HowCA
,
Messer2023AutomatedGA
,
Bishop2024EvaluatingSC
,
Hariharan2025SemanticME
,
Keuning2023ASM
,
Ernst2017WhatTF
,
Tablan2025SmarterTC
,
Jiang2024FromET
,
Rosenberg2002SoftwareQM
,
Curtis2022MeasuringTS
]
, while the blue-highlighted metrics extend beyond traditional software engineering taxonomies
[
Messer2023AutomatedGA
,
Messer2024HowCA
,
Menolli2025EducationalIF
,
Rai2022ARO
,
Bishop2024EvaluatingSC
,
Hariharan2025SemanticME
,
Ernst2017WhatTF
]
, capturing additional dimensions not typically represented in evaluation criteria. Full rubric groupings appear in Table
13
.
Shared Across All
Code Edit and Chat
Code Completion and Chat
Code Completion
Code Edit
Chat
User-Centeredness
Instruction Following
Creativity / Innovation
Explanatory / Ethical Awareness
Data / Type Management
Domain-Specific Detail
Conciseness
Standards / Conventions
Completeness
Syntax / Structural Consistency
Correctness / Precision
Presentation / Formatting
Efficiency
Modularity / Structure
Error Handling / Robustness
Clarity / Explicitness
After generating rubrics independently for each interaction modality (full rubrics in Appendix
C.5
), we identify semantically similar rubric items across interaction types and cluster them into broader themes (Table
4
). We examine how these themes map onto established software engineering criteria and where they extend beyond existing frameworks.
Judge misalignment persists even in established code quality criteria.
As shown in Table
4
, 11 of 16 themes correspond directly to established software engineering metrics.
For example, syntax validity is foundational to existing code taxonomies
[
Ernst2017WhatTF
]
, formatting and structural clarity appear in both professional and educational rubrics
[
Keuning2023ASM
,
10.1145/2999541.2999555
]
, and conciseness relates to complexity-based measures such as cyclomatic complexity while also capturing notions of minimalism and elegance
[
Nilson2019DoIS
,
AlGhuwairi2023VisualizingSR
,
Messer2024HowCA
]
.
A smaller set of themes has more limited explicit coverage in traditional code quality frameworks, although partial connections exist. Further discussion of these connections are discussed in Appendix
C.5
.
Overall, the rubric items generated by our framework reflect the multidimensional view of code quality emphasized in prior literature. Examining model coefficients (Section
5.2
) across these themes shows that 6 of the 11 rubric themes aligned with established software engineering criteria still exhibit significant judge-human misalignment. Although many judge models are trained to predict human preferences
[
ouyang2022traininglanguagemodelsfollow
]
, they remain misaligned with human judgments along well-established dimensions of software engineering, indicating that substantial alignment gaps persist in these settings.
6
Conclusions, Limitations, and Future Work
We presented
TRACE
, a framework for evaluating LLM judges in realistic code interaction settings and automatically extracting rubric items that explain how LLM judge preference differs from human preference. Across chat-based programming, IDE autocompletion, and instructed code editing, the strongest judges among the evaluated models still underperformed aggregate human annotators. Beyond overall accuracy,
TRACE
revealed several sources of judge misalignment on rubric items across all modalities. These findings suggest that improving automated code evaluation will require rubric-aware calibration or targeted judge training.
6.1
Limitations and Future Work
Our framework has several limitations. First,
TRACE
uses a linear model to estimate rubric coefficients for interpretability, though nonlinear models may better capture interactions between rubric dimensions. Future work should test whether more expressive models, paired with explainability methods such as SHAP, improve fidelity. Second,
TRACE
identifies rubric-level misalignment but does not provide a way to directly align judges using the rubrics. A simple alignment strategy is to directly inject the misaligned rubrics into the judge prompt, but this did not improve accuracy or reduce invalid outputs (Appendix
C.2
). More promising next steps are (i) rubric-conditioned objectives that train judges to predict per-rubric scores and then aggregate them into a decision, (ii) calibration layers that learn rubric-specific reweighting to align judge signals with human coefficients, and (iii) targeted data selection on examples that expose rubric-critical failures.
Acknowledgments
We thank Bogdan Vasilescu and members of the Sage Lab for their helpful feedback.
This work was supported in part by the National Science Foundation grants IIS1705121, IIS1838017, IIS2046613, IIS2112471, and funding from Datadog. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of any of these funding agencies.
References
Appendix A
Methodology
A.1
Predicting Human Preference
A.1.1
Prompt Templates
These templates define the LLM judge prompts used across our experiments to compare two responses and return a structured preference.
Code Completion Prompt.
system: |
  Please act as an impartial judge and evaluate the quality of the
  responses provided by two AI assistants to the coding context
  displayed below.

  You should choose the answer that fits the prefix AND suffix
  contexts within the XML tags. Your evaluation should consider
  factors such as relevance, accuracy, and style.

  Begin your evaluation by comparing the two responses and provide
  a short explanation. Avoid any position biases and ensure that
  the order in which the responses were presented does not
  influence your decision. Do not allow the length of the
  responses to influence your evaluation. Do not favor certain
  names of the assistants. Be as objective as possible.

  After providing your explanation, output your final verdict by
  strictlyfollowing this format within <answer> </answer> XML tags.

  Use the answer "[[A]]" if assistant A is better, "[[B]]" if
  assistant B is better.

query: |
  <prefix>
  {prefix}
  </prefix>

  <suffix>
  {suffix}
  </suffix>

  <assistant_a_response>
  {answer_a}
  </assistant_a_response>

  <assistant_b_response>
  {answer_b}
  </assistant_b_response>
Instructed Code Edit Prompt.
system: |
  I am a machine learning scientist studying responses given by
  LLM coding assistants. The models are tasked with editing user
  code to follow user instructions.

  Please act as an impartial judge and evaluate the quality of
  the responses provided by the two AI assistants. The responses
  appear below within XML tags labelled "Assistant A" and
  "Assistant B".

  Begin your evaluation by comparing the two responses and
  provide a short explanation. Avoid any position biases and
  ensure that the order in which the responses were presented
  does not influence your decision. Do not allow the length of
  the responses to influence your evaluation. Do not favor
  certain names of the assistants. Be as objective as possible.

  After providing your explanation, output your final verdict
  by strictly following this format within <answer> </answer>
  XML tags.

  Use the answer "[[A]]" if assistant A is better, "[[B]]" if
  assistant B is better.

query: |
  This is the prefix of the coding file:
  {prefix}

  This is the suffix of the file:
  {suffix}

  This is the code selected by the user to rewrite:
  {code_to_edit}

  The user has given the instructions:
  {user_input}

  Below are the assistant-generated edits to the code:

  <assistant_a_response>
  {answer_a}
  </assistant_a_response>

  <assistant_b_response>
  {answer_b}
  </assistant_b_response>
Chat-baesd Interface Prompt.
system: |
  Please act as an impartial judge and evaluate the quality of
  the responses provided by two AI assistants to a user prompt.

  The prompt appears below within the XML tag <prompt>, and
  the two responses appear within tags labelled "Assistant A"
  and "Assistant B".

  Your evaluation should consider factors such as relevance,
  accuracy, and style. Begin by comparing the two responses
  and provide a short explanation.
  Avoid any position biases and ensure the order of
  presentation does not influence your decision. Do not allow
  response length to influence your evaluation. Do not favor
  certain assistant names. Be as objective as possible.

  After providing your explanation, output your final verdict
  by strictly following this format within <answer> </answer>
  XML tags.

  Use the answer "[[A]]" if assistant A is better, "[[B]]" if
  assistant B is better.

query: |
  <prompt>
  {user_instruction}
  </prompt>

  <assistant_a_response>
  {answer_a}
  </assistant_a_response>

  <assistant_b_response>
  {answer_b}
  </assistant_b_response>
A.1.2
Reward Models
Reward models assign scalar scores to LLM outputs to indicate their alignment with human preferences. To run inference for a reward model
J
J
, we evaluate the input
x
x
paired with each candidate response,
(
x
,
y
A
)
(x,y_{A})
and
(
x
,
y
B
)
(x,y_{B})
, independently, yielding scores
s
A
s_{A}
and
s
B
s_{B}
. The model preference is defined as
J
​
(
x
,
y
A
,
y
B
)
=
−
1
J(x,y_{A},y_{B})=-1
when
s
A
<
s
B
s_{A}<s_{B}
, and
1
1
otherwise. Many modern reward models adapt this framework (see Section
4.2
for examples).
A.2
Discovering Evaluative Criteria
Configuration.
In our pipeline,
GPT-4o
is the rubric proposer. For efficiency, we process thirty samples in batches of five during each generation pass. We repeat this step three times, for a total of ninety samples, to produce a more complete rubric set.
A.2.1
Prompt Templates
Proposer Prompt.
This prompt adapts the original VibeCheck proposer template to generate evaluative criteria, with modifications to produce more specific and unique rubric items.
You are a machine learning researcher analyzing two large language
models (LLMs) by comparing how their responses differ to the same
set of questions. Your goal is to identify unique, interpretable
behavioral dimensions ("axes of variation") that capture subtle or
surprising differences between the models.

Here are the questions and responses:
{combined_responses}

For each axis, describe what makes one model’s responses higher
and the other’s lower on that dimension. Focus on differences
that reveal deeper behavioral tendencies rather than surface
traits.

Format your output as a bulleted list, with each axis on a new
line starting with a dash (-) or asterisk (*). Each axis should
follow this format:

- {axis}: High → {description of high end} | Low → {description
    of low end}

Example:
- Self-consistency: High → Responses maintain consistent
reasoning throughout | Low → Reasoning may shift or contradict
earlier statements

Guidelines:
- Avoid obvious or generic dimensions such as "clarity,"
    "conciseness," or "formality."
- Look for behavioral nuances from reasoning patterns, goal
    orientation, implicit assumptions, moral framing, creativity
    style, uncertainty handling, or tone of confidence.
- Axes may mix abstract and domain-specific aspects.
- Each axis must be something a human could use to categorize
    which model response is higher or lower.
- Do not add explanations, prefaces, or summaries.
- If no substantive differences exist, output only "No
    differences found."
Aggregation Prompt.
This prompt adapts the VibeCheck reduction template to aggregate rubric items, prioritizing unique, task-specific dimensions over very general criteria.
The following are axes of variation for comparing two model outputs.
Each axisincludes a name and a description of what makes an output
high or low on that dimension. Some axes may be redundant, misnamed,
or overlap with others. Your task is to cluster and reduce these
axes into a minimal set of parent axes that are as distinct and
non-overlapping as possible, while preserving the specificity
and uniqueness of the original axes. Do not over-merge genuinely
distinct properties.

For each parent axis you create:
- Ensure the high and low descriptions faithfully subsume the axes
    they replace, while retaining distinctive properties rather
    than over-generalizing.
- If an axis is truly unique or nuanced, keep it as its own parent
    axis rather than forcing a merge.
- Parent axes must be mutually exclusive and enable a human to
    reliably and uniquely categorize model outputs along each
    dimension.
- If an axis is domain- or task-specific (e.g., coding), reflect
    this specificity in the axis name.

Here are the axes of variation (each formatted as
{axis name}: High: {high description} Low: {low description}):

{differences}

Cluster and reduce these axes into a minimal, clear set of parent
axes, retaining uniqueness where present. Each parent axis should
include a name and a concise (<20 words) description that preserves
any domain-specific or distinctive properties in the original.

Format your output as a bulleted list, one axis per line, using:

- {axis}: High → {description of high end} | Low → {description
of low end}
Annotator-Comment Proposer Prompt.
This prompt identifies evaluative criteria from annotator comments, discovering criteria that reflect how humans differentiate between two candidate responses.
You are a machine learning researcher analyzing annotator comments
to surface unique, interpretable behavioral dimensions ("axes of
variation") that capture what annotators notice when preferring one
answer over another. Work only from the comments -- do not assume
anything about the original questions or answers.

Here are the comments to analyze:
{comments}

For each axis, describe what makes a response higher versus lower
on that dimension. Focus on differences that reveal deeper
behavioral tendencies rather than surface traits.

Format your output as a bulleted list, with each axis on a new line
starting with a dash (-) or asterisk (*). Each axis should follow
this format:

- {axis}: High → {description of high end} | Low → {description
of low end}

Guidelines:
- Derive axes only from the themes present in the comments (e.g.,
    syntax validity, conciseness, unnecessary extras, instruction
    alignment).
- Look for interpretable, discriminative properties (reasoning
    patterns, goal orientation, adherence to constraints) rather
    than generic "good/bad."
- Keep axes human-usable; a reviewer should be able to place an
    answer as higher or lower on the axis from the comment.
- Do not mention specific questions, models, or options -- focus
    on underlying properties.
- If no substantive differences are present, output only "No
    differences found."
Rubric-Injection Judge Prompt (Ablation).
In our rubric-injection ablation (Appendix
C.2
), we used the following prompt template for judge inference. In the Baseline condition, we removed the rubric block (the “human preference rubrics” section). In the “+All” and “+Top-1” conditions, we instantiated
{rubrics}
with the full dataset-specific rubric list or a single rubric item, respectively.
system: |
  Please act as an impartial judge and evaluate the quality of the
  responses provided by two AI assistants to the coding context
  displayed below. You should choose the answer that fits the
  prefix AND suffix contexts within the XML tags. Your evaluation
  should consider factors such as the relevance, accuracy, and
  style of the responses. Begin your evaluation by comparing the
  two responses and provide a short explanation. Avoid any
  position biases and ensure that the order in which the responses
  were presented does not influence your decision. Do not allow
  the length of the responses to influence your evaluation. Do
  not favor certain names of the assistants. Be as objective
  as possible.

  Also consider the following human preference rubrics as additional
  judging axes. Favor the "High" side of each axis unless it
  conflicts with the user instruction.
  {rubrics}

  After providing your explanation, output your final verdict by
  strictly following this format within <answer> </answer> XML
  tags. Use the answer "[[A]]" if assistant A is better, "[[B]]"
  if assistant B is better.
query: |
  <prefix>
  {prefix}
  </prefix>

  <suffix>
  {suffix}
  </suffix>

  <assistant A’s response>
  {answer_a}
  </assistant A’s response>

  <assistant B’s response>
  {answer_b}
  </assistant B’s response>
A.3
Diagnosing Judge Misalignment
A.3.1
Rubric Ranking
Configuration.
In our pipeline,
GPT-5.1
serves as the rubric ranker. For efficiency, we evaluate five rubric axes per sample in a single scoring pass. We retry malformed outputs up to three times and assign a neutral score when a value remains missing. We use the VibeCheck ranker prompt template for all ranking.
Positional Bias.
To control for positional bias, we evaluate every pair twice, once in the original order and once with the responses swapped. We retain rubric scores only when the ranker is positionally consistent, meaning the preference flips under swapping. For inconsistent cases, we set the corresponding rubric score to neutral.
Appendix B
Experimental Setup
B.1
Dataset Filtering and Normalization
We apply dataset-specific preprocessing to ensure that each instance corresponds to a well-formed pairwise preference example of the form
(
x
,
y
A
,
y
B
,
w
)
(x,y_{A},y_{B},w)
with sufficient context to evaluate the responses. Across all datasets, we (i) require an explicit human preference between two candidates (no ties), (ii) drop rows with malformed serialization or missing required fields, and (iii) remove degenerate pairs where the two candidates are identical when applicable.
We encode preferences using
w
∈
{
−
1
,
1
}
w\in\{-1,1\}
, where
w
=
1
w=1
indicates that the user preferred
y
A
y_{A}
and
w
=
−
1
w=-1
indicates that the user preferred
y
B
y_{B}
.
B.1.1
Copilot Arena (Code Completion)
Copilot Arena logs come from a VSCode extension that presents two fill-in-the-middle code completions for the same cursor context. Each record includes the surrounding code context (preceding and following text) and two candidate completions. We parse the serialized completion metadata and retain only examples with a valid user preference between the two candidates. In our implementation, we keep only records where the user accepted the
second
of the two presented completions, which mitigates the possibility that users accept the first completion with minimal comparison and never meaningfully inspect the alternative. Under this filtering, the preferred completion always corresponds to the second candidate, so we set
w
=
−
1
w=-1
. We additionally require that the completion metadata contains the preceding code context.
B.1.2
EDIT-Bench (Code Edits)
EDIT-Bench examples consist of a natural-language edit instruction, a code span to edit, and file context (preceding and following text), paired with two candidate edits. The raw CSV stores the candidate data in a string-serialized field; we safely parse this field and drop rows that fail to deserialize. We then restrict to research-consented examples with a binary preference label over the two candidates. We keep only rows that contain the required context (instruction, code span, and file context) and extract both candidate edits to form
(
x
,
y
A
,
y
B
,
w
)
(x,y_{A},y_{B},w)
. To avoid trivial comparisons, we remove pairs where the two candidate edits are identical after trimming leading/trailing whitespace. The winner label
w
w
is taken from the recorded preference (first candidate preferred
→
w
=
1
\rightarrow w=1
; second candidate preferred
→
w
=
−
1
\rightarrow w=-1
).
B.1.3
LMArena (Chat)
For chat-based assistance, we use the
lmarena-ai/arena-human-preference-140k
dataset. Because LMArena covers a wide range of domains, we apply additional constraints to isolate code-centric, comparable examples. We retain only instances annotated as code-related with a decisive preference for one of the two candidates, and we restrict to the canonical presentation order used for evaluation. To reduce variation due to conversational history, we further require single-turn conversations for both candidates (exactly one user message and one assistant response).
To focus on developer-like completion/edit interactions, we additionally filter to prompts that match an
edit-like
heuristic (e.g., containing common edit/repair verbs or placeholder markers) while excluding prompts that are primarily explanatory (e.g., definition or “explain” requests) or unrelated to code editing (e.g., image-generation requests).
Finally, we require that
both
assistant responses contain fenced code blocks (triple backticks) with language tags drawn from a curated set of programming-language identifiers, and that the two responses share at least one such language tag. We also require code-like tokens within the fenced regions to remove prose-only fences. Together, these constraints remove comparisons where candidates respond in different programming languages or where one response is not substantively code.
To construct an LMArena subset that is comparable to the completion and edit datasets, we further restrict the filtered set to a list of manually retained question identifiers. This list is created by three annotators via inspection of the prompt–response traces, retaining only examples that match our intended coding interaction and contain sufficient context for a meaningful preference judgment.
B.2
Human Baseline
(a)
Code Completion portal view.
(b)
Chat portal view.
Figure 4:
Reviewer portal used for the human baseline study.
The interface shows the task context and two candidate answers (Option 1/Option 2); the mapping from underlying candidates to displayed options is randomized to mitigate positional effects.
Portal workflow.
Annotators interact with a lightweight web portal that exposes a “next question / submit response” loop. For each item, the portal renders the available task context (instruction, optional code-to-edit span, and surrounding file context) alongside two candidate answers displayed as Option 1 / Option 2. To mitigate positional effects, the mapping from the underlying candidates (
A
/
B
A/B
) to the displayed options is randomized per question using a fixed seed, and the global question order is deterministically shuffled so that every annotator sees the same 30-question batch.
Question selection.
For question sets, we draw a fixed 30-question batch using a deterministic random shuffle with a fixed seed, so that all annotators review the same questions while avoiding systematic selection effects. For LMArena, the random sample is drawn after applying the manual curation described in Appendix
B.1
.
Annotation protocol.
For every question, annotators select the better option and provide a brief free-form justification (required for every submission). The interface does not display the original user-selected answer. For completion and edit tasks, the portal optionally highlights differences between the two candidates to support fine-grained comparisons; for chat responses, answers are rendered as markdown and the portal provides an optional translation-to-English toggle to reduce language barriers.
Logging and aggregation.
Each submission records the question identifier, the randomized presentation order, the selected option mapped back to
A
/
B
A/B
, the selected answer text, the annotator comment, and a timestamp. To enable per-reviewer aggregation without storing personal identifiers, the backend writes results under a pseudonymous reviewer id obtained by hashing the local username, and it rejects duplicate submissions for the same reviewer and question. For analysis, we combine the original user label with three additional annotator labels and use the resulting majority vote as a human reference (ties broken in favor of the original user). We report majority–model alignment (MMA), defined as the fraction of examples where a model’s prediction matches this aggregated label, in Table
8
.
Appendix C
Results
C.1
Comparison to other benchmarks
Across models, performance on our modalities aligns only weakly with established judge benchmarks (Table
5
). Strong results on external judge tasks do not necessarily carry over.
Skywork Critic (Llama-3.1-70B)
leads on RewardBench yet ranks only mid-range on code completion and code edits.
NVIDIA Qwen3-Nemotron-32B-GenRM-Principle
tops JudgeBench (Coding) but shows uneven performance across interaction modalities.
Table 5:
External judge benchmarks correlate weakly with completion/edit accuracy.
We report model accuracy (Acc, %) on our three interaction modalities—IDE code completion, instructed code edits, and chat-based coding—alongside each model’s published score (%, higher is better) on established judge benchmarks (RewardBench, RewardBench 2, and JudgeBench-Coding). Dashes indicate unavailable results. Models are abbreviated for space.
Interaction Modalities
External Benchmarks
Model
CodeCompletion
CodeEdit
Chat
RewardBench
RewardBench 2
JudgeBench (Coding)
Skywork Critic
48.6
32.0
51.6
93.3
–
47.6
GPT-5 mini
45.9
32.0
32.4
80.1
58.0
45.2
GPT-4o
38.6
34.6
49.0
86.7
64.9
59.5
Gemini 2.5 Pro
57.8
38.0
56.4
–
79.5
–
Claude Sonnet 4
55.6
38.8
52.4
–
71.2
–
Llama-3.1-70B
46.4
31.8
27.8
84.0
–
–
GRM-Gemma-2B
60.8
45.8
53.4
–
59.7
54.8
Nemotron-32B
56.2
50.8
57.4
–
–
90.5
C.2
Rubric-Injection Ablation
Table
6
reports the rubric-injection ablation, where rubric items are explicitly added to the model prompt to increase judge accuracy.
Table 6:
Rubric injection does not consistently improve judging and can increase invalid outputs.
Each entry reports positional accuracy
Acc
PC
\text{Acc}_{\text{PC}}
(in %) and invalid rate (in %) as
Acc
PC
\text{Acc}_{\text{PC}}
(Inv). “+All” appends the full dataset-specific rubric list, and “+Top-1” appends only the single most misaligned rubric item for that model. Metrics are computed on the aligned subset of prompts available for each model/variant (up to 500 per dataset).
Code Completion
Code Edit
Model
Baseline
+All
+Top-1
Baseline
+All
+Top-1
Fine-tuned Judge
Atla Selene 1 Mini (Llama-3.1-8B)
56.7 (35.4)
61.4 (35.8)
61.1 (36.2)
51.8 (39.0)
54.7 (46.6)
52.8 (47.0)
Atla Selene 1 (Llama-3.3-70B)
62.0 (25.8)
61.2 (27.4)
60.2 (28.6)
54.4 (33.4)
54.5 (37.2)
54.2 (38.4)
Prometheus 2 (7B)
53.6 (44.8)
61.6 (57.8)
61.6 (57.8)
52.2 (50.2)
53.8 (76.6)
53.8 (76.6)
3rd Party
OpenAI GPT-4o mini
59.3 (22.8)
59.1 (20.8)
–
52.4 (36.6)
52.3 (38.0)
–
OpenAI GPT-5 mini
62.2 (17.4)
63.8 (14.8)
65.3 (16.4)
53.8 (28.2)
54.4 (27.6)
53.6 (28.4)
Meta Llama-3.1-70B Instruct
62.0 (25.2)
62.2 (30.2)
61.7 (30.0)
51.8 (34.2)
55.4 (44.0)
54.8 (43.4)
Reward Models
PairRM
50.6 (0.0)
51.2 (0.0)
51.2 (0.0)
47.0 (0.0)
48.4 (0.0)
48.4 (0.0)
NVIDIA Qwen3-Nemotron-32B-GenRM-Principle
56.2 (0.0)
46.6 (0.0)
–
50.8 (0.0)
45.4 (0.0)
–
GRM-Gemma-2B-rewardmodel-ft
60.8 (0.0)
61.4 (0.0)
61.4 (0.0)
45.8 (0.0)
48.2 (0.0)
48.0 (0.0)
C.3
Evaluating LLM Judges
C.3.1
Controlling for Context Length
Table
7
shows a consistent gap between full-prompt and truncated-prompt performance across all three benchmarks. Models achieve higher accuracy when the entire prompt fits within the model’s context window. Performance degrades when examples exceed that window and the prompt must be truncated. The decline is often substantial for models with shorter context windows, while models with larger context windows exhibit smaller drops. Regardless, even when we restrict evaluation to examples whose full prompt fits within the model’s context window, these models largely do not achieve accuracy comparable to the top model previously reported in each benchmark.
Table 7:
Judging accuracy drops when prompts exceed a model’s context window.
The full-prompt accuracy (
Acc
F
\text{Acc}_{\text{F}}
) is computed on examples whose prompt fits within the model’s context length. The truncated-prompt accuracy (
Acc
T
\text{Acc}_{\text{T}}
) is computed on examples that require truncation. Models are abbreviated for space.
Code Completion
Code Edit
Chat
Context Length
Acc
F
\text{Acc}_{\text{F}}
↑
\uparrow
Acc
T
\text{Acc}_{\text{T}}
↑
\uparrow
Acc
F
\text{Acc}_{\text{F}}
↑
\uparrow
Acc
T
\text{Acc}_{\text{T}}
↑
\uparrow
Acc
F
\text{Acc}_{\text{F}}
↑
\uparrow
Acc
T
\text{Acc}_{\text{T}}
↑
\uparrow
Fine-tuned Judge
Atla Selene 1 Mini
2048
42.22
19.01
36.17
25.69
29.70
16.29
Atla Selene 1
4096
47.28
18.18
36.64
34.58
33.33
22.11
Prometheus 2 (7B)
2048
33.53
21.25
28.28
23.83
37.04
23.99
Skywork Critic
4096
49.37
31.82
33.84
25.23
52.09
51.05
Reward Models
PairRM
2048
53.77
48.5
50.00
45.76
52.63
50.7
GRM-Gemma-2B
3000
54.63
100.0
47.2
42.86
46.15
53.80
Top Model
−
60.80
60.80
47.00
47.00
57.60
57.60
C.3.2
Model Agreement with Human Majority
For each sample in the dataset, we let
m
m
be the majority vote of the three annotators. The Majority–User Agreement (MUA) is the fraction of samples where
m
m
matches the original preference label
w
w
.
To provide an additional human reference beyond a single user label, we evaluate each judge on the 30-example overlap set annotated by three additional engineers and aggregate labels by majority vote with the original label as a tie-breaker. We report majority–model alignment (MMA) as both positional accuracy (conditioned on valid, positionally consistent decisions) and overall accuracy over all 30 items (Table
8
). Across datasets, MMA remains moderate and varies substantially by interaction modality, suggesting that disagreement with human judgment persists even when the target label is stabilized by aggregation.
Table 8:
Model agreement remains below human consensus even with aggregated labels.
We compute majority–model alignment on a 30-example overlap set labeled by the original user plus three additional annotators (ties broken in favor of the original user). The positional accuracy (
Acc
PC
\text{Acc}_{\text{PC}}
) conditions on valid, positionally consistent decisions; the overall accuracy (Acc) is over all 30 items.
Code Completion
Code Edit
Chat
Acc
PC
\text{Acc}_{\text{PC}}
↑
\uparrow
Acc
↑
\uparrow
Acc
PC
\text{Acc}_{\text{PC}}
↑
\uparrow
Acc
↑
\uparrow
Acc
PC
\text{Acc}_{\text{PC}}
↑
\uparrow
Acc
↑
\uparrow
Fine-tuned Judge
Atla Selene 1 Mini (Llama-3.1-8B)
66.67
33.33
36.36
26.67
60.00
20.00
Atla Selene 1 (Llama-3.3-70B)
68.00
56.67
27.78
16.67
70.00
23.33
Prometheus 2 (7B)
65.22
50.00
23.53
13.33
41.67
16.67
Skywork Critic (Llama-3.1-70B)
65.38
56.67
35.00
23.33
55.56
50.00
3rd Party
OpenAI GPT-5 mini
66.67
53.33
40.00
33.33
59.26
53.33
OpenAI GPT-5
66.67
60.00
52.00
43.33
57.14
53.33
OpenAI o3-mini
60.00
50.00
45.83
36.67
56.00
46.67
OpenAI GPT-4o
68.00
56.67
23.81
16.67
57.14
40.00
Anthropic Claude Sonnet 4
71.43
50.00
40.00
33.33
60.00
50.00
DeepSeek-R1
68.75
36.67
53.33
26.67
58.33
46.67
Meta Llama-3.1-70B Instruct
67.86
63.33
23.53
13.33
45.45
16.67
Reward Models
PairRM
50.00
50.00
53.33
53.33
53.33
53.33
GRM-Gemma-2B-rewardmodel-ft
46.67
46.67
26.67
26.67
60.00
60.00
C.4
Identifying Judge Misalignment
Figures
5
,
6
, and
7
analyze the signed coefficient difference
β
J
(
i
)
−
β
H
(
i
)
\beta_{J}^{(i)}-\beta_{H}^{(i)}
for each judge and rubric item
R
(
i
)
R^{(i)}
across the code completion, code edit, and chat modalities respectively. We bold significant judge-human gaps, defined when the 95% confidence interval for
β
J
(
i
)
\beta_{J}^{(i)}
excludes
β
H
(
i
)
\beta_{H}^{(i)}
.
C.4.1
Statistically Significant Judge–Rubric Gaps
Table
9
lists all judge–rubric pairs where the judge’s 95% CI for
β
J
(
i
)
\beta_{J}^{(i)}
excludes
β
H
(
i
)
\beta_{H}^{(i)}
, indicating a statistically detectable difference in how that judge weights the rubric item relative to humans.
Table 9:
Statistically detectable gaps cluster in a small number of rubric dimensions.
A judge–rubric pair is significant if the judge’s 95% CI for
β
J
(
i
)
\beta_{J}^{(i)}
excludes
β
H
(
i
)
\beta_{H}^{(i)}
. The direction column indicates whether the judge overweights (
↑
\uparrow
) or underweights (
↓
\downarrow
) the rubric item relative to humans.
Judge
Rubric
Dir
Δ
=
β
J
−
β
H
\Delta=\beta_{J}-\beta_{H}
Code Completion
Prometheus 2 (7B)
Explicitness and Clarity
↓
\downarrow
-0.924
GRM-Gemma-2B-rewardmodel-ft
Explicitness and Clarity
↓
\downarrow
-0.721
GRM-Gemma-2B-rewardmodel-ft
Functional and Logical Alignment
↑
\uparrow
+0.691
PairRM
Functional and Logical Alignment
↑
\uparrow
+0.669
Skywork Critic (Llama-3.1-70B)
Explicitness and Clarity
↓
\downarrow
-0.605
OpenAI GPT-5 mini
Explicitness and Clarity
↓
\downarrow
-0.578
OpenAI GPT-5
Functional and Logical Alignment
↑
\uparrow
+0.574
OpenAI GPT-5 mini
Functional and Logical Alignment
↑
\uparrow
+0.520
OpenAI GPT-5
Explicitness and Clarity
↓
\downarrow
-0.500
Atla Selene 1 (Llama-3.3-70B)
Syntax and Structural Consistency
↑
\uparrow
+0.482
GRM-Gemma-2B-rewardmodel-ft
Flexibility and Generality
↑
\uparrow
+0.414
OpenAI o3-mini (high reasoning effort)
Flexibility and Generality
↑
\uparrow
+0.374
PairRM
Engagement and User Interaction
↑
\uparrow
+0.331
OpenAI o3-mini (high reasoning effort)
Explanatory and Ethical Awareness
↓
\downarrow
-0.317
OpenAI GPT-5 mini
Engagement and User Interaction
↑
\uparrow
+0.312
Atla Selene 1 (Llama-3.3-70B)
Creativity and Innovation
↓
\downarrow
-0.291
Code Edit
DeepSeek-R1
Explicitness and Clarity
↓
\downarrow
-0.534
Skywork Critic (Llama-3.1-70B)
Explicitness and Clarity
↑
\uparrow
+0.489
Meta Llama-3.1-70B Instruct
Explicitness and Clarity
↓
\downarrow
-0.431
GRM-Gemma-2B-rewardmodel-ft
Data and Type Management
↑
\uparrow
+0.379
OpenAI GPT-4o
Conformance to Standards
↑
\uparrow
+0.364
Skywork Critic (Llama-3.1-70B)
Modularity and Abstraction
↑
\uparrow
+0.347
Chat
Prometheus 2 (7B)
Completeness and Precision
↑
\uparrow
+0.939
OpenAI o3-mini (high reasoning effort)
Domain-Specific Detail and Technical Creativity
↓
\downarrow
-0.740
Prometheus 2 (7B)
Domain-Specific Detail and Technical Creativity
↓
\downarrow
-0.696
OpenAI GPT-5 mini
Domain-Specific Detail and Technical Creativity
↓
\downarrow
-0.625
Meta Llama-3.1-70B Instruct
Completeness and Precision
↓
\downarrow
-0.606
OpenAI GPT-4o
Error-Free and Clarity of Presentation
↑
\uparrow
+0.410
OpenAI GPT-4o
Completeness and Precision
↓
\downarrow
-0.394
OpenAI GPT-5
Code Explanation and Clarity
↑
\uparrow
+0.355
OpenAI o3-mini (high reasoning effort)
Code Explanation and Clarity
↑
\uparrow
+0.328
OpenAI GPT-4o
Code Explanation and Clarity
↑
\uparrow
+0.303
Skywork Critic (Llama-3.1-70B)
Code Explanation and Clarity
↑
\uparrow
+0.280
Anthropic Claude Sonnet 4
User Interaction and Feedback Responsiveness
↑
\uparrow
+0.259
Skywork Critic (Llama-3.1-70B)
Modularity and Code Structure
↑
\uparrow
+0.237
Figure 5:
Code completion alignment across all judges and rubrics.
Figure 6:
Code edit alignment across all judges and rubrics.
Figure 7:
Chat completion alignment across all judges and rubrics.
C.5
Discovering Evaluative Criteria
Tables
10
,
11
, and
12
list the evaluative criteria produced by our rubric construction pipeline for the code completion, code edit, and chat modalities respectively. For each dataset, we report the final set of rubric axes, along with short descriptions of the upper and lower ends of each axis. We also include minimal code examples for each axis to make these rubrics more concrete. Table
13
summarizes how these rubric axes align across datasets.
Code quality criteria shift across interaction modalities.
The modality-specific columns in Table
4
show how different interaction settings give rise to distinct evaluation criteria.
Code completion rubric items emphasize low-level program concerns like
Syntax/Structural Consistency
, reflecting the need for a completion to fit seamlessly into an existing file.
Rubric items for code edits mainly capture compliance criteria such as
Data/Type Management
, where judges assess a model obeys explicit instructions and code invariants.
Chat-based criteria emphasize communication behavior through
Domain-Specific Detail
, where responses provide reasoning and explanations beyond code edits.
Rubric items connect to traditional code quality methods.
Several elements are closely related to well-studied quality dimensions.
Syntax/Structural Consistency
,
Presentation/Formatting
,
Conciseness
, and
Correctness/Precision
align with core software quality principles. Syntax validity is foundational to existing code taxonomies
[
Ernst2017WhatTF
]
, formatting and structural clarity appear in both professional and educational rubrics
[
Keuning2023ASM
,
10.1145/2999541.2999555
]
, and conciseness relates to complexity-based measures such as cyclomatic complexity while also capturing notions of minimalism and elegance
[
Nilson2019DoIS
,
AlGhuwairi2023VisualizingSR
,
Messer2024HowCA
]
. Functional and logical alignment reflects functional and methodological correctness
[
Messer2023AutomatedGA
]
.
Error Handling/Robustness
corresponds to reliability-focused evaluation criteria
[
Bishop2024EvaluatingSC
]
and engineering-oriented performance metrics
[
Hariharan2025SemanticME
]
. More granular criteria, such as
Data/Type Management
, emphasize type safety and error prevention
[
hanenberg2013
]
. Additional themes—
Clarity/Explicitness
,
Modularity/Structure
, and
Completeness
—map to established notions of readability, modularization, design quality, and problem coverage
[
Keuning2023ASM
,
Ernst2017WhatTF
,
Tablan2025SmarterTC
]
. Beyond code-level properties,
Efficiency
-oriented rubric items capture system-level quality concerns such as computational time and space usage
[
Jiang2024FromET
,
Rosenberg2002SoftwareQM
,
Curtis2022MeasuringTS
]
.
A subset of rubric items extend beyond traditional code quality methods.
Explanatory/Ethical Awareness
extends existing notions of documentation
[
Messer2023AutomatedGA
,
Messer2024HowCA
,
Menolli2025EducationalIF
,
Rai2022ARO
]
, by introducing ethical considerations, such as privacy, fairness, and societal impact, concerns largely missing from technically focused rubrics.
User-Centeredness
has limited precedent; although usability appears in ISO/IEC 9126
[
Bishop2024EvaluatingSC
]
and productivity-oriented metrics exist
[
Hariharan2025SemanticME
]
, our rubric extends beyond usability and efficiency to emphasize empathetic human–computer interaction and focus on problem context.
Creativity/Innovation
represents the strongest departure from traditional frameworks, which prioritize adherence to established patterns (another rubric item
Standards/Conventions
) and correct use of language idioms
[
Ernst2017WhatTF
]
over novelty. The broader literature rarely treats creativity as a code quality criterion, reflecting a historical emphasis on predictability and maintainability despite creativity’s importance in domains such as optimization and novel algorithm design.
Instruction Following
and
Domain-Specific Detail
further reflect recent evaluation dimensions emerging from interactive, goal-conditioned code generation and the growing need for specialized knowledge in LLM applications across diverse domains.
Table 10:
Rubric items produced by our pipeline for code completion.
Color indicates whether the rubric is
LLM-generated
,
human-annotated
, or
hybrid
(due to aggregation).
Rubric Axis
Upper End of Axis
Lower End of Axis
Error and Context Management
Comprehensive error handling, fallback mechanisms.
Minimal or no error handling.
if not file.exists(path):
raise FileNotFoundError(path)
open(path)
Completeness and Integrity
Ensures all essential components and functional integrity.
Misses important parts, leading to gaps.
connect()
query()
close()
query()
Explanatory and Ethical Awareness
Provides depth and considers ethical implications.
Minimal explanation with no ethical consideration.
# Mask PII before logging
print(user_ssn)
Engagement and User Interaction
Engages empathetically and responds to user context.
Lacks engagement and ignores user perspective.
"JSON or CSV?"
"Done."
Creativity and Innovation
Introduces novel problem decompositions or reframes the task in an original way.
Applies standard patterns without rethinking the structure of the problem.
def solve(items):
return groupby(normalize(items))
result = []
for x in items:
result.append(x)
Conciseness and Simplicity
Minimal, straightforward solutions avoiding unnecessary complexity.
Unnecessarily complex and verbose.
return sum(xs)
total = 0
for i in xs:
total += i
return total
Flexibility and Generality
Adaptable, modular solutions that handle diverse inputs.
Rigid, specific implementations without generality.
def load(path, fmt):
…
def load_csv(path):
…
Syntax and Structural Consistency
Adheres to syntax rules with consistent structure.
Contains syntax errors and inconsistent elements.
def add(a,b):
return a+b
def add(a b)
return a+b
Functional and Logical Alignment
Matches expected behavior / logic.
Deviates from intended behavior / logic.
if x > 0:
handle(x)
if x < 0:
handle(x)
Explicitness and Clarity
Clear, self-explanatory approaches that minimize ambiguity.
Obscure and requires deeper analysis to understand.
user_count = len(users)
uc = len(u)
Table 11:
Rubric items produced by our pipeline for code edits.
Color indicates whether the rubric is
LLM-generated
,
human-annotated
, or a
hybrid
(due to aggregation).
Rubric Axis
Upper End of Axis
Lower End of Axis
Instruction Fidelity
Strictly follows templates and instructions.
Interprets instructions flexibly.
# Format: name,age,date
print("{name},{age},{date}")
# Close enough
print(name, age)
Contextual and Creative Adaptability
Uses context cues to choose an appropriate approach.
Uses a fixed approach regardless of context.
if len(records) > 1000000:
process_stream(records)
process_in_memory(records)
Visual Presentation
Uses contrast and spacing to ensure readability.
Places text on low-contrast backgrounds, harming legibility.
# High contrast
plt.text(0.5, 0.5, "Warning", color="black", bbox=dict(facecolor="yellow"))
# Low contrast
plt.text(0.5, 0.5, "Warning", color="lightgray", bbox=dict(facecolor="lightgray"))
Data and Type Management
Preserves data type integrity and handles errors gracefully.
Simplifies data types and neglects detailed error handling.
x: int = int(s)
if x < 0: raise ValueError()
x = s
return x
Modularity and Abstraction
Uses modular, abstract components and reasoning.
Prefers integrated, concrete implementations.
def parse(x):
…
def validate(y):
…
def run(x):
parse(x)
validate(x)
Conformance to Standards
Adheres to established standards and practices.
Deviates from conventions with non-standard approaches.
class UserService:
…
class userservice123:
…
Correctness and Precision
Ensures logical and factual accuracy, focusing on details.
Contains inaccuracies with broader strokes.
if n % 2 == 0:
even += 1
if n > 0:
even += 1
Explicitness and Clarity
Provides clear, detailed documentation and explicit code elements.
Lacks clarity with sparse documentation.
# Count active users
active_users = len(u)
a = len(u)
Brevity and Conciseness
Delivers clear, concise responses without redundancies.
Includes verbose or superfluous content.
return sum(xs)
total = 0
for i in xs:
total += i
return total
Robustness and Error Handling
Offers resilient solutions with comprehensive error management.
Fragile solutions with basic error handling.
try: load(p)
except IOError: fallback()
load(p)
Table 12:
Rubric items produced by our pipeline for chat-based coding.
Color indicates whether the rubric is
LLM-generated
,
human-annotated
, or a
hybrid
(due to aggregation).
Rubric Axis
Upper End of Axis
Lower End of Axis
User Interaction and Feedback Responsiveness
Adapts based on prior feedback.
Ignores feedback and repeats defaults.
use_json = False
emit_yaml(data)
emit_json(data)
Modularity and Code Structure
Promotes modular, organized code.
Integrated and disorganized.
def load():
…
def save():
…
def run():
load()
save()
Domain-Specific Detail and Technical Creativity
In-depth, creative domain-aware solutions.
Generic and conventional.
use_btree_index(keys)
store_list(keys)
Code Explanation and Clarity
Provides clear, detailed explanations of code.
Lacks clarity and detail in explanation.
# Validate before write
if not ok(x):
raise Err()
do_thing(x)
Language and Terminology Appropriateness
Uses preferred language and terminology.
Uses undesired or unexpected language.
def enqueue(job):
…
def push_stuff(x):
…
Efficiency and Simplicity
Efficient and straightforward design.
Resource-intensive and complex.
return sum(xs)
total = 0
for i in range(len(xs)):
total += xs[i]
Focus and Conciseness
Emphasizes the requested change only.
Includes irrelevant details.
# Patch overflow
limit = min(n, MAX)
# Here is a full redesign
init()
connect()
Error-Free and Clarity of Presentation
Clear, well-formatted, error-free.
Contains errors and unclear formatting.
if x == 0:
return None
if x = 0:
return
Intent Alignment and Instruction Adaptability
Adheres to goals and integrates complex instructions.
Deviates from goals and struggles with instructions.
# Only update auth logic
update_auth(token)
# Refactor everything
rewrite_system()
Completeness and Precision
Thorough and precise.
Broad and underspecified.
open()
read()
close()
handle_file()
Table 13:
Several core themes recur across datasets, but each modality also contributes unique axes.
Generated rubric items across code completion, code edits, and chat-based interaction, highlighting evaluation criteria shared across all datasets, shared by two datasets, or unique to one dataset.
Theme
Code Completion
Instructed Code Edits
Chat-based Coding
Scope
Clarity / Explicitness
Explicitness and Clarity
Explicitness and Clarity
Code Explanation and Clarity
All
Conciseness
Conciseness and Simplicity
Brevity and Conciseness
Focus and Conciseness
All
Correctness / Precision
Functional and Logical Alignment
Correctness and Precision
Completeness and Precision
All
Modularity / Structure
Flexibility and Generality
Modularity and Abstraction
Modularity and Code Structure
All
Error Handling / Robustness
Error and Context Management
Robustness and Error Handling
Error-Free and Clarity of Presentation
All
User-Centeredness
Engagement and User Interaction
Contextual and Creative Adaptability
User Interaction and Feedback Responsiveness
All
Creativity / Innovation
Creativity and Innovation
–
Domain-Specific Detail and Technical Creativity
Two
Completeness
Completeness and Integrity
–
Completeness and Precision
Two
Instruction Following
–
Instruction Fidelity
Intent Alignment and Instruction Adaptability
Two
Standards / Conventions
–
Conformance to Standards
Language and Terminology Appropriateness
Two
Efficiency
Conciseness and Simplicity
–
Efficiency and Simplicity
Two
Presentation / Formatting
–
Visual Presentation
Error-Free and Clarity of Presentation
Two
Syntax / Structural Consistency
Syntax and Structural Consistency
–
–
One
Explanatory / Ethical Awareness
Explanatory and Ethical Awareness
–
–
One
Data / Type Management
–
Data and Type Management
–
One
Domain-Specific Detail
–
–
Domain-Specific Detail
One