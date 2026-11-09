---
title: '[2606.16062] Auditing Reward Hackability in Code RL Training Environments'
id: 260616062-auditing-reward-hackability-in-code-rl-training-environments
tags:
- code-llm-requirement-pivots-5d35f5
- reward-hacking
- test-suite-weakness
created: '2026-07-20T06:53:55.943488Z'
updated: '2026-07-20T06:56:05.415068Z'
source: https://arxiv.org/abs/2606.16062
source_domain: arxiv.org
fetched_at: '2026-07-20T06:53:55.943125Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Empirically audits how often code RL training/eval environments (SWE-bench
  Verified, R2E-Gym) accept incorrect solutions as correct due to weak test suites,
  operating at whole-task granularity (does ANY Docker-verified incorrect patch pass
  the task's full test suite), not per-unit-test/per-requirement granularity. Finds
  28.5% of a 49-task SWE-bench Verified sample and 25.0% of R2E-Gym tasks have exploitable
  test suites; a random-effects meta-analysis across 134 frontier model submissions
  shows Pass@1 is +14.14pp higher on flagged-hackable tasks than robust ones within
  the same difficulty stratum (95% CI [11.80,16.48], p<1e-6). Proposes a gold-sanity-gated
  LLM judge to harden weak tasks, catching 61.9% of decisive LLM-generated tests that
  fail on the gold patch itself.
---

[2606.16062] Auditing Reward Hackability in Code RL Training Environments
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Artificial Intelligence
arXiv:2606.16062
(cs)
[Submitted on 14 Jun 2026]
Title:
Auditing Reward Hackability in Code RL Training Environments
Authors:
Shreshth Rajan
View a PDF of the paper titled Auditing Reward Hackability in Code RL Training Environments, by Shreshth Rajan
View PDF
HTML (experimental)
Abstract:
We measure the rate at which code RL environments accept incorrect solutions as correct. On a 49-task sample of SWE-bench Verified, 28.5% of tasks have test suites weak enough that a Docker-verified incorrect patch passes them. On 20 R2E-Gym tasks across 6 repositories, the same pipeline at single-shot exploit generation yields 25.0%. A random-effects meta-analysis over 134 frontier model submissions to SWE-bench Verified finds, within the same human-rated difficulty stratum, model Pass@1 is +14.14 percentage points higher on flagged-hackable tasks than on robust ones (95% CI [+11.80, +16.48]; one-sided p < 10^-6; I^2 = 0%; 123 of 134 models positive). We then describe a procedure for hardening the broken tasks. An inline LLM judge with a Docker gold-sanity gate runs each generated test against the gold solution before the judge is consulted. On the 11 broken tasks in the audit, the gate flags 65 of 105 decisive LLM-generated tests as failing on the gold patch itself, a 61.9% per-augmentation defect rate the LLM judge alone misses. With diversity-biased retry, the loop converges 9 of 11 tasks to a gated upgrade.
Subjects:
Artificial Intelligence (cs.AI)
; Machine Learning (cs.LG)
Cite as:
arXiv:2606.16062
[cs.AI]
(or
arXiv:2606.16062v1
[cs.AI]
for this version)
https://doi.org/10.48550/arXiv.2606.16062
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Shreshth Rajan [
view email
]
[v1]
Sun, 14 Jun 2026 23:31:42 UTC (79 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Auditing Reward Hackability in Code RL Training Environments, by Shreshth Rajan
View PDF
HTML (experimental)
TeX Source
view license
Current browse context:
cs.AI
< prev
|
next >
new
|
recent
|
2026-06
Change to browse by:
cs
cs.LG
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