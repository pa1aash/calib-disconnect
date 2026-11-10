---
title: 'Verbalized Uncertainty in Coding LLMs: Contamination-Aware Calibration (UncertaiNLP
  2026, full text PDF)'
id: verbalized-uncertainty-in-coding-llms-contamination-aware-calibration-uncertainl
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
created: '2026-11-09T23:11:24.603602Z'
updated: '2026-11-09T23:27:44.713991Z'
source: https://aclanthology.org/2026.uncertainlp-main.21.pdf
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT. Tuerlings and Valdenegro-Toro (UncertaiNLP 2026, pp 328-355):
  six instruct coder models (Qwen2.5-Coder 7B/32B, CodeLlama 7B/34B, DeepSeek-Coder
  6.7B/33B), 365 LiveCodeBench v6 problems in a shared window 2024-09-19..2025-04-30,
  three verbal elicitation formats on frozen code. All 18 NCE negative; 8/18 collapsed,
  5 unstable; ECE and AUROC decouple (Table 1). Verbal-only: no probes, no base/instruct
  pairs, no reasoning models, no per-model release-date split. Close occupant of L1
  (post-cutoff window) and verbal side of L2.'
---

Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of
 Confidence Calibration
 Hunter Tuerlings and Matias Valdenegro-Toro
 Department of Artificial Intelligence
 University of Groningen
 h.f.m.tuerlings@student.rug.nl, m.a.valdenegro.toro@rug.nl
 Abstract yet 46% actively distrust the accuracy of the output
 they receive (Stack Overflow, 2025).
 Coding large language models (LLMs) can
 A natural response is to pair each generated so-
 produce plausible solutions that fail hidden
 test cases, making it difficult to judge when lution with a confidence score, giving developers
 to trust their output. This paper presents some insight into how much review the code might
 a contamination-aware comparison of estab- need (Spiess et al., 2025). A confidence score is a
 lished methods for eliciting verbalized con- number, here on a 0 to 100 scale, expressing how
 fidence in generated code. Six instruction- likely the model judges its own output to be cor-
 tuned, coding-specialized LLMs from three rect, and an uncertainty estimate is the same score
 model families are evaluated on 365 prob-
 read in reverse. Such a score is only useful if it
 lems from a shared contamination-aware L IVE -
 C ODE B ENCH window. For each frozen code is well calibrated, meaning predictions made with
 generation, confidence is elicited separately 70% confidence should be correct about 70% of
 under three strategies, Direct numeric scor- the time (Geng et al., 2024).
 ing, Chain-of-Thought reasoning followed by The score studied here comes from verbalized
 a score, and Linguistic confidence labels. Un- confidence elicitation, in which the model states its
 der strict scoring, all 18 model-strategy com- confidence directly in natural language rather than
 binations have negative Net Calibration Error, reading it off internal token probabilities. The exact
 showing a consistent tendency toward overcon-
 wording used to ask for that judgment is the elicita-
 fidence. Linguistic elicitation achieves the low-
 est Expected Calibration Error for four of six tion strategy, and different strategies can produce
 models, but several favourable values result different confidence values for the same code.
 from collapsed confidence distributions. Eight Figure 1 shows why the problem is not trivial.
 of the 18 combinations are collapsed and five Both programs come from the same model under
 are unstable across repeated runs, including the same elicitation strategy, yet the reported confi-
 three Chain-of-Thought combinations. When dence runs opposite to correctness. The program
 outputs are ranked by confidence and the least
 in (a) is rated 100 percent confident and fails the
 confident are reviewed first, Direct elicitation
 gives the largest improvement over random se- hidden tests, while the program in (b) is rated 0
 lection in four of six models. Verbalized confi- percent confident and passes every one. A score
 dence cannot be reduced to a single trustworthy that behaves like this is worse than no score at all,
 pass probability; calibration, ranking ability, because it turns a developer toward trusting the
 distributional collapse, and stability must each wrong output and re-checking the right one. Both
 be checked separately. cases are worked through in Appendix P.
 Prior work shows that LLMs are often poorly cal-
1 Introduction
 ibrated when asked to verbalize their uncertainty,
Coding large language models (LLMs) are widely with overconfidence observed across NLP and
used and can produce plausible-looking code that vision-language tasks (Xiong et al., 2024; Groot
appears correct at first glance. Generated code can and Valdenegro-Toro, 2024). For code specifically,
still fail on hidden test cases or introduce subtle Spiess et al. (2025) find poor calibration across
bugs through edge cases, so knowing when to trust several code-related tasks, but their evaluation re-
an output matters in practice. In the 2025 Stack lies on static benchmarks whose problems may
Overflow Developer Survey, 84% of respondents already have appeared in training data, which in-
report using or planning to use AI-assisted tools, flates performance and complicates the interpreta-
 328
 The Proceedings of the Third Workshop on Uncertainty-Aware NLP, pages 328–355
 October 29, 2026 ©2026 Association for Computational Linguistics
 (a) Incorrect code, confidence 100 (b) Correct code, confidence 0
LeetCode 3417: zigzag traversal while skipping every other LeetCode 3502: minimum cost to reach every position in a
 visited cell. line.
 for i in range(rows): for i in range(1, n): # redundant loop
 if i % 2 == 0: answer[i] = cost[i]
 for j in range(0, cols, 2): ... for j in range(i): ...
 else: for i in range(n): # correct prefix minima
 for j in range(cols - 1, -1, -2): ... min_cost = min(min_cost, cost[i])
 FINAL_CONFIDENCE: 100 answer[i] = min_cost
 FINAL_CONFIDENCE: 0
Figure 1: Two Qwen2.5-Coder-32B outputs under Direct elicitation. In (a), row-wise skipping breaks the required
global traversal pattern, yet receives confidence 100. In (b), a redundant loop does not affect correctness, yet the
passing program receives confidence 0. Full code and test-level explanations are in Appendix P.
tion of calibration results (Jain et al., 2025). L IVE - we also assess how an additional call to repair in-
C ODE B ENCH addresses this by continuously col- correctly formatted confidence responses affects
lecting newly released competitive programming calibration and ranking.
problems with release dates, so that evaluation can
be restricted to problems that postdate a model’s 2 Related Work
training cutoff (Jain et al., 2025). That restriction is
 Calibration in language models: Calibration
what makes the setting contamination-aware, and
 refers to the alignment between a model’s reported
code generation is the L IVE C ODE B ENCH task with
 confidence and its empirical accuracy across many
enough post-cutoff problems to support the calibra-
 predictions (Geng et al., 2024). Two properties
tion analysis.
 matter in practice and can come apart. Calibration
 In code generation the model receives a prob-
 quality is how closely stated confidence tracks ob-
lem specification and must produce a complete
 served accuracy on average. Ranking ability, also
program, which is then executed against a suite of
 called discriminative ability, is whether the score
hidden test cases, so correctness is a binary pass or
 separates correct predictions from incorrect ones
fail signal rather than a subjective judgment. The
 regardless of whether the values are numerically
following research question guides this paper.
 calibrated. A related property, selective prediction,
 asks whether ordering outputs by confidence lets
 To what extent do verbalized confi- a developer review the least trustworthy ones first,
 dence elicitation strategies produce cal- which can hold even when the absolute values are
 ibrated uncertainty estimates for objec- miscalibrated.
 tively scored code generation correctness
 in a contamination-aware setting, and Verbalized confidence in LLMs: Uncertainty
 how does calibration vary across elici- methods are commonly divided into intrinsic ap-
 tation strategies and models? proaches, which use model internals (e.g., log-
 token probabilities), and verbalized approaches,
 Three elicitation strategies are applied to six which ask for a number or label (Geng et al., 2024;
coding-specialized LLMs spanning three model Xiong et al., 2024). This work studies verbalized
families and two parameter scales each, with cal- confidence because many deployed APIs expose
ibration quality, direction of miscalibration, rank- only text and because token likelihood need not rep-
ing ability, and stability each assessed separately. resent whole-program correctness. Recent intrinsic
Multiple models and strategies are compared be- studies show that code uncertainty depends highly
cause both the model and the elicitation wording on structure; perplexity, how surprised an LLM
can change the result, so a single pairing would is by a sequence of text, varies by programming
not reveal whether an observed pattern generalizes. language and model in code completion (Kotti
Our contribution is a contamination-aware compar- et al., 2026), while syntax-aware aggregation im-
ison of established verbalized-confidence methods, proves uncertainty estimation for function calling
using the same generated code and correctness la- (Ye et al., 2026). More broadly, a single scalar
bels across strategies within each model. Further, may conflate input ambiguity, knowledge gaps,
 329
and decoding randomness (Taparia et al., 2026). 3.1 Benchmark and problem selection
Groot and Valdenegro-Toro (2024) find high cali-
 L IVE C ODE B ENCH is a continuously updated
bration error and predominantly overconfident ver-
 benchmark of competitive-programming problems
balized scores across several NLP tasks, while
 collected from public contest platforms, with each
Xiong et al. (2024) show that values often clus-
 problem tagged by its release date (Jain et al.,
ter in the 80-100% range and on round multiples
 2025). Problems come in two input formats, that is
of five. Larger models can be well calibrated in
 function-completion starter code with a fixed signa-
structured multiple-choice and true/false settings
 ture, and standard input and output. Each problem
(Kadavath et al., 2022), but Chain-of-Thought ef-
 has public example tests and a larger hidden test
fects remain inconsistent across tasks and models
 suite, and grading uses the hidden suite so a solu-
(Xiong et al., 2024).
 tion cannot be tuned to the visible cases.
Calibration for code generation: Code is a use- Under strict scoring a solution counts as cor-
ful calibration setting because hidden tests provide rect only when it produces the expected output
an objective binary correctness signal (Spiess et al., on every hidden test, following the execution-
2025). Spiess et al. (2025) evaluate intrinsic and based functional-correctness protocol of Chen et al.
reflective confidence across completion, synthesis, (2021). This all-or-nothing rule makes correct-
and repair, finding poor out-of-the-box calibration; ness a binary label and is the primary scoring used
however, their static benchmarks, including Hu- throughout. Lenient scoring is a secondary diag-
manEval and MBPP, may have appeared in training nostic that additionally counts a solution as correct
(Chen et al., 2021; Austin et al., 2021; Jain et al., when the expected output is a single number and
2025). Recent work has expanded uncertainty es- the generated value falls within a 10% relative tol-
timation for code generation through uncertainty- erance, with a full tolerance sweep in Appendix F.
guided Chain-of-Thought prompting (Zhu et al., All experiments use L IVE C ODE B ENCH re-
2025), risk-controlling prediction sets (Xu et al., lease_v6 (Jain et al., 2025), from the Hugging Face
2026), and multicalibration of likelihood-based dataset livecodebench/code_generation_lite
confidence (Campos et al., 2026). These meth- at revision 0fe84c3, scored with the harness at
ods primarily focus on generation-time uncertainty commit 6729765. Restricting evaluation to prob-
or post-hoc calibration using intrinsic model sig- lems released only after a model’s training cutoff
nals. In contrast, no existing work compares black- is central to the design, and to keep the comparison
box verbalized elicitation strategies across multiple identical, all six models are evaluated on the same
coding-specialized LLMs on a shared temporally window from 2024-09-19 to 2025-04-30 inclusive.
filtered window. This paper addresses that gap by The window starts there because Qwen2.5-Coder
combining the verbalized-confidence framework of is the newest family used and does not publish a
Xiong et al. (2024) with the code-calibration fram- formal training-data cutoff, so the first public arXiv
ing of Spiess et al. (2025) and the contamination- submission date of its technical report, 2024-09-18,
aware design of L IVE C ODE B ENCH (Jain et al., is used as a transparent proxy boundary (Hui et al.,
2025). 2024). This does not prove that every earlier prob-
 lem was in training nor that every later one could
3 Methods not have been seen, but it provides a reproducible
The evaluation pipeline proceeds in five stages. boundary, mirroring the temporal split that defines
Eligible problems are selected from L IVE - L IVE C ODE B ENCH itself (Jain et al., 2025). The
C ODE B ENCH using a shared post-cutoff window. heuristic is supported by Li and Flanigan (2024),
Each model generates one solution per problem; who show that models perform better on tasks re-
these outputs are frozen. Frozen outputs are scored leased before their training cutoff than on tasks
for correctness against hidden test cases. Confi- released after. Within this window the code genera-
dence is elicited in a separate inference pass under tion task yields exactly 365 eligible problems.
three prompting strategies. Finally, the resulting
 3.2 Models
confidence scores and correctness labels are paired
to compute calibration metrics. Figure 4 in Ap- Six instruction-tuned, coding-specialized LLMs
pendix A summarizes the flow, and the subsections are evaluated, drawn from three families at two pa-
below describe each stage in the order it is run. rameter scales each, Qwen2.5-Coder (Hui et al.,
 330
2024), CodeLlama (Rozière et al., 2023), and the same final confidence line, applying chain-of-
DeepSeek-Coder (Guo et al., 2024). Evaluating thought prompting (Wei et al., 2022) to the con-
two scales within each family allows calibration fidence judgment. Linguistic elicitation asks for
to be examined as a function of capacity while one of five ordered labels, very low to very high,
holding the family fixed, a comparison of interest mapped to 10, 30, 50, 70, 90, testing whether a
because larger models have been reported to be coarser categorical signal mitigates the tendency of
better calibrated in suitably formatted settings (Ka- numeric confidence to cluster at round high values
davath et al., 2022), and the three families together (Xiong et al., 2024; Groot and Valdenegro-Toro,
provide diversity in pretraining corpora and instruc- 2024). Each strategy is a single fixed prompt, re-
tion tuning. All models are loaded without quanti- produced in full in Appendix B, so a finding such
zation in each checkpoint’s native BF16 precision, as “CoT underperforms Direct” is a finding about
and each model’s bundled tokenizer chat template that particular prompt.
is applied to all prompts. Identifiers, parameter A line-based parser handles all three strategies.
counts, and cutoff evidence are listed in Appendix If the primary parse fails, a single repair call
Table 3. The DeepSeek-Coder dates come from presents the original prompt alongside the mal-
a maintainer response on the official repository formed response and requests only the correctly
(DeepSeek-AI, 2023), the CodeLlama dates from formatted output, and if repair also fails the con-
the Hugging Face model cards (Meta AI, 2023b,a), fidence defaults to 50, which retains every prob-
and Qwen2.5-Coder has no formally disclosed cor- lem. A repair call may elicit a new judgment rather
pus cutoff, so its rows are marked before September than only changing formatting, therefore we com-
2024 (Hui et al., 2024). All inference is run on the pare the complete pipeline with immediate fallback
Hábrók cluster at the University of Groningen with to a confidence of 50 on the same problems (Ap-
all random seeds fixed, and library versions are pendix N). Across the full primary pipeline, 5,441
listed in Appendix A. outputs parse cleanly, 1,123 are repaired, and 6
 default to 50. Per-cell rates are in Appendix C.2.
