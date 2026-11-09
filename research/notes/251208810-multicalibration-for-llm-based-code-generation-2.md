---
title: '[2512.08810] Multicalibration for LLM-based Code Generation'
id: 251208810-multicalibration-for-llm-based-code-generation-2
tags:
- aaai-bar-eval-dprc-d78e07
created: '2026-07-19T20:06:17.151528Z'
updated: '2026-07-19T20:06:45.310552Z'
source: https://arxiv.org/abs/2512.08810
source_domain: arxiv.org
fetched_at: '2026-07-19T20:06:17.151135Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'NOT an AAAI paper -- accepted at AI-SQE 2026 (1st Intl Workshop on AI for
  Software Quality Evaluation), submitted arXiv 9 Dec 2025. Campos, Kuschnereit, Ulges
  study multicalibration (calibration conditioned on problem sub-groups: complexity,
  code length, programming language) for code LLM confidence, testing 4 multicalibration
  approaches on 3 function-synthesis benchmarks across Qwen3 Coder, GPT-OSS, DeepSeek-R1-Distill.
  Reports +1.03 skill-score improvement over uncalibrated token likelihoods and +0.37
  over baseline calibrations; releases a public dataset of code generations + likelihoods
  + correctness labels. Relevance to DPRC: adjacent competitive-landscape work in
  the exact code-LLM-calibration niche, confirming the subfield is workshop-tier active
  but this specific multicalibration angle has NOT yet cleared an AAAI/top-tier main-track
  bar -- it targets SCALAR per-problem calibration conditioned on metadata factors,
  not DPRC''s per-requirement/per-unittest localized confidence. Its workshop (not
  main-track) placement is itself evidence that scalar code-calibration work with
  3 benchmarks/3 models sits below the AAAI main-track bar without a stronger novelty
  hook.'
---

*Suggested by [[aaai-2026-highlights-award-winners-trends-key-papers]] — code-LLM calibration search lead, direct comparable to DPRC subarea*

[2512.08810] Multicalibration for LLM-based Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2512.08810
(cs)
[Submitted on 9 Dec 2025]
Title:
Multicalibration for LLM-based Code Generation
Authors:
Viola Campos
,
Robin Kuschnereit
,
Adrian Ulges
View a PDF of the paper titled Multicalibration for LLM-based Code Generation, by Viola Campos and 2 other authors
View PDF
HTML (experimental)
Abstract:
As AI-based code generation becomes widespread, researchers are investigating the calibration of code LLMs - ensuring their confidence scores faithfully represent the true likelihood of code correctness. To do so, we investigate multicalibration, which can capture additional factors about a coding problem, such as complexity, code length, or programming language used. We study four multicalibration approaches on three function synthesis benchmarks, using latest-generation code LLMs (Qwen3 Coder, GPT-OSS, DeepSeek-R1-Distill). Our results demonstrate that multicalibration can yield distinct improvements over both uncalibrated token likelihoods (+1.03 in skill score) and baseline calibrations (+0.37 in skill score). We study the influence of the aforementioned factors in ablations, and make our dataset (consisting of code generations, likelihoods, and correctness labels) available for future research on code LLM calibration.
Comments:
Accepted at AI-SQE 2026 (The 1st International Workshop on AI for Software Quality Evaluation: Judgment, Metrics, Benchmarks, and Beyond)
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
MSC
classes:
I.2.2, D.2.4
Cite as:
arXiv:2512.08810
[cs.SE]
(or
arXiv:2512.08810v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2512.08810
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Viola Campos [
view email
]
[v1]
Tue, 9 Dec 2025 17:04:01 UTC (141 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Multicalibration for LLM-based Code Generation, by Viola Campos and 2 other authors
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
2025-12
Change to browse by:
cs
cs.AI
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