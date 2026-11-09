---
title: '[2603.03752] Confidence-Calibrated Small-Large Language Model Collaboration
  for Cost-Efficient Reasoning'
id: 260303752-confidence-calibrated-small-large-language-model-collaboration-for-cos
tags:
- aaai-bar-eval-dprc-d78e07
- calibration
- selective-prediction
- venue-mismatch
- eacl-2026
- venue-mismatch-not-aaai
- downstream-utility-framing
- code-llm-probe-verbalize-gap-3d8995
created: '2026-07-19T20:02:36.460010Z'
updated: '2026-07-20T06:38:07.647919Z'
source: https://arxiv.org/abs/2603.03752
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:36.459660Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'VENUE MISMATCH FLAG: arXiv comment explicitly states ''Accepted to EACL
  2026 Main Conference'' -- this is NOT an AAAI paper despite initial web-search summaries
  mislabeling it as AAAI 2026. Keeping in vault as a NON-AAAI comparator, not evidence
  for the AAAI bar. Zhang, Zhu, Wei et al. propose COREA (COllaborative REAsoner):
  cascades a small LM with a large LM, where the SLM outputs both an answer and a
  verbalized confidence score; questions below a confidence threshold are deferred
  to the LLM. Trains the SLM''s confidence calibration via an RL (GRPO-style) reward
  that jointly optimizes reasoning accuracy and confidence calibration. Results: 21.5%
  cost reduction on out-of-domain math and 16.8% on non-math datasets vs LLM-only,
  with pass@1 drop within 2%. Novelty type: new method (RL-trained verbalized-confidence-gated
  cascade) with a downstream UTILITY metric (cost reduction) rather than calibration
  metrics alone -- directly relevant to DPRC''s ''deliverable 5'' question about adding
  a downstream-utility result: COREA demonstrates that pairing a calibration signal
  with a concrete deployment use-case (cascade routing / cost savings) is a publishable
  framing at a top venue, a template DPRC could borrow (e.g., routing to human review
  or re-generation only for low-confidence per-requirement predictions).'
---

[2603.03752] Confidence-Calibrated Small-Large Language Model Collaboration for Cost-Efficient Reasoning
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2603.03752
(cs)
[Submitted on 4 Mar 2026]
Title:
Confidence-Calibrated Small-Large Language Model Collaboration for Cost-Efficient Reasoning
Authors:
Chuang Zhang
,
Zizhen Zhu
,
Yihao Wei
,
Bing Tian
,
Junyi Liu
,
Henan Wang
,
Xavier Wang
,
Yaxiao Liu
View a PDF of the paper titled Confidence-Calibrated Small-Large Language Model Collaboration for Cost-Efficient Reasoning, by Chuang Zhang and 7 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) demonstrate superior reasoning capabilities compared to small language models (SLMs), but incur substantially higher costs. We propose COllaborative REAsoner (COREA), a system that cascades an SLM with an LLM to achieve a balance between accuracy and cost in complex reasoning tasks. COREA first attempts to answer questions using the SLM, which outputs both an answer and a verbalized confidence score. Questions with confidence below a predefined threshold are deferred to the LLM for more accurate resolution. We introduce a reinforcement learning-based training algorithm that aligns the SLM's confidence through an additional confidence calibration reward. Extensive experiments demonstrate that our method jointly improves the SLM's reasoning ability and confidence calibration across diverse datasets and model backbones. Compared to using the LLM alone, COREA reduces cost by 21.5% and 16.8% on out-of-domain math and non-math datasets, respectively, with only an absolute pass@1 drop within 2%.
Comments:
Accepted to EACL 2026 Main Conference
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2603.03752
[cs.CL]
(or
arXiv:2603.03752v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2603.03752
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Chuang Zhang [
view email
]
[v1]
Wed, 4 Mar 2026 05:55:20 UTC (288 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Confidence-Calibrated Small-Large Language Model Collaboration for Cost-Efficient Reasoning, by Chuang Zhang and 7 other authors
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
2026-03
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