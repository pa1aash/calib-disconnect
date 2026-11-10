# Cell verdicts after the body-text re-run (wave 5, Part A, sub-part A4b)

Run date 2026-11-10. Instruments and every query are in `QUERIES.md`. The primary instrument was arXiv full-text search (search.arxiv.org): 37 queries, up to 100 hits each, every page returned HTTP 200 after one retry. Secondary instruments: OpenAlex (10 queries), OpenReview v2 (5 queries), and Semantic Scholar (3 queries, all HTTP 429, a gap). Every work below that could occupy a cell was read in full text (`raw/ft/`). Dossiers for new close works are in `dossiers/`. Status tags follow A23. "Concurrent" means first posted after 2026-05-10.

## RANK 1 THREATS

**T1. 2610.31820, "Free Lunch for LLMs Confidence: The RL Critic Already Knows" (concurrent, arXiv v1 2026-10-22; dossier `dossiers/2610.31820.md`).** This is a partial scoop of the Rank 1 controlled disconnect test (L2 Q1c and Q11). It does not unseat Rank 1, but it takes the pooled headline that W4 listed as missing.

- **What it already does on code.** It compares a trained own-readout (R-Tuning, which fine-tunes the policy to append "I am sure" or "I am unsure" and scores the confidence-token probability) with a linear probe on the policy's last-token activations fit "with the same labeled data" (Section 4.1). It adds zero-shot verbalized probability, 8-sample self-consistency, and the PPO critic. The models are Qwen3-8B and Nemotron-Cascade-8B with thinking on (Appendix C). Code is in distribution on held-out TACO, CodeContests, and Codeforces, and out of distribution on LiveCodeBench. Results are in pooled AUROC, ECE, and Brier (Table 3; per-benchmark Table 9).
- **Code AUROC, trained readout against probe (Table 3).**
  - Qwen3-8B: in distribution .86 vs .88; LiveCodeBench .85 vs .84.
  - Nemotron: in distribution .89 vs .89; LiveCodeBench .79 vs .80.
  - Zero-shot verbalized confidence: .58 to .61.
  - So under matched supervision the trained readout ties the probe on code: the gap is at most .02 in all four code splits.
- **Input-only baseline, partly done.** Section 2, Table 1 trains external models of similar size on the target policy's (question, response, correctness) triples, and these read text only. They match self-estimation on code: APPS AUC .84 (self) vs .82 and .86 (external); TACO .89 vs .80 and .90. This is a candidate-text-only baseline in all but name, though for the R-Tuning format only.
- **Consequence for pivot A14 (VERDICTS.md L2, criterion 3).** W4 said A14 was not triggered because no work had "same-sample AUROC comparison with a probe". That condition is now nearly met on code at the pooled level. The one exception: R-Tuning fine-tunes the policy and lowers its accuracy on 15 of 16 splits (Section 4.2, Table 2), so the trained arm is scored on different generations from the probe arm. I recommend the operator treat A14 as **effectively triggered for any pooled, uncontrolled headline**. The Rank 1 headline must therefore be the controlled residual below, not "probes beat stated confidence on code."
- **What Rank 1 still owns (residual).**
  - The probe, a trained numeric own-readout, and zero-shot verbal and categorical readouts, all on identical self-generated code samples, with explicit execution labels. 2610.31820 says only "rule-based grading" (Appendix C).
  - Prompt-only and candidate-text-only baselines for the probe itself.
  - Within-problem scoring next to pooled scoring. 2610.31820 is pooled only.
  - The base and instruct factor and the same-weights reasoning toggle. 2610.31820 has thinking on only.
- **Novelty sentences to drop or cite.** Any claim that supervision-matched probe and trained-readout comparisons on code are new must cite 2610.31820. So must any claim that text-only estimators match self-estimators on code.

**No other Rank 1 threat found.** I screened every scoop query (SC-1 to SC-12, OA-SC-1 to 3, OR-2, OR-5) and read these full texts. None of them occupies the probe versus trained-readout comparison on code:

