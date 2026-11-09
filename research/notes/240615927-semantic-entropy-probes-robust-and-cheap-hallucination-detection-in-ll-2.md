---
title: '[2406.15927] Semantic Entropy Probes: Robust and Cheap Hallucination Detection
  in LLMs'
id: 240615927-semantic-entropy-probes-robust-and-cheap-hallucination-detection-in-ll-2
tags:
- code-llm-calibration-aaai27-eabf3f
created: '2026-07-17T18:36:49.802610Z'
source: https://arxiv.org/abs/2406.15927
source_domain: arxiv.org
fetched_at: '2026-07-17T18:36:49.802146Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
---

*Suggested by [[model-agnostic-correctness-assessment-for-llm-generated-code-via-dynamic-interna]] — directly parallels the KEY QUESTION: cheap single-pass hidden-state probe approximating expensive n-sample semantic entropy*

[2406.15927] Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2406.15927
(cs)
[Submitted on 22 Jun 2024]
Title:
Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs
Authors:
Jannik Kossen
,
Jiatong Han
,
Muhammed Razzak
,
Lisa Schut
,
Shreshth Malik
,
Yarin Gal
View a PDF of the paper titled Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs, by Jannik Kossen and 5 other authors
View PDF
HTML (experimental)
Abstract:
We propose semantic entropy probes (SEPs), a cheap and reliable method for uncertainty quantification in Large Language Models (LLMs). Hallucinations, which are plausible-sounding but factually incorrect and arbitrary model generations, present a major challenge to the practical adoption of LLMs. Recent work by Farquhar et al. (2024) proposes semantic entropy (SE), which can detect hallucinations by estimating uncertainty in the space semantic meaning for a set of model generations. However, the 5-to-10-fold increase in computation cost associated with SE computation hinders practical adoption. To address this, we propose SEPs, which directly approximate SE from the hidden states of a single generation. SEPs are simple to train and do not require sampling multiple model generations at test time, reducing the overhead of semantic uncertainty quantification to almost zero. We show that SEPs retain high performance for hallucination detection and generalize better to out-of-distribution data than previous probing methods that directly predict model accuracy. Our results across models and tasks suggest that model hidden states capture SE, and our ablation studies give further insights into the token positions and model layers for which this is the case.
Comments:
First three authors contributed equally
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2406.15927
[cs.CL]
(or
arXiv:2406.15927v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2406.15927
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Jannik Kossen [
view email
]
[v1]
Sat, 22 Jun 2024 19:46:06 UTC (1,585 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs, by Jannik Kossen and 5 other authors
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
2024-06
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