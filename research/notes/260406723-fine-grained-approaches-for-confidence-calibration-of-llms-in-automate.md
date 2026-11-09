---
title: '[2604.06723] Fine-grained Approaches for Confidence Calibration of LLMs in
  Automated Code Revision'
id: 260406723-fine-grained-approaches-for-confidence-calibration-of-llms-in-automate
tags:
- code-llm-probe-verbalize-gap-3d8995
- fine-grained-code-calibration
- novelty-risk
- not-probing
created: '2026-07-20T06:38:49.794315Z'
updated: '2026-07-20T06:39:51.278644Z'
source: https://arxiv.org/abs/2604.06723
source_domain: arxiv.org
fetched_at: '2026-07-20T06:38:49.793964Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Lin, Liu, Gao, Thongtanunam, Treude (arXiv 8 Apr 2026, SE venue -- no AAAI/major-venue
  accept tag visible in abstract). Direct prior-art comparator on ''fine-grained code
  confidence'': argues global/sequence-level Platt-scaling calibration (the standard
  post-hoc calibration baseline) is ill-suited to automated code revision (ACR: program
  repair, vulnerability repair, code refinement) because correctness there is determined
  by LOCAL EDIT DECISIONS, and proposes local Platt-scaling applied separately to
  three different fine-grained (sub-sequence/edit-level) confidence scores. Evaluated
  across 3 tasks x 14 models, finds fine-grained scores consistently give lower calibration
  error across probability intervals, amplified when combined with global scaling.
  IMPORTANT DISTINCTION from the pivot: this is a CALIBRATION-METHOD paper (recalibrating
  existing confidence scores/logits with Platt scaling), not a PROBING paper (no hidden-state
  readout of latent correctness) and not per-requirement (their ''fine-grained'' =
  per-edit/per-hunk, not per-functional-requirement/per-test-case). No verbalized-vs-internal
  comparison and no faithfulness-gap framing at all. Establishes that ''fine-grained
  code confidence calibration'' as a topic is already being worked in SE venues via
  a different (non-probing, non-faithfulness) mechanism -- raises the bar for DPRC''s
  novelty claim on granularity alone; DPRC needs to differentiate on (a) probing internal
  states vs external logit recalibration, and (b) the verbalize/probe faithfulness
  gap, which this paper does not touch.'
---

[2604.06723] Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2604.06723
(cs)
[Submitted on 8 Apr 2026]
Title:
Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision
Authors:
Hong Yi Lin
,
Chunhua Liu
,
Haoyu Gao
,
Patanamon Thongtanunam
,
Christoph Treude
View a PDF of the paper titled Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision, by Hong Yi Lin and 4 other authors
View PDF
HTML (experimental)
Abstract:
In today's AI-assisted software engineering landscape, developers increasingly depend on LLMs that are highly capable, yet inherently imperfect. The tendency of these models to produce incorrect outputs can reduce developer productivity. To this end, a canonical mitigation method is to provide calibrated confidence scores that faithfully reflect their likelihood of correctness at the instance-level. Such information allows users to make immediate decisions regarding output acceptance, abstain error-prone outputs, and better align their expectations with the model's capabilities. Since post-trained LLMs do not inherently produce well-calibrated confidence scores, researchers have developed post-hoc calibration methods, with global Platt-scaling of sequence-level confidence scores proving effective in many generative software engineering tasks but remaining unreliable or unexplored for automated code revision (ACR) tasks such as program repair, vulnerability repair, and code refinement. We hypothesise that the coarse-grained nature of this conventional method makes it ill-suited for ACR tasks, where correctness is often determined by local edit decisions and miscalibration can be sample-dependent, thereby motivating fine-grained confidence calibration. To address this, our study proposes local Platt-scaling applied separately to three different fine-grained confidence scores. Through experiments across 3 separate tasks and correctness metrics, as well as 14 different models of various sizes, we find that fine-grained confidence scores consistently achieve lower calibration error across a broader range of probability intervals, and this effect is further amplified when global Platt-scaling is applied. Our proposed approaches offer a practical solution to eliciting well-calibrated confidence scores, enabling more trustworthy and streamlined usage of imperfect models in ACR tasks.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2604.06723
[cs.SE]
(or
arXiv:2604.06723v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2604.06723
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Hong Yi Lin [
view email
]
[v1]
Wed, 8 Apr 2026 06:41:09 UTC (9,896 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision, by Hong Yi Lin and 4 other authors
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
2026-04
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