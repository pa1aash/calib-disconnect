# Positioning brief: scope of the literature-positioning run

Wave 3, 2026-11-10. This brief scopes the next wave's literature-positioning run. It does not run
it. Every work named below is an **unverified lead**: the run must fetch a record for it before it
can count as evidence, and must not cite it otherwise. Leads come from the operator's wave 3 prompt
and from an earlier vault report (`research/notes/final_report_code-llm-probe-verbalize-gap-3d8995.md`,
July 2026), whose sources were never re-checked and whose quoted legacy numbers have no backing file
(`docs/s2/METHOD_INVENTORY.md` section 11.3).

## 1. Candidate contributions to test

Each candidate is a hypothesis about where an open contribution lies. The run decides, with
evidence, whether each is OCCUPIED, NARROW, or CLEAN.

| Id | Candidate | Core claim it would support |
|----|-----------|-----------------------------|
| L1 | Measurement foundation | An execution-graded comparison of confidence methods across model families, scales, and benchmarks, with a release-date contamination control, establishes which methods track correctness on code |
| L2 | Locating the disconnect | Comparing hidden-state probes with verbal and sampled readouts, across base and instruct pairs, reasoning and non-reasoning models, and elicitation formats, locates where correctness information is lost between internal state and output |
| L3 | Verification utility | Confidence-routed execution budgets beat random routing and approach oracle routing; verbal confidence does or does not update after the model sees a failing test |
| L4 | Angles the legacy material supports better | Per-requirement (per-test-group) confidence from `src/v4_dprc`: confidence that localizes which requirement a solution fails, plus targeted repair versus regeneration and self-written test adequacy (designed in v4, never run) |
| F | Framing hypothesis: measurement-instrument lens | Calibration treated as instrument assessment: internal state as the measurand, verbal output and sampling as readouts, with readout error decomposed into bias, resolution, and noise |

Ordering note: the earlier vault report judged a probe-versus-verbal gap on code "multiply scooped"
at whole-solution granularity. That judgment is itself unverified; the run treats it as the first
claim to test for L2.

## 2. Occupancy questions and seed leads

### L1 Measurement foundation

Occupancy questions:

1. Has any 2024 to 2026 study compared four or more confidence families (sampling agreement, token
   probability, stated confidence, hidden-state probe) against execution labels for code?
2. Does any such study span three or more model families, two or more scales, and three or more
   benchmarks?
3. Does any use a release-date split (for example LiveCodeBench windows) as a contamination control
   for calibration, as distinct from accuracy?
4. Does any report label independence (label from a generation that no confidence method used)?

Seed leads (unverified):

- Spiess et al., calibration and correctness in code models (ICSE 2025).
- Campos et al., multicalibration for code (2025), cited in the legacy v3 manuscript.
- Semantic-equivalence and execution-based uncertainty for code, 2024 to 2026 (search facet, no
  named lead).
- PAC prediction sets for code language models (vault note `230208703-...`).
- Benchmarks surveys of code-model calibration published 2025 to 2026 (search facet).

### L2 Locating the disconnect

Occupancy questions:

1. Has hidden-state probing for code correctness been compared against stated confidence and
   sampling agreement on the same problems?
2. Has the comparison been made across base and instruct pairs of the same model, and across
   reasoning and non-reasoning models?
3. Has elicitation format (numeric, verbal category, token probability of a yes/no question,
   post-hoc critique) been varied as a factor?
4. Is the gap's location (present in base, introduced by instruction tuning, or reduced by
   reasoning) reported anywhere for code?

Seed leads (unverified):

- Kumar et al., 2024, confidence-probability alignment in LLMs.
- Xiong et al., ICLR 2024, verbalized confidence elicitation; Tian et al., 2023, verbalized
  confidence after RLHF.
- Kadavath et al., 2022, "Language models (mostly) know what they know" (vault note
  `220705221-...`).
- Orgad et al., ICLR 2025, hidden states encoding correctness ("LLMs know more than they show").
- Azaria and Mitchell, 2023, "The internal state of an LLM knows when it's lying" (vault note
  `230413734-...`).
