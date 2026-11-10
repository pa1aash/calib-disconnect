# B4: Benchmark fact sheet for the pre-registered design

Wave 6 Part B, task B4. Retrieval date for every fact below: 2026-11-10 (headless curl). No data files were downloaded; only cards, metadata APIs, GitHub pages, release feeds, source files rendered on github.com, and arXiv abstracts and PDFs (PDF text excerpts saved). Saved pages are in `raw/` (file named in the Source column). "HF API" means `https://huggingface.co/api/datasets/<id>`.

## 1. HumanEval (openai/openai_humaneval)

| Fact | Value | Source (raw file) |
|---|---|---|
| Problem count | 164 (single `test` split, 164 examples) | HF API and card, `raw/hfapi_openai_openai_humaneval.json`, `raw/hfreadme_openai_openai_humaneval.md` |
| Fields | task_id, prompt, canonical_solution, test, entry_point | same |
| License | MIT (HF card `license: mit`; GitHub LICENSE "The MIT License, Copyright (c) OpenAI") | HF card; https://github.com/openai/human-eval/blob/master/LICENSE, `raw/gh_humaneval_LICENSE.html` |
| Release date | arXiv 2107.03374 v1 submitted 2021-07-07 (v2 2021-07-14); first GitHub commit ("squash commits") 2021-07-08; license file added 2021-07-14. HF `createdAt` 2022-03-02 is a Hub migration date, not the release date | https://export.arxiv.org/abs/2107.03374, `raw/arxiv_abs_2107.03374.html`; https://github.com/openai/human-eval/commits/master.atom, `raw/gh_humaneval_commits.atom` |
| Tests per problem | "an average of 7.7 tests per problem" (Chen et al. 2021, Sec. 2.2). EvalPlus counts differently: HumanEval avg 9.6, median 7.0, min 1, max 1052 (four tasks cross-check over random inputs; without them max/avg 26/7.3) | `raw/arxiv_pdf_excerpt_2107.03374.txt`; `raw/arxiv_pdf_excerpt_2305.01210.txt` (Table 2 and footnote 2) |
| Maintenance status | Repo README now says "Deprecated and unmaintained" (commit 2026-10-16). Data unchanged | https://github.com/openai/human-eval/blob/master/README.md, `raw/gh_humaneval_README.txt` |

## 2. HumanEval+ and MBPP+ (EvalPlus)

Dataset releases live in separate repos (`evalplus/humanevalplus_release`, `evalplus/mbppplus_release`); the `evalplus/evalplus` tags (v0.1.3 to v0.3.1) are tool releases, not dataset versions.

### 2a. Versions and counts

| Dataset | Version (latest first) | Release date (GitHub) | Tasks | Variants published | Source |
|---|---|---|---|---|---|
| HumanEval+ | v0.1.10 (current; `HUMANEVAL_PLUS_VERSION = "v0.1.10"` in evalplus master) | 2024-05-01 | 164 (HF card and HF tag v0.1.10) | HumanEvalPlus, -Mini, -NoExtreme, -OriginFmt (.jsonl.gz) | https://github.com/evalplus/humanevalplus_release/releases.atom, `raw/gh_humanevalplus_release.atom`; `raw/gh_heplus_assets_v0.1.10.html`; `raw/gh_evalplus_evalplus_data_humaneval.py.txt`; `raw/hfapi_evalplus_humanevalplus.json`, `raw/hf_refs_evalplus_humanevalplus.json` |
| HumanEval+ | v0.1.9 | 2024-02-02 | not stated on release page (gap) | same four variants | `raw/gh_heplus_assets_v0.1.9.html` |
| HumanEval+ | v0.1.0 to v0.1.8 | shipped inside evalplus tool releases 2023 | 164 per paper | Mini first released with tool v0.1.5 (2023-06-02) | `raw/gh_evalplus_releases.atom`, `raw/gh_evalplus_README.txt` |
| MBPP+ | v0.2.0 (current; `MBPP_PLUS_VERSION = "v0.2.0"`) | 2024-04-17 | 378 | MbppPlus, -NoExtreme, -OriginFmt (no Mini) | https://github.com/evalplus/mbppplus_release/releases.atom, `raw/gh_mbppplus_release.atom`; `raw/gh_mbppplus_assets_v0.2.0.html`; `raw/gh_evalplus_evalplus_data_mbpp.py.txt` |
| MBPP+ | v0.1.0 | 2024-04-17 (tagged retroactively; dataset first shipped with tool v0.2.0, 2023-11-28) | 399 | same three | `raw/gh_mbppplus_release.atom`, `raw/gh_evalplus_releases.atom` |

