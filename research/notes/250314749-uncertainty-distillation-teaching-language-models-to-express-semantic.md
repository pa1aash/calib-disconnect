---
title: '[2503.14749] Uncertainty Distillation: Teaching Language Models to Express
  Semantic Confidence'
id: 250314749-uncertainty-distillation-teaching-language-models-to-express-semantic
tags:
- code-llm-calibration-aaai27-eabf3f
created: '2026-07-17T18:30:18.267217Z'
updated: '2026-07-17T18:33:02.038586Z'
source: http://arxiv.org/abs/2503.14749
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:18.266699Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
---

[2503.14749] Uncertainty Distillation: Teaching Language Models to Express Semantic Confidence
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2503.14749
(cs)
[Submitted on 18 Mar 2025 (
v1
), last revised 12 Dec 2025 (this version, v3)]
Title:
Uncertainty Distillation: Teaching Language Models to Express Semantic Confidence
Authors:
Sophia Hager
,
David Mueller
,
Kevin Duh
,
Nicholas Andrews
View a PDF of the paper titled Uncertainty Distillation: Teaching Language Models to Express Semantic Confidence, by Sophia Hager and 3 other authors
View PDF
HTML (experimental)
Abstract:
As large language models (LLMs) are increasingly used for factual question-answering, it becomes more important for LLMs to have the capability to communicate the likelihood that their answer is correct. For these verbalized expressions of uncertainty to be meaningful, they should reflect the error rates at the expressed level of confidence. However, when prompted to express confidence, the error rates of current LLMs are inconsistent with their communicated confidences, highlighting the need for uncertainty quantification methods. Many prior methods calculate lexical uncertainty, estimating a model's confidence in the specific string it generated. In some cases, however, it may be more useful to estimate semantic uncertainty, or the model's confidence in the answer regardless of how it is verbalized. We propose a simple procedure, uncertainty distillation, to teach an LLM to verbalize calibrated semantic confidences. Using held-out data to map initial uncertainty estimates to meaningful probabilities, we create examples annotated with verbalized probabilities for supervised fine-tuning. We find that our method yields verbalized confidences that correlate well with observed error rates, even when compared to strong baselines, some of which are more than twenty times slower at inference time. Additionally, we demonstrate that our method can be applied to black-box models that allow API-based fine-tuning, resulting in estimates of uncertainty that are both more effective and more efficient than any of our baselines.
Subjects:
Computation and Language (cs.CL)
; Machine Learning (cs.LG)
Cite as:
arXiv:2503.14749
[cs.CL]
(or
arXiv:2503.14749v3
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2503.14749
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Sophia Hager [
view email
]
[v1]
Tue, 18 Mar 2025 21:29:29 UTC (524 KB)
[v2]
Thu, 22 May 2025 02:52:11 UTC (1,416 KB)
[v3]
Fri, 12 Dec 2025 16:31:27 UTC (717 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Uncertainty Distillation: Teaching Language Models to Express Semantic Confidence, by Sophia Hager and 3 other authors
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