---
title: '[2410.06913] Utilize the Flow before Stepping into the Same River Twice: Certainty
  Represented Knowledge Flow for Refusal-Aware Instruction Tuning'
id: 241006913-utilize-the-flow-before-stepping-into-the-same-river-twice-certainty-r
tags:
- aaai-bar-eval-dprc-d78e07
- calibration
- aaai-accepted-2025
- refusal-aware-tuning
- closest-mechanism-analog
created: '2026-07-19T20:01:41.036421Z'
updated: '2026-07-19T20:04:28.964558Z'
source: https://arxiv.org/abs/2410.06913
source_domain: arxiv.org
fetched_at: '2026-07-19T20:01:41.035982Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'AAAI-25 (Proceedings of the AAAI Conference on Artificial Intelligence,
  vol 39, pp 26157-26165). Zhu, Ma, Wu et al. (Shanghai AI Lab + collaborators) tackle
  over-refusal in Refusal-Aware Instruction Tuning (RAIT): models trained to say ''I
  don''t know'' on unknown questions end up refusing questions they could actually
  answer. Diagnoses TWO root causes -- static conflict (similar samples in feature
  space get inconsistent supervision: some kept as answers, others flipped to IDK)
  and dynamic conflict (a question unanswerable at the start of SFT becomes answerable
  as the model learns during training, but retains stale IDK-label supervision). Proposes
  CRaFT: (1) uses response CERTAINTY (not just correctness) to filter/relabel training
  data, reducing static conflict; (2) ''rehearsal'' training that periodically re-probes
  the model''s own evolving knowledge state during SFT to catch dynamic conflict.
  Evaluated on open-ended QA and multiple-choice QA tasks, multiple LLM backbones.
  This is the closest AAAI-accepted paper structurally to DPRC''s mechanism: it explicitly
  ties CALIBRATED CERTAINTY (not just binary correctness) to a downstream training
  signal, and treats the confidence/certainty channel as something that must be actively
  reconciled against a moving ground truth during fine-tuning -- directly analogous
  to DPRC''s problem of eliciting a self-expressed, trainable confidence signal. Novelty
  type: new method (training procedure) + new diagnostic framing (static/dynamic conflict
  taxonomy), grounded in extensive ablations, not a new benchmark.'
---

[2410.06913] Utilize the Flow before Stepping into the Same River Twice: Certainty Represented Knowledge Flow for Refusal-Aware Instruction Tuning
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2410.06913
(cs)
[Submitted on 9 Oct 2024 (
v1
), last revised 20 Dec 2024 (this version, v3)]
Title:
Utilize the Flow before Stepping into the Same River Twice: Certainty Represented Knowledge Flow for Refusal-Aware Instruction Tuning
Authors:
Runchuan Zhu
,
Zhipeng Ma
,
Jiang Wu
,
Junyuan Gao
,
Jiaqi Wang
,
Dahua Lin
,
Conghui He
View a PDF of the paper titled Utilize the Flow before Stepping into the Same River Twice: Certainty Represented Knowledge Flow for Refusal-Aware Instruction Tuning, by Runchuan Zhu and 6 other authors
View PDF
HTML (experimental)
Abstract:
Refusal-Aware Instruction Tuning (RAIT) enables Large Language Models (LLMs) to refuse to answer unknown questions. By modifying responses of unknown questions in the training data to refusal responses such as "I don't know", RAIT enhances the reliability of LLMs and reduces their hallucination. Generally, RAIT modifies training samples based on the correctness of the initial LLM's response. However, this crude approach can cause LLMs to excessively refuse answering questions they could have correctly answered, the problem we call over-refusal. In this paper, we explore two primary causes of over-refusal: Static conflict occurs when similar samples within the LLM's feature space receive differing supervision signals (original vs. modified "I don't know"). Dynamic conflict arises as the LLM's evolving knowledge during SFT enables it to answer previously unanswerable questions, but the now-answerable training samples still retain the original "I don't know" supervision signals from the initial LLM state, leading to inconsistencies. These conflicts cause the trained LLM to misclassify known questions as unknown, resulting in over-refusal. To address this issue, we introduce Certainty Represented Knowledge Flow for Refusal-Aware Instructions Tuning (CRaFT). CRaFT centers on two main contributions: First, we additionally incorporate response certainty to selectively filter and modify data, reducing static conflicts. Second, we implement preliminary rehearsal training to characterize changes in the LLM's knowledge state, which helps mitigate dynamic conflicts during the fine-tuning process. We conducted extensive experiments on open-ended question answering and multiple-choice question task. Experiment results show that CRaFT can improve LLM's overall performance during the RAIT process. Code and data will be released at
this https URL
.
Comments:
Equal contribution: Runchuan Zhu, Zhipeng Ma, Jiang Wu; Corresponding author: Conghui He
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2410.06913
[cs.CL]
(or
arXiv:2410.06913v3
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2410.06913
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Jiang Wu [
view email
]
[v1]
Wed, 9 Oct 2024 14:12:51 UTC (2,639 KB)
[v2]
Mon, 18 Nov 2024 13:15:41 UTC (2,640 KB)
[v3]
Fri, 20 Dec 2024 09:40:54 UTC (2,251 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Utilize the Flow before Stepping into the Same River Twice: Certainty Represented Knowledge Flow for Refusal-Aware Instruction Tuning, by Runchuan Zhu and 6 other authors
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
2024-10
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