HF mirrors: `evalplus/humanevalplus` has tag v0.1.10 (= main, sha d32357c, lastModified 2024-05-01, 164 rows). `evalplus/mbppplus` has tags v0.2.0 (9a36f31) and v0.1.0 (f057175); main (b2d74c9, 378 rows) is one commit after tag v0.2.0 ("Remove test.jsonl and use parquet", 2024-04-17). Both HF copies are the **OriginFmt** file (`hf_upload.py` reads `*-OriginFmt.jsonl.gz`). Source: `raw/hf_refs_evalplus_*.json`, `raw/hf_commits_evalplus_*.json`, `raw/gh_*_release_hf_upload.py.txt`.

Test counts (paper, v3 2023-10-30, Table 2): HumanEval+ avg 764.1 tests/task (median 982.5, min 12, max 1,100); HumanEval+-Mini avg 16.1 (median 13.0, min 5, max 110), "47x" smaller. The Table 4 caption and v0.1.5 release note give 774.8 (and Mini 16.5), an internal inconsistency in the sources. MBPP+: "on avg from 3.1 to 108.5" tests (tool v0.2.0 release note, which describes 399-task v0.1.0); README says "35x". 83 of 164 HumanEval+ tasks have hand-written contracts. Sources: `raw/arxiv_pdf_excerpt_2305.01210.txt`, `raw/gh_evalplus_releases.atom`.

### 2b. Storage of base_input and plus_input

- Native EvalPlus format (`HumanEvalPlus.jsonl.gz`, `MbppPlus.jsonl.gz`): each task has `task_id`, `prompt`, `contract`, `canonical_solution`, `base_input` ("test inputs from original HumanEval"), `plus_input` ("test inputs brought by EvalPlus"), `atol` (and `entry_point`). `completeness_check` asserts these keys. Inputs are JSON lists of argument lists; MBPP+ needs per-task deserialization (`mbpp_deserialize_inputs`, about 60 task IDs need tuple, set, or complex restoration). Source: `raw/gh_evalplus_evalplus_data_humaneval.py.txt`, `raw/gh_evalplus_evalplus_data_mbpp.py.txt`, `raw/gh_evalplus_evalplus_data_utils.py.txt`.
- **No expected outputs are stored in the native format.** `evaluate.get_groundtruth` computes them by running `prompt + canonical_solution` on `base_input` and on `plus_input` (separately, with timing) and caches a pickle keyed by dataset hash. Source: `raw/gh_evalplus_evalplus_evaluate.py.txt` lines 42 to 76.
- OriginFmt and HF copies: the `test` string defines `check(candidate)` with literal `inputs = [...]` and `results = [...]` lists plus an `assertion(out, exp, atol)` helper, so precomputed expected outputs are present there. Whether base and plus inputs are distinguishable inside that single list was not verified (gap). Source: HF viewer pages `raw/hfpage_evalplus_humanevalplus.html`, `raw/hfpage_evalplus_mbppplus.html`.
- Mini and NoExtreme are selected by URL suffix (`-Mini`, `-NoExtreme`); `mini` and `noextreme` are mutually exclusive; MBPP+ asserts "Mini version of MBPP+ is not available yet." Source: `raw/gh_evalplus_evalplus_data_utils.py.txt`, `raw/gh_evalplus_evalplus_data_mbpp.py.txt`.

### 2c. Removed or fixed problems (as documented)

