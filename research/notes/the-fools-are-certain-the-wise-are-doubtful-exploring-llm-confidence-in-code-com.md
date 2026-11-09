---
title: 'The Fools are Certain; the Wise are Doubtful: Exploring LLM Confidence in
  Code Completion'
id: the-fools-are-certain-the-wise-are-doubtful-exploring-llm-confidence-in-code-com
tags:
- aaai-bar-eval-dprc-d78e07
- evaluation-scale-precedent
- contamination-control
created: '2026-07-19T20:04:59.720466Z'
updated: '2026-07-19T20:06:38.121780Z'
source: https://arxiv.org/html/2508.16131
source_domain: arxiv.org
fetched_at: '2026-07-19T20:04:59.720108Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Kotti, Dritsa, Spinellis, Louridas (Athens U. of Economics and Business;
  arXiv:2508.16131, journal-style empirical study). NOT about calibration/verbalized
  confidence -- studies INTRINSIC code perplexity (not correctness-predictive confidence)
  as a function of programming language, model, and code characteristics. Evaluates
  12 open code-LLM checkpoints (LLaMA 3.2 3b/3 8b/3.1 8b/2 13b, CodeLlama 13b, CodeShell
  7b, Gemma 3 27b/4 31b, Mistral 7b, Mixtral 8x7b MoE, Qwen 3.5 27b, StarCoder2 15b)
  across 14 programming languages (C, C#, C++, CSS, Go, HTML, Java, JavaScript, Perl,
  PHP, Python, R, Ruby, Shell) on 2254 files sampled from 881 GitHub projects. Methodologically
  notable for CONTAMINATION CONTROL: explicitly builds its evaluation corpus from
  GNU-copyleft-licensed GitHub projects EXCLUDED from LLaMA''s permissive-license
  training set (Apache/BSD/MIT), filtering 785,567 candidate projects down to 114,160
  quality-filtered projects, then randomly sampling 1008 projects (72/language) and
  deduplicating via SHA-hash and a published project-deduplication dataset -- final
  corpus of 296,543 unique files, 2254 sampled for analysis. Key finding: strongly-typed
  languages have lower perplexity than dynamically-typed; Shell is universally high-perplexity,
  Java universally low; language-level perplexity rankings are moderately stable across
  models but not identical. Relevance to AAAI-bar question: this is a useful EXEMPLAR
  of the scale/rigor expected for empirical code-LLM measurement papers in this space
  -- 12 models x 14 languages with explicit contamination-avoidance methodology --
  though it does not itself address calibration, per-requirement confidence, or correctness
  prediction, making it evaluation-scale precedent rather than a direct competitor
  or baseline.'
---

