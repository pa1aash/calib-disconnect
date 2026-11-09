> **Legacy document (banner added in wave 2, 2026-11-10).** This guide describes the legacy v1 to v3
> bundle, which is now frozen (see `docs/LEGACY.md`). Seven script-to-output attributions in section 2
> below are incorrect. Corrected attributions are in `docs/s1/BUNDLE_MAP.md`, section 3.6
> ("Documentation errors in REPRODUCE.md §2"). The body below is unchanged.

# Reproduction Guide

This guide explains how the project is structured and how to reproduce each iteration.
Scripts were written to run on a remote GPU box at the path
`/home/ubuntu/dl4c_experiments/` (hard-coded `RESULTS_DIR` paths). To reproduce, either
run on such a box or edit the `RESULTS_DIR` constant near the top of each script.

> Nothing in this folder was renamed, deleted, or edited during organization — files
> were only moved into subfolders. The paths below reflect the new locations.

---

## 1. Environment

- **GPU:** NVIDIA GH200 480GB (98GB VRAM) — see `docs/research-state.md` for the box
  details. Some v2 runs used an A100-40GB (`src/v2_comprehensive/exp_final_a100.py`).
- **Python deps** (installed on the GPU box by `src/v3_multimodel/deploy_v3.sh`):

  ```bash
  pip install scikit-learn datasets transformers peft accelerate torch
  # v1 baseline also uses vLLM (see src/v1_baseline/exp1_vllm.py)
  pip install vllm
  ```

- **Datasets** (auto-downloaded via HuggingFace `datasets`):
  - `openai_humaneval` (test, 164 problems)
  - `google-research-datasets/mbpp` (sanitized, test, 500 problems)

---

## 2. Data flow: which script produces which result

### v1 — baseline pipeline (`src/v1_baseline/` -> `results/v1/`)

| Script | Role | Output |
|--------|------|--------|
| `exp1_baseline_calibration.py` | Baseline calibration measurement (ECE/Brier/AUROC) | `results/v1/exp1_qwen2.5-coder-7b_humaneval.json`, `..._mbpp_fixed.json` |
| `exp1_vllm.py`, `exp1_optimized.py`, `exp1_streamlined.py`, `exp1_final.py` | Iterative speed/robustness variants of Experiment 1 | (same exp1 JSONs) |
| `exp2_dpo_training.py` | Confidence-aware DPO training (LoRA) | trained adapter on GPU box |
| `exp3_post_training_eval.py` | Post-training calibration eval | JSON on GPU box |
| `exp4_trust_study.py` | Simulated trust-calibration study | JSON on GPU box |
| `run_all_experiments.py` | Runs exp1–exp4 sequentially with logging | `experiment_log.json` |

Run all of v1:

```bash
cd src/v1_baseline
python run_all_experiments.py
```

### v2 — comprehensive revision (`src/v2_comprehensive/` -> `results/v2/`)

| Script | Role | Output |
|--------|------|--------|
| `exp_v2_comprehensive.py` | Temp-aligned confidence + labels, bootstrap CIs, log-prob baseline, `tau`/`n` sensitivity | `results/v2/main_humaneval.json`, `main_mbpp.json`, `sensitivity_tau_*.json`, `sensitivity_n_*.json` |
| `exp_final_a100.py` | Remaining runs on A100-40GB: n=20 sensitivity + SFT train/eval | `results/v2/sensitivity_n_20.json`, `sft_training_metrics.json`, `sft_evaluation.json` |
| `exp34_eval.py` | SFT model eval + trust study (CUDA-error tolerant) | `results/v2/sft_evaluation.json` |
| `sft_eval_only.py` | Focused SFT evaluation, one model at a time | `results/v2/sft_evaluation.json` |
| `run_all_v2.py` | All-in-one v2 runner (fixes MBPP exec, reruns baselines, DPO, eval, trust) | multiple `results/v2/*.json` |

Run the main v2 pipeline:

```bash
cd src/v2_comprehensive
python run_all_v2.py            # or: python exp_v2_comprehensive.py
python exp_final_a100.py        # SFT + n=20 (A100 leg)
```

### v3 — multi-model + reviewer response (`src/v3_multimodel/` -> `results/v3/`)

| Script | Role | Output |
|--------|------|--------|
| `exp_v3_multimodel.py` | Second model (DeepSeek-Coder), quantitative SFT eval w/ bootstrap CIs, n=20 sensitivity, cross-model summary | `results/v3/v3_qwen2.5-coder-7b_humaneval.json`, `v3_deepseek-coder-6.7b_humaneval.json`, `sft_discrimination.json`, `harness_info.json` |
| `exp_v3_all.py` | Reviewer-R2 experiments: independent label draw, same-temp verbal elicitation, isotonic-regression log-prob baseline, AST-clustering proxy confidence | `results/v3/*.json` |
| `deploy_v3.sh` | Copies script to GPU box, installs deps, launches under `nohup` (disconnect-safe) | remote `v3_log.txt` |

Deploy and run v3 on the GPU box:

```bash
cd src/v3_multimodel
bash deploy_v3.sh <GPU_IP>     # defaults to [REDACTED-IP]
# monitor: ssh -i <key> ubuntu@<IP> 'tail -f /home/ubuntu/dl4c_experiments/v3_log.txt'
```

> `deploy_v3.sh` expects the SSH key at `/tmp/[REDACTED-KEYFILE]`. Copy
> `credentials/[REDACTED-KEYFILE]` there first (and `chmod 600`), or edit the `KEY`
> variable in the script.

---

## 3. Building the papers

Each `papers/vN/` directory is self-contained (includes its own ICML 2026 `.sty`/`.bst`
files, `references.bib`, and the compiled `main.pdf`). To rebuild:

```bash
cd papers/v3            # latest; or v1 / v2
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The pre-compiled `main.pdf` is already present in each directory.

---

## 4. Reproduction order (recommended)

1. Read `docs/methodology.md` for the full experimental design.
2. Provision a GH200 (or comparable) GPU box; install deps (Section 1).
3. Run **v1** (`src/v1_baseline/run_all_experiments.py`) for baselines.
4. Run **v2** (`src/v2_comprehensive/run_all_v2.py` + `exp_final_a100.py`) for the
   rigorous revision.
5. Run **v3** (`src/v3_multimodel/deploy_v3.sh`) for multi-model generalization.
6. Rebuild the latest manuscript in `papers/v3/`.

Expected end-to-end compute: ~7 hours per model set on a GH200 (see
`docs/methodology.md`, "Compute Requirements").

---

## 5. Notes & caveats

- **Hard-coded paths:** scripts write to `/home/ubuntu/dl4c_experiments/results*`.
  Edit `RESULTS_DIR` at the top of each script if running elsewhere; then copy the
  produced JSONs back into the matching `results/vN/` folder.
- **`misc/nul`** is a Windows redirect artifact, not a real data file. Safe to ignore.
- **`archives/*.zip`** are frozen submission snapshots of the v1/v2 papers and the
  original ICML style bundle — kept for provenance.
