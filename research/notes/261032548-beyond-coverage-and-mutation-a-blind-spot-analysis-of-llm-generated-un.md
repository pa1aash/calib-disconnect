---
title: '[2610.32548] Beyond Coverage and Mutation: A Blind-Spot Analysis of LLM-Generated
  Unit Tests'
id: 261032548-beyond-coverage-and-mutation-a-blind-spot-analysis-of-llm-generated-un
tags:
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-11-09T23:11:08.553544Z'
updated: '2026-11-09T23:28:28.538392Z'
source: https://arxiv.org/abs/2610.32548
source_domain: arxiv.org
fetched_at: '2026-11-09T23:11:08.552964Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Vault note holds the arXiv abstract page; full text read from locally extracted
  arXiv PDF. Shi et al. introduce BlindSpotEval (Boundary-Value Adequacy, Control-Flow
  Adequacy, Oracle Strength) and ObligBench (895 complex + 700 low-complexity Java
  functions); 14,320 tests from GPT-5.4, Gemma-4-31B, Gemini-3.6-flash, Qwen3-Coder-30B
  under four prompting strategies. 19.7% of tests fail to execute; 15.6% of test failures
  are wrong-oracle. Relevant to L4 self-written test adequacy (LLM-written tests are
  blind to null/negative/empty inputs and exceptional paths) but Java, no confidence
  estimation.
---

[2610.32548] Beyond Coverage and Mutation: A Blind-Spot Analysis of LLM-Generated Unit Tests
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2610.32548
(cs)
[Submitted on 23 Oct 2026]
Title:
Beyond Coverage and Mutation: A Blind-Spot Analysis of LLM-Generated Unit Tests
Authors:
Xiaoyu Shi
,
Wenqiang Luo
,
Boyang Yang
,
Haoye Tian
View a PDF of the paper titled Beyond Coverage and Mutation: A Blind-Spot Analysis of LLM-Generated Unit Tests, by Xiaoyu Shi and 3 other authors
View PDF
HTML (experimental)
Abstract:
Existing evaluation protocols for unit tests rely on aggregate metrics such as branch coverage and mutation score. These metrics quantify the extent to which a test suite exercises program behavior, but do not identify the behavioral obligations it systematically leaves unchecked. We propose BlindSpotEval, an obligation-based evaluation framework aligned with the Arrange-Act-Assert pattern. The framework comprises three metrics, Boundary-Value Adequacy, Control-Flow Adequacy, and Oracle Strength, complemented by an assessment of execution reliability. We also introduce ObligBench, a complexity-stratified Java benchmark comprising 895 complex and 700 low-complexity functions with source-side obligation annotations. Evaluating 14,320 tests from four LLMs under four prompting strategies reveals systematic blind spots. Incorrect assertions account for 15.6% of test failures, illustrating that coverage alone does not establish oracle correctness. Among executable tests, coverage of null, negative, and empty arguments reaches only 34.8%, 23.8%, and 38.8%, compared with average coverage above 93% for booleans. Catch blocks and default groups have Control-Flow Adequacy scores of only 0.100 and 0.312. Across both dimensions, LLM-generated tests exhibit the happy-path bias observed in human-written tests, concentrating on normal inputs and expected flows while leaving unusual values and exceptional paths unchecked. Oracle strength is high on average but uneven, with weaker assertions for object return property values and exceptions. These blind spots also occur in low-complexity functions, suggesting that code complexity alone does not explain them. BlindSpotEval provides construct-level adequacy profiles that identify under-tested obligation types and can guide targeted improvements beyond those supported by aggregate scores alone.
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2610.32548
[cs.SE]
(or
arXiv:2610.32548v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2610.32548
Focus to learn more
arXiv-issued DOI via DataCite (pending registration)
Submission history
From: Xiaoyu Shi [
view email
]
[v1]
Fri, 23 Oct 2026 12:29:53 UTC (278 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Beyond Coverage and Mutation: A Blind-Spot Analysis of LLM-Generated Unit Tests, by Xiaoyu Shi and 3 other authors
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
2026-10
Change to browse by:
cs
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