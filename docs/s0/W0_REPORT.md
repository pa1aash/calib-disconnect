# Wave 0 Report: preflight, secret scrub, repository creation

Date: 2026-11-10 (UTC run started 2026-11-09T20:10Z). No stop condition fired, and every step (1 to 9) was completed.

Step 1 location check: `/Users/palaash/Developer/calib-disconnect` existed, and neither it nor any parent up to `$HOME` was a git repository.

## 1. Toolchain

| Tool | Version / status | Action |
|------|------------------|--------|
| git | 2.54.0 (Apple Git-157) | none |
| gh | 2.89.0; authenticated as `pa1aash` (keyring, https; scopes repo, workflow, gist, read:org, admin:ssh_signing_key) | none |
| python3 | 3.13.12 (miniforge) | none |
| uv | 0.11.6 | none |
| conda | 26.1.1 | none |
| node | missing | none (not in install list) |
| latexmk | 4.88 | none |
| pdflatex | pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026) | none |
| tectonic | 0.15.0 | none |
| chktex | missing | none (not in install list) |
| pdftotext (poppler) | 26.10.0 | none (already present) |
| gitleaks | missing at preflight, now 8.30.1 | installed with `brew install gitleaks` |
| trufflehog | missing | none (not in install list) |
| jq | 1.8.1 | none |

## 2. Located paths

- hyperresearch skill: `~/.claude/skills/hyperresearch/SKILL.md` (router skill, "Hyperresearch V8"). Its 14 subagent definitions are at `~/.claude/agents/hyperresearch-*.md`. The 16 step skills (`hyperresearch-1-decompose` … `hyperresearch-16-readability-audit`) are project-local, under the bundle's ignored agent directory. There is no hyperresearch plugin or plugin-cache entry. The SKILL.md frontmatter has no version field. The CLI `/opt/homebrew/Caskroom/miniforge/base/bin/hyperresearch --version` reports **v0.8.5**, but the installed Python package metadata (`pip show`) reports **0.8.6**.
- Prose audit prompt: two files, `~/Downloads/paper-prose-audit-prompt.md` and `~/Downloads/paper-prose-audit-prompt (1).md`. Neither was read. None were found in ~/Desktop or ~/Documents.
- `~/Downloads/TMLR Formatting`: a git repository, but **not a clone**, because it has no remote configured. Branch `main`, HEAD `d0f97cea0188463580f9d7dbb649cce59b0674ad` (2026-09-28, "Close Session D").

## 3. Inventory summary

Pristine backup: `/Users/palaash/Developer/_backups/calib-disconnect-pristine-20261109T201032Z/`. It holds 617 files and 29,449,148 bytes (identical to the source at copy time) and is read-only (`chmod -R a-w`). It holds the **unredacted** originals.

Top level at preflight (files / bytes):

| Path | Files | Bytes |
|------|------:|------:|
| research/ (notes 225, runs 175, temp 59, index 0) | 463 | 7,132,096 |
| .hyperresearch/ (SQLite index, config, template) | 3 | 18,662,124 |
| papers/ (v1, v2, v3; 13 files each) | 39 | 1,537,937 |
| results/ (v1, v2, v3; v4_dprc empty) | 18 | 1,115,889 |
| src/ (v1_baseline, v2_comprehensive, v3_multimodel, v4_dprc) | 46 | 452,011 |
| archives/ | 3 | 322,857 |
| .claude/ (16 skill files) | 16 | 117,588 |
| docs/ | 5 | 45,049 |
| data/v4_dprc/labels | 2 | 42,259 |
| .remember/ (session-tool state created at session start) | 18 | 2,210 |
| misc/ | 0 | 0 |
| root files: README.md, REPRODUCE.md, CLAUDE.md, .gitignore | 4 | — |

- File types: 281 md, 227 json, 34 py, 12 sty, 9 pyc, 3 each of zip/tex/pdf/bib/bbl/aux/out/blg/bst, 6 log, 2 sh, 1 toml, 1 jsonl, 1 db, plus a few tool state files.
- Files over 10 MB: `.hyperresearch/hyperresearch.db` (18,661,376 B). No files over 50 MB, so none needed a size-based ignore.
- Archives: `archives/icml2026_styles.zip` (224 KB), `archives/dl4cV1.zip` (44 KB) and `archives/dl4cV2.zip` (52 KB). All three were scanned.
- Nested `.git` directories: none. `.env` files: none. Notebooks: none.

## 4. Secret scan