| Change | Where |
|---|---|
| MBPP+ v0.1.0 to v0.2.0: 399 to 378 tasks, removing tasks whose `test_list` (from original MBPP) is wrong; prompts are never edited, so ill-posed prompts are removed instead of fixed; oracle improved; "~4pp pass@1 improvement" expected. Commit 3de2268. The 21 removed task IDs are not listed on the pages fetched (gap) | `raw/gh_evalplus_issue159.html`, `raw/gh_evalplus_commit_3de2268.html`, `raw/gh_evalplus_README.txt` |
| MBPP+ ground-truth fixes, tasks 459, 102, 559 (README news dated 2024-06-09, "pre v0.3.0"); no new MBPP+ release tag after v0.2.0, so which file carries these fixes is unclear (gap) | `raw/gh_evalplus_README.txt` |
| HumanEval+ tool v0.2.1: oracle fix HumanEval/32 | `raw/gh_evalplus_releases.atom` |
| Tool v0.2.0: HumanEval contract and input fixes 0/3/9/148/114/1/2/99/28/32/35/160 | `raw/gh_evalplus_README.txt` |
| Tool v0.1.7: contract fixes 116, 126, 6; extreme inputs removed for 32 | `raw/gh_evalplus_releases.atom` |
| Tool v0.1.6: contract fixes 129, 148, 75, 53, 0, 3, 9; ground-truth fix 140 | `raw/gh_evalplus_releases.atom` |
| Paper: over 10% of original HumanEval ground truths were wrong; all re-implemented for HumanEval+ | `raw/arxiv_pdf_excerpt_2305.01210.txt` |
| HumanEval+ v0.1.9 to v0.1.10 changes: release note says only "HumanEval+ v0.1.10" (gap) | `raw/gh_humanevalplus_release.atom` |

