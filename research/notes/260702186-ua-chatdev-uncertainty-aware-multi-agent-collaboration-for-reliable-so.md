---
title: '[2607.02186] UA-ChatDev: Uncertainty-Aware Multi-Agent Collaboration for Reliable
  Software Development'
id: 260702186-ua-chatdev-uncertainty-aware-multi-agent-collaboration-for-reliable-so
tags:
- code-llm-calibration-aaai27-eabf3f
- ua-chatdev
- occupancy-partial
- multi-agent-swe
created: '2026-07-17T19:24:54.225164Z'
updated: '2026-07-17T19:25:38.225826Z'
source: https://arxiv.org/abs/2607.02186
source_domain: arxiv.org
fetched_at: '2026-07-17T19:24:54.224825Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'UA-ChatDev (arXiv:2607.02186, submitted 2 Jul 2026): an uncertainty-aware
  MULTI-AGENT software development framework (built on ChatDev-style role-based agents:
  requirements analyst, coder, tester, etc.) that adds a ''lightweight uncertainty
  estimation mechanism based on token-level log probabilities'' to assess confidence
  of each agent''s response, and uses ''phase-aware threshold calibration'' to decide
  when to trigger retrieval-based verification (RAG) if uncertainty exceeds a threshold.
  Evaluated on the SRDD benchmark, reporting gains in completeness, executability,
  consistency, and overall software-quality metrics versus single-agent and multi-agent
  baselines, plus ablations/communication analyses. Distinctions from the proposed
  per-test structured-confidence headline: (1) uncertainty signal is TOKEN LOG-PROBABILITY,
  the same proxy the parent paper already showed is poorly discriminative (AUROC 0.668)
  and behaves differently from execution-verified per-test confidence; (2) granularity
  is per-AGENT-RESPONSE / per-development-PHASE (requirements, design, coding, testing),
  not per-TEST-CASE within a single code-generation problem; (3) ''calibration'' here
  means threshold-tuning for when to trigger verification, not ECE/AUROC-style probability
  calibration against ground-truth correctness; (4) the confidence signal is never
  validated against actual test-execution outcomes as ground truth — no per-test pass/fail
  labels are used as supervision at all, so it does not exploit code''s free per-test
  verifiability the way the proposed method does.'
---

[2607.02186] UA-ChatDev: Uncertainty-Aware Multi-Agent Collaboration for Reliable Software Development
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2607.02186
(cs)
[Submitted on 2 Jul 2026]
Title:
UA-ChatDev: Uncertainty-Aware Multi-Agent Collaboration for Reliable Software Development
Authors:
Temitayo Olamilekan Ogunsusi
,
Lijun Qian
,
Xishuang Dong
View a PDF of the paper titled UA-ChatDev: Uncertainty-Aware Multi-Agent Collaboration for Reliable Software Development, by Temitayo Olamilekan Ogunsusi and 2 other authors
View PDF
HTML (experimental)
Abstract:
Software development is a complex task that demands cooperation among agents with diverse roles. Large language models (LLMs) have enabled autonomous multi-agent software development frameworks that leverage role-based collaboration to automate requirements analysis, coding, testing, and refinement. However, existing approaches typically assume that intermediate agent outputs are equally reliable, leaving them vulnerable to hallucination propagation, where incorrect decisions generated in early development phases are transferred to downstream agents and negatively impact final software quality. To address this challenge, we propose UA-ChatDev, an uncertainty-aware multi-agent software development framework that integrates uncertainty quantification into agent interactions. It introduces a lightweight uncertainty estimation mechanism based on token-level log probabilities to assess the confidence of agent responses and employs phase-aware threshold calibration to selectively trigger retrieval-based verification when uncertainty exceeds acceptable levels. Extensive experiments on the SRDD benchmark demonstrate that UA-ChatDev consistently outperforms existing single-agent and multi-agent software development frameworks across completeness, executability, consistency, and overall quality metrics. Further ablation studies and communication analyses verify that uncertainty-aware interactions enhance code execution reliability.
Subjects:
Artificial Intelligence (cs.AI)
Cite as:
arXiv:2607.02186
[cs.AI]
(or
arXiv:2607.02186v1
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2607.02186
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Xishuang Dong [
view email
]
[v1]
Thu, 2 Jul 2026 13:56:57 UTC (2,037 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled UA-ChatDev: Uncertainty-Aware Multi-Agent Collaboration for Reliable Software Development, by Temitayo Olamilekan Ogunsusi and 2 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.AI
< prev
|
next >
new
|
recent
|
2026-07
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