3.3 Code generation and confidence elicitation
Code generation is performed once per model and 3.4 Stability analysis
the outputs are frozen before any confidence elici- A confidence score is only useful if it is consistent
tation, so the model cannot adjust its code for the across repeated elicitation on the same code. For
confidence prompt and correctness labels are deter- each (problem, generated code) pair, five indepen-
mined independently of any confidence estimation. dent confidence elicitations are run with tempera-
All primary generations use greedy decoding, so ev- ture 0.3 and sampling enabled, using seeds 42 + i
ery result is deterministic and exactly reproducible for i ∈ {0, . . . , 4}. If a run falls back to the de-
for a fixed model and prompt. Each model gen- fault confidence of 50, that value is kept so the
erates a single solution per problem, the pass@1 reported variability covers the full pipeline. The
setting of Chen et al. (2021), matching the deploy- sample standard deviation across the five values is
ment case in which a developer receives one com- computed for each pair, and pairs are classified on
mitted output and must decide whether to trust it. the 0–100 scale as stable (below 5), marginal (be-
Full generation parameters are in Appendix A. tween 5 and 10), or unstable (10 or above). These
 Confidence is then elicited in a separate infer- thresholds are heuristic and descriptive and are not
ence pass, following Lin et al. (2022) and Xiong deployment-safety boundaries. Aggregate statistics
et al. (2024), with the same model that generated per cell are in Appendix J.
the code assessing its own output, a self-evaluation
setup following Kadavath et al. (2022). The confi- 3.5 Calibration metrics
dence prompt contains the full problem statement Four properties are evaluated after normalizing con-
and the extracted code. Three methods are com- fidence to [0, 1]. Expected Calibration Error (ECE)
pared. Direct elicitation asks for the probability measures the count-weighted absolute gap between
that the code passes all hidden tests, without expla- confidence and empirical accuracy over ten equal-
nation, as an integer between 0 and 100. Chain- width bins; lower is better (Naeini et al., 2015;
of-Thought (CoT) elicitation first asks the model Guo et al., 2017). Net Calibration Error (NCE)
to analyze whether the code handles edge cases is the signed mean difference between correctness
and whether the algorithm is sound, then to output and confidence, so negative values indicate over-
 331
confidence and positive values underconfidence Table 1: Strict calibration metrics for all 18 model-strategy
 cells. ECE: lower is better; AUROC: higher is better; negative
(Groot and Valdenegro-Toro, 2024). Area Under NCE indicates overconfidence. Confidence intervals are in
the ROC Curve (AUROC) measures whether confi- Appendix D.
dence ranks correct solutions above incorrect ones Model Strategy ECE AUROC NCE
independently of numerical calibration, with 0.5 Qwen-32B Direct 0.327 0.834 -0.294
indicating random discrimination (Fawcett, 2006; Qwen-32B CoT 0.330 0.810 -0.324
Hendrycks and Gimpel, 2017). Qwen-32B Linguistic 0.216 0.841 -0.216
 Selective prediction retains the programs with Qwen-7B Direct 0.624 0.766 -0.619
 Qwen-7B CoT 0.506 0.772 -0.495
the highest confidence scores. The fraction retained Qwen-7B Linguistic 0.507 0.709 -0.505
is called coverage; measuring accuracy as this DS-33B Direct 0.183 0.760 -0.057
fraction varies gives an accuracy-coverage curve. DS-33B CoT 0.553 0.675 -0.536
Its area is AUACC (Geifman and El-Yaniv, 2017; DS-33B Linguistic 0.258 0.638 -0.197
Kamath et al., 2020). The AUACC gaps in Ap- DS-6.7B Direct 0.849 0.518 -0.849
pendix M subtract overall pass@1 accuracy from DS-6.7B CoT 0.779 0.716 -0.779
 DS-6.7B Linguistic 0.713 0.498 -0.713
this area. For comparisons across models with
 CL-34B Direct 0.813 0.655 -0.813
different accuracies, we additionally report the pre- CL-34B CoT 0.814 0.620 -0.814
diction rejection ratio (PRR). PRR measures the CL-34B Linguistic 0.660 0.681 -0.660
improvement in AUACC over random ordering as CL-7B Direct 0.862 0.639 -0.862
a fraction of the improvement possible under an CL-7B CoT 0.680 0.556 -0.663
ideal ordering that places every correct solution CL-7B Linguistic 0.013 0.491 -0.012
before every incorrect one (Vashurin et al., 2025).
PRR is zero for random ordering and one for ideal 4.2 Calibration metrics
ordering. Separately, when programs receive the
 ECE, AUROC, and NCE for all eighteen cells (3
same confidence score, we average over their pos-
 families × 2 sizes × 3 strategies) are listed in
sible orderings when calculating PRR, so that the
 Table 1. Reliability diagrams for all cells are in
result does not depend on their order in the saved
 Appendix K, and full bootstrap intervals in Ap-
data. The calculation of PRR and the effect of tie
 pendix D.
handling can be found in Appendix O. ECE, AU-
 All eighteen strict-scoring NCE point estimates
ROC, and NCE use 1,000 bootstrap resamples for
 are negative, and seventeen of the corresponding
95% percentile confidence intervals. Reliability
 95% bootstrap intervals remain below zero. The
diagrams and 20-bin histograms diagnose patterns
 exception is CodeLlama-7B with Linguistic elic-
hidden by scalar metrics; a cell is labelled collapsed
 itation, where the NCE is −0.012 with a 95% CI
when one histogram bin contains at least 50% of
 of [−0.04, 0.02] that includes zero. The magni-
its scores. Platt scaling is used only as a post-hoc
 tude of the NCE differs sharply across cells, from
diagnostic. Equations and full procedural details
 −0.012 for CodeLlama-7B Linguistic to −0.862
are in Appendix A.1, with recalibration results in
 for CodeLlama-7B Direct with a 95% CI of [−0.89,
Appendix E.
 −0.83]. Individual confidence outputs can diverge
 sharply from correctness in both directions, as il-
4 Results lustrated in Figure 1.
 ECE and AUROC measure different properties
4.1 Accuracy and do not correlate across cells. The lowest ECE
 in the table is 0.013 for CodeLlama-7B Linguistic,
Because code outputs are frozen before confidence whose AUROC is 0.491, while the highest AU-
elicitation, pass@1 accuracy is identical across ROC is 0.841 for Qwen2.5-Coder-32B Linguis-
strategies. Strict accuracy ranges from 8.22% for tic, whose ECE is 0.216. Qwen2.5-Coder-32B
CodeLlama-34B to 29.86% for Qwen2.5-Coder- is the only model with AUROC above 0.80 for
32B; CodeLlama is the only family with an in- all three strategies. The bootstrap intervals sepa-
version, as its 7B model reaches 9.86%. Lenient rate some strategy comparisons but not others. For
scoring adds only 0.55-3.56 percentage points. The Qwen2.5-Coder-32B, Linguistic (ECE 0.216, [0.18,
complete accuracy table and tolerance sweep are 0.25]) lies clearly below both Direct (0.327, [0.28,
in Appendix F. 0.37]) and CoT (0.330, [0.29, 0.37]), whereas for
 332
 1.0 Family Strategy
 Table 2: Tie-averaged PRR for the saved repair pipeline. Zero
 Qwen Direct represents random ordering; one represents ideal ordering,
 DeepSeek CoT
 CodeLlama Linguistic with every correct solution before every incorrect one.
 0.8 Model Direct CoT Ling.
 Qwen-32B 0.633 0.525 0.705
 Qwen-7B 0.428 0.413 0.257
Strict pass@1 accuracy
 0.6 DS-33B 0.474 0.239 0.291
 DS-6.7B 0.016 0.257 -0.003
 CL-34B 0.310 0.160 0.167
 CL-7B 0.178 0.096 -0.029
 0.4
 Q32-C
 Q32-L
 Q32-D
 DS33-L Q7-L DS33-C 4.4 Repair sensitivity and selective prediction
 0.2 Q7-C Q7-D DS7-C
 DS33-D
 DS7-L DS7-D
 CL7-C
 CL7-L
 CL34-L CL34-C
 CL7-D We compare the saved repair pipeline with an al-
 0.0
 CL34-D
 ternative that skips repair and assigns a confidence
 0.0 0.2 0.4 0.6 0.8 1.0
 Mean confidence of 50 whenever the first response is unable to be
Figure 2: Mean elicited confidence versus strict pass@1 accu- successfully parsed. Both policies retain all the 365
racy for all 18 model-strategy cells. Points below the dashed problems for each model-strategy combination. For
diagonal are overconfident. Color encodes model family;
marker labels identify each combination. CodeLlama-7B CoT, ECE falls from 0.680 down to
 0.445, while AUROC changes from 0.556 to 0.546;
 for DeepSeek-33B Direct, ECE rises from 0.183 up
Qwen2.5-Coder-7B the CoT and Linguistic esti- to 0.330. Following this, a lower calibration error
mates of 0.506 and 0.507 have overlapping inter- under fallback confidence values does not mean
vals and are not meaningfully separated. better ranking. Eight combinations are unchanged
 Figure 2 plots mean elicited confidence against because none of their responses required repair.
strict pass@1 accuracy for all 18 cells. Almost all The full results, along with confidence intervals,
points sit where mean confidence exceeds accuracy. for the differences can be found in Appendix N. Im-
The three Qwen2.5-Coder-32B cells occupy the portantly, any malformed original responses were
highest accuracy positions at approximately 0.30 overwritten with repair, this comparison is unable
and show lower mean confidence than the remain- to establish if repair preserves the original judg-
ing cells, while several CodeLlama and DeepSeek- ment from the first response.
Coder-6.7B cells report mean confidence above
0.80 despite strict accuracy below 0.15. The relia-
bility diagrams in Appendix K show the same split. 4.5 Within-family scaling
Qwen2.5-Coder-32B spreads across the confidence
range and sits mostly below the diagonal, whereas Mean ECE and AUROC averaged across the
CodeLlama-7B Linguistic concentrates nearly all three strategies are visualized and tabulated in Ap-
predictions at one value, so its diagram reduces pendix H. For Qwen2.5-Coder, the 32B variant
to isolated points and its near-zero ECE reflects improves strict accuracy from 16.44% to 29.86%,
a constant confidence that happens to sit near the reduces mean ECE from 0.546 to 0.291, and in-
model’s empirical accuracy. creases mean AUROC from 0.749 to 0.828 relative
 to the 7B variant. For DeepSeek-Coder, the 33B
 model improves the three quantities from 14.25%
4.3 Strategy comparison to 18.90%, from 0.780 to 0.331, and from 0.577 to
 0.691 relative to the 6.7B model. CodeLlama does
Linguistic elicitation has the lowest point-estimate not follow this pattern. Its accuracy inverts, with
ECE in four of six models, namely Qwen2.5-Coder- CodeLlama-34B at 8.22% below CodeLlama-7B
32B, DeepSeek-Coder-6.7B, CodeLlama-34B, and at 9.86%. Mean ECE is 0.518 for CodeLlama-7B
CodeLlama-7B. Three of these four lowest-ECE and 0.762 for CodeLlama-34B, but excluding the
Linguistic cells are collapsed distributions, includ- degenerate CodeLlama-7B Linguistic cell raises
ing CodeLlama-7B Linguistic (Section 4.6), so the the CodeLlama-7B mean ECE to 0.771. Mean AU-
low ECE there does not by itself indicate a useful ROC is 0.652 for CodeLlama-34B and 0.562 for
confidence signal. CodeLlama-7B.
 333
4.6 Degenerate confidence distributions gaps reported above retain the saved-file order of
 programs with equal confidence scores; the PRR
A collapsed, or degenerate, confidence distribution
 results average over possible orderings within each
is one in which the model outputs the same value
 tied group. Table 2 shows that Direct achieves the
for almost all problems, so the scores barely vary re-
 highest PRR for four of the six models. Linguistic
gardless of whether the underlying code is correct.
 performs best for Qwen2.5-Coder-32B, and CoT
A cell is flagged as collapsed when a single inter-
 performs best for DeepSeek-Coder-6.7B. PRR is
val of the 20-bin confidence histogram contains
 negative only for DeepSeek-Coder-6.7B Linguistic
at least 50% of all predictions. Eight of the eigh-
 (−0.003) and CodeLlama-7B Linguistic (−0.029).
teen cells meet this criterion, with histograms and
 The four below-baseline results reported above thus
per-cell statistics in Appendix I. CodeLlama-7B
 apply to the original AUACC calculation. They do
Linguistic places 359 of 365 predictions (98.4%)
 not all remain below baseline after averaging over
at confidence 10, producing an ECE of 0.013 and
 tied orderings, a distinction examined separately in
an AUROC of 0.491.
 Appendix O.
4.7 Stability
Five of the eighteen cells are unstable, with a mean 5 Discussion
sample standard deviation of at least 10 on the 0–
 Verbalized confidence is not reliably calibrated for
100 scale across five temperature-0.3 runs. Three
 contamination-aware code generation. The vari-
are CoT cells, namely Qwen2.5-Coder-7B (19.59),
 ation across strategies and models is where the
DeepSeek-Coder-33B (20.29), and CodeLlama-7B
 picture becomes more complicated, and eight of
(17.32); the other two are DeepSeek-Coder-33B
 the eighteen cells have collapsed confidence distri-
