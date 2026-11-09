# S1 Bundle Map: manuscripts → scripts → results

Wave 1, 2026-11-10. This is a read-only provenance trace. It records which claims exist and
what backs them. It does not judge the science. Nothing in `papers/`, `src/`, `results/` or
`data/` was modified to produce it.

## 0. Conventions

**Method.** Each manuscript (`papers/vN/main.tex`) was read in full. Every number that depends
on an experiment was looked up in the result JSONs in memory and compared after rounding to the
printed precision. Each result file was attributed to a producing script by matching its
filename, its `model` string and its top-level and per-problem key structure against what each
script dumps. Scripts were not executed, and no metric was recomputed apart from tallies of
bins and distributions taken from stored arrays.

**Status values.**

| Status | Meaning |
|--------|---------|
| MATCH | The value equals the JSON value after rounding. |
| MISMATCH | Both values are given. |
| NO-FILE | No file in the repository holds the value. |
| UNCLEAR | Derived, interpretive, or contradictory. |

**Line numbers** (`l.N`) are approximate positions in that version's `main.tex`. Labels are LaTeX
`\label`s. Table and figure numbers come from each version's `main.aux`.

**Remote roots.** No v1 to v3 script writes into this repository. Every script writes to one of
two GPU-box trees, and the result files here were copied back by hand. No copy step is recorded.

- **A** = `/home/ubuntu/dl4c_experiments/` (`results/`, `results_v2/`, `results_v3/`, `models/`, `data/`)
- **B** = `/home/ubuntu/dl4c/` (`results_v2/`, `results_v3/`, `models/`, `data/`)

**File shorthands.**

| Short | File |
|-------|------|
| R1-HE | `results/v1/exp1_qwen2.5-coder-7b_humaneval.json` |
| R1-MB | `results/v1/exp1_qwen2.5-coder-7b_mbpp_fixed.json` |
| R2-HE | `results/v2/main_humaneval.json` |
| R2-MB | `results/v2/main_mbpp.json` |
| R2-τ* | `results/v2/sensitivity_tau_{0.2,0.5,0.8,1.0}.json` |
| R2-n* | `results/v2/sensitivity_n_{3,5,10,20}.json` |
| R2-SFTE | `results/v2/sft_evaluation.json` |
| R2-SFTM | `results/v2/sft_training_metrics.json` |
| R3-Q | `results/v3/v3_qwen2.5-coder-7b_humaneval.json` |
| R3-D | `results/v3/v3_deepseek-coder-6.7b_humaneval.json` |
| R3-S | `results/v3/sft_discrimination.json` |
| R3-H | `results/v3/harness_info.json` |

## 1. Claim → location → script → result table

### 1.1 papers/v1 (DL4C / ICML 2026 workshop draft; identical to `archives/dl4cV1.zip`)

