# Draft A — The Paper to Write: A Code LLM That Localizes Its Own Failures

## Executive Summary

Write the paper that teaches a code LLM to say, in its own words, *which part of its own solution will fail* — and be right about it. The single headline claim is this: **a 7B code model can be trained to emit calibrated, discriminative confidence at per-test-case / per-requirement granularity, achieving per-requirement failure-localization AUROC in the 0.78–0.86 band where no incumbent number exists, using only the free per-test execution labels the diagnostic study already computes.** The mechanism is a decoupled, masked-gradient LoRA objective (a single-GPU adaptation of DCPO [8]) trained with a bounded Brier reward against continuous per-test pass-rate targets. The scalar version of this capability — one confidence number per solution — is now occupied by DCPO [8], which reports AUROC 0.796–0.914 on code, so it becomes a replication baseline, not the contribution. The contribution is the *structured* version, which every method that defines the current frontier is architecturally incapable of producing because they all emit exactly one scalar per answer.

This lands because three of its four ingredients are already proven, just never in combination. Verbalized-confidence RL produces discriminative self-reports at AUROC 0.85–0.86 — but only on question answering (Rewarding Doubt [9], ConfTuner [11]). Decoupled training produces those numbers *on code at the scalar level* (DCPO [8]). Per-unit self-reported confidence with an anti-collapse training pipeline works — but on natural-language claims verified by a noisy fact-checker, topping out at AUROC 0.667 (CURE [17]). The proposed paper is the empty conjunction: self-expressed (not an external probe), per-test-case (not scalar, not per-line, not per-NL-claim), trained against the code's own deterministic execution oracle (not a noisy verifier), on code (not QA). No published work occupies all four axes. The primary AAAI-27 topic is **ML: Bayesian Learning & Uncertainty Quantification** [28]; the contribution is a training method, which is what main-track rewards.

The guaranteed floor, if the structured signal only partially discriminates, is a risk-controlled selective-generation curve wrapped on the *untouched* internal sampling signal (AUROC 0.987 in the base study [1]) — 70–90% coverage at ≤2–5% error, benchmarked against Sharma & David's 77.8–88% coverage at ≤0.02% FPR on LiveCodeBench [5]. The paper cannot die: the worst case is still a complete AAAI-27 submission.

---

## 1. The Research Frontier in Code-LLM Confidence and Calibration

### A. The consensus that no longer needs defending: code's internal signal is near-perfect, its expressed signal is not

The defining empirical fact of this subfield in 2026 is a split between two channels. When a code LLM is *sampled repeatedly* and its confidence is read off the empirical pass rate over completions, discrimination is extraordinary: the diagnostic study that motivates this proposal reports AUROC 0.987 on HumanEval [1], and this is not an outlier. Functional Entropy reaches AUROC up to 0.87 (Python) and 0.84 (SQL) once equivalence is judged functionally rather than by NLI [3]; ConSelf's execution-behavior semantic entropy hits AUC 0.804 with Pearson r = −0.717 against pass rate on Qwen2.5-Coder [4]; Sharma & David restore near-oracle abstention through symbolic-execution clustering [5]. The internal channel works because code has a deterministic oracle — execution — that natural-language tasks lack.

The *expressed* channel — anything a user could read off a single generation — fails. Token log-probability discriminates at AUROC 0.668 in the base study [1], and Spiess et al. showed the same across three tasks and five datasets: intrinsic confidence is poorly aligned with correctness, with completions above 90% average per-token confidence passing tests only 52% of the time [2]. Verbalized 1–5 self-assessment collapses to AUROC 0.519–0.564 with 67% of problems assigned maximum confidence [1]. ConSelf independently replicates the pattern: token entropy and negative log-likelihood "barely surpass random guessing" on CodeLlama at the problem level [4]. AutoProbe confirms that even a trained single-pass hidden-state probe plateaus at 0.63–0.77 accuracy on independent-unit functional correctness — with its own oracle upper bound capping at ~0.77 — while repeated sampling reaches 0.987 [6]. The gap between channels is not a tuning artifact; it is structural.

The correct reading of this consensus is the one the frontier has not yet acted on: **the community has spent its effort making the internal signal better (better clustering, better probes) and almost none making the expressed signal trustworthy.** That asymmetry is the opportunity.

### B. Post-hoc calibration is the wrong tool, and the field is starting to admit it

