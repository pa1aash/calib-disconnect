---
title: '[2504.05419] Reasoning Models Know When They''re Right: Probing Hidden States
  for Self-Verification'
id: 250405419-reasoning-models-know-when-theyre-right-probing-hidden-states-for-self
tags:
- code-llm-probe-verbalize-gap-3d8995
- latent-knowledge
- reasoning-probe
- exploitation-gap
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-20T06:38:15.842356Z'
updated: '2026-11-09T23:26:01.253087Z'
source: https://arxiv.org/abs/2504.05419
source_domain: arxiv.org
fetched_at: '2026-07-20T06:38:15.842026Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Zhang, Chen, Pan, Zhao, Panda, Li, He (NYU, arXiv Apr 2025). Probes hidden
  states of REASONING models (math/logical reasoning chains) to verify correctness
  of intermediate answers mid-chain-of-thought. The probe verifies intermediate-answer
  correctness with high accuracy and produces well-calibrated scores; hidden states
  also encode correctness of FUTURE (not-yet-produced) answers, enabling early prediction
  before the answer is fully formulated. Authors use the probe as an inference-time
  verifier to decide when to exit reasoning early, cutting inference tokens 24% with
  no performance loss. Domain: math/logical reasoning benchmarks (not code generation).
  Granularity: per-intermediate-answer within a reasoning chain (closer to a step-level/per-claim
  granularity than pure whole-final-answer, but still not per-requirement/per-unit-test
  on a generated program). Central framing line directly relevant to our lane: ''these
  findings confirm that reasoning models do encode a notion of correctness yet fail
  to exploit it'' -- but this is an EXPLOITATION gap (the pipeline doesn''t use the
  internal signal operationally), not explicitly a VERBALIZATION/self-report gap --
  the paper does not train or compare the model''s own stated/verbalized confidence
  against the probe. No code-generation task, no unit-test-based requirement decomposition,
  no comparison to trained self-reported confidence.'
---

*Suggested by [[260614530-code-correctness-is-linearly-decodable-from-llm-hidden-states-before-g]] — hidden-state self-verification probe vs verbalized confidence gap, found via web search*

[2504.05419] Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2504.05419
(cs)
[Submitted on 7 Apr 2025]
Title:
Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification
Authors:
Anqi Zhang
,
Yulin Chen
,
Jane Pan
,
Chen Zhao
,
Aurojit Panda
,
Jinyang Li
,
He He
View a PDF of the paper titled Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification, by Anqi Zhang and 6 other authors
View PDF
HTML (experimental)
Abstract:
Reasoning models have achieved remarkable performance on tasks like math and logical reasoning thanks to their ability to search during reasoning. However, they still suffer from overthinking, often performing unnecessary reasoning steps even after reaching the correct answer. This raises the question: can models evaluate the correctness of their intermediate answers during reasoning? In this work, we study whether reasoning models encode information about answer correctness through probing the model's hidden states. The resulting probe can verify intermediate answers with high accuracy and produces highly calibrated scores. Additionally, we find models' hidden states encode correctness of future answers, enabling early prediction of the correctness before the intermediate answer is fully formulated. We then use the probe as a verifier to decide whether to exit reasoning at intermediate answers during inference, reducing the number of inference tokens by 24\% without compromising performance. These findings confirm that reasoning models do encode a notion of correctness yet fail to exploit it, revealing substantial untapped potential to enhance their efficiency.
Subjects:
Artificial Intelligence (cs.AI)
; Computation and Language (cs.CL)
Cite as:
arXiv:2504.05419
[cs.AI]
(or
arXiv:2504.05419v1
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2504.05419
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Anqi Zhang [
view email
]
[v1]
Mon, 7 Apr 2025 18:42:01 UTC (442 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification, by Anqi Zhang and 6 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.AI
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