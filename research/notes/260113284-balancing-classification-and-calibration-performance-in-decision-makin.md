---
title: '[2601.13284] Balancing Classification and Calibration Performance in Decision-Making
  LLMs via Calibration Aware Reinforcement Learning'
id: 260113284-balancing-classification-and-calibration-performance-in-decision-makin
tags:
- code-llm-calibration-aaai27-eabf3f
- rlvr-overconfidence
- sft-vs-rlvr-calibration
created: '2026-07-17T18:31:17.828807Z'
updated: '2026-07-17T18:35:29.742964Z'
source: http://arxiv.org/abs/2601.13284
source_domain: arxiv.org
fetched_at: '2026-07-17T18:31:17.828171Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv:2601.13284 (Yaldiz, Spiliopoulou, Qi, Varia, Doss, Pappas; submitted
  Jan 19 2026). Directly relevant secondary anchor for the AAAI-27 extension: systematically
  studies calibration under two fine-tuning paradigms for decision-making LLMs --
  supervised fine-tuning (SFT) vs. reinforcement learning with verifiable rewards
  (RLVR). Headline finding: RLVR improves task accuracy but produces extremely overconfident
  models, whereas SFT yields substantially better calibration (even under distribution
  shift) at the cost of smaller accuracy gains -- establishing an explicit classification-accuracy-vs-calibration
  tradeoff across training paradigms. Diagnostic mechanism: decision tokens act merely
  as ''extraction steps'' in reasoning traces and do not carry confidence information,
  which is why RLVR cannot surface calibrated alternatives (the RL objective never
  rewards confidence honesty at the decision token). Proposes a calibration-aware
  RL formulation that directly adjusts decision-token probabilities, preserving RLVR''s
  accuracy while reducing ECE by up to 9 points. This is not code-specific (general
  decision-making LLMs) but supplies the fine-tuning-paradigm mechanism (RLVR overconfidence
  vs. SFT calibration) that the Spiess et al. ICSE 2025 paper does not test -- Spiess
  only evaluates GPT-3.5/Codex/CodeGen2 out-of-the-box and via Platt-scaling post-hoc
  rescaling, never varying the training/fine-tuning paradigm itself. Bridges directly
  to a novelty gap: no prior work (as surfaced in this batch) tests whether RLVR-vs-SFT-induced
  overconfidence specifically manifests in code-generation correctness tasks the way
  Spiess measures it (ECE, Skill Score, bucket collapse).'
---

[2601.13284] Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2601.13284
(cs)
[Submitted on 19 Jan 2026]
Title:
Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning
Authors:
Duygu Nur Yaldiz
,
Evangelia Spiliopoulou
,
Zheng Qi
,
Siddharth Varia
,
Srikanth Doss
,
Nikolaos Pappas
View a PDF of the paper titled Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning, by Duygu Nur Yaldiz and 5 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) are increasingly deployed in decision-making tasks, where not only accuracy but also reliable confidence estimates are essential. Well-calibrated confidence enables downstream systems to decide when to trust a model and when to defer to fallback mechanisms. In this work, we conduct a systematic study of calibration in two widely used fine-tuning paradigms: supervised fine-tuning (SFT) and reinforcement learning with verifiable rewards (RLVR). We show that while RLVR improves task performance, it produces extremely overconfident models, whereas SFT yields substantially better calibration, even under distribution shift, though with smaller performance gains. Through targeted experiments, we diagnose RLVR's failure, showing that decision tokens act as extraction steps of the decision in reasoning traces and do not carry confidence information, which prevents reinforcement learning from surfacing calibrated alternatives. Based on this insight, we propose a calibration-aware reinforcement learning formulation that directly adjusts decision-token probabilities. Our method preserves RLVR's accuracy level while mitigating overconfidence, reducing ECE scores up to 9 points.
Subjects:
Machine Learning (cs.LG)
Cite as:
arXiv:2601.13284
[cs.LG]
(or
arXiv:2601.13284v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2601.13284
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Duygu Nur Yaldiz [
view email
]
[v1]
Mon, 19 Jan 2026 18:31:31 UTC (4,422 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning, by Duygu Nur Yaldiz and 5 other authors
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