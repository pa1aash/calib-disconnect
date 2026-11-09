---
title: '[2506.22716] BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute'
id: 250622716-best-route-adaptive-llm-routing-with-test-time-optimal-compute
tags:
- code-llm-requirement-pivots-5d35f5
- llm-routing
- adaptive-best-of-n
created: '2026-07-20T06:52:57.195965Z'
updated: '2026-07-20T06:55:25.470858Z'
source: https://arxiv.org/abs/2506.22716
source_domain: arxiv.org
fetched_at: '2026-07-20T06:52:57.195643Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Ding et al. (Microsoft/UBC, ICML 2025): BEST-Route routes each incoming
  query to a model AND decides how many samples (best-of-n) to draw from that model,
  jointly optimizing cost vs quality based on predicted query difficulty and a quality
  threshold. Reduces cost up to 60% with <1% performance drop on real-world datasets.
  Routing and compute-allocation decisions are made per-query (whole task), evaluated
  on general LLM benchmarks, not code generation or sub-task/requirement granularity.
  Confirms ''compute allocation via routing'' is scooped at whole-query level; per-requirement
  routing within a single code problem is untouched.'
---

[2506.22716] BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2506.22716
(cs)
[Submitted on 28 Jun 2025]
Title:
BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute
Authors:
Dujian Ding
,
Ankur Mallick
,
Shaokun Zhang
,
Chi Wang
,
Daniel Madrigal
,
Mirian Del Carmen Hipolito Garcia
,
Menglin Xia
,
Laks V.S. Lakshmanan
,
Qingyun Wu
,
Victor Rühle
View a PDF of the paper titled BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute, by Dujian Ding and 9 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) are powerful tools but are often expensive to deploy at scale. LLM query routing mitigates this by dynamically assigning queries to models of varying cost and quality to obtain a desired trade-off. Prior query routing approaches generate only one response from the selected model and a single response from a small (inexpensive) model was often not good enough to beat a response from a large (expensive) model due to which they end up overusing the large model and missing out on potential cost savings. However, it is well known that for small models, generating multiple responses and selecting the best can enhance quality while remaining cheaper than a single large-model response. We leverage this idea to propose BEST-Route, a novel routing framework that chooses a model and the number of responses to sample from it based on query difficulty and the quality thresholds. Experiments on real-world datasets demonstrate that our method reduces costs by up to 60% with less than 1% performance drop.
Comments:
Accepted to ICML 2025 (main conference)
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL); Databases (cs.DB)
Cite as:
arXiv:2506.22716
[cs.LG]
(or
arXiv:2506.22716v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2506.22716
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Dujian Ding [
view email
]
[v1]
Sat, 28 Jun 2025 01:52:50 UTC (258 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute, by Dujian Ding and 9 other authors
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
2025-06
Change to browse by:
cs
cs.AI
cs.CL
cs.DB
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