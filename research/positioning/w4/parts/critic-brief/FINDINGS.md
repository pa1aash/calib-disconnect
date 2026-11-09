<!-- Saved by the wave 4 orchestrator: the critic sub-agent's own write to this path was blocked by the harness, so its final returned message is stored here verbatim. -->

The findings file was not written. The harness blocked the write to `<user-home>/Developer/calib-disconnect/research/positioning/w4/parts/critic-brief/FINDINGS.md` and told me to return the findings as text, so the full content is below for you to save.

**Summary (under 200 words).** Coverage of (a) to (j): (a) and (j) are COVERED with small gaps. (b), (c), (d), (e), (f), (g), and (i) are PARTIAL. (h), metrics beyond binned ECE, is MISSING. The biggest problems: the verdict definitions can't be tested as written. "Comparable breadth" is undefined, there is no union-occupancy rule, any residual counts as NARROW, and CLEAN needs an unbounded facet grid while also contradicting the "gaps are not zeros" rule. Pivot criterion 1 is so strict it will almost never fire. Criterion 3 leaves out trained verbal confidence and recalibration. Possible problem: ORIENTATION line 35 lets sampling agreement use hidden tests, and the brief has no facet to compare it with test-free execution-agreement methods. On the seed leads: the legacy bib title for Spiess differs from the brief's description, two legacy code-UQ leads and the vault report's FLARE lead were left out, and the vault report could anchor the search. I propose 32 numbered amendments (14 must, 14 should, 4 could), each with insertion text and arXiv, Semantic Scholar, and OpenReview query strings. No queries were run. I did not check that the arXiv full-text endpoint exists.

---

# Full findings

Files read: POSITIONING_BRIEF (PB:line), ORIENTATION (OR:line), TMLR_RUBRIC (RU:line), the vault report (VR:line), and `papers/v3/references.bib` (BIB:line). The vault note ids at PB:47, 69, 71, 74, 94, 95, and 96 exist as files; I matched filenames only. Anything not already named in those files is an "unverified lead". Verified means the problem can be seen at the cited line. Suspicion means it still needs checking.

## Part 1. Checklist (a) to (j)

| Item | Status | Brief location | Gap | Amendment |
|---|---|---|---|---|
| (a) | COVERED, minor gap | PB:18, 52-61, 140 | L2 Q1 doesn't require execution labels and leaves out token probability | A10 |
| (b) | PARTIAL | PB:54-55, 140 | No questions on the probe literature itself (pre- versus post-generation, layer, transfer, within-problem, SAE features) | A2, A16 |
| (c) | PARTIAL | PB:56-61, 66-67, 142 | No RLHF, DPO, or RL-from-tests terms; trained verbal confidence isn't a question | A3, A14 |
| (d) | PARTIAL | PB:57, 60-61, 142 | No question, terms, or seed for thinking models | A4 |
| (e) | PARTIAL | PB:45-46, 140 | Facet only, no question; no execution, symbolic, or clustering terms; possible oracle leakage (OR:35) | A5 |
| (f) | PARTIAL | PB:80-97, 141 | No reranking, verifiers, cascades, or repository-agent uncertainty | A6 |
| (g) | PARTIAL | PB:86-87, 97, 141 | No terms for confidence revision, multi-turn, feedback, or capitulation | A7 |
| (h) | MISSING | only PB:121-127, inside F | No metric question or facet; OR:37's choice of metrics isn't positioned | A1 |
| (i) | PARTIAL | PB:37-38, 142 | No benchmark inventory, no test-adequacy facet, no question on contamination effects on calibration | A8, A18 |
| (j) | COVERED, testability gap | PB:115-128, 143 | Metacognition and signal-detection framings missing; PB:124 can't be tested | A9, A24 |

## Part 2. Findings

- **F1 (verified, must). Verdict definitions (PB:185-191) can't be tested.**
  - OCCUPIED depends on "comparable breadth", which is never defined.
  - There is no union rule for a claim covered piecewise by several works.
  - NARROW accepts any residual at all.
  - CLEAN needs "every source in the facet grid", but the grid is never listed and runs to thousands of cells.
  - CLEAN-with-gaps (PB:191) contradicts PB:174.
  - Whether an occupant is published or only a preprint is not recorded, although RU:111 makes that distinction.
