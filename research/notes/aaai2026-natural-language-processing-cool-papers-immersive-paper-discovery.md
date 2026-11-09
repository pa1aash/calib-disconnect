---
title: AAAI.2026 - Natural Language Processing | Cool Papers - Immersive Paper Discovery
id: aaai2026-natural-language-processing-cool-papers-immersive-paper-discovery
tags:
- code-llm-best-aaai-paper-6ded37
- paper-shape-census
- source-hub
created: '2026-07-20T07:40:44.043088Z'
updated: '2026-07-20T07:46:18.443793Z'
source: https://papers.cool/venue/AAAI.2026?group=Natural+Language+Processing
source_domain: papers.cool
fetched_at: '2026-07-20T07:40:44.042586Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'Directory listing (595 papers) of AAAI-2026 NLP-track accepted papers with
  abstracts, from papers.cool venue browser. Sampled titles/abstracts show the dominant
  accepted-paper SHAPE at AAAI-26 NLP track: (method or framework) + (new benchmark/dataset
  OR mechanistic analysis) + (multi-model empirical evaluation with a clear numeric
  headline, e.g. ''macro-F1 +7.55%'', ''attack success rate reduced'', ''AUC 0.8-0.89'').
  Confirms code-generation and calibration/uncertainty papers are present but a small
  minority relative to safety/alignment, reasoning-efficiency, and dialogue/agent
  papers. No factor-analysis/IRT/latent-skill-decomposition paper specific to CODE
  generation appeared among sampled titles (general-domain IRT papers exist, see ''Lost
  in Benchmarks''). Source hub / directory, not a citable primary claim source itself.'
---

AAAI.2026 - Natural Language Processing | Cool Papers - Immersive Paper Discovery
AAAI.2026 - Natural Language Processing
|
        Total: 595
