---
title: '[2601.03525] Beyond Binary: Turning Partial Success into Dense Verifiable
  Rewards for Reinforcement Learning in Code Generation'
id: 260103525-beyond-binary-turning-partial-success-into-dense-verifiable-rewards-fo
tags:
- code-llm-calibration-aaai27-eabf3f
- verpo
- occupancy-distinct
- rl-reward-shaping
- aaai-bar-eval-dprc-d78e07
- code-llm-requirement-pivots-5d35f5
created: '2026-07-17T19:24:50.216320Z'
updated: '2026-07-20T06:53:24.484195Z'
source: https://arxiv.org/abs/2601.03525
source_domain: arxiv.org
fetched_at: '2026-07-17T19:24:50.215979Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'VeRPO (arXiv:2601.03525, submitted Jan 2026, v3 May 2026): an RL framework
  for code-generation RL that converts per-test-case partial success (passing a subset
  of hidden test cases) into a DENSE VERIFIABLE REWARD SIGNAL for policy optimization,
  not a confidence/calibration output. The paper identifies a ''cardinality bias''
  in naive weighted-sum partial-success rewards (updates disproportionately favor
  gains from easy-test successes over frontier-test progress) and introduces a dynamic,
  density-calibrated local reward that corrects this bias, then combines it with global
  execution-outcome reward. Reports up to +8.83 pass@1 gain over outcome-driven and
  reward-model baselines with negligible (<0.02%) time overhead and zero GPU memory
  overhead. Critically: ''calibrated'' here refers to reward-shaping calibration (correcting
  cardinality bias in the reward function), NOT to model-expressed confidence calibration
  (ECE/AUROC/Brier) — the paper never trains or evaluates the model''s ability to
  output a per-test or per-problem confidence score; its sole objective is boosting
  pass@1 correctness via RL.'
---

[2601.03525] Beyond Binary: Turning Partial Success into Dense Verifiable Rewards for Reinforcement Learning in Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2601.03525
(cs)
[Submitted on 7 Jan 2026 (
v1
), last revised 26 May 2026 (this version, v3)]
Title:
Beyond Binary: Turning Partial Success into Dense Verifiable Rewards for Reinforcement Learning in Code Generation
Authors:
Longwen Wang
,
Yirui Liu
,
Xuan'er Wu
,
Xiaohui Hu
,
Yuankai Fan
,
Kaidong Yu
,
Qizhen Weng
,
Wei Xi
,
Xuelong Li
View a PDF of the paper titled Beyond Binary: Turning Partial Success into Dense Verifiable Rewards for Reinforcement Learning in Code Generation, by Longwen Wang and 8 other authors
View PDF
HTML (experimental)
Abstract:
Effective reward design is a central challenge in Reinforcement Learning (RL) for code generation. Mainstream test-suite-level outcome rewards enforce functional correctness but induce sparsity, while external Reward Models (RMs) provide dense supervision at the cost of misalignment and additional overhead. Since code evaluation naturally yields multiple test-case-level outcomes, partial success, i.e., passing a subset of test cases, offers an intrinsic, verifiable source of dense supervision. In this paper, we propose VeRPO (Verifiable Dense Reward Policy Optimization), an RL framework that systematically turns verifiable partial success into reliable dense rewards. We analyze partial-success rewards using a weighted sum formulation, theoretically identifying a critical cardinality bias that causes policy updates to disproportionately favor gains from easy-test successes over progress on frontier tests. Based on this, VeRPO introduces a dynamic, density-calibrated local reward that explicitly corrects this bias and provides robust dense supervision from partial success. To enhance alignment with end-to-end functional correctness, VeRPO further integrates the local dense reward with global execution outcomes. Extensive experiments across diverse benchmarks and settings demonstrate that VeRPO outperforms outcome-driven and RM-based baselines, achieving up to +8.83 pass@1 gain with negligible time cost (< 0.02%) and zero GPU memory overhead.
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2601.03525
[cs.LG]
(or
arXiv:2601.03525v3
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2601.03525
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Longwen Wang [
view email
]
[v1]
Wed, 7 Jan 2026 02:29:49 UTC (1,738 KB)
[v2]
Fri, 9 Jan 2026 03:27:47 UTC (1,737 KB)
[v3]
Tue, 26 May 2026 16:39:06 UTC (533 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Beyond Binary: Turning Partial Success into Dense Verifiable Rewards for Reinforcement Learning in Code Generation, by Longwen Wang and 8 other authors
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
2026-01
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