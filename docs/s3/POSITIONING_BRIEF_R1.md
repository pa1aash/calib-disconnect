# Positioning brief, revision 1 (R1)

Wave 4, 2026-11-10. This revision applies the amendments accepted from the wave 4 adversarial
review. The review is in `research/positioning/w4/parts/critic-brief/FINDINGS.md`; amendment numbers
A1 to A32 refer to it. The original, `docs/s3/POSITIONING_BRIEF.md`, is kept unchanged. Section 7
records every amendment as accepted, modified, or rejected, with reasons.

R1 also reflects the wave 4 instrument validation (`research/positioning/w4/INSTRUMENTS.md`):

- arXiv full-text search failed.
- OpenAlex full-text search is partial.
- Semantic Scholar keyword search is rate-limited and counts as a gap.

## 0. Status of leads (A30)

Every work named below is an **unverified lead**. It counts as evidence only after a record for it
is fetched. Leads come from:

- the operator's wave 3 prompt;
- an earlier vault report (`research/notes/final_report_code-llm-probe-verbalize-gap-3d8995.md`);
- the legacy bibliography (`papers/v3/references.bib`).

Legacy bibliography entries are leads, not metadata. Several have "and others" authors or no
identifier (references.bib lines 94-99, 265-271, and 273-279). The ICSE 2025 Spiess entry (line 87)
is titled "Calibration of LLM Code Generation", which differs from the brief's description. All
metadata must come from fetched records, and a lead that cannot be found is recorded as "not
located".

## 1. Candidate contributions to test

| Id | Candidate | Core claim it would support |
|----|-----------|-----------------------------|
| L1 | Measurement foundation | An execution-graded comparison of confidence methods across model families, scales, and benchmarks, with a release-date contamination control, establishes which methods track correctness on code |
| L2 | Locating the disconnect | Comparing hidden-state probes with verbal and sampled readouts, across base and instruct pairs, reasoning and non-reasoning models, and elicitation formats, locates where correctness information is lost between internal state and output |
| L3 | Verification utility | Confidence-routed execution budgets beat random routing and approach oracle routing; verbal confidence does or does not update after the model sees a failing test |
| L4 | Per-requirement confidence (v4 angles) | Per-requirement (per-test-group) confidence from `src/v4_dprc`, which localizes the requirement a solution fails, plus targeted repair versus regeneration and self-written test adequacy |
| F | Framing hypothesis: measurement-instrument lens | Calibration treated as instrument assessment: internal state as the measurand, verbal output and sampling as readouts, with readout error decomposed into bias, resolution, and noise |

**Ordering note.** The wave 4 step 3 check (`research/positioning/w4/L2_OCCUPANT.md`) has
confirmed the earlier report's closest code occupant, Ribeiro et al., ICSE 2026. The run still
records whether its own width sweep finds that work independently (modified A31).

## 2. Occupancy questions and seed leads

### L1 Measurement foundation

1. Has any 2024 to 2026 study compared four or more confidence families against execution labels
   for code? The families are sampling agreement, token probability, stated confidence, and
   hidden-state probe.
2. Does any such study span three or more model families, two or more scales, and three or more
   benchmarks?
3. Does any use a release-date split, such as LiveCodeBench windows, as a contamination control for
   calibration rather than for accuracy?
4. Does any report label independence, meaning the label comes from a generation that no
   confidence method used?
5. (A1) Which calibration estimators do 2022 to 2026 confidence studies for code and LLMs use? The
   range includes equal-width and equal-mass binned ECE, debiased or smoothed ECE, kernel or
   binning-free estimators, proper scoring rules, reliability diagrams with intervals, AUROC, AUPRC,
   and selective risk or AURC. Has any code study shown that its method ranking changes with the
   estimator?
6. (A1) Has any code study formally separated calibration from discrimination, or tested
   recalibration as a control that separates the mapping from the information?
7. (A5) Which code confidence methods measure agreement among samples without using the
   benchmark's hidden tests? Candidates include agreement of execution outputs on generated inputs,
   agreement with model-generated tests, functional clustering, minimum Bayes risk over execution,
   and symbolic or formal equivalence. How do they compare with test-pass agreement under the same
   labels?
