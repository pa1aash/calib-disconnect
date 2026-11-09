---
title: '[2606.29054] When Can Conformal Risk Control Certify LLM Outputs? Bounds,
  Impossibility, and Adaptation for Structured Generation'
id: 260629054-when-can-conformal-risk-control-certify-llm-outputs-bounds-impossibili
tags:
- code-llm-best-aaai-paper-6ded37
- conformal-prediction
- impossibility-result
- structured-generation-theory
created: '2026-07-20T07:42:28.777340Z'
updated: '2026-07-20T07:46:03.424178Z'
source: https://arxiv.org/abs/2606.29054
source_domain: arxiv.org
fetched_at: '2026-07-20T07:42:28.776992Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility,
  and Adaptation for Structured Generation (Kotte, solo author, arXiv:2606.29054,
  submitted 27 Jun 2026). Theory paper on the LIMITS of conformal risk control (CRC)
  for structured LLM generation (NER, JSON extraction, QA, classification -- NOT code).
  Proves a closed-form impossibility result: when base risk mu > target alpha, any
  distribution-free method must abstain on at least (mu-alpha)/(1-alpha) examples
  -- a feasibility pre-check before running CRC. Builds a certification hierarchy
  (Hoeffding -> empirical-Bernstein -> betting-based e-CRC): Bernstein gives the largest
  gain (+37% certified configs), e-CRC helps when calibration data is scarce (10%
  certification at 20% data vs 0% for Hoeffding). Validates adaptive conformal inference
  under distribution shift, cutting risk-target violations from 71% to 21%. Tested
  on 6 open-weight models (3B-72B), 8 datasets, 4 tasks, 6 nonconformity scores; hard
  configs uncertifiable at alpha=0.10 but 40-60% certifiable at alpha=0.30-0.40. Relevant
  theoretical machinery (feasibility test, bound hierarchy) for a per-requirement
  risk-control theorem, and a template for the rigor/honesty bar such a paper needs,
  but never touches code or requirement decomposition.'
---

[2606.29054] When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Machine Learning
arXiv:2606.29054
(cs)
[Submitted on 27 Jun 2026]
Title:
When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation
Authors:
Varun Kotte
View a PDF of the paper titled When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation, by Varun Kotte
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) deployed for structured generation (NER, JSON extraction, QA, and classification) lack formal reliability guarantees, and standard heuristic abstention policies miss user-specified risk targets by 7.5--12.5%. We characterize when conformal risk control (CRC) can certify structured LLM outputs and when it provably cannot. First, we prove an impossibility result: when the base risk (\mu > \alpha), any distribution-free method must abstain on at least ((\mu-\alpha)/(1-\alpha)) examples, yielding a closed-form feasibility test: one can check whether CRC will work before running it. Second, we analyze a certification hierarchy across Hoeffding, empirical Bernstein, and a betting-based e-CRC bound, with strict gains in low-variance/large-sample regimes: the Hoeffding-to-Bernstein step delivers the largest gain (+37% certified configurations), while e-CRC adds value when calibration data is scarce (10% certification at 20% data versus 0% for Hoeffding). Third, we validate adaptive conformal inference (ACI) under cross-dataset shift, reducing risk-target violations from 71% to 21%, with residual failures concentrated exactly where the impossibility bound predicts. Across six open-weight models (3B--72B parameters), eight datasets, four tasks, and six nonconformity scores, hard NER/QA/CLS configurations are uncertifiable at (\alpha = 0.10); relaxing to (\alpha = 0.30--0.40) unlocks practical certification (47% NER, 40% QA, 60% CLS). The framework gives a three-step deployment recipe: check feasibility, select the bound and score, then mitigate shift.
Subjects:
Machine Learning (cs.LG)
Cite as:
arXiv:2606.29054
[cs.LG]
(or
arXiv:2606.29054v1
[cs.LG]
for this version)
https://doi.org/10.48550/arXiv.2606.29054
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Varun Kotte [
view email
]
[v1]
Sat, 27 Jun 2026 19:25:07 UTC (49 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation for Structured Generation, by Varun Kotte
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
2026-06
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