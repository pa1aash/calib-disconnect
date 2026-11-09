# Cross-locus comparisons — the argumentative spine

The five depth investigators converge on a concrete, feasible METHOD but fork sharply on
WHERE the novelty now lives, because full-text reading of DCPO (ICML 2026) revealed it
occupies more of the "scalar expressed confidence for code" cell than the width sweep assumed.
The final proposal must be built around resolving Tension 1.

## Tension 1: DCPO occupies the scalar-verbal-confidence-for-code cell — where is the residual novelty? [CENTRAL]

- **Locus `code-verbal-calibration-occupied-or-open`** ([[interim-report-code-verbal-calibration-occupied-or-open]]) commits: the cell "expressed + code-native + AUROC" is OPEN; RLCM uses a probe and never reports AUROC. (confidence 60-70%)
- **Locus `collapse-proof-training-objective`** ([[interim-report-collapse-proof-training-objective]]) commits, with a load-bearing CORRECTION: DCPO (ICML 2026) trains a DECODED `<conf>` block against a hybrid instance+group EXECUTION-PASS-RATE target and reports AUROC 0.796–0.914 on LiveCodeBench v5/v6 + HumanEval+ (Qwen3-8B), beating joint-reward RLCR on AUROC AND accuracy. (confidence medium)
- **The cross-locus dynamic:** These directly conflict on the novelty question. DCPO already demonstrates the naive headline ("train a code LLM to verbalize calibrated, discriminative scalar confidence, measured by AUROC") — same decoded interface, same execution-pass-rate target, same benchmarks. The novelty-occupancy investigator's "open" verdict rested on RLCM (probe, no AUROC) and missed DCPO's code results. Honest conclusion: the SCALAR expressed-confidence-for-code headline is now substantially OCCUPIED. Pursuing it is the "X but for code / DCPO-lite on LoRA" incrementalism trap the user explicitly wants to avoid (P1 = novelty).
- **How the draft should engage this:** The recommendation MUST pivot the headline to the code-unique residual that DCPO/RLCM/Rewarding-Doubt structurally cannot produce because they all emit ONE scalar per answer: **calibrated STRUCTURED / per-test-case (per-requirement) confidence that LOCALIZES which part of a solution will fail.** Code's execution gives a VECTOR of per-test outcomes (QA/math have a single correctness bit), so the fine-grained ground-truth labels are FREE from the n-sample runs the disconnect paper already computes. DCPO's decoupled training recipe becomes the METHOD (keeps P2 high); the scalar-AUROC result becomes a replication/sanity baseline, explicitly positioned against DCPO, not the contribution. Step 8 corpus-critic MUST verify per-test/structured code-confidence is genuinely unoccupied before this locks.
- **Calibration note:** Both investigators are medium-confidence; the correction (DCPO code results, grep+table verified) is high-confidence fact and overrides the "open" verdict for the scalar framing. The residual (structured confidence) is currently UNVERIFIED for occupancy — this is the single most important gap-check for step 8.

## Tension 2: Decouple vs. joint objective — the collapse-proof recipe (holds regardless of headline)

- **Locus `collapse-proof-training-objective`** commits: DCPO-style masked-gradient DECOUPLED objective (separate confidence-token advantage, bounded Brier reward vs continuous execution-pass-rate), LoRA-adapted single-GPU; Prop 4.2 formally names the gradient conflict our 274-example joint SFT hit.
- **Locus `self-report-vs-external-judge-vs-probe-reversal`** ([[interim-report-self-report-vs-external-judge-vs-probe-reversal]]) commits: same-model DECOUPLED self-report (frozen generation + 2nd-turn LoRA confidence head, proper-scoring loss vs pass-rate) — "self-report fails" is only true UNTRAINED.
- **The cross-locus dynamic:** Strong CONVERGENCE from independent paths — both independently land on "decouple the confidence signal from generation + train it with a proper scoring rule against the continuous execution-pass-rate." This is the robust methodological core whether the headline is scalar or structured. The counter-evidence (Rewarding Doubt: joint reward, AUROC 0.859, single-A40 LoRA) shows decoupling may not be strictly necessary, but decoupling is the safer bet given our documented collapse.
- **How the draft should engage this:** State this decoupled + continuous-pass-rate + bounded-Brier recipe as THE method with high confidence; cite Prop 4.2 + our own collapse as the twin motivation for decoupling; note Rewarding-Doubt as the joint-objective ablation to run.
- **Calibration note:** Convergence of two medium-confidence positions on the same recipe raises combined confidence to medium-high. Named open risk (both loci): does masked-gradient decoupling survive LoRA (untested on code)? → a Day-1 pilot resolves it.

## Tension 3: Ambition vs. the 10-day / single-GPU budget