- Marks and Tegmark, geometry of truth (year to confirm).
- Burns et al., ICLR 2023, latent knowledge without supervision (vault note `221203827-...`).
- From the earlier vault report: Ribeiro, Spiess, Devanbu, and Nadi, internal representation of
  code correctness (reported as ICSE 2026); Miao and Ungar, confidence-faithfulness gap (reported
  as March 2026); Sarfati et al., forecasters' probe versus stated confidence (reported as July
  2026); ConfTuner and "Rewarding Doubt" (Stangel et al., 2025) on trained verbal confidence.

### L3 Verification utility

Occupancy questions:

1. Has confidence-routed allocation of execution or sampling budget been evaluated against oracle
   and random routing for code generation or code agents?
2. Does any work measure whether stated confidence updates after the model observes a failing test,
   and whether the update tracks the repair outcome?
3. Do selective prediction or verifier-routing papers for code agents already report coverage and
   risk curves that subsume this?

Seed leads (unverified):

- Selective prediction and verifier routing for code agents, 2024 to 2026 (search facet).
- Semantic entropy: Kuhn et al., 2023 (vault note `230209664-...`); Farquhar et al., Nature 2024.
- Self-consistency (Wang et al., 2023; vault note `220311171-...`) as a sampling-budget baseline.
- Conformal risk control (vault note `220802814-...`) for routing with guarantees.
- Self-repair and self-debugging with test feedback (search facet).

### L4 Per-requirement confidence and related v4 angles

Occupancy questions:

1. Has per-test or per-requirement confidence for generated code been elicited, trained, or probed,
   and evaluated as localization (which requirement fails)?
2. Has targeted repair guided by per-requirement confidence been compared with regeneration?
3. Has the adequacy of model-written tests been related to the model's own correctness or
   confidence?

Seed leads (unverified):

- Per-edit or fine-grained confidence for code (an SE-venue recalibration paper named in the
  earlier vault report without full details).
- Test-generation and self-test adequacy studies, 2024 to 2026 (search facet).

### F Measurement-instrument framing

Occupancy questions:

1. Is "measurand", "readout", "instrument", or metrology vocabulary already used for LLM
   calibration or confidence elicitation?
2. Does any work decompose stated-confidence error into bias, resolution, and noise relative to an
   internal reference, as distinct from the standard calibration and refinement decomposition of
   the Brier score?
3. Would the framing add analysis a reviewer can use, or only names?

Seed leads (unverified): Brier score decomposition literature (Murphy, 1973) as the existing
baseline the framing must go beyond; "LLM as measurement instrument" and psychometrics-of-LLMs
work (search facet).

## 3. Search facets, venues, years, and instrument rules

### Facets

Combine one term from each of two or more groups.

| Group | Terms |
|-------|-------|
| Object | code generation, code language model, program synthesis, coding agent, software engineering LLM |
| Signal | calibration, confidence estimation, uncertainty quantification, verbalized confidence, self-assessment, P(True), semantic entropy, self-consistency, hidden-state probe, linear probe, internal representation |
| Ground truth | execution, unit tests, functional correctness, pass@k, test-based |
| Use | selective prediction, abstention, routing, verifier, test-time compute, self-repair, deferral |
| Factor | instruction tuning, base versus instruct, reasoning model, chain of thought, elicitation format, contamination, release date |
| Framing | measurement, metrology, measurand, readout, instrument, psychometrics |

### Venues

ICLR, ICML, NeurIPS, TMLR, COLM, ACL, EMNLP, NAACL, and Findings; ICSE, FSE, ASE, ISSTA, and TOSEM;
Nature and Nature Machine Intelligence; arXiv cs.LG, cs.CL, cs.SE, and cs.AI.

### Years

January 2022 to November 2026, with emphasis on 2025 to 2026. Forward citation screens cover
everything up to the run date.

### Instrument rules

1. **Headless retrieval only.** Use the literature-search tool's default builtin provider and
   headless curl. No visible browser and no login profile. Readiness was confirmed in wave 3
   (`docs/s3/W3_REPORT.md`, literature-search tooling).
