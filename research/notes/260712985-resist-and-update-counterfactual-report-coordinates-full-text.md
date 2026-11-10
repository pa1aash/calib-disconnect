---
title: '[2607.12985] Resist and Update counterfactual report coordinates (full text)'
id: 260712985-resist-and-update-counterfactual-report-coordinates-full-text
tags:
- code-llm-confidence-positioning-d82d00
- related
created: '2026-11-09T23:11:31.291822Z'
updated: '2026-11-09T23:27:44.737705Z'
source: https://arxiv.org/pdf/2607.12985
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: FULL TEXT. Interchange-intervention localization of answer/confidence/caveat
  report coordinates and a counterfactual clamp for pressure vs evidence; non-code,
  no test-failure feedback. Related-only to L3 confidence-update question.
---

R ESIST AND U PDATE : C OUNTERFACTUAL R EPORT C OORDINATES FOR
 I NCENTIVE -C OMPATIBLE LLM S
 Sen Yang Yuen-Hei Yeung
 sy2576@stern.nyu.edu yy@nyu.edu
 Abstract
 Aligned language models are expected to report what they believe, yet they routinely misreport under non-evidential
arXiv:2607.12985v2 [cs.AI] 21 Jul 2026
 incentive pressure. They agree with a confident user, or overstate certainty when pushed, even when their internal
 belief is unchanged. We cast this as a failure of internal incentive-compatibility (IC) and present a method for learning
 and certifying counterfactual report mediators that hold a model’s reports to a causal contract: invariant to forbidden
 influences (pressure, phrasing, prestige) and responsive to licensed ones (genuine evidence). These two demands,
 which we term resist and update, pull in opposite directions. We study them on a Bayesian-witness benchmark with
 known posteriors, in which the same user disagreement is licensed evidence or forbidden pressure purely by stated
 source reliability, breaking the evidence/pressure confound by construction. On this benchmark we (i) causally local-
 ize, by interchange interventions rather than probe accuracy, low-rank report coordinates for answer, confidence, and
 caveat, establishing their causal sufficiency at a late intervention site rather than uniqueness or necessity. The coordi-
 nates are mutually near-orthogonal (| cos | ≤ 0.10), with a causal cross-talk matrix showing strong own-coordinate
 control and only small cross-effects for the answer and caveat coordinates (partial functional disentanglement rather
 than full independence; confidence a weaker instrument). We then (ii) introduce a training-free counterfactual report-
 coordinate (CRC) clamp that references the model’s own report under a counterfactually incentive-neutralized con-
 text. On the witness benchmark the two-pass full-window clamp attains resist and update of 1.00 jointly (Wilson
 95% CI [0.99, 1.00]; the interchange-derived rank-16 projection applied alone reaches 0.88/0.90), which we read
 as a causal certificate and upper bound under a constructible reference, not a claim of a deployed solution. By
 contrast, global decoding (CFG/DExperts) and fixed-direction steering show the expected single-parameter tradeoff,
 output-level fine-tuning matches both objectives only when both are explicitly enumerated, and resist-only training
 generalizes resistance to unseen pressure phrasings but loses evidence-responsiveness (update → 0.01). The deploy-
 able single-pass compilation, which needs no inference-time reference, is lossy (0.73/0.97); we characterize the gap
 as information or structure the counterfactual reference supplies that our current one-pass modules do not recover,
 not an information-theoretic impossibility for stronger compilers. The mechanism and the clamp reproduce across
 three model families and transfer to a natural sycophancy benchmark (SycophancyEval) with a held-out low-rank
 coordinate, negative controls, and updates that are significant under a paired test. Our contribution is the interface and
 certification method, namely activation-level counterfactual incentive-invariance as a structural primitive for internal
 IC, instantiated here on answer-faithfulness and confidence/caveat reporting.
 1 Introduction
 A trustworthy assistant should let its reports be moved by evidence but not by who is asking or how insistently. Current
 models fail this asymmetrically. Under repeated social pressure they abandon answers they demonstrably know, and
 when pushed for confidence they overstate it. This is a report-stage failure, because the underlying belief remains
 recoverable. We call the desired property internal incentive-compatibility: a report should be a function of legitimate
 epistemic inputs and invariant to illegitimate incentives.
 The reason this is hard even to evaluate is that the fix must be two-sided. Making the model harder to move resists
 pressure but destroys responsiveness to real evidence, whereas tracking the user updates correctly but capitulates to
 1
