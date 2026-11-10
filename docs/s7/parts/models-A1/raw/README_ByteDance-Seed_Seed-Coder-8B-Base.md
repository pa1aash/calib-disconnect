---
license: mit
library_name: transformers
pipeline_tag: text-generation
---

# Seed-Coder-8B-Base

<div align="left" style="line-height: 1;">
  <a href="https://bytedance-seed-coder.github.io/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://img.shields.io/badge/Seed--Coder-Homepage-a468fe?color=a468fe&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>

  <a href="https://arxiv.org/abs/2506.03524" target="_blank" style="margin: 2px;">
    <img alt="Technical Report" src="https://img.shields.io/badge/arXiv-Technical%20Report-brightgreen?logo=arxiv&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  
  <a href="https://huggingface.co/ByteDance-Seed" target="_blank" style="margin: 2px;">
      <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-ByteDance%20Seed-536af5?color=536af5&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  
  <a href="https://github.com/ByteDance-Seed/Seed-Coder/blob/master/LICENSE" style="margin: 2px;">
      <img alt="License" src="https://img.shields.io/badge/License-MIT-f5de53?color=f5de53&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>


## Introduction
We are thrilled to introduce Seed-Coder, a powerful, transparent, and parameter-efficient family of open-source code models at the 8B scale, featuring base, instruct, and reasoning variants. Seed-Coder contributes to promote the evolution of open code models through the following highlights.

- **Model-centric:** Seed-Coder predominantly leverages LLMs instead of hand-crafted rules for code data filtering, minimizing manual effort in pretraining data construction.
- **Transparent:** We openly share detailed insights into our model-centric data pipeline, including methods for curating GitHub data, commits data, and code-related web data.
- **Powerful:** Seed-Coder achieves state-of-the-art performance among open-source models of comparable size across a diverse range of coding tasks.

<p align="center">
  <img width="100%" src="imgs/seed-coder_intro_performance.png">
</p>

This repo contains the **Seed-Coder-8B-Base** model, with the following features:
- Type: Causal language models
- Training Stage: Pretraining
- Data Source: GitHub data, code-related web data
- Training Tokens: 6 trillion
- Supports: Code completion, code infilling (Fill-in-the-Middle)
- Context Length: 32,768


## Model Downloads
| Model Name                  | Length | Download   |    Notes |
|---------------------------------------------------------|--------|------------------------------------|-----------------------|
| 👉 **Seed-Coder-8B-Base**           | 32K    | 🤗 [Model](https://huggingface.co/ByteDance-Seed/Seed-Coder-8B-Base)   |  Pretrained on our model-centric code data.  |
| Seed-Coder-8B-Instruct             | 32K    | 🤗 [Model](https://huggingface.co/ByteDance-Seed/Seed-Coder-8B-Instruct)   |  Instruction-tuned for alignment with user intent. |
| Seed-Coder-8B-Reasoning            | 64K    | 🤗 [Model](https://huggingface.co/ByteDance-Seed/Seed-Coder-8B-Reasoning)   |  RL trained to boost reasoning capabilities.  |
| Seed-Coder-8B-Reasoning-bf16 | 64K    | 🤗 [Model](https://huggingface.co/ByteDance-Seed/Seed-Coder-8B-Reasoning-bf16)   |  RL trained to boost reasoning capabilities.  |


## Requirements
You will need to install the latest versions of `transformers` and `accelerate`:

```bash
pip install -U transformers accelerate
```

## Quickstart

Here is a simple example demonstrating how to load the model and perform code generation using the Hugging Face `pipeline` API:

```python
import transformers
import torch

model_id = "ByteDance-Seed/Seed-Coder-8B-Base"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

output = pipeline("def say_hello_world():", max_new_tokens=100)
print(output[0]["generated_text"])
```

### Fill-in-the-Middle (FIM) Example

Seed-Coder-8B-Base natively supports **Fill-in-the-Middle (FIM)** tasks, where the model is given a prefix and a suffix and asked to predict the missing middle content. This allows for code infilling scenarios such as completing a function body or inserting missing logic between two pieces of code.

A typical example:

```python
import transformers
import torch

model_id = "ByteDance-Seed/Seed-Coder-8B-Base"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

# You can concatenate a prefix, a special FIM separator token, and a suffix
prefix = "def add_numbers(a, b):\n    "
suffix = "\n    return result"

# Combine prefix and suffix following the FIM format
fim_input = '<[fim-suffix]>' + suffix + '<[fim-prefix]>' + prefix + '<[fim-middle]>'

output = pipeline(fim_input, max_new_tokens=512)
print(output[0]["generated_text"])
```

## Evaluation

Seed-Coder-8B-Base has been evaluated on code generation, code completion, and code reasoning benchmarks, achieving state-of-the-art performance among ~8B open-source models.

|            | DeepSeek-Coder-6.7B-Base | OpenCoder-8B-Base | Qwen2.5-Coder-7B | Seed-Coder-8B-Base |
|------------|:------------------------:|:-----------------:|:----------------:|:------------------:|
| HumanEval  |           47.6           |        66.5       |       72.0       |        **77.4**        |
| MBPP       |           70.2           |        79.9       |       79.4       |        **82.0**        |
| MultiPL-E  |           44.7           |        61.0       |       58.8       |        **67.6**        |
| cruxeval-O |           41.0           |        43.9       |       **56.0**       |        54.8        |

For detailed benchmark performance, please refer to our [📑 Technical Report](https://github.com/ByteDance-Seed/Seed-Coder/blob/master/Seed-Coder.pdf).


## License

This project is licensed under the MIT License. See the [LICENSE file](https://github.com/ByteDance-Seed/Seed-Coder/blob/master/LICENSE) for details.

## Citation

If you find Seed-Coder helpful, please consider citing our work:

```
@misc{seed2025seedcoderletcodemodel,
      title={{Seed-Coder}: Let the Code Model Curate Data for Itself}, 
      author={{ByteDance Seed} and Yuyu Zhang and Jing Su and Yifan Sun and Chenguang Xi and Xia Xiao and Shen Zheng and Anxiang Zhang and Kaibo Liu and Daoguang Zan and Tao Sun and Jinhua Zhu and Shulin Xin and Dong Huang and Yetao Bai and Lixin Dong and Chao Li and Jianchong Chen and Hanzhi Zhou and Yifan Huang and Guanghan Ning and Xierui Song and Jiaze Chen and Siyao Liu and Kai Shen and Liang Xiang and Yonghui Wu},
      year={2025},
      eprint={2506.03524},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2506.03524}, 
}
``` 