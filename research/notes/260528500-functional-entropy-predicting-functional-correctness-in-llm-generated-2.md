---
title: '[2605.28500] Functional Entropy: Predicting Functional Correctness in LLM-Generated
  Code with Uncertainty Quantification'
id: 260528500-functional-entropy-predicting-functional-correctness-in-llm-generated-2
tags:
- aaai-bar-eval-dprc-d78e07
created: '2026-07-19T20:02:23.776146Z'
source: https://arxiv.org/abs/2605.28500
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:23.775575Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
---

[2605.28500] Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2605.28500
(cs)
[Submitted on 27 May 2026]
Title:
Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification
Authors:
Dylan Bouchard
,
Mohit Singh Chauhan
,
Zeya Ahmad
,
Ho-Kyeong Ra
View a PDF of the paper titled Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification, by Dylan Bouchard and 3 other authors
View PDF
HTML (experimental)
Abstract:
Large language models have shown impressive capabilities in code generation, yet they often produce functionally incorrect code. Uncertainty quantification (UQ) methods have emerged as a promising approach for detecting hallucinations in natural language generation, but their effectiveness for code generation tasks remains underexplored. We systematically evaluate how UQ techniques transfer to code generation across three programming languages, five LLMs, and over 1,700 problems. We find that some token-probability-based methods generalize effectively without modification, while sampling-based methods relying on natural language inference (NLI) fail because NLI models cannot distinguish functionally different code, causing most responses to collapse into a single semantic cluster. To address this, we introduce functional equivalence methods, a family of code-specific methods that replace NLI-based semantic equivalence with an LLM-based functional equivalence assessment, including functional entropy, a code-specific analog of semantic entropy. Functional equivalence methods achieve top AUROC in 11 out of 15 model-benchmark combinations and the best calibration across most settings, consistently outperforming both NLI-based counterparts and all other methods evaluated.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2605.28500
[cs.CL]
(or
arXiv:2605.28500v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2605.28500
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Dylan Bouchard [
view email
]
[v1]
Wed, 27 May 2026 14:01:30 UTC (506 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification, by Dylan Bouchard and 3 other authors
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
2026-05
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