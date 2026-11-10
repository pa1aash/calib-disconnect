# W5 Part A1: search instrument re-validation (draft)

Retrieved 2026-11-10 (UTC times are in each raw header). Headless curl with the desktop user agent, no email in any request, no browser. Every raw response is in `raw/` with a first line giving URL, retrieval date, and HTTP status. Backoff logs for Semantic Scholar are `raw/s2_*.json.log`.

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

## 1. arXiv full text (search.arxiv.org): PASS with a hit cap

### 1.1 Endpoint
- `https://arxiv.org/search_classic` (GET with `searchtype=ft`, and form POST) returns 302 to `https://search.arxiv.org/?query="<q>"&in=`. Without parameters it returns 302 to `arxiv.org/find/...` (raw/sc_redirect_headers.txt). So search_classic is a redirector; the instrument is search.arxiv.org.
- Template: `https://search.arxiv.org/?in=&query=%22<phrase>%22` and `&startat=<10k>` for pages. `in=cs` restricts to CS (Kuhn phrase: 59 hits with `in=cs`, 62 with `in=`).

### 1.2 Recall on body-only positives
Each phrase was confirmed in the vault full-text note (whitespace-normalized, lower case) and confirmed absent from the abstract returned by `export.arxiv.org/api/query?id_list=...` (raw/ax_abs_batch.xml). Queries are quoted.

| Paper | Body-only phrase | search.arxiv.org result | Raw |
|---|---|---|---|
| 2207.05221 (W4) | "train models with a value head" | 1 of 1, target (snippet is the body sentence) | sax_valuehead_q.html |
| 2302.09664 (W4) | "semantic equivalence relation" | 62 hits, target at rank 22 (page 3) | sax_kuhn__22semantic_equivalence_relation_22_.html, sax_ser_p10..p60.html |
| 2611.07876 | "trained only on candidates the model judges correctly" | 1 of 1, target | sax_pos1_2611.07876.html |
| 2609.34857 | "most confident value already covers half the pool" | 1 of 1, target | sax_pos2_2609.34857.html |
| 2609.36783 | "ten random directions of matched norm" | 1 of 1, target | sax_pos3_2609.36783.html |
| 2605.09023 | "random seed of the fuzz-input generator" | 1 of 1, target | sax_pos4_2605.09023.html |
| 2607.05188 | "shuffled labels collapse to 0.50" | 1 of 1, target | sax_pos5_2607.05188.html |
| 2606.14530 | "extracted from a prompt-only forward pass" | 1 of 1, target | sax_pos6_2606.14530.html |
| control 1 | "zxqv blorptangle wumbleflange" | "No Results." | sax_pos7_ctrl1.html |
| control 2 | "quorbic flentasm drivulate monotrophe" | "No Results." | sax_pos8_ctrl2.html |

Recall: 8 of 8 positives, 0 of 2 controls. 2512.07404 was not used: its vault note holds only the abstract page.

### 1.3 Why the orchestrator saw 0 ids for 2302.09664
Index coverage and quoting are ruled out: the paper is indexed and the quoted phrase returns it. Phrase length is ruled out: a 3-word phrase works. Further evidence:
- Quoted, the target is at rank 22 of 62, so it is not on page 1 (ids on page 1: 2610.33267, 2605.23942, and 8 others).
- Unquoted, it is at rank 61 of 322 (raw/sax_ser_unq_p*.html).
- The longer quoted phrase "placeholder semantic equivalence relation" gives 3 hits including the target. Adding the word Kuhn gives 18 hits, with the target at rank 4.
- In this session, macOS `sed` and `grep` failed on these pages with "illegal byte sequence" under the default locale. A pipeline that hides that error yields 0 ids. Using `LC_ALL=C` or Python avoids it.

The 0 is therefore consistent with reading page 1 only, or with that parsing failure. I cannot tell which from here.