2. **arXiv full text.** The arXiv API `all:` field searches metadata only. Full-text queries go
   through the `search_classic` endpoint with `searchtype=ft`. Before relying on it, validate the
   endpoint on two known positives (a phrase that occurs only in the body of a known paper) and
   record the result; if validation fails, record an instrument gap.
3. **Semantic Scholar** with incremental backoff on HTTP 429 (for example 2, 4, 8, 16, then 32
   seconds, then record a gap). Use it for search and for forward and backward citations.
4. **OpenReview** for ICLR, TMLR, and COLM records, including withdrawn and rejected submissions.
5. **Forward citation screens** on the closest occupants of each candidate: every paper citing them,
   screened by title and abstract, then fetched if relevant.
6. **Bibliography only from fetched records.** A BibTeX entry is written only from a record the run
   fetched (arXiv, Semantic Scholar, OpenReview, DOI landing page, or publisher page), with the URL
   and retrieval date in a comment.
7. **Gaps are not zeros.** An unreachable source, a rate limit, a login wall, or a failed endpoint is
   recorded as an instrument gap with the query and the error. A verdict may not rely on the absence
   of results from a source that had a gap.
8. **Hosts.** The run needs network access beyond this wave's list: arxiv.org and export.arxiv.org,
   api.semanticscholar.org, api.openreview.net and openreview.net, api.openalex.org, doi.org, and
   publisher and proceedings hosts (aclanthology.org, proceedings.mlr.press, papers.nips.cc,
   dl.acm.org, ieeexplore.ieee.org, nature.com). The next wave prompt must allow them.

## 4. Output contract

All outputs go under `research/positioning/<vault_tag>/` and are tracked. The sync step in the
local tooling note copies every source note and run artifact there with a hash manifest.

1. `VERDICTS.md`: for each candidate (L1 to L4, F), one verdict with evidence.
   - **OCCUPIED**: a fetched work already makes the candidate's core claim with comparable or
     greater breadth. Name it, quote the claim, and give the record URL.
   - **NARROW**: related work exists, but a precisely stated residual remains. State the residual
     in one sentence and the closest work on each side of it.
   - **CLEAN**: no fetched work makes the claim, and every source in the facet grid was reached
     (list any instrument gaps that weaken this).
2. `RECOMMENDATION.md`: a ranked list of the strongest defensible contributions for a TMLR paper,
   each with its supporting verdicts, the evidence the new pipeline must produce to support it
   (mapped to `docs/s3/ORIENTATION.md` section c), and the main reviewer objection with an answer.
3. `references.bib`: verified BibTeX, one entry per cited work, each from a fetched record.
4. `DIGEST.md`: one paragraph per closest occupant (claim, method, models, benchmarks, granularity,
   venue and year, record URL), the search log (queries, sources, hit counts, date), and the
   instrument-gap log.
5. `MANIFEST.json`: every copied file with source path, size, and SHA-256.

## 5. Pivot criteria for L2 as the spine

L2 is unviable as the paper's spine if any of the following is found in a fetched record:

1. A study already compares hidden-state probes, stated confidence, and sampling agreement for code
   correctness across base and instruct pairs and across reasoning and non-reasoning models (L2
   OCCUPIED at our intended breadth).
2. The residual after the closest occupant is only a change of models or benchmarks, with no new
   factor (granularity, tuning stage, reasoning, or elicitation format) left unstudied.
3. The probe-versus-stated-confidence gap on code is shown to close under an elicitation method we
   would have to include, which would remove the disconnect the paper is about.

Replacement order if L2 fails:

1. **L1 plus L3 as the spine.** A broad execution-graded measurement study (L1) whose payoff is
   verification utility (L3): which confidence signal should decide when to run tests or sample
   more, with oracle and random routing as bounds. L2 findings that remain NARROW become one
   section, not the headline.
2. **L4 if CLEAN or NARROW.** Per-requirement confidence and localization, if the run finds the
   granularity unoccupied and the v4 design can be rebuilt within the new pipeline. This needs the
   operator's v4 scope decision.
3. **F only as framing.** The measurement-instrument lens is adopted only if it is not already in
   use and it yields an analysis (an error decomposition) that the standard Brier decomposition
   does not; otherwise it is dropped.
