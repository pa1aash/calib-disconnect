---
title: '[2507.22462] IFEvalCode: Controlled Code Generation'
id: 250722462-ifevalcode-controlled-code-generation
tags:
- code-llm-requirement-pivots-5d35f5
- adjacent-not-scooping
created: '2026-07-20T06:52:52.028234Z'
updated: '2026-07-20T06:55:55.577401Z'
source: https://arxiv.org/abs/2507.22462
source_domain: arxiv.org
fetched_at: '2026-07-20T06:52:52.027866Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'IFEvalCode (1.6K samples, 7 languages, EN+ZH queries, 40+ LLMs evaluated):
  decouples code eval into two axes -- Correctness (functional pass/fail) and Instruction-Following
  (adherence to style/line-count/structural constraints via forward+backward constraint
  generation). This is a two-metric decoupling, not a per-requirement/per-unittest
  partial-credit protocol; the ''instruction constraints'' are generation-time formatting/style
  directives, not functional sub-behaviors tested by separate unittest methods. Finding:
  large gap between models'' raw correctness and their constraint-adherence, i.e.
  models that write correct code often violate explicit formatting/structural instructions.
  Adjacent to but distinct from requirement-level functional partial credit.'
---

[2507.22462] IFEvalCode: Controlled Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2507.22462
(cs)
[Submitted on 30 Jul 2025 (
v1
), last revised 1 Aug 2025 (this version, v2)]
Title:
IFEvalCode: Controlled Code Generation
Authors:
Jian Yang
,
Wei Zhang
,
Shukai Liu
,
Linzheng Chai
,
Yingshui Tan
,
Jiaheng Liu
,
Ge Zhang
,
Wangchunshu Zhou
,
Guanglin Niu
,
Zhoujun Li
,
Binyuan Hui
,
Junyang Lin
View a PDF of the paper titled IFEvalCode: Controlled Code Generation, by Jian Yang and 11 other authors
View PDF
HTML (experimental)
Abstract:
Code large language models (Code LLMs) have made significant progress in code generation by translating natural language descriptions into functional code; however, real-world applications often demand stricter adherence to detailed requirements such as coding style, line count, and structural constraints, beyond mere correctness. To address this, the paper introduces forward and backward constraints generation to improve the instruction-following capabilities of Code LLMs in controlled code generation, ensuring outputs align more closely with human-defined guidelines. The authors further present IFEvalCode, a multilingual benchmark comprising 1.6K test samples across seven programming languages (Python, Java, JavaScript, TypeScript, Shell, C++, and C#), with each sample featuring both Chinese and English queries. Unlike existing benchmarks, IFEvalCode decouples evaluation into two metrics: correctness (Corr.) and instruction-following (Instr.), enabling a more nuanced assessment. Experiments on over 40 LLMs reveal that closed-source models outperform open-source ones in controllable code generation and highlight a significant gap between the models' ability to generate correct code versus code that precisely follows instructions.
Comments:
10 pages
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2507.22462
[cs.CL]
(or
arXiv:2507.22462v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2507.22462
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Jian Yang [
view email
]
[v1]
Wed, 30 Jul 2025 08:08:48 UTC (5,752 KB)
[v2]
Fri, 1 Aug 2025 10:07:37 UTC (5,753 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled IFEvalCode: Controlled Code Generation, by Jian Yang and 11 other authors
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