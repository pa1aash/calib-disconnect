---
title: '[2606.14530] Code Correctness Is Linearly Decodable from LLM Hidden States
  Before Generation'
id: 260614530-code-correctness-is-linearly-decodable-from-llm-hidden-states-before-g
tags:
- code-llm-probe-verbalize-gap-3d8995
- hidden-state-probe
- whole-program-granularity
- pre-generation-probe
- code-correctness-probe
- scoop-risk
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-20T06:36:26.516780Z'
updated: '2026-11-09T23:26:02.243860Z'
source: https://arxiv.org/abs/2606.14530
source_domain: arxiv.org
fetched_at: '2026-07-20T06:36:26.516186Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Di Cicco (single-author, arXiv, submitted Jun 2026, v3 Jul 2026). Directly
  tests whether CODE correctness is linearly decodable from hidden states, on Qwen3-4B-Instruct-2507
  over 444 LiveCodeBench tasks. Key result: whether the model''s first-attempt code
  will pass (i.e. whole-solution correctness, not per-unit-test) is linearly decodable
  from the hidden state at the FINAL PROMPT TOKEN -- captured BEFORE any output/code
  token is generated -- with leakage-free held-out AUC 0.881 +/- 0.008 across 50 outer
  splits. After residualizing each hidden-state dimension against prompt length (confound
  control), the probe still achieves AUC 0.842 +/- 0.010, well above a prompt-length-only
  logistic baseline of AUC 0.657 +/- 0.014, and no nonlinear model tested improves
  on the linear probe. A planned analysis of whether self-repair (fixing a failed
  first attempt) leaves a geometric signature could not be completed -- successful
  repairs were too rare in-sample. Domain: CODE generation (LiveCodeBench). Granularity:
  WHOLE-TASK/whole-solution pass-fail (does the eventual generated program pass ALL
  tests), evaluated PRE-GENERATION from the prompt-only hidden state -- explicitly
  NOT per-requirement/per-unit-test decomposition; the paper does not decompose a
  single problem''s multiple test cases into separately-probed requirements. Also
  does not touch verbalized/self-reported confidence at all -- no comparison to the
  model''s own stated confidence, no training of a self-report head, no faithfulness-gap
  framing. 7 pages, single author, code+data+scripts released. This is the single
  most direct scoop-adjacent paper found for the code+hidden-state+correctness combination,
  but it (a) operates at whole-task granularity, not per-requirement, and (b) has
  no verbalization/self-report comparison, so it does not scoop the proposed pivot''s
  core claim (per-requirement granularity + faithfulness-gap-vs-verbalization). Flag:
  very recent, thin single-author preprint -- verify venue/peer-review status and
  citation count before treating as an established precedent in the write-up; still
  establishes clear prior art for ''hidden states predict code correctness'' at the
  whole-solution level and should be cited to differentiate the granularity claim.'
---

[2606.14530] Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2606.14530
(cs)
[Submitted on 12 Jun 2026 (
v1
), last revised 16 Jul 2026 (this version, v3)]
Title:
Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation
Authors:
Carlo Di Cicco
View a PDF of the paper titled Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation, by Carlo Di Cicco
View PDF
HTML (experimental)
Abstract:
Large language models encode rich information in their hidden states. This work asks whether the correctness of code that Qwen3-4B-Instruct-2507 has not yet generated is already legible in its hidden states, evaluated on a set of 444 tasks from LiveCodeBench. The correctness of the model's first-attempt code is linearly decodable from the hidden state at the final prompt token, captured before any output token is generated, with a leakage-free held-out AUC of 0.881 +/- 0.008 across 50 outer splits. To assess whether this signal is explained by prompt length, each hidden state dimension is residualized with respect to its linear effect. The probe still achieves an AUC of 0.842 +/- 0.010, substantially above a logistic prompt-length baseline of 0.657 +/- 0.014, and none of the nonlinear models tested improves upon it. A companion question about whether self-repair leaves a geometric signature in the model's hidden states could not be answered, because successful repairs following a failed first attempt are too rare in this setting to support the analysis. The contribution is both empirical and methodological, providing evidence that pre-generation hidden states contain a robust signal of eventual code correctness, together with a confound-control diagnostic that quantifies how much of that signal survives adjustment for prompt length.
Comments:
7 pages, 4 tables. Code, data, and analysis scripts available at
this https URL
Subjects:
Machine Learning (cs.LG)
Cite as:
arXiv:2606.14530
[cs.LG]
(or
arXiv:2606.14530v3
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2606.14530
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Carlo Di Cicco [
view email
]
[v1]
Fri, 12 Jun 2026 15:06:15 UTC (16 KB)
[v2]
Fri, 10 Jul 2026 10:43:50 UTC (16 KB)
[v3]
Thu, 16 Jul 2026 10:01:41 UTC (10 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation, by Carlo Di Cicco
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.LG
< prev
|
next >
new
|
recent
|
2026-06
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
IArxiv recommender toggle
IArxiv Recommender
(
What is IArxiv?
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