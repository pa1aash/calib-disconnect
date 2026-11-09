# Orchestrator notes — aaai-bar-eval-dprc-d78e07

## Fetcher 1 (competitors+utility+scoop) RESULTS
- DCPO: scalar, whole-response, general reasoning (RLVR), not code-per-requirement. Foil for granularity.
- CURE: closest analog — self-reports per-CLAIM confidence (SFT+RL), +16pp AUROC, but NL fact-verify
  labels not execution. DPRC's execution oracle is the cleaner-signal differentiator.
- FLARE: separate diagnostic model, line-level; +1.72-7.42pp Pass@1 from spatial localization →
  downstream utility from localization is REAL (but spatial, external, not self-expressed).
- Gros&Devanbu: per-line/span, external white-box probe, edit-likelihood. Distinct axis.
- **SCOOP: UT-Dallas "Beyond Execution"/"Beyond Confidence" STILL UNPUBLISHED (no arXiv). Timing risk
  DOWN — can't cite/scoop us yet. Their published sibling = abstention+repair framing.**
- **Code-MUE (ISSTA'26): execution-grounded uncertainty w/ MEASURED downstream utility (selective
  prediction, re-ranking) — but SCALAR only. "Code Is More Than Text" ensemble AUROC 0.696->0.776.**
- >>> KEY GAP: downstream utility shown at SCALAR (Code-MUE) + LINE-level (FLARE), NONE at
  PER-REQUIREMENT. A per-requirement downstream-utility result (targeted repair / selective gen /
  test-prioritization) is the highest-leverage OPEN "cook harder" addition. <<<

## Emerging bar picture (to confirm from other fetchers)
The paper likely needs: (a) the trained self-expressed per-method AUROC near the 0.93 oracle, (b) a
DOWNSTREAM UTILITY result at per-requirement granularity (the open gap), (c) cross-model (both), (d)
the competitive-vs-functional contrast as a principled scope finding. Reviewer-2 axis: "is per-method
localization USEFUL, or just a number?" → utility result answers it.

## Fetcher 3 (AAAI reviewing bar) RESULTS — HARD BAR DATA
- AAAI-26 acceptance **17.6%** (4167/23680), down from 23.4% (2025). ~29K submissions. AI-review
  pilot scans for "scientific weaknesses" (visible to SPC). Bar is HIGH + rising.
- Reviewer rubric (AAAI-26): baselines-vs-SOTA, benchmark-appropriateness ("are there better
  benchmarks?"), error analysis, FULL replicability (code at review time), limitations. Operative checklist.
- **EAGLE = accepted AAAI-26 calibration paper: multi-dataset × multi-model × multi-baseline + 3
  ablations.** = the accepted-calibration bar.
- **Multicalibration-for-code (scalar, 3-bench/3-model, no training) only WORKSHOP (AI-SQE'26), NOT
  main track.** Proof scalar code-cal at that scope is below bar.
- >>> VERDICT INPUT: DPRC at 2-dataset(TACO+BCB)/1-model is BELOW bar. Needs EAGLE-level scope
  (both models, multi-benchmark, strong baselines, ablations) + a hook (competitive-vs-functional
  insight + per-requirement downstream-UTILITY result [the open gap from fetcher 1]). <<<

## GAP-CLOSURE crystallizing (for §3 to-do)
1. SCOPE: both models (Qwen+DeepSeek); multiple FUNCTIONAL benchmarks (BigCodeBench + MBPP+/HumanEval+
   /ClassEval-style); strong baselines (DCPO scalar, untrained self-report, log-prob, external probe);
   ablations (grouping, loss, continuous-vs-tier, decouple).
2. UTILITY: per-requirement confidence -> a measured downstream win (targeted repair / selective gen /
   test-prioritization). THE open gap; highest leverage.
3. HOOK: competitive-vs-functional as principled scope finding + why per-claim NL methods don't transfer.
4. RIGOR: bootstrap CIs, contamination control, code submitted, limitations.

## Fetcher 2 (AAAI accepted code-LLM) RESULTS — the TEMPLATE
- Incoherence (AAAI'26): oracle-less code-correctness, whole-program (not per-req). Closest comparable.
- **AdaPR bug-localization (AAAI-25 ORAL) + Counterexample-repair (AAAI-25, 1431 progs x 6 LLMs):
  AAAI rewards localization WHEN IT FEEDS A DOWNSTREAM TASK (repair). AUROC-in-isolation is weaker.**
- FLUE (AAAI-25): zero-inference-overhead was the REWARDED criterion. DPRC priming adds cost -> address/justify.
- COREA (EACL'26): verbalized conf + downstream utility (21.5%/16.8% cost reduction, <2% pass@1 drop) = the pattern.
- BigCodeBench = ICLR-25 Oral, 1140 tasks, unsaturated, realistic -> solid foundation for functional claim.
- **WHITE SPACE CONFIRMED: no AAAI paper combines self-expressed + per-requirement + code. Open niche.
  RISK: reviewers ask "why hasn't anyone done this" / demand direct comparison to nearest neighbors.**

## LOCKED (3 independent fetchers converge):
(A) DPRC niche is genuinely OPEN at AAAI (white space).
(B) DOWNSTREAM-UTILITY at per-requirement granularity is THE required + open move — every accepted
    localization paper feeds a task; AUROC alone is below bar; per-req utility is unclaimed.
(C) Scope must reach EAGLE-level (multi-model/multi-benchmark/baselines/ablations); 2-dataset/1-model
    is workshop-tier per the Multicalibration-for-code datapoint.
=> The paper: per-requirement self-expressed confidence on realistic code + a DOWNSTREAM-UTILITY
   result (targeted repair a la AdaPR, OR selective generation a la COREA) + competitive-vs-functional
   scope finding + EAGLE-scope rigor.

## Fetcher 4 (AAAI accepted UQ) RESULTS
- **BayesAgent/vPGM (AAAI-26): verbalized/PRIMED elicitation of structured probabilistic signal ->
  LEGITIMIZES DPRC's digit-priming mechanism (accepted precedent). Pairs calibration + generation-quality gain.**
- CRaFT (AAAI-25): closest MECHANISM analog — graded certainty tied to trainable signal vs moving GT.
- EAGLE (AAAI-26): reads confidence from HIDDEN LAYERS -> reviewers likely demand DPRC ablate
  output-token-readout vs hidden-layer probe. Add that ablation.
- AlignVQA (AAAI-26): new arch + calibration-aware loss, multi-benchmark. Sample-Consistency (AAAI-25): 9 datasets.
- Accepted UQ papers PAIR calibration with a downstream/quality gain -> reinforces utility requirement.
- Track note: code-domain calibration/localization has landed in AAAI APPLICATION DOMAINS track (AdaPR).
  Our primary-topic choice (ML: Bayesian Learning & UQ) is defensible but the code framing could route
  to Applications — the method-vs-application framing matters for desk routing.

## METHOD DEFENSE STRENGTHENED: digit-priming elicitation has an accepted-AAAI precedent (BayesAgent).
## REQUIRED ABLATION SURFACED: output-token readout vs hidden-layer probe (EAGLE comparison).

## Awaiting: calib accept/reject-norms fetcher, generalization+bench fetcher. Box 377/1140. (AAAI accepted UQ, accepted code-LLM, reviewing bar, calibration accept/reject
## norms, generalization+benchmark-standing) + box labeling (377/1140).