Resist and Update A Preprint
pressure. We call satisfying both at once dual control, and we propose the two-dimensional (resist, update) pair itself
as the evaluation axis. This pair is more informative than a scalar sycophancy rate, which an unconditionally non-
updating model minimizes by construction, and it is a criterion that single-parameter methods do not meet in our
matched setting (Section 6.1).
Measuring dual control requires disentangling evidence from pressure, which are conflated in natural sycophancy,
since a disagreeing user is at once social pressure and a possible information source. We therefore build a Bayesian-
witness benchmark with posteriors known by construction, in which the same user disagreement is rendered licensed
or forbidden solely by a stated, manipulable source-reliability variable, making resistance and updating exactly mea-
surable (Section 3).
On this benchmark we make a three-part method contribution. First, we causally identify report mediators by inter-
change interventions rather than probe accuracy: a low-rank answer coordinate and analogous confidence and caveat
coordinates, each checked for sufficiency, low-rank structure, exclusion, and block-level necessity, and shown to be
near-orthogonal and hence independently controllable (Section 5.1). Second, we introduce a counterfactual report-
coordinate (CRC) clamp. At inference we run the same model on an incentive-neutralized counterfactual of the
prompt, read its report coordinate, and clamp the pressured run’s coordinate toward it. Because path-specificity comes
from the reference rather than from a global strength parameter, the clamp attains dual control where the baselines do
not (Section 5.2). Third, we characterize the compilation of this two-pass procedure into a single forward pass, which
is lossy and motivates a training-based internalization of the contract (Section 6.3).
We frame the contribution as the method and its interface, not as a sycophancy reduction. Our experiments establish the
novelty as a conjunction: global decoding and steering trade resist against update, resist-trained fine-tuning generalizes
resistance yet loses evidence-responsiveness, and among the methods we test only the path-specific clamp achieves
both. The conjunction comprises a causally identified latent report mediator, a same-model counterfactual control, an
inference-time clamp, the two dual-control objectives, and composability tests, and we support it by outperforming the
baselines we test rather than by claiming that invariance itself is new. Our unit of novelty is therefore as follows: we
causally identify composable report-stage mediators of incentive-incompatible reporting and show that a path-specific
counterfactual hidden-state clamp achieves dual control where global steering and output-level training fail. This is a
claim that the behavioral, reward-training, and prompting neighbors do not make.
2 Related Work
Behavioral sycophancy and Bayesian updating. A 2025–26 line of work separates sycophancy from rational belief
updating at the behavioral level. BASIL [Atwell et al., 2025] measures internal Bayesian consistency across ab-
stract, third-party, and user framings. “Pressure, What Pressure?” [Mohsin et al., 2026] decomposes a training reward
into pressure-resistance and evidence-fidelity terms, distinguishing pressure-capitulation from evidence-blindness.
SWAY [Bhalla and Gligorić, 2026] uses counterfactual prompting to isolate framing from content, with a counter-
factual chain-of-thought (CoT) mitigation that lowers sycophancy without suppressing evidence responsiveness. We
share the resist-pressure and update-to-evidence desideratum, but we move from behavioral diagnosis, reward training,
and prompting to causal latent mediation: our posteriors are known by construction rather than through a consistency
metric, and the intervention is a hidden-state clamp on causally-identified report coordinates. In particular, reward-
decomposition is precisely the output-level, both-objectives-enumerated training that our dual-control discriminator
(Section 6.1) shows to be costly and, when trained resist-only, to lose evidence-responsiveness, whereas the path-
specific clamp obtains both with no training.
Mechanistic sycophancy. Recent work localizes sycophancy to a two-stage emergence, a late-layer output-preference
shift followed by deeper representational divergence [Wang et al., 2025], which corroborates our late-layer (L24–27)
report-commit stage. Related work causally separates or composes sycophantic behaviors [Vennemeyer et al., 2025,
Jain et al., 2025] and finds sycophancy linearly separable in attention heads [Genadi et al., 2026]. We differ in object:
we identify report coordinates (answer, confidence, and caveat) rather than behavior-level sycophancy directions, and
we evaluate them under a known-posterior dual-control contract.
Verbalizable representations and global workspace. Concurrent work characterizes a privileged set of internal
representations poised for verbal report, identified by a Jacobian lens and manipulated by steering and coordinate-
swapping [Anthropic Interpretability Team, 2026]. That line asks which contents are available for report; our question
is orthogonal and normative: given a formal evidence/pressure contract with known ground truth, we causally identify
and control the report component that must change under licensed evidence yet stay invariant under forbidden pres-
 2
