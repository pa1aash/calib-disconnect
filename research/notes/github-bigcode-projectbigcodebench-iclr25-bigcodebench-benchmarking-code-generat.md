---
title: 'GitHub - bigcode-project/bigcodebench: [ICLR''25] BigCodeBench: Benchmarking
  Code Generation Towards AGI · GitHub'
id: github-bigcode-projectbigcodebench-iclr25-bigcodebench-benchmarking-code-generat
tags:
- aaai-bar-eval-dprc-d78e07
- benchmark
- bigcodebench
- adoption-evidence
created: '2026-07-19T20:03:23.320109Z'
updated: '2026-07-19T20:06:31.987083Z'
source: https://github.com/bigcode-project/bigcodebench
source_domain: github.com
fetched_at: '2026-07-19T20:03:23.318036Z'
fetch_provider: builtin
status: draft
type: note
tier: ground_truth
content_type: code
deprecated: false
summary: 'Official BigCodeBench GitHub repo (bigcode-project, ICLR''25 tag in repo
  title). Confirms adoption by frontier LLM labs -- Zhipu AI, Alibaba Qwen, DeepSeek,
  Amazon AWS AI, Snowflake AI Research, ServiceNow Research, Meta AI, Cohere AI, Sakana
  AI, AI2 -- as a trusted evaluation benchmark, evidencing it is a live, actively-maintained,
  industry-adopted eval rather than a toy academic dataset (163 models evaluated as
  of the v0.2.2.dev2 release, 515 GitHub stars). Two splits: Complete (docstring-based
  code completion) and Instruct (natural-language instruction following for chat/instruction-tuned
  models). A BigCodeBench-Hard subset (148 tasks) was carved out in 2024-07 to track
  models more aligned with real-world programming. This corroborates BigCodeBench''s
  standing as a credible, unsaturated, ICLR-2025-Oral, widely-adopted benchmark suitable
  to anchor DPRC''s ''realistic functional code'' claim, though the repo itself provides
  no evidence about AAAI-specific precedent for the per-requirement/partial-credit
  angle.'
---