- **F2 (verified, must). The pivot criteria are too lenient.**
  - Criterion 1 (PB:205-207) needs one study to do everything at once, so it will almost never fire.
  - Under criterion 2, any one unstudied factor rescues L2, even when the general-NLP direction is already known.
  - Criterion 3 leaves out trained confidence (VR:33-37) and recalibration (OR:38).
  - "Locating" is a causal claim, but no criterion covers causal intervention (VR:17-19).
  - The replacement path (PB:213-224) has no gate of its own and no terminal fallback. RU:111 and RU:123 limit what a measurement-only paper can claim.
- **F3 (verified, must). Query construction (PB:136) is loose.** It doesn't require an Object anchor. It sets no budget, no stopping rule, and no zero-hit logging. Common synonyms and benchmark anchors are missing. The Object group omits code translation, although BIB:273-279 has a code-translation lead.
- **F4 (should). Instrument rules lack fallbacks.**
  - Suspicion: I have not verified that the `searchtype=ft` endpoint exists, and there is no full-text fallback if it fails.
  - Verified: there is no OpenReview procedure, and NeurIPS is not included.
  - Verified: there is no cap on forward-citation screens and no rule to record the index date.
- **F5 (verified, should). Missing venues:** TSE, EMSE, MSR, ICSME, SANER, TACL, AAAI, IJCAI, and workshops. The earlier vault report targeted AAAI (VR:55-58).
- **F6 (should). Seed leads.**
  1. Verified: PB:43 describes Spiess et al. as "calibration and correctness in code models", but BIB:87 gives the title as "Calibration of LLM Code Generation".
  2. Verified: the Campos entry (BIB:94-99) lists authors as "and others". Suspicion only that it is inaccurate.
  3. Verified omission: two legacy code-UQ leads have no identifier and "others" authors (BIB:265-271 self-consistency distillation, BIB:273-279 UQ4CT). Suspicion that they may be inaccurate.
  4. Verified omission: the FLARE-style line-level lead (VR:41-42). Its quoted effect sizes must not be carried forward.
  5. PB:48 "Benchmarks surveys" is garbled.
  6. PB:65, Kumar et al., is too thin to resolve by surname.
  7. Anchoring risk from the earlier vault report's verdicts (VR:13-16).
  8. Legacy leads the brief omits: li2022competition (BIB:73), lin2022teaching (BIB:35), nixon2019measuring (BIB:249-254), and the trust studies (BIB:126-182).
- **F7 (suspicion on a verified basis, must).** OR:35 says sampling agreement is the "fraction of samples that pass". If that uses the benchmark's hidden tests, it works as an oracle, not a confidence method. Reviewers will expect test-free execution-agreement baselines.
- **F8 (suspicion, should).** Probes and sampling agreement may encode problem difficulty rather than whether a particular sample is correct. The brief needs a question on within-problem discrimination.

## Part 3. Amendments

Query keys used below:
- **ft:** arXiv full-text phrases
- **meta:** arXiv API `search_query`
- **S2:** Semantic Scholar
- **OR:** OpenReview term, run per venue

**A1 (must, h).** After PB:39 add:
> 5. Which calibration estimators do 2022 to 2026 confidence studies for code and LLMs use (equal-width and equal-mass binned ECE, debiased or smoothed ECE, kernel or binning-free estimators, proper scoring rules, reliability diagrams with intervals, AUROC, AUPRC, selective risk and AURC), and has any code study shown its method ranking changes with the estimator?
> 6. Has any code study separated calibration from discrimination formally, or tested recalibration as the mapping versus information control?

Add a facet row after PB:143:
> | Metric | expected calibration error, ECE estimator bias, debiased ECE, smooth ECE, adaptive binning, equal-mass binning, kernel calibration error, proper scoring rule, Brier score decomposition, refinement, reliability diagram, AUROC, AURC, risk-coverage, selective risk |

