# Wave 2 Report: W1 decisions applied, legacy frozen, method inventory, TMLR venue pack

Date: 2026-11-10. No stop condition fired. Parts A, B, and C were completed.

## 0. Start-state check

| Check | Result |
|-------|--------|
| Working tree | clean (`git status --porcelain` empty) |
| Branch | `main` |
| Local HEAD / origin/main / remote `refs/heads/main` | all `69deaf50d60df288666fbbdfa80518b2831f8ed1` |
| Hooks | `.git/hooks/pre-commit` and `.git/hooks/commit-msg` are symlinks to `tools/hooks/` |

## 1. Commits and check results

All commits were authored and committed as Palaash Gang <palaashgang@gmail.com>. Both hooks ran on
every commit. No commit was rejected, and `--no-verify` was not used. No commit message contains an
attribution string or trailer (checked with grep over `69deaf5..HEAD`).

| SHA | Item | Message |
|-----|------|---------|
| `8978128` | A1 | Replace collaborator home path in wave 0 report with placeholder |
| `4849360` | A2 | Document archive contents: dl4cV2.zip holds the v3 manuscript |
| `eb4fd35` | A3 | Add legacy banner to REPRODUCE.md pointing to corrected attributions |
| `368555a` | A4 | Freeze legacy bundle: add docs/LEGACY.md and pre-commit freeze check (pushed; remote HEAD = local HEAD = `368555a9cd5e...`) |
| `876f659` | B2 merge | Add official TMLR style files, venue sources and TMLR rubric |
| `943b0d7` | B1 merge | Add method inventory of legacy manuscripts and code, with prompt texts |
| `e015c5f` | B4 | Add project context capsule for future sessions (pushed; remote HEAD = local HEAD = `e015c5f90f2a...`) |

This report is committed and pushed after these.

Item notes:

- **A1.** The home-directory path (with the `C:` prefix on line 117) was replaced with `<user-home>`
  on `docs/s0/W0_REPORT.md` lines 71, 82, 114, and 117. No other tracked file outside `src/`,
  `papers/`, `results/`, and `data/` contained it. Three research notes contain the same given name
  inside published author names (reference lists); these are not paths and were left alone.
  Redaction log rows 14 to 17 are under a new "W2" heading. **Remaining occurrences inside `src/`,
  `papers/`, `results/`, or `data/`: none.** Git history keeps the earlier text.
- **A2.** `archives/README.md` records SHA-256 for all three zips. It states that `dl4cV2.zip` holds
  the v3 bundle and that no archive holds v2. Evidence: every member of each zip was byte-compared
  with `papers/v1`, `papers/v2`, and `papers/v3`. In `dl4cV2.zip`, `main.tex`, `references.bib`, and
  `main.bbl` are identical to `papers/v3` only, and the five style files are identical in all three
  versions.
- **A3.** The banner points to `docs/s1/BUNDLE_MAP.md` section 3.6. The body is unchanged
  (diff: 5 added lines at the top).
- **A4.** `docs/LEGACY.md` records the freeze, the retained section 3.2 mismatches, the fact that no
  legacy manuscript is the new paper's base, and that the missing GPU-host artifacts are unbacked.
  Hook check 5 in `tools/hooks/pre-commit` rejects any staged change under `papers/v1-3/`,
  `src/v1_baseline/`, `src/v2_comprehensive/`, `src/v3_multimodel/`, `src/v4_dprc/`, `results/`,
  `data/`, `archives/*.zip`, and `REPRODUCE.md`. It has no override switch.
- **A4 hook test** (scratch branch `w2-hooktest-scratch`, never pushed, deleted afterwards):
  - Rejected: a staged modification of `papers/v1/main.tex`.
  - Rejected: a staged deletion of `archives/dl4cV1.zip`.
  - Passed: a commit adding a new file at the repository root.
  - The frozen files were verified unchanged afterwards. `install.sh` was rerun before the commit.

Secret scans:

- `gitleaks git` over full history: 15 commits scanned, no leaks.
- `gitleaks dir --max-archive-depth 3` over the whole working folder: about 11.75 MB, no leaks.
- `gitleaks dir` over each merged folder before its commit: no leaks.
- The pre-commit gitleaks staged scan passed on every commit.

Orchestrator spot-check of the method inventory: 10 entries were checked against code and manuscript
lines, and all 10 match.

1. v1 label uses `sample_ok[0]` (`exp1_optimized.py:134`).
2. Same in `run_all_v2.py:171`.
3. MBPP runs the raw program plus tests (`run_all_v2.py:54-58`).
4. exp(mean log p) at `exp_v2_comprehensive.py:191`.
5. exp(mean log p) at `exp_v3_all.py:208`.
6. sigmoid in the text at v2 line 130 and v3 line 140.
7. The v1 text label definition at line 126.
8. The AST formula at `exp_v3_all.py:267`.
9. TACE `int(np.sqrt(n))` bins at `exp_v3_all.py:80`.
10. The v1 SFT threshold 0.7 at `exp2_dpo_training.py:203`.

In addition, no `manual_seed`, `set_seed`, or `np.random.seed` call exists in v1 to v3, and the
summary-table tally (11 AGREE, 15 DIFFER, 4 ABSENT) was recounted.

## 2. Twelve most consequential DIFFER and ABSENT entries (method inventory)

These are taken from `docs/s2/METHOD_INVENTORY.md` section 12, in its ranking. They record divergence
only and do not say which side is correct.

1. **v1 correctness label:** the text gives the deterministic tau = 0.1 generation; the code uses the
   first tau = 0.8 sample (`exp1_optimized.py:134`).
2. **Log-probability transform:** the v2 and v3 texts give sigmoid(mean log p); the code computes
   exp(mean log p). Stored values (0.59 to 0.999) fit only the exp form.
3. **Which generation each confidence describes (ABSENT in the texts):** log-prob comes from a fresh
   sample, verbal from a separate unexecuted response, and the label from the first or an 11th
   sample.
4. **AST proxy:** the text describes the largest-cluster share with name normalization; the code
   uses max(0, 1 - (K - 1)/9) over raw AST dumps.
5. **Verbal prompts:** the quoted and appendix prompts are not the code prompts, in all versions.
6. **MBPP execution:** signature enforcement is described in the v2 text; the code aliases the first
   `def`, and the v1 MBPP producer has no fix.
7. **v2 "held-out" SFT set:** it overlaps the SFT training source.
8. **SFT data and readout:** the tier sentences are longer than quoted, `incorrect_honest` examples
   are not mentioned, and SFT-phrase-first parsing is applied to base-model answers.
9. **Verbal parsing (ABSENT in the texts):** unparsed answers default to 0.6, with a different
   keyword ladder per script.
10. **n = 20 sensitivity row:** it comes from a different script (`exp_final_a100.py`) with stored
    pass@1 0.0875.
11. **TACE:** the code uses floor(sqrt n) equal-count bins, a 0.01 gap filter, and share weighting;
    the text gives an unweighted equal-mass mean.
12. **v1 SFT tier threshold:** 0.8 in the text, 0.7 in the code.

The inventory also records:

- the labels used for the SFT tables;
- that Brier and AUROC are stored as bootstrap means;
- that generation is unseeded (items 13 to 15).

`src/v4_dprc` is described in section 11 (designed stages, gates, and status: only a 5-problem dry
run exists, and stage (b) and phases 3 to 5 were never built).

## 3. TMLR rubric headline

Source: `docs/s2/venue/TMLR_RUBRIC.md`. Every quotation in it is verbatim from the pages saved in
`docs/s2/venue/sources/` (12 jmlr.org/tmlr pages, all HTTP 200).

- **Length:** no page limit. "Submissions may be any length, but a paper's length should be
  justified by its content". Main bodies over 12 pages get longer review timescales.
