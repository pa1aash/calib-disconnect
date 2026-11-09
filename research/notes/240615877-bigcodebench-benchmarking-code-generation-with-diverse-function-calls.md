---
title: '[2406.15877] BigCodeBench: Benchmarking Code Generation with Diverse Function
  Calls and Complex Instructions'
id: 240615877-bigcodebench-benchmarking-code-generation-with-diverse-function-calls
tags:
- aaai-bar-eval-dprc-d78e07
- benchmark
- bigcodebench
- iclr-2025
created: '2026-07-19T20:01:48.436922Z'
updated: '2026-07-19T20:04:47.672489Z'
source: https://arxiv.org/abs/2406.15877
source_domain: arxiv.org
fetched_at: '2026-07-19T20:01:48.436470Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'BigCodeBench (ICLR 2025 Oral; Zhuo, Vu, Chim, Hu et al., 33 authors, BigCode
  community) is a code-generation benchmark of 1,140 fine-grained Python tasks requiring
  LLMs to invoke diverse function calls across 139 libraries and 7 domains (not short
  self-contained algorithmic problems like HumanEval/MBPP). Each task has an average
  of 5.6 test cases with 99% average branch coverage — high per-task test rigor. A
  natural-language variant, BigCodeBench-Instruct, strips docstrings to essential-information-only
  instructions. Across 60 LLMs evaluated, best scores reach only ~60% versus 97% human
  performance, evidencing the benchmark is far from saturated and considered realistic/practical
  rather than competitive-programming-style. This is the direct benchmark DPRC uses
  for its ''realistic functional code'' condition (oracle per-method AUROC 0.931 >
  scalar 0.875): BigCodeBench is a peer-reviewed, ICLR-2025-Oral, actively-used and
  unsaturated benchmark with dense multi-test-case tasks well suited to per-requirement/per-unittest-method
  confidence localization, giving DPRC''s functional-code claim a credible, non-toy
  benchmark foundation — though it is NOT itself an AAAI venue paper, so it establishes
  benchmark credibility but not AAAI-specific precedent.'
---

[2406.15877] BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2406.15877
(cs)
[Submitted on 22 Jun 2024 (
v1
), last revised 1 Apr 2025 (this version, v4)]
Title:
BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions
Authors:
Terry Yue Zhuo
,
Minh Chien Vu
,
Jenny Chim
,
Han Hu
,
Wenhao Yu
,
Ratnadira Widyasari
,
Imam Nur Bani Yusuf
,
Haolan Zhan
,
Junda He
,
Indraneil Paul
,
Simon Brunner
,
Chen Gong
,
Thong Hoang
,
Armel Randy Zebaze
,
Xiaoheng Hong
,
Wen-Ding Li
,
Jean Kaddour
,
Ming Xu
,
Zhihan Zhang
,
Prateek Yadav
,
Naman Jain
,
Alex Gu
,
Zhoujun Cheng
,
Jiawei Liu
,
Qian Liu
,
Zijian Wang
,
Binyuan Hui
,
Niklas Muennighoff
,
David Lo
,
Daniel Fried
,
Xiaoning Du
,
Harm de Vries
,
Leandro Von Werra
View a PDF of the paper titled BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions, by Terry Yue Zhuo and 32 other authors
View PDF
HTML (experimental)
Abstract:
Task automation has been greatly empowered by the recent advances in Large Language Models (LLMs) via Python code, where the tasks ranging from software engineering development to general-purpose reasoning. While current benchmarks have shown that LLMs can solve tasks using programs like human developers, the majority of their evaluations are limited to short and self-contained algorithmic tasks or standalone function calls. Solving challenging and practical tasks requires the capability of utilizing diverse function calls as tools to efficiently implement functionalities like data analysis and web development. In addition, using multiple tools to solve a task needs compositional reasoning by accurately understanding complex instructions. Fulfilling both of these characteristics can pose a great challenge for
this http URL
assess how well LLMs can solve challenging and practical tasks via programs, we introduce BigCodeBench, a benchmark that challenges LLMs to invoke multiple function calls as tools from 139 libraries and 7 domains for 1,140 fine-grained tasks. To evaluate LLMs rigorously, each task encompasses 5.6 test cases with an average branch coverage of 99%. In addition, we propose a natural-language-oriented variant of BigCodeBench, BigCodeBench-Instruct, that automatically transforms the original docstrings into short instructions only with essential information. Our extensive evaluation of 60 LLMs shows that LLMs are not yet capable of following complex instructions to use function calls precisely, with scores up to 60%, significantly lower than the human performance of 97%. The results underscore the need for further advancements in this area.
Comments:
Accpeted at ICLR 2025 (Oral), built with love by the BigCode community :)
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2406.15877
[cs.SE]
(or
arXiv:2406.15877v4
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2406.15877
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Terry Yue Zhuo [
view email
]
[v1]
Sat, 22 Jun 2024 15:52:04 UTC (1,396 KB)
[v2]
Wed, 26 Jun 2024 17:05:14 UTC (1,393 KB)
[v3]
Mon, 7 Oct 2024 17:23:30 UTC (2,662 KB)
[v4]
Tue, 1 Apr 2025 08:36:44 UTC (2,650 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions, by Terry Yue Zhuo and 32 other authors
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
2024-06
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