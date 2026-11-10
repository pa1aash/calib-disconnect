---
title: '[2306.09896] Is Self-Repair a Silver Bullet for Code Generation?'
id: 230609896-is-self-repair-a-silver-bullet-for-code-generation
tags:
- code-llm-requirement-pivots-5d35f5
- self-repair
- code-repair
- baseline
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-20T06:53:21.925142Z'
updated: '2026-11-09T23:26:04.797462Z'
source: https://arxiv.org/abs/2306.09896
source_domain: arxiv.org
fetched_at: '2026-07-20T06:53:21.924683Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Olausson, Inala, Wang, Gao, Solar-Lezama (ICLR 2024): rigorous evaluation
  of self-repair (model debugs and fixes its own code) on Code Llama, GPT-3.5, GPT-4
  across HumanEval and APPS. Central finding: when the COST of performing repair is
  accounted for (i.e., compared against just spending that compute on more initial
  samples), performance gains from self-repair are ''often modest, vary a lot between
  subsets of the data, and are sometimes not present at all.'' The bottleneck is identified
  as the model''s own ability to generate useful feedback on its own code -- artificially
  boosting feedback quality with a stronger model yields substantially larger gains,
  and even GPT-4 self-repair ''lags far behind'' human-level debugging feedback. Operates
  at whole-program granularity: one feedback pass, one repair pass, no per-requirement
  targeting. This is the canonical negative/cautionary result the parent agent already
  flagged as ruling out plain ''targeted repair'' as incremental -- it establishes
  that repair quality is bottlenecked by FEEDBACK QUALITY, which is exactly what a
  validated per-requirement probe/self-report signal could fix if requirement-level
  feedback is more localized/precise than whole-program feedback.'
---

[2306.09896] Is Self-Repair a Silver Bullet for Code Generation?
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2306.09896
(cs)
[Submitted on 16 Jun 2023 (
v1
), last revised 2 Feb 2024 (this version, v5)]
Title:
Is Self-Repair a Silver Bullet for Code Generation?
Authors:
Theo X. Olausson
,
Jeevana Priya Inala
,
Chenglong Wang
,
Jianfeng Gao
,
Armando Solar-Lezama
View a PDF of the paper titled Is Self-Repair a Silver Bullet for Code Generation?, by Theo X. Olausson and 4 other authors
View PDF
Abstract:
Large language models have shown remarkable aptitude in code generation, but still struggle to perform complex tasks. Self-repair -- in which the model debugs and repairs its own code -- has recently become a popular way to boost performance in these settings. However, despite its increasing popularity, existing studies of self-repair have been limited in scope; in many settings, its efficacy thus remains poorly understood. In this paper, we analyze Code Llama, GPT-3.5 and GPT-4's ability to perform self-repair on problems taken from HumanEval and APPS. We find that when the cost of carrying out repair is taken into account, performance gains are often modest, vary a lot between subsets of the data, and are sometimes not present at all. We hypothesize that this is because self-repair is bottlenecked by the model's ability to provide feedback on its own code; using a stronger model to artificially boost the quality of the feedback, we observe substantially larger performance gains. Similarly, a small-scale study in which we provide GPT-4 with feedback from human participants suggests that even for the strongest models, self-repair still lags far behind what can be achieved with human-level debugging.
Comments:
Accepted to ICLR 2024. Added additional Code Llama experiments and fixed a data processing error harming Code Llama's reported self-repair performance on HumanEval
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Programming Languages (cs.PL); Software Engineering (cs.SE)
Cite as:
arXiv:2306.09896
[cs.CL]
(or
arXiv:2306.09896v5
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2306.09896
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Theo Olausson [
view email
]
[v1]
Fri, 16 Jun 2023 15:13:17 UTC (906 KB)
[v2]
Tue, 20 Jun 2023 04:38:43 UTC (906 KB)
[v3]
Thu, 22 Jun 2023 17:55:21 UTC (906 KB)
[v4]
Tue, 17 Oct 2023 17:51:27 UTC (1,107 KB)
[v5]
Fri, 2 Feb 2024 18:31:34 UTC (1,255 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Is Self-Repair a Silver Bullet for Code Generation?, by Theo X. Olausson and 4 other authors
View PDF
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
2023-06
Change to browse by:
cs
cs.AI
cs.PL
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