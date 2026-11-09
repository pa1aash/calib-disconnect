# Provenance: TMLR LaTeX style files

This file is intended to become `paper/tmlr-template/PROVENANCE.md`. The template files are an unmodified copy of the upstream clone (minus `.git`).

| Item | Value |
|---|---|
| Upstream URL | https://github.com/JmlrOrg/tmlr-style-file |
| Organization | JmlrOrg (also hosts `tmlr`, `tmlr-blog`, `tmlr-infinite-conf`; found with `gh search repos --owner JmlrOrg tmlr`) |
| Official linkage | The TMLR author guide (https://jmlr.org/tmlr/author-guide.html, saved as `sources/author-guide.txt`) links "TMLR LaTeX stylefile" to https://github.com/JmlrOrg/tmlr-style-file/archive/refs/heads/main.zip |
| Default branch | `main` (confirmed with `gh api repos/JmlrOrg/tmlr-style-file`) |
| HEAD commit (full SHA) | `7bf90efe3a0debbba703c05c43f3ff7e4d4a2992` |
| HEAD commit date | 2023-06-30T16:21:15-04:00 ("Removed duplicated line in tmlr.sty") |
| First commit date | 2021-12-06T16:04:24-05:00 |
| GitHub `pushed_at` | 2023-06-30T20:21:20Z (no later pushes) |
| Retrieval date | 2026-11-10 |
| License | Apache License 2.0 (`LICENSE` in repository) |
| Clone location | `scratch/venue/tmlr-style-file-upstream/` (git-ignored) |

## Tracked files at HEAD

| File | Bytes | SHA-256 (first 16 hex) |
|---|---|---|
| LICENSE | 11357 | c71d239df91726fc |
| README.md | 81 | 91310b3f169ecd2d |
| fancyhdr.sty | 17086 | 3d2922548e0e5f1a |
| main-accepted.pdf | 371384 | ac157e281fadd90e |
| main.bib | 629 | cdd86e7d4c31854d |
| main.pdf | 310912 | d0447217845872d2 |
| main.tex | 16787 | 85a994256fae5347 |
| math_commands.tex | 12284 | 90473c4d0542070d |
| tmlr.bst | 26969 | 306fd454cf40771b |
| tmlr.sty | 6560 | 816214ff5919aa45 |

## Notes

- The style option list in `tmlr.sty` is: default (anonymous, "Paper under double-blind review"), `accepted` (camera ready; requires `\month` and `\year`), and `preprint` (de-anonymized, no TMLR mentions).
- The repository ships no version tag; the commit SHA above is the only version identifier.
- The retrieval was performed on 2026-11-10 and the commit has been unchanged since 2023-06-30 per GitHub metadata.