Linguistic (13.81) and CodeLlama-34B Linguistic
 butions, so the scalar metrics cannot be read alone.
(12.01). Every CoT cell has a higher mean standard
deviation than the corresponding Direct cell for the
same model, and in four of the six models CoT is 5.1 Systematic overconfidence
the single most unstable strategy. The complete Every one of the eighteen strict-scoring NCE point
analysis is in Appendix J. estimates is negative, and seventeen of the corre-
 sponding intervals remain below zero, a systematic
4.8 Selective prediction
 pattern of overconfidence. This extends the over-
A positive gap means that ordering outputs by con- confidence trend documented for general NLP and
fidence and reviewing the least confident first con- vision-language tasks (Xiong et al., 2024; Groot
centrates the failures better than a random ordering. and Valdenegro-Toro, 2024) and for verbalized
Qwen2.5-Coder-32B has the largest gaps, with Lin- confidence under distribution shift (Borszukovszki
guistic at +0.264, Direct at +0.236, and CoT at et al., 2025) into contamination-aware code genera-
+0.195, and Qwen2.5-Coder-7B and DeepSeek- tion, and it agrees with the finding that code models
Coder-33B are also positive for all three strate- are poorly calibrated out of the box (Spiess et al.,
gies. These gaps occur even though the same 2025). Restricting the window using documented
cells are overconfident in absolute terms, so a us- cutoffs where available, and a transparent release-
able review ordering is present despite the mis- date proxy for Qwen2.5-Coder, reduces the risk
calibration. Direct gives the highest gap in four that memorized benchmark problems inflate the
of six models. Four cells fall below the random observed accuracy. That cannot rule out contami-
baseline, DeepSeek-Coder-6.7B Direct, DeepSeek- nation completely, but it shows the pattern persists
Coder-6.7B Linguistic, CodeLlama-34B Linguis- under a temporally filtered evaluation setting (Jain
tic, and CodeLlama-7B Linguistic, all of which et al., 2025; Li and Flanigan, 2024). The magnitude
coincide with collapsed distributions. Direct pro- is far from uniform, and the two smallest values are
duces one below-baseline gap, while Linguistic misleading. The near-zero NCE of CodeLlama-7B
produces three. Linguistic reflects a collapsed distribution rather
 We also report PRR to compare models with than a useful signal, and DeepSeek-Coder-33B Di-
different accuracies. PRR expresses the gain in rect is a different special case where a small NCE
AUACC over random ordering as a fraction of the reflects a bimodal distribution rather than good cal-
gain possible under ideal ordering. The AUACC ibration.
 334
5.2 Calibration versus discrimination Since the algorithm logic is incorrect, the
 confidence score should reflect
ECE and AUROC do not co-vary across cells, and
 that the code does not meet the problem’s
this separation is central to interpreting the results.
 requirements.
The lowest ECE (0.013, CodeLlama-7B Linguis-
tic) sits at an AUROC of 0.491, which is random FINAL_CONFIDENCE: 0
discrimination, while the highest AUROC (0.841,
 Figure 3: Closing lines of the Qwen2.5-Coder-32B Chain-of-
Qwen2.5-Coder-32B Linguistic) sits at an ECE Thought reasoning trace on a solution that passes all hidden
of 0.216. A confidence score can rank correct tests. The trace concludes that the logic is incorrect and out-
solutions above incorrect ones while remaining puts confidence 0. The full example is in Appendix P.
numerically overconfident, and a low ECE can
 before stating a score does not consistently improve
carry no ranking signal at all, which is why the
 the confidence signal and adds variability relative
two properties were measured separately (Geng
 to Direct. One example makes the failure con-
et al., 2024; Fawcett, 2006; Hendrycks and Gimpel,
 crete. Qwen2.5-Coder-32B under CoT correctly
2017). The practical consequence is visible in the
 transcribed the required condition, then claimed the
AUACC gaps. Qwen2.5-Coder-7B and DeepSeek-
 submitted code checked a different condition and
Coder-33B show positive AUACC gaps for all three
 concluded it was wrong, giving a final confidence
strategies despite being overconfident in absolute
 of 0. The two conditions were logically identi-
terms, so a developer who reviews the least confi-
 cal and the code passed all hidden tests. Figure 3
dent outputs first will catch more failures earlier
 shows the closing lines. CoT can improve task
than a random sweep would. Confidence can re-
 accuracy (Wei et al., 2022), but here it does not re-
main useful for prioritizing manual review even
 liably improve the confidence judgment, consistent
when miscalibrated, the same observation that mo-
 with prior reports that reasoning-style prompting
tivates selective prediction under distribution shift
 has inconsistent effects on calibration (Xiong et al.,
(Kamath et al., 2020; Geifman and El-Yaniv, 2017).
 2024).
The PRR results also support this finding when av-
eraging over possible program orderings with equal 5.4 Stability, scaling, and metric limits
confidence.
 Stability matters for deployment in a way the cali-
 bration metrics alone do not capture. A confidence
5.3 Behaviour of the elicitation strategies
 value that varies widely on repeated elicitation of
The ranking of the three strategies varies across the same code cannot be trusted as a fixed prop-
metrics, so the best choice depends on how confi- erty of that code, because the number a developer
dence scores will be used. Linguistic has the lowest sees depends on the run rather than on the program.
ECE in four of the six models, with scores closer to CoT is the least stable strategy across the full proce-
the empirical pass rate on average. Direct has the dure, including repair calls. The saved data cannot
largest AUACC gap in four models and the highest separate variability in the initial responses from
PRR in four after averaging over possible order- variability introduced by repair.
ings of tied scores. The number of below-baseline The larger Qwen2.5-Coder and DeepSeek-Coder
results also depends on how ties are handled. Keep- variants improve on all three metrics, consistent
ing tied programs in their saved-file order gives with findings that larger models can be better cal-
one negative AUACC gap for Direct and three for ibrated in suitably formatted settings (Kadavath
Linguistic. Averaging over tied orderings leaves et al., 2022). CodeLlama does not follow this pat-
Direct with no negative PRR values and Linguistic tern, and its apparent ECE improvement at 7B is an
with two. These findings favour Direct for several artifact of the degenerate CodeLlama-7B Linguistic
tested models, but they do not establish that it is cell, since removing that cell leaves the two scales
consistently more reliable for reviewing programs essentially tied. These comparisons are descriptive
in confidence order. rather than causal, because the variants may differ
 CoT does not consistently improve calibration, in pretraining data and instruction tuning, not just
although it achieves the highest PRR for DeepSeek- parameter count.
Coder-6.7B. It is the least stable strategy overall, The degenerate cells expose a limit in the met-
with three of the five unstable cells being CoT cells. rics. A low ECE can result from distribution col-
Prompting the model to reason about code quality lapse rather than from alignment between confi-
 335
dence and accuracy, so it must be read alongside not establish behaviour under repeated sampling,
the histogram and AUROC. CodeLlama-7B Lin- reranking, iterative refinement, or developer use.
guistic is the clearest example, its near-zero ECE of Future work should cover more programming lan-
0.013 arising because a nearly constant confidence guages and prompt variants, and examine how con-
value happens to sit close to the model’s empiri- fidence differs across error categories. Newer or
cal accuracy, while its AUROC of 0.491 shows the closed models could also be included where the
score carries almost no information about which available cutoff evidence allows. Comparing intrin-
outputs are correct (Naeini et al., 2015; Guo et al., sic and verbalized measures over the same evalu-
2017). DeepSeek-Coder-33B Direct is a different ation window would help assess their differences.
degeneracy, where a bimodal distribution lets over- Testing confidence ordering in real code review
confidence in the high bin and underconfidence in would show whether it improves the review pro-
the low bin partially cancel, explaining an NCE cess.
of only −0.057 despite an ECE of 0.183, while
the cell keeps useful ranking ability. No single 6 Conclusion
number is enough. NCE shows the direction of Verbalized confidence is not reliably calibrated in
miscalibration, ECE its average magnitude, AU- this setting, since all eighteen strict-scoring NCE
ROC whether the scores rank correct outputs above point estimates indicate overconfidence and sev-
incorrect ones, and the histogram whether the dis- enteen of the eighteen bootstrap intervals remain
tribution has collapsed. below zero. Calibration also depends strongly on
 the model, the elicitation strategy, and the met-
Limitations ric. Calibration quality and ranking ability do not
 co-vary, so a low ECE can coincide with random
The evaluation is contamination-aware rather than discrimination and a strong ranking signal can co-
contamination-free. Qwen2.5-Coder has no dis- incide with substantial overconfidence. Among
closed corpus cutoff, so its technical-report date strategies, Linguistic minimizes ECE most often,
is used as a reproducible proxy, and competitive- Direct gives the highest AUACC gap and the high-
programming problems do not capture the full com- est PRR in four of six models, and CoT is the
plexity of production software. Only six open- least stable overall. Among models, the larger vari-
weight coding models are evaluated, since closed ants show better accuracy, calibration, and rank-
assistants do not expose stable versions and cut- ing within Qwen2.5-Coder and DeepSeek-Coder,
off evidence needed for the shared temporal win- while CodeLlama does not follow this pattern. The
dow. Correctness also depends on the hidden test repair comparison also shows that lower calibration
suite, which may miss semantically wrong pro- error does not necessarily imply better ranking.
grams, while lenient scoring is meaningful only for The overall takeaway is that verbalized confi-
single-number outputs. dence in coding LLMs should be treated as a multi-
 The strategy comparison covers one fixed dimensional signal rather than a single calibration
prompt and, for Linguistic, one fixed label map- score. It can still support selective review in some
ping. The collapse and stability thresholds describe model-strategy combinations, but it should not be
the observed distributions and variation across runs. interpreted as a trustworthy pass probability unless
They have not been validated as cutoffs for reliable calibration, ranking ability, distributional collapse,
confidence. Because any malformed original re- and stability have all been checked.
sponses were not saved, we cannot compare them
directly with their repaired versions. Comparing re- Data Availability
pair with an immediate default of 50 measures the
 Retained confidence responses, confidence scores,
effect of using repair, but does not show whether
 correctness labels, and repair-status records are pro-
it preserves the original confidence judgment that
 vided in the accompanying Zenodo dataset (Tuer-
a model gave. The stability measurements cover
 lings and Valdenegro-Toro, 2026).
the full procedure, including any repair calls. In-
sample Platt scaling is an optimistic bound rather
than deployable performance, although five-fold
results remain close for most cells (Appendix E).
The findings concern frozen pass@1 outputs and do
 336
References ference on Machine Learning, volume 70 of Pro-
 ceedings of Machine Learning Research, pages 1321–
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten 1330. PMLR.
 Bosma, Henryk Michalewski, David Dohan, Ellen
 Jiang, Carrie Cai, Michael Terry, Quoc Le, and Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai
 Charles Sutton. 2021. Program synthesis with large Dong, Wentao Zhang, Guanting Chen, Xiao Bi,
 language models. CoRR, abs/2108.07732. Y. Wu, Y. K. Li, Fuli Luo, Yingfei Xiong, and Wen-
 feng Liang. 2024. DeepSeek-Coder: When the large
Mirko Borszukovszki, Ivo Pascal De Jong, and Ma- language model meets programming – the rise of
 tias Valdenegro-Toro. 2025. Know what you do not code intelligence. CoRR, abs/2401.14196.
 know: Verbalized uncertainty estimation robustness
 on corrupted images in vision-language models. In Dan Hendrycks and Kevin Gimpel. 2017. A baseline
 Proceedings of the 5th Workshop on Trustworthy NLP for detecting misclassified and out-of-distribution ex-
 (TrustNLP 2025), pages 247–265, Albuquerque, New amples in neural networks. In The Fifth International
 Mexico. Association for Computational Linguistics. Conference on Learning Representations (ICLR).
Viola Campos, Robin Kuschnereit, and Adrian Ulges. Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Day-
 2026. Multicalibration for llm-based code generation. iheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang,
 In Proceedings of the 1st International Workshop on Bowen Yu, Keming Lu, Kai Dang, Yang Fan,
 AI for Software Quality Evaluation - Judgment, Met- Yichang Zhang, An Yang, Rui Men, Fei Huang,
 rics, Benchmarks, and Beyond, AI-SQE ’26, page Bo Zheng, Yibo Miao, Shanghaoran Quan, and 5 oth-
 61–71, New York, NY, USA. Association for Com- ers. 2024. Qwen2.5-Coder technical report. CoRR,
 puting Machinery. abs/2409.12186.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia
 Henrique Ponde de Oliveira Pinto, Jared Kaplan, Yan, Tianjun Zhang, Sida Wang, Armando Solar-
 Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Lezama, Koushik Sen, and Ion Stoica. 2025. Live-
 Brockman, Alex Ray, Raul Puri, Gretchen Krueger, CodeBench: Holistic and contamination free evalua-
 Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela tion of large language models for code. In The Thir-
 Mishkin, Brooke Chan, Scott Gray, and 39 others. teenth International Conference on Learning Repre-
 2021. Evaluating large language models trained on sentations (ICLR).
 code. CoRR, abs/2107.03374.
 Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
DeepSeek-AI. 2023. Cutoff dates. GitHub issue #89 Henighan, Dawn Drain, Ethan Perez, Nicholas
 in the DeepSeek-Coder repository. GitHub issue Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli
 opened 30 December 2023. Accessed 5 May 2026. Tran-Johnson, Scott Johnston, Sheer El-Showk,
 Andy Jones, Nelson Elhage, Tristan Hume, Anna
Tom Fawcett. 2006. An introduction to ROC analysis. Chen, Yuntao Bai, Sam Bowman, Stanislav Fort, and
 Pattern Recognition Letters, 27(8):861–874. 17 others. 2022. Language models (mostly) know
 what they know. CoRR, abs/2207.05221.
Yonatan Geifman and Ran El-Yaniv. 2017. Selec-
 tive classification for deep neural networks. In Ad- Amita Kamath, Robin Jia, and Percy Liang. 2020. Se-
 vances in Neural Information Processing Systems 30 lective question answering under domain shift. In
 (NeurIPS 2017), pages 4878–4887. Proceedings of the 58th Annual Meeting of the Asso-
 ciation for Computational Linguistics (ACL), pages
