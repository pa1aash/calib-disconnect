# Conformance audit: frozen design against the pipeline code

Design: `docs/s7/PIPELINE_DESIGN_FROZEN.md` (line numbers below refer to it). Binding sections audited: 4, 5, 6, 7 (7.1 to 7.12), 8, 9, 13, and the parts of 1.2 to 1.6 that the code computes. Sections 2, 3, 10, 11, 12, 14 to 17 are not audited except where a binding row depends on them.

Method: every row was checked by reading the implementing function, not its name. "Test" names the test that covers the row, as `path::test_name`; "none" means no test exercises the row as stated.

Test run: NOT RUN. This audit session had read, search, and write tools only and no shell, so `uv run pytest` was not executed. Test names come from reading the test files; whether they pass was not verified. Findings marked "suspected" were not confirmed by execution.

Status: MET, PARTIAL (implemented with a gap or an unlogged departure), GAP (not implemented), DIVERGENT (implemented differently from the design).

## Section 1 (parts the code computes)

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 1.2a | Gamma(x) = M_d(P^(l), y^(l)) - M_d(S^(r,t,l), y^(l)); M_0 pooled AUROC, M_1 = W; positive means probe ahead (116-120) | analysis/gap.py:125 (`discrimination_cells`), :116 (`cell_roles`), :74 (`stated_name`) | tests/analysis/test_shapley_gap_routing.py::test_cells_match_direct_and_r_is_null_at_d1 | MET |
| 1.2b | All 16 cells on one problem set valid under both suites; every supervised readout of the game fit on that population (175, 558) | Scoring restricted: analysis/stage.py:135 (`valid_lv_problems`), :533. Fitting not restricted: pipeline/readouts/common.py:118 | none | PARTIAL (G1) |
| 1.2c | Tie rule: recalibrated score ranked by (isotonic value, pre-map score) (122) | analysis/ranking.py:20 (`lex_keys`); pipeline/readouts/isotonic.py:81-84 | tests/analysis/test_metrics.py::test_equal_score_different_tiebreak_not_a_tie; ::test_W_invariant_to_monotone_map_with_tie_rule; tests/readouts/test_readouts_fits.py::test_isotonic_tie_rule_clip_and_values | MET |
| 1.2d | Tie rates with and without the rule reported; the no-tie-break variant is a sensitivity analysis (122) | analysis/gap.py:296 (`tie_rates`); analysis/metrics.py:493-495, 512 (per-readout no-tie-break values). No budget recomputed without the tie-break | none | PARTIAL (G6) |
| 1.2e | G0 = Gamma(0,0,0,0); R = Gamma(1,1,1,1); R_pool = Gamma(1,1,0,1) (124-134) | analysis/shapley.py:33 (keys "rtdl"); analysis/stage.py:634-636 ("1101") | tests/analysis/test_shapley_gap_routing.py::test_model_budget_and_pooling_runs | MET |
| 1.2f | At t = 1, r = 1 the map is fit on inner-cross-fitted training-fold scores; no test-fold score enters a map (112) | pipeline/readouts/stage.py:319-320; pipeline/readouts/recipe.py:230 (`inner_cross_fit`); isotonic.py:71 | tests/readouts/test_readouts_recipe.py::test_final_adapter_uses_step_transfer_and_inner_adapter_counts; tests/readouts/test_readouts_fits.py::test_isotonic_train_scores_replace_own_scores | MET |
| 1.3a | Diagnostic split of d: pooled AUROC on mixed problems and fold-averaged pooled AUROC beside phi_d (144) | analysis/gap.py:235 (`d_diagnostics`); metrics.py:465-478 | tests/analysis/test_metrics.py::test_d_diagnostics_hand; tests/analysis/test_shapley_gap_routing.py::test_l_and_d_diagnostics_consistent | MET |
| 1.3b | Diagnostic split of l at (1,1,1): refit step, relabel step, W on problems mixed under both suites (146) | analysis/gap.py:259 (`l_diagnostics`) | tests/analysis/test_shapley_gap_routing.py::test_l_and_d_diagnostics_consistent | MET |
| 1.3c | r x t interaction index and pooled AUROC of S^T with and without the map at t = 1 (156) | analysis/gap.py:283 (`rt_diagnostics`); shapley.py:70 | tests/analysis/test_shapley_gap_routing.py::test_model_budget_and_pooling_runs | MET |
| 1.3d | Budget recomputed with V2 as the zero-shot readout (152) | analysis/budget.py:64-82; analysis/stage.py:579 | tests/analysis/test_stage.py::test_stage_k3_switch_and_dry_run | MET |
| 1.3e | R against each probe-family member; R at LoRA ranks 1, 4, 16 and the LoRA-plus-head control (153-154) | not located in analysis/ | none | GAP (G6) |
| 1.3f | Strata: contamination, family, scale, base vs instruct, reasoning, coder; stratum-by-term table (148-150, 240) | not located | none | GAP (G5) |
| 1.4a | Shapley values with exact weights over N = {r,t,d,l}; efficiency G0 + sum phi = R (166-172) | analysis/shapley.py:54 (`shapley_values`), :104 (`shapley`, efficiency assert :113-115) | tests/analysis/test_shapley_gap_routing.py::test_shapley_weights_hand; ::test_shapley_efficiency_property | MET |
| 1.4b | Game at fold seed 0; R^(0) shown beside R_bar with R_bar - R^(0) (173) | analysis/stage.py:637-640 | none specific | MET |
| 1.4c | phi_t split into format step and training step at (1,1,1) and in both orders, paired intervals (174) | analysis/shapley.py:157 (`readout_change_split`), :177 (`SPLIT_POSITIONS`); budget.py:72-82 | tests/analysis/test_shapley_gap_routing.py::test_readout_change_split_hand | MET |
| 1.4d | Share of pairs tied by V1 imputation reported beside G0 (174) | analysis/gap.py:309; metrics.py:263 | tests/analysis/test_metrics.py::test_imputation_tie_share_hand | MET |
| 1.4e | Pairwise Shapley interaction indices for the six pairs (176) | analysis/shapley.py:70 | tests/analysis/test_shapley_gap_routing.py::test_shapley_unanimity_game_hand | MET |
| 1.4f | Sequential decompositions, labels first (l,d,t,r) and readout first (r,t,d,l) (178-181) | analysis/shapley.py:29-30, :86 | tests/analysis/test_shapley_gap_routing.py::test_shapley_additive_game_hand | MET |
| 1.5a | Delta Gamma_g at r = 0 for d, l in {0,1}; cross contrast; probe shift; mixed-both at d = 1; pass rate, mixed count, extraction-failure rate per set (194-198) | analysis/generation_shift.py:51 (`contrasts`), :75 (`set_rates`); analysis/stage.py:376 | tests/analysis/test_shapley_gap_routing.py::test_generation_shift_identical_sets_give_zero; tests/analysis/test_stage.py::test_stage_generation_shift_and_reconciliation | MET |
| 1.5b | Fresh set (g = 1) scored by S^R from its own suffix and by the same fitted probe through a base-weights pass with the V2 turn (191) | not located: no producer writes fresh-set scores | none | GAP (G4) |
| 1.5c | Readout-format contrast S^R vs S^T at g = 0 in the reconciliation table (202) | not located in analysis/ | none | GAP (G6) |
| 1.6a | R_bar = mean over P1..P6 of R_m; one problem-clustered paired bootstrap (206) | analysis/decisions.py:233 (`primary_report`); refit.py:26, :36 | tests/analysis/test_inference.py::test_primary_report_and_k4 | MET |
| 1.6b | D1, D2, D3 on the 90 percent interval, mutually exclusive, else inconclusive (208-216) | analysis/decisions.py:49 (`classify_interval`) | tests/analysis/test_inference.py::test_decision_rules_hand; ::test_decisions_mutually_exclusive; ::test_classify_boundaries | MET |
| 1.6c | delta = 0.03 applied once (218) | pipeline/contracts/constants.py:15 | tests/contracts/test_contracts.py::test_design_values | MET |
| 1.6d | Decisions also at 0.02 and 0.05, labeled sensitivity (228) | constants.py:16; analysis/decisions.py:251-252 | tests/analysis/test_inference.py::test_primary_report_and_k4 | MET |
| 1.6e | R_pool gets the three decisions at a pooled margin of 0.03, secondary, no refit component (230) | analysis/decisions.py:289 (`pooled_residual_report`), :84 | none specific | MET |
| 1.6f | Conventional bounds (R_bar > 0, < 0) beside, labeled secondary; decision interval includes refit variance (216) | analysis/decisions.py:76-81 | tests/analysis/test_inference.py::test_decision_rules_hand | MET |

