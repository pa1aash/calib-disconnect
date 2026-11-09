---
title: '[2512.07404] On LLMs'' Internal Representation of Code Correctness'
id: 251207404-on-llms-internal-representation-of-code-correctness
tags:
- code-llm-probe-verbalize-gap-3d8995
- hidden-state-probe
- whole-program-granularity
- verbalized-vs-internal-comparison
created: '2026-07-20T06:36:31.399806Z'
updated: '2026-07-20T06:39:14.387819Z'
source: https://arxiv.org/abs/2512.07404
source_domain: arxiv.org
fetched_at: '2026-07-20T06:36:31.399404Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Ribeiro, Spiess, Devanbu, Nadi (ICSE 2026 accepted; arXiv:2512.07404, v1
  titled ''Do LLMs Trust the Code They Write?''). Identifies a CODE-CORRECTNESS DIRECTION
  inside LLM hidden states by contrasting mean hidden-state activations between pairs
  of correct vs incorrect code generated for the SAME programming task (a RepE/contrastive-direction
  technique, analogous to prior truthfulness-direction work in NLP, applied to code
  for the first time). Tested on 4 open code LLMs. Central result: this extracted
  internal-representation signal OUTPERFORMS both (a) standard log-likelihood/sequence-probability
  ranking and (b) VERBALIZED model confidence (the model''s own stated/prompted confidence)
  at identifying correct code. Also shows the internal signal can select higher-quality
  code samples WITHOUT requiring test execution. CRITICAL OCCUPANCY FINDING for the
  pivot: this paper already establishes the core ''internal representation beats verbalized
  confidence for code correctness'' comparison -- but strictly at WHOLE-SOLUTION/WHOLE-PROGRAM
  granularity (one correctness label per generated program, not per unit test or per
  requirement). It does not decompose correctness into per-test/per-requirement outcomes,
  does not train the model itself to emit calibrated per-requirement confidence, and
  does not report an AUROC-style probe number broken out by requirement. This means
  the ''internal-knowledge-vs-verbalized'' framing for code is NOT novel per se (this
  ICSE''26 paper already has it); the pivot''s novelty must rest entirely on (1) PER-REQUIREMENT/per-unit-test
  granularity of both the probe and the verbalization target, (2) comparing against
  TRAINED (SFT/RL) self-reported confidence rather than zero-shot prompted verbalization,
  and (3) downstream utility tied to the per-requirement signal specifically.'
---

[2512.07404] On LLMs' Internal Representation of Code Correctness
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2512.07404
(cs)
[Submitted on 8 Dec 2025 (
v1
), last revised 21 Jan 2026 (this version, v3)]
Title:
On LLMs' Internal Representation of Code Correctness
Authors:
Francisco Ribeiro
,
Claudio Spiess
,
Prem Devanbu
,
Sarah Nadi
View a PDF of the paper titled On LLMs' Internal Representation of Code Correctness, by Francisco Ribeiro and 3 other authors
View PDF
HTML (experimental)
Abstract:
Despite the effectiveness of large language models (LLMs) for code generation, they often output incorrect code. One reason is that model output probabilities are often not well-correlated with correctness, and reflect only the final output of the generation process. Inspired by findings that LLMs internally encode concepts like truthfulness, this paper explores if LLMs similarly represent code correctness. Specifically, we identify a correctness representation inside LLMs by contrasting the hidden states between pairs of correct and incorrect code for the same programming tasks. By experimenting on four LLMs, we show that exploiting this extracted correctness representation outperforms standard log-likelihood ranking, as well as verbalized model confidence. Furthermore, we explore how this internal correctness signal can be used to select higher-quality code samples, without requiring test execution. Ultimately, this work demonstrates how leveraging internal representations can enhance code generation systems and make LLMs more reliable, thus improving confidence in automatically generated code.
Comments:
Accepted for ICSE'26
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2512.07404
[cs.SE]
(or
arXiv:2512.07404v3
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2512.07404
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Francisco Ribeiro [
view email
]
[v1]
Mon, 8 Dec 2025 10:38:03 UTC (293 KB)
[v2]
Mon, 5 Jan 2026 11:52:55 UTC (293 KB)
[v3]
Wed, 21 Jan 2026 12:24:23 UTC (228 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled On LLMs' Internal Representation of Code Correctness, by Francisco Ribeiro and 3 other authors
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
2025-12
Change to browse by:
cs
cs.AI
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