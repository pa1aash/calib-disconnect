---
title: Where Do LLMs Still Struggle? An In-Depth Analysis of Code Generation Benchmarks
id: where-do-llms-still-struggle-an-in-depth-analysis-of-code-generation-benchmarks
tags:
- code-llm-best-aaai-paper-6ded37
- failure-taxonomy
- task-level-not-requirement-level
created: '2026-07-20T07:43:11.484523Z'
updated: '2026-07-20T07:45:54.245436Z'
source: https://arxiv.org/html/2511.04355v1
source_domain: arxiv.org
fetched_at: '2026-07-20T07:43:11.484148Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Empirical study of 4 benchmarks (MBPP, HumanEval, BigCodeBench, LiveCodeBench)
  x 6 LLMs (Claude Sonnet-4, DeepSeek-V3, Qwen3-Coder, GPT-4o, Llama-3.3-70B, Mistral-3.2-24B),
  identifying 114 tasks that all models consistently fail on WHOLE-TASK granularity
  (not per-requirement). Finds static code complexity does NOT fully explain failures;
  qualitative inspection yields four recurring failure patterns: wrong problem mapping,
  flawed/incomplete algorithm design, edge-case mishandling, and formatting mistakes.
  Useful as a task-level (not requirement-level) failure-taxonomy baseline and citation
  for motivating why aggregate pass@1 hides structure -- but purely qualitative/taxonomic,
  no factor-analytic or IRT latent-skill modeling, and does not use per-unittest-method
  partial credit.'
---

