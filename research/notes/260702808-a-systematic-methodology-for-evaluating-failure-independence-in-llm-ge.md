---
title: '[2607.02808] A Systematic Methodology for Evaluating Failure Independence
  in LLM-Generated Code'
id: 260702808-a-systematic-methodology-for-evaluating-failure-independence-in-llm-ge
tags:
- code-llm-best-aaai-paper-6ded37
- correlated-failures
- adjacent-not-scooping
- nvp-reliability
created: '2026-07-20T07:44:10.937098Z'
updated: '2026-07-20T07:46:13.842958Z'
source: https://arxiv.org/abs/2607.02808
source_domain: arxiv.org
fetched_at: '2026-07-20T07:44:10.936776Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Proposes the first systematic methodology to assess FAILURE INDEPENDENCE
  across independently-generated implementations (N-Version Programming), applied
  to 224 problems x 12 models x 5 languages x 3 prompting strategies. Measures structural
  diversity (code similarity) and behavioral diversity (whether different implementations
  fail the SAME test cases), plus N-version reliability under majority voting. Key
  finding: implementations fail on the same tests far more often than chance/independence
  would predict; three/five-version ensembles realize only 0.43/0.44 of the reliability
  gain achievable under true independence (dropping below 0.3 for same-model ensembles);
  manual inspection shows even differently-manifesting failures often share root causes.
  DIFFERENT UNIT OF ANALYSIS from a per-requirement latent-skill paper: this correlates
  failures ACROSS independently-sampled SOLUTIONS to the same problem (ensemble/NVP
  reliability angle), not per-requirement (per-unittest-method) pass/fail correlation
  WITHIN one solution, and does not attempt a factor-analytic/IRT latent-skill decomposition
  or cross-model-family shared-vs-idiosyncratic skill claim. Confirms ''correlated
  code-LLM failures'' is an active 2026 research area from an adjacent (reliability-engineering)
  angle.'
---

[2607.02808] A Systematic Methodology for Evaluating Failure Independence in LLM-Generated Code
Skip to main content
arXiv is now an independent nonprofit!
Learn more
×
Search arXiv
Press Enter to search ·
Advanced search
Computer Science > Software Engineering
arXiv:2607.02808
(cs)
[Submitted on 2 Jul 2026]
Title:
A Systematic Methodology for Evaluating Failure Independence in LLM-Generated Code
Authors:
Rodrigo Pato Nogueira
,
Karthik Pattabiraman
,
Marco Vieira
,
João R. Campos
View a PDF of the paper titled A Systematic Methodology for Evaluating Failure Independence in LLM-Generated Code, by Rodrigo Pato Nogueira and 3 other authors
View PDF
HTML (experimental)
Abstract:
N-Version Programming (NVP) improves software reliability by executing multiple independent implementations and combining outputs, but its adoption is limited by high cost and the assumption of failure independence, which empirical studies have challenged. Recent advances in Large Language Models (LLMs) reduce the cost of generating multiple implementations, shifting focus to whether their failures are independent. We propose the first systematic methodology to assess failure independence in LLM-generated code and apply it to 224 problems across twelve models, five languages, and three prompting strategies. We analyze both structural and behavioral diversity (i.e., whether implementations fail on the same test cases), complemented by N-version reliability analysis under majority voting and manual inspection of the generated code. Structural diversity analysis shows that implementations from the same model are highly similar, while different models produce more distinct solutions. The same trend appears in behavioral diversity, with implementations from different models showing higher diversity yet still failing on the same tests far more often than expected under independence. N-version reliability analysis reinforces this: three- and five-version ensembles realize only 0.43 and 0.44 of the reliability gain achievable under independence, dropping below 0.3 when ensembles are built from the same model. Manual fault analysis shows that even different failure patterns often share root causes. Overall, these results suggest LLM-generated solutions do not satisfy NVP's failure independence assumption, though heterogeneous models help partially. They also validate our methodology as a tool for systematically evaluating failure independence as models evolve.
Subjects:
Software Engineering (cs.SE)
Cite as:
arXiv:2607.02808
[cs.SE]
(or
arXiv:2607.02808v1
[cs.SE]
for this version)
https://doi.org/10.48550/arXiv.2607.02808
Focus to learn more
arXiv-issued DOI via DataCite
Submission history
From: Joāo R. Campos [
view email
]
[v1]
Thu, 2 Jul 2026 22:49:05 UTC (253 KB)
Full-text links:
Access Paper:
View a PDF of the paper titled A Systematic Methodology for Evaluating Failure Independence in LLM-Generated Code, by Rodrigo Pato Nogueira and 3 other authors
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
2026-07
Change to browse by:
cs
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