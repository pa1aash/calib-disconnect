---
title: '[2607.08046] What LLM Forecasters Know but Don''t Say: Probing Internal Representations
  for Calibration and Faithfulness'
id: 260708046-what-llm-forecasters-know-but-dont-say-probing-internal-representation
tags:
- code-llm-probe-verbalize-gap-3d8995
- faithfulness-gap
- novelty-risk
- utility-template
created: '2026-07-20T06:38:46.282100Z'
updated: '2026-07-20T06:39:43.712035Z'
source: https://arxiv.org/abs/2607.08046
source_domain: arxiv.org
fetched_at: '2026-07-20T06:38:46.281786Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Sarfati, Tiwari, Boppana, Earls, Varadaraj, Ho (arXiv 9 Jul 2026, no venue
  tag yet -- likely a workshop/preprint at time of fetch). HIGHEST novelty-risk comparator
  for the code-probe pivot: trains representation-pooling probes on intermediate activations
  of an LLM forecaster (Eternis-Forecaster 8B on OpenForesight, replicated on GLM-4.7-Flash/GLM-4.5-Air)
  and shows probes achieve substantially better calibration than the model''s own
  verbalized/CoT-derived confidence -- i.e. the exact ''internal knows, verbalization
  fails'' structure the pivot proposes, but for FORECASTING not code. Adds two things
  beyond a bare faithfulness-gap claim: (1) a causal/mechanistic faithfulness test
  via evidence ablation and diversionary injection -- removing an influential prompt
  source changes the forecast while leaving the CoT trace unchanged, and probe activations
  track the true behavioral shift in 84% of cases even when CoT conceals the perturbation''s
  effect (this is a STRONGER faithfulness test than accuracy-of-self-report alone:
  it tests whether verbalized reasoning tracks a KNOWN causal intervention); (2) a
  downstream-UTILITY result: forced-answering shows forecasts are fixed before reasoning
  begins, so routing/triaging questions by the spread of a single pre-reasoning pass
  saves 30-47% of generated tokens with no accuracy loss. This is the template answer
  to ''what utility result clears the bar'': a probe-derived signal that (a) beats
  verbalized confidence at calibration, (b) is causally validated as tracking real
  internal state rather than confounds, and (c) is cashed out into a concrete deployment
  saving (token/cost reduction via triage), not just AUROC restated. Directly informs
  DPRC: doing per-requirement code probing + faithfulness gap alone replicates this
  paper''s core structure in a new domain; without an analogous causal-faithfulness
  test and a cashed deployment result (targeted repair/selective generation), a reviewer
  familiar with this paper would call DPRC incremental.'
---

[2607.08046] What LLM Forecasters Know but Don't Say: Probing Internal Representations for Calibration and Faithfulness
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2607.08046
(cs)
[Submitted on 9 Jul 2026]
Title:
What LLM Forecasters Know but Don't Say: Probing Internal Representations for Calibration and Faithfulness
Authors:
Raphaël Sarfati
,
Pratyush Ranjan Tiwari
,
Siddharth Boppana
,
Christopher J. Earls
,
Srikar Varadaraj
,
Eric Ho
View a PDF of the paper titled What LLM Forecasters Know but Don't Say: Probing Internal Representations for Calibration and Faithfulness, by Rapha\"el Sarfati and 5 other authors
View PDF
Abstract:
Large language models fine-tuned for forecasting can be accurate yet poorly calibrated, and their chain-of-thought (CoT) reasoning may not faithfully reflect the evidence behind a forecast. We ask whether internal representations offer a more direct window into both. Working with Eternis-Forecaster 8B on OpenForesight, we train representation-pooling probes on intermediate activations and find they achieve substantially better calibration; a result that also holds for GLM-4.7-Flash and GLM-4.5-Air. We then assess CoT faithfulness through evidence ablation and diversionary injection: removing an influential source in the prompt often changes the model's forecast while leaving the reasoning trace untouched. The same probes function as lie detectors: their activations track behavioral shifts far better than the reasoning trace does, and they also predict the direction of change in 84% of cases, including when the CoT conceals the perturbation's influence. Finally, forced answering reveals that forecasts are largely fixed before reasoning begins: a single pre-reasoning pass recovers the committed answer and confidence, and routing questions by the spread of this pre-set answer distribution saves 30-47% of generated tokens, with no loss of accuracy. Together, these results establish probing internal representations as a practical tool for calibrating, auditing, and triaging language model forecasters and reasoning models more broadly.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2607.08046
[cs.CL]
(or
arXiv:2607.08046v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2607.08046
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Raphael Sarfati [
view email
]
[v1]
Thu, 9 Jul 2026 01:52:09 UTC (858 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled What LLM Forecasters Know but Don't Say: Probing Internal Representations for Calibration and Faithfulness, by Rapha\"el Sarfati and 5 other authors
View PDF
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
2026-07
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