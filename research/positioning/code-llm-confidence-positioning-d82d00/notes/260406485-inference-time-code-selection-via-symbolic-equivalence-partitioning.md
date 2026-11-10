---
title: '[2604.06485] Inference-Time Code Selection via Symbolic Equivalence Partitioning'
id: 260406485-inference-time-code-selection-via-symbolic-equivalence-partitioning
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:07:36.258514Z'
updated: '2026-11-09T23:27:43.002803Z'
source: https://arxiv.org/abs/2604.06485
source_domain: arxiv.org
fetched_at: '2026-11-09T23:07:36.258048Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '[2604.06485] Inference-Time Code Selection via Symbolic Equivalence Partitioning'
---

[2604.06485] Inference-Time Code Selection via Symbolic Equivalence Partitioning
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2604.06485
(cs)
[Submitted on 7 Apr 2026 (
v1
), last revised 11 May 2026 (this version, v2)]
Title:
Inference-Time Code Selection via Symbolic Equivalence Partitioning
Authors:
David Cho
,
Yifan Wang
,
Fanping Sui
,
Ananth Grama
View a PDF of the paper titled Inference-Time Code Selection via Symbolic Equivalence Partitioning, by David Cho and 3 other authors
View PDF
HTML (experimental)
Abstract:
Sampling multiple candidate programs at inference time is an effective way to improve LLM code generation. However, its benefit depends on reliably selecting a correct solution from the generated pool. We observe that this selection problem has a distinctive semantic structure: correct solutions, despite differences in syntax, implementation, or algorithmic strategy, often converge to the same functional behavior over valid inputs. At the same time, consensus alone is not sufficient for correctness, because models can also produce correlated wrong solutions that implement the same mistaken behavior. We propose Symbolic Equivalence Partitioning (SEP), an inference-time selection framework that first uses problem-provided public examples as lightweight validity signals. SEP then uses symbolic execution to partition the remaining candidate programs into bounded functional equivalence classes and selects from the dominant equivalence class. Across HumanEval+ and LiveCodeBench, SEP consistently improves selection accuracy without auxiliary test generation, learned verifiers, or additional LLM inference. At $N=10$, SEP improves average accuracy from 0.754 to 0.826 on HumanEval+ and from 0.565 to 0.647 on LiveCodeBench, showing that symbolic functional agreement is an effective signal for inference-time code selection.
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2604.06485
[cs.LG]
(or
arXiv:2604.06485v2
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2604.06485
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: David Cho [
view email
]
[v1]
Tue, 7 Apr 2026 21:37:59 UTC (538 KB)
[v2]
Mon, 11 May 2026 22:03:07 UTC (1,633 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Inference-Time Code Selection via Symbolic Equivalence Partitioning, by David Cho and 3 other authors
View PDF
HTML (experimental)
TeX Source
view license
Additional Features
Audio Summary
Current browse context:
cs.LG
< prev
|
next >
new
|
recent
|
2026-04
Change to browse by:
cs
cs.AI
References & Citations
SciX
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