# bench-A2: benchmark pins and gap resolution (wave 7)

Retrieved 2026-11-10 with headless curl (huggingface.co, github.com release assets) and `gh api` (api.github.com). File hashes are in `MANIFEST.json`; the pin table is `BENCHMARK_PINS_DRAFT.md`. Downloaded data sit in `cache/` (untracked). Small derived outputs (no problem text, no tests) are in `derived/`; metadata pages are in `raw/`. All analysis scripts are in `scripts/` and were run with `python3 -I`; none executes code from the data (LiveCodeBench private tests are unpickled with a loader that refuses every global).

Derived-output hashes (SHA-256): `derived/lcb_summary.json` 459537bc1db7..., `derived/evalplus_inspect.json` 1d9ae5897262..., `derived/mbpp_humaneval_inspect.json` 8af458b5afd8..., `derived/heplus_extra.txt` 9dac2b702ab7....

## 1. MBPP+ task IDs removed between v0.1.0 (399) and v0.2.0 (378)

Source: set difference of `task_id` in the two release assets `MbppPlus.jsonl.gz` (v0.1.0 sha256 `57d639e7...`, v0.2.0 sha256 `af43697e...`), script `scripts/evalplus_inspect.py`, output `derived/evalplus_inspect.json`.

Removed (21): Mbpp/83, 115, 117, 143, 164, 229, 249, 295, 396, 400, 407, 431, 438, 442, 461, 574, 582, 595, 640, 746, 783. Added: none.

Cross-check: `tools/mbpp/fix_v010.py` in evalplus (saved as `raw/gh_evalplus_tools_mbpp_fix_v010.py`, git blob `f1aedfc9...`) deletes exactly these 21 IDs. The same script edits 18 prompts (Mbpp/734, 735, 736, 739, 740, 743, 745, 749, 751, 752, 753, 757, 763, 771, 780, 781, 782, 803) to strip source URLs; the asset diff confirms only the `prompt` field changed for those 18 tasks. B4's "prompts are never edited" holds for wording, but v0.2.0 prompts differ from v0.1.0 by URL removal.

All 378 v0.2.0 IDs lie in MBPP-sanitized, drawn from all four sanitized splits: prompt 7, test 224, train 108, validation 39 (v0.1.0: 7, 239, 111, 42). This answers B4's "all sanitized splits or only test" question. 28 sanitized IDs were never in MBPP+ (listed in `derived/mbpp_humaneval_inspect.json`).

## 2. June 2024 ground-truth fixes (Mbpp/459, 102, 559) and version recommendation

- The fixes are evalplus commit `4a4e0bff69c4052759b91aae2a5e7008a16e6427` (2024-06-10, "fix(mbpp): reference solutions 102/459/559 (#211)"). It adds only a patch script, `tools/mbpp/fix_v011.py`, renamed `fix_v020.py` in `ce8f729e0a` (2024-10-20). Its `SOURCE_VERSION = "v0.2.0"` and `TARGET_VERSION = "v0.2.1"` (`raw/gh_evalplus_tools_mbpp_fix_v020.py`, git blob `b35a229a...`).
- No v0.2.1 exists. `evalplus/mbppplus_release` has only tags v0.1.0 and v0.2.0, with assets uploaded 2024-04-17 and never updated (`raw/gh_mbppplus_release_releases.json`). Its last commit is 2024-04-17. HF `evalplus/mbppplus` main is `b2d74c9` (2024-04-17). `MBPP_PLUS_VERSION = "v0.2.0"` in evalplus v0.3.1 and in master `26d6d00` (2025-10-02).
- The v0.2.0 asset does NOT contain the fixes. At the indices the patch checks (55, 215, 236), the canonical solutions are the old ones. Mbpp/459 uses `c.islower()` rather than `not c.isupper()`. Mbpp/102 uses `x.capitalize() or '_'`. Mbpp/559 initializes `max_so_far = 0`. The same old code is in the OriginFmt `code` field, and so in the HF mirror, which is built from OriginFmt.
- Related June 2024 evaluator fixes are special oracles for Mbpp/581 and Mbpp/558 (commit `f86db47`, 2024-06-18). They live in evalplus code, not in the data, and are present at tool tag v0.3.1.
- **Recommendation.** Pin MBPP+ v0.2.0 native `MbppPlus.jsonl.gz` and apply `fix_v020.py` (from evalplus `26d6d00`) in the pipeline. Record the patched file's hash; it is not computed here because it depends on the pipeline's serialization. Regenerate expected outputs from the patched canonical solutions. Evaluate with evalplus v0.3.1 semantics (special oracles). Pin HumanEval+ v0.1.10 native `HumanEvalPlus.jsonl.gz`, the newest release. HumanEval+ has no later ground-truth fix.