## Section 4: Benchmarks

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 4a | Every benchmark file pinned by URL, revision, SHA-256 (543) | pipeline/data/pins.py | tests/data/test_data_pins.py::test_pins_match_manifest; ::test_verify_file_detects_changes | MET |
| 4b | MBPP+ v0.2.0 with the pinned patch; 459, 102, 559 recomputed; patched-file SHA-256 in the manifest (549, 552) | pipeline/data/stage.py:211-215; pipeline/data/evalplus_data.py | tests/data/test_data_evalplus.py::test_patch_equals_pinned_fix_script_and_changes_exactly_three | MET |
| 4c | Label-validity population: problems valid under both suites; every supervised readout of the game fit on it only (558) | Scoring: analysis/stage.py:135, :533. Fitting: pipeline/readouts/common.py:113-118 uses per-suite labels; pipeline/execute/labels.py:81-82 drops only the excluded (problem, suite) pair; pipeline/data/stage.py:196-199 builds folds over all problems | none | DIVERGENT (G1) |
| 4d | LiveCodeBench: three toggles (r, t, d), label toggle replaced by a public-vs-label-suite analog, fit on LiveCodeBench folds only (559) | analysis/stage.py:67 (four-player game with "lcb_public", "lcb_label"); pipeline/readouts/stage.py:58-59 | none | PARTIAL (G15) |
| 4e | Contamination windows: LiveCodeBench problems classified by contest_date against each model's count date; stratum per model and Olmo/Gemma pooled (561-574) | constants.py:161 (`COUNT_DATES`) only; no classifier or stratum budget located | none | GAP (G5) |
| 4f | Near-duplicate groups (AST-identical or prompt Jaccard >= 0.8), one fold per group by hash of smallest ID under every seed, listed in the manifest (575) | pipeline/data/folds.py:81, :127; pipeline/data/stage.py:191-202 | tests/data/test_data_folds.py::test_cross_benchmark_pairs_are_grouped_and_key_is_smallest_id; ::test_group_uses_group_key_even_when_key_problem_is_absent; ::test_humaneval_pairs_are_counted_not_grouped | MET |
| 4g | HumanEval/MBPP agreement inputs: seeded TypedMutGen, contract filter, dedup by canonical repr (6 significant digits), cap 50, removed counts and label-proxy share reported (579-583) | pipeline/data/agreement.py:128; pipeline/data/inputs.py:81; pipeline/execute/labels.py:169 | tests/data/test_data_agreement.py::test_deterministic_per_seed_and_disjoint_from_label_inputs; tests/data/test_data_inputs.py::test_float_rounding_to_six_significant_digits; tests/execute/test_execute_sandbox.py::test_agreement_signatures_and_label_proxy | MET |
| 4h | LiveCodeBench: SHA-256 of each private input selects 20 percent for agreement; labels use public + 80 percent; no public test in agreement; zero-input problems missing, counted (584-588) | pipeline/contracts/hashing.py:57; pipeline/data/stage.py:176-185; pipeline/readouts/unsupervised.py:116-121 | tests/contracts/test_contracts.py::test_lcb_agreement_split_counts; tests/data/test_data_lcb.py::test_zero_agreement_inputs_get_empty_suite; ::test_zero_agreement_counted_by_store | MET |
| 4i | Labeling sensitivity on the full official suite, without the agreement readout (586) | readouts fit "lcb_full" (pipeline/readouts/stage.py:59); no analysis of it located | none | PARTIAL (G6) |

## Section 5: Generation

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 5a | Temperature 1.0, top-p 1.0, no top-k, no repetition penalty, stop at end of turn; card recommendations recorded, not used (594-598) | pipeline/generate/backends.py:224-245 (`generation_config="vllm"`) | tests/generate/test_backends.py::test_vllm_backend_settings; ::test_sampling_follows_the_softmax_at_temperature_one | PARTIAL (G22) |
| 5b | k = 10, or 20 under the k rule with samples 11..20 added by the same seed rule, 1..10 unchanged (600) | pipeline/generate/requests.py:86; pipeline/generate/stage.py:143 (`_chunks`) | tests/generate/test_requests.py::test_k_extension_leaves_samples_1_to_10_unchanged; tests/generate/test_stage.py::test_k_extension_adds_shards_without_touching_samples_1_to_10 | MET |
| 5c | Max new tokens 1,024, reasoning 16,384; truncated outputs labeled incorrect and counted (601-604) | requests.py:56; pipeline/execute/extract.py:187-188 | tests/generate/test_requests.py::test_thinking_and_base_and_special_models; tests/execute/test_execute_extract.py::test_truncated_takes_precedence_and_keeps_no_code | MET |
| 5d | Frozen prompt files hashed in the manifest; chat template pinned and hashed as rendered (605) | pipeline/generate/prompts.py; generate/stage.py:253 (`_record_prompts`) | tests/generate/test_prompts.py::test_real_prompts_load_and_match_constants; ::test_tampered_prompt_is_refused; ::test_chat_rendering_thinking_flag_and_hashes | MET |
| 5e | V1 and V2 turns verbatim; V1 decoded greedily up to 8 tokens (607-614) | constants.py:77-81; pipeline/generate/capture.py:281 (`_greedy`) | tests/contracts/test_contracts.py::test_prompt_files_match_hashes_and_verbatim_text; tests/generate/test_capture.py::test_v1_kv_cache_reuse_equals_no_cache_decode | MET |
| 5f | V2 readout sums "the case and leading-space variants of each token" (616) | pipeline/generate/tokens.py:164 follows 7.12 (exact "Yes"/"No" after stripping leading whitespace; no case variants) | tests/generate/test_tokens.py::test_answer_token_variant_rule | DIVERGENT (G17) |
| 5g | Reasoning stratum: both elicitation turns with thinking off (617) | tokens.py:104-105 (`thinking=False`) | tests/generate/test_capture.py::test_rewriting_template_layout_and_thinking_on_elicitation | MET |
| 5h | Seed = first 8 bytes of SHA-256 over (model ID, revision, benchmark, problem ID, index); vLLM per-request seed; engine pinned (618) | hashing.py:42; backends.py:213-214, :244 | tests/contracts/test_contracts.py::test_sample_seed_hand_computed; tests/generate/test_requests.py::test_seeds_follow_the_design_rule; tests/generate/test_backends.py::test_engine_seed_is_signed_64_bit; ::test_vllm_version_pin_and_lazy_import | MET |
| 5i | One teacher-forced pass over [prompt, code, V2 turn]: code-token log-probs, states at p1, p2, p3, V2 logits at p3; p2 for extraction failures is the last generated token before end of turn (619-625) | capture.py:106 (`prepare`), :147-150, :239 (`_run_batch`) | tests/generate/test_capture.py::test_shapes_layers_and_values_against_direct_forward; ::test_extraction_failure_positions | MET |
| 5j | Candidate layers at depth fractions rounded down, plus mean-pooled code-token state (626) | capture.py:40 (`layer_indices`), :251-252 | tests/generate/test_capture.py::test_shapes_layers_and_values_against_direct_forward | MET |
| 5k | V1 from the same prefix with the prefix KV cache reused (627) | capture.py:267 (`_row_cache`), :295 (`v1_ids`) | tests/generate/test_capture.py::test_v1_cache_reuse_in_a_padded_batch_equals_no_cache_decode | MET |
| 5l | bfloat16 hidden states, sharded per model (628) | capture.py:452; pipeline/generate/storage.py | tests/generate/test_stage.py::test_capture_shard_roundtrip | MET |
| 5m | Gemma 4 empty thought block kept in the frozen generation, skipped by extraction, excluded from code tokens (599) | extract.py:33 (`THOUGHT_MARKERS`, marked NOT VERIFIED), :51; tokens.py:189 | tests/execute/test_execute_extract.py::test_empty_thought_block_is_stripped; tests/generate/test_tokens.py::test_code_inside_thought_block_is_skipped | PARTIAL (G21) |
| 5n | Extra pass on the generation-shift model: S^R adapter active, k_g per test-fold problem per fold and suite, executed under both suites, reading A scored (629-636) | Generation only: generate/stage.py:233-242; requests.py:95. No caller builds `extra["fresh"]`; no scoring | tests/generate/test_stage.py::test_fresh_pass_with_adapter_uses_separate_set_and_seeds | PARTIAL (G4) |

