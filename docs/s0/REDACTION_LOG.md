# S0 Redaction Log

Wave 0 secret and identifier scrub. Original values are not recorded here. The
unredacted originals exist only in the local, read-only pristine backup taken
before any change (outside the repository).

Line numbers refer to the files as committed. Every redaction is a single in-place
replacement on one line, and nothing else in these files was changed.

| # | File | Line | Class | Replacement token |
|---|------|------|-------|-------------------|
| 1 | docs/methodology.md | 75 | infrastructure identifier (GPU host IP) | `[REDACTED-IP]` |
| 2 | docs/research-state.md | 41 | infrastructure identifier (GPU host IP, SSH target) | `[REDACTED-IP]` |
| 3 | docs/research-state.md | 41 | infrastructure identifier (SSH key filename) | `[REDACTED-KEYFILE]` |
| 4 | REPRODUCE.md | 81 | infrastructure identifier (GPU host IP, script default) | `[REDACTED-IP]` |
| 5 | REPRODUCE.md | 85 | infrastructure identifier (SSH key filename) | `[REDACTED-KEYFILE]` |
| 6 | REPRODUCE.md | 86 | infrastructure identifier (SSH key filename) | `[REDACTED-KEYFILE]` |
| 7 | src/v3_multimodel/deploy_v3.sh | 4 | infrastructure identifier (GPU host IP, usage comment) | `[REDACTED-IP]` |
| 8 | src/v3_multimodel/deploy_v3.sh | 8 | infrastructure identifier (GPU host IP, default argument) | `[REDACTED-IP]` |
| 9 | src/v3_multimodel/deploy_v3.sh | 9 | infrastructure identifier (SSH key filename) | `[REDACTED-KEYFILE]` |
| 10 | docs/README_original.md | 63 | infrastructure identifier (SSH key filename) | `[REDACTED-KEYFILE]` |
| 11 | docs/README_original.md | 99 | infrastructure identifier (SSH key filename) | `[REDACTED-KEYFILE]` |

Notes:
- Rows 1, 2, 4, 7 and 8 are all the same public IPv4 address.
- Rows 3, 6, 10 and 11 are one key filename, and rows 5 and 9 are a second key filename.
- Rows 10 and 11 were redacted in the original top-level `README.md`. That file was then
  moved unchanged to `docs/README_original.md`, so the new three-line `README.md` could
  take its place.
- `src/v3_multimodel/deploy_v3.sh` still passes `bash -n`. Running it now needs the
  host IP as its first argument and a real key path in `KEY`.

Credentials found: none. `gitleaks dir` found no leaks before or after redaction. The scan
also covered the zip archives (scanned directly, and extracted), PDF text extracted with
pdftotext, and printable strings from the local SQLite index.

Files withheld from git (via `.gitignore`), not redacted:
- No key or credential files are present in the bundle. The `credentials/` directory named
  in the original README does not exist here, and `*.pem`, `*.key`, `.env*` and
  `credentials/` are ignored anyway.
- `src/v4_dprc/README.md` is withheld because it references a local agent-tool plan path.
  It needs an operator decision; see `docs/s0/W0_REPORT.md`.

## W1 (2026-11-10)

Operator decision A3: personal home path replaced with the placeholder `<user-home>`.
The drive or mount prefix in front of the home directory (`C:` and `/c`) was replaced
together with it, so each line now reads `<user-home>/...`. `/home/ubuntu` paths were
left untouched by design.

| # | File | Line | Class | Replacement token |
|---|------|------|-------|-------------------|
| 12 | research/runs/archive-aaai-bar-eval-dprc-d78e07-20260720T063245Z/scaffold.md | 15 | personal identifier (home path) | `<user-home>` |
| 13 | research/runs/archive-code-llm-calibration-aaai27-eabf3f-20260719T195636Z/scaffold.md | 15 | personal identifier (home path) | `<user-home>` |

## W2 (2026-11-10)

Operator decision A1: the collaborator's home-directory path, with any drive prefix (`C:`), was
replaced with the placeholder `<user-home>` in every tracked file outside `src/`, `papers/`,
`results/` and `data/`. Only `docs/s0/W0_REPORT.md` contained it. Three research notes contain the
same given name as part of published author names in reference lists; these are not paths and were
not changed. No occurrence was found inside `src/`, `papers/`, `results/` or `data/`. Git history
keeps the earlier text (no history rewrite).

| # | File | Line | Class | Replacement token |
|---|------|------|-------|-------------------|
| 14 | docs/s0/W0_REPORT.md | 71 | personal identifier (home path) | `<user-home>` |
| 15 | docs/s0/W0_REPORT.md | 82 | personal identifier (home path) | `<user-home>` |
| 16 | docs/s0/W0_REPORT.md | 114 | personal identifier (home path) | `<user-home>` |
| 17 | docs/s0/W0_REPORT.md | 117 | personal identifier (home path, with drive prefix) | `<user-home>` |
