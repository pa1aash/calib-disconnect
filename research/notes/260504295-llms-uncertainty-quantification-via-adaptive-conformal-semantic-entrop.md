---
title: '[2605.04295] LLMs Uncertainty Quantification via Adaptive Conformal Semantic
  Entropy'
id: 260504295-llms-uncertainty-quantification-via-adaptive-conformal-semantic-entrop
tags:
- code-llm-calibration-aaai27-eabf3f
- conformal-calibration
- semantic-entropy
- multi-sample-baseline
created: '2026-07-17T18:30:29.819331Z'
updated: '2026-07-17T18:31:37.251421Z'
source: http://arxiv.org/abs/2605.04295
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:29.818551Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Karimi, Meyappan, Samavi (IJCAI 2026, submitted May 2026). Proposes Adaptive
  Conformal Semantic Entropy (ACSE): a prompt-level uncertainty scoring function built
  by clustering semantic entropy across MULTIPLE diverse sampled responses (still
  n-sample, not single-pass), then applying conformal calibration to get a finite-sample
  distribution-free accept/abstain guarantee bounding the error rate among accepted
  responses. Headline number: AUROC 0.88 on TriviaQA vs 0.65 for token-entropy baseline.
  This is a multi-sample method -- it does NOT address the cheap single-pass approximation
  angle; it is a competing/baseline data point showing how far conformal calibration
  + semantic clustering can push AUROC when you DO pay for sampling. No code-generation
  validation mentioned. Useful primarily as a strong sampling-based AUROC benchmark
  and as evidence that conformal calibration is a live technique in this space (potential
  ingredient for calibration guarantees on top of a cheap probe).'
---

[2605.04295] LLMs Uncertainty Quantification via Adaptive Conformal Semantic Entropy
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2605.04295
(cs)
[Submitted on 5 May 2026 (
v1
), last revised 23 May 2026 (this version, v2)]
Title:
LLMs Uncertainty Quantification via Adaptive Conformal Semantic Entropy
Authors:
Hamed Karimi
,
Vaishali Meyappan
,
Reza Samavi
View a PDF of the paper titled LLMs Uncertainty Quantification via Adaptive Conformal Semantic Entropy, by Hamed Karimi and 2 other authors
View PDF
HTML (experimental)
Abstract:
LLMs' overconfidence, particularly when hallucinating, poses a significant challenge for the deployment of the models in safety-critical settings and makes a reliable estimation of uncertainty necessary. Existing approaches for uncertainty quantification typically prioritize lexical or probabilistic measures; however, these techniques often ignore the semantic variance of different responses with similar meaning. In this paper, we propose Adaptive Conformal Semantic Entropy (ACSE), a method for estimating prompt-level uncertainty by adaptively measuring semantic dispersion in LLMs outputs. Our uncertainty scoring function is based on clustering semantic entropy of multiple diverse responses to the same prompt. The function adaptively adjusts the uncertainty score based on semantic features of each cluster. To ensure statistical reliability of our score, we use conformal calibration to apply a decision rule to accept/abstain the prompts, providing a finite-sample, distribution-free guarantee such that the error rate among the accepted responses remains bounded by a user-specified tolerance. Our extensive experimental evaluations using different LLMs and datasets, demonstrate that our approach consistently outperforms state-of-the-art uncertainty quantification baselines using discriminative performance, conformal guarantees, and probabilistic calibration indicators. As a highlight, for TriviaQA dataset, AUROC of our approach is 0.88 compared to 0.65 produced by the token entropy approach.
Comments:
Accepted for publication in the Proceedings of the 35th International Joint Conference on Artificial Intelligence (IJCAI 2026); 14 Pages
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2605.04295
[cs.LG]
(or
arXiv:2605.04295v2
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2605.04295
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Hamed Karimi [
view email
]
[v1]
Tue, 5 May 2026 20:56:11 UTC (394 KB)
[v2]
Sat, 23 May 2026 09:37:14 UTC (350 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled LLMs Uncertainty Quantification via Adaptive Conformal Semantic Entropy, by Hamed Karimi and 2 other authors
View PDF
HTML (experimental)
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