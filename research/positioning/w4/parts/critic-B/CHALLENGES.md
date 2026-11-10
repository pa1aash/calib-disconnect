# Critic B challenges to OCCUPIED verdicts (W4 step 6)

Run date 2026-11-10. Scope: every OCCUPIED and OCCUPIED (union) verdict in
`research/positioning/w4/VERDICTS.md`. Method: read each cited dossier, then the decisive sections
of the occupant's full text in `research/notes/` (NeuroSym-Cal from
`parts/dossier-D4/raw/neurosym.txt`). No new fetches were made, so there is no `raw/` folder.
A21 tests: condition 1 (factor, granularity, label protocol, or use, not only new models or
benchmarks); condition 2 (a stated, concrete reason why the code result could differ).

## Summary

| Verdict | Proposed | Note |
|---|---|---|
| L1 Q1 (union) | keep OCCUPIED (union) | union holds; add 2605.28500 and 2512.24560 as backups; Campos sampling is problem level only |
| L1 Q6 (token level) | keep OCCUPIED (token level) | Gros Tables 3-4 already cover all four families at line and token level |
| L1 Q7, Q8 | keep OCCUPIED for existence; second half of Q7 is partly occupied by 2605.09023 Table 6 | this weakens L1 Q4's NARROW residual for the sampling family |
| L1 Q9 | keep OCCUPIED | none |
| L1 Q11 (token likelihood) | keep OCCUPIED | none |
| L1 Q12 | keep OCCUPIED | 2610.11300's judge is external, not self |
| L2 Q1 | relabel OCCUPIED (union); keep the headline taken | it needs two works; misread of Ribeiro RQ2 in Q1c; Gros is a single-work, line-level occupant |
| L2 Q3 (within verbal) | keep OCCUPIED, label (union) | needs Tuerlings plus Ribeiro or 2605.28500 for P(True) |
| L2 Q5, Q6, Q7 | keep OCCUPIED | Q6 "beats likelihood out of distribution" is only weakly covered |
| L3 Q3 | keep OCCUPIED for single-shot code; record that it does not subsume L3 Q1 | the brief asks about code agents and the occupants are not agents |
| L3 Q6 (union) | keep OCCUPIED (plain, not union) | any one work suffices; Kaddour 2602.06948 covers verbal at task level |
| L4 Q4 | keep OCCUPIED | dossier misread: Gros's Qwen Probe-7B reads the generator's own states |
| F Q1 | keep split verdict | none |
| F Q2 (union) | keep OCCUPIED (union) with a caveat | Ghosh's probe predicts semantic entropy, not correctness; the "internal reference" part rests on algebra, not on an instantiation |
| F Q3 (effective) | keep OCCUPIED | possible code residual (execution-verified rewrites); condition 2 is borderline |
| F Q4 | keep OCCUPIED | the residual collapses into L2 Q1 |

No OCCUPIED verdict moves to NARROW on this review. Three verdicts need relabeling or a status
fix, and two dossiers misread their occupant (listed at the end).

## L1 Q1. Four or more families against execution labels: OCCUPIED (union)