8. (A5) Has semantic entropy been adapted to code with execution-equivalence or
   symbolic-equivalence clustering?
9. (A8) Which code benchmarks provide release-date windows or decontamination, and which have been
   used for calibration rather than accuracy?
10. (A8) Has insufficient benchmark test coverage been shown to change calibration or method
    rankings, and which augmented-test variants exist?
11. (A12) Has calibration of code confidence been reported by subgroup (difficulty, language,
    source, release window), and does multicalibration change the rankings?
12. (A13) Has a model's self-judgment, or a judge model's score of code, been evaluated as
    confidence against execution labels and compared with the families in question 1?
13. (A18) Has contamination or memorization been shown to change calibration or discrimination, for
    example by comparing problems released before and after the training cutoff?

Seed leads (unverified):

- Spiess et al., ICSE 2025. The legacy bibliography titles it "Calibration of LLM Code Generation".
- Campos et al., multicalibration for code (2025).
- The legacy leads at references.bib lines 265-271 (self-consistency distillation) and 273-279
  (UQ4CT).
- li2022competition (AlphaCode clustering) and lin2022teaching.
- PAC prediction sets for code language models (vault note `230208703-...`).
- Generated-test dual agreement and execution-based minimum Bayes risk reranking (search facet).
- Benchmarks and surveys of code-model calibration published 2025 to 2026 (search facet).

### L2 Locating the disconnect

1. (A10) Has hidden-state probing for code correctness been compared on the same problems against
   stated confidence, token probability, and sampling agreement, with execution-graded labels?
2. Has the comparison been made across base and instruct pairs of the same model, and across
   reasoning and non-reasoning models?
3. Has elicitation format been varied as a factor? Formats include numeric, verbal category, the
   token probability of a yes or no question, and post-hoc critique.
4. Does any work report, for code, where the gap arises: whether it is present in base models,
   introduced by instruction tuning, or reduced by reasoning?
5. (A2) Has a hidden-state probe been trained to predict execution-graded correctness of generated
   code? If so, with which labels, layers, token positions (prompt-only before generation, or after
   it), and model families?
6. (A2) Has probe transfer across benchmarks, languages, or models been reported? Does the probe
   beat sequence likelihood and sampling agreement out of distribution?
7. (A2) Have other white-box readouts, such as attention, sparse autoencoder features, or steering
   directions, been used for code correctness?
8. (A3) Has the calibration of one code model been measured before and after each post-training
   stage, with execution labels? The readouts are token probability, sampling agreement, and stated
   confidence. In general NLP, preference tuning is reported to degrade token-probability
   calibration. Is that finding replicated, contradicted, or untested for code?
9. (A4) Has any 2025 to 2026 study measured whether extended reasoning changes the calibration or
   discrimination of stated confidence on code or other verifiable tasks? Do signals inside the
   reasoning trace (hedging, backtracking, length) beat the final stated number?
10. (A4) Has probing of reasoning models been compared with their stated confidence, with reasoning
    enabled?
11. (A14) Has stated confidence been trained on code or other verifiable tasks? Methods include SFT,
    RL with proper-scoring rewards, and distillation from agreement. Does training close the gap in
    discrimination as well as in calibration?
12. (A15) Has any work intervened causally (steering, ablation, patching) on a correctness or
    confidence direction to change stated confidence?
13. (A16) Has any code-confidence study separated discrimination between problems (difficulty) from
    discrimination within a problem?

Seed leads (unverified):

- Kumar et al., 2024, confidence-probability alignment. Semantic Scholar query: "confidence
  probability alignment large language models".
- Xiong et al., ICLR 2024; Tian et al., 2023.
- Kadavath et al., 2022 (`220705221-...`).
- Orgad et al., ICLR 2025.
- Azaria and Mitchell, 2023 (`230413734-...`).
- Marks and Tegmark.
- Burns et al., ICLR 2023 (`221203827-...`).
- Ribeiro, Spiess, Devanbu, and Nadi, ICSE 2026 (confirmed in wave 4 step 3), and its close citers:
  arXiv 2611.07876, 2608.08266, 2606.14530, and 2607.05188.
