---
title: '[2604.12632] Calibration-Aware Policy Optimization for Reasoning LLMs'
id: 260412632-calibration-aware-policy-optimization-for-reasoning-llms
tags:
- code-llm-calibration-aaai27-eabf3f
- auc-discrimination-objective
- single-gpu-lora
- no-code-eval-gap
created: '2026-07-17T18:38:10.573770Z'
updated: '2026-07-17T18:39:17.148929Z'
source: https://arxiv.org/abs/2604.12632
source_domain: arxiv.org
fetched_at: '2026-07-17T18:38:10.573247Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Wang, Lou, Wu, Wen, Zhang (ACL 2026, arXiv:2604.12632). CAPO. Proves that
  GRPO-style overconfidence (incorrect responses getting LOWER perplexity than correct
  ones) stems specifically from uncertainty-agnostic advantage estimation, which misaligns
  optimization gradients with an AUC/AUROC-style discrimination objective -- i.e.,
  pursuing accuracy via a standard advantage function actively degrades ranking/discrimination,
  not just calibration error. Fix: a logistic AUC surrogate loss (theoretically consistent,
  with a provable regret bound) that makes the advantage estimator uncertainty-aware,
  plus a noise-masking mechanism for stable joint optimization. CAPO-1.5B (small model,
  plausibly single-GPU feasible) improves calibration by up to 15% while matching/beating
  GRPO accuracy on math reasoning benchmarks, and boosts inference-time-scaling accuracy
  by up to 5%. Under an abstention option, achieves a Pareto-optimal precision-coverage
  trade-off. Notably frames its core evaluation metric as AUC/AUROC (discrimination)
  rather than ECE, aligning closely with the target paper''s priority on discriminative
  (not just calibrated) expressed confidence. No code-domain evaluation; math reasoning
  only, and the confidence signal is derived from response perplexity/advantage, not
  necessarily a user-facing verbalized token.'
---

*Suggested by [[process-supervision-of-confidence-margin-for-calibrated-llm-reasoning]] — web-search-surfaced adjacent 2026 calibration-aware policy optimization paper*

[2604.12632] Calibration-Aware Policy Optimization for Reasoning LLMs
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2604.12632
(cs)
[Submitted on 14 Apr 2026]
Title:
Calibration-Aware Policy Optimization for Reasoning LLMs
Authors:
Ziqi Wang
,
Xingzhou Lou
,
Meiqi Wu
,
Zhengqi Wen
,
Junge Zhang
View a PDF of the paper titled Calibration-Aware Policy Optimization for Reasoning LLMs, by Ziqi Wang and 4 other authors
View PDF
HTML (experimental)
Abstract:
Group Relative Policy Optimization (GRPO) enhances LLM reasoning but often induces overconfidence, where incorrect responses yield lower perplexity than correct ones, degrading relative calibration as described by the Area Under the Curve (AUC). Existing approaches either yield limited improvements in calibration or sacrifice gains in reasoning accuracy. We first prove that this degradation in GRPO-style algorithms stems from their uncertainty-agnostic advantage estimation, which inevitably misaligns optimization gradients with calibration. This leads to improved accuracy at the expense of degraded calibration. We then propose Calibration-Aware Policy Optimization (CAPO). It adopts a logistic AUC surrogate loss that is theoretically consistent and admits regret bound, enabling uncertainty-aware advantage estimation. By further incorporating a noise masking mechanism, CAPO achieves stable learning dynamics that jointly optimize calibration and accuracy. Experiments on multiple mathematical reasoning benchmarks show that CAPO-1.5B significantly improves calibration by up to 15% while achieving accuracy comparable to or better than GRPO, and further boosts accuracy on downstream inference-time scaling tasks by up to 5%. Moreover, when allowed to abstain under low-confidence conditions, CAPO achieves a Pareto-optimal precision-coverage trade-off, highlighting its practical value for hallucination mitigation.
Comments:
Published as a conference paper at ACL 2026
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2604.12632
[cs.LG]
(or
arXiv:2604.12632v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2604.12632
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Ziqi Wang [
view email
]
[v1]
Tue, 14 Apr 2026 12:03:17 UTC (444 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Calibration-Aware Policy Optimization for Reasoning LLMs, by Ziqi Wang and 4 other authors
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