Where Do LLMs Still Struggle? An In-Depth Analysis of Code Generation Benchmarks
Where Do LLMs Still Struggle? An In-Depth Analysis of Code Generation Benchmarks
Amir Molzam Sharifloo1,
Maedeh Heydari1, Parsa Kazerooni1,
Daniel Maninger12,
Mira Mezini123
Abstract
Large Language Models (LLMs) have achieved remarkable success in code generation, and the race to improve their performance has become a central focus of AI research. Benchmarks and leaderboards are increasingly popular, offering quantitative rankings of LLMs. However, they provide limited insight into the tasks that LLMs consistently fail to solve—information that is crucial for understanding current limitations and guiding the development of more capable models.
To address this gap, we examined code generation tasks across four popular benchmarks, identifying those that major LLMs are most likely to fail. To understand the causes of these failures, we investigated whether the static complexity of solution code contributes to them, followed by a systematic inspection of 114 tasks that LLMs consistently struggled with.
Our analysis revealed four recurring patterns of weaknesses in LLMs, as well as common complications within benchmark tasks that most often lead to failure.
I
Introduction
Large Language Models (LLMs) are rapidly transforming software development by automating code generation tasks. Trained on massive corpora of open-source code, these systems are now widely adopted in practice—recent surveys indicate that many developers regularly use AI-assisted coding tools
[
1
]
. As the adoption of code-generating LLMs accelerates, rigorous benchmarking becomes increasingly critical. Effective benchmarks provide a standardized framework to evaluate model capabilities, track progress over time, and compare systems on common grounds.
A variety of benchmarks have been proposed to evaluate LLM code generation
[
2
,
3
,
4
,
5
,
6
]
. Early efforts, such as
Most Basic Python Problems (MBPP)
[
3
]
and
HumanEval
[
2
]
, focus on functional correctness for small Python programs, probing models’ understanding of algorithms, language, and basic libraries. Extensions like MBPP+ and HumanEval+
[
7
]
increase test coverage to reveal edge cases, while HumanEval Pro and MBPP Pro
[
8
]
introduce compositional tasks requiring multiple function calls, testing reasoning across generation steps. Other benchmarks emphasize scale and realism:
APPS
[
9
]
offers thousands of competitive programming problems with multiple test cases, and
LiveCodeBench
[
4
]
continuously updates problems from platforms like LeetCode and AtCoder.
BigCodeBench
[
5
]
evaluates use of external libraries across domains, while repository-level benchmarks such as
SWE-bench
[
6
]
assess LLM performance on multi-file software development tasks.
Despite the widespread adoption of these benchmarks, there has been little systematic analysis of their tasks and the cases where LLMs failed to generate correct code. Identifying failure-inducing tasks and understanding the underlying causes of the failures is essential for guiding both benchmark design and model development. The prior work
[
10
]
analyzed the errors that LLMs made when generating code for the HumanEval benchmark and reported both syntactic and semantic mistakes. However, its scope was limited to HumanEval and did not consider more diverse or challenging benchmarks. In contrast, this paper addresses this gap by conducting an empirical study of popular function-level code generation benchmarks, aiming to answer the following research questions:
RQ1:
Which tasks do LLMs consistently fail to solve?
RQ2:
To what extent can these failures be explained by the complexity of the solution code?
RQ3:
Which additional factors, beyond code complexity, influence LLM failures?
To investigate these questions, we conducted a task-level study of four widely used benchmarks (MBPP, HumanEval, BigCodeBench, and LiveCodeBench) and evaluated six representative advanced LLMs selected to reflect diverse and popular code generation scenarios (Claude Sonnet-4, DeepSeek-V3, Qwen3-Coder, GPT-4o, Llama-3.3-70B, and Mistral-3.2-24B). We additionally implemented a tool to measure task complexity from the corresponding solution code, which we used to examine its correlation with model failures. Interestingly, complexity alone did not fully account for these failures, suggesting that additional factors play a significant role. Analyzing the 114 consistently failed tasks across benchmarks, we identified four recurring failure patterns:
wrong problem mapping, flawed or incomplete algorithm design, edge case mishandling, and formatting mistakes
. This analysis reveals how factors beyond solution complexity contribute to LLM failures. We further observed that some benchmark tasks are extremely ambiguous, so that certain failures do not necessarily reflect actual model weaknesses. Our contributions are as follows:
(1)
Detailed task-level experimental results for four widely used benchmarks evaluated on six major LLMs.
(2)
A method for measuring solution code complexity and analyzing its correlation with LLM failure rates.
(3)
Fine-grained failure inspection of 114 tasks, revealing patterns of weaknesses in LLMs and challenges arising from benchmark design.
The experimental data and analysis scripts are publicly released on GitHub to support reproducibility and future research.
1
1
1
https://github.com/breath24/FailureBench
.
II
Experimental Setup
Benchmarks:
We conducted a survey of existing code generation benchmarks and selected those that are both widely adopted in the research community and equipped with executable test cases, enabling reliable evaluation of generated code. Our final selection comprises HumanEval (5,845 citations as of August 2025), MBPP (2,142), LiveCodeBench (524), and BigCodeBench (240), representing a diverse yet widely used set of benchmarks for code generation. In this paper, we focused on benchmarks that specialize in function generation, where a natural language problem is given (with or without contextual code) and the model is required to generate a function that implements the expected functionality.
We used the latest version of each benchmark available to minimize data contamination, thereby increasing the likelihood of observing failures. The APPS benchmark was excluded, as it is widely used for training and would risk contamination. Due to the large number of tasks in MBPP, we relied on a subset of 378 tasks, used in recent extensions such as MBPP+.
For LiveCodeBench, we used LCB-V6, which consists of 175 programming problems released between January and April 2025. For BigCodeBench, we focused on the BCB-Hard subset (148 tasks) using instruct prompts, which contains the most difficult tasks to challenge LLMs. In total, we experimented with 865 tasks across four benchamrks.
Models:
As for the LLMs, we chose six representative advanced LLMs—namely Claude Sonnet-4, DeepSeek-V3, Qwen3-Coder, GPT-4o, Llama-3.3-70B and Mistral-3.2-24B—from different projects that have been widely used. Unfortunately, we excluded Gemini and Grok due to our limited budget and their costly inference fees.
Evaluation Procedure:
To identify which tasks lead to failure, we ran the benchmarks on the selected LLMs and collected the generated code. Each task was evaluated using a single generated solution per model (PASS@1): a task was classified as a success if the solution passed all test cases, and as a failure otherwise. For failed tasks, additional details were recorded for further analysis. Table
I
reports the number of failures for each model across the benchmarks.
TABLE I
:
The number of task failures across benchmarks.
Model
HumanEval
MBPP
LCB
BCB-Hard
Claude Sonnet-4
2
11
54
109
Qwen3-Coder
7
9
73
102
DeepSeek-V3
14
9
76
107
GPT-4o
25
14
85
107
Mistral-3.2-24B
28
23
110
114
Llama-3.3-70B
32
32
100
101
Results:
To provide a categorization of task difficulty based on actual LLM performance, we further classified tasks according to the number of models that failed to solve them, resulting in seven categories ranging from 0 to 6, where 0 represents tasks solved by all models, and 6 represents tasks for which all models failed to generate correct code. Table
II
shows the number of failures in each category.
TABLE II
:
Distribution of model failures across benchmarks. For each benchmark, columns 0–6 indicate the number of models that failed a task: 0 = solved by all models, 1 = failed by 1 model, …, 6 = failed by all models. This provides a difficulty categorization of tasks.
Model
HumanEval (164 tasks)
MBPP (378)
LiveCodeBench (175)
BCB-Hard (148)
# Models Failed (0–6)
0
1
2
3
4
5
6
0
1
2
3
4
5
6
0
1
2
3
4
5
6
0
1
2
3
4
5
6
Claude Sonnet-4
113
0
0
0
0
1
1
318
3
0
2
2
2
2
43
0
2
1
6
10
35
14
2
4
6
8
13
76
Qwen3-Coder
113
1
0
0
2
3
1
318
1
1
1
1
3
2
43
2
3
6
9
18
35
14
0
2
5
7
12
76
DeepSeek-V3
113
0
3
3
3
4
1
318
3
0
1
1
2
2
43
0
7
6
10
18
35
14
1
2
6
8
14
76
GPT-4o
113
4
10
2
4
4
1
318
4
3
1
1
3
2
43
1
8
8
15
18
35
14
2
1
6
7
15
76
Mistral-3.2-24B
113
6
10
3
4
4
1
318
13
3
0
2
3
2
43
7
16
13
18
21
35
14
3
5
9
7
14
76
Llama-3.3-70B
113
11
9
4
3
4
1
318
21
5
1
1
2
2
43
9
14
8
14
20
35
14
3
4
4
7
7
76
Number of Tasks
113
22
16
4
4
4
1
318
45
6
2
2
3
2
43
19
25
14
18
21
35
14
11
9
12
11
15
76
•
HumanEval:
Out of 164 tasks, 113 were solved correctly by every model. There was only one task for which none of the models managed to generate the correct code. Claude Sonnet-4 performed exceptionally good with only two failures, while Llama-3.3-70B records high in failing with tasks that other models were able to solve.
•
MBPP:
Throughout the benchmark, 318 tasks were solved by every model. Two tasks were not solved by any of the models. Qwen3-Coder and DeepSeek-V3 emerged as the best models, while Llama-3.3-70B failed the highest number of tasks.
•
LiveCodeBench:
Among all tasks, 35 could not be solved correctly by any model, while 43 were solved correctly by every model. Claude Sonnet-4 demonstrated the strongest performance with only 54 failures, while Mistral-3.2-24B produced most failures.
•
BCB-Hard:
In this benchmark, only 14 tasks were correctly solved by all models, while 76 tasks were consistently failed. All models produced many failures with a failure rate range from 68% to 77%.
RQ1:
Which tasks do LLMs consistently fail at?
Our experiments identified 114 tasks across four benchmarks that all models consistently failed. BCB-Hard had the most failures, followed by LiveCodeBench.
III
Code Complexity Analysis
Solution code complexity provides a quantitative lens on task difficulty, independent of natural language prompts. To explore whether this complexity correlates to LLM performance, we analyzed ground-truth solutions across benchmarks. We first describe the complexity metrics we use, then report descriptive statistics, followed by correlation and regression analyses to examine their relationship with model failures.
III-A
Complexity Measurement
We designed and implemented an algorithm to quantitatively measure the complexity of solution code. We used a set of different code complexity dimensions, each of which captures a distinct facet of what makes a code snippet more cognitively or technically challenging. The dimensions are defined as follows:
•
Cyclomatic Complexity (CC)
: Measures the intricacy of control flow constructs, including conditionals (
if
), loops (
for
,
while
), and branching. A higher CC value indicates more involved execution paths and decision points.
•
Data Structures
: Assesses the extent and variety of data structure usage, such as lists, dictionaries, sets, and user-defined containers.
•
Function Calls
: Captures the frequency of function invocation.
•
Code Length
: Serves as a surface-level proxy for overall complexity, as longer code may correspond to richer logic.
•
Nesting Depth
: Reflects the maximum depth of syntactic nesting, such as loops within conditionals or recursive calls embedded in other structures.
•
Recursions
: Specifically tracks the presence and frequency of recursive functions.
We use static analysis of abstract syntax trees to compute each of these metrics, averaging values across all tasks in a benchmark. Table
III
presents the results of these measurements. As the measurement shows, recursions are extremely rare across benchmarks and that the use of data structures is relatively limited. LiveCodeBench demonstrates greater or nearly equal values for all metrics comparing to other benchmarks, highlighting that its solutions require highest code complexity.
TABLE III
:
Code complexity metrics-average value- across benchmarks.
Metric
HumanEval
MBPP
LCB
BCB-Hard
CC
3.34
2.58
9
4.66
Data Structures
0.26
0.10
0.62
0.69
Function Calls
3.10
2.07
12.97
11.89
Length
6.30
6.68
29.54
15.91
Nesting Depth
8.37
8.70
10.48
9.42
Recursions
0.09
0.09
0.25
0.03
III-B
Correlation Analysis
Figure
1
illustrates how average metric values vary across tasks grouped by the number of LLMs that failed to solve them. LiveCodeBench shows a clear positive correlation between code complexity metrics and failure rate, whereas no such trend is evident in the other benchmarks. To quantify these relationships, we applied the Spearman and linear regression methods to measure the correlation between benchmark failure rates and individual metrics. Spearman’s results suggested that LiveCodeBench failures were positively correlated with code complexity metrics. In contrast, correlations remain weak and statistically non-significant for HumanEval, MBPP, and BCB-Hard. Applying regression, the explanatory power of all metrics is negligible in HumanEval and MBPP, with consistently low
R
2
R^{2}
values and non-significant p-values, indicating that these metrics do not meaningfully account for failure rates. BCB-Hard exhibits slightly stronger signals: metrics such as length and nesting depth achieve moderate
R
2
R^{2}
values (
≈
0.14
\approx 0.14
–
0.15
0.15
) with borderline p-values (
≈
0.07
\approx 0.07
–
0.09
0.09
), suggesting weak but potentially meaningful associations. However, none reach conventional thresholds for statistical significance. By contrast, LiveCodeBench displays the strongest relationships. Several metrics—including cyclomatic complexity, function calls, and length—show relatively high
R
2
R^{2}
values (up to
0.32
0.32
) alongside highly significant p-values (
<
10
−
6
<10^{-6}
), indicating robust linear associations with failure rate.
((a))
Cyclomatic Complexity
((b))
Length
((c))
Nesting Depth
((d))
Function Calls
Figure 1
:
Comparison of benchmark code metrics for tasks, grouped by the number of LLMs that failed them. LiveCodeBench shows a positive correlation between code complexity and failure rate, while other benchmarks do not.
RQ2:
To what extent are these failures explained by solution complexity?
Failures show only a weak association with solution code complexity across HumanEval, MBPP, and BCB-Hard. These results suggest that code complexity alone cannot systematically explain LLM failures across benchmarks, and that semantic task properties and benchmark-specific factors likely play a more significant role.
IV
Failure Inspection
We conducted a detailed task-by-task analysis of consistently failed tasks, examining the code generated by each model together with the corresponding failed test cases. This close inspection allowed us to uncover recurring patterns and better understand systematic challenges faced by LLMs across benchmarks.
LLM Failure Patterns:
Across the consistently failed tasks, we identified four main failure modes:
•
Wrong problem mapping
occurs when models interpret a task as belonging to the wrong problem class. For example, in
HumanEval/132
, the task is to determine whether a string of square brackets contains a valid subsequence with at least one nested pair. All models incorrectly mapped this to the standard ”balanced brackets” class of problems and applied a stack-based early-return strategy: pushing opening brackets, popping on closing brackets, and returning
True
as soon as a nested configuration was locally detected.
This approach failed because it identified only the first instance of nesting rather than ensuring that sufficient nesting occurred, as required by the canonical solution. This illustrates a common bias in LLMs toward familiar problem types, which can lead them to overlook details specified in the prompt.
•
Flawed or incomplete algorithm design
arises when LLMs take the correct approach but include a flawed or incomplete set of steps. For example, task
BCB-Hard/945
requires generating a time series of sales data starting from a specified date, using regression to forecast future sales. LLMs correctly implemented data processing and regression, but did not incorporate mechanisms to handle non-monotonic trends.
•
Edge case mishandling
refers to failures where the code generated by an LLM cannot correctly handle uncommon or boundary scenarios. For example,
BCB-Hard/964
requires converting files with multiple extensions from a source directory into CSV files in a target directory, but all models failed the nested subdirectory test case because their code only iterated over top-level files rather than recursively traversing subfolders.
•
Formatting mistakes
arise when the underlying algorithm is correct, but solutions are rejected because of strict input/output requirements. For instance,
LiveCodeBench/3736
required results to be returned as string literals (e.g.,
"23"
), whereas the models produced unquoted digits.
Table
IV
reports the number of patterns observed in each benchmark. In some tasks, more than one pattern appeared to contribute to the failures, as we analyzed the outputs from all LLMs, each producing different solution code.
TABLE IV
:
Number of failure patterns across benchmarks.
Failure Pattern
HumanEval
MBPP
LCB
BCB-Hard
Wrong Problem Mapping
1
0
20
24
Flawed/Incomplete Algorithm
0
1
31
35
Formatting Mistakes
0
0
10
32
Edge Case Mishandling
0
1
1
27
Ambiguous Prompt & Restricted Test:
Many failures in
BCB-Hard
arise from task ambiguity, where prompts are underspecified and tests are overspecified, forcing models to make reasonable assumptions that nonetheless lead to failure. For instance, models sometimes assumed specific column names in the output CSV, which the test cases did not expect. A task is passed only when a model’s assumptions happen to match the hidden expectations or when the generated code is flexible enough to satisfy alternative assumptions imposed by the tests.
Additionally, we investigated why Llama-3.3-70B outperformed other models on BCB-Hard, particularly Claude Sonnet-4, which demonstrated stronger performance across the remaining benchmarks. We did this by examining tasks that Llama-3.3-70B solved correctly while others failed. A closer examination of these tasks revealed that Llama’s success often stemmed from a simple or literal interpretation of the prompts, whereas stronger models tended to rely on conventional coding practices or added assumptions that were reasonable in general but not aligned with the benchmark’s strict test cases. For instance, in
BCB-Hard/147
, Claude Sonnet-4 skipped network and broadcast IP addresses following standard Python networking conventions, while Llama-3.3-70B iterated over all addresses literally as requested in the prompt. This may illustrate a broader phenomenon: more capable models can sometimes over-optimize for general correctness or practicality, inadvertently violating strict benchmark test cases, whereas simpler models may succeed by adhering more literally to the task instructions.
RQ3:
Which additional task characteristics, beyond solution complexity, influence LLM failures?
We identified four recurring failure patterns—
wrong problem mapping, flawed or incomplete algorithm design, edge case mishandling, and formatting mistakes
—that highlight current LLM weaknesses. Underspecified prompts, as well as overspecified tests in benchmark tasks, are additional factors contributing to further failures.
V
Limitations and Future Directions
In this section, we briefly discuss several limitations of our study and outline future directions:
(1)
Our experiments are currently limited to four benchmarks. We plan to extend them with further function-level as well as repository-level benchmarks, such as SWE-Bench
[
6
]
, which requires solving coding issues across multiple files.
(2)
We will broaden our study to cover a wide range of models, from small to large scale, to examine what types of failures arise with different architectures and sizes.
(3)
Our complexity measurement focuses on solution code, but it could be extended to include prompt complexity.
(4)
Recursion and the use of data structures are underrepresented across existing benchmarks. Future work could involve creating specialized benchmarks to address this gap.
(5)
Building on failure pattern insights (e.g., edge case handling and problem mapping), we plan to design targeted training strategies to improve LLM performance.
(6)
We also plan to design benchmarks based on common failure patterns to more effectively discriminate between model capabilities.
Acknowledgment
This work was funded by the Hessian Ministry of Higher Education, Research, Science and the Arts within the cluster project
The Third Wave of Artificial Intelligence
(3AI), by the National Research Center for Applied Cybersecurity ATHENE within the project
Foundational Models for Secure Software Development
, and by the LOEWE initiative (Hesse, Germany) [LOEWE/4a//519/05/00.002(0013)/95].
References
[1]
J. Ji, J. Jun, M. Wu, and R. Gelles, “Cybersecurity risks of ai-generated
code,” Center for Security and Emerging Technology, Tech. Rep., November
2024. [Online]. Available:
https://cset.georgetown.edu/wp-content/uploads/CSET-Cybersecurity-Risks-of-AI-Generated-Code.pdf
[2]
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan,
H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger,
M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder,
M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P.
Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss,
W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji,
S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra,
E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer,
P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and
W. Zaremba, “Evaluating large language models trained on code,” 2021.
[Online]. Available: https://arxiv.org/abs/2107.03374
[3]
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang,
C. Cai, M. Terry, Q. Le, and C. Sutton, “Program synthesis with large
language models,” 2021. [Online]. Available:
https://arxiv.org/abs/2108.07732
[4]
S. Jain, S. B. Kong, E. Zelikman, A. Chen, T. Chen, A. Svyatkovskiy, and
C. Sutton, “Livecodebench: Holistic and contamination-free evaluation of
llms for code,” 2024. [Online]. Available:
https://arxiv.org/abs/2404.00699
[5]
T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf,
H. Zhan, J. He, I. Paul, S. Brunner, C. Gong, T. Hoang, A. R. Zebaze,
X. Hong, W.-D. Li, J. Kaddour, M. Xu, Z. Zhang, P. Yadav, N. Jain, A. Gu,
Z. Cheng, J. Liu, Q. Liu, Z. Wang, B. Hui, N. Muennighoff, D. Lo, D. Fried,
X. Du, H. de Vries, and L. V. Werra, “Bigcodebench: Benchmarking code
generation with diverse function calls and complex instructions,” 2025.
[Online]. Available: https://arxiv.org/abs/2406.15877
[6]
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan,
“Swe-bench: Can language models resolve real-world github issues?” 2024.
[Online]. Available: https://arxiv.org/abs/2310.06770
[7]
J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is your code generated by chatgpt
really correct? rigorous evaluation of large language models for code
generation,” in
Proceedings of the 37th International Conference on
Neural Information Processing Systems
, ser. NIPS ’23. Red Hook, NY, USA: Curran Associates Inc., 2023.
[8]
Z. Yu, Y. Zhao, A. Cohan, and X.-P. Zhang, “Humaneval pro and mbpp pro:
Evaluating large language models on self-invoking code generation,” 2024.
[Online]. Available: https://arxiv.org/abs/2412.21199
[9]
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns,
S. Puranik, H. He, D. Song, and J. Steinhardt, “Measuring coding challenge
competence with apps,” 2021. [Online]. Available:
https://arxiv.org/abs/2105.09938
[10]
Z. Wang, Z. Zhou, D. Song, Y. Huang, S. Chen, L. Ma, and T. Zhang, “Towards
understanding the characteristics of code generation errors made by large
language models,” in
2025 IEEE/ACM 47th International Conference on
Software Engineering (ICSE)
. Los
Alamitos, CA, USA: IEEE Computer Society, May 2025, pp. 2587–2599. [Online].
Available:
https://doi.ieeecomputersociety.org/10.1109/ICSE55347.2025.00180