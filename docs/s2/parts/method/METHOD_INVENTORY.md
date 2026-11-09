# Method inventory: manuscripts vs code (v1, v2, v3, v4_dprc)

Sub-agent B1, wave 2. Read-only trace. This file records what each manuscript version states and
what each code version implements, with locations. It does not judge which side is right and does
not evaluate the science. No legacy code was run. Numbers taken from stored result JSONs are
labeled as such.

## 0. How to read this file

**Locations.** `l.N` is a line of `papers/vN/main.tex`. `file:N` is a line of a script under `src/`.
Remote box paths that appear in the scripts are not reproduced here; "box A" and "box B" are the
two remote trees described in `docs/s1/BUNDLE_MAP.md` section 0.

**Which code is paired with which manuscript.** The pairing follows `docs/s1/BUNDLE_MAP.md` section 2.1
and was re-checked against the scripts' `RESULTS_DIR`/file names and result-file keys.

| Manuscript | Code used for the pair | What it produced in `results/` |
|---|---|---|
| v1 (`papers/v1/main.tex`) | `src/v1_baseline/exp1_optimized.py` (HumanEval); `src/v2_comprehensive/run_all_v2.py` (MBPP "fixed" run, and the preference-pair / SFT / DPO code) | `results/v1/exp1_qwen2.5-coder-7b_humaneval.json`, `results/v1/exp1_qwen2.5-coder-7b_mbpp_fixed.json` |
| v2 (`papers/v2/main.tex`) | `src/v2_comprehensive/exp_v2_comprehensive.py` (main tables, tau sweep, n=3/5/10); `exp_final_a100.py` (n=20, SFT data and training); `sft_eval_only.py` (SFT evaluation) | `results/v2/*` |
| v3 (`papers/v3/main.tex`) | `src/v3_multimodel/exp_v3_all.py` (main table, DeepSeek, SFT discrimination, harness info); v2 scripts for sweeps and SFT | `results/v3/*` |

The other scripts in `src/v1_baseline/` (`exp1_baseline_calibration.py`, `exp1_vllm.py`,
`exp1_streamlined.py`, `exp1_final.py`, `exp2_dpo_training.py`, `exp3_post_training_eval.py`,
`exp4_trust_study.py`, `run_all_experiments.py`), `src/v2_comprehensive/exp34_eval.py`, and
`src/v3_multimodel/exp_v3_multimodel.py` / `deploy_v3.sh` are not the recorded producers of any file in `results/`. Where
they differ from the producer on an element, that is noted as "variant".

**Marks.** Each row compares the manuscript statement of a version with the code paired to that same
version. `AGREE`: both sides state it and it matches. `DIFFER`: both sides state it and they do not
match. `ABSENT`: one side says nothing (the cell names which side). `n/a`: the element does not
exist for that version on either side. A mark applies only to the stated item.

**Summary rule (section 12).** For an element and version: DIFFER if any sub-item is DIFFER, else AGREE
if at least one sub-item is AGREE, else ABSENT.

## 1. Benchmarks, splits, and any held-out subset

| # | Item | Manuscript says | Code does | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 1.1 | HumanEval source and size | v1: 164 problems (l.163). v2: 164 (l.169). v3: 164, HF `openai_humaneval`, unmodified `check()` (l.200, l.701-702) | `load_dataset("openai_humaneval", split="test")`: `exp1_optimized.py:167-168`; `exp_v2_comprehensive.py:201-204`; `exp_v3_all.py:214-217`. Stored `n_problems`/lengths are 164 in R1/R2/R3 files | AGREE | AGREE | AGREE |
| 1.2 | MBPP source and size | v1: MBPP Sanitized, 257 (l.163). v2: same (l.169). v3: not used (l.616 "a single benchmark") | `load_dataset("google-research-datasets/mbpp", "sanitized", split="test")`: `exp1_optimized.py:169-170` (not the recorded MBPP producer), `run_all_v2.py:132-135` (R1-MB), `exp_v2_comprehensive.py:206-209` (R2-MB). `exp_v3_all.py` has no MBPP loader (its harness record only names the MBPP source string, `exp_v3_all.py:48`) | AGREE | AGREE | AGREE |
| 1.3 | Fields read from MBPP | v1, v2: "natural language description and test cases" (v2 l.169); v1 silent | description from `prompt`, tests as `"\n".join(test_list)`, reference `code` kept but unused: `run_all_v2.py:132-135`, `exp_v2_comprehensive.py:206-209` | ABSENT (text) | AGREE | n/a |
| 1.4 | Subset for sweeps | v2: "fixed subset of 80 HumanEval problems" for tau and n sweeps (l.176, l.424, l.504). v3: same (l.200, l.362, l.428) | `humaneval[:80]`: `exp_v2_comprehensive.py:374`; `exp_final_a100.py:148` (n=20) | n/a | AGREE | AGREE |
| 1.5 | Which 80 problems | v2, v3: not stated (only "fixed") | the first 80 in dataset order: `exp_v2_comprehensive.py:374`, `exp_final_a100.py:148,319`, `sft_eval_only.py:157`, `exp_v3_all.py:418` | n/a | ABSENT (text) | ABSENT (text) |
| 1.6 | SFT / preference data source | v1: "from HumanEval", 10-sample results (l.150). v2: "from HumanEval execution feedback" (l.632). v3: same (l.205) | all 164 HumanEval problems: `run_all_v2.py:540` (v1 pairs), `exp_final_a100.py:425` (SFT data, v2/v3). Variant: `exp2_dpo_training.py:80-95` builds pairs from APPS `introductory` problems (cap 500), not HumanEval | AGREE | AGREE | AGREE |
| 1.7 | "Held-out" SFT evaluation subset | v2: "a held-out 80-problem subset of HumanEval" (l.634; caption l.638 "HumanEval subset"). v3: "80-problem evaluation subset" (l.499), no "held-out" wording. v1: no evaluation subset | evaluation uses `humaneval[:80]` (`sft_eval_only.py:157`, `exp_final_a100.py:319`) but the SFT data was generated from all 164 problems (`exp_final_a100.py:425`). The 90/10 train/eval split is over examples, not problems, `train_test_split(test_size=0.1, seed=42)` (`exp_final_a100.py:257`; stored `n_train` 246, `n_eval` 28 in `results/v2/sft_training_metrics.json`) | ABSENT | DIFFER | ABSENT (text uses no held-out claim; overlap exists in code) |
| 1.8 | Easy/hard subsets of the SFT discrimination table | v3: easy pass >= 0.8 (n=73), hard pass < 0.5 (n=5) (l.518) | `exp_v3_all.py:439-441`: easy >= 0.8, hard < 0.5, medium 0.5 to < 0.8 (n=2, not in the table). The pass rate is the SFT model's own 10-sample rate (`exp_v3_all.py:426-428`) | n/a | n/a | AGREE |
| 1.9 | Other subsets in code only | none of v1-v3 | trust study uses `humaneval[:50]` (`run_all_v2.py:363`, `exp34_eval.py:158`) | ABSENT (text) | ABSENT (text) | n/a |

## 2. Models, checkpoints, revisions

| # | Item | Manuscript says | Code does | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 2.1 | Primary model | v1: Qwen2.5-Coder-7B-Instruct (l.163). v2: same (l.176). v3: same (l.200) | HF id `Qwen/Qwen2.5-Coder-7B-Instruct`: `exp1_optimized.py:22`; `run_all_v2.py:22`; `exp_v2_comprehensive.py:27`; `exp_v3_all.py:34`. The MBPP run labels its output model `qwen2.5-coder-7b-base` (`run_all_v2.py:522,528`, stored `model` field) while loading the Instruct id | AGREE | AGREE | AGREE |
| 2.2 | Second model | v3: DeepSeek-Coder-6.7B-Instruct (l.200). v1, v2: single model (v2 l.663) | v3 producer: `deepseek-ai/deepseek-coder-6.7b-instruct` (`exp_v3_all.py:35`). Variant: `exp_v3_multimodel.py:29` and `deploy_v3.sh` (launches `exp_v3_multimodel.py`) use `deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct`. v1 producer lists DeepSeek-Coder-6.7B too (`exp1_optimized.py:23`, loop at `:174`) but `results/v1` holds Qwen only; v1 text names Qwen only | ABSENT (text) | AGREE | AGREE |
| 2.3 | Exact checkpoint revision or commit hash | none in v1-v3 | no `revision=` argument in any script (searched `src/`); only HF repo ids. Not located in any result file | ABSENT | ABSENT | ABSENT |
| 2.4 | Precision and loading flags | none stated | `bfloat16`, `device_map="auto"`, `trust_remote_code=True`: `exp1_optimized.py:87`; `exp_v2_comprehensive.py:511`; `exp_v3_all.py:490`. The keyword is `dtype=` in most scripts and `torch_dtype=` in `exp_final_a100.py:261,311,315,410` | ABSENT | ABSENT | ABSENT |
| 2.5 | Hardware and software | v1: GH200 480GB (l.163). v2: GH200 480GB (l.176). v3: A100-SXM4-40GB, Python 3.10.12, PyTorch 2.11.0+cu130, "40960 MiB", scikit-learn 1.4 (l.200, l.698-707) | no hardware recorded by v1 or v2 producers. `exp_final_a100.py:1-6` states A100-40GB (it ran n=20 and SFT). `results/v3/harness_info.json`: A100-SXM4-40GB, Python 3.10.12, torch 2.11.0+cu130, `gpu_memory_gb` 42.4, no scikit-learn version recorded | ABSENT (code) | DIFFER | AGREE (GPU, Python, torch); memory figure and scikit-learn version not located |
| 2.6 | Base model of the SFT adapter | not stated in v1-v3 | `BASE_MODEL` = Qwen2.5-Coder-7B-Instruct: `run_all_v2.py:22,281,325`; `exp_final_a100.py:21,260` | ABSENT | ABSENT | ABSENT |

## 3. Prompts and instruction formats