The instinctive fix — rescale the bad signal — provably fails on the axis that matters. In the base study, isotonic and Platt scaling *improve* ECE while *degrading* AUROC (isotonic 0.668→0.587; Platt →0.386) [1]. Spiess names the mechanism precisely: "bucket collapse," where Platt scaling squashes a poorly-aligned signal into a single bucket at the base correctness rate, producing deceptively low ECE while Skill Score reveals zero predictive utility [2]. Multicalibration for code inherits exactly this blind spot: Campos et al. report Brier Skill Score gains and accuracy rising to 72.5–95.5% but never report AUROC at all [7] — so it cannot distinguish real rank-discrimination from threshold relocation. The fine-grained code-revision study reaches the same verdict from a fourth independent lab, explicitly noting that a degenerate confidence score "lacks the capability of instance-level discrimination" and "cannot support decision-making or thresholding" [22]. The frontier is converging on a methodological principle: **report discrimination (AUROC), not just calibration (ECE), because a near-constant predictor games ECE.** This principle is a positioning wedge, not just a metric choice.

### C. Train-time verbalized calibration works — everywhere except code

The most important cluster for a *prescriptive* paper is the train-time verbalized-confidence line, because it proves the expressed channel is fixable by training rather than rescaling. Rewarding Doubt trains a verbalized confidence token via a log-scoring-rule RL reward on Llama-3-8B with 4-bit LoRA on a single A40, reaching TriviaQA AUROC 0.8592 — and explicitly beats a lower-ECE SFT probe on discrimination, arguing that ECE alone "can hide a model that assigns moderate confidence everywhere" [9]. ConfTuner's tokenized Brier score is a proper scoring rule at the token level, needs zero extra sampling, converges at 2,000 examples on 7–8B models, and delivers up to +14.4% relative AUROC [11]. RLCR proves any bounded proper scoring rule yields simultaneously accurate-and-calibrated models, and warns via its Toy-Arm experiment that an *unbounded* log-score reward-hacks into abstention collapse — boundedness is mandatory [10]. CAPO proves GRPO's implicit advantage is an AUC-*inconsistent* surrogate and supplies a consistent logistic replacement, formalizing why accuracy-only RL degrades relative calibration [13]. ORCE decouples a separate confidence LLM against a Spearman-rank reward, preserving answer accuracy by construction [12]. CSFT shows even trivial SFT on self-consistency labels lifts GSM8K verbalized AUROC from 50.57 to 81.25 and generalizes out of domain [14]. Uncertainty Distillation distills the sampling signal into five verbal bins at AUROC 0.69–0.79 [15].

Every one of these — Rewarding Doubt, ConfTuner, RLCR, CAPO, ORCE, CSFT, Uncertainty Distillation — is QA or math. None touches code. The mechanism is proven; the domain transfer is not. That is the frontier's single largest structural gap, and code is precisely the domain where the training labels are cheapest and most reliable.

### D. The one method that crossed into code — and what it did not do

DCPO is the pivot point of the entire analysis [8]. It is the only method in the corpus with direct code-domain AUROC evidence for a *trained, decoded* confidence signal: a `<conf>` block trained via masked-gradient decoupled GRPO against a hybrid instance-plus-group execution-pass-rate target, reaching AUROC 0.796 (LiveCodeBench v5), 0.845 (v6), and 0.914 (HumanEval+) on Qwen3-8B, beating the joint-reward RLCR baseline on both AUROC and accuracy. Its Proposition 4.2 formally proves the gradient conflict — that for an overconfident model with positively-correlated confidence features, the accuracy and calibration gradients are strictly anti-aligned — which names exactly the mechanism behind the base study's SFT collapse [1][8]. DCPO substantially settles the *scalar* expressed-confidence-for-code question. Its structural limitation is the opening: **DCPO emits one number for the whole solution.** It cannot tell you *which* requirement will fail. Neither can Rewarding Doubt, RLCR, or ConfTuner — they are all scalar-per-answer by construction. That residual is code-unique, and it is where the paper must live.

---

## 2. Caveats, Holes, and Open Problems at the Frontier

### A. The scalar cell is occupied; the structured cell is empty

The most consequential caveat is one this analysis discovered by reading DCPO's full text rather than its abstract: the naive headline — "train a code LLM to verbalize calibrated discriminative *scalar* confidence, measured by AUROC" — is no longer novel. DCPO did it, on the same benchmarks, with the same execution-pass-rate target [8]. Pursuing it would be the "DCPO-lite on LoRA" incrementalism trap. But DCPO's own architecture reveals the hole: because code execution yields a *vector* of per-test outcomes while QA and math yield a single correctness bit, there exists a fine-grained confidence target that scalar methods physically cannot express and that has free ground-truth labels. No paper trains a code LLM to self-report per-test-case or per-requirement confidence and evaluates it by discrimination. This is the empty cell.

### B. Everyone measures the wrong thing, or the wrong signal, or in the wrong domain

