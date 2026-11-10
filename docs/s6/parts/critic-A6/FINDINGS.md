# Critic A6: wave 6 Part A findings

Saved by the orchestrator from the critic's returned text, because the harness blocked the critic's own write (same procedure as waves 4 and 5). The content is the critic's return, lightly reformatted as markdown. Paths are relative to `research/positioning/` or `docs/s6/parts/` as written by the critic.

**Stop-condition verdict: NOT TRIGGERED (concur), but the occupancy is narrower than DECOMPOSITION_OCCUPANCY.md states.** 2605.27752 has no probe. In 2609.04582 the expressed side is a YES/NO verdict on a supplied candidate, not stated confidence. 2609.33290, 2605.09502, and 2610.22139 each hold one term, or a related decomposition, without a stated-confidence gap. F1 to F5 change the citations and the differentiation that the verdict depends on.

**F1 (major, verified). 2609.33290 is not "S only".**
- **Location:** w6/DECOMPOSITION_OCCUPANCY.md:54 and occ-A1a/CANDIDATES.md:76.
- **Evidence:**
  - Students are "evaluated with 10 samples per question", while "Verbal, Answer Probability, and post-hoc recalibration use one generation of the original model" (occ-A1a/raw/ft/2609.33290.txt:571-575).
  - "The frozen Probe scores the original model's sampled answers rather than the student's outputs" (txt:3448). So a trained stated readout on its own fresh generations is compared with a frozen probe and with isotonic and Platt verbal readouts on the original generations: G is present as an unisolated confound.
  - EA-SD uses "the question's empirical accuracy" as its teacher (txt:549, 810-812), a D-like control.
- **Fix:** recode as S, D-like, and confounded G. Add it to row 13 of the differential and cite it where G is motivated.

**F2 (major, verified). 2605.09502 is missing from the A1 synthesis.**
- **Location:** DECOMPOSITION_OCCUPANCY.md:45-64.
- **Evidence:**
  - occ-A1b/CANDIDATES.md:94 lists it as FULL TEXT: probe vs verbalized vs a text-surface classifier, with a "Within-problem difficulty control" (raw/fulltext/2605.09502.html:623-627, 667).
  - Published 2026-05-10T12:26:46Z (raw/arxiv_abs.xml:251), right on the concurrency boundary used at DIFFERENTIAL_R1.md:86.
  - 2608.07528 is also missing from the D list at :64.
- **Fix:** add it as a single-term D occupant and settle its concurrency status explicitly.

**F3 (major, verified). RADAR (2610.22139) is underplayed.**
- **Location:** DECOMPOSITION_OCCUPANCY.md:52 and :66-78.
- **Evidence:** RADAR decomposes risk into "outcome noise, information hidden by the score, and mapping error; only the last term can be corrected by scalar recalibration" (2610.22139.html:459-463). It uses probe anchors (:403-406), a prompt-clustered test (:408-410), and "fixed realized answers" (:633). This is the theoretical content of the residual-gap test.
- **Fix:** add an Effects item citing RADAR for any split into a recalibration-removable part and a residual.

**F4 (major, verified). The full-text absence of "error budget" and Shapley is claimed without a valid instrument.**
- **Location:** DECOMPOSITION_OCCUPANCY.md:27.
- **Evidence:**
  - No A1a query searches "error budget" or "systematics budget" (occ-A1a/CANDIDATES.md:11-60).
  - Q12 (Shapley) had total 270 with 100 read, so it is a lead source only (:22).
  - A1b screened titles and abstracts only (occ-A1b/CANDIDATES.md:105).
- **Fix:** restrict the claim to titles and abstracts, or run quoted full-text queries with totals under 150.

**F5 (major, verified). A2 overstates the "own new outputs" inference.**
- **Location:** R2610_31820_PROTOCOL.md:9-15 and :40.
- **Evidence:**
  - R-Tuning appends a statement to a response and reads the confidence-token probability (w5/.../2610.31820.txt:110-112).
  - In Sec 2, R-Tuned external estimators score the target policy's fixed responses "as text" (txt:113-115), a trained readout on frozen generations.
  - Table 2 accuracy (txt:251-270) shows that the fine-tuned model generated outputs, but not which responses the Table 3 confidence was read on. txt:1104 does not name the answering model.
