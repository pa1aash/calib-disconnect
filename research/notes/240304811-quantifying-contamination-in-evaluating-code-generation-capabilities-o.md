---
title: '[2403.04811] Quantifying Contamination in Evaluating Code Generation Capabilities
  of Language Models'
id: 240304811-quantifying-contamination-in-evaluating-code-generation-capabilities-o
tags:
- code-llm-calibration-aaai27-eabf3f
- benchmark-contamination
- code-llm-evaluation
created: '2026-07-17T18:33:43.654773Z'
updated: '2026-07-17T18:34:48.735726Z'
source: https://arxiv.org/abs/2403.04811
source_domain: arxiv.org
fetched_at: '2026-07-17T18:33:43.654331Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Riddell, Ni & Cohan (2024, cs.SE) perform the first comprehensive quantification
  of data contamination in code-generation benchmarks (HumanEval, MBPP, and others),
  measuring surface-level AND semantic-level overlap with open pretraining corpora
  (e.g., RedPajama-Data-1T, StarCoder-Data). Finds substantial overlap between popular
  benchmarks and pretraining data, and shows models perform SIGNIFICANTLY BETTER on
  the subset of benchmark problems with similar solutions seen during training --
  i.e., benchmark accuracy is inflated by memorization, not generalization. Also analyzes
  factors affecting model memorization vs. generalization: model size, problem difficulty,
  and question length all modulate the contamination effect. Releases the full matching
  pipeline for reuse. Directly threatens the disconnect paper''s AUROC 0.987 finding:
  if the code benchmark(s) used for sampling-confidence AUROC evaluation are contaminated,
  near-perfect discrimination between correct/incorrect completions could partly reflect
  the model having memorized which specific problems it ''knows'' rather than a genuine,
  generalizable confidence signal -- a single-benchmark contamination confound that
  a robust AAAI-27 paper must control for via decontaminated or contamination-free
  benchmarks (e.g., LiveCodeBench-style continuously-refreshed problem sets).'
---

*Suggested by [[250706489-on-the-robustness-of-verbal-confidence-of-llms-in-adversarial-attacks]] — benchmark contamination as a distinct threat to code-LLM confidence evaluation validity*

[2403.04811] Quantifying Contamination in Evaluating Code Generation Capabilities of Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2403.04811
(cs)
[Submitted on 6 Mar 2024]
Title:
Quantifying Contamination in Evaluating Code Generation Capabilities of Language Models
Authors:
Martin Riddell
,
Ansong Ni
,
Arman Cohan
View a PDF of the paper titled Quantifying Contamination in Evaluating Code Generation Capabilities of Language Models, by Martin Riddell and 2 other authors
View PDF
HTML (experimental)
Abstract:
While large language models have achieved remarkable performance on various code generation benchmarks, there have been growing concerns regarding potential contamination of these benchmarks as they may be leaked into pretraining and finetuning data. While recent work has investigated contamination in natural language generation and understanding tasks, there has been less extensive research into how data contamination impacts the evaluation of code generation, which is critical for understanding the robustness and reliability of LLMs in programming contexts. In this work, we perform a comprehensive study of data contamination of popular code generation benchmarks, and precisely quantify their overlap with pretraining corpus through both surface-level and semantic-level matching. In our experiments, we show that there are substantial overlap between popular code generation benchmarks and open training corpus, and models perform significantly better on the subset of the benchmarks where similar solutions are seen during training. We also conduct extensive analysis on the factors that affects model memorization and generalization, such as model size, problem difficulty, and question length. We release all resulting files from our matching pipeline for future research.
Subjects:
Software Engineering (cs.SE)
; Computation and Language (cs.CL); Machine Learning (cs.LG)
Cite as:
arXiv:2403.04811
[cs.SE]
(or
arXiv:2403.04811v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2403.04811
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Ansong Ni [
view email
]
[v1]
Wed, 6 Mar 2024 21:45:35 UTC (263 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Quantifying Contamination in Evaluating Code Generation Capabilities of Language Models, by Martin Riddell and 2 other authors
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
2024-03
Change to browse by:
cs
cs.CL
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