---
title: '[2605.15588] Calibrating LLMs with Semantic-level Reward'
id: 260515588-calibrating-llms-with-semantic-level-reward
tags:
- code-llm-calibration-aaai27-eabf3f
- non-verbalized-calibration
- single-gpu-lora
created: '2026-07-17T18:30:17.143241Z'
updated: '2026-07-17T18:34:04.727442Z'
source: http://arxiv.org/abs/2605.15588
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:17.142464Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: arXiv abstract page for Yu, Niu, Wu, Ma, Yu (UCSD) 2026, CSR. Explicitly
  abandons the verbalized-confidence interface, calibrating in semantic-cluster space
  instead; argues verbalized confidence is unstable across paraphrases of the same
  answer. Beats verbalized baselines (RD, RLCR) on ECE (up to 40% lower) and AUROC
  (up to 31% higher) on QA datasets. See full-text note 'calibrating-llms-with-semantic-level-reward'
  for single-A100 LoRA setup and the format-failure-rate critique of verbalized interfaces.
---

[2605.15588] Calibrating LLMs with Semantic-level Reward
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2605.15588
(cs)
[Submitted on 15 May 2026 (
v1
), last revised 20 May 2026 (this version, v2)]
Title:
Calibrating LLMs with Semantic-level Reward
Authors:
Fengfei Yu
,
Ruijia Niu
,
Dongxia Wu
,
Yian Ma
,
Rose Yu
View a PDF of the paper titled Calibrating LLMs with Semantic-level Reward, by Fengfei Yu and 4 other authors
View PDF
HTML (experimental)
Abstract:
As large language models (LLMs) are deployed in consequential settings such as medical question answering and legal reasoning, the ability to estimate when their outputs are likely to be correct is essential for safe and reliable use, requiring well-calibrated uncertainty. Standard reinforcement learning with verifiable rewards (RLVR) trains models with a binary correctness reward that is indifferent to confidence, providing no penalty for confident but wrong predictions and thereby degrading calibration. Recent work addresses this by training models to produce verbalized confidence scores alongside answers and rewarding agreement with correctness. However, verbalized confidence is calibrated at the token level and thus exhibits inconsistency across textual variations with same semantic meaning. We propose \textbf{Calibration with Semantic Reward (CSR)}, a framework that calibrates language models directly in semantic space without a verbalized confidence interface. CSR combines the correctness reward with a novel semantic calibration reward that encourages exploitation among correct rollouts by promoting semantic agreement, and exploration among incorrect ones by discouraging spurious consistency. Experiments across three model families on HotpotQA (in-distribution) and TriviaQA, MSMARCO, and NQ-Open (out-of-distribution) show that CSR consistently achieves lower ECE and higher AUROC than verbalized-confidence baselines across nearly all settings, reducing ECE by up to $40\%$ and improving AUROC by up to $31\%$ over verbalized-confidence baselines, with calibration behavior generalizing robustly across all four evaluation settings.
Subjects:
Computation and Language (cs.CL)
; Machine Learning (cs.LG)
Cite as:
arXiv:2605.15588
[cs.CL]
(or
arXiv:2605.15588v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2605.15588
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Ruijia Niu [
view email
]
[v1]
Fri, 15 May 2026 03:55:11 UTC (2,364 KB)
[v2]
Wed, 20 May 2026 21:06:51 UTC (2,366 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Calibrating LLMs with Semantic-level Reward, by Fengfei Yu and 4 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.CL
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
cs.LG
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