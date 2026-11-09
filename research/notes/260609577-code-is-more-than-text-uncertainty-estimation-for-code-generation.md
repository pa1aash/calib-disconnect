---
title: '[2606.09577] Code Is More Than Text: Uncertainty Estimation for Code Generation'
id: 260609577-code-is-more-than-text-uncertainty-estimation-for-code-generation
tags:
- code-llm-calibration-aaai27-eabf3f
- occupancy-partial
- code-uncertainty-estimation
- aaai-bar-eval-dprc-d78e07
created: '2026-07-17T19:27:18.582190Z'
updated: '2026-07-19T20:03:50.894566Z'
source: https://arxiv.org/abs/2606.09577
source_domain: arxiv.org
fetched_at: '2026-07-17T19:27:18.581875Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '''Code Is More Than Text: Uncertainty Estimation for Code Generation'' (arXiv:2606.09577,
  submitted 8 Jun 2026), Shi, Zhang, Li, Wang, Chen, Collier, Gu (Cambridge/Shanghai
  Jiao Tong-affiliated authors). Argues code-specific uncertainty estimation (UE)
  is needed because code differs from natural language in three ways: token fragility
  (one wrong token breaks the program), the intent-code gap (algorithmic intent and
  implementation can diverge independently), and executability. Instantiates these
  as three orthogonal UE axes: lexical (Top-K token entropy), algorithmic (pseudo-code
  consistency), and functional (behavioral/execution consistency). An ensemble of
  the three axes improves average AUROC from 0.696 (strongest NL-derived baseline)
  to 0.776 (+8.1 points) across five code LLMs; on Qwen3-14B, single-pass Top-K token
  entropy alone matches the strongest multi-pass baseline at >3x lower cost. Distinctions
  from the proposed per-test structured-confidence headline: this is an INFERENCE-TIME
  ensemble of UE signals producing a single scalar per-problem/per-generation score
  (evaluated via AUROC discrimination), not a per-test-case dense confidence vector;
  it is not a training method (no SFT/RL to make the model itself express confidence)
  and does not exploit per-test pass/fail as free supervision — the ''functional''
  axis is a behavioral-consistency signal (cross-sample agreement), not per-individual-test
  pass/fail decomposition.'
---

[2606.09577] Code Is More Than Text: Uncertainty Estimation for Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2606.09577
(cs)
[Submitted on 8 Jun 2026]
Title:
Code Is More Than Text: Uncertainty Estimation for Code Generation
Authors:
Yuling Shi
,
Caiqi Zhang
,
Yuexian Li
,
Haopeng Wang
,
Yeheng Chen
,
Nigel Collier
,
Xiaodong Gu
View a PDF of the paper titled Code Is More Than Text: Uncertainty Estimation for Code Generation, by Yuling Shi and 6 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) are increasingly deployed as code generators, where silently wrong programs pose real safety and reliability risks. Reliable uncertainty estimation (UE) is essential for selective prediction, human-in-the-loop review, and downstream agentic decisions. Yet most existing code UE methods are inherited from natural language (NL) generation and ignore properties that make code distinct. We argue that code differs from NL in three ways: a single wrong token can break an entire program (token fragility); algorithmic intent and concrete implementation can disagree independently (intent-code gap); and programs can be executed (executability). We instantiate these properties as three orthogonal uncertainty axes: lexical (Top-K token entropy), algorithmic (pseudo-code consistency), and functional (behavioral consistency). Across five code LLMs, our three-axis ensemble improves average AUROC from 0.696 for the strongest NL-derived baseline to 0.776 (+8.1 points). Notably, on Qwen3-14B, our single-pass Top-K token entropy matches the strongest multi-pass baseline while being over 3x cheaper; across models, it remains a competitive low-cost signal. These results suggest that code UE deserves code-specific design rather than direct NL ports.
Subjects:
Computation and Language (cs.CL)
; Machine Learning (cs.LG); Software Engineering (cs.SE)
Cite as:
arXiv:2606.09577
[cs.CL]
(or
arXiv:2606.09577v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2606.09577
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Yuling Shi [
view email
]
[v1]
Mon, 8 Jun 2026 14:52:43 UTC (728 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Code Is More Than Text: Uncertainty Estimation for Code Generation, by Yuling Shi and 6 other authors
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
2026-06
Change to browse by:
cs
cs.LG
cs.SE
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