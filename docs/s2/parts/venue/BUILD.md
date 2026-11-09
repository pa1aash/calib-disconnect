# Build of the TMLR example document

Date: 2026-11-10. Location: `scratch/venue/build/` (a copy of the upstream clone at `7bf90efe3a0debbba703c05c43f3ff7e4d4a2992`, minus `.git`, with the shipped `main.pdf` removed before building). No artifacts were written elsewhere.

## Command

```
cd scratch/venue/build
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

## Toolchain

- pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026)
- latexmk 4.88 (9 March 2026)
- BibTeX 0.99e (TeX Live 2026)
- pdfinfo (Poppler) for page count

## Result

- Success (latexmk exit code 0), about 3.8 s wall time.
- Output `main.pdf`: 7 pages, letter (612 x 792 pts), producer pdfTeX-1.40.29. The shipped `main.pdf` and `main-accepted.pdf` in the upstream repository are also 7 pages each.
- BibTeX: no warnings (`warning$ -- 0`).

## Warnings and errors (summarized)

- No LaTeX errors and no undefined references or citations.
- Three "Underfull \vbox (badness 10000) has occurred while \output is active" messages (float or page-break cosmetics).
- "(\end occurred inside a group at level 1)": caused by an unclosed `\bgroup` at `main.tex` line 244 (`\bgroup` in the "Sets and Graphs" notation table, with no matching `\egroup`). This is an upstream template quirk; it is harmless for this build and is left unmodified in the upstream copy. Whoever adopts the template for the paper should not copy that notation table.
- The default options produce the anonymous version (author block replaced with "Anonymous authors / Paper under double-blind review").
