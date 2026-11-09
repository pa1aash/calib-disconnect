# Orchestrator notes — code-llm-calibration-aaai27-eabf3f

## Wave 1 dispatched (8 fetchers, ~30 arXiv sources + AAAI scope + Spiess)
Batches: 1=direct code-UQ competitors, 2=selective/abstention/IDE-trust,
3=internal-probe-code-correctness, 4=train-time RL calibration,
5=verbalized elicitation+distillation, 6=semantic-entropy/single-pass UQ,
7=adversarial/protocol/metric caveats, 8=AAAI scope + Spiess + decision-cal.

## The strategic picture forming (pre-evidence, to be tested against sources)

The current paper is DIAGNOSTIC and NEGATIVE: "the internal signal exists but
no interface communicates it." For AAAI main-track (methodological advance,
P1 novelty), the paper must become PRESCRIPTIVE: it must CLOSE the gap it found,
with a method + a headline number.

Three candidate directions the evidence must adjudicate between:

**Direction A — "Distill the sampling oracle into a single forward pass."**
Headline shape: "A cheap probe/head trained to regress the n-sample pass-rate
recovers X% of the AUROC-0.987 oracle at 1/n the cost, and — unlike log-prob
or verbal — stays discriminative (AUROC ~0.9)." 
- Novelty risk: semantic-entropy-probes / Dist2ill / internal-probe-code
  (batch 3, 6) may ALREADY do single-pass approximation of self-consistency.
  If a probe already hits ~0.9 AUROC on code correctness, our novelty collapses
  to "we did it for code" (incremental). MUST check batch 3/6 results.
- Confidence: HIGH if the probe idea is under-explored for CODE specifically.
  Regression-to-passrate is very likely to train well on single GPU.

**Direction B — "Train the model to VERBALIZE calibrated+discriminative
confidence by distilling the sampling signal (not human labels)."**
Headline: "Sampling-distilled verbal confidence achieves AUROC 0.8x — the first
verbal interface that discriminates, closing the disconnect." 
- Our own SFT failed (calibration w/o discrimination) because targets were 3
  coarse tiers. The fix: use the CONTINUOUS n-sample pass-rate as the SFT/DPO
  target, many bins, difficulty-balanced. Rewarding Doubt / Beyond Binary
  Rewards (batch 4) show RL can make verbal confidence calibrated — but were
  they discriminative, and on code? The gap = code + discrimination.
- Novelty risk: uncertainty-distillation (batch 5) distills self-consistency
  into verbal bins already — but for QA/math, and the open question is whether
  it yields DISCRIMINATION not just calibration. Our SFT-collapse result is
  actually the perfect motivation.
- Confidence: MEDIUM. Training verbal to discriminate is exactly where our SFT
  failed; must show the continuous-target fix actually breaks the collapse.

