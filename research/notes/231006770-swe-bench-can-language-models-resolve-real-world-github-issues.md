---
title: '[2310.06770] SWE-bench: Can Language Models Resolve Real-World GitHub Issues?'
id: 231006770-swe-bench-can-language-models-resolve-real-world-github-issues
tags:
- aaai-bar-eval-dprc-d78e07
- benchmark
- swe-bench
- iclr-2024
created: '2026-07-19T20:04:01.904946Z'
updated: '2026-07-19T20:06:45.488435Z'
source: https://arxiv.org/abs/2310.06770
source_domain: arxiv.org
fetched_at: '2026-07-19T20:04:01.904612Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'SWE-bench (Jimenez, Yang, Wettig, Yao, Pei, Press, Narasimhan; Princeton/others;
  ICLR 2024 Oral, arXiv:2310.06770). 2,294 real-world software-engineering problems
  from GitHub issues + merged PRs across 12 popular Python repos; a model must edit
  the codebase to resolve the issue, requiring multi-file/multi-function reasoning
  and long-context handling well beyond function-level code generation. Headline number:
  best model (Claude 2) solved only 1.96% of issues at release, establishing SWE-bench
  as an extremely hard, far-from-saturated, top-tier (ICLR Oral) benchmark. Relevant
  to DPRC as the standing comparison point: SWE-bench is repository-scale/patch-level
  (binary resolved-or-not per issue, similar all-or-nothing flavor to competitive
  code at the issue level, though richer at the file/hunk level), whereas BigCodeBench
  is function-level with dense per-task unit tests (5.6 tests/task) enabling per-requirement
  partial-pass signal. This confirms BigCodeBench, not SWE-bench, is the correct benchmark
  class for DPRC''s per-unittest-method confidence localization claim; SWE-bench''s
  issue-level binary resolution would likely behave more like TACO (collapse to scalar)
  than like BigCodeBench.'
---

[2310.06770] SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2310.06770
(cs)
[Submitted on 10 Oct 2023 (
v1
), last revised 11 Nov 2024 (this version, v3)]
Title:
SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
Authors:
Carlos E. Jimenez
,
John Yang
,
Alexander Wettig
,
Shunyu Yao
,
Kexin Pei
,
Ofir Press
,
Karthik Narasimhan
View a PDF of the paper titled SWE-bench: Can Language Models Resolve Real-World GitHub Issues?, by Carlos E. Jimenez and 6 other authors
View PDF
Abstract:
Language models have outpaced our ability to evaluate them effectively, but for their future development it is essential to study the frontier of their capabilities. We find real-world software engineering to be a rich, sustainable, and challenging testbed for evaluating the next generation of language models. To this end, we introduce SWE-bench, an evaluation framework consisting of $2,294$ software engineering problems drawn from real GitHub issues and corresponding pull requests across $12$ popular Python repositories. Given a codebase along with a description of an issue to be resolved, a language model is tasked with editing the codebase to address the issue. Resolving issues in SWE-bench frequently requires understanding and coordinating changes across multiple functions, classes, and even files simultaneously, calling for models to interact with execution environments, process extremely long contexts and perform complex reasoning that goes far beyond traditional code generation tasks. Our evaluations show that both state-of-the-art proprietary models and our fine-tuned model SWE-Llama can resolve only the simplest issues. The best-performing model, Claude 2, is able to solve a mere $1.96$% of the issues. Advances on SWE-bench represent steps towards LMs that are more practical, intelligent, and autonomous.
Comments:
Data, code, and leaderboard are available at
this https URL
ICLR 2024,
this https URL
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Software Engineering (cs.SE)
Cite as:
arXiv:2310.06770
[cs.CL]
(or
arXiv:2310.06770v3
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2310.06770
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Carlos E. Jimenez [
view email
]
[v1]
Tue, 10 Oct 2023 16:47:29 UTC (2,003 KB)
[v2]
Fri, 5 Apr 2024 18:16:29 UTC (2,258 KB)
[v3]
Mon, 11 Nov 2024 23:05:04 UTC (2,398 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled SWE-bench: Can Language Models Resolve Real-World GitHub Issues?, by Carlos E. Jimenez and 6 other authors
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
2023-10
Change to browse by:
cs
cs.AI
cs.SE
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