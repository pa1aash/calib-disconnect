# Instrument validation (wave 4, step 2)

Run 2026-11-10 (IST; 2026-11-09 UTC). Headless curl with a desktop user agent, and no email in any
request. Raw responses are in `parts/fetcher-instruments/raw/`, with the orchestrator's follow-up
checks in `raw/orch/`. The full sub-agent record is `parts/fetcher-instruments/INSTRUMENTS_DRAFT.md`.

## Summary

| Instrument | Verdict | Consequence for verdicts |
|---|---|---|
| arXiv full-text search (search_classic, `searchtype=ft`) | **FAIL** | Every negative that would need body-text search is an instrument gap |
| arXiv metadata search (`searchtype=all`, export API `all:`, `ti:`, `abs:`) | PASS (metadata only, confirmed) | Usable for title and abstract recall only |
| OpenAlex full-text filter (`fulltext.search`) | **PARTIAL** (1 of 2 known positives) | Positive hits count; negatives are gaps |
| OpenAlex title and abstract search | PASS | Primary search instrument |
| Semantic Scholar paper lookup and citations | PASS | Forward and backward citation screens work |
| Semantic Scholar search | **FAIL** (HTTP 429 on 10 attempts, two sessions, full backoff) | Gap: Semantic Scholar keyword recall is missing |
| OpenReview v1 `notes/search` (api.openreview.net) | PASS | Keyword search of OpenReview records |
| OpenReview venue listing, forum pages, PDFs | FAIL (403 browser challenge) | OpenReview-only full texts are unreachable; most also exist on arXiv |
| Crossref | PASS | Bibliographic records |
| DBLP | FAIL (HTTP 202 proof-of-work page) | Bibliographic cross-check unavailable |
| Full-text reading by PDF fetch (`arxiv.org/pdf/<id>` plus local text extraction) | PASS | Verdicts rest on fetched full texts read locally |

## 1. arXiv full-text search: FAIL

- **No full-text field.** The advanced-search form (https://arxiv.org/search/advanced, HTTP 200)
  offers these fields: title, author, abstract, comments, journal_ref, acm_class, msc_class,
  report_num, paper_id, cross_list_category, doi, orcid, author_id, and all. None of them is a
  full-text field.
- **`searchtype=ft` is silently ignored.** `https://arxiv.org/search/?query=<q>&searchtype=ft` returns
  HTTP 200 with a blank form and no results. The same blank page comes back for positives and for the
  nonsense control.
- **`searchtype=full_text` leaves the allowlist.** It redirects (HTTP 301) to search.arxiv.org, a host
  not on this wave's list, so the redirect was not followed. The other spellings either return no
  results or fail form validation.

Known positives were checked in full text and then in the abstract:

| Paper | Body-only phrase | Location in full text | In abstract? | arXiv `all:` result |
|---|---|---|---|---|
| 2207.05221 (Kadavath et al.) | "train models with a value head" | Section 1, contributions | no | 0 hits |
| 2302.09664 (Kuhn et al.) | "semantic equivalence relation" | Section 3.1 | no | 5 hits, target absent |

The `all:` field therefore behaves as metadata-only search, as the brief expected. Real full-text
search could not be reached on an allowed host.

## 2. OpenAlex full-text filter: PARTIAL

The orchestrator ran `https://api.openalex.org/works?filter=fulltext.search:"<phrase>"&per-page=50`,
reading every page.

| Phrase | Total hits | Target returned? |
|---|---|---|
| "train models with a value head" | 2 | yes (2207.05221) |
| "semantic equivalence relation" | 113 | **no**, although OpenAlex lists 2302.09664 with `has_fulltext: True` |
| "zxqv blorptangle wumbleflange" (control) | 0 | n/a |

OpenAlex full text found one of the two positives. Its positive hits are usable leads. A zero from it
is not evidence of absence.

## 3. Semantic Scholar: search is a gap

| Call | Attempts | Result |
|---|---|---|
| `graph/v1/paper/search?query=code+generation+calibration` | Sub-agent: 6 attempts, waits 0, 4, 8, 16, 32, and 40 s. Orchestrator: 4 attempts, waits 0, 4, 8, and 16 s. | HTTP 429 every time: **gap** |
| `graph/v1/paper/arXiv:2207.05221` | 1 | HTTP 200 |
| `graph/v1/paper/arXiv:2207.05221/citations` | 1 | HTTP 200, paginated |

Unauthenticated keyword search is throttled harder than lookups. Downstream agents use Semantic
Scholar only for lookups and citation screens, with backoff.

## 4. OpenReview

| URL | Status | Result |
|---|---|---|
| `https://api.openreview.net/notes/search?term=calibration%20code&limit=5` | 200 | Works; returns records such as "Calibration and Correctness of Language Models for Code" |
| `https://api.openreview.net/notes?content.venueid=ICLR.cc/2025/Conference` | 403 | Browser challenge |
| `https://openreview.net/forum?id=...` and `/pdf?id=...` | 200 challenge page, 403 | Challenge page instead of content |
| `https://api2.openreview.net/notes/search?...` | 200 | Called once by the sub-agent before it tried the allowed hosts. This host is not on the wave's allowlist (deviation recorded in the W4 report) and was not used again. |

## 5. Search protocol adopted for the run

1. **Recall.** Keyword recall uses OpenAlex search (title and abstract, plus partial full text),
   arXiv metadata search, OpenReview v1 search, and Crossref.
2. **Citation screens.** Forward and backward screens use Semantic Scholar citations and references,
   with OpenAlex `cites:` as a second source.
3. **Verdicts on body text.** These rest on the fetched PDF, read locally with section citations.
4. **Recording negatives.** A negative that would need body-text search is recorded as an instrument
   gap. So is a negative from Semantic Scholar keyword search. No CLEAN verdict rests on such a
   negative.
