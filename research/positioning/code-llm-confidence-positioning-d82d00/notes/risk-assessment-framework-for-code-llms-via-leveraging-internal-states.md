---
title: Risk Assessment Framework for Code LLMs via Leveraging Internal States
id: risk-assessment-framework-for-code-llms-via-leveraging-internal-states
tags:
- code-llm-confidence-positioning-d82d00
- close-occupant
created: '2026-11-09T23:18:15.935538Z'
updated: '2026-11-09T23:27:44.782590Z'
source: https://arxiv.org/html/2504.14640
source_domain: arxiv.org
fetched_at: '2026-11-09T23:18:15.935178Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: FULL TEXT (Huang et al., PtTrust, arXiv 2504.14640, Fujitsu). Two-stage internal-state
  risk predictor (SAE pre-training then labeled risk predictor) for code-line-level
  risk assessment on HumanEvalPack and DebugBench with transfer to code editing, translation,
  repair (StarCoder2-15B among targets). L4 occupant for line-level localization via
  internal states; no verbal readout.
---

Risk Assessment Framework for Code LLMs via Leveraging Internal States
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: arXiv.org perpetual non-exclusive license
arXiv:2504.14640v1 [cs.SE] 20 Apr 2025
Risk Assessment Framework for Code LLMs via Leveraging Internal States
Conference:
33rd ACM
International Conference on the Foundations of Software Engineering; June
23–28, 2025; Trondheim, Norway
33rd ACM International Conference on the Foundations of
Software Engineering (FSE Companion ’25), June 23–28, 2025, Trondheim,
Norway
DOI:
10.1145/3696630.3728566
ISBN:
979-8-4007-1276-0/2025/06
CCS:
Computing methodologies Natural language generation
CCS:
Software and its engineering Development frameworks and environments
Yuheng Huang
Affiliation:
The University of Tokyo
email:
yuhenghuang42@g.ecc.u-tokyo.ac.jp
,
Lei Ma
Affiliation:
The University of Tokyo
Affiliation:
University of Alberta
email:
ma.lei@acm.org
,
Keizaburo Nishikino
Affiliation:
Fujitsu Limited
email:
nishikino@fujitsu.com
and
Takumi Akazaki
Affiliation:
Fujitsu Limited
email:
akazaki.takumi@fujitsu.com
© acmlicensed
Abstract.
The pre-training paradigm plays a key role in the success of Large Language Models (LLMs), which have been recognized as one of the most significant advancements of AI recently. Building on these breakthroughs, code LLMs with advanced coding capabilities bring huge impacts on software engineering, showing the tendency to become an essential part of developers’ daily routines. However, the current code LLMs still face serious challenges related to trustworthiness, as they can generate incorrect, insecure, or unreliable code.
Recent exploratory studies find that it can be promising to detect such risky outputs by analyzing LLMs’ internal states, akin to how the human brain unconsciously recognizes its own mistakes. Yet, most of these approaches are limited to narrow sub-domains of LLM operations and fall short of achieving industry-level scalability and practicability. To address these challenges, in this paper, we propose
PtTrust
, a two-stage risk assessment framework for code LLM based on internal state pre-training, designed to integrate seamlessly with the existing infrastructure of software companies. The core idea is that the risk assessment framework could also undergo a pre-training process similar to LLMs. Specifically,
PtTrust
first performs unsupervised pre-training on large-scale unlabeled source code to learn general representations of LLM states. Then, it uses a small, labeled dataset to train a risk predictor. We demonstrate the effectiveness of
PtTrust
through fine-grained, code line-level risk assessment and demonstrate that it generalizes across tasks and different programming languages. Further experiments also reveal that
PtTrust
provides highly intuitive and interpretable features, fostering greater user trust. We believe
PtTrust
makes a promising step toward scalable and trustworthy assurance for code LLMs.
Keywords:
Large Language Models, LLMs, Risk Assessment, Trustworthiness Assurance, AI-assisted programming, Pre-training,
1.
Introduction
The biggest lesson that can be read from 70 years of AI research is that general methods that leverage computation are
ultimately the most effective, and by a large margin.
Seeking an improvement that makes a difference in the shorter term, researchers seek to leverage their human knowledge of the domain, but the only thing that matters in the long run is the
leveraging of computation.
The Bitter Lesson
— Richard S. Sutton
The recent advancements in Large Language Models (LLMs) are continuously exhibiting significant impacts on software engineering, which are increasingly integrated into various stages of the development lifecycle and are becoming an essential component of many software development processes and ecosystems.
In particular, some recent state-of-the-art (SOTA) LLMs demonstrate remarkable performance across a wide range of software engineering tasks, including requirements engineering, software design, development, program analysis, quality assurance, and maintenance
(
Hou et al., 2024
)
. For example, a survey from GitHub conducted in late 2023 revealed that 92% of U.S.-based developers were already utilizing AI coding tools
(
Inbal Shani, 2025
)
. This trend continues to grow, highlighting the significant impact of these technologies on the software development industry. As an active industrial contributor in these advancements, Fujitsu has recently developed several pre-trained models, including its most advanced version, Takane
(
Fujitsu Limited, 2024a
)
, together with highly customized and secure services for private LLM deployments
(
Fujitsu Limited, 2024b
)
, towards addressing the industrial urgent demand.
Despite the promise, in practice, the current LLMs still face significant challenges in trustworthiness. Recent studies revealed that their generated code often lacks robustness, security, usability, and correctness
(
Arakelyan et al., 2023
;
Pearce et al., 2022
;
Barke et al., 2023
;
Chen et al., 2021
;
Nguyen and Nadi, 2022
;
Jesse et al., 2023
;
Wang et al., 2024c
)
. Additionally, a user study
(
Tang et al., 2024
)
found that LLM-generated code introduces atypical errors with patterns distinct from human errors, potentially increasing the cognitive load for developers. These trustworthiness concerns could potentially impede the widespread adoption of LLM technologies. Recognizing this, Fujitsu is actively engaged in R&D efforts to create more trustworthy LLMs, contributing to advancing reliable, safe, and secure LLM systems.
A practical approach to enhance user trust in LLMs is designing automated tools that help users understand inherent risks and identify potential issues. While compiling test cases to evaluate different aspects (e.g., security, correctness) of the generated code is a viable option, manual test cases can introduce additional labor costs, and LLM-generated tests risk “chasing one’s own tail” issues. Another approach is to examine the internal workings of LLMs and identify potential risk patterns within their vast network of neurons. This is akin to identifying error neuron behaviors in the human brain, which subconsciously signal when something is amiss
(
Frank et al., 2005
)
. Preliminary studies have shown the potential of this approach in natural language processing (NLP) tasks for LLMs
(
Azaria and Mitchell, 2023
)
.
Although promising, these techniques primarily focus on NLP tasks rather than code-related tasks and have yet to achieve industry-level practicability. A significant limitation is that most existing approaches still follow a pre-LLM paradigm, training classifiers based on LLMs’ internal states using a small domain-specific dataset. This approach often fails to generalize effectively to other tasks, which is a critical drawback given LLMs’ foundational and multi-task nature.
To address such challenges, in this paper, we propose
PtTrust
, a two-stage pre-training framework for risk assessment of code LLMs: (1) The first stage leverages unsupervised learning with a recently introduced architecture called Sparse Autoencoders (SAE)
(
Gao et al., 2024
)
, where OpenAI claims to find scaling laws on them, (2) The second semantic binding stage uses supervised learning to enable generalization across different trustworthiness properties. In particular,
PtTrust
is designed to leverage the existing infrastructure of software companies, allowing it to be seamlessly integrated into existing code LLM service platforms.
We demonstrate the promising of
PtTrust
through a fine-grained, code line-level risk assessment task. This task is based on the observation that when code LLMs make mistakes, it is often that not all code lines are incorrect, but identifying the problematic lines can be time-consuming for developers. By prioritizing incorrect code lines, developers can save significant time and effort. While the company regulations prevent us from directly sharing internal data and results in this paper, we conducted a series of experiments using three representative LLMs with advanced coding capabilities (i.e., Code Llama, StarCoder2, Qwen2.5-Coder) on publicly available datasets. Through only labels on Python languages for code generation and repair datasets (i.e., HumanEval
(
Chen et al., 2021
)
, HumanEvalPack
(
Muennighoff et al., 2023
)
, and QuixBug
(
Lin et al., 2017
)
),
PtTrust
shows highly promising results across tasks (in Python and Java), e.g., including code editing, code translation, and code repair. The results highlight
PtTrust
’s SOTA cross-language and cross-task capabilities in identifying risks associated with code LLMs.
The main contributions of this paper are summarized as follows:
•
We proposed a two-stage pre-training risk assessment platform
PtTrust
for code LLMs, which is designed to integrate seamlessly with the infrastructure of software companies. This platform is built to scale efficiently to large-scale corpora, potentially providing trustworthy guardrails to the company’s code assets generated by LLMs.
•
We proposed and contributed to establishing a new task, fine-grained code line-level identification, aimed at enhancing developers’ efficiency when interacting with LLMs. This could be potentially useful to enable further research in this direction.
•
We systematically evaluated
PtTrust
’s performance across various software engineering tasks and found that it demonstrates strong cross-language and cross-task capabilities attributed to the proposed pre-training technique.
•
We further demonstrated that
PtTrust
provides interpretable features, enabling users to better understand and interpret LLMs’ internal states. This can
potentially facilitate many human-centered, interactive, and explainable techniques to enable various trustworthy assurance activities to build trust for code LLMs
The implementation (e.g., for LLM internal state extraction, analysis, model training, evaluation toolchain) and the labeled datasets contributed in this paper are available at:
https://github.com/YuhengHuang42/trust_codeLLM
2.
Related Work
2.1.
Internal State Analysis of LLMs
The rapid advancement of LLM technology has drawn increasing attention from researchers seeking to understand their underlying working mechanisms. Such studies are crucial in improving the performance, trustworthiness, and safety of these models. Notably, one branch of research draws parallels between LLMs and human brains, exploring the relationship between their behavioral characteristics and internal states of LLMs
(
Mischler et al., 2024
)
. Just as human brains exhibit identifiable patterns when making errors, recent findings indicate that similar patterns can be observed within LLMs. A pioneering work demonstrated that a simple classifier could be trained to uncover some relationships between a model’s truthfulness and internal neuron activations
(
Azaria and Mitchell, 2023
)
.
Based on these insights, subsequent research makes various exploratory attempts to investigate the connections between correctness
(
He et al., 2024
;
Marks and Tegmark, 2024
)
, safety
(
Song et al., 2024
;
Chen et al., 2024b
)
, privacy concerns
(
Wu et al., 2024
)
, toxicity
(
Liu et al., 2024c
)
, and their internal states. Among these studies, an important work by Zhou et al.
(
Zou et al., 2023
)
introduced an approach called representation engineering, which conducts analysis and intervenes in the activations of LLM internal neurons to detect and control their risky behaviors.
However, one particular drawback of existing approaches is that they rely on the high dimensionality of LLMs’ internal states, often involving thousands of neurons per token
(
Song et al., 2024
)
. From a performance perspective, this can lead to the curse of dimensionality
(
Clarkson, 1994
)
, severely impacting effectiveness. From a computation standpoint, it significantly increases significant complexity in both space and time, posing challenges for real-world deployment. Recently, sparse autoencoders (SAE)
(
Bricken et al., 2023
;
Huben et al., 2024
)
have emerged as a powerful solution to reduce dimensionality and extract interpretable features. OpenAI’s recent study
(
Gao et al., 2024
)
claims that they found clear scaling laws for training SAE, paving the way for scalable internal feature extraction.
In addition to approaches centered on neuron activations, another line of research focuses on analyzing the attention mechanism—a core component of LLMs’ transformer architecture
(
Vaswani, 2017
;
Su et al., 2024b
)
. Chuang
et al
.
introduced
LookBack Lens
(
Chuang et al., 2024
)
, a method designed to detect contextual hallucination in NLP tasks by examining the proportion of attention weights assigned to the input context compared to newly generated tokens. Most of the aforementioned studies primarily address trustworthiness issues in general LLMs applied to NLP tasks rather than identifying subtle errors made by code LLMs in multilingual and multi-task settings, which make our work different from these existing work.
2.2.
LLMs for Code-Related Tasks
While LLMs excel at handling a wide range of tasks in a zero-shot manner, code-related tasks, which heavily rely on advanced reasoning, problem-solving, and general coding understanding abilities, remain challenging for general-purpose models. To overcome these challenges, both industry
(
Roziere et al., 2023
;
Hui et al., 2024
;
Guo et al., 2024
;
Yu et al., 2024
;
Team et al., 2024
)
and academia
(
Li et al., 2023a
;
Lozhkov et al., 2024
;
Wei et al., 2024
)
are actively working to enhance LLMs’ coding capabilities. Related efforts include curating higher-quality code datasets for pre-training, introducing diverse training objectives such as Fill-in-the-Middle (FIM)
(
Fried et al., 2023
)
, and employing instruction fine-tuning to improve responses to code-related queries. These models serve as the foundation for current state-of-the-art code intelligent code assistants. Their capabilities can be further enhanced through advanced prompting techniques
(
Chen et al., 2023
;
Li et al., 2023b
;
Gao et al., 2023
;
Ding et al., 2024
;
Jiang et al., 2024a
;
Li et al., 2024b
)
, the integration of diverse programming tools
(
Wang et al., 2024a
)
, and access to external databases
(
Chen et al., 2024a
;
Su et al., 2024a
;
Liu et al., 2024a
;
Phan et al., 2024
)
, enabling them to tackle increasingly complex tasks. Such an approach, often referred to as code agents
(
Jimenez et al., 2024
)
, has gained significant interest in both the research community and the software industry in recent years. The rapid advancement of code LLMs has empowered them to tackle highly complex tasks, such as program analysis
(
Xie et al., 2024
)
.
Despite major breakthroughs, the current code LLMs still suffer from challenges, such as limited robustness
(
Arakelyan et al., 2023
)
, security
(
Pearce et al., 2022
)
, usability
(
Barke et al., 2023
)
, and correctness
(
Chen et al., 2021
;
Nguyen and Nadi, 2022
;
Jesse et al., 2023
)
. Researchers have tried to examine the shortcomings of code LLMs, constructing hierarchical taxonomies that encompass errors, coding style, and maintainability
(
Liu et al., 2023
;
Pan et al., 2024a
;
Liu et al., 2024b
)
. To delve deeper into the mechanisms underlying these errors, a recent study by Kou
et al
.
(
Kou et al., 2024
)
investigated the relationship between LLM errors and their internal attention states. The study revealed that misalignment between model attention and human attention increases the likelihood of errors. These studies indicate that the current code LLMs are still far from perfect, and there is an urgent need to address their trustworthiness issues.
3.
Method
Overall, the primary goal of
PtTrust
is to enable fine-grained identification of errors at the code line level. Specifically, given an incorrect generated response
A
A
by an LLM consisting of
n
n
lines, the framework should identify a subset
E
⊆
A
{E\subseteq A}
, representing the erroneous line set.
To achieve this goal, we first provide a high-level introduction to our method
PtTrust
, by explaining the workflow of our technique. Then, we explain the details of each stage in the method.
3.1.
Overview
Overall, three key procedures of
PtTrust
are summarized in Figure
1
. Stage
\footnotesize1⃝
starts with extracting the internal states of a given LLM (
\footnotesizeA⃝
) and training a sparse autoencoder (
\footnotesizeB⃝
) using these probed states. This stage aims to derive a general and universal low-dimension representation of the LLM’s hidden states, forming the basis for further analysis. This stage operates in a fully unsupervised manner, enabling it to scale effectively to large code corpora. In the software industry, companies often maintain extensive code repositories; this approach offers a cost-effective way to leverage existing software assets. Additionally, depending on the characteristics of the source code, the trained autoencoders can capture features unique to specific companies or even different departments.
After training the sparse autoencoders, we proceed to Stage
\footnotesize2⃝
. While the abstract representations learned in Stage
\footnotesize1⃝
contain rich information that can help identify risks in code lines, establishing a direct mapping between these representations and specific risks is challenging without external labels. To address this, Stage
\footnotesize2⃝
focuses on collecting fine-grained labels for the correctness of generated code lines. This label collection process can seamlessly integrate into the interaction between LLMs and developers, similar to how ChatGPT incorporates user feedback to improve its models. Developers simply need to highlight the code lines they identify as incorrect during manual review. In addition, as will be demonstrated in our experiments later, even a small number of fine-grained labels (e.g., approximately 100+ code snippets) can significantly outperform existing methods. Combining the representation of autoencoders and the corresponding labels, we can further train a downstream classifier to predict the risks of the generated code (
\footnotesizeC⃝
).
Figure 1
.
The Summarized Workflow of
PtTrust
.
Building on the target code LLM (
\footnotesizeA⃝
), the sparse autoencoders (
\footnotesizeB⃝
), and the downstream classifier (
\footnotesizeC⃝
), our framework,
PtTrust
, supports various risk assessment applications in Stage
\footnotesize3⃝
. As an example, we present a prototype for predicting risks at the code line level, though the framework is easily adaptable to other domains by modifying the labels collected in Stage
\footnotesize2⃝
. An additional benefit of
PtTrust
is that the introduced sparse autoencoders can improve the traceability and transparency of the entire system, offering rich internal information besides a single number. Prior research has shown that sparsity is strongly linked to explainability
(
Elhage et al., 2022
;
Bricken et al., 2023
;
Huben et al., 2024
)
, and we will also demonstrate this advantage in Section
4.4
. This enhanced interpretability can significantly increase user trust in a black-box AI system, which could be the key to their experience
(
Wang et al., 2023
)
.
Hereafter, we refer to Stage
\footnotesize1⃝
as the pre-training stage and Stage
\footnotesize2⃝
as the semantic-binding stage. In the following sections, we provide more detailed explanations of each stage.
3.2.
Pre-training Stage
The pre-training stage is designed to scale efficiently for large-scale code repositories. The first step in this stage is profiling. Specifically, given a text input, we pass it through the target LLM and extract its internal states for each token in the input. We select the early layers (e.g., the first quarter of all network layers) as the profiling target. Previous studies
(
Huben et al., 2024
;
He et al., 2024
;
Huang et al., 2024
)
have shown that early layers are often associated more with high-level decision-making processes, making them a suitable choice for our analysis. Notably, this process involves only a single forward pass without any generation. This is analogous to brain studies, where researchers observe and record brain activity as participants read given materials
(
Frank et al., 2005
;
Meyer et al., 2014
)
. Since the ultimate goal is to assess the risks associated with the LLM, it is essential for our “participant”—the LLM—to encounter incorrect inputs, such as buggy code. Fortunately, extracting commit histories from version control systems provides a straightforward way to collect mistakes and bugs made by developers
(
Muennighoff et al., 2023
)
. Additionally, we also propose the use of mutation techniques to deliberately generate incorrect code based on existing code snippets. Specifically, we introduce three types of mutators:
•
Switch Inside
: We randomly select and switch two code lines in a given snippet.
•
Switch Outside
: We randomly select two code snippets from the dataset and swap two lines within each snippet.
•
Delete Line
: We randomly delete one code line in a code snippet.
1
1
1
The contrastive learning phase requires forming a pair before and after the mutation. For line deletion, the pair consists of the original code line (correct) versus the line following the deleted line (incorrect). Such a setting also applies to the code line error labels in the evaluation stage.
These mutations are simpler to apply in cross-language tasks and have a more significant impact than traditional mutation testing methods, potentially leading to greater differences in neuron behavior. More fine-grained mutators, such as the universal mutator proposed by Deb et al.
(
Deb et al., 2024
)
, could also be applied. However, our preliminary experiments did not obtain significant improvements, possibly because the mutations were too fine-grained to have a substantial impact compared to line-level mutations under the scale of our study.
A more systematic investigation into mutation strategies is left for future work.
Given the profiled internal states of LLMs from the text corpus, the next step is to train an autoencoder to extract meaningful information efficiently. Before delving into the technical details, we would like to highlight the motivation behind this step. While it is feasible to directly use the raw internal states for risk assessment, this approach raises two key concerns: practicality and performance. From a practical standpoint, the high-dimensional internal neurons of LLMs are both computationally intensive to process and require substantial storage space to handle the data.
For example, Code Llama includes 8,192 neurons per layer. Generating a single response with 1,000 tokens results in 8,192,000 floating-point values that need to be analyzed. When scaled to multiple responses and users, running such services in real-time becomes prohibitively expensive. From a performance perspective, the large size of the internal states makes it challenging to handle efficiently with machine learning algorithms, especially when the number of labels (e.g., human feedback from Stage
\footnotesize2⃝
) is limited, which could easily lead to over-fitting
(
Hawkins, 2004
)
.
To address this challenge, we propose the use of autoencoders
(
Baldi, 2012
)
trained on the collected internal states. The autoencoders compress the high-dimensional states into a lower-dimensional latent representation (code), which serves as a more efficient and practical alternative to the original full-dimensional internal states. Their encoder-decoder architecture resembles an hourglass shape with output
s
^
\hat{s}
, and they are trained to recover the input states
s
s
given the loss function:
(1)
ℒ
plain
=
‖
s
−
s
^
‖
2
2
\mathcal{L}_{\text{plain}}=||s-\hat{s}||_{2}^{2}
In this work, we utilize a variant of autoencoders known as Sparse Autoencoders (SAE)
(
Ng et al., 2011
)
, which have gained significant traction in Explainable AI (XAI) research on LLMs
(
Huben et al., 2024
)
. Specifically, we employ TopK autoencoders, a model where OpenAI
(
Gao et al., 2024
)
has reported observing scaling laws
2
2
2
According to the scaling law, the latent dimension of SAE can sometimes exceed the input dimension when trained on large-scale data. However, despite this, the representation remains highly sparse—for instance, only a small subset (e.g., 32 latents) is activated at any given time. This sparsity ensures that the approach remains computationally efficient.
. The encoder is defined as:
(2)
z
=
TopK
​
(
W
enc
⋅
(
s
−
b
pre
)
+
b
enc
)
z=\text{TopK}(W_{\text{enc}}\cdot(s-b_{\text{pre}})+b_{\text{enc}})
where
W
enc
W_{\text{enc}}
is the encoder weight,
b
pre
b_{\text{pre}}
is the pre-encoder bias term
3
3
3
This bias is introduced because the SAE operates under dictionary learning context, where we seek to decompose the target activation into a combination of general features. The
b
pre
b_{\text{pre}}
is the bias in that decomposition process. Due to space constraints, we cannot provide all the details here and instead refer keen readers to
(
Bricken et al., 2023
)
,
b
enc
b_{\text{enc}}
is the encoder bias term, and
z
z
is the latent (code).
z
z
will be the main feature for the following stages of
PtTrust
. TopK is an activation function that retains only the k largest latent values, introducing sparsity by setting all other values to zero. The decoder is simply:
(3)
s
^
=
W
dec
⋅
z
+
b
pre
\hat{s}=W_{\text{dec}}\cdot z+b_{\text{pre}}
where
W
dec
W_{\text{dec}}
is the decoder weight.
The loss described in Eq.
2
encourages SAE to use the compressed latent representation
z
z
to capture the most salient features necessary for reconstructing the input. However, since our ultimate goal is to assess the risks associated with code LLMs, we aim to make the model more sensitive to error-related information. To achieve this, we incorporate contrastive learning
(
Chopra et al., 2005
;
Khosla et al., 2020
;
Zhang et al., 2024
;
Jiang et al., 2024b
)
, which encourages the model to distinguish between the representations of correct and incorrect code lines. Specifically, the contrastive loss is defined as:
(4)
ℒ
cont
​
(
x
i
,
x
j
,
θ
)
=
max
⁡
(
0
,
ϵ
−
‖
f
θ
​
(
x
i
)
−
f
θ
​
(
x
j
)
‖
2
)
2
\mathcal{L}_{\text{cont}}(x_{i},x_{j},\theta)=\max\left(0,\epsilon-||f_{\theta}(x_{i})-f_{\theta}(x_{j})||_{2}\right)^{2}
where
(
x
i
,
x
j
)
(x_{i},x_{j})
are contrastive pairs,
θ
\theta
is the parameter of the neural network, and
ϵ
\epsilon
defines the lower bound distance between contrastive pairs. In our study, these pairs are created in two ways: by using already-known correct and incorrect code lines or by comparing original code snippets with their mutated counterparts. So the final loss is
ℒ
plain
+
ℒ
cont
\mathcal{L}_{\text{plain}}+\mathcal{L}_{\text{cont}}
.
Finally, an important implementation detail is that, instead of training SAE on every token, we focus exclusively on the newline token (\n at the end of every code line). This decision significantly reduces training time and computational costs. For instance, in the pre-training stage, the total number of \n tokens is around 280,000, whereas the total number of all tokens is around 9,873,000, about 35 times larger. Moreover, previous studies
(
Marks and Tegmark, 2023
;
Jorgensen et al., 2023
;
Laurito et al., 2024
)
have highlighted the difficulty of distilling high-level features (e.g., correctness) from internal states, as these states are entangled with the next-token prediction process. By focusing on only the newline token (\n), we can alleviate this issue and mitigate the bias introduced by different tokens.
3.3.
Semantic Binding Stage
The final stage is semantic binding. While the previous stage produced low-dimension representations
z
z
of the code LLMs’ internal states for each code line, these representations are not yet linked to the specific risks inherent in the responses. This stage is designed to assign meaning to each vector through a learning process. This is why we refer to this stage as semantic binding: it establishes the connection between the abstract representations and their corresponding risks.
To begin with, we collect a set of coding questions for the target LLM and instruct it to generate responses (which involve hundreds to thousands of inferences). This process differs from Stage
\footnotesize1⃝
, where only a single inference was performed. In Stage
\footnotesize1⃝
, the LLM only
sees
what is correct or incorrect. However, in Stage
\footnotesize2⃝
, we instruct them to
act
and generate complete responses, and we collect its hidden states throughout the generation process, saving them at the line level. Then, for each generated answer
A
i
A_{i}
of question
i
i
, along with its corresponding hidden states
S
i
S_{i}
, we annotate the incorrect code lines
e
j
∈
E
i
e_{j}\in E_{i}
. We transform the hidden states
S
i
S_{i}
to
Z
i
Z_{i}
using the SAE trained in stage
\footnotesize1⃝
. This results in the formation of a dataset
(
A
,
Z
,
E
)
(A,Z,E)
where
A
A
is the answer set,
Z
Z
is the latents obtained from SAE, and
E
E
is the identified erroneous lines.
The next challenge is formulating the mapping
(
A
,
Z
)
→
E
(A,Z)\rightarrow E
as a machine learning problem. With the SAE parameters frozen, a straightforward approach would be to directly train another DNN for line-level error prediction. However, we found that in practical industrial scenarios, instead of giving verbose predictions of every single code line, it is more natural and intuitive to provide a list of rankings indicating the riskiest code lines to attract developers’ attention. By focusing on the most critical lines, this approach reduces cognitive load and makes the risk assessment interface more streamlined and user-friendly.
Building on this insight, we propose using learning-to-rank (LTR)
(
Liu et al., 2009
)
, a series of well-established techniques in recommender systems that have been widely adopted in industrial applications. Specifically, given a list of code lines
A
i
=
{
a
i
j
|
0
≤
j
<
n
}
A_{i}=\{a^{j}_{i}|0\leq j<n\}
, the goal is to compute a corresponding list of scores
{
r
j
|
0
≤
j
<
n
}
\{r_{j}|0\leq j<n\}
where each
r
j
∈
[
0
,
1
]
r_{j}\in[0,1]
represents the risk level associated with the
j
j
-th code line. A higher score means a more severe risk.
In particular, we employ
NeuralNDCG
loss
(
Pobrotyn and Białobrzeski, 2021
)
to train the network. This loss function integrates seamlessly into standard DNN training pipelines and serves as a differentiable approximation of sorting, enabling the network to learn to rank code lines effectively based on their risk levels. Due to space limitations, we omit the technical details of the loss function here. During training, we assign a score of 0 to correct code lines. For incorrect code lines, we rank them based on their length under the assumption that longer lines warrant greater attention.
4.
Result and Analysis
The first research question (RQ1) addresses the primary focus of this paper: the ability to identify errors at a fine-grained code line level. This ability enables risk assessment tools to highlight the most vulnerable lines of code, allowing users to focus their attention on quickly identifying and addressing potential issues. In contrast, the second research question (RQ2) examines a more traditional aspect: determining whether an entire code snippet is incorrect. While RQ1 is about the relative risk and prioritization of individual code lines, RQ2 addresses the overall correctness of a code segment. Finally, we assess the robustness and interpretability of the features learned by our method, which is essential for fostering user trust.
4.1.
Experiment Settings
4.1.1.
Dataset
Dataset selection is critical for evaluation. Due to company regulations, we cannot release internal datasets. Instead, we use open-source datasets that closely resemble real-world industrial scenarios to ensure the evaluation’s relevance and practicality.
For the pre-training stage
, we select three datasets comprising multilingual programming problems and their solutions. Notice that the data used in this stage can be replaced with code from internal software repositories within a software company. The first dataset is the LeetCode Dataset
(
Wang et al., 2024b
;
lee, 2025
)
, from which we extract approximately 2,358 coding problems across four programming languages. This dataset does not contain buggy code line information, so we apply mutation as described in Section
3.2
. The other two are HumanEvalPack (EvalPack for short)
(
Muennighoff et al., 2023
)
and DebugBench
(
Tian et al., 2024
)
. EvalPack dataset is derived from the original HumanEval
(
Chen et al., 2021
)
dataset, with manually introduced bugs added to each of the 164 HumanEval solutions. It spans six programming languages. DebugBench contains 4,253 instances in three programming languages. Each instance is accompanied by detailed annotations of bugs and their corresponding correct implementations. Therefore, we can leverage this labeling directly without performing mutations. These two datasets can be substituted with commit histories from software companies’ version control systems.
For the semantic binding stage
, we aim to replicate real-world scenarios where labels are scarce and highly valuable. Furthermore, to further evaluate
PtTrust
’s performance across languages, we intentionally limit this stage to include only Python code. As such, we choose HumanEval
(
Chen et al., 2021
)
for Python code generation, EvalPack
(
Muennighoff et al., 2023
)
and Quixbug
(
Lin et al., 2017
)
for Python code repair. In total, there are 368 instances, which is two orders of magnitude smaller than the dataset used in the pre-training stage.
For the evaluation stage
, we select three diverse tasks: code editing, code translation, and code repair. Code editing involves providing LLMs with original code along with new requirements and instructing them to make the corresponding modifications. Code translation requires converting a program from one programming language to another. Code repair focuses on fixing errors in a given code snippet. We select EditEval
(
Li et al., 2024a
)
, Code Lingua
(
Pan et al., 2024b
)
and Defects4j
(
Just et al., 2014
)
dataset for each of the task. Specifically, for Code Lingua, we select the Python-Java AVATAR subset, which contains abundant test cases (i.e., on average, 50 for each instance). For Defects4j, we follow the settings (e.g., prompts) in
(
Xia et al., 2023
)
and merge Defects4j-1.2 and Defects4j-2.0 into one to test LLMs’ single function repair ability.
The next challenge is to obtain fine-grained labels after code LLMs generate answers to the selected questions. For repair tasks (e.g., Defects4j), the modifications are relatively limited compared to the ground truth code, allowing us to use standard
diff
tools to automatically label the LLM-generated incorrect code. However, for HumanEval, EditEval and Code Lingua, there might be several correct alternatives that are syntactically different. Manually labeling all instances is highly time-consuming. To address this, we instruct GPT-4o to identify erroneous code lines. To validate GPT-4o’s accuracy in identifying these lines, we also ask it to provide repair solutions based on the identified errors. For those problems that GPT-4o fails to fix, the authors perform a manual review by sampling these cases. The sampling is conducted with a 90% confidence level and a margin of error of 20%. The overall statistics are shown in Table
1
. In general, we believe the label quality is reliable. Finally, we make manual adjustments in cases where the provided code lines do not align with the generated answers.
Model
HumanEval
Code Lingua
EditEval
LLM Error
GPT4o Error
GPT4o failed
LLM Error
GPT4o Error
GPT4o failed
LLM Error
GPT4o Error
GPT4o failed
Code Llama
44/164
17/44
2/9
136/250
60/136
2/14
80/194
11/80
1/7
StarCoder2
66/164
25/66
2/13
130/250
69/130
4/14
79/194
10/79
1/7
Qwen2.5-Coder
58/164
21/58
2/10
107/250
56/107
4/14
60/194
14/60
1/8
Table 1
.
Labeling statistics for three datasets.
LLM Error
means the total number of errors generated by the LLM during its responses.
GPT-4o Error
means the number of cases where GPT-4o’s attempted fixes failed to produce the correct code.
GPT-4o Failed
refers to the number of instances manually confirmed where GPT-4o failed to label the code line errors correctly.
4.1.2.
Model
When selecting code LLMs for evaluation, we prioritize open-source models with relatively strong capabilities to ensure they can generate reasonable answers for the given datasets. This avoids trivial results where all code lines would be labeled as errors due to poor model performance. Following this guidance, we select the following models: Code Llama-34B
(
Roziere et al., 2023
)
and Qwen2.5-Coder-32B
(
Hui et al., 2024
)
, which are representative of industrial-grade models, as well as StarCoder2-15B
(
Lozhkov et al., 2024
)
, which comes from the academic and open source community.
4.1.3.
Baseline
There has been little research focusing on fine-grained errors made by LLMs. Among the existing approaches:
•
Uncertainty
-based methods are the most straightforward
(
Huang et al., 2025
;
Spiess et al., 2025
)
, as they directly analyze the model’s output. One possible way is to aggregate confidence scores for all tokens within a code line. In this work, we use the
mean
as an indicator of its risk (
1
−
c
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
1-confidence
). We aggregate at the line level in RQ1 and the code snippet level in RQ2. Despite their simplicity, such methods can perform well in some cases because they do not rely on any training data, thus avoiding associated biases.
•
LookBack Lens
is a recent approach that detects in-context errors by analyzing the ratio of attention weights assigned to the context versus newly generated tokens. By adjusting the window size,
LookBack Lens
enables fine-grained error detection. In their original work, Logistic Regression was used for error detection. To provide a fair comparison and align model complexity with our approach, we also evaluate its performance using a Multilayer Perceptron (MLP)-based implementation.
•
Probing Classifier
(
Azaria and Mitchell, 2023
;
Liu et al., 2024c
)
refers to the approaches that directly train a classifier based on models’ internal states. We use a lightweight 4-layer Multilayer Perceptron (MLP) with a hidden size of 32. This architecture is shared for both
Probing Classifier
and
PtTrust
with only the difference in the input layer.
4.1.4.
Hardware
To conduct our large-scale experiments, we utilized a server with AMD 3955WX CPU, 256GB RAM, and four NVIDIA A4000 GPUs (16GB VRAM of each) and two servers each with AMD Pro 5955WX CPU, 256GB RAM, and two NVIDIA A6000 GPUs (48GB VRAM of each).
4.2.
RQ1: How effective is our method in identifying incorrect code lines?
Method
EditEval
Code Lingua
Defects4j
Top-1
Top-3
Top-5
Top-1
Top-3
Top-5
Top-1
Top-3
Top-5
LookBack Lens
-Logistic
0.100
0.347
0.587
0.051
0.142
0.252
0.109
0.262
0.395
LookBack Lens
-MLP
0.091
0.346
0.561
0.051
0.145
0.232
0.110
0.277
0.405
Probing Classifier
0.252
0.560
0.709
0.142
0.325
0.440
0.229
0.397
0.507
Uncertainty
0.256
0.557
0.722
0.040
0.152
0.268
0.262
0.499
0.603
Ours (
PtTrust
)
0.349
0.641
0.798
0.223
0.419
0.528
0.287
0.479
0.595
Table 2
.
Top-K Hit Rate
of Code Llama in code line error identification. Different colors are used to highlight the
best
and
second-best
Method
EditEval
Code Lingua
Defects4j
Top-1
Top-3
Top-5
Top-1
Top-3
Top-5
Top-1
Top-3
Top-5
LookBack Lens
-Logistic
0.136
0.405
0.585
0.074
0.192
0.256
0.122
0.301
0.426
LookBack Lens
-MLP
0.189
0.484
0.628
0.113
0.196
0.293
0.149
0.317
0.430
Probing Classifier
0.202
0.502
0.701
0.053
0.121
0.202
0.103
0.317
0.438
Uncertainty
0.239
0.514
0.682
0.034
0.149
0.258
0.192
0.361
0.486
Ours (
PtTrust
)
0.302
0.555
0.754
0.216
0.404
0.565
0.207
0.388
0.503
Table 3
.
Top-K Hit Rate
of StarCoder2 in code line error identification. Different colors are used to highlight the
best
and
second-best
Method
EditEval
Code Lingua
Defects4j
Top-1
Top-3
Top-5
Top-1
Top-3
Top-5
Top-1
Top-3
Top-5
LookBack Lens
-Logistic
0.122
0.346
0.594
0.014
0.092
0.162
0.129
0.350
0.453
LookBack Lens
-MLP
0.115
0.344
0.594
0.019
0.082
0.160
0.131
0.339
0.443
Probing Classifier
0.214
0.399
0.559
0.051
0.116
0.229
0.124
0.289
0.401
Uncertainty
0.257
0.558
0.717
0.031
0.154
0.245
0.254
0.474
0.588
Ours (
PtTrust
)
0.287
0.581
0.728
0.177
0.328
0.434
0.193
0.328
0.429
Table 4
.
Top-K Hit Rate
of Qwen2.5-Coder in code line error identification. Different colors are used to highlight the
best
and
second-best
The first RQ highlights the primary focus of this work: fine-grained code line error detection. To evaluate each method, we use the metric
Top-K Hit Rate
. Specifically, each method assigns a score to each code line in a given problem. From these scores, we select the Top-K lines with the highest scores and calculate the proportion of buggy tokens within these lines relative to the total number of buggy tokens. We evaluate Code Llama, StarCoder2, and Qwen2.5-Coder on EditEval, Code Lingua, and Defects4j datasets. The results of Top-1, Top-3 and Top-5 Hit Rate are shown in Table
2
-
4
.
We can observe that
PtTrust
achieves state-of-the-art performance across all three code LLMs. Specifically,
PtTrust
attains the highest Top-K scores for all tasks on StarCoder2 and for all tasks except Defects4j on Code Llama and Qwen2.5-Coder. For Defects4j, the
Uncertainty
method performs surprisingly well. This performance gap might be attributed to the very limited amount of training data related to repair tasks during the semantic binding stage. For instance, Qwen2.5-Coder made only 58 errors in the EvalPack dataset and two errors in the QuixBug dataset. This restricts the number of error-related training instances to only 60 in total. Additionally, these training data are exclusively in Python, whereas test set Defects4j is in Java, posing a significant challenge for learning-based methods to generalize effectively. A slightly larger and more comprehensive data could potentially improve the performance of
PtTrust
and other training-based methods.
However,
PtTrust
remains competitive on this task. In contrast, for Code Lingua tasks,
PtTrust
significantly outperforms other methods. For instance, on Code Llama,
PtTrust
identifies 5.5 times as many buggy code lines as the
Uncertainty
method on the Top-1 metric and 5.7 times on Qwen2.5-Coder.
On the other hand,
LookBack Lens
appears to struggle to produce good results. First of all,
LookBack Lens
is originally designed for NLP tasks, which may limit its effectiveness in handling code-related tasks. Adapting it to better suit the unique characteristics of code tasks might be necessary. Another possible reason is the significant differences in LLMs’ attention patterns between the training data used in the semantic binding stage and the data used during evaluation, making it difficult for downstream models to generalize effectively. Especially considering we are evaluating the methods under cross-task and cross-lingual settings. While the
Probing Classifier
performs better than
LookBack Lens
, it still falls short of the out-of-the-box
Uncertainty
method. These findings support our hypothesis that in the era of LLMs, training classifiers for error prediction requires caution. The operational range of LLMs can far exceed the scope of the limited training data, leading to challenges in achieving reliable generalization.
Finding 1
:

