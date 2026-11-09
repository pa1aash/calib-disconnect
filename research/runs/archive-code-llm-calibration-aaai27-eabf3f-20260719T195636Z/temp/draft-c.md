# Structured, Execution-Grounded Confidence for Code LLMs: The Executable Plan

## Executive Summary

The paper to write is this: **train a 7B code language model to emit calibrated, discriminative confidence at per-test-case (per-requirement) granularity — a self-reported vector that localizes *which parts* of a generated solution will fail — and show that this structured signal discriminates correct-from-incorrect at the requirement level (per-test AUROC), a capability the single-scalar confidence methods that define the 2026 frontier structurally cannot produce.** The headline number is a *per-test-case discrimination AUROC in the 0.75–0.85 band on contamination-controlled benchmarks* — a number for which no incumbent exists, because every prior train-time confidence method emits one scalar per answer and is evaluated only on QA/math, or (in the one code case, DCPO) emits one scalar per code solution [1].

This is not the naive "train a code LLM to verbalize a calibrated confidence number" paper. That paper is already largely written: DCPO (Decoupled Confidence Policy Optimization, ICML 2026) trains a decoded `<conf>` block against an execution-pass-rate target and reports scalar AUROC 0.796–0.914 on LiveCodeBench v5/v6 and HumanEval+ [1]. Pursuing the scalar headline would be "DCPO-lite on LoRA," exactly the incremental trap to avoid. The novelty lives one level deeper: code execution produces a *vector* of per-test outcomes where QA and math produce a single correctness bit, so the fine-grained ground-truth labels the structured target needs are **free** — they are already computed by the n-sample runs the current manuscript uses to obtain its AUROC-0.987 internal signal.

The method is a **decoupled, masked-gradient LoRA head trained with a bounded proper scoring rule (Brier) against continuous per-test pass-rate targets** — DCPO's collapse-proof recipe [1], LoRA-adapted to single-GPU following the rank-16 precedent of Yaldiz et al. [6], warm-started with the ConfTuner tokenized-Brier objective [3]. The total compute is **~15–75 GPU-hours** on a single A100-40GB or GH200, comfortably inside a 10-day window [3][6][11].

The paper is de-risked on two fronts. First, the **failure mode is named and the fallback is pre-registered**: if the trained structured signal underperforms, wrap the *untouched* internal sampling signal (never the trained output) in a Clopper-Pearson risk-controlled selective-generation policy targeting 70–90% coverage at ≤2–5% error [9][10] — a guaranteed-to-land secondary result. Second, the **decision points are pre-registered** as a de-scoping ladder from the bold per-test headline down to a per-category headline down to the selective-generation floor, each gated by a concrete number from a Day-1 timing pilot and a Day-3 collapse-check pilot.

The AAAI-27 primary keyword is **"ML: Bayesian Learning & Uncertainty Quantification"** (calibration has no separate keyword; it falls here) [20], with secondaries "NLP: Code Generation / Program Synthesis" and "ML: Evaluation, Benchmarking, Datasets & Analysis" [20]. The contribution is methodological (a new training objective and confidence *granularity*), which keeps it in the main track rather than being redirected to an application track [20][22].

What follows is the executable spine: exact experiments, exact GPU-hour accounting, exact pre-registered decision thresholds, and the AAAI-27-vs-next-venue contingency. This draft's job is to make the plan *runnable* without wasting money on a dead paper.

---

## 1. The Research Frontier in Code-LLM Confidence and Calibration

The 2026 frontier splits cleanly into two questions that the literature has mostly answered and one it has not.

**Question one — can a signal internal to the model discriminate correct code?** Answered, decisively yes. Repeated-sampling / execution-pass-rate confidence discriminates correct from incorrect code generations at AUROC ~0.80–0.99 across every study that measures it: the current manuscript reports 0.987 on HumanEval, ConSelf reports 0.804 on LiveCodeBench [11], and symbolic-execution-clustering variants of Sharma & David reach coverage 77.8–88% at a false-positive-rate below 0.02% on LiveCodeBench [8]. The consensus is strong enough to state without hedging: **the internal signal is not the research problem.** Any paper whose headline is "sampling confidence discriminates code correctness" is dead on arrival.

**Question two — does a *train-time* intervention exist that makes a model's *expressed* confidence discriminative?** For QA and math, yes, and the mechanisms are well-characterized. ConfTuner trains a "tokenized Brier score" — a proper scoring rule applied directly to the confidence token's next-token distribution — requiring zero extra sampling and converging at ~2,000 examples on 7–8B models, with +14.4% relative AUROC over prior verbalized-confidence baselines [3]. Rewarding Doubt trains a log-scoring-rule RL reward integrated into generation on a single A40 with 4-bit LoRA, reaching TriviaQA AUROC 0.859 — and, critically, *beats a lower-ECE trained-probe baseline on discrimination*, demonstrating that a well-designed joint objective need not collapse [2]. RLCR (Beyond Binary Rewards) proves any bounded proper scoring rule has a population optimum that is simultaneously accurate and calibrated, while showing that an *unbounded* log-score reward hacks into abstention-collapse under low signal — establishing boundedness as a non-negotiable design constraint [5]. CAPO proves GRPO's implicit advantage estimator is an AUC-*inconsistent* surrogate and supplies an AUC-consistent logistic replacement [4].

