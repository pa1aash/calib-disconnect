---
title: '[2606.09800] FASE: Fast Adaptive Semantic Entropy for Code Quality'
id: 260609800-fase-fast-adaptive-semantic-entropy-for-code-quality
tags:
- code-llm-calibration-aaai27-eabf3f
created: '2026-07-17T18:29:36.968793Z'
updated: '2026-07-17T18:32:47.971714Z'
source: http://arxiv.org/abs/2606.09800
source_domain: arxiv.org
fetched_at: '2026-07-17T18:29:36.967906Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Abstract-only duplicate of the full-text note (fase-fast-adaptive-semantic-entropy-for-code-quality);
  superseded.
---

[2606.09800] FASE: Fast Adaptive Semantic Entropy for Code Quality
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2606.09800
(cs)
[Submitted on 8 Jun 2026]
Title:
FASE: Fast Adaptive Semantic Entropy for Code Quality
Authors:
Shizhe Lin
,
Ladan Tahvildari
View a PDF of the paper titled FASE: Fast Adaptive Semantic Entropy for Code Quality, by Shizhe Lin and Ladan Tahvildari
View PDF
HTML (experimental)
Abstract:
Multi-agent code generation offers a promising paradigm for autonomous software development by simulating the human software engineering lifecycle. However, system reliability remains hindered by LLM hallucinations and error propagation across interacting agents. While semantic entropy provides a principled way to quantify uncertainty without ground-truth answers, current methods often rely on costly LLM-driven equivalence checks. In this work, we introduce Fast Adaptive Semantic Entropy (FASE), a novel metric that approximates functional correctness based on the minimum spanning tree of structural and semantic dissimilarity graphs. Evaluations on HumanEval and BigCodeBench demonstrate that FASE outperforms state-of-the-art semantic entropy by LLM entailment, achieving a 25% average improvement in Spearman correlation and a 19% increase in ROCAUC score against Pass@1 from ground-truth test cases when using the Qwen3-Embedding-8B model. Furthermore, by eliminating costly LLM-driven equivalence evaluation, FASE incurs negligible computational overhead, requiring only approximately 0.3% of the runtime cost of traditional semantic entropy approaches. These results position FASE as a practical, cost-effective solution for optimizing uncertainty quantification in real-world multi-agent workflows.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Multiagent Systems (cs.MA)
Cite as:
arXiv:2606.09800
[cs.SE]
(or
arXiv:2606.09800v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2606.09800
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Shizhe Lin [
view email
]
[v1]
Mon, 8 Jun 2026 17:53:05 UTC (1,950 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled FASE: Fast Adaptive Semantic Entropy for Code Quality, by Shizhe Lin and Ladan Tahvildari
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
cs.MA
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