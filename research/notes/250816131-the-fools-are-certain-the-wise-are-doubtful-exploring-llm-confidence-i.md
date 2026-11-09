---
title: '[2508.16131] The Fools are Certain; the Wise are Doubtful: Exploring LLM Confidence
  in Code Completion'
id: 250816131-the-fools-are-certain-the-wise-are-doubtful-exploring-llm-confidence-i
tags:
- aaai-bar-eval-dprc-d78e07
created: '2026-07-19T20:04:49.114378Z'
updated: '2026-07-19T20:05:09.303770Z'
source: https://arxiv.org/abs/2508.16131
source_domain: arxiv.org
fetched_at: '2026-07-19T20:04:49.114051Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Abstract-only stub; superseded by full-text note the-fools-are-certain-the-wise-are-doubtful-exploring-llm-confidence-in-code-com
---

[2508.16131] The Fools are Certain; the Wise are Doubtful: Exploring LLM Confidence in Code Completion
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2508.16131
(cs)
[Submitted on 22 Aug 2025 (
v1
), last revised 28 Apr 2026 (this version, v2)]
Title:
The Fools are Certain; the Wise are Doubtful: Exploring LLM Confidence in Code Completion
Authors:
Zoe Kotti
,
Konstantina Dritsa
,
Diomidis Spinellis
,
Panos Louridas
View a PDF of the paper titled The Fools are Certain; the Wise are Doubtful: Exploring LLM Confidence in Code Completion, by Zoe Kotti and Konstantina Dritsa and Diomidis Spinellis and Panos Louridas
View PDF
HTML (experimental)
Abstract:
Code completion entails the task of providing missing tokens given a surrounding context. It can boost developer productivity while providing a powerful code discovery tool. Following the Large Language Model (LLM) wave, code completion has been approached with diverse LLMs fine-tuned on code (code LLMs). The performance of code LLMs can be assessed with downstream and intrinsic metrics. Downstream metrics are usually employed to evaluate the practical utility of a model, but can be unreliable and require complex calculations and domain-specific knowledge. In contrast, intrinsic metrics such as perplexity, entropy, and mutual information, which measure model confidence or uncertainty, are simple, versatile, and universal across LLMs and tasks, and can serve as proxies for functional correctness and hallucination risk in LLM-generated code. Motivated by this, we evaluate the confidence of LLMs when generating code by measuring code perplexity across programming languages, models, and datasets using various LLMs, and a sample of 2254 files from 881 GitHub projects. We find that strongly-typed languages exhibit lower perplexity than dynamically typed languages. Scripting languages also demonstrate higher perplexity. Shell appears universally high in perplexity, whereas Java appears low. Code perplexity depends on the employed LLM; under a fixed model, relative language-level rankings are moderately stable across evaluation corpora. Although code comments often increase perplexity, the language ranking based on perplexity is barely affected by their presence. LLM researchers, developers, and users can employ our findings to assess the benefits and suitability of LLM-based code completion in specific software projects based on how language, model choice, and code characteristics impact model confidence.
Comments:
32 pages, 10 figures, 1 table
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2508.16131
[cs.SE]
(or
arXiv:2508.16131v2
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2508.16131
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Zoe Kotti [
view email
]
[v1]
Fri, 22 Aug 2025 06:51:13 UTC (92 KB)
[v2]
Tue, 28 Apr 2026 19:54:19 UTC (111 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled The Fools are Certain; the Wise are Doubtful: Exploring LLM Confidence in Code Completion, by Zoe Kotti and Konstantina Dritsa and Diomidis Spinellis and Panos Louridas
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
2025-08
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