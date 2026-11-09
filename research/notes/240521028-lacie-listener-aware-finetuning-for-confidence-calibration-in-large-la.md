---
title: '[2405.21028] LACIE: Listener-Aware Finetuning for Confidence Calibration in
  Large Language Models'
id: 240521028-lacie-listener-aware-finetuning-for-confidence-calibration-in-large-la
tags:
- code-llm-calibration-aaai27-eabf3f
- verbalized-confidence-dpo
- no-code-eval-gap
created: '2026-07-17T18:37:49.922776Z'
updated: '2026-07-17T18:38:49.130451Z'
source: https://arxiv.org/abs/2405.21028
source_domain: arxiv.org
fetched_at: '2026-07-17T18:37:49.922350Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Stengel-Eskin, Hase, Bansal (UNC), LACIE (arXiv:2405.21028, 2024). Casts
  confidence calibration as DPO preference optimization: a two-agent game where a
  simulated listener judges a speaker model''s answer+confidence, generating preference
  pairs used for DPO fine-tuning. Calibrates BOTH explicit confidence markers (numeric
  scores) and implicit ones (authoritative tone, hedging, elaboration) -- broader
  than a single verbalized-confidence token. Fine-tuned Mistral-7B, Llama3-8B, Llama3-70B
  on TriviaQA; in human evaluation, 47% fewer incorrect answers were accepted by listeners
  while correct-answer acceptance stayed the same. Explicitly reports ''a better confidence
  separation between correct and incorrect examples'' -- a discrimination claim, though
  not an AUROC number. Generalizes from TriviaQA training to TruthfulQA. Produces
  emergent abstention behavior (''I don''t know'') on likely-wrong answers. Cited
  by Rewarding Doubt (2503.02623) as the DPO-based baseline it outperforms on AUROC.
  No code-domain evaluation; QA only. Establishes that preference-optimization (not
  just RL reward-shaping) is a viable train-time route to calibrated verbalized confidence.'
---

*Suggested by [[rewarding-doubt-a-reinforcement-learning-approach-to-calibrated-confidence-expre]] — LACIE cited as DPO-based verbalized-confidence baseline*

[2405.21028] LACIE: Listener-Aware Finetuning for Confidence Calibration in Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2405.21028
(cs)
[Submitted on 31 May 2024 (
v1
), last revised 3 Jul 2024 (this version, v2)]
Title:
LACIE: Listener-Aware Finetuning for Confidence Calibration in Large Language Models
Authors:
Elias Stengel-Eskin
,
Peter Hase
,
Mohit Bansal
View a PDF of the paper titled LACIE: Listener-Aware Finetuning for Confidence Calibration in Large Language Models, by Elias Stengel-Eskin and 2 other authors
View PDF
HTML (experimental)
Abstract:
When answering questions, LLMs can convey not only an answer, but a level of confidence about the answer being correct. This includes explicit confidence markers (e.g. giving a numeric score) as well as implicit markers, like an authoritative tone or elaborating with additional knowledge. For LLMs to be trustworthy knowledge sources, the confidence they convey should match their actual expertise; however, most current models tend towards overconfidence. To calibrate both implicit and explicit confidence markers, we introduce a pragmatic, listener-aware finetuning method (LACIE) that models the listener, considering not only whether an answer is right, but whether it will be accepted by a listener. We cast calibration as preference optimization, creating data via a two-agent game, where a speaker model's outputs are judged by a simulated listener. We then finetune three LLMs (Mistral-7B, Llama3-8B, Llama3-70B) with LACIE, and show that the resulting models are better calibrated w.r.t. a simulated listener. Crucially, these trends transfer to human listeners, helping them correctly predict model correctness: we conduct a human evaluation where annotators accept or reject an LLM's answers, finding that training with LACIE results in 47% fewer incorrect answers being accepted while maintaining the same level of acceptance for correct answers. Furthermore, LACIE generalizes to another dataset, resulting in a large increase in truthfulness on TruthfulQA when trained on TriviaQA. Our analysis indicates that LACIE leads to a better confidence separation between correct and incorrect examples. Qualitatively, we find that a LACIE-trained model hedges more and implicitly signals certainty when it is correct by using an authoritative tone or including details. Finally, LACIE finetuning leads to an emergent increase in model abstention (e.g. saying "I don't know") for answers that are likely wrong.
Comments:
18 pages. Code:
this https URL
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2405.21028
[cs.CL]
(or
arXiv:2405.21028v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2405.21028
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Elias Stengel-Eskin [
view email
]
[v1]
Fri, 31 May 2024 17:16:38 UTC (650 KB)
[v2]
Wed, 3 Jul 2024 12:49:23 UTC (535 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled LACIE: Listener-Aware Finetuning for Confidence Calibration in Large Language Models, by Elias Stengel-Eskin and 2 other authors
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
2024-05
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