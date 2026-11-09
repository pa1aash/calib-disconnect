# L2 occupant priority check

Wave 4, 2026-11-10. This file checks the code-model occupant for L2 claimed by an earlier vault
report. All quotations come from full texts fetched in this wave. The raw texts and the retrieval
logs are in `parts/fetcher-l2/` (`EXTRACT.md`, `CITING.md`, `raw/`).

## 1. The claim being checked

The earlier vault report (`research/notes/final_report_code-llm-probe-verbalize-gap-3d8995.md`,
section 1, July 2026) states:

> "It is ALREADY demonstrated on code: Ribeiro, Spiess, Devanbu, Nadi, 'On LLMs' Internal
> Representation of Code Correctness' (ICSE'26, accepted). A contrastive hidden-state direction
> beats BOTH log-likelihood AND the model's verbalized confidence on 4 code LLMs. This is the
> single closest prior work. But: whole-solution granularity only; zero-shot prompted
> verbalization (not trained)."

The quotation is lightly normalized: bold markers are removed and the em-dash is replaced with a
colon.

## 2. Identity (fetched records)

| Field | Value | Record |
|---|---|---|
| Title | On LLMs' Internal Representation of Code Correctness (v1 title: "Do LLMs Trust the Code They Write?") | https://arxiv.org/abs/2512.07404 |
| Authors | Francisco Ribeiro, Claudio Spiess, Prem Devanbu, Sarah Nadi | arXiv API |
| Versions | v1 2025-12-08, v2 2026-01-05, v3 2026-01-21 (fetched and used) | arXiv |
| Venue | ICSE 2026 (IEEE/ACM 48th International Conference on Software Engineering), pp. 1160-1172 | https://doi.org/10.1145/3744916.3787846 (Crossref) |
| Artifact | https://github.com/sanadlab/code-repe (named in the paper) | PDF text |

The venue comes from Crossref, Semantic Scholar, and OpenAlex. The v3 PDF still carries the ACM
template placeholder header. OpenAlex labels the source "ICSE-Companion", but Crossref gives the
main proceedings. That discrepancy is unresolved and does not affect the verdicts. DBLP was
unreachable because it returned HTTP 202 with a proof-of-work page (instrument gap).

**Verdict on the claim:** confirmed. The title, authors, and venue match, and so does the
characterization: whole-solution granularity, with prompted, untrained verbal confidence. The vault
report omitted one nuance. The paper's task is selection among candidate programs, not a per-solution
calibrated probability.

## 3. What the paper did

- **Models (Section 4.1.4).** "Mistral-7B-Instruct-v0.3, Qwen2.5-Coder-7B-Instruct,
  OpenCoder-8B-Instruct, and CodeLlama-7B-Instruct." All four are instruct models of 7 to 8B. Other
  models only generate incorrect candidates.
- **Benchmarks (Section 4.1.1, Table 1).** Evaluation is on HumanEval (QA_HE, 151 tasks) and
  BigCodeBench (QA_BCB, 457 tasks). MBPP+ and a 20-task synthetic set are fit data only.
- **Labels (Section 3).** "those that pass the reference suite are deemed correct, those that fail
  are deemed incorrect." The label is binary execution on the whole test suite.
- **Probe (Sections 2.1 and 3).** Representation Engineering LAT: an unsupervised PCA direction over
  normalized difference vectors of hidden states from correct and incorrect pairs on the same task,
  read at the final token. The layer is chosen on validation data, and "LAT (Best)" is reported
  separately as a test-selected upper bound.
- **Readouts compared (Section 2.3).**
  - "Standard": length-normalized sequence likelihood.
  - "Regular": seven verbal levels, "Very low" to "Very high", mapped to [-1, 1] and weighted by
    token probability.
  - "True/False": the probability of "True".
  - Both verbal variants are prompted zero-shot. Nothing is trained.
- **Task and metrics.**
  - RQ1 is multiple-choice selection: one correct and three incorrect candidates, scored by accuracy.
  - RQ2 ranks 10 self-generated samples (temperature 1.0) by pass@rank-k, against RankEF.
  - The paper reports no AUROC, ECE, or Brier score (searched for: "AUROC", "AUC", "ECE",
    "calibration error").
- **Finding (Section 4.2.1).** "LAT consistently outperforms all baselines. On BigCodeBench, it
  improves accuracy by +13.3 to +29.0 pp over the best reflective accuracy; on HumanEval, gains range
  from +8.7 to +26.2 pp over the strongest baseline." The takeaway box says "+13.3 to +28.8 pp", an
  internal inconsistency in the paper. The paper also says (Section 5.2.2): "Across all models, the
  Reflective ranking methods consistently underperform, often doing worse than Random."
- **Elicitation format (Section 4.2.1).** The paper compares two verbal formats and calls them
  inconsistent. For example, on HumanEval, Mistral scores 40.6% with Regular and 15.3% with
  True/False. It runs no other prompt ablation.
- **Limitations it states (Discussion, Threats).**
  - It does not explain why the signal exists.
  - Results are for 7 to 8B models and two Python benchmarks only.
  - "Prompt formatting choices or verbalized confidence levels could influence our observations."
  - The approach captures "relative correctness" and is model-specific.

## 4. Point-by-point overlap with L2