| ID | Claim (value) | Location | Producing script | Result file (key) | Status |
|----|---------------|----------|------------------|-------------------|--------|
| v1-C01 | HE sampling ECE .021, AUROC .990 | Abstract l.57; Intro l.76; §Results l.196; Concl. | v1 `exp1_optimized.py` | R1-HE `sampling_ece`, `sampling_auroc` | MATCH |
| v1-C02 | HE verbalized ECE .090, AUROC .546 | Abstract; l.76; l.196; l.360 | `exp1_optimized.py` | R1-HE `verbalized_*` | MATCH |
| v1-C03 | 63% of problems at max verbal confidence | Abstract; Concl. | `exp1_optimized.py` | R1-HE `verbalized_bins[2].count` 103/164 | MATCH |
| v1-C04 | 87.4% of max-confidence problems correct | Abstract; l.314; Fig. 1b | `exp1_optimized.py` | R1-HE `verbalized_bins[2].accuracy` | MATCH |
| v1-C05 | MBPP verbal ECE .755; "63×" sampling ECE | Abstract; l.77; l.198; l.364 | v2 `run_all_v2.py` | R1-MB `verbalized_ece`, `sampling_ece` | MATCH (63× is computed from rounded values; unrounded it is 64.7×) |
| v1-C06 | HE ECE gap 4.2×, Brier gap 5.1× | l.76; l.196 | `exp1_optimized.py` | R1-HE ratios | MATCH |
| v1-C07 | MBPP sampling ECE .012 | l.77; l.198 | `run_all_v2.py` | R1-MB `sampling_ece` | MATCH |
| v1-C08 | HE pass@1 .854 | Intro l.66 | `exp1_optimized.py` | R1-HE `pass_at_1` | MATCH |
| v1-C09 | Tab. 1 (`tab:main`) HE sampling .021/.027/.990 | l.185 | `exp1_optimized.py` | R1-HE `sampling_{ece,brier,auroc}` | MATCH |
| v1-C10 | Tab. 1 HE verbalized .090/.137/.546 | l.186 | `exp1_optimized.py` | R1-HE `verbalized_*` | MATCH |
| v1-C11 | Tab. 1 MBPP sampling .012/.013/.995 | l.189 | `run_all_v2.py` | R1-MB `sampling_*` | MATCH |
| v1-C12 | Tab. 1 MBPP verbalized .755/.636/.506 | l.190 | `run_all_v2.py` | R1-MB `verbalized_*` | MATCH |
| v1-C13 | MBPP row labelled "Instruct" model | l.163; l.177 | `run_all_v2.py` | R1-MB `model` = `qwen2.5-coder-7b-base` | UNCLEAR (label only) |
| v1-C14 | MBPP pass@1 .066; fails 93.4% | l.198; l.364 | `run_all_v2.py` | R1-MB `pass_at_1` | MATCH |
| v1-C15 | MBPP mean verbal confidence ≈.82 | l.198 | `run_all_v2.py` | derived from R1-MB `verbalized_confidences` = .821 | MATCH |
| v1-C16 | HE top sampling bin .99/.99, n=129 | l.312 | `exp1_optimized.py` | R1-HE `sampling_bins[7]` | MATCH |
| v1-C17 | Verbal uses only 3 bins in [.6, 1.0] | l.308; l.314; l.356 | `exp1_optimized.py` | R1-HE `verbalized_bins` | MATCH |
| v1-C18 | HE verbal counts 3/58/103 | l.360 | `exp1_optimized.py` | R1-HE `verbalized_bins[*].count` | MATCH |
| v1-C19 | 11/58 wrong at .8; 13/103 wrong at 1.0 | l.360 | `exp1_optimized.py` | derived cross-tab of R1-HE | MATCH |
| v1-C20 | MBPP 226 at .8, 29 at 1.0; 99.2% high | l.364 | `run_all_v2.py` | R1-MB `verbalized_bins` | MATCH |
| v1-C21 | MBPP 229/257 in lowest sampling bin | l.364 | `run_all_v2.py` | R1-MB `sampling_bins[0]` | MATCH |
| v1-C22 | HE evaluation ≈75 min | l.392 | `exp1_optimized.py` | R1-HE `time_seconds` = 4504.5 | MATCH |
| v1-C23 | 164 HE / 257 MBPP; n=10; τ=0.8 | l.57; l.115; l.163 | both | `per_problem` lengths, `pass_count` max | MATCH |
| v1-C24 | Correctness label = the τ=0.1 deterministic generation | Method l.126 | `exp1_optimized.py:134`; `run_all_v2.py:169` | code uses the first τ=0.8 sample | MISMATCH (text vs code) |
| v1-C25 | Quoted verbal prompt | l.123 | same | code prompt wording differs | MISMATCH (text vs code) |
| v1-C26 | 10 s timeout "per test case" | l.115; l.163 | `execute_code_safe` | timeout is per sample script | MISMATCH (minor, text vs code) |
| v1-C27 | Hardware GH200 480GB | l.163 | — | not recorded in any v1 file | NO-FILE |
| v1-C28 | SFT tiers high ≥0.8 / 0.3 / low | l.150–156; l.395 | `run_all_v2.py` (HumanEval); v1 `exp2_dpo_training.py` uses APPS | code threshold is ≥0.7 | MISMATCH (threshold) / NO-FILE |
| v1-C29 | 228 preference pairs (133/64/31) | l.158; l.402; l.424 | `run_all_v2.py` / `exp2_dpo_training.py` | A/data/`dpo_confidence_pairs.json` (remote only) | NO-FILE |
| v1-C30 | LoRA r=16, α=32, 3 epochs | l.158; l.402 | `exp2_dpo_training.py`; `run_all_v2.py` | code config | MATCH (config) |
| v1-C31 | DPO NaN losses after several hundred steps | l.158; l.404 | same | A/results/`dpo_training_metrics.json` (remote only) | NO-FILE |
| v1-C32 | Qualitative SFT behaviour (target confidence vocabulary) | Abstract; l.78; l.402 | `exp3_post_training_eval.py` / `run_all_v2.py` | A/results/`exp3_*.json` (remote only) | NO-FILE |
| v1-C33 | "Natural thresholds" .8/.3 visible in the reliability diagram | l.395 | — | interpretive | UNCLEAR |
| v1-C34 | MBPP failures are due to format mismatch | l.198; l.364 | `run_all_v2.py` | no diagnostic stored | UNCLEAR |
| v1-F1 | Fig. 1 `fig:reliability` (a) sampling and (b) verbal bins | l.204–310 (inline pgfplots) | transcribed | R1-HE `sampling_bins`, `verbalized_bins` | MATCH |
| v1-F2 | Fig. 2 `fig:distribution` correct/incorrect bars | l.318–358 (inline pgfplots) | transcribed | R1-HE cross-tab | MATCH |

### 1.2 papers/v2 (comprehensive revision)

