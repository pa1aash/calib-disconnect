---
title: '[2502.11620] Assessing Correctness in LLM-Based Code Generation via Uncertainty
  Estimation'
id: 250211620-assessing-correctness-in-llm-based-code-generation-via-uncertainty-est
tags:
- code-llm-calibration-aaai27-eabf3f
created: '2026-07-17T18:37:17.235715Z'
updated: '2026-07-17T18:37:52.571680Z'
source: https://arxiv.org/abs/2502.11620
source_domain: arxiv.org
fetched_at: '2026-07-17T18:37:17.235363Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Abstract-only duplicate; superseded by full-text note assessing-correctness-in-llm-based-code-generation-via-uncertainty-estimation.
---

*Suggested by [[functional-entropy-predicting-functional-correctness-in-llm-generated-code-with]] — cited as symbolic/AST-clustering uncertainty method for code, directly relevant to AST-clustering proxy in disconnect thesis*

[2502.11620] Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2502.11620
(cs)
[Submitted on 17 Feb 2025 (
v1
), last revised 1 Jul 2025 (this version, v3)]
Title:
Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation
Authors:
Arindam Sharma
,
Cristina David
View a PDF of the paper titled Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation, by Arindam Sharma and Cristina David
View PDF
HTML (experimental)
Abstract:
In this work, we explore uncertainty estimation as a proxy for correctness in LLM-generated code. To this end, we adapt two state-of-the-art techniques from natural language generation -- one based on entropy and another on mutual information -- to the domain of code generation. Given the distinct semantic properties of code, we introduce modifications, including a semantic equivalence check based on symbolic execution. Our findings indicate a strong correlation between the uncertainty computed through these techniques and correctness, highlighting the potential of uncertainty estimation for quality assessment. Additionally, we propose a simplified version of the entropy-based method that assumes a uniform distribution over the LLM's responses, demonstrating comparable effectiveness. Using these techniques, we develop an abstention policy that prevents the model from making predictions when uncertainty is high, reducing incorrect outputs to near zero. Our evaluation on the LiveCodeBench shows that our approach significantly outperforms a baseline relying solely on LLM-reported log-probabilities.
Comments:
18 pages and 3 References Pages
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2502.11620
[cs.SE]
(or
arXiv:2502.11620v3
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2502.11620
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Arindam Sharma [
view email
]
[v1]
Mon, 17 Feb 2025 10:03:01 UTC (1,802 KB)
[v2]
Wed, 5 Mar 2025 18:24:41 UTC (2,387 KB)
[v3]
Tue, 1 Jul 2025 12:15:44 UTC (2,510 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation, by Arindam Sharma and Cristina David
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.SE
< prev
|
next >
new
|
recent
|
2025-02
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