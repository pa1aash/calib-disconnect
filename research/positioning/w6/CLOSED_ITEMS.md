# Wave 5 unverified items closed in wave 6 (task A4)

Run date 2026-11-10. Sub-agent record: `../../../docs/s6/parts/closed-A4/CLOSED.md`. It contains every quote with its line number. The fetched PDF, HTML, and text of 2609.36783 are in `../../../docs/s6/parts/closed-A4/raw/`, with SHA-256 prefixes.

## 1. Miglani et al., arXiv 2609.36783: "0.677 versus 0.703"

**VERIFIED.** Full text, v2, dated 2026-09-30 (`raw/2609.36783.txt`).

- **Qwen2.5-Coder** (Sec 4.2, Table 1): "On the same attempts within the Qwen2.5-Coder experiment, probe AUC is 0.677 and log-probability confidence AUC is 0.703 (Table 1)." There are 448 attempts from 56 problems.
- **DiffuCoder-7B:** probe 0.842 against negative token entropy 0.838, and 0.798 for the masked-forward score. There are 95 attempts from 19 problems.
- **Metric:** within-problem AUC, averaged over mixed problems (lines 111-113).
- **Same attempts:** yes, within each model (Table 1 caption).
- **Activations and folds:** activations are centered within problem, and the five folds are assigned by problem (App B, line 485).

**Precision notes for every later use of these numbers:**

- **Optimistic probe value.** The probe value is the maximum over layers of out-of-fold AUC, "without an additional holdout" (lines 116-117). It is biased upward, so the Qwen deficit is not an artifact against the probe. It is also an example of the layer-selection leakage that `docs/s6/PIPELINE_DESIGN_R1.md` section 7 forbids.
- **No significance claims.** The paper makes none: "We therefore compare point estimates rather than make significance or equivalence claims" (line 340).
- **Comparator and benchmark.** The comparator is token likelihood, not stated confidence. The benchmark is MBPP+ (line 669).
- **Ties and model size** (A6 F20). The AUC uses "sorted ranks without explicit tie averaging" (line 488). The paper does not state the size of the Qwen2.5-Coder model.

**Effect on verdicts:** none. The W4 sentence stands, with the comparator named as completion log probability.

## 2. Thinking-in-Bets, arXiv 2610.34654: content of the bug reports

**The paper does not specify it.** Full text: `../w5/parts/ft-A4b/raw/ft/2610.34654.txt`.

- **No simulated-user prompt.** Appendix A.1 (lines 841-960) gives agent-side prompts only.
- **Tables 8 and 13 hold only counts and rates** (lines 1502, 1800, 2464-2479).
- **What the text does say:**
  - Valid and mistaken feedback come from a simulated user (line 465).
  - In SWE-Pushback-Hidden, "The harness privately runs a hidden test: the complaint is mistaken if the requirement passes and valid if it fails" (line 468).
  - Mistaken criticism "is usually a brief objection without a failing case" (line 543).
  - In SWE-Interact, validity combines hidden tests with a model judge, with Cohen's kappa 0.963 (line 2574).

**Wording for any later sentence:**

> natural-language bug reports from a simulated user, whose validity is set by hidden tests (SWE-Pushback-Hidden) or by hidden tests combined with a model judge (SWE-Interact)

Say neither that the agent sees a failing test nor that it does not.

**Effect on verdicts:** none. L3 Q2/Q7 stays NARROW. The Rank 3 study stays out of the main paper (operator decision, wave 6).