## Section 6: Labels

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 6a | Pass = every test passes within its limit, normal exit, no raise (641) | pipeline/execute/sandbox.py:513 (`_interpret`) | tests/execute/test_execute_sandbox.py::test_correct_solution_passes_both_suites; ::test_exception_is_a_failure; ::test_candidate_output_and_exit_do_not_break_the_result | MET |
| 6b | HumanEval/MBPP use the EvalPlus evaluator at a pinned version; O = base inputs, E = base + plus (642) | pipeline/execute/harness.py:110 (`evalplus_match`); extract.py:147 (no sanitize, no prompt imports) | tests/execute/test_execute_semantics.py::test_copied_oracle_constants_match_installed_evalplus; tests/data/test_data_evalplus.py::test_suites | PARTIAL (G8) |
| 6c | Per-test time limit = factor x reference runtime with a floor, recorded (643) | harness.py:104 (`time_limits_for`); sandbox.py:347 (`_rule`) | tests/execute/test_execute_semantics.py::test_time_limit_rule; tests/data/test_data_evalplus.py::test_time_limit_rule_matches_evalplus_config | MET |
| 6d | LiveCodeBench official evaluator at a pinned commit, its time limits (644) | pipeline/execute/vendor/lcb/testing_util.py; sandbox.py:52, :217 | tests/execute/test_execute_lcb_and_backends.py::test_vendored_file_matches_its_recorded_hash_and_commit; ::test_lcb_timeout_uses_the_evaluators_own_limit | MET |
| 6e | Fresh unprivileged container: no network, read-only FS with tmpfs, CPU time and 2 GB memory limits, process-count limit, interpreter by path; 60 s program cap (645-652) | sandbox.py:160 (container argv), :127 (bwrap argv); harness.py:370-383 (setrlimit incl. RLIMIT_NPROC); sandbox.py:579 (cap) | tests/execute/test_execute_lcb_and_backends.py::test_container_argv; ::test_bwrap_argv; tests/execute/test_execute_sandbox.py::test_memory_limit_stops_an_allocating_program; ::test_loop_that_swallows_the_alarm_hits_the_program_cap; ::test_interpreter_must_be_an_absolute_path; tests/execute/test_execute_lcb_and_backends.py::test_bwrap_preflight_and_run_on_the_pod (pod only) | PARTIAL (G11) |
| 6f | Orchestrator rule: generated code never runs on the Mac; no silent fallback from bwrap or container | sandbox.py:368 (`_require_allowed`), :632 (`preflight`), :264-281 (raise if runtime missing); pipeline/execute/stage.py:201-221 | tests/execute/test_execute_sandbox.py::test_no_silent_fallback_when_bwrap_is_missing; ::test_trusted_only_backend_refuses_untrusted_even_when_enabled; ::test_preflight_cannot_prove_isolation_on_trusted_only; tests/execute/test_execute_stage.py::test_stage_refuses_to_execute_on_trusted_only_even_if_asked | MET |
| 6g | Reference solution run under every suite before labeling; failures excluded and listed, not repaired; share per suite (653-656) | pipeline/execute/stage.py:168-198; pipeline/execute/reference.py:164, :201 | tests/execute/test_execute_sandbox.py::test_reference_check_on_five_real_humaneval_plus_problems; ::test_reference_that_raises_or_times_out_is_excluded_not_repaired; ::test_excluded_pairs_get_no_label_row | MET |
| 6h | LiveCodeBench: list problems no sample passes under public tests, and problems whose public and full labels disagree for every passing sample (657) | not located | none | GAP (G14) |
| 6i | Extraction-failure codes; labeled incorrect; a sensitivity analysis excludes them; rates per model, benchmark, suite (658-665) | extract.py:147; labels.py:83-84, :97-98; execute/stage.py:284. Exclusion used only in reconciliation diagnostics (analysis/stage.py:230-239, :500) | tests/execute/test_execute_extract.py::test_failure_codes_are_the_contract_codes; ::test_no_block | PARTIAL (G6) |
| 6j | Both suites per sample; flip table per model; fail-to-pass listed (666) | labels.py:105 (`flip_table`) | tests/execute/test_execute_sandbox.py::test_flip_table | MET |
| 6k | Cache key (normalized code, problem, suite or input set, evaluator version, time-limit rule and memory, interpreter hash); value; reuse; 1 percent audit (667-671) | hashing.py:95; sandbox.py:355; pipeline/execute/cache.py:35, :83 | tests/contracts/test_contracts.py::test_exec_cache_key_changes_with_every_field; tests/execute/test_execute_sandbox.py::test_cache_key_depends_on_every_field; ::test_label_samples_and_cache_reuse; ::test_cache_audit_logs_a_mismatch | MET |
| 6l | Implied by 641: a label reflects the program, not an infrastructure failure | sandbox.py:519-529 maps harness or sandbox errors to `sandbox_error`; labels.py:100-101 records y = 0 | none | PARTIAL (G19) |

## Section 7: Readouts and baselines

### 7 (common protocol)

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.0a | Five problem-grouped folds by SHA-256(fold seed, problem ID) mod 5, same for every model and readout (677) | hashing.py:51; pipeline/data/folds.py:127 | tests/contracts/test_contracts.py::test_fold_of_hand_computed_and_range; tests/data/test_data_folds.py::test_fold_properties | MET |
| 7.0b | Seed 0 primary; P and S^T (E) refit on seeds 1, 2 for every primary model; non-LoRA readouts on all seeds (678) | pipeline/readouts/stage.py:269 (`lora_seeds`), :416-420 | tests/readouts/test_readouts_stage.py::test_stage_mock_run | MET (pilot T1: G3) |
| 7.0c | Inner 4-fold problem-grouped split, each training fold in turn (679) | pipeline/contracts/schemas.py:141; readouts/common.py:130 | tests/contracts/test_contracts.py::test_foldplan_inner_splits | MET |
| 7.0d | Every supervised readout refit under each label suite (680) | readouts/stage.py:419-420, :280 | tests/readouts/test_readouts_stage.py::test_stage_mock_run | MET |
| 7.0e | No test-fold information in any fit (681) | readouts/common.py:48 (`record_fit`) in every fit | tests/readouts/test_readouts_fits.py::test_fits_never_see_the_outer_test_fold; tests/integration/test_pipeline_mock.py::test_fold_integrity_and_no_leakage | MET |
| 7.0f | Label-validity and LiveCodeBench populations fit separately (682) | readouts/stage.py:58, :401-409 | none | MET |

### 7.1 Hidden-state probe

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.1a | L2 logistic regression on features standardized with training-fold mean and variance (686) | pipeline/readouts/probe.py:80 (`_design`), :100 | tests/readouts/test_readouts_fits.py::test_probe_family_outputs | MET |
| 7.1b | Family P2 (p2), P3 (p3), Pmulti (seven layers at p2, PCA 512 on training folds) (687-690) | probe.py:54, :89-96 | tests/readouts/test_readouts_fits.py::test_pmulti_pca_is_capped_at_training_rank | MET |
| 7.1c | Member, layer, and C in {1e-3..10} chosen by inner 4-fold grouped CV on log loss (691) | probe.py:136 (`select_over_specs`), :234-248 | tests/readouts/test_readouts_fits.py::test_probe_family_outputs | MET |
| 7.1d | Each member reported separately; R against each member (691, 153) | scores per member: readouts/stage.py:168-175; R per member not computed | none | PARTIAL (G6) |
| 7.1e | No class balancing (692) | probe.py:109 (default class weights) | none | MET |

