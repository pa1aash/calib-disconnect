---
title: '[2309.02772] Hot or Cold? Adaptive Temperature Sampling for Code Generation
  with Large Language Models'
id: 230902772-hot-or-cold-adaptive-temperature-sampling-for-code-generation-with-lar
tags:
- code-llm-calibration-aaai27-eabf3f
- decoding-time-action
- aaai-precedent
created: '2026-07-17T18:34:20.605272Z'
updated: '2026-07-17T18:35:47.542811Z'
source: https://arxiv.org/abs/2309.02772
source_domain: arxiv.org
fetched_at: '2026-07-17T18:34:20.604869Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: AAAI 2024 paper introducing AdapT (Adaptive Temperature) sampling, the baseline
  that AdaDec (2506.08980) beats. Systematic study of loss distributions of code tokens
  finds they split into 'challenging' tokens (hard to predict, concentrated at the
  start of code blocks) and 'confident' tokens (easily inferred); AdapT applies a
  larger sampling temperature to challenging tokens (encourage exploration) and a
  smaller temperature to confident tokens (suppress tail-randomness noise). This IS
  a downstream decoding ACTION driven by a per-token uncertainty proxy (loss/perplexity,
  single-pass) with a measured payoff -- 'significantly outperforms state-of-the-art
  decoding strategy' across model sizes and two datasets -- establishing precedent
  (and an AAAI acceptance track record) for token-uncertainty-as-decoding-control
  papers in code generation. Uses raw loss/perplexity as the uncertainty proxy, not
  repeated-sampling confidence, and never audits its calibration against ground-truth
  correctness.
---

*Suggested by [[250608980-adadec-a-uncertainty-guided-lookahead-decoding-framework-for-llm-based]] — AdapT baseline cited/compared against in AdaDec abstract*

[2309.02772] Hot or Cold? Adaptive Temperature Sampling for Code Generation with Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2309.02772
(cs)
[Submitted on 6 Sep 2023 (
v1
), last revised 28 Dec 2023 (this version, v3)]
Title:
Hot or Cold? Adaptive Temperature Sampling for Code Generation with Large Language Models
Authors:
Yuqi Zhu
,
Jia Li
,
Ge Li
,
YunFei Zhao
,
Jia Li
,
Zhi Jin
,
Hong Mei
View a PDF of the paper titled Hot or Cold? Adaptive Temperature Sampling for Code Generation with Large Language Models, by Yuqi Zhu and 6 other authors
View PDF
HTML (experimental)
Abstract:
Recently, Large Language Models (LLMs) have shown impressive abilities in code generation. However, existing LLMs' decoding strategies are designed for Natural Language (NL) generation, overlooking the differences between NL and programming languages (PL). Due to this oversight, a better decoding strategy for code generation remains an open question. In this paper, we conduct the first systematic study to explore a decoding strategy specialized in code generation. With an analysis of loss distributions of code tokens, we find that code tokens can be divided into two categories: challenging tokens that are difficult to predict and confident tokens that can be easily inferred. Among them, the challenging tokens mainly appear at the beginning of a code block. Inspired by the above findings, we propose a simple yet effective method: Adaptive Temperature (AdapT) sampling, which dynamically adjusts the temperature coefficient when decoding different tokens. We apply a larger temperature when sampling for challenging tokens, allowing LLMs to explore diverse choices. We employ a smaller temperature for confident tokens avoiding the influence of tail randomness noises. We apply AdapT sampling to LLMs with different sizes and conduct evaluations on two popular datasets. Results show that AdapT sampling significantly outperforms state-of-the-art decoding strategy.
Comments:
This paper is accepted by AAAI 2024
Subjects:
Software Engineering (cs.SE)
; Computation and Language (cs.CL)
Cite as:
arXiv:2309.02772
[cs.SE]
(or
arXiv:2309.02772v3
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2309.02772
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Yuqi Zhu [
view email
]
[v1]
Wed, 6 Sep 2023 06:27:33 UTC (5,076 KB)
[v2]
Sat, 14 Oct 2023 09:27:51 UTC (5,076 KB)
[v3]
Thu, 28 Dec 2023 10:54:36 UTC (7,687 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Hot or Cold? Adaptive Temperature Sampling for Code Generation with Large Language Models, by Yuqi Zhu and 6 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.SE
< prev
|
next >
new
|
recent
|
2023-09
Change to browse by:
cs
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