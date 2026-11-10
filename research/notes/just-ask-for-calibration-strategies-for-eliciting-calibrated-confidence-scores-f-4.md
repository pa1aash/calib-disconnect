---
title: 'Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores
  from Language Models Fine-Tuned with Human Feedback'
id: just-ask-for-calibration-strategies-for-eliciting-calibrated-confidence-scores-f-4
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:13:01.704309Z'
source: https://arxiv.org/html/2305.14975v1
source_domain: arxiv.org
fetched_at: '2026-11-09T23:13:01.702341Z'
fetch_provider: builtin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
---

Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
Skip to main content
Title:
Content selection saved. Describe the issue below:
Description:
License: CC BY 4.0
arXiv:2305.14975v1 [cs.CL] 24 May 2023
Just Ask for Calibration
: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
Katherine Tian*
†
Eric Mitchell*
‡
Allan Zhou
‡
Archit Sharma
‡
Rafael Rafailov
‡
Huaxiu Yao
‡
Chelsea Finn
‡
Christopher D. Manning
‡
†
Harvard University
‡
Stanford University
Abstract
A trustworthy real-world prediction system should be
well-calibrated
; that is, its confidence in an answer is indicative of the likelihood that the answer is correct, enabling deferral to a more expensive expert in cases of low-confidence predictions. While recent studies have shown that unsupervised pre-training produces large language models (LMs) that are remarkably well-calibrated, the most widely-used LMs in practice are fine-tuned with reinforcement learning with human feedback (RLHF-LMs) after the initial unsupervised pre-training stage, and results are mixed as to whether these models preserve the well-calibratedness of their ancestors. In this paper, we conduct a broad evaluation of computationally feasible methods for extracting confidence scores from LLMs fine-tuned with RLHF. We find that with the right prompting strategy, RLHF-LMs verbalize probabilities that are much better calibrated than the model’s conditional probabilities, enabling fairly well-calibrated predictions. Through a combination of prompting strategy and temperature scaling, we find that we can reduce the expected calibration error of RLHF-LMs by over 50%.
1
Introduction
†
†
* Equal contribution. Correspondence to
ktian@college.harvard.edu
,
eric.mitchell@cs.stanford.edu
.
A trustworthy prediction system should produce not just predictions, but
well-calibrated
probabilities: the model’s confidence in a prediction should accurately reflect the probability that the prediction is correct
(
Guo et al., 2017
)
. In the context of language models, one consequence of poor calibration may be
hallucination
, where a language model confidently asserts incorrect facts or reasoning. While the ability of very large LMs to absorb, synthesize, and recombine knowledge about the outside world has gained significant attention
(
Brown et al., 2020
;
Roberts et al., 2020
;
Bubeck et al., 2023
)
, relatively little attention has been given to their well-calibratedness
(
Kadavath et al., 2022
)
. Further, most existing analyses of the calibratedness of LLMs focuses on models trained with maximum likelihood, while in practice, the most widely-used LLMs (such as ChatGPT) are fine-tuned from a pre-trained generative model with methods such as reinforcement learning from human feedback
(
Christiano et al., 2017
)
. Some findings have suggested that RLHF-LMs may sacrifice well-calibrated predictions for the sake of closer adherence to user instructions in dialogue
(
Kadavath et al., 2022
;
OpenAI, 2023
)
, as the reinforcement learning objective encourages the model to allocate as much probability mass as possible to the most likely answer, rather than matching the relative frequency of possible answers.
Figure 1:
Calibration plots and ECE for
gpt-3.5-turbo
on the SciQ science question-answering dataset. For each bar corresponding to a range of x-axis values, the height of the bar is the average accuracy of model predictions whose confidence falls within the x-axis range. Darker bars mean a larger percentage of model predictions fall into that range. Using raw model probabilities
(left; Label Prob.)
to assess confidence leads to consistent over-confidence. Using directly verbalized numerical probabilities
(middle three plots; Verb. 1S top-
k
k
)
provides significantly improved calibration, with calibration improving as the model produces more possible hypotheses before giving a confidence score (mirroring the phenomenon of ‘Considering the Opposite’ in human psychology;
Lord et al. (1985)
). Alternatively to verbalized numerical probabilities, verbalizing linguistic
expressions of likelihood
(right)
also provides well-calibrated confidences.
In this paper, we evaluate a collection of methods for extracting confidences about model predictions from RLHF-LMs. Due to concerns that RLHF may cause systematic overconfidence in the model’s probabilities, as well as the general unavailability of per-token log-probabilities in widely used RLHF-LMs, we pay particular attention to prompting strategies that elicit
verbalized
probabilities, i.e., the model expresses its confidence in token-space, as either numerical probabilities or another linguistic expression of uncertainty.
We find that, surprisingly, popular RLHF-LMs are able to verbalize confidence scores directly that are better-calibrated than the true conditional probabilities of the model (estimated via sampling), even without
any
fine-tuning specifically for verbalizing confidence accurately.
Inspired by research in human psychology showing that overconfidence can be mitigated by considering alternative answers before responding
(
Lord et al., 1985
;
Mussweiler et al., 2000
)
, we show that prompting a model to produce several answer choices before giving its confidence scores significantly improves calibration of verbalized probabilities. Combined with temperature scaling
(
Guo et al., 2017
)
, this approach consistently improves the calibration of ChatGPT and GPT-4 across datasets, reducing expected calibration error (ECE) by well over 50% on average.
Related Work.
Several studies have examined the calibration of large LMs
(
Lin et al., 2022a
;
Park and Caragea, 2022
;
Kadavath et al., 2022
;
Xiao et al., 2022
;
Kuhn et al., 2023
)
, finding that combining large pre-trained LMs with temperature scaling
(
Guo et al., 2017
)
produces very well-calibrated predictions
(
Kadavath et al., 2022
;
Xiao et al., 2022
;
Kuhn et al., 2023
)
. Other works focus on the tendency of language and dialogue models to use linguistic expressions of uncertainty in a well-calibrated manner
(
Zhou et al., 2023
;
Mielke et al., 2022
)
. However, existing studies focus on LMs trained purely with supervised learning (
Kadavath et al. (2022)
briefly examine RLHF-LMs), while widely-used models in practice are fine-tuned with instruction-tuning or RLHF
(
Christiano et al., 2017
)
. RLHF has been shown to effectively leverage annotations of human preferences to control sentiment
(
Ziegler et al., 2020
)
, improve summarization or instruction-following quality
(
Stiennon et al., 2022
;
Ouyang et al., 2022
)
, and inject behavioral priors of harmlessness
(
Bai et al., 2022b
;
Bai et al., 2022a
)
. However, recent work has raised the question of whether or not RLHF is damaging to calibration
(
OpenAI, 2023
)
.
Our work is the first to perform a targeted analysis of the calibration of RLHF-LMs, focusing on ChatGPT and GPT-4.
2
Evaluating Calibration in RLHF-LMs
To better understand the factors influencing calibration in RLHF-LMs, we conduct a collection of experiments with
gpt-3.5-turbo
(ChatGPT) and
gpt-4
(GPT-4).
Metrics.
We measure calibration with multiple metrics. To measure
ECE
(expected calibration error;
Guo et al. (2017)
), we bin model predictions by their confidence and measure the average accuracy of predictions in each confidence bin. The ECE is defined as the average (squared) error between the average accuracy and confidence within each bin, where each error is weighted by the fraction of samples falling within the bin. We report raw ECE as well as ECE with temperature scaling
(ECE-t)
. Temperature scaling fits a single temperature value
β
\beta
to the model’s confidences to minimize negative log likelihood (NLL) on the data, giving scaled probability
p
~
\tilde{p}
of class
i
i
as
p
~
i
∝
p
i
β
\tilde{p}_{i}\propto p_{i}^{\beta}
. See Figure
1
for a depiction of ECE binning. Finally, we assess calibration using metrics from the selective classification literature, where a model may
abstain
from predicting when its confidence is low. We measure
accuracy@coverage
(acc@
q
q
) and
coverage@accuracy
(cov@
p
p
). acc@
q
q
is defined as the accuracy of the most confident
q
q
percent of predictions (i.e., precision), while cov@
p
p
measures the largest percentage
c
c
such that the most confident
c
c
percent of predictions have accuracy above
p
p
(i.e., recall). While ECE in a sense measures the reliability of confidence scores in isolation, acc@
q
q
and cov@
p
p
measure
relative
quality of confidence scores; the results are invariant to monotonic transformations of the scores.
TriviaQA
SciQ
TruthfulQA
Method Name
ECE
↓
\downarrow
ECE-t
↓
\downarrow
acc@50
↑
\uparrow
cov@90
↑
\uparrow
ECE
↓
\downarrow
ECE-t
↓
\downarrow
acc@50
↑
\uparrow
cov@70
↑
\uparrow
ECE
↓
\downarrow
ECE-t
↓
\downarrow
acc@50
↑
\uparrow
cov@50
↑
\uparrow
Label prob.
0.144
0.096
0.738
0.460
0.259
0.196
0.780
0.789
0.442
0.328
0.422
0.009
‘Is True’ prob.
0.135
0.090
0.885
0.020
0.350
0.200
0.710
0.550
0.425
0.234
0.542
0.566
Entropy
-
-
0.895
0.460
-
-
0.780
0.789
-
-
0.422
0.009
Verb. CoT
0.112
0.137
0.852
0.029
0.325
0.239
0.716
0.582
0.425
0.245
0.564
0.706
Verb. 1S top-1
0.071
0.097
0.912
0.581
0.243
0.095
0.779
0.819
0.383
0.191
0.538
0.651
Verb. 1S top-2
0.048
0.049
0.920
0.564
0.140
0.064
0.770
0.859
0.362
0.103
0.475
0.393
Verb. 1S top-4
0.047
0.073
0.917
0.641
0.070
0.056
0.762
0.830
0.199
0.462
0.395
0.305
Verb. 2S top-1
0.135
0.090
0.885
0.020
0.350
0.200
0.710
0.550
0.425
0.234
0.542
0.566
Verb. 2S top-2
0.053
0.047
0.912
0.571
0.165
0.042
0.765
0.807
0.397
0.101
0.498
0.495
Verb. 2S top-4
0.045
0.045
0.875
0.377
0.136
0.049
0.728
0.656
0.273
0.145
0.425
0.301
Ling. 1S-human
0.066
0.065
0.899
0.632
0.163
0.093
0.712
0.818
0.309
0.256
0.469
0.352
Ling. 1S-opt.
0.063
0.055
0.898
0.548
0.066
0.062
0.703
0.638
0.179
0.168
0.440
0.234
Table 1:
Verbalized confidences are
reliably
better calibrated than using the true model probabilities (as estimated by sampling with
n
=
10
n=10
samples), although the best approach to verbalized probabilities varies by dataset. Linguistic expressions of uncertainty (selecting from a fixed set of expressions like ‘highly likely’ and post-hoc mapping each expression to a probability) is also a strong alternative, often outperforming direct probability verbalization.
Datasets.
Our experiments use three question-answering datasets assessing factual knowledge. TriviaQA
(
Joshi et al., 2017
)
contains 650k question-answer pairs gathered by trivia enthusiasts, SciQ
(
Welbl et al., 2017
)
contains approximately 14k crowdsourced science exam question-answer pairs, and TruthfulQA
(
Lin et al., 2022b
)
contains 817 questions designed to test language models’ tendency to mimic human falsehoods. We sample 1000 questions from the validation split of TriviaQA and SciQ and take 817 questions from TruthfulQA for our experiments.
Evaluation protocol.
For each dataset, we generate a response and corresponding confidence from each method on each of the evaluation questions. Because calibration essentially quantifies the relationship between model confidence and correctness, computing correctness is crucial to accurate measurements of calibration. However, we find doing so to be a non-trivial challenge, especially in datasets where only a single ground-truth answer (but not aliases or semantically-equivalent rephrases) is provided. In order to avoid excessive false negatives in our correctness computation as a result of exact-match evaluation, we use a pre-trained RLHF-LM to evaluate the correctness of each response, using
gpt-4
for TriviaQA due to a high disagreement rate with a human evaluator and
gpt-3.5-turbo
for SciQ and TruthfulQA. We use the prompt “Are the following two answers to my question Q semantically equivalent?" and provide the question and two answers to the model to determine whether two answers are equivalent.
TriviaQA
SciQ
TruthfulQA
Method Name
ECE
ECE-t
acc@50
cov@90
ECE
ECE-t
acc@50
cov@85
ECE
ECE-t
acc@50
cov@50
Label prob.
0.082
0.080
0.958
0.976
0.221
0.173
0.820
0.177
0.441
0.330
0.489
0.024
Verb. 1S top-1
0.031
0.030
0.947
0.971
0.211
0.061
0.867
0.618
0.345
0.135
0.647
0.845
Verb. 1S top-4
0.042
0.031
0.967
0.977
0.054
0.052
0.835
0.417
0.198
0.135
0.650
0.965
Ling. 1S-hum.
0.057
0.048
0.938
0.984
0.149
0.042
0.860
0.521
0.234
0.130
0.642
0.881
Ling. 1S-opt.
0.051
0.049
0.930
0.983
0.040
0.041
0.854
0.508
0.121
0.137
0.628
0.883
Table 2:
Similarly to
gpt-3.5-turbo
, GPT-4’s verbalized probabilities are substantially better-calibrated than the model probabilities themselves, even after temperature scaling.
Methods.
We compare a wide variety of methods for extracting confidence estimates from LLMs. For a comprehensive list of the prompts used for each method, see Appendix Table
3
.
First, we consider two methods that leverage the true conditional distribution of the model to generate confidence scores. The simplest is
Label prob.
, which uses the conditional probability distribution
p
⁡
(
y
|
x
)
p(y|x)
of the model given a question
x
x
, which we estimate using
n
=
10
n=10
samples as the models in question do not offer per-token probabilities. We return the most common answer, using the LLM-based equivalence function to determine when two lexically different answers are semantically equivalent. In a variation described by
Kadavath et al. (2022)
,
‘Is True’ prob.
samples a single answer
y
y
from the model given a question
x
x
, and the probability it is true is estimated by the probability the model assigns to ‘True’ when asked if the given answer is true (where once again the probabilities are estimated via samples), i.e.,
p
⁡
(
True
|
x
,
y
^
)
p(\texttt{True}|x,\hat{y})
.
Next, we consider methods that extract confidence scores through
verbalization
(
Lin et al., 2022a
)
, i.e., the model expresses its confidence in token space, either with numerical probabilities or linguistic expressions of likelihood.
2
2
2
However, note that
none
of the methods described fine-tune the model to perform verbalization.
First,
Verb. 1S top-
k
k
uses verbalized numerical probabilities, that is, the model is prompted to express its probabilities in token-space, as a number from 0 to 1. We augment this procedure by asking the model to produce its top
k
k
guesses, and a probability for each one, all in a single response (i.e., ‘1 Stage’). We take the highest-probability prediction and its associated probability as the model’s output and confidence.
Verb. 2S top-
k
k
similarly uses numerical probabilities, except the model is first asked to provide only its answers, and afterwards, in a second round of dialogue, asked to assign probabilities of correctness to each answer (i.e., ‘2 stage’). That is, in this case, the model does not ‘know’ it will need to assign probabilities to its guesses when it produces them.
Ling. 1S-human
uses linguistic likelihood expressions, rather than numerical probabilities, to express uncertainty. The model is prompted to assign confidences to its guesses by choosing from a set of linguistic expressions of uncertainty: {
Almost certain
,
Likely
, … ,
Almost no chance
}. Each likelihood expression is mapped to a probability using responses from a human survey on social media with 123 respondents
(
Fagen-Ulmschneider, 2023
)
.
Ling. 1S-opt.
uses a held out set of calibration questions and answers to compute the average accuracy for each likelihood expression, using these ‘optimized’ values instead. Expressions that are not used for at least
1
N
\frac{1}{N}
of questions, where
N
N
is the number of calibration questions, simply use the human probability.
3
Results
Figure 2:
GPT-3.5-turbo usage rate of each likelihood expression; the model displays markedly verbalized lower confidence on TruthfulQA than more standard factual recall problems.
Tables
1
and
2
show the results of evaluating various methods for extracting confidence from RLHF-LMs on
gpt-3.5-turbo
and
gpt-4
, respectively. We distill several key conclusions from these experiments.
1.
As a whole, our evaluations suggest that RLHF-LMs are capable of producing far better-calibrated confidence estimates through direct verbalization (asking for a numerical confidence probability) or linguistic uncertainty quantification (asking for confidence using one of a fixed set of choices, such as ‘highly likely’) than using the model’s probabilities themselves.
2.
Among the methods for verbalizing probabilities directly, we observe that generating and evaluating multiple hypotheses improves calibration (see Figure
1
), similarly to humans
(
Lord et al., 1985
)
, and corroborating a similar finding in LMs
(
Kadavath et al., 2022
)
.
3.
Language models are able can express their uncertainty with
words
and
numerical probabilities
with similar efficacy.
4.
For TruthfulQA, which is a quasi-adversarial dataset constructed to test model beliefs in common misconceptions, calibration is noticeably worse (i.e., much higher ECE), suggesting that while RLHF-LMs may be well-calibrated for standard factual recall problems, other problems requiring more robust
reasoning
may be more challenging. Figure
2
shows that
gpt-3.5-turbo
is systematically less confident for TruthfulQA (see Appendix Figure
3
for GPT-4).
4
Discussion
Our results raise several questions for future work. For example, the one-stage and two-stage verbalized numerical confidence prompts sometimes different drastically in the calibration of their confidences, even though they differ only in whether they ask for probabilities before or after generating answer choices: How can we reduce sensitivity of a model’s calibration to the prompt? Going beyond question-answering, can we leverage good calibration in short-answer settings to improve the reliability of long-form generations, perhaps by breaking down long-form generation into a sequence of short questions? Finally, to what extent does a language model’s calibration depend on the domain; do our conclusions in the context of factual recall hold in the context of reasoning or arithmetic? Answering these questions provides one path toward building more trustworthy and ultimately more useful language systems.
5
Acknowledgements
CF and CM are CIFAR Fellows. EM gratefully acknowledges funding from a Knight-Hennessy Graduate Fellowship. AZ is supported by the NSF graduate research fellowship program. This research was supported in part by Juniper Networks, Apple, and ONR grant N00014-20-1-2675. The authors thank Yoonho Lee and Noah Goodman for helpful feedback on calibration metrics and experiment design.
References
Bai et al. (2022a)
Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma,
Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, Nicholas Joseph,
Saurav Kadavath, Jackson Kernion, Tom Conerly, Sheer El-Showk, Nelson Elhage,
Zac Hatfield-Dodds, Danny Hernandez, Tristan Hume, Scott Johnston, Shauna
Kravec, Liane Lovitt, Neel Nanda, Catherine Olsson, Dario Amodei, Tom Brown,
Jack Clark, Sam McCandlish, Chris Olah, Ben Mann, and Jared Kaplan.
2022a.
Training a helpful and
harmless assistant with reinforcement learning from human feedback
.
Bai et al. (2022b)
Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion,
Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon,
Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain,
Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared
Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosuite,
Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi
Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott
Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham,
Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R.
Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam
McCandlish, Tom Brown, and Jared Kaplan. 2022b.
Constitutional ai:
Harmlessness from ai feedback
.
Brown et al. (2020)
Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla
Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon
Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris
Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever,
and Dario Amodei. 2020.
Language models are few-shot learners
.
In
Advances in Neural Information Processing Systems
,
volume 33, pages 1877–1901. Curran Associates, Inc.
Bubeck et al. (2023)
Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric
Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg,
Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro, and Yi Zhang. 2023.
Sparks of artificial general
intelligence: Early experiments with GPT-4
.
ArXiv preprint arXiv:2303.12712.
Christiano et al. (2017)
Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario
Amodei. 2017.
Deep reinforcement learning from human preferences
.
In
Advances in Neural Information Processing Systems
,
volume 30. Curran Associates, Inc.
Fagen-Ulmschneider (2023)
Wade Fagen-Ulmschneider. 2023.
Perception of probability words
.
05-24-2023.
Guo et al. (2017)
Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017.
On calibration
of modern neural networks
.
In
Proceedings of the 34th International Conference on Machine
Learning
, volume 70 of
Proceedings of Machine Learning Research
,
pages 1321–1330. PMLR.
Joshi et al. (2017)
Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. 2017.
TriviaQA: A large
scale distantly supervised challenge dataset for reading comprehension
.
In
Proceedings of the 55th Annual Meeting of the Association
for Computational Linguistics (Volume 1: Long Papers)
, pages 1601–1611,
Vancouver, Canada. Association for Computational Linguistics.
Kadavath et al. (2022)
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan
Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli
Tran-Johnson, Scott Johnston, Sheer El-Showk, Andy Jones, Nelson Elhage,
Tristan Hume, Anna Chen, Yuntao Bai, Sam Bowman, Stanislav Fort, Deep
Ganguli, Danny Hernandez, Josh Jacobson, Jackson Kernion, Shauna Kravec,
Liane Lovitt, Kamal Ndousse, Catherine Olsson, Sam Ringer, Dario Amodei, Tom
Brown, Jack Clark, Nicholas Joseph, Ben Mann, Sam McCandlish, Chris Olah, and
Jared Kaplan. 2022.
Language models (mostly)
know what they know
.
Cite arxiv:2207.05221Comment: 23+17 pages; refs added, typos fixed.
Kuhn et al. (2023)
Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.
Semantic
uncertainty: Linguistic invariances for uncertainty estimation in natural
language generation
.
In
The Eleventh International Conference on Learning
Representations
.
Lin et al. (2022a)
Stephanie Lin, Jacob Hilton, and Owain Evans. 2022a.
Teaching models
to express their uncertainty in words
.
Transactions on Machine Learning Research
.
Lin et al. (2022b)
Stephanie Lin, Jacob Hilton, and Owain Evans. 2022b.
TruthfulQA: Measuring how models mimic human falsehoods
.
In
Proceedings of the 60th Annual Meeting of the Association
for Computational Linguistics (Volume 1: Long Papers)
, pages 3214–3252,
Dublin, Ireland. Association for Computational Linguistics.
Lord et al. (1985)
Charles Lord, Mark Lepper, and Elizabeth Preston. 1985.
Considering the
opposite: A corrective strategy for social judgment
.
Journal of personality and social psychology
, 47:1231–43.
Mielke et al. (2022)
Sabrina J. Mielke, Arthur Szlam, Emily Dinan, and Y-Lan Boureau. 2022.
Reducing conversational
agents’ overconfidence through linguistic calibration
.
Transactions of the Association for Computational Linguistics
,
10:857–872.
Mussweiler et al. (2000)
Thomas Mussweiler, Fritz Strack, and Tim Pfeiffer. 2000.
Overcoming the
inevitable anchoring effect: Considering the opposite compensates for
selective accessibility
.
Personality and Social Psychology Bulletin
, 26(9):1142–1150.
OpenAI (2023)
OpenAI. 2023.
Gpt-4 technical report
.
Ouyang et al. (2022)
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela
Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John
Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda
Askell, Peter Welinder, Paul F Christiano, Jan Leike, and Ryan Lowe. 2022.
Training language models to follow instructions with human feedback
.
In
Advances in Neural Information Processing Systems
,
volume 35, pages 27730–27744. Curran Associates, Inc.
Park and Caragea (2022)
Seo Yeon Park and Cornelia Caragea. 2022.
On the
calibration of pre-trained language models using mixup guided by area under
the margin and saliency
.
In
Proceedings of the 60th Annual Meeting of the Association
for Computational Linguistics (Volume 1: Long Papers)
, pages 5364–5374,
Dublin, Ireland. Association for Computational Linguistics.
Roberts et al. (2020)
Adam Roberts, Colin Raffel, and Noam Shazeer. 2020.
How much
knowledge can you pack into the parameters of a language model?
In
Proceedings of the 2020 Conference on Empirical Methods in
Natural Language Processing (EMNLP)
, pages 5418–5426, Online. Association
for Computational Linguistics.
Stiennon et al. (2022)
Nisan Stiennon, Long Ouyang, Jeff Wu, Daniel M. Ziegler, Ryan Lowe, Chelsea
Voss, Alec Radford, Dario Amodei, and Paul Christiano. 2022.
Learning to summarize from
human feedback
.
Welbl et al. (2017)
Johannes Welbl, Nelson F. Liu, and Matt Gardner. 2017.
Crowdsourcing multiple choice science questions.
ArXiv
, abs/1707.06209.
Xiao et al. (2022)
Yuxin Xiao, Paul Pu Liang, Umang Bhatt, Willie Neiswanger, Ruslan
Salakhutdinov, and Louis-Philippe Morency. 2022.
Uncertainty
quantification with pre-trained language models: A large-scale empirical
analysis
.
In
Findings of the Association for Computational Linguistics:
EMNLP 2022
, pages 7273–7284, Abu Dhabi, United Arab Emirates. Association
for Computational Linguistics.
Zhou et al. (2023)
Kaitlyn Zhou, Dan Jurafsky, and Tatsunori Hashimoto. 2023.
Navigating the grey area:
Expressions of overconfidence and uncertainty in language models
.
Ziegler et al. (2020)
Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B. Brown, Alec Radford,
Dario Amodei, Paul Christiano, and Geoffrey Irving. 2020.
Fine-tuning language models
from human preferences
.
Appendix A
Prompt Templates
Method
Template
Label prob.
Provide your best guess for the following question. Give ONLY the guess, no other words or explanation.\n\nFor example:\n\nGuess: <most likely guess, as short as possible; not a complete sentence, just the guess!>\n\nThe question is:${THE_QUESTION}
‘Is True’ prob.
Question: ${QUESTION}\nProposed Answer: ${ANSWER}\nIs the proposed answer:\n\t(A) True or\n\t(B) False?\n The proposed answer is:
Verb. CoT
Provide your best guess for the following question. Before giving your answer, provide a step-by-step explanation of your thought process. Then on a new line give the guess with no other words or explanation.\n\nFor example:\n\nExplanation: <one sentence step-by-step explanation of your thought process>\n\nExplanation: <one sentence step-by-step explanation of your thought process>\n\nGuess: <most likely guess, as short as possible; not a complete sentence, just the guess!>\n\nThe question is: ${THE_QUESTION}
Verb. 1S top-1
Provide your best guess and the probability that it is correct (0.0 to 1.0) for the following question. Give ONLY the guess and probability, no other words or explanation. For example:\n\nGuess: <most likely guess, as short as possible; not a complete sentence, just the guess!>\n Probability: <the probability between 0.0 and 1.0 that your guess is correct, without any extra commentary whatsoever; just the probability!>\n\nThe question is: ${THE_QUESTION}
Verb. 1S top-
k
k
Provide your ${k} best guesses and the probability that each is correct (0.0 to 1.0) for the following question. Give ONLY the guesses and probabilities, no other words or explanation. For example:\n\nG1: <first most likely guess, as short as possible; not a complete sentence, just the guess!>\n\nP1: <the probability between 0.0 and 1.0 that G1 is correct, without any extra commentary whatsoever; just the probability!> ... G${k}: <${k}-th most likely guess, as short as possible; not a complete sentence, just the guess!>\n\nP${k}: <the probability between 0.0 and 1.0 that G${k} is correct, without any extra commentary whatsoever; just the probability!> \n\nThe question is: ${THE_QUESTION}
Verb. 2S top-1
Provide your best guess for the following question. Give ONLY the guess, no other words or explanation.\n\nFor example:\n\nGuess: <most likely guess, as short as possible; not a complete sentence, just the guess!>\n\nThe question is:${THE_QUESTION}
Provide the probability that your guess is correct. Give ONLY the probability, no other words or explanation.\n\nFor example:\n\nProbability: <the probability between 0.0 and 1.0 that your guess is correct, without any extra commentary whatsoever; just the probability!>\n
Verb. 2S top-
k
k
Provide your ${k} best guesses for the following question. Give ONLY the guesses, no other words or explanation. For example:\n\nG1: <first most likely guess, as short as possible; not a complete sentence, just the guess!>\n\nP1: <the probability between 0.0 and 1.0 that G1 is correct, without any extra commentary whatsoever; just the probability!> ... G${k}: <${k}-th most likely guess, as short as possible; not a complete sentence, just the guess!>\n\nThe question is:${THE_QUESTION}
Provide the probability that each of your guesses is correct. Give ONLY the probabilities, no other words or explanation.\n\nFor example:\n\nP1: <the probability between 0.0 and 1.0 that G1 is correct, without any extra commentary whatsoever; just the probability!>\n... P${k}: <the probability between 0.0 and 1.0 that G${k} is correct, without any extra commentary whatsoever; just the probability!>
Ling. 1S
Provide your best guess for the following question, and describe how likely it is that your guess is correct as one of the following expressions: ${EXPRESSION_LIST}. Give ONLY the guess and your confidence, no other words or explanation. For example:\n\nGuess: <most likely guess, as short as possible; not a complete sentence, just the guess!>\nConfidence: <description of confidence, without any extra commentary whatsoever; just a short phrase!> \n\nThe question is: ${THE_QUESTION}
Table 3:
Prompt templates for each method evaluated. Methods above the double line use multiple samples in order to estimate confidence scores; methods below the double line use the verbalized confidences directly, requiring only a single sample.
The prompt template for each sampling method is provided in Table
3
. The question is substituted for the variable
${THE_QUESTION}
in each prompt.
Appendix B
Additional Results
Here, we include the likelihood expression usage distribution for
gpt-4
(Figure
3
). The contrast between model confidence for TriviaQA and SciQ compared with TruthfulQA is even more stark.
Figure 3:
GPT-4 usage rate of each likelihood expression; the model displays markedly lower verbalized confidence on TruthfulQA than more standard factual recall problems.