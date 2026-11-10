# PROTOCOL: arXiv 2610.31820 "Free Lunch for LLMs Confidence: The RL Critic Already Knows" (Wu and Ji)

Wave 6, task A2. Read-only extraction. Full-text basis.

## Sources and citation key

- Full text (primary): `research/positioning/w5/parts/ft-A4b/raw/ft/2610.31820.txt` (2,939 lines). Cited below as `txt:N`, where N is the line number in that file as displayed by the Read tool. Section and appendix labels come from the paper's own headings as they appear in that text.
- The `.html` sibling was not read; the user stated it is the same paper. No URL was fetched.
- Existing dossier: `research/positioning/w5/parts/ft-A4b/dossiers/2610.31820.md`. Its numbers were spot-checked against Tables 1 and 3 (for example, Qwen3-8B code AUROC ID/OOD: Verbalized 0.60/0.61, R-Tuning 0.86/0.85, Probe 0.88/0.84, CaC 0.93/0.91 at `txt:386`-`txt:478`) and agree with the text. The dossier's sentence that R-Tuning "so its arm is scored on different generations from the probe arm" is the dossier's own inference, not a statement in the paper (see Section 7).
- Table-layout note: in the extracted text, the model-name labels for Table 2 and Table 3 sit inside the row group of the preceding Best@8 row. Table 2 block for Qwen3-8B is `txt:251`-`txt:301` and for Nemotron-Cascade-8B is `txt:302`-`txt:353`. Table 3 block for Qwen3-8B is `txt:384`-`txt:479` and for Nemotron-Cascade-8B is `txt:480`-`txt:575`. This mapping is inferred from label position and from the 3.9-point average drops stated at `txt:1112` (Qwen R-Tuning average 50.4 vs Original 54.3; Nemotron 51.6 vs 55.5).

---

## 1. Which generations the R-Tuning readout was scored on

**Answer: not stated.** The text never says explicitly whether the R-Tuning confidence score in Table 3 (`txt:423`-`txt:460`, `txt:519`-`txt:556`, and the per-benchmark Tables 8-10) was computed on the fine-tuned R-Tuning model's own new outputs or on frozen generations of the base or RL policy.

Every sentence that bears on the question:

- Section 4.1, Baselines (`txt:1096`): "R-Tuning ( Zhang et al., 2024b ) , the training-based estimator, fine-tunes the policy on held-out labeled responses to append “I am sure” or “I am unsure”."
- Section 4.1, Baselines (`txt:1098`): "The labeled sets are disjoint from all RL training and evaluation data, and each contains the same number of examples as the corresponding RL training set."
- Section 4.1, Evaluation (`txt:1104`): "Every prompt is answered with several samples at the RL temperature, and every sample is scored with AUROC (AUC), 15-bin ECE and the Brier score."
- Section 4.1, Evaluation (`txt:1100`): "Each domain has an in-distribution (ID) split of held-out problems from the RL training sources and an out-of-distribution (OOD) split from external benchmarks:"
- Section 4.2 (`txt:1108`): "Table 2 reports task accuracy, Table 3 reports confidence estimation on math, code and agentic tool calling,"
- Section 4.2 (`txt:1112`): "CaC never updates the policy, so its task accuracy is exactly that of the RL policy (the Original Policy rows in Table 2). R-Tuning does not share this property: fine-tuning the policy on the confidence objective lowers accuracy on 15 of the 16 model–domain–split combinations, by 3.9 points on average for both Qwen3-8B and Nemotron-Cascade-8B."
- Section 4.2 (`txt:1113`): "CaC pays nothing here because it never updates the policy: the critic is trained alongside it during RL and is read out as is."
- Section 2, R-Tuning mechanics, Llama-3 setting (`txt:112`): "At inference time, we use the probability assigned to the confidence token as a continuous confidence score." (Section 2 concerns Llama-3-8B-Instruct, not the Section 4 models.)
- Table 2 caption (`txt:354`-`txt:355`): "Task accuracy (%) with and without inference-time scaling. Rows above the thin rule use a single response; rows below sample N = 8 N{=}8 responses ..."
- Appendix C, Evaluation (`txt:2019`-`txt:2020`): "We use the same sampling temperature, top- p p , and response-length limit as in training, drawing four responses per prompt."

