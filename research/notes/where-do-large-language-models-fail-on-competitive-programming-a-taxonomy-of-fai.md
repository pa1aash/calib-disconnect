---
title: Where Do Large Language Models Fail on Competitive Programming? A Taxonomy
  of Failures by Algorithm Type and Difficulty Rating
id: where-do-large-language-models-fail-on-competitive-programming-a-taxonomy-of-fai
tags:
- code-llm-requirement-pivots-5d35f5
- competitive-programming-eval
- prior-art-check
created: '2026-07-20T06:52:20.891782Z'
updated: '2026-07-20T06:55:36.888936Z'
source: https://arxiv.org/html/2606.05228
source_domain: arxiv.org
fetched_at: '2026-07-20T06:52:20.891413Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Empirical failure taxonomy of GPT-4o and Claude Sonnet 4.6 on 315 balanced
  Codeforces problems (7 algorithm categories x 3 difficulty tiers, pass@1, whole-submission
  verdict). Evaluation is WHOLE-PROBLEM binary (AC vs not) checked against only up
  to 3 public test cases; no per-test-case/partial-credit granularity is reported
  -- the paper''s contribution is a 2D taxonomy of aggregate pass rate by category
  x difficulty plus a verdict-type breakdown (WA/CE/RE/TLE), not sub-task decomposition.
  Key finding: Wrong Answer dominates failures (92% GPT-4o, 70% Claude), confirming
  competitive-programming evaluation in the literature stays coarse/binary at the
  whole-solution level even when authors want fine-grained diagnosis -- corroborates
  that no one is doing per-test partial credit on competitive code. Also documents
  a ''CoT penalty'': forced chain-of-thought drops GPT-4o''s AC rate from 46.0% to
  36.8% via hallucinated flawed algorithmic proofs (''context poisoning''), while
  it triples Claude''s compile errors (9->31) via markdown formatting collapse under
  verbose CoT.'
---

