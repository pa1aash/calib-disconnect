---
title: '[2605.24079] TRACER: A Semantic-Aware Framework for Fine-Grained Contamination
  Detection in Code LLMs'
id: 260524079-tracer-a-semantic-aware-framework-for-fine-grained-contamination-detec
tags:
- code-llm-calibration-aaai27-eabf3f
- benchmark-contamination
- code-llm-evaluation
created: '2026-07-17T18:33:49.397858Z'
updated: '2026-07-17T18:34:55.622682Z'
source: https://arxiv.org/abs/2605.24079
source_domain: arxiv.org
fetched_at: '2026-07-17T18:33:49.397425Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Di, Huang & Zhang (submitted May 2026) present TRACER, a semantic-aware
  fine-grained contamination-detection framework for code LLMs that goes beyond exact-match/surface
  deduplication, modeling contamination at three levels: Functionally Identical, Nearly
  Identical, and Shared Logic, via a coarse-to-fine detection pipeline. Introduces
  the first fine-grained code-contamination benchmark spanning 3 widely used code
  benchmarks and 3 representative post-training datasets. TRACER reaches F1=0.91 (fine-grained)
  and F1=0.92 (binary) with GPT-5 as backbone, outperforming existing contamination-detection
  baselines by 42-217%. Relevance to the disconnect paper: prior contamination work
  (e.g., Riddell et al. 2024) only catches surface/near-exact duplication, but TRACER''s
  ''Shared Logic'' category shows models can be contaminated even when solutions are
  semantically but not textually identical -- meaning surface-level decontamination
  checks (common in code-LLM calibration papers) are likely insufficient, and a robust
  AAAI-27 methodology should apply semantic-level contamination screening, not just
  string-matching, before trusting a 0.987 AUROC as a genuine discrimination signal
  rather than a memorization artifact.'
---

*Suggested by [[250706489-on-the-robustness-of-verbal-confidence-of-llms-in-adversarial-attacks]] — recent fine-grained contamination detection framework specific to code LLMs*

[2605.24079] TRACER: A Semantic-Aware Framework for Fine-Grained Contamination Detection in Code LLMs
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2605.24079
(cs)
[Submitted on 22 May 2026]
Title:
TRACER: A Semantic-Aware Framework for Fine-Grained Contamination Detection in Code LLMs
Authors:
Yifeng Di
,
Xuliang Huang
,
Tianyi Zhang
View a PDF of the paper titled TRACER: A Semantic-Aware Framework for Fine-Grained Contamination Detection in Code LLMs, by Yifeng Di and 2 other authors
View PDF
HTML (experimental)
Abstract:
Data contamination is a known threat to the reliability of model evaluation. However, it remains underexplored in code large language models (LLMs), where contamination often goes beyond exact duplication. We present TRACER, a semantic-aware framework for fine-grained code contamination detection. TRACER models contamination using three levels of semantic overlap - Functionally Identical, Nearly Identical, and Shared Logic - and detects them through a coarse-to-fine pipeline. We also introduce the first benchmark for fine-grained code contamination detection, spanning three widely used benchmarks and three representative post-training datasets. TRACER achieves strong and consistent performance across multiple LLM backbones, with GPT-5 reaching an F1 score of 0.91 in fine-grained detection. In the binary setting, TRACER attains an F1 of 0.92, outperforming existing methods by 42%-217%. We further conduct ablation studies and error analysis to assess the contributions of individual components in TRACER.
Comments:
21 pages, 2 figures, 15 tables
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2605.24079
[cs.SE]
(or
arXiv:2605.24079v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2605.24079
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Yifeng Di [
view email
]
[v1]
Fri, 22 May 2026 17:30:20 UTC (1,893 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled TRACER: A Semantic-Aware Framework for Fine-Grained Contamination Detection in Code LLMs, by Yifeng Di and 2 other authors
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
2026-05
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