Add the lead nixon2019measuring (BIB:249-254, unverified). Pre-2022 metric works count as foundations, not occupants.

Queries:
- ft: `"expected calibration error" "code generation" "debiased"`, `"smooth ECE" "language model"`, `"risk-coverage" "code generation"`
- meta: `all:"calibration error" AND all:estimator AND (cat:cs.LG OR cat:stat.ML)`
- S2: `bias of expected calibration error estimators binning`, `calibration metrics code generation LLM AUROC Brier`
- OR: `calibration error estimator`, `smooth calibration error`

**A2 (must, b).** After PB:61 add:
> 5. Has a hidden-state probe been trained to predict execution-graded correctness of generated code, with which labels, layers, token positions (prompt-only before generation versus after), and families?
> 6. Has probe transfer across benchmarks, languages, or models been reported, and does the probe beat sequence likelihood and sampling agreement out of distribution?
> 7. Have other white-box readouts (attention, sparse autoencoder features, steering directions) been used for code correctness?

Add Signal terms: `activations, white-box, probing classifier, truthfulness direction, sparse autoencoder feature, pre-generation probe, P(IK)`.

Queries:
- ft: `"linear probe" "functional correctness" "code"`, `"hidden states" "pass@1" "probe"`, `"internal representation" "code correctness"`
- meta: `all:probe AND all:"hidden states" AND all:code AND all:correctness`
- S2: `hidden state probe predicts correctness of generated code`, `predicting code generation success from activations before generation`
- OR: `probing code correctness hidden states`

**A3 (must, c).** Replace PB:142 with:
> | Factor | instruction tuning, supervised fine-tuning, base versus instruct, RLHF, DPO, preference optimization, reinforcement learning from unit tests, RL with verifiable rewards, reward model, reasoning model, chain of thought, elicitation format, contamination, release date |

Add to L2:
> 8. Has calibration (token probability, sampling agreement, stated confidence) of the same code model been measured before and after each post-training stage, with execution labels? Is the general-NLP finding that preference tuning degrades token-probability calibration replicated, contradicted, or untested for code?

Lead: technical-report calibration-after-RLHF statements (unverified).

Queries:
- ft: `"calibration" "RLHF" "code generation"`, `"base model" "instruct" "calibration" "HumanEval"`
- meta: `all:calibration AND (all:RLHF OR all:DPO OR all:"preference optimization") AND all:code`
- S2: `effect of RLHF on calibration of code language models`, `RL with verifiable rewards calibration overconfidence`
- OR: `RLHF calibration`, `RLVR calibration`

**A4 (must, d).** Add to L2:
> 9. Has any 2025 to 2026 study measured whether extended reasoning changes calibration or discrimination of stated confidence on code or other verifiable tasks? Do signals inside the trace (hedging, backtracking, length) beat the final stated number?
> 10. Has probing of reasoning models been compared with their stated confidence?

Factor terms: `thinking model, long chain of thought, reasoning trace, reasoning budget, overthinking`. Signal terms: `hedging, epistemic markers`.

Queries:
- ft: `"reasoning models" "verbalized confidence" "calibration"`, `"long chain-of-thought" "calibration"`
- meta: `all:"reasoning model" AND all:confidence AND all:calibration`
- S2: `do reasoning models know when they are right calibration verbalized confidence`, `probing hidden states of reasoning models for answer correctness`
- OR: `reasoning models calibration`

**A5 (must, e and F7).** Add to L1:
> 7. Which code confidence methods measure sample agreement without the benchmark's hidden tests (execution-output agreement on generated inputs, agreement with model-generated tests, functional clustering, minimum Bayes risk over execution, symbolic or formal equivalence), and how do they compare with test-pass agreement under the same labels?
> 8. Has semantic entropy been adapted to code with execution- or symbolic-equivalence clustering?

Replace PB:45-46 with:
> Semantic-equivalence, execution-based, and symbolic uncertainty for code, 2022 to 2026 (search facet). Unverified leads to locate: generated-test dual agreement and execution-based minimum Bayes risk reranking, AlphaCode-style clustering (li2022competition, BIB:73), and the lead at BIB:265-271.