| ID | Claim (value) | Location | Producing script | Result file (key) | Status |
|----|---------------|----------|------------------|-------------------|--------|
| v2-C01 | HE sampling ECE .029 [.022,.063], AUROC .982 [.959,.995] | Abstract l.62; §4.1 l.187; Tab. 1 `tab:humaneval` l.199; l.621; Concl. | v2 `exp_v2_comprehensive.py` | R2-HE `sampling_ece(_ci)`, `sampling_auroc(_ci)` | MATCH |
| v2-C02 | HE sampling Brier .036 | l.187; Tab. 1 | same | R2-HE `sampling_brier` | MATCH |
| v2-C03 | Tab. 1 sampling Brier CI [.022,.063] | l.199 | same | R2-HE `sampling_brier_ci` = [.019,.056] | MISMATCH (the ECE CI is printed in the Brier column) |
| v2-C04 | HE log-prob ECE .077 [.035,.136], AUROC .661 [.535,.776], Brier .122 | Abstract; l.209; Tab. 1 l.200; l.603 | same | R2-HE `logprob_*` | MATCH |
| v2-C05 | log-prob Brier CI [.035,.136] | Tab. 1 l.200 | same | `logprob_brier_ci` = [.081,.170] | MISMATCH |
| v2-C06 | verbal-numeric ECE .082 [.043,.139], Brier .124, AUROC .633 [.523,.743] | Tab. 1 l.201; l.612 | same | `verbal_numeric_*` | MATCH |
| v2-C07 | verbal-numeric Brier CI [.043,.139] | Tab. 1 | same | `verbal_numeric_brier_ci` = [.084,.169] | MISMATCH |
| v2-C08 | verbal-critique ECE .065 [.028,.118], Brier .120, AUROC .621 [.516,.720] | Tab. 1 l.202; l.209; l.612 | same | `verbal_critique_*` | MATCH |
| v2-C09 | verbal-critique Brier CI [.028,.118] | Tab. 1 | same | `verbal_critique_brier_ci` = [.086,.158] | MISMATCH |
| v2-C10 | verbal-CoT ECE .126 [.072,.177], Brier .134, AUROC .670 [.572,.754] | Tab. 1 l.203; l.209 | same | `verbal_cot_*` | MATCH |
| v2-C11 | verbal-CoT Brier CI [.072,.177] | Tab. 1 | same | `verbal_cot_brier_ci` = [.108,.161] | MISMATCH |
| v2-C12 | "All three verbal AUROC below 0.67" | Abstract l.62 | same | CoT .6695 | MATCH, but Tab. 1 prints .670 (internal inconsistency) |
| v2-C13 | HE pass@1 .860, pass@10 .951 | l.71; Tab. 1 caption; l.577; l.581 | same | R2-HE `pass_at_1`, `pass_at_10` | MATCH |
| v2-C14 | MBPP pass@1 .588, pass@10 .689 | l.71; Tab. 2 caption; l.171; l.577 | same | R2-MB | MATCH |
| v2-C15 | Tab. 2 `tab:mbpp` ECE/AUROC for 5 methods (10 cells) | l.222–226; l.211; l.612 | same | R2-MB `*_ece`, `*_auroc` | MATCH |
| v2-C16 | MBPP verbal ECE "> .220" / ".220–.289" | l.211; l.577; l.581 | same | CoT .2202 | MATCH (at the rounding edge) |
| v2-C17 | Sampling ECE <.03 and AUROC >.98 on both benchmarks; verbal ECE >.06 on HE | l.577 | same | R2-HE, R2-MB | MATCH |
| v2-C18 | MBPP pass@1 .066 → .588 after the signature fix | §3.3 l.171 | `run_all_v2.py` → `exp_v2_comprehensive.py` | R1-MB `pass_at_1`; R2-MB | MATCH |
| v2-C19 | Mean generation time 2.18 s/sample | §3.4 l.176; l.621; l.627 | same | R2-HE `mean_latency_per_sample_s` = 2.18 (MBPP is 1.28) | MATCH (HE only) |
| v2-C20 | τ=0.8, n=10, 512 tokens, 10 s, 1000 bootstraps, 80-problem subset | §3 | same | code constants | MATCH (config) |
| v2-C21 | All experiments on GH200 480GB | l.176; l.627 | — | `exp_final_a100.py` ran n=20 and SFT on A100-40GB | UNCLEAR (conflicts with code) |
| v2-C22 | Fig. 1(a) `fig:reliability` HE sampling points | l.263–269 | — | equal to the **v1** R1-HE bins, not R2-HE | MISMATCH (stale v1 data) |
| v2-C23 | Fig. 1(b) HE verbal (.6,1.0)(.8,.827)(1.0,.873) | l.295–300 | — | R2-HE `verbal_numeric_bins` = (.8,.75)(1.0,.909); v1 = .810/.874 | MISMATCH |
| v2-C24 | Fig. 1(c) MBPP sampling points | l.327–332 | — | matches neither R2-MB nor R1-MB bins | NO-FILE |
| v2-C25 | Fig. 1(d) MBPP verbal points | l.358–363 | — | R2-MB bins differ | NO-FILE / MISMATCH |
| v2-C26 | HE top bin ≈.99/.99; verbal only 3 bins ≥.6 | §4.2 l.235–237 | `exp_v2_comprehensive.py` | R2-HE bins | MATCH |
| v2-C27 | Verbal distributions (numeric 0/2/52/110; critique 1/12/97/54; CoT 0/87/4/73) | Fig. 2 `fig:verbal_dist` l.400–412; Tab. 6 `tab:verbal_detail` l.758–760 | same | R2-HE `conf_*_dist` | MATCH |
| v2-C28 | Percentages: 67% at 1.0; critique 33%/59%; CoT 45%/53% | §4.3 l.374; §5.1 l.598 | same | derived from C27 | MATCH |
| v2-C29 | Tab. 3 `tab:temperature` sampling pass@1/ECE/AUC across τ | l.438–441; l.424 | same | R2-τ* | MATCH |
| v2-C30 | Tab. 3 log-prob ECE/AUC; text "AUROC .566–.702" | l.438–441; l.456 | same | R2-τ* `logprob_*` | MATCH |
| v2-C31 | Tab. 3 verbal-numeric ECE/AUC; ".020–.028" | l.447–450; l.456 | same | R2-τ* `verbal_numeric_*` | MATCH |
| v2-C32 | Fig. 3 `fig:temp_ece` | l.478–488 (inline) | same | R2-τ* | MATCH |
| v2-C33 | Tab. 4 `tab:samples` n=3: ECE .025 [.004,.054], AUROC .998 [.992,1.00] | l.512; l.500; l.83 | same | `sensitivity_n_3.json` | MATCH |
| v2-C34 | Tab. 4 n=5: .020 [.005,.060], .984 [.941,1.00] | l.513 | same | `sensitivity_n_5.json` | MATCH |
| v2-C35 | Tab. 4 n=10: .026 [.010,.063], .990 [.967,1.00] | l.514 | same | `sensitivity_n_10.json` | MATCH |
| v2-C36 | Tab. 4 n=20: ECE .046 [.018,.112], AUROC .757 | l.515; l.500 | `exp_final_a100.py` | `sensitivity_n_20.json` | MATCH |
| v2-C37 | Tab. 4 n=20 AUROC CI [.600,.900] | l.515 | `exp_final_a100.py` | `sampling_auroc_ci` = [.617,.888] | MISMATCH |
| v2-C38 | Latency 6.5/10.9/21.8/43.6 s | Tab. 4; Fig. 4 `fig:samples_tradeoff` l.564; Abstract; l.621; l.627 | hand-derived as 2.18 × n | measured in the R2-n* files: 6.6/10.6/22.2/33.4 | UNCLEAR (derived; n=20 disagrees with its own run) |
| v2-C39 | "n=10 gives slightly narrower CIs than n=3" | l.521 | — | ECE CI width: n=3 .050, n=10 .053 | MISMATCH |
| v2-C40 | Confidence tiers ≥0.8 / 0.3–0.8 / <0.3 "from our data" | §5.4 l.623 | — | interpretive | NO-FILE |
| v2-C41 | SFT data: 274 examples | §5.5 l.632; l.669 | `exp_final_a100.py` | R2-SFTM `n_train` 246 + `n_eval` 28; B/data/`sft_confidence_data.json` (remote only) | MATCH (count) |
| v2-C42 | LoRA r=16, α=32, 3 epochs | l.634 | `exp_final_a100.py` | code | MATCH (config) |
| v2-C43 | Train loss 1.21 → 0.99 | l.634 | `exp_final_a100.py` | R2-SFTM `train_losses` 1.213 → **0.828** (0.999 is the 5th of 9 entries) | MISMATCH |
| v2-C44 | Eval loss 0.86 | l.634 | same | R2-SFTM `eval_losses[-1]` | MATCH |
| v2-C45 | Evaluated on a "held-out" 80-problem subset | l.634; Tab. 5 caption | `exp_final_a100.py` / `sft_eval_only.py` | SFT data is drawn from all 164 HE problems; eval uses `humaneval[:80]` | UNCLEAR (text vs code) |
| v2-C46 | Tab. 5 `tab:sft` pass@1 .950/.938 | l.646–649; l.655 | `sft_eval_only.py` | R2-SFTE `{base,sft}.pass_at_1` | MATCH |
| v2-C47 | Verbal ECE .148 [.095,.203] → .053 [.019,.103], −64% | Tab. 5; l.84; l.655; l.669 | same | R2-SFTE `verbal_ece(_ci)` | MATCH |
| v2-C48 | Verbal Brier .087 / .069 | Tab. 5 | same | R2-SFTE `verbal_brier` | MATCH |
| v2-C49 | Base Brier CI [.052,.128] | Tab. 5 | same | [.048,.135] | MISMATCH |
| v2-C50 | SFT Brier CI [.038,.106] | Tab. 5 | same | [.030,.118] | MISMATCH |
| v2-C51 | Verbal AUROC .428 / .473 | Tab. 5; l.655 | same | R2-SFTE `verbal_auroc` | MATCH |
| v2-C52 | Base AUROC CI [.207,.655] | Tab. 5 | same | [.205,.652] | MISMATCH (small) |
| v2-C53 | SFT AUROC CI [.246,.700], described as "wide" | Tab. 5; l.655 | same | [.447,.493] | MISMATCH |
| v2-C54 | Base 46% at 1.0; SFT .9 on 95%; true pass rate .94 | l.655; l.669 | same | R2-SFTE `verbal_dist` | MATCH |
| v2-C55 | DPO attempt numerically unstable | l.655 | `run_all_v2.py` | A/results/`dpo_training_metrics.json` (remote only) | NO-FILE |
| v2-C56 | Benchmark sizes 164 / 257 | Abstract; §3.3 | `exp_v2_comprehensive.py` | `n_problems` | MATCH |

