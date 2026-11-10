# Provenance: LiveCodeBench evaluator (vendored verbatim)

| Field | Value |
|---|---|
| Repository | https://github.com/LiveCodeBench/LiveCodeBench |
| Commit | `28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24` (latest commit of the default branch `main` when retrieved; committed 2025-07-16, message "fix: typo in the Explorer URL top README (#109)") |
| Retrieved | 2026-11-10, with `gh api -H "Accept: application/vnd.github.raw" repos/LiveCodeBench/LiveCodeBench/contents/<path>?ref=<commit>` |
| Licence | MIT (repository `LICENSE`, copied here as `LICENSE`) |

| File | Source path at that commit | Git blob SHA | SHA-256 |
|---|---|---|---|
| `testing_util.py` | `lcb_runner/evaluation/testing_util.py` | `ecc89474b813cb552ae060a53b3a7da534476968` | `b7cb6a8a69807bb868150a61742e25d7bb5328bbe01d514471b6ec43c9fa9ed2` |
| `LICENSE` | `LICENSE` | not recorded | `104099948b78ebc36f2e951b3a7973b956adfa7d39aaec0d1512f97a2686d15d` |

The blob SHA of `testing_util.py` equals `git hash-object` of the local file, so the file is byte-identical
to the upstream blob.

## Use

`testing_util.py` is self-contained apart from the standard library and numpy, so no other upstream file is
needed. `pipeline/execute/harness.py` imports it inside the sandbox and calls `run_test(sample, test=code,
timeout=6)`, which is the call `lcb_runner/evaluation/compute_code_generation_metrics.py` makes. The upstream
pass rule (`pass_k_utils.py`, every per-test result greater than zero) is applied in the harness.

## Changes to vendored files

None. The only adaptation is the separate file `pipeline/execute/lcb_capture.py`, which records outputs
for agreement signatures; its docstring lists every difference from the upstream logic.

## Notes

- The upstream whole-run guard is `(timeout + 1) * n_tests + 5` seconds; this pipeline uses the design's
  60 s whole-program cap instead (design section 6), and the evaluator's own per-test `timeout=6`.
- `run_test` calls the upstream `reliability_guard()`, which does not set a memory limit; the sandbox
  applies the 2 GB limit before calling it.
