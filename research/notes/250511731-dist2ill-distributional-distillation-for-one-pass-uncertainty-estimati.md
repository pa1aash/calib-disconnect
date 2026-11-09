---
title: '[2505.11731] Dist2ill: Distributional Distillation for One-Pass Uncertainty
  Estimation in Large Language Models'
id: 250511731-dist2ill-distributional-distillation-for-one-pass-uncertainty-estimati
tags:
- code-llm-calibration-aaai27-eabf3f
- single-pass-uq
- distillation
- calibration-metrics
created: '2026-07-17T18:30:35.170930Z'
updated: '2026-07-17T18:31:44.476789Z'
source: http://arxiv.org/abs/2505.11731
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:35.170412Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Zhao, Tsang, Vejendla, Shi, Li, Hua, Xu, Zhang, Wang, Han, Malin, Wang (v1
  May 2025, extended v3 Feb 2026). Proposes Dist2ill, a distributional-distillation
  framework that trains an LLM to emit MULTIPLE diverse reasoning paths within a SINGLE
  inference pass, paired with a lightweight parametric module that approximates the
  empirical confidence score that would have come from full sampling-based marginalization
  (over weight posterior or reasoning traces). Framed explicitly as a fix for the
  'substantial computational overhead due to repeated sampling at test time' of Bayesian/sampling
  UQ. Reports SOTA Expected Calibration Error (ECE) and Negative Log-Likelihood (NLL)
  while remaining computationally efficient; v3 (Feb 2026) extended the method from
  discriminative to also cover generative reasoning tasks. This is the second-closest
  prior-art precedent to the AAAI-27 angle -- a genuine single-pass architecture that
  internally simulates sample diversity. No AUROC number given in the abstract (uses
  ECE/NLL, not AUROC), and no explicit code-generation validation mentioned -- both
  gaps worth checking in the full paper. Its 'produce multiple reasoning paths in
  one pass' mechanism is a candidate building block or contrast case for a code-specific
  cheap probe.
---

[2505.11731] Dist2ill: Distributional Distillation for One-Pass Uncertainty Estimation in Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2505.11731
(cs)
[Submitted on 16 May 2025 (
v1
), last revised 9 Feb 2026 (this version, v3)]
Title:
Dist2ill: Distributional Distillation for One-Pass Uncertainty Estimation in Large Language Models
Authors:
Yicong Zhao
,
King Yeung Tsang
,
Harshil Vejendla
,
Haizhou Shi
,
Zhuohang Li
,
Zhigang Hua
,
Qi Xu
,
Tunyu Zhang
,
Yi Wang
,
Ligong Han
,
Bradley A. Malin
,
Hao Wang
View a PDF of the paper titled Dist2ill: Distributional Distillation for One-Pass Uncertainty Estimation in Large Language Models, by Yicong Zhao and 11 other authors
View PDF
Abstract:
Large Language Models (LLMs) often exhibit misalignment between the quality of their generated responses and the confidence estimates they assign to them. Bayesian treatments, such as marginalizing over a reliable weight posterior or over the space of reasoning traces, provide an effective remedy, but incur substantial computational overhead due to repeated sampling at test time. To enable accurate uncertainty estimation in a single forward pass, we propose a novel distributional distillation framework (Dist2ill) that trains an LLM to produce multiple diverse reasoning paths within one inference pass, while using a lightweight parametric module to approximate empirical confidence scores derived from the sampling distribution. Extensive experiments demonstrate that Dist2ill preserves reasoning diversity and achieves state-of-the-art uncertainty estimation, substantially improving Expected Calibration Error (ECE) and Negative Log-Likelihood (NLL), while remaining computationally efficient.
Comments:
Preprint; work in progress. Update Log: 05/2025 (v1&v2): Introduced Dist2ill (previously named EUD) for efficient uncertainty estimation, focusing on discriminative reasoning tasks. 02/2026 (v3): Extended Dist2ill to a unified framework supporting both discriminative and generative reasoning
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2505.11731
[cs.LG]
(or
arXiv:2505.11731v3
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2505.11731
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Haizhou Shi [
view email
]
[v1]
Fri, 16 May 2025 22:26:03 UTC (1,347 KB)
[v2]
Fri, 23 May 2025 18:24:43 UTC (1,499 KB)
[v3]
Mon, 9 Feb 2026 03:26:03 UTC (1,289 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Dist2ill: Distributional Distillation for One-Pass Uncertainty Estimation in Large Language Models, by Yicong Zhao and 11 other authors
View PDF
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
2025-05
Change to browse by:
cs
cs.AI
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