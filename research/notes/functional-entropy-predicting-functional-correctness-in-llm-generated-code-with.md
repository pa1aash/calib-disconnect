---
title: 'Functional Entropy: Predicting Functional Correctness in LLM-Generated Code
  with Uncertainty Quantification'
id: functional-entropy-predicting-functional-correctness-in-llm-generated-code-with
tags:
- code-llm-calibration-aaai27-eabf3f
- functional-entropy
- semantic-entropy
- sampling-uq
- locus-code-verbal-calibration-occupied-or-open
- aaai-bar-eval-dprc-d78e07
created: '2026-07-17T18:30:44.016388Z'
updated: '2026-07-19T20:13:26.316080Z'
source: https://arxiv.org/html/2605.28500
source_domain: arxiv.org
fetched_at: '2026-07-17T18:30:44.015551Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'CVS Health team (Bouchard, Chauhan, Ahmad, Ra) systematically evaluates
  UQ methods for code correctness prediction across 3 languages (Python/LiveCodeBench,
  Java/MultiPL-E, SQL/LiveSQLBench), 5 closed-API LLMs (GPT-4o, GPT-4o-mini, Gemini-2.5-Pro/Flash/Flash-Lite),
  and 1,711 problems. Central diagnosis: NLI-based semantic entropy/sets (the standard
  sampling-based UQ signal, using deberta-large-mnli) collapses to near-chance AUROC
  (0.47-0.58 SQL, 0.48-0.56 Java, 0.50-0.53 Python) because NLI models cannot distinguish
  functionally different code and assign nearly all samples to one cluster -- the
  equivalence-assessment step is the bottleneck, not the sampling-consistency principle
  itself. Fix: replace NLI equivalence with an LLM-judge functional-equivalence check
  (does code produce the same outputs for all valid inputs), yielding three new scorers
  (Functional Equivalence Rate, Functional Entropy, Functional Sets Confidence) that
  hit top AUROC in 11/15 model-benchmark combos (up to 0.87 Python, 0.84 SQL) and
  best calibration in most settings with NO explicit calibration step. Verbalized
  confidence is inconsistent (AUROC 0.52-0.80); reflexive P(True) is occasionally
  strong (0.82-0.84) but erratic. Requires m=5-10 extra samples plus per-pair LLM-judge
  calls (93-97% precision vs execution ground truth); m=5 recovers most of the AUROC
  gain. Explicitly does NOT test open-weight models (Qwen, Llama, Mistral, DeepSeek
  excluded as a stated limitation) -- direct gap for a Qwen2.5-Coder/DeepSeek-Coder
  study. Relation to disconnect thesis: this paper improves the INTERNAL signal itself
  (better equivalence clustering) rather than solving the expressed-interface problem
  -- it still requires costly resampling + external LLM-judge calls, not a lightweight
  single-generation confidence a user could read off the model. Positions functional/AST-style
  equivalence clustering as an upper bound on what pure-embedding or NLI-based semantic-entropy
  proxies can achieve, useful as an oracle baseline against which a cheaper expressed-confidence
  method should be judged.'
