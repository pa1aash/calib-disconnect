---
title: '[2312.06681] Steering Llama 2 via Contrastive Activation Addition'
id: 231206681-steering-llama-2-via-contrastive-activation-addition
tags:
- code-llm-calibration-aaai27-eabf3f
- mechanistic-interpretability
- activation-steering
created: '2026-07-17T18:33:54.934571Z'
updated: '2026-07-17T18:35:02.019860Z'
source: https://arxiv.org/abs/2312.06681
source_domain: arxiv.org
fetched_at: '2026-07-17T18:33:54.934046Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Panickssery, Gabrieli, Schulz, Tong, Hubinger & Turner (2023/ACL 2024) introduce
  Contrastive Activation Addition (CAA): steering vectors computed as the mean difference
  in residual-stream activations between paired positive/negative behavioral examples
  (e.g., factual vs. hallucinatory), added at all post-prompt token positions during
  inference with a tunable coefficient. Evaluated on Llama 2 Chat across multiple-choice
  behavioral datasets and open-ended generation, CAA reliably alters targeted behaviors,
  works on top of finetuning/system-prompt baselines, and minimally degrades general
  capability. This is the base methodology that the confidence-faithfulness-gap paper
  (2603.25052) adapts into a two-stage steering pipeline to align verbalized confidence
  with a model''s internal accuracy estimate. Relevance to the adversarial lens: activation
  steering is an intervention on the model''s INTERNAL representation, not the elicitation
  protocol or evaluation metric -- it does not resolve or bear on whether ECE/AUROC
  computed at the benchmark level are themselves fragile, protocol-sensitive, or contamination-confounded;
  it is a distinct axis (representational fix) from the measurement-validity concerns
  raised by the other sources in this batch.'
---

*Suggested by [[260325052-closing-the-confidence-faithfulness-gap-in-large-language-models]] — CAA steering methodology used to fix the orthogonal confidence-calibration directions*

[2312.06681] Steering Llama 2 via Contrastive Activation Addition
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2312.06681
(cs)
[Submitted on 9 Dec 2023 (
v1
), last revised 5 Jul 2024 (this version, v4)]
Title:
Steering Llama 2 via Contrastive Activation Addition
Authors:
Nina Panickssery
,
Nick Gabrieli
,
Julian Schulz
,
Meg Tong
,
Evan Hubinger
,
Alexander Matt Turner
View a PDF of the paper titled Steering Llama 2 via Contrastive Activation Addition, by Nina Panickssery and 5 other authors
View PDF
HTML (experimental)
Abstract:
We introduce Contrastive Activation Addition (CAA), an innovative method for steering language models by modifying their activations during forward passes. CAA computes "steering vectors" by averaging the difference in residual stream activations between pairs of positive and negative examples of a particular behavior, such as factual versus hallucinatory responses. During inference, these steering vectors are added at all token positions after the user's prompt with either a positive or negative coefficient, allowing precise control over the degree of the targeted behavior. We evaluate CAA's effectiveness on Llama 2 Chat using multiple-choice behavioral question datasets and open-ended generation tasks. We demonstrate that CAA significantly alters model behavior, is effective over and on top of traditional methods like finetuning and system prompt design, and minimally reduces capabilities. Moreover, we gain deeper insights into CAA's mechanisms by employing various activation space interpretation methods. CAA accurately steers model outputs and sheds light on how high-level concepts are represented in Large Language Models (LLMs).
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2312.06681
[cs.CL]
(or
arXiv:2312.06681v4
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2312.06681
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Nina Panickssery [
view email
]
[v1]
Sat, 9 Dec 2023 04:40:46 UTC (9,269 KB)
[v2]
Wed, 27 Dec 2023 05:02:35 UTC (8,671 KB)
[v3]
Thu, 7 Mar 2024 02:06:00 UTC (10,693 KB)
[v4]
Fri, 5 Jul 2024 15:30:45 UTC (10,738 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Steering Llama 2 via Contrastive Activation Addition, by Nina Panickssery and 5 other authors
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
2023-12
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