**The DCPO correction.** The single most important fact for scoping this paper is that DCPO (ICML 2026) already carried this machinery into code. It splits the response into a reasoning block and a verbalized `<conf>` block, computes *separate* group-relative advantages for each, and applies a masked gradient so each advantage touches only its own tokens — mechanically preventing the accuracy-vs-calibration gradient conflict its Proposition 4.2 proves is generic to overconfident models [1]. DCPO's Table 2, on Qwen3-8B, reports scalar confidence AUROC of 0.796 (LiveCodeBench v5), 0.845 (v6), and 0.914 (HumanEval+), beating joint-reward RLCR on both AUROC and accuracy [1]. **The scalar-expressed-confidence-for-code cell is occupied.** This is the load-bearing correction that reshapes the entire proposal: the frontier is not "nobody has trained expressed code confidence," it is "everybody who has, emits one number per solution."

The frontier's shape, then: internal discrimination is solved; scalar expressed discrimination is solved for QA/math and freshly solved for code by DCPO; and the *structure* of the expressed signal — its granularity — has been left entirely unexplored. That is where a novel paper must live.

## 2. Caveats, Holes, and Open Problems at the Frontier

Five holes are load-bearing, and I rank them by how much a new paper can exploit each.

**Hole 1 — the granularity hole (the exploitable one).** Every train-time confidence method in the corpus emits a single scalar per answer: DCPO's `<conf>` block [1], Rewarding Doubt's confidence token [2], ConfTuner's tokenized Brier over one confidence value [3], ORCE's separate confidence LLM producing one score [7]. This is *forced* by the QA/math substrate, where correctness is a single bit. Code is different: a generated function is executed against a suite of tests, producing a *vector* of pass/fail outcomes. A scalar confidence throws that structure away. No prior work trains a model to express confidence *per test / per requirement*, and — decisively — the fine-grained labels needed to supervise it are already a byproduct of the n-sample pass-rate computation the current manuscript performs. This is the paper.

**Hole 2 — the ECE-only evaluation hole.** A large fraction of the code-calibration literature reports only ECE (Expected Calibration Error — the average gap between confidence and accuracy within confidence bins) and never reports discrimination. Multicalibration-for-code reports Brier Skill Score and ECE, never AUROC; Yaldiz et al. report ECE and distribution-spread but no AUROC [6]. This is not a cosmetic gap. A near-constant predictor — one that outputs 0.9 on everything — trivially satisfies ECE while carrying zero discriminative power. CAPO states this almost verbatim: "assigning identical confidence to both correct and incorrect responses perfectly satisfies calibration yet fails to distinguish them" [4]. The current manuscript's own SFT run *is* this pathology (mean 0.900 on easy and hard alike). A paper that makes discrimination (AUROC) primary and treats ECE — computed with a debiased estimator [17] — as secondary occupies the methodologically correct position and simultaneously critiques the ECE-only prior work.

**Hole 3 — the contamination hole.** The current manuscript's 0.987 oracle is on HumanEval, and Riddell et al. show HumanEval/MBPP carry both surface-level and semantic contamination, with models scoring measurably higher on contaminated subsets [16]. A single-benchmark near-perfect number is a reviewer magnet for the "memorization not generalization" objection. The fix converts the threat into a robustness pillar: evaluate primarily on LiveCodeBench, whose problems are time-windowed to post-training-cutoff dates [15], and treat HumanEval as a legacy comparison only. ConSelf already replicates the difficulty-level disconnect on LiveCodeBench with the same model families, which is direct evidence the finding survives decontamination [11].

**Hole 4 — the semantic-equivalence hole.** Generic semantic-similarity proxies (NLI, embeddings, CodeBLEU, AST clustering) collapse on code: the current manuscript's AST proxy reaches only AUROC 0.689, and Sharma & David find that only *symbolic-execution* clustering restores signal, log-probabilities being statistically insignificant [8]. This reinforces, rather than threatens, the plan: per-test execution outcomes are the only reliable label source for code confidence, and they are exactly what the structured target uses.

**Hole 5 — the deployment-relevance hole.** Large-scale IDE studies show post-hoc Platt scaling of a single-pass token confidence does not align with developer acceptance, and developers prefer categorical/color-coded reliability cues over numeric scores. A structured signal that says "this function is likely correct on the main path but I'm unsure about the empty-input case" is closer to what practitioners can act on than any single number — an argument the paper should make explicitly but not stake its technical claim on.

## 3. Where the Current Calibration-Disconnect Paper Falls Short of Main-Track

The current manuscript is an excellent diagnosis and a weak prescription. Three shortfalls block main-track acceptance, and all three are fixable by the proposed extension.

**It is diagnostic, not methodological.** Its finding — internal AUROC 0.987, no expressed interface communicates it — is a measurement result. AAAI main-track review explicitly rewards papers that "introduce new problems... or introduce methods of interest beyond a single sub-area" over measurement studies within a narrow area [22]. A pure diagnosis risks redirection to an application venue. The extension supplies a *method* (a new training objective at a new granularity), which is the fix.