Signal terms: `functional equivalence, execution agreement, output clustering, generated tests, symbolic execution, equivalence checking, minimum Bayes risk`.

Queries:
- ft: `"semantic entropy" "code generation" "execution"`, `"functional equivalence" "uncertainty" "code"`, `"symbolic execution" "uncertainty" "code generation"`
- meta: `all:uncertainty AND all:"code generation" AND (all:execution OR all:symbolic OR all:semantic)`
- S2: `semantic uncertainty code generation execution based clustering`, `dual agreement generated tests code selection`
- OR: `uncertainty code generation execution`

**A6 (should, f).** Add to L3:
> 4. Do reranking, learned-verifier, or reward-model papers report the value of confidence for allocating samples, tests, or verifier calls against oracle and random?
> 5. Do cascade or deferral papers for code measure routing against an oracle?
> 6. Has uncertainty or abstention been studied for repository-level agents, at what unit?

Use terms: `reranking, best-of-n, learned verifier, outcome reward model, process reward model, cascade, model routing, budget allocation, agent trajectory, SWE-bench`.

Queries:
- ft: `"confidence" "routing" "code generation" "oracle"`, `"abstain" "SWE-bench" "uncertainty"`
- meta: `all:"code generation" AND (all:cascade OR all:routing OR all:abstention OR all:"selective prediction")`
- S2: `uncertainty estimation for software engineering agents SWE-bench`, `LLM cascade code generation confidence deferral`
- OR: `code agent uncertainty`, `selective generation code`

**A7 (should, g).** Add to L3:
> 7. Does stated confidence or a probe readout change after execution feedback, and does the change predict repair success? Do models revise confidence regardless of feedback validity, measured with correct versus spurious failures?

Signal terms: `confidence revision, belief update, multi-turn, execution feedback, self-correction, self-debugging, capitulation, sycophancy`.

Queries:
- ft: `"self-debugging" "confidence"`, `"multi-turn" "calibration" "code"`
- meta: `all:"self-correction" AND all:calibration`
- S2: `does LLM confidence update after execution feedback self-repair`, `LLM capitulation incorrect feedback confidence`
- OR: `self-repair confidence`

**A8 (must, i).** Add to L1:
> 9. Which code benchmarks offer release-date windows or decontamination, and which have been used for calibration rather than accuracy?
> 10. Has insufficient benchmark test coverage been shown to change calibration or method rankings, and which augmented-test variants exist?

Add a facet row:
> | Benchmark | HumanEval, MBPP, APPS, CodeContests, LiveCodeBench, BigCodeBench, SWE-bench, augmented tests, test insufficiency, decontamination, release window |

Queries:
- ft: `"insufficient tests" "calibration"`, `"augmented test" "HumanEval" "false positive"`, `"LiveCodeBench" "calibration"`
- S2: `test insufficiency HumanEval augmented tests`, `contamination free code generation benchmark release date`
- OR: `augmented tests code evaluation`

**A9 (should, j).** Framing terms: `metacognition, metacognitive sensitivity, metacognitive efficiency, type-2 signal detection, meta-d', introspection, construct validity, measurement validity, item response theory`. After PB:124 add:
> 4. Has the internal-versus-expressed gap been formalized as metacognitive efficiency (type-2 signal detection) for LLMs? If so, the measurand-readout decomposition must be shown to differ.

Leads (unverified): meta-d' literature, and a Yates-style covariance decomposition of the Brier score.

Queries:
- ft: `"metacognitive" "meta-d" "language model"`, `"measurand" "language model"`
- S2: `metacognitive sensitivity large language models meta-d`, `LLM introspection confidence internal states`
- OR: `metacognition LLM confidence`

**A10 (could, a).** Replace PB:54-55 with:
> 1. Has hidden-state probing for code correctness been compared against stated confidence, token probability, and sampling agreement on the same problems, with execution-graded labels?

**A11 (should).** Add to L4:
> 4. Has line-, token-, edit-, or step-level code confidence been evaluated as localization, and how does it relate to per-test-group localization?

Leads: FLARE-style line-level localization (VR:41-42, unverified), and process reward models for code (unverified).

