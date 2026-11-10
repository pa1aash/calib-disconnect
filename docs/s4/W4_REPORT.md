# Wave 4 Report: literature positioning for the TMLR submission

Date: 2026-11-10. No stop condition fired. Steps 0 to 8 were completed. The start-state check passed:
the working tree was clean, the branch was `main`, local HEAD matched origin, and the hooks were
installed.

## 1. Model identifier

- **Orchestrator:** `claude-opus-5-5` (Opus 5.5).
- **Sub-agents:** the models configured in their agent definitions:
  - project agents: fetcher, critic, reader;
  - pipeline agents: fetcher, loci analyst, depth investigator, corpus critic, draft orchestrator, synthesizer, four critics, patcher, polish auditor, readability recommender.

## 2. Commits and check results

Every commit was authored and committed as Palaash Gang. Both hooks ran on every commit, and
`--no-verify` was never used.

| SHA | Contents |
|-----|----------|
| `e6643fd` | Brief review, revised brief `docs/s3/POSITIONING_BRIEF_R1.md`, instrument validation, L2 occupant check |
| `a178904` | Search records, sub-agent outputs (`parts/`), 75 dossiers, run logs (790 files) |
| `6358df4` | Vault notes, run artifacts, critic findings, final report, `.gitleaksignore` |
| `e029aea` | `VERDICTS.md`, `RECOMMENDATION.md`, `DIGEST.md`, `references.bib`, synced run with `MANIFEST.json` |

This report and `docs/CONTEXT.md` are committed and pushed after these. Before this report's
commit, the remote and local HEAD were both `e029aeaf43fb`.

**Checks:**

- **gitleaks, full history:** 24 commits scanned, no leaks.
- **gitleaks, staged changes:** clean for `a178904` and `e029aea`.
- **gitleaks rejection on the first `6358df4` attempt:**
  - The hook rejected the commit with 5 generic-api-key matches in fetched paper text: three ACL Anthology bibkeys and two lists of model names.
  - All five were verified as false positives and added by fingerprint to a new tracked `.gitleaksignore`, together with their copies under the sync folder.
  - The commit then passed.
- **Staged-file scan:** no home paths, no secrets, and no host addresses. The only IP-like strings are section numbers in a saved HTML page.
- **Freeze:** no staged change touched a frozen path; the pre-commit hook enforces this.
- **Integrity gate on the final report:**
  - no em-dashes;
  - all 10 sections present;
  - every wikilink resolves;
  - no pipeline leaks.

## 3. Brief amendments

The critic review of `docs/s3/POSITIONING_BRIEF.md` proposed 31 amendments. The decisions are in
`docs/s3/POSITIONING_BRIEF_R1.md` section 7:

- **Accepted:** 26 amendments.
- **Modified:**
  - **A22:** CLEAN is judged against the instruments that passed validation. Body-text claims are capped at CLEAN (provisional).
  - **A27:** queries are logged in `QUERIES.md` and `SEARCH_LOG.md`.
  - **A29:** no Semantic Scholar snippet search; OpenReview v1 search with venue terms.
  - **A31:** a blind first pass was no longer possible. It was replaced by a record of whether keyword search finds Ribeiro et al. independently. It does: OpenAlex queries L1-03, L1-18, L2-01, L2-02, and L4-08 all return 2512.07404.
- **Rejected:**
  - **A17,** the human-factors facet. No verdict depends on it.

## 4. Instrument validation (`research/positioning/w4/INSTRUMENTS.md`)

| Instrument | Verdict |
|---|---|
| arXiv full-text search | **FAIL**: `searchtype=ft` is ignored, and the full-text host is off the allowlist |
| arXiv metadata search | PASS (title and abstract only) |
| OpenAlex full-text filter | **PARTIAL**: 1 of 2 known positives found |
| OpenAlex title and abstract search | PASS; daily budget exhausted at about 05:05 IST |
| Semantic Scholar lookups and citations | PASS, with intermittent HTTP 429 |
| Semantic Scholar keyword search | **FAIL**: HTTP 429 throughout |
| OpenReview v1 search | PASS; forum pages and PDFs are behind a browser challenge |
| Crossref | PASS |
| DBLP | FAIL (proof-of-work page) |
| Reading full texts from PDFs | PASS, through arXiv HTML renders or local text extraction |

