---
title: '[2203.11171] Self-Consistency Improves Chain of Thought Reasoning in Language
  Models'
id: 220311171-self-consistency-improves-chain-of-thought-reasoning-in-language-model
tags:
- code-llm-calibration-aaai27-eabf3f
- self-consistency
- foundational-method
created: '2026-07-17T18:33:44.658695Z'
updated: '2026-07-17T18:35:07.295993Z'
source: https://arxiv.org/abs/2203.11171
source_domain: arxiv.org
fetched_at: '2026-07-17T18:33:44.658287Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Wang, Wei, Schuurmans, Le, Chi, Narang, Chowdhery, Zhou (ICLR 2023, arXiv
  Mar 2022). The foundational self-consistency paper: replaces greedy chain-of-thought
  decoding with sampling a diverse set of reasoning paths and marginalizing to the
  most consistent final answer (majority vote over multiple sampled chains). This
  is the accuracy-improvement precursor to self-consistency-as-a-confidence-signal
  (the fraction/majority agreement across n samples is later repurposed as an uncertainty/calibration
  score in UQ work, including the paper''s own AUROC 0.987 code finding). Reports
  large accuracy gains from sampling+marginalizing versus single greedy decode: GSM8K
  +17.9%, SVAMP +11.0%, AQuA +12.2%, StrategyQA +6.4%, ARC-challenge +3.9%. Since
  self-consistency inherently requires sampling n independent generations per prompt
  and comparing them, it is the direct source of the ''n samples'' cost problem motivating
  the AAAI-27 cheap single-pass angle. Not originally proposed as a confidence/calibration
  method -- it is a decoding-time accuracy booster; its repurposing as an uncertainty
  signal (agreement rate as confidence) is a later development documented in downstream
  UQ papers.'
---

*Suggested by [[260319118-how-uncertainty-estimation-scales-with-sampling-in-reasoning-models]] — foundational self-consistency method being scaled/compared in the sample-scaling paper*

[2203.11171] Self-Consistency Improves Chain of Thought Reasoning in Language Models
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2203.11171
(cs)
[Submitted on 21 Mar 2022 (
v1
), last revised 7 Mar 2023 (this version, v4)]
Title:
Self-Consistency Improves Chain of Thought Reasoning in Language Models
Authors:
Xuezhi Wang
,
Jason Wei
,
Dale Schuurmans
,
Quoc Le
,
Ed Chi
,
Sharan Narang
,
Aakanksha Chowdhery
,
Denny Zhou
View a PDF of the paper titled Self-Consistency Improves Chain of Thought Reasoning in Language Models, by Xuezhi Wang and 7 other authors
View PDF
Abstract:
Chain-of-thought prompting combined with pre-trained large language models has achieved encouraging results on complex reasoning tasks. In this paper, we propose a new decoding strategy, self-consistency, to replace the naive greedy decoding used in chain-of-thought prompting. It first samples a diverse set of reasoning paths instead of only taking the greedy one, and then selects the most consistent answer by marginalizing out the sampled reasoning paths. Self-consistency leverages the intuition that a complex reasoning problem typically admits multiple different ways of thinking leading to its unique correct answer. Our extensive empirical evaluation shows that self-consistency boosts the performance of chain-of-thought prompting with a striking margin on a range of popular arithmetic and commonsense reasoning benchmarks, including GSM8K (+17.9%), SVAMP (+11.0%), AQuA (+12.2%), StrategyQA (+6.4%) and ARC-challenge (+3.9%).
Comments:
Published at ICLR 2023. V2: added PaLM results; V3: added UL2 results; V4: camera ready version at ICLR 2023
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2203.11171
[cs.CL]
(or
arXiv:2203.11171v4
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2203.11171
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Xuezhi Wang [
view email
]
[v1]
Mon, 21 Mar 2022 17:48:52 UTC (7,808 KB)
[v2]
Wed, 6 Apr 2022 04:40:11 UTC (12,644 KB)
[v3]
Tue, 4 Oct 2022 16:46:29 UTC (12,968 KB)
[v4]
Tue, 7 Mar 2023 17:57:37 UTC (12,751 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Self-Consistency Improves Chain of Thought Reasoning in Language Models, by Xuezhi Wang and 7 other authors
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
2022-03
Change to browse by:
cs
cs.AI
References & Citations
NASA ADS
Google Scholar
Semantic Scholar
3 blog links
(
what is this?
)
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