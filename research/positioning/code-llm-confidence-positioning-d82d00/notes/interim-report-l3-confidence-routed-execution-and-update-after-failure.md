---
title: Interim report — l3-confidence-routed-execution-and-update-after-failure
id: interim-report-l3-confidence-routed-execution-and-update-after-failure
tags:
- code-llm-confidence-positioning-d82d00
- locus-l3-confidence-routed-execution-and-update-after-failure
created: '2026-11-10T08:43:05.560586Z'
status: draft
type: interim
deprecated: false
summary: 'L3 NARROW: no occupant routes execution by elicited verbal/probe confidence
  vs random and attainable oracle on code; update-after-failing-test CLEAN (provisional);
  positives use trained gates, negatives use pass-rate priors'
---

# Interim report: l3-confidence-routed-execution-and-update-after-failure

**Locus question:** Whether confidence-routed execution budgets beat random and approach oracle routing on code, and whether verbal confidence updates after observed test failures (R1 L3 questions 1 to 7).
**Flavor:** dialectical

Scope: R1 section 2 L3 Q1-Q7 and section 4 verdict rules. Instrument gaps this run: arXiv export API returned HTTP 429 (all searches after the first burst; one first-burst query returned 6 irrelevant hits); Semantic Scholar citations for 2611.06372 returned HTTP 429 (two attempts, 4 s and 12 s backoff); OpenAlex budget exhausted per wave note. Citations for 2512.24661 succeeded (retrieved 2026-11-10). Every "none found" below is therefore a gap, not a zero. All papers were read in full text from vault notes (HTML or PDF extraction) unless marked.

## What the corpus already said

The width sweep found eight L3-adjacent works and the loci analyst split them into "gating helps" and "gating does not help". The loci rationale carried two errors I corrected on reading: swe-router is not a "little gain" paper (it beats a random band), and 1introduction (2608.14659) tests regeneration, not execution-budget routing. Notes: [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]], [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]], [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]], [[swe-router-routing-in-multi-turn-agentic-software-engineering-tasks]], [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]], [[1introduction]], [[do-large-language-models-know-what-they-are-capable-of]], [[260712985-resist-and-update-counterfactual-report-coordinates-full-text]], [[not-one-belief-answer-payloads-persistence-and-dissociated-confidence-signals-in]].

## What the new sources say

Three new fetches (budget 8; none needed beyond them). Found by Semantic Scholar forward citations of 2512.24661.

**[[agentic-uncertainty-reveals-agentic-overconfidence]]** (Kaddour et al., arXiv 2602.06948, Feb 2026; preprint). Full text. Elicits stated success probability pre-, mid-, and post-execution for GPT-5.2-Codex, Gemini-3-Pro, Claude Opus 4.5 on 100 SWE-bench Pro tasks (Sec 3). Mid-execution (Sec "Mid-Execution: Uninformative Doubt", Table 1) at 25/50/75% of steps: agents "develop 'cold feet': confidence decreases as they observe their partial work, but this doubt is uninformative, occurring equally for successes and failures"; AUROC GPT ~0.53 flat, Gemini 0.49 to 0.64, Claude 0.62 to 0.52. Post-execution GPT predicts 73% vs 35% true. Critically, Sec 2.2.1 gives the agent read-only access: "the agent cannot execute code, run tests", so no failing test is ever observed. This is the closest occupant of "does stated confidence update with accruing execution evidence" at trajectory granularity, and it does not reach the test-failure question.

**[[capability-self-assessment-in-large-language-models]]** (Yang, Shirkavand et al., arXiv 2606.00251v2, Sep 2026). Full text. RLVR-trained solve-or-delegate policy. Table 7 (math routing to Qwen3-235B-A22B): Random 0.65/0.72, CSA 0.73/0.80, Cloud-only 0.86 for Qwen3-1.7B/4B; "improving over random routing by about 8.2 percentage points at matched cloud-call budgets". Code appears only as transfer (Table 5, 722 Python problems): assessment M-F1 0.36 to 0.64 (1.7B), 0.41 to 0.63 (4B), pass@1 unchanged. Matched-budget random baseline exists, but math, a trained binary decision rather than elicited confidence, no code routing utility.

**[[ladder-diagnosing-domain-level-self-assessment-under-noisy-feedback]]** (arXiv 2610.34737). Full text. Domain-level self-assessment from noisy feedback across 18 models; code not a domain (searched: code, test in body); only cites BigCodeBench/SWE-bench prediction work. Tangential: it shows the valid-versus-noisy-feedback contrast is being built as a design, at domain not program level.

