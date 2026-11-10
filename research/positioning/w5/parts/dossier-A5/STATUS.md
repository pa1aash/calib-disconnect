# A5 status: full-text verification of three close works

Retrieval date 2026-11-10. Versions from export.arxiv.org (raw/meta.xml). Full texts from arxiv.org/pdf and arxiv.org/html (all HTTP 200, raw/FETCHLOG.md), extracted locally with pymupdf (raw/*.txt). Page numbers below are PDF pages.

## Status table

| Paper | W4 status | W5 status | Version read | Corrections with evidence |
|---|---|---|---|---|
| Ribeiro, Spiess, Devanbu, Nadi, 2512.07404 | FULL TEXT dossier | FULL TEXT, verified; corrected copy written | v3, 2026-01-21 (latest; v1 2025-12-08) | (1) Venue confirmed: Crossref DOI 10.1145/3744916.3787846, ICSE 2026, pp. 1160-1172. (2) The quoted "+13.3 to +29.0 pp" (Sec 4.2.1) is right, but the same paper says +28.8 in Sec 4.2.3 and the RQ1 box (p. 7): 29.0 is against best reflective (OpenCoder T/F 27.3%), 28.8 against Random 27.5% (Table 3). (3) The HumanEval +26.2 is Qwen FitSyn (OOD fit) 63.0% over Intrinsic (likelihood) 36.8%, not over verbal (Sec 4.2.3, Table 4). So the DIGEST range "8.7 to 29.0 points better than verbal and likelihood readouts" mixes baselines. (4) "Verbal" readouts are token probabilities of verbal answers: Regular is "weighted by the model's joint probability"; T/F is "scored according to the model's assigned probability to True" (Sec 2.3). They are not a sampled stated confidence. (5) The W4 label-independence entry is incomplete. In RQ1 the correct candidate is the reference solution and the incorrect ones are other LLMs' failures (Sec 4.1.1). In RQ2 the candidates are self-generated, 10 at T=1 (Sec 5.1.1). (6) The W4 dossier omits the inference method, GEE logistic regression with BH correction (Sec 4.2.1). (7) It also omits the RankEF trained ranker baseline (Sec 5.1.3). (8) Test splits are 121 and 367 tasks; LAT is fit on only 15 or 46 tasks (Table 2). Every other W4 number checks. |
| Campos, Klassert, Ulges, 2611.07876 | FULL TEXT dossier | FULL TEXT, verified; corrected copy written; no newer version | v1, 2026-11-05 (only version on 2026-11-10) | (1) The W4 Table II numbers are correct but belong to the verdict-correctness target; W4 does not label the target. (2) The model is Qwen3-Coder-30B-A3B-Instruct, a MoE with 3B active, so "30B" overstates active scale (Sec V-A a). (3) W4 omits the within-problem AUROC (Sec V-C a, Fig. 3, Sec VI-A c, VI-C c, Table V) and the input-only probe at the last prompt token (Table V). (4) W4 omits the inference method, a paired problem-clustered bootstrap with 2,000 resamples (Sec V-C b). (5) The reasoning check uses 498 candidates; balanced accuracy goes from 62.4% to 67.8% (Sec VIII a). (6) DIGEST/VERDICTS "Campos 0.620 vs 0.629" is not a matched pair. The 0.629 is Qwen3-Coder confidence, within problem, under language shift, program target (Sec VI-C c). The paper does not print 0.620 as a shift value. Under shift, Table V gives within-problem .540 for the judging-pass probe and .627 for the last-code-token probe (ID values: .553 and .620). The matched shift comparison is .540 or .627 vs .629. All other W4 numbers check. |
| Fan et al., CREDO, 2609.34857 | NO dossier (cc-1 gap-fill note only) | FULL TEXT, new dossier | v1, 2026-09-28 (only version) | (1) The vault note is the same paper (title and ID match). (2) The cc-1 phrase "in-domain code" means trained on DeepCoder and macro-averaged over four code sets, including LCB v5/v6 and HumanEval+ (Table 1, B.3). It is not the DeepCoder test split alone. (3) The CREDO AUROC lead is not robust to reading the baseline by digit expectation: DCPO-d .849±.027 vs CREDO .850±.027 (Table 1), and DCPO-d leads on LCB v6, .896 vs .887 (Table 13). CREDO's clear wins are on ECE and Brier. (4) The cc-1 AUROC values .850/.815/.776/.753/.690 check (Table 1). |

## Pointers for the differential table

### Ribeiro 2512.07404 (v3)
- Training/supervision per readout: LAT is PCA on paired correct-minus-incorrect differences; sign from labels; layer chosen on Val (Sec 2.1 Step 3, Sec 3, Fig. 2, pp. 3-4). Likelihood is unsupervised (Sec 2.3). Reflective readouts are zero-shot prompts scored by token probability (Sec 2.3, Fig. 3). RankEF is a trained CodeT5+ on 5,000 APPS tasks (Sec 5.1.3).
- Data splits: task-level 10% Fit / 10% Val / 80% Test, 10-fold CV; OOD fit on MBPP+ or Synthetic with 4-fold inner CV (Sec 4.1.2, Table 2). RQ2 uses fold 1 only (Sec 5.1.2). Problem-grouped: yes.
- Within-problem metrics: all metrics are within task. RQ1 is 1-of-4 selection accuracy (Sec 4.1.3, Tables 3-4); RQ2 is pass@rank-k over 10 own samples (Sec 5.1.3, Tables 5-6, Figs. 4-5). No pooled AUROC.
- Input-only baselines: none.
- Calibration metrics: none (searched: ECE, Brier, AUROC).
- Contamination/release controls: none (searched: contamin, cutoff). Threats to validity discuss shared training data of the source models (Sec 7 Internal Validity).
- Statistical inference: GEE logistic regression with Benjamini-Hochberg, p < 0.05 (Sec 4.2.1); mean ± sd over 10 folds (Sec 4.1.2); "Only a few comparisons reached statistical significance" in RQ2 (Sec 5.2.1).
- Base vs instruct: none; all four models are instruct (Sec 4.1.4).
- Reasoning toggles: none.
- Routing/selection: RQ2 candidate ranking and selection (Sec 5, Tables 5-6, Figs. 4-5); practical gating discussion only (Sec 6.1). No routing experiment.

### Campos 2611.07876 (v1)
- Training/supervision per readout: confidence is untrained, with temperature as its free parameter (Sec IV-A, V-B b). EigenScore is unsupervised (Sec IV-B). The probe is logistic regression on 512 candidates per class (Sec IV-C a, V-B a). LAT uses Ribeiro's prompt with one pass/fail pair per problem (Sec IV-C b, V-B a). DAS uses k=6 and trains on correctly judged candidates (Sec IV-D b, V-B a). The value probe is described in Sec IV-D d, and the generation probes of RQ3 in Sec V-B a. Layer selection is cross-fitted (Sec V-B b).
- Data splits: 60/20/20 by problem, three partitions with disjoint test sets (Sec V-A d). Language sets share one problem split across languages (Sec III-C). Problem-grouped: yes.
- Within-problem metrics: definition in Sec V-C a. Results in Fig. 3, Sec VI-A c (verdict target), Sec VI-C c (program target), and Table V.
- Input-only baselines: the probe at the last prompt token of generation "has seen only the problem" (Sec VI-C d, Table V). The problem-level comparison is in RQ4 (Sec VI-D, Table VI).
- Calibration metrics: none; AUROC only (Sec V-C a).
- Contamination/release controls: the language sets use 454 LCB problems released Oct 2024 to May 2025 (Sec V-A b). There is no contamination analysis.
- Statistical inference: paired problem-clustered bootstrap with 2,000 resamples plus between-partition variance; significance at |Δ| > 1.96 SE (Sec V-C b). Rerun noise is up to 0.02 AUROC (Sec VIII b).
- Base vs instruct: none.
- Reasoning toggles: gpt-oss is run with its final channel prefilled, so no reasoning (Sec V-A a). A medium-effort reasoning check is in Sec VIII a.
- Routing/selection: none run. "Triage rather than selection" discussion (Sec VII b); gating is future work (Sec IX).

### CREDO 2609.34857 (v1)
- Training/supervision per readout: the CREDO readout is regressed toward a hybrid target (Sec 3.1-3.2, Eqs. 6-7). Policy rewards are in Sec 3.3 (Eq. 8) and discrepancy weighting in Sec 3.4 (Eq. 9). RLCR and DCPO rewards are in Sec 2.2 (Eq. 4). The GRPO objective is in Sec 2.1 (Eq. 1). Hyperparameters are in App B.2 (Table 4) and prompts in App B.1. Ablations are in Sec 4.3 (Table 2, Fig. 4) and App C.2-C.3.
- Data splits: DeepCoder train 9,500 / test 500; held-out sets are HumanEval+, LCB v5, and LCB v6 (App B.3, Table 5). Grouping is by dataset; within-problem pooling is not discussed.
- Within-problem metrics: none. Pooled metrics only (App B.3).
- Input-only baselines: none.
- Calibration metrics: ECE (10 equal-width bins), Brier, AUROC, AURC, acc@coverage, and threshold count (App B.3, Eqs. 20-21). Results are in Table 1, Table 3, Fig. 6 (App C.5), and Tables 11-14 (App D.1).
- Contamination/release controls: none (searched: contamin). AIME 2026 and LCB v6 are used without date filtering (Table 5).
- Statistical inference: mean ± std over training seeds 43-45; bold marks results within one joint SE (Table 1, Sec 4.1). Section 4.4 says some results are "statistically tied" without naming a test.
- Base vs instruct: none. "Base" is the untrained Qwen3-8B (App B.2, Table 4). Scale runs at 1.7B and 4B are math only (App C.1, Table 6).
- Reasoning toggles: none (searched: think). All runs use a step-by-step prompt (App B.1).
- Routing/selection: selective prediction and abstention (Sec 4.4, Table 3, Fig. 5). Routing is mentioned only for Chuang et al. (Sec 5).
