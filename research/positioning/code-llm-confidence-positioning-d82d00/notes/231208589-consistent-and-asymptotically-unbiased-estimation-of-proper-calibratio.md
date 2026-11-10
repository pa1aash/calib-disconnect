---
title: '[2312.08589] Consistent and Asymptotically Unbiased Estimation of Proper Calibration
  Errors'
id: 231208589-consistent-and-asymptotically-unbiased-estimation-of-proper-calibratio
tags:
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-11-09T23:10:59.282163Z'
updated: '2026-11-09T23:28:22.640751Z'
source: https://arxiv.org/abs/2312.08589
source_domain: arxiv.org
fetched_at: '2026-11-09T23:10:59.281501Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Vault note holds the arXiv abstract page; full text read from locally extracted
  arXiv PDF. Popordanoska et al. (AISTATS-style, Dec 2023) give a consistent and asymptotically
  unbiased estimator of proper calibration errors and refinement for any proper score
  (Brier gives squared L2 CE, log loss gives KL CE), via kernel density; classification
  experiments (not code, not LLM). Supplies estimator-theory background for an F (metrology)
  framing; not code-specific.
---

[2312.08589] Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2312.08589
(cs)
[Submitted on 14 Dec 2023]
Title:
Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors
Authors:
Teodora Popordanoska
,
Sebastian G. Gruber
,
Aleksei Tiulpin
,
Florian Buettner
,
Matthew B. Blaschko
View a PDF of the paper titled Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors, by Teodora Popordanoska and 4 other authors
View PDF
Abstract:
Proper scoring rules evaluate the quality of probabilistic predictions, playing an essential role in the pursuit of accurate and well-calibrated models. Every proper score decomposes into two fundamental components -- proper calibration error and refinement -- utilizing a Bregman divergence. While uncertainty calibration has gained significant attention, current literature lacks a general estimator for these quantities with known statistical properties. To address this gap, we propose a method that allows consistent, and asymptotically unbiased estimation of all proper calibration errors and refinement terms. In particular, we introduce Kullback--Leibler calibration error, induced by the commonly used cross-entropy loss. As part of our results, we prove the relation between refinement and f-divergences, which implies information monotonicity in neural networks, regardless of which proper scoring rule is optimized. Our experiments validate empirically the claimed properties of the proposed estimator and suggest that the selection of a post-hoc calibration method should be determined by the particular calibration error of interest.
Comments:
Preprint
Subjects:
Machine Learning (cs.LG)
; Machine Learning (stat.ML)
Cite as:
arXiv:2312.08589
[cs.LG]
(or
arXiv:2312.08589v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2312.08589
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Teodora Popordanoska [
view email
]
[v1]
Thu, 14 Dec 2023 01:20:08 UTC (211 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Consistent and Asymptotically Unbiased Estimation of Proper Calibration Errors, by Teodora Popordanoska and 4 other authors
View PDF
TeX Source
view license
Current browse context:
cs.LG
< prev
|
next >
new
|
recent
|
2023-12
Change to browse by:
cs
stat
stat.ML
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
IArxiv recommender toggle
IArxiv Recommender
(
What is IArxiv?
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