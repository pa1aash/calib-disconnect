---
title: '[2507.00057] Incoherence as Oracle-less Measure of Error in LLM-Based Code
  Generation'
id: 250700057-incoherence-as-oracle-less-measure-of-error-in-llm-based-code-generati
tags:
- aaai-bar-eval-dprc-d78e07
- code-llm
- oracle-less-evaluation
- aaai-2026
created: '2026-07-19T20:02:06.763150Z'
updated: '2026-07-19T20:04:31.852120Z'
source: https://arxiv.org/abs/2507.00057
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:06.762820Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'AAAI 2026 main-track paper (Valentin, Madadi, Sapia, Böhme) proposing ''incoherence''
  as an oracle-less measure of LLM code-generation error: without any correct reference
  implementation or test oracle, they estimate a lower bound on the probability that
  an LLM-generated program is incorrect, purely from properties of the model''s own
  generation distribution. Incoherence-based detection automatically identifies about
  two-thirds of incorrect programs with no reported false positives on the average
  task, and LLM rankings by pass@1 (oracle-based) closely match LLM rankings by incoherence
  (oracle-less), suggesting oracle-based evaluation can be reliably replaced. This
  is the closest AAAI-accepted analog to DPRC''s self-expressed confidence angle:
  both estimate per-program/per-requirement correctness probability from internal
  model signal without ground truth at inference time, but Incoherence targets a binary
  whole-program correctness estimate (not per-requirement localization) and is training-free
  (no fine-tuning), whereas DPRC trains the model via LoRA to self-express calibrated
  per-requirement digits.'
---

[2507.00057] Incoherence as Oracle-less Measure of Error in LLM-Based Code Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Programming Languages
arXiv:2507.00057
(cs)
[Submitted on 26 Jun 2025 (
v1
), last revised 13 Dec 2025 (this version, v2)]
Title:
Incoherence as Oracle-less Measure of Error in LLM-Based Code Generation
Authors:
Thomas Valentin
,
Ardi Madadi
,
Gaetano Sapia
,
Marcel Böhme
View a PDF of the paper titled Incoherence as Oracle-less Measure of Error in LLM-Based Code Generation, by Thomas Valentin and 3 other authors
View PDF
HTML (experimental)
Abstract:
Generating code from a natural language programming task is one of the most successful applications of Large Language Models (LLMs). Yet, the generated program may be buggy. Without an oracle, such as an existing, correct implementation or a formal specification, can we somehow estimate how likely the generated program is correct?
In this paper, we propose a measure of incorrectness, called *incoherence*, that can be estimated efficiently in the absence of an oracle and allows us to establish a lower bound on the error, i.e., the probability that the LLM-generated program for that specification is incorrect. In our experiments, our incoherence-based methodology can automatically identify about two-thirds of incorrect programs without reports of false positives for the average task. In fact, *an oracle-based evaluation of LLMs can be reliably replaced by an incoherence-based evaluation*. In particular, we find a very strong agreement between the ranking of LLMs by the number of programs deemed correct via an oracle (pass@1) and the ranking of LLMs by the number of programs deemed correct via incoherence.
Comments:
Accepted at AAAI'26 (extended version). 8 pages + refs and appendix
Subjects:
Programming Languages (cs.PL)
; Artificial Intelligence (cs.AI); Machine Learning (cs.LG); Software Engineering (cs.SE)
Cite as:
arXiv:2507.00057
[cs.PL]
(or
arXiv:2507.00057v2
[cs.PL]
for this version)
https://doi.org/10.48550/arXiv.2507.00057
Focus to learn more
arXiv-issued DOI via DataCite
Journal reference:
40th Annual AAAI Conference on Artificial Intelligence (AAAI), 2026
Submission history
From: Marcel Böhme [
view email
]
[v1]
Thu, 26 Jun 2025 22:00:50 UTC (3,808 KB)
[v2]
Sat, 13 Dec 2025 19:27:44 UTC (3,809 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Incoherence as Oracle-less Measure of Error in LLM-Based Code Generation, by Thomas Valentin and 3 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.PL
< prev
|
next >
new
|
recent
|
2025-07
Change to browse by:
cs
cs.AI
cs.LG
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