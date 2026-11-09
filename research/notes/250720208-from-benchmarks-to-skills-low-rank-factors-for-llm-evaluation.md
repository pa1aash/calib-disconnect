---
title: '[2507.20208] From Benchmarks to Skills: Low-Rank Factors for LLM Evaluation'
id: 250720208-from-benchmarks-to-skills-low-rank-factors-for-llm-evaluation
tags:
- code-llm-best-aaai-paper-6ded37
- capability-science
- latent-skill-factor-analysis
created: '2026-07-20T07:40:14.282359Z'
updated: '2026-07-20T07:45:37.050268Z'
source: https://arxiv.org/abs/2507.20208
source_domain: arxiv.org
fetched_at: '2026-07-20T07:40:14.281987Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Applies Factor Analysis to a 60-model x 44-benchmark performance matrix
  and finds intrinsically LOW-RANK structure: a small number of latent factors explain
  most cross-benchmark variance, meaning many benchmarks measure overlapping abilities
  rather than independent skills. The latent factors correspond to coherent, skill-like
  dimensions of LLM behavior. Delivers three tools: redundant-task identification,
  new-model profiling from a small task subset, and model selection by desired skill
  profile. Closest-work candidate for the capability-science angle, but operates at
  the BENCHMARK level (whole tasks as items, models as rows) not at the per-requirement/sub-test
  level within a single code-generation problem, and does not analyze cross-model-family
  sharing of specific failure patterns.'
---

[2507.20208] From Benchmarks to Skills: Low-Rank Factors for LLM Evaluation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2507.20208
(cs)
[Submitted on 27 Jul 2025 (
v1
), last revised 11 Jun 2026 (this version, v2)]
Title:
From Benchmarks to Skills: Low-Rank Factors for LLM Evaluation
Authors:
Aviya Maimon
,
Amir DN Cohen
,
Gal Vishne
,
Shauli Ravfogel
,
Reut Tsarfaty
View a PDF of the paper titled From Benchmarks to Skills: Low-Rank Factors for LLM Evaluation, by Aviya Maimon and 4 other authors
View PDF
HTML (experimental)
Abstract:
Current evaluations of large language models (LLMs) rely heavily on a growing collection of benchmarks and on aggregate benchmark scores, yet it remains unclear what this comparison actually captures, and what these scores reveal about models' underlying capabilities. Here, we propose a new paradigm for LLM evaluation, by asking whether benchmark performance reflects many independent abilities, or rather relies on a small number of shared dimensions. To answer this, we apply Factor Analysis (FA) to a massive performance matrix of LLMs versus benchmarks \((60\times44)\) revealing an \emph{intrinsically low-rank} structure of that matrix. That is, a small number of latent factors captures most of the structure in the full task space. This low-rank geometry reveals substantial redundancy across existing tasks and explains why many benchmarks appear to be measuring overlapping abilities. We further show that these latent factors correspond to coherent, skill-like, dimensions of LLM behavior. Leveraging this latent skill-space, we deliver three practical tools for LLM evaluation and downstream users: (i)~identifying redundant tasks, (ii)~profiling new models using a small subset of tasks, and (iii)~selecting models aligned with desired skill profiles. Our method provides a solid alternative to the de-facto standard of a single aggregate score, and establishes an interpretable and practical framework for understanding and benchmarking LLM core capabilities.
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2507.20208
[cs.CL]
(or
arXiv:2507.20208v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2507.20208
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Aviya Maimon [
view email
]
[v1]
Sun, 27 Jul 2025 10:11:16 UTC (1,930 KB)
[v2]
Thu, 11 Jun 2026 05:27:45 UTC (2,221 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled From Benchmarks to Skills: Low-Rank Factors for LLM Evaluation, by Aviya Maimon and 4 other authors
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
2025-07
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