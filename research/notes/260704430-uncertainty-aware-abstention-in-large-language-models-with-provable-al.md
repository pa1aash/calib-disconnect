---
title: '[2607.04430] Uncertainty-Aware Abstention in Large Language Models with Provable
  Alignment Guarantees'
id: 260704430-uncertainty-aware-abstention-in-large-language-models-with-provable-al
tags:
- code-llm-calibration-aaai27-eabf3f
- conformal-abstention
- selective-generation
created: '2026-07-17T18:34:27.405211Z'
updated: '2026-07-17T18:35:55.172991Z'
source: https://arxiv.org/abs/2607.04430
source_domain: arxiv.org
fetched_at: '2026-07-17T18:34:27.404713Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Proposes CIC, a confidence-interval-based calibration framework that converts
  ANY arbitrary (possibly poorly-calibrated) uncertainty score into a risk-controlled
  selective-answering rule via a held-out calibration set: for each candidate threshold
  it computes a high-probability upper confidence bound (Hoeffding or Clopper-Pearson)
  on the acceptance-conditioned error rate, and picks the largest threshold whose
  bound stays below a user-specified risk level alpha, maximizing answering rate under
  a finite-sample reliability constraint. Under exchangeability, guarantees with probability
  >= 1-delta that the selected threshold controls the accepted-answer error rate at
  level alpha. Evaluated on closed- and open-ended QA benchmarks across seven LLMs
  and multiple uncertainty estimators (general QA, not code-specific). Directly relevant
  as a general-purpose reduction: it explicitly does NOT require the underlying uncertainty
  score to be well-calibrated -- it just needs monotonic ordering -- so it is a natural
  mechanism to wrap around the target paper''s near-perfectly-calibrated repeated-sampling
  confidence signal to produce a formally risk-controlled abstention/selective-generation
  policy for code, a gap none of the code-specific abstention papers close with this
  generality.'
---

*Suggested by [[260517029-task-abstention-for-large-language-models-in-code-generation]] — Related provable-guarantee abstention framework, generalizes the multiple-hypothesis-testing abstention approach*

[2607.04430] Uncertainty-Aware Abstention in Large Language Models with Provable Alignment Guarantees
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2607.04430
(cs)
[Submitted on 5 Jul 2026]
Title:
Uncertainty-Aware Abstention in Large Language Models with Provable Alignment Guarantees
Authors:
Sijin Dong
,
Hiroyuki Shinnou
View a PDF of the paper titled Uncertainty-Aware Abstention in Large Language Models with Provable Alignment Guarantees, by Sijin Dong and 1 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) are increasingly deployed in question answering (QA) systems, yet they may generate hallucinated or misaligned responses without reliable confidence estimates. Uncertainty quantification (UQ) offers a natural basis for selective answering, where a system answers only when its prediction is deemed reliable and abstains otherwise. However, existing uncertainty scores for LLMs are often heuristic: a threshold chosen on such scores does not, by itself, provide statistical guarantees on the error rate among accepted answers. We propose CIC, a confidence-interval-based calibration framework that converts arbitrary uncertainty scores into risk-controlled selective answering rules. Given a held-out calibration set, CIC evaluates each generated response using an application-specific alignment criterion and associates it with an uncertainty score and a binary error label. For each candidate uncertainty threshold, CIC estimates the acceptance-conditioned error rate and constructs a high-probability upper confidence bound using either Hoeffding-style or Clopper-Pearson confidence intervals. It then selects the largest threshold whose upper bound is below a user-specified risk level $\alpha$, thereby maximizing the answering rate subject to a finite-sample reliability constraint. Under exchangeability, CIC guarantees with probability at least $1-\delta$ that the selected threshold, if non-null, controls the error rate among accepted answers at level $\alpha$. We evaluate CIC on both closed-ended and open-ended QA benchmarks across seven LLMs and multiple uncertainty estimators. Experimental results show that CIC consistently achieves valid risk control while retaining strong answering efficiency, providing a practical and statistically grounded mechanism for deploying LLMs in reliability-sensitive QA workflows.
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2607.04430
[cs.CL]
(or
arXiv:2607.04430v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2607.04430
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Sijin Dong [
view email
]
[v1]
Sun, 5 Jul 2026 17:50:32 UTC (358 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Uncertainty-Aware Abstention in Large Language Models with Provable Alignment Guarantees, by Sijin Dong and 1 other authors
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
2026-07
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