# Contract requests from pipeline.readouts (B4)

1. Token layouts for LoRA readouts (real backend). `TeacherForcedLayout` (prompt, completion, and elicitation
   token IDs) cannot be rebuilt from the capture index. Please provide
   `pipeline.generate.layouts:teacher_forced_layouts(cfg, layout, model_key, benchmarks, sample_uids, tokenizer)
   -> list[TeacherForcedLayout]` aligned to `sample_uids`, or set `cfg.extra["layouts_provider"]` to another
   "module:function". Without it the real backend stops with a RuntimeError and the stage reports `ok=False`.
2. Readout names beyond `READOUTS`: `SZ_V1_drop` (V1 with unparsed rows dropped), `AGREE_problem` (largest-cluster
   share), `iso:SZ_V1_drop`, `iso:ST_inner234` (map fit on inner splits 2 to 4), `iso:ST_insample` (in-sample map).
   Please add them to `READOUTS` or tell analysis to read them by name.
3. `config/answer_tokens.json` format: the stage reads `{model_key: {"yes": [ids], "no": [ids]}}` if present and
   otherwise scans the tokenizer. Please confirm or state the real format.
4. Per-model V1 parse rate and the K3 switch are written to `readouts/<model>/<population>/SZ_V1/none/parse_rate.json`
   (no `layout` path exists for it). Recipes: `readouts/<model>/<population>/ST/recipes_seed<s>.json`.
5. Fit records may contain null for undefined losses (NaN is written as null).