- Bui et al. and Vu et al. on pre-generation code-correctness probing, cited by those citers.
- Miao and Ungar (March 2026), Sarfati et al. (July 2026), ConfTuner, and "Rewarding Doubt"
  (Stangel et al., 2025).
- Technical-report statements on calibration after RLHF (search facet).

### L3 Verification utility

1. Has confidence-routed allocation of execution or sampling budget been evaluated against oracle
   and random routing, for code generation or code agents?
2. Does any work measure whether stated confidence updates after the model observes a failing test,
   and whether the update tracks the repair outcome?
3. Do selective prediction or verifier-routing papers for code agents already report coverage and
   risk curves that subsume this?
4. (A6) Do reranking, learned-verifier, or reward-model papers report the value of confidence for
   allocating samples, tests, or verifier calls, against oracle and random allocation?
5. (A6) Do cascade or deferral papers for code measure routing against an oracle?
6. (A6) Has uncertainty or abstention been studied for repository-level agents, and at what unit?
7. (A7) Does stated confidence or a probe readout change after execution feedback, and does the
   change predict repair success? Do models revise confidence whether or not the feedback is valid,
   measured with correct versus spurious failures?

Seed leads (unverified):

- Kuhn et al., 2023 (`230209664-...`), and Farquhar et al., Nature 2024.
- Self-consistency (`220311171-...`).
- Conformal risk control (`220802814-...`).
- (A32) Conformal prediction and abstention for code beyond PAC sets.
- Self-repair and self-debugging with test feedback (`230609896-...`).
- Selective prediction and verifier routing for code agents (search facet).

### L4 Per-requirement confidence and related v4 angles

1. Has per-test or per-requirement confidence for generated code been elicited, trained, or probed,
   and evaluated as localization of the failing requirement?
2. Has targeted repair guided by per-requirement confidence been compared with regeneration?
3. Has the adequacy of model-written tests been related to the model's own correctness or
   confidence?
4. (A11) Has code confidence at the line, token, edit, or step level been evaluated as localization,
   and how does it relate to localization by test group?

Seed leads (unverified):

- FLARE-style line-level localization (earlier vault report, section 4). Its quoted effect sizes are
  not carried forward.
- Per-edit Platt recalibration (SE venue).
- Process reward models for code.
- arXiv 2607.05188, step-level probes in agents.

### F Measurement-instrument framing

1. Is "measurand", "readout", "instrument", or other metrology vocabulary already used for LLM
   calibration or confidence elicitation?
2. Does any work decompose stated-confidence error into bias, resolution, and noise relative to an
   internal reference, as distinct from the standard calibration and refinement decomposition of
   the Brier score?
3. (A24) Does the framing define at least one quantity that cannot be computed from the Murphy
   decomposition, a covariance decomposition of the Brier score, or a metacognitive-efficiency ratio?
   Examples are readout bias, readout resolution relative to an internal reference, and readout
   noise across formats. Record the candidate quantity beside the closest existing one.
