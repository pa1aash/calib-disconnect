---
title: '[2605.27752] Asking Is Not Enough: Protocol Sensitivity in LLM Confidence
  Calibration'
id: 260527752-asking-is-not-enough-protocol-sensitivity-in-llm-confidence-calibratio
tags:
- code-llm-calibration-aaai27-eabf3f
- protocol-sensitivity
- ece-fragility
created: '2026-07-17T18:30:39.887795Z'
updated: '2026-07-17T18:31:33.484810Z'
source: http://arxiv.org/abs/2605.27752
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:39.886948Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Kim & Kang (2026) show that the standard token-probability-vs-verbalized-confidence
  comparison used to claim calibration gaps is itself an artifact of unstated measurement
  choices. Holding verbalized-confidence elicitation fixed, they vary three axes of
  the token-probability side: which answer string is scored, how the token-probability
  readout is computed, and the conditioning context under which it is measured. Across
  4 QA benchmarks and 3 open 7-8B model families (with larger Qwen2.5 as robustness
  check), conditioning context alone flips the SIGN or magnitude of the ECE gap between
  token and verbal confidence; token readout choice produces smaller but still sign-moving
  changes; ECE estimator choice has little effect. Under the default generated-answer/bare-context
  protocol, Instruct models show near-parity between signals rather than the large
  verbalized-confidence deficit often reported. A separate supplied-answer analysis
  finds surface-plausible WRONG answers get nearly the same verbalized confidence
  as gold answers -- confidence tracks answer plausibility/provenance, not correctness.
  Proposes a reporting checklist (elicitation provenance, scored answer, token-probability
  readout, conditioning context) as a methodological control. Directly threatens any
  single-protocol AUROC/ECE comparison as potentially non-robust to measurement choice.'
---

[2605.27752] Asking Is Not Enough: Protocol Sensitivity in LLM Confidence Calibration
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2605.27752
(cs)
[Submitted on 26 May 2026 (
v1
), last revised 1 Jun 2026 (this version, v2)]
Title:
Asking Is Not Enough: Protocol Sensitivity in LLM Confidence Calibration
Authors:
Hankyeol Kim
,
Pilsung Kang
View a PDF of the paper titled Asking Is Not Enough: Protocol Sensitivity in LLM Confidence Calibration, by Hankyeol Kim and Pilsung Kang
View PDF
HTML (experimental)
Abstract:
LLM confidence calibration is often evaluated by comparing two signals: token-probability scores and verbalized confidence. These signals are sometimes treated as direct readouts of model uncertainty, but their comparison depends on measurement choices that are rarely made explicit. In the main analysis, we hold the verbalized-confidence elicitation fixed: a single prompt template, probability scale, and output format. We then vary the measurement axes that define the verbalized-vs-token comparison: which answer string receives the token-probability score, how that score is read from the answer tokens, and under which conditioning context it is measured. We evaluate this design on four QA benchmarks across three open 7--8B base/Instruct model families, with larger Qwen2.5 variants as same-family robustness checks. The resulting comparison is sensitive to these choices: conditioning context changes the sign or magnitude of the ECE gap across settings, token readout produces smaller but still sign-moving changes, and changing the ECE estimator has little effect. Under the default generated-answer, bare-context protocol, Instruct settings are close to parity rather than showing a large calibration gain for verbalized confidence. In a separate supplied-answer analysis, surface-plausible wrong answers receive nearly the same confidence as supplied gold answers, suggesting that verbalized confidence also reflects answer plausibility and provenance rather than correctness alone. We argue that both confidence signals should be treated as protocol-dependent behavioral measurements, and provide a reporting checklist covering elicitation provenance, scored answer, token-probability readout, and conditioning context.
Subjects:
Artificial Intelligence (cs.AI)
Cite as:
arXiv:2605.27752
[cs.AI]
(or
arXiv:2605.27752v2
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2605.27752
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Hankyeol Kim [
view email
]
[v1]
Tue, 26 May 2026 23:03:38 UTC (60 KB)
[v2]
Mon, 1 Jun 2026 13:50:34 UTC (60 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Asking Is Not Enough: Protocol Sensitivity in LLM Confidence Calibration, by Hankyeol Kim and Pilsung Kang
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
2026-05
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