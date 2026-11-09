---
title: '[2306.13063] Can LLMs Express Their Uncertainty? An Empirical Evaluation of
  Confidence Elicitation in LLMs'
id: 230613063-can-llms-express-their-uncertainty-an-empirical-evaluation-of-confiden
tags:
- code-llm-calibration-aaai27-eabf3f
- verbal-confidence-failure
- protocol-sensitivity
- verbalized-confidence
- black-box-uq
- foundational-method
created: '2026-07-17T18:33:38.145419Z'
updated: '2026-07-17T18:35:17.481920Z'
source: https://arxiv.org/abs/2306.13063
source_domain: arxiv.org
fetched_at: '2026-07-17T18:33:38.144996Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Xiong, Hu, Lu, Li, Fu, He, Hooi (ICLR 2024, arXiv Jun 2023). Systematic
  black-box confidence-elicitation framework with three components: verbalize-based
  prompting, sampling-based consistency, and aggregation techniques. Benchmarks across
  5 dataset types (commonsense/arithmetic reasoning etc.) and 5 LLMs including GPT-4
  and LLaMA 2 Chat, on two tasks: confidence calibration and failure prediction. Key
  findings load-bearing for the AAAI-27 angle: (1) LLMs are overconfident when verbalizing
  confidence, mimicking human overconfidence patterns; (2) calibration and failure-prediction
  performance improve as model capability scales; (3) consistency-based (sampling)
  methods outperform verbalized confidence in most cases, but hybrid strategies combining
  both perform best; (4) white-box methods (using internal model info) only narrowly
  beat black-box methods -- AUROC 0.605 vs 0.522 -- suggesting the gap between cheap
  black-box signals and expensive/internal signals may be small; (5) no single technique
  consistently wins, and ALL methods struggle on tasks requiring professional/specialized
  knowledge (directly relevant caveat for code, a professional-knowledge domain).
  This paper is the source for the ''verbalized confidence'' signal used as a comparison
  point in the sample-scaling study (2603.19118) and establishes the white-box-vs-black-box
  AUROC gap benchmark (0.522 to 0.605) that a code-specific cheap single-pass method
  should be measured against.'
---

*Suggested by [[260319118-how-uncertainty-estimation-scales-with-sampling-in-reasoning-models]] — verbalized confidence baseline compared against self-consistency*

*Suggested by [[260527752-asking-is-not-enough-protocol-sensitivity-in-llm-confidence-calibratio]] — original verbalized-confidence elicitation protocol paper being critiqued*

[2306.13063] Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2306.13063
(cs)
[Submitted on 22 Jun 2023 (
v1
), last revised 17 Mar 2024 (this version, v2)]
Title:
Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs
Authors:
Miao Xiong
,
Zhiyuan Hu
,
Xinyang Lu
,
Yifei Li
,
Jie Fu
,
Junxian He
,
Bryan Hooi
View a PDF of the paper titled Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs, by Miao Xiong and 6 other authors
View PDF
HTML (experimental)
Abstract:
Empowering large language models to accurately express confidence in their answers is essential for trustworthy decision-making. Previous confidence elicitation methods, which primarily rely on white-box access to internal model information or model fine-tuning, have become less suitable for LLMs, especially closed-source commercial APIs. This leads to a growing need to explore the untapped area of black-box approaches for LLM uncertainty estimation. To better break down the problem, we define a systematic framework with three components: prompting strategies for eliciting verbalized confidence, sampling methods for generating multiple responses, and aggregation techniques for computing consistency. We then benchmark these methods on two key tasks-confidence calibration and failure prediction-across five types of datasets (e.g., commonsense and arithmetic reasoning) and five widely-used LLMs including GPT-4 and LLaMA 2 Chat. Our analysis uncovers several key insights: 1) LLMs, when verbalizing their confidence, tend to be overconfident, potentially imitating human patterns of expressing confidence. 2) As model capability scales up, both calibration and failure prediction performance improve. 3) Employing our proposed strategies, such as human-inspired prompts, consistency among multiple responses, and better aggregation strategies can help mitigate this overconfidence from various perspectives. 4) Comparisons with white-box methods indicate that while white-box methods perform better, the gap is narrow, e.g., 0.522 to 0.605 in AUROC. Despite these advancements, none of these techniques consistently outperform others, and all investigated methods struggle in challenging tasks, such as those requiring professional knowledge, indicating significant scope for improvement. We believe this study can serve as a strong baseline and provide insights for eliciting confidence in black-box LLMs.
Comments:
The paper is accepted by ICLR 2024. The code is publicly available at
this https URL
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2306.13063
[cs.CL]
(or
arXiv:2306.13063v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2306.13063
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Miao Xiong [
view email
]
[v1]
Thu, 22 Jun 2023 17:31:44 UTC (1,653 KB)
[v2]
Sun, 17 Mar 2024 04:38:48 UTC (675 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs, by Miao Xiong and 6 other authors
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
2023-06
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