---
title: '[2302.08703] PAC Prediction Sets for Large Language Models of Code'
id: 230208703-pac-prediction-sets-for-large-language-models-of-code
tags:
- code-llm-best-aaai-paper-6ded37
- conformal-prediction
- pac-prediction-sets
- foundational
- program-level-granularity
created: '2026-07-20T07:42:18.998592Z'
updated: '2026-07-20T07:45:58.796079Z'
source: https://arxiv.org/abs/2302.08703
source_domain: arxiv.org
fetched_at: '2026-07-20T07:42:18.998248Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'PAC Prediction Sets for Large Language Models of Code (Khakhar, Mell, Bastani;
  arXiv:2302.08703, ICML 2023) -- foundational paper for distribution-free/PAC prediction
  sets in code generation, direct ancestor RisCoSet explicitly critiques. Represents
  a compact prediction set as a PARTIAL PROGRAM: an AST with uncertain nodes/subtrees
  replaced by holes, sized via optimization so that, with PAC guarantee, the correct
  completion is containable within the partial program with high probability. Evaluated
  on PICARD (T5 SQL semantic parsing) and Codex. First PAC-prediction-set paper for
  generative code models. Program/AST-level granularity (which nodes to leave uncertain),
  NOT unit-test/requirement granularity -- no notion of ''this specific requirement
  is satisfied,'' only ''this subtree is uncertain.'' Imposes a monotonicity constraint
  on the risk function (flagged by RisCoSet as a source of suboptimal partial programs)
  and treats code generation as single-label, ignoring semantically-equivalent multi-label
  completions.'
---

*Suggested by [[260512201-uncertainty-quantification-for-llm-based-code-generation]] — the existing PAC prediction sets attempt that RisCoSet explicitly critiques and improves on*

[2302.08703] PAC Prediction Sets for Large Language Models of Code
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2302.08703
(cs)
[Submitted on 17 Feb 2023 (
v1
), last revised 21 Jun 2023 (this version, v2)]
Title:
PAC Prediction Sets for Large Language Models of Code
Authors:
Adam Khakhar
,
Stephen Mell
,
Osbert Bastani
View a PDF of the paper titled PAC Prediction Sets for Large Language Models of Code, by Adam Khakhar and 2 other authors
View PDF
Abstract:
Prediction sets have recently been shown to be a promising strategy for quantifying the uncertainty of deep neural networks in a way that provides theoretical guarantees. However, existing techniques have largely targeted settings where the space of labels is simple, so prediction sets can be arbitrary subsets of labels. For structured prediction problems where the space of labels is exponential in size, even prediction sets containing a small fraction of all labels can be exponentially large. In the context of code generation, we propose a solution that considers a restricted set of prediction sets that can compactly be represented as partial programs, which are programs with portions replaced with holes. Given a trained code generation model, our algorithm leverages a programming language's abstract syntax tree to generate a set of programs such that the correct program is in the set with high-confidence. Valuable applications of our algorithm include a Codex-style code generator with holes in uncertain parts of the generated code, which provides a partial program with theoretical guarantees. We evaluate our approach on PICARD (a T5 model for SQL semantic parsing) and Codex (a GPT model for over a dozen programming languages, including Python), demonstrating that our approach generates compact PAC prediction sets. This is the first research contribution that generates PAC prediction sets for generative code models.
Comments:
Proceedings of the 40th International Conference on Machine Learning
Subjects:
Machine Learning (cs.LG)
Cite as:
arXiv:2302.08703
[cs.LG]
(or
arXiv:2302.08703v2
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2302.08703
Focus to learn more
arXiv-issued DOI via DataCite
Journal reference:
PMLR 202, 2023
Submission history
From: Adam Khakhar [
view email
]
[v1]
Fri, 17 Feb 2023 05:32:24 UTC (1,346 KB)
[v2]
Wed, 21 Jun 2023 02:35:39 UTC (1,452 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled PAC Prediction Sets for Large Language Models of Code, by Adam Khakhar and 2 other authors
View PDF
TeX Source
view license
Current browse context:
cs.LG
< prev
|
next >
new
|
recent
|
2023-02
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
IArxiv recommender toggle
IArxiv Recommender
(
What is IArxiv?
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