Strongest inference (not stated): the R-Tuning score was read from the fine-tuned R-Tuning model's own new outputs. Basis:
1. Table 2 gives the R-Tuning rows their own task accuracy, distinct from the Original Policy rows (`txt:252`-`txt:259` vs `txt:262`-`txt:269` for Qwen3-8B; `txt:303`-`txt:310` vs `txt:313`-`txt:320` for Nemotron-Cascade-8B). A model that is fine-tuned, and whose accuracy is measured separately, is evidently generating its own responses.
2. The paper describes R-Tuning as fine-tuning "the policy" (`txt:1096`) and says its accuracy drops because of that fine-tuning (`txt:1112`), so the confidence token is emitted by the modified model.
3. The paper's own scoring protocol (`txt:1104`) is "answered with several samples at the RL temperature", which is applied uniformly to all estimators.

Caveats: the text does not say which model's responses were used as the R-Tuning training targets (the "held-out labeled responses" at `txt:1096` are not attributed to a generating policy), does not say whether the R-Tuning evaluation prompts and samples match those of Probe and CaC, and does not say whether the fine-tuned model was the base instruct checkpoint or the RL checkpoint.

## 2. Generations scored for the Probe and CaC; probe layer, token position, training data

### Probe

- Generations scored: **not stated.** Inference: the RL policy's own samples (the Original Policy). Basis: the probe is "fits a linear classifier on the policy’s last-token activations" (`txt:1097`), "the policy" in this paper means the RL policy (`txt:1112`), and the protocol is common to all estimators (`txt:1104`). Not explicitly stated that the probe reads activations from the Original Policy's generations.
- Layer: **not stated.**
- Token position: "last-token activations" (`txt:1097`). Whether this is the last prompt token or the last response token is **not stated**.
- Classifier type: "a linear classifier" (`txt:1097`). Regularization, optimizer, and loss: **not stated**.
- Training data: "with the same labeled data" (`txt:1097`), which is the labeled set described at `txt:1098` (disjoint from RL data; same size as the corresponding RL training set). The generating policy for the labeled set is **not stated** in Section 4. Size of the RL training set: **not stated**.

### CaC (Critic-as-Confidence)

- Generations scored: samples from the RL run's policy at the RL temperature (`txt:1104`; Appendix C `txt:2019`-`txt:2020`). Score is read from the critic at the last response token, clipped to [0, 1] (`txt:1092`; `txt:232`-`txt:233`).
- Reading position: "Confidence is read from the critic’s scalar output at the last non-padding token." (`txt:2022`). Prefix-level reads exist for Table 6 only (`txt:1223`, `txt:1227`).
- Critic architecture: "with a randomly initialized scalar value head for the critic" on the actor's model (`txt:1973`). Which hidden layer feeds the head: **not stated**.
- Critic training data: the PPO rollouts of the RL run (`txt:1177`, `txt:1977`-`txt:1980`). PPO configuration (Table 7, `txt:1982`-`txt:2018`): PPO with GAE, discount and GAE lambda 1.0/1.0, terminal correctness reward in {0, 1}, actor learning rate 10^-6 and critic learning rate 2×10^-5 (rendered as `txt:1990`-`txt:1991`), constant schedule, actor clip ratio 0.2, actor KL coefficient 10^-3, critic loss unclipped MSE, PPO epochs per batch 1, gradient clipping 1.0, prompts per step 16, rollouts per prompt 64, PPO mini-batch size 16, max prompt/response tokens 2,048/16,384, sampling temperature 1.0, top-p 1.0.
- Run length: "Training runs for 300 steps without repeating prompts." (`txt:1980`). One RL run per domain (`txt:1088`).
- Critic for critic-free RL (Table 5, `txt:1174`-`txt:1177`): a value model "fit post hoc on the rollouts that GRPO already generated" (`txt:1177`), Qwen3-8B on WebInstruct-verified. Its probe and R-Tuning baselines are in Table 5 but no per-baseline generation details are given.