### 1.3 papers/v3 (multi-model + reviewer response; identical to `archives/dl4cV2.zip`)

| ID | Claim (value) | Location | Producing script | Result file (key) | Status |
|----|---------------|----------|------------------|-------------------|--------|
| v3-C01 | Sampling ECE .059, AUROC .987 (independent labels) | Abstract; l.79; §4.1 l.218; l.598; Concl. | v3 `exp_v3_all.py` | R3-Q `sampling_ece`, `sampling_auroc` | MATCH |
| v3-C02 | Post-hoc calibration improves ECE but lowers AUROC | Abstract; Intro; §4.1; §4.3; §5.2 | same | R3-Q `logprob_isotonic_*`, `logprob_platt_*` | MATCH |
| v3-C03 | DeepSeek pass rate 0% | Abstract; §4.5; Tab. 2 caption | same | R3-D `pass_at_1_independent` = 0.0 | MATCH |
| v3-C04 | SFT cuts verbal ECE by 64% | Abstract; Intro; §4.7; §5.5 | v2 `sft_eval_only.py` | R2-SFTE | MATCH |
| v3-C05 | AST proxy AUROC .689 | Intro; §4.4; §5.3 | `exp_v3_all.py` | R3-Q `ast_proxy_auroc` | MATCH |
| v3-C06 | Harness: A100-SXM4-40GB, Python 3.10.12, PyTorch 2.11.0+cu130, 512 tokens, top-p .95, 10 s | §3.5 l.200; App. B | same (`log_harness_info`) | R3-H | MATCH |
| v3-C07 | GPU "40960 MiB"; scikit-learn 1.4 | App. B | — | R3-H `gpu_memory_gb` = 42.4; no scikit-learn version recorded | UNCLEAR / NO-FILE |
| v3-C08 | Mean generation time 2.18 s/sample (A100) | §3.5 l.200; §5.3 | — | R3-Q `mean_latency_per_sample_s` = 2.49; 2.18 is the v2 GH200 value | MISMATCH |
| v3-C09 | 274 SFT examples; LoRA r=16, α=32, 3 epochs | §3.6 | v2 `exp_final_a100.py` | R2-SFTM | MATCH |
| v3-C10 | Independent-label pass@1 .823 | §4.1 l.216; Tab. 1 caption | `exp_v3_all.py` | R3-Q `pass_at_1_independent` = **.884** | MISMATCH (.823 = 135/164 appears in no file) |
| v3-C11 | Tab. 1 `tab:main` sampling: ECE .059 [.035,.088], Brier .036, AUROC .987 [.971,.997], TACE .041 | l.236 | same | R3-Q `sampling_*` | MATCH |
| v3-C12a | Tab. 1 log-prob ECE .058 [.017,.108], AUROC .668 [.511,.798], TACE .083 | l.237; l.220 | same | R3-Q `logprob_*` | MATCH |
| v3-C12b | Tab. 1 log-prob Brier .122 | l.237 | same | R3-Q `logprob_brier` = .101 (.122 is the v2 value) | MISMATCH |
| v3-C13 | Isotonic ECE .047, AUROC .587 | l.238; l.220 | same | R3-Q `logprob_isotonic_*` | MATCH |
| v3-C14a | Platt ECE .003 | l.239 | same | R3-Q `logprob_platt_ece` | MATCH |
| v3-C14b | Platt AUROC .386 | l.239 | same | `logprob_platt_auroc` = .38547 | MISMATCH (rounding: .385) |
| v3-C15 | AST ECE .351 [.290,.414], AUROC .689 [.566,.790], TACE .351 | l.240; l.222 | same | R3-Q `ast_proxy_*` | MATCH |
| v3-C16a | Verbal τ=0.1 ECE .079, AUROC .564, TACE .099 (with CIs) | l.241; l.224 | same | R3-Q `verbal_tau01_*` | MATCH |
| v3-C16b | Verbal τ=0.1 Brier .124 | l.241 | same | R3-Q = .109 (.124 is v2 verbal-numeric) | MISMATCH |
| v3-C17a | Verbal τ=0.8 ECE .113, AUROC .519, TACE .123 (with CIs) | l.242; l.224 | same | R3-Q `verbal_tau08_*` | MATCH |
| v3-C17b | Verbal τ=0.8 Brier .134 | l.242 | same | R3-Q = .118 (.134 is v2 verbal-CoT, a different method) | MISMATCH |
| v3-C18 | τ=0.8 worse than τ=0.1 on every metric | l.224 | same | R3-Q | MATCH |
| v3-C19 | Fig. 1a `fig:reliability` sampling points | l.277 | intended: `exp_v3_all.py` | copied from v2/v1 figure; R3-Q bins differ | MISMATCH |
| v3-C20 | Fig. 1b verbal (.6,1.0)(.8,.827)(1.0,.873) | l.310 | intended: same | R3-Q `verbal_tau01_bins` acc 1.0/.839/.906 | MISMATCH |
| v3-C21 | 67% at max verbal confidence | §4.2 l.251; Fig. 1 caption; §5.1 | same | R3-Q `verbal_01_dist` 106/164 = 64.6% (67% is v2) | MISMATCH |
| v3-C22 | Verbal τ=0.1 uses 3 bins, none <0.6 | §4.2 | same | R3-Q | MATCH |
| v3-C23 | Tab. 2 `tab:deepseek` ECE [CI] for 5 methods | l.347–351; l.357 | same | R3-D `*_ece(_ci)` | MATCH except C23b |
| v3-C23b | DeepSeek AST CI lower bound .113 | l.349 | same | .11247 | MISMATCH (rounding: .112) |
| v3-C24 | DeepSeek AUROC undefined | §4.5 | same | R3-D `*_auroc` = NaN | MATCH |
| v3-C25 | DeepSeek failure caused by instruction-format mismatch | §4.5 l.336 | — | no diagnostic artifact | UNCLEAR |
| v3-C26 | Tab. 3 `tab:temperature` (all cells) | l.376–379 | v2 `exp_v2_comprehensive.py` | R2-τ* | MATCH |
| v3-C27 | Fig. 2 `fig:temp_ece` | inline | same | R2-τ* | MATCH |
| v3-C28 | τ-sweep text ranges | §4.6 l.362 | same | R2-τ* | MATCH |
| v3-C29 | Tab. 4 `tab:samples` n=3/5/10 | l.436–438 | same | R2-n{3,5,10} | MATCH |
| v3-C29b | Tab. 4 n=20 ECE/AUROC | l.439 | v2 `exp_final_a100.py` | `sensitivity_n_20.json` | MATCH |
| v3-C29c | Tab. 4 n=20 AUROC CI [.600,.900] | l.439 | same | [.617,.888] | MISMATCH (carried from v2) |
| v3-C30 | Latency 6.5/10.9/21.8/43.6 s | Tab. 4; Fig. 3; §4.6; §5.3 | hand-derived | 2.18 × n | UNCLEAR |
| v3-C31 | Fig. 3 `fig:samples_tradeoff` ECE line | inline | v2 | R2-n* | MATCH |
| v3-C32a | Tab. 5 `tab:sft` point values | l.511–512; l.499 | v2 `sft_eval_only.py` | R2-SFTE | MATCH |
| v3-C32b–e | Tab. 5 four CIs (base/SFT Brier, base/SFT AUROC) | l.511–512 | same | see v2-C49, C50, C52, C53 | MISMATCH (carried from v2) |
| v3-C33 | Tab. 6 `tab:sft_disc` All: n=80, ECE .058 | l.529 | `exp_v3_all.py` | R3-S `all_verbal_ece` | MATCH |
| v3-C33b | Tab. 6 All: mean confidence .900 | l.529 | same | R3-S `all_mean_conf` = .8925 | MISMATCH |
| v3-C34 | Tab. 6 Easy n=73 (.900/.100); Hard n=5 (.900/.700) | l.530–531; l.518 | same | R3-S `easy_*`, `hard_*` | MATCH |
| v3-C35 | SFT confidence distribution (76 at .9, 4 at .6); Fig. 4 `fig:sft_dist`; Tab. 9 | §4.7 l.518 | v2 `sft_eval_only.py` | R2-SFTE matches; R3-S `all_conf_dist` (.9: 79, .3: 1) does not | MATCH to R2-SFTE; the paper mixes two SFT runs |
| v3-C36 | True pass rate .938 | l.537; §5.5 | v2 | R2-SFTE `sft.pass_at_1` (R3-S has .95) | MATCH (to v2 run) |
| v3-C37 | App. C Tab. 7 `tab:bins` sampling bins | l.725–728 | intended: `exp_v3_all.py` | neither R3-Q nor R2-HE | MISMATCH / NO-FILE |
| v3-C38 | App. C Tab. 7 verbal bins (2/52/110; 1.0/.827/.873) | l.730–732 | same | R3-Q 2/56/106, 1.0/.839/.906 (counts equal v2) | MISMATCH |
| v3-C39 | App. D Tab. 8 `tab:verbal_detail` τ=0.1 dist 2/52/110 | l.749 | same | R3-Q `verbal_01_dist` = 2/56/106 | MISMATCH |
| v3-C39b | τ=0.8 "more dispersed" | l.750 | same | R3-Q `verbal_08_dist` 15/48/101 | UNCLEAR (qualitative) |
| v3-C40 | 1,000 bootstraps; 5-fold CV for isotonic/Platt | §3.4; App. B | same | code | MATCH (config) |
| v3-C41 | Method definitions (AST confidence eq. 3, TACE, verbal prompt, SFT tier phrases) | §3.2–3.4; App. A | same | code differs on each (see §4) | MISMATCH (text vs code) |

