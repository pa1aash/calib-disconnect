# Forward-citation screen G2 (recovered by the orchestrator)

Retrieval date 2026-11-10. The G2 sub-agent fetched the raw citation records (`raw/`) but stopped before writing its screening files. The orchestrator screened the saved records by title and abstract (ABSTRACT-ONLY) and wrote this file and `NEW_CLOSE.md`. Merge script: titles normalized and deduplicated across Semantic Scholar and OpenAlex; vault presence checked by arXiv id and title prefix over `research/notes`.

## Counts per seed

| Seed | Semantic Scholar citers (page 1) | OpenAlex `cites:` | Gap |
|---|---|---|---|
| arXiv:2402.02047 (Spiess et al.) | 100 (no `next` page; at the limit of 100, so a cap cannot be excluded) | 200 | Possible S2 cap at 100: gap |
| arXiv:2512.08810 | 4 | 429 | OpenAlex budget exhausted: gap |
| arXiv:2502.11620 | 26 | 429 | OpenAlex gap |
| arXiv:2606.09577 | 5 | 429 | OpenAlex gap |
| arXiv:2605.28500 | 3 | 429 | OpenAlex gap |
| arXiv:2607.12273 | 0 | 429 | OpenAlex gap |
| arXiv:2605.09023 | 1 | 429 | OpenAlex gap |
| arXiv:2610.11300 | 1 | 429 | OpenAlex gap |
| arXiv:2603.27098 | 0 | 429 | OpenAlex gap |
| arXiv:2505.13553 | 1 | 429 | OpenAlex gap |
| DOI:10.18653/2026.uncertainlp-main.21 | 0 | 429 | OpenAlex gap |

Merged distinct citers: 149, of which 27 are already in the vault.

## CLOSE (not in vault)

See `NEW_CLOSE.md`.

## RELATED (not in vault)

2606.27359 (sequence probability and correctness), 2601.07965 (calibration, cascading, cleaning), 2511.12288 (semantic triangulation for code hallucination), 2608.24492 (supervised UQ ensembles robustness), 2609.02783 (EarlyEval, agent early outcome prediction), 2608.10315 (cross-contextual consistency), 2404.19318 (calibration on code summarization), 2601.10496 (exposure-aware bug-vs-fix preference), UnCert-CoT (no arXiv id in record).

## UNRELATED

The remaining citers (code translation, accessibility, security tooling, RAG, education, surveys of LLM use in SE, and similar) bear on no candidate's core claim.
