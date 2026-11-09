---
title: '[2205.14334] Teaching Models to Express Their Uncertainty in Words'
id: 220514334-teaching-models-to-express-their-uncertainty-in-words
tags:
- code-llm-probe-verbalize-gap-3d8995
- verbalized-confidence
- foundational
created: '2026-07-20T06:36:44.527317Z'
updated: '2026-07-20T06:42:07.957320Z'
source: https://arxiv.org/abs/2205.14334
source_domain: arxiv.org
fetched_at: '2026-07-20T06:36:44.526971Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Lin, Hilton, Evans (OpenAI/Oxford, arXiv May 2022). Foundational verbalized-confidence
  paper: shows GPT-3 can be FINE-TUNED (supervised, on human-labeled calibration data)
  to emit natural-language confidence (''90% confidence'' / ''high confidence'') without
  using model logits, and that these verbalized probabilities are well-calibrated
  on the authors'' own CalibratedMath benchmark, remain moderately calibrated under
  distribution shift, and are sensitive to the model''s own uncertainty rather than
  imitating human calibration patterns. Directly compares verbalized-word confidence
  to logit-derived confidence and finds both generalize under distribution shift;
  also finds verbalized calibration ability depends on pretrained latent representations
  correlated with epistemic uncertainty -- i.e. an early hint that verbalization draws
  on an internal uncertainty signal rather than being independent of it. Domain: elementary/arithmetic
  math word problems (CalibratedMath), NOT code, NOT per-requirement. This is the
  founding positive result for trained verbalized confidence (contrasts with later
  papers like Xiong 2023/2306.13063 and the disconnect-paper''s own findings that
  UNTRAINED/zero-shot verbalized confidence is overconfident and poorly discriminative)
  -- establishes that training CAN make verbalization calibrated on math, raising
  the comparison question of whether the same training approach transfers to per-requirement
  code confidence, which no source in this search directly tests.'
---

[2205.14334] Teaching Models to Express Their Uncertainty in Words
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2205.14334
(cs)
[Submitted on 28 May 2022 (
v1
), last revised 13 Jun 2022 (this version, v2)]
Title:
Teaching Models to Express Their Uncertainty in Words
Authors:
Stephanie Lin
,
Jacob Hilton
,
Owain Evans
View a PDF of the paper titled Teaching Models to Express Their Uncertainty in Words, by Stephanie Lin and 2 other authors
View PDF
Abstract:
We show that a GPT-3 model can learn to express uncertainty about its own answers in natural language -- without use of model logits. When given a question, the model generates both an answer and a level of confidence (e.g. "90% confidence" or "high confidence"). These levels map to probabilities that are well calibrated. The model also remains moderately calibrated under distribution shift, and is sensitive to uncertainty in its own answers, rather than imitating human examples. To our knowledge, this is the first time a model has been shown to express calibrated uncertainty about its own answers in natural language. For testing calibration, we introduce the CalibratedMath suite of tasks. We compare the calibration of uncertainty expressed in words ("verbalized probability") to uncertainty extracted from model logits. Both kinds of uncertainty are capable of generalizing calibration under distribution shift. We also provide evidence that GPT-3's ability to generalize calibration depends on pre-trained latent representations that correlate with epistemic uncertainty over its answers.
Comments:
CalibratedMath tasks and evaluation code are available at
this https URL
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2205.14334
[cs.CL]
(or
arXiv:2205.14334v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2205.14334
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Stephanie Lin [
view email
]
[v1]
Sat, 28 May 2022 05:02:31 UTC (2,691 KB)
[v2]
Mon, 13 Jun 2022 05:04:53 UTC (2,691 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Teaching Models to Express Their Uncertainty in Words, by Stephanie Lin and 2 other authors
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
2022-05
Change to browse by:
cs
cs.AI
cs.LG
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