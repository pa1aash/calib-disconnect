---
title: '[2603.18893] Don''t Ask: Understanding What Numeric Self-Reports Measure in
  Language Models'
id: 260318893-dont-ask-understanding-what-numeric-self-reports-measure-in-language-m
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:08:30.247266Z'
updated: '2026-11-09T23:27:43.009912Z'
source: https://arxiv.org/abs/2603.18893
source_domain: arxiv.org
fetched_at: '2026-11-09T23:08:30.246858Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '[2603.18893] Don''t Ask: Understanding What Numeric Self-Reports Measure
  in Language Models'
---

[2603.18893] Don't Ask: Understanding What Numeric Self-Reports Measure in Language Models
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2603.18893
(cs)
[Submitted on 19 Mar 2026 (
v1
), last revised 10 Oct 2026 (this version, v3)]
Title:
Don't Ask: Understanding What Numeric Self-Reports Measure in Language Models
Authors:
Nicolas Martorell
,
Bruno Bianchi
View a PDF of the paper titled Don't Ask: Understanding What Numeric Self-Reports Measure in Language Models, by Nicolas Martorell and 1 other authors
View PDF
HTML (experimental)
Abstract:
Language models are often asked to rate their internal states with a number, but it is unclear how reliable this measure is. We train probes for four affective concepts (wellbeing, interest, focus and impulsivity) in eight instruction-tuned models to track these states over multi-turn conversations. We compare each probe's score with a numeric self-report of the same state, elicited at every turn. We find that rating questions displace the probed state, and that the rating is only weakly coupled with the probe score before the question but tracks the post-question probe much more strongly. Steering experiments suggest that models use the affective directions to inform ratings, but that relationship is not specific: ratings are associated with other concepts' probes as much as with their own, and change little when the question is about the user. Finally, neither the pre-question coupling nor concept specificity improves with scale (1B-27B). We warn about the effect a question can have on the internal states one is asking about, and caution against numeric self-report as a reliable measure of those states.
Comments:
41 pages, 30 figures, 18 tables. Replaces the preprint "Quantitative Introspection in Language Models: Tracking Emotive States Across Conversation" with an extended, revised study: new title; 8 models (previously 1 in depth, 4 in less detail); 100 conversations (40 previous, 60 new); probe readouts before and after the rating question (previously only after); new controls; revised conclusions
Subjects:
Artificial Intelligence (cs.AI)
Cite as:
arXiv:2603.18893
[cs.AI]
(or
arXiv:2603.18893v3
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2603.18893
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Nicolas Martorell [
view email
]
[v1]
Thu, 19 Mar 2026 13:33:27 UTC (7,120 KB)
[v2]
Sat, 11 Apr 2026 00:08:59 UTC (7,551 KB)
[v3]
Sat, 10 Oct 2026 21:22:12 UTC (754 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Don't Ask: Understanding What Numeric Self-Reports Measure in Language Models, by Nicolas Martorell and 1 other authors
View PDF
HTML (experimental)
TeX Source
view license
Additional Features
Audio Summary
Current browse context:
cs.AI
< prev
|
next >
new
|
recent
|
2026-03
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