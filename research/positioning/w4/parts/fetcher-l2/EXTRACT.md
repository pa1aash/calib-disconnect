# EXTRACT: Ribeiro, Spiess, Devanbu, Nadi, "On LLMs' Internal Representation of Code Correctness"

Retrieved 2026-11-10 (all fetches HTTP 200 unless noted). Quotations are verbatim from raw/2512.07404.txt (pdftotext of arXiv v3, 21 Jan 2026). Table cells were checked against `pdftotext -layout` of page 7-8. Section numbers are as printed or inferred from the text; unnumbered ones are marked.

## 0. Identity (fetched records)

| Field | Value | Source |
|---|---|---|
| Title (v2, v3) | On LLMs' Internal Representation of Code Correctness | arXiv API raw/arxiv_search.xml; abs.html |
| Title (v1) | Do LLMs Trust the Code They Write? | raw/2512.07404v1.txt first page |
| Authors | Francisco Ribeiro, Claudio Spiess, Prem Devanbu, Sarah Nadi (matches vault claim) | arXiv API |
| arXiv id | 2512.07404; v1 published 2025-12-08; v2 dated 5 Jan 2026; v3 dated 21 Jan 2026 (latest, fetched) | PDF stamps; API `updated` 2026-01-21 |
| Category | cs.SE | PDF stamp |
| Venue | Proceedings of the 2026 IEEE/ACM 48th International Conference on Software Engineering (ICSE 2026), pp. 1160-1172, issued 2026-04-12, proceedings-article, ACM | raw/crossref.json |
| DOI | 10.1145/3744916.3787846 (ACM); arXiv DOI 10.48550/arXiv.2512.07404 | Crossref, S2, OpenAlex |
| Record URLs | https://arxiv.org/abs/2512.07404 ; https://doi.org/10.1145/3744916.3787846 ; S2 paper id cf670e59946d1d18663f51aabd1c8b054771d029 ; OpenAlex W7113916628 | |
| Artifact | "https://github.com/sanadlab/code-repe" (PDF line ~148, reference [5]) | PDF text |

Vault claim check: title, authors, and "ICSE 2026" match. Notes: (a) the v1 title differed ("Do LLMs Trust the Code They Write?"); (b) the v3 PDF text contains no explicit "ICSE 2026" statement (header reads "Conference'17, July 2017, Washington, DC, USA", the ACM template placeholder); the ICSE 2026 venue comes from Crossref/S2/OpenAlex records; (c) OpenAlex labels the source as "ACM/IEEE International Conference on Software Engineering: Companion Proceedings (ICSE-Companion)" while Crossref's container title is the main ICSE 2026 proceedings, a metadata discrepancy not resolved here; (d) DBLP could not be queried (HTTP 202 Anubis proof-of-work page; recorded as a gap, raw/dblp.json holds the challenge page). The vault note is research/notes/251207404-on-llms-internal-representation-of-code-correctness.md (source https://arxiv.org/abs/2512.07404, fetched 2026-07-20 per its frontmatter, status draft, tier institutional); its summary says ICSE 2026 accepted and states the whole-solution, prompted-verbalization framing. The vault report research/notes/final_report_code-llm-probe-verbalize-gap-3d8995.md names it "ICSE'26, accepted" and says "whole-solution granularity only; zero-shot *prompted* verbalization (not trained)". Both claims are consistent with the full text (sections below), with the nuance that the paper's task is selection among candidates, not a per-solution calibrated probability.

Related follow-up (same group, found in the arXiv title search): "On the Robustness of LLMs' Internal Representation of Code Correctness", arXiv 2608.08266v1 (2026-08-08), authors Francisco Ribeiro, Sohaila Abdulsattar, Renata Gonzalez, Mahmoud Kassem, Sarah Nadi. See CITING.md.

## 1. Models (Section 4.1.4)

> "Mistral-7B-Instruct-v0.3, Qwen2.5-Coder-7B-Instruct, OpenCoder-8B-Instruct, and CodeLlama-7B-Instruct. From now on, we refer to these using the short forms Mistral, Qwen, OpenCoder, and CodeLlama, respectively. Our selection criteria were: (1) Open-source: required for extracting internal activations. (2) Consistency: Mistral was used in the original RepE work. (3) Comparable: models have 7-8B parameters ... (4) Code: Besides Mistral, we used three code-specialized models..."

