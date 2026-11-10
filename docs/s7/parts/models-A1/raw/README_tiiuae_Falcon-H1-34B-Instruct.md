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
base_model: tiiuae/Falcon-H1-34B-Base
inference: true
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

| Tasks | Falcon-H1-34B | Qwen3-32B | Qwen2.5-72B | Qwen2.5-32B | Gemma3-27B | Llama3.3-70B | Llama4-scout |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **General**  | | | | | | |
| BBH | 70.68 | 62.47 | **72.52** | 68.72 | 67.28 | 69.15 | 64.9 |
| ARC-C | 61.01 | 48.98 | 46.59 | 44.54 | 54.52 | **63.65** | 56.14 |
| TruthfulQA | 65.27 | 58.58 | 69.8 | **70.28** | 64.26 | 66.15 | 62.74 |
| HellaSwag | **81.94** | 68.89 | 68.79 | 73.95 | 57.25 | 70.24 | 65.03 |
| MMLU | 84.05 | 80.89 | **84.42** | 82.8 | 78.01 | 82.08 | 80.4 |
| **Math**  | | | | | | |
| GSM8k | 83.62 | 88.78 | 82.26 | 78.47 | 90.37 | **93.71** | 90.37 |
| MATH-500 | 83.8 | 82.0 | 83.6 | 82.2 | **90.0** | 70.6 | 83.2 |
| AMC-23 | 69.38 | 67.34 | 67.34 | 68.75 | **77.81** | 39.38 | 69.06 |
| AIME-24 | 23.75 | 27.71 | 17.29 | 17.92 | 27.5 | 12.92 | **27.92** |
| AIME-25 | 16.67 | 19.79 | 15.21 | 11.46 | **22.71** | 1.25 | 8.96 |
| **Science**  | | | | | | |
| GPQA | **41.53** | 30.2 | 37.67 | 34.31 | 36.49 | 31.99 | 31.8 |
| GPQA_Diamond | 49.66 | 49.49 | 44.95 | 40.74 | 47.47 | 42.09 | **51.18** |
| MMLU-Pro | **58.73** | 54.68 | 56.35 | 56.63 | 47.81 | 53.29 | 55.58 |
| MMLU-stem | **83.57** | 81.64 | 82.59 | 82.37 | 73.55 | 74.88 | 75.2 |
| **Code**  | | | | | | |
| HumanEval | 87.2 | **90.85** | 87.2 | 90.24 | 86.59 | 83.53 | 85.4 |
| HumanEval+ | 81.71 | **85.37** | 80.49 | 82.32 | 78.05 | 79.87 | 78.7 |
| MBPP | 83.86 | 86.24 | **89.68** | 87.83 | 88.36 | 88.09 | 81.5 |
| MBPP+ | 71.43 | 71.96 | **75.4** | 74.07 | 74.07 | 73.81 | 64.8 |
| LiveCodeBench | 49.71 | 45.01 | **54.6** | 49.12 | 39.53 | 40.31 | 40.12 |
| CRUXEval | 73.07 | **78.45** | 75.63 | 73.5 | 74.82 | 69.53 | 68.32 |
| **Instruction Following**  | | | | | | |
| IFEval | 89.37 | 86.97 | 86.35 | 81.79 | 83.19 | **89.94** | 86.32 |
| Alpaca-Eval | 48.32 | **64.21** | 49.29 | 39.26 | 56.16 | 38.27 | 36.26 |
| MTBench | **9.2** | 9.05 | 9.16 | 9.09 | 8.75 | 8.98 | 8.98 |
| LiveBench | 46.26 | **63.05** | 54.03 | 52.92 | 55.41 | 53.11 | 54.21 |

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