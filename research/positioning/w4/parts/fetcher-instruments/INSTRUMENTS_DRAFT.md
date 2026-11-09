# W4 Step 2 instrument validation (draft)

Retrieved 2026-11-09 UTC (local date 2026-11-10). Desktop user agent, headless curl. No email in any request. Raw responses in raw/.

## 1. arXiv full-text search: FAIL

The advanced-search form (https://arxiv.org/search/advanced, raw/form.html, 200) lists terms-0-field options: title, author, abstract, comments, journal_ref, acm_class, msc_class, report_num, paper_id, cross_list_category, doi, orcid, author_id, all. There is NO full-text option. searchtype on the form is "all" only.

| URL | Status | Hits | Result |
|---|---|---|---|
| https://arxiv.org/search/?query=%22semantic+likelihoods%22&searchtype=ft | 200 | no results page (blank search form, 0 result nodes, cookie arxiv-search-parameters={}) | FAIL, silently ignored |
| .../search/?query=%22semantic+equivalence+relation%22&searchtype=ft | 200 | 0 result nodes | FAIL |
| .../search/?query=%22zxqv+blorptangle+wumbleflange%22&searchtype=ft (negative control) | 200 | 0 result nodes | uninformative (same blank page as positives) |
| .../search/?query=%22semantic+likelihoods%22&searchtype=full_text | 301 | redirect to http://search.arxiv.org/?in=&query=... (legacy host, not on allowlist, not followed) | FAIL |
| .../search/?query=...&searchtype=fulltext | 200 | 0 result nodes | FAIL |
| advanced?...terms-0-field=full_text / fulltext / ft | 200 | "Whoops! Something went wrong. Please correct errors in the form" | FAIL (invalid field) |

Verdict: arXiv full-text search is not available on allowed hosts. Every negative search downstream that relies on full text is an instrument gap. Only title/abstract/all-metadata search works (searchtype=all, and export API all:).

Positives chosen (full text via https://arxiv.org/pdf/<id>, pdftotext; abstracts via export.arxiv.org/api/query?id_list=<id>, 200):
- 2207.05221: phrase "train models with a value head" (body, Section 1 contributions bullet, "Finetuning to Identify the Questions Models Can Correctly Answer": "We train models with a value head to predict the probability that they can answer a question correctly, which we refer to as P(IK)."). Absent from abstract (0 matches for "value head").
- 2302.09664: phrase "semantic equivalence relation" (body, Section 3.1; "Let us introduce a placeholder semantic equivalence relation, E(., .), which holds of any two sentences that mean the same thing"; 3 body matches). Absent from abstract (0 matches).

Phrase test results (the all: field is metadata only):

| Phrase | Full-text (searchtype=ft) | export API all:"phrase" | arxiv.org searchtype=all |
|---|---|---|---|
| train models with a value head (2207.05221) | not functional (blank) | 200, totalResults 0 | 200, 0 results |
| semantic equivalence relation (2302.09664) | not functional (blank) | 200, totalResults 5, target 2302.09664 NOT among them (unrelated papers) | 200, 5 results |
| zxqv blorptangle wumbleflange (negative) | not functional (blank) | 200, 0 | 200, 0 |

Correct behavior for all: (metadata only) confirmed; correct behavior for full text not achievable. Working substitute: arXiv search_classic searchtype=all and export API all:/ti:/abs: for metadata; fetch PDFs (https://arxiv.org/pdf/<id>) and grep locally for body claims.

Working templates (metadata only):
- https://arxiv.org/search/?query=%22PHRASE+WORDS%22&searchtype=all
- https://export.arxiv.org/api/query?search_query=all:%22phrase+words%22&max_results=N
- https://export.arxiv.org/api/query?id_list=<id>

## 2. Semantic Scholar Graph API: PARTIAL (search gap)

| Call | Attempts (status) | Final | Result |
|---|---|---|---|
| paper/search?query=code+generation+calibration&fields=title,year,externalIds,citationCount&limit=5 | wait 0:429, 4:429, 8:429, 16:429, 32:429, 40:429 (22:42:23 to 22:44:08Z) | 429 | GAP recorded, not retried |
| paper/arXiv:2207.05221?fields=title,year,citationCount | 0:200 | 200 | "Language Models (Mostly) Know What They Know", 2022, citationCount 2324 |
| paper/arXiv:2207.05221/citations?fields=title,year&limit=5 | 0:200 | 200 | 5 citing papers returned (offset 0, next 5) |

Base: https://api.semanticscholar.org/graph/v1/ . Unauthenticated; search endpoint is rate-limited harder. Logs: raw/ss_*.log.

## 3. OpenReview: PARTIAL

Host note: I called api2.openreview.net once (first, before trying api.openreview.net; ordering deviated from the instructions) and will not call it again. It returned 200. api2.openreview.net is not on the allowlist: host question for the orchestrator.

| URL | Status | Hits | Result |
|---|---|---|---|
| https://api2.openreview.net/notes/search?term=calibration%20code&limit=5 | 200 | count 10000 (capped) | works; includes 2025-26 venues |
| https://api.openreview.net/notes/search?term=calibration%20code&limit=5 | 200 | count 10000 (capped) | works (allowed host); returns 5 notes incl. "Calibration and Correctness of Language Models for Code" (id VDZkSSpa_b, dblp record) |
| https://api.openreview.net/notes/search?term=calibration+language+model&group=ICLR.cc/2025/Conference&limit=5 | 200 | 0 | group filter yielded nothing; ICLR 2025 not found in v1 index |
| https://api.openreview.net/notes?content.venueid=ICLR.cc/2025/Conference&limit=1 | 403 | n/a | ChallengeRequiredError (browser challenge) |
| https://api.openreview.net/notes?forum=0qSOodKmJaN&limit=3 | 403 | n/a | challenge |
| https://openreview.net/notes/search?term=... | 400 | n/a | "New Version Available" message |
| https://openreview.net/forum?id=0qSOodKmJaN | 200 | n/a | "Verifying your browser" challenge page (4789 B), not paper content: FAIL |
| https://openreview.net/pdf?id=0qSOodKmJaN | 403 | n/a | challenge HTML, no PDF: FAIL |

No ICLR 2025 paper located via v1 (the forum/pdf test used ICLR 2023 paper 0qSOodKmJaN, found via v1 search). Working: v1 notes/search (allowed host). Not working: venueid listing, forum pages, PDFs (challenge). Template: https://api.openreview.net/notes/search?term=<url-encoded>&limit=N

## 4. Other bibliographic services

| URL | Status | Hits | Result |
|---|---|---|---|
| https://api.openalex.org/works?search=calibration+code+language+models&per-page=3 | 200 | count 200793 (full-text-in-scope search) | PASS; top: "Calibration and Correctness of Language Models for Code", "Calibration of Large Language Models on Code Summarization", "An Empirical Study of Security Calibration in Large Language Models for Code". Notice: no API key shares a $0.10 daily budget per IP |
| https://api.crossref.org/works?query=calibration+code+language+models&rows=3 | 200 | total-results 2799462 | PASS (noisy relevance) |
| https://dblp.org/search/publ/api?q=calibration+code+language+models&format=json&h=3 | 202 (twice, 8 s apart) | n/a | FAIL: bot challenge ("Making sure you're not a bot!") |

OpenAlex note: its search is "title, abstract, or full text" (fulltext.search in x_query), a possible substitute for arXiv full-text but with OpenAlex's own coverage; not validated against the positives here.

## Summary

| Instrument | Verdict |
|---|---|
| arXiv full-text (search_classic ft) | FAIL (no ft option; ft ignored; full_text redirects off-allowlist) |
| arXiv metadata (all:, searchtype=all) | PASS |
| Semantic Scholar paper + citations | PASS; search 429 gap |
| OpenReview v1 search (api.openreview.net) | PASS; venue/forum/pdf FAIL (challenge); api2 needs host approval |
| OpenAlex | PASS |
| Crossref | PASS |
| DBLP | FAIL (challenge 202) |
