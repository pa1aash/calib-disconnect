---
title: '[2403.07974] LiveCodeBench: Holistic and Contamination Free Evaluation of
  Large Language Models for Code'
id: 240307974-livecodebench-holistic-and-contamination-free-evaluation-of-large-lang
tags:
- code-llm-calibration-aaai27-eabf3f
- benchmark-test-density
- occupancy-distinct
created: '2026-07-17T19:28:37.247241Z'
updated: '2026-07-17T19:31:33.118928Z'
source: https://arxiv.org/abs/2403.07974
source_domain: arxiv.org
fetched_at: '2026-07-17T19:28:37.246544Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: LiveCodeBench (arXiv:2403.07974, Mar 2024, v2 Jun 2024), Jain, Han, Gu, Li,
  Yan, Zhang, Wang, Solar-Lezama, Sen, Stoica (UC Berkeley/MIT). A contamination-free,
  continuously-updated code-LLM benchmark drawing 400 (as of the fetched abstract;
  the live benchmark has grown since) problems from LeetCode, AtCoder, and CodeForces
  contests, covering code generation, self-repair, code execution, and test-output
  prediction beyond plain generation; evaluated 18 base + 34 instruction-tuned LLMs.
  The fetched abstract does not itself state a per-problem test-case count; external
  secondary reporting (unconfirmed against primary text, flagged for verification)
  suggests an average around 17 test cases per problem, i.e., roughly 2.4x HumanEval's
  ~7 — denser than HumanEval but much sparser than TACO or CodeContests-family benchmarks
  for per-test dense-label purposes.
---

[2403.07974] LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2403.07974
(cs)
[Submitted on 12 Mar 2024 (
v1
), last revised 6 Jun 2024 (this version, v2)]
Title:
LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code
Authors:
Naman Jain
,
King Han
,
Alex Gu
,
Wen-Ding Li
,
Fanjia Yan
,
Tianjun Zhang
,
Sida Wang
,
Armando Solar-Lezama
,
Koushik Sen
,
Ion Stoica
View a PDF of the paper titled LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code, by Naman Jain and 9 other authors
View PDF
HTML (experimental)
Abstract:
Large Language Models (LLMs) applied to code-related applications have emerged as a prominent field, attracting significant interest from both academia and industry. However, as new and improved LLMs are developed, existing evaluation benchmarks (e.g., HumanEval, MBPP) are no longer sufficient for assessing their capabilities. In this work, we propose LiveCodeBench, a comprehensive and contamination-free evaluation of LLMs for code, which continuously collects new problems over time from contests across three competition platforms, namely LeetCode, AtCoder, and CodeForces. Notably, our benchmark also focuses on a broader range of code related capabilities, such as self-repair, code execution, and test output prediction, beyond just code generation. Currently, LiveCodeBench hosts four hundred high-quality coding problems that were published between May 2023 and May 2024. We have evaluated 18 base LLMs and 34 instruction-tuned LLMs on LiveCodeBench. We present empirical findings on contamination, holistic performance comparisons, potential overfitting in existing benchmarks as well as individual model comparisons. We will release all prompts and model completions for further community analysis, along with a general toolkit for adding new scenarios and model
Comments:
Website -
this https URL
Subjects:
Software Engineering (cs.SE)
; Computation and Language (cs.CL); Machine Learning (cs.LG)
Cite as:
arXiv:2403.07974
[cs.SE]
(or
arXiv:2403.07974v2
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2403.07974
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Naman Jain [
view email
]
[v1]
Tue, 12 Mar 2024 17:58:04 UTC (6,890 KB)
[v2]
Thu, 6 Jun 2024 17:41:21 UTC (7,772 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code, by Naman Jain and 9 other authors
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
2024-03
Change to browse by:
cs
cs.CL
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