Stakeholders should exercise caution when applying learning-based risk classifiers, especially in scenarios where there is a potential data distribution shift between training and testing, which could often be the case for general-purpose code LLMs. However, thanks to the pre-training stage,
PtTrust
achieves SOTA performance while maintaining robustness across tasks and programming languages.
4.3.
RQ2: How effective is our method in identifying incorrect code snippets?
While predicting the correctness of an entire code snippet is not the primary focus of this study, it provides a useful perspective for evaluating the quality of the learned features. Following the settings of previous studies
(
Azaria and Mitchell, 2023
;
Zou et al., 2023
)
, we use the hidden state of the final token as the feature to train a simple classifier. We exclude
LookBack Lens
from this RQ since it is not designed for such tasks. Our preliminary results for
LookBack Lens
on EditEval and Code Lingua also reveal that it trivially predicts zero for all test instances, regardless of whether the feature is derived from the final token or the entire generated code snippet. For the
Uncertainty
method, we continue to use mean aggregation but at the code snippet level. A key design choice is the selection of the threshold for determining whether a line is classified as erroneous. To optimize this threshold, we use Youden’s J statistic
(
Fluss et al., 2005
)
, which balances sensitivity and specificity. The cutoff is determined using the training dataset from the semantic binding stage (i.e., HumanEval, EvalPack, and Quixbug).
The results measured in code-snippet level error detection accuracy are shown in Table
5
. In general,
PtTrust
continues to deliver the best performance, achieving state-of-the-art results in 7 out of 9 cases. A slightly different observation this time is that the
Uncertainty
method performs the worst. This aligns with findings from previous studies
(
Huang et al., 2025
;
Spiess et al., 2025
)
indicating that LLMs are generally poorly calibrated in their out-of-the-box state. While uncertainty scores can effectively highlight relative risks between different code lines, they may struggle with snippet-level correctness due to the excessive noise introduced in the process. For example, not all tokens within a snippet contribute equally to the overall correctness, which makes aggregation methods less reliable in such scenarios.
Method
EditEval
Code Lingua
Defects4j
Code Llama
StarCoder2
Qwen2.5-Coder
Code Llama
StarCoder2
Qwen2.5-Coder
Code Llama
StarCoder2
Qwen2.5-Coder
Probing Classifier
0.516
0.606
0.601
0.569
0.571
0.577
0.437
0.667
0.154
Uncertainty
0.552
0.565
0.586
0.621
0.563
0.617
0.499
0.346
0.309
Ours (
PtTrust
)
0.593
0.622
0.627
0.508
0.595
0.548
0.515
0.845
0.355
Table 5
.
Classification Performance for three datasets with three code LLMs.
Finding 2
:
PtTrust
achieves SOTA performance in entire code snippet error prediction across all baselines. Unlike the results in RQ1, where the
Uncertainty
method showed competitive performance, it struggles with this task.
4.4.
RQ3: Can our method learn robust and interpretable features?
In addition to evaluating downstream model performance quantitatively, this section explores
PtTrust
’s effectiveness by analyzing the learned features (latent representations of SAE) from two perspectives: whether the learned features can convey robust representations across programming languages and whether these features are interpretable.
4.4.1.
Cross-language ability
A key concern with internal-state-based methods is that, theoretically, the internal neurons of LLMs primarily encode information related to next-token prediction, which is their training objective. This makes it highly challenging to extract insights into the model’s beliefs, decisions, or other high-level reasoning. Next-token prediction typically emphasizes syntactic features at the time of inference. For instance, experiments by Bricken
et al
.
(
Bricken et al., 2023
)
demonstrate that the activated latent representations can effectively distinguish Arabic script from base64 strings.
Code Llama
StarCoder2
Qwen2.5-Coder
Figure 2
.
Distribution difference across tasks for three LLMs. The lower triangle represents the distance between each language pair in the LeetCode dataset, while the upper triangle shows the corresponding distances within the EvalPack dataset. The diagonal entries indicate the cross-task distance (LeetCode v.s. EvalPack) for the same language.
To evaluate whether the SAE in
PtTrust
can learn robust representations for risk assessment, we analyze the activation distribution differences across tasks and programming languages. For this purpose, we use the LeetCode and EvalPack datasets during the pre-training stage, as they provide balanced instances for various programming languages. We perform inference with all three models and collect latent representations for three widely-used programming languages: Python, C++, and Java.
For each (language, dataset) pair, we calculate the mean activation across instances and measure the distribution differences using the Wasserstein distance, where higher values indicate greater dissimilarity between distributions. We first compute the distance between programming languages within each dataset and then calculate the distance across datasets for the same programming language. The resulting distance matrix is illustrated in Figure
2
. We can observe a really intriguing phenomenon: the cross-task distance for the same language (diagonal entries) is generally larger than the in-task distance between different languages (low triangle and upper triangle). The only exception to this pattern is the Python v.s. Java pair for the Code Llama model on the EvalPack dataset. Upon closer examination, we find that this anomaly may arise because, in the EvalPack dataset, only Java code begins with “class solution”, whereas other programming languages use function-based answers. Code Llama appears to be sensitive to such structural differences, leading to greater internal state variations for this specific case. Overall, these results suggest that the latent representations learned by the SAE can, to some extent, capture high-level task-related information.
4.4.2.
Feature Interpretability
Figure 3
.
Activation difference between buggy and correct code lines on Code Llama. Latent 121 is highlighted.
Figure 4
.
Activation difference between buggy and correct code lines on StarCoder2. Latent 44 is highlighted.
Figure 5
.
Activation difference between buggy and correct code lines on Qwen2.5-Coder. Latent 63 is highlighted.
While
PtTrust
allows replacing SAE with a more powerful autoencoder for potentially more accurate risk assessment, we select SAE because it offers a unique advantage: improved interpretability. Enabling users to observe and interact with a complex AI system fosters greater trust compared to providing a single risk score. This enhanced transparency can lead to significant advantages in real-world interactions between code LLMs and developers.
The interpretability of SAE comes from its ability to extract monosemantic features. The neurons of general DNNs have a phenomenon known as Superposition
(
Elhage et al., 2022
)
, where models tend to represent more features than the neurons they have, and this leads to polysemanticity – each neuron can convey different information under different contexts. This is good for performance but bad for interpretability. In contrast, SAE is found to be able to identify monosemantic features
(
Bricken et al., 2023
)
and can better align with human understanding. Next, we present a simple showcase of this feature.
Given all the datasets in the semantic binding stage and evaluation stage (i.e., HumanEval, QuixBugs, Evalpack, Code Lingua, EditEval, and Defects4j), we select those that LLMs’ answers that are incorrect. Within these samples, we calculate the average latent activation of the SAE for both incorrect and correct code lines, then subtract the latter from the former. Positive values in the resulting activation map highlight latents that are more activated in incorrect code lines compared to correct ones. We further average this activation map at the dataset level and visualize the results in Figure
3
-
5
.
Surprisingly, we observe obvious cross-task latents across all studied code LLMs that represent erroneous code lines. It is important to note that these datasets encompass a wide range of tasks, including code editing, generation, translation, and repair, across both Python and Java programming languages. This finding may explain why
PtTrust
demonstrates robust performance in risk assessment across diverse tasks. This behavior closely resembles Error-Related Negativity (ERN)
(
Frank et al., 2005
)
observed in human brains, where neurons exhibit clear signals when recognizing errors.
Finding 3
:

