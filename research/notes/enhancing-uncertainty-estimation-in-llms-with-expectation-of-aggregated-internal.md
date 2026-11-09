---
title: "Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal\
  \ Belief\n\t\t\t\t\t\t\t| Proceedings of the AAAI Conference on Artificial Intelligence"
id: enhancing-uncertainty-estimation-in-llms-with-expectation-of-aggregated-internal
tags:
- aaai-bar-eval-dprc-d78e07
- code-llm-probe-verbalize-gap-3d8995
created: '2026-07-19T20:05:05.347328Z'
updated: '2026-07-20T06:41:25.058906Z'
source: https://ojs.aaai.org/index.php/AAAI/article/view/40698
source_domain: ojs.aaai.org
fetched_at: '2026-07-19T20:05:05.345054Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'ACCEPTED AAAI-26 paper (AAAI-26 Technical Track on NLP V, Vol 40 No 40,
  pp.34043-34051, published 2026-03-14) -- direct comparable for DPRC''s calibration-space
  bar. EAGLE (Xiao, Dou, Xiong, Chen, Chen; Shanghai U of Finance & Economics + Southern
  U of Science & Tech) targets LLM overconfidence, especially post-RLHF. Method: self-evaluation-based
  calibration extracting internal beliefs from MULTIPLE INTERMEDIATE LAYERS (not just
  final output) during self-evaluation, aggregating layer-wise beliefs and taking
  the expectation over the resulting confidence-score distribution. Evaluated on ''diverse
  datasets and LLMs'' (plural, general QA/reasoning domain, not code) against ''existing
  baselines'' -- explicit baseline comparison is load-bearing per the abstract framing.
  Includes three separate ablation/analysis studies: (1) layer-wise examination of
  uncertainty patterns, (2) impact of self-evaluation prompt design, (3) effect of
  self-evaluation score range. Relevance to DPRC: this is what an ACCEPTED scalar/general-domain
  self-verbalized-confidence paper looks like at AAAI-26 -- multiple datasets, multiple
  base models, multiple baselines, plus 3 mechanism-probing ablations beyond the headline
  number. DPRC (single code-domain focus, in-progress on 2 datasets/1 model) is currently
  thinner on model/dataset diversity and ablation depth than this accepted bar-setter,
  though DPRC''s per-requirement localization claim is a different (more granular)
  contribution than EAGLE''s scalar aggregation.'
---

Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal Belief
							| Proceedings of the AAAI Conference on Artificial Intelligence
Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal Belief
Authors
Zeguan Xiao
Shanghai University of Finance and Economics
Diyang Dou
Shanghai University of Finance and Economics
Boya Xiong
Shanghai University of Finance and Economics
Yun Chen
Shanghai University of Finance and Economics
Guanhua Chen
Southern University of Science and Technology
DOI:
https://doi.org/10.1609/aaai.v40i40.40698
Abstract
Large Language Models (LLMs) have achieved remarkable success across a wide range of natural language tasks, but often exhibit overconfidence and generate plausible yet incorrect answers. This overconfidence, especially in models undergone Reinforcement Learning from Human Feedback (RLHF), poses significant challenges for reliable uncertainty estimation and safe deployment.
In this paper, we propose EAGLE (Expectation of AGgregated internaL bEief), a novel self-evaluation-based calibration method that leverages the internal hidden states of LLMs to derive more accurate confidence scores.
Instead of relying on the model's final output, our approach extracts internal beliefs from multiple intermediate layers during self-evaluation. By aggregating these layer-wise beliefs and calculating the expectation over the resulting confidence score distribution, EAGLE produces a refined confidence score that more faithfully reflects the model's internal certainty. Extensive experiments on diverse datasets and LLMs demonstrate that EAGLE significantly improves calibration performance over existing baselines.
We also provide an in-depth analysis of EAGLE, including a layer-wise examination of uncertainty patterns, a study of the impact of self-evaluation prompts, and an analysis of the effect of self-evaluation score range.
Downloads
PDF
Published
2026-03-14
How to Cite
Xiao, Z., Dou, D., Xiong, B., Chen, Y., & Chen, G. (2026). Enhancing Uncertainty Estimation in LLMs with Expectation of Aggregated Internal Belief.
Proceedings of the AAAI Conference on Artificial Intelligence
,
40
(40), 34043–34051. https://doi.org/10.1609/aaai.v40i40.40698
More Citation Formats
ACM
ACS
APA
ABNT
Chicago
Harvard
IEEE
MLA
Turabian
Vancouver
Download Citation
Endnote/Zotero/Mendeley (RIS)
BibTeX
Issue
Vol. 40 No. 40: AAAI-26 Technical Tracks 40
Section
AAAI Technical Track on Natural Language Processing V
Information
For Readers
For Authors
For Librarians
Part of the
PKP Publishing Services Network
Copyright © 2024, Association for the Advancement of Artificial Intelligence