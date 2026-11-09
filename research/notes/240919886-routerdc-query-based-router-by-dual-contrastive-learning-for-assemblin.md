---
title: '[2409.19886] RouterDC: Query-Based Router by Dual Contrastive Learning for
  Assembling Large Language Models'
id: 240919886-routerdc-query-based-router-by-dual-contrastive-learning-for-assemblin
tags:
- code-llm-requirement-pivots-5d35f5
- llm-routing
- ensembling
created: '2026-07-20T06:53:02.424939Z'
updated: '2026-07-20T06:55:26.739022Z'
source: https://arxiv.org/abs/2409.19886
source_domain: arxiv.org
fetched_at: '2026-07-20T06:53:02.424470Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Chen, Jiang, Lin, Kwok, Zhang (NeurIPS 2024): RouterDC trains an encoder
  + LLM-embedding router via two contrastive losses to pick the single best-suited
  off-the-shelf LLM for each incoming query, addressing cases where multiple LLMs
  perform comparably. Outperforms individual top LLMs and prior routing methods by
  +2.76% in-distribution and +1.90% OOD. Routing decision is one-LLM-per-whole-query;
  no decomposition into sub-tasks or requirements, no code-generation-specific evaluation,
  no mechanism to combine partial outputs from different models on the same task.
  Establishes that cross-model routing research targets whole-query selection, leaving
  per-requirement/per-unit-test routing within a single generation task open.'
---

[2409.19886] RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2409.19886
(cs)
[Submitted on 30 Sep 2024]
Title:
RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models
Authors:
Shuhao Chen
,
Weisen Jiang
,
Baijiong Lin
,
James T. Kwok
,
Yu Zhang
View a PDF of the paper titled RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models, by Shuhao Chen and 4 other authors
View PDF
Abstract:
Recent works show that assembling multiple off-the-shelf large language models (LLMs) can harness their complementary abilities. To achieve this, routing is a promising method, which learns a router to select the most suitable LLM for each query. However, existing routing models are ineffective when multiple LLMs perform well for a query. To address this problem, in this paper, we propose a method called query-based Router by Dual Contrastive learning (RouterDC). The RouterDC model consists of an encoder and LLM embeddings, and we propose two contrastive learning losses to train the RouterDC model. Experimental results show that RouterDC is effective in assembling LLMs and largely outperforms individual top-performing LLMs as well as existing routing methods on both in-distribution (+2.76\%) and out-of-distribution (+1.90\%) tasks. Source code is available at
this https URL
.
Comments:
Accepted by NeurIPS 2024
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2409.19886
[cs.LG]
(or
arXiv:2409.19886v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2409.19886
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Shuhao Chen [
view email
]
[v1]
Mon, 30 Sep 2024 02:31:40 UTC (1,846 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models, by Shuhao Chen and 4 other authors
View PDF
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
2024-09
Change to browse by:
cs
cs.AI
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