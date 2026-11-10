---
title: '[2603.21172] Entropy Alone is Insufficient for Safe Selective Prediction in
  LLMs'
id: 260321172-entropy-alone-is-insufficient-for-safe-selective-prediction-in-llms
tags:
- code-llm-calibration-aaai27-eabf3f
- selective-generation
- token-level-uncertainty
created: '2026-07-17T18:34:44.317991Z'
updated: '2026-07-17T18:36:08.287548Z'
source: https://arxiv.org/abs/2603.21172
source_domain: arxiv.org
fetched_at: '2026-07-17T18:34:44.317571Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Identifies a model-dependent failure mode of entropy-based uncertainty methods
  for selective prediction (abstention): raw entropy alone leads to unreliable abstention
  behavior that breaks down when the deployment-facing metric is the risk-coverage
  tradeoff at LOW target error rates (the regime that matters for safety-critical
  deployment), not aggregate AUROC/accuracy. Fixes this by combining entropy scores
  with a separate learned ''correctness probe'' signal; across three QA benchmarks
  (TriviaQA, BioASQ, MedicalQA) and four model families, the combined score improves
  both risk-coverage tradeoff and calibration relative to entropy-only baselines.
  Directly reinforces the target paper''s central disconnect finding (single-pass
  token-level uncertainty is not a trustworthy expressed interface) but does so in
  general QA, not code, and its fix is a learned auxiliary probe rather than the repeated-sampling
  signal the target paper shows is near-perfectly calibrated -- leaving open whether
  sampling-based confidence would outperform the entropy+probe combination, especially
  at low-error-rate operating points relevant to IDE deployment.'
---

*Suggested by [[250608980-adadec-a-uncertainty-guided-lookahead-decoding-framework-for-llm-based]] — Directly reinforces the calibration-disconnect thesis: entropy/token-level uncertainty alone is insufficient for safe selective prediction*

[2603.21172] Entropy Alone is Insufficient for Safe Selective Prediction in LLMs
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2603.21172
(cs)
[Submitted on 22 Mar 2026]
Title:
Entropy Alone is Insufficient for Safe Selective Prediction in LLMs
Authors:
Edward Phillips
,
Fredrik K. Gustafsson
,
Sean Wu
,
Anshul Thakur
,
David A. Clifton
View a PDF of the paper titled Entropy Alone is Insufficient for Safe Selective Prediction in LLMs, by Edward Phillips and 4 other authors
View PDF
HTML (experimental)
Abstract:
Selective prediction systems can mitigate harms resulting from language model hallucinations by abstaining from answering in high-risk cases. Uncertainty quantification techniques are often employed to identify such cases, but are rarely evaluated in the context of the wider selective prediction policy and its ability to operate at low target error rates. We identify a model-dependent failure mode of entropy-based uncertainty methods that leads to unreliable abstention behaviour, and address it by combining entropy scores with a correctness probe signal. We find that across three QA benchmarks (TriviaQA, BioASQ, MedicalQA) and four model families, the combined score generally improves both the risk--coverage trade-off and calibration performance relative to entropy-only baselines. Our results highlight the importance of deployment-facing evaluation of uncertainty methods, using metrics that directly reflect whether a system can be trusted to operate at a stated risk level.
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2603.21172
[cs.CL]
(or
arXiv:2603.21172v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2603.21172
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Edward Phillips [
view email
]
[v1]
Sun, 22 Mar 2026 11:27:13 UTC (198 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Entropy Alone is Insufficient for Safe Selective Prediction in LLMs, by Edward Phillips and 4 other authors
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
2026-03
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