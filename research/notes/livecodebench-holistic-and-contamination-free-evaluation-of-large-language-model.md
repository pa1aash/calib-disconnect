---
title: "LiveCodeBench: Holistic and Contamination Free Evaluation of Large\n    Language\
  \ Models for Code"
id: livecodebench-holistic-and-contamination-free-evaluation-of-large-language-model
tags:
- aaai-bar-eval-dprc-d78e07
- benchmark
- livecodebench
- competitive-programming
created: '2026-07-19T20:02:24.028952Z'
updated: '2026-07-19T20:06:19.024420Z'
source: https://livecodebench.github.io/
source_domain: livecodebench.github.io
fetched_at: '2026-07-19T20:02:24.028496Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'LiveCodeBench project page (Jain, Han, Gu, Li, Yan, Zhang, Wang, Solar-Lezama,
  Sen, Stoica; UC Berkeley/MIT/Cornell; arXiv:2403.07974). A contamination-free, continuously-updated
  benchmark scraping fresh competitive-programming problems from LeetCode, AtCoder,
  Codeforces (300+ problems, May 2023-Feb 2024 window at time of writing), evaluating
  29 LLMs across code generation, self-repair, test-output prediction, and code execution
  -- broader than raw pass@1. Time-stamps each problem so post-cutoff-date subsets
  test true generalization; found DeepSeek models show a sharp performance drop on
  LeetCode problems released after their training cutoff, evidencing prior-benchmark
  contamination. Also finds HumanEval overfitting: some fine-tuned open models beat
  larger closed models on HumanEval but lag badly on LCB-Easy, i.e. HumanEval performance
  does not transfer. For our purposes: LiveCodeBench is explicitly competitive-programming-sourced
  (LeetCode/AtCoder/Codeforces), reinforcing that it -- like TACO -- sits on the all-or-nothing
  competitive-code side of the competitive-vs-functional divide, distinct from BigCodeBench''s
  library-call/unit-test functional-code setting.'
---

LiveCodeBench: Holistic and Contamination Free Evaluation of Large
    Language Models for Code
LiveCodeBench: Holistic and Contamination Free Evaluation of
              Large Language Models for Code
Naman Jain
1
,
King Han
1
,
Alex Gu
2
,
Wen-Ding Li
3
,
Fanjia Yan
1
,
Tianjun Zhang
1
,
Sida Wang
,
Armando Solar-Lezama
2
,
Koushik Sen
1
,
Ion Stoica
1
1
UC Berkeley
2
MIT
3
Cornell University
Paper
Code
Data
Leaderboard
LiveCodeBench
collects problems from periodic contests on
LeetCode
,
AtCoder
, and
Codeforces
platforms and uses them for constructing a holistic benchmark for evaluating Code LLMs across variety of
          code-related scenarios continuously over time.
Introduction
LiveCodeBench is a holistic and contamination-free evaluation benchmark
              of LLMs for code that continuously collects new problems over time.
              Particularly, LiveCodeBench also focuses on broader code-related capabilities,
              such as self-repair, code execution, and test output prediction,
              beyond mere code generation. Currently, LiveCodeBench hosts over
              three hundred high-quality coding problems published between May
              2023 and February 2024. We evaluate 29 LLMs on LiveCodeBench
              scenarios and present novel empirical findings not revealed in
              prior benchmarks.
Contamination
LiveCodeBench
annotates problems with release dates, and thus allows evaluating
              models on problems released during a specific time period. Thus, for a newer model
              with a training-cutoff date
D
, we can evaluate it on problems released after
D
to measure its generalization on
unseen
problems.
The above plots depict the performance of models on code generation and test output prediction scenarios
              on problems released over different months. We find that
DeepSeek
models
              exhibit a stark drop in performance on LeetCode problems released since September 2023, its release date,
              indicating that the earlier problems might be contaminated. In contrast, for
GPT
models, the performance is relatively stable across different months.
Holistic Evaluation and Open vs Closed Models
LiveCodeBench
evaluates models on a variety of code-related scenarios, such as
              code generation, self-repair, test output prediction, and code execution. We find that while model
              performances
              are correlated across different scenarios, there relative performances and ordering can vary (left
              figure).
              For instance,
Claude-3-Opus
overtakes
GPT-4-turbo
in
              the
              test output prediction scenario, but not in the code generation scenario. Similarly,
Mistral-Large
performs considerably better on natural language reasoning tasks like test output prediction and code
              execution.
We compare the performance of open access models with closed api-access models on
LiveCodeBench
and find that generally the closed api-access models outperform the
              open models. Particularly, the only open models that surpass the barrier are fine-tuned variants of large
              (30+B parameter) models.
Potential Overfitting in HumanEval
We also find that models that perform well on
HumanEval
might be overfitting on
              the benchmark. Particularly, the models are separated into two clusters depicted
              by the green and red shaded region in the right scatterplot. The models in the green region perform
              similarly on
HumanEval
and
LCB-Easy
, while the models in the red
              region
              perform well on
HumanEval
but lag behind on
LCB-Easy
.
              For instance,
DS-Ins-1.3B
model outperforms
Gemini-Pro
and
Claude-Ins-1
but performs considerably
              worse on
LCB-Easy
.
              Interestingly, the models in the red region are mostly fine-tuned variants of open access models. On the
              other hand, base models and most of the closed api-access models lie in the green region. This highlights
              a potential lack of diverse fine-tuning data being employed by the open source community and the need for
              optimizing models for a broader set of code-related tasks.
Model Comparisions
The above plots depict the performance of models on different scenarios considered in
LiveCodeBench
. We find that
GPT-4-turbo
and
Claude-3-Opus
models perform best across different scenarios. Among open source
              models,
DS-Ins-33B
and
Phind-34B
perform the best.
Submitting Custom Models
To submit models you can create a pull request on our
Github
. Particularly, you can copy your model
              generations folder from `output` to the `submissions` folder and create a pull request. We will review the
              submission and add the model to the leaderboard accordingly.
BibTeX
@article{jain2024livecodebench,
    title={LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code},
    author={Jain, Naman and Han, King and Gu, Alex and Li, Wen-Ding and Yan, Fanjia and Zhang, Tianjun and Wang, Sida and Solar-Lezama, Armando and Sen, Koushik and Stoica, Ion},
    journal={arXiv preprint arXiv:2403.07974},
    year={2024}
}