---

Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2605.28500v1 [cs.CL] 27 May 2026
Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification
Dylan Bouchard
†
Mohit Singh Chauhan
†
Zeya Ahmad   Ho-Kyeong Ra
CVS Health
®
, Wellesley, MA, USA
Correspondence:
mohitsingh.chauhan@cvshealth.com
.
†
Co-first authors.
Abstract
Large language models have shown impressive capabilities in code generation, yet they often produce functionally incorrect code. Uncertainty quantification (UQ) methods have emerged as a promising approach for detecting hallucinations in natural language generation, but their effectiveness for code generation tasks remains underexplored. We systematically evaluate how UQ techniques transfer to code generation across three programming languages, five LLMs, and over 1,700 problems. We find that some token-probability-based methods generalize effectively without modification, while sampling-based methods relying on natural language inference (NLI) fail because NLI models cannot distinguish functionally different code, causing most responses to collapse into a single semantic cluster. To address this, we introduce
functional equivalence methods
, a family of code-specific methods that replace NLI-based semantic equivalence with an LLM-based functional equivalence assessment, including functional entropy, a code-specific analog of semantic entropy. Functional equivalence methods achieve top AUROC in 11 out of 15 model-benchmark combinations and the best calibration across most settings, consistently outperforming both NLI-based counterparts and all other methods evaluated.
Functional Entropy: Predicting Functional Correctness in LLM-Generated Code with Uncertainty Quantification
Dylan Bouchard
†
Mohit Singh Chauhan
†
†
†
thanks:
Correspondence:
mohitsingh.chauhan@cvshealth.com
.
†
Co-first authors.
Zeya Ahmad    Ho-Kyeong Ra
CVS Health
®
, Wellesley, MA, USA
1
Introduction
Large language models (LLMs) have demonstrated remarkable capabilities in code generation, powering tools that assist developers in writing, completing, and debugging code. However, these models can produce plausible-looking but functionally incorrect code, a failure mode that poses significant risks in software development contexts where correctness is paramount. Studies on established benchmarks such as LiveCodeBench
(Jain
et al.
,
2024
)
and LiveSQLBench
(Team,
2024
)
show that even state-of-the-art models produce incorrect solutions for a substantial fraction of problems
(Gao
et al.
,
2025
; Tian
et al.
,
2025
)
. Incorrect code can fail silently, introduce security vulnerabilities, or cause downstream system failures. These risks are amplified in settings where generated code is executed with limited or no human review, such as autonomous coding agents, text-to-SQL systems that run queries directly against databases, or agentic workflows where code is generated and executed as an intermediate tool-use step. Reliably predicting when generated code is likely wrong is therefore a pressing practical challenge.
In natural language generation (NLG), uncertainty quantification (UQ) has emerged as a promising approach for detecting unreliable outputs. Methods such as predictive entropy, self-consistency, and semantic entropy leverage token probabilities or sample agreement to estimate model confidence, with low confidence serving as a signal for potential hallucination. Recent work has shown that these techniques can effectively identify unreliable generations in question-answering, summarization, and other NLG tasks
Farquhar
et al.
(
2024
); Vashurin
et al.
(
2025a
)
. Yet it remains unclear how well these methods transfer to code generation, where outputs have distinct structural properties and where functional correctness, as determined by test execution, provides a relatively unambiguous ground truth. While recent studies have begun exploring UQ for code generation, existing evaluations remain limited in scope, leaving practitioners without comprehensive guidance on which techniques to adopt across different languages and models or how to adapt them.
Several factors complicate this transfer. First, code exhibits
functional equivalence
, meaning syntactically different programs can be semantically identical, and hence surface-level disagreement among samples does not necessarily indicate uncertainty. Second, UQ methods designed for natural language often rely on NLG-specific components, such as natural language inference (NLI) models to assess semantic equivalence or text embeddings to measure similarity. When applied to code without adaptation, these components become a bottleneck, degrading the performance of otherwise effective UQ frameworks. Third, although execution-based evaluation provides the most reliable measure of code correctness, gold test cases are not always available, and automatically generated tests may not cover the relevant failure modes. This raises the question of whether execution-free UQ methods can approximate the signal that test suites provide, and under what conditions they fall short.
These complications motivate not only a systematic evaluation of existing UQ techniques in the code domain, but also the development of code-specific adaptations where general-purpose methods prove insufficient. In this paper, we investigate how existing uncertainty quantification techniques generalize to code generation across three programming languages (Python, Java, and SQL). We evaluate a comprehensive suite of methods spanning token-probability-based approaches, sampling-based consistency methods, and reflexive techniques across five LLMs and established code generation benchmarks. We find that some single-generation token-probability-based methods transfer effectively to code with no modification, though their effectiveness varies substantially across datasets and methods. For sampling-based methods, we show that NLI-based semantic equivalence is the critical bottleneck because NLI models cannot reliably distinguish functionally different code, causing most responses to collapse into a single cluster and rendering clustering-based UQ methods uninformative. To address this, we introduce
functional equivalence methods
, a family of code-specific methods that replace NLI-based semantic equivalence with LLM-based functional equivalence assessment, including functional entropy, a code-specific analog of semantic entropy. Functional equivalence methods consistently achieve the strongest performance across models and languages, demonstrating that the bottleneck in transferring sampling-based UQ methods to code lies specifically in the equivalence assessment mechanism.
Our contributions are as follows. First, we provide a comprehensive evaluation of uncertainty quantification methods for code correctness prediction across five LLMs, three programming languages, and over 1,700 problems, establishing baseline performance and revealing that method effectiveness varies substantially across languages, offering actionable guidance for practitioners. Second, we introduce functional equivalence methods, a family of methods comprising functional equivalence rate, functional entropy, and functional sets confidence, that replace NLI-based semantic equivalence with LLM-evaluated functional equivalence for clustering code responses. These methods achieve top AUROC in 11 out of 15 model-benchmark combinations and the best calibration across most settings, consistently outperforming both their NLI-based counterparts and all other methods evaluated. Third, we release all methods, including functional entropy and additional code-adapted scorers using code embeddings and CodeBLEU-based consistency
(Sharma and David,
2025
)
, as
part of UQLM,
an open-source library for uncertainty quantification in both natural language and code generation.
1
1
1
https://github.com/cvs-health/uqlm
; See
Bouchard
et al.
(
2026
)
for software details.
2
Related Work
Uncertainty Quantification for Natural Language Generation.
Uncertainty quantification has demonstrated strong performance in detecting hallucinations in natural language generation
(Huang
et al.
,
2023
; Shorinwa
et al.
,
2024
)
. Existing methods can be broadly categorized by their access requirements and computational approach. Various white-box methods leverage token probabilities from a single generation, using signals such as sequence probability
(Malinin and Gales,
2021
)
, minimum token probability
(Manakul
et al.
,
2023
)
, probability margin
(Farr
et al.
,
2024
)
, and token-level entropy
(Scalena
et al.
,
2025
)
. Sampling-based methods generate multiple responses from the same prompt and measure consistency, either through black-box approaches using exact match
(Cole
et al.
,
2023
)
, embedding similarity
(Manakul
et al.
,
2023
; Bouchard and Chauhan,
2025
)
, or NLI-based semantic equivalence
(Chen and Mueller,
2023
; Kuhn
et al.
,
2023
; Farquhar
et al.
,
2024
)
, or through white-box approaches that additionally incorporate token probabilities
(Vashurin
et al.
,
2025a
,
b
; Qiu and Miikkulainen,
2024
)
. Reflexive methods prompt models to self-evaluate their outputs, either by eliciting explicit confidence scores
(Tian
et al.
,
2023
)
or by probing agreement with the original response
(Kadavath
et al.
,
2022
)
. While these methods have been extensively studied for question answering and summarization, their effectiveness for code generation remains underexplored.
Hallucination Detection in Code Generation.
Recent work has begun characterizing hallucinations in code generation, proposing taxonomies and benchmarks for evaluation
(Gao
et al.
,
2025
; Tian
et al.
,
2025
; Liu
et al.
,
2026
; Jiang
et al.
,
2024
)
. From an uncertainty perspective,
Huang
et al.
(
2025
)
conducted an exploratory study of uncertainty estimation for LLMs across both NLP tasks and code generation, finding that uncertainty metrics can help identify buggy programs, while
Spiess
et al.
(
2024
)
find token-probability-based confidence scores for generated code are better-calibrated than those based on verbalized confidence.
Sharma and David (
2025
)
proposed symbolic clustering for uncertainty estimation in code, arguing that existing confidence measures fail to capture semantic equivalence. Several approaches have been proposed to mitigate code hallucinations, including entropy-aware adaptive decoding
(Scalena
et al.
,
2025
)
, attention-based uncertainty quantification
(Vazhentsev
et al.
,
2025
)
, and highlighting likely-incorrect tokens
(Vasconcelos
et al.
,
2025
)
. In adjacent domains,
Yang
et al.
(
2025
)
proposed metamorphic testing for hallucination detection in text-to-SQL generation,
Tantithamthavorn
et al.
(
2026
)
developed a reference-free hallucination detector for code review automation, and
Healy
et al.
(
2026
)
explored internal-representation-based UQ for agent tool selection. From a decoding perspective,
He
et al.
(
2025
)
proposed uncertainty-aware adaptive decoding, and
Zhu
et al.
(
2025
)
presented UnCerT-CoT for dynamic chain-of-thought reasoning. Our work differs by systematically evaluating a comprehensive suite of UQ methods across multiple programming languages and models, diagnosing the specific failure of NLI-based equivalence for code, and introducing functional entropy methods that recover strong performance through LLM-based functional equivalence assessment.
3
Methods
We consider the problem of predicting functional correctness in code generation (i.e., whether generated code satisfies the intended specification), often termed hallucination detection in the broader literature. Given a prompt
x
x
(e.g., a natural language description or docstring) and a generated code response
y
y
, our goal is to produce a confidence score
s
​
(
y
)
∈
[
0
,
1
]
s(y)\in[0,1]
that effectively distinguishes functionally correct code from incorrect code, enabling reliable ranking and classification without requiring execution or access to test cases at inference time. Our primary evaluation criterion is AUROC, measuring how well the score ranks correct generations above incorrect ones.
We evaluate three families of uncertainty quantification methods: (1) token-probability-based methods that operate on a single generation, (2) sampling-based consistency methods that compare multiple generations from the same prompt, and (3) reflexive methods that prompt the model to self-evaluate its outputs. For sampling-based methods, we develop code-specific extensions that replace natural language components with analogs designed for code.
3.1
Token-Probability-Based Methods
These methods derive confidence scores directly from the token-level probabilities produced by the language model during generation. Let the tokenization of response
y
y
be denoted
{
t
1
,
…
,
t
L
}
\{t_{1},\ldots,t_{L}\}
, where
L
L
is the number of tokens, and let
p
j
p_{j}
denote the probability assigned to token
t
j
t_{j}
by the model.
Length-Normalized Sequence Probability (LNSP).
Sequence probability
(Vashurin
et al.
,
2025a
)
is the joint probability of all tokens in the response:
SP
​
(
y
;
x
)
=
∏
j
=
1
L
p
j
.
\text{SP}(y;x)=\prod_{j=1}^{L}p_{j}.
To account for the tendency of longer sequences to have lower joint probabilities, we focus on length-normalized sequence probability
(Malinin and Gales,
2021
)
, which computes the geometric mean of token probabilities:
LNSP
​
(
y
;
x
)
=
(
∏
j
=
1
L
p
j
)
1
/
L
\text{LNSP}(y;x)=\left(\prod_{j=1}^{L}p_{j}\right)^{1/L}
Minimum Token Probability (MTP).
This method uses the minimum token probability as a confidence score
(Manakul
et al.
,
2023
)
, capturing the intuition that a single low-confidence token may indicate an unreliable generation:
MTP
​
(
y
;
x
)
=
min
j
∈
{
1
,
…
,
L
}
⁡
p
j
\text{MTP}(y;x)=\min_{j\in\{1,\ldots,L\}}p_{j}
Other methods require access to the top-
K
K
token probabilities for each token position. Let
{
p
j
,
1
,
…
,
p
j
,
K
}
\{p_{j,1},\ldots,p_{j,K}\}
denote the top-
K
K
token probabilities at position
j
j
, ordered by decreasing probability.
Probability Margin (PM).
Probability margin
(Farr
et al.
,
2024
)
measures the average gap between the most likely and second most likely token at each position:
PM
​
(
y
;
x
)
=
1
L
​
∑
j
=
1
L
(
p
j
,
1
−
p
j
,
2
)
\text{PM}(y;x)=\frac{1}{L}\sum_{j=1}^{L}(p_{j,1}-p_{j,2})
Average Token Negentropy at
K
K
(ATN@
K
K
).
This method computes the entropy over the top-
K
K
tokens at each position and normalizes it to a confidence score
(Scalena
et al.
,
2025
; Manakul
et al.
,
2023
)
. The top-
K
K
token entropy at position
j
j
is:
TE@
​
K
​
(
t
j
)
=
−
∑
k
=
1
K
p
j
,
k
(
K
)
​
log
⁡
p
j
,
k
(
K
)
\text{TE@}K(t_{j})=-\sum_{k=1}^{K}p_{j,k}^{(K)}\log p_{j,k}^{(K)}
where
p
j
,
k
(
K
)
=
p
j
,
k
/
∑
i
=
1
K
p
j
,
i
,
p_{j,k}^{(K)}=p_{j,k}/\sum_{i=1}^{K}p_{j,i},
k
=
1
,
…
,
K
k=1,...,K
are the renormalized top-K probabilities. The token negentropy transformation normalizes this to
[
0
,
1
]
[0,1]
with higher values indicating higher confidence:
TN@
​
K
​
(
t
j
)
=
1
−
TE@
​
K
​
(
t
j
)
log
⁡
K
\text{TN@}K(t_{j})=1-\frac{\text{TE@}K(t_{j})}{\log K}
Average token negentropy at
K
K
is then the mean top-
K
K
token negentropy across all positions:
ATN@
​
K
​
(
y
;
x
)
=
1
L
​
∑
j
=
1
L
TN@
​
K
​
(
t
j
)
\text{ATN@}K(y;x)=\frac{1}{L}\sum_{j=1}^{L}\text{TN@}K(t_{j})
Minimum Token Negentropy at
K
K
(MTN@
K
K
).
Analogous to minimum token probability, this method uses the minimum token negentropy as the confidence score
(Scalena
et al.
,
2025
; Manakul
et al.
,
2023
)
:
MTN@
​
K
​
(
y
;
x
)
=
min
j
∈
{
1
,
…
,
L
}
⁡
TN@
​
K
​
(
t
j
)
\text{MTN@}K(y;x)=\min_{j\in\{1,\ldots,L\}}\text{TN@}K(t_{j})
3.2
Sampling-Based Consistency Methods
These methods generate
m
m
additional responses
𝐲
~
=
{
y
~
1
,
…
,
y
~
m
}
\tilde{\mathbf{y}}=\{\tilde{y}_{1},\ldots,\tilde{y}_{m}\}
from the same prompt
x
x
using a non-zero sampling temperature (specified in Section
4
), then measure consistency between the original response
y
y
and the sampled responses. The intuition is that when a model is confident, independently sampled responses should agree; disagreement signals uncertainty.
3.2.1
Functional Equivalence Methods
We introduce a family of three methods built on a shared foundation: LLM-based functional equivalence assessment. In natural language UQ, sampling-based methods typically use NLI models to assess semantic equivalence between responses, classifying each pair as entailment, contradiction, or neutral
(Kuhn
et al.
,
2023
)
. For code, we replace this with a direct LLM-based assessment of whether two code snippets are functionally equivalent, i.e., whether they would produce the same outputs for all valid inputs (see Appendix
G
for the prompt template). Each method extracts a different summary statistic from the resulting equivalence structure.
Functional Equivalence Rate (FER).
This method estimates the proportion of sampled responses that are functionally equivalent to the original response:
FER
​
(
y
;
𝐲
~
,
x
)
=
1
m
​
∑
j
=
1
m
𝕀
​
[
y
≡
y
~
j
]
\text{FER}(y;\tilde{\mathbf{y}},x)=\frac{1}{m}\sum_{j=1}^{m}\mathbb{I}[y\equiv\tilde{y}_{j}]
where
𝕀
​
[
y
≡
y
~
j
]
∈
{
0
,
1
}
\mathbb{I}[y\equiv\tilde{y}_{j}]\in\{0,1\}
denotes the LLM-based functional equivalence indicator.
Functional Entropy (FE).
Functional entropy clusters responses based on functional equivalence, then computes entropy over the cluster distribution.
2
2
2
Clusters are formed through a greedy procedure, where the original response initializes the first cluster, and each remaining response is compared against existing cluster representatives. Responses judged equivalent to a representative join that cluster; the first response not equivalent to any existing representative initializes a new cluster and becomes its representative. This process continues until all responses are assigned, requiring fewer comparisons than exhaustive pairwise evaluation.
This is a code-specific analogue of semantic entropy
(Kuhn
et al.
,
2023
)
, replacing NLI-based mutual entailment with LLM-based functional equivalence assessment. Let
𝒞
\mathcal{C}
denote the set of clusters obtained from
(
y
,
y
~
1
,
…
,
y
~
m
)
(y,\tilde{y}_{1},\ldots,\tilde{y}_{m})
, and let
P
​
(
C
)
P(C)
denote the proportion of responses in cluster
C
C
. Functional entropy is:
FE
​
(
y
;
𝐲
~
,
x
)
=
−
∑
C
∈
𝒞
P
​
(
C
)
​
log
⁡
P
​
(
C
)
\text{FE}(y;\tilde{\mathbf{y}},x)=-\sum_{C\in\mathcal{C}}P(C)\log P(C)
Following
Bouchard and Chauhan (
2025
)
, we normalize to obtain a confidence score in
[
0
,
1
]
[0,1]
:
NFN
​
(
y
;
𝐲
~
,
x
)
=
1
−
FE
​
(
y
;
𝐲
~
,
x
)
log
⁡
(
m
+
1
)
\text{NFN}(y;\tilde{\mathbf{y}},x)=1-\frac{\text{FE}(y;\tilde{\mathbf{y}},x)}{\log(m+1)}
Functional Sets Confidence (FSC).
This method counts the number of unique functional clusters
|
𝒞
|
|\mathcal{C}|
(Lin
et al.
,
2024
)
. Following
Bouchard
et al.
(
2026
)
, we normalize to
[
0
,
1
]
[0,1]
:
FSC
​
(
y
;
𝐲
~
,
x
)
=
m
+
1
−
|
𝒞
|
m
\text{FSC}(y;\tilde{\mathbf{y}},x)=\frac{m+1-|\mathcal{C}|}{m}
When all
m
+
1
m+1
responses (the original plus
m
m
samples) cluster together (
|
𝒞
|
=
1
|\mathcal{C}|=1
), confidence is 1; when all responses are distinct (
|
𝒞
|
=
m
+
1
|\mathcal{C}|=m+1
), confidence is 0.
3.2.2
Similarity-Based Methods
Normalized Cosine Similarity (NCS).
This method embeds responses using a code embedding model
V
:
𝒴
→
ℝ
d
V:\mathcal{Y}\rightarrow\mathbb{R}^{d}
and measures average cosine similarity across sampled responses, normalized to
[
0
,
1
]
[0,1]
(Bouchard and Chauhan,
2025
)
:
NCS
​
(
y
;
𝐲
~
,
x
)
=
1
2
+
1
2
​
m
​
∑
j
=
1
m
V
​
(
y
)
⋅
V
​
(
y
~
j
)
‖
V
​
(
y
)
‖
⋅
‖
V
​
(
y
~
j
)
‖
.
\text{NCS}(y;\tilde{\mathbf{y}},x)=\frac{1}{2}+\frac{1}{2m}\sum_{j=1}^{m}\frac{V(y)\cdot V(\tilde{y}_{j})}{\|V(y)\|\cdot\|V(\tilde{y}_{j})\|}.
CodeBLEU Consistency (CBC).
Following
Sharma and David (
2025
)
, we implement a consistency scorer based on CodeBLEU
(Ren
et al.
,
2020
)
, a metric for code generation that incorporates n-gram match, weighted n-gram match, syntax match via abstract syntax trees, and semantic match via data-flow analysis. Unlike the equivalence-based methods above, which assess functional agreement, CBC captures structural and syntactic similarity between generations:
CBC
​
(
y
;
𝐲
~
,
x
)
=
1
m
​
∑
j
=
1
m
CodeBLEU
​
(
y
,
y
~
j
)
\text{CBC}(y;\tilde{\mathbf{y}},x)=\frac{1}{m}\sum_{j=1}^{m}\text{CodeBLEU}(y,\tilde{y}_{j})
3.3
Reflexive Methods
Reflexive methods prompt the model to evaluate the correctness of its own outputs.
P(True).
This method asks the model to classify its response as correct or incorrect, using the token probability assigned to “True” as the confidence score:
P(True)
​
(
y
;
x
)
=
p
​
(
“True”
∣
x
,
y
)
\text{P(True)}(y;x)=p(\text{``True''}\mid x,y)
(Kadavath
et al.
,
2022
)
.
Verbalized Confidence (VC).
VC prompts the model to express confidence on a six-level Likert scale from “No chance” (0%) to “Almost certain” (100%), mapped to
[
0
,
1
]
[0,1]
without requiring access to token-level probabilities
(Tian
et al.
,
2023
)
.
4
Experiments
We evaluate the full suite of uncertainty quantification methods on code generation tasks spanning three programming languages, five large language models, and 1,711 problems.
Benchmark
Gem-Pro
Gem-Fl
Gem-Fl-Lt
GPT4o
GPT4o-m
LCB (Python)
0.91
0.87
0.67
0.56
0.51
Mult.-E (Java)
0.53
0.51
0.48
0.57
0.56
LSQLB (SQL)
0.45
0.45
0.24
0.29
0.21
Table 1:
Model accuracy (Pass@1) across benchmarks.
4.1
Experimental Setup
We evaluate on three code generation benchmarks covering Python, Java, and SQL.
LiveCodeBench
(Jain
et al.
,
2024
)
contains 1,055 Python problems sourced from LeetCode, AtCoder, and Codeforces programming platforms. Problems span a range of difficulty levels and require generating complete function implementations from natural language descriptions and function signatures.
MultiPL-E (Java)
(Cassano
et al.
,
2022
)
provides 386 Java problems translated from the Mostly Basic Python Problems benchmark, covering common programming tasks such as string manipulation, list processing, and mathematical computations.
LiveSQLBench
(Team,
2024
)
contains 270 SQLite problems requiring database query generation from natural language questions and schema descriptions; problems range from simple single-table queries to complex multi-table joins and aggregations.
We generate code using five large language models spanning different capability levels and providers: GPT-4o, GPT-4o-mini
(OpenAI,
2025
)
, Gemini-2.5-Pro, Gemini-2.5-Flash, and Gemini-2.5-Flash-Lite
(
Google,
)
. For each model-benchmark pair, we generate an original response using greedy decoding and
m
=
10
m=10
sampled responses with temperature
T
=
1.0
T=1.0
for sampling-based methods. We ablate over
m
∈
{
1
,
…
,
10
}
m\in\{1,\ldots,10\}
in Appendix
F
. For Python and Java benchmarks, a generated solution is considered correct if it passes all unit tests for the given problem. For SQL problems, correctness is determined by comparing the output of the generated query against that of the reference solution.
We evaluate each scorer on classification performance and calibration. For classification, we report Area Under the Receiver Operating Characteristic curve (AUROC), treating correctness prediction as a binary classification task. For calibration, we report Brier Score and Expected Calibration Error (ECE), which measure how well confidence scores align with empirical accuracy. Calibration results are reported in Appendix
A
. We use Gemini-2.5-Flash for the functional equivalence assessments, validated against execution-based outcomes with 93–97% precision across evaluated settings (Appendix
D
), and
jina-embeddings-v2-base-code
for code embeddings.
Across all experiments, functional equivalence methods achieve top AUROC in 11 out of 15 model-benchmark combinations. These methods also achieve the best calibration in Python and SQL while remaining competitive on Java, meaning their confidence scores often serve as reliable probability estimates in addition to providing strong ranking performance. We now present results for each benchmark; cross-benchmark patterns and implications are discussed in Section
5
.
4.2
Python (LiveCodeBench)
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
red!35!white0.691
\cellcolor
red!45!white0.580
\cellcolor
red!15!white0.761
\cellcolor
red!15!white0.757
\cellcolor
red!25!white0.729
Min. Prob.
\cellcolor
blue!5!white0.773
\cellcolor
red!15!white0.762
\cellcolor
blue!5!white0.783
\cellcolor
red!25!white0.738
\cellcolor
red!35!white0.705
Prob. Margin
\cellcolor
red!45!white0.668
\cellcolor
red!45!white0.554
\cellcolor
red!5!white0.762
\cellcolor
red!25!white0.752
\cellcolor
red!25!white0.749
Avg. Tok. Neg.
\cellcolor
red!35!white0.695
\cellcolor
red!45!white0.582
\cellcolor
blue!5!white0.774
\cellcolor
blue!5!white0.776
\cellcolor
red!15!white0.760
Min. Tok. Neg.
\cellcolor
red!5!white0.766
\cellcolor
red!5!white0.770
\cellcolor
blue!15!white0.797
\cellcolor
blue!5!white0.779
\cellcolor
red!5!white0.768
Functional Equivalence Methods
Func. Equiv.
\cellcolor
blue!45!white
0.867
\cellcolor
blue!25!white0.826
\cellcolor
blue!45!white
0.859
\cellcolor
blue!45!white0.859
\cellcolor
blue!35!white
0.856
Func. Entropy
\cellcolor
blue!45!white0.857
\cellcolor
blue!35!white
0.829
\cellcolor
blue!45!white0.857
\cellcolor
blue!45!white
0.859
\cellcolor
blue!35!white0.855
Func. Sets
\cellcolor
blue!35!white0.855
\cellcolor
blue!25!white0.826
\cellcolor
blue!35!white0.852
\cellcolor
blue!45!white0.856
\cellcolor
blue!35!white0.855
Similarity-Based Methods
Cos. Sim.
\cellcolor
red!15!white0.753
\cellcolor
blue!15!white0.804
\cellcolor
red!15!white0.756
\cellcolor
red!25!white0.738
\cellcolor
red!35!white0.724
CodeBLEU
\cellcolor
blue!15!white0.795
\cellcolor
blue!25!white0.813
\cellcolor
blue!15!white0.795
\cellcolor
red!5!white0.766
\cellcolor
red!25!white0.744
Reflexive Methods
Verb. Conf.
\cellcolor
blue!15!white0.795
\cellcolor
red!35!white0.716
\cellcolor
red!45!white0.597
\cellcolor
red!35!white0.725
\cellcolor
red!45!white0.681
P(True)
\cellcolor
red!5!white0.771
\cellcolor
blue!25!white0.815
\cellcolor
blue!35!white0.830
\cellcolor
red!15!white0.752
\cellcolor
blue!25!white0.824
Table 2:
Code correctness AUROC on LiveCodeBench (Python). Higher is better; red = low, blue = high.
Table
2
presents AUROC results for predicting functional correctness on LiveCodeBench. Model accuracy (pass@1) ranges from 0.51 (GPT-4o-mini) to 0.91 (Gemini-2.5-Pro). Overall AUROC scores are the highest across our three benchmarks, with most methods exceeding 0.70 and the best performers reaching 0.87, suggesting that the richness and diversity of Python solutions provides strong signal for uncertainty estimation.
Sampling-based methods using LLM-based functional equivalence achieve the strongest performance across all models. Functional equivalence rate achieves the highest overall score of 0.87 on Gemini-2.5-Flash, with functional entropy and functional sets confidence performing comparably (0.83–0.86 across models). These methods show remarkable consistency, maintaining strong performance regardless of underlying model capability. CodeBLEU consistency also performs well, achieving 0.81 on Gemini-2.5-Pro and 0.80 on Gemini-2.5-Flash, confirming that syntax-aware similarity captures meaningful variation in Python code.
Most token-probability methods show solid performance on Python. Minimum token negentropy achieves 0.77–0.80 across models, while minimum probability reaches 0.78 on Gemini-2.5-Flash-Lite. Sequence probability and probability margin are notably weaker on Gemini-2.5-Pro (0.580 and 0.554), indicating that aggregated token-level confidence does not reliably reflect correctness for all models. Among reflexive methods, P(True) is competitive, reaching 0.83 on Gemini-2.5-Flash-Lite and 0.82 on GPT-4o, while verbalized confidence is inconsistent (0.60–0.80).
4.3
Java (MultiPL-E)
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
red!45!white0.551
\cellcolor
red!35!white0.588
\cellcolor
blue!5!white0.637
\cellcolor
red!35!white0.572
\cellcolor
blue!5!white0.638
Min. Prob.
\cellcolor
blue!5!white0.635
\cellcolor
red!15!white0.618
\cellcolor
blue!45!white
0.705
\cellcolor
red!25!white0.599
\cellcolor
blue!15!white0.647
Prob. Margin
\cellcolor
red!45!white0.525
\cellcolor
red!25!white0.596
\cellcolor
red!25!white0.601
\cellcolor
red!35!white0.553
\cellcolor
blue!5!white0.640
Avg. Tok. Neg.
\cellcolor
red!45!white0.536
\cellcolor
red!25!white0.598
\cellcolor
red!25!white0.589
\cellcolor
red!45!white0.551
\cellcolor
blue!15!white0.644
Min. Tok. Neg.
\cellcolor
blue!15!white0.652
\cellcolor
blue!5!white0.644
\cellcolor
blue!25!white0.674
\cellcolor
red!5!white0.632
\cellcolor
blue!15!white0.653
Functional Equivalence Methods
Func. Equiv.
\cellcolor
red!15!white0.616
\cellcolor
blue!25!white
0.665
\cellcolor
blue!35!white0.690
\cellcolor
blue!35!white0.681
\cellcolor
blue!35!white0.687
Func. Entropy
\cellcolor
red!5!white0.628
\cellcolor
blue!25!white0.662
\cellcolor
blue!45!white0.701
\cellcolor
blue!45!white
0.695
\cellcolor
blue!35!white0.686
Func. Sets
\cellcolor
red!5!white0.623
\cellcolor
blue!25!white0.663
\cellcolor
blue!45!white0.697
\cellcolor
blue!45!white0.693
\cellcolor
blue!35!white
0.691
Similarity-Based Methods
Cos. Sim.
\cellcolor
blue!15!white0.645
\cellcolor
red!5!white0.627
\cellcolor
red!15!white0.615
\cellcolor
red!15!white0.610
\cellcolor
red!5!white0.626
CodeBLEU
\cellcolor
blue!35!white
0.690
\cellcolor
blue!25!white0.662
\cellcolor
blue!25!white0.676
\cellcolor
blue!15!white0.658
\cellcolor
blue!25!white0.672
Reflexive Methods
Verb. Conf.
\cellcolor
red!5!white0.623
\cellcolor
red!45!white0.548
\cellcolor
red!25!white0.595
\cellcolor
red!15!white0.615
\cellcolor
red!25!white0.592
P(True)
\cellcolor
red!45!white0.529
\cellcolor
red!15!white0.616
\cellcolor
red!45!white0.548
\cellcolor
blue!5!white0.640
\cellcolor
blue!35!white0.687
Table 3:
Code correctness AUROC on MultiPL-E (Java). Higher is better; red = low, blue = high.
Table
3
presents AUROC results for predicting functional correctness on MultiPL-E (Java). Model accuracy ranges from 0.49 (Gemini-2.5-Flash-Lite) to 0.57 (GPT-4o). Overall AUROC scores are lower than on Python problems, with most methods falling between 0.55–0.70 and limited separation between scorer families. As with Python, sampling-based methods using LLM-based functional equivalence achieve the strongest performance, though the margin over token-probability methods is less pronounced. Functional entropy and functional sets confidence reach approximately 0.70 on Gemini-2.5-Flash-Lite and GPT-4o-mini, while functional equivalence rate performs comparably. CodeBLEU consistency shows competitive results, achieving 0.69 on Gemini-2.5-Flash, suggesting that syntax-aware similarity metrics capture meaningful variation in Java code.
Token-probability methods perform moderately well on Java, with minimum probability achieving the highest AUROC of 0.705 on Gemini-2.5-Flash-Lite, outperforming several sampling-based methods for that model. Minimum token negentropy is consistent across models, ranging from 0.63 to 0.67. Among reflexive methods, P(True) achieves its best performance on GPT-4o (0.687), with ranking of AUROC across models mostly consistent with pass@1 rates, while verbalized confidence is consistently weaker (0.55–0.62).
4.4
SQL (LiveSQLBench)
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
red!45!white0.554
\cellcolor
red!45!white0.529
\cellcolor
red!15!white0.658
\cellcolor
blue!5!white0.678
\cellcolor
red!25!white0.646
Min. Prob.
\cellcolor
red!25!white0.628
\cellcolor
red!35!white0.602
\cellcolor
red!25!white0.641
\cellcolor
red!5!white0.672
\cellcolor
blue!5!white0.679
Prob. Margin
\cellcolor
red!45!white0.546
\cellcolor
red!45!white0.517
\cellcolor
red!25!white0.629
\cellcolor
red!5!white0.673
\cellcolor
red!35!white0.616
Avg. Tok. Neg.
\cellcolor
red!45!white0.558
\cellcolor
red!45!white0.528
\cellcolor
red!15!white0.662
\cellcolor
blue!5!white0.694
\cellcolor
red!25!white0.632
Min. Tok. Neg.
\cellcolor
red!15!white0.654
\cellcolor
red!35!white0.623
\cellcolor
blue!15!white0.712
\cellcolor
blue!5!white0.687
\cellcolor
blue!15!white0.706
Functional Equivalence Methods
Func. Equiv.
\cellcolor
red!15!white0.657
\cellcolor
blue!15!white0.702
\cellcolor
blue!25!white0.738
\cellcolor
blue!45!white0.782
\cellcolor
blue!35!white0.749
Func. Entropy
\cellcolor
red!5!white0.674
\cellcolor
blue!35!white0.745
\cellcolor
blue!35!white0.745
\cellcolor
blue!45!white0.840
\cellcolor
blue!45!white0.775
Func. Sets
\cellcolor
red!5!white
0.678
\cellcolor
blue!35!white
0.750
\cellcolor
blue!25!white0.743
\cellcolor
blue!45!white
0.842
\cellcolor
blue!45!white0.778
Similarity-Based Methods
Cos. Sim.
\cellcolor
red!15!white0.665
\cellcolor
blue!25!white0.726
\cellcolor
blue!5!white0.683
\cellcolor
blue!15!white0.705
\cellcolor
blue!25!white0.721
Reflexive Methods
Verb. Conf.
\cellcolor
red!45!white0.535
\cellcolor
red!35!white0.596
\cellcolor
blue!25!white0.739
\cellcolor
blue!25!white0.737
\cellcolor
red!35!white0.596
P(True)
\cellcolor
red!15!white0.647
\cellcolor
blue!15!white0.695
\cellcolor
blue!35!white
0.749
\cellcolor
blue!5!white0.687
\cellcolor
blue!45!white
0.818
Table 4:
Code correctness AUROC on LiveSQLBench (SQLite). Higher is better; red = low, blue = high.
Table
4
presents AUROC results for classifying functional correctness on LiveSQLBench. Model accuracy on this benchmark ranges from 0.21 (GPT-4o-mini) to 0.45 (Gemini-2.5-Pro and Gemini-2.5-Flash). Overall AUROC scores are moderate, with most methods falling in the 0.55–0.75 range and the best performers reaching 0.84. Again, sampling-based methods using LLM-based equivalence assessment consistently achieve the highest scores across all models, while token-probability methods show weaker discrimination for SQL generation compared to Python and Java.
Among sampling-based methods, functional sets confidence and functional entropy achieve the strongest performance. Notably, GPT-4o-mini reaches 0.842 AUROC with functional sets confidence despite having the lowest accuracy (0.21); we discuss the practical implications of this finding in Section
5
. Functional equivalence rate and cosine similarity also perform well, with scores above 0.70 for most models.
3
3
3
We omit CodeBLEU, as it does not support SQL.
Token-probability methods show limited effectiveness for SQL, with most scores in the 0.52–0.71 range. Sequence probability and probability margin perform near chance level for Gemini-2.5-Pro and Gemini-2.5-Flash (0.52–0.55), suggesting that token-level confidence scores carry little discriminative signal for SQL correctness on these models. Minimum token negentropy is the strongest performer among single-generation methods, achieving 0.71 on Gemini-2.5-Flash-Lite and GPT-4o. Among reflexive methods, P(True) achieves strong performance on GPT-4o (0.82), outperforming most other methods for that model, while verbalized confidence shows inconsistent results, ranging from 0.54 on Gemini-2.5-Flash to 0.74 on Gemini-2.5-Flash-Lite.
Figure 1:
AUROC of NLI-Based Methods vs. Code-Adapted (Functional Equivalence) Methods
4.5
NLI Methods vs. Code-Adapted Methods
To validate that replacing NLI-specific components with code-adapted analogs yields meaningful gains, we compare each functional equivalence method against its NLI-based counterpart: functional equivalence rate vs. non-contradiction probability
(Chen and Mueller,
2023
)
, functional entropy vs. NLI-based semantic entropy
(Kuhn
et al.
,
2023
)
, and functional sets confidence vs.  NLI-based semantic sets confidence
(Vashurin
et al.
,
2025a
)
.
4
4
4
Non-contradiction probability replaces
I
​
[
y
≡
y
j
]
I[y\equiv y_{j}]
with bi-directional average of NLI-estimated
1
−
P
​
(
contradict
)
1-P(\text{contradict})
.
Following previous studies
(Kuhn
et al.
,
2023
; Manakul
et al.
,
2023
; Lin
et al.
,
2024
; Vashurin
et al.
,
2025a
)
, we use
deberta-large-mnli
for our NLI model
(He
et al.
,
2021
)
. Figure
1
summarizes the results.
The comparison reveals two patterns. For the clustering-based methods (entropy and sets), functional equivalence yields large and consistent improvements across all benchmarks and models. NLI-based semantic entropy and semantic sets confidence perform near chance across all three languages, ranging from 0.47-0.58 on SQL, 0.48-0.56 on Java, and 0.50-0.53 on Python (with one exception at 0.74 on Gemini-2.5-Pro), a consequence of NLI models assigning nearly all responses to a single cluster regardless of functional differences (see Appendix
C
for full distributions). The gains from functional equivalence methods are largest on Python and SQL, where the gap exceeds 0.30 AUROC for most models. On Java, functional methods also outperform consistently (0.62-0.70 vs. 0.48-0.56), though the margin is smaller.
For the non-contradiction probability vs. functional equivalence rate comparison, the pattern is more nuanced. Non-contradiction often retains a useful continuous signal even when discrete clustering fails, achieving 0.70–0.71 on Python and 0.67–0.79 on SQL. However, functional equivalence rate exceeds it on 12 of 15 benchmark-model combinations, with the largest gains on Python (up to 0.16 AUROC on Gemini-2.5-Flash), while on Java gains are more modest (0.03–0.09). On SQL, the two methods perform comparably, likely because SQL syntax more closely resembles natural language (e.g.,
SELECT height, weight FROM mytable
), allowing the NLI model to partially capture semantic relationships between queries.
5
Discussion and Conclusion
Our results demonstrate that uncertainty quantification methods can effectively predict functional correctness in LLM-generated code, with functional equivalence methods achieving top AUROC in 11 out of 15 model-benchmark combinations. These methods also exhibit the best calibration across most settings without any explicit calibration procedure, meaning their confidence scores often serve as reliable probability estimates. The comparison with NLI-based counterparts suggests that NLG-specific subcomponents are the primary bottleneck. In particular, NLI-based clustering fails on code because it cannot reliably distinguish functionally different programs, while LLM-based functional equivalence assessment overcomes this limitation directly. This finding has implications beyond our specific methods, suggesting that other NLG-to-code transfer efforts relying on NLI or text embeddings may face similar degradation, and that LLM-based evaluation offers a viable path for domain adaptation of UQ methods more broadly.
Performance varies substantially across languages. We hypothesize that Python yields the highest AUROC overall due to richer training data and the relative expressiveness of Python solutions, which provide more signal for both token-probability and sampling-based methods. SQL poses the greatest challenge for token-probability methods, which frequently perform near chance, possibly because the constrained syntax of SQL queries leads to high token-level confidence regardless of correctness. Java falls between the two: overall AUROC is lower than Python across all method families, likely reflecting the more rigid boilerplate structure of Java solutions (e.g., class declarations, type annotations), which reduces the diversity of sampled responses and provides less signal for sampling-based methods. Sampling-based functional equivalence methods are more robust to these language-level differences, maintaining strong performance across all three settings. Notably, on SQL, GPT-4o-mini achieves 0.84 AUROC with functional entropy despite having the lowest accuracy (0.21), illustrating that sampling-based consistency can rank correct and incorrect generations effectively even for weak models. That said, UQ is most valuable as a complementary signal for a reasonably competent generator; when base accuracy is sufficiently low, the appropriate intervention is model selection rather than uncertainty-based filtering. The cross-language variation in NLI performance is itself informative: NLI-based non-contradiction performs comparably to functional equivalence on SQL, where query syntax is more similar to natural language, but gaps relative to functional equivalence are notably larger on Python and Java, where code structure diverges from natural language patterns.
To evaluate sensitivity to equivalence judge choice, we replace Gemini-2.5-Flash with Gemini-2.5-Flash-Lite and GPT-4o-mini as equivalence judges. We find Gemini-2.5-Flash-Lite produces AUROC within 0.02 of the primary judge across all configurations, while GPT-4o-mini shows moderate degradation (up to 0.07), with functional equivalence methods remaining the top-performing family in most configurations (Appendix
F.2
).
For practitioners, we recommend functional equivalence methods when the sampling and equivalence assessment costs are acceptable, as these methods generally perform best in classification and calibration. When sampling is not feasible, whether due to latency constraints or API costs, minimum token negentropy is the strongest single-generation alternative across benchmarks, achieving highest within-family AUROC in 12 of 15 model-benchmark combinations. Even at
m
=
10
m=10
generations, equivalence scoring costs are modest relative to the sampled generation cost that all sampling-based methods share (Appendix
E
). Moreover, our ablation in Appendix
F.1
shows that
m
=
5
m=5
captures most of the AUROC gain (within 0.01–0.02 of
m
=
10
m=10
across most settings), reducing functional equivalence rate to 5 judge calls per prompt and clustering-based methods to at most 15.
All methods evaluated in this paper are available
through
uqlm
, our
open-source library for LLM uncertainty quantification. Future work includes extending evaluation to additional programming languages and models as well as exploring hybrid approaches that use UQ scores to selectively trigger execution-based verification in settings where test generation is possible but expensive.
Limitations
Our study has several limitations that should be considered when interpreting the results.
Coverage of benchmarks and programming languages.
We evaluate on three benchmarks covering Python, Java, and SQL, which represent a subset of programming languages and task types. Our findings may not generalize to other languages with different syntactic properties (e.g., statically typed languages like Rust or Haskell), to longer code generation tasks involving multi-file projects, or to tasks requiring interaction with external APIs or databases. LiveSQLBench contains only 270 problems, which limits statistical power for SQL-specific conclusions. In particular, cross-method comparisons on SQL should be interpreted with more caution than those on Python (1,055 problems) or Java (386 problems), and claims about SQL-specific patterns, such as the relative competitiveness of NLI-based methods on SQL syntax, would benefit from validation on larger benchmarks as they become available.
Model coverage.
All five models evaluated are closed-source API models from two providers (OpenAI and Google). Other models may differ in calibration properties and generation characteristics. In particular, our evaluation does not include open-weight models (e.g., Llama, Mistral, Qwen), which are increasingly common in cost-sensitive deployment settings. Our results should not be assumed to transfer directly to these or other LLMs without further evaluation.
Single-turn scope.
Our evaluation targets single-turn code generation on established benchmarks. Extending to multi-turn agentic settings, where generated code is iteratively refined or executed as part of a broader tool-use pipeline, is a natural next step but may introduce additional challenges such as error propagation across turns.
Computational cost.
Sampling-based methods require generating multiple responses per prompt and, in the case of functional equivalence methods, additional LLM calls for pairwise equivalence assessment. This increases both latency and cost relative to single-generation token-probability methods (see Appendix
E
).
Correctness definition.
We define functional correctness using test-based evaluation (i.e., a solution is correct if it passes all provided test cases). This is an approximation, as test suites may not cover all edge cases, and a solution that passes all tests may still contain latent bugs. This limitation applies uniformly across all methods for both Python and Java.
Equivalence judge and model overlap.
We use Gemini-2.5-Flash as the functional equivalence judge across all experiments, including settings where Gemini models also serve as the code generator. In principle, a judge could exhibit differential accuracy when assessing code from models within its own family versus code from other providers. However, any such bias is unlikely to artificially inflate performance for same-family generators, since the judge determines cluster structure rather than correctness labels. Our execution-based validation (Appendix
D
) and judge sensitivity ablation (Appendix
F.2
) further mitigate this concern.
Conflict of Interest
Mohit Singh Chauhan, Zeya Ahmad, and Ho-Kyeong Ra are employed by, and receive stock and equity from, CVS Health Corporation. Dylan Bouchard was employed by, and received stock and equity from, CVS Health Corporation at the time this work was conducted.
Disclaimer
Prompts are included solely for reproducibility and do not imply endorsement or affiliation. Gemini is a trademark of Google and GPT is a trademark of OpenAI. This is an independent publication and has not been authorized, endorsed, or sponsored by Google or OpenAI.
References
D. Bouchard, M. S. Chauhan, D. Skarbrevik, H. Ra, V. Bajaj, and Z. Ahmad (2026)
UQLM: a python package for uncertainty quantification in large language models
.
Journal of Machine Learning Research
27
(
13
),
pp. 1–10
.
External Links:
Link
Cited by:
§3.2.1
,
footnote 1
.
D. Bouchard and M. S. Chauhan (2025)
Uncertainty quantification for language models: a suite of black-box, white-box, LLM judge, and ensemble scorers
.
Transactions on Machine Learning Research
.
Note:
External Links:
ISSN 2835-8856
,
Link
Cited by:
§2
,
§3.2.1
,
§3.2.2
.
F. Cassano, J. Gouwar, D. Nguyen, S. Nguyen, L. Phipps-Costin, D. Pinckney, M. Yee, Y. Zi, C. J. Anderson, M. Q. Feldman, A. Guha, M. Greenberg, and A. Jangda (2022)
MultiPL-e: a scalable and extensible approach to benchmarking neural code generation
.
External Links:
2208.08227
,
Link
Cited by:
§4.1
.
J. Chen and J. Mueller (2023)
Quantifying uncertainty in answers from any language model and enhancing their trustworthiness
.
External Links:
2308.16175
,
Link
Cited by:
§2
,
§4.5
.
J. R. Cole, M. J. Q. Zhang, D. Gillick, J. M. Eisenschlos, B. Dhingra, and J. Eisenstein (2023)
Selectively answering ambiguous questions
.
External Links:
2305.14613
,
Link
Cited by:
§2
.
S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal (2024)
Detecting hallucinations in large language models using semantic entropy
.
Nature
630
(
8017
),
pp. 625–630
.
External Links:
ISSN 1476-4687
,
Document
,
Link
Cited by:
§1
,
§2
.
D. Farr, N. Manzonelli, I. Cruickshank, and J. West (2024)
RED-ct: a systems design methodology for using llm-labeled data to train and deploy edge classifiers for computational social science
.
External Links:
2408.08217
,
Link
Cited by:
§2
,
§3.1
.
C. Gao, G. Fan, C. Y. Chong, S. Chen, C. Liu, D. Lo, Z. Zheng, and Q. Liao (2025)
A systematic literature review of code hallucinations in llms: characterization, mitigation methods, challenges, and future directions for reliable ai
.
arXiv preprint arXiv:2511.00776
.
Cited by:
§1
,
§2
.
[9]
Google
External Links:
Link
Cited by:
§4.1
.
K. He, M. Liu, C. Wang, Z. Li, Y. Wang, X. Peng, and Z. Zheng (2025)
AdaDec: uncertainty-guided adaptive decoding for llm-based code generation
.
arXiv preprint arXiv:2506.08980
.
Cited by:
§2
.
P. He, X. Liu, J. Gao, and W. Chen (2021)
DeBERTa: decoding-enhanced bert with disentangled attention
.
External Links:
2006.03654
,
Link
Cited by:
§4.5
.
K. Healy, B. Srinivasan, V. Madathil, and J. Wu (2026)
Internal representations as indicators of hallucinations in agent tool selection
.
External Links:
2601.05214
,
Link
Cited by:
§2
.
L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin, and T. Liu (2023)
A survey on hallucination in large language models: principles, taxonomy, challenges, and open questions
.
External Links:
2311.05232
,
Link
Cited by:
§2
.
Y. Huang, J. Song, Z. Wang, S. Zhao, H. Chen, F. Juefei-Xu, and L. Ma (2025)
Look before you leap: an exploratory study of uncertainty analysis for large language models
.
IEEE Transactions on Software Engineering
51
(
2
),
pp. 413–429
.
External Links:
ISSN 2326-3881
,
Link
,
Document
Cited by:
§2
.
N. Jain, K. Han, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica (2024)
LiveCodeBench: holistic and contamination free evaluation of large language models for code
.
External Links:
2403.07974
,
Link
Cited by:
§1
,
§4.1
.
N. Jiang, Q. Li, L. Tan, and T. Zhang (2024)
Collu-bench: a benchmark for predicting language model hallucinations in code
.
External Links:
2410.09997
,
Link
Cited by:
§2
.
S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson, S. Johnston, S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen, Y. Bai, S. Bowman, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion, S. Kravec, L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei, T. Brown, J. Clark, N. Joseph, B. Mann, S. McCandlish, C. Olah, and J. Kaplan (2022)
Language models (mostly) know what they know
.
External Links:
2207.05221
,
Link
Cited by:
§2
,
§3.3
.
L. Kuhn, Y. Gal, and S. Farquhar (2023)
Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation
.
External Links:
2302.09664
,
Link
Cited by:
§B.1
,
§2
,
§3.2.1
,
§3.2.1
,
§4.5
.
Z. Lin, S. Trivedi, and J. Sun (2024)
Generating with confidence: uncertainty quantification for black-box large language models
.
External Links:
2305.19187
,
Link
Cited by:
§3.2.1
,
§4.5
.
F. Liu, Y. Liu, L. Shi, Z. Yang, L. Zhang, X. Lian, Z. Li, and Y. Ma (2026)
Beyond functional correctness: exploring hallucinations in llm-generated code
.
External Links:
2404.00971
,
Link
Cited by:
§2
.
A. Malinin and M. Gales (2021)
Uncertainty estimation in autoregressive structured prediction
.
External Links:
2002.07650
,
Link
Cited by:
§2
,
§3.1
.
P. Manakul, A. Liusie, and M. J. F. Gales (2023)
SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models
.
External Links:
2303.08896
,
Link
Cited by:
§2
,
§3.1
,
§3.1
,
§3.1
,
§4.5
.
OpenAI (2025)
Introducing gpt-4.5 | openai
.
External Links:
Link
Cited by:
§4.1
.
X. Qiu and R. Miikkulainen (2024)
Semantic density: uncertainty quantification for large language models through confidence measurement in semantic space
.
External Links:
2405.13845
,
Link
Cited by:
§2
.
S. Ren, D. Guo, S. Lu, L. Zhou, S. Liu, D. Tang, N. Sundaresan, M. Zhou, A. Blanco, and S. Ma (2020)
CodeBLEU: a method for automatic evaluation of code synthesis
.
External Links:
2009.10297
,
Link
Cited by:
§3.2.2
.
D. Scalena, L. Zotos, E. Fersini, M. Nissim, and A. Üstün (2025)
EAGER: entropy-aware generation for adaptive inference-time scaling
.
External Links:
2510.11170
,
Link
Cited by:
§2
,
§2
,
§3.1
,
§3.1
.
A. Sharma and C. David (2025)
Assessing correctness in llm-based code generation via uncertainty estimation
.
arXiv preprint arXiv:2502.11620
.
Cited by:
§1
,
§2
,
§3.2.2
.
O. Shorinwa, Z. Mei, J. Lidard, A. Z. Ren, and A. Majumdar (2024)
A survey on uncertainty quantification of large language models: taxonomy, open research challenges, and future directions
.
External Links:
2412.05563
,
Link
Cited by:
§2
.
C. Spiess, D. Gros, K. S. Pai, M. Pradel, M. R. I. Rabin, A. Alipour, S. Jha, P. Devanbu, and T. Ahmed (2024)
Calibration and correctness of language models for code
.
External Links:
2402.02047
,
Link
Cited by:
§2
.
K. Tantithamthavorn, H. Y. Lin, P. Thongtanunam, W. Charoenwet, M. Jeong, and M. Wu (2026)
HalluJudge: a reference-free hallucination detection for context misalignment in code review automation
.
External Links:
2601.19072
,
Link
Cited by:
§2
.
B. Team (2024)
LiveSQLBench: a dynamic and contamination-free benchmark for evaluating llms on real-world text-to-sql tasks
.
Note:
https://github.com/bird-bench/livesqlbenchAccessed: 2025-05-22
Cited by:
§1
,
§4.1
.
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. D. Manning (2023)
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
External Links:
2305.14975
,
Link
Cited by:
§2
,
§3.3
.
Y. Tian, W. Yan, Q. Yang, X. Zhao, Q. Chen, W. Wang, Z. Luo, L. Ma, and D. Song (2025)
CodeHalu: investigating code hallucinations in llms via execution-based verification
.
External Links:
2405.00253
,
Link
Cited by:
§1
,
§2
.
H. Vasconcelos, G. Bansal, A. Fourney, Q. V. Liao, and J. Wortman Vaughan (2025)
Generation probabilities are not enough: uncertainty highlighting in ai code completions
.
ACM Transactions on Computer-Human Interaction
32
(
1
),
pp. 1–30
.
Cited by:
§2
.
R. Vashurin, E. Fadeeva, A. Vazhentsev, L. Rvanova, D. Vasilev, A. Tsvigun, S. Petrakov, R. Xing, A. Sadallah, K. Grishchenkov, A. Panchenko, T. Baldwin, P. Nakov, M. Panov, and A. Shelmanov (2025a)
Benchmarking uncertainty quantification methods for large language models with lm-polygraph
.
Transactions of the Association for Computational Linguistics
13
,
pp. 220–248
.
External Links:
ISSN 2307-387X
,
Link
,
Document
Cited by:
§1
,
§2
,
§3.1
,
§4.5
.
R. Vashurin, M. Goloburda, A. Ilina, A. Rubashevskii, P. Nakov, A. Shelmanov, and M. Panov (2025b)
Uncertainty quantification for llms through minimum bayes risk: bridging confidence and consistency
.
External Links:
2502.04964
,
Link
Cited by:
§B.1
,
§2
.
A. Vazhentsev, L. Rvanova, G. Kuzmin, E. Fadeeva, I. Lazichny, A. Panchenko, M. Panov, T. Baldwin, M. Sachan, P. Nakov,
et al.
(2025)
Uncertainty-aware attention heads: efficient unsupervised uncertainty quantification for llms
.
arXiv preprint arXiv:2505.20045
.
Cited by:
§2
.
B. Yang, Y. Xia, W. Sun, and Y. Liu (2025)
Hallucination detection for llm-based text-to-sql generation via two-stage metamorphic testing
.
External Links:
2512.22250
,
Link
Cited by:
§2
.
Y. Zhu, G. Li, X. Jiang, J. Li, H. Mei, Z. Jin, and Y. Dong (2025)
Uncertainty-guided chain-of-thought for code generation with llms
.
arXiv preprint arXiv:2503.15341
.
Cited by:
§2
.
Appendix A
Calibration
We report two calibration metrics for all methods evaluated in the main text: Expected Calibration Error (ECE) and Brier Score. ECE measures the average gap between predicted confidence and observed accuracy across binned confidence intervals, while Brier Score measures the mean squared error between confidence scores and binary correctness labels. For both metrics, lower values indicate better calibration. Tables
5
,
6
, and
7
report ECE results, while Tables
8
,
9
, and
10
report Brier Score across all three benchmarks.
The calibration results are broadly consistent with the AUROC findings reported in the main text. Functional equivalence methods (functional entropy, functional sets confidence) achieve the best calibration across most benchmark-model combinations, with ECE values frequently below 0.20 and competitive Brier scores. This is particularly notable on Python problems, where these methods produce well-calibrated confidence estimates without any explicit calibration procedure.
Token-probability methods show a wide calibration range. Minimum token negentropy and minimum probability tend to be better calibrated than sequence probability, mean token negentropy, and probability margin, which often exhibit high ECE, particularly on SQL where values exceed 0.70 in several cases. This pattern is consistent with the AUROC finding that aggregated token-probability methods are often confidently wrong on SQL.
Normalized cosine similarity, despite reasonable AUROC performance, shows poor calibration on SQL and Java, with ECE and Brier scores comparable to the weakest token-probability methods. This suggests that embedding-based similarity scores do not naturally align with correctness probabilities, even when they provide useful ranking signal.
Among reflexive methods, P(True) shows variable calibration across benchmarks, while verbalized confidence is generally poorly calibrated, consistent with prior observations that LLMs tend to express overconfident or inconsistent self-assessments.
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
blue!35!white0.051
\cellcolor
blue!45!white
0.015
\cellcolor
red!5!white0.253
\cellcolor
red!25!white0.352
\cellcolor
red!5!white0.220
Min. Prob.
\cellcolor
red!45!white0.726
\cellcolor
red!45!white0.824
\cellcolor
red!45!white0.502
\cellcolor
red!35!white0.390
\cellcolor
red!45!white0.501
Prob. Margin
\cellcolor
blue!35!white0.059
\cellcolor
blue!45!white0.022
\cellcolor
red!15!white0.262
\cellcolor
red!35!white0.414
\cellcolor
red!25!white0.325
Avg. Tok. Neg.
\cellcolor
blue!15!white0.091
\cellcolor
blue!35!white0.050
\cellcolor
red!15!white0.292
\cellcolor
red!35!white0.444
\cellcolor
red!25!white0.366
Min. Tok. Neg.
\cellcolor
red!45!white0.535
\cellcolor
red!45!white0.538
\cellcolor
red!15!white0.271
\cellcolor
blue!25!white0.082
\cellcolor
red!5!white0.251
Functional Equivalence Methods
Func. Equiv. Rate
\cellcolor
blue!5!white0.110
\cellcolor
red!5!white0.200
\cellcolor
blue!5!white0.113
\cellcolor
blue!15!white0.100
\cellcolor
blue!5!white0.117
Func. Neg.
\cellcolor
blue!25!white0.073
\cellcolor
blue!5!white0.152
\cellcolor
blue!45!white
0.038
\cellcolor
blue!45!white
0.041
\cellcolor
blue!35!white
0.046
Func. Sets
\cellcolor
blue!45!white
0.024
\cellcolor
blue!25!white0.080
\cellcolor
blue!25!white0.071
\cellcolor
blue!5!white0.110
\cellcolor
blue!15!white0.090
Similarity-Based Methods
Cos. Sim.
\cellcolor
blue!35!white0.044
\cellcolor
blue!45!white0.039
\cellcolor
red!15!white0.273
\cellcolor
red!35!white0.430
\cellcolor
red!25!white0.362
CodeBLEU
\cellcolor
red!35!white0.428
\cellcolor
red!35!white0.468
\cellcolor
blue!15!white0.085
\cellcolor
blue!25!white0.082
\cellcolor
blue!15!white0.100
Reflexive Methods
Verb. Conf.
\cellcolor
blue!25!white0.072
\cellcolor
blue!35!white0.060
\cellcolor
red!5!white0.260
\cellcolor
red!15!white0.281
\cellcolor
red!25!white0.303
P(True)
\cellcolor
blue!5!white0.111
\cellcolor
blue!15!white0.087
\cellcolor
red!5!white0.210
\cellcolor
red!25!white0.349
\cellcolor
red!15!white0.300
Table 5:
ECE for predicting code correctness on LiveCodeBench (Python). Lower is better. Colors reflect rankings: blue (best) to red (worst). The best-calibrated scorer based on ECE is
underlined
.
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
red!25!white0.431
\cellcolor
red!35!white0.435
\cellcolor
red!45!white0.465
\cellcolor
red!5!white0.374
\cellcolor
red!5!white0.359
Min. Prob.
\cellcolor
blue!15!white0.244
\cellcolor
blue!5!white0.249
\cellcolor
blue!25!white0.211
\cellcolor
blue!5!white0.289
\cellcolor
blue!5!white0.300
Prob. Margin
\cellcolor
red!35!white0.433
\cellcolor
red!35!white0.432
\cellcolor
red!45!white0.468
\cellcolor
red!15!white0.386
\cellcolor
red!15!white0.375
Avg. Tok. Neg.
\cellcolor
red!45!white0.463
\cellcolor
red!35!white0.451
\cellcolor
red!45!white0.493
\cellcolor
red!15!white0.413
\cellcolor
red!15!white0.400
Min. Tok. Neg.
\cellcolor
blue!35!white0.123
\cellcolor
blue!35!white0.164
\cellcolor
blue!45!white
0.075
\cellcolor
blue!45!white
0.105
\cellcolor
blue!45!white0.099
Functional Equivalence Methods
Func. Equiv. Rate
\cellcolor
blue!15!white0.241
\cellcolor
blue!25!white0.212
\cellcolor
blue!15!white0.222
\cellcolor
blue!15!white0.221
\cellcolor
blue!25!white0.198
Func. Neg.
\cellcolor
blue!35!white0.189
\cellcolor
blue!25!white0.206
\cellcolor
blue!15!white0.223
\cellcolor
blue!35!white0.197
\cellcolor
blue!35!white0.155
Func. Sets
\cellcolor
blue!5!white0.294
\cellcolor
blue!5!white0.297
\cellcolor
red!5!white0.308
\cellcolor
blue!5!white0.262
\cellcolor
blue!15!white0.229
Similarity-Based Methods
Cos. Sim.
\cellcolor
red!35!white0.448
\cellcolor
red!25!white0.420
\cellcolor
red!45!white0.486
\cellcolor
red!25!white0.414
\cellcolor
red!15!white0.394
CodeBLEU
\cellcolor
blue!45!white
0.089
\cellcolor
blue!45!white
0.086
\cellcolor
blue!25!white0.209
\cellcolor
blue!35!white0.149
\cellcolor
blue!45!white
0.084
Reflexive Methods
Verb. Conf.
\cellcolor
red!15!white0.375
\cellcolor
red!25!white0.425
\cellcolor
red!35!white0.447
\cellcolor
blue!25!white0.220
\cellcolor
red!5!white0.342
P(True)
\cellcolor
red!45!white0.466
\cellcolor
red!25!white0.424
\cellcolor
red!25!white0.416
\cellcolor
red!5!white0.350
\cellcolor
red!5!white0.324
Table 6:
ECE for predicting code correctness on MultiPL-E (Java). Lower is better. Colors reflect rankings: blue (best) to red (worst). The best-calibrated scorer based on ECE is
underlined
.
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
red!25!white0.523
\cellcolor
red!15!white0.521
\cellcolor
red!35!white0.714
\cellcolor
red!35!white0.675
\cellcolor
red!5!white0.417
Min. Prob.
\cellcolor
blue!5!white0.260
\cellcolor
blue!15!white0.251
\cellcolor
blue!25!white0.150
\cellcolor
blue!35!white0.144
\cellcolor
blue!5!white0.260
Prob. Margin
\cellcolor
red!25!white0.523
\cellcolor
red!15!white0.520
\cellcolor
red!35!white0.717
\cellcolor
red!45!white0.724
\cellcolor
red!35!white0.592
Avg. Tok. Neg.
\cellcolor
red!25!white0.533
\cellcolor
red!25!white0.533
\cellcolor
red!45!white0.738
\cellcolor
red!45!white0.752
\cellcolor
red!35!white0.633
Min. Tok. Neg.
\cellcolor
blue!35!white
0.126
\cellcolor
blue!25!white0.164
\cellcolor
blue!15!white0.180
\cellcolor
blue!15!white0.257
\cellcolor
blue!45!white
0.040
Functional Equivalence Methods
Func. Equiv. Rate
\cellcolor
blue!5!white0.262
\cellcolor
blue!15!white0.208
\cellcolor
blue!25!white0.154
\cellcolor
blue!35!white0.124
\cellcolor
blue!25!white0.177
Func. Neg.
\cellcolor
blue!15!white0.192
\cellcolor
blue!45!white0.110
\cellcolor
blue!35!white
0.130
\cellcolor
blue!45!white
0.067
\cellcolor
blue!35!white0.119
Func. Sets
\cellcolor
blue!25!white0.157
\cellcolor
blue!45!white
0.102
\cellcolor
blue!25!white0.146
\cellcolor
blue!45!white0.083
\cellcolor
blue!45!white0.089
Similarity-Based Methods
Cos. Sim.
\cellcolor
red!15!white0.516
\cellcolor
red!15!white0.513
\cellcolor
red!45!white0.727
\cellcolor
red!45!white0.756
\cellcolor
red!35!white0.648
Reflexive Methods
Verb. Conf.
\cellcolor
blue!5!white0.412
\cellcolor
red!5!white0.464
\cellcolor
red!5!white0.441
\cellcolor
red!15!white0.509
\cellcolor
red!25!white0.573
P(True)
\cellcolor
red!5!white0.485
\cellcolor
red!5!white0.423
\cellcolor
blue!5!white0.400
\cellcolor
red!15!white0.496
\cellcolor
blue!5!white0.323
Table 7:
ECE for predicting code correctness on LiveSQLBench (SQLite). Lower is better. Colors reflect rankings: blue (best) to red (worst). The best-calibrated scorer based on ECE is
underlined
.
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
blue!25!white0.109
\cellcolor
blue!45!white0.078
\cellcolor
red!5!white0.263
\cellcolor
red!25!white0.348
\cellcolor
red!5!white0.258
Min. Prob.
\cellcolor
red!45!white0.678
\cellcolor
red!45!white0.767
\cellcolor
red!45!white0.449
\cellcolor
red!35!white0.373
\cellcolor
red!45!white0.485
Prob. Margin
\cellcolor
blue!25!white0.112
\cellcolor
blue!45!white0.079
\cellcolor
red!15!white0.272
\cellcolor
red!35!white0.406
\cellcolor
red!25!white0.332
Avg. Tok. Neg.
\cellcolor
blue!25!white0.118
\cellcolor
blue!45!white0.081
\cellcolor
red!15!white0.294
\cellcolor
red!45!white0.436
\cellcolor
red!35!white0.365
Min. Tok. Neg.
\cellcolor
red!35!white0.416
\cellcolor
red!35!white0.371
\cellcolor
red!5!white0.244
\cellcolor
blue!5!white0.198
\cellcolor
red!5!white0.263
Functional Equivalence Methods
Func. Equiv. Rate
\cellcolor
blue!25!white0.108
\cellcolor
blue!15!white0.151
\cellcolor
blue!5!white0.161
\cellcolor
blue!15!white0.161
\cellcolor
blue!5!white0.165
Func. Neg.
\cellcolor
blue!35!white0.092
\cellcolor
blue!35!white0.104
\cellcolor
blue!25!white
0.145
\cellcolor
blue!15!white
0.152
\cellcolor
blue!15!white
0.153
Func. Sets
\cellcolor
blue!35!white
0.083
\cellcolor
blue!45!white0.073
\cellcolor
blue!15!white0.150
\cellcolor
blue!5!white0.166
\cellcolor
blue!15!white0.161
Similarity-Based Methods
Cos. Sim.
\cellcolor
blue!35!white0.108
\cellcolor
blue!45!white0.073
\cellcolor
red!15!white0.281
\cellcolor
red!45!white0.420
\cellcolor
red!35!white0.363
CodeBLEU
\cellcolor
red!15!white0.289
\cellcolor
red!25!white0.294
\cellcolor
blue!5!white0.179
\cellcolor
blue!5!white0.203
\cellcolor
red!5!white0.219
Reflexive Methods
Verb. Conf.
\cellcolor
blue!35!white0.090
\cellcolor
blue!45!white
0.067
\cellcolor
red!15!white0.279
\cellcolor
red!25!white0.295
\cellcolor
red!25!white0.302
P(True)
\cellcolor
blue!25!white0.111
\cellcolor
blue!35!white0.086
\cellcolor
red!5!white0.212
\cellcolor
red!25!white0.348
\cellcolor
red!15!white0.290
Table 8:
Brier Score for predicting code correctness on LiveCodeBench (Python). Lower is better. Colors reflect rankings: blue (best) to red (worst). The best-calibrated scorer based on Brier Score is
underlined
.
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
red!35!white0.434
\cellcolor
red!35!white0.435
\cellcolor
red!45!white0.460
\cellcolor
red!15!white0.383
\cellcolor
red!5!white0.364
Min. Prob.
\cellcolor
blue!5!white0.306
\cellcolor
blue!5!white0.303
\cellcolor
blue!35!white0.263
\cellcolor
red!5!white0.340
\cellcolor
blue!5!white0.325
Prob. Margin
\cellcolor
red!35!white0.438
\cellcolor
red!25!white0.432
\cellcolor
red!45!white0.465
\cellcolor
red!15!white0.394
\cellcolor
red!5!white0.378
Avg. Tok. Neg.
\cellcolor
red!45!white0.463
\cellcolor
red!35!white0.450
\cellcolor
red!45!white0.490
\cellcolor
red!25!white0.415
\cellcolor
red!15!white0.400
Min. Tok. Neg.
\cellcolor
blue!35!white0.250
\cellcolor
blue!25!white0.263
\cellcolor
blue!45!white
0.232
\cellcolor
blue!35!white
0.245
\cellcolor
blue!45!white0.237
Functional Equivalence Methods
Func. Equiv. Rate
\cellcolor
blue!15!white0.303
\cellcolor
blue!15!white0.280
\cellcolor
blue!25!white0.274
\cellcolor
blue!25!white0.273
\cellcolor
blue!35!white0.259
Func. Neg.
\cellcolor
blue!15!white0.284
\cellcolor
blue!15!white0.275
\cellcolor
blue!25!white0.272
\cellcolor
blue!35!white0.254
\cellcolor
blue!45!white0.243
Func. Sets
\cellcolor
blue!5!white0.326
\cellcolor
blue!5!white0.314
\cellcolor
blue!5!white0.314
\cellcolor
blue!15!white0.283
\cellcolor
blue!25!white0.266
Similarity-Based Methods
Cos. Sim.
\cellcolor
red!35!white0.445
\cellcolor
red!25!white0.419
\cellcolor
red!45!white0.484
\cellcolor
red!15!white0.413
\cellcolor
red!15!white0.396
CodeBLEU
\cellcolor
blue!45!white
0.231
\cellcolor
blue!45!white
0.236
\cellcolor
blue!25!white0.271
\cellcolor
blue!35!white0.252
\cellcolor
blue!45!white
0.233
Reflexive Methods
Verb. Conf.
\cellcolor
red!15!white0.379
\cellcolor
red!25!white0.425
\cellcolor
red!35!white0.438
\cellcolor
blue!15!white0.282
\cellcolor
red!5!white0.354
P(True)
\cellcolor
red!45!white0.466
\cellcolor
red!25!white0.423
\cellcolor
red!25!white0.419
\cellcolor
red!5!white0.360
\cellcolor
red!5!white0.331
Table 9:
Brier Score for predicting code correctness on MultiPL-E (Java). Lower is better. Colors reflect rankings: blue (best) to red (worst). The best-calibrated scorer based on Brier Score is
underlined
.
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
Token-Probability Methods
Seq. Prob.
\cellcolor
red!25!white0.520
\cellcolor
red!15!white0.519
\cellcolor
red!35!white0.687
\cellcolor
red!35!white0.627
\cellcolor
red!5!white0.398
Min. Prob.
\cellcolor
blue!5!white0.302
\cellcolor
blue!5!white0.308
\cellcolor
blue!35!white0.199
\cellcolor
blue!35!white0.175
\cellcolor
blue!15!white0.266
Prob. Margin
\cellcolor
red!25!white0.521
\cellcolor
red!15!white0.518
\cellcolor
red!45!white0.692
\cellcolor
red!35!white0.686
\cellcolor
red!35!white0.553
Avg. Tok. Neg.
\cellcolor
red!25!white0.532
\cellcolor
red!25!white0.532
\cellcolor
red!45!white0.724
\cellcolor
red!45!white0.729
\cellcolor
red!35!white0.604
Min. Tok. Neg.
\cellcolor
blue!25!white
0.248
\cellcolor
blue!5!white0.266
\cellcolor
blue!25!white0.200
\cellcolor
blue!25!white0.225
\cellcolor
blue!35!white0.184
Functional Equivalence Methods
Func. Equiv. Rate
\cellcolor
blue!5!white0.302
\cellcolor
blue!15!white0.263
\cellcolor
blue!45!white0.169
\cellcolor
blue!45!white0.147
\cellcolor
blue!25!white0.200
Func. Neg.
\cellcolor
blue!15!white0.261
\cellcolor
blue!25!white0.215
\cellcolor
blue!45!white
0.168
\cellcolor
blue!45!white
0.129
\cellcolor
blue!35!white
0.183
Func. Sets
\cellcolor
blue!15!white
0.248
\cellcolor
blue!25!white
0.207
\cellcolor
blue!35!white0.176
\cellcolor
blue!45!white0.135
\cellcolor
blue!45!white0.174
Similarity-Based Methods
Cos. Sim.
\cellcolor
red!15!white0.510
\cellcolor
red!15!white0.503
\cellcolor
red!45!white0.705
\cellcolor
red!45!white0.734
\cellcolor
red!35!white0.620
Reflexive Methods
Verb. Conf.
\cellcolor
red!5!white0.430
\cellcolor
red!5!white0.460
\cellcolor
blue!5!white0.368
\cellcolor
red!5!white0.431
\cellcolor
red!25!white0.548
P(True)
\cellcolor
red!15!white0.485
\cellcolor
red!5!white0.422
\cellcolor
blue!5!white0.381
\cellcolor
red!15!white0.477
\cellcolor
blue!15!white0.264
Table 10:
Brier Score for predicting code correctness on LiveSQLBench (SQLite). Lower is better. Colors reflect rankings: blue (best) to red (worst). The best-calibrated scorer based on Brier Score is
underlined
.
Appendix B
Hybrid Methods
Hybrid methods combine token-probability signals with sampling-based consistency measures, leveraging both the model’s internal confidence and agreement across multiple generations. We evaluate three hybrid methods described below. While these methods are reasonably competitive, none achieve the highest AUROC on any benchmark-model combination in our experiments, and we therefore present these results in the appendix rather than the main text.
B.1
Methods
Consistency and Confidence Approach (CoCoA).
CoCoA combines the length-normalized sequence probability of the original response with embedding-based consistency
(Vashurin
et al.
,
2025b
)
. Let
y
0
y_{0}
denote the original response and
{
y
~
1
,
…
,
y
~
m
}
\{\tilde{y}_{1},\ldots,\tilde{y}_{m}\}
denote the sampled responses. CoCoA is defined as:
CoCoA
​
(
y
;
𝐲
~
,
x
)
=
LNSP
​
(
y
)
⋅
NCS
​
(
y
;
𝐲
~
)
\text{CoCoA}(y;\tilde{\mathbf{y}},x)=\text{LNSP}(y)\cdot\text{NCS}(y;\tilde{\mathbf{y}})
We use the code embedding variant described in Section
3.2
, with
jinaai/jina-embeddings-v3
as the embedding model.
Monte Carlo Sequence Probability (MCSP).
This method computes the average length-normalized sequence probability across
m
m
sampled responses
{
y
1
,
…
,
y
m
}
\{y_{1},\ldots,y_{m}\}
(Kuhn
et al.
,
2023
)
:
MCSP
​
(
y
;
𝐲
~
,
x
)
=
1
m
+
1
​
∑
i
=
0
m
LNSP
​
(
y
i
)
\text{MCSP}(y;\tilde{\mathbf{y}},x)=\frac{1}{m+1}\sum_{i=0}^{m}\text{LNSP}(y_{i})
where
y
0
=
y
y_{0}=y
denotes the original response.
White-Box Normalized Functional Negentropy (WB-NFN).
In the hybrid setting, we weight cluster probabilities by the length-normalized sequence probabilities of responses within each cluster, rather than treating all responses equally:
P
​
(
C
)
=
∑
y
i
∈
C
LNSP
​
(
y
i
)
∑
i
=
0
m
LNSP
​
(
y
i
)
P(C)=\frac{\sum_{y_{i}\in C}\text{LNSP}(y_{i})}{\sum_{i=0}^{m}\text{LNSP}(y_{i})}
This white-box version replaces the frequency-based
P
​
(
C
)
P(C)
used in the black-box NFN (Section
3.2
) with a token-probability-weighted version. The remaining calculations, including LLM-based functional equivalence for clustering, are identical.
B.2
Results
Tables
11
,
12
, and
13
present AUROC results for hybrid methods across all three benchmarks.
Across all three benchmarks, no hybrid method achieves the top AUROC for any model. WB-NFN is the strongest of the three, reaching 0.850 on Python (Gemini-2.5-Flash) and 0.817 on SQL (GPT-4o-mini), but these scores are consistently matched or exceeded by the black-box functional entropy methods reported in the main text. This suggests that incorporating token-probability weighting into the cluster distribution does not provide additional discriminative signal beyond what frequency-based functional equivalence clustering already captures. MCSP shows high variance across models, performing well on Python for some models (0.821 on GPT-4o) but poorly on Java (0.538 on Gemini-2.5-Flash). CoCoA performs moderately across all benchmarks without distinguishing itself on any, indicating that the multiplicative combination of sequence probability and embedding similarity does not yield complementary signal for code generation.
Table 11:
Hybrid method AUROC on LiveCodeBench (Python).
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
MCSP
0.718
0.594
0.809
0.808
0.821
WB-NFN
0.850
0.802
0.787
0.789
0.825
CoCoA
0.783
0.793
0.790
0.772
0.746
Table 12:
Hybrid method AUROC on MultiPL-E (Java).
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
MCSP
0.538
0.588
0.585
0.557
0.645
WB-NFN
0.626
0.661
0.697
0.699
0.686
CoCoA
0.605
0.621
0.628
0.584
0.643
Table 13:
Hybrid method AUROC on LiveSQLBench (SQL).
Scorer
Gem-Fl
Gem-Pro
Gem-Fl-Lt
GPT4o-m
GPT4o
MCSP
0.559
0.632
0.654
0.719
0.748
WB-NFN
0.672
0.748
0.732
0.817
0.624
CoCoA
0.627
0.676
0.683
0.706
0.674
Appendix C
Semantic and Functional Sets Distributions
Figure
2
compares the distribution of cluster counts produced by NLI-based clustering and functional equivalence clustering across all models and languages. Overall, our results indicate that the number of clusters directly determines the behavior of functional entropy and functional sets confidence. In particular, when all responses collapse into a single cluster, entropy is zero and sets confidence is maximal, regardless of whether the underlying code is correct.
NLI-based clustering assigns the vast majority of responses to a single cluster across all settings, with over 80% of prompts producing exactly one cluster on Python and SQL. This collapse explains why NLI-based semantic entropy and semantic sets confidence perform near chance in the main experiments, i.e., the resulting confidence scores carry almost no variation and cannot discriminate between correct and incorrect code. The pattern is slightly less severe on Java, where NLI-based clustering occasionally produces 2–3 clusters, consistent with the narrower but still present performance gap observed in the main results.
Functional equivalence clustering produces a substantially broader distribution of cluster counts across all languages. On Python, cluster counts range from 1 to 11 with meaningful mass across the range, particularly for models with lower accuracy (e.g., GPT-4o-mini), where incorrect solutions are more likely to diverge from each other. On SQL, the distribution is similarly broad, with GPT-4o-mini again showing the widest spread. Java shows an intermediate pattern, with functional equivalence clustering producing more variation than NLI but less than Python or SQL, consistent with the moderate AUROC gains observed for Java in the main text.
These distributions confirm that the performance gap between NLI-based and functional equivalence methods is driven by the inability of NLI models to form meaningful clusters from code, rather than by differences in the summary statistics (entropy, sets confidence) applied to those clusters.
Figure 2:
Distribution of cluster counts for NLI-based clustering (red) and functional equivalence clustering (blue) across all models and languages. NLI-based clustering collapses nearly all responses into a single cluster, while functional equivalence clustering produces meaningful variation. Each subplot shows the relative frequency of cluster counts across all prompts for a given model-language combination, with
m
=
10
m=10
sampled responses per prompt (yielding a maximum of 11 clusters).
Appendix D
Execution-Based Validation of Equivalence Judgments
The functional equivalence methods rely on an LLM to judge whether two code snippets are functionally equivalent. To validate the accuracy of these judgments, we compare LLM-assessed equivalence clusters against execution-based outcomes using Gemini-2.5-Flash as the equivalence judge, consistent with the main experiments. Specifically, we check whether responses assigned to the same cluster produce the same results when executed. For Python, we compare actual outputs on test inputs, requiring all cluster members to produce identical results.
5
5
5
We omit Java from this validation as it uses the same equivalence prompt as Python and the same judge model.
For SQL, we compare pass/fail outcomes against the reference solution, which is a weaker check since two queries can both fail for different reasons. Importantly, we note that this validation can detect false equivalence (the judge incorrectly merges functionally different code into the same cluster) but cannot detect false non-equivalence (the judge incorrectly splits equivalent code into separate clusters), since agreement on a finite set of test inputs does not guarantee equivalence on all possible inputs.
We define
cluster purity
as the proportion of multi-element clusters in which all members produce the same execution results: identical outputs on test inputs for Python, and the same pass/fail outcome for SQL.
6
6
6
The SQL validation uses pass/fail agreement rather than output comparison because LiveSQLBench’s evaluation framework returns only binary correctness against the reference solution; comparing full result sets across sampled queries would have required substantial modifications to the evaluation pipeline. We note that this is a weaker check, since two queries can both fail for different reasons.
Cluster purity is analogous to precision: high purity confirms that the judge rarely merges functionally different code into the same cluster (low false equivalence), but does not measure whether equivalent code is incorrectly split into separate clusters (false non-equivalence). We additionally report
response purity
, the proportion of responses in multi-element clusters that belong to pure clusters, which accounts for variation in cluster size. We evaluate on the highest-accuracy and lowest-accuracy models for each benchmark to bound the analysis across the capability range. For Python, we restrict the analysis to the 444 LeetCode callable-style problems where output comparison is feasible, and exclude instances containing any runtime errors (8 for Gemini-2.5-Pro, 29 for GPT-4o-mini).
7
7
7
When including clusters with runtime errors and treating matching error types as equivalent, cluster purity drops slightly: 94.7% (Gemini-2.5-Pro) and 93.5% (GPT-4o-mini). We report the error-excluded results as the primary metric since runtime errors do not produce meaningful outputs for comparison.
Table
14
summarizes the full results.
Python (LiveCodeBench).
On Gemini-2.5-Pro (highest accuracy), 96.1% of 560 multi-element clusters are pure. On GPT-4o-mini (lowest accuracy), 96.1% of 616 multi-element clusters are pure. The consistency across models of different capability levels suggests that the equivalence judge performs reliably regardless of the quality of code being assessed.
SQL (LiveSQLBench).
On Gemini-2.5-Pro (highest accuracy), 96.7% of 487 multi-element clusters are pure. On GPT-4o-mini (lowest accuracy), 93.1% of 303 multi-element clusters are pure. The slightly lower purity on GPT-4o-mini likely reflects the greater diversity of incorrect queries generated by the lower-accuracy model.
Cluster-level
Response-level
Benchmark
Model
Clusters
Purity
Responses
Purity
Python
Gem-2.5-Pro
560
96.1%
4,586
97.1%
GPT-4o-mini
616
96.1%
3,396
97.2%
SQL
Gem-2.5-Pro
487
96.7%
1,731
96.7%
GPT-4o-mini
303
93.1%
1,032
92.2%
Table 14:
Cluster purity of LLM-based equivalence judgments validated against execution. Cluster-level purity is the proportion of multi-element clusters where all members produce the same execution results. Response-level purity is the proportion of responses in multi-element clusters that belong to pure clusters.
Summary.
Across both benchmarks and all four model evaluations, cluster purity exceeds 93%, indicating that the LLM equivalence judge rarely merges functionally different code into the same cluster. The validation is one-directional: high purity confirms low false equivalence rates, but does not measure false non-equivalence, since agreement on finite test inputs does not guarantee equivalence on all possible inputs. Nonetheless, false equivalence is the more consequential error for uncertainty quantification, as it would inflate confidence scores for incorrect code.
Appendix E
Computational Cost Analysis
Method Family
Generations (Orig. LLM)
Equiv. Judge Calls
Logprobs
Token-probability
1
0
Yes
Reflexive
1 + 1
†
0
P(True): Yes; VC: No
Similarity-based
m
+
1
m+1
0
No
Functional equivalence
m
+
1
m+1
FER:
m
m
; Clustering: up to
(
m
+
1
2
)
\binom{m+1}{2}
No
Table 15:
Computational cost by method family.
Generations (Orig. LLM)
denotes calls to the original language model.
Equiv. Judge Calls
denotes calls to the equivalence judge model.
Logprobs
indicates whether access to token-level log-probabilities is required.
†
Reflexive methods use one additional call to the original LLM for self-evaluation, not the equivalence judge.
We summarize the computational requirements of each method family in terms of calls to the original LLM, calls to the equivalence judge, and whether access to log-probabilities is required.
Token-probability methods are the cheapest, requiring only a single greedy generation with log-probabilities enabled. Reflexive methods add one self-evaluation call to the original LLM. P(True) extracts the token probability assigned to “True,” while verbalized confidence prompts the model to express its confidence on a Likert scale. Neither requires an equivalence judge. Similarity-based methods (cosine similarity, CodeBLEU) require
m
+
1
m+1
generations but no additional LLM calls, as similarity computation is handled locally by the embedding model or CodeBLEU.
Functional equivalence methods require
m
+
1
m+1
generations from the original LLM plus additional calls to the equivalence judge. Specifically, functional equivalence rate requires
m
m
pairwise comparisons between the original response and each sample, while the clustering-based methods (functional entropy, functional sets confidence) require up to
(
m
+
1
2
)
\binom{m+1}{2}
pairwise comparisons among all sampled responses. In practice, the clustering algorithm terminates early once cluster assignments are determined, so the number of comparisons is typically well below the
(
m
+
1
2
)
\binom{m+1}{2}
upper bound. All equivalence calls are independent, and our implementation executes them as asynchronous LLM calls, so wall-clock latency scales less than linearly with the number of comparisons.
Cost structure of equivalence assessment.
Each equivalence call consists of the prompt template (Appendix
G
) plus two code snippets, with the judge returning a single classification label (“Equivalent” or “Not Equivalent”). Output token costs are therefore negligible, and the cost of equivalence assessment is dominated by input tokens, which scale with the length of generated solutions and vary by benchmark. At
m
=
5
m=5
(the practical recommendation from Appendix
F
), functional equivalence rate requires 5 judge calls per prompt, while clustering-based methods require up to 15. At
m
=
10
m=10
, these increase to 10 and up to 55, respectively. In both cases, individual equivalence calls are substantially cheaper than generation calls, since they produce only the predicted class rather than a full code response.
Dollar cost analysis.
To ground the above complexity analysis in concrete terms, we report the average per-prompt dollar cost of generation and equivalence scoring across all model–language combinations using Gemini-2.5-Flash as the equivalence judge ($0.30 per 1M input tokens, $2.50 per 1M output tokens). Table
16
reports three cost components: (1) the generation cost for a single response from the primary LLM, (2) the sampled generation cost for
m
=
10
m=10
additional responses from the primary LLM, and (3) the equivalence scoring cost. The scoring cost column reports a range corresponding to the best case (
m
m
judge calls, when all samples are assigned to one cluster via early transitivity) and the worst case (
(
m
+
1
2
)
\binom{m+1}{2}
pairwise calls, when all samples are in separate clusters).
Across all settings, equivalence scoring costs are modest and generally comparable to or smaller than the sampled generation cost. For example, for GPT-4o on Python, sampled generation costs $0.036 per prompt while scoring adds $0.002–$0.010. The most expensive generation configuration is GPT-4o on SQL ($0.406 per prompt for sampled generation), where scoring adds only $0.003–$0.016. This indicates that for practitioners already committing to multi-sample generation for sampling-based UQ, the marginal cost of functional equivalence scoring is reasonable relative to the generation cost that all sampling-based methods share.
Lang.
Model
Generation
Sampled Gen.
Scoring Cost
($)
($)
($ Lower–Upper)
Java
25-flash
4.7e-04
0.004
0.002–0.008
25-flash-lite
6.9e-05
5.0e-04
0.001–0.007
25-pro
0.001
0.010
0.001–0.006
4o
9.9e-04
0.009
0.001–0.006
4o-mini
5.9e-05
5.7e-04
0.001–0.006
Python
25-flash
0.002
0.017
0.004–0.025
25-flash-lite
0.001
0.005
0.009–0.050
25-pro
0.009
0.073
0.005–0.025
4o
0.004
0.036
0.002–0.010
4o-mini
1.9e-04
0.002
0.002–0.009
SQL
25-flash
0.006
0.054
0.003–0.017
25-flash-lite
0.002
0.016
0.003–0.017
25-pro
0.026
0.257
0.003–0.016
4o
0.041
0.406
0.003–0.016
4o-mini
0.002
0.024
0.002–0.013
Table 16:
Average dollar cost per prompt ($USD) for generation and equivalence scoring by language and model, using Gemini-2.5-Flash as the equivalence judge.
Generation
is the cost of a single original response.
Sampled Generation
is the cost of
m
=
10
m{=}10
additional sampled responses.
Scoring
reports the range from best-case (
m
m
judge calls) to worst-case (
(
m
+
1
2
)
\binom{m+1}{2}
judge calls).
Appendix F
Ablations
F.1
Number of Sampled Responses
We evaluate the sensitivity of sampling-based methods to the number of sampled responses
m
∈
{
1
,
…
,
10
}
m\in\{1,\ldots,10\}
. Figures
3
,
4
, and
5
present results for Python, Java, and SQL, respectively.
Across all three languages, AUROC increases with
m
m
but exhibits diminishing returns. On Python, functional equivalence methods improve steeply from
m
=
1
m=1
to
m
=
4
m=4
, after which gains flatten considerably. By
m
=
5
m=5
, most models achieve within 0.01–0.02 AUROC of their
m
=
10
m=10
performance. Functional entropy and functional sets confidence follow nearly identical trajectories, consistent with both methods relying on the same underlying cluster structure. Equivalence rate shows a similar pattern but starts slightly higher at low
m
m
, as it does not require multiple clusters to produce a useful signal. Cosine similarity is notably less sensitive to
m
m
, with performance plateauing by
m
=
3
m=3
on most models, likely because pairwise similarity scores are informative even with few samples.
On Java, the diminishing returns pattern holds but with two notable differences. First, CodeBLEU consistency is competitive with or exceeds functional equivalence methods at all values of
m
m
, particularly on Gemini-2.5-Flash where it achieves the highest AUROC throughout. This contrasts with Python and SQL, where functional equivalence methods dominate at higher
m
m
. Second, equivalence rate lags behind functional entropy and functional sets confidence more substantially than on other languages, suggesting that the binary equivalence signal is less informative for Java code where functional differences may be more subtle. Cosine similarity again plateaus early but at a lower level than on Python.
On SQL, the overall pattern is similar but with more variance at low
m
m
, reflecting the smaller benchmark size (270 problems). Functional entropy and functional sets confidence again show the steepest improvement, with most gains realized by
m
=
5
m=5
–
6
6
. Cosine similarity observes generally smaller gains from additional samples relative to Python and Java. Equivalence rate improves more gradually on SQL and does not fully converge by
m
=
10
m=10
for some models (e.g., GPT-4o-mini), indicating that pairwise equivalence judgments for SQL may benefit from larger sample sizes.
Overall, these results suggest that
m
=
5
m=5
offers a practical balance between performance and computational cost for most settings.
Figure 3:
AUROC as a function of the number of sampled responses
m
m
on LiveCodeBench (Python). Performance increases with
m
m
but exhibits diminishing returns, with most gains realized by
m
=
5
m=5
.
Figure 4:
AUROC as a function of the number of sampled responses
m
m
on MultiPL-E (Java). Performance increases with
m
m
but exhibits diminishing returns, with most gains realized by
m
=
5
m=5
.
Figure 5:
AUROC as a function of the number of sampled responses
m
m
on LiveSQLBench (SQL). The pattern is similar to Python, with more variance at low
m
m
due to the smaller benchmark size.
F.2
Sensitivity to Equivalence Judge
The functional equivalence methods introduced in Section
3.2
rely on an LLM to assess pairwise functional equivalence between code responses. All main experiments use Gemini-2.5-Flash as the equivalence judge. To evaluate how sensitive the methods are to judge choice, we replace the judge with two alternatives: Gemini-2.5-Flash-Lite, a smaller model from the same provider, and GPT-4o-mini, a model from a different provider (OpenAI). Following Appendix
D
, we evaluate on Python (LiveCodeBench) and SQL (LiveSQLBench) using the highest- and lowest-accuracy generators for each benchmark: Gemini-2.5-Pro and GPT-4o-mini.
Table
17
presents AUROC results for the three functional equivalence scorers across all three judges, with the Gemini-2.5-Flash results from the main experiments included for reference.
Original LLM
Scorer
Gem-Fl.
Gem-Fl.-Lt
GPT4o-m
Python (LiveCodeBench)
Gem-Pro
Func. Entropy
0.829
0.834
0.829
Func. Sets
0.826
0.836
0.831
Equiv. Rate
0.826
0.829
0.814
GPT4o-m
Func. Entropy
0.859
0.852
0.836
Func. Sets
0.859
0.855
0.837
Equiv. Rate
0.856
0.842
0.824
SQL (LiveSQLBench)
Gem-Pro
Func. Entropy
0.745
0.752
0.711
Func. Sets
0.750
0.752
0.714
Equiv. Rate
0.702
0.700
0.637
GPT4o-m
Func. Entropy
0.840
0.828
0.825
Func. Sets
0.842
0.828
0.826
Equiv. Rate
0.782
0.791
0.756
Table 17:
AUROC of functional equivalence methods across three equivalence judges. Gem-Fl. denotes the primary judge (Gemini-2.5-Flash) used in all main experiments. Gemini-2.5-Flash-Lite and GPT-4o-mini are alternative judges of varying capability.
Gemini-2.5-Flash-Lite produces AUROC scores within 0.01 of the primary judge in most configurations, and in some cases marginally exceeds it (e.g., functional entropy on Python with Gemini-2.5-Pro responses: 0.834 vs. 0.829). This suggests that the functional equivalence approach is not sensitive to moderate reductions in judge capability within the same model family.
GPT-4o-mini shows more notable degradation as a judge. On Python, functional entropy shows no degradation on Gemini-2.5-Pro responses but drops by 0.023 on GPT-4o-mini responses relative to the primary judge. On SQL, the drop is larger: 0.034 on Gemini-2.5-Pro responses and 0.015 on GPT-4o-mini responses. Equivalence rate is the most affected scorer, dropping by 0.065 on SQL with Gemini-2.5-Pro responses, likely because it relies on individual pairwise judgments without the smoothing effect of cluster-level aggregation. Functional entropy and functional sets confidence degrade more gracefully, consistent with their reliance on distributional properties of the full cluster structure rather than individual binary comparisons.
Despite the degradation with GPT-4o-mini, functional equivalence methods remain competitive with or exceed the strongest baselines in most configurations, indicating that the approach provides value even with a weaker judge. These results suggest that judge capability affects absolute performance but does not alter the overall conclusion that LLM-based functional equivalence assessment improves upon both NLI-based and token-probability methods for code correctness prediction.
F.3
Sensitivity to Sampled Response Ordering
The greedy clustering procedure used by Functional Sets Confidence and Functional Negentropy is order-dependent: the sequence in which responses are compared can affect cluster assignments. To assess the impact of this ordering sensitivity on downstream UQ metrics, we conduct a permutation analysis. For both Python (LiveCodeBench) and SQL (LiveSQLBench), we sample 100 problems for both the strongest model (Gemini-2.5-Pro) and weakest model (GPT-4o-mini), and recompute all three functional equivalence scorers 10 times with random permutations of the
m
=
10
m=10
sampled responses. We note that Functional Equivalence Rate is permutation-invariant by construction, as it aggregates all pairwise judgments without clustering. Any variation observed for this scorer therefore reflects LLM judge stochasticity rather than ordering effects.
Table
18
summarizes the results. Across all 12 scorer–dataset–model combinations, AUROC ranges are narrow, and pairwise Pearson correlations between runs exceed 0.82 in all settings and 0.94 in 10 of 12 settings. ECE variation is similarly small. We note that this analysis uses subsamples of 100 problems, and metric variability is expected to decrease on the full dataset due to standard sampling effects.
Scorer
Setting
AUROC Range
ECE Range
Min
r
r
Func. Sets
SQL / Gem-2.5-Pro
0.71–0.75
0.09–0.13
0.95
SQL / 4o-mini
0.80–0.83
0.12–0.17
0.96
Py / Gem-2.5-Pro
0.87–0.94
0.02–0.06
0.83
Py / 4o-mini
0.86–0.88
0.07–0.11
0.98
Func. Entr.
SQL / Gem-2.5-Pro
0.71–0.74
0.15–0.18
0.95
SQL / 4o-mini
0.80–0.83
0.08–0.14
0.96
Py / Gem-2.5-Pro
0.89–0.94
0.05–0.07
0.88
Py / 4o-mini
0.87–0.89
0.04–0.08
0.98
Func. Equiv.
SQL / Gem-2.5-Pro
0.64–0.69
0.24–0.27
0.94
SQL / 4o-mini
0.74–0.80
0.08–0.14
0.96
Py / Gem-2.5-Pro
0.94–0.96
0.09–0.11
0.91
Py / 4o-mini
0.89–0.91
0.10–0.13
0.98
Table 18:
Ordering sensitivity of functional equivalence scorers. For each setting, we report the AUROC and ECE range (min–max) across 10 reshuffled runs and the minimum pairwise Pearson correlation between runs.
Appendix G
Prompt Templates
The complete equivalence prompts used in our Python and Java experiments is presented in Table
19
, while the prompt for SQL experiments is presented in Table
20
.
Python/Java Code Equivalence
You are a [LANGUAGE] code equivalence judge.
Definition:
Two [LANGUAGE] code blocks are considered functionally equivalent if they would produce the same outputs for the same inputs.
Consider equivalent:
- Different implementations or algorithms that achieve the same result
- Refactored or restructured code with the same behavior
- Minor variations in edge case handling
Consider NOT equivalent:
- Code that would produce different outputs for the same inputs
- Code where one is incomplete or missing functionality present in the other
Decision rule:
- If both code snippets would generally produce the same results → output exactly: "Equivalent"
- If the code snippets would produce different outputs → output exactly: "Not Equivalent"
Output format:
Output EXACTLY one of: "Equivalent" OR "Not Equivalent".
Do not add explanations, reasoning, punctuation, or extra text.
Table 19:
Prompt for Python/Java Code Equivalence.
SQL Equivalence
You are a SQLite query equivalence judge.
Definition:
Two SQLite queries are considered semantically equivalent only if, when executed against the same database state, they produce exactly the same result set.
Same result set means:
- The same rows (treating rows as unordered sets, unless ORDER BY is specified in both queries)
- The same column values in each row
- The same column order
Ignore:
- Purely syntactic differences (formatting, whitespace, capitalization of keywords)
- Use of aliases that do not affect the result set
- Equivalent expressions (e.g., ‘WHERE a = 1 AND b = 2‘ vs. ‘WHERE b = 2 AND a = 1‘)
- Different join syntax with equivalent semantics (e.g., implicit vs. explicit JOIN)
- Use of parentheses that do not change query semantics
- Comments
Do NOT ignore:
- Different row ordering if either query specifies ORDER BY
- NULL handling differences that affect results
- DISTINCT vs. non-DISTINCT if it changes output rows
- Column order differences in the SELECT clause
Decision rule:
- If both queries would return the same result set on any valid database state → output exactly: "Equivalent"
- If any valid database state exists where the queries would return different results → output exactly: "Not Equivalent"
Output format:
Output EXACTLY one of: "Equivalent" OR "Not Equivalent".
Do not add explanations, reasoning, punctuation, or extra text.
Table 20:
Prompt for SQLite Equivalence.