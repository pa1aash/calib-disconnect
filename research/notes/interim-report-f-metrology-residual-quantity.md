---
title: Interim report — f-metrology-residual-quantity
id: interim-report-f-metrology-residual-quantity
tags:
- code-llm-confidence-positioning-d82d00
- locus-f-metrology-residual-quantity
created: '2026-11-10T08:41:01.504633Z'
status: draft
type: interim
deprecated: false
summary: 'F is OCCUPIED as framing: bias, resolution-vs-internal-reference, and cross-format
  noise all map to Yates/Murphy/grouping-loss/Spearman quantities; meta-d'' undefined
  for open-ended code; use as exposition only'
---

# Interim report: f-metrology-residual-quantity

**Locus question:** Whether a measurement-instrument framing yields a quantity beyond Murphy decomposition and meta-d', and whether the framing is unused, used, or contested; decides F.
**Flavor:** synthesis (convergent)

## What the corpus already said

The width sweep found three families of neighbors. (1) Psychometric/SDT readings of LLM confidence outside code: [[do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec]] (Cacioli), [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]], [[measuring-some-aspects-of-the-metacognition-of-ai]] (Servajean and Servajean), [[the-metacognitive-monitoring-battery-a-cross-domain-benchmark-for-llm-self-monit]]. (2) A pre-registered three-channel audit using "measurement validity" and Murphy resolution, [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]]. (3) Proper-score decompositions: [[260305544-yates-covariance-decomposition-rearrangement-for-brier-score-full-text]], [[decomposing-probabilistic-scores-reliability-information-loss-and-uncertaintysup]]. Formal metrology papers ([[uncertainty-evaluation-bridging-machine-learning-and-measurement-science-full-te]], [[a-metrological-framework-for-uncertainty-evaluation-in-machine-learning-classifi]]) never treat LLM confidence. No note mapped each candidate quantity (readout bias, resolution against an internal reference, cross-format noise) to its nearest existing quantity. That mapping is the work here. All eleven notes below were read as full text except where marked.

## What the new sources say

Fetch budget: 3 (two new notes created; one duplicate URL reused). Extra primary-source chase used: 1 (Mahaut).

**[[factual-confidence-of-llms-on-reliability-and-robustness-of-current-estimators]]** (Mahaut et al., arXiv 2406.13415, full text HTML; the "closest prior" named by 2610.25846 Section 2). Section "Robustness to Linguistic Variations": "if a method is robust, it should produce equally reliable estimates (equally high AUPRC scores) across different input formulations"; AUPRC "remains stable for all methods (absolute variation between 5% and 10%)", yet per-fact confidence changes under 8 paraphrases per input, which the authors read as "excessive sensitivity to how a claim is worded". Factual QA only, no code, no execution labels, no hidden-state-versus-verbal gap decomposition. This occupies the cross-format/prompt noise quantity in general NLP, as a stability statistic.

**[[language-models-are-capable-of-metacognitive-monitoring-and-control-of-their-int]]** (Ji-An et al., arXiv 2505.13763, full text HTML; abstract and Appendix "Quantifying reporting accuracy", "Control precision"). Literal measurand-readout paradigm: a model reports a direction of its own activations given in-context neurofeedback; reporting accuracy and cross-entropy rise with in-context examples; the reportable "metacognitive space" is far lower-dimensional than the neural space. It treats the internal activation axis as the reference and the verbal report as the readout, with precision and signal-to-noise terms. It concerns reporting activation labels, not confidence in correctness, and not code. Fetched under the budget as the nearest "internal reference" work; it was not cited by a CLOSE item, so I count it as a budget fetch, not a chase.

**[[measuring-some-aspects-of-the-metacognition-of-ai]]** (reused, 13.9k words, full text). Abstract: common AUROC-style metacognitive sensitivity is "confounded by type 1 task performance"; advocates meta-d'/M-ratio and SDT criterion shifts, on GPT-5, DeepSeek-V3.2-Exp, Mistral-Medium-2508, three non-code tasks (SST-2 valence, oral versus written, deleted "the"). States "strictly instrumental and outcome-oriented". Requires a two-alternative type-1 task.

## Evidence synthesis

Mapping the three candidate F quantities onto the nearest existing quantity:

