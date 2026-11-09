---
title: '[2602.07842] Evaluating and Calibrating LLM Confidence on Questions with Multiple
  Correct Answers'
id: 260207842-evaluating-and-calibrating-llm-confidence-on-questions-with-multiple-c
tags:
- aaai-bar-eval-dprc-d78e07
created: '2026-07-19T20:07:24.292688Z'
updated: '2026-07-19T20:07:51.733943Z'
source: https://arxiv.org/abs/2602.07842
source_domain: arxiv.org
fetched_at: '2026-07-19T20:07:24.292270Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Abstract-only stub; superseded by full-text note evaluating-and-calibrating-llm-confidence-on-questions-with-multiple-correct-ans
---

[2602.07842] Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct Answers
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2602.07842
(cs)
[Submitted on 8 Feb 2026 (
v1
), last revised 2 Jun 2026 (this version, v2)]
Title:
Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct Answers
Authors:
Yuhan Wang
,
Shiyu Ni
,
Zhikai Ding
,
Zihang Zhan
,
Yuanzi Li
,
Keping Bi
View a PDF of the paper titled Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct Answers, by Yuhan Wang and 5 other authors
View PDF
HTML (experimental)
Abstract:
Confidence calibration is essential for making large language models (LLMs) reliable, yet existing training-free methods have been primarily studied under single-answer question answering. In this paper, we show that these methods break down in the presence of multiple valid answers, where disagreement among equally correct responses leads to systematic underestimation of confidence. To enable a systematic study of this phenomenon, we introduce MACE, a benchmark of 12,000 factual questions spanning six domains with varying numbers of correct answers. Experiments across 15 representative calibration methods and four LLM families (7B-72B) reveal that while accuracy increases with answer cardinality, estimated confidence consistently decreases, causing severe miscalibration for questions with mixed answer counts. To address this issue, we propose Semantic Confidence Aggregation (SCA), which aggregates confidence over multiple high-probability sampled responses. SCA achieves state-of-the-art calibration performance under mixed-answer settings while preserving strong calibration on single-answer questions.
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2602.07842
[cs.CL]
(or
arXiv:2602.07842v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2602.07842
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Shiyu Ni [
view email
]
[v1]
Sun, 8 Feb 2026 07:03:27 UTC (1,429 KB)
[v2]
Tue, 2 Jun 2026 11:57:37 UTC (1,590 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Evaluating and Calibrating LLM Confidence on Questions with Multiple Correct Answers, by Yuhan Wang and 5 other authors
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
2026-02
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