- **What the full texts show.**
  - NeuroSym-Cal (Sec 4.2 and Table 1) reports AvgLogit-Code and Platt (token), P-True ("We prompt
    the model to verbally estimate the probability that its generated solution is correct"), SC
    with K=10 (sampling), and IGLB, scored by ECE, Brier, and AUROC on 3 models and 3 benchmarks.
    Its 0 to 100 self-verification score (Sec 3.2) appears only inside the fused method and in the
    "w/o Extrinsic" ablation (Table 2). The stated-confidence family is covered by P-True.
  - Campos 2611.07876 (Sec IV, Table II) reports Yes-token confidence, EigenScore, linear probe and
    LAT, and DAS predictors. EigenScore "scores a problem rather than a candidate and does not rank
    the candidates of one problem" (method section). The probe-versus-sampling comparison is
    therefore problem level only.
- **Backup occupants not cited in VERDICTS.**
  - Functional Entropy 2605.28500 (Sec 4.1) covers token, sampling, P(True), and six-level
    verbalized readouts with AUROC, Brier, and ECE.
  - Gros and Devanbu 2512.24560 (Tables 3-4) compare token probability, multisampling, line
    verbalized, and probes on the same generations with BSS, ECE, and AUC. Its labels come from
    test-validated minimal patches, at line and token level. Problem-level results appear only
    averaged inside the probe-design ablation (Table 6).
- **Narrowest residual tried.** Candidate-level (not problem-level) sampling agreement against a
  probe and stated confidence at program level on identical generations. Closest work: Campos
  (problem-level sampling) and Gros (all four families, line level).
- **A21.** Condition 1 passes (granularity). Condition 2 fails: I found no concrete reason why
  per-candidate agreement would rank differently on code than in NLP. Per-candidate functional
  cluster share already exists in 2603.27098 and Code-MUE for the sampling family alone. This
  residual is already carried by the L2 Q13 NARROW verdict ("per-candidate sampling readouts").
- **Union check.** It holds. Every family is covered by at most two works (NeuroSym-Cal plus
  Campos, or 2605.28500 plus Campos). What remains is running them on the same problems, together
  with the protocol controls that L1 already carries as NARROW. If the operator rules concurrent
  works out (Campos and 2605.28500 are both concurrent), the probe side falls back to Gros, which is
  line level only. L1 Q1 would then become NARROW, with the residual "four families at program
  level". VERDICTS already predicts this result.
- **Proposed verdict:** keep OCCUPIED (union). Add 2605.28500 as an alternative stated-confidence
  source, and record that Campos's sampling family is problem level.

## L1 Q6. Calibration versus discrimination, recalibration as a control: OCCUPIED (token level)

- **Full text.** 2610.11300 Sec 6.1 and Table 5: Platt and isotonic recalibration with five-fold
  cross-validation. On BigCodeBench, CodeLlama's Brier score falls from 0.856 to 0.061 while BSS
  stays near 0.001. The finding is stated as: "calibration primarily corrects the scale of the
  uncertainty scores rather than providing substantial predictive information". This is the
  mapping-versus-information separation. Gros Tables 3-4 report unscaled and Platt-scaled BSS and
  ECE for token, multisampling, verbalized, and probe readouts at line and token level.
- **Narrowest residual.** Recalibration as a control across all four families at program level,
  which VERDICTS already states. Closest work: 2610.11300 (token, program level) and Gros (four
  families, line level).
- **A21.** Condition 1 passes (granularity). Condition 2 belongs to Critic A, because it bears on
  the NARROW half of the verdict.
- **Proposed verdict:** keep OCCUPIED for the token level. Make the across-families half explicit:
  it is OCCUPIED at line and token level by Gros, and NARROW only at program level.

## L1 Q7 and Q8. Test-free agreement; semantic entropy with execution or symbolic clustering: OCCUPIED

- **Full text.**
  - Sharma and David 2502.11620 uses symbolic-execution clustering (Sec 4).
  - Code-MUE uses execution graphs over generated inputs that "are not used to decide whether a
    program is correct".
  - 2603.27098 uses ESE, with clustering tests generated by Qwen3-Coder-30B and labels from
    official tests (Sec 5.1-5.2).
  - 2605.28500 uses LLM-judged functional-equivalence clustering.
  - 2605.09023 uses fuzz-input behavioral clustering.
- **Q7 has a second half:** "How do they compare with test-pass agreement under the same labels?"
  2605.09023 (Sec 4.5, Table 6) answers it in part for the sampling family. Fuzzing seeded with
  benchmark-provided test inputs gives a higher AUROC than a seed-free variant that "never reads
  benchmark-provided test cases, expected outputs, or reference implementations". The drop is 0.014
  to 0.087 (for example, HumanEval-X C++ SDE 0.796 to 0.709; LiveCodeBench DSDE 0.844 to 0.787,
  GPT-4o-mini). This is a measured effect of label-source overlap on an agreement score.
- **Narrowest residual.** Whether reusing the benchmark's oracle inside a confidence method changes
  the method ranking across families, not just the AUROC of one family. Closest work: 2605.09023
  Table 6 (one family, seeding only) and Liu 2609.25938 (oracle choice, text-to-SQL).
- **A21.** Condition 1 passes (label protocol). Condition 2 passes: hidden tests both define the
  label and can feed test-based agreement, a coupling with no NLI-clustering analogue.
- **Proposed verdict:** keep OCCUPIED for Q7 and Q8 as existence claims. Pass to the orchestrator:
  2605.09023 Table 6 belongs in L1 Q4's evidence, and Q4's residual should be worded as a
  cross-family ranking change, because a single-family label-overlap effect is already measured.

## L1 Q9. Release-window benchmarks used for calibration: OCCUPIED

- **Full text.**
  - Tuerlings (Sec 3.1) uses 365 LiveCodeBench v6 problems in one post-cutoff window with ECE and
    AUROC.
  - NeuroSym-Cal (Sec 4.1) holds out a post-cutoff LiveCodeBench subset per model.
  - 2512.08810 uses LiveCodeBench v6 for calibration as a leakage mitigation.
- **Residual.** None beyond Q3 and Q13, which VERDICTS already carries.
- **Proposed verdict:** keep OCCUPIED.

## L1 Q11. Subgroup calibration; multicalibration: OCCUPIED (token likelihood)

- **Full text.** 2512.08810 (Sections 4-6, Table 1) multicalibrates avg_prob, code_prob, and
  tail_prob over complexity, length, and language groups. NeuroSym-Cal reuses IGLB as a baseline
  with groups for cyclomatic complexity and length (Sec 4.2).
- **Residual.** Release window as a subgroup is not in 2512.08810. That residual is the same as
  Q3 and Q13 and needs no separate entry.
- **Proposed verdict:** keep.

## L1 Q12. Self-judgment or judge score as confidence: OCCUPIED

- **Full text.**
  - 2610.11300 (Sec 3) defines judge-based signals as "an external model", so it is not
    self-judgment.
  - NeuroSym-Cal's self-verification is a self-judgment on a 0 to 100 scale (Sec 3.2), as is
    P-True.
  - OPENIA uses a zero-shot LLM-as-judge.
  - AutoProbe (Table 5) separates in-house (self) from external judges, with accuracy 0.32 to 0.61
    versus 0.93 to 0.97.
- **Residual.** Self versus external judge as a factor. It is occupied by AutoProbe at whole
  solution, with accuracy only.
- **Proposed verdict:** keep OCCUPIED. Correct the evidence line: 2610.11300 counts as a judge
  score, not a self-judgment.

## L2 Q1. Probe versus stated, token, and sampling readouts, uncontrolled: OCCUPIED

- **Full text, Ribeiro 2512.07404.**
  - RQ1 (Sec 4.1.1) uses incorrect candidates from other models: Llama-3.3-70B, GPT-4o, and Gemini
    2.0 Flash on BCB; Llama-3.2-3B, Gemma-3-1B, and Granite-3.3-2B on HE.
  - LAT beats Reflective selection accuracy by +13.3 to +29.0 pp on BCB and +8.7 to +26.2 pp on HE
    (Sec 4.2.1).
  - RQ2 (Sec 5.1-5.2) ranks each model's own 10 samples at temperature 1.0 within each task: "The
    goal is to assess each model's ability to rank its own outputs". It compares LAT with
    Random, Intrinsic, Reflective, and RankEF. The result: "LAT shows superior or comparable
    accuracy to all baselines ... Only a few comparisons reached statistical significance", and on
    one benchmark "CodeLlama benefits most from its Intrinsic metric (39.7%)".
- **Full text, Campos.** It adds problem-level EigenScore and AUROC, with no verbal numeric
  readout.
- **Full text, Gros 2512.24560 (Table 4, Qwen2.5-Coder-7B, line level).** All four families run on
  the same self-generated code. Line AUC is 0.55 for token probability, 0.72 for multisampling,
  0.71 for line verbalized, and 0.83 for Probe-7B. Scaled BSS is 0.33 for the probe and 0.10 for
  verbalized. Probe-7B reads the 7B model under test itself (method text: "a probe of the
  embeddings from the 7B-parameter MUT").
- **Labeling issue.** The verdict needs two works: Ribeiro for verbal and likelihood, Campos for
  sampling. Under R1 section 4 that makes it OCCUPIED (union), not OCCUPIED. The union holds: what
  remains is co-running them, and Gros already co-runs all four families at line level.
- **Narrowest residual.** Probe versus stated confidence on self-generated code with
  per-candidate discrimination metrics at program level. Closest work: Ribeiro RQ2 (self samples,
  within task, ranking only, mostly not significant) and Gros (self samples, line level).
- **A21.** Condition 1 passes (label protocol and granularity). Condition 2 passes, but only for
  the controlled version: RQ1's incorrect class comes from other models, so a probe can separate
  authorship or style rather than correctness, a confound specific to cross-model code
  candidates. This residual is the one L2 Q1c already holds.
- **Proposed verdict:** relabel as OCCUPIED (union): Ribeiro plus Campos, with Gros as the line-level
  single-work occupant. The headline remains taken.
- **Misread (bears on Q1c).** VERDICTS Q1c describes Ribeiro's protocol only as "correct class is
  the human reference, incorrect class is other models' failures, Sec 4.1.1". That omits RQ2, which
  is a self-generated, within-problem probe-versus-verbal comparison. RQ2 should be added to the
  "only within-problem code comparisons tie" list beside Campos and Miglani. It supports the
  verdict, but Q1c's residual must be stated as "supervision-matched and with AUROC and
  calibration", not "self-generated and within problem" alone.

## L2 Q3. Elicitation format as a factor: OCCUPIED (within verbal, on code)

- **Full text.**
  - Tuerlings (Sec 3.3, Table 1) compares Direct, Chain-of-Thought, and Linguistic formats on 6
    models.
  - Ribeiro compares 7-level and True/False (Mistral HE 40.6% versus 15.3%).
  - 2605.28500 has P(True) and a six-level Likert scale.
  - NeuroSym-Cal compares P-True with 0 to 100 self-verification as a judge-style post-hoc rating.
  - The brief's four formats (numeric, category, yes/no token probability, post-hoc critique) are
    covered by three works together.
- **Residual.** Format by readout family, which VERDICTS already holds as NARROW.
- **Proposed verdict:** keep OCCUPIED, labeled (union).

## L2 Q5, Q6, Q7. Probes for code correctness; transfer; other white-box readouts: OCCUPIED

- **Full text.**
  - Q5: OPENIA (last token, last layer, three families), AutoProbe (learned layer and position
    weights), 2606.14530 (pre-generation), and Klassert 2609.13975 (positions varied).
  - Q6: OPENIA's cross-benchmark and cross-language tests against LLM-Check, which includes "output
    prediction probabilities"; AutoProbe trains on MBPP and tests on HumanEval; Campos Table II
    under language shift (Qwen3-Coder probe ID .761, shift .668, versus confidence .644 and .643).
  - Q7: 2510.02917 (SAE features and steering) and AutoProbe (attention weighting).
- **Weak spot.** Q6's sub-question asks whether the probe beats sequence likelihood and sampling
  agreement out of distribution. Campos's out-of-distribution sampling comparison is problem level
  only, and its "confidence" is a Yes-token probability, not sequence likelihood. Only OPENIA (via
  LLM-Check) has a likelihood-type baseline under transfer. The sub-question is answered only
  thinly.
- **Residual.** Out-of-distribution probe versus sequence likelihood and per-candidate agreement.
  Condition 1 fails: it is a change of benchmarks.
- **Proposed verdict:** keep OCCUPIED.

## L3 Q3. Selective prediction with coverage and risk on code: OCCUPIED

- **Full text.**
  - CodeRefuser (Sec 3-4, Figs 2-3) gives the admission-risk distribution at alpha 0.10 to 0.25
    and the abstention rate, with abstention precision and F1. The selector is execution-cluster
    agreement over generated tests.
  - 2505.13553 (Table 1) bounds FDR-CE with a likelihood score.
  - 2605.19369 (Sec 4.1) reports one point: "over 70%" accuracy at 80% coverage on MBPP+.
  - Also relevant: NeuroSym-Cal (Sec 5.2, Fig 3) has risk-coverage curves and AURC on
    LiveCodeBench.
- **Scope issue.** Brief L3 Q3 asks whether selective-prediction or verifier-routing papers "for
  code agents" report coverage-risk curves "that subsume this", meaning L3 routing. None of the
  cited occupants is an agent, and none evaluates budget routing against random and oracle arms.
  They therefore do not subsume L3 Q1, which VERDICTS correctly keeps NARROW.
- **Narrowest residual.** Selective prediction gated by stated or probe confidence on code. Closest
  work: NeuroSym-Cal (fused score, and P-True only as a calibration baseline) and 2610.11300
  (token-based selective generation).
- **A21.** Condition 1 passes (readout family as a factor within a use). Condition 2 passes:
  verbal confidence on code is anti-informative in fetched work. Tuerlings reports "All eighteen
  strict-scoring NCE point estimates are negative", and Ribeiro reports that Reflective ranking is
  "often doing worse than Random". A verbal-gated selector on code could therefore fall below
  random, unlike the NLP case.
- **Proposed verdict:** keep OCCUPIED for "selective prediction with coverage and risk on
  single-shot code". Fold the residual into L3 Q1, where it is already stated. State in VERDICTS
  that the answer to the brief's literal question (do they subsume L3?) is no.

## L3 Q6. Uncertainty or abstention for repository agents: OCCUPIED (union)

- **Full text.**
  - Kaddour et al. 2602.06948 elicits verbal success probabilities before, during, and after
    execution on 100 SWE-bench Pro tasks for GPT-5.2-Codex, Gemini-3-Pro, and Opus 4.5 ("predict
    73% success against a true rate of 35%").
  - SWE-Verifier works at the step unit, 2611.08285 at the run unit, and 2610.05572 and 2607.05188
    probe agent hidden states.
- **Union check.** Q6 is an existence and unit question, and any one work answers it. The "(union)"
  label is not needed: Kaddour alone makes the claim for the agent's own stated confidence, and
  the others add units.
- **Residual.** None that passes condition 1. The unit (task, step, run) is already covered.
- **Proposed verdict:** keep OCCUPIED. Drop "(union)" and add Kaddour as the primary occupant.

## L4 Q4. Line, token, edit, or step localization: OCCUPIED

- **Full text.**
  - Gros Tables 3-4 report line and token BSS, ECE, and AUC for four families, with labels from
    test-validated minimal patches.
  - FLARE Table 2 reports line-targeted refinement and "67% Top-1" localization.
  - 2607.05188 Sec 4.1 reports step probes (AUC up to 0.83).
  - PtTrust Table 2 reports Top-K line localization, where Defects4J Top-3 0.479 loses to token
    uncertainty at 0.499.
- **Residual.** Localization by test group (Q1), which is already NARROW. Gros's labels are edit
  locations, not failing requirements.
- **Misread.** Dossier 2512.24560 says "Probes read a separate supervisor model, not the
  generator's own states". That is true for GPT-4o. For the Qwen2.5-Coder-7B generator, Probe-7B
  reads the generator's own embeddings (method text on the 7B MUT). This strengthens both L4 Q4 and
  the line-level L2 occupancy.
- **Proposed verdict:** keep OCCUPIED.

## F Q1. Metrology or measurement vocabulary: OCCUPIED (psychometric) / CLEAN (provisional) (metrology proper)

- **Full text.** 2610.25846 ("measurement validity", pre-registered), 2604.22215 ("Psychometric
  Validity Screen", 7 of 7 models Invalid), 2604.17707 ("validity scaling", 63 uses of "validity"),
  2604.15702 (psychometric battery). The vault notes contain no use of "measurand" (checked by
  grep).
- **Proposed verdict:** keep the split.

## F Q2. Bias, resolution, noise relative to an internal reference: OCCUPIED (union)

- **Full text.**
  - 2603.05544 (Theorem 1) splits forecast versus outcome; the dossier notes "never to an internal
    reference".
  - 2603.15232 (Theorems 2.1-2.6, Proposition 3.2) gives miscalibration plus grouping
    (information loss from X to S) plus irreducible uncertainty. It has no LLM content.
  - Ghosh 2610.25846 (Sec 6, Table 3) reports Murphy reliability and resolution for verbal,
    consensus, and probe readouts, with resolution ratio 2.02x. Its probe "predict[s] a median
    split of the model's own semantic entropy, not correctness" (Limitations), so it is not an
    internal correctness reference.
- **Union check.** It holds only by composition. The "internal reference" dimension is covered by
  Charpentier's grouping term with X set to the hidden state, which no fetched work instantiates.
  Readout-relative bias and resolution then reduce to differences of Murphy terms between a
  correctness probe and the stated readout, and cross-format noise is Ghosh's or Mahaut's
  statistic. "Only running them on the same problems" is slightly too strong: one also needs a
  calibrated correctness probe as the reference.
- **Narrowest residual.** The grouping-term loss from a correctness probe to stated confidence,
  measured on code. Closest work: Charpentier (theory) and Ghosh (non-code, entropy-labeled
  probe).
- **A21.** Condition 1 passes (use). Condition 2 fails: the only code-specific point is that
  execution labels make the reference's calibration checkable. That makes the estimate cleaner;
  it is not a reason the result would differ.
- **Proposed verdict:** keep OCCUPIED (union). Add the caveat that Ghosh's probe is not a
  correctness reference.

## F Q3. A24 residual quantity: OCCUPIED (effective)

- **Full text.** Mahaut 2406.13415 compares five families (trained probes, sequence probability,
  verbalization, surrogate token probability, consistency) for robustness across paraphrases.
  Ghosh Table 2 reports cross-format correlations (Spearman 0.126, -0.069, 0.247).
- **Narrowest residual.** Readout noise of stated confidence under semantics-preserving program
  rewrites (renaming, reformatting) whose label invariance is verified by execution. Closest work:
  Mahaut (question paraphrases, NLP) and 2608.08266 (framing changes for the probe only, "no single
  configuration is best").
- **A21.** Condition 1 passes (label protocol). Condition 2 is borderline. Code allows candidate
  rewrites with a provably fixed label, which NLP paraphrase sets assume rather than verify, and
  2608.08266 shows that code readouts react to framing. Neither shows that the stated-confidence
  noise itself would differ.
- **Proposed verdict:** keep OCCUPIED. Record the rewrite-invariance residual as optional, to be
  adopted only if the orchestrator accepts the condition 2 argument.

## F Q4. meta-d' and metacognitive efficiency: OCCUPIED

- **Full text.**
  - 2603.29693 reports meta-d', M-ratio, and AUC2 for verbal ratings on three non-code tasks.
  - 2603.25112 reports type-2 SDT of token log-probability plus meta-I_2r, and calls meta-d'
    ill-defined for open QA.
  - Neither uses a hidden-state readout as the "internal" term. M-ratio's denominator is type-1
    d', not a probe.
- **Residual.** Probe type-2 sensitivity versus stated type-2 sensitivity. That is AUROC of the
  probe versus AUROC of stated confidence, which is L2 Q1 and adds no F claim.
- **Proposed verdict:** keep OCCUPIED.

## Misreads and status inconsistencies to fix

1. VERDICTS L2 Q1c: Ribeiro's RQ2 is omitted; it is a self-generated, within-task probe-versus-verbal
   ranking (Sec 5.1-5.2, "Only a few comparisons reached statistical significance").
2. Dossier 2512.24560: for Qwen, Probe-7B reads the generator's own states, so the "separate
   supervisor" note is wrong.
3. Dossier 2611.07876 and VERDICTS L1 Q1 and L2 Q1: EigenScore is problem level only; Campos does
   not compare per-candidate sampling with probes.
4. VERDICTS L1 Q12: 2610.11300's judge is an external model.
5. VERDICTS L2 Q1: it rests on two works, so the label should be OCCUPIED (union).
6. VERDICTS status table: CodeRefuser 2605.17029 was submitted 2026-05-16 per its dossier, so it is
   concurrent, not "check against the window". Code-MUE 2607.12273 and 2605.19369 carry published
   venues in their dossiers (ISSTA 2026 PACMSE; ICSE-NIER 2026), and the A23 tags should say so.
7. 2605.09023 Table 6, a seeded versus seed-free AUROC drop of 0.014 to 0.087, is missing from L1
   Q4's evidence. It occupies the single-family version of the label-independence residual.
