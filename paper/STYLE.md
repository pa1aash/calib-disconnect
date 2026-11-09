# Writing brief for the manuscript

This brief is binding for every pass that drafts or revises text in `paper/`. It turns the sixteen
categories of the prose audit prompt (`docs/style/prose-audit-prompt.md`) and the project
conventions into write-time rules, so that defects are not written in the first place.

## How the rules are enforced

- **HARD** rules are either checked by the prose linter or block the audit. A draft with any HARD
  finding is not handed on. Run the linter on every source file you touch:
  `python3 tools/prose_lint.py paper/<file>.tex --md <report>.md`. It exits non-zero on any HARD
  finding. Severities live in `tools/prose_lint.toml`.
- **JUDGMENT** rules are reviewed by the prose audit (the audit prompt pasted above the manuscript).
  The linter may raise a warning for some of them; a warning is a prompt to look, not a verdict.
- When a rule and a linter result disagree, the rule wins. Report the false positive or false
  negative so the linter can be fixed; do not rewrite a correct sentence to please the linter.
- Examples marked with a file and line are real instances from the frozen legacy manuscript
  `papers/v3/main.tex` (reference only; it is not edited and is not the base of the new paper).
  Examples marked "constructed" were written for this brief.

## Rule index

| # | Rule | Audit category | Class |
|---|------|----------------|-------|
| 1 | American spelling | 15 | HARD |
| 2 | No em-dashes | 15 | HARD |
| 3 | Serial comma | 15 | JUDGMENT |
| 4 | Formal register | 16 | JUDGMENT |
| 5 | Title with no colon and no question mark | 7 | HARD |
| 6 | State the claim; no rhetorical negation | 1 | HARD |
| 7 | No rule-out cascades or mirrored contrasts | 1 | JUDGMENT |
| 8 | No significance announcers | 2 | HARD |
| 9 | No roadmap sentences or summary-before-results paragraphs | 3 | HARD |
| 10 | No trailing appositive qualifications | 4 | JUDGMENT |
| 11 | No softening adverbs; no contradictory pairs | 5 | HARD (pairs), JUDGMENT (adverbs) |
| 12 | No "What" openers or emphatic clefts | 6 | HARD ("What"), JUDGMENT (clefts) |
| 13 | Headings name their content | 7 | HARD (form), JUDGMENT (content) |
| 14 | Captions describe and instruct, at most three sentences | 8 | HARD (length), JUDGMENT (content) |
| 15 | One figure style, no in-figure annotations, every figure necessary | 8 | HARD |
| 16 | No run-on or over-nested sentences | 9 | JUDGMENT |
| 17 | At most two aphoristic paragraph endings | 10 | JUDGMENT |
| 18 | No internal labels, process words, paths, or code identifiers | 11 | HARD |
| 19 | No narrated process or belief revision | 11 | JUDGMENT |
| 20 | One name per concept, fixed in the glossary | 12 | JUDGMENT |
| 21 | Every number comes from a generated macro | 13 | HARD |
| 22 | Precision matches the evidence | 13 | HARD (p-values), JUDGMENT (rest) |
| 23 | Every abstract and introduction claim maps to a stated result | 14 | HARD |
| 24 | Structure puts results where readers look | 14 | JUDGMENT |
| 25 | Anything that makes a reader stop | 16 | JUDGMENT |

## Conventions

### Rule 1. American spelling (HARD)

Use American spelling throughout, including in captions, tables, and the appendix. The linter
holds the British-to-American list.

- Bad (constructed): "We analyse the behaviour of the calibrated models and summarise the colour
  scale."
- Good: "We analyze the behavior of the calibrated models and summarize the color scale."

### Rule 2. No em-dashes (HARD)

Do not use the em-dash (`---` in LaTeX source or the Unicode character). Use a period, a colon in
running prose, parentheses, or a comma. En-dashes (`--`) for ranges are fine.

- Bad (constructed): "Sampling is expensive --- each problem needs ten generations."
- Good: "Sampling is expensive. Each problem needs ten generations."

### Rule 3. Serial comma (JUDGMENT)

Put a comma before the final "and" or "or" in every list of three or more items.

- Bad (constructed): "We report ECE, Brier score and AUROC."
- Good: "We report ECE, Brier score, and AUROC."

### Rule 4. Formal register (JUDGMENT)

Write in a formal, plain register. No contractions, no exclamation marks, no rhetorical questions in
the body, no colloquial intensifiers ("striking", "dramatic", "huge"), and no second person
addressed to the reader.

- Bad (`papers/v3/main.tex:357`): "This result is particularly striking: the model's verbalized
  self-assessment expresses high confidence in solutions that never pass a single test case."
