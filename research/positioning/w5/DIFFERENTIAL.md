# Differential table: controls of the Rank 1 design against the closest works (wave 5, A6)

Run date 2026-11-10. One row per control of the Rank 1 design (RECOMMENDATION Rank 1), one column per paper. Every cell rests on the paper's full text. Cell evidence, search terms for absences, and source provenance are in `parts/diff-A6/CELLS.md` (Ribeiro, Campos, CREDO, Spiess, NeuroSym-Cal, RLCM), `parts/dossier-A5/STATUS.md` (section pointers for Ribeiro, Campos, CREDO), and `parts/ft-A4b/dossiers/2610.31820.md` with its full text in `parts/ft-A4b/raw/ft/2610.31820.html` (2610.31820 column, filled by the orchestrator).

Codes: **present** (the paper implements the control as defined), **partial** (a weaker or related version), **absent** (searched for and not found).

## Columns

| Column | Paper | Status | Why it is a column |
|---|---|---|---|
| Ribeiro | Ribeiro, Spiess, Devanbu, and Nadi, arXiv 2512.07404, read at v3 | published, ICSE 2026 | occupant of "probes beat stated confidence on code" |
| Campos | Campos, Klassert, and Ulges, arXiv 2611.07876, v1 | concurrent | probes, sampling, and within-problem AUROC on code |
| CREDO | Fan et al., arXiv 2609.34857, v1 | concurrent | trained stated confidence on code, no probe |
| Spiess | Spiess et al., arXiv 2402.02047 | published, ICSE 2025 | calibration of code models against tests |
| CaC | "Free Lunch for LLMs Confidence: The RL Critic Already Knows", arXiv 2610.31820, v1 | concurrent (2026-10-22) | **next-closest on the readout side**, found in wave 5 (A4b): a trained own-readout against a probe "with the same labeled data" on code |
| NeuroSym | NeuroSym-Cal, Findings of ACL 2026 | published | **next-closest on the measurement layer**: four readout families and a per-model post-cutoff subset |

RLCM (arXiv 2604.23333), chosen as next-closest before A4b found CaC, is kept as a supplementary column. CaC replaces it because CaC fits the probe and the trained readout on the same labels and evaluates code in distribution, while RLCM evaluates code only out of domain, with readouts from different policies.

## Table

| # | Control | Ribeiro | Campos | CREDO | Spiess | CaC | NeuroSym | RLCM (supp.) |
|---|---|---|---|---|---|---|---|---|
| 1 | Supervision-matched readouts | absent (Sec 4.1.2, Table 2) | partial (Sec V-A, V-B) | partial (Sec 4.1, Table 4) | partial (Sec III-D, Table IV) | partial (Sec 4.1; Sec 4.2, Table 2) | absent (Sec 4.1) | partial (Sec 4.1, App B) |
| 2 | Trained stated-confidence readout | absent (Sec 2.3) | absent (Sec III-A, IV-A) | present (Sec 2.2, 3, Table 1) | absent (Sec III-B) | present (Sec 4.1) | absent (Sec 3.2, 4.1) | present (Sec 4.1, Table 1) |
| 3 | Prompt-only baseline | absent (Sec 4.1.1) | present (Sec VI-C, Table V) | absent (Sec 3.2) | absent (Sec III-C) | partial (Sec 4.5, Table 6) | absent (Sec 4.2) | absent (Sec 4.1) |
| 4 | Code-text-only baseline | partial (Sec 5.1.3, Tables 5-6) | absent (Sec IV, Table V) | absent (Sec 4.1) | partial (Sec III-B, Tables III-IV) | partial (Sec 2, Table 1) | partial (Sec 3.4, Table 2) | absent (Sec 4.1) |
| 5 | Within-problem scoring | present (Sec 5.1.3, Tables 5-6) | present (Sec V-C, Fig 3, Table V) | absent (App B.3) | absent (Sec III-F) | partial (Sec 4.3, Table 2) | absent (Sec 4.1, 5.1) | partial (Sec 5.2, Table 3) |
| 6 | Oracle swap of test suites | absent (Sec 4.1.2) | absent (Sec V-A, VIII) | absent (App B.3) | partial (Sec III-A, IV-A2, Table II) | absent (Sec 4.1, App C) | absent (Sec 4.1) | absent (Sec 4.1) |
| 7 | Release or contamination split | absent (Sec 7) | absent (Sec V-A) | absent (Sec 4.1, App D.1) | absent (Sec VI) | absent (Sec 4.1) | partial (Sec 4.1, Table 1) | absent (Sec 4.1) |
| 8 | Calibration estimator set | absent (Sec 4.1.3) | absent (Sec V-C) | partial (App B.3, Eq. 20; equal-mass reliability diagrams) | partial (Sec III-C, Fig 2) | absent (Sec 4.1) | absent (Sec 4.3) | absent (Sec 4.1) |
| 9 | Clustered paired inference | partial (Sec 4.2.1) | present (Sec V-C) | absent (Table 1, App B.3) | absent (Sec VI) | absent (Table 3) | absent (Sec 5, Table 1) | absent (Sec 4.2) |
| 10 | Base versus instruct | absent (Sec 4.1.4) | absent (Sec V-A) | absent (Sec 4.1, App B.1) | absent (Sec IV-A4) | absent (Sec 4.1, App C) | absent (Sec 4.1) | absent (Sec 4.1, App C.1) |
| 11 | Same-weights reasoning on/off | absent (Sec 4.1.4) | partial (Sec V-A, VIII) | absent (App B.1) | absent (Sec IV-D) | absent (App C) | absent (Sec 4.1) | absent (App A, C.1) |
| 12 | Routing replay with random and oracle comparators | partial (Sec 5.1.3: best-of-10 selection against Random and a pass@10 ceiling, no execution allocated) | absent (Sec VII, IX) | partial (Sec 4.4, Table 3) | absent (Sec I, V) | partial (Sec 4.3, Table 2) | partial (Sec 5.2, Fig 3) | partial (Sec 5.1, App F) |