### 7.2 Zero-shot verbal confidence

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.2a | V1 = regex integer, clipped to [0, 100], divided by 100 (696) | capture.py:45 (`parse_v1`) | tests/generate/test_capture.py::test_parse_v1_cases | MET |
| 7.2b | Unparsed is missing, never a default; imputed with training-fold median, flagged; imputed samples tie (697-698) | pipeline/readouts/verbal.py:49, :58 | tests/readouts/test_readouts_fits.py::test_v1_imputation_uses_training_folds_only | MET |
| 7.2c | Sensitivity analysis drops unparsed samples (699) | verbal.py:58 (`SZ_V1_drop`); not used in any budget | none | PARTIAL (G6) |
| 7.2d | Parse rate reported (700) | verbal.py:28; analysis/stage.py:246 | tests/readouts/test_readouts_fits.py::test_v1_drop_variant_parse_rate_and_k3 | MET |
| 7.2e | V2 from logits at p3, never missing (701) | verbal.py:111 | tests/readouts/test_readouts_fits.py::test_v2_is_float32_logodds_and_never_missing | MET |
| 7.2f | V1 is the primary-chain zero-shot readout, V2 the sensitivity chain (702) | analysis/stage.py:566-579 | tests/analysis/test_stage.py::test_stage_k3_switch_and_dry_run | MET |

### 7.3 Isotonic recalibration

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.3a | Isotonic fit on training-fold samples, applied out of fold; zero-shot maps fit directly (706-707) | pipeline/readouts/isotonic.py:49 | tests/readouts/test_readouts_fits.py::test_isotonic_train_scores_replace_own_scores | MET |
| 7.3b | S^T map on inner-cross-fitted scores (four inner adapters per outer fold and suite), split-1 reuse stated, inner-2-to-4 and in-sample sensitivities (708) | recipe.py:230; readouts/stage.py:319-324; isotonic.py:99 | tests/readouts/test_readouts_recipe.py::test_final_adapter_uses_step_transfer_and_inner_adapter_counts; ::test_surrogate_pipeline_end_to_end_with_isotonic | PARTIAL (G16, G6) |
| 7.3c | In-sample maps for secondary strata, seed refits, and LiveCodeBench, labeled (709-711) | readouts/stage.py:325-327 | tests/readouts/test_readouts_stage.py::test_stage_mock_run | MET |
| 7.3d | Ranking ties broken by the pre-map score (712) | isotonic.py:81-84 | tests/readouts/test_readouts_fits.py::test_isotonic_tie_rule_clip_and_values | MET |
| 7.3e | `out_of_bounds = clip`; single-class training set gives the base rate (713) | isotonic.py:32 | tests/readouts/test_readouts_fits.py::test_isotonic_fit_clip_and_single_class | MET |

### 7.4 Trained stated-confidence readout

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.4a | LoRA rank 16, alpha 32, dropout 0.05, no bias, all attention and MLP projections (718) | pipeline/readouts/masked_lora.py:65, :87, :183 | tests/readouts/test_readouts_masked_lora.py::test_adapter_uses_the_design_lora_settings; ::test_target_modules_are_all_attention_and_mlp_projections | MET |
| 7.4b | Adapter active only on the elicitation turn and answer position; prefix KV cache identical to base (719-720) | masked_lora.py:202 (`_hook`), :130-146 (`collate_layouts`), :304 (`final_state`) | tests/readouts/test_readouts_masked_lora.py::test_mask_unit_test_on_each_architecture; ::test_no_grad_prefix_gives_the_same_loss_and_gradients; tests/readouts/test_readouts_review_fixes.py::test_collate_rejects_a_mask_that_is_not_the_trailing_span | MET |
| 7.4c | S^T = P(Yes)/(P(Yes)+P(No)) at the answer position, V2 format (721) | masked_lora.py:320 | tests/readouts/test_readouts_masked_lora.py::test_yes_no_logodds_is_float32_and_matches_manual_head | MET |
| 7.4d | Binary cross-entropy loss (722) | pipeline/readouts/lora_train.py:51 | tests/readouts/test_readouts_recipe.py::test_masked_lora_training_reduces_loss | MET |
| 7.4e | All training-fold samples, unweighted; AdamW, cosine, 5 percent warmup, effective batch 64, up to 2 epochs (724-725) | lora_train.py:101-130; recipe.py:43 | tests/readouts/test_readouts_recipe.py::test_lr_schedule | PARTIAL (G16) |
| 7.4f | LR and step chosen on the first inner split's validation fold, E suite, every 20 steps, per (fold seed, outer fold), recorded; step transfer by epoch fraction (726) | recipe.py:177 (`select_recipes`), :53, :217; readouts/stage.py:241 | tests/readouts/test_readouts_recipe.py::test_recipe_selection_picks_lr_and_step_by_inner_validation_loss; ::test_step_transfer_arithmetic; ::test_recipe_table_roundtrip | PARTIAL (G16) |
| 7.4g | Recipe reused for O, LiveCodeBench, base and trajectory checkpoints; thinking-on reuses thinking-off (726) | readouts/stage.py:66 (`RECIPE_SOURCE`), :214 (`table`) | tests/readouts/test_readouts_review_fixes.py::test_checkpoints_reuse_the_source_recipe_per_seed_and_fold; ::test_recipe_source_table | MET (pilot consequence: G2) |
| 7.4h | Run inventory per primary model and outer fold, incl. seeds 1, 2 selection and final adapters (727) | readouts/stage.py:274 (`run_lora`), :295 | tests/readouts/test_readouts_stage.py::test_stage_mock_run | MET |
| 7.4i | Probe selected on the first inner split only as a sensitivity, R reported under it (728) | probe.py:245-248 (`P2_single_split`); R not computed | tests/readouts/test_readouts_fits.py::test_probe_family_outputs | PARTIAL (G6) |

### 7.5 [2610.31820]-style readout

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.5a | Same LoRA settings and recipe, active on all positions; fit on label validity (for Delta Gamma_g) and LiveCodeBench (732) | pipeline/readouts/real_backend.py:108; readouts/stage.py:359; runs for every model (stage.py:62, :284-287) | tests/readouts/test_readouts_rtuning.py::test_training_learns_the_sure_unsure_label_and_adapter_is_unmasked | PARTIAL (G18) |
| 7.5b | SFT on prompt + frozen code + "I am sure"/"I am unsure"; loss on code and suffix (733) | pipeline/readouts/rtuning.py:69 | tests/readouts/test_readouts_rtuning.py::test_sft_example_layout_and_supervision | MET |
| 7.5c | Readout P(sure)/(P(sure)+P(unsure)) after "I am" (734) | rtuning.py:112 | tests/readouts/test_readouts_rtuning.py::test_score_multi_token_continuation_matches_manual_logprobs | MET |
| 7.5d | Reading B: teacher-force frozen test-fold samples followed by "I am" (737) | rtuning.py:157 via recipe.py:217 | none specific | MET |
| 7.5e | Reading A: fresh samples scored from their own suffix; probe read on the same samples (736) | not located | none | GAP (G4) |
| 7.5f | Adapter pass rate on fresh samples reported against base (738) | analysis/generation_shift.py:75 (needs fresh labels, see G4) | none | PARTIAL (G4) |

