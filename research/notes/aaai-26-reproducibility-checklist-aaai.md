---
title: AAAI-26 Reproducibility Checklist - AAAI
id: aaai-26-reproducibility-checklist-aaai
tags:
- aaai-bar-eval-dprc-d78e07
- reproducibility-checklist
- significance-testing-required
created: '2026-07-19T20:10:47.195705Z'
updated: '2026-07-19T20:11:25.302380Z'
source: https://web.archive.org/web/2026/https://aaai.org/conference/aaai/aaai-26/reproducibility-checklist/
source_domain: web.archive.org
fetched_at: '2026-07-19T20:10:47.195320Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'AAAI-26 official Reproducibility Checklist (Wayback capture; answered inline
  in every submission''s appendix, ''yes'' expected as default). MOST DIRECTLY LOAD-BEARING
  primary source found for the rigor-expectation half of this query. Mandatory checklist
  items with direct bearing on the DPRC AAAI-27 bar: ''This paper states the number
  of algorithm runs used to compute each reported result'' (yes/no, not partial);
  ''Analysis of experiments goes beyond single-dimensional summaries of performance
  (e.g., average; median) to include measures of variation, confidence, or other distributional
  information'' (yes/no) -- i.e. reporting a bare AUROC/ECE point estimate without
  variance/CI is a checklist violation, not just a nice-to-have; ''The significance
  of any improvement or decrease in performance is judged using appropriate statistical
  tests (e.g., Wilcoxon signed-rank)'' (yes/partial/no) -- confirms AAAI expects formal
  significance testing for claimed improvements, explicitly naming Wilcoxon signed-rank
  as an accepted method. Also requires: computing infrastructure disclosure (GPU/CPU,
  memory, OS, library versions), seed-setting methodology for randomness, full hyperparameter
  search ranges and selection criteria, motivation for dataset choice, and public
  release of code/data upon publication. For a single-model-per-benchmark scalar-AUROC
  style result (no repeated sampling variance report, no significance test vs. baselines),
  this checklist item set is a concrete, checkable failure point independent of any
  reviewer''s subjective judgment -- an AC or reviewer can literally point to unchecked
  boxes. Directly actionable for DPRC: report per-seed/per-run distributions (not
  single AUROC numbers), bootstrap or Wilcoxon significance tests for AUROC deltas
  vs. baselines (scalar self-report, DCPO, external probes), and infrastructure/seed
  disclosure.'
---

*Suggested by [[main-technical-track-call-for-papers-aaai]] — linked from AAAI-26 policies/guidelines nav; primary reproducibility bar document*

