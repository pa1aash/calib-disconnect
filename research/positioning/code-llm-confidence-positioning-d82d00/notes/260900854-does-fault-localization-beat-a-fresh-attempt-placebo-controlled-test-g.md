---
title: 2609.00854 Does Fault Localization Beat a Fresh Attempt? Placebo-Controlled
  Test-Guided Code Repair (abstract only)
id: 260900854-does-fault-localization-beat-a-fresh-attempt-placebo-controlled-test-g
tags:
- code-llm-confidence-positioning-d82d00
- post-critic-fill
- repair
created: '2026-11-10T09:25:13.699991Z'
source: https://arxiv.org/abs/2609.00854
status: draft
type: note
content_type: paper
deprecated: false
summary: 'ABSTRACT-ONLY: spectrum-based localization plus span infilling loses to
  blind resampling at matched attempts (3:40) on 177 localizable candidates; only
  9.0% of failures localizable; placebo lead suggestive only'
---

ABSTRACT-ONLY. Record from the arXiv export API (https://export.arxiv.org/api/query?id_list=2609.00854), first posted 2026-09-01. Full text not read in wave 4.

## Abstract (verbatim)

Fault localization can focus a code model's repair on the statements a failing test implicates, but a targeted edit may succeed merely because it is small, and a second model call may succeed without using the failure at all. We separate these explanations with three arms applied to the same failed candidate: blind whole-solution resampling, spectrum-based localization followed by suspect-span infilling, and same-length infilling at a disjoint random code span. Across three frozen 26-32B models, three benchmarks and 488 failing candidates, plus a separately declared 24B fourth model from a third family, three results follow. First, localization is rarely available: only 9.0% of failing candidates expose a failing public test with a usable spectrum. Second, among the 177 candidates localizable from a strong suite, localized infilling loses decisively to blind resampling at a matched attempt count (3:40, p = 3.0 x 10^-9), opposite to our hypothesis; the loss replicates in a third family at -11.3 points (95% CI [-16.6, -6.8]), and widening the edit does not rescue it. Third, against the random-span placebo localized infilling leads pooled (11:1, Holm-adjusted p = .019), but that lead resolves in no individual model under the analysis our shipped plan designates primary (best Holm p = .087), so we report the location effect as suggestive rather than established. Re-pricing attempts as tokens narrows but does not overturn this: a span attempt spends 21.7 generated tokens against 371.1, yet 16 localized attempts reach 6.8% while one blind attempt already reaches 10.1%. Infilling reproduces the removed span verbatim in 48.9% of attempts, which is why more budget does not help. We restrict every localization conclusion to the 24-32B models tested.
