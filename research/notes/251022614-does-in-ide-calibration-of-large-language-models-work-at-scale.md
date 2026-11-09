---
title: '[2510.22614] Does In-IDE Calibration of Large Language Models work at Scale?'
id: 251022614-does-in-ide-calibration-of-large-language-models-work-at-scale
tags:
- code-llm-calibration-aaai27-eabf3f
- in-ide-deployment
- developer-trust
- post-hoc-calibration
created: '2026-07-17T18:29:35.184597Z'
updated: '2026-07-17T18:31:46.026526Z'
source: http://arxiv.org/abs/2510.22614
source_domain: arxiv.org
fetched_at: '2026-07-17T18:29:35.183490Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Large-scale real-deployment study (24M+ real developer interactions, multiple
  languages) testing whether post-hoc Platt-scaling calibration of code-model confidence
  aligns with actual DEVELOPER ACCEPTANCE behavior in an IDE. Finds that a general
  population-level post-hoc calibrator does NOT, on average, improve reliability/alignment
  of confidence signals; dynamic per-user personalized calibration can work but its
  effectiveness depends heavily on volume of that user's interaction history (cold-start
  problem). A parallel multi-phase design study (3 expert designers, 153 professional
  developers; scenario-based design + interviews + survey) finds a clear preference
  for non-numerical, color-coded reliability indicators over numeric confidence scores
  in the editor workflow. Uses single-pass token confidence + Platt scaling as the
  underlying signal -- never tests whether a repeated-sampling/self-consistency confidence
  signal (the near-perfectly-calibrated signal type) would fare better at this real
  deployment scale. Directly extends the target paper's expressed-interface disconnect
  finding to a live, large-N deployment context and to a different downstream metric
  (developer acceptance, not correctness), while leaving the sampling-based-signal
  question completely open -- a strong candidate gap for the new paper to occupy.
---

[2510.22614] Does In-IDE Calibration of Large Language Models work at Scale?
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2510.22614
(cs)
[Submitted on 26 Oct 2025]
Title:
Does In-IDE Calibration of Large Language Models work at Scale?
Authors:
Roham Koohestani
,
Agnia Sergeyuk
,
David Gros
,
Claudio Spiess
,
Sergey Titov
,
Prem Devanbu
,
Maliheh Izadi
View a PDF of the paper titled Does In-IDE Calibration of Large Language Models work at Scale?, by Roham Koohestani and 6 other authors
View PDF
HTML (experimental)
Abstract:
The introduction of large language models into integrated development environments (IDEs) is revolutionizing software engineering, yet it poses challenges to the usefulness and reliability of Artificial Intelligence-generated code. Post-hoc calibration of internal model confidences aims to align probabilities with an acceptability measure. Prior work suggests calibration can improve alignment, but at-scale evidence is limited. In this work, we investigate the feasibility of applying calibration of code models to an in-IDE context. We study two aspects of the problem: (1) the technical method for implementing confidence calibration and improving the reliability of code generation models, and (2) the human-centered design principles for effectively communicating reliability signal to developers. First, we develop a scalable and flexible calibration framework which can be used to obtain calibration weights for open-source models using any dataset, and evaluate whether calibrators improve the alignment between model confidence and developer acceptance behavior. Through a large-scale analysis of over 24 million real-world developer interactions across multiple programming languages, we find that a general, post-hoc calibration model based on Platt-scaling does not, on average, improve the reliability of model confidence signals. We also find that while dynamically personalizing calibration to individual users can be effective, its effectiveness is highly dependent on the volume of user interaction data. Second, we conduct a multi-phase design study with 3 expert designers and 153 professional developers, combining scenario-based design, semi-structured interviews, and survey validation, revealing a clear preference for presenting reliability signals via non-numerical, color-coded indicators within the in-editor code generation workflow.
Comments:
Under Review
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2510.22614
[cs.SE]
(or
arXiv:2510.22614v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2510.22614
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Roham Koohestani [
view email
]
[v1]
Sun, 26 Oct 2025 10:15:03 UTC (1,082 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Does In-IDE Calibration of Large Language Models work at Scale?, by Roham Koohestani and 6 other authors
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.SE
< prev
|
next >
new
|
recent
|
2025-10
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