**Its one intervention failed in the instructive way.** The 274-example LoRA-r16 SFT cut verbal ECE 64% but produced mean confidence 0.900 on both easy and hard problems — "calibration without discrimination." Read against DCPO's Proposition 4.2 and CAPO's AUC-inconsistency proof, this is not a tuning failure; it is the *predicted* outcome of a single joint objective over coarse tiers with too little data [1][4]. The manuscript reports the collapse but does not repair it. The extension repairs it (decoupled objective + continuous instance-level targets + proper scoring rule) and, in doing so, turns the collapse from an embarrassment into the motivating evidence for the method.

**Its evidence base is too thin for a confident headline.** One benchmark (HumanEval, 164 problems, skewed easy), two models, 274 SFT examples, no contamination control, no discrimination metric on the trained output. Each is individually survivable; together they cap the paper below main-track. The extension broadens to LiveCodeBench + TACO/CodeContests + HumanEval-legacy, ≥2,000 training problems, contamination-controlled primary eval, and AUROC-primary reporting.

The committed reading: **the current paper is a strong Section 2 of the paper it should become.** Its disconnect finding becomes the motivation; the structured-confidence method becomes the contribution.

## 4. Candidate Directions, Scored on Novelty and Confidence

Four directions were on the table. I score each on novelty (the binding Priority 1) and confidence-of-landing (Priority 2), on a 1–5 scale, and commit to one.

| Direction | Novelty | Confidence | Verdict |
|---|---|---|---|
| **A. Scalar expressed code confidence (DCPO-lite on LoRA)** | 2 | 5 | Reject as headline — occupied by DCPO [1] |
| **B. Per-test-case / structured expressed confidence** | 5 | 3.5 | **Commit** — empty cell, free labels, comparable cost |
| **C. Selective generation / abstention wrapper on internal signal** | 2.5 | 5 | Demote to fallback — occupied by CIC [9], CODEREFUSER [10], Sharma & David [8] |
| **D. Complexity-routed estimator (self-report vs judge vs probe)** | 3.5 | 2.5 | Reject — requires repo-level benchmark build; out of single-GPU budget |

**Why B over A.** A is a safe bet (DCPO already got 0.80–0.91 scalar AUROC on code [1]) but fails Priority 1: it is the incrementalism trap. B is the only direction that is simultaneously novel (the four-axis conjunction below is empty), feasible (labels free, cost comparable to A), and a genuine methodological advance (a new confidence *granularity* plus the training objective to reach it).

**Why not C as headline.** The abstention literature is dense: CIC gives a general Clopper-Pearson risk-controlled wrapper [9], CODEREFUSER a code-specific zero-oracle-at-inference variant delivering ~3.5× more answered tasks than a perplexity baseline at matched risk [10], and Sharma & David a symbolic-execution ceiling [8]. Wrapping the internal signal is valuable but not "extremely novel." It is the perfect *floor*, not the headline.

**Why not D.** AutoProbe's three-way reversal (external judge wins on simple code ~0.94, internal probe wins on repo-level ~0.82) is real but asymmetric, concerns post-hoc third-party assessment rather than the coder's own expressed confidence, and requires building a repo-level benchmark — a larger lift than the single-GPU/10-day budget supports. It survives as a one-paragraph robustness ablation, not a pillar.

The commit is **B: structured, execution-grounded, self-expressed confidence**, with A as a positioned baseline and C as the pre-registered fallback.

## 5. The One Paper: Committed Recommendation

**Title (working):** *"Where Will It Break? Training Code LLMs to Express Calibrated Per-Requirement Confidence."*

**One-sentence contribution:** A training method that makes a 7B code LLM express calibrated, discriminative confidence at per-test-case granularity — localizing which requirements of a generated solution will fail — a structured capability enabled by code's per-test verifiability and unreachable by the scalar-confidence methods (DCPO, RLCR, Rewarding Doubt) that define the current frontier [1][2][5].

**The four-axis novelty conjunction** (verified empty against the closest prior work): the signal is (1) **self-expressed** by the coder itself, not read from an external probe or judge; (2) **per-test-case / per-requirement**, not scalar and not per-line-spatial; (3) trained against the code's **own deterministic execution oracle**, not a noisy fact-checker or an edit dataset; (4) on **code**, not QA/math. No prior work occupies all four (Section 9).

**The method, precisely.** Take Qwen2.5-Coder-7B-Instruct. For each problem it generates a solution followed by a **structured confidence block** — a small sequence of confidence tokens, one per test-case slot (or per test *category*; see the de-scope ladder). Train that block with a **decoupled, masked-gradient objective**: the reasoning/solution tokens receive advantage only from a binary correctness signal, while the confidence tokens receive advantage only from a **bounded Brier reward against continuous per-test pass-rate targets**, exactly mirroring DCPO's masked-gradient split but at vector rather than scalar granularity [1]. Warm-start the confidence block with a ConfTuner-style tokenized-Brier SFT pass against the same per-test pass-rate labels [3], then optionally run a short on-policy refinement stage. Everything is LoRA rank-16, single-GPU, following the exact feasibility precedent of Yaldiz et al. (LoRA r16, alpha 32, decoupled at the token level, ~500 GPU-hours across *three* model sizes → ~150/model) [6].