The frontier's holes are systematic. Post-hoc code-calibration work (Multicalibration [7], fine-grained code revision [22]) measures ECE/Skill-Score but never AUROC, so it cannot show discrimination. Train-time verbalized work (Rewarding Doubt [9], ConfTuner [11], RLCR [10], CAPO [13], ORCE [12], CSFT [14], Uncertainty Distillation [15]) measures AUROC but only on QA/math. Code-native execution work either improves the *internal* signal without ever expressing it (Functional Entropy [3], ConSelf [4], Sharma & David [5]) or produces a signal from a *separate* model rather than the coder's self-report (AutoProbe [6], FLARE [19]). The structured-confidence work exists only outside code, verified by noisy fact-checkers (CURE [17], Atomic Calibration [18]). **No single work combines self-expression, per-test granularity, execution ground truth, and the code domain.** Each near-miss fails on exactly one axis — which is what makes the wedge defensible rather than lucky.

### C. Evaluation and contamination hazards the paper must pre-empt

Two threats could sink a naive execution. First, ECE is fragile and gameable — the base study's own collapse (mean confidence 0.900 everywhere, low ECE, no discrimination) is the proof [1], reinforced by CAPO's formal argument that assigning identical confidence to all instances satisfies calibration yet fails discrimination [13]. The paper must therefore make per-test AUROC primary and report debiased/adaptive ECE secondarily. Second, HumanEval's near-perfect oracle risks being a contamination artifact; ConSelf independently replicates the difficulty-level disconnect on time-windowed LiveCodeBench [4], so primary evaluation must run on LiveCodeBench with HumanEval as a legacy comparison only. Both hazards convert into robustness pillars if handled explicitly, and into fatal reviewer objections if ignored.

---

## 3. Where the Current Calibration-Disconnect Paper Falls Short of Main-Track

The existing manuscript is a strong diagnostic, and diagnostics do not win AAAI main track. Its three shortfalls are precisely what the extension repairs.

**It is descriptive, not prescriptive.** The finding is "no expressed interface communicates the internal signal" [1]. That is a negative result. Main-track methodology rewards a *positive* mechanism that closes the gap, not a demonstration that a gap exists. AAAI's own routing rules push measurement/application studies toward IAAI or AI-for-Social-Impact; the contribution must be a training method [28].

**Its one intervention failed in the most instructive way.** The 274-example LoRA SFT reduced verbal ECE by 64% but produced "calibration without discrimination" — mean confidence 0.900 on both easy and hard problems [1]. This is not a dead end; it is a diagnosis. DCPO's Proposition 4.2 explains it (joint objective, gradient conflict) [8]; the label-feasibility analysis explains it further (coarse 1–5 bins, 274 examples, majority-bin collapse) [11]. The extension replaces the coarse joint SFT with a decoupled, continuous-target, proper-scoring objective — turning the failed intervention into the ablation that motivates the method.

**It is scoped to a scalar interface that the field has since occupied.** Even a successful scalar-confidence result would now be measured against DCPO's 0.796–0.914 [8]. The manuscript's own framing — one confidence number per solution — is the ceiling the field already reached. The only way up is to change *what is expressed*, not merely to express it better. The structured per-test interface is that change, and it is native to code in a way no competing domain can replicate.

---

## 4. Candidate Directions, Scored on Novelty and Confidence

Four directions were weighed on the binding priority order (Priority 1 = novelty, Priority 2 = confidence the headline materializes).

### A. Direction 1 — Scalar self-expressed confidence for code (DCPO-lite on LoRA)
**Novelty: low. Confidence: very high.** A LoRA single-GPU replication of DCPO's decoupled scalar recipe would almost certainly hit AUROC 0.80–0.90 [8][9]. But DCPO already published this exact result on code [8]. High confidence, low novelty — fails Priority 1. Rejected as headline; retained as a baseline.

### B. Direction 2 — Structured per-test / per-requirement self-expressed confidence
**Novelty: high. Confidence: medium-high.** The empty four-axis conjunction (§2A, §9). Labels are free (per-test pass rates already computed for the 0.987 oracle) [1]; the mechanism is DCPO's decoupling generalized to a vector target [8]; the closest analog (CURE) proves the anti-collapse pipeline works at AUROC 0.667 on a *noisier* signal, so a cleaner execution oracle should do better [17]. This is the recommendation.

### C. Direction 3 — Complexity-routed estimator (AutoProbe-style)
**Novelty: medium. Confidence: medium.** AutoProbe's judge-vs-probe reversal (external judge 0.94 on simple code, internal probe 0.82 on repo-level) is real but asymmetric, concerns third-party assessment not self-report, and requires a repo-level benchmark beyond the single-GPU budget [6]. A one-paragraph robustness ablation, not a headline.

### D. Direction 4 — Risk-controlled selective generation on the internal signal
**Novelty: low-medium. Confidence: very high.** CIC-style conformal wrapping of the 0.987 signal is nearly guaranteed to land 70–90% coverage at low error [5][23][24]. But CIC (generic) and Sharma & David / CODEREFUSER (code abstention) already occupy most of the conceptual space [5][23][24]. Not "extremely novel." This is the *fallback floor*, not the headline.