## 5. L2 occupant finding (`research/positioning/w4/L2_OCCUPANT.md`)

Ribeiro, Spiess, Devanbu, and Nadi, "On LLMs' Internal Representation of Code Correctness" (ICSE
2026, arXiv 2512.07404), occupies the claim that a probe beats stated confidence on code. Its scope
is whole-solution granularity, four 7-8B instruct models, zero-shot categorical verbal readouts, and
no sampling family. Its close citers are 2611.07876, 2608.08266, 2606.14530, and 2607.05188.

Later steps added three findings:

- Ribeiro RQ2 already ranks each model's own samples within a task against verbal confidence. It has no trained readout and no input-only baseline.
- Campos et al. 2611.07876 (concurrent) adds sampling readouts and within-problem AUROC, with no verbal readout.
- CREDO 2609.34857 (concurrent) trains stated confidence on code with execution labels, with no probe.

## 6. Verdict table (`research/positioning/w4/VERDICTS.md`)

| Candidate | Verdict | Strongest surviving residual |
|---|---|---|
| L1 | OCCUPIED (union) as a comparison; NARROW as a protocol; Q10 and Q13 CLEAN (provisional) | estimator set, augmented-test oracle swap, and per-model release split on identical generations with a probe family |
| L2 | OCCUPIED uncontrolled; NARROW controlled and factorial (Q1c, Q2a, Q2b, Q11, Q13) | supervision-matched, within-problem probe versus own-readout comparison, with input-only baselines |
| L3 | routing NARROW (residual restated by TRIAGE 2605.13414); update after a failing test CLEAN (provisional); Q3 and Q6 OCCUPIED | gate by elicited confidence at matched execution budget; confidence change after a shown failing test |
| L4 | NARROW; line level OCCUPIED (Gros and Devanbu 2512.24560); repair residual shrinks (2609.00854, ABSTRACT-ONLY); Q3 CLEAN (provisional) | per-test-group localization |
| F | OCCUPIED; metrology-proper vocabulary used by 2604.26671 and TRACE 2605.03838 | none as a contribution |

No CLEAN verdict is unconditional. Each one rests on the instrument gaps in section 8.

## 7. Ranked recommendation (`research/positioning/w4/RECOMMENDATION.md`)

1. **Controlled disconnect test on an execution-graded measurement layer.**
   - **Contribution sentence:** "On self-generated, execution-labeled code from several open model families, we test whether hidden-state probes carry correctness information that the model's own readouts lack, when every readout receives the same supervision, input-only baselines are included, and discrimination is scored both within and between problems; we report how much of the published probe advantage survives these controls and whether the ranking holds under different calibration estimators, an augmented-test oracle, and a per-model release-date split."
   - **TMLR fit:** criterion 1 is strong because the result is reported whichever way it comes out. Criterion 2 is good.
   - **Main risk:** a concurrent scoop, or a trained readout that closes the gap.
2. **Label-oracle and estimator protocol alone.**
   - **Contribution sentence:** "We show whether the ranking of four confidence families on code (sampling agreement, token probability, stated confidence, and hidden-state probes) changes when execution labels are strengthened with augmented tests, when the calibration estimator changes, and when problems released after each model's training cutoff are separated from those released before."
   - **Role:** the fallback.
3. **Stated-confidence update after a shown failing test.**
   - **Contribution sentence:** "We measure whether a code model's stated confidence changes after it is shown a genuinely failing test, a spuriously failing test, or a placebo, and whether the change predicts repair success."
   - **Role:** a small add-on, CLEAN (provisional).
4. **Confidence-routed execution budgets.**
   - **Contribution sentence:** "On the same generations, we compare routing execution by elicited stated or probe confidence with random routing and a label-sorted oracle at matched execution budgets, stratified by pass rate."
   - **Role:** inside Rank 1 as an offline replay.

**Required answers:**

