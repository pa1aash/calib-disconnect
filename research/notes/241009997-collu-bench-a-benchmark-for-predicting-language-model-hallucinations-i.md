---
title: '[2410.09997] Collu-Bench: A Benchmark for Predicting Language Model Hallucinations
  in Code'
id: 241009997-collu-bench-a-benchmark-for-predicting-language-model-hallucinations-i
tags:
- code-llm-calibration-aaai27-eabf3f
- benchmark-not-method
- distinct
- training-data-source
created: '2026-07-17T19:30:20.283806Z'
updated: '2026-07-17T19:31:00.090204Z'
source: https://arxiv.org/abs/2410.09997
source_domain: arxiv.org
fetched_at: '2026-07-17T19:30:20.283293Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Collu-Bench (Jiang, Li, Tan, Zhang; arXiv:2410.09997, Oct 2024) is the benchmark/dataset
  that FLARE''s diagnostic model is trained on. It contains 13,234 code-hallucination
  instances (buggy code with ground-truth hallucination location) collected from 5
  datasets and 11 diverse LLMs, spanning code generation (CG) and automated program
  repair (APR) tasks. Each instance is annotated with per-step log probabilities,
  token types, and execution feedback as features for localization. The authors''
  own baseline experiments (traditional ML + neural networks) predicting hallucination
  location achieve only 22.03-33.15% accuracy, underscoring that hallucination LOCALIZATION
  is hard even with rich features. OCCUPANCY vs proposed headline: DISTINCT -- this
  is a benchmark/dataset paper providing localization LABELS and features for training
  external diagnostic models (as FLARE does), not a method that elicits the code-generating
  LLM''s own calibrated confidence. It targets a hallucination-location classification
  task, not per-test-case pass/fail prediction, and reports classification accuracy,
  never AUROC or a calibration metric. It is infrastructure/data that a proposed method
  could reuse (e.g., as one training source) but does not itself occupy any part of
  the novelty claim.'
---

*Suggested by [[flare-fine-grained-diagnostic-feedback-for-llm-code-refinement]] — training data source for FLARE's diagnostic model; benchmark predicting LLM hallucinations in code with ground-truth bug locations*

[2410.09997] Collu-Bench: A Benchmark for Predicting Language Model Hallucinations in Code
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2410.09997
(cs)
[Submitted on 13 Oct 2024]
Title:
Collu-Bench: A Benchmark for Predicting Language Model Hallucinations in Code
Authors:
Nan Jiang
,
Qi Li
,
Lin Tan
,
Tianyi Zhang
View a PDF of the paper titled Collu-Bench: A Benchmark for Predicting Language Model Hallucinations in Code, by Nan Jiang and 3 other authors
View PDF
HTML (experimental)
Abstract:
Despite their success, large language models (LLMs) face the critical challenge of hallucinations, generating plausible but incorrect content. While much research has focused on hallucinations in multiple modalities including images and natural language text, less attention has been given to hallucinations in source code, which leads to incorrect and vulnerable code that causes significant financial loss. To pave the way for research in LLMs' hallucinations in code, we introduce Collu-Bench, a benchmark for predicting code hallucinations of LLMs across code generation (CG) and automated program repair (APR) tasks. Collu-Bench includes 13,234 code hallucination instances collected from five datasets and 11 diverse LLMs, ranging from open-source models to commercial ones. To better understand and predict code hallucinations, Collu-Bench provides detailed features such as the per-step log probabilities of LLMs' output, token types, and the execution feedback of LLMs' generated code for in-depth analysis. In addition, we conduct experiments to predict hallucination on Collu-Bench, using both traditional machine learning techniques and neural networks, which achieves 22.03 -- 33.15% accuracy. Our experiments draw insightful findings of code hallucination patterns, reveal the challenge of accurately localizing LLMs' hallucinations, and highlight the need for more sophisticated techniques.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2410.09997
[cs.SE]
(or
arXiv:2410.09997v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2410.09997
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Nan Jiang [
view email
]
[v1]
Sun, 13 Oct 2024 20:41:47 UTC (396 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Collu-Bench: A Benchmark for Predicting Language Model Hallucinations in Code, by Nan Jiang and 3 other authors
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
2024-10
Change to browse by:
cs
cs.AI
cs.CL
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