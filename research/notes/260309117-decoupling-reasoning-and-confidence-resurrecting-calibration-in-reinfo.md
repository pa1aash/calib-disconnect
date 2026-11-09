---
title: '[2603.09117] Decoupling Reasoning and Confidence: Resurrecting Calibration
  in Reinforcement Learning from Verifiable Rewards'
id: 260309117-decoupling-reasoning-and-confidence-resurrecting-calibration-in-reinfo
tags:
- code-llm-calibration-aaai27-eabf3f
- gradient-conflict-theory
- no-code-eval-gap
- aaai-bar-eval-dprc-d78e07
created: '2026-07-17T18:38:04.743860Z'
updated: '2026-07-19T20:03:37.040512Z'
source: https://arxiv.org/abs/2603.09117
source_domain: arxiv.org
fetched_at: '2026-07-17T18:38:04.743476Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Ma, Wen, Cao, Lu, Lin, Yang, He, Han, Sun (ICML 2026, arXiv:2603.09117).
  DCPO. THEORETICAL result directly relevant to design of any train-time calibration
  objective: proves that directly incorporating a calibration objective (e.g., a Brier/log-scoring
  term as in RLCR/Rewarding Doubt) into the same RLVR optimization target as accuracy
  creates a FUNDAMENTAL GRADIENT CONFLICT between maximizing policy accuracy and minimizing
  calibration error -- the two gradients can point in opposing directions during optimization.
  DCPO''s fix is to systematically DECOUPLE the reasoning (accuracy) and calibration
  objectives (e.g., separate optimization steps/heads rather than a single summed
  reward), preserving GRPO-level accuracy while achieving the best calibration and
  substantially mitigating overconfidence. This is a load-bearing theoretical caveat
  for any AAAI-27 methodological paper that proposes a joint correctness+calibration
  reward: it must either show the gradient-conflict issue doesn''t bind in the code
  domain, or adopt a decoupled objective design. No code-domain evaluation in this
  paper either (general RLVR reasoning setting).'
---

*Suggested by [[process-supervision-of-confidence-margin-for-calibrated-llm-reasoning]] — web-search-surfaced adjacent 2026 train-time calibration RLVR paper*

[2603.09117] Decoupling Reasoning and Confidence: Resurrecting Calibration in Reinforcement Learning from Verifiable Rewards
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2603.09117
(cs)
[Submitted on 10 Mar 2026 (
v1
), last revised 27 May 2026 (this version, v3)]
Title:
Decoupling Reasoning and Confidence: Resurrecting Calibration in Reinforcement Learning from Verifiable Rewards
Authors:
Zhengzhao Ma
,
Xueru Wen
,
Boxi Cao
,
Yaojie Lu
,
Hongyu Lin
,
Jinglin Yang
,
Min He
,
Xianpei Han
,
Le Sun
View a PDF of the paper titled Decoupling Reasoning and Confidence: Resurrecting Calibration in Reinforcement Learning from Verifiable Rewards, by Zhengzhao Ma and 8 other authors
View PDF
HTML (experimental)
Abstract:
Reinforcement Learning from Verifiable Rewards (RLVR) significantly enhances large language models (LLMs) reasoning but severely suffers from calibration degeneration, where models become excessively over-confident in incorrect answers. Previous studies devote to directly incorporating calibration objective into existing optimization target. However, our theoretical analysis demonstrates that there exists a fundamental gradient conflict between the optimization for maximizing policy accuracy and minimizing calibration error. Building on this insight, we propose DCPO, a simple yet effective framework that systematically decouples reasoning and calibration objectives. Extensive experiments demonstrate that our DCPO not only preserves accuracy on par with GRPO but also achieves the best calibration performance and substantially mitigates the over-confidence issue. Our study provides valuable insights and practical solution for more reliable LLM deployment.
Comments:
Accepted at the 43rd International Conference on Machine Learning (ICML 2026)
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2603.09117
[cs.LG]
(or
arXiv:2603.09117v3
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2603.09117
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Zhengzhao Ma [
view email
]
[v1]
Tue, 10 Mar 2026 02:47:59 UTC (756 KB)
[v2]
Thu, 30 Apr 2026 07:39:01 UTC (1,027 KB)
[v3]
Wed, 27 May 2026 02:49:05 UTC (422 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Decoupling Reasoning and Confidence: Resurrecting Calibration in Reinforcement Learning from Verifiable Rewards, by Zhengzhao Ma and 8 other authors
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
2026-03
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