Jiahui Geng, Fengyu Cai, Yuxia Wang, Heinz Koeppl, 5684–5696. Association for Computational Linguis-
 Preslav Nakov, and Iryna Gurevych. 2024. A sur- tics.
 vey of confidence estimation and calibration in large
 language models. In Proceedings of the 2024 Con- Zoe Kotti, Konstantina Dritsa, Diomidis Spinellis, and
 ference of the North American Chapter of the Asso- Panos Louridas. 2026. The fools are certain; the
 ciation for Computational Linguistics: Human Lan- wise are doubtful: Exploring llm confidence in code
 guage Technologies (Volume 1: Long Papers), pages completion. Preprint, arXiv:2508.16131.
 6577–6595, Mexico City, Mexico. Association for
 Computational Linguistics. Changmao Li and Jeffrey Flanigan. 2024. Task con-
 tamination: Language models may not be few-shot
Tobias Groot and Matias Valdenegro-Toro. 2024. Over- anymore. In Proceedings of the AAAI Conference
 confidence is key: Verbalized uncertainty evaluation on Artificial Intelligence, volume 38, pages 18471–
 in large language and vision-language models. In 18480.
 Proceedings of the 4th Workshop on Trustworthy Nat-
 ural Language Processing (TrustNLP 2024), pages Stephanie Lin, Jacob Hilton, and Owain Evans. 2022.
 145–171, Mexico City, Mexico. Association for Com- Teaching models to express their uncertainty in
 putational Linguistics. words. Transactions on Machine Learning Research.
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Wein- Meta AI. 2023a. CodeLlama-34b-Instruct-hf model
 berger. 2017. On calibration of modern neural net- card. Hugging Face model hub. Accessed 5 May
 works. In Proceedings of the 34th International Con- 2026.
 337
Meta AI. 2023b. CodeLlama-7b-Instruct-hf model card. Zihuiwen Ye, Lukas Aichberger, Michael Kirchhof,
 Hugging Face model hub. Accessed 5 May 2026. Sinead Williamson, Luca Zappella, Yarin Gal, Arno
 Blaas, and Adam Golinski. 2026. Uncertainty
Mahdi Pakdaman Naeini, Gregory F. Cooper, and Milos quantification for llm function-calling. Preprint,
 Hauskrecht. 2015. Obtaining well calibrated prob- arXiv:2604.22985.
 abilities using bayesian binning. In Proceedings of
 the Twenty-Ninth AAAI Conference on Artificial In- Yuqi Zhu, Ge Li, Xue Jiang, Jia Li, Hong Mei, Zhi Jin,
 telligence, pages 2901–2907. and Yihong Dong. 2025. Uncertainty-guided chain-
 of-thought for code generation with llms. Preprint,
Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten arXiv:2503.15341.
 Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,
 Jingyu Liu, Romain Sauvestre, Tal Remez, J’er’emy
 Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna
 Bitton, Manish Bhatt, Cristian Canton Ferrer, Aaron
 Grattafiori, Wenhan Xiong, Alexandre D’efossez,
 and 7 others. 2023. Code Llama: Open foundation
 models for code. CoRR, abs/2308.12950.
Claudio Spiess, David Gros, Kunal Suresh Pai, Michael
 Pradel, Md Rafiqul Islam Rabin, Amin Alipour, Sus-
 mit Jha, Prem Devanbu, and Toufique Ahmed. 2025.
 Calibration and correctness of language models for
 code. In 2025 IEEE/ACM 47th International Con-
 ference on Software Engineering (ICSE), pages 540–
 552. IEEE Press.
Stack Overflow. 2025. Ai | 2025 stack overflow devel-
 oper survey. Accessed 5 May 2026.
Aditya Taparia, Ransalu Senanayake, Kowshik Thopalli,
 and Vivek Narayanaswamy. 2026. The anatomy of
 uncertainty in llms. Preprint, arXiv:2603.24967.
Hunter Tuerlings and Matias Valdenegro-Toro.
 2026. Verbalized uncertainty in coding llms: A
 contamination-aware confidence calibration dataset.
Roman Vashurin, Ekaterina Fadeeva, Artem Vazhentsev,
 Lyudmila Rvanova, Daniil Vasilev, Akim Tsvigun,
 Sergey Petrakov, Rui Xing, Abdelrahman Sadallah,
 Kirill Grishchenkov, Alexander Panchenko, Timothy
 Baldwin, Preslav Nakov, Maxim Panov, and Artem
 Shelmanov. 2025. Benchmarking uncertainty quan-
 tification methods for large language models with
 lm-polygraph. Transactions of the Association for
 Computational Linguistics, 13:220–248.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
 Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le,
 and Denny Zhou. 2022. Chain-of-thought prompting
 elicits reasoning in large language models. In Ad-
 vances in Neural Information Processing Systems 35
 (NeurIPS 2022), pages 24824–24837.
Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie
 Fu, Junxian He, and Bryan Hooi. 2024. Can LLMs
 express their uncertainty? an empirical evaluation of
 confidence elicitation in LLMs. In The Twelfth In-
 ternational Conference on Learning Representations
 (ICLR).
Senrong Xu, Yuhao Tan, Yanke Zhou, Guangyuan Wu,
 Zenan Li, Yuan Yao, Taolue Chen, Feng Xu, and Xi-
 aoxing Ma. 2026. Uncertainty quantification for llm-
 based code generation. Preprint, arXiv:2605.12201.
 338
A Evaluation Pipeline and Generation Table 4: Generation parameters by stage. Sampling is enabled
 whenever the temperature is greater than zero. No top-k or
 Parameters repetition penalty is applied. For the stability runs, “as pri-
 mary” means each run reuses the max-token budget of the
Figure 4 summarizes the five stages of the evalua- strategy it repeats. The repair pass uses the temperature of its
tion pipeline described in Section 3. Table 4 lists enclosing run.
the generation parameters used at each stage. Stage Temp. Samp. top-p Max tok. Seed
 All inference was run on the Hábrók high- Code generation 0.0 off 1.0 1024 42
 Direct (primary) 0.0 off 1.0 64 42
performance computing cluster at the University CoT (primary) 0.0 off 1.0 512 42
of Groningen using Transformers 4.57.6, PyTorch Linguistic (primary) 0.0 off 1.0 64 42
 Stability (5 runs) 0.3 on 1.0 as prim. 42+i
2.10.0, Datasets 3.6.0, and Accelerate 1.13.0, with Repair (on failure) run match 1.0 64 42+i+1
all random seeds fixed for reproducibility.
A.1 Metric Definitions B Prompt Templates
Let yi ∈ {0, 1} denote execution-based correctness
and ĉi ∈ [0, 1] confidence for N = 365 predictions. This appendix lists the prompt templates used for
With ten equal-width bins Bm , Expected Calibra- the final experimental outputs. Code generation
tion Error is used provider-specific chat wrappers for Qwen2.5-
 X10 Coder, CodeLlama, and DeepSeek-Coder. Con-
 |Bm |
 ECE = |c̄(Bm ) − ā(Bm )| , (1) fidence elicitation and repair used shared strat-
 N
 m=1 egy prompts across models, passed through each
where c̄(Bm ) and ā(Bm ) are mean confidence and model’s tokenizer chat template where available.
empirical accuracy. Net Calibration Error preserves
direction, Table 5: Prompt templates used in the final pipeline.
 N Pipeline stage Appendix location
 1 X
 NCE = (yi − ĉi ), (2) Qwen2.5-Coder code generation Appendix B.1.1
 N
 i=1 CodeLlama code generation Appendix B.1.2
so negative values indicate overconfidence. AU- Shared code-generation user body Appendix B.1.3
 DeepSeek-Coder code generation Appendix B.1.4
ROC is the probability that a randomly chosen Direct confidence Appendix B.2.1
correct program receives higher confidence than a Chain-of-Thought confidence Appendix B.2.2
randomly chosen incorrect program. For selective Linguistic confidence Appendix B.2.3
 Repair Appendix C.1
prediction, predictions are sorted by confidence,
accuracy is computed at each retained coverage,
and trapezoidal integration yields AUACC; sub- B.1 Code Generation Prompts
tracting unconditional pass@1 accuracy gives the
reported gap. ECE, NCE, and AUROC are addi- B.1.1 Qwen2.5-Coder
tionally computed over 1,000 bootstrap resamples,
 The Qwen2.5-Coder code-generation provider
using percentile 95% confidence intervals.
 used the following system message, passed
 LiveCodeBench
 365 problems
 through the tokenizer chat template with
 2024-09-19 to 2025-
 04-30 · release v6
 add_generation_prompt=True.
 Code generation
 outputs frozen
 greedy · temp.=0 · pass@1
 You are an expert Python programmer. You will
 be given a question (problem specification)
 Correctness scoring
 strict / lenient
 Confidence elicitation
 separate inference pass
 and will generate a correct Python program
 that matches the specification and passes all
 tests. Return only the final code solution.
ground truth labels
 Chain-of-
 Direct Linguistic
 Thought
 integer 0–100 5-point label
 reason then score
 B.1.2 CodeLlama
 Calibration metrics
 The CodeLlama code-generation provider used
 ECE · AUROC · NCE · AUACC
Figure 4: Overview of the evaluation pipeline. Code genera-
tion outputs are frozen before any confidence elicitation pass, the same system message as Qwen2.5-Coder,
ensuring correctness labels are independent of the confidence passed through the tokenizer chat template with
prompts that follow. add_generation_prompt=True.
 339
Table 3: Models evaluated in this study, all loaded unquantized in native BF16 precision from Hugging Face. DeepSeek-Coder
and CodeLlama have documented cutoff evidence; Qwen2.5-Coder has no formal disclosed corpus cutoff, so the evaluation
window is set after the first public arXiv submission of its technical report (Sep. 2024).
 Hugging Face Identifier Family Params Cutoff
 deepseek-ai/deepseek-coder-6.7b-instruct DeepSeek-Coder 6.7B Mar. 2023
 deepseek-ai/deepseek-coder-33b-instruct DeepSeek-Coder 33B Mar. 2023
 codellama/CodeLlama-7b-Instruct-hf CodeLlama 7B Jul. 2023
 codellama/CodeLlama-34b-Instruct-hf CodeLlama 34B Jul. 2023
 Qwen/Qwen2.5-Coder-7B-Instruct Qwen2.5-Coder 7B Before Sep. 2024
 Qwen/Qwen2.5-Coder-32B-Instruct Qwen2.5-Coder 32B Before Sep. 2024
 You are an expert Python programmer. You will B.1.4 DeepSeek-Coder
 be given a question (problem specification)
 and will generate a correct Python program The DeepSeek-Coder provider used a hardcoded
 that matches the specification and passes all prompt format rather than a tokenizer chat tem-
 tests. Return only the final code solution. plate.
B.1.3 Shared Qwen2.5-Coder and CodeLlama
 User Body You are an AI programming assistant,
 utilizing the DeepSeek Coder model, developed
For Qwen2.5-Coder and CodeLlama, the shared
 by DeepSeek Company, and you answer questions
user body began with the following text.
 related to computer science.
 You will be given a question (problem
 ### Instruction:
 specification) and will generate a correct
 You will be given a question (problem
 Python program that matches the specification
 specification) and will generate a correct
 and passes all tests. You will NOT return
 Python program that matches the specification
 anything except for the program.
 and passes all tests. You will NOT return
 anything except for the program.
 Question:
 {question_content}
 Question:
 {question_content}
 When starter code was available, the following
block was appended. {starter_or_stdin_branch}
 You will use the following starter code to ### Response:
 write the solution to the problem and enclose
 your code within delimiters.
 ```python
 {starter_code}
 The {starter_or_stdin_branch} field used
 ```
 the same starter-code or standard-input branch
 shown in Appendix B.1.3.
 When the problem used standard input and out-
put, the following block was appended instead.
 Read the inputs from stdin solve the problem
 and write the answer to stdout (do not
 directly test on the sample inputs). Enclose
 your code within delimiters as follows.
 ```python
 # YOUR CODE HERE
 ```
 340
B.2 Confidence Elicitation Prompts C Parsing and Repair
B.2.1 Direct This appendix documents the repair step and the
 Direct rate at which it was triggered. The repair prompt
 System. You are a code correctness assessor. is given first, the per-cell parse and repair counts
 User. Programming problem: second, and representative malformed outputs third.
 {question_content} Together these show that the models did not always
 follow the requested output format and that a single
 Submitted code: repair call recovered most of the failures.
 {answer}
 C.1 Repair Prompt
 What is the probability (integer 0-100) If primary parsing failed, a single repair call was
 that this exact code passes all hidden test made. For Direct and CoT, the repair system mes-
 cases? sage was constructed by appending the following
 Output EXACTLY one line in the form: instruction to the original system message.
 FINAL_CONFIDENCE: <integer 0-100>
 Your previous reply was not in the required
 Do not add any explanation.
 format. Restate ONLY the final confidence
B.2.2 Chain-of-Thought line, using the same underlying judgment.
 Output EXACTLY one line in the form:
 Chain-of-Thought
 FINAL_CONFIDENCE: <integer 0-100>. Do not add
 System. You are a code correctness assessor. any explanation.
 First, briefly analyse whether the submitted
 code handles edge cases correctly and whether For Linguistic, the repair system message in-
 the algorithm is sound. Then, on the final stead requested the categorical output format.
 line, output EXACTLY: FINAL_CONFIDENCE:
 <integer 0-100>. Do not write anything after Your previous reply was not in the required
 that final line. format. Restate ONLY the final label, using
 the same underlying judgment. Output EXACTLY
 User. Programming problem:
 one line in the form: FINAL_LABEL: <very low|
 {question_content}
 low|moderate|high|very high>. Do not add any
 explanation.
 Submitted code:
 {answer}
 The repair user message was shared across strate-
