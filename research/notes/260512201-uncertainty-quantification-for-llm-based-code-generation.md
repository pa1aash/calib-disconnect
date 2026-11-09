---
title: '[2605.12201] Uncertainty Quantification for LLM-based Code Generation'
id: 260512201-uncertainty-quantification-for-llm-based-code-generation
tags:
- code-llm-calibration-aaai27-eabf3f
- selective-generation
- prediction-sets
- conformal-prediction
created: '2026-07-17T18:34:36.243755Z'
updated: '2026-07-20T07:46:13.653719Z'
source: https://arxiv.org/abs/2605.12201
source_domain: arxiv.org
fetched_at: '2026-07-17T18:34:36.243322Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Companion paper (overlapping author list with Task Abstention, 2605.17029:
  Senrong Xu, Yuhao Tan, Yanke Zhou, Zenan Li, Yuan Yao, Taolue Chen, Xiaoxing Ma)
  proposing RisCoSet, a prediction-set method for LLM-based code generation using
  multiple hypothesis testing to construct risk-controlling prediction sets represented
  as PARTIAL PROGRAMS, guaranteed to contain a correct solution with high confidence.
  Explicitly positions itself against PAC prediction sets, criticizing their strong
  monotonicity assumption on risk and single-label classification framing as unable
  to accommodate code generation''s multiple valid outputs. Reports RisCoSet reduces
  code removal (i.e., how much of the candidate program must be excluded/masked to
  hit the risk target) by up to 24.5% versus state-of-the-art, at the same risk level,
  across three LLMs. This is a genuine downstream ACTION (constrained/partial generation
  under a coverage guarantee) with a measured efficiency payoff, from the same group
  as Task Abstention -- together the two papers show this group has built formal risk-control
  machinery for code generation but, per both abstracts, neither benchmarks against
  or builds on the specific near-perfectly-calibrated repeated-sampling confidence
  signal, nor evaluates real deployment/developer-trust payoffs.'
---

*Suggested by [[240905923-mathbbuscd-improving-code-generation-of-llms-by-uncertainty-aware-sele]] — Uncertainty quantification survey/method for code generation, contextualizes token-level UQ gap*

[2605.12201] Uncertainty Quantification for LLM-based Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2605.12201
(cs)
[Submitted on 12 May 2026]
Title:
Uncertainty Quantification for LLM-based Code Generation
Authors:
Senrong Xu
,
Yuhao Tan
,
Yanke Zhou
,
Guangyuan Wu
,
Zenan Li
,
Yuan Yao
,
Taolue Chen
,
Feng Xu
,
Xiaoxing Ma
View a PDF of the paper titled Uncertainty Quantification for LLM-based Code Generation, by Senrong Xu and 8 other authors
View PDF
HTML (experimental)
Abstract:
Prediction sets provide a theoretically grounded framework for quantifying uncertainty in machine learning models. Adapting them to structured generation tasks, in particular, large language model (LLM) based code generation, remains a challenging problem. An existing attempt proposes PAC prediction sets but is limited by its strong monotonicity assumption on risk and single-label classification framework, which severely limits the space of candidate programs and cannot accommodate the multiple valid outputs inherent to code generation. To address these limitations, we propose an approach RisCoSet that leverages multiple hypothesis testing to construct risk-controlling predictions for LLM-based code generation. Given a trained code generation model, we produce a prediction set represented by a partial program, which is guaranteed to contain a correct solution with high confidence. Extensive experiments on three LLMs demonstrate the effectiveness of the proposed method. For instance, compared with the state-of-the-art, our method can significantly reduce the code removal by up to 24.5%, at the same level of risk.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2605.12201
[cs.SE]
(or
arXiv:2605.12201v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2605.12201
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Senrong Xu [
view email
]
[v1]
Tue, 12 May 2026 14:40:29 UTC (596 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Uncertainty Quantification for LLM-based Code Generation, by Senrong Xu and 8 other authors
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
2026-05
Change to browse by:
cs
cs.AI
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