- Good: "The model states high confidence on solutions that pass no test case."

## Title, negation, and announcements

### Rule 5. Title with no colon and no question mark (HARD)

The title names the finding or the object of study in one clause.

- Bad (`papers/v3/main.tex:51`): "Mind the Gap: The Calibration Disconnect Between Internal and
  Expressed Confidence in Code Language Models"
- Good (constructed): "Internal and Expressed Confidence Disagree in Code Language Models"

### Rule 6. State the claim; no rhetorical negation (HARD)

Write Y. Do not write "not X but Y", "not merely X", "not only X but Y", or "not A, not B, but C".
If X must be ruled out, rule it out in its own sentence with a reason and a number. Genuine
technical contrasts are allowed when the contrast carries information, for example "the test is
conservative rather than exact". "rather than" is a linter warning, reviewed by the audit.

- Bad (`papers/v3/main.tex:84`): "...proving the failure is fundamental, not a calibration
  artifact."
- Good (constructed): "Recalibration lowers ECE and lowers AUROC, so the ranking information is
  absent from the raw scores."
- Bad (`papers/v3/main.tex:86`): "...the improvement reflects better defaults rather than
  problem-sensitive uncertainty."
- Good (constructed): "After fine-tuning, the model gives the same confidence to easy and hard
  problems."

### Rule 7. No rule-out cascades or mirrored contrasts (JUDGMENT)

Do not open with three or more sentences that rule out alternatives before the claim appears. Do
not state the same distinction in both directions in different sections.

- Bad (constructed): "This is not a prompting effect. It is not a temperature effect. Nor is it a
  parsing artifact. The gap is present at every scale."
- Good (constructed): "The gap is present at every scale, under three prompts and two
  temperatures (Table 3)."

### Rule 8. No significance announcers (HARD)

Delete "it is worth noting", "it is important to", "crucially", "notably", "importantly", "the key
point is", "what matters here is", and similar. Keep the claim.

- Bad (`papers/v3/main.tex:608`): "The SFT analysis reveals a subtle but important distinction
  between calibration and discrimination."
- Good (constructed): "Fine-tuning improves calibration and leaves discrimination unchanged."

### Rule 9. No roadmap sentences or summary-before-results paragraphs (HARD)