## CaC column evidence (2610.31820, full text v1)

- **Row 1, partial.** The probe "fits a linear classifier on the policy's last-token activations with the same labeled data" as R-Tuning (Sec 4.1). R-Tuning fine-tunes the policy, which "lowers accuracy on 15 of the 16 model-domain-split combinations" (Sec 4.2, Table 2). The two arms are therefore inferred, not stated, to be scored on different generations.
- **Row 2, present** (corrected after A7 F11). R-Tuning "fine-tunes the policy on held-out labeled responses to append 'I am sure' or 'I am unsure'" (Sec 4.1), a trained verbal readout. It is categorical and scored by token probability; no trained numeric stated confidence is reported.
- **Row 3, partial.** The critic read "at the prompt alone" reaches AUROC 0.83 in distribution (Sec 4.5, Table 6). That analysis is a critic on the general-reasoning checkpoint, not a prompt-only baseline for the code probe.
- **Row 4, partial.** External estimators read only "the question and the target policy's response as text" and match self-estimation (Sec 2, Table 1: APPS, TACO). They are fit to a Llama-3-8B-Instruct policy's traces, not to the Sec 4 policies.
- **Row 5, partial** (corrected after A7 F12). Metrics are pooled: "every sample is scored with AUROC (AUC), 15-bin ECE and the Brier score" (Sec 4.1). Critic selection among the model's own 8 samples per prompt (Sec 4.3, Table 2) is within-problem use, but no within-problem discrimination metric is reported.
- **Rows 6 to 8, absent.** Code labels come from "rule-based grading" (App C). In-distribution and out-of-distribution splits are by source (Sec 4.1), not by release date. ECE uses 15 bins only (Sec 4.1).
- **Row 9, absent.** Table 3 has no intervals or tests.
- **Rows 10 and 11, absent.** Both policies are PPO-trained with thinking on (App C).
- **Row 12, partial.** Critic selection among 8 samples is compared with Maj@8 and an oracle Best@8 (Sec 4.3, Table 2). There is no random comparator and no execution budget.

## Corrections after the A7 critic

Cells changed after the A7 critic (`parts/critic-A7/FINDINGS.md`), each checked against the full text:

- **CaC row 2, F11:** partial changed to present.
- **CaC row 5, F12:** absent changed to partial.
- **CREDO row 8, F14:** absent changed to partial.
- **Ribeiro row 12, F15:** absent changed to partial, for consistency with CaC.
- **CaC row 1, F16:** "different generations" is now marked as inferred.
- **Campos wording, F13:** corrected.

The A7 critic also concluded that, with concurrent works in scope, 2610.31820 and Campos together leave only the combination of a trained readout with within-problem scoring on identical generations (F2). That changes the ranking; see `../w4/VERDICTS.md` and `../w4/RECOMMENDATION.md` (wave 5 change logs).

## Clean residual

These cells are not present in any of the six main columns (RLCM excluded):

| # | Control | Best cells | Why they fall short |
|---|---|---|---|
| 1 | Supervision-matched readouts | partial: Campos, CREDO, Spiess, CaC | No paper fits every readout to the same labels and folds on identical generations. CaC is closest, but R-Tuning changes the generations. |
| 4 | Code-text-only baseline | partial: Ribeiro, Spiess, CaC, NeuroSym | None is a code-text classifier fit to the study's own labels on the same policy as the probe. |
| 6 | Oracle swap of test suites | partial: Spiess (exact match versus tests) | None contrasts original and augmented tests on the same generations across readout families. Outside the six columns, MARGIN 2605.22949 (concurrent) does so for verbal confidence only (`parts/ft-A4a/dossiers/2605.22949.md`). |
| 7 | Release or contamination split | partial: NeuroSym | No pre- versus post-cutoff result is reported. |
| 8 | Calibration estimator set | partial: Spiess, CREDO | Every paper reports one ECE value; Spiess and CREDO add only equal-mass reliability plots. |
| 10 | Base versus instruct | none | Absent in every column. |
| 11 | Same-weights reasoning on/off | partial: Campos | Campos makes one check, on the confidence readout only. |
| 12 | Routing replay with random and oracle comparators | partial: Ribeiro, CREDO, CaC, NeuroSym | No replay on code with both comparators at a matched execution budget. |

Rows 2, 3, 5, and 9 are each present in at least one column, so they are not residual on their own. What is unoccupied is their combination: no column has a trained stated readout (row 2) together with within-problem scoring (row 5) and input-only baselines for the probe (rows 3 and 4) on identical generations. CaC holds rows 2 (present) and 1, 3, 4, and 5 (partial), with pooled metrics only. Campos holds rows 3, 5, and 9 and reads a categorical self-judgment, P(Yes), but no numeric or trained stated readout (corrected after A7 F13).

Caveat: the residual is judged against these columns plus the A3, A4a, and A4b screens. Other wave 4 occupants cover single rows outside code or with other signals: TRIAGE 2605.13414 and 2606.15841 (random and oracle routing comparators), 2610.11300 (base versus instruct, token readouts on code), and Miao and Ungar 2603.25052 (base versus instruct, non-code). These are not repeated here; see `../w4/VERDICTS.md`.
