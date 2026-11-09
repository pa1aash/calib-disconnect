# Literature Review: Calibrated Uncertainty Communication in Coding Agents

## Summary

This review synthesizes 50+ papers across five facets: LLM calibration, coding agents, uncertainty in code generation, post-training alignment for code, and trust calibration in human-AI interaction.

Modern LLMs are consistently overconfident (Guo et al., 2017; Kadavath et al., 2022), and this problem is exacerbated after RLHF (Tian et al., 2023). For code specifically, Spiess et al. (ICSE 2025) provide the first rigorous study showing code LLMs are poorly calibrated—their token-level probabilities do not reliably predict functional correctness. Campos et al. (2025) extend this with multicalibration across code complexity subgroups.

Coding agents (SWE-Agent, OpenHands, AutoCodeRover) have made remarkable progress on benchmarks like SWE-bench, but studies of developer interaction (Vaithilingam et al., 2022; Mozannar et al., 2024) reveal a gap: developers struggle to calibrate trust because agents provide no confidence signals. This leads to both overtrust (accepting buggy code) and undertrust (rejecting correct code).

The trust calibration literature from HCI (Lee & See, 2004; Zhang et al., 2020; Yin et al., 2019) establishes that showing AI confidence can improve human decision-making, but only when confidence is well-calibrated. Poorly calibrated confidence can actively harm trust (Rechkemmer & Yin, 2022).

Post-training methods for code (CodeRL, GRPO, DPO) exploit code's unique verifiability through execution feedback. This suggests a path: use execution-based correctness as ground truth to train models to verbalize calibrated confidence.

## Key Findings by Facet

### Facet 1: LLM Calibration
- Modern neural networks are overconfident; temperature scaling is a simple but effective post-hoc fix (Guo et al., 2017)
- Pre-trained transformers are reasonably calibrated in-domain but degrade OOD (Desai & Durrett, 2020)
- LLMs can verbalize confidence, but verbalized probabilities are poorly calibrated without training (Xiong et al., 2024; Tian et al., 2023)
- Kadavath et al. (2022) show LLMs "mostly know what they know" — internal representations contain calibration signal
- RLHF makes models more sycophantic and less calibrated (Tian et al., 2023)
- Lin et al. (2022) show models can be taught to express uncertainty in words with supervised fine-tuning

### Facet 2: Coding Agents and Developer Interaction
- SWE-Agent (Yang et al., 2024): agent-computer interfaces are as important as model capability
- OpenHands (Wang et al., 2024): open platform for coding agents, 53% on SWE-bench Verified
- SWE-bench (Jimenez et al., 2024): standard benchmark for real-world software engineering
- Developer productivity studies show 55.8% faster completion with Copilot (Peng et al., 2023)
- Vaithilingam et al. (2022): gap between developer expectations and experience with Copilot
- Mozannar et al. (2024): developers use different strategies for verifying AI-generated code
- Critical gap: no work on confidence communication in coding agents

### Facet 3: Uncertainty in Code Generation
- Semantic uncertainty (Kuhn et al., 2023): cluster semantically equivalent outputs for better UQ
- pass@k (Chen et al., 2021): sampling multiple solutions dramatically improves solve rate
- CodeT (Chen et al., 2023): dual execution agreement provides strong correctness signal
- LEVER (Ni et al., 2023): learned verifiers over execution traces
- MPSC (Huang et al., 2023): multi-perspective self-consistency across code + NL + tests
- Spiess et al. (2025): first rigorous study of calibration for code LLMs; shows poor calibration
- Campos et al. (2025): multicalibration reveals subgroup-specific miscalibration

### Facet 4: Post-Training Alignment for Code
- CodeRL (Le et al., 2022): RL with execution feedback improves code generation
- GRPO (DeepSeek-R1, Shao et al., 2024): group relative policy optimization for reasoning/code
- DPO for code (CodeDPO): preference pairs from execution-validated solutions
- Reflexion (Shinn et al., 2023): verbal self-reflection on execution errors
- SelfCodeAlign (2024): fully self-generated instruction tuning without human labels

### Facet 5: Trust Calibration in Human-AI Interaction
- Trust in automation is multidimensional: performance, process, purpose (Lee & See, 2004)
- Showing AI confidence improves trust calibration, but only when confidence is accurate (Yin et al., 2019)
- Explanations don't reliably reduce overreliance (Bansal et al., 2021)
- Confidence + explanation together are more effective than either alone (Zhang et al., 2020)
- Cost-benefit framework explains when explanations succeed (Vasconcelos et al., 2023)
- Developer-specific: programmers use distinct modes (acceleration vs. exploration) (Mozannar et al., 2024)

## Identified Gaps & Opportunities

1. **No existing work trains code models to verbalize calibrated confidence** — the intersection of calibration training and code generation is unexplored
2. **Coding agents provide no uncertainty signals** — all output is presented with equal certainty
3. **Execution feedback provides cheap ground-truth** — code correctness can be automatically verified, providing training signal for calibration
4. **Trust calibration research shows confidence helps** — but only when well-calibrated, creating a clear optimization target
5. **Verbalized confidence is more natural than numeric scores** — Lin et al. (2022) show linguistic uncertainty is preferred by users
6. **Self-consistency across samples can be used as a proxy for confidence** — connecting pass@k with calibration

## Complete References
See methodology.md for full BibTeX entries used in the paper.
