# models-A1: third model family and rebalanced matrix

Wave 7, sub-agent models-A1. Retrieved 2026-11-10 by headless curl (desktop user agent, no authentication) from huggingface.co, github.com, arxiv.org, and export.arxiv.org. No weights downloaded. Every fetched page is saved verbatim in `raw/`; URLs and dates are in `SOURCES.md`.

Conventions (same as wave 6 B3):

- Revision is the `sha` field of `https://huggingface.co/api/models/<id>` (or `/revision/main`) at retrieval. Pin by `revision=<sha>`.
- Params is `safetensors.total` from the API. bf16 GB = 2 bytes x params; FP8 GB = 1 byte x params (decimal GB, weights only; KV cache and activations are extra). For multimodal checkpoints the count includes the vision or audio encoder.
- "UB" (upper bound) is the repository `createdAt` date. It is not a cutoff; it is used only when no cutoff is stated.
- ISO cutoff dates: a stated month is converted to the last day of that month (conservative for the post-cutoff count); a stated day is used as is.
- "not stated" means the card and the report named in the cell were searched and gave no value.

## 1. Candidate third families: facts

### 1.1 Repositories, revisions, licence, size, cutoff

| Family | Repository ID | Revision (main) | createdAt | Gated | Licence (cardData) | Params | bf16 / FP8 GB | Architecture | Stated cutoff (quote, source) |
|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 | google/gemma-4-12B | 1a2c7729392586f5ecddae8807ee2ef741eabb9a | 2026-05-23 | no | apache-2.0 | 11,959,730,224 | 23.9 / 12.0 | Gemma4UnifiedForConditionalGeneration | "with a cutoff date of January 2025" (card, Training Dataset; arXiv 2607.02770 Sec 2.4 "Training data") |
| Gemma 4 | google/gemma-4-12B-it | 43c9d014b231474fa7212dbb48a762566c2b255d | 2026-05-23 | no | apache-2.0 | 11,959,730,224 | 23.9 / 12.0 | Gemma4UnifiedForConditionalGeneration | as above |
| Gemma 4 | google/gemma-4-31B | 5bbc2fb1c1b2c611d06e3d9f23c170ba21659d89 | 2026-03-12 | no | apache-2.0 | 31,273,088,876 | 62.5 / 31.3 | Gemma4ForConditionalGeneration | as above |
| Gemma 4 | google/gemma-4-31B-it | 842da3794eaa0b77d5f08bae87a17459d91ff475 | 2026-03-11 | no | apache-2.0 | 31,273,088,876 | 62.5 / 31.3 | Gemma4ForConditionalGeneration | as above |
| Gemma 4 (MoE, not proposed) | google/gemma-4-26B-A4B / -it | 24548b62aa021d562695c04aaf7758a1ea47990b / 4d7ae4984b7db7de8f8457170b3f1a419ee76d52 | 2026-03-12 / 2026-03-11 | no | apache-2.0 | 25,805,936,206 | 51.6 / 25.8 | Gemma4ForConditionalGeneration | as above |
| IBM Granite 4.1 | ibm-granite/granite-4.1-8b-base | cbc32f94fbf8179ca4b22b664831f6a73965bb16 | 2026-04-06 | no | apache-2.0 | 8,380,551,168 | 16.8 / 8.4 | GraniteForCausalLM | not stated (card, GitHub granite-4.1-language-models README); UB 2026-04-06 |
| IBM Granite 4.1 | ibm-granite/granite-4.1-8b | 1504002f650e656a0a3789d99574df12e3e94ed0 | 2026-04-06 | no | apache-2.0 | 8,791,592,960 | 17.6 / 8.8 | GraniteForCausalLM | not stated; UB 2026-04-06 |
| IBM Granite 4.1 | ibm-granite/granite-4.1-30b-base | 9bb22a92d17f4a51788c4750d32764ed068d94f2 | 2026-04-06 | no | apache-2.0 | 28,865,728,512 | 57.7 / 28.9 | GraniteForCausalLM | not stated; UB 2026-04-06 |
| IBM Granite 4.1 | ibm-granite/granite-4.1-30b | 4fae6278f7132abf5e971f9de49ebbad09c54cce | 2026-04-06 | no | apache-2.0 | 28,865,728,512 | 57.7 / 28.9 | GraniteForCausalLM | not stated; UB 2026-04-06 |
| IBM Granite 4.2 (thinking, on 4.1 base) | ibm-granite/granite-4.2-8b | a7042144125ce5ae64f89610e8289647fc000b9a | 2026-08-07 | no | apache-2.0 | 8,791,592,960 | 17.6 / 8.8 | GraniteForCausalLM | not stated; UB 2026-08-07 |
| IBM Granite 4.2 | ibm-granite/granite-4.2-30b | 9e668ce1c538387ef24d3644e9b0606647762636 | 2026-08-07 | no | apache-2.0 | 29,276,770,304 | 58.6 / 29.3 | GraniteForCausalLM | not stated; UB 2026-08-07 |
| IBM Granite 4.0 (hybrid MoE) | ibm-granite/granite-4.0-h-small-base / -h-small | 4b4faa80c56f74d6fbd8ff305646aa32dd53d600 / b8c0982bab7fde4eb48110f5a069527c008fab39 | 2025-09-16 | no | apache-2.0 | 32,207,337,984 | 64.4 / 32.2 | GraniteMoeHybridForCausalLM | not stated; UB 2025-09-16 |
| IBM Granite 4.0 (hybrid MoE) | ibm-granite/granite-4.0-h-tiny-base / -h-tiny | f95c8e83b06c12f877486f18d2e2d109ab252bd0 / 791e0d3d28c86e106c9b6e0b4cecdee0375b6124 | 2025-09-16 | no | apache-2.0 | 6,939,037,248 | 13.9 / 6.9 | GraniteMoeHybridForCausalLM | not stated; UB 2025-09-16 |
| IBM Granite 3.3 (one scale) | ibm-granite/granite-3.3-8b-base / -instruct | cfb7adb44a974653cbb2ff883653971c54dba578 / 51dd4bc2ade4059a6bd87649d68aa11e4fb2529b | 2025-04-09 | no | apache-2.0 | 8,170,835,968 / 8,170,864,640 | 16.3 / 8.2 | GraniteForCausalLM | not stated; UB 2025-04-09 |
| Ministral 3 | mistralai/Ministral-3-8B-Base-2512 | d4883f9b36aa2e5d775730d3fdba3d30de51a8ef | 2025-10-31 | no | apache-2.0 | 8,918,026,240 | 17.8 / 8.9 | Mistral3ForConditionalGeneration | not stated (card, arXiv 2601.08584); UB 2025-10-31 |
| Ministral 3 | mistralai/Ministral-3-8B-Instruct-2512-BF16 | f6fae9795746f63c9be8344932f01275f3c63734 | 2025-10-31 | no | apache-2.0 | 8,918,026,240 | 17.8 / 8.9 | Mistral3ForConditionalGeneration | not stated; UB 2025-10-31 |
| Ministral 3 | mistralai/Ministral-3-8B-Instruct-2512 (FP8 release) | 5b26027e7b19eeb4b7352e1fed3926375dd2cb4d | 2025-10-31 | no | apache-2.0 | 8,918,026,240 (BF16 1.50B + F8_E4M3 7.42B) | n/a (ships FP8) | Mistral3ForConditionalGeneration | not stated; UB 2025-10-31 |
| Ministral 3 | mistralai/Ministral-3-14B-Base-2512 | 5b0ceedbb42dff466ae60b258ba296f32da51384 | 2025-10-31 | no | apache-2.0 | 13,945,031,680 | 27.9 / 13.9 | Mistral3ForConditionalGeneration | not stated; UB 2025-10-31 |
| Ministral 3 | mistralai/Ministral-3-14B-Instruct-2512-BF16 | 3cea74c1ebaf5ce5f5a2553de470e2ceab825142 | 2025-10-31 | no | apache-2.0 | 13,945,031,680 | 27.9 / 13.9 | Mistral3ForConditionalGeneration | not stated; UB 2025-10-31 |
| Mistral Small 3 (one scale) | mistralai/Mistral-Small-24B-Base-2501 / -Instruct-2501 | b0a2e4ed093c26997495ae625528f81ea04b749f / 9527884be6e5616bdd54de542f9ae13384489724 | 2025-01-23 / 2025-01-28 | no | apache-2.0 | 23,572,403,200 | 47.1 / 23.6 | MistralForCausalLM | recommended system prompt: "Your knowledge base was last updated on 2023-10-01." (Instruct card) |
| Mistral Small 3.1 (one scale) | mistralai/Mistral-Small-3.1-24B-Base-2503 / -Instruct-2503 | ba6496e3dce1d0bdc93848804b1d4b9d5f3c57bc / 68faf511d618ef198fef186659617cfd2eb8e33a | 2025-03-16 / 2025-03-11 | no | apache-2.0 | 24,011,361,280 | 48.0 / 24.0 | Mistral3ForConditionalGeneration | not stated; UB 2025-03-11 |
| Llama 3.1 | meta-llama/Llama-3.1-8B | d04e592bb4f6aa9cfee91e2e20afa771667e1d4b | 2024-07-14 | manual | llama3.1 | 8,030,261,248 | 16.1 / 8.0 | LlamaForCausalLM | "Knowledge cutoff ... December 2023"; "The pretraining data has a cutoff of December 2023." (card) |
| Llama 3.1 | meta-llama/Llama-3.1-8B-Instruct | 0e9e39f249a16976918f6564b8830bc894c89659 | 2024-07-18 | manual | llama3.1 | 8,030,261,248 | 16.1 / 8.0 | LlamaForCausalLM | as above |
| Llama 3.1 | meta-llama/Llama-3.1-70B | 349b2ddb53ce8f2849a6c168a81980ab25258dac | 2024-07-14 | manual | llama3.1 | 70,553,706,496 | 141.1 / 70.6 | LlamaForCausalLM | as above |
| Llama 3.1 | meta-llama/Llama-3.1-70B-Instruct | 1605565b47bb9346c5515c34102e054115b4f98b | 2024-07-16 | manual | llama3.1 | 70,553,706,496 | 141.1 / 70.6 | LlamaForCausalLM | as above |
| Gemma 3 | google/gemma-3-12b-pt / -it | 295efb63d01a7017928f273a94ebb86105c9526f / 96b6f1eccf38110c56df3a15bffe176da04bfd80 | 2025-03-01 | manual | gemma | 12,187,325,040 | 24.4 / 12.2 | Gemma3ForConditionalGeneration | not stated (card; arXiv 2503.19786 per wave 6); UB 2025-03-01 |
| Gemma 3 | google/gemma-3-27b-pt / -it | 9fe3c4ebc93fbadb14913801536d022054ef11cc / 005ad3404e59d6023443cb575daa05336842228a | 2025-03-01 | manual | gemma | 27,432,406,640 | 54.9 / 27.4 | Gemma3ForConditionalGeneration | not stated; UB 2025-03-01 |
| Falcon-H1 | tiiuae/Falcon-H1-7B-Base / -Instruct | c9a4cbb95c01b1ede39f69eda083d03d8903b8f0 / 41e72f27effbab80cd45b6e884688452253a3686 | 2025-05-01 | no | other (falcon-llm-license) | 7,585,648,736 / 7,585,654,880 | 15.2 / 7.6 | FalconH1ForCausalLM (hybrid attention plus SSM) | not stated (card); UB 2025-05-01 |
| Falcon-H1 | tiiuae/Falcon-H1-34B-Base / -Instruct | db4eb5f380b8a94f2842ba5cc1b49095a244509d / 6e6890e26cba1f58b1e6ee70d654ddf054f9fce8 | 2025-05-01 | no | other (falcon-llm-license) | 33,642,516,224 | 67.3 / 33.6 | FalconH1ForCausalLM | not stated; UB 2025-05-01 |
| DeepSeek-Coder | deepseek-ai/deepseek-coder-6.7b-base / -instruct | ce2207a8bfef3ee92bd7dd4cc31c52cfa0046912 / e5d64addd26a6a1db0f9b863abf6ee3141936807 | 2023-10-23 / 2023-10-29 | no | other (deepseek-license) | 6,740,512,768 | 13.5 / 6.7 | LlamaForCausalLM | code only: GitHub repos "created before February 2023" (arXiv 2401.14196 Sec 2.1, per wave 6) |
| DeepSeek-Coder | deepseek-ai/deepseek-coder-33b-base / -instruct | 45c85cadf3720ef3e85a492e24fd4b8c5d21d8ac / 61dc97b922b13995e7f83b7c8397701dbf9cfd4c | 2023-10-28 / 2023-11-01 | no | other (deepseek-license) | 33,342,991,360 | 66.7 / 33.3 | LlamaForCausalLM | as above |
| StarCoder2 | bigcode/starcoder2-7b, -15b, -15b-instruct-v0.1 | bb9afde76d7945da5745592525db122d4d729eb1, 46d44742909c03ac8cee08eb03fdebce02e193ec, ffb8dd9776ba9a66d655ecd962e882f3013e9f7c | 2024-02-20 to 2024-04-23 | no | bigcode-openrail-m | 7.17B, 15.96B | 14.3, 31.9 | Starcoder2ForCausalLM | not checked (fails pair criterion: no 7B instruct) |
| Seed-Coder (one scale) | ByteDance-Seed/Seed-Coder-8B-Base / -Instruct | 049f843238b40ea67671836204f3d8585a679327 / 1c5af72afa21c22c9272a0b60a3a404195e88fcd | 2025-04-27 | no | mit | 8,250,462,208 | 16.5 / 8.3 | LlamaForCausalLM | not stated (card); UB 2025-04-27 |
| EXAONE 3.5 | LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct, -32B-Instruct | 553ea250b9a5317231459279d5847d6cf955b9aa, 3d27aab477c042df2e174d36eea47b77c8871ef0 | 2024-12-01 | no | other: "EXAONE AI Model License Agreement 1.1 - NC" | 7.82B, 32.00B | 15.6, 64.0 | ExaoneForCausalLM | not checked (fails: no base repo listed; non-commercial licence) |
| Phi-4 | microsoft/phi-4 | 2db69c1c3e91a05d2c64a3185acfbaf36f744e25 | 2024-12-11 | no | mit | 14,659,507,200 | 29.3 / 14.7 | Phi3ForCausalLM | "cutoff dates of June 2024 and earlier for publicly available data" (card); no base checkpoint referenced, one scale |
| SmolLM3 | HuggingFaceTB/SmolLM3-3B-Base / -3B | d78a42f79198603e614095753484a04c10c2b940 / a07cc9a04f16550a088caea529712d1d335b0ac1 | 2025-06-19 / 2025-07-08 | no | apache-2.0 | 3,075,098,624 | 6.2 / 3.1 | SmolLM3ForCausalLM | not checked (one scale, 3B) |