### HumanEval+ v0.1.10 contents

Source: `HumanEvalPlus.jsonl.gz` at v0.1.10, sha256 `272720b9...`. 164 tasks (HumanEval/0 to /163). Fields: task_id, prompt, entry_point, canonical_solution, contract, base_input, plus_input, atol. All 164 have a non-empty contract and 3 have nonzero `atol`.

| Variant | base_input total (mean, median, min, max) | plus_input total (mean, median, min, max) |
|---|---|---|
| HumanEvalPlus | 1,570 (9.57, 7, 1, 105) | 122,683 (748.07, 972, 2, 1000) |
| HumanEvalPlus-NoExtreme | 1,570 (same) | 122,504 (746.98, 972, 1, 1000) |
| HumanEvalPlus-Mini | 1,570 (same) | 1,107 (6.75, 6, 1, 19) |

- **Changes from v0.1.9.** Four tasks differ. `plus_input` was cut for HumanEval/1 (1000 to 83) and HumanEval/28 (1000 to 861). The `contract` changed for HumanEval/99 (now `value = float(value)`) and HumanEval/160. This resolves B4 gap 3.
- **Mini and NoExtreme.** Their plus inputs are subsets of the full plus inputs, and their base inputs equal the full base inputs (`derived/heplus_extra.txt`). This resolves B4 gap 8 on data.
- **Overlap and duplicates.** In HumanEval+ v0.1.10, 218 plus inputs equal a base input and 6 are within-task duplicates. In MBPP+ v0.2.0 the figures are 134 and 244. One MBPP+ task (Mbpp/793) has zero plus inputs. All of this matters for the hash-partition and dedup steps in R1 section 4.
- **MBPP+ v0.2.0 (native).** base_input total 1,174 (mean 3.11, min 3, max 7). plus_input total 39,841 (mean 105.4, median 105, min 0, max 147). 13 tasks have nonzero `atol`.
- **OriginFmt files** (HumanEval+ and MBPP+) have no base_input or plus_input fields, only a `test` string. Native files are the only source that separates base from plus (B4 gap 4).

## 3. LiveCodeBench: newest release

- **Official sources checked.**
  - HF dataset `livecodebench/code_generation_lite`: refs have no tags, only `main` = `0fe84c3912ea0c4d4a78037083943e8f0c4dd505` (2025-06-05, "fix typos") (`raw/hf_lcb_refs.json`, `raw/hfapi_lcb.json`).
  - The HF tree has shards `test.jsonl` to `test6.jsonl` (`raw/hf_lcb_tree_main.json`).
  - The loader at that commit (`raw/hf_lcb_loader_0fe84c3.py`) defines release_v1 to release_v6 and release_latest (= all six shards), plus slice tags v1 to v6 and vI_vJ.
  - Other livecodebench HF datasets were last modified 2024 (`raw/hf_lcb_author_datasets.json`).
  - GitHub `LiveCodeBench/LiveCodeBench`: 0 releases, 0 tags, last commit `28fef95` 2025-07-16. Its README lists release_v1 to v6 (`raw/gh_lcb_README.md`). The other branch, `feat--new-autograder`, was last committed 2025-01-13 and lists only up to v4. A GitHub code search for `release_v7` returned 0 hits.
