---
title: '[2302.09664] Semantic Uncertainty: Linguistic Invariances for Uncertainty
  Estimation in Natural Language Generation'
id: 230209664-semantic-uncertainty-linguistic-invariances-for-uncertainty-estimation
tags:
- code-llm-calibration-aaai27-eabf3f
- semantic-entropy
- foundational-method
created: '2026-07-17T18:33:39.996043Z'
updated: '2026-07-17T18:35:00.887210Z'
source: https://arxiv.org/abs/2302.09664
source_domain: arxiv.org
fetched_at: '2026-07-17T18:33:39.995676Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Kuhn, Gal, Farquhar (ICLR 2023 Spotlight, arXiv Feb 2023). The original semantic
  entropy / semantic uncertainty paper that precedes and is later scaled up into the
  Farquhar et al. 2024 Nature paper. Introduces the core idea that entropy should
  be computed over clusters of semantically-equivalent generations ('semantic equivalence'
  via linguistic invariance) rather than over raw token sequences, because measuring
  uncertainty at the token/sequence level conflates meaning-uncertainty with surface-form
  variation. The method is unsupervised, uses only a single model (no auxiliary classifier),
  and needs no modification to off-the-shelf LLMs -- but still requires sampling multiple
  generations per prompt to build the semantic clusters. Ablations show semantic entropy
  is more predictive of model accuracy on QA datasets than comparable baselines. This
  is the foundational precursor establishing why naive token-probability confidence
  fails and why semantic clustering over samples works; it is the theoretical root
  of the multi-sample cost problem the AAAI-27 paper needs a cheap proxy for.
---

*Suggested by [[240615927-semantic-entropy-probes-robust-and-cheap-hallucination-detection-in-ll]] — original semantic uncertainty/entropy method that SE and SEPs build on*

[2302.09664] Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2302.09664
(cs)
[Submitted on 19 Feb 2023 (
v1
), last revised 15 Apr 2023 (this version, v3)]
Title:
Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation
Authors:
Lorenz Kuhn
,
Yarin Gal
,
Sebastian Farquhar
View a PDF of the paper titled Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation, by Lorenz Kuhn and 2 other authors
View PDF
Abstract:
We introduce a method to measure uncertainty in large language models. For tasks like question answering, it is essential to know when we can trust the natural language outputs of foundation models. We show that measuring uncertainty in natural language is challenging because of "semantic equivalence" -- different sentences can mean the same thing. To overcome these challenges we introduce semantic entropy -- an entropy which incorporates linguistic invariances created by shared meanings. Our method is unsupervised, uses only a single model, and requires no modifications to off-the-shelf language models. In comprehensive ablation studies we show that the semantic entropy is more predictive of model accuracy on question answering data sets than comparable baselines.
Comments:
International Conference on Learning Representations 2023 (Spotlight)
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2302.09664
[cs.CL]
(or
arXiv:2302.09664v3
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2302.09664
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Lorenz Kuhn [
view email
]
[v1]
Sun, 19 Feb 2023 20:10:07 UTC (108 KB)
[v2]
Tue, 21 Feb 2023 16:30:15 UTC (108 KB)
[v3]
Sat, 15 Apr 2023 12:55:45 UTC (108 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation, by Lorenz Kuhn and 2 other authors
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
2023-02
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