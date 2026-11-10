---
title: '[2506.10056] Pareto Optimal Code Generation'
id: 250610056-pareto-optimal-code-generation
tags:
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-11-09T23:10:57.278992Z'
updated: '2026-11-09T23:28:24.347418Z'
source: https://arxiv.org/abs/2506.10056
source_domain: arxiv.org
fetched_at: '2026-11-09T23:10:57.278633Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Vault note holds the arXiv abstract page; full text read from the arXiv PDF
  extracted locally (fetch of the PDF URL returned JUNK_CONTENT). Orlanski et al.
  frame verifier selection as accuracy-throughput Pareto optimization on four Python
  benchmarks, comparing full test suites, partial test execution, and outcome reward
  models (ORMs trained on CodeContests/GSM8K with Qwen2.5-Coder-Instruct 7B/14B/3B
  samples). Staged verification with ORMs gives 11.64x throughput at 8.26% accuracy
  loss. No model-confidence routing, no verbal confidence, no calibration. Adjacent
  but not occupying L3 (confidence-routed execution budgets); relevant as cost-accuracy
  comparator and for budget framing.
---

[2506.10056] Pareto Optimal Code Generation
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2506.10056
(cs)
[Submitted on 11 Jun 2025 (
v1
), last revised 24 Feb 2026 (this version, v2)]
Title:
Pareto Optimal Code Generation
Authors:
Gabriel Orlanski
,
Nicholas Roberts
,
Aws Albarghouthi
,
Frederic Sala
View a PDF of the paper titled Pareto Optimal Code Generation, by Gabriel Orlanski and 3 other authors
View PDF
HTML (experimental)
Abstract:
Generate-then-rank is the dominant test-time scaling (TTS) paradigm for code generation, but scaling accuracy by sampling and executing more candidates makes comprehensive verification a major computational bottleneck. This creates an inherent trade-off between accuracy and compute that, despite its importance to TTS, is often ignored. Specifically, faster but noisier signals, such as outcome reward models (ORMs), are dismissed as suboptimal. We frame verifier selection as a Pareto optimization problem and empirically map the accuracy-throughput frontier across signals, including the full test suite, heuristics for selective execution, and ORMs, across four Python benchmarks. We show that ORMs are most effective at optimizing the Pareto curve when pruning is used in the generate-then-rank pipeline--known as staged verification--where lightweight filters remove obviously incorrect solutions, including candidates with small syntactic or character-level bugs, before expensive verification. Our pruning analysis shows that eliminating incorrect yet highly ranked candidates (often character-level bugs) prevents wasted compute on incorrect tokens. We find that ORMs with staged verification shift the Pareto frontier outward, achieving 11.64x higher throughput at a cost of 8.26% accuracy relative to full test-suite verification.
Comments:
29 pages, 6 figures, code released here:
this https URL
Subjects:
Software Engineering (cs.SE)
; Programming Languages (cs.PL)
Cite as:
arXiv:2506.10056
[cs.SE]
(or
arXiv:2506.10056v2
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2506.10056
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Gabriel Orlanski [
view email
]
[v1]
Wed, 11 Jun 2025 17:58:21 UTC (179 KB)
[v2]
Tue, 24 Feb 2026 21:46:21 UTC (322 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Pareto Optimal Code Generation, by Gabriel Orlanski and 3 other authors
View PDF
HTML (experimental)
TeX Source
view license
Additional Features
Audio Summary
Current browse context:
cs.SE
< prev
|
next >
new
|
recent
|
2025-06
Change to browse by:
cs
cs.PL
References & Citations
SciX
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