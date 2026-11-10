---
title: '[2606.03852] FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement'
id: 260603852-flare-fine-grained-diagnostic-feedback-for-llm-code-refinement
tags:
- code-llm-calibration-aaai27-eabf3f
- aaai-bar-eval-dprc-d78e07
- code-llm-probe-verbalize-gap-3d8995
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-17T19:24:36.741756Z'
updated: '2026-11-09T23:25:59.766127Z'
source: https://arxiv.org/abs/2606.03852
source_domain: arxiv.org
fetched_at: '2026-07-17T19:24:36.741441Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Abstract-only arXiv page for FLARE (2606.03852); full text fetched separately
  at note flare-fine-grained-diagnostic-feedback-for-llm-code-refinement. See that
  note for full occupancy analysis.
---

[2606.03852] FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2606.03852
(cs)
[Submitted on 2 Jun 2026]
Title:
FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement
Authors:
Yinsheng Yao
,
Hongxiang Zhang
,
Weixi Tong
,
Tianyi Zhang
View a PDF of the paper titled FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement, by Yinsheng Yao and Hongxiang Zhang and Weixi Tong and Tianyi Zhang
View PDF
HTML (experimental)
Abstract:
Large language models often generate code with bugs. Existing methods rely on feedback signals such as test failures and self-critiques to iteratively refine the generated code. Such signals are either too coarse-grained or too high-level, which is not sufficient to inform the model where to fix the bug. In this work, we present Flare, an iterative framework with a lightweight diagnostic model that predicts line-level suspiciousness signals for bug localization and code refinement. Given the inherent uncertainty of diagnostic predictions, Flare searches over the top-k suspicious regions and selects the best candidate according to execution outcomes. Experiments on LiveCodeBench and BigCodeBench with five base LLMs show that, even without candidate search (k=1), Flare outperforms the strongest baseline with an absolute improvement from 1.72% to 7.42%. Furthermore, searching over 10 candidates yields an average improvement of 8.50% compared with no candidate search. When evaluated in isolation, our lightweight diagnostic model achieves the best performance compared with recent fault localization methods, demonstrating that it can provide reliable fine-grained guidance for code refinement.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2606.03852
[cs.SE]
(or
arXiv:2606.03852v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2606.03852
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Hongxiang Zhang [
view email
]
[v1]
Tue, 2 Jun 2026 16:29:17 UTC (478 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement, by Yinsheng Yao and Hongxiang Zhang and Weixi Tong and Tianyi Zhang
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
2026-06
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