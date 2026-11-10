---
title: '[2605.19369] When to Answer and When to Defer: A Decision Framework for Reliable
  Code Predictions'
id: 260519369-when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-cod
tags:
- code-llm-calibration-aaai27-eabf3f
- ut-dallas-scoop-risk
- occupancy-partial
- code-abstention
- aaai-bar-eval-dprc-d78e07
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-17T19:27:13.922973Z'
updated: '2026-11-09T23:26:21.023861Z'
source: https://arxiv.org/abs/2605.19369
source_domain: arxiv.org
fetched_at: '2026-07-17T19:27:13.922662Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '''When to Answer and When to Defer: A Decision Framework for Reliable Code
  Predictions'' (arXiv:2605.19369, submitted 19 May 2026), by Ravishka Rathnasuriya
  (PhD student) and Wei Yang, UT Dallas — published at ICSE-NIER 2026 (New Ideas and
  Emerging Results track, a short/positional-paper venue). CONFIRMED as the UT Dallas
  group named in the scoop-risk brief. Proposes a unified framework integrating (1)
  uncertainty estimation, (2) model calibration, and (3) tool-based abstention handling
  for code models: the model assigns a correctness probability, abstains when uncertain,
  and invokes lightweight program-analysis procedures to validate/repair abstained
  outputs, across both code classification and generation settings. Key critique cited
  from the abstract: post-hoc calibration reduces probability misalignment but fails
  to improve ranking of predictions by correctness likelihood — echoing the parent
  paper''s own ECE-improves/AUROC-degrades finding. CRITICALLY, the correctness probability
  described is a single scalar PER PREDICTION (whole-output level), not a per-test-case
  or per-component structured/localized confidence score, and the abstract gives no
  indication the framework exploits per-test pass/fail as free dense training labels
  — it is architected around post-hoc calibration + selective abstention + external
  tool-based repair, not training the code LLM itself to natively express calibrated
  per-test confidence via SFT/RL on already-computed execution labels. HIGHEST SCOOP-RISK
  SIGNAL: the same authors'' Google Sites publications page lists two SUBMITTED/UNDER-REVIEW
  (not yet on arXiv as of this fetch) papers with near-identical framing: ''Beyond
  Confidence: Rethinking Uncertainty Calibration in Deep Code Models'' and ''Beyond
  Execution: Uncertainty Estimation and Abstention in LLM-Based Code Generation''
  (both Rathnasuriya & Yang). These could not be located publicly and their exact
  mechanism is unknown, but the titles indicate this group is actively working the
  exact code-confidence-calibration niche.'
---

[2605.19369] When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2605.19369
(cs)
[Submitted on 19 May 2026]
Title:
When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions
Authors:
Ravishka Rathnasuriya
,
Wei Yang
View a PDF of the paper titled When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions, by Ravishka Rathnasuriya and 1 other authors
View PDF
HTML (experimental)
Abstract:
Code language models are increasingly adopted for both understanding and generative tasks. Despite their success, these models frequently produce overconfident incorrect predictions and underconfident correct predictions, undermining their reliability in deployment. Practical deployment demands three capabilities: accurately estimating the likelihood of correctness, abstaining on uncertain predictions, and invoking external mechanisms to validate or repair abstained outputs. Existing calibration and uncertainty estimation methods, primarily developed for natural language tasks, do not readily transfer to code. Notably, post-hoc calibration techniques often reduce probability misalignment but fail to improve the ranking of predictions by correctness likelihood-a requirement for selective prediction under partial coverage. Furthermore, most approaches treat uncertainty as a passive indicator rather than an actionable signal. This work introduces a unified framework that integrates uncertainty estimation, model calibration, and tool-based abstention handling for code models. The proposed design enables models to assign reliable correctness probabilities, abstain under uncertainty, and invoke lightweight program analysis procedures to process abstained cases. By combining these components within a single deployment-oriented workflow, this framework supports risk-aware, coverage-controlled use of code models across both classification and generation settings.
Comments:
In Proceedings of the 48th IEEE/ACM International Conference on Software Engineering- New Idea and Emerging Results Track (ICSE-NIER 2026)
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2605.19369
[cs.SE]
(or
arXiv:2605.19369v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2605.19369
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Ravishka Rathnasuriya [
view email
]
[v1]
Tue, 19 May 2026 05:04:42 UTC (262 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions, by Ravishka Rathnasuriya and 1 other authors
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
2026-05
Change to browse by:
cs
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