The Fools are Certain; the Wise are Doubtful: Exploring LLM Confidence in Code Completion
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2508.16131v2 [cs.SE] 28 Apr 2026
[1]
\fnm
Zoe
\sur
Kotti
[1]
\orgdiv
Department of Management Science and Technology,
\orgname
Athens University of Economics and Business,
\orgaddress
\city
Athens,
\country
Greece
The Fools are Certain; the Wise are Doubtful:
Exploring LLM Confidence in Code Completion
zoekotti@aueb.gr
\fnm
Konstantina
\sur
Dritsa
dritsakon@aueb.gr
\fnm
Diomidis
\sur
Spinellis
dds@aueb.gr
\fnm
Panos
\sur
Louridas
louridas@aueb.gr
*
Abstract
Code completion entails the task of providing missing
tokens given a surrounding context. It can boost developer
productivity while providing a powerful code discovery tool.
Following the Large Language Model (LLM) wave, code completion has
been approached with diverse LLMs fine-tuned on code (code LLMs).
The performance of code LLMs can be assessed with downstream and
intrinsic metrics. Downstream metrics are usually employed to
evaluate the practical utility of a model, but can be unreliable and
require complex calculations and domain-specific knowledge. In
contrast, intrinsic metrics such as perplexity, entropy, and mutual
information, which measure model confidence or uncertainty, are
simple, versatile, and universal across LLMs and tasks, and can
serve as proxies for functional correctness and hallucination risk
in LLM-generated code. Motivated by this, we evaluate the confidence
of LLMs when generating code by measuring code perplexity across
programming languages, models, and datasets using various LLMs, and
a sample of 2254 files from 881 GitHub projects. We find that
strongly-typed languages exhibit lower perplexity than dynamically
typed languages. Scripting languages also demonstrate higher
perplexity. Shell appears universally high in perplexity, whereas
Java appears low. Code perplexity depends on the employed LLM; under
a fixed model, relative language-level rankings are moderately
stable across evaluation corpora. Although code comments often
increase perplexity, the language ranking based on perplexity is
barely affected by their presence. LLM researchers, developers, and
users can employ our findings to assess the benefits and suitability
of LLM-based code completion in specific software projects based on
how language, model choice, and code characteristics impact model
confidence.
keywords:
code completion,
large language models,
model confidence,
perplexity
“The fundamental cause of the trouble is that in the modern world
the stupid are cocksure while the intelligent are full of doubt.”
— Bertrand Russell
[
russell1998essays
]
1
Introduction
Code completion entails the task of providing missing tokens
given a surrounding context
[
kim2021code
]
.
It is commonly encountered in IDEs and powerful editors,
where it provides developers with code suggestions
based on the code they have already typed
[
wang2023review
]
.
Code completion can boost developer productivity
by generating entire code blocks or functions
(with varying degrees of correctness)
[
kim2021code
,
barke2022grounded
,
li2024acecoder
,
husein2025llms
]
.
At the same time,
it makes an unobtrusive code discovery tool
by allowing developers to stay in the same mental context
when looking for some functionality,
instead of browsing through developer question-and-answer websites
[
kim2021code
,
wang2023review
]
.
Similar to word prediction, Large Language Models (LLMs) can be leveraged
to predict code tokens based on semantic insights from existing code and comments,
provided they can be fine-tuned for code tasks using code data.
This has led to the development of specialized models for code
known as
code LLMs
[
pan2024lost
]
or
LLMs4Code
[
sharma2024llms
]
.
Code LLMs find applications in diverse software engineering tasks including
code generation
[
zan2023survey
]
,
code understanding
[
nam2024using
]
, and
code translation
[
pan2024lost
]
.
The performance of code LLMs can be assessed with two types of metrics:
downstream and intrinsic.
The former are usually employed to evaluate the practical utility of a model,
while the latter can assess model confidence or uncertainty.
Downstream metrics may not always be reliable,
and typically require domain-specific knowledge and complex calculations
[
huyen2019evaluation
,
liu2024evalplus
]
.
In contrast,
intrinsic metrics are simple, versatile, and universal
across LLMs and tasks
[
huyen2019evaluation
,
farquhar2024detecting
]
.
At the same time,
they provide valuable insights during the model training process
by helping the understanding of how effectively the model is learning
to make predictions from the training data
[
huyen2019evaluation
,
li2023starcoder
]
.
Such insights can be used to adjust the training strategy and model architecture.
Despite these advantages,
downstream metrics dominate current practice in code generation evaluation.
A recent review
[
hou2024large
]
found over 300 papers using 18 different downstream metrics including
BLEU Score
,
Pass@k
,
Accuracy/Accuracy@k
,
Exact Match
, and
CodeBLEU
.
Only one study
[
xu2022polycoder
]
employed perplexity
[
jelinek:1977
]
as a primary intrinsic metric,
highlighting an opportunity to assess LLM confidence more systematically.
This evaluation gap is further underscored by a growing focus on code hallucinations:
plausible-looking but incorrect code fragments that can mislead developers.
Researchers have recently introduced a taxonomy of hallucinations in code generation,
and a benchmark to detect such issues
[
agarwal2024codemirage
]
.
Complementary to hallucination detection,
understanding and quantifying model uncertainty (and by extension,
confidence
)
may offer early indicators of potential issues in generated code
before they are propagated into codebases
[
spiess2025calibration
]
.
Confidence evaluation metrics (
e
.
g
., entropy, mutual information, perplexity)
can serve as
proxies
for correctness and hallucination risk in LLM-generated code.
Sharma
et al.
[
sharma2025assessing
]
empirically showed that
higher entropy and mutual information correlate with lower functional
correctness.
In this work we focus on
perplexity
. Perplexity measures a
model’s confidence in predicting the next token based on the context
provided by the previous tokens
[
huyen2019evaluation
,
yang2024unveiling
]
. The higher the perplexity, the less confident a
model is: intuitively, the more perplexed a model is, the more
uncertain it is about its predictions. Perplexity has been found to be
positively correlated with error rate
[
bahl1983likelihood
]
. In
certain tasks (
e
.
g
., sentiment analysis, multi-genre natural language
inference, code completion, program synthesis) improved (that is,
lower) perplexity seems to improve end-task performance, thus
providing for practitioners a lightweight and early indicator of
potential issues in generated code
[
liu2019roberta
,
xu2022polycoder
,
nijkamp2023codegen
]
. As a consequence, perplexity,
as a confidence measure, can offer valuable support for risk
assessment and quality enhancement within development workflows. For
example, development teams could adopt a code review policy based on
the confidence of the LLM-generated code: highly confident code
suggestions could be reviewed more lightly than moderate- or
low-confidence ones
[
spiess2025calibration
]
.
Code produced by LLMs exhibits more consistent line-by-line perplexity
compared to human-authored code
[
xu2024detecting
]
.
Still,
limited research has been conducted on code perplexity through LLMs.
To fill this gap
in this study we investigate code perplexity
across diverse programming languages, models, and datasets
using multiple LLMs.
Specifically,
we set out to answer the following research questions:
RQ1
How does code perplexity vary across programming languages when measured through LLMs?
RQ2
How do intrinsic language properties and code structure features affect an LLM’s measured code perplexity?
RQ3
How does code perplexity vary across LLMs on a multilingual code corpus?
RQ4
How do different evaluation datasets affect an LLM’s measured code perplexity?
This study makes the following contributions:
•
A reproducible method and an open-source toolkit
for computing code perplexity using multiple LLMs,
enabling standardized evaluations across programming languages and datasets.
•
The first large-scale, language-specific analysis of
code perplexity measured through LLMs,
offering new insights into how model confidence varies across programming languages.
•
Analysis of the relationship between language properties and code structure features
and LLM perplexity,
showing that strongly-typed and more recent languages generally exhibit lower perplexity,
while comments increase it.
•
An assessment regarding the generalizability of code perplexity across LLMs and benchmark datasets,
providing patterns that can inform model selection and training strategies.
•
Contextualization of the findings in relation to prior work
on LLM confidence, uncertainty, and correctness,
highlighting the practical relevance of perplexity as a lightweight diagnostic indicator
in code generation tasks.
In the following section we present an overview of related work
on code completion powered by LLMs, and
approaches for their evaluation.
We then describe the study methods in Section
3
,
present the research results in Section
4
, and
discuss their implications in Section
5
.
The study is complemented by considering its limitations
in Section
6
,
followed by our concluding remarks in Section
7
.
We provide any references to source code through permalinks
based on Software Hash Identifiers (SWHIDs—
ISO18670:2025
).
According to published guidelines
[
ince2012case
]
,
the code and produced data of our study are publicly available
online,
1
1
1
https://doi.org/10.5281/zenodo.10886458
and
can be used for replication or further empirical research.
2
Related Work
We classify related work into three main axes:
i) code attributes and naturalness;
ii) code completion with LLMs; and
iii) evaluation of code LLMs.
We then present the novelty our research offers
with respect to existing research.
2.1
Code Attributes and Naturalness
The naturalness hypothesis
[
allamanis2018naturalness
]
suggests that code,
like natural language,
serves as a means of human communication
[
knuth1984literate
]
, and
shares exploitable linguistic properties.
Hindle
et al.
[
hindle2012naturalness
]
showed that code,
modeled with
n
-grams, is even more predictable than text.
Ray
et al.
[
ray2016buggy
]
found buggy code to be more entropic, and
thus less natural to language models.
Various strategies have been developed to handle the high rate of new or rare vocabulary
introduced by identifier names
[
karampatsis2020vocab
,
sharma2024survey
]
.
Ultimately, code’s repetitive nature,
well-captured by Natural Language Processing-driven models,
enables the development of effective tools for software engineers.
2.2
Code Completion with LLMs
Most studies on LLM-based code completion either propose new models or
conduct empirical research.
Notable open code LLMs include
StarCoder
[
li2023starcoder
]
,
CodeGeeX
[
zheng2023codegeex
]
,
LLaMA
[
touvron2023llama
,
touvron2023llama2
]
,
CodeLlama
[
roziere2024code
]
,
SantaCoder
[
allal2023santacoder
]
,
PolyCoder
[
xu2022polycoder
]
,
InCoder
[
fried2023incoder
]
, and
CodeGen
[
nijkamp2023codegen
]
.
Empirical research largely focuses on
Copilot
[
wang2023review
]
, examining its
applications
[
moroz2022potential
]
, impact on
productivity
[
ZKLR24
]
, and developer
interaction
[
barke2022grounded
]
.
Copilot
serves as both
an acceleration and exploration tool, enhancing productivity and
assisting with unfamiliar tasks
[
barke2022grounded
]
. An early
study showed that, despite its benefits, improvements are needed in
security, reliability, and effectiveness
[
moroz2022potential
]
.
Since then, and with the accompanying improvements in LLMs, use of
Copilot has been shown to increase developer productivity as the acceptance
rates of its suggestions correlate with productivity
gain
[
ZKLR24
,
cui:2024
,
shihab:2025
,
bakal:2025
]
.
2.3
Evaluation of Code LLMs
Here we review the main evaluation frameworks, surveys, and empirical studies on code LLMs.
2.3.1
Evaluation Frameworks
Liu
et al.
[
liu2024evalplus
]
propose
EvalPlus
,
a benchmarking framework for assessing the functional correctness of LLM-generated code.
It expands an initial dataset using LLM- and mutation-based input generators
to validate completions.
Testing 14 LLMs including
GPT-4
and
ChatGPT
reveals
many previously undetected errors,
lowering
pass@k
by 15.1% on average.
This suggests existing evaluations may overestimate code correctness.
Ding
et al.
[
ding2023static
]
propose a static evaluation framework
for Python code completions, parsing snippets into Abstract Syntax Trees (ASTs) and
analyzing them with
Pyflakes
.
2
2
2
https://github.com/PyCQA/pyflakes
They evaluate 100K function completions from the
CodeGen
models
[
nijkamp2023codegen
]
,
finding most AST errors stem from incomplete generations due to length limits,
while static errors mainly involve
Undefined Name
and
Unused Variable
.
Higher temperatures degrade performance,
and larger model sizes show mixed effects—reducing undefined variables
but increasing undefined methods.
Errors in prompts often propagate to completions,
highlighting LLMs’ in-context learning.
Wang
et al.
[
wang2023recode
]
introduce
ReCode
, a
robustness evaluation framework for LLM-generated code. It applies
natural, semantics-preserving transformations (
e
.
g
., on docstrings,
variable names, code syntax and format). Evaluating models like
CodeGen
[
nijkamp2023codegen
]
,
InCoder
[
fried2023incoder
]
, and
GPT-J
[
wang2021gptj
]
shows that while larger models and
diverse pretraining data improve robustness, they reduce
generalizability. Models are particularly sensitive to syntax changes.
2.3.2
Surveys
Chang
et al.
[
chang2024survey
]
review LLM performance across domains
including code generation.
They find that
CodeGen-16B
[
nijkamp2023codegen
]
performs comparably
to
ChatGPT
with more parameters.
While
ChatGPT
struggles with data structures and graph theory,
it surpasses college students in dynamic programming, greedy algorithms, and search.
GPT-4
excels in code generation, understanding, and reasoning.
Zheng
et al.
[
zheng2024survey
]
review the evolution,
benchmarking, and future trends of code LLMs. The
CodeLlama
series
[
roziere2024code
]
leads in code generation, while
ToolCoder
[
zhang2023toolcoder
]
excels in API-based code
generation.
GPT-4
and
GPT-3.5
dominate test case
generation. Comparisons show that, with similar parameter sizes, code
LLMs outperform general LLMs, and current State-of-the-Art (SOTA) code
LLMs surpass general LLMs in code generation.
Husein
et al.
[
husein2025llms
]
review LLMs for code completion,
noting productivity gains across all granularity levels in IDEs.
Larger datasets help prevent overfitting,
but performance varies by language and dataset.
Dynamically typed languages like Python pose challenges due to their flexible type information,
while statically typed languages like Java provide clearer context.
In Python, the low relevance of context lines increases ambiguity,
making precise completions harder.
2.3.3
Empirical Studies
Izadi
et al.
[
izadi2024language
]
evaluated three public code LLMs
(
InCoder
—
fried2023incoder
,
UniXcoder
—
guo2022unixcoder
,
CodeGPT
—
lu2021codexglue
)
using real auto-completion data.
The models perform better in common languages like Python and Java
but struggle with less popular ones such as Rust and Scala.
InCoder
is the most performant,
suggesting superior training data and objectives.
However, all models show a high failure rate (66.3%),
with issues including incorrect predictions and poor semantics.
The authors recommend improvements in training, error tolerance, usability, and hybrid systems.
Another systematic evaluation compares SOTA code LLMs
(
Codex
—
chen2021codex
,
GPT-J 6b
—
wang2021gptj
,
GPT-Neo 2.7b
—
black2021gptneo
,
GPT-NeoX 20b
—
black2022gptneox
,
CodeParrot
—
tunstall2022natural
) across programming
languages using perplexity (
xu2022polycoder
,
cf.
2.4
below). Despite
Codex
’s
commercial advantage, open-source models perform comparably in some
languages. To address the need for a multilingual code model,
PolyCoder
(2.7b parameters, GPT-2 based) was trained on 249GB
of code in 12 languages. It ranked fourth overall, behind
Codex
and
GPT-Neo/J
, but led in C language performance.
Yang
et al.
[
yang2024unveiling
]
empirically analyze
the memorization ability of large code models
using variations of the perplexity metric.
Lower perplexity often indicates higher memorization,
especially on seen examples.
Models memorize various content types including
documentation,
licenses,
sensitive information, and
code logic.
Memorization is influenced by factors such as
model size,
top-
k
sampling,
output length,
number of outputs, and
fragment frequency,
suggesting that deduplication of training data can help reduce memorization.
Zhou
et al.
[
lexin2024largerlessreliable
]
show that
larger, more instructable LLMs can be less reliable than smaller ones,
often producing incorrect answers to difficult questions missed by human evaluators.
Their study assesses several LLMs
using six reliability indicators focused on
response proportion,
prompting stability, and
difficulty concordance.
Liu
et al.
[
liu2024empirical
]
present a case study
on using
GPT-4
for safety-critical software generation,
introducing
Prompt-FDC
,
a prompt engineering method combining
functional requirements,
domain features, and
constraints.
Their approach enhances
code completeness,
compliance,
readability,
maintainability, and
comment coverage,
showing that with proper prompting,
LLMs can meet production engineering standards.
2.4
Research Novelty
What is, and is not, novel
Perplexity is not a new concept for LLM evaluation; several
code-oriented studies including
PolyCoder
[
xu2022polycoder
]
already report multilingual
or multi-model figures. The novelty of this work is not a single
definition, but the combination of: a confidence- and
comparability-driven design on a copyleft, LLaMA-complementary GitHub
sample; a reproducible strided sliding-window perplexity
implementation (Section
3.5
) with reruns
for 12 checkpoints in RQ3; and a broad set of empirical RQs
(properties of languages, structure features, cross-LLM agreement, and
cross-benchmark orderings) tied to the same file population.
Positioning with respect to PolyCoder
PolyCoder
introduces a new code LLM and situates it against
competitors
[
xu2022polycoder
]
, whereas we treat perplexity as an
instrument for evaluating model confidence in code completion under a
fixed, balanced GPL-centered file sample
(Section
3.2
).
PolyCoder
’s evaluation
sets vary strongly in files per language; our preprocessed draw keeps
languages more evenly represented for per-language medians, which
matters when ranking languages. Their reported pipeline aggregates
disjoint chunks, summing chunk log-likelihoods; we implement the
strided sliding-window approach so that each scored token, except for
short file heads, is predicted with up to the full allocated context
Moreover, we shorten the active window to the file length when a file
has fewer than 2048 tokens, so context is file-adaptive rather than a
small fixed cap on every file (Section
3.5
).
PolyCoder
also used a long (2048-token) window, but their
benchmark files are relatively short in the median (598 tokens), which
limits how many tokens receive a full long-context read in practice;
our balanced GPL sample, together with the stride, yields dense
coverage of each file under the strided policy.
Empirical distinctions beyond PolyCoder
Beyond dataset and model choices, our findings that extend
PolyCoder
’s multilingual perplexity evaluation are:
a systematic view of how 12 public
checkpoints agree on language orderings, with a correlation map and
parallel coordinates (Section
4.3
); a quantified test of
whether median language orderings carry over to the
PolyCoder
file set under the same model (Section
4.4
); probes for
comments, typing, age, and size, including tests where appropriate
(Section
4.2
), along with a discussion that separates how
much model change versus benchmark change moves perplexity, which was
not the target of the original
PolyCoder
study; and a
leakage-aware GPL sampling rationale tied to the evaluator model
family (
i
.
e
., controlling overlap with the model’s known training mix),
which is orthogonal to merely listing per-language perplexities in a
multi-language table. When we agree directionally with prior
observations (
e
.
g
., the role of static type
hints—
husein2025llms
), our contribution is complete quantitative
results on this corpus, a cross-model and cross-benchmark validation,
and a clear discussion of limitations from broad language categories and
limited sample size (
n
n
).
3
Methods
Our methods involve
selecting and preprocessing the code dataset of our analysis as well as
selecting, configuring, and running an LLM for computing the perplexity of the dataset.
An overview of the methods is presented
through a UML information flow diagram in Figure
1
.
Google
BigQuery
GitHub dataset
Project license filtering
Project deduplication
Project quality filtering
Project sampling
Project bare cloning
File quality filtering
File deduplication
File sample selection
Code cleaning
Perplexity calculation
Evaluation of code
perplexity through LLM
X
Data source
X
Project preprocessing
X
File preprocessing
X
LLM evaluation
ńflowż
Figure 1
:
Information flow of study methods.
3.1
LLM Selection
We used Meta’s LLaMA 3.2 3b model
[
meta2024llama3_2
]
whose
weights are openly provided upon
request,
3
3
3
https://llama.com/llama-downloads/
has been
trained on code data, can run on a single conventional GPU, and comes
from a family of competitive LLMs for code
generation
[
roziere2024code
,
zheng2024survey
]
. The evaluation
corpus is intentionally built from GitHub projects that are
complementary to the code used to train
LLaMA
[
touvron2023llama
]
, as detailed in
Section
3.2
. We therefore adopt a LLaMA-series
checkpoint so that tokenizer vocabulary, subword segmentation, and the
train-test contamination controls sketched there apply to the same
model family being scored. Within the LLaMA 3.2 release, Meta ships
lightweight
text-only
checkpoints at 1b and 3b parameters,
whereas the larger 11b and 90b LLaMA 3.2 variants are multimodal
vision-language models
[
meta2024llama3_2
]
. Because perplexity
here is computed over textual code tokens, we restrict attention to
these text-only LLaMA 3.2 weights rather than the vision-capable
checkpoints.
Sections
4.1
,
4.2
, and
4.4
are set
on LLaMA 3.2 3b. Every perplexity statistic in those sections
therefore uses one fixed tokenizer and weights so that comparisons
across languages and features stay internally consistent.
Section
4.3
evaluates cross-model variability—including
how absolute perplexity scale and language-level ranking agreement
compare against larger decoder-only checkpoints from other
families—by repeating the same corpus and pipeline on 11
general-purpose and code-specialized checkpoints
besides
LLaMA 3.2 3b: CodeLlama 13b, CodeShell 7b, Gemma 3 27b, Gemma 4 31b,
LLaMA 2 13b, LLaMA 3 8b, LLaMA 3.1 8b, Mistral 7b, Mixtral MoE 8x7b,
Qwen 3.5 27b, and StarCoder 2 15b. Including LLaMA 3.2 3b yields 12
checkpoints in the pairwise and parallel-coordinate plots of
Section
4.3
.
3.2
Project Selection
To avoid evaluation overfitting we synthesized the dataset of the
analysis with code that is complementary to the code used to train
LLaMA
[
touvron2023llama
]
. Specifically, we created a dataset of
GitHub projects that were
not
used in LLaMA’s training dataset.
In LLaMA the authors queried the public
GitHub Activity Data
available on Google
BigQuery,
4
4
4
https://console.cloud.google.com/marketplace/product/github/github-repos
and only kept projects that are distributed under the (permissive)
Apache, BSD, and MIT licenses. Consequently, we used the same dataset
(snapshot 23 Feb 2023), and only kept (copyleft) GNU-licensed
projects. For this we queried Table
licenses
(snapshot 27 Nov
2022), and
identified 15 distinct licenses in all projects.
From these we filtered all copyleft licenses
(
gpl-2.0, gpl-3.0, agpl-3.0, lgpl-2.1
,
lgpl-3.0
).
We then selected from the table
licenses
all projects distributed with these licenses.
The total number of retrieved projects was 785 567.
3.3
Project Preprocessing
Project deduplication
We deduplicated the GPL projects on the project level using the
deduplication dataset by Spinellis
et al.
[
spinellis2020deduplication
]
. We mapped projects to
the source field of the deduplication dataset, and used the
corresponding target project. We kept projects not present in the
deduplication dataset, and also verified that final projects are not
present in the LLaMA initial project list.
From this process we kept 757 642 unique projects.
Project quality filtering
We filtered projects based on the following recommended quality
criteria
[
dabic2021sampling
,
kalliamvakou2015mining
,
sheoran2014watchers
]
. We kept projects with at least one star, one
fork, and a listed primary language. In addition, we filtered out
projects where the frequency of the primary language within the
projects was less than 1%. To retrieve these project metadata we
queried the GitHub GraphQL
API.
5
5
5
https://docs.github.com/en/graphql
In the end a total of 114 160 projects were retained.
Project sample selection
We selected a random sample of 1008 projects for experimentation
uniformly from all 14 languages included in the dataset (
i
.
e
., 72
projects per language),
6
6
6
C, C#, C++, CSS, Go, HTML, Java,
JavaScript, Perl, PHP, Python, R, Ruby, Shell
and used Git to clone
the
bare
projects with
𝑑𝑒𝑝𝑡ℎ
=
1
\mathit{depth}=1
. We strived for a
sample size that was large enough to provide a representative dataset,
but also manageable by our laboratory infrastructure and time
constraints. The employed
git-clone
configuration minimizes
storage wasted on data not needed by our study.
3.4
File Preprocessing
File quality filtering
We kept 430 359 files whose extensions belonged to the 14 languages
of the dataset. We created a list of file extensions per language
based on the list of
extensions
7
7
7
https://archive.softwareheritage.org/swh:1:cnt:af779c91e6a52ae9ffbd8fb566ae50e461d066f5;origin=https://github.com/github-linguist/linguist;visit=swh:1:snp:26c84095ee29473e8ec4ffa6bebc095d7ae47bf9;anchor=swh:1:rev:af34cb5e7ba4a40721f65a782e0e8ddacfbfe459;path=/lib/linguist/languages.yml
provided by the
github-linguist/linguist
project.
8
8
8
https://github.com/github-linguist
We
converted the extensions list to CSV format, and manually reviewed the
extensions of the languages with
𝑓𝑟𝑒𝑞𝑢𝑒𝑛𝑐𝑦
≥
1
%
\mathit{frequency}\geq 1\%
to
remove any redundant extensions.
File deduplication
Similarly to LLaMA training,
we deduplicated exact-matched files based on the Git-provided SHA sums,
retaining 296 543 unique files.
From an analysis of the SHA sums of the sampled projects it appears that
duplicate files are mostly empty
__init__.py
and empty-body
index.html
files
(
<html><body></body></html
).
File sample selection
We classified each sampled project into multiple languages based on the extensions of its files.
We then performed language-level file sampling while ensuring a
balanced representation of the projects using a combination of
stratified and random sampling. For sample size we used the number of
files of the language with the lowest file representation (
i
.
e
., R-Project, 161 files). We did this to include as many files as
possible but also equal in number across languages. Therefore, for
each language, we sampled 161 files in total from as many projects as
possible,
leading to a final set of 2254 sampled files from 881 distinct projects.
Code cleaning
We first decoded all 2254 source code files after detecting their
encoding with the
chardet
Python
library.
9
9
9
https://github.com/chardet/chardet
Next we
removed any boilerplate header comments from the files,
i
.
e
., non-code-related headers such as license notices, copyright
statements, version tags, and author attributions. For this we used
the
pygments
library
10
10
10
https://pygments.org/
to
tokenize the files, and then detected and removed the following
comment types occurring at the file start (until the first non-comment
line is found):
Comment.Multiline
,
Comment.Single
, and
Comment.Special
. We skipped any comments of type
Comment.Hashbang
or
Whitespace
. We also kept any
String.Doc
header comments because these mainly include
code-related comments. To conclude that we identified all
String.Doc
header comments in our sampled projects, and
manually reviewed a random sample of 50 such comments.
3.5
Perplexity Implementation
Mathematically, perplexity is defined as the exponentiated
cross-entropy loss of a prediction sequence
[
jelinek:1977
]
.
Given a tokenized sequence
X
=
(
x
1
,
x
2
,
…
,
x
N
)
X=(x_{1},x_{2},...,x_{N})
it can be
calculated as:
Perplexity
​
(
X
)
=
2
−
1
N
​
∑
i
=
0
N
lg
⁡
p
​
(
x
i
|
x
<
i
)
\mathrm{Perplexity}(X)=2^{-\frac{1}{N}\sum_{i=0}^{N}\lg{p\left(x_{i}|x_{<i}\right)}}
(1)
In LLMs, the tokenized sequence is the sequence of predictions. If the
model is very confident in its prediction, each
p
​
(
x
i
|
x
<
i
)
p(x_{i}|x_{<i})
will
be equal to one and the perplexity will be one. If the model gives
equal probability to each word for all predictions, then the
perplexity will be equal to the size of the vocabulary.
Initially we experimented with Hugging Face’s method for computing
perplexity for fixed-length
models.
11
11
11
https://web.archive.org/web/20250518012847/https://huggingface.co/docs/transformers/perplexity
The method comes with an implementation example with GPT-2 using the
Hugging Face Transformers
library.
12
12
12
https://web.archive.org/web/20250511140609/https://huggingface.co/docs/transformers/index
We used this implementation after replacing the
WikiText-2
dataset with our preprocessed (untokenized) source code files, and
GPT-2 with LLaMA 3.2, which is also supported by Hugging
Face.
13
13
13
https://web.archive.org/web/20250419160227/https://huggingface.co/blog/llama32
However, this implementation was too slow on our laboratory machines,
and we also detected some potential memory leakage.
Therefore, we developed a Python driver for file-level perplexity
that loads a
llama.cpp
model
14
14
14
https://github.com/ggml-org/llama.cpp
via the Python bindings provided by the
llama-cpp-python
library.
15
15
15
https://github.com/abetlen/llama-cpp-python
We used the
cuBLAS
build, which provides BLAS acceleration
using the CUDA cores of our NVIDIA A100 PCIe 80 GB GPU.
We retrieved the LLaMA 3.2 3b checkpoint from Hugging Face, and
converted it to
GGUF F16
format
with the
convert_hf_to_gguf.py
script
by
ggml-org/llama.cpp
.
16
16
16
https://archive.softwareheritage.org/swh:1:cnt:42d559dfecf91ed33dfc9183f586eef3c6a2b9f9;origin=https://github.com/ggml-org/llama.cpp;visit=swh:1:snp:481de56e1a7d5e2e6a03219a657d2bbf677a0f5d;anchor=swh:1:rev:45cac7ca703fb9085eae62b9121fca01d20177f6;path=/convert_hf_to_gguf.py
This stack was fast enough for our large-scale runs, and
did not exhibit the slowdown and suspected memory issues we saw
with the Transformers-based prototype.
Although perplexity is mathematically defined as above, it is not
feasible, nor optimal, to compute it following the exact mathematical
formula. Regarding optimality, LLMs generate tokens using previous
tokens as context. Therefore to guard against volatile predictions
because of lack of sufficient context, we want to calculate perplexity
after an initial number of tokens in the sequence. Regarding
feasibility, LLMs have limits on the number of tokens they can take as
input (their context window). That means that we have to break the
input into windows and feed them to the LLM. Even when LLMs have
long-enough windows (and they get longer with time), using them
requires more resources, which may be beyond a study’s limits.
There are two ways to break the sequence into windows that constitute
the context. In the first approach, windows are not overlapping. All
tokens in the context are evaluated by causal attention. Then we start
at the middle of the context window and calculate the negative
log-likelihood of the prediction of the first, second,
etc
., tokens
from that point until the end of the window. Therefore the first token
from the middle uses half of the context for its perplexity, the
second token from the middle adds the first token in the context of
its perplexity, until the last token of the window that has all the
previous tokens of the window as its context. Note that as the windows
are non-overlapping, only half of the tokens of the sequence are used
for calculating the perplexity; see
Figure
2(a)
.
In the second approach, the windows are overlapping; the length of
their non-overlapping part is the
stride
. Perplexity is
calculated over the last stride tokens of each sliding window. That
means that only the tokens of the first window up to the stride do
not have their perplexity calculated; see
Figure
2(b)
. For example, given a sequence of
2000 tokens and a context size of 1024, the sliding window strategy
with stride equal to 1 produces overlapping chunks such as tokens 0–1023,
1–1024, 2–1025, and so on. Each window is used to evaluate the
log-likelihood of its final token.
(a)
(b)
Figure 2
:
Perplexity calculation with sliding window context and:
(a) without stride,
(b) with stride.
In both panels, context window is hatched, perplexity calculation is on the
cross-hatched regions.
The strided method is more accurate, but requires more calculations:
the computation for stride equal to 1 is context size times more than
the non-stride calculation. As a compromise, our perplexity program
loads each model with context size set to 2048, and invokes the driver
with stride equal to 512; to ensure adequate context, it uses the
first 512 tokens of the first window as context for starting the
predictions with the following token. When a file has fewer than 2048
tokens the implementation shortens the working window to the tokenized
file length and the starting context to half that, so the effective
context is adaptive per file instead of padding or forcing a very
small static cap. All figures in Section
4
that
reference this configuration use the same strided policy; RQ4 reuses
it on the
PolyCoder
files.
4
Results
Below we present our results with respect to
the research questions outlined in Section
1
.
Our key takeaways are set in
italics
in shaded boxes.
4.1
RQ1: How does code perplexity vary across
programming languages when measured through LLMs?
Figure 3
:
Perplexity across programming languages.
In Figure
3
we present the perplexity box plots per
programming language after removing outliers. Languages are sorted in
ascending order of median perplexity. Lower perplexity suggests that
the model has a better predictive ability regarding the code syntax
and semantics, leading to more accurate predictions. We observe that
Java, C#, Go, and PHP have the lowest (best) perplexity, while Shell,
C, R, and Perl demonstrate the highest (worst) perplexity. Thus, code
perplexity varies by programming language. Developers can use this
ranking to assess which of their software projects, based on their
language, could derive greater benefit from LLM assistance.
Furthermore, one can argue that less readable languages have higher
perplexity
[
husein2025llms
]
; Perl, for instance, has been
famously described as a “write-only” language
[
SFP11
]
.
Finding 1
Code perplexity varies by programming language.
A possible factor for the differences in perplexity could be that
LLaMA has been trained on more projects in some languages and then
could be more confident in them. To check this, we investigated the
effect of the language distribution in the LLaMA training data on code
perplexity. We retrieved the primary language of the projects that we
found to be in the LLaMA training data (see
Section
3.2
) by querying again the GitHub
GraphQL API as in Section
3.3
.
Figure
4
plots,
for each language, the percentage of projects in the LLaMA training
data against median code perplexity.
Figure 4
:
Language distribution in LLaMA training data versus perplexity.
JavaScript has the largest training share, but its median perplexity
is only mid-range. Java combines high training share with low median
perplexity, while Shell combines low share with higher perplexity.
Because the sample contains only 14 languages, those contrasts can
still steer an informal fit slightly downward. That tilt reflects
leverage from a few languages rather than a robust pattern across all
of them. We quantified the association over the
n
=
14
n=14
languages, but
we found no statistical significance at
α
=
0.05
\alpha=0.05
:
Pearson
r
=
−
0.14
r=-0.14
(
p
≈
0.62
p\approx 0.62
) and Spearman
ρ
=
−
0.44
\rho=-0.44
(
p
≈
0.12
p\approx 0.12
). Taking out JavaScript and Shell as outliers did
not result in statistically significant results. Taken together, these
results do not support a systematic effect of training-language
distribution on code perplexity.
Finding 2
The hypothesis that the language distribution in the LLaMA training
data affects code perplexity is not supported.
4.2
RQ2: How do intrinsic language properties and code structure features affect an LLM’s measured code perplexity?
After observing perplexity variation across programming languages
we aimed to identify which intrinsic language properties and code structure features
might explain these differences in model performance.
Specifically, we investigated the effect of
code comments,
language typing,
language age,
code size and vocabulary size on code perplexity.
To investigate the effect of comments on code perplexity
we preprocessed the sampled files of all languages by removing
any boilerplate header comments (see Section
3.4
).
We proceeded to investigate whether comments do affect perplexity
by re-running the perplexity program on a second sample of files selected with the same methods
detailed in Section
3.4
,
where the code cleaning step additionally removed all remaining comments
(inline and block comments throughout the file body).
Both samples therefore share the same boilerplate-free baseline;
the only difference is the presence or absence of those in-body comments.
At a file level, comments increase perplexity: A Wilconxon signed-rank
test for the 2232 paired fails finds a significant difference
(
W
=
463 027
W=463\,027
,
p
≈
0
p\approx 0
). A plausible hypothesis is that natural
language in comments is on average less predictable, under the same
next-token model, than the surrounding program tokens. However, this
does not affect the language perplexity rankings.
Figure
5
visualizes the median perplexity
of the two samples (
i
.
e
., with and without comments).
17
17
17
Since the study’s goal is not to evaluate prediction models or
create a new prediction model, in the remainder of the analysis we
retain the initial boilerplate-cleaned (but comment-inclusive) file
sample.
Finding 3
Code comments increase perplexity but do not affect the language
perplexity ranking.
Figure 5
:
Perplexity of files with versus without comments.
By observing the language ranking of Figure
3
we
identify a common characteristic of the languages placed at the top
and bottom of the ranking: the top-ranked languages are mainly
strongly typed, whereas the bottom-ranked ones are mainly dynamically
typed languages. A special case here is Python, which can exhibit
characteristics of both strong and dynamic typing.
In our dataset only one Python sample contains the arrow operator
(“
->
”) in positions consistent with typed return annotations
under our simple token-based scan, so we treat Python here as leaning
toward dynamic usage in practice. Scripting-oriented
languages
[
scott2025pragmatics
]
tend to sit higher in the
ranking, which is interesting considering that they often have simpler
surface syntax than some of the top-ranked languages, which can be
more verbose.
These observations align with previous
research
[
husein2025llms
]
, but are based on 14 languages and a
coarse binary split. To complement the narrative, we divided languages
into a strongly typed set (C, C#, C++, CSS, Go, Java) and a
scripting-oriented set (HTML, JavaScript, Perl, PHP, Python, R, Ruby,
Shell)—the same partition used when discussing
Figure
3
—and compared the two sets of
per-language median perplexities with a two-sided Mann-Whitney
U
U
test. We must note, however, that languages are neither independent
nor exchangeable units (for instance, we cannot meaningfully simply
swap C and Python between the two groups, as required by the
Mann-Whitney
U
U
test), labels are debatable (
e
.
g
., Python), and
n
=
14
n=14
is small. Therefore, we treat this only as exploratory: we obtain
U
=
9
U=9
and
p
≈
0.06
p\approx 0.06
(two-sided),
i
.
e
., no significant difference
at
α
=
0.05
\alpha=0.05
. A one-sided formulation aligned with “strong set
lower than scripting set” would yield
p
≈
0.03
p\approx 0.03
, but again we
emphasize that such testing is exploratory rather than confirmatory.
Finding 4
Coarse grouping suggests lower median perplexity for strongly typed
languages than for scripting-oriented languages in our sample, but
the pattern is not strong enough to exhibit statistical
significance.
(a)
(b)
Figure 6
:
Per-language median total tokens (a) and median unique tokens (b) versus median perplexity.
We also investigated whether perplexity correlates with the total size
or the vocabulary size of source code, influenced by the work of
Karampatsis
et al.
[
karampatsis2020vocab
]
, who demonstrate
that large vocabularies can negatively impact model performance and
scalability.
18
18
18
Perplexity, by definition, depends on the
vocabulary size; but the dependency is on the vocabulary size of the
LLM, not the vocabulary size of the programming language.
Figures
6(a)
and
6(b)
plot,
for each language, the number of median total tokens and median unique
tokens of the preprocessed files against median perplexity. We
computed Pearson and Spearman correlations between those
language-level medians, as we did for
Figure
4
in
Section
4.1
. For total tokens, Pearson
r
=
−
0.42
r=-0.42
(
p
≈
0.14
p\approx 0.14
) and Spearman
ρ
=
−
0.29
\rho=-0.29
(
p
≈
0.31
p\approx 0.31
); for
unique tokens, Pearson
r
=
−
0.35
r=-0.35
(
p
≈
0.22
p\approx 0.22
) and
Spearman
ρ
=
0
\rho=0
(
p
=
1
p=1
), the latter reflecting extensive ties
in the rounded per-language unique-token medians. We also checked the
associations without HTML and Ruby, which appear as outliers. None of
these associations was statistically significant at
α
=
0.05
\alpha=0.05
; we
therefore do not infer an effect of file size or vocabulary size on
perplexity from these summaries.
Finding 5
Language-level correlational tests do not support a reliable association
between total size or vocabulary size of source code and perplexity.
Furthermore, we investigated how perplexity relates to each
programming language’s age. This was motivated by the observation that
language design principles have evolved over time, with more recent
languages typically featuring stronger typing systems and more
standardized syntax—characteristics that Husein
et al.
[
husein2025llms
]
found to provide clearer context
for code prediction models. In Figure
7
we
visualize the release dates of the programming languages against their
median perplexity. Qualitatively, languages at the low-perplexity end
(
e
.
g
., Go, C#, Java) were released more recently than several
high-perplexity languages (
e
.
g
., Shell, C). At language granularity
(
n
=
14
n=14
), Pearson correlation yields
r
=
−
0.68
r=-0.68
(
p
≈
0.008
p\approx 0.008
) and
Spearman
ρ
=
−
0.73
\rho=-0.73
(
p
≈
0.003
p\approx 0.003
) between year and median
perplexity,
i
.
e
., younger languages’ years are associated with lower
median perplexity.
Finding 6
Median perplexity is negatively associated with the languages’
release dates; younger languages are associated with lower median
perplexity.
Figure 7
:
Release dates of programming languages versus perplexity.
4.3
RQ3: How does code perplexity vary across LLMs on a multilingual code corpus?
We examined the correlation between our results and the results of the
two empirical studies of the related work
(Section
2
,
izadi2024language
,
xu2022polycoder
). Because our study’s setup differs from those used
in the other studies (
e
.
g
., different datasets and model sizes), we
could not directly compare absolute perplexity values across studies.
Instead, we focused on the
relative
language rankings produced
by each study,
i
.
e
., how models order programming languages by
perplexity rather than their raw scores. For this we ran statistical
tests between our LLaMA 3.2 language ranking and the language ranking
produced by each model assessed in the other studies, by computing the
Spearman
ρ
\rho
and the Kendall
τ
\tau
rank correlation coefficients,
which measure agreement between ordinal rankings without relying on
the absolute metric values.
Results are presented in Table
1
sorted in descending order by Spearman’s
ρ
\rho
.
Next to each coefficient we also provide the associated
p
p
-value.
We identified a strong negative correlation between our LLaMA 3.2 ranking and
the CodeGPT ranking of the evaluation by Izadi
et al.
[
izadi2024language
]
,
which is statistically significant according to the associated
p
p
-values
(
p
<
0.05
p<0.05
).
In addition,
we examined the correlation between the models of the other studies, and
identified some statistical dependence in
PolyCoder
[
xu2022polycoder
]
between the rankings produced by
GPT-Neo 2.7b
and
GPT-J 6b
, and
GPT-Neo 2.7b
and
GPT-NeoX 20b
.
This comes as no surprise considering that the models come from the same family.
Consequently,
it appears that code perplexity depends on the employed LLM.
Table 1
:
Correlation Between our LLaMA 3.2 Perplexity-based Language Ranking and
Rankings by Models in Other Studies
Spearman
Kendall
Study
Model
ρ
\rho
p
p
τ
\tau
p
p
izadi2024language
UniXcoder
[
guo2022unixcoder
]
0.24
0.24
0.57
0.57
0.21
0.21
0.55
0.55
xu2022polycoder
PolyCoder 2.7b
[
xu2022polycoder
]
0.20
0.20
0.60
0.60
0.11
0.11
0.76
0.76
izadi2024language
InCoder
[
fried2023incoder
]
0.17
0.17
0.69
0.69
0.07
0.07
0.90
0.90
xu2022polycoder
Codex
[
chen2021codex
]
0.05
0.05
0.90
0.90
−
0.05
-0.05
0.92
0.92
xu2022polycoder
GPT-NeoX 20b
[
black2022gptneox
]
−
0.07
-0.07
0.86
0.86
0.00
0.00
1.00
1.00
xu2022polycoder
CodeParrot
[
tunstall2022natural
]
−
0.27
-0.27
0.49
0.49
−
0.22
-0.22
0.48
0.48
xu2022polycoder
GPT-J 6b
[
wang2021gptj
]
−
0.33
-0.33
0.38
0.38
−
0.17
-0.17
0.61
0.61
xu2022polycoder
GPT-Neo 2.7b
[
black2021gptneo
]
−
0.43
-0.43
0.24
0.24
−
0.33
-0.33
0.26
0.26
izadi2024language
CodeGPT
[
lu2021codexglue
]
−
0.81
-0.81
0.01
0.01
−
0.64
-0.64
0.03
0.03
Furthermore, we repeated the perplexity experiment using a set of
general-purpose and code LLMs supported by
llama.cpp
,
i
.
e
., the
11 checkpoints named in Section
3.1
plus the same
LLaMA 3.2 3b weights as above:
CodeLlama 13b
[
roziere2024code
]
; CodeShell 7b
[
xie2024codeshelltechnicalreport
]
; Gemma 3 27b
[
gemmateam2025gemma3technicalreport
]
;
Gemma 4 31b
[
farabet2026gemma4
]
;
LLaMA 2 13b
[
touvron2023llama2
]
;
LLaMA 3 8b
[
dubey2024llama3herdmodels
]
;
LLaMA 3.1 8b
[
dubey2024llama3herdmodels
]
; Mistral 7b
[
jiang2023mistral7b
]
; Mixtral MoE 8x7b
[
jiang2024mixtralexperts
]
; Qwen 3.5 27b
[
qwen35blog
]
;
StarCoder 2 15b
[
lozhkov2024starcoder2stackv2
]
;
and
LLaMA 3.2 3b
[
meta2024llama3_2
]
. Again, the checkpoints
were retrieved from Hugging Face and converted to
GGUF F16
format.
Mixtral MoE 8x7b was additionally quantized to
Q4_K_M
format
with
llama.cpp
’s
llama-quantize
tool
to fit into the GPU memory of our laboratory machine.
Figure
8
presents a pairwise
Pearson correlation coefficient heatmap of the LLMs computed from
their median perplexities across the programming languages. The LLMs
are sorted by mean correlation in descending order (axis labels run
from highest to lowest average agreement with all other models).
Correlations are high throughout (median
≈
0.95
\approx 0.95
; most cells
>
0.90
>0.90
; the lowest, mostly Gemma 4 31b against LLaMA/Mistral, still
>
0.85
>0.85
). Related models appear as darker blocks (
e
.
g
., Mistral and
Mixtral with the LLaMA line and CodeLlama, and StarCoder 2 with
CodeShell or Qwen); Gemma 3 and Gemma 4 against LLaMA/Mistral is the
(comparatively) lightest region, but still very positive. In short,
most models rank languages similarly, but not identically: changing
the model changes the numbers and can swap close pairs.
Finding 7
Code perplexity depends on the chosen LLM: median perplexity
profiles correlate strongly across model variants, yet absolute
values and ordinal detail still shift between models, with related
models agreeing more closely than unrelated ones.
Furthermore, Figure
9
visualizes perplexity across LLMs and programming languages. Models
are sorted by their overall median perplexity across all languages in
ascending order. The figure demonstrates an agreement between models
in some clear-cut cases: Shell is universally high in perplexity,
whereas Java is low.
Finding 8
Shell is universally high in perplexity,
as opposed to Java which is universally low.
Figure 8
:
Pairwise correlation of LLMs based on their median perplexity.
Figure 9
:
Perplexity across LLMs and programming languages.
4.4
RQ4: How do different evaluation datasets affect an LLM’s measured code perplexity?
We tested whether language-level conclusions transfer when only
the
evaluation corpus
changes. We held the model and tooling
fixed, and re-ran the same strided sliding-window computation on the
multilingual benchmark files released for the
PolyCoder
study
[
xu2022dataset
]
. We used the same context length, stride,
and toolchain parameters as for the LLaMA 3.2 run underlying
Figure
3
(Section
3.5
), so
differences in medians and orderings are driven by the file set rather
than the perplexity configuration.
Our sample of
PolyCoder
files spans 12 languages; intersecting
them with the 14 languages in Figure
3
yields nine
shared languages: C, C#, C++, Go, Java, JavaScript, PHP, Python, and
Ruby. Figure
10
plots the perplexity
boxplots per language over the
PolyCoder
benchmark files
alongside the perplexity boxplots of our dataset for the same
languages (subset of Figure
3
).
To quantify how much the two corpora agree on the ordering of
languages by median perplexity (treating lower median as
easier
for the model in the next-token sense, higher as
harder
), we
correlated those median-based rankings for the nine shared languages.
Spearman’s
ρ
\rho
is approximately
0.73
0.73
(
p
≈
0.02
p\approx 0.02
) and
Kendall’s
τ
\tau
is approximately
0.56
0.56
(
p
≈
0.04
p\approx 0.04
). Thus,
median ordering is positively and significantly associated across
datasets under this setup, even though absolute perplexities
necessarily shift with different files, as is seen in
Figure
10
. We therefore treat
portability as a statement about
relative
ordering by
perplexity, not identical numeric scores.
Finding 9
Under a fixed model and perplexity pipeline, median perplexity
rankings on the PolyCoder benchmark correlate positively with
rankings on our dataset, so relative conclusions are broadly
portable despite different dataset perplexity scores.
Figure 10
:
(a) Perplexity across programming languages using the
PolyCoder
evaluation dataset. (b) Perplexity for the same
languages calculated on our dataset.
5
Discussion and Implications
Our study on code perplexity across programming languages, models, and
datasets has several implications for software engineering practice
and research. The confidence of LLM-based code assistance seems to
vary significantly by programming language. Strongly-typed languages
like Java, C#, and Go consistently show lower perplexity, indicating
that developers working with these languages may experience more
accurate and reliable code suggestions. This aligns with previous
research by Husein
et al.
[
husein2025llms
]
, who noted that
static type information provides clearer context for code prediction
models.
The perplexity variations across languages have direct implications
for development practices. Teams using languages with consistently
higher perplexity (Shell, C, R, Perl) might benefit from a more
cautious approach when adopting LLM-based tools, potentially
implementing stricter review processes for machine-generated code.
Conversely, projects using languages with lower perplexity could
benefit from streamlined workflows that leverage LLM suggestions more
extensively.
Perplexity’s value as a confidence indicator provides practical
applications for code review and quality assurance. As demonstrated by
Sharma
et al.
[
sharma2025assessing
]
, higher entropy
correlates with lower functional correctness in generated code.
Organizations could implement tiered review processes where
high-perplexity code blocks receive additional inspection, potentially
reducing error propagation in production systems. Such
confidence-based approaches could be particularly valuable for
critical codebases where reliability is paramount.
Our contribution is the open measurement pipeline and the empirical
basis for leveraging perplexity as a signal when using LLMs. Teams
could still use perplexity in an advisory way—
e
.
g
., computing it on
files changed in a pull request and flagging them for extra review
when scores exceed a team-defined threshold, or showing file- or
region-level scores in a code review interface as a non-blocking hint
next to linters and tests. Doing so would require local choices of
model, budget, and cut-offs, and would benefit from calibration to the
deployment context, as for any confidence proxy
(Section
6
).
Our finding that model choice shifts measured perplexity more strongly
than swapping the evaluation corpus (Section
4.4
) has
significant implications for LLM development. It suggests that
architectural improvements might yield greater benefits than
expanding training data
. The observed genealogical correlations
between model families (Mistral–Mixtral MoE; Meta LLaMA line;
CodeLlama–LLaMA 2; and StarCoder 2–CodeShell) indicate that
fundamental architectural decisions influence perplexity patterns
across model generations.
The observation that code comments generally increase perplexity
indicates that there are inherent differences in how humans and
machines express programming concepts, with human-authored comments
being more ambiguous and less predictable than code. This may hint at
the importance of precision in explaining code, and particularly
requirements, when programming by prompting is gaining momentum and
more and more code is being written by LLMs.
The relationship between language age and perplexity reveals an
interesting evolution in programming language design. More recent
languages with stronger typing systems and standardized syntax appear
more predictable by LLMs. Apparently, the same design principles that
enhance human readability and maintainability—clear structure,
consistent syntax, explicit typing—also improve machine
predictability. This insight could inform future language design
efforts, particularly for domain-specific languages.
The contrast between low perplexity in many strongly typed languages
and high perplexity in scripting languages in Section
4.2
,
leads to the hypothesis, consistent with Husein
et al.
[
husein2025llms
]
, that static types and fixed
interfaces contract the set of locally legal continuations, which
tends to lower next-token uncertainty for a model trained on large
code collections. The extent of possible continuations helps with the
“simple syntax” puzzle in scripting: surface compactness is not the
same as low continuation entropy, because idiom diversity, dynamic
features, and glue-style automation (including markup and command
shells present in our sample) can leave many semantically different
next lines plausible, even when the grammar is small; training-data
mix and repository style can reinforce that pattern. To establish
causality, however, would require controlled corpora, syntax
manipulations, or ablations, which we do not perform here, and which
we mark as future work.
From a theoretical perspective, our results contribute to the broader
discussion on code naturalness
[
allamanis2018naturalness
]
. The
moderate rank agreement between our corpus and the
PolyCoder
files (Section
4.4
) suggests that some predictability
differences between languages recur across corpora, while absolute
scores remain instance- and benchmark-dependent. This supports the
naturalness hypothesis while adding nuance: not all programming
languages are equally
natural
from a modeling perspective.
Overall, our research findings can enhance several aspects of software
development. Organizations can make more informed decisions about
which LLM-based tools might be most effective for their technology
stack. Teams can implement confidence-based review processes that
allocate resources according to the expected reliability of
LLM-generated code. In addition, perplexity can serve as a
quantitative factor when evaluating potential language migrations,
particularly for teams seeking to maximize the effectiveness of
AI-assisted development. Finally, developers of code completion tools
can use perplexity to evaluate which models might perform best for
specific languages.
6
Limitations
We present the risks resulting from our perplexity analysis
with respect to the internal and external validity of the study.
6.1
Internal Validity
The internal validity of the study is affected by particular steps
of our methods (Figure
1
).
The file filtering (Section
3.4
)
based on the language extensions by the
github-linguist/linguist
project
may have missed some relevant files whose extensions were not in the list.
Although we manually reviewed the extensions’ list,
we may not have been able to correct all possible errors
[
PVK15
]
.
Another risk stems from the fact that
the files of the sample are of various sizes,
resulting in diverse numbers of prediction steps
during the perplexity computation of each file.
Although we did not find any association between file or vocabulary size
(in terms of tokens) and perplexity in our data (Section
4.1
),
we cannot be certain whether an association generally exists.
The perplexity implementation we used is a close approximation of the
mathematical definition of perplexity. In theory, the complete history
is used in each prediction step. In practice, though, LLMs have a limited
context size, and the complete history may exceed that. As a
workaround, we used the strided method, and set a dynamic context size
so that all languages would be adequately represented
in the results (Section
3.5
).
Another limitation to consider is that we did not calibrate the
perplexity metric before using it as confidence indicator. Recent work
by Spiess
et al.
[
spiess2025calibration
]
discusses that
confidence metrics can benefit from calibration for decision-making
contexts. However, this limitation is mitigated by several factors.
First, our study focuses on comparative analyses between languages and
models rather than absolute confidence thresholds, and these relative
rankings are likely to remain valid even after calibration. Secondly,
our use of multiple LLMs for cross-validation provides additional
robustness to our findings beyond what calibration alone would offer.
Nevertheless, future work could explore calibration techniques such as
Platt scaling
[
platt1999probabilistic
]
to further refine the
relationship between perplexity scores and code correctness.
We also do not relate file-level perplexity to downstream outcomes
(
e
.
g
., build or test failure rates, or defect labels)
on LLM-generated code in a single controlled run.
That would need a task-specific generation, execution, and scoring
pipeline—outside the scope of our intrinsic, human-authored corpus design.
Section
1
reviews why intrinsic measures are discussed
as potential proxies in the code LLM literature, and
Section
5
considers heuristic uses of perplexity
in code review and quality workflows.
The present work does not add a direct empirical link from our file-level scores
to build, test, or defect outcomes;
closing that loop would require a dedicated generation-and-execution study,
which we treat as future work.
Finally, the inferential statistics we report have limitations common
to observational corpus studies. Rank-agreement tests (Spearman and
Kendall coefficients for comparing language orderings) operate at
small effective sample sizes—for example, only nine languages intersect our corpus and the
PolyCoder
benchmark—so
p
p
-values are coarse and sensitivity analyses would be
informative. Programming languages are not statistically independent
draws (they share semantics and syntax, ecosystems, tooling, and
corpora), so treating each language as one observation understates
dependence and can bias uncertainty downward. We also compare many
model pairs and study pairs without a formal multiple-testing
correction; the heatmap in
Figure
8
is an exploratory map
and not a family-wide error-controlled test of hypotheses.
6.2
External Validity
A limitation of the main analyses in Sections
4.1
and
4.2
is that we keep the checkpoint fixed
(Section
3.1
): all values use the LLaMA 3.2 3b
tokenizer and weights. In Section
4.4
we use the same
configuration and re-run the strided sliding-window procedure on the
PolyCoder
benchmark. Rank-agreement tests on the nine shared
languages compare language orderings across corpora,
i
.
e
., they reflect
corpus
shift rather than a change of LLM. The perplexity
figures reported in RQ1 and RQ2, and the
PolyCoder
medians in
RQ4 are therefore tied to that model and to those file samples. We
would not expect the same numbers to follow under another
architecture, or for an unrelated repository snapshot, without
re-computation.
We mitigate this risk in part through the tests in RQ3 and the
PolyCoder
extension in RQ4
(Sections
4.3
,
4.4
). In RQ3, we re-score the same
multilingual GPL fileset on 12 LLMs: the median language-level
profiles are strongly aligned
(Figures
8
,
9
;
see the Finding in Section
4.3
). The broad
relative
contrasts in language-level ordering (
i
.
e
., which languages exhibit
lower versus higher median perplexity) therefore recur across
architectures, but absolute perplexities and some adjacent ranks in
the ordering still move with the checkpoint
(cf. Section
4.3
). In addition, the rank-agreement tests in
Section
4.4
show
moderate
agreement of median
orderings for the nine shared languages, so
relative
statements
about language ordering agree only in part when we compare the two
file sets, and the per-benchmark medians need not coincide
(Section
4.4
Finding). Taken together,
the RQ3 and RQ4
results suggest that language-level ordering may partially
generalize when either the model or the evaluation dataset
changes, whereas reported numeric perplexities remain tied to
a particular model, corpus, and tooling configuration, and need to
be recomputed before making outside comparisons.
Generalizability concerns arise from the sample selection process employed
in project (Section
3.3
) and
file selection (Sections
3.4
).
We strived for a file sample
distributed evenly across programming languages and projects,
that at the same time would represent as many projects as possible.
Yet, the stability of the perplexity results could be strengthened
through cross-validation with multiple different samples.
Also, the projects of the initial population are all distributed with
GPL licenses to avoid training-test leakage with LLaMA 3.2 (see
Section
3.2
), hence perplexity results may not
generalize to non-GPL-licensed projects. In addition, the correlation
output between perplexity and total/vocabulary size in
Section
4.1
may be affected by our restricted sample size,
and should be repeated on larger samples to draw stable conclusions.
Our perplexity observations with respect to the language
characteristics in Section
4.1
could be affected by the
representation of the languages in the training data. For instance,
mainstream languages could have more training data available impacting
model performance. Although our analysis of the effect of the language
distribution in the LLaMA training data on code perplexity did not
reveal any relationship between the two variables, we cannot be
certain that such a relationship does not generally exist.
7
Conclusion
We investigated code perplexity through various LLMs on a multilingual
code corpus. Perplexity
[
jelinek:1977
,
huyen2019evaluation
]
is a
simple, efficient, versatile, and straightforward intrinsic metric
that can be applied universally across LLMs and
tasks
[
huyen2019evaluation
,
xu2022polycoder
]
. Lower perplexity
has been found to decrease error rate
[
bahl1983likelihood
]
and
improve end-task performance
[
liu2019roberta
,
xu2022polycoder
,
nijkamp2023codegen
]
, offering an effective and efficient proxy for
downstream metrics. Still, limited research has investigated LLM
performance from this perspective.
To fill this gap we conducted an empirical analysis of a sample of
2254 files coming from 881 GPL-licensed projects from GitHub, spanning
14 programming languages. Through our analysis we evaluated code
perplexity variation across languages, models, and datasets, and
compared our results with two other empirical
works
[
izadi2024language
,
xu2022polycoder
]
. We found that
strongly-typed languages show lower code perplexity than dynamically
typed languages. Scripting languages demonstrate higher perplexity,
with Shell appearing universally high as opposed to Java which appears
universally low in perplexity. Although code comments often increase
perplexity, the language ranking based on perplexity is barely
affected. We did not identify any correlation between vocabulary or
file size (in tokens) and code perplexity. Lastly, average code
perplexity depends on the employed LLM, whereas median language
rankings are moderately stable when re-evaluating the same model on
the
PolyCoder
benchmark files.
Our findings allow LLM researchers, developers, and users to know how
beneficial the use of an LLM assistant can be in a software project
depending on its language as well as what LLM to choose. Also, they
can understand how a model’s confidence is affected by different
project, language, and code characteristics such as language verbosity
and type system, vocabulary size, and code comments.
Future research could investigate further the impact of vocabulary and
file size on perplexity. Some supplementary questions worth
researching concern how project, developer, and additional language
characteristics may affect code perplexity, and how code perplexity
correlates with LLMs’ downstream performance metrics.
References