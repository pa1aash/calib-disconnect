---
title: '[2506.05817] CodeContests+: High-Quality Test Case Generation for Competitive
  Programming'
id: 250605817-codecontests-high-quality-test-case-generation-for-competitive-program
tags:
- code-llm-calibration-aaai27-eabf3f
- benchmark-test-density
- occupancy-distinct
created: '2026-07-17T19:28:32.559379Z'
updated: '2026-07-17T19:31:26.969660Z'
source: https://arxiv.org/abs/2506.05817
source_domain: arxiv.org
fetched_at: '2026-07-17T19:28:32.559033Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'CodeContests+ (arXiv:2506.05817, Jun 2025): an LLM-agent-based system that
  regenerates higher-quality, higher-accuracy test cases for the original DeepMind
  CodeContests competitive-programming dataset. Validated against 1.72 million submissions
  with known pass/fail labels, showing CodeContests+ achieves significantly higher
  evaluation accuracy and True Positive Rate than the original CodeContests test suite;
  RL experiments confirm that improved test-case quality yields measurable RL performance
  gains. External secondary reporting (not in this fetched abstract, flagged for verification
  against full paper) states the CodeContests+ 1x version averages ~25 test cases/problem,
  with 2x-5x augmented versions averaging 44/62/80/98 test cases/problem — versus
  the original CodeContests dataset, where only ~67% of 1.18M generated test cases
  passed validation. Relevant to benchmark-selection: shows CodeContests-family benchmarks
  are dense in per-problem test cases (tens per problem) but the ORIGINAL CodeContests
  test suite has known correctness/noise issues that a confidence-calibration method
  built on ''free'' per-test labels would inherit unless CodeContests+ or similar
  cleaned test suites are used.'
---

*Suggested by [[260519369-when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-cod]] — benchmark test-case density source for CodeContests*

[2506.05817] CodeContests+: High-Quality Test Case Generation for Competitive Programming
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2506.05817
(cs)
[Submitted on 6 Jun 2025]
Title:
CodeContests+: High-Quality Test Case Generation for Competitive Programming
Authors:
Zihan Wang
,
Siyao Liu
,
Yang Sun
,
Hongyan Li
,
Kai Shen
View a PDF of the paper titled CodeContests+: High-Quality Test Case Generation for Competitive Programming, by Zihan Wang and 4 other authors
View PDF
HTML (experimental)
Abstract:
Competitive programming, due to its high reasoning difficulty and precise correctness feedback, has become a key task for both training and evaluating the reasoning capabilities of large language models (LLMs). However, while a large amount of public problem data, such as problem statements and solutions, is available, the test cases of these problems are often difficult to obtain. Therefore, test case generation is a necessary task for building large-scale datasets, and the quality of the test cases directly determines the accuracy of the evaluation. In this paper, we introduce an LLM-based agent system that creates high-quality test cases for competitive programming problems. We apply this system to the CodeContests dataset and propose a new version with improved test cases, named CodeContests+. We evaluated the quality of test cases in CodeContestsPlus. First, we used 1.72 million submissions with pass/fail labels to examine the accuracy of these test cases in evaluation. The results indicated that CodeContests+ achieves significantly higher accuracy than CodeContests, particularly with a notably higher True Positive Rate (TPR). Subsequently, our experiments in LLM Reinforcement Learning (RL) further confirmed that improvements in test case quality yield considerable advantages for RL.
Comments:
28 pages, 7 figures
Subjects:
Software Engineering (cs.SE)
; Computation and Language (cs.CL)
Cite as:
arXiv:2506.05817
[cs.SE]
(or
arXiv:2506.05817v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2506.05817
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Zihan Wang [
view email
]
[v1]
Fri, 6 Jun 2025 07:29:01 UTC (1,997 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled CodeContests+: High-Quality Test Case Generation for Competitive Programming, by Zihan Wang and 4 other authors
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
2025-06
Change to browse by:
cs
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