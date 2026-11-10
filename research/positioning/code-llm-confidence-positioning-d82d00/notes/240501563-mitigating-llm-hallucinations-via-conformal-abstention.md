---
title: '[2405.01563] Mitigating LLM Hallucinations via Conformal Abstention'
id: 240501563-mitigating-llm-hallucinations-via-conformal-abstention
tags:
- code-llm-calibration-aaai27-eabf3f
- conformal-abstention
- self-consistency
created: '2026-07-17T18:34:53.862227Z'
updated: '2026-07-17T18:36:15.062549Z'
source: https://arxiv.org/abs/2405.01563
source_domain: arxiv.org
fetched_at: '2026-07-17T18:34:53.861726Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Foundational (Google DeepMind) conformal-abstention framework: builds on
  self-consistency (sampling multiple responses and measuring their mutual similarity)
  as a more reliable confidence measure than log-probabilities, then uses the LLM
  ITSELF to self-evaluate pairwise similarity between sampled responses, and applies
  conformal prediction to convert this into an abstention rule with a rigorous theoretical
  bound on the hallucination (error) rate. On closed-book open-domain QA, the resulting
  method bounds the hallucination rate reliably while being less conservative (higher
  answering rate) than log-probability-based baselines on long-response data (Temporal
  Sequences) and comparable on short-answer data (TriviaQA). Also proposes a conformal-prediction-calibrated
  similarity threshold for automatically judging response equivalence. This is the
  closest general-domain precedent for turning a repeated-sampling/self-consistency
  confidence signal into a formally-guaranteed downstream action (abstention) with
  measured utility -- general QA only, not code, and not evaluated in a deployment/developer-trust
  context; a strong methodological template the target paper could adapt to code with
  execution-based (not LLM-judged) equivalence.'
---

*Suggested by [[260517029-task-abstention-for-large-language-models-in-code-generation]] — Foundational conformal-abstention framework for LLM hallucination mitigation, precedent for the multiple-hypothesis-testing abstention rule*

[2405.01563] Mitigating LLM Hallucinations via Conformal Abstention
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2405.01563
(cs)
[Submitted on 4 Apr 2024]
Title:
Mitigating LLM Hallucinations via Conformal Abstention
Authors:
Yasin Abbasi Yadkori
,
Ilja Kuzborskij
,
David Stutz
,
András György
,
Adam Fisch
,
Arnaud Doucet
,
Iuliya Beloshapka
,
Wei-Hung Weng
,
Yao-Yuan Yang
,
Csaba Szepesvári
,
Ali Taylan Cemgil
,
Nenad Tomasev
View a PDF of the paper titled Mitigating LLM Hallucinations via Conformal Abstention, by Yasin Abbasi Yadkori and 11 other authors
View PDF
HTML (experimental)
Abstract:
We develop a principled procedure for determining when a large language model (LLM) should abstain from responding (e.g., by saying "I don't know") in a general domain, instead of resorting to possibly "hallucinating" a non-sensical or incorrect answer. Building on earlier approaches that use self-consistency as a more reliable measure of model confidence, we propose using the LLM itself to self-evaluate the similarity between each of its sampled responses for a given query. We then further leverage conformal prediction techniques to develop an abstention procedure that benefits from rigorous theoretical guarantees on the hallucination rate (error rate). Experimentally, our resulting conformal abstention method reliably bounds the hallucination rate on various closed-book, open-domain generative question answering datasets, while also maintaining a significantly less conservative abstention rate on a dataset with long responses (Temporal Sequences) compared to baselines using log-probability scores to quantify uncertainty, while achieveing comparable performance on a dataset with short answers (TriviaQA). To evaluate the experiments automatically, one needs to determine if two responses are equivalent given a question. Following standard practice, we use a thresholded similarity function to determine if two responses match, but also provide a method for calibrating the threshold based on conformal prediction, with theoretical guarantees on the accuracy of the match prediction, which might be of independent interest.
Subjects:
Machine Learning (cs.LG)
; Artificial Intelligence (cs.AI); Computation and Language (cs.CL)
Cite as:
arXiv:2405.01563
[cs.LG]
(or
arXiv:2405.01563v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2405.01563
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Yasin Abbasi Yadkori [
view email
]
[v1]
Thu, 4 Apr 2024 11:32:03 UTC (150 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Mitigating LLM Hallucinations via Conformal Abstention, by Yasin Abbasi Yadkori and 11 other authors
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
2024-05
Change to browse by:
cs
cs.AI
cs.CL
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