# Wave 1 Report: operator decisions applied, bundle mapped

Date: 2026-11-10. No stop condition fired. Parts A and B were completed.

## 1. Start-state check

| Check | Result |
|-------|--------|
| Working tree | clean (`git status --porcelain` empty) |
| Branch | `main` |
| Local HEAD / origin/main / remote `refs/heads/main` | all `d4bee2eb2d04aca1b8e7594b6143d96f8c6edffe` |
| Hooks | `.git/hooks/pre-commit` and `.git/hooks/commit-msg` are symlinks to `tools/hooks/`, executable; `core.hooksPath` unset |

## 2. Part A: operator decisions

All commits were authored and committed as Palaash Gang <palaashgang@gmail.com>. Both hooks ran on
every commit (they produce no output on success). No commit was rejected, and `--no-verify` was not
used.

| Item | Commit | Change |
|------|--------|--------|
| A1 | `f51b0bd88be6234c8197269dd4a8deacf549d7a2` | Removed the one line in `src/v4_dprc/README.md` that held the local plan-file path. The sentence now reads "Full rationale + gates: the research report at `research/notes/…`". The withhold rule and its comment header were removed from `.gitignore`, and the file is now tracked. The rest of the README is unchanged. |
| A2 | — (no change) | `git check-ignore -v .hyperresearch/config.toml` → `.gitignore:60:.hyperresearch/`. The file is still ignored and untracked. |
| A3 | `2d4608e7c154bbaa021afe458cc4152afad10b0e` | Replaced the home path with `<user-home>` in `research/runs/archive-aaai-bar-eval-dprc-d78e07-20260720T063245Z/scaffold.md` line 15 and `research/runs/archive-code-llm-calibration-aaai27-eabf3f-20260719T195636Z/scaffold.md` line 15. Appended a dated "W1" section (rows 12–13) to `docs/s0/REDACTION_LOG.md`. `/home/ubuntu` paths were not changed. |
| A4 | `297b5e478170c080f87fdadae83d6504215a8ed3` | Added `!papers/v*/main.bbl` after `*.bbl` in `.gitignore` and tracked `papers/v1/main.bbl`, `papers/v2/main.bbl` and `papers/v3/main.bbl`. Checked with `git check-ignore`: other `.bbl` files, including `papers/v1/other.bbl`, stay ignored. |

Gitleaks results for Part A:

- **A1:** `gitleaks dir` found no leaks in `src/v4_dprc/README.md`.
- **A4:** `gitleaks dir` found no leaks in each of the three `main.bbl` files, and a grep for home paths and `@` found 0 hits.
- **All commits:** the pre-commit hook's `gitleaks git --pre-commit --staged` passed on every commit.

After Part A, the branch was pushed (`d4bee2e..297b5e4`), and local HEAD equaled the remote `refs/heads/main` (`297b5e4…`) before Part B started.

## 3. Part B: bundle map

Output: `docs/s1/BUNDLE_MAP.md`.

**Method.** Four parallel read-only analysis passes ran: one each for papers/v1, v2 and v3, and one for the code → results trace across `src/v1_baseline` … `src/v4_dprc`. They were then merged by hand. These numbers were re-checked directly against the JSONs before merging:

- v3 pass@1: 0.823 printed vs 0.884 in the file.
- v3 log-prob Brier: 0.122 vs 0.101.
- v2 Tab. 1 Brier CI: equal to the ECE CI.
- n=20 AUROC CI: [.600, .900] printed vs [.617, .888] in the file.

**Archive contents.** These were checked by byte comparison (`cmp`):

- `archives/dl4cV1.zip` main.tex is identical to papers/v1.
- `archives/dl4cV2.zip` main.tex is identical to **papers/v3**, not papers/v2.

**Headline findings.** None of these is a judgment of the science:

- **Claims traced:** v1 has 34 claims plus 2 figures; v2 has 56; v3 has about 50, counting sub-rows.
- **v1 matches its result files.** Every number in v1 matches; the only problems are method-text vs code differences and the SFT/DPO claims, which have no file behind them.
- **v2 mismatches:**
  - All Brier CIs in Tab. 1.
  - Four SFT CIs in Tab. 5.
  - The n=20 AUROC CI.
  - The final training loss.
  - The Fig. 1 reliability points. Panel (a) still shows v1 data; panels (c) and (d) match no file.
- **v3 mismatches:**
  - pass@1 0.823 appears in no file.
  - Three Brier cells in the main table are carried over from v2.
  - 2.18 s latency and 67% are v2 values.
  - Fig. 1 and the App. C/D bins match neither the v3 nor the v2 files.
  - Tab. 6 mean confidence.
  - Two values are off in the third decimal.
