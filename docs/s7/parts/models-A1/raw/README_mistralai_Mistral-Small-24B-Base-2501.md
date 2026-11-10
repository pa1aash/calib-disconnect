---
library_name: vllm
language:
- en
- fr
- de
- es
- it
- pt
- zh
- ja
- ru
- ko
license: apache-2.0
inference: false
extra_gated_description: >-
  If you want to learn more about how we process your personal data, please read
  our <a href="https://mistral.ai/terms/">Privacy Policy</a>.
tags:
- mistral-common
---

# Model Card for Mistral-Small-24B-Base-2501

Mistral Small 3 ( 2501 ) sets a new benchmark in the "small" Large Language Models category below 70B, boasting 24B parameters and achieving state-of-the-art capabilities comparable to larger models!  
Check out our fine-tuned Instruct version [Mistral-Small-24B-Instruct-2501](https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501).

For enterprises that need specialized capabilities (increased context, particular modalities, domain specific knowledge, etc.), we will be releasing commercial models beyond what Mistral AI contributes to the community.

This release demonstrates our commitment to open source, serving as a strong base model. 

Learn more about Mistral Small in our [blog post](https://mistral.ai/news/mistral-small-3/).

Model developper: Mistral AI Team

## Key Features
- **Multilingual:** Supports dozens of languages, including English, French, German, Spanish, Italian, Chinese, Japanese, Korean, Portuguese, Dutch, and Polish.
- **Advanced Reasoning:** State-of-the-art conversational and reasoning capabilities.
- **Apache 2.0 License:** Open license allowing usage and modification for both commercial and non-commercial purposes.
- **Context Window:** A 32k context window.
- **Tokenizer:** Utilizes a Tekken tokenizer with a 131k vocabulary size.

## Benchmark Results

| Benchmark                      | Metric        | Mistral-Small-24B-Base |
| ------------------------------ | ------------- | ----------- |
| [MMLU][mmlu]                   | 5-shot        | 80.73        |
| [MMLU Pro][mmlu_pro]         | 5-shot, CoT       | 54.37        |
| [GPQA Main][gpqa]                   | 5-shot, CoT        | 34.37        |
| [TriviaQA][triviaqa]         | 5-shot        | 80.32      |
| [ARC-c][arc]                   | 0-shot       | 91.29        |
| [TriviaQA][triviaqa]           | 5-shot        | 76.6        |
| [MBPP][mbpp]                   | pass@1        | 69.64        |
| [GSM8K][gsm8k]                 | 5-shot, maj@1 | 80.73        |
| [MATH][math]                   | 4-shot, MaJ        | 45.98        |
| [AGIEval][agieval]             | -      | 65.80        |

| Benchmark                      | Metric        | Mistral-Small-24B-Base |
| ------------------------------ | ------------- | ----------- |
| French MMLU                    | -             | 78.03        |
| German MMLU                    | -             | 77.69        |
| Spanish MMLU                   | -             | 78.86        |
| Russian MMLU                   | -             | 75.64        |
| Chinese MMLU                   | -             | 70.35        |
| Korean MMLU                    | -             | 56.42        |
| Japanese MMLU                  | -             | 74.46        |


[mmlu]: https://arxiv.org/abs/2009.03300
[hellaswag]: https://arxiv.org/abs/1905.07830
[piqa]: https://arxiv.org/abs/1911.11641
[socialiqa]: https://arxiv.org/abs/1904.09728
[boolq]: https://arxiv.org/abs/1905.10044
[winogrande]: https://arxiv.org/abs/1907.10641
[commonsenseqa]: https://arxiv.org/abs/1811.00937
[openbookqa]: https://arxiv.org/abs/1809.02789
[arc]: https://arxiv.org/abs/1911.01547
[triviaqa]: https://arxiv.org/abs/1705.03551
[naturalq]: https://github.com/google-research-datasets/natural-questions
[humaneval]: https://arxiv.org/abs/2107.03374
[mbpp]: https://arxiv.org/abs/2108.07732
[gsm8k]: https://arxiv.org/abs/2110.14168
[realtox]: https://arxiv.org/abs/2009.11462
[bold]: https://arxiv.org/abs/2101.11718
[crows]: https://aclanthology.org/2020.emnlp-main.154/
[bbq]: https://arxiv.org/abs/2110.08193v2
[winogender]: https://arxiv.org/abs/1804.09301
[truthfulqa]: https://arxiv.org/abs/2109.07958
[winobias]: https://arxiv.org/abs/1804.06876
[math]: https://arxiv.org/abs/2103.03874
[agieval]: https://arxiv.org/abs/2304.06364
[big-bench]: https://arxiv.org/abs/2206.04615
[toxigen]: https://arxiv.org/abs/2203.09509
[mmlu_pro]: https://arxiv.org/abs/2406.01574
[gpqa]: https://arxiv.org/abs/2311.12022