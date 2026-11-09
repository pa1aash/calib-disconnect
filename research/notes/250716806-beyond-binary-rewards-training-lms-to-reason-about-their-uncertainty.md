---
title: '[2507.16806] Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty'
id: 250716806-beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty
tags:
- code-llm-calibration-aaai27-eabf3f
- verbalized-confidence-rl
created: '2026-07-17T18:30:01.470363Z'
updated: '2026-07-17T18:33:51.408930Z'
source: http://arxiv.org/abs/2507.16806
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:01.469619Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: arXiv abstract page for Damani, Puri, Slocum, Shenfeld, Choshen, Kim, Andreas
  (MIT) 2025/2026, 'Beyond Binary Rewards' (RLCR). RL reward = correctness minus squared
  error of verbalized confidence (Brier-style, a bounded proper scoring rule); proves
  this yields models that are both accurate and calibrated, and shows it beats ordinary
  RLVR and post-hoc confidence classifiers in- and out-of-domain. Code/models released.
  See full-text note 'beyond-binary-rewards-training-lms-to-reason-about-their-uncertainty'
  for dataset/compute detail.
---

[2507.16806] Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2507.16806
(cs)
[Submitted on 22 Jul 2025 (
v1
), last revised 15 May 2026 (this version, v2)]
Title:
Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty
Authors:
Mehul Damani
,
Isha Puri
,
Stewart Slocum
,
Idan Shenfeld
,
Leshem Choshen
,
Yoon Kim
,
Jacob Andreas
View a PDF of the paper titled Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty, by Mehul Damani and 6 other authors
View PDF
HTML (experimental)
Abstract:
When language models (LMs) are trained via reinforcement learning (RL) to generate natural language "reasoning chains", their performance improves on a variety of difficult question answering tasks. Today, almost all successful applications of RL for reasoning use binary reward functions that evaluate the correctness of LM outputs. Because such reward functions do not penalize guessing or low-confidence outputs, they often have the unintended side-effect of degrading calibration and increasing the rate at which LMs generate incorrect responses (or "hallucinate") in other problem domains. This paper describes RLCR (Reinforcement Learning with Calibration Rewards), an approach to training reasoning models that jointly improves accuracy and calibrated confidence estimation. During RLCR, LMs generate both predictions and numerical confidence estimates after reasoning. They are trained to optimize a reward function that augments a binary correctness score with a Brier score -- a scoring rule for confidence estimates that incentivizes calibrated prediction. We first prove that this reward function (or any reward function that uses a bounded, proper scoring rule) yields models whose predictions are both accurate and well-calibrated. We next show that across diverse datasets, RLCR substantially improves calibration with no loss in accuracy, on both in-domain and out-of-domain evaluations -- outperforming both ordinary RL training and classifiers trained to assign post-hoc confidence scores. While ordinary RL hurts calibration, RLCR improves it. Finally, we demonstrate that verbalized confidence can be leveraged at test time to improve accuracy and calibration via confidence-weighted scaling methods. Our results show that explicitly optimizing for calibration can produce more generally reliable reasoning models. Code, models, and further info is available at
this https URL
.
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2507.16806
[cs.LG]
(or
arXiv:2507.16806v2
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2507.16806
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Isha Puri [
view email
]
[v1]
Tue, 22 Jul 2025 17:56:01 UTC (1,586 KB)
[v2]
Fri, 15 May 2026 00:00:51 UTC (1,995 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty, by Mehul Damani and 6 other authors
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
2025-07
Change to browse by:
cs
cs.AI
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