---
title: '[2503.15341] Uncertainty-Guided Chain-of-Thought for Code Generation with
  LLMs'
id: 250315341-uncertainty-guided-chain-of-thought-for-code-generation-with-llms
tags:
- code-llm-calibration-aaai27-eabf3f
- expressed-uncertainty
- adaptive-compute
- log-prob-confidence
created: '2026-07-17T18:29:52.823170Z'
updated: '2026-07-17T18:33:52.688721Z'
source: http://arxiv.org/abs/2503.15341
source_domain: arxiv.org
fetched_at: '2026-07-17T18:29:52.822717Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'UnCert-CoT (Zhu, Li, Jiang, Li, Mei, Jin, Dong; Mar 2025): addresses CoT
  "overthinking" in code generation by gating extended reasoning on an uncertainty
  signal computed from the LLM''s own OUTPUT DISTRIBUTION (expressed/log-prob-based,
  not hidden-state probing). Proposes two lightweight, single-pass confidence measures
  -- Entropy-based and Probability-Differential-based -- computed over next-token
  distributions during initial generation. When uncertainty is high, the method activates
  CoT-decoding to produce multiple reasoning paths and picks the code with highest
  estimated correctness likelihood; when uncertainty is low, it skips extra reasoning
  and generates directly. Evaluated on MHPP (Mostly Hard Python Problems); reports
  up to +6.1 points PassRate/pass@1 accuracy versus baseline CoT, concentrated on
  cases where plain LLMs are error-prone.


  Relevance: this is a genuine EXPRESSED-uncertainty method (entropy/prob-diff over
  logits, i.e., a log-prob-derived interface) used not to communicate confidence to
  a user but to internally gate compute allocation (adaptive test-time reasoning).
  It does not report AUROC/calibration of the uncertainty signal against ground-truth
  functional correctness directly -- the abstract frames uncertainty purely as a routing
  mechanism, so it is an example of the "expressed interface exists but is validated
  only for a proxy task (efficiency), not for calibration against correctness" pattern
  the base paper diagnoses. Useful contrast case: log-prob-based entropy is treated
  as good enough to gate reasoning depth, but its calibration quality (AUROC vs the
  0.987 sampling benchmark) is not established here -- a gap the new AAAI-27 paper
  could exploit by testing whether such entropy/prob-diff measures, which are essentially
  free (computed from the already-generated logits, no extra passes), correlate with
  functional correctness at all, or only with "task hardness."'
---

[2503.15341] Uncertainty-Guided Chain-of-Thought for Code Generation with LLMs
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2503.15341
(cs)
[Submitted on 19 Mar 2025]
Title:
Uncertainty-Guided Chain-of-Thought for Code Generation with LLMs
Authors:
Yuqi Zhu
,
Ge Li
,
Xue Jiang
,
Jia Li
,
Hong Mei
,
Zhi Jin
,
Yihong Dong
View a PDF of the paper titled Uncertainty-Guided Chain-of-Thought for Code Generation with LLMs, by Yuqi Zhu and 6 other authors
View PDF
HTML (experimental)
Abstract:
Chain-of-Thought (CoT) reasoning has been demonstrated as an effective technique for improving the problem-solving capabilities of large language models (LLMs) in the context of code generation. However, existing CoT methods often exhibit a tendency toward "overthinking", where the LLM consistently applies reasoning strategies without adequately considering the task's underlying complexity. This results in the LLMs allocating excessive computational resources, in terms of tokens, to relatively simple tasks or problems where the correct answer is already evident. Additionally, this overthinking may lead LLMs down incorrect reasoning paths, resulting in incorrect code generation. In this paper, we introduce UnCertainty-Aware Chain-of-Thought (UnCert-CoT), an LLM-based approach designed to enhance code generation by incorporating an uncertainty-aware CoT reasoning mechanism, which focuses computational resources on targeting points where LLMs are more prone to error. We propose two confidence-based uncertainty measures: Entropy-based and Probability Differential-based methods. When uncertainty is high, UnCert-CoT activates CoT-decoding to generate multiple reasoning paths and selects the final code that exhibits the highest likelihood of correctness. In contrast, LLM directly generates the code when uncertainty is low. This uncertainty judgment mechanism allows LLMs to prioritize complex tasks and avoid unnecessary steps in simpler cases, thereby improving overall efficiency and accuracy in code generation. Our experimental results demonstrate that UnCert-CoT significantly enhances code generation accuracy on challenging benchmark MHPP(Mostly Hard Python Problems), it achieves improvements up to 6.1% on PassRate accuracy, particularly in situations where traditional LLMs are prone to errors.
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2503.15341
[cs.SE]
(or
arXiv:2503.15341v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2503.15341
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Yuqi Zhu [
view email
]
[v1]
Wed, 19 Mar 2025 15:40:45 UTC (796 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Uncertainty-Guided Chain-of-Thought for Code Generation with LLMs, by Yuqi Zhu and 6 other authors
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
2025-03
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