- **Mixed SFT runs in v3.** v3 mixes two SFT evaluation runs: the Tab. 6 and Fig. 4 distributions come from different files.
- **REPRODUCE.md §2 attributions are wrong in seven places.** For example, the `results/v3` files come from `exp_v3_all.py`, not `exp_v3_multimodel.py`, and `results/v1/…_mbpp_fixed.json` was produced by the v2 script `run_all_v2.py`.
- **v4_dprc has produced nothing beyond a stub.** Only a 5-problem StubGenerator dry run exists. `results/v4_dprc` and `data/v4_dprc/adapters` are empty. Seven v4 stages have no output at all, and the analysis modules write only to stdout.
- **No result file is uncited and none lacks a producer.** All 18 result files have an identifiable producer and are cited by at least one manuscript. Many scripts' outputs, all trained adapters and all DPO/trust-study artifacts exist only on the GPU boxes and are missing here.

## 4. Part B commit

The Part B commit holds this report and `docs/s1/BUNDLE_MAP.md`. Its hash is recorded in the operator hand-off, because a file cannot contain its own commit hash. Before committing, `gitleaks dir docs/s1` found no leaks, and grep found no IPs, key filenames or personal home paths in `docs/s1`.

## 5. Deviations

1. **Accidental write outside the project.** During the A4 `.gitignore` check, one command created an empty file `/tmp/x.bbl` (a leftover scratch `touch`). It had no content, was never used, and was deleted immediately in the next command. Nothing else was written outside the project.
2. **A3 scope.** The A3 replacement covered the drive/mount prefix together with the home directory (`C:` + home → `<user-home>`, `/c` + home → `<user-home>`). That way the result reads `<user-home>/…` rather than `C:<user-home>/…`.
3. **Remaining home-path mentions in `docs/s0/W0_REPORT.md`.** That file still contains the home-directory name in four places, at lines 71, 82, 114 and 117. Line 117 contains the full Windows CLI path. A3 was scoped to the run scaffolds, so these were left alone. See operator item 1.
4. **Part B write method.** The analysis passes wrote no files. All intermediate output was kept in session memory. The only files Part B wrote were the two documents in `docs/s1/`.

## 6. Items needing operator decision before the next wave

1. **[OPERATOR] Home path in `docs/s0/W0_REPORT.md`.** The collaborator's home-directory name is still in the W0 report (4 lines, including one full Windows CLI path on line 117). Decide whether to scrub these to `<user-home>`. Note that git history keeps the earlier text either way, and no history rewrite is allowed.
2. **[OPERATOR] Manuscript-vs-results mismatches (`BUNDLE_MAP.md` §3.2).** Decide how the next wave treats them: correct the manuscript text, regenerate the figures and tables from the JSONs, or re-run the experiments. The most significant are:
   - v3 pass@1 0.823 against 0.884 in the results file.
   - The v3 Brier column, which holds v2 values.
   - The v2/v3 Fig. 1 and App. C bins.
   - The SFT CIs.
   - The n=20 row, whose run has pass@1 0.0875.
3. **[OPERATOR] Source of truth for "the paper".** Decide which manuscript the next wave builds on (papers/v3 is the latest), and whether v1 and v2 are frozen history only.
4. **[OPERATOR] `archives/dl4cV2.zip` naming.** The archive holds the v3 manuscript, and no archive contains v2. Decide whether to document this, for example in REPRODUCE.md or the README, or leave it as is.
5. **[OPERATOR] REPRODUCE.md corrections.** §2 contains at least seven wrong script → output attributions (`BUNDLE_MAP.md` §3.6). Decide whether a later wave should correct that document. This wave did not modify it.
6. **[OPERATOR] Missing remote artifacts.** Decide whether the GPU-box outputs can be recovered: DPO pairs and metrics, `exp3_*`, the trust study, the `sft_confidence_data.json` data file, both `qwen_confidence_sft` adapters, `sensitivity_summary.json`, the `exp_v3_multimodel.py` outputs, and the run logs. If they are lost, the NO-FILE claims stay unbacked.
7. **[OPERATOR] v4_dprc status.** v4 has only stub output. Decide whether v4 is in scope for the TMLR target, or whether it should be marked as unrun future work.
8. **[OPERATOR] Text-vs-code method discrepancies.** These cover the correctness-label definition, the prompts, the log-prob transform, the AST-confidence formula, TACE binning, the SFT tier thresholds and the "held-out" SFT subset. Decide whether the code or the text is authoritative.
9. **[OPERATOR] Carried from W0.** These W0 items are still open:
   - item 1: rotate the infrastructure key and host.
   - item 6: keep the pristine backup private.
   - item 7: fix the local agent-instruction file's CLI path. That file is untracked; this wave did not touch it.
