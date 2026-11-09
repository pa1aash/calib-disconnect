---
title: '[2407.00499] ConU: Conformal Uncertainty in Large Language Models with Correctness
  Coverage Guarantees'
id: 240700499-conu-conformal-uncertainty-in-large-language-models-with-correctness-c
tags:
- code-llm-best-aaai-paper-6ded37
- conformal-prediction
- whole-response-granularity
created: '2026-07-20T07:39:53.164568Z'
updated: '2026-07-20T07:45:46.815206Z'
source: https://arxiv.org/abs/2407.00499
source_domain: arxiv.org
fetched_at: '2026-07-20T07:39:53.164229Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'ConU: Conformal Uncertainty in LLMs with Correctness Coverage Guarantees
  (arXiv:2407.00499). Applies split conformal prediction to open-ended NLG/QA (not
  code): defines a self-consistency-based nonconformity score and calibrates a threshold
  so that, with probability >=1-alpha, the returned prediction set contains at least
  one correct generation, using a sampling-based admission function rather than execution
  ground truth. General-domain LLM output (short-answer QA), whole-response granularity
  -- no notion of sub-response/requirement decomposition, no code execution oracle.
  Closest-genre precedent for correctness-coverage-guarantee-via-conformal-calibration
  but operates at the single-response level, not structured/multi-part outputs.'
---

[2407.00499] ConU: Conformal Uncertainty in Large Language Models with Correctness Coverage Guarantees
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2407.00499
(cs)
[Submitted on 29 Jun 2024 (
v1
), last revised 18 Nov 2024 (this version, v3)]
Title:
ConU: Conformal Uncertainty in Large Language Models with Correctness Coverage Guarantees
Authors:
Zhiyuan Wang
,
Jinhao Duan
,
Lu Cheng
,
Yue Zhang
,
Qingni Wang
,
Xiaoshuang Shi
,
Kaidi Xu
,
Hengtao Shen
,
Xiaofeng Zhu
View a PDF of the paper titled ConU: Conformal Uncertainty in Large Language Models with Correctness Coverage Guarantees, by Zhiyuan Wang and 8 other authors
View PDF
HTML (experimental)
Abstract:
Uncertainty quantification (UQ) in natural language generation (NLG) tasks remains an open challenge, exacerbated by the closed-source nature of the latest large language models (LLMs). This study investigates applying conformal prediction (CP), which can transform any heuristic uncertainty notion into rigorous prediction sets, to black-box LLMs in open-ended NLG tasks. We introduce a novel uncertainty measure based on self-consistency theory, and then develop a conformal uncertainty criterion by integrating the uncertainty condition aligned with correctness into the CP algorithm. Empirical evaluations indicate that our uncertainty measure outperforms prior state-of-the-art methods. Furthermore, we achieve strict control over the correctness coverage rate utilizing 7 popular LLMs on 4 free-form NLG datasets, spanning general-purpose and medical scenarios. Additionally, the calibrated prediction sets with small size further highlights the efficiency of our method in providing trustworthy guarantees for practical open-ended NLG applications.
Comments:
Accepted by EMNLP 2024 Findings
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2407.00499
[cs.CL]
(or
arXiv:2407.00499v3
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2407.00499
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Zhiyuan Wang [
view email
]
[v1]
Sat, 29 Jun 2024 17:33:07 UTC (4,518 KB)
[v2]
Sun, 20 Oct 2024 04:17:20 UTC (5,078 KB)
[v3]
Mon, 18 Nov 2024 08:33:35 UTC (5,079 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled ConU: Conformal Uncertainty in Large Language Models with Correctness Coverage Guarantees, by Zhiyuan Wang and 8 other authors
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
2024-07
Change to browse by:
cs
cs.AI
cs.LG
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