| F candidate | Nearest existing quantity | Where | Computable from existing? |
|---|---|---|---|
| Readout bias | Calibration-in-the-large (mu_F - mu_Y) in the Yates covariance decomposition (Vieira note, Section 1.3, BS = Var(F-Y) + (mu_F-mu_Y)^2); SDT criterion c (Cacioli, signal-detectors; Servajean type-1 criterion) | 260305544; 2603.14893 | Yes |
| Readout resolution relative to an internal reference | Murphy resolution Var(E[Y|F]) of each readout, differenced across readouts (2610.25846, Section 6.1: behavioral 0.06371 vs verbal 0.03160 vs probe 0.05154, a 2.02x ratio); Charpentier and Fernandes Machado "grouping" term E[d(C,Q)], the information lost mapping features X to score S, which post-hoc recalibration cannot fix (Section 5 text and decomposition identity; recalibration "leaves grouping essentially unchanged") | 2610.25846; 2603.15232 | Yes; reference-conditioned version is grouping loss with the probe or a high-capacity model as reference |
| Cross-format readout noise | Pairwise Spearman across three verbal formats 0.126, -0.069, 0.247 against a 0.60 gate (2610.25846, Gate 2 and Section 5); AUPRC variation 5-10% and per-fact paraphrase sensitivity (Mahaut, Robustness section) | 2610.25846; 2406.13415 | Not from Murphy, but already reported as a statistic |
| Metacognitive efficiency | meta-d'/M-ratio (Servajean); model-free meta-I = I(correct;confidence)/H(correct) after Cacioli v3 retracts M-ratio as ill-defined for open-ended QA and reverses its v1/v2 coupling finding after a length-biased scorer (agreement with human labels 0.76 to 0.86) | 2603.29693; 2603.25112 | Yes |

Three points follow. First, vocabulary: "measurand" appears only in the two formal metrology papers, and "instrument" in a reactivity argument in [[dont-ask-understanding-what-numeric-self-reports-measure-in-language-models]] ("Numeric self-report has been a primary instrument for internal states", with the finding that the rating question displaces the probed state). The LLM-confidence literature has already adopted "measurement validity" (2610.25846), "measurement framework" (2603.14893, "SDT is applied here as a measurement framework for decomposing performance"), and psychometric batteries (2604.15702). So the framing is USED in general NLP in everything except metrology-proper terms (GUM uncertainty budget, traceability), which are unused for LLM confidence (Petri and Mari explicitly exclude generative ML; no experiments). Second, the "internal reference" idea has a circularity that blocks it as a new quantity. In the code setting the probe is trained on the same execution labels it is meant to referee, so a probe-referenced resolution is Murphy resolution of the probe minus Murphy resolution of the readout, or a conditional mutual information I(Y; verbal | probe). Both are functions of joint distributions the existing decompositions already cover. Third, the one quantity the Murphy and covariance decompositions truly cannot produce is a cross-format variance component (item x format variance), but that is exactly what 2610.25846 and Mahaut already measure (as rank correlations and AUPRC spread) and what generalizability theory would formalize. Nothing found defines it for code.

Caveat on meta-d': it needs a binary type-1 decision with a latent evidence variable. Code generation has no S1/S2 choice, so M-ratio is undefined (Cacioli's own retraction logic). An F paper cannot "beat" meta-d' on code; it would simply use the model-free meta-I that Cacioli already defined. This weakens A9's request that the decomposition "differ from" meta-d' (it differs by non-applicability, not by adding content).

Instrument gaps: arXiv metadata search returned HTTP 429 on the id_list call and returned no hit for abs:"measurand" plus language model; OpenAlex budget was exhausted; no Murphy 1973, Yates 1982, Fleming and Lau 2014, or Maniscalco and Lau 2012 full text (pre-2022 foundations, not on allowed hosts). Negatives on "no LLM-calibration paper uses a measurand/readout decomposition" are therefore CLEAN (provisional) at most.

## Committed position

