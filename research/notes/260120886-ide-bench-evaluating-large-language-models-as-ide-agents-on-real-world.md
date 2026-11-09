---
title: '[2601.20886] IDE-Bench: Evaluating Large Language Models as IDE Agents on
  Real-World Software Engineering Tasks'
id: 260120886-ide-bench-evaluating-large-language-models-as-ide-agents-on-real-world
tags:
- code-llm-requirement-pivots-5d35f5
- partial-pass-corroboration
created: '2026-07-20T06:54:27.052425Z'
updated: '2026-07-20T06:56:02.078882Z'
source: https://arxiv.org/abs/2601.20886
source_domain: arxiv.org
fetched_at: '2026-07-20T06:54:27.052006Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'IDE-Bench: 80 agentic SWE tasks across 8 uncontaminated repos (C/C++, Java,
  MERN), Dockerized IDE-tool harness, evaluated via per-test pass rate within each
  task (not just binary task pass@k). Abstract itself is about the benchmark''s tool-interface
  design; third-party analysis of its results highlights a ''near miss'' pattern --
  e.g. models repeatedly scoring 91.7% or 92.3% test-pass-rate on a task yet 0% under
  pass@k because the task-level metric requires all tests to pass -- illustrating
  that binary task framing hides graded partial competence even in agentic/repo-level
  settings, not just function-level ones. Relevant as further corroboration that ''partial
  credit reveals hidden competence'' is an emerging but not yet systematized observation
  across multiple benchmark types (agentic repo tasks here; BigCodeBench-style function
  tasks in our own harness).'
---

[2601.20886] IDE-Bench: Evaluating Large Language Models as IDE Agents on Real-World Software Engineering Tasks
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2601.20886
(cs)
[Submitted on 28 Jan 2026 (
v1
), last revised 30 Jan 2026 (this version, v2)]
Title:
IDE-Bench: Evaluating Large Language Models as IDE Agents on Real-World Software Engineering Tasks
Authors:
Spencer Mateega
,
Jeff Yang
,
Tiana Costello
,
Shaurya Jadhav
,
Nicole Tian
,
Agustin Garcinuño
View a PDF of the paper titled IDE-Bench: Evaluating Large Language Models as IDE Agents on Real-World Software Engineering Tasks, by Spencer Mateega and 5 other authors
View PDF
HTML (experimental)
Abstract:
IDE-Bench is a comprehensive framework for evaluating AI IDE agents on real-world software engineering tasks through an IDE-native tool interface. We present a Dockerized test harness that goes beyond raw terminal execution, granting models a structured tool ecosystem that represents AI-native IDEs like Cursor and Windsurf. By providing high-level abstractions for codebase search, structured file editing, and tools for testing full-stack applications, IDE-Bench evaluates an agent's ability to act as a true engineering collaborator. For evaluation and to prevent training data contamination, we created 80 tasks across eight never-published repositories spanning C/C++, Java, and MERN stacks, representing modern tech stack production scenarios, including feature implementation, bug fixing, refactoring, and performance optimization that mirror daily developer workflows in private codebases. Our benchmark is the first to systematically correlate agent-reported intent with successful project-level modifications in a multi-language, full-stack environment on completely uncontaminated code. We release IDE-Bench and a public leaderboard at:
this https URL
.
Subjects:
Software Engineering (cs.SE)
; Machine Learning (cs.LG)
Cite as:
arXiv:2601.20886
[cs.SE]
(or
arXiv:2601.20886v2
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2601.20886
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Spencer Mateega [
view email
]
[v1]
Wed, 28 Jan 2026 02:06:37 UTC (5,453 KB)
[v2]
Fri, 30 Jan 2026 03:43:06 UTC (5,453 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled IDE-Bench: Evaluating Large Language Models as IDE Agents on Real-World Software Engineering Tasks, by Spencer Mateega and 5 other authors
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
2026-01
Change to browse by:
cs
cs.LG
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