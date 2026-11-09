---
title: '[2504.09246] Type-Constrained Code Generation with Language Models'
id: 250409246-type-constrained-code-generation-with-language-models
tags:
- code-llm-requirement-pivots-5d35f5
- constrained-decoding
- code-generation
created: '2026-07-20T06:54:09.630247Z'
updated: '2026-07-20T06:55:49.650035Z'
source: https://arxiv.org/abs/2504.09246
source_domain: arxiv.org
fetched_at: '2026-07-20T06:54:09.629936Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Mündler, He, Wang, Sen, Song, Vechev (ACM PACMPL/OOPSLA 2025): introduces
  type-constrained decoding -- novel prefix automata plus a search over inhabitable
  types -- to enforce well-typedness during token-by-token LLM code generation, extending
  constrained decoding beyond syntax/DSLs to general-purpose-language type systems
  (formalized on a simply-typed calculus, extended to TypeScript). On HumanEval/MBPP,
  reduces compilation errors by more than half and significantly increases functional
  correctness in synthesis, translation, and repair tasks across model sizes up to
  30B+. This is the closest existing work to ''requirement-aware decoding'' for candidate
  (a), but the constraint enforced is a STATIC, universal property (type well-formedness)
  checkable via a formal grammar/automaton at every token -- not a dynamic, per-instance,
  confidence-weighted steering toward specific NATURAL-LANGUAGE-SPECIFIED behavioral
  requirements (e.g., unit-test-level semantics) that cannot be captured by a type
  system or automaton. Confirms constrained decoding for code is scooped for syntax/type
  correctness but wide open for semantic, requirement-level, confidence-triggered
  steering.'
---

[2504.09246] Type-Constrained Code Generation with Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2504.09246
(cs)
[Submitted on 12 Apr 2025 (
v1
), last revised 8 May 2025 (this version, v2)]
Title:
Type-Constrained Code Generation with Language Models
Authors:
Niels Mündler
,
Jingxuan He
,
Hao Wang
,
Koushik Sen
,
Dawn Song
,
Martin Vechev
View a PDF of the paper titled Type-Constrained Code Generation with Language Models, by Niels M\"undler and Jingxuan He and Hao Wang and Koushik Sen and Dawn Song and Martin Vechev
View PDF
Abstract:
Large language models (LLMs) have achieved notable success in code generation. However, they still frequently produce uncompilable output because their next-token inference procedure does not model formal aspects of code. Although constrained decoding is a promising approach to alleviate this issue, it has only been applied to handle either domain-specific languages or syntactic features of general-purpose programming languages. However, LLMs frequently generate code with typing errors, which are beyond the domain of syntax and generally hard to adequately constrain. To address this challenge, we introduce a type-constrained decoding approach that leverages type systems to guide code generation. For this purpose, we develop novel prefix automata and a search over inhabitable types, forming a sound approach to enforce well-typedness on LLM-generated code. We formalize our approach on a foundational simply-typed language and extend it to TypeScript to demonstrate practicality. Our evaluation on the HumanEval and MBPP datasets shows that our approach reduces compilation errors by more than half and significantly increases functional correctness in code synthesis, translation, and repair tasks across LLMs of various sizes and model families, including state-of-the-art open-weight models with more than 30B parameters. The results demonstrate the generality and effectiveness of our approach in constraining LLM code generation with formal rules of type systems.
Subjects:
Machine Learning (cs.LG)
; Programming Languages (cs.PL)
Cite as:
arXiv:2504.09246
[cs.LG]
(or
arXiv:2504.09246v2
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2504.09246
Focus to learn more
arXiv-issued DOI via DataCite
Related DOI
:
https://doi.org/10.1145/3729274
Focus to learn more
DOI(s) linking to related resources
Submission history
From: Niels Mündler [
view email
]
[v1]
Sat, 12 Apr 2025 15:03:00 UTC (2,798 KB)
[v2]
Thu, 8 May 2025 09:33:40 UTC (2,667 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Type-Constrained Code Generation with Language Models, by Niels M\"undler and Jingxuan He and Hao Wang and Koushik Sen and Dawn Song and Martin Vechev
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
2025-04
Change to browse by:
cs
cs.PL
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