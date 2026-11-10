# pipeline

Evaluation code for the frozen design (`docs/s7/PIPELINE_DESIGN_FROZEN.md`). Legacy code under `src/` is
frozen and is not imported or modified (`docs/LEGACY.md`).

| Package | Contents |
|---|---|
| `pipeline/contracts/` | Constants, hash encodings, schemas, on-disk layout, manifest format, module interfaces (read first) |
| `pipeline/prompts/` | Frozen prompt files with `PROMPTS.sha256.json` |
| `pipeline/data/` | Pinned benchmarks, MBPP+ patch, LiveCodeBench by ID, agreement inputs, near-duplicate groups, folds |
| `pipeline/execute/` | Code extraction, sandboxed execution, execution cache, labels, reference check |
| `pipeline/generate/` | Generation backends (vLLM on the pod, transformers on CPU for the smoke test, mock), capture pass, shards |
| `pipeline/readouts/` | Every readout of design section 7, cross-fitting, isotonic maps, masked LoRA, R-Tuning-style readout |
| `analysis/` | Statistics (metrics, bootstrap, refit widening, Shapley, decisions, k rule, reconciliation) |
| `ops/` | Pod bootstrap, job runner, output sync, cost guard, RunPod API driver, dry run |

Environment: `uv sync --group local` on the Mac (CPU), `uv sync --group pod` on the GPU pod. Tests:
`uv run pytest`.
