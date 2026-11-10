---
title: '[2603.25052] Closing the Confidence-Faithfulness Gap in Large Language Models'
id: 260325052-closing-the-confidence-faithfulness-gap-in-large-language-models-2
tags:
- code-llm-probe-verbalize-gap-3d8995
- faithfulness-gap
- verbalized-confidence
- mechanistic-interpretability
- scoop-risk
- novelty-risk
- steering-fix
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-20T06:38:22.486534Z'
updated: '2026-11-09T23:25:58.299192Z'
source: https://arxiv.org/abs/2603.25052
source_domain: arxiv.org
fetched_at: '2026-07-20T06:38:22.486104Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Miao, Ungar (arXiv v1 26 Mar 2026, v2 1 Apr 2026; venue not stated in abstract
  page). Mechanistic-interpretability paper that names and formalizes the exact phenomenon
  the pivot calls a ''faithfulness gap'': using linear probes + contrastive activation
  addition (CAA) steering across 3 open-weight models and 4 datasets, shows CALIBRATION
  signal (does the model''s internal state predict correctness) and VERBALIZED-CONFIDENCE
  signal are both linearly decodable from activations but are ORTHOGONAL directions
  -- i.e. the model''s stated confidence is not just a lossy readout of its internal
  calibration, it is a geometrically distinct, largely uncorrelated signal. Identifies
  a ''Reasoning Contamination Effect'': prompting the model to simultaneously reason
  (CoT) and verbalize confidence causes the reasoning process to disrupt/overwrite
  the verbalized-confidence direction, WORSENING miscalibration. UTILITY MOVE: proposes
  a two-stage adaptive steering pipeline that reads the internal accuracy-estimate
  direction and steers the verbalized output toward it, substantially improving calibration
  alignment across all evaluated models -- i.e. the paper doesn''t stop at diagnosing
  the gap, it closes it with an intervention and re-measures calibration as the outcome
  metric. General QA/reasoning domain, not code, not per-requirement. Strongest signal
  in this search that ''faithfulness/verbalization gap'' framing is being actively
  published RIGHT NOW (Mar-Jul 2026) as mechanistic-interpretability work with an
  intervention, not treated as a dead-end negative result -- but every instance found
  (this paper, the forecasting paper) pairs the diagnosis with either a steering-based
  FIX or a deployment-utility cashout, never leaves the gap as the terminal contribution.'
---

[2603.25052] Closing the Confidence-Faithfulness Gap in Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2603.25052
(cs)
[Submitted on 26 Mar 2026 (
v1
), last revised 1 Apr 2026 (this version, v2)]
Title:
Closing the Confidence-Faithfulness Gap in Large Language Models
Authors:
Miranda Muqing Miao
,
Lyle Ungar
View a PDF of the paper titled Closing the Confidence-Faithfulness Gap in Large Language Models, by Miranda Muqing Miao and 1 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) tend to verbalize confidence scores that are largely detached from their actual accuracy, yet the geometric relationship governing this behavior remain poorly understood. In this work, we present a mechanistic interpretability analysis of verbalized confidence, using linear probes and contrastive activation addition (CAA) steering to show that calibration and verbalized confidence signals are encoded linearly but are orthogonal to one another -- a finding consistent across three open-weight models and four datasets. Interestingly, when models are prompted to simultaneously reason through a problem and verbalize a confidence score, the reasoning process disrupts the verbalized confidence direction, exacerbating miscalibration. We term this the "Reasoning Contamination Effect." Leveraging this insight, we introduce a two-stage adaptive steering pipeline that reads the model's internal accuracy estimate and steers verbalized output to match it, substantially improving calibration alignment across all evaluated models.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2603.25052
[cs.CL]
(or
arXiv:2603.25052v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2603.25052
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Muqing Miao [
view email
]
[v1]
Thu, 26 Mar 2026 05:42:04 UTC (966 KB)
[v2]
Wed, 1 Apr 2026 05:05:49 UTC (2,145 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Closing the Confidence-Faithfulness Gap in Large Language Models, by Miranda Muqing Miao and 1 other authors
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