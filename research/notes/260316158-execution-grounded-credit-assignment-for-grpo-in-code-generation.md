---
title: '[2603.16158] Execution-Grounded Credit Assignment for GRPO in Code Generation'
id: 260316158-execution-grounded-credit-assignment-for-grpo-in-code-generation
tags:
- code-llm-requirement-pivots-5d35f5
- rl-reward-shaping
- credit-assignment
created: '2026-07-20T06:51:31.630938Z'
updated: '2026-07-20T06:53:47.245629Z'
source: https://arxiv.org/abs/2603.16158
source_domain: arxiv.org
fetched_at: '2026-07-20T06:51:31.630458Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Mar 2026 paper (ICLR 2026 SPOT workshop) proposing Execution-Grounded Credit
  Assignment (EGCA) for critic-free RLVR/GRPO code RL: rather than reward magnitude
  decomposition, it fixes CREDIT ASSIGNMENT WITHIN a failing program by executing
  the candidate against a canonical reference solution under identical instrumentation,
  locating the earliest semantic divergence point, and restricting the GRPO advantage/gradient
  to the token span up to that divergence (masking downstream tokens) rather than
  spreading one outcome signal uniformly across the whole generated program. Drop-in
  modification, no critic/auxiliary loss/learned verifier needed. Reports 82.1% pass@1
  on HumanEval (+3.1 over vanilla GRPO) and 68.9% on MBPP (+1.5), with 18% wall-clock
  training overhead. This is orthogonal-but-adjacent to reward-decomposition-by-requirement:
  it decomposes credit spatially within one solution''s token sequence using execution
  traces, rather than decomposing the reward magnitude by which of several stated
  requirements/tests were satisfied. Narrows the available novelty for any per-requirement
  reward-shaping proposal, since fine-grained execution-trace-based credit assignment
  for GRPO code RL is already an accepted workshop contribution.'
---

[2603.16158] Execution-Grounded Credit Assignment for GRPO in Code Generation
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2603.16158
(cs)
[Submitted on 17 Mar 2026]
Title:
Execution-Grounded Credit Assignment for GRPO in Code Generation
Authors:
Abhijit Kumar
,
Natalya Kumar
,
Shikhar Gupta
View a PDF of the paper titled Execution-Grounded Credit Assignment for GRPO in Code Generation, by Abhijit Kumar and 2 other authors
View PDF
HTML (experimental)
Abstract:
Critic-free reinforcement learning with verifiable rewards (RLVR) improves code generation by optimizing unit-test pass rates, but GRPO-style updates suffer from coarse credit assignment: a single outcome signal is spread uniformly across long programs even when failure stems from a localized semantic error. We propose Execution-Grounded Credit Assignment (EGCA), which localizes GRPO updates using execution traces. For programs that satisfy algorithmic constraints but fail tests, EGCA executes the candidate and a canonical reference solution (curated once offline; used for analysis, not supervision) under identical instrumentation, identifies the earliest semantic divergence, and assigns advantage only to the corresponding token span while masking downstream tokens. EGCA is a drop-in modification requiring no critic, auxiliary loss, or learned verifier, yielding 82.1% pass@1 on HumanEval (+3.1 over GRPO) and 68.9% on MBPP (+1.5) with 18% wall-clock overhead.
Comments:
Accepted at SPOT ICLR 2026 (
this https URL
)
Subjects:
Machine Learning (cs.LG)
Cite as:
arXiv:2603.16158
[cs.LG]
(or
arXiv:2603.16158v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2603.16158
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Abhijit Kumar [
view email
]
[v1]
Tue, 17 Mar 2026 06:22:44 UTC (1,331 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Execution-Grounded Credit Assignment for GRPO in Code Generation, by Abhijit Kumar and 2 other authors
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