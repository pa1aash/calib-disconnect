# Wave 6, task A4: closing critic-A7 F20 (Miglani) and F9 (Thinking-in-Bets)

Retrieved 2026-11-10 by headless curl (desktop user agent) from arxiv.org.

## Raw files (docs/s6/parts/closed-A4/raw/)

| File | Source | SHA-256 (first 12) |
|---|---|---|
| 2609.36783.pdf | https://arxiv.org/pdf/2609.36783 (HTTP 200, application/pdf; header reads "arXiv:2609.36783v2 [cs.SE] 30 Sep 2026") | 94ddad186c2a |
| 2609.36783.html | https://arxiv.org/html/2609.36783 (HTTP 200) | 6abdd329ae3c |
| 2609.36783.txt | `pdftotext -layout` of the PDF, 721 lines | 948fd8f46d0f |

Line numbers below for item 1 refer to `raw/2609.36783.txt`. Line numbers for item 2 refer to `research/positioning/w5/parts/ft-A4b/raw/ft/2610.34654.txt`.

## Item 1: Miglani et al., arXiv 2609.36783. Verdict: VERIFIED (with two precision notes)

Title confirmed (line 1-2): "A Heckler in the Hidden State: Correctness Signals in Diffusion Language Models".

| Vault claim | Paper text | Status |
|---|---|---|
| Sec 4.2, Table 1 | Sec "4.2 Confidence provides a competitive readout" (line 176); Table 1 (lines 211-217) | VERIFIED |
| DiffuCoder-7B probe 0.842 vs negative token entropy 0.838 | line 177: "DiffuCoder gives a probe AUC of 0.842, compared with 0.838 for negative token entropy and 0.798 for the masked-forward confidence score."; Table 1 lines 215-216 | VERIFIED |
| Qwen2.5-Coder probe 0.677 vs completion log-probability 0.703 | line 178/208: "On the same attempts within the Qwen2.5-Coder experiment, probe AUC is 0.677 and log-probability confidence AUC is 0.703 (Table 1)."; Table 1 line 217 "Qwen2.5-Coder 0.677 0.703 Completion log probability" | VERIFIED |
| 19 problems, 95 attempts (DiffuCoder) | line 99: "the 32-step confidence comparison contains 95 attempts from 19 problems"; Table A2 line 474 "DiffuCoder, 32 denoising steps 19 95" | VERIFIED |
| 56 problems, 448 attempts (Qwen) | lines 99-100: "the Qwen2.5-Coder comparison contains 448 attempts from 56 problems"; Table A2 line 477 | VERIFIED |
| within-problem centering, folds grouped by problem (App B) | line 485: "Activations are centered within problem. Five folds are assigned by problem using NumPy seed 0; attempts from the same problem never cross folds." Also Sec 3.2, lines 108-110. | VERIFIED |
| Quote "Model confidence is thus a competitive baseline ... Reading hidden states provides little apparent gain" | lines 219-220, verbatim | VERIFIED |
| Steering pass@1 0.433 / 0.388 / 0.298 | lines 266-267 | VERIFIED |

Metric: within-problem AUROC. Lines 111-113: "Within-problem area under the receiver operating characteristic curve (AUC) measures how often a passing attempt receives a higher score than a failing attempt for the same problem. Scores are averaged across mixed problems." Line 488: "AUCs of held-out projections are averaged equally across mixed problems."

Same attempts: yes, within each model. Table 1 caption (lines 211-212): "Each model's probe and confidence scores use the same attempts; the two models use different cohorts (Appendix B)."

Readouts compared: probe = projection of the response-token-pooled residual-stream activation onto the difference of class means (lines 103-106); line 484: "Analysis uses DiffuCoder's last-step response-token mean and Qwen's completion-token mean." Confidence = negative token entropy and masked-forward score (DiffuCoder), completion log probability (Qwen). Line 494: "Diffusion confidence controls use mean visible-token log probability, negative mean visible-token entropy, and mean completion log probability with response positions masked."