## 3. Models, benchmarks, problem and sample counts, splits, grading, decoding

### Models

| Role | Model (as named in text) | Citation in text | Checkpoint ID, release | Source |
|---|---|---|---|---|
| RL policy and critic (Section 4) | Qwen3-8B | Yang et al., 2025 (arXiv:2505.09388) | Checkpoint ID not stated; release not stated | `txt:1088`, `txt:1973`, refs `txt:1708`-`txt:1713` |
| RL policy and critic (Section 4) | Nemotron-Cascade-8B | Wang et al., 2025 (arXiv:2512.13607) | Checkpoint ID not stated; release not stated | `txt:1088`, `txt:1973`, refs `txt:1650`-`txt:1655` |
| Section 2 target | Llama-3-8B-Instruct | Grattafiori et al., 2024 | Not stated | `txt:101` |
| Section 2 external estimator | Qwen2.5-7B-Instruct | Qwen Team, 2024 | Not stated | `txt:113` |
| Section 2 external estimator | Mistral-7B-Instruct-v0.3 | Jiang et al., 2023 | Not stated | `txt:113` |

- Base vs instruct status for the Section 4 models: **not stated**. Thinking mode: "Thinking mode remains enabled under the default chat template." (`txt:1974`). The chat template is named only as "default".
- Section 2 uses LoRA SFT: "All models are fine-tuned with the same LoRA-based ( Hu et al., 2022 ) supervised fine-tuning procedure." (`txt:114`).

### Benchmarks per split (Section 4)

| Domain | RL training source(s) (ID source) | OOD benchmark(s) | Source |
|---|---|---|---|
| Math | NuminaMath; ID columns are six sources: synth. math, olympiads, synth. amc, cn_k12, aops, amc_aime | AIME 2024 and AIME 2025 | `txt:1089`, `txt:1101`, `txt:2030`-`txt:2037`, `txt:2379` |
| Code | TACO, CodeContests, Codeforces (ID columns are these three) | LiveCodeBench, reported by Easy, Medium, Hard | `txt:1089`, `txt:1101`, `txt:2384`-`txt:2394`, `txt:2676` |
| Agentic tool calling | ToolRL (ID is held-out ToolRL) | API-Bank, levels 1 to 3 | `txt:1090`, `txt:1102`, `txt:2681`-`txt:2684`, `txt:2906` |
| General reasoning | WebInstruct-verified (mix-RL run) | 400 questions each from MedMCQA, PubMedQA, ChemBench, UGPhysics, OpenScienceReasoning-2 | `txt:1091`, `txt:1103`, `txt:1085`; ID column headers `txt:582`-`txt:590`; OOD column headers `txt:591`-`txt:595` |

- LiveCodeBench version and date window: **not stated.** The only reference is "LiveCodeBench: holistic and contamination free evaluation of large language models for code" (ICLR, arXiv:2403.07974; `txt:1398`-`txt:1404`), cited as "( Jain et al., 2025 )" at `txt:1101`.
- Dataset versions and dates for NuminaMath, TACO, CodeContests, Codeforces, ToolRL, API-Bank, WebInstruct-verified: **not stated** beyond the citations. Hugging Face URLs appear only in references for NuminaMath-CoT (`txt:1475`), OpenScienceReasoning-2 (`txt:1549`), and open-r1 Codeforces (`txt:1570`).
- General-reasoner OOD mapping: the Table 4 OOD column headers are "Phys.", "Bio.", "Med.", "Multi", "Chem." (`txt:591`-`txt:595`). The text does not map these headers to the five OOD sources. Mapping: **not stated**.
- Section 2 benchmarks (Llama-3-8B-Instruct): GSM8K, NuminaMath, APPS-intro, TACO, ARC-Challenge (`txt:106`). Responses sampled "from the training split" (`txt:102`). "We cap the number of training examples at 2,000 per benchmark." (`txt:105`). Sampling temperature and max tokens for Section 2: **not stated**.

### Problems, samples per prompt, splits

