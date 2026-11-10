---
title: '[2605.12446] ORCE: Order-Aware Alignment of Verbalized Confidence in Large
  Language Models'
id: 260512446-orce-order-aware-alignment-of-verbalized-confidence-in-large-language
tags:
- code-llm-calibration-aaai27-eabf3f
created: '2026-07-17T18:30:28.377954Z'
updated: '2026-11-10T09:27:37.741299Z'
source: http://arxiv.org/abs/2605.12446
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:28.377230Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Deprecated duplicate or empty-body record (arXiv metadata only); superseded
  by a full-text note of the same paper or out of scope
---

[2605.12446] ORCE: Order-Aware Alignment of Verbalized Confidence in Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2605.12446
(cs)
[Submitted on 12 May 2026]
Title:
ORCE: Order-Aware Alignment of Verbalized Confidence in Large Language Models
Authors:
Chen Li
,
Xiaoling Hu
,
Songzhu Zheng
,
Jiawei Zhou
,
Chao Chen
View a PDF of the paper titled ORCE: Order-Aware Alignment of Verbalized Confidence in Large Language Models, by Chen Li and 4 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) often produce answers with high certainty even when they are incorrect, making reliable confidence estimation essential for deployment in real-world scenarios. Verbalized confidence, where models explicitly state their confidence in natural language, provides a flexible and user-facing uncertainty signal that can be applied even when token logits are unavailable. However, existing verbalized-confidence methods often optimize answer generation and confidence generation jointly, which can cause confidence-alignment objectives to interfere with answer accuracy. In this work, we propose a decoupled and order-aware framework for verbalized confidence calibration. Our method first generates an answer and then estimates confidence conditioned on the fixed question--answer pair, allowing confidence optimization without directly perturbing the answer-generation process. To align confidence with correctness likelihood, we construct a sampling-based surrogate from multiple model completions and optimize rank-based reinforcement learning objectives that encourage responses with higher estimated correctness likelihood to receive higher verbalized confidence. Experiments on reasoning and knowledge-intensive benchmarks show that our method improves calibration and failure prediction performance while largely preserving answer accuracy. These results demonstrate that verbalized confidence can be more reliably aligned by decoupling confidence estimation from answer generation and optimizing the relative ordering of confidence across responses.
Comments:
18 pages, 2 figures
Subjects:
Machine Learning (cs.LG)
; Computation and Language (cs.CL)
Cite as:
arXiv:2605.12446
[cs.LG]
(or
arXiv:2605.12446v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2605.12446
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Chen Li [
view email
]
[v1]
Tue, 12 May 2026 17:39:43 UTC (261 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled ORCE: Order-Aware Alignment of Verbalized Confidence in Large Language Models, by Chen Li and 4 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.LG
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
cs.CL
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
IArxiv recommender toggle
IArxiv Recommender
(
What is IArxiv?
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