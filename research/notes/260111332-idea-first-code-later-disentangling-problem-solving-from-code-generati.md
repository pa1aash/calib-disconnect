---
title: '[2601.11332] Idea First, Code Later: Disentangling Problem Solving from Code
  Generation in Evaluating LLMs for Competitive Programming'
id: 260111332-idea-first-code-later-disentangling-problem-solving-from-code-generati
tags:
- aaai-bar-eval-dprc-d78e07
- competitive-programming
- all-or-nothing
created: '2026-07-19T20:10:02.983652Z'
updated: '2026-07-19T20:10:23.520535Z'
source: https://arxiv.org/abs/2601.11332
source_domain: arxiv.org
fetched_at: '2026-07-19T20:10:02.983324Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Hadhoud, Elsetohy, Hudi, Cruz, Halim, Aji (arXiv 2601.11332, Jan 2026, venue
  not yet confirmed). Argues that standard competitive-programming pass/fail evaluation
  conflates two distinct capabilities -- algorithmic problem-solving and code implementation
  -- and proposes centering natural-language ''editorials'' (algorithm explanations)
  as an intermediate evaluation artifact. Builds an 83-problem ICPC-style dataset
  with gold editorials + full test suites, evaluates 19 LLMs, and finds that even
  with gold (expert) editorials provided, models still struggle with implementation
  -- while the generated-vs-gold editorial gap reveals a persistent algorithmic problem-solving
  bottleneck distinct from coding bugs. Relevant to DPRC''s framing: independent confirmation
  that competitive-programming correctness is evaluated and explained through mechanisms
  OTHER than per-test partial credit (editorial/reasoning-quality diagnosis instead),
  reinforcing that the field treats competitive-programming failure as a monolithic
  solve/no-solve or reasoning/implementation split rather than a graded per-requirement
  signal -- consistent with DPRC''s claim that competitive code lacks the partial-pass
  substrate that per-requirement confidence needs.'
---

*Suggested by [[250622954-evaluating-and-improving-large-language-models-for-competitive-program]] — further characterizes competitive programming as structurally distinct (problem-solving vs implementation), reinforcing the competitive-vs-functional divide*

[2601.11332] Idea First, Code Later: Disentangling Problem Solving from Code Generation in Evaluating LLMs for Competitive Programming
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2601.11332
(cs)
[Submitted on 16 Jan 2026]
Title:
Idea First, Code Later: Disentangling Problem Solving from Code Generation in Evaluating LLMs for Competitive Programming
Authors:
Sama Hadhoud
,
Alaa Elsetohy
,
Frederikus Hudi
,
Jan Christian Blaise Cruz
,
Steven Halim
,
Alham Fikri Aji
View a PDF of the paper titled Idea First, Code Later: Disentangling Problem Solving from Code Generation in Evaluating LLMs for Competitive Programming, by Sama Hadhoud and 5 other authors
View PDF
HTML (experimental)
Abstract:
Large Language Models (LLMs) increasingly succeed on competitive programming problems, yet existing evaluations conflate algorithmic reasoning with code-level implementation. We argue that competitive programming is fundamentally a problem-solving task and propose centering natural-language editorials in both solution generation and evaluation. Generating an editorial prior to code improves solve rates for some LLMs, with substantially larger gains when using expertly written gold editorials. However, even with gold editorials, models continue to struggle with implementation, while the gap between generated and gold editorials reveals a persistent problem-solving bottleneck in specifying correct and complete algorithms. Beyond pass/fail metrics, we diagnose reasoning errors by comparing model-generated editorials to gold standards using expert annotations and validate an LLM-as-a-judge protocol for scalable evaluation. We introduce a dataset of 83 ICPC-style problems with gold editorials and full test suites, and evaluate 19 LLMs, arguing that future benchmarks should explicitly separate problem solving from implementation.
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2601.11332
[cs.CL]
(or
arXiv:2601.11332v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2601.11332
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Sama Hadhoud [
view email
]
[v1]
Fri, 16 Jan 2026 14:29:54 UTC (1,791 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Idea First, Code Later: Disentangling Problem Solving from Code Generation in Evaluating LLMs for Competitive Programming, by Sama Hadhoud and 5 other authors
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
2026-01
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