- **Anonymity:** double-blind. The PDF, supplementary material, and linked artifacts must be
  anonymized. arXiv preprints are allowed.
- **Required statements:**
  - A Broader Impact Statement is required only for work with significant risk of harm.
  - Use of LLM tools must be disclosed in a first-page footnote (TMLR FAQ).
  - No mandatory reproducibility checklist was found on the fetched pages.
- **Template:** the official style file and template are mandatory, and alterations may lead to
  rejection without review.
- **Certifications:** Outstanding, Featured, Reproducibility, Survey, J2C, and Expert. The FAQ states
  that as of 2026-09-01 TMLR no longer considers survey papers.
- **Template provenance:** the official repository is JmlrOrg/tmlr-style-file, at HEAD
  `7bf90efe3a0debbba703c05c43f3ff7e4d4a2992` (2023-06-30). The jmlr.org author guide links to it.
  It is copied unmodified to `paper/tmlr-template/` with `PROVENANCE.md`.
- **Local copy:** the folder "~/Downloads/TMLR Formatting" is a different repository with no remote.
  Its template files are byte-identical to upstream.
- **Build:** the template's example builds with `latexmk -pdf` (pdfTeX 1.40.29, TeX Live 2026) to 7
  pages with no errors. It produced 3 underfull-vbox messages and one unclosed `\bgroup` warning,
  which is an upstream quirk at `main.tex` line 244.
- **Not readable headlessly:** the OpenReview TMLR group page (a JavaScript shell). Pages on
  non-permitted hosts are recorded as pointers.

## 4. Literature-search tooling

The project's literature-search tooling is a locally installed research pipeline.

- **Version:** the CLI reports v0.8.5, and the installed package metadata reports 0.8.6.
- **Invocation:** it is invoked through a slash command whose router dispatches to 16 step
  procedures. A light tier runs 5 of them (steps 1, 2, 10, 15, and 16) and a full tier runs all 16.
  The steps cover query decomposition, a width search, a contradiction graph, depth investigation,
  drafting, adversarial critique, patching, and polishing.
- **Agents:** it spawns 14 agent types, 5 pinned to a mid-size model and 9 to the largest model.
  None is pinned to the small model. The patching and polishing agents are restricted to
  read-and-edit tools.
- **Output:** it writes to a `research/` directory: notes, raw PDFs, run scaffolds, and temporary
  artifacts. A vault-root setting exists, but the step procedures hard-code `research/`.
- **Headless retrieval:** retrieval of public pages runs fully headless with the default HTTP
  provider. Login-gated sites require a one-time interactive browser profile, and with a profile
  five social-media domains switch to a visible browser.
- **Dependency inconsistency:** its own files contain one, a setup hint naming a package extra that
  does not exist.

The full note is local and untracked (`.claude/notes/hyperresearch.md`).

## 5. Accepted model identifiers

Evidence comes from the installed command-line tool (version 2.1.321) and from this session.

- **`--model` / `/model`:** the CLI help says it accepts "an alias for the latest model (e.g.
  'fable', 'opus', or 'sonnet') or a model's full name". The full names published for this
  installation are `claude-fable-5-2`, `claude-opus-5-5`, `claude-sonnet-5-5`, and
  `claude-haiku-5-5`.
- **Sub-agents:** the per-agent model option accepts the aliases `sonnet`, `opus`, `haiku`, and
  `fable`. Agent-definition frontmatter accepts the same aliases: the existing definitions use
  `opus` and `sonnet`, and the five new ones use `haiku`, `sonnet`, and `opus`.
- **Exercised this wave:**
  - `sonnet`: B1 and B2 sub-agents.
  - `haiku`: B3 sub-agent.
  - `opus`: the orchestrating session ran on `claude-opus-5-5`.
- **Fable:** it is listed as selectable in both places (`--model` alias and sub-agent option) but
  was not exercised.
- **Not tested:** no full identifier was test-invoked. Starting nested sessions would contact a host
  outside this wave's permitted network list.

## 6. Deviations