Queries:
- ft: `"line-level" "uncertainty" "code generation"`, `"per-test" "confidence"`
- S2: `fine-grained uncertainty localization generated code errors`, `per edit calibration code LLM`
- OR: `line-level uncertainty code`

**A12 (should).** Add to L1:
> 11. Has code-confidence calibration been reported by subgroup (difficulty, language, source, release window), and does multicalibration change rankings?

Terms: `multicalibration, subgroup calibration, conditional calibration`.

Queries:
- S2: `multicalibration confidence scoring LLM code generation`
- ft: `"multicalibration" "code"`
- OR: `multicalibration language models`

**A13 (should).** Add to L1:
> 12. Has self-judgment or a judge model's score of code been evaluated as confidence against execution labels and compared with the question 1 families?

Queries:
- ft: `"LLM-as-a-judge" "code" "execution"`, `"P(True)" "code"`
- S2: `LLM as judge code correctness without execution evaluation`
- OR: `LLM judge code correctness`

**A14 (must).** Add to L2:
> 11. Has stated confidence been trained (SFT, RL with proper-scoring rewards, distillation from agreement) on code or verifiable tasks, and does training close the gap in discrimination, not only calibration?

Replace PB:210-211 with:
> 3. The probe-versus-stated-confidence gap on code is shown to close (in discrimination, not only calibration) under an elicitation method, a training method for stated confidence, or post-hoc recalibration that we would have to include.

Queries:
- ft: `"verbalized confidence" "reinforcement learning" "code"`
- S2: `training LLMs to express calibrated verbal confidence reinforcement learning`
- OR: `calibrated verbalized confidence training`

**A15 (should).** Add to L2:
> 12. Has any work intervened causally (steering, ablation, patching) on a correctness or confidence direction to change stated confidence?

Add pivot criterion 4:
> 4. A fetched work already demonstrates by causal intervention where correctness information is lost on code, so a correlational comparison adds no location claim.

Queries:
- ft: `"steering" "verbalized confidence" "probe"`
- S2: `steering vector confidence faithfulness verbalized internal`
- OR: `faithfulness of verbalized confidence`

**A16 (should).** Add to L2:
> 13. Has any code-confidence study separated between-problem (difficulty) from within-problem discrimination?

Queries:
- S2: `do correctness probes encode problem difficulty rather than answer correctness`
- ft: `"within-problem" "AUROC"`

**A17 (could).** Add a facet row:
> | Human factors | developer trust, displayed confidence, code assistant user study, highlighting uncertain tokens, reliance |

Basis: BIB:126-182. Query (S2): `displaying confidence code assistant developer trust user study`.

**A18 (should).** Add to L1:
> 13. Has contamination or memorization been shown to change calibration or discrimination, for example by comparing problems before and after the training cutoff?

Queries:
- S2: `data contamination effect on LLM calibration confidence`
- ft: `"contamination" "calibration" "training cutoff"`

**A19 (must).** After PB:187 add:
> Breadth is judged on a fixed matrix recorded in DIGEST.md per occupant: confidence families; model families; scales; benchmarks; base and instruct pairs; post-training stages; reasoning versus non-reasoning; elicitation formats; label source; label independence; contamination split; granularity; causal intervention. "Comparable" means the occupant matches or exceeds the candidate on every dimension its core claim names.

**A20 (must).** Add a verdict:
> **OCCUPIED (union)**: at most three fetched works together cover every dimension of the core claim, and the only addition is running them on the same problems.

Replace PB:205-207 with:
> 1. One study, or at most three together, compare probes, stated confidence, and sampling agreement for code with execution labels and together cover base and instruct pairs and reasoning and non-reasoning models.

**A21 (must).** Append to PB:189:
> A residual qualifies only if (i) it is a factor, granularity, label protocol, or use, not only a change of models or benchmarks, and (ii) a concrete reason is stated why the code result could differ from the closest general-NLP result. Otherwise the verdict is OCCUPIED.

Add to pivot criterion 2: "or the only unstudied factor has an established direction in general NLP with no stated reason code would differ."

