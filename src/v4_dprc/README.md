# DPRC — Decoupled Per-Requirement Confidence for code LLMs (AAAI-27 extension)

Turns the diagnostic "Calibration Disconnect" into a prescriptive method: train a 7B code LLM to
**self-express calibrated, discriminative confidence at per-test-case / per-requirement granularity**
— localizing *which requirement its own solution will fail*. Full rationale + gates: the research
report at `research/notes/final_report_code-llm-calibration-aaai27-eabf3f.md`.

## Module map

| File | Role | Tested |
|---|---|---|
| `config.py` | paths, model registry, **frozen** hyperparams + gate thresholds | — |
| `metrics.py` | validated ECE/TACE/Brier/AUROC (from v3) + **problem-level grouped bootstrap** | ✅ self-test |
| `pertest_harness.py` | **Build #1** — split tests → `[n_sol×n_test]` pass matrix + flaky/broken discard (CPU-parallel) | ✅ self-test |
| `grouping.py` | requirement grouping: **L1** per-test / **L2** per-category (frozen taxonomy) | ✅ self-test |
| `loaders.py` | per-test loaders: HumanEval, MBPP (tested) · APPS, TACO, LiveCodeBench (**Build #2**, run on box) | ✅ HE/MBPP |
| `serialization.py` | **Build #3** — persist per-test outcomes + code + manifest (GATE-1 spread) | ✅ round-trip |
| `sampling.py` | `VLLMGenerator` (GPU) + `StubGenerator` (CPU dry-run) | ✅ dry-run |
| `label_dataset.py` | **Phase 1** driver: sample+label + **GATE-0**/**GATE-1** | ✅ e2e dry-run |
| `conf_block.py` | structured confidence block + **tokenized-Brier** scoring math | ✅ self-test |
| `train_dprc.py` | **Build #4a** — DPRC stage-(a) LoRA SFT (`--loss ce|brier`); data-prep tested | ✅ data-prep |
| `pilot.py` | **Pilot + GATE-2** (per-requirement AUROC → L1/L2/L3 verdict) | ✅ gate logic |
| `setup_lambda.sh` | box bootstrap (pin deps, warm cache, run CPU self-tests) | — |

"Tested" = verified on this laptop (CPU). GPU paths (`VLLMGenerator`, `train_dprc.train`,
`pilot.elicit_confidence`) are written and import-clean but run first on the box.

## Run order on the box (Phases 0→2, the critical path to the 07-20 pilot gate)

```bash
bash setup_lambda.sh                         # Phase 0: env + warm cache + CPU self-tests

# GATE-0 timing pilot (executions are CPU — can run off the GPU):
python3 label_dataset.py --limit 50 --stub   # confirm harness throughput + GATE-0 extrapolation

# Phase 1: free labels (GPU for generation; executions CPU). Reads GATE-0/GATE-1 automatically.
python3 label_dataset.py --sources mbpp apps taco livecodebench --limit 3000 --model qwen2.5-coder-7b \
        --out data/v4_dprc/labels/pool.jsonl
#  -> inspect data/v4_dprc/labels/pool_manifest.json : GATE-1 needs spread_fraction >= 0.20

# Phase 2 PILOT (Qwen, ~300 problems, must finish by 07-20):
python3 train_dprc.py --labels data/v4_dprc/labels/pool.jsonl --level l1 --loss ce   # stage-(a) warm-start
python3 pilot.py --labels <held-out-slice>.jsonl --adapter data/v4_dprc/adapters/dprc_qwen2.5-coder-7b_l1_ce
#  -> GATE-2: per-test AUROC > 0.65 => L1 ; else per-category > 0.65 => L2 ; else => L3
```

## Gates (pre-registered — a fail blocks the next phase)

- **GATE-0** (`label_dataset.estimate_gate0`): full-pool executions ≤ ~2 days wall-clock (CPU pool) AND
  GPU-$ ≤ ~$375. Fail → de-scope pool / add CPU cores / cut DeepSeek to a supporting panel.
- **GATE-1** (`label_dataset.check_gate1`): ≥ enough problems with ≥2 groups AND
  `spread_fraction_intermediate ≥ 0.20`. Fail → enrich pool with harder TACO/LiveCodeBench.
- **GATE-2** (`pilot.gate2`): pilot per-test (or per-category) AUROC > 0.65 by **07-20** → picks the
  AAAI-27 headline level (L1/L2/L3). The abstract (07-21) commits to the *capability*, not a number.

## What is NOT built yet (deliberately — downstream of GATE-2)

- **Stage-(b)**: masked-gradient decoupled RL refinement (DCPO-style `R_c=−|conf−R_IG|` with token-block
  advantage masking). Build only if GATE-2 → L1 and the CE warm-start shows real per-test signal.
- **Phase 3–5**: full two-model run, the 6 ablations, and the selective-generation floor (`metrics` +
  a Clopper-Pearson wrapper). These reuse the modules above; scaffold after the pilot.

## Frozen for reproducibility (AAAI checklist)
Seeds, LoRA config, sampling params, the L1/L2 grouping taxonomy, gate thresholds, and the
LiveCodeBench eval window all live in `config.py`. Do not change them mid-run.
