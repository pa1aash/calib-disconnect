---
title: '[2605.21384] SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents'
id: 260521384-specbench-measuring-reward-hacking-in-long-horizon-coding-agents
tags:
- code-llm-requirement-pivots-5d35f5
created: '2026-07-20T06:57:12.724511Z'
updated: '2026-11-10T09:27:36.237264Z'
source: https://arxiv.org/abs/2605.21384
source_domain: arxiv.org
fetched_at: '2026-07-20T06:57:12.724162Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: SpecBench 2605.21384 measures reward hacking by long-horizon coding agents
  against visible versus held-out specification tests (peripheral to calibration)
---

*Suggested by [[260616062-auditing-reward-hackability-in-code-rl-training-environments]] — related reward-hacking-in-coding-agents benchmark found via same literature search*

[2605.21384] SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2605.21384
(cs)
[Submitted on 20 May 2026]
Title:
SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents
Authors:
Bingchen Zhao
,
Dhruv Srikanth
,
Yuxiang Wu
,
Zhengyao Jiang
View a PDF of the paper titled SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents, by Bingchen Zhao and 3 other authors
View PDF
HTML (experimental)
Abstract:
As long-horizon coding agents produce more code than any developer can review, oversight collapses onto a single surface: the automated test suite. Reward hacking naturally arises in this setup, as the agent optimizes for passing tests while deviating from the users true goal. We study this reward hacking phenomenon by decompose software engineering tasks into three parts: (i) a natural language description of the specification (ii) visible validation tests that exercise specified features in isolation, and (iii) held-out tests that compose those same features to simulate real-world usage. Based on the specification and the visible validation test suites, a genuine agent would be able to generate a solution that can also pass all of the held-out tests. Therefore we use the gap in pass rates on these two suites to quantify reward hacking. Based on this methodology, we introduce SpecBench, a benchmark comprising 30 systems-level programming tasks ranging from short horizon tasks like building a JSON parser to ultra long horizon tasks like building an entire OS kernel from scratch. Large-scale experiments reveal a consistent pattern: while every frontier agent saturates the visible suite, reward hacking persists, with smaller models exhibiting larger gaps on holdout suites. The gap also scales sharply with task length: it grows by 28 percentage points for every tenfold increase in code size. Failures range from subtle feature isolation to deliberate exploits, including a 2,900-line hash-table "compiler" that memorizes test inputs. SpecBench offers a principled testbed for measuring whether coding agents build genuine working systems or merely game the test suites developers hand them.
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2605.21384
[cs.SE]
(or
arXiv:2605.21384v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2605.21384
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Bingchen Zhao [
view email
]
[v1]
Wed, 20 May 2026 16:41:51 UTC (594 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents, by Bingchen Zhao and 3 other authors
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
2026-05
Change to browse by:
cs
cs.AI
cs.CL
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