- Number of problems per benchmark or per split: **not stated** (no counts appear anywhere in the text or tables).
- Samples per prompt, evaluation: "several samples" (`txt:1104`) and "drawing four responses per prompt" (`txt:2020`). The paper uses four in its Appendix C evaluation block; "several" in Section 4.1 is not reconciled with "four" in the text.
- Samples per prompt, inference-time selection: N = 8 (`txt:1127`; Table 2 caption `txt:355`). Single-sample rows of Table 2 use one response (`txt:355`).
- Samples per prompt, training: 64 rollouts per prompt (Table 7, `txt:2010`-`txt:2011`).
- Train, validation, test: ID is "held-out problems from the RL training sources" (`txt:1100`). Whether the split is "by problem" is implied by "held-out problems" but is not written as "split by problem". Validation split: **not stated**. Sizes of train, held-out, and test splits: **not stated**.
- R-Tuning and Probe labeled set: "disjoint from all RL training and evaluation data" and sized to the corresponding RL training set (`txt:1098`). Size in examples: **not stated**.

### Label suite and grading

- "Correctness is determined by rule-based grading, with truncated responses counted as incorrect." (`txt:2021`).
- Specific graders, test cases, execution-based checking for code: **not stated**. The word "execution" does not appear in the text.
- Section 2: "using the corresponding benchmark-specific grader" (`txt:102`), grader not further described.

### Decoding settings

- Section 4 RL and evaluation: sampling temperature 1.0 and top-p 1.0 (Table 7, `txt:2016`-`txt:2017`). Max prompt tokens 2,048 and max response tokens 16,384 (`txt:2014`-`txt:2015`). Evaluation uses "the same sampling temperature, top- p p , and response-length limit as in training" (`txt:2019`-`txt:2020`).
- Section 2 decoding: **not stated**.
- R-Tuning decoding in Section 4: **not stated** beyond the statement that its samples are drawn at the RL temperature (`txt:1104`), which is inferred to apply to all arms.

## 4. Scoring level, metrics, binning, intervals

- Scoring level: per sample. "every sample is scored with AUROC (AUC), 15-bin ECE and the Brier score." (`txt:1104`).
- Pooling: "Split-level numbers are averages over sub-benchmarks weighted by sample count" (`txt:1104`-`txt:1105`); Table 3 caption: "ID and OOD values are averages over the sub-benchmarks of each split weighted by the number of scored samples" (`txt:578`). The pooled unit is therefore the sample, pooled across prompts within each sub-benchmark and then across sub-benchmarks in each split.
- Within-problem scoring (for example, grouping samples by prompt before computing AUROC): **not stated**.
- AUROC: "We compute AUROC from raw outputs" (`txt:2023`). For the Verbalized and Self-consistency baselines, the raw-output definition is not separately stated.
- ECE: "15 equal-width bins" (`txt:2023`). Section 4.1 says "15-bin ECE" (`txt:1104`). Computed after clipping outputs to [0, 1] (`txt:2023`).
- Brier: "Brier score after clipping outputs to [0, 1]" (`txt:2023`).
- Intervals: **none reported.** No confidence intervals, standard errors, bootstrap, or ± values appear in Tables 2, 3, 4, 5, 6, or 8-10 (checked by search for interval, bootstrap, std, ±). Number of seeds or independent runs: "one run per domain" (`txt:1088`); no seed count stated.
- Metric definitions of Section 2 (AUC, ECE, Brier) cite Naeini et al., 2015 and Brier, 1950 (`txt:117`), without binning details for Section 2.

## 5. R-Tuning details

Section 2 (Llama-3-8B-Instruct; the more detailed description in the text):
- Training data: question-response-correctness triples from the target policy, "using only question–response–correctness triples collected from the target policy" (`txt:96`), capped at 2,000 per benchmark (`txt:105`).
- Labels and appended text: "For a correct response, we append “I am sure” to the response, while for an incorrect response, we append “I am unsure”." (`txt:111`). Appended to "the response" (`txt:110`).
- Labels derive from the target policy's own responses: "it supervises a model with correctness labels derived from the target policy’s own responses" (`txt:109`).
- Loss: "supervised fine-tuning" (`txt:114`); the loss function is not named. Epochs, learning rate, LoRA rank and alpha, batch size: **not stated**.
- Confidence score at inference: "the probability assigned to the confidence token as a continuous confidence score" (`txt:112`). The exact token (for example, the first token of "sure" versus "unsure", or the full phrase), normalization between the two labels, and handling of multi-token phrases: **not stated**.