## 2. Per-version summary

### 2.1 Which source and result files each iteration relies on

| Manuscript | Source versions actually behind its numbers | Result files cited | Archive copy |
|------------|---------------------------------------------|--------------------|--------------|
| papers/v1 | `src/v1_baseline/exp1_optimized.py` (HumanEval); `src/v2_comprehensive/run_all_v2.py` (MBPP "fixed" run); SFT/DPO from `run_all_v2.py` / `exp2_dpo_training.py` (no files) | R1-HE, R1-MB | `archives/dl4cV1.zip` (byte-identical tex/bib/bbl) |
| papers/v2 | `src/v2_comprehensive/exp_v2_comprehensive.py` (main, τ, n=3/5/10); `exp_final_a100.py` (n=20, SFT training); `sft_eval_only.py` (SFT eval); `run_all_v2.py` (the .066 MBPP figure); Fig. 1(a) reuses v1 data | R2-HE, R2-MB, R2-τ*, R2-n*, R2-SFTE, R2-SFTM, R1-MB | none (no archive holds v2) |
| papers/v3 | `src/v3_multimodel/exp_v3_all.py` (main table, DeepSeek, SFT discrimination, harness); v2 scripts for Tabs. 3–5 and Figs. 2–4 | R3-Q, R3-D, R3-S, R3-H, R2-τ*, R2-n*, R2-SFTE, R2-SFTM | `archives/dl4cV2.zip` (byte-identical tex/bib/bbl, despite its name) |