Precision notes for vault wording:
1. The probe number is the maximum over layers of out-of-fold AUC, with no layer-selection holdout (lines 116-117: "We report the maximum AUC across the out-of-fold layer scores. Layer selection uses these same scores, without an additional holdout."). This biases the probe upward, so the Qwen deficit is not an artifact against the probe.
2. The paper makes no significance claims (lines 340: "We therefore compare point estimates rather than make significance or equivalence claims"). The bootstrap "merges repeated draws, losing the multiplicity required for a cluster bootstrap" (lines 338-339). The Qwen2.5-Coder size is not stated in the text; benchmark is MBPP+ (line 669). The DIGEST line 33 phrase "within-problem comparisons" is accurate.

## Item 2: Thinking-in-Bets, arXiv 2610.34654. Verdict: content of valid bug reports UNSPECIFIED in the paper

Finding: the paper never states what a valid bug report contains. No simulated-user or feedback-generation prompt is given. Appendix A.1 (lines 841-960) gives only agent-side prompts (claim book, adjudication note, confidence gate, Verify-Then-Respond, Post-Reply Gate, HLE Draft-First). Tables 8 and 13 give only counts and rates. Nothing says that a failing test case, test output, or execution trace is passed to the agent. The evidence that exists points to natural-language text from a simulated user, with the hidden test run privately by the harness.

Verbatim evidence:
- Line 465: "The agent writes and tests code across multiple turns with a simulated user on SWE-Together and SWE-Interact. Replies are cooperative clarifications, mistaken criticism with no failing case, or mixed feedback with equal shares of mistaken complaints and valid bug reports."
- Line 468: "In SWE-Pushback-Hidden, built on 110 DeepSWE tasks, the agent submits a patch before receiving a review complaint about one requirement. The harness privately runs a hidden test: the complaint is mistaken if the requirement passes and valid if it fails. In SWE-Interact mid-task Q&A, the user sends mostly valid bug reports while the agent is still coding (17 tasks)."
- Line 527: "Here, a reviewer challenges one requirement whose ground-truth validity is determined by the repository's hidden test suite."
- Line 543: "Our interactive experiments use simulated users whose mistaken criticism is usually a brief objection without a failing case; real users often mix valid and mistaken points in the same message."
- Line 2574: "SWE-Interact labels combine hidden tests with a model that checks requirements against the current code changes. A second model agrees on 496/506 sampled feedback labels (Cohen's κ = 0.963)." So validity in SWE-Interact is partly model-judged, not purely execution-defined.
- Line 2600 (only feedback example quoted, a mistaken one): "The cookie handling in DigestAuthWithCookies doesn't seem right. Redo it."
- Line 2587: "even a brief complaint can sometimes signal a real mistake, so λ(u_t | e_i) is not necessarily zero when a user provides no failing test case."
- Line 1501 (HLE, not code): "No hint and With hint report balanced accuracy under bare criticism vs. criticism with a concrete hint."

Tables 8 and 13:
- Table 8 caption (line 1502): "Coding results under mistaken criticism, cooperative feedback, hidden-test review, and mid-task questions." Notes (line 1800): "...invalid is the false-reversal rate on complaints where the challenged requirement already passed the hidden test. ... The last column reports ... the share of valid bug reports left unedited in Panel C." No description of the content of a report.
- Table 13 caption (line 2464): "Detailed mixed-feedback event counts and token overhead on SWE-Interact. Event denominators reflect eligible judged feedback turns; extra checklist tokens report Claim Checklist output tokens per trial." Columns (lines 2465-2479): task pass, false reversals, unjustified reversals, successful corrections, recurring-bug trials, balanced accuracy, extra checklist tokens. No description of content.

Implication for the Rank 3 novelty sentence: describe 2610.34654's valid feedback as "natural-language bug reports from a simulated user, whose validity is set by hidden tests (SWE-Pushback-Hidden) or by hidden tests combined with a model judge (SWE-Interact)". Do not say the agent sees a failing test or a trace. Do not say it does not see one either: the paper is silent on this.
