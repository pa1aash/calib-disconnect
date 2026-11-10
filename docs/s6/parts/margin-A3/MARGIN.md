# MARGIN (arXiv 2605.22949): full-text inventory for wave 6, task A3

Scope: what MARGIN covers that bears on L1 Q10 (augmented-test oracle swap with calibration measured), what it does not cover, and what a systematics-budget study adds beyond it. No judgment of correctness is offered; citations only.

## Sources and conventions

- TXT = `research/positioning/w5/parts/ft-A4a/raw/ft/2605.22949.txt` (extracted text, 2389 lines, read in full). Its header states arXiv:2605.22949v4 dated 8 Oct 2026 (TXT:6, TXT:45). Single author (TXT:3-5).
- DOS = `research/positioning/w5/parts/ft-A4a/dossiers/2605.22949.md`
- F4 = `research/positioning/w5/parts/critic-A7/FINDINGS.md` lines 59-62
- The arXiv v1 date (2026-05-21) is carried from DOS:2 and F4:61 and is not verified in TXT.
- "Not located" means the phrase or quantity was not found in TXT after reading all 2389 lines and grepping for AUROC, AUC, isotonic, probe, logit, hidden, sampl, contamina, release, difficult, prompt-only, text-only, cluster, within-problem, token, temperature, retrain, EvalPlus, Brier, and pairwise.

## 1. Q1: what MARGIN covers for the hardening cell

| Item | What the paper states | Citation |
|---|---|---|
| Hardening checks | HE→HE+ and MBPP→MBPP+ are "expanded tests from EvalPlus [24] on the original candidate programs." | TXT:447-449 |
| Status of the checks | "These two hardening checks change the correctness criterion for previously seen tasks; they are not independent unseen-question generalisation tests." | TXT:448-450 |
| Candidates re-scored? | Yes. "These tests reuse the original candidate programs rather than eliciting new answers." | TXT:1238-1240 |
| Table label | "'Hardening' reuses the original tasks under expanded tests." | TXT:484-485 |
| Source label regime | Original HE and MBPP labels "re-evaluated against pinned tests." | TXT:474-475 |
| Adaptation protocol | Full correctness feedback on source; each online method "carries its own state into the target workload without reset." | TXT:468-470 |
| Confidence family | Verbalized, single family. "Verbalized collection requested an answer followed by confidence on a 0–100 scale, using temperature zero." | TXT:1256-1257; also TXT:206-207 |
| Prompt, HE | Confidence requested as "Confidence: {0-100}"; HE prompt shows no test cases. | TXT:1262-1271 |
| Prompt, MBPP | MBPP prompt includes "{first test case}" in the prompt text. | TXT:1274-1285 (test case at TXT:1279-1280) |
| Agreement-based signal | Sensitivity only; "matched agreement-based signals are sensitivity evidence." Not stated to cover hardening rows (not located). | TXT:164-165; TXT:2375-2378 |
| Calibration metric | ECE, ten equal-width bins, pooled across responders in a cohort, 0-100 scale. | TXT:549-561 (Eq. 12 at TXT:551-558) |
| Exclusions | Rows without valid confidence or determinate correctness excluded from calibration. | TXT:562-563 |
| Selection / pairwise | Not reported for hardening rows. Selection is for HE, MBPP, BCB cold start (TXT:676-681; Table 4 at TXT:690-733). Table 10 hardening rows contain ECE only (TXT:1598-1669). | as listed |
| Raw ECE, original tests, same cohort | Not located. Table 3 raw values are for the EvalPlus target only. | TXT:661-668 |
| Nearest raw ECE on original tests (different cohort) | 18-model cold start: HumanEval raw 12.80 (TXT:698-700); MBPP raw 17.51 (TXT:711-714). Different pool and phase from Table 3's nine-cloud cohort. The paper does not compare these with the EvalPlus raw values. | TXT:690-692 (caption, "18-model pool") |
| Raw ECE, EvalPlus, nine-cloud | HE→HE+ raw 8.57, MARGIN 3.57, Δ −5.00 [−6.25, −1.99]. MBPP→MBPP+ raw 17.96, MARGIN 3.07, Δ −14.89 [−16.18, −9.82]. | TXT:661-668 |
| AUROC | Not located (no occurrence of AUROC or AUC). | grep, all of TXT |
| Task counts | HE 164 (Table 1 source) → HE+ 163 (TXT:521); HE+ excludes HumanEval/32. MBPP 257 → MBPP+ 224 (TXT:524). | TXT:490-493; TXT:518-524; TXT:1238-1239 |
| Usable target records | HE→HE+ 1467; MBPP→MBPP+ 2016. | TXT:1221-1228 (Table 9) |
| Models | Nine cloud models for the hardening rows (TXT:520, TXT:523). Cloud identifiers: MiniMax-M2.5, Qwen2.5-14B-Instruct-1M, Qwen2.5-32B-Instruct, Qwen3-32B, Qwen3-Coder-480B-A35B-Instruct-FP8, DeepSeek-R1-Distill-Qwen-32B, DeepSeek-V3.2, openai/gpt-oss-120b, zai-org/GLM-4.7-Flash. | TXT:1117-1141, 1181, 1185 (identifiers, Table 8) |
| Hardening comparators, HE→HE+ (ECE) | Decayed histogram 2.81; Online Platt 1.94; sliding-window 2.71; windowed multiply 4.75; windowed replace 4.17; MARGIN ks=0 2.25. | TXT:1598-1633 |
| Hardening comparators, MBPP→MBPP+ (ECE) | Decayed histogram 4.71; Online Platt 2.79; sliding-window 4.02; windowed multiply 5.06; windowed replace 4.37; MARGIN ks=0 2.19. | TXT:1634-1669 |
| Hardening comparisons significance | All five comparisons on each hardening check are inconclusive. Platt and decayed histogram have lower point ECE than MARGIN on HE+ (Δ for MARGIN minus comparator is positive, intervals include zero). | TXT:638-640; TXT:1604-1618; TXT:1643-1647 |
| No-shrinkage ablation on hardening | MARGIN minus MARGIN ks=0: HE→HE+ +1.318 [+0.725, +1.702]; MBPP→MBPP+ +0.876 [+0.148, +0.954]. Interval excludes zero on both. | TXT:1629-1633; TXT:1665-1669; TXT:834-835 |
| Selected-model diagnostic on hardening | Table 11 includes HE→HE+ (selected 3.39, degradation −0.184 [−2.287, +1.075]) and MBPP→MBPP+ (selected 4.91, degradation +1.844 [−1.025, +3.202]). Only MARGIN is reported. Table 12 has no hardening rows. | TXT:1732-1764; TXT:1765-1767 (Table 12 caption) |
| Stated scope | "Test hardening reuses tasks; gradual or recurring drift is untested." | TXT:907-909 |

