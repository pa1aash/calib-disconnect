# Raw source provenance (diff-A6)

Retrieval date for every network fetch: 2026-11-10. Client: headless curl, desktop user agent. Per-file `.meta` records sit beside each file.

| File | URL | HTTP status | Notes |
|---|---|---|---|
| 2512.07404.html / .txt | https://arxiv.org/html/2512.07404 | 200 | Ribeiro et al.; .txt is a local tag-stripped extraction |
| 2611.07876.html / .txt / .body.txt | https://arxiv.org/html/2611.07876 | 200 | Campos et al.; .body.txt is Abstract through References |
| 2609.34857.html / .txt / .body.txt | https://arxiv.org/html/2609.34857 | 200 | CREDO; appendices read in .txt (lines 1304 onward) |
| 2402.02047.html / .txt / .body.txt | https://arxiv.org/html/2402.02047 | 200 | Spiess et al. |
| 2604.23333.html / .txt / .body.txt | https://arxiv.org/html/2604.23333 | 200 | RLCM; .body.txt includes appendices A to F |
| neurosym_arxiv_search.xml | https://export.arxiv.org/api/query?search_query=ti:NeuroSym-Cal&max_results=10 | 200 | zero entries returned |
| neurosym_arxiv_search2.xml | https://export.arxiv.org/api/query?search_query=all:"reasoning-execution gap" AND all:calibration&max_results=10 | 200 | zero entries returned |

## NeuroSym-Cal (Findings of ACL 2026, pp. 6132-6143, doi 10.18653/v1/2026.findings-acl.305)

- No arXiv version was found (two export.arxiv.org queries above, zero entries).
- The vault note `research/notes/neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc.md` is ABSTRACT-ONLY (its own summary says so).
- Full text was read from the local extraction made in wave 4: `research/positioning/w4/parts/dossier-D4/raw/neurosym.txt` (from `neurosym.pdf` in the same folder). No new request to ACL Anthology was made in this pass. Page numbers cited in CELLS.md are the printed Findings page numbers in that text.