The SAE component in
PtTrust
demonstrates robust representations that are consistent across both languages and tasks. Additionally, we identify intuitive features strongly associated with code LLMs’ errors. This level of interpretability positions
PtTrust
as a promising step toward establishing a systematic and trustworthy framework for code LLMs.
5.
Discussion
5.1.
Lesson Learned
Disentangle Representation and Computation.
Risk assessment for LLMs can be pretty challenging since they are trained on large-scale data. These data are usually inaccessible. Even when accessible, directly linking these data to the risk of LLMs is difficult because LLMs are optimized for next-token prediction, a paradigm significantly different from that of classical DNNs explicitly trained for specific functionalities.
The way we address this challenge is to disentangle representation from computation. Specifically, we train a feature extractor, the Sparse Autoencoder (SAE), in an unsupervised pre-training manner to capture the internal representations of the models’ states. Following this, we establish a mapping between the internal states and the correctness of the outputs through a supervised semantic binding process. This two-stage approach proves highly effective, especially when pre-training data are abundant but labeled data for downstream tasks are scarce.
The Critical Role of Data Management.
In the initial phase of our project, we concentrated primarily on developing pipeline prototypes, dedicating significant time to state extraction and SAE training. However, once we successfully executed a basic “hello world” example, the complexity of data management became apparent, eventually consuming the majority of our efforts. The challenge lay in handling various dataset versions across multiple tasks and programming languages, each with distinct pre- and post-processing requirements.
Despite these challenges, we discovered that enhancing data quality through methods such as adding datasets and refining the annotation/processing strategies proved more beneficial than merely optimizing training algorithms or adopting new architectures. This is particularly relevant in the era of LLMs, where data pipelines are more dynamic compared to the pre-LLM era, largely due to LLMs’ multitasking capabilities. Consequently, we advocate for increased focus on the design and management of data pipelines among related stakeholders.
5.2.
Future Direction
Vast space yet to be explored.
In this study, we focus on probing a specific early layer of LLMs, as prior research suggests that these layers exhibit a stronger correlation with high-level decisions made by the models
(
Zou et al., 2023
;
He et al., 2024
;
Huang et al., 2024
)
. However, many other layers remain untested and unexplored. Different layers might respond uniquely to different features—for instance, some may be more aligned with code performance, while others could be tied to code security. Furthermore,
PtTrust
is not limited to analyzing hidden layers; it can also be extended to directly analyze attention layers, offering additional insights into the model’s internal mechanisms. Future work could take several directions. One approach is to determine, for a specific task (e.g., code line error detection), which layer contributes most effectively to final accuracy and how to identify it automatically. Another is to deepen our understanding of the roles played by individual layers, providing valuable guidance for subsequent research and practical applications.
More trustworthiness properties.
In this work, we focus on applying
PtTrust
to code line errors and code snippet errors. However, the semantic binding stage of
PtTrust
is not explicitly restricted to specific types of labels, which means it could, in theory, be extended to address other properties, such as the security and performance of generated code, as long as the internal states contain relevant information. Extending
PtTrust
to these applications would be an intriguing avenue for future research. Along the way, two key components could be further enhanced to support such different scenarios: (1) Refine the methods for extracting hidden states that contain richer and more task-relevant information, such as by enhancing the plain and contrastive loss functions at the pre-training stage. (2) Develop more effective ways to align the desired semantic properties with the learned representations, ensuring that the model captures the target characteristics more accurately at the semantic binding stage.
Evaluation of the learned representation quality.
PtTrust
relies on the learned latent representations from the pre-training stage to achieve cross-language and cross-task effectiveness. However, before evaluating the entire framework on downstream tasks, it is challenging to directly assess the quality of the internal states. Currently, this quality can only be evaluated indirectly through downstream performance or manual feature analysis, as demonstrated in Section
4.4
. A promising direction for future work is to develop methods for assessing the quality of latent representations without relying on external labels. Such evaluation techniques could significantly accelerate the iterative improvement of the first-stage pre-training method, facilitate SAE comparisons, and further enhance the overall effectiveness of
PtTrust
.
6.
Threats to Validity
Internal and Construct Validity.
One primary concern is the process of obtaining fine-grained line-level error labels, which are critical for both the semantic binding and evaluation stages. This process could potentially threaten internal and construct validity, as the GPT-4o models used at this stage may introduce errors and uncertainty.
To address this issue, we take a two-step approach. First, we instruct GPT-4o to correct the identified error lines in the given code and run automatic testing based on the provided test cases of each dataset. For cases where GPT-4o fails to give a correct answer, we conduct sampling and manual review to verify and correct the labels. In future work, we could enhance this process by directly utilizing fully human-labeled data collected from feedback platforms, further improving the reliability of the labels.
External Validity.
The external validity of this study relates to the generalizability of our findings across different LLMs and tasks. To address this concern, we evaluate
PtTrust
using three advanced LLMs from both industry and academia. Additionally, we include a diverse range of tasks—such as code editing, code translation, and code repair—across two programming languages in evaluation. Future work could consider incorporating a wider variety of code LLMs and expanding the range of tasks covered in the evaluation.
7.
Conclusion
In this paper, we propose a pre-training framework
PtTrust
for code LLMs that is, by its design, able to scale to vast amounts of training data. We outline a workflow for constructing
PtTrust
, which can be seamlessly integrated into the existing infrastructure of software companies. Through systematic evaluation, we demonstrate the promising performance of
PtTrust
, even with a very limited number of data available at the semantic binding stage. Our experiments show that the representations learned during the pre-training stage enable
PtTrust
to generalize effectively to diverse software engineering tasks across different programming languages that the downstream classifier has never encountered during training. Additionally,
PtTrust
provides intuitive and interpretable features, allowing users to better understand the potential risks in the answers generated by LLMs. Building on these findings, we call for related stakeholders to push the pre-training-based LLMs’ risk assessment forward, paving the way for more robust and trustworthy LLM-driven systems.
Acknowledgements.
This work was supported by Fujitsu Limited.
References
lee (2025)
2025.
Leetcode Dataset.
https://huggingface.co/datasets/greengerong/leetcode
Accessed: 2025-01-13.
Arakelyan et al
.
(2023)
Shushan Arakelyan, Rocktim Das, Yi Mao, and Xiang Ren. 2023.
Exploring distributional shifts in large language models for code analysis. In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
. 16298–16314.
Azaria and Mitchell (2023)
Amos Azaria and Tom Mitchell. 2023.
The Internal State of an LLM Knows When It’s Lying. In
The 2023 Conference on Empirical Methods in Natural Language Processing
.
https://openreview.net/forum?id=y2V6YgLaW7
Baldi (2012)
Pierre Baldi. 2012.
Autoencoders, unsupervised learning, and deep architectures. In
Proceedings of ICML workshop on unsupervised and transfer learning
. JMLR Workshop and Conference Proceedings, 37–49.
Barke et al
.
(2023)
Shraddha Barke, Michael B James, and Nadia Polikarpova. 2023.
Grounded copilot: How programmers interact with code-generating models.
Proceedings of the ACM on Programming Languages
7, OOPSLA1 (2023), 85–111.
Bricken et al
.
(2023)
Travis Bricken, Alex Templeton, Joshua Batson, Benjamin Chen, Alan Jermyn, et al
.
2023.
Towards Monosemanticity: Decomposing Language Models with Dictionary Learning.
Transformer Circuits Thread
(2023).
Chen et al
.
(2023)
Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. 2023.
CodeT: Code Generation with Generated Tests. In
The Eleventh International Conference on Learning Representations
.
Chen et al
.
(2024a)
Junkai Chen, Xing Hu, Zhenhao Li, Cuiyun Gao, Xin Xia, and David Lo. 2024a.
Code search is all you need? improving code suggestions with code search. In
Proceedings of the IEEE/ACM 46th International Conference on Software Engineering
. 1–13.
Chen et al
.
(2024b)
Jianhui Chen, Xiaozhi Wang, Zijun Yao, Yushi Bai, Lei Hou, and Juanzi Li. 2024b.
Finding Safety Neurons in Large Language Models.
arXiv preprint arXiv:2406.14144
(2024).
Chen et al
.
(2021)
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, et al
.
2021.
Evaluating large language models trained on code.
arXiv preprint arXiv:2107.03374
(2021).
Chopra et al
.
(2005)
Sumit Chopra, Raia Hadsell, and Yann LeCun. 2005.
Learning a similarity metric discriminatively, with application to face verification. In
2005 IEEE computer society conference on computer vision and pattern recognition (CVPR’05)
, Vol. 1. IEEE, 539–546.
Chuang et al
.
(2024)
Yung-Sung Chuang, Linlu Qiu, Cheng-Yu Hsieh, Ranjay Krishna, Yoon Kim, and James R. Glass. 2024.
Lookback Lens: Detecting and Mitigating Contextual Hallucinations in Large Language Models Using Only Attention Maps. In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
, Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguistics, Miami, Florida, USA, 1419–1436.
https://doi.org/10.18653/v1/2024.emnlp-main.84
Clarkson (1994)
Kenneth L Clarkson. 1994.
An algorithm for approximate closest-point queries. In
Proceedings of the tenth annual symposium on Computational geometry
. 160–164.
Deb et al
.
(2024)
Sourav Deb, Kush Jain, Rijnard Van Tonder, Claire Le Goues, and Alex Groce. 2024.
Syntax Is All You Need: A Universal-Language Approach to Mutant Generation.
Proceedings of the ACM on Software Engineering (FSE 2024)
(2024).
Ding et al
.
(2024)
Yangruibo Ding, Marcus J Min, Gail Kaiser, and Baishakhi Ray. 2024.
CYCLE: Learning to Self-Refine the Code Generation.
Proceedings of the ACM on Programming Languages
8, OOPSLA1 (2024), 392–418.
Elhage et al
.
(2022)
Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain, Carol Chen, et al
.
2022.
Toy models of superposition.
arXiv preprint arXiv:2209.10652
(2022).
Fluss et al
.
(2005)
Ronen Fluss, David Faraggi, and Benjamin Reiser. 2005.
Estimation of the Youden Index and its associated cutoff point.
Biometrical Journal: Journal of Mathematical Methods in Biosciences
47, 4 (2005), 458–472.
Frank et al
.
(2005)
Michael J Frank, Brion S Woroch, and Tim Curran. 2005.
Error-related negativity predicts reinforcement learning and conflict biases.
Neuron
47, 4 (2005), 495–501.
Fried et al
.
(2023)
Daniel Fried, Armen Aghajanyan, Jessy Lin, Sida Wang, Eric Wallace, Freda Shi, Ruiqi Zhong, Scott Yih, Luke Zettlemoyer, and Mike Lewis. 2023.
InCoder: A Generative Model for Code Infilling and Synthesis. In
The Eleventh International Conference on Learning Representations
.
https://openreview.net/forum?id=hQwb-lbM6EL
Fujitsu Limited (2024a)
Fujitsu Limited. 2024a.
Fujitsu launches “Takane” - A large language model for enterprises offering the highest Japanese language proficiency in the world.
https://www.fujitsu.com/global/about/resources/news/press-releases/2024/0930-01.html
Accessed: 2025-01-15.
Fujitsu Limited (2024b)
Fujitsu Limited. 2024b.
Fujitsu to provide the world’s first enterprise-wide generative AI framework technology to meet changing needs of companies.
https://www.fujitsu.com/global/about/resources/news/press-releases/2024/0604-01.html
Accessed: 2025-01-15.
Gao et al
.
(2024)
Leo Gao, Tom Dupré la Tour, Henk Tillman, Gabriel Goh, Rajan Troll, Alec Radford, Ilya Sutskever, Jan Leike, and Jeffrey Wu. 2024.
Scaling and evaluating sparse autoencoders.
arXiv preprint arXiv:2406.04093
(2024).
Gao et al
.
(2023)
Shuzheng Gao, Xin-Cheng Wen, Cuiyun Gao, Wenxuan Wang, Hongyu Zhang, and Michael R Lyu. 2023.
What makes good in-context demonstrations for code intelligence tasks with llms?. In
2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)
. IEEE, 761–773.
Guo et al
.
(2024)
Daya Guo, Qihao Zhu, et al
.
2024.
DeepSeek-Coder: When the Large Language Model Meets Programming–The Rise of Code Intelligence.
arXiv preprint arXiv:2401.14196
(2024).
Hawkins (2004)
Douglas M Hawkins. 2004.
The problem of overfitting.
Journal of chemical information and computer sciences
44, 1 (2004), 1–12.
He et al
.
(2024)
Jinwen He, Yujia Gong, Zijin Lin, Yue Zhao, Kai Chen, et al
.
2024.
Llm factoscope: Uncovering llms’ factual discernment through measuring inner states. In
Findings of the Association for Computational Linguistics ACL 2024
. 10218–10230.
Hou et al
.
(2024)
Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li, Xiapu Luo, David Lo, John Grundy, and Haoyu Wang. 2024.
Large language models for software engineering: A systematic literature review.
ACM Transactions on Software Engineering and Methodology
33, 8 (2024), 1–79.
Huang et al
.
(2024)
Yuheng Huang, Jiayang Song, Qiang Hu, Felix Juefei-Xu, and Lei Ma. 2024.
Active Testing of Large Language Model via Multi-Stage Sampling.
arXiv preprint arXiv:2408.03573
(2024).
Huang et al
.
(2025)
Yuheng Huang, Jiayang Song, Zhijie Wang, Shengming Zhao, Huaming Chen, Felix Juefei-Xu, and Lei Ma. 2025.
Look before you leap: An exploratory study of uncertainty measurement for large language models.
IEEE Transactions on Software Engineering (TSE)
(2025).
Huben et al
.
(2024)
Robert Huben, Hoagy Cunningham, Logan Riggs Smith, Aidan Ewart, and Lee Sharkey. 2024.
Sparse Autoencoders Find Highly Interpretable Features in Language Models. In
The Twelfth International Conference on Learning Representations
.
https://openreview.net/forum?id=F76bwRSLeK
Hui et al
.
(2024)
Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, et al
.
2024.
Qwen2. 5-coder technical report.
arXiv preprint arXiv:2409.12186
(2024).
Inbal Shani (2025)
Inbal Shani. 2025.
Survey reveals AI’s impact on the developer experience.
https://github.blog/news-insights/research/survey-reveals-ais-impact-on-the-developer-experience/
.
Accessed: 2025-01-14.
Jesse et al
.
(2023)
Kevin Jesse, Toufique Ahmed, Premkumar T Devanbu, and Emily Morgan. 2023.
Large language models and simple, stupid bugs. In
IEEE/ACM 20th International Conference on Mining Software Repositories (MSR)
. 563–575.
Jiang et al
.
(2024b)
Nan Jiang, Chengxiao Wang, Kevin Liu, Xiangzhe Xu, Lin Tan, Xiangyu Zhang, and Petr Babkin. 2024b.
Nova: Generative Language Models for Assembly Code with Hierarchical Attention and Contrastive Learning.
arXiv:2311.13721 [cs.SE]
https://arxiv.org/abs/2311.13721
Jiang et al
.
(2024a)
Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang, Qiwei Shang, Ge Li, Zhi Jin, and Wenpin Jiao. 2024a.
Self-planning code generation with large language models.
ACM Transactions on Software Engineering and Methodology
33, 7 (2024), 1–30.
Jimenez et al
.
(2024)
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. 2024.
SWE-bench: Can Language Models Resolve Real-world Github Issues?. In
The Twelfth International Conference on Learning Representations
.
https://openreview.net/forum?id=VTF8yNQM66
Jorgensen et al
.
(2023)
Ole Jorgensen, Dylan Cope, Nandi Schoots, and Murray Shanahan. 2023.
Improving activation steering in language models with mean-centring.
arXiv preprint arXiv:2312.03813
(2023).
Just et al
.
(2014)
René Just, Darioush Jalali, and Michael D Ernst. 2014.
Defects4J: A database of existing faults to enable controlled testing studies for Java programs. In
Proceedings of the 2014 international symposium on software testing and analysis
. 437–440.
Khosla et al
.
(2020)
Prannay Khosla, Piotr Teterwak, et al
.
2020.
Supervised contrastive learning.
Advances in neural information processing systems
33 (2020), 18661–18673.
Kou et al
.
(2024)
Bonan Kou, Shengmai Chen, Zhijie Wang, Lei Ma, and Tianyi Zhang. 2024.
Do large language models pay similar attention like human programmers when generating code?
Proceedings of the ACM on Software Engineering
1, FSE (2024), 2261–2284.
Laurito et al
.
(2024)
Walter Laurito, Sharan Maiya, Grégoire Dhimoïla, Owen Ho Wan Yeung, and Kaarel Hänni. 2024.
Cluster-Norm for Unsupervised Probing of Knowledge. In
Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing
, Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguistics, Miami, Florida, USA, 14083–14112.
https://doi.org/10.18653/v1/2024.emnlp-main.780
Li et al
.
(2023b)
Jia Li et al
.
2023b.
Skcoder: A sketch-based approach for automatic code generation. In
2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)
. IEEE, 2124–2135.
Li et al
.
(2024b)
Jia Li, Yunfei Zhao, Yongmin Li, Ge Li, and Zhi Jin. 2024b.
Acecoder: An effective prompting technique specialized in code generation.
ACM Transactions on Software Engineering and Methodology
33, 8 (2024), 1–26.
Li et al
.
(2024a)
Kaixin Li, Qisheng Hu, James Zhao, Hui Chen, Yuxi Xie, Tiedong Liu, Michael Shieh, and Junxian He. 2024a.
Instructcoder: Instruction tuning large language models for code editing. In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop)
. 50–70.
Li et al
.
(2023a)
Raymond Li, Loubna Ben Allal, Yangtian Zi, et al
.
2023a.
StarCoder: may the source be with you!
Transactions on Machine Learning Research
(2023).
https://openreview.net/forum?id=KoFOg41haE
Reproducibility Certification.
Lin et al
.
(2017)
Derrick Lin, James Koppel, Angela Chen, and Armando Solar-Lezama. 2017.
QuixBugs: A multi-lingual program repair benchmark set based on the Quixey Challenge. In
Proceedings Companion of the 2017 ACM SIGPLAN international conference on systems, programming, languages, and applications: software for humanity
. 55–56.
Liu et al
.
(2009)
Tie-Yan Liu et al
.
2009.
Learning to rank for information retrieval.
Foundations and Trends® in Information Retrieval
3, 3 (2009), 225–331.
Liu et al
.
(2024a)
Xiangyan Liu, Bo Lan, Zhiyuan Hu, et al
.
2024a.
Codexgraph: Bridging large language models and code repositories via code graph databases.
arXiv preprint arXiv:2408.03910
(2024).
Liu et al
.
(2023)
Yue Liu, Thanh Le-Cong, et al
.
2023.
Refining ChatGPT-Generated Code: Characterizing and Mitigating Code Quality Issues.
ACM Transactions on Software Engineering and Methodology
(2023).
Liu et al
.
(2024c)
Yi Liu, Junzhe Yu, Huijia Sun, Ling Shi, Gelei Deng, Yuqi Chen, and Yang Liu. 2024c.
Efficient Detection of Toxic Prompts in Large Language Models. In
Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering
. 455–467.
Liu et al
.
(2024b)
Zhijie Liu, Yutian Tang, Xiapu Luo, Yuming Zhou, and Liang Feng Zhang. 2024b.
No need to lift a finger anymore? Assessing the quality of code generation by ChatGPT.
IEEE Transactions on Software Engineering
(2024).
Lozhkov et al
.
(2024)
Anton Lozhkov, Raymond Li, Loubna Ben Allal, et al
.
2024.
Starcoder 2 and the stack v2: The next generation.
arXiv preprint arXiv:2402.19173
(2024).
Marks and Tegmark (2023)
Samuel Marks and Max Tegmark. 2023.
The geometry of truth: Emergent linear structure in large language model representations of true/false datasets.
arXiv preprint arXiv:2310.06824
(2023).
Marks and Tegmark (2024)
Samuel Marks and Max Tegmark. 2024.
The Geometry of Truth: Emergent Linear Structure in Large Language Model Representations of True/False Datasets. In
First Conference on Language Modeling
.
https://openreview.net/forum?id=aajyHYjjsk
Meyer et al
.
(2014)
Alexandria Meyer, Jennifer N Bress, and Greg Hajcak Proudfit. 2014.
Psychometric properties of the error-related negativity in children and adolescents.
Psychophysiology
51, 7 (2014), 602–610.
Mischler et al
.
(2024)
Gavin Mischler, Yinghao Aaron Li, Stephan Bickel, Ashesh D Mehta, and Nima Mesgarani. 2024.
Contextual feature extraction hierarchies converge in large language models and the brain.
Nature Machine Intelligence
(2024), 1–11.
Muennighoff et al
.
(2023)
Niklas Muennighoff, Qian Liu, Armel Zebaze, Qinkai Zheng, Binyuan Hui, Terry Yue Zhuo, Swayam Singh, Xiangru Tang, Leandro Von Werra, and Shayne Longpre. 2023.
Octopack: Instruction tuning code large language models.
arXiv preprint arXiv:2308.07124
(2023).
Ng et al
.
(2011)
Andrew Ng et al
.
2011.
Sparse autoencoder.
CS294A Lecture notes
72, 2011 (2011), 1–19.
Nguyen and Nadi (2022)
Nhan Nguyen and Sarah Nadi. 2022.
An empirical evaluation of GitHub copilot’s code suggestions. In
Proceedings of the 19th International Conference on Mining Software Repositories
. 1–5.
Pan et al
.
(2024a)
Rangeet Pan, Ali Reza Ibrahimzada, et al
.
2024a.
Lost in translation: A study of bugs introduced by large language models while translating code. In
Proceedings of the IEEE/ACM 46th International Conference on Software Engineering
. 1–13.
Pan et al
.
(2024b)
Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lambert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh Sinha, and Reyhaneh Jabbarvand. 2024b.
Lost in translation: A study of bugs introduced by large language models while translating code. In
Proceedings of the IEEE/ACM 46th International Conference on Software Engineering
. 1–13.
Pearce et al
.
(2022)
Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. 2022.
Asleep at the keyboard? assessing the security of github copilot’s code contributions. In
IEEE Symposium on Security and Privacy
. 754–768.
Phan et al
.
(2024)
Huy N Phan, Hoang N Phan, Tien N Nguyen, and Nghi DQ Bui. 2024.
Repohyper: Better context retrieval is all you need for repository-level code completion.
arXiv preprint arXiv:2403.06095
(2024).
Pobrotyn and Białobrzeski (2021)
Przemysław Pobrotyn and Radosław Białobrzeski. 2021.
Neuralndcg: Direct optimisation of a ranking metric via differentiable relaxation of sorting.
arXiv preprint arXiv:2102.07831
(2021).
Roziere et al
.
(2023)
Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, et al
.
2023.
Code llama: Open foundation models for code.
arXiv preprint arXiv:2308.12950
(2023).
Song et al
.
(2024)
Da Song, Xuan Xie, Jiayang Song, Derui Zhu, Yuheng Huang, Felix Juefei-Xu, and Lei Ma. 2024.
LUNA: A Model-Based Universal Analysis Framework for Large Language Models.
IEEE Transactions on Software Engineering
(2024).
Spiess et al
.
(2025)
Claudio Spiess, David Gros, et al
.
2025.
Calibration and correctness of language models for code.
Proceedings of the 47th International Conference on Software Engineering (ICSE 2025)
(2025).
Su et al
.
(2024a)
Hongjin Su, Shuyang Jiang, Yuhang Lai, Haoyuan Wu, Boao Shi, Che Liu, Qian Liu, and Tao Yu. 2024a.
EvoR: Evolving Retrieval for Code Generation. In
Findings of the Association for Computational Linguistics: EMNLP 2024
, Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguistics, Miami, Florida, USA, 2538–2554.
https://doi.org/10.18653/v1/2024.findings-emnlp.143
Su et al
.
(2024b)
Zian Su, Xiangzhe Xu, Ziyang Huang, Zhuo Zhang, Yapeng Ye, Jianjun Huang, and Xiangyu Zhang. 2024b.
Codeart: Better code models by attention regularization when symbols are lacking.
Proceedings of the ACM on Software Engineering
1, FSE (2024), 562–585.
Tang et al
.
(2024)
Ningzhi Tang, Meng Chen, Zheng Ning, Aakash Bansal, Yu Huang, Collin McMillan, and Toby Jia-Jun Li. 2024.
A Study on Developer Behaviors for Validating and Repairing LLM-Generated Code Using Eye Tracking and IDE Actions.
arXiv preprint arXiv:2405.16081
(2024).
Team et al
.
(2024)
CodeGemma Team, Heri Zhao, Jeffrey Hui, Joshua Howland, et al
.
2024.
Codegemma: Open code models based on gemma.
arXiv preprint arXiv:2406.11409
(2024).
Tian et al
.
(2024)
Runchu Tian, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Zhiyuan Liu, and Maosong Sun. 2024.
DebugBench: Evaluating Debugging Capability of Large Language Models.
arXiv:2401.04621 [cs.SE]
Vaswani (2017)
A Vaswani. 2017.
Attention is all you need.
Advances in Neural Information Processing Systems
(2017).
Wang et al
.
(2024b)
Wenhan Wang, Chenyuan Yang, Zhijie Wang, Yuheng Huang, Zhaoyang Chu, Da Song, Lingming Zhang, An Ran Chen, and Lei Ma. 2024b.
TESTEVAL: Benchmarking Large Language Models for Test Case Generation.
arXiv preprint arXiv:2406.04531
(2024).
Wang et al
.
(2024a)
Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and Heng Ji. 2024a.
Executable Code Actions Elicit Better LLM Agents. In
ICML
.
arXiv:2402.01030
Wang et al
.
(2023)
Zhijie Wang, Yuheng Huang, Da Song, Lei Ma, and Tianyi Zhang. 2023.
Deepseer: Interactive rnn explanation and debugging via state abstraction. In
Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems
. 1–20.
Wang et al
.
(2024c)
Zhijie Wang, Zijie Zhou, Da Song, Yuheng Huang, Shengmai Chen, Lei Ma, and Tianyi Zhang. 2024c.
Where Do Large Language Models Fail When Generating Code?
arXiv preprint arXiv:2406.08731
(2024).
Wei et al
.
(2024)
Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. 2024.
Magicoder: Empowering Code Generation with OSS-Instruct. In
Proceedings of the 41st International Conference on Machine Learning
(Proceedings of Machine Learning Research, Vol. 235)
. PMLR, 52632–52657.
https://proceedings.mlr.press/v235/wei24h.html
Wu et al
.
(2024)
Xinwei Wu, Weilong Dong, Shaoyang Xu, and Deyi Xiong. 2024.
Mitigating Privacy Seesaw in Large Language Models: Augmented Privacy Neuron Editing via Activation Patching. In
Findings of the Association for Computational Linguistics: ACL 2024
, Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 5319–5332.
https://doi.org/10.18653/v1/2024.findings-acl.315
Xia et al
.
(2023)
Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023.
Automated program repair in the era of large pre-trained language models. In
2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)
. IEEE, 1482–1494.
Xie et al
.
(2024)
Danning Xie, Zhuo Zhang, Nan Jiang, Xiangzhe Xu, Lin Tan, and Xiangyu Zhang. 2024.
ReSym: Harnessing LLMs to Recover Variable and Data Structure Symbols from Stripped Binaries. In
Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security
. 4554–4568.
Yu et al
.
(2024)
Zhaojian Yu, Xin Zhang, et al
.
2024.
WaveCoder: Widespread and versatile enhancement for code large language models by instruction tuning. In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
. 5140–5153.
Zhang et al
.
(2024)
Shaolei Zhang, Tian Yu, and Yang Feng. 2024.
TruthX: Alleviating Hallucinations by Editing Large Language Models in Truthful Space. In
Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)
, Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 8908–8949.
https://doi.org/10.18653/v1/2024.acl-long.483
Zou et al
.
(2023)
Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, et al
.
2023.
Representation engineering: A top-down approach to ai transparency.
arXiv preprint arXiv:2310.01405
(2023).