- 2606.00251 (Capability Self-Assessment): query-level; the probe or adapter is compared on Math and Science only (Section 4, "Why retention matters": 0.62 to 0.73 M-F1 on Math, 0.51 to 0.56 on Science); coding is zero-shot transfer only (Section 4, Table 5).
- 2610.03894 (Proxy Confidence): a surrogate model's log-probabilities, no probe of the agent.
- 2608.07528 (Knowing-Saying Gap): multi-hop arithmetic, not code.
- 2609.33886 and 2604.24070: factual QA.
- 2610.06216: MATH, pre-generation probes.
- 2609.33220: failure disclosure under GRPO, no probe-versus-trained-readout AUROC.
- 2509.10625: question-only probes, trivia.

The within-problem verbal queries returned only adjacent hits: SC-2 had 3 hits and SC-11 had 65, and only previously known code-probe works occupy anything there (2611.07876, 2609.36783, 2610.05572).

## L2 Q9 sub-part: reasoning-trace signals beat the final stated number, on code

**Verdict: stays CLEAN (provisional).** This took 11 queries: Q9-1 to Q9-8, OA-Q9-1 and 2, and OR-4.

- **New evidence.** Playing Psychic 2604.16931 (preprint; dossier `dossiers/2604.16931.md`) shows that thought-tree features of DeepSeek-R1 and QwQ-32B traces predict correctness on CRUXEval, SAFIM, and CodeLingua, "up to 89%" (Section 1, Figure 6). It has no stated-confidence, token, or probe comparison. So the non-comparative claim, "trace signals predict code correctness," is occupied. The comparative claim, "they beat the final stated number," is not.
- **Read and not on code.** These were read in full text and none uses a code benchmark (counts of LiveCodeBench, HumanEval, MBPP, BigCodeBench, and SWE-bench are all zero):
  - RMCB 2601.08134: math, finance, medical, and legal domains (Appendix B.3, B.4).
  - 2609.32470: 16 math and general reasoning benchmarks.
  - SELFDOUBT 2604.06389: MMLU and GPQA.
  - 2610.18614: ALFWorld and WebShop.
  - 2607.01612: MMLU and GSM8K.
  - Also 2606.11211, 2610.11352, 2605.07776, and 2610.36709.
- **Read, code but no stated-number comparison.** 2611.06095 and 2610.36952 study reasoning cost against code correctness with no confidence readout. 2602.09832 is about "coding" in the sense of annotating classroom discourse, not program synthesis.
- **Remaining gaps.** Semantic Scholar search returned 429. The OpenAlex full-text phrase search returned 0, which is a gap under G-OA. arXiv full-text search covers arXiv only, so venue-only papers are unscreened.

## L3 Q2/Q7: stated confidence updates after a shown failing test; valid versus spurious failures; whether the update tracks repair success (code)

**Verdict: moves from CLEAN (provisional) to NARROW.** This took 15 queries: L3-1 to L3-10, OA-L3-1 to 3, OR-1, and S2-2 (which returned 429).

- **Closest work.** Thinking-in-Bets 2610.34654 (concurrent; dossier `dossiers/2610.34654.md`). On code (SWE-Together, SWE-Interact, DeepSWE), it records requirement-level stated confidence before and after user feedback. Requirements are scored by the test suite, and a hidden test decides whether a review complaint is valid or mistaken (Sections 3.3 and 4.1).
  - It finds that a complaint "without a failing test case" lowers confidence "by roughly the same amount on satisfied and unsatisfied requirements" (Section 4.2, Figure 3a; 10,323 requirement checks).
  - It reports false reversals (12.2% vs 0.02%) and successful corrections.
  - That covers the update after feedback, the split by ground truth, and valid versus mistaken feedback, all on code.
- **Residual (one sentence).** The update after a *shown executed failing test*, with valid tests contrasted against spurious tests (a wrong oracle), and whether the size of the update predicts repair success. 2610.34654 uses natural-language complaints, and its mistaken complaints carry no failing case (Section 4.1, Section 5 limitations). It does not report update magnitude as a predictor of repair.
- **Closest on each side.**
  - Feedback side: 2610.34654 (complaints, Gemini only).
  - Test side: Iscan 2606.31511 (repair with tests, no confidence; W4).
  - Adjacent: 2604.05397 (multi-turn calibration under persuasion, non-code); LADDER 2610.34737 (W4, non-code).
