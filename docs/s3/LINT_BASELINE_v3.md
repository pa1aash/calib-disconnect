# Prose lint baseline: legacy v3 manuscript

Wave 3, 2026-11-10. A calibration record for `tools/prose_lint.py`. The legacy text is frozen and
is not to be fixed; this file shows what the linter finds on a real manuscript in this domain, so
that later results on the new paper can be read against it.

- Input: `papers/v3/main.tex` (770 lines, read only; SHA-256 prefix `2bab80b268e558b7`).
- Linter: `tools/prose_lint.py` (SHA-256 prefix `827616574d4e25d3`) with `tools/prose_lint.toml`
  (prefix `3845224b13b6f992`), default severities. Test suite: 171 tests, all passing.
- Command: `python3 tools/prose_lint.py papers/v3/main.tex --json docs/s3/lint/v3_baseline.json --md docs/s3/lint/v3_baseline.md`
- Exit status 1 (HARD findings present).
- Full outputs: `docs/s3/lint/v3_baseline.json` and `docs/s3/lint/v3_baseline.md`.

## Headline

158 findings on 54 lines: 138 HARD and 20 WARN. Hand-typed decimals in prose account for 121 of the
138 HARD findings, because the legacy manuscript prints every result by hand instead of through
generated macros. Excluding them, 17 HARD findings remain: roadmap sentences (6), rhetorical "not X
but Y" (3), colons in the title and running title (2), colons in headings (2), significance
announcers (2), one caption over three sentences, and one em-dash.

## Per-category counts

| Category | HARD | WARN |
|---|---:|---:|
| decimal_in_prose | 121 | 0 |
| roadmap | 6 | 0 |
| negation_not_but | 3 | 0 |
| title | 2 | 0 |
| heading | 2 | 0 |
| significance_announcer | 2 | 0 |
| caption_length | 1 | 0 |
| em_dash | 1 | 0 |
| rather_than | 0 | 10 |
| softening_adverb | 0 | 4 |
| negation_comma_not | 0 | 3 |
| short_paragraph_end | 0 | 2 |
| negation_cascade | 0 | 1 |
| All other categories (internal_label, process_word, file_path, underscore_identifier, pvalue_precision, mc_precision, british_spelling, cleft_what, cleft_it_that, cleft_there_which, contradictory_pair, significantly) | 0 | 0 |
| **Total** | **138** | **20** |

## Twenty worst lines

Ranked by HARD count, then WARN count, then line number. The excerpt is the first 90 characters of
the source line.

| Rank | Line | HARD | WARN | Categories | Excerpt |
|---:|---:|---:|---:|---|---|
| 1 | 362 | 10 | 1 | decimal_in_prose 9, roadmap 1, softening_adverb 1 | `Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece} present calibration metrics acro...` |
| 2 | 357 | 9 | 1 | decimal_in_prose 7, significance_announcer 1, softening_adverb 1, negation_not_but 1 | `Sampling confidence correctly identifies universal failure (ECE\,=\,0.000: all samples fai...` |
| 3 | 220 | 7 | 0 | decimal_in_prose 7 | `Log-probability confidence achieves comparable ECE (0.058) but dramatically worse discrimi...` |
| 4 | 499 | 7 | 0 | decimal_in_prose 6, roadmap 1 | `Table~\ref{tab:sft} presents the SFT results on the 80-problem evaluation subset. The SFT ...` |
| 5 | 224 | 6 | 0 | decimal_in_prose 6 | `Both verbal methods perform poorly. Verbal confidence at $\tau$\,=\,0.1 achieves ECE\,=\,0...` |
| 6 | 326 | 6 | 0 | decimal_in_prose 6 | `The post-hoc calibration results in Table~\ref{tab:main} provide the strongest evidence th...` |
| 7 | 331 | 6 | 0 | decimal_in_prose 5, significance_announcer 1 | `The AST clustering proxy achieves AUROC\,=\,0.689, which is noteworthy for a method requir...` |
| 8 | 518 | 5 | 1 | decimal_in_prose 5, short_paragraph_end 1 | `To understand why, we analyze the SFT model's discrimination on easy and hard problem subs...` |
| 9 | 218 | 5 | 0 | decimal_in_prose 5 | `Sampling-based confidence achieves the best calibration across all metrics by a substantia...` |
| 10 | 424 | 5 | 0 | decimal_in_prose 4, roadmap 1 | `Table~\ref{tab:samples} and Figure~\ref{fig:samples_tradeoff} present the sample count ana...` |
| 11 | 598 | 5 | 0 | decimal_in_prose 5 | `The near-perfect sampling AUROC (0.987) means coding agents could provide highly reliable ...` |
| 12 | 608 | 4 | 2 | decimal_in_prose 4, rather_than 1, softening_adverb 1 | `The SFT analysis reveals a subtle but important distinction between calibration and discri...` |
| 13 | 200 | 4 | 0 | decimal_in_prose 4 | `We evaluate two models: \textbf{Qwen2.5-Coder-7B-Instruct}~\citep{hui2024qwen25coder} as o...` |
| 14 | 205 | 4 | 0 | decimal_in_prose 3, em_dash 1 | `To explore whether verbal confidence can be improved through training, we constructed a 27...` |
| 15 | 251 | 4 | 0 | decimal_in_prose 3, roadmap 1 | `Figure~\ref{fig:reliability} presents reliability diagrams comparing sampling and verbal (...` |
| 16 | 66 | 3 | 2 | decimal_in_prose 3, rather_than 1, negation_comma_not 1 | `AI coding assistants present all generated code with equal certainty, providing developers...` |
| 17 | 588 | 3 | 1 | decimal_in_prose 2, rather_than 1, negation_not_but 1 | `The consistent failure of verbal confidence across both temperatures points to structural ...` |
| 18 | 79 | 3 | 0 | decimal_in_prose 3 | `Our key finding is a striking calibration disconnect: the internal uncertainty signal avai...` |
| 19 | 222 | 3 | 0 | decimal_in_prose 3 | `AST clustering achieves AUROC\,=\,0.689 without requiring test execution, comparable to ra...` |
| 20 | 336 | 3 | 0 | decimal_in_prose 2, roadmap 1 | `Table~\ref{tab:deepseek} presents results for DeepSeek-Coder-6.7B-Instruct, which achieves...` |
## Calibration notes

Every non-decimal finding was read against the source; all 37 are true positives under
`paper/STYLE.md`. Notes:

1. The em-dash (line 205) sits inside a quoted fine-tuning target sentence. The rule still applies
   to the new paper, where quoted model text will go in a verbatim or `\texttt` span.
2. Three classes of defect cited in `paper/STYLE.md` are not linted and are left to the audit
   (JUDGMENT rules): captions that argue (lines 340, 522, 574), headings that state a result (line
   590), and expletive openers without a relative clause ("There is no training signal", line 588).
   The comma contrast "fundamental, not a calibration artifact" (line 84) is caught as a WARN.
3. Three linter gaps were found on this baseline and fixed before it was recorded: the
   `\icmltitle` and `\icmltitlerunning` macros (now in `title_macros`), roadmap sentences of the
   form "Table N and Figure M present", and announcers such as "noteworthy" and "particularly
   striking".
4. Line 216 ("The independent-label pass@1 is 0.823.") is flagged as a decimal and as a short
   paragraph ending. Its number is also one of the manuscript-versus-file mismatches in
   `docs/s1/BUNDLE_MAP.md` section 3.2, the failure that Rule 21 (numbers only from macros) exists to
   prevent.
