---
title: '[2604.23333] Process Supervision of Confidence Margin for Calibrated LLM Reasoning'
id: 260423333-process-supervision-of-confidence-margin-for-calibrated-llm-reasoning
tags:
- code-llm-calibration-aaai27-eabf3f
- process-supervision
- code-benchmark-tested
created: '2026-07-17T18:30:11.456424Z'
updated: '2026-07-17T18:33:57.511339Z'
source: http://arxiv.org/abs/2604.23333
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:11.455899Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: arXiv abstract page for Wang, Zuo, Jurayj, Van Durme, Liu (JHU) 2026, RLCM
  (COLM 2026). Process-level RL reward widens the confidence margin between correct/incorrect
  intermediate reasoning steps within a trajectory rather than aligning confidence
  to accuracy directly; tested across math, code, logic, and science benchmarks. Confidence
  is read from a trained linear probe on hidden states, NOT a verbalized token --
  see full-text note 'process-supervision-of-confidence-margin-for-calibrated-llm-reasoning'
  for the code-benchmark (LiveCodeBench) numbers and the explicit finding that verbalized
  confidence (RLCR) underperforms probe-based confidence.
---

[2604.23333] Process Supervision of Confidence Margin for Calibrated LLM Reasoning
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2604.23333
(cs)
[Submitted on 25 Apr 2026]
Title:
Process Supervision of Confidence Margin for Calibrated LLM Reasoning
Authors:
Liaoyaqi Wang
,
Chunsheng Zuo
,
William Jurayj
,
Benjamin Van Durme
,
Anqi Liu
View a PDF of the paper titled Process Supervision of Confidence Margin for Calibrated LLM Reasoning, by Liaoyaqi Wang and 4 other authors
View PDF
HTML (experimental)
Abstract:
Scaling test-time computation with reinforcement learning (RL) has emerged as a reliable path to improve large language models (LLM) reasoning ability. Yet, outcome-based reward often incentivizes models to be overconfident, leading to hallucinations, unreliable confidence-based control, and unnecessary compute allocation. We introduce Reinforcement Learning with Confidence Margin (\textbf{RLCM}), a calibration-aware RL framework that jointly optimizes correctness and confidence reliability via a margin-enhanced process reward over intermediate-budget completions. Rather than aligning confidence to correctness likelihoods, RLCM encourages to widen the confidence margin between correct and incorrect steps within a single reasoning trajectory. Across mathematical, code, logic and science benchmarks, our method substantially improves calibration while maintaining or improving accuracy. We further show that, with calibrated confidence signals, the resulting models enable more efficient conformal risk control and effective confidence-weighted aggregation.
Subjects:
Machine Learning (cs.LG)
; Computation and Language (cs.CL)
Cite as:
arXiv:2604.23333
[cs.LG]
(or
arXiv:2604.23333v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2604.23333
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Liaoyaqi Wang [
view email
]
[v1]
Sat, 25 Apr 2026 14:40:13 UTC (543 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Process Supervision of Confidence Margin for Calibrated LLM Reasoning, by Liaoyaqi Wang and 4 other authors
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
2026-04
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