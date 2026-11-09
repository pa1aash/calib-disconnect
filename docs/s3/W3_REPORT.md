# Wave 3 Report: layout, literature-search tooling readiness, prose system, orientation, and positioning brief

Date: 2026-11-10. No stop condition fired. Parts A, B, and C were completed.

## 1. Model identifier (step 0)

The orchestrating session ran as `claude-opus-5-5` (Opus 5.5). It is not a Fable model; the wave
continued as instructed. The prose-lint sub-agent ran on the `sonnet` alias.

Start-state check:

| Check | Result |
|-------|--------|
| Working tree | clean |
| Branch | `main` |
| Local HEAD and origin/main | both `e2ec5e92931a...` |
| Hooks | `.git/hooks/pre-commit` and `.git/hooks/commit-msg` are symlinks to `tools/hooks/` |

## 2. Commits and check results

All commits were authored and committed as Palaash Gang <palaashgang@gmail.com>. Both hooks ran on
every commit. None was rejected, and `--no-verify` was not used.

| SHA | Item | Message |
|-----|------|---------|
| `8805a72` | A1 | Add top-level layout for new work: pipeline, runs, analysis, paper, figures, positioning |
| `151ebd4` | B1 | Add operator prose audit prompt and binding manuscript writing brief |
| `fb86d17` | B2 | Add orientation record and literature-positioning brief |
| `b0140b1` | B1 | Add prose linter for manuscript source with configurable severities and tests |
| `72fa287` | B1 | Record prose lint baseline on the legacy v3 manuscript (pushed; remote HEAD = local HEAD = `72fa28708e96...`) |

This report and the updated `docs/CONTEXT.md` are committed and pushed after these.

Checks:

- **pytest:** `tests/prose_lint`, 171 tests, all passed.
- **gitleaks, full history:** 21 commits scanned, no leaks.
- **gitleaks, staged changes:** no leaks.
- **gitleaks, new directories:** no leaks.
- **Freeze:** no change under any frozen path in `e2ec5e9..HEAD`. A1 confirmed that the freeze
  hook accepts the new top-level directories.
- **Identity:** a single identity on every commit.
- **Attribution:** no attribution string in any commit message or added line (grep).

Item notes:

- **A1.** Created `pipeline/`, `runs/`, `analysis/`, `paper/figures/`, and `research/positioning/`,
  each with a README, plus `paper/README.md`. The layout is recorded in `docs/CONTEXT.md`.
- **A2.** In `scratch/CLAUDE.md.pre-w2`, 24 occurrences of the collaborator's home path were replaced with `<user-home>`. No occurrence remains. The file is local
  only, so there was nothing to commit.
- **B1.** `docs/style/prose-audit-prompt.md` is the operator's prompt with a provenance header. The
  body after the header is byte-identical to the source (SHA-256 `8228131187f7...`, verified after
  the copy).

## 3. Literature-search tooling

**Version mismatch.** The mismatch comes from the published package, not from the installation.

- The tool was installed with pip from the package index.
- Every one of its 89 installed files matches the 0.8.6 release's file record by hash.
- The 0.8.6 wheel itself, downloaded and inspected, carries 0.8.6 metadata and a stale internal
  version string, "0.8.5". The version command prints that string.
- The global entry procedure, the 16 project step procedures, and all 14 agent definitions match
  what the 0.8.6 installer produces.

**Alignment.** A forced reinstall of 0.8.6 with the original installer (pip) left the versions
unchanged: before and after, the command reports v0.8.5 and the metadata 0.8.6. The string can
only change by patching the installed file, which was not done, or by upgrading. The package index
lists 0.13.1 as its latest release.

**Output location.** The tool already writes inside this repository: notes, run artifacts, and
archived runs go under `research/`, and all of it is tracked. Only its configuration and a
rebuildable search index sit in an ignored hidden directory. The output root is configurable, but
its step procedures hard-code `research/`, so changing the root would break them. Instead, a sync
step designed for the positioning run copies every note and artifact of a run into
`research/positioning/<tag>/` with a SHA-256 manifest. The sync must run before any later run
archives those artifacts.

**Headless retrieval.** A probe fetch with the default HTTP provider, into a throwaway vault in a
temporary directory, succeeded and started no browser. An optional headless-browser provider is also
installed, and no login profile is configured. Retrieval can therefore run entirely headless. The
full record is in the local, untracked tooling note.

## 4. Lint baseline headline

The linter (`tools/prose_lint.py`, pure Python, 171 tests) found 158 findings on 54 lines of
`papers/v3/main.tex`: 138 HARD and 20 WARN.

- **Decimals:** 121 of the HARD findings are hand-typed decimals in prose.
- **Other HARD findings (17):**
  - roadmap sentences: 6;
  - "not X but Y" negations: 3;
  - colons in the title and running title: 2;
  - colons in headings: 2;
  - significance announcers: 2;
  - caption over three sentences: 1;
  - em-dash: 1.
