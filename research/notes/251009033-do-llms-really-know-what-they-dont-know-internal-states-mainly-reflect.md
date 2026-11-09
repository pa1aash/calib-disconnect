---
title: '[2510.09033] Do LLMs Really Know What They Don''t Know? Internal States Mainly
  Reflect Knowledge Recall Rather Than Truthfulness'
id: 251009033-do-llms-really-know-what-they-dont-know-internal-states-mainly-reflect
tags:
- code-llm-probe-verbalize-gap-3d8995
- latent-knowledge
- critique
- hallucination-taxonomy
created: '2026-07-20T06:38:33.742384Z'
updated: '2026-07-20T06:40:00.161408Z'
source: https://arxiv.org/abs/2510.09033
source_domain: arxiv.org
fetched_at: '2026-07-20T06:38:33.742037Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Cheang, Chan, Zhang, Deng (arXiv Oct 2025, rev. Apr 2026). Critical/nuancing
  follow-up to the ''LLMs know what they don''t know'' internal-probing literature
  (incl. SAPLMA/Azaria and Burns-style work). Argues hallucinations have heterogeneous
  causes: Unassociated Hallucinations (UHs, lacking any parametric grounding) vs Associated
  Hallucinations (AHs, driven by spurious statistical associations learned in pretraining
  that mimic genuine recall). Mechanistic analysis shows hidden states mainly encode
  WHETHER the model is doing parametric knowledge recall, not whether the output is
  actually true -- so AHs have hidden-state geometry that overlaps heavily with genuinely
  correct/factual outputs, making standard probe-based hallucination detectors fail
  on AHs specifically, while UHs remain detectable via distinctive clustered representations.
  Domain: general factual QA/hallucination benchmarks, non-code. Granularity: whole-output
  level. Relevance to our lane: this is an important CAVEAT/limitation paper for the
  premise that ''internal states cleanly encode correctness'' -- it shows the internal
  signal is confounded with recall-vs-generation processes, not a pure truth detector,
  for one hallucination subtype. Strengthens the case that a probe achieving only
  moderate AUROC (0.72-0.75) on a genuinely new domain (per-requirement code correctness)
  is plausible and non-trivial, and gives the pivot paper a natural related-work citation
  to preempt a ''but doesn''t this confound with recall?'' reviewer objection.'
---

[2510.09033] Do LLMs Really Know What They Don't Know? Internal States Mainly Reflect Knowledge Recall Rather Than Truthfulness
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2510.09033
(cs)
[Submitted on 10 Oct 2025 (
v1
), last revised 17 Apr 2026 (this version, v3)]
Title:
Do LLMs Really Know What They Don't Know? Internal States Mainly Reflect Knowledge Recall Rather Than Truthfulness
Authors:
Chi Seng Cheang
,
Hou Pong Chan
,
Wenxuan Zhang
,
Yang Deng
View a PDF of the paper titled Do LLMs Really Know What They Don't Know? Internal States Mainly Reflect Knowledge Recall Rather Than Truthfulness, by Chi Seng Cheang and 3 other authors
View PDF
HTML (experimental)
Abstract:
Recent work suggests that LLMs "know what they don't know", positing that hallucinated and factually correct outputs arise from distinct internal processes and can therefore be distinguished using internal signals. However, hallucinations have multifaceted causes: beyond simple knowledge gaps, they can emerge from training incentives that encourage models to exploit statistical shortcuts or spurious associations learned during pretraining. In this paper, we argue that when LLMs rely on such learned associations to produce hallucinations, their internal processes are mechanistically similar to those of factual recall, as both stem from strong statistical correlations encoded in the model's parameters. To verify this, we propose a novel taxonomy categorizing hallucinations into Unassociated Hallucinations (UHs), where outputs lack parametric grounding, and Associated Hallucinations (AHs), which are driven by spurious associations. Through mechanistic analysis, we compare their computational processes and hidden-state geometries with factually correct outputs. Our results show that hidden states primarily reflect whether the model is recalling parametric knowledge rather than the truthfulness of the output itself. Consequently, AHs exhibit hidden-state geometries that largely overlap with factual outputs, rendering standard detection methods ineffective. In contrast, UHs exhibit distinctive, clustered representations that facilitate reliable detection.
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2510.09033
[cs.CL]
(or
arXiv:2510.09033v3
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2510.09033
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Chi Seng Cheang [
view email
]
[v1]
Fri, 10 Oct 2025 06:09:04 UTC (339 KB)
[v2]
Fri, 6 Mar 2026 08:31:05 UTC (338 KB)
[v3]
Fri, 17 Apr 2026 13:34:13 UTC (333 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Do LLMs Really Know What They Don't Know? Internal States Mainly Reflect Knowledge Recall Rather Than Truthfulness, by Chi Seng Cheang and 3 other authors
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
2025-10
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