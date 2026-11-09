# The Calibration Disconnect: Calibrated Uncertainty Communication in Coding Agents

Research project investigating whether code LLMs can be post-trained to produce
**calibrated verbal confidence signals** that correlate with actual code correctness,
and whether exposing these signals improves human-agent collaboration on coding tasks.

Target venue: **DL4C** (Deep Learning for Code) / ICML 2026 style.

> **Note on organization.** This folder was reorganized into subdirectories for
> clarity and reproducibility. **No files were renamed, deleted, or edited** — every
> original file keeps its exact name and contents; files were only moved into folders.
> See `REPRODUCE.md` for the full script-to-result mapping and run instructions.

---

## Research Question

Can code LLMs be post-trained to produce calibrated verbal confidence that correlates
with actual code correctness, and does exposing these signals improve human-agent
collaboration in coding tasks?

**Core idea:** Code is *verifiable* — we can execute solutions against test cases to get
cheap ground-truth "should the model have been confident?" labels. This gives a cleaner
calibration signal than general NLP tasks where correctness is subjective.

---

## Directory Layout

```
.
├── README.md                  <- this file
├── REPRODUCE.md               <- step-by-step reproduction guide + script/result map
│
├── docs/                      <- research planning & literature (chronological record)
│   ├── research-state.md              scope, GPU details, experiment log
│   ├── literature-review.md           50+ papers across 5 facets
│   ├── reasoning.md                   hypotheses & research deliberation
│   ├── methodology.md                 full experimental design (4 experiments)
│   └── uncertainty_code_generation_papers.md   annotated bibliography
│
├── src/                       <- experiment code, grouped by paper iteration
│   ├── v1_baseline/                   original 4-experiment pipeline
│   ├── v2_comprehensive/              revised: temp alignment, bootstrap CIs, sensitivity
│   └── v3_multimodel/                 multi-model generalization + reviewer response
│
├── results/                   <- experiment outputs (JSON), grouped by iteration
│   ├── v1/                            baseline calibration (Qwen2.5-Coder-7B)
│   ├── v2/                            HumanEval/MBPP, sensitivity sweeps, SFT eval
│   └── v3/                            multi-model (Qwen + DeepSeek), SFT discrimination
│
├── papers/                    <- LaTeX manuscripts, one self-contained dir per version
│   ├── v1/                            main.tex, references.bib, .sty, compiled main.pdf
│   ├── v2/                            "
│   └── v3/                            "  (latest)
│
├── archives/                  <- zipped snapshots
│   ├── dl4cV1.zip                     paper v1 submission bundle
│   ├── dl4cV2.zip                     paper v2 submission bundle
│   └── icml2026_styles.zip            original ICML 2026 style template
│
├── credentials/               <- SSH key for the GH200 GPU box (DO NOT COMMIT)
│   └── [REDACTED-KEYFILE]
│
└── misc/                      <- stray/artifact files
    └── nul                            accidental Windows redirect artifact
```

---

## Project Iterations

The project went through three revision cycles. Each has its own code (`src/`),
results (`results/`), and manuscript (`papers/`):

| Version | Focus | Key additions |
|---------|-------|---------------|
| **v1** | Baseline pipeline | 4 experiments: baseline calibration, confidence-aware DPO, post-training eval, simulated trust study |
| **v2** | Rigor & robustness | Temperature-aligned confidence/labels, bootstrap CIs, sensitivity sweeps over `tau` and `n`, log-prob baseline, SFT ablation |
| **v3** | Generalization & reviewer response | Second model (DeepSeek-Coder), independent label draw, same-temperature verbal elicitation, isotonic-regression baseline, AST-clustering proxy confidence |

---

## Methods (summary)

- **Models:** Qwen2.5-Coder-7B-Instruct, DeepSeek-Coder-6.7B/V2-Lite, CodeLlama-13B.
- **Benchmarks:** HumanEval (164), MBPP (500).
- **Confidence signals:** logit-based, sampling/consistency-based, verbalized (1–5 scale).
- **Metrics:** ECE (Expected Calibration Error), Brier score, AUROC, pass@1 / pass@10.
- **Post-training:** confidence-aware DPO (LoRA) and SFT ablation.
- **Hardware:** NVIDIA GH200 480GB (98GB VRAM); some v2 runs on A100-40GB.

Full design is in `docs/methodology.md`.

---

## Security note

`credentials/[REDACTED-KEYFILE]` is a private SSH key for the GPU instance. Keep it out
of version control and rotate it if this folder is ever shared. Add `credentials/` to
`.gitignore` before committing anywhere.
