---
title: '[2304.15004] Are Emergent Abilities of Large Language Models a Mirage?'
id: 230415004-are-emergent-abilities-of-large-language-models-a-mirage
tags:
- aaai-bar-eval-dprc-d78e07
- negative-results
- scope-condition
- neurips-outstanding-paper
created: '2026-07-19T20:04:54.178585Z'
updated: '2026-07-19T20:06:54.020055Z'
source: https://arxiv.org/abs/2304.15004
source_domain: arxiv.org
fetched_at: '2026-07-19T20:04:54.178192Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Schaeffer, Miranda, Koyejo (Stanford), NeurIPS 2023 Outstanding Paper Award
  (submitted arXiv Apr 2023, published proceedings.neurips.cc). Canonical example
  of a scope/boundary-condition finding accepted -- and specifically honored -- at
  a top-tier ML venue: the paper does not propose a new method but instead shows that
  a widely-believed phenomenon (emergent abilities of LLMs -- sharp, unpredictable
  capability jumps with scale) is largely an artifact of the researcher''s METRIC
  CHOICE rather than a fundamental property of scaling. Nonlinear/discontinuous metrics
  (e.g., exact-match accuracy) manufacture apparent sharp emergence; linear/continuous
  metrics (e.g., token-edit-distance, cross-entropy) reveal smooth, predictable improvement
  on the same underlying model outputs. The authors make and confirm testable predictions
  across three complementary analyses: (1) InstructGPT/GPT-3 family on tasks with
  claimed emergent abilities, (2) a meta-analysis of BIG-Bench emergent-ability claims,
  (3) deliberately manufacturing ''emergent abilities'' in vision tasks by choice
  of metric alone. Directly load-bearing for DPRC''s framing question: this is hard
  proof that a ''when does phenomenon X actually appear vs when is it an artifact
  of measurement/evaluation choice'' contribution -- with NO new method, just a mechanistic
  re-explanation of when/why an effect appears -- is not just accepted but can win
  the top award at a top-tier ML venue, provided the paper (a) makes and confirms
  falsifiable predictions, and (b) explains the underlying MECHANISM (metric nonlinearity)
  rather than just reporting the works-here/fails-there contrast.'
---

[2304.15004] Are Emergent Abilities of Large Language Models a Mirage?
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2304.15004
(cs)
[Submitted on 28 Apr 2023 (
v1
), last revised 22 May 2023 (this version, v2)]
Title:
Are Emergent Abilities of Large Language Models a Mirage?
Authors:
Rylan Schaeffer
,
Brando Miranda
,
Sanmi Koyejo
View a PDF of the paper titled Are Emergent Abilities of Large Language Models a Mirage?, by Rylan Schaeffer and 2 other authors
View PDF
Abstract:
Recent work claims that large language models display emergent abilities, abilities not present in smaller-scale models that are present in larger-scale models. What makes emergent abilities intriguing is two-fold: their sharpness, transitioning seemingly instantaneously from not present to present, and their unpredictability, appearing at seemingly unforeseeable model scales. Here, we present an alternative explanation for emergent abilities: that for a particular task and model family, when analyzing fixed model outputs, emergent abilities appear due to the researcher's choice of metric rather than due to fundamental changes in model behavior with scale. Specifically, nonlinear or discontinuous metrics produce apparent emergent abilities, whereas linear or continuous metrics produce smooth, continuous predictable changes in model performance. We present our alternative explanation in a simple mathematical model, then test it in three complementary ways: we (1) make, test and confirm three predictions on the effect of metric choice using the InstructGPT/GPT-3 family on tasks with claimed emergent abilities; (2) make, test and confirm two predictions about metric choices in a meta-analysis of emergent abilities on BIG-Bench; and (3) show to choose metrics to produce never-before-seen seemingly emergent abilities in multiple vision tasks across diverse deep networks. Via all three analyses, we provide evidence that alleged emergent abilities evaporate with different metrics or with better statistics, and may not be a fundamental property of scaling AI models.
Subjects:
Artificial Intelligence (cs.AI)
; Machine Learning (cs.LG)
Cite as:
arXiv:2304.15004
[cs.AI]
(or
arXiv:2304.15004v2
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2304.15004
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Rylan Schaeffer [
view email
]
[v1]
Fri, 28 Apr 2023 17:52:11 UTC (20,235 KB)
[v2]
Mon, 22 May 2023 15:56:25 UTC (20,235 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Are Emergent Abilities of Large Language Models a Mirage?, by Rylan Schaeffer and 2 other authors
View PDF
TeX Source
view license
Current browse context:
cs.AI
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
cs.LG
References & Citations
NASA ADS
Google Scholar
Semantic Scholar
2 blog links
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