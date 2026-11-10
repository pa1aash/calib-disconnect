---
title: 'AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code
  Generation'
id: adadec-a-uncertainty-guided-lookahead-decoding-framework-for-llm-based-code-gene
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:09:17.773936Z'
updated: '2026-11-09T23:27:44.641888Z'
source: https://arxiv.org/html/2506.08980
source_domain: arxiv.org
fetched_at: '2026-11-09T23:09:17.773430Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: AdaDec, arXiv 2506.08980, FULL TEXT (HTML note; short duplicate 250608980-...
  exists). Entropy-triggered pause-then-rerank lookahead decoding with learned model-specific
  thresholds; empirical study shows Spearman rho 0.4595-0.5249 between token entropy
  and ground-truth token rank across DeepSeek-Coder, StableCode, Qwen2.5, Qwen3 models
  (Table 1). Improves Pass@1 by up to 20.9% absolute over greedy on HumanEval+, MBPP+,
  DevEval. About decoding, not confidence calibration; at most a related token-level
  uncertainty use for L4-style localization of uncertain decision points.
---

AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code Generation
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2506.08980v5 [cs.SE] 24 Apr 2026
AdaDec: A Uncertainty-Guided Lookahead Decoding Framework for LLM-Based Code Generation
DOI:
10.1145/3808142
Journal:
PACMSE
Volume:
3
FSE
FSE135
7
fse26mainb-p469-p
CCS:
Software and its engineering Automatic programming
Kaifeng He
Affiliation:
Sun Yat-sen University
,
Zhuhai
,
China
email:
hekaifeng70@gmail.com
,
Mingwei Liu
Affiliation:
Sun Yat-sen University
,
Zhuhai
,
China
email:
liumw26@mail.sysu.edu.cn
,
Chong Wang
Affiliation:
Nanyang Technological University
,
Singapore
,
Singapore
email:
chong.wang@ntu.edu.sg
,
Zike Li
Affiliation:
Sun Yat-sen University
,
Zhuhai
,
China
email:
lizk8@mail2.sysu.edu.cn
,
Yanlin Wang
Affiliation:
Sun Yat-sen University
,
Zhuhai
,
China
email:
yanlin-wang@outlook.com
,
Xin Peng
Affiliation:
Fudan University
,
Shanghai
,
China
email:
pengxin@fudan.edu.cn
and
Zibin Zheng
Affiliation:
Sun Yat-sen University
,
Zhuhai
,
China
email:
zhzibin@mail.sysu.edu.cn
Received  2026-03-24
Abstract.
Code generation with large language models (LLMs) is highly sensitive to token selection during decoding, particularly at uncertain decision points that influence program logic. While standard strategies such as greedy decoding treat all tokens uniformly, they overlook code-specific uncertainty patterns, leading to suboptimal performance. This paper presents an empirical study revealing that many generation errors stem from token ranking mistakes at high-uncertainty steps, where the correct token is present but not top-ranked.
Motivated by these findings, we propose
AdaDec
, a lookahead-based uncertainty-guided adaptive decoding framework that integrates a token-level
pause-then-rerank
mechanism driven by token uncertainty.
AdaDec
learns model-specific uncertainty thresholds and applies a lookahead-based reranking strategy when uncertainty is high.
Experiments on HumanEval+, MBPP+, and DevEval benchmarks show that
AdaDec
improves Pass@1 accuracy by up to 20.9% in absolute terms over greedy decoding. More importantly, it consistently outperforms both competitive baselines like Beam Search and state-of-the-art adaptive decoding methods such as AdapT, while maintaining high efficiency through selective, uncertainty-triggered pausing.
Our results highlight the promise of uncertainty-aware adaptive decoding for improving both the reliability and efficiency of LLM-based code generation.
Keywords:
Code Generation, Adaptive Strategy, Language Model
†
†
cc-license:
by
†
†
authorsaddresses:
⋆
Corresponding authors: Mingwei Liu and Chong Wang.
Kaifeng He, Mingwei Liu, Zike Li, Yanlin Wang, and Zibin Zheng are with the School of Software Engineering and the Zhuhai Key Laboratory of Trusted Large Language Models, Sun Yat-sen University, Zhuhai, China.
Email: hekaifeng70@gmail.com, liumw26@mail.sysu.edu.cn, lizk8@mail2.sysu.edu.cn, yanlin-wang@outlook.com, zhzibin@mail.sysu.edu.cn.
Chong Wang is with Nanyang Technological University, Singapore.
Email: chong.wang@ntu.edu.sg.
Xin Peng is with Fudan University, Shanghai, China.
Email: pengxin@fudan.edu.cn.
1.
Introduction
Large language models (LLMs) have significantly advanced the field of code generation by learning expressive representations of programming syntax and semantics from large-scale corpora of source code and documentation
(
Li et al., 2023
;
Di and Zhang, 2025
;
Tian et al., 2024
;
Jiang et al., 2025
;
Lin et al., 2024
;
Cao et al., 2026
)
. Models such as CodeLlama
(
Rozière et al., 2024
)
and DeepSeek-Coder
(
Guo et al., 2024
)
—pre-trained on billions of lines of code—exhibit strong capabilities in producing syntactically correct and context-aware code snippets from natural language prompts
(
Yuan et al., 2023
;
Sun et al., 2024
;
Ugare et al., 2024
;
Li et al., 2025
)
. These capabilities have catalyzed a range of intelligent software engineering tasks, including code completion, automated bug fixing
(
Fu et al., 2022
;
Jin et al., 2023
;
Xia and Zhang, 2022
)
, and test-case generation, ultimately reducing developer effort and accelerating the software development process
(
Jiang et al., 2024
;
Huynh and Lin, 2025
;
Liu et al., 2026
)
.
At the core of code generation with large language models (LLMs) lies the decoding process, which translates learned latent representations into discrete, executable token sequences
(
Chen et al., 2021
)
. Decoding for code generation, however, faces domain-specific challenges. Code exhibits distinctive patterns of token uncertainty: certain tokens (e.g., identifiers or control keywords at the start of a line) are intrinsically ambiguous because their correct choice depends on
future logic
, while others (e.g., syntactically constrained keywords or repeated identifiers) are relatively deterministic. Crucially, mistakes at a few high-uncertainty points can yield irreversible semantic errors (for example, selecting “for” versus “return” at line start fundamentally alters control flow). Figure
1
provides an example. Therefore, the choice of decoding strategy—how the next token is selected or processed—plays a decisive role in balancing efficiency, diversity, and reliability.
Figure 1.
Illustration of irreversible semantic errors in code due to high-uncertainty points.
A range of strategies have been proposed: deterministic greedy decoding
(
Radford et al., 2019
)
is simple and efficient but prone to premature commitment to suboptimal tokens;
beam search
(
Freitag and Al-Onaizan, 2017
)
improves results by maintaining multiple candidates but incurs high computational overhead;
sampling-based approaches such as top-
k
k
(
Holtzman et al., 2020
)
and nucleus (top-
p
p
)
(
Holtzman et al., 2020
)
sampling enhance diversity but often introduce syntactic or semantic errors that are unacceptable for code; and uncertainty-based methods aim to exploit token-level difficulty signals. For instance, AdapT
(
Zhu et al., 2023
)
estimates uncertainty by computing cross-entropy loss between model predictions and ground truth tokens, finding that tokens with higher loss values tend to cluster at line starts. Based on this
pre-identified
pattern rather than dynamic signals during decoding, AdapT assigns higher temperatures to line-initial tokens, but its reliance on randomness makes gains unstable and limited. By contrast, Uncert-CoT
(
Zhu et al., 2025
)
dynamically measures uncertainty at decoding time, employing Shannon entropy
(
Shannon, 1948
)
or probability difference (the gap between the top-1 and top-2 token probabilities) to decide whether a line-initial token is highly uncertain, in which case single-line chain-of-thought reasoning is triggered. While this avoids uniform treatment of all line starts, it overlooks uncertain tokens beyond line boundaries and has shown only marginal improvements in practice. Overall, existing methods either treat all decoding steps uniformly or rely on coarse heuristics tied to line structure, and current uncertainty-based decoding approaches have not yet explored which uncertainty signals are most appropriate to guide intervention at decoding time.
To address this gap, we conduct an empirical study to better understand token-level uncertainty during the decoding process in LLM-based code generation. Using DeepSeek-Coder
(
Guo et al., 2024
)
and the HumanEval dataset
(
Chen et al., 2021
)
, we analyze decoding failures by comparing model predictions that fail test cases with their corresponding ground-truth solutions.
Finding 1
: The analysis reveals that many errors stem from local ranking mistakes—where the correct token exists in the candidate set but is not ranked first—thereby causing logic drift. To further investigate this phenomenon, we perform next-token prediction on 164 HumanEval problems, recording decoding information and the rank of the ground-truth token at each step. This enables us to statistically identify the locations of logic drift points and analyze the relationship between logic drift and entropy.
Finding 2
: The results suggest that entropy can serve as a useful signal for detecting logic drift and guiding adaptive pausing and reranking. However, due to variability across models, a fixed entropy threshold is suboptimal, highlighting the need for a dynamic, model-aware thresholding mechanism.
Based on these findings, we introduce
AdaDec
, an uncertainty-guided adaptive decoding framework for code generation with large language models.
AdaDec
enhances standard decoding (e.g., greedy decoding, sampling) by incorporating a
pause-then-rerank
mechanism that reacts to model uncertainty, measured by Shannon entropy at each step. When uncertainty exceeds a threshold, decoding is paused and a reranking procedure is triggered. Because a fixed threshold does not generalize well across different models,
AdaDec
learns this threshold through a data-driven logistic regression approach. During reranking,
AdaDec
selects the top candidate tokens and evaluates them using a lookahead strategy inspired by A* search heuristics and a prior constrained generation method
(
Lu et al., 2021
)
, scoring each candidate based on expected future continuations. The highest-scoring token is chosen for generation, and the process repeats until the sequence is complete. In contrast to prior approaches that either treat all decoding steps uniformly or rely on coarse heuristics tied to line structure,
AdaDec
systematically explores Shannon entropy as a token-level uncertainty signal and applies dynamic, token-level intervention across both line-initial and in-line tokens only at high-uncertainty steps, addressing the identified gap and enabling targeted correction of the most consequential decision points.
We conduct extensive experiments on the HumanEval+, MBPP+ and DevEval benchmarks using models ranging from 0.6B to 8B parameters. Our uncertainty-guided adaptive decoding framework,
AdaDec
, consistently improves Pass1 accuracy by up to 20.9% over Greedy decoding and consistently outperforms state-of-the-art adaptive decoding methods such as AdapT. In practice,
AdaDec
selectively pauses decoding at a low rate (averaging 6.75%), and the targeted lookahead introduces moderate additional latency, effectively balancing quality and efficiency. Ablation studies confirm that the learned entropy threshold accurately identifies uncertain decoding steps, and empirical comparisons show that using the learned threshold outperforms a fixed threshold, particularly for models where the fixed threshold deviates substantially from the learned value. Overall,
AdaDec
generalizes well across model scales and datasets, significantly improving code generation accuracy without incurring excessive runtime overhead.
In summary, this paper makes the following contributions:
•
An empirical study that reveals many code generation errors arise from local token ranking mistakes, not only occurring at line beginnings but also sometimes within lines, and that Shannon entropy serves as a useful signal for detecting uncertain decoding steps prone to logic drift.
•
An adaptive decoding framework,
AdaDec
, which employs an entropy-guided pause-then-rerank mechanism with learned, model-specific thresholds and a lookahead strategy to improve generation quality.
•
Experimental results that show
AdaDec
improves Pass@1 accuracy by up to 20.9% over Greedy decoding, achieves high efficiency by selectively pausing decoding at a low rate, and generalizes effectively across diverse model sizes and benchmark datasets.
2.
Empirical Study
We conduct an empirical study to investigate the characteristics of token uncertainty in LLM-based code generation and analyze the feasibility of integrating token uncertainty into decoding process. Specifically, the study aims to answer the following research questions:
•
RQ1:
Where do logic drifts occur in code, and how are they influenced by token uncertainty?
•
RQ2:
How can token uncertainty be leveraged to improve token selection during decoding?
2.1.
Study Setup
2.1.1.
Models
To ensure the generality of our findings, we conduct our study on a diverse set of open-source models ranging from 0.6B to 8B parameters, accessed via Hugging Face. These encompass various architectures and instruction-tuning schemes. Specifically, we include code-specialized models: DeepSeek-Coder-1.3B/6.7B-Instruct (DS-1.3B, DS-6.7B)
(
Guo et al., 2024
)
, StableCode-Instruct-3B (ST-3B)
(
Pinnaparaju et al., 2023
)
, and Qwen2.5-Coder-1.5B/7B-Instruct (QW2.5-1.5B, QW2.5-7B)
(
Hui et al., 2024
)
. We also include general-purpose models featuring dynamic reasoning capabilities: the Qwen3 family, including the 0.6B (QW3-0.6B), 1.7B (QW3-1.7B), 4B (QW3-4B), and 8B (QW3-8B) variants
(
Team, 2025
)
.
2.1.2.
Implementation
Our implementation is built with PyTorch and the Hugging Face Transformers library. Decoding is performed without batching (i.e., using a batch size of 1) to ensure independent processing of each instance. The maximum generation length is capped at 1,024 tokens for all methods to enable fair comparison across models.
Experiments are conducted on a machine equipped with NVIDIA RTX 5880 Ada Generation GPUs (48 GB VRAM each) and an NVIDIA A100 GPU (80 GB VRAM), supported by NVIDIA Driver 550.163.01 and CUDA 12.4.
2.2.
RQ1: Where do logic drifts occur in code, and how are they influenced by token uncertainty?
To address this research question, we first use DS-6.7B as a representative model to generate code for 164 programming problems in the widely used HumanEval dataset
(
Chen et al., 2021
)
. We begin by analyzing the locations of
logic drifts
—points during decoding where the generated sequence diverges from the correct solution—which often lead to incorrect program behavior. We then investigate how token-level uncertainty, quantified using Shannon entropy
(
Shannon, 1948
)
, relates to the occurrence of such drifts.
2.2.1.
Method
For each programming problem in the HumanEval dataset, we use DS-6.7B to generate code snippets using a greedy decoding strategy.
We then filter out the generations that successfully pass all test cases. Based on an initial human analysis, we observe that in several cases, the model begins with a correct sequence but introduces a critical error—often in the form of incorrect code structures—at a specific step. For example, instead of generating a
for
loop to iterate over remaining elements, the model might incorrectly rank the
return
token at the top position, prematurely terminating the control flow. At these error points, the correct next token is not missing from the candidate set but is ranked below the top-1 position (commonly second or third), resulting in an irreversible deviation from the correct logic. This suggests that some generation failures are caused by local ranking errors at specific decoding steps, ultimately leading to incorrect code behavior. We refer to such steps as logic
drift points
during decoding and aim to identify them.
Given the high cost of fully manual annotation, we develop a semi-automatic approach that combines abstract syntax tree (AST) comparison with human verification and fine-grained token-level annotation. To ensure annotation focuses only on faulty generations, we first filter out all generated samples that can pass the tests. Subsequently, we construct ASTs for both the ground-truth and generated code, and normalize them by removing identifiers and comments. This normalization ensures that the comparison focuses solely on structural differences. We then perform a parallel traversal to compare the two normalized ASTs node by node. For instance, a structural discrepancy is flagged when:
(1)
control-flow node types differ (e.g.,
if
vs.
for
);
(2)
relational or boolean operators differ (e.g.,
>
vs.
>=
);
(3)
loop or branching boundaries diverge;
(4)
indentation-aligned block structures differ.
Any identified mismatch is traced back to its corresponding line in the original code and extracted as a candidate drift point.
For each candidate line, we further determine whether the drift occurs at the beginning of the line and record this for statistical analysis. Finally, each candidate is reviewed by a human annotator to confirm the validity of the drift and to annotate the precise start token. To ensure consistency, annotators adhered to the following explicit guidelines:
(i)
focus strictly on structural (AST-level) differences;
(ii)
ignore lexical or superficial variations (e.g., variable names, comments);
(iii)
label the earliest divergence point;
(iv)
treat alternative valid implementations as non-drift unless the semantics fundamentally change.
For instance, a mismatch between the generated line
if shift > len(s):
and the ground-truth line
if shift >= len(digits):
triggers a drift point at the position of the operator
>=
.
In addition to the identified drift points, we collect all other non-drift decoding steps from the same generated code snippets. We compute the Shannon entropy for each step and compare the entropy distribution of drift points with that of non-drift steps. This comparison allows us to investigate the relationship between logic drift and token uncertainty, as measured by Shannon entropy. Given a probability distribution
𝒑
\bm{p}
, the corresponding entropy
H
⁡
(
𝒑
)
H(\bm{p})
is calculated as follows:
H
(
𝒑
)
=
−
∑
p
i
∈
𝒑
p
i
log
p
i
H(\bm{p})=-\sum_{p_{i}\in\bm{p}}p_{i}\log p_{i}
2.2.2.
Results
We identify a total of 46 drift points and 2,889 non-drift decoding steps across 46 HumanEval problems. Statistical analysis shows that divergences at line start account for 86.96% of all drift points, while 13.04% occur within lines. This observation suggests that focusing solely on line-initial tokens for uncertainty-based intervention is insufficient, as it ignores more than 10% of logic drift points. Figure
2
presents a boxplot comparing the entropy distribution at drift points with that of all non-drift steps. For clarity, outliers are omitted in boxplots. The entropy values at drift points are markedly higher: the median entropy is 1.26, with a mean of 1.39, compared to a much lower median of 0.03 and mean of 0.30 for the rest. The interquartile range (IQR) for drift points is also shifted higher (0.63–2.01) relative to that of non-drift steps (0.003–0.34). The results show that tokens at drift points exhibit significantly higher entropy values compared to the rest, suggesting a clear relationship between entropy and logic drift.
Figure 2.
Entropy comparison between drift points and non-drift decoding steps.
Finding 1:
This empirical pattern indicates that focusing solely on line-start tokens for uncertainty-based intervention is insufficient, motivating the search for a suitable uncertainty signal that monitors all tokens and triggers targeted intervention at high-uncertainty steps. Subsequent analysis shows that token uncertainty measured by Shannon entropy is strongly correlated with logic drift, providing a useful signal for identifying potential drift points and predicting code behavior deviations during decoding.
2.3.
RQ2: How can token uncertainty be leveraged to improve token selection during decoding?
To integrate token uncertainty into the token selection process and enhance the likelihood of generating correct code, we further investigate the relationship between entropy and the rank positions of expected tokens during decoding.
2.3.1.
Method
We perform next-token prediction using 164 problems and their corresponding ground-truth solutions from the HumanEval dataset. Specifically, given a problem
P
P
and its ground-truth solution
S
S
, we tokenize them into sequences
T
P
\mathrm{T}^{P}
and
T
S
\mathrm{T}^{S}
, respectively. At each decoding step
k
k
, we feed the concatenated sequence
T
P
⊕
T
S
:
k
\mathrm{T}^{P}\oplus\mathrm{T}^{S}_{:k}
into the LLM to obtain a probability distribution over the next token. Here,
T
S
:
k
\mathrm{T}^{S}_{:k}
denotes the prefix of the ground-truth solution containing the first
k
k
tokens, and
⊕
\oplus
indicates sequence concatenation. By iterating over all positions
k
k
from 1 to the length of
T
S
\mathrm{T}^{S}
, we collect a set of predicted probability distributions. For each prediction, we compute the Shannon entropy of the distribution and record the rank of the expected (ground-truth) token within it.
We apply this next-token prediction procedure to a range of open-source LLMs, including five code-specific models, DS-1.3B, DS-6.7B, ST-3B, QW2.5-1.5B, and QW2.5-7B, as well as four general-purpose models: QW3-0.6B, QW3-1.7B, QW3-4B, and QW3-8B.
For Qwen3, we disable the reasoning-specific settings (e.g., thinking mode).
In total, we collect 180,879 token-level probability distributions for two DeepSeek-Coder models, 169,496 for StableCode, and 129,165 for Qwen series.
2.3.2.
Results
We compute the Spearman correlation between entropy and the rank of the ground-truth token across all models. As shown in Table
1
, the results consistently exhibit a positive correlation, further reinforcing the notion that entropy serves as a meaningful signal for identifying uncertain decoding steps. We omit p-values from the table, as the large sample sizes (approximately 130,000 to 180,000 tokens per model) yield statistically significant results with p-values effectively indistinguishable from zero.
Table 1.
Spearman correlation
𝝆
\bm{\rho}
between entropy and the rank of ground-truth tokens.
Model
DS-1.3B
DS-6.7B
ST-3B
QW2.5-1.5B
QW2.5-7B
QW3-0.6B
QW3-1.7B
QW3-4B
QW3-8B
𝝆
\bm{\rho}
0.4728
0.4595
0.4620
0.4906
0.4755
0.5249
0.5028
0.4936
0.4877
Figure
4
shows how the percentage of decoding steps with entropy exceeding a given threshold changes as the threshold increases. Figure
4
illustrates the corresponding change in the average rank of ground-truth tokens, separated by whether the entropy at each step is above or below the threshold. These plots reveal that different models exhibit varying sensitivity to entropy thresholds. For example, at a threshold of 1.2, QW3-0.6B has approximately 13% of decoding steps exceeding the threshold, while other models remain below 10%. In terms of average rank, two models (DS-6.7B and QW3-1.7B) exceed a value of 5.5, and the rest fall in the range of 3.5 to 4.7.
Figure 3.
Change in the average rank of ground-truth tokens above and below a given entropy threshold, as the threshold increases.
Figure 4.
Change in the percentage of decoding steps exceeding a given entropy threshold as the threshold increases.
Finding 2:
The observed correlation between entropy and the rank of the ground-truth token suggests that entropy can be used as an indicator to adaptively
pause
the decoding process and
rerank
uncertain tokens. However, our entropy percentile analysis shows that it is difficult to define a universal, fixed entropy threshold across all models that effectively balances pause frequency and the number of reranking candidates. This highlights the need for a
dynamic
mechanism to determine the model-specific entropy threshold.
3.
Approach
We now introduce
AdaDec
, an uncertainty-guided adaptive decoding framework for LLM-based code generation.
AdaDec
integrates a token-level
pause-then-rerank
mechanism into the decoding process of the target LLM, drawing on insights from our empirical analysis.
3.1.
Overview
Figure 5.
Approach Overview of
AdaDec
As illustrated in Figure
5
,
AdaDec
is an adaptive (dynamic) decoding framework: at inference time it continuously monitors per-step uncertainty and dynamically decides whether to intervene, rather than applying a uniform policy across all steps or only at line-start positions. Given a target model
LM
, at each decoding step
t
t
the model produces a next-token distribution
𝒑
t
\bm{p}_{t}
.
AdaDec
computes the Shannon entropy
H
⁡
(
𝒑
t
)
H(\bm{p}_{t})
and compares it against a model-specific threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
. If
H
⁡
(
𝒑
t
)
≤
τ
𝑳
​
𝑴
H(\bm{p}_{t})\leq\tau^{\bm{LM}}
, the framework proceeds with the base decoding policy (e.g., greedy, top-
k
k
, or top-
p
p
sampling). If
H
⁡
(
𝒑
t
)
>
τ
𝑳
​
𝑴
H(\bm{p}_{t})>\tau^{\bm{LM}}
,
AdaDec
pauses normal decoding and triggers a targeted reranking routine over the top-
K
K
candidates. During reranking, each candidate undergoes a short lookahead of up to
N
N
steps to estimate the quality of its future trajectory, and the candidate with the highest score is selected as the next token. This per-step decision loop repeats until an end-of-sequence (EOS) token is generated.
The adaptive nature of
AdaDec
has three practical consequences. First, the intervention is selective and data-driven: only high-uncertainty steps incur additional computation, which limits overhead compared to always-on strategies. Second, the threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
is learned in a preparation stage (we describe the learning procedure in Sec.
3.2
) so that the pause decision is model-aware rather than hand-tuned. Third, the framework supports flexible reranking configurations (e.g., adjustable lookahead length
N
N
and lookahead width
K
K
), allowing trade-offs between accuracy and latency to be tuned for different deployment constraints.
AdaDec
is designed to be broadly applicable. Since the pause-then-rerank mechanism is triggered purely by uncertainty signals (entropy), it can be seamlessly integrated with various decoding strategies, including sampling. This flexibility underscores the generality of
AdaDec
: rather than being tied to a specific decoding style, it acts as a plug-in framework that can enhance both deterministic (e.g., greedy) and stochastic (e.g., sampling) generation. Unless otherwise specified, we use
greedy decoding as the base policy
throughout the remainder of this paper.
The details of the pause checking and lookahead reranking are described in the following sections.
3.2.
Entropy-based Pause Checking
We use the Shannon entropy
H
⁡
(
𝒑
t
)
H(\bm{p}_{t})
over the probability distribution
𝒑
t
\bm{p}_{t}
predicted by the model
LM
to measure the token uncertainty. When
H
H
exceeds a threshold,
AdaDec
pauses the decoding process. As revealed in the empirical study, a fixed entropy threshold may not generalize well across models with different output distributions. Therefore, we propose a data-driven method to learn a model-specific threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
using logistic regression.
3.2.1.
Data Collection
We cast threshold learning as a binary classification task. Each decoding step is a sample, where the input feature is the entropy
H
⁡
(
𝒑
t
)
H(\bm{p}_{t})
and the label is 1 if the ground-truth token is the top-1 prediction, and 0 otherwise. Training data is generated via ground-truth–guided next-token prediction on BigCodeBench
(
Zhuo et al., 2025
)
. To strictly mitigate data contamination, we verified semantic similarity between BigCodeBench and our evaluation sets using SBERT
(
Reimers and Gurevych, 2019
)
. Manual review of all problem pairs exceeding a 0.7 cosine similarity threshold (maximum observed was 0.75) confirmed zero overlapping duplicates. Through this process, we collect approximately 100K––160K positive samples and 16K–23K negative samples per model (e.g., 161K positive and 19K negative for DS-6.7B).
We then balance the dataset by randomly downsampling the positive samples and selecting an equal number of negative samples, which is a common technique for handling imbalanced classification tasks
(
Lemaitre et al., 2016
)
. This choice is driven by the nature of logic drift in code generation: once a drift point occurs, it typically leads to irreversible semantic errors. Therefore, it is essential to maximize the classifier’s ability to detect negative cases, even if they are relatively scarce. By constructing a balanced dataset, we prevent the model from being biased toward the majority class and enable it to more effectively learn the decision boundary for identifying uncertain decoding steps. This strategy enhances the classifier’s sensitivity to potential drift points, thereby improving the overall reliability of the entropy-based triggering mechanism.
3.2.2.
Regression Model Training
We train a logistic regression model to predict whether the ground truth token is the top-1 prediction, using only the entropy value as input. The model estimates the probability of a positive label using the sigmoid function:
P
⁡
(
y
=
1
∣
H
(
i
)
)
=
1
1
+
exp
⁡
(
−
(
β
0
+
β
1
​
H
(
i
)
)
)
,
P(y=1\mid H^{(i)})=\frac{1}{1+\exp(-(\beta_{0}+\beta_{1}H^{(i)}))},
where
H
(
i
)
H^{(i)}
denotes the entropy of the
i
i
-th sample, and
β
0
\beta_{0}
,
β
1
\beta_{1}
are the model parameters to be learned. These parameters are learned by minimizing the binary cross-entropy loss through maximum likelihood estimation. Note that, since the training data is collected using the target
LM
, the trained logistic regression model is specific to that
LM
.
3.2.3.
Threshold Estimation
To estimate a model-specific entropy threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
, we use the trained logistic regression model to perform binary classification on the validation set, where the task is to predict whether the top-1 token matches the ground-truth token. As the logistic regression model outputs probabilities, we first identify the optimal probability threshold that maximizes classification accuracy, and then convert this probability threshold into an equivalent entropy threshold.
Specifically, we conduct a grid search over probability thresholds in the range [0.01, 0.99], using a step size of 0.01. For each candidate threshold, a sample is classified as positive if its predicted probability exceeds the threshold, and negative otherwise. The threshold that achieves the highest classification accuracy on the validation set is selected as the optimal probability threshold, denoted by
p
∗
p^{*}
. We then convert this optimal probability threshold into the corresponding entropy threshold using the parameters of the trained logistic regression model. Given the intercept
β
0
\beta_{0}
and the coefficient
β
1
\beta_{1}
, the entropy threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
is computed using the log-odds transformation:
τ
𝑳
​
𝑴
=
log
⁡
(
p
∗
1
−
p
∗
)
−
β
0
β
1
.
\tau^{\bm{LM}}=\frac{\log\left(\frac{p^{*}}{1-p^{*}}\right)-\beta_{0}}{\beta_{1}}.
Entropy values below
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
are classified as positive (i.e., the model is likely to correctly predict the top-1 token), while those above are classified as negative. This entropy threshold is then used as the final decision boundary for the target language model during decoding.
3.2.4.
Pause Triggering
During decoding,
AdaDec
uses the learned threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
to decide when to trigger candidate reranking. If the entropy at a decoding step exceeds
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
, it indicates high uncertainty, suggesting that the top-1 prediction may be incorrect. In such cases, the decoding process is paused, and the top candidates are reranked to improve accuracy.
3.3.
Lookahead-based Token Reranking
AdaDec
employs a lookahead re-scoring strategy for token reranking, enhancing selection by assessing the future impact of each candidate token at every decoding step. Inspired by A* search heuristics and prior work on constrained generation
(
Lu et al., 2021
)
, this method extends token probability evaluation beyond immediate next-token predictions to consider longer-term sequence quality. The process is governed by two hyperparameters: the
lookahead beam size
(
B
B
), which determines the number of candidate tokens considered, and the
lookahead length
(
L
L
), which sets the length of the future token sequence evaluated.
3.3.1.
Lookahead Process
At decoding step
t
t
, the model outputs a probability distribution
𝒑
t
\bm{p}_{t}
over the vocabulary for the next token. From this distribution, we select the top-
B
B
tokens to form the candidate set
𝒞
t
=
{
c
t
(
1
)
,
c
t
(
2
)
,
…
,
c
t
(
B
)
}
\mathcal{C}_{t}=\{c_{t}^{(1)},c_{t}^{(2)},\dots,c_{t}^{(B)}\}
.
For each candidate token
c
t
(
k
)
c_{t}^{(k)}
, we construct a lookahead trajectory of length
L
L
by appending
L
L
tokens generated via greedy decoding, conditioned on the current input and previously generated tokens. This results in the trajectory
𝐓
t
(
k
)
\mathbf{T}_{t}^{(k)}
:
𝐓
t
(
k
)
=
(
c
t
(
k
)
,
c
^
t
+
1
(
k
)
,
c
^
t
+
2
(
k
)
,
…
,
c
^
t
+
L
(
k
)
)
,
\mathbf{T}_{t}^{(k)}=(c_{t}^{(k)},\hat{c}_{t+1}^{(k)},\hat{c}_{t+2}^{(k)},\dots,\hat{c}_{t+L}^{(k)}),
where each
c
^
t
+
i
(
k
)
\hat{c}_{t+i}^{(k)}
is the most probable token predicted at step
t
+
i
t+i
, given the prefix ending with
c
t
(
k
)
c_{t}^{(k)}
.
Trajectory Scoring.
We evaluate each trajectory by computing the average log-probability of its tokens:
score
​
(
c
t
(
k
)
)
=
1
L
+
1
​
[
log
⁡
P
⁡
(
c
t
(
k
)
)
+
∑
i
=
1
L
log
⁡
P
⁡
(
c
^
t
+
i
(
k
)
)
]
,
\text{score}(c_{t}^{(k)})=\frac{1}{L+1}\left[\log P(c_{t}^{(k)})+\sum_{i=1}^{L}\log P(\hat{c}_{t+i}^{(k)})\right],
where
P
⁡
(
⋅
)
P(\cdot)
denotes the model’s predicted probability for a token. Because we apply an early stopping mechanism, different candidates may result in varying lookahead lengths. To ensure a fair comparison across such candidates, we normalize the total log-probability by computing the geometric mean of token probabilities in the above equation, rather than relying solely on log-likelihood. This normalization mitigates the bias against longer sequences, which tend to accumulate lower joint probabilities. The resulting score captures the model’s overall confidence in the full trajectory, balancing immediate token likelihood with the coherence of future predictions.
Token Selection.
The candidate with the highest trajectory score is selected as the output token at step
t
t
:
c
t
∗
=
arg
⁡
max
c
t
(
k
)
∈
𝒞
t
​
score
​
(
c
t
(
k
)
)
.
c^{*}_{t}=\arg\max_{c_{t}^{(k)}\in\mathcal{C}_{t}}\text{score}(c_{t}^{(k)}).
This process is repeated at each decoding step, ensuring that token selection is guided not just by immediate probabilities, but by the expected quality of the downstream sequence.
This lookahead mechanism improves generation quality by favoring tokens that lead to fluent and coherent continuations, which is particularly important in structured domains like code generation. The hyperparameters
B
B
and
L
L
control the trade-off between computational cost and generation quality: larger values offer better foresight at the expense of increased inference time.
3.3.2.
Lookahead Beam Size Selection
To determine an appropriate value for
B
B
, we analyze the training data collected in Section
3.2.1
. Specifically, we examine the average rank of the ground truth token at decoding steps where the Shannon entropy is either above or below the threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
, which is learned via logistic regression. After filtering out samples where the ground truth token’s rank exceeds 20, we observe a clear distinction: when the entropy is below or equal to the threshold, the average rank typically falls between 1.1 and 1.3, indicating high model confidence. In contrast, when the entropy exceeds the threshold—thus triggering a pause—the average rank increases to between 2.6 and 3.4.
These findings support the use of a small beam size (e.g.,
B
=
3
B=3
) to achieve a practical trade-off between candidate coverage and computational efficiency.
3.3.3.
Lookahead Length Selection
We adopt a lookahead length parameter
L
L
when performing trajectory scoring. At each reranking step we simulate up to
L
L
future tokens for each candidate to estimate the quality of its continuation. The parameter
L
L
controls the trade-off between accuracy and efficiency: a larger
L
L
provides a more reliable estimate of long-term trajectory quality but incurs higher computation cost, whereas a smaller
L
L
reduces overhead but may fail to capture meaningful differences among candidates.
In practice, we find that moderate values of
L
L
(e.g.,
L
=
5
L=5
) are sufficient to balance these concerns, since code generation typically exhibits strong local dependencies and short-horizon lookahead already provides useful signals. We analyze the effect of varying
L
L
through experiments in Section
4.5
.
4.
Evaluation
We conduct extensive experiments to evaluate the effectiveness of
AdaDec
. Specifically, we aim to answer the following research questions:
•
RQ1 (Effectiveness):
How effective is
AdaDec
in improving the functional correctness of generated code?
•
RQ2 (Efficiency):
How efficient is
AdaDec
in terms of computational cost?
•
RQ3 (Ablation Study):
How effective is the logistic regression–based threshold learning component, and can the learned thresholds better guide practical decoding?
•
RQ4 (Parameter Sensitivity):
How does
AdaDec
perform under different values of the lookahead length
L
L
?
4.1.
Experimental Setup
Our experimental setup is as follows.
Datasets.
We evaluate our method on three widely used code generation benchmarks:
•
HumanEval+
(
Liu et al., 2023
)
: An extended version of HumanEval
(
Chen et al., 2021
)
with test cases increased by a factor of 81 for 164 Python problems, enabling rigorous functional correctness evaluation.
•
MBPP+
(
Liu et al., 2023
)
: A refined subset of 378 MBPP
(
Austin et al., 2021
)
problems with 35 times larger unit tests for stricter evaluation.
•
DevEval
(
Li et al., 2024
)
: A repository-level benchmark aligned with real-world scenarios. We randomly sample 238 problems from its 1,874 samples, ensuring 90% confidence within a ±5% margin.
Baselines.
We compare
AdaDec
against three decoding strategies:
•
Greedy Decoding
(
Radford et al., 2019
)
: Selects the highest-probability token at each step; computationally efficient but myopic.
•
Beam Search
(
Freitag and Al-Onaizan, 2017
)
: Maintains the top-
k
k
sequences. We set beam size
B
=
3
B=3
to match
AdaDec
’s candidate pool, isolating the benefits of uncertainty-guided reranking.
•
AdapT
(
Zhu et al., 2023
)
: Adjusts sampling temperature for line-start (high-uncertainty) tokens. We empirically set
a
=
0.5
a=0.5
and
b
=
0.05
b=0.05
(for other tokens) for optimal benchmark performance.
We also considered
Uncert-CoT
(
Zhu et al., 2025
)
, another uncertainty-guided decoding method originally proposed for chain-of-thought reasoning tasks. However, we do not include it in our experimental comparison since no official implementation is available and the original paper omits several crucial details necessary for faithful reproduction.
4.2.
RQ1: Effectiveness in Improving Functional Correctness
Table
2
presents the Pass@1 performance of four decoding strategies—Greedy, Beam Search (
B
=
3
B=3
), AdapT, and
AdaDec
—across nine LLMs evaluated on the HumanEval+, MBPP+, and DevEval datasets.
Table 2.
Pass@1 (%) comparison of Greedy, Beam Search, AdapT, and
AdaDec
on HumanEval+, MBPP+, and DevEval. Values in parentheses indicate the change relative to Greedy.
Model
HumanEval+
MBPP+
DevEval
Greedy
Beam
AdapT
AdaDec
Greedy
Beam
AdapT
AdaDec
Greedy
Beam
AdapT
AdaDec
DS-1.3B
62.20
62.20
(+0.00)
63.41
(+1.21)
65.24
(+3.04)
52.12
51.59
(-0.53)
52.65
(+0.53)
53.17
(+1.05)
14.29
18.91
(+4.62)
12.61
(-1.68)
18.49
(+4.20)
DS-6.7B
71.34
76.83
(+5.49)
72.56
(+1.22)
73.78
(+2.44)
65.61
65.87
(+0.26)
66.93
(+1.32)
67.72
(+2.11)
25.21
28.57
(+3.36)
26.47
(+1.26)
26.47
(+1.26)
ST-3B
48.78
50.61
(+1.83)
51.83
(+3.05)
50.61
(+1.83)
38.89
45.77
(+6.88)
39.42
(+0.53)
46.03
(+7.14)
15.55
13.03
(-2.52)
13.03
(-2.52)
22.69
(+7.14)
QW2.5-1.5B
64.02
68.90
(+4.88)
64.02
(+0.00)
67.07
(+3.05)
59.79
61.64
(+1.85)
60.32
(+0.53)
62.17
(+2.38)
10.08
11.34
(+1.26)
10.50
(+0.42)
14.71
(+4.63)
QW2.5-7B
84.15
83.54
(-0.61)
87.20
(+3.05)
87.20
(+3.05)
71.16
71.96
(+0.80)
72.22
(+1.06)
72.22
(+1.06)
18.49
14.71
(-3.78)
18.07
(-0.42)
23.11
(+4.62)
QW3-0.6B
17.07
24.39
(+7.32)
18.29
(+1.22)
22.56
(+5.49)
9.52
21.16
(+11.64)
11.11
(+1.59)
30.42
(+20.90)
2.94
5.88
(+2.94)
2.52
(-0.42)
7.56
(+4.62)
QW3-1.7B
40.24
41.46
(+1.22)
42.07
(+1.83)
44.51
(+4.27)
37.57
43.39
(+5.82)
36.51
(-1.06)
42.86
(+5.29)
7.98
9.24
(+1.26)
7.56
(-0.42)
11.76
(+3.78)
QW3-4B
53.05
57.32
(+4.27)
53.66
(+0.61)
56.10
(+3.05)
40.48
42.86
(+2.38)
41.01
(+0.53)
51.32
(+10.84)
9.24
13.45
(+4.21)
9.24
(+0.00)
16.81
(+7.57)
QW3-8B
56.71
59.76
(+3.05)
57.32
(+0.61)
62.80
(+6.09)
29.37
36.24
(+6.87)
29.63
(+0.26)
47.09
(+17.72)
4.62
6.30
(+1.68)
4.20
(-0.42)
7.56
(+2.94)
AVG.
Δ
\Delta
–
+3.05
+1.42
+3.59
–
+4.00
+0.59
+7.61
–
+1.45
-0.47
+4.53
Comparison with Greedy Search.
Across all three benchmarks,
AdaDec
consistently outperforms Greedy decoding.
On HumanEval+,
AdaDec
improves Pass@1 by an average of
+3.59%
, with gains as high as +6.09% for QW3-8B and +5.49% for QW3-0.6B.
On MBPP+, the improvement is even more pronounced:
AdaDec
yields an average gain of
+7.61%
, with particularly significant performance boosts observed for QW3-0.6B (+20.90%) and QW3-8B (+17.72%).
On DevEval,
AdaDec
demonstrates robust effectiveness, yielding meaningful improvements for all evaluated models (
+4.53%
on average). Particularly, QW3-4B and ST-3B show strong gains of +7.57% and +7.14%, respectively.
Unlike the mixed results sometimes observed with other strategies,
AdaDec
achieves positive improvements across all models on DevEval, highlighting its ability to handle repository-level contexts where long-range logic consistency is crucial.
Comparison with Beam Search.
A critical question is whether the gains of
AdaDec
stem merely from searching multiple candidate tokens or from our uncertainty-guided strategy.
Comparing
AdaDec
with standard Beam Search (using the same beam width
B
=
3
B=3
), we observe that
AdaDec
consistently achieves superior performance.
While Beam Search provides a baseline improvement over Greedy (averaging +3.05% on HumanEval+ and +4.00% on MBPP+),
AdaDec
surpasses it by further margins.
The advantage of
AdaDec
is particularly evident on the more challenging MBPP+ and DevEval benchmarks. For instance, on DevEval, Beam Search yields a modest average gain of +1.45%, whereas
AdaDec
achieves
+4.53%
, nearly tripling the improvement.
This indicates that blindly searching for top-
k
k
continuations (as in Beam Search) is less effective than
AdaDec
’s approach of triggering lookahead only at high-uncertainty points, which allows for more targeted and semantically meaningful corrections.
Comparison with AdapT.
When compared to AdapT,
AdaDec
shows clear advantages in both stability and magnitude of improvement.
While AdapT offers marginal improvements over Greedy decoding (e.g., +1.42% on HumanEval+ and +0.59% on MBPP+), it exhibits instability, leading to performance drops on DevEval for several models (average -0.47%).
In contrast,
AdaDec
consistently achieves larger gains, surpassing AdapT by wide margins across nearly all models and datasets.
For example, on MBPP+,
AdaDec
exceeds AdapT by approximately
+7%
on average.
These results confirm that utilizing Shannon entropy to guide lookahead is a more reliable strategy than the heuristic-based temperature adjustment used in AdapT.
Summary:
Overall, the results indicate that
AdaDec
is highly effective in improving the functional correctness of generated code. It consistently outperforms Greedy decoding across diverse models and benchmarks. More importantly, it surpasses Beam Search, particularly on complex tasks (MBPP+ and DevEval), proving that uncertainty-guided intervention is superior to blind search. Compared with AdapT,
AdaDec
demonstrates significantly more robust and scalable gains.
4.3.
RQ2: Efficiency in Computational Cost
We evaluate the efficiency of
AdaDec
in terms of computational cost on the HumanEval+, MBPP+, and DevEval datasets. We analyze two key metrics: the
pause rate
and
prediction latency
.
Pause Rate.
Table
3
presents the pause rates across different models and datasets. The results show that
AdaDec
triggers the reranking mechanism sparingly, with pause rates ranging from 0.85% to 12.17%, averaging approximately
6.75%
across all configurations.
This low activation frequency indicates that the entropy-based threshold successfully identifies a small subset of critical, high-uncertainty steps. Unlike global search strategies,
AdaDec
concentrates computational effort only where necessary. Notably, even for the largest models, the pause rate generally remains below 10%, demonstrating that our selective triggering mechanism scales efficiently without incurring the cost of constant lookahead.
Table 3.
Pause ratio of the models on HumanEval+, MBPP+, and DevEval.
DS-1.3B
DS-6.7B
ST-3B
QW2.5-1.5B
QW2.5-7B
QW3-0.6B
QW3-1.7B
QW3-4B
QW3-8B
HumanEval+
2.81%
2.33%
4.80%
1.48%
0.85%
6.11%
11.17%
7.82%
5.98%
MBPP+
8.49%
7.46%
6.52%
6.24%
4.43%
8.50%
12.17%
7.11%
8.33%
DevEval
7.75%
6.29%
6.59%
6.95%
9.70%
6.16%
11.47%
9.69%
5.04%
AVG.
Δ
\Delta
6.35%
5.36%
5.97%
4.89%
4.99%
6.92%
11.60%
8.21%
6.45%
Latency.
Table
4
reports the average generation time per problem for Greedy, Beam Search (
B
=
3
B=3
), AdapT, and
AdaDec
.
Comparison with Greedy.
Overall,
AdaDec
introduces moderate additional latency compared to Greedy decoding (e.g., an average increase of +0.75s on HumanEval+ and +0.32s on MBPP+). This overhead is expected due to the lookahead computations. However, considering the substantial accuracy gains reported in RQ1, this trade-off is highly favorable.
Notably, for certain models (e.g., QW3-0.6B and QW3-1.7B on HumanEval+),
AdaDec
actually exhibits lower latency than Greedy decoding. This counter-intuitive result occurs because
AdaDec
prevents the model from drifting into erroneous, low-quality trajectories—such as repetitive loops or verbose, nonsensical outputs—that often plague Greedy decoding at high-uncertainty points. By correcting the generation path early via lookahead,
AdaDec
produces more concise and correct solutions, thereby reducing the total number of generated tokens and effectively offsetting the computational cost of reranking.
Comparison with Beam Search.
A critical finding is that
AdaDec
is significantly more efficient than Beam Search, despite outperforming it in accuracy.
As shown in Table
4
, Beam Search introduces substantial latency overhead due to maintaining multiple active beams at every step. For instance, on the repository-level DevEval benchmark, Beam Search increases the average generation time by
+24.62s
compared to Greedy. In contrast,
AdaDec
increases it by only
+7.47s
.
This efficiency stems from our
selective pausing strategy
: by triggering the lookahead mechanism only at high-uncertainty steps rather than globally,
AdaDec
avoids wasted computation on trivial tokens.
Comparison with AdapT.
AdapT exhibits mixed runtime behavior. In simpler scenarios (e.g., MBPP+), it adds negligible overhead (+0.10s) or even reduces time slightly for specific models by promoting shorter sequences via sampling. However,
AdaDec
provides a more consistent balance: while slightly slower than AdapT, it delivers far more robust functional correctness (as shown in RQ1), justifying the marginal increase in runtime.
Table 4.
Comparison of the average generation time per problem (in seconds) by Greedy, Beam Search, AdapT,
AdaDec
on HumanEval+, MBPP+, DevEval.
Model
HumanEval+
MBPP+
DevEval
Greedy
Beam
AdapT
AdaDec
Greedy
Beam
AdapT
AdaDec
Greedy
Beam
AdapT
AdaDec
DS-1.3B
2.94
7.01
2.72
4.56
1.46
1.91
1.47
1.68
4.03
14.59
4.24
7.66
DS-6.7B
9.55
25.60
13.59
11.87
3.21
7.51
3.13
4.81
20.56
53.52
23.72
32.91
ST-3B
1.71
3.45
2.72
2.06
0.60
1.01
0.84
0.77
6.92
34.40
8.33
14.90
QW2.5-1.5B
5.29
9.39
4.18
5.82
1.78
2.24
1.55
2.24
7.91
19.02
7.88
10.12
QW2.5-7B
12.24
38.22
13.40
14.38
3.94
10.12
3.90
6.02
12.12
26.51
13.71
22.19
QW3-0.6B
6.34
8.94
5.18
5.03
5.94
9.44
6.14
3.89
19.49
23.79
17.86
21.84
QW3-1.7B
8.23
9.98
6.03
5.29
2.13
3.17
2.54
2.28
22.21
46.98
20.56
29.53
QW3-4B
5.41
9.13
7.29
8.10
3.49
5.02
3.76
3.37
29.57
80.24
31.94
42.78
QW3-8B
5.62
11.76
5.63
6.99
3.88
5.19
4.03
4.21
61.14
106.48
63.53
69.23
AVG.
Δ
\Delta
–
+7.35
+0.38
+0.75
–
+2.13
+0.10
+0.32
–
+24.62
+0.87
+7.47
Summary:
AdaDec
maintains high efficiency by selectively triggering lookahead at a low rate (average
≈
\approx
6.75%), effectively filtering out low-utility computations. Crucially, compared to Beam Search,
AdaDec
incurs significantly lower additional overhead while achieving superior output quality across all benchmarks. This confirms that uncertainty-guided lookahead represents a far more efficient allocation of inference resources than blind search.
4.4.
RQ3: Ablation Study
We perform an ablation study to evaluate the key components of
AdaDec
. In particular, we investigate whether the learned entropy threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
serves as an effective signal, both in terms of predictive ability (as a classifier) and in practical decoding performance.
Predictive Effectiveness of Learned Entropy Thresholds.
Table
5
summarizes the performance of the logistic regression classifier trained with learned entropy thresholds (
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
).
Overall, the classifier demonstrates robust predictive capability across all models, achieving an average F1 score of 0.9351 and an AUC of 0.9116.
The highest performance is observed on DS-6.7B, with an accuracy of 91.05% and an F1 score of 0.9512. Even for smaller models, the classifier remains reliable; for instance, ST-3B achieves an F1 score of 0.9475.
These high metrics confirm that Shannon entropy, when calibrated via our learning process, serves as a high-fidelity signal for distinguishing between correct and incorrect token predictions.
Table 5.
Evaluation of logistic regression models trained to predict whether the ground truth token is the top-1 prediction. The learned
𝝉
𝑳
​
𝑴
\bm{\tau}^{\bm{LM}}
denotes the entropy threshold selected via logistic regression.
Model
Accuracy
Precision
Recall
F1 Score
AUC
Learned
τ
L
​
M
\bm{\tau}^{\bm{LM}}
DS-1.3B
0.8994
0.9251
0.9640
0.9442
0.9268
0.9850
DS-6.7B
0.9105
0.9276
0.9761
0.9512
0.9305
1.1338
ST-3B
0.9038
0.9188
0.9780
0.9475
0.9222
1.1005
QW2.5-1.5B
0.8824
0.9055
0.9638
0.9337
0.9085
1.2232
QW2.5-7B
0.8889
0.9106
0.9679
0.9384
0.9119
1.1739
QW3-0.6B
0.8512
0.8774
0.9498
0.9122
0.8914
1.3213
QW3-1.7B
0.8664
0.9003
0.9457
0.9225
0.8964
0.6153
QW3-4B
0.8807
0.9166
0.9471
0.9316
0.9073
0.7134
QW3-8B
0.8843
0.9158
0.9533
0.9342
0.9092
0.7060
AVG.
Δ
\Delta
0.8853
0.9109
0.9606
0.9351
0.9116
0.9969
Practical Effectiveness of Learned Entropy Thresholds.
To validate the necessity of learning the threshold rather than using a heuristic constant, we compare the decoding performance of models using the learned threshold versus a fixed threshold. The fixed threshold is set to 1.2.
Table
6
reports the Pass@1 results on HumanEval+.
The experiments demonstrate that using the learned thresholds yields consistent improvements over the fixed threshold baseline across all evaluated models.
The average improvement is
+1.76%
, with gains ranging from +0.61% to +4.88%.
Specifically, while most models (e.g., DS-1.3B, QW2.5-7B, QW3-8B) show stable moderate gains between 1.2% and 1.8%, distinctively larger boosts are observed for QW3-1.7B (+3.05%) and QW3-4B (+4.88%).
This indicates that a fixed threshold of 1.2 is often suboptimal. By calibrating the threshold to each model’s specific uncertainty distribution,
AdaDec
ensures robust performance gains, effectively unlocking the model’s potential regardless of its specific architecture or scale.
Table 6.
Comparison of Learned vs. Fixed Entropy Thresholds on HumanEval+ (Pass@1). Fixed threshold is set to 1.2.
Strategy
DS-1.3B
DS-6.7B
ST-3B
QW2.5-1.5B
QW2.5-7B
QW3-0.6B
QW3-1.7B
QW3-4B
QW3-8B
AVG
Fixed
63.41%
73.17%
50.00%
65.85%
85.98%
21.34%
41.46%
51.22%
61.59%
57.11%
Learned
65.24%
73.78%
50.61%
67.07%
87.20%
22.56%
44.51%
56.10%
62.80%
58.87%
Δ
\Delta
+1.83%
+0.61%
+0.61%
+1.22%
+1.22%
+1.22%
+3.05%
+4.88%
+1.21%
+1.76%
Summary:
The learned entropy threshold
τ
𝑳
​
𝑴
\tau^{\bm{LM}}
is both theoretically sound and practically effective. It reliably predicts token risks and consistently outperforms a fixed-threshold baseline across all models, delivering an average Pass@1 improvement of +1.76% and maximizing the effectiveness of the uncertainty-guided intervention.
4.5.
RQ4: Parameter Sensitivity
To investigate the impact of key hyperparameters on decoding performance, we conduct sensitivity analyses on the lookahead length
L
L
and the learned entropy threshold
τ
L
​
M
\tau^{LM}
. All experiments in this section use DS-1.3B as the backbone model evaluated on HumanEval+.
Sensitivity to Lookahead Length (
L
L
).
We vary
L
L
from 2 to 9 and report Pass@1 results. Figure
6
illustrates the trend.
Figure 6.
Pass@1 Performance of the DS-1.3B Model on the HumanEval+ Dataset Under Different Lookahead Length (L) Configurations.
The results show that Pass@1 increases steadily with larger
L
L
up to
L
=
5
L=5
, at which point it reaches the peak performance of
65.24%
.
Beyond
L
=
5
L=5
, the performance does not continue to rise; instead, it exhibits slight fluctuations, hovering between 63.41% and 64.63%.
This behavior reflects the trade-off between local guidance and global noise: while shorter lookaheads may fail to capture sufficient future context, excessively long lookaheads (
L
>
5
L>5
) may introduce noise from uncertainty accumulation, diluting the relevance of immediate local signals.
Crucially, across all values of
L
L
,
AdaDec
consistently outperforms the Greedy baseline (62.20%). Even at the minimal setting of
L
=
2
L=2
,
AdaDec
achieves 62.80%, reducing to a safe margin of +0.60%. This demonstrates that our approach is robust to hyperparameter choices and provides stable improvements.
Sensitivity to Threshold Variations (
τ
L
​
M
\tau^{LM}
).
As illustrated in Table
7
, we evaluate the Pass@1 accuracy by shifting the optimal learned threshold (
τ
L
​
M
≈
0.9850
\tau^{LM}\approx 0.9850
) across various intervals.
AdaDec
demonstrates high robustness to minor fluctuations. Within the
[
τ
L
​
M
−
0.1
,
τ
L
​
M
+
0.1
]
[\tau^{LM}-0.1,\tau^{LM}+0.1]
range, Pass@1 remains highly stable and consistently outperforms the greedy baseline.
Table 7.
Sensitivity of
AdaDec
performance (Pass@1) to entropy threshold (
τ
\tau
) variations on HumanEval+. Evaluated with DS-1.3B.
Learned
denotes the optimal threshold derived from our approach.
Setting
Threshold
τ
\tau
Pass@1 (%)
Pause Rate (%)
Baseline (Greedy)
–
62.20
–
τ
L
​
M
−
0.50
\tau^{LM}-0.50
0.4850
63.41
7.82
τ
L
​
M
−
0.10
\tau^{LM}-0.10
0.8850
65.24
3.46
τ
L
​
M
−
0.05
\tau^{LM}-0.05
0.9350
64.63
3.10
τ
L
​
M
\tau^{LM}
(Learned)
0.9850
65.24
2.81
τ
L
​
M
+
0.05
\tau^{LM}+0.05
1.0350
65.24
2.52
τ
L
​
M
+
0.10
\tau^{LM}+0.10
1.0850
64.63
2.16
τ
L
​
M
+
0.50
\tau^{LM}+0.50
1.4850
62.80
0.83
Visible performance degradation occurs only under drastic shifts (
±
0.5
\pm 0.5
): excessively low thresholds introduce noise via over-intervention, while excessively high thresholds become too conservative. This confirms that
τ
L
​
M
\tau^{LM}
is not a fragile hyperparameter requiring extreme precision.
Summary:
Both key hyperparameters exhibit high robustness. The lookahead length
L
L
shows a non-monotonic effect, with moderate values (e.g.,
L
=
5
L=5
) maximizing the benefits of lookahead guidance. The learned threshold
τ
L
​
M
\tau^{LM}
is highly stable against minor fluctuations within
±
0.1
\pm 0.1
. Notably,
AdaDec
consistently surpasses baseline performance across varying hyperparameter settings.
5.
Discussion
5.1.
Generalizability and Transferability of the Learned Threshold (
τ
L
​
M
\tau^{LM}
)
We conduct a quantitative analysis using DS-1.3B to evaluate the robustness of the learned entropy threshold (
τ
L
​
M
\tau^{LM}
) across domain and prompt shifts, and provide guidance on its practical application.
Robustness to Domain and Prompt Shifts.
We evaluate the transferability of
τ
L
​
M
\tau^{LM}
to library-heavy domains and varying prompt templates. We compute the optimal thresholds for two specific data science scenarios: a data science subset filtered from BigCodeBench (666 problems) and the DS-1000 benchmark
(
Lai et al., 2022
)
(1000 problems, featuring drastically different prompt styles and task requirements). The optimal thresholds for these two datasets are
0.9740
0.9740
(
Δ
=
0.0110
\Delta=0.0110
) and
0.9178
0.9178
(
Δ
=
0.0672
\Delta=0.0672
), respectively. Since our parameter sensitivity analysis (Section
4.5
) demonstrates that deviations within
±
0.1
\pm 0.1
do not significantly impact performance, a globally learned
τ
L
​
M
\tau^{LM}
remains highly effective without the need for task-specific tuning.
Guidance on Relearning
τ
L
​
M
\tau^{LM}
.
These findings indicate that
τ
L
​
M
\tau^{LM}
reflects the intrinsic uncertainty calibration of the base LLM rather than task-specific artifacts. Therefore, relearning
τ
L
​
M
\tau^{LM}
is generally unnecessary for different standard coding domains or prompt styles. Retraining is only recommended when the base model’s confidence distribution changes fundamentally, such as after Supervised Fine-Tuning (SFT) or alignment techniques.
5.2.
Limitations
While
AdaDec
demonstrates improvements in code generation accuracy and maintains acceptable computational cost, it has several limitations that warrant further investigation:
Reliance Solely on Shannon Entropy.
Our uncertainty trigger is based solely on the Shannon entropy of the token distribution, which provides a coarse measure of model uncertainty. More nuanced contextual features—such as entropy of subpopulations of tokens, token-level gradient norms, or higher-order statistics—might better capture subtle divergences. Future work could integrate richer uncertainty signals or leverage learned uncertainty estimators.
Threshold Learning Simplicity.
We employ a logistic regression classifier to learn entropy thresholds, which offers interpretability but may be insufficiently expressive for capturing complex interactions among uncertainty features. More powerful models (e.g., small neural networks) could potentially improve threshold accuracy, at the cost of increased complexity.
Fixed Lookahead Depth.
Currently,
AdaDec
utilizes a fixed lookahead length (e.g.,
L
=
5
L=5
) across all benchmarks. While this serves as a reasonable global setting, repository-level tasks (e.g., DevEval) often require longer-range reasoning, and a short lookahead window may under-express these dependencies. Future research could explore adaptive, context-aware lookahead depths that dynamically adjust to accommodate both short-term syntactic constraints and long-term semantic reasoning demands.
Addressing these limitations will be an actionable direction for future work, towards making uncertainty-guided adaptive decoding more robust, flexible, and broadly applicable.
5.3.
Case Study
To illustrate
AdaDec
’s practical advantage, Figure
7
presents the
check_dict_case
task from HumanEval+. While standard greedy decoding unsafely assumes all dictionary keys are strings (causing runtime errors for integer keys),
AdaDec
detects high entropy at this critical decision point. Consequently, it triggers lookahead reranking and selects a robust continuation that explicitly verifies key types (e.g.,
isinstance(key, str)
) before case checking. This demonstrates how
AdaDec
leverages entropy signals to proactively prevent subtle bugs and enhance generation reliability.
Figure 7.
A case study from HumanEval+
6.
Threats to Validity
We analyze threats to validity across four dimensions—internal, external, construct, and conclusion—and note our mitigation strategies or key limitations.
Internal Validity.
Drift point identification may be imperfect: our semi-automated AST comparison could miss subtle semantic shifts (e.g., identifier drift), and human verification introduces potential annotator bias. We mitigated these risks through clear guidelines and cross-checking. Entropy-based analysis may also depend on tokenizer or model-specific distributions; to reduce this risk, we validated results across multiple models and confirmed entropy–rank correlations in RQ2.
External Validity.
We focus on open-source models (DeepSeek, StableCode, Qwen) and three benchmarks (HumanEval+, MBPP+, DevEval). Results may not fully generalize to proprietary models or to broader real-world tasks. Future work should extend evaluation to more diverse datasets and model families.
Construct Validity.
We evaluate functional correctness (Pass@1) and efficiency (latency), which directly measure the primary objectives of correctness and performance. Nevertheless, these metrics do not capture other important qualities such as readability or adherence to coding conventions. Similarly, our use of Shannon entropy as an uncertainty signal assumes it faithfully reflects model uncertainty, though it may only provide a coarse approximation. Alternative measures could offer complementary insights.
Conclusion Validity.
Conclusion validity threats arise from the statistical robustness of our empirical results. Although we report consistent trends across multiple models and datasets, the sample size of benchmarks such as HumanEval+ remains relatively small, which may limit the statistical power of our findings. Additionally, hyperparameter choices (e.g., lookahead length
L
L
, candidate pool size
B
B
) may affect performance outcomes, and while we explored reasonable ranges, further sensitivity analysis would strengthen confidence in our conclusions.
7.
Related Work
7.1.
LLM-based Code Generation
Large Language Models (LLMs) have shown strong potential in software engineering tasks such as code generation
(
Li et al., 2023
;
Di and Zhang, 2025
;
Tian et al., 2024
;
Jiang et al., 2025
;
Lin et al., 2024
)
, unit test generation
(
Nan et al., 2025
;
Yang et al., 2024
;
Yuan et al., 2024
;
Lops et al., 2025
;
Ryan et al., 2024
)
, and comment generation
(
Haider et al., 2024
;
Katzy et al., 2025
;
Lu and Liu, 2024
)
. Typically, LLMs generate code from textual requirements via prompt-based interaction. By learning expressive representations from large-scale code and documentation corpora, they can produce syntactically correct and context-aware code snippets
(
Yuan et al., 2023
;
Sun et al., 2024
;
Ugare et al., 2024
)
. Open-foundation models further advance tasks like code completion, bug fixing
(
Fu et al., 2022
;
Jin et al., 2023
;
Xia and Zhang, 2022
)
, and test-case generation.
To evaluate their effectiveness, benchmarks like HumanEval
(
Chen et al., 2021
)
, MBPP
(
Austin et al., 2021
)
, and DS-1000
(
Lai et al., 2022
)
focus on function-level generation, while ClassEval
(
Du et al., 2023
)
extends evaluation to class-level tasks
(
Cao et al., 2026
)
. More recently, CoderEval
(
Zhang et al., 2024
)
and DevEval
(
Li et al., 2024
)
target repository-level scenarios, reflecting growing research interest in applying LLMs to real-world software development.
7.2.
Decoding strategies for LLMs
Large Language Models (LLMs) generate text in an autoregressive manner, producing one token at a time. At each generation step, the model samples a token from its predicted probability distribution. The most straightforward sampling strategy is greedy decoding, which selects the token with the highest probability as the next word. A more refined variant is beam search
(
Freitag and Al-Onaizan, 2017
)
, which maintains multiple candidate sequences at each decoding step and preserves the top-k sequences based on cumulative log-probabilities.
Beyond these, commonly used sampling strategies include temperature sampling
(
Holtzman et al., 2020
)
, top-p (nucleus) sampling
(
Holtzman et al., 2020
)
, and top-k sampling
(
Holtzman et al., 2020
)
, each designed to balance diversity and coherence in generated outputs.
To further improve sampling for code generation tasks, Li et al. introduced AdapT Sampling
(
Zhu et al., 2023
)
(Adaptive Temperature
Sampling). This method dynamically adjusts the temperature parameter T based on token context. For instance, when the current token initiates a code block, a higher T is used to encourage diversity and creativity. In contrast, for other tokens, a lower T is applied to suppress random noise and preserve syntactic and semantic correctness.
Another relevant approach is UnCert-CoT
(
Zhu et al., 2025
)
, which enhances code generation through uncertainty-aware Chain-of-Thought (CoT) reasoning, activating multi-path reasoning when token uncertainty surpasses a fixed threshold. While effective, its relies on fixed thresholds and costly CoT reasoning. In contrast,
AdaDec
learns model-specific uncertainty thresholds for stronger generalization, while its lightweight rerank mechanism cuts computational costs significantly without compromising benchmark performance.
8.
Conclusion
This paper presents
AdaDec
, an uncertainty-guided adaptive decoding framework for large language model-based code generation. Motivated by an empirical study revealing that ranking errors at high-uncertainty decoding steps often lead to logic drift,
AdaDec
introduces a novel pause-then-rerank mechanism that dynamically identifies and corrects uncertain token predictions using Shannon entropy. By learning model-specific entropy thresholds and employing a lookahead-based reranking strategy,
AdaDec
achieves substantial improvements in accuracy while maintaining computational cost and efficiency within acceptable bounds. Experiments on HumanEval+, MBPP+, and DevEval benchmarks demonstrate that
AdaDec
consistently outperforms all compared methods. These findings underscore the importance of token-level uncertainty modeling and open up new directions for adaptive decoding in code generation and beyond.
9.
Data Availability
To facilitate the replication study, we have released our data and code at :
https://github.com/SYSUSELab/AdaDec
.
Acknowledgements.
This work was supported by the National Natural Science Foundation of China (Grant No. 92582117, Grant No. 62402113), the General Program of the Natural Science Foundation of Guangdong Province, China (Grant No. 2025A1515011631), and GMCC-SYSU Joint Lab for Smart Applications.
References
Austin
et al.
(2021)
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton
Program synthesis with large language models
.
External Links:
2108.07732
,
Link
Cited by:
2nd item
,
§7.1
.
Cao
et al.
(2026)
J. Cao, Y. Chan, Z. Ling, W. Wang, S. Li, M. Liu, R. Qiao, Y. Han, C. Wang, B. Yu, P. He, S. Wang, Z. Zheng, M. R. Lyu, and S. Cheung
Rigor, reliability, and reproducibility matter: a decade-scale survey of 572 code benchmarks
.
External Links:
2501.10711
,
Link
Cited by:
§1
,
§7.1
.
Chen
et al.
(2021)
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba
Evaluating large language models trained on code
.
External Links:
2107.03374
,
Link
Cited by:
§1
,
§1
,
§2.2
,
1st item
,
§7.1
.
Di and Zhang (2025)
Y. Di and T. Zhang
Enhancing code generation via bidirectional comment-level mutual grounding
.
External Links:
2505.07768
,
Link
Cited by:
§1
,
§7.1
.
Du
et al.
(2023)
X. Du, M. Liu, K. Wang, H. Wang, J. Liu, Y. Chen, J. Feng, C. Sha, X. Peng, and Y. Lou
ClassEval: a manually-crafted benchmark for evaluating llms on class-level code generation
.
External Links:
2308.01861
,
Link
Cited by:
§7.1
.
Freitag and Al-Onaizan (2017)
M. Freitag and Y. Al-Onaizan
Beam search strategies for neural machine translation
.
In
Proceedings of the First Workshop on Neural Machine Translation
,
T. Luong, A. Birch, G. Neubig, and A. Finch (Eds.)
,
Vancouver
,
pp. 56–60
.
External Links:
Link
,
Document
Cited by:
§1
,
2nd item
,
§7.2
.
Fu
et al.
(2022)
M. Fu, C. Tantithamthavorn, T. Le, V. Nguyen, and D. Phung
VulRepair: a t5-based automated software vulnerability repair
.
In
Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering
,
ESEC/FSE 2022
,
New York, NY, USA
,
pp. 935–947
.
External Links:
ISBN 9781450394130
,
Link
,
Document
Cited by:
§1
,
§7.1
.
Guo
et al.
(2024)
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y.K. Li, F. Luo, Y. Xiong, and W. Liang
DeepSeek-coder: when the large language model meets programming – the rise of code intelligence
.
Vol.
abs/2401.14196
.
External Links:
Link
Cited by:
§1
,
§1
,
§2.1.1
.
Haider
et al.
(2024)
Md. A. Haider, A. B. Mostofa, Sk. S. B. Mosaddek, A. Iqbal, and T. Ahmed
Prompting and fine-tuning large language models for automated code review comment generation
.
External Links:
2411.10129
,
Link
Cited by:
§7.1
.
Holtzman
et al.
(2020)
A. Holtzman, J. Buys, L. Du, M. Forbes, and Y. Choi
The curious case of neural text degeneration
.
External Links:
1904.09751
,
Link
Cited by:
§1
,
§7.2
.
Hui
et al.
(2024)
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu, K. Dang, Y. Fan, Y. Zhang, A. Yang, R. Men, F. Huang, B. Zheng, Y. Miao, S. Quan, Y. Feng, X. Ren, X. Ren, J. Zhou, and J. Lin
Qwen2.5-coder technical report
.
External Links:
2409.12186
,
Link
Cited by:
§2.1.1
.
Huynh and Lin (2025)
N. Huynh and B. Lin
Large language models for code generation: a comprehensive survey of challenges, techniques, evaluation, and applications
.
External Links:
2503.01245
,
Link
Cited by:
§1
.
Jiang
et al.
(2024)
J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim
A survey on large language models for code generation
.
External Links:
2406.00515
,
Link
Cited by:
§1
.
Jiang
et al.
(2025)
X. Jiang, Y. Dong, Y. Tao, H. Liu, Z. Jin, W. Jiao, and G. Li
ROCODE: integrating backtracking mechanism and program analysis in large language models for code generation
.
External Links:
2411.07112
,
Link
Cited by:
§1
,
§7.1
.
Jin
et al.
(2023)
M. Jin, S. Shahriar, M. Tufano, X. Shi, S. Lu, N. Sundaresan, and A. Svyatkovskiy
InferFix: end-to-end program repair with llms
.
External Links:
2303.07263
,
Link
Cited by:
§1
,
§7.1
.
Katzy
et al.
(2025)
J. Katzy, Y. Huang, G. Panchu, M. Ziemlewski, P. Loizides, S. Vermeulen, A. van Deursen, and M. Izadi
A qualitative investigation into llm-generated multilingual code comments and automatic evaluation metrics
.
External Links:
2505.15469
,
Link
Cited by:
§7.1
.
Lai
et al.
(2022)
Y. Lai, C. Li, Y. Wang, T. Zhang, R. Zhong, L. Zettlemoyer, S. W. Yih, D. Fried, S. Wang, and T. Yu
DS-1000: a natural and reliable benchmark for data science code generation
.
External Links:
2211.11501
,
Link
Cited by:
§5.1
,
§7.1
.
Lemaitre
et al.
(2016)
G. Lemaitre, F. Nogueira, and C. K. Aridas
Imbalanced-learn: a python toolbox to tackle the curse of imbalanced datasets in machine learning
.
External Links:
1609.06570
,
Link
Cited by:
§3.2.1
.
Li
et al.
(2024)
J. Li, G. Li, Y. Zhao, Y. Li, H. Liu, H. Zhu, L. Wang, K. Liu, Z. Fang, L. Wang, J. Ding, X. Zhang, Y. Zhu, Y. Dong, Z. Jin, B. Li, F. Huang, and Y. Li
DevEval: a manually-annotated code generation benchmark aligned with real-world code repositories
.
External Links:
2405.19856
,
Link
Cited by:
3rd item
,
§7.1
.
Li
et al.
(2023)
J. Li, Y. Li, G. Li, Z. Jin, Y. Hao, and X. Hu
SkCoder: a sketch-based approach for automatic code generation
.
External Links:
2302.06144
,
Link
Cited by:
§1
,
§7.1
.
Li
et al.
(2025)
Z. Li, M. Liu, A. Li, K. He, Y. Wang, X. Peng, and Z. Zheng
A preliminary study on the robustness of code generation by large language models
.
External Links:
2503.20197
,
Link
Cited by:
§1
.
Lin
et al.
(2024)
F. Lin, D. J. Kim, Tse-Husn, and Chen
SOEN-101: code generation by emulating software process models using large language model agents
.
External Links:
2403.15852
,
Link
Cited by:
§1
,
§7.1
.
Liu
et al.
(2023)
J. Liu, C. S. Xia, Y. Wang, and L. Zhang
Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation
.
External Links:
2305.01210
,
Link
Cited by:
1st item
,
2nd item
.
Liu
et al.
(2026)
S. Liu, Y. Huang, M. Liu, J. Chen, E. Shi, Y. Ma, H. Zhang, Y. Zhang, and Y. Wang
ShortCoder: knowledge-augmented syntax optimization for token-efficient code generation
.
External Links:
2601.09703
,
Link
Cited by:
§1
.
Lops
et al.
(2025)
A. Lops, F. Narducci, A. Ragone, M. Trizio, and C. Bartolini
A system for automated unit test generation using large language models and assessment of generated test suites
.
In
2025 IEEE International Conference on Software Testing, Verification and Validation Workshops (ICSTW)
,
pp. 29–36
.
External Links:
Link
,
Document
Cited by:
§7.1
.
Lu and Liu (2024)
H. Lu and Z. Liu
Improving retrieval-augmented code comment generation by retrieving for generation
.
External Links:
2408.03623
,
Link
Cited by:
§7.1
.
Lu
et al.
(2021)
X. Lu, S. Welleck, P. West, L. Jiang, J. Kasai, D. Khashabi, R. L. Bras, L. Qin, Y. Yu, R. Zellers, N. A. Smith, and Y. Choi
NeuroLogic a*esque decoding: constrained text generation with lookahead heuristics
.
External Links:
2112.08726
,
Link
Cited by:
§1
,
§3.3
.
Nan
et al.
(2025)
Z. Nan, Z. Guo, K. Liu, and X. Xia
Test Intention Guided LLM-based Unit Test Generation
.
In
2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)
,
Vol.
,
Los Alamitos, CA, USA
,
pp. 779–779
.
External Links:
ISSN 1558-1225
,
Document
,
Link
Cited by:
§7.1
.
Pinnaparaju
et al.
(2023)
N. Pinnaparaju, R. Adithyan, D. Phung, J. Tow, J. Baicoianu, and N. Cooper
Stable code 3b
.
Note:
https://huggingface.co/stabilityai/stable-code-3b
Cited by:
§2.1.1
.
Radford
et al.
(2019)
A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever
Language models are unsupervised multitask learners
.
Technical report
OpenAI
.
Note:
Accessed: 2024-11-15
External Links:
Link
Cited by:
§1
,
1st item
.
Reimers and Gurevych (2019)
N. Reimers and I. Gurevych
Sentence-bert: sentence embeddings using siamese bert-networks
.
External Links:
1908.10084
,
Link
Cited by:
§3.2.1
.
Rozière
et al.
(2024)
B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez, J. Rapin, A. Kozhevnikov, I. Evtimov, J. Bitton, M. Bhatt, C. C. Ferrer, A. Grattafiori, W. Xiong, A. Défossez, J. Copet, F. Azhar, H. Touvron, L. Martin, N. Usunier, T. Scialom, and G. Synnaeve
Code llama: open foundation models for code
.
External Links:
2308.12950
,
Link
Cited by:
§1
.
Ryan
et al.
(2024)
G. Ryan, S. Jain, M. Shang, S. Wang, X. Ma, M. K. Ramanathan, and B. Ray
Code-aware prompting: a study of coverage-guided test generation in regression setting using llm
.
Proc. ACM Softw. Eng.
1
(
FSE
).
External Links:
Link
,
Document
Cited by:
§7.1
.
Shannon (1948)
C. E. Shannon
A mathematical theory of communication
.
The Bell System Technical Journal
27
(
3
),
pp. 379–423
.
External Links:
Document
Cited by:
§1
,
§2.2
.
Sun
et al.
(2024)
Z. Sun, C. Lyu, B. Li, Y. Wan, H. Zhang, G. Li, and Z. Jin
Enhancing code generation performance of smaller models by distilling the reasoning ability of llms
.
External Links:
2403.13271
,
Link
Cited by:
§1
,
§7.1
.
Team (2025)
Q. Team
Qwen3 technical report
.
External Links:
2505.09388
,
Link
Cited by:
§2.1.1
.
Tian
et al.
(2024)
Z. Tian, J. Chen, and X. Zhang
Fixing large language models’ specification misunderstanding for better code generation
.
External Links:
2309.16120
,
Link
Cited by:
§1
,
§7.1
.
Ugare
et al.
(2024)
S. Ugare, T. Suresh, H. Kang, S. Misailovic, and G. Singh
SynCode: llm generation with grammar augmentation
.
External Links:
2403.01632
,
Link
Cited by:
§1
,
§7.1
.
Xia and Zhang (2022)
C. S. Xia and L. Zhang
Less training, more repairing please: revisiting automated program repair via zero-shot learning
.
In
Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering
,
ESEC/FSE 2022
,
New York, NY, USA
,
pp. 959–971
.
External Links:
ISBN 9781450394130
,
Link
,
Document
Cited by:
§1
,
§7.1
.
Yang
et al.
(2024)
L. Yang, C. Yang, S. Gao, W. Wang, B. Wang, Q. Zhu, X. Chu, J. Zhou, G. Liang, Q. Wang, and J. Chen
On the evaluation of large language models in unit test generation
.
External Links:
2406.18181
,
Link
Cited by:
§7.1
.
Yuan
et al.
(2023)
Z. Yuan, J. Liu, Q. Zi, M. Liu, X. Peng, and Y. Lou
Evaluating instruction-tuned large language models on code comprehension and generation
.
External Links:
2308.01240
,
Link
Cited by:
§1
,
§7.1
.
Yuan
et al.
(2024)
Z. Yuan, M. Liu, S. Ding, K. Wang, Y. Chen, X. Peng, and Y. Lou
Evaluating and improving chatgpt for unit test generation
.
Proc. ACM Softw. Eng.
1
(
FSE
).
External Links:
Link
,
Document
Cited by:
§7.1
.
Zhang
et al.
(2024)
Y. Zhang, W. Zhang, D. Ran, Q. Zhu, C. Dou, D. Hao, T. Xie, and L. Zhang
Learning-based widget matching for migrating gui test cases
.
In
Proceedings of the IEEE/ACM 46th International Conference on Software Engineering
,
ICSE ’24
,
New York, NY, USA
.
External Links:
ISBN 9798400702174
,
Link
,
Document
Cited by:
§7.1
.
Zhu
et al.
(2025)
Y. Zhu, G. Li, X. Jiang, J. Li, H. Mei, Z. Jin, and Y. Dong
Uncertainty-guided chain-of-thought for code generation with llms
.
External Links:
2503.15341
,
Link
Cited by:
§1
,
§4.1
,
§7.2
.
Zhu
et al.
(2023)
Y. Zhu, J. Li, G. Li, Y. Zhao, J. Li, Z. Jin, and H. Mei
Hot or cold? adaptive temperature sampling for code generation with large language models
.
External Links:
2309.02772
,
Link
Cited by:
§1
,
3rd item
,
§7.2
.
Zhuo
et al.
(2025)
T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf, H. Zhan, J. He, I. Paul, S. Brunner, C. Gong, T. Hoang, A. R. Zebaze, X. Hong, W. Li, J. Kaddour, M. Xu, Z. Zhang, P. Yadav, N. Jain, A. Gu, Z. Cheng, J. Liu, Q. Liu, Z. Wang, B. Hui, N. Muennighoff, D. Lo, D. Fried, X. Du, H. de Vries, and L. V. Werra
BigCodeBench: benchmarking code generation with diverse function calls and complex instructions
.
External Links:
2406.15877
,
Link
Cited by:
§3.2.1
.