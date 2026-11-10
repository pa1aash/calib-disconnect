---
library_name: vllm
language:
- en
- fr
- de
- es
- pt
- it
- ja
- ko
- ru
- zh
- ar
- fa
- id
- ms
- ne
- pl
- ro
- sr
- sv
- tr
- uk
- vi
- hi
- bn
license: apache-2.0
inference: false
extra_gated_description: >-
  If you want to learn more about how we process your personal data, please read
  our <a href="https://mistral.ai/terms/">Privacy Policy</a>.
tags:
- mistral-common
---

# Model Card for Mistral-Small-3.1-24B-Base-2503

Building upon Mistral Small 3 (2501), Mistral Small 3.1 (2503) **adds state-of-the-art vision understanding** and enhances **long context capabilities up to 128k tokens** without compromising text performance. 
With 24 billion parameters, this model achieves top-tier capabilities in both text and vision tasks.  
This model is the base model of [Mistral-Small-3.1-24B-Instruct-2503](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503).

For enterprises requiring specialized capabilities (increased context, specific modalities, domain-specific knowledge, etc.), we will release commercial models beyond what Mistral AI contributes to the community.

Learn more about Mistral Small 3.1 in our [blog post](https://mistral.ai/news/mistral-small-3-1/).

## Key Features
- **Vision:** Vision capabilities enable the model to analyze images and provide insights based on visual content in addition to text.
- **Multilingual:** Supports dozens of languages, including English, French, German, Greek, Hindi, Indonesian, Italian, Japanese, Korean, Malay, Nepali, Polish, Portuguese, Romanian, Russian, Serbian, Spanish, Swedish, Turkish, Ukrainian, Vietnamese, Arabic, Bengali, Chinese, Farshi.
- **Apache 2.0 License:** Open license allowing usage and modification for both commercial and non-commercial purposes.
- **Context Window:** A 128k context window.
- **Tokenizer:** Utilizes a Tekken tokenizer with a 131k vocabulary size.

## Benchmark Results

When available, we report numbers previously published by other model providers, otherwise we re-evaluate them using our own evaluation harness.

### Pretrain Evals

| Model                          | MMLU (5-shot) | MMLU Pro (5-shot CoT) | TriviaQA   | GPQA Main (5-shot CoT)| MMMU      |
|--------------------------------|---------------|-----------------------|------------|-----------------------|-----------|
| **Small 3.1 24B Base**         | **81.01%**    | **56.03%**            | 80.50%     | **37.50%**            | **59.27%**|
| Gemma 3 27B PT                 | 78.60%        | 52.20%                | **81.30%** | 24.30%                | 56.10%    |

## Usage Examples

### vLLM (recommended)

We recommend using Mistral-Small 3.1 Base with the [vLLM library](https://github.com/vllm-project/vllm).
_Note_ however that this is a pretrained-only checkpoint and thus not ready to work as an instruction model out-of-the-box.
For a production-ready instruction model please use [Mistral-Small-3.1-24B-Instruct-2503](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503).

**_Installation_**

We recommend using this model with the [vLLM library](https://github.com/vllm-project/vllm)
to implement production-ready inference pipelines.

Make sure you install [`vLLM >= 0.8.1`](https://github.com/vllm-project/vllm/releases/tag/v0.8.1):

```
pip install vllm --ugrade
```

Doing so should automatically install [`mistral_common >= 1.5.4`](https://github.com/mistralai/mistral-common/releases/tag/v1.5.4).

To check:
```
python -c "import mistral_common; print(mistral_common.__version__)"
```

You can also make use of a ready-to-go [docker image](https://github.com/vllm-project/vllm/blob/main/Dockerfile) or on the [docker hub](https://hub.docker.com/layers/vllm/vllm-openai/latest/images/sha256-de9032a92ffea7b5c007dad80b38fd44aac11eddc31c435f8e52f3b7404bbf39).

**_Example_**

```py
from vllm import LLM
from vllm.sampling_params import SamplingParams
from vllm.inputs.data import TokensPrompt
import requests
from PIL import Image
from io import BytesIO
from vllm.multimodal import MultiModalDataBuiltins

from mistral_common.protocol.instruct.messages import TextChunk, ImageURLChunk

model_name = "mistralai/Mistral-Small-3.1-24B-Base-2503"
sampling_params = SamplingParams(max_tokens=8192)

llm = LLM(model=model_name, tokenizer_mode="mistral")

url = "https://huggingface.co/datasets/patrickvonplaten/random_img/resolve/main/yosemite.png"
response = requests.get(url)
image = Image.open(BytesIO(response.content))

prompt = "The image shows a"

user_content = [ImageURLChunk(image_url=url), TextChunk(text=prompt)]

tokenizer = llm.llm_engine.tokenizer.tokenizer.mistral.instruct_tokenizer
tokens, _ = tokenizer.encode_user_content(user_content, False)

prompt = TokensPrompt(
    prompt_token_ids=tokens, multi_modal_data=MultiModalDataBuiltins(image=[image])
)
outputs = llm.generate(prompt, sampling_params=sampling_params)

print(outputs[0].outputs[0].text)
# ' scene in Yosemite Valley and was taken at ISO 250 with an aperture of f/16 and a shutter speed of 1/18 second. ...'
```

### Transformers (untested)

Transformers-compatible model weights are also uploaded (thanks a lot @cyrilvallez). 
However the transformers implementation was **not throughly tested**, but only on "vibe-checks".
Hence, we can only ensure 100% correct behavior when using the original weight format with vllm (see above).