Method: I ran `gitleaks dir --max-archive-depth 3` over the whole folder, which scanned inside dl4cV1.zip and dl4cV2.zip. Gitleaks skips PDFs and the binary SQLite index by default, and it skipped the PDF inside icml2026_styles.zip, so I covered those separately. I extracted all three zips, the pdftotext output of all five PDFs, and `strings` of the SQLite index, then ran gitleaks on those plus a regex scan over everything. As a result, no archive was left unscanned.

Hit counts by class:

| Class | Before | After (committed set) |
|-------|-------:|------:|
| gitleaks findings | 0 | 0 (folder, staged diffs via hook, and full git history) |
| Credentials (sk-, sk-ant-, hf_, AKIA, ghp_, github_pat_, xox, AIza; assigned password/token/secret/api_key values) | 0 | 0 |
| Infrastructure identifiers: IPv4 | 5 (one public address, in 4 files) | 0 |
| Infrastructure identifiers: key filenames | 6 (two distinct .pem names) | 0 |
| Infrastructure identifiers: hosts (runpod/vast/lambda/compute/aws/gcp) | 0 real (3 false positives) | 0 real |
| Personal identifiers: absolute home paths | 694 raw (mostly LaTeX logs and tool state) | 39 (37 `/home/ubuntu`, 2 `/Users/arjun`) |
| Personal identifiers: emails | 427 raw (incl. the SQLite strings dump) | 114, all third-party published author or style-file maintainer addresses, plus the operator's own address in the pre-commit hook |
| Phone-number pattern | 70 raw | 17, all in fetched research notes (numeric IDs, not phone numbers): false positives |
| Keyword words (token/secret/password/api_key) | 4,251 | 1,423, all ML vocabulary (`tokenizer`, `max_tokens`, …): false positives |

False positives in the committed set: `.gitignore` patterns (`*.pem`, `id_rsa*`, `id_ed25519*`); `doi.ieeecomputersociety.org` in one research note (matched "compute"); and the script filename `setup_lambda.sh` (matched "lambda"). Gitleaks reported nothing, so `.gitleaks.toml` was not created and no allowlist was needed.

Redactions made: 11 tokens on 10 lines in 5 files (5 × `[REDACTED-IP]`, 6 × `[REDACTED-KEYFILE]`); see `docs/s0/REDACTION_LOG.md` for the exact table. Absolute home paths and personal identifiers were not redacted (listed below).