4. (A9) Has the gap between internal and expressed confidence been formalized for LLMs as
   metacognitive efficiency (type-2 signal detection, meta-d')? If so, the measurand-readout
   decomposition must be shown to differ from it.

Seed leads (unverified):

- Brier score decomposition (Murphy, 1973) and the Yates covariance decomposition.
- The meta-d' literature.
- Work on LLMs as measurement instruments, psychometrics of LLMs, and construct validity.

## 3. Search facets, venues, years, and instrument rules

### Facets

| Group | Terms |
|-------|-------|
| Object | code generation, code language model, code LLM, LLMs for code, large language models of code, program synthesis, coding agent, software engineering LLM, code completion, code repair, code translation, text-to-SQL |
| Signal | calibration, confidence estimation, confidence calibration, uncertainty quantification, uncertainty estimation, verbalized confidence, self-assessment, self-evaluation, know what they don't know, P(True), P(IK), semantic entropy, self-consistency, sequence likelihood, perplexity, hidden-state probe, linear probe, probing classifier, internal representation, activations, white-box, truthfulness direction, sparse autoencoder feature, pre-generation probe, functional equivalence, execution agreement, output clustering, generated tests, symbolic execution, equivalence checking, minimum Bayes risk, hedging, epistemic markers, confidence revision, belief update |
| Ground truth | execution, unit tests, functional correctness, pass@k, test-based |
| Use | selective prediction, abstention, routing, verifier, test-time compute, self-repair, self-debugging, self-correction, deferral, reranking, best-of-n, learned verifier, outcome reward model, process reward model, cascade, model routing, budget allocation, agent trajectory, SWE-bench, multi-turn, execution feedback, capitulation, sycophancy |
| Factor | instruction tuning, supervised fine-tuning, base versus instruct, RLHF, DPO, preference optimization, reinforcement learning from unit tests, RL with verifiable rewards, reward model, reasoning model, thinking model, long chain of thought, reasoning trace, reasoning budget, overthinking, chain of thought, elicitation format, contamination, release date, multicalibration, subgroup calibration |
| Metric (A1) | expected calibration error, ECE estimator bias, debiased ECE, smooth ECE, adaptive binning, equal-mass binning, kernel calibration error, proper scoring rule, Brier score decomposition, refinement, reliability diagram, AUROC, AURC, risk-coverage, selective risk |
| Benchmark (A8) | HumanEval, MBPP, APPS, CodeContests, LiveCodeBench, BigCodeBench, SWE-bench, augmented tests, test insufficiency, decontamination, release window |
| Framing | measurement, metrology, measurand, readout, instrument, psychometrics, metacognition, metacognitive sensitivity, metacognitive efficiency, type-2 signal detection, meta-d', introspection, construct validity, measurement validity, item response theory |

**Query construction (A27, modified).**

- Every query includes one Object or Benchmark term and one Signal term, plus at least one term from
  Ground truth, Use, Factor, Metric, or Framing.
- General-NLP queries for L2 and F may drop the Object term, but must then include a Factor or
  Framing term.
- Each candidate gets a fixed list of 15 to 30 queries, written to
  `research/positioning/w4/QUERIES.md` before searching.
- Every query is logged in `research/positioning/w4/SEARCH_LOG.md` with its instrument, date, hit
  count, and number screened, including zero hits.

### Venues (A28)

- **ML conferences and journals:** ICLR, ICML, NeurIPS (through OpenReview and proceedings), TMLR,
  COLM, AAAI, IJCAI.
- **NLP:** ACL, EMNLP, NAACL, and Findings; TACL.
- **Software engineering:** ICSE, FSE, ASE, ISSTA, TOSEM, IEEE TSE, Empirical Software Engineering,
  MSR, ICSME, SANER.
- **Other:** Nature and Nature Machine Intelligence; workshops focused on code or uncertainty,
  tagged as workshop.
- **Preprints:** arXiv cs.LG, cs.CL, cs.SE, and cs.AI.

### Years

January 2022 to November 2026, with emphasis on 2025 and 2026. Forward citation screens cover
everything up to the run date. Pre-2022 metric and decomposition works count as foundations, not
occupants.

### Instrument rules (revised to match `research/positioning/w4/INSTRUMENTS.md`)

1. **Headless retrieval only.** Use the literature-search tool's builtin provider and headless curl,
   to the wave's allowed hosts only. No web-search engine is used.
2. **arXiv full text: failed validation.** The `search_classic` `searchtype=ft` endpoint is not
   functional on allowed hosts. Any negative that would need body-text search is an instrument gap.
   arXiv metadata search (`all:`, `ti:`, `abs:`, `searchtype=all`) is used for recall only (A29,
   modified).
3. **OpenAlex** search, title and abstract plus a partial full-text filter, is the primary keyword
   instrument. Its full-text filter found one of two validation positives. Its positive hits count;
   its negatives are gaps.
4. **Semantic Scholar** is used for lookups, forward citations, and backward citations, with backoff
   from 4 to 40 seconds. Keyword search through it is a recorded gap (HTTP 429).
5. **OpenReview** is searched through v1 `notes/search` on api.openreview.net, with venue and year
   terms in the query (A29, modified). Venue listings, forum pages, and PDFs are behind a browser
   challenge. OpenReview-only full texts are gaps.
6. **Forward citation screens (A29).** Screen at least the three closest occupants per candidate,
   and record the retrieval date of the citation index. Every paper rated a close occupant is
   screened.
7. **Bibliography only from fetched records.** Records come from Crossref, DBLP, arXiv, OpenReview,
   or the publisher, each with its source URL and retrieval date.
8. **Gaps are not zeros.** An unreachable source, a rate limit, a login wall, or a failed endpoint
   is recorded with the query and the error.

## 4. Verdict definitions (A19 to A23, A22 modified)

**Breadth matrix (A19).** Each occupant's breadth is recorded in its dossier on a fixed matrix:

- confidence families;
- model families;
- scales;
- benchmarks;
- base and instruct pairs;
- post-training stages;
- reasoning versus non-reasoning models;
- elicitation formats;
- label source;
- label independence;
- contamination split;
- calibration metrics;
- granularity;
- causal intervention.

"Comparable breadth" means the occupant matches or exceeds the candidate on every dimension that the
candidate's core claim names.

**Verdicts:**

- **OCCUPIED.** A fetched work makes the candidate's (or component's) core claim with comparable
  breadth.