B.2.3 Linguistic gies.
 Linguistic Original task:
 System. You are a code correctness assessor. {original_user}
 User. Programming problem:
 Your previous (malformed) reply:
 {question_content}
 {previous_response}
 Submitted code:
 Provide the reformatted final line now.
 {answer}
 How confident are you that this code passes
 C.2 Parse and Repair Rates
 all hidden test cases?
 Output EXACTLY one line in the form: Table 6 shows the parse outcome for every (model,
 FINAL_LABEL: <very low|low|moderate|high| strategy) cell across all of the 365 problems. Across
 very high> the full primary pipeline, 5,441 outputs are parsed
 Do not add any explanation. cleanly, 1,123 are repaired successfully, and 6 de-
 fault to confidence 50. The repair rate is not uni-
 Confidence prompts were passed through the to- form across all the cells and is divided amongst
kenizer chat template as a system-user conversation them. For example, CodeLlama-7B CoT is the
with add_generation_prompt=True. most extreme case, with only 55 of 365 outputs
 341
(15.1%) parsing on the first attempt, and DeepSeek- only as a FINAL_LABEL line or as a standalone la-
Coder-6.7B CoT and CodeLlama-34B CoT also re- bel.
quired repair on more than 40% of problems. CoT
is the format the models follow least reliably, which My confidence that this code passes all hidden tests is
is consistent with the longer reasoning trace that high.
gives the model more room to drift away from the
required line at the end. In the evaluation pipeline, the repair call presented
Table 6: Parse and repair outcome counts per (model, strategy)
 the original prompt and the malformed reply and
cell, out of 365 problems. nclean is the number parsed on the asked only for the correctly formatted final line,
first attempt; nrepaired is the number corrected after a failed pri- which recovered the large majority of failures as
mary parse; ndefault is the number that fell back to confidence
50 after both parse and repair failed. shown in Table 6.
 Model Strategy nclean nrepaired ndefault
 D Bootstrap Confidence Intervals
 Qwen2.5-Coder-32B Direct 365 0 0
 Qwen2.5-Coder-32B CoT 359 6 0
 Qwen2.5-Coder-32B Linguistic 365 0 0 Table 7 reports 95% bootstrap confidence intervals
 Qwen2.5-Coder-7B Direct 365 0 0 for ECE, AUROC, and NCE across all 18 model-
 Qwen2.5-Coder-7B CoT 269 96 0
 Qwen2.5-Coder-7B Linguistic 365 0 0 strategy cells under strict scoring.
 DeepSeek-Coder-33B Direct 226 139 0
 DeepSeek-Coder-33B CoT 259 105 1 E Cross-Validated Platt Scaling
 DeepSeek-Coder-33B Linguistic 271 94 0
 DeepSeek-Coder-6.7B Direct 354 11 0
 Diagnostics
 DeepSeek-Coder-6.7B CoT 212 153 0
 DeepSeek-Coder-6.7B Linguistic 365 0 0 In order to check whether the in-sample Platt scal-
 CodeLlama-34B Direct 333 32 0 ing estimates overfit the binned ECE metric, the lo-
 CodeLlama-34B CoT 183 177 5
 CodeLlama-34B Linguistic 365 0 0 gistic transformations were recomputed under five-
 CodeLlama-7B Direct 365 0 0 fold stratified cross-validation. For each model-
 CodeLlama-7B CoT 55 310 0
 CodeLlama-7B Linguistic 365 0 0
 strategy pair, a two-parameter logistic regression
 was fitted on 80% of observations and evaluated
 on the held-out 20%, which produced a fully out-
C.3 Examples of Parse Failures of-fold probability vector across all 365 problems.
The following constructed examples illustrate re- Table 8 reports the resulting ECE alongside the
sponse formats rejected by the parser described in in-sample baseline.
Section 3.3; they are not model outputs from the For fifteen of the eighteen cells, the absolute dif-
main experiment. Table 6 reports observed pars- ference between in-sample and out-of-fold ECE is
ing outcomes. Below is an example of a common below 0.015. The small differences suggest limited
Chain-of-Thought failure, a reasoning trace that in-sample optimism for this metric on the evaluated
never emits a final FINAL_CONFIDENCE line at all. distribution, but do not establish performance on
 other distributions.
 The algorithm looks correct and handles the main cases,
 The near-zero ECE values under Platt scaling
 so it mostly belong to the collapsed cells discussed in
 should pass most of the hidden tests. I am fairly
 confident in Section 4.6. CodeLlama-34B under Direct elic-
 this solution.
 itation, and DeepSeek-Coder-6.7B under Direct
 and Linguistic elicitation, generate confidence out-
A Direct failure typically states the score inside a puts that cluster almost entirely near the maximum
sentence rather than on the required line, so there is value, leaving limited variation for the regression to
no FINAL_CONFIDENCE marker and no standalone use. Predictions close to the base rate can produce
integer for the parser to accept. near-zero local error without demonstrating useful
 discrimination. This does not mean that the orig-
 inal confidence scores contain no discriminative
 I would estimate the probability at around 80 percent.
 information.
 The largest shifts observed are DeepSeek-Coder-
A Linguistic failure embeds the label in a sentence, 33B Linguistic (+0.027) and CodeLlama-7B Di-
which the parser ignores because a label is accepted rect (−0.030). At n = 365, these differences may
 342
Table 7: 95% bootstrap confidence intervals for ECE, AUROC, and NCE under strict scoring, computed from 1000 resamples
with replacement. Each interval is the [2.5th, 97.5th] percentile of the bootstrap distribution. Point estimates repeat Table 1 for
reference.
 ECE AUROC NCE
 Model Strategy Point 95% CI Point 95% CI Point 95% CI
 Qwen2.5-Coder-32B Direct 0.327 [0.28, 0.37] 0.834 [0.79, 0.88] −0.294 [−0.34, −0.25]
 Qwen2.5-Coder-32B CoT 0.330 [0.29, 0.37] 0.810 [0.76, 0.85] −0.324 [−0.37, −0.28]
 Qwen2.5-Coder-32B Linguistic 0.216 [0.18, 0.25] 0.841 [0.80, 0.88] −0.216 [−0.25, −0.18]
 Qwen2.5-Coder-7B Direct 0.624 [0.59, 0.66] 0.766 [0.71, 0.82] −0.619 [−0.66, −0.57]
 Qwen2.5-Coder-7B CoT 0.506 [0.46, 0.55] 0.772 [0.71, 0.83] −0.495 [−0.54, −0.45]
 Qwen2.5-Coder-7B Linguistic 0.507 [0.47, 0.55] 0.709 [0.66, 0.76] −0.505 [−0.55, −0.46]
 DeepSeek-Coder-33B Direct 0.183 [0.15, 0.22] 0.760 [0.70, 0.82] −0.057 [−0.10, −0.01]
 DeepSeek-Coder-33B CoT 0.553 [0.51, 0.59] 0.675 [0.61, 0.74] −0.536 [−0.58, −0.49]
 DeepSeek-Coder-33B Linguistic 0.258 [0.22, 0.30] 0.638 [0.56, 0.72] −0.197 [−0.24, −0.16]
 DeepSeek-Coder-6.7B Direct 0.849 [0.82, 0.89] 0.518 [0.51, 0.53] −0.849 [−0.88, −0.82]
 DeepSeek-Coder-6.7B CoT 0.779 [0.75, 0.81] 0.716 [0.66, 0.77] −0.779 [−0.81, −0.75]
 DeepSeek-Coder-6.7B Linguistic 0.713 [0.68, 0.75] 0.498 [0.44, 0.55] −0.713 [−0.75, −0.68]
 CodeLlama-34B Direct 0.813 [0.78, 0.84] 0.655 [0.58, 0.75] −0.813 [−0.84, −0.78]
 CodeLlama-34B CoT 0.814 [0.78, 0.84] 0.620 [0.50, 0.73] −0.814 [−0.84, −0.78]
 CodeLlama-34B Linguistic 0.660 [0.63, 0.69] 0.681 [0.64, 0.72] −0.660 [−0.69, −0.63]
 CodeLlama-7B Direct 0.862 [0.83, 0.89] 0.639 [0.55, 0.73] −0.862 [−0.89, −0.83]
 CodeLlama-7B CoT 0.680 [0.65, 0.71] 0.556 [0.45, 0.66] −0.663 [−0.70, −0.62]
 CodeLlama-7B Linguistic 0.013 [0.01, 0.05] 0.491 [0.48, 0.50] −0.012 [−0.04, 0.02]
reflect sample-to-fold variability and changes in a string, an error, or a parse failure. When both
bin placement. sides are numbers, the model’s answer is accepted
 All of this taken together, the cross-validation if it falls within 10% of the expected value, that
results support reading scalar ECE alongside the is |ypred − ytrue |/|ytrue | ≤ τ . When the expected
confidence histogram and AUROC rather than just answer is 0, a percentage tolerance is effectively
as a number by itself, consistent with the broader meaningless, so a separate absolute check is used
interpretive point that was outlined in Section 5.4. when |ytrue | < 10−6 , accepting the prediction if
 |ypred − ytrue | ≤ 10−6 . Anything that cannot be
F Leniency Threshold Sensitivity parsed as a number, including non-finite values and
 parse failures, remains a strict failure and stays in
The main text evaluates correctness under strict
 the analysis denominator.
scoring, under which a solution is correct if and
only if the hidden-test evaluator determines that
 F.2 Relative-Tolerance Sweep
it passes the test case(s). Because some L IVE -
C ODE B ENCH problems request a single numeric Design
value, a strict-failure solution that produces a nu-
merically close answer may still be useful as a The sweep evaluates τ ∈
secondary diagnostic. This is what is defined as le- {0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5} for
nient scoring, so essentially giving the model some all six models and three confidence-elicitation
benefit of doubt in its answer if it’s close enough. strategies (Direct, CoT, Linguistic), giving 126
This appendix first compares strict scoring with the metric triples in addition to the Strict baseline
primary lenient threshold of τ = 0.10, then reports that is used throughout the main text. Confidence
how the three primary calibration metrics change values are loaded from the frozen merged JSON
across relative numeric leniency thresholds from files that were stored after generation, so without
τ = 0.1% to τ = 50%. re-running any model inference. The primary
 threshold used throughout the main text is
F.1 Strict vs. Lenient Correctness τ = 0.10 (10% relative tolerance).
Table 9 compares strict and primary-lenient (τ =
 Pass@1 accuracy
0.10) metrics for all 18 (model, strategy) cells. Un-
der lenient scoring, all strict passes remain correct. Table 10 reports mean accuracy (pass@1) under
Some strict failures are additionally reclassified each threshold. Because accuracy is a property
as correct, but only when both the model’s out- of the model outputs rather than the confidence
put and the expected answer are actual numbers, distribution, all three strategies for a given model
since there is nothing to compare if either side is share the same accuracy at every threshold.
 343
Table 8: Comparison of in-sample and five-fold cross-validated (CV) Platt scaling ECE across all eighteen model-strategy
combinations under strict scoring (N = 365). Positive ∆ values indicate in-sample optimism; negative values indicate that the
full-sample estimator inflated ECE relative to the out-of-fold estimate. Cells with near-zero values reflect distribution collapse
rather than calibration.
 Model Strategy Pos. Rate In-Sample ECE CV ECE ∆ (CV − In-Sample)
 Qwen2.5-Coder-32B Direct 0.299 0.0366 0.0396 +0.0030
 Qwen2.5-Coder-32B CoT 0.299 0.0395 0.0430 +0.0035
 Qwen2.5-Coder-32B Linguistic 0.299 0.0756 0.0854 +0.0098
 Qwen2.5-Coder-7B Direct 0.164 0.0978 0.0738 −0.0240
 Qwen2.5-Coder-7B CoT 0.164 0.0531 0.0559 +0.0029
 Qwen2.5-Coder-7B Linguistic 0.164 0.0409 0.0407 −0.0002
 DeepSeek-Coder-33B Direct 0.189 0.0123 0.0267 +0.0144
 DeepSeek-Coder-33B CoT 0.189 0.0432 0.0449 +0.0017
 DeepSeek-Coder-33B Linguistic 0.189 0.0150 0.0419 +0.0268
 DeepSeek-Coder-6.7B Direct 0.142 0.0000 0.0000 +0.0000
 DeepSeek-Coder-6.7B CoT 0.142 0.0167 0.0028 −0.0139
 DeepSeek-Coder-6.7B Linguistic 0.142 0.0000 0.0002 +0.0001
 CodeLlama-34B Direct 0.082 0.0000 0.0001 +0.0000
 CodeLlama-34B CoT 0.082 0.0000 0.0001 +0.0001
 CodeLlama-34B Linguistic 0.082 0.0273 0.0199 −0.0074
 CodeLlama-7B Direct 0.099 0.0572 0.0273 −0.0299
 CodeLlama-7B CoT 0.099 0.0000 0.0126 +0.0126
 CodeLlama-7B Linguistic 0.099 0.0001 0.0000 −0.0001
 Table 9: Strict vs. lenient (τ = 0.10) calibration metrics for all 18 cells.
 Strict Lenient (τ = 10%)
 Model Strategy ECE AUROC NCE ECE AUROC NCE
 Qwen2.5-Coder-32B Direct 0.327 0.834 −0.294 0.319 0.804 −0.259
 Qwen2.5-Coder-32B CoT 0.330 0.810 −0.324 0.299 0.782 −0.288
 Qwen2.5-Coder-32B Linguistic 0.216 0.841 −0.216 0.180 0.813 −0.180
 Qwen2.5-Coder-7B Direct 0.624 0.766 −0.619 0.599 0.763 −0.594
 Qwen2.5-Coder-7B CoT 0.506 0.772 −0.495 0.487 0.772 −0.471
 Qwen2.5-Coder-7B Linguistic 0.507 0.709 −0.505 0.482 0.716 −0.481
 DeepSeek-Coder-33B Direct 0.183 0.760 −0.057 0.197 0.736 −0.038
 DeepSeek-Coder-33B CoT 0.553 0.675 −0.536 0.533 0.674 −0.517
 DeepSeek-Coder-33B Linguistic 0.258 0.638 −0.197 0.244 0.628 −0.178
 DeepSeek-Coder-6.7B Direct 0.849 0.518 −0.849 0.830 0.518 −0.830
 DeepSeek-Coder-6.7B CoT 0.779 0.716 −0.779 0.760 0.724 −0.760
 DeepSeek-Coder-6.7B Linguistic 0.713 0.498 −0.713 0.694 0.499 −0.694
 CodeLlama-34B Direct 0.813 0.655 −0.813 0.807 0.645 −0.807
 CodeLlama-34B CoT 0.814 0.620 −0.814 0.808 0.587 −0.808
 CodeLlama-34B Linguistic 0.660 0.681 −0.660 0.655 0.684 −0.655
 CodeLlama-7B Direct 0.862 0.639 −0.862 0.854 0.621 −0.854
 CodeLlama-7B CoT 0.680 0.556 −0.663 0.671 0.557 −0.655
 CodeLlama-7B Linguistic 0.013 0.491 −0.012 0.021 0.491 −0.004