- **Fix:** present two readings (own fresh outputs, or teacher-forced on the RL policy's samples), mark the question unresolved, and reproduce under both.

**F6 (major, verified). "A (dossier)" basis for rows 13 to 17.**
- **Location:** DIFFERENTIAL_R1.md:44 and :62-66.
- **Evidence:**
  - Ribeiro explicitly scores one probe readout on other-model candidates (RQ1) and on self-generated candidates (RQ2) (w5/parts/dossier-A5/raw/2512.07404v3.txt:1427-1431).
  - W5 defines "absent" as "searched for and not found" (w5/DIFFERENTIAL.md:5); rows 13 to 17 were not searched.
  - Spiess and NeuroSym have no dossier.
- **Fix:** recode Ribeiro row 13 as Pa. Search the full texts for rows 13 to 17, or mark those cells "not assessed".

**F7 (major, verified). 2609.04582 row 5 "n.a. (one trial per item)" is false.**
- **Location:** DIFFERENTIAL_R1.md:54.
- **Evidence:** "Each instance yields a gold-YES trial ... and gold-NO foils" (txt:173); the foils use matched words (txt:119, 177).
- **Fix:** code it A or Pa.

**F8 (minor).** "Table 4" is cited for 2609.04582's generation audit, but Table 4 is the ladder table (txt:425). The audit is in running text at txt:427-429.
- **Locations:** A1:50, A5:52, A1a:74.

**F9 (minor).** 2609.04582 row 11 should be Pa, not A. Table 3 reports Qwen3-0.6B "+ extended reasoning" 0.902 against a probe at 0.898 (txt:332-367).

**F10 (minor).** 2609.04582 row 4 should also cite the verification design's own text-only controls: the lexical baseline (0.76), "text-only bounds", and the candidate-only control at 0.500 (txt:248, 250, 383).

**F11 (minor).** Supervision coding is inconsistent with the W5 precedent.
- W5 coded Spiess (Platt rescaling as the only supervised arm) as row 1 Pa and row 2 A.
- MARGIN is coded the opposite way: row 1 A and row 2 Pa (2605.22949.txt:527-528).
- 2605.27752 fits isotonic and Platt maps (html:3005-3014) but is row 1 A.
- **Fix:** MARGIN row 1 Pa and row 2 A; 2605.27752 row 1 Pa.

**F12 (minor).** MARGIN row 6 "P" contradicts A3's own finding of no matched raw values on the original suite (MARGIN_COVERAGE.md:20; txt:643-668 vs 690-714). Code it Pa.

**F13 (minor).** MARGIN row 5 should be Pa: cold-start pairwise resolution is within-task (txt:567-570).

**F14 (minor).** The 2605.27752 "G-like" arm does not measure the gap.
- **Evidence:** the supplied-answer probe "measures the level of verbalized confidence, not the gap" (html:470-472); the paper does "not attribute the shift to any single prompt element" (:1380-1381).
- **Fix:** add these caveats, and replace "Attributes shifts" at A1:49 with "compares one-axis shifts".

**F15 (minor).** DIFFERENTIAL_R1.md:86 says every supplementary column is concurrent (first posted after 2026-05-10). RLCM (arXiv 2604.23333, an April 2026 ID) is not.

**F16 (minor).** In 2610.25846 the probe predicts "the median-split semantic-entropy label" (txt:211), not correctness, and it "does not beat" TF-IDF (:466, :597), which is not "matches".
- **Locations:** A1:53 and :74-75.

**F17 (minor).** A1a fetched six full texts that it never dispositions: 2604.06613, 2609.03436, 2610.36709, 2610.01006, 2604.10495, and 2608.18719. A spot-check of two abstracts shows no occupant, but they were not fully screened.

**F18 (minor).** A1a:126 lists "Q39-Q50" as absence evidence, which includes the partial queries Q47 and Q49. A1's count of 39 is right only once those are excluded.

**F19 (minor, verified).** The MARGIN count flag resolves: 1,467 = 9 x 163 and 2,016 = 9 x 224 (txt:476-477). The flag compared against the source-phase columns, the wrong denominator.
- **Locations:** MARGIN_COVERAGE.md:47 and margin-A3/MARGIN.md:92.

**F20 (minor).** CLOSED_ITEMS should add two notes: the Miglani AUC uses "sorted ranks without explicit tie averaging" (2609.36783.txt:488), and the Qwen2.5-Coder model size is not stated. All other A4 quotes check out.

**F21 (minor, not located).** `docs/s6/PIPELINE_DESIGN_R1.md` and "design section" references point to a file not yet written.
- **Locations:** DIFFERENTIAL_R1.md:7, R2610_31820_PROTOCOL.md:15 and :50, CLOSED_ITEMS.md:17.

**F22 (minor).** Sentences that describe existing work without citing it. These citations are needed before any such sentence enters the paper.
- MARGIN_COVERAGE.md:36 needs Ribeiro.
- MARGIN_COVERAGE.md:38 needs Campos.
- MARGIN_COVERAGE.md:39 needs 2610.31820 and 2609.33290.
- A1:70 needs Ribeiro, Campos, and 2610.31820.

**F23 (minor).** The ABSTRACT-ONLY Zenodo entry "Making LLMs Say What They Know" is Cacioli (2026), as cited and described in 2609.33290.txt:288 and :1076-1079. Add the author and keep ABSTRACT-ONLY.

**Spot-checks with no finding:**
- 2610.31820: Table 3 code AUROCs and the 15 of 16 accuracy drops.
- 2605.22949: MARGIN Table 3 values.
- 2605.27752: abstract quote, App J review of 12, paired bootstrap.
- 2606.29490: per-signal ANOVA.
- 2609.04582: nested layer selection and the residual-gap passage.
