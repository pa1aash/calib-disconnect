---
title: '[2302.08468] LEVER: Learning to Verify Language-to-Code Generation with Execution'
id: 230208468-lever-learning-to-verify-language-to-code-generation-with-execution
tags:
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-11-09T23:11:06.042987Z'
updated: '2026-11-09T23:28:29.796647Z'
source: https://arxiv.org/abs/2302.08468
source_domain: arxiv.org
fetched_at: '2026-11-09T23:11:06.042349Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Vault note holds the arXiv abstract page; full text read from locally extracted
  arXiv PDF (ICML 2023). Ni et al.: learned verifier (T5/Codex-based) scores sampled
  programs from NL input, program, and execution result; reranks by combining verification
  probability with generation probability and marginalizing over programs with identical
  execution results. Gains 4.6% to 10.9% with code-davinci-002 on four datasets (Spider,
  WikiTQ, GSM8K, MBPP). Verification-utility occupant (execution-aware correctness
  prediction) but not confidence-routed budgets, not verbal confidence, not hidden-state
  probes.'
---

[2302.08468] LEVER: Learning to Verify Language-to-Code Generation with Execution
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2302.08468
(cs)
[Submitted on 16 Feb 2023 (
v1
), last revised 1 Sep 2023 (this version, v3)]
Title:
LEVER: Learning to Verify Language-to-Code Generation with Execution
Authors:
Ansong Ni
,
Srini Iyer
,
Dragomir Radev
,
Ves Stoyanov
,
Wen-tau Yih
,
Sida I. Wang
,
Xi Victoria Lin
View a PDF of the paper titled LEVER: Learning to Verify Language-to-Code Generation with Execution, by Ansong Ni and 6 other authors
View PDF
HTML (experimental)
Abstract:
The advent of large language models trained on code (code LLMs) has led to significant progress in language-to-code generation. State-of-the-art approaches in this area combine LLM decoding with sample pruning and reranking using test cases or heuristics based on the execution results. However, it is challenging to obtain test cases for many real-world language-to-code applications, and heuristics cannot well capture the semantic features of the execution results, such as data type and value range, which often indicates the correctness of the program. In this work, we propose LEVER, a simple approach to improve language-to-code generation by learning to verify the generated programs with their execution results. Specifically, we train verifiers to determine whether a program sampled from the LLMs is correct or not based on the natural language input, the program itself and its execution results. The sampled programs are reranked by combining the verification score with the LLM generation probability, and marginalizing over programs with the same execution results. On four datasets across the domains of table QA, math QA and basic Python programming, LEVER consistently improves over the base code LLMs(4.6% to 10.9% with code-davinci-002) and achieves new state-of-the-art results on all of them.
Comments:
ICML'23; code available at
this https URL
Subjects:
Machine Learning (cs.LG)
; Computation and Language (cs.CL); Programming Languages (cs.PL); Software Engineering (cs.SE)
Cite as:
arXiv:2302.08468
[cs.LG]
(or
arXiv:2302.08468v3
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2302.08468
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Ansong Ni [
view email
]
[v1]
Thu, 16 Feb 2023 18:23:22 UTC (3,509 KB)
[v2]
Wed, 5 Jul 2023 08:00:15 UTC (1,621 KB)
[v3]
Fri, 1 Sep 2023 17:37:42 UTC (3,512 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled LEVER: Learning to Verify Language-to-Code Generation with Execution, by Ansong Ni and 6 other authors
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
2023-02
Change to browse by:
cs
cs.CL
cs.PL
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