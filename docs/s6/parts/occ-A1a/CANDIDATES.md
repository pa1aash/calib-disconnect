# A1a: decomposition-occupancy search, arXiv full text (search.arxiv.org)

Run date: 2026-11-10. Tool: `research/positioning/w5/parts/ft-A4a/raw/axft_search.py` (tag, quoted query of 64 characters or fewer, outdir, maxresults 100). Raw search pages and parsed JSON: `raw/Qnn_p*.html`, `raw/Qnn.json`. Full texts: `raw/ft/<id>.html` (arxiv.org/html, headless curl, desktop user agent) with a tag-stripped `raw/ft/<id>.txt`. Hosts used: search.arxiv.org and arxiv.org only. All HTTP responses were 200. No PDF fallback was needed.

Rules applied (INSTRUMENTS.md, section 6): quoted exact phrases; a zero or an absence counts only when the reported total is under 150 and every page up to that total was read; there is a second phrasing per concept. The "read" column counts parsed hit records. It can exceed the total by one or two when a snippet holds a reference-list URL. Queries with totals of 150 or more (Q04, Q05, Q07, Q09, Q12, Q13, Q28, Q38) were capped at 100 hits read. They are used only as lead sources, not as evidence of absence. Q24, Q47, and Q49 had totals between 100 and 150 with 100 read, so they are partial.

## Query log

| Tag | Query | Total | Read | HTTP | Usable for absence |
|---|---|---|---|---|---|
| Q01 | `"internal and expressed confidence"` | 4 | 4 | 200 (1 pages) | yes |
| Q02 | `"internal confidence and verbalized confidence"` | 2 | 2 | 200 (1 pages) | yes |
| Q03 | `"knowing more than it says"` | 0 | 0 | 200 (1 pages) | yes |
| Q04 | `"know more than they show"` | 201 | 103 | 200 (10 pages) | no (total>=150) |
| Q05 | `"verbalized confidence" "probe"` | 201 | 100 | 200 (10 pages) | no (total>=150) |
| Q06 | `"decompose the calibration gap"` | 0 | 0 | 200 (1 pages) | yes |
| Q07 | `"attribute the gap"` | 211 | 100 | 200 (10 pages) | no (total>=150) |
| Q08 | `"disconnect between internal"` | 16 | 16 | 200 (2 pages) | yes |
| Q09 | `"hidden knowledge" confidence` | 200 | 100 | 200 (10 pages) | no (total>=150) |
| Q10 | `"within-question" AUROC` | 43 | 43 | 200 (5 pages) | yes |
| Q11 | `"difficulty confound"` | 27 | 27 | 200 (3 pages) | yes |
| Q12 | `"Shapley" calibration confidence` | 270 | 100 | 200 (10 pages) | no (total>=150) |
| Q13 | `"label noise" calibration probe` | 209 | 100 | 200 (10 pages) | no (total>=150) |
| Q14 | `"sources of miscalibration"` | 20 | 20 | 200 (2 pages) | yes |
| Q15 | `"calibration gap" "hidden states"` | 44 | 44 | 200 (5 pages) | yes |
| Q16 | `"internal confidence" "stated confidence"` | 25 | 25 | 200 (3 pages) | yes |
| Q17 | `"probe" "verbalized" "token probability" calibration` | 97 | 97 | 200 (10 pages) | yes |
| Q18 | `"knowing-saying gap"` | 2 | 3 | 200 (1 pages) | yes |
| Q19 | `"probe-verbal gap"` | 1 | 1 | 200 (1 pages) | yes |
| Q20 | `"stated versus internal"` | 3 | 3 | 200 (1 pages) | yes |
| Q21 | `"internal and verbalized confidence"` | 7 | 7 | 200 (1 pages) | yes |
| Q22 | `"verbalized and internal"` | 16 | 16 | 200 (2 pages) | yes |
| Q23 | `"gap between probe and verbalized"` | 0 | 0 | 200 (1 pages) | yes |
| Q24 | `"decompose the gap"` | 136 | 100 | 200 (10 pages) | partial (100 of 136 read) |
| Q25 | `"decomposition of the gap" confidence` | 90 | 90 | 200 (9 pages) | yes |
| Q26 | `"confidence gap" "probe" "verbalized"` | 18 | 18 | 200 (2 pages) | yes |
| Q27 | `"within-problem" AUROC` | 21 | 21 | 200 (3 pages) | yes |
| Q28 | `"prompt-only" probe correctness` | 208 | 100 | 200 (10 pages) | no (total>=150) |
| Q29 | `"difficulty baseline" probe` | 27 | 27 | 200 (3 pages) | yes |
| Q30 | `"test-suite strength" calibration` | 2 | 2 | 200 (1 pages) | yes |
| Q31 | `"noisy labels" "verbalized confidence"` | 15 | 15 | 200 (2 pages) | yes |
| Q32 | `"frozen generations" probe` | 4 | 4 | 200 (1 pages) | yes |
| Q33 | `"own generations" "verbalized confidence"` | 36 | 37 | 200 (4 pages) | yes |
| Q34 | `"zero-shot" "recalibrated" "trained probe"` | 5 | 5 | 200 (1 pages) | yes |
| Q35 | `"calibration decomposition"` | 31 | 31 | 200 (4 pages) | yes |
| Q36 | `"behavior-concealed knowledge"` | 2 | 3 | 200 (1 pages) | yes |
| Q37 | `"linguistic and internal confidence"` | 5 | 5 | 200 (1 pages) | yes |
| Q38 | `"internal-external" confidence gap` | 209 | 100 | 200 (10 pages) | no (total>=150) |
| Q39 | `"expressed confidence" "hidden states" gap` | 35 | 35 | 200 (4 pages) | yes |
| Q40 | `"nearly orthogonal" "verbalized confidence"` | 8 | 8 | 200 (1 pages) | yes |
| Q41 | `"knowledge-expression gap"` | 0 | 0 | 200 (1 pages) | yes |
| Q42 | `"internal-external gap"` | 5 | 5 | 200 (1 pages) | yes |
| Q43 | `"pooled AUROC" "verbalized confidence"` | 6 | 6 | 200 (1 pages) | yes |
| Q44 | `"pooled AUROC" probe difficulty` | 34 | 34 | 200 (4 pages) | yes |
| Q45 | `"self-reported confidence" "hidden states"` | 58 | 58 | 200 (6 pages) | yes |
| Q46 | `"verbalized confidence" "unit tests" probe` | 22 | 22 | 200 (3 pages) | yes |
| Q47 | `"test suite" "label noise" confidence` | 102 | 100 | 200 (10 pages) | partial (100 of 102 read) |
| Q48 | `"weak test" calibration code` | 87 | 88 | 200 (9 pages) | yes |
| Q49 | `"stated confidence" probe code correctness` | 113 | 100 | 200 (10 pages) | partial (100 of 113 read) |
| Q50 | `"what a model says" "what it knows" confidence` | 9 | 9 | 200 (1 pages) | yes |