- **Newest release: `release_v6` (= `release_latest`).** Its six shards were streamed. Each shard's SHA-256 and size matched the HF LFS oid and size.

| Release | Shard added | Shard problems | Release total | Day-level contest_date range of release | Range of the added shard |
|---|---|---|---|---|---|
| release_v1 | test.jsonl | 400 | 400 | 2023-05-07 to 2024-03-02 | 2023-05-07 to 2024-03-02 |
| release_v2 | test2.jsonl | 111 | 511 | 2023-05-07 to 2024-05-25 | 2024-03-09 to 2024-05-25 |
| release_v3 | test3.jsonl | 101 | 612 | 2023-05-07 to 2024-08-10 | 2024-06-01 to 2024-08-10 |
| release_v4 | test4.jsonl | 101 | 713 | 2023-05-07 to 2024-10-05 | 2023-08-26 to 2024-10-05 |
| release_v5 | test5.jsonl | 167 | 880 | 2023-05-07 to 2025-01-04 | 2024-09-22 to 2025-01-04 |
| release_v6 | test6.jsonl | 175 | 1055 | 2023-05-07 to 2025-04-06 | 2025-01-04 to 2025-04-06 |

- Totals match the README counts. All 1,055 question_ids are unique. This resolves B4 gap 1 on day-level bounds.
- **Shard date ranges overlap.**
  - test4 contains 12 problems dated at or before v3's last day: 7 from abc366 (2024-08-10), 4 from arc181 (2024-08-04), and 1 from weekly-contest-360 (2023-08-26).
  - test5 has 10 problems on or before 2024-10-05.
  - test5 and test6 both contain problems dated 2025-01-04 (7 and 4).
  - Slice tags (v4, v5, ...) are therefore not clean date windows. Date filters must use `contest_date`.
- **Fields** (all 1,055): question_title, question_content, platform, question_id, contest_id, contest_date, starter_code, difficulty, public_test_cases, private_test_cases, metadata. There is **no language field**. Problems are either stdin (610) or functional (444, all LeetCode, each with starter_code and `metadata.func_name`). One problem (abc350_c) has an empty public test list. Python eligibility therefore cannot be read from a field. That every problem is solvable in Python is the LCB design assumption, not a checked field.
- **Platforms**: AtCoder 602, LeetCode 444, Codeforces 9 (all 9 in v1). **Difficulty**: easy 322, medium 383, hard 350.
- **contest_date times.** AtCoder dates are midnight. 161 LeetCode dates (from test4 on) carry times 06:30, 07:30, 18:30, or 19:30. The timezone is unstated, so a LeetCode problem's day can be off by one relative to UTC. Day-level comparisons below use the stored day.
- **Private tests.** All 1,055 problems have non-empty private tests, all in the base64-zlib-pickle encoding, with 0 decode errors. Per-problem counts are min 1, median 20, max 100, 25,492 in total, and 18 problems have fewer than 5 private tests. This resolves B4 gap 1 on private tests. With the R1 20 percent hash split, problems with 1 to 4 private tests yield 0 or 1 agreement inputs.
- **Licence.**
  - HF card front matter: `license: cc`, no variant (`raw/hf_lcb_README_0fe84c3.md`).
  - HF loader: `license="MIT License"`.
  - GitHub LICENSE: MIT, "Copyright (c) 2024 LiveCodeBench" (`raw/gh_lcb_LICENSE.txt`).
  - No page states terms for the contest-site problem text. Gap unchanged.

## 4. Post-cutoff counts (release_v6, day(contest_date) strictly after the date)

