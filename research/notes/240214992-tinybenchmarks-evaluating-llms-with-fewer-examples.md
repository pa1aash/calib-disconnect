---
title: '[2402.14992] tinyBenchmarks: evaluating LLMs with fewer examples'
id: 240214992-tinybenchmarks-evaluating-llms-with-fewer-examples
tags:
- code-llm-best-aaai-paper-6ded37
- irt-benchmark
- closest-prior-method
created: '2026-07-20T07:42:44.529233Z'
updated: '2026-07-20T07:43:54.862046Z'
source: https://arxiv.org/abs/2402.14992
source_domain: arxiv.org
fetched_at: '2026-07-20T07:42:44.528366Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Maia Polo, Weber, Choshen, Sun, Xu & Yurochkin (ICML 2024). Introduces tinyBenchmarks:
  applies classical/Item-Response-Theory (IRT) psychometric modeling to WHOLE-BENCHMARK-ITEM
  (question-level) correctness matrices across many LLMs (Open LLM Leaderboard, MMLU,
  HELM, AlpacaEval 2.0) to fit per-item difficulty/discrimination parameters and per-model
  ability, then selects a small (~100-item) maximally-informative subset (via IRT
  item-information + anchor-point/clustering strategies) that reproduces full-benchmark
  rankings at a fraction of the evaluation cost. Releases curated tiny benchmarks
  + IRT tooling. Relevance: this is the template technique for ''principled hard/diagnostic
  subset mining'' via a statistical model of item difficulty and discrimination rather
  than heuristic solve-rate thresholds (cf. BigCodeBench-Hard). It operates at whole-QUESTION
  granularity for general (mostly multiple-choice/short-answer) benchmarks; nobody
  has yet applied this IRT machinery at the per-REQUIREMENT (unit-test-within-task)
  granularity for code-generation benchmarks with partial-pass structure -- that gap
  is the open opportunity.'
---

[2402.14992] tinyBenchmarks: evaluating LLMs with fewer examples
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2402.14992
(cs)
[Submitted on 22 Feb 2024 (
v1
), last revised 26 May 2024 (this version, v2)]
Title:
tinyBenchmarks: evaluating LLMs with fewer examples
Authors:
Felipe Maia Polo
,
Lucas Weber
,
Leshem Choshen
,
Yuekai Sun
,
Gongjun Xu
,
Mikhail Yurochkin
View a PDF of the paper titled tinyBenchmarks: evaluating LLMs with fewer examples, by Felipe Maia Polo and 5 other authors
View PDF
HTML (experimental)
Abstract:
The versatility of large language models (LLMs) led to the creation of diverse benchmarks that thoroughly test a variety of language models' abilities. These benchmarks consist of tens of thousands of examples making evaluation of LLMs very expensive. In this paper, we investigate strategies to reduce the number of evaluations needed to assess the performance of an LLM on several key benchmarks. For example, we show that to accurately estimate the performance of an LLM on MMLU, a popular multiple-choice QA benchmark consisting of 14K examples, it is sufficient to evaluate this LLM on 100 curated examples. We release evaluation tools and tiny versions of popular benchmarks: Open LLM Leaderboard, MMLU, HELM, and AlpacaEval 2.0. Our empirical analysis demonstrates that these tools and tiny benchmarks are sufficient to reliably and efficiently reproduce the original evaluation results.
Comments:
Proceedings of the 41st International Conference on Machine Learning (ICML)
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG); Machine Learning (stat.ML)
Cite as:
arXiv:2402.14992
[cs.CL]
(or
arXiv:2402.14992v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2402.14992
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Felipe Maia Polo [
view email
]
[v1]
Thu, 22 Feb 2024 22:05:23 UTC (5,640 KB)
[v2]
Sun, 26 May 2024 22:27:23 UTC (5,468 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled tinyBenchmarks: evaluating LLMs with fewer examples, by Felipe Maia Polo and 5 other authors
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
2024-02
Change to browse by:
cs
cs.AI
cs.LG
stat
stat.ML
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