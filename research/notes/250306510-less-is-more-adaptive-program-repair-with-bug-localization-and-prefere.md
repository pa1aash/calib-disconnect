---
title: '[2503.06510] Less is More: Adaptive Program Repair with Bug Localization and
  Preference Learning'
id: 250306510-less-is-more-adaptive-program-repair-with-bug-localization-and-prefere
tags:
- aaai-bar-eval-dprc-d78e07
- code-llm
- bug-localization
- aaai-2025
- program-repair
created: '2026-07-19T20:02:13.495951Z'
updated: '2026-07-19T20:04:34.479707Z'
source: https://arxiv.org/abs/2503.06510
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:13.495604Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'AAAI 2025 Oral (Dai, Chen, Zhao, Tang, Wu, Yao, Gao, Chen) introducing AdaPR
  (Adaptive Program Repair) and a two-stage AdaPatcher framework: a Bug Locator trained
  with self-debug learning to pinpoint bug locations, then a Program Modifier trained
  with location-aware repair learning, hybrid selective-reference training, and adaptive
  preference learning to minimize edit distance from the original buggy code while
  fixing it. Outperforms a set of baselines ''by a large margin'' (exact numbers require
  full-text). Directly relevant to DPRC as an AAAI-2025-Oral example of localization-as-a-trained-component
  in code LLMs: bug localization here is a full trained sub-model with its own objective
  (self-debug learning) and downstream utility (feeding the fix generator), not merely
  evaluated via AUROC as in DPRC — illustrating the AAAI bar''s preference for localization
  signals that are shown to be USED for something (a downstream task) rather than
  assessed in isolation.'
---

[2503.06510] Less is More: Adaptive Program Repair with Bug Localization and Preference Learning
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2503.06510
(cs)
[Submitted on 9 Mar 2025]
Title:
Less is More: Adaptive Program Repair with Bug Localization and Preference Learning
Authors:
Zhenlong Dai
,
Bingrui Chen
,
Zhuoluo Zhao
,
Xiu Tang
,
Sai Wu
,
Chang Yao
,
Zhipeng Gao
,
Jingyuan Chen
View a PDF of the paper titled Less is More: Adaptive Program Repair with Bug Localization and Preference Learning, by Zhenlong Dai and 7 other authors
View PDF
HTML (experimental)
Abstract:
Automated Program Repair (APR) is a task to automatically generate patches for the buggy code. However, most research focuses on generating correct patches while ignoring the consistency between the fixed code and the original buggy code. How to conduct adaptive bug fixing and generate patches with minimal modifications have seldom been investigated. To bridge this gap, we first introduce a novel task, namely AdaPR (Adaptive Program Repair). We then propose a two-stage approach AdaPatcher (Adaptive Patch Generator) to enhance program repair while maintaining the consistency. In the first stage, we utilize a Bug Locator with self-debug learning to accurately pinpoint bug locations. In the second stage, we train a Program Modifier to ensure consistency between the post-modified fixed code and the pre-modified buggy code. The Program Modifier is enhanced with a location-aware repair learning strategy to generate patches based on identified buggy lines, a hybrid training strategy for selective reference and an adaptive preference learning to prioritize fewer changes. The experimental results show that our approach outperforms a set of baselines by a large margin, validating the effectiveness of our two-stage framework for the newly proposed AdaPR task.
Comments:
accepted by AAAI2025 Oral
Subjects:
Software Engineering (cs.SE)
; Computation and Language (cs.CL)
Cite as:
arXiv:2503.06510
[cs.SE]
(or
arXiv:2503.06510v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2503.06510
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Zhenlong Dai [
view email
]
[v1]
Sun, 9 Mar 2025 08:32:38 UTC (1,565 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Less is More: Adaptive Program Repair with Bug Localization and Preference Learning, by Zhenlong Dai and 7 other authors
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
2025-03
Change to browse by:
cs
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