# Critic B (budget and feasibility, sonnet): findings on PIPELINE_DESIGN_R0.md

Saved by the orchestrator from the critic's returned text (the critic's own write was rejected). The critic checked the arithmetic by hand; no network, no code run.

**Recomputation.** The section 12.2 rows and the 132.4 h total reproduce; 1.2 x 132.4 = 158.9 h. The 17 conditions, 15,970 samples per model, and 62.4 GB of hidden-state storage (actual hidden sizes from the saved model configs) check out. No blocker.

## Findings

- **F1 (major).** Hardware and prices are not given, so throughput cannot be judged. The prefill rates imply about 230 to 250 TFLOP/s sustained.
- **F2 (major).** Thinking-on stages are 42.5 h and rest on an unsourced 6,000-token mean; each +1,000 tokens adds about 6.3 h.
- **F3 (major).** LoRA scoring and validation are short by about 12.9 h; reading-B scoring is missing (about 1.7 h).
- **F4 (major).** Probe fits (about 216,000 logistic fits) and the bootstrap have no CPU budget.
- **F5 (minor).** The V1 allowance of 1.0 h depends on an unstated engine; it could be about 10 h.
- **F6 (major).** The LiveCodeBench label-analog refits are omitted, about 29 h.
- **F7 (major).** The K7 cuts recover at most about 32 h against a trigger of 66 h or more; they also remove primary models; K7 is used for two different things (kill criterion and risk ID).
- **F8 (major).** The pilot (one 7B model) misses 67 percent of the cost: all 32B and all thinking-on stages.
- **F9 (minor).** The cost-minimizing claim is unshown: k = 8 would save about 25 h; the contingency is not derived.
- **F10 (major).** The reference-solution check is impossible on LiveCodeBench, which has no canonical solutions.
- **F11 (minor).** Execution-cost inputs are unsupported.
- **F12 (minor).** The generation-shift row double counts fresh samples.
- **F13 (minor).** The weights cache (about 544 GB) and the float16 storage format are unaddressed.
- **F14 (minor).** LoRA early stopping is inert.

**Corrected GPU total (critic).** About 185 h before contingency and about 222 h with 20 percent contingency, leaving about 14 h of headroom to the K7 trigger.
