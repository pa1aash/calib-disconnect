---
title: '[2012.08668] Mitigating Bias in Calibration Error Estimation'
id: 201208668-mitigating-bias-in-calibration-error-estimation
tags:
- code-llm-calibration-aaai27-eabf3f
- ece-fragility
- metric-critique
created: '2026-07-17T18:33:33.125919Z'
updated: '2026-07-17T18:34:35.092295Z'
source: https://arxiv.org/abs/2012.08668
source_domain: arxiv.org
fetched_at: '2026-07-17T18:33:33.125441Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Roelofs, Cain, Shlens & Mozer (AISTATS 2022) establish that ECE_bin -- the
  standard binned expected-calibration-error metric -- is a STATISTICALLY BIASED estimator
  of true calibration error, with the bias direction and magnitude depending on the
  nature of miscalibration, evaluation set size, and number of bins. Using a framework
  that synthesizes model outputs matching real-network statistics, they show equal-mass
  binning has substantially lower bias than the conventional equal-width binning used
  in most papers. They propose two reliable estimators -- the debiased estimator (Brocker
  2012; Ferro & Fricker 2012) and their own ECE_sweep (equal-mass bins, bin count
  maximized subject to monotonicity) -- and show these change conclusions about recalibration-method
  effectiveness and miscalibration detection. This is the canonical, foundational
  critique underlying any claim that ECE improvements from post-hoc calibration are
  metric artifacts rather than real calibration gains: if the disconnect paper''s
  ECE is computed with standard equal-width binning and unreported bin count, the
  reported ECE improvement (paired with AUROC degradation) could itself be a biased-estimator
  artifact rather than a genuine calibration/discrimination tradeoff.'
---

*Suggested by [[260527752-asking-is-not-enough-protocol-sensitivity-in-llm-confidence-calibratio]] — ECE binning-bias critique underlying protocol-sensitivity concerns*

[2012.08668] Mitigating Bias in Calibration Error Estimation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2012.08668
(cs)
[Submitted on 15 Dec 2020 (
v1
), last revised 11 Feb 2022 (this version, v3)]
Title:
Mitigating Bias in Calibration Error Estimation
Authors:
Rebecca Roelofs
,
Nicholas Cain
,
Jonathon Shlens
,
Michael C. Mozer
View a PDF of the paper titled Mitigating Bias in Calibration Error Estimation, by Rebecca Roelofs and 3 other authors
View PDF
Abstract:
For an AI system to be reliable, the confidence it expresses in its decisions must match its accuracy. To assess the degree of match, examples are typically binned by confidence and the per-bin mean confidence and accuracy are compared. Most research in calibration focuses on techniques to reduce this empirical measure of calibration error, ECE_bin. We instead focus on assessing statistical bias in this empirical measure, and we identify better estimators. We propose a framework through which we can compute the bias of a particular estimator for an evaluation data set of a given size. The framework involves synthesizing model outputs that have the same statistics as common neural architectures on popular data sets. We find that binning-based estimators with bins of equal mass (number of instances) have lower bias than estimators with bins of equal width. Our results indicate two reliable calibration-error estimators: the debiased estimator (Brocker, 2012; Ferro and Fricker, 2012) and a method we propose, ECE_sweep, which uses equal-mass bins and chooses the number of bins to be as large as possible while preserving monotonicity in the calibration function. With these estimators, we observe improvements in the effectiveness of recalibration methods and in the detection of model miscalibration.
Comments:
To be published in AISTATS 2022. Code is available
this https URL
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computer Vision and Pattern Recognition (cs.CV); Machine Learning (stat.ML)
Cite as:
arXiv:2012.08668
[cs.LG]
(or
arXiv:2012.08668v3
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2012.08668
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Rebecca Roelofs [
view email
]
[v1]
Tue, 15 Dec 2020 23:28:06 UTC (798 KB)
[v2]
Wed, 24 Feb 2021 19:25:00 UTC (1,491 KB)
[v3]
Fri, 11 Feb 2022 00:15:27 UTC (3,818 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Mitigating Bias in Calibration Error Estimation, by Rebecca Roelofs and 3 other authors
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
2020-12
Change to browse by:
cs
cs.AI
cs.CV
stat
stat.ML
References & Citations
NASA ADS
Google Scholar
Semantic Scholar
DBLP
- CS Bibliography
listing
|
bibtex
Rebecca Roelofs
Jonathon Shlens
Michael C. Mozer
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