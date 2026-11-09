---
title: '[2208.02814] Conformal Risk Control'
id: 220802814-conformal-risk-control
tags:
- code-llm-best-aaai-paper-6ded37
- conformal-prediction
- foundational
- closest-theory-template
created: '2026-07-20T07:43:35.913354Z'
updated: '2026-07-20T07:46:12.572646Z'
source: https://arxiv.org/abs/2208.02814
source_domain: arxiv.org
fetched_at: '2026-07-20T07:43:35.913049Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Conformal Risk Control (Angelopoulos, Bates, Fisch, Lei, Schuster; arXiv:2208.02814).
  Foundational theorem extending split-conformal prediction from miscoverage control
  to control of any bounded, monotone loss function''s expectation at a user-specified
  level alpha, via a single calibrated threshold with a finite-sample distribution-free
  guarantee (exchangeability-only assumption). Demonstrated on image segmentation
  (false-negative-rate control) and multi-label classification (recall control). This
  is the exact theorem a per-requirement risk-control result would specialize: define
  the loss as the fraction of accepted requirements per generated solution that fail
  their unit test, and show a calibrated threshold on a hidden-state probe score controls
  E[loss] <= alpha at the requirement-set level. General/domain-agnostic; not applied
  to code or to structured/sub-claim decomposition of a single generation.'
---

*Suggested by [[260517029-task-abstention-for-large-language-models-in-code-generation-2]] — foundational conformal risk control theorem this lane would repurpose for per-requirement guarantees*

[2208.02814] Conformal Risk Control
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Statistics > Methodology
arXiv:2208.02814
(stat)
[Submitted on 4 Aug 2022 (
v1
), last revised 13 Jun 2025 (this version, v4)]
Title:
Conformal Risk Control
Authors:
Anastasios N. Angelopoulos
,
Stephen Bates
,
Adam Fisch
,
Lihua Lei
,
Tal Schuster
View a PDF of the paper titled Conformal Risk Control, by Anastasios N. Angelopoulos and Stephen Bates and Adam Fisch and Lihua Lei and Tal Schuster
View PDF
HTML (experimental)
Abstract:
We extend conformal prediction to control the expected value of any monotone loss function. The algorithm generalizes split conformal prediction together with its coverage guarantee. Like conformal prediction, the conformal risk control procedure is tight up to an $\mathcal{O}(1/n)$ factor. We also introduce extensions of the idea to distribution shift, quantile risk control, multiple and adversarial risk control, and expectations of U-statistics. Worked examples from computer vision and natural language processing demonstrate the usage of our algorithm to bound the false negative rate, graph distance, and token-level F1-score.
Comments:
Code available at
this https URL
Subjects:
Methodology (stat.ME)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG); Statistics Theory (math.ST); Machine Learning (stat.ML)
Cite as:
arXiv:2208.02814
[stat.ME]
(or
arXiv:2208.02814v4
[stat.ME]
for this version)
https://doi.org/10.48550/arXiv.2208.02814
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Anastasios Angelopoulos [
view email
]
[v1]
Thu, 4 Aug 2022 17:59:44 UTC (2,245 KB)
[v2]
Sun, 23 Apr 2023 22:03:15 UTC (1,128 KB)
[v3]
Sat, 29 Apr 2023 21:20:48 UTC (1,130 KB)
[v4]
Fri, 13 Jun 2025 18:38:23 UTC (1,108 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Conformal Risk Control, by Anastasios N. Angelopoulos and Stephen Bates and Adam Fisch and Lihua Lei and Tal Schuster
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
stat.ME
< prev
|
next >
new
|
recent
|
2022-08
Change to browse by:
cs
cs.AI
cs.LG
math
math.ST
stat
stat.ML
stat.TH
References & Citations
NASA ADS
Google Scholar
Semantic Scholar
1 blog link
(
what is this?
)
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