F is not a contribution; it is a vocabulary choice for a paper whose evidence lives in L1 and L2. Every quantity the framing proposes maps onto an existing one: readout bias is the Yates (mu_F - mu_Y)^2 term or SDT criterion c, readout resolution against an internal reference is the difference of Murphy resolutions (or the Charpentier grouping term with the probe as reference), and cross-format noise is already reported as pairwise Spearman 0.126/-0.069/0.247 by Ghosh et al. and as AUPRC spread by Mahaut et al. The only quantity outside Murphy is a format-by-item variance component, and it is occupied as a statistic in general NLP with no code-specific reason for a different result (A21 condition 2 fails). The load-bearing reason: the internal reference is a probe trained on the same execution labels, so any "relative to internal state" quantity collapses to a contrast of two ordinary resolutions. Use "readout" and "measurand" as exposition inside L2, report the Murphy terms and meta-I (not meta-d', which is undefined for open-ended code), and do not claim novelty for the lens.

- **Position:** F is OCCUPIED as a framing and yields no quantity beyond Murphy, Yates, grouping loss, and meta-I; adopt it as exposition only, never as a headline contribution (fails pivot criterion 3 on both counts: not unused, no new quantity).
- **Confidence:** medium-high (about 75%). Seven full-text papers read; the argument is a mapping, so it is checkable; the unread foundations and unsearchable body text are the weak point.
- **Boundary conditions:** Holds for the three candidate quantities as defined in R1 F question 3 (bias, resolution against an internal reference, cross-format noise) and a probe-trained-on-execution-labels reference. A different, label-free internal reference (for example an unsupervised truthfulness direction, or a causal-intervention-defined readout as in Ji-An et al.) could define a genuinely new quantity; none was found for confidence in correctness.
- **What would change this position:** a fetched paper that defines a readout-error quantity against an observed internal state that is not a function of (probe score, verbal score, outcome), or that shows by cross-format variance decomposition on code a result that differs from the general-NLP finding with a stated mechanism. A full-text hit for "measurand" with LLM confidence would also move F from CLEAN (provisional) toward OCCUPIED on vocabulary.
- **Evidence weight:** 7 full-text papers support the mapping (2610.25846, 2603.14893, 2603.25112, 2603.29693, 2603.05544, 2603.15232, 2406.13415); 2 formal-metrology papers are classification-only and out-of-scope for generative models (2504.03359, 2610.18066); 1 (Ji-An) is adjacent and leaves a small opening; 0 are code papers.

### Provisional verdicts per R1 F component
- **F Q1 (metrology vocabulary used for LLM confidence):** OCCUPIED in "measurement validity", "measurement framework", and psychometric terms (2610.25846, 2603.14893, 2604.15702); metrology-proper terms (GUM, traceability, uncertainty budget) CLEAN (provisional) for LLM confidence, gaps: arXiv full-text search failed, OpenAlex full text partial, Semantic Scholar keyword search rate-limited.
- **F Q2 (bias/resolution/noise decomposition vs. Brier calibration-refinement):** OCCUPIED (union): Yates 3-term decomposition (bias, variance mismatch, correlation deficit) plus Charpentier reliability/grouping/uncertainty plus Ghosh cross-format Spearman cover every dimension; closest on each side: Vieira (2603.05544) and Ghosh et al. (2610.25846).
- **F Q3 (A24 residual quantity):** NARROW at best; stated residual: a format-by-item variance component of verbal confidence on execution-graded code. Closest work on each side: Mahaut et al. 2406.13415 (paraphrase stability, factual QA) and Ghosh et al. 2610.25846 (three-format Spearman). It fails the A21 test (no stated reason code would differ), so the effective verdict is OCCUPIED.
- **F Q4 (A9 meta-d'):** OCCUPIED (Servajean 2603.29693; Cacioli 2603.25112 v3; 2603.14893), with the added fact that M-ratio is undefined for open-ended generation.
- **Whole F:** OCCUPIED; fallback role under R1 section 6 item 3 is not met.

## Open questions
- Whether Perez-Lebel et al. grouping-loss estimators (cited in Charpentier) have been applied to an LLM readout against hidden states; not searched.
- Whether any work reports a format-by-item variance decomposition (ICC or generalizability study) for LLM verbal confidence; negative rests on gapped instruments.
- Ghosh et al. Section 5 formats are factual/math QA; verbal format instability on code is untested in any fetched work (a possible L2 factor, not an F quantity).
- Ribeiro et al. and its citers were not re-read for measurement vocabulary.

## Sources
1. [[measurement-validity-and-representation-dynamics-ofconfidence-signals-in-large-l]] Ghosh, Kumar, Garg, arXiv 2610.25846
2. [[do-llms-know-what-they-know-measuring-metacognitive-efficiency-with-signal-detec]] Cacioli, arXiv 2603.25112 v3
3. [[llms-as-signal-detectors-sensitivity-bias-and-the-temperaturecriterion-analogy]] arXiv 2603.14893
4. [[measuring-some-aspects-of-the-metacognition-of-ai]] Servajean and Servajean, arXiv 2603.29693 v4
5. [[260305544-yates-covariance-decomposition-rearrangement-for-brier-score-full-text]] Vieira, arXiv 2603.05544
6. [[decomposing-probabilistic-scores-reliability-information-loss-and-uncertaintysup]] Charpentier and Fernandes Machado, arXiv 2603.15232
7. [[factual-confidence-of-llms-on-reliability-and-robustness-of-current-estimators]] Mahaut et al., arXiv 2406.13415 (new)
8. [[language-models-are-capable-of-metacognitive-monitoring-and-control-of-their-int]] Ji-An et al., arXiv 2505.13763 (new)
9. [[dont-ask-understanding-what-numeric-self-reports-measure-in-language-models]] arXiv 2603.18893
10. [[uncertainty-evaluation-bridging-machine-learning-and-measurement-science-full-te]] and [[261018066-uncertainty-evaluation-bridging-machine-learning-and-measurement-scien]] Petri and Mari, arXiv 2610.18066
11. [[a-metrological-framework-for-uncertainty-evaluation-in-machine-learning-classifi]] arXiv 2504.03359
12. [[the-metacognitive-monitoring-battery-a-cross-domain-benchmark-for-llm-self-monit]] arXiv 2604.15702
