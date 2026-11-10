---
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen3-Coder-Next-Base/blob/main/LICENSE
pipeline_tag: text-generation
---

# Qwen3-Coder-Next-Base

## Highlights

Today, we're announcing **Qwen3-Coder-Next-Base**, an open-weight language model designed specifically for coding agents and local development. It features the following key enhancements:  

- **Advanced architecture**: It integrates the Hybrid Attention with highly sparse MoE, enabling high throughput and strong ultra-long-context modeling.

- **Robust data foundation**: Trained on highly diverse, broad-coverage corpora, with native 256K context and support for 370+ languages, it leaves ample headroom for post-training.

- **Agentic coding capability**: With a carefully designed training recipe, it has strong capabilities in tool calling, scaffold/template adaptation, and error detection/recovery, making it a strong backbone for reliable coding agents.

## Model Overview

**Qwen3-Coder-Next-Base** has the following features:
- Type: Causal Language Models
- Training Stage: Pretraining
- Number of Parameters: 80B in total and 3B activated
- Number of Parameters (Non-Embedding): 79B
- Hidden Dimension: 2048
- Number of Layers: 48
  - Hybrid Layout: 12 \* (3 \* (Gated DeltaNet -> MoE) -> 1 \* (Gated Attention -> MoE))
- Gated Attention:
  - Number of Attention Heads: 16 for Q and 2 for KV
  - Head Dimension: 256
  - Rotary Position Embedding Dimension: 64
- Gated DeltaNet:
  - Number of Linear Attention Heads: 32 for V and 16 for QK
  - Head Dimension: 128
- Mixture of Experts:
  - Number of Experts: 512
  - Number of Activated Experts: 10
  - Number of Shared Experts: 1
  - Expert Intermediate Dimension: 512
- Context Length: 262,144 natively

**NOTE: This model supports only non-thinking mode and does not generate ``<think></think>`` blocks in its output. Meanwhile, specifying `enable_thinking=False` is no longer required.**

For more details, including benchmark evaluation, hardware requirements, and inference performance, please refer to our [blog](https://qwen.ai/blog?id=qwen3-coder-next), [GitHub](https://github.com/QwenLM/Qwen3-Coder), and [Documentation](https://qwen.readthedocs.io/en/latest/).

## Best Practices

To achieve optimal performance, we recommend the following sampling parameters: `temperature=1.0`, `top_p=0.95`, `top_k=40`.


## Citation

If you find our work helpful, feel free to give us a cite.

```
@techreport{qwen_qwen3_coder_next_tech_report,
  title        = {Qwen3-Coder-Next Technical Report},
  author       = {{Qwen Team}},
  url          = {https://github.com/QwenLM/Qwen3-Coder/blob/main/qwen3_coder_next_tech_report.pdf},
  note         = {Accessed: 2026-02-03}
}
```