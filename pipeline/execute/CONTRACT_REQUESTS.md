# Contract requests and open questions (B2, pipeline.execute)

No contract file was edited. Requests for the orchestrator:

1. `layout.py`: add a property for `execute/agreement_label_proxy.json` (the stage writes `layout.root / "execute" / "agreement_label_proxy.json"`).
2. `schemas.ExecutionResult.sandbox` vocabulary: this module also emits `"bwrap"` (comment lists container, rlimit-subprocess, fixture). `Executor.name` is the backend string (`"trusted-only"` on the Mac, not `"fixture"`).
3. `Executor` protocol: this module adds `cache_key(code, problem, suite, *, capture_outputs=False)`, `run_reference(...)`, and `preflight_limits()`. `label_samples` takes extra keyword arguments `trusted`, `workers`, `excluded`; `extract_code` takes keyword-only `benchmark` and `stop_strings`.
4. `Problem` has no input-contract field, so "reference fails its own contract" is implemented as "reference fails its own pass criterion against its recorded outputs".
5. Question for the design owner (rows 5.6 and 5.7): extracted chat code is run as is. If a model omits `from typing import ...` or a helper function defined in the HumanEval prompt, the sample fails with NameError. EvalPlus's own sanitizer would add them. Decide whether to prepend the prompt's imports and helpers.
6. B1 must keep storing MBPP+ inputs in EvalPlus JSON form (the stage applies `mbpp_deserialize_inputs`), and LiveCodeBench inputs and expected outputs as the native strings.
7. The Gemma 4 empty-thought marker spellings in `extract.THOUGHT_MARKERS` are not verified against the model card.