AAAI-26 Reproducibility Checklist - AAAI
Skip to main content
Menu
Home
/
Conferences
/
AAAI Conference on Artificial Intelligence
/
AAAI-26
/
June 9, 2025
The 40th Annual AAAI Conference on Artificial Intelligence
January 20
–
January 27, 2026 | Singapore
AAAI-26
Attend
Accommodations and Travel
Job Fair
Registration Information
Student Scholar Volunteer Program
Visa Letters of Invitation
Ways to Participate in AAAI-26
Expo Information
Program
Program Overview
Bridge Program
Tutorial and Lab Program
Workshop Program
Calls
Main Technical Track
Special Track on AI Alignment
Special Track on AI for Social Impact
Bridge Program
Community Activities
Demonstration Program
Doctoral Consortium
EAAI-26
Emerging Trends in AI Track
IAAI-26
Journal Track
New Faculty Highlights
Senior Member Presentation Track
Student Abstract and Poster Program
Tutorial and Lab Program
Undergraduate Consortium
Workshops
Sponsors
AAAI-26 Sponsors
Become a Sponsor
Policies and Guidelines
AAAI-26 Review Process Update
AAAI Code of Conduct for Conferences and Events
Ethical Guidelines for AAAI-26 Reviewers
FAQ for the AI-Assisted Peer-Review Process Pilot Program
Instructions for AAAI-26 Reviewers
Policies for AAAI-26 Authors
Publication Ethics and and Malpractice Statement
FAQ for Authors (Rebuttal)
Conference Organizers
AAAI-26 Author Kit
Main Conference Timetable for Authors
Note: all deadlines are “anywhere on earth” (UTC-12)
June 16, 2025
Open Review submission site opens for author registration
June 25, 2025
Open Review submission site opens for paper submission
July 25, 2025
Abstracts due at 11:59 PM UTC-12
August 1, 2025
Full papers due at 11:59 PM UTC-12
August 4, 2025
Supplementary material and code due by 11:59 PM UTC-12
September 8, 2025
Notification of Phase 1 rejections
October 2-8, 2025
Author feedback window
November 3, 2025
Notification of final acceptance or rejection (Main Technical Track)
November 13, 2025
Submission of camera-ready files (Main Technical Track)
January 20-27, 2026
AAAI-26 Conference
Note: Deadlines are track-specific and may differ from those listed above. Track-specific deadlines are listed on their respective CFP.
Reproducibility Checklist
Unless specified otherwise, please answer “yes” to each question if the relevant information is described either in the paper itself or in a technical appendix with an explicit reference from the main paper. If you wish to explain an answer further, please do so in a section titled “Reproducibility Checklist” at the end of the technical appendix.
This paper:
Includes a conceptual outline and/or pseudocode description of AI methods introduced (yes/partial/no/NA)
Clearly delineates statements that are opinions, hypothesis, and speculation from objective facts and results (yes/no)
Provides well marked pedagogical references for less-familiare readers to gain background necessary to replicate the paper (yes/no)
Does this paper make theoretical contributions? (yes/no)
If yes, please complete the list below.
All assumptions and restrictions are stated clearly and formally. (yes/partial/no)
All novel claims are stated formally (e.g., in theorem statements). (yes/partial/no)
Proofs of all novel claims are included. (yes/partial/no)
Proof sketches or intuitions are given for complex and/or novel results. (yes/partial/no)
Appropriate citations to theoretical tools used are given. (yes/partial/no)
All theoretical claims are demonstrated empirically to hold. (yes/partial/no/NA)
All experimental code used to eliminate or disprove claims is included. (yes/no/NA)
Does this paper rely on one or more datasets? (yes/no)
If yes, please complete the list below.
A motivation is given for why the experiments are conducted on the selected datasets (yes/partial/no/NA)
All novel datasets introduced in this paper are included in a data appendix. (yes/partial/no/NA)
All novel datasets introduced in this paper will be made publicly available upon publication of the paper with a license that allows free usage for research purposes. (yes/partial/no/NA)
All datasets drawn from the existing literature (potentially including authors’ own previously published work) are accompanied by appropriate citations. (yes/no/NA)
All datasets drawn from the existing literature (potentially including authors’ own previously published work) are publicly available. (yes/partial/no/NA)
All datasets that are not publicly available are described in detail, with explanation why publicly available alternatives are not scientifically satisficing. (yes/partial/no/NA)
Does this paper include computational experiments? (yes/no)
If yes, please complete the list below.
This paper states the number and range of values tried per (hyper-) parameter during development of the paper, along with the criterion used for selecting the final parameter setting. (yes/partial/no/NA)
Any code required for pre-processing data is included in the appendix. (yes/partial/no).
All source code required for conducting and analyzing the experiments is included in a code appendix. (yes/partial/no)
All source code required for conducting and analyzing the experiments will be made publicly available upon publication of the paper with a license that allows free usage for research purposes. (yes/partial/no)
All source code implementing new methods have comments detailing the implementation, with references to the paper where each step comes from (yes/partial/no)
If an algorithm depends on randomness, then the method used for setting seeds is described in a way sufficient to allow replication of results. (yes/partial/no/NA)
This paper specifies the computing infrastructure used for running experiments (hardware and software), including GPU/CPU models; amount of memory; operating system; names and versions of relevant software libraries and frameworks. (yes/partial/no)
This paper formally describes evaluation metrics used and explains the motivation for choosing these metrics. (yes/partial/no)
This paper states the number of algorithm runs used to compute each reported result. (yes/no)
Analysis of experiments goes beyond single-dimensional summaries of performance (e.g., average; median) to include measures of variation, confidence, or other distributional information. (yes/no)
The significance of any improvement or decrease in performance is judged using appropriate statistical tests (e.g., Wilcoxon signed-rank). (yes/partial/no)
This paper lists all final (hyper-)parameters used for each model/algorithm in the paper’s experiments. (yes/partial/no/NA)
We use cookies on our website to give you the most relevant experience by remembering your preferences and repeat visits. By clicking “Accept All”, you consent to the use of ALL the cookies. However, you may visit "Cookie Settings" to provide a controlled consent.
Cookie Settings
Accept All
Manage consent
Close
Privacy Overview
This website uses cookies to improve your experience while you navigate through the website. Out of these, the cookies that are categorized as necessary are stored on your browser as they are essential for the working of basic functionalities of the website. We also use third-party cookies that help us analyze and understand how you use this website. These cookies will be stored in your browser only with your consent. You also have the option to opt-out of these cookies. But opting out of some of these cookies may affect your browsing experience.
Necessary
Necessary
Always Enabled
Necessary cookies are absolutely essential for the website to function properly. These cookies ensure basic functionalities and security features of the website, anonymously.
Cookie
Duration
Description
cookielawinfo-checkbox-analytics
11 months
This cookie is set by GDPR Cookie Consent plugin. The cookie is used to store the user consent for the cookies in the category "Analytics".
cookielawinfo-checkbox-functional
11 months
The cookie is set by GDPR cookie consent to record the user consent for the cookies in the category "Functional".
cookielawinfo-checkbox-necessary
11 months
This cookie is set by GDPR Cookie Consent plugin. The cookies is used to store the user consent for the cookies in the category "Necessary".
cookielawinfo-checkbox-others
11 months
This cookie is set by GDPR Cookie Consent plugin. The cookie is used to store the user consent for the cookies in the category "Other.
cookielawinfo-checkbox-performance
11 months
This cookie is set by GDPR Cookie Consent plugin. The cookie is used to store the user consent for the cookies in the category "Performance".
viewed_cookie_policy
11 months
The cookie is set by the GDPR Cookie Consent plugin and is used to store whether or not user has consented to the use of cookies. It does not store any personal data.
Functional
Functional
Functional cookies help to perform certain functionalities like sharing the content of the website on social media platforms, collect feedbacks, and other third-party features.
Performance
Performance
Performance cookies are used to understand and analyze the key performance indexes of the website which helps in delivering a better user experience for the visitors.
Analytics
Analytics
Analytical cookies are used to understand how visitors interact with the website. These cookies help provide information on metrics the number of visitors, bounce rate, traffic source, etc.
Advertisement
Advertisement
Advertisement cookies are used to provide visitors with relevant ads and marketing campaigns. These cookies track visitors across websites and collect information to provide customized ads.
Others
Others
Other uncategorized cookies are those that are being analyzed and have not been classified into a category as yet.
SAVE & ACCEPT
Close GDPR Cookie Settings
Privacy Overview
Strictly Necessary Cookies
Powered by
GDPR Cookie Compliance
Privacy Overview
This website uses cookies so that we can provide you with the best user experience possible. Cookie information is stored in your browser and performs functions such as recognising you when you return to our website and helping our team to understand which sections of the website you find most interesting and useful.
Strictly Necessary Cookies
Strictly Necessary Cookie should be enabled at all times so that we can save your preferences for cookie settings.
Enable or Disable Cookies
Enabled
Disabled
Enable All
Save Settings