`src/v4_dprc` is not cited by any manuscript. It is the code for a planned extension (DPRC)
and has produced only dry-run labels (§3.4).

### 2.2 Claims that changed between iterations

**v1 → v2**

- **HumanEval sampling:** ECE .021 → .029, Brier .027 → .036, AUROC .990 → .982.
- **HumanEval verbal:** ECE .090 / AUROC .546 becomes three strategies: numeric .082 / .633,
  critique .065 / .621 and CoT .126 / .670.
- **HumanEval pass@1:** .854 → .860.
- **MBPP was re-run end to end:**
  - pass@1 .066 → .588.
  - Sampling ECE .012 → .018.
  - Verbal ECE .755 → .220–.328.
  - The "63× gap" headline is dropped. The value .066 is kept only as the pre-fix figure.
- **Added:**
  - log-prob baseline
  - bootstrap CIs
  - MBPP AUROC table
  - temperature sweep (Tab. 3, Fig. 3)
  - sample-count sweep with latency (Tab. 4, Fig. 4)
  - verbal distribution figure and table
  - quantitative SFT table
- **SFT:** "228 pairs, qualitative" becomes "274 examples, ECE −64%, loss 1.21 → 0.99".
- **Reused without change:** Fig. 1(a), which still shows v1 bins.

**v2 → v3**

- **Labelling protocol** changed to independent labels.
  - HumanEval sampling ECE .029 → .059 and AUROC .982 → .987.
  - Log-prob ECE .077 → .058 and AUROC .661 → .668.
  - Verbal (numeric, now "τ=0.1") ECE .082 → .079 and AUROC .633 → .564.
  - pass@1 .860 → .823. The JSON says .884.
- **Hardware** statement changed from GH200 to A100.
- **Added:**
  - isotonic and Platt rows
  - AST proxy
  - verbal τ=0.8
  - TACE column
  - DeepSeek table
  - SFT discrimination table
  - SFT distribution figure
  - harness, bins and verbal-detail appendices
- **Removed:**
  - MBPP (table, figure panels, cross-benchmark section)
  - verbal-critique and verbal-CoT
  - pass@10
  - SFT loss values
  - DPO-instability note
  - Δ row of the SFT table