## Evidence synthesis

Routing against random. The positive code results all use a learned or proxy gate, not elicited confidence. Heteroskedastic-signals (Sec 5 Setup; Table 1) is a replay on MBPP with Qwen3-8B, LLaMA3-8B, GPT-4o-mini: Rand .551, Thr .636, CST .671, Oracle 1.00 at beta=10% (Qwen3, err=.558). Caveats from the text: costs are synthetic (proxy cost vs true cost correlation about 0.3), "We add 10% Bernoulli label noise and Gaussian proxy noise", the signal is a logit-margin/token-probability proxy, "Oracle signal: replacing proxy signals with true labels yields perfect hit rate", i.e. the oracle is the label itself, so "approaches oracle" is not informative; the CST-minus-Threshold gain at 10% has CI [-0.2, +7.0]. Its own finding is that signals are near-random in some strata. SWE-Verifier (261030284, Table 1) gates step-level sampling with a trained Qwen3.5-4B score: MiniMax-M2.7 75.47±1.40 to 77.20±0.87 at 1.09x cost, 3.43% steps verified; all-step self-verification 75.27 at 3.35x; Oracle@3 82.20 at 3.00x is a trajectory-level best-of-3 oracle, not a routing oracle, and Table 2 ablates untrained vs trained gates, never a random gate at matched rate. SWE-Router (2607.00053, Sec 5, Table 2) uses a trained 7B value head on partial trajectories; Route-AUC normalizes 0 (cost-proportional interpolation, i.e. random) to 1 ("matches the strong model's resolved rate at the weak model's cost"), reports 0.780 with deepseek-v3.2 (+15.3 pp over non-temporal baseline) and a curve "above the random-assignment band". This is the only SWE work with a normalized random-to-ideal scale, but its model-pair routing is not execution-budget routing and the 1.0 anchor is not an attainable oracle. CoTT (2609.12489, Table 1) gates test-output generation by sampling agreement: cost $0.077 to $0.065, no random or oracle arm. Adaptive-Consistency (2305.11860) stops sampling on agreement, up to 7.9x fewer samples at <0.1% accuracy drop, again without random/oracle routing. CodeRefuser (2605.17029, Table 1, Fig 3) is risk-controlled abstention on code (Learn-Then-Test, alpha=0.2, MBPP Qwen2.5-Coder-32B abstains about 30% vs over 80% for perplexity) and is the occupant for selective prediction with coverage control on code (Q3), but its signal is execution consistency over generated tests and it reports abstention precision/F1 against an oracle-derived label.

Negative side. Give-Up-to-Get-More (2611.06372, Table 1) shows difficulty-proportional rules capture 50 to 100% of oracle gain on easy workloads but "at most 13%" on hard ones even with true pass rates; CodeContests Llama-3-8B (mean p 0.021, oracle gain +4.8 pts): IAS 1%; Llama-3-70B 2%. With a verifier, Thompson sampling needs a history prior with rank correlation above roughly 0.3 to 0.55; Table 3 shows LLM-derived priors (rating, P(solvable), NLL) give Spearman 0.10 to 0.46 and gain -2.1 to -0.1 vs round-robin. Important scope limit: its priors are pass-rate priors and zero-shot difficulty ratings of problem text, not post-generation verbal confidence or probes, and it claims "no claim about novel user queries". Hard-Issue (2611.08285, RQ2) shows trajectory failure predictors reach about 0.62 AUROC vs 0.92 for an issue-difficulty reference, gain beyond difficulty and ability is equivalent to zero (TOST ±0.02), and the oracle gap (best 76.8% vs any-model 86.8%) is not above chance and not attainable (45% of failures have no model to switch to). 1introduction (2608.14659, Table 1 and Sec 5): uncertainty-triggered regeneration lowers Pass@1 in 5 of 6 configs, verbalized-confidence Pearson -0.327/-0.090/-0.114 for small instruct models, verification-based regeneration +6 to +26 pp; conclusion that uncertainty serves as "gating signals for costlier execution-based correction loops" is asserted, not tested against a random gate.