### 1.4 Behavior
- **Exact phrase versus bag of words.** Quoted strings are exact-phrase matches (value-head phrase: 1 hit). Unquoted strings are ranked bag-of-words with stemming: the same words give 405 hits, with "heads" highlighted.
- **Hit cap (important).** Reported totals plateau at about 200 to 450, whatever the true frequency: "large language models" 382, "language model" 338, calibration 339, "semantic entropy" 208, "expected calibration error" 224, `byDate=1` exactly 200. Truncation is confirmed with a known positive. 2605.09023 uses "semantic entropy" 11 times in its body. Yet it is absent from all 208 ids for quoted "semantic entropy", read across 21 pages (raw/sax_se_p*.html), while 2302.09664 is present at rank 48. Narrowing to `"semantic entropy" "fuzz-input"` returns 2605.09023 (1 of 1, raw/sax_se_narrow.html). A broad query's total is therefore a truncated relevance list, not a complete match set.
- **Pagination.** 10 hits per page via `startat`, and results run to the reported total (`startat=400` gives hits 401 to 405). `startat` beyond the total gives HTTP 500. Page-size parameters (`max`, `numResults`, `hits`) are ignored.
- **Query length.** The form's `maxlength=64` is client-side only. A 94-character quoted GET query worked (1 of 1, 2607.05188, raw/sax_len92.html).
- **Freshness.** Sorted by date, the newest indexed ids are 2611.09892 and 2611.09894. 2611.09894 was submitted 2026-11-06T18:59:57Z, and 2611.11000 (submitted 2026-11-07) is not found. The export API's newest cs.LG id is 2611.12884, submitted 2026-11-09. The index therefore lags about 3 to 4 days (raw/sax_fresh_bydate*.html, raw/ax_fresh_dates.xml, raw/ax_latest.xml).
- **Rate limiting.** About 110 requests were spaced 1 to 3 s apart, and none was throttled.

## 2. OpenReview api2: search PARTIAL, PDFs FAIL

- **Search works.** `https://api2.openreview.net/notes/search?term=<q>` returns 200. Parameters `content=title`, `source=forum`, `group=<venue>`, `limit`, and `offset` all work: `limit=1000&offset=1000` returned 1000 notes. The `count` field is capped at 10000. Without `source=forum`, results are mostly reviews and comments.
- **Known positive.** 2505.13553 ("Towards Functional Correctness of Code Models with Selective Generation"; arXiv title confirmed in the vault note) is found as ICLR 2026 Rejected_Submission 0pRvnSBNGx ("Ensuring Functional Correctness of Large Code Models with Selective Generation"), as ICML 2026 1CQZbl24wp, and as a NeurIPS 2025 DL4C workshop paper. Raw: or2_title1.json and or2_quoted_abs.json. Quoted "selective generation" returns 48 hits. The ICSE 2025 dblp mirror record of 2402.02047 (uS1g2crF3k) is also returned. Group search works for ICLR 2025 (count 4004) and TMLR (count 1429). The index is fresh: ICLR 2027 submissions appear.
- **Coverage limits.**
  - api2 search is metadata and abstract only. Quoted "semantic equivalence relation" in group ICLR.cc/2023/Conference returns 0.
  - ICLR 2023 is absent from api2: "semantic uncertainty" in that group returns 0, and a title search does not return Kuhn VD-AYtP0dve.
  - api v1 does return VD-AYtP0dve (raw/or1_kuhn_title_retry.json, 200 after a 429 "limit of 5 requests" backoff), but v1 body-phrase search returns 0.
  - The control returns count 0.
- **Full text: FAIL.** Every endpoint gave 403 with `ChallengeRequiredError` JSON or a challenge HTML page:
  - api2 `/notes?id=`
  - api2 `/pdf?id=`
  - api2 `/attachment?id=&name=pdf`
  - api2 `/pdf/<hash>.pdf`, the hashed path from the note's `pdf` field
  - openreview.net `/pdf?id=`, `/attachment`, and `/pdf/<hash>.pdf`

  openreview.net `/forum?id=` gave 307 to `/challenge`. Raw: or2_pdf_*.bin and or2_pdfhash_*.bin.