- **Carried over unchanged from v2:**
  - Tabs. 3–5 and Figs. 2–3, including the stale n=20 CI and four mismatched SFT CIs.
  - Fig. 1 coordinates.
  - The values 67%, 2.18 s, 64% and 274.
  - Brier values .122, .124 and .134 in the new Tab. 1. These are v2 numbers placed next to
    v3 ECE and AUROC values.

## 3. Flagged list

### 3.1 Claims with no backing result file (NO-FILE)

- **v1:**
  - C27: GH200 hardware.
  - C28, C29: SFT tiers and the 228 preference pairs. The data is in remote-only
    `dpo_confidence_pairs.json`.
  - C31: DPO NaN losses. The data is in remote-only `dpo_training_metrics.json`.
  - C32: qualitative SFT behaviour. The data is in remote-only `exp3_*.json`.
- **v2:**
  - C24, C25: Fig. 1(c,d) MBPP reliability points.
  - C40: confidence tiers "from our data".
  - C55: DPO instability.
- **v3:**
  - C07: "40960 MiB" and scikit-learn 1.4.
  - C10: pass@1 .823.
  - C37, C38: App. C bin table. These values match no file.
- **Hand-derived, not stored:** the latency series 6.5 / 10.9 / 21.8 / 43.6 s in v2 and v3
  is 2.18 × n. The measured n=20 run gives 33.4 s.

### 3.2 Values in a manuscript that disagree with the file that should back them (MISMATCH)

- **v2:**
  - Tab. 1: all four Brier CIs (C03, C05, C07, C09).
  - Fig. 1(a,b), which shows stale v1 data or matches no file (C22, C23).
  - Tab. 4: n=20 AUROC CI (C37).
  - The "narrower CI" sentence (C39).
  - Training loss endpoint (C43).
  - Tab. 5: four CIs (C49, C50, C52, C53).
- **v3:**
  - pass@1 (C10).
  - Tab. 1: three Brier values that are carried over from v2 (C12b, C16b, C17b).
  - Latency 2.18 s (C08).
  - Fig. 1 and the 67% figure (C19–C21).
  - Tab. 6 mean confidence (C33b).
  - App. C/D distributions (C37–C39).
  - The four SFT CIs and the n=20 CI carried from v2 (C29c, C32b–e).
  - Two third-decimal rounding cases (C14b, C23b).
- **Method text vs code, all versions:**
  - v1 correctness-label definition, prompt wording, timeout scope, SFT threshold
    (C24–C26, C28).
  - v2 log-prob is defined as sigmoid(mean logp) while the code uses exp(mean logp); appendix
    prompts differ from the code; base-model verbal parsing in `sft_eval_only.py`; the
    "held-out" subset overlaps the SFT training source (C45).
  - v3 AST-confidence formula, TACE binning and weighting, and verbal prompt (C41). R3-Q and
    R3-D Brier/AUROC are stored as bootstrap means, not point estimates.

### 3.3 Result files or keys no manuscript cites

- **Whole files:**
  - None of the 18 result files is entirely uncited by every version.
  - `results/v2/main_mbpp.json` is cited only by v2. v3 dropped MBPP.
  - `results/v1/*` is cited by v1, and R1-MB again by v2 (.066).
- **Significant uncited keys:**
  - `sensitivity_n_20.json` `pass_at_1` = **0.0875**. The other subset runs are .90–.95. This
    file has a different schema and verbal prompt, and its n=20 row is reported without this
    value.
  - R3-Q / R3-D `*_firstsample` metrics and `pass_at_1_first_sample`.
  - Brier, TACE and CIs for isotonic, Platt and AST. The Platt ECE .0028 lies outside its own
    CI.
  - R3-Q `mean_latency_per_sample_s` 2.49.
  - R3-S `all_verbal_auroc` .493, `n_medium` = 2, `hard_mean_correct` .2.
  - R2-SFTE sampling metrics.
  - R2-SFTM `time_minutes`.
  - R2-MB Brier values and CIs.
  - R2-τ* critique/CoT metrics.
  - R1 `pass_at_10`.
- **`data/v4_dprc/labels/*`** is cited by no manuscript. It is dry-run output.

### 3.4 Scripts whose outputs are missing from the repository