**A22 (must).** Replace PB:190-191 with:
> **CLEAN**: no fetched work makes the claim after (i) every query in the candidate's fixed list (written to DIGEST.md before searching) ran on arXiv full text, Semantic Scholar, and OpenReview, (ii) forward and backward screens of the three closest works were completed, and (iii) the last ten screened queries or citation pages added nothing relevant. Any gap in (i) to (iii) gives **CLEAN (provisional)** with the gaps listed; RECOMMENDATION.md may not claim novelty on it without hedging.

**A23 (should).** After PB:198 add:
> Each occupant is tagged: published or accepted (venue, year), preprint only (first posting date), withdrawn or rejected, or concurrent (posted within six months of the run date). Verdicts state which tags they rest on.

The six-month window is a proposal for the operator to decide.

**A24 (should).** Replace PB:124 with:
> 3. Does the framing define at least one quantity (readout bias, readout resolution relative to an internal reference, or readout noise across formats) not computable from the Murphy decomposition, a covariance decomposition of the Brier score, or a metacognitive-efficiency ratio? Record the candidate quantity beside the closest existing one.

**A25 (must).** After PB:213 add:
> Each replacement is adopted only if its own verdicts are NARROW or CLEAN under the amended definitions. If L1 is OCCUPIED, a measurement-only paper states its added value (label-independence protocol, release-date control, augmented-test labels) and claims no novelty for the comparison itself.

**A26 (should).** After PB:224 add:
> 4. **If every candidate is OCCUPIED,** RECOMMENDATION.md says so, lists the strongest residual per candidate, and the next wave decides with the operator whether to proceed with a claims-reduced study or stop.

**A27 (must).** Replace PB:136 with:
> Every query includes one Object or Benchmark term, one Signal term, and at least one term from Ground truth, Use, Factor, Metric, or Framing. General-NLP queries for L2 and F may drop Object but must include a Factor or Framing term. Each candidate gets a fixed list of 15 to 30 queries written to DIGEST.md before searching. Every query is logged with source, date, hit count, and number screened, including zero hits. Object adds "code LLM", "LLMs for code", "large language models of code", "code completion", "code repair", "code translation", and "text-to-SQL". Signal adds "uncertainty estimation", "confidence calibration", "self-evaluation", "know what they don't know", "sequence likelihood", and "perplexity".

The list sizes are proposals.

**A28 (should).** Append to PB:147-148:
> IEEE TSE, Empirical Software Engineering, MSR, ICSME, and SANER; TACL; AAAI and IJCAI; NeurIPS via OpenReview; code- and uncertainty-focused workshops, tagged as workshop.

**A29 (should).**
- After PB:163: "If full-text validation fails, validate and use another permitted body-text search (Semantic Scholar snippet search, if available); record which candidates lost body-text coverage."
- After PB:166: "Search per venue and year (ICLR 2023 to 2027, TMLR, COLM, NeurIPS 2022 to 2026) on title, abstract, and keywords; record the procedure."
- After PB:168: "Screen at least three closest occupants per candidate; record the citation index retrieval date."

**A30 (should).** After PB:8 add:
> Legacy bibliography entries are leads, not metadata. Several have "and others" authors or no identifier (references.bib lines 94-99, 265-271, 273-279), and the ICSE 2025 entry's title (line 87) differs from L1's description. All metadata comes from fetched records. Unlocated leads are recorded as "not located".

Also:
- Add the BIB:265-271, BIB:273-279, li2022competition, and lin2022teaching leads (all unverified).
- Fix PB:48 to "Benchmarks and surveys".
- Give PB:65 the S2 query `confidence probability alignment large language models`.

**A31 (could).** After PB:25 add:
> The run executes the L2 query lists before fetching any vault-report lead, records the five closest works found independently, then fetches the vault-report leads and records whether the blind search found each.

**A32 (could).** Add a lead to L3: conformal prediction and abstention for code beyond PAC sets (unverified). Query (S2): `conformal prediction code generation LLM abstention`.

Counts: 14 must (A1-A5, A8, A14, A19-A22, A25, A27), 14 should, and 4 could (A10, A17, A31, A32).