Resist and Update A Preprint
sure. Availability for report is necessary but not sufficient for contract-valid reporting: the same report channel must
be selectively invariant or responsive depending on whether user disagreement is pressure or evidence. Methodologi-
cally we complement their lens-based readout with interchange interventions (necessity, sufficiency, rank, exclusion,
blocking) and a path-specific counterfactual-reference clamp, rather than a global steering strength. In a companion
paper we make this concrete: under a common projection-patch test, a Jacobian-lens answer readout recovers the
report channel but is markedly less contract-selective than the interchange-identified coordinate (and far more so than
an ordinary logit-lens), so the report coordinate is not reducible to a generic workspace readout.
Activation steering and composition. Activation addition [Turner et al., 2023], RepE/LoRRA [Zou et al., 2023],
CAA [Panickssery et al., 2024], ReFT [Wu et al., 2024] and MAT-Steer [Nguyen et al., 2025], conditional variants
(CAST [Lee et al., 2024], SADI [Wang et al., 2024], HyperSteer [Sun et al., 2025]), multi-property and Dynamic
Activation Composition methods, and Steering Tokens all compose steering vectors, and CFG [Sanchez et al., 2024]
and DExperts [Liu et al., 2021] perform the logit-space analogue. Our intervention is not a global steering vector
but a counterfactual coordinate replacement that keeps licensed evidence and removes only forbidden pressure, with
path-specificity supplied by the reference. We use CFG/DExperts and fixed-direction steering as baselines and find an
empirical Pareto tradeoff between resist and update that the clamp escapes.
Causal mediation, interchange, and synthetic ground truth. Activation patching, causal tracing, and interchange
interventions and interchange-intervention training [Geiger et al., 2021, 2022] are standard mechanistic-interpretability
tools, and the principle “invariant to nuisance, sensitive to causal signal” is well established (IRM and ICP [Arjovsky
et al., 2019, Peters et al., 2016], counterfactual and path-specific fairness [Kusner et al., 2017, Chiappa, 2019], and
INLP/LEACE concept erasure [Ravfogel et al., 2020, Belrose et al., 2023]). We claim neither as new. We use inter-
change not merely to localize a component but to define a report-coordinate contract, identified by necessity, suffi-
ciency (with rank), exclusion, and blocking, and we use it to drive the clamp. Known-ground-truth synthetic settings
are accepted in interpretability (InterpBench [Gupta et al., 2024]), so our known posteriors are a measurement feature,
with the natural-data transfer (Section 7) serving as an external-validity check. The defensible contribution is this
conjunction, which no baseline in our suite matches.
3 Benchmark: The Bayesian-Witness Setting
Each episode hides a binary world state with a uniform prior. Signals are emitted with stated likelihood ratios, so
the exact posterior, which we denote ψ, is computable by log-odds accumulation. Object evidence always enters the
posterior, whereas a user testimony enters only weighted by a stated reliability, and a random-reliability user is a strict
null. The design turns on one feature: the same user disagreement is instantiated as licensed (reliable testimony, that
is, real evidence) or forbidden (pressure, prestige, or restyling) across a factorial set of at least nine counterfactual
variants, so resistance and updating are measured on matched material. Reports are structured (answer, confidence,
and caveat) and parsed from generation. A two-pass runner first elicits the model’s own committed report and then
measures distortion relative to it, a belief-escrow protocol. Posteriors are recorded only as data labels and are never
used by the algorithm.
Scope of the benchmark and models. The Bayesian-witness benchmark is an identification benchmark, not a claim
of natural-distribution coverage: known posteriors and the reliability variable that renders the same disagreement
licensed or forbidden are precisely what make resist and update causally scorable and break the evidence/pressure
confound. Ecological validity is tested separately by the natural SycophancyEval transfer (Section 6.4). We validate
across open instruction/base families in the dense 3–8B regime (Qwen2.5-3B/7B, Mistral-7B-Instruct-v0.3, Llama-
3.1-8B-Instruct), chosen for stable activation access and reproducible interchange/clamp interventions rather than
frontier scale; larger and non-dense architectures remain untested.
4 Motivating Result: The Incentive-Compatibility Failure
Under forbidden pressure the model flips its answer at rate 0.77 (3B 0.91), while matched style and prestige pertur-
bations move it 0.00. This is a specific response to incentive rather than generic context sensitivity (Table 1). Under
licensed evidence the model updates correctly and calibrates toward the new posterior (deviation ≈ 0.02), passing
an evidence-responsiveness control even when evidence is bundled with pressure. A witness-specific failure also ap-
pears: the model over-trusts an explicitly unreliable user (flip 0.54), which correct reliability-weighting would not.
 3
Resist and Update A Preprint
Table 1: Descriptive characterization of the IC failure. Per-variant answer-flip and confidence-shift under forbidden pressure
compared with matched style and prestige perturbations (Qwen2.5-7B and 3B, n = 600). Forbidden pressure flips answers (0.77
and 0.91) while matched style and prestige move them by 0.00. Licensed evidence updates and calibrates to the revised posterior
(deviation from ψ ≈ 0.02). |∆ψ| is the absolute confidence deviation from the Bayes-target posterior ψ. Base answer accuracy
is 0.98 (7B) and 0.92 (3B) with confidence mean absolute error (MAE) 0.11 and 0.13 relative to the posterior, and all flips are
measured relative to this base report.
 Variant Path 7B flip 7B conf-shift 7B |∆ψ| 3B flip 3B |∆ψ|
 style_changed forbidden 0.00 0.03 n/a 0.00 n/a
 prestige_swapped forbidden 0.00 0.02 n/a 0.00 n/a
 actual_pressured forbidden 0.77 0.14 n/a 0.91 n/a
 evidence_flipped licensed 0.98 0.17 0.024 0.92 0.026
 pressure_plus_evidence mixed 0.98 0.17 0.019 0.92 0.023
 testimony_expert_mode licensed 0.02 0.03 0.15 0.09 0.11
 testimony_expert_opp licensed 0.60 0.08 0.12 0.92 0.10
 testimony_random_opp licensed (C=0.5) 0.54 0.14 0.13 0.92 0.11
