---
title: Showing LLM-Generated Code Selectively Based on Confidence of LLMs
id: showing-llm-generated-code-selectively-based-on-confidence-of-llms
tags:
- code-llm-confidence-positioning-d82d00
- w3-forward-citation
created: '2026-11-10T08:23:57.528870Z'
updated: '2026-11-10T08:25:33.189396Z'
source: https://arxiv.org/html/2410.03234
source_domain: arxiv.org
fetched_at: '2026-11-10T08:23:57.528373Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'HonestCoder (2024): confidence from multi-modal similarity between sampled
  programs; releases TruthCodeBench (2,265 Python and Java samples), four instruct
  code LLMs (DeepSeek-Coder-Instruct 1.3B and 6.7B, Code Llama-Instruct 13B and 7B),
  +27.79% AUROC and +63.74% AUCPR over best baseline, eight baselines. Sampled-consistency
  readout only; no probe, no verbal. Prior work for L1 (code confidence vs test labels)
  and selective showing (L3-adjacent).'
---

Showing LLM-Generated Code Selectively Based on Confidence of LLMs
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2410.03234v1 [cs.SE] 04 Oct 2024
Showing LLM-Generated Code Selectively Based on Confidence of LLMs
DOI:
XXXXXXX.XXXXXXX
Conference:
Make sure to enter the correct
conference title from your rights confirmation emai; June 03–05,
2018; Woodstock, NY
ISBN:
978-1-4503-XXXX-X/18/06
CCS:
Computing methodologies Neural networks
CCS:
Software and its engineering Automatic programming
Jia Li
♂
\male
email:
lijia@stu.pku.edu.cn
Affiliation:
School of Computer Science, Peking University
,
Beijing
,
China
,
Yuqi Zhu
email:
lijia@stu.pku.edu.cn
Affiliation:
Academy of Military Sciences
,
Beijing
,
China
,
Yongmin Li
email:
liyongmin@pku.edu.cn
Affiliation:
School of Computer Science, Peking University
,
Beijing
,
China
,
Ge Li
email:
lige@pku.edu.cn
Affiliation:
School of Computer Science, Peking University
,
Beijing
,
China
and
Zhi Jin
email:
zhijin@pku.edu.cn
Affiliation:
School of Computer Science, Peking University
,
Beijing
,
China
Received  5 June 2009
Abstract.
Large Language Models (LLMs) have shown impressive abilities in code generation, but they may generate erroneous programs. Reading a program takes ten times longer than writing it
(
Martin, 2009
)
. Showing these erroneous programs to developers will waste developers’ energies and introduce security risks to software.
To address the above limitations, we propose
HonestCoder
, a novel LLM-based code generation approach.
HonestCoder
selectively shows the generated programs to developers based on LLMs’ confidence. The confidence provides valuable insights into the correctness of generated programs. To achieve this goal, we propose a novel approach to estimate LLMs’ confidence in code generation. It estimates confidence by measuring the multi-modal similarity between LLMs-generated programs.
We collect and release a multilingual benchmark named
TruthCodeBench
, which consists of 2,265 samples and covers two popular programming languages (
i.e.,
Python and Java). We apply
HonestCoder
to four popular LLMs (
e.g.,
DeepSeek-Coder and Code Llama) and evaluate it on
TruthCodeBench
. Based on the experiments, we obtain the following insights.
❶
HonestCoder
can effectively estimate LLMs’ confidence and accurately determine the correctness of generated programs. For example,
HonestCoder
outperforms the state-of-the-art baseline by 27.79% in AUROC and 63.74% in AUCPR.
❷
HonestCoder
can decrease the number of erroneous programs shown to developers. Compared to eight baselines, it can show more correct programs and fewer erroneous programs to developers.
❸ Compared to showing code indiscriminately,
HonestCoder
only adds slight time overhead (approximately 0.4 seconds per requirement).
❹ We discuss future directions to facilitate the application of LLMs in software development. We hope this work can motivate broad discussions about measuring the reliability of LLMs’ outputs in performing code-related tasks.
Keywords:
Code Generation, Large Language Models
1.
Introduction
Large Language Models (LLMs)
(
OpenAI, 2024
;
Guo et al., 2024
;
Rozière et al., 2023
)
have been widely used in code generation. For example, GitHub Copilot
(
GitHub, 2023
)
, an LLM-based code generation tool, is regularly utilized by developers from over 10,000 organizations
(
Scheffler, 2023
)
. However, LLMs may produce erroneous programs
(
Wang et al., 2024
;
Dou et al., 2024
)
. Showing these erroneous programs to developers leads to two negative consequences. ❶
Wasting developers’ energies.
Reading a program takes ten times longer than writing it
(
Martin, 2009
)
. Developers waste more time reading and testing erroneous programs than writing them. ❷
Introducing the security risks.
LLM-generated erroneous programs have unexpected behaviors and may crash on unknown inputs. Extensive LLM-generated erroneous programs remain a widespread and growing risk to the software infrastructure.
Figure 1.
The comparison of (a) previous LLM-based code generation approaches and (b) our
HonestCoder
. Previous approaches indiscriminately show developers the generated code, including the erroneous code. In contrast,
HonestCoder
selectively shows the generated code based on LLMs’ confidence. When LLMs are uncertain,
HonestCoder
outputs “
I can not solve this requirement
”.
To address the above limitations, we propose
HonestCoder
, a novel LLM-based code generation approach.
Our motivation is that a critical aspect of human intelligence is to express confidence in a problem
(
Cosmides and Tooby, 1996
)
. The confidence provides valuable insights into the reliability of responses. Inspired by this observation,
HonestCoder
aims to estimate LLMs’ confidence and selectively show the LLM-generated code based on the confidence. The higher the confidence, the greater the probability that LLMs will generate the correct code for requirements.
Figure
1
compares previous code generation approaches and
HonestCoder
. Previous approaches
(
Guo et al., 2024
;
Li et al., 2024b
;
Li et al., 2024a
)
indiscriminately show developers LLM-generated programs, including erroneous programs. In contrast,
HonestCoder
only shows the generated programs when LLMs are confident. When LLMs are uncertain, the generated programs probably are erroneous, and
HonestCoder
just outputs “
I can not solve this requirement
”. We think that
HonestCoder
has the following advantages:
•
Improving developers’ productivity.
HonestCoder
builds more efficient human-machine collaborative programming, where LLMs only output trustworthy programs and refuse to answer uncertain requirements. It saves developers’ energy spent in reading and testing LLMs’ erroneous programs. Developers can focus on solving complex requirements and leave other requirements to LLMs.
•
Profound implications.
HonestCoder
reveals the confidence of LLMs in code generation and inspires many promising code generation techniques,
e.g.,
selective retrieval-augmented generation and human-in-the-loop generation.
The idea of
HonestCoder
can also be applied to other code-related tasks (
e.g.,
vulnerability detection
(
Zhou et al., 2019
)
) and motivate broad discussions. In Section
9
, we discuss these implications in detail.
The main challenge in implementing
HonestCoder
is how to estimate the LLMs’ confidence in code generation.
The existing similar work
(
Spiess et al., 2024
)
is initially designed for natural language generation and has shown sub-optimal performance in code generation. Therefore, we propose a new confidence estimation approach. Our motivation is that high confidence typically leads to consistent answers. For example, if humans are confident about a question (
e.g.,
What shape is the Earth?), they are convinced of the answer (
e.g.,
sphere) regardless of how many times they are asked. Otherwise, if uncertain, they might arbitrarily make up disparate answers (
e.g.,
cube, pyramid). A similar phenomenon has been observed in LLMs
(
Zhang et al., 2024a
;
Farquhar et al., 2024
)
. Inspired by this observation, our approach estimates LLMs’ confidence in two steps. First, given a requirement, we independently sample multiple programs from LLMs. These programs represent LLM’s multiple attempts to solve the requirement. Second, we employ a
multi-modal estimator
to comprehensively measure the similarities between programs from multiple modalities (
e.g.,
lexical, syntactic, and semantic levels). The average of code similarities is considered the LLMs’ confidence in the requirement.
To evaluate
HonestCoder
, we collect and release an evaluation benchmark named
TruthCodeBench
.
TruthCodeBench
covers two programming languages (
i.e.,
Python and Java) and consists of 2,265 samples. Each sample comprises a human-written requirement and LLM-specific labels (
i.e.,
passed or failed). The labels indicate whether the specific LLMs can generate the correct programs for requirements. We study four popular LLMs, including DeepSeek-Coder-Instruct
(
Guo et al., 2024
)
(1.3B, 6.7B) and Code Llama-Instruct
(
Rozière et al., 2023
)
(13B, 7B). Detailed information about
TruthCodeBench
is provided in Section
4
. During the evaluation, given a requirement, we use
HonestCoder
to predict whether to show the generated programs. We expect that
HonestCoder
only shows the generation results of passed requirements and refuses failed requirements. Thus, we leverage two evaluation metrics (
i.e.,
AUROC
(
scikit learn, 2024b
)
and AUCPR
(
scikit learn, 2024a
)
) to evaluate the correlation between
HonestCoder
’s predictions and labels. The stronger the correlation, the more valuable the
HonestCoder
’s predictions.
We conduct a large-scale study upon
TruthCodeBench
and yield the following observations.
❶
HonestCoder
can effectively estimate LLMs’ confidence and accurately determine the functional correctness of generated programs. For example,
HonestCoder
outperforms the state-of-the-art baseline by 27.79% in AUROC and 63.74% in AUCPR. ❷
HonestCoder
can decrease the number of erroneous programs shown to developers. Compared to eight baselines, it can show more correct programs and fewer erroneous programs. ❸ We explore the other eight variants of
HonestCoder
and compare them to
HonestCoder
. The results show the superiority
HonestCoder
. ❹ We measure the time efficiency of
HonestCoder
. Compared to showing code indiscriminately,
HonestCoder
adds slight time overhead (approximately 0.4 seconds). ❺ We discuss future directions to facilitate the application of LLMs in software development. We hope this work can motivate broad discussions about measuring the reliability of LLMs’ outputs in performing code-related tasks.
Our contributions are summarized below.
•
We propose a novel code generation approach named
HonestCoder
, which selectively shows LLM-generated programs to developers based on LLMs’ confidence.
•
To implement
HonestCoder
, we propose a new approach to estimating the LLMs’ confidence in code generation. The confidence provides valuable insights into the correctness of the generated programs.
•
We release a multilingual benchmark -
TruthCodeBench
, to evaluate
HonestCoder
and facilitate future research. It comprises 2,265 samples and covers two programming languages and four popular LLMs.
•
We conduct a large-scale study on
TruthCodeBench
and show the effectiveness of
HonestCoder
. We discuss the future directions of our work to facilitate the application of LLMs in software development.
2.
Motivating Examples
In this section, we describe our motivations through some statistics.
Existing LLMs may generate erroneous programs.
We select a popular LLM - DeepSeek Coder-6.7B (abbr. DS-Coder) and evaluate it on two popular benchmarks (
i.e.,
HumanEval
(
Chen et al., 2021
)
and MBPP
(
Austin et al., 2021
)
). DS-Coder generates a program per requirement in benchmarks.
The evaluation results are shown in Figure
1
(a). DS-Coder fails to solve 41% and 34% of requirements in both benchmarks, respectively. The main reason for the failed programs is functional errors.
Figure 2.
(a) The performance of a popular LLM - DeepSeek Coder-6.7B on two popular benchmarks
(
Chen et al., 2021
;
Austin et al., 2021
)
. It may generate programs with errors (
e.g.,
functional errors). (b) The similarity distribution between programs in passed/failed requirements. The programs in passed requirements are more deterministic (
i.e.,
higher similarity) than the ones in failed requirements.
Showing the erroneous programs will waste developers’ energy.
Reading a program takes ten times longer than writing it
(
Martin, 2009
)
. In practice, developers spend more energy reading and testing erroneous programs than writing correct versions.
Besides, many programs are not equipped with testing environments during development. This makes it more difficult to detect these erroneous programs.
To address the above limitation, we propose a novel code generation approach named
HonestCoder
.
HonestCoder
selectively shows LLM-generated programs based on LLMs’ confidence. The confidence indicates the probability that LLMs generate correct programs. To implement
HonestCoder
, we propose a approach to estimating LLMs’ confidence in code generation. Next, we describe the motivation for our confidence estimation approach.
LLMs tend to generate deterministic programs when they are confident of solving the requirements.
Our idea is inspired by an observation that if humans are confident about a question (
e.g.,
In which year was the first public release of Python released?), their answers are deterministic (
e.g.,
1991) despite how many times they are asked. Otherwise, if humans are uncertain, they might make up disparate answers (
e.g.,
1989, 1994). LLMs also show similar behavior on question answering
(
Zhang et al., 2024a
;
Farquhar et al., 2024
)
.
To validate that the above phenomenon also occurs in code generation, we collect the programs generated by DS-Coder in HumanEval and MBPP. DS-Coder generates
N
N
(
N
=
20
N=20
in this paper) programs for each requirement. The temperature for sampling is 1. If at least one of
N
N
programs passes all test cases, this requirement is passed. Otherwise, it is failed. Then, we compute the average similarities between
N
N
programs in passed and failed requirements as follows.
(1)
AvgSim
=
1
N
⁡
(
N
−
1
)
​
∑
i
=
1
N
∑
j
=
1
N
Sim
​
(
c
i
,
c
j
)
i
≠
j
\text{AvgSim}=\frac{1}{N(N-1)}\sum_{i=1}^{N}\sum_{j=1}^{N}\text{Sim}(c_{i},c_{j})\quad i\neq j
where
c
i
c_{i}
and
c
j
c_{j}
are the
i
i
-th and
j
j
-th generated program for a requirement.
Sim
​
(
⋅
)
\text{Sim}(\cdot)
is a similarity metric. Inspired by related studies
(
Lu et al., 2022
;
Ren et al., 2020
)
, we set four similarity metrics: text similarity, syntax similarity, dataflow similarity, and embedding similarity. They measure the similarity between two programs from different modalities (
i.e.,
code sequences, abstract syntax trees, data flows, and embedding vectors). The detailed definitions of these metrics are in Section
3.3
.
The results are shown in Figure
2
(b).
We can see that the code similarities in passed requirements are greater than the ones in failed requirements.
It means that LLMs are prone to generate more deterministic (
i.e.,
more similar) programs when their outputs are correct. Based on this finding, we propose to estimate the confidence of LLMs based on the similarity between generated programs. The higher the code similarity, the greater the confidence of LLMs.
3.
HonestCoder
This section describes the proposed
HonestCoder
. We show an overview of
HonestCoder
and then describe its details.
3.1.
An Overview of
HonestCoder
Figure 3.
An overview of
HonestCoder
. Given a requirement, it samples multiple programs from LLMs (Section
3.2
). Then, it leverages an estimator to estimate the LLMs’ confidence by measuring the multi-modal similarities between sampled programs (Section
3.3
). Finally, it determines whether to show the generated programs based on confidence (Section
3.4
).
HonestCoder
is an LLM-based code generation approach. Unlike previous approaches, given a requirement, it can estimate the LLMs’ confidence in the requirement and selectively show the generated programs to developers. Figure
3
shows an overview of
HonestCoder
. Its pipeline consists of the following three stages:
•
Code Generation (Section
3.2
).
Given a requirement, we leverage an LLM to generate
N
N
(
N
>
1
N>1
) programs. These programs denote multiple attempts by the LLM to solve the requirement.
•
Confidence Estimation (Section
3.3
).
A multi-modal estimator is designed to estimate the confidence of LLMs by measuring the multi-modal similarity between sampled programs. The higher the similarity, the greater the confidence of LLMs.
•
Response Output (Section
3.4
).
Based on the confidence of LLMs, it determines whether to show the generated programs. When the confidence is greater than a threshold, it shows programs. Otherwise, it outputs a refusal.
3.2.
Code Generation
In this stage, we leverage an LLM to generate
N
N
(
N
>
1
N>1
) programs for a requirement. The generated programs denote multiple attempts by the LLM to solve the requirement. Specifically, we employ a popular sampling algorithm - temperature sampling
(
Ackley et al., 1985
)
. The motivations for choosing temperature sampling are two-fold. First, temperature sampling introduces randomness into the decoding process and can sample diverse answers based on LLMs’ logits. It is beneficial to reveal the uncertainty of LLMs
(
Zhang et al., 2024b
;
Farquhar et al., 2024
)
. Second, temperature sampling is a mainstream way to liberate the coding ability of LLMs and has been widely employed in code generation
(
Rozière et al., 2023
;
Guo et al., 2024
;
Zhu et al., 2024a
)
.
We want to clarify that the above sampling aims to facilitate confidence estimation and is invisible to developers. If
HonestCoder
finally determines that LLMs are uncertain, these sampled programs will not be shown to developers. Besides, sampling can be parallelized, so it does not add extra time overheads. We measure the time efficiency of
HonestCoder
in Section
7.1
and tune the default sampling size
N
N
to 20.
3.3.
Confidence Estimation
Algorithm 1
The workflow of our estimator.
1:
Input:
A set of sampled programs
𝐂
\mathbf{C}
2:
Output:
A confidence score
3:
N
←
Len
⁡
(
𝐂
)
N\leftarrow\operatorname{Len}(\mathbf{C})
//
Len
⁡
(
)
\operatorname{Len}()
is a function returning the number of elements in a list
4:
S
​
i
​
m
​
_
​
l
​
i
​
s
​
t
←
[
]
Sim\_list\leftarrow[]
5:
for
i
=
1
i=1
to
N
N
do
6:
for
j
=
1
j=1
to
N
N
do
7:
if
i
≠
j
i\neq j
then
8:
c
i
←
𝐂
⁡
[
i
]
c_{i}\leftarrow\mathbf{C}[i]
,
c
j
←
𝐂
⁡
[
j
]
c_{j}\leftarrow\mathbf{C}[j]
9:
Compute
Sim
​
(
c
i
,
c
j
)
\text{Sim}(c_{i},c_{j})
Using Equation
2
10:
Append
Sim
​
(
c
i
,
c
j
)
\text{Sim}(c_{i},c_{j})
to
S
​
i
​
m
​
_
​
l
​
i
​
s
​
t
Sim\_list
11:
end
if
12:
end
for
13:
end
for
14:
C
​
o
​
n
​
f
​
i
​
d
​
e
​
n
​
c
​
e
←
SUM
⁡
(
S
​
i
​
m
​
_
​
l
​
i
​
s
​
t
)
/
Len
⁡
(
S
​
i
​
m
​
_
​
l
​
i
​
s
​
t
)
Confidence\leftarrow\operatorname{SUM}(Sim\_list)/\operatorname{Len}(Sim\_list)
15:
return
C
​
o
​
n
​
f
​
i
​
d
​
e
​
n
​
c
​
e
Confidence
This stage aims to estimate the LLMs’ confidence in code generation. The confidence reflects the probability that LLMs can generate the correct programs for the requirement. As discussed in Section
2
, LLMs tend to generate deterministic programs when they are confident. Conversely, the generated programs typically are disparate when LLMs are uncertain. Thus, our estimator estimates LLMs’ confidence by measuring the similarity between sampled programs.
The key challenge in implementing the estimator is to accurately measure the similarity between programs. We think that a good estimator should satisfy two principles:
•
Comprehensive.
The similarity between programs is often reflected at different levels,
e.g.,
text surfaces, syntactic structures and semantic embeddings. Thus, our estimator should measure the code similarity in a comprehensive view. A narrow perspective may result in false results.
•
General.
LLMs are emerging and employed to generate programs across various domains. Therefore, our estimator should be generalizable across domains and easily applicable to different LLMs.
However, no existing studies fulfill both principles. Traditional code similarity metrics (
e.g.,
BLEU
(
Papineni et al., 2002
)
and CodeBLEU
(
Ren et al., 2020
)
) fall into narrow perspectives (
e.g.,
text surfaces or syntactic structures) and struggle to provide comprehensive measurements. Deep learning-based approaches are typically task-specific (
e.g.,
code clone detection
(
Li et al., 2023b
)
) and lack generalization.
To satisfy the above principles, we propose a multi-modal estimator. It comprehensively measures the code similarity from multiple modalities and can generalize to various LLMs. Algorithm
1
shows the workflow of our estimator. Specifically, it parses the code into four mainstream modalities: token sequences, concrete syntax trees, data flows, and semantic embeddings. Then, it computes a weighted sum of similarities in different modalities:
(2)
Sim
​
(
c
i
,
c
j
)
=
\displaystyle\text{Sim}(c_{i},c_{j})=
α
×
Sim
text
​
(
c
i
,
c
j
)
+
β
×
Sim
syntax
​
(
c
i
,
c
j
)
+
\displaystyle\alpha\times\text{Sim}_{\text{text}}(c_{i},c_{j})+\beta\times\text{Sim}_{\text{syntax}}(c_{i},c_{j})+
γ
×
Sim
df
​
(
c
i
,
c
j
)
+
δ
×
Sim
embed
​
(
c
i
,
c
j
)
\displaystyle\gamma\times\text{Sim}_{\text{df}}(c_{i},c_{j})+\delta\times\text{Sim}_{\text{embed}}(c_{i},c_{j})
where
c
i
c_{i}
and
c
j
c_{j}
are two generated programs.
Sim
text
\text{Sim}_{\text{text}}
,
Sim
syntax
\text{Sim}_{\text{syntax}}
,
Sim
df
\text{Sim}_{\text{df}}
, and
Sim
embed
\text{Sim}_{\text{embed}}
denote the similarities in four modalities, respectively.
α
\alpha
,
β
\beta
,
γ
\gamma
, and
δ
\delta
are hyper-parameters and within the range
[
0
,
1
]
[0,1]
. We tune these hyper-parameters on the training data and release them in our replication package
(
Anonymous, 2024
)
.
The LLMs’ confidence in a requirement is computed as the average of the pairwise similarity scores between the generated programs. We describe how to compute similarities in different modalities as follows.
Text Similarity.
Programs with similar functionalities often have similar text surfaces. Researchers have proposed many successful metrics to measure the text similarity between programs
(
Papineni et al., 2002
;
Eghbali and Pradel, 2022
)
. Following existing studies
(
Papineni et al., 2002
)
, we split programs into token sequences and compute the
n
n
-gram similarity between two code sequences. Specifically,
(3)
Sim
text
​
(
c
i
,
c
j
)
=
exp
⁡
(
∑
n
=
1
4
1
4
​
log
⁡
s
i
​
j
n
s
j
n
)
\text{Sim}_{\text{text}}(c_{i},c_{j})=\exp\left(\sum_{n=1}^{4}\frac{1}{4}\log\frac{s^{n}_{ij}}{s^{n}_{j}}\right)
where the maximum of
n
n
is empirically set to 4.
s
i
​
j
n
s^{n}_{ij}
is the number of overlapping
n
n
-grams between
c
i
c_{i}
and
c
j
c_{j}
.
s
j
n
s^{n}_{j}
means the number of
n
n
-grams in
c
j
c_{j}
.
Syntactic Similarity.
The code is structured and can be parsed into tree structures,
e.g.,
Concrete Syntax Trees (CSTs). Programs with different text surfaces may have similar syntactic structures. Following the related work
(
Ren et al., 2020
)
, we calculate the similarity in syntactic structures. Specifically, we parse the programs into CSTs and extract sub-trees from CSTs. Then, we compute the ratio of overlapping sub-trees between two programs. Formally,
(4)
Sim
syntax
​
(
c
i
,
c
j
)
=
|
CST
​
(
c
i
)
∩
CST
​
(
c
j
)
|
|
CST
​
(
c
j
)
|
\text{Sim}_{\text{syntax}}(c_{i},c_{j})=\frac{|\text{CST}(c_{i})\cap\text{CST}(c_{j})|}{|\text{CST}(c_{j})|}
where
CST
​
(
⋅
)
\text{CST}(\cdot)
is a function for extracting all CST sub-trees of a program.
Data Flow Similarity.
The code is executable and contains rich data flow information. Data flows reflect the dependencies between variables and can represent the code’s functionality
(
Guo et al., 2021
)
. Inspired by related works
(
Guo et al., 2021
;
Ren et al., 2020
)
, we first extract the data-flow graphs from programs. Each node (
e.g.,
v
i
,
v
j
v_{i},v_{j}
) in the data-flow graphs denotes a variable. The directed edge
e
=
⟨
v
i
,
v
j
⟩
e=\langle v_{i},v_{j}\rangle
from
v
i
v_{i}
to
v
j
v_{j}
refers that the value of
v
j
v_{j}
comes from
v
i
v_{i}
. Then, we compute the ratio of overlapping data-flow edges between two programs. Specifically,
(5)
Sim
df
​
(
c
i
,
c
j
)
=
|
DFG
edge
​
(
c
i
)
∩
DFG
edge
​
(
c
j
)
|
|
DFG
edge
​
(
c
j
)
|
\text{Sim}_{\text{df}}(c_{i},c_{j})=\frac{|\text{DFG}_{\text{edge}}(c_{i})\cap\text{DFG}_{\text{edge}}(c_{j})|}{|\text{DFG}_{\text{edge}}(c_{j})|}
where
DFG
​
(
⋅
)
\text{DFG}(\cdot)
is a function for extracting all data flow edges of a program.
Semantic Embedding Similarity.
LLMs have shown impressive abilities in code representation
(
Nam et al., 2024
)
. Thus, we can leverage LLMs to represent a program with a semantic embedding (
i.e.,
a high-dimension vector). Then, we compute the cosine similarity between embeddings as follows:
(6)
𝐞
i
=
M
​
(
c
i
)
,
𝐞
j
=
M
​
(
c
j
)
Sim
embed
​
(
c
i
,
c
j
)
=
𝐞
i
⋅
𝐞
j
‖
𝐞
i
‖
​
‖
𝐞
j
‖
\begin{gathered}\mathbf{e}_{i}=\text{M}(c_{i}),\mathbf{e}_{j}=\text{M}(c_{j})\\
\text{Sim}_{\text{embed}}(c_{i},c_{j})=\frac{\mathbf{e}_{i}\cdot\mathbf{e}_{j}}{\|\mathbf{e}_{i}\|\|\mathbf{e}_{j}\|}\end{gathered}
M
denotes an LLM used for encoding programs.
𝐞
i
\mathbf{e}_{i}
and
𝐞
j
\mathbf{e}_{j}
denote the semantic embeddings of
c
i
c_{i}
and
c
j
c_{j}
, respectively.
Specifically, we leverage a powerful LLM (
e.g.,
DeepSeek Coder-6.7B-base
(
Guo et al., 2024
)
) as
M
and pick the last token’s hidden state in the last layer as the embedding. Our motivations are two-fold. First, because LLMs are autoregressive, only the last code token’s hidden state is computed based on the whole code. Thus, it can represent the comprehensive semantics of the code. Second, the shallow layers of LLMs mainly capture the lexical information of programs, while the deep layer focuses on the semantic information of programs
(
Wan et al., 2022
)
. Thus, we select the hidden states in the last layer.
Our estimator provides a
comprehensive
measurement of code similarity and is
general
for different LLMs and programs. In Section
6.3
, we compare our estimator to eight other variants (
e.g.,
BLEU-based, CodeBLEU-based) and validate the superiority of our estimator.
3.4.
Response Output
In this stage, we determine whether to show the generated programs to developers based on LLMs’ confidence. Specifically, if the LLMs’ confidence is greater than a threshold
T
T
,
HonestCoder
shows the sampled programs in the first stage to developers. Otherwise,
HonestCoder
outputs a refusal. For example,
HonestCoder
will output a special response -
Sorry, I cannot solve this requirement.
In the future, researchers can design more advanced generation techniques when LLMs are uncertain,
e.g.,
human-in-the-loop generation and retrieval-augmented generation.
Because this paper is an early step in discussing selective code generation, we leave this exploration in future work.
In practice, practitioners can control the aggressiveness of
HonestCoder
by adjusting the threshold
T
T
. A larger
T
T
makes
HonestCoder
more conservative, and LLMs only show the generation results of requirements with very high confidence. In contrast, a smaller
T
T
makes
HonestCoder
more aggressive, and the shown programs may contain minor mistakes.
4.
Evaluation Benchmark -
TruthCodeBench
In this section, we collect an evaluation benchmark named
TruthCodeBench
to evaluate
HonestCoder
. We show an overview of
TruthCodeBench
and then describe its collection pipeline.
4.1.
An Overview of
TruthCodeBench
Data Format.
TruthCodeBench
covers two popular programming languages,
i.e.,
Python and Java. Both languages are mainstream programming languages for software developers and are widely used by developers around the world
(
SnapLogic, 2024
)
. Thus, we start
TruthCodeBench
with these two languages and leave other languages in future work.
Figure
4
shows two samples in
TruthCodeBench
. Each sample in
TruthCodeBench
consists of two components: a requirement and LLM-specific binary labels (
i.e.,
passed or failed). The label represents whether the specific LLM can generate the correct programs for a requirement. We expect that
HonestCoder
only shows the generated code for passed requirements and refuses failed requirements.
Figure 4.
Two samples of
TruthCodeBench
in Python and Java, respectively. Each sample has two components: a requirement and LLM-specific binary labels (
i.e.,
passed or failed). The label represents whether a specific LLM can generate the correct programs for a requirement. We expect that
HonestCoder
only shows the generated code for passed requirements and refuses failed requirements.
Data Statistics.
The statistics of
TruthCodeBench
are shown in Table
1
. For each language,
TruthCodeBench
contains a training set and a test set. For Python, the training set and test set both contain 569 samples. The training and test sets for Java comprise 563 and 564 samples, respectively. In this paper, we study four popular LLMs and annotate each sample with four LLM-specific labels. The details of four LLMs are described in Section
5.2
. Given that the coding capabilities of LLMs vary, the label distributions of different LLMs are different.
Table 1.
The statistics of
TruthCodeBench
. “Train / Test” means the number of samples in the training and test sets, respectively. “Train/Test Distribution” denotes the rates of passed and failed requirements in the training and test sets, respectively. DS-Coder: DeepSeek Coder. Ins: Instruct.
Language
Train / Test
LLM
Train Distribution
Test Distribution
Python
569 / 569
DS-Code-6.7B-Ins
41.12% / 58.88%
40.25% / 59.75%
DS-Code-1.3B-Ins
35.33% / 64.67%
30.23% / 69.77%
Codellama-13B-Ins
34.97% / 65.03%
30.58% / 69.42%
Codellama-7B-Ins
21.61% / 78.38%
21.97% / 78.03%
Java
563 / 564
DS-Code-6.7B-Ins
39.96% / 60.04%
51.95% / 48.05%
DS-Code-1.3B-Ins
40.67% / 59.33%
43.62% / 56.38%
Codellama-13B-Ins
28.24% / 71.76%
33.33% / 66.67%
Codellama-7B-Ins
20.60% / 79.40%
25.35% / 74.65%
4.2.
Benchmark Collection Pipeline
The collection pipeline of
TruthCodeBench
consists of the following three stages.
Step ❶: Requirement Collection.
We collect requirements from two popular benchmarks,
i.e.,
HumanEval-X
(
Chen et al., 2021
)
and MBXP
(
Austin et al., 2021
)
. These requirements are written by human developers and cover diverse programming domains (
e.g.,
data science and text processing). We collect requirements in Python and Java and leave other languages in future work. We randomly split the requirements into training and test sets in a 5:5 ratio. The split ratio is empirically set based on related work
(
Hendrycks et al., 2021
)
.
Step ❷: Label Annotation.
For each requirement, we annotate LLM-specific labels. Specifically, we allow an LLM to generate
K
K
programs for a requirement and execute test cases to check the programs. If at least one of the
K
K
programs passes all test cases, the requirement is passed; otherwise, it is failed.
In practice, the performance of LLMs on code generation is impacted by inference settings,
e.g.,
sampling algorithms
(
Zhu et al., 2024b
)
and prompt designs
(
Li et al., 2024b
;
Li et al., 2024a
)
. Different inference settings often lead to different generation results for the same requirement and LLM. To ensure annotation consistency, we interviewed 10 experienced developers who regularly use LLMs and summarized their conventions. For example, developers often employ zero-shot prompting and sample programs from LLMs using temperature sampling. The common temperatures include 0, 0.2, 0.6, 0.8, and 1. Besides, developers’ time and energy are limited. If an LLM fails to solve a requirement within a limited number of attempts (
i.e.,
average: 3.4, max: 5), developers prefer to manually write the code than read the generated erroneous programs.
Based on the above conventions, we design a default inference setting. Given a requirement, we use zero-shot prompting and temperature sampling to sample five programs from an LLM. The five programs are generated by different temperatures (
i.e.,
0, 0.2, 0.6, 0.8, and 1). If any of the five programs pass all test cases, the requirement is passed for specific LLMs; otherwise, it is failed. In future work, practitioners can design inference settings based on their application scenarios and label data following our pipeline.
5.
Study Design
We conduct a large-scale study to evaluate our
HonestCoder
. This section describes the settings of our study, including research questions, studied LLMs, compared baselines, and evaluation metrics.
5.1.
Research Questions
The goal of
HonestCoder
is to estimate LLMs’ confidence in requirements and avoid showing the generated erroneous code to developers. Thus, we design the RQ1 and RQ2 to evaluate the effectiveness of
HonestCoder
in these two aspects.
RQ1: How does
HonestCoder
perform in distinguishing between passed and failed requirements?
As shown in Figure
3
,
HonestCoder
estimates LLMs’ confidence and only shows the generated programs for high-confidence requirements. Thus, accurate confidence estimation is crucial. In this RQ, we evaluate the capability of
HonestCoder
in distinguishing between passed and failed requirements based on confidence.
Specifically, we apply
HonestCoder
to
TruthCodeBench
and estimate a confidence score for each requirement. If the confidence score exceeds a threshold, the requirement is predicted as passed. Otherwise, it is predicted as failed. Then, we use evaluation metrics (Section
5.4
) to comprehensively measure the performance of
HonestCoder
under different thresholds. To show the superiority of
HonestCoder
, we design eight baselines (Section
5.3
) for comparison.
RQ2: How does
HonestCoder
perform in decreasing the number of erroneous programs shown to developers?
In this RQ, we set three control groups. In the first group, LLMs indiscriminately show the generated programs to developers. In the second and third groups, LLMs selectively show the generated programs based on the predictions of baselines and
HonestCoder
, respectively. Then, we count the numbers of correct and erroneous programs shown to developers in three groups.
As stated in Section
3.3
, a critical stage in
HonestCoder
is to estimate the LLMs’ confidence by measuring the similarity between the generated programs. We propose to measure the similarity from multiple modalities. The RQ3 is designed to validate the effectiveness of our estimator and explore the contributions of different modalities.
RQ3: How effective is the multi-modal estimator?
We design eight variants of our estimators, which use different code similarity metrics. Then, we compare them to our estimator on four LLMs and analyze the contributions of different modalities in our estimator.
5.2.
Studied LLMs
This paper studies four popular LLMs, including DeepSeek-Coder-Instruct-{6.7B, 1.3B}, and Code Llama-Instruct-{13B, 7B}. Their details are shown as follows.
DeepSeek-Coder-Instruct (DS-Coder-Ins)
(
Guo et al., 2024
)
.
It is a family of LLMs for code released by DeepSeek-AI. Researchers develop DS-Coder-Ins by enhancing the DS-Coder-Base through instruction tuning on high-quality data. The training data comprises helpful and impartial human instructions structured by the single-turn dialogue format, containing 2B tokens in total. DS-Coder-Ins provides multiple versions with different sizes. In our experiments, we select DS-Code-Ins with 6.7B and 1.3B parameters.
Code Llama-Instruct (CodeLlama-Ins)
(
Rozière et al., 2023
)
.
It is a popular family of LLMs for code developed by Meta-AI. The first part of its training data is a proprietary dataset consisting of many multi-turn dialogues between a user and an assistant. The second part of the training data is 14k code-related question-answering pairs generated by Llama 2-70B
(
Touvron et al., 2023
)
. In this paper, we select CodeLlama-Ins with 7B and 13B parameters.
5.3.
Compared Baselines
To our knowledge, this paper is the first to explore selectively showing LLM-generated programs to developers. We collect some studies with motivations similar to this paper and apply them to our task. These related studies can be divided into two groups, including code confidence estimation and requirement confidence estimation. We describe their details as follows.
Code confidence-based approaches
aim to estimate the LLMs’ confidence in the generated programs and average the confidence of all programs as output. If the outputted confidence is greater than a threshold, the programs are shown to developers. A recent work
(
Spiess et al., 2024
)
studied a few approaches to estimating code confidence. We select four representative approaches as baselines. We describe their details as follows.
•
Average Prob.
It collects the generation probabilities of code tokens and averages all probabilities as the confidence.
•
Product Prob.
It collects the generation probabilities of code tokens and calculates the product of all probabilities as the confidence.
•
Self-Asking (Code).
It directly uses prompting to ask for the confidence of LLMs in the code. Specifically, we craft a prompt asking LLMs to determine the functional correctness of the generated code,
i.e.,
answering “Yes” or “No”. The prompt is available in our replication package
(
Anonymous, 2024
)
. Then, we extract the output probability of “Yes” as the confidence.
•
Code Classifier.
It is a neural classifier that takes the generated code as input and predicts a probability that the code is functionally correct. Specifically, we select a popular code representation model (
i.e.,
UniXcoder
(
Guo et al., 2022
)
) as the backbone and add a classification head to it. We split the original training set into a new training and validation set. We train this classifier for 20 epochs and select the best checkpoint based on the performance upon the validation set.
Requirement confidence-based approaches
are to estimate the LLMs’ confidence in requirements and determine whether to generate programs for requirements. We apply three effective approaches
(
Wang et al., 2023
)
in question answering to code generation and design the following baselines.
•
Self-Asking (Re.).
It directly uses prompting to ask for the LLMs’ confidence in successfully solving current requirements. Specifically, we craft a prompt asking LLMs to determine whether they can solve a requirement,
i.e.,
answering “Yes” or “No”. The prompt is available in our replication package
(
Anonymous, 2024
)
. Then, we extract the generation probability of “Yes” as the confidence.
•
K-Nearest Neighbor Search (K-NNS).
Its motivation is that if LLMs can solve a specific requirement, then a similar requirement is likely solvable. Given a requirement, K-NNS retrieves
K
K
most similar requirements in the training set. Then, it calculates the ratio of passed requirements in retrieved results as output. This paper employs two retrieval metrics,
i.e.,
BM25
(
Robertson and Zaragoza, 2009
)
and embedding similarity. BM25 is a common text similarity metric. We use a natural language representation model (
i.e.,
Sentence-BERT
(
Reimers and Gurevych, 2019
)
) to convert requirements into embedding vectors and compute the cosine similarity between two embeddings. The value of
K
K
is tuned on the performance of K-NNS on the training set.
•
Requirement Classifier.
It is a neural classifier to predict the probability that LLMs successfully solve the requirement. We select a natural language representation model (
e.g.,
Sentence-BERT
(
Reimers and Gurevych, 2019
)
) as the backbone and add a classification head to it. We split the original training set into a new training and validation set. We train this classifier for 20 epochs and select the best checkpoint based on the performance upon the validation set.
5.4.
Evaluation Metrics
The problem studied in this paper can be viewed as a binary classification task,
i.e.,
whether to show LLM-generated programs to developers. Traditional metrics for classification tasks (
e.g.,
accuracy and F1) are sensitive to pre-defined thresholds and cannot reflect the comprehensive performance of approaches. Following previous studies
(
Xiong et al., 2023
;
Farquhar et al., 2024
)
, we employ two popular metrics,
i.e.,
AUROC and AUCPR. They can measure the comprehensive performance of approaches under different thresholds. We describe the details of two metrics as follows.
AUROC
is a popular metric for evaluating binary classifiers. The closer the AUROC is to 1, the stronger the classification ability of a classifier. We compute the AUROC through a public API
(
scikit learn, 2024b
)
.
AUROC is the area under a ROC curve. The ROC curve represents the relationships between TPR (True Positive Rate) and FPR (False Position Rate) under different thresholds. The calculation formulas for TPR and FPR are as follows:
(7)
TPR
=
TP
TP
+
FN
,
FPR
=
FP
FP
+
TN
\text{TPR}=\frac{\text{TP}}{\text{TP}+\text{FN}},\quad\text{FPR}=\frac{\text{FP}}{\text{FP}+\text{TN}}
where TP, FP, TN, and FN denote the number of true positives, false positives, true negatives, and false negatives, respectively.
AUCPR.
It is an effective classification task metric and particularly suitable for unbalanced datasets. AUCPR is a value between 0 and 1. The larger the AUCPR, the better the classification ability of the model. We calculate the AUCPR using a public API
(
scikit learn, 2024a
)
.
Specifically, AUCPR is the area under a PR (Precision-Recall) Curve. The PR curve reflects the relationships between precision and recall under different thresholds. The calculation formulas for precision and recall are as follows:
(8)
Precision
=
TP
TP
+
FP
,
Recall
=
TP
TP
+
FN
\text{Precision}=\frac{\text{TP}}{\text{TP}+\text{FP}},\quad\text{Recall}=\frac{\text{TP}}{\text{TP}+\text{FN}}
6.
Results and Analyses
6.1.
RQ1: The performance in distinguishing between passed and failed requirements
As shown in Figure
3
,
HonestCoder
estimates LLMs’ confidence and only shows the generated programs for high-confidence requirements. Thus, accurate confidence estimation is crucial. In the RQ1, we evaluate the effectiveness of the confidence scores from
HonestCoder
in distinguishing between passed and failed requirements.
Table 2.
The performance of different approaches in distinguishing between passed and failed requirements on
TruthCodeBench
(Python).
CodeLlama-13B-Ins
CodeLlama-7B-Ins
DS-Coder-6.7B-Ins
DS-Coder-1.3B-Ins
Approach
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
Average Prob.
56.64%
36.30%
58.36%
27.27%
54.75%
44.96%
53.49%
34.90%
Product Prob.
54.33%
34.71%
57.12%
25.76%
52.11%
42.85%
51.33%
33.45%
Self-Asking (Code)
53.15%
33.11%
56.17%
24.33%
50.97%
41.58%
50.28%
31.29%
Code Classifier
55.13%
35.19%
57.32%
25.99%
53.05%
43.77%
52.15%
33.67%
Self-Asking (Re.)
51.40%
32.40%
52.47%
26.07%
49.92%
41.11%
54.30%
34.78%
K-NNS (BM25)
60.14%
36.42%
57.60%
29.58%
61.48%
48.09%
62.89%
38.56%
K-NNS (Embedding)
60.33%
37.79%
56.89%
27.74%
59.64%
46.09%
61.90%
37.87%
Requirement Classifier
47.95%
44.37%
44.37%
18.80%
61.56%
48.83%
47.95%
28.17%
HonestCoder
74.05%
54.83%
73.91%
46.55%
63.73%
54.38%
73.36%
50.96%
Relative Improvement
22.74%
23.57%
26.64%
57.37%
3.53%
11.37%
16.65%
32.16%
Table 3.
The performance of different approaches in distinguishing between passed and failed requirements on
TruthCodeBench
(Java).
CodeLlama-13B-Ins
CodeLlama-7B-Ins
DS-Coder-6.7B-Ins
DS-Coder-1.3B-Ins
Approach
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
Average Prob.
55.64%
36.07%
53.38%
25.93%
51.96%
51.53%
58.90%
48.54%
Product Prob.
53.12%
34.79%
51.98%
23.78%
49.22%
48.79%
56.19%
46.78%
Self-Asking (Code)
52.19%
33.14%
50.77%
23.64%
48.56%
47.98%
55.41%
45.70%
Code Classifier
54.33%
35.67%
52.16%
24.77%
50.15%
50.77%
57.21%
47.64%
Self-Asking (Re.)
58.22%
38.65%
56.13%
28.50%
56.52%
58.45%
62.67%
51.75%
K-NNS (BM25)
49.80%
33.58%
54.59%
28.54%
52.71%
53.87%
52.01%
44.16%
K-NNS (Embedding)
54.71%
36.46%
54.53%
27.24%
52.36%
56.07%
54.87%
50.00%
Requirement Classifier
53.61%
34.71%
48.78%
23.79%
41.98%
45.54%
55.46%
46.58%
HonestCoder
68.46%
53.95%
71.73%
46.73%
64.71%
64.17%
68.21%
59.92%
Relative Improvement
17.59%
39.59%
27.79%
63.74%
14.49%
9.79%
8.84%
15.79%
Settings.
We leverage
HonestCoder
or baselines to compute a confidence score for each requirement in
TruthCodeBench
. If the confidence score exceeds a threshold, the requirement is predicted as passed. Otherwise, it is predicted as failed. Then, we use evaluation metrics (Section
5.4
) to comprehensively measure the classification performance of different approaches under different thresholds.
Results and Analyses.
The results of RQ1 are shown in Table
2
and
3
. From the results, we obtain the following insights.
HonestCoder
substantially outperforms baselines in AUROC and AUCPR.
In terms of CodeLlama-7B-Instruct,
HonestCoder
outperforms the strongest baseline by up to 27.79% in AUROC and 63.74% in AUCPR. Both metrics show the comprehensive performance of approaches under different classification thresholds. The substantial improvements show that the confidence from
HonestCoder
provides reliable insights into the correctness of LLM-generated programs.
HonestCoder
is effective in different LLMs and programming languages.
As shown in Table
2
and
3
,
HonestCoder
achieves stable improvements in LLMs with different scales (
e.g.,
13B, 7B, 6.7B, and 1.3B) and languages (
i.e.,
Python and Java). In the future, practitioners can apply
HonestCoder
to more advanced LLMs and new languages in a plug-and-play manner.
Self-Asking and probability-based approaches are prone to be over-confident.
As shown in Table
2
and
3
, the performance of Self-Asking and probability-based approaches is not satisfactory. We inspect 50 failure samples of these baselines. We find that LLMs are prone to express high confidence in requirements and the generated programs. Similar phenomena have also been found in work in other fields
(
Zhang et al., 2024b
;
Xiong et al., 2023
)
. In contrast, our
HonestCoder
offers a more promising direction to confidence estimation and significantly outperforms baselines.
Answer to RQ1:
In four LLMs and two programming languages,
HonestCoder
substantially outperforms baselines in AUROC and AUCPR. The results comprehensively show the effectiveness of
HonestCoder
in distinguishing between passed and failed requirements.
Figure 5.
The number of correct and erroneous programs shown to developers on
TruthCodeBench
. The stars denote the results of showing LLM-generated programs indiscriminately. The curves denote the results of baselines and
HonestCoder
under different thresholds. The closer the curve is to the upper left corner, the better the approach’s performance.
6.2.
RQ2: The performance in reducing erroneous programs shown to developers
As stated in Section
1
, the goal of
HonestCoder
is to avoid showing LLM-generated erroneous programs to developers. Meanwhile, we expect that
HonestCoder
does not hinder LLMs from showing correct programs. Thus, in the RQ2, we evaluate the impact of
HonestCoder
on the number of correct and erroneous programs shown to developers.
Settings.
We set three control groups. In the first group, LLMs indiscriminately show the generated programs to developers. In the second and third groups, LLMs selectively show the generated programs based on the predictions of baselines and our
HonestCoder
, respectively. Then, we count the correct and erroneous programs shown to developers in three groups. According to the developers’ conventions summarized in Section
4.2
, we ask LLMs to generate five programs per requirement. We execute test cases to check the correctness of generated programs.
HonestCoder
and baselines all rely on thresholds for making predictions. To achieve a comprehensive comparison, we take 100 equally spaced values from each approach’s range as its thresholds and show the results under these thresholds.
Results and Analyses.
The results are shown in Figure
5
. The horizontal and vertical axes represent the number of erroneous and correct programs, respectively. The stars in Figure
5
denote the results of the first control group. The curves denote the results of the second and third groups, respectively. Each curve reflects the results of an approach under different thresholds. We expect the LLMs to generate more correct programs and fewer erroneous programs. Thus, the closer a curve is to the upper left corner, the better the approach’s performance.
HonestCoder
effectively decreases the number of erroneous programs shown to developers.
Compared to the results of the first group,
HonestCoder
significantly decreases the number of erroneous programs. However,
HonestCoder
and baselines lose a few correct programs.
HonestCoder
outputs more correct programs and fewer erroneous programs than baselines under different thresholds.
As shown in Figure
5
, the curves of
HonestCoder
are closer to the upper left corners. With the same number of erroneous programs,
HonestCoder
can show more correct programs. Similarly, with the same number of correct programs,
HonestCoder
can show fewer erroneous programs. The results show that
HonestCoder
brings stable improvements over baselines under different thresholds.
Answer to RQ2:
HonestCoder
effectively decreases the number of erroneous programs shown to developers. Besides,
HonestCoder
outperforms baselines by outputting more correct programs and fewer erroneous programs.
6.3.
RQ3: Effectiveness of our multi-modal estimator
As stated in Section
3.3
, a critical stage in
HonestCoder
is to estimate the LLMs’ confidence by measuring the similarity between the generated programs. We propose to measure the similarity from multiple modalities. In the RQ3, we design and compare eight other estimators to our estimator to validate its effectiveness. We also analyze the contributions of different modalities.
Table 4.
The performance of different estimators on
TruthCodeBench
(python).
Estimator
CodeLlama-13B-Ins
CodeLlama-7B-Ins
DS-Coder-6.7B-Ins
DS-Coder-1.3B-Ins
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
BLEU
71.55%
52.91%
72.15%
44.95%
62.35%
52.47%
72.58%
49.85%
CodeBLEU
72.07%
53.54%
72.88%
45.92%
62.54%
53.48%
71.66%
49.32%
Edit Similarity
72.64%
52.39%
70.42%
43.83%
60.19%
49.46%
70.31%
45.65%
Embedding Similarity
69.40%
49.00%
67.46%
39.42%
62.04%
52.91%
68.88%
46.70%
Ours w/o Text
72.74%
53.12%
71.20%
44.13%
62.04%
52.91%
71.31%
47.18%
Ours w/o Syntactic
72.15%
51.77%
72.99%
45.84%
62.04%
52.91%
73.04%
50.30%
Ours w/o Dataflow
73.59%
54.27%
72.99%
45.84%
62.04%
52.91%
71.96%
48.78%
Ours w/o Embedding
71.07%
51.85%
72.15%
44.95%
63.53%
54.31%
71.48%
48.63%
Ours
74.05%
54.83%
73.91%
46.55%
63.73%
54.38%
73.36%
50.96%
Table 5.
The performance of different estimators on
TruthCodeBench
(java).
Estimator
CodeLlama-13B-Ins
CodeLlama-7B-Ins
DS-Coder-6.7B-Ins
DS-Coder-1.3B-Ins
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
AUROC
AUCPR
BLEU
66.46%
51.53%
69.79%
44.18%
63.84%
63.29%
67.36%
57.08%
CodeBLEU
66.86%
51.92%
70.14%
45.55%
63.84%
64.17%
67.49%
57.64%
Edit Similarity
66.41%
51.55%
69.09%
44.42%
63.06%
62.16%
67.83%
57.89%
Embedding Similarity
55.32%
37.91%
62.39%
32.39%
54.06%
55.49%
62.96%
55.86%
Ours w/o Text
66.84%
51.13%
69.33%
45.87%
62.77%
64.05%
68.12%
57.48%
Ours w/o Syntactic
68.12%
53.48%
69.63%
45.77%
63.36%
63.45%
68.20%
59.90%
Ours w/o Dataflow
67.97%
52.81%
70.51%
45.95%
63.86%
63.85%
68.25%
57.33%
Ours w/o Embedding
67.90%
52.55%
70.30%
46.12%
64.60%
64.06%
68.08%
57.73%
Ours
68.46%
53.95%
71.73%
46.73%
64.71%
64.17%
68.21%
59.92%
Settings.
The critical point of an estimator is the code similarity metric. We collect some popular metrics and design the following estimators for comparison:
❶BLEU-based Estimator.
It uses the BLEU
(
Papineni et al., 2002
)
as the similarity metric. BLEU is a classic text similarity metric widely used in code generation
(
Li et al., 2023a
;
Sun et al., 2020
;
Yin and Neubig, 2018
)
. BLEU computes the
n
n
-gram similarity between programs:
(9)
BLEU
=
BP
⋅
exp
⁡
(
∑
n
=
1
4
1
4
​
log
⁡
p
n
)
\text{BLEU}=\text{BP}\cdot\exp\left(\sum_{n=1}^{4}\frac{1}{4}\log p_{n}\right)
where
p
n
p_{n}
is the ratio of overlapping subsequences of length
n
n
between two programs.
❷CodeBLEU-based Estimator.
It uses the CodeBLEU
(
Ren et al., 2020
)
as the similarity metric. CodeBLEU is a variant of BLEU and is designed for code. CodeBLEU revises the weights in BLEU and adds the similarities in code structures. The details of CodeBLEU can be found in its original paper
(
Ren et al., 2020
)
.
❸Edit Similarity-based Estimator.
It uses the edit similarity as the similarity metric. Edit similarity is computed based on the edit distance
(
Wikipedia, 2024
)
. The edit distance between two strings is the minimum number of edit operations (
i.e.,
insertions, deletions, or substitutions) required to transform one string into the other. We compute the edit similarity as follows:
(10)
Edit Similarity
=
1
−
L
​
e
​
v
​
(
c
i
,
c
j
)
m
​
a
​
x
​
(
l
​
e
​
n
​
(
c
i
)
,
l
​
e
​
n
​
(
c
j
)
)
\text{Edit Similarity}=1-\frac{Lev(c_{i},c_{j})}{max(len(c_{i}),len(c_{j}))}
where
c
i
c_{i}
and
c
j
c_{j}
are two programs.
L
​
e
​
v
​
(
⋅
)
Lev(\cdot)
is to compute token-level edit distances between programs.
❹Embedding Similarity-based Estimator.
It considers the embedding similarity as the similarity metric. Following our estimator, it leverages an LLM (
i.e.,
DeepSeek Coder-Instruct-6.7B) to convert programs into dense embedding and outputs the cosine similarity between embeddings.
Besides the above four estimators, we make four variants of our multi-modal estimators by removing different modalities independently. For example, ❺ Ours w/o Text Similarity removes the text similarity. Similarly, we make ❻ Ours w/o Syntactic Similarity, ❼ Ours w/o Dataflow Similarity, and ❽ Ours w/o Embedding Similarity.
Results and Analyses.
Table
4
and
5
shows the performance of
HonestCoder
with different estimators. “Ours” means the proposed multi-modal estimator.
Our estimator performs better than other design choices.
As shown in Table
4
and
5
, our estimator outperforms other designs on four LLMs and two programming languages. We attribute the improvements to our proposed multi-modal code similarity measurement. It offers a comprehensive view to measure the similarities between LLM-generated programs and is beneficial to estimating the certainty of LLMs. In the future, practitioners can introduce more advanced code similarity metrics and further enhance
HonestCoder
.
All four modalities contribute to the performance of
HonestCoder
.
As shown in Table
4
and
5
, removing any of the modalities will result in a degradation of
HonestCoder
’s performance. The results validate our motivation that the similarities between programs are reflected in different aspects. Thus, it is necessary to measure the code similarity from multiple modalities.
Answer to RQ3:
Our multi-modal estimator performs better than the other eight estimators. Besides, an ablation study shows that all four modalities contribute to the performance of
HonestCoder
.
7.
Discussion
Figure 6.
The comparison of different approaches regarding time costs and AUROC. The red dashed line shows the time cost when showing the generated code indiscriminately. “Ours (
N
N
)“ means
HonestCoder
with a sampling size
N
N
.
HonestCoder
adds slight time overheads (approximately 0.4 seconds) and performs better than all baselines in AUROC.
7.1.
Time Efficiency of
HonestCoder
Code generation tools typically require outputting programs efficiently. Thus, it is necessary to measure the time efficiency of
HonestCoder
. We select DS-Coder-1.3B-Ins as the base model and apply
HonestCoder
to it. Then, we calculate the average time costs of
HonestCoder
to process a requirement in
TruthCodeBench
(python). It includes the time costs for estimating LLMs’ confidence and outputting programs. We evaluate baselines in the same way. We run this experiment on an NVIDIA A100 GPU with 40GB memory.
Figure
6
shows the time costs (seconds) and AUROC (%) of different approaches. “Ours (
N
N
)“ means our
HonestCoder
with a sampling size
N
N
. The red dashed line shows generating and showing the code indiscriminately.
HonestCoder
adds slight time overheads (approximately 0.4 seconds) and performs better than all baselines in AUROC. Because the steps (
e.g.,
code generation and confidence estimation) in
HonestCoder
can be parallelized, a larger
N
N
does not result in more time overheads but requires more memory. We set the default
N
N
to 20 because a larger
N
N
slightly improves AUROC. We recommend that practitioners set the sampling size according to specific application scenarios.
7.2.
Threats To Validity
There are two main threats to the validity of our work.
The impact of inference settings.
In Section
4.2
, we annotate requirements as passed and failed requirements based on whether LLMs can generate the correct programs for them. In practice, the performance of LLMs on code generation is sensitive to inference settings,
e.g.,
sampling algorithms
(
Zhu et al., 2024b
)
and prompt designs
(
Li et al., 2024b
;
Li et al., 2024a
)
. To address this threat, we design a default inference setting in the label annotation. The inference setting is designed based on an interview of ten experienced developers and is described in Section
4.2
. Furthermore, our data collection pipeline and
HonestCoder
do not rely on specific inference settings. Practitioners can easily apply our work to different inference settings.
Comparison with test case generation.
Recent studies
(
Yuan et al., 2024
;
Lemieux et al., 2023
)
have proposed automatic test case generation. Intuitively, we can use the generated test cases to check LLM-generated programs and only show passed programs. However, we think this approach has the following limitations.
•
Unreliable.
Auto-generated test cases may be untrustworthy
(
Yuan et al., 2024
)
. Even if a program passes the generated test cases, it could still be wrong.
•
Heavy.
Executing test cases requiring installing all dependencies properly. This is especially problematic when developers want code suggestions in a project with multiple files and dependencies. Even if these dependencies are satisfied, many realistic programming scenarios involve incomplete code under active development where execution is infeasible.
•
Unsafe.
LLM-generated programs may have security risks (
e.g.,
deleting files). Thus, executing such programs requires heavy-weight isolation mechanisms such as a sandbox environment.
In comparison, our
HonestCoder
addresses the above limitations.
HonestCoder
provides a new idea to measure the correctness of programs by estimating the confidence of LLMs. Extensive experiments in four LLMs have shown the effectiveness of our idea. Besides,
HonestCoder
is execution-free and does not rely on any dependencies. Developers can easily use
HonestCoder
on different LLMs and code projects.
8.
Related Work
To our knowledge, this paper is the first to explore selectively showing LLM-generated programs to developers. In this section, we summarize related studies with motivations similar to this paper. These related studies can be divided into two groups, including code confidence estimation and requirement confidence estimation. We describe their details as follows.
Code confidence estimation
aims to estimate the LLMs’ confidence in the generated programs. The confidence reflects the reliability of the generated programs. A recent work
(
Spiess et al., 2024
)
studied a few approaches to estimating code confidence,
e.g.,
average token probability and self-asking. The details of these approaches are in Section
5.3
. The studied approaches are initially designed for natural language generation and have sub-optimal performance in code generation.
Requirement confidence estimation
is to estimate the LLMs’ confidence in requirements. For low-confidence requirements, LLMs should refuse to answer. No public studies are exploring this topic on code generation. We draw on related work
(
Wang et al., 2023
)
in question answering and apply three effective approaches to code generation, including self-asking, K-nearest neighbor search, and requirement classifier. The details of these approaches are described in Section
5.3
.
Comparison with this paper.
The differences between the above studies and this paper are two-fold. First, this paper focuses on a new practical problem (
i.e.,
selectively showing LLMs-generated programs). To address this problem, we propose a new approach -
HonestCoder
and release a new benchmark. Second, our proposed
HonestCoder
provides a new idea to estimate the LLMs’ confidence,
i.e.,
measuring the similarity between LLM-generated multiple programs. In the RQ1 (Section
6.1
) and RQ2 (Section
6.2
), the confidence computed by
HonestCoder
substantially outperforms the above work on four LLMs.
9.
Conclusion and Future Work
LLMs may generate erroneous programs, and we should avoid showing them to developers. To achieve this goal, we propose a novel code generation approach named
HonestCoder
. It selectively shows LLM-generated programs to developers based on the LLMs’ confidence. We propose an effective approach to estimate the LLMs’ confidence in code generation. The confidence provides valuable insights into the reliability of LLM-generated programs. We collect a multilingual benchmark and evaluate
HonestCoder
on it. Extensive experiments show the effectiveness of
HonestCoder
in estimating LLMs’ confidence and reducing the shown erroneous programs.
Future Work.
We summarize the potential directions of our work to facilitate the application of LLMs in software development.
•
Exploring more accurate confidence estimation approaches.
Accurate confidence estimation is valuable in explaining the LLMs’ behavior. In the future, researchers can explore more accurate confidence estimation approaches. For example, we can estimate the LLMs’ confidence based on their internal hidden states and attention scores. Besides, we can also teach LLMs to verbalize their confidence by instruction tuning.
•
Designing more advanced generation techniques.
HonestCoder
refusal to show programs when LLMs are uncertain. In the future, we will explore alternatives. For example, we retrieve relevant programs from a codebase and re-generate programs based on retrieved results. Besides, we can teach LLMs to verbalize why they are uncertain. Then, developers can provide more information to address the LLMs’ uncertainty.
•
Motivating discussion in other fields.
The research problem in this paper probably exists in other code-related tasks,
e.g.,
code repair and vulnerability detection. Our work will motivate broad discussions in these tasks. For example, on vulnerability detection, we can decrease the number of false positives in LLMs’ predictions based on the LLMs’ confidence.
References
Ackley et al
.
(1985)
David H. Ackley, Geoffrey E. Hinton, and Terrence J. Sejnowski. 1985.
A Learning Algorithm for Boltzmann Machines.
Cogn. Sci.
9, 1 (1985), 147–169.
https://doi.org/10.1207/S15516709COG0901_7
Anonymous (2024)
Anonymous. 2024.
HonestCoder.
(9 2024).
https://doi.org/10.6084/m9.figshare.26983477.v1
Austin et al
.
(2021)
Jacob Austin, Augustus Odena, Maxwell I. Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie J. Cai, Michael Terry, Quoc V. Le, and Charles Sutton. 2021.
Program Synthesis with Large Language Models.
CoRR
abs/2108.07732 (2021).
arXiv:2108.07732
https://arxiv.org/abs/2108.07732
Chen et al
.
(2021)
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios
Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021.
Evaluating Large Language Models Trained on Code.
CoRR
abs/2107.03374 (2021).
arXiv:2107.03374
https://arxiv.org/abs/2107.03374
Cosmides and Tooby (1996)
Leda Cosmides and John Tooby. 1996.
Are humans good intuitive statisticians after all? Rethinking some conclusions from the literature on judgment under uncertainty.
Cognition
58, 1 (1996), 1–73.
https://doi.org/10.1016/0010-0277(95)00664-8
Dou et al
.
(2024)
Shihan Dou, Haoxiang Jia, Shenxi Wu, Huiyuan Zheng, Weikang Zhou, Muling Wu, Mingxu Chai, Jessica Fan, Caishuang Huang, Yunbo Tao, et al
.
2024.
What’s Wrong with Your Code Generated by Large Language Models? An Extensive Study.
arXiv preprint arXiv:2407.06153
(2024).
Eghbali and Pradel (2022)
Aryaz Eghbali and Michael Pradel. 2022.
CrystalBLEU: Precisely and Efficiently Measuring the Similarity of Code. In
44th IEEE/ACM International Conference on Software Engineering: Companion Proceedings, ICSE Companion 2022, Pittsburgh, PA, USA, May 22-24, 2022
. ACM/IEEE, 341–342.
https://doi.org/10.1145/3510454.3528648
Farquhar et al
.
(2024)
Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and Yarin Gal. 2024.
Detecting hallucinations in large language models using semantic entropy.
Nat.
630, 8017 (2024), 625–630.
https://doi.org/10.1038/S41586-024-07421-0
GitHub (2023)
GitHub. 2023.
GitHub Copilot.
https://github.com/features/copilot
.
Guo et al
.
(2022)
Daya Guo, Shuai Lu, Nan Duan, Yanlin Wang, Ming Zhou, and Jian Yin. 2022.
UniXcoder: Unified Cross-Modal Pre-training for Code Representation. In
Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022
, Smaranda Muresan, Preslav Nakov, and Aline Villavicencio (Eds.). Association for Computational Linguistics, 7212–7225.
https://doi.org/10.18653/V1/2022.ACL-LONG.499
Guo et al
.
(2021)
Daya Guo, Shuo Ren, Shuai Lu, Zhangyin Feng, Duyu Tang, Shujie Liu, Long Zhou, Nan Duan, Alexey Svyatkovskiy, Shengyu Fu, Michele Tufano, Shao Kun Deng, Colin B. Clement, Dawn Drain, Neel Sundaresan, Jian Yin, Daxin Jiang, and Ming Zhou. 2021.
GraphCodeBERT: Pre-training Code Representations with Data Flow. In
9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021
. OpenReview.net.
https://openreview.net/forum?id=jLoC4ez43PZ
Guo et al
.
(2024)
Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Y. Wu, Y. K. Li, Fuli Luo, Yingfei Xiong, and Wenfeng Liang. 2024.
DeepSeek-Coder: When the Large Language Model Meets Programming - The Rise of Code Intelligence.
CoRR
abs/2401.14196 (2024).
https://doi.org/10.48550/ARXIV.2401.14196
arXiv:2401.14196
Hendrycks et al
.
(2021)
Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob Steinhardt. 2021.
Measuring Coding Challenge Competence With APPS. In
Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021, virtual
, Joaquin Vanschoren and Sai-Kit Yeung (Eds.).
https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/c24cd76e1ce41366a4bbe8a49b02a028-Abstract-round2.html
Lemieux et al
.
(2023)
Caroline Lemieux, Jeevana Priya Inala, Shuvendu K. Lahiri, and Siddhartha Sen. 2023.
CodaMosa: Escaping Coverage Plateaus in Test Generation with Pre-trained Large Language Models. In
45th IEEE/ACM International Conference on Software Engineering, ICSE 2023, Melbourne, Australia, May 14-20, 2023
. IEEE, 919–931.
https://doi.org/10.1109/ICSE48619.2023.00085
Li et al
.
(2024a)
Jia Li, Ge Li, Yongmin Li, and Zhi Jin. 2024a.
Structured Chain-of-Thought Prompting for Code Generation.
ACM Trans. Softw. Eng. Methodol.
(aug 2024).
https://doi.org/10.1145/3690635
Just Accepted.
Li et al
.
(2023a)
Jia Li, Yongmin Li, Ge Li, Zhi Jin, Yiyang Hao, and Xing Hu. 2023a.
SkCoder: A Sketch-based Approach for Automatic Code Generation. In
45th IEEE/ACM International Conference on Software Engineering, ICSE 2023, Melbourne, Australia, May 14-20, 2023
. IEEE, 2124–2135.
https://doi.org/10.1109/ICSE48619.2023.00179
Li et al
.
(2023b)
Jia Li, Chongyang Tao, Zhi Jin, Fang Liu, Jia Li, and Ge Li. 2023b.
ZC
3
{}^{\mbox{3}}
: Zero-Shot Cross-Language Code Clone Detection. In
38th IEEE/ACM International Conference on Automated Software Engineering, ASE 2023, Luxembourg, September 11-15, 2023
. IEEE, 875–887.
https://doi.org/10.1109/ASE56229.2023.00210
Li et al
.
(2024b)
Jia Li, Yunfei Zhao, Yongmin Li, Ge Li, and Zhi Jin. 2024b.
AceCoder: An Effective Prompting Technique Specialized in Code Generation.
ACM Trans. Softw. Eng. Methodol.
(jul 2024).
https://doi.org/10.1145/3675395
Just Accepted.
Lu et al
.
(2022)
Shuai Lu, Nan Duan, Hojae Han, Daya Guo, Seung-won Hwang, and Alexey Svyatkovskiy. 2022.
ReACC: A Retrieval-Augmented Code Completion Framework. In
Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022
, Smaranda Muresan, Preslav Nakov, and Aline Villavicencio (Eds.). Association for Computational Linguistics, 6227–6240.
https://doi.org/10.18653/V1/2022.ACL-LONG.431
Martin (2009)
Robert C. Martin. 2009.
Clean Code - a Handbook of Agile Software Craftsmanship
.
Prentice Hall.
http://vig.pearsoned.com/store/product/1,1207,store-12521_isbn-0132350882,00.html
Nam et al
.
(2024)
Daye Nam, Andrew Macvean, Vincent J. Hellendoorn, Bogdan Vasilescu, and Brad A. Myers. 2024.
Using an LLM to Help With Code Understanding. In
Proceedings of the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024
. ACM, 97:1–97:13.
https://doi.org/10.1145/3597503.3639187
OpenAI (2024)
OpenAI. 2024.
GPT-4o.
https://openai.com/index/hello-gpt-4o/
.
Papineni et al
.
(2002)
Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002.
Bleu: a Method for Automatic Evaluation of Machine Translation. In
Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics, July 6-12, 2002, Philadelphia, PA, USA
. ACL, 311–318.
https://doi.org/10.3115/1073083.1073135
Reimers and Gurevych (2019)
Nils Reimers and Iryna Gurevych. 2019.
Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In
Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019
, Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan (Eds.). Association for Computational Linguistics, 3980–3990.
https://doi.org/10.18653/V1/D19-1410
Ren et al
.
(2020)
Shuo Ren, Daya Guo, Shuai Lu, Long Zhou, Shujie Liu, Duyu Tang, Neel Sundaresan, Ming Zhou, Ambrosio Blanco, and Shuai Ma. 2020.
CodeBLEU: a Method for Automatic Evaluation of Code Synthesis.
CoRR
abs/2009.10297 (2020).
arXiv:2009.10297
https://arxiv.org/abs/2009.10297
Robertson and Zaragoza (2009)
Stephen E. Robertson and Hugo Zaragoza. 2009.
The Probabilistic Relevance Framework: BM25 and Beyond.
Found. Trends Inf. Retr.
3, 4 (2009), 333–389.
https://doi.org/10.1561/1500000019
Rozière et al
.
(2023)
Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton-Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet, Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and Gabriel Synnaeve. 2023.
Code Llama: Open Foundation Models for Code.
CoRR
abs/2308.12950 (2023).
https://doi.org/10.48550/ARXIV.2308.12950
arXiv:2308.12950
Scheffler (2023)
Ian Scheffler. 2023.
A Talk About GitHub Copilot.
https://www.freethink.com/robots-ai/github-copilot
.
scikit learn (2024a)
scikit learn. 2024a.
A Public API for Computing AUCPR.
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.auc.html
.
scikit learn (2024b)
scikit learn. 2024b.
A Public API for Computing AUROC.
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
.
SnapLogic (2024)
SnapLogic. 2024.
Python vs. Java Performance – Comparison & Examples.
https://www.snaplogic.com/glossary/python-vs-java-performance
.
Spiess et al
.
(2024)
Claudio Spiess, David Gros, Kunal Suresh Pai, Michael Pradel, Md. Rafiqul Islam Rabin, Amin Alipour, Susmit Jha, Prem Devanbu, and Toufique Ahmed. 2024.
Calibration and Correctness of Language Models for Code.
CoRR
abs/2402.02047 (2024).
https://doi.org/10.48550/ARXIV.2402.02047
arXiv:2402.02047
Sun et al
.
(2020)
Zeyu Sun, Qihao Zhu, Yingfei Xiong, Yican Sun, Lili Mou, and Lu Zhang. 2020.
TreeGen: A Tree-Based Transformer Architecture for Code Generation. In
The Thirty-Fourth AAAI Conference on Artificial Intelligence, AAAI 2020, The Thirty-Second Innovative Applications of Artificial Intelligence Conference, IAAI 2020, The Tenth AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI 2020, New York, NY, USA, February 7-12, 2020
. AAAI Press, 8984–8991.
https://doi.org/10.1609/AAAI.V34I05.6430
Touvron et al
.
(2023)
Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton-Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa,
Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen
Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurélien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. 2023.
Llama 2: Open Foundation and Fine-Tuned Chat Models.
CoRR
abs/2307.09288 (2023).
https://doi.org/10.48550/ARXIV.2307.09288
arXiv:2307.09288
Wan et al
.
(2022)
Yao Wan, Wei Zhao, Hongyu Zhang, Yulei Sui, Guandong Xu, and Hai Jin. 2022.
What Do They Capture? - A Structural Analysis of Pre-Trained Language Models for Source Code. In
44th IEEE/ACM 44th International Conference on Software Engineering, ICSE 2022, Pittsburgh, PA, USA, May 25-27, 2022
. ACM, 2377–2388.
https://doi.org/10.1145/3510003.3510050
Wang et al
.
(2023)
Yile Wang, Peng Li, Maosong Sun, and Yang Liu. 2023.
Self-Knowledge Guided Retrieval Augmentation for Large Language Models. In
Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023
, Houda Bouamor, Juan Pino, and Kalika Bali (Eds.). Association for Computational Linguistics, 10303–10315.
https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.691
Wang et al
.
(2024)
Zhijie Wang, Zijie Zhou, Da Song, Yuheng Huang, Shengmai Chen, Lei Ma, and Tianyi Zhang. 2024.
Where Do Large Language Models Fail When Generating Code?
CoRR
abs/2406.08731 (2024).
https://doi.org/10.48550/ARXIV.2406.08731
arXiv:2406.08731
Wikipedia (2024)
Wikipedia. 2024.
Levenshtein Distance.
https://en.wikipedia.org/wiki/Levenshtein_distance
.
Xiong et al
.
(2023)
Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan Hooi. 2023.
Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs.
CoRR
abs/2306.13063 (2023).
https://doi.org/10.48550/ARXIV.2306.13063
arXiv:2306.13063
Yin and Neubig (2018)
Pengcheng Yin and Graham Neubig. 2018.
TRANX: A Transition-based Neural Abstract Syntax Parser for Semantic Parsing and Code Generation. In
Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, EMNLP 2018: System Demonstrations, Brussels, Belgium, October 31 - November 4, 2018
, Eduardo Blanco and Wei Lu (Eds.). Association for Computational Linguistics, 7–12.
https://doi.org/10.18653/V1/D18-2002
Yuan et al
.
(2024)
Zhiqiang Yuan, Mingwei Liu, Shiji Ding, Kaixin Wang, Yixuan Chen, Xin Peng, and Yiling Lou. 2024.
Evaluating and Improving ChatGPT for Unit Test Generation.
Proc. ACM Softw. Eng.
1, FSE (2024), 1703–1726.
https://doi.org/10.1145/3660783
Zhang et al
.
(2024a)
Mozhi Zhang, Mianqiu Huang, Rundong Shi, Linsen Guo, Chong Peng, Peng Yan, Yaqian Zhou, and Xipeng Qiu. 2024a.
Calibrating the Confidence of Large Language Models by Eliciting Fidelity.
CoRR
abs/2404.02655 (2024).
https://doi.org/10.48550/ARXIV.2404.02655
arXiv:2404.02655
Zhang et al
.
(2024b)
Mozhi Zhang, Mianqiu Huang, Rundong Shi, Linsen Guo, Chong Peng, Peng Yan, Yaqian Zhou, and Xipeng Qiu. 2024b.
Calibrating the Confidence of Large Language Models by Eliciting Fidelity.
CoRR
abs/2404.02655 (2024).
https://doi.org/10.48550/ARXIV.2404.02655
arXiv:2404.02655
Zhou et al
.
(2019)
Yaqin Zhou, Shangqing Liu, Jing Kai Siow, Xiaoning Du, and Yang Liu. 2019.
Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics via Graph Neural Networks. In
Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada
, Hanna M. Wallach, Hugo Larochelle, Alina Beygelzimer, Florence d’Alché-Buc, Emily B. Fox, and Roman Garnett (Eds.). 10197–10207.
https://proceedings.neurips.cc/paper/2019/hash/49265d2447bc3bbfe9e76306ce40a31f-Abstract.html
Zhu et al
.
(2024a)
Qihao Zhu, Daya Guo, Zhihong Shao, Dejian Yang, Peiyi Wang, Runxin Xu, Y Wu, Yukun Li, Huazuo Gao, Shirong Ma, et al
.
2024a.
DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence.
arXiv preprint arXiv:2406.11931
(2024).
Zhu et al
.
(2024b)
Yuqi Zhu, Jia Li, Ge Li, Yunfei Zhao, Jia Li, Zhi Jin, and Hong Mei. 2024b.
Hot or Cold? Adaptive Temperature Sampling for Code Generation with Large Language Models. In
Thirty-Eighth AAAI Conference on Artificial Intelligence, AAAI 2024, Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence, IAAI 2024, Fourteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2014, February 20-27, 2024, Vancouver, Canada
, Michael J. Wooldridge, Jennifer G. Dy, and Sriraam Natarajan (Eds.). AAAI Press, 437–445.
https://doi.org/10.1609/AAAI.V38I1.27798