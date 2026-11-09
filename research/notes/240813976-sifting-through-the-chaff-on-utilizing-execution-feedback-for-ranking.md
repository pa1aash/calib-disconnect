---
title: '[2408.13976] Sifting through the Chaff: On Utilizing Execution Feedback for
  Ranking the Generated Code Candidates'
id: 240813976-sifting-through-the-chaff-on-utilizing-execution-feedback-for-ranking
tags:
- code-llm-requirement-pivots-5d35f5
- code-ranking
- execution-feedback
created: '2026-07-20T06:53:11.818065Z'
updated: '2026-07-20T06:55:37.027365Z'
source: https://arxiv.org/abs/2408.13976
source_domain: arxiv.org
fetched_at: '2026-07-20T06:53:11.817744Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Sun, Wan, Li, Zhang, Jin, Li, Lyu (ASE 2024): RankEF ranks multiple whole-solution
  code candidates by multi-task learning that jointly predicts a correctness classification
  label and generates execution-feedback-style explanations of why code is wrong,
  avoiding the need to actually execute code at ranking time. Outperforms CodeRanker
  (prior SOTA non-execution ranker) on three code-gen benchmarks. Ranking unit is
  the entire candidate program, not individual requirements/unit tests within a program
  -- there is no per-requirement pass/fail signal used to select or repair specific
  parts of a solution. Confirms code-candidate ranking/selection work operates at
  whole-solution granularity.'
---

[2408.13976] Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2408.13976
(cs)
[Submitted on 26 Aug 2024 (
v1
), last revised 19 Sep 2024 (this version, v3)]
Title:
Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates
Authors:
Zhihong Sun
,
Yao Wan
,
Jia Li
,
Hongyu Zhang
,
Zhi Jin
,
Ge Li
,
Chen Lyu
View a PDF of the paper titled Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates, by Zhihong Sun and 6 other authors
View PDF
HTML (experimental)
Abstract:
Large Language Models (LLMs), such as GPT-4, StarCoder, and CodeLlama, are transforming the way developers approach programming by automatically generating code based on given natural language descriptions. Despite advancements, generating syntactically and semantically correct code remains challenging, especially for complex programming tasks. Existing approaches typically generate multiple candidate solutions using LLMs to increase the likelihood of producing correct code. However, selecting the correct code from these candidates-a process known as code ranking-remains a major challenge. Current research on code ranking can be categorized into execution-based and non-execution-based methods. Execution-based methods, although effective, encounter notable limitations, such as scarcity of quality unit tests and security risks. Non-execution-based methods like CodeRanker, which rely solely on classification labels to train a code ranker, struggle to capture subtle errors and provide detailed error insights. Recognizing the strengths and limitations of both approaches, we propose a new method. The key insight of our work is that an effective code ranker is expected to truly comprehend the underlying causes of erroneous code, as relying solely on classification labels is insufficient. Inspired by this, this paper puts forward RankEF, an innovative approach for code ranking that leverages execution feedback. RankEF employs multi-task learning to integrate code classification with execution feedback generation. This approach enables the model to understand the reasons behind incorrect code, distinguishing between correct and incorrect solutions without the need to execute the code during the ranking phase. Experiments on three code generation benchmarks demonstrate that RankEF significantly outperforms the state-of-the-art CodeRanker.
Comments:
Accepted by the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE 2024)
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2408.13976
[cs.SE]
(or
arXiv:2408.13976v3
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2408.13976
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Chen Lyu [
view email
]
[v1]
Mon, 26 Aug 2024 01:48:57 UTC (4,593 KB)
[v2]
Tue, 27 Aug 2024 06:49:19 UTC (4,592 KB)
[v3]
Thu, 19 Sep 2024 13:16:34 UTC (3,560 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates, by Zhihong Sun and 6 other authors
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
2024-08
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