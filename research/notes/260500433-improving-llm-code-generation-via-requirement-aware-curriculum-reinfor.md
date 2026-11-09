---
title: '[2605.00433] Improving LLM Code Generation via Requirement-Aware Curriculum
  Reinforcement Learning'
id: 260500433-improving-llm-code-generation-via-requirement-aware-curriculum-reinfor
tags:
- code-llm-best-aaai-paper-6ded37
- requirement-difficulty
- rl-not-benchmark
created: '2026-07-20T07:40:51.235379Z'
updated: '2026-07-20T07:43:53.829288Z'
source: https://arxiv.org/abs/2605.00433
source_domain: arxiv.org
fetched_at: '2026-07-20T07:40:51.235035Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Yin, Tian, Chen & Guo (May 2026) propose RECRL, a curriculum-RL framework
  for code-generation fine-tuning that perceives PER-REQUIREMENT difficulty (model-specific,
  not static), optimizes/rewrites requirements judged too hard for effective learning
  signal, and adaptively samples training batches along a smooth difficulty curriculum.
  Evaluated on 5 LLMs x 5 benchmarks vs. 5 SOTA CRL baselines, gives average Pass@1
  gains of 1.23-5.62%. Relevance: RECRL''s ''requirement difficulty perception'' module
  is the closest prior work to a per-requirement difficulty-mining mechanism, but
  (a) it is purely a TRAINING-time RL curriculum technique, not a released evaluation
  benchmark/protocol/diagnostic artifact; (b) difficulty is measured per whole coding
  requirement/task the model is trained on, not per unit-test sub-requirement within
  one task; (c) no released ''hard requirements'' diagnostic subset or contamination-resistant
  benchmark artifact results from it. Confirms per-requirement difficulty modeling
  is an active idea in code-LLM research, but channelled into RL reward shaping (an
  already-ruled-out lane for this project) rather than benchmark/eval-artifact contribution.'
---

[2605.00433] Improving LLM Code Generation via Requirement-Aware Curriculum Reinforcement Learning
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2605.00433
(cs)
[Submitted on 1 May 2026]
Title:
Improving LLM Code Generation via Requirement-Aware Curriculum Reinforcement Learning
Authors:
Shouyu Yin
,
Zhao Tian
,
Junjie Chen
,
Shikai Guo
View a PDF of the paper titled Improving LLM Code Generation via Requirement-Aware Curriculum Reinforcement Learning, by Shouyu Yin and 3 other authors
View PDF
HTML (experimental)
Abstract:
Code generation, which aims to automatically generate source code from given programming requirements, has the potential to substantially improve software development efficiency. With the rapid advancement of large language models (LLMs), LLM-based code generation has attracted widespread attention from both academia and industry. However, as programming requirements become increasingly complex, existing LLMs still exhibit notable performance limitations. To address this challenge, recent studies have proposed training-based curriculum reinforcement learning (CRL) strategies to improve LLM code generation performance. Despite their effectiveness, existing CRL approaches suffer from several limitations, including misaligned requirement difficulty perception, the absence of requirement difficulty optimization, and suboptimal curriculum sampling strategies. In CRL-based code generation, programming requirements serve as the sole input to the model, making their quality and difficulty critical to training effectiveness. Motivated by insights from software requirements engineering, we propose RECRL, a novel requirement-aware curriculum reinforcement learning framework for enhancing LLM-based code generation. RECRL automatically perceives model-specific requirement difficulty, optimizes challenging requirements to improve training data utilization, and employs an adaptive curriculum sampling strategy to construct training batches with smoothly varying difficulty. Extensive experiments on five state-of-the-art LLMs across five widely-used code generation benchmarks by comparing with five state-of-the-art baselines, demonstrate the significant effectiveness of RECRL. For example, RECRL achieves an average Pass@1 improvement of 1.23%-5.62% over all state-of-the-art baselines.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2605.00433
[cs.SE]
(or
arXiv:2605.00433v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2605.00433
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Yin Shouyu [
view email
]
[v1]
Fri, 1 May 2026 06:10:03 UTC (465 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Improving LLM Code Generation via Requirement-Aware Curriculum Reinforcement Learning, by Shouyu Yin and 3 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.SE
< prev
|
next >
new
|
recent
|
2026-05
Change to browse by:
cs
cs.AI
References & Citations
NASA ADS
Google Scholar
Semantic Scholar
export BibTeX citation
Loading...
BibTeX formatted citation
×
loading...
Data provided by:
Bookmark
Bibliographic Tools
Bibliographic and Citation Tools
Bibliographic Explorer Toggle
Bibliographic Explorer
(
What is the Explorer?
)
Connected Papers Toggle
Connected Papers
(
What is Connected Papers?
)
Litmaps Toggle
Litmaps
(
What is Litmaps?
)
scite.ai Toggle
scite Smart Citations
(
What are Smart Citations?
)
Code, Data, Media
Code, Data and Media Associated with this Article
alphaXiv Toggle
alphaXiv
(
What is alphaXiv?
)
Links to Code Toggle
CatalyzeX Code Finder for Papers
(
What is CatalyzeX?
)
DagsHub Toggle
DagsHub
(
What is DagsHub?
)
GotitPub Toggle
Gotit.pub
(
What is GotitPub?
)
Huggingface Toggle
Hugging Face
(
What is Huggingface?
)
ScienceCast Toggle
ScienceCast
(
What is ScienceCast?
)
Demos
Demos
Replicate Toggle
Replicate
(
What is Replicate?
)
Spaces Toggle
Hugging Face Spaces
(
What is Spaces?
)
Spaces Toggle
TXYZ.AI
(
What is TXYZ.AI?
)
Related Papers
Recommenders and Search Tools
Link to Influence Flower
Influence Flower
(
What are Influence Flowers?
)
Core recommender toggle
CORE Recommender
(
What is CORE?
)
Author
Venue
Institution
Topic
About arXivLabs
arXivLabs: experimental projects with community collaborators
arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.
Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.
Have an idea for a project that will add value for arXiv's community?
Learn more about arXivLabs
.
Which authors of this paper are endorsers?
|
Disable MathJax
(
What is MathJax?
)