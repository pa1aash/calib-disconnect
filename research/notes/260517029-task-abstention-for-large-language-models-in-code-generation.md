---
title: '[2605.17029] Task Abstention for Large Language Models in Code Generation'
id: 260517029-task-abstention-for-large-language-models-in-code-generation
tags:
- code-llm-calibration-aaai27-eabf3f
- selective-generation
- abstention
created: '2026-07-17T18:29:29.781610Z'
updated: '2026-07-17T18:31:37.749836Z'
source: http://arxiv.org/abs/2605.17029
source_domain: arxiv.org
fetched_at: '2026-07-17T18:29:29.781086Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Proposes a calibrated task-abstention rule for code LLMs grounded in multiple-hypothesis
  testing: assesses generation consistency via repeated CODE EXECUTION outcomes (not
  token log-probs, not oracle tests) and abstains when consistency fails a statistical
  threshold, yielding a distribution-free theoretical guarantee on abstention error.
  Evaluated on benchmark datasets across several open-source code LLMs; claims more
  accurate/efficient hallucination identification than existing abstention techniques.
  Turns an execution-consistency signal (a close cousin of the target paper''s repeated-sampling
  confidence) into a genuine downstream ACTION (abstain vs. answer) with a formal
  guarantee -- but only a binary decision, no graded/communicated confidence, no deployment
  or developer-trust context, and abstract gives no concrete accuracy/coverage numbers.'
---

[2605.17029] Task Abstention for Large Language Models in Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2605.17029
(cs)
[Submitted on 16 May 2026]
Title:
Task Abstention for Large Language Models in Code Generation
Authors:
Yanke Zhou
,
Yuhao Tan
,
Senrong Xu
,
Zenan Li
,
Yuan Yao
,
Taolue Chen
,
Xiaoxing Ma
View a PDF of the paper titled Task Abstention for Large Language Models in Code Generation, by Yanke Zhou and 6 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) have revolutionized automated code generation. One serious concern, however, is the so-called ``hallucination'', i.e., LLMs may generate seemingly plausible but functionally incorrect code. In this paper, we study the task abstention problem, i.e., determining whether a given LLM should abstain from performing a specific code generation task to avoid likely hallucination. Our approach features a calibrated abstention rule, grounded in the principles of multiple hypothesis testing. The rule assesses generation consistency through code execution outcomes, allowing it to handle syntactic diversity of semantically equivalent code without reliance on oracle test cases or external databases. We prove that our approach provides a rigorous, distribution-free theoretical guarantee on its abstention decisions. We evaluate our method on benchmark datasets using several open-source code LLMs. Results show that our method allows generative models to more accurately and efficiently identify and abstain from tasks that induce hallucination compared to existing techniques, providing a reliable mechanism for safer and more robust code generation.
Comments:
17 pages, 4 figures
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2605.17029
[cs.SE]
(or
arXiv:2605.17029v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2605.17029
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Yanke Zhou [
view email
]
[v1]
Sat, 16 May 2026 14:58:11 UTC (405 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Task Abstention for Large Language Models in Code Generation, by Yanke Zhou and 6 other authors
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