Section 4 (Qwen3-8B and Nemotron-Cascade-8B):
- Training data: "held-out labeled responses" (`txt:1096`), disjoint from RL data and of the same count as the RL training set (`txt:1098`). Source policy for these responses: **not stated**.
- Labels, loss, epochs, learning rate, LoRA: **not stated** for Section 4. Section 4 says only "fine-tunes the policy". Section 2's LoRA-based SFT (`txt:114`) is not explicitly said to carry over.
- Confidence-token probability and appended-text format in Section 4: **not stated** beyond the phrases "I am sure" and "I am unsure" (`txt:1096`).

## 6. Code and checkpoint release

- Released code: **not stated.** No statement about a code repository, release, or availability was found (search for github, code is, release, available, checkpoint, open-source returned only the HTML page chrome at `txt:4`, `txt:9`, `txt:10`, and the arXiv error-report boilerplate at `txt:2907`-`txt:2939`).
- Released checkpoints or datasets generated by the paper: **not stated.**
- Licensing line: "License: CC BY-NC-SA 4.0" (`txt:60`). This is the paper's license line, not a code or data license.
- arXiv identifier and date as printed: "arXiv:2610.31820v1 [cs.CL] 22 Oct 2026" (`txt:61`).
- Authors as printed: Shujin Wu and Heng Ji, University of Illinois Urbana-Champaign (`txt:63`-`txt:66`).

## 7. Flags and discrepancies

1. Central gap: the paper does not state the generating policy or the scored generations for R-Tuning, Probe, or the labeled sets (Q1, Q2). The inference in Section 1 above is not stated in the text.
2. Dossier sentence not in the paper: the dossier says R-Tuning's arm "is scored on different generations from the probe arm" (dossier line 5). The paper does not say this. The paper's own description (`txt:1104`, `txt:1112`) makes it plausible but does not state it.
3. Sample count inconsistency: "several samples" (`txt:1104`), "four responses per prompt" (`txt:2020`), and N = 8 for selection (`txt:1127`). The four-response count is in the Appendix C evaluation block; the text does not explicitly link it to Table 3.
4. Table 4 OOD column labels ("Phys.", "Bio.", "Med.", "Multi", "Chem.") are not mapped to the five named OOD sources (`txt:1103`).
5. Section 2 and Section 4 models differ; Section 2 is not the same protocol as Section 4 (different base models, different sample caps, and the text reports Table 1 only for Section 2). The dossier's note that Section 2 uses APPS-intro and TACO matches `txt:106`.
6. No intervals, no seeds, no per-problem counts, no LiveCodeBench version or date window, no probe layer, no R-Tuning loss or epochs for Section 4.
7. Table 2's R-Tuning rows vary per model; the 15-of-16 count (`txt:1112`) was checked against Table 2 values and matches (the one exception is Qwen3-8B tool-calling OOD, R-Tuning 59.5 vs Original 59.1, `txt:257` vs `txt:267`).

## 8. Quick reference of key line numbers

- Section 2 setup: `txt:101`-`txt:115`; Table 1: `txt:117`-`txt:183`.
- Section 3 critic definition and CaC: `txt:197`-`txt:235`.
- Section 4.1 Setup: `txt:1086`-`txt:1106`.
- Section 4.2 Results: `txt:1107`-`txt:1125`.
- Section 4.3 Inference-time scaling: `txt:1126`-`txt:1129`.
- Section 4.4 Critic-free RL (Table 5): `txt:1175`-`txt:1178`.
- Section 4.5 Trajectory (Table 6): `txt:1224`-`txt:1232`.
- Limitations: `txt:1275`-`txt:1279`.
- Appendix A (proofs): `txt:1777`-`txt:1954`.
- Appendix C (Model, PPO, Evaluation): `txt:1971`-`txt:2023`.
- Appendix D (per-benchmark Tables 8-10): `txt:2024`-`txt:2906`.
