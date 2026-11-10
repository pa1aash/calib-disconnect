# Decomposition occupancy (wave 6, task A1)

Run date 2026-11-10. Revised after the A6 critic (`docs/s6/parts/critic-A6/FINDINGS.md`). Dispositions are at the end of this file.

**Question.** Has any work decomposed, attributed, reconciled, or audited a gap between an internal confidence readout and an expressed one? More generally, has any work attributed a gap between confidence readouts to these four terms:

- supervision (S);
- difficulty (D);
- label validity (L);
- generation shift (G).

The search covered code and non-code LLM settings from 2023 to November 2026.

**Stop-relevant case.** A full-text paper that attributes or decomposes the probe-versus-stated-confidence gap into several of these terms on shared generations.

## Verdict

**Stop condition not triggered.** No full text found attributes or decomposes the gap between a hidden-state probe and stated confidence into two or more of S, D, L, and G on shared generations, in code or in general domains. The A6 critic concurs.

**The occupancy is narrower than the first draft said.** Several works hold one term each, or a related decomposition, without a stated-confidence gap:

- 2609.33290 holds S, a D-like control, and an unisolated G confound.
- 2605.09502 holds D.
- 2610.22139 (RADAR) holds a risk decomposition without a verbal arm.
- 2605.27752 holds one-axis protocol shifts of a token-versus-verbal gap.
- 2609.04582 holds a recalibration-versus-residual split of a probe-versus-answer gap.

**Cell verdicts:**

| Cell | Verdict |
|---|---|
| Specific estimand: joint attribution of the probe-versus-stated gap on code to S, D, L, and G, with clustered intervals and refit readouts | CLEAN (provisional) |
| Broader idea: varying or splitting a gap between confidence readouts by measurement or protocol choices on fixed answers | NARROW. Closest: 2605.27752 (one-axis shifts, token vs verbal, QA), 2609.04582 (recalibration vs residual, probe vs answer), and RADAR 2610.22139 (risk decomposition, scalar-recalibration-removable term vs residual) |

**The budget language stays exposition only**, as the operator decided. No title or abstract screened through Semantic Scholar bulk search or OpenAlex applies "error budget", "systematics budget", or Shapley attribution to LLM calibration or uncertainty evaluation. Full-text absence of these phrases was not tested:

- no A1a query searched "error budget" or "systematics budget";
- the Shapley query Q12 had a total of 270 and counts for leads only.

No claim of absence is made for full text, and none is needed, because the language is not claimed as novel.

## Instruments (all passed in wave 5)

| Instrument | Use | Record |
|---|---|---|
| arXiv full text, search.arxiv.org | 50 quoted phrases, all HTTP 200. Absence rests on the 39 queries with totals under 150 and every page read. That excludes the lead-only queries (Q04, Q05, Q07, Q09, Q12, Q13, Q28, Q38) and the partial queries (Q24, Q47, Q49). It includes the zero-hit phrases "decompose the calibration gap", "gap between probe and verbalized", "knowing more than it says", and "knowledge-expression gap". 30 full texts were fetched from arxiv.org/html | `docs/s6/parts/occ-A1a/CANDIDATES.md`, `raw/` |
| Semantic Scholar bulk search | 35 boolean queries, all HTTP 200, no 429; titles and abstracts | `docs/s6/parts/occ-A1b/CANDIDATES.md`, `raw/` |
| OpenAlex works search | 30 queries, all HTTP 200; first 100 records by relevance screened, so OpenAlex misses are not evidence of absence | same |

**Recall check:** 7 of 8 known close works surfaced in A1b (2610.34654 did not).

**Remaining gaps:**

- OpenReview-only and OSF-only full texts (G-FT PARTIAL).
- search.arxiv.org is indexed only to about 2026-11-06.
- Two Zenodo records are ABSTRACT-ONLY, because zenodo.org is off the allowlist.
- **Six A1a full texts screened by title and abstract only** (F17), none an occupant:
  - 2604.06613, "The Detection-Extraction Gap";
  - 2609.03436, "It's the Problem, Not the Path" (Bulut; difficulty confounds in reasoning trajectories, already in the vault);
  - 2610.36709, token confidence measures chain length;
  - 2610.01006, black-box decision-model audit;
  - 2604.10495, uncertainty sources;
  - 2608.18719, skill-document optimization.