Where Do Large Language Models Fail on Competitive Programming? A Taxonomy of Failures by Algorithm Type and Difficulty Rating
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2606.05228v1 [cs.SE] 02 Jun 2026
Where Do Large Language Models Fail on Competitive Programming?
A Taxonomy of Failures by Algorithm Type and Difficulty Rating
Ayush Kumar Jha
Department of Information Technology
IIIT Bhubaneswar
Bhubaneswar, Odisha, India
ayushjha4277@gmail.com
Shalini Jha
Department of Computer Science
IIT Patna
Patna, Bihar, India
jha718897@gmail.com
Abstract
Large language models (LLMs) demonstrate increasing proficiency on competitive programming benchmarks, yet technical reports predominantly publish aggregate pass rates, obscuring domain-specific vulnerabilities. We present a systematic empirical study of LLM failure patterns using a balanced taxonomy of 315 Codeforces problems across seven algorithm categories and three difficulty tiers. We evaluate GPT-4o and Claude Sonnet 4.6 under strict execution-based conditions, controlling for temperature (
T
=
0.2
T=0.2
). To isolate the impact of reasoning frameworks on algorithmic correctness, we conduct an ablation study comparing direct zero-shot generation against zero-shot Chain-of-Thought (CoT). Our findings reveal a severe divergence from standard NLP benchmarks: forcing CoT aggressively penalizes GPT-4o, dropping its pass rate from 46.0% to 36.8% and exacerbating a critical weakness in Greedy logic. Conversely, while Claude maintains a higher logical baseline (63.5% under CoT), the expanded text generation severely degrades its markdown instruction adherence, causing its Compile Errors to more than triple (from 9 to 31, a 244% increase). Furthermore, failure-mode analysis indicates that Wrong Answer (WA) is the dominant verdict for both models—accounting for over 90% of GPT-4o’s and roughly 70% of Claude’s unaccepted solutions. These findings empirically demonstrate that standard prompt engineering techniques fail to bridge the algorithmic reasoning gap in competitive programming environments.
Keywords
large language models
⋅
\cdot
code generation
⋅
\cdot
competitive programming
⋅
\cdot
failure analysis
⋅
\cdot
algorithm taxonomy
⋅
\cdot
GPT-4o
⋅
\cdot
Claude
1
Introduction
Large Language Models (LLMs) have demonstrated substantial capability in automated code generation. Early benchmarks, such as HumanEval
[
3
]
, evaluated basic functional synthesis, while subsequent datasets like APPS
[
6
]
and CodeContests
[
4
]
shifted the evaluation frontier to competitive programming. Competitive programming requires models to parse complex natural language constraints, identify optimal algorithmic substructures, and synthesize executable code that strictly adheres to asymptotic time and memory limits.
While frontier models including AlphaCode
[
8
]
, GPT-4
[
11
]
, and the Claude 3 family
[
1
]
have achieved increasingly high aggregate pass rates on these benchmarks, the monolithic reporting of these metrics obscures the specific boundaries of model capabilities. Current technical reports provide percentile rankings or overall zero-shot accuracy, but fail to provide granular taxonomies of
where
and
how
these models fail across distinct algorithmic domains.
We address this gap by presenting a systematic empirical study of LLM failure patterns. Using a highly controlled, balanced sample of 315 Codeforces problems, we map the performance of two high-efficiency frontier models (GPT-4o and Claude Sonnet 4.6) across seven distinct algorithm categories and three difficulty tiers.
1.1
Motivation
Understanding the specific algorithmic blind spots of LLMs is necessary for the development of targeted self-correction pipelines and specialized code-generation agents. If a model fails predominantly on syntax or compilation, the intervention requires better linters or compiler-feedback loops. However, if a model reliably compiles but fails on mathematical logic or edge-case handling, the intervention requires algorithmic reasoning frameworks. By categorizing failures simultaneously by problem type, difficulty, and execution verdict, we provide practitioners and benchmark designers with a diagnostic map of current model limitations.
1.2
Research Questions
Our empirical evaluation is structured around three primary research questions:
RQ1
Does LLM performance degrade non-uniformly across specific algorithm categories (e.g., Dynamic Programming, Graphs, Greedy logic)?
RQ2
How does the empirical pass rate correlate with official Codeforces difficulty ratings, and where do frontier models cross the threshold of failure?
RQ3
What is the primary execution failure mode (Wrong Answer, Time Limit Exceeded, Runtime Error, or Compile Error) when models fail to generate an accepted solution?
1.3
Contributions
Our methodology and findings yield the following contributions to the evaluation of code-generation models:
1.
A 2D Failure Taxonomy:
We introduce a novel evaluation grid isolating LLM performance across both Algorithm Category and Difficulty Tier, proving that pass rates degrade non-linearly depending on the required algorithmic domain.
2.
The CoT Penalty in Code Generation:
Through a controlled ablation study, we demonstrate that zero-shot Chain-of-Thought prompting—a standard technique for improving LLM reasoning—catastrophically degrades GPT-4o’s performance (
−
9.2
-9.2
percentage points in AC rate) while destroying Claude Sonnet 4.6’s formatting adherence.
3.
Execution Error Profiling:
We demonstrate that the majority of unaccepted solutions result from a Wrong Answer (WA) verdict (over 90% for GPT-4o), indicating the bottleneck is fundamentally algorithmic reasoning rather than syntactical validity or asymptotic efficiency.
2
Related Work
Our evaluation intersects with three primary subfields of machine learning research: foundational code generation benchmarks, frontier model evaluations, and the analysis of language model failure modes.
2.1
Foundational Code Generation Benchmarks
Initial evaluations of LLM coding capabilities relied on zero-shot generation of isolated functions. HumanEval
[
3
]
established a baseline for measuring syntactical correctness and basic functional logic using a pass@
k
k
metric. To evaluate deeper algorithmic reasoning,
Hendrycks et al. [
6
]
introduced the APPS dataset, shifting the focus to competitive programming problems sourced from platforms like Codeforces and LeetCode. While these benchmarks defined the standard for evaluating code generation, they predominantly report aggregate pass rates. Our work extends this methodology by disaggregating performance, providing a fine-grained taxonomy of where these aggregate metrics fail across specific algorithm categories and difficulty tiers.
2.2
Frontier Models and Competitive Programming
Competitive programming serves as a rigorous testbed for LLM reasoning capabilities due to its strict execution constraints and requirement for multi-step logical synthesis. AlphaCode
[
8
]
demonstrated that transformer-based architectures could achieve median human-level performance in simulated programming contests using massive-scale sampling and filtering. Subsequent open-weight models, such as DeepSeek-Coder
[
5
]
, and proprietary frontier models like GPT-4
[
11
]
and the Claude 3 family
[
1
]
, have further optimized for competitive programming tasks. However, the technical reports accompanying these models typically publish monolithic success metrics (e.g., simulated Elo ratings or aggregate pass@1 scores). These reports obscure the models’ specific algorithmic blind spots, which our 2D taxonomy matrix explicitly maps.
2.3
Evaluation Contamination
A known confounding variable in competitive programming evaluations is dataset contamination.
Jain et al. [
7
]
introduced LiveCodeBench, demonstrating that frontier LLMs achieve inflated performance on historical LeetCode and Codeforces problems due to memorization of their pre-training corpora. By establishing a contamination-free evaluation window, they proved that true zero-shot reasoning degrades significantly on novel problems. We acknowledge that our CodeContests
[
4
]
evaluation set predates the training cutoffs for both GPT-4o and Claude Sonnet 4.6. Consequently, our study does not claim to measure uncontaminated zero-shot reasoning; rather, it measures the models’ combined retrieval and reasoning capabilities. Given this baseline, the severe degradation we observe on specific algorithmic subsets (such as hard dynamic programming and greedy logic) represents a fundamental failure in the models’ ability to synthesize learned concepts, regardless of prior exposure.
2.4
Failure Analysis and Self-Correction
Recent literature investigates how LLMs resolve generation failures through iterative prompting. Techniques such as Chain-of-Thought (CoT)
[
14
]
structure the reasoning process, while frameworks like Reflexion
[
13
]
and Self-Refine
[
9
]
attempt to correct code using verbal reinforcement and compiler feedback. Despite these advancements,
Olausson et al. [
10
]
empirically demonstrated that LLMs frequently fail to self-repair logical bugs without external human guidance. Their findings indicate that while models easily resolve syntax errors, they struggle to identify and correct flawed algorithmic logic. This limitation directly motivates our experimental design; by restricting evaluation to a single-attempt (pass@1) zero-shot prompt, we isolate the models’ base logical pathways. Our finding that failures are overwhelmingly dominated by Wrong Answer (WA) rather than Compile Error (CE) verdicts provides empirical reinforcement for Olausson et al.’s observations within a strictly categorized competitive programming taxonomy.
3
Methodology
To systematically evaluate where Large Language Models fail on competitive programming tasks, we designed an automated, zero-shot evaluation pipeline. This pipeline samples problems across algorithmic domains, queries models under controlled hyperparameters, executes the generated Python code in an isolated sandbox, and classifies failures into a standard competitive programming verdict hierarchy.
3.1
Dataset
We construct our evaluation benchmark using the CodeContests dataset
[
4
]
, originally introduced to evaluate AlphaCode
[
8
]
. While CodeContests aggregates problem statements from multiple competitive programming platforms, we filter the dataset to exclusively include problems sourced from Codeforces. This filtering is strictly necessary to access high-quality, community-verified metadata—specifically, the
cf_tags
(algorithm categorisations) and
cf_rating
(Elo-based difficulty scores) required to build our taxonomy.
3.2
Problem Categorisation
To map model performance across distinct logical domains, we group the official Codeforces problem tags into seven broad algorithm categories. Problems containing multiple tags are assigned to the first matching category. The taxonomy mapping is detailed in Table
1
.
Table 1:
Algorithm categories and their corresponding Codeforces tags.
Category
Codeforces Tags
Dynamic Programming
dp
Graphs
graphs, dfs and similar, shortest paths, trees
Greedy
greedy
Binary Search
binary search, two pointers
Mathematics
math, number theory, combinatorics
Data Structures
data structures, sortings
Implementation
implementation, brute force
3.3
Difficulty Tiers
We stratify the problems into three difficulty tiers based on their official Codeforces Elo problem ratings. These cutoffs are not arbitrary; they align directly with Codeforces’ official user rank thresholds and Division boundaries:
•
Easy (800–1400):
Corresponds to the Newbie and Pupil ranks. Problems typically require introductory logic and basic implementation (standard Division 3/4 difficulty).
•
Medium (1401–1900):
Corresponds to the Specialist and Expert ranks. Problems require intermediate algorithms and standard data structures (standard Division 2 difficulty).
•
Hard (1901–3500):
Corresponds to Candidate Master and above. Problems require advanced multi-step optimization and complex mathematics (standard Division 1 difficulty).
3.4
Sampling Strategy
To prevent algorithmic imbalance from skewing the aggregate pass rates, we apply a strict balanced sampling strategy. We extract exactly 15 problems for each intersection of Algorithm Category and Difficulty Tier (7 categories
×
\times
3 tiers
×
\times
15 problems), yielding a highly controlled benchmark of 315 problems. To ensure reproducibility, problems are selected deterministically based on their original index in the CodeContests training split.
3.5
Models Evaluated
We evaluate two widely deployed, high-efficiency frontier models: GPT-4o
[
12
]
and Claude Sonnet 4.6 (released February 2026)
[
2
]
. To minimize output variance and measure the models’ most confident logical pathways, we set the sampling temperature to
T
=
0.2
T=0.2
. The maximum output length is constrained to 2048 tokens to accommodate verbose reasoning and complex string manipulations without truncation. We evaluate using a strict
pass@1
metric; each model is given only a single generation attempt per problem.
3.6
Prompt Design and Ablation Setup
To isolate the impact of reasoning frameworks on algorithmic accuracy, both models are evaluated under two strict, zero-shot prompting conditions. We structure the input using a standard user prompt that dynamically injects the problem metadata, paired with a condition-specific system prompt.
The universal user prompt applied across all evaluations is formatted as follows:
⬇
Problem
:
{
problem
[’
name
’]}
{
problem
[’
description
’]}
Write
a
complete
Python
3
solution
.
Condition A: Direct Generation.
This baseline strictly forbids natural language explanations, forcing the model to rely on its implicit internal representations and maximizing the token budget for code generation.
⬇
You
are
a
competitive
programmer
.
Solve
the
given
problem
in
Python
3.
Output
ONLY
the
complete
Python
code
inside
a
markdown
block
.
No
explanations
.
The
code
must
read
from
stdin
and
print
to
stdout
.
Condition B: Chain-of-Thought (CoT).
This condition overrides the Direct baseline by forcing explicit algorithmic planning prior to code generation. This tests whether enforced exchange-arguments and formal mathematical derivations resolve the models’ logical blind spots.
⬇
You
are
a
competitive
programmer
.
Solve
the
given
problem
in
Python
3.
First
,
write
a
detailed
algorithmic
plan
and
mathematical
proof
of
your
approach
.
Then
,
output
the
complete
Python
code
inside
a
markdown
block
.
The
code
must
read
from
stdin
and
print
to
stdout
.
3.7
Evaluation Protocol
Model outputs are parsed via regular expressions to extract the executable Python code, which is then run inside a
subprocess
sandbox. Each solution is executed against a maximum of three public test cases. To ensure a fair assessment of algorithmic efficiency, we enforce a strict 5-second timeout limit per test case.
Results are classified into a standard competitive programming verdict hierarchy. If a solution fails multiple test cases, the worst verdict is recorded based on the following priority list:
1.
Compile Error (CE):
Invalid Python syntax.
2.
Runtime Error (RE):
Exceptions during execution (e.g.,
IndexError
,
ZeroDivisionError
).
3.
Time Limit Exceeded (TLE):
Execution exceeds the 5-second threshold, indicating suboptimal asymptotic complexity.
4.
Wrong Answer (WA):
The program compiles and executes within the time limit, but produces incorrect output.
5.
Accepted (AC):
The program produces the exact expected output for all test cases.
4
Results
In this section, we present the empirical pass rates and failure distributions across the 315 evaluated problems. We structure our findings to systematically address the core research questions: aggregate performance, degradation by algorithm and difficulty, and the distribution of execution failure modes. Unless stated otherwise, all per-category, per-tier, joint, and failure-mode results report the Chain-of-Thought (CoT) condition; the Direct condition is reported only as the ablation baseline in Section
4.1
.
4.1
Overall Performance
Across the strictly controlled, balanced sample of 315 problems, Claude Sonnet 4.6 established a higher empirical baseline than GPT-4o under both prompting conditions. Under
Direct
generation, Claude achieved an Accepted (AC) verdict on 196 problems (62.2%) versus GPT-4o’s 145 (46.0%). Under
Chain-of-Thought
prompting, Claude solved 200 problems (63.5%) while GPT-4o dropped to 116 (36.8%). Claude thus remained essentially stable across the two conditions, whereas enforced CoT degraded GPT-4o by
9.2
9.2
percentage points—a divergence we analyze in detail in Section
5
.
4.2
Performance by Algorithm Category (RQ1)
Model performance exhibits high variance depending on the underlying algorithmic domain required to solve the problem. Table
2
details the pass rates across all seven categories under CoT prompting.
Claude Sonnet 4.6 outperformed GPT-4o in every category. The performance gap is most pronounced in Greedy and Graphs logic. On
greedy
problems, Claude reached 64.4% versus GPT-4o’s 28.9%—a gap of 35.5 percentage points (Figure
1
). Greedy was also GPT-4o’s single weakest category (28.9%), consistent with the “context-poisoning” effect we analyze in Section
5.1
.
Table 2:
Pass rate (%) by algorithm category under CoT prompting (
n
=
45
n=45
per category).
Algorithm Category
GPT-4o
Claude Sonnet 4.6
Dynamic Programming
35.6
60.0
Graphs
33.3
64.4
Greedy
28.9
64.4
Binary Search
40.0
60.0
Mathematics
35.6
62.2
Data Structures
42.2
68.9
Implementation
42.2
64.4
Figure 1:
Aggregate pass rates by algorithm category under CoT prompting. GPT-4o’s vulnerability to "context poisoning" is most evident in the Greedy category, where its pass rate degraded to 29%.
4.3
Performance by Difficulty Tier (RQ2)
We observe a non-linear degradation in pass rates as problem difficulty scales. As shown in Table
3
, both models reliably solve introductory logic, with Claude and GPT-4o achieving 91.4% and 61.9% on Easy problems, respectively.
However, scaling to Medium difficulty exposes a sharp divergence in model capabilities. GPT-4o experiences a steep 22.9 percentage point drop in accuracy (falling to 39.0%), whereas Claude demonstrates higher robustness, retaining a 70.5% pass rate on intermediate data structures and algorithms. Both models collapse on Hard problems, falling to 28.6% (Claude) and 9.5% (GPT-4o)—below the 30% threshold.
Table 3:
Pass rate (%) by difficulty tier under CoT prompting (
n
=
105
n=105
per tier).
Difficulty Tier
GPT-4o
Claude Sonnet 4.6
Easy (800–1400)
61.9
91.4
Medium (1401–1900)
39.0
70.5
Hard (1901–3500)
9.5
28.6
4.4
Joint Analysis: Algorithm
×
\times
Difficulty
To isolate specific algorithmic bottlenecks, we expand the evaluation into a 2D taxonomy matrix (Table
4
), reporting the CoT condition visualized in Figure
2
. This granular breakdown reveals domain-specific failure thresholds.
Dynamic Programming (DP) proves universally brittle for LLMs at higher difficulties; on Hard DP problems, GPT-4o solves none (0%) while Claude manages only 20%. GPT-4o’s collapse at the Hard tier is most severe in DP and Binary Search, where it fails every problem (0%). Claude outperforms GPT-4o in every cell of the matrix; its largest Hard-tier advantage appears in Graphs (47% vs. 13%), where it identifies structural graph-theoretic templates that GPT-4o misses. We note that the Direct baseline produces a different picture at the extremes—most notably an inversion on Hard Mathematics in which GPT-4o briefly overtakes Claude—which we analyze in Section
5.2
.
Table 4:
Taxonomy of Pass Rates (%) across Algorithm Category
×
\times
Difficulty Tier, under CoT prompting. Format: GPT-4o / Claude Sonnet 4.6. Bold text denotes the superior pass rate for the given cell.
Algorithm
Easy
Medium
Hard
Dynamic Programming
60 /
87
47 /
73
0 /
20
Graphs
53 /
93
33 /
53
13 /
47
Greedy
53 /
87
20 /
73
13 /
33
Binary Search
80 /
87
40 /
67
0 /
27
Mathematics
60 /
100
33 /
67
13 /
20
Data Structures
60 /
93
53 /
80
13 /
33
Implementation
67 /
93
47 /
80
13 /
20
Figure 2:
Pass rates (%) across the Algorithm
×
\times
Difficulty taxonomy under the Chain-of-Thought (CoT) condition. GPT-4o exhibits a severe capability collapse at the Hard tier (dropping to 0% on DP and Binary Search), while Claude Sonnet 4.6 maintains structural stability.
4.5
Failure Mode Analysis (RQ3)
Evaluating the raw distribution of verdict labels provides crucial insight into the nature of LLM coding failures. For solutions that did not achieve an AC verdict under CoT prompting, we isolate the specific execution bottlenecks (Table
5
).
The data demonstrates that failures are overwhelmingly logical rather than syntactical or efficiency-based (Figure
3
). Wrong Answer (WA) accounts for 92.0% (183/199) of GPT-4o’s failures and 69.6% (80/115) of Claude’s failures. This indicates that both models reliably generate executable Python code that runs within the time limit (evidenced by only a single cumulative Time Limit Exceeded failure), but fail to correctly implement the underlying mathematical proofs or handle edge cases.
The two models diverge in their secondary failure modes. Claude’s failures include a pronounced spike in Compile Errors (31 CE)—consistent with the formatting collapse induced by verbose CoT generation (Section
5.2
)—alongside only 3 Runtime Errors (RE). GPT-4o, by contrast, produced just 6 CE but 10 RE. Broken down by algorithm category, GPT-4o’s failures are uniformly dominated by WA across every domain (Figure
4
), reinforcing that its bottleneck is correctness rather than syntax.
Table 5:
Distribution of failure modes for unaccepted solutions under CoT prompting.
Verdict
GPT-4o (Failures: 199)
Claude (Failures: 115)
Wrong Answer (WA)
183
80
Compile Error (CE)
6
31
Runtime Error (RE)
10
3
Time Limit Exceeded (TLE)
0
1
Figure 3:
Distribution of failure verdicts under CoT prompting. The requirement to generate verbose mathematical proofs induced a formatting collapse in Claude Sonnet 4.6, resulting in a spike of Compile Errors (CE), whereas GPT-4o’s failures remain overwhelmingly logical (WA).
Figure 4:
Distribution of GPT-4o’s failure types across algorithm categories. The uniform dominance of Wrong Answer (WA) confirms that the model consistently generates syntactically valid code that fails implicit correctness proofs.
5
Discussion
The empirical results demonstrate that LLM failure on competitive programming tasks is highly sensitive to the underlying algorithmic paradigm. In this section, we provide a qualitative failure analysis of the anomalous phenomena observed in the 2D taxonomy matrix, leveraging code forensics from both the Direct and CoT evaluations to distinguish between reasoning failures and execution bottlenecks.
5.1
The CoT Penalty and Context Poisoning in Greedy Algorithms
The most counter-intuitive finding in our dataset is the catastrophic degradation of GPT-4o under CoT prompting (dropping from a 46.0% to 36.8% aggregate AC rate). This deficit is most pronounced in the
greedy
category, where performance dropped to 28.9%.
Code forensics reveal a phenomenon we characterize as "context poisoning" driven by proof obligation blindness. Greedy algorithms require an implicit correctness proof—typically an exchange argument—to guarantee that a local choice yields a global optimum. When forced by the CoT prompt to explicitly write out this algorithmic plan, GPT-4o frequently hallucinates a provably incorrect heuristic. Because self-attention mechanisms heavily weight the immediate preceding context, this flawed natural language proof appears to bind the subsequent Python generation to the incorrect logic. GPT-4o performs significantly better when allowed to bypass explicit proof generation and rely on its implicit coding intuition.
5.2
Formatting Collapse and the Math Inversion
While Claude Sonnet 4.6 did not suffer a logical penalty under CoT, it suffered a mechanical one. The requirement to generate detailed proofs caused Claude to output massive text blocks (frequently 1,000+ tokens) before initializing its Python markdown environment. Even at a controlled temperature of
T
=
0.2
T=0.2
, this extended generation severely degraded its instruction adherence, causing Compile Errors to more than triple, rising from 9 in the Direct run to 31 in the CoT run.
The Direct baseline additionally exhibited an anomalous Hard Mathematics inversion. Under Direct generation, GPT-4o beat Claude on Hard Math (27% vs. 13%) by substituting elegant derivation with optimized brute-force computational iteration. When the CoT condition forced both models to attempt formal algebraic derivations, GPT-4o collapsed: under CoT, Claude holds Hard Math at 20% against GPT-4o’s 13% (Figure
2
). This reversal confirms that GPT-4o’s zero-shot strength in CP mathematics relies heavily on computational heuristics rather than formal proofs.
5.3
Wrong Answer as the Persistent Bottleneck
Despite the introduction of CoT, the most significant empirical signature in our dataset remains the dominance of the Wrong Answer (WA) verdict. Under CoT prompting, WA accounted for 183 of GPT-4o’s 199 unaccepted solutions and 80 of Claude’s 115.
This indicates that both models possess a robust grasp of Python syntax and standard API usage, successfully executing code within the strict 5-second limit. The bottleneck is strictly algorithmic correctness. For practitioners building coding assistants, this implies that integrating better code formatters, linters, or compiler-feedback loops will yield marginal returns. Standard prompt engineering (like CoT) fails to bridge this gap; the performance deficit must be addressed at the foundational reasoning layer.
5.4
Degradation Curves and Capability Ceilings
Comparing the two models across the taxonomy reveals distinct degradation curves. Claude’s degradation is back-loaded: it maintains remarkable stability through the Medium tier before collapsing at the Hard tier. A notable exception occurs in Graphs, where Claude maintains a comparatively stable pass rate across the Medium and Hard tiers (53% and 47%) by successfully identifying structural graph-theoretic templates (e.g., Strongly Connected Components, 2-SAT) on which GPT-4o scores only 13%. GPT-4o, by contrast, degrades steeply at every step and bottoms out at 0% on the hardest DP and Binary Search problems.
5.5
Limitations
We acknowledge several limitations in our methodology that restrict the generalizability of these findings:
1.
Instruction Adherence and Token Limits:
Claude frequently struggled to balance verbose CoT generation with the 2048-token limit, occasionally resulting in truncation.
2.
Public Test Cases:
Submissions were evaluated against public test cases (pretests) rather than hidden system tests. Because the pretests are limited, the near-absence of Time Limit Exceeded verdicts reflects the lightweight tests as much as the code’s asymptotic efficiency; a rigorous evaluation against complete private test suites would likely lower the aggregate pass rates for both models.
3.
Language Bias:
All evaluations were conducted in Python 3. Because competitive programming heavily favors C++, the models’ exposure to CP concepts during pre-training may be disproportionately weighted toward C++.
4.
Sample Variance:
While our stratified sampling ensured category balance, the limit of 15 problems per cell introduces substantial variance; a single problem corresponds to roughly 6.7 percentage points. Cell-level observations (such as the Hard Mathematics inversion, which rests on a difference of two problems) should therefore be read as suggestive rather than statistically confirmed. Expanding the taxonomy grid to a larger
N
N
per cell, and reporting confidence intervals, would increase the statistical confidence of the domain-specific anomalies observed.
6
Conclusion
In this paper, we introduced a 2D evaluation taxonomy to systematically measure LLM performance on competitive programming tasks across algorithm categories and difficulty tiers. By conducting an ablation study evaluating GPT-4o and Claude Sonnet 4.6 under both Direct and Chain-of-Thought (CoT) prompting conditions, we demonstrated that aggregate pass rates mask severe, domain-specific reasoning deficits. Furthermore, we established that standard prompt engineering paradigms do not cleanly generalize to strict execution-based environments.
6.1
Summary of Findings
Our empirical evaluation yielded three primary findings:
1.
The CoT Penalty:
Contrary to standard NLP benchmarks, forcing zero-shot CoT severely penalizes GPT-4o (dropping its aggregate AC rate from 46.0% to 36.8%). This is driven by "context poisoning," where the model hallucinates flawed algorithmic proofs (particularly in Greedy logic) that subsequently corrupt its code generation.
2.
Formatting Collapse:
Extended text generation mechanicalizes failure. While Claude Sonnet 4.6 maintained a high logical baseline under CoT (63.5% AC), the token exhaustion associated with verbose mathematical proofs caused its markdown adherence to break down, more than tripling its Compile Errors (from 9 to 31).
3.
The Algorithmic Logic Bottleneck:
The dominance of the Wrong Answer (WA) verdict across both conditions confirms that both models generate syntactically valid Python code that runs within the time limit, but fundamentally fail at mathematical reasoning and edge-case simulation.
6.2
Future Work
The failure of zero-shot CoT to resolve algorithmic blind spots indicates that single-pass generation has reached a structural reasoning ceiling in competitive programming. Future research must investigate dynamic test-time compute—specifically, whether models can utilize isolated execution sandboxes to verify exchange arguments and recurrence relations prior to final output. Additionally, evaluating multi-agent debate and execution-guided self-repair on our taxonomy will determine if iterative compiler feedback can successfully guide models to correct the deep logical flaws inherent in dynamic programming and greedy failures.
Acknowledgements
The authors acknowledge the researchers at Google DeepMind for the open-source release of the CodeContests dataset, as well as the broader Codeforces competitive programming community for providing the robust problem structures that made this evaluation possible.
References
Anthropic [2024]
Anthropic.
The Claude 3 model family: Opus, sonnet, haiku.
Technical report, Anthropic, 2024.
Anthropic [2026]
Anthropic.
Claude Sonnet 4.6.
Anthropic model announcement, 2026.
Released February 2026.
https://www.anthropic.com/news
.
Chen et al. [2021]
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al.
Evaluating large language models trained on code.
arXiv preprint arXiv:2107.03374
, 2021.
DeepMind [2022]
DeepMind.
CodeContests: A competitive programming dataset.
HuggingFace Datasets, 2022.
https://huggingface.co/datasets/deepmind/code_contests
.
Guo et al. [2024]
Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, et al.
DeepSeek-Coder: When the large language model meets programming – the rise of code intelligence.
arXiv preprint arXiv:2401.14196
, 2024.
Hendrycks et al. [2021]
Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob Steinhardt.
Measuring coding challenge competence with APPS.
In
Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks (NeurIPS Datasets and Benchmarks)
, 2021.
arXiv:2105.09938.
Jain et al. [2025]
Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
LiveCodeBench: Holistic and contamination free evaluation of large language models for code.
In
The Thirteenth International Conference on Learning Representations (ICLR)
, 2025.
Li et al. [2022]
Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, et al.
Competition-level code generation with AlphaCode.
Science
, 378(6624):1092–1097, 2022.
Madaan et al. [2023]
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, et al.
Self-refine: Iterative refinement with self-feedback.
In
Advances in Neural Information Processing Systems (NeurIPS)
, volume 36, 2023.
Olausson et al. [2024]
Theo X. Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao, and Armando Solar-Lezama.
Is self-repair a silver bullet for code generation?
In
The Twelfth International Conference on Learning Representations (ICLR)
, 2024.
OpenAI [2023]
OpenAI.
GPT-4 technical report.
arXiv preprint arXiv:2303.08774
, 2023.
OpenAI [2024]
OpenAI.
GPT-4o system card.
arXiv preprint arXiv:2410.21276
, 2024.
Shinn et al. [2023]
Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
Reflexion: Language agents with verbal reinforcement learning.
In
Advances in Neural Information Processing Systems (NeurIPS)
, volume 36, 2023.
Wei et al. [2022]
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V. Le, and Denny Zhou.
Chain-of-thought prompting elicits reasoning in large language models.
In
Advances in Neural Information Processing Systems (NeurIPS)
, volume 35, pages 24824–24837, 2022.
Appendices
Appendix A
Prompt Templates
To ensure complete reproducibility, we provide the exact prompt templates used in our evaluation pipeline. The
{problem[’name’]}
and
{problem[’description’]}
fields were dynamically populated from the filtered CodeContests dataset during execution.
A.1
User Prompt (Universal)
⬇
Problem
:
{
problem
[’
name
’]}
{
problem
[’
description
’]}
Write
a
complete
Python
3
solution
.
A.2
System Prompt (Condition A: Direct Generation)
⬇
You
are
a
competitive
programmer
.
Solve
the
given
problem
in
Python
3.
Output
ONLY
the
complete
Python
code
inside
a
markdown
block
.
No
explanations
.
The
code
must
read
from
stdin
and
print
to
stdout
.
A.3
System Prompt (Condition B: Chain-of-Thought)
⬇
You
are
a
competitive
programmer
.
Solve
the
given
problem
in
Python
3.
First
,
write
a
detailed
algorithmic
plan
and
mathematical
proof
of
your
approach
.
Then
,
output
the
complete
Python
code
inside
a
markdown
block
.
The
code
must
read
from
stdin
and
print
to
stdout
.
Appendix B
Dataset Statistics
To construct the balanced evaluation taxonomy of 315 problems, we sampled exactly 15 problems per intersection of Algorithm Category and Difficulty Tier. Table
6
details the total available pool of valid, Codeforces-sourced problems within the CodeContests dataset that met our strict filtering criteria before sampling.
The smallest pool (Binary Search, Easy) contained 72 problems, validating that a strict sample size of 15 problems per cell was methodologically sound without risking duplicate sampling or dataset exhaustion.
Table 6:
Total available problem pool sizes in the filtered CodeContests dataset before balanced sampling (
n
=
15
n=15
per cell).
Algorithm Category
Easy (800–1400)
Medium (1401–1900)
Hard (1901–3500)
Dynamic Programming
118
440
1100
Graphs
80
286
725
Greedy
547
475
316
Binary Search
72
168
224
Mathematics
476
305
399
Data Structures
99
105
277
Implementation
631
212
115