What this establishes for L1 Q10: MARGIN reports post-EvalPlus ECE for one verbal-confidence family, pooled over responders, on nine cloud models, with MARGIN's ECE below raw in both hardening rows (TXT:661-668). It does not report raw calibration or AUROC on the original tests for the same nine-cloud cohort, so it does not measure whether test insufficiency changes raw calibration. Its hardening result is about calibration after a relabel, with the comparison to baselines inconclusive (TXT:638-640).

## 2. Q2: probe, token, sampling, trained readout, within-problem, release, and clustered inference

| Element | Status | Citation |
|---|---|---|
| Probe or hidden-state readout | Absent. "without model internals, retraining, or a separate calibration dataset." | TXT:61-62 |
| Logits or token probabilities | Absent. "No model weights, logits, or training data are available to the coordinator." | TXT:110-112 |
| Token caps | Output caps are configuration, not a readout: "A configured output cap does not establish how many tokens were actually generated." | TXT:1257-1259 |
| Sampling | Primary elicitation is temperature zero, single response. Sampling appears only in an extended agreement-based channel: "Agreement confidence is computed from five additional archived sample signatures matching the original candidate; correctness labels are not inputs." Self-consistency is discussed in related work only. | TXT:1256-1257; TXT:2375-2378; TXT:161-163 |
| Trained readout | Present on stated confidence only. Online Platt: "p = σ(ac + b)", one SGD step per observation, η = 0.1, λ = 10⁻⁴. No hidden-state readout. | TXT:535-539; TXT:1363-1369 |
| Histogram and windowed estimators | Non-trained, non-parametric; decayed histogram uses decay 0.98; sliding window W = 200. | TXT:527-532; TXT:1340-1362 |
| Within-problem scoring | Pairwise resolution compares responses to the same task: "Pairwise resolution considers only pairs containing exactly one correct response." This is in cold-start coordination (HE, MBPP, BCB) and the BCB diagnosis, not in hardening rows. | TXT:567-570; TXT:709-733; TXT:738-745; TXT:158-159 |
| Within-problem ordering | Primary ordering processes all predictions for a problem before its updates. This is ordering, not a within-problem score. | TXT:584-586; TXT:1379-1382 |
| Release or contamination split | Absent. Excluded archives (LiveCodeBench, CodeContests, TriviaQA) are excluded for evidence-authentication reasons, not contamination. "Data and code availability. The code and retained analysis data supporting the reported results are not publicly available." | TXT:481-483; TXT:1250-1253; TXT:931-932; grep "contamina" and "release" returned no calibration split |
| Difficulty strata | Not located. Table 9 gives support counts, not difficulty. | TXT:1189-1190 |
| Prompt-only or code-text-only baseline | Not located. | grep, all of TXT |
| Interval method | Paired 95% intervals from "10,000 problem-cluster bootstrap draws." Seed: NumPy RandomState 42. | TXT:577-578; TXT:1418-1419 |
| Interval scope | Resamples retained contributions; "no calibration trajectory is replayed inside a draw." Conditional on recorded histories. | TXT:579-581; TXT:1421-1424 |
| Interval correction | "Intervals are pointwise without multiplicity adjustment." | TXT:582-583; TXT:1423-1424 |
| Clustering on model or family | Not located. The only cluster is the problem. | TXT:577; TXT:1418 |
| Shuffle histories | 100 recorded shuffle histories are averaged, not used as an uncertainty source for intervals. | TXT:571-573; TXT:1398-1408 |
| Model-level breakdown | Table 8 gives per-model counts (TXT:1117-1186). Reported ECE and comparisons are pooled; cloud/local split described as "descriptive" and "never a controlled intervention." | TXT:1107-1109 |

