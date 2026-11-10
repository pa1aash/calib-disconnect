# Wave 5 Report: gap-closing literature pass (Part A); Part B not started

Date: 2026-11-10.

**A stop condition fired in Part A.** A fetched full text changed a verdict enough to unseat Rank 1. The concurrent work "Free Lunch for LLMs Confidence: The RL Critic Already Knows" (arXiv 2610.31820) triggers pivot A14 of `docs/s3/POSITIONING_BRIEF_R1.md` section 6. As the wave prompt requires:

- Part A was finished, committed, and pushed.
- This report was written.
- **Part B (the draft pre-registered design, `docs/s5/PIPELINE_DESIGN_R0.md` and `R1.md`) was not started.** No design document, design critics, or disposition file exists.

**Start-state check (Step 0): passed.**

- Tracked files were clean.
- The branch was `main`.
- Local HEAD equaled origin/main at `b9239eb`.
- Both hooks were installed (symlinks to `tools/hooks/`).
- The untracked stubs in `research/temp/` were left untouched.

## 1. Model identifier

- **Orchestrator:** `claude-opus-5-5` (Opus 5.5), not Fable, as recorded at Step 0.
- **Sub-agents:**
  - seven Part A agents ran on the default sub-agent model;
  - the A7 critic ran on opus, as the prompt specifies.

## 2. Commits and checks

Every commit was authored and committed as Palaash Gang. Both hooks ran on every commit, and `--no-verify` was never used.

| SHA | Contents |
|---|---|
| `cfd5b01` | Part A sub-agent records under `research/positioning/w5/parts/` (1,013 files): instruments, dossiers, citation screens, body-text queries, differential cells, critic findings; `.gitleaksignore` entry |
| `9576310` | `research/positioning/w5/INSTRUMENTS.md`, `DIFFERENTIAL.md`; wave 5 change logs in `research/positioning/w4/VERDICTS.md`, `RECOMMENDATION.md`, `DIGEST.md` |

This report and `docs/CONTEXT.md` follow in a third commit.

**Checks:**

- **gitleaks rejection on the first attempt at `cfd5b01`:** 4 generic-api-key findings. The hook rejected the commit and the cause was fixed:
  - **Three findings in a saved GitHub repository page:** anonymous CSRF and upload tokens. The page is not committed; it is kept locally under `scratch/`, and the tracked stub `parts/dossier-A2/raw/github_CDD-TED4LLMs.EXCLUDED.md` records why. No verdict rests on it.
  - **One finding in a Semantic Scholar bulk-search response:** a pagination cursor. It was verified as a false positive and added by fingerprint to `.gitleaksignore`.
  - The commit then passed.
- **gitleaks, full history:** 29 commits scanned, no leaks.
- **Attribution and path scan of staged files:** no home paths and no attribution strings. Lowercase "generated with" occurs in fetched paper text, and the hook's case-sensitive pattern does not match it.
- **Freeze:** no staged change touched a frozen path.
- **Push:** after `9576310`, remote HEAD equaled local HEAD (`9576310d0b0e`).

## 3. Part A results

### Instruments (A1, `research/positioning/w5/INSTRUMENTS.md`)

No Semantic Scholar or OpenAlex key was available: there is no local `.env`, and no key is set in the environment.

| Instrument | Verdict |
|---|---|
| arXiv full text (search.arxiv.org; `search_classic` redirects there) | PASS with a hit cap: 8 of 8 body-only positives (6 from 2026), 0 of 2 controls; indexed to about 2026-11-06 |
| OpenReview api2 keyword search | PARTIAL; every PDF and attachment path returns 403 |
| Semantic Scholar bulk search | PASS |
| Semantic Scholar relevance search | PARTIAL, intermittent 429 |
| Semantic Scholar snippet search | FAIL, 429 throughout |
| Semantic Scholar citations | PASS, paging past 1,000 |
| OpenAlex works search | PASS; the budget has reset |
| OpenAlex full-text filter | PARTIAL, 5 of 8 |
| DataCite | PASS for OSF DOIs |
| osf.io files | FAIL: they redirect to files.osf.io, which is off the allowlist |

**Gaps:**

- **G-AX:** CLOSED.
- **G-FT, G-OA, G-S2, and G-OR:** PARTIAL.

Every remaining CLEAN cell therefore stays CLEAN (provisional).

### Leads and forward screens

- **A2, 2610.19226 (full text).** Its challenge is a single neutral "reconsider" prompt, with no test output. No verdict change.
- **A2, TSE record 10.1109/tse.2026.3713834.** No arXiv copy of the TSE version exists. The dossier reads arXiv 2402.15938v3 (ACL 2024), which has no calibration metric. The match to the TSE paper is unconfirmed, so the TSE-only text is ABSTRACT-ONLY. No verdict change.
- **A3, forward screens.** All are complete or have a named gap:
  - **Resist-and-Update (2607.12985):** 3 distinct citers. The one CLOSE citer, 2611.07913, is a synthetic belief-update study with no code.
  - **G4 seeds:** 2603.18893 complete; 2610.18066 has zero citers; 2504.03359 has an OpenAlex gap of 2.
  - **Spiess (2402.02047):** its true Semantic Scholar total is 100, so W4's "cap" was the real count. No new citers.