All four are instruct variants of 7-8B parameters. Base-vs-instruct comparison: not present in full text (searched for: "base model", "Instruct", "base vs"; the only "base model" hit is RankEF's CodeT5+). Reasoning models: not present in full text (searched for: "reasoning model"; only hit is a citation "in line with similar observations in reasoning models [84]" in the Discussion). Models used only to produce incorrect candidates: Llama-3.3-70B, GPT-4o, Gemini 2.0 Flash (BigCodeBench pre-generated), Llama-3.2-3B, Gemma-3-1B, Granite-3.3-2B (HumanEval), GPT-4 failed attempts from EvalPlus (MBPP+ fit set), Llama-3.2-11B-Vision-Instruct (synthetic fit set) (Section 4.1.1-4.1.2).

## 2. Benchmarks

> "We focus on two datasets, HumanEval [16] and BigCodeBench [90] ... Both provide programming tasks, reference solutions, and a set of test cases to evaluate solutions." (Section 4.1.1)

Table 1: MBPP+ v0.2.0 378 tasks; HumanEval 164 tasks; BigCodeBench 1,140 tasks. QA_BCB = 457 tasks (all three incorrect-source models failed); QA_HE = 151 tasks ("at least three incorrect attempts from the total pool of 30 attempts per task"). MBPP+ (97 tasks with correct and incorrect solutions) and a synthetic set (20 tasks) are used only as out-of-distribution fit/validation data (Section 4.1.2).

## 3. Correctness labels (Section 3)

> "In this work, we define code correctness as adherence to a given problem specification, which can be verified through test execution" (Section 1)

> "Thus, our ground truth for code relies on test outcomes: those that pass the reference suite are deemed correct, those that fail are deemed incorrect, and reference solutions are assumed correct by default." (Section 3)

Execution against the benchmark test suites; binary pass/fail on the whole reference suite. RQ2: "correct(.) indicates whether the implementation passes all unit tests" (Section 5.1.3).

## 4. Methods

Probe type (Section 2.1, 3): Representation Engineering / Linear Artificial Tomography (LAT), unsupervised PCA, not a trained classifier.

> "General Pipeline RepE follows a three-phase pipeline: 1) Fitting: for each layer, collect hidden states from positive and negative stimuli, compute and normalize difference vectors, and fit a PCA to extract the principal direction that best separates the two classes 2) Validation: project held-out data onto each layer's principal component and select the layer with the highest accuracy at distinguishing positive and negative stimuli 3) Testing: using the chosen layer, score new instances on a test set and record accuracy."

Contrastive direction (Section 3): "we extract the model's hidden states at the final token for each layer ... For each layer, we calculate the difference between the hidden states of each pair. Next, we normalize these difference vectors by calculating their mean and subtracting it from each vector ... Finally, we apply PCA ... " Section 2.1: "only the first principal component (a vector) for each layer is used." Sign assigned by correlation with concept labels. Pairs are same-task correct vs incorrect: "we construct pairs of code snippets, one correct and one incorrect, without explicit labels in the stimuli."

Layers: every layer is fitted; one layer chosen per fold by validation accuracy. "LAT (Val) uses the layer selected by the validation sets (realistic performance), while LAT (Best) selects the optimal layer based on the Test set (theoretical upper bound)." (Section 4.1.2). Specific selected layer indices: not present in full text (searched for: "layer" in results).

Evaluation prompt (Listing 1 and Listing 6):
```
Consider the amount of correctness in the following:
Task: <task>
Code:
```python
<code>
```
The amount of correctness is
```
Score = dot product of last-token hidden state with the layer's vector (Section 3); "While this score alone does not directly classify correctness, it enables comparison among several candidate solutions."

Log-likelihood baseline (Section 2.3, "Intrinsic"): "Length-normalized sequence likelihood: sums the token-level log-probabilities and normalizes by sequence length".

Verbalized confidence ("Reflective", Section 2.3, Figure 3):
> "Reflective: elicit a verbal confidence rating, asking the LLM to score its certainty on a fixed scale. These ratings are then combined with token probabilities. We consider two variants: Regular: Seven verbalized levels ("Very low" to "Very high"), mapped to a numeric scale (evenly spaced from -1 to 1) and weighted by the model's joint probability of generating the tokens corresponding to the verbalized confidence ... True/False (T/F): A binary confidence asking whether the candidate is correct (True or False), scored according to the model's assigned probability to True"

Figure 3 prompt text (extracted): Regular: "What is the amount of <concept> of the following scenario? Please answer using EXACTLY one of the following: Very low ... Very high / Task: <programming task> / Code: ```python <implementation>```", score "Sum of log-likelihood of <pre-filled choice>"; T/F: "Does the following code exhibit <concept>? Please answer with True or False. / Task: ... Code: ...  True", score "Sum of log-likelihood of True". The extraction shows only "Very low ... Very high"; the intermediate five level names are not printed in the figure. Format: categorical (7-level ordinal and binary), mapped to numeric, probability-weighted; prompted zero-shot, not trained (no fine-tuning of the verbalizer anywhere; the only trained baseline is RankEF).

Task format (Section 4.1.1-4.1.3): multiple-choice selection (1 correct + 3 incorrect), accuracy = proportion of tasks where the top-scored candidate is the correct one. RQ2 (Section 5): rank 10 self-generated samples (temperature 1.0) by score, pass@rank-k, k = 1..5; baseline RankEF (CodeT5+ trained on execution feedback).

## 5. Main results

Table 3 (BigCodeBench, TestBCB; accuracy, mean ± std over 10 folds). Columns: Standard (log-likelihood), Regular, T/F, LAT (Val) FitBCB / FitMBPP+ / FitSyn, LAT (Best) FitBCB / FitMBPP+ / FitSyn. A stray "27.5%" sits in the Random column (extraction shows no per-row Random value).

| Model | Standard | Regular | T/F | LAT Val FitBCB | Val FitMBPP+ | Val FitSyn | Best FitBCB | Best FitMBPP+ | Best FitSyn |
|---|---|---|---|---|---|---|---|---|---|
| Mistral | 5.7% ± 0.4 | 28.9% ± 0.8 | 23.7% ± 0.0 | 51.1% ± 10.6* | 47.8% ± 0.8* | 33.0% ± 0.1* | 57.9% ± 4.5 | 59.3% ± 0.9 | 48.4% ± 0.5 |
| Qwen | 5.0% ± 0.3 | 38.0% ± 0.7 | 41.1% ± 0.8 | 54.4% ± 3.8* | 40.2% ± 0.9 | 12.2% ± 0.8 | 57.1% ± 2.7 | 55.7% ± 0.7 | 39.4% ± 0.5 |
| CodeLlama | 4.8% ± 0.4 | 24.7% ± 0.4 | 23.7% ± 0.0 | 50.3% ± 6.2* | 25.8% ± 0.3 | 22.2% ± 0.7 | 55.0% ± 3.0 | 48.2% ± 0.9 | 39.0% ± 0.7 |
| OpenCoder | 6.4% ± 0.4 | 24.5% ± 1.3 | 27.3% ± 0.5 | 56.3% ± 5.1* | 29.5% ± 0.3 | 30.5% ± 0.7 | 60.0% ± 2.8 | 44.2% ± 0.7 | 44.2% ± 1.2 |

Table 4 (HumanEval, TestHE). A stray "30.6%" sits in the Random column.

| Model | Standard | Regular | T/F | LAT Val FitHE | Val FitMBPP+ | Val FitSyn | Best FitHE | Best FitMBPP+ | Best FitSyn |
|---|---|---|---|---|---|---|---|---|---|
| Mistral | 21.3% ± 3.3 | 40.6% ± 2.7 | 15.3% ± 2.7 | 49.3% ± 7.0* | 39.9% ± 2.2 | 38.1% ± 1.4 | 53.8% ± 7.2 | 58.4% ± 1.2 | 47.6% ± 1.7 |
| Qwen | 36.8% ± 3.1 | 7.0% ± 1.1 | 6.7% ± 0.9 | 60.7% ± 8.3* | 39.6% ± 1.3 | 63.0% ± 2.0* | 67.8% ± 4.6 | 65.6% ± 1.8 | 65.2% ± 1.9 |
| CodeLlama | 21.3% ± 2.5 | 28.9% ± 2.1 | 26.5% ± 0.0 | 41.4% ± 6.4* | 32.2% ± 1.0 | 25.5% ± 1.3 | 52.7% ± 4.5 | 49.6% ± 2.1 | 46.7% ± 1.5 |
| OpenCoder | 36.5% ± 3.9 | 31.0% ± 2.5 | 9.9% ± 1.6 | 44.0% ± 8.3* | 35.1% ± 1.8 | 47.8% ± 3.0* | 56.5% ± 3.1 | 52.4% ± 2.8 | 56.6% ± 3.9 |

Text (Section 4.2.1): "Third and most importantly, LAT consistently outperforms all baselines. On BigCodeBench, it improves accuracy by +13.3 to +29.0 pp over the best reflective accuracy; on HumanEval, gains range from +8.7 to +26.2 pp over the strongest baseline." The RQ1 takeaway box says "+13.3 to +28.8 pp" (internal inconsistency in the paper; also Section 4.2.3 says OpenCoder baseline "27.5%" while Table 3 shows 27.3%). Section 4.2.1: "the intrinsic (standard) metric on BigCodeBench hovers around 5-6% for all models, whereas on HumanEval it ranges from 21%-37%"; "reflective variants are inconsistent". Metric is selection accuracy, not AUROC or ECE (searched for: "AUROC", "AUC", "ECE", "calibration error": none in the results; only "calibrat" in related work).

Table 5 (HumanEval pass@rank-1, RankEF comparison; row order Random, Intrinsic, Regular, T/F, FitHE, FitMBPP, FitSyn, RankEF, as printed): Mistral 38.0, 33.9, 26.4, 33.9, 41.3, 35.5, 41.3, 35.5; Qwen 64.5, 80.2, 24.8, 26.4, 85.1, 28.1, 85.1, 81.0; CodeLlama 35.5, 39.7, 31.4, 30.6, 35.5, 30.6, 31.4, 34.7; OpenCoder 76.9, 76.0, 64.5, 63.6, 63.6, 70.2, 80.2, 75.2 (column assignment inferred from header order and checked against the text values 41.3, 85.1, 80.2, 39.7, 35.5 RankEF). Table 6 (BigCodeBench pass@rank-1) values quoted in text: Mistral FitSyn 5.7%, Qwen FitMBPP 7.1%, OpenCoder FitSyn 8.4%, RankEF Mistral 4.1%, Qwen 6.0%, CodeLlama 3.3% (Section 5.2.3). Text: "Across all models, the Reflective ranking methods consistently underperform, often doing worse than Random." (Section 5.2.2).

## 6. Granularity

Whole solution. Each candidate program gets one score; ground truth is one pass/fail on the entire test suite. Per-test / per-requirement / per-line labels: not present in full text (searched for: "per-test", "per test", "line-level", "requirement"). Related work contrasts: "Bui et al. [13] also use LLM internal states for code correctness, but classify single programs, while we rank candidates." and "Huang et al. [30] use internal states for line-level risk assessment".

## 7. Elicitation-format variation

Two verbalized formats are compared (Regular 7-level vs True/False), see Section 4.2.1: "on BigCodeBench, the true/false variant outperforms the regular variant for Qwen (41.1% vs. 38.0%) but underperforms for Mistral (23.7% vs. 28.9%). In contrast, on HumanEval, Mistral's reflective regular accuracy (40.6%) exceeds its true/false accuracy (15.3%), while Qwen scores around 7% on both." No other prompt-wording ablation: not present in full text (searched for: "paraphrase", "prompt variation", "ablation").

## 8. Limitations and future work (Discussion, Threats to Validity; section numbers unprinted in extraction)

> "In this work, we showed that this signal exists and can be leveraged but not why or how it exists. Is the model learning a deep semantic understanding of the code's logic? Or is it learning more superficial pattern recognition ... It would be interesting to explore this distinction in future work."

> "future work could explore whether LAT can also capture other non-functional properties such as maintainability or efficiency"

> "Internal Validity. Prompt formatting choices or verbalized confidence levels could influence our observations."

> "External Validity. We evaluate the accuracy of four 7-8B parameter LLMs on two Python benchmarks (HumanEval and BigCodeBench) ... the observed LAT effectiveness and ranking improvements may not hold for larger or smaller models, different architectures, or other programming languages. Our single-function evaluation does not cover some aspects of real-world code, e.g., multi-file projects or integration tests ... We plan to explore such settings as future work."

Other: "our approach is model-specific (representations captured from one LLM cannot be applied to another's hidden states)"; "Our technique requires extracting hidden states during generation, resulting in higher per-task inference time (0.399s vs. RankEF's 0.202s)"; "Since our approach captures relative correctness, it is best suited for comparing code changes." Calibrated absolute probabilities (no AUROC/ECE), training the model to verbalize, and downstream targeted repair: not present for the paper's own method (searched for: "fine-tun", "repair", "AUROC", "per-test", "requirement"; the only hits are RankEF "full fine-tune procedure", and Huang et al. "code repair" as related work).