- **OCCUPIED (union) (A20).** At most three fetched works together cover every dimension of the core
  claim, and the only thing left to add is running them on the same problems.
- **NARROW.** Related work exists, but a precisely stated residual remains (A21). The residual
  qualifies only if both conditions hold:
  1. it is a factor, granularity, label protocol, or use, not just a change of models or
     benchmarks;
  2. there is a stated, concrete reason why the code result could differ from the closest
     general-NLP result.

  Otherwise the verdict is OCCUPIED. A NARROW verdict states the residual in one sentence and names
  the closest work on each side of it.
- **CLEAN.** No fetched work makes the claim, and all three of these hold:
  1. every query in the candidate's fixed list ran on every instrument that passed validation;
  2. forward and backward screens of the three closest works were completed;
  3. the last ten screened queries or citation pages added nothing relevant.
- **CLEAN (provisional).** The CLEAN conditions hold except for an instrument gap that bears on the
  claim. The gap is always the case for body-text claims in this wave, because arXiv full-text
  search failed. A CLEAN (provisional) verdict lists its gaps, and RECOMMENDATION.md may not claim
  novelty on it without hedging.

**Occupant status (A23).** Each occupant is tagged with one of:

- published or accepted (venue and year);
- preprint only (first posting date);
- withdrawn or rejected;
- concurrent, meaning posted within six months of the run date (after 2026-05-10).

The six-month window is a proposal for the operator to confirm. Verdicts state which tags they rest
on.

## 5. Output contract

Everything is under `research/positioning/`:

1. `w4/VERDICTS.md`: a verdict for each candidate and each component, with evidence and the gaps
   that weaken any CLEAN or NARROW verdict.
2. `w4/RECOMMENDATION.md`: a ranked list of contributions. Each entry has a contribution sentence,
   its evidence needs (mapped to `docs/s3/ORIENTATION.md` section c), its TMLR fit, and its main risk.
3. `w4/references.bib`: one entry per cited work, each from a fetched record with its URL.
4. `w4/DIGEST.md`: at most 1,500 words, readable in place of the run.
5. `w4/dossiers/`: one dossier of at most 300 words per close occupant, including its breadth
   matrix.
6. `w4/QUERIES.md` and `w4/SEARCH_LOG.md`: the fixed query lists and the per-query log (modified
   A27; moved out of DIGEST.md to respect its word limit).
7. `<vault_tag>/MANIFEST.json`: every synced file with its source path, size, and SHA-256.

## 6. Pivot criteria for L2 as the spine (A14, A15, A20, A21, A25, A26)

L2 is unviable as the paper's spine if a fetched record shows any of the following:

1. (A20) One study, or at most three together, compare probes, stated confidence, and sampling
   agreement for code with execution labels, and together cover base and instruct pairs and
   reasoning and non-reasoning models.
