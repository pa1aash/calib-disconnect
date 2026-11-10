# Contract change log

Contracts were written in wave 8 Part A, before any module build. Any change after Part B starts is
made by the orchestrator only and is listed here with the date, the file, the change, and the reason.

| Date | File | Change | Reason |
|---|---|---|---|
| 2026-11-10 | all | Initial contracts: constants, hashing, schemas, layout, manifest, interfaces; prompts frozen in `pipeline/prompts/` | Part A |
| 2026-11-11 | layout.py | `RunLayout.scores` and `fits` take `gen_set` (default "frozen", path unchanged); other generation sets add a directory level | Fresh-sample scores (generation shift, reading A) would otherwise overwrite frozen scores (B5 request) |
| 2026-11-11 | layout.py | (Part A, before Part B) `agreement_outputs` and `reference_outputs` paths | Needed by the execute stage |