### 7.6 to 7.10

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.6a | Code tokens only, excluding fence and end-of-turn tokens (742) | capture.py:136-156 | tests/generate/test_tokens.py::test_code_span_mapping_excludes_fences | MET |
| 7.6b | Geometric mean, exp(min log p), total log p; Intrinsic = geometric mean (744-747) | pipeline/readouts/unsupervised.py:51 | tests/readouts/test_readouts_fits.py::test_token_likelihood_variants | MET |
| 7.6c | Samples without code tokens: undefined values are missing, never imputed (section 11 row 7.7; generate CONTRACT_REQUESTS item 2) | unsupervised.py:71-74 sets TL_geo = TL_min = 0 and TL_sum = floor; analysis/stage.py:283-290 scores them | tests/readouts/test_readouts_fits.py::test_token_likelihood_variants | DIVERGENT (G9) |
| 7.6d | Isotonic versions for calibration only (749) | readouts/stage.py:60 | none | MET |
| 7.7a | Disjoint inputs; signature = output or exception per input, canonical repr with floats to 9 significant digits (755-756) | labels.py:139; harness.py:210; unsupervised.py:91 | tests/execute/test_execute_sandbox.py::test_agree_signature_normalizes_floats; tests/execute/test_execute_semantics.py::test_floats_are_normalized_to_nine_significant_digits | MET |
| 7.7b | A = (1/(k-1)) sum of signature matches; problem-level largest-cluster share (757-758) | unsupervised.py:107 | tests/readouts/test_readouts_fits.py::test_agreement_share_of_other_samples | MET |
| 7.8 | AST alpha-renaming, docstrings and comments removed, `ast.dump`, unparseable singletons, cluster size / k (768-769) | unsupervised.py:209, :223 | tests/readouts/test_readouts_fits.py::test_ast_renaming_docstrings_and_singletons | MET |
| 7.9 | Prompt-only probe: same class and nested selection on the state at p1 (773-774) | probe.py:300 | tests/readouts/test_readouts_fits.py::test_prompt_probe_is_constant_within_a_problem | MET |
| 7.10 | Character 3-5-gram TF-IDF (sublinear, min df 3, training folds), L2 logistic, C by inner grouped CV (779-780) | pipeline/readouts/codetext.py:27, :53 | tests/readouts/test_readouts_fits.py::test_codetext_reads_surface_text_only | MET |

### 7.11 Capacity controls

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.11a | Ladder on Olmo-3-7B-Instruct and Qwen3-14B: ranks 1, 4, 16, alpha twice the rank, E suite, seed 0 (788) | readouts/stage.py:329; masked_lora.py:71; constants.py:58-59 | tests/readouts/test_readouts_stage.py::test_stage_mock_run | MET |
| 7.11b | R at each rung with paired interval; capacity sentence fires if the rank-16 minus rank-1 W(S^T) interval lies outside (-delta, delta) on either model (788) | not located in analysis/ | none | GAP (G6) |
| 7.11c | LoRA plus linear head on the p3 state, reported as a contrast with S^T (789) | masked_lora.py:252; readouts/stage.py:352-357; contrast not computed | none | PARTIAL (G6) |
| 7.11d | MLP probe (width 256, ReLU, weight decay on inner split) on all six primary models, R beside the primary R (790) | probe.py:339; readouts/stage.py:169-179; R not computed | tests/readouts/test_readouts_fits.py::test_mlp_probe | PARTIAL (G6) |

### 7.12 Implementation rules fixed before the pilot

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 7.12a | Yes/No logits in float32 from the final hidden state, LM head in float32, stored as log-odds; ranking uses the log-odds (794) | capture.py:205; masked_lora.py:320; verbal.py:117; adapter_readout.py:62 | tests/generate/test_capture.py::test_yes_no_logodds_float32_against_manual_computation; ::test_head_is_applied_in_float32_even_for_a_bfloat16_model; tests/readouts/test_readouts_masked_lora.py::test_yes_no_logodds_is_float32_and_matches_manual_head | MET |
| 7.12b | Answer sets = single tokens whose text, stripped of leading whitespace, is exactly "Yes" or "No"; class probability summed; lists written to the manifest before the pilot (794) | tokens.py:164; generate/stage.py:334-335; real_backend.py:45 | tests/generate/test_tokens.py::test_answer_token_variant_rule; tests/readouts/test_readouts_review_fixes.py::test_answer_ids_read_the_file_the_generate_stage_writes | MET |
| 7.12c | Within-problem tie rate reported for every readout entering R (794) | analysis/gap.py:296 (seed 0 only) | none | MET |
| 7.12d | Mask = 1 from the first token of the V2 turn header through the last token before the answer; p3 = last token of the span; spans per model written to the manifest (795) | tokens.py:85-139; capture.py:128; generate/stage.py:336-337; masked_lora.py:144-146 | tests/generate/test_tokens.py::test_elicitation_turn_from_template; tests/readouts/test_readouts_review_fixes.py::test_mask_span_from_generate_layouts_matches_independent_count; ::test_a_wrong_span_fails_the_independent_check | MET |
| 7.12e | Mask unit test once per architecture class before its first trained readout, padded training layout, through the S^T engine; (a) non-masked states and KV within 1e-3 in float32, (b) masked states differ; full adapter as negative control (796) | pipeline/readouts/gate.py:68, :34 (2-layer float32 slice); readouts/stage.py:262-265; masked_lora.py:387 | tests/readouts/test_readouts_masked_lora.py::test_mask_unit_test_on_each_architecture; tests/readouts/test_readouts_review_fixes.py::test_gate_runs_on_a_float32_slice_of_a_bf16_model; ::test_stage_refuses_to_train_when_the_mask_test_fails; ::test_positive_control_fails_for_a_zero_adapter | PARTIAL (G12) |
| 7.12f | S^T scored by the training framework's masked forward, not a serving engine (796) | masked_lora.py:304-339 | tests/readouts/test_readouts_masked_lora.py::test_padded_batch_equals_unpadded_rows | MET |

## Section 8: Metrics

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 8a | Pooled AUROC, Mann-Whitney, ties one half (801) | analysis/metrics.py:102 | tests/analysis/test_metrics.py::test_auroc_pooled_hand | MET |
| 8b | Pooled AUPRC for "pass" with base rate; "fail" AUPRC too (802) | metrics.py:147, :174 | tests/analysis/test_metrics.py::test_auprc_hand | MET |
| 8c | W pair-weighted; all-pass and all-fail drop out; counts reported per model and suite (805-807) | metrics.py:186, :214 | tests/analysis/test_metrics.py::test_within_problem_auroc_hand | MET |
| 8d | W_avg secondary (809) | metrics.py:200, :457 | tests/analysis/test_metrics.py::test_rankstats_matches_direct_weighted | MET |
| 8e | W on each suite's own mixed set; W on problems mixed under both; entering and leaving counts (810) | analysis/gap.py:259-280 | tests/analysis/test_shapley_gap_routing.py::test_l_and_d_diagnostics_consistent | MET |
| 8f | Brier with Murphy decomposition, 15 equal-mass bins (815) | metrics.py:296, :305 | tests/analysis/test_metrics.py::test_brier_and_murphy_hand | MET |
| 8g | Problem-demeaned Brier within mixed problems for d = 1 (816) | metrics.py:347; gap.py:143 | tests/analysis/test_metrics.py::test_demeaned_brier_hand | MET |
| 8h | Brier and calibration budgets oriented stated minus probe (817) | gap.py:206 | tests/analysis/test_shapley_gap_routing.py::test_secondary_sign_convention | MET |
| 8i | Debiased equal-mass ECE (15 bins), smooth ECE, KS calibration error (819-823) | analysis/calibration.py:144, :189, :337 | tests/analysis/test_calibration.py::test_debiased_ece_hand; ::test_smooth_ece_batch_equals_scalar; ::test_ks_hand; ::test_reference_cross_check_values | MET |
| 8j | Equal-width 15-bin and 10-bin ECE for the two comparisons (825) | calibration.py:352; metrics.py:509-510 | tests/analysis/test_calibration.py::test_equal_width_hand | MET |
| 8k | Legacy TACE retired (827-833) | no TACE in analysis/ (searched) | none | MET |