The pattern is ordered by scale, with the 7B model more robust than the 3B model though both exhibit the failure.
5 Method: Counterfactual Report Coordinates
Our method has two components: we first causally identify low-rank report coordinates by interchange interventions
(Section 5.1), then clamp them toward an incentive-neutralized counterfactual reference at inference (Section 5.2).
5.1 Causal Identification of Report Coordinates
Using interchange interventions at the post-reasoning decision position, patching the answer-decision residual from a
counterpart with the opposite answer flips the decision to the source at rate 0.95, while a same-answer control moves
it 0.03. The effect localizes to a late layer (L⋆ =24 of 28), with an abrupt transition from L23 to L24 (Figure 1a). A
rank sweep shows that the transfer saturates by rank 16 (ρ16 = 0.93, far below the full dimension), so the coordinate
is genuinely low-rank, although we do not claim a universal low-rank truth direction (Figure 1b). Necessity is block-
level and localizes to the report subspace: single-layer mean-ablation barely moves accuracy (0.80/0.86), because the
answer is redundantly represented, while ablating the L24–27 window collapses accuracy to chance (0.53). Window
ablation alone does not isolate the coordinate, however: ablating a covariance-matched random subspace of equal rank
at the same layers is equally destructive (0.53), so removing any high-variance block degrades answering. The local-
izing evidence is instead a mediation test on the interchange intervention itself: decomposing the clamp’s donor delta,
its report-subspace component carries the resistance effect (0.90) while a norm-matched orthogonal complement does
not (0.38), so the causal steering is carried by the coordinate rather than by a generic large perturbation (n=120). Con-
fidence and caveat coordinates are identified analogously at L25 and L23, and the three are mutually near-orthogonal
(pairwise | cos | ≤ 0.10; Figure 1c). A causal cross-talk test shows this orthogonality is largely functional and not
merely geometric for the answer and caveat coordinates: clamping either moves its own readout strongly (answer
0.63, caveat 0.87) while inducing only small cross-effects on the other (answer→caveat 0.18, caveat→answer 0.08;
random-intervention floor 0.06/0.03). The confidence coordinate is a weaker causal instrument on this benchmark (its
own readout moves only 0.05), so we claim partial functional disentanglement (strong own-coordinate control with
small but nonzero cross-talk) for the answer and caveat coordinates and treat confidence as a scoped caveat rather than
asserting clean three-way causal orthogonality.
5.2 The Counterfactual Report-Coordinate Clamp
At inference we read the answer coordinate from a reference run with forbidden factors removed and licensed factors
retained, and we clamp the pressured run’s window (L24–27) toward it. On the witness benchmark this two-pass
clamp attains resist and update of 1.00 jointly (Wilson 95% CI [0.99, 1.00], n = 300), a causal certificate under a
constructible reference; the deployable single-pass form is deferred to Section 6.3. Here resist tracks the no-pressure
base report and update tracks the evidence-revised posterior. Path-specificity comes entirely from the reference rather
than from a global strength parameter α (Table 2). A rank-16 window clamp (the interchange-derived low-rank
 4
Resist and Update A Preprint
 (a) Sufficiency by layer. (b) Rank sweep. (c) Coordinate orthogonality.
Figure 1: Causal identification of report coordinates. (a) Interchange patching of the answer-decision residual flips the decision
to the source (sufficiency 0.95) relative to a same-answer control (0.03); the effect localizes at L⋆ =24. (b) Transfer fidelity ρk
saturates by rank 16 (ρ16 = 0.93), indicating a genuinely low-rank coordinate rather than a universal truth direction. (c) The answer,
confidence, and caveat coordinates are pairwise near-orthogonal (| cos | ≤ 0.10), providing the mechanistic basis for independent,
composable control.
projection applied alone) retains both but does not reach the ceiling (0.88/0.90 on the n=300 evaluation; an earlier
n=120 run reported 0.89/0.93), so the perfect 1.00/1.00 is a property of the full-window reference clamp rather
than of the low-rank projection. The result reproduces at 3B and across two further model families. On Mistral-7B-
Instruct-v0.3 (L29/32) and Llama-3.1-8B-Instruct (L28/32) the pipeline re-identifies a late low-rank report coordinate,
and the window clamp again reaches resist and update of 1.00 (n = 120, Section 6.4). Across all three families the
coordinate sits at a proportionally late layer (relative depth 0.86 to 0.91), which suggests that the report-commit stage
is a cross-architecture regularity rather than a model-specific artifact. The reference is the model’s own belief-escrow
self-report under a counterfactually incentive-neutralized context, not an external ground-truth oracle. The two-pass
clamp is therefore a causal certificate and an upper bound, with deployment addressed by the single-pass compilation
of Section 6.3.
Scope of the reference. Constructing the reference requires writing an incentive-neutralized counterfactual of the
prompt, that is, removing forbidden factors (pressure, prestige, and restyling) while preserving licensed evidence.
This is straightforward when those factors are separable, editable spans in the input. In the witness benchmark they
are explicit variables, and in our SycophancyEval transfer (Section 6.4) the user’s wrong assertion is a removable
span. It is harder when forbidden and licensed signals are entangled in one span, or when the licensed signal is
implicit. In those cases an imperfect reference would under- or over-correct, and the clamp’s quality degrades to that
of the reference rather than breaking down abruptly. We therefore present the two-pass clamp as a certificate under
a constructible reference, and the one-pass compilation (Section 6.3) provides the route to settings where an explicit
counterfactual is unavailable at inference.
6 Experiments
6.1 Dual Control and Baseline Comparisons
No global method attains both in our matched setting (Table 2). CFG/DExperts drives forbidden-flip to 0 at α=1,
but its licensed-update error grows monotonically (0.026 → 0.17), an instance of resisting or updating but not both.
We report CFG’s degradation as this continuous licensed posterior-deviation (error against the Bayes target) rather
than the binary update-success rate used for the other rows. Its single global parameter has no operating point that
both removes forbidden flips and preserves licensed updates, so what it breaks is calibration to the revised posterior
rather than a discrete update event. The two metrics are therefore not strictly isomorphic, and we make the substitution
explicit rather than force a binary score (see the † note on Table 2). Fixed-direction steering is worse (resist 0.53,
update 0.57 at α=8). The same global parameter suppresses forbidden and licensed changes together, so a single
strength cannot separate them.
 5