L2 (brief, section 1): comparing hidden-state probes with verbal and sampled readouts, across base
and instruct pairs, reasoning and non-reasoning models, and elicitation formats, locates where
correctness information is lost between internal state and output.

| L2 component | Ribeiro et al. 2026 | Closest citing work (section 5) | Verdict (provisional, before Step 4) |
|---|---|---|---|
| Probe versus verbal readout, code, execution labels | Yes: LAT direction versus 7-level and True/False verbal readouts, 4 instruct models, 2 benchmarks; probe wins everywhere (Section 4.2.1) | 2608.08266 (same group) varies the extraction; 2611.07876 compares probes with output (verdict-token) confidence in AUROC | **OCCUPIED** at whole-solution granularity, as a qualitative claim (probe beats stated confidence) |
| Probe versus sampled readouts (sampling agreement) | No sampling-agreement readout; log-likelihood only | 2611.07876 includes a sampled-solutions family (EigenScore) with hidden-state probes and output confidence on Qwen3-Coder-30B and gpt-oss-20b (Section IV, Table II) | **NARROW**: a three-family comparison exists on two models; the residual is a matched comparison of probe, verbal, and sampling-agreement readouts on the same generations with calibration metrics |
| Calibration-grade metrics (AUROC, ECE, Brier) for probe versus verbal | No; selection accuracy and pass@rank only | 2611.07876 reports AUROC for probe versus output confidence, but not for verbal numeric confidence | **NARROW** |
| Base versus instruct pairs | Not present (all instruct; searched for: "base model", "base vs") | Not present in any citing full text fetched (all instruct) | **CLEAN** in this occupant's neighborhood (to be tested in Step 4) |
| Reasoning versus non-reasoning models | Not present ("reasoning models" appears only in a citation, Discussion) | 2611.07876 uses gpt-oss-20b but prefills its final channel so that it answers without reasoning (Section V.A: "Judging without reasoning costs gpt-oss some accuracy") | **NARROW**: a reasoning model has been probed, but with reasoning disabled; probe versus verbal confidence with reasoning enabled on code is not in this neighborhood |
| Elicitation format as a factor | Partial: two categorical formats (7-level, True/False), no numeric percentage, no post-hoc critique, no controlled design; authors flag format as a validity threat | 2608.08266 varies stimulus framing (neutral, concept, function) for the probe, not for the verbal readout | **NARROW** |
| Location of the gap (present in base, introduced by tuning, reduced by reasoning) | Not present | Not present | **CLEAN** in this neighborhood (to be tested in Step 4) |
| Granularity below whole solution | Not present (searched for: "per-test", "requirement", "line-level"); related work cites Huang et al. for line-level internal-state risk | 2607.05188 probes agent steps (parse, tests pass, failing-test reduction, regression) | Belongs to L4; **NARROW** pending Step 4 |

## 5. Forward-citation screen

- **Sources.** Semantic Scholar returned 14 citing records, which are 12 distinct papers plus one
  self-duplicate (the v1 record). OpenAlex returned 7 records, one of them not in Semantic Scholar.
  The merged distinct total is 13.
- **Gaps.** DBLP was unreachable. OpenAlex indexes only the ACM record, so citers that exist only on
  arXiv may be undercounted. Three Semantic Scholar records had no abstract.

| arXiv id | Title | Tag | What it adds against L2 |
|---|---|---|---|
| 2611.07876 | Which Signals of Code Correctness Survive Distribution Shift? Hidden-State and Causal Predictors of Program and Verdict Correctness (2026-11-05) | CLOSE | Six predictors from four families (output confidence, sampled solutions, hidden-state probes, causal localization) on Qwen3-Coder-30B and gpt-oss-20b, LiveCodeBench and BigCodeBench, three languages, AUROC. Has no verbal numeric confidence, no base and instruct pairs, and no reasoning-on condition. |
| 2608.08266 | On the Robustness of LLMs' Internal Representation of Code Correctness (2026-08-08) | CLOSE | Same group and models. Finds "no single configuration is best, and that isolating the fault does not help". |
| 2606.14530 | Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation | CLOSE | Linear probe on Qwen3-4B-Instruct-2507, 444 LiveCodeBench tasks, pre-generation. Single model ("Single model" is listed as a limitation); no verbal comparison. |
| 2607.05188 | Latent Programming Horizons in Coding Agents | CLOSE | Probes on agent residual streams decode parse, tests pass, and regression signals. Has no verbal comparison. |

The 6 RELATED and 3 UNRELATED citers are listed in `parts/fetcher-l2/CITING.md`. The CLOSE papers
also cite earlier code-correctness probing by Bui et al. and Vu et al., which was not fetched in this
step. Both go to the Step 4 run as leads.

## 6. Consequence for L2

- **What is taken.** The headline "hidden states know code correctness better than the model says"
  is no longer available on code at whole-solution granularity. Ribeiro et al. 2026 makes it with
  four models and two benchmarks.
- **What is not taken.** Any claim about where the gap arises (base versus instruct, reasoning on
  versus off), and the format-controlled comparison of verbal numeric confidence with probes and
  sampling agreement under calibration metrics, is not made by this occupant or its citers.
- **Status.** These verdicts are provisional. Step 4 re-tests them against the full literature
  (`VERDICTS.md`).