License: Apache-2.0 (evalplus repo LICENSE, both release repos' LICENSE, both HF cards). Source: `raw/gh_evalplus_LICENSE.txt`, `raw/gh_*_release_home.html`, `raw/hfapi_evalplus_*.json`. Note that the underlying prompts derive from HumanEval (MIT) and MBPP (CC-BY-4.0).

## 3. MBPP (google-research-datasets/mbpp)

| Fact | Value | Source |
|---|---|---|
| Original ("full") | 974 problems; HF splits train 374, test 500, validation 90, prompt 10 (task IDs: 11 to 510 test, 1 to 10 prompt, 511 to 600 validation, 601 to 974 train). Each has 3 tests (`test_list`) plus `challenge_test_list` | `raw/hfapi_google-research-datasets_mbpp.json`; https://github.com/google-research/google-research/blob/master/mbpp/README.md, `raw/gh_mbpp_README.txt`; `raw/arxiv_pdf_excerpt_2108.07732.txt` |
| Sanitized | HF splits train 120, test 257, validation 43, prompt 7 (total 427). Paper text says "426 hand-verified questions"; EvalPlus v0.2.0 note says "~427". 426 vs 427 discrepancy unresolved (gap) | same |
| EvalPlus MBPP+ base | Built from MBPP-sanitized (`get_mbpp()` docstring "Get sanitized MBPP"; downloads `sanitized-mbpp.json`; v0.2.0 note "MBPP+ improves MBPP based on its sanitized version"). Which sanitized splits feed MBPP+ (all 427 or only test) is not stated (gap) | `raw/gh_evalplus_evalplus_data_mbpp.py.txt`, `raw/gh_evalplus_releases.atom` |
| Release date | arXiv 2108.07732 v1 2021-08-16 | `raw/arxiv_abs_2108.07732.html` |
| License | CC-BY-4.0 (HF card) | `raw/hfapi_google-research-datasets_mbpp.json` |

## 4. LiveCodeBench code_generation_lite

| Release tag | Contest window (month granularity) | Problems | Data file added | HF commit date |
|---|---|---|---|---|
| release_v1 | May 2023 to Mar 2024 | 400 | test.jsonl | 2024-04-16 |
| release_v2 | May 2023 to May 2024 | 511 | + test2.jsonl | 2024-06-02 |
| release_v3 | May 2023 to Jul 2024 | 612 | + test3.jsonl | 2024-08-12 |
| release_v4 | May 2023 to Sep 2024 | 713 | + test4.jsonl | 2024-10-06 |
| release_v5 | May 2023 to Jan 2025 | 880 | + test5.jsonl | 2025-01-14 |
| release_v6 (= release_latest) | May 2023 to Apr 2025 | 1055 | + test6.jsonl | 2025-04-21 |

Sources: GitHub README "Dataset Versions" (https://github.com/LiveCodeBench/LiveCodeBench/blob/main/README.md, `raw/gh_lcb_README.txt`) for v1 to v6; HF card lists only v1 to v5 (`raw/hfreadme_livecodebench_code_generation_lite.md`); HF loader `code_generation_lite.py` defines release_v1 to release_v6 and release_latest (= all six files), plus slice tags `v1` to `v6` and `vI_vJ` (`raw/hf_lcb_loader.py`); HF commit log `raw/hf_lcb_commits.json`. As of 2026-11-10 no release after v6: last HF commit 2025-06-05 ("fix typos"), last GitHub commit 2025-07-16, no GitHub releases or HF tags (`raw/gh_lcb_commits.atom`, `raw/gh_lcb_releases.atom`, `raw/hf_refs_livecodebench_code_generation_lite.json`, `raw/hf_lcb_author_datasets.json`). Per-file sizes 0.13 to 1.25 GB (`raw/hf_lcb_tree.json`), so not downloaded.

Per-problem fields (loader features, all strings): question_title, question_content, platform (leetcode, codeforces, atcoder), question_id, contest_id, contest_date (ISO datetime), starter_code, difficulty (easy, medium, hard), public_test_cases (JSON list of {input, output, testtype}), private_test_cases (JSON, or base64 of zlib of pickle of JSON), metadata (JSON; `func_name` for functional tests). testtype is `stdin` or `functional`. LCB's evaluator grades on public + private tests concatenated (`get_evaluation_sample`). Source: `raw/hf_lcb_loader.py`, `raw/gh_lcb_lcb_runner_benchmarks_code_generation.py.txt`.

Test provenance (paper v2): about 17 tests per problem on average (full, not lite); AtCoder provides public and hidden tests used directly; LeetCode hidden tests are not available, so tests come from GPT-4-Turbo-built input generators plus some collected failing tests; CodeForces tests from semi-automatically built generators. The lite version "has pruned and sampled tests". Source: `raw/arxiv_pdf_excerpt_2403.07974.txt`, HF card.

Known issues: ERRATA lists multiple-accepted-output problems (e.g., abc311_c, abc326_d, find-the-peaks), interactive problems (abc337_e, abc355_e), and erroneous tests (abc350_c, apply-operations-to-make-string-empty, most-frequent-ids, arc189_a); its own counts ("7", "2", "1") do not match its lists. Source: `raw/gh_lcb_ERRATA.md.txt`.

License: inconsistent. HF card `license: cc` (no variant); HF loader `license="MIT License"`; GitHub repo LICENSE is MIT (code). Problem statements are scraped from LeetCode, AtCoder, and Codeforces, whose terms are not addressed in the fetched pages (gap).

## 5. BigCodeBench (secondary candidate)

| Fact | Full | Hard | Source |
|---|---|---|---|
| Tasks | 1,140 | 148 | `raw/hfapi_bigcode_bigcodebench*.json`; README news 2024-07-18 |
| HF dataset versions (splits) | v0.1.0_hf, v0.1.1, v0.1.2, v0.1.3, v0.1.4 (each 1,140) | same five (each 148) | same |
| Dates | HF created 2024-06-05; announced 2024-06-18 (arXiv 2406.15877 v1 2024-06-22); last data upload 2025-02-23 | announced 2024-07-18; HF created 2024-09-14; last upload 2025-02-23 | `raw/hf_commits_bigcode_*.json`, `raw/gh_bcb_README.txt`, `raw/arxiv_abs_2406.15877.html` |
| Avg tests | 5.6 per task, 99% avg branch coverage (card) | not stated | `raw/hfreadme_bigcode_bigcodebench.md` |
| License | Apache-2.0 (card and repo) | Hard card has no license field (gap) | `raw/hfapi_bigcode_bigcodebench.json`, `raw/gh_bcb_LICENSE.html` |

Tool (pip) releases are separate: v0.2.5 on 2025-04-11 is the latest GitHub release (`raw/gh_bcb_releases.atom`). The per-split change log for v0.1.1 to v0.1.4 is not on the card (card changelog lists only v0.1.0) (gap).

## 6. Problem-level release dates for HumanEval and MBPP

Neither dataset has a per-problem date field (HF features listed above). Only dataset-level dates exist: HumanEval 2021-07-07 (arXiv v1) and 2021-07-08 (GitHub); MBPP 2021-08-16 (arXiv v1). HumanEval+ and MBPP+ add tests, contracts, and fixed solutions later (2023 to 2024) but reuse the original prompts unchanged (issue 159 policy), so problem text dates are the 2021 dates; the augmented tests themselves were public from 2023-05-02 (EvalPlus arXiv v1) and 2023-11-28 (MBPP+). All of these predate every model cutoff the study is likely to use, so for contamination stratification these benchmarks fall entirely in the "released before cutoff" stratum; only LCB `contest_date` supports a within-benchmark split.

## 7. Options for held-out agreement inputs disjoint from the label suite

1. **Hash-partition `plus_input`** (HumanEval+, MBPP+). Assign each input to label or agreement by a fixed hash of (task_id, canonical JSON of the input), e.g. sha256 mod m. Pros: no new tooling, inputs already contract-valid. Cons: the "EvalPlus-augmented" label suite becomes a subset of the published plus suite, so labels are no longer the standard HumanEval+/MBPP+ verdict; tasks with few plus inputs (min 12 per paper, HumanEval+) give small agreement sets; must deduplicate inputs before hashing.
2. **HumanEval+ Mini as label, remainder as agreement.** Mini is a reduced subset of HumanEval+ tests (set-cover reduction), so `plus_input` minus Mini inputs is disjoint by construction (subset relation inferred from the paper's definition; not verified on data). Not available for MBPP+ (no Mini). Changes the label suite to Mini.
3. **Freshly generated inputs**, keeping the full plus suite as label. `evalplus/inputgen.py` generates inputs per task with `ChatGPTGen` (needs an OpenAI-compatible LLM) seeded by `base_input`, then `TypedMutGen` type-aware mutation; contracts (`contract` field) filter invalid inputs. Generated inputs must then be de-duplicated against base and plus inputs. Agreement needs no expected outputs, so no oracle run is required. Source: `raw/gh_evalplus_evalplus_inputgen.py.txt`; tools/ directory also has `filter_inputs.py` and `tsr/` (test-suite reduction), not read.
4. **LiveCodeBench.** Label on private tests, agreement on public tests (or hash-split private tests). Caveat: public tests are typically the examples shown in the prompt, so agreement on them is not held out from the model's view; whether every problem has non-empty private tests in lite could not be checked without downloading data (gap). For stdin problems agreement compares stdout strings; functional problems use `metadata.func_name`.
5. **Expected outputs.** Native EvalPlus files store inputs only; expected outputs come from running the canonical solution (needed only for labels). OriginFmt and HF copies embed precomputed `results`. LCB tests store input and output pairs.

## Gaps

1. LCB: exact day-level contest_date boundaries per release; whether all problems in lite have non-empty `private_test_cases`; per-release platform and difficulty counts for lite; license of scraped problem text (card "cc" vs loader "MIT").
2. MBPP+: list of the 21 task IDs removed in v0.2.0; whether the 2024-06-09 fixes (459, 102, 559) are in the v0.2.0 release asset; whether MBPP+ draws from all sanitized splits or only test.
3. HumanEval+: what changed in v0.1.10 vs v0.1.9; per-version task counts for v0.1.9 and earlier (164 assumed from paper, not confirmed per release).
4. Whether OriginFmt `inputs` lists separate base from plus inputs.
5. MBPP sanitized count: 426 (paper) vs 427 (HF splits).
6. Test-count averages for current versions (paper figures predate fixes; 764.1 vs 774.8 inconsistency).
7. BigCodeBench: changes between v0.1.0_hf and v0.1.4; Hard license field.
8. The Mini-subset-of-plus relation (option 2) is inferred from the paper, not checked on data.