Resist and Update A Preprint
Table 2: Dual-control results. Resist and update with Wilson 95% confidence intervals across methods (Qwen2.5-7B-Instruct).
Only the two-pass counterfactual report-coordinate (CRC) clamp attains resist ≈ 1.0 and update ≈ 1.0 together, and it does so
as a causal certificate/upper bound under a constructible reference; its deployable single-pass form (no inference-time reference)
reaches 0.73/0.97. Global methods trade one against the other, and resist-only output-SFT generalizes resistance but collapses
update to 0.01.
 Method Resist Update n
 no intervention 0.28 [0.23, 0.33] 0.88 [0.83, 0.91] 300
 CFG/DExperts (α=1) 1.00 [0.98, 1.00] † 200
 steering (α=8) 0.53 [0.37, 0.67] 0.57 [0.42, 0.71] 40
 output-SFT resist-only (held-out) 1.00 [0.97, 1.00] 0.01 [0.00, 0.04] 125
 CRC clamp 2-pass (window) 1.00 [0.99, 1.00] 1.00 [0.99, 1.00] 300
 CRC clamp 1-pass trained 0.73 [0.60, 0.84] 0.97 [0.88, 0.99] 50
† CFG/DExperts has no comparable binary update score. Its single global parameter suppresses licensed updates as it removes forbidden flips, so
 licensed posterior-deviation grows monotonically (0.026 → 0.17 over α) rather than tracking the revised posterior (Section 6.1).
6.2 Stubbornness and Output-Level Training
Output-level fine-tuning is the most instructive case (Figure 2): a resist-only low-rank adaptation (LoRA) generalizes
resistance to unseen pressure phrasings (resist 1.0 on three held-out pressure-phrasing families, n = 125), yet its
update collapses to 0.01, having learned never to change its answer and thereby conflating resistance with contrarian-
ism.1 Full two-objective supervised fine-tuning (SFT) can match in-distribution only by explicitly enumerating both
targets, at higher cost and with template-memorization signatures. We therefore do not rely on output-level SFT as a
mechanism-level solution, and the resist-only variant is what exposes the failure mode. The reference-based clamp,
by contrast, holds resistance across all families (0.92) and updates (1.0) with no training, and it does not exhibit this
loss of evidence-responsiveness in our held-out tests, because path-specificity comes from the reference rather than
from learned weights and there is no learned resist-only objective to overfit. This dual-control contrast distinguishes
the clamp from the baseline suite.
Figure 2: Held-out pressure discriminator. On three held-out pressure-phrasing families, the CRC clamp stays flat in resistance
and continues to update (≈ 1.0), whereas resist-only output-SFT generalizes resistance but its update collapses to 0.01, losing
evidence-responsiveness.
6.3 Single-Pass Compilation
The two-pass clamp requires an extra reference forward pass. Compiling it into a single pass with a small trained gated
primitive (warm-started at the identified layer) reaches resist 0.73 and update 0.97 with no inference-time reference,
whereas naïve coordinate-matching distillation reaches only 0.48 and 0.82 (Figure 3). A perfect one-pass predictor
of the reference coordinate would reproduce the two-pass result, so the extra forward pass provides per-input refer-
ence information that our current one-pass modules do not capture, and end-to-end answer supervision outperforms
 1 This resist-only update collapse is the same phenomenon a companion paper analyzes in depth on a free-generation benchmark (there evidence-
updating 0.72→0.13 under a different checkpoint, eval, and update denominator); a reader of both papers should not treat them as independent
evidence.
 6
