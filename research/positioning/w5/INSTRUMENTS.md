# Instrument re-validation (wave 5, A1)

Run date 2026-11-10. This wave allowed new hosts: search.arxiv.org, api2.openreview.net, api.datacite.org, and osf.io. No Semantic Scholar or OpenAlex API key was available: there is no local `.env`, and no key is set in the environment. The full sub-agent record, including recall tables and backoff logs, is `parts/fetcher-instruments/INSTRUMENTS_DRAFT.md`. Its 167 raw responses are in `parts/fetcher-instruments/raw/`.

## Orchestrator notes

- **The orchestrator's early probe.** It returned 0 ids for the 2302.09664 phrase. A1 shows the paper is indexed (hit 22 of 62, page 3). So that 0 came from reading page 1 only or from a parsing failure; it is not an index miss.
- **How the Part A body-text queries (A4a, A4b) used search.arxiv.org.**
  - They used quoted phrases and read every page up to 100 results per query.
  - A few queries had totals over the cap rule below; for example, A4a A5-02 had 254 hits and 100 read.
  - Zeros from those queries are not used as evidence of absence.
  - Every cell that stays without an occupant is therefore still labeled CLEAN (provisional), not CLEAN. G-FT and G-S2 are only PARTIAL.
- **Host deviation.** One sub-agent request went to raw.githubusercontent.com, which is not on the allowlist (A2, recorded in `parts/dossier-A2/`). Its content was discarded and not used.

## Summary

| Instrument | Verdict | Consequence for negative (absence) claims |
|---|---|---|
| arXiv full text, search.arxiv.org (also reached through arxiv.org/search_classic, which 302-redirects there) | **PASS**, with a hit cap | Usable for absence claims only with a quoted exact phrase whose reported total is well under the cap (about 200 to 450; see 1.4), with every result page read |
| OpenReview api2 `notes/search` | **PARTIAL** | Metadata and abstract keyword search of v2 venues (2024 to 2027, TMLR, DBLP mirror records); a zero does not cover body text or v1-era venues (ICLR 2023 and earlier, where api v1 still answers) |
| OpenReview PDFs and attachments (api2 and openreview.net) | **FAIL** (403 challenge) | No OpenReview-only full text; body claims need an arXiv copy |
| Semantic Scholar `paper/search` (relevance) | **PARTIAL** (429 on attempt 1, 200 on attempt 2 after 8 s) | Intermittent; a zero counts only when a 200 is in hand |
| Semantic Scholar `paper/search/bulk` | **PASS** (200 on both attempts, known positives recalled) | Usable for title and abstract absence claims, boolean syntax |
| Semantic Scholar `snippet/search` | **FAIL** (429 on all 18 tries, 3 queries, 2 sessions) | Gap; not usable |
| Semantic Scholar lookup and `/citations` with offset | **PASS** (offset 100 and 1000 work; offset + limit must be < 10000) | Full forward-citation screens possible for papers with fewer than 10000 citers |
| OpenAlex works `search` | **PASS** (daily budget has reset; 200) | Title and abstract recall |
| OpenAlex `fulltext.search` filter | **PARTIAL** (5 of 8 body-only positives) | Positive hits are leads; zeros are not evidence |
| api.datacite.org DOI lookup | **PASS** for DataCite DOIs (OSF 10.17605) | PsyArXiv 10.31234 DOIs are Crossref DOIs (DataCite 404, Crossref 200) |
| osf.io full text or file download | **FAIL** | Download redirects to files.osf.io (not allowed); pages are JavaScript shells |

## 6. Use for negative claims in this wave, and gap status

Negative (absence) claims may rest on:
- **search.arxiv.org**, for body text of arXiv papers indexed up to about 2026-11-06. This requires a quoted exact phrase, a reported total well under the cap (rule of thumb: under 150), every page read, and a second phrasing.
- **Semantic Scholar bulk search, OpenAlex works search, and arXiv metadata**, for title and abstract absence.
- **OpenReview api2 search**, for metadata absence in v2 venues, plus api v1 for venues from 2023 and earlier.
- **Semantic Scholar `/citations`**, for forward-citation completeness, when the citer count is under 10000.

These may not support negatives: OpenAlex `fulltext.search` (5 of 8), Semantic Scholar snippet search (never answered), OpenReview body text and PDFs, and OSF full text.

| Gap | W4 meaning | Status now | Reason |
|---|---|---|---|
| G-FT | No body-text search | **PARTIAL** | Closed for arXiv-hosted papers via search.arxiv.org, within the cap and the 3 to 4 day lag. Open for OpenReview-only and OSF-only full texts |
| G-OA | OpenAlex full text partial, budget exhausted | **PARTIAL** | Budget reset (200); full-text recall is still 5 of 8 |
| G-S2 | Semantic Scholar keyword search 429 | **PARTIAL** | Bulk search works (2 of 2 sessions); relevance search is intermittent; snippet search is unavailable |
| G-AX | arXiv export API returned HTTP 429 intermittently (W4); A1 recorded it here as arXiv full-text reachability | **CLOSED** | No Part A agent reported an HTTP 429 from the export API. Full text through search.arxiv.org recalls 8 of 8 body-only positives and 0 of 2 controls, with the hit-cap rule applied. |
| G-OR | OpenReview listing and PDFs blocked | **PARTIAL** | api2 keyword search works with venue filters; every PDF or attachment path is still 403 |