- **Locus `label-and-data-feasibility`** ([[interim-report-label-and-data-feasibility]]) commits: YES feasible — ConfTuner-style tokenized-Brier on the EXISTING n=10 pass-rate labels, ≥2000 real problems, ~15-25 GPU-hrs, fits single A100/GH200 in the window.
- **Tension 1's pivot** demands structured/per-test-case confidence, a harder training target than one scalar.
- **The cross-locus dynamic:** Complication, not conflict. The feasibility verdict was scoped to the SCALAR target. Structured confidence is a harder objective — BUT its fine-grained labels are equally free (per-test pass rates already computed), and the training cost is comparable (same LoRA, richer target). The tight AAAI-27 deadline (paper 2026-07-28) makes a from-scratch structured-confidence result risky in 10 days.
- **How the draft should engage this:** Present the structured-confidence headline with a PRE-REGISTERED de-scoped version (e.g., per-test-category rather than per-individual-test; single model Qwen2.5-Coder-7B first, DeepSeek as time permits). Recommend a Day-1 timing pilot. Be explicit that if AAAI-27's 10-day window is too tight, the identical paper targets the next venue (ICLR/ACL/NeurIPS) — the contribution is venue-agnostic.
- **Calibration note:** feasibility medium-high for scalar; structured adds risk → hence the mandatory fallback (Tension 4).

## Tension 4: The guaranteed floor — fallback keeps the paper alive

- **Locus `fallback-utility-of-collapsed-confidence`** ([[interim-report-fallback-utility-of-collapsed-confidence]]) commits: if the trained interface underperforms, wrap the UNCOLLAPSED internal sampling signal in a CIC-style risk-controlled selective-generation policy (70-90% coverage @ ≤2-5% err, pre-reg α=0.10); publishable-grade insurance, not the headline.
- **The cross-locus dynamic:** This is the floor under Tensions 1+3's upside. Reinforcement, not conflict: even a partial structured-confidence result plus the risk-coverage utility curve = a complete, landable paper. Ceilings to benchmark: CODEREFUSER 26.5pt precision / ~3.5x coverage; Sharma&David 77.8-88% coverage @ ≤0.02% FPR on LiveCodeBench.
- **How the draft should engage this:** State the fallback explicitly in the proposal's "failure mode + pre-registered fallback" section (a query requirement). Frame the paper so the headline is upside and the utility/selective-generation result is guaranteed downside protection.
- **Calibration note:** high confidence the fallback lands (mechanism is off-the-shelf + code abstention already hits strong numbers); its own novelty is modest, so it cannot be the headline.

## Tension 5: Which AUROC target is a safe bet, given DCPO's numbers?

- **`collapse-proof`** gives the anchor: DCPO scalar AUROC 0.796 (LCB-v5) → 0.914 (HE+); Rewarding Doubt 0.859 (QA). Our own sampling ORACLE is 0.987 (upper bound the expressed signal is distilling toward).
- **The cross-locus dynamic:** These set realistic expectations. A scalar expressed-confidence AUROC in the 0.80-0.90 band on code is a SAFE bet (DCPO already got it). A structured/per-test AUROC is unbenchmarked — likely lands 0.70-0.85 per-test, which is still a strong first result because NO prior number exists.
- **How the draft should engage this:** Set the headline number expectation honestly: scalar ~0.85 (safe, but occupied → baseline); structured per-test ~0.75-0.85 (novel, no incumbent to beat → the contribution). Emphasize the paper wins on NOVELTY of the capability, not on beating DCPO's scalar number.
- **Calibration note:** P2 (confidence result lands) is well-supported for BOTH numbers by DCPO's existence; the risk is entirely on P1 (is structured confidence novel + does it train well), which the fallback covers.

---

## Step 8 corpus-critic UPDATE — novelty verdict: PARTIALLY-OVERLAPPING → headline SURVIVES with a precise defense

Adversarial scoop-search (20+ arXiv queries, DCPO citation graph, vault) CONFIRMS the exact
conjunction is EMPTY: "a code LLM's OWN self-reported confidence, discriminative at per-test /
per-requirement granularity, AUROC-evaluated against EXECUTION-verified ground truth." The three
closest works each miss on a different axis (full-text verified):
- **FLARE** (2606.03852): execution + fine-grained BUT (a) a SEPARATE diagnostic transformer, not
  the coder's self-report, (b) LINE-level not test-case, (c) grep-confirmed ZERO "AUROC"/"calibrat".
  → DISTINCT.
- **CURE / Think-Through-Uncertainty** (2604.12046): self-report + per-claim + AUROC + a 3-stage
  SFT→DPO→GRPO pipeline explicitly avoiding the uniform-high-confidence collapse — BUT general
  long-form factuality, ground truth from a NOISY retrieval fact-checker (VeriScore), NO code/
  execution. AUROC only 0.667 (noisy oracle). → PARTIALLY-OVERLAPS on method, DISTINCT on domain.