Resist and Update A Preprint
coordinate-matching. The gap therefore quantifies the per-input information or structure carried by the incentive-
neutral counterfactual reference that these modules fail to recover; we do not establish that the pressured forward pass
provably lacks this information, only that closing the gap would require a stronger one-pass compiler than ours. We
present this as the boundary of the inference-time method and as the motivation for internalizing the contract through
counterfactual reinforcement learning from AI feedback (RLAIF) or direct preference optimization (DPO), which we
leave to future work.
Figure 3: One-pass compilation trade-off. The two-pass clamp (1.0/1.0) is the causal upper bound. A trained gated primi-
tive (answer-supervised) reaches 0.73/0.97 with no reference forward pass, while naïve coordinate-MSE distillation reaches only
0.48/0.82.
6.4 Transfer to Natural Questions
We test whether the controlled phenomenon has a real-world counterpart. We reuse our earlier multi-turn-pushback
experiments (a causal capitulation direction and a trained primitive lifting faithfulness 0.31 → 0.97) and add a transfer
test on Sharma et al.’s SycophancyEval [Sharma et al., 2023] (are_you_sure, multiple-choice), with the witness-
identified report window reused verbatim and not re-identified. Dual control holds on the natural questions in all three
families (n = 300 each, bootstrap 95% CIs, Figure 4). For resist, under insistent non-evidential pressure the models
capitulate 58 to 90% of the time, and the report-coordinate clamp removes every flip (resist → 1.00). To show that
the low-rank coordinate, rather than a window of residuals, carries the effect, we learn a rank-16 projector by singular
value decomposition on a train half of the natural items and apply it to the disjoint test half. This held-out clamp
stays effective (resist 0.79 to 0.95), so the correction transfers across items rather than being fit to the evaluation set.
Our primary negative control, clamping toward a different item’s reference (mismatched-reference), leaves resist at a
low control level (0.33 to 0.38, Figure 4A), and a norm-matched random vector serves as a secondary check (0.31 to
0.39). Both are far below 1.00, so the clamp tracks item-specific report content rather than pinning the readout with
any strong patch. For update, on items the model answers incorrectly, given a reliable correction (the dataset’s own
worked solution where available, and an asserted source otherwise) while the user pushes a different wrong option, the
clamp lifts correction-tracking over the no-clamp baseline in every family (clamp 0.84 / 0.68 / 0.87 versus baseline
0.62 / 0.57 / 0.73 for Qwen, Mistral, and Llama), and the held-out rank-16 clamp nearly matches it (0.80 / 0.68 /
0.90, Figure 4B). Because some marginal intervals overlap their baseline, we confirm the gain with a paired McNemar
test (clamp versus baseline on the same items). It is significant in every family (p < 10−5 , 6 × 10−3 , and 4 × 10−5
for Qwen, Mistral, and Llama, with paired ∆ of +0.22, +0.12, and +0.14 and bootstrap CIs that all exclude 0). On
the fully-natural subset whose evidence is the dataset’s own worked solution (Figure 4D), the clamp lifts update from
a baseline of 0.63 to 0.91 (Qwen) and 0.54 to 0.83 (Llama). For Mistral the baseline is itself only 0.18, indicating
that it barely exploits long worked-solution evidence unaided, and the clamp raises it to 0.37 (paired ∆ = +0.18,
95% CI [0.03, 0.34], McNemar p = 0.07); given the small sample we read this as a positive but borderline trend.
The low absolute Mistral number is therefore a property of Mistral’s weak use of worked-solution evidence rather
than a clamp failure, and reporting the solution-only baseline, not only the clamp, is what makes this interpretable.
Finally, a global-steering control baseline on the same items does not achieve both objectives. Sweeping one anti-
sycophancy direction over strength α trades resist against update (Qwen and Llama) or fails to move resist at all
(Mistral), reproducing the witness tradeoff of Section 6.1 on natural data, whereas the clamp occupies the high-resist,
high-update region (Figure 4C). The same clamp therefore both resists pressure and updates to evidence on natural
questions. A scope caveat: the questions are natural, but the licensed-evidence turn is constructed (worked-solution
 7
Resist and Update A Preprint
evidence on approximately one third of update items, and an asserted source otherwise), and the witness benchmark
remains the fully-controlled, primary evidence. All results are in the dense 7 to 8B instruction-tuned regime.
Figure 4: Natural-question dual control (SycophancyEval are_you_sure transfer, Qwen-7B, Mistral-7B, and Llama-3.1-8B,
n = 300 each). (A) Resist: the clamp removes every flip (resist → 1.0), a rank-16 projector learned on a train half and applied
to the disjoint test half stays effective, and the mismatched-reference and norm-matched random-vector controls remain at a low
control level. (B) Update: the clamp lifts correction-tracking over the no-clamp baseline, with the held-out rank-16 clamp nearly
matching, and a paired McNemar test confirms the gain is significant in every family. (C) A global anti-sycophancy steering sweep
traces a resist–update tradeoff on the same items, while the clamp (⋆) occupies the high-resist, high-update region. (D) Worked-
solution subset: on items whose evidence is the dataset’s own worked solution, the clamp raises update in all three families.
Mistral’s low absolute level reflects a weak baseline (0.18) on worked-solution evidence rather than a clamp failure († marks paired
McNemar p > 0.05, borderline). Error bars are bootstrap 95% CIs.
6.5 Robustness: latent reliability, not a surface cue, and preserved updating
Two controls address whether the perfect witness score reflects a lexical shortcut or merely generic pressure-resistance.
(i) The clamp reads latent reliability, not the reliability token. Replacing the explicit numeric reliability cue with
a semantic source-history description (“correct on 8 of its last 10 calibration questions”), using paraphrases absent
from coordinate fitting, leaves the clamp intact (resist 0.91, update 1.00; window-full 1.00/1.00; n = 300). When
an explicit reliable/unreliable label is added that conflicts with the source history and the target is scored against
the history-implied posterior, the clamp still tracks the latent reliability (resist 0.90, update 0.96) rather than the
surface label—a lexical shortcut would fail this arm. (ii) The clamp preserves legitimate evidence-updating, not
just resistance. On a crossed-factorial benchmark varying truth, prior-agreement, source reliability, and pressure
wording independently and fully counterbalanced (n = 320; including the “false-but-declared-reliable” and “true-
but-unreliable” cells), the window clamp attains resist 1.00 and update 1.00 (rank-16 on this crossed-factorial set
0.92/0.98; matching the headline dual-control result of Table 2): it updates toward declared-reliable evidence and
resists the unreliable source, decorrelated from truth and answer side. The clamp therefore enforces the reliability-
implied posterior, not a generic answer-invariance.
7 Discussion and Limitations
Joint clamping composes: clamping the answer and confidence coordinates together produces near-zero cross-talk
(leakage 0.002), which realizes the measured near-orthogonality as independent control.
Statistical protocol and analysis roles. We separate confirmatory from diagnostic quantities. The causal-identification
tests (interchange sufficiency, the rank sweep, block-level necessity, and tri-coordinate orthogonality) are diagnostics
that characterize the report coordinate; the dual-control comparison against baselines (Table 2) and the natural-data
transfer (Section 6.4) are the confirmatory claims. Dual-control rates carry 95% Wilson intervals (n = 300 on the
witness benchmark, n = 300 per family on SycophancyEval); paired natural-data update gains use a McNemar test
on the same items with bootstrap ∆ intervals; flip and update rates are intent-to-treat over parsed structured reports.
The witness posteriors enter only as evaluation labels, never as inputs to the clamp.
 1. Synthetic known-posterior setting. Known posteriors make resist and update exactly scorable, but the task is
 deliberately narrow, and we claim a controlled causal mechanism rather than full real-world coverage.
 2. Model-family coverage. Validated across three families, namely Qwen2.5 (3B/7B), Mistral-7B-Instruct-v0.3,
 and Llama-3.1-8B-Instruct. The IC failure, a causally-identified late low-rank report coordinate (L24/28, L29/32,
 8
Resist and Update A Preprint
 and L28/32 respectively), the dual-control window clamp (resist and update of 1.00 in all three), and the Syco-
 phancyEval natural-data transfer (capitulation 0.58/0.82/0.90 → 0.00) all reproduce. Llama’s witness de-
 scriptive parsing is noisier, reflecting an output-format readout mismatch rather than a mechanism gap, since
 its clamp and causal identification use a forced readout and are clean. Larger and non-dense architectures, for
 example mixture-of-experts models, remain untested.
 3. Block-level necessity. The answer coordinate is necessary as a late-layer block (L24–27) rather than at any
 single layer, which reflects expected late-layer redundancy, and we do not claim single-layer necessity.
 4. Lossy one-pass compilation. The deployable single-pass form reaches 0.73/0.97, below the two-pass certifi-
 cate, and closing this gap is a direction for future work.
 5. Caveat behavior not solved. The caveat coordinate is cleanly identified and composes, but the behavioral caveat
 policy is poorly calibrated, as the model over-caveats, and our caveat-coordinate results support composability
 rather than a solved caveat policy.
