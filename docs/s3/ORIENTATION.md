# Orientation: what to keep from the legacy study, and what TMLR asks of the new one

Wave 3, 2026-11-10. Inputs: `docs/s1/BUNDLE_MAP.md`, `docs/s2/METHOD_INVENTORY.md` (rows cited as
"MI x.y"), `docs/s2/venue/TMLR_RUBRIC.md`, and the saved TMLR pages in `docs/s2/venue/sources/`.
No legacy number is used as evidence here; legacy numbers are cited only to describe what was
claimed.

## (a) What the legacy work set out to show, and its strongest idea

The legacy study (manuscripts v1 to v3) set out to show that code language models carry a usable
signal about whether their own code is correct, but do not report it. Confidence from agreement
among sampled solutions was claimed to track execution outcomes closely, while token
log-probabilities and the model's stated confidence did not, and fine-tuning the stated confidence
was claimed to improve calibration without improving discrimination.

Its strongest idea is that execution turns the calibration of code models into a measurement
problem with an objective, automatic ground truth. With a test-based label for every problem, and
with the label drawn from a generation that no confidence method saw, the gap between what a
model's behavior reveals and what it says can be measured on thousands of problems instead of
argued from small human-labeled sets.

(The two paragraphs above total 135 words.)

## (b) Legacy design elements: keep or replace

These record the design, not the legacy numbers, which are not carried forward
(`docs/LEGACY.md`).

### Worth keeping

| Element | Why keep it | Rows |
|---|---|---|
| Execution-graded correctness label in an isolated subprocess with a timeout | Objective label; text and code agree on the pass criterion | MI 5.1, MI 5.3 |
| Label from an extra sample not used by any confidence method (the "independent labeling protocol") | Removes dependence between confidence and label; v2 and v3 code implement it, and v4 makes it explicit (`N_LABEL_EXTRA = 1`) | MI 5.4 (v2, v3 AGREE), MI section 11.2 |
| Sampling-agreement confidence (fraction of samples that pass, or agree) | Simple, model-agnostic, consistent across versions | MI 6.2 |
| Several method families compared on the same problems | The comparison itself is the contribution; families span behavior, token probabilities, structure, and stated confidence | MI 6.1 (v2, v3 AGREE) |
| Equal-width ECE, Brier score, and AUROC reported together | Separates calibration from discrimination, which the legacy conclusions depended on | MI 7.1, 7.2, 7.3, 7.6 |
| Cross-validated post-hoc recalibration (isotonic, Platt) as a control | Tests whether a method's failure is a mapping problem or an information problem | MI 6.5 |
| Bootstrap intervals with 1,000 resamples and percentile intervals | Standard and simple; v4 adds a problem-level grouped bootstrap, which is the right unit | MI 8.1, 8.3, section 11.2 |
| Per-test execution with flaky-test discard (canonical solution run twice) | Finer labels and a check on the harness itself | MI section 11.2 (v4 `pertest_harness.py`) |
| Release-date windows for a contamination-resistant benchmark (LiveCodeBench train and evaluation windows) | Basis for a release-date contamination control | MI section 11.2 (v4 `config.py:43-44`) |
| Hidden-state probe as a confidence readout | Lets the study compare internal state with stated confidence directly; designed in v4 but never run, and its quoted numbers have no backing file | MI section 11.2, 11.3 |

### Broken or missing (to be replaced, not repaired)

| Element | Problem | Rows |
|---|---|---|
| Which generation is labeled | v1 text says the deterministic tau = 0.1 generation; code labels the first tau = 0.8 sample | MI 5.4 (v1 DIFFER) |
| Log-probability confidence | Texts give sigmoid(mean log p); code computes exp(mean log p) | MI 6.3 (v2, v3 DIFFER) |
| Which generation each confidence describes | Log-prob from a fresh sample, verbal from a separate unexecuted response, label from another sample; not stated in any text | MI section 12, item 3 |
| AST-agreement confidence | Text describes the largest-cluster share; code uses max(0, 1 - (K - 1)/9) over raw AST dumps | MI 6.6 (v3 DIFFER) |
| Verbal prompts and parsing | Printed prompts are not the code prompts; unparsed answers default silently to 0.6 | MI 3.3 (all DIFFER), MI 6.8 (all ABSENT in text) |
| TACE | floor(sqrt n) equal-count bins, a 0.01 gap filter, and share weighting, unlike the text | MI 7.4 (v3 DIFFER) |
| Stored point estimates | Stored Brier and AUROC are bootstrap means, not point estimates | MI 7.8 |
| SFT evaluation set | The v2 "held-out" set overlaps the training source; v1 tier threshold 0.8 in text, 0.7 in code | MI 1.7, MI 9.7 |
| Reproducibility metadata | No checkpoint revision, precision flags, stop sequences, or decoding settings recorded | MI 2.3, 2.4, 4.5, 4.6, 4.7 |
| Seeds | Generation unseeded in v1 to v3; only bootstrap and splits use seed 42 | MI section 10 |
| Execution details | Timeout scope differs between text and code; MBPP signature handling differs; code extraction undocumented | MI 5.2, 5.7, 5.8 |
| Scope | One benchmark and two models in v3. The second model's pass@1 is zero on HumanEval in its result file; the manuscript attributes this to an instruction-format mismatch with no diagnostic artifact, and a zero pass rate for a 6.7B instruction-tuned code model points to an extraction or harness fault (not verified) | MI 1.1, 2.2, 5.7; `docs/s1/BUNDLE_MAP.md` rows v3-C03, v3-C25 |
| Unbacked artifacts | DPO pairs, trust study, adapters, and other GPU-host outputs are missing | `docs/LEGACY.md` decision 3 |