## Candidate table

Term codes:
- S: supervision (zero-shot vs. recalibrated vs. trained readout).
- D: difficulty (pooled vs. within-question scoring, or a prompt-only or question-only baseline).
- L: label validity (test-suite strength, noisy or audited labels).
- G: generation shift (a readout scored on its own generations vs. on frozen generations).

"Shared generations" means the compared readouts are scored on the same outputs. Section cites use the paper's own headings, as they appear in `raw/ft/<id>.txt`. Dates are the arXiv id month. None of these candidates is in the known list. Where a candidate appears in earlier project records, the Notes column says so.

| id | Title (short) | Date | Gap studied | Terms varied | Shared generations | Text basis | Section cites | Notes |
|---|---|---|---|---|---|---|---|---|
| 2609.04582 | When Do Internal Probes Beat Reading the Answer? Miscalibrated Readouts and Behavior-Concealed Knowledge | 2026-09 | Probe vs. the expressed YES/NO answer, with the model's own logit margin as an intermediate rung ("ladder": behavior, margin, probe). Not stated or verbalized confidence. | S yes: a zero-shot answer, a one-parameter bias calibration fit leave-one-structure-out, few-shot recentering, and a trained probe, compared on paired trials. The paper splits the gap into a threshold-offset part and a residual "concealment" part. D yes, but only in the separate generation-setting audit: a 4-feature difficulty baseline at the pre-answer position beats every hidden-state probe under transfer. L yes, also only in that audit: heuristic keyword labels vs. adjudicated labels change which predictors work. G no. | y for the verification ladder (the same trials, paired margins zero-shot vs. few-shot). The D and L controls are a different design (open generation); they are not applied to the ladder. | FULL TEXT | Abstract; "Knowledge, Expression, and a Diagnostic" (Prop. 1, Prop. 2); "Repair, Elicitation, and the Diagnostic" (Table 3; "One parameter, cross-validated"; "Few-shot prompting predominantly recenters the threshold"; "The residual gap"); "Generation: Why the Controls Matter" (Table 4); "Discussion: For evaluation" | Closest occupant found. It decomposes an internal-vs-expressed gap, but the expressed side is the answer, not a confidence statement. The decomposition is mainly S (threshold vs. ranking). It cites Gekhman et al. (2025) and Park et al. (2025) as the prior gap work. New to the project. |
| 2610.25846 | Measurement Validity and Representation Dynamics of Confidence Signals in LLMs | 2026-10 | Three channels: verbalized confidence, a prefill-state probe (predicting sampled-answer disagreement), and semantic entropy, on the same 30-cell grid (5 Qwen2.5 models). | D yes: a prompt-only TF-IDF baseline matches the probe in most retrieval cells and is a pass gate. L partial: a pre-registered human grading-validity gate (an audit, not a varied term). Calibration vs. resolution via a Murphy decomposition of Brier. S no, G no. | y (the same items and splits) | FULL TEXT | Abstract; §3.2; §3.3 (Gate 1); §4.1; §5 (prompt-format instability); §6 (Murphy decomposition) | A measurement-validity audit. It does not attribute the probe-vs-verbal gap to terms. Cites Mahaut et al. 2024 as the closest prior work, and DECK 2606.02289. Already in the project vault (research/temp). |
| 2609.33290 | Calibration, Not Answer Selection: Distilling Internal Confidence in Reasoning Models | 2026-09 | Probe vs. verbalized score on the same sampled traces (Qwen3-14B, Ministral-3-8B). | S partial: raw verbalized vs. post-hoc recalibration (temperature, isotonic; argued not to transfer) vs. a trained probe, and a probe-distilled verbalized score. D, L, and G no. | y ("on the same sampled traces", §3.1) | FULL TEXT | Abstract; §1 contributions; §3.1 (Table 1); §3.3; §5.2 | Compares readouts and gives a mechanism claim (verbal confidence tracks commitment). No decomposition. |
| 2608.28382 | When Linguistic and Internal Confidence Diverge in LLMs | 2026-08 | Linguistic confidence vs. logits-based confidence (semantic entropy for generation); 30 models, 10 tasks. | D partial, at task level only: association vs. chance-corrected task accuracy; not within-question. A regression attributes cross-channel alignment to distributional properties, model properties (instruction tuning), and prompts. S, L, and G no. | y | FULL TEXT | Abstract; §5.2; §5.3; §5.5; §6.1 (regression); §6.2 | It attributes cross-channel agreement, not a correctness-prediction gap. Its factors are not the four terms. Earlier only a raw search hit in w4/w5. |
| 2610.27455 | Detecting Errors in LLM Responses: The Incremental Predictive Value of Hidden States | 2026-10 | Hidden-state gain over a stacked output-side baseline. The baseline blocks include token scores, cross-sample consistency, "explicit confidence", and prompt context. | Partial attribution by block: removing generation and sampling signals inflates the hidden-state gain (§5.2). The prompt-context block is a prompt-only input inside the baseline. Grouping sensitivity is examined (§4.4). It does not vary S as defined, and there is no L or G. | y (identical splits and outputs) | FULL TEXT | Abstract; §3.1; §3.2 ("Information blocks", Table 2); §3.3; §4.4; §5.1 (Table 3); §5.2 | It attributes the probe advantage to output-side information blocks. The explicit-confidence block is not isolated as its own gap. |
| 2607.22034 | Small VLMs Know When They Are Wrong But Cannot Say So (stated vs. internal) | 2026-07 | Verbalized confidence vs. mean token probability on the same 3,800 predictions (2 VLMs, image degradations). | S partial: single-signal temperature scaling (§4.7). Degradation severity is varied (input shift, not G as defined). D, L, and G no. | y ("on the very same predictions", §4.6) | FULL TEXT | Abstract; §3.4; §4.2; §4.3; §4.6; §4.7; §5.1 | A comparison only. |
| 2608.07528 | The Knowing-Saying Gap: When Probes See Errors that Confidence Misses | 2026-08 | Probe corruption detection vs. failure prediction, vs. structured verbalized confidence and six surface signals. | D partial: a final_degraded target "to isolate propagation from baseline difficulty" (matched clean vs. corrupted). S, L, and G no. | y (the same traces) | FULL TEXT | Abstract; §1 "This paper"; §4.5; §4.7; §5 | Earlier only a raw hit in w5 ft-A4b. |
| 2610.35694 | Not One Belief: Answer Payloads, Persistence, and Dissociated Confidence Signals | 2026-10 | Verbalized confidence, sequence likelihood, a frozen first-turn probe, and P(True) on the same multi-turn transcripts. | Attribution is to parts of the user turn (speech act vs. payload), not to the four terms. D partial: held-out-question rescoring and a shuffled-label control. L partial: cleaned answers for Llama-3-8B, and model-read labels in a sensitivity check. S and G no. | y ("On the same transcripts") | FULL TEXT | Abstract; §2; §3.3; §3.4; §5; §6 ("Held-out questions") | Points to Miao and Ungar 2603.25052 (an accuracy probe vs. the verbal-confidence direction, near orthogonal; SNIPPET ONLY here) and Kumaran 2606.29490 (reported confidence tracks commitment; NOT FETCHED). |
| 2609.20541 | An Analysis of Training-Free Self-Reported Confidence in LMs | 2026-09 | Verbalized confidence vs. post-hoc P(True) vs. agreement among 3 extra samples, on the same 100 TriviaQA questions. There is no hidden-state probe. | L yes: auditing benchmark errors changes the conclusion (§5.5). Re-eliciting confidence for fixed answers under equivalent prompts (§5.3) is a frozen-answer re-scoring of the stated readout, close to G. S and D no. | y | FULL TEXT | Abstract; §3.2; §5.1; §5.3; §5.5 | There is no internal probe, so it is outside the probe-vs-stated case. It is relevant to the L and G terms. |
| 2608.08791 | Unsure but Certain: The Representation-Confidence Gap in Diffusion LMs | 2026-08 | A hidden-state readout vs. the model's output certainty under input noise. | S partial: score recalibration removes the concentration of high scores but not the ranking deficit; matched training is tested as well. D, L, and G no. | y | FULL TEXT | Abstract; "Results"; appendix "The gain requires the hidden state" | The output-certainty side is model confidence, not verbalized confidence (the text has no "verbal" string). |
| 2606.29034 | Strength of clinical evidence is recoverable from LM representations but not from their stated grades | 2026-06 | A linear estimator vs. the stated evidence grade (22 LLMs). | Lexical, truth, and cross-framework controls (a lexical control is close to a prompt-only D control). S, L, and G no. The target is evidence strength, not self-correctness. | y | FULL TEXT | Abstract; Introduction | An analogue, not occupancy. |
| 2610.00827 | Verbalized and Internal Probabilities Are Coupled in LLMs | 2026-10 | The alignment of verbalized and internal probability readouts. | Training-data interventions (frequency-based vs. asserted uncertainty). None of S, D, L, or G. | y | FULL TEXT | Abstract; §3.2; §6.1; §6.2 | Mechanism, not decomposition. |
| 2503.15299 | Inside-Out: Hidden Factual Knowledge in LLMs (Gekhman et al.) | 2025-03 | Internal (hidden-state scorer) vs. external (token-probability) knowledge: the per-question pairwise ranking of correct vs. incorrect candidates. | D is handled by the definition: scoring is within-question. S, L, and G are not varied. The external side is token probability, not verbalized confidence. | y (the same candidate sets) | FULL TEXT | Abstract; §2.1 (Def. 1); §2.2 (Def. 2); §4.1 | General-domain hidden-knowledge line. It quantifies the gap and does not decompose it. |
| 2410.02707 | LLMs Know More Than They Show (Orgad et al.) | 2024-10 | Probe-detected correct answers vs. the generated answer. | None of S, D, L, or G as a decomposition. | y | FULL TEXT | Abstract; §6 "Detecting the Correct Answer" | General-domain line. A discrepancy is shown and not decomposed. |
| 2406.13415 | Factual Confidence of LLMs (Mahaut et al., ACL 2024) | 2024-06 | Trained probes, sequence probability, verbalization, surrogate token probability, and consistency in one framework. | None as a decomposition. There is paraphrase and translation robustness. | y | FULL TEXT | Abstract; §3; §4; §5 | A comparison only. |
| 2605.02241 | Zero-Shot Confidence Estimation for Small LLMs: When Supervised Baselines Aren't Worth Training | 2026-05 | Zero-shot token log-probability vs. RouteLLM-style supervised query-only routers. | S yes (zero-shot vs. supervised), and the supervised routers are prompt-only (D-like). No probe and no verbalized confidence. L and G no. | y | FULL TEXT | Abstract; §II-A; §II-B; §IV-C; §V-B | Relevant to S and D only. |
| 2609.36461 | Rethinking Reasoning Paths as Phase-Structured Trajectories (PAIR) | 2026-09 | Across-question vs. within-question correctness probes. | D yes (within-question evaluation shrinks probe power). S, L, and G no. No stated confidence. | y (multiple trajectories per question) | FULL TEXT (abstract read; body not screened) | Abstract | Difficulty term only. New to the project. |
| 2610.05572 | Disentangling Task Difficulty from Run-Level Failure in Agent Failure Prediction | 2026-10 | Pooled vs. within-task AUROC for agent failure predictors. | D yes. Others no. | y | FULL TEXT (abstract read) | Abstract | Already in the project vault. Difficulty only. |
| 2610.07354 | Evaluating Escalation Signals for LLM Routing: Targets, Controls, and Five Ways to Fool Yourself | 2026-10 | Semantic entropy vs. a question-only difficulty baseline. Two definitions of the escalation target. | D yes. Label or target definition is varied (L-like). S and G no. No probe. | y | FULL TEXT | Abstract; §3.6; §6.6 | Difficulty and target validity, not probe vs. stated. |
| 2606.14530 | Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation | 2026-06 | A pre-generation probe vs. a prompt-length baseline (LiveCodeBench). | D partial (prompt-length residualization). Others no. | n/a (pre-generation) | FULL TEXT (abstract read) | Abstract | Already in the project (W4). |
| 2608.08266 | On the Robustness of LLMs' Internal Representation of Code Correctness | 2026-08 | Probe configuration sweep; fault-isolated mutant pairs. | Varies extraction design. Mutant pairs control program differences. L is mentioned for the prior LLM-injected pairs ("residual label noise"). It does not decompose the probe-vs-stated gap; it restates Ribeiro's result that the probe beats token and stated confidence. | y | FULL TEXT | Abstract; §I; §III-D; §V | Already in the project (W3, W4). Its ref [11] is Ribeiro (known, 2512.07404). |

