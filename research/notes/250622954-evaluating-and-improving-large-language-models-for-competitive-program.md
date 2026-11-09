---
title: '[2506.22954] Evaluating and Improving Large Language Models for Competitive
  Program Generation'
id: 250622954-evaluating-and-improving-large-language-models-for-competitive-program
tags:
- aaai-bar-eval-dprc-d78e07
- competitive-programming
- all-or-nothing
- error-taxonomy
created: '2026-07-19T20:02:54.966994Z'
updated: '2026-07-19T20:06:25.740654Z'
source: https://arxiv.org/abs/2506.22954
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:54.966626Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Wei, Li, Chen, Zheng, Qu, Yu, Chen, Ju (arXiv 2506.22954, Jun 2025, cs.SI/cs.SE,
  not yet confirmed at a peer-reviewed venue). Curates 80 contamination-resistant
  problems from 9 regional 2024 ICPC/CCPC contests and evaluates DeepSeek-R1 via online-judge
  submission. Key number: only 5/80 (6.25%) problems fully accepted with a basic prompt
  -- underscoring the all-or-nothing grading regime of competitive programming (a
  solution is judged correct only if it passes ALL hidden tests on the OJ; there is
  no partial credit reported at the headline level). Builds a fine-grained error taxonomy
  (general: design/boundary/condition/data-type/syntax/I-O errors; specialized: math,
  greedy, graph-theory errors) and a repair framework (multi-turn dialogue repair
  + information-augmented regeneration) that raises accepted solutions from 5/80 to
  46/80. Corroborates DPRC''s TACO finding: competitive-programming correctness is
  binary/all-or-nothing at the OJ-acceptance level, which is the structural reason
  per-requirement (sub-test) confidence collapses to a scalar signal on competitive
  code -- there is no requirement-level partial-pass distribution to localize confidence
  against until iterative repair is applied.'
---

[2506.22954] Evaluating and Improving Large Language Models for Competitive Program Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Social and Information Networks
arXiv:2506.22954
(cs)
[Submitted on 28 Jun 2025]
Title:
Evaluating and Improving Large Language Models for Competitive Program Generation
Authors:
Minnan Wei
,
Ziming Li
,
Xiang Chen
,
Menglin Zheng
,
Ziyan Qu
,
Cheng Yu
,
Siyu Chen
,
Xiaolin Ju
View a PDF of the paper titled Evaluating and Improving Large Language Models for Competitive Program Generation, by Minnan Wei and 6 other authors
View PDF
HTML (experimental)
Abstract:
Context: Due to the demand for strong algorithmic reasoning, complex logic implementation, and strict adherence to input/output formats and resource constraints, competitive programming generation by large language models (LLMs) is considered the most challenging problem in current LLM-based code generation. However, previous studies often evaluate LLMs using simple prompts and benchmark datasets prone to data leakage. Moreover, prior work has limited consideration of the diversity in algorithm types and difficulty levels. Objective: In this study, we aim to evaluate and improve LLMs in solving real-world competitive programming problems. Methods: We initially collect 117 problems from nine regional ICPC/CCPC contests held in 2024 and design four filtering criteria to construct a curated benchmark consisting of 80 problems. Leveraging DeepSeek-R1 as the LLM, we evaluate its competitive program generation capabilities through the online judge (OJ) platforms, guided by a carefully designed basic prompt. For incorrect submissions, we construct a fine-grained error taxonomy and then propose a targeted improvement framework by combining a multi-turn dialogue-based repair phase and an information-augmented regeneration phase. Results: Experimental results show that only 5 out of 80 problems are fully accepted when using basic prompts. For the unsolved problems, we construct the error taxonomy, including general errors (such as design, boundary, condition, data type, syntax, and input/output errors) and specialized errors (such as those in mathematical problems, greedy algorithms, and graph theories). After applying our proposed improvement strategies, we substantially increased the number of correct solutions, with 46 out of 80 problems successfully accepted.
Subjects:
Social and Information Networks (cs.SI)
; Software Engineering (cs.SE)
Cite as:
arXiv:2506.22954
[cs.SI]
(or
arXiv:2506.22954v1
[cs.SI]
for this version)
https://doi.org/10.48550/arXiv.2506.22954
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Minnan Wei [
view email
]
[v1]
Sat, 28 Jun 2025 17:18:23 UTC (14,387 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Evaluating and Improving Large Language Models for Competitive Program Generation, by Minnan Wei and 6 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.SI
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
cs.SE
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