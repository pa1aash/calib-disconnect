---
title: '[2502.07786] Counterexample Guided Program Repair Using Zero-Shot Learning
  and MaxSAT-based Fault Localization'
id: 250207786-counterexample-guided-program-repair-using-zero-shot-learning-and-maxs
tags:
- aaai-bar-eval-dprc-d78e07
- code-llm
- fault-localization
- aaai-2025
- program-repair
created: '2026-07-19T20:02:15.969059Z'
updated: '2026-07-19T20:04:35.978960Z'
source: https://arxiv.org/abs/2502.07786
source_domain: arxiv.org
fetched_at: '2026-07-19T20:02:15.968683Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'AAAI 2025 paper (Orvalho, Janota, Manquinho; U. Lisbon) on Automated Program
  Repair for introductory programming assignments, combining MaxSAT-based formal fault
  localization (identifies buggy statements deterministically from a test suite) with
  zero-shot LLM synthesis in a Counterexample-Guided Inductive Synthesis (CEGIS) loop:
  the LLM is shown a program sketch with buggy statements removed, synthesizes replacements,
  and iterates using failing counterexamples as feedback. Evaluated on 1,431 real
  incorrect student programs across six LLMs, showing significantly more programs
  repaired with smaller (less invasive) fixes than pure-LLM or pure-symbolic-repair
  baselines. Relevant to DPRC as an AAAI-2025 example pairing formal/symbolic fault
  localization with LLM code generation on a large real dataset (1,431 programs) and
  six-model baseline sweep — a scale of evaluation (many models, many real programs,
  ablated configurations) that DPRC''s current single-model, ~1140-problem BigCodeBench
  run does not yet match.'
---

[2502.07786] Counterexample Guided Program Repair Using Zero-Shot Learning and MaxSAT-based Fault Localization
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2502.07786
(cs)
[Submitted on 19 Dec 2024]
Title:
Counterexample Guided Program Repair Using Zero-Shot Learning and MaxSAT-based Fault Localization
Authors:
Pedro Orvalho
,
Mikoláš Janota
,
Vasco Manquinho
View a PDF of the paper titled Counterexample Guided Program Repair Using Zero-Shot Learning and MaxSAT-based Fault Localization, by Pedro Orvalho and Mikol\'a\v{s} Janota and Vasco Manquinho
View PDF
HTML (experimental)
Abstract:
Automated Program Repair (APR) for introductory programming assignments (IPAs) is motivated by the large number of student enrollments in programming courses each year. Since providing feedback on IPAs requires substantial time and effort from faculty, personalized feedback often involves suggesting fixes to students' programs. Formal Methods (FM)-based semantic repair approaches, check a program's execution against a test suite or reference solution, are effective but limited. These tools excel at identifying buggy parts but can only fix programs if the correct implementation and the faulty one share the same control flow graph. Conversely, Large Language Models (LLMs) are used for APR but often make extensive instead of minimal rewrites. This leads to more invasive fixes, making it harder for students to learn from their mistakes. In summary, LLMs excel at completing strings, while FM-based fault localization excel at identifying buggy parts of a program. In this paper, we propose a novel approach that combines the strengths of both FM-based fault localization and LLMs, via zero-shot learning, to enhance APR for IPAs. Our method uses MaxSAT-based fault localization to identify buggy parts of a program, then presents the LLM with a program sketch devoid of these buggy statements. This hybrid approach follows a CEGIS loop to iteratively refine the program. We ask the LLM to synthesize the missing parts, which are then checked against a test suite. If the suggested program is incorrect, a counterexample from the test suite is fed back to the LLM. Our experiments show that our counterexample guided approach, using MaxSAT-based bug-free program sketches, significantly improves the repair capabilities of all six evaluated LLMs. This method allows LLMs to repair more programs with smaller fixes, outperforming other configurations and state-of-the-art symbolic program repair tools.
Comments:
Accepted at AAAI 2025. 11 pages, 4 listings, 2 figures and 5 tables
Subjects:
Software Engineering (cs.SE)
; Artificial Intelligence (cs.AI)
Cite as:
arXiv:2502.07786
[cs.SE]
(or
arXiv:2502.07786v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2502.07786
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Pedro Orvalho [
view email
]
[v1]
Thu, 19 Dec 2024 12:08:44 UTC (135 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Counterexample Guided Program Repair Using Zero-Shot Learning and MaxSAT-based Fault Localization, by Pedro Orvalho and Mikol\'a\v{s} Janota and Vasco Manquinho
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
2025-02
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