- **Pivot criteria:**
  - A20: not triggered.
  - A21: triggered for the uncontrolled headline only.
  - A14: open, and a concrete threat because of CREDO.
  - A15: not triggered.
- **Measurement-instrument framing:** used.
- **`src/v4_dprc`:** does not belong in the strongest version.

## 8. Instrument gaps

- **G-FT:** arXiv full-text search failed.
- **G-OA:** OpenAlex full text is partial, and the budget ran out.
- **G-S2:** Semantic Scholar keyword search returned HTTP 429 throughout.
- **G-AX:** the arXiv export API returned HTTP 429 intermittently.
- **G-OR:** OpenReview pages are behind a browser challenge.
- **G-FCS:** some forward-citation screens are partial:
  - the Spiess citation list stopped at 100 entries;
  - the last three G4 seeds were blocked;
  - the Resist-and-Update citers were not screened.
- **Records not fully read:**
  - 2610.19226: abstract only;
  - Crossref 10.1109/tse.2026.3713834: title only;
  - 2609.00854 and OSF 8jq4f: abstract only;
  - OSF qpk9a: no bibliographic record (Crossref 404), so it is not in `references.bib`.

## 9. Deviations (`research/positioning/w4/DEVIATIONS.md`)

**Hosts and tool calls:**

- One call to api2.openreview.net and one to api.datacite.org, neither on the allowlist. Their results were not used.
- One curl to an allowed host with the sandbox disabled, run by a depth investigator without authorization.

**Recoveries by the orchestrator:**

- The G2 forward-citation screen.
- Writes that the harness blocked for the brief critic and the cc-1 agent; the orchestrator saved their returned text.
- 56 tracked claims files that the tool's archive step had moved out of `research/temp/`. They were restored from HEAD, so both copies now exist.

**Tool behavior:**

- `hyperresearch repair` side effects were reverted. The stub notes it created are left uncommitted, and `repair` was not run again.
- At sync time, `hyperresearch search --tag` returned 0 results, so the sync selected notes by frontmatter tag instead.
- The builtin fetcher rejected arXiv PDFs, so fetchers used HTML renders or local text extraction. No note has a `raw_file:` entry, so the sync's `raw/` folder is empty.

**Process:**

- The dossiers ran in parallel with pipeline steps 4 and 5.
- The final report is 13,336 words, over its 10,000-word target. Cutting further would drop evidence; `DIGEST.md` (1,284 words) is the short form.
- LADDER 2610.34737, listed as an unread lead, turned out to have a full-text note in the vault. On reading, it is adjacent and not an occupant.

**Curation:**

- 14 notes still lack the tier or content type field, and lint reports 257 singleton tags. Neither affects any verdict.

## 10. [OPERATOR] items

1. **Network allowlist.** For a short gap-closing pass, add these hosts to the next wave's prompt: search.arxiv.org (arXiv full-text search), api2.openreview.net, api.datacite.org, and osf.io. Alternatively, put a Semantic Scholar API key or an OpenAlex key in a local, untracked environment variable and name the variable in the prompt.
2. **Concurrency window.** Confirm or change the six-month window (works first posted after 2026-05-10) by stating it in the next prompt. If it changes, `VERDICTS.md` gives the effect: L2 Q11 goes back to CLEAN (provisional), and the ranking does not change.
3. **v4 scope.** Confirm that `src/v4_dprc` is recorded as unrun future work. A one-line decision is enough; the orchestrator will add it to `docs/LEGACY.md`.
4. **LLM-use footnote.** Decide the wording of TMLR's first-page footnote disclosing LLM-tool use.
5. **Unread leads.** Before the introduction is drafted, read or authorize fetching these:
   - arXiv 2610.19226;
   - Crossref record 10.1109/tse.2026.3713834;
   - the forward citers of Resist-and-Update 2607.12985;
   - the incomplete G4 forward screens.
6. **Method definitions.** Still open from wave 2: decide the method definitions the new pipeline uses (`docs/s2/METHOD_INVENTORY.md`).
7. **Former GPU host key.** Still open from wave 0: rotate the former GPU host key if it is still live.
