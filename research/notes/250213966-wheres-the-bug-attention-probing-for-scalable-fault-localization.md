---
title: '[2502.13966] Where''s the Bug? Attention Probing for Scalable Fault Localization'
id: 250213966-wheres-the-bug-attention-probing-for-scalable-fault-localization
tags:
- code-llm-calibration-aaai27-eabf3f
- attention-probe
- distinct
- no-execution-training-signal
created: '2026-07-17T19:30:25.369904Z'
updated: '2026-07-17T19:31:07.182710Z'
source: https://arxiv.org/abs/2502.13966
source_domain: arxiv.org
fetched_at: '2026-07-17T19:30:25.369585Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'BAP / Bug Attention Probe (Stein, Wayne, Naik, Naik, Wong; arXiv:2502.13966,
  Feb 2025) is a fault-localization method that learns to predict buggy lines by probing
  an LLM''s ATTENTION patterns, trained with weak supervision from bug reports alone
  -- explicitly WITHOUT requiring executable test cases or direct line-level localization
  labels (''Existing FL approaches rely on executable test cases, require training
  on costly and often noisy line-level annotations... BAP learns state-of-the-art
  fault localization without any direct localization labels''). Evaluated across 8
  datasets (including Defects4J, real-world Java bugs) via top-1 accuracy: +34.6%
  over strongest FL baseline, +93.4% over zero-shot GPT-4o prompting. FLARE''s paper
  cites BAP as one of the fault-localization baselines it beats (54% Top-1 for BAP
  vs FLARE''s 67%). OCCUPANCY vs proposed headline: DISTINCT -- BAP is (1) a probe
  on model-internal attention weights, not the generating LLM''s own self-reported/expressed
  confidence; (2) line-level, not test-case/requirement-level; (3) evaluated via Top-1/Top-N
  localization accuracy, never AUROC or a calibration metric; (4) explicitly avoids
  using execution/test signals as its training source (the opposite emphasis from
  the proposed paper''s per-test-execution-verifiability angle). It is methodologically
  adjacent (model-internal-signal-based code fault localization) but occupies none
  of the load-bearing conjunction terms.'
---

*Suggested by [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement]] — BAP fault-localization baseline FLARE compares against; uses attention probing (model-internal signal) for line-level bug localization*

[2502.13966] Where's the Bug? Attention Probing for Scalable Fault Localization
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2502.13966
(cs)
[Submitted on 19 Feb 2025 (
v1
), last revised 20 Feb 2025 (this version, v2)]
Title:
Where's the Bug? Attention Probing for Scalable Fault Localization
Authors:
Adam Stein
,
Arthur Wayne
,
Aaditya Naik
,
Mayur Naik
,
Eric Wong
View a PDF of the paper titled Where's the Bug? Attention Probing for Scalable Fault Localization, by Adam Stein and 4 other authors
View PDF
HTML (experimental)
Abstract:
Ensuring code correctness remains a challenging problem even as large language models (LLMs) become increasingly capable at code-related tasks. While LLM-based program repair systems can propose bug fixes using only a user's bug report, their effectiveness is fundamentally limited by their ability to perform fault localization (FL), a challenging problem for both humans and LLMs. Existing FL approaches rely on executable test cases, require training on costly and often noisy line-level annotations, or demand resource-intensive LLMs. In this paper, we present Bug Attention Probe (BAP), a method which learns state-of-the-art fault localization without any direct localization labels, outperforming traditional FL baselines and prompting of large-scale LLMs. We evaluate our approach across a variety of code settings, including real-world Java bugs from the standard Defects4J dataset as well as seven other datasets which span a diverse set of bug types and languages. Averaged across all eight datasets, BAP improves by 34.6% top-1 accuracy compared to the strongest baseline and 93.4% over zero-shot prompting GPT-4o. BAP is also significantly more efficient than prompting, outperforming large open-weight models at a small fraction of the computational cost.
Comments:
14 pages, 5 figures
Subjects:
Software Engineering (cs.SE)
; Machine Learning (cs.LG)
Cite as:
arXiv:2502.13966
[cs.SE]
(or
arXiv:2502.13966v2
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2502.13966
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Adam Stein [
view email
]
[v1]
Wed, 19 Feb 2025 18:59:32 UTC (398 KB)
[v2]
Thu, 20 Feb 2025 02:29:19 UTC (437 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Where's the Bug? Attention Probing for Scalable Fault Localization, by Adam Stein and 4 other authors
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
2025-02
Change to browse by:
cs
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