Net Calibration Error Expected Calibration Error
 Table 12 reports ECE. For most cells, ECE de-
Table 11 reports NCE = mean(accuracy − confi- creases or remains stable as τ increases because
dence). Figure 5 shows all 18 NCE curves on a promoting strict failures to correct narrows the
categorical axis; the NCE = 0 line separates over- confidence–accuracy gap. There are some ex-
confident (negative) from underconfident (positive) ceptions, DeepSeek-Coder-33B Direct rises from
cells. 0.183 under Strict to 0.315 at τ = 0.5, while
 At τ = 0.10, all 18 (model, strategy) cells re- CodeLlama-7B Linguistic increases as the thresh-
main at negative NCE, confirming systematic over- old becomes more permissive. Qwen2.5-Coder-
confidence under strict and mildly lenient scoring. 32B Direct shows non-monotonicity. For Qwen2.5-
Two cells first cross zero between τ = 0.10 and Coder-32B, Linguistic remains the lowest-ECE
τ = 0.25: CodeLlama-7B Linguistic (NCE rises strategy at every tested threshold, while Direct and
from −0.004 to +0.021) and DeepSeek-Coder- CoT remain close and change order. ECE values
33B Direct (NCE rises from −0.038 to +0.017). and some AUROC strategy rankings also shift at
No cell crosses zero at or below τ = 0.10. higher thresholds, so strict scoring remains the pri-
 344
Table 10: Pass@1 accuracy under relative numeric leniency. Strict uses strict scoring; τ columns use lenient scoring. All
strategies within a model share the same accuracy.
 Model Strict 0.1% 0.5% 1% 5% 10% 25% 50%
 Qwen2.5-Coder-32B 0.299 0.310 0.312 0.312 0.321 0.334 0.389 0.460
 Qwen2.5-Coder-7B 0.164 0.170 0.173 0.175 0.181 0.189 0.225 0.337
 DeepSeek-Coder-33B 0.189 0.195 0.195 0.195 0.203 0.208 0.263 0.359
 DeepSeek-Coder-6.7B 0.142 0.145 0.148 0.151 0.156 0.162 0.200 0.293
 CodeLlama-34B 0.082 0.082 0.082 0.082 0.085 0.088 0.096 0.126
 CodeLlama-7B 0.099 0.099 0.101 0.101 0.104 0.107 0.132 0.244
Table 11: NCE under relative numeric leniency. Negative values indicate overconfidence; the Strict column matches Table 1.
 Model Strategy Strict 0.1% 0.5% 1% 5% 10% 25% 50%
 Qwen2.5-Coder-32B Direct −0.294 −0.283 −0.281 −0.281 −0.272 −0.259 −0.204 −0.133
 Qwen2.5-Coder-32B CoT −0.324 −0.313 −0.310 −0.310 −0.302 −0.288 −0.234 −0.162
 Qwen2.5-Coder-32B Linguistic −0.216 −0.205 −0.202 −0.202 −0.194 −0.180 −0.125 −0.054
 Qwen2.5-Coder-7B Direct −0.619 −0.613 −0.610 −0.608 −0.602 −0.594 −0.558 −0.446
 Qwen2.5-Coder-7B CoT −0.495 −0.490 −0.487 −0.484 −0.479 −0.471 −0.435 −0.323
 Qwen2.5-Coder-7B Linguistic −0.505 −0.500 −0.497 −0.495 −0.489 −0.481 −0.445 −0.333
 DeepSeek-Coder-33B Direct −0.057 −0.052 −0.052 −0.052 −0.044 −0.038 +0.017 +0.113
 DeepSeek-Coder-33B CoT −0.536 −0.531 −0.531 −0.531 −0.522 −0.517 −0.462 −0.366
 DeepSeek-Coder-33B Linguistic −0.197 −0.192 −0.192 −0.192 −0.183 −0.178 −0.123 −0.027
 DeepSeek-Coder-6.7B Direct −0.849 −0.847 −0.844 −0.841 −0.836 −0.830 −0.792 −0.699
 DeepSeek-Coder-6.7B CoT −0.779 −0.776 −0.774 −0.771 −0.765 −0.760 −0.722 −0.628
 DeepSeek-Coder-6.7B Linguistic −0.713 −0.710 −0.708 −0.705 −0.699 −0.694 −0.656 −0.562
 CodeLlama-34B Direct −0.813 −0.813 −0.813 −0.813 −0.810 −0.807 −0.799 −0.769
 CodeLlama-34B CoT −0.814 −0.814 −0.814 −0.814 −0.811 −0.808 −0.800 −0.770
 CodeLlama-34B Linguistic −0.660 −0.660 −0.660 −0.660 −0.657 −0.655 −0.646 −0.616
 CodeLlama-7B Direct −0.862 −0.862 −0.859 −0.859 −0.856 −0.854 −0.829 −0.717
 CodeLlama-7B CoT −0.663 −0.663 −0.660 −0.660 −0.658 −0.655 −0.630 −0.518
 CodeLlama-7B Linguistic −0.012 −0.012 −0.010 −0.010 −0.007 −0.004 +0.021 +0.133
mary correctness definition throughout. has to accept worse and worse answers. This was
 purely reported to see if the models can get close to
Area Under the ROC Curve the answers it needs, and if so, what that threshold
Table 13 shows AUROC; AUROC is stable or would be.
slightly decreasing with τ for most cells; pro-
moting strict failures can reduce class separation.
CodeLlama-34B CoT shows non-monotone AU- G Strategy Ranking by ECE
ROC across thresholds; AUROC for CodeLlama-
7B Linguistic remains approximately constant,
changing from 0.491 to 0.489 at τ = 0.50, with a 1.0
 Direct
nearly constant confidence distribution. Strategy CoT
 Linguistic
rankings are mostly preserved across thresholds, 0.8
but some change at higher tolerances.
 ECE (strict, lower is better)
 0.6
F.3 Interpretation 0.4
Overall, the evidence across all three metrics 0.2
clearly supports treating τ = 0.10 as the primary collapsed dist.
threshold for sensitivity analysis, while strict scor- 0.0
 2 B -7B 3B .7B 34B 7B
 en-3 wen ek-3 ek-6 ma- ma-
 Qw pSe pSe eLla
ing remains the primary correctness definition in Q
 Dee Dee Cod
 eLla Cod
the main text. At τ = 0.10, the qualitative findings Figure 6: ECE under strict scoring per model grouped by
from the main text are unchanged. All 18 cells elicitation strategy. Lower is better. Error bars show asym-
 metric 95% bootstrap confidence intervals. The near-zero
remain overconfident under NCE, Linguistic re- CodeLlama-7B Linguistic bar reflects distribution collapse
mains among the better-performing ECE strategies (Section 4.6).
for Qwen2.5-Coder-32B, and the Qwen2.5-Coder
cells retain comparatively strong AUROC discrimi-
nation. Anything higher to be reported in the main Table 14 provides strategy rankings by strict ECE
text would come at the cost to the developer who within each model.
 345
 NCE under relative numeric leniency sweep
 Model
 0.0 Qwen2.5-Coder-32B
 NCE (mean accuracy - mean confidence)
 Qwen2.5-Coder-7B
 DeepSeek-Coder-33B
 DeepSeek-Coder-6.7B
 CodeLlama-34B
 0.2 CodeLlama-7B
 0.4
 Strategy
 Direct
 0.6 CoT
 Linguistic
 NCE = 0
 0.8
 Strict 0.1% 0.5% 1% 5% 10% 25% 50%
 Correctness threshold
Figure 5: NCE for all 18 (model, strategy) cells across the leniency sweep. The leftmost position is strict. Subsequent positions
are lenient correct scores at increasing τ . The dashed horizontal line marks NCE = 0. Line colour encodes model; linestyle
encodes strategy (solid = Direct, dashed = CoT, dotted = Linguistic).
H Within-Family Scaling Statistics Table 17: Stability analysis across all 18 cells. Mean std dev is
 the average sample standard deviation of confidence over five
 temperature-0.3 runs on the 0–100 scale. Cells are classified
Table 15 provides detailed scaling statistics for all as stable (mean std dev < 5), marginal (5 ≤ mean std dev
six models. Mean ECE and mean AUROC are < 10), or unstable (mean std dev ≥ 10). Unstable cells are
averaged over the three elicitation strategies under shown in bold.
strict scoring. The CodeLlama-7B mean ECE of Model Strategy Mean Category
0.518 is distorted by the degenerate Linguistic cell; std dev
excluding that cell raises the corrected mean to Qwen2.5-Coder-32B Direct 4.14 stable
0.771, as noted in Section 4.5 and Figure 7. Qwen2.5-Coder-32B CoT 7.93 marginal
 Qwen2.5-Coder-32B Linguistic 1.67 stable
Table 15: Scaling comparison within each family under strict Qwen2.5-Coder-7B Direct 8.96 marginal
scoring. Mean ECE and AUROC are averaged over the Qwen2.5-Coder-7B CoT 19.59 unstable
three strategies. ‡ marks the CodeLlama accuracy inversion. Qwen2.5-Coder-7B Linguistic 8.78 marginal
CodeLlama-7B mean ECE excluding the degenerate Linguis- DeepSeek-Coder-33B Direct 9.89 marginal
tic cell is 0.771. DeepSeek-Coder-33B CoT 20.29 unstable
 Family Model Acc. Mean ECE Mean AUROC DeepSeek-Coder-33B Linguistic 13.81 unstable
 Qwen 32B 0.299 0.291 0.828 DeepSeek-Coder-6.7B Direct 2.64 stable
 Qwen 7B 0.164 0.546 0.749 DeepSeek-Coder-6.7B CoT 6.94 marginal
 DeepSeek-Coder-6.7B Linguistic 7.98 marginal
 DeepSeek 33B 0.189 0.331 0.691
 DeepSeek 6.7B 0.142 0.780 0.577 CodeLlama-34B Direct 5.84 marginal
 CodeLlama 34B 0.082‡ 0.762 0.652 CodeLlama-34B CoT 7.91 marginal
 CodeLlama 7B 0.099‡ 0.518 0.562 CodeLlama-34B Linguistic 12.01 unstable
 CodeLlama-7B Direct 7.59 marginal
 CodeLlama-7B CoT 17.32 unstable
 CodeLlama-7B Linguistic 6.19 marginal
I Collapsed Distribution Statistics
Table 16 provides distribution statistics for all eight
collapsed model-strategy cells identified in Sec- K Reliability Diagrams
tion 4.6.
 Figure 11 shows reliability diagrams for all 18
J Full Stability Analysis model-strategy cells under strict scoring, arranged
 by model in rows and elicitation strategy in
Table 17 reports mean sample standard deviation columns. Each panel plots mean elicited confi-
across five temperature-0.3 runs per cell for all 18 dence (x-axis) against the empirical fraction cor-
model-strategy combinations. rect (y-axis) for predictions falling in each of 10
 346
 Table 12: ECE under relative numeric leniency. The Strict column matches Table 1.
 Model Strategy Strict 0.1% 0.5% 1% 5% 10% 25% 50%
 Qwen2.5-Coder-32B Direct 0.327 0.316 0.313 0.313 0.316 0.319 0.313 0.297
 Qwen2.5-Coder-32B CoT 0.330 0.319 0.316 0.316 0.308 0.299 0.269 0.269
 Qwen2.5-Coder-32B Linguistic 0.216 0.205 0.202 0.202 0.194 0.180 0.125 0.073
 Qwen2.5-Coder-7B Direct 0.624 0.619 0.616 0.613 0.608 0.599 0.569 0.495
 Qwen2.5-Coder-7B CoT 0.506 0.501 0.498 0.495 0.490 0.487 0.457 0.392
 Qwen2.5-Coder-7B Linguistic 0.507 0.502 0.499 0.496 0.491 0.482 0.447 0.375
 DeepSeek-Coder-33B Direct 0.183 0.189 0.189 0.189 0.192 0.197 0.246 0.315
 DeepSeek-Coder-33B CoT 0.553 0.547 0.547 0.547 0.539 0.533 0.501 0.416
 DeepSeek-Coder-33B Linguistic 0.258 0.252 0.252 0.252 0.244 0.244 0.228 0.183
 DeepSeek-Coder-6.7B Direct 0.849 0.847 0.844 0.841 0.836 0.830 0.792 0.699
 DeepSeek-Coder-6.7B CoT 0.779 0.776 0.774 0.771 0.765 0.760 0.722 0.628
 DeepSeek-Coder-6.7B Linguistic 0.713 0.710 0.708 0.705 0.699 0.694 0.656 0.562
 CodeLlama-34B Direct 0.813 0.813 0.813 0.813 0.810 0.807 0.799 0.769
 CodeLlama-34B CoT 0.814 0.814 0.814 0.814 0.811 0.808 0.800 0.770
 CodeLlama-34B Linguistic 0.660 0.660 0.660 0.660 0.657 0.655 0.646 0.616
 CodeLlama-7B Direct 0.862 0.862 0.859 0.859 0.856 0.854 0.829 0.717
 CodeLlama-7B CoT 0.680 0.680 0.677 0.677 0.674 0.671 0.647 0.540
 CodeLlama-7B Linguistic 0.013 0.013 0.016 0.016 0.018 0.021 0.046 0.158
 DeepSeek-Coder-6.7B 0.85
 0.80 Qwen2.5-Coder-32B
 CodeLlama-34B
 0.80
 0.70 Qwen2.5-Coder-7B
 Mean ECE (lower is better) Mean AUROC (higher is better)
 0.75
 0.60
 Qwen2.5-Coder-7B DeepSeek-Coder-33B
 0.70
 0.50
 CodeLlama-7B 0.65
 CodeLlama-34B
 0.40 DeepSeek-Coder-6.7B
 DeepSeek-Coder-33B 0.60
 0.30 CodeLlama-7B
 Qwen2.5-Coder-32B 0.55
 Small scale Large scale Small scale Large scale
 (6.7/7B) (32/34B) (6.7/7B) (32/34B)
 CodeLlama-7B mean ECE = 0.771 when excluding the degenerate Linguistic cell.