Update after failure. No fetched record measures stated confidence before and after observing a failing test on the same program, with a repair-outcome label, and with a valid-versus-spurious failure contrast (searched in vault full text; arXiv/S2 keyword search unavailable, so a gap). Nearest: Barkan et al. (2512.24661, Exp. 2-3) restate confidence per tool call on SWE-bench Verified (Claude AUROC rises then falls below the step-1 value; OpenAI models improve step by step) and after in-context contract outcomes, which are task-level, not test failures on the same code; Kaddour (above) shows uninformative doubt with tests unobservable; Resist-and-Update (2607.12985) and Not-One-Belief (2610.35694) give a design pattern (known-posterior evidence vs pressure; payload vs speech act) and show confidence can move with persistence or pressure, but are non-code QA. Iscan (2606.31511) decomposes feedback content for self-repair with a placebo arm on 0.5B-1.5B models, finding "blind resampling beat bare-code retry by +18 net unlocks"; it never elicits confidence.

### Position A: confidence gating helps (steelman)
Heteroskedastic (+3.4 to +17.0 pp for CST), SWE-Verifier (+1.73 pp at 1.09x), SWE-Router (above the random band), CSA (+8.2 pp over random at matched calls) all show a cheap score concentrates costly computation better than random, and CodeRefuser shows risk-controlled abstention on code is feasible. The mechanism is sound and mostly requires the score to be informative within the competing pool.

### Position B: little or no gain, no update (steelman)
Each positive result is conditional on a trained or in-domain gate, a weak-model-hard-workload split, or injected noise; Give-Up and Hard-Issue show that on hard workloads the usable signal is mostly difficulty, which routing by a prior cannot exploit, and the oracle ceiling is mostly unattainable. Uncertainty-triggered regeneration harms. Confidence moves with persistence and pressure, and is uninformative when it moves in agentic runs.

## Committed position

Both camps are measuring different things, so the dispute is partly definitional, and the part that is real favors a narrow, conditional version of Position A: a gate beats random only when its signal's within-pool rank correlation with execution outcome clears roughly 0.3 to 0.55 (the Give-Up break-even) and the workload is not mostly hopeless (mean pass rate above about 0.1), and no fetched work establishes that an elicited verbal or probe confidence from a code model clears it under execution-graded labels with a matched random arm and an attainable oracle. The L3 routing component is therefore NARROW, not OCCUPIED: no occupant combines (i) elicited verbal or probe confidence as the gate, (ii) execution-graded labels without injected noise, (iii) random and an attainable (label-sorted at equal budget) oracle at matched budget on code. The load-bearing reason is that every positive occupant uses a different signal class (logit proxy, trained verifier, trained value head, RLVR policy) and every negative occupant uses a different budget unit (pass-rate prior, regeneration, model switching). The update-after-failure component is the cleaner one: NARROW toward CLEAN (provisional), because the nearest works (Kaddour, Barkan) show uninformative or model-dependent drift without ever showing the model a failing test, and the valid-versus-spurious contrast exists only in non-code work.

- **Position:** Confidence-routed execution budgets are a defensible, narrowly scoped L3 claim, but as an offline replay with a matched random arm and an attainable oracle on execution labels, not as a headline "confidence routing works" claim; an honest negative is as publishable as a positive.
- **Verdicts (provisional):**
  - L3 Q1/Q4/Q5 routing vs random and oracle on code with elicited verbal/probe confidence: **NARROW**. Residual: elicited verbal or probe confidence from the code model as the gate, execution-graded labels, matched-budget random and label-sorted oracle, offline replay. Closest on the signal side: SWE-Verifier (trained verifier gate, no random arm, Table 1-2) and Heteroskedastic (logit proxy, 10% injected label noise, Table 1); closest on the budget-unit side: Give-Up (pass-rate priors, CodeContests, Table 1/3) and 1introduction (regeneration triggers, n small). Concrete reason code could differ from NLP: execution labels are binary with hidden-test coverage limits and pass rates are very low on hard code (CodeContests mean p 0.021), the regime where Give-Up shows difficulty-proportional rules fail.
  - L3 Q3 selective prediction with coverage and risk on code: **OCCUPIED** by CodeRefuser (Table 1, Fig 2-3) for generation abstention with risk control; do not claim it.
  - L3 Q6 uncertainty/abstention for repository agents: **OCCUPIED (union)** for the step/trajectory unit by SWE-Verifier, SWE-Router, Kaddour; residual only on signal class.
  - L3 Q2/Q7 (A7) verbal confidence update after an observed failing test, tracking repair outcome, valid vs spurious: **CLEAN (provisional)**. Gaps: arXiv full-text search failed, S2 keyword search 429, OpenAlex 429, arXiv export 429 after the first burst; forward citation screen done only for 2512.24661 (16 citers screened by title); 2611.06372, 2610.30284, 2608.14659 citers not screened. Nearest and not occupying: Barkan Exp. 3, Kaddour mid-execution (tests unobservable), Resist-and-Update/Not-One-Belief (non-code), Iscan (no confidence). Do not claim novelty without hedging.
  - L3 as a whole: **NARROW**.
