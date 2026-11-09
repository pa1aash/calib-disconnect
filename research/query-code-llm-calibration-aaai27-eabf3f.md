---
vault_tag: code-llm-calibration-aaai27
created: 2026-07-17T18:20:28Z
source: user-prompt
---

## User's verbatim request

Look for places where we can extend this paper and make it AAAI 27 main track
level. Go through previous works within this field, look for caveats and holes
that we can write a paper in. Shortlist ~5-10 papers and synthesize to have one
final paper idea with a confident headline result that is extremely novel. I
don't want to start running everything and waste time and money and have a dead
paper on my hands. Priority 1 is novelty and priority 2 is confidence in
attaining a headline and supporting results. Give me a good paper!

## What "this paper" is (grounding — the current manuscript, v3)

**Title:** "Mind the Gap: The Calibration Disconnect Between Internal and
Expressed Confidence in Code Language Models" (currently DL4C / ICML 2026 style,
blind).

**Central finding (descriptive/diagnostic):** Code LLMs possess a near-perfectly
calibrated *internal* uncertainty signal accessible via repeated sampling
(sampling-based confidence = empirical pass rate over n samples), but NO tested
*expressed* interface can faithfully communicate it. Specifically, on
HumanEval (164 problems) with an independent (n+1)-sample labeling protocol and
bootstrap 95% CIs:

- Sampling confidence: ECE 0.059, AUROC 0.987 (near-perfect discrimination).
- Token log-probability: ECE 0.058 but AUROC only 0.668. Post-hoc calibration
  (isotonic, Platt, 5-fold CV) IMPROVES ECE but DEGRADES AUROC (isotonic →
  0.587, Platt → 0.386), which the paper argues proves the discrimination
  failure is fundamental, not a calibration artifact.
- AST-clustering proxy (test-free, fraction in largest AST cluster): AUROC 0.689.
- Verbal self-assessment (1–5 scale) at τ=0.1 AND at matched τ=0.8: both fail
  (AUROC 0.564 and 0.519); model puts 67% of problems at max confidence.
- Cross-model: DeepSeek-Coder-6.7B-Instruct confirms overconfidence pattern but
  has pass@1 = 0.000 on HumanEval (instruction-format mismatch), so AUROC is
  undefined for it — only ECE is informative.
- SFT intervention (274 examples, LoRA r=16): reduces verbal ECE by 64% but a
  difficulty-subset analysis shows this is "calibration without discrimination"
  — the SFT model assigns mean confidence 0.900 to BOTH easy and hard problems;
  the distribution collapses to a single default bin.

**Metrics used:** ECE, TACE, Brier, AUROC, pass@1/pass@10.
**Models:** Qwen2.5-Coder-7B-Instruct (primary), DeepSeek-Coder-6.7B-Instruct.
**Benchmark:** HumanEval only (164). MBPP appears in earlier versions/results.
**Hardware available:** single NVIDIA A100-40GB (some runs) and an NVIDIA GH200
480GB (98GB VRAM) box. So single-GPU 7B-scale experiments are feasible; large
multi-node training is NOT.

**Known limitations the current paper admits:** two models, one benchmark
(HumanEval), self-contained function-level problems only (no repo-level /
multi-file / agentic SWE-bench-style tasks), skewed easy difficulty
distribution, SFT dataset only 274 examples, no real developer user study,
DeepSeek 0% pass rate limits analysis.

## What the research must deliver (the actual task)

The pipeline is NOT being asked to re-survey the paper. It is being asked to:

1. Survey prior work in code-LLM confidence/calibration/uncertainty estimation,
   selective code generation, train-time calibration (RL/SFT/distillation for
   verbalized confidence), semantic/self-consistency uncertainty, LLM
   abstention/deferral, and human-AI trust calibration for coding — enough to
   locate the REAL research frontier as of 2026.
2. Identify the specific caveats, holes, and unproven claims in that frontier
   (including in the current paper's own diagnostic finding) that a new paper
   could occupy.
3. Shortlist ~5–10 load-bearing papers and synthesize them into ONE concrete,
   defensible paper proposal that EXTENDS the current calibration-disconnect
   work into a positive/prescriptive contribution strong enough for AAAI-27 main
   track.
4. The proposal must state: a single extremely-novel headline claim; the exact
   experiment(s) that would produce the headline number; why that headline is
   likely to come out favorable (feasibility + prior-evidence grounding), given
   ONLY single-GPU 7B-scale compute; the supporting results needed; the most
   likely failure mode and a pre-registered fallback; and an honest novelty
   defense against the closest existing work.

Priority ordering is explicit and binding: **(1) novelty, (2) confidence that
the headline + supporting results will actually materialize.** The user
explicitly does not want a speculative direction that produces a dead paper.
Favor proposals where prior evidence already hints the result will land.

## ADDED BINDING CONSTRAINT (second invocation): AAAI-27 topic alignment

The final paper proposal MUST be pinned to a specific primary topic/keyword from
the AAAI-27 areas-and-topics list (https://aaai.org/conference/aaai/aaai-27/areas-and-topics/),
and the proposal will "never deviate from that scope." Requirements the research
must satisfy:

1. Identify the single best-fit AAAI-27 PRIMARY topic/keyword for the proposed
   paper, following AAAI's own selection rules (paste of those rules is part of
   this query): choose the subarea of the paper's MAIN methodological
   contribution — the community best positioned to evaluate it. For an ML method
   motivated by code, the primary topic is usually an ML keyword (with code as
   application), UNLESS the contribution is specifically about the structure of
   the code-generation problem, in which case an NLP/code keyword is primary.
   The most likely candidates for this line of work are ML keywords such as
   "ML: Calibration & Uncertainty Quantification", "ML: Trustworthy /
   Safe / Reliable ML", "ML: Evaluation", or an NLP keyword such as
   "NLP: (Large) Language Models" / "NLP: Applications" (code). The research
   must confirm the exact current AAAI-27 keyword strings and pick the best fit
   with a defended rationale, plus 1-2 sensible SECONDARY topics.
2. The proposed contribution must be a METHODOLOGICAL advance (not merely an
   application/measurement study), because AAAI main track rewards methodology;
   an application framing risks being redirected to AI-for-Social-Impact/IAAI.
   This reinforces the "positive/prescriptive, not diagnostic" requirement above.
3. Format reality: AAAI-27 main track = 7 pages main content (max 9 total, extra
   pages references only), supplementary allowed but not guaranteed to be read,
   mandatory reproducibility checklist. The proposal must therefore be scoped to
   fit ONE tight 7-page methodological story with one headline + a compact
   supporting-experiment set — not a sprawling multi-study agenda.

The final report must include an explicit "AAAI-27 topic alignment" treatment:
the chosen primary keyword (verbatim from the list), the rationale under AAAI's
rules, secondary keywords, and a one-line statement of why the paper's main
contribution sits in that subarea and will not drift out of it.
