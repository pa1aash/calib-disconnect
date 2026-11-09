---
title: '[2410.17621] Process Supervision-Guided Policy Optimization for Code Generation'
id: 241017621-process-supervision-guided-policy-optimization-for-code-generation
tags:
- code-llm-requirement-pivots-5d35f5
- rl-reward-shaping
- process-reward-model
created: '2026-07-20T06:51:26.686348Z'
updated: '2026-07-20T06:53:39.097222Z'
source: https://arxiv.org/abs/2410.17621
source_domain: arxiv.org
fetched_at: '2026-07-20T06:51:26.685986Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Oct 2024 (v2 Feb 2025) ByteDance-affiliated paper proposing a Process Reward
  Model (PRM) trained to give dense, LINE-LEVEL feedback on code correctness during
  generation (not test-case-level), used both as a dense RL reward signal and for
  critic/value-function initialization in the RL loop. Motivation identical to our
  pivot''s framing: sparse pass/fail-only reward gives zero learning signal when all
  unit tests fail, hindering progress on complex/long-horizon tasks. Finds PRM-as-reward
  plus PRM-as-value-init significantly outperforms outcome-only RL, especially on
  long-horizon code generation. Establishes that ''dense process supervision beats
  sparse outcome reward for code RL'' was already a validated empirical claim by late
  2024/early 2025, roughly a year before our target submission window, using a learned
  PRM rather than directly-verifiable per-test signal.'
---

[2410.17621] Process Supervision-Guided Policy Optimization for Code Generation
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2410.17621
(cs)
[Submitted on 23 Oct 2024 (
v1
), last revised 4 Feb 2025 (this version, v2)]
Title:
Process Supervision-Guided Policy Optimization for Code Generation
Authors:
Ning Dai
,
Zheng Wu
,
Renjie Zheng
,
Ziyun Wei
,
Wenlei Shi
,
Xing Jin
,
Guanlin Liu
,
Chen Dun
,
Liang Huang
,
Lin Yan
View a PDF of the paper titled Process Supervision-Guided Policy Optimization for Code Generation, by Ning Dai and 9 other authors
View PDF
HTML (experimental)
Abstract:
Reinforcement learning (RL) with unit test feedback has enhanced large language models' (LLMs) code generation, but relies on sparse rewards provided only after complete code evaluation, limiting learning efficiency and incremental improvements. When generated code fails all unit tests, no learning signal is received, hindering progress on complex tasks. To address this, we propose a Process Reward Model (PRM) that delivers dense, line-level feedback on code correctness during generation, mimicking human code refinement and providing immediate guidance. We explore various strategies for training PRMs and integrating them into the RL framework, finding that using PRMs both as dense rewards and for value function initialization significantly boosts performance. Our experimental results also highlight the effectiveness of PRMs in enhancing RL-driven code generation, especially for long-horizon scenarios.
Comments:
15 pages, 8 figures
Subjects:
Artificial Intelligence (cs.AI)
MSC
classes:
I.2.7,
Cite as:
arXiv:2410.17621
[cs.AI]
(or
arXiv:2410.17621v2
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2410.17621
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Ning Dai [
view email
]
[v1]
Wed, 23 Oct 2024 07:22:33 UTC (550 KB)
[v2]
Tue, 4 Feb 2025 09:24:30 UTC (906 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Process Supervision-Guided Policy Optimization for Code Generation, by Ning Dai and 9 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.AI
< prev
|
next >
new
|
recent
|
2024-10
Change to browse by:
cs
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