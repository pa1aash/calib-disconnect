---
title: '[2305.14975] Just Ask for Calibration: Strategies for Eliciting Calibrated
  Confidence Scores from Language Models Fine-Tuned with Human Feedback'
id: 230514975-just-ask-for-calibration-strategies-for-eliciting-calibrated-confidenc
tags:
- code-llm-calibration-aaai27-eabf3f
- verbalized-confidence-elicitation
- prompting-baseline
created: '2026-07-17T18:30:13.089776Z'
updated: '2026-07-17T18:33:00.827321Z'
source: http://arxiv.org/abs/2305.14975
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:13.088977Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Tian et al. (EMNLP 2023) benchmark methods for eliciting calibrated confidence
  from RLHF-tuned LLMs (ChatGPT, GPT-4, Claude) on TriviaQA, SciQ, TruthfulQA. Core
  finding: verbalized confidence (model states a number/word as output tokens) is
  often BETTER calibrated than the model''s own token-level conditional probabilities
  for RLHF models, reducing expected calibration error by a relative ~50% in some
  settings — the opposite of the pretrained-LM case where token probabilities are
  well-calibrated. This is the foundational ''just ask'' elicitation paper (pure prompting,
  no fine-tuning/distillation) establishing that verbalized confidence CAN work for
  closed-source RLHF chat models on short-form QA; it is the prompting baseline that
  most later distillation papers (ConTuner, ORCE, Uncertainty Distillation) benchmark
  against and beat. No code-generation tasks tested; no fine-tuning/distillation method
  proposed — pure elicitation via prompt engineering across multiple strategies (e.g.,
  asking for a probability, asking for a word, self-consistency-based verbal elicitation).'
---

[2305.14975] Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2305.14975
(cs)
[Submitted on 24 May 2023 (
v1
), last revised 24 Oct 2023 (this version, v2)]
Title:
Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
Authors:
Katherine Tian
,
Eric Mitchell
,
Allan Zhou
,
Archit Sharma
,
Rafael Rafailov
,
Huaxiu Yao
,
Chelsea Finn
,
Christopher D. Manning
View a PDF of the paper titled Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback, by Katherine Tian and 7 other authors
View PDF
Abstract:
A trustworthy real-world prediction system should produce well-calibrated confidence scores; that is, its confidence in an answer should be indicative of the likelihood that the answer is correct, enabling deferral to an expert in cases of low-confidence predictions. Recent studies have shown that unsupervised pre-training produces large language models (LMs) whose conditional probabilities are remarkably well-calibrated. However, the most widely-used LMs are fine-tuned with reinforcement learning from human feedback (RLHF-LMs), and some studies have suggested that RLHF-LMs produce conditional probabilities that are very poorly calibrated. In light of this perceived weakness, we conduct a broad evaluation of methods for extracting confidence scores from RLHF-LMs. For RLHF-LMs such as ChatGPT, GPT-4, and Claude, we find that verbalized confidences emitted as output tokens are typically better-calibrated than the model's conditional probabilities on the TriviaQA, SciQ, and TruthfulQA benchmarks, often reducing the expected calibration error by a relative 50%.
Comments:
EMNLP 2023 Camera Ready
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2305.14975
[cs.CL]
(or
arXiv:2305.14975v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2305.14975
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Eric A Mitchell [
view email
]
[v1]
Wed, 24 May 2023 10:12:33 UTC (978 KB)
[v2]
Tue, 24 Oct 2023 04:27:42 UTC (2,398 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback, by Katherine Tian and 7 other authors
View PDF
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
2023-05
Change to browse by:
cs
References & Citations
NASA ADS
Google Scholar
Semantic Scholar
1 blog link
(
what is this?
)
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