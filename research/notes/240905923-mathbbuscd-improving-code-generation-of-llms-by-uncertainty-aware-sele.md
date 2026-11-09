---
title: '[2409.05923] $\mathbb{USCD}$: Improving Code Generation of LLMs by Uncertainty-Aware
  Selective Contrastive Decoding'
id: 240905923-mathbbuscd-improving-code-generation-of-llms-by-uncertainty-aware-sele
tags:
- code-llm-calibration-aaai27-eabf3f
- decoding-time-action
- contrastive-decoding
created: '2026-07-17T18:29:49.058582Z'
updated: '2026-07-17T18:31:59.243360Z'
source: http://arxiv.org/abs/2409.05923
source_domain: arxiv.org
fetched_at: '2026-07-17T18:29:49.058097Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Uncertainty-aware selective contrastive decoding (USCD) for one-pass code
  generation. Constructs a ''lame prompt'' (few-shot prompt stripped of input-output
  examples) whose output distribution approximates pure hallucination/noise; measures
  Jensen-Shannon divergence between standard-prompt TOKEN-DISTRIBUTION UNCERTAINTY
  and this noise distribution (~0.25, judged ''relatively low'' i.e. correlated),
  then selectively subtracts the lame-prompt distribution from the standard-prompt
  distribution at each token, GATED by the standard prompt''s token-level uncertainty
  (contrastive correction applied more where uncertainty is higher). Inference-only,
  plug-and-play, no retraining. Utility metric: average pass@1 increase of 16.59%
  across HumanEval, MBPP, and MultiPL-E on five code LLMs (InCoder-6B, CodeLlama-7B,
  WizardCoder-15B, StarCoder, Llama2-7B). Downstream action = decoding-time contrastive
  gating with a measured accuracy payoff, but again the gating signal is single-pass
  TOKEN uncertainty with no calibration audit (no AUROC/ECE against ground-truth correctness)
  -- it is used purely as an internal heuristic, not a signal ever exposed to or trusted
  by an end user. Notable finding: an imperfectly-calibrated uncertainty proxy can
  still be USEFUL for internal decoding decisions even where the target paper''s disconnect
  finding suggests it would fail as a human-facing confidence signal.'
---

[2409.05923] $\mathbb{USCD}$: Improving Code Generation of LLMs by Uncertainty-Aware Selective Contrastive Decoding
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2409.05923
(cs)
[Submitted on 9 Sep 2024]
Title:
$\mathbb{USCD}$: Improving Code Generation of LLMs by Uncertainty-Aware Selective Contrastive Decoding
Authors:
Shuai Wang
,
Liang Ding
,
Li Shen
,
Yong Luo
,
Zheng He
,
Wei Yu
,
Dacheng Tao
View a PDF of the paper titled $\mathbb{USCD}$: Improving Code Generation of LLMs by Uncertainty-Aware Selective Contrastive Decoding, by Shuai Wang and 6 other authors
View PDF
HTML (experimental)
Abstract:
Large language models (LLMs) have shown remarkable capabilities in code generation. However, the effects of hallucinations (e.g., output noise) make it particularly challenging for LLMs to generate high-quality code in one pass. In this work, we propose a simple and effective \textbf{u}ncertainty-aware \textbf{s}elective \textbf{c}ontrastive \textbf{d}ecoding ($\mathbb{USCD}$) mechanism to improve the quality of one-pass code generation in LLMs and reduce the impact of output noise. To be specific, we first elaborately designed a negative prompt (namely lame prompt) to output noise by removing input-output examples from the standard few-shot prompt. Our preliminary study shows that the Jensen-Shannon divergence (JS divergence) between token distribution uncertainty and the output noise is relatively low (approximately $0.25$), indicating their high relevance. Then, we selectively eliminate output noise induced by lame prompts based on the uncertainty of the prediction distribution from the standard prompt. Notably, our proposed plug-and-play mechanism is an inference-only method, enjoying appealing flexibility. Extensive experiments on widely used benchmarks, e.g., HumanEval, MBPP, and MultiPL-E, upon several LLMs (i.e., Inocder-6b, CodeLlama-7b, WizardCoder-15b, StarCoder, and Llama2-7b), demonstrate that our proposed USCD significantly improves one-pass code generation, with an average \textit{pass@$1$} scores increase of 16.59\%. We will release code and data on GitHub.
Comments:
13pages,8 figures
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2409.05923
[cs.SE]
(or
arXiv:2409.05923v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2409.05923
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Shuai Wang [
view email
]
[v1]
Mon, 9 Sep 2024 02:07:41 UTC (8,301 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled $\mathbb{USCD}$: Improving Code Generation of LLMs by Uncertainty-Aware Selective Contrastive Decoding, by Shuai Wang and 6 other authors
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
2024-09
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