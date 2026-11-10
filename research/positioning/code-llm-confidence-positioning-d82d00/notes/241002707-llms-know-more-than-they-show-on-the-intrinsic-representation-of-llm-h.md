---
title: '[2410.02707] LLMs Know More Than They Show: On the Intrinsic Representation
  of LLM Hallucinations'
id: 241002707-llms-know-more-than-they-show-on-the-intrinsic-representation-of-llm-h
tags:
- code-llm-probe-verbalize-gap-3d8995
- latent-knowledge
- truthfulness-probing
- hidden-state-probe
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-07-20T06:35:08.060283Z'
updated: '2026-11-09T23:26:03.658037Z'
source: https://arxiv.org/abs/2410.02707
source_domain: arxiv.org
fetched_at: '2026-07-20T06:35:08.058796Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Orgad, Toker, Gekhman, Reichart, Szpektor, Kotek, Belinkov (2024/2025, arXiv
  v4 May 2025). Extends the SAPLMA-style internal-truthfulness-probing line by (1)
  showing truthfulness info is concentrated in specific ''exact answer'' tokens rather
  than spread uniformly, boosting error-detection AUROC when probing those tokens;
  (2) showing probes trained on one dataset/task generalize poorly to others -- truthfulness
  encoding is task-specific/multifaceted, not a single universal ''truth direction''
  (contra earlier universalist claims incl. some readings of Burns 2022 and Azaria
  & Mitchell 2023); (3) using internal reps to predict which TYPE of error the model
  will make, not just whether it will err; and (4) most load-bearing for our lane:
  explicitly demonstrating a discrepancy between internal encoding and external behavior
  -- models can internally encode the correct answer in hidden states while consistently
  emitting an incorrect one at generation time. Domain: closed-book QA / factual recall
  benchmarks (general NLP truthfulness, e.g. entity/knowledge QA), evaluated on multiple
  open LLMs (Mistral, Llama-family per abstract-level description). Granularity: WHOLE-ANSWER
  level (probe predicts correctness of a full generated answer/final token span, not
  per-requirement or per-claim decomposition) -- there is no unit-test-like decomposition
  of a single output into independently gradable requirements. Abstract-only fetch
  (HTML full text available but not pulled; word_count 749 is the arXiv listing page,
  not the paper body).'
---

[2410.02707] LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2410.02707
(cs)
[Submitted on 3 Oct 2024 (
v1
), last revised 18 May 2025 (this version, v4)]
Title:
LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations
Authors:
Hadas Orgad
,
Michael Toker
,
Zorik Gekhman
,
Roi Reichart
,
Idan Szpektor
,
Hadas Kotek
,
Yonatan Belinkov
View a PDF of the paper titled LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations, by Hadas Orgad and 6 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) often produce errors, including factual inaccuracies, biases, and reasoning failures, collectively referred to as "hallucinations". Recent studies have demonstrated that LLMs' internal states encode information regarding the truthfulness of their outputs, and that this information can be utilized to detect errors. In this work, we show that the internal representations of LLMs encode much more information about truthfulness than previously recognized. We first discover that the truthfulness information is concentrated in specific tokens, and leveraging this property significantly enhances error detection performance. Yet, we show that such error detectors fail to generalize across datasets, implying that -- contrary to prior claims -- truthfulness encoding is not universal but rather multifaceted. Next, we show that internal representations can also be used for predicting the types of errors the model is likely to make, facilitating the development of tailored mitigation strategies. Lastly, we reveal a discrepancy between LLMs' internal encoding and external behavior: they may encode the correct answer, yet consistently generate an incorrect one. Taken together, these insights deepen our understanding of LLM errors from the model's internal perspective, which can guide future research on enhancing error analysis and mitigation.
Subjects:
Computation and Language (cs.CL)
; Artificial Intelligence (cs.AI)
MSC
classes:
68T50
ACM
classes:
I.2.7
Cite as:
arXiv:2410.02707
[cs.CL]
(or
arXiv:2410.02707v4
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2410.02707
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Hadas Orgad [
view email
]
[v1]
Thu, 3 Oct 2024 17:31:31 UTC (2,525 KB)
[v2]
Mon, 7 Oct 2024 14:46:11 UTC (2,530 KB)
[v3]
Mon, 28 Oct 2024 12:33:44 UTC (2,360 KB)
[v4]
Sun, 18 May 2025 11:18:56 UTC (2,365 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations, by Hadas Orgad and 6 other authors
View PDF
HTML (experimental)
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
2024-10
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