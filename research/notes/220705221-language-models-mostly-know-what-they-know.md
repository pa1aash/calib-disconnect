---
title: '[2207.05221] Language Models (Mostly) Know What They Know'
id: 220705221-language-models-mostly-know-what-they-know
tags:
- code-llm-calibration-aaai27-eabf3f
- verbalized-confidence
- p-true-self-evaluation
created: '2026-07-17T18:37:32.288004Z'
updated: '2026-07-17T18:38:51.189988Z'
source: https://arxiv.org/abs/2207.05221
source_domain: arxiv.org
fetched_at: '2026-07-17T18:37:32.287448Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Kadavath et al. (Anthropic), 2022 (arXiv:2207.05221). Foundational paper
  on LLM self-evaluation/verbalized confidence, directly cited by Spiess et al. as
  prior work on reflective confidence measures. Shows larger LLMs are well-calibrated
  on multiple-choice/true-false questions when prompted in the right format, and that
  models can self-evaluate open-ended answers via a 'P(True)' probability -- asking
  the model to propose an answer then estimate the probability that its own answer
  is correct -- with performance improving further when the model considers multiple
  of its own samples before judging validity. Also introduces 'P(IK)' (probability
  I Know), a confidence estimate trained without reference to any specific proposed
  answer; P(IK) partially generalizes across tasks but the paper explicitly notes
  it struggles with calibration on genuinely new/held-out tasks. P(IK) increases appropriately
  with relevant context or hints. This paper is the direct ancestor of the 'reflective'/verbalized
  confidence measures (p_v, self-ask) that Spiess et al. test on code generation and
  find largely uncorrelated with logit-based intrinsic measures -- the disconnect
  paper's likely novelty angle is that Kadavath's optimistic 'LLMs mostly know what
  they know' finding (on general QA/multiple-choice) does not transfer to code correctness
  judgments, where Spiess shows both intrinsic and reflective measures are poorly
  calibrated out of the box.
---

*Suggested by [[calibration-and-correctness-of-language-models-for-code]] — foundational paper on LLM verbalized/reflective self-confidence, cited by Spiess as key prior work on whether LLMs know what they know*

[2207.05221] Language Models (Mostly) Know What They Know
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2207.05221
(cs)
[Submitted on 11 Jul 2022 (
v1
), last revised 21 Nov 2022 (this version, v4)]
Title:
Language Models (Mostly) Know What They Know
Authors:
Saurav Kadavath
,
Tom Conerly
,
Amanda Askell
,
Tom Henighan
,
Dawn Drain
,
Ethan Perez
,
Nicholas Schiefer
,
Zac Hatfield-Dodds
,
Nova DasSarma
,
Eli Tran-Johnson
,
Scott Johnston
,
Sheer El-Showk
,
Andy Jones
,
Nelson Elhage
,
Tristan Hume
,
Anna Chen
,
Yuntao Bai
,
Sam Bowman
,
Stanislav Fort
,
Deep Ganguli
,
Danny Hernandez
,
Josh Jacobson
,
Jackson Kernion
,
Shauna Kravec
,
Liane Lovitt
,
Kamal Ndousse
,
Catherine Olsson
,
Sam Ringer
,
Dario Amodei
,
Tom Brown
,
Jack Clark
,
Nicholas Joseph
,
Ben Mann
,
Sam McCandlish
,
Chris Olah
,
Jared Kaplan
View a PDF of the paper titled Language Models (Mostly) Know What They Know, by Saurav Kadavath and 35 other authors
View PDF
Abstract:
We study whether language models can evaluate the validity of their own claims and predict which questions they will be able to answer correctly. We first show that larger models are well-calibrated on diverse multiple choice and true/false questions when they are provided in the right format. Thus we can approach self-evaluation on open-ended sampling tasks by asking models to first propose answers, and then to evaluate the probability "P(True)" that their answers are correct. We find encouraging performance, calibration, and scaling for P(True) on a diverse array of tasks. Performance at self-evaluation further improves when we allow models to consider many of their own samples before predicting the validity of one specific possibility. Next, we investigate whether models can be trained to predict "P(IK)", the probability that "I know" the answer to a question, without reference to any particular proposed answer. Models perform well at predicting P(IK) and partially generalize across tasks, though they struggle with calibration of P(IK) on new tasks. The predicted P(IK) probabilities also increase appropriately in the presence of relevant source materials in the context, and in the presence of hints towards the solution of mathematical word problems. We hope these observations lay the groundwork for training more honest models, and for investigating how honesty generalizes to cases where models are trained on objectives other than the imitation of human writing.
Comments:
23+17 pages; refs added, typos fixed
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2207.05221
[cs.CL]
(or
arXiv:2207.05221v4
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2207.05221
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Jared Kaplan [
view email
]
[v1]
Mon, 11 Jul 2022 22:59:39 UTC (1,249 KB)
[v2]
Wed, 13 Jul 2022 18:36:41 UTC (1,249 KB)
[v3]
Sat, 16 Jul 2022 15:24:01 UTC (1,251 KB)
[v4]
Mon, 21 Nov 2022 16:38:35 UTC (1,252 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Language Models (Mostly) Know What They Know, by Saurav Kadavath and 35 other authors
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
2022-07
Change to browse by:
cs
cs.AI
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