Discovery: author listings (`raw/list_<author>.json`, 200 newest repos each) for google, mistralai, ibm-granite, meta-llama, microsoft, tiiuae, LGAI-EXAONE, bigcode, deepseek-ai, HuggingFaceTB, ByteDance-Seed. Not found: a dense Gemma 4 model between E4B and 12B; any Granite 4.2 base repo (4.2 instruct cards name `granite-4.1-*-base` as base); a 7B StarCoder2 instruct; EXAONE 3.5 base repos; a public `Qwen/Qwen3-32B-Base` (the API returned HTTP 401, saved as `raw/api_Qwen_Qwen3-32B-Base.json`), although `Qwen/Qwen3-32B` exists (sha 9216db5781bf21249d130ec9da846c4624c16137, apache-2.0, 32,762,123,264 params, 65.5 GB bf16).

### 1.2 Licence: research use and publication

| Family | Licence | Research use and publication of results | Key text (source) | Gating cost |
|---|---|---|---|---|
| Gemma 4 | Apache-2.0 | permitted | card: "License: Apache 2.0"; arXiv 2607.02770 Sec 1: "We release the Gemma 4 models under an Apache 2.0 license" | none (not gated) |
| Granite 4.1 / 4.2 | Apache-2.0 | permitted | 4.1 card: "License: Apache 2.0"; 4.2 card: "All Granite models are released under the Apache 2.0 license, enabling unrestricted commercial and academic use." | none |
| Ministral 3 | Apache-2.0 | permitted | card: "Apache 2.0 License: Open-source license allowing usage and modification for both commercial and non-commercial purposes."; arXiv 2601.08584: "All Ministral 3 models (3 sizes x 3 variants) are open-weight under the Apache 2.0 license." | none |
| Mistral Small 3 / 3.1 | Apache-2.0 | permitted | card: "Apache 2.0 License" | none |
| Llama 3.1 | Llama 3.1 Community License | permitted, with conditions | card: "Llama 3.1 is intended for commercial and research use in multiple languages."; licence Sec 1.b.i: redistributors must "prominently display 'Built with Llama'" | gated (manual); operator must accept terms |
| Gemma 3 | Gemma Terms of Use (`license: gemma`) | permitted per the terms' name and gate text; terms page not read | gate text: "you're required to review and agree to Google's usage license"; terms link `https://ai.google.dev/gemma/terms` (host outside the allowed list) | gated (manual) |
| Falcon-H1 | Falcon-LLM License | not verified | licence link `https://falconllm.tii.ae/falcon-terms-and-conditions.html` (host outside the allowed list) | none |
| DeepSeek-Coder | DeepSeek Model License | permitted per card | card: "DeepSeek Coder supports commercial use." | none |
| EXAONE 3.5 | EXAONE AI Model License 1.1 - NC | non-commercial; research likely allowed, not verified | card "License" section | none |
| StarCoder2 | BigCode OpenRAIL-M | permitted with use restrictions | cardData | none |
| Seed-Coder, Phi-4 | MIT | permitted | cardData | none |

