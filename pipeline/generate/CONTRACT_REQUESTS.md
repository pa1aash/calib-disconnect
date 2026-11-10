# Contract requests and divergences (B3)

1. **bfloat16 arrays are torch tensors.** numpy has no bfloat16 and ml_dtypes is not installed, so
   `CaptureBackend.capture` returns `hs_*` as `torch.bfloat16` tensors (other arrays are numpy). Readers use
   `pipeline.generate.storage.load_capture_shard`, which returns float32 numpy. Suggest the contract say so.
2. **Extraction failures.** `n_code_tokens = 0`, `code_token_span = (p2 + 1, p2 + 1)`, and the three
   log-prob summaries are NaN (no code tokens). `hs_mean_code` falls back to the mean over the generated
   completion tokens. B4 must treat NaN token-likelihood scores as missing. Please confirm or specify another rule.
3. **Bridge tokens.** The whitespace between the end-of-turn token and the user header (for example the
   newline after `<|im_end|>`) is appended to `completion_ids`, so the sequence equals the template render.
   The elicitation span starts at the first header token. For truncated samples no end-of-turn token or bridge is appended.
4. **Seeds to engines** are passed as signed 64-bit (two's complement of the unsigned seed) because vLLM
   validates signed longs. The recorded `seed` stays unsigned.
5. **`prompt_sha256`** is the SHA-256 of the unfilled template actually used (`gen_chat.txt` with the payload
   file substituted, or `base_completion_function.txt`); component hashes are in `config/prompts.json`.
6. Generation user messages have trailing newlines stripped. Base-model stop strings (EvalPlus style) are
   not verified against the installed evalplus source. vLLM `top_k=-1` and `generation_config="vllm"` are not verified on 0.33.0 (pod only).
7. Capture shard indices follow generation shard indices one to one; shards are chunked within blocks of 10
   sample indices so adding samples 11..20 never changes earlier shards.

## Gemma 4 thought markers (G21), for pipeline/execute/extract.py (owner: orchestrator)

Verified by rendering the pinned chat template (`google/gemma-4-12B-it` at 43c9d014..., same template file
hash for the 31B model) with jinja2; tokenizer_config.json names `<|channel>` (soc), `<channel|>` (eoc), `<turn|>` (eot).
- Thinking off: the generation prompt itself ends with `<|channel>thought\n<channel|>`. The empty block is
  therefore in the prompt, not emitted by the model, so completions normally contain no thought block.
- Thinking on: the block is `<|channel>thought\n` ... `<channel|>`, followed by the answer.
- Correct `THOUGHT_MARKERS` entry: `("<|channel>thought", "<channel|>", False)` (the existing `empty_only=True`
  entry with these strings is right for thinking off; allow non-empty for thinking on). Remove the unverified
  `("<|channel|>thought", "<|channel|>", ...)` and `("<start_of_thought>", "<end_of_thought>", ...)` entries.
- `BASE_STOP_STRINGS` is now imported by `pipeline.generate.prompts` from `pipeline.execute.extract`.

## Timing-only jobs (G10)

`cfg.extra["timing_only"]`: generate writes only generation set "timing" (always rewritten); capture runs the
forward passes over it and stores nothing; timings go to `StageReport.metrics` and `logs/timing_<model>.json`.
Normal capture ignores the "timing" directory. Readouts and ops must not read it.