Every prompt below is stored verbatim (rendered from the source with Python's `ast`, not retyped)
in `prompts/`, one file per prompt, first line `# SOURCE: file:line-range`. Placeholders such as
`{prob['prompt']}` mark where the problem text is inserted. Generation goes through
`tokenizer.apply_chat_template([...], add_generation_prompt=True)` with a single user turn unless a
system turn is listed; if that call raises, the raw user text is used (e.g. `exp1_optimized.py:108-109`,
`exp_v2_comprehensive.py:195-197`). The manuscripts say nothing about the chat template.
`v4_selftests_test_prompt.txt` contains one em-dash because it is verbatim source text.

### 3.1 Comparison

| # | Prompt | Manuscript text | Code (file:line) and prompt file | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 3.1 | HumanEval generation | v1: not quoted. v2: "Complete the following Python function. Only output the complete function, no explanations." (l.176; appendix l.703-709). v3: appendix l.650-657 | `exp1_optimized.py:107` (`prompts/v1_exp1_optimized_codegen.txt`); `exp_v2_comprehensive.py:213` (`prompts/v2_exp_v2_comprehensive_codegen_humaneval.txt`); `exp_v3_all.py:242` (`prompts/v3_exp_v3_all_codegen.txt`). Same sentence plus a blank line and the problem text | ABSENT (text) | AGREE | AGREE |
| 3.2 | MBPP generation | v1: not quoted. v2: "Write a Python function to solve: {description}. Only output the function, no explanations." (l.176; appendix l.712-718) | `run_all_v2.py:148` (`prompts/v2_run_all_v2_codegen_mbpp.txt`, R1-MB producer); `exp_v2_comprehensive.py:214` (`prompts/v2_exp_v2_comprehensive_codegen_mbpp.txt`). `exp1_optimized.py:107` would send the HumanEval-style sentence to MBPP descriptions (variant). Text and code are the same wording; the code puts a newline before "Only output" | ABSENT (text) | AGREE | n/a |
| 3.3 | Verbal numeric confidence | v1: "Rate your confidence that this solution is correct on a scale of 1 (very uncertain) to 5 (very confident)." (l.123). v2: same sentence (l.136) and appendix block ending "Only output the number." (l.720-726). v3: "...on a scale of 1--5." (l.160); appendix l.659-665 | v1 `exp1_optimized.py:126` (`prompts/v1_exp1_optimized_verbal.txt`): "Rate your confidence from 1-5 (1=unsure, 5=confident). Format: CONFIDENCE: [N]. Then solve." v2 `exp_v2_comprehensive.py:217` (`prompts/v2_exp_v2_comprehensive_verbal_numeric.txt`): "(1=very unsure, 5=very confident) that your solution is correct. Format: CONFIDENCE: [N]\nThen provide the solution." v3 `exp_v3_all.py:276` (`prompts/v3_exp_v3_all_verbal.txt`): same but without "that your solution is correct". The code asks for a solution plus the rating in one response; no version contains "Only output the number" | DIFFER | DIFFER | DIFFER |
| 3.4 | Verbal critique-then-rate | v2: critique "for potential pitfalls, difficulty, and edge cases", solve, rate 1-5 (l.138-139; appendix l.728-734) | `exp_v2_comprehensive.py:219-222` (`prompts/v2_exp_v2_comprehensive_verbal_critique.txt`): "(edge cases, tricky constraints)", "rate your confidence 1-5 that you can solve it correctly. Format: CONFIDENCE: [N]" | n/a | DIFFER | n/a |
| 3.5 | Verbal chain-of-thought | v2: l.141-142; appendix l.736-741 | `exp_v2_comprehensive.py:224-227` (`prompts/v2_exp_v2_comprehensive_verbal_cot.txt`): "Think step by step... Format: CONFIDENCE: [N]" | n/a | DIFFER | n/a |
| 3.6 | Verbal at tau = 0.8 | v3: same prompt as tau = 0.1, temperature 0.8 (l.162-163; appendix l.667-668) | `exp_v3_all.py:281` reuses `ci_01` (`prompts/v3_exp_v3_all_verbal.txt`) | n/a | n/a | AGREE |
| 3.7 | Chat template and system turn | none stated | chat template, user turn only for all main generation prompts; system turn only in SFT-model elicitation (row 3.8) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 3.8 | SFT-model elicitation prompt | v2, v3: not quoted (v3 appendix l.679-692 lists only the tier phrases) | system + user pair: `exp_final_a100.py:340-341` (`prompts/v2_exp_final_a100_sfteval_verbal_sft.txt`); `sft_eval_only.py:121-122` (`prompts/v2_sft_eval_only_verbal_sft.txt`); `exp_v3_all.py:430-431` (`prompts/v3_exp_v3_all_sftdisc_verbal_sft.txt`) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 3.9 | SFT-evaluation code-generation prompt | not stated separately | "Complete the following Python function. Only output the function." (no "complete", no "no explanations"): `exp_final_a100.py:333`, `sft_eval_only.py:115`, `exp_v3_all.py:425` (`prompts/v2_sft_eval_only_codegen.txt`, `prompts/v3_exp_v3_all_sftdisc_codegen.txt`) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 3.10 | Base-model verbal prompt in the SFT comparison | v2 Tab. 5 and v3 Tab. 5 call it the base model's verbal confidence; prompt not quoted | "Rate confidence 1-5. Format: CONFIDENCE: [N]. Then solve." (`sft_eval_only.py:124`, `prompts/v2_sft_eval_only_verbal_base.txt`; `exp_final_a100.py:345` is the same wording), different from 3.3 | n/a | ABSENT (text) | ABSENT (text) |
| 3.11 | n=20 verbal prompt | not stated | `exp_final_a100.py:167` (`prompts/v2_exp_final_a100_n20_verbal.txt`): same wording as `exp_v3_all.py:276`, not the `PROMPT_NUMERIC` text used for the n=3/5/10 runs (`exp_v2_comprehensive.py:217`) | n/a | ABSENT (text) | ABSENT (text) |
| 3.12 | SFT data-generation and training prompts | v1, v2, v3: not quoted | generation: "Complete the following Python function:\n\n{...}" (`run_all_v2.py:214`, `exp_final_a100.py:213`); training user turn: "State your confidence level, then complete the following Python function.\n\n{...}" (`run_all_v2.py:238`, `exp_final_a100.py:230`). Evaluation prompts differ from the training user turn (see 3.8) | ABSENT (text) | ABSENT (text) | ABSENT (text) |

### 3.2 Prompt file index

| File | Source | Note |
|---|---|---|
| `prompts/v1_exp1_baseline_calibration_humaneval_qwen_deepseek.txt` | `src/v1_baseline/exp1_baseline_calibration.py:143-143,144-144` | not the producer of results/v1 |
| `prompts/v1_exp1_baseline_calibration_mbpp_qwen_deepseek.txt` | `src/v1_baseline/exp1_baseline_calibration.py:158-158,159-159` | not the producer of results/v1 |
| `prompts/v1_exp1_baseline_calibration_verbal_other_models.txt` | `src/v1_baseline/exp1_baseline_calibration.py:178-178` | not the producer of results/v1 |
| `prompts/v1_exp1_baseline_calibration_verbal_qwen_deepseek.txt` | `src/v1_baseline/exp1_baseline_calibration.py:173-173,174-174` | not the producer of results/v1 |
| `prompts/v1_exp1_final_codegen.txt` | `src/v1_baseline/exp1_final.py:156-156` | not the producer of results/v1 |
| `prompts/v1_exp1_final_verbal.txt` | `src/v1_baseline/exp1_final.py:182-182` | not the producer of results/v1 |
| `prompts/v1_exp1_optimized_codegen.txt` | `src/v1_baseline/exp1_optimized.py:107-107` | user turn, chat template applied |
| `prompts/v1_exp1_optimized_verbal.txt` | `src/v1_baseline/exp1_optimized.py:126-126` | user turn, tau=0.1 |
| `prompts/v1_exp1_streamlined_codegen.txt` | `src/v1_baseline/exp1_streamlined.py:109-109,110-110` | not the producer of results/v1 |
| `prompts/v1_exp1_streamlined_verbal.txt` | `src/v1_baseline/exp1_streamlined.py:152-152,153-153` | not the producer of results/v1 |
| `prompts/v1_exp1_vllm_codegen_humaneval.txt` | `src/v1_baseline/exp1_vllm.py:118-118` | not the producer of results/v1 |
| `prompts/v1_exp1_vllm_codegen_mbpp.txt` | `src/v1_baseline/exp1_vllm.py:120-120` | not the producer of results/v1 |
| `prompts/v1_exp1_vllm_verbal.txt` | `src/v1_baseline/exp1_vllm.py:126-126` | not the producer of results/v1 |
| `prompts/v1_exp2_dpo_training_apps_datagen.txt` | `src/v1_baseline/exp2_dpo_training.py:125-125,126-126` |  |
| `prompts/v1_exp2_dpo_training_conf_labels.txt` | `src/v1_baseline/exp2_dpo_training.py:35-35,36-36,37-37,41-41,42-42,46-46,47-47` | APPS-based preference data; dpo_confidence_pairs.json is not in the repository |
| `prompts/v1_exp2_dpo_training_pair_prompt.txt` | `src/v1_baseline/exp2_dpo_training.py:229-229` |  |
| `prompts/v1_exp3_post_training_eval_verbal_trained.txt` | `src/v1_baseline/exp3_post_training_eval.py:142-142,143-143` |  |
| `prompts/v1_exp4_trust_study_calibrated.txt` | `src/v1_baseline/exp4_trust_study.py:165-165,166-166` |  |
| `prompts/v1_exp4_trust_study_plain.txt` | `src/v1_baseline/exp4_trust_study.py:170-170,171-171` |  |
| `prompts/v2_exp_final_a100_conf_labels.txt` | `src/v2_comprehensive/exp_final_a100.py:136-136,137-137,138-138` | assistant-turn confidence sentences in SFT data |
| `prompts/v2_exp_final_a100_n20_verbal.txt` | `src/v2_comprehensive/exp_final_a100.py:167-167` | n=20 sensitivity, tau=0.1 |
| `prompts/v2_exp_final_a100_sft_datagen_prompt.txt` | `src/v2_comprehensive/exp_final_a100.py:213-213` |  |
| `prompts/v2_exp_final_a100_sft_train_prompt.txt` | `src/v2_comprehensive/exp_final_a100.py:230-230` |  |
| `prompts/v2_exp_final_a100_sfteval_codegen.txt` | `src/v2_comprehensive/exp_final_a100.py:333-333` | base vs SFT sampling |
| `prompts/v2_exp_final_a100_sfteval_verbal_base.txt` | `src/v2_comprehensive/exp_final_a100.py:345-345` |  |
| `prompts/v2_exp_final_a100_sfteval_verbal_sft.txt` | `src/v2_comprehensive/exp_final_a100.py:340-340,341-341` |  |
| `prompts/v2_exp_v2_comprehensive_codegen_humaneval.txt` | `src/v2_comprehensive/exp_v2_comprehensive.py:213-213` |  |
| `prompts/v2_exp_v2_comprehensive_codegen_mbpp.txt` | `src/v2_comprehensive/exp_v2_comprehensive.py:214-214` |  |
| `prompts/v2_exp_v2_comprehensive_sft_eval.txt` | `src/v2_comprehensive/exp_v2_comprehensive.py:457-457,458-458` | SFT model verbal elicitation |
| `prompts/v2_exp_v2_comprehensive_sft_system.txt` | `src/v2_comprehensive/exp_v2_comprehensive.py:229-235` |  |
| `prompts/v2_exp_v2_comprehensive_verbal_cot.txt` | `src/v2_comprehensive/exp_v2_comprehensive.py:224-227` | tau=0.1 |
| `prompts/v2_exp_v2_comprehensive_verbal_critique.txt` | `src/v2_comprehensive/exp_v2_comprehensive.py:219-222` | tau=0.1 |
| `prompts/v2_exp_v2_comprehensive_verbal_numeric.txt` | `src/v2_comprehensive/exp_v2_comprehensive.py:217-217` | tau=0.1 |
| `prompts/v2_run_all_v2_codegen_humaneval.txt` | `src/v2_comprehensive/run_all_v2.py:148-148` |  |
| `prompts/v2_run_all_v2_codegen_mbpp.txt` | `src/v2_comprehensive/run_all_v2.py:148-148` |  |
| `prompts/v2_run_all_v2_conf_labels.txt` | `src/v2_comprehensive/run_all_v2.py:204-204,205-205,206-206` | confidence sentences prepended to training responses |
| `prompts/v2_run_all_v2_dpo_sft_datagen_prompt.txt` | `src/v2_comprehensive/run_all_v2.py:214-214` |  |
| `prompts/v2_run_all_v2_dpo_sft_train_prompt.txt` | `src/v2_comprehensive/run_all_v2.py:238-238` |  |
| `prompts/v2_run_all_v2_verbal_base.txt` | `src/v2_comprehensive/run_all_v2.py:164-164` | tau=0.1 |
| `prompts/v2_run_all_v2_verbal_trained.txt` | `src/v2_comprehensive/run_all_v2.py:161-161,162-162` | used when use_trained_conf=True |
| `prompts/v2_sft_eval_only_codegen.txt` | `src/v2_comprehensive/sft_eval_only.py:115-115` |  |
| `prompts/v2_sft_eval_only_verbal_base.txt` | `src/v2_comprehensive/sft_eval_only.py:124-124` |  |
| `prompts/v2_sft_eval_only_verbal_sft.txt` | `src/v2_comprehensive/sft_eval_only.py:121-121,122-122` |  |
| `prompts/v3_exp_v3_all_codegen.txt` | `src/v3_multimodel/exp_v3_all.py:242-242` | Qwen and DeepSeek |
| `prompts/v3_exp_v3_all_sftdisc_codegen.txt` | `src/v3_multimodel/exp_v3_all.py:425-425` |  |
| `prompts/v3_exp_v3_all_sftdisc_verbal_sft.txt` | `src/v3_multimodel/exp_v3_all.py:430-430,431-431` |  |
| `prompts/v3_exp_v3_all_verbal.txt` | `src/v3_multimodel/exp_v3_all.py:276-276` | used at tau=0.1 and tau=0.8 |
| `prompts/v4_repair_derisk_regen_prompt.txt` | `src/v4_dprc/repair_derisk.py:33-35 (build_regen_prompt)` |  |
| `prompts/v4_repair_derisk_repair_prompt.txt` | `src/v4_dprc/repair_derisk.py:26-30 (build_repair_prompt), joined in source order` |  |
| `prompts/v4_sampling_build_prompt_call.txt` | `src/v4_dprc/sampling.py:22-26 (build_prompt, call style); {tests} is empty or the block shown after the blank line (first 3 assert lines of the problem units)` |  |
| `prompts/v4_sampling_build_prompt_io.txt` | `src/v4_dprc/sampling.py:19-21 (build_prompt, style == "io"); literals joined with problem.prompt as in source` |  |
| `prompts/v4_selftests_test_prompt.txt` | `src/v4_dprc/selftests.py:19-23 (build_test_prompt); problem.prompt is appended after the blank line, as in source` |  |
| `prompts/v4_type_requirements_type_prompt.txt` | `src/v4_dprc/type_requirements.py:21-28 (build_type_prompt)` |  |

Notes on the index. `exp_v3_multimodel.py:266-286` defines `PROMPT_DIRECT`, `PROMPT_MBPP`,
`PROMPT_NUMERIC`, `PROMPT_CRITIQUE`, `PROMPT_COT`, and `PROMPT_SFT` with the same text as
`exp_v2_comprehensive.py:213-235` (compared side by side); no separate files were written for that
variant. `PROMPT_SFT` (`exp_v2_comprehensive.py:229`) is defined and not referenced in that file. `exp34_eval.py:110,123-124,175,177,226-227`
holds near-copies of the SFT-evaluation and trust-study prompts (variant, not stored separately).

## 4. Sampling parameters and sample counts

| # | Item | Manuscript says | Code does | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 4.1 | Temperature for sampling confidence and labels | v1: 0.8 (l.115, l.163). v2: 0.8 (l.176). v3: 0.8 (l.200) | `temp=0.8`: `exp1_optimized.py:112`; main call `exp_v2_comprehensive.py:522`; `exp_v3_all.py:246` | AGREE | AGREE | AGREE |
| 4.2 | Temperature for verbal elicitation | v1: 0.1 (l.123, l.163). v2: 0.1 (l.135, l.176). v3: 0.1 and 0.8 (l.159-163) | `temp=0.1`: `exp1_optimized.py:129`; `exp_v2_comprehensive.py:288,293,298`; `exp_v3_all.py:277` (0.1) and `:281` (0.8) | AGREE | AGREE | AGREE |
| 4.3 | top-p | v1, v2: not stated. v3: 0.95 (l.200, l.704) | `top_p=0.95`: `exp1_optimized.py:78`; `exp_v2_comprehensive.py:168,179`; `exp_v3_all.py:190,199` | ABSENT (text) | ABSENT (text) | AGREE |
| 4.4 | Max new tokens | v1: not stated. v2: 512 (l.176). v3: 512 (l.200, l.704) | `MAX_TOKENS = 512` (`exp1_optimized.py:27`, `exp_v2_comprehensive.py:31`, `exp_v3_all.py:31`), passed as `max_new_tokens` | ABSENT (text) | AGREE | AGREE |
| 4.5 | Prompt truncation | none stated | prompt tokenized with `truncation=True, max_length=2048`: `exp1_optimized.py:75`; `exp_v2_comprehensive.py:163`; `exp_v3_all.py:185` | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 4.6 | Stop sequences | none stated | none set; generation ends at EOS or the token cap. No stop strings in any `generate` call (`exp1_optimized.py:78`, `exp_v2_comprehensive.py:167`, `exp_v3_all.py:189`) | ABSENT | ABSENT | ABSENT |
| 4.7 | Other decoding settings | none stated | `do_sample=True` always (verbal at 0.1 is sampled, not greedy). v2 and v3 clamp with `temperature=max(temp, 0.01)` (`exp_v2_comprehensive.py:167`, `exp_v3_all.py:189`); v1 passes `temp` unclamped (`exp1_optimized.py:78`). `top_k`, penalties, and a generation seed are not set (library or model `generation_config` defaults apply and are not recorded) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 4.8 | Samples per problem for sampling confidence | v1: n = 10 (l.115, l.163). v2: n = 10 default (l.176). v3: n = 10 (l.200) | `NUM_SAMPLES = 10` (`exp1_optimized.py:26`); `n_samples=10` (`exp_v2_comprehensive.py:522`); first 10 of 11 (`exp_v3_all.py:246-249`). Variant: `exp1_baseline_calibration.py:33` has 20 | AGREE | AGREE | AGREE |
| 4.9 | Extra generations per problem | v1: one verbal generation (l.123). v2, v3: not itemized | v1: 10 + 1 verbal (`exp1_optimized.py:112,129`). v2: 10 + 1 log-prob generation (`exp_v2_comprehensive.py:281`) + 3 verbal (`:288,293,298`). v3: 10 + 1 independent-label sample (`exp_v3_all.py:246`) + 1 log-prob generation (`:271`) + 2 verbal (`:277,281`) | AGREE | ABSENT (text) | ABSENT (text) |
| 4.10 | Sweep grids | v2: tau in {0.2, 0.5, 0.8, 1.0}, n in {3, 5, 10, 20} (l.176). v3: same (l.200) | `exp_v2_comprehensive.py:379,394`; n = 20 comes from a different script, `exp_final_a100.py:160`, with its own extractor (`:94-104`) and verbal prompt (3.11). Stored `pass_at_1` of `results/v2/sensitivity_n_20.json` is 0.0875; the other subset runs are 0.90 to 0.95 | n/a | AGREE (grid); n=20 provenance ABSENT (text) | AGREE (grid); n=20 provenance ABSENT (text) |
| 4.11 | pass@k definition | v1, v2 report pass@1 (and v2 pass@10) without a formula; v3 reports pass@1 | pass@1 = mean of the single label; pass@10 = mean of `1 - C(n-c, k)/C(n, k)` with `k = min(10, n)` (`exp1_optimized.py:151-153`; `exp_v2_comprehensive.py:329-335`); v3 stores `pass_at_1_independent` and `pass_at_1_first_sample` (`exp_v3_all.py:306-307`) | ABSENT (text) | ABSENT (text) | ABSENT (text) |

## 5. Execution harness and correctness label

| # | Item | Manuscript says | Code does | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 5.1 | Isolation | v1: "subprocess isolation" (l.163). v2: "in a subprocess" (l.169). v3: "subprocess isolation ... temporary file cleanup" (l.200, l.703) | each candidate is written to a `NamedTemporaryFile(suffix='.py')`, run with `subprocess.run(['python3', path], capture_output=True, text=True, timeout=10)`, and the file is deleted in `finally`: `exp1_optimized.py:48-54`; `exp_v2_comprehensive.py:85-90`; `exp_v3_all.py:133-138`. No container, no resource limits, no network or filesystem restriction, and the `python3` found on `PATH` is used (not `sys.executable`) | AGREE | AGREE | AGREE |
| 5.2 | Timeout scope | v1: "10-second timeout per test case" (l.115, l.163). v2: "per test case" (l.120, l.169). v3: "10-second timeout" (l.130), "per test" (l.200, l.703) | `timeout=10` applies to the whole script, which contains the entire `check()` (HumanEval) or all assertions (MBPP); there is no per-assertion timeout. A timeout or any exception returns `False` (bare `except`) | DIFFER | DIFFER | DIFFER |
| 5.3 | Correctness label definition (pass criterion) | all test cases pass (v1 l.120; v2 l.125, l.170; v3 l.135, l.702) | label true iff process exit code 0 (`returncode == 0`): `exp1_optimized.py:52`; `exp_v2_comprehensive.py:88`; `exp_v3_all.py:136` | AGREE | AGREE | AGREE |
| 5.4 | Which generation is the label (greedy vs sample) | v1: "the single deterministic generation (the same one used for verbalized confidence)", tau = 0.1 (l.123, l.126). v2: first of the n samples, tau = 0.8 (l.125). v3: an independent (n+1)th sample, tau = 0.8 (l.165-168) | v1: `corr_list.append(float(sample_ok[0]))`, the first tau = 0.8 sample (`exp1_optimized.py:134`; same in `run_all_v2.py:171`). The tau = 0.1 verbal response is only parsed for a rating and its code is never executed (`exp1_optimized.py:129-130`). v2: `first_correct = sample_results[0]["correct"]` (`exp_v2_comprehensive.py:277`, labels at `:320`). v3: 11th sample (`exp_v3_all.py:246,250,256,300`); the first-sample label is also stored (`:259,301`). No greedy decoding exists anywhere in v1-v3 | DIFFER | AGREE | AGREE |
| 5.5 | Label for the SFT tables | v2: Tab. 5 (l.636-655). v3: Tab. 5 and Tab. 6 (l.499-531); the independent-label protocol is described in the Method (l.165-168) | v2 and v3 SFT tables use the first sample of the 10 (`sft_eval_only.py:129`; `exp_final_a100.py:351`; SFT discrimination `exp_v3_all.py:436`), not an independent draw | n/a | AGREE (first-sample) | ABSENT (text does not say which protocol applies to the SFT tables) |
| 5.6 | HumanEval program assembly | v3: unmodified `check()` (l.201-202, l.702). v1, v2: only that tests run (v2 l.169) | `full = code if prompt in code else prompt + code`; tests = dataset `test` + `"\ncheck(entry_point)"`: `exp1_optimized.py:117-119`; `exp_v2_comprehensive.py:92-95`; `exp_v3_all.py:140-143` | ABSENT (text) | ABSENT (text) | AGREE |
| 5.7 | Code extraction | none stated | first fenced block via ``r'```(?:python)?\n?(.*?)```'``. Fallback when no fence differs by script: whole response (`exp1_optimized.py:56-58`); from the first `def` or `class` line (`run_all_v2.py:69-89`, `exp_v2_comprehensive.py:121-135`); from the first `def` line only (`exp_final_a100.py:82-92`, `sft_eval_only.py:67-76`, `exp_v3_all.py:145-154`) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 5.8 | MBPP execution and "signature enforcement" | v2: parses the tests "to extract the expected function name and validating that the generated code defines a function with the matching signature"; this resolved depressed pass rates, 0.066 to 0.588 (l.171). v1: nothing stated | R1-MB producer `run_all_v2.py:54-58`: raw `code + "\n" + tests`, no fix. R2-MB producer `exp_v2_comprehensive.py:97-119`: run raw first; if it fails and the function named in the first `assert name(` is not defined, append `name = <first def in the code>` and run again. No signature or argument validation. Wrong-name solutions that behave correctly pass | ABSENT (text) | DIFFER | n/a |
| 5.9 | Failed generation handling | none stated | `except: results.append("")` turns a failed `generate` into an empty response (counted as incorrect and as an unparsed verbal answer): `exp_v2_comprehensive.py:170-171`; `exp_final_a100.py:122`; `sft_eval_only.py:100`; `exp_v3_all.py:192`. `exp1_optimized.py` has no such handler | n/a | ABSENT (text) | ABSENT (text) |
| 5.10 | Variant harnesses | none | v4 splits each test into its own subprocess (section 11); `exp_v3_multimodel.py:124` repeats `execute_mbpp_fixed` | n/a | n/a | n/a |

## 6. Confidence-estimation methods (formulas as implemented)

### 6.1 Method inventory

| # | Method | Manuscript | Code | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 6.1 | Number of methods | v1: "three confidence estimation approaches" (l.109), then defines two (l.114-123). v2: "five ... spanning three families" (l.114). v3: "seven ... four families" (l.119) | v1 producer: sampling and verbalized only (`exp1_optimized.py:132-133,140`). v2: sampling, log-prob, three verbal (`exp_v2_comprehensive.py:337-339`). v3: sampling, log-prob, AST, verbal tau 0.1, verbal tau 0.8 (`exp_v3_all.py:311-317`) plus isotonic and Platt (`:375`) = seven | DIFFER | AGREE | AGREE |
| 6.2 | Sampling (pass-rate) confidence | v1 eq. `eq:sampling` (l.117); v2 (l.122); v3 (l.132): `c_i = (1/n) * sum_j 1[pass(s_ij)]` | `c = sum(ok)/len(ok)`: `exp1_optimized.py:123`; `exp_v2_comprehensive.py:274`; `exp_v3_all.py:262` (over the first 10 samples). This is an execution pass rate (requires tests), not agreement between outputs | AGREE | AGREE | AGREE |
| 6.3 | Log-probability confidence | v2 eq. `eq:logprob` (l.130): `c = sigma( (1/L) * sum_l log p(t_l \| t_<l) )`. v3 (l.140): same. v1: none | v2: `c = exp( (1/L) * sum_l log p(t_l \| t_<l) )`, the geometric mean token probability, `confidence = float(np.exp(mean_lp))` (`exp_v2_comprehensive.py:189-191`). v3: same (`exp_v3_all.py:207-208`). Computed from a forward pass of the untempered model over all generated tokens `out[0][P:]` (includes the end token if emitted): log-softmax of raw logits (`:184-189`, `:202-206`). It is taken from a separate fresh generation at tau, not from any of the 10 sampled solutions or the labeled one (`exp_v2_comprehensive.py:281`, `exp_v3_all.py:271`); on any exception the value is 0.5 (`:282-283`, `:272-273`). Stored values (R2-HE min 0.706 max 0.996; R3-Q min 0.817 max 0.999) are consistent with exp, not a sigmoid of a non-positive number. Variant `exp_v3_multimodel.py:233` uses `1/(1+exp(-mean_lp))` (sigmoid, as in the text) and is not the recorded producer | ABSENT | DIFFER | DIFFER |
| 6.4 | v1 variant logit-style confidences | not in v1 text | not in the producer. Variants: mean over tokens of the max softmax probability (`exp1_baseline_calibration.py:259-266`, `exp1_streamlined.py:132`, first 50 tokens); mean chosen-token probability over the first 50 tokens (`exp1_vllm.py:196-219`) | ABSENT (text) | n/a | n/a |
| 6.5 | Post-hoc calibration on log-prob (isotonic, Platt) | v3: 5-fold CV, each fold's held-out predictions mapped through a calibrator fit on the other four (l.145-149; appendix l.676-677: scikit-learn `IsotonicRegression`, logistic regression with intercept) | `KFold(n_splits=5, shuffle=True, random_state=42)` (`exp_v3_all.py:353`); inputs are the raw `exp(mean_lp)` values and the independent labels; `IsotonicRegression(out_of_bounds='clip')` (`:360`); `LogisticRegression()` with library defaults (L2, C = 1) on the 1-D confidence (`:366`); single-class training folds fall back to the training base rate (`:369`); an exception falls back to raw confidence (isotonic) or the overall mean label (Platt) (`:372-373`). Out-of-fold predictions are pooled and scored once (`:375-387`). Shuffle and seed are not in the text | n/a | n/a | AGREE (shuffle, seed, defaults ABSENT in text) |
| 6.6 | AST clustering proxy | v3 eq. `eq:ast` (l.154): `c = \|largest_cluster(s_1..s_n)\| / n`, clusters formed "after normalizing variable names and whitespace" (l.152) | `normalize_code_for_ast(code) = ast.dump(ast.parse(code), annotate_fields=False)`, fallback `code.strip()` on a parse error (`exp_v3_all.py:175-181`). `K` = number of distinct normalized strings among the 10 samples (`:265`). `c = max(0, 1 - (K - 1)/9)` (`:267`). Identifiers and constants stay in the dump (no variable-name normalization); whitespace and comments vanish through parsing. Example: cluster sizes {5, 3, 2} give 0.5 by the text and 0.778 by the code; `K = 10` gives 0.1 by the text and 0.0 by the code. Stored values lie on the grid k/9 | n/a | n/a | DIFFER |
| 6.7 | Verbal numeric confidence: scale mapping | v1: 1-5 divided by 5 (l.123). v2: mapped to {0.2, 0.4, 0.6, 0.8, 1.0} (l.135). v3: same (l.160) | first regex digit clipped to [1, 5] then `/5` (`exp1_optimized.py:61-62`; `exp_v2_comprehensive.py:140-141`; `exp_v3_all.py:157-158`) | AGREE | AGREE | AGREE |
| 6.8 | Verbal parsing rules | none stated in v1-v3 | `re.search(r'CONFIDENCE:\s*(\d)', resp)` over the whole response (first match, one digit); else `re.search(r'(\d)\s*/\s*5', resp)` with `int/5` and no clipping (so `0/5` gives 0.0 and `7/5` gives 1.4); else a keyword ladder; else the default 0.6. Ladders differ per script (table 6.2) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 6.9 | Verbal critique and CoT: extraction | v2: not stated beyond "rates its confidence on the same 1-5 scale" (l.139) | same `extract_numeric_conf` on the critique and CoT responses (`exp_v2_comprehensive.py:294,299`); responses are capped at 512 new tokens, and a response that never reaches a `CONFIDENCE:` line falls through to the ladder or 0.6 | n/a | ABSENT (text) | n/a |
| 6.10 | Verbal tau = 0.8 | v3 (l.162-163) | `exp_v3_all.py:281-282`, same prompt and extractor as tau = 0.1 | n/a | n/a | AGREE |
| 6.11 | SFT-model verbal readout | v1: three phrases (l.153-155). v2: three phrases (l.632). v3: phrases mapped to 0.9, 0.6, 0.3 (l.205; appendix l.679-691) | `extract_trained_conf`: lower-cased substring tests in order, `'i am confident this solution is correct'` gives 0.9; `'should work for most cases'` or `'please verify'` gives 0.6; `'not confident'` or `'may contain bugs'` gives 0.3; otherwise falls back to the numeric extractor (`exp_v3_all.py:168-173`; `exp_final_a100.py:106-111`; `run_all_v2.py:104-111`). `sft_eval_only.py:78-89` (the R2-SFTE producer) has its own variant ending in a different ladder and is applied to the base model's answers as well (`:126`, both branches call `extract_trained_conf`) | ABSENT (text; no numeric mapping) | ABSENT (text; no numeric mapping) | AGREE |

### 6.2 Verbal keyword-ladder fallbacks per script

The ladder applies only when both regexes fail. All use `resp.lower()` substring tests, in the order shown, first hit wins.

| Script | Ladder (value: triggers) |
|---|---|
| `exp1_optimized.py:65-70` | 0.9: `very confident`; 0.8: `confident` and not `not` anywhere in the response; 0.6: `should work` or `most cases`; 0.3: `unsure`, `not confident`, `not sure`; default 0.6 |
| `run_all_v2.py:96-102` | 0.9: `very confident`, `certainly correct`; 0.8: `i am confident`, `quite confident`, `highly confident`; 0.6: `should work`, `most cases`, `fairly`, `moderately`; 0.3: `unsure`, `not confident`, `not sure`, `uncertain`, `may have bugs`; 0.2: `very unsure`, `likely wrong`, `probably incorrect` (`very unsure` is already caught by the `unsure` test at 0.3); default 0.6 |
| `exp_v2_comprehensive.py:144-150` (and `exp_v3_multimodel.py:159-177`) | 1.0: `very confident`, `5/5`; 0.8: `quite confident`, or (`confident` and not `not`); 0.6: `moderately`, `should work`, `fairly`; 0.4: `somewhat`, `unsure`; 0.2: `not confident`, `unlikely`; default 0.6 |
| `exp_final_a100.py:99-104`, `exp_v3_all.py:161-166` | 1.0: `very confident`; 0.8: `confident` and not `not`; 0.6: `should work`, `moderately`; 0.4: `unsure`, `not confident`; default 0.6 |
| `sft_eval_only.py:78-89` | trained phrases first (0.9, 0.6, 0.3 as above), then `CONFIDENCE:\s*(\d)`, then 0.8: `confident` and not `not`; 0.6: `should work`; 0.4: `unsure`; default 0.6 |

Because the default is 0.6 and 0.6 is also a valid parsed rating, parse failures are
indistinguishable from a rating of 3 in the stored arrays; the stored `*_dist` counts at 0.6 include
both.

## 7. Calibration and discrimination metrics

| # | Item | Manuscript says | Code does | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 7.1 | ECE: bins | M = 10 equally spaced bins, weighted by `\|B_m\|/N` (v1 eq. `eq:ece` l.134-136; v2 l.150-152; v3 l.176-178) | `bounds = np.linspace(0, 1, 11)`; bin i is `[b_i, b_(i+1))`, last bin closed on the right; empty bins skipped; weights `bin_size/len(c)`: `exp1_optimized.py:29-39`; `exp_v2_comprehensive.py:35-45`; `exp_v3_all.py:62-72`. Floating-point edge: `linspace` gives 0.6000000000000001, so a confidence of exactly 0.6 (3/5) lands in `[0.5, 0.6]` (stored verbal bins in R2-HE and R3-Q show `lo` 0.5, `hi` 0.6000000000000001, `n` 2) | AGREE | AGREE | AGREE |
| 7.2 | Equal-width vs equal-mass | ECE equal-width (all). v3 says TACE is equal-mass (l.184) | ECE equal-width; TACE equal-count after sorting (7.4) | AGREE | AGREE | AGREE |
| 7.3 | Brier | mean squared error `(c - y)^2` (v1 l.142; v2 l.158; v3 l.192) | `np.mean((c - a)**2)`: `exp1_optimized.py:41`; `exp_v2_comprehensive.py:47`; `exp_v3_all.py:93` | AGREE | AGREE | AGREE |
| 7.4 | TACE | v3 eq. `eq:tace` (l.186): `(1/\|R\|) * sum_{m in R} \|acc(B_m) - conf(B_m)\|`, adaptive (equal-mass) bins, `R` = bins above a minimum sample count (l.184-189). v1, v2: none | `compute_tace` (`exp_v3_all.py:74-91`): sort by confidence; `n_bins = max(1, int(sqrt(n)))` (12 for n = 164, 8 for n = 80); `bin_size = n // n_bins`, last bin takes the remainder (21 samples for n = 164); a bin contributes `(len/n) * gap` only if `gap > 0.01`, otherwise nothing. The bin-count (minimum sample) criterion is absent; the threshold acts on the gap size, not the sample count; the sum is weighted by bin share and is not divided by `\|R\|`. Ties are ordered by `np.argsort` default | n/a | n/a | DIFFER |
| 7.5 | Number of metrics | v1: "three" (l.131). v2: "three" (l.147). v3: "five complementary metrics" (l.173), then lists four (ECE, TACE, Brier, AUROC) | v1 producer: ECE, Brier, AUROC (`exp1_optimized.py:140-147`). v2: same three. v3: ECE, Brier, AUROC, TACE (`exp_v3_all.py:99-117`) | AGREE | AGREE | DIFFER |
| 7.6 | AUROC | area under ROC with confidence as the score for correct vs incorrect (v1 l.145; v2 l.160; v3 l.194) | `sklearn.metrics.roc_auc_score(labels, confidences)`; `nan` when the labels contain one class (`exp1_optimized.py:43-46`; `exp_v2_comprehensive.py:49-52`; `exp_v3_all.py:95-97`). Ties are handled by scikit-learn (library behavior) | AGREE | AGREE | AGREE |
| 7.7 | Undefined AUROC | v3: undefined for DeepSeek, single class (l.336) | `nan` rule above; `pass_at_1_independent` 0.0 in R3-D | n/a | n/a | AGREE |
| 7.8 | What the stored "point" value is | none stated | ECE and TACE are computed on the full sample; stored Brier and AUROC for v2 and v3 are the mean of the bootstrap replicates (`exp_v2_comprehensive.py:342-349`; `exp_final_a100.py:362-368`; `sft_eval_only.py:140-143`; `exp_v3_all.py:322-331`). v1 stores full-sample values (`exp1_optimized.py:141-144`) | AGREE | ABSENT (text) | ABSENT (text) |
| 7.9 | Classification threshold | none | none; all metrics use the continuous confidence | n/a | n/a | n/a |

## 8. Confidence intervals and the bootstrap

v1 reports no intervals in text or code (`exp1_optimized.py` computes none).

| # | Item | Manuscript says | Code does | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 8.1 | Resample count | v2: 1,000 (l.147, l.164). v3: 1,000 (l.173, l.706) | `n_boot=1000`: `exp_v2_comprehensive.py:54,71`; `exp_final_a100.py:46`; `sft_eval_only.py:35`; `exp_v3_all.py:99` | n/a | AGREE | AGREE |
| 8.2 | Resampling unit | v2: "resampling the problem set with replacement" (l.164). v3: not stated (l.173, l.706 say "resampling iterations") | `idx = rng.randint(0, len(c), len(c))` applied jointly to confidences and labels, i.e. problems with replacement, no stratification: `exp_v2_comprehensive.py:60`; `exp_final_a100.py:54`; `exp_v3_all.py:106` | n/a | AGREE | ABSENT (text) |
| 8.3 | Interval type | v2: 2.5th and 97.5th percentiles (l.164). v3: same (l.706) | percentile on the sorted replicate list: `vals[int(0.025*len(vals))]` and `vals[int(0.975*len(vals))]` (no interpolation, no bias correction); `len(vals)` counts non-NaN replicates (`exp_v2_comprehensive.py:69`; `exp_final_a100.py:62`; `exp_v3_all.py:114`). With 1,000 replicates these are the 26th and 976th ordered values | n/a | AGREE | AGREE |
| 8.4 | Replicates dropped | none stated | NaN replicates (single-class resample, undefined AUROC) are skipped (`exp_v2_comprehensive.py:63-64`; `exp_v3_all.py:109`); any exception in the metric also skips the replicate (bare `except: pass`) | n/a | ABSENT (text) | ABSENT (text) |
| 8.5 | Seed and sharing of resamples | not stated | seed 42 (section 10). In `exp_v2_comprehensive.py:54-56,71-76` each metric is bootstrapped by its own call that reseeds with 42 (the three metrics see the same resamples); in `exp_final_a100.py:47`, `sft_eval_only.py:36`, `exp_v3_all.py:100` one generator is created per call and consumed metric after metric (different resamples per metric) | n/a | ABSENT (text) | ABSENT (text) |
| 8.6 | Intervals for post-hoc calibrated scores | not stated | CV predictions are pooled once, then bootstrapped; calibrators are not refit per resample (`exp_v3_all.py:375-378`) | n/a | n/a | ABSENT (text) |

## 9. SFT and DPO training details and thresholds

Producers. v1 text: pair/SFT code in `run_all_v2.py:200-354` (HumanEval-based; the adapters are not in the repository). v2 and v3 text: `exp_final_a100.py:205-300` (SFT data and training), evaluated by `sft_eval_only.py` (v2 Tab. 5) and `exp_v3_all.py:401-466` (v3 Tab. 6). Variant: `exp2_dpo_training.py` (APPS-based pairs). No data file or adapter exists in the repository.

| # | Item | Manuscript says | Code does | v1 | v2 | v3 |
|---|---|---|---|---|---|---|
| 9.1 | Base model | not stated | Qwen2.5-Coder-7B-Instruct (`run_all_v2.py:22,281,325`; `exp_final_a100.py:21,260`) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 9.2 | LoRA r and alpha | v1: r = 16, alpha = 32 (l.158). v2: same (l.634). v3: same (l.205) | `LoraConfig(r=16, lora_alpha=32, ...)`: `run_all_v2.py:284,328`; `exp_final_a100.py:264` | AGREE | AGREE | AGREE |
| 9.3 | LoRA dropout, targets, bias | not stated | `lora_dropout=0.05`; targets `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`; `bias="none"`; `TaskType.CAUSAL_LM` (`run_all_v2.py:284-286`; `exp_final_a100.py:264-266`) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 9.4 | Epochs | v1: 3 (l.158). v2: 3 (l.634). v3: 3 (l.205) | `num_train_epochs=3`: `run_all_v2.py:289,333`; `exp_final_a100.py:268` | AGREE | AGREE | AGREE |
| 9.5 | Learning rate, batch, scheduler | not stated | SFT lr 2e-5, cosine, warmup ratio 0.1 (`run_all_v2.py:334-335`); per-device batch 2 with accumulation 8 (`run_all_v2.py:333-334`) for v1; v2 and v3 adapter: per-device batch 1, accumulation 16, lr 2e-5, cosine, `warmup_ratio=0.1`, `max_length=2048`, bf16, gradient checkpointing, evaluation each epoch (`exp_final_a100.py:268-272`) | ABSENT (text) | ABSENT (text) | ABSENT (text) |
| 9.6 | DPO attempt | v1: "initial attempt at DPO ... NaN losses" (l.158). v2: "numerically unstable" (l.655) | `DPOConfig` lr 5e-7, beta 0.1, cosine, warmup 0.1, 3 epochs, batch 2 x accumulation 8, `max_length=2048`, LoRA as above (`run_all_v2.py:289-294`); no metrics file exists | AGREE (existence); hyperparameters ABSENT (text) | AGREE (existence); hyperparameters ABSENT (text) | n/a |
| 9.7 | Confidence-tier thresholds | v1: high >= 0.8, medium 0.3 to < 0.8, low < 0.3 (l.153-155). v2: high >= 0.7, medium 0.3 to < 0.7, low < 0.3 (l.632). v3: same as v2 (l.205; appendix l.682-690) | `>= 0.7` high, `>= 0.3` medium, else low: `run_all_v2.py:231-233`; `exp_final_a100.py:220-222`. Variant: `exp2_dpo_training.py:203-206` also 0.7/0.3 | DIFFER | AGREE | AGREE |
| 9.8 | Tier sentences | v1: "I'm confident this is correct.", "This should work, but please verify edge cases.", "I'm not sure about this -- please review carefully." (l.153-155). v2: "I'm confident this is correct", "This should work, but please verify edge cases", "I'm not confident---please review carefully" (l.632). v3: same as v2 (l.205, appendix l.682-691) | v1 code: `CONF_HIGH` "I am confident this solution is correct. The logic handles the requirements and edge cases well.", `CONF_MED` "This solution should work for most cases, but please verify edge cases. There may be subtle issues I'm not certain about.", `CONF_LOW` "I am not confident in this solution. It may contain bugs or miss important edge cases. Please review carefully before using." (`run_all_v2.py:204-206`; `prompts/v2_run_all_v2_conf_labels.txt`). v2 and v3 adapter: `exp_final_a100.py:136-138`, with a shorter `CONF_MED` ending "There may be subtle issues." (`prompts/v2_exp_final_a100_conf_labels.txt`). The evaluation parser tests for `'i am confident this solution is correct'`, the code wording | DIFFER | DIFFER | DIFFER |
| 9.9 | Numeric value of each tier | v3: 0.9, 0.6, 0.3 (l.205). v1, v2: none | 0.9 / 0.6 / 0.3 in `extract_trained_conf` (`exp_v3_all.py:168-173`) | ABSENT (text) | ABSENT (text) | AGREE |
| 9.10 | Pair construction (preference data) | v1: 228 pairs: 133 calibrated-high vs underconfident, 64 correct-calibrated vs incorrect-overconfident, 31 calibrated-low vs overconfident (l.158) | three pair types per problem from the 10 samples (`run_all_v2.py:240-261`): (a) `correct_calibrated_vs_incorrect_overconfident`: first correct sample with the true tier sentence vs first incorrect sample with `CONF_HIGH` (needs both kinds of sample); (b) `calibrated_low_vs_overconfident`: for low or medium problems, first incorrect sample with the true tier vs a second incorrect sample with `CONF_HIGH`; (c) `calibrated_high_vs_underconfident`: for high problems, first correct sample with `CONF_HIGH` vs a second correct sample with `CONF_LOW`. The type names match the text; counts 133/64/31 and the 228 total: not located (pair file is remote only) | AGREE (scheme); counts not located | n/a | n/a |
| 9.11 | SFT target (v1) | v1: SFT on the calibrated (chosen) responses (l.158) | `sft_data` is built from the `chosen` field of the pairs (`run_all_v2.py:319-320`); 90/10 split, seed 42 (`:322`) | AGREE | n/a | n/a |
| 9.12 | SFT dataset construction (v2, v3) | v2: 274 examples, "each response includes a verbal confidence tier matched to the empirical pass rate" (l.632). v3: same (l.205, l.618) | up to two examples per problem (`exp_final_a100.py:228-241`): `correct_calibrated` (first correct sample's code with the tier sentence of the pass rate) if any sample passed; `incorrect_honest` (first incorrect sample's code with `CONF_LOW`) if some sample failed and the pass rate < 0.5. Incorrect code therefore appears as a training target. Total 274 = 246 train + 28 eval in `results/v2/sft_training_metrics.json`. Pass rate from 10 samples at tau 0.8 (`:214-218`) | n/a | AGREE (count, tiers); incorrect_honest examples ABSENT (text) | AGREE (count, tiers); incorrect_honest examples ABSENT (text) |
| 9.13 | Train / eval split of the SFT data | not stated (v2 l.634 quotes an eval loss of 0.86) | `train_test_split(test_size=0.1, seed=42)` over examples (`exp_final_a100.py:257`); stored final eval loss 0.856 | n/a | ABSENT (text) | ABSENT (text) |
| 9.14 | SFT evaluation protocol | v2: sampling and verbal confidence of base and SFT models on 80 problems (l.634-655) | SFT model is queried with a system + user instruction (3.8) at tau 0.1; the base model is queried with the 3.10 prompt; both answers are parsed with `extract_trained_conf` in `sft_eval_only.py:126` (both branches of the conditional call the same function), so trained-phrase tests run before the numeric regex on base outputs | n/a | ABSENT (text) | ABSENT (text) |
| 9.15 | Two separate evaluations of one adapter | v3 Tab. 5 uses `results/v2/sft_evaluation.json`; v3 Tab. 6 uses `results/v3/sft_discrimination.json` | `sft_eval_only.py` (R2-SFTE: SFT confidences 0.9 x 76, 0.6 x 4) and `exp_v3_all.py:401-466` (R3-S: 0.9 x 79, 0.3 x 1) are separate sampling runs over the same `humaneval[:80]` | n/a | n/a | ABSENT (text) |

## 10. Random seeds

No seed is set for generation in any v1-v3 script: no `torch.manual_seed`, `set_seed`, or `seed=` argument appears near a `generate` call (searched `src/v1_baseline`, `src/v2_comprehensive`, `src/v3_multimodel`). The Trainer configs (`SFTConfig`, `DPOConfig`) do not pass `seed`. None of the three manuscripts states any seed.

| File:line | Value | What it seeds | v1 text | v2 text | v3 text |
|---|---|---|---|---|---|
| `exp_v2_comprehensive.py:54` (default arg), `:56` | 42 | `np.random.RandomState` for bootstrap resampling | n/a | ABSENT | n/a |
| `exp_final_a100.py:47` | 42 | bootstrap `RandomState` (n=20, SFT evaluation) | n/a | ABSENT | n/a |
| `sft_eval_only.py:36` | 42 | bootstrap `RandomState` (SFT evaluation) | n/a | ABSENT | n/a |
| `exp_v3_all.py:100` | 42 | bootstrap `RandomState` (v3 main table) | n/a | n/a | ABSENT |
| `exp_v3_all.py:353` | 42 | `KFold(n_splits=5, shuffle=True, random_state=42)` for isotonic and Platt | n/a | n/a | ABSENT |
| `exp_v3_multimodel.py:70-71` | 42 | bootstrap, variant | n/a | n/a | n/a |
| `run_all_v2.py:277` | 42 | `train_test_split` of DPO pairs | ABSENT | n/a | n/a |
| `run_all_v2.py:322` | 42 | `train_test_split` of SFT examples (v1 pairs) | ABSENT | n/a | n/a |
| `exp_final_a100.py:257` | 42 | `train_test_split` of SFT examples (v2/v3 adapter) | n/a | ABSENT | ABSENT |
| `exp2_dpo_training.py:305,418` | 42 | `train_test_split`, APPS variant | n/a | n/a | n/a |
| generation (all) | none | token sampling is not seeded; repeated runs differ | ABSENT | ABSENT | ABSENT |

For the seeds of `src/v4_dprc` see section 11.5.

## 11. src/v4_dprc

No manuscript (v1, v2, v3) cites `src/v4_dprc`; there is no manuscript statement to compare against, so
no AGREE/DIFFER marks are assigned in this section. It is the code for a planned extension named DPRC. Every statement
below is from `src/v4_dprc/README.md` (cited as `README:N`) or the code.

### 11.1 What it was designed to do

DPRC ("Decoupled Per-Requirement Confidence for code LLMs", `README:1`) turns the diagnostic
calibration-disconnect study into a prescriptive method: train a 7B code LLM to self-express
calibrated, discriminative confidence at per-test-case or per-requirement granularity, to localize
which requirement its own solution will fail (`README:3-5`). `README:6` points to a research note
under `research/notes/` (present in the repository; not analyzed here). Frozen settings are in
`config.py`, with the stated aim of landing in a reproducibility checklist (`README:63-65`,
`config.py:1-4`).

### 11.2 Stages as designed, and where each lives

| Stage | Purpose | Code | Key settings |
|---|---|---|---|
| Phase 0 | box bootstrap (venv, pinned dependencies, cache warm-up, CPU self-tests) | `setup_lambda.sh` | not analyzed further |
| Phase 1 labeling | sample n + 1 solutions, execute each test separately, build per-group targets and labels | `label_dataset.py:23-70`; `sampling.py`; `pertest_harness.py`; `grouping.py`; `serialization.py` | `N_SAMPLES = 10`, `N_LABEL_EXTRA = 1` (independent 11th sample is the evaluation label source), `TEMPERATURE = 0.8`, `TOP_P = 0.95`, `MAX_NEW_TOKENS = 512`, `EXEC_TIMEOUT = 10` s per test (`config.py:28-33`); vLLM `SamplingParams(..., seed=config.SEED)` (`sampling.py:74`) or HF `generate` (`sampling.py:97-120`); chunked in 40 problems (`label_dataset.py:24`) |
| Per-test execution | one subprocess per (solution, test), thread pool; canonical solution run twice per test to discard flaky or broken tests | `pertest_harness.py:110-170` (`DEFAULT_TIMEOUT = 10`, line 32), `discard_flaky` at `:177-193` (`runs=2`) | uses `sys.executable`, temp file, hard timeout; HumanEval `check()` is split at top-level asserts (loop-based checks stay one unit, `:18-19`) |
| Grouping | L1 = each test is a group; L2 = category from the literals in the test input (`empty_or_zero`, `negative`, `large`, `typical`, `other`; large = abs value >= 1,000,000, string >= 200 chars, or container >= 50 elements) | `grouping.py:22-23,26-106` | training target of a group = mean pass over all solutions and tests in the group; per-solution label = passes every test in the group (`per_group_pass_rate`, `grouping.py`, docstring and body) |
| Data pool | mixture of sources, at least 3 tests per problem, pool target 3,000 | `config.py:36-40`; `loaders.py` (HumanEval, MBPP sanitized, APPS introductory, TACO, LiveCodeBench, BigCodeBench v0.1.2) | `POOL_MIX = {mbpp: 0.15, taco: 0.65, livecodebench: 0.20}` (APPS dropped, comment at `config.py:38`); LiveCodeBench windows `LCB_TRAIN_WINDOW = (None, "2024-06-30")`, `LCB_EVAL_WINDOW = ("2024-09-01", None)` (`config.py:43-44`) |
| Confidence block | model emits `CONFIDENCE:` then `REQ <group>: <digit>`; scalar confidence = expected digit / 9 | `conf_block.py:3-17,48-53`; readout in `pilot.py:26-57` | `c_g = (sum_k k * p(digit=k)) / 9`; Brier loss `mean_g (c_g - t_g)^2` (`conf_block.py:12-17`); discrete buckets `CONF_BUCKETS` (`config.py:75`) |
| Stage (a) training | LoRA SFT of the confidence block on continuous per-group targets, loss only on the completion | `train_dprc.py:30-64` (data), `:75-111` (train), `:114-156` (Brier trainer) | LoRA r = 16, alpha = 32, dropout 0.05, seven projection targets; 3 epochs; lr 2e-5; batch 1, accumulation 16; max length 2048; cosine; seed 42 (`config.py:51-60`, `train_dprc.py:92-100`). Example target per group = `0.5 * per_solution_satisfaction + 0.5 * group pass rate` (`:36,54`), digit = `round(9 * target)` (`conf_block.py:33-35`), at most 3 solutions per problem (`:30`). `--loss ce` is the default; `--loss brier` adds a Brier term over the ten digit logits to the LM loss, and its target is the teacher digit divided by 9 (`:149`), not the continuous target listed in `examples[...]["targets"]` (`:62`) |
| Pilot and GATE-2 | elicit per-group confidence from the trained model on held-out labeled problems, compute pooled per-requirement AUROC with a problem-level bootstrap, localization precision at 1 | `pilot.py:67-104` (`evaluate`, `gate2`); `metrics.py:86-151` | gate: L1 AUROC > 0.65 gives headline L1, else L2 AUROC > 0.65 gives L2, else L3 (`config.py:67`, `pilot.py:87-104`); amber 0.63 (`config.py:68`); `PILOT_N_PROBLEMS = 300` (`config.py:69`) is not referenced elsewhere in `src/` |
| Gates 0 and 1 | GATE-0: extrapolated execution wall clock <= 2.0 days and GPU budget <= 375 USD; GATE-1: >= 1,500 problems (scaled for partial runs) and intermediate-target spread fraction >= 0.20 | `label_dataset.py:73-98`; `config.py:63-66` | targets "intermediate" means in (0.1, 0.9) per the comment at `config.py:66` |
| Metrics | ECE, TACE, Brier, AUROC, flat bootstrap, and a problem-level grouped bootstrap | `metrics.py` (scalar functions stated to be copied verbatim from `exp_v3_all.py:62-117`, and the code matches) | 1,000 replicates, percentile `int(0.025 * B)` / `int(0.975 * B)`, seed 42 (`metrics.py:59,99,127`) |
| Stage (b) | masked-gradient decoupled RL refinement | not built (`README:56-61`) | none |
| Phases 3 to 5 | full two-model run, six ablations, selective-generation floor | not built (`README:60-61`) | none |
| Additional analyses (BigCodeBench-based, not in the README module map) | `hidden_probe.py` (hidden-state probe), `repair_derisk.py` (targeted repair vs regeneration; prompts in `prompts/v4_repair_derisk_*.txt`), `test_adequacy.py` (self-written tests vs code competence; uses `selftests.py`), `type_effect.py` (requirement-type ANOVA), `type_requirements.py` (type labeling prompt), `selftests.py` (model-written unit tests) | defaults point to a `/workspace/...` box layout (e.g. `hidden_probe.py:156`, `type_requirements.py:40-43`) | print to stdout only; none writes under `results/v4_dprc` |

The models are `Qwen/Qwen2.5-Coder-7B-Instruct` (primary) and `deepseek-ai/deepseek-coder-6.7b-instruct`
(`config.py:21-25`). The config comments state that the sampling settings match the v3 harness
(`config.py:27`).

### 11.3 Status as found in the repository

| Item | State | Evidence |
|---|---|---|
| `data/v4_dprc/labels/` | holds only `labels_dryrun.jsonl` (5 lines) and `labels_dryrun_manifest.json` | directory listing |
| Dry-run content | 5 HumanEval problems (`humaneval/HumanEval/0` to `/4`), 23 groups, spread fraction 0.1304 (below the 0.20 threshold in `config.py:66`), `gen_secs` 0.0, `exec_secs` 3.07, 253 executions, 82.5 executions per second. Each problem has 10 solutions but only 2 distinct strings (the canonical solution and one perturbation) | manifest; record fields; `StubGenerator` at `sampling.py:123-147` (every fourth sample is perturbed); the records carry no model field |
| `data/v4_dprc/adapters/` | empty | directory listing |
| `results/v4_dprc/` | empty; no v4 module writes there (analysis modules print to stdout). Both directories are created at import by `config.py:17-18` | directory listing; code search |
| Real Phase-1 labels, stage-(a) adapters, GATE-2 pilot, hidden-state probe, repair de-risk, self-tests, requirement typing, test adequacy, type effect | no output files exist | repository search |
| README claim of status | "Tested" means verified on a laptop (CPU); the GPU paths are "written and import-clean but run first on the box" (`README:25-26`) | `README:25-26` |
| Numbers quoted without a backing file | the `hidden_probe.py` docstring cites AUROC 0.805 (oracle) and 0.603 (digit readout) (`hidden_probe.py:3-4`) | no result file in the repository holds them |

README and code mismatches found while reading:

- `README:37` lists `apps` among the Phase-1 sources; `config.POOL_MIX` drops APPS (`config.py:38-40`).
- The README module map (`README:10-23`) omits `hidden_probe.py`, `repair_derisk.py`, `test_adequacy.py`, `type_effect.py`, `type_requirements.py`, and `selftests.py`.
- `train_dprc.py --dataprep-only` reads `ex[0]["text"]` (`:173`) and asserts `"CONFIDENCE:" in e["text"]` (`:175`), but `build_sft_examples` returns dictionaries with `prompt`, `completion`, `groups`, and `targets` keys (`:58-63`).
- `README:43` names the adapter directory `dprc_qwen2.5-coder-7b_l1_ce`, which matches `train_dprc.py:94`; no such directory exists.

### 11.4 Benchmarks, splits, and held-out data in v4

Sources are loaded per test (`loaders.py`). Splits: LiveCodeBench has disjoint train and evaluation
date windows (`config.py:43-44`); the BigCodeBench analyses take `--labels`/`--train`/`--test` files
whose producer is not in the repository (`hidden_probe.py:156`, `BUNDLE_MAP` section 4). The pilot
reads a "held-out slice" file (`README:43`); no script creates it.

### 11.5 Seeds in v4

| File:line | Value | Scope |
|---|---|---|
| `config.py:60` | 42 | `SEED`, used by `sampling.py:74` (vLLM) and `train_dprc.py:100` (Trainer) |
| `metrics.py:59`, `:99` | 42 | default `seed` of `bootstrap_all` and `bootstrap_grouped`; `RandomState(seed)` at `:62` and `:107` |
| `pilot.py:118` | 0 | `RandomState` for the synthetic self-test |
| `hidden_probe.py:73`, `:139` | 0 | `RandomState` in the probe code |
| `test_adequacy.py:118` | 0 | `RandomState` in its self-test |


## 12. Summary table

One row per element and version. The mark follows the rule in section 0 (DIFFER if any sub-item differs, else AGREE if any agrees, else ABSENT). The tally counts sub-item rows of sections 1 to 10 for that element and version (A = AGREE, D = DIFFER, B = ABSENT; `n/a` rows are not counted). `src/v4_dprc` has no manuscript and is not scored.

| Element | Version | Mark | Tally (A / D / B) | Sub-items driving the mark |
|---|---|---|---|---|
| 1. Benchmarks, splits, held-out subset | v1 | AGREE | 3 / 0 / 3 | AGREE: 1.1, 1.2, 1.6 |
| 1. Benchmarks, splits, held-out subset | v2 | DIFFER | 5 / 1 / 2 | DIFFER: 1.7 |
| 1. Benchmarks, splits, held-out subset | v3 | AGREE | 5 / 0 / 2 | AGREE: 1.1, 1.2, 1.4, 1.6, 1.8 |
| 2. Models and checkpoints | v1 | AGREE | 1 / 0 / 5 | AGREE: 2.1 |
| 2. Models and checkpoints | v2 | DIFFER | 2 / 1 / 3 | DIFFER: 2.5 |
| 2. Models and checkpoints | v3 | AGREE | 3 / 0 / 3 | AGREE: 2.1, 2.2, 2.5 |
| 3. Prompts and instruction formats | v1 | DIFFER | 0 / 1 / 6 | DIFFER: 3.3 |
| 3. Prompts and instruction formats | v2 | DIFFER | 2 / 3 / 6 | DIFFER: 3.3, 3.4, 3.5 |
| 3. Prompts and instruction formats | v3 | DIFFER | 2 / 1 / 6 | DIFFER: 3.3 |
| 4. Sampling parameters and counts | v1 | AGREE | 4 / 0 / 6 | AGREE: 4.1, 4.2, 4.8, 4.9 |
| 4. Sampling parameters and counts | v2 | AGREE | 5 / 0 / 6 | AGREE: 4.1, 4.2, 4.4, 4.8, 4.10 |
| 4. Sampling parameters and counts | v3 | AGREE | 6 / 0 / 5 | AGREE: 4.1, 4.2, 4.3, 4.4, 4.8, 4.10 |
| 5. Execution harness and correctness label | v1 | DIFFER | 2 / 2 / 3 | DIFFER: 5.2, 5.4 |
| 5. Execution harness and correctness label | v2 | DIFFER | 4 / 2 / 3 | DIFFER: 5.2, 5.8 |
| 5. Execution harness and correctness label | v3 | DIFFER | 4 / 1 / 3 | DIFFER: 5.2 |
| 6. Confidence-estimation methods | v1 | DIFFER | 2 / 1 / 4 | DIFFER: 6.1 |
| 6. Confidence-estimation methods | v2 | DIFFER | 3 / 1 / 3 | DIFFER: 6.3 |
| 6. Confidence-estimation methods | v3 | DIFFER | 6 / 2 / 1 | DIFFER: 6.3, 6.6 |
| 7. Calibration and discrimination metrics | v1 | AGREE | 6 / 0 / 0 | AGREE: 7.1, 7.2, 7.3, 7.5, 7.6, 7.8 |
| 7. Calibration and discrimination metrics | v2 | AGREE | 5 / 0 / 1 | AGREE: 7.1, 7.2, 7.3, 7.5, 7.6 |
| 7. Calibration and discrimination metrics | v3 | DIFFER | 5 / 2 / 1 | DIFFER: 7.4, 7.5 |
| 8. Confidence intervals and bootstrap | v1 | ABSENT | 0 / 0 / 0 | neither the v1 text nor the v1 code computes intervals |
| 8. Confidence intervals and bootstrap | v2 | AGREE | 3 / 0 / 2 | AGREE: 8.1, 8.2, 8.3 |
| 8. Confidence intervals and bootstrap | v3 | AGREE | 2 / 0 / 4 | AGREE: 8.1, 8.3 |
| 9. SFT and DPO training | v1 | DIFFER | 5 / 2 / 4 | DIFFER: 9.7, 9.8 |
| 9. SFT and DPO training | v2 | DIFFER | 5 / 1 / 6 | DIFFER: 9.8 |
| 9. SFT and DPO training | v3 | DIFFER | 5 / 1 / 6 | DIFFER: 9.8 |
| 10. Random seeds | v1 | ABSENT | 0 / 0 / 3 | ABSENT only |
| 10. Random seeds | v2 | ABSENT | 0 / 0 / 5 | ABSENT only |
| 10. Random seeds | v3 | ABSENT | 0 / 0 / 4 | ABSENT only |

Element-by-version marks (30 rows): AGREE 11, DIFFER 15, ABSENT 4.
Sub-item marks across sections 1 to 10 (counted per version column): AGREE 95, DIFFER 22, ABSENT 106.

### Most consequential DIFFER and ABSENT entries

Ranked by how much each would change a reported number or the meaning of a label. Each entry is a
fact about where text and code diverge; none says which is correct.

1. **v1 label definition (5.4).** The text defines the label as the single deterministic tau = 0.1 generation, the same one used for the verbal rating (v1 l.126). The code labels with the first of the ten tau = 0.8 samples (`exp1_optimized.py:134`; `run_all_v2.py:171`), which is also one of the samples that form the sampling confidence. This changes the meaning of every v1 ECE, Brier, and AUROC value.
2. **Log-probability transform (6.3).** The text defines `sigma(mean log p)` (v2 l.130, v3 l.140); the producers compute `exp(mean log p)` (`exp_v2_comprehensive.py:191`, `exp_v3_all.py:208`). Stored arrays checked (R2-HE, R2-MB, R3-Q, R3-D) lie between 0.59 and 0.999, which a sigmoid of a non-positive number cannot produce. ECE and Brier of the log-prob rows (and the isotonic and Platt rows built on them) depend on the transform; AUROC does not under any monotone map. The non-producing `exp_v3_multimodel.py:233` implements the sigmoid.
3. **Which generation each confidence describes (6.3, 4.9, 5.4).** Log-prob confidence comes from an extra fresh sample, and verbal confidence from a separate tau = 0.1 response whose code is never executed, while the label comes from the first sample (v1, v2) or an independent 11th sample (v3). The texts do not say so (ABSENT), and the pairing of confidence and label is across different generations.
4. **AST proxy formula (6.6).** Text: largest-cluster share with variable-name normalization. Code: `max(0, 1 - (K - 1)/9)` over distinct `ast.dump` strings with identifiers kept. Affects the reported AST ECE 0.351 and AUROC 0.689 rows in v3.
5. **Verbal prompts (3.3 to 3.5).** The quoted and appendix prompts (including "Only output the number") are not the prompts in the code, which ask for `CONFIDENCE: [N]` followed by a full solution in one response. This holds for v1, v2 (all three strategies), and v3. It changes what the verbal numbers measure.
6. **MBPP execution (5.8).** The v2 text describes signature enforcement and validation; the code runs the raw program, then aliases the first `def` to the expected name. The v1 MBPP producer has no fix at all (`run_all_v2.py:54-58`). This bears on MBPP pass@1 (0.066 vs 0.588) and every MBPP calibration number.
7. **"Held-out" SFT evaluation (1.7).** v2 calls the 80-problem set held-out; the SFT data was generated from all 164 problems, so the 80 problems are in the training source (example-level 90/10 split, seed 42). Bears on the SFT ECE reduction in v2 Tab. 5 and v3 Tab. 5.
8. **SFT data and readout (9.8, 9.12, 9.14).** Tier sentences in the code are longer than those quoted in all three texts; the code adds `incorrect_honest` examples (incorrect code with the low-confidence sentence) that the texts do not mention; the SFT evaluation parses base-model answers with the SFT phrase tests first. These shape the SFT confidence distribution (0.9 for 95 percent of problems) and the base-vs-SFT contrast.
9. **Verbal parsing and defaults (6.8, 6.2 table).** The texts say nothing about the regex or fallbacks. Unparsed responses silently map to 0.6, with a different keyword ladder per script, so the 0.6 bin mixes ratings and parse failures; CoT and critique responses can be truncated at 512 tokens before the rating.
10. **n = 20 sensitivity run (4.10).** The row comes from `exp_final_a100.py` with its own extractor and verbal prompt; its stored `pass_at_1` is 0.0875 against 0.90 to 0.95 for the other subset runs. Neither text mentions the separate provenance.
11. **TACE definition (7.4).** Text: unweighted mean over equal-mass bins above a minimum sample count. Code: floor(sqrt n) equal-count bins, weighted by bin share, a bin counted only if its gap exceeds 0.01, not divided by the number of retained bins. Affects the v3 TACE column.
12. **v1 SFT tier threshold (9.7).** v1 text high >= 0.8; code >= 0.7. The v2 and v3 texts (0.7) match the code.
13. **Label protocol for the SFT tables (5.5).** SFT tables use first-sample labels (`sft_eval_only.py:129`, `exp_v3_all.py:436`), while the v3 Method describes independent labels; v3 does not say which applies to its SFT tables.
14. **Reported Brier and AUROC are bootstrap means (7.8).** ECE and TACE are full-sample values; Brier and AUROC in the stored v2 and v3 files are means of 1,000 resamples. The texts do not say.
15. **Generation is unseeded (10).** No seed is set for sampling in v1-v3 and none of the manuscripts mentions one; bootstrap, `KFold`, and `train_test_split` use seed 42. Reruns would not reproduce the stored samples. Also noted but not ranked: the 10-second timeout applies per script, not per test (5.2), in all three versions.

### Changes between versions that agree with their own code

These are not text-vs-code differences, but they change what a label or a metric means from one
manuscript to the next: the label moves from "first sample" (v2) to an "independent 11th sample" (v3);
v3 adds an AST proxy, post-hoc calibrators, TACE, and a second model; v3 drops MBPP and the critique and CoT strategies.

### Items stated by a text and not located in the repository

- the 228 pairs and the 133/64/31 split (v1 l.158): the pair file is remote only;
- the "40960 MiB" GPU memory string and "scikit-learn 1.4" (v3 l.698-707): `harness_info.json` records 42.4 GB and no scikit-learn version;
- the GH200 hardware statement for the v1 and v2 runs: no run record exists, and `exp_final_a100.py:1-6` states A100;
- any model revision or commit hash (none in text or code).