## 3. Q3: what a systematics-budget study adds beyond MARGIN

Each row gives MARGIN's status, then what the budget design adds. Citations as above.

1. Raw gap between a hidden-state probe and stated confidence on frozen self-generated code. MARGIN has no probe and no hidden-state readout (TXT:61-62, TXT:110-112). It has one stated-confidence family (TXT:1256-1257). Added: the probe-minus-stated gap itself, on the same frozen programs.

2. Attribution with clustered uncertainty. MARGIN uses a problem-cluster bootstrap, pointwise, with no multiplicity adjustment and conditional on recorded histories (TXT:577-583; TXT:1418-1424). Added: clustered uncertainty over problems and models, and an attribution decomposition whose components carry their own intervals.

3. Supervision axis. Zero-shot: raw stated confidence is an "uncalibrated reference" (TXT:527-528). Isotonic: not located. Trained stated readout: online Platt (TXT:535-539, TXT:1363-1369), updated online, not fit offline. Added: a zero-shot probe and stated baseline, an isotonic readout (not in MARGIN), an offline trained stated readout, and a trained probe readout, all under one protocol.

4. Difficulty axis. Pooled ECE across responders (TXT:560-561). Within-problem comparison exists only as pairwise resolution in cold-start coordination (TXT:567-570; TXT:709-733). Prompt-only and code-text-only baselines: not located. Difficulty strata: not located. Added: pooled and within-problem scoring for probe and stated readouts, with prompt-only and code-text-only baselines.

5. Label validity axis. Original and EvalPlus suites are both used, but on the same programs as a relabel (TXT:447-450; TXT:1238-1240), with source state carried into the target without reset (TXT:468-470). No readout is retrained under each suite. Added: all readouts retrained under each suite, both suites reported on matched raw calibration and AUROC, and the MBPP prompt's exposed first test case (TXT:1279-1280) treated as a stratum.

6. Generation shift. Not present. Candidates are reused (TXT:1239-1240). The only generation is temperature zero per prompt (TXT:1256-1257). Sampling appears only as the extended agreement channel (TXT:2375-2378). Added: a generation-condition shift, which MARGIN does not vary.

7. Contamination. Not present as a split (see Section 2). Added: a contamination stratum.

8. Model family and scale. Eighteen models across Qwen, DeepSeek, GPT-OSS, MiniMax, GLM, LLaMA, Phi, Mistral, and Coder variants (TXT:1117-1186). Results are pooled; cloud versus local is descriptive (TXT:1107-1109). Quantization (4-bit local) and Ollama context sizes differ (TXT:1105-1106). Serving telemetry is incomplete (TXT:909-910; TXT:1107). Added: family and scale as explicit strata with per-stratum estimates.

9. Ranking statistic on original and EvalPlus labels. AUROC: not located. Pairwise resolution is the nearest same-task ranking statistic, and it is not reported on hardening rows (TXT:567-570; TXT:709-733). Added: AUROC and matched pairwise on both suites.

## 4. Flags for the orchestrator

- Table 9 hardening counts do not match the Table 8 cloud columns when summed. Table 9 gives 1467 usable target records for HE→HE+ and 2016 for MBPP→MBPP+ (TXT:1221-1228). Summing the nine cloud HE entries in Table 8 (TXT:1118-1186) gives 1320 (values 158, 164, 164, 163, 163, 55, 164, 132, 157). Summing the nine cloud MBPP entries gives 2142 (254, 257, 257, 257, 257, 102, 257, 246, 255). This is my arithmetic from TXT. The text does not reconcile these. The BCB rows do reconcile: the nine cloud BCB entries sum to 1190, matching Table 9 (TXT:1190; TXT:1204-1208).
- Table 4's raw ECE values (TXT:700, 714) are from the 18-model cold start, not the nine-cloud cohort, so they cannot be used as a matched original-test baseline for Table 3's hardening rows.
- The critic's F4 statement (F4:62) is confirmed by this full read: no raw ECE on the original tests for the same cohort.
- Dossier DOS:4 says "BigCodeBench-Hard," consistent with TXT:1233.
- The v1 date is not verified in TXT.