**Direction C — "Selective code generation with a utility headline."**
Turn the calibrated signal into a DECISION: abstain/defer/escalate, and report
a downstream utility win (e.g. risk-coverage curve, or "at 80% coverage,
selective accuracy 0.99"). Task Abstention for Code (batch 2) may already own
this. If so, C is dead as a standalone.

## Leaning (to revisit after evidence)
Direction A or a fused A+B looks strongest on the P1×P2 objective. The single
most defensible AAAI headline: a CHEAP, SINGLE-PASS confidence head, trained by
distilling the sampling oracle, that is the FIRST expressed interface to preserve
the oracle's discrimination on code — validated across models/benchmarks, with a
selective-generation utility corollary. The disconnect paper becomes the
motivation section, not the contribution.

## Dialectical tension to force in loci
- Does a probe/single-pass method ALREADY close the gap (novelty killer)? →
  batch 3 & 6 are decisive.
- Is "distill sampling into verbal/probe" already done for code? → batch 5 & 1.
- Methodological (ML: calibration/UQ) vs application (NLP: code) framing for AAAI
  primary topic — the contribution must be a general calibration METHOD to sit
  in ML and clear main-track novelty.

## Batch 7 (adversarial) RESULTS — decisive for robustness framing
Three independent threats to the 0.987 AUROC headline the NEW paper must pre-empt:
1. **Metric fragility**: ECE_bin is a biased estimator (Roelofs AISTATS'22); equal-width
   binning worst. Protocol sensitivity (Kim&Kang 2026) — the prob-vs-verbal ECE gap can
   flip sign with conditioning. → new paper must use debiased/adaptive metrics + AUROC
   (rank metric, binning-free) as PRIMARY. Good news: our headline should lean on AUROC,
   which is robust to the ECE critique.
2. **Benchmark contamination**: HumanEval/MBPP overlap pretraining (Riddell 2024; TRACER
   2026 catches semantic "shared logic" contamination surface-decontam misses). The near-
   perfect 0.987 could partly be memorization. → STRONG reason to add a contamination-free
   benchmark (LiveCodeBench) as a headline-robustness pillar. This DOUBLES as novelty:
   "does the internal signal survive on truly unseen problems?"
3. **Verbal fails via MULTIPLE mechanisms** (Miao&Ungar 2026: calibration & verbal-conf
   directions are ORTHOGONAL in activation space, CoT contaminates the verbal direction;
   Obadinma NeurIPS'25 adversarial brittleness; Xiong ICLR'24 black-box AUROC 0.52-0.60).
   → our "verbal can't communicate the internal signal" is well-supported; the fix is NOT
   prompting but a trained/probed interface. The orthogonality result is a MECHANISTIC
   explanation we can cite for WHY distillation is needed.

Implication for direction choice: Miao&Ungar's "calibration signal is linearly encoded"
directly supports **Direction A (linear probe / single-pass head recovers the signal)** —
if calibration is a linear direction in activations, a cheap probe should extract it. This
RAISES novelty risk for A (someone may have built the probe) but RAISES confidence it works.

## Batch 6 (semantic entropy / single-pass) RESULTS — novelty window located
- **Semantic Entropy Probes (Kossen/Gal 2024)**: probe on hidden states of a SINGLE
  generation approximates semantic entropy, ~0 sampling overhead. **NO CODE VALIDATION.**
- **Dist2ill (2025→2026)**: single-pass module approximating sampling-derived confidence.
  ECE/NLL not AUROC; **no code validation.**
- **Semantic entropy (Farquhar Nature 2024)**: AUROC 0.79, TriviaQA/SQuAD/etc — **no code datasets.**
- **Sample-scaling (2026)**: n=2 hybrid (self-consistency + verbalized) = +12 AUROC, then
  diminishing. Math/STEM only, no code.

DECISIVE READ: single-pass probing of self-consistency EXISTS in QA/math but is UNVALIDATED
on code functional correctness. That is a clean, defensible novelty window for Direction A:
"a single-forward-pass probe that recovers the near-perfect sampling/pass-rate oracle FOR CODE,
where the correctness label is execution ground-truth (cleaner than QA's fuzzy semantic
equivalence)." Novelty = first code-functional-correctness single-pass probe targeting the
pass-rate oracle + execution labels; Confidence = HIGH (SEP hits 0.79 on QA with a fuzzier
target; our oracle is 0.987 and code correctness is crisply verifiable, so the probe has a
strong, clean learning target). This is the A+robustness fusion I was leaning toward.

Remaining decisive input: batch 3 (internal-probe-code) — if someone ALREADY built a
single-pass probe for code correctness hitting ~0.9, novelty narrows to "vs sampling oracle
+ contamination-free benchmark." Batch 1 (Functional Entropy) — if it's already a single-pass
functional-correctness predictor, that's the closest competitor to distinguish from.

## Batch 2 (selective/abstention/deployment) RESULTS — supporting-utility + motivation
- **In-IDE Calibration at Scale (2025)**: 24M real dev interactions — Platt-scaling post-hoc
  single-pass calibration does NOT align with developer acceptance; 153-dev study PREFERS
  color-coded categorical signals over numbers. Sampling-based calibration NEVER tested.
  → PERFECT motivation: "the deployed single-pass interface provably fails; we build the
  trained single-pass interface that recovers the sampling oracle." Also licenses a
  categorical/risk-tier output (human-preferred) rather than a raw number.
- **Task Abstention for Code / RisCoSet (same group)**: execution-consistency → distribution-
  free abstention, binary only. Risk-control machinery exists for code but NOT connected to
  a calibrated single-pass/expressed signal.
- **AdaDec (+20.9% pass@1), USCD (+16.6%)**: uncertainty-guided decoding wins, but internal-
  only uncalibrated token signal. Shows uncertainty→action pays off in code (AAAI precedent:
  AdapT @ AAAI 2024).
- **Conformal abstention (DeepMind)**: self-consistency→conformal abstention for QA, never code.

Triple gap (batch-2 synthesis): sampling-confidence + formal risk control + IDE-realistic
eval is unoccupied. This is the SUPPORTING-UTILITY arm for Direction A: after the single-pass
probe recovers the oracle, show a risk-coverage curve / selective-accuracy headline
("at 80% coverage, selective pass-rate 0.99") — a concrete downstream win, not just AUROC.

## Consolidating: the paper taking shape (still provisional pending batches 1,3,4,5,8)
CORE (methodological, novel, ML:UQ): a SINGLE-FORWARD-PASS confidence predictor for code
functional correctness, TRAINED to match the near-perfect n-sample pass-rate oracle
(distillation of self-consistency into a probe/head), using EXECUTION labels. First for code.
ROBUSTNESS pillars (answer the adversarial batch-7 threats): (i) AUROC-primary (dodges ECE
critique), (ii) contamination-free benchmark LiveCodeBench (dodges HumanEval memorization),
(iii) cross-model. UTILITY corollary (batch-2): risk-coverage/selective-generation headline.
MOTIVATION: disconnect finding + In-IDE-at-scale negative result. Mechanistic backing:
Miao&Ungar orthogonality (calibration is a linear direction → probe should extract it).
Headline candidate: "A single forward pass recovers 0.9x of the sampling oracle's
discrimination on unseen code — the first expressed interface that preserves it — at 1/n cost."

## Batch 3 (internal probes for code) RESULTS — PIVOTAL, reshapes novelty
KEY: a cheap single-pass hidden-state probe does NOT match the n-sample oracle. Probes
plateau 0.63-0.79 on HumanEval/MBPP-style code; even an ORACLE upper bound ~0.66-0.77 →
a genuine INFORMATIONAL CEILING for single-pass reps on short/simple code. (AutoProbe
2510.02934 [15.9k words, flag source-analyst], Openia 2501.12934, Azaria&Mitchell precedent.)

CONSEQUENCES:
1. Naive Direction A ("single-pass probe recovers the 0.987 oracle") is WOUNDED — the
   ceiling means a probe CANNOT hit ~0.9 on simple code. Confidence in that headline: now LOW.
   The pipeline just avoided a dead paper. Good.
2. This ceiling is itself a RESULT: n independent executions carry information not present in
   one forward pass. Could anchor an analysis paper, but weaker methodological novelty.
3. **Complexity-dependent interface REVERSAL (genuinely novel):** on independent-unit code,
   external LLM-as-Judge verbalized confidence WINS (0.75-0.97) and probes lose; on repo-level
   code, probes win (0.70-0.80) and verbal collapses. Best interface is task/context-length
   conditional — no universal fix.
4. **Contradiction with OUR paper:** we report verbal AUROC ~0.52-0.56 (self-assessment,
   same model rates own solution). Batch 3 reports external LLM-as-Judge verbal 0.75-0.97 on
   simple code. Reconciliation candidate: SELF-verbalized fails; EXTERNAL/fresh-context judge
   succeeds. That distinction is publishable and reframes "verbal fails" → "SELF-verbal fails,
   and here's the interface that doesn't." NOTE this contradiction for step 3 contradiction-graph
   and step 5 depth investigation.

REVISED direction ranking (pending batches 1,4,5,8):
- A (probe recovers oracle): DOWNGRADED (ceiling). Keep only as a bound/analysis, not headline.
- B (train VERBAL to discriminate by distilling continuous pass-rate; fix SFT-collapse; and/or
  external-judge framing): UP. The verbal self-vs-judge contradiction + our SFT-collapse make a
  crisp motivated methodological story. Confidence hinges on batches 4/5 (does trained/distilled
  verbal actually DISCRIMINATE on code?).
- C (risk-controlled selective gen w/ sampling signal + utility headline): steady, safest P2,
  weaker P1.
- NEW D — "complexity/context-conditional confidence routing": route between
  sampling / probe / judge by predicted code complexity; headline = a single ROUTER beats every
  fixed interface across the difficulty spectrum. Novel (the reversal is unexploited), feasible
  (all components single-GPU), but needs the reversal to replicate on our models.

Depth investigation (step 5) must resolve: (i) can trained/distilled VERBAL discriminate on code
(B), (ii) does the complexity reversal replicate (D), (iii) is Functional Entropy (batch 1)
already the single-pass functional-correctness predictor that caps our novelty.

## AAAI topic — CONFIRMED (batch 8, from AAAI-27 areas-and-topics via Wayback)
NO standalone "ML: Calibration" keyword exists. Best fit:
- PRIMARY: **ML: Bayesian Learning & Uncertainty Quantification**
- SECONDARY: NLP: Code Generation / Program Synthesis; ML: Evaluation, Benchmarking,
  Datasets & Analysis (and/or NLP: (Large) Language Models).
Method = primary (UQ), code = application/secondary — matches AAAI's methodology-first rule.

## AAAI-27 FORMAT + DEADLINES — CONFIRMED (batch 8) — FLAG TO USER
7pg main / 9 max (extra = refs + reproducibility checklist). Mandatory reproducibility
checklist at submission. Code/data "after acceptance" NOT accepted as evidence.
DEADLINES: abstracts **2026-07-21**, full papers **2026-07-28**, code 2026-07-31,
conf Feb 16-23 2027 Montreal. Today is 2026-07-18 → paper deadline is ~10 days out.
This is a HARD feasibility fact the user must weigh (their P2 = don't waste time on a
dead paper). Either target AAAI-27 with an experiment plan that fits ~10 days, or aim the
same paper at the next venue (ICLR/ACL/NeurIPS) if AAAI-27 is infeasible. SURFACE THIS.

## Batch 4 (train-time RL calibration) RESULTS — feasibility CONFIRMED for verbal
- **Rewarding Doubt**: RL log-scoring reward on verbalized confidence. **Llama-3-8B, 4-bit
  LoRA, SINGLE A40.** TriviaQA AUROC 0.859 — explicitly MORE discriminative than a trained
  probe. **No code.** ← strongest existing proof verbal CAN discriminate + single-GPU feasible.
- **RLCM (JHU, COLM'26)**: only train-time paper with a CODE result (LiveCodeBench), but reads
  confidence via HIDDEN-STATE PROBE, not expressed; ablation: verbalized/logit "insufficient"
  vs probe. 4xH100 (not single-GPU).
- **CSR (UCSD)**: abandons verbalized (unstable across paraphrases). Single A100 LoRA. No code.
  → the adversarial "don't pursue verbal" position the paper must REBUT.
- **DCPO (ICML'26)**: PROVES gradient conflict between accuracy & calibration in one reward →
  design caveat (decouple; calibrate-only or advantage reshaping).
- **CAPO (ACL'26)**: discrimination-first (AUC) surrogate loss beats calibration-error-first;
  small model, single-GPU. No code. ← the loss design to adopt.

## Batch 1 (direct competitors) RESULTS — "better internal signal for code" is CROWDED
- Functional Entropy (0.87 via LLM-judge functional clustering; excludes open-weight = our gap),
  FASE (0.74-0.91, Qwen/DeepSeek-Coder-7B/HumanEval), ConSelf (0.804, our exact models +
  LiveCodeBench), Sharma&David (only symbolic-execution clustering restores signal; log-prob
  NOT significant), Multicalibration-for-code (never reports AUROC — conflation gap).
  → "sampling/execution confidence works for code" is now 2026 CONSENSUS. NOT novel by itself.
  The EXPRESSED/communicated interface for code remains UNOCCUPIED.

## CONSOLIDATED STRATEGIC READ (post full corpus) — for loci/depth to adjudicate
Crowded (avoid as headline): better internal/behavioral signal for code; "sampling works."
Dead: single-pass probe recovers the 0.987 oracle (AutoProbe informational ceiling ~0.77).
OPEN & valuable:
  (B) EXECUTION-GROUNDED train-time calibration of EXPRESSED confidence for CODE — first to
      make a code LLM's stated confidence discriminative, using pass-rate/execution as the
      reward (distilling the sampling oracle into the expressed channel). Rebuts CSR. Feasible
      (Rewarding-Doubt = single-GPU LoRA, AUROC 0.859 on QA gives a strong prior). Adopt CAPO
      discrimination-first loss; avoid DCPO gradient conflict. HIGH P1×P2. LEADING CANDIDATE.
  (D) Complexity-conditional interface reversal/routing (AutoProbe reversal) — novel but needs
      replication; secondary.
Contradiction to exploit (step 3): OUR paper "verbal AUROC 0.52 (self-assessment)" vs batch-3
external-LLM-judge verbal 0.75-0.97 on simple code + Functional Entropy verbal 0.52-0.80. The
self-vs-external and untrained-vs-trained distinction is the crux the paper resolves.
Code-unique novelty lever (Spiess open gap): execution gives PER-TEST-CASE labels → structured/
localized confidence (which clause is likely wrong), impossible in QA. Highest novelty, lower
headline-confidence; hold as an extension, not the headline.

## Step 4 dispatched — loci-analyst A (novelty angle) + B (feasibility/risk angle)
Waiting. Leading direction to be scored: (B) execution-grounded train-time calibration of
expressed confidence for code. Novelty-killers to test: RLCM (code+probe), Rewarding Doubt
(verbal RL, QA), Functional Entropy (better internal signal). Dialectical locus required.

## Loci A returned (5 loci): collapse-proof-training-objective (dial), self-report-vs-
## external-judge-vs-probe-reversal (dial, AutoProbe verified: self fails, judge 0.94 on
## simple, probe 0.82 near-oracle on repo), repo-level-feasibility, multicalib-competitor-check,
## fallback-utility. Rejected better-internal-signal (crowded), ECE-artifact (resolved),
## human-study (scope). Waiting on B.

## TIMELINE REALITY (to raise with user in next report)
AAAI-27 full-paper deadline 2026-07-28 (abstract 07-21). ~10 days from today. A from-scratch
train-a-model-and-run-experiments paper is very tight for AAAI-27. Options: (i) if the leading
direction reuses the EXISTING harness/models (it does — same Qwen/DeepSeek-Coder-7B, HumanEval+
LiveCodeBench, LoRA), a focused 10-day sprint is conceivable but risky; (ii) target the same
paper at the next major venue (ICLR'27/ACL/NeurIPS) with more runway. The research direction is
venue-agnostic; only the deadline pressure differs. Will present both.

## Step 5 dispatched — 5 depth investigators (novelty-occupied, collapse-proof-objective,
## interface-reversal, label/data-feasibility, fallback). Waiting for all 5.
## The two decisive verdicts: (1) is the direction OPEN (novelty locus), (2) what recipe
## breaks the collapse with a confident AUROC (collapse-proof locus). These determine the
## headline and whether the paper is a safe bet. Reconcile in step 6.

## Depth interim 1/5 — interface-reversal COMMITTED:
Premise "self-report fails everywhere" FALSE — fails only untrained/free-text; trained proper-
scoring self-report succeeds (ConfTuner/Rewarding Doubt ~0.86 QA, never code). Method core =
SAME-MODEL DECOUPLED self-report: frozen generation + 2nd-turn LoRA confidence head, proper-
scoring-rule loss vs execution-pass-rate labels. Keeps "expressed interface" novelty, avoids
"X but for code". AutoProbe complexity-router = secondary/future, not headline (asymmetric:
23-34pt judge win simple vs 0-11pt probe win repo). Confidence 65-75%. Converges with collapse-
proof locus. Architecture crystallizing: decoupled LoRA head + proper-scoring + pass-rate labels.

## Depth interim 2/5 — label/data-feasibility COMMITTED: YES achievable.
Recipe: ConfTuner tokenized-Brier proper-scoring loss RETARGETED on existing n=10 execution
pass-rate (continuous, not binary/tiers → fixes collapse), ≥2000 real problems MBPP+APPS+
LiveCodeBench, eval HumanEval+LiveCodeBench. ~15-25 GPU-hrs (45-75 w/ buffer), fits 10 days
single A100/GH200. Rule out ORCE 2-model DPO (4xH100) + UD N=100. Confidence med-high. Flag:
exact hybrid untested on code → Day-1 pilot recommended. CONVERGES with interface-reversal
(same recipe). Method now concrete + feasible. Awaiting novelty + collapse-proof + fallback.

## Depth interim 3/5 — novelty-occupied COMMITTED: OPEN (narrowly scoped). DECISIVE.
No 2026 paper combines (a) EXPRESSED/decoded (non-probe) confidence + (b) trained NATIVELY on
code + (c) AUROC on a code benchmark. RLCM (closest) = OOD-transfer + hidden-state PROBE + NEVER
reports AUROC (grep-verified full text). Rewarding Doubt/ConfTuner = expressed token AUROC
0.74-0.86 but QA-only. Multicalib/Fine-grained-ACR/When-to-Defer skip code discrimination.
HEADLINE FRAMING: "does discrimination survive the DECODE step?" — first expressed, code-native,
AUROC-measured calibrated confidence. Confidence 60-70% (high on occupancy, lower the pivot beats
collapse). Flags: UT-Dallas "When to Answer/When to Defer" 12-mo roadmap = competitive-timing
risk; the collapse-proof locus (DCPO/CAPO) is the main threat to landing. Awaiting collapse-proof
+ fallback — collapse-proof is now the linchpin verdict.

## Depth interim 4/5 — fallback COMMITTED: real, publishable-grade insurance (not headline).
Fallback = wrap UNCOLLAPSED internal sampling signal in CIC Clopper-Pearson risk-controlled
selective generation; target 70-90% coverage @ ≤2-5% err, pre-reg alpha=0.10 (0.05 stretch);
calibration-pool expansion HumanEval→+MBPP as fallback². Not "extremely novel" alone (CIC +
CODEREFUSER + Sharma&David occupy abstention). Ceilings: CODEREFUSER 26.5pt precision / ~3.5x
coverage; Sharma&David 77.8-88% coverage @ ≤0.02% FPR LiveCodeBench. Failure mode to pre-reg:
CIC infeasible @ alpha=0.05 on weak models. → paper LEADS with verbal-discrimination result,
reports this as guaranteed secondary. Only collapse-proof-objective (linchpin) remains.

## Depth interim 5/5 — collapse-proof COMMITTED + CORPUS CORRECTION (pivotal tension).
Recipe: DCPO masked-gradient DECOUPLED objective (separate token-block advantages for
reasoning vs verbalized-confidence, bounded Brier reward vs continuous instance+group pass-rate).
Formal gradient-conflict proof (Prop 4.2) names our SFT-collapse mechanism. Recommend LoRA-adapt
+ replace coarse 3-tier targets with continuous n=10 pass-rate.
**CORRECTION (load-bearing):** DCPO is NOT theory-only — full text shows it EVALUATES on
LiveCodeBench v5/v6 + HumanEval+ with AUROC 0.796-0.914 (Qwen3-8B), beating joint RLCR.

### >>> #1 ISSUE FOR STEP 6 RECONCILE: DCPO vs the novelty claim <<<
Novelty investigator said "no paper = expressed + code-native + AUROC." Collapse-proof
investigator found DCPO reports AUROC on code with a DECODED confidence signal → the cell is at
least PARTIALLY OCCUPIED. Reconciliation must find the DEFENSIBLE residual novelty. Candidates:
  (i) EXECUTION-GROUNDED reward: DCPO/RLCM use binary correctness in a general RLVR REASONING
      setup; none use graded n-sample EXECUTION pass-rate as the continuous training target for a
      code-gen (non-reasoning) instruct model. Code's per-test verifiability = denser reward. REAL.
  (ii) DCPO = general reasoning-model method, code is one eval domain (like RLCM's OOD). A
      CODE-NATIVE, single-GPU-LoRA, execution-reward method is distinct but risks "DCPO-lite for code."
  (iii) PIVOT the HEADLINE to what DCPO/RLCM/Rewarding-Doubt structurally CANNOT do: exploit code's
      PER-TEST-CASE verifiability for STRUCTURED/LOCALIZED confidence ("which clause/test is likely
      to fail"), Spiess's explicit open gap, impossible in QA/math. Highest P1 novelty; use the
      now-proven DCPO/execution machinery as the METHOD so P2 stays high.
Given user's P1=NOVELTY (top), lean (iii)-as-headline + (i)-as-mechanism, with scalar-confidence
as a supporting result — but this is exactly reconciliation's call. Verify in step 6 whether DCPO
actually calibrates confidence in generated CODE's functional correctness vs a reasoning answer
scored on coding problems (matters for how much it occupies our cell).

## ALL 5 DEPTH INTERIMS DONE. Step 6 comparisons.md written (DCPO pivot). Step 7 source-
## tensions written. Step 8 corpus-critic dispatched: adversarial scoop-check on the per-test
## STRUCTURED-confidence headline. If OCCUPIED → pivot dies, need new headline. If OPEN → lock it.
## Contingency if occupied: (a) complexity-conditional routing (Direction D), (b) single-GPU-LoRA
## execution-reward code-native scalar positioned hard vs DCPO's 8xA100 reasoning-model setup,
## (c) the selective-generation-utility floor becomes a bigger part of the story.

## Step 10 dispatched — 3 drafts (A bold-thesis, B risk-first steelman, C runnable-plan). Waiting.

## SYNTHESIS PLAN (for step 11) — the final report the user needs
The user wants ONE paper idea + confident headline, extremely novel, P2 feasible. The report must
be a decisive RECOMMENDATION, not a survey. Structure (per required_section_headings):
1. Frontier (brief) — sampling-works-for-code is consensus; expressed interface is the open frontier.
2. Holes — expressed/communicated confidence unoccupied for code; DCPO occupies scalar; metric+
   contamination caveats; per-test structured cell empty.
3. Where current paper falls short — diagnostic/negative, single benchmark, SFT-collapse; needs a
   prescriptive methodological turn for main-track.
4. Candidate directions scored (novelty×confidence): A=per-test structured self-expressed (LEAD),
   B=scalar single-GPU (occupied by DCPO→demote to baseline), C=complexity routing (secondary),
   D=selective-generation utility (safe floor). Table with the two-axis scores.
5. THE ONE PAPER — committed: "SelfEval/per-test structured execution-grounded confidence." Method:
   decoupled masked-gradient LoRA + bounded Brier vs continuous per-test pass-rate; single-GPU.
6. Headline + exact experiment: "First code LLM that self-expresses calibrated per-test confidence
   localizing which requirement fails — per-test AUROC ~0.80 (target), no incumbent." + scalar
   replication vs DCPO + risk-coverage utility.
7. Why it lands: DCPO 0.79-0.91 scalar code proof; Rewarding Doubt 0.859 single-GPU; CURE per-claim
   0.667 w/ NOISY oracle (ours cleaner); labels free; Prop-4.2 + continuous targets fix collapse.
8. Failure mode + PRE-REGISTERED fallback: if per-test AUROC < ~0.70, report risk-coverage utility
   (Sharma&David ceiling 77.8-88% @ ≤0.02% FPR) + scalar result — still a complete paper.
9. Novelty defense: the 4-axis wedge; distinguish DCPO/FLARE/CURE/Atomic/Gros&Devanbu/VeRPO;
   HONEST scoop caveat (UT Dallas under-review).
10. AAAI-27 topic: primary ML: Bayesian Learning & UQ; secondary NLP: Code Gen / ML: Eval.
11. Shortlist 5-10 load-bearing papers with per-paper contribution/hole.
PLUS a prominent, honest TIMELINE box: AAAI-27 paper deadline 2026-07-28 (~10 days) → either a
scoped sprint reusing the existing harness, or next venue. This is decision-critical for the user.
Argumentative beats to preserve from comparisons.md: DCPO-occupancy resolution; decouple-vs-joint;
self-report-vs-probe; ECE-vs-AUROC; contamination→LiveCodeBench.

## Draft C DONE (5926w): per-test AUROC 0.75-0.85 headline; de-scope LADDER w/ numeric gates
(L1 per-test-case, gate Day-3 pilot AUROC>0.65 → L2 per-category → L3 selective-gen floor 70-90%
cov @ ≤2-5% err); Day-6 bootstrap-stability check = AAAI-vs-next-venue pivot. Synthesizer must
carry this de-scope ladder + calendar verbatim — it's the anti-dead-paper spine. Benchmark density
numbers low-confidence (hedge). Awaiting A + B.

## Draft A DONE (5631w): headline per-requirement AUROC 0.78-0.86; 4-axis novelty defense; key
"will-it-land" argument = 3 separately-proven ingredients (CURE 0.667 on NOISIER oracle → exec
oracle should exceed; DCPO scalar code proof; free labels). Scoop risk surfaced §9E. Awaiting B.

## Step 11 synthesizer dispatched. What the step-12 critics must scrutinize:
- DIALECTIC critic: does the report honestly engage the DCPO-occupancy + UT-Dallas scoop threats,
  or straw-man them? Does it over-claim the per-test AUROC will land (P2)?
- DEPTH critic: is the training recipe (decoupled masked-gradient LoRA + bounded Brier + continuous
  per-test targets) technically specified enough, or hand-wavy? Is the "free labels" claim precise?
- WIDTH critic: any corpus-supported angle missing? (e.g., per-test label noise from flaky tests;
  the DCPO-LoRA-untested risk; benchmark test-density low-confidence numbers.)
- INSTRUCTION critic: all 11 required headings + exec summary present? shortlist has 5-10 papers?
  AAAI topic pinned? failure-mode+fallback present? 7-page-fit acknowledged? novelty defended?
Watch for: report must stay a PROPOSAL (not drift into writing the paper); must foreground novelty
(P1) while keeping the three-tier confidence spine (P2); timeline honesty preserved.

## Critic 1/4 DEPTH: 9 findings (5 major), all patcher-actionable. Highest value: add DCPO reward
## formula R_c=-|conf-R_IG| + Theorem 5.1 (the cure); add Functional Entropy code-native constrained
## self-report 0.82-0.87 (P2 de-risker); fix emission-architecture contradiction (frozen-gen + 2nd
## confidence-only LoRA turn). Also: Yaldiz block-vs-token-decoupling caveat, CIC α=0.05 infeasibility
## gate. No structural skip. Awaiting dialectic, width, instruction.

## Critic 2/4 INSTRUCTION: PASS. All 11 headings in order verbatim; 12-pt checklist satisfied;
## one committed idea "DPRC"; 10-paper shortlist; AAAI primary pinned verbatim (confirmed vs note).
## Only major: UQ4CT omitted from novelty defense (NOT in vault; tangential MoE-router UQ → patcher
## adds 1-line axis-distinction, NO gap-fetch needed). Minors: en-dash→hyphen §11 heading. Awaiting
## dialectic + width.

## Critic 3/4 WIDTH: 7 findings (0 critical, 4 major). Adds: Miao&Ungar orthogonality (why verbal
## fails); single-pass SEP/Dist2ill to distinguish; human-trust (Copilot-ZoomInfo, Critical-or-
## Compliant); AutoProbe 0.77 ceiling to bracket headline. Minor bloat: timeline repeated 4x. All
## patcher-actionable, no gap-fetch needed (all in vault). Awaiting dialectic (last).

## Critic 4/4 DIALECTIC: 9 findings (1 CRITICAL, 7 major) — the sharpest, all honest & fixable.
- CRITICAL: "guaranteed floor" leans on internal 0.987 signal, but semantic-collapse note shows it
  silently fails on 18-32% of LiveCodeBench items → floor not as guaranteed as claimed. FIX: caveat.
- MAJOR: headline band 0.75-0.85 over-claimed — CURE only 0.667 (below floor); §8B's own top-risk
  0.65-0.72 lies BELOW the band. FIX: widen honest range / soften ("target, pilot-set; plausible
  0.65-0.85") and reconcile with §8B.
- MAJOR: method could read as "DCPO scalar→vector one-line delta" → strengthen method-novelty framing.
- MAJOR: UT-Dallas "Beyond Execution" under-review under-weighted (contemporaneous policy ≠ protection).
- MAJOR: numeric per-req interface vs in-IDE "developers prefer categorical" — confront, don't only
  cite for floor. (Easy fix: frame per-req confidence as drivable to categorical UI.)
- MAJOR: flaky/correlated tests = label-VALIDITY threat (not just discrimination). FIX: add.
- MAJOR: self-report chosen for novelty when probe is safer high-AUROC route → acknowledge tradeoff.
- STRUCTURAL (orchestrator-level): "cannot come out dead" equivocates complete vs AAAI-acceptable;
  L3 floor is novelty-2.5/"occupied" so demotion-to-L3 IS a weak paper. REAL insurance = the scalar
  tier + the ICLR-27 pivot, NOT L3. → ORCHESTRATOR FRAMING DECISION for patcher (below).

## >>> ORCHESTRATOR FRAMING DECISION (encode into patch guidance) <<<
Honest reframe: the paper is engineered so it always yields a COMPLETE submission, and the genuine
insurance against a *weak/dead* paper is two-fold: (1) the DCPO-backed SCALAR tier (high-confidence,
defensible-if-incremental result), and (2) the ICLR-27 venue pivot (6 extra weeks converts the
per-test gamble into a safe bet). L3 selective-gen floor guarantees COMPLETENESS, not main-track
novelty — say so plainly. Do NOT let "cannot come out dead" stand unqualified. This preserves the
user's P2 honestly without overselling.

## Long sources worth deeper read in depth phase (step 5 investigators to read fully)
AutoProbe (15.9k), Spiess (14.5k), Sharma&David (15.9k), Detommaso multicalib (19.9k),
RLCR/Beyond-Binary (20.5k).
