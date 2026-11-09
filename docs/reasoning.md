# Research Deliberation: Calibrated Uncertainty Communication in Coding Agents

## Knowledge Consolidation

The literature reveals a clear convergence of findings: (1) code LLMs are poorly calibrated, (2) coding agents provide no confidence signals to developers, (3) developers struggle with trust calibration, and (4) showing well-calibrated confidence improves human-AI collaboration. The missing piece is a method that connects these: training code models to produce calibrated verbal confidence that developers can act on.

Code's unique advantage is verifiability — we can automatically check correctness through execution, giving us cheap ground-truth labels for whether the model "should have been confident." This is a much cleaner signal than general NLP tasks where correctness is subjective.

## Knowledge Gaps & Contradictions

- **Gap 1**: No method exists for training code LLMs to verbalize calibrated confidence
- **Gap 2**: No benchmark measures interaction quality with confidence-aware coding agents
- **Gap 3**: Unclear whether logit-based, sampling-based, or verbalized confidence works best for code
- **Contradiction**: Bansal et al. (2021) show explanations don't reduce overreliance, but Zhang et al. (2020) show confidence + explanation helps — the difference may be calibration quality

## Candidate Hypotheses

### Hypothesis 1: DPO on confidence-annotated code pairs improves calibration
- **Statement**: Training a code LLM with DPO on pairs where the preferred response includes accurate verbal confidence (matched to execution outcomes) will produce a model with significantly better calibration than the base model, while maintaining code quality.
- Null hypothesis: DPO-trained model shows no improvement in calibration (ECE) vs. base model
- Required evidence: ECE reduction on held-out coding benchmarks
- Feasibility: HIGH — we can generate training data automatically using execution feedback
- Novelty: HIGH — no prior work on DPO for confidence calibration in code
- If confirmed: opens a new direction for human-centered coding agents
- If refuted: suggests calibration may need different training signals

### Hypothesis 2: Self-consistency sampling provides a better confidence signal than logits
- **Statement**: Confidence derived from agreement across multiple sampled solutions (self-consistency) is better calibrated than token-level logit probabilities for code generation.
- Null hypothesis: Logit-based confidence has equal or better calibration than sampling-based
- Required evidence: Comparison of ECE for both methods across benchmarks
- Feasibility: HIGH — can be measured directly
- Novelty: MEDIUM — extends Kuhn et al. (2023) to code domain specifically
- If confirmed: validates using sampling-based confidence as the training signal
- If refuted: use logit-based confidence instead

### Hypothesis 3: Verbalized confidence improves developer trust calibration
- **Statement**: When a coding agent provides well-calibrated verbal confidence (e.g., "I'm confident this is correct" vs. "Please verify this edge case"), simulated developer decision-making shows better trust calibration (fewer overtrust and undertrust errors).
- Null hypothesis: Verbal confidence provides no improvement over no-confidence baseline
- Required evidence: Simulated user study using LLM-as-judge for trust decisions
- Feasibility: MEDIUM — simulated study is feasible; real user study is not in scope
- Novelty: HIGH — no prior work on verbal confidence for code agents

## Structured Deliberation

| Hypothesis | Strengths | Weaknesses | Key Uncertainty | Information Gain |
|------------|-----------|------------|-----------------|-----------------|
| H1: DPO for calibration | Novel, executable, directly actionable | DPO may not suffice for calibration | Whether DPO signal is strong enough | Very high — new method |
| H2: Self-consistency vs logits | Clean comparison, grounded in theory | Incremental contribution alone | Compute cost of sampling | Medium — extends prior work |
| H3: Trust improvement | Directly addresses DL4C theme | Simulated study has limitations | Simulated vs. real users | High — practical impact |

## Selected Direction

**Chosen: All three hypotheses form a coherent paper.** H2 establishes the confidence signal, H1 introduces the training method, H3 evaluates the downstream impact. This creates a complete story:

1. **Measure** existing calibration of code LLMs (confirming the problem)
2. **Compare** confidence estimation methods for code (logits vs. sampling — H2)
3. **Train** with DPO to improve verbalized calibration (H1)
4. **Evaluate** downstream impact on trust calibration (H3)

**Rationale**: This combines a novel training method (DPO for code confidence calibration) with practical evaluation (trust calibration), directly addressing DL4C's human-centered coding agents theme.

**Key risks**: 
- DPO training may not converge or may hurt code quality
- Simulated user study may not generalize to real developers

**Pre-specified success criteria**:
- ECE (Expected Calibration Error) reduction of ≥5% absolute on HumanEval/MBPP
- Code quality (pass@1) maintained within 2% of base model
- Simulated trust calibration improvement measurable

**Fallback plan**: If DPO doesn't work, try supervised fine-tuning on confidence-annotated data. If calibration doesn't improve, focus paper on the measurement and analysis contribution.