2. (A21) The residual after the closest occupant is only a change of models or benchmarks, with no
   new factor (granularity, tuning stage, reasoning, or elicitation format) left unstudied. The same
   applies if the only unstudied factor has an established direction in general NLP and there is no
   stated reason why code would differ.
3. (A14) The gap between probe and stated confidence on code is shown to close, in discrimination
   and not only in calibration, under a method we would have to include: an elicitation method, a
   training method for stated confidence, or post-hoc recalibration.
4. (A15) A fetched work already shows by causal intervention where correctness information is lost
   on code, so a correlational comparison adds no claim about location.

Replacement order if L2 fails (A25: each replacement is adopted only if its own verdicts are NARROW
or CLEAN under section 4):

1. **L1 plus L3 as the spine.** If L1 is OCCUPIED, a measurement-only paper states its added value,
   such as the label-independence protocol, the release-date control, or augmented-test labels. It
   claims no novelty for the comparison itself.
2. **L4, if CLEAN or NARROW.** This also needs the operator's v4 scope decision.
3. **F only as framing.** F is adopted only if it is unused and yields a quantity under F question 3.
4. **(A26) If every candidate is OCCUPIED,** RECOMMENDATION.md says so and lists the strongest
   residual per candidate. The next wave then decides with the operator whether to proceed with a
   claims-reduced study or stop.

## 7. Amendment decisions

| Amendment | Decision | Reason or change |
|---|---|---|
| A1 metrics questions and facet | Accepted | Item (h) was missing |
| A2 probe literature questions | Accepted | |
| A3 post-training factor terms and question | Accepted | |
| A4 reasoning-model questions | Accepted | |
| A5 test-free agreement and execution-equivalence uncertainty | Accepted | The oracle-leakage concern (F7) is also recorded as a pipeline-design note for the next wave |
| A6 reranking, cascades, and repository agents | Accepted | |
| A7 confidence revision after feedback | Accepted | |
| A8 benchmark inventory and test insufficiency | Accepted | |
| A9 metacognition framing | Accepted | |
| A10 L2 question 1 wording | Accepted | |
| A11 line, edit, and step localization | Accepted | |
| A12 multicalibration | Accepted | |
| A13 LLM-as-judge | Accepted | |
| A14 trained stated confidence and pivot criterion 3 | Accepted | |
| A15 causal intervention and pivot criterion 4 | Accepted | |
| A16 within-problem discrimination | Accepted | |
| A17 human-factors facet | **Rejected** | No candidate's core claim depends on human trust. The legacy trust study is unbacked (`docs/LEGACY.md` decision 3). Adding the facet would widen the search without affecting any verdict. |
| A18 contamination effects on calibration | Accepted | |
| A19 breadth matrix | Accepted | "Calibration metrics" added as a dimension |
| A20 union occupancy | Accepted | |
| A21 residual qualification rule | Accepted | |
| A22 CLEAN definition | **Modified** | "ArXiv full text, Semantic Scholar, and OpenReview" became "every instrument that passed validation". Full text and Semantic Scholar search failed validation, so as written no verdict could ever be CLEAN; claims that need body text are capped at CLEAN (provisional). |
| A23 occupant status tags | Accepted | The six-month concurrency window is flagged for operator confirmation |
| A24 F question 3 | Accepted | |
| A25 gate on replacements | Accepted | |
| A26 all-occupied fallback | Accepted | |
| A27 query construction | **Modified** | Query lists and the log go to `QUERIES.md` and `SEARCH_LOG.md`, not `DIGEST.md`, which the wave limits to 1,500 words |
| A28 venues | Accepted | |
| A29 instrument fallbacks | **Modified** | Semantic Scholar snippet search is not used: its search endpoint is rate-limited. The OpenReview per-venue procedure uses v1 search with venue terms, because venue listings are behind a challenge. The rest is accepted. |
| A30 legacy leads | Accepted | Also fixes "Benchmarks surveys" and gives the Kumar lead a query |
| A31 blind-first search | **Rejected in its original form; modified version kept** | The wave fixed step 3, the check on the vault-report lead, before the run, so a blind first pass is no longer possible. The run still records whether the width sweep finds Ribeiro et al. independently. |
| A32 conformal abstention lead | Accepted | |