Do not announce what a section, table, or figure will do ("this section", "in this section", "the
rest of this paper", "Section 4 shows", "Table 1 collects"). Build the content. Do not open a
results section with an abstract-shaped paragraph that the following paragraphs restate; keep only
its unique sentences. The phrase checks are linted; restated paragraphs are reviewed.

- Bad (`papers/v3/main.tex:362`): "Table~\ref{tab:temperature} and Figure~\ref{fig:temp_ece}
  present calibration metrics across four temperatures on a fixed 80-problem HumanEval subset."
- Good (constructed): "Sampling ECE rises from \ResSampEceLowTemp{} to \ResSampEceHighTemp{} as the
  temperature rises (Table~\ref{tab:temperature})."

## Sentence-level hedging and emphasis

### Rule 10. No trailing appositive qualifications (JUDGMENT)

Do not tack a hedge, confession, or editorial clause onto the end of a sentence after a comma.
Promote it to its own sentence, move it to the limitations, or delete it. Check that a trailing
modifier attaches to the noun you mean.

- Bad (`papers/v3/main.tex:616`): "Potential benchmark contamination is a consideration, though our
  central finding concerns the \emph{gap} between methods rather than absolute performance."
- Good (constructed): "The benchmark may be in the training data. Section 6 tests this with
  problems released after each model's training cutoff."

### Rule 11. No softening adverbs; no contradictory pairs (HARD for pairs, JUDGMENT for adverbs)

A binary claim is true or false. Delete softening adverbs (arguably, somewhat, fairly, rather,
quite, perhaps, seemingly, essentially, virtually, largely, generally, typically, usually, roughly,
comfortably, clearly, actually, exactly, almost, nearly, real, really, relatively, effectively,
particularly), or replace the hedge with the number that justifies it. Contradictory pairs ("almost
exactly", "essentially always") are HARD. Evaluative adjectives that do argumentative work ("a
natural construction", "a reasonable choice", "a realistic setting") need a definition or must go.

- Bad (`papers/v3/main.tex:608`): "...the confidence distribution collapses to essentially a single
  bin."
- Good (constructed): "\ResSftModalShare{} of problems receive the same confidence value."
- Bad (`papers/v3/main.tex:362`): "Verbal ECE is effectively constant..."
- Good (constructed): "Verbal ECE varies by less than \ResVerbEceRange{} across temperatures."

### Rule 12. No "What" openers or emphatic clefts (HARD for "What", JUDGMENT for clefts)

Do not start a sentence with "What". Rewrite "It is X that ..." and "There is/are X which/that ..."
when they exist only for emphasis.

- Bad (constructed): "What this shows is that probes outrank verbal reports."
- Good: "Probes outrank verbal reports."
- Bad (`papers/v3/main.tex:588`): "There is no training signal for calibrated self-assessment..."
- Good (constructed): "Standard training objectives contain no term for the accuracy of stated
  confidence."

## Headings, captions, and figures

### Rule 13. Headings name their content (HARD for form, JUDGMENT for content)

A heading names what the section contains so a reader scanning the contents can find it. HARD (linted):
no colon, no question mark, no three-item "A, B, and C" list, no suffix "in full", "revisited", or
"in detail". JUDGMENT: no argument or result in a heading, no paired rhetorical headings, no two
results in one heading.

- Bad (`papers/v3/main.tex:328`): "Test-Free Confidence: AST Clustering"
- Good: "Syntax-Tree Agreement"
- Bad (`papers/v3/main.tex:590`): "Post-Hoc Calibration Cannot Fix Discrimination"
- Good: "Recalibration and Discrimination"

### Rule 14. Captions describe and instruct, at most three sentences (HARD for length, JUDGMENT for content)

A caption states what is plotted or tabulated and how to read it, in at most three sentences and
60 words (linted). It does not argue, interpret, or justify a design choice; it does not restate a
claim from the body; it holds no specification that belongs in the method section; and it never
holds a measurement that appears nowhere else.

- Bad (`papers/v3/main.tex:574`): "...SFT collapses to a single default (0.9 for 95\% of problems),
  achieving better calibration through a more accurate prior rather than problem-sensitive
  discrimination."
- Good (constructed): "Share of problems at each stated confidence value, before and after
  fine-tuning. Bars sum to one within each model."
- Bad (`papers/v3/main.tex:340`): "...ECE reveals systematic overconfidence across all non-sampling
  methods."
- Good (constructed): "Calibration metrics for the second model family on HumanEval. Intervals are
  bootstrap 95\% intervals."

### Rule 15. One figure style, no in-figure annotations, every figure necessary (HARD)

All figures share one style: the same fonts, sizes, palette, line weights, marker set, and axis
conventions, set in one shared plotting module under `paper/figures/`. Do not place annotations,
callouts, arrows, text boxes, or value labels inside the plot area; the axis labels, legend, and
caption carry the reading. Each figure must support a claim in the body that a table cannot carry
as well; otherwise cut it or move it to the appendix. Checked in figure review; a violation blocks
the audit.

- Bad (constructed): a reliability diagram with an arrow and the text "overconfident!" inside the
  axes, in a different font from the other figures.
- Good: the same diagram with only the diagonal, the bins, the axis labels, and the legend, drawn
  by the shared style module.

### Rule 16. No run-on or over-nested sentences (JUDGMENT)

Split any sentence with four or more comma-joined clauses, a parenthetical inside a parenthetical,
or three or more independent findings joined by commas.

- Bad (`papers/v3/main.tex:66`): "We conduct the first systematic comparison of seven confidence
  estimation methods for code language models, spanning sampling consistency, token
  log-probabilities with post-hoc calibration (isotonic regression and Platt scaling), AST-based
  clustering (a test-free proxy), and verbalized self-assessment at matched and mismatched
  temperatures."
- Good (constructed): "We compare seven confidence methods for code language models. They fall
  into four families: sampling agreement, token probabilities, syntax-tree agreement, and stated
  confidence."

### Rule 17. At most two aphoristic paragraph endings (JUDGMENT)

Short, quotable closing sentences establish an overclaiming voice. Keep at most two in the paper.
The linter counts paragraph-final sentences of eight words or fewer as warnings.

- Bad (constructed): "...under every prompt we tried. The model knows; it does not say."
- Good (constructed): "...under every prompt we tried. Probe accuracy exceeds stated-confidence
  accuracy on all \ResNumModels{} models."

## Leakage, terminology, and numbers

### Rule 18. No internal labels, process words, paths, or code identifiers (HARD)

Paper prose contains none of: internal tracking labels (letter-plus-digit codes such as the
candidate or work-package names used in planning documents), the words session, wave, and gate,
file paths, script names, or underscore identifiers. Code identifiers that a reader needs go in
`\texttt{}`; dataset names go in their published form.

- Bad (constructed): "The L2 analysis in exp\_v3\_all.py passes the first gate."
- Good (constructed): "The probe analysis (Section 5) meets the preregistered accuracy threshold."
- Real instance of the permitted form (`papers/v3/main.tex:701`): "\texttt{openai\_humaneval}".

### Rule 19. No narrated process or belief revision (JUDGMENT)

Do not narrate how the project changed its mind ("originally we thought", "contradicting our
earlier claim"), refer to things the reader cannot see ("this study's budget", "our internal
threshold"), or phrase preregistration as narrative. State the fact and, where it matters, the
date or document that fixes it.

- Bad (constructed): "We originally expected verbal confidence to improve with scale, but it did
  not."
- Good (constructed): "Verbal ECE does not decrease with parameter count (Figure 3)."

### Rule 20. One name per concept, fixed in the glossary (JUDGMENT)

Each concept has one name, one symbol, and one definition, recorded in the glossary below before
drafting begins. Do not reuse a symbol for two quantities. Define every term before first use. Do
not give a bare definite noun ("the gate", "the box") without naming it first.

- Bad (`papers/v3/main.tex:79` and `papers/v3/main.tex:51`): sampling agreement is called "the
  internal uncertainty signal" in the introduction, while the title's "internal" confidence would
  ordinarily mean hidden-state readouts.
- Good (constructed): "sampling agreement" everywhere for the fraction of samples that agree, and
  "hidden-state probe" for readouts of internal activations.

### Rule 21. Every number comes from a generated macro (HARD)

Every number in the paper (text, tables, captions, and appendix) is a LaTeX macro generated from a
JSON file under `analysis/`, and each macro records the file and key it came from. Never type a
result by hand, copy it from a log, or round it in the text. The linter flags decimal numerals in
prose outside the number macros; integers that are results (counts, sample sizes) must also be
macros, which the audit checks.

- Bad (`papers/v3/main.tex:228`): a caption that prints "pass@1\,=\,0.823" by hand, while the
  corresponding result file holds 0.884 (`docs/s1/BUNDLE_MAP.md` section 3.2).
- Good (constructed): "pass@1 is \ResPassAtOneHumanEval{}." with the macro generated from
  `analysis/` JSON.

### Rule 22. Precision matches the evidence (HARD for p-values, JUDGMENT for the rest)

Report p-values and Monte Carlo quantities to at most two significant figures (linted). Report each
quantity at one precision everywhere it appears. State a resolution floor or clipped bound as such
instead of repeating it as if it were a measurement. Make every comparative name its comparison.

- Bad (`papers/v3/main.tex:66` and `papers/v3/main.tex:238`): ECE is printed as "0.059" in the
  abstract and as ".047" (no leading zero) in the table.
- Good (constructed): one macro format for all ECE values, for example three decimals with a
  leading zero in both places.
- Bad (constructed): "p = 0.01234 (10,000 permutations)."
- Good (constructed): "p = 0.012 (10,000 permutations)."

## Structure and claims

### Rule 23. Every abstract and introduction claim maps to a stated result (HARD)

Each claim in the abstract and introduction must point to a specific table, figure, or section
whose result states it at the same strength. Keep a claim map (claim, location of the supporting
result, macro names) beside the draft; the audit blocks any unmapped claim. Novelty claims ("the
first") need a positioning record that supports them, or they are removed.

- Bad (`papers/v3/main.tex:66`): "We conduct the first systematic comparison of seven confidence
  estimation methods for code language models", with no supporting search record.
- Good (constructed): "We compare seven confidence methods against execution outcomes on three
  benchmarks (Section 4)."

### Rule 24. Structure puts results where readers look (JUDGMENT)

Results go in results sections, never in background or related work. Order sections so that no
forward reference needs a later repair sentence. Do not state the same content three times in the
abstract, introduction, and a section opening. End with a conclusion that states the recommendation
a reader should act on; do not end on limitations.

- Bad (`papers/v3/main.tex:626`): the conclusion repeats the abstract's findings in the same order
  ("sampling-based confidence achieves AUROC\,=\,0.987 with independent labels, while post-hoc
  calibration...").
- Good (constructed): a conclusion that states the recommendation ("Route verification effort by
  sampling agreement; do not use stated confidence") and the one open question it leaves.

### Rule 25. Anything that makes a reader stop (JUDGMENT)

Fix unclear antecedents, buried subjects, jargon before definition, sentences that need a second
reading, and metaphors that do not survive scrutiny.

- Bad (`papers/v3/main.tex:608`): "This is analogous to a weather forecaster who always says ``90\%
  chance of sun'' in a sunny climate; they will have low ECE but no ability to predict rain."
- Good (constructed): "A constant forecast equal to the base rate has low ECE and an AUROC of 0.5."
  (with both numbers as macros if they are results).

## Terminology glossary

To be filled at the design stage, before any drafting. One row per concept: preferred term, symbol,
definition, and terms not to use.

| Term | Symbol | Definition | Do not use |
|------|--------|------------|------------|