- **A5, close dossiers.** Full-text dossiers now exist for Ribeiro (v3), Campos (v1), and CREDO (v1, new). The corrections to W4 numbers are in the VERDICTS change log:
  - Campos "0.620 versus 0.629" is a mismatched pair; the matched comparison under shift is .627 or .540 versus .629.
  - CREDO's untrained Base-d is .782, not .690.
  - The Ribeiro range mixes baselines, and its unit is selection accuracy.

### Body-text re-runs (A4) and verdict changes

| Cell | W4 | W5 | Evidence |
|---|---|---|---|
| L1 Q10 (test insufficiency) | CLEAN (provisional) | NARROW | MARGIN 2605.22949 (concurrent): EvalPlus re-scoring of verbal confidence only (Sec 6.1, Tables 1 and 3) |
| L2 Q1c (controlled comparison) | NARROW | NARROW, at the A20 union boundary | 2610.31820 Sec 4.1, Table 3; Campos Table V prompt-only probe |
| L2 Q10 (probe vs stated confidence, reasoning on, code) | NARROW | OCCUPIED (concurrent) | 2610.31820 Tables 3 and 9, App C |
| L2 Q11 | NARROW | NARROW, CREDO numbers corrected | CREDO Table 1 (Base-d .782) |
| **Pivot A14** | not triggered | **TRIGGERED (concurrent)** | 2610.31820 Table 3: trained own-readout (R-Tuning) within .02 AUROC of a same-label probe on all four code splits |
| L3 Q2/Q7 (update after a failing test) | CLEAN (provisional) | NARROW | Thinking-in-Bets 2610.34654 (concurrent), Sec 3.3, 4.1-4.2 |
| L4 Q1 | NARROW | NARROW, residual shrinks | 2610.34654, requirement-level confidence |

Unchanged:

- **Still CLEAN (provisional):** L1 Q5 (estimator sub-part), L1 Q13, L2 Q9, and L4 Q3.
- **Checked, no change:** L1 Q1, L2 Q13, L3 Q1/Q4/Q5, and F.

**Why Rank 1 is unseated.** R1 section 6 item 3 makes L2 unviable as the spine if the probe-versus-stated-confidence gap on code is "shown to close, in discrimination ... under ... a training method for stated confidence". 2610.31820 does exactly that:

- **Qwen3-8B:** .86 vs .88 in distribution, and .85 vs .84 on LiveCodeBench.
- **Nemotron-Cascade-8B:** .89 vs .89, and .79 vs .80.

The operator decision for this wave says concurrent work is always cited and differentiated. The A7 critic reached the same verdict independently (`parts/critic-A7/FINDINGS.md`, F1 and F2). It also found that Campos already holds the prompt-only baseline, within-problem AUROC, and clustered inference. Together the two works leave only one combination open: a trained readout scored within problem on identical generations.

**Caveats that do not change the A14 test:**

- 2610.31820 scores pooled only.
- Its readout is categorical ("I am sure" or "I am unsure").
- Its grading is "rule-based".
- Its two arms are inferred, not stated, to be scored on different generations.

**RECOMMENDATION.md after wave 5** (proposed, for operator confirmation):

1. The execution-graded measurement protocol (former Rank 2) becomes the spine, following R1 replacement item 1, "L1 plus L3". The controlled comparison and the routing replay run as analyses on the same generations.
2. The controlled comparison as a stand-alone headline is not recommended while concurrent works are in scope.
3. The update-after-failing-test study is now NARROW and stays out of the main paper.

## 4. Differential table, condensed (`research/positioning/w5/DIFFERENTIAL.md`)

Cells are P (present), Pa (partial), and A (absent). The table was corrected after the A7 critic.

| Control | Ribeiro | Campos | CREDO | Spiess | CaC (2610.31820) | NeuroSym-Cal |
|---|---|---|---|---|---|---|
| Supervision-matched readouts | A | Pa | Pa | Pa | Pa | A |
| Trained stated-confidence readout | A | A | P | A | P | A |
| Prompt-only baseline | A | P | A | A | Pa | A |
| Code-text-only baseline | Pa | A | A | Pa | Pa | Pa |
| Within-problem scoring | P | P | A | A | Pa | A |
| Oracle swap of test suites | A | A | A | Pa | A | A |
| Release or contamination split | A | A | A | A | A | Pa |
| Calibration estimator set | A | A | Pa | Pa | A | A |
| Clustered paired inference | Pa | P | A | A | A | A |
| Base versus instruct | A | A | A | A | A | A |
| Same-weights reasoning on/off | A | Pa | A | A | A | A |
| Routing replay (random and oracle) | Pa | A | Pa | A | Pa | Pa |

**Columns.** The two next-closest works are:

- **CaC (2610.31820):** next-closest on the readout side. It replaces RLCM 2604.23333, which is kept as a supplementary column.
- **NeuroSym-Cal:** next-closest on the measurement layer.

