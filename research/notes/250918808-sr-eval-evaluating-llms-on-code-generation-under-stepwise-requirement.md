---
title: '[2509.18808] SR-Eval: Evaluating LLMs on Code Generation under Stepwise Requirement
  Refinement'
id: 250918808-sr-eval-evaluating-llms-on-code-generation-under-stepwise-requirement
tags:
- code-llm-best-aaai-paper-6ded37
- requirement-decomposition
- adjacent-not-scooping
created: '2026-07-20T07:40:32.259144Z'
updated: '2026-07-20T07:43:33.367836Z'
source: https://arxiv.org/abs/2509.18808
source_domain: arxiv.org
fetched_at: '2026-07-20T07:40:32.258779Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Zhan, Gao, Hu & Gao (Sep 2025, rev. Mar 2026) present SR-Eval, a benchmark
  for iterative code generation under stepwise requirement refinement -- 443 multi-turn
  tasks / 1,857 questions at function- and repository-level (Python + Java), built
  via a multi-agent pipeline that simulates multi-round requirement evolution and
  a semantic-aware discriminative test-case generator ensuring each turn''s tests
  are consistent yet distinguishing. Best of 11 evaluated LLMs reaches only 22.67%
  function-level and 20.00% repo-level completion, showing the benchmark is far from
  saturated. This is a REQUIREMENT-axis benchmark but at a different granularity than
  our target: SR-Eval decomposes a task into sequential, evolving requirement TURNS
  (multi-turn dialogue structure) rather than into the concurrent, co-existing unit-test-level
  sub-requirements within a single static task that BigCodeBench''s ~5.6-tests-per-task
  structure provides. It is not a per-requirement partial-pass/hard-subset-mining
  or psychometric-scoring paper, but it demonstrates recent AAAI/SE-venue appetite
  for requirement-decomposition-based code benchmarks.'
---

[2509.18808] SR-Eval: Evaluating LLMs on Code Generation under Stepwise Requirement Refinement
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2509.18808
(cs)
[Submitted on 23 Sep 2025 (
v1
), last revised 17 Mar 2026 (this version, v2)]
Title:
SR-Eval: Evaluating LLMs on Code Generation under Stepwise Requirement Refinement
Authors:
Zexun Zhan
,
Shuzheng Gao
,
Ruida Hu
,
Cuiyun Gao
View a PDF of the paper titled SR-Eval: Evaluating LLMs on Code Generation under Stepwise Requirement Refinement, by Zexun Zhan and 3 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) have achieved remarkable progress in code generation. However, existing benchmarks mainly formalize the task as a static, single-turn problem, overlooking the stepwise requirement changes and iterative workflows in real-world software development. This mismatch limits the understanding of how well LLMs can support real-world development workflows. Constructing such iterative benchmarks is challenging due to the lack of public interaction traces and the difficulty of creating discriminative, turn-specific test cases.
To bridge this gap, we present SR-Eval, a benchmark specifically designed to assess LLMs on iterative code generation under Stepwise requirements Refinement. SR-Eval spans both function-level and repository-level tasks in Python and Java, enabling fine-grained and progressive evaluation across evolving requirements. The construction of SR-Eval follows a carefully designed pipeline that first leverages a multi-agent-based requirement generation method to simulate the development process and recover the multi-round interaction process from final requirements, then employs a semantic-aware discriminative test case generation component to ensure discriminative and consistent evaluation at each turn. SR-Eval comprises 443 multi-turn tasks and 1,857 questions at both function and repository levels. Using SR-Eval, we evaluate 11 representative LLMs with three prompting strategies that simulate different usage patterns. Results show that iterative code generation under stepwise requirement refinement remains highly challenging: the best-performing model achieves only 22.67% completion rate on function-level tasks and 20.00% on repository-level tasks. We further observe that prompting strategies substantially influence performance, highlighting the need for the development of advanced methods.
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2509.18808
[cs.SE]
(or
arXiv:2509.18808v2
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2509.18808
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Zexun Zhan [
view email
]
[v1]
Tue, 23 Sep 2025 08:59:05 UTC (601 KB)
[v2]
Tue, 17 Mar 2026 14:02:48 UTC (559 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled SR-Eval: Evaluating LLMs on Code Generation under Stepwise Requirement Refinement, by Zexun Zhan and 3 other authors
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
2025-09
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