Figure 7: Mean ECE and mean AUROC averaged over three strategies, plotted against model scale within each family under
strict scoring. Lines connect the small-scale and large-scale variants within each family. The CodeLlama ECE line is distorted by
the degenerate CL-7B Linguistic cell (see Section 4.5).
equal-width confidence bins. The dashed diago- repair and instead immediately assigns 50. We use
nal represents perfect calibration; points below it the saved parsing records to identify the responses
indicate overconfidence. from the models that were in need of repair. Across
 the 18 combinations, 1,129 responses needed re-
L Confidence Score Distributions pair, of which 1,123 yielded an output with a confi-
 dence score, while six received the fallback value
Figure 12 displays the full confidence score distri-
 of 50.
butions for all 18 model-strategy cells under strict
scoring, arranged by model in rows and strategy in Both policies are evaluated on the same 365 gen-
columns. erated programs for each model-strategy combi-
 nation, with the same test outcomes. Responses
M Accuracy-Coverage Curves whose confidence cannot be parsed are kept in
 the comparison, so any differences between the
Figure 10 shows accuracy-coverage curves for all policies arise from the confidence scores assigned
18 model-strategy cells under strict scoring. rather than from excluding programs. The re-
 sponses that were malformed originally were over-
N Repair Policy Ablation written by the repair output; thus, this comparison
The main pipeline makes one repair call after a is unable to verify whether repair manages to pre-
failed primary parse, then defaults to a confidence serve the original judgment.
of 50 if repair also fails. The alternative here skips Table 19 reports all cells. Table 20 gives confi-
 347
 Table 13: AUROC under relative numeric leniency. The Strict column matches Table 1.
 Model Strategy Strict 0.1% 0.5% 1% 5% 10% 25% 50%
 Qwen2.5-Coder-32B Direct 0.834 0.838 0.836 0.836 0.824 0.804 0.770 0.743
 Qwen2.5-Coder-32B CoT 0.810 0.810 0.809 0.809 0.802 0.782 0.759 0.730
 Qwen2.5-Coder-32B Linguistic 0.841 0.841 0.839 0.839 0.830 0.813 0.778 0.748
 Qwen2.5-Coder-7B Direct 0.766 0.770 0.765 0.771 0.775 0.763 0.749 0.647
 Qwen2.5-Coder-7B CoT 0.772 0.777 0.777 0.781 0.782 0.772 0.759 0.677
 Qwen2.5-Coder-7B Linguistic 0.709 0.713 0.714 0.716 0.719 0.716 0.698 0.603
 DeepSeek-Coder-33B Direct 0.760 0.750 0.750 0.750 0.745 0.736 0.673 0.624
 DeepSeek-Coder-33B CoT 0.675 0.679 0.679 0.679 0.677 0.674 0.636 0.591
 DeepSeek-Coder-33B Linguistic 0.638 0.641 0.641 0.641 0.639 0.628 0.571 0.546
 DeepSeek-Coder-6.7B Direct 0.518 0.518 0.518 0.518 0.518 0.518 0.519 0.515
 DeepSeek-Coder-6.7B CoT 0.716 0.719 0.721 0.723 0.728 0.724 0.674 0.669
 DeepSeek-Coder-6.7B Linguistic 0.498 0.500 0.489 0.491 0.495 0.499 0.518 0.525
 CodeLlama-34B Direct 0.655 0.655 0.655 0.655 0.649 0.645 0.631 0.621
 CodeLlama-34B CoT 0.620 0.620 0.620 0.620 0.603 0.587 0.599 0.602
 CodeLlama-34B Linguistic 0.681 0.681 0.681 0.681 0.683 0.684 0.672 0.634
 CodeLlama-7B Direct 0.639 0.639 0.624 0.624 0.615 0.621 0.611 0.554
 CodeLlama-7B CoT 0.556 0.556 0.555 0.555 0.546 0.557 0.551 0.573
 CodeLlama-7B Linguistic 0.491 0.491 0.491 0.491 0.491 0.491 0.491 0.489
Table 14: Strategy ranking by strict ECE within each model. Rankings are based on point estimates; near-ties should be
interpreted with the bootstrap intervals in Appendix D. † marks cells with collapsed confidence distributions.
 Model Best Second Worst
 Qwen-32B Ling. (0.216) Dir. (0.327) CoT (0.330)
 Qwen-7B CoT/Ling.† (0.506/0.507) – Dir. (0.624)
 DS-33B Dir.† (0.183) Ling. (0.258) CoT (0.553)
 DS-6.7B Ling.† (0.713) CoT (0.779) Dir.† (0.849)
 CL-34B Ling.† (0.660) Dir.† (0.813) CoT (0.814)
 CL-7B Ling.† (0.013) CoT (0.680) Dir.† (0.862)
dence intervals for the differences. We repeatedly (Vashurin et al., 2025):
sample problems with replacement, using the same
sample for both policies to keep the comparisons A − Ar
 PRR = (3)
paired. For each sample, we recalculate all metrics, Ao − Ar
including PRR and its random and ideal reference We calculate all three areas by trapezoidal inte-
orderings. The fixed fallback can improve ECE gration with the same coverage values k/N for
simply by lowering overconfident scores. This im- k = 1, . . . , N . We exclude zero coverage because
provement does not show that repair harmed an accuracy is undefined when no programs are re-
original judgment. Neither policy uniformly im- tained. If p is the fraction of programs that pass
proves ranking. all tests, random ordering has expected accuracy p
 at every retained fraction, so Ar = p(N − 1)/N .
O Prediction Rejection Ratio
 Ideal ordering has accuracy min(k, N p)/k, since
For each model-strategy combination, we order N p programs are correct. If a PRR of zero occurs,
programs from highest to lowest confidence and it corresponds to a random ordering, and a value
calculate accuracy among the top k programs. Cov- of one corresponds to ideal ordering, along with
erage is the retained fraction k/N , where N is the potential negative values that indicate worse-than-
total number of programs. Varying k from 1 to N random performance.
gives an accuracy-coverage curve. We compare the Furthermore, PRR normalization and the treat-
area under this curve, A, with the areas under ran- ment of equal confidence scores are separate
dom ordering, Ar , and ideal (i.e., oracle) ordering, choices. Notably, confidence scores do not pro-
Ao . The ideal ordering places all correct programs vide any ordering within a tied group, so we give
before all incorrect programs. PRR expresses the every possible ordering within that group equal
improvement over random ordering as a fraction weight. Thus, suppose a tied group contains m
of the improvement possible under ideal ordering programs, of which s are correct. The higher-
 348
Table 16: Distribution statistics for all eight collapsed model-strategy cells. A distribution is classified as collapsed when a single
20-bin interval contains at least 50% of all predictions. The table reports the exact modal confidence value and the dominant
20-bin histogram interval separately; these coincide for all cells except CodeLlama-7B Direct. Confidence values are normalised
to [0, 1]. AUROC is included to indicate whether the collapsed distribution retains discriminative ability.
 Exact modal value Dominant 20-bin
 Model Strategy Value nmodal / 365 Interval nbin / 365 AUROC
 Qwen2.5-Coder-7B Linguistic 0.90 202 (55.3%) [0.90, 0.95) 202 (55.3%) 0.709
 DeepSeek-Coder-33B Direct 0.00* 275 (75.3%) [0.00, 0.05) 275 (75.3%) 0.760
 DeepSeek-Coder-6.7B Direct 1.00 354 (97.0%) [0.95, 1.00] 354 (97.0%) 0.518
 DeepSeek-Coder-6.7B Linguistic 0.90 305 (83.6%) [0.90, 0.95) 305 (83.6%) 0.498
 CodeLlama-34B Direct 0.90 314 (86.0%) [0.90, 0.95) 314 (86.0%) 0.655
 CodeLlama-34B Linguistic 0.90 232 (63.6%) [0.90, 0.95) 232 (63.6%) 0.681
 CodeLlama-7B Linguistic 0.10 359 (98.4%) [0.10, 0.15) 359 (98.4%) 0.491
 CodeLlama-7B Direct 1.00 155 (42.5%) [0.95, 1.00] 293 (80.3%) 0.639
*
 DS-33B Direct is bimodal. A secondary mode at confidence 1.00 accounts for 89 predictions (24.4%); both modes are visible in
Figure 8.
 CodeLlama-7B Linguistic DeepSeek-33B Direct CodeLlama-7B Direct
 300
 350 98.4% in [10, 15] 75.3% in [0, 5] 24.4% at 100 80.3% in [95, 100]
 250
 300 250
 250 200
 200
 200 150
 Count Count Count 150
 150
 100 100
 100
 50 50
 50
 0 0 0
 0 20 40 60 80 100 0 20 40 60 80 100 0 20 40 60 80 100
 Confidence Confidence Confidence
Figure 8: Confidence histograms for three extreme cells using 20 bins on the 0–100 confidence scale. CodeLlama-7B Linguistic
concentrates 98.4% of predictions at confidence 10 (AUROC 0.491); DeepSeek-Coder-33B Direct is bimodal at 0 and 100
(AUROC 0.760); CodeLlama-7B Direct concentrates 80.3% of predictions in the top bin [95, 100], with 42.5% at the exact
maximum value (AUROC 0.639).
 50
Confidence Std Dev (0 100 scale)
 40
 30
 20
 10 unstable threshold
 stable threshold
 0
 Qwen-32B Qwen-7B Qwen-32B Qwen-7B Qwen-32B Qwen-7B
 DeepSeek-33B DeepSeek-6.7B CodeLlama-34B CodeLlama-7B DeepSeek-33B DeepSeek-6.7B CodeLlama-34B CodeLlama-7B DeepSeek-33B DeepSeek-6.7B CodeLlama-34B CodeLlama-7B
 Direct CoT Linguistic
Figure 9: Distribution of per-problem confidence standard deviation across five temperature-0.3 runs, grouped by elicitation
strategy across all six models. CoT cells show higher mean standard deviations than Direct cells for every model and than
Linguistic cells for four of the six models.
confidence groups contain b programs, of which c is
are correct. Retaining the first j programs from the c + js/m
 E[accuracyb+j ] = . (4)
tied group adds js/m correct programs on average. b+j
For j = 1, . . . , m, the expected retained accuracy Integrating the expected accuracies yields the
 exact mean area across all possible orderings within
 349
Table 18: AUACC gaps (area under the accuracy–coverage curve minus overall pass@1 accuracy) for all 18 model–strategy
combinations under strict scoring. Programs with equal confidence retain their saved-file order; negative gaps are shown in bold.
Appendix O reports PRR and examines the effect of averaging equal-score orderings. ‡ marks the CodeLlama accuracy inversion.
Accuracy–coverage curves are in Appendix M.
 Model Acc. (baseline) Direct gap CoT gap Linguistic gap
 Qwen2.5-Coder-32B 0.299 +0.236 +0.195 +0.264
 Qwen2.5-Coder-7B 0.164 +0.130 +0.116 +0.087
 DeepSeek-Coder-33B 0.189 +0.145 +0.072 +0.090
 DeepSeek-Coder-6.7B 0.142 −0.026 +0.044 −0.024
 CodeLlama-34B 0.082‡ +0.044 +0.007 −0.004
 CodeLlama-7B 0.099‡ +0.036 +0.015 −0.025
Table 19: Full-set repair sensitivity (N = 365 per cell). R: saved repair pipeline; F: no repair, immediate fallback to 50 after an
initial parse failure. PRR averages over possible orderings of programs with equal confidence. Accuracy is unchanged. The eight
combinations without repair attempts are included.
 Repair ECE ↓ AUROC ↑ PRR ↑
 Model Strategy attempts R F R F R F
 Qwen-32B Direct 0 0.327 0.327 0.834 0.834 0.633 0.633
 Qwen-32B CoT 6 0.330 0.332 0.810 0.811 0.525 0.526
 Qwen-32B Linguistic 0 0.216 0.216 0.841 0.841 0.705 0.705
 Qwen-7B Direct 0 0.624 0.624 0.766 0.766 0.428 0.428
 Qwen-7B CoT 96 0.506 0.471 0.772 0.743 0.413 0.372
 Qwen-7B Linguistic 0 0.507 0.507 0.709 0.709 0.257 0.257
 DS-33B Direct 139 0.183 0.330 0.760 0.736 0.474 0.453
 DS-33B CoT 106 0.553 0.520 0.675 0.705 0.239 0.306
 DS-33B Linguistic 94 0.258 0.279 0.638 0.618 0.291 0.272
 DS-6.7B Direct 11 0.849 0.841 0.518 0.521 0.016 0.019
 DS-6.7B CoT 153 0.779 0.628 0.716 0.697 0.257 0.255
 DS-6.7B Linguistic 0 0.713 0.713 0.498 0.498 -0.003 -0.003
 CL-34B Direct 32 0.813 0.784 0.655 0.674 0.310 0.352
 CL-34B CoT 182 0.814 0.635 0.620 0.620 0.160 0.150
 CL-34B Linguistic 0 0.660 0.660 0.681 0.681 0.167 0.167
 CL-7B Direct 0 0.862 0.862 0.639 0.639 0.178 0.178
 CL-7B CoT 310 0.680 0.445 0.556 0.546 0.096 0.109
 CL-7B Linguistic 0 0.013 0.013 0.491 0.491 -0.029 -0.029