GitHub - bigcode-project/bigcodebench: [ICLR'25] BigCodeBench: Benchmarking Code Generation Towards AGI · GitHub
Skip to content
You signed in with another tab or window.
Reload
to refresh your session.
You signed out in another tab or window.
Reload
to refresh your session.
You switched accounts on another tab or window.
Reload
to refresh your session.
Dismiss alert
Uh oh!
There was an error while loading.
Please reload this page
.
bigcode-project
/
bigcodebench
Public
Notifications
You must be signed in to change notification settings
Fork
74
Star
515
main
Branches
Tags
Go to file
Code
Open more actions menu
Folders and files
Name
Name
Last commit message
Last commit date
Latest commit
History
1,274 Commits
1,274 Commits
.github/
ISSUE_TEMPLATE
.github/
ISSUE_TEMPLATE
Docker
Docker
Requirements
Requirements
analysis
analysis
bigcodebench
bigcodebench
decontamination
decontamination
sandbox-templates
sandbox-templates
tests
tests
tools
tools
.dockerignore
.dockerignore
.gitignore
.gitignore
.pre-commit-config.yaml
.pre-commit-config.yaml
ADVANCED_USAGE.md
ADVANCED_USAGE.md
CITATION.cff
CITATION.cff
LICENSE
LICENSE
MANIFEST.in
MANIFEST.in
README.md
README.md
pyproject.toml
pyproject.toml
release.sh
release.sh
release_docker.sh
release_docker.sh
run.sh
run.sh
setup.cfg
setup.cfg
View all files
Repository files navigation
BigCodeBench
💥 Impact
•
📰 News
•
🔥 Quick Start
•
🚀 Remote Evaluation
•
💻 LLM-generated Code
•
🧑 Advanced Usage
•
📰 Result Submission
•
📜 Citation
🎉 Check out our latest work!
🌟 BigCodeArena 🌟
🚀 Open Evaluation Platform on AI for Vibe Coding 🚀
✨ 100% free to use the latest frontier models! ✨
💥 Impact
BigCodeBench has been trusted by many LLM teams including:
Zhipu AI
Alibaba Qwen
DeepSeek
Amazon AWS AI
Snowflake AI Research
ServiceNow Research
Meta AI
Cohere AI
Sakana AI
Allen Institute for Artificial Intelligence (AI2)
📰 News
[2025-01-22]
We are releasing
bigcodebench==v0.2.2.dev2
, with 163 models evaluated!
[2024-10-06]
We are releasing
bigcodebench==v0.2.0
!
[2024-10-05]
We create a public code execution API on the
Hugging Face space
.
[2024-10-01]
We have evaluated 139 models on BigCodeBench-Hard so far. Take a look at the
leaderboard
!
[2024-08-19]
To make the evaluation fully reproducible, we add a real-time code execution session to the leaderboard. It can be viewed
here
.
[2024-08-02]
We release
bigcodebench==v0.1.9
.
More News
:: click to expand ::
[2024-07-18]
We announce a subset of BigCodeBench, BigCodeBench-Hard, which includes 148 tasks that are more aligned with the real-world programming tasks. The details are available
in this blog post
. The dataset is available
here
. The new release is
bigcodebench==v0.1.8
.
[2024-06-28]
We release
bigcodebench==v0.1.7
.
[2024-06-27]
We release
bigcodebench==v0.1.6
.
[2024-06-19]
We start the Hugging Face BigCodeBench Leaderboard! The leaderboard is available
here
.
[2024-06-18]
We release BigCodeBench, a new benchmark for code generation with 1140 software-engineering-oriented programming tasks. Preprint is available
here
. PyPI package is available
here
with the version
0.1.5
.
🌸 About
BigCodeBench
BigCodeBench is an
easy-to-use
benchmark for solving
practical
and
challenging
tasks via code. It aims to evaluate the true programming capabilities of large language models (LLMs) in a more realistic setting. The benchmark is designed for HumanEval-like function-level code generation tasks, but with much more complex instructions and diverse function calls.
There are two splits in BigCodeBench:
Complete
: Thes split is designed for code completion based on the comprehensive docstrings.
Instruct
: The split works for the instruction-tuned and chat models only, where the models are asked to generate a code snippet based on the natural language instructions. The instructions only contain necessary information, and require more complex reasoning.
Why BigCodeBench?
BigCodeBench focuses on task automation via code generation with
diverse function calls
and
complex instructions
, with:
✨
Precise evaluation & ranking
: See
our leaderboard
for latest LLM rankings before & after rigorous evaluation.
✨
Pre-generated samples
: BigCodeBench accelerates code intelligence research by open-sourcing
LLM-generated samples
for various models -- no need to re-run the expensive benchmarks!
🔥 Quick Start
To get started, please first set up the environment:
#
By default, you will use the remote evaluation API to execute the output samples.
pip install bigcodebench --upgrade
#
You are suggested to use `flash-attn` for generating code samples.
pip install packaging ninja
pip install flash-attn --no-build-isolation
#
Note: if you have installation problem, consider using pre-built
#
wheels from https://github.com/Dao-AILab/flash-attention/releases
⏬ Install nightly version
:: click to expand ::
#
Install to use bigcodebench.generate
pip install
"
git+https://github.com/bigcode-project/bigcodebench.git
"
--upgrade
🚀 Remote Evaluation
We use the greedy decoding as an example to show how to evaluate the generated code samples via remote API.
Warning
To ease the generation, we use batch inference by default. However, the batch inference results could vary from
batch sizes to batch sizes
and
versions to versions
, at least for the vLLM backend. If you want to get more deterministic results for greedy decoding, please set
--bs
to
1
.
Note
gradio
backend on
BigCodeBench-Full
typically takes 6-7 minutes, and on
BigCodeBench-Hard
typically takes 4-5 minutes.
e2b
backend with default machine on
BigCodeBench-Full
typically takes 25-30 minutes, and on
BigCodeBench-Hard
typically takes 15-20 minutes.
bigcodebench.evaluate \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --execution [e2b
|
gradio
|
local] \
  --split [complete
|
instruct] \
  --subset [full
|
hard] \
  --backend [vllm
|
openai
|
anthropic
|
google
|
mistral
|
hf
|
hf-inference]
All the resulted files will be stored in a folder named
bcb_results
.
The generated code samples will be stored in a file named
[model_name]--bigcodebench-[instruct|complete]--[backend]-[temp]-[n_samples]-sanitized_calibrated.jsonl
.
The evaluation results will be stored in a file named
[model_name]--bigcodebench-[instruct|complete]--[backend]-[temp]-[n_samples]-sanitized_calibrated_eval_results.json
.
The pass@k results will be stored in a file named
[model_name]--bigcodebench-[instruct|complete]--[backend]-[temp]-[n_samples]-sanitized_calibrated_pass_at_k.json
.
Note
The
gradio
backend is hosted on the
Hugging Face space
by default.
The default space can be sometimes slow, so we recommend you to use the
gradio
backend with a cloned
bigcodebench-evaluator
endpoint for faster evaluation.
Otherwise, you can also use the
e2b
sandbox for evaluation, which is also pretty slow on the default machine.
Note
BigCodeBench uses different prompts for base and chat models.
By default it is detected by
tokenizer.chat_template
when using
hf
/
vllm
as backend.
For other backends, only chat mode is allowed.
Therefore, if your base models come with a
tokenizer.chat_template
,
please add
--direct_completion
to avoid being evaluated
in a chat mode.
To use E2B, you need to set up an account and get an API key from
E2B
.
export
E2B_API_KEY=
<
your_e2b_api_key
>
Access OpenAI APIs from
OpenAI Console
export
OPENAI_API_KEY=
<
your_openai_api_key
>
Access Anthropic APIs from
Anthropic Console
export
ANTHROPIC_API_KEY=
<
your_anthropic_api_key
>
Access Mistral APIs from
Mistral Console
export
MISTRAL_API_KEY=
<
your_mistral_api_key
>
Access Gemini APIs from
Google AI Studio
export
GOOGLE_API_KEY=
<
your_google_api_key
>
Access the
Hugging Face Serverless Inference API
export
HF_INFERENCE_API_KEY=
<
your_hf_api_key
>
Please make sure your HF access token has the
Make calls to inference providers
permission.
💻 LLM-generated Code
We share pre-generated code samples from LLMs we have
evaluated
on the full set:
See the attachment of our
v0.2.4
. We include
sanitized_samples_calibrated.zip
for your convenience.
🧑 Advanced Usage
Please refer to the
ADVANCED USAGE
for more details.
📰 Result Submission
Please email both the generated code samples and the execution results to
terry.zhuo@monash.edu
if you would like to contribute your model to the leaderboard. Note that the file names should be in the format of
[model_name]--[revision]--[bigcodebench|bigcodebench-hard]-[instruct|complete]--[backend]-[temp]-[n_samples]-sanitized_calibrated.jsonl
and
[model_name]--[revision]--[bigcodebench|bigcodebench-hard]-[instruct|complete]--[backend]-[temp]-[n_samples]-sanitized_calibrated_eval_results.json
. You can
file an issue
to remind us if we do not respond to your email within 3 days.
📜 Citation
@article
{
zhuo2024bigcodebench
,
title
=
{
BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions
}
,
author
=
{
Zhuo, Terry Yue and Vu, Minh Chien and Chim, Jenny and Hu, Han and Yu, Wenhao and Widyasari, Ratnadira and Yusuf, Imam Nur Bani and Zhan, Haolan and He, Junda and Paul, Indraneil and others
}
,
journal
=
{
arXiv preprint arXiv:2406.15877
}
,
year
=
{
2024
}
}
🙏 Acknowledgement
EvalPlus
About
[ICLR'25] BigCodeBench: Benchmarking Code Generation Towards AGI
bigcode-bench.github.io/
Topics
agent
benchmark
program-synthesis
gemini
code-generation
agents
tool-use
instruction-following
gpt-4
large-language-models
llm
chatgpt
function-calling
deepseek
claude-3
Resources
Readme
License
Apache-2.0 license
Uh oh!
There was an error while loading.
Please reload this page
.
Activity
Custom properties
Stars
515
stars
Watchers
7
watching
Forks
74
forks
Report repository
Releases
13
Release BigCodeBench v0.2.4
Latest
Mar 2, 2025
+ 12 releases
Packages
0
Uh oh!
There was an error while loading.
Please reload this page
.
Uh oh!
There was an error while loading.
Please reload this page
.
Contributors
Uh oh!
There was an error while loading.
Please reload this page
.
Languages
Python
95.1%
Dockerfile
4.3%
Shell
0.6%
You can’t perform that action at this time.