## Section 9: Inference

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 9a | One problem-clustered paired bootstrap, B = 10,000, joint over models, readouts, suites, cells (839) | analysis/bootstrap.py:29; analysis/stage.py:556 | tests/analysis/test_inference.py::test_draw_determinism_and_shape; ::test_pairing_same_draws_across_statistics | MET |
| 9b | Percentile intervals; BCa sensitivity for the primary statistic (840) | bootstrap.py:82, :107; analysis/stage.py:613-616 | tests/analysis/test_inference.py::test_percentile_interval_hand_and_undefined_rule; ::test_bca_reduces_to_percentile_when_symmetric | MET |
| 9c | Undefined replicates dropped and counted; above 1 percent the interval is unavailable; never imputed (841) | bootstrap.py:74, :82 | tests/analysis/test_inference.py::test_undefined_rule_property | MET |
| 9d | Single fixed seed for all metrics (842) | constants.py:25 | tests/analysis/test_inference.py::test_draw_determinism_property | MET |
| 9e | Per-problem pair counts and rank sums precomputed (843) | metrics.py:399 (`RankStats`) | tests/analysis/test_metrics.py::test_rankstats_matches_direct_weighted | MET |
| 9f | P and S^T (E) under seeds 0, 1, 2; same draw for all seeds; R_m seed mean; R_bar model mean (847-848) | analysis/stage.py:327 (`seed_residuals`); refit.py:26, :36 | tests/analysis/test_inference.py::test_primary_report_and_k4 | MET |
| 9g | s2_refit = (1/3)(1/36) sum sigma2_m, 12 df (849) | analysis/refit.py:56, :70 | tests/analysis/test_inference.py::test_refit_widening_hand | MET |
| 9h | Symmetric widening to sqrt(h^2 + (t s)^2), t = 1.782; six sigma2_m and unwidened interval reported (850) | refit.py:74, :81; decisions.py:63 | tests/analysis/test_inference.py::test_refit_widening_hand | MET |
| 9i | Other cells at seed 0; R^(0) beside R_bar (853) | analysis/stage.py:637-640 | none specific | MET |
| 9j | All 16 cells per resample; percentile intervals for terms, sequential terms, interactions (855) | analysis/budget.py:36; shapley.py:124 | tests/analysis/test_shapley_gap_routing.py::test_cell_replicates_match_weighted_direct | MET |
| 9k | Holm across the six models per decision; Bonferroni 98.75 percent for pooled terms with 95 beside; per-model terms 95 unadjusted (857-863) | decisions.py:114; budget.py:24; constants.py:20 | tests/analysis/test_inference.py::test_holm_step_down_hand | MET |
| 9l | Heterogeneity: R_m 90 percent unwidened and widened; between-model SD; tau2_hat with interval; same for G0 and each term; per-family means (867-872) | decisions.py:148, :172, :201; budget.py:145-154 | tests/analysis/test_inference.py::test_heterogeneity_hand | MET |
| 9m | Sign disagreement or tau_hat > delta flagged for the decision sentence (874) | decisions.py:213 | none | MET |

## Section 13: Kill and pivot criteria (code-checkable parts)

| Req ID | Requirement (design line) | Implementation | Test | Status |
|---|---|---|---|---|
| 13a | Pilot: T1 end to end, including the trained readout with recipe selection (1116) | ops/plans/pilot.json:6-22; pipeline/readouts/stage.py:66, :229-236, :422-423 | tests/readouts/test_readouts_review_fixes.py::test_pilot_model_may_select_its_own_recipe (flag set by hand; the plan does not set it) | DIVERGENT (G2) |
| 13b | Mixed-count part for P1..P6: generation and labels only; no forward pass, readout, score, or Gamma cell of a primary model (1117, 1119) | pilot.json:16; generate/stage.py:281-283; readouts/stage.py:398-400; analysis/stage.py:571-572 | tests/readouts/test_readouts_stage.py::test_stage_skips_generation_only_models_and_missing_capture; tests/integration/test_pipeline_mock.py::test_sealed_pilot_mode | MET |
| 13c | m_bar = mean over P1..P6 of problems mixed under E on the label-validity population after exclusions (1117) | analysis/stage.py:601-607; analysis/krule.py:24 | tests/analysis/test_inference.py::test_k_rule_boundary | MET |
| 13d | Throughput probes on P4, P6 (forward pass, 200 LoRA steps on 50 problems) and S1 thinking length (1118) | pilot.json:24-29; no stage reads `timing_only` or `gen_set` | none | GAP (G10) |
| 13e | Sealing: Gamma cells, terms, residual written to a hashed file, not opened; only operational outputs opened (1120) | analysis/stage.py:101-106, :645-656 | tests/analysis/test_stage.py::test_stage_sealed_writes_nothing_gamma_to_results; tests/integration/test_pipeline_mock.py::test_sealed_pilot_mode | MET |
| 13f | Pilot reports the T1 seed-to-seed spread of W(S^T) over fold seeds 0, 1, 2 (1120, 1122) | analysis/stage.py:587-593 needs S^T at seeds 1, 2; readouts/stage.py:83-84, :269-272 fit T1's S^T at seed 0 only | none | GAP (G3) |
| 13g | k = 20 if m_bar < T10 = 185, else 10; T20 = 125 reported; per-model counts, pair counts, histograms (1122) | krule.py:20-51; constants.py:29-32 | tests/analysis/test_inference.py::test_k_rule_boundary | MET |
| 13h | K1: reference exclusion above 5 percent of a suite stops the run (1128) | execute/stage.py:182-190 (metric and note only); reference.py:201 | tests/execute/test_execute_sandbox.py::test_k1_threshold_is_five_percent | PARTIAL (G7) |
| 13i | K3: V1 parse rate below 80 percent switches to V2; all-V2 budget and switched models reported; V2 degenerate on more than half the primary models changes the G0 report (1130) | analysis/stage.py:566-570, :621-629 | tests/analysis/test_stage.py::test_stage_k3_switch_and_dry_run | PARTIAL (G13) |
| 13j | K4: per model and seed; retry at lr 1e-3, 4 epochs, eval every 20 steps; inner loss only; probe matching retry; flag; unflagged sensitivity; "only through flagged" stated (1131) | recipe.py:177-211; probe.py:197-213; decisions.py:268-285 | tests/readouts/test_readouts_recipe.py::test_k4_majority_failure_retries_with_fixed_setting; ::test_k4_failure_after_retry_keeps_best_grid_point_and_flags; tests/readouts/test_readouts_review_fixes.py::test_probe_k4_retry_succeeds_with_extra_c_values; tests/analysis/test_inference.py::test_primary_report_and_k4 | PARTIAL (G20) |

K5 and K6 have no code obligation. K7 (ops/cost.py) was not audited in depth.

## Already-known items, re-verified

| Item | Claim | Evidence | Status |
|---|---|---|---|
| Review B1 | Answer-token file read in the generate-stage format | real_backend.py:45-56 accepts `{"id", ...}` entries; tests/readouts/test_readouts_review_fixes.py::test_answer_ids_read_the_file_the_generate_stage_writes | MET |
| Review B2 | Adapter init device-safe | masked_lora.py:227-238 (CPU generator, copy to device); ::test_reset_is_seeded_and_uses_cpu_generator_then_copies; ::test_reset_on_cuda needs a GPU (not run) | MET (CUDA path not executed) |
| Review M1 | Mask gate runs before training | gate.py:68; readouts/stage.py:262-265 | PARTIAL (G12) |
| Review M2 | Recipe reuse for checkpoints | readouts/stage.py:66, :214 | MET, but it breaks the pilot plan (G2) |
| Review M3 | Span checked independently | masked_lora.py:144-146; ::test_mask_span_from_generate_layouts_matches_independent_count | MET |
| Review M4 | Probe K4 retry | probe.py:197-213 | MET (trigger and grid unlogged, G20) |
| Review M5 | Split-1 selection-adapter schedule mismatch disclosed | still present (recipe.py:241-245); not in docs/DEVIATIONS.md:12 | OPEN (G16) |
| Review m1, m2, m14 | wd 0 and clip 1.0; eval at final step; ladder recipe reuse logged | lora_train.py:56, :113; stage.py:339-349; DEVIATIONS.md has no entries | OPEN (G16) |
| Review m4, m5, m6, m7, m9, m15 | bias, answer-id rule, left-pad guard, torch.where, positive-control failures, sliding-window gradient | masked_lora.py:330-332, :157-162, :306-307, :205-207; review-fix tests | MET |
| Review m3, m8, m10, m12, m13 | minor items | not re-verified | not verified |
| analysis CR open item | Fresh scores must not overwrite frozen scores | pipeline/contracts/layout.py:141-152 adds a generation-set level | MET |
| readouts CR 1, 2 | Extra readout names; path helpers | analysis reads only some names (G6); paths built ad hoc (readouts/stage.py:155, :195, :264) | PARTIAL (no number affected) |
| readouts CR 4 | Deviations to log | not in DEVIATIONS.md | OPEN (G16) |
| execute CR 5 | Prompt imports and helpers for chat code | unresolved; extract.py:147-201 | OPEN (G8) |
| execute CR 7 | Gemma 4 thought markers unverified | extract.py:29-38 | OPEN (G21) |
| execute CR 1 to 4, 6 | layout property, vocabulary, protocol extras, contract reading, input encoding | execute/stage.py:194 writes the proxy path ad hoc; others descriptive | no number affected |
| generate CR 2 | NaN token-likelihood treated as missing | not honored (unsupervised.py:71-74) | OPEN (G9) |
| generate CR 6 | Base stop strings and vLLM `top_k=-1` not verified on the pinned engine | backends.py:243 | OPEN (G22) |
| generate CR 1, 3, 4, 5, 7 | dtype, bridge tokens, signed seeds, prompt hash, shard blocks | consistent with 5 and 7.12 | MET |
| data CR 2 | Adapted contracts for patched MBPP+ tasks need a DEVIATIONS line | not logged | OPEN (G16) |
| data CR 4, 5 | Manifest save; empty agreement suites | 4 not re-verified; 5 handled as missing (unsupervised.py:116-121) | not verified / MET |
| ops CR 2 | Timing-only probes need stage support | no stage implements it | OPEN (G10) |
| ops CR 6 | Operator confirmations (container image and others) | pilot.json:13 selects "container" with no `container_image`; sandbox.py:265-266 raises | OPEN (G11 note) |