**Why this specific recipe and not another.** Two independent lines of the analysis converge on it. The collapse-proof line: DCPO's Proposition 4.2 proves a single joint objective has strictly negative gradient inner product once a model drifts overconfident (the generic code-LLM regime), and the manuscript's own mean-0.900 collapse is that proposition realized [1]; decoupling the confidence gradient into its own masked token-block removes the conflict, and continuous instance-level targets remove the coarse-bin collapse (DCPO's ablation shows removing instance-level labels alone degrades ECE 0.128→0.209 [1]). The self-report line: "self-report fails" is true only *untrained* — Functional Entropy's free-text verbal confidence is 0.54–0.80, but its constrained P(True) variant is 0.82–0.87, same model, same self-reference; the failure is the elicitation format, not the act of self-assessment. Trained with a proper scoring rule, same-model self-report discriminates (ConfTuner, Rewarding Doubt, both ~0.86 on QA) [2][3]. The recipe imports the *architecture* of the winning code method (DCPO's decoupling) and the *feasibility budget* of a LoRA method (Yaldiz, Rewarding Doubt) [1][2][6].

**Boundary condition — when the bold headline wins vs the fallback.** The structured headline wins if and only if two conditions hold, both checkable by Day 3: (i) the per-test target is *learnable* — a pilot LoRA run on ~300 problems yields a per-test AUROC materially above 0.65 rather than collapsing to a constant; and (ii) the per-test labels have *spread* — problems whose tests are all-pass or all-fail carry no per-test signal, so the training pool must contain enough partially-passing solutions. If (i) fails, de-scope to per-category confidence (coarser slots, easier target). If per-category also fails, the safe fallback (Section 8) becomes the headline. This boundary is pre-registered as a decision gate, not discovered post hoc.

## 6. Headline Claim and the Exact Experiment That Produces It

**Headline claim.** *A 7B code LLM, trained with a decoupled masked-gradient LoRA objective against free per-test execution labels, expresses per-test-case confidence that discriminates passing from failing requirements at AUROC 0.75–0.85 on contamination-controlled LiveCodeBench — the first self-expressed structured confidence signal for code, and one no scalar-confidence method can produce.*

**The headline number, precisely defined.** Pool all (solution, test-case) pairs across the held-out evaluation set. For each pair, the label is whether that test passes (ground truth via execution), and the prediction is the model's expressed confidence for that test slot. **Per-test AUROC** is the area under the ROC curve over this pooled set — it measures whether the model's per-slot confidence ranks passing tests above failing tests. This is the number with no incumbent. Report it with bootstrap 95% CIs (resampling problems, not test-cases, to respect the dependence structure).

**The exact experimental protocol, end to end.**

*Data.* Training pool: 2,000–4,000 problems drawn from MBPP (974, human-written tests), a filtered APPS/TACO subset (≥3 test cases/problem to dodge the verification-ceiling risk [12], and to guarantee per-test label spread), and a LiveCodeBench *train-window* release [15]. TACO is the density workhorse: ~50–200 test cases/problem in its test split [13], versus LiveCodeBench's ~17 [15] and HumanEval's ~7 — dense per-test labels are exactly what the structured target needs. CodeContests+ is the clean alternative, ~25–98 tests/problem with test-suite noise repaired [14]. Evaluation: held-out LiveCodeBench (contamination-controlled, primary) [15][16] + HumanEval (legacy) + a held-out TACO slice. Strict train/eval separation by problem and by release window; no problem appears in both.

*Labels (free).* For each training problem, sample n=10 solutions from the base model and execute each against the full test suite. The per-test pass rate across the 10 samples is the continuous [0,1] target for that test slot; the per-problem mean pass rate is the scalar target for the baseline. **This reuses the exact computation the current manuscript already performs for its 0.987 signal — zero incremental labeling design, only more test suites executed.** Label-generation cost is CPU-bound execution plus one batch of GPU sampling.

*Training.* LoRA r16/alpha32 on Q/V (ConfTuner config [3]) or the standard attention+MLP set (Yaldiz config [6]). Warm-start SFT: tokenized-Brier loss on the confidence block against per-test targets, ~2–3 epochs, 2,000–4,000 problems — ConfTuner reports ~4 minutes at 2,000 examples on 4×A40, so <1 GPU-hour here [3]. Optional on-policy refinement: masked-gradient GRPO/DPO, confidence advantage = bounded Brier reward against the hybrid instance+group per-test target R_IG, reasoning advantage = binary pass/fail, following DCPO [1].

*Metrics.* Primary: per-test AUROC (structured headline). Secondary: scalar-confidence AUROC (vs DCPO [1]), debiased/equal-mass ECE [17], per-test adaptive ECE, and a **risk-coverage utility curve** (the fallback, guaranteed). Report per-seed distributions across ≥3 seeds, never a favorable subset.

*Ablations (each cheap, each answering a specific reviewer objection).*
1. **Joint vs decoupled** — run the single-objective version (Rewarding Doubt style [2]); if it collapses, this is the direct empirical instantiation of Proposition 4.2 [1].
2. **Continuous vs 3-tier targets** — relabel with coarse tiers; if discrimination drops, this pins the current manuscript's collapse on coarse labels, not on self-report per se.
3. **Self-report vs decoupled-head vs external probe** — settles the architecture question on code with matched AUROC.
4. **N-sweep** — per-test AUROC vs N∈{5,10,20,50,100} on a ~300-problem subset; expected to saturate near N=10, rebutting "just use N=100" [3].

The headline experiment *is* the primary training run plus the per-test AUROC readout; everything else is supporting.

## 7. Why the Headline Will Likely Land: Feasibility on Single-GPU 7B Compute

Feasibility is where this draft earns its keep. The claim is not "it should be fine"; it is a line-item GPU-hour budget with named risks.

**Label generation.** Anchoring to Uncertainty Distillation's reported ~0.377 sec/completion (which *includes* NLI-clustering overhead we don't pay, since code equivalence is CPU-side execution diffing), and discounting ~20%:

| Pool | N=10 (matches manuscript) | N=20 | N=100 (ablation only) |
|---|---|---|---|
| 2,000 problems | ~1.7 GPU-hr | ~3.4 GPU-hr | ~16.8 GPU-hr |
| 4,000 problems | ~3.4 GPU-hr | ~6.7 GPU-hr | ~33.5 GPU-hr |

Test execution is CPU-bound and parallelizable; the named risk is wall-clock, not GPU-hours — running 40,000–800,000 test executions needs a sandboxed harness stood up on Day 1.

**Training.** LoRA at this scale is a rounding error: ConfTuner reports 4 minutes at 2,000 examples [3]; Raschka's linear-scaling benchmark puts a 50k-example 7B LoRA run at 1.85 hours on a single A100, so 2,000–8,000 examples is well under an hour [18]. The on-policy refinement stage is the cost driver; extrapolating Yaldiz's ~150 GPU-hours/model to a single 7B model with a short refinement gives ~50–100 GPU-hours as the upper bound if full refinement is used [6].

**Generation throughput** is not a bottleneck: vLLM v0.6.0 reports large aggregate throughput on 7–8B models on A100/H100-class GPUs, and single-stream ~77 tok/s is the pessimistic floor [19].

**Total budget.** One clean pass — label generation + warm-start SFT + eval sampling + N-sweep + 2–3 baseline reproductions — is **~15–25 GPU-hours**. With a 3× buffer for debugging and reruns, **~45–75 GPU-hours** — inside 10 days at ~5–6 active GPU-hours/day on a single A100-40GB or GH200 [3][6][11][18]. If the full on-policy GRPO refinement is included, add the ~50–100 GPU-hours above; the pre-registered plan uses warm-start-SFT-only as the primary (cheaper, and ConfTuner shows SFT-with-proper-scoring alone reaches strong AUROC [3]), with refinement as an upside experiment run only if the pilot leaves time.

**Why the number itself is likely favorable.** Three grounding facts. First, the *labels are near-oracle* — code's per-test execution signal is crisp and low-noise, unlike QA's exact-match/LLM-judge labels, so the target the model distills toward is cleaner than anything in the QA calibration literature; the internal per-test signal the manuscript already sees is near-ceiling [8]. Second, the *mechanism is proven adjacent* — DCPO hit scalar AUROC 0.796–0.914 on these exact benchmarks with this exact decoupled recipe [1]; the structured version distills a *richer* free label, and there is no reason per-test discrimination should fall below the 0.75 floor when the scalar version clears 0.80. Third, the *collapse cause is understood and removed* — continuous instance-level targets + decoupled gradients directly address both failure mechanisms named by DCPO and CAPO [1][4]. The residual risk is entirely on whether structured discrimination *survives the decode-to-expressed step*, which the Day-3 pilot resolves before any money is spent on the full run.

## 8. Supporting Results, Failure Mode, and Pre-Registered Fallback

**Supporting results (three, each landable independently).**
1. *Scalar replication vs DCPO.* Reproduce the scalar-confidence AUROC (expect ~0.80–0.90 [1]) as a sanity baseline and explicit positioning point — "our structured signal matches the scalar incumbent on the scalar metric while adding a capability it lacks."
2. *Risk-coverage utility curve* on the internal signal (see fallback) — the guaranteed floor.
3. *Ablation panel* (Section 6) — each rebuts a specific reviewer objection and doubles as evidence for the mechanism.

**The most likely failure mode.** The structured target fails to train: the confidence block collapses to a near-constant vector despite continuous targets and decoupling, reproducing the manuscript's own mean-0.900 pathology at vector granularity. This would falsify the "coarse-label + data-starvation" diagnosis and point to a deeper representational limit. Probability: moderate — the mechanism is sound but untested on code at vector granularity, and LoRA r16 may lack capacity to represent per-slot structure.

**The pre-registered fallback (guaranteed floor).** If the trained structured signal underperforms (per-test AUROC < 0.70 after both the per-test and per-category attempts), the paper pivots its headline to a **Clopper-Pearson risk-controlled selective-generation policy built on the untouched internal sampling signal — never on the trained output.** This is a load-bearing scoping point: the collapsed trained signal has no score spread and cannot be thresholded, so any wrapper must act on the internal signal directly [9]. Pre-registered targets: **coverage 70–90% at accepted-output error ≤2–5% at α=0.10** (primary), with α=0.05 as a stretch. The floor is well-grounded: Sharma & David hit 77.8–88% coverage at ≤0.02% error via execution clustering on LiveCodeBench [8], and CODEREFUSER delivers ~3.5× more answered tasks than a perplexity baseline at matched risk [10]. Because the manuscript's internal signal (AUROC 0.987) is a stronger discriminator than anything inside CIC's own general-QA tests [9], the wrapped numbers should land at or above the Sharma & David ceiling.

**The fallback's own pre-registered failure mode.** CIC documents that at α=0.05 with a weak signal and a small calibration set, the calibration procedure returns *no valid threshold* on up to 100% of splits [9]. HumanEval's 164 problems is thin. Pre-registered fallback-to-the-fallback: if α=0.05 is infeasible at n=164, expand the calibration pool to HumanEval+MBPP (~400+ problems, inference-only, single-GPU-cheap) and, if still infeasible, restrict the claim to α=0.10 — a weaker but still defensible guarantee [9].

**The de-scope ladder, pre-registered with numeric gates.**

| Level | Headline | Gate to earn it | Status |
|---|---|---|---|
| L1 (bold) | Per-**test-case** confidence, AUROC 0.75–0.85 | Day-3 pilot per-test AUROC > 0.65 on ~300 problems | Target |
| L2 (safe-bold) | Per-**category** confidence (grouped test slots) | L1 fails but per-category AUROC > 0.65 | Fallback-1 |
| L3 (floor) | Risk-controlled selective generation, 70–90% cov @ ≤2–5% err | Both above fail; wrapper on internal signal | Guaranteed |

Every level is publishable; L3 is guaranteed by off-the-shelf mechanisms on a signal known to be strong [8][9][10]. The paper cannot be dead.

**Day-by-day decision calendar (10-day AAAI-27 sprint).**
- **Day 1 — timing pilot.** Time 50 completions and a full test-suite execution batch on the target GPU; stand up the sandbox harness; finalize the problem pool (confirm LiveCodeBench train-window size and APPS/TACO ≥3-test survivors). *Gate: if 40k–800k executions exceed ~2 days wall-clock even parallelized, de-scope the pool now.*
- **Days 2–3 — collapse-check pilot.** ~300-problem warm-start SFT at per-test granularity; read per-test AUROC. *Gate: >0.65 → proceed L1; ≤0.65 → try per-category (L2); both ≤0.65 → commit to L3 and reallocate remaining days to the selective-generation result.*
- **Days 4–6 — full run.** Full-pool warm-start SFT, eval on held-out LiveCodeBench+HumanEval+TACO, bootstrap CIs.
- **Days 7–8 — ablations + fallback.** Joint-vs-decoupled, continuous-vs-tier, N-sweep, self-report-vs-head; risk-coverage curve on internal signal (runs regardless of L-level).
- **Days 9–10 — write + reproducibility checklist + code freeze.** Code and data must be *submitted*, not promised — AAAI treats "released after acceptance" as no evidence of reproducibility [21].

## 9. Novelty Defense Against the Closest Prior Work

The empty cell is the conjunction of four axes; each nearby work misses at least one (all full-text-verified).

- **DCPO** [1] — same decoupled recipe, same benchmarks, but emits **one scalar** per solution. Misses axis 2 (granularity). This is the incumbent to *position against*, not beat: our scalar-replication baseline matches it, and our structured signal adds what its single output cannot express.
- **FLARE** (execution + line-level) — misses axes 1 and 2: a *separate diagnostic transformer* (not the coder's self-report) at *line* granularity (spatial, not per-requirement functional), and reports no AUROC/calibration.
- **CURE / Think-Through-Uncertainty** — self-report + per-claim + AUROC + a 3-stage anti-collapse pipeline, but general long-form factuality with a *noisy VeriScore oracle* and no code; AUROC only 0.667. Misses axes 3 (noisy oracle vs our clean execution oracle) and 4 (domain). Our clean per-test oracle should beat its 0.667.
- **Atomic Calibration** — decompose-and-calibrate framing + AUROC, but an *analysis/taxonomy paper with no training method*, NL-QA only. Misses axes 3 and 4 and supplies no method.
- **Gros & Devanbu, "Localized Calibrated Uncertainty in Code LMs" (Dec 2025)** — the closest *published title*: calibrated per-line/span edit probability via an *external white-box probe*. Misses axes 1 (external probe, not self-expressed) and 2 (spatial per-line, not functional per-test). Cite-and-distinguish prominently.
- **VeRPO** — per-test partial success as a *correctness reward*, never a confidence output. Confirms the "free per-test labels for *confidence*" cell is unoccupied.
- **RLCM** — decoupled hidden-state probe, math-trained, OOD to code, never reports AUROC. Misses axes 1, 2, 3, 4.

**The one-sentence defense:** the paper combines CURE's self-reported, decoupled-trained, AUROC-evaluated methodology with FLARE's execution-verifiable code substrate at *test-case* granularity — a conjunction no prior work attempts — and uniquely replaces the noisy external verifier (CURE, Atomic) and the separate diagnostic model (FLARE, Gros & Devanbu) with the code's *own deterministic per-test execution oracle*, which is both a cleaner training signal and free.

**Honest scoop caveat (pre-registered for the user, not the paper).** A UT Dallas group (Rathnasuriya & Yang) has two under-review, not-yet-public papers with on-topic titles and a public roadmap paper that is scalar per-prediction abstention (partial, not per-test) [8-adjacent]. Content unknown; genuine timing risk. Mitigation: move fast, frame the per-test-case self-expressed axis sharply, and lead with the four-axis conjunction that their public work does not occupy. Novelty confidence: **high, with a named caveat.**

## 10. AAAI-27 Topic Alignment: Primary and Secondary Keywords

**Primary keyword (verbatim from the AAAI-27 areas-and-topics list):** **"ML: Bayesian Learning & Uncertainty Quantification."** There is no separate "ML: Calibration" keyword; calibration falls under this uncertainty-quantification keyword [20]. The paper's main methodological contribution — a training objective that produces calibrated, discriminative *uncertainty estimates at a new granularity* — is a general ML/UQ advance whose substrate happens to be code. AAAI's own selection rule files a general ML advance demonstrated on code under ML, not NLP/Software Engineering, unless the contribution is fundamentally about code-specific structure [20]. Here the contribution *is* general (a decoupled proper-scoring objective for structured confidence), and code is the enabling substrate (free per-test labels), so ML/UQ is correct.

**Secondary keywords (up to five allowed; use two):** "NLP: Code Generation / Program Synthesis" (the application substrate) and "ML: Evaluation, Benchmarking, Datasets & Analysis" (the AUROC-primary evaluation methodology and contamination-controlled protocol) [20].

**Why it will not drift out of scope.** The headline metric (per-test AUROC), the training objective (bounded proper scoring rule), and the collapse-proof mechanism (decoupled gradients) are all uncertainty-quantification methodology; the code-specific element (per-test labels) is an *enabler*, not the contribution's core. This keeps the paper legible to the UQ community best positioned to evaluate it and away from the application-track redirection that a measurement study would risk [20][22]. **Format compliance:** 7 pages main content, up to 9 total (extra pages references + the reproducibility checklist, which lives in the reference-only pages) [21][22]; mandatory reproducibility checklist with code/data submitted at submission time, not promised [21].

**AAAI-27 vs next-venue contingency.** The deadlines are strict: abstracts July 21, full papers July 28, code July 31, 2027 [21]. If the Day-3 collapse-check pilot slips or the sandbox harness eats more than its budgeted wall-clock, the *identical paper* targets the next cycle (ICLR/ACL/NeurIPS) with zero loss of novelty — the contribution is venue-agnostic, and arXiv/workshop preprints do not count as prior publication for AAAI, so a NeurIPS submission could be retracted and resubmitted [21]. Pre-registered rule: **if by Day 6 the full run has not produced a bootstrap-stable per-test AUROC (L1 or L2) *or* a complete risk-coverage curve (L3), pivot to the next venue rather than submit a thin paper.** Do not burn the AAAI slot on an under-powered result.

## 11. The Shortlist: 5–10 Load-Bearing Papers

1. **DCPO — Decoupled Confidence Policy Optimization** [1]. *Contributes:* the decoupled masked-gradient recipe and Proposition 4.2 (gradient-conflict proof); scalar code AUROC 0.796–0.914. *Leaves open:* structure — emits one scalar; never per-test. The incumbent to position against and the method to import.
2. **ConfTuner** [3]. *Contributes:* tokenized-Brier proper-scoring loss, zero extra sampling, ~2,000-example convergence, minutes-scale training. *Leaves open:* code, and structured targets. Supplies the warm-start objective and the feasibility floor.
3. **Rewarding Doubt** [2]. *Contributes:* single-A40 LoRA RL, AUROC 0.859, proof that a joint objective can discriminate and that ECE hides collapse. *Leaves open:* code. The single-GPU feasibility existence-proof and the joint-vs-decoupled ablation.
4. **RLCR / Beyond Binary Rewards** [5]. *Contributes:* bounded-proper-scoring-rule theorem and the unbounded-log-score abstention-collapse experiment. *Leaves open:* code. Justifies the non-negotiable boundedness of the Brier reward.
5. **CAPO** [4]. *Contributes:* proof that GRPO's implicit surrogate is AUC-inconsistent; the "identical confidence satisfies calibration yet fails to distinguish" argument. *Leaves open:* code. The formal spine of the AUROC-primary decision.
6. **Yaldiz et al., Balancing Classification and Calibration** [6]. *Contributes:* LoRA r16 decoupled training on 4×A100-40GB, ~500 GPU-hrs/3 models — the single-GPU LoRA feasibility precedent. *Leaves open:* reports no AUROC. Anchors the compute budget.
7. **Sharma & David, Uncertainty Estimation for Code** [8]. *Contributes:* symbolic-execution clustering, 77.8–88% coverage at ≤0.02% error on LiveCodeBench; only execution restores signal. *Leaves open:* no trained expressed signal. The abstention ceiling and the label-source justification.
8. **CIC — Uncertainty-Aware Abstention** [9]. *Contributes:* Clopper-Pearson risk-controlled selective generation; documents the α=0.05 infeasibility failure mode. The fallback mechanism and its pre-registered failure.
9. **LiveCodeBench** [15] + **Riddell et al., Quantifying Contamination** [16]. *Contributes:* contamination-controlled time-windowed eval, and the proof HumanEval/MBPP are contaminated. Converts the contamination threat into a robustness pillar.
10. **TACO** [13] / **CodeContests+** [14]. *Contributes:* dense per-test labels (~50–200 and ~25–98 tests/problem respectively). The data substrate that makes per-test targets learnable; CodeContests+ repairs test-suite noise [14].

Supporting cast cited above: Roelofs et al. (debiased ECE) [17], ConSelf (LiveCodeBench disconnect replication) [11], CODEREFUSER (code abstention) [10], ORCE (decoupled architecture) [7], Verification Limits (test-strength filtering) [12], vLLM [19] and Raschka [18] (throughput anchors).

---

## Sources

[1] Ma et al., *DCPO: Decoupling Reasoning and Confidence — Resurrecting Calibration in Reinforcement Learning*, ICML 2026. arXiv:2603.09117. https://arxiv.org/abs/2603.09117
[2] Bani-Harouni et al., *Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of LLMs*, ICLR 2026 (TU Munich). arXiv:2503.02623. https://arxiv.org/abs/2503.02623
[3] *ConfTuner: Training Large Language Models to Express Their Confidence Verbally*, NUS, NeurIPS 2025. arXiv:2508.18847. https://arxiv.org/abs/2508.18847
[4] Wang et al., *CAPO: Calibration-Aware Policy Optimization for Reasoning LLMs*, ACL 2026. arXiv:2604.12632. https://arxiv.org/abs/2604.12632
[5] Damani et al., *Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty (RLCR)*, MIT. arXiv:2507.16806. https://arxiv.org/abs/2507.16806
[6] Yaldiz et al., *Balancing Classification and Calibration Performance in Decision-Making LLMs*. arXiv:2601.13284. https://arxiv.org/abs/2601.13284
[7] Li et al., *ORCE: Order-Aware Alignment of Verbalized Confidence in Large Language Models*, Stony Brook. arXiv:2605.12446. https://arxiv.org/abs/2605.12446
[8] Sharma & David, *Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation*. arXiv:2502.11620. https://arxiv.org/abs/2502.11620
[9] Dong & Shinnou, *CIC: Uncertainty-Aware Abstention in Large Language Models with Provable Alignment*, 2026. https://arxiv.org/abs/2607.04430
[10] Zhou et al., *CODEREFUSER: Task Abstention for Large Language Models in Code Generation*, 2026. https://arxiv.org/abs/2606.17029
[11] *ConSelf: Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus*, ICPC 2026.
[12] Gureja et al., *Verification Limits Code LLM Training*, Cohere Labs, Sep 2025. arXiv:2509.20837. https://arxiv.org/abs/2509.20837
[13] Li et al., *TACO: Topics in Algorithmic COde generation dataset*, Dec 2023. arXiv:2312.14852. https://arxiv.org/abs/2312.14852
[14] Wang et al., *CodeContests+: High-Quality Test Case Generation for Competitive Programming*, Jun 2025. arXiv:2506.05817. https://arxiv.org/abs/2506.05817
[15] Jain et al., *LiveCodeBench: Holistic and Contamination-Free Evaluation of LLMs for Code*, UC Berkeley/MIT, 2024. arXiv:2403.07974. https://arxiv.org/abs/2403.07974
[16] Riddell, Ni & Cohan, *Quantifying Contamination in Evaluating Code Generation Capabilities of Language Models*, 2024. arXiv:2403.04811. https://arxiv.org/abs/2403.04811
[17] Roelofs, Cain, Shlens & Mozer, *Mitigating Bias in Calibration Error Estimation*, AISTATS 2022. arXiv:2012.08668. https://arxiv.org/abs/2012.08668
[18] Raschka, *Practical Tips for Finetuning LLMs Using LoRA (Low-Rank Adaptation)*, blog. https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms
[19] vLLM Team, *vLLM v0.6.0: 2.7x Throughput Improvement and 5x Latency Reduction*, vLLM blog. https://blog.vllm.ai/2024/09/05/perf-update.html
[20] AAAI-27 *Areas and Topics*. https://aaai.org/conference/aaai/aaai-27/areas-and-topics/
[21] AAAI-27 *Submission Instructions*. https://aaai.org/conference/aaai/aaai-27/submission-instructions/
[22] AAAI-27 *Main Technical Track Call for Papers*. https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/