## Closest works (full text unless marked)

| Work | Readouts | Terms varied | Shared generations | Why it is not the stop case |
|---|---|---|---|---|
| 2605.27752, Kim and Kang, "Same Answer, Different Confidence: Protocol Sensitivity in Measuring LLM Confidence" (v1 2026-05-26, v4 2026-10-23) | verbalized vs token probability; no probe | Compares one-axis shifts of the verbal-minus-token gap across scoring context, correctness rule (L-like), token aggregation, and ECE estimator (Sec 4.4, Table 4). Recalibration transfer with isotonic and Platt maps (App G, S-like). A targeted review of 12 published comparisons (App J). The supplied-answer probe "measures the level of verbalized confidence, not the gap", and the paper does "not attribute the shift to any single prompt element" | yes: "we fix each answer, its verbalized confidence, and its correctness label" (Abstract) | No probe; no difficulty term; no trained readout; no joint attribution; QA, not code; no execution labels |
| 2609.04582, "When Do Internal Probes Beat Reading the Answer? Miscalibrated Readouts and Behavior-Concealed Knowledge" (2026-09) | probe vs logit margin vs the expressed YES/NO verdict on a supplied candidate | S: a one-parameter bias correction and few-shot recentering against a trained probe. The gap is split into a threshold-offset part and a residual "concealment" part ("The residual gap", Table 3). D and L appear only in the separate open-generation audit, in running text under "Generation: Why the Controls Matter" (txt:427-429) | yes, for the verification ladder | The expressed side is the verdict, not stated confidence; D and L are not applied to the decomposition; no G; synthetic verification tasks. The design follows its nested layer selection inside folds |
| 2610.22139, RADAR, "Are You Sure Your LLM Is Sure? Repairing and Auditing Confidence" (2026-10-15) | likelihood and fixed-choice scores; probes as repair anchors | Squared risk split into "outcome noise, information hidden by the score, and mapping error; only the last term can be corrected by scalar recalibration" (Sec 3, Theorem 3.1); probe-anchored isotonic repair; a prompt-clustered test | yes ("fixed realized answers") | No verbal arm, no D/L/G attribution; non-code. Its split into a recalibration-removable part and a residual is the theoretical content of the budget's residual-gap test |
| 2609.33290, "Calibration, Not Answer Selection: Distilling Internal Confidence in Reasoning Models" (2026-09) | probe vs verbalized, isotonic and Platt recalibrated verbalized, probe-distilled verbalized (trained) | S (raw, recalibrated, trained readouts); D-like (an empirical-accuracy teacher, txt:549, 810-812); G as an unisolated confound: trained students are "evaluated with 10 samples per question" while "Verbal, Answer Probability, and post-hoc recalibration use one generation of the original model" (txt:571-575), and "The frozen Probe scores the original model's sampled answers rather than the student's outputs" (txt:3448) | partly: baseline arms yes; trained arm on its own fresh generations | No attribution; G is confounded, not isolated; non-code. It is the clearest published instance of the confound the budget's G term isolates |
| 2606.29490, "Reported Confidence in LLMs Tracks Commitment More Than Correctness" (2026-06-28) | verbalized vs calibrated log-prob vs activation probes | Two-way ANOVA (partial eta squared); verbal confidence residualized on calibrated log-prob, correctness, and item difficulty | yes, within model | Variance partition of verbal confidence, not of a probe-versus-stated discrimination gap; S fixed; no L, no G; non-code |
| 2605.09502, "Hidden Error Awareness in Chain-of-Thought Reasoning" (posted 2026-05-10T12:26Z, on the concurrency boundary) | probe vs verbalized vs a text-surface classifier | D: within-problem difficulty control (Table 3); text-surface baseline | yes (same traces) | Single term (D); non-code |
| 2610.25846, "Measurement Validity and Representation Dynamics of Confidence Signals in LLMs" (2026-10-19) | verbalized vs a prefill probe that predicts "the median-split semantic-entropy label" (txt:211), not correctness, vs semantic entropy | D: the probe "does not beat" a prompt-only TF-IDF baseline in most retrieval cells (txt:466, 597); a human grading-validity gate (L as an audit); Murphy decomposition of Brier | yes | Audit gates; the probe target is not correctness; no attribution; non-code |
| 2610.27455, "Detecting Errors in LLM Responses: The Incremental Predictive Value of Hidden States" (2026-10) | hidden states vs generation, sampling, and prompt-context feature blocks | Block-removal attribution of the hidden-state gain (Sec 5.2); the prompt-context block is an input-only baseline (D-like) | yes | Attribution to feature blocks, not to S, L, or G; no stated-confidence gap |
| 2608.07528, "The Knowing-Saying Gap" (2026-07-21); 2608.08791, "Unsure but Certain" (diffusion LMs); 2607.22034, small VLMs | probe or token vs stated | One term each: D-like matched design (2608.07528); S by recalibration (2608.08791, 2607.22034) | yes | Single term |
| 2609.20541, "An Analysis of Training-Free Self-Reported Confidence in LMs" | verbalized, P(True), agreement | L: a benchmark-error audit changes the conclusion (Sec 5.5); re-elicitation on fixed answers (Sec 5.3) | yes | No probe; no decomposition |
| Gekhman et al. 2503.15299; Orgad et al. 2410.02707 | hidden-state vs token-probability scoring of candidates | D by within-question definition (Gekhman) | yes | They measure the internal-versus-external gap; they do not decompose it |
| "The Propagation Gap" (Zenodo 10.5281/zenodo.19122015, 2026-03-20) | probe vs logit features vs verbalized | probe-minus-output AUROC gap; surface-form controls | unknown | ABSTRACT-ONLY |
| Cacioli (2026), "Making LLMs Say What They Know: Probe-Targeted Fine-Tuning for Verbal Confidence Calibration" (Zenodo 10.5281/zenodo.20436840; author as cited in 2609.33290 txt:288, 1076-1079) | probe vs trained verbal | S (a trained verbal readout targeted at the probe) | unknown | ABSTRACT-ONLY |

