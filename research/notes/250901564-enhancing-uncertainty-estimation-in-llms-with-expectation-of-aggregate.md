---
title: '[2509.01564] Enhancing Uncertainty Estimation in LLMs with Expectation of
  Aggregated Internal Belief'
id: 250901564-enhancing-uncertainty-estimation-in-llms-with-expectation-of-aggregate
tags:
- aaai-bar-eval-dprc-d78e07
- calibration
- aaai-accepted-2026
- internal-belief-probing
- code-llm-probe-verbalize-gap-3d8995
created: '2026-07-19T20:01:59.324932Z'
updated: '2026-07-20T06:38:06.580094Z'
source: https://arxiv.org/abs/2509.01564
source_domain: arxiv.org
fetched_at: '2026-07-19T20:01:59.324582Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'AAAI 2026 (arXiv comment ''Accepted by AAAI 2026''). Xiao, Dou, Xiong, Chen,
  Chen propose EAGLE (Expectation of AGgregated internaL bEief): a self-evaluation
  calibration method that reads confidence not just from the model''s final output/logit
  but from INTERMEDIATE HIDDEN LAYERS during a self-evaluation prompt, aggregates
  layer-wise ''internal beliefs'' into a distribution, and takes the expectation as
  the refined confidence score. Targets overconfidence specifically in RLHF''d models.
  Scope: ''extensive experiments on diverse datasets and LLMs'' plus ablations --
  layer-wise uncertainty pattern analysis, self-evaluation prompt sensitivity study,
  and self-evaluation score-range analysis. Novelty type: new method (white-box, layer-aggregation
  self-eval) + mechanistic analysis (which layers carry the most calibration signal),
  positioned against existing self-eval / verbalized-confidence and single-layer-probe
  baselines. Relevant to DPRC as a comparator on ''where in the model does reliable
  confidence live'' -- EAGLE argues intermediate layers beat the final layer; DPRC''s
  tokenized-digit readout is a final-layer/output-level signal, so EAGLE is a natural
  ablation DPRC reviewers could demand (''did you try reading confidence from internal
  layers instead of a primed output token?'').'
---

[2509.01564] Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal Belief
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2509.01564
(cs)
[Submitted on 1 Sep 2025 (
v1
), last revised 23 Dec 2025 (this version, v2)]
Title:
Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal Belief
Authors:
Zeguan Xiao
,
Diyang Dou
,
Boya Xiong
,
Yun Chen
,
Guanhua Chen
View a PDF of the paper titled Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal Belief, by Zeguan Xiao and 4 other authors
View PDF
HTML (experimental)
Abstract:
Large Language Models (LLMs) have achieved remarkable success across a wide range of natural language tasks, but often exhibit overconfidence and generate plausible yet incorrect answers. This overconfidence, especially in models undergone Reinforcement Learning from Human Feedback (RLHF), poses significant challenges for reliable uncertainty estimation and safe deployment. In this paper, we propose EAGLE (Expectation of AGgregated internaL bEief), a novel self-evaluation-based calibration method that leverages the internal hidden states of LLMs to derive more accurate confidence scores. Instead of relying on the model's final output, our approach extracts internal beliefs from multiple intermediate layers during self-evaluation. By aggregating these layer-wise beliefs and calculating the expectation over the resulting confidence score distribution, EAGLE produces a refined confidence score that more faithfully reflects the model's internal certainty. Extensive experiments on diverse datasets and LLMs demonstrate that EAGLE significantly improves calibration performance over existing baselines. We also provide an in-depth analysis of EAGLE, including a layer-wise examination of uncertainty patterns, a study of the impact of self-evaluation prompts, and an analysis of the effect of self-evaluation score range.
Comments:
Accepted by AAAI 2026
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2509.01564
[cs.CL]
(or
arXiv:2509.01564v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2509.01564
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Zeguan Xiao [
view email
]
[v1]
Mon, 1 Sep 2025 15:50:10 UTC (179 KB)
[v2]
Tue, 23 Dec 2025 12:29:17 UTC (227 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal Belief, by Zeguan Xiao and 4 other authors
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
2025-09
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