---
title: '[2506.03723] Verbalized Confidence Triggers Self-Verification: Emergent Behavior
  Without Explicit Reasoning Supervision'
id: 250603723-verbalized-confidence-triggers-self-verification-emergent-behavior-wit
tags:
- code-llm-calibration-aaai27-eabf3f
created: '2026-07-17T18:30:34.008427Z'
updated: '2026-11-10T09:27:38.234956Z'
source: http://arxiv.org/abs/2506.03723
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:34.007766Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Deprecated duplicate or empty-body record (arXiv metadata only); superseded
  by a full-text note of the same paper or out of scope
---

[2506.03723] Verbalized Confidence Triggers Self-Verification: Emergent Behavior Without Explicit Reasoning Supervision
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2506.03723
(cs)
[Submitted on 4 Jun 2025]
Title:
Verbalized Confidence Triggers Self-Verification: Emergent Behavior Without Explicit Reasoning Supervision
Authors:
Chaeyun Jang
,
Moonseok Choi
,
Yegon Kim
,
Hyungi Lee
,
Juho Lee
View a PDF of the paper titled Verbalized Confidence Triggers Self-Verification: Emergent Behavior Without Explicit Reasoning Supervision, by Chaeyun Jang and 4 other authors
View PDF
HTML (experimental)
Abstract:
Uncertainty calibration is essential for the safe deployment of large language models (LLMs), particularly when users rely on verbalized confidence estimates. While prior work has focused on classifiers or short-form generation, confidence calibration for chain-of-thought (CoT) reasoning remains largely unexplored. Surprisingly, we find that supervised fine-tuning with scalar confidence labels alone suffices to elicit self-verification behavior of language models, without any explicit reasoning supervision or reinforcement learning-based rewards. Despite being trained only to produce a verbalized confidence score without any self-verifying examples, the model learns to generate longer and self-checking responses for low-confidence queries while providing more concise answers for high-confidence ones. We further propose a simple rethinking method that boosts performance via test-time scaling based on calibrated uncertainty. Experiments on GSM8K and held-out reasoning tasks such as MATH-500 and ARC-Challenge show that our confidence-aware fine-tuning improves both calibration and accuracy, while also enhancing interpretability by aligning the model's reasoning path with its confidence.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2506.03723
[cs.CL]
(or
arXiv:2506.03723v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2506.03723
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Chaeyun Jang [
view email
]
[v1]
Wed, 4 Jun 2025 08:56:24 UTC (99 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Verbalized Confidence Triggers Self-Verification: Emergent Behavior Without Explicit Reasoning Supervision, by Chaeyun Jang and 4 other authors
View PDF
HTML (experimental)
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
2025-06
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