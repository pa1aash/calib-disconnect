---
title: Instructions for AAAI-26 Reviewers - AAAI
id: instructions-for-aaai-26-reviewers-aaai
tags:
- aaai-bar-eval-dprc-d78e07
created: '2026-07-19T20:01:29.726406Z'
updated: '2026-07-19T20:02:04.354135Z'
source: https://web.archive.org/web/2026/https://aaai.org/conference/aaai/aaai-26/instructions-for-aaai-26-reviewers/
source_domain: web.archive.org
fetched_at: '2026-07-19T20:01:29.723792Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'Official AAAI-26 reviewer instructions (fetched via Wayback; live aaai.org
  403s). Lays out the exact rubric human reviewers apply: story clarity, problem significance,
  limitations of SOTA addressed, whether empirical results support claims, key novel
  technical contribution, technical soundness/reproducibility, related-work placement,
  and a dedicated Evaluations checklist -- appropriate baselines/comparisons vs SOTA,
  well-established metrics, appropriately chosen benchmarks/datasets (''are there
  better benchmarks that should have been used?''), error analysis of the proposed
  approach, and full replicability of evaluations. Confirms two-phase review: Phase
  1 = two human reviews + one non-rated/non-recommending AI-generated review used
  only as SPC context (AI review cannot itself advance/reject a paper); Phase 2 adds
  human reviewers plus author rebuttal, after which human reviewers may revise ratings;
  an AI-generated discussion summary aids the SPC/AC decision but does not decide.
  Explicitly bars reviewers from duplicating other reviews'' content. This is the
  primary artifact defining ''what reviewers actually check'' -- directly operationalizes
  the AAAI-27 CFP''s abstract novelty/soundness language into a checklist DPRC must
  satisfy item-by-item (esp. baselines vs SOTA, error analysis, benchmark appropriateness,
  and full replicability).'
---

