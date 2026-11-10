# NEW_CLOSE: CLOSE citers not in the vault (fcs-A3)

Retrieval date 2026-11-10. Vault check: `grep -rilF` on arXiv id and distinctive title words over `research/notes`, `research/positioning/w4/dossiers`, and `research/positioning/w4/VERDICTS.md`; zero hits for the entry below.

## Absent from the vault

| arXiv id | Title | Year | Cites seed | Candidate and component | Text basis | Verdict effect |
|---|---|---|---|---|---|---|
| 2611.07913 | Same Answer, Different Future: Matched Predictions Do Not Imply Matched Belief Updating in Language Models | 2026 (v1 2026-11-05, concurrent) | 2607.12985 | L3 Q2 and Q7 (update after evidence) | FULL TEXT, `dossiers/2611.07913.md` | None. Synthetic Bernoulli inference on three 8-12B instruct models; no code, no correctness labels, no failing tests. L3 "update after a shown failing test" stays CLEAN (provisional). Design note: evidence format and elicitation query moved measured update weights by orders of magnitude, so the add-on should fix the query and report a query-variation check. |

## Other seeds

- 2603.18893, 2610.18066, 2504.03359: no new CLOSE citer. The one W4 CLOSE citer of 2504.03359 (TRACE 2605.03838) now has a dedicated vault note.
- 2402.02047 (Spiess et al.): 0 new citers after dedupe (122 of 122 already in the W4 fcs-G2 set), so no new CLOSE citer. Every Spiess citer that bears on the highlight criteria (for example 2512.07404, 2611.07876, 2608.08266) is already in the vault.

## Highlight criteria

No new CLOSE citer runs probes against verbal or trained stated confidence on execution-labeled code, uses within-problem scoring, swaps the oracle, or splits calibration at a pre- or post-cutoff release date. None measures stated-confidence change after a shown failing test on code.
