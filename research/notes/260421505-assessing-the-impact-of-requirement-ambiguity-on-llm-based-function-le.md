---
title: '[2604.21505] Assessing the Impact of Requirement Ambiguity on LLM-based Function-Level
  Code Generation'
id: 260421505-assessing-the-impact-of-requirement-ambiguity-on-llm-based-function-le
tags:
- code-llm-requirement-pivots-5d35f5
- spec-ambiguity
- whole-task-granularity
created: '2026-07-20T06:54:00.984049Z'
updated: '2026-07-20T06:56:06.672857Z'
source: https://arxiv.org/abs/2604.21505
source_domain: arxiv.org
fetched_at: '2026-07-20T06:54:00.983711Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Introduces Orchid, the first code-gen benchmark with deliberately ambiguous
  requirements: 1,304 function-level tasks tagged with one of four ambiguity types
  (lexical, syntactic, semantic, vagueness). Operates at WHOLE-TASK granularity --
  each task carries one ambiguity label and is scored on whole-function pass/fail
  -- not decomposed into per-sub-requirement ambiguity within a single multi-requirement
  task. Finds ambiguity consistently degrades LLM performance (worst for the most
  advanced models) and that models produce functionally divergent implementations
  for the same ambiguous prompt, with no autonomous ambiguity detection/resolution
  capability.'
---

[2604.21505] Assessing the Impact of Requirement Ambiguity on LLM-based Function-Level Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2604.21505
(cs)
[Submitted on 23 Apr 2026]
Title:
Assessing the Impact of Requirement Ambiguity on LLM-based Function-Level Code Generation
Authors:
Di Yang
,
Xinou Xie
,
Xiuwen Yang
,
Ming Hu
,
Yihao Huang
,
Yueling Zhang
,
Weikai Miao
,
Ting Su
,
Chengcheng Wan
,
Geguang Pu
View a PDF of the paper titled Assessing the Impact of Requirement Ambiguity on LLM-based Function-Level Code Generation, by Di Yang and 9 other authors
View PDF
HTML (experimental)
Abstract:
Software requirement ambiguity is ubiquitous in real-world development, stemming from the inherent imprecision of natural language and the varying interpretations of stakeholders. While Large Language Models (LLMs) have demonstrated impressive capabilities in generating code from precise specifications, such ambiguity poses a significant obstacle to reliable automated code generation. Existing benchmarks typically assume clear and unambiguous requirements, leaving an empirical gap in understanding how LLMs behave when faced with the inherent uncertainty of real-world software requirements. In this paper, we introduce Orchid, the first code generation benchmark specifically designed with ambiguous requirements. It comprises 1,304 function-level tasks covering four distinct types of ambiguity: lexical, syntactic, semantic, and vagueness. Leveraging this dataset, we conduct the first systematic empirical study to evaluate the impact of requirement ambiguity on LLM-based code generation. Our results demonstrate that ambiguity consistently degrades the performance of all evaluated LLMs, with the most pronounced negative effects observed in highly advanced models. Furthermore, we observe that LLMs frequently produce functionally divergent implementations for the same ambiguous requirement and lack the capability to identify or resolve such ambiguity autonomously. These findings reveal a significant performance gap between clear and ambiguous requirements, underscoring the urgent need for ambiguity-aware techniques in the next generation of automated software engineering tools. The Orchid benchmark is publicly available at
this https URL
.
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2604.21505
[cs.SE]
(or
arXiv:2604.21505v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2604.21505
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Di Yang [
view email
]
[v1]
Thu, 23 Apr 2026 10:07:33 UTC (884 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Assessing the Impact of Requirement Ambiguity on LLM-based Function-Level Code Generation, by Di Yang and 9 other authors
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
2026-04
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