**Single-term works on D:**

- 2605.09502, 2608.07528, 2609.36461, 2610.05572, and 2610.07354.
- On code: 2606.14530 (prompt-length residualization of a pre-generation probe) and 2608.08266 (robustness follow-up to Ribeiro). No new effect.

## Effects on the design

1. **Cite 2605.27752** wherever the paper says that a confidence-readout comparison moves with measurement choices on fixed answers. That covers the estimator sensitivity analysis and the reconciliation table.
   - Differentiation: a probe readout; trained readouts as in 2610.31820 and CREDO; difficulty terms as in Campos and Ribeiro; the generation-shift term; joint Shapley attribution with clustered intervals; and execution labels on code.
2. **Cite RADAR (2610.22139) and 2609.04582** for any split of a gap into a part removable by scalar recalibration and a residual.
   - The budget's isotonic toggle and residual-gap test are an application of that idea to the probe-versus-stated gap.
   - It is not claimed as a new decomposition.
3. **Cite 2609.33290** where the generation-shift term is motivated. It scores a trained stated readout on the student's fresh generations against a probe on the original model's generations, which is the confound the G term isolates.
   - 2610.31820 has the same unresolved question (`R2610_31820_PROTOCOL.md`).
4. **Cite 2610.25846 and 2605.09502** for prompt-only or text-surface baselines and within-problem difficulty controls outside code. Campos stays the citation for the prompt-only baseline on code.
5. **No change to the operator's spine.** The residual-gap test stays the primary test.
6. **Differential.** These works enter `DIFFERENTIAL_R1.md`, where the row 13 notes cite 2609.33290.

## Disposition of the A6 critic findings on this file

| Finding | Disposition |
|---|---|
| F1 | Accepted. 2609.33290 is recoded as S, D-like, and confounded G; Effects item 3 added |
| F2 | Accepted. 2605.09502 added with its boundary date; 2608.07528 added to the D list |
| F3 | Accepted. RADAR row expanded; Effects item 2 added |
| F4 | Accepted. Claim restricted to titles and abstracts |
| F8 | Accepted. Location corrected to running text |
| F14 | Accepted. "Compares one-axis shifts", with both caveats quoted |
| F16 | Accepted. 2610.25846 wording corrected |
| F17 | Accepted. The six texts screened by title and abstract; listed under gaps |
| F18 | Accepted. Query list made explicit |
| F22 (A1 line) | Accepted. Effects item 1 now cites Ribeiro, Campos, 2610.31820, and CREDO |
| F23 | Accepted. Author added; ABSTRACT-ONLY kept |