**Residual.** No column is present on these eight rows:

- supervision matching;
- code-text-only;
- oracle swap;
- release split;
- estimator set;
- base versus instruct;
- reasoning toggle;
- routing replay.

Base versus instruct is absent everywhere. The oracle swap residual narrows further outside the table: MARGIN does it for verbal confidence only.

## 5. Primary hypothesis, delta, and outcome statements

**Not produced:** Part B was not started (stop condition).

**Carried forward for the design wave:** a design-stage power simulation, kept locally in `scratch/w5-power/` (untracked; numpy only, deterministic seed). It was run during Part A, before the stop fired. It is planning arithmetic under stated assumptions, not a result, and it will be re-run for whatever primary contrast the operator chooses. Its setting:

- the pair-weighted within-problem AUROC gap;
- delta 0.03;
- a problem-clustered bootstrap.

## 6. Model and benchmark matrix

Not produced (stop condition). No model card was fetched in this wave.

## 7. Compute budget

Not produced (stop condition).

## 8. Critic findings and dispositions

The Part B critics (methodologist, TMLR reviewer, and budget) did not run. These are the A7 critic's top findings and how each was handled:

| Finding | Severity | Disposition |
|---|---|---|
| F1: A14 triggered, not "near-triggered" | critical | Accepted. VERDICTS and RECOMMENDATION updated; stop condition applied |
| F2: Rank 1 controls at the A20 union boundary (2610.31820 plus Campos) | critical | Accepted. L2 Q1c relabeled |
| F3: residual sentence; five novelty sentences that must cite 2610.31820 | critical | Accepted. Listed in RECOMMENDATION wave 5 update |
| F5: L2 Q10 changed by 2610.31820 | major | Accepted. OCCUPIED (concurrent) |
| F7: prompt-only baseline is not residual (Campos Table V) | major | Accepted. Removed from residual statements; kept as a required baseline |
| F9: 2610.34654 also narrows L4 Q1 | major | Accepted |
| F11 to F16: six DIFFERENTIAL cells or wordings wrong | major and minor | Accepted. Cells corrected, with a correction log in DIFFERENTIAL.md |
| F18: CREDO Base-d .782 | major | Accepted. Verified in the CREDO full text, then logged |
| F19: W4 sentences to change | major | Accepted in part. Changed cells are edited in VERDICTS, with a change log in VERDICTS and RECOMMENDATION and a banner on DIGEST. The W4 body text of RECOMMENDATION and DIGEST is kept as the record, not rewritten line by line |
| F6: self-consistency beats the probe out of distribution in 2610.31820 | major | Accepted into RECOMMENDATION's list of cite-required sentences; the A4b dossier itself was not edited |
| F20: no fabrication found | | Noted. Not verified: Miglani 0.677 vs 0.703 (W4), the TSE-only text, R-Tuning generations, and the 2610.34654 bug-report content |

## 9. Deviations and open decisions

**Deviations:**

- **One off-allowlist request:** A2 requested raw.githubusercontent.com once. The content was discarded and not used.
- **A blocked write:** the harness blocked the A7 critic's write to its file, so the orchestrator saved its returned text verbatim, as in W4.
- **Early Part B preparation:** the power simulation was written during Part A, while agents were still running, as preparation for Part B. After the stop fired it was moved out of the tracked tree and was not committed.
- **Excluded raw file:** one GitHub page was left out of the commit because of gitleaks (see section 2).

**Open decisions:**

- the spine after A14 (section 10, item 1);
- whether concurrent works count for the pivot rules;
- whether the next wave writes the design for the replacement spine.

## 10. [OPERATOR] items

1. **[OPERATOR] Confirm the replacement spine, or override the stop.** Either option resumes Part B in a new wave prompt.
   - **Option A:** confirm that the measurement protocol (L1 plus L3 replay), with the controlled comparison as an analysis, is the spine. Reply "Confirm W5 replacement spine", and the next wave writes `PIPELINE_DESIGN_R0.md` for it.
   - **Option B:** rule that concurrent works do not trigger pivot criteria, so the former Rank 1 stands. State this in the next prompt.
2. **[OPERATOR] Decide the pivot scope of concurrent work.** The wave prompt says concurrent work "is always cited and differentiated" and that the six-month window decides what must be compared experimentally. It does not say whether a concurrent work can trigger A14. One sentence in the next prompt settles it.
3. **[OPERATOR] Decide whether 2610.31820 is a required experimental comparison.** It was posted 2026-10-22, inside the six-month window. Either name it a required experimental comparison or accept discussion only. Its checkpoints are PPO-trained by its authors, and whether they are released was not checked.
4. **[OPERATOR] Optional API keys.** To close G-S2 and G-OA, put a Semantic Scholar or OpenAlex API key in a local, untracked `.env`, and name the variable in the next prompt.
5. **[OPERATOR] Carried over and still open:**
   - the TMLR LLM-use footnote wording;
   - the method definitions (`docs/s2/METHOD_INVENTORY.md`);
   - rotating the former GPU host key, if it is still live.
