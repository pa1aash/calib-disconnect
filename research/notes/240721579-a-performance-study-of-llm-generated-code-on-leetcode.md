---
title: '[2407.21579] A Performance Study of LLM-Generated Code on Leetcode'
id: 240721579-a-performance-study-of-llm-generated-code-on-leetcode
tags:
- code-llm-requirement-pivots-5d35f5
- partial-pass-corroboration
created: '2026-07-20T06:54:29.810818Z'
updated: '2026-07-20T06:56:04.173464Z'
source: https://arxiv.org/abs/2407.21579
source_domain: arxiv.org
fetched_at: '2026-07-20T06:54:29.810467Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Compares 18 LLMs on LeetCode problems for both correctness and runtime efficiency
  of generated solutions vs human-crafted code. Reports LLM-generated code is on average
  as fast or faster than human solutions when it passes. Third-party synthesis of
  this paper's pass-rate data describes it as 'skewed towards pass rates of 1.0 and
  0.0, demonstrating a bimodal distribution' attributed to self-consistency bias (models
  that generate a solution also tend to believe it's correct) and to outright failures
  (bad test cases, timeouts). This is a second independent LeetCode-based corroboration
  (alongside 'Beyond Pass Rate') that competitive/algorithmic-style coding benchmarks
  produce near-binary/bimodal pass-rate distributions rather than the graded partial-pass
  distribution we observe on BigCodeBench-style functional tasks.
---

[2407.21579] A Performance Study of LLM-Generated Code on Leetcode
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2407.21579
(cs)
[Submitted on 31 Jul 2024]
Title:
A Performance Study of LLM-Generated Code on Leetcode
Authors:
Tristan Coignion
,
Clément Quinton
,
Romain Rouvoy
View a PDF of the paper titled A Performance Study of LLM-Generated Code on Leetcode, by Tristan Coignion and 2 other authors
View PDF
HTML (experimental)
Abstract:
This study evaluates the efficiency of code generation by Large Language Models (LLMs) and measures their performance against human-crafted solutions using a dataset from Leetcode. We compare 18 LLMs, considering factors such as model temperature and success rate, and their impact on code performance. This research introduces a novel method for measuring and comparing the speed of LLM-generated code, revealing that LLMs produce code with comparable performance, irrespective of the adopted LLM. We also find that LLMs are capable of generating code that is, on average, more efficient than the code written by humans. The paper further discusses the use of Leetcode as a benchmarking dataset, the limitations imposed by potential data contamination, and the platform's measurement reliability. We believe that our findings contribute to a better understanding of LLM capabilities in code generation and set the stage for future optimizations in the field.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2407.21579
[cs.SE]
(or
arXiv:2407.21579v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2407.21579
Focus to learn more
arXiv-issued DOI via DataCite
Journal reference:
Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering, 2024
Related DOI
:
https://doi.org/10.1145/3661167.3661221
Focus to learn more
DOI(s) linking to related resources
Submission history
From: Tristan Coignion [
view email
]
[v1]
Wed, 31 Jul 2024 13:10:03 UTC (708 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled A Performance Study of LLM-Generated Code on Leetcode, by Tristan Coignion and 2 other authors
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
2024-07
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