- **Review:** all 37 non-decimal findings were read against the source and are true positives.
- **Linter fixes from the baseline:** it exposed three gaps (the venue title macros, "Table N and
  Figure M present" roadmaps, and announcers such as "noteworthy"). All three were fixed before the
  baseline was recorded.
- **Record:** `docs/s3/LINT_BASELINE_v3.md`, with full outputs in `docs/s3/lint/`.

## 5. Strongest idea (from `docs/s3/ORIENTATION.md`)

Its strongest idea is that execution turns the calibration of code models into a measurement
problem with an objective, automatic ground truth. With a test-based label for every problem, and
with the label drawn from a generation that no confidence method saw, the gap between what a
model's behavior reveals and what it says can be measured on thousands of problems instead of
argued from small human-labeled sets.

## 6. Positioning brief summary

`docs/s3/POSITIONING_BRIEF.md` scopes the next wave's literature-positioning run. It does not run
it.

- **Candidates to test, not assume:**
  - L1, an execution-graded measurement foundation with a release-date contamination control;
  - L2, locating the disconnect between hidden-state probes and verbal or sampled readouts;
  - L3, verification utility through confidence-routed execution budgets and post-failure
    confidence updates;
  - L4, per-requirement confidence from the v4 design;
  - F, a measurement-instrument framing.
- **Occupancy questions and leads:** each candidate has its own questions and seed leads. All leads
  are unverified, including those carried from an earlier vault report, which names a close code
  occupant for L2.
- **Search scope:** facets, venues, and the years 2022 to November 2026.
- **Instrument rules:**
  - headless retrieval only;
  - arXiv full-text search, validated on known positives first;
  - Semantic Scholar with backoff;
  - OpenReview;
  - forward citation screens;
  - bibliography entries only from fetched records;
  - a gap is never recorded as a zero.
- **Output contract:** OCCUPIED, NARROW, or CLEAN verdicts with evidence, a ranked recommendation,
  verified BibTeX, a digest, and a manifest, all under `research/positioning/`.
- **Pivot criteria:** if L2 is occupied at the intended breadth, the replacement spine is L1 with
  L3, then L4, with F kept only if it adds analysis beyond the standard Brier decomposition.

## 7. Deviations

1. **Model.** The session was not a Fable model (`claude-opus-5-5`), as recorded in section 1.
2. **Commits for A2 and A3.** A2 and A3 changed only local, untracked files, so Part A produced a
   single commit (A1).
3. **A3 alignment.** The version could not be aligned. A forced reinstall of 0.8.6 was run and
   changed nothing, because the release itself is inconsistent. The installed file was not patched,
   and the newer release was not installed.
4. **A3 output location.** Output was not redirected. A sync step was designed instead, because the
   tool's procedures hard-code their paths. The tool already writes to tracked paths in the
   repository.
5. **Writes outside the project for A3.** The reinstall wrote to the Python environment's package
   directory. The PyPI download and the probe vault were written to the session's temporary
   directory, and the probe fetched one page from jmlr.org. Hosts used: pypi.org,
   files.pythonhosted.org, and jmlr.org.
6. **Prose audit prompt copy.** The copy has a header comment prepended, as the task asked. Its body
   keeps the source's em-dashes, because it is verbatim source text.
7. **Lint sub-agent.** The sub-agent was resumed twice with calibration fixes found while running
   the baseline (title macros; roadmap, announcer, and comma-negation patterns). The baseline was
   recorded after both rounds. Its files are limited to its assigned paths. It deliberately added
   no package marker in `tests/prose_lint/`, so the test directory does not shadow the module.
8. **Extra output.** The baseline's raw JSON and Markdown outputs are tracked under `docs/s3/lint/`,
   in addition to the requested summary file.
9. **Severity assignments.** Softening adverbs, "rather than", clefts other than "What",
   short paragraph endings, negation cascades, and Monte Carlo precision default to WARN in the
   linter, matching their JUDGMENT class in `paper/STYLE.md`. Contradictory pairs are HARD.
10. **Style brief scope.** `paper/STYLE.md` has 25 rules. They cover all sixteen audit categories
    plus the conventions, and figure style is a separate HARD rule. Eighteen rules cite real
    instances from `papers/v3/main.tex`; the rest use constructed examples.
11. **Unverified judgment in the orientation.** `docs/s3/ORIENTATION.md` judges the legacy
    second-model pass rate of zero to point to an extraction or harness fault. This was not
    verified.
12. **Context capsule.** `docs/CONTEXT.md` was updated twice: the layout table in A1, and the
    current stage with this report.

## 8. Items needing operator input

1. **[OPERATOR] Allow the hosts the positioning run needs.** In the next wave prompt, permit
   headless access to arxiv.org, export.arxiv.org, api.semanticscholar.org, openreview.net,
   api.openreview.net, api.openalex.org, and doi.org. Also permit the publisher and proceedings
   hosts listed in `docs/s3/POSITIONING_BRIEF.md` section 3, rule 8.
2. **[OPERATOR] Decide the literature-search tool version.** Either keep 0.8.6, whose only
   inconsistency is its self-reported version string, or authorize an upgrade to 0.13.1 with pip
   before the positioning run. An upgrade replaces the step procedures and agent definitions.
3. **[OPERATOR] Decide v4 scope (carried from wave 2).** Say whether `src/v4_dprc` is in scope. The
   L4 candidate and its pivot role depend on it.
4. **[OPERATOR] Confirm the HARD and JUDGMENT classes in `paper/STYLE.md`.** In particular, confirm
   that softening adverbs stay JUDGMENT (a linter WARN) and are not made HARD.
5. **[OPERATOR] Carried from wave 2, still open:**
   - which definition the new pipeline uses for each DIFFER entry;
   - rotating the former GPU host key;
   - recording the OpenReview submission-form fields while logged in;
   - the wording of the first-page LLM-use footnote (requirement quoted in
     `docs/s3/ORIENTATION.md` section d);
   - whether Fable should be used for any role. This session ran on Opus.
6. **[OPERATOR] Optional: delete `scratch/CLAUDE.md.pre-w2`.** It is now redacted, but it remains a
   local copy of the old agent-instruction file.