Home paths left in committed files:
- `/home/ubuntu/...` appears in REPRODUCE.md (3), src/v1_baseline/* (14 across 9 files), src/v2_comprehensive/* (12 across 5 files), src/v3_multimodel/* (7 across 3 files) and src/v4_dprc/config.py (1).
- `/Users/arjun/...` appears in `research/runs/archive-aaai-bar-eval-dprc-d78e07-20260720T063245Z/scaffold.md` (1) and `research/runs/archive-code-llm-calibration-aaai27-eabf3f-20260719T195636Z/scaffold.md` (1).

Files withheld from git (`.gitignore`):
- Key or credential files: none present. `*.pem`, `*.key`, `.env*` and `credentials/` are ignored pre-emptively.
- `src/v4_dprc/README.md` is withheld because line 6 references a plan file under the local agent-tool home directory. Editing it was outside the step 6 redaction scope. See [OPERATOR] item 2.
- `.hyperresearch/` (local research-vault config and an 18.7 MB rebuildable binary SQLite index) is withheld. See [OPERATOR] item 3.
- `.remember/` (session-tool state), `.claude/` and `CLAUDE.md` (local agent-tool files) are withheld as specified.
- LaTeX intermediates in papers/v1-v3 (`main.aux/.bbl/.blg/.log/.out`) and `src/v4_dprc/__pycache__/` are withheld.

Guardrail deviations (honest record): during classification, two terminal outputs printed the GPU host IP in full. One was an email-pattern match on `ubuntu@<ip>`, and the other was a failed zsh word-split whose fallback grep echoed raw lines. The second one also printed the two key filenames. Neither value was written to any file, commit or remote. All later output was masked.

## 5. Repository facts

- URL: https://github.com/pa1aash/calib-disconnect
- Visibility: public. Default branch: `main` (verified via `gh api repos/pa1aash/calib-disconnect`).
- HEAD before this report: `55796cf662777418b27d7a84587259905aa4e35e`. Remote HEAD matched local HEAD. The commit that adds this report follows it.
- Hooks are tracked in `tools/hooks/` (`pre-commit`, `commit-msg`, `install.sh`) and installed as symlinks in `.git/hooks/`. I tested them on a scratch orphan branch that was deleted afterwards and never pushed. These cases were rejected: commit-msg co-author trailer; pre-commit wrong author identity; staged agent-instruction filename; staged attribution phrase; staged synthetic GitHub token (gitleaks). One clean commit passed both hooks.
- During real commits, the pre-commit hook caught its own comment once (it contained the literal phrase). The comment was reworded and nothing was committed in that attempt.
- License: MIT, from `gh api /licenses/mit --jq .body`, with the year 2026 and the name Palaash Gang.
- Remote checks: `.claude/`, `CLAUDE.md`, `.remember/`, `.hyperresearch/` and `src/v4_dprc/README.md` are all absent.

| SHA | Author | Committer | Message |
|-----|--------|-----------|---------|
| d061e6d | Palaash Gang <palaashgang@gmail.com> | Palaash Gang <palaashgang@gmail.com> | Add repository scaffolding, hygiene hooks, license and readme |
| 5bbe208 | Palaash Gang <palaashgang@gmail.com> | Palaash Gang <palaashgang@gmail.com> | Add redacted research bundle |
| 55796cf | Palaash Gang <palaashgang@gmail.com> | Palaash Gang <palaashgang@gmail.com> | Add wave 0 redaction log |

## 6. Operator actions

1. **[OPERATOR] Rotate infrastructure access.** The GPU host's public IP and the names of two SSH key files sat in plaintext in the local bundle. They are not in git, but the pristine backup keeps them. If that instance or key is still live, revoke the key pair and terminate or re-IP the host.
2. **[OPERATOR] decide on `src/v4_dprc/README.md`.** It is withheld from git because line 6 references a local agent-tool plan file path. Either delete that reference (and the plan pointer) and then track the file, or keep it withheld.
3. **[OPERATOR] decide on `.hyperresearch/`.** It is withheld: `config.toml` is the vault configuration (its exclude list names the agent instruction file), and `hyperresearch.db` is an 18.7 MB rebuildable index. Track `config.toml` only if later sessions need it in the repository.
4. **[OPERATOR] review home paths** listed in section 4. `/Users/arjun` in two run scaffolds names a collaborator's account, and `/home/ubuntu` paths are generic cloud-box defaults in code. They were not redacted, by design.
5. **[OPERATOR] confirm `.bbl` handling.** The pre-existing `.gitignore` said that `main.bbl` was intentionally tracked. W0 now ignores `*.bbl` as instructed, so `papers/v*/main.bbl` are untracked locally.
6. **[OPERATOR] keep the pristine backup private.** `/Users/palaash/Developer/_backups/calib-disconnect-pristine-20261109T201032Z/` holds the unredacted originals, including the IP and key filenames.
7. **[OPERATOR] fix the project agent-instruction file's CLI path (local only, untracked).** It points the hyperresearch CLI at a Windows path (`C:/Users/arjun/anaconda3/Scripts/hyperresearch.exe`) that does not exist on this Mac. The working CLI is `/opt/homebrew/Caskroom/miniforge/base/bin/hyperresearch`.

## 7. Layout observations

- Three full manuscript iterations (papers/v1, v2, v3) each carry their own copies of the ICML 2026 style files. The latest PDF is in v3.
- Two of the zips in `archives/` (`dl4cV1.zip`, `dl4cV2.zip`) are snapshots of earlier manuscripts, and the third is the stock ICML 2026 style kit.
- The original README targets DL4C / ICML 2026. The research run folders are named for AAAI-27, and the next target is TMLR, so the venue has moved three times.
- The original README describes a post-training / human-trust project. That differs in emphasis from the working title supplied for this wave. It is now preserved at `docs/README_original.md`.
- `src/v4_dprc` has 29 files, but `results/v4_dprc/` and `data/v4_dprc/adapters/` are empty. Only dry-run labels exist under `data/v4_dprc/labels/`.
- `misc/`, `research/index/` and `.hyperresearch/exports/` are empty directories. Git does not track empty directories, so they are absent remotely.
- `research/notes/` has several near-duplicate notes with `-2` … `-7` suffixes for the same arXiv paper (2305.14975).
- `research/runs/` holds two archived pipeline runs (126 and 49 files), and `research/temp/` holds 59 working files from the research pipeline.
- `src/v4_dprc/__pycache__/` contains 9 compiled `.pyc` files in the bundle; they are ignored, not tracked.
- The two `paper-prose-audit-prompt` files in ~/Downloads look like a duplicate download.
- The hyperresearch CLI version (0.8.5) and package metadata (0.8.6) disagree.
