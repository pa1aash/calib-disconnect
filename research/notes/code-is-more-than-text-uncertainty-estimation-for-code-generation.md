---
title: 'Code Is More Than Text: Uncertainty Estimation for Code Generation'
id: code-is-more-than-text-uncertainty-estimation-for-code-generation
tags:
- code-llm-confidence-positioning-d82d00
- uq-code
created: '2026-11-09T23:08:40.040362Z'
updated: '2026-11-09T23:27:44.498945Z'
source: https://arxiv.org/html/2606.09577
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:40.039872Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv HTML). CLOSE for L1/L3/L4. Code UE with three axes (Top-K
  token entropy, pseudo-code consistency, self-generated-test behavioral consistency);
  ensemble avg AUROC 0.776 vs 0.696 best NL baseline over 5 open code LLMs (14B-32B)
  on APPS-Intro/Interview, HumanEval, MBPP. Labels = official hidden-test pass@1,
  separate from self tests. AUROC/PRAUC only: ECE and Brier explicitly not reported;
  downstream utility left to future work; no probes, no base/instruct pairs, no contamination
  split; verbalized confidence only advised against (Sec 5).'
---

Code Is More Than Text: Uncertainty Estimation for Code Generation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2606.09577v1 [cs.CL] 08 Jun 2026
Code Is More Than Text: Uncertainty Estimation for Code Generation
Yuling Shi  Caiqi Zhang
1
1
footnotemark:
1
Yuexian Li  Haopeng Wang
†
†
thanks:
Equal contribution.
Affiliation:
Shanghai Jiao Tong University University of Cambridge
Yeheng Chen  Nigel Collier  Xiaodong Gu
Affiliation:
Shanghai Jiao Tong University University of Cambridge
Abstract
Large language models (LLMs) are increasingly deployed as code generators, where silently wrong programs pose real safety and reliability risks. Reliable
uncertainty estimation
(UE) is essential for selective prediction, human-in-the-loop review, and downstream agentic decisions. Yet most existing code UE methods are inherited from natural language (NL) generation and ignore properties that make code distinct. We argue that code differs from NL in three ways: a single wrong token can break an entire program (
token fragility
); algorithmic intent and concrete implementation can disagree independently (
intent–code gap
); and programs can be executed (
executability
). We instantiate these properties as three orthogonal uncertainty axes:
lexical
(Top-
K
K
token entropy),
algorithmic
(pseudo-code consistency), and
functional
(behavioral consistency). Across five code LLMs, our three-axis ensemble improves average AUROC from 0.696 for the strongest NL-derived baseline to 0.776 (+8.1 points). Notably, on Qwen3-14B, our single-pass Top-
K
K
token entropy matches the strongest multi-pass baseline while being over
3
×
3\times
cheaper; across models, it remains a competitive low-cost signal. These results suggest that code UE deserves code-specific design rather than direct NL ports.
1
Introduction
Large language models (LLMs) have moved from single-line code completion to acting as the execution unit of IDE assistants, autonomous coding agents, and multi-step software-engineering pipelines
(
Chen et al., 2021
;
Austin et al., 2021
;
Shi et al., 2025c
)
. A silently wrong output is far more dangerous than a refusal or a flagged guess: errors slip past review and compound across downstream steps. Reliable
uncertainty estimation
(UE) has accordingly become increasingly important to safe deployment, gating selective prediction in autocomplete, prioritizing human review in code agents, and informing retry and escalation policies
(
Zhang et al., 2024
)
.
However, the methods that currently dominate code UE are
direct ports of NL UE
, including length-normalized likelihood, mean predictive entropy, semantic-consistency clustering, and verbalized confidence prompts
(
Malinin and Gales, 2021
;
Kuhn et al., 2023
;
Sharma and David, 2025
;
Zhang et al., 2024
)
, which treat code as just another token sequence. We argue that this abstraction fails to exploit the characteristics of code. Code differs from NL in three under-exploited ways. First, code suffers from
token fragility
: a single wrong operator can break the entire program, so uncertainty in code is sparse rather than uniform. Second, a program has an
intent–code gap
that separates algorithmic intent from concrete implementation; code can be abstracted into pseudo-code, which strips away surface variation and provides a cleaner basis for consistency-based estimation than raw code. Third, code is
executable
: the pass/fail pattern of a candidate program against test cases is a direct behavioral signal of functional correctness: a signal that is unique in NL generation.
How to design a UE method that respects these three properties remains an open question.
Figure 1:
Three methods based on characteristics of coding uncertainty signals
Motivated by these properties, we propose treating code uncertainty as a
three-axis
quantity in which each axis captures exactly one property (Figure
1
, Contribution
#1
): a
lexical
axis (Top-
K
K
token entropy) for token fragility, an
algorithmic
axis (pseudo-code consistency) that elicits
N
N
natural-language solution plans and measures their inter-sample agreement at the algorithmic level, and a
functional
axis (behavioral consistency) that scores how consistently a candidate’s runtime behavior agrees with the self-generated test cases, providing a calibration signal rather than a selection mechanism, in contrast to CodeT-style reranking
(
Chen et al., 2023
)
. The three axes are designed to be complementary, and a simple rank-normalized weighted sum gives an ensemble whose role is to demonstrate that complementarity rather than to be the contribution itself.
We evaluate on four benchmarks (APPS-Intro, APPS-Interview, HumanEval, MBPP) across five code-capable LLMs, comparing against single- and multi-pass NL UE baselines (Contribution
#2
). Our findings are as follows.
First
, each of the three axes independently matches or outperforms the strongest NL baseline on the property it targets, confirming that code-specific signals carry information that NL-derived methods miss (§
4
).
Second
, on Qwen3-14B, Top-
K
K
token entropy alone, despite being single-pass, matches the strongest multi-pass NL baseline at over 3
×
\times
lower cost; across models, it remains a competitive low-cost signal, indicating that token-level entropy has been substantially undervalued for code. Combining the three signals further improves performance, with the ensemble reaching 0.800 average AUROC on Qwen3-14B and 0.776 average AUROC across all five models (§
5
).
Third
, splitting token entropy over code versus comment tokens reveals an asymmetry invisible to full-sequence aggregation: code-only AUROC is 0.716, while comment-only entropy is
worse than random
(0.375) (§
5
). A cost–performance analysis (§
5
, Contribution
#3
) recommends Top-
K
K
entropy under tight sampling budgets and the three-signal ensemble when calibration matters. Our results suggest that code UE deserves code-specific design, and these three axes are a first instantiation rather than the last word.
2
Method
2.1
Problem Formulation
We study post-hoc uncertainty estimation for code generation. Given a natural-language prompt
x
x
describing a programming problem and a program
y
=
(
y
1
,
…
,
y
T
)
y=(y_{1},\ldots,y_{T})
generated by an LLM
π
θ
\pi_{\theta}
conditioned on
x
x
, an uncertainty estimator is a function
U
⁡
(
x
,
y
)
∈
ℝ
U(x,y)\in\mathbb{R}
that scores how uncertain
π
θ
\pi_{\theta}
is about its own output (larger = more uncertain). Ground-truth correctness is functional:
y
y
is correct iff it passes every test case in the problem’s
official
test suite (pass@1)
(
Chen et al., 2021
)
, which is held out and never shown to
π
θ
\pi_{\theta}
. The self-generated tests used by the functional signal in §
2.4
are strictly separate. Since larger
U
U
indicates higher uncertainty, we report AUROC and PRAUC using
−
U
-U
as the score, with the binary correctness label as the positive class.
2.2
Lexical Uncertainty
Motivation.
A single wrong token can break an entire program: one flipped operator, one off-by-one index, one misspelled function name, and the program crashes or silently returns the wrong answer. Natural language is far more tolerant; a wrong word usually leaves the meaning recoverable from context. This asymmetry, which we call
token fragility
, implies that uncertainty in code is
sparse
: correctness hinges on a small number of critical positions rather than being spread evenly across the sequence. Averaging entropy over the full output, the default in NL UE, dilutes these few decisive tokens. We therefore design our lexical signal to focus on the most uncertain positions rather than the full sequence.
Token-Level Entropy.
Given an input prompt
x
x
and a generated code sequence
y
=
(
y
1
,
y
2
,
…
,
y
T
)
y=(y_{1},y_{2},\ldots,y_{T})
, we
compute the token-level entropy at position
t
t
as
H
(
y
t
)
=
−
∑
v
∈
𝒱
p
(
v
∣
y
<
t
,
x
)
log
p
(
v
∣
y
<
t
,
x
)
,
H(y_{t})=-\sum_{v\in\mathcal{V}}p(v\mid y_{<t},x)\log p(v\mid y_{<t},x),
(1)
where
𝒱
\mathcal{V}
is the vocabulary and
p
⁡
(
v
∣
y
<
t
,
x
)
p(v\mid y_{<t},x)
is the model’s predicted
probability for token
v
v
. To obtain a sequence-level uncertainty score
U
⁡
(
y
)
U(y)
, we aggregate
token-level entropies across the generated program, preserving information from a small number
of potentially decisive high-uncertainty tokens.
Top-
K
K
Max Entropy.
A minimal sparse aggregator takes the single most uncertain token,
U
⁡
(
y
)
=
max
t
⁡
H
⁡
(
y
t
)
U(y)=\max_{t}H(y_{t})
. Because a single entropy spike can be noisy or non-critical, we extend this to averaging the
K
K
largest token entropies:
U
⁡
(
y
)
=
1
K
​
∑
i
=
1
K
H
⁡
(
y
σ
⁡
(
i
)
)
,
U(y)=\frac{1}{K}\sum_{i=1}^{K}H(y_{\sigma(i)}),
(2)
where
σ
\sigma
sorts token positions in descending order of entropy. Max entropy is the special case
K
=
1
K{=}1
; Top-
K
K
is more robust to isolated spikes.
K
K
is the only hyperparameter, with sensitivity reported in §
D.1
.
2.3
Algorithmic Uncertainty
Motivation.
Measuring consistency directly on code can sometimes be hard. Two correct quicksorts can look entirely different syntactically; two near-identical implementations can encode different algorithms. Surface or embedding similarity
(
Kuhn et al., 2023
;
Malinin and Gales, 2021
)
therefore conflates implementation noise with genuine algorithmic disagreement. Pseudo-code sidesteps both problems: it abstracts away naming and control-flow variants, so semantically equivalent solutions look alike, while still exposing genuine algorithmic differences. It also preserves the information needed for correctness: conditioning Qwen3-14B on ground-truth pseudo-code lifts MBPP pass@1 from 54% to 98% (Appendix
D.2
). Our algorithmic signal therefore elicits natural-language solution plans from
π
θ
\pi_{\theta}
and scores their inter-sample agreement.
Pipeline.
For each prompt
x
x
, we elicit
N
N
natural-language solution plans
{
z
(
1
)
,
…
,
z
(
N
)
}
\{z^{(1)},\ldots,z^{(N)}\}
directly from
π
θ
\pi_{\theta}
, using a prompt that asks for 6–10 numbered reasoning steps and explicitly forbids code constructs such as
for
,
while
, or variable assignments (full prompt in Appendix
A
). The
N
N
plans are sampled independently with temperature
τ
\tau
; each captures the model’s reasoning about the algorithmic solution, free of any particular implementation.
Agreement Score.
We measure inter-sample algorithmic agreement with
step-aware ROUGE-L similarity
, a structural matching metric tailored to the step-by-step nature of the elicited plans. The metric splits each plan into semantic steps, computes token-level ROUGE-L for each step pair, and aggregates scores through bidirectional max matching, capturing algorithmic consistency while ignoring superficial wording variations. For two plans
z
(
i
)
,
z
(
j
)
z^{(i)},z^{(j)}
:
sim
⁡
(
z
(
i
)
,
z
(
j
)
)
=
2
⋅
RL
step
​
(
z
(
i
)
,
z
(
j
)
)
len
⁡
(
z
(
i
)
)
+
len
⁡
(
z
(
j
)
)
.
\operatorname{sim}(z^{(i)},z^{(j)})=\frac{2\cdot\text{RL}_{\text{step}}(z^{(i)},z^{(j)})}{\operatorname{len}(z^{(i)})+\operatorname{len}(z^{(j)})}.
(3)
The algorithmic uncertainty for prompt
x
x
is the mean pairwise dissimilarity,
U
algo
​
(
x
)
=
1
−
2
N
⁡
(
N
−
1
)
​
∑
i
<
j
sim
⁡
(
z
(
i
)
,
z
(
j
)
)
,
U_{\text{algo}}(x)\;=\;1\;-\;\frac{2}{N(N-1)}\sum_{i<j}\operatorname{sim}\bigl(z^{(i)},z^{(j)}\bigr),
(4)
so low inter-plan agreement yields high uncertainty. The score is associated with the prompt
x
x
; when a per-candidate score is required, we assign
U
algo
​
(
x
)
U_{\text{algo}}(x)
to every candidate
y
y
drawn from
x
x
.
Why elicit plans directly, not abstract from sampled code.
A natural alternative is to first sample
N
N
programs and then prompt
π
θ
\pi_{\theta}
to abstract each into a pseudo-code summary. We prefer direct elicitation for two reasons. (i) The abstraction step is a second pass over a possibly wrong program, which compounds noise: an incorrect implementation often yields an incorrect abstraction that nonetheless looks plausible. (ii) Direct elicitation forces
π
θ
\pi_{\theta}
to commit to an algorithmic plan at the natural-language level without an intermediate code-writing step that conflates implementation and intent. Two other alternatives also fail. AST-based equivalence on raw code is too strict: it treats semantically equivalent rewrites (loop
↔
\leftrightarrow
comprehension) as disagreements and inflates uncertainty on correct samples. Execution-based equivalence requires running the programs and therefore collapses into the functional signal in §
2.4
.
2.4
Functional Uncertainty
Motivation.
Code is
executable
: a candidate program can be run on inputs and its outputs compared to expected ones. The fraction of self-generated tests that a candidate passes is therefore a direct, behaviorally grounded signal of functional correctness, available in the code setting through execution at substantially lower cost than multi-sample consistency methods, and inaccessible to any NL UE method. Our functional signal turns this fraction into an uncertainty score by measuring how
consistent
the candidate’s runtime behavior is with the behavior the self-generated tests expect.
Pipeline.
For each prompt
x
x
, we (i) prompt
π
θ
\pi_{\theta}
to self-generate
M
M
test cases
𝒯
⁡
(
x
)
=
{
t
1
,
…
,
t
M
}
\mathcal{T}(x)=\{t_{1},\ldots,t_{M}\}
(prompt in Appendix
A
); (ii) take the candidate program
y
y
produced for
x
x
(the greedy generation, in our default setup); and (iii) execute
y
y
against each test in a sandboxed interpreter, treating compile errors, runtime errors, and timeouts as failures.
Consistency Score.
Let
P
j
​
(
y
)
=
𝟙
​
[
y
​
passes
​
t
j
]
P_{j}(y)=\mathbb{1}[y\text{ passes }t_{j}]
. We define the candidate’s
behavioral consistency
with its self-tests as the fraction of tests passed,
C
⁡
(
y
)
=
1
M
​
∑
j
=
1
M
P
j
​
(
y
)
,
C(y)\;=\;\frac{1}{M}\sum_{j=1}^{M}P_{j}(y),
(5)
and the functional uncertainty as the complementary disagreement,
U
func
​
(
x
,
y
)
=
1
−
C
⁡
(
y
)
.
U_{\text{func}}\bigl(x,y\bigr)\;=\;1-C(y).
(6)
A candidate that disagrees with most of its own problem’s self-tests is flagged as uncertain. This formulation operates on a single candidate; aggregations exploiting multiple candidates’ joint pass/fail patterns (pairwise Hamming agreement, per-test Bernoulli entropy) are an alternative we leave to future work.
Differentiation from selection-based methods.
The functional signal is closely related to test-case-based program selection. CodeT
(
Chen et al., 2023
)
and related self-verification methods use self-generated tests to
rerank or filter
candidate programs, returning a preferred program; we instead use the pass pattern to
score
the model’s uncertainty about a given output, which is a calibration signal rather than a selection mechanism. The two uses are orthogonal: a CodeT-selected program still carries an uncertainty value under our scheme, and our score can gate or defer a CodeT decision.
Self-test quality.
Self-generated tests can be wrong, biased toward easy cases, or fail to exercise edge conditions. We quantify the gap to the official test suite in §
D.2
by varying
M
M
and comparing against an oracle upper bound, and discuss it in Limitations.
2.5
Ensemble
The three signals, namely
U
lex
U_{\text{lex}}
(Top-
K
K
token entropy, §
2.2
),
U
algo
U_{\text{algo}}
(pseudo-code consistency, §
2.3
), and
U
func
U_{\text{func}}
(behavioral consistency, §
2.4
), live on different scales and have different empirical ranges. Before combining them, we map each score to its empirical rank on the evaluation set and rescale to
[
0
,
1
]
[0,1]
; let
U
~
∙
\tilde{U}_{\bullet}
denote the rank-normalized version of
U
∙
U_{\bullet}
. The ensemble is a simple weighted sum,
U
ens
​
(
x
,
y
)
=
α
lex
​
U
~
lex
​
(
x
,
y
)
+
α
algo
​
U
~
algo
​
(
x
)
+
α
func
​
U
~
func
​
(
x
,
y
)
,
\begin{split}U_{\text{ens}}(x,y)&=\alpha_{\text{lex}}\tilde{U}_{\text{lex}}(x,y)+\alpha_{\text{algo}}\tilde{U}_{\text{algo}}(x)\\
&\quad+\alpha_{\text{func}}\tilde{U}_{\text{func}}(x,y),\end{split}
(7)
with non-negative weights summing to one. Details of the choice of ensemble weights are in Appendix
C
.
We deliberately keep the combiner simple. The ensemble is not the contribution of the paper; its role is to demonstrate that
the three axes are complementary
, a claim we substantiate directly in §
5
via three analyses.
3
Experimental Setup
Datasets.
We evaluate on four widely used Python code generation benchmarks that together span a broad difficulty range. APPS
(
Hendrycks et al., 2021
)
provides programming problems collected from competitive-coding platforms; we use its
Introductory
(N = 1000) and
Interview
(N = 1000) subsets, which differ substantially in algorithmic depth and so let us probe whether each uncertainty signal degrades gracefully with problem difficulty. HumanEval
(
Chen et al., 2021
)
(N = 164) and MBPP
(
Austin et al., 2021
)
(N = 500) are community-standard benchmarks of short, function-level problems with hidden unit tests. HumanEval and MBPP are now close to saturated for strong code LLMs in pass@1; APPS-Interview leaves clear headroom and provides a harder distribution on which calibration matters most.
Models.
We evaluate on five open-source code LLMs spanning 14B–32B parameters and a mix of general and code-specialized models: Qwen3-14B and Qwen3-32B
(
Yang et al., 2025
)
, the code-specialized Qwen3-Coder-30B-A3B-Instruct
(
Yang et al., 2025
)
, denoted as Qwen3-Coder-30B, Mistral-Devstral-Small-2505
(
Rastogi et al., 2025
)
, denoted as Devstral-Small-2505, and DeepSeek-Coder-V2-Lite-Instruct
(
Zhu et al., 2024
)
, denoted as Deepseek-Coder-V2. We report three representative models (Qwen3-14B, DeepSeek-Coder-V2, and Devstral-Small-2505) in Table
1
and defer the full per-model breakdown to Appendix
D
.
Baselines.
We compare our method against two families.
Single-pass
methods score one greedy generation: Mean Entropy, which aggregate raw entropy without Top-
K
K
filtering.
Multi-pass
methods constitute the current state of the art for UE in both code and long-form text generation: Consistency (Basic) and Consistency (VR)
Huang et al. (2025)
, both using pairwise CodeBLEU
(
Malinin and Gales, 2021
)
; and Symbolic Clustering
(
Sharma and David, 2025
)
; Within our own framework, Max Entropy serves as natural
K
=
1
K{=}1
ablations of the lexical signal.
Metrics.
We measure discrimination with AUROC and ranking quality with PRAUC, with the positive class set to
correct
and
−
U
-U
(i.e., confidence) as the ranking score. Correctness is defined functionally: the label
y
=
1
y{=}1
iff the candidate program passes the problem’s
official
hidden test suite (
not
the self-generated tests of §
2.4
). This distinction is critical, since otherwise the functional signal would be trivially perfect by construction. We do not report Brier Score or ECE: post-hoc rank-normalized scores have no meaningful absolute calibration, and AUROC/PRAUC suffice to assess the underlying signal.
Hyperparameters.
For the lexical signal we use
K
=
5
K{=}5
(Top-
K
K
token entropy) on a single greedy generation (
τ
=
0
\tau{=}0
); sensitivity to
K
K
is reported in §
D.1
. For the algorithmic signal we sample
N
=
10
N{=}10
pseudo-code plans at temperature
τ
=
0.8
\tau{=}0.8
. For the functional signal we score the greedy candidate against
M
=
10
M{=}10
self-generated tests with a per-test execution timeout of 4 s; compile errors, runtime errors, and timeouts are treated as failures. Ensemble weights are fixed at
(
α
lex
,
α
func
,
α
algo
)
=
(
0.2
,
0.4
,
0.4
)
(\alpha_{\text{lex}},\alpha_{\text{func}},\alpha_{\text{algo}})=(0.2,0.4,0.4)
. Full prompt templates and additional decoding settings are in Appendix
B
.
4
Main Results
Method
APPS Intro
APPS Interview
HumanEval
MBPP
Average
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
Qwen3-14B
NL-derived baselines
Mean Entropy
.694
.700
.691
.414
.715
.941
.526
.565
.657
.655
Consistency (BLEU)
.742
.776
.723
.495
.694
.945
.640
.673
.700
.722
Consistency (VR)
.776
.798
.748
.525
.741
.955
.648
.684
.728
.741
Symb. Clustering
.764
.813
.690
.522
.673
.943
.661
.691
.697
.742
Three axes (ours)
Top-5 Entropy (LEX)
.813
.828
.798
.611
.729
.952
.570
.616
.728
.752
Pseudo Consistency (ALGO)
.713
.833
.604
.588
.718
.947
.615
.650
.662
.755
Generated Tests (FUNC)
.745
.787
.755
.549
.822
.958
.730
.702
.763
.749
Ensemble (ours)
Top-5 + Tests + Pseudo
.792
.870
.810
.725
.852
.983
.746
.761
.800
.835
DeepSeek-Coder-V2
NL-derived baselines
Mean Entropy
.483
.532
.528
.277
.376
.798
.544
.611
.483
.555
Consistency (BLEU)
.721
.767
.703
.470
.586
.850
.596
.641
.652
.682
Consistency (VR)
.759
.797
.747
.522
.635
.877
.616
.639
.689
.709
Symb. Clustering
.566
.643
.473
.277
.646
.895
.565
.639
.563
.614
Three axes (ours)
Top-5 Entropy (LEX)
.637
.668
.634
.368
.466
.827
.616
.653
.588
.629
Pseudo Consistency (ALGO)
.691
.802
.653
.500
.759
.832
.722
.636
.706
.693
Generated Tests (FUNC)
.708
.763
.692
.501
.861
.952
.741
.736
.751
.738
Ensemble (ours)
Top-5 + Tests + Pseudo
.749
.814
.747
.558
.842
.957
.740
.755
.770
.771
Devstral-Small-2505
NL-derived baselines
Mean Entropy
.491
.461
.558
.189
.612
.876
.528
.558
.547
.521
Consistency (BLEU)
.614
.624
.609
.246
.616
.885
.597
.621
.609
.594
Consistency (VR)
.745
.737
.675
.281
.644
.875
.611
.642
.669
.634
Symb. Clustering
.484
.506
.461
.190
.668
.893
.514
.575
.532
.541
Three axes (ours)
Top-5 Entropy (LEX)
.701
.651
.627
.239
.749
.934
.614
.653
.673
.619
Pseudo Consistency (ALGO)
.803
.704
.646
.433
.768
.939
.647
.620
.716
.674
Generated Tests (FUNC)
.747
.748
.712
.392
.819
.940
.776
.735
.764
.704
Ensemble (ours)
Top-5 + Tests + Pseudo
.752
.739
.734
.449
.886
.990
.791
.785
.791
.741
Table 1:
Main results on Qwen3-14B, DeepSeek-Coder-V2 and Devstral-Small-2505: AUROC (AUC) and PRAUC across four benchmarks. Per-model tables are in Appendix
D
. Bold indicates best performance; underline indicates second-best performance.
Table
1
reports AUROC and PRAUC on all four benchmarks for Qwen3-14B, DeepSeek-Coder-V2, and Devstral-Small-2505; Results on more models are availbale in Appendix
D
.
Each axis captures complementary uncertainty.
Top-
5
5
token entropy (lexical) excels on algorithmically demanding APPS subsets (0.813 AUROC on Intro for Qwen3-14B), matching the strongest multi-pass NL baseline (Consistency-vr: 0.728 average) at over 3
×
\times
lower cost. Generated Tests (functional) dominates on executable benchmarks, achieving 0.822 on HumanEval and 0.730 on MBPP. Pseudo-code consistency (algorithmic) provides orthogonal signal, particularly strong on Devstral-Small-2505 (0.716 average AUROC).
The ensemble yields substantial gains across all models.
The weighted ensemble (0.2/0.4/0.4) raises average AUROC to 0.800 for Qwen3-14B (+7.2 over best single signal), 0.770 for DeepSeek-Coder-V2 (+1.9), and 0.791 for Devstral-Small-2505 (+2.7), confirming complementarity. The ensemble is the top method on every benchmark in Table
1
, with particularly strong gains on HumanEval (0.852 AUROC, 0.983 PRAUC for Qwen3-14B).
5
Analysis
Orthogonality of the Three Signals.
Pair
Pearson
r
r
Spearman
ρ
\rho
Pseudo vs Test
0.0997
0.1085
Pseudo vs Entropy
0.1149
0.1154
Test vs Entropy
0.1830
0.2212
Table 2:
Pairwise correlations among the three signals on MBPP with Qwen3-Coder-30B. Low
correlations indicate largely non-redundant information.
Variant
AUROC
PRAUC
Full (P+T+E)
0.7478
0.7672
Drop P (T+E)
0.7392
0.7416
Drop T (P+E)
0.6172
0.6758
Drop E (P+T)
0.7457
0.7574
Table 3:
Drop-one ablation on MBPP with Qwen3-Coder-30B. Removing any signal degrades performance,
with the test signal (T) contributing most.
(a)
Disagreement-score distributions for correct vs. incorrect.
(b)
Counts of confidence signal per sample, by correctness.
Figure 2:
Per-sample disagreement analysis on Qwen3-Coder-30B on MBPP.
While Table
1
demonstrates that each axis outperforms NL-derived baselines individually and that the ensemble yields further gains, neither observation directly establishes that the three signals capture genuinely distinct information. We provide three complementary lines of evidence. First, pairwise correlations (Table
2
) are low, with Pearson and Spearman coefficients ranging 0.10–0.22; the lexical–functional pair is most decoupled (
r
=
0.183
r{=}0.183
,
ρ
=
0.221
\rho{=}0.221
), consistent with targeting structurally distinct failure modes (sparse high-entropy token decisions vs. end-to-end execution). Second, drop-one ablation (Table
3
) reveals non-trivial degradation when removing any signal: dropping the functional axis reduces AUROC by 13.1 points, while omitting algorithmic or lexical axes reduces AUROC by 0.9 and 0.2 points respectively, confirming no signal is subsumed by the other two. Third, per-sample disagreement analysis (Figure
2
) shows each axis is most reliable on distinct error classes: lexical on single-token failures, algorithmic when samples implement different solution strategies, and functional when code is syntactically valid but semantically incorrect.
Cost–Performance Pareto.
Figure 3:
Computational efficiency comparison of uncertainty estimation methods. Average time per problem on HumanEval (164 problems) with Qwen3-14B model.
Figure
3
reports wall-clock time per problem for entropy- and consistency-based methods on HumanEval with Qwen3-14B. Top-
K
K
entropy requires only 2.29 seconds per problem, approximately 3.1
×
\times
faster than sampling-based consistency via code (VR: 7.10s) and 2.9
×
\times
faster than pseudo-code consistency (6.55s). Generated test cases take 3.06 seconds, slightly slower than entropy but still 2.3
×
\times
faster than VR. Combined with Table
1
, this places Top-
K
K
entropy in the lower-left of the cost–AUROC plane (fast, competitive accuracy), while the full three-axis ensemble achieves the strongest overall performance by aggregating lexical, algorithmic, and functional signals. The full three-signal ensemble adds pseudo-code consistency, increasing runtime by 6.55s but yielding only marginal AUROC gains on most benchmarks. We therefore recommend Top-
K
K
entropy as the default for latency-sensitive settings (e.g., in-IDE autocomplete), and the full three-axis ensemble when calibration matters more than speed and the added cost of aggregating lexical, algorithmic, and functional signals is acceptable.
Code vs. Comment Entropy.
Token Scope
AUROC
↑
\uparrow
PRAUC
↑
\uparrow
All Tokens
0.728
0.752
Code Only
0.716
0.726
Comment Only
0.375
0.471
Table 4:
Top-5 max entropy applied to different token scopes (Qwen3-14B, averaged across datasets).
Code and comments serve fundamentally different roles in a program. Table
4
decomposes Top-
5
5
max entropy by token scope. Code-only entropy achieves competitive performance (AUROC 0.716), confirming that executable tokens carry the primary uncertainty signal. Comment-only entropy, by contrast, performs worse than random (AUROC 0.375), indicating that the model’s uncertainty about natural-language explanations anti-correlates with functional correctness. Yet all-token entropy (0.728) modestly outperforms code-only (0.716), suggesting that while comment tokens are individually unreliable, their entropy distribution interacts with code-token entropy to sharpen the overall rank ordering. This asymmetry is invisible to methods that aggregate uncertainty uniformly over the full sequence and would be missed by NL-derived baselines. Practitioners should retain comment tokens when computing entropy-based uncertainty but avoid relying on verbalized confidence as a proxy for code correctness. In summary, executable code tokens are the dominant source of uncertainty signal, yet naively discarding comments sacrifices a modest but consistent gain.
Generalization to Other Languages.
Method
C++
Java
Go
JS
Mean Entropy
.543
.624
.510
.582
Max Entropy
.649
.679
.660
.612
Mean Probability
.523
.502
.588
.513
Max Probability
Consistency (BLEU)
.581
.682
.651
.583
Consistency (VR)
.572
.665
.650
.597
Symb. Clustering
Top-5 Entropy (ours)
.648
.690
.673
.625
Pseudo Consistency(ours)
Generated Tests(ours)
Top-5 + Tests + Pseudo(ours)
Table 5:
Cross-language AUROC on Qwen3-Coder-30B (HumanEval-X). Top-
5
5
max entropy is consistently the
strongest signal among methods that transfer to non-Python settings.
We evaluate whether the lexical and consistency-based axes transfer to non-Python languages by testing Qwen3-Coder-30B on HumanEval-X (C++, Java, Go, JavaScript). The functional axis is omitted due to the complexity of a uniform sandbox across four languages. Table
5
shows that Top-
5
5
max entropy is the strongest signal on Java, Go and JS, tied on C++, outperforming both single-pass baselines (Max Entropy, Line Max) and the multi-pass consistency baseline (VR). This replicates the Python finding and confirms that the lexical uncertainty signal generalizes across programming languages.
Practical guidance.
Top-
K
K
token entropy
is the default for latency-sensitive settings (e.g., in-IDE autocomplete): it is single-pass and competitive with sampling-based methods. The
full three-signal ensemble
(Top-
K
K
+ behavioral consistency + pseudo-code consistency) provides the strongest average performance when calibration matters more than latency and the added cost is acceptable. The algorithmic axis is best used as a complement, not in isolation.
6
Related Work
Uncertainty estimation for natural language generation.
Confidence and uncertainty estimation in LLMs has been studied along several axes: post-hoc calibration
(
Guo et al., 2017
;
Zadrozny and Elkan, 2002
)
, sampling-based consistency and semantic clustering
(
Kuhn et al., 2023
;
Malinin and Gales, 2021
;
Lin et al., 2024
)
, verbalized confidence and P(True) prompts
(
Tian et al., 2023
;
Xiong et al., 2024
;
Kadavath et al., 2022
)
, and long-form decomposition into atomic claims
(
Zhang et al., 2025
;
Zhang et al., 2024
)
; surveys cover the landscape
(
Geng et al., 2024
;
Xiong et al., 2024
)
. A complementary thread highlights token-level entropy as a useful signal for confidence or reasoning quality in NL and code tasks
(
Wang et al., 2025
;
Li et al., 2026
;
Cooper and Scholak, 2024
;
Zeng et al., 2025
;
Shi et al., 2025a
)
.
None of these methods is code-aware:
they view programs merely as token sequences, relying on uniform sequence uncertainty and surface clustering to approximate semantic consistency, without accounting for executability. Our framework keeps the multi-sample-agreement intuition of consistency-based methods but instantiates it at code-specific abstraction levels, and motivates Top-
K
K
aggregation specifically from token fragility.
Uncertainty and self-verification for code.
Direct work on code UE is sparse.
Sharma and David (2025)
adapt entropy- and mutual-information-based UE to code with a symbolic-execution semantic-equivalence check; LUQ
(
Zhang et al., 2024
)
is a sampling-based UE method for long-form generation; structural-entropy
(
Song et al., 2025
)
and complexity-feedback
(
Sepidband et al., 2025
)
derive signals from candidate programs themselves. A parallel line uses self-generated tests to
select
or
repair
programs rather than score uncertainty: CodeT
(
Chen et al., 2023
)
ranks candidates by self-test pass count, while self-debug
(
Chen et al., 2024
;
Shi et al., 2025b
;
Li et al., 2025
;
Chen et al., 2025
)
and self-edit
(
Zhang et al., 2023
)
iteratively repair programs from execution feedback.
Each existing UE method commits to a single equivalence definition,
covering implementation-level symbolic execution, surface sampling and natural language-derived atomic claim decomposition while self-verification outputs selected programs instead of calibration cues. We contend no single equivalence standard suits code, defining lexical, algorithmic and functional disagreement as three orthogonal dimensions and tests their orthogonality (§
5
); the functional axis can be layered on top of CodeT-style selection without conflict.
7
Conclusion
We introduce a three-axis framework for code uncertainty estimation that maps one-to-one onto three properties distinguishing code from natural language: token fragility, two-level structure, and executability. Across four benchmarks and five code LLMs, the three axes provide complementary signals for code uncertainty estimation. In our main Qwen3-14B setting, Top-
K
K
entropy alone matches the strongest multi-pass NL baseline at over 3
×
\times
lower cost, while across models it remains a competitive low-cost estimator. The full three-axis ensemble further improves average AUROC, reaching 0.800 on Qwen3-14B and 0.776 across all five models. Our results suggest that as code-LLM deployment matures, calibration, not further capability scaling, becomes the bottleneck, and code-specific signals such as type checks, static analyses, and runtime traces should expand the framework rather than be forced into NL-style estimators.
Limitations
Our study focuses on Python code generation with hidden test suites; preliminary cross-language results (Section
5
) suggest the lexical and consistency axes transfer, and extending the framework to open-ended code tasks such as refactoring and multi-file edits is a natural next step. The functional axis assumes an executable environment, which is standard in code-generation benchmarks but not universal; the lexical and algorithmic axes remain applicable when execution is unavailable. We evaluate discrimination and ranking quality (AUROC, PRAUC) and leave the study of downstream utility (selective generation, human-in-the-loop review, agentic deferral) to future work.
AI Usage Disclosure
The authors used ChatGPT to refine the manuscript’s grammar. All AI-assisted text was reviewed and revised by the authors, who take full responsibility for the
final version.
Ethical Statement
This study uses only publicly available datasets (APPS, HumanEval, MBPP), obtained and cited in compliance with their respective licenses. No private data, human
subjects, or sensitive information are involved, and the work follows standard academic integrity norms, with research-derived data not used outside research contexts.
References
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
§1
,
§3
.
Chen
et al.
(2023)
B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J. Lou, and W. Chen
CodeT: code generation with generated tests
.
In
The Eleventh International Conference on Learning Representations,
ICLR 2023, Kigali, Rwanda, May 1-5, 2023
,
External Links:
Link
Cited by:
§1
,
§2.4
,
§6
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
§2.1
,
§3
.
Chen
et al.
(2025)
S. Chen, S. Lin, X. Gu, Y. Shi, H. Lian, L. Yun, D. Chen, W. Sun, L. Cao, and Q. Wang
SWE-exp: experience-driven software issue resolution
.
arXiv preprint arXiv:2507.23361
.
Cited by:
§6
.
Chen
et al.
(2024)
X. Chen, M. Lin, N. Schärli, and D. Zhou
Teaching large language models to self-debug
.
In
The Twelfth International Conference on Learning Representations,
ICLR 2024, Vienna, Austria, May 7-11, 2024
,
External Links:
Link
Cited by:
§6
.
Cooper and Scholak (2024)
N. Cooper and T. Scholak
Perplexed: understanding when large language models are confused
.
External Links:
2404.06634
,
Link
Cited by:
§6
.
Geng
et al.
(2024)
J. Geng, F. Cai, Y. Wang, H. Koeppl, P. Nakov, and I. Gurevych
A survey of confidence estimation and calibration in large language models
.
In
Proceedings of the 2024 Conference of the North American Chapter of
the Association for Computational Linguistics: Human Language Technologies
(Volume 1: Long Papers), NAACL 2024, Mexico City, Mexico, June 16-21,
2024
,
K. Duh, H. Gómez-Adorno, and S. Bethard (Eds.)
,
pp. 6577–6595
.
External Links:
Link
,
Document
Cited by:
§6
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
Proceedings of the 34th International Conference on Machine Learning,
ICML 2017, Sydney, NSW, Australia, 6-11 August 2017
,
D. Precup and Y. W. Teh (Eds.)
,
Proceedings of Machine Learning Research
,
pp. 1321–1330
.
External Links:
Link
Cited by:
§6
.
Hendrycks
et al.
(2021)
D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song, and J. Steinhardt
Measuring coding challenge competence with APPS
.
In
Proceedings of the Neural Information Processing Systems Track on
Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December
2021, virtual
,
J. Vanschoren and S. Yeung (Eds.)
,
External Links:
Link
Cited by:
§3
.
Huang
et al.
(2025)
Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma
Look before you leap: an exploratory study of uncertainty analysis for large language models
.
IEEE Trans. Software Eng.
51
(
2
),
pp. 413–429
.
External Links:
Link
,
Document
Cited by:
§3
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
§6
.
Kuhn
et al.
(2023)
L. Kuhn, Y. Gal, and S. Farquhar
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
In
The Eleventh International Conference on Learning Representations,
ICLR 2023, Kigali, Rwanda, May 1-5, 2023
,
External Links:
Link
Cited by:
§1
,
§2.3
,
§6
.
Li
et al.
(2025)
H. Li, Y. Shi, S. Lin, X. Gu, H. Lian, X. Wang, Y. Jia, T. Huang, and Q. Wang
SWE-debate: competitive multi-agent debate for software issue resolution
.
arXiv preprint arXiv:2507.23348
.
Cited by:
§6
.
Li
et al.
(2026)
X. Li, E. Callanan, A. Ghassel, and X. Zhu
Entropy-gated branching for efficient test-time reasoning
.
In
Proceedings of the 19th Conference of the European Chapter of the
Association for Computational Linguistics, EACL 2026 - Volume 1:
Long Papers, Rabat, Morocco, March 24-29, 2026
,
V. Demberg, K. Inui, and L. Marquez (Eds.)
,
pp. 5054–5069
.
External Links:
Link
Cited by:
§6
.
Lin
et al.
(2024)
Z. Lin, S. Trivedi, and J. Sun
Generating with confidence: uncertainty quantification for black-box large language models
.
Trans. Mach. Learn. Res.
2024
.
External Links:
Link
Cited by:
§6
.
Malinin and Gales (2021)
A. Malinin and M. J. F. Gales
Uncertainty estimation in autoregressive structured prediction
.
In
9th International Conference on Learning Representations, ICLR 2021,
Virtual Event, Austria, May 3-7, 2021
,
External Links:
Link
Cited by:
§1
,
§2.3
,
§3
,
§6
.
Rastogi
et al.
(2025)
A. Rastogi, A. Yang, A. Q. Jiang, A. H. Liu, A. Sablayrolles, A. Héliou, A. Martin, A. Agarwal, A. Ehrenberg, A. Lo, A. Roux, A. Darcet, A. Mensch, B. Bout, B. Rozière, B. D. Monicault, C. Bamford, C. Wallenwein, C. Renaudin, C. Lanfranchi, C. Denoix, C. Barreau, D. D. D. Mizelle, D. de las Casas, E. Chane-Sane, E. Fugier, E. B. Hanna, G. Berrada, G. Delerce, G. Guinet, G. Novikov, G. Neubig, G. Lample, G. Martin, H. Jaju, J. Ludziejewski, J. Rute, J. Delignon, J. Chabran, J. Studnia, J. Barmentlo, J. Amar, J. S. Roberts, J. Denize, K. Saxena, K. Yadav, K. Khandelwal, K. R. Chandu, K. Jain, L. R. Lavaud, L. Blier, L. Zhao, L. Martin, L. Saulnier, L. Gao, M. Pellat, M. Guillaumin, M. Felardos, M. Dinot, M. Darrin, M. Augustin, M. Seznec, N. Gupta, N. Raghuraman, O. Duchenne, P. Wang, P. von Platen, P. Saffer, P. Jacob, P. Wambergue, P. Kurylowicz, P. Chagniot, P. Stock, P. Agrawal, R. Delacourt, R. Soletskyi, R. Sauvestre, S. Vaze, S. Gandhi, S. Subramanian, S. Dalal, S. Gandhi, S. Ghosh, S. Mishra, S. Aithal, S. Antoniak, T. L. Scao, T. Lavril, T. Schueller, T. Foubert, T. Robert, T. Wang, T. Lacroix, T. Bewley, V. Nemychnikova, V. Paltz, V. Richard, W. Li, W. Marshall, X. Wang, X. Zhang, Y. Wan, and Y. Tang
Devstral: fine-tuning language models for coding agent applications
.
External Links:
2509.25193
,
Link
Cited by:
§3
.
Sepidband
et al.
(2025)
M. Sepidband, H. Taherkhani, S. Wang, and H. Hemmati
Enhancing llm-based code generation with complexity metrics: A feedback-driven approach
.
In
49th IEEE Annual Computers, Software, and Applications Conference,
COMPSAC 2025, Toronto, ON, Canada, July 8-11, 2025
,
H. Shahriar, K. S. Alam, H. Ohsaki, S. Cimato, M. A. M. Capretz, S. Ahmed, S. I. Ahamed, A. J. A. Majumder, M. Haque, T. Yoshihisa, A. Cuzzocrea, M. Takemoto, N. Sakib, and M. Elsayed (Eds.)
,
pp. 1416–1426
.
External Links:
Link
,
Document
Cited by:
§6
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
§1
,
§3
,
§6
.
Shi
et al.
(2025a)
Y. Shi, Y. Qian, H. Zhang, B. Shen, and X. Gu
LongCodeZip: compress long context for code language models
.
arXiv preprint arXiv:2510.00446
.
Cited by:
§6
.
Shi
et al.
(2025b)
Y. Shi, S. Wang, C. Wan, M. Wang, and X. Gu
From code to correctness: closing the last mile of code generation with hierarchical debugging
.
External Links:
2410.01215
,
Link
Cited by:
§6
.
Shi
et al.
(2025c)
Y. Shi, H. Zhang, C. Wan, and X. Gu
Between lines of code: unraveling the distinct patterns of machine and human programmers
.
In
47th IEEE/ACM International Conference on Software Engineering,
ICSE 2025, Ottawa, ON, Canada, April 26 - May 6, 2025
,
pp. 1628–1639
.
External Links:
Link
,
Document
Cited by:
§1
.
Song
et al.
(2025)
Y. Song, T. Sun, X. Tang, P. Rajput, T. F. Bissyandé, and J. Klein
Measuring LLM code generation stability via structural entropy
.
In
40th IEEE/ACM International Conference on Automated Software Engineering,
ASE 2025, Seoul, Korea, Republic of, November 16-20, 2025
,
pp. 3922–3926
.
External Links:
Link
,
Document
Cited by:
§6
.
Tian
et al.
(2023)
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. D. Manning
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
In
Proceedings of the 2023 Conference on Empirical Methods in Natural
Language Processing, EMNLP 2023, Singapore, December 6-10, 2023
,
H. Bouamor, J. Pino, and K. Bali (Eds.)
,
pp. 5433–5442
.
External Links:
Link
,
Document
Cited by:
§6
.
Wang
et al.
(2025)
S. Wang, L. Yu, C. Gao, C. Zheng, S. Liu, R. Lu, K. Dang, X. Chen, J. Yang, Z. Zhang, Y. Liu, A. Yang, A. Zhao, Y. Yue, S. Song, B. Yu, G. Huang, and J. Lin
Beyond the 80/20 rule: high-entropy minority tokens drive effective reinforcement learning for llm reasoning
.
External Links:
2506.01939
,
Link
Cited by:
§6
.
Xiong
et al.
(2024)
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi
Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms
.
In
The Twelfth International Conference on Learning Representations,
ICLR 2024, Vienna, Austria, May 7-11, 2024
,
External Links:
Link
Cited by:
§6
.
Yang
et al.
(2025)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu
Qwen3 technical report
.
External Links:
2505.09388
,
Link
Cited by:
§3
.
Zadrozny and Elkan (2002)
B. Zadrozny and C. Elkan
Transforming classifier scores into accurate multiclass probability estimates
.
In
Proceedings of the Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining
,
KDD ’02
,
New York, NY, USA
,
pp. 694–699
.
External Links:
ISBN 158113567X
,
Link
,
Document
Cited by:
§6
.
Zeng
et al.
(2025)
W. Zeng, Y. Wang, C. Hu, Y. Shi, C. Wan, H. Zhang, and X. Gu
Pruning the unsurprising: efficient code reasoning via first-token surprisal
.
arXiv preprint arXiv:2508.05988
.
Cited by:
§6
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
§1
,
§1
,
§6
,
§6
.
Zhang
et al.
(2025)
C. Zhang, R. Yang, Z. Zhang, X. Huang, S. Yang, D. Yu, and N. Collier
Atomic calibration of llms in long-form generations
.
In
Proceedings of the 14th International Joint Conference on Natural
Language Processing and the 4th Conference of the Asia-Pacific Chapter
of the Association for Computational Linguistics, IJCNLP-AACL 2025,
Mumbai, India, December 20-24, 2025
,
K. Inui, S. Sakti, H. Wang, D. F. Wong, P. Bhattacharyya, B. Banerjee, A. Ekbal, T. Chakraborty, and D. P. Singh (Eds.)
,
pp. 148–169
.
External Links:
Link
Cited by:
§6
.
Zhang
et al.
(2023)
K. Zhang, Z. Li, J. Li, G. Li, and Z. Jin
Self-edit: fault-aware code editor for code generation
.
In
Proceedings of the 61st Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada,
July 9-14, 2023
,
A. Rogers, J. L. Boyd-Graber, and N. Okazaki (Eds.)
,
pp. 769–787
.
External Links:
Link
,
Document
Cited by:
§6
.
Zhu
et al.
(2024)
Q. Zhu, D. Guo, Z. Shao, D. Yang, P. Wang, R. Xu, Y. Wu, Y. Li, H. Gao, S. Ma,
et al.
DeepSeek-Coder-V2: breaking the barrier of closed-source models in code intelligence
.
arXiv preprint arXiv:2406.11931
.
Cited by:
§3
.
Appendix A
Prompts
This section provides the exact prompts used in our experiments for code generation, pseudo-code generation, and test case generation.
A.1
Code Generation Prompt
We use a unified prompt template across all benchmarks (HumanEval, MBPP, and APPS):
⬇
<
user
>
Complete
the
following
Python
Code
:
{
problem_description
}
Output
only
the
complete
code
with
brief
comments
,
when
you
output
“‘,
the
code
should
be
complete
and
executable
and
you
should
stop
immediately
.
</
user
>
<
assistant
>
<
think
></
think
>
Here
are
the
complete
codes
for
this
problem
:
“‘
python
where
{problem_description}
contains the function signature and docstring for HumanEval/MBPP, or the full problem statement with optional starter code for APPS. Code generation uses greedy decoding (temperature=0.0, top-p=0.95, max_tokens=1024).
A.2
Pseudo-Code Generation Prompt
For pseudo-code consistency estimation, we generate multiple high-level solution plans without writing actual code:
⬇
<
user
>
Read
the
problem
and
describe
the
solution
logic
in
a
step
-
by
-
step
plan
.
Problem
:
{
problem_description
}
Write
a
solution
plan
with
6-10
numbered
steps
that
:
-
Describes
the
core
algorithm
logic
and
reasoning
-
Explains
what
needs
to
be
done
and
why
-
Uses
natural
language
like
"
examine
each
item
",
"
keep
track
of
",
"
compare
values
"
-
Avoids
programming
constructs
(
no
"
for
",
"
while
",
"
if
-
else
",
variable
assignments
)
-
Focuses
on
the
logical
flow
:
"
first
do
X
,
then
check
Y
,
finally
return
Z
"
Output
the
plan
directly
.
</
user
>
<
assistant
>
<
think
></
think
>
Solution
plan
:
We generate 10 pseudo-code plans per problem using temperature sampling (Temperature=0.8, Top-p=0.95, Max_tokens=2048) and compute pairwise step-aware ROUGE-L similarity to measure reasoning consistency.
A.3
Test Case Generation Prompt
⬇
<
user
>
Generate
{
num_test_cases
}
DIFFERENT
test
cases
for
this
function
.
DO
NOT
implement
the
function
.
Function
Specification
:
{
problem_description
}
Requirements
:
1.
Generate
exactly
{
num_test_cases
}
diverse
test
cases
as
valid
Python
assert
statements
2.
Use
the
exact
function
name
and
parameters
from
the
specification
3.
Cover
different
scenarios
:
edge
cases
,
normal
cases
,
boundary
conditions
4.
Output
ONLY
valid
JSON
array
with
{
num_test_cases
}
assert
statements
JSON
format
:
[
"
assert
function_name
(
args1
)
==
expected1
",
"
assert
function_name
(
args2
)
==
expected2
",
…
]
Output
only
the
JSON
,
when
you
output
“‘,
the
JSON
should
be
complete
and
you
should
stop
immediately
.
</
user
>
<
assistant
>
<
think
></
think
>
Here
are
the
test
cases
in
JSON
format
:
“‘
json
We generate test cases to evaluate code correctness without executing against ground-truth tests:
We generate 10 test cases per problem using sampling decoding (Temperature=0.8, Top-p=0.95, Max_tokens=1024). For APPS problems with standard I/O format, we adapt the output to
{"input": "...", "output": "..."}
pairs instead of assert statements.
Appendix B
Hyperparameters and Experiment Details
Hyperparameter
Value
Descriptions
Temperatures
τ
\tau
when generating outputs
0
Greedy decoding for deterministic final outputs
Temperatures
τ
\tau
for entropy analysis
1
Sampling temperature for entropy distribution analysis
Temperatures
τ
\tau
during consistent calculation
0.8
Sampling temperature for generating
diverse code samples in VR and algorithmic consistency
Temperatures
τ
\tau
when generating pseudo codes
0.8
Sampling temperature for diverse
pseudo-code generation
Temperatures
τ
\tau
when generating testcases
0.8
Sampling temperature for diverse test case
generation
Sample Number
N
N
10
Number of samples per problem for consistency metrics
Test Case Number
M
M
10
Number of test cases per code for functional uncertainty
Top-K
K
K
5
Number of highest-entropy tokens for Top5_ent metric
Ensemble Weights
α
lex
\alpha_{\text{lex}}
,
α
algo
\alpha_{\text{algo}}
,
α
func
\alpha_{\text{func}}
0.2, 0.4,
0.4
Combination weights for lexical, algorithmic, and functional uncertainty
Top_P
0.95
Nucleus sampling threshold for all diverse generation
Seed
42
Random seed for reproducibility
Table 6:
Hyperparameter settings and configurations for uncertainty estimation and output generation.
In our experiments, we use 10 samples per instance for consistency calculation and clustering. As depicted in Table
6
,
for the LLM, we set the temperature to 0.8 during consistency calculation and to 0 when
generating outputs for entropy computation. The temperature is set to 1 when generating
perturbed results for entropy analysis. For Top-
K
K
max entropy we use
K
=
5
K{=}5
as the default.
The ensemble weights used in the main results are
α
lexical
=
0.2
\alpha_{\text{lexical}}{=}0.2
,
α
functional
=
0.4
\alpha_{\text{functional}}{=}0.4
,
α
algorithmic
=
0.4
\alpha_{\text{algorithmic}}{=}0.4
after rank-normalization.
Appendix C
Analysis of Ensemble
To determine the optimal ensemble weights (
α
lex
\alpha_{\text{lex}}
,
α
algo
\alpha_{\text{algo}}
, and
α
func
\alpha_{\text{func}}
), we perform a simple grid search on a small held-out validation set partitioned from the training data, rather than tuning directly on the evaluation benchmarks. We evaluate the combination of weights with a step size of 0.1 and select the configuration that maximizes the overall AUROC score. The performance remains consistently high across a broad range of weight combinations, demonstrating that our ensemble method is robust to hyperparameter choices and does not suffer from severe overfitting.
Appendix D
Per-Model, Per-Dataset Results
Table
9
and Table
10
report AUROC and PRAUC for all five models across all four benchmarks, including single-pass entropy methods, multi-pass NL-derived consistency baselines, our functional axis (Generated Tests), and both ensembles. The Qwen3-14B block reproduces Table
1
for reference.
Model
APPS Intro
APPS Interview
HumanEval
MBPP
Average
Acc
AUROC
PRAUC
Acc
AUROC
PRAUC
Acc
AUROC
PRAUC
Acc
AUROC
PRAUC
Acc
AUROC
PRAUC
Qwen3-14B
0.569
0.745
0.787
0.282
0.755
0.549
0.875
0.822
0.958
0.540
0.730
0.702
0.567
0.763
0.749
Qwen3-32B
0.590
0.742
0.804
0.281
0.770
0.571
0.869
0.756
0.938
0.580
0.711
0.724
0.580
0.745
0.759
Qwen3-Coder-30B
0.606
0.749
0.809
0.341
0.738
0.576
0.950
0.734
0.973
0.556
0.731
0.722
0.613
0.738
0.770
DeepSeek-Coder-V2
0.549
0.708
0.763
0.261
0.692
0.501
0.825
0.861
0.952
0.564
0.741
0.736
0.550
0.751
0.738
Devstral-Small-2505
0.479
0.747
0.748
0.161
0.712
0.392
0.799
0.819
0.940
0.530
0.776
0.735
0.492
0.764
0.704
Table 7:
Problem-level evaluation of LLM-generated test cases as a proxy for code correctness.
Across all five models, ensemble consistently dominates:
The
Top-5 + Tests + Pseudo
ensemble achieves the best (or tied-best) performance on every {model, dataset} cell tested, demonstrating that the three axes—lexical (LEX), algorithmic (ALGO), and functional (FUNC)—capture complementary signals. While individual methods show dataset-specific strengths (Top-5 Entropy excels on APPS, Generated Tests on HumanEval/MBPP), the ensemble robustly combines their advantages: it matches or exceeds the best single method on each benchmark, with gains of up to +8.7 PRAUC points (Qwen3-14B on APPS Interview) over the strongest baseline. The relative contribution of each axis varies by model—stronger code models (Qwen3-Coder-30B, Devstral-Small-2505) benefit more from lexical diversity, while smaller models (DeepSeek-Coder-V2) gain more from functional verification—but the ensemble remains the most reliable estimator across all settings.
D.1
Method-specific Ablations
Figure 4:
AUROC of Top-
K
K
entropy as a function of
K
K
, averaged across models and benchmarks. Performance improves from
K
=
1
K{=}1
to
K
=
5
K{=}5
, then plateaus.
Figure 5:
AUROC and PRAUC of testcases as a function of the testcase number.Performance is the best when the number is 10.
Top-
K
K
entropy: a small
K
K
captures most of the signal; performance plateaus around
K
=
5
K{=}5
(§
D.1
).
Figure
4
shows how AUROC varies with
K
K
. Performance improves steadily from
K
=
1
K{=}1
(max entropy) to
K
=
5
K{=}5
and then plateaus, matching the
token fragility
hypothesis: a few high-entropy tokens carry the most informative uncertainty signal, and as
K
K
grows, lower-entropy boilerplate tokens dilute it. We use
K
=
5
K{=}5
as the default.
D.2
Pseudo-Code Preserves Algorithmic Information
We validate that pseudo-code retains the information needed for correct implementation. On 100 MBPP problems, we provide [MODEL] with the reference solution and prompt it to produce pseudo-code, then ask Qwen3-14B to implement each problem conditioned on the pseudo-code. Pass@1 reaches 98%, compared to 54% for Qwen3-14B’s unconditional generation on MBPP (Table
8
). This confirms that pseudo-code abstracts away surface implementation details while preserving the algorithmic content needed for correctness, justifying it as the abstraction level for our algorithmic signal.
Test-case consistency: discrimination improves with more self-generated tests, but plateaus below the oracle (§
D.2
).
This suggests room for test-generation strategies optimized for uncertainty estimation (coverage- or boundary-aware prompts) rather than for program selection.
Appendix E
Compute Budget
All experiments were conducted on a single NVIDIA A100-SXM4-80GB GPU. We report the GPU hours required for each uncertainty estimation method
on the HumanEval benchmark (164 problems) using the Qwen3-14B model (14B parameters).
Per-experiment GPU hours:
•
Consistency(VR):
0.32 hours (1161s generation + 4s VR calculation + 2s metrics execution = 1167s total)
•
Pseudo-code Consistency:
0.30 hours (1067s generation + 8s VR calculation + 2s metrics execution = 1077s total)
•
Top5 Token Entropy:
0.10 hours (210s generation + 163s entropy calculation + 2s metrics execution = 375s total)
•
Behavioral Consistency:
0.14 hours (231s generation + 269s test generation + 2s execution = 502s total)
Appendix F
Pass Rates of Generated Results
Table
8
presents the pass@1 rates of our code solutions generated by the five evaluated LLMs across all four benchmarks. Model performance varies across benchmarks and these results validate the reliability of our dataset used in the uncertainty estimation.
Model
APPS Introductory
APPS Interview
HumanEval
MBPP
Qwen3-Coder-30B
61.20%
31.50%
94.51%
56.00%
Qwen3-14B
56.60%
28.60%
88.41%
54.20%
Qwen3-32B
58.90%
27.30%
87.80%
58.00%
DeepSeek-Coder-V2
53.40%
26.00%
81.10%
57.00%
Devstral-Small-2505
48.00%
16.00%
80.49%
52.00%
Table 8:
Pass rate of generated codes.
Method
APPS Intro
APPS Interview
HumanEval
MBPP
Average
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
Qwen3-14B
NL-derived baselines
Mean Entropy
.694
.700
.691
.414
.715
.941
.526
.565
.657
.655
Max Entropy
.724
.767
.672
.411
.601
.898
.532
.569
.632
.661
Mean Probability
.716
.751
.582
.408
.619
.902
.518
.555
.609
.654
Max Probability
.720
.718
.625
.513
.630
.935
.521
.564
.624
.683
Consistency (BLEU)
.742
.776
.723
.495
.694
.945
.640
.673
.700
.722
Consistency (VR)
.776
.798
.748
.525
.741
.955
.648
.684
.728
.741
Symb. Clustering
.764
.813
.690
.522
.673
.943
.661
.691
.697
.742
Three axes (ours)
Top-5 Entropy (LEX)
.813
.828
.798
.611
.729
.952
.570
.616
.728
.752
Pseudo Consistency (ALGO)
.713
.833
.604
.588
.718
.947
.615
.650
.662
.755
Generated Tests (FUNC)
.745
.787
.755
.549
.822
.958
.730
.702
.763
.749
Ensemble (ours)
Top-5 + Tests + Pseudo
.792
.870
.810
.725
.852
.983
.746
.761
.800
.835
DeepSeek-Coder-V2
NL-derived baselines
Mean Entropy
.483
.532
.528
.277
.376
.798
.544
.611
.483
.555
Max Entropy
.503
.534
.652
.349
.412
.826
.601
.620
.542
.582
Mean Probability
.499
.528
.519
.318
.393
.767
.596
.612
.502
.556
Max Probability
.510
.530
.546
.341
.425
.788
.617
.634
.525
.573
Consistency (BLEU)
.721
.767
.703
.470
.586
.850
.596
.641
.652
.682
Consistency (VR)
.759
.797
.747
.522
.635
.877
.616
.639
.689
.709
Symb. Clustering
.566
.643
.473
.277
.646
.895
.565
.639
.563
.614
Three axes (ours)
Top-5 Entropy (LEX)
.637
.668
.634
.368
.466
.827
.616
.653
.588
.629
Pseudo Consistency (ALGO)
.691
.802
.653
.500
.759
.832
.722
.636
.706
.693
Generated Tests (FUNC)
.708
.763
.692
.501
.861
.952
.741
.736
.751
.738
Ensemble (ours)
Top-5 + Tests + Pseudo
.749
.814
.747
.558
.842
.957
.740
.755
.770
.771
Devstral-Small-2505
NL-derived baselines
Mean Entropy
.491
.461
.558
.189
.612
.876
.528
.558
.547
.521
Max Entropy
.508
.469
.544
.200
.619
.881
.532
.563
.551
.528
Mean Probability
.515
.512
.549
.208
.675
.889
.529
.561
.567
.543
Max Probability
.504
.510
.567
.237
.680
.902
.535
.570
.572
.555
Consistency (BLEU)
.614
.624
.609
.246
.616
.885
.597
.621
.609
.594
Consistency (VR)
.745
.737
.675
.281
.644
.875
.611
.642
.669
.634
Symb. Clustering
.484
.506
.461
.190
.668
.893
.514
.575
.532
.541
Three axes (ours)
Top-5 Entropy (LEX)
.701
.651
.627
.239
.749
.934
.614
.653
.673
.619
Pseudo Consistency (ALGO)
.803
.704
.646
.433
.768
.939
.647
.620
.716
.674
Generated Tests (FUNC)
.747
.748
.712
.392
.819
.940
.776
.735
.764
.704
Ensemble (ours)
Top-5 + Tests + Pseudo
.752
.739
.734
.449
.886
.990
.791
.785
.791
.741
Table 9:
Full uncertainty estimation results: Qwen3-14B, DeepSeek-Coder-V2, and Devstral-Small-2505
Method
APPS Intro
APPS Interview
HumanEval
MBPP
Average
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
AUROC
PRAUC
Qwen3-32B
NL-derived baselines
Mean Entropy
.450
.561
.532
.291
.490
.868
.544
.617
.504
.584
Max Entropy
.460
.559
.491
.283
.523
.889
.532
.632
.502
.591
Mean Probability
.469
.602
.520
.316
.530
.900
.580
.658
.525
.619
Max Probability
.467
.605
.528
.323
.549
.899
.573
.660
.529
.622
Consistency (BLEU)
.739
.797
.705
.479
.516
.885
.603
.664
.641
.706
Consistency (VR)
.799
.843
.762
.587
.574
.898
.663
.713
.700
.760
Symb. Clustering
.665
.776
.610
.477
.654
.922
.560
.660
.622
.709
Three axes (ours)
Top-5 Entropy (LEX)
.573
.644
.616
.369
.613
.902
.592
.657
.599
.643
Pseudo Consistency (ALGO)
.671
.753
.642
.448
.621
.915
.611
.656
.636
.693
Generated Tests (FUNC)
.743
.804
.770
.571
.756
.938
.711
.724
.745
.759
Ensemble (ours)
Top-5 + Tests + Pseudo
.759
.884
.768
.603
.734
.944
.727
.738
.747
.792
Qwen3-Coder-30B
NL-derived baselines
Mean Entropy
.670
.710
.655
.458
.581
.957
.585
.627
.623
.688
Max Entropy
.780
.806
.722
.546
.678
.977
.570
.607
.688
.734
Mean Probability
.612
.659
.619
.518
.662
.951
.510
.610
.601
.684
Max Probability
.633
.692
.643
.522
.667
.960
.536
.609
.620
.696
Consistency (BLEU)
.736
.781
.725
.544
.705
.981
.600
.619
.692
.731
Consistency (VR)
.689
.733
.667
.483
.578
.962
.528
.560
.616
.685
Symb. Clustering
.612
.697
.550
.434
.517
.960
.592
.616
.568
.677
Three axes (ours)
Top-5 Entropy (LEX)
.807
.822
.756
.580
.591
.967
.599
.629
.688
.750
Pseudo Consistency (ALGO)
.721
.838
.610
.672
.671
.973
.602
.660
.651
.786
Generated Tests (FUNC)
.749
.809
.738
.576
.734
.973
.731
.722
.738
.770
Ensemble (ours)
Top-5 + Tests + Pseudo
.796
.852
.800
.614
.746
.980
.748
.767
.773
.803
Table 10:
Additional full uncertainty estimation results: Qwen3-32B and Qwen3-Coder-30B