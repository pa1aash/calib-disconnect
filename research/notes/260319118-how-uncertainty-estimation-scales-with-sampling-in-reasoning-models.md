---
title: '[2603.19118] How Uncertainty Estimation Scales with Sampling in Reasoning
  Models'
id: 260319118-how-uncertainty-estimation-scales-with-sampling-in-reasoning-models
tags:
- code-llm-calibration-aaai27-eabf3f
- sample-scaling
- self-consistency
- verbalized-confidence
created: '2026-07-17T18:30:39.869177Z'
updated: '2026-07-17T18:31:51.806776Z'
source: http://arxiv.org/abs/2603.19118
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:39.868664Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Del, Kangsepp, Domnich, Tampuu, Yankovskaya, Kull, Fishel (submitted Mar
  2026). Empirically characterizes how self-consistency and verbalized-confidence
  UQ signals scale with sampling budget n in reasoning LLMs -- 3 reasoning models
  x 17 tasks across math, STEM, humanities (no code-generation tasks). Key findings,
  quantitatively load-bearing for the AAAI-27 cost-benefit argument: (1) self-consistency
  shows LOWER initial discrimination than verbalized confidence and lags behind it
  under moderate sampling budgets; (2) most of the uncertainty gain comes from combining
  both signals -- a hybrid estimator with just n=2 samples improves AUROC by up to
  +12 points on average over either signal alone, and this n=2 hybrid already outperforms
  either single signal scaled to much larger n, after which returns diminish sharply;
  (3) effects are domain-dependent -- math (RLVR post-training''s native domain) shows
  higher UQ quality and faster signal-combination gains than STEM/humanities. This
  paper is the direct evidence base for ''self-consistency is expensive because full
  benefit needs many samples, but most of the achievable gain is front-loaded at very
  low n'' -- supports framing a cheap single/near-single-pass proxy as recovering
  most of the achievable AUROC gain rather than needing the full n. Not validated
  on code; a clean gap for a code-specific replication+extension.'
---

[2603.19118] How Uncertainty Estimation Scales with Sampling in Reasoning Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2603.19118
(cs)
[Submitted on 19 Mar 2026]
Title:
How Uncertainty Estimation Scales with Sampling in Reasoning Models
Authors:
Maksym Del
,
Markus Kängsepp
,
Marharyta Domnich
,
Ardi Tampuu
,
Lisa Yankovskaya
,
Meelis Kull
,
Mark Fishel
View a PDF of the paper titled How Uncertainty Estimation Scales with Sampling in Reasoning Models, by Maksym Del and 6 other authors
View PDF
HTML (experimental)
Abstract:
Uncertainty estimation is critical for deploying reasoning language models, yet remains poorly understood under extended chain-of-thought reasoning. We study parallel sampling as a fully black-box approach using verbalized confidence and self-consistency. Across three reasoning models and 17 tasks spanning mathematics, STEM, and humanities, we characterize how these signals scale.
Both self-consistency and verbalized confidence scale in reasoning models, but self-consistency exhibits lower initial discrimination and lags behind verbalized confidence under moderate sampling. Most uncertainty gains, however, arise from signal combination: with just two samples, a hybrid estimator improves AUROC by up to $+12$ on average and already outperforms either signal alone even when scaled to much larger budgets, after which returns diminish. These effects are domain-dependent: in mathematics, the native domain of RLVR-style post-training, reasoning models achieve higher uncertainty quality and exhibit both stronger complementarity and faster scaling than in STEM or humanities.
Subjects:
Artificial Intelligence (cs.AI)
; Computation and Language (cs.CL); Machine Learning (cs.LG)
Cite as:
arXiv:2603.19118
[cs.AI]
(or
arXiv:2603.19118v1
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2603.19118
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Maksym Del [
view email
]
[v1]
Thu, 19 Mar 2026 16:42:05 UTC (315 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled How Uncertainty Estimation Scales with Sampling in Reasoning Models, by Maksym Del and 6 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.AI
< prev
|
next >
new
|
recent
|
2026-03
Change to browse by:
cs
cs.CL
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