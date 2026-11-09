---
title: '[2404.19472] Multi-label Classification under Uncertainty: A Tree-based Conformal
  Prediction Approach'
id: 240419472-multi-label-classification-under-uncertainty-a-tree-based-conformal-pr
tags:
- code-llm-best-aaai-paper-6ded37
- conformal-prediction
- multi-label-fdr
- closest-theory-template
created: '2026-07-20T07:43:25.274361Z'
updated: '2026-07-20T07:46:07.935793Z'
source: https://arxiv.org/abs/2404.19472
source_domain: arxiv.org
fetched_at: '2026-07-20T07:43:25.274013Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Multi-label Classification under Uncertainty: A Tree-based Conformal Prediction
  Approach (Tyagi & Guo, arXiv:2404.19472, COPA 2023). General statistics-methodology
  paper (not code, not LLMs): builds a hierarchical tree over labelsets via clustering,
  casts multi-label conformal prediction as a hierarchical multiple-hypothesis-testing
  problem, derives marginal conformal p-values per node/hypothesis, and proves family-wise-error-rate
  control for two testing procedures (hierarchical Bonferroni + a modification), yielding
  coverage-valid prediction sets for which labels are jointly retained. Closest GENERIC
  theoretical template for per-requirement risk control within one instance: treat
  each of a code problem''s unit-test requirements as a hypothesis/label, derive per-requirement
  conformal p-values from calibration pass/fail data, and control FWER/FDR over which
  requirements are accepted -- but the paper never touches code, execution oracles,
  or generative structured outputs; it is pure multi-label classification on independent
  feature vectors.'
---

[2404.19472] Multi-label Classification under Uncertainty: A Tree-based Conformal Prediction Approach
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Statistics > Methodology
arXiv:2404.19472
(stat)
[Submitted on 30 Apr 2024]
Title:
Multi-label Classification under Uncertainty: A Tree-based Conformal Prediction Approach
Authors:
Chhavi Tyagi
,
Wenge Guo
View a PDF of the paper titled Multi-label Classification under Uncertainty: A Tree-based Conformal Prediction Approach, by Chhavi Tyagi and Wenge Guo
View PDF
HTML (experimental)
Abstract:
Multi-label classification is a common challenge in various machine learning applications, where a single data instance can be associated with multiple classes simultaneously. The current paper proposes a novel tree-based method for multi-label classification using conformal prediction and multiple hypothesis testing. The proposed method employs hierarchical clustering with labelsets to develop a hierarchical tree, which is then formulated as a multiple-testing problem with a hierarchical structure. The split-conformal prediction method is used to obtain marginal conformal $p$-values for each tested hypothesis, and two \textit{hierarchical testing procedures} are developed based on marginal conformal $p$-values, including a hierarchical Bonferroni procedure and its modification for controlling the family-wise error rate. The prediction sets are thus formed based on the testing outcomes of these two procedures. We establish a theoretical guarantee of valid coverage for the prediction sets through proven family-wise error rate control of those two procedures. We demonstrate the effectiveness of our method in a simulation study and two real data analysis compared to other conformal methods for multi-label classification.
Comments:
21 pages, 7 figures; 3 supplementary pages
Subjects:
Methodology (stat.ME)
Cite as:
arXiv:2404.19472
[stat.ME]
(or
arXiv:2404.19472v1
[stat.ME]
for this version)
https://doi.org/10.48550/arXiv.2404.19472
Focus to learn more
arXiv-issued DOI via DataCite
Journal reference:
In COPA 2023 : 12th Symposium on Conformal and Probabilistic Prediction with Applications
Submission history
From: Wenge Guo [
view email
]
[v1]
Tue, 30 Apr 2024 11:37:33 UTC (3,152 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Multi-label Classification under Uncertainty: A Tree-based Conformal Prediction Approach, by Chhavi Tyagi and Wenge Guo
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
2024-04
Change to browse by:
stat
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