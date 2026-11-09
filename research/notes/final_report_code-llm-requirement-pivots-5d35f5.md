# Direction-Discovery: Higher-Novelty Pivots Our Per-Requirement Assets Enable

**Committed recommendation: pursue "requirement-level code/test blind-spot alignment" (Direction B) as the
primary pivot, with the partial-pass compositionality mechanism (Direction C) as a fast complementary
analysis.** Four adversarial scouts vetted five pivot families against 2024-2026 literature. Two are scooped;
the strongest survivor uniquely requires BOTH of our rare assets (per-requirement execution labels + the
labeled 10-solution pool as a mutation-adequacy oracle) and has a crisp, un-scooped headline.

## Scoop map (what's dead)
- **Dense per-requirement RL reward — SCOOPED.** VeRPO (2601.03525, Jan-May'26) does exactly per-test partial
  reward + cardinality-bias correction (+8.83 pass@1); StepCoder, EGCA, PRM work; plus a negative-result paper
  (pass-rate reward doesn't beat binary). Kill.
- **Constrained/requirement-aware decoding — SCOOPED** for syntax/type (Type-Constrained Codegen, OOPSLA'25);
  semantic steering infeasible in weeks.
- **Requirement-decomposed self-repair — PARTIALLY SCOOPED** by SCOPE (2607.05810, Jul'26, on BigCodeBench Hard).
- **Partial-pass CONTRAST (34% functional vs ~0% competitive) — confirmatory, not novel** on its own (LeetCode/
  Codeforces bimodal collapse already shown, 2606.08840 / 2407.21579).

## Ranked surviving pivots

### B — Requirement-level code/test blind-spot alignment  [PRIMARY REC]
**Pitch:** score whether a model's *self-generated* unit tests actually discriminate correct-vs-incorrect
solutions **per requirement** (using our labeled 10-solution pool as a mutation set), then correlate that
per-requirement *test*-adequacy with the same model's per-requirement *code*-pass rate.
**Headline:** *"The requirement types a model fails to CODE are the same it fails to TEST for — per-requirement
competence, not role (coder vs verifier), drives failure — invisible to whole-task benchmarks."*
- **Novelty: OPEN.** Closest (SAGA/TCGBench, 2507.06920) shows code/test blind-spot correlation only at
  whole-problem granularity; nobody asks "is the specific requirement you can't code the one you can't test."
- **Feasibility: high.** Only new step = vLLM-generate self-tests + run against the existing labeled pool. No new ground truth.
- **Uniquely ours:** structurally needs BOTH assets at once — hard for whole-task-pass groups to replicate cheaply.
- **Actionable hook (de-risks "just a correlation"):** predict under-tested requirements → guide test generation / verifier improvement.

### C — Partial-pass compositionality mechanism  [FAST COMPLEMENT / SECTION]
**Pitch:** within-problem requirement-failure CORRELATION — do BCB requirements fail quasi-independently
(→ near-binomial partial-pass) while competitive-code sub-tests fail in a correlated block (→ bimodal collapse)?
A testable *structural explanation* for why partial credit exists in one regime and not the other.
- **Novelty: partial→open** (the mechanism, not the contrast). **Feasibility: very high** (pure analysis on existing pool, days).
- Best used as the mechanism section that turns a descriptive observation into an explanation; thin as a standalone.

### A — Cross-model requirement-level routing  [ATTRACTIVE, BUT VERIFY THE MECHANISM]
**Pitch:** models disagree at requirement level (Qwen vs DeepSeek); route/compose by requirement.
- **Novelty: open granularity** (all routing is whole-query). **But a real hole:** a function is monolithic —
  you can't stitch per-requirement code from two models, so "oracle per-requirement routing" risks collapsing to
  whole-solution best-of-2 (not novel) or requirement-level repair (overlaps scooped SCOPE/FLARE). Survives only
  as a *complementarity finding* or if a genuine composition mechanism exists. Rank below B until that's resolved.

### D — Within-task spec-ambiguity localization  [CLEAN SECONDARY]
**Pitch:** within one task, does the ambiguity of the clause naming requirement R predict R's failure (within-subject)?
- **Novelty: open** (Orchid / "When Prompts Go Wrong" are whole-task). **Feasibility: high** (annotate clause ambiguity + reuse labels).
- A clean, low-risk second track that shares the requirement-decomposition infra.

## Honest framing note
None of these is an 8-day paper — all are weeks-scale (multi-experiment + rigor) → **later venue**, consistent with
the earlier verdict. B is the strongest single bet: most novel, uniquely asset-enabled, crisp headline, feasible,
with an actionable hook. Recommended de-risk before committing: one targeted novelty check that no code-test
co-generation/agreement paper already does the per-requirement blind-spot alignment (scouts found none, but confirm).