Leads seen in snippets and not fetched (ABSTRACT-ONLY or SNIPPET ONLY; not used for the verdict):
- 2603.25052: Miao and Ungar, accuracy probe vs. verbal-confidence direction, steering.
- 2606.29490: Kumaran, reported confidence tracks commitment.
- 2604.22271: Kumaran et al., internal confidence signals in error correction.
- 2605.27752: protocol sensitivity of confidence.
- 2610.27566: learned readout tokens.
- 2611.04834: feeling of knowing.
- 2606.32032: RL with metacognitive feedback, faithful expression.
- 2512.11998: Direct Confidence Alignment.
- 2405.16282: Kumar et al., confidence-probability alignment.
- 2607.08046: forecaster probes vs. verbalized confidence. Fetched; only the abstract and headings were read.
- 2604.17714: validity screening of confidence signals. Fetched; the abstract was read; it is a contingency-table decomposition, not probe vs. stated.
- 2603.18893: numeric self-reports vs. probes for affective states. Fetched; abstract read; already in the project from W5.

Known items surfaced by these queries (not re-reported as new):
- 2610.31820: Q05, Q49.
- 2611.07876: Q04, Q27, Q44.

## Verdict

**No.** None of the 21 full-text candidates in the table (30 full texts fetched in all) decomposes, attributes, or audits the gap between a probe (or token probability) and stated confidence. No paper splits that gap into several of supervision, difficulty, label validity, and generation shift on shared generations.

The nearest occupant is 2609.04582. On shared trials it splits a probe-vs-expressed-answer gap into a threshold or recalibration (S) part and a residual concealment part. The expressed side is the binary answer, not verbalized confidence. Its D and L controls sit in a separate open-generation audit and are not applied to that decomposition. It also has no G term.

Other papers cover single terms on shared generations:
- S partial: 2609.33290, 2607.22034, 2608.08791.
- D: 2610.25846, 2609.36461, 2610.05572, 2610.07354.
- L: 2609.20541, and 2610.25846 as a gate.
- Close to G: 2609.20541, which re-elicits confidence on fixed answers.

**Instrument caveat.** Absence rests on these queries, which had totals under 150 with every page read: Q01-Q03, Q06, Q08, Q10, Q11, Q14-Q23, Q25-Q27, Q29-Q37, and Q39-Q50. These include the zero-hit phrases "decompose the calibration gap", "gap between probe and verbalized", "knowing more than it says", and "knowledge-expression gap". Queries with totals of 150 or more were used only for leads. The search covers arXiv-hosted text indexed up to about 2026-11-06. OpenReview-only and OSF-only full texts remain a gap (G-FT PARTIAL).
