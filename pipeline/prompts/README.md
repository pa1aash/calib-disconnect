# Frozen prompts (design section 5)

Every file here is frozen before the pilot. `PROMPTS.sha256.json` records the SHA-256 of each file;
`pipeline.generate.prompts` refuses to render a prompt whose file hash differs from the recorded hash,
and checks `elicit_v1.txt` and `elicit_v2.txt` byte for byte against the verbatim text of section 5
(`pipeline/contracts/constants.py`). A change to any file is a deviation (`docs/DEVIATIONS.md`).

| File | Use | Placeholders |
|---|---|---|
| `gen_chat.txt` | Generation prompt (user turn) for every instruct model and every benchmark; the two benchmark families differ only in the payload | `{payload}` |
| `payload_function.txt` | Payload for HumanEval+ and MBPP+: the EvalPlus prompt (signature and docstring) | `{prompt}` |
| `payload_lcb_functional.txt` | Payload for LiveCodeBench problems with starter code | `{statement}`, `{starter_code}` |
| `payload_lcb_stdin.txt` | Payload for LiveCodeBench standard-input problems | `{statement}` |
| `elicit_v1.txt` | Elicitation format V1 (numeric), verbatim from section 5 | none |
| `elicit_v2.txt` | Elicitation format V2 (categorical), verbatim from section 5 | none |
| `base_completion_function.txt` | Completion-style generation prompt for base models (section 10): the EvalPlus prompt itself; stop strings in `pipeline.generate.prompts` | `{prompt}` |
| `base_elicitation_frame.txt` | Plain-text dialogue frame for base-model elicitation (section 10); `{question}` is the V1 or V2 text | `{program}`, `{question}` |
| `rtuning_sure.txt`, `rtuning_unsure.txt` | R-Tuning-style suffixes (section 7.5) | none |

The chat template of each model is applied by the tokenizer at its pinned revision, with
`enable_thinking=False` where the model supports it (thinking-on runs set it to True), and the
rendered text's SHA-256 is recorded per sample (`GenerationRecord.rendered_prompt_sha256`).
