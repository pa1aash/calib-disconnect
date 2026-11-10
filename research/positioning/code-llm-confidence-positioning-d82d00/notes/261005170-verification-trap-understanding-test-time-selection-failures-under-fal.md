---
title: '[2610.05170] Verification Trap: Understanding Test-Time Selection Failures
  under False Premises in Code Generation'
id: 261005170-verification-trap-understanding-test-time-selection-failures-under-fal
tags:
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-11-09T23:11:01.375364Z'
updated: '2026-11-09T23:28:27.351818Z'
source: https://arxiv.org/abs/2610.05170
source_domain: arxiv.org
fetched_at: '2026-11-09T23:11:01.374790Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Vault note holds the arXiv abstract page; full text read from locally extracted
  arXiv PDF. He et al. study test-time selection (64 samples, generated-test verifiers)
  under false task premises on HumanEval+, MBPP, LiveCodeBench with DeepSeek-Coder-6.7B-Instruct,
  Qwen2.5-Coder-7B/14B/32B-Instruct, GPT-4o-mini. Metrics: Pass@1, Selected@64, Oracle@64,
  Trap@64; a gold-free predictor reaches 0.846 AUROC. Shows verifier-written tests
  inherit generator blind spots (relevant to L4 self-written test adequacy and L3
  oracle gap) but uses no confidence routing or verbal confidence.'
---

[2610.05170] Verification Trap: Understanding Test-Time Selection Failures under False Premises in Code Generation
Skip to main content
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Computation and Language
arXiv:2610.05170
(cs)
[Submitted on 4 Oct 2026]
Title:
Verification Trap: Understanding Test-Time Selection Failures under False Premises in Code Generation
Authors:
Feng He
,
Hejia Wang
,
Linghao Meng
,
Ming Gao
,
Qiankun Li
View a PDF of the paper titled Verification Trap: Understanding Test-Time Selection Failures under False Premises in Code Generation, by Feng He and 4 other authors
View PDF
HTML (experimental)
Abstract:
Test-time compute has become a central way to improve code generation: systems sample multiple candidate programs and use verifier-visible evidence to select the final output. This paradigm implicitly assumes that the verifier provides a corrective signal independent from the generator. We challenge this assumption under misleading task premises. When the generator and verifier share a false premise, they become coupled through a mistaken belief: the generator produces premise-consistent shortcuts, while the verifier supplies evidence that fails to expose them. Consequently, the selector may choose a hidden-test-wrong candidate even when a hidden-test-correct program exists in the pool. We call this failure mode Verification Trap. Across three code-generation benchmarks and five code models, false premises consistently degrade first-sample correctness, reduce selector-chosen correctness after 64-sample test-time selection, and amplify recoverable mis-selection. Mechanistically, verifier-written tests inherit the premise-level blind spot, reshaping verifier-visible candidate space away from hidden-test correctness. These traces make Verification Trap predictable before hidden execution: a lightweight gold-free predictor using verifier-visible features reaches 0.846 AUROC. Our results identify decoupled evidence as a key mitigation axis: coupled scaling provides limited recovery, whereas premise-agnostic robustness auditors recover substantial oracle headroom.
Comments:
EMNLP 2026
Subjects:
Computation and Language (cs.CL)
Cite as:
arXiv:2610.05170
[cs.CL]
(or
arXiv:2610.05170v1
[cs.CL]
for this version)
https://doi.org/10.48550/arXiv.2610.05170
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Feng He [
view email
]
[v1]
Sun, 4 Oct 2026 12:28:10 UTC (5,631 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled Verification Trap: Understanding Test-Time Selection Failures under False Premises in Code Generation, by Feng He and 4 other authors
View PDF
HTML (experimental)
TeX Source
view license
Additional Features
Audio Summary
Current browse context:
cs.CL
< prev
|
next >
new
|
recent
|
2026-10
Change to browse by:
cs
References & Citations
SciX
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