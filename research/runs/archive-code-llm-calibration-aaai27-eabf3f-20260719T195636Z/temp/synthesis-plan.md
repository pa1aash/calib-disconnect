# Synthesis plan

## Core thesis (1-2 sentences)
The paper to write extends the diagnostic "calibration disconnect" into a prescriptive method:
train a 7B code LLM to SELF-EXPRESS calibrated, discriminative confidence at PER-TEST-CASE /
PER-REQUIREMENT granularity — localizing which part of its own solution will fail — via a
single-GPU decoupled masked-gradient LoRA objective (bounded Brier reward against the free per-test
execution-pass-rate labels). It is architected as a risk-stratified three-tier paper so Priority-1
novelty (structured per-test confidence, no incumbent AUROC) and Priority-2 confidence (a guaranteed
selective-generation floor + a DCPO-positioned scalar replication) live in different tiers and the
paper cannot come out dead.

## The strongest argumentative beats
1. **The two-channel split (Draft A/C §frontier)** — internal/execution confidence for code is
   near-perfect (0.987) and now CONSENSUS; the expressed channel fails (log-prob 0.668, verbal 0.52).
   The open frontier is COMMUNICATION, not detection. Load-bearing because it reframes the disconnect
   paper's own strength as the non-novel part.
2. **The DCPO correction (all 3)** — DCPO (ICML'26) already trains a decoded scalar `<conf>` on code
   to AUROC 0.796-0.914, so the scalar headline is OCCUPIED. This is the honest pivot that saves the
   user from an incremental "DCPO-lite" desk-reject. Must be stated plainly, not buried.
3. **The four-axis novelty wedge (Draft A §9)** — the empty conjunction: self-expressed × per-test-case
   × execution-oracle × code. Each closest competitor (DCPO scalar; FLARE/Gros&Devanbu external+spatial;
   CURE/Atomic noisy-NL; VeRPO reward-not-confidence) misses exactly one axis.
4. **"Will it land" = 3 proven ingredients (Draft A §7)** — verbalized-RL discriminates (0.85-0.86, QA);
   decoupled training works on code scalar (DCPO); per-unit self-report with anti-collapse pipeline works
   (CURE 0.667 on a NOISIER oracle → deterministic execution oracle should EXCEED it). Turns the headline
   from a gamble into an assembly.
5. **The risk-stratified three-tier architecture (Draft B)** — floor (guaranteed) + scalar (high-conf) +
   structured (novel upside). The organizing principle that satisfies P1 AND P2. THE structural spine.
6. **The collapse-proof recipe (Draft C + collapse-proof interim)** — decoupled masked-gradient LoRA +
   bounded Brier + CONTINUOUS per-test targets fixes the documented SFT-collapse (DCPO Prop 4.2 + our
   274-example mean-0.900 collapse are the twin motivation).
7. **The de-scope ladder + 10-day calendar + venue contingency (Draft C + B)** — Day-2/3 pilot go/no-go
   gate; L1 per-test → L2 per-category → L3 floor; AAAI-27 (paper 2026-07-28) vs ICLR-27 pivot. The
   anti-dead-paper operational spine + the honest timeline the user MUST see.

## Section structure (required_section_headings, in order)
1. Frontier; 2. Holes/open problems; 3. Where current paper falls short; 4. Candidate directions
scored on novelty×confidence; 5. THE ONE PAPER (committed); 6. Headline + exact experiment;
7. Why it lands (feasibility on single-GPU); 8. Supporting results, failure mode + pre-registered
fallback; 9. Novelty defense vs closest prior work; 10. AAAI-27 topic alignment; 11. Shortlist of
5-10 load-bearing papers. Open with a short executive summary (the committed answer first).

## Per-section commitments
- §4 MUST contain a scored table: directions {structured-per-test, scalar, complexity-routing,
  selective-utility} × {novelty 1-5, confidence 1-5}, showing the composed three-tier paper wins.
- §6 headline: per-test AUROC ~0.75-0.85 band (no incumbent), number fixed by pilot; + scalar
  replication vs DCPO; + risk-coverage utility curve.
- §8 MUST state the pre-registered fallback numerically (if per-test AUROC < ~0.70 → report floor
  70-90% coverage @ ≤2-5% err + scalar) and the de-scope ladder.
- §9 MUST use the four-axis wedge AND honestly disclose the UT-Dallas under-review scoop risk +
  Gros&Devanbu; lean on AAAI contemporaneous-work norms.
- §10: primary ML: Bayesian Learning & Uncertainty Quantification; secondary NLP: Code Generation /
  Program Synthesis + ML: Evaluation, Benchmarking, Datasets & Analysis. Method=primary, code=secondary.
- Include a prominent TIMELINE/VENUE callout (AAAI-27 paper due 2026-07-28 ~10 days; pilot-gated
  pivot to ICLR-27). This is decision-critical for the user's "don't waste time/money."

## Where drafts disagreed
- Headline band: unify to ~0.75-0.85, pilot-set. Framing: adopt B's three-tier architecture but
  foreground the structured headline (P1=novelty). Commit to this; don't hedge equally.

## Length target
- response_format: argumentative. Pass 1 ~6500 words; Pass 2 final ~5500-6000 words (cut redundancy
  across the 3 drafts' overlapping frontier/DCPO exposition). This is a PROPOSAL, keep it decisive.
