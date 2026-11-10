---
title: Identity or Prompt Noise? A Calibrated Invariance Audit of LLM Code Generation
id: identity-or-prompt-noise-a-calibrated-invariance-audit-of-llm-code-generation
tags:
- code-llm-confidence-positioning-d82d00
- locus-l1-estimator-and-label-oracle-sensitivity-with-contamination-control
created: '2026-11-10T08:40:03.554798Z'
updated: '2026-11-10T09:27:33.581020Z'
source: https://arxiv.org/html/2609.22511
source_domain: arxiv.org
fetched_at: '2026-11-10T08:40:03.554217Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Eren et al. 2609.22511 audit 30.73M executed Python generations under personas;
  occupation is the most consistent structural axis in CodeBLEU dispersion, pass-rate
  dispersion significant in no high-pass cell
---

Identity or Prompt Noise? A Calibrated Invariance Audit of LLM Code Generation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC Zero
arXiv:2609.22511v1 [cs.SE] 18 Sep 2026
Identity or Prompt Noise? A Calibrated Invariance Audit of LLM Code Generation
DOI:
XXXXXXX.XXXXXXX
Journal:
AILET
Volume:
37
4
111
8
CCS:
Computing methodologies Artificial intelligence
CCS:
Social and professional topics Computing / technology policy
Maksim E. Eren
email:
maksim@lanl.gov
Affiliation:
Computational Intelligence & Modeling, LANL
,
Los Alamos
,
NM
,
USA
,
Ryan Barron
email:
barron@lanl.gov
Affiliation:
Computational Intelligence & Modeling, LANL
,
Los Alamos
,
NM
,
USA
,
Eric Michalak
email:
emichalak@lanl.gov
Affiliation:
Advanced Research in Cyber Systems, LANL
,
Los Alamos
,
NM
,
USA
,
Charles Nicholas
email:
nicholas@umbc.edu
Affiliation:
Computer Science and Electrical Engineering, UMBC
,
Baltimore
,
MD
,
USA
and
Manish Bhattarai
email:
ceodspspectrum@lanl.gov
Affiliation:
Theoretical Division, LANL
,
Los Alamos
,
NM
,
USA
2026
Abstract.
Identity cues are irrelevant to a fixed programming specification, but raw counterfactual differences can arise from unequal samples and prompt wording. We audit 30.73 million executed Python generations from seven checkpoints on HumanEval+ and MBPP+, supplemented by an exploratory 550B slice, under model-assigned gender, country, and occupation personas. Within-task randomization and false-discovery-rate control identify occupation as the most consistent structural axis: CodeBLEU dispersion exceeds its exchangeability null in 10/14 model–benchmark cells, remains significant in 8/12 full-coverage cells, and exceeds the country ratio in every paired cell, although the median excess is only 0.141 points. In six high-pass-rate cells, occupation dispersion replicates across token similarity, length, comments, reference similarity, and complexity, while pass-rate dispersion is significant in none. Country leads raw dispersion in 12/14 cells but has a median calibrated ratio of 1.00. Gender-associated variation cannot be separated from persona wording in this design. Thus, the evidence supports small, reproducible occupation-conditioned changes in code form, not stable disadvantage to named identities or demonstrated downstream harm. We use this finding to motivate a broader commentary on the potential impacts of bias in code generation, including the possibility that models may condition their outputs on identity information available from prior conversational context.
Keywords:
code generation, counterfactual invariance, algorithmic bias, prompt sensitivity, randomization inference
1.
Introduction
Functional correctness does not establish that a code generator is invariant to task-irrelevant context. For a fixed programming task, changing a model-assigned gender, country, or occupation persona should alter neither correctness nor implementation form. Yet unequal samples across identity values and innocuous rewording can create raw differences, so an identity effect cannot be inferred from extreme groups or neutral-relative deltas alone. Prior work examines demographic stereotypes in language models
(
Gallegos et al., 2024
;
Sheng et al., 2019
)
, discriminatory logic in socially sensitive programs
(
Liu et al., 2023b
;
Huang et al., 2026
)
, and code sensitivity to personas or prompt reformulation
(
Guo et al., 2025
;
Paleyes et al., 2026
)
. We instead test
irrelevant-identity invariance
: executable tasks remain fixed while the assigned identity persona varies. This separates harmful application logic from an upstream robustness question: whether task-irrelevant identity cues alter outputs for an unchanged programming specification. We therefore evaluate functional correctness and code form separately.
Our contribution is a calibrated audit of 30.73 million executed generations. A within-task randomization test asks whether identity-conditioned dispersion exceeds a label-exchangeability null; false-discovery-rate (FDR) correction, wording controls, a full-coverage cohort, and matched-cell scale comparisons bound the result. Calibration reverses the raw conclusion: country appears most variable before calibration, whereas occupation is the most reproducible structural axis afterward. The effect is small and concerns code form, not demonstrated harm or stable treatment of named occupations.
2.
Experimental Setup and Results
2.1.
Design and Estimand
We test counterfactual invariance: holding task and generation settings fixed, does varying a task-irrelevant assigned persona alter correctness or implementation form? Our estimand is across-identity dispersion in task-centered outcomes beyond that induced by sample allocation; it tests axis-level non-exchangeability, not benefit, harm, or causality for named identities.
HumanEval+ (164 tasks) and MBPP+ (378 tasks) provide augmented functional tests
(
Chen et al., 2021
;
Austin et al., 2021
;
Liu et al., 2023a
)
. Fixed tasks are paired with 20 gender labels, 112 countries
(
Haerpfer et al., 2022
)
, 234 occupations, and ten generic persona-noun controls. Every exact prompt is decoded once; identities recur across tasks. The main archive contains 30,728,903 generations from seven checkpoints (Llama-3.2-3B, Mistral-7B, Llama-3-8B, Nemotron-3-Nano-30B, Gemma-4-31B, gpt-oss-120B, and Nemotron-3-Super-120B)
(
Dubey et al., 2024
;
Jiang et al., 2023
;
NVIDIA, 2025
;
Gemma Team, 2026
;
OpenAI, 2025
;
NVIDIA, 2026
)
. Gemma-4-31B has incomplete coverage; an additional 260,000-row Ultra-550B HumanEval+ occupation slice is exploratory. We infer within model, benchmark, and axis, repeat the analysis on six full-coverage models, and match cells for scale comparisons.
Generation settings are fixed within runs (temperature 0.2, top-
p
p
0.95, and at most 2,048 new tokens). Parseable programs are sandboxed and checked against EvalPlus tests. EvalPlus pass rate is the functional primary outcome. CodeBLEU, which combines lexical, syntactic, and data-flow similarity
(
Ren et al., 2020
)
, is the structural primary outcome; it measures similarity to a reference, not code quality or benefit. Five additional structure metrics are exploratory.
For each model–benchmark–axis cell, we center outcomes within task and compute the standard deviation
σ
^
obs
\widehat{\sigma}_{\mathrm{obs}}
of identity-level means. We then shuffle outcomes within task 1,000 times, preserving tasks, sample sizes, and outcome distributions while breaking identity association. We report the observed-to-null ratio, one-sided randomization
p
p
-value, and excess dispersion
σ
^
excess
=
max
⁡
(
0
,
σ
^
obs
2
−
σ
^
null
2
)
.
\widehat{\sigma}_{\mathrm{excess}}=\sqrt{\max(0,\widehat{\sigma}_{\mathrm{obs}}^{2}-\widehat{\sigma}_{\mathrm{null}}^{2})}.
This is a label-exchangeability null, not an exact-prompt decoding baseline. Benjamini–Hochberg correction at
q
<
0.05
q<0.05
is applied separately to 42 CodeBLEU and 42 pass-rate tests (seven models, two benchmarks, three axes), then recomputed over 36 tests for the full-coverage cohort. Neutral persona-noun and within-gender noun controls form separate corrected families.
2.2.
Results
Table
1
gives the confirmatory result. Occupation CodeBLEU dispersion survives correction in 10/14 main cells and 8/12 full-coverage cells; its ratio exceeds one in all 14 and exceeds country in every paired cell. Country nevertheless has the largest
raw
spread in 12/14 cells because it has fewer observations per value. After calibration its median ratio is 1.00. Thus calibration changes which axis appears dominant, not merely its reported magnitude. Functional discoveries are less consistent, and median pass-rate excess is at most 0.315 percentage points. Given the corpus size, we interpret significance together with absolute excess.
Table 1.
Calibrated dispersion. FDR counts BH-significant cells; ratios and CodeBLEU excess are main-cohort medians. “Raw lead” counts the largest uncalibrated CodeBLEU spread.
CodeBLEU
Pass
Axis
Main FDR
Full FDR
Ratio/Excess
Main FDR
Full FDR
Raw lead
Occupation
10/14
8/12
1.29 / 0.141
6/14
4/12
1/14
Gender
7/14
7/12
1.35 / 0.095
6/14
4/12
1/14
Country
2/14
1/12
1.00 / 0.021
1/14
1/12
12/14
Figure
1
shows every main-checkpoint CodeBLEU cell. Occupation replicates on both benchmarks for five of seven checkpoints, compared with three for gender and none for country. The two country discoveries are isolated rather than cross-benchmark effects.
Wording controls constrain the gender interpretation. Neutral persona nouns are significant in 2/14 CodeBLEU cells and 0/14 pass cells. Regrouping gender-only rows by persona noun yields 6/14 CodeBLEU and 4/14 pass discoveries, similar to gender’s 7/14 and 6/14; paired ratios do not differ (
p
=
0.358
p=0.358
, exploratory). Thus demographic meaning is not isolated from wording.
Figure 1.
Observed-to-null CodeBLEU dispersion across identity axes. Asterisks denote BH-adjusted
q
<
0.05
q<0.05
; Gemma-4-31B results reflect incomplete coverage.
Five exploratory structure metrics are corrected jointly across nine available model–benchmark cells (45 tests). Table
2
summarizes the six complete cells: token BLEU, lines, and comments are significant in all six, and reference similarity and complexity in five; pass rate, corrected in its separate primary family, is significant in none. The effects are consistent but small.
Table 2.
Occupation sensitivity in six full, high-pass-rate cells.
Metric
FDR cells
Median ratio
Median excess
Reference similarity
5/6
1.916
0.578 points
Token BLEU
6/6
1.620
0.403 points
Lines of code
6/6
1.823
0.189 lines
Comment lines
6/6
1.369
0.021 lines
Complexity
5/6
1.108
0.011 units
EvalPlus pass
0/6
1.041
0.140 points
On 15,312 cells shared by all eight archived checkpoints, parameter count correlates with pass rate (Spearman
ρ
=
0.922
\rho=0.922
,
p
=
0.001
p=0.001
) but not with lower occupation spread (
ρ
=
0.431
\rho=0.431
,
p
=
0.286
p=0.286
). The exploratory Ultra-550B slice likewise has calibrated occupation CodeBLEU sensitivity (ratio 1.305,
p
=
0.001
p=0.001
) but null pass sensitivity (ratio 1.020,
p
=
0.349
p=0.349
). However, occupation rankings are unstable across checkpoints (median pairwise Spearman
ρ
=
0.067
\rho=0.067
). Scale therefore does not guarantee invariance, but the data do not support stable favoritism toward named occupations or a causal scaling law.
3.
Discussion and Limitations
The defensible finding is narrow: task-irrelevant occupation personas predict small changes in implementation form across models, benchmarks, and independent metrics, while correctness is more stable. This is
bias
only as identity-conditioned non-invariance. Reference similarity is not inherently beneficial, personas are model assignments rather than observed users, and we do not measure security, validated maintainability, developer effort, or social harm.
This distinction matters for evaluation. An accuracy-only audit misses structural sensitivity, while an uncalibrated audit selects country as the dominant axis in 12/14 cells even though its calibrated ratio is nearly null. The proposed test supplies a release-time statistic on fixed executable tasks and distinguishes robust axis-level dispersion from noisy identity extremes; the same calibration applies to other irrelevant contextual cues. The near-equivalence of gender and wording discoveries also exposes a confound that neutral-baseline comparisons alone do not resolve.
The archive permits two downstream-adjacent checks. Maintainability proxies show reproducible but minute occupation effects (median excess: 0.189 lines, 0.021 comment lines, and 0.011 complexity units), not validated maintainability outcomes. In a separate exploratory family of 30 tests over the same six high-pass cells, failures under augmented tests and timeouts are significant in 0/6 cells each, harness execution time in 1/6, and execution failures and imports in 3/6 each. Corresponding median excesses are only 2.98 ms, 0.134 percentage points, and 0.002 imports; wall time is not controlled algorithmic efficiency, and imports are not security findings.
Occupation pass dispersion is significant in 6/14 main cells, but all six discoveries occur in Mistral-7B, Llama-3-8B, or Gemma-4-31B, and none occurs in the six full high-pass cells. Across 234 occupations and 12 full model–benchmark cells, task-normalized pass rankings have median pairwise Spearman
ρ
=
0.001
\rho=0.001
(range
−
0.231
-0.231
to
0.462
0.462
), and no occupation remains in the bottom quartile in at least 9/12 cells. This argues against stable correctness disadvantage in the present benchmarks, not against discrimination generally.
Three limitations bound interpretation. First, the permutation test estimates label exchangeability within task, not stochastic variation from repeated decoding of the exact prompt. Existing persona nouns are only partially crossed with occupations; a retrospective held-out-task decomposition cannot establish a semantic identity effect because wording-only prediction is near zero and occupation-only prediction is negative. A causal test requires identities fully crossed with paraphrases and repeated decodes. Second, Gemma-4-31B and Ultra-550B have incomplete coverage; central results are also reported for a full-coverage cohort, and Ultra-550B supports only an exploratory occupation claim. Third, the five-metric and consequence-proxy analyses were conducted after the primary CodeBLEU finding and remain exploratory despite conservative correction. Coverage imbalance, model-family confounding, small absolute effects, and unstable occupation rankings further preclude claims about named groups or practical harm.
In summary, these results ask three simple questions: do identity labels change the generated code more than we would expect from sampling alone, does that pattern repeat across models and benchmarks, and is the difference large enough to matter? Calibration helps separate apparent differences from reproducible ones. After calibration, occupation shows a small but reproducible difference in how code is written, while most country differences largely disappear and gender effects cannot yet be separated from persona wording. Importantly, this should not be read as evidence that particular occupations are consistently favored or harmed: the affected occupations are not stable across models, and the differences do not consistently change whether the code passes its tests. Existing proxies show no consistent downstream penalty, and the present results do not establish effects in conversational or educational settings. Still, even small identity-conditioned differences in code form could matter if they affect properties not measured here, such as maintainability, security, or behavior over longer interactions. This may be especially relevant in conversational systems, where identity information disclosed or inferred earlier in a chat—or retained through conversational memory—could become part of the context used for later code-generation requests even when that information is irrelevant to the programming task. We therefore use these findings to motivate a broader commentary on potential robustness risks, including possible implications for education, where such variation could influence the examples, explanations, or programming support different learners receive. We do not interpret the present results as evidence of demonstrated downstream harm. Future work should test repeated exact prompts, fully crossed paraphrases, longer conversational contexts, and downstream outcomes in settings such as software security, maintenance, and education to determine when these differences become consequential.
Acknowledgments
Approved for unlimited release LA-UR-26-27647. This work was funded by Los Alamos National Laboratory, operated by Triad National Security, LLC, for the National Nuclear Security Administration of the U.S. Department of Energy (Contract No. 89233218CNA000001).
References
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton
Program synthesis with large language models
.
arXiv preprint arXiv:2108.07732
.
Cited by:
§2.1
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
et al.
Evaluating large language models trained on code
.
arXiv preprint arXiv:2107.03374
.
Cited by:
§2.1
.
Dubey
et al.
(2024)
A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle,
et al.
The llama 3 herd of models
.
arXiv preprint arXiv:2407.21783
.
Cited by:
§2.1
.
Gallegos
et al.
(2024)
I. O. Gallegos, R. A. Rossi, J. Barrow, M. M. Tanjim, S. Kim, F. Dernoncourt, T. Yu, R. Zhang, and N. K. Ahmed
Bias and fairness in large language models: a survey
.
Computational Linguistics
50
(
3
),
pp. 1097–1179
.
External Links:
Document
,
Link
Cited by:
§1
.
Gemma Team (2026)
Gemma Team
Gemma 4 Technical Report
.
arXiv preprint arXiv:2607.02770
.
External Links:
2607.02770
,
Link
Cited by:
§2.1
.
Guo
et al.
(2025)
Y. Guo, Z. Chen, J. M. Zhang, Y. Liu, and Y. Ma
Personality-guided code generation using large language models
.
In
Proceedings of the 63rd Annual Meeting of the Association
for Computational Linguistics
(Volume 1: Long Papers)
,
Vienna, Austria
,
pp. 1068–1080
.
External Links:
ISBN 979-8-89176-251-0
,
Document
,
Link
Cited by:
§1
.
Haerpfer
et al.
(2022)
C. Haerpfer, R. Inglehart, A. Moreno, C. Welzel, K. Kizilova, J. Diez-Medrano, M. Lagos, P. Norris, E. Ponarin, and B. Puranen
World values survey: round seven – country-pooled datafile
.
Note:
JD Systems Institute & WVSA Secretariat, Madrid & ViennaVersion 4.0
Cited by:
§2.1
.
Huang
et al.
(2026)
D. Huang, J. M. Zhang, Q. Bu, X. Xie, J. Chen, and H. Cui
Bias testing and mitigation in LLM-based code generation
.
ACM Transactions on Software Engineering and Methodology
35
(
1
),
pp. 5:1–5:31
.
External Links:
Document
,
Link
Cited by:
§1
.
Jiang
et al.
(2023)
A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford, D. S. Chaplot, D. de las Casas,
et al.
Mistral 7B
.
arXiv preprint arXiv:2310.06825
.
Cited by:
§2.1
.
Liu
et al.
(2023a)
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
Is your code generated by ChatGPT really correct? rigorous evaluation of large language models for code generation
.
In
Advances in Neural Information Processing Systems (NeurIPS)
,
Vol.
36
.
Cited by:
§2.1
.
Liu
et al.
(2023b)
Y. Liu, X. Chen, Y. Gao, Z. Su, F. Zhang, D. Zan, J. Lou, P. Chen, and T. Ho
Uncovering and quantifying social biases in code generation
.
In
Advances in Neural Information Processing Systems
,
Vol.
36
,
pp. 2368–2380
.
External Links:
Link
Cited by:
§1
.
NVIDIA (2025)
NVIDIA
NVIDIA-Nemotron-3-Nano-30B-A3B-BF16 model card
.
Note:
https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16
Accessed 2026-07-13
Cited by:
§2.1
.
NVIDIA (2026)
NVIDIA
NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4 model card
.
Note:
https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4
Accessed 2026-07-13
Cited by:
§2.1
.
OpenAI (2025)
OpenAI
Gpt-oss-120b & gpt-oss-20b model card
.
arXiv preprint arXiv:2508.10925
.
Cited by:
§2.1
.
Paleyes
et al.
(2026)
A. Paleyes, R. Sendyka, D. Robinson, C. Cabrera, and N. D. Lawrence
Code roulette: how prompt variability affects LLM code generation
.
In
Proceedings of the 3rd International Workshop on
Large Language Models for Code
,
LLM4Code ’26
,
New York, NY, USA
.
External Links:
ISBN 979-8-4007-2412-1
,
Document
,
Link
Cited by:
§1
.
Ren
et al.
(2020)
S. Ren, D. Guo, S. Lu, L. Zhou, S. Liu, D. Tang, N. Sundaresan, M. Zhou, A. Blanco, and S. Ma
CodeBLEU: a method for automatic evaluation of code synthesis
.
arXiv preprint arXiv:2009.10297
.
Cited by:
§2.1
.
Sheng
et al.
(2019)
E. Sheng, K. Chang, P. Natarajan, and N. Peng
The woman worked as a babysitter: on biases in language generation
.
In
Proceedings of the 2019 Conference on Empirical Methods
in Natural Language Processing and the 9th International
Joint Conference on Natural Language Processing
(EMNLP-IJCNLP)
,
Hong Kong, China
,
pp. 3407–3412
.
External Links:
Document
,
Link
Cited by:
§1
.