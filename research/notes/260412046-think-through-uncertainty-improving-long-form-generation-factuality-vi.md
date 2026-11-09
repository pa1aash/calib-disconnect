---
title: '[2604.12046] Think Through Uncertainty: Improving Long-Form Generation Factuality
  via Reasoning Calibration'
id: 260412046-think-through-uncertainty-improving-long-form-generation-factuality-vi
tags:
- code-llm-calibration-aaai27-eabf3f
- aaai-bar-eval-dprc-d78e07
created: '2026-07-17T19:24:41.255175Z'
updated: '2026-07-19T20:03:38.316998Z'
source: https://arxiv.org/abs/2604.12046
source_domain: arxiv.org
fetched_at: '2026-07-17T19:24:41.254850Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Abstract-only arXiv page for CURE (2604.12046); full text fetched separately
  at note think-through-uncertainty-improving-long-form-generation-factuality-via-reasonin.
  See that note for full occupancy analysis.
---

[2604.12046] Think Through Uncertainty: Improving Long-Form Generation Factuality via Reasoning Calibration
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2604.12046
(cs)
[Submitted on 13 Apr 2026]
Title:
Think Through Uncertainty: Improving Long-Form Generation Factuality via Reasoning Calibration
Authors:
Xin Liu
,
Lu Wang
View a PDF of the paper titled Think Through Uncertainty: Improving Long-Form Generation Factuality via Reasoning Calibration, by Xin Liu and Lu Wang
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) often hallucinate in long-form generation. Existing approaches mainly improve factuality through post-hoc revision or reinforcement learning (RL) with correctness-based rewards, but they do not teach the model to estimate which parts of its generation are reliable. As a result, models may still state incorrect claims confidently in their responses. Recent advances in reasoning have significantly improved LLM performance, and have been leveraged to estimate confidence by incorporating calibration into RL objectives. However, existing approaches remain limited to a single scalar confidence for the entire response, which is insufficient for long-form generation where uncertainty varies across individual claims. To mitigate this problem, we propose CURE, a framework that improves long-form factuality by teaching LLMs to reason about uncertainty at the claim level. We first introduce a Claim-Aware Reasoning Protocol, which structures outputs into atomic claims paired with explicit confidence estimates. We then develop a multi-stage training pipeline that aligns model confidence with claims' correctness and then optimizes on factuality. The resulting calibrated confidence further enables selective prediction, allowing the model to abstain from uncertain claims at inference time. Experiments on four long-form factuality benchmarks show that CURE consistently improves factual accuracy over competitive supervised and RL baselines, while maintaining factual recall. In particular, it improves claim-level accuracy by up to 39.9% on Biography generation. These gains are accompanied by improved calibration, as reflected by a 16.0% increase in AUROC on FactBench.
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2604.12046
[cs.CL]
(or
arXiv:2604.12046v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2604.12046
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Xin Liu [
view email
]
[v1]
Mon, 13 Apr 2026 20:38:36 UTC (965 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Think Through Uncertainty: Improving Long-Form Generation Factuality via Reasoning Calibration, by Xin Liu and Lu Wang
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
2026-04
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