Table 20: Paired policy differences, F minus R, with 95% percentile intervals from 1,000 problem-level paired bootstrap
resamples (seed 42). ECE below zero favors fallback; AUROC/PRR above zero favors fallback. Intervals are descriptive and
unadjusted for multiple comparisons. Cells without attempted repair have exactly zero differences and are omitted.
 Model Strategy ∆ECE [95% CI] ∆AUROC [95% CI] ∆PRR [95% CI]
 Qwen-32B CoT 0.003 [-0.002, 0.008] 0.001 [-0.001, 0.005] 0.001 [-0.001, 0.004]
 Qwen-7B CoT -0.035 [-0.054, -0.015] -0.030 [-0.069, 0.004] -0.041 [-0.101, 0.007]
 DS-33B Direct 0.147 [0.111, 0.178] -0.024 [-0.056, 0.006] -0.021 [-0.047, 0.005]
 DS-33B CoT -0.032 [-0.054, -0.008] 0.030 [-0.010, 0.065] 0.066 [0.013, 0.121]
 DS-33B Linguistic 0.021 [0.015, 0.027] -0.020 [-0.030, -0.012] -0.019 [-0.030, -0.011]
 DS-6.7B Direct -0.008 [-0.015, -0.003] 0.003 [0.000, 0.008] 0.003 [0.000, 0.008]
 DS-6.7B CoT -0.151 [-0.169, -0.133] -0.020 [-0.053, 0.009] -0.002 [-0.036, 0.029]
 CL-34B Direct -0.029 [-0.042, -0.016] 0.019 [-0.020, 0.048] 0.042 [0.005, 0.077]
 CL-34B CoT -0.179 [-0.200, -0.159] -0.000 [-0.113, 0.110] -0.010 [-0.121, 0.085]
 CL-7B CoT -0.235 [-0.258, -0.213] -0.011 [-0.115, 0.092] 0.013 [-0.158, 0.178]
tied groups. Table 21 compares PRR using saved-
file order within ties with PRR averaged over all
possible orderings within ties.
 350
 Qwen-32B (acc=0.299) Qwen-7B (acc=0.164) DeepSeek-33B (acc=0.189)
 1.0
 0.8
Precision at Coverage Precision at Coverage Precision at Coverage
 0.6
 0.4
 0.2
 0.0
 Coverage Coverage Coverage
 DeepSeek-6.7B (acc=0.142) CodeLlama-34B (acc=0.082) CodeLlama-7B (acc=0.099)
 1.0
 0.8
Precision at Coverage Precision at Coverage Precision at Coverage
 0.6
 0.4
 0.2
 0.0
 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0
 Coverage Coverage Coverage
 Direct CoT Linguistic pass@1 baseline
Figure 10: Accuracy-coverage curves for all 18 cells under strict scoring. Each panel shows one model; the three lines correspond
to elicitation strategies. The horizontal dashed line marks the model’s pass@1 accuracy, which is the expected accuracy at
coverage under random selection. A curve above this line indicates that confidence-ordered selection outperforms random
selection at that coverage.
 Qwen-32B / Direct Qwen-32B / CoT Qwen-32B / Linguistic
 1.0
 0.8 Confidence Score Distributions (all 18 cells, 0-100 scale)
Fraction Correct
 0.6 Direct CoT Linguistic
 0.4
 0.2
 Qwen-32B
 0.0
 Qwen-7B / Direct Qwen-7B / CoT Qwen-7B / Linguistic
 1.0
 0.8
Fraction Correct
 0.6
 0.4
 0.2
 0.0 Qwen-7B
 DeepSeek-33B / Direct DeepSeek-33B / CoT DeepSeek-33B / Linguistic
 1.0
 0.8
Fraction Correct
 0.6
 0.4
 0.2 DS-33B
 0.0
 DeepSeek-6.7B / Direct DeepSeek-6.7B / CoT DeepSeek-6.7B / Linguistic
 1.0
 0.8
Fraction Correct
 0.6
 DS-6.7B
 0.4
 0.2
 0.0
 CodeLlama-34B / Direct CodeLlama-34B / CoT CodeLlama-34B / Linguistic
 1.0
 0.8
Fraction Correct
 0.6
 0.4 CL-34B
 0.2
 0.0
 CodeLlama-7B / Direct CodeLlama-7B / CoT CodeLlama-7B / Linguistic
 1.0
 0.8
Fraction Correct
 0.6
 CL-7B
 0.4
 0.2
 0.0
 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0
 Mean Confidence Mean Confidence Mean Confidence
 Figure 12: Confidence score distributions for all 18 model-
 strategy cells under strict scoring, arranged by model in rows
 Perfect calibration Overconfident region Direct CoT Linguistic
Figure 11: Reliability diagrams for all 18 model-strategy cells (Qwen2.5-Coder-32B, Qwen2.5-Coder-7B, DeepSeek-Coder-
under strict scoring, arranged by model in rows and strategy 33B, DeepSeek-Coder-6.7B, CodeLlama-34B, CodeLlama-
in columns. The dashed diagonal represents perfect calibra- 7B from top to bottom) and strategy in columns (Direct, CoT,
tion. Points below the diagonal indicate overconfidence. Cells Linguistic from left to right). Each panel shows prediction
marked † have collapsed confidence distributions as described counts across 20 equal-width bins on the 0–1 confidence scale.
in Section 4.6.
 351
Table 21: PRR tie sensitivity for the saved repair pipeline. File 1.00 1.00
order keeps equally confident programs in their saved order;
tie-averaged results average over all possible orderings within 0.75 0.75
each equal-confidence group.
 Fraction Correct Fraction Correct
 0.50 0.50
 Model Strategy File order Tie-averaged
 Qwen-32B Direct 0.660 0.633 0.25 0.25
 Qwen-32B CoT 0.544 0.525
 Qwen-32B Linguistic 0.738 0.705 0.00 0.00
 0.00 0.25 0.50 0.75 1.00 0.00 0.25 0.50 0.75 1.00
 Qwen-7B Direct 0.443 0.428 Mean Confidence Mean Confidence
 Qwen-7B CoT 0.395 0.413
 Qwen-7B Linguistic 0.296 0.257 (a) Qwen2.5-Coder-32B, (b) CodeLlama-7B,
 DS-33B Direct 0.464 0.474
 Direct Linguistic†
 DS-33B CoT 0.233 0.239
 DS-33B Linguistic 0.291 0.291 Figure 13: Reliability diagrams for two contrasting cells. The
 DS-6.7B Direct -0.094 0.016 dashed diagonal is perfect calibration; the shaded region marks
 DS-6.7B CoT 0.162 0.257 the overconfident half. Panel (a) spreads across the confidence
 DS-6.7B Linguistic -0.085 -0.003 range and sits mostly below the diagonal. Panel (b) is marked
 CL-34B Direct 0.218 0.310 † for collapse and reduces to isolated points. All 18 diagrams
 CL-34B CoT 0.037 0.160 are in Appendix K.
 CL-34B Linguistic -0.019 0.167
 CL-7B Direct 0.160 0.178
 CL-7B CoT 0.068 0.096 What is the probability (integer 0-100) that
 CL-7B Linguistic -0.111 -0.029 this exact code passes all
 hidden test cases?
 Output EXACTLY one line in the form:
 FINAL_CONFIDENCE: <integer 0-100>
 Do not add any explanation.
 Chain-of-Thought: The system message is:
P Worked Examples of Confidence You are a code correctness assessor. First,
 Elicitation briefly analyse whether the
 submitted code handles edge cases correctly
 and whether the algorithm is
 sound. Then, on the final line, output
 EXACTLY: FINAL_CONFIDENCE:
 <integer 0-100>. Do not write anything after
 that final line.
 Linguistic: The system message identifies the
 model as a code correctness assessor. The fixed
This appendix presents worked examples of ver- instruction is:
balized confidence elicitation drawn from the per-
problem output files. The examples are selected
 How confident are you that this code passes
to illustrate the specific behaviors observed in the all hidden test cases?
results. Output EXACTLY one line in the form:
 FINAL_LABEL: <very low|low|moderate|high|
 very high>
 Do not add any explanation.
Direct: The system message identifies the model
as a code correctness assessor. The fixed instruction
is:
 352
Direct Failure Assigned 100% Confidence Direct Pass Assigned 0% Confidence
Model and outcome: Qwen2.5-Coder-32B, Model and outcome: Qwen2.5-Coder-32B,
Direct, question_id 3708. Parsed confi- Direct, question_id 3832. Parsed confi-
dence: 100. Strict result: fail. dence: 0. Strict result: pass.
Problem excerpt. The model is asked to Problem excerpt. The model is given an
traverse a two-dimensional grid in a zigzag array of swap costs and must return the min-
pattern while skipping every alternate cell. imum total cost required to reach each po-
The traversal begins from the top-left cell, sition in a line. Swapping with a person in
alternates direction between rows, and must front has the listed cost, while later swaps
return the visited values in order. with people behind are free.
Generated code. Generated code.
 from typing import List from typing import List
 class Solution: class Solution:
 def zigzagTraversal(self, grid: def minCosts(self, cost: List[int
 List[List[int]]) -> List[int]: ]) -> List[int]:
 result = [] n = len(cost)
 rows = len(grid) answer = [float('inf')] * n
 cols = len(grid[0]) answer[0] = cost[0]
 for i in range(rows): for i in range(1, n):
 if i % 2 == 0: answer[i] = cost[i]
 # Traverse right for j in range(i):
 for j in range(0, answer[i] = min(
 cols, 2): answer[i], answer[j])
 result.append(
 grid[i][j]) min_cost_so_far = float('inf
 else: ')
 # Traverse left for i in range(n):
 for j in range(cols - min_cost_so_far = min(
 1, -1, -2): min_cost_so_far, cost[i])
 result.append( answer[i] =
 grid[i][j]) min_cost_so_far
 return result return answer
Raw confidence response. Raw confidence response.
 FINAL_CONFIDENCE: 100 FINAL_CONFIDENCE: 0
Interpretation: The model assigns com- Interpretation: The model assigns zero
plete confidence to a program that fails strict confidence to a generated program that
grading. For the available failing test, the passes all strict hidden tests. Together with
expected output is [1, 3, 5, 7, 9] while the previous example, this shows that ex-
the program returns [1, 3, 6, 4, 7, 9]. treme Direct scores can be wrong in both
The row-local stride of two misaligns the directions.
global skip pattern when traversal direction
reverses.
 353
CoT Error on a Passing Program Passing Submission
Model and outcome: Qwen2.5-Coder- Model and outcome: CodeLlama-7B, Lin-
32B, Chain-of-Thought, question_id guistic. This case is 3606. Linguistic label,
abc375_a. Parsed confidence: 0. Strict which maps to confidence 10.
result: pass. Problem excerpt.The model must replace
Problem excerpt. The task is to count pat- each number in an integer array with the
terns of three adjacent seats in which the sum of its digits and return the minimum
two outer seats are occupied and the middle resulting value.
seat is unoccupied. Generated code.
Generated code.
 class Solution:
 # YOUR CODE HERE def minElement(self, nums: List[
 import sys int]) -> int:
 for i in range(len(nums)):
 input = sys.stdin.read().split() nums[i] = sum(int(digit)
 N = int(input[0]) for digit in str(nums[i]))
 S = input[1] return min(nums)
 count = 0
 for i in range(1, N - 1): Raw confidence response.
 if S[i] == '.' and S[i - 1] ==
 '#' and S[i + 1] == '#':
 count += 1 FINAL_LABEL: very low
 print(count)
 Interpretation: The identical label appears
 for a strict failure and a strict pass. Since
Raw confidence response.
 359 of 365 predictions in this cell have con-
 fidence 10, its AUROC of 0.491 reflects
 The submitted code does not correctly solve the problem
 as per the given requirements. The condition to almost no ranking information.
 check should be that seats `i` and `i + 2` are
 occupied (`#`), and seat `i + 1` is unoccupied
 (`.`). However, the code checks if seat `i` is
 unoccupied and seats `i - 1` and `i + 1` are
 occupied, which is incorrect.
 To fix this, the condition inside the loop should be
 changed to:
 ```python
 if S[i - 1] == '#' and S[i] == '.' and S[i + 1] == '#':
 ```
 Additionally, the code handles edge cases correctly by
 iterating from `1` to `N - 2`, ensuring that it
 does not go out of bounds when checking `i + 1`
 and `i - 1`.
 Since the algorithm logic is incorrect, the confidence
 score should reflect that the code does not meet
 the problem's requirements.
 FINAL_CONFIDENCE: 0
Interpretation: The generated program
passes all strict hidden tests. The raw rea-
soning response nevertheless claims that the
condition is wrong, then proposes the same
condition with its terms reordered. This
example makes the failure mode concrete.
A reasoning trace can introduce an incor-
rect self-assessment rather than improve it,
which goes against the expected intuition of
reasoning actually helping an LLM.
 354
Failing Submission
Model and outcome: CodeLlama-7B, Lin-
guistic. This case is 3487. Linguistic label,
which maps to confidence 10.
Problem excerpt. The model must deter-
mine the maximum number of removable
characters from a source string while pre-
serving a given pattern as a subsequence.
Characters may be removed only at the pro-
vided target indices.
Generated code.
 class Solution:
 def maxRemovals(self, source: str, pattern: str,
 targetIndices: List[int]) -> int:
 # Initialize variables
 max_removals = 0
 current_removals = 0
 pattern_index = 0
 source_index = 0
 # Iterate through the target indices
 for target_index in targetIndices:
 # Check if the current character in the
 source string matches the current character in
 the pattern string
 if source[target_index] == pattern[
 pattern_index]:
 # Increment the pattern index
 pattern_index += 1
 # Check if the pattern index has reached
 the end of the pattern string
 if pattern_index == len(pattern):
 # Increment the current removals
 current_removals += 1
 # Reset the pattern index
 pattern_index = 0
 else:
 # Check if the current removals is
 greater than the maximum removals
 if current_removals > max_removals:
 # Update the maximum removals
 max_removals = current_removals
 # Reset the current removals
 current_removals = 0
 # Check if the current removals is greater than
 the maximum removals
 if current_removals > max_removals:
 # Update the maximum removals
 max_removals = current_removals
 # Return the maximum removals
 return max_removals
Raw confidence response.
 FINAL_LABEL: very low
Strict grading evidence. For the available
failing test, the expected output is 1 while
the program returns 0.
 355