- **W4 abstract-only lead resolved.** 2610.19226 is now read in full text. It covers task-feasibility beliefs and the response to a single challenge on Terminal-Bench 2.1 and tau2-bench (Abstract, Section 2), with no executed failing test. It is adjacent and does not occupy this cell.
- **Read and not occupying.**
  - 2608.04355: intrinsic self-correction with no external feedback.
  - 2605.24693 (CP-Agent): "probe" is a hypothesis-testing action, not a confidence readout.
  - 2607.28457 (SVR): no code benchmark.
  - 2610.19596: no confidence.
  - 2610.14662, 2611.06863, 2609.28150, 2610.37859, 2605.28010, and 2610.22139: no stated-confidence update after a test.
  - 2609.00652: a Contexto search, not code.
  - 2610.18082: belief states over repair frontiers, not stated confidence.
- **Remaining gaps.** Semantic Scholar returned 429. OA-L3-1 (0 hits) and OA-L3-3 (1 hit, MutaBot) are gaps under G-OA. W4's forward-citation gap (G-FCS) for 2611.06372, 2610.30284, and 2608.14659 was not addressed here.

## L4 Q3: adequacy of self-written tests versus own confidence

**Verdict: stays CLEAN (provisional).** This took 11 queries: L4-1 to L4-7, OA-L4-1 and 2, OR-3, and S2-3 (which returned 429).

- **New adjacent evidence.** None of these measures the model's stated or internal confidence:
  - 2607.28871: in repair agents, 46.0% of positive validation events carry no bug-discriminating information (Abstract).
  - 2609.38812: terminal agents detect only 61.43% of their incorrect candidates during self-verification (Abstract).
  - 2602.07900: agent-written tests on SWE-bench Verified do not change resolution totals significantly (Abstract).
  - OpenReview Yhu7RTmtrJ: buggy code misguides generated tests.
  - 2610.32548 (W4): adequacy without confidence.
- **Residual unchanged.** Test adequacy (mutation or coverage of the model's own tests) set against the model's own confidence in its code.
- **Remaining gaps.** Semantic Scholar returned 429. The OpenAlex full-text phrase search returned 0, which is a gap. The small hit counts on the exact-phrase queries (L4-3: 3, L4-4: 9, L4-7: 3) show the phrasing is rare, but body-text recall is still limited to arXiv.

## Scoop-check cells (L2 Q1c, Q11, Q13): verdict updates

| Cell | W4 | After A4b | Change |
|---|---|---|---|
| L2 Q1c controlled comparison | NARROW | **NARROW, residual smaller** | 2610.31820 covers supervision-matched probe vs trained own-readout on code (pooled), with text-only external estimators (Section 2). Residual: identical generations, prompt-only and candidate-text-only baselines for the probe, within-problem scoring, numeric trained readout, execution labels, and the base/instruct and reasoning factors. |
| L2 Q11 trained stated confidence on code vs probe | NARROW | **NARROW, near OCCUPIED for pooled AUROC** | 2610.31820 Table 3: trained readout within .02 AUROC of the probe on all 4 code splits. Pivot A14 is effectively triggered for a pooled headline (see T1). If the operator rules concurrent work out of scope, this returns to W4's NARROW. |
| L2 Q13 pooled vs within-problem | NARROW | **NARROW, unchanged** | No new code work scores verbal or trained readouts within problem; 2610.31820 is pooled only (Appendix C). |

## Gaps that bear on every verdict above

- Semantic Scholar keyword search returned HTTP 429 on all 18 attempts.
- OpenAlex full-text phrase search returned 0 for 4 of 6 phrases, which counts as a gap under G-OA.
- For the OpenAlex `search=` queries, only the first 50 results were screened.
- OpenReview v1 returned 429 on 3 of 5 queries. v2 answered all 5, but forum full texts were not fetched.
- arXiv full-text search does not cover venue-only papers.
- Forward-citation screens of 2610.31820 and 2610.34654 were not run. Both are under three weeks old.