## Findings

**G1. BLOCKING. Supervised readouts are fit on suite-specific problem sets, not on the both-suite label-validity population.** Design 4 (558) and 1.4 (175) require every supervised readout of the 16-cell game to be fit only on problems whose reference passes both suites. A problem excluded under E only keeps its O labels (execute/labels.py:81-82 drops just the excluded pair; readouts/files.py:125 sets the other suite's label to -1 only where missing), the fold plans cover every problem (data/stage.py:196-199), and `Folds.valid` keeps any row with a label under the active suite (readouts/common.py:118). So P^(O), iso:S^Z(O), S^T(O), and iso:S^T(O) are trained on extra problems that the analysis later drops (analysis/stage.py:135, :533). This changes G0 and every l = 0 cell, and therefore every Shapley term. R (l = 1) is affected only if some problem is excluded under O but not under E. Verified by reading. Fix: in the readouts stage, read `data/reference_checks.parquet` and set the label of every suite to -1 for any label-validity problem excluded under either suite (or have the execute stage write no row for either suite in that case). Add a test with one E-only exclusion that asserts no O-suite fit records that problem.

**G2. BLOCKING. The pilot plan cannot fit T1's trained readout.** `RECIPE_SOURCE["T1"] = "P3"` (readouts/stage.py:66). In the pilot P3 has no fits, so `table()` raises `MissingRecipeError` unless `cfg.extra["allow_own_recipe"]` is set (stage.py:229-236), and the stage re-raises it (stage.py:422-423). ops/plans/pilot.json sets no `extra`. Design 13 (1116) requires T1 end to end "including the trained readout with recipe selection". The unit test sets the flag by hand and does not test the plan. Verified by reading. Fix: add `"overrides": {"extra": {"allow_own_recipe": true}}` to the T1 readouts group in pilot.json, and add a plan-level test that expands the pilot plan and dry-runs T1 readouts with no P3 fits. Log in DEVIATIONS.md that T1's pilot recipe is selected on T1 and the full-run T1 reuses P3's recipe.

**G3. BLOCKING. The pilot cannot report the T1 seed-to-seed spread of W(S^T), and it does not exercise the primary S^T path.** `lora_seeds` gives seeds 1 and 2 only to primary, MOCK, and SMOKE models (readouts/stage.py:83-84, :269-272), so T1's S^T exists at seed 0 only. `seed_residuals` then returns None (analysis/stage.py:335-336) and `st_W_seed_spread` is never written. Design 13 (1120, 1122) requires this number, and the K7 compute estimate depends on the pilot timing the primary code path (three seeds, inner adapters). Verified by reading. Fix: treat `PILOT_MODEL` like a primary model in `_is_primary` for S^T seeds and inner adapters (label-validity population only), and add a test that the pilot plan produces S^T at seeds 0, 1, and 2 for T1.

**G4. MAJOR. The generation-shift contrast (reading A) has no producer.** The analysis side is complete (analysis/generation_shift.py:51; analysis/stage.py:376), but nothing builds `extra["fresh"]` from the saved S^R adapters (no match in ops/), nothing scores fresh samples with S^R from their own suffix (`score_rtuning` is never called on fresh data), fitted probe weights are not saved, so the "same fitted member" cannot be applied to fresh states, and the readouts stage always loads the frozen set (readouts/files.py:66; readouts/stage.py:405). Delta Gamma_g (1.5), the [2610.31820] reading A (which K7 says is never cut), and the 7.5 accuracy check therefore cannot be computed. Verified by reading. This is not on the primary decision path. Fix: persist the probe's scaler, PCA, and coefficients per (seed, outer fold, suite); add a readouts step that, for each fresh set "fresh:SR_<suite>_seed<s>_fold<f>", loads the base-weights capture, applies the fold's probe, scores S^R with the fold's adapter by `score_rtuning`, and writes rows with that `generation_set`; add the fresh-pass jobs to the full plan.

**G5. MAJOR. The contamination stratum is not implemented.** Design 4 (561-574) and H4 (240) require classifying each LiveCodeBench problem by contest_date against the model's count date and computing the budget per window, per model and for Olmo 3 and Gemma 4 pooled, with "pre or unknown" labeling for upper-bound dates. Only the dates exist (constants.py:161; data/lcb.py:180 sets `release_date`). No other stratum (family, scale, base vs instruct, reasoning, coder) contrast is computed either. Verified by search. Fix: add an analysis step that partitions the LiveCodeBench problems per model by `release_date > COUNT_DATES[m]` and runs `model_budget` on each partition with the same draws restricted to those columns; report Qwen3 as having no stratum.

**G6. MAJOR. Pre-specified sensitivity analyses and the capacity outcome rule are not computed.** The readouts stage writes the needed scores, but analysis/ computes only per-readout marginal metrics (analysis/stage.py:270) for them. Missing: R against each probe member (7.1, 1.3); R under single-split probe selection (7.4); R with the MLP probe (7.11); R at each ladder rung with paired intervals and the rank-16 minus rank-1 W(S^T) rule that decides the capacity sentence (7.11); the LoRA-plus-head contrast (7.11); the budget without the tie-break (1.2); the V1-drop budget (7.2); the iso:ST_inner234 and iso:ST_insample map sensitivities (7.3); the extraction-failure-excluded analysis (6, done only for reconciliation); the LiveCodeBench full-suite labeling sensitivity (4); the S^R versus S^T readout-format contrast (1.5). Verified by search. Fix: add a `sensitivity` step that recomputes `per_seed_residual` (and the cells where stated) with each substitute readout on the same draws, and reports paired differences against the primary R with intervals; implement the 7.11 rule as a boolean with its interval.

**G7. MAJOR. K1 is not a gate.** execute/stage.py:188-190 records `k1_triggered` and a note but leaves `rep.ok = True`, and no runner code checks it (no match in ops/). Design 13 K1 says "Stop ... Do not proceed until the excluded share is at most 5 percent or the operator accepts the list". Verified by reading. Fix: set `rep.ok = False` when K1 fires unless an operator acceptance file listing the excluded IDs exists under the run's `config/`, and have the runner stop on a failed stage.

**G8. MAJOR. Chat-mode programs are executed without the prompt's imports or helpers and without EvalPlus-style sanitizing, an unresolved labeling decision.** extract.py:147-201 runs the first fenced block as is. A correct function that relies on `from typing import List` or on a helper defined in the HumanEval prompt fails with NameError, and module-level example code (prints, asserts, input calls) runs at import. The execute CONTRACT_REQUESTS item 5 asked for a decision; none is recorded. Labels feed every primary number. How often this happens was not measured. Fix: decide before the pilot. Either implement the pinned EvalPlus 0.3.1 sanitizer (entry-point dependency extraction) plus the prompt's import lines, with a test, or log: "Extracted chat-mode code is executed as written, without prepending the prompt's imports or helper definitions and without removing module-level statements; this differs from EvalPlus's sanitize step." Report the NameError share per model from the pilot.

**G9. MAJOR. Token-likelihood readouts impute the minimum score for samples without code tokens.** unsupervised.py:71-74 sets TL_geo = TL_min = 0 and TL_sum below every observed value, flags `missing`, and analysis scores those rows because only non-finite scores are dropped (analysis/stage.py:283-290). Samples without code tokens are mostly extraction failures, which are always labeled 0, so the imputed value carries the label and inflates TL's AUROC and AUPRC, including the [Ribeiro] "Intrinsic" comparison. Section 11 row 7.7 says undefined values are never imputed, and the generate CONTRACT_REQUESTS item 2 asked for NaN to be treated as missing. Verified by reading. AGREE has a milder version: a sample with no signature gets 0.0 (unsupervised.py:124). Fix: write NaN with `missing=True` and score TL on non-missing samples (reporting the count), or keep the imputation as a labeled sensitivity. If kept, log: "Token-likelihood readouts assign the lowest score to samples with no code tokens."

**G10. MAJOR. The pilot throughput probes do nothing useful.** The P4 and P6 capture and LoRA probes are skipped, because both models are in `generation_only_models` (generate/stage.py:281-283; readouts/stage.py:398-400). No stage reads `timing_only`, `probe`, or `gen_set` (no match in pipeline/), so the S1 thinking-length probe writes its samples as the pilot run's frozen set. Design 13 (1118) requires these timings, and K7 uses them. Verified by reading. Fix: implement the ops CONTRACT_REQUESTS item 2 in the capture, readouts, and generate stages, writing to the "timing" generation set and exempting timing jobs from the generation-only skip, without writing any score or hidden state to analyzable paths. Add a plan-level test.

**G11. MAJOR (suspected). The process-count limit may be ineffective under bwrap when the pod runs as root, and the pilot sandbox configuration is incomplete.** bwrap relies on RLIMIT_NPROC set inside the sandbox (harness.py:383). The Linux kernel does not enforce RLIMIT_NPROC for the root user, and bwrap with `--unshare-all` and no `--uid` keeps uid 0 (build_bwrap_argv, sandbox.py:135). The preflight does not test a fork limit (sandbox.py:632-658). This was not executed. Separately, pilot.json:13 selects "container" with no `container_image`, so `SandboxExecutor` raises at construction (sandbox.py:265-266). That failure is loud, so there is no silent fallback, but the pilot cannot label as configured. Fix: run bwrap with `--unshare-user --uid 65534 --gid 65534`, or put each run in a cgroup with `pids.max`; add a fork-bomb probe to `preflight`; and set the backend and image in the pilot plan once the operator confirms them.

**G12. MINOR. The mask gate runs on a two-layer float32 slice, not the model that computes S^T.** gate.py:79 uses `float32_slice(model, 2)` on GPU. Design 7.12 (796) asks for the test "through the engine that computes S^T", with states and KV cache compared at every non-masked position. For a model whose first layers share one attention type (Gemma 4 interleaves sliding and global layers; the pattern was not verified), the other attention path is never tested. Fix: choose slice layers that cover every `layer_types` value, or run the test on the full bf16 model with float32 comparison, or log: "The 7.12 mask unit test runs on a float32 copy of the first two decoder layers with real weights."

**G13. MINOR. The K3 degenerate-V2 clause is not implemented.** No code checks whether V2 takes one value for every sample on more than half the primary models (design 1130). Fix: add the check and a flag to `pooled`.

**G14. MINOR. The LiveCodeBench problem listings are missing.** No list exists of problems that no sample passes under the public tests, or of problems whose public and full-suite labels disagree for every passing sample (design 657). Fix: add both lists to the operational output.

**G15. MINOR. The LiveCodeBench budget is a four-player game.** analysis/stage.py:67 treats "lcb_public" and "lcb_label" as l. The design (559) says the budget "has three toggles (r, t, d)" with the label toggle "replaced by" an analog, which can be read either way. Fix: also report the three-player game at l = "lcb_label", or log: "On LiveCodeBench the label analog is a fourth player of the game."

**G16. MINOR. Implementation choices are not logged in docs/DEVIATIONS.md, which still says "No deviations recorded" (line 12).** Unlogged choices:
- AdamW weight decay 0 and gradient clipping at 1.0 (lora_train.py:56, :125).
- Evaluation at the final step as well as every 20 steps (lora_train.py:113).
- Ladder ranks 1 and 4 reuse the rank-16 recipe (readouts/stage.py:347-349).
- The split-1 selection adapter used for the isotonic map trains on a different learning-rate schedule (recipe.py:241-245; review M5).
- The probe's K4 retry grid (probe.py:197).
- The MLP weight-decay grid (probe.py:38).
- The `canonical_repr` reading that keeps list and tuple order (inputs.py:84-87).
- HumanEval pairs are not grouped as near duplicates (folds.py:102-106).
- Adapted contracts for the patched MBPP+ tasks (data CONTRACT_REQUESTS item 2).
- TL_sum's probability (unsupervised.py:8-9).

Fix: log each before the pilot, with impact "none on estimands" except M5, which affects iso:S^T on pooled cells only.

**G17. MINOR. The design is inconsistent on the Yes/No token sets.** Section 5 (616) sums "the case and leading-space variants"; 7.12 (794) takes only exact "Yes"/"No" after stripping leading whitespace. The code follows 7.12 (tokens.py:164-180). Log: "Answer-token sets follow 7.12 (no case variants); section 5's wording is superseded."

**G18. MINOR. S^R and the LoRA family run for every model when `cfg.readouts` is empty.** readouts/stage.py:62 and :274-287 train S^R for all models and populations, while 7.5 fits S^R only for the generation-shift model and the LiveCodeBench reconciliation. This costs compute only. In the stub full plan, X1 and X2 on LiveCodeBench would raise `MissingRecipeError`, because they have no label-validity S^T fits (stage.py:229-236; full.json:24). Fix: restrict the LoRA readouts by model role.

**G19. MINOR. Infrastructure failures become negative labels.** A harness or sandbox error (`sandbox_error`) is labeled y = 0 (sandbox.py:526-529; labels.py:100-101), and the only record is a note. Fix: re-run such samples, and label them missing (not 0) if they still fail, with a count; or stop the stage if any remain.

**G20. MINOR. The probe K4 retry trigger and grid are this code's reading.** probe.py:207-212 retries whenever the probe fails on a majority of folds, whatever S^T did, and adds C in {1e-4, 100}. The design says "the matching retry of its own selection if it also fails". Log the reading.

**G21. MINOR. The Gemma 4 thought-block markers are unverified.** extract.py:29-38 marks them NOT VERIFIED. The failure is described as benign for extraction, but the code-token span and the V1 and V2 prefixes depend on the marker. Fix: verify against the pinned tokenizer's rendered template before the Gemma runs, and add a test that uses the cached tokenizer when present.

**G22. MINOR. Card sampling recommendations are not recorded, and two engine settings are unverified.** Design 5 (598) says the card recommendations are "recorded and not used". The code does not use them, but they are not recorded anywhere. vLLM `top_k=-1` and the base-model stop strings are not verified on the pinned engine (generate CONTRACT_REQUESTS item 6). Fix: add the recommendations to `config/prompts.json` per model, and verify both settings on the pod.

## Counts

Design-requirement rows (sections 1, 4 to 9, 13): 152.

| Status | Count |
|---|---|
| MET | 113 |
| PARTIAL | 25 |
| GAP | 10 |
| DIVERGENT | 4 |

| Severity | Count | IDs |
|---|---|---|
| BLOCKING | 3 | G1, G2, G3 |
| MAJOR | 8 | G4, G5, G6, G7, G8, G9, G10, G11 |
| MINOR | 11 | G12 to G22 |

Of the already-known items: review B1, B2, M2, M3, and M4 are fixed. M1 is partly fixed (G12), and the M2 fix caused G2. M5, m1, m2, and m14 are still open (G16). Open contract requests map to G8, G9, G10, G11, G16, G21, and G22.
