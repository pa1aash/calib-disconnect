---
title: '[2407.21227] TaskEval: Assessing Difficulty of Code Generation Tasks for Large
  Language Models'
id: 240721227-taskeval-assessing-difficulty-of-code-generation-tasks-for-large-langu
tags:
- code-llm-requirement-pivots-5d35f5
- irt-code-difficulty
- prior-art-check
created: '2026-07-20T06:52:49.248570Z'
updated: '2026-07-20T06:55:53.261113Z'
source: https://arxiv.org/abs/2407.21227
source_domain: arxiv.org
fetched_at: '2026-07-20T06:52:49.248153Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'TaskEval (accepted ACM TOSEM): applies Item Response Theory to CODE-GENERATION
  TASKS (whole HumanEval+/ClassEval problems), not to sub-task/per-requirement units.
  Uses diverse prompt reformulations per task + 8 LLMs to fit IRT difficulty/discrimination
  parameters per TASK, then cross-analyzes task difficulty against topic clusters
  (17/21 topics) and programming constructs used (variable assignment, conditionals,
  etc.), and compares LLM-vs-human difficulty perception. Granularity is at the whole-problem
  level, so it does not overlap with a per-unittest-requirement IRT approach -- an
  IRT model fit on individual test_* requirements (our candidate framing) remains
  unaddressed by this paper, though it establishes IRT-for-code-difficulty as a known,
  TOSEM-published technique that a requirement-level extension would need to differentiate
  against explicitly.'
---

[2407.21227] TaskEval: Assessing Difficulty of Code Generation Tasks for Large Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2407.21227
(cs)
[Submitted on 30 Jul 2024 (
v1
), last revised 24 Oct 2025 (this version, v3)]
Title:
TaskEval: Assessing Difficulty of Code Generation Tasks for Large Language Models
Authors:
Florian Tambon
,
Amin Nikanjam
,
Cyrine Zid
,
Foutse Khomh
,
Giuliano Antoniol
View a PDF of the paper titled TaskEval: Assessing Difficulty of Code Generation Tasks for Large Language Models, by Florian Tambon and 4 other authors
View PDF
HTML (experimental)
Abstract:
Large Language Models (LLMs) excel in code-related tasks like code generation, but benchmark evaluations often overlook task characteristics, such as difficulty. Moreover, benchmarks are usually built using tasks described with a single prompt, despite the formulation of prompts having a profound impact on the outcome. This paper introduces a generalist approach, TaskEval, a framework using diverse prompts and Item Response Theory (IRT) to efficiently assess LLMs' capabilities and benchmark task characteristics, improving the understanding of their performance.
Using two code generation benchmarks, \textit{HumanEval}+ and \textit{ClassEval}, as well as 8 code generation LLMs, we show that \textit{TaskEval} is capable of characterising the properties of tasks. Using topic analysis, we identify and analyse the tasks of 17 and 21 topics within the benchmarks. We also cross-analyse tasks' characteristics with programming constructs (e.g., variable assignment, conditions, etc.) used by LLMs, emphasising some patterns with tasks' difficulty. Finally, we conduct a comparison between the difficulty assessment of tasks by human annotators and LLMs. Orthogonal to current benchmarking evaluation efforts, \textit{TaskEval} can assist researchers and practitioners in fostering better assessments of LLMs. The tasks' characteristics can be used to identify shortcomings within existing benchmarks or improve the evaluation of LLMs.
Comments:
Accepted ACM Transactions on Software Engineering and Methodology
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2407.21227
[cs.SE]
(or
arXiv:2407.21227v3
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2407.21227
Focus to learn more
arXiv-issued DOI via DataCite
Related DOI
:
https://doi.org/10.1145/3773285
Focus to learn more
DOI(s) linking to related resources
Submission history
From: Florian Tambon [
view email
]
[v1]
Tue, 30 Jul 2024 22:31:19 UTC (700 KB)
[v2]
Mon, 10 Mar 2025 17:41:17 UTC (2,158 KB)
[v3]
Fri, 24 Oct 2025 07:24:46 UTC (1,063 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled TaskEval: Assessing Difficulty of Code Generation Tasks for Large Language Models, by Florian Tambon and 4 other authors
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
2024-07
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