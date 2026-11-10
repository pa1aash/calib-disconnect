---
title: 1Introduction
id: 1introduction-3
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:27:16.683676Z'
updated: '2026-11-09T23:31:25.614031Z'
source: https://arxiv.org/html/2506.10056
source_domain: arxiv.org
fetched_at: '2026-11-09T23:27:16.683020Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Pareto-Optimal Code Generation (arXiv 2506.10056, full text): maps accuracy-throughput
  Pareto frontier of verifiers (full test suite, selective-execution filters, ORMs)
  on Python benchmarks; staged verification with ORMs gives 11.64x throughput for
  8.26% accuracy loss; Qwen-only generators and ORMs.'
---

1Introduction
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY-SA 4.0
arXiv:2506.10056v2 [cs.SE] 24 Feb 2026
marginparsep has been altered.
topmargin has been altered.
marginparpush has been altered.
The page layout violates the CONF style.
Please do not change the page layout, or include packages like geometry,
savetrees, or fullpage, which change it for you.
We’re not able to reliably undo arbitrary changes to the style. Please remove
the offending package(s), or layout-changing commands and try again.
Pareto Optimal Code Generation
Gabriel Orlanski
1
Nicholas Roberts
1
Aws Albarghouthi
1
Frederic Sala
1
†
†
footnotetext:
1
University of Wisconsin-Madison. Correspondence to: Gabriel Orlanski <gorlanski@cs.wisc.edu>.
Preprint. August 24, 2026.
Abstract
Generate-then-rank is the dominant test-time scaling (TTS) paradigm for code generation, but scaling accuracy by sampling and executing more candidates makes comprehensive verification a major computational bottleneck.
This creates an inherent trade-off between accuracy and compute that, despite its importance to TTS, is often ignored.
Specifically, faster but noisier signals, such as outcome reward models (ORMs), are dismissed as suboptimal.
We frame verifier selection as a Pareto optimization problem and empirically map the accuracy-throughput frontier across signals, including the full test suite, heuristics for selective execution, and ORMs, across four Python benchmarks.
We show that ORMs are most effective at optimizing the Pareto curve when pruning is used in the generate-then-rank pipeline–known as staged verification–where lightweight filters remove obviously incorrect solutions, including candidates with small syntactic or character-level bugs, before expensive verification.
Our pruning analysis shows that eliminating incorrect yet highly ranked candidates (often character-level bugs) prevents wasted compute on incorrect tokens.
We find that ORMs with staged verification shift the Pareto frontier outward, achieving 11.64x higher throughput at a cost of 8.26% accuracy relative to full test-suite verification.
1
Introduction
Figure 1:
Staged Verification Shifts the Pareto Frontier.
Each panel shows one generator size (500M to 14B) on CodeContests.
Red dashed
: non-staged verification.
Blue solid
: staged verification, which filters before ORM ranking.
Gold
×
\times
: full test suite. The shaded region shows gains from staging; the frontier shifts outward across all generator sizes.
Generate-then-rank has become the dominant paradigm for test-time scaling in code generation. The pipeline
generates
many candidates from a model,
verifies
each one against a test suite, and
returns
the highest-ranked correct solution. With hundreds or thousands of candidates, verification becomes the bottleneck. This is especially true for more comprehensive SWE-Bench
(
Jimenez et al., 2024
)
test suites, which cost orders of magnitude more than the much lighter-weight HumanEval
(
Chen et al., 2021
)
unit tests.
Recent work discards neural reward models when reliable test suites exist
(
DeepSeek-AI et al., 2025
;
Muennighoff et al., 2025
;
Lambert et al., 2025
)
, but this assumes verification cost is negligible relative to generation cost. As test suites grow more complex, this assumption breaks down.
This cost creates a fundamental tradeoff. Full test suites maximize correctness but bottleneck throughput; lightweight checks like compilation and partial execution maximize throughput but miss bugs. Outcome Reward Models (ORMs) offer a third option: neural rankers that score candidates in a single pass, with inference cost depending on candidate length rather than task complexity. These three approaches define a Pareto frontier of accuracy vs. throughput. However, where ORMs sit on this frontier relative to execution-based methods—and whether combining the two shifts the frontier outward—has not been studied.
The question is complicated by an asymmetry. Execution-based tradeoffs are
transparent
: using fewer tests predictably misses more bugs. ORM tradeoffs are
opaque
: these models can assign high scores to candidates with obvious defects, including arithmetic mistakes and logical errors in intermediate reasoning steps
(
Lightman et al., 2023
;
Wang et al., 2024
)
. Cheap execution filters catch precisely these failure modes. Prior work evaluates verifiers in isolation, reporting accuracy or throughput but not both, leaving the frontier unmapped
(
Inala et al., 2022
;
Zhang et al., 2022
;
Ni et al., 2023
;
Cobbe et al., 2021
;
Snell et al., 2024
)
.
We empirically map the accuracy-throughput frontier for code verification.
We focus on single-file Python benchmarks where verification cost already varies substantially; repository-scale tasks like SWE-Bench are future work. Our investigation spans three verification signals across four benchmarks: full test suites, partial test execution, and ORMs. We evaluate both standard generate-then-rank and
staged verification
, where lightweight filters remove obvious failures before ORM ranking (
Figure 2
).
Staged verification dominates naive ORM ranking across much of the frontier: filtering eliminates candidates with syntactic bugs that ORMs systematically over-rank, preventing wasted compute on incorrect solutions
(
Figure 1
).
Our contributions are as follows:
•
We map the accuracy-throughput frontier:
ORMs are 8.60
×
\times
faster than full test suites and 32.86% more accurate than majority voting.
•
We show staged verification shifts the frontier outward:
Filtering before ranking is 11.64
×
\times
faster and 8.26% less accurate than full test suites.
•
We characterize ORM failure modes and demonstrate that staged verification addresses them:
Gains stem from removing incorrect candidates that ORMs over-rank, particularly code with small syntactic bugs that preserve overall structure.
•
We show staged verification does not require careful test curation:
Random subsets of tests achieve false positive rates comparable to those of curated subsets, with low variance across selections.
We have also released code reproducing our experiments.
1
1
1
https://github.com/SprocketLab/orm-code-verifier
2
The Verification Pareto Frontier
This section formalizes the verification problem. We first define the metrics that characterize the Pareto frontier (
subsection 2.1
), then introduce staged verification as a strategy for combining cheap filters with neural rankers (
subsection 2.2
), and finally describe ORMs trained with the Bradley-Terry objective as fixed-cost verifiers (
subsection 2.3
).
Verification strategies occupy different points on an accuracy-throughput Pareto frontier. Strong verifiers (full test suites) maximize accuracy but bottleneck throughput; weak verifiers (syntax checks, partial execution) maximize throughput but sacrifice accuracy. ORMs offer fixed inference cost regardless of test suite complexity, but where they sit on this frontier—and whether combining them with lightweight filters can shift the frontier outward—remains unexplored. We focus on Python benchmarks with test-based verification; repository-scale tasks are future work.
Figure 2:
Comparison of verification strategies.
Normal ranking
runs all tests to produce a high-quality ordering but is slow, especially with a large test suite.
Staged verification
uses a weak verifier to filter obvious failures, then ranks survivors using an ORM.
2.1
Problem Setup
Given a programming problem
x
x
, a generator produces candidates
C
=
{
c
1
,
…
,
c
n
}
C=\{c_{1},\ldots,c_{n}\}
. Each candidate is scored by a verifier
V
V
, and the top-ranked candidate is returned. We assume each problem is associated with test cases that determine the correctness of a candidate, as is standard in competitive programming
(
Li et al., 2022
;
Jain et al., 2024
)
and software engineering benchmarks
(
Jimenez et al., 2024
)
.
Accuracy.
We measure ranking quality using Best-of-
k
k
(
Hosseini et al., 2024
, Bof
k
k
;)
: the probability that among
k
k
random candidates, the highest-ranked one is correct. Let
r
i
r_{i}
denote the rank
i
i
candidate and
𝟏
​
[
r
i
]
\mathbf{1}[r_{i}]
indicate correctness:
Bof
​
k
:=
1
(
n
k
)
​
∑
i
=
0
n
−
k
(
n
−
i
−
1
k
−
1
)
⋅
𝟏
​
[
r
i
​
is correct
]
.
\text{Bof}k:=\frac{1}{{n\choose k}}\sum_{i=0}^{n-k}{n-i-1\choose k-1}\cdot\mathbf{1}[r_{i}\text{ is correct}].
(1)
Throughput.
We measure the programs processed per second (PPS). Strong verifiers achieve high accuracy but low PPS; weak verifiers achieve high PPS but lower accuracy.
Verifiers.
The strongest verifier
V
all
V_{\text{all}}{}
(full test suite) runs all test cases and admits no false positives as a candidate that passes is correct. Weak verifiers
V
S
N
V_{S_{N}}
(first-
N
N
-tests) check only a subset of tests; they are fast but admit false positives. An outcome reward model
V
θ
V_{\theta}{}
(neural ranker) scores candidates without execution, offering constant-time inference regardless of test suite size.
2.2
Staged Verification
A program that fails
any
test is incorrect; a program that passes
all
tests is correct. This asymmetry motivates staged verification: use a cheap filter to eliminate obviously incorrect candidates before ranking survivors with an ORM. Removing candidates that can never be correct avoids wasted compute on ORM ranking and reduces possible spurious correlations, so with a sufficiently large ORM we would expect both accuracy and throughput improvements.
We use deliberately simple filters—compilation, linting, execution on the first
N
N
test cases—to isolate the interaction between filtering and neural ranking from the complexity of filter design. The pipeline is shown in
Figure 2
.
2.3
ORMs as Verifiers
Let
V
θ
V_{\theta}
be the verifier that uses the ORM with parameters
θ
\theta
to predict if
c
c
is correct. We denote its output as:
V
θ
​
(
c
∣
x
)
=
P
⁡
(
c
​
passes all tests
∣
x
,
c
)
.
V_{\theta}(c\mid x)=P(c\text{ passes all tests}\mid x,c).
(2)
We use a language model backbone with a scalar prediction head that outputs scores in
[
0
,
1
]
[0,1]
. Training uses pairs of candidates
(
c
w
,
c
ℓ
)
(c_{w},c_{\ell})
where
c
w
c_{w}
is correct and
c
ℓ
c_{\ell}
is incorrect. The Bradley-Terry objective
(
Bradley and Terry, 1952
;
Stiennon et al., 2020
)
maximizes the margin between correct and incorrect candidates. Formally, this objective is:
ℒ
RM
=
−
𝔼
(
x
,
c
w
,
c
ℓ
)
∼
𝒟
​
[
log
⁡
σ
⁡
(
V
θ
​
(
c
w
|
x
)
−
V
θ
​
(
c
ℓ
|
x
)
)
]
.
\mathcal{L}_{\text{RM}}=-\mathbb{E}_{(x,c_{w},c_{\ell})\sim\mathcal{D}}[\log\sigma(V_{\theta}{}(c_{w}|x)-V_{\theta}{}(c_{\ell}|x))].
(3)
At inference, the ORM scores each candidate in a single forward pass. Full training details are in
Appendix A
.
Why not process reward models?
Process reward models (PRMs) score individual reasoning steps rather than final outcomes
(
Lightman et al., 2023
;
Uesato et al., 2022
)
. We exclude PRMs for two reasons. First, step-level annotations are expensive. PRM800K required extensive human labeling
(
Lightman et al., 2023
)
, and automated alternatives remain an active research area
(
Wang et al., 2024
)
. Second, PRMs require scoring each step, resulting in multiple forward passes per candidate, directly undermining the throughput advantage that makes learned verifiers attractive. ORMs require only pass/fail labels and a single pass, making them practical for high-throughput verification.
3
Experimental Design
We train ORMs on CodeContests and GSM8K, then measure their accuracy and throughput across four benchmarks. In
subsection 3.1
we describe the data, training, and evaluation protocol. In
subsection 3.2
we detail the ranking strategies and weak filters under comparison.
3.1
Setup
Data.
We train ORMs on CodeContests-Python
(
Li et al., 2022
)
and GSM8K
(
Cobbe et al., 2021
)
in PAL format
(
Gao et al., 2022
)
. Training candidates are generated with Qwen 2.5 Coder Instruct 7B
(
Hui et al., 2024
)
using VLLM
(
Kwon et al., 2023
)
, sampling
128
128{}
times per problem with temperature
T
=
1.0
T{=}1.0
and
top
p
=
0.95
\text{top}_{p}{=}0.95
(
Holtzman et al., 2020
)
. We randomly sample up to 6 pairs per problem from 4.7K CodeContests and 7.3K GSM8K problems. For distribution shift evaluation, we use HumanEval
(
Chen et al., 2021
)
and MBPP
(
Austin et al., 2021
)
via EvalPlus
(
Liu et al., 2023
;
Liu et al., 2024
)
. All code is formatted using the Black formatter for standardization and to handle whitespace requirements.
To determine correctness, we follow existing works
(
Cassano et al., 2022
;
Orlanski et al., 2023
;
Jain et al., 2024
)
in using the subprocess
2
2
2
https://docs.python.org/3/library/subprocess.html
library to execute the programs with the test cases. For GSM8K, we check that the outputted scalar is correct using an assertion. In the case of CodeContests, we check that the program prints the correct output to STDOUT and stop execution on the first error. We detail our training data in
Table 4
. We filter out any programs with syntax errors as these could be caused by the model hitting the token limit rather than a poor generation.
Training.
An ORM does not necessarily need to be a language model, but given the strong overall results of prior work in using a language model as an ORM
(
Cobbe et al., 2021
)
, we choose to use these. We train with the Bradley-Terry objective (
Equation 3
), which models
P
⁡
(
c
w
≻
c
ℓ
)
P(c_{w}\succ c_{\ell})
for correct candidate
c
w
c_{w}
and incorrect candidate
c
ℓ
c_{\ell}
. Intuitively, this objective pushes
V
θ
​
(
c
w
|
x
)
V_{\theta}{}(c_{w}|x)
higher than
V
θ
​
(
c
ℓ
|
x
)
V_{\theta}{}(c_{\ell}|x)
by maximizing the margin between correct and incorrect candidates. At inference, the ORM scores any new candidate based on how likely it is to be preferred over incorrect solutions.
We train using Adam
(
Kingma and Ba, 2017
)
, cosine scheduling (peak
5
​
e
−
6
5\text{e}{-}6
, 10% warmup), batch size 64, and max sequence length 2048. We train for 2 epochs, use the final checkpoint, and average results over six random seeds. Both generators and ORM backbones are from the Qwen family. While this ensures compatibility, it may favor the ORM through distribution matching; we partially address this via distribution-shift evaluation on HumanEval and MBPP. Full hyperparameters are in
Appendix A
.
Evaluation.
CodeContests and GSM8K programs execute via subprocess with a 30s timeout
(
Cassano et al., 2022
;
Orlanski et al., 2023
)
. HumanEval and MBPP use EvalPlus
(
Liu et al., 2023
;
Liu et al., 2024
)
. All verifiers are run across 5 independent trials to mitigate runtime noise. We measure preprocessing, execution, and postprocessing time, excluding disk I/O.
V
θ
V_{\theta}{}
experiments use a single 48GB A6000 GPU with 16 cores and 64GB memory. Execution-only setups use 64 cores and 256GB for CodeContests. For the other datasets, we use 32 cores and 128GB memory. These configurations are roughly cost-equivalent according to the current prices per hour on AWS. We deduplicate candidates via exact string match after Black formatting, then weight outcomes by duplicate count for fair
Best-of-
​
k
\textrm{Best-of-}k
measurement.
ORM Inference.
We use dynamic batching akin to sequence packing
(
Raffel et al., 2020
)
: rather than fixed batch sizes bounded by outlier-length programs, we construct a batch by continuously adding candidates to the batch until the net tokens is over a threshold size. This establishes a fairer comparison to CPU methods as we are properly utilizing GPU memory and FLOPs. For the 500M ORM we set the max tokens per batch to 500,000 while for the 1.5B ORM we set the max tokens to 200,000.
3.2
Verification Methods
We evaluate the following three ranking strategies and three filtering methods that can precede ranking:
1.
Majority Voting:
Select the most common candidate after normalization with Black. Standard method for ranking sequences generated
(
Ehrlich et al., 2025
)
.
2.
𝐕
θ
\mathbf{V_{\theta}{}}
:
Score each candidate with the ORM and then select the highest-scoring candidate.
3.
𝐕
all
\mathbf{V_{\text{all}}{}}
:
Select the candidate passing the most tests.
Next, for experiments involving staged verification, we use the following heuristics as weak verifiers:
1.
𝐕
𝐜
\mathbf{V_{c}}
:
Remove candidates failing the syntax checker.
2.
𝐕
Lint
\mathbf{V_{\text{Lint}}{}}
:
Remove candidates with PyLint errors.
3.
𝐕
𝐒
𝐍
\mathbf{V_{S_{N}}}
:
Remove candidates failing the first
N
N
test cases within a timeout of 3 seconds.
We denote staged verification as
V
x
+
θ
V_{\text{x}+\theta}
where
x
x
is the filter. For example,
V
S
10
+
θ
V_{S_{10}+\theta}{}
filters with the first 10 tests, then ranks survivors with the ORM. For majority voting baselines, we rank by test cases passed with duplicate count as tiebreaker
(
Ehrlich et al., 2025
;
Li et al., 2022
)
.
4
Results
Table 1:
Overall results for the different pruning with a weak verifier then ranking methods. If Filter is “—” that means no pruning is done.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run. Rows with Ranker set to “MV” are verifier-only baselines that select using majority voting without ORM inference. “Syntax” and “Lint” remove any programs with the respective errors. “N Test” prunes out any programs that do not pass the first
N
N
test cases. The evaluation dataset is generated with Qwen 2.5 Coder 7B Instruct using
T
=
1.0
T=1.0
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens. The results are averaged over six random seeds.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
MV
2.55
64777.78
83.28
39596.93
84.21
48077.73
66.36
52179.55
500M
5.33
52.49
84.13
264.94
79.31
144.84
66.04
303.14
1.5B
6.34
22.53
87.05
113.79
81.37
64.14
69.70
133.17
Syntax
MV
2.55
6122.37
83.32
6256.05
84.22
6774.73
66.63
5679.06
500M
5.79
60.87
84.75
309.44
79.57
145.15
65.54
353.34
1.5B
6.58
25.09
88.09
127.63
82.37
66.88
70.92
149.13
Lint
MV
2.67
302.09
83.39
488.17
84.23
633.15
67.44
613.41
500M
5.34
47.56
84.30
156.85
79.26
101.10
66.37
166.69
1.5B
6.60
22.64
87.05
90.24
82.23
55.19
70.36
100.38
1 Test
MV
15.72
131.73
—
—
87.62
1020.54
76.07
930.69
500M
15.75
69.50
—
—
83.88
125.86
75.17
229.08
1.5B
16.86
58.35
—
—
85.98
63.32
77.04
132.52
10 Tests
MV
17.12
120.93
—
—
92.46
650.77
86.06
345.21
500M
17.54
73.22
—
—
90.01
134.92
85.19
169.30
1.5B
18.06
65.80
—
—
90.05
72.83
86.57
121.29
V
all
V_{\text{all}}{}
20.69
2.95
97.96
88.21
95.97
22.19
90.04
15.01
We first characterize when ORM-only ranking occupies favorable frontier points (
subsection 4.1
), then show how test-based filtering shifts the frontier further outward (
subsection 4.2
).
subsection 4.3
investigates why staging helps: ORMs systematically overrank candidates with subtle bugs that tests catch.
subsection 4.4
confirms that filtering effectiveness is robust to test choice, and
subsection 4.5
translates these findings into cost-accuracy trade-offs.
Figure 1
shows that staged verification shifts the Pareto frontier outward across generator sizes. ORMs occupy favorable frontier points (8.60
×
\times
faster than
V
all
V_{\text{all}}{}
, 32.86% more accurate than naive baselines) across datasets (
Table 1
) and generator sizes (
Table 2
). Staging improves on ORM-only points because lightweight filters remove incorrect candidates that ORMs systematically overrank. This benefit does not depend on specific test selection: random subsets achieve comparable false positive rates with low variance.
4.1
ORMs Occupy Favorable Frontier Points
Table 1
summarizes accuracy (Best-of-64) and throughput (PPS) across verification methods. Results are averaged over six random seeds with 95% confidence intervals; median CI width is 1.48 percentage points.
When full-suite execution is the bottleneck,
V
θ
V_{\theta}{}
achieves 8.60
×
\times
higher throughput than
V
all
V_{\text{all}}{}
while remaining more accurate than naive baselines (
Table 1
), making ORM-only ranking a practical frontier choice. When even partial execution is inexpensive, however, running a small number of tests provides reliable signal at low cost, and ORM-only points become less competitive. Smaller ORMs sharpen this trade-off: the 500M variant is 1.44
×
\times
faster than the 1.5B model with only a 4.99% accuracy loss.
ORM-only ranking is most compelling when execution is expensive; when even partial execution is cheap, ORM-only points become less competitive on the frontier.
4.2
Staged Verification Shifts the Frontier
Table 2:
Results for the different pruning then ranking on only CodeContests as we scale the size of the generator model. If Filter is “—” that means no pruning is done.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run. Rows with Ranker set to “MV” are verifier-only baselines that select using majority voting without ORM inference. “Syntax” and “Lint” remove any programs with the respective errors. “N Test” prunes out any programs that do not pass the first
N
N
test cases. The evaluation dataset is generated with Qwen 2.5 Coder Instruct models using
T
=
1.0
T=1.0
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens. The results are averaged over six random seeds.
500M
1.5B
3B
7B
14B
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
MV
0.00
65679.19
0.09
66369.90
1.87
64541.54
2.55
64777.78
2.21
62487.39
500M
0.47
68.39
1.64
67.79
4.52
64.02
5.33
52.49
10.99
59.83
1.5B
0.61
26.42
2.62
26.63
5.76
25.14
6.34
22.53
12.86
23.52
Syntax
MV
0.00
5642.49
0.09
5785.38
1.87
4972.95
2.55
6122.37
5.23
6432.92
500M
0.46
64.53
1.65
70.63
4.55
65.86
5.79
60.87
11.02
62.31
1.5B
0.58
27.16
2.67
28.25
5.68
25.56
6.58
25.09
13.03
24.61
Lint
MV
0.00
523.78
0.10
550.65
1.92
548.99
2.67
302.09
5.25
459.62
500M
0.47
62.47
1.55
58.69
4.31
51.05
5.34
47.56
7.89
44.11
1.5B
0.67
31.28
2.62
27.19
5.47
23.45
6.60
22.64
8.90
20.01
1 Test
MV
1.39
126.19
4.92
124.94
9.65
122.58
15.72
131.73
22.76
132.92
500M
1.71
79.64
5.64
74.06
10.93
66.69
15.75
69.50
24.47
66.16
1.5B
2.02
74.27
5.60
67.36
11.39
58.02
16.86
58.35
25.52
52.46
10 Tests
MV
1.65
125.65
5.73
122.34
12.16
116.15
17.12
120.93
25.83
120.53
500M
1.76
87.47
5.95
79.18
12.67
70.78
17.54
73.22
28.02
67.14
1.5B
2.15
82.33
5.75
73.53
13.04
64.18
18.06
65.80
28.10
57.46
V
all
V_{\text{all}}{}
2.16
3.32
7.83
2.23
14.92
2.54
20.69
2.95
31.98
3.65
Table 2
shows results across generators. Syntax and lint filtering remove only 1.30% and 2.62% of candidates on average as shown in
Table 8
. The filtering overhead exceeds inference savings, decreasing throughput by 10.42
×
\times
for the 500M ORM and 4.24
×
\times
for the 1.5B. Test-based filtering changes the picture: on CodeContests,
V
S
10
V_{S_{10}}
removes 90% to 97% of candidates, shifting the cost balance so that
V
S
N
+
θ
V_{S_{N}+\theta}{}
delivers 12.41
×
\times
higher throughput than
V
all
V_{\text{all}}{}
.
The best configuration,
V
S
10
+
θ
V_{S_{10}+\theta}{}
with the 1.5B ORM, is 10.22
×
\times
faster than
V
all
V_{\text{all}}{}
while losing only 7.58% accuracy.
Staged verification is not purely a speed optimization, as accuracy
improves
alongside throughput: the 500M ORM sees a 45.15% rise in
Best-of-
​
64
\textrm{Best-of-}64
and the 1.5B a 38.09% rise over their unfiltered counterparts because
test filtering removes candidates the ORM would have misranked
. On CodeContests, the 1.5B ORM with
V
S
10
+
θ
V_{S_{10}+\theta}{}
achieves 18.06% with 95% CI of [17.67, 18.45]. These accuracy gains of 12+ points over ORM-only exceed CI widths by roughly 15
×
\times
.
These patterns hold across generator sizes and sampling temperatures. With the 14B generator,
V
S
10
+
θ
V_{S_{10}+\theta}{}
yields 8.65
×
\times
speedup at 7.64% accuracy loss. Temperature ablations show average throughput of 146.40
±
\pm
68.97 and 89.28
±
\pm
33.49 PPS for the 500M and 1.5B ORMs, which is 13.44
×
\times
faster than
V
all
V_{\text{all}}{}
while accuracy degrades by only 8.80 points. Throughput CIs are tight for CodeContests at less than 1% of mean and moderate for HumanEval/MBPP at 3–10%. The latter use EvalPlus, which executes code via
eval
rather than subprocess, introducing additional runtime variance. Reported speedups exceed CI widths by 10
×
\times
or more. ORMs remain most useful when partial execution has high fixed costs like environment setup or container launch, or when filtering leaves a large ambiguous survivor set.
We find that staged verification shifts the Pareto frontier outward, with
V
S
10
+
θ
V_{S_{10}+\theta}{}
achieving near-
V
all
V_{\text{all}}{}
accuracy at an order of magnitude higher throughput.
4.3
ORMs Systematically Overrank Small Bugs
Figure 3:
Distribution of filtered candidates by ORM rank. Rank 1 is the top-ranked candidate; rank 128 is the lowest. Rows are filters; columns are datasets. Results shown for the 1.5B ORM; the 500M ORM graph is in
Figure 6
.
We do not retrain the ORM after filtering; the only way to improve
Best-of-
​
k
\textrm{Best-of-}k
is to remove incorrect candidates that the ORM ranked too highly. In
Figure 3
we show where the filtered candidates fall in the ORM ranking.
Syntax-filtered candidates cluster at the bottom (mean rank 96.72 out of 128, placing them in the lowest quartile). Removing candidates the ORM already dislikes changes little. Test-filtered candidates tell a different story: mean rank 65.29, a shift of 31 positions toward the top. These are incorrect candidates the ORM ranked in the middle or higher; removing them directly improves accuracy. Filtering also stabilizes results: with
V
S
10
+
θ
V_{S_{10}+\theta}{}
,
Best-of-
​
64
\textrm{Best-of-}64
standard deviation drops by 23.23% (500M) and 31.23% (1.5B).
What bugs do ORMs miss?
We analyze candidates the ORM ranked in its top-16 but
V
S
1
V_{S_{1}}
filtered. Comparing pattern prevalence in these “overrated” candidates versus correct ones reveals which bugs ORMs fail to penalize.
Table 3:
Bug patterns the ORM fails to penalize. Freq is overall pattern prevalence in problems with at least one passing solution; Top-16 is the percentage of solutions in the top-16 ORM-rated selections containing the pattern.
CodeContests
Pattern
Freq
Top-16
sorted()
w/o key
4.8%
2.5%
/
instead of
//
2.9%
3.4%
.remove()
in loop
1.3%
2.1%
Large number ops
1.1%
0.8%
while len()
0.7%
0.8%
HumanEval + MBPP
Pattern
Freq
Top-16
/
instead of
//
3.8%
3.3%
sorted()
w/o key
2.1%
3.7%
/2
in binary search
1.5%
0.7%
(a+b)/2
midpoint
0.6%
0.3%
Three patterns are 20 to 46
×
\times
more common in overrated candidates:
while len(x)
loops (46
×
\times
enrichment), large integer arithmetic (40
×
\times
), and
.remove()
inside iteration (22
×
\times
).
Table 3
confirms the mechanism: these patterns appear at similar rates in the full candidate pool and in the ORM’s top-16 selections.
These bugs share a property: they preserve surface form. Float division (
/
) and integer division (
//
) differ by one character.
int(x/2)
and
x//2
look similar but behave differently for negative numbers. ORMs trained on correctness labels see similar token sequences and assign similar scores; a single test catches the runtime difference.
Test-based filtering catches bugs the ORM misses, particularly single-character errors that preserve surface form but fail at runtime. Filtered candidates sat 31 ranks too high on average; removing them shifts the frontier.
4.4
Robustness to Test Selection
How sensitive is filtering effectiveness to which tests are selected? If there are large discrepancies between the discriminative power of test cases, then using staged verification for code generation is not generalizable. We investigate the false-positive rate (FPR) of test cases on CodeContests to determine if our previously discussed results are an artifact of lucky test selection. To do this, we profile the test execution time of generated solutions for CodeContests with the 1.5B and 3B Qwen 2.5 Coder Instruct generated solutions.
3
3
3
The 7B and 14B generated solutions continuously caused our 64 core/256GB to hang indefinitely with the additional profiling.
We run each test case five times with the solution and measure its mean wall time to run in isolation.
Figure 4:
False positive rate and cumulative time for random test subsets (top: 1.5B, bottom: 3B). Error bars show within-problem standard deviation across subset selections.
In
Figure 4
we show that test selection has minimal impact. At
k
=
1
k=1
, mean FPR is 86.3% (1.5B) and 79.6% (3B), with low variance across test choices (error bars). At
k
=
10
k=10
, mean FPR drops to 60.1% in 0.71 s (1.5B) and 51.2% in 0.62 s (3B). Incorrect LLM-generated code tends to fail broadly rather than on specific edge cases—any single test is roughly as effective as any other. We conclude that the filtering benefit is not be an artifact of test ordering, but a generalizable property of LLM bug distributions.
Our error bars show within-problem standard deviations across five random subsets. For FPR, this is 3.3 and 3.1 percentage points (1.5B/3B) at
k
=
1
k=1
, and 4.8 and 4.0 points at
k
=
10
k=10
, corresponding to 95% confidence intervals of roughly
±
\pm
4–6 points. This suggests more efficient test-suite verification techniques than running a full test suite on all candidates—e.g. filtering with a small random subset of tests and running the full suite on the candidates that survive the filter—which we leave as a promising future direction.
We find staged verification to not require careful test curation, as random test subsets achieve comparable false positive rates with low variance.
4.5
Practical Implications
Our findings enable cost-accuracy Pareto frontiers based on cloud provider pricing (
Table 7
); in
Figure 5
we show this frontier for CodeContests, where
V
S
10
+
θ
V_{S_{10}+\theta}{}
is Pareto-optimal, achieving near-
V
all
V_{\text{all}}{}
accuracy at a fraction of the cost.
We translate throughput to dollars using on-demand prices (January 22, 2026) and the hardware configurations in
section 3
. For CodeContests (
n
=
128
n{=}128
), costs per 100k programs form three tiers: majority voting baselines cost $0.63–$0.69, staged ORM verification costs $1.3–$2.4, and
V
all
V_{\text{all}}{}
costs $28. Staged verification is 12–22
×
\times
cheaper than
V
all
V_{\text{all}}{}
while recovering most of its accuracy. Moving from 1 to 10 tests adds only $0.06 but gains 1.40% absolute accuracy.
Figure 5:
Cost-accuracy Pareto frontier for Qwen 2.5 Coder Instruct models on CodeContests.
Top: 7B; bottom: 14B. Lines show Pareto curves for
non-staged
,
1-test
, and
10-test
. Costs are per 100k programs (log scale).
Costs are stable across generator sizes: verifier-only PPS ranges 122.6–132.9 for 1 test and 116.2–125.7 for 10 tests (
Table 2
). Cost estimates have tight 95% CIs—the 10-test baseline costs $0.69 (CI: $0.68–$0.70)—indicating throughput variance contributes negligibly to cost uncertainty compared to provider choice.
Staged verification is 12–22
×
\times
cheaper than full test-suite verification while recovering most of its accuracy, making it the Pareto-optimal choice for budget-constrained verification.
5
Related Work
Verification cost in code generation.
Execution-based evaluation is now standard in code benchmarks, from unit-test style tasks such as HumanEval and MBPP to larger suites such as APPS
(
Chen et al., 2021
;
Austin et al., 2021
;
Hendrycks et al., 2021
)
. More recently, repository-scale settings such as SWE-Bench require environment setup and running a test suite per candidate, making verification a dominant cost in test-time scaling
(
Jimenez et al., 2024
;
Li et al., 2024
;
Miserendino et al., 2025
;
Orlanski et al., 2025
)
.
Learned verifiers for selection.
Reward models, popularized by RLHF, are widely used for test-time selection (ORMs) and step-level evaluation (PRMs), and recent work also studies generative verification via LLM reasoning
(
Stiennon et al., 2020
;
Ouyang et al., 2022
;
Lightman et al., 2023
;
Wang et al., 2024
;
Zhang et al., 2024
)
. The closest work to ours is
Singhi et al. (2025)
, which studies when to sample more versus verify with an LLM; in contrast, we map the
accuracy–throughput
frontier for code verification and study how execution filters and ORMs interact.
Ranking programs.
A substantial line of work studies how to rank or rerank generated code candidates using execution signals, learned rankers, or auxiliary LLM-based reviewers
(
Inala et al., 2022
;
Ni et al., 2023
;
Sun et al., 2024
;
Zhang et al., 2022
;
Zhong et al., 2024
)
. Compared to these works, we emphasize the compute dimension by reporting accuracy and throughput across verifiers, and analyze how lightweight execution filters complement neural rankers.
Staged filtering and budgeted verification.
Staging verification—using cheap checks to reduce the number of candidates that reach more expensive validation—is common in software engineering workflows. Related ideas appear in automated program repair, where many candidate patches are generated and validated against test suites
(
Jiang et al., 2023
)
, and in work that reduces patch-validation cost or expensive test execution via prioritization and test selection
(
Benton et al., 2022
;
Chen and Zhang, 2020
;
Lou et al., 2021
;
Yuan et al., 2022
)
. Similar cost–accuracy trade-offs also appear in multi-stage code generation systems that use cascades or budgeted selection
(
Chen et al., 2024
;
Ehrlich et al., 2025
)
. Our focus is on how combining lightweight execution filters with neural ranking shifts and optimizes the
accuracy–throughput
Pareto frontier.
6
Conclusion
Progress in verification for test-time scaling should be measured by Pareto improvement: moving the accuracy–throughput frontier outward. Our results show that the most consistent Pareto gains come from a simple staged verification pipeline of cheap filtering followed by ORM ranking—which achieves 11.64
×
\times
higher throughput with 8.26% lower accuracy than full test-suite verification. The need for the filter comes from a recurring ORM error mode: ORMs over-score near-miss programs whose tokens look right but fail on basic runtime semantics, such as division operator slips and mutation during iteration, placing filtered failures about 31 ranks too high on average. Future work should target this failure mode directly and test whether the same frontier shifts appear when verification is dominated by much more substantial repository-scale overhead.
Limitations.
While our motivation includes repository-scale verification such as SWE-Bench, our experiments focus on single-file Python benchmarks. We therefore do not measure costs that can dominate end-to-end verification at much larger scales, including container startup, dependency installation, and integration testing; we leave the evaluation of staged verification in such settings to future work.
Our generators and ORMs also share a common model family—Qwen—which may bias results.
As additional powerful open weights models are released, the effects of varying the choice model family should be evaluated in future work.
Additionally, results may differ under larger distribution shifts across languages, domains, or other aspects of the training pipeline.
The dollar-cost analysis in
Table 7
depends on specific hardware and cloud pricing assumptions; while these affect absolute costs, the empirical accuracy–throughput frontier is measured directly.
Impact Statement
Staged verification reduces compute costs for large-scale code generation by pruning incorrect candidates before expensive validation. However, treating lightweight filters as a substitute for thorough testing could increase the risk of deploying incorrect or insecure code, and lowering verification costs may amplify harmful uses of high-volume generation. We emphasize that staged verification is a selection tool, not a replacement for full test suites. Sandboxed execution and human review remain essential before deployment.
References
Allal
et al.
(2025)
L. B. Allal, N. Muennighoff, L. K. Kumar Umapathi, B. Lipkin, and L. von Werra
Bigcode-project/bigcode-evaluation-harness
.
BigCode Project
.
Note:
original-date: 2022-08-09T12:58:56Z
External Links:
Link
Cited by:
Appendix F
.
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton
Program Synthesis with Large Language Models
.
arXiv
.
Note:
arXiv:2108.07732 [cs]
External Links:
Link
,
Document
Cited by:
§3.1
,
§5
.
Benton
et al.
(2022)
S. Benton, Y. Xie, L. Lu, M. Zhang, X. Li, and L. Zhang
Towards boosting patch execution on-the-fly
.
In
Proceedings of the 44th International Conference on Software Engineering
,
ICSE ’22
,
New York, NY, USA
,
pp. 2165–2176
.
External Links:
ISBN 9781450392211
,
Link
,
Document
Cited by:
§5
.
Bradley and Terry (1952)
R. A. Bradley and M. E. Terry
Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons
.
Biometrika
39
(
3/4
),
pp. 324–345
.
Note:
Publisher: [Oxford University Press, Biometrika Trust]
External Links:
ISSN 0006-3444
,
Link
,
Document
Cited by:
§2.3
.
Cassano
et al.
(2022)
F. Cassano, J. Gouwar, D. Nguyen, S. Nguyen, L. Phipps-Costin, D. Pinckney, M. Yee, Y. Zi, C. J. Anderson, M. Q. Feldman, A. Guha, M. Greenberg, and A. Jangda
MultiPL-E: A Scalable and Extensible Approach to Benchmarking Neural Code Generation
.
arXiv
.
Note:
arXiv:2208.08227 [cs]
External Links:
Link
,
Document
Cited by:
§3.1
,
§3.1
.
Center for High Throughput Computing (2006)
Center for High Throughput Computing
Center for high throughput computing
.
Center for High Throughput Computing
.
External Links:
Document
,
Link
Cited by:
Appendix E
.
Chen
et al.
(2024)
B. Chen, M. Zhu, B. Dolan-Gavitt, M. Shafique, and S. Garg
Model cascading for code: a cascaded black-box multi-model framework for cost-efficient code completion with self-testing
.
2025 International Joint Conference on Neural Networks (IJCNN)
,
pp. 1–9
.
External Links:
Link
Cited by:
§5
.
Chen and Zhang (2020)
L. Chen and L. Zhang
Fast and precise on-the-fly patch validation for all
.
2021 IEEE/ACM 43rd International Conference on Software Engineering (ICSE)
,
pp. 1123–1134
.
External Links:
Link
Cited by:
§5
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba
Evaluating Large Language Models Trained on Code
.
arXiv
.
Note:
arXiv:2107.03374 [cs]
External Links:
Link
,
Document
Cited by:
§1
,
§3.1
,
§5
.
Cobbe
et al.
(2021)
K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and J. Schulman
Training Verifiers to Solve Math Word Problems
.
arXiv
.
Note:
arXiv:2110.14168 [cs]
External Links:
Link
,
Document
Cited by:
Appendix F
,
§1
,
§3.1
,
§3.1
.
Dao (2023)
T. Dao
FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
.
arXiv
.
Note:
arXiv:2307.08691 [cs]
External Links:
Link
,
Document
Cited by:
§A.1
.
DeepSeek-AI
et al.
(2025)
DeepSeek-AI, D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao, Z. Li, Z. Gao, A. Liu, B. Xue, B. Wang, B. Wu, B. Feng, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, D. Dai, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Bao, H. Xu, H. Wang, H. Ding, H. Xin, H. Gao, H. Qu, H. Li, J. Guo, J. Li, J. Wang, J. Chen, J. Yuan, J. Qiu, J. Li, J. L. Cai, J. Ni, J. Liang, J. Chen, K. Dong, K. Hu, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Zhao, L. Wang, L. Zhang, L. Xu, L. Xia, M. Zhang, M. Zhang, M. Tang, M. Li, M. Wang, M. Li, N. Tian, P. Huang, P. Zhang, Q. Wang, Q. Chen, Q. Du, R. Ge, R. Zhang, R. Pan, R. Wang, R. J. Chen, R. L. Jin, R. Chen, S. Lu, S. Zhou, S. Chen, S. Ye, S. Wang, S. Yu, S. Zhou, S. Pan, S. S. Li, S. Zhou, S. Wu, S. Ye, T. Yun, T. Pei, T. Sun, T. Wang, W. Zeng, W. Zhao, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, W. L. Xiao, W. An, X. Liu, X. Wang, X. Chen, X. Nie, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yang, X. Li, X. Su, X. Lin, X. Q. Li, X. Jin, X. Shen, X. Chen, X. Sun, X. Wang, X. Song, X. Zhou, X. Wang, X. Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. Zhang, Y. Xu, Y. Li, Y. Zhao, Y. Sun, Y. Wang, Y. Yu, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Ou, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Xiong, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. X. Zhu, Y. Xu, Y. Huang, Y. Li, Y. Zheng, Y. Zhu, Y. Ma, Y. Tang, Y. Zha, Y. Yan, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Xie, Z. Zhang, Z. Hao, Z. Ma, Z. Yan, Z. Wu, Z. Gu, Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Pan, Z. Huang, Z. Xu, Z. Zhang, and Z. Zhang
DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
.
arXiv
.
Note:
arXiv:2501.12948 [cs]
External Links:
Link
,
Document
Cited by:
§1
.
Ehrlich
et al.
(2025)
R. Ehrlich, B. Brown, J. Juravsky, R. Clark, C. Ré, and A. Mirhoseini
CodeMonkeys: Scaling Test-Time Compute for Software Engineering
.
arXiv
.
Note:
arXiv:2501.14723 [cs]
External Links:
Link
,
Document
Cited by:
item 1
,
§3.2
,
§5
.
Frantar
et al.
(2023)
E. Frantar, S. Ashkboos, T. Hoefler, and D. Alistarh
GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers
.
arXiv
.
Note:
arXiv:2210.17323 [cs]
External Links:
Link
,
Document
Cited by:
Appendix F
.
Gao
et al.
(2022)
L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig
PAL: Program-aided Language Models
.
ArXiv
abs/2211.10435
.
External Links:
Link
Cited by:
Appendix F
,
§3.1
.
Hendrycks
et al.
(2021)
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. X. Song, and J. Steinhardt
Measuring Coding Challenge Competence With APPS
.
ArXiv
abs/2105.09938
.
External Links:
Link
Cited by:
§5
.
Holtzman
et al.
(2020)
A. Holtzman, J. Buys, L. Du, M. Forbes, and Y. Choi
The Curious Case of Neural Text Degeneration
.
arXiv
.
Note:
arXiv:1904.09751 [cs]
External Links:
Link
,
Document
Cited by:
§3.1
.
Hosseini
et al.
(2024)
A. Hosseini, X. Yuan, N. Malkin, A. Courville, A. Sordoni, and R. Agarwal
V-STaR: Training Verifiers for Self-Taught Reasoners
.
arXiv
.
Note:
arXiv:2402.06457 [cs]
External Links:
Link
,
Document
Cited by:
§2.1
.
Hui
et al.
(2024)
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu, K. Dang, Y. Fan, Y. Zhang, A. Yang, R. Men, F. Huang, B. Zheng, Y. Miao, S. Quan, Y. Feng, X. Ren, X. Ren, J. Zhou, and J. Lin
Qwen2.5-Coder Technical Report
.
arXiv
.
Note:
arXiv:2409.12186 [cs]
External Links:
Link
,
Document
Cited by:
Appendix F
,
§3.1
.
Inala
et al.
(2022)
J. P. Inala, C. Wang, M. Yang, A. Codas, M. Encarnación, S. K. Lahiri, M. Musuvathi, and J. Gao
Fault-Aware Neural Code Rankers
.
(
en
).
External Links:
Link
Cited by:
§1
,
§5
.
Jain
et al.
(2024)
N. Jain, K. Han, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica
LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code
.
arXiv
.
Note:
arXiv:2403.07974 [cs]
External Links:
Link
,
Document
Cited by:
Appendix F
,
§2.1
,
§3.1
.
Jiang
et al.
(2023)
N. Jiang, T. Lutellier, Y. Lou, L. Tan, D. Goldwasser, and X. Zhang
KNOD: domain knowledge distilled tree decoder for automated program repair
.
2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)
,
pp. 1251–1263
.
External Links:
Link
Cited by:
§5
.
Jimenez
et al.
(2024)
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan
SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
.
arXiv
.
Note:
arXiv:2310.06770 [cs]
External Links:
Link
,
Document
Cited by:
§1
,
§2.1
,
§5
.
Kingma and Ba (2017)
D. P. Kingma and J. Ba
Adam: A Method for Stochastic Optimization
.
arXiv
.
Note:
arXiv:1412.6980 [cs]
External Links:
Link
,
Document
Cited by:
§A.1
,
§3.1
.
Kwon
et al.
(2023)
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica
Efficient Memory Management for Large Language Model Serving with PagedAttention
.
arXiv
.
Note:
arXiv:2309.06180 [cs]
External Links:
Link
,
Document
Cited by:
Appendix F
,
§3.1
.
Lambert
et al.
(2025)
N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu, Y. Gu, S. Malik, V. Graf, J. D. Hwang, J. Yang, R. L. Bras, O. Tafjord, C. Wilhelm, L. Soldaini, N. A. Smith, Y. Wang, P. Dasigi, and H. Hajishirzi
Tulu 3: Pushing Frontiers in Open Language Model Post-Training
.
arXiv
.
Note:
arXiv:2411.15124 [cs]
External Links:
Link
,
Document
Cited by:
§1
.
Lhoest
et al.
(2021)
Q. Lhoest, A. V. d. Moral, Y. Jernite, A. Thakur, P. v. Platen, S. Patil, J. Chaumond, M. Drame, J. Plu, L. Tunstall, J. Davison, M. Šaško, G. Chhablani, B. Malik, S. Brandeis, T. L. Scao, V. Sanh, C. Xu, N. Patry, A. McMillan-Major, P. Schmid, S. Gugger, C. Delangue, T. Matussière, L. Debut, S. Bekman, P. Cistac, T. Goehringer, V. Mustar, F. Lagunas, A. M. Rush, and T. Wolf
Datasets: A Community Library for Natural Language Processing
.
arXiv
.
Note:
arXiv:2109.02846 [cs]
External Links:
Link
,
Document
Cited by:
§A.1
.
Li
et al.
(2024)
J. Li, G. Li, Y. Zhao, Y. Li, H. Liu, H. Zhu, L. Wang, K. Liu, Z. Fang, L. Wang, J. Ding, X. Zhang, Y. Zhu, Y. Dong, Z. Jin, B. Li, F. Huang, and Y. Li
DevEval: a manually-annotated code generation benchmark aligned with real-world code repositories
.
In
Annual Meeting of the Association for Computational Linguistics
,
External Links:
Link
Cited by:
§5
.
Li
et al.
(2022)
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy, C. d. M. d’Autume, I. Babuschkin, X. Chen, P. Huang, J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S. Robson, P. Kohli, N. d. Freitas, K. Kavukcuoglu, and O. Vinyals
Competition-Level Code Generation with AlphaCode
.
Science
378
(
6624
),
pp. 1092–1097
.
Note:
arXiv:2203.07814 [cs]
External Links:
ISSN 0036-8075, 1095-9203
,
Link
,
Document
Cited by:
Appendix F
,
§2.1
,
§3.1
,
§3.2
.
Lightman
et al.
(2023)
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
Let’s Verify Step by Step
.
arXiv
.
Note:
arXiv:2305.20050 [cs]
External Links:
Link
,
Document
Cited by:
§1
,
§2.3
,
§5
.
Liu
et al.
(2023)
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation
.
arXiv
.
Note:
arXiv:2305.01210 [cs]
External Links:
Link
Cited by:
§3.1
,
§3.1
.
Liu
et al.
(2024)
J. Liu, S. Xie, J. Wang, Y. Wei, Y. Ding, and L. Zhang
Evaluating Language Models for Efficient Code Generation
.
arXiv
.
Note:
arXiv:2408.06450 [cs]
External Links:
Link
,
Document
Cited by:
§3.1
,
§3.1
.
Lou
et al.
(2021)
Y. Lou, J. Yang, S. Benton, D. Hao, L. Tan, Z. Chen, L. Zhang, and L. Zhang
When automated program repair meets regression testing—an extensive study on two million patches
.
ACM Transactions on Software Engineering and Methodology
33
,
pp. 1 – 23
.
External Links:
Link
Cited by:
§5
.
Miserendino
et al.
(2025)
S. Miserendino, M. Wang, T. Patwardhan, and J. Heidecke
SWE-lancer: can frontier llms earn $1 million from real-world freelance software engineering?
.
ArXiv
abs/2502.12115
.
External Links:
Link
Cited by:
§5
.
Muennighoff
et al.
(2025)
N. Muennighoff, Z. Yang, W. Shi, X. L. Li, L. Fei-Fei, H. Hajishirzi, L. Zettlemoyer, P. Liang, E. Candès, and T. Hashimoto
S1: Simple test-time scaling
.
arXiv
.
Note:
arXiv:2501.19393 [cs]
External Links:
Link
,
Document
Cited by:
§1
.
Ni
et al.
(2023)
A. Ni, S. Iyer, D. Radev, V. Stoyanov, W. Yih, S. I. Wang, and X. V. Lin
LEVER: Learning to Verify Language-to-Code Generation with Execution
.
arXiv
(
en
).
Note:
arXiv:2302.08468 [cs]
External Links:
Link
Cited by:
§1
,
§5
.
Orlanski
et al.
(2025)
G. Orlanski, D. Roy, A. Yun, C. Shin, A. Gu, A. Ge, D. Adila, A. Albarghouthi, and F. Sala
SlopCodeBench: Measuring Code Erosion Under Iterative Specification Refinement
.
External Links:
Document
,
Link
Cited by:
§5
.
Orlanski
et al.
(2023)
G. Orlanski, K. Xiao, X. Garcia, J. Hui, J. Howland, J. Malmaud, J. Austin, R. Singh, and M. Catasta
Measuring The Impact Of Programming Language Distribution
.
arXiv
.
Note:
arXiv:2302.01973 [cs]
External Links:
Link
,
Document
Cited by:
§3.1
,
§3.1
.
Ouyang
et al.
(2022)
L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. E. Miller, M. Simens, A. Askell, P. Welinder, P. F. Christiano, J. Leike, and R. J. Lowe
Training language models to follow instructions with human feedback
.
ArXiv
abs/2203.02155
.
External Links:
Link
Cited by:
§5
.
Raffel
et al.
(2020)
C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu
Exploring the limits of transfer learning with a unified text-to-text transformer
.
Journal of Machine Learning Research
21
(
140
),
pp. 1–67
.
External Links:
Link
Cited by:
§3.1
.
Singhi
et al.
(2025)
N. Singhi, H. Bansal, A. Hosseini, A. Grover, K. Chang, M. Rohrbach, and A. Rohrbach
When To Solve, When To Verify: Compute-Optimal Problem Solving and Generative Verification for LLM Reasoning
.
External Links:
Link
Cited by:
§5
.
Snell
et al.
(2024)
C. Snell, J. Lee, K. Xu, and A. Kumar
Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
.
arXiv
.
Note:
arXiv:2408.03314 [cs]
External Links:
Link
,
Document
Cited by:
§1
.
Stiennon
et al.
(2020)
N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss, A. Radford, D. Amodei, and P. F. Christiano
Learning to summarize with human feedback
.
In
Advances in Neural Information Processing Systems
,
Vol.
33
,
pp. 3008–3021
.
External Links:
Link
Cited by:
§2.3
,
§5
.
Sun
et al.
(2024)
Z. Sun, Y. Wan, J. Li, H. Zhang, Z. Jin, G. Li, and C. Lyu
Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates
.
Note:
Publisher: arXiv
Version Number: 3
External Links:
Link
,
Document
Cited by:
§5
.
Uesato
et al.
(2022)
J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang, A. Creswell, G. Irving, and I. Higgins
Solving math word problems with process- and outcome-based feedback
.
Note:
Publisher: arXiv
Version Number: 1
External Links:
Link
,
Document
Cited by:
§2.3
.
Wang
et al.
(2024)
P. Wang, L. Li, Z. Shao, R. X. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui
Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations
.
arXiv
.
Note:
arXiv:2312.08935 [cs]
External Links:
Link
,
Document
Cited by:
§1
,
§2.3
,
§5
.
Wolf
et al.
(2020)
T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi, P. Cistac, T. Rault, R. Louf, M. Funtowicz, J. Davison, S. Shleifer, P. v. Platen, C. Ma, Y. Jernite, J. Plu, C. Xu, T. L. Scao, S. Gugger, M. Drame, Q. Lhoest, and A. M. Rush
HuggingFace’s Transformers: State-of-the-art Natural Language Processing
.
arXiv
.
Note:
arXiv:1910.03771 [cs]
External Links:
Link
,
Document
Cited by:
§A.1
.
Yuan
et al.
(2022)
W. Yuan, Q. Zhang, T. He, C. Fang, N. Q. V. Hung, X. Hao, and H. Yin
CIRCLE: continual repair across programming languages
.
In
Proceedings of the 31st ACM SIGSOFT International Symposium on Software Testing and Analysis
,
ISSTA 2022
,
New York, NY, USA
,
pp. 678–690
.
External Links:
ISBN 9781450393799
,
Link
,
Document
Cited by:
§5
.
Zhang
et al.
(2024)
L. Zhang, A. Hosseini, H. Bansal, M. Kazemi, A. Kumar, and R. Agarwal
Generative Verifiers: Reward Modeling as Next-Token Prediction
.
arXiv
.
Note:
arXiv:2408.15240
External Links:
Link
,
Document
Cited by:
§5
.
Zhang
et al.
(2022)
T. Zhang, T. Yu, T. B. Hashimoto, M. Lewis, W. Yih, D. Fried, and S. I. Wang
Coder Reviewer Reranking for Code Generation
.
arXiv
.
Note:
arXiv:2211.16490
External Links:
Link
Cited by:
§1
,
§5
.
Zhong
et al.
(2024)
L. Zhong, Z. Wang, and J. Shang
Debug like a Human: A Large Language Model Debugger via Verifying Runtime Execution Step by Step
.
In
Findings of the Association for Computational Linguistics ACL 2024
,
Bangkok, Thailand and virtual meeting
,
pp. 851–870
(
en
).
External Links:
Link
,
Document
Cited by:
§5
.
Appendix A
Training Details Continued
Table 4:
Details of our training datasets. “# Probs” is the number of problems in the dataset. “Prob. Tok” is the average number of tokens in the problem description. “Tokens” is the average number of tokens in the problem and solutions when formatted with the prompt. “Sols.” is the average number of unique non-syntax error solutions per problem. “# Passed” is the mean number of passing solutions per problem. “% Passed” is the percentage of problems that had at least one passing solution. “# Pairs” is the average number of possible pairs per problem, where a pair is 1 correct and 1 incorrect solution.
Dataset
Split
# Probs
Prob. Tok
Tokens
Sols.
# Passed
% Passed
# Pairs
CodeContests
Train
13,213
776.76
508.08
124.78
14.00
35.92
6.58
Val
117
921.66
625.66
126.31
4.36
23.08
3.61
GSM8K
Train
7,373
160.16
59.55
83.50
67.03
98.87
9.26
Val
100
177.42
66.63
105.93
78.66
100.00
15.16
A.1
Hyperparameters
We use The Transformers Library
(
Wolf et al., 2020
)
with Hugging Face Datasets
(
Lhoest et al., 2021
)
for training our models. We use FlashAttention 2.0
(
Dao, 2023
)
and BFloat16 precision. We use the Adam optimizer
(
Kingma and Ba, 2017
)
with
β
1
=
0.9
\beta_{1}=0.9
,
β
2
=
0.999
\beta_{2}=0.999
,
ϵ
=
1
​
e
−
8
\epsilon=1e-8
. We use a cosine learning rate schedule that peaks at
5
​
e
−
6
5e-6
and 10% warmup steps. We use a batch size of 64 with a maximum sequence length of 2048. We employ gradient checkpointing and accumulation to be able to train our models on a single A6000 GPU. We train the ORM for 2 epochs on our dataset and use the last checkpoint for evaluation. We train each setup six times across six random seeds (1, 1999, 2000, 2021, 2024, 2042) and report the mean results.
To create our training data we first apply Black formatting to the generated code as mentioned in
section 3
. We then filter out any programs with syntax errors and problems which do not have at least 1 correct and 1 incorrect solution. Then we randomly sample at most six examples per problem. For our pairwise objectives this means we sample a total of 12 programs per problem. We use the CodeContests validation set along with 100 randomly sampled problems from the GSM8K validation set to create our validation data.
Appendix B
Example Problem
Listing 1:
Example Problem Description From CodeContests
⬇
1
A
string
is
called
square
if
it
is
some
string
written
twice
in
a
row
.
For
example
,
the
strings
”
aa
”,
”
abcabc
”,
”
abab
”
and
”
baabaa
”
are
square
.
But
the
strings
”
aaa
”,
”
abaaab
”
and
”
abcdabc
”
are
not
square
.
2
3
For
a
given
string
s
determine
if
it
is
square
.
4
5
Input
6
7
The
first
line
of
input
data
contains
an
integer
t
(1
<=
t
<=
100)
-
the
number
of
test
cases
.
8
9
This
is
followed
by
t
lines
,
each
containing
a
description
of
one
test
case
.
The
given
strings
consist
only
of
lowercase
Latin
letters
and
have
lengths
between
1
and
100
inclusive
.
10
11
Output
12
13
For
each
test
case
,
output
on
a
separate
line
:
14
15
*
YES
if
the
string
in
the
corresponding
test
case
is
square
,
16
*
NO
otherwise
.
17
18
19
20
You
can
output
YES
and
NO
in
any
case
(
for
example
,
strings
yEs
,
yes
,
Yes
and
YES
will
be
recognized
as
a
positive
response
).
21
22
Example
23
24
Input
25
26
27
10
28
a
29
aa
30
aaa
31
aaaa
32
abab
33
abcabc
34
abacaba
35
xxyy
36
xyyx
37
xyxy
38
39
40
Output
41
42
43
NO
44
YES
45
NO
46
YES
47
YES
48
YES
49
NO
50
NO
51
NO
52
YES
Listing 2:
Example Correct Solution
⬇
1
import
sys
2
3
#
Read
input
from
stdin
4
input
=
sys
.
stdin
.
read
5
data
=
input
().
split
()
6
7
#
The
first
element
is
the
number
of
test
cases
8
t
=
int
(
data
[0])
9
10
#
Iterate
over
each
test
case
11
for
i
in
range
(1,
t
+
1):
12
s
=
data
[
i
]
13
length
=
len
(
s
)
14
#
Check
if
the
length
of
the
string
is
even
15
if
length
%
2
==
0:
16
half
=
length
//
2
17
#
Check
if
the
first
half
is
equal
to
the
second
half
18
if
s
[:
half
]
==
s
[
half
:]:
19
print
(
”YES”
,
end
=
”\n”
)
20
else
:
21
print
(
”NO”
,
end
=
”\n”
)
22
else
:
23
print
(
”NO”
,
end
=
”\n”
)
Listing 3:
Example Incorrect Solution
⬇
1
import
sys
2
3
4
def
is_square
(
s
):
5
n
=
len
(
s
)
6
for
i
in
range
(1,
n
//
2
+
1):
7
if
n
%
i
==
0:
8
prefix
=
s
[:
i
]
9
if
prefix
*
(
n
//
i
)
==
s
:
10
return
”YES”
11
return
”NO”
12
13
14
def
main
():
15
input
=
sys
.
stdin
.
read
16
data
=
input
().
split
()
17
t
=
int
(
data
[0])
18
results
=
[]
19
for
i
in
range
(1,
t
+
1):
20
results
.
append
(
is_square
(
data
[
i
]))
21
for
result
in
results
:
22
print
(
result
)
23
24
25
if
__name__
==
”__main__”
:
26
main
()
Appendix C
Bug Pattern Examples
Examples of each bug pattern from
Table 3
. All examples are from solutions ranked in the ORM’s top-16 but filtered by
V
S
1
V_{S_{1}}
.
C.1
Float Division in Binary Search
Using
/
instead of
//
produces floats that cause
TypeError
on indexing or silent truncation bugs. A single character difference.
Listing 4:
Wrong: float division (ORM Rank 2)
⬇
1
while
right
-
left
>
1
e
-9:
2
mid
=
(
left
+
right
)
/
2
#
Bug:
returns
float
5.5,
not
int
5
3
if
check
(
k
,
mid
,
points
):
4
right
=
mid
5
else
:
6
left
=
mid
Listing 5:
Correct: integer division
⬇
1
while
left
<=
right
:
2
mid
=
(
left
+
right
)
//
2
#
Returns
int
5
3
if
check
(
k
,
mid
,
points
):
4
right
=
mid
-
1
5
else
:
6
left
=
mid
+
1
C.2
Int Cast of Float Division
Using
int(x/y)
instead of
x//y
. Appears correct but
int()
truncates toward zero while
//
floors, giving different results for negative numbers.
Listing 6:
Wrong: int of float division (ORM Rank 3)
⬇
1
prefix
=
[1]
2
for
x
,
y
in
zip
(
a
,
b
):
3
if
y
==
”*”
:
4
prefix
.
append
(
prefix
[-1]
*
x
)
5
else
:
6
prefix
.
append
(
int
(
prefix
[-1]
/
x
))
#
Bug:
int(-3/2)=-1,
-3//2=-2
Listing 7:
Correct: floor division
⬇
1
prefix
.
append
(
prefix
[-1]
//
x
)
#
Correct
floor
division
C.3
Large Integer Arithmetic
Operations on large integers that lose precision or overflow intermediate values. Common in competitive programming where results require modular arithmetic.
Listing 8:
Wrong: intermediate overflow (ORM Rank 3)
⬇
1
def
count_paths
(
n
,
edges
):
2
MOD
=
10**9
+
7
3
#
Bug:
a
*
b
overflows
before
modulo
on
some
paths
4
result
=
a
*
b
*
c
%
MOD
#
Intermediate
a*b*c
exceeds
int
precision
5
return
result
Listing 9:
Correct: modulo at each step
⬇
1
def
count_paths
(
n
,
edges
):
2
MOD
=
10**9
+
7
3
result
=
a
*
b
%
MOD
4
result
=
result
*
c
%
MOD
#
Keep
intermediate
values
bounded
5
return
result
C.4
Remove in Loop
Calling
.remove()
inside a loop modifies the collection while iterating, causing skipped elements or
ValueError
.
Listing 10:
Wrong: modifying set while iterating (ORM Rank 4)
⬇
1
for
i
in
range
(1,
n
):
2
if
(
u
,
i
)
in
E
and
(
v
,
i
)
not
in
E
:
3
T
=
min
(
T
,
f
(
u
,
i
,
t
+
1))
4
E
.
remove
((
u
,
i
))
#
Bug:
modifies
E
during
iteration
5
E
.
remove
((
v
,
i
))
6
E
.
add
((
u
,
v
))
Listing 11:
Correct: collect then remove
⬇
1
to_remove
=
[]
2
for
i
in
range
(1,
n
):
3
if
(
u
,
i
)
in
E
and
(
v
,
i
)
not
in
E
:
4
T
=
min
(
T
,
f
(
u
,
i
,
t
+
1))
5
to_remove
.
append
(((
u
,
i
),
(
v
,
i
)))
6
for
pair
in
to_remove
:
7
E
.
discard
(
pair
[0])
8
E
.
discard
(
pair
[1])
C.5
While Len Condition
Using
while len(x) > 0
instead of
while x
. Verbose and often indicates confused reasoning about the loop invariant.
Listing 12:
Wrong: verbose length check (ORM Rank 5)
⬇
1
while
len
(
habitats
)
>
0:
#
Unidiomatic
2
if
is_inside
((
center
,
radius
),
habitats
[-1]):
3
habitats
.
pop
()
4
else
:
5
radius
+=
dist
((
center
,
radius
),
habitats
[-1])
6
#
Bug:
infinite
loop
if
habitat
can’t
be
covered
Listing 13:
Correct: idiomatic check with termination
⬇
1
while
habitats
:
2
habitat
=
habitats
[-1]
3
if
is_inside
((
center
,
radius
),
habitat
):
4
habitats
.
pop
()
5
elif
radius
>=
max_radius
:
6
break
#
Explicit
termination
condition
7
else
:
8
radius
=
compute_new_radius
(
center
,
habitat
)
Appendix D
Prompts Used
Listing 14:
Prompt used for training and inference
⬇
1
#
Question
2
Tom
and
Tim
both
brought
4,
six
-
sided
dice
to
school
.
3
How
many
total
sides
are
there
?
4
5
#
Proposed
Solution
6
“‘
python
7
def
solution
():
8
dice_per_person
=
4
9
sides_per_die
=
6
10
total_dice
=
dice_per_person
*
2
11
total_sides
=
total_dice
*
sides_per_die
12
result
=
total_sides
13
return
result
14
15
“‘
16
<|
end_of_text
|>
Appendix E
Execution Details Continued
HumanEval tests function completion where the model must write the correct function given a docstring and signature. MBPP, on the other hand, tasks the model with synthesizing a function given a single sentence specification and a single test case. Then we use the execution framework provided by EvalPlus that executes the program from inside of a Python process. In both of these cases, the evaluation relies on assertions that call a specific entrypoint function. Thus, we use EvalPlus
sanitize
method to extract all relevant code and comments using treesitter
4
4
4
https://github.com/tree-sitter/tree-sitter
to parse the AST. This does come with the caveat that it heavily perturbs the whitespace of the original code in unnatural ways. Thus we use the Black formatter
5
5
5
https://github.com/psf/black
to format both our evaluation and training data. We run all of our trials on a cluster designed for high throughput computing
(
Center for High Throughput Computing, 2006
)
.
Appendix F
Data Generation Details
To generate our training data for our ORMs, we use the training splits of CodeContests-Python
(
Li et al., 2022
)
and GSM8K
(
Cobbe et al., 2021
)
in Program-aided Language Models (PAL) format
(
Gao et al., 2022
)
. The CodeContests dataset is a collection of competitive programming problems from platforms such as CodeForces.
6
6
6
https://codeforces.com/
Each program requires taking in STDIN inputs and printing the results to STDOUT. Most, but not all, problems have a few private test cases. We follow the LiveCodeBench
(
Jain et al., 2024
)
prompts and formatting for generation.
For GSM8K, we opt for the PAL format as it allows us to have more programming training data from a different domain. We additionally use the BigCodeEval
(
Allal et al., 2025
)
in context examples for GSM8K. We use Qwen 2.5 Coder Instruct 7B
(
Hui et al., 2024
)
with Int8 GPTQ quantization
(
Frantar et al., 2023
)
to generate our training data. We sample a maximum of 1024 tokens
128
128
times per problem with a temperature of
T
=
1.0
T=1.0
and top-p of
0.95
0.95
. We use the VLLM
(
Kwon et al., 2023
)
library to generate our data. Full details of our training data are found in
Appendix A
.
Table 5:
Breakdown of evaluation data.
π
G
\pi_{\textrm{G}}
is the generator size,
T
T
is the temperature, and DS is the dataset. Prob Pass is the percentage of problems where at least one solution passes at least one test. % Pass is the mean fraction of tests passed per solution. Net Sols is the total number of solutions. Prob. Tok and Tok. are the average token counts for problem statements and solutions. # Pass is the average number of fully correct solutions (passing all tests) per problem. Avg. Sols is the average number of solutions per problem.
π
G
\pi_{\textrm{G}}
T
T
DS
Prob Pass
% Pass
Net Sols
Prob. Tok
Tok.
# Pass
Avg. Sols
500M
1.0
CC
68.48
2.75
21,014
620.74
878.31
0.04
127.36
GSM8K
80.36
18.75
151,608
71.31
155.68
18.31
114.94
HE
100.00
41.99
16,444
144.22
359.51
33.98
100.27
MBPP
95.77
40.42
40,187
60.51
156.05
39.50
106.31
1.5B
1.0
CC
78.18
6.03
20,932
620.74
868.14
0.13
126.86
GSM8K
95.00
50.33
135,144
71.31
160.51
45.92
102.46
HE
100.00
57.90
16,643
144.22
320.82
51.06
101.48
MBPP
98.41
54.72
41,018
60.51
132.90
53.15
108.51
3B
1.0
CC
88.48
9.83
21,108
620.74
921.48
0.47
127.93
GSM8K
97.80
66.16
129,375
71.31
163.22
59.09
98.09
HE
100.00
75.27
14,935
144.22
336.42
63.43
91.07
MBPP
99.47
58.99
44,896
60.51
138.26
65.64
118.77
7B
0.2
CC
84.24
14.54
11,905
620.74
902.13
0.21
72.15
GSM8K
91.66
82.20
14,135
71.31
162.98
7.10
10.72
HE
99.39
86.09
2,643
144.22
323.89
12.14
16.12
MBPP
96.83
72.24
10,281
60.51
144.11
14.60
27.20
0.4
CC
88.48
14.92
18,331
620.74
895.37
0.32
111.10
GSM8K
95.68
82.11
40,932
71.31
163.93
21.26
31.03
HE
99.39
83.88
7,071
144.22
324.28
33.40
43.12
MBPP
97.88
71.08
24,167
60.51
144.51
37.24
63.93
0.6
CC
90.30
14.80
20,300
620.74
892.90
0.42
123.03
GSM8K
96.89
81.23
69,711
71.31
164.16
37.52
52.85
HE
99.39
83.23
11,127
144.22
319.59
52.44
67.85
MBPP
98.94
69.65
34,328
60.51
144.02
55.72
90.81
0.8
CC
93.33
14.47
20,834
620.74
893.17
0.38
126.27
GSM8K
97.88
80.62
94,225
71.31
164.30
52.23
71.44
HE
99.39
81.76
14,241
144.22
315.55
67.17
86.84
MBPP
99.21
68.69
40,961
60.51
143.52
68.29
108.36
1.0
CC
92.12
14.11
21,022
620.74
897.16
0.32
127.41
GSM8K
98.56
79.44
114,882
71.31
165.06
64.48
87.10
HE
99.39
80.98
16,625
144.22
310.11
78.46
101.37
MBPP
99.74
66.64
44,915
60.51
144.73
74.42
118.82
14B
1.0
CC
92.73
18.76
19,852
620.74
988.10
0.10
120.32
GSM8K
98.94
87.69
129,548
71.31
170.84
83.86
98.22
HE
100.00
83.97
15,410
144.22
314.70
75.10
93.96
MBPP
98.94
70.23
24,411
60.51
142.26
38.29
64.58
Figure 6:
Distribution of the failed candidates based on where
V
θ
V_{\theta}{}
had ranked them. A rank of 1 means the candidate was the top-ranked, while 128 means it was the lowest-ranked. The rows are the individual verifiers while the columns are the datasets. This is for the 500M
V
θ
V_{\theta}
.
Table 6:
Standard deviation of the results for the different pruning with a weak verifier then ranking methods.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run. “Syntax” and “Lint” remove any programs with the respective errors. “N Test” prunes out any programs that do not pass the first
N
N
test cases. The evaluation dataset is generated with Qwen 2.5 Coder 7B Instruct using
T
=
1.0
T=1.0
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens. For the Non-ORM methods, there is no standard deviation for best-of-64 as the ordering is the same
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
MV
—
—
—
—
—
—
—
—
500M
0.74
14.45
0.99
71.70
1.05
37.57
1.06
76.28
1.5B
0.69
4.00
1.28
20.18
1.54
10.92
1.20
23.13
Syntax
MV
—
399.40
—
445.70
—
517.91
—
742.06
500M
0.70
2.73
0.30
13.23
0.93
5.26
0.81
15.19
1.5B
0.76
1.76
0.43
8.23
1.80
4.19
0.83
9.72
Lint
MV
—
92.07
—
9.88
—
4.69
—
9.62
500M
0.87
9.60
1.26
18.62
0.89
12.14
2.26
11.73
1.5B
0.82
2.75
1.98
7.56
1.41
5.02
1.74
7.12
1 Test
MV
—
1.48
—
—
—
101.45
—
150.46
500M
0.34
0.28
—
—
1.03
27.92
1.42
48.73
1.5B
0.49
0.61
—
—
1.54
9.17
1.00
20.22
10 Tests
MV
—
2.27
—
—
—
54.43
—
44.48
500M
0.15
0.01
—
—
0.76
0.27
0.39
0.03
1.5B
0.49
0.04
—
—
0.82
0.06
0.18
0.08
V
all
V_{\text{all}}{}
—
0.09
—
37.90
—
0.92
—
0.43
Appendix G
All result tables
Table 7:
On-demand hourly prices for hardware-matched instances. Prices are Linux on-demand in AWS us-east-1, Azure eastus, and GCP us-central1 (Jan 22, 2026).
Provider
GPU (single
∼
\sim
48GB)
CPU 64c/256GB
AWS
$3.004/hr
$3.072/hr
Azure
$3.673/hr
$3.072/hr
GCP
$5.782/hr
$3.1078/hr
Table 8:
Information about the tokens filtered from the datasets by the 5 verifiers we look at on the 3B, 7B, and 14B models. The percentage filtered is the percentage of tokens filtered from the dataset, the average sequence length is the average sequence length of the tokens that were filtered, and the total tokens filtered is the total number of tokens filtered from the dataset.
π
G
\pi_{\textrm{G}}
V
V
DS
% Filtered
Avg. Seq Length
Total Tokens Filtered
7B
Syntax
CC
0.76
1,222.81
1.89e+07
GSM8K
0.45
201.33
2.04e+07
HE
0.00
135.00
5.47e+06
MBPP
0.00
65.00
6.63e+06
Lint
CC
5.36
1,131.51
1.89e+07
GSM8K
1.33
203.86
2.04e+07
HE
1.00
408.92
5.47e+06
MBPP
1.05
159.68
6.63e+06
1 Test
CC
88.90
919.54
1.89e+07
HE
8.44
378.60
5.47e+06
MBPP
22.88
173.66
6.63e+06
3 Tests
CC
92.85
908.04
1.89e+07
HE
13.97
364.37
5.47e+06
MBPP
27.58
170.55
6.63e+06
10 Tests
CC
93.39
906.89
1.89e+07
HE
18.84
364.83
5.47e+06
MBPP
37.92
165.21
6.63e+06
14B
Syntax
CC
4.87
1,610.94
1.96e+07
GSM8K
0.16
213.89
2.35e+07
HE
0.04
130.29
5.22e+06
MBPP
0.13
61.49
3.93e+06
Lint
CC
7.76
1,411.36
1.96e+07
GSM8K
0.81
216.55
2.35e+07
HE
0.95
315.97
5.22e+06
MBPP
0.94
135.12
3.93e+06
1 Test
CC
85.08
1,019.14
1.96e+07
HE
5.99
375.57
5.22e+06
MBPP
21.93
182.11
3.93e+06
3 Tests
CC
89.01
1,005.72
1.96e+07
HE
11.18
369.63
5.22e+06
MBPP
26.60
178.78
3.93e+06
10 Tests
CC
89.95
1,003.10
1.96e+07
HE
15.53
373.36
5.22e+06
MBPP
38.54
173.15
3.93e+06
Table 9:
Information on filtered solutions for the 500M and 1.5B
V
θ
V_{\theta}
across the datasets when using the 7B Qwen 2.5 Coder Instruct
π
G
\pi_{\textrm{G}}
and a temperature of 1.0. “# Rem” is the average number of solutions removed per question. “Avg. Rank” is the average rank of the solutions that were removed. “M1 Rank” is the average highest rank of the solutions that were removed. “M5 Rank” is the average rank of the 5 top ranks of the solutions that were removed. “% Removed” is the total percentage of solutions removed across all questions. “% Prob” is the percentage of problems where all solutions were removed. “Spread” is the average spread of the solutions that were removed across the six seeds.
V
θ
V_{\theta}
V
V
# Rem
Avg. Rank
M1 Rank
M5 Rank
% Removed
% Prob
Spread
500M
1 Test
51.38
82.90
38.87
51.04
40.14
6.86
20.00
10 Tests
63.53
77.81
27.63
39.36
49.63
12.57
17.90
Lint
4.76
102.31
86.49
97.84
3.72
0.00
31.91
Syntax
5.13
106.50
98.53
104.93
4.01
0.00
32.08
1.5B
1 Test
51.38
89.27
47.87
58.42
40.14
6.86
19.14
10 Tests
63.53
83.47
35.41
45.89
49.63
12.57
17.14
Lint
4.76
108.70
96.02
104.91
3.72
0.00
30.16
Syntax
5.13
112.99
107.00
111.73
4.01
0.00
30.28
Table 10:
Results for the generation with Qwen 2.5 Coder 500M instruct with
T
=
1.0
T=1.0
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
0.47
68.39
38.08
374.52
51.96
157.37
47.70
353.18
1.5B
0.61
26.42
53.91
147.74
67.50
64.10
57.70
145.72
1 Test
MV
1.39
126.19
—
—
64.05
851.41
61.41
870.83
500M
1.71
79.64
—
—
65.51
180.55
62.42
325.07
1.5B
2.02
74.27
—
—
74.18
91.64
66.59
200.19
3 Tests
MV
1.39
125.72
—
—
72.13
814.36
64.44
483.11
500M
1.72
72.82
—
—
74.46
215.28
65.26
335.60
1.5B
2.05
69.09
—
—
78.73
116.20
67.90
213.38
10 Tests
MV
1.65
125.65
—
—
82.88
620.28
70.64
378.63
500M
1.76
87.47
—
—
83.21
182.60
71.64
199.45
1.5B
2.15
82.33
—
—
83.67
114.91
72.36
154.63
V
all
V_{\text{all}}{}
2.16
3.32
73.63
391.53
86.79
19.09
73.73
13.99
Table 11:
Results for the generation with Qwen 2.5 Coder 1.5B instruct with
T
=
1.0
T=1.0
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
1.64
67.79
63.63
348.16
64.78
169.35
58.72
394.16
1.5B
2.62
26.63
75.01
137.80
71.85
69.56
65.72
162.73
1 Test
MV
4.92
124.94
—
—
72.17
905.65
72.81
1195.51
500M
5.64
74.06
—
—
73.05
162.21
72.34
312.70
1.5B
5.60
67.36
—
—
77.90
80.87
74.26
186.30
3 Tests
MV
5.39
122.97
—
—
80.10
1026.14
76.22
1070.13
500M
5.80
79.71
—
—
79.99
180.70
75.14
316.46
1.5B
5.61
73.83
—
—
83.29
93.31
76.07
193.02
10 Tests
MV
5.73
122.34
—
—
88.60
571.02
81.66
511.41
500M
5.95
79.18
—
—
86.44
157.04
82.33
189.80
1.5B
5.75
73.53
—
—
88.15
91.79
82.47
142.11
V
all
V_{\text{all}}{}
7.83
2.23
92.72
173.71
94.06
20.09
85.64
20.97
Table 12:
Results for the generation with Qwen 2.5 Coder 3B instruct with
T
=
1.0
T=1.0
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
4.52
64.02
75.48
339.96
75.50
159.60
60.70
387.75
1.5B
5.76
25.14
81.89
134.53
79.90
65.21
67.54
159.58
1 Test
MV
9.65
122.58
—
—
82.39
1057.72
74.99
1217.04
500M
10.93
66.69
—
—
79.15
142.54
72.22
294.73
1.5B
11.39
58.02
—
—
84.01
66.80
75.09
169.51
3 Tests
MV
11.34
118.91
—
—
85.78
1208.37
77.72
1074.66
500M
12.40
64.03
—
—
85.29
153.96
74.96
301.64
1.5B
12.83
58.40
—
—
88.22
72.96
77.45
177.22
10 Tests
MV
12.16
116.15
—
—
89.54
684.03
84.10
509.97
500M
12.67
70.78
—
—
89.01
137.37
83.04
178.20
1.5B
13.04
64.18
—
—
91.33
71.77
84.24
131.16
V
all
V_{\text{all}}{}
14.92
2.54
96.63
647.01
95.41
22.13
88.23
12.48
Table 13:
Results for the generation with Qwen 2.5 Coder 14B instruct with
T
=
1.0
T=1.0
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
10.99
59.83
90.53
323.74
83.23
172.96
68.85
328.09
1.5B
12.86
23.52
91.49
127.83
85.44
70.92
73.28
137.09
1 Test
MV
22.76
132.92
—
—
88.67
1197.05
79.82
1360.04
500M
24.47
66.16
—
—
85.08
143.42
75.26
264.22
1.5B
25.52
52.46
—
—
86.89
67.51
77.29
139.90
3 Tests
MV
24.32
127.07
—
—
90.36
1130.49
81.65
1127.35
500M
26.07
59.08
—
—
88.10
148.71
77.00
267.42
1.5B
26.60
50.44
—
—
88.98
70.44
78.66
145.13
10 Tests
MV
25.83
120.53
—
—
91.62
662.39
87.72
349.60
500M
28.02
67.14
—
—
90.47
128.04
85.83
157.48
1.5B
28.10
57.46
—
—
90.88
67.25
86.47
112.77
V
all
V_{\text{all}}{}
31.98
3.65
98.61
153.10
96.57
24.43
90.29
17.11
Table 14:
Results for the generation with Qwen 2.5 Coder 7B instruct with
T
=
0.2
T=0.2
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
5.86
61.72
84.94
259.14
85.11
131.74
71.26
258.15
1.5B
5.38
24.54
86.11
110.67
86.44
57.42
73.93
115.38
1 Test
MV
10.82
173.82
—
—
88.41
961.83
78.24
316.36
500M
10.86
81.39
—
—
86.12
116.61
76.98
234.99
1.5B
11.72
66.73
—
—
88.01
56.21
77.42
128.61
3 Tests
MV
11.69
163.05
—
—
89.63
1196.20
79.63
1010.78
500M
12.11
90.59
—
—
88.09
120.93
77.53
240.79
1.5B
12.38
80.77
—
—
89.52
59.52
78.31
135.70
10 Tests
MV
12.09
157.14
—
—
90.85
611.21
81.60
373.46
500M
12.35
88.55
—
—
89.26
104.69
80.95
143.88
1.5B
12.40
80.12
—
—
90.38
56.36
81.31
104.77
V
all
V_{\text{all}}{}
12.40
3.09
91.17
504.11
91.46
11.63
82.40
6.97
Table 15:
Results for the generation with Qwen 2.5 Coder 7B instruct with
T
=
0.4
T=0.4
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
5.61
65.65
86.15
299.19
82.74
151.34
69.13
317.32
1.5B
7.29
26.06
88.40
120.73
85.35
63.50
72.65
134.96
1 Test
MV
13.11
163.12
—
—
87.80
1146.83
79.15
1257.67
500M
14.29
77.29
—
—
84.35
134.12
75.38
254.88
1.5B
14.91
64.04
—
—
86.96
62.73
76.75
138.36
3 Tests
MV
15.50
153.76
—
—
89.56
1143.86
80.52
1207.37
500M
15.64
78.18
—
—
87.23
138.00
76.82
261.47
1.5B
16.18
69.93
—
—
88.85
65.37
78.44
144.88
10 Tests
MV
15.90
147.99
—
—
90.78
639.57
83.29
358.78
500M
16.00
82.17
—
—
89.27
116.53
82.32
157.60
1.5B
16.29
73.83
—
—
90.03
61.52
83.10
112.16
V
all
V_{\text{all}}{}
16.74
3.83
95.21
60.02
92.57
15.11
84.55
14.80
Table 16:
Results for the generation with Qwen 2.5 Coder 7B instruct with
T
=
0.6
T=0.6
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
6.00
66.83
85.73
317.18
83.09
163.23
67.14
351.91
1.5B
7.21
26.53
88.19
127.31
84.78
67.77
71.45
146.91
1 Test
MV
12.99
145.28
—
—
86.77
1280.37
77.83
1183.06
500M
13.46
74.06
—
—
84.87
140.68
74.82
264.62
1.5B
14.94
62.05
—
—
86.55
66.63
77.02
144.47
3 Tests
MV
14.76
142.47
—
—
89.71
1232.14
80.06
1011.88
500M
14.84
78.82
—
—
87.75
150.36
76.82
268.41
1.5B
15.82
70.11
—
—
88.50
70.82
78.91
150.06
10 Tests
MV
15.63
136.34
—
—
90.93
504.65
85.36
362.63
500M
15.30
80.81
—
—
89.52
125.36
84.09
159.63
1.5B
16.09
72.55
—
—
89.69
66.52
85.30
114.18
V
all
V_{\text{all}}{}
17.65
2.13
96.40
590.56
94.05
18.06
86.23
26.87
Table 17:
Results for the generation with Qwen 2.5 Coder 7B instruct with
T
=
0.8
T=0.8
,
n
=
128
n=128
,
t
​
o
​
p
p
=
0.95
top_{p}=0.95
, and 1024 tokens.
Green backgrounds
is higher performance while
Red backgrounds
is lower performance with respect to the entire column. If
V
V
is “—” that means no pruning is done.
V
all
V_{\text{all}}{}
is the case where
all
test cases are run.
CodeContests
GSM8K
HumanEval
MBPP
Filter
Ranker
Bof64
PPS
Bof64
PPS
Bof64
PPS
Bof64
PPS
—
500M
5.44
67.12
85.26
328.44
80.57
172.06
66.03
374.18
1.5B
6.96
25.49
87.97
125.81
82.54
71.43
71.12
151.33
1 Test
MV
13.54
137.85
—
—
87.43
1327.06
76.03
1097.09
500M
13.98
70.55
—
—
83.44
143.43
74.78
268.36
1.5B
14.92
59.29
—
—
84.53
67.50
77.26
145.59
3 Tests
MV
14.46
131.96
—
—
90.72
1178.13
79.32
1063.62
500M
15.24
64.33
—
—
86.33
151.41
76.69
270.28
1.5B
15.60
57.96
—
—
87.06
71.48
79.00
150.07
10 Tests
MV
14.56
126.77
—
—
92.10
680.40
85.77
459.95
500M
15.46
75.19
—
—
89.52
129.99
84.93
169.68
1.5B
15.70
67.22
—
—
89.56
68.03
86.31
118.63
V
all
V_{\text{all}}{}
17.98
3.35
97.30
582.08
95.65
19.81
89.03
19.55