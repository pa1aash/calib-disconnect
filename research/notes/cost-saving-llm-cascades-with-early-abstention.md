---
title: Cost-Saving LLM Cascades with Early Abstention
id: cost-saving-llm-cascades-with-early-abstention
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:09:14.491913Z'
updated: '2026-11-09T23:27:44.631988Z'
source: https://arxiv.org/html/2502.09054
source_domain: arxiv.org
fetched_at: '2026-11-09T23:09:14.491542Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Early abstention in LLM cascades (arXiv 2502.09054): lets small models abstain,
  cutting test loss 2.2% on average across six benchmarks, 13.0% cost reduction, 5.0%
  error reduction for 4.1% higher abstention. Non-code. FULL TEXT. Verdict: L3 adjacent:
  confidence-gated cascade cost framing in non-code tasks.'
---

Cost-Saving LLM Cascades with Early Abstention
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2502.09054v2 [cs.AI] 29 Mar 2025
Cost-Saving LLM Cascades with Early Abstention
Michael J. Zellinger & Rex Liu
Affiliation:
Computing + Mathematical Sciences
Affiliation:
California Institute of Technology
Affiliation:
{zellinger, rex}@caltech.edu
Matt Thomson
Affiliation:
Biology & Biological Engineering
Affiliation:
California Institute of Technology
Email:
mthomson@caltech.edu
Abstract
LLM cascades deploy small LLMs to answer most queries, limiting the use of large and expensive LLMs to difficult queries. This approach can significantly reduce costs without impacting performance. However, risk-sensitive domains such as finance or medicine place an additional premium on avoiding model errors. Since even the most expensive models are susceptible to making mistakes, applications in these domains benefit from allowing LLM systems to completely abstain from answering difficult queries. Introducing abstention poses a design question for LLM cascades: should abstention only be allowed at the final model or also at earlier models? Since error patterns of small and large models are correlated, allowing earlier models to abstain may reduce inference costs and latency by anticipating abstention decisions by expensive and slow models– avoiding the need to run these models. We investigate the benefits of such “early abstention” in LLM cascades and find that it reduces overall test loss by 2.2% on average across six benchmarks (GSM8K, MedMCQA, MMLU, TriviaQA, TruthfulQA, and XSum). These gains result from a more effective use of abstention, trading a 4.1% average increase in the overall abstention rate for a 13.0% reduction in cost and a 5.0% reduction in error rate. Our findings demonstrate the possibility of leveraging correlations between the error patterns of different language models to drive performance improvements for LLM systems with abstention.
1
Introduction
Following the proliferation of publicly available LLMs, many authors have proposed combining different models into LLM systems to enhance reliability and reduce costs. Specifically, LLM cascades have emerged as a powerful design pattern for navigating the trade-off between performance and cost when deploying LLMs (
Chen et al.,, 2023
;
Aggarwal et al.,, 2024
;
Yue et al.,, 2024
;
Jitkrittum et al.,, 2024
), especially for edge-to-cloud deployments (
Kag et al.,, 2023
).
The basic idea behind cascades is that it would be inefficient to process all queries using the largest and most expensive LLMs. On many tasks, relatively small LLMs can correctly answer most queries. To leverage this fact, a cascade initially sends each query to a small LLM. If this small model has a high chance of correctly answering the query, as measured by a confidence indicator, the cascade returns the output to the user. Otherwise, the cascade defers the query to a larger and more expensive model. In this way, LLM cascades yield impressive cost and latency reductions without meaningfully compromising performance (
Chen et al.,, 2023
). However, cost and latency reduction are not the only desiderata of an LLM cascade. In risk-sensitive areas such as finance, law, or medicine, the overriding concern is often to avoid mistakes. For these applications, it is natural to give LLM cascades the ability to abstain from answering any query when the risk of making a mistake is significant (
Chow,, 1957
,
Chow,, 1970
,
El-Yaniv and Wiener,, 2010
,
Cortes et al.,, 2016
).
Introducing abstention poses a design question for LLM cascades: is it sufficient to allow the final model to abstain, or should the smaller models at the start of the cascade be allowed to abstain “early”? Since error patterns of small and large models are correlated (
Zellinger and Thomson,, 2025
), there is a potential for the small models to anticipate abstention decisions by large models, significantly reducing inference cost and latency on abstained queries.
Understanding the benefits of such
early abstention
is important for cascade design since implementing early abstention requires access to a cascade’s internal logic– it cannot simply be added on later to a black-box cascade. By contrast, abstaining at the final model can be implemented as a simple post-processing step of the final model’s output and its associated confidence score. Hence, an understanding of the benefits of early abstention helps inform whether the capacity for abstention can be effectively
decoupled
from the overall implementation of a cascade.
In this paper, our main contributions are as follows:
•
We introduce the possibility of “early abstention” for LLM cascades with abstention.
•
We extend the continuous optimization-based algorithm for tuning confidence thresholds in LLM cascades of
Zellinger and Thomson, (2025)
to a multi-objective formalism incorporating abstention.
•
We demonstrate that early abstention lowers the overall test loss by 2.2% across six benchmarks (GSM8K, MedMCQA, MMLU, TriviaQA, TruthfulQA, XSum).
•
We show that early abstention allows cascades to make more effective use of the ability to abstain, trading an increase in the abstention rate (+4.1% on average) for significant cost reductions (-13.0% on average) and error reductions (-5.0% on average).
2
Background and Related Work
This paper combines two distinct strands of research within the language modeling community: selective prediction, which aims at reducing the error rate by allowing models to abstain on the most difficult queries, and LLM cascades, which focus on combining small and large LLMs to reduce cost.
Selective prediction.
Selective prediction focuses on giving machine learning models the ability to abstain on difficult queries (
El-Yaniv and Wiener, (2010)
). This perspective is especially useful in risk-sensitive domains, where the cost of making a mistake far outweighs the inconvenience of handling abstained queries. The field goes back to the works of Chow (
Chow, (1957)
,
Chow, (1970)
), who analyzed abstention in the context of applying optical character recognition to scanning business documents.
Geifman and El-Yaniv, (2017)
applied selective prediction in deep learning, significantly reducing image classification error rates.
In natural language processing,
Xin et al., (2021)
and
Yoshikawa and Okazaki, (2023)
introduced abstention for language models by thresholding various confidence scores derived from the conditional token distribution. In the modern era of
large
language models post-ChatGPT, selective prediction research has largely taken place in the emerging field of uncertainty quantification for LLMs (
Manakul et al.,, 2023
;
Farquhar et al.,, 2024
;
Lin et al.,, 2024
).
LLM cascades.
LLM cascades leverage confidence scores in a different way from selective prediction. Rather than abstain on difficult queries, a cascade adaptively selects the most cost-effective model to answer each query. An incoming query first goes to a small LLM. If the small model’s confidence score is below a chosen threshold, the cascade forwards the query to a larger and more powerful LLM. This approach has yielded impressive cost savings without impacting performance (
Chen et al.,, 2023
;
Aggarwal et al., (2024)
;
Yue et al.,, 2024
). Cascades often make use of an LLM’s conditional probability distribution for computing confidence scores (
Jitkrittum et al.,, 2024
), finetune smaller language models for correctness prediction (
Chen et al.,, 2023
), or compute consistency-based uncertainty metrics (
Yue et al.,, 2024
).
However, few prior works raise the question of correlations between the confidence scores of different LLMs, with the exception of
Zellinger and Thomson, (2025)
. Our approach benefits from such correlations, as they make it easier for small models to anticipate abstention decisions by larger models.
3
Cost-Saving LLM Cascades with Abstention
Cascades with abstention.
Let
C
=
M
1
→
…
→
M
k
C=M_{1}\rightarrow...\rightarrow M_{k}
be a large language model (LLM) cascade. Given a query
x
x
, each model
M
i
M_{i}
uses a confidence score
Φ
i
=
Φ
i
​
(
x
)
∈
[
0
,
1
]
\Phi_{i}=\Phi_{i}(x)\in[0,1]
to decide whether to return the response or defer the query to
M
i
+
1
M_{i+1}
. In a typical LLM cascade without abstention,
M
i
M_{i}
returns the response if its confidence
Φ
i
\Phi_{i}
exceeds its deferral threshold
ϕ
i
\phi_{i}
.
To introduce the possibility of abstention, we pair each deferral threshold
ϕ
i
\phi_{i}
with an additional
abstention threshold
ξ
i
<
ϕ
i
\xi_{i}<\phi_{i}
. The intuition is that if confidence is
low
, the model should defer, but if it is
very low
, the model should abstain. Given a query
x
x
, the output
C
⁡
(
x
)
C(x)
of a cascade
C
=
M
1
→
…
→
M
k
C=M_{1}\rightarrow...\rightarrow M_{k}
with deferral thresholds
(
ϕ
1
,
…
,
ϕ
k
−
1
)
(\phi_{1},...,\phi_{k-1})
and abstention thresholds
(
ξ
1
,
…
,
ξ
k
)
(\xi_{1},...,\xi_{k})
is then defined recursively as
C
(
x
)
=
{
M
1
​
(
x
)
if
​
Φ
1
​
(
x
)
>
ϕ
1
​
or
​
|
C
|
=
1
C
2:k
(
x
)
if
​
ξ
1
≤
Φ
1
​
(
x
)
≤
ϕ
1
,
∅
if
​
Φ
1
​
(
x
)
<
ξ
1
,
C(x)=\begin{cases}M_{1}(x)&\text{~if~}\Phi_{1}(x)>\phi_{1}\text{~or~}|C|=1\\
C_{\text{2:k}}(x)&\text{~if~}\xi_{1}\leq\Phi_{1}(x)\leq\phi_{1},\\
\varnothing&\text{~if~}\Phi_{1}(x)<\xi_{1},\end{cases}
(1)
where
C
2:k
C_{\text{2:k}}
is the subcascade
M
2
→
…
→
M
k
M_{2}\rightarrow...\rightarrow M_{k}
, and returning
∅
\varnothing
means that the cascade abstains.
In other words, the cascade abstains if the confidence score for any model
M
i
M_{i}
falls below its abstention threshold
ξ
i
\xi_{i}
. If the confidence score exceeds
ξ
i
\xi_{i}
but is still below the deferral threshold
ϕ
i
\phi_{i}
, the query is forwarded to
M
i
+
1
M_{i+1}
. Note that the final model
M
k
M_{k}
of the cascade has an abstention threshold
ξ
k
\xi_{k}
but no deferral threshold, since there is no downstream model to which it could defer the query.
Definition
(Early Abstention)
.
Given a cascade
C
=
M
1
→
…
→
M
k
C=M_{1}\rightarrow...\rightarrow M_{k}
with deferral thresholds
ϕ
=
(
ϕ
1
,
…
,
ϕ
k
−
1
)
\boldsymbol{\phi}=(\phi_{1},...,\phi_{k-1})
and abstention thresholds
𝝃
=
(
ξ
1
,
…
,
ξ
k
)
\boldsymbol{\xi}=(\xi_{1},...,\xi_{k})
, we define
early abstention
as the event
𝒜
E
=
⋃
i
=
1
k
−
1
{
x
:
Φ
i
​
(
x
)
<
ξ
i
}
\mathcal{A}_{E}=\bigcup_{i=1}^{k-1}\{x:\Phi_{i}(x)<\xi_{i}\}
(2)
that the confidence
Φ
i
\Phi_{i}
of an earlier model
(
i
<
k
)
(i<k)
falls below its abstention threshold
ξ
i
\xi_{i}
.
Compared to abstaining only at the final model, early abstention can reduce the cost and latency of a cascade, since confidence scores between small and large LLMs are often correlated (
Zellinger and Thomson,, 2025
). In Section
4.1
, we present empirical precision-recall trade-offs for the ability to anticipate a large model’s abstention decisions.
Evaluating cascade performance.
Introducing abstention adds complexity to performance evaluation, as the overall performance of a cascade now depends on the error rate, cost, and abstention rate– a three-dimensional space. Consistent with standard multi-objective optimization, given two performance vectors
ν
=
(
e
,
c
,
a
)
\nu=(e,c,a)
and
ν
′
=
(
e
′
,
c
′
,
a
′
)
\nu^{\prime}=(e^{\prime},c^{\prime},a^{\prime})
we say that
ν
\nu
dominates
ν
′
\nu^{\prime}
if
e
≤
e
′
e\leq e^{\prime}
,
c
≤
c
′
c\leq c^{\prime}
, and
a
≤
a
′
a\leq a^{\prime}
, and at least one of the inequalities is strict. Any performance vector
ν
\nu
that is not dominated by any other performance vector is
Pareto-optimal
.
A cascade
C
C
gives rise to a set of Pareto-optimal performance vectors, corresponding to the possible choices for deferral and abstention thresholds. For example, raising deferral thresholds generally results in lower error rates while increasing cost; raising abstention thresholds leads to lower error rates while increasing the abstention rate. The set of Pareto-optimal performance vectors
Γ
⁡
(
C
)
=
{
ν
∈
ℝ
3
:
ν
​
is Pareto-optimal for
C
}
\Gamma(C)=\{\nu\in\mathbb{R}^{3}:\nu\text{~is Pareto-optimal for $C$}\}
(3)
forms a nonlinear two-dimensional surface embedded in
ℝ
3
\mathbb{R}^{3}
. These surfaces can be cumbersome to compare across different cascades. We provide a more user-friendly approach by introducing the user preference parameters
λ
c
≥
0
\lambda_{\text{c}}\geq 0
and
λ
a
≥
0
\lambda_{\text{a}}\geq 0
measuring the user’s sensitivity towards higher cost and query abstention, respectively, relative to the need for avoiding errors.
Definition
(Cascade Loss)
.
We measure performance of a cascade
C
C
, given user preferences
λ
c
\lambda_{c}
,
λ
a
≥
0
\lambda_{a}\geq 0
for avoiding cost and query abstentions, by the
cascade loss
ℓ
⁡
(
λ
c
,
λ
a
)
=
min
ϕ
,
𝝃
⁡
ℙ
⁡
(
Error
∧
¬
Abstention
)
+
λ
c
​
𝔼
​
[
Cost
]
+
λ
a
​
ℙ
​
(
Abstention
)
,
\ell(\lambda_{c},\lambda_{a})=\min_{\boldsymbol{\phi},\boldsymbol{\xi}}\mathbb{P}(\text{Error}\land\neg\text{Abstention})+\lambda_{\text{c}}~\mathbb{E}[\text{Cost}]+\lambda_{\text{a}}~\mathbb{P}(\text{Abstention}),
(4)
where
[
ϕ
,
𝝃
]
=
[
ϕ
1
,
…
,
ϕ
k
−
1
,
ξ
1
,
…
,
ξ
k
]
∈
ℝ
2
​
k
−
1
[\boldsymbol{\phi},\boldsymbol{\xi}]=[\phi_{1},...,\phi_{k-1},\xi_{1},...,\xi_{k}]\in\mathbb{R}^{2k-1}
are the deferral and abstention thresholds. Given a grid of user preferences
Λ
c
×
Λ
a
\Lambda_{c}\times\Lambda_{a}
, we measure overall system performance by the
overall cascade loss
ℒ
⁡
(
C
)
=
1
|
Λ
c
|
​
|
Λ
a
|
​
∑
(
λ
c
,
λ
a
)
∈
Λ
c
×
Λ
a
ℓ
⁡
(
λ
c
,
λ
a
)
,
\mathcal{L}(C)=\frac{1}{|\Lambda_{c}||\Lambda_{a}|}\sum_{(\lambda_{c},\lambda_{a})\in\Lambda_{c}\times\Lambda_{a}}\ell(\lambda_{c},\lambda_{a}),
(5)
which averages the cascade loss over the grid of user preferences.
Equation (
4
) aligns with previous work on selective prediction (
Cortes et al.,, 2016
), while the overall cascade loss (
5
) provides an effective means for comparing different cascades, while avoiding the difficulties of nonlinear Pareto surfaces. Figure
1
illustrates our approach for evaluating cascade performance across the user preference space. Importantly, each pair of preferences
(
λ
c
,
λ
a
)
(\lambda_{c},\lambda_{a})
requires separately optimizing the cascade thresholds
[
ϕ
,
𝝃
]
∈
ℝ
2
​
k
−
1
[\boldsymbol{\phi},\boldsymbol{\xi}]\in\mathbb{R}^{2k-1}
.
Figure 1:
Our framework evaluates cascade performance across the range of user preferences by taking into account the user’s desire to reduce cost (
λ
c
\lambda_{c}
) and abstention (
λ
a
\lambda_{a}
), relative to the need for avoiding errors.
Optimizing cascade thresholds
. Computing the cascade loss
ℓ
⁡
(
λ
c
,
λ
a
)
\ell(\lambda_{c},\lambda_{a})
requires selecting deferral and abstention thresholds
[
ϕ
,
𝝃
]
∈
ℝ
2
​
k
−
1
[\boldsymbol{\phi},\boldsymbol{\xi}]\in\mathbb{R}^{2k-1}
for each choice of user preferences
(
λ
c
,
λ
a
)
(\lambda_{c},\lambda_{a})
. Intuitively, penalizing cost (
λ
c
↑
\lambda_{c}\uparrow
) results in lower deferral thresholds (increased use of smaller models), whereas penalizing abstention (
λ
a
↑
\lambda_{a}\uparrow
) leads to lower abstention thresholds (less abstention). To optimize
[
ϕ
,
𝝃
]
[\boldsymbol{\phi},\boldsymbol{\xi}]
for each
(
λ
c
,
λ
a
)
(\lambda_{c},\lambda_{a})
, we apply the continuous optimization-based algorithm of
Zellinger and Thomson, (2025)
. Their approach is based on
1.
Modeling the joint distribution of confidence scores
(
Φ
1
,
…
,
Φ
k
)
(\Phi_{1},...,\Phi_{k})
through a Markov factorization based on mixture-of-beta marginals
p
⁡
(
Φ
i
)
p(\Phi_{i})
and copula-based conditionals
p
⁡
(
Φ
i
|
Φ
i
−
1
)
p(\Phi_{i}|\Phi_{i-1})
:
p
⁡
(
Φ
1
,
…
,
Φ
k
)
≈
p
⁡
(
Φ
1
)
​
∏
i
=
2
k
p
⁡
(
Φ
i
|
Φ
i
−
1
)
.
p(\Phi_{1},...,\Phi_{k})\approx p(\Phi_{1})\prod_{i=2}^{k}p(\Phi_{i}|\Phi_{i-1}).
2.
Plugging
[
ϕ
[\boldsymbol{\phi}
,
𝝃
\boldsymbol{\xi}
]-differentiable expressions for the error probability, expected cost, and abstention probability into the cascade loss (
4
) and finding the optimal cascade thresholds
ϕ
∗
,
𝝃
∗
\boldsymbol{\phi}^{*},\boldsymbol{\xi}^{*}
using a continuous optimizer.
We apply this continuous optimization-based approach largely because a simple grid search faces runtime issues with increasing numbers of parameters. Implementing early abstention essentially doubles the number of cascade thresholds from
k
−
1
k-1
(deferral thresholds only) to
2
​
k
−
1
2k-1
(deferral and abstention thresholds), so the cross-over point when grid search becomes inconveniently slow happens much sooner (as early as
k
=
3
k=3
).
Note that
Zellinger and Thomson, (2025)
do not consider abstention, so we extend their methodology to include abstention thresholds. We provide the modified Markov equations for the the correctness probability, expected cost, and abstention rate in Appendix A. Solving the optimization problem (
4
) requires enforcing the inequalities
ξ
i
<
ϕ
i
\xi_{i}<\phi_{i}
for
i
<
k
i<k
(each abstention threshold must be lower than its corresponding deferral threshold). To implement these constraints, we switch the optimizer to sequential least squares (
Virtanen et al.,, 2020
).
Quantifying confidence
. To compute LLM confidence scores, we follow the approach of
Zellinger and Thomson, (2025)
, who use logistic regression to calibrate a token-based confidence signal
p
raw
​
(
x
)
p_{\text{raw}}(x)
, which varies based on the type of task:
•
multiple-choice question answering
:
p
raw
p_{\text{raw}}
is the maximum probability assigned to the valid answer tokens (for example, “A”, “B”, “C”, or “D” for MMLU)
•
free-form natural language generation
: the LLM receives a follow-up verification query to assess whether its proposed response is correct;
p
raw
p_{\text{raw}}
is the token probability assigned to “Y” (yes, correct) as opposed to “N” (no, incorrect)
In principle, any other confidence signal could be used, such as the consistency-based confidence measures proposed by
Manakul et al., (2023)
and
Farquhar et al., (2024)
.
4
Results
First, we demonstrate the inefficiency of abstaining at the final model by showing that smaller models are capable of anticipating a large model’s decision to abstain. Second, we compare the overall cascade loss between cascades
with
and
without
early abstention, finding that
•
Early abstention improves overall cascade performance by 2.2% on average, ranging from a 2% detriment to a 7.3% gain across six benchmarks.
•
The benefits of early abstention are visibly concentrated in the upper right quadrant of the user preference space (
λ
c
\lambda_{c}
high,
λ
a
\lambda_{a}
low), where cost is a concern and abstention is not heavily penalized.
•
Early abstention makes more effective use of the ability to abstain, trading a 4.1% increase in the overall abstention rate for an average cost reduction of 13.0% and an average error reduction of 5.0%.
To carry out our experiments, we build on the data from
Zellinger and Thomson, (2025)
. All results are based on a low-data regime with
n
≈
300
n\approx 300
training examples, and LLMs are prompted zero-shot.
4.1
The Inefficiency of Final-Model Abstention
(a)
Llama3.1 405B, 20%
(b)
OpenAI GPT-4o, 20%
(c)
Qwen2.5 72B, 20%
(d)
Llama3.1 405B, 30%
(e)
OpenAI GPT-4o, 30%
(f)
Qwen2.5 72B, 30%
Figure 2:
Precision-recall curves for
early abstention
– predicting a large model’s decision to abstain using small models’ confidence scores; % is the large model’s abstention rate. Performance visibly exceeds the random baseline (dashed gray line, equal to large model’s abstention rate). At lower recall, smaller models can often predict final-model abstentions with high precision.
To assess the ability of small models to anticipate abstention decisions by a larger model, we compute empirical precision-recall trade-offs for abstention prediction for the following LLM cascades:
•
Meta Llama3 1B
→
\rightarrow
3B
→
\rightarrow
8B
→
\rightarrow
70B
→
\rightarrow
405B
•
OpenAI GPT-4o Mini
→
\rightarrow
GPT-4o
•
Alibaba Qwen2.5 32B Coder
→
\rightarrow
Qwen 72B
In our experiment, we set the abstention threshold of the final model (highlighted in bold above) so that it abstains on the bottom 20% and 30% of queries with the lowest confidence scores on the training set. We then train logistic regression classifiers to predict these abstention decisions, based on the confidence scores of all previous models in the cascade. The training sets contain
n
≈
300
n\approx 300
examples and the test sets
n
≈
1000
n\approx 1000
examples. See Appendix B for implementation details.
Figure
2
shows the precision-recall trade-offs computed on the test sets. We evaluate abstention prediction on six benchmarks (GSM8K, MMLU, MedMCQA, TriviaQA, TruthfulQA, and XSum) spanning a variety of tasks from mathematical reasoning to summarization.
The results suggest that at low recall, smaller models can often predict final-model abstention with high precision. To see the significance of these results, consider the case of 80% precision at 20% recall. Early abstention leads to cost savings on the correct calls (
30
%
​
abstention rate
×
20
%
​
recall
=
6
%
30\%\text{~abstention rate}\times 20\%\text{~recall}=6\%
of all queries) and incorrect calls (
25
%
​
imprecision/precision
×
6
%
​
correct calls
=
1.5
%
​
of all queries
25\%\text{~imprecision/precision}\times 6\%\text{~correct calls}=1.5\%\text{~of all queries}
). Each instance of early abstention reduces inference costs by approximately a factor of ten. Hence, early abstention reduces overall inference costs roughly from
C
C
to
0.925
×
C
+
0.075
×
(
C
/
10
)
0.925\times C+0.075\times(C/10)
: a
6.75
%
6.75\%
total cost reduction in exchange for raising the overall abstention rate from 30% to 31.5%.
4.2
Evaluating the Benefits of Early Abstention
To formally evaluate the benefits of early abstention, we compare the performance of two different architectures for LLM cascades
M
1
→
…
→
M
k
M_{1}\rightarrow...\rightarrow M_{k}
:
•
Early Abstention (“Early”)
: each model
M
i
M_{i}
has a separate abstention threshold
ξ
i
\xi_{i}
•
Final-Model Abstention (“Final”)
: only
M
k
M_{k}
has an abstention threshold
ξ
k
\xi_{k}
To compare cascade performance, we optimize the cascade thresholds across a grid of user preference parameters
λ
c
,
λ
a
\lambda_{c},\lambda_{a}
as described in Section
3
. We applied light smoothing on the 2D grid of optimal thresholds by detecting outliers
1
1
1
We call a threshold vector an
outlier
if the mean of its components differs from the means of neighboring threshold vectors by much more than the variability of those neighbors. More details can be found in Appendix C.
and replacing their values with the mean values of their neighbors. To assess the overall performance of a cascade, we compute the overall cascade loss (
5
). All reported numbers refer to performance on the the test sets (
n
≈
1000
n\approx 1000
examples). We optimized the cascade thresholds on training sets with
n
≈
300
n\approx 300
examples.
Model names.
In our tables,
LxB
are the Meta Llama3 models with
x
x
billion parameters;
4o
and
4o Mini
are the OpenAI GPT models; and
QxB(c)
are the Alibaba Qwen2.5 (coding) models with
x
x
billion parameters.
Table 1:
Change in overall cascade loss on the test set when using early abstention (“Early”)
compared to final-model abstention (“Final”): GSM8K, MedMCQA, and MMLU.
Cascade
GSM8K
MedMCQA
MMLU
Early
Final
%
𝚫
\boldsymbol{\Delta}
Early
Final
%
𝚫
\boldsymbol{\Delta}
Early
Final
%
𝚫
\boldsymbol{\Delta}
L1B
→
\rightarrow
L3B
0.196
0.199
-1.772
0.349
0.349
0.054
0.319
0.319
0.066
L1B
→
\rightarrow
L8B
0.157
0.158
-0.189
0.355
0.354
0.242
0.279
0.278
0.243
L1B
→
\rightarrow
L70B
0.108
0.111
-2.476
0.243
0.244
-0.441
0.177
0.178
-0.614
L1B
→
\rightarrow
L405B
0.186
0.211
-12.057
0.271
0.285
-5.042
0.199
0.210
-5.243
L3B
→
\rightarrow
L8B
0.182
0.182
0.350
0.355
0.355
-0.065
0.276
0.275
0.300
L3B
→
\rightarrow
L70B
0.120
0.115
4.369
0.247
0.245
1.064
0.174
0.177
-1.520
L3B
→
\rightarrow
L405B
0.161
0.170
-5.615
0.270
0.286
-5.662
0.191
0.201
-4.904
L8B
→
\rightarrow
L70B
0.111
0.111
-0.090
0.254
0.252
0.502
0.178
0.182
-2.292
L8B
→
\rightarrow
L405B
0.131
0.136
-3.735
0.281
0.298
-5.606
0.185
0.197
-5.982
L70B
→
\rightarrow
L405B
0.103
0.102
0.720
0.260
0.269
-3.682
0.169
0.184
-8.250
4o-Mini
→
\rightarrow
Q32Bc
0.093
0.096
-3.895
0.282
0.286
-1.433
0.207
0.209
-1.090
4o-Mini
→
\rightarrow
Q72B
0.091
0.088
3.691
0.259
0.260
-0.410
0.169
0.169
-0.114
4o-Mini
→
\rightarrow
4o
0.093
0.097
-4.833
0.225
0.231
-2.677
0.174
0.180
-3.673
Q32Bc
→
\rightarrow
Q72B
0.116
0.103
11.807
0.287
0.288
-0.207
0.193
0.194
-0.306
Q32Bc
→
\rightarrow
4o
0.103
0.104
-0.951
0.261
0.268
-2.826
0.223
0.238
-6.252
Q72B
→
\rightarrow
4o
0.088
0.092
-4.328
0.242
0.253
-4.169
0.173
0.195
-11.454
Average
0.127
0.130
-1.188
0.277
0.283
-1.897
0.205
0.212
-3.193
Table 2:
Change in overall cascade loss on the test set when using early abstention (“Early”)
compared to final-model abstention (“Final”): TriviaQA, TruthfulQA, and XSum.
Cascade
TriviaQA
TruthfulQA
XSum
Early
Final
%
𝚫
\boldsymbol{\Delta}
Early
Final
%
𝚫
\boldsymbol{\Delta}
Early
Final
%
𝚫
\boldsymbol{\Delta}
L1B
→
\rightarrow
L3B
0.275
0.270
1.594
0.428
0.428
-0.050
0.488
0.497
-1.731
L1B
→
\rightarrow
L8B
0.170
0.169
0.549
0.398
0.395
0.670
0.369
0.371
-0.519
L1B
→
\rightarrow
L70B
0.078
0.075
4.359
0.323
0.327
-1.052
0.231
0.248
-7.131
L1B
→
\rightarrow
L405B
0.087
0.086
1.259
0.286
0.298
-4.004
0.356
0.471
-24.317
L3B
→
\rightarrow
L8B
0.170
0.170
0.194
0.385
0.387
-0.458
0.367
0.371
-1.152
L3B
→
\rightarrow
L70B
0.075
0.075
-0.153
0.323
0.326
-0.873
0.229
0.246
-6.974
L3B
→
\rightarrow
L405B
0.084
0.086
-2.612
0.289
0.300
-3.782
0.354
0.467
-24.184
L8B
→
\rightarrow
L70B
0.080
0.081
-1.880
0.326
0.329
-0.940
0.231
0.250
-7.552
L8B
→
\rightarrow
L405B
0.080
0.081
-1.014
0.290
0.303
-4.451
0.303
0.381
-20.432
L70B
→
\rightarrow
L405B
0.069
0.069
0.005
0.296
0.304
-2.655
0.231
0.249
-7.281
4o-Mini
→
\rightarrow
Q32Bc
0.089
0.091
-1.952
0.318
0.319
-0.363
0.054
0.055
-1.694
4o-Mini
→
\rightarrow
Q72B
0.083
0.076
9.957
0.322
0.322
-0.042
0.055
0.054
0.793
4o-Mini
→
\rightarrow
4o
0.065
0.056
16.892
0.283
0.290
-2.537
0.054
0.054
-1.340
Q32Bc
→
\rightarrow
Q72B
0.127
0.124
2.270
0.315
0.316
-0.531
0.230
0.232
-0.850
Q32Bc
→
\rightarrow
4o
0.082
0.081
1.707
0.261
0.270
-3.525
0.292
0.330
-11.391
Q72B
→
\rightarrow
4o
0.061
0.061
0.776
0.280
0.287
-2.568
0.143
0.145
-1.725
Average
0.105
0.103
1.997
0.320
0.325
-1.698
0.249
0.276
-7.343
(a)
GSM8K
(b)
MedMCQA
(c)
MMLU
(d)
TriviaQA
(e)
TruthfulQA
(f)
XSum
Figure 3:
Percentage change in overall cascade loss when allowing early abstention vs only abstaining at the final model, for the Llama3.2 1B
→
\rightarrow
Llama3.1 405B cascade. The performance benefits of early abstention concentrate in the top right corner of the user preference space (blue), where the user’s sensitivity to abstention (
λ
a
\lambda_{a}
) is low to moderate and the sensitivity to cost (
λ
c
\lambda_{c}
) is moderate to high.
Early abstention reduces overall test loss.
Tables
1
and
2
show the percentage changes in overall cascade loss when allowing the small model in a two-model cascade to abstain. On six benchmarks, allowing early abstention lowers the overall cascade loss (
5
) by 2.2% on average. On five out of the six benchmarks (GSM8K, MedMCQA, MMLU, XSum, and TruthfulQA), early abstention reduces the overall loss by 3.1% on average, ranging from -1.2% on GSM8K to -7.3% on XSum. Only on TriviaQA, early abstention performed worse, raising the overall loss by 2.0%.
The benefits are concentrated in the upper right quadrant of user preference space.
Figure
3
shows heatmaps of the percentage changes in overall cascade loss across the user preference space
(
λ
cost
,
λ
abs
)
(\lambda_{\text{cost}},\lambda_{\text{abs}})
, for the cascade Llama3.2 1B
→
\rightarrow
Llama3.1 405B. The figure illustrates that the benefits of early abstention are highly concentrated in the upper right quadrant of the user preference space, where cost is a concern (
λ
c
\lambda_{c}
moderate to high) and the penalty on abstention is not severe (
λ
a
\lambda_{a}
low to moderate). This trend holds generally across cascades.
Early abstention makes more effective use of the ability to abstain.
Tables
3
and
4
show the effects of early abstention on the test error rate, expected cost, and abstention rate, broken down by benchmark and by cascade. These results show that allowing the small model in a two-model cascade to directly abstain on a query leads to significant cost reductions (-13% on average), and error reductions (-5% on average), at the expense of a moderate increase in the abstention rate (+4% on average).
2
2
2
We report the change in abstention rate as a difference rather than a percentage change because early abstention sometimes uses low amounts of abstention when final-model abstention uses none, leading to undefined percentage changes.
Our interpretation is that early abstention makes more effective use of the ability to abstain, leading a cascade to make greater use of abstention in order to improve overall performance. Appendix D provides more detailed results on the changes in the test error rate, expected cost, and abstention rate due to early abstention.
Table 3:
Early abstention trades a 4% absolute increase in the abstention rate for a 5% error reduction and 13% cost reduction, on average. Results broken down by benchmark.
Benchmark
%
𝚫
\boldsymbol{\%\Delta}
Error
%
𝚫
\boldsymbol{\%\Delta}
Cost
𝚫
\boldsymbol{\Delta}
Abstention
GSM8K
-6.763
-4.097
0.037
MedMCQA
-1.592
-11.085
0.022
MMLU
-3.175
-15.178
0.030
TriviaQA
-1.360
-7.512
0.020
TruthfulQA
-2.380
-19.713
0.025
XSum
-14.635
-20.273
0.110
Average
-4.984
-12.976
0.041
Table 4:
Early abstention trades a 4% absolute increase in the abstention rate for a 5% error reduction and 13% cost reduction, on average. Results broken down by cascade.
Cascade
%
𝚫
Error
\boldsymbol{\%\Delta\textbf{Error}}
%
𝚫
Cost
\boldsymbol{\%\Delta\textbf{Cost}}
𝚫
​
Abstention
\boldsymbol{\Delta\textbf{Abstention}}
L1B
→
\to
L3B
-3.581
-13.764
0.022
L1B
→
\to
L8B
-0.618
-12.273
0.013
L1B
→
\to
L70B
-2.483
-12.292
0.042
L1B
→
\to
L405B
-10.650
-21.361
0.112
L3B
→
\to
L8B
-2.205
-11.952
0.016
L3B
→
\to
L70B
-1.597
-12.765
0.023
L3B
→
\to
L405B
-10.352
-21.551
0.101
L8B
→
\to
L70B
-2.272
-11.803
0.020
L8B
→
\to
L405B
-9.660
-17.936
0.081
L70B
→
\to
L405B
-2.736
-12.524
0.022
4o-Mini
→
\to
Q32Bc
-5.710
-12.002
0.017
4o-Mini
→
\to
Q72B
-1.127
-7.993
0.005
4o-Mini
→
\to
4o
-3.908
-14.766
0.031
Q32Bc
→
\to
Q72B
-4.574
-0.235
0.022
Q32Bc
→
\to
4o
-9.424
-14.039
0.077
Q72B
→
\to
4o
-8.848
-10.368
0.046
Average
-4.984
-12.976
0.041
5
Conclusion
In this work, we investigated the question of early abstention in cascade design: when designing an LLM cascade capable of abstaining from difficult queries, does it make sense to allow small models earlier in the cascade to abstain, compared to only abstaining at the final model? Our results indicate that early abstention improves overall performance, as measured by a 2.2% average reduction in overall cascade loss across six language modeling benchmarks. We find that the benefits are concentrated in the upper right quadrant of the user preference space, where cost is a concern and abstention is not heavily penalized. Overall, early abstention allows a cascade to make more effective use of the ability to abstain, trading a moderate increase in the abstention rate (+4.1% on average) for significant cost savings (-13.0% on average) and some error reduction (-5.0% on average).
These positive results can be explained by the correlations between the error patterns of small and large LLMs. On one level, our findings show that these correlations can be leveraged to improve the performance of an LLM system with abstention. Viewed more broadly, an LLM cascade with early abstention is an example of an
integrated
LLM system that incorporates interactions between models to improve performance. As the LLM research community increasingly moves towards ensembles of LLMs collaborating with each other to solve tasks more efficiently and reliably, we expect that leveraging interactions between models will become critical for optimizing LLM systems.
References
Aggarwal et al.,  (2024)
Aggarwal, P., Madaan, A., Anand, A., Potharaju, S. P., Mishra, S., Zhou, P., Gupta, A., Rajagopal, D., Kappaganthu, K., Yang, Y., Upadhyay, S., Faruqui, M., and Mausam (2024).
Automix: Automatically mixing language models.
Chen et al.,  (2023)
Chen, L., Zaharia, M., and Zou, J. (2023).
Frugalgpt: How to use large language models while reducing cost and improving performance.
Chow,  (1957)
Chow, C. K. (1957).
An optimum character recognition system using decision function.
IEEE Transactions on Computers
, 6(4):247–254.
Chow,  (1970)
Chow, C. K. (1970).
On optimum recognition error and reject trade-off.
IEEE Transactions on Information Theory
, 16:41–36.
Cortes et al.,  (2016)
Cortes, C., DeSalvo, G., and Mohri, M. (2016).
Learning with rejection.
In
Algorithmic Learning Theory: 27th International Conference, ALT 2016
, pages 67–82, Bari, Italy. Springer International Publishing.
El-Yaniv and Wiener,  (2010)
El-Yaniv, R. and Wiener, Y. (2010).
On the foundations of noise-free selective classification.
Journal of Machine Learning Research
, 11:1605–1641.
Farquhar et al.,  (2024)
Farquhar, S., Kossen, J., Kuhn, L., et al. (2024).
Detecting hallucinations in large language models using semantic entropy.
Nature
, 630:625–630.
Geifman and El-Yaniv,  (2017)
Geifman, Y. and El-Yaniv, R. (2017).
Selective classification for deep neural networks.
Jitkrittum et al.,  (2024)
Jitkrittum, W., Gupta, N., Menon, A. K., Narasimhan, H., Rawat, A. S., and Kumar, S. (2024).
When does confidence-based cascade deferral suffice?
Kag et al.,  (2023)
Kag, A., Fedorov, I., Gangrade, A., Whatmough, P., and Saligrama, V. (2023).
Efficient edge inference by selective query.
In
The Eleventh International Conference on Learning Representations
.
Lin et al.,  (2024)
Lin, Z., Trivedi, S., and Sun, J. (2024).
Generating with confidence: Uncertainty quantification for black-box large language models.
Manakul et al.,  (2023)
Manakul, P., Liusie, A., and Gales, M. J. F. (2023).
Selfcheckgpt: Zero-resource black-box hallucination detection for generative large language models.
Virtanen et al.,  (2020)
Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S. J., Brett, M., Wilson, J., Millman, K. J., Mayorov, N., Nelson, A. R. J., Jones, E., Kern, R., Larson, E., Carey, C. J., Polat, İ., Feng, Y., Moore, E. W., VanderPlas, J., Laxalde, D., Perktold, J., Cimrman, R., Henriksen, I., Quintero, E. A., Harris, C. R., Archibald, A. M., Ribeiro, A. H., Pedregosa, F., van Mulbregt, P., and SciPy 1.0 Contributors (2020).
SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.
Nature Methods
, 17:261–272.
Xin et al.,  (2021)
Xin, J., Tang, R., Yu, Y., and Lin, J. (2021).
The art of abstention: Selective prediction and error regularization for natural language processing.
In Zong, C., Xia, F., Li, W., and Navigli, R., editors,
Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)
, pages 1040–1051, Online. Association for Computational Linguistics.
Yoshikawa and Okazaki,  (2023)
Yoshikawa, H. and Okazaki, N. (2023).
Selective-LAMA: Selective prediction for confidence-aware evaluation of language models.
In Vlachos, A. and Augenstein, I., editors,
Findings of the Association for Computational Linguistics: EACL 2023
, pages 2017–2028, Dubrovnik, Croatia. Association for Computational Linguistics.
Yue et al.,  (2024)
Yue, M., Zhao, J., Zhang, M., Du, L., and Yao, Z. (2024).
Large language model cascades with mixture of thoughts representations for cost-efficient reasoning.
Zellinger and Thomson,  (2025)
Zellinger, M. J. and Thomson, M. (2025).
Rational tuning of llm cascades via probabilistic modeling.
Appendix A: Modified Equations for Performance Metrics
The “rational tuning” approach towards optimizing cascade thresholds (
Zellinger and Thomson,, 2025
) relies on differentiable expressions for the probability of correctness and the expected cost. We extend this approach to include abstention, in accordance with our cascade model (
1
). The modified equations for
ℙ
⁡
(
Correct
)
\mathbb{P}(\text{Correct})
,
𝔼
⁡
[
Cost
]
\mathbb{E}[\text{Cost}]
, and
ℙ
⁡
(
Abstention
)
\mathbb{P}(\text{Abstention})
become
ℙ
⁡
(
Correct
)
=
\displaystyle\mathbb{P}(\text{Correct})=
Q
1
+
∑
i
=
2
k
P
1
​
(
∏
j
=
2
i
−
1
P
j
−
1
,
j
)
​
Q
i
−
1
,
i
\displaystyle~Q_{1}+\sum_{i=2}^{k}P_{1}\left(\prod_{j=2}^{i-1}P_{j-1,j}\right)Q_{i-1,i}
𝔼
⁡
[
Cost
]
=
\displaystyle\mathbb{E}[\text{Cost}]=
(
1
−
P
1
)
​
𝔼
​
[
C
1
]
+
∑
i
=
2
k
P
1
​
(
∏
j
=
2
i
−
1
P
j
−
1
,
j
)
​
(
1
−
P
i
−
1
,
i
)
​
(
∑
j
=
1
i
𝔼
⁡
[
C
j
]
)
\displaystyle~(1-P_{1})~\mathbb{E}[C_{1}]+\sum_{i=2}^{k}P_{1}\left(\prod_{j=2}^{i-1}P_{j-1,j}\right)(1-P_{i-1,i})\left(\sum_{j=1}^{i}\mathbb{E}[C_{j}]\right)
ℙ
⁡
(
Abstention
)
=
\displaystyle\mathbb{P}(\text{Abstention})=
ℙ
⁡
(
Φ
1
<
ξ
1
)
+
∑
i
=
2
k
P
1
​
(
∏
j
=
2
i
−
1
P
j
−
1
,
j
)
​
ℙ
​
(
Φ
i
<
ξ
i
|
Φ
i
−
1
∈
[
ξ
i
−
1
,
ϕ
i
−
1
]
)
,
\displaystyle~\mathbb{P}(\Phi_{1}<\xi_{1})+\sum_{i=2}^{k}P_{1}\left(\prod_{j=2}^{i-1}P_{j-1,j}\right)\mathbb{P}(\Phi_{i}<\xi_{i}|\Phi_{i-1}\in[\xi_{i-1},\phi_{i-1}]),
where
Q
1
:=
\displaystyle Q_{1}:=
∫
{
Φ
1
>
ϕ
1
}
Φ
1
d
ℙ
\displaystyle\int_{\{\Phi_{1}>\phi_{1}\}}\Phi_{1}\text{~d}\mathbb{P}
Q
i
,
j
:=
\displaystyle Q_{i,j}:=
∫
{
Φ
j
>
ϕ
j
}
Φ
j
(
ω
)
d
ℙ
(
ω
|
Φ
i
∈
[
ξ
i
,
ϕ
i
]
)
\displaystyle\int_{\{\Phi_{j}>\phi_{j}\}}\Phi_{j}(\omega)\text{~d}\mathbb{P}(\omega|\Phi_{i}\in[\xi_{i},\phi_{i}])
P
1
:=
\displaystyle P_{1}:=
ℙ
⁡
(
Φ
1
∈
[
ξ
1
,
ϕ
1
]
)
\displaystyle~\mathbb{P}(\Phi_{1}\in[\xi_{1},\phi_{1}])
P
i
,
j
:=
\displaystyle P_{i,j}:=
ℙ
⁡
(
Φ
j
∈
[
ξ
j
,
ϕ
j
]
|
Φ
i
∈
[
ξ
i
,
ϕ
i
]
)
,
\displaystyle~\mathbb{P}(\Phi_{j}\in[\xi_{j},\phi_{j}]~|~\Phi_{i}\in[\xi_{i},\phi_{i}]),
and
𝔼
⁡
[
C
i
]
\mathbb{E}[C_{i}]
is the expected cost per query of
M
i
M_{i}
. As in Proposition 2 of
Zellinger and Thomson, (2025)
, we let
ϕ
k
:=
−
∞
\phi_{k}:=-\infty
, even though the final model does not have a deferral threshold.
Appendix B: Logistic Regression for Abstention Prediction
To predict the final model’s decision to abstain, we fit a logistic regression model based on the earlier model’s confidence scores.
Consider a cascade
C
=
M
1
→
…
→
M
k
C=M_{1}\rightarrow...\rightarrow M_{k}
and let the observed confidence scores of the final model
M
k
M_{k}
on the training set be
{
Φ
k
(
i
)
}
i
=
1
n
\{\Phi_{k}^{(i)}\}_{i=1}^{n}
. To achieve abstention rates of 20% and 30%, we set the abstention threshold
ξ
k
\xi_{k}
to be the lower 20% and 30% quantiles of
{
Φ
k
(
i
)
}
i
=
1
n
\{\Phi_{k}^{(i)}\}_{i=1}^{n}
. Applying this abstention policy leads to abstention decisions
y
i
=
𝟙
[
Φ
k
(
i
)
<
ξ
k
]
y_{i}=\mathds{1}[\Phi_{k}^{(i)}<\xi_{k}]
for
i
=
1
,
…
,
n
i=1,...,n
. Using the
y
i
y_{i}
as ground truth labels, we fit the following logistic regression model for the probability
p
p
that the final model abstains:
log
⁡
(
p
1
−
p
)
=
β
0
+
∑
j
=
1
k
−
1
β
j
​
f
​
(
Φ
j
(
i
)
)
+
ϵ
,
\log\left(\frac{p}{1-p}\right)=\beta_{0}+\sum_{j=1}^{k-1}\beta_{j}f(\Phi_{j}^{(i)})+\epsilon,
(6)
where
f
f
is a nonlinear transformation of the confidence scores
Φ
j
(
i
)
\Phi_{j}^{(i)}
. Specifically,
f
⁡
(
Φ
j
(
i
)
)
f(\Phi_{j}^{(i)})
is the “transformed” raw confidence signal as in
Zellinger and Thomson, (2025)
. For example, on multiple-choice QA benchmarks,
f
⁡
(
Φ
)
=
log
⁡
(
1
1
−
p
raw
)
,
f(\Phi)=\log\left(\frac{1}{1-p_{\text{raw}}}\right),
(7)
where
p
raw
p_{\text{raw}}
is maximum conditional next-token probability among the valid answer choices (e.g., “A”, “B”, “C”, or “D” on MMLU).
Appendix C: Smoothing Procedure for Optimal Cascade Thresholds
We apply light smoothing on the grid of optimal cascade thresholds to avoid potential artifacts from numerical optimization. Our procedure consists of two steps:
•
Step 1: Identify outliers
•
Step 2: Replace outliers by the mean values of their neighbors
In Step 1, we call a threshold vector
𝜽
\boldsymbol{\theta}
an
outlier
if
θ
¯
:=
∑
i
=
1
n
θ
i
\overline{\theta}:=\sum_{i=1}^{n}\theta_{i}
satisfies
(
θ
¯
−
1
|
N
|
​
∑
n
∈
N
θ
n
¯
)
2
>
r
​
Var
​
(
θ
n
¯
,
n
∈
N
)
,
(\overline{\theta}-\frac{1}{|N|}\sum_{n\in N}\overline{\theta_{n}})^{2}>r\text{Var}(\overline{\theta_{n}},n\in N),
(8)
where
n
∈
N
n\in N
indexes the set of neighboring optimal thresholds on the 2D grid (an interior point has four neighbors).
Reported results in the paper use
r
=
10
r=10
. This results in smoothing 3.5% of data points for early abstention and 2.7% of data points for final-model abstention.
Appendix D: Detailed Changes in Error, Cost, and Abstention
Below we provide detailed results on the changes in the test error rate (Table
5
), expected cost (Table
6
), and abstention rate (Table
7
) resulting from using early abstention, compared to abstaining only at the final model.
Table 5:
Change in
error rate
on the test set when using early abstention (“Early”) compared to final-model abstention (“Final”). Bolded numbers indicate outperformance.
Cascade
GSM8K
MedMCQA
MMLU
TriviaQA
TruthfulQA
XSum
Average
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
L1B
→
\rightarrow
L3B
0.168
0.174
-3.108
0.228
0.225
1.620
0.203
0.214
-5.281
0.177
0.182
-2.755
0.248
0.246
0.810
0.148
0.170
-12.773
0.195
0.202
-3.581
L1B
→
\rightarrow
L8B
0.130
0.131
-0.368
0.239
0.240
-0.266
0.171
0.173
-1.265
0.130
0.136
-4.117
0.279
0.275
1.264
0.189
0.187
1.044
0.190
0.190
-0.618
L1B
→
\rightarrow
L70B
0.045
0.047
-3.877
0.187
0.186
0.355
0.111
0.111
-0.048
0.055
0.055
0.267
0.221
0.226
-2.175
0.110
0.122
-9.421
0.122
0.125
-2.483
L1B
→
\rightarrow
L405B
0.022
0.027
-19.898
0.177
0.184
-3.992
0.093
0.092
0.425
0.039
0.040
-0.878
0.185
0.193
-4.365
0.085
0.131
-35.191
0.100
0.111
-10.650
L3B
→
\rightarrow
L8B
0.159
0.169
-5.530
0.240
0.246
-2.399
0.174
0.176
-0.987
0.137
0.138
-0.543
0.263
0.270
-2.539
0.188
0.191
-1.235
0.194
0.198
-2.205
L3B
→
\rightarrow
L70B
0.077
0.079
-2.704
0.192
0.190
1.061
0.112
0.111
1.201
0.056
0.055
0.561
0.223
0.227
-1.617
0.109
0.119
-8.083
0.128
0.130
-1.597
L3B
→
\rightarrow
L405B
0.132
0.150
-11.961
0.190
0.204
-6.860
0.094
0.096
-2.441
0.040
0.040
0.334
0.185
0.196
-5.355
0.093
0.145
-35.832
0.122
0.138
-10.352
L8B
→
\rightarrow
L70B
0.068
0.068
-0.726
0.203
0.197
3.173
0.115
0.116
-1.131
0.061
0.063
-3.258
0.222
0.226
-1.468
0.116
0.129
-10.222
0.131
0.133
-2.272
L8B
→
\rightarrow
L405B
0.099
0.105
-5.294
0.206
0.217
-5.216
0.095
0.099
-3.848
0.045
0.046
-1.356
0.183
0.200
-8.456
0.138
0.209
-33.793
0.128
0.146
-9.660
L70B
→
\rightarrow
L405B
0.046
0.046
0.305
0.193
0.197
-2.343
0.099
0.099
-0.259
0.049
0.047
3.788
0.197
0.200
-1.552
0.112
0.134
-16.357
0.116
0.121
-2.736
4o-Mini
→
\rightarrow
Q32Bc
0.047
0.051
-8.602
0.201
0.203
-0.721
0.160
0.159
0.406
0.062
0.069
-10.337
0.237
0.244
-2.602
0.022
0.025
-12.404
0.122
0.125
-5.710
4o-Mini
→
\rightarrow
Q72B
0.050
0.053
-4.445
0.200
0.199
0.455
0.138
0.135
1.878
0.057
0.056
0.963
0.241
0.242
-0.671
0.024
0.025
-4.941
0.118
0.118
-1.127
4o-Mini
→
\rightarrow
4o
0.058
0.067
-13.938
0.153
0.155
-1.153
0.107
0.108
-1.229
0.038
0.038
2.280
0.204
0.209
-2.449
0.020
0.022
-6.962
0.097
0.100
-3.908
Q32Bc
→
\rightarrow
Q72B
0.042
0.049
-14.945
0.195
0.196
-0.644
0.137
0.137
0.109
0.076
0.077
-1.301
0.219
0.222
-1.486
0.061
0.067
-9.177
0.122
0.125
-4.574
Q32Bc
→
\rightarrow
4o
0.048
0.049
-1.889
0.142
0.148
-3.676
0.158
0.186
-15.105
0.022
0.023
-2.698
0.163
0.167
-2.615
0.115
0.165
-30.562
0.108
0.123
-9.424
Q72B
→
\rightarrow
4o
0.037
0.041
-11.229
0.162
0.171
-4.863
0.126
0.165
-23.230
0.031
0.032
-2.710
0.175
0.180
-2.803
0.039
0.043
-8.251
0.095
0.105
-8.848
Average
0.077
0.082
-6.763
0.194
0.197
-1.592
0.131
0.136
-3.175
0.067
0.069
-1.360
0.215
0.220
-2.380
0.098
0.118
-14.635
0.130
0.137
-4.984
Table 6:
Change in
expected cost
on the test set when using early abstention (“Early”) compared to final-model abstention (“Final”). Bolded numbers indicate outperformance.
Cascade
GSM8K
MedMCQA
MMLU
TriviaQA
TruthfulQA
XSum
Average
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
Early
Final
%
𝚫
\boldsymbol{\%\Delta}
L1B
→
\rightarrow
L3B
71.601
73.988
-3.226
31.986
33.354
-4.102
34.008
37.118
-8.379
14.860
16.966
-12.417
15.373
19.043
-19.269
86.081
132.816
-35.188
42.318
52.214
-13.764
L1B
→
\rightarrow
L8B
104.607
111.371
-6.073
47.126
49.997
-5.741
50.688
55.466
-8.614
23.236
25.642
-9.382
23.479
30.187
-22.221
159.931
204.010
-21.606
68.178
79.445
-12.273
L1B
→
\rightarrow
L70B
354.301
380.237
-6.821
155.516
165.923
-6.272
162.822
185.591
-12.268
80.017
84.741
-5.574
79.822
101.761
-21.559
550.516
699.117
-21.256
230.499
269.562
-12.292
L1B
→
\rightarrow
L405B
980.892
1192.188
-17.723
441.203
507.625
-13.085
456.881
561.538
-18.638
253.605
275.737
-8.026
245.452
322.141
-23.806
1144.376
2154.710
-46.890
587.068
835.657
-21.361
L3B
→
\rightarrow
L8B
52.641
56.314
-6.523
39.131
42.783
-8.536
44.607
50.427
-11.541
24.214
25.324
-4.382
22.071
28.303
-22.017
164.680
202.595
-18.715
57.891
67.624
-11.952
L3B
→
\rightarrow
L70B
245.738
257.410
-4.534
132.535
145.584
-8.963
145.695
171.722
-15.156
81.480
84.531
-3.609
77.356
100.440
-22.983
546.826
695.215
-21.344
204.938
242.483
-12.765
L3B
→
\rightarrow
L405B
266.372
319.065
-16.515
354.817
413.319
-14.154
386.859
495.710
-21.959
260.629
274.757
-5.142
239.152
319.538
-25.157
1112.024
2073.907
-46.380
436.642
649.383
-21.551
L8B
→
\rightarrow
L70B
297.188
299.470
-0.762
140.904
154.070
-8.546
144.409
171.579
-15.835
89.032
92.948
-4.213
90.105
113.664
-20.727
541.207
682.801
-20.737
217.141
252.422
-11.803
L8B
→
\rightarrow
L405B
378.868
386.338
-1.934
344.400
393.865
-12.559
345.498
458.153
-24.589
232.487
238.229
-2.410
250.111
334.041
-25.126
784.729
1330.056
-41.000
389.349
523.447
-17.936
L70B
→
\rightarrow
L405B
360.270
375.946
-4.170
341.569
368.177
-7.227
280.033
394.310
-28.982
124.742
134.139
-7.005
280.365
337.100
-16.830
758.173
851.186
-10.927
357.525
410.143
-12.524
4o-Mini
→
\rightarrow
Q32Bc
305.301
317.501
-3.843
80.971
97.703
-17.125
105.827
113.517
-6.774
17.863
21.886
-18.381
54.924
67.327
-18.422
173.952
187.989
-7.467
123.140
134.320
-12.002
4o-Mini
→
\rightarrow
Q72B
237.061
230.590
2.806
104.568
112.711
-7.225
106.761
113.088
-5.594
22.287
26.170
-14.836
58.558
69.758
-16.055
182.660
196.515
-7.051
118.649
124.805
-7.993
4o-Mini
→
\rightarrow
4o
292.712
319.961
-8.516
221.225
254.593
-13.106
181.611
233.275
-22.147
45.837
53.248
-13.919
195.566
249.827
-21.719
269.220
296.455
-9.187
201.029
234.560
-14.766
Q32Bc
→
\rightarrow
Q72B
429.898
363.289
18.335
256.089
275.515
-7.051
254.571
261.253
-2.557
149.262
151.646
-1.572
136.128
143.954
-5.437
1119.445
1155.584
-3.127
390.899
391.873
-0.235
Q32Bc
→
\rightarrow
4o
367.540
372.570
-1.350
468.630
552.128
-15.123
180.103
264.787
-31.982
283.386
297.182
-4.642
310.432
381.989
-18.733
1423.186
1624.714
-12.404
505.546
582.228
-14.039
Q72B
→
\rightarrow
4o
349.557
366.776
-4.695
255.560
357.690
-28.553
174.184
188.993
-7.836
134.595
141.211
-4.686
328.934
388.573
-15.348
751.315
759.613
-1.092
332.358
367.143
-10.368
Average
318.409
338.938
-4.097
213.514
245.315
-11.085
190.910
234.783
-15.178
114.846
121.522
-7.512
150.489
187.978
-19.713
610.520
827.955
-20.273
266.448
326.082
-12.976
Table 7:
Change in
abstention rate
on the test set when using early abstention (“Early”) compared to final-model abstention (“Final”). Bolded numbers indicate outperformance.
Cascade
GSM8K
MedMCQA
MMLU
TriviaQA
TruthfulQA
XSum
Average
Early
Final
𝚫
\boldsymbol{\Delta}
Early
Final
𝚫
\boldsymbol{\Delta}
Early
Final
𝚫
\boldsymbol{\Delta}
Early
Final
𝚫
\boldsymbol{\Delta}
Early
Final
𝚫
\boldsymbol{\Delta}
Early
Final
𝚫
\boldsymbol{\Delta}
Early
Final
𝚫
\boldsymbol{\Delta}
L1B
→
\rightarrow
L3B
0.129
0.094
0.035
0.428
0.428
-0.000
0.434
0.409
0.025
0.407
0.362
0.045
0.593
0.594
-0.001
0.806
0.777
0.029
0.466
0.444
0.022
L1B
→
\rightarrow
L8B
0.126
0.127
-0.001
0.399
0.396
0.004
0.394
0.384
0.010
0.229
0.186
0.043
0.481
0.480
0.001
0.525
0.501
0.023
0.359
0.346
0.013
L1B
→
\rightarrow
L70B
0.089
0.040
0.048
0.201
0.188
0.013
0.239
0.222
0.017
0.092
0.062
0.030
0.408
0.390
0.018
0.264
0.138
0.126
0.215
0.173
0.042
L1B
→
\rightarrow
L405B
0.195
0.058
0.137
0.201
0.150
0.051
0.252
0.181
0.071
0.095
0.041
0.054
0.340
0.298
0.042
0.488
0.169
0.319
0.262
0.150
0.112
L3B
→
\rightarrow
L8B
0.119
0.089
0.031
0.410
0.395
0.015
0.387
0.381
0.006
0.196
0.185
0.011
0.485
0.473
0.012
0.522
0.501
0.020
0.353
0.337
0.016
L3B
→
\rightarrow
L70B
0.058
0.029
0.028
0.200
0.208
-0.008
0.235
0.235
0.000
0.084
0.079
0.005
0.403
0.392
0.011
0.267
0.164
0.103
0.208
0.184
0.023
L3B
→
\rightarrow
L405B
0.122
0.016
0.106
0.180
0.109
0.071
0.251
0.174
0.076
0.073
0.060
0.014
0.345
0.290
0.055
0.483
0.200
0.283
0.242
0.142
0.101
L8B
→
\rightarrow
L70B
0.021
0.024
-0.002
0.186
0.209
-0.023
0.232
0.242
-0.011
0.064
0.018
0.047
0.410
0.399
0.010
0.256
0.159
0.097
0.195
0.175
0.020
L8B
→
\rightarrow
L405B
0.050
0.019
0.030
0.166
0.112
0.054
0.239
0.190
0.049
0.038
0.021
0.017
0.348
0.270
0.078
0.379
0.124
0.254
0.203
0.123
0.081
L70B
→
\rightarrow
L405B
0.008
0.011
-0.002
0.122
0.097
0.025
0.192
0.189
0.003
0.022
0.042
-0.021
0.325
0.302
0.023
0.152
0.048
0.105
0.137
0.115
0.022
4o-Mini
→
\rightarrow
Q32Bc
0.048
0.003
0.045
0.280
0.278
0.002
0.158
0.157
0.000
0.077
0.071
0.006
0.294
0.273
0.021
0.044
0.019
0.025
0.150
0.134
0.017
4o-Mini
→
\rightarrow
Q72B
0.026
0.012
0.014
0.216
0.214
0.002
0.107
0.105
0.002
0.067
0.070
-0.003
0.294
0.288
0.007
0.014
0.004
0.010
0.121
0.115
0.005
4o-Mini
→
\rightarrow
4o
0.070
0.005
0.065
0.201
0.179
0.022
0.182
0.156
0.025
0.052
0.039
0.013
0.235
0.203
0.032
0.032
0.001
0.031
0.128
0.097
0.031
Q32Bc
→
\rightarrow
Q72B
0.035
0.000
0.034
0.270
0.258
0.011
0.153
0.154
-0.002
0.145
0.126
0.019
0.365
0.357
0.008
0.097
0.039
0.059
0.177
0.156
0.022
Q32Bc
→
\rightarrow
4o
0.001
0.000
0.001
0.259
0.203
0.056
0.211
0.128
0.082
0.110
0.069
0.042
0.295
0.245
0.050
0.238
0.007
0.231
0.186
0.109
0.077
Q72B
→
\rightarrow
4o
0.027
0.004
0.023
0.254
0.205
0.049
0.148
0.027
0.121
0.057
0.049
0.008
0.293
0.256
0.037
0.040
0.000
0.040
0.136
0.090
0.046
Average
0.070
0.033
0.037
0.248
0.227
0.022
0.238
0.208
0.030
0.113
0.092
0.020
0.369
0.344
0.025
0.288
0.178
0.110
0.221
0.181
0.041