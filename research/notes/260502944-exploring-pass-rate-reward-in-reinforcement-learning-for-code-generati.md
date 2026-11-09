---
title: '[2605.02944] Exploring Pass-Rate Reward in Reinforcement Learning for Code
  Generation'
id: 260502944-exploring-pass-rate-reward-in-reinforcement-learning-for-code-generati
tags:
- code-llm-requirement-pivots-5d35f5
- rl-reward-shaping
- negative-result
created: '2026-07-20T06:51:21.798465Z'
updated: '2026-07-20T06:53:33.613696Z'
source: https://arxiv.org/abs/2605.02944
source_domain: arxiv.org
fetched_at: '2026-07-20T06:51:21.798116Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Rigorous controlled study (May 2026, Nanjing Univ group) directly refuting
  the naive form of our proposed direction: tests critic-free RL (GRPO, RLOO) with
  test-case pass-rate as a dense surrogate reward vs. binary whole-task pass/fail
  across multiple base code LLMs, and finds pass-rate reward does NOT reliably beat
  binary reward despite being denser. Mechanistic explanation: pass-rate is a miscalibrated
  surrogate for progress toward full correctness, and when no rollout in a GRPO/RLOO
  group achieves full pass, partial-pass solutions induce conflicting/canceling gradient
  directions at the group level, so the induced update fails to consistently move
  probability mass toward full-pass solutions. This is a load-bearing negative result:
  it shows that simply substituting per-requirement/per-test pass-fraction for binary
  reward -- the naive version of our pivot idea -- is already empirically tested and
  found insufficient in a controlled ablation, and the paper explicitly calls for
  ''reward designs that better align optimization with the goal of full correctness,''
  which is exactly the gap VeRPO (2601.03525) and EGCA (2603.16158) separately claim
  to fill.'
---

[2605.02944] Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2605.02944
(cs)
[Submitted on 1 May 2026]
Title:
Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation
Authors:
Xin-Ye Li
,
Ren-Biao Liu
,
Yun-Ji Zhang
,
Hui Sun
,
Zheng Xie
,
Ming Li
View a PDF of the paper titled Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation, by Xin-Ye Li and 5 other authors
View PDF
HTML (experimental)
Abstract:
Reinforcement learning (RL) from unit-test feedback has become a standard post-training recipe for improving large language models (LLMs) on code generation. However, the pass-all-tests binary reward can be sparse, yielding no learning signal on challenging problems where none of the sampled solutions passes all tests. A common remedy is to use the test-case pass rate as a surrogate reward.
In this work, we study pass-rate rewards in critic-free RL for code generation (e.g., GRPO and RLOO) and report a consistent pattern across base models and algorithms: despite alleviating reward sparsity, pass-rate rewards do not reliably improve final performance over binary rewards in rigorous controlled experiments.
To understand this discrepancy, we analyze reward density and the resulting gradient directions. We find that pass-rate rewards are denser, but the induced gradient updates do not consistently move probability mass toward full-pass solutions. This arises because test-case pass rate is a miscalibrated surrogate for progress toward full correctness, and partial-pass solutions within the same group can induce conflicting gradient directions that cancel out.
Overall, our results suggest that, in critic-free RL, pass-rate rewards are insufficient to improve code generation and motivate reward designs that better align optimization with the goal of full correctness.
Comments:
16 pages, 6 figures
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Software Engineering (cs.SE)
Cite as:
arXiv:2605.02944
[cs.LG]
(or
arXiv:2605.02944v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2605.02944
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Xin-Ye Li [
view email
]
[v1]
Fri, 1 May 2026 10:26:43 UTC (367 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation, by Xin-Ye Li and 5 other authors
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
2026-05
Change to browse by:
cs
cs.AI
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