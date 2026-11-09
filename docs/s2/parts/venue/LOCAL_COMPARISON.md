# Local copy versus fetched upstream

Compared on 2026-11-10. The fetched official copy (JmlrOrg/tmlr-style-file at `7bf90efe3a0debbba703c05c43f3ff7e4d4a2992`) is authoritative. The local directory "~/Downloads/TMLR Formatting" was treated as read-only.

## Local repository facts

| Item | Value |
|---|---|
| Remote (`git remote -v`) | none configured (empty output) |
| HEAD SHA | `d0f97cea0188463580f9d7dbb649cce59b0674ad` ("Close Session D") |
| Branch | `main` |
| Nature | A separate project repository (audit, docs, papers, submission directories, its own CLAUDE.md), not a clone of the style repository. Its history is unrelated to the upstream SHA. |
| Template subdirectories | `tmlr_template/` and `tmlr_template_testbuild/` |

## File-level diff (`diff -rq`, excluding `.git` and `.DS_Store`)

- Top level: not comparable (it is a different project). Only the two template subdirectories carry style files.
- `tmlr_template/` versus upstream: identical except for one extra file, `tmlr-style-file-main.zip` (a downloaded archive of the `main` branch). All ten upstream files, including both PDFs, are byte-identical.
- `tmlr_template_testbuild/` versus upstream: `main-accepted.pdf` is absent, `main.pdf` differs (it is a local rebuild, not the shipped PDF), and build artifacts are extra (`main.aux`, `main.bbl`, `main.blg`, `main.fls`, `main.log`, `main.out`, `b1.out`, `p1.out`, `p2.out`, `p3.out`). All source files are identical.

## Content diff of shared style files (`cmp`)

| File | `tmlr_template/` | `tmlr_template_testbuild/` |
|---|---|---|
| tmlr.sty | identical | identical |
| tmlr.bst | identical | identical |
| fancyhdr.sty | identical | identical |
| math_commands.tex | identical | identical |
| main.tex | identical | identical |

## Verdict

The style and bibliography files in the local template directories MATCH the fetched official copy exactly (tmlr.sty, tmlr.bst, fancyhdr.sty, math_commands.tex, main.tex, main.bib, LICENSE, README.md). The local directory has no git remote, so its provenance is established here only by content equality with the upstream HEAD, not by history. Use the upstream clone, not the local copy, for the repository's `paper/tmlr-template/`.
