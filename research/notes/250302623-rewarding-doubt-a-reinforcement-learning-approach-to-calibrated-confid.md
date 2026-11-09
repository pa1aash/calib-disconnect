---
title: '[2503.02623] Rewarding Doubt: A Reinforcement Learning Approach to Calibrated
  Confidence Expression of Large Language Models'
id: 250302623-rewarding-doubt-a-reinforcement-learning-approach-to-calibrated-confid
tags:
- code-llm-calibration-aaai27-eabf3f
- verbalized-confidence-rl
- single-gpu-lora
created: '2026-07-17T18:29:56.387671Z'
updated: '2026-07-17T18:33:46.316488Z'
source: http://arxiv.org/abs/2503.02623
source_domain: arxiv.org
fetched_at: '2026-07-17T18:29:56.387120Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: arXiv abstract page for Bani-Harouni et al. 2025/2026, 'Rewarding Doubt'
  (TU Munich). RL fine-tunes LLMs with a log-scoring-rule reward that penalizes over/under-confidence
  so the optimal policy is perfectly calibrated verbalized confidence, integrated
  into generation rather than a decoupled probe. See full-text note 'rewarding-doubt-a-reinforcement-learning-approach-to-calibrated-confidence-expre'
  for method/results detail.
---

[2503.02623] Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2503.02623
(cs)
[Submitted on 4 Mar 2025 (
v1
), last revised 28 Feb 2026 (this version, v6)]
Title:
Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of Large Language Models
Authors:
David Bani-Harouni
,
Chantal Pellegrini
,
Paul Stangel
,
Ege Özsoy
,
Kamilia Zaripova
,
Nassir Navab
,
Matthias Keicher
View a PDF of the paper titled Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of Large Language Models, by David Bani-Harouni and 6 other authors
View PDF
HTML (experimental)
Abstract:
A safe and trustworthy use of Large Language Models (LLMs) requires an accurate expression of confidence in their answers. We propose a novel Reinforcement Learning approach that allows to directly fine-tune LLMs to express calibrated confidence estimates alongside their answers to factual questions. Our method optimizes a reward based on the logarithmic scoring rule, explicitly penalizing both over- and under-confidence. This encourages the model to align its confidence estimates with the actual predictive accuracy. The optimal policy under our reward design would result in perfectly calibrated confidence expressions. Unlike prior approaches that decouple confidence estimation from response generation, our method integrates confidence calibration seamlessly into the generative process of the LLM. Empirically, we demonstrate that models trained with our approach exhibit substantially improved calibration and generalize to unseen tasks without further fine-tuning, suggesting the emergence of general confidence awareness.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2503.02623
[cs.CL]
(or
arXiv:2503.02623v6
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2503.02623
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: David Bani-Harouni [
view email
]
[v1]
Tue, 4 Mar 2025 13:48:50 UTC (1,218 KB)
[v2]
Wed, 5 Mar 2025 15:23:16 UTC (1,218 KB)
[v3]
Fri, 23 May 2025 09:40:34 UTC (1,069 KB)
[v4]
Tue, 27 Jan 2026 16:03:47 UTC (129 KB)
[v5]
Wed, 28 Jan 2026 08:51:18 UTC (129 KB)
[v6]
Sat, 28 Feb 2026 17:29:41 UTC (129 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Rewarding Doubt: A Reinforcement Learning Approach to Calibrated Confidence Expression of Large Language Models, by David Bani-Harouni and 6 other authors
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
2025-03
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