Instructions for AAAI-26 Reviewers - AAAI
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
July 26, 2025
The 40th Annual AAAI Conference on Artificial Intelligence
January 20
–
January 27, 2026 | Singapore
AAAI-26
IAAI-26
EAAI-26
Attend
Accommodations and Travel
Registration Information
Visa Letters of Invitation
Student Activities
Student Scholar Volunteer Program
Job Fair
Ways to Participate in AAAI-26
Onsite Childcare
Nearby Dining
Expo Information
Program
AAAI-26 Invited Talks
AAAI-26 Program Overview
Bridge Program
Community Activities
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
Poster Guidelines and Printing Options
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
Instructions for AAAI-26 Reviewers
Review Timeline
AAAI-26 will follow a two-phase reviewing process as in previous years, with two additions: an additional AI-generated review in Phase 1, and an AI-generated summary of the discussions at the end of the discussion phase.  The AI-generated content is being used as part of a pilot program to evaluate the ability of AI tools to assist in the peer review process.
Phase 1:
This year, the two human-written reviews in Phase 1 will be supplemented by an additional AI-generated review.  This AI review will not include
any ratings or recommendations,
as an experiment for the pilot program. No human reviewers are being replaced by AI reviewing.  Only the human-written reviews and human expertise will be used to decide whether the paper proceeds to Phase 2.
Phase 2:
If the paper proceeds to Phase 2, it is assigned additional human reviewers.
During the author response phase, all reviews, including the AI-generated review, become visible to the reviewers and the authors. The AI-generated review will be clearly labelled as such. Just as in previous years, authors may submit a response to the reviews, including to the AI-generated review.
Phase 2 Discussion Phase:
Based on all the reviews (including the AI-generated review), and the authors’ response, the human reviewers may revise their own reviews and/or their ratings. At the conclusion of the discussion phase, an AI generated summary will recap points of consensus and difference between the reviews (including human and AI-generated reviews), visible only to the SPC and AC.
Guidelines On Writing Helpful Reviews
To write a professional, respectful, and effective review:
In general, please do not use “I”, “you”, “the authors”, etc., in your reviews. Reviews should be depersonalized as much as possible. Use terms like “the paper”, “the work”, “the project”. The review should focus on the work and not the individuals (reviewers or authors). Avoid referring to yourself. If you must refer to yourself, it should be in the third person (e.g., “this reviewer”) and done sparingly.
Phrase your comments as would be appropriate if you were speaking respectfully to the authors face-to-face.
Instead of “What is wrong with this paper?”, ask yourself “How could this paper be better?”
When suggesting revisions in the review, think about whether the revisions are reasonable in terms of time and resources — which of the recommendations are essential, and which are nice-to-have but optional?
Is the story of the paper clear?
What is the problem that the paper aims to address?
What are the limitations in the state of the art that the paper addresses? Are the limitations clearly articulated, and reflective of the state of the art?
Do the empirical results really support the claims of the paper?
What is the key novel technical contribution in the paper?
Presentation of the proposed contribution:
Is the technical approach sound and clearly described?
Are there any errors, unstated assumptions, or missing details?
Is it expressed in sufficient detail to permit reproduction of the work?
Does the paper clearly describe the limitations (in scope and generalizability) of its conclusions?  (All work has limits, and it is vital to understand them.)
Related work:
Is the proposed contribution placed in the appropriate context of previous and related work, so as to allow a reader to draw connections between this work and others?
Evaluations:
Does the empirical evaluation include appropriate baselines and comparisons to validate the proposed approach compared to the state of the art?
Does the empirical evaluation report well-established and reasonable metrics?
Are the evaluation benchmarks and datasets appropriately chosen? Are there any better benchmarks or datasets that should have been used?
Does the paper include an analysis of errors made by the proposed approach?
Do the empirical results really support the claims of the paper?
Are the evaluations fully replicable?
Suggestions for improvement:
How could the research or the presentation of the paper be improved in light of the above?
Using the AI-Generated Reviews and Summaries
When will the AI-generated review be visible?
To ACs and SPCs: As soon as the review is generated.
To reviewers:
If the paper is rejected in Phase 1, the AI-generated review, along with the other reviews, will become visible to all reviewers of the paper when the decision is released.
If the paper proceeds to Phase 2, the AI-generated review will only be visible to reviewers during the author rebuttal phase, as is done with human reviews.
To authors:
The AI review is made visible along with the other reviews according to the normal review process — if the paper is rejected in Phase 1, all reviews are made available then, and if the paper proceeds to Phase 2, all reviews are made available at the start of the rebuttal period.
How can I flag issues with the AI-generated review?
All reviewers will have the ability to make an official comment on the AI-generated review (distinct from the reviewer discussion), along with review ratings. These comments will only be visible to SPCs and higher. The Program Chairs, Workflow chairs, and Area Chairs will monitor comments made on AI-generated reviews to identify issues, and will take action as appropriate, such as re-generating the review, or excluding it entirely.
What can a reviewer do with the AI-generated review?
As with human-generated reviews, reviewers will have the opportunity to read and reflect on others’ reviews, including the AI-generated reviews, and the author responses, during the rebuttal period. They may accordingly update their own reviews as they see fit, such as if a misunderstanding is clarified. The reviewers
must not
duplicate content from other reviews (neither the AI-generated nor human reviews), but are free to express their level of agreement with the points raised.
What can the SPC and the AC do with the AI-generated review?
Phase 1
: The SPC makes recommendations to promote papers from Phase 1 to Phase 2 after reading all reviews, including the AI-generated reviews. Note that only the human reviews will have a paper rating and recommendations — the AI-generated reviews will not have any ratings or recommendations. The SPC will make their recommendation based on all the information available — the two human reviews and the AI review, and the recommendations from the human reviewers.
Phase 2
: The SPC and AC make decision recommendations in phase 2 for the paper based on 1) all the reviews available from the human reviewers and the AI system; 2) the author responses; 3) discussions among the reviewers; 4) the AI-generated summary of author responses and reviewer discussions.
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