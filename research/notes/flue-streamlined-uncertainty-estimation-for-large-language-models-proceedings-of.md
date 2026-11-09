---
title: "FLUE: Streamlined Uncertainty Estimation for Large Language Models\n\t\t\t\
  \t\t\t\t| Proceedings of the AAAI Conference on Artificial Intelligence"
id: flue-streamlined-uncertainty-estimation-for-large-language-models-proceedings-of
tags:
- aaai-bar-eval-dprc-d78e07
- uncertainty-quantification
- aaai-2025
created: '2026-07-19T20:02:10.100221Z'
updated: '2026-07-19T20:04:33.127430Z'
source: https://ojs.aaai.org/index.php/AAAI/article/view/33840
source_domain: ojs.aaai.org
fetched_at: '2026-07-19T20:02:10.099701Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'AAAI 2025 Technical Track paper (Gao, Gong, Lin, Xu, Zhou, Li; Beihang University
  / NUS) proposing FLUE, a single-forward-pass uncertainty estimation method for open-ended
  QA that converts parameter redundancy into randomness to obtain token-level Monte
  Carlo samples without repeated inference, then learns state transitions from token-level
  to sequence-level uncertainty via post-processing. Evaluated only on open-ended
  QA (not code); demonstrates competitive uncertainty estimation with zero added inference
  cost versus multi-sample baselines. Relevant to DPRC as an example of an AAAI-accepted
  UQ paper prioritizing zero-inference-overhead as its core selling point — a dimension
  DPRC does not currently optimize for (DPRC requires priming with ''REQ <requirement>:
  <digit>'' per requirement, i.e., additional forward passes per requirement).'
---

FLUE: Streamlined Uncertainty Estimation for Large Language Models
							| Proceedings of the AAAI Conference on Artificial Intelligence
FLUE: Streamlined Uncertainty Estimation for Large Language Models
Authors
Shiqi Gao
Beihang University
Tianxiang Gong
Beihang University
Zijie Lin
National University of Singapore
Runhua Xu
Beihang University
Haoyi Zhou
Beihang University
Jianxin Li
Beihang University
DOI:
https://doi.org/10.1609/aaai.v39i16.33840
Abstract
Uncertainty estimation is essential for practical applications such as decision-making, risk assessment, and human-AI collaboration. However, Uncertainty estimation in open-ended question-answering (QA) tasks presents unique challenges. The output space for open-ended QA is vast and discrete, and the autoregressive nature of LLMs, combined with the rapid increase in model parameters, makes inference sampling significantly costly. An ideal uncertainty estimation for LLMs should meet two criteria: 1) incur no additional inference cost and 2) capture the semantic dependencies of token-level uncertainty within sequences. We propose a promising solution that converts redundancy into randomness in the extensive parameters of LLMs to quantify knowledge uncertainty. We can obtain token-level Monte Carlo samples without multiple inferences by introducing randomness during a single forward pass. We theoretically analyze the FLUE sampling method and employ a post-processing method to learn the state transitions from token uncertainty to sequence uncertainty. In open-ended question-answering tasks, we demonstrate that FLUE can achieve competitive performance in estimating the uncertainty of generated sentences without adding extra inference overhead.
Downloads
PDF
Published
2025-04-11
How to Cite
Gao, S., Gong, T., Lin, Z., Xu, R., Zhou, H., & Li, J. (2025). FLUE: Streamlined Uncertainty Estimation for Large Language Models.
Proceedings of the AAAI Conference on Artificial Intelligence
,
39
(16), 16745–16753. https://doi.org/10.1609/aaai.v39i16.33840
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
Vol. 39 No. 16: AAAI-25 Technical Tracks 16
Section
AAAI Technical Track on Machine Learning II
Information
For Readers
For Authors
For Librarians
Part of the
PKP Publishing Services Network
Copyright © 2024, Association for the Advancement of Artificial Intelligence