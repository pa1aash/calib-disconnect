---
library_name: transformers
language:
- ar
- cs
- de
- en
- es
- fr
- hi
- it
- ja
- ko
- nl
- pl
- pt
- ro
- ru
- sv
- ur
- zh
tags:
- falcon-h1
license: other
license_name: falcon-llm-license
license_link: https://falconllm.tii.ae/falcon-terms-and-conditions.html
---

<img src="https://huggingface.co/datasets/tiiuae/documentation-images/resolve/main/falcon_mamba/falcon-h1-logo.png" alt="drawing" width="800"/>

#  Table of Contents

0. [TL;DR](#TL;DR)
1. [Model Details](#model-details)
2. [Training Details](#training-details)
3. [Usage](#usage)
4. [Evaluation](#evaluation)
5. [Citation](#citation)

# TL;DR

# Model Details

## Model Description

- **Developed by:** [https://www.tii.ae](https://www.tii.ae)
- **Model type:** Causal decoder-only
- **Architecture:** Hybrid Transformers + Mamba architecture
- **Language(s) (NLP):** English, Multilingual
- **License:** Falcon-LLM License

# Training details

For more details about the training protocol of this model, please refer to the [Falcon-H1 technical blogpost](https://falcon-lm.github.io/blog/falcon-h1/) and [Technical Report](https://arxiv.org/abs/2507.22448).

# Usage

Currently to use this model you can either rely on Hugging Face `transformers`, `vLLM` or `llama.cpp` library.

## Inference

Make sure to install the latest version of `transformers` or `vllm`, eventually install these packages from source:

```bash
pip install git+https://github.com/huggingface/transformers.git
```

For vLLM, make sure to install `vllm>=0.9.0`:

```bash
pip install "vllm>=0.9.0"
```

### 🤗 transformers

Refer to the snippet below to run H1 models using 🤗 transformers:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "tiiuae/Falcon-H1-1B-Base"

model = AutoModelForCausalLM.from_pretrained(
  model_id,
  torch_dtype=torch.bfloat16,
  device_map="auto"
)

# Perform text generation
```

### vLLM

For vLLM, simply start a server by executing the command below:

```
# pip install vllm>=0.9.0
vllm serve tiiuae/Falcon-H1-1B-Instruct --tensor-parallel-size 2 --data-parallel-size 1
```

### `llama.cpp`

You can find all GGUF files under [our official collection](https://huggingface.co/collections/tiiuae/falcon-h1-6819f2795bc406da60fab8df)

# Evaluation

Falcon-H1 series perform very well on a variety of tasks, including reasoning tasks. 

| Tasks | Falcon-H1-34B | Qwen2.5-72B | Qwen2.5-32B | Gemma3-27B | Llama3.1-70B | Llama4-scout |
| --- | --- | --- | --- | --- | --- | --- |
| **General**  | | | | | |
| BBH | **69.36** | 67.77 | 67.45 | 61.6 | 62.78 | 61.71 |
| MMLU | 83.46 | **85.96** | 83.18 | 78.32 | 78.49 | 77.98 |
| ARC-C | 71.25 | **72.44** | 70.48 | 70.31 | 69.2 | 62.97 |
| HellaSwag | 85.68 | 87.57 | 85.13 | 86.19 | **87.78** | 84.01 |
| Winogrande | 82.72 | 83.74 | 82.32 | 82.4 | **85.32** | 78.93 |
| **Math**  | | | | | |
| GSM8k | 76.5 | 89.76 | **90.14** | 81.35 | 80.52 | 83.24 |
| MATH lvl5 | **40.71** | 38.14 | 36.4 | 25.38 | 18.81 | 27.19 |
| **Science**  | | | | | |
| GPQA | **42.7** | 42.28 | 39.68 | 35.82 | 36.49 | 35.99 |
| MMLU-Pro | 57.18 | **60.22** | 58.05 | 49.64 | 47.07 | 50.16 |
| MMLU-stem | 83.82 | **84.81** | 82.81 | 76.59 | 70.35 | 72.57 |
| **Code**  | | | | | |
| HumanEval | **70.12** | 59.15 | 59.76 | 48.78 | 57.32 | 57.32 |
| HumanEval+ | **64.63** | 51.22 | 51.83 | 40.85 | 50.61 | 48.78 |
| MBPP | 83.33 | **87.04** | 83.07 | 76.19 | 78.84 | 77.78 |
| MBPP+ | 70.37 | **70.63** | 68.78 | 61.64 | 66.67 | 64.29 |

You can check more in detail on our [our release blogpost](https://falcon-lm.github.io/blog/falcon-h1/), detailed benchmarks.

# Useful links

- View [our release blogpost](https://falcon-lm.github.io/blog/falcon-h1/).
- View [our technical report](https://arxiv.org/abs/2507.22448).
- Feel free to join [our discord server](https://discord.gg/trwMYP9PYm) if you have any questions or to interact with our researchers and developers.

# Citation

If the Falcon-H1 family of models were helpful to your work, feel free to give us a cite.

```
@article{falconh1,
    title={Falcon-H1: A Family of Hybrid-Head Language Models Redefining Efficiency and Performance},
    author={Jingwei Zuo and Maksim Velikanov and Ilyas Chahed and Younes Belkada and Dhia Eddine Rhayem and Guillaume Kunsch and Hakim Hacid and Hamza Yous and Brahim Farhat and Ibrahim Khadraoui and Mugariya Farooq and Giulia Campesan and Ruxandra Cojocaru and Yasser Djilali and Shi Hu and Iheb Chaabane and Puneesh Khanna and Mohamed El Amine Seddik and Ngoc Dung Huynh and Phuc Le Khac and Leen AlQadi and Billel Mokeddem and Mohamed Chami and Abdalgader Abubaker and Mikhail Lubinets and Kacper Piskorski and Slim Frikha},
    journal = {arXiv preprint arXiv:2507.22448},
    year={2025}
}
```