## 3. Semantic Scholar

| Endpoint | Attempt 1 (from 10:58Z) | Attempt 2 (from 11:03Z, about 5 min later) |
|---|---|---|
| `paper/search?query=code+generation+calibration` | 429 at waits 0, 2, 4, 8, 16, and 32 s | 429 at waits 0, 2, and 4 s, then 200 at the 8 s wait: total 189278, 10 results |
| `paper/search/bulk?query="code generation" +calibration` | 200, total 132 | 200, total 132 (identical) |
| `snippet/search?query=train models with a value head` | 429 on all 6 waits | 429 on all 6 waits |
| `snippet/search?query=semantic equivalence relation` | not run | 429 on all 6 waits |

- **Bulk recall.**
  - `+calibration +correctness +code` returns total 1484, with 1000 rows per page and a continuation token. 2402.02047 is among the rows.
  - `+"distribution shift" +"code correctness"` returns 1 of 1, 2611.07876.
  - The control returns 0.

  Bulk matches title and abstract, so it is not a full-text instrument.
- **Snippet endpoint.** It answered 429, never 404, so the route appears to exist, but it was never usable.
- **Citations.**
  - arXiv:2402.02047 has citationCount 100. offset 0 returns 100 rows; offset 100 and offset 200 return 0, which is consistent with exactly 100 citers.
  - Deeper paging was tested on arXiv:2207.05221. offset 100 returns 100 rows (next 200), offset 1000 returns 100 rows (next 1100), and offset 2300 returns 24 rows (next none).
  - offset 9950 returns 400: "offset + limit must be < 10000".
  - The final lookup was throttled (429).

## 4. OpenAlex

- **Budget.** The daily budget has reset: all calls returned 200. `works?search=calibration code language models` gives count 200793, and the top 3 results are on code calibration.
- **`fulltext.search`.** Quoted phrases, `per-page=50`:
  - Hits: 2207.05221 (2 hits), 2611.07876, 2609.34857, 2607.05188, and 2606.14530 (1 each).
  - Misses: 2302.09664 (113 hits, absent from all 3 pages), 2609.36783 (0), and 2605.09023 (0).
  - Controls: 0 and 0.

  All three misses have `has_fulltext: true` in OpenAlex (raw/oa_lookup_*.json). Shorter variants still miss: "random directions of matched norm" gives 3 hits without the target, and "fuzz-input generator" gives 7 without the target. Recall is 5 of 8.

## 5. DataCite and OSF

- **DataCite.** `api.datacite.org/dois/10.17605/osf.io/qpk9a` returns 200 ("Signal Detection Theory for LLM Calibration", OSF Registries 2026, url https://osf.io/qpk9a/). `.../10.31234/osf.io/8jq4f_v1` returns 404. That DOI is Crossref-registered: `api.crossref.org/works/10.31234/osf.io/8jq4f_v1` returns 200, "A trade-off between reasoning ability and metacognitive sensitivity in large language models", posted-content, Center for Open Science. DataCite keyword search also works (total 2255) and indexes arXiv DOIs.
- **OSF.**
  - Pages `osf.io/<id>/` and `osf.io/preprints/psyarxiv/8jq4f_v1` return 200, but as a 4309-byte JavaScript shell with no abstract or text.
  - `osf.io/<id>/download` redirects 301, then 308, then 302 to `files.osf.io/v1/resources/...`, a host not on the allowlist, so the redirect was not followed.
  - For qpk9a (a registration), the download returns 500.
  - No full text was reachable headlessly on allowed hosts (raw/osf_headers.txt).

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
| G-AX | arXiv full text unreachable | **CLOSED** | 8 of 8 body-only positives and 0 of 2 controls; hit-cap rule applies |
| G-OR | OpenReview listing and PDFs blocked | **PARTIAL** | api2 keyword search works with venue filters; every PDF or attachment path is still 403 |
