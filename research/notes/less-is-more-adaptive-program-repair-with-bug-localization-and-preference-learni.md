---
title: "Less Is More: Adaptive Program Repair with Bug Localization and Preference\
  \ Learning\n\t\t\t\t\t\t\t| Proceedings of the AAAI Conference on Artificial Intelligence"
id: less-is-more-adaptive-program-repair-with-bug-localization-and-preference-learni
tags:
- aaai-bar-eval-dprc-d78e07
- calibration
- aaai-accepted-2025
- code-llm
- bug-localization
- track-placement-signal
- code-llm-probe-verbalize-gap-3d8995
created: '2026-07-19T20:08:13.437873Z'
updated: '2026-07-20T06:38:10.780804Z'
source: https://ojs.aaai.org/index.php/AAAI/article/view/31988
source_domain: ojs.aaai.org
fetched_at: '2026-07-19T20:08:13.437527Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'AAAI proceedings page (not arXiv) for the AdaPatcher paper: confirms it
  published in Proceedings of the AAAI Conference on Artificial Intelligence, Vol
  39, No 1 (AAAI-25 Technical Tracks 1), pages 128-136, under the ''AAAI Technical
  Track on Application Domains'' (not the ML or NLP track) -- useful track-placement
  signal: an AAAI-accepted code-localization + repair paper landed in Application
  Domains rather than core ML/UQ tracks, suggesting DPRC (a code-domain calibration
  paper) could plausibly target Application Domains as well as the ML/UQ track depending
  on framing. Authors: Zhejiang University + collaborators. Page does not surface
  the full results table (67.57% accuracy figure found via secondary web search, not
  verified verbatim in this fetch) -- the primary PDF itself was not directly fetchable
  through this route; exact numeric tables remain in the PDF download, not the HTML
  abstract page.'
---

*Suggested by [[250306510-less-is-more-adaptive-program-repair-with-bug-localization-and-prefere]] — primary AAAI proceedings page for exact metrics/baseline table missing from arXiv abstract*

Less Is More: Adaptive Program Repair with Bug Localization and Preference Learning
							| Proceedings of the AAAI Conference on Artificial Intelligence
Less Is More: Adaptive Program Repair with Bug Localization and Preference Learning
Authors
Zhenlong Dai
Zhejiang University
Hangzhou High-Tech Zone (Binjiang) Institute of Blockchain and Data Security
Bingrui Chen
Hohai University
Zhuoluo Zhao
Guizhou University
Xiu Tang
Zhejiang University
Hangzhou High-Tech Zone (Binjiang) Institute of Blockchain and Data Security
Sai Wu
Zhejiang University
Hangzhou High-Tech Zone (Binjiang) Institute of Blockchain and Data Security
Chang Yao
Zhejiang University
Hangzhou High-Tech Zone (Binjiang) Institute of Blockchain and Data Security
Zhipeng Gao
Zhejiang University
Jingyuan Chen
Zhejiang University
DOI:
https://doi.org/10.1609/aaai.v39i1.31988
Abstract
Automated Program Repair (APR) is a task to automatically generate patches for the buggy code. However, most research focuses on generating correct patches while ignoring the consistency between the fixed code and the original buggy code. How to conduct adaptive bug fixing and generate patches with minimal modifications have seldom been investigated. To bridge this gap, we first introduce a novel task, namely AdaPR (Adaptive Program Repair). We then propose a two-stage approach AdaPatcher (Adaptive Patch Generator) to enhance program repair while maintaining the consistency. In the first stage, we utilize a Bug Locator with self-debug learning to accurately pinpoint bug locations. In the second stage, we train a Program Modifier to ensure consistency between the post-modified fixed code and the pre-modified buggy code. The Program Modifier is enhanced with a location-aware repair learning strategy to generate patches based on identified buggy lines, a hybrid training strategy for selective reference and an adaptive preference learning to prioritize fewer changes. 
The experimental results show that our approach outperforms a set of baselines by a large margin, validating the effectiveness of our two-stage framework for the newly proposed AdaPR task.
Downloads
PDF
Video/Poster/Slides
Published
2025-04-11
How to Cite
Dai, Z., Chen, B., Zhao, Z., Tang, X., Wu, S., Yao, C., … Chen, J. (2025). Less Is More: Adaptive Program Repair with Bug Localization and Preference Learning.
Proceedings of the AAAI Conference on Artificial Intelligence
,
39
(1), 128–136. https://doi.org/10.1609/aaai.v39i1.31988
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
Vol. 39 No. 1: AAAI-25 Technical Tracks 1
Section
AAAI Technical Track on Application Domains
Information
For Readers
For Authors
For Librarians
Part of the
PKP Publishing Services Network
Copyright © 2024, Association for the Advancement of Artificial Intelligence