### 1.3 Published code scores (instruct unless marked; numbers as printed)

| Model | HumanEval | HumanEval+ | MBPP | MBPP+ | LiveCodeBench | Location |
|---|---|---|---|---|---|---|
| gemma-4-12B-it | not stated | not stated | not stated | not stated | v6: 72.0 (thinking mode) | card "Benchmark Results"; arXiv 2607.02770 Table 5 ("All models are in thinking mode unless explicitly stated") |
| gemma-4-31B-it | not stated | not stated | not stated | not stated | v6: 80.0 (thinking mode) | as above |
| gemma-4 base (12B, 31B) | not stated | not stated | not stated | not stated | not stated | card, arXiv 2607.02770 |
| gemma-3-27b-it | not stated | not stated | not stated | not stated | v6: 29.1 ("Gemma 3 27B (no think)") | Gemma 4 card table |
| gemma-3-12b-pt / 27b-pt (base) | 45.7 / 48.8 (0-shot) | not stated | 60.4 / 65.6 (3-shot) | not stated | not stated | Gemma 3 card "STEM and code" |
| granite-4.1-8b | 85.37 | 79.88 | 87.30 | 73.81 | not stated | 4.1 card "Code Tasks" (pass@1) |
| granite-4.1-30b | 88.41 | 85.37 | 85.45 | 73.54 | not stated | as above |
| granite-4.1-8b-base | 68.29 (StarCoder prompt: 79.24) | 62.80 | 63.76 | 53.97 | not stated | 4.1 base card "Code Tasks" |
| granite-4.1-30b-base | 69.50 (StarCoder prompt: 81.52); the row prints a fourth unlabeled value 67.68 | 62.20 | 83.60 | 69.58 | not stated | as above |
| granite-4.2-8b / 30b (thinking) | not stated | not stated | not stated | not stated | v6: 73.24 / 75.77 | 4.2 card "Reasoning" |
| Ministral-3-8B / 14B Instruct | not stated | not stated | not stated | not stated | not stated (card's 0.616 / 0.646 is the Reasoning variant) | card; arXiv 2601.08584 |
| Ministral-3-8B / 14B Base | not stated | not stated | 70.0 / 71.6 (3-shot pass@1) | not stated | not stated | arXiv 2601.08584 Table 3 |
| Ministral-3-8B / 14B Reasoning | not stated | not stated | not stated | not stated | v6: 61.6 / 64.6 (pass@5) | arXiv 2601.08584 Table 5 |
| Llama-3.1-8B / 70B-Instruct | 72.6 / 80.5 | not stated | "MBPP ++ base version" 72.8 / 86.0 | not stated | not stated | card instruct table |
| Mistral-Small-24B-Instruct-2501 | 0.848 (humaneval_instruct_pass@1) | not stated | not stated | not stated | not stated | card |
| Falcon-H1-7B / 34B-Instruct | 86.59 / 87.2 | 81.1 / 81.71 | 80.69 / 83.86 | 68.78 / 71.43 | 35.03 / 49.71 (version not stated) | cards "Code" rows |
| Falcon-H1-7B / 34B-Base | 67.68 / 70.12 | 63.41 / 64.63 | 78.57 / 83.33 | 67.2 / 70.37 | not stated | base cards |
| Seed-Coder-8B-Instruct | 84.8 | not stated | 85.2 | not stated | 24.7 (2410 to 2502) | card |
| phi-4 | 82.6 | not stated | not stated | not stated | not stated | card |

## 2. Recommendation: Gemma 4, 12B and 31B

Recommended third family: **Gemma 4**, instruct `google/gemma-4-12B-it` (43c9d014b231474fa7212dbb48a762566c2b255d) and `google/gemma-4-31B-it` (842da3794eaa0b77d5f08bae87a17459d91ff475), bases `google/gemma-4-12B` (1a2c7729392586f5ecddae8807ee2ef741eabb9a) and `google/gemma-4-31B` (5bbc2fb1c1b2c611d06e3d9f23c170ba21659d89). Alternate: **Granite 4.1, 8B and 30B**.

| Criterion | Gemma 4 12B / 31B | Granite 4.1 8B / 30B (alternate) | Ministral 3 8B / 14B | Llama 3.1 8B / 70B | Gemma 3 12B / 27B |
|---|---|---|---|---|---|
| (a) base and instruct at each scale | yes, both | yes, both | yes, both | yes, both | yes, both |
| (b) licence for research and publication | Apache-2.0 | Apache-2.0 | Apache-2.0 | Llama 3.1 licence, attribution required | Gemma terms, not read |
| Gated | no | no | no | yes (manual) | yes (manual) |
| (c) hidden states | open weights; multimodal wrapper | open weights; text-only dense | open weights; multimodal wrapper | open weights | open weights; multimodal wrapper |
| (d) fits 96 GB | 23.9 and 62.5 GB bf16 | 17.6 and 57.7 GB bf16 | 17.8 and 27.9 GB bf16 | 70B needs FP8 (70.6 GB) | 24.4 and 54.9 GB bf16 |
| Code competence (stated) | LCB v6 72.0 / 80.0 (thinking) | HE 85.37 / 88.41, MBPP 87.30 / 85.45 | no instruct code score stated | HE 72.6 / 80.5 | 27B-it LCB v6 29.1 |
| Stated cutoff | January 2025 | not stated (UB 2026-04-06) | not stated (UB 2025-10-31) | December 2023 | not stated (UB 2025-03-01) |
| Scale match to 7-8B and 14-32B | 12B and 31B | 8B and 30B (best match) | 8B and 14B | 8B and 70B | 12B and 27B |

Reasons for Gemma 4 over Granite 4.1:

1. **Stated cutoff.** Gemma 4 states January 2025 in both the card and the report, next to Olmo 3 (December 31, 2024). Granite 4.1 states none, and its upper bound is 2026-04-06, so almost no LiveCodeBench problem could be counted as post-cutoff for certain. The post-cutoff analysis needs a stated or early date.
2. **Code competence.** Gemma 4 has the highest stated LiveCodeBench v6 of any candidate at these scales: 72.0 and 80.0. These scores are in thinking mode, so the non-thinking accuracy that the primary set uses is not stated.
3. **Licence and access.** Gemma 4 is Apache-2.0 and not gated, unlike Gemma 3 and Llama 3.1. It adds no terms for the operator to accept.
4. **Thinking toggle.** Gemma 4 has a same-weights thinking toggle (`<|think|>` in the system prompt, `enable_thinking` in the processor). This gives a second-family reasoning arm, optional (section 4).

Costs of Gemma 4, recorded for the design:

- **Architectures differ across scales.** The 12B is "Gemma 4 12B Unified", which has no encoder ("Gemma4UnifiedForConditionalGeneration", text, image, and audio). The 31B has a separate vision encoder of about 550M parameters ("Gemma4ForConditionalGeneration"). Hidden states must be read from the decoder stack of each. Within-family scale contrasts therefore mix scale with architecture.
- **Smaller small scale.** The small scale is 12B, not 7-8B. No dense Gemma 4 model sits between E4B and 12B; E4B uses per-layer embeddings.
- **Empty thought block.** With thinking off, the card says the model "will still generate the tags but with an empty thought block". Answer extraction must strip `<|channel>thought\n<channel|>`.
- **Sampling.** The card recommends `temperature=1.0`, `top_p=0.95`, `top_k=64`. The frozen design uses temperature 1.0 and top-p 1.0; record this as a deviation from the card, as for Qwen3.
- **Recent updates.** The 12B repos were last modified on 2026-10-30. Pin the SHAs above.
- **Loading class.** The cards load the models with `AutoModelForMultimodalLM`, so the Transformers version must be pinned.

When to switch to the alternate (Granite 4.1): if multimodal checkpoints are unacceptable for hidden-state extraction, use Granite 4.1. It is plain dense GraniteForCausalLM at both scales, Apache-2.0, and not gated, and it has the best-documented HumanEval and MBPP scores. Granite 4.2 also ships a same-weights thinking toggle on the same 4.1 bases. The cost is no stated cutoff. Note: the 4.1-8b instruct count (8,791,592,960) differs from its base (8,380,551,168), but the card says the architecture has "shared input/output embeddings". This discrepancy is unexplained.

## 3. Re-verification of R1 section 3.2 revisions

All 16 distinct repository IDs in R1 section 3.2, plus the Olmo-3.1-32B-Instruct SFT and DPO checkpoints from B3 (18 in all), were queried at `/api/models/<id>/revision/main` on 2026-11-10 (`raw/rev_*.json`). **None changed** since wave 6. The SHAs in R1 section 3.2 stand, and the section 4 matrix below repeats them.

## 4. Rebalanced matrix

Choice of the two primary Qwen models: **Qwen3-8B and Qwen3-14B**, both with thinking off. The reasons:

1. **Two scales of one family.** The pair is two scales of one model family, as Olmo 3 and Gemma 4 are. A within-family scale contrast is therefore not confounded with a change of training recipe or generation.
2. **Same kind of model.** All six primary models are then general-purpose instruct models with chat templates; none is a code specialist. The code-specialist question becomes an explicit stratum (C1 to C4) and is no longer a hidden imbalance within one family.
3. **Reasoning toggle on primary weights.** The reasoning toggle and the 2610.31820 reconciliation (Qwen3-8B, thinking on) use the same weights as a primary model.
4. **Base pairs exist.** Both have released bases (Qwen3-8B-Base, Qwen3-14B-Base). Qwen3-32B has no public base (`Qwen/Qwen3-32B-Base` returned 401), so it cannot replace 14B under the base-stratum requirement.

The cost of this choice: Qwen's large scale is 14B, while the other two families reach 31-32B. Qwen3 also has no stated cutoff; its upper bound is 2025-04-27, later than Qwen2.5-Coder's 2024-09-17 and 2024-11-06.

Cutoff column: "count date" is the date another agent should use for the post-cutoff LiveCodeBench count. It is the stated whole-corpus cutoff if one exists, otherwise the UB. A problem released after the count date is post-cutoff for certain.

| # | Role | Repository ID | Revision (main) | Params | bf16 GB | Licence | Stated cutoff (source) | UB (createdAt) | Count date |
|---|---|---|---|---|---|---|---|---|---|
| P1 | Primary, instruct (thinking off) | Qwen/Qwen3-8B | b968826d9c46dd6066d109eabc6255188de91218 | 8.19B | 16.4 | Apache-2.0 | not stated (card, arXiv 2505.09388) | 2025-04-27 | 2025-04-27 |
| P2 | Primary, instruct (thinking off) | Qwen/Qwen3-14B | 40c069824f4251a91eefaf281ebe4c544efd3e18 | 14.77B | 29.5 | Apache-2.0 | not stated | 2025-04-27 | 2025-04-27 |
| P3 | Primary, instruct | allenai/Olmo-3-7B-Instruct | 6e5971d9eba42665f5bd5a0fcf047f299ce1dccc | 7.30B | 14.6 | Apache-2.0 | "Date cutoff: Dec. 2024." (card); "December 31, 2024" (arXiv 2512.13961 Sec 3.4.1) | 2025-11-19 | 2024-12-31 |
| P4 | Primary, instruct | allenai/Olmo-3.1-32B-Instruct | ac0587e4a7744a551c059d8cd17ba220bc940dae | 32.23B | 64.5 | Apache-2.0 | as P3 | 2025-12-10 | 2024-12-31 |
| P5 | Primary, instruct (thinking off) | google/gemma-4-12B-it | 43c9d014b231474fa7212dbb48a762566c2b255d | 11.96B | 23.9 | Apache-2.0 | "cutoff date of January 2025" (card; arXiv 2607.02770 Sec 2.4) | 2026-05-23 | 2025-01-31 |
| P6 | Primary, instruct (thinking off) | google/gemma-4-31B-it | 842da3794eaa0b77d5f08bae87a17459d91ff475 | 31.27B | 62.5 | Apache-2.0 | as P5 | 2026-03-11 | 2025-01-31 |
| B1 | Base stratum (base of P1) | Qwen/Qwen3-8B-Base | 49e3418fbbbca6ecbdf9608b4d22e5a407081db4 | 8.19B | 16.4 | Apache-2.0 | not stated | 2025-04-28 | 2025-04-28 |
| B2 | Base stratum (base of P2) | Qwen/Qwen3-14B-Base | 0b0bd3732e2c374d483664439ea334928b65f304 | 14.77B | 29.5 | Apache-2.0 | not stated | 2025-04-28 | 2025-04-28 |
| B3 | Base stratum (base of P3); trajectory start | allenai/Olmo-3-1025-7B | a81bae42db3975be1671e27b9c9a56da1a9f980f | 7.30B | 14.6 | Apache-2.0 | as P3 | 2025-09-12 | 2024-12-31 |
| B4 | Base stratum (base of P4) | allenai/Olmo-3-1125-32B | c2b61dae89a1ad10e4ad5653d0e46b590902607b | 32.23B | 64.5 | Apache-2.0 | as P3 | 2025-11-04 | 2024-12-31 |
| B5 | Base stratum (base of P5) | google/gemma-4-12B | 1a2c7729392586f5ecddae8807ee2ef741eabb9a | 11.96B | 23.9 | Apache-2.0 | as P5 | 2026-05-23 | 2025-01-31 |
| B6 | Base stratum (base of P6) | google/gemma-4-31B | 5bbc2fb1c1b2c611d06e3d9f23c170ba21659d89 | 31.27B | 62.5 | Apache-2.0 | as P5 | 2026-03-12 | 2025-01-31 |
| S1 | Reasoning toggle, same weights as P1; also the 2610.31820 reconciliation model | Qwen/Qwen3-8B, thinking on | b968826d9c46dd6066d109eabc6255188de91218 | 8.19B | 16.4 | Apache-2.0 | as P1 | 2025-04-27 | 2025-04-27 |
| S2 | Reasoning toggle, second scale (same weights as P2; optional) | Qwen/Qwen3-14B, thinking on | 40c069824f4251a91eefaf281ebe4c544efd3e18 | 14.77B | 29.5 | Apache-2.0 | as P2 | 2025-04-27 | 2025-04-27 |
| S3 | Reasoning toggle, second family (same weights as P5 or P6; optional, operator item) | google/gemma-4-12B-it or -31B-it, thinking on | as P5 / P6 | as P5 / P6 | as P5 / P6 | Apache-2.0 | as P5 | as P5 / P6 | 2025-01-31 |
| C1 | Coder-variant stratum (moved from primary); also the [Ribeiro] reconciliation model | Qwen/Qwen2.5-Coder-7B-Instruct | c03e6d358207e414f1eca0bb1891e29f1db0e242 | 7.62B | 15.2 | Apache-2.0 | code only: GitHub repos "created before February 2024" (arXiv 2409.12186 Sec 3.1.1), i.e. 2024-01-31; corpus not stated | 2024-09-17 | 2024-09-17 |
| C2 | Coder-variant stratum (moved from primary) | Qwen/Qwen2.5-Coder-32B-Instruct | 381fc969f78efac66bc87ff7ddeadb7e73c218a7 | 32.76B | 65.5 | Apache-2.0 | as C1 | 2024-11-06 | 2024-11-06 |
| C3 | Coder-variant base versus instruct (base of C1) | Qwen/Qwen2.5-Coder-7B | 0396a76181e127dfc13e5c5ec48a8cee09938b02 | 7.62B | 15.2 | Apache-2.0 | as C1 | 2024-09-16 | 2024-09-16 |
| C4 | Coder-variant base versus instruct (base of C2) | Qwen/Qwen2.5-Coder-32B | 2e12b5f7bc878d424d222e224ed40aee564ec45f | 32.76B | 65.5 | Apache-2.0 | as C1 | 2024-11-08 | 2024-11-08 |
| T1 | Post-training trajectory (SFT); also the pilot model | allenai/Olmo-3-7B-Instruct-SFT | e1452fc572d51966ff4aaeb25118b891eb93e549 | 7.30B | 14.6 | Apache-2.0 | as P3 | 2025-11-17 | 2024-12-31 |
| T2 | Post-training trajectory (DPO) | allenai/Olmo-3-7B-Instruct-DPO | b33130b7de49f0c2553b5c2b3bc8409ff3e627d1 | 7.30B | 14.6 | Apache-2.0 | as P3 | 2025-11-19 | 2024-12-31 |
| T3 | Trajectory endpoints (already listed) | B3, then T1, then T2, then P3 | | | | | | | |
| T4 | 32B trajectory (SFT; optional) | allenai/Olmo-3.1-32B-Instruct-SFT | 152782ecc41a86c5cbe3fb6afa68bd90934de48a | 32.23B | 64.5 | Apache-2.0 | as P3 | 2025-11-18 | 2024-12-31 |
| T5 | 32B trajectory (DPO; optional) | allenai/Olmo-3.1-32B-Instruct-DPO | fc84a4f699916fcf585aa54371f47897fa934d5c | 32.23B | 64.5 | Apache-2.0 | as P3 | 2025-11-18 | 2024-12-31 |
| R1 | Reconciliation only ([Campos]) | Qwen/Qwen3-Coder-30B-A3B-Instruct | b2cff646eb4bb1d68355c01b18ae02e7cf42d120 | 30.53B total, 3.3B active | 61.1 | Apache-2.0 | not stated (card) | 2025-07-31 | 2025-07-31 |
| R2 | Reconciliation only ([Campos]); native MXFP4 MoE weights | openai/gpt-oss-20b | 6cee5e81ee83917806bbde320786a8fb61efebee | 21B (card) | 42.0 | Apache-2.0 | "knowledge cutoff of June 2024" (arXiv 2508.10925 Sec 2.4) | 2025-08-04 | 2024-06-30 |

Notes on the matrix:

- **Reconciliation.** The [Ribeiro] reconciliation uses C1 and the [2610.31820] reconciliation uses S1. Both models remain in the matrix, through secondary strata.
- **Fit on one 96 GB GPU.** The largest model is Qwen2.5-Coder-32B at 65.5 GB bf16 (C2, C4). The largest primary model is Olmo-3.1-32B-Instruct at 64.5 GB. Every model fits one 96 GB GPU at bf16, and no FP8 is needed.
- **Count dates.** In the primary set, count dates range from 2024-12-31 (Olmo 3) through 2025-01-31 (Gemma 4) to 2025-04-27 (Qwen3, UB only). The latest count date in the whole matrix is 2025-07-31 (R1).
- **Family balance.** The primary set has two models each from three developers: Alibaba Qwen, Ai2, and Google. This resolves R1 section 3.2's "Family balance (TMLR F13)" operator item.

## 5. Instrument gaps

1. **Licence pages not read.** The Gemma 4 licence link (`ai.google.dev/gemma/docs/gemma_4_license`), the Gemma 3 terms (`ai.google.dev/gemma/terms`), and the Falcon-LLM licence (`falconllm.tii.ae`) are on hosts outside the allowed list. For Gemma 4, the Apache-2.0 status rests on cardData, the card, and the arXiv report. The repo has no LICENSE file.
2. **Gated cards were readable.** The READMEs of the gated Gemma 3 and Llama 3.1 repos were readable anonymously via `resolve/main/README.md` this time, unlike wave 6. Their configs and weights were not requested.
3. **No stated cutoffs.** No cutoff is stated for Qwen3, Qwen3-Coder, Granite 4.x, Ministral 3, Mistral Small 3.1, Gemma 3, Falcon-H1, or Seed-Coder. Only UBs are given.
4. **Gemma 4 scores.** Gemma 4 has no stated HumanEval, HumanEval+, MBPP, or MBPP+ for any variant. Its LiveCodeBench v6 scores are thinking-mode scores; non-thinking code accuracy is not stated.
5. **Ministral 3 scores.** The Ministral 3 Instruct variants have no stated code score.
6. **Granite parameter counts.** The granite-4.1-8b instruct and base parameter counts differ (8,791,592,960 versus 8,380,551,168), which is unexplained by the card. The 30B base HumanEval row prints an unlabeled fourth value.
7. **Report section numbers.** arXiv section numbers are from the HTML render headings. Verify them against the PDF before citing.
8. **Listing truncation.** Author listings were capped at the 200 newest repos, so older repos (for example microsoft/phi-4 itself) may be missing from the discovery lists. Candidates were then queried by ID.