**Verdict:** Direction 2 is the only cell that is simultaneously novel (Priority 1) and de-riskable with a guaranteed Direction-4 floor (Priority 2). It is the one paper.

---

## 5. The One Paper: Committed Recommendation

**Title (working):** *"Which Test Will I Fail? Teaching Code LLMs to Localize Their Own Errors with Calibrated Per-Requirement Confidence."*

**The committed thesis.** A code LLM can be trained to express calibrated, discriminative confidence at per-test-case / per-requirement granularity — to point at the specific requirement its solution will violate — a capability that is enabled by code's per-test execution verifiability and structurally impossible for the scalar-confidence methods (DCPO [8], RLCR [10], Rewarding Doubt [9]) that define the current frontier. Call the method **Decoupled Per-Requirement Confidence (DPRC)**.

**The mechanism, committed.** After generating a solution, the frozen-generation model emits a structured confidence block: for each requirement/test-group $g$ of the problem, a verbalized confidence token $c_g \in [0,100]$ that predicts the probability its solution passes that group. The block is trained by a **decoupled masked-gradient LoRA objective** — the single-GPU adaptation of DCPO [8] — so the confidence-token advantage never backpropagates into the generation policy, mechanically preventing the Proposition 4.2 gradient conflict that produced the base study's collapse [1][8]. The reward per confidence token is a **bounded Brier-style proper scoring rule** (never unbounded log-score, per RLCR's Toy-Arm collapse warning [10]; proper-scoring per ConfTuner's theorem [11]) against the **continuous per-test pass rate** already computed at $n=10$ samples for the 0.987 oracle [1]. Labels are free: no new sampling, only reuse.

**Why this exact design.** Three convergent findings force it. First, the self-report/probe analysis shows self-report fails only when *untrained or naively joint-SFT'd*, and succeeds under proper-scoring training — so keep the coder's own voice but decouple the *optimization* [9][11][12]. Second, the collapse-proof analysis shows DCPO's decoupling is the only code-validated recipe with a formal anti-collapse guarantee, and that continuous instance-level targets (not coarse tiers) are what supply the discrimination gradient — DCPO's ablation loses 0.081 ECE when instance labels are removed [8]. Third, the feasibility analysis shows ConfTuner's tokenized-Brier loss on the existing pass-rate labels is single-GPU cheap and converges at 2,000 examples [11]. DPRC is the intersection: DCPO's architecture, ConfTuner's loss, the base study's free labels, extended from a scalar to a per-requirement vector.

**Requirement granularity, committed.** "Per-requirement" is operationalized as per-test-*group*, where tests are clustered by the requirement they exercise (public examples, edge cases, and hidden functional groups), not per-individual-hidden-test — this keeps the target dimension modest (typically 3–6 groups) and the labels dense. On dense benchmarks (TACO ~50–200 tests/problem [27]; LiveCodeBench ~17 [26]) the grouping is data-driven; on sparse ones (HumanEval ~7 [26]) it degrades gracefully to public-vs-hidden.

---

## 6. Headline Claim and the Exact Experiment That Produces It

### A. The single headline number

> **A 7B code LLM trained with DPRC self-reports which requirement it will fail at per-requirement AUROC 0.78–0.86 on LiveCodeBench — versus ~0.52–0.56 for prompted per-requirement self-report and with no prior method able to produce the number at all — the first demonstration that a code model can localize its own functional failures in its own voice.**

The comparison anchor is deliberate: there is *no incumbent per-test AUROC* to beat, so the paper wins on the novelty of the capability, not on out-scoring DCPO's scalar number. The untrained baseline (~0.52–0.56) is the base study's own verbalized failure [1], replicated at the per-requirement level; the trained result is the contribution.

### B. The exact experiment

