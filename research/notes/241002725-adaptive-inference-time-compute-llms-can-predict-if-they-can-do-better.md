---
title: '[2410.02725] Adaptive Inference-Time Compute: LLMs Can Predict if They Can
  Do Better, Even Mid-Generation'
id: 241002725-adaptive-inference-time-compute-llms-can-predict-if-they-can-do-better
tags:
- code-llm-requirement-pivots-5d35f5
- adaptive-best-of-n
- test-time-compute
created: '2026-07-20T06:52:52.617317Z'
updated: '2026-07-20T06:55:17.918522Z'
source: https://arxiv.org/abs/2410.02725
source_domain: arxiv.org
fetched_at: '2026-07-20T06:52:52.616985Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Manvi, Singh, Ermon (Stanford, Oct 2024): generative self-evaluation scheme
  where the LLM predicts mid-generation (via a single extra token) the probability
  that restarting will yield a better response, used to adaptively decide whether
  to keep sampling, prune unpromising samples early, or pick the best sample -- without
  an external reward model. On AlpacaEval, Llama-3.1-8B win rate vs GPT-4 rises from
  21% to 34% with 16 samples; 74% of that gain is recovered with only 1.2 samples
  on average via adaptive stopping; 50-75% of samples can be pruned early with minimal
  degradation. This is the closest general (non-code) precedent for ''adaptive best-of-n''
  -- but operates at whole-response granularity (one confidence signal per candidate
  response), not per-requirement/per-unit-test within a single problem. No code-generation
  or per-subtask compute-allocation application shown.'
---

[2410.02725] Adaptive Inference-Time Compute: LLMs Can Predict if They Can Do Better, Even Mid-Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2410.02725
(cs)
[Submitted on 3 Oct 2024]
Title:
Adaptive Inference-Time Compute: LLMs Can Predict if They Can Do Better, Even Mid-Generation
Authors:
Rohin Manvi
,
Anikait Singh
,
Stefano Ermon
View a PDF of the paper titled Adaptive Inference-Time Compute: LLMs Can Predict if They Can Do Better, Even Mid-Generation, by Rohin Manvi and 2 other authors
View PDF
HTML (experimental)
Abstract:
Inference-time computation is a powerful paradigm to enhance the performance of large language models (LLMs), with Best-of-N sampling being a widely used technique. However, this method is computationally expensive, requiring both (1) an external reward model and (2) the generation of multiple samples. In this work, we introduce a new generative self-evaluation scheme designed to adaptively reduce the number of generated samples while maintaining or even improving performance. We use a generative reward model formulation, allowing the LLM to predict mid-generation the probability that restarting the generation will yield a better response. These predictions are obtained without an external reward model and can be used to decide whether or not to generate more samples, prune unpromising samples early on, or to pick the best sample. This capability is very inexpensive as it involves generating a single predefined token. Trained using a dataset constructed with real unfiltered LMSYS user prompts, Llama 3.1 8B's win rate against GPT-4 on AlpacaEval increases from 21% to 34% with 16 samples and math performance on GSM8K improves from 84% to 91%. By sampling only when the LLM determines that it is beneficial to do so and adaptively adjusting temperature annealing, we demonstrate that 74% of the improvement from using 16 samples can be achieved with only 1.2 samples on average. We further demonstrate that 50-75% of samples can be pruned early in generation with minimal degradation in performance. Overall, our methods enable more efficient and scalable compute utilization during inference for LLMs.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2410.02725
[cs.CL]
(or
arXiv:2410.02725v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2410.02725
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Rohin Manvi [
view email
]
[v1]
Thu, 3 Oct 2024 17:47:29 UTC (1,998 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Adaptive Inference-Time Compute: LLMs Can Predict if They Can Do Better, Even Mid-Generation, by Rohin Manvi and 2 other authors
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
2024-10
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