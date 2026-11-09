---
title: '[2511.11169] Refine and Align: Confidence Calibration through Multi-Agent
  Interaction in VQA'
id: 251111169-refine-and-align-confidence-calibration-through-multi-agent-interactio
tags:
- aaai-bar-eval-dprc-d78e07
- calibration
- aaai-accepted-2026
- multi-agent-vqa
created: '2026-07-19T20:02:03.963178Z'
updated: '2026-07-19T20:04:56.411446Z'
source: https://arxiv.org/abs/2511.11169
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:03.962852Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'AAAI 2026, accepted to the Special Track on AI Alignment (17 pages, 6 figures,
  5 tables). Pandey, Bardhan, Jain, Hebbalaguppe, Dhanakshirur, Vig (TCS Research)
  propose AlignVQA: a debate-based multi-agent framework for VQA calibration where
  diverse specialized VLMs (each using a distinct prompting strategy -- CoT, self-ask,
  search-style) generate candidate answers, then generalist agents critique/refine/aggregate
  them in a two-stage debate. Introduces AlignCal, a differentiable calibration-aware
  loss that fine-tunes specialized agents by minimizing an upper bound on calibration
  error. Scope: multiple benchmark VQA datasets, ablations on debate structure and
  agent specialization. Novelty type: new method (multi-agent debate + a new calibration
  loss/objective) with both an architectural and a training-objective contribution
  -- notable because it pairs a NEW LOSS FUNCTION (not just post-hoc scaling or prompting)
  with an architecture, which is a stronger novelty bar than pure prompting-based
  calibration papers. Relevant to DPRC as an example of what ''a new loss/training-objective
  contribution'' looks like as an AAAI-accepted novelty type, and as a domain (VQA,
  not code) confirming multi-benchmark VQA calibration papers get in without needing
  a brand-new benchmark.'
---

[2511.11169] Refine and Align: Confidence Calibration through Multi-Agent Interaction in VQA
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computer Vision and Pattern Recognition
arXiv:2511.11169
(cs)
[Submitted on 14 Nov 2025]
Title:
Refine and Align: Confidence Calibration through Multi-Agent Interaction in VQA
Authors:
Ayush Pandey
,
Jai Bardhan
,
Ishita Jain
,
Ramya S Hebbalaguppe
,
Rohan Raju Dhanakshirur
,
Lovekesh Vig
View a PDF of the paper titled Refine and Align: Confidence Calibration through Multi-Agent Interaction in VQA, by Ayush Pandey and 5 other authors
View PDF
HTML (experimental)
Abstract:
In the context of Visual Question Answering (VQA) and Agentic AI, calibration refers to how closely an AI system's confidence in its answers reflects their actual correctness. This aspect becomes especially important when such systems operate autonomously and must make decisions under visual uncertainty. While modern VQA systems, powered by advanced vision-language models (VLMs), are increasingly used in high-stakes domains like medical diagnostics and autonomous navigation due to their improved accuracy, the reliability of their confidence estimates remains under-examined. Particularly, these systems often produce overconfident responses. To address this, we introduce AlignVQA, a debate-based multi-agent framework, in which diverse specialized VLM -- each following distinct prompting strategies -- generate candidate answers and then engage in two-stage interaction: generalist agents critique, refine and aggregate these proposals. This debate process yields confidence estimates that more accurately reflect the model's true predictive performance. We find that more calibrated specialized agents produce better aligned confidences. Furthermore, we introduce a novel differentiable calibration-aware loss function called aligncal designed to fine-tune the specialized agents by minimizing an upper bound on the calibration error. This objective explicitly improves the fidelity of each agent's confidence estimates. Empirical results across multiple benchmark VQA datasets substantiate the efficacy of our approach, demonstrating substantial reductions in calibration discrepancies. Furthermore, we propose a novel differentiable calibration-aware loss to fine-tune the specialized agents and improve the quality of their individual confidence estimates based on minimising upper bound calibration error.
Comments:
17 pages, 6 figures, 5 tables. Accepted to Special Track on AI Alignment, AAAI 2026. Project Page-
this https URL
Subjects:
Computer Vision and Pattern Recognition (cs.CV)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2511.11169
[cs.CV]
(or
arXiv:2511.11169v1
[cs.CV]
for this version)
https://doi.org/10.48550/arXiv.2511.11169
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Ayush Pandey [
view email
]
[v1]
Fri, 14 Nov 2025 11:08:21 UTC (383 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Refine and Align: Confidence Calibration through Multi-Agent Interaction in VQA, by Ayush Pandey and 5 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.CV
< prev
|
next >
new
|
recent
|
2025-11
Change to browse by:
cs
cs.AI
cs.LG
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