## (c) TMLR's two acceptance criteria applied to this topic

TMLR reviewers answer two questions (`docs/s2/venue/TMLR_RUBRIC.md` section 2): are the claims
supported by accurate, convincing, and clear evidence, and would some individuals in the TMLR
audience be interested in the findings. Novelty is not required, but incorrect novelty claims are a
stated ground for rejection.

### Claims and evidence

A claim of the form "method A is better calibrated or discriminates better than method B on code
models" is convincingly supported only if the following hold.

1. **Breadth that matches the claim.** Several model families, at least two scales within a family,
   and base and instruction-tuned pairs where the claim concerns tuning. At least three benchmarks
   with different problem styles, including one built from problems released after each model's
   training cutoff.
2. **A verified harness.** Every reference solution passes its own tests in the harness; flaky tests
   are removed; extraction failures are counted and reported separately from wrong code.
3. **Independent labels.** The label comes from a generation that no confidence method used, and
   every confidence states which generation it describes.
4. **Fixed and recorded settings.** Seeds for generation, prompts verbatim in the appendix, parse
   rules and their failure rates, and model revisions pinned.
5. **Uncertainty at the right unit.** Problem-level bootstrap intervals for every metric, and paired
   comparisons between methods on the same problems, with corrections where several comparisons
   back one claim.
6. **Controls for the obvious alternatives.** Recalibration to separate mapping from information;
   prompt-format variation for stated confidence; a release-date split for contamination.
7. **Claims sized to the evidence.** Where a result holds for some families or benchmarks only, the
   claim says so. TMLR's guidance allows reducing claims to close a gap.
8. **Released artifacts.** Code, per-sample outputs, labels, and the analysis JSON behind every
   number, anonymized for review.

### Audience

- Researchers on uncertainty and calibration of language models, for whom code offers exact labels
  that most natural-language tasks lack.
- Researchers on code generation and coding agents, who need to decide when to run tests, sample
  more, or defer to a human.
- Interpretability researchers studying whether hidden states encode correctness that outputs do
  not report.
- Practitioners building verification and routing into code assistants.

## (d) TMLR LLM-use disclosure requirement

From https://jmlr.org/tmlr/faq.html (saved as `docs/s2/venue/sources/faq.txt`, retrieved
2026-11-10, HTTP 200), quoted exactly:

> Q: Can I use ChatGPT or other large language model systems to assist in writing my TMLR
> submission?
>
> A: Yes, but TMLR also considers that it is the authors' responsibility to avoid any unforeseen
> consequences that might come about from using such tools, such as the later discovery that a
> significant part of the submission's content has been plagiarized (in which case we'd have to
> reject the paper). Similarly, our expectation is that the ideas, claims and results found in
> submissions are human-sourced, not produced by such tools.
>
> Additionally, transparency is always good, so we also require that authors mention explicitly in
> their submission that they have used this tool, as a footnote on the first page.

The editorial policy adds, from https://jmlr.org/tmlr/editorial-policies.html (saved as
`docs/s2/venue/sources/editorial-policies.txt`, section "LLM use policy for authors"), quoted
exactly:

> LLMs may be used as general-purpose assistive tools. Whichever tools are used, authors are fully
> responsible for content on which they are listed as (co-) authors. This includes, but is not
> limited to, content generated by LLMs that could be construed as plagiarism or scientific
> misconduct (e.g., fabrication of facts). Low-quality contributions (be they submissions or
> reviews) that appear to be largely LLM-generated will be closely examined for evidence of the
> issues mentioned previously, such as scientific misconduct. LLMs are not eligible for authorship.
> We will periodically revise this policy as new information about the use of LLMs in the
> scientific process becomes available.

The footnote wording is an operator decision (wave 2 report, item 6).