- **Confidence:** medium (55 to 65%) for NARROW on routing; medium-low (45 to 55%) for CLEAN (provisional) on update-after-failure, because the instrument gaps bear directly on a body-text claim and a one-paragraph experiment inside an agent paper would not appear in titles/abstracts.
- **Boundary conditions:** Holds for Python function-level generation and SWE-style agents, 2022 to Nov 2026, with elicited stated or probe confidence as the gate. Does not extend to learned verifiers/reward models (occupied territory), to sample-count allocation with pass-rate priors (Give-Up occupies), or to human-in-the-loop triage.
- **What would change this position:** (1) A code paper that routes execution or sampling by elicited verbal/probe confidence with a matched random arm and a label-sorted oracle (move to OCCUPIED); (2) any code study showing confidence before and after a shown failing test with a spurious-failure arm (update component to NARROW or OCCUPIED); (3) an empirical result in our own replay where AUROC of the verbal gate is below about 0.6 with pass rates below 0.1, which would make Position B correct for our setting and the paper a negative-result contribution; (4) a successful S2/arXiv/OpenAlex citation screen of the three closest occupants.
- **Evidence weight:** 9 full-text studies read (4 code-routing positives with non-elicited gates, 3 negatives/conditional, 2 on revision) plus 3 new full-text fetches; zero direct occupants for the narrow residual; two key instruments failed so CLEAN is provisional. Strongest for TMLR: claim is supported by evidence the paper itself generates; interest is moderate, since TMLR wants correctness and L3 adds utility to an L1/L2 measurement paper rather than carrying it alone.
- **Prescriptive spec for the replay design:** compare the gate against Random and a label-sorted Oracle at equal budgets beta in {10, 20, 30, 50}% with 10 or more seeds, report paired gain with 95% CI (Heteroskedastic's CI [-0.2, +7.0] at 10% shows a single point is not enough), stratify by mean pass rate (below 0.1 versus above 0.4) because Give-Up's 13% ceiling predicts the hard stratum fails for every gate, and use unmodified execution labels (no injected label noise). For the update question, use paired programs with a genuine failing test, a spurious failure (executed test that is wrong), and a placebo, following the evidence-vs-pressure design of Resist-and-Update; report change in stated confidence and its AUROC against repair success.

## Open questions

- Does the 2606.31511 follow-up or Iscan's program include confidence elicitation? Not found in body.
- Citation screens of 2611.06372, 2610.30284, 2608.14659, 2607.00053 not run (S2 429); recommend a retry window.
- Huang et al. 2025 (cited by Give-Up as sampling until a confidence threshold) was not fetched; non-code, lead only.
- Which hidden-test coverage level makes the label itself noisy enough to undo a routing gain (R1 L1 Q10)?

## Sources

1. [[heteroskedastic-signals-in-budgeted-llm-verificationstructural-heterogeneity-lim]] Table 1, Sec 5 setup
2. [[give-up-to-get-more-priors-not-policies-govern-test-time-compute-allocation]] Tables 1 and 3, 2611.06372
3. [[261030284-swe-verifier-selective-verification-for-coding-agents-full-text]] Tables 1-2, 2610.30284
4. [[swe-router-routing-in-multi-turn-agentic-software-engineering-tasks]] Sec 5, Table 2, 2607.00053
5. [[hard-issue-weak-model-or-bad-runrethinking-failure-prediction-for-coding-agents]] RQ2, 2611.08285
6. [[1introduction]] 2608.14659
7. [[do-large-language-models-know-what-they-are-capable-of]] 2512.24661
8. [[260712985-resist-and-update-counterfactual-report-coordinates-full-text]]
9. [[not-one-belief-answer-payloads-persistence-and-dissociated-confidence-signals-in]]
10. [[agentic-uncertainty-reveals-agentic-overconfidence]] (new)
11. [[capability-self-assessment-in-large-language-models]] (new)
12. [[ladder-diagnosing-domain-level-self-assessment-under-noisy-feedback]] (new)
13. [[260517029-task-abstention-for-large-language-models-in-code-generation-full-text]]
14. [[falsification-not-exposure-placebo-controlled-decomposition-of-self-repair-feedb]]
15. [[confidence-gated-transductive-test-generation-for-code-reranking]]
16. [[lets-sample-step-by-stepadaptive-consistency-for-efficient-reasoning-and-coding]]
