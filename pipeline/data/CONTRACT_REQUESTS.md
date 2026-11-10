# Contract requests and notes from B1 (pipeline.data)

No contract file was edited. Items for the orchestrator:

1. **Input encoding (note for pipeline.execute).** HumanEval+/MBPP+ `TestSuite.inputs` hold the EvalPlus
   JSON form. Call `pipeline.data.inputs.decode_inputs(problem_id, suite.inputs)` before running any
   input; it applies EvalPlus `mbpp_deserialize_inputs` (lists back to tuples, complex, and so on).
   LiveCodeBench inputs are the raw input strings of the shards; function problems keep one JSON
   argument per line. `Problem.canonical_solution` for HumanEval+ is the complete program (prompt plus body).
2. **Patched MBPP+ tasks and their contracts.** The pinned patch renames parameters of Mbpp/102
   (word to snake_str) and Mbpp/559 (a, size to arr, n) and re-indents the body, so the stored EvalPlus
   contract raises NameError or IndentationError against the patched solution. Label inputs and the stored
   contract are unchanged; only agreement-input generation uses an adapted contract
   (`evalplus_data.adapt_contract`). Worth a line in docs/DEVIATIONS.md.
3. **LiveCodeBench suites size.** `suites_lcb_v6.jsonl` repeats every test in lcb_label, lcb_full, and
   (private part) agree, so it may be several times the size of the shards. Not measured (shards were not
   downloaded). A reference-by-index suite schema would avoid this if it matters.
4. **Manifest saving.** The stage adds entries to the `Manifest` object but does not call `save`.
5. **Agreement input coverage.** Some problems end with an empty "agree" suite (all generated inputs equal
   label inputs, or none valid); counts are in `data/agreement_inputs_stats.json`.
