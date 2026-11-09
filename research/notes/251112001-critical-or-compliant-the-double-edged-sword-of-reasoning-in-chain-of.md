---
title: '[2511.12001] Critical or Compliant? The Double-Edged Sword of Reasoning in
  Chain-of-Thought Explanations'
id: 251112001-critical-or-compliant-the-double-edged-sword-of-reasoning-in-chain-of
tags:
- code-llm-calibration-aaai27-eabf3f
- human-trust
- confirmation-bias
created: '2026-07-17T18:30:57.428444Z'
updated: '2026-07-17T18:31:52.638154Z'
source: http://arxiv.org/abs/2511.12001
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:57.427927Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Park et al. (under review, 16pp/15figs) study the downstream human-trust
  effects of Chain-of-Thought explanations in multimodal moral-reasoning scenarios
  via a user study with systematically perturbed reasoning chains and manipulated
  delivery tone (confident vs. hedged). Two key findings: (1) users conflate trust
  with outcome agreement -- they keep relying on the explanation even when the underlying
  reasoning is flawed, so long as the output ''looks right''; (2) a CONFIDENT DELIVERY
  TONE suppresses users'' ability to detect reasoning errors while sustaining reliance,
  i.e., surface confidence style overrides actual correctness in shaping human trust.
  This is not about model-internal calibration metrics but about the human-facing
  consequence: even a well-calibrated confidence signal could be misused or a poorly-calibrated
  one could still drive trust if delivered confidently. Directly supports the ''human-trust
  downstream'' arm of the adversarial lens -- calibration metrics (AUROC/ECE) may
  not predict whether users actually calibrate their trust appropriately, especially
  in code-generation contexts where users often cannot verify correctness themselves.'
---

[2511.12001] Critical or Compliant? The Double-Edged Sword of Reasoning in Chain-of-Thought Explanations
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2511.12001
(cs)
[Submitted on 15 Nov 2025 (
v1
), last revised 19 Nov 2025 (this version, v2)]
Title:
Critical or Compliant? The Double-Edged Sword of Reasoning in Chain-of-Thought Explanations
Authors:
Eunkyu Park
,
Wesley Hanwen Deng
,
Vasudha Varadarajan
,
Mingxi Yan
,
Gunhee Kim
,
Maarten Sap
,
Motahhare Eslami
View a PDF of the paper titled Critical or Compliant? The Double-Edged Sword of Reasoning in Chain-of-Thought Explanations, by Eunkyu Park and 6 other authors
View PDF
HTML (experimental)
Abstract:
Explanations are often promoted as tools for transparency, but they can also foster confirmation bias; users may assume reasoning is correct whenever outputs appear acceptable. We study this double-edged role of Chain-of-Thought (CoT) explanations in multimodal moral scenarios by systematically perturbing reasoning chains and manipulating delivery tones. Specifically, we analyze reasoning errors in vision language models (VLMs) and how they impact user trust and the ability to detect errors. Our findings reveal two key effects: (1) users often equate trust with outcome agreement, sustaining reliance even when reasoning is flawed, and (2) the confident tone suppresses error detection while maintaining reliance, showing that delivery styles can override correctness. These results highlight how CoT explanations can simultaneously clarify and mislead, underscoring the need for NLP systems to provide explanations that encourage scrutiny and critical thinking rather than blind trust. All code will be released publicly.
Comments:
Under review; 16 pages, 15 figures
Subjects:
Computation and Language (cs.CL)
; Human-Computer Interaction (cs.HC)
Cite as:
arXiv:2511.12001
[cs.CL]
(or
arXiv:2511.12001v2
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2511.12001
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Eunkyu Park [
view email
]
[v1]
Sat, 15 Nov 2025 02:38:49 UTC (3,343 KB)
[v2]
Wed, 19 Nov 2025 05:49:39 UTC (4,490 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Critical or Compliant? The Double-Edged Sword of Reasoning in Chain-of-Thought Explanations, by Eunkyu Park and 6 other authors
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
2025-11
Change to browse by:
cs
cs.HC
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