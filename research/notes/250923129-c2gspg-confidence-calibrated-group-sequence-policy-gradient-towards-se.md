---
title: '[2509.23129] C$^2$GSPG: Confidence-calibrated Group Sequence Policy Gradient
  towards Self-aware Reasoning'
id: 250923129-c2gspg-confidence-calibrated-group-sequence-policy-gradient-towards-se
tags:
- code-llm-calibration-aaai27-eabf3f
- logit-based-confidence
- no-code-eval-gap
created: '2026-07-17T18:37:59.878469Z'
updated: '2026-07-17T18:39:02.832897Z'
source: https://arxiv.org/abs/2509.23129
source_domain: arxiv.org
fetched_at: '2026-07-17T18:37:59.878067Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Liu, Wang, Xu (arXiv:2509.23129, 2025-2026). Proposes GSPG, a sequence-level
  (not token-level) variant of GRPO that eliminates GRPO's token-level advantage bias,
  then adds a cross-entropy regularizer aligning a NORMALIZED SEQUENCE-LEVEL LOG-PROBABILITY
  (a logit-based confidence proxy, not a verbalized token) to the sequence's binary
  reward. Proves the calibration regularizer and the GSPG accuracy objective share
  the same gradient direction for binary rewards, avoiding an accuracy/calibration
  trade-off in that regime; for non-binary rewards uses nonlinear reward normalization
  plus adaptive regularizer clipping to prevent objective conflict. Tested only on
  logical and mathematical reasoning post-training, no code. Confirms this is the
  'C2GSPG' cited by RLCM (2604.23333) as a logit-based calibration baseline that RLCM
  shows underperforms a hidden-state probe -- so C2GSPG's own logit-based confidence,
  despite being internal to the model (not a decoded token), still loses to hidden-state
  probes in RLCM's later comparison, suggesting logit-based confidence is an intermediate
  point between fully-internal probes and fully-expressed verbal tokens, and is not
  sufficient either.
---

*Suggested by [[process-supervision-of-confidence-margin-for-calibrated-llm-reasoning]] — C2GSPG cited as logit-based calibration-aware policy optimization baseline*

[2509.23129] C$^2$GSPG: Confidence-calibrated Group Sequence Policy Gradient towards Self-aware Reasoning
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2509.23129
(cs)
[Submitted on 27 Sep 2025 (
v1
), last revised 23 Dec 2025 (this version, v2)]
Title:
C$^2$GSPG: Confidence-calibrated Group Sequence Policy Gradient towards Self-aware Reasoning
Authors:
Haotian Liu
,
Shuo Wang
,
Hongteng Xu
View a PDF of the paper titled C$^2$GSPG: Confidence-calibrated Group Sequence Policy Gradient towards Self-aware Reasoning, by Haotian Liu and 2 other authors
View PDF
HTML (experimental)
Abstract:
Reinforcement Learning (RL) methods, exemplified by Group Relative Policy Optimization (GRPO) and its variants, play a central role in developing reasoning models. However, these methods often suffer from a critical overconfidence issue, which prevents them from achieving self-aware reasoning models. In this study, we propose a simple yet effective confidence-calibration group sequence policy gradient method, called C$^2$GSPG, which simultaneously enhances reasoning performance while suppressing overconfidence. In principle, we propose a Group Sequence Policy Gradient (GSPG) framework for learning reasoning models, which eliminates the token-level bias commonly appearing in GRPO and its variants. In this framework, we define the model confidence for each reasoning problem using the normalized sequence-level probability, and then apply a cross-entropy regularizer to calibrate the model confidence to the sequence's reward. We demonstrate that the confidence calibration regularizer and GSPG are collaborative for binary rewards, as their objectives always share the same gradient direction. For non-binary rewards, we apply nonlinear reward normalization and adaptive regularizer clipping, mitigating the potential conflict between the two objectives. Applying C$^2$GSPG to post-train large language models in logical and mathematical reasoning tasks, we show its superiority over state-of-the-art methods in both reasoning accuracy and confidence calibration. The code of C$^2$GSPG is available at
this https URL
.
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2509.23129
[cs.LG]
(or
arXiv:2509.23129v2
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2509.23129
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Haotian Liu [
view email
]
[v1]
Sat, 27 Sep 2025 05:24:51 UTC (157 KB)
[v2]
Tue, 23 Dec 2025 07:56:48 UTC (188 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled C$^2$GSPG: Confidence-calibrated Group Sequence Policy Gradient towards Self-aware Reasoning, by Haotian Liu and 2 other authors
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
2025-09
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