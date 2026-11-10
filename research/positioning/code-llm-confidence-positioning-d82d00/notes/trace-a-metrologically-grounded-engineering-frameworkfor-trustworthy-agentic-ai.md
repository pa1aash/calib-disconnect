---
title: 'TRACE: A Metrologically-Grounded Engineering Frameworkfor Trustworthy Agentic
  AI Systems inOperationally Critical Domains'
id: trace-a-metrologically-grounded-engineering-frameworkfor-trustworthy-agentic-ai
tags:
- code-llm-confidence-positioning-d82d00
- f-measurement-framing
created: '2026-11-10T08:24:17.084348Z'
updated: '2026-11-10T08:27:10.793745Z'
source: https://arxiv.org/html/2605.03838
source_domain: arxiv.org
fetched_at: '2026-11-10T08:24:17.083976Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: arXiv 2605.03838 TRACE. Conceptual agentic-AI architecture with trust metrics
  mapped to GUM/VIM/ISO 17025; Calibration Error is one listed metric. No code-confidence
  experiments. Weak F occupant (metrology vocabulary applied to agentic AI, not LLM
  code confidence). Full text.
---

TRACE: A Metrologically-Grounded Engineering Frameworkfor Trustworthy Agentic AI Systems inOperationally Critical Domains
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY-NC-ND 4.0
arXiv:2605.03838v1 [cs.CL] 05 May 2026
TRACE: A Metrologically-Grounded Engineering Framework
for Trustworthy Agentic AI Systems in
Operationally Critical Domains
Serhii Zabolotnii
†
†
thanks:
Corresponding author. Email:
zabolotnii.serhii@csbc.edu.ua
.
Cherkasy State Business College, Cherkasy 18028, Ukraine
State Scientific Research Institute of Armament and Military Equipment
Testing and Certification, Cherkasy, Ukraine
healthPrecision, New York, NY, USA
Abstract
We introduce TRACE, a cross-domain engineering framework for trustworthy agentic AI
in operationally critical domains.
TRACE combines a four-layer reference architecture with an explicit classical-ML
vs. LLM-validator split (L2a/L2b), a stateful orchestration-and-escalation policy (L3),
and bounded human supervision (L4);
a metrologically grounded trust-metric suite mapped to GUM/VIM/ISO 17025;
and a Model-Parsimony principle quantified by the Computational Parsimony Ratio (CPR).
Three instantiations—clinical decision support, industrial multi-domain
operations, and a judicial AI assistant—transfer the same architecture and metrics
across principally different governance contexts.
The L2a/L2b separation makes the use of large language models a deliberate design
decision rather than an architectural default, with parsimony quantified through CPR.
TRACE introduces CPR as a first-class design principle in trustworthy-AI engineering.
Keywords:
Trustworthy AI •
Agentic AI •
Large language models •
LLM validators •
LLM-orchestrated oversight •
Metrological traceability •
Tiered oversight •
Model parsimony •
Operationally critical systems •
Human–AI supervision
Companion site:
Documentation, the up-to-date publication roster, and CRediT-style author
contributions are available at
https://traces.solutions
.
1
Introduction
Trust in agentic AI is not an intrinsic property of the model.
A high-benchmark model can behave dangerously in real-world deployment;
a modestly accurate model can operate safely within a correctly engineered architecture.
As agentic AI systems enter operationally critical domains—clinical decision support,
industrial multi-domain operations, judicial assistance, energy and infrastructure
management—this observation becomes an engineering problem rather than a philosophical one:
how should the architecture be designed so that trust is a measurable property of
the system, not merely a declaration?
The 2024–2026 literature addresses this question through four parallel but largely
disconnected streams.
Stream 1 – Clinical trust frameworks.
FUTURE-AI
[
1
]
provides an international six-principle consensus
for trustworthy clinical AI
(fairness, universality, traceability, usability, robustness, explainability).
TRIAD
[
2
]
formulates a three-component governance/value/deployment model
for human–AI collaboration in medicine.
Both are domain-specific and lack metrological grounding or cross-domain applicability.
Stream 2 – Hierarchical agentic oversight.
Tiered Agentic Oversight (TAO) by Kim et al.
[
3
]
formalises tiered agentic
escalation with an orchestrator and clinician in the loop, empirically demonstrating
absorption of 16.9–24.3% of individual-agent errors (Table 6,
[
3
]
).
TAO is the closest architectural predecessor of TRACE and an empirical anchor for
cross-domain generalisation.
A complementary, more recent line of work—Eywa by Li et al.
[
4
]
—
demonstrates heterogeneous foundation-model / LLM collaboration through an explicit
FM–LLM communication protocol (
Tsaheylu
), with the EywaBench benchmark
showing consistent token-cost reduction at improved utility across nine scientific
domains.
However, TAO (i) is limited to the clinical domain; (ii) implements routing and rules
through an LLM orchestrator without a dedicated deterministic rule layer;
(iii) conflates model-class selection and invocation policy in the same tiered hierarchy;
(iv) relies on LLM agents throughout—a limitation explicitly acknowledged by its
authors
[
3
]
; (v) has no metrological apparatus; and (vi) does not address
model parsimony.
Eywa addresses the LLM-only limitation by formalising the FM–LLM interface but,
as a domain-collaboration framework, does not propose a layered trust architecture
or a metrologically grounded metric suite.
Stream 3 – Metrological uncertainty for ML.
Bilson et al.
[
5
]
transfer VIM/GUM apparatus to ML classification
via probability mass functions;
Thompson et al.
[
6
]
bridge trustworthy AI and metrology
conceptually.
Both are limited to classification tasks without agentic architecture or cross-domain scope.
Stream 4 – Model parsimony.
Belcak et al. (NVIDIA)
[
7
]
argue that small language models are the
appropriate medium for most agentic sub-tasks;
Schwartz et al.
[
8
]
frame efficiency as a first-class evaluation
metric.
These works provide an economic and engineering imperative but do not offer a trust
architecture.
Parallel governance anchors—NIST AI RMF
[
9
]
,
NIST GAI Profile
[
10
]
,
ISO/IEC 42001
[
11
]
,
EU AI Act
[
12
]
, and the cross-domain framework by
Herrera-Poyatos et al.
[
13
]
—provide regulatory scaffolding
but not an engineering architecture.
TRACE positions itself as the engineering layer that operationalises those obligations
through measurable, architecture-embedded artefacts.
Gap.
No published work unifies (i) a multi-layer trust architecture,
(ii) cross-domain instantiation in operationally critical domains,
(iii) a metrologically grounded trust-metric suite, and
(iv) a model-parsimony principle in a single framework.
TRACE closes this four-sided gap.
Genesis.
TRACE emerged from the author’s recognition and formalisation of a shared structural
pattern observed across two independently developed operationally critical systems:
(i) a clinical decision-support architecture with metrological uncertainty
monitoring
[
14
]
, in which the author is a co-developer,
currently under review at
IEEE Instrumentation & Measurement Magazine
;
and (ii) an industrial multi-domain agentic-AI platform for upstream oil-and-gas
operations spanning technology/operations/administrative loops, developed independently
by Shcherban (2024–2026)
[
15
,
16
]
.
Recognising the four-layer decomposition, tiered escalation, and parsimony of learned
components shared between these two structurally distinct systems is the conceptual core
of TRACE; this paper formalises that recognition.
Contributions.
This work: (a) presents TRACE as a domain-neutral engineering framework grounded in six
principles with explicit metrological analogues; (b) defines a four-layer reference
architecture with an L2a/L2b split based on the parsimony principle and an
architecturally separate L3 orchestration-and-escalation policy; (c) specifies a
layer-wise trust-metric suite culminating in CPR—the first quantitative first-class
parsimony metric in the trustworthy-AI literature; (d) instantiates the framework in
three domains (clinical, industrial multi-domain, judicial) and makes the architectural
distinction from TAO precise.
2
The TRACE Framework
2.1
Six Design Principles
TRACE rests on six mutually reinforcing principles, each with a metrological analogue:
1.
Evidence Traceability.
Every prescriptive action carries a machine-readable evidence trail.
Metrological analogue:
traceability of measurement results
[
17
]
.
2.
Bounded Human Supervision.
Human oversight is an architectural layer with measurable workload and veto rights,
not a cosmetic safety net.
Analogue:
operator supervision of measurement systems
[
18
]
.
3.
Staged Autonomy.
Action rights are earned through accumulated evidence, not granted by default.
Analogue:
type approval and operational qualification.
4.
Bounded Context.
The input context is explicitly specified, time-stamped, and kept current as a
safety property.
Analogue:
operational limits and environmental conditions.
5.
Metrological Accountability.
All quality characteristics are specified, measurable, calibrated, and monitored
over time
[
5
,
19
]
.
Analogue:
calibration, drift monitoring, stability testing.
6.
Model Parsimony / Right-Sized Components.
The type of learned component (classical ML, specialised neural network, LLM, or
hybrid) is chosen by fitness for purpose, not by LLM presumption
[
7
,
8
]
.
Analogue:
fitness for purpose
—the foundational metrological
requirement.
The acronym TRACE reflects five user-visible system properties
(
trustworthy, reasoned, accountable, context-bound, escalated
);
model parsimony operates as an internal design constraint.
2.2
Four-Layer Reference Architecture
Figure 1:
TRACE four-layer reference architecture.
L1 provides the deterministic rule core (trust anchor);
L2 holds the stateless learned-component inventory, partitioned into
classical ML (L2a) and LLM validators (L2b);
L3 is the stateful orchestration-and-escalation policy;
L4 is bounded human supervision.
Figure
1
shows the four-layer decomposition.
L1 – Deterministic / Physics-Based Core.
Non-generative, interpretable, stable logic: rule systems, control theory, enumerated
protocols, physical models, compliance scaffolding.
Key architectural distinction from TAO
[
3
]
: TAO implements routing
and rules through an LLM orchestrator; TRACE separates L1 as an independent, non-learned,
formally verifiable layer and the primary trust anchor of the system.
L2 – Learned-Component Inventory (stateless).
A catalogue of trained components partitioned by the parsimony principle.
L2 defines
what
the system can do;
when and in what order
components are
invoked is the responsibility of L3 policy.
Each L2 invocation is stateless and accountable to its calling policy.
•
L2a – Specialised / Classical ML.
Gradient boosting (XGBoost, CatBoost), random forests, isolation forests, SVM,
and classical neural architectures (CNN, LSTM, Transformer encoders for sensor fusion).
Applied where inputs are structured, latency is critical, reproducibility is
required, and probability calibration is formally verifiable
[
20
,
21
]
.
•
L2b – Generative / LLM Validators.
LLMs and generative models as contextual validators, semantic reviewers, and
inconsistency detectors for free-form data.
Invoked only where the task genuinely requires linguistic understanding.
The L2a/L2b boundary is described here at the architectural level. A concrete
protocol-level realisation of an analogous boundary is given by Eywa’s
Tsaheylu
interface
[
4
]
, which formalises the communication
contract between domain-specific foundation models (analogous to L2a) and
language-model agents (analogous to L2b). TRACE remains protocol-agnostic;
Tsaheylu is one viable implementation of the L2a
↔
\leftrightarrow
L2b boundary
within the framework.
L3 – Orchestration-and-Escalation Policy (stateful).
An architecturally separate policy layer
above the L2 inventory
, operating on
task state (passage history, accumulated confidence, risk context, latency and cost
budget).
The policy specifies:
(i) which L2 components are invoked and in what order for a given task type;
(ii) conditions for re-invocation with expanded context or switching to an alternative
component;
(iii) escalation triggers to L4—the
joint
condition of high risk and high
confidence
[
3
]
(a confident error in a high-risk context is more dangerous
than an acknowledged uncertainty), or L3-detected inconsistency between L2 components,
or exhaustion of the re-invocation budget;
(iv) cost accounting for each execution path (Tier Cost Coefficient).
Key distinction from TAO
: TAO implements tiered oversight as a hierarchy of LLM
agents under an LLM orchestrator—in TRACE terms, this conflates L2-concern
(model-class selection) and L3-concern (invocation policy).
TRACE separates them: L2a vs. L2b is a static design decision by fitness for purpose;
invocation sequence, re-invocations, and escalation are L3 policy, independently
calibrated from operational statistics.
This separation removes the TAO safety-parsimony trade-off.
L4 – Bounded Human Supervision.
Final accountability, veto, and calibration of AI authority bounds.
L4 entry is determined by L3 policy, not by direct L2 requests.
2.3
Sub-Domain
×
\times
Layer Matrix
Real deployments often span multiple operational sub-domains.
TRACE represents this as a
sub-domain
×
\times
layer matrix
: each sub-domain
instantiates all four layers independently, and cross-sub-domain coordination is provided
by a master orchestrator.
This yields systematic, transferable deployment templates for complex multi-domain
systems.
Instance B (Section
3.2
) provides a documented precedent for this
matrix across three sub-domains with principally different data types.
2.4
Trust Metric Suite
TRACE specifies 17 metrics: 12 layer-wise, 4 cross-cutting, and 1 parsimony metric.
The suite extends the metrological apparatus of
Bilson et al.
[
5
]
and
Thompson et al.
[
6
]
from ML classification alone to the full
agentic lifecycle:
ingestion
→
\to
inference
→
\to
escalation
→
\to
human adjudication
.
Layer-wise metrics:
L1:
Rule Coverage Rate, Rule Consistency Index,
Update Traceability Coefficient.
L2:
Context Relevance Precision, Context Freshness Index,
Input Perturbation Stability Rate.
L3:
Escalation Precision (correctness of L4 hand-off decisions);
Tier Cost Coefficient (aggregate computational cost of the policy-chosen execution path);
False Positive Attenuation (suppression of spurious escalations through L2
re-invocations).
These metrics evaluate the policy itself, not the quality of individual L2
components
[
22
]
.
L4:
Review Burden Index, Override Rate, Signal-to-Noise Ratio.
Cross-cutting metrics:
Evidence Trail Completeness;
Calibration Error
[
20
]
;
Autonomy Boundary Compliance;
Operational Stability Index.
Parsimony metric – Computational Parsimony Ratio (CPR).
CPR is the ratio of the resource cost of the most economical model that adequately
solves the sub-task (meeting required accuracy, calibration, and operational reliability)
to the resource cost of the deployed model.
CPR
=
1
\text{CPR}=1
indicates an optimal model choice;
values substantially below 1 signal architectural overhead.
Resource cost encompasses latency, compute, training, and operational expenditure.
To the best of our knowledge, CPR is the first formalisation of Complexity-Performance
Ratio as a first-class design principle in the trustworthy-AI literature.
Empirical support for the underlying intuition is provided by Eywa’s EywaBench
results
[
4
]
: across nine scientific domains, replacing LLM-only
pipelines with FM–LLM heterogeneous collaboration improves utility while reducing
token cost—precisely the regime CPR is designed to surface as architectural overhead.
Each metric has a direct metrological analogue (accuracy, repeatability, systematic
error, drift, fitness for purpose), enabling principled aggregation via GUM-style
uncertainty propagation across layers
[
19
,
5
]
.
3
Multi-Domain Instantiations
The framework’s universality is demonstrated by three instantiations.
Instances A and B are
foundational precedents
—independently developed
systems whose shared structural pattern motivated TRACE’s formalisation.
Instance C is a
partially implemented extension
demonstrating architectural portability.
3.1
Instance A: Clinical Decision Support (Foundational)
A detailed account of the clinical foundational implementation—architecture, metrics,
validation—appears in a companion paper
[
14
]
currently under
review at
IEEE Instrumentation & Measurement Magazine
.
The TRACE layer projection is:
•
L1:
Rule-based clinical logic, compatible with the FUTURE-AI
traceability principle
[
1
]
.
•
L2a:
Classical ML for structured prediction: risk scores,
vital-sign time-series classification, laboratory data modelling.
•
L2b:
LLM validator for free-form clinical notes;
contextual consistency checking of recommendations against patient history.
•
L3:
Clinical escalation policy: routine cases are handled by L2a
risk scores with calibrated probabilities; at boundary confidence or with a
complex context, L2b is invoked for free-form data verification; on joint
high-risk / high-confidence coincidence, or L3-detected inconsistency between
L2a and L2b, mandatory clinician hand-off is triggered.
Compatible with the TAO pattern
[
3
]
but with explicit L1/L2/L3
separation.
•
L4:
Clinician as final reviewer, aligned with the TRIAD
collaboration framework
[
2
]
.
3.2
Instance B: Industrial Multi-Domain Platform (Foundational)
Figure 2:
Sub-domain
×
\times
layer matrix for Instance B (industrial multi-domain
platform). The same four-layer architecture manifests differently across three
sub-domains: in Technology and Operations, L2a (classical ML) dominates;
in Administrative, the dominant pair is L1 (compliance rules) and L2b
(semantic contract review). Model parsimony applies adaptively to the evidence
type of each sub-domain. L3 is realised as an independent Escalation Policy
in each sub-domain; a master orchestrator coordinates cross-sub-domain pipelines.
Attribution and scope.
Instance B is an independently developed industrial agentic-AI platform for upstream
oil-and-gas operations, designed by Shcherban
(2024–2026)
[
15
,
16
]
.
The system simultaneously spans three operational sub-domains:
technology
(drilling, production, well operations),
operations
(maintenance, condition monitoring), and
administrative
(procurement, contract lifecycle, compliance).
This system serves here as a structural reference exhibiting the TRACE pattern in a
domain principally different from clinical decision support; detailed methodology,
operational statistics, and component-level specifications are reported separately by
the system’s developer (Paper 2, in preparation).
Architectural projection on TRACE layers.
At the level of architectural pattern visible in the public record of the system, each
sub-domain instantiates all four TRACE layers, but with characteristically different L2
weighting (Figure
2
):
the
technology
and
operations
sub-domains are
L2a-dominant
, since
the bulk of inference operates over structured, low-latency sensor and equipment-state
signals where classical and specialised ML satisfy calibration and reproducibility
requirements at substantially lower cost than LLMs;
the
administrative
sub-domain is
L1+L2b-dominant
, since regulatory and
contractual rules must be formally specified rather than learned (L1), while semantic
review of free-form contract text and unstructured documents is the natural target for
LLM validators (L2b).
A master orchestrator coordinates cross-sub-domain pipelines
(e.g., the chain procurement
→
\to
contract
→
\to
compliance check
→
\to
operational
integration when new downhole equipment is introduced) and aggregates TRACE metrics
across sub-domains, enabling measurement of operational stability for the platform as a
whole.
Significance for TRACE.
At the level of structural pattern, Instance B demonstrates three claims that motivated
TRACE’s formalisation:
(i) the parsimony principle is empirically natural—two of three sub-domains are
L2a-dominant despite the broader trend of LLM-default deployment;
(ii) the sub-domain
×
\times
layer matrix (§
2.3
) is documented in a
real-world design precedent;
(iii) the architecture transfers across principally different evidence types (sensor
signals vs. legal documents) within a single platform.
Component-level validation of these claims belongs to the domain paper.
3.3
Instance C: Judicial AI Assistant (Partially Implemented)
L1—procedural and substantive legal norms
[
23
,
24
]
.
L2a—classical classifiers for document categorisation, precedent relevance ranking,
NER for parties and circumstances.
L2b—LLM for case-material analysis, precedent semantic correlation, draft document
preparation.
Empirical anchor: Magesh et al.
[
25
]
report a 17%
hallucination rate in commercial legal RAG systems, providing direct motivation for
multi-layer trust oversight.
L3—legal escalation policy: L2a/NER retrieval selects relevant precedents;
L2b mandatory hallucination verification; at high claim stakes and a confident
recommendation, juridical L4 review is required before execution.
L4—legal professional (judge, assistant)
[
26
]
.
Instance C is currently partially implemented as an AI assistant for judicial-decision
analysis within the EU project “Pravo-Justice” — “Support of the Supreme
Court on improving (modernising) the Database of Legal Positions”
(funded by Expertise France)
[
27
,
28
]
.
This serves as a demonstration of architectural portability: the same four-layer pattern
and the same metrics apply in a domain with a principally different governance context
(judicial ethics, burden of proof, procedural accountability).
3.4
Unity and Variation
Across all three instances the
same reference architecture, the same six principles,
and the same metric suite
apply—only the instantiated parameters and the L2a/L2b
split vary.
Instance B additionally demonstrates that the sub-domain
×
\times
layer matrix operates
within a single system for three sub-domains with principally different data types.
This invariance is the central empirical claim of the framework.
4
Discussion
4.1
Relation to TAO, Revisited
TAO
[
3
]
supplies two empirical facts that TRACE preserves and absorbs:
(i) tiered oversight reduces individual-agent error rates by 16.9–24.3% (Table 6);
(ii) confident errors in high-risk contexts are more dangerous than acknowledged
uncertainty (Fig. 15).
TRACE reinterprets both within a purely layered architecture:
(i) becomes the lower bound on the expected effect of any correctly configured L3 policy
operating over a heterogeneous L2 inventory;
(ii) becomes the precise specification of the L3
→
\to
L4 hand-off trigger
(joint risk
∧
\wedge
confidence).
TAO’s descending-vs-ascending capability finding—that descending is safer—is
reinterpreted as valid
within a single model class
and serves as a calibration
anchor for L3 policy, not as an architectural norm.
This interpretation is only visible after separating L2-concern (model-class selection)
from L3-concern (invocation policy), which TAO does not do.
4.2
Relation to Eywa: Complementary Decomposition
Eywa
[
4
]
and TRACE address overlapping problems from complementary
angles. Eywa provides a
protocol-level
answer to the question of how
heterogeneous foundation models and LLMs should communicate, with three concrete
instantiations (EywaAgent, EywaMAS, EywaOrchestra) and an empirical benchmark
(EywaBench) over nine scientific domains. TRACE provides an
architectural and
metrological
answer to the question of what layer-wise decomposition operationally
critical AI should adopt, and how the resulting trust properties should be measured.
The two are not competing: Eywa’s Tsaheylu protocol is a viable realisation of the
TRACE L2a
↔
\leftrightarrow
L2b boundary; conversely, TRACE supplies the L1
deterministic anchor, the L3 stateful policy, the L4 supervision layer, and the
GUM/VIM-grounded metric suite that Eywa, by design, does not address.
A natural integration path—layered TRACE architecture with a Tsaheylu-conformant
L2a/L2b interface—is left to follow-up work.
4.3
Parsimony as an Architectural Constraint
CPR introduces a quantitative parsimony metric into trustworthy-AI alongside accuracy,
calibration, and review burden.
Its practical value is twofold: the metric surfaces architectural overhead (an LLM
deployed where a gradient-boosted classifier satisfies the required calibration yields
CPR
≪
1
\ll 1
) and provides an auditable artefact for certification bodies
(e.g., under EU AI Act Art. 15
[
12
]
).
The architectural correlate of CPR is the L2a/L2b split: it makes the parsimony choice
a
visible
design decision rather than an implicit LLM-default bias.
Instance B makes this concrete: two of three sub-domains are naturally L2a-dominant;
an LLM-by-default deployment would be measurably over-engineered.
Limitations.
The Trust Metric Suite is currently specified analytically; empirical calibration from
production deployments is forthcoming in the domain-specific follow-up papers.
CPR requires operational benchmarking for normalisation against domain-specific cost
models.
Instance C is partially implemented; the EU project deployment covers judicial-decision
analysis but full operational statistics await the completion of Phase 2.
5
Conclusion
TRACE provides a metrologically grounded, cross-domain engineering framework for
trustworthy agentic AI in operationally critical domains.
Its four-layer architecture, six design principles, 17-metric trust suite, and CPR
parsimony metric synthesise four previously disconnected literature streams into a single
reusable engineering blueprint.
Two foundational precedents—clinical decision support and an industrial
multi-domain platform—validate the shared structural pattern that motivated
TRACE’s formalisation.
TRACE operationalises trust and model parsimony as engineering outcomes, shifting the
design question from “how intelligent is this model?” to “what is this system
permitted to do, on what grounds, under what supervision, with what measurable
uncertainty, and is the right type of model being used for each sub-task?”
Acknowledgements
The author thanks
Andriy Shcherban
, whose independently developed industrial
multi-domain platform served as the empirical catalyst for TRACE’s formalisation;
the structural pattern shared between that system and the clinical foundational
implementation motivated the abstraction presented here.
The clinical foundational implementation (Instance A) is reported separately by
S. Zabolotnii, V. Holinko, and O. Antonenko
[
14
]
;
the author thanks V. Holinko and O. Antonenko for the collaboration on that companion
work.
References
[1]
K. Lekadir, A. F. Frangi, A. R. Porras, B. Glocker, C. Cintas, C. P. Langlotz,
et al.
(2025)
FUTURE-AI: international consensus guideline for trustworthy and deployable artificial intelligence in healthcare
.
BMJ
388
,
pp. e081554
.
Note:
Correction: BMJ 2025;388:r340, doi:10.1136/bmj.r340
External Links:
Document
Cited by:
§1
,
1st item
.
[2]
J. Li, Z. Zhou, Z. Wang, H. Lv,
et al.
(2026)
Prioritizing human-AI collaboration in healthcare: the TRIAD framework for trustworthy governance, real-world value, and integrated adaptive deployment
.
Military Medical Research
12
,
pp. 97
.
Note:
DOI to be revalidated at camera-ready
External Links:
Document
Cited by:
§1
,
5th item
.
[3]
Y. Kim, H. Jeong, C. Park, E. Park, H. Zhang, X. Liu, H. Lee, D. McDuff, M. Ghassemi, C. Breazeal, S. Tulebaev, and H. W. Park
(2025)
Tiered agentic oversight: a hierarchical multi-agent system for healthcare safety
.
arXiv preprint arXiv:2506.12482v2
.
Note:
Accepted at ICML 2025; project page: https://tiered-agentic-oversight.github.io/; verify proceedings DOI before camera-ready
External Links:
Link
Cited by:
§1
,
§2.2
,
§2.2
,
4th item
,
§4.1
.
[4]
Z. Li, J. Zou, F. Fang, X. Ning, M. Ai, T. Wei, S. Chen, X. Yang, and J. He
(2026)
Eywa: heterogeneous scientific foundation model collaboration
.
arXiv preprint
.
Note:
Introduces the FM–LLM Tsaheylu interface; instantiations EywaAgent / EywaMAS / EywaOrchestra; benchmark EywaBench across 9 scientific domains.
External Links:
2604.27351
,
Link
Cited by:
§1
,
§2.2
,
§2.4
,
§4.2
.
[5]
S. Bilson, M. Cox, A. Pustogvar, and A. Thompson
(2025)
A metrological framework for uncertainty evaluation in machine learning classification models
.
Metrologia
62
(
6
),
pp. 064001
.
External Links:
Document
Cited by:
§1
,
item 5
,
§2.4
,
§2.4
.
[6]
A. Thompson, T. Adel, S. Bilson, and M. Levene
(2024)
Trustworthy artificial intelligence in the context of metrology
.
In
Producing Artificial Intelligent Systems: The Roles of Benchmarking, Standardisation and Certification
,
Note:
arXiv:2406.10117
External Links:
Document
Cited by:
§1
,
§2.4
.
[7]
P. Belcak, G. Heinrich, S. Diao, Y. Fu, X. Dong, S. Muralidharan, Y. C. Lin, and P. Molchanov
(2025)
Small language models are the future of agentic AI
.
arXiv preprint arXiv:2506.02153
.
Note:
NVIDIA Research position paper
External Links:
Document
Cited by:
§1
,
item 6
.
[8]
R. Schwartz, J. Dodge, N. A. Smith, and O. Etzioni
(2020)
Green AI
.
Communications of the ACM
63
(
12
),
pp. 54–63
.
External Links:
Document
Cited by:
§1
,
item 6
.
[9]
E. Tabassi
(2023)
Artificial intelligence risk management framework (ai rmf 1.0)
.
NIST AI 100-1
National Institute of Standards and Technology
.
External Links:
Document
Cited by:
§1
.
[10]
National Institute of Standards and Technology
(2024)
Artificial intelligence risk management framework: generative artificial intelligence profile
.
NIST AI 600-1
NIST
.
External Links:
Document
Cited by:
§1
.
[11]
ISO/IEC
(2023)
ISO/IEC 42001:2023 — information technology — artificial intelligence — management system
.
ISO/IEC
.
Note:
International Standard
External Links:
Link
Cited by:
§1
.
[12]
European Parliament and Council of the European Union
(2024)
Regulation (eu) 2024/1689 of 13 june 2024 laying down harmonised rules on artificial intelligence (AI Act)
.
Note:
Official Journal of the European Union, L 2024/1689, 12 July 2024
External Links:
Link
Cited by:
§1
,
§4.3
.
[13]
A. Herrera-Poyatos, J. Del Ser, M. Lopez de Prado, F. Wang, E. Herrera-Viedma, and F. Herrera
(2025)
A framework for responsible AI systems: building societal trust through domain definition, trustworthy AI design, auditability, accountability, and governance
.
arXiv preprint arXiv:2503.04739
.
External Links:
Link
Cited by:
§1
.
[14]
S. Zabolotnii, V. Holinko, and O. Antonenko
(2026)
From black-box confidence to measurable trust in clinical AI: a framework for evidence, supervision, and staged autonomy
.
IEEE Instrumentation and Measurement Magazine
.
Note:
arXiv:2604.26671. Special Issue "A Measure of Trust in Healthcare" (guest editors: O. Postolache, A. Solanas); submitted April 2026, under review. Update volume/issue/pages before camera-ready.
External Links:
Document
,
Link
Cited by:
§1
,
§3.1
,
Acknowledgements
.
[15]
A. Shcherban
(2025)
A method for controlling the drilling process at oil and gas fields using agentic artificial intelligence
.
Note:
Ukrainian Utility Model Patent ApplicationFiled 19 August 2025; applicant: A. Shcherban. Status: utility model application.
Cited by:
§1
,
§3.2
.
[16]
A. Shcherban
(2026)
Agentic AI for upstream operational intelligence: A unified framework
.
Note:
U.S. Copyright Office (deposit copy submitted)Submitted 15 March 2026; application number pending final registration confirmation. Update before camera-ready.
Cited by:
§1
,
§3.2
.
[17]
JCGM
(2012)
International vocabulary of metrology — basic and general concepts and associated terms (VIM), 3rd edition
.
BIPM Joint Committee for Guides in Metrology
.
Note:
JCGM 200:2012
Cited by:
item 1
.
[18]
E. Mosqueira-Rey, E. Hernández-Pereira, D. Alonso-Ríos, J. Bobes-Bascarán, and Á. Fernández-Leal
(2023)
Human-in-the-loop machine learning: a state of the art
.
Artificial Intelligence Review
56
(
4
),
pp. 3005–3054
.
External Links:
Document
Cited by:
item 2
.
[19]
JCGM
(2008)
Evaluation of measurement data — guide to the expression of uncertainty in measurement (GUM)
.
BIPM Joint Committee for Guides in Metrology
.
Note:
JCGM 100:2008
Cited by:
item 5
,
§2.4
.
[20]
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
(2017)
On calibration of modern neural networks
.
In
Proceedings of the 34th International Conference on Machine Learning (ICML)
,
PMLR
, Vol.
70
,
pp. 1321–1330
.
Note:
arXiv:1706.04599
Cited by:
1st item
,
§2.4
.
[21]
G. Menghani
(2023)
Efficient deep learning: a survey on making deep learning models smaller, faster, and better
.
ACM Computing Surveys
55
(
12
),
pp. 259:1–259:37
.
External Links:
Document
Cited by:
1st item
.
[22]
Y. Dong, W. Huang, V. Bharti, V. Cox, A. Banks, S. Wang, X. Zhao, S. Schewe, and X. Huang
(2023)
Reliability assessment and safety arguments for machine learning components in system assurance
.
ACM Transactions on Embedded Computing Systems
22
(
3
),
pp. 39:1–39:48
.
External Links:
Document
Cited by:
§2.4
.
[23]
Council of Europe / CEPEJ
(2018)
European ethical charter on the use of artificial intelligence in judicial systems and their environment
.
Note:
Strasbourg, 3–4 December 2018
External Links:
Link
Cited by:
§3.3
.
[24]
Council of Europe / CEPEJ
(2025)
Operationalisation of the CEPEJ ethical charter — assessment tool
.
CEPEJ(2023)16rev
Council of Europe
.
Note:
Revised 5 June 2025
Cited by:
§3.3
.
[25]
V. Magesh
et al.
(2025)
Hallucination-free? assessing the reliability of leading AI legal research tools
.
Journal of Empirical Legal Studies
22
,
pp. 216
.
Cited by:
§3.3
.
[26]
D. Kolkman, F. Bex, N. Narayan, and M. van der Put
(2024)
Justitia ex machina: the impact of an AI system on legal decision-making and discretionary authority
.
Big Data & Society
11
(
2
).
External Links:
Document
Cited by:
§3.3
.
[27]
High Qualification Commission of Judges of Ukraine
(2024)
The European Union funded project “Support to Justice Sector Reforms in Ukraine (PRAVO-JUSTICE III)”
.
Note:
https://vkksu.gov.ua/en/page/european-union-funded-project-support-justice-sector-reforms-ukraine-pravo-justice-iii
Implementing agency: Expertise France S.A.S.; duration:
January 2024 – June 2026
Cited by:
§3.3
.
[28]
EU Project Pravo-Justice
(2024)
Database of legal positions of the Supreme Court: Uniformity of jurisprudence online
.
Note:
https://www.pravojustice.eu/en/post/baza-pravovih-pozicij-verhovnogo-sudu-yednist-sudovoyi-praktiki-onlajn-en
Implemented by Expertise France; funded by the European Union
Cited by:
§3.3
.