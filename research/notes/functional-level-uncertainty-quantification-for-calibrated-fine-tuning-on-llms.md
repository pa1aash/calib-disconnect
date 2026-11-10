---
title: Functional-level Uncertainty Quantification for Calibrated Fine-tuning on LLMs
id: functional-level-uncertainty-quantification-for-calibrated-fine-tuning-on-llms
tags:
- code-llm-confidence-positioning-d82d00
- off-target
created: '2026-11-09T23:17:33.809291Z'
updated: '2026-11-09T23:27:44.779797Z'
source: https://arxiv.org/html/2410.06431
source_domain: arxiv.org
fetched_at: '2026-11-09T23:17:33.808004Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT (arXiv 2410.06431 v5). UQ4CT = Functional-level UQ for Calibrated
  Fine-tuning: MoE-LoRA calibration loss reducing ECE by over 25% on multiple-choice
  and open-ended QA with Llama3.1-8B. NOT a code-uncertainty paper; the batch lead
  ''UQ4CT (code uncertainty)'' is a mis-description.'
---

Functional-level Uncertainty Quantification for Calibrated Fine-tuning on LLMs
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2410.06431v5 [cs.LG] 13 May 2026
Functional-level Uncertainty Quantification for Calibrated Fine-tuning on LLMs
Ruijia Niu
Dongxia Wu
Rose Yu
Yi-An Ma
Abstract
Accurate uncertainty quantification in large language models (LLMs) is essential for reliable confidence estimation, yet fine-tuned LLMs often become overconfident under limited adaptation data. Existing uncertainty methods for PEFT-based LLMs are largely post hoc, estimating uncertainty after fine-tuning rather than improving how adapters specialize to task-specific input-output relationships. We propose Functional-Level Uncertainty Quantification for Calibrated Fine-Tuning (UQ4CT), which calibrates uncertainty over the functional space induced by prompt-dependent mixtures of LoRA experts. UQ4CT implements this perspective through a mixture-of-experts fine-tuning framework, where a calibration loss aligns functional-level confidence with predictive correctness during training. Across four multiple-choice benchmarks and two open-ended generative QA tasks, UQ4CT reduces Expected Calibration Error (ECE) by over
25
%
25\%
while preserving high accuracy. Under distribution shift, UQ4CT maintains superior calibration and competitive accuracy, demonstrating improved reliability and generalization for fine-tuned LLMs.
1
1
footnotetext:
Department of Computer Science and Engineering, University of California San Diego, La Jolla, California, USA
2
2
footnotetext:
Halıcıoğlu Data Science Institute, University of California San Diego, La Jolla, California, USA
†
†
footnotetext:
Preprint. Correspondence to: Yian Ma <yianma@ucsd.edu>.
1
Introduction
Quantifying the credibility of outputs has been one of the most important problems around large language models (LLMs)
(
Chang et al., 2024
)
. In particular, fine-tuned LLMs often struggle with overconfidence in their outputs due to limited training data, failing to reflect the true credibility of their answers
(
Xiao et al., 2022
;
He et al., 2023
;
Tian et al., 2023
;
OpenAI, 2023
)
. Such overconfidence can assert misinformation with high certainty, making it difficult for users to discern truth from falsehood. This has become a crucial problem in safety-critical decision making and scientific domains where data is relatively limited, such as formal proof generation, climate science, and healthcare
(
Singhal et al., 2022
;
Wu et al., 2023a
;
Lampinen et al., 2023
;
Li et al., 2022
)
. Methods that enhance uncertainty quantification for fine-tuned LLMs are therefore essential to ensure trustworthy predictions.
A key challenge in LLM uncertainty quantification is balancing accuracy, calibration, and efficiency: uncertainty estimates should be calibrated without degrading predictive performance or slowing generation. Existing methods often rely on prompt perturbations to measure prediction variance
(
Hou et al., 2023
;
Gao et al., 2024
)
or multiple sampled completions to estimate disagreement
(
Farquhar et al., 2024
)
. However, these approaches largely assume the model is already aligned with the target data distribution, limiting their ability to capture fine-tuning-induced uncertainty and generalization gaps under limited adaptation data. Their reliance on multiple forward passes also introduces substantial computational overhead, reducing scalability.
Beyond prompt-level approaches, Bayesian methods and ensemble-based uncertainty quantification have been established for fine-tuned LLMs, often in conjunction with low-rank adaptation(LoRA)
(
Hu et al., 2021a
)
. Methods such as Monte Carlo dropout
(
Gal and Ghahramani, 2016
)
, checkpoint ensembles
(
Chen et al., 2017
)
, deep ensembles
(
Lakshminarayanan et al., 2017
;
Wang et al., 2023
;
Zhai et al., 2023
)
, and Laplace-LoRA
(
Yang et al., 2024a
)
apply Bayesian inference or ensembling over LoRA parameters to capture uncertainty arising from model adaptation and limited data.
While Bayesian and ensemble methods estimate uncertainty after fine-tuning by analyzing the learned parameter space, they do not address the limitations caused by sparse data during fine-tuning. This post hoc perspective can miss uncertainty that arises when adapting to new tasks with limited data.
Figure 1:
Left: The MoE architecture captures diverse functional relationships by dynamically routing inputs to different expert modules based on the prompt. Right: The standard LoRA approach lacks such functional-space diversity, limiting its capacity to capture variations in the functional relationships during fine-tuning.
To overcome this, we shift focus from parameter-space to functional-space uncertainty quantification. The functional space encompasses the input-output mappings the model can realize, capturing the true variability in its predictions. By calibrating uncertainty at this level during fine-tuning, we ensure the model’s confidence better reflects its actual predictive reliability.
We therefore introduce Functional-Level Uncertainty Quantification for Calibrated Fine-Tuning (UQ4CT), a method that explicitly calibrates functional-level uncertainty in LLMs during fine-tuning. As demonstrated in
Figure
1
, UQ4CT leverages ensembles of LoRA modules at each layer to construct a rich set of basis functions. We then employ a Mixture-of-Experts (MoE) architecture
(
Li et al., 2024
)
to hierarchically combine these basis functions, forming a flexible functional space. During fine-tuning, UQ4CT jointly learns the LoRA expert parameters and calibrates the prompt-dependent function mixture to align functional-level uncertainty with predictive correctness, enabling the model to output calibrated distributions over the functional space.
During inference, LoRA experts offer diverse functional relationships acquired during fine-tuning, while MoE routers dynamically select the most relevant experts for each input prompt. This selection is guided by functional-level uncertainty calibration performed throughout fine-tuning, which aims to optimize the choice of the correct functional relationship for each prompt. More accurate expert selection enables the model to learn diverse functional relationships. As a result, the model’s uncertainty estimates become better aligned, enhancing calibration without compromising accuracy.
To summarize, our contributions include:
•
A novel uncertainty quantification approach for LLMs with MoE architecture during fine-tuning to quantify functional-level uncertainty and align with the probability of predictive correctness, which mitigates overconfidence issue and improves generalizability.
•
A new calibration loss incorporating predictive correctness to dynamically align the prompt-dependent LoRA mixture for better uncertainty estimation.
•
Hierarchical decomposition of functional-level uncertainty into layer-wise mixture weights with guarantee that our calibration loss aligns mixture weights with predictive correctness.
•
Empirically, UQ4CT achieves over
25
%
25\%
ECE reduction on
3
3
common-sense reasoning tasks and
1
1
domain-specific question answering task while preserving high accuracy. Under distribution shift, UQ4CT maintains superior calibration on
2
2
common-sense reasoning tasks and
4
4
domain-specific tasks. Experiments on open-ended generative QA further suggest that the functional-space calibration perspective extends beyond classification-style settings.
2
Preliminaries
Low-rank Adaptation (LoRA).
LLMs have numerous large weight matrices to perform matrix multiplication, denoted as
𝐖
0
∈
ℝ
n
out
×
n
in
\mathbf{W}_{0}\in\mathbb{R}^{n_{\text{out}}\times n_{\text{in}}}
that maps inputs
𝐱
\mathbf{x}
to outputs
𝐡
\mathbf{h}
.
Hu et al. (2021a)
proposes LoRA, which fixes
𝐖
0
\mathbf{W}_{0}
and introduces a low-rank perturbation
Δ
​
𝐖
\Delta\mathbf{W}
to the weight matrix:
𝐡
\displaystyle\mathbf{h}
=
𝐖
0
​
𝐱
+
Δ
​
𝐖𝐱
=
𝐖
0
​
𝐱
+
𝐁𝐀𝐱
.
\displaystyle=\mathbf{W}_{0}\mathbf{x}+\Delta\mathbf{W}\mathbf{x}=\mathbf{W}_{0}\mathbf{x}+\mathbf{B}\mathbf{A}\mathbf{x}.
(1)
Here,
Δ
​
𝐖
\Delta\mathbf{W}
is calculated as the product of two matrices,
𝐁
∈
ℝ
n
out
×
n
lr
\mathbf{B}\in\mathbb{R}^{n_{\text{out}}\times n_{\text{lr}}}
and
𝐀
∈
ℝ
n
lr
×
n
in
\mathbf{A}\in\mathbb{R}^{n_{\text{lr}}\times n_{\text{in}}}
where
n
lr
n_{\text{lr}}
is significantly smaller than
n
in
n_{\text{in}}
or
n
out
n_{\text{out}}
. For example, we use
n
lr
=
32
n_{\text{lr}}=32
while
n
in
=
n
out
=
4096
n_{\text{in}}=n_{\text{out}}=4096
for the Llama3.1-8B model
(
Grattafiori et al., 2024
)
. Therefore, the total number of LoRA parameters for this
Δ
​
𝐖
\Delta\mathbf{W}
is
n
lr
​
(
n
in
+
n
out
)
n_{\text{lr}}(n_{\text{in}}+n_{\text{out}})
, which is far smaller than the parameter count of the full matrix,
n
in
​
n
out
n_{\text{in}}n_{\text{out}}
. One of the key motivations of incorporating LoRA to fine-tune LLMs is the vast amount of memory cost reduction compared with fine-tuning on the full model. For an LLM with
7
7
billion parameters, maintaining the average gradient
and average squared gradients for optimization multiplies the memory required by a factor of
3
3
compared to simply loading model weights. LoRA greatly mitigates this memory cost as the tripled memory consumption only applies to LoRA adapters.
Mixture of Experts (MoE).
LoRA Mixture-of-Experts
(
Li et al., 2024
;
Wu et al., 2024b
)
is an efficient approach to scale the number of parameters while maintaining the same computational bounds. LoRA MoE utilizes the top-k router to assign each token to the LoRA experts
(
Lepikhin et al., 2020
)
. The router is a linear layer that maps the input hidden state
𝐡
\mathbf{h}
to a probability distribution of candidate experts.
The plain transformer block in a large language model consists of the
q
,
k
,
v
q,k,v
encoding layers (
FFN
q
,
k
,
v
\text{FFN}_{q,k,v}
),
layer norm (LN) and the feedforward layer (FFN), together with residual connections. Formally, given
𝐡
1
\mathbf{h}^{1}
as the tokenized input text, the output of
ℓ
\ell
-th layer is generated as:
𝐳
ℓ
=
f
a
​
t
​
t
​
n
​
(
FFN
q
,
k
,
v
​
(
LN
​
(
𝐡
ℓ
−
1
)
)
)
+
𝐡
ℓ
−
1
,
𝐡
ℓ
=
FFN
​
(
LN
​
(
𝐳
ℓ
)
)
+
𝐳
ℓ
.
\mathbf{z}^{\ell}=f_{attn}(\text{FFN}_{q,k,v}(\text{LN}(\mathbf{h}^{\ell-1})))+\mathbf{h}^{\ell-1},\quad\mathbf{h}^{\ell}=\text{FFN}(\text{LN}(\mathbf{z}^{\ell}))+\mathbf{z}^{\ell}.
(2)
Here,
f
a
​
t
​
t
​
n
f_{attn}
represents the attention calculation step.
Let
𝐡
ℓ
∈
ℝ
1
×
d
\mathbf{h}^{\ell}\in\mathbb{R}^{1\times d}
(
1
≤
ℓ
≤
L
)
(1\leq\ell\leq L)
denote the output hidden state at the
ℓ
\ell
-th layer of the LLM, where
L
L
is the number of LLM layers and
d
d
is the hidden dimension. With
𝐖
r
ℓ
\mathbf{W}_{r}^{\ell}
as the trainable router weight at layer
ℓ
\ell
, the top-k gate router
R
~
​
(
⋅
)
\tilde{R}(\cdot)
chooses
k
k
experts with highest probability given a hidden state
𝐡
ℓ
\mathbf{h}^{\ell}
:
R
~
ℓ
​
(
𝐡
ℓ
)
=
Keep-Top-k
​
(
Softmax
​
(
𝐖
r
ℓ
⋅
𝐡
ℓ
)
)
.
\tilde{R}^{\ell}(\mathbf{h}^{\ell})=\text{Keep-Top-k}(\text{Softmax}(\mathbf{W}^{\ell}_{r}\cdot\mathbf{h}^{\ell})).
(3)
Finally, we obtain the final MixLoRA prediction with:
MixLoRA
​
(
𝐡
ℓ
)
=
∑
k
=
1
K
R
~
ℓ
​
(
𝐡
ℓ
)
k
​
E
k
ℓ
​
(
𝐡
ℓ
)
,
E
k
ℓ
​
(
𝐡
ℓ
)
=
𝐖
p
​
r
​
e
ℓ
⋅
𝐡
ℓ
+
𝐁
k
ℓ
​
𝐀
k
ℓ
⋅
𝐡
ℓ
.
\text{MixLoRA}(\mathbf{h}^{\ell})=\sum_{k=1}^{K}\tilde{R}^{\ell}(\mathbf{h}^{\ell})_{k}E^{\ell}_{k}(\mathbf{h}^{\ell}),\quad E^{\ell}_{k}(\mathbf{h}^{\ell})=\mathbf{W}_{pre}^{\ell}\cdot\mathbf{h}^{\ell}+\mathbf{B}^{\ell}_{k}\mathbf{A}^{\ell}_{k}\cdot\mathbf{h}^{\ell}.
(4)
where
𝐖
p
​
r
​
e
ℓ
\mathbf{W}^{\ell}_{pre}
is the frozen pretrained weight at layer
ℓ
\ell
and
𝐁
k
ℓ
​
𝐀
k
ℓ
\mathbf{B}^{\ell}_{k}\mathbf{A}^{\ell}_{k}
is the k-th LoRA expert.
With MixLoRA defined in Equation
4
, we can apply MixLoRA layers at
q
,
k
,
v
q,k,v
encoding and FFN layers:
𝐳
ℓ
=
f
a
​
t
​
t
​
n
​
(
MixLoRA
q
,
k
,
v
​
(
LN
​
(
𝐡
ℓ
−
1
)
)
)
+
𝐡
ℓ
−
1
,
𝐡
ℓ
=
MixLoRA
​
(
LN
​
(
𝐳
ℓ
)
)
+
𝐳
ℓ
.
\mathbf{z}^{\ell}=f_{attn}(\text{MixLoRA}_{q,k,v}(\text{LN}(\mathbf{h}^{\ell-1})))+\mathbf{h}^{\ell-1},\quad\mathbf{h}^{\ell}=\text{MixLoRA}(\text{LN}(\mathbf{z}^{\ell}))+\mathbf{z}^{\ell}.
(5)
3
Methodology
The high-level goal of UQ4CT is to leverage the ensemble of prompt-dependent LoRA mixture-of-experts (MoE) to guide and calibrate the confidence of the model during fine-tuning. By quantifying the variability in how different LoRA experts are combined for each input, UQ4CT enables the model to adaptively select expert mixtures that reflect the true uncertainty in its predictions. Our approach not only encourages the model to exploit confident expert combinations for accurate predictions but also promotes exploration of alternative experts when uncertainty is high, ultimately leading to better-calibrated and more reliable model outputs.
We note that the MixLoRA MoE structure used in UQ4CT is not part of the LLM architecture itself; rather, it is a lightweight, modular fine-tuning adapter that operates entirely at the LoRA adapter level. UQ4CT only requires LoRA-compatible linear layers, which are standard in modern decoder-based LLMs. With the base model remains unchanged, it is as easy to apply as standard LoRA.
Figure 2:
MoE architecture to capture functional-level uncertainty. LoRA experts (
B
i
B_{i}
,
A
i
A_{i}
) capture diverse functional bases, while the top-
k
k
router assigns mixture weights based on the input hidden state. The calibration loss aligns functional-level uncertainty with prediction correctness, encouraging confident expert selection for correct predictions and higher uncertainty for incorrect ones.
3.1
Decomposition of the Functional Space
Given the immense size of both the pre-training dataset and the model, we posit that the pretrained network contains submodules capable of expressing a wide range of functional relationships present in the data. During fine-tuning, our focus is on the functional space spanned by the model, which can be effectively captured as a mixture of LoRA experts, each representing a distinct basis function. However, naively decomposing the full functional space by considering all possible combinations of these experts quickly leads to a combinatorial explosion.
Naive Decomposition.
Denote the input prompt as
𝐱
\mathbf{x}
and the functional map from input to output as
f
f
. A straightforward approach is to express the function as a sum over all possible compositions of
K
K
submodules per layer, across
L
L
layers:
f
(
𝐱
)
=
∑
k
1
,
⋯
,
k
L
=
1
K
α
k
1
,
…
,
k
L
g
k
L
L
(
⋯
(
g
k
l
l
(
…
g
k
1
1
(
𝐱
)
)
)
)
,
f(\mathbf{x})=\sum_{k^{1},\cdots,k^{L}=1}^{K}\alpha_{k^{1},\dots,k^{L}}g_{k^{L}}^{L}\bigg(\cdots\bigg(g_{k^{l}}^{l}\big(\dots g_{k^{1}}^{1}(\mathbf{x})\big)\bigg)\bigg),
(6)
where each
g
k
ℓ
ℓ
g_{k^{\ell}}^{\ell}
denotes a particular variant (e.g., LoRA-adapted) of the
ℓ
\ell
-th block and
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
=
𝐡
ℓ
+
E
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
ℓ
)
)
,
\displaystyle g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})=\mathbf{h}^{\ell}+E_{k^{\ell}}^{\ell}\big(f_{trans}^{\ell}(\mathbf{h}^{\ell})\big),
(7)
here
f
t
​
r
​
a
​
n
​
s
ℓ
f_{trans}^{\ell}
represents the necessary non-fine-tuned operations within a transformer block (i.e. layer norm, attention calculation, etc.) and as defined in Eq.
4
,
E
k
ℓ
ℓ
E_{k^{\ell}}^{\ell}
denotes the parameterized adaptation associated with the
k
ℓ
k^{\ell}
-th expert in the
ℓ
\ell
-th layer.
However, this naive decomposition is intractable in practice, as it requires keeping track of
K
L
K^{L}
mixture weights
α
k
1
,
…
,
k
L
\alpha_{k^{1},\ldots,k^{L}}
. This is an exponential growth in the number of parameters with respect to both the number of layers
L
L
and the number of submodules per layer
K
K
, which makes the direct approach computationally infeasible for realistic network sizes.
Hierarchical Decomposition.
To address the combinatorial explosion of mixture weights, we instead propose a hierarchical decomposition. Here, the mixture at each layer is formed independently, and the output of each layer is a weighted sum over its submodules, with the weights themselves being layer-specific:
f
(
𝐱
)
=
∑
k
L
=
1
K
α
k
L
L
g
k
L
L
(
⋯
(
∑
k
l
=
1
K
α
k
l
l
g
k
l
l
(
…
∑
k
1
=
1
K
α
k
1
1
g
k
1
1
(
𝐱
)
)
)
)
.
f(\mathbf{x})=\sum_{k^{L}=1}^{K}\alpha^{L}_{k^{L}}g_{k^{L}}^{L}\bigg(\cdots\Bigg(\sum_{k^{l}=1}^{K}\alpha^{l}_{k^{l}}g_{k^{l}}^{l}\bigg(\dots\sum_{k^{1}=1}^{K}\alpha^{1}_{k^{1}}g_{k^{1}}^{1}(\mathbf{x})\bigg)\Bigg)\Bigg).
(8)
Instead of needing
K
L
K^{L}
mixture weights, this hierarchical structure only requires
K
⋅
L
K\cdot L
weights
α
k
ℓ
ℓ
\alpha^{\ell}_{k^{\ell}}
, one for each submodule in each layer. This dramatically reduces the parameters required and makes the decomposition tractable, while still enabling a rich set of compositional functions.
Dynamic, Input-Dependent Routing.
To further enhance expressivity and efficiency, we allow the mixture weights to depend dynamically on the input at each layer. Specifically, we set the mixture weights to be a sparse routing function
R
ℓ
R^{\ell}
of the hidden state
𝐡
ℓ
\mathbf{h}^{\ell}
at each layer, where
α
k
ℓ
ℓ
=
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
=
R
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
ℓ
)
)
.
\alpha_{k^{\ell}}^{\ell}=\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})=R_{k^{\ell}}^{\ell}(f_{trans}^{\ell}(\mathbf{h}^{\ell})).
Substituting this definition into the hierarchical mixture, the overall function
f
⁡
(
𝐱
)
f(\mathbf{x})
becomes:
f
⁡
(
𝐱
)
=
∑
k
L
=
1
K
R
k
L
L
​
(
f
t
​
r
​
a
​
n
​
s
L
​
(
𝐡
L
)
)
​
g
k
L
L
​
(
…
​
(
∑
k
1
=
1
K
R
k
1
1
​
(
f
t
​
r
​
a
​
n
​
s
1
​
(
𝐡
1
)
)
​
g
k
1
1
​
(
𝐱
)
)
)
.
f(\mathbf{x})=\sum_{k^{L}=1}^{K}R_{k^{L}}^{L}(f_{trans}^{L}(\mathbf{h}^{L}))g_{k^{L}}^{L}\Bigg(\dots\Bigg(\sum_{k^{1}=1}^{K}R_{k^{1}}^{1}(f_{trans}^{1}(\mathbf{h}^{1}))g_{k^{1}}^{1}(\mathbf{x})\Bigg)\Bigg).
(9)
This recursive formulation shows that at each layer, the submodules are weighted according to the input-dependent routing function, which adapts based on the current hidden state.
For a layer-wise perspective, the computation at each layer
ℓ
\ell
can be explicitly written as:
𝐡
ℓ
+
1
=
∑
k
ℓ
=
1
K
R
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
ℓ
)
)
​
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
.
\displaystyle\mathbf{h}^{\ell+1}=\sum_{k^{\ell}=1}^{K}R_{k^{\ell}}^{\ell}(f_{trans}^{\ell}(\mathbf{h}^{\ell}))g^{\ell}_{k^{\ell}}(\mathbf{h}^{\ell}).
(10)
Here,
R
ℓ
R^{\ell}
selects the most relevant submodules for a given input, allowing the network to adaptively compose its computation path at each layer in a sparse fashion.
3.2
Quantifying FLC with MixLoRA
In the previous section, we have established a parsimonious representation of the functional space.
In this section, we choose a simple function to encode the functional level uncertainty and provide the intuition as follows. We first note that given a fixed MoE model architecture, the larger weight a mixture component has, the more certain we are about that component.
The model uncertainty of the MixLoRA architecture is quantified by considering perturbations
Δ
​
f
​
(
𝐱
)
\Delta f(\mathbf{x})
to the model
f
⁡
(
𝐱
)
f(\mathbf{x})
. Following the discussion and notation in Sec.
3.1
, we can show that these perturbations are instantiated in the space of the mixture weights
α
\alpha
(as defined in Eq.
8
and
9
):
Fact 3.1
(Model Perturbation Structure)
.
Under regularity assumptions on the residual connection architecture, perturbations
Δ
​
f
​
(
x
)
\Delta f(x)
to the model
f
⁡
(
x
)
f(x)
approximately decompose as:
Δ
​
f
​
(
x
)
≈
∑
ℓ
=
1
L
∑
k
ℓ
=
1
K
Δ
​
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
⋅
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
.
\Delta f(x)\approx\sum_{\ell=1}^{L}\sum_{k^{\ell}=1}^{K}\Delta\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell}).
In high-dimensional settings, the basis functions are approximately orthogonal. Thus, the perturbation
Δ
​
f
​
(
x
)
\Delta f(x)
is entirely represented by the set
{
Δ
​
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
}
k
ℓ
=
1
,
…
,
K
ℓ
=
1
,
…
,
L
\left\{\Delta\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\right\}_{k^{\ell}=1,\dots,K}^{\ell=1,\dots,L}
.
Therefore, the functional-level confidence (FLC) can be generally modeled as a linear function over the mixture weights:
FLC
​
(
x
)
=
U
⁡
(
{
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
}
k
ℓ
=
1
,
…
,
K
ℓ
=
1
,
…
,
L
)
,
\text{FLC}(x)=U\left(\left\{\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\right\}_{k^{\ell}=1,\dots,K}^{\ell=1,\dots,L}\right),
where
U
⁡
(
⋅
)
U(\cdot)
denotes a linear aggregation function. Details of derivation is presented in Appendix
A.1
.
In practice, as illustrated in Figure
2
, the top-
k
k
router at each layer produces a sparse routing distribution that dynamically mixes the basis functions represented by the LoRA experts conditioned on the current hidden state. The retained top-
K
K
routing weights directly reflect the concentration of expert selection and therefore provide a functional-level confidence signal. Following the MoE routing mechanism in Eq. (
3
) and Eq. (
4
), we use a top-
2
2
router. For each layer
ℓ
\ell
, we compute the router probabilities and retain the two largest entries:
R
~
ℓ
​
(
𝐡
ℓ
)
=
KeepTop2
⁡
(
Softmax
⁡
(
𝐖
r
ℓ
​
𝐡
ℓ
)
)
,
FLC
⁡
(
x
)
=
1
L
​
∑
ℓ
=
1
L
∑
i
=
1
2
R
~
i
ℓ
​
(
𝐡
ℓ
)
.
\tilde{R}^{\ell}(\mathbf{h}^{\ell})=\mathrm{KeepTop2}\!\left(\mathrm{Softmax}(\mathbf{W}_{r}^{\ell}\mathbf{h}^{\ell})\right),\quad\mathrm{FLC}(x)=\frac{1}{L}\sum_{\ell=1}^{L}\sum_{i=1}^{2}\tilde{R}_{i}^{\ell}(\mathbf{h}^{\ell}).
(11)
Given an input prompt
x
x
, we aggregate the retained routing weights over the selected experts and across all
L
L
layers to estimate the functional-level confidence (FLC) for the predicted next token, where
i
i
indexes the two experts selected by the top-
2
2
router at layer
ℓ
\ell
.
3.3
Calibration Loss
The FLC model provides a principled way to calibrate the mixture parameters against predictive accuracy, enabling better alignment between output distributions and true model confidence. Specifically, for MoE top-
k
k
routers, we design the following calibration loss for training:
ℒ
cal
=
(
𝟙
{
MixLoRA
(
x
)
=
y
∗
}
−
FLC
(
x
)
)
2
.
\mathcal{L}_{\mathrm{cal}}=\left(\mathbbm{1}{\{\text{MixLoRA}(x)=y^{*}\}}-\text{FLC}(x)\right)^{2}.
(12)
The first term is an indicator function that equals
1
1
if the model prediction matches the ground truth
y
∗
y^{*}
for prompt
x
x
, and
0
0
otherwise, corresponding to a one-hot definition of ground truth confidence.
This calibration loss encourages functional-level confidence (FLC) to reflect predictive correctness. As shown in Figure
2
, correct predictions push FLC toward
1
1
, while incorrect predictions push toward
0
0
. Optimized over the data distribution, this objective aligns FLC with the probability of prediction correctness.
We formally state this property as follows and present the proof in Appendix
A.1
:
Proposition 3.2
(Truthfulness of Calibration Loss)
.
Let the calibration risk be defined as the expectation of the calibration loss over the data distribution:
ℒ
¯
cal
=
𝔼
(
x
,
y
∗
)
∼
𝒟
(
𝟙
{
MixLoRA
(
x
)
=
y
∗
}
−
FLC
(
x
)
)
2
.
\bar{\mathcal{L}}_{\mathrm{cal}}=\mathbb{E}_{(x,y^{*})\sim\mathcal{D}}\left(\mathbbm{1}\{\mathrm{MixLoRA}(x)=y^{*}\}-\mathrm{FLC}(x)\right)^{2}.
If this calibration risk is optimized over the data distribution
𝒟
\mathcal{D}
, then the optimal solution is
FLC
⁡
(
x
)
=
ℙ
⁡
(
MixLoRA
⁡
(
x
)
=
y
∗
​
(
x
)
)
\mathrm{FLC}(x)=\mathbb{P}(\mathrm{MixLoRA}(x)=y^{*}(x))
; that is, the optimally trained FLC corresponds to the probability that the model’s prediction is correct.
3.4
Fine-tuning with the Total Loss
Our proposed calibration loss
ℒ
cal
\mathcal{L}_{\mathrm{cal}}
improves predictive reliability by adaptively balancing expert exploitation and exploration according to functional-level uncertainty. As shown in Figure
2
,
ℒ
cal
\mathcal{L}_{\mathrm{cal}}
aligns uncertainty with predictive correctness, increasing the router probability of the selected expert for correct predictions (exploitation) and decreasing it for incorrect ones (exploration).
Ideally, when the
K
K
LoRA experts collectively capture the relevant functional relationships in the data during fine-tuning via cross-entropy loss,
ℒ
cal
\mathcal{L}_{\mathrm{cal}}
further guides the model to select appropriate mixtures of LoRA experts conditioned on the input
𝐱
\mathbf{x}
. This targeted selection enables the model to match the data distribution more closely and provides more calibrated uncertainty estimates.
To ensure balanced expert utilization, we incorporate a load balancing loss
ℒ
b
\mathcal{L}_{b}
as proposed by
Li et al. (2024)
. Our overall loss function is:
ℒ
=
𝐂𝐄
+
γ
⋅
ℒ
b
+
β
⋅
ℒ
cal
,
\mathcal{L}=\mathbf{CE}+\gamma\cdot\mathcal{L}_{b}+\beta\cdot\mathcal{L}_{\mathrm{cal}},
(13)
where
𝐂𝐄
\mathbf{CE}
is the cross-entropy loss, and
γ
\gamma
,
β
\beta
are hyperparameters for the auxiliary terms. We fix
γ
\gamma
,
β
\beta
to
1
1
for our experiments. Details of
ℒ
b
\mathcal{L}_{b}
are provided in Appendix
A.2
.
4
Related Work
Table 1:
Performance comparison of different methods fine-tuned with Llama3.1-8B across three common sense reasoning tasks and a domain-specific task. UQ4CT shows substantial ECE improvements while maintaining high accuracy.
Metrics
Methods
ARC-E
ARC-C
OBQA
ClimateQA
ACC
↑
\uparrow
Base Model
87.27
87.27
74.32
74.32
72.80
72.80
68.64
68.64
LoRA
88.82
1.82
¯
\underline{88.82_{1.82}}
78.21
0.73
78.21_{0.73}
88.00
1.22
88.00_{1.22}
78.25
1.29
78.25_{1.29}
MC Drop
88.16
1.75
88.16_{1.75}
77.14
0.69
77.14_{0.69}
87.12
1.18
87.12_{1.18}
78.19
1.35
78.19_{1.35}
Ensemble
89.14
1.31
\mathbf{89.14_{1.31}}
78.81
0.96
78.81_{0.96}
86.47
0.42
86.47_{0.42}
78.53
2.98
78.53_{2.98}
MixLoRA
87.74
0.36
87.74_{0.36}
78.56
1.87
78.56_{1.87}
88.27
0.50
¯
\underline{88.27_{0.50}}
79.94
1.29
¯
\underline{79.94_{1.29}}
LA
86.22
3.52
86.22_{3.52}
78.00
3.76
78.00_{3.76}
86.00
6.01
86.00_{6.01}
79.82
3.48
79.82_{3.48}
BLoB(Mean)
88.71
0.82
88.71_{0.82}
79.37
0.71
79.37_{0.71}
87.60
1.04
87.60_{1.04}
79.02
0.50
79.02_{0.50}
BLoB(N=10)
87.96
0.62
87.96_{0.62}
80.08
1.55
\mathbf{80.08_{1.55}}
87.13
0.88
87.13_{0.88}
79.02
0.50
79.02_{0.50}
UQ4CT
88.66
0.20
88.66_{0.20}
79.60
1.21
¯
\underline{79.60_{1.21}}
88.40
0.35
\mathbf{88.40_{0.35}}
79.97
0.85
\mathbf{79.97_{0.85}}
ECE
↓
\downarrow
Base Model
13.76
13.76
11.30
11.30
11.39
11.39
14.58
14.58
LoRA
6.55
1.70
6.55_{1.70}
14.07
0.68
14.07_{0.68}
7.30
0.43
7.30_{0.43}
13.70
1.50
13.70_{1.50}
MC Drop
6.48
1.74
6.48_{1.74}
14.12
0.71
14.12_{0.71}
7.24
0.39
7.24_{0.39}
13.11
1.46
13.11_{1.46}
Ensemble
7.08
0.73
7.08_{0.73}
13.71
1.29
13.71_{1.29}
8.63
0.38
8.63_{0.38}
14.69
0.84
14.69_{0.84}
MixLoRA
7.79
0.45
7.79_{0.45}
13.71
1.90
13.71_{1.90}
6.58
0.21
6.58_{0.21}
14.68
0.09
14.68_{0.09}
LA
7.63
1.71
7.63_{1.71}
8.92
4.16
8.92_{4.16}
11.97
5.97
11.97_{5.97}
11.48
1.66
11.48_{1.66}
BLoB(Mean)
4.89
0.32
4.89_{0.32}
11.26
1.13
11.26_{1.13}
6.83
0.90
6.83_{0.90}
12.74
0.88
12.74_{0.88}
BLoB(N=10)
3.35
0.50
\mathbf{3.35_{0.50}}
6.81
1.43
¯
\underline{6.81_{1.43}}
3.84
1.00
¯
\underline{3.84_{1.00}}
11.96
2.57
¯
\underline{11.96_{2.57}}
UQ4CT
3.97
0.78
¯
\underline{3.97_{0.78}}
4.43
0.82
\mathbf{4.43_{0.82}}
3.34
1.60
\mathbf{3.34_{1.60}}
9.36
2.77
\mathbf{9.36_{2.77}}
Mixture of LoRA Experts.
LLMs have achieved impressive performance across diverse NLP tasks
(
Brown et al., 2020
;
Hoffmann et al., 2022
;
Touvron et al., 2023b
;
Touvron et al., 2023d
)
, with instruction fine-tuning
(
Chung et al., 2022
;
Iyer et al., 2022
;
Zheng et al., 2024
)
further boosting their adaptability for conversational AI
(
Wu et al., 2023b
;
Achiam et al., 2023
)
. However, scaling LLMs increases the resource demands of full fine-tuning. Parameter-efficient fine-tuning (PEFT) methods
(
Mangrulkar et al., 2022
)
such as LoRA
(
Hu et al., 2021b
)
and its variants
(
Kopiczko et al., 2023
;
Hyeon-Woo et al., 2021
;
Renduchintala et al., 2023
;
Zhang et al., 2023
;
Liu et al., 2024
)
reduce adaptation costs by updating a subset of parameters.
Recent advances combine PEFT with the Mixture-of-Experts (MoE) framework
(
Jacobs et al., 1991
;
Wang et al., 2020
)
, which sparsely activates expert subnetworks for greater model capacity and specialization. MoE-based LLMs leverage expert routing and parameter-efficient adaptations to target new domains or tasks efficiently. Notably, methods such as MoRAL
(
Yang et al., 2024b
)
, LoRAMoE
(
Dou et al., 2024
)
, PESC
(
Wu et al., 2024a
)
, MoE-LoRA
(
Luo et al., 2024
)
, and MixLoRA
(
Li et al., 2024
)
optimize domain-specific routing, mitigate forgetting, and enable scalable, high-throughput training and inference with mixtures of LoRA experts.
Uncertainty Quantification in LLMs.
Established uncertainty quantification methods have been studied in conjunction with the LoRA structure for LLMs. Monte-Carlo dropout
(
Gal and Ghahramani, 2016
)
interprets dropout in neural networks as approximate Bayesian inference in deep Gaussian processes, allowing uncertainty estimates to be obtained from existing LoRA adapters without modifying them. Checkpoint ensemble
(
Chen et al., 2017
)
utilizes predictions from multiple LoRA checkpoints saved during a single fine-tuning process to calibrate uncertainty. Deep ensemble
(
Lakshminarayanan et al., 2017
;
Wang et al., 2023
;
Zhai et al., 2023
)
combines the predictions from multiple LoRA adapters for better uncertainty calibration. Laplace-LoRA
(
Yang et al., 2024a
)
applies Bayesian inference via Laplace approximation to the LoRA parameters after fine-tuning, resulting in improved calibration and uncertainty estimates. Bayesian Low-Rank Adaptation by Backpropagation (BLoB)
(
Wang et al., 2024
)
extends the LA method by jointly optimizing the mean and covariance of LoRA parameters via backpropagation throughout fine-tuning.
Prompt-perturbation and resampling-based approaches have also been explored for UQ in LLMs. These methods estimate uncertainty by measuring prediction variability under different prompt formulations or sampled input variants, without altering model parameters
(
Farquhar et al., 2024
;
Hou et al., 2023
;
Gao et al., 2024
)
. This line of work leverages the inherent sensitivity of LLMs to input perturbations as a means to assess model confidence, providing a complementary perspective to parameter-based methods.
5
Experiments
Datasets.
We evaluate on four multiple-choice QA benchmarks: OpenBookQA (OBQA)
(
Mihaylov et al., 2018
)
, ARC-Easy (ARC-E), ARC-Challenge (ARC-C)
(
Clark et al., 2018
)
, and ClimateQA, a domain-specific climate science benchmark. To assess generalization to open-ended generation, we further evaluate on TruthfulQA
(
Lin et al., 2021
)
and TriviaQA
(
Joshi et al., 2017
)
. For robustness under distribution shift, we group domain-specific MMLU subtasks
(
Hendrycks et al., 2020
)
into four professional-domain benchmarks: Computer Science (CS), Engineering (Eng), Law, and Health, with details provided in Appendix
A.9
. Models are fine-tuned on the public training split and evaluated on the corresponding test split for each benchmark.
Table 2:
Performance comparison of different methods fine-tuned on the OBQA dataset with Llama3.1-8B across two smaller distribution shift (DS) tasks and four larger distribution shift tasks. UQ4CT shows substantial ECE improvements while maintaining high accuracy.
ID
Smaller DS
Larger DS
Metrics
Methods
OBQA
ARC-C
ARC-E
CS
Eng
Law
Health
ACC
↑
\uparrow
LoRA
88.0
1.22
88.0_{1.22}
77.8
0.16
77.8_{0.16}
86.7
0.77
86.7_{0.77}
55.8
0.52
\mathbf{55.8_{0.52}}
54.3
3.30
54.3_{3.30}
44.9
0.23
44.9_{0.23}
58.8
0.21
58.8_{0.21}
MC Drop
87.1
1.18
87.1_{1.18}
77.1
2.01
77.1_{2.01}
86.9
2.42
86.9_{2.42}
54.4
1.58
54.4_{1.58}
54.1
1.82
54.1_{1.82}
45.0
0.76
45.0_{0.76}
58.3
1.46
58.3_{1.46}
Ensemble
86.5
0.42
86.5_{0.42}
78.2
0.90
78.2_{0.90}
85.4
0.47
85.4_{0.47}
53.8
1.02
53.8_{1.02}
52.4
0.56
52.4_{0.56}
45.0
0.20
45.0_{0.20}
60.6
0.57
60.6_{0.57}
MixLoRA
88.3
0.50
¯
\underline{88.3_{0.50}}
78.1
0.45
78.1_{0.45}
86.7
0.35
86.7_{0.35}
53.1
1.14
53.1_{1.14}
54.7
2.28
¯
\underline{54.7_{2.28}}
45.0
1.46
45.0_{1.46}
60.9
1.04
¯
\underline{60.9_{1.04}}
LA
86.0
6.01
86.0_{6.01}
78.7
0.55
78.7_{0.55}
86.4
0.76
86.4_{0.76}
54.7
1.82
¯
\underline{54.7_{1.82}}
53.6
2.77
53.6_{2.77}
44.9
1.03
44.9_{1.03}
59.7
0.94
59.7_{0.94}
BLoB(Mean)
87.6
1.04
87.6_{1.04}
79.5
1.10
¯
\underline{79.5_{1.10}}
86.6
0.65
86.6_{0.65}
51.2
0.99
51.2_{0.99}
48.6
1.44
48.6_{1.44}
39.9
7.85
39.9_{7.85}
57.0
3.51
57.0_{3.51}
BLoB(N=10)
87.1
0.88
87.1_{0.88}
79.8
1.06
\mathbf{79.8_{1.06}}
87.2
0.79
¯
\underline{87.2_{0.79}}
52.8
1.28
52.8_{1.28}
51.9
3.13
51.9_{3.13}
43.8
4.60
43.8_{4.60}
58.5
5.33
58.5_{5.33}
UQ4CT
88.4
0.35
\mathbf{88.4_{0.35}}
79.0
0.56
79.0_{0.56}
87.8
0.47
\mathbf{87.8_{0.47}}
53.3
0.61
53.3_{0.61}
61.1
3.20
\mathbf{61.1_{3.20}}
45.4
0.50
\mathbf{45.4_{0.50}}
61.1
1.48
\mathbf{61.1_{1.48}}
ECE
↓
\downarrow
LoRA
7.30
0.43
7.30_{0.43}
14.8
0.62
14.8_{0.62}
9.6
0.69
9.6_{0.69}
21.0
3.05
21.0_{3.05}
24.1
3.63
24.1_{3.63}
29.3
1.98
29.3_{1.98}
24.0
1.81
24.0_{1.81}
MC Drop
7.24
0.39
7.24_{0.39}
13.4
2.15
13.4_{2.15}
10.2
1.89
10.2_{1.89}
20.8
3.26
20.8_{3.26}
24.1
0.77
24.1_{0.77}
29.1
0.64
29.1_{0.64}
21.6
3.92
21.6_{3.92}
Ensemble
8.63
0.38
8.63_{0.38}
15.4
0.46
15.4_{0.46}
10.7
0.56
10.7_{0.56}
14.0
3.18
14.0_{3.18}
17.4
1.98
17.4_{1.98}
19.9
2.95
19.9_{2.95}
16.1
2.07
16.1_{2.07}
MixLoRA
6.58
0.21
6.58_{0.21}
14.5
0.55
14.5_{0.55}
9.9
0.20
9.9_{0.20}
17.1
3.06
17.1_{3.06}
17.8
2.80
17.8_{2.80}
21.6
4.07
21.6_{4.07}
18.0
2.78
18.0_{2.78}
LA
11.97
5.97
11.97_{5.97}
7.2
0.5
7.2_{0.5}
6.4
0.42
6.4_{0.42}
13.7
2.14
13.7_{2.14}
15.5
2.0
15.5_{2.0}
19.0
0.54
¯
\underline{19.0_{0.54}}
15.7
2.30
15.7_{2.30}
BLoB(Mean)
6.83
0.90
6.83_{0.90}
11.37
1.94
11.37_{1.94}
6.6
1.65
6.6_{1.65}
17.2
2.72
17.2_{2.72}
18.5
2.82
18.5_{2.82}
22.6
1.26
22.6_{1.26}
16.9
3.02
16.9_{3.02}
BLoB(N=10)
3.84
1.00
¯
\underline{3.84_{1.00}}
5.8
0.96
¯
\underline{5.8_{0.96}}
3.0
0.87
\mathbf{3.0_{0.87}}
11.5
2.76
¯
\underline{11.5_{2.76}}
14.9
1.93
¯
\underline{14.9_{1.93}}
19.7
3.21
19.7_{3.21}
14.5
3.38
¯
\underline{14.5_{3.38}}
UQ4CT
3.34
1.60
\mathbf{3.34_{1.60}}
3.6
1.44
\mathbf{3.6_{1.44}}
3.6
1.32
¯
\underline{3.6_{1.32}}
10.8
3.73
\mathbf{10.8_{3.73}}
13.2
1.86
\mathbf{13.2_{1.86}}
18.1
4.40
\mathbf{18.1_{4.40}}
13.2
4.06
\mathbf{13.2_{4.06}}
Experiment Setup.
We implement UQ4CT with PyTorch
(
Paszke et al., 2019
)
, extending the MixLoRA repository in
(
Li et al., 2024
)
. We use the Llama-3.1-8B
(
Grattafiori et al., 2024
)
as our base model. In particular, we apply MixLoRA to query, key, value and output layers, together with the feed-forward networks in LLaMA-3.1-8B (gate layer, down layer and up layer). Details are provided in Appendix
A.7
.
Baselines.
We compare UQ4CT with state-of-the-art uncertainty estimation methods along with naive fine-tuning applied to the LoRA adapters of LLMs, including
LoRA
(
Hu et al., 2021a
)
,
Monte Carlo (MC) Dropout
(
Gal and Ghahramani, 2016
)
,
Deep Ensemble
(
Lakshminarayanan et al., 2017
)
,
Laplace-LoRA (LA)
(
Yang et al., 2024a
)
,
Bayesian Low-Rank Adaptation by Backpropagation (BLoB)
(
Wang et al., 2024
)
and
MixLoRA
(
Li et al., 2024
)
. Note that for
BLoB(N=10)
, the method performs
10
10
forward passes with differently sampled LoRA parameters for each question, which is an unfair computational budget advantage compared against UQ4CT with only
1
1
forward pass.
Evaluation.
We evaluate prediction accuracy on the validation set across all four tasks. For uncertainty calibration, we use the expected calibration error (ECE;
Guo et al. (2017)
; more details in
A.8
) to measure the alignment between predicted probabilities and actual outcomes.
To assess robustness under distribution shifts, we fine-tune models on the OBQA dataset and evaluate them following
Yang et al. (2024a)
. We use ARC-C and ARC-E to represent smaller distribution shifts, as these datasets focus on general science reasoning similar to OBQA but are more challenging and diverse. For larger shifts, we utilize the four aforementioned domain-specific MMLU subtasks, which span a wide range of expertise from elementary to professional levels. This domain represents a greater distribution shift from the general common sense focus of OBQA.
The in-distribution setting evaluates alignment with the target task, while the distribution-shift setting assesses generalization to novel domains. Together, they provide a practical evaluation of both task-specific performance and robustness to out-of-distribution inputs.
5.1
In-distribution Performance
As shown in Table
1
, UQ4CT achieves notable gains in uncertainty calibration across diverse tasks while maintaining competitive accuracy relative to baseline approaches. The accuracy remains on par with or above the best baselines, demonstrating that improved uncertainty quantification does not come at the expense of predictive performance.
The primary gains are in calibration. UQ4CT consistently achieves the lowest ECE across benchmarks, with especially large improvements on challenging tasks where baselines remain poorly calibrated. Notably, UQ4CT requires only a single forward pass, whereas BLoB (
N
=
10
N=10
) uses ten forward passes yet still yields higher ECE on most benchmarks.
To further validate our method, we include results from fine-tuning both LLaMA-3.1-8B (main text) and Mistral-7B (Appendix
A.3
). Across both models, UQ4CT delivers substantial and consistent improvements in uncertainty calibration. A key advantage of UQ4CT is that it incorporates uncertainty calibration directly during fine-tuning, incurring minimal computational overhead compared to other UQ methods that require costly repetitive sampling or post-hoc adjustments.
5.2
Performance Under Distribution Shift
Due to the sparse nature of the fine-tuning data, real world deployment of LLMs often requires the model to be robust to out-of-distribution knowledge
(
Ouyang et al., 2022
;
Touvron et al., 2023a
;
Touvron et al., 2023c
)
. Therefore, we evaluate the performance of UQ4CT along with other baseline models fine-tuned on the OBQA dataset under smaller and larger distribution shift scenarios.
Table
2
presents the distribution shift evaluations. UQ4CT achieves substantial ECE improvements while maintaining high accuracy across smaller and larger distribution shifts. For smaller shifts, UQ4CT’s ECE remains comparable to the in-distribution scenario. Under larger shifts, UQ4CT attains the lowest ECE among baselines and delivers competitive accuracy on all domain-specific tasks. These results demonstrate that aligning uncertainty at the functional level with predictive correctness improves generalizability and mitigates overconfidence in fine-tuned models.
5.3
Ablation Studies
We conduct ablation studies to assess the contribution of the calibration loss,
ℒ
c
​
a
​
l
\mathcal{L}_{cal}
. We analyze sensitivity to
β
\beta
in Equation
13
(Appendix
A.4
), showing that small values already yield substantial ECE gains and that
β
=
1
\beta=1
provides the best trade-off. We further examine the number of active LoRA experts (Appendix
A.5
), incremental calibration weighting (Appendix
A.6
), and comparisons with prompt-perturbation methods (Appendix
A.10
). Finally, we provide a detailed peak memory analysis comparing LoRA, UQ4CT, and BLoB in Appendix
A.11
, showing that UQ4CT and BLoB have nearly identical peak memory (
∼
{\sim}
21.35 GB), both only
∼
{\sim}
7.5% above standard LoRA.
Open-Ended Generative Extension.
To explore the potential of UQ4CT extending beyond multiple-choice tasks, we evaluate on TruthfulQA and TriviaQA using an F1-based correctness proxy for calibration. For controlled comparison, we first fine-tune the base model with MixLoRA and then apply all baselines to the same fine-tuned backbone. Setup details, including the adapted calibration loss and baselines, are provided in Appendix
A.12
.
Table 3:
All UQ methods applied to the
same MixLoRA-fine-tuned
Llama-3.1-8B-Instruct on open-ended generative benchmarks. Sampling-based methods (marked with *) use
N
=
5
N=5
samples. SE: Semantic Entropy, SD: Semantic Density, VC: Verbalized Consistency.
Task
Metrics
SE*
SD*
SeqProb
Verb.
VC*
UQ4CT
TruthfulQA
ACC
↑
\uparrow
86.66
0.58
86.66_{0.58}
86.66
0.58
86.66_{0.58}
84.19
0.72
84.19_{0.72}
85.63
0.41
85.63_{0.41}
87.49
0.39
87.49_{0.39}
94.60
0.32
\mathbf{94.60}_{0.32}
ECE
↓
\downarrow
18.19
1.22
18.19_{1.22}
16.65
1.31
16.65_{1.31}
9.93
1.38
9.93_{1.38}
13.00
1.35
13.00_{1.35}
11.35
1.24
11.35_{1.24}
6.08
1.72
\mathbf{6.08}_{1.72}
TriviaQA
ACC
↑
\uparrow
71.82
0.63
71.82_{0.63}
71.82
0.63
71.82_{0.63}
71.61
0.78
71.61_{0.78}
72.05
0.36
72.05_{0.36}
72.08
0.36
72.08_{0.36}
72.40
0.93
\mathbf{72.40}_{0.93}
ECE
↓
\downarrow
8.56
1.17
8.56_{1.17}
13.10
1.38
13.10_{1.38}
19.23
1.45
19.23_{1.45}
20.54
1.28
20.54_{1.28}
11.01
1.30
11.01_{1.30}
6.63
1.50
\mathbf{6.63}_{1.50}
As shown in Table
3
, UQ4CT achieves the lowest ECE on both benchmarks while maintaining the highest accuracy with only a single forward pass. The gains are particularly pronounced on TruthfulQA, where baselines show substantially higher ECE, indicating that our calibration loss improves MoE routing toward more accurate expert selection in generative settings.
6
Discussion & Conclusion
In this work, we propose Functional-Level Uncertainty Quantification for Calibrated Fine-Tuning (UQ4CT), a framework for mitigating overconfidence in fine-tuned large language models. UQ4CT quantifies uncertainty from a functional perspective and incorporates it into a mixture-of-experts fine-tuning objective. The resulting calibration-aware loss substantially improves uncertainty calibration while preserving predictive accuracy. Across common-sense reasoning, domain-specific QA, and open-ended generation tasks, UQ4CT reduces Expected Calibration Error by more than 25% without compromising accuracy under both in-distribution and out-of-distribution settings.
UQ4CT’s calibration loss requires a correctness signal during training. For multiple-choice tasks, exact-match provides this naturally. Our exploratory experiments on open-ended generative QA (Sec.
5.3
) demonstrate that a simple token-level F1 threshold serves as a promising correctness proxy, suggesting that the functional-space perspective on calibration extends beyond classification-style tasks. However, this work primarily establishes the foundations of functional-level uncertainty quantification for calibrated fine-tuning; scaling to long-form reasoning or multi-step generation remains an important direction for future work. Potential avenues include leveraging reward models or learned evaluation functions as soft correctness proxies to broaden applicability.
Acknowledgement
This work was supported in part by U. S. Army Research Office
under Army-ECASE award W911NF-07-R-0003-03, the U.S. Department Of Energy, Office of Science, IARPA HAYSTAC Program, and NSF Grants #2205093, #2146343, #2134274, CDC-RFA-FT-23-0069, DARPA AIE FoundSci and DARPA YFA.
References
Achiam
et al.
(2023)
J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat,
et al.
Gpt-4 technical report
.
arXiv preprint arXiv: 2303.08774
.
Cited by:
§4
.
Alur
et al.
(2024)
R. Alur, M. Raghavan, and D. Shah
Human expertise in algorithmic prediction
.
Advances in Neural Information Processing Systems
37
,
pp. 138088–138129
.
Cited by:
§A.12
.
Brown
et al.
(2020)
T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell,
et al.
Language models are few-shot learners
.
Advances in neural information processing systems
33
,
pp. 1877–1901
.
Cited by:
§4
.
Chang
et al.
(2024)
Y. Chang, X. Wang, J. Wang, Y. Wu, L. Yang, K. Zhu, H. Chen, X. Yi, C. Wang, Y. Wang,
et al.
A survey on evaluation of large language models
.
ACM Transactions on Intelligent Systems and Technology
15
(
3
),
pp. 1–45
.
Cited by:
§1
.
Chen
et al.
(2017)
H. Chen, S. Lundberg, and S. Lee
Checkpoint ensembles: ensemble methods from a single training process
.
arXiv preprint arXiv:1710.03282
.
Cited by:
§1
,
§4
.
Chung
et al.
(2022)
H. W. Chung, L. Hou, S. Longpre, B. Zoph, Y. Tay, W. Fedus, E. Li, X. Wang, M. Dehghani, S. Brahma, A. Webson, S. S. Gu, Z. Dai, M. Suzgun, X. Chen, A. Chowdhery, D. Valter, S. Narang, G. Mishra, A. W. Yu, V. Zhao, Y. Huang, A. M. Dai, H. Yu, S. Petrov, E. H. Chi, J. Dean, J. Devlin, A. Roberts, D. Zhou, Q. V. Le, and J. Wei
Scaling instruction-finetuned language models
.
ArXiv
abs/2210.11416
.
External Links:
Link
Cited by:
§4
.
Clark
et al.
(2018)
P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord
Think you have solved question answering? try arc, the ai2 reasoning challenge
.
arXiv preprint arXiv:1803.05457
.
Cited by:
§5
.
Dou
et al.
(2024)
S. Dou, E. Zhou, Y. Liu, S. Gao, J. Zhao, W. Shen, Y. Zhou, Z. Xi, X. Wang, X. Fan, S. Pu, J. Zhu, R. Zheng, T. Gui, Q. Zhang, and X. Huang
LoRAMoE: alleviate world knowledge forgetting in large language models via moe-style plugin
.
arXiv
.
Cited by:
§4
.
Farquhar
et al.
(2024)
S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal
Detecting hallucinations in large language models using semantic entropy
.
Nature
630
(
8017
),
pp. 625–630
.
Cited by:
§A.12
,
§1
,
§4
.
Gal and Ghahramani (2016)
Y. Gal and Z. Ghahramani
Dropout as a bayesian approximation: representing model uncertainty in deep learning
.
In
international conference on machine learning
,
pp. 1050–1059
.
Cited by:
§1
,
§4
,
§5
.
Gao
et al.
(2024)
X. Gao, J. Zhang, L. Mouatadid, and K. Das
SPUQ: perturbation-based uncertainty quantification for large language models
.
arXiv preprint arXiv:2403.02509
.
Cited by:
§A.10
,
§1
,
§4
.
Grattafiori
et al.
(2024)
A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan,
et al.
The llama 3 herd of models
.
arXiv preprint arXiv:2407.21783
.
Cited by:
§2
,
§5
.
Guo
et al.
(2017)
C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger
On calibration of modern neural networks
.
In
International conference on machine learning
,
pp. 1321–1330
.
Cited by:
§5
.
He
et al.
(2023)
G. He, J. Chen, and J. Zhu
Preserving pre-trained features helps calibrate fine-tuned language models
.
In
ICLR
,
Cited by:
§1
.
Hendrycks
et al.
(2020)
D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt
Measuring massive multitask language understanding
.
arXiv preprint arXiv:2009.03300
.
Cited by:
§5
.
Hoffmann
et al.
(2022)
J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai, E. Rutherford, D. de Las Casas, L. A. Hendricks, J. Welbl, A. Clark, T. Hennigan, E. Noland, K. Millican, G. van den Driessche, B. Damoc, A. Guy, S. Osindero, K. Simonyan, E. Elsen, J. W. Rae, O. Vinyals, and L. Sifre
Training compute-optimal large language models
.
ArXiv
abs/2203.15556
.
External Links:
Link
Cited by:
§4
.
Hou
et al.
(2023)
B. Hou, Y. Liu, K. Qian, J. Andreas, S. Chang, and Y. Zhang
Decomposing uncertainty for large language models through input clarification ensembling
.
External Links:
2311.08718
Cited by:
§1
,
§4
.
Hu
et al.
(2021a)
E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen
Lora: low-rank adaptation of large language models
.
arXiv preprint arXiv:2106.09685
.
Cited by:
§1
,
§2
,
§5
.
Hu
et al.
(2021b)
J. E. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, and W. Chen
LoRA: low-rank adaptation of large language models
.
ArXiv
abs/2106.09685
.
External Links:
Link
Cited by:
§4
.
Hyeon-Woo
et al.
(2021)
N. Hyeon-Woo, M. Ye-Bin, and T. Oh
Fedpara: low-rank hadamard product for communication-efficient federated learning
.
arXiv preprint arXiv: 2108.06098
.
Cited by:
§4
.
Iyer
et al.
(2022)
S. Iyer, X. V. Lin, R. Pasunuru, T. Mihaylov, D. Simig, P. Yu, K. Shuster, T. Wang, Q. Liu, P. S. Koura, X. Li, B. O’Horo, G. Pereyra, J. Wang, C. Dewan, A. Celikyilmaz, L. Zettlemoyer, and V. Stoyanov
OPT-iml: scaling language model instruction meta learning through the lens of generalization
.
ArXiv
abs/2212.12017
.
External Links:
Link
Cited by:
§4
.
Jacobs
et al.
(1991)
R. A. Jacobs, M. I. Jordan, S. J. Nowlan, and G. E. Hinton
Adaptive mixtures of local experts
.
Neural Computation
.
Cited by:
§4
.
Jiang
et al.
(2023)
A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford, D. S. Chaplot, D. d. l. Casas, F. Bressand, G. Lengyel, G. Lample, L. Saulnier,
et al.
Mistral 7b
.
arXiv preprint arXiv: 2310.06825
.
Cited by:
§A.3
.
Joshi
et al.
(2017)
M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer
TriviaQA: a large scale distantly supervised challenge dataset for reading comprehension
.
In
Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics
,
pp. 1601–1611
.
Cited by:
§A.12
,
§5
.
Kopiczko
et al.
(2023)
D. J. Kopiczko, T. Blankevoort, and Y. M. Asano
Vera: vector-based random matrix adaptation
.
arXiv preprint arXiv: 2310.11454
.
Cited by:
§4
.
Lakshminarayanan
et al.
(2017)
B. Lakshminarayanan, A. Pritzel, and C. Blundell
Simple and scalable predictive uncertainty estimation using deep ensembles
.
Advances in neural information processing systems
30
.
Cited by:
§1
,
§4
,
§5
.
Lampinen
et al.
(2023)
A. K. Lampinen, S. C. Y. Chan, I. Dasgupta, A. J. Nam, and J. X. Wang
Passive learning of active causal strategies in agents and language models
.
arXiv
.
Cited by:
§1
.
Lepikhin
et al.
(2020)
D. Lepikhin, H. Lee, Y. Xu, D. Chen, O. Firat, Y. Huang, M. Krikun, N. Shazeer, and Z. Chen
GShard: scaling giant models with conditional computation and automatic sharding
.
In
ICLR
,
Cited by:
§2
.
Li
et al.
(2024)
D. Li, Y. Ma, N. Wang, Z. Ye, Z. Cheng, Y. Tang, Y. Zhang, L. Duan, J. Zuo, C. Yang,
et al.
Mixlora: enhancing large language models fine-tuning with lora-based mixture of experts
.
arXiv preprint arXiv:2404.15159
.
Cited by:
§A.2
,
§1
,
§2
,
§3.4
,
§4
,
§5
,
§5
.
Li
et al.
(2022)
S. Li, X. Puig, C. Paxton, Y. Du, C. Wang, L. Fan, T. Chen, D. Huang, E. Akyürek, A. Anandkumar,
et al.
Pre-trained language models for interactive decision-making
.
Advances in Neural Information Processing Systems
35
,
pp. 31199–31212
.
Cited by:
§1
.
Lin
et al.
(2021)
S. Lin, J. Hilton, and O. Evans
Truthfulqa: measuring how models mimic human falsehoods
.
arXiv preprint arXiv:2109.07958
.
Cited by:
§A.12
,
§5
.
Liu
et al.
(2024)
S. Liu, C. Wang, H. Yin, P. Molchanov, Y. F. Wang, K. Cheng, and M. Chen
DoRA: weight-decomposed low-rank adaptation
.
arXiv preprint arXiv: 2402.09353
.
Cited by:
§4
.
Luo
et al.
(2024)
T. Luo, J. Lei, F. Lei, W. Liu, S. He, J. Zhao, and K. Liu
Moelora: contrastive learning guided mixture of experts on parameter-efficient fine-tuning for large language models
.
arXiv preprint arXiv: 2402.12851
.
Cited by:
§4
.
Mangrulkar
et al.
(2022)
S. Mangrulkar, S. Gugger, L. Debut, Y. Belkada, and S. Paul
PEFT: state-of-the-art parameter-efficient fine-tuning methods
.
Note:
https://github.com/huggingface/peft
Cited by:
§4
.
Mihaylov
et al.
(2018)
T. Mihaylov, P. Clark, T. Khot, and A. Sabharwal
Can a suit of armor conduct electricity? a new dataset for open book question answering
.
In
EMNLP
,
Cited by:
§5
.
OpenAI (2023)
OpenAI
GPT-4 technical report
.
External Links:
2303.08774
Cited by:
§1
.
Ouyang
et al.
(2022)
L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray,
et al.
Training language models to follow instructions with human feedback
.
Advances in Neural Information Processing Systems
35
,
pp. 27730–27744
.
Cited by:
§5.2
.
Paszke
et al.
(2019)
A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga,
et al.
Pytorch: an imperative style, high-performance deep learning library
.
Advances in neural information processing systems
32
.
Cited by:
§5
.
Qiu and Miikkulainen (2024)
X. Qiu and R. Miikkulainen
Semantic density: uncertainty quantification for large language models through confidence measurement in semantic space
.
arXiv preprint arXiv:2405.13845
.
Cited by:
§A.12
.
Renduchintala
et al.
(2023)
A. Renduchintala, T. Konuk, and O. Kuchaiev
Tied-lora: enhacing parameter efficiency of lora with weight tying
.
arXiv preprint arXiv: 2311.09578
.
Cited by:
§4
.
Singhal
et al.
(2022)
K. Singhal, S. Azizi, T. Tu, S. S. Mahdavi, J. Wei, H. W. Chung, N. Scales, A. Tanwani, H. Cole-Lewis, S. Pfohl, P. Payne, M. Seneviratne, P. Gamble, C. Kelly, N. Scharli, A. Chowdhery, P. Mansfield, B. A. y Arcas, D. Webster, G. S. Corrado, Y. Matias, K. Chou, J. Gottweis, N. Tomasev, Y. Liu, A. Rajkomar, J. Barral, C. Semturs, A. Karthikesalingam, and V. Natarajan
Large Language Models Encode Clinical Knowledge
.
arXiv
.
Cited by:
§1
.
Tian
et al.
(2023)
K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. D. Manning
Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback
.
arXiv preprint arXiv:2305.14975
.
Cited by:
§1
.
Touvron
et al.
(2023a)
H. Touvron, T. Lavril, G. Izacard, X. Martinet, M. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar,
et al.
Llama: open and efficient foundation language models
.
arXiv preprint arXiv:2302.13971
.
Cited by:
§5.2
.
Touvron
et al.
(2023b)
H. Touvron, T. Lavril, G. Izacard, X. Martinet, M. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample
LLaMA: open and efficient foundation language models
.
ArXiv
abs/2302.13971
.
External Links:
Link
,
2302.13971
Cited by:
§4
.
Touvron
et al.
(2023c)
H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale,
et al.
Llama 2: open foundation and fine-tuned chat models
.
arXiv preprint arXiv:2307.09288
.
Cited by:
§5.2
.
Touvron
et al.
(2023d)
H. Touvron, L. Martin, K. R. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, D. M. Bikel, L. Blecher, C. C. Ferrer, M. Chen, G. Cucurull, D. Esiobu, J. Fernandes, J. Fu, W. Fu, B. Fuller, C. Gao, V. Goswami, N. Goyal, A. S. Hartshorn, S. Hosseini, R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. M. Kloumann, A. V. Korenev, P. S. Koura, M. Lachaux, T. Lavril, J. Lee, D. Liskovich, Y. Lu, Y. Mao, X. Martinet, T. Mihaylov, P. Mishra, I. Molybog, Y. Nie, A. Poulton, J. Reizenstein, R. Rungta, K. Saladi, A. Schelten, R. Silva, E. M. Smith, R. Subramanian, X. Tan, B. Tang, R. Taylor, A. Williams, J. X. Kuan, P. Xu, Z. Yan, I. Zarov, Y. Zhang, A. Fan, M. Kambadur, S. Narang, A. Rodriguez, R. Stojnic, S. Edunov, and T. Scialom
Llama 2: open foundation and fine-tuned chat models
.
ArXiv
abs/2307.09288
.
External Links:
Link
Cited by:
§4
.
Wang
et al.
(2023)
X. Wang, L. Aitchison, and M. Rudolph
LoRA ensembles for large language model fine-tuning
.
arXiv preprint arXiv:2310.00035
.
Cited by:
§1
,
§4
.
Wang
et al.
(2020)
X. Wang, F. Yu, L. Dunlap, Y. Ma, R. Wang, A. Mirhoseini, T. Darrell, and J. E. Gonzalez
Deep mixture of experts via shallow embedding
.
In
Uncertainty in artificial intelligence
,
pp. 552–562
.
Cited by:
§4
.
Wang
et al.
(2024)
Y. Wang, H. Shi, L. Han, D. Metaxas, and H. Wang
Blob: bayesian low-rank adaptation by backpropagation for large language models
.
Advances in Neural Information Processing Systems
37
,
pp. 67758–67794
.
Cited by:
§A.11
,
§4
,
§5
.
Wu
et al.
(2024a)
H. Wu, H. Zheng, and B. Yu
Parameter-efficient sparsity crafting from dense to mixture-of-experts for instruction tuning on general tasks
.
arXiv preprint arXiv: 2401.02731
.
Cited by:
§4
.
Wu
et al.
(2023a)
S. Wu, O. Irsoy, S. Lu, V. Dabravolski, M. Dredze, S. Gehrmann, P. Kambadur, D. Rosenberg, and G. Mann
BloombergGPT: A Large Language Model for Finance
.
arXiv
.
Cited by:
§1
.
Wu
et al.
(2023b)
T. Wu, S. He, J. Liu, S. Sun, K. Liu, Q. Han, and Y. Tang
A brief overview of chatgpt: the history, status quo and potential future development
.
IEEE/CAA Journal of Automatica Sinica
10
(
5
),
pp. 1122–1136
.
Cited by:
§4
.
Wu
et al.
(2024b)
X. Wu, S. Huang, and F. Wei
Mixture of lora experts
.
arXiv preprint arXiv:2404.13628
.
Cited by:
§2
.
Xiao
et al.
(2022)
Y. Xiao, P. P. Liang, U. Bhatt, W. Neiswanger, R. Salakhutdinov, and L. Morency
Uncertainty quantification with pre-trained language models: a large-scale empirical analysis
.
In
EMNLP
,
Cited by:
§1
.
Xiong
et al.
(2024)
M. Xiong, Z. Hu, X. Lu, Y. Li, J. Fu, J. He, and B. Hooi
Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms
.
In
International Conference on Learning Representations
,
Cited by:
§A.12
.
Yang
et al.
(2024a)
A. X. Yang, M. Robeyns, X. Wang, and L. Aitchison
Bayesian low-rank adaptation for large language models
.
External Links:
2308.13111
Cited by:
§A.8
,
§1
,
§4
,
§5
,
§5
.
Yang
et al.
(2024b)
S. Yang, M. A. Ali, C. Wang, L. Hu, and D. Wang
MoRAL: moe augmented lora for llms’ lifelong learning
.
arXiv preprint arXiv: 2402.11260
.
Cited by:
§4
.
Zhai
et al.
(2023)
Y. Zhai, H. Zhang, Y. Lei, Y. Yu, K. Xu, D. Feng, B. Ding, and H. Wang
Uncertainty-penalized reinforcement learning from human feedback with diverse reward lora ensembles
.
arXiv preprint arXiv:2401.00243
.
Cited by:
§1
,
§4
.
Zhang
et al.
(2023)
Q. Zhang, M. Chen, A. Bukharin, P. He, Y. Cheng, W. Chen, and T. Zhao
Adaptive budget allocation for parameter-efficient fine-tuning
.
In
ICLR
,
Cited by:
§4
.
Zheng
et al.
(2024)
L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing,
et al.
Judging llm-as-a-judge with mt-bench and chatbot arena
.
NeurIPS
36
.
Cited by:
§4
.
Appendix A
Appendix
A.1
Theoretical Derivation of the Method
In this section, we provide complete theoretical statements and proofs that are used in Sec.
3
to derive our method.
Fact A.1
(Model Perturbation Structure, Restatement of Fact
3.1
)
.
Assume that in the residual connection architecture in each layer:
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
=
𝐡
ℓ
+
E
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
ℓ
)
)
g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})=\mathbf{h}^{\ell}+E_{k^{\ell}}^{\ell}\big(f_{trans}^{\ell}(\mathbf{h}^{\ell})\big)
, the Lipschitzness of the residual term
E
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
ℓ
)
)
E_{k^{\ell}}^{\ell}\big(f_{trans}^{\ell}(\mathbf{h}^{\ell})\big)
is much smaller as compared to that of
𝐡
ℓ
\mathbf{h}^{\ell}
itself:
‖
E
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
^
ℓ
)
)
−
E
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
ℓ
)
)
‖
=
o
⁡
(
‖
𝐡
^
ℓ
−
𝐡
ℓ
‖
)
\left\|E_{k^{\ell}}^{\ell}\big(f_{trans}^{\ell}(\hat{\mathbf{h}}^{\ell})\big)-E_{k^{\ell}}^{\ell}\big(f_{trans}^{\ell}(\mathbf{h}^{\ell})\big)\right\|=o\left(\|\hat{\mathbf{h}}^{\ell}-\mathbf{h}^{\ell}\|\right)
.
Under this regularity assumption, perturbations
Δ
​
f
​
(
x
)
\Delta f(x)
to the model
f
⁡
(
x
)
f(x)
approximately decomposes as:
Δ
​
f
​
(
x
)
≈
∑
ℓ
=
1
L
∑
k
ℓ
=
1
K
Δ
​
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
⋅
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
.
\Delta f(x)\approx\sum_{\ell=1}^{L}\sum_{k^{\ell}=1}^{K}\Delta\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell}).
Proof of Fact
3.1
and
A.1
.
In each layer, we can decompose the perturbation to the output as follows:
Δ
𝐡
ℓ
+
1
=
∑
k
ℓ
=
1
K
[
Δ
α
k
ℓ
ℓ
(
𝐡
ℓ
)
⋅
g
k
ℓ
ℓ
(
𝐡
ℓ
)
+
α
k
ℓ
ℓ
(
𝐡
ℓ
)
⋅
Δ
g
k
ℓ
ℓ
(
𝐡
ℓ
)
]
,
∀
ℓ
=
1
,
…
,
L
,
\displaystyle\Delta\mathbf{h}^{\ell+1}=\sum_{k^{\ell}=1}^{K}\left[\Delta\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})+\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot\Delta g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\right],\quad\forall\ell=1,\dots,L,
where the input
𝐡
1
=
x
\mathbf{h}^{1}=x
and the output
f
⁡
(
x
)
=
𝐡
L
+
1
f(x)=\mathbf{h}^{L+1}
.
Due to the residual connection architecture and our assumption on the regularity of the residual term, we have:
Δ
​
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
=
Δ
​
𝐡
ℓ
+
Δ
​
E
k
ℓ
ℓ
​
(
f
t
​
r
​
a
​
n
​
s
ℓ
​
(
𝐡
ℓ
)
)
=
Δ
​
𝐡
ℓ
+
o
⁡
(
Δ
​
𝐡
ℓ
)
.
\Delta g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})=\Delta\mathbf{h}^{\ell}+\Delta E_{k^{\ell}}^{\ell}\left(f_{trans}^{\ell}(\mathbf{h}^{\ell})\right)=\Delta\mathbf{h}^{\ell}+o\left(\Delta\mathbf{h}^{\ell}\right).
Hence,
Δ
​
𝐡
ℓ
+
1
≈
∑
k
ℓ
=
1
K
(
Δ
​
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
⋅
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
+
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
⋅
Δ
​
𝐡
ℓ
)
=
∑
k
ℓ
=
1
K
Δ
​
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
⋅
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
+
Δ
​
𝐡
ℓ
.
\displaystyle\Delta\mathbf{h}^{\ell+1}\approx\sum_{k^{\ell}=1}^{K}\left(\Delta\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})+\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot\Delta\mathbf{h}^{\ell}\right)=\sum_{k^{\ell}=1}^{K}\Delta\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})+\Delta\mathbf{h}^{\ell}.
Expanding this recursion, the output perturbation can be approximated as:
Δ
​
f
​
(
x
)
=
Δ
​
𝐡
L
+
1
≈
∑
ℓ
=
1
L
∑
k
ℓ
=
1
K
Δ
​
α
k
ℓ
ℓ
​
(
𝐡
ℓ
)
⋅
g
k
ℓ
ℓ
​
(
𝐡
ℓ
)
.
\Delta f(x)=\Delta\mathbf{h}^{L+1}\approx\sum_{\ell=1}^{L}\sum_{k^{\ell}=1}^{K}\Delta\alpha_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell})\cdot g_{k^{\ell}}^{\ell}(\mathbf{h}^{\ell}).
∎
Proposition A.2
(Calibration Loss, Restatement of Proposition
3.2
)
.
Let the calibration risk be defined as the expectation of the calibration loss over the data distribution:
ℒ
¯
cal
=
𝔼
(
x
,
y
∗
)
∼
𝒟
(
𝟙
{
MixLoRA
(
x
)
=
y
∗
}
−
FLC
(
x
)
)
2
.
\bar{\mathcal{L}}_{\mathrm{cal}}=\mathbb{E}_{(x,y^{*})\sim\mathcal{D}}\left(\mathbbm{1}\{\mathrm{MixLoRA}(x)=y^{*}\}-\mathrm{FLC}(x)\right)^{2}.
If this calibration risk is optimized over the data distribution
𝒟
\mathcal{D}
, then the optimal solution is
FLC
⁡
(
x
)
=
ℙ
⁡
(
MixLoRA
⁡
(
x
)
=
y
∗
​
(
x
)
)
\mathrm{FLC}(x)=\mathbb{P}(\mathrm{MixLoRA}(x)=y^{*}(x))
; that is, the optimally trained FLC corresponds to the probability that the model’s prediction is correct.
Proof of Proposition
3.2
and
A.2
.
Expanding the calibration risk, we have:
ℒ
¯
cal
\displaystyle\bar{\mathcal{L}}_{\mathrm{cal}}
=
𝔼
(
x
,
y
∗
)
∼
𝒟
(
𝟙
{
MixLoRA
(
x
)
=
y
∗
}
−
FLC
(
x
)
)
2
\displaystyle=\mathbb{E}_{(x,y^{*})\sim\mathcal{D}}\left(\mathbbm{1}\{\mathrm{MixLoRA}(x)=y^{*}\}-\mathrm{FLC}(x)\right)^{2}
=
𝔼
(
x
,
y
∗
)
∼
𝒟
[
𝟙
{
MixLoRA
(
x
)
=
y
∗
}
]
2
\displaystyle=\mathbb{E}_{(x,y^{*})\sim\mathcal{D}}\left[\mathbbm{1}\{\mathrm{MixLoRA}(x)=y^{*}\}\right]^{2}
−
2
𝔼
x
𝔼
y
∗
|
x
[
𝟙
{
MixLoRA
(
x
)
=
y
∗
}
⋅
FLC
(
x
)
]
+
𝔼
x
[
FLC
(
x
)
2
]
\displaystyle\quad-2\,\mathbb{E}_{x}\mathbb{E}_{y^{*}|x}\left[\mathbbm{1}\{\mathrm{MixLoRA}(x)=y^{*}\}\cdot\mathrm{FLC}(x)\right]+\mathbb{E}_{x}\left[\mathrm{FLC}(x)^{2}\right]
=
C
+
𝔼
x
​
[
FLC
​
(
x
)
2
−
2
​
ℙ
​
(
MixLoRA
⁡
(
x
)
=
y
∗
​
(
x
)
)
⋅
FLC
⁡
(
x
)
]
,
\displaystyle=C+\mathbb{E}_{x}\left[\mathrm{FLC}(x)^{2}-2\,\mathbb{P}(\mathrm{MixLoRA}(x)=y^{*}(x))\cdot\mathrm{FLC}(x)\right],
where
C
C
is a constant independent of
FLC
⁡
(
x
)
\mathrm{FLC}(x)
. Thus, the calibration risk is minimized when
FLC
⁡
(
x
)
=
ℙ
⁡
(
MixLoRA
⁡
(
x
)
=
y
∗
​
(
x
)
)
\mathrm{FLC}(x)=\mathbb{P}(\mathrm{MixLoRA}(x)=y^{*}(x))
.
∎
A.2
Load Balancing Loss
We follow the load balancing loss in
[
Li et al., 2024
]
. Given
N
N
experts indexed by
i
=
1
i=1
to
N
N
and a batch
B
B
with
T
T
tokens, the auxiliary loss is computed as:
ℒ
a
​
u
​
x
=
a
⋅
N
⋅
∑
i
=
1
N
ℱ
i
⋅
𝒫
i
,
\displaystyle\mathcal{L}_{aux}=a\cdot N\cdot\sum^{N}_{i=1}\mathcal{F}_{i}\cdot\mathcal{P}_{i},
(14)
where
ℱ
i
=
1
T
∑
x
∈
B
𝟙
{
a
r
g
m
a
x
k
ℛ
(
x
)
k
=
i
}
,
𝒫
i
=
1
T
∑
x
∈
B
ℛ
(
x
)
i
.
\displaystyle\mathcal{F}_{i}=\frac{1}{T}\sum_{x\in B}\mathbbm{1}\{argmax_{k}\mathcal{R}(x)_{k}=i\},\mathcal{P}_{i}=\frac{1}{T}\sum_{x\in B}\mathcal{R}(x)_{i}.
(15)
Here,
ℛ
⁡
(
⋅
)
\mathcal{R}(\cdot)
is the top-k router,
ℱ
i
\mathcal{F}_{i}
is the fraction of tokens dispatched to expert
i
i
and
𝒫
i
\mathcal{P}_{i}
is the fraction of the router probability allocated for expert
i
i
. The final loss is multiplied by the expert count
N
N
to keep the loss constant as the number of experts varies, and the constant term
a
a
is set to
10
−
2
10^{-2}
as a multiplicative coefficient, which is large enough to ensure load balancing while remaining small enough not to overwhelm the primary objective.
A.3
Experimental Results with Mistral-7B
In this section, we present the results using Mistral-7B
[
Jiang et al., 2023
]
, a different decoder-based LLM backbone. Table
4
shows the results of fine-tuning Mistral-7B on
3
3
common-sense reasoning tasks and one domain-specific climate question-answering task.
For each of the tasks, UQ4CT effectively calibrates the parameter mixtures, leading to the best ECE performance in
3
3
out of
4
4
tasks. This indicates the robustness of UQ4CT across different LLMs.
Table 4:
Performance comparison of different methods fine-tuned with Mistral-7B across
3
3
common sense reasoning tasks and a domain-specific task. UQ4CT shows significant ECE improvements while maintaining high accuracy.
Metrics
Methods
ARC-E
ARC-C
OBQA
ClimateQA
ACC
↑
\uparrow
LoRA
84.8
0.47
84.8_{0.47}
70.2
0.84
70.2_{0.84}
82.8
0.62
82.8_{0.62}
72.5
1.6
72.5_{1.6}
MC Drop
84.6
0.91
84.6_{0.91}
69.6
0.76
69.6_{0.76}
82.6
0.71
82.6_{0.71}
72.5
1.6
72.5_{1.6}
Ensemble
84.2
0.66
84.2_{0.66}
71.0
1.41
71.0_{1.41}
82.5
0.6
82.5_{0.6}
72.9
2.88
72.9_{2.88}
LA
82.4
2.05
82.4_{2.05}
68.5
3.31
68.5_{3.31}
82.5
0.77
82.5_{0.77}
71.6
1.56
71.6_{1.56}
MixLoRA
85.5
1.27
85.5_{1.27}
71.2
1.75
71.2_{1.75}
83.3
1.14
83.3_{1.14}
72.0
1.69
72.0_{1.69}
UQ4CT
85.9
0.82
\mathbf{85.9_{0.82}}
74.4
0.82
\mathbf{74.4_{0.82}}
83.7
1.22
\mathbf{83.7_{1.22}}
73.2
1.29
\mathbf{73.2_{1.29}}
ECE
↓
\downarrow
LoRA
9.46
1.62
9.46_{1.62}
18.42
1.91
18.42_{1.91}
13.3
0.25
13.3_{0.25}
13.72
2.62
13.72_{2.62}
MC Drop
8.91
1.35
8.91_{1.35}
18.38
1.66
18.38_{1.66}
13.3
0.31
13.3_{0.31}
13.72
2.61
13.72_{2.61}
Ensemble
8.72
1.49
8.72_{1.49}
17.0
0.97
17.0_{0.97}
9.14
2.82
9.14_{2.82}
12.86
1.78
12.86_{1.78}
LA
20.3
5.7
20.3_{5.7}
21.27
4.15
21.27_{4.15}
6.41
3.22
\mathbf{6.41_{3.22}}
14.64
2.21
14.64_{2.21}
MixLoRA
8.16
0.99
8.16_{0.99}
15.51
3.86
15.51_{3.86}
10.53
1.73
10.53_{1.73}
14.05
3.09
14.05_{3.09}
UQ4CT
5.7
0.69
\mathbf{5.7_{0.69}}
7.04
0.58
\mathbf{7.04_{0.58}}
7.92
1.14
¯
\underline{7.92_{1.14}}
11.4
1.14
\mathbf{11.4_{1.14}}
A.4
Sensitivity Test on Calibration Term
To understand the effectiveness of the calibration loss, we perform a sensitivity test of
β
\beta
in Equation
13
. This evaluates how our proposed calibration of parameter mixtures affects the overall model prediction and uncertainty quantification capabilities. We evaluate
β
\beta
values ranging from
0
0
to
1.5
1.5
, where
β
=
0
\beta=0
resembles the original MixLoRA method.
Table 5:
Performance of UQ4CT with varying
β
\beta
values on the OBQA dataset. Prediction accuracy and uncertainty calibration improve with increasing
β
\beta
, highlighting the effectiveness of
ℒ
cal
\mathcal{L}_{\mathrm{cal}}
.
β
\beta
0
0
0.2
0.2
0.5
0.5
0.8
0.8
1
1
1.2
1.2
1.5
1.5
ACC
↑
\uparrow
87.0
2.85
87.0_{2.85}
87.1
0.58
87.1_{0.58}
87.1
0.29
87.1_{0.29}
87.3
0.38
87.3_{0.38}
88.4
0.35
\mathbf{88.4_{0.35}}
88.3
0.57
88.3_{0.57}
87.5
0.88
87.5_{0.88}
ECE
↓
\downarrow
12.7
1.92
12.7_{1.92}
7.35
0.75
7.35_{0.75}
7.69
0.89
7.69_{0.89}
5.82
1.12
5.82_{1.12}
3.34
1.60
\mathbf{3.34_{1.60}}
6.31
2.58
6.31_{2.58}
9.03
0.82
9.03_{0.82}
Results in Table
5
demonstrate the effectiveness of the calibration loss. Without calibration (
β
=
0
\beta=0
), the model exhibits high ECE. Even small values (
β
=
0.2
\beta=0.2
or
0.5
0.5
) yield substantial ECE improvements. The best trade-off is at
β
=
1
\beta=1
, where the calibration term effectively optimizes the conditional parameter mixtures to fit the data distribution, achieving both the lowest ECE and highest accuracy. Beyond
β
=
1
\beta=1
, the calibration term begins to dominate the training objective, degrading both metrics.
A.5
Number of Active Experts
One important aspect of the LoRA MoE architecture is how many experts to activate. We investigate the performance impact of different numbers of active LoRA experts, evaluating the model with
1
1
to
5
5
active experts out of
8
8
total.
Table 6:
Performance comparison of UQ4CT with varying number of experts on OBQA dataset. Top-2 expert selection strategy grants best accuracy and calibration.
Top-K
ACC
↑
\uparrow
ECE
↓
\downarrow
Top-1
86.8
0.59
86.8_{0.59}
7.54
1.89
7.54_{1.89}
Top-2
88.4
0.35
\mathbf{88.4_{0.35}}
3.34
1.60
\mathbf{3.34_{1.60}}
Top-3
87.0
0.77
87.0_{0.77}
5.68
0.78
5.68_{0.78}
Top-4
87.4
0.51
87.4_{0.51}
7.52
0.44
7.52_{0.44}
Top-5
87.1
0.48
87.1_{0.48}
6.16
0.58
6.16_{0.58}
As shown in Table
6
,
2
2
active experts give the optimal performance in terms of accuracy and ECE scores. One expert alone cannot capture complicated functional relationships, while more than
2
2
experts could potentially introduce redundant functional bases to the model, which deviates the output distribution from the data distribution, thus worsening predictive and calibration performance. Additionally, more active experts lead to a more flattened distribution across experts, which hardens the alignment of parameter mixtures during fine-tuning.
A.6
Incremental Weighting on Calibration Term.
Due to the random initialization of LoRA experts, the predictions during early fine-tuning stage are likely to be incorrect as the model has little knowledge on the functional relationships regarding the data. Thus, it is intuitive to incrementally increase the weight parameter
β
\beta
over the calibration term
ℒ
cal
\mathcal{L}_{\mathrm{cal}}
in the training loss for the LoRA experts to learn before calibration. We conduct this study by incrementally increase
β
\beta
from
0
0
to
1
1
within
50
50
gradient steps during the early stage of fine-tuning:
β
=
min
⁡
{
1
,
current
​
_
​
grad
​
_
​
step
50
}
.
\beta=\min\left\{1,\frac{\mathrm{current\_grad\_step}}{50}\right\}.
(16)
We choose
50
50
gradient steps from our observation that training loss generally stabilizes after
50
50
gradient steps, indicating the LoRA experts have learned some functional relationships from data.
As shown in Table
7
, the incremental loss has significantly worse ECE performance across all tasks. This demonstrates the advantage of uncertainty calibration even in the early stage. In the beginning, the lack of functional relationships on the training data in LoRA experts lead to high uncertainty. Thus, UQ4CT encourages exploration over all LoRA experts while UQ4CT_Incremental lacks it due to the small weighting in the beginning.
Table 7:
Performance comparison of UQ4CT with and without incremental weighting. Incremental weighting has worse ECE performance while maintains similar accuracy.
Metrics
Methods
ARC-E
ARC-C
OBQA
ClimateQA
ACC
↑
\uparrow
UQ4CT
88.66
0.20
88.66_{0.20}
79.60
1.21
79.60_{1.21}
88.40
0.35
88.40_{0.35}
79.97
0.85
79.97_{0.85}
UQ4CT_Incremental
87.15
0.95
87.15_{0.95}
80.84
1.03
80.84_{1.03}
88.53
0.48
88.53_{0.48}
75.87
2.89
75.87_{2.89}
ECE
↓
\downarrow
UQ4CT
3.97
0.78
\mathbf{3.97_{0.78}}
4.43
0.82
\mathbf{4.43_{0.82}}
3.34
1.60
\mathbf{3.34_{1.60}}
9.36
2.77
\mathbf{9.36_{2.77}}
UQ4CT_Incremental
6.55
1.42
6.55_{1.42}
10.02
1.95
10.02_{1.95}
6.87
1.68
6.87_{1.68}
14.16
0.91
14.16_{0.91}
A.7
Training Details
We train our model with total of
8
8
LoRA experts, and select
2
2
experts with the highest probability. For each expert, we use
r
​
a
​
n
​
k
=
16
rank=16
and
a
​
l
​
p
​
h
​
a
=
32
alpha=32
. We use batch size of
16
16
to train our model. For climate task, we set the learning rate to
5
​
e
−
4
5e-4
and dropout rate to
0.1
0.1
to incorporate the small dataset size. For other tasks, we use
2
​
e
−
4
2e-4
as our learning rate with dropout
0.05
0.05
. We use AdamW as our optimizer and a cutoff length of
512
512
for prompts during training. Our model is trained on A100 GPU, with 20GB GPU memory consumption per task. Training time is from
25
25
to
50
50
minutes depending on the task.
The experimental setup for single LoRA based models is similar with LoRA ranks set to
80
80
to accommodate the MoE model size. For the ensemble baseline, we use an ensemble size of
8
8
with
r
​
a
​
n
​
k
=
16
rank=16
. For Laplace-LoRA, we follow the Laplace hyperparameters in
this Github Repository
.
A.8
Expected Calibration Error
Expected calibration error (ECE) is a commonly used metric to asses uncertainty quantification performance. ECE measures the alignment between prediction accuracy and model confidence through regrouping the predicted probabilities into
m
m
bins. This method then computes the weighted average of the difference between average accuracy and confidence in each bin:
ECE
=
∑
m
=
1
M
|
B
m
|
N
​
|
acc
​
(
B
m
)
−
conf
​
(
B
m
)
|
,
\displaystyle\text{ECE}=\sum_{m=1}^{M}\frac{|B_{m}|}{N}|\text{acc}(B_{m})-\text{conf}(B_{m})|,
(17)
where
|
B
m
|
|B_{m}|
is the number of evaluated datapoints in bin
m
m
, acc and conf is calculated as following:
acc
​
(
B
m
)
=
1
|
B
m
|
​
∑
i
∈
B
m
𝟏
​
(
y
^
i
=
y
i
)
,
\displaystyle\text{acc}(B_{m})=\frac{1}{|B_{m}|}\sum_{i\in B_{m}}\mathbf{1}(\hat{y}_{i}=y_{i}),
(18)
conf
​
(
B
m
)
=
1
|
B
m
|
​
∑
i
∈
B
m
P
⁡
(
y
^
i
)
.
\displaystyle\text{conf}(B_{m})=\frac{1}{|B_{m}|}\sum_{i\in B_{m}}P(\hat{y}_{i}).
(19)
In this paper, we use an ECE bin size of
15
15
, following the experiment setup in Laplace-LoRA
[
Yang et al., 2024a
]
.
A.9
MMLU Distribution Shift Dataset Composition
•
Computer Science (CS)
:
–
College Computer Science
–
Computer Security
–
High School Computer Science
–
Machine Learning
•
Engineering (Eng)
:
–
Electrical Engineering
•
Law
:
–
International Law
–
Jurisprudence
–
Professional Law
•
Health
:
–
Anatomy
–
Clinical Knowledge
–
College Medicine
–
Human Aging
–
Nutrition
–
Professional Medicine
–
Virology
A.10
Prompt Perturbation Comparison
Here, we compare our method with SPUQ
[
Gao et al., 2024
]
, which perturbs the prompt, aggregates predictions and confidences to measure uncertainty. We test SPUQ and UQ4CT with LLama3.1-8b as the base model. As shown in Table
8
, SPUQ’s large ECE values suggest that simply aggregating predictions from perturbed prompts does not adequately calibrate model confidence, highlighting the limitations of prompt perturbation as an uncertainty quantification strategy for LLMs, especially for smaller models.
Table 8:
Performance comparison of UQ4CT and SPUQ across four tasks. UQ4CT achieves higher accuracy and substantially lower ECE than SPUQ.
Metrics
Methods
ARC-E
ARC-C
OBQA
ClimateQA
ACC
↑
\uparrow
SPUQ
86.67
86.67
73.94
73.94
74.00
74.00
67.80
67.80
UQ4CT
88.66
0.20
88.66_{0.20}
79.60
1.21
79.60_{1.21}
88.40
0.35
88.40_{0.35}
79.97
0.85
79.97_{0.85}
ECE
↓
\downarrow
SPUQ
10.81
10.81
7.40
7.40
8.86
8.86
14.68
14.68
UQ4CT
3.97
0.78
\mathbf{3.97_{0.78}}
4.43
0.82
\mathbf{4.43_{0.82}}
3.34
1.60
\mathbf{3.34_{1.60}}
9.36
2.77
\mathbf{9.36_{2.77}}
A.11
Peak Memory Analysis
We provide a peak memory analysis using the same setup (Llama3.1-8B, OBQA, single A100, bf16 training). Following the BLoB paper’s asymmetric design (Sec 3.1 of
Wang et al. [2024]
), only
𝐀
\mathbf{A}
is Bayesianized with variance parameterized by
𝐆
∈
ℝ
r
×
n
in
\mathbf{G}\in\mathbb{R}^{r\times n_{\text{in}}}
, and training uses
K
=
1
K=1
sample with Flipout.
All three methods adapt 7 matrices per layer (Q, K, V, O, gate, up, down) across 32 layers. For Llama3.1-8B:
•
Q, K, V, O:
n
in
=
n
out
=
4096
n_{\text{in}}=n_{\text{out}}=4096
•
Gate, Up:
n
in
=
4096
n_{\text{in}}=4096
,
n
out
=
14336
n_{\text{out}}=14336
•
Down:
n
in
=
14336
n_{\text{in}}=14336
,
n
out
=
4096
n_{\text{out}}=4096
Per layer:
∑
n
in
=
4
×
4096
+
2
×
4096
+
14336
=
38912
\sum n_{\text{in}}=4\times 4096+2\times 4096+14336=38912
,
∑
n
out
=
4
×
4096
+
2
×
14336
+
4096
=
43008
\sum n_{\text{out}}=4\times 4096+2\times 14336+4096=43008
,
∑
(
n
in
+
n
out
)
=
81920
\sum(n_{\text{in}}+n_{\text{out}})=81920
.
Trainable parameters (bf16, 2 bytes/param).
Table 9:
Trainable parameter counts for LoRA, UQ4CT, and BLoB (bf16, 2 bytes/param).
Method
Component
Params
bf16
LoRA (
r
=
80
r{=}80
)
𝐁
∈
ℝ
n
out
×
r
\mathbf{B}\in\mathbb{R}^{n_{\text{out}}\times r}
:
80
×
43008
×
32
=
110.10
80\times 43008\times 32=110.10
M
𝐀
∈
ℝ
r
×
n
in
\mathbf{A}\in\mathbb{R}^{r\times n_{\text{in}}}
:
80
×
38912
×
32
=
99.61
80\times 38912\times 32=99.61
M
209.72M
0.41 GB
UQ4CT (
K
=
8
K{=}8
,
r
=
16
r{=}16
)
8 experts, each
𝐁
k
,
𝐀
k
\mathbf{B}_{k},\mathbf{A}_{k}
:
8
×
16
×
81920
×
32
=
335.54
8\times 16\times 81920\times 32=335.54
M
Routers
𝐖
r
∈
ℝ
K
×
d
\mathbf{W}_{r}\in\mathbb{R}^{K\times d}
:
7
×
8
×
4096
×
32
=
7.34
7\times 8\times 4096\times 32=7.34
M
342.88M
0.64 GB
BLoB (
r
=
80
r{=}80
)
𝐁
∈
ℝ
n
out
×
r
\mathbf{B}\in\mathbb{R}^{n_{\text{out}}\times r}
(deterministic):
80
×
43008
×
32
=
110.10
80\times 43008\times 32=110.10
M
𝐌
∈
ℝ
r
×
n
in
\mathbf{M}\in\mathbb{R}^{r\times n_{\text{in}}}
(mean of
𝐀
\mathbf{A}
):
80
×
38912
×
32
=
99.61
80\times 38912\times 32=99.61
M
𝐆
∈
ℝ
r
×
n
in
\mathbf{G}\in\mathbb{R}^{r\times n_{\text{in}}}
(std param of
𝐀
\mathbf{A}
,
Ω
=
𝐆
2
\Omega=\mathbf{G}^{2}
):
80
×
38912
×
32
=
99.61
80\times 38912\times 32=99.61
M
309.33M
0.58 GB
Note:
∑
n
out
>
∑
n
in
\sum n_{\text{out}}>\sum n_{\text{in}}
because the FFN gate/up layers project from 4096 to 14336 (large
n
out
n_{\text{out}}
), while the down layer reverses this. The asymmetry does not cancel, so
𝐁
\mathbf{B}
(which depends on
n
out
n_{\text{out}}
) has more parameters than
𝐌
\mathbf{M}
or
𝐆
\mathbf{G}
(which depend on
n
in
n_{\text{in}}
).
Peak GPU memory breakdown.
Table 10:
Peak GPU memory breakdown for LoRA, UQ4CT, and BLoB on Llama3.1-8B (OBQA, single A100, bf16).
Component
LoRA
UQ4CT
BLoB
Base model (frozen, bf16)
16.00 GB
16.00 GB
16.00 GB
Adapter params (bf16, 2B/param)
0.41 GB
0.64 GB
0.58 GB
Optimizer states (fp32, 8B/param)
1.56 GB
2.57 GB
2.31 GB
Gradients (bf16, 2B/param)
0.39 GB
0.64 GB
0.58 GB
Sampling buffers (
𝐄
\mathbf{E}
, sampled
𝐀
\mathbf{A}
, each
r
×
n
in
r\times n_{\text{in}}
)
—
—
0.38 GB
Activations/KV cache (shared)
∼
{\sim}
1.50 GB
∼
{\sim}
1.50 GB
∼
{\sim}
1.50 GB
Estimated peak
∼
19.86
\mathbf{{\sim}19.86}
GB
∼
21.35
\mathbf{{\sim}21.35}
GB
∼
21.35
\mathbf{{\sim}21.35}
GB
As the analysis above shows, UQ4CT and BLoB have nearly identical peak memory (
∼
{\sim}
21.35 GB), both
∼
{\sim}
1.49 GB (
∼
{\sim}
7.50%) above standard LoRA, which is minimal and manageable. UQ4CT’s overhead comes from additional expert parameters, while BLoB’s comes from variance parameters (
𝐆
\mathbf{G}
) plus sampling buffers.
A.12
Open-Ended Generative Setup
To extend UQ4CT beyond multiple-choice settings, we adapt the calibration loss (Eq.
12
) for open-ended generation by replacing the exact-match indicator with an F1-score-based correctness proxy:
ℒ
cal
=
(
𝟙
{
F
1
(
MixLoRA
(
x
)
,
y
∗
)
>
τ
}
−
FLC
(
x
)
)
2
,
\mathcal{L}_{\mathrm{cal}}=\left(\mathbbm{1}\{F_{1}(\mathrm{MixLoRA}(x),y^{*})>\tau\}-\mathrm{FLC}(x)\right)^{2},
(20)
where
τ
=
0.3
\tau=0.3
. If the token-level F1 between the generated answer and the ground truth exceeds
τ
\tau
, we count the prediction as correct. The threshold
τ
=
0.3
\tau=0.3
is motivated by
Alur et al. [2024]
, who show that this level aligns with human judgment boundaries for partial-credit correctness in open-ended QA.
We evaluate on TruthfulQA
[
Lin et al., 2021
]
and TriviaQA
[
Joshi et al., 2017
]
using Llama-3.1-8B-Instruct. To ensure a controlled comparison, we first fine-tune the base model with MixLoRA (rank=16, 8 experts), then apply all UQ baseline methods to this shared fine-tuned backbone. The baselines include
Sequence Probability (SeqProb)
and
Verbalized Confidence
[
Xiong et al., 2024
]
,
Verbalized Consistency
[
Xiong et al., 2024
]
,
Semantic Entropy
[
Farquhar et al., 2024
]
, and
Semantic Density
[
Qiu and Miikkulainen, 2024
]
. Sampling-based methods (marked with *) use
N
=
5
N=5
samples per question. All baselines use average generated token probability as confidence.