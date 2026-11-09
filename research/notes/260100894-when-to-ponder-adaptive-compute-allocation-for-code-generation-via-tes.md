---
title: '[2601.00894] When to Ponder: Adaptive Compute Allocation for Code Generation
  via Test-Time Training'
id: 260100894-when-to-ponder-adaptive-compute-allocation-for-code-generation-via-tes
tags:
- code-llm-requirement-pivots-5d35f5
- adaptive-compute-allocation
- test-time-training
created: '2026-07-20T06:52:47.604927Z'
updated: '2026-07-20T06:55:16.828112Z'
source: https://arxiv.org/abs/2601.00894
source_domain: arxiv.org
fetched_at: '2026-07-20T06:52:47.604593Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'PonderTTT (Gihyeon Sim, Dec 2025, GPT-2 124M-1.5B on The Stack v2 code LM):
  training-free gating strategy using a TTT layer''s self-supervised reconstruction
  loss as a signal to decide when to trigger test-time-training weight updates per
  input, rather than uniformly for all inputs. Achieves 82-89% Oracle Recovery vs
  Random Skip baselines, up to 16% lower loss on OOD languages. Granularity is per-input
  (whole code sequence), not per-requirement/per-test-case, and the task is next-token
  code language modeling perplexity, not solving discrete coding problems with unit-test
  requirements. Closest existing analog to ''spend more compute where confidence is
  low'' but at sequence level, not sub-task/requirement level -- confirms daylight
  exists for genuinely per-requirement compute allocation.'
---

[2601.00894] When to Ponder: Adaptive Compute Allocation for Code Generation via Test-Time Training
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2601.00894
(cs)
[Submitted on 31 Dec 2025]
Title:
When to Ponder: Adaptive Compute Allocation for Code Generation via Test-Time Training
Authors:
Gihyeon Sim
View a PDF of the paper titled When to Ponder: Adaptive Compute Allocation for Code Generation via Test-Time Training, by Gihyeon Sim
View PDF
HTML (experimental)
Abstract:
Large language models apply uniform computation to all inputs, regardless of difficulty. We propose PonderTTT, a gating strategy using the TTT layer's self-supervised reconstruction loss to selectively trigger Test-Time Training (TTT) updates. The gating decision itself is training-free--requiring no learned classifier or auxiliary networks; only a single scalar threshold is initially calibrated on unlabeled data and continuously adapted via EMA to maintain target update rates. Our experiments with GPT-2 models (124M to 1.5B) on code language modeling (The Stack v2, teacher-forced perplexity) demonstrate that this signal is inference-compatible, requiring no ground-truth labels. Our Reconstruction Gating achieves 82-89% Oracle Recovery while being fully training-free, significantly outperforming Random Skip baselines (up to 16% lower loss on OOD languages).
Comments:
14 pages, 1 figure, 14 tables, code available at
this https URL
Subjects:
Machine Learning (cs.LG)
; Computation and Language (cs.CL)
Cite as:
arXiv:2601.00894
[cs.LG]
(or
arXiv:2601.00894v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2601.00894
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Gi Hyeon Sim [
view email
]
[v1]
Wed, 31 Dec 2025 14:49:54 UTC (31 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled When to Ponder: Adaptive Compute Allocation for Code Generation via Test-Time Training, by Gihyeon Sim
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
2026-01
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