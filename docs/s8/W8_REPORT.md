# Wave 8 report: pipeline and pod tooling built against the frozen design, local smoke test, analysis code hashed

Date: 2026-11-11. Scope: code only. No primary or secondary model was run and no GPU was rented. The only model weights downloaded were the smoke model, Qwen/Qwen3-0.6B at revision `c1899de2...`, into the git-ignored `.hf-cache/` (1.4 GB). Every number below comes from a test run, a stage report, or a file named next to it. The smoke labels are synthetic (section 4), so no smoke metric is a measurement.

## 1. Model identifier

The orchestrator ran as `claude-opus-5-5`. Module owners B1 (data), B2 (execute), B3 (generate), B4 (readouts), and B6 (ops) ran on sonnet; B5 (statistics), the masked-LoRA reviewer, and the C3 conformance critic ran on opus, the critic in fresh context.

## 2. Commits and checks

| Commit | Content |
|---|---|
| `6b433bb` | A1 and A2: `pyproject.toml` and `uv.lock` (224 packages; groups `local` and `pod`; Python >=3.12,<3.13), `pipeline/contracts/` (constants, hashing, schemas, layout, manifest, interfaces, CHANGELOG), `pipeline/prompts/` with SHA-256 hashes |
| `b77be55` | Contract change: agreement-output and reference-output paths (logged in `pipeline/contracts/CHANGELOG.md`) |
| `d4c244b`, `4bef8d4` | B6 ops: bootstrap, plans, runner, guard, sync, cost ledger, RunPod client (dry run by default); test placeholder fix |
| `4b90348` | B2 execute: extraction, sandbox backends, EvalPlus harness, reference check, cache, labels, vendored LiveCodeBench evaluator |
| `4b31d02` | B3 generate: prompts, seeded requests, vLLM, transformers and mock backends, teacher-forced capture, sharded storage |
| `0ff5001` | B1 data: pinned benchmark files, loaders, LiveCodeBench by ID (1,055 IDs, no problem text), agreement inputs, near-duplicate groups, folds |
| `f4d9132` | B4 readouts: every readout of section 7 |
| `2e5e9d0` | B5 statistics and the C1 integration test |
| `b063546` | Masked-LoRA review fixes (`docs/s8/parts/masked_lora_review.md`) |
| `4273175`, `3046cb5`, `eca157f`, `e7f6772`, `5e0ffd9` | C3 first-round fixes per module |
| `9b8f458` | DEV-001 to DEV-014, `docs/s8/CONFORMANCE.md`, the non-blocking analysis warning in `tools/hooks/pre-commit` |
| `91751d8`, `6f130c8` | C3 re-check fixes (N1 to N4, G10), DEV-016, DEV-017 |
| `540e864` | Second re-check fixes (N2, N6 to N9, S1), DEV-018, DEV-019 |
| `41d113e` | C4: DEV-015 and `docs/s8/ANALYSIS_TREE_HASH.txt`; `analysis/results/` git-ignored |
| `ea6ec80` | Third re-check record; data dry-run listing |
| `2ec3d55` | Smoke-run finding: a reused mask-test report is registered in the manifest |
| (this report) | `docs/s8/W8_REPORT.md`, `docs/CONTEXT.md` |

Checks:

- Start state: no unexpected tracked changes; remote HEAD matched local. The frozen design's SHA-256 matched `docs/s7/FROZEN_SHA256.txt`; neither file was touched.
- Every commit passed the pre-commit hook (identity, attribution strings, legacy freeze, design freeze, staged gitleaks). Two rejections, both fixed without a bypass:
  - Fake RunPod keys in `tests/ops` were flagged; they were replaced by low-entropy placeholders.
  - Seven SHA-256 values in `pipeline/generate/card_recommendations.json` were flagged, because their JSON keys contained the word "token". The file was restructured as `{"file", "sha256"}` records.
