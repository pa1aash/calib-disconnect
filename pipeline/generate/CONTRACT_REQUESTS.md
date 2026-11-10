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
