---
title: '[2212.03827] Discovering Latent Knowledge in Language Models Without Supervision'
id: 221203827-discovering-latent-knowledge-in-language-models-without-supervision
tags:
- code-llm-probe-verbalize-gap-3d8995
- latent-knowledge
- ccs
- unsupervised-probing
- foundational
created: '2026-07-20T06:35:17.535130Z'
updated: '2026-07-20T06:36:09.239765Z'
source: https://arxiv.org/abs/2212.03827
source_domain: arxiv.org
fetched_at: '2026-07-20T06:35:17.534803Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Burns, Ye, Klein, Steinhardt (ICLR 2023). Introduces Contrast-Consistent
  Search (CCS): an UNSUPERVISED method that finds a linear direction in a language
  model''s activation space encoding truth value, using only logical-consistency constraints
  (a statement and its negation must have opposite truth values) -- no labels, no
  model outputs used for training the probe. Tested across 6 models and 10 QA/true-false
  datasets; CCS-derived answers outperform the model''s own zero-shot-generated answers
  by 4% accuracy on average, and the method halves prompt sensitivity and stays accurate
  even when the model is deliberately prompted to lie/generate incorrect answers.
  This is the foundational ''what a model knows vs. what it says'' framing paper:
  explicitly frames its contribution as recovering latent knowledge ''distinct from
  what they say,'' i.e. establishing internal representations can be MORE reliable
  than the model''s surface output, using zero external supervision. Domain: general
  factual/commonsense true-false and QA benchmarks (e.g. BoolQ, IMDB sentiment as
  a truth-like binary task, COPA, etc.) -- NOT code, NOT per-requirement decomposition.
  Granularity: WHOLE-STATEMENT binary truth value only. Highly cited (1000s of citations)
  foundational precedent for ''probe recovers truth the model doesn''t say'' but at
  coarse whole-claim granularity in non-code domains, using an unsupervised contrastive
  method rather than a supervised per-requirement correctness classifier.'
---

[2212.03827] Discovering Latent Knowledge in Language Models Without Supervision
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2212.03827
(cs)
[Submitted on 7 Dec 2022 (
v1
), last revised 2 Mar 2024 (this version, v2)]
Title:
Discovering Latent Knowledge in Language Models Without Supervision
Authors:
Collin Burns
,
Haotian Ye
,
Dan Klein
,
Jacob Steinhardt
View a PDF of the paper titled Discovering Latent Knowledge in Language Models Without Supervision, by Collin Burns and 3 other authors
View PDF
HTML (experimental)
Abstract:
Existing techniques for training language models can be misaligned with the truth: if we train models with imitation learning, they may reproduce errors that humans make; if we train them to generate text that humans rate highly, they may output errors that human evaluators can't detect. We propose circumventing this issue by directly finding latent knowledge inside the internal activations of a language model in a purely unsupervised way. Specifically, we introduce a method for accurately answering yes-no questions given only unlabeled model activations. It works by finding a direction in activation space that satisfies logical consistency properties, such as that a statement and its negation have opposite truth values. We show that despite using no supervision and no model outputs, our method can recover diverse knowledge represented in large language models: across 6 models and 10 question-answering datasets, it outperforms zero-shot accuracy by 4\% on average. We also find that it cuts prompt sensitivity in half and continues to maintain high accuracy even when models are prompted to generate incorrect answers. Our results provide an initial step toward discovering what language models know, distinct from what they say, even when we don't have access to explicit ground truth labels.
Comments:
ICLR 2023
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2212.03827
[cs.CL]
(or
arXiv:2212.03827v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2212.03827
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Collin Burns [
view email
]
[v1]
Wed, 7 Dec 2022 18:17:56 UTC (1,486 KB)
[v2]
Sat, 2 Mar 2024 21:33:53 UTC (5,120 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Discovering Latent Knowledge in Language Models Without Supervision, by Collin Burns and 3 other authors
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
2022-12
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