Script: `scripts/post_cutoff.py DATE [--end END] [--release TAG] [--index-dir DIR] [--json]`. It defaults to release_v6 and the index in `cache/lcb_index`; `derived/lcb_index` is a tracked copy. Outputs are in `derived/post_cutoff_*.json`.

| Cutoff | Model use | Post-cutoff | First, last day | By month |
|---|---|---|---|---|
| 2023-12-31 | OLMo 2 | 729 | 2024-01-06, 2025-04-06 | 2024-01 36, 02 32, 03 45, 04 37, 05 36, 06 46, 07 43, 08 66, 09 47, 10 53, 11 57, 12 49, 2025-01 51, 02 51, 03 68, 04 12 |
| 2024-02-29 | Qwen2.5-Coder code data | 661 | 2024-03-02, 2025-04-06 | from 2024-03 as above |
| 2024-06-30 | gpt-oss | 497 | 2024-07-06, 2025-04-06 | from 2024-07 as above |
| 2024-09-16 | Qwen2.5-Coder 7B bound | 365 | 2024-09-21, 2025-04-06 | 2024-09 24, then from 2024-10 as above |
| 2024-11-08 | Qwen2.5-Coder 32B bound | 278 | 2024-11-09, 2025-04-06 | 2024-11 47, then from 2024-12 as above |
| 2024-12-31 | Olmo 3 | 182 | 2025-01-04, 2025-04-06 | 2025-01 51, 02 51, 03 68, 04 12 |
| 2025-04-27 | Qwen3 bound | 0 | none | none |
| 2025-07-31 | Qwen3-Coder | 0 | none | none |

- **Platform split** of post-cutoff problems (AtCoder, LeetCode): 436, 293 / 397, 264 / 310, 187 / 229, 136 / 170, 108 / 112, 70.
- **Boundary sensitivity.** Most cutoffs have no problem within one day. The exceptions are 2023-12-31 (3 problems on 12-30, counted pre-cutoff), 2024-06-30 (5 problems on 06-30, pre-cutoff), and 2024-11-08 (12 problems on 11-09, counted post-cutoff, 5 of them LeetCode with 06:30 or 18:30 times). If the timezone shifted those 11-09 times back, at most 5 would move.
- **Campos window** (2024-10-01 to 2025-05-31 inclusive): 341 problems. By month: 2024-10 53, 11 57, 12 49, 2025-01 51, 02 51, 03 68, 04 12. The window extends past the last v6 day (2025-04-06).

## 5. Pins

See `BENCHMARK_PINS_DRAFT.md` and `MANIFEST.json`: 34 entries, each with URL, revision (HF commit, or release tag plus tag commit, or GitHub commit plus git blob), bytes, and SHA-256.

- The HumanEval+ tag `v0.1.10` points at commit `68cd26d`, whose message is "feat(v0.1.9)". The v0.1.10 bump commit `200defc` came after the tag target. The release assets themselves differ from v0.1.9, so pin by asset hash, not by commit.
- All HF parquet hashes match their LFS oids. The GitHub MBPP files match their git blob SHAs.

## 6. Other B4 gaps

- **MBPP-sanitized count is 427**, not 426: `sanitized-mbpp.json` at `f82046b` has 427 unique task IDs (2 to 809), and the HF sanitized splits have 7 + 257 + 120 + 43 = 427 identical IDs. The paper's "426" is a text claim with no file to match. The full MBPP file has 974 rows.
- HumanEval HF parquet: 164 rows, HumanEval/0 to /163, 5 columns.

## Remaining gaps

- The LCB contest_date timezone for LeetCode times is not documented.
- The licence of LCB problem text (contest-site terms) is not stated.
- No LCB problem is dated after 2025-04-06, so the Qwen3 and Qwen3-Coder post-cutoff strata are empty on every official release.
- The hash of the patched MBPP+ file is left to the pipeline.
- Evalplus master changes after v0.3.1 (44 commits) were not reviewed.
- Third-party commit feeds (with co-author trailers) were kept only in `cache/`.