- **Atomic Calibration** (2410.13246): decompose-and-calibrate framing + AUROC BUT an ANALYSIS/
  taxonomy paper (no training method), NL-QA only, grep-confirmed zero "code/test case/execution".
  → PARTIALLY-OVERLAPS on framing only.

**THE NOVELTY DEFENSE (precise, one sentence):** the paper combines CURE's self-reported /
decoupled-trained / AUROC-evaluated confidence methodology with FLARE's execution-verifiable code
substrate, at TEST-CASE granularity — a combination no prior work attempts; and it uniquely
replaces the noisy external verifier (CURE/Atomic) and the separate diagnostic model (FLARE) with
the code's OWN deterministic per-test execution oracle, which is both a cleaner training signal
(should beat CURE's 0.667) and free. Papers to cite-and-distinguish in Related Work: FLARE, CURE,
Atomic Calibration, fine-grained code-revision calibration (2604.06723), VeRPO (per-test reward for
CORRECTNESS not confidence), DCPO (scalar). Confidence in novelty defense: HIGH.

## Step 8 gap-fetch UPDATE 2 — two nearby competitors + one live scoop risk (sharpen the wedge)

- **Gros & Devanbu, "Localized Calibrated Uncertainty in Code Language Models" (arXiv:2512.24560,
  Dec 2025)** — the closest PUBLISHED title. Assigns calibrated per-LINE/SPAN probability of being
  edited in a minimal repair patch, via an EXTERNAL white-box probe on model internals. Distinct on
  our two load-bearing axes: (a) axis = SPATIAL (which lines) not FUNCTIONAL (which test/requirement
  fails); (b) EXTERNAL probe, not the LLM SELF-EXPRESSING. Must be cite-and-distinguished prominently.
- **VeRPO (2601.03525): DISTINCT** — per-test partial success as a CORRECTNESS reward, never a
  confidence output. Confirms our "free per-test labels for CONFIDENCE" framing is unoccupied.
- **UA-ChatDev (2607.02186): PARTIAL** — token log-prob per-agent-phase (the AUROC-0.668 proxy our
  paper already dismissed), not per-test. Distinct.
- **Benchmark density**: TACO (~50-200 tests/problem) and CodeContests+ (dense) >> LiveCodeBench
  (~17) >> HumanEval (~7). Use TACO/CodeContests for dense per-test labels. (Exact counts
  WebSearch-sourced, LOW confidence — verify against dataset cards before citing.)
- **>>> LIVE SCOOP RISK (surface to user) <<<**: UT Dallas group (Rathnasuriya & Yang) has TWO
  UNDER-REVIEW, not-yet-public papers with on-topic titles — "Beyond Confidence: Rethinking
  Uncertainty Calibration in Deep Code Models" and "Beyond Execution: Uncertainty Estimation and
  Abstention in LLM-Based Code Generation." Content unknown; their public ICSE-NIER'26 short paper
  is SCALAR per-prediction abstention (PARTIAL, not per-test). Genuine timing risk — the paper should
  move fast and frame the per-test-case self-expressed axis sharply to stay differentiated.

### SHARPENED NOVELTY WEDGE (final): the empty cell is the CONJUNCTION of four axes —
(1) SELF-EXPRESSED/decoded by the coder itself (vs external probe: FLARE, Gros&Devanbu, RLCM, BAP);
(2) per-TEST-CASE/REQUIREMENT functional decomposition (vs scalar: DCPO; vs per-line spatial:
Gros&Devanbu, FLARE; vs per-claim NL: CURE, Atomic); (3) trained against the code's own EXECUTION
oracle (vs noisy fact-checker: CURE/Atomic; vs edit-dataset: Gros&Devanbu); (4) on CODE (vs QA/math:
Rewarding Doubt, RLCR, CURE, Atomic). No work occupies all four. Novelty confidence: HIGH but with a
named, honest scoop caveat (UT Dallas under-review).

## Distilled resolution for the drafters
The paper the evidence supports: **"Structured, execution-grounded confidence for code — training a code LLM to express calibrated, DISCRIMINATIVE confidence at per-requirement/per-test-case granularity that localizes which part of a solution will fail, a capability enabled by code's per-test verifiability and impossible for the scalar-confidence methods (DCPO, RLCR, Rewarding Doubt) that define the current frontier."** Method = DCPO-style decoupled masked-gradient LoRA training against continuous per-test execution-pass-rate targets with a bounded Brier reward (proven on code by DCPO at the scalar level; extended here to structured targets whose labels are free). Primary headline = per-test localization/calibration AUROC (no incumbent). Supporting = scalar-confidence replication (vs DCPO) + risk-controlled selective-generation utility (the guaranteed floor). AAAI-27 primary topic: ML: Bayesian Learning & Uncertainty Quantification. Step 8 MUST verify structured/per-test code-confidence is unoccupied.