1. **Sub-agent output paths.** The task named `paper/tmlr-template/` and `docs/s2/venue/` as B2
   outputs, but the guardrail limits sub-agents to `docs/s2/parts/<agent>/`. B2 therefore wrote to
   `docs/s2/parts/venue/` and to a git-ignored `scratch/venue/` (clone and build). The orchestrator
   copied the clone (minus `.git`, verified identical with `diff -rq`) and the merged files to the
   final paths.
2. **Scratch ignore.** `scratch/` is excluded through `.git/info/exclude` (local), not `.gitignore`.
   `.gitignore` was left unchanged.
3. **Freeze scope is stricter than "modification or deletion".** The hook also rejects additions and
   renames under the frozen directories, and it covers the whole of `REPRODUCE.md`, including the new
   banner.
4. **Em-dashes.** The merged `TMLR_RUBRIC.md` uses " | " separators. The raw copy in
   `docs/s2/parts/venue/` keeps the em-dash separators that the orchestrator's own prompt specified.
   Verbatim quotations, saved source pages, and one verbatim prompt file
   (`v4_selftests_test_prompt.txt`) keep em-dashes, because they are source text.
5. **Timing.** The five agent definitions and the agent-instruction update were written while B1 was
   still running, instead of after B1 to B3 had returned. They are untracked and did not depend on
   B1 output. `docs/CONTEXT.md` was written after all three returned.
6. **Copy of the agent-instruction file.** A pre-edit copy is kept at
   `scratch/CLAUDE.md.pre-w2` (untracked, ignored). It contains the old CLI path with the
   collaborator's home directory.
7. **Hook layout.** The freeze check is numbered 5 but placed before check 4 (gitleaks) in the hook
   file.
8. **B3 summary.** B3's summary misstated the agent-model count. Its note is correct (14 agents:
   5 mid-size, 9 large), which was verified against the frontmatter.
9. **Agent-instruction file.** The CLI path was fixed (24 occurrences), and a project section was
   added outside the tool's managed block. Its stale "Today is" date line inside that block was not
   changed.

## 7. Items needing operator input

1. **[OPERATOR] Decide v4 (DPRC) scope.** Say whether `src/v4_dprc` is in scope for the TMLR paper.
   If it is, a later wave designs a new v4 pipeline outside the frozen paths. If not, record it as
   unrun future work in `docs/CONTEXT.md`.
2. **[OPERATOR] Choose definitions for the new pipeline.** For each DIFFER entry in section 2, state
   which definition the new pipeline implements: label protocol, log-probability transform, AST
   formula, TACE, prompts, MBPP execution, SFT split, and seeds.
3. **[OPERATOR] Rotate infrastructure access (carried from W0).** If the former GPU host or its key
   pair is still live, revoke the key and terminate or re-IP the host.
4. **[OPERATOR] Keep local unredacted copies private.** Keep the pristine backup under
   `~/Developer/_backups/` private. Delete `scratch/CLAUDE.md.pre-w2` if you do not want a local copy
   of the old path.
5. **[OPERATOR] Read the OpenReview submission form.** While logged in, open
   https://openreview.net/group?id=TMLR and record the submission-form fields and checkboxes (any
   checklist, statements, or supplementary upload rules) for addition to `TMLR_RUBRIC.md`.
6. **[OPERATOR] Decide the LLM-use disclosure.** Choose the wording of the first-page footnote that
   the TMLR FAQ requires for LLM tool use.
7. **[OPERATOR] Confirm the freeze strictness.** The hook also blocks new files under `results/` and
   `data/`. Confirm that new pipeline outputs go to new top-level paths, or authorize a hook edit in
   its own commit.
8. **[OPERATOR] Decide on Fable.** Say whether Fable should be used for any agent role. If so, try
   `/model fable` once to confirm access, and a later wave updates the agent definitions.
9. **[OPERATOR] Optional: reinstall the literature-search CLI.** Its version report (0.8.5) disagrees
   with its package metadata (0.8.6).