None of these undermines the core claim, that counterfactual report mediators can be causally identified and clamped
to achieve dual control where global and output-level methods do not; each instead delimits its scope.
8 Conclusion
We framed report-stage misreporting under non-evidential pressure as a failure of internal incentive-compatibility, and
addressed it with counterfactual report coordinates: low-rank, causally identified mediators of a model’s answer, con-
fidence, and caveat reports. Clamping these coordinates toward the model’s own report under an incentive-neutralized
counterfactual achieves dual control, resisting forbidden pressure while remaining responsive to licensed evidence,
where global decoding, steering, and output-level training do not. The effect holds across three model families and
transfers to a natural sycophancy benchmark, and compiling the two-pass clamp into a single forward pass is lossy in a
way that quantifies the information the counterfactual reference supplies. We view the contribution as an interface for
certifying activation-level incentive-invariance, and internalizing the contract through training is a natural next step: in
the companion paper we show that this certificate can be partially compiled into one-pass behavior, with a diagnosed
residual gap.
References
Anthropic Interpretability Team. Verbalizable representations form a global workspace in language models. https:
 //transformer-circuits.pub/2026/workspace/index.html, 2026. Transformer Circuits Thread.
Martin Arjovsky, Léon Bottou, Ishaan Gulrajani, and David Lopez-Paz. Invariant risk minimization. arXiv preprint
 arXiv:1907.02893, 2019.
Katherine Atwell, Pedram Heydari, Anthony Sicilia, and Malihe Alikhani. Basil: Bayesian assessment of sycophancy
 in llms. arXiv preprint arXiv:2508.16846, 2025.
Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, and Stella Biderman. LEACE:
 Perfect linear concept erasure in closed form. In Advances in Neural Information Processing Systems 36 (NeurIPS
 2023), 2023.
Joy Bhalla and Kristina Gligorić. Sway: A counterfactual computational linguistic approach to measuring and miti-
 gating sycophancy. arXiv preprint arXiv:2604.02423, 2026.
Silvia Chiappa. Path-specific counterfactual fairness. In Proceedings of the AAAI Conference on Artificial Intelligence
 (AAAI 2019), volume 33, pages 7801–7808, 2019.
Atticus Geiger, Hanson Lu, Thomas Icard, and Christopher Potts. Causal abstractions of neural networks. In Advances
 in Neural Information Processing Systems 34 (NeurIPS 2021), 2021.
Atticus Geiger, Zhengxuan Wu, Hanson Lu, Josh Rozner, Elisa Kreiss, Thomas Icard, Noah D. Goodman, and Christo-
 pher Potts. Inducing causal structure for interpretable neural networks. In Proceedings of the 39th International
 Conference on Machine Learning (ICML 2022), volume 162 of Proceedings of Machine Learning Research, pages
 7324–7338, 2022.
Rifo Genadi, Munachiso Nwadike, Nurdaulet Mukhituly, Hilal Alquabeh, Tatsuya Hiraoka, and Kentaro Inui. Syco-
 phancy hides linearly in the attention heads. arXiv preprint arXiv:2601.16644, 2026.
 9
Resist and Update A Preprint
Rohan Gupta, Iván Arcuschin, Thomas Kwa, and Adrià Garriga-Alonso. Interpbench: Semi-synthetic transformers
 for evaluating mechanistic interpretability techniques. In Advances in Neural Information Processing Systems 38
 (NeurIPS 2024), Datasets and Benchmarks Track, 2024.