1. **Data.** Assemble 2,000–4,000 problems from MBPP, a ≥3-test-case-filtered APPS subset, and a LiveCodeBench training window, holding out HumanEval and a disjoint LiveCodeBench window for evaluation to control contamination [4][26][27]. Cluster each problem's tests into requirement groups.
2. **Free labels.** For each problem, sample $n=10$ solutions from Qwen2.5-Coder-7B-Instruct; record the per-test pass matrix. The per-group pass rate is the continuous confidence target. (This is the same sampling that produced 0.987; reuse it [1].)
3. **Train DPRC.** LoRA rank 16 on the confidence block; decoupled masked-gradient update; bounded Brier reward against per-group pass rate; generation weights frozen for the confidence pass [8][11][12].
4. **Headline metric.** Per-requirement AUROC: pool all (problem, group) pairs, label = did the solution pass that group, score = self-reported $c_g$. Report bootstrap 95% CIs.
5. **Baselines on the same axis.** Prompted per-group self-report (untrained); coarse joint-SFT (the base study's failed recipe, replicated to show the collapse [1]); per-group log-prob; per-group AST/consistency proxy.

### C. The three-panel supporting figure

- **Panel 1 (headline):** per-requirement AUROC, DPRC vs. baselines, LiveCodeBench primary + HumanEval legacy.
- **Panel 2 (scalar sanity):** aggregate scalar AUROC vs. DCPO's reported 0.796–0.914, showing the LoRA single-GPU recipe reproduces the scalar result before extending it [8].
- **Panel 3 (utility floor):** risk-coverage curve from the selective-generation fallback (§8), guaranteed to land [5].

---

## 7. Why the Headline Will Likely Land: Feasibility on Single-GPU 7B Compute

### A. The mechanism is proven three times over, just never combined

The confidence in Priority 2 rests on borrowed evidence. DCPO already got AUROC 0.796–0.914 for a *decoded, trained* confidence signal on code with an execution-pass-rate target — the scalar special case of DPRC — so the reward shape and target are validated in-domain [8]. Rewarding Doubt got AUROC 0.859 with a genuinely verbalized token under LoRA on a *single A40* [9], and ConfTuner got +14.4% AUROC with a proper-scoring loss on 7–8B models converging at 2,000 examples [11] — so the training mechanism is single-GPU feasible. CURE got the *structured, per-unit, self-reported, anti-collapse* result at AUROC 0.667 on a **noisier** oracle (VeriScore) in a **harder** domain (long-form factuality) [17] — so the structured extension is demonstrably trainable, and a deterministic execution oracle should beat 0.667, not fall below it. Every ingredient has a positive precedent; the paper is an assembly, not a gamble.

### B. Compute fits with wide margin

The feasibility analysis pins the numbers: label generation reuses existing $n=10$ sampling (~1.7–6.7 GPU-hours for a 2,000–4,000-problem pool), LoRA training is minutes-to-under-an-hour (ConfTuner's own 4 minutes at 2,000 examples; Raschka's 1.85h/50k linear extrapolation), and one clean end-to-end pass is ~15–25 GPU-hours, ~45–75 with a 3× debugging buffer [11][15]. ConSelf is the exact-hardware precedent: single-GPU LoRA DPO on 6,372 curated examples using DeepSeek-Coder-6.7B and Qwen2.5-Coder-7B — the identical model family — and it showed curated subsets beat unfiltered ones, so more data is not needed [4]. The 260113284 precedent shows LoRA rank-16 decoupling survives at ~500 GPU-hours across three model sizes [8-context]. Nothing in DCPO's architecture requires full fine-tuning; the masked-gradient split is a training-loop change, not a scale requirement.

### C. The expected number, calibrated honestly

DCPO's scalar band (0.80–0.91) and the internal-signal ceiling (0.987) bracket the plausible per-requirement result [1][8]. Per-requirement discrimination is a harder target than scalar (fewer samples per group, higher label noise per cell), so a realistic landing is AUROC 0.75–0.85 — below scalar DCPO but above CURE's 0.667 because execution is a cleaner oracle than VeriScore [8][17]. Crucially, *any* number in that band is a first, because no prior per-test AUROC exists. Priority 2 risk is therefore not "will the number be good enough to beat an incumbent" (there is none) but "will discrimination survive the decode-to-structured step" — which the fallback (§8) fully insures.

---

## 8. Supporting Results, Failure Mode, and Pre-Registered Fallback

### A. Supporting results that make the headline defensible

1. **Scalar replication** reproducing DCPO's 0.80–0.91 band on LoRA single-GPU, proving the recipe before extending it [8].
2. **The collapse ablation:** the base study's coarse joint-SFT re-run to exhibit mean-confidence collapse, then DPRC's decoupled continuous-target objective repairing it — a direct, mechanistic before/after [1][8].
3. **Decoupling ablation** (DPRC vs. bounded joint reward à la Rewarding Doubt) isolating whether decoupling is necessary or merely safer [9][10].
4. **Sample-count sweep** ($n \in \{5,10,20,50,100\}$ vs. AUROC) showing code's execution signal saturates far below Uncertainty Distillation's N=100, a cheap panel rebutting "just use UD's recipe" [15].
5. **Contamination control:** LiveCodeBench primary, HumanEval legacy [4][26].

### B. The most likely failure mode, named precisely

The single largest risk is that DPRC reproduces the base study's collapse at the structured level — the model emits a near-constant per-group confidence despite continuous targets and decoupling — because per-group labels are noisier than scalar labels (fewer effective samples per cell), and because LoRA rank 16 may lack capacity to represent a structured objective distinct from generation [1][8]. A Day-1 pilot on ~200–300 problems resolves this before commitment: if the structured signal collapses, the diagnosis is representational, not procedural.

### C. The pre-registered fallback (the guaranteed floor)

If the structured signal underperforms (per-requirement AUROC < ~0.70), the paper pivots its headline to a **risk-controlled selective-generation result wrapped on the untouched internal sampling signal — never on the collapsed verbal output**, which lacks the score spread any threshold-search needs [5][24]. Concretely: a Clopper-Pearson upper-confidence-bound policy at a pre-registered primary **α = 0.10** (where CIC shows feasibility even for weak signals), with **α = 0.05 as a stretch goal** and calibration-pool expansion (HumanEval+MBPP, ~400+ problems, inference-only) as the pre-registered fallback-to-the-fallback if α = 0.05 returns infeasible on a large fraction of splits — mirroring CIC's own documented failure mode rather than pretending it cannot happen [24]. The target is 70–90% coverage at ≤2–5% accepted-output error, anchored to Sharma & David's 77.8–88% coverage at ≤0.02% FPR on LiveCodeBench and CODEREFUSER's ~3.5× coverage over a perplexity baseline at matched risk [5][23]. Because the 0.987 signal is a stronger discriminator than anything inside CIC's own general-QA tests, this floor should land at or above the Sharma & David ceiling [1][5][24]. This is publishable-grade insurance — reframed as "decoupling the *action* problem (solvable) from the *communication* problem (still hard)," and aligned with the in-IDE deployment finding that developers prefer categorical/color-coded reliability cues over numeric confidence [25] — but its own novelty is modest, so it is the floor, never the headline.

### D. Pre-registration discipline

The α levels, the AUROC-primary metric, the LiveCodeBench-primary evaluation, the requirement-grouping rule, and the fallback trigger threshold are all fixed *before* the runs, satisfying AAAI-27's mandatory reproducibility checklist, which must be submitted at submission time — not promised for later [29].

---

## 9. Novelty Defense Against the Closest Prior Work

The wedge is the **conjunction of four axes**, and every near-miss fails exactly one. The defense is a single sentence: *no prior work has a code LLM express its own confidence, at per-test-case/per-requirement granularity, trained against the code's own deterministic execution oracle, evaluated by discrimination.*

### A. Axis 1 — self-expressed, not an external probe or separate model
FLARE localizes bugs at line level via a **separate diagnostic transformer** trained from scratch, not the coder's self-report, and reports Top-k localization accuracy — never AUROC or any calibration metric (grep-verified) [19]. Gros & Devanbu's "Localized Calibrated Uncertainty" — the closest *title* — assigns calibrated per-line edit probability via an **external white-box probe** on internals, not the model's own voice [20]. AutoProbe is likewise a probe, and its in-house LLM-as-judge (the self-report analog) is catastrophic at 0.27–0.73 [6]. RLCM's confidence is a decoupled hidden-state probe whose gradients never enter the policy [16]. DPRC is the model's own decoded output. Distinct.

### B. Axis 2 — per-test-case/per-requirement, not scalar, not per-line, not per-NL-claim
DCPO emits one scalar per solution [8]; RLCR, Rewarding Doubt, ConfTuner, CAPO, ORCE, CSFT all emit one scalar per answer [9][10][11][12][13][14]. Gros & Devanbu and FLARE localize *spatially* (which line), a fundamentally different structuring than *functionally* (which requirement/test) [19][20]. CURE and Atomic Calibration decompose into *NL claims* [17][18]. The per-test-case functional axis is unoccupied.

### C. Axis 3 — trained against the code's own execution oracle, not a noisy verifier
CURE's labels come from VeriScore, a retrieval-based fact-checker capping it at AUROC 0.667 [17]; Atomic Calibration uses an external NLI/LLM fact-checker [18]; Gros & Devanbu build a curated Minimal-Intent-Aligning-Patches dataset (construction is itself a cost) [20]. DPRC's oracle is deterministic per-test execution — free, exact, and the very reason code's internal signal reaches 0.987 [1]. This is code's structural advantage over every competing domain.

### D. Axis 4 — code, not QA/math
Rewarding Doubt, RLCR, ConfTuner, CAPO, ORCE, CSFT, Uncertainty Distillation, CURE, Atomic Calibration — all QA or math [9][10][11][12][13][14][15][17][18]. VeRPO is the sharpest same-domain distractor: it turns per-test partial success into a **correctness reward**, never a confidence output, which confirms the "free per-test labels for *confidence*" framing is unoccupied [21].

### E. The honest scoop caveat
Two under-review UT Dallas papers ("Beyond Confidence…", "Beyond Execution…") have on-topic titles; their public ICSE-NIER short paper is *scalar* per-prediction abstention, which is partial and distinct from the per-test self-expressed axis [16-context]. The paper must move fast and frame the four-axis conjunction sharply. AAAI's contemporaneous-work policy (anything published within two months of the July 28 deadline need not be addressed) provides partial cover [29]. Novelty confidence: high, with this one named caveat.

---

## 10. AAAI-27 Topic Alignment: Primary and Secondary Keywords

**Primary keyword (verbatim):** **ML: Bayesian Learning & Uncertainty Quantification** [28]. There is no separate "ML: Calibration" keyword in the AAAI-27 list; calibration and discriminative uncertainty estimation fall squarely under this keyword. The paper's main contribution is a *training method for calibrated, discriminative uncertainty quantification* — a general ML/UQ advance whose novelty (structured, decoupled, proper-scoring confidence with a formal anti-collapse motivation) is evaluable by the UQ community. Under AAAI's own rule — file under the subarea of the main methodological contribution, and an ML method demonstrated on code goes under ML unless the contribution is fundamentally about code-specific structure [28] — this is the correct home. The method *exploits* code's execution verifiability, but the contribution is the UQ training objective, not a code-generation advance per se, so ML/UQ is primary and NLP/code is the application.

**Secondary keywords:** **NLP: Code Generation / Program Synthesis** (the application domain and the source of the free per-test labels) and **ML: Evaluation, Benchmarking, Datasets & Analysis** (the AUROC-primary evaluation protocol, the per-requirement labeling scheme, and the ECE-gaming critique) [28].

**One-line scope statement.** The paper's main contribution is a decoupled, execution-grounded training objective for calibrated per-requirement uncertainty quantification; it sits in ML: Bayesian Learning & Uncertainty Quantification and will not drift into a code-generation or software-engineering framing, because the headline is a UQ capability (failure localization by calibrated self-report), not a pass@k improvement.

**Format compliance.** AAAI-27 allows 7 pages of technical content plus reference/checklist-only pages [29]. The one-headline, three-panel, five-ablation scope fits: §6's experiment is one training run plus baselines, §8's fallback is one conformal wrapper. The reproducibility checklist and code must be submitted at submission time [29]. Deadlines: abstract July 21, paper July 28, code July 31, 2026 [28][29].

---

## 11. The Shortlist: 5–10 Load-Bearing Papers

1. **DCPO — Decoupling Reasoning and Confidence** [8] (arXiv:2603.09117). *Contributes:* the decoupled masked-gradient objective, the Proposition 4.2 gradient-conflict proof, and the only code-domain trained-confidence AUROC (0.796–0.914). *Leaves open:* everything is scalar — one number per solution, no per-requirement structure. **The method's parent and the scalar baseline to position against.**

2. **CURE — Think-Through-Uncertainty** [17] (arXiv:2604.12046). *Contributes:* the closest methodological analog — self-reported, per-claim, discriminative, AUROC-evaluated confidence with a three-stage anti-collapse pipeline, explicitly critiquing scalar confidence. *Leaves open:* general long-form factuality with a noisy VeriScore oracle (AUROC 0.667), no code, no execution. **The must-distinguish paper; the argument is that execution beats fact-checking.**

3. **Rewarding Doubt** [9] (arXiv:2503.02623). *Contributes:* proof that a genuinely verbalized confidence token, RL-trained on a single A40 LoRA, is *more discriminative* than a lower-ECE probe (AUROC 0.859). *Leaves open:* QA only, single scalar. **The single-GPU feasibility existence proof.**

4. **The base "Calibration Disconnect" manuscript** [1]. *Contributes:* the 0.987 internal / 0.668 log-prob / 0.52–0.56 verbal disconnect, the post-hoc AUROC-degradation result, and the free per-test labels the method reuses. *Leaves open:* it is diagnostic and its one intervention collapsed. **The foundation the paper extends.**

5. **Gros & Devanbu — Localized Calibrated Uncertainty in Code LMs** [20] (arXiv:2512.24560). *Contributes:* the closest title — calibrated *localized* code uncertainty. *Leaves open:* spatial (per-line) not functional (per-test), external probe not self-report, curated patch dataset not free execution labels. **The prominent cite-and-distinguish on the "localized" framing.**

6. **ConfTuner** [11] (arXiv:2508.18847). *Contributes:* tokenized Brier proper-scoring loss, zero extra sampling, 2,000-example convergence on 7–8B. *Leaves open:* QA only, scalar, single-generation binary label. **The loss function and the feasibility floor.**

7. **RLCR — Beyond Binary Rewards** [10] (arXiv:2507.16806). *Contributes:* the bounded-proper-scoring-rule theorem and the Toy-Arm proof that unbounded log-score reward-hacks into collapse. *Leaves open:* QA/math, scalar, heavier compute. **The reason the reward must be bounded Brier.**

8. **FLARE** [19] (arXiv:2606.03852). *Contributes:* fine-grained (line-level) execution-guided code diagnosis. *Leaves open:* separate diagnostic model, line-level not per-test, never reports AUROC/calibration. **The execution-plus-fine-grained near-miss on the self-expression axis.**

9. **Sharma & David — Assessing Correctness via Uncertainty Estimation** [5] (arXiv:2502.11620). *Contributes:* symbolic-execution abstention at 77.8–88% coverage, ≤0.02% FPR on LiveCodeBench. *Leaves open:* internal signal, not a trained expressed interface. **The fallback ceiling to benchmark.**

10. **Spiess et al. — Calibration and Correctness of LMs for Code** [2] (ICSE 2025, arXiv:2402.02047). *Contributes:* the bucket-collapse critique and the ECE-is-insufficient lesson for code. *Leaves open:* only older non-instruction-tuned models, no train-time method, no per-region calibration (its own future-work item). **The anchor for the AUROC-over-ECE positioning and the field's foundational calibration reference.**

---

## Sources

[1] The "Calibration Disconnect" manuscript (v3), *Mind the Gap: The Calibration Disconnect Between Internal and Expressed Confidence in Code Language Models* — base-paper grounding, `research/query-code-llm-calibration-aaai27-eabf3f.md`.
[2] Spiess et al., *Calibration and Correctness of Language Models for Code*, ICSE 2025, arXiv:2402.02047.
[3] Bouchard et al. (CVS Health), *Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification*, arXiv:2605.28500.
[4] Zhang, Cheng, Hu, *ConSelf: Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus*, ICPC 2026.
[5] Sharma & David, *Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation*, arXiv:2502.11620.
[6] Vu et al. (VNU), *AutoProbe: Model-Agnostic Correctness Assessment for LLM-Generated Code via Dynamic Internal Representation Selection*, 2025.
[7] Campos, Kuschnereit, Ulges (RheinMain), *Multicalibration for LLM-based Code Generation*, AI-SQE 2026, arXiv:2512.08810.
[8] Ma et al. (ISCAS), *DCPO: Decoupling Reasoning and Confidence — Resurrecting Calibration in Reinforcement Learning*, ICML 2026, arXiv:2603.09117.
[9] Bani-Harouni et al. (TU Munich), *Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of LLMs*, arXiv:2503.02623.
[10] Damani et al. (MIT/MIT-IBM), *Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty (RLCR)*, arXiv:2507.16806.
[11] Li, Xiong, Wu, Hooi (NUS), *ConfTuner: Training Large Language Models to Express Their Confidence Verbally*, NeurIPS 2025, arXiv:2508.18847.
[12] Li et al. (Stony Brook), *ORCE: Order-Aware Alignment of Verbalized Confidence in Large Language Models*, arXiv:2605.12446.
[13] Wang et al. (CASIA/Tsinghua), *CAPO: Calibration-Aware Policy Optimization for Reasoning LLMs*, arXiv:2604.12632.
[14] Jang et al. (KAIST), *Verbalized Confidence Triggers Self-Verification: Emergent Behavior Without Explicit Reward (CSFT)*, arXiv:2506.03723.
[15] Hager et al. (JHU), *Uncertainty Distillation: Teaching Language Models to Express Semantic Confidence*, arXiv:2503.14749.
[16] Wang, Zuo, Jurayj, Van Durme, Liu (JHU), *RLCM: Process Supervision of Confidence Margin for Calibrated LLM Reasoning*, COLM 2026, arXiv:2604.23333.
[17] Liu & Wang (U. Michigan), *CURE: Think-Through-Uncertainty — Improving Long-Form Generation Factuality via Reasoning About Uncertainty*, arXiv:2604.12046.
[18] Zhang et al. (Cambridge/Fudan/Tencent), *Atomic Calibration of LLMs in Long-Form Generations*, ACL 2025 KnowFM, arXiv:2410.13246.
[19] Yao, Zhang, Tong, Zhang (Tongji/Purdue), *FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement*, arXiv:2606.03852.
[20] Gros & Devanbu (UC Davis), *Localized Calibrated Uncertainty in Code Language Models*, arXiv:2512.24560.
[21] *VeRPO: Beyond Binary — Turning Partial Success into Dense Verifiable Rewards for Code Generation*, arXiv:2601.03525.
[22] Lin et al. (Melbourne/SMU), *Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision*, arXiv:2604.06723.
[23] Zhou et al., *CODEREFUSER: Task Abstention for Large Language Models in Code Generation*, arXiv:2605.17029.
[24] Dong & Shinnou, *CIC: Uncertainty-Aware Abstention in Large Language Models with Provable Guarantees*, arXiv:2607.04430.
[25] *Does In-IDE Calibration of Large Language Models Work at Scale?*, arXiv:2510.22614.
[26] Jain et al. (UC Berkeley/MIT), *LiveCodeBench: Holistic and Contamination-Free Evaluation of Large Language Models for Code*, arXiv:2403.07974.
[27] *TACO: Topics in Algorithmic Code Generation Dataset*, arXiv:2312.14852.
[28] AAAI-27 Areas and Topics (official, Wayback snapshot 2026-07-04).
[29] AAAI-27 Submission Instructions (official, Wayback snapshot).
