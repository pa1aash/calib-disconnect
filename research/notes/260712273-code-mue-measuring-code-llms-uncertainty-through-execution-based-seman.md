---
title: '[2607.12273] Code-MUE: Measuring Code LLMs'' Uncertainty through Execution-based
  Semantic Interaction Graphs'
id: 260712273-code-mue-measuring-code-llms-uncertainty-through-execution-based-seman
tags:
- aaai-bar-eval-dprc-d78e07
- code-uncertainty-estimation
- scalar-not-localized
- downstream-utility-scalar-only
- code-llm-probe-verbalize-gap-3d8995
- code-llm-confidence-positioning-d82d00
- duplicate
- duplicate-abstract-only
created: '2026-07-19T20:02:56.354763Z'
updated: '2026-11-09T23:26:01.754755Z'
source: https://arxiv.org/abs/2607.12273
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:56.354405Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Short older note; full text is in code-mue-measuring-code-llms-uncertainty-through-execution-based-semantic-intera.
---

*Suggested by [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement]] — downstream-utility candidate for localized/execution-based code confidence*

[2607.12273] Code-MUE: Measuring Code LLMs' Uncertainty through Execution-based Semantic Interaction Graphs
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2607.12273
(cs)
[Submitted on 14 Jul 2026]
Title:
Code-MUE: Measuring Code LLMs' Uncertainty through Execution-based Semantic Interaction Graphs
Authors:
Xiaoning Ren
,
Yinxing Xue
,
Lei Ma
,
Yuheng Huang
View a PDF of the paper titled Code-MUE: Measuring Code LLMs' Uncertainty through Execution-based Semantic Interaction Graphs, by Xiaoning Ren and 3 other authors
View PDF
HTML (experimental)
Abstract:
As Code Large Language Models (LLMs) become central to modern software engineering, their inherent stochasticity poses significant real-world risks, where even minor errors can lead to severe functional, security, or safety consequences. Reliable automation, therefore, demands the ability to distinguish between confident, well-supported predictions and stochastic guessing. However, existing uncertainty estimation methods face a critical gap: white and grey-box techniques are often inapplicable to closed-source models, while standard "black-box" text metrics fail to capture the unique fragility of code, where syntactic variation does not always imply semantic divergence. To bridge this syntax-semantics gap, we introduce Code-MUE, a purely black-box framework that measures uncertainty through execution-based Semantic Interaction Graphs. Unlike prior approaches that rely on superficial textual similarity, Code-MUE grounds uncertainty in observable runtime behavior, calculating the Von Neumann entropy of the solution space to quantify global semantic diversity. A large-scale empirical study across eight state-of-the-art LLMs demonstrates that Code-MUE achieves a strong negative correlation with functional correctness (Spearman's correlation up to -0.98), significantly outperforming lexical and embedding-based baselines while enabling robust risk detection and selective prediction in practical workflows.
Comments:
To appear at The ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA) 2026
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2607.12273
[cs.SE]
(or
arXiv:2607.12273v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2607.12273
Focus to learn more
arXiv-issued DOI via DataCite (pending registration)
Submission history
From: Yuheng Huang [
view email
]
[v1]
Tue, 14 Jul 2026 02:23:17 UTC (1,287 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Code-MUE: Measuring Code LLMs' Uncertainty through Execution-based Semantic Interaction Graphs, by Xiaoning Ren and 3 other authors
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
2026-07
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