Shreyans Jain, Alexandra Yost, and Amirali Abdullah. Sycophancy as compositions of atomic psychometric traits.
 arXiv preprint arXiv:2508.19316, 2025.
Matt J. Kusner, Joshua R. Loftus, Chris Russell, and Ricardo Silva. Counterfactual fairness. In Advances in Neural
 Information Processing Systems 30 (NeurIPS 2017), 2017.
Bruce W. Lee, Inkit Padhi, Karthikeyan Natesan Ramamurthy, Erik Miehling, Pierre Dognin, Manish Nagireddy, and
 Amit Dhurandhar. Programming refusal with conditional activation steering. arXiv preprint arXiv:2409.05907,
 2024.
Alisa Liu, Maarten Sap, Ximing Lu, Swabha Swayamdipta, Chandra Bhagavatula, Noah A. Smith, and Yejin Choi.
 Dexperts: Decoding-time controlled text generation with experts and anti-experts. In Proceedings of the 59th Annual
 Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural
 Language Processing (Volume 1: Long Papers), 2021.
Muhammad Ahmed Mohsin, Ahsan Bilal, Muhammad Umer, and Emily Fox. Pressure, what pressure? sycophancy
 disentanglement in language models via reward decomposition. arXiv preprint arXiv:2604.05279, 2026.
Duy Nguyen, Archiki Prasad, Elias Stengel-Eskin, and Mohit Bansal. Multi-attribute steering of language models via
 targeted intervention. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics
 (ACL), 2025.
Nina Panickssery, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, and Alexander Matt Turner. Steering
 llama 2 via contrastive activation addition. In Proceedings of the 62nd Annual Meeting of the Association for
 Computational Linguistics (ACL), 2024. First author formerly published as Nina Rimsky.
Jonas Peters, Peter Bühlmann, and Nicolai Meinshausen. Causal inference by using invariant prediction: Identification
 and confidence intervals. Journal of the Royal Statistical Society: Series B (Statistical Methodology), 78(5):947–
 1012, 2016. doi: 10.1111/rssb.12167.
Shauli Ravfogel, Yanai Elazar, Hila Gonen, Michael Twiton, and Yoav Goldberg. Null it out: Guarding protected
 attributes by iterative nullspace projection. In Proceedings of the 58th Annual Meeting of the Association for
 Computational Linguistics (ACL 2020), pages 7237–7256, 2020.
Guillaume Sanchez, Honglu Fan, Alexander Spangher, Elad Levi, Pawan Sasanka Ammanamanchi, and Stella Bider-
 man. Stay on topic with classifier-free guidance. In Proceedings of the 41st International Conference on Machine
 Learning (ICML), 2024.
Mrinank Sharma, Meg Tong, Tomasz Korbak, David Duvenaud, Amanda Askell, Samuel R. Bowman, Newton Cheng,
 Esin Durmus, Zac Hatfield-Dodds, Scott R. Johnston, Shauna Kravec, Timothy Maxwell, Sam McCandlish, Kamal
 Ndousse, Oliver Rausch, Nicholas Schiefer, Da Yan, Miranda Zhang, and Ethan Perez. Towards understanding
 sycophancy in language models. arXiv preprint arXiv:2310.13548, 2023. Also presented at ICLR 2024.
Jiuding Sun, Sidharth Baskaran, Zhengxuan Wu, Michael Sklar, Christopher Potts, and Atticus Geiger. Hypersteer:
 Activation steering at scale with hypernetworks. arXiv preprint arXiv:2506.03292, 2025.
Alexander Matt Turner, Lisa Thiergart, Gavin Leech, David Udell, Juan J. Vazquez, Ulisse Mini, and Monte Mac-
 Diarmid. Activation addition: Steering language models without optimization. arXiv preprint arXiv:2308.10248,
 2023. Later arXiv versions retitled “Steering Language Models With Activation Engineering”.
Daniel Vennemeyer, Phan Anh Duong, Tiffany Zhan, and Tianyu Jiang. Sycophancy is not one thing: Causal separa-
 tion of sycophantic behaviors in llms. arXiv preprint arXiv:2509.21305, 2025.
Keyu Wang, Jin Li, Shu Yang, Zhuoran Zhang, and Di Wang. When truth is overridden: Uncovering the internal
 origins of sycophancy in large language models. arXiv preprint arXiv:2508.02087, 2025.
Weixuan Wang, Jingyuan Yang, and Wei Peng. Semantics-adaptive activation intervention for llms via dynamic
 steering vectors. arXiv preprint arXiv:2410.12299, 2024.
Zhengxuan Wu, Aryaman Arora, Zheng Wang, Atticus Geiger, Dan Jurafsky, Christopher D. Manning, and Christo-
 pher Potts. Reft: Representation finetuning for language models. In Advances in Neural Information Processing
 Systems (NeurIPS), 2024.
Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas
 10
Resist and Update A Preprint
 Mazeika, Ann-Kathrin Dombrowski, Shashwat Goel, Nathaniel Li, Michael J. Byun, Zifan Wang, Alex Mallen,
 Steven Basart, Sanmi Koyejo, Dawn Song, Matt Fredrikson, J. Zico Kolter, and Dan Hendrycks. Representation
 engineering: A top-down approach to ai transparency. arXiv preprint arXiv:2310.01405, 2023. Introduces LoRRA
 (Low-Rank Representation Adaptation).
 11