| Script | Missing output(s) |
|--------|-------------------|
| v1 `exp1_baseline_calibration.py` | `{model}_{bench}.json` ×4, `experiment1_summary.json` |
| v1 `exp1_vllm.py`, `exp1_streamlined.py`, `exp1_final.py` | their per-run `exp1_*` files (the repo's R1-HE matches `exp1_optimized.py` only), `experiment1_summary.json` |
| v1 `exp2_dpo_training.py` | `dpo_confidence_pairs.json`, DPO/SFT adapters, `dpo_training_metrics.json` |
| v1 `exp3_post_training_eval.py` | `exp3_{base,dpo,sft}_{humaneval,mbpp}.json`, `experiment3_summary.json` |
| v1 `exp4_trust_study.py` | `experiment4_trust_study.json` |
| v1 `run_all_experiments.py` | `experiment_log.json` |
| v2 `run_all_v2.py` | everything except R1-MB: DPO pairs/metrics, adapters, `exp3_qwen-{dpo,sft}_humaneval.json`, trust study |
| v2 `exp34_eval.py` | `exp3_qwen-sft_humaneval.json`, `experiment4_trust_study.json` |
| v2 `exp_v2_comprehensive.py` | its own `sensitivity_n_20.json`, `sensitivity_summary.json`, flat `sft_evaluation.json` (the sensitivity loop seems not to have finished, or was not copied back) |
| v2 `exp_final_a100.py` | `sft_confidence_data.json`, SFT adapter, its own `sft_evaluation.json` variant |
| v3 `exp_v3_multimodel.py` | all 5: `deepseek-coder-v2-lite_{humaneval,mbpp}.json`, `sensitivity_n_20.json`, `sft_evaluation.json`, `cross_model_summary.json` |
| v3 `deploy_v3.sh` | remote `v3_log.txt` |
| No trained adapter from any version is in the repository. | |

### 3.5 Dry-run or empty outputs (v4_dprc)

- **`results/v4_dprc/` is empty.** No v4 module writes there. The analysis modules
  (`pilot.py`, `hidden_probe.py`, `repair_derisk.py`, `test_adequacy.py`, `type_effect.py`)
  print to stdout only.
- **`data/v4_dprc/adapters/` is empty.** `train_dprc.py` was never run to completion, so
  `dprc_{model}_{level}_{loss}/` is missing.
- **`data/v4_dprc/labels/labels_dryrun.jsonl` and `_manifest.json` are a stub run** of
  `label_dataset.py` (StubGenerator, default `--limit 5`). Details:
  - 5 HumanEval problems, 23 groups, `gen_secs` 0.0, 253 executions.
  - Each problem has only two distinct solutions: the canonical one and one perturbation.
  - Only the filename marks it as a dry run; the records carry no model field.
- **v4 stages with no output at all:**
  - real Phase-1 labelling (`pool*`, `bcb_full/train/test`)
  - stage-(a) training
  - GATE-2 pilot
  - hidden-state probe
  - repair de-risk
  - self-tests (`selftests_qwen.jsonl`)
  - requirement typing (`req_types.jsonl`)
  - test adequacy
  - type effect
- **Cited AUROC values with no backing file.** The `hidden_probe.py` docstring cites AUROC
  values (oracle 0.805, digit readout 0.603) that no file backs.
- **README gaps.** `src/v4_dprc/README.md` omits six modules, all BigCodeBench and
  `/workspace/...`-path based. It also lists APPS in the Phase-1 command, which
  `config.POOL_MIX` has dropped.

### 3.6 Documentation errors in REPRODUCE.md §2

Script → output attributions that the code contradicts:

| REPRODUCE.md says | What the code shows |
|-------------------|---------------------|
| `exp1_baseline_calibration.py` writes both v1 files | R1-HE comes from `exp1_optimized.py`; R1-MB comes from v2 `run_all_v2.py` |
| `exp1_*` variants all write the same JSONs | only `exp1_optimized.py` matches |
| `run_all_experiments.py` reproduces v1 | it loads scripts from the box path under the module name `"module"`, so no `__main__` block runs |
| `exp34_eval.py` and `exp_final_a100.py` write `results/v2/sft_evaluation.json` | that file comes from `sft_eval_only.py` |
| `run_all_v2.py` writes "results/v2/*.json" | it writes to the v1-era directory |
| `exp_v3_multimodel.py` produced the four `results/v3` files | they come from `exp_v3_all.py` |
| `deploy_v3.sh` launches the v3 run | it launches `exp_v3_multimodel.py`; no launcher exists for `exp_v3_all.py` |

REPRODUCE.md also does not distinguish the two different `qwen_confidence_sft` adapters. The
root A adapter was trained on DPO pairs; the root B adapter was trained on
`sft_confidence_data.json`.

## 4. Unknowns

| Item | What was examined | Why it is unresolved |
|------|-------------------|----------------------|
| Exact producer of R1-HE | key order, `model` string, n, and schema of all five v1 exp1 variants and `run_all_v2.py` | Only `exp1_optimized.py` fits, but no run log exists to confirm it, or to rule out an unrecorded edit. |
| Which `run_all_v2.py` revision produced R1-MB | `execute_mbpp` in `run_all_v2.py` vs `execute_mbpp_fixed` in `exp_v2_comprehensive.py` | There is no version history for the scripts. |
| Copy-back from roots A and B to `results/vN` | all scripts and REPRODUCE.md | No script or log records the copy or any renaming. A v2 script's output (R1-MB) sits under `results/v1`. |
| Missing `sensitivity_summary.json` | `exp_v2_comprehensive.py` control flow | The run either crashed before writing it or the file was not copied; this cannot be determined. |
| Source of v2 Fig. 1(b–d), v3 Fig. 1 and App. C bins | v1, v2 and v3 bins; recomputed tallies of v2 confidences × v3 labels | The tallies reproduce .827 but not .873. No file matches. |
| Source of the mismatched Tab. 5 CIs | R2-SFTE, and the alternative `sft_evaluation` schemas from `exp_final_a100.py`, `exp_v2_comprehensive.py` and `exp_v3_multimodel.py` | No alternative file exists in the repository. They may come from an overwritten run on root B. |
| v3 pass@1 .823 | `pass_at_1_independent`, `pass_at_1_first_sample`, the v2 values | No file holds .823 (135/164). |
| Hardware statements (GH200 vs A100) | script docstrings, R3-H | v1 and v2 runs record no hardware. R3-H is the only recorded harness. |
| DeepSeek "instruction-format mismatch" | R3-D `per_problem` | No diagnostic output was stored. |
| v4 BigCodeBench inputs (`bcb_full/train/test`, `selftests_qwen`, `req_types`) | all v4 modules, `data/v4_dprc` | The train/test split has no producer in the repository. `/workspace/...` is a box path. |
| Remote logs (`v3_log.txt`, `experiment_log.json`) | repo-wide | None are in the repository. |
| `research/` notes and runs as a possible source of box outputs | not examined | Out of scope for this map. |
