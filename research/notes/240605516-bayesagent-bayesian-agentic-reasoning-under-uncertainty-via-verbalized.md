---
title: '[2406.05516] BayesAgent: Bayesian Agentic Reasoning Under Uncertainty via
  Verbalized Probabilistic Graphical Modeling'
id: 240605516-bayesagent-bayesian-agentic-reasoning-under-uncertainty-via-verbalized
tags:
- aaai-bar-eval-dprc-d78e07
- calibration
- aaai-accepted-2026
- verbalized-confidence
created: '2026-07-19T20:02:59.743050Z'
updated: '2026-07-19T20:05:04.588012Z'
source: https://arxiv.org/abs/2406.05516
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:59.742692Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'AAAI 2026 (arXiv comment ''Accepted to AAAI 2026''). Huang, Shen, Wang,
  Meng, Liu, Duchene, Wang, Bhatt introduce vPGM (Verbalized Probabilistic Graphical
  Modeling) / BayesAgent: a framework that has LLM agents follow probabilistic-graphical-model
  principles expressed in NATURAL LANGUAGE (verbalized factor graphs / conditional
  structure), then refines the resulting posteriors via actual numerical Bayesian
  inference on top. Framed as the first bridge between LLM agents and PGMs for agentic
  reasoning under uncertainty, avoiding the need for expert-specified probabilistic
  model design. Scope: evaluated on multiple agentic reasoning tasks, both close-ended
  and open-ended; reports improved confidence calibration AND text generation quality
  (i.e., calibration is one of two headline metrics, not the sole contribution). Novelty
  type: new method/framework bridging two existing paradigms (LLM verbalization +
  classical PGM inference) -- theory-adjacent (draws on Bayesian formalism) but empirically
  validated, not a pure theory paper. Relevant to DPRC as an example of ''verbalized''
  signal elicitation (natural-language priming eliciting a structured probabilistic
  read-out) being an accepted mechanism at AAAI-26, structurally similar to DPRC''s
  digit-priming elicitation trick -- but vPGM additionally does numerical Bayesian
  refinement after elicitation, which DPRC currently does not (a candidate ''cook
  harder'' addition).'
---

[2406.05516] BayesAgent: Bayesian Agentic Reasoning Under Uncertainty via Verbalized Probabilistic Graphical Modeling
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2406.05516
(cs)
[Submitted on 8 Jun 2024 (
v1
), last revised 21 Jan 2026 (this version, v4)]
Title:
BayesAgent: Bayesian Agentic Reasoning Under Uncertainty via Verbalized Probabilistic Graphical Modeling
Authors:
Hengguan Huang
,
Xing Shen
,
Songtao Wang
,
Lingfa Meng
,
Dianbo Liu
,
David Alejandro Duchene
,
Hao Wang
,
Samir Bhatt
View a PDF of the paper titled BayesAgent: Bayesian Agentic Reasoning Under Uncertainty via Verbalized Probabilistic Graphical Modeling, by Hengguan Huang and 7 other authors
View PDF
HTML (experimental)
Abstract:
Human cognition excels at transcending sensory input and forming latent representations that structure our understanding of the world. While Large Language Model (LLM) agents demonstrate emergent reasoning and decision-making abilities, they lack a principled framework for capturing latent structures and modeling uncertainty. In this work, we explore for the first time how to bridge LLM agents with probabilistic graphical models (PGMs) to address agentic reasoning under uncertainty. To this end, we introduce Verbalized Probabilistic Graphical Modeling (vPGM), a Bayesian agentic framework that (i) guides LLM agents in following key principles of PGMs through natural language and (ii) refines the resulting posterior distributions via numerical Bayesian inference. Unlike many traditional probabilistic methods requiring substantial domain expertise, vPGM bypasses expert-driven model design, making it well-suited for scenarios with limited assumptions. We evaluated our model on several agentic reasoning tasks, both close-ended and open-ended. Our results indicate that the model effectively enhances confidence calibration and text generation quality.
Comments:
Accepted to AAAI 2026
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2406.05516
[cs.LG]
(or
arXiv:2406.05516v4
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2406.05516
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Hengguan Huang [
view email
]
[v1]
Sat, 8 Jun 2024 16:35:31 UTC (2,021 KB)
[v2]
Wed, 26 Feb 2025 13:56:16 UTC (1,407 KB)
[v3]
Tue, 4 Mar 2025 18:07:34 UTC (2,646 KB)
[v4]
Wed, 21 Jan 2026 01:18:41 UTC (364 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled BayesAgent: Bayesian Agentic Reasoning Under Uncertainty via Verbalized Probabilistic Graphical Modeling, by Hengguan Huang and 7 other authors
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
2024-06
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