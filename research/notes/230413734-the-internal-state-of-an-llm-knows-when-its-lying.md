---
title: '[2304.13734] The Internal State of an LLM Knows When It''s Lying'
id: 230413734-the-internal-state-of-an-llm-knows-when-its-lying
tags:
- code-llm-calibration-aaai27-eabf3f
- internal-probing
- hidden-state-probe
- foundational
- code-llm-probe-verbalize-gap-3d8995
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-17T18:36:47.398594Z'
updated: '2026-11-09T23:28:30.488982Z'
source: https://arxiv.org/abs/2304.13734
source_domain: arxiv.org
fetched_at: '2026-07-17T18:36:47.398167Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL-TEXT (arXiv PDF extracted locally; vault note also present). Azaria
  and Mitchell SAPLMA: classifier on hidden-layer activations of OPT-6.7b and LLaMA2
  labeling statements true or false; 71% to 83% average accuracy depending on base
  model; beats few-shot prompting and sentence-probability baselines. Text-factual
  domain, not code; canonical prior for hidden-state probing (L2 background, not an
  occupant for code).'
---

*Suggested by [[model-agnostic-correctness-assessment-for-llm-generated-code-via-dynamic-interna]] — foundational hidden-state truthfulness probing paper cited by AutoProbe as prior white-box work*

[2304.13734] The Internal State of an LLM Knows When It's Lying
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2304.13734
(cs)
[Submitted on 26 Apr 2023 (
v1
), last revised 17 Oct 2023 (this version, v2)]
Title:
The Internal State of an LLM Knows When It's Lying
Authors:
Amos Azaria
,
Tom Mitchell
View a PDF of the paper titled The Internal State of an LLM Knows When It's Lying, by Amos Azaria and 1 other authors
View PDF
Abstract:
While Large Language Models (LLMs) have shown exceptional performance in various tasks, one of their most prominent drawbacks is generating inaccurate or false information with a confident tone. In this paper, we provide evidence that the LLM's internal state can be used to reveal the truthfulness of statements. This includes both statements provided to the LLM, and statements that the LLM itself generates. Our approach is to train a classifier that outputs the probability that a statement is truthful, based on the hidden layer activations of the LLM as it reads or generates the statement. Experiments demonstrate that given a set of test sentences, of which half are true and half false, our trained classifier achieves an average of 71\% to 83\% accuracy labeling which sentences are true versus false, depending on the LLM base model. Furthermore, we explore the relationship between our classifier's performance and approaches based on the probability assigned to the sentence by the LLM. We show that while LLM-assigned sentence probability is related to sentence truthfulness, this probability is also dependent on sentence length and the frequencies of words in the sentence, resulting in our trained classifier providing a more reliable approach to detecting truthfulness, highlighting its potential to enhance the reliability of LLM-generated content and its practical applicability in real-world scenarios.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG)
Cite as:
arXiv:2304.13734
[cs.CL]
(or
arXiv:2304.13734v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2304.13734
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Amos Azaria [
view email
]
[v1]
Wed, 26 Apr 2023 02:49:38 UTC (21 KB)
[v2]
Tue, 17 Oct 2023 09:34:30 UTC (58 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled The Internal State of an LLM Knows When It's Lying, by Amos Azaria and 1 other authors
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
2023-04
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