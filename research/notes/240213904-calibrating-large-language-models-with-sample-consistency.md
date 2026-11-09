---
title: '[2402.13904] Calibrating Large Language Models with Sample Consistency'
id: 240213904-calibrating-large-language-models-with-sample-consistency
tags:
- aaai-bar-eval-dprc-d78e07
- calibration
- aaai-accepted-2025
- sample-consistency
- aaai-2024
- sampling-consistency
created: '2026-07-19T20:01:35.283422Z'
updated: '2026-07-19T20:04:58.303555Z'
source: https://arxiv.org/abs/2402.13904
source_domain: arxiv.org
fetched_at: '2026-07-19T20:01:35.283053Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: AAAI 2024 paper (Lyu, Shridhar, Malaviya, Zhang, Elazar, Tandon, Apidianaki,
  Sachan, Callison-Burch) deriving LLM confidence from the distribution of multiple
  randomly-sampled generations via three consistency measures, evaluated across open
  and closed-source models on nine REASONING datasets (not code). Finds consistency-based
  calibration outperforms existing post-hoc calibration approaches; intermediate explanations,
  model scaling, and larger sample counts improve calibration, while instruction-tuning
  makes calibration harder. Relevant to DPRC as the closest AAAI-accepted precedent
  for 'derive confidence from sampling distribution' (analogous to the base paper's
  internal-sampling-confidence AUROC 0.987 finding) but at whole-answer granularity
  across 9 QA/reasoning datasets, not per-requirement localization on code — underscoring
  that AAAI has already rewarded a sampling-consistency calibration paper at broad
  multi-dataset scale, raising the bar for DPRC's own dataset breadth (currently 2
  code benchmarks, TACO and BigCodeBench).
---

[2402.13904] Calibrating Large Language Models with Sample Consistency
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2402.13904
(cs)
[Submitted on 21 Feb 2024 (
v1
), last revised 23 Feb 2026 (this version, v2)]
Title:
Calibrating Large Language Models with Sample Consistency
Authors:
Qing Lyu
,
Kumar Shridhar
,
Chaitanya Malaviya
,
Li Zhang
,
Yanai Elazar
,
Niket Tandon
,
Marianna Apidianaki
,
Mrinmaya Sachan
,
Chris Callison-Burch
View a PDF of the paper titled Calibrating Large Language Models with Sample Consistency, by Qing Lyu and 8 other authors
View PDF
HTML (experimental)
Abstract:
Accurately gauging the confidence level of Large Language Models' (LLMs) predictions is pivotal for their reliable application. However, LLMs are often uncalibrated inherently and elude conventional calibration techniques due to their proprietary nature and massive scale. In this work, we explore the potential of deriving confidence from the distribution of multiple randomly sampled model generations, via three measures of consistency. We perform an extensive evaluation across various open and closed-source models on nine reasoning datasets. Results show that consistency-based calibration methods outperform existing post-hoc approaches. Meanwhile, we find that factors such as intermediate explanations, model scaling, and larger sample sizes enhance calibration, while instruction-tuning makes calibration more difficult. Moreover, confidence scores obtained from consistency have the potential to enhance model performance. Finally, we offer practical guidance on choosing suitable consistency metrics for calibration, tailored to the characteristics of various LMs.
Comments:
AAAI 2024
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2402.13904
[cs.CL]
(or
arXiv:2402.13904v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2402.13904
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Qing Lyu [
view email
]
[v1]
Wed, 21 Feb 2024 16:15:20 UTC (975 KB)
[v2]
Mon, 23 Feb 2026 07:37:56 UTC (974 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Calibrating Large Language Models with Sample Consistency, by Qing Lyu and 8 other authors
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
2024-02
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