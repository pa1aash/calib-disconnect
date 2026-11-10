---
title: 'DreamPRM-Code: Function-as-Step Process Reward Model with Label Correction
  for LLM Coding'
id: dreamprm-code-function-as-step-process-reward-model-with-label-correction-for-ll
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:07:52.929351Z'
updated: '2026-11-09T23:27:44.393351Z'
source: https://arxiv.org/html/2512.15000
source_domain: arxiv.org
fetched_at: '2026-11-09T23:07:52.928963Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Full text. DreamPRM-Code: function-as-step PRM with Chain-of-Function and
  bi-level label correction from unit-test labels; 80.9 pass@1 LiveCodeBench (+3.8
  over o4-mini-high). RELATED to L4 (function-level scoring for best-of-N, not calibrated
  confidence or repair).'
---

DreamPRM-Code: Function-as-Step Process Reward Model with Label Correction for LLM Coding
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2512.15000v1 [cs.LG] 17 Dec 2025
DreamPRM-Code: Function-as-Step Process Reward Model with Label Correction for LLM Coding
Ruiyi Zhang
Affiliation:
University of California, San Diego
Peijia Qin
Affiliation:
University of California, San Diego
Qi Cao
Affiliation:
University of California, San Diego
Pengtao Xie
Affiliation:
University of California, San Diego
Correspondence to:
p1xie@ucsd.edu
Abstract
Process Reward Models (PRMs) have become essential for improving Large Language Models (LLMs) via test-time scaling, yet their effectiveness in coding remains limited due to the lack of meaningful step decompositions in code and the noise of Monte-Carlo–generated partial labels. We propose DreamPRM-Code, a coding-focused PRM that treats functions as reasoning steps using a Chain-of-Function prompting strategy to induce modular code generation, enabling PRM training and application analogous to mathematical reasoning tasks. To address label noise, DreamPRM-Code introduces a meta-learning–based correction mechanism that leverages clean final-solution unit-test labels and performs bi-level optimization to refine intermediate labels. Applying on test-time scaling, DreamPRM-Code achieved state-of-the-art performance on LiveCodeBench with 80.9 pass@1 rate, surpassing OpenAI o4-mini.
Project Page:
[DreamPRM-Code]
Keywords:
Machine Learning, ICML
1
Introduction
Post-training methods for Large Language Models (LLMs)
(
Brown et al., 2020
;
Qiu et al., 2025
)
, such as Reinforcement Learning from Human Feedback (RLHF)
(
Ouyang et al., 2022
)
and test-time scaling
(
OpenAI et al., 2024
;
Guo et al., 2025
)
, have proven effective for improving model capability. In this process, Process Reward Models (PRMs), which take in a partial reasoning state of an LLM and output a correctness score, have emerged as a promising method
(
Wang et al., 2024
;
Zhang et al., 2024
;
Cao et al., 2025
)
. They are capable of (1) simulating costly human-feedback rewards to conduct reinforcement learning for LLMs
(
Zou et al., 2025
)
and (2) supporting test-time scaling of LLMs via PRM-selected best-of-N or tree search methods
(
Setlur et al., 2025
)
.
Although PRMs have seen widespread success in mathematical reasoning tasks, their application to coding tasks remains limited. While solving both coding and mathematical problems requires strong reasoning capability from LLMs, two challenges prevent PRMs from being effectively used for coding. First, most modern PRMs require LLM-generated text to be separated into meaningful steps. Unlike Chain-of-Thought (CoT) reasoning in mathematics
(
Wei et al., 2022
)
, which naturally decomposes into steps, LLM-generated code lacks a clear definition of such “steps.” Some existing works use a line of code as a reasoning step, which significantly increases computation cost due to too many steps
(
Wang et al., 2024
)
. Other define steps in natural-language-based planning processes instead of in the generated code, ignoring inherent reasoning process in programming code itself
(
Li et al., 2025
)
. Second, PRMs are typically trained with Monte-Carlo-generated pseudo-labels for the correctness of each partial reasoning state. These labels can be quite noisy and ultimately reduce PRM performance.
To tackle these challenges, we propose a novel method called DreamPRM-Code. To tackle the first challenge, the proposed method leverages a novel Chain-of-Function prompting strategy to use functions as PRM steps. To address the second challenge, DreamPRM-Code contains a novel label correction method to automatically purify noisy middle-step PRM labels via meta learning. We benchmark DreamPRM-Code on
(
Jain et al., 2025
)
and achieved 80.9 pass@1 rate, surpassing the strongest existing model, OpenAI o4-mini
(
OpenAI, 2025
)
, and other baseline test-time scaling methods.
2
Method
In this section, we describe the proposed DreamPRM-Code framework in detail. DreamPRM-Code is a coding-focused Process Reward Model that defines reasoning steps at the level of functions in the generated code and incorporates a label-correction mechanism to improve training signal quality.
2.1
Chain-of-Function as PRM Steps
To address the first challenge outlined in the previous section, namely the absence of a natural step decomposition in code, we introduce a Chain-of-Function prompting strategy designed to encourage LLMs to generate modular, well-structured programs. This prompt steers the model toward producing independent code blocks whose logic can be isolated and encapsulated into separate functions. Inspired by Chain-of-Thought prompting, where high-level plans are produced before detailed reasoning, Chain-of-Function encourages the model to generate high-level functions early, providing a blueprint that guides the construction of more specific helper functions. Under this structure, DreamPRM-Code can treat each function as a coherent reasoning step, enabling the direct adaptation of standard PRM training and inference pipelines commonly used in mathematical reasoning tasks.
Algorithm
1
illustrates an example decomposition under the Chain-of-Function paradigm, where a model-generated solution is separated into three PRM steps. In the first step, a
main
function is introduced to select Dijkstra’s algorithm as the appropriate approach for the problem. The remaining two steps implement the
dijkstra
and
build_graph
functions, which are invoked within
main
to complete the overall solution. This structured decomposition not only provides clear intermediate reasoning states for PRM evaluation but also aligns closely with human software-engineering practices, enabling more interpretable and modular code generation.
Algorithm 1
An Example of Chain-of-Function Definition for PRM Steps in LLM Generated Code
Chain-of-Function Prompt
You will be given a question (problem specification) and will generate a correct Python program that matches the specification and passes all tests. You should follow the code organization guidelines:
1. Function Organization: Place high-level solving functions first (e.g., “main()”, primary algorithm). Follow with helper functions that implement specific subtasks. Avoid nested functions; keep all functions at the top level.
2. Write Docstrings in Each Function (Chain of Thought): Add a docstring using triple quotes (
’’’
) at the beginning of each function. Main methods should explain the approach, algorithm choice, strategy, and key steps; helper methods should explain their specific logic and purpose.
3. Extract logic into separate methods when operations are repeated or complex calculations can be isolated.
LLM Generated Code
(Step-1)
def main():
’’’
Strategy: Use Dijkstra’s algorithm to find shortest path in weighted graph…
’’’
[Code Block]
(Step-2)
def dijkstra(graph, start, end):
’’’
Implements Dijkstra’s algorithm using min-heap priority queue…
’’’
[Code Block]
(Step-3)
def build_graph(n, m):
’’’
Build adjacency list from stdin input…
’’’
[Code Block]
2.2
Automatic Label Correction with Meta Learning
To address the second challenge, we propose a meta learning based label correction framework
(
Tu et al., 2023
;
Tong et al., 2025
;
Taraday and Baskin, 2023
;
Wu et al., 2020
)
that explicitly denoises MC sampled PRM labels. In coding tasks, we can leverage a private unit test evaluation system to obtain clean and reliable correctness labels once the LLM completes code generation. These final step labels provide strong supervision signals that are not available in mathematical reasoning tasks, where intermediate and final reasoning states typically lack automatic evaluation. DreamPRM-Code exploits this unique property of coding problems to improve the quality of intermediate supervision.
Specifically, we consider two sources of data: clean last step PRM data
(
X
meta
,
Y
meta
)
(X_{\text{meta}},Y_{\text{meta}})
obtained from unit test evaluation, and noisy middle step data
(
X
,
Y
)
(X,Y)
obtained through MC sampling. Since the middle step labels may be inaccurate, we treat the noisy labels
Y
Y
as learnable parameters rather than fixed targets, and optimize them using meta learning. This allows the model to adaptively correct label noise based on performance on clean final step data.
The proposed approach follows a bi-level optimization framework. In the lower level, we train the PRM
f
θ
f_{\theta}
on the middle step data using the current estimate of noisy labels. The PRM parameters are updated by minimizing the training loss:
θ
∗
​
(
Y
)
=
arg
​
min
θ
⁡
ℒ
​
(
f
θ
​
(
X
)
,
Y
)
,
\theta^{*}(Y)=\argmin_{\theta}\mathcal{L}\big(f_{\theta}(X),Y\big),
(1)
where the optimized parameter
θ
∗
\theta^{*}
depends implicitly on the labels
Y
Y
. In the upper level, we evaluate the optimized PRM
f
θ
∗
​
(
Y
)
f_{\theta^{*}(Y)}
on the clean last step data and compute a meta loss with respect to the ground truth labels
Y
meta
Y_{\text{meta}}
:
min
Y
⁡
ℒ
⁡
(
f
θ
∗
​
(
Y
)
​
(
X
meta
)
,
Y
meta
)
.
\min_{Y}\,\mathcal{L}\big(f_{\theta^{*}(Y)}(X_{\text{meta}}),Y_{\text{meta}}\big).
(2)
Because the meta loss depends on
θ
∗
\theta^{*}
and therefore on the middle step labels
Y
Y
, minimizing this objective encourages label assignments that lead to PRM parameters generalizing well to clean final step supervision. In practice, we solve this nested optimization by alternately updating the PRM parameters and the noisy labels using gradient descent. Through this iterative process, DreamPRM-Code progressively refines the middle step labels, producing denoised training signals that improve PRM robustness and downstream performance in both test time scaling and reinforcement learning settings. A complete illustration of the label correction process is shown in Figure
1
.
Figure 1
:
The meta-learning based label correction framework in DreamPRM-Code.
The parameters of the PRM are first optimized using noisy data. The updated PRM is then applied on clean data to compute a loss, which is then used for optimize label of the noisy data used in previous step.
3
Results
3.1
Experimental Settings
We evaluate DreamPRM-Code primarily on LiveCodeBench (LCB)
(
Jain et al., 2025
)
, a comprehensive and contamination-free benchmark for code generation with large language models. LiveCodeBench continuously collects newly released programming problems from competitive programming platforms such as LeetCode, AtCoder, and Codeforces. Each problem is associated with a timestamp indicating its publication date. In our experiments, we use 601 problems published before 2024-08-01 as the training split for PRM, and 131 problems published after 2025-02-01 as the test split, ensuring a strict temporal separation and no data overlap.
During the training of DreamPRM-Code, we use Qwen3-Coder-30B-A3B
(
Yang et al., 2025
)
to generate both Chain-of-Function (CoF) trajectories for PRM training and Monte Carlo (MC)–sampled labels. We adopt Qwen-2.5-Coder-3B as the process reward model (PRM)
(
Qwen et al., 2024
)
. Specifically, we replace the final language-model head with a classification head to output step-level reward scores. We train the PRM using the Adam optimizer
(
Kingma and Ba, 2014
)
with a learning rate of
10
−
4
10^{-4}
, a meta-learning rate of
10
−
2
10^{-2}
, and a weight decay of
10
−
2
10^{-2}
. We use a batch size of 8 and set the meta-learning unroll step to 1. The bi-level optimization procedure for label correction is implemented using the Betty library
(
Choe et al., 2023
)
.
For test-time scaling, we use OpenAI o4-mini-high as the base (policy) model
(
OpenAI, 2025
)
. For each problem, the base LLM generates four candidate solutions, from which DreamPRM-Code selects the final output. We apply mean aggregation over the per-step reward scores produced by DreamPRM-Code to obtain a final score for each candidate.
3.2
Baselines
We compare DreamPRM-Code against two categories of baselines. First, we consider leading LLMs on LiveCodeBench without test-time scaling, including o4-mini-high
(
OpenAI, 2025
)
, Gemini-2.5
(
Comanici and others, 2025
)
, DeepSeek R1
(
Guo et al., 2025
)
, and the o3 models.
Second, we evaluate alternative test-time scaling approaches, including outcome reward models (ORMs), which assign a single reward score to the entire generated solution rather than per-step rewards
(
Uesato et al., 2022
)
. We also include an ablation baseline of DreamPRM-Code without label correction (PRM-CoF).
3.3
Results on LiveCodeBench
Table 1
:
Performance comparison of DreamPRM-Code and baseline methods across Easy, Medium, and Hard difficulty levels on LiveCodeBench. Results include top-performing LLMs from the leaderboard and test-time scaling methods applied to O4-mini-high, with results reported as pass@1 percentages.
Easy
Medium
Hard
Overall
Top LLMs on the Leaderboard
Gemini-2.5
100
82.1
52.5
72.5
O3
100
71.8
57.4
71.8
DeepSeek-R1
99.7
77.7
47.2
68.7
O4-mini-high
100
89.7
57.4
77.1
Test-Time Scaling Methods (O4-mini-high)
ORM
100
89.7
62.3
79.4
DreamPRM-Code
100
92.3
63.9
80.9
The results of DreamPRM-Code and all baselines are reported in Table
1
. Compared to leading proprietary models on the LiveCodeBench leaderboard, DreamPRM-Code outperforms the strongest baseline, o4-mini-high, by 3.8 points in pass@1 accuracy. We further compare DreamPRM-Code with other test-time scaling methods under the same base model, o4-mini-high. DreamPRM-Code consistently outperforms ORM-based scaling, highlighting the advantage of decomposing code generation into intermediate steps and assigning rewards at a finer granularity, and underscoring the importance of our Chain-of-Function (CoF) formulation. In summary, the state-of-the-art performance of DreamPRM-Code demonstrates the effectiveness of our proposed approach.
3.4
Ablation Study
Table 2
:
Performance comparison between DreamPRM-Code and its ablation baseline, DreamPRM-Code without the label correction mechanism (PRM-CoF).
Easy
Medium
Hard
Overall
PRM-CoF
100
92.3
62.3
80.2
DreamPRM-Code
100
92.3
63.9
80.9
In this section, we conduct an ablation study to investigate the effectiveness of the label correction mechanism in DreamPRM-Code by comparing it with an ablation baseline in which PRMs are trained on CoF trajectories using traditional MC-sampled labels without label correction. As shown in Table
2
, DreamPRM-Code outperforms this ablation baseline (PRM-CoF), demonstrating the effectiveness of the proposed label correction framework.
4
Conclusion
In this paper, we propose DreamPRM-Code, a process reward model designed for large language model–based code generation. DreamPRM-Code introduces a novel Chain-of-Function prompting strategy to explicitly define and generate fine-grained PRM steps, along with a meta-learning–based label correction approach to mitigate noise in intermediate-step training labels. When applied to test-time scaling, DreamPRM-Code achieves state-of-the-art performance on LiveCodeBench, attaining an 80.9 pass@1 score and outperforming OpenAI o4-mini as well as other test-time scaling baselines. These results demonstrate the effectiveness of DreamPRM-Code in improving step-level reasoning quality and overall code generation performance.
References
Brown
et al.
(2020)
T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei
Language models are few-shot learners
.
In
Advances in Neural Information Processing Systems 33 (NeurIPS 2020)
,
Cited by:
§1
.
Cao
et al.
(2025)
Q. Cao, R. Wang, R. Zhang, S. A. Somayajula, and P. Xie
DreamPRM: domain-reweighted process reward model for multimodal reasoning
.
In
The Thirty-ninth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.
Choe
et al.
(2023)
S. K. Choe, W. Neiswanger, P. Xie, and E. Xing
Betty: an automatic differentiation library for multilevel optimization
.
In
The Eleventh International Conference on Learning Representations
,
External Links:
Link
Cited by:
§3.1
.
Comanici
et al.
(2025)
G. Comanici
et al.
Gemini 2.5: pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities
.
ArXiv
abs/2507.06261
.
External Links:
Link
Cited by:
§3.2
.
Guo
et al.
(2025)
D. Guo, D. Yang, H. Zhang,
et al.
DeepSeek-r1 incentivizes reasoning in llms through reinforcement learning
.
Nature
645
,
pp. 633–638
.
External Links:
Document
,
Link
Cited by:
§1
,
§3.2
.
Jain
et al.
(2025)
N. Jain, K. Han, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica
LiveCodeBench: holistic and contamination free evaluation of large language models for code
.
In
The Thirteenth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
,
§3.1
.
Kingma and Ba (2014)
D. P. Kingma and J. Ba
Adam: a method for stochastic optimization
.
CoRR
abs/1412.6980
.
External Links:
Link
Cited by:
§3.1
.
Li
et al.
(2025)
Q. Li, X. Dai, X. Li, W. Zhang, Y. Wang, R. Tang, and Y. Yu
CodePRM: execution feedback-enhanced process reward model for code generation
.
In
Findings of the Association for Computational Linguistics: ACL 2025
,
W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.)
,
Vienna, Austria
,
pp. 8169–8182
.
External Links:
Link
,
Document
,
ISBN 979-8-89176-256-5
Cited by:
§1
.
OpenAI
et al.
(2024)
OpenAI, A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel,
et al.
OpenAI o1 system card
.
arXiv preprint arXiv:2412.16720
.
External Links:
Document
,
Link
Cited by:
§1
.
OpenAI (2025)
OpenAI
OpenAI o3 and o4-mini system card
.
Note:
https://openai.com/index/o3-o4-mini-system-card/
Accessed: 2025-12-15
Cited by:
§1
,
§3.1
,
§3.2
.
Ouyang
et al.
(2022)
L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano, J. Leike, and R. Lowe
Training language models to follow instructions with human feedback
.
In
Advances in Neural Information Processing Systems 35 (NeurIPS 2022)
,
Cited by:
§1
.
Qiu
et al.
(2025)
Z. Qiu, Z. Wang, B. Zheng, Z. Huang, K. Wen, S. Yang, R. Men, L. Yu, F. Huang, S. Huang, D. Liu, J. Zhou, and J. Lin
Gated attention for large language models: non-linearity, sparsity, and attention-sink-free
.
In
The Thirty-ninth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.
Qwen
et al.
(2024)
Qwen, A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, G. Dong, H. Wei, H. Lin, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Lin, K. Dang, K. Lu, K. Bao, K. Yang, L. Yu, M. Li, M. Xue, P. Zhang, Q. Zhu, R. Men, R. Lin, T. Li, T. Xia, X. Ren, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Wan, Y. Liu, Z. Cui, Z. Zhang, Z. Qiu, S. Quan, and Z. Wang
Qwen2.5 technical report
.
ArXiv
abs/2412.15115
.
External Links:
Link
Cited by:
§3.1
.
Setlur
et al.
(2025)
A. Setlur, C. Nagpal, A. Fisch, X. Geng, J. Eisenstein, R. Agarwal, A. Agarwal, J. Berant, and A. Kumar
Rewarding progress: scaling automated process verifiers for LLM reasoning
.
In
The Thirteenth International Conference on Learning Representations
,
External Links:
Link
Cited by:
§1
.
Taraday and Baskin (2023)
M. K. Taraday and C. Baskin
Enhanced meta label correction for coping with label corruption
.
In
Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)
,
pp. 16295–16304
.
Cited by:
§2.2
.
Tong
et al.
(2025)
T. Tong, Y. Mo, Y. Xie, S. Cai, X. Shi, and X. Zhu
Meta label correction with generalization regularizer
.
In
Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence
,
IJCAI ’25
.
External Links:
ISBN 978-1-956792-06-5
,
Link
,
Document
Cited by:
§2.2
.
Tu
et al.
(2023)
Y. Tu, B. Zhang, Y. Li, L. Liu, J. Li, J. Zhang, Y. Wang, C. Wang, and C. R. Zhao
Learning from noisy labels with decoupled meta label purifier
.
2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
,
pp. 19934–19943
.
External Links:
Link
Cited by:
§2.2
.
Uesato
et al.
(2022)
J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang, A. Creswell, G. Irving, and I. Higgins
Solving math word problems with process- and outcome-based feedback
.
ArXiv
abs/2211.14275
.
External Links:
Link
Cited by:
§3.2
.
Wang
et al.
(2024)
Z. Wang, Y. Li, Y. Wu, L. Luo, L. Hou, H. Yu, and J. Shang
Multi-step problem solving through a verifier: an empirical analysis on model-induced process supervision
.
In
Findings of the Association for Computational Linguistics: EMNLP 2024
,
Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.)
,
Miami, Florida, USA
,
pp. 7309–7319
.
External Links:
Link
,
Document
Cited by:
§1
,
§1
.
Wei
et al.
(2022)
J. Wei, X. Wang, D. Schuurmans, M. Bosma, brian ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou
Chain of thought prompting elicits reasoning in large language models
.
In
Advances in Neural Information Processing Systems
,
A. H. Oh, A. Agarwal, D. Belgrave, and K. Cho (Eds.)
,
External Links:
Link
Cited by:
§1
.
Wu
et al.
(2020)
Y. Wu, J. Shu, Q. Xie, Q. Zhao, and D. Meng
Learning to purify noisy labels via meta soft label corrector
.
In
AAAI Conference on Artificial Intelligence
,
External Links:
Link
Cited by:
§2.2
.
Yang
et al.
(2025)
A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu
Qwen3 technical report
.
ArXiv
abs/2505.09388
.
External Links:
Link
Cited by:
§3.1
.
Zhang
et al.
(2024)
D. Zhang, S. Zhoubian, Z. Hu, Y. Yue, Y. Dong, and J. Tang
ReST-MCTS*: LLM self-training via process reward guided tree search
.
In
The Thirty-eighth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.
Zou
et al.
(2025)
J. Zou, L. Yang, J. Gu, J. Qiu, K. Shen, J. He, and M. Wang
ReasonFlux-PRM: trajectory-aware PRMs for long chain-of-thought reasoning in LLMs
.
In
The Thirty-ninth Annual Conference on Neural Information Processing Systems
,
External Links:
Link
Cited by:
§1
.