- One commit (`d4c244b`) went in with a failing test. A `| tail` in the command had masked pytest's exit code. The test was fixed in `4bef8d4`; later commits ran only after a passing suite.
- Full test suite in one process at `41d113e`: exit 0, 753 passed, 3 skipped. After `2ec3d55` added one readouts test, the readouts suite was rerun and passed (section 3 counts include it).
- Gitleaks:
  - Full history (`gitleaks git --redact`, 61 commits through `41d113e`): exit 0, no findings.
  - Staged changes: exit 0.
- Every commit is authored and committed as Palaash Gang.
- Push: after each push, `git ls-remote origin refs/heads/main` equals local HEAD.

## 3. Test counts per module

Collected by `uv run pytest tests --collect-only`; all pass except the three skips.

| Module | Tests | Skipped (why) |
|---|---|---|
| contracts | 11 | |
| data | 67 | |
| execute | 137 | 2 (bubblewrap or a container runtime; pod only) |
| generate | 85 | |
| readouts | 114 | 1 (CUDA) |
| analysis | 69 | |
| ops | 97 | |
| integration (C1) | 6 | |
| prose_lint (earlier waves) | 171 | |
| **Total** | **757** | **3** |

The C1 integration test (`tests/integration/test_pipeline_mock.py`) runs every stage on synthetic data with the mock backend: 8 problems, k = 4, fold seeds 0 to 2. It asserts:

- every stage succeeds;
- labels exist under both suites;
- Shapley efficiency holds to 1e-12 in both chains;
- fold integrity: near-duplicate groups share a fold, and every out-of-fold score sits in its problem's fold;
- no problem leaks between outer train, inner splits, and test;
- the manifest lists every file with a matching hash;
- pilot sealing keeps every Gamma cell, Shapley term, and residual out of the open results.

## 4. Smoke test (C2) and the untrusted-code path

**Path used: reference solutions plus trusted fixtures only.** No container runtime is installed on this Mac, so the container path was not available. The execute stage ran with `execute_untrusted = false`:

- It ran only the reference check (the benchmark's canonical solutions). The 10 generated programs are recorded in `execute/extractions/` and were never executed.
- The local executor tests run only hand-written fixtures. The mock backend's samples are hand mutations of reference code, run only when the backend is mock and `mock_fixtures_trusted` is set.

To exercise readouts and analysis without executing model code, the smoke run uses synthetic labels:

- The labels are a fixed function of (problem, sample index), with means 0.5 under O and 0.4 under E.
- They are marked by `cache_key = "SYNTHETIC-SMOKE-LABEL"` and `execute/SYNTHETIC_LABELS.txt` in the run.
- No smoke metric is a measurement.

Configuration (`ops/plans/smoke.json`):

| Setting | Value |
|---|---|
| Model | SMOKE (Qwen/Qwen3-0.6B) |
| Backend and device | transformers, CPU |
| Problems | 5 HumanEval+ |
| k | 2 |
| Fold seed | 0 |
| LoRA | `lora_max_steps = 2` |
| Bootstrap | B = 200 |
| T1 recipe | own recipe allowed |

The run directory was in the session scratchpad, not in the repo.

| Stage | ok | Seconds | Notes |
|---|---|---|---|
| data | yes | 6.6 | 5 problems, 15 suites, 5 near-duplicate groups (singletons), 200 agreement inputs kept |
| generate | yes | 2,957.4 | 10 samples, 1,747 tokens, 0.59 tokens/s, 0 truncated |
| execute | yes | 4.2 | reference check only; 0 percent reference exclusion under O, E, and agreement; K1 not triggered |
| capture | yes | 392.4 | 10 samples, 3,855 tokens, 10.08 tokens/s; V1 parse rate 1.0 (10 of 10) |
| readouts | yes | 5,746.9 | 30 readouts written (list below); AGREE skipped (no agreement outputs, because no generated code ran); 107 outputs |
| analysis | yes | 3.3 | 1,320 metric rows; budgets, per-seed residuals, pooled, sensitivity, strata, operational |

The 30 readouts: AST, CODETEXT, LAT, MLP, P, P2, P2_single_split, P3, PROMPT, Pmulti, SR, ST, ST_head, ST_r1, ST_r4, ST_r16, SZ_V1, SZ_V1_drop, SZ_V2, TL_geo, TL_min, TL_sum, and the isotonic maps of ST, ST_inner234, ST_insample, SZ_V1, SZ_V1_drop, SZ_V2, TL_geo, and TL_min.

Total wall time: 9,111 seconds (2.5 hours). The Mac was under heavy memory pressure from other processes during the run, with constant swapping, and generation speed reflects that. These timings are not an estimate of pod throughput; the pilot's timing jobs measure that.

Checks on the smoke run:

- **Masked LoRA:** the 7.12 mask test passed on the full float32 model (`config/mask_test_qwen3.json`):
  - non-masked hidden-state and KV differences 0.0;
  - masked positions differ;
  - economy and full-pass log-odds agree to 9.4e-4 (tolerance 1e-3);
  - the negative control differs.

  The minimal masked-LoRA fits ran with recipe selection on inner splits, under O and E. Fold 2 had no fit; with 5 problems, one per fold, a single-class training split is possible.
- **Shapley:** the efficiency gap is 0.0 in both the discrimination and V2 chains.
- **Manifest:** 124 entries, all present with matching hashes. One file, the mask-test report, was not listed: the gate reused a passing report from an earlier interrupted attempt and skipped registration on that path. This is fixed in `2ec3d55`, with a test.
- **Code versions:** generate and capture ran on the code as of `b063546`. Readouts and analysis were rerun on `540e864`, whose `pipeline/` and `analysis/` match the hashed tree (section 6). The first readouts attempt ran on code from before the conformance fixes; it was stopped, and its outputs were deleted before the rerun.

## 5. Conformance summary (C3, `docs/s8/CONFORMANCE.md`)

The opus critic mapped sections 1, 4 to 9, 7.12, and 13 to functions and tests: 152 design-requirement rows, of which 113 MET, 25 PARTIAL, 10 GAP, and 4 DIVERGENT. It raised 22 findings: 3 BLOCKING, 8 MAJOR, and 11 MINOR.

- **BLOCKING:**
  - G1: label-validity fits included problems excluded under the other suite.
  - G2: the pilot could not fit T1's trained readout.
  - G3: T1 lacked the three-seed S^T path.
- **MAJOR:**
  - G4: no producer for the generation shift.
  - G5: no contamination stratum.
  - G6: no sensitivity analyses or capacity rule.
  - G7: K1 was not a gate.
  - G8: the chat-code assembly decision was open.
  - G9: token likelihood was imputed.
  - G10: the timing probes did nothing.
  - G11: the process limit under bwrap as root.

Three re-check passes followed:

- **Re-check 1** found BLOCKING N1, a pre-existing bug: per-benchmark data and execute jobs overwrote the population fold plan and the reference checks, so HumanEval+ would have dropped out of every readout. It also found MAJOR N2 to N5. All are fixed.
- **Re-check 2** found minor items S1 and S2 and noted that N6 to N9 were not yet addressed. All are fixed or logged.
- **Re-check 3:**
  - Of G1 to G22: 16 fixed, 5 logged as deviations (G8, G15, G16, G17, G20), and 1 pod-only operator item (G22, vLLM `top_k=-1`).
  - Of the re-check findings: all fixed or logged.
  - No BLOCKING, MAJOR, or MINOR item is open.

No fix changed a decision rule, an estimand, the margin, the model set, or the k rule, so no stop condition was met.

## 6. Analysis-code hash (C4, section 13)

| Item | Value |
|---|---|
| git tree hash of `analysis/` | `eaedc4a6178152aef5821e4bec1f98361552d9ba` |
| last commit touching `analysis/` | `6f130c8` |
| Recorded in | `docs/DEVIATIONS.md` (DEV-015) and `docs/s8/ANALYSIS_TREE_HASH.txt` |

Verify with `git rev-parse <commit>:analysis`. Generated outputs go to `analysis/results/`, which is git-ignored and outside the tree.

`tools/hooks/pre-commit` section 7 prints a non-blocking warning for any staged change under `analysis/` (excluding `analysis/results/`). The warning is stronger when `docs/DEVIATIONS.md` is not staged.

The analysis stage separately writes its own `analysis_code_sha256` into every result index. In the smoke run that was `e851470d...`, a hash of the module sources rather than a git tree.

## 7. Deviations (`docs/DEVIATIONS.md`)

Nineteen entries, all dated 2026-11-11. No study data existed for any of them.

| ID | Section | Subject |
|---|---|---|
| DEV-001 | 6, R8 | bwrap on the pod (unprivileged uid 65534, no network, rlimits, cgroup pids limit, fork-limit preflight); container optional |
| DEV-002 | 6 | HumanEval/32 find_zero bookkeeping fix over EvalPlus 0.3.1 |
| DEV-003 | 9 vs 11 row 8.4 | Undefined replicates follow section 9 |
| DEV-004 | 4 | Near-duplicate grouping scope |
| DEV-005 | 4 | Agreement canonicalization and patched MBPP+ contracts |
| DEV-006 | 7.4, 7.12 | Unspecified LoRA settings and the split-1 schedule (review M5) |
| DEV-007 | 7.1, 7.11, 13 | Probe K4 retry grid and trigger; MLP weight-decay grid |
| DEV-008 | 5, 7.12 | Yes/No token sets follow 7.12 |
| DEV-009 | 5.6, 5.7 | Chat code executed as extracted; NameError share reported in the pilot |
| DEV-010 | 7.6 | TL_sum probability |
| DEV-011 | 4, 1.2 | Three-player LiveCodeBench game primary; four-player beside it |
| DEV-012 | 13, 7.4 | T1 selects its own recipe in the pilot |
| DEV-013 | 7.12 | Mask test on a float32 slice (wording corrected by DEV-018) |
| DEV-014 | 5 | Authored prompt texts hashed before the pilot |
| DEV-015 | 13 | Pre-pilot analysis-code hash |
| DEV-016 | 5.6 | Correction to DEV-009's reason |
| DEV-017 | 9, 4 | Three-player pooled intervals |
| DEV-018 | 7.12 | Correction to DEV-013's wording |
| DEV-019 | 7.11, 4 | Capacity-rule level, rank-0 rung, LiveCodeBench listing scope, Reading A fallback count |

The operator's LiveCodeBench decision (IDs and a fetch script only) needed no entry, because sections 4 and 14.1 already say so.

## 8. Operator pilot checklist

Environment variables. Set them in the shell or in an untracked `.env`, and never in a tracked file.

| Name | Where | Purpose |
|---|---|---|
| `RUNPOD_API_KEY` | Mac | RunPod REST API key (launch, stop, terminate) |
| `HF_TOKEN` | Mac, passed to the pod by name (`--env-names HF_TOKEN`) | Hugging Face downloads at the pinned revisions |
| `POD_SSH_HOST`, `POD_SSH_PORT`, `POD_SSH_USER`, `POD_SSH_KEY` | Mac | sync and the remote guard reader (printed redacted) |
| `RUNPOD_GPU_TYPE_ID` (optional) | Mac | overrides the default GPU type ID |
| `RUNPOD_IMAGE` (optional) | Mac | default pod image |
| `RUNPOD_API_BASE` (optional) | Mac | API base URL override (tests only) |
| `RUNPOD_POD_ID` | Mac | written locally at launch; read by `stop` |

Before launch:

1. **Gemma license.** In a browser, open the model pages for `google/gemma-4-12B-it` and `google/gemma-4-31B-it` while logged in with the account that owns `HF_TOKEN`, and accept the terms if any are shown. The frozen design lists them as ungated; `bash ops/bootstrap.sh` checks access for every pinned model and stops if any is refused.
2. **GPU.** Use one RTX PRO 6000 (Blackwell). The default type ID is `NVIDIA RTX PRO 6000 Blackwell Server Edition`. Check the exact string in the RunPod console and pass `--gpu-type-id "<string>"` if it differs.
3. **Pod template or image.** Use a CUDA 13 capable PyTorch base image with Python 3.12, and pass it as `--image <name:tag>` or `--template-id <id>`. The pod must allow unprivileged user namespaces for bwrap; `bootstrap.sh` runs the sandbox preflight, including the fork-limit probe, and stops if it fails. If user namespaces are not available, pass `--container-image <name@sha256:...>` instead.
4. **Price.** Read the hourly price for that GPU in the RunPod console at launch time, then pass `--hourly-price-usd <price>` and `--price-source "<page and time you read it>"`. The launch appends the row to `runs/COST_LEDGER.csv`.

Commands, run from the repo root:

1. Dry run of the pilot launch (calls nothing, prints every action redacted):
   `uv run python -m ops launch --plan pilot --hourly-price-usd <price> --price-source "<source>" --image <image>`
2. Real launch:
   `uv run python -m ops launch --plan pilot --hourly-price-usd <price> --price-source "<source>" --image <image> --execute`
3. Set up the pod and run the plan:
   - On the pod, clone to `/workspace/calib-disconnect` and run `bash ops/bootstrap.sh --plan pilot --dry-run`, then `bash ops/bootstrap.sh --plan pilot`.
   - Then run `uv run python -m ops run --plan pilot --execute --keep-going`.
   - Alongside it, run `uv run python -m ops guard --run-id pilot --launched-at <UTC from the launch output> --execute`. The guard's GPU-hour cap defaults to 7.5.
4. Sync, then stop:
   - `uv run python -m ops sync --run-id pilot --skip-large --execute`.
   - Then `uv run python -m ops stop --execute`, and `uv run python -m ops ledger summary`.

## 9. [OPERATOR] items with exact actions

1. **RunPod key and token.** Export `RUNPOD_API_KEY` and `HF_TOKEN` on the Mac, or put them in an untracked `.env`.
2. **Gemma license.** Accept it on both Gemma 4 model pages, if shown (checklist item 1).
3. **GPU type ID.** Confirm the exact RTX PRO 6000 type ID and the REST fields in the RunPod console (checklist item 2). `ops/runpod_api.py` follows the documented REST shape (`gpuTypeIds`, `imageName` or `templateId`, `volumeInGb`, `env`) and has not been called live.
4. **Image or template.** Choose the image or template, and confirm it allows user namespaces (checklist item 3).
5. **Hourly price.** Record it at launch through `--hourly-price-usd` and `--price-source`.
6. **vLLM settings (G22).** On the pod, confirm that vLLM 0.33.0 accepts `top_k=-1` (no request error in the first T1 generate job) and that base-model completions stop at the strings in `pipeline/execute/extract.py` (look at the first T1 generation shard). Also run `uv run pytest tests -m pod`, which exercises the two real sandbox tests; no vLLM test exists.
7. **K1 acceptance.** If K1 fires in the pilot, the execute stage stops. To accept the exclusion list, write `runs/pilot/config/k1_accepted.json` listing exactly the excluded (problem_id, suite_id) pairs; otherwise fix the cause.
8. **Former GPU host key (from W0).** Rotate it, and the host, if still live.
9. **LiveCodeBench license (R16).** Still open. Only IDs and a fetch script are released.

## 10. What is not done

- No pod run happened. The bwrap sandbox, the cgroup pids limit, vLLM, CUDA paths (one test), and the RunPod API are tested only with fakes or dry runs.
- The smoke test did not execute generated code; its labels are synthetic.
- The readouts suite takes about 5 to 6 minutes, and the full suite about 15 minutes, on this Mac.