#1
LogicCat: A Chain-of-Thought Text-to-SQL Benchmark for Complex Reasoning
[PDF
40
]
[Copy]
[Kimi
9
]
[REL]
Authors
:
Liutao
,
Xutao Mao
,
Dixuan Zhang
,
Yifan Li
,
LiuHaixin
,
KongLulu
,
Jiaming Hou
,
Rui Li
,
YunLong Li
,
Aoze Zheng
,
Zhiqiang Zhang
,
Luo Zhewei
,
Hongying Zan
,
Kunli Zhang
,
Min Peng
Text-to-SQL is a critical task in natural language processing that aims to transform natural language questions into accurate and executable SQL queries. In real-world scenarios, these reasoning tasks are often accompanied by complex mathematical computations, domain knowledge, and hypothetical reasoning scenarios. However, existing large-scale Text-to-SQL datasets typically focus on business logic and task logic, neglecting critical factors such as vertical domain knowledge, complex mathematical reasoning, and hypothetical reasoning, which are essential for realistically reflecting the reasoning demands in practical applications and completing data querying and analysis. To bridge this gap, we introduce LogicCat, the first Text-to-SQL benchmark dataset specifically designed for complex reasoning and chain-of-thought parsing, encompassing physics, arithmetic, commonsense, and hypothetical reasoning scenarios. LogicCat comprises 4,038 English questions paired 12,114 detailed chain-of-thought reasoning steps, spanning 45 databases across diverse domains, significantly surpassing existing datasets in complexity. Experimental results demonstrate that LogicCat substantially increases the task difficulty for current state-of-the-art models to at most 33.20% execution accuracy, indicating that this task remains exceptionally challenging. The advancement of LogicCat represents a crucial step toward developing systems suitable for real-world enterprise data analysis and autonomous query generation.
Subject
:
AAAI.2026 - Natural Language Processing
#2
DialogXpert: Driving Intelligent and Emotion-Aware Conversations Through Online Value-Based Reinforcement Learning with LLM Priors
[PDF
31
]
[Copy]
[Kimi
6
]
[REL]
Authors
:
Tazeek Bin Abdur Rakib
,
Ambuj Mehrish
,
Lay-Ki Soon
,
Wern Han Lim
,
Soujanya Poria
Large-language-model (LLM) agents excel at reactive dialogue but struggle with proactive, goal-driven interactions due to myopic decoding and costly planning. We introduce DialogXpert, which leverages a frozen LLM to propose a small, high-quality set of candidate actions per turn and employs a compact Q-network over fixed BERT embeddings trained via temporal-difference learning to select optimal moves within this reduced space. By tracking the user's emotions DialogXpert tailors each decision to advance the task while nurturing a genuine, empathetic connection. Across negotiation, emotional support, and tutoring benchmarks, DialogXpert drives conversations to under 3 turns with success rates exceeding 94% and, with a larger LLM prior, pushes success above 97% while markedly improving negotiation outcomes. This framework delivers real-time, strategic, and emotionally intelligent dialogue planning at scale.
Subject
:
AAAI.2026 - Natural Language Processing
#3
Where Norms and References Collide: Evaluating LLMs on Normative Reasoning
[PDF
18
]
[Copy]
[Kimi
4
]
[REL]
Authors
:
Mitchell Abrams
,
Kaveh Eskandari Miandoab
,
Felix Gervits
,
Vasanth Sarathy
,
Matthias Scheutz
Embodied agents, such as robots, will need to interact in situated environments where successful communication often depends on reasoning over social norms: shared expectations that constrain what actions are appropriate in context. A key capability in such settings is norm-based reference resolution (NBRR), where interpreting referential expressions requires inferring implicit normative expectations grounded in physical and social context. Yet it remains unclear whether Large Language Models (LLMs) can support this kind of reasoning. In this work, we introduce SNIC (Situated Norms in Context), a human-validated diagnostic testbed designed to probe how well state-of-the-art LLMs can extract and utilize normative principles relevant to NBRR. SNIC emphasizes physically grounded norms that arise in everyday tasks such as cleaning, tidying, and serving. Across a range of controlled evaluations, we find that even the strongest LLMs struggle to consistently identify and apply social norms—particularly when norms are implicit, underspecified, or in conflict. These findings reveal a blind spot in current LLMs and highlight a key challenge for deploying language-based systems in socially situated, embodied settings.
Subject
:
AAAI.2026 - Natural Language Processing
#4
MAMA-Memeia! Multi-Aspect Multi-Agent Collaboration for Depressive Symptoms Identification in Memes
[PDF
30
]
[Copy]
[Kimi
6
]
[REL]
Authors
:
Siddhant Agarwal
,
Adya Dhuler
,
Polly Ruhnke
,
Melvin Speisman
,
Md Shad Akhtar
,
Shweta Yadav
Over the past years, memes have evolved from being exclusively a medium of humorous exchanges to one that allows users to express a range of emotions freely and easily. With the ever-growing utilization of memes in expressing depressive sentiments, we conduct a study on identifying depressive symptoms exhibited by memes shared by users of online social media platforms. We introduce RESTOREx as a vital resource for detecting depressive symptoms in memes on social media through the Large Language Model (LLM) generated and human-annotated explanations. We introduce MAMA-Memeia, a collaborative multi-agent multi-aspect discussion framework grounded in the clinical psychology method of Cognitive Analytic Therapy (CAT) Competencies. MAMA-Memeia improves upon the current state-of-the-art by 7.55% in macro-F1 and is established as the new benchmark compared to over 30 methods.
Subject
:
AAAI.2026 - Natural Language Processing
#5
ViDia2Std: A Parallel Corpus and Methods for Low-Resource Vietnamese Dialect-to-Standard Translation
[PDF
14
]
[Copy]
[Kimi
2
]
[REL]
Authors
:
Khoa Anh Ta
,
Nguyen Van Dinh
,
Kiet Van Nguyen
Vietnamese exhibits extensive dialectal variation, posing challenges for NLP systems trained predominantly on standard Vietnamese. Such systems often underperform on dialectal inputs, especially from underrepresented Central and Southern regions. Previous work on dialect normalization has focused narrowly on Central-to-Northern dialect transfer using synthetic data and limited dialectal diversity. These efforts exclude Southern varieties and intra-regional variants within the North. We introduce ViDia2Std, the first manually annotated parallel corpus for dialect-to-standard Vietnamese translation covering all 63 provinces. Unlike prior datasets, ViDia2Std includes diverse dialects from Central, Southern, and non-standard Northern regions often absent from existing resources, making it the most dialectally inclusive corpus to date. The dataset consists of over 13,000 sentence pairs sourced from real-world Facebook comments and annotated by native speakers across all three dialect regions. To assess annotation consistency, we define a semantic mapping agreement metric that accounts for synonymous standard mappings across annotators. Based on this criterion, we report agreement rates of 86% (North), 82% (Central), and 85% (South). We benchmark several sequence-to-sequence models on ViDia2Std. mBART-large-50 achieves the best results (BLEU 0.8166, ROUGE-L 0.9384, METEOR 0.8925), while ViT5-base offers competitive performance with fewer parameters. ViDia2Std demonstrates that dialect normalization substantially improves downstream tasks, highlighting the need for dialect-aware resources in building robust Vietnamese NLP systems.
Subject
:
AAAI.2026 - Natural Language Processing
#6
Rethinking Deep Alignment Through the Lens of Incomplete Safety Learning
[PDF
18
]
[Copy]
[Kimi
6
]
[REL]
Authors
:
Thong Bach
,
Dung Nguyen
,
Thao Minh Le
,
Truyen Tran
Large language models exhibit systematic vulnerabilities to adversarial attacks despite extensive safety alignment through supervised fine-tuning and reinforcement learning from human feedback. These vulnerabilities manifest as differential safety behavior across token positions, with safety modifications concentrating in early positions while later positions show minimal distributional changes from base models. We provide a mechanistic analysis of safety alignment training dynamics, revealing that gradient concentration during autoregressive training creates signal decay across token positions. This leads to incomplete distributional learning where safety training fails to fully transform model preferences in later response regions. We introduce base-favored tokens as computational indicators of incomplete safety learning. Analysis reveals that while early positions undergo substantial distributional changes, later positions retain concerning base model preferences in safety-critical contexts, indicating systematic incomplete learning due to insufficient training signals. We develop a targeted completion method that addresses these undertrained regions through adaptive penalties and hybrid teacher distillation. Experimental evaluation across Llama and Qwen model families demonstrates remarkable improvements in adversarial robustness, with dramatic reductions in attack success rates across multiple attack types while fully preserving general capabilities.
Subject
:
AAAI.2026 - Natural Language Processing
#7
HQ-SVC: Towards High-Quality Zero-Shot Singing Voice Conversion in Low-Resource Scenarios
[PDF
11
]
[Copy]
[Kimi
2
]
[REL]
Authors
:
Bingsong Bai
,
Yizhong Geng
,
Fengping Wang
,
Cong Wang
,
Puyuan Guo
,
Yingming Gao
,
Ya Li
Zero-shot singing voice conversion (SVC) transforms a source singer's timbre to an unseen target speaker's voice while preserving melodic content without fine-tuning. Existing methods model speaker timbre and vocal content separately, losing essential acoustic information that degrades output quality while requiring significant computational resources. To overcome these limitations, we propose HQ-SVC, an efficient framework for high-quality zero-shot SVC. HQ-SVC first extracts jointly content and speaker features using a decoupled codec. It then enhances fidelity through pitch and volume modeling, preserving critical acoustic information typically lost in separate modeling approaches, and progressively refines outputs via differentiable signal processing and diffusion techniques. Evaluations confirm HQ-SVC significantly outperforms state-of-the-art zero-shot SVC methods in conversion quality and efficiency. Beyond voice conversion, HQ-SVC achieves superior voice naturalness compared to specialized audio super-resolution methods while natively supporting voice super-resolution tasks.
Subject
:
AAAI.2026 - Natural Language Processing
#8
Towards Effective Code-Integrated Reasoning
[PDF
9
]
[Copy]
[Kimi
2
]
[REL]
Authors
:
Fei Bai
,
Yingqian Min
,
Beichen Zhang
,
Zhipeng Chen
,
Xin Zhao
,
Lei Fang
,
Zheng Liu
,
Zhongyuan Wang
,
Hongteng Xu
In this paper, we investigate code-integrated reasoning (CIR), where models generate code when necessary and integrate feedback by executing it through a code interpreter. To acquire this capability, models must learn when and how to use external code tools effectively, which is supported by tool-augmented reinforcement learning (RL). Despite its benefits, tool-augmented RL can still suffer from potential instability in the learning dynamics. In light of this challenge, we present a systematic approach ETIR (Effective TIR) to improving the training effectiveness and stability of tool-augmented RL for code-integrated reasoning. Specifically, we develop enhanced training strategies that balance exploration and stability, progressively building tool-use capabilities while improving reasoning performance. Through extensive experiments on five mainstream mathematical reasoning benchmarks, our model demonstrates significant performance improvements over multiple competitive baselines. Furthermore, we conduct an in-depth analysis of the mechanism of code-integrated reasoning, revealing several key insights, such as the extension of model’s capability boundaries and the simultaneous improvement of reasoning efficiency through code integration. These findings underscore the potential of code-integrated reasoning as a scalable paradigm for advancing robust and efficient language model reasoning.
Subject
:
AAAI.2026 - Natural Language Processing
#9
Identifying and Analyzing Performance-Critical Tokens in Large Language Models
[PDF
13
]
[Copy]
[Kimi
4
]
[REL]
Authors
:
Yu Bai
,
Heyan Huang
,
Cesare Spinoso-Di Piano
,
Sanxing Chen
,
Marc-Antoine Rondeau
,
Yang Gao
,
Jackie Chi Kit Cheung
In-context learning (ICL) has emerged as an effective solution for few-shot learning with large language models (LLMs). However, how LLMs leverage demonstrations to specify a task and learn a corresponding computational function through ICL is underexplored. Drawing from the way humans learn from content-label mappings in demonstrations, we categorize the tokens in an ICL prompt into content, stopword, and template tokens. Our goal is to identify the types of tokens whose representations directly influence LLM's performance, a property we refer to as being performance-critical. By ablating representations from the attention of the test example, we find that the representations of informative content tokens have less influence on performance compared to template and stopword tokens, which contrasts with the human attention to informative words. We give evidence that the representations of performance-critical tokens aggregate information from the content tokens. Moreover, we demonstrate experimentally that lexical meaning, repetition, and structural cues are the main distinguishing characteristics of these tokens. Our work sheds light on how LLMs learn to perform tasks from demonstrations and deepens our understanding of the roles different types of tokens play in LLMs.
Subject
:
AAAI.2026 - Natural Language Processing
#10
IROTE: Human-like Traits Elicitation of Large Language Model via In-Context Self-Reflective Optimization
[PDF
9
]
[Copy]
[Kimi
2
]
[REL]
Authors
:
Yuzhuo Bai
,
Shitong Duan
,
Muhua Huang
,
Jing Yao
,
Zhenghao Liu
,
Peng Zhang
,
Tun Lu
,
Xiaoyuan Yi
,
Maosong Sun
,
Xing Xie
Trained on various human-authored corpora, Large Language Models (LLMs) have demonstrated a certain capability of reflecting specific human-like traits (e.g., personality or values) by prompting, benefiting applications like personalized LLMs and social simulations. However, existing methods suffer from the superficial elicitation problem: LLMs can only be steered to mimic shallow and unstable stylistic patterns, failing to embody the desired traits precisely and consistently across diverse tasks like humans. To address this challenge, we propose IROTE, a novel in-context method for stable and transferable trait elicitation. Drawing on psychological theories suggesting that traits are formed through identity-related reflection, our method automatically generates and optimizes a textual self-reflection within prompts, which comprises self-perceived experience, to stimulate LLMs' trait-driven behavior. The optimization is performed by iteratively maximizing an information-theoretic objective that enhances the connections between LLMs' behavior and the target trait, while reducing noisy redundancy in reflection without any fine-tuning, leading to evocative and compact trait reflection. Extensive experiments across three human trait systems manifest that one single IROTE-generated self-reflection can induce LLMs' stable impersonation of the target trait across diverse downstream tasks beyond simple questionnaire answering, consistently outperforming existing strong baselines.
Subject
:
AAAI.2026 - Natural Language Processing
#11
Time-Frequency Token Advantage Clipping for Training Efficient Large Reasoning Model
[PDF
10
]
[Copy]
[Kimi
1
]
[REL]
Authors
:
Rong Bao
,
Bo Wang
,
Xiao Wang
,
Hongyu Li
,
Rui Zheng
,
Leszek Rutkowski
,
Qi Zhang
,
Liang Ding
,
Dacheng Tao
Long Chain-of-Thought (CoT) reasoning enhances large reasoning models' performance but suffers from severe inefficiencies, as models often overthink simple problems or underthink complex ones. Current sequence-level optimizations, like length penalties, are too coarse-grained to distinguish core logic from verbose language, precluding the necessary token-level control for efficient reasoning CoT. To overcome these limitations, we introduce Time-Frequency token Advantage Clipping (TFAC), a novel training framework designed to build efficient large reasoning models via token-level interventions. Specifically, TFAC functions along two dimensions: 1) The Frequency Dimension: It discourages inefficient loops and encourages deeper exploration by dynamically reducing the advantage scores of high-entropy tokens that are repeatedly generated within a single reasoning path. 2) The Time Dimension: It reduces excessive overthinking of the system by establishing a historical baseline for the occurrence count of each critical token in previously successful trajectories, and clipping the advantages of tokens that exceed this baseline during training. Crucially, to preserve the model's exploratory capabilities on novel problems, this suppression mechanism is automatically disabled when no historical record of success is available. Experiments conducted on the Deepseek-Distill-32B and Qwen3-8B models show that TFAC outperforms leading baseline methods, improving performance by 2.3 and 3.1 percentage points, respectively, while simultaneously reducing inference costs by 35% and 28% in scenarios where correct answers are generated. These results validate the significant efficacy of TFAC in training large reasoning models that are both powerful and highly efficient.
Subject
:
AAAI.2026 - Natural Language Processing
#12
Beyond Next Token Probabilities: Learnable, Fast Detection of Hallucinations and Data Contamination on LLM Output Distributions
[PDF
5
]
[Copy]
[Kimi
2
]
[REL]
Authors
:
Guy Bar-Shalom
,
Fabrizio Frasca
,
Derek Lim
,
Yoav Gelberg
,
Yftah Ziser
,
Ran El-Yaniv
,
Gal Chechik
,
Haggai Maron
The automated detection of hallucinations and training data contamination is pivotal to the safe deployment of Large Language Models (LLMs). These tasks are particularly challenging in settings where no access to model internals is available. Current approaches in this setup typically leverage only the probabilities of actual tokens in the text, relying on simple task-specific heuristics. Crucially, they overlook the information contained in the full sequence of next-token probability distributions. We propose to go beyond hand-crafted decision rules by learning directly from the complete observable output of LLMs — consisting not only of next-token probabilities, but also the full sequence of next-token distributions. We refer to this as the LLM Output Signature (LOS), and treat it as a reference data type for detecting hallucinations and data contamination. To that end, we introduce LOS-Net, a lightweight attention-based architecture trained on an efficient encoding of the LOS, which can provably approximate a broad class of existing techniques for both tasks. Empirically, LOS-Net achieves superior performance across diverse benchmarks and LLMs, while maintaining extremely low detection latency. Furthermore, it demonstrates promising transfer capabilities across datasets and LLMs.
Subject
:
AAAI.2026 - Natural Language Processing
#13
Steering Pretrained Drafters During Speculative Decoding
[PDF
3
]
[Copy]
[Kimi
2
]
[REL]
Authors
:
Frédéric Berdoz
,
Peer Rheinboldt
,
Roger Wattenhofer
Speculative decoding accelerates language model inference by separating generation into fast drafting and parallel verification. Its main limitation is drafter–verifier misalignment, which limits token acceptance and reduces overall effectiveness. While small drafting heads trained from scratch compensate with speed, they struggle when verification dominates latency or when inputs are out of distribution. In contrast, pretrained drafters, though slower, achieve higher acceptance rates thanks to stronger standalone generation capabilities, making them competitive when drafting latency is negligible relative to verification or communication overhead. In this work, we aim to improve the acceptance rates of pretrained drafters by introducing a lightweight dynamic alignment mechanism: a steering vector computed from the verifier’s hidden states and injected into the pretrained drafter. Compared to existing offline alignment methods such as distillation, our approach boosts the number of accepted tokens by up to 35% under standard sampling and 22% under greedy sampling, all while incurring negligible computational overhead. Importantly, our approach can be retrofitted to existing architectures and pretrained models, enabling rapid adoption.
Subject
:
AAAI.2026 - Natural Language Processing
#14
JudgeBoard: Benchmarking and Enhancing Small Language Models for Reasoning Evaluation
[PDF
12
]
[Copy]
[Kimi
1
]
[REL]
Authors
:
Zhenyu Bi
,
Gaurav Srivastava
,
Yang Li
,
Swastik Roy
,
Meng Lu
,
Morteza Ziyadi
,
Xuan Wang
While small language models (SLMs) have shown promise on various reasoning tasks, their ability to judge the correctness of answers remains unclear compared to large language models (LLMs). Prior work on LLM-as-a-judge frameworks typically relies on comparing candidate answers against ground-truth labels or other candidate answers using predefined metrics like entailment. However, this approach is inherently indirect and difficult to fully automate, offering limited support for fine-grained and scalable evaluation of reasoning outputs. In this work, we propose JudgeBoard, a novel evaluation pipeline that directly queries models to assess the correctness of candidate answers without requiring extra answer comparisons. We focus on two core reasoning domains: mathematical reasoning and science/commonsense reasoning, and construct task-specific evaluation leaderboards using both accuracy-based ranking and an Elo-based rating system across five benchmark datasets, enabling consistent model comparison as judges rather than comparators. To improve judgment performance in lightweight models, we propose MAJ (Multi-Agent Judging), a novel multi-agent evaluation framework that leverages multiple interacting SLMs with distinct reasoning profiles to approximate LLM-level judgment accuracy through collaborative deliberation. Experimental results reveal a significant performance gap between SLMs and LLMs in isolated judging tasks. However, our MAJ framework substantially improves the reliability and consistency of SLMs. On the MATH dataset, MAJ using smaller-sized models as backbones performs comparatively well or even better than their larger-sized counterparts. Our findings highlight that multi-agent SLM systems can potentially match or exceed LLM performance in judgment tasks, with implications for scalable and efficient assessment.
Subject
:
AAAI.2026 - Natural Language Processing
#15
OptiHive: Ensemble Selection for LLM-Based Optimization via Statistical Modeling
[PDF
5
]
[Copy]
[Kimi
]
[REL]
Authors
:
Maxime Bouscary
,
Saurabh Amin
LLM-based solvers have emerged as a promising means of automating problem modeling and solving. However, they remain unreliable and often depend on iterative repair loops that result in significant latency. We introduce OptiHive, a framework that enhances any solver-generation pipeline to produce higher-quality solvers from natural-language descriptions of optimization problems. OptiHive uses a single batched generation to produce diverse components (solvers, problem instances, and validation tests) and filters out erroneous components to ensure fully interpretable outputs. Accounting for the imperfection of the generated components, we employ a statistical model to infer their true performance, enabling principled uncertainty quantification and solver selection. On tasks ranging from traditional optimization problems to challenging variants of the Multi-Depot Vehicle Routing Problem, OptiHive significantly outperforms baselines, increasing the optimality rate from 5% to 92% on the most complex problems.
Subject
:
AAAI.2026 - Natural Language Processing
#16
Do LLMs Really Struggle at NL-FOL Translation? Revealing Their Strengths via a Novel Benchmarking Strategy
[PDF
5
]
[Copy]
[Kimi
]
[REL]
Authors
:
Andrea Brunello
,
Luca Geatti
,
Michele Mignani
,
Angelo Montanari
,
Nicola Saccomanno
Due to its expressiveness and unambiguous nature, First-Order Logic (FOL) is a powerful formalism for representing concepts expressed in natural language (NL). This is useful, e.g., for specifying and verifying desired system properties. While translating FOL into human-readable English is relatively straightforward, the inverse problem, converting NL to FOL (NL-FOL translation), has remained a longstanding challenge, for both humans and machines. Although the emergence of Large Language Models (LLMs) promised a breakthrough, recent literature provides contrasting results on their ability to perform NL-FOL translation. In this work, we provide a threefold contribution. First, we critically examine existing datasets and protocols for evaluating NL-FOL translation performance, revealing key limitations that may cause a misrepresentation of LLMs' actual capabilities. Second, to overcome these shortcomings, we propose a novel evaluation protocol explicitly designed to distinguish genuine semantic-level logical understanding from superficial pattern recognition, memorization, and dataset contamination. Third, using this new approach, we show that state-of-the-art, dialogue-oriented LLMs demonstrate strong NL-FOL translation skills and a genuine grasp of sentence-level logic, whereas embedding-centric models perform markedly worse.
Subject
:
AAAI.2026 - Natural Language Processing
#17
Sampling-Free Uncertainty Quantification via Hidden State Dynamics in Language Models
[PDF
2
]
[Copy]
[Kimi
]
[REL]
Authors
:
Yixin Bu
,
Guanyun Zou
,
Renzhi Wang
,
Runze Xia
,
Cunjun Wang
,
Hongliang Dai
,
Xiaoqing Ma
,
Piji Li
Large language models (LLMs) demonstrate remarkable capabilities in various complex language tasks, yet they face significant reliability challenges, including factual inaccuracies and generated biases. Uncertainty quantification (UQ) plays a pivotal role in assessing model trustworthiness, particularly for high-stakes applications. However, current UQ methods for LLMs encounter computational efficiency bottlenecks due to their reliance on extensive sampling or external model invocations. In this work, we introduce a novel, sampling-free uncertainty quantification framework centered on hidden layer representation analysis. Our method facilitates real-time uncertainty quantification by modeling hierarchical internal semantic dynamics during the generation process. Through comprehensive experiments on multiple QA datasets and diverse model scales, we show that our approach consistently outperforms existing uncertainty quantification techniques in distinguishing correct from incorrect generations. Our results reveal that analyzing the dynamic evolution of hidden states provides a potent and computationally efficient signal for uncertainty quantification, directly from the model's internal workings, surpassing methods that depend solely on output probabilities or approximations via multiple samples.
Subject
:
AAAI.2026 - Natural Language Processing
#18
RaCoT: Plug-and-Play Contrastive Example Generation Mechanism for Enhanced LLM Reasoning Reliability
[PDF
7
]
[Copy]
[Kimi
]
[REL]
Authors
:
Kaitong Cai
,
Jusheng Zhang
,
Yijia Fan
,
Jing Yang
,
Keze Wang
Retrieval-Augmented Generation (RAG) faces a core bottleneck with knowledge-sparse and semantically ambiguous long-tail queries, where retrieval noise distorts reasoning and necessitates costly post-processing. To tackle this, we propose RaCoT (Retrieval-aware Contrastive-of-Thought), a novel framework that shifts contrastive thinking to the pre-retrieval stage. By automatically generating a semantically adjacent yet differently answered contrastive question and extracting a Δ-Prompt to capture their key differences, RaCoT guides the model to proactively focus on the "critical details that determine answer divergence." This approach allows it to suppress semantic interference within a single retrieval pass, overcoming the theoretical bottleneck of single-vector queries that struggle to simultaneously encode signals for what to attend to and what to ignore. On six authoritative benchmarks, including PopQA and TriviaQA-unfiltered, RaCoT outperforms strong baselines like RankRAG and Self-RAG by 0.9-2.4 percentage points. It exhibits superior robustness, with a performance drop of only 8.6% in adversarial tests, far surpassing the over 15% degradation in other methods. Furthermore, its low latency (3.12s) and token overhead (11.54) place it on the accuracy-efficiency Pareto frontier, while ablation studies validate the necessity of each component. Ultimately, RaCoT reframes the RAG paradigm from "post-hoc context cleaning" to "a priori shaping of discriminative reasoning," offering an efficient and robust path toward reliable AI systems for real-time, resource-constrained deployments.
Subject
:
AAAI.2026 - Natural Language Processing
#19
ERank: Fusing Supervised Fine-Tuning and Reinforcement Learning for Effective and Efficient Text Reranking
[PDF
3
]
[Copy]
[Kimi
]
[REL]
Authors
:
Yuzheng Cai
,
Yanzhao Zhang
,
Dingkun Long
,
Mingxin Li
,
Pengjun Xie
,
Weiguo Zheng
Text reranking models are a crucial component in modern systems like Retrieval-Augmented Generation, tasked with selecting the most relevant documents prior to generation. However, current Large Language Models (LLMs) powered rerankers often face a fundamental trade-off. On one hand, Supervised Fine-Tuning based pointwise methods that frame relevance as a binary classification task lack the necessary scoring discrimination, particularly for those built on reasoning LLMs. On the other hand, approaches designed for complex reasoning often employ powerful yet inefficient listwise formulations, rendering them impractical for low latency applications. To resolve this dilemma, we introduce ERank, a highly Effective and Efficient pointwise reranker built from a reasoning LLM that excels across diverse relevance scenarios. We propose a novel two-stage training pipeline that begins with Supervised Fine-Tuning (SFT). In this stage, we move beyond binary labels and train the model generatively to output fine grained integer scores, which significantly enhances relevance discrimination. The model is then further refined using Reinforcement Learning (RL) with a novel, listwise derived reward. This technique instills global ranking awareness into the efficient pointwise architecture. We evaluate the ERank reranker on the BRIGHT, FollowIR, TREC DL, and BEIR benchmarks, demonstrating superior effectiveness and robustness compared to existing approaches. On the reasoning-intensive BRIGHT benchmark, our ERank-4B achieves an nDCG@10 of 38.7, while a larger 32B variant reaches a state of the art nDCG@10 of 40.2.
Subject
:
AAAI.2026 - Natural Language Processing
#20
Does Question Really Matter? The Attribution of Answer Bias in LLM Evaluation
[PDF
2
]
[Copy]
[Kimi
1
]
[REL]
Authors
:
Boxi Cao
,
Ruotong Pan
,
Hongyu Lin
,
Xianpei Han
,
Le Sun
Multiple-choices question answering (MCQA) has emerged as one of the most popular task formats for large language models (LLMs) evaluation. Unfortunately, there exist substantial evidence that the evaluation of current MCQA benchmarks suffers from significant answer bias, which severely undermines the reliability of the evaluation conclusions. Specifically, many LLMs achieve performance significantly higher than random selection even when the questions are omitted from input information. To this end, we conduct a systematic investigation of the attribution of answer bias, and demonstrate a strong correlation between the degree of data contamination and the severity of answer bias, while the position of options and the popularity of answers have relatively minor effects. Building on these insights, we further propose OPD, a straightforward yet effective tool for contamination detection and dataset debiasing without requiring access to the model’s internal training data. Our findings and algorithms provide valuable insights for the design of future trustworthy LLM evaluation protocols.
Subject
:
AAAI.2026 - Natural Language Processing
#21
On the Superimposed Noise Accumulation Problem in Sequential Knowledge Editing of Large Language Models
[PDF
5
]
[Copy]
[Kimi
1
]
[REL]
Authors
:
Ding Cao
,
Yuchen Cai
,
Yuqing Huang
,
Xuesong He
,
Rongxi Guo
,
Guiquan Liu
,
Guangzhong Sun
Sequential knowledge editing techniques aim to continuously update knowledge in large language models at low cost, preventing models from generating outdated or incorrect information. However, existing sequential editing methods suffer from a significant decline in editing success rates after long-term editing. Through theoretical analysis and experiments, our findings reveal that as the number of edits increases, the model's output increasingly deviates from the desired target, leading to a drop in editing success rates. We refer to this issue as the superimposed noise accumulation problem. Our further analysis demonstrates that the problem is related to the erroneous activation of irrelevant knowledge and conflicts between activated knowledge. Based on this analysis, a method named DeltaEdit is proposed that reduces conflicts between knowledge through dynamic orthogonal constraint strategies. Experiments show that DeltaEdit significantly reduces superimposed noise, achieving a 16.8% improvement in editing performance over the strongest baseline.
Subject
:
AAAI.2026 - Natural Language Processing
#22
TIV: Thought Injection via Vectors for Efficient Reasoning in Large Reasoning Models
[PDF
11
]
[Copy]
[Kimi
4
]
[REL]
Authors
:
Yi Cao
,
Weijie Shi
,
Wei-Jie Xu
,
Yucheng Shen
,
Yue Cui
,
Hanghui Guo
,
Shimin Di
,
Ziyi Liu
,
Jiaming Li
,
Alexander Zhou
,
Jia Zhu
,
Jiajie Xu
Large Reasoning Models (LRMs) have recently demonstrated impressive performance across a range of reasoning tasks by generating intermediate thoughts. However, these models can suffer from overthinking—generating excessive tokens that contribute little to final accuracy while increasing inference cost. To mitigate this, we propose TIV (Thought Injection via Vectors), an innovative framework that compresses token-level reasoning into compact vectors without sacrificing performance. Rather than generating explicit thoughts, TIV injects learnable vectors into the post-attention hidden states of the final token across Transformer layers, enabling implicit and lightweight reasoning. We further introduce a two-stage reinforcement learning strategy: the first stage calibrates the model's reasoning distribution, and the second distills it into a vector-based policy optimized for both accuracy and brevity. Experiments on three reasoning benchmarks show that TIV preserves over 99% of the original accuracy while reducing output length by more than 65% on average, reaching up to 80% in some cases. Moreover, TIV consistently achieves superior trade-offs between accuracy and efficiency compared to existing methods, distinguishing itself as a state-of-the-art (SOTA) approach for efficient reasoning in LRMs.
Subject
:
AAAI.2026 - Natural Language Processing
#23
DCTR: Dual-Constraint Subgraph Optimization for Knowledge Graph-based Retrieval-Augmented Generation
[PDF
5
]
[Copy]
[Kimi
1
]
[REL]
Authors
:
Yukun Cao
,
Zirui Xu
,
Dongyang Li
,
Zhihao Guo
,
Luobin Huang
,
Lisheng Wang
Knowledge Graph (KG)-based Retrieval-Augmented Generation (RAG) shifts the contents of retrieval from narrative text to a relational knowledge network, empowering large language models (LLMs) to harness structured relationships between entities. However, conventional KG-RAG approaches are resource-intensive, requiring either query decomposition with multiple LLM rounds or parameterized static knowledge injection to update the model. Although subgraph reasoning aims to address these issues, most current methods are based on heuristic shortest path and multi-hop graph traversal algorithms. The retrieved subgraphs suffer from incompleteness and semantic drift, and neglect the interaction between subgraph and LLMs in terms of fine-grained structural semantics. We propose a dual-constraint subgraph optimization for KG-RAG (DCTR). It improves subgraph retrieval and generates high-quality subgraphs with structural integrity and information salience for LLMs. Specifically, it formulates subgraph generation as a two-stage graph-theoretic constrained optimization problem to create compact and complete pseudo-labels. Since these pseudo-labels are discrete, a smooth approximation is employed to convert them into a differentiable representation, thereby optimizing the retriever to highlight key information while extracting subgraphs. On two benchmark datasets, DCTR significantly enhances subgraph quality, achieving state-of-the-art performance in LLM reasoning.
Subject
:
AAAI.2026 - Natural Language Processing
#24
Sparse Attention Across Multiple-Context KV Cache
[PDF
5
]
[Copy]
[Kimi
2
]
[REL]
Authors
:
Ziyi Cao
,
Qingyi Si
,
Jingbin Zhang
,
Bingquan Liu
Large language models face significant cost challenges in long-sequence inference. To address this, reusing historical Key-Value (KV) Cache for improved inference efficiency has become a mainstream approach. Recent advances further enhance throughput by sparse attention mechanisms to select the most relevant KV Cache, thereby reducing sequence length. However, such techniques are limited to single-context scenarios, where historical KV Cache is computed sequentially with causal-attention dependencies. In retrieval-augmented generation (RAG) scenarios, where retrieved documents as context are unknown beforehand, each document’s KV Cache is computed and stored independently (termed multiple-context KV Cache), lacking cross-attention between contexts. This renders existing methods ineffective. Although prior work partially recomputes multiple-context KV Cache to mitigate accuracy loss from missing cross-attention, it requires retaining all KV Cache throughout, failing to reduce memory overhead. This paper presents SamKV, the first exploration of attention sparsification for multiple-context KV Cache. Specifically, SamKV takes into account the complementary information of other contexts when sparsifying one context, and then locally recomputes the sparsified information. Experiments demonstrate that our method compresses sequence length to 15% without accuracy degradation compared with full-recomputation baselines, significantly boosting throughput in multi-context RAG scenarios.
Subject
:
AAAI.2026 - Natural Language Processing
#25
Calibrating and Rotating: A Unified Framework for Weight Conditioning in PEFT
[PDF
5
]
[Copy]
[Kimi
]
[REL]
Authors
:
Da Chang
,
Peng Xue
,
Yu Li
,
Yongxiang Liu
,
Pengxiang Xu
,
Shixun Zhang
Parameter-Efficient Fine-Tuning (PEFT) methods are crucial for adapting large pre-trained models. Among these, LoRA is considered a foundational approach. Building on this, the influential DoRA method enhances performance by decomposing weight updates into magnitude and direction. However, its underlying mechanism remains unclear, and it introduces significant computational overhead. In this work, we first identify that DoRA's success stems from its capacity to increase the singular value entropy of the weight update matrix, which promotes a more uniform update distribution akin to full fine-tuning. We then reformulate DoRA into a mathematically equivalent and more efficient matrix form, revealing it as a learnable weight conditioning method. Based on this insight, we propose a unified framework for designing advanced PEFT methods by exploring two orthogonal dimensions: the architectural placement and the transformation type of the conditioning matrix. Within this framework, we introduce two novel methods: (1) Pre-Diag, which applies a diagonal conditioning matrix before the LoRA update to efficiently calibrate the pre-trained weights, thereby enhancing performance while reducing training time; and (2) Skewed Orthogonal Rotation Adaptation (SORA), which employs a parameter-efficient orthogonal rotation to perform a more powerful, norm-preserving transformation of the feature space. Extensive experiments on natural language understanding and generation tasks demonstrate that our proposed methods achieve superior performance and efficiency compared to both LoRA and DoRA.
Subject
:
AAAI.2026 - Natural Language Processing
Designed by
kexue.fm
| Powered by
kimi.ai
Include(
OR
):
Exclude:
Search
Filter
Highlight
Stared Paper(s):
#1
LogicCat: A Chain-of-Thought Text-to-SQL Benchmark for Complex Reasoning
#2
DialogXpert: Driving Intelligent and Emotion-Aware Conversations Through Online Value-Based Reinforcement Learning with LLM Priors
#3
Where Norms and References Collide: Evaluating LLMs on Normative Reasoning
#4
MAMA-Memeia! Multi-Aspect Multi-Agent Collaboration for Depressive Symptoms Identification in Memes
#5
ViDia2Std: A Parallel Corpus and Methods for Low-Resource Vietnamese Dialect-to-Standard Translation
#6
Rethinking Deep Alignment Through the Lens of Incomplete Safety Learning
#7
HQ-SVC: Towards High-Quality Zero-Shot Singing Voice Conversion in Low-Resource Scenarios
#8
Towards Effective Code-Integrated Reasoning
#9
Identifying and Analyzing Performance-Critical Tokens in Large Language Models
#10
IROTE: Human-like Traits Elicitation of Large Language Model via In-Context Self-Reflective Optimization
#11
Time-Frequency Token Advantage Clipping for Training Efficient Large Reasoning Model
#12
Beyond Next Token Probabilities: Learnable, Fast Detection of Hallucinations and Data Contamination on LLM Output Distributions
#13
Steering Pretrained Drafters During Speculative Decoding
#14
JudgeBoard: Benchmarking and Enhancing Small Language Models for Reasoning Evaluation
#15
OptiHive: Ensemble Selection for LLM-Based Optimization via Statistical Modeling
#16
Do LLMs Really Struggle at NL-FOL Translation? Revealing Their Strengths via a Novel Benchmarking Strategy
#17
Sampling-Free Uncertainty Quantification via Hidden State Dynamics in Language Models
#18
RaCoT: Plug-and-Play Contrastive Example Generation Mechanism for Enhanced LLM Reasoning Reliability
#19
ERank: Fusing Supervised Fine-Tuning and Reinforcement Learning for Effective and Efficient Text Reranking
#20
Does Question Really Matter? The Attribution of Answer Bias in LLM Evaluation
#21
On the Superimposed Noise Accumulation Problem in Sequential Knowledge Editing of Large Language Models
#22
TIV: Thought Injection via Vectors for Efficient Reasoning in Large Reasoning Models
#23
DCTR: Dual-Constraint Subgraph Optimization for Knowledge Graph-based Retrieval-Augmented Generation
#24
Sparse Attention Across Multiple-Context KV Cache
#25
Calibrating and Rotating: A Unified Framework for Weight Conditioning in PEFT
Export
Magic Token:
Kimi Language:
中文
English
Desc Language:
中文
English
Save
Bug report? Issue submit? Please visit:
Github:
https://github.com/bojone/papers.cool
Please read our
Disclaimer
before proceeding.
For more interesting features, please visit
kexue.fm
and
kimi.ai
.