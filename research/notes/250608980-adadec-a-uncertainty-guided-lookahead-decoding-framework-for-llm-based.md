---
title: '[2506.08980] AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for
  LLM-Based Code Generation'
id: 250608980-adadec-a-uncertainty-guided-lookahead-decoding-framework-for-llm-based
tags:
- code-llm-calibration-aaai27-eabf3f
- decoding-time-action
- token-level-uncertainty
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-17T18:29:43.668504Z'
updated: '2026-11-09T23:26:02.736117Z'
source: http://arxiv.org/abs/2506.08980
source_domain: arxiv.org
fetched_at: '2026-07-17T18:29:43.667818Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Token-level uncertainty-guided adaptive decoding for code LLMs. An empirical
  study first shows many generation errors stem from token-RANKING mistakes at high-uncertainty
  decoding steps (correct token present but not top-1). AdaDec then learns model-specific
  uncertainty thresholds on next-token entropy/logit uncertainty and, when a step''s
  uncertainty exceeds threshold, triggers a lookahead pause-then-rerank (limited local
  search) instead of continuing greedy decoding. Decision rule: per-token threshold
  trigger, not sampling-based or execution-based. Utility metric: Pass@1 accuracy
  on HumanEval+, MBPP+, DevEval -- up to +20.9% absolute over greedy decoding, and
  consistently beats Beam Search and the adaptive-decoding baseline AdapT, with selective
  triggering keeping efficiency high. This IS a downstream action with a measured
  payoff, but the uncertainty signal is single-pass TOKEN-LEVEL (an ''expressed interface''
  type the target paper shows is NOT faithfully calibrated to correctness) and the
  paper never audits that signal''s calibration quality (no AUROC/ECE) -- it only
  uses uncertainty as a heuristic trigger, not a validated confidence estimate. Open
  question for extension: does substituting the near-perfectly-calibrated repeated-sampling
  confidence as the trigger signal improve on AdaDec''s accuracy/efficiency tradeoff?'
---

[2506.08980] AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2506.08980
(cs)
[Submitted on 10 Jun 2025 (
v1
), last revised 24 Apr 2026 (this version, v5)]
Title:
AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code Generation
Authors:
Kaifeng He
,
Mingwei Liu
,
Chong Wang
,
Zike Li
,
Yanlin Wang
,
Xin Peng
,
Zibin Zheng
View a PDF of the paper titled AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code Generation, by Kaifeng He and 6 other authors
View PDF
HTML (experimental)
Abstract:
Code generation with large language models (LLMs) is highly sensitive to token selection during decoding, particularly at uncertain decision points that influence program logic. While standard strategies such as greedy decoding treat all tokens uniformly, they overlook code-specific uncertainty patterns, leading to suboptimal performance. This paper presents an empirical study revealing that many generation errors stem from token ranking mistakes at high-uncertainty steps, where the correct token is present but not top-ranked.
Motivated by these findings, we propose AdaDec, a lookahead-based uncertainty-guided adaptive decoding framework that integrates a token-level pause-then-rerank mechanism driven by token uncertainty. AdaDec learns model-specific uncertainty thresholds and applies a lookahead-based reranking strategy when uncertainty is high. Experiments on HumanEval+, MBPP+, and DevEval benchmarks show that AdaDec improves Pass@1 accuracy by up to 20.9% in absolute terms over greedy decoding. More importantly, it consistently outperforms both competitive baselines like Beam Search and state-of-the-art adaptive decoding methods such as AdapT, while maintaining high efficiency through selective, uncertainty-triggered pausing. Our results highlight the promise of uncertainty-aware adaptive decoding for improving both the reliability and efficiency of LLM-based code generation.
Comments:
23 pages, 7 figures, FSE 2026
Subjects:
Software Engineering (cs.SE)
ACM
classes:
I.2.7; I.2.2
Cite as:
arXiv:2506.08980
[cs.SE]
(or
arXiv:2506.08980v5
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2506.08980
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: He Kaifeng [
view email
]
[v1]
Tue, 10 Jun 2025 16:49:46 UTC (529 KB)
[v2]
Wed, 11 Jun 2025 04:29:51 UTC (529 KB)
[v3]
Fri, 19 Sep 2025 07:14:38 UTC (534 KB)
[v4]
Wed, 25 Feb 2026 15:08:15 UTC (556 KB)
[v5]
Fri, 24 Apr 2026 10:45:51 UTC (565 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code Generation, by Kaifeng He and 6 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.SE
< prev
|
next >
new
|
recent
|
2025-06
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