---
title: 'Cognitive Dissonance: Why Do Language Model Outputs Disagree with Internal
  Representations of Truthfulness? (full text)'
id: cognitive-dissonance-why-do-language-model-outputs-disagree-with-internal-repres
tags:
- code-llm-confidence-positioning-d82d00
- full-text
created: '2026-11-09T23:28:15.872467Z'
updated: '2026-11-09T23:31:27.205356Z'
source: https://arxiv.org/pdf/2312.03729
status: draft
type: note
content_type: paper
deprecated: false
summary: 'Liu, Casper, Hadfield-Menell, Andreas 2023 (arXiv 2312.03729) full text:
  GPT2-XL/GPT-J probes vs query probabilities on BoolQ, SciQ, CREAK; probe advantage
  largely better calibration; taxonomy confabulation/heterogeneity/deception; ensemble
  helps in 4 of 6 cases.'
---

Cognitive Dissonance:
                                                                   Why Do Language Model Outputs Disagree
                                                                  with Internal Representations of Truthfulness?

                                                       Kevin Liu∗         Stephen Casper∗  Dylan Hadfield-Menell Jacob Andreas
                                                                                          MIT CSAIL
                                                                             {kevliu, scasper, dhm, jda}@mit.edu


                                                                   Abstract                                A p(query is correct) ∝ pLM(yes ∣ Q: …)                                         1
                                                                                                                                                                                                              Hetero-
                                                                                                                                                    no 0.20                                “Deception”
                                                                                                                                                                                                              geneity
                                                                                                                                                                                                                        Agreement
                                                 Neural language models (LMs) can be used to                          Language Model




                                                                                                                                                                     p(probe is correct)
                                                                                                                                                    yes 0.70
                                                                                                                                                                                           ⅔
                                                                                                                                                    he 0.02
                                                 evaluate the truth of factual statements in two             Q: Is Sting a police officer? A:        …                                          Model
                                                                                                                                                                                                                            Hetero-




arXiv:2312.03729v1 [cs.CL] 27 Nov 2023
                                                                                                                                                                                               Confabu-   Agreement
                                                                                                                                                                                                                            geneity
                                                 ways: they can be either queried for statement                                                                                            ⅓
                                                                                                                                                                                                lation

                                                                                                           B p(probe is correct) ∝ exp{ w⊤hLM(Q:… A: no) }
                                                 probabilities, or probed for internal represen-                                                                                                           Probe
                                                                                                                                                                                                                            Probe
                                                                                                                                                      Probe                                Agreement      Confabu-
                                                 tations of truthfulness. Past work has found                             Language Model
                                                                                                                                                                                           0              ⅓
                                                                                                                                                                                                           lation
                                                                                                                                                                                                                        ⅔
                                                                                                                                                                                                                            Error
                                                                                                                                                                                                                                      1
                                                                                                                                                    correct 0.1
                                                 that these two procedures sometimes disagree,               Q: Is Sting a police officer? A: yes   incorr. 0.9
                                                                                                                                                                     C                              p(query is correct)
                                                 and that probes tend to be more accurate than
                                                 LM outputs. This has led some researchers to
                                                                                                          GPT2-XL
                                                                                                                    30%
                                                 conclude that LMs “lie” or otherwise encode
                                                 non-cooperative communicative intents. Is this
                                                                                                                    0%
                                                 an accurate description of today’s LMs, or can
                                                 query–probe disagreement arise in other ways?                      60%
                                                 We identify three different classes of disagree-
                                                 ment, which we term confabulation, deception,
                                                                                                          GPT-J     30%
                                                 and heterogeneity. In many cases, the superi-
                                                 ority of probes is simply attributable to better
                                                 calibration on uncertain answers rather than                       0%

                                                 a greater fraction of correct, high-confidence           D                       BoolQ                           SciQ                                           CREAK


                                                 answers. In some cases, queries and probes
                                                 perform better on different subsets of inputs,           Figure 1: Varieties of disagreement between language
                                                 and accuracy can further be improved by en-              model outputs and internal states. We evaluate two
                                                 sembling the two.1                                       approaches for answering questions or verifying state-
                                                                                                          ments: querying models directly for answers (A), or
                                                                                                          training a binary classifier to probe their internal states
                                         1       Introduction
                                                                                                          (B). Probes and queries sometimes disagree. We pro-
                                         Text generated by neural language models (LMs)                   pose a taxonomy of different query–probe disagreement
                                                                                                          types (C); across several models and datasets, we find
                                         often contains factual errors (Martindale et al.,
                                                                                                          that disagreements mostly occur in situations where
                                         2019). These errors limit LMs’ ability to gener-                 either probes or queries are uncertain (D).
                                         ate trustworthy content and serve as knowledge
                                         sources in downstream applications (Ji et al., 2023).
                                            Surprisingly, even when LM outputs are factu-                 have consistently been found to be slightly more
                                         ally incorrect, it is sometimes possible to assess               reliable at question answering and fact verification
                                         the truth of statements by probing models’ hidden                than direct queries to LMs (Burns et al., 2022),
                                         states. In the example shown in Fig. 1A, a language              suggesting a mismatch between LMs’ (internal)
                                         model assigns high probability to the incorrect an-              representations of factuality and their (external)
                                         swer yes when prompted to answer the question Is                 expressions of statement probability.
                                         Sting a police officer? However, a linear knowl-                    How should we understand this behavior? One
                                         edge probe trained on the LM’s hidden represen-                  possible interpretation, suggested by several pre-
                                         tations (Fig. 1B) successfully classifies no as the              vious studies, is that it is analogous to “deception”
                                         more likely answer. Knowledge probes of this kind                in human language users (Kadavath et al., 2022;
                                             *
                                                 Equal contribution. Correspondence to scasper@mit.edu.   Azaria and Mitchell, 2023; Zou et al., 2023). In
                                             1
                                                 Code at github.com/lingo-mit/lm-truthfulness.            this framing, if LM representations encode truthful-
ness more reliably than outputs, then mismatches         2       Preliminaries
between LM queries and probes must result from
                                                         Extracting answers from LMs We study autore-
situations in which LMs “know” that a statement is
                                                         gressive LMs that compute a next-token distribu-
untrue and nonetheless assign it high probability.
                                                         tion pLM (xi | x<i ) by first mapping the input x<i
   But knowledge is not a binary phenomenon in           to some hidden representation hLM (x<i ), then us-
LMs or humans. While probes are better than              ing this representation to predict xi . There are two
queries on average, they may not be better on every      standard procedures for answering questions using
example. Moreover, both LMs and probes are prob-         such an LM:
abilistic models: LM predictions can encode uncer-
tainty over possible answers, and this uncertainty           1. Querying: Provide the question q as input
can be decoded from their internal representations              to the LM, and rank answers a (e.g. yes/no)
(Mielke et al., 2022). There are thus a variety of              according to pLM (a | q) (Petroni et al., 2019).
mechanisms that might underlie query–probe dis-
agreement, ranging from differences in calibration           2. Probing: Extract the hidden representa-
to differences in behavior in different input subsets.          tion h([q, a]) from the LM, then use ques-
                                                                tion/answer pairs labeled for correctness (or
   In this paper, we seek to understand mismatches
                                                                unsupervised clustering methods) to train a
between internal and external expressions of truth-
                                                                binary classifier that maps from hLM to a dis-
fulness by understanding the distribution over pre-
                                                                tribution pprobe (correct | h) (Burns et al.,
dictions, taking into account uncertainty in an-
                                                                2022).
swers produced by both queries and probes. In
doing so, we hope to provide a formal ground-            Causes of disagreement Past work has shown
ing of several terms that are widely (but vaguely        that this probing procedure is effective; recent work
and inconsistently) used to describe factual errors      has shown that it often produces different, and
in LMs. LMs and probing techniques are rapidly           slightly better, answers than direct querying (Burns
evolving, so we do not aim to provide a defini-          et al., 2022). Why might this mismatch occur? In
tive answer to the question of why LMs assign            this paper, we define three possible cases:
false statements high probability. However, in a
widely studied probe class, two LMs, and three               1. Model Confabulation (Edwards, 2023): Dis-
question-answering datasets, we identify three qual-            agreements occurring when probe confidence
itatively different reasons that probes may outper-             is low, and the completions from queries are
form queries, which we call confabulation (queries              incorrect (mid-left of Figure 1). In these cases
produce high-confidence answers when probes are                 probes may be slightly more accurate if their
low-confidence), heterogeneity (probes and queries              prediction confidence is better calibrated to
improve performance on different data subsets),                 the probability of correctness. In LMs exhibit-
and (in a small number of instances) what past                  ing confabulation, a large fraction of disagree-
work would characterize as deception (Fig. 1C–D,                ments will occur on inputs with large probe en-
in which queries and probes disagree confidently                tropy Hprobe (correct | (q, a)) and large query
on answer probabilities). Most mismatches occur                 confidence pquery (a | q) for any a.
when probes or queries are uncertain about answers.
By combining probe and query predictions, it is              2. “Deception” (Azaria and Mitchell, 2023),
sometimes possible to obtain better accuracy than               which we define as the set of disagreements
either alone.                                                   in which the probe is confidently correct and
                                                                the query completion is confidently incorrect
   Our results paint a nuanced picture of the repre-
                                                                (upper-left of Figure 1). In these cases, a large
sentation of factuality in LMs: even when probes
                                                                fraction of disagreements will occur on ques-
outperform LMs, they do not explain all of LMs’
                                                                tions to which queries and probes both assign
ability to make factual predictions. Today, many
                                                                high confidence, but to different outputs.2
mismatches between internal and external represen-
tations of factuality appear attributable to different       2
                                                              We use this terminology for consistency with past work,
prediction pathways, rather than an explicit rep-        and do not intend any claims about the presence of specific
                                                         communicative intentions in LMs (q.v. Abercrombie et al.,
resentation of a latent intent to generate outputs       2023; Shanahan, 2022). In humans, deception involves models
“known” to be incorrect.                                 of other agents’ mental states (Mahon, 2008) of a kind that are
  3. Heterogeneity: Disagreements resulting from                                       BoolQ          SciQ           CREAK
                                                                                  GPT-2   GPT-J   GPT-2    GPT-J   GPT-2   GPT-J
     probes and queries exhibiting differential ac-
     curacy on specific input subsets (upper-mid of                     Query     61.8     61.8    76.1    84.1    51.1    50.4
                                                                        Probe     62.9     62.5    78.8    88.6    63.5    71.0
     Figure 1). In these cases, probes may outper-
                                                                       Ensemble    –       62.7    79.7    90.5     –      71.3
     form queries if the subset of inputs on which
     probes are more effective is larger than the                  Table 1: Accuracies of different evaluation approaches.
     (disjoint) subset on which queries are more                   As in past work, we find that probes are consistently
     effective.                                                    more accurate than queries. Surprisingly, by ensembling
                                                                   probes and queries together, it is possible in 4 of 6 cases
  These three categories (along with cases of                      to obtain further improvements.
query–probe agreement, and probe confabulation
and error) are visualized in Fig. 1C. Behaviors may                               BoolQ             SciQ           CREAK
occur simultaneously in a single model: we are ulti-
mately interested in understanding what fraction of
                                                                   Probe
predictions corresponds to each of these categories.

                                                                                                                                   Accuracy
Datasets We evaluate predictions on three
datasets: BoolQ, a dataset of general-topic yes–no
questions derived from search queries (Clark et al.,
                                                                   Query
2019); SciQ, a dataset of crowdsourced multiple-
choice science exam questions, and CREAK, a
dataset of crowdsourced (true and false) factual as-
                                                                                                  Confidence
sertions (Onoe et al., 2021). We evaluate model
behavior on all three datasets via a binary ques-                  Figure 2: Calibration of GPT-J queries and probes. Each
tion answering task. SciQ contains multiple wrong                  point represents a group of predictions: the horizontal
answers for each question; we retain the correct                   axis shows the query’s average confidence Eq,a p(a | q),
                                                                   the vertical axis shows the query’s empirical accuracy
answer and select a single distractor.
                                                                   E[a is correct], and point radius shows the number of
Models As the base LM (and implementation of                       predictions in the group. Probes are substantially better
pquery ), we use the GPT2-XL (Radford et al., 2019)                calibrated than LM queries.
and GPT-J LMs (Wang and Komatsuzaki, 2021).
We query LMs by evaluating the probability they
                                                                   regression objective) to classify (question, answer)
assign to correct answers. In BoolQ and CREAK
                                                                   pairs as correct or incorrect using the training split
we re-normalize their output distributions over the
                                                                   of each dataset described above. The input to this
strings {true, false}; in SciQ we use provided cor-
                                                                   linear model is the LM’s final hidden state in the
rect and incorrect answers.3
                                                                   final layer (we did not find substantial differences
Probes While the space of probe designs is large,                  in probe accuracy using different layers or repre-
many recent studies have used linear probes in                     sentation pooling techniques). As in past work, we
LMs (Hernandez and Andreas, 2021; Ravfogel                         obtain a distribution over answers by normalizing
et al., 2022; Burns et al., 2022; Marks and Tegmark,               over pprobe (correct | q, a). Our main results train
2023).4 We train a linear model (using a logistic                  an ordinary linear model; additional results with a
not exhibited by the LMs we study (Sap et al., 2022). What
                                                                   sparse probing objective (as in e.g. Voita and Titov,
we call “deception” is necessary but insufficient for an LM to     2020) are in Appendix A.
“believe” one thing but choose to say another.
    3
      Just as different behavior may be exhibited by different
models, it may be induced by different prompts or query
                                                                   3     The success of probes over queries can
formats (Lin et al., 2022). We experimented with different               largely be explained by better
query formatting strategies but found no striking changes in             calibration
results. However, future work may more systematically study
the distribution of query–probe disagreements induced by
different prompts.                                                 By evaluating accuracy of probes and queries on
    4
      The probing paradigm has limitations. A successful probe     held-out data, we replicate the finding that probes
does not indicate that the LM necessarily uses the feature being   are more accurate than queries (Table 1). In some
probed for, and an unsuccessful probe does not indicate that
the LM does not use the feature being probed for (Ravichander      cases the difference is small (less than 1% for GPT-
et al., 2020; Elazar et al., 2021; Belinkov, 2022).                J on BoolQ); in other cases, it is substantial (more
                                                                                                              both correct


GPT2-XL
                                                                                                              probe is correct
                                                                                                              query is correct
                                                                                                              both incorrect


                                                                                                           p(query is )
                                                                                                              correct
                                                                                                       1                     1




                                                                                                                                 proportion of preds.
GPT-J                                                                                  p(probe is)
                                                                                             correct
                                                                                                       ½


                                                                                                       0       ½          1 0
            BoolQ                   SciQ                        CREAK                                      LEGEND



Figure 3: Distribution of query and probe predictions. “Deception”-like results (orange) do not feature particularly
prominently compared to other outcomes. Note that heatmaps (left) use the same shade of gray for “both correct”
and “both incorrect”, even though they are distinguished in histograms (right) to enable direct comparison.


than 20% on CREAK).                                        substantially between datasets. In BoolQ and SciQ,
   Another striking difference between probes and          the query is correct and the probe is incorrect nearly
queries is visualized in Fig. 2, which plots the cal-      as often as the opposite case; on both datasets, ex-
ibration of predictions from GPT-J (e.g. when a            amples of highly confident but contradictory pre-
model predicts an answer with 70% probability,             dictions by probes and queries are rare.
is it right 70% of the time?). Probes are well cali-          Fig. 1D shows the fraction of examples in each
brated, while queries are reasonably well calibrated       of the nine categories depicted in Fig. 1C. Only
on SciQ but poorly calibrated on other datasets.           in CREAK do we observe a significant number of
This aligns with the finding by Mielke et al. (2022)       instances of “deception”; however, we also observe
that it is possible to obtain calibrated prediction        many instances of probe errors. In all other cases
of model errors (without assigning probabilities to        (even SciQ, where probes are substantially more
specific answers) using a similar probe.                   accurate than queries), query–probe mismatches
   It is important to emphasize that the main goal         predominantly represent other types of disagree-
of this work is to understand representational cor-        ment.
relates of truthfulness, not to build more accurate
models. Indeed, the superior calibration and accu-         5     Queries and probes are complementary
racy of probes over queries might not seem surpris-        Another observation in Fig. 1 is that almost all
ing given that probes are trained many-shot while          datasets exhibit a substantial portion of heterogene-
queries use the model zero-shot. To contextual-            ity: there are large subsets of the data in which
ize these results, we also finetuned GPT2-XL on            probes have low confidence, but queries assign high
true question/answer pairs and found it performed          probability to the correct answer (and vice-versa).
better overall than probing the pretrained model.             We can exploit this fact by constructing an en-
Probe predictions exhibited 1.7% better accuracy           semble model of the form:
than fine-tuned model queries on BoolQ. However,
querying the fine-tuned model had 6.9% and 4.0%                pensemble (a | q) = λ · pprobe (a | q)
                                                                                                                                 (1)
better accuracy on SciQ and CREAK.                                                  + (1 − λ) · pquery (a | q)

4         Most disagreements result from                     We select λ using 500 validation examples from
          confabulation and heterogeneity                  each dataset, and evaluate accuracy on the test split.
                                                           Results are shown at the bottom of Table 1; in 4/6
Next, we study the joint distribution of query and         cases, this ensemble model is able to improve over
probe predictions. Results are visualized in Fig. 3.       the probe. While improvements on BoolQ and
GPT2-XL and GPT-J exhibit a similar pattern of             CREAK are small, on SciQ they are substantial—
errors on each dataset, but that distribution varies       nearly as large as the improvement of the probe
over the base LM. These results underscore the           errors. However, better understanding of model-
fact that, even when probes significantly outper-        internal representations of factuality and truthful-
form queries, query errors are not the source of         ness might enable system developers to steer mod-
all mismatches, and heterogeneity in probing and         els toward undesirable or harmful behaviors.
querying pathways can be exploited.                         Finally, while we have presented techniques for
                                                         slightly improving the accuracy of models on ques-
6   Conclusion                                           tion answering tasks, models continue to make a
We studied mismatches between language models’           significant number of errors, and are not suitable
factual assertions and probes trained on their inter-    for deployment in applications where factuality and
nal states, and showed that these mismatches reflect     reliability are required.
a diverse set of situations including confabulation,
                                                         Acknowledgments
heterogeneity, and a small number of instances
of deception. In current models, disagreements           This work was supported by a grant from the Open-
between internal and external representations of         Philanthropy foundation.
truthfulness appear predominantly attributable to
different prediction pathways, rather than a latent
intent to produce incorrect output. A variety of         References
other model interventions are known to decrease          Gavin Abercrombie, Amanda Cercas Curry, Tanvi
truthfulness, including carefully designed prompts         Dinkar, and Zeerak Talat. 2023. Mirages: On an-
                                                           thropomorphism in dialogue systems. arXiv preprint
(Lin et al., 2022), and future models may exhibit
                                                           arXiv:2305.09800.
more complex relationships between internal repre-
sentations and generated text (especially for open-      Amanda Askell, Yuntao Bai, Anna Chen, Dawn Drain,
ended generation). Even in these cases, we expect         Deep Ganguli, Tom Henighan, Andy Jones, Nicholas
                                                          Joseph, Ben Mann, Nova DasSarma, et al. 2021. A
the taxonomy in Fig. 1 to remain useful: not all          general language assistant as a laboratory for align-
mismatches between model and probe behavior in-           ment. arXiv preprint arXiv:2112.00861.
volve deception, and not all model behaviors are
                                                         Amos Azaria and Tom Mitchell. 2023. The internal
(currently) reducible to easily decodable properties
                                                          state of an LLM knows when it’s lying. arXiv
of their internal states.                                 preprint arXiv:2304.13734.

7   Limitations                                          Yonatan Belinkov. 2022. Probing classifiers: Promises,
                                                           shortcomings, and advances. Computational Linguis-
As seen in Fig. 1, there is significant heterogeneity      tics, 48(1):207–219.
in the distribution of disagreement types across
                                                         Collin Burns, Haotian Ye, Dan Klein, and Jacob Stein-
datasets. These specific findings may thus not             hardt. 2022. Discovering latent knowledge in lan-
predict the distribution of disagreements in future        guage models without supervision. In The Eleventh
datasets. As noted in Section 2, our experiments           International Conference on Learning Representa-
use only a single prompt template for each experi-         tions.
ment; we believe it is likely (especially in CREAK)      Christopher Clark, Kenton Lee, Ming-Wei Chang,
that better prompts exist that would substantially         Tom Kwiatkowski, Michael Collins, and Kristina
alter the distribution of disagreements—our goal in        Toutanova. 2019. BoolQ: Exploring the surprising
                                                           difficulty of natural yes/no questions. In Proceedings
this work has been to establish a taxonomy of er-
                                                           of the Conference of the North American Chapter of
rors for future models. Finally, we have presented         the Association for Comptuational Linguistics.
only results on linear probes. The success of ensem-
bling methods means that some information must           Benj Edwards. 2023. Why ChatGPT and Bing Chat are
                                                           so good at making things up. Ars Technica.
be encoded non-linearly in model representations.
                                                         Yanai Elazar, Shauli Ravfogel, Alon Jacovi, and Yoav
8   Ethical Considerations                                 Goldberg. 2021. Amnesic probing: Behavioral expla-
                                                           nation with amnesic counterfactuals. Transactions of
Our work is motivated by ethical concerns raised           the Association for Computational Linguistics, 9:160–
in past work (e.g., Askell et al., 2021; Evans et al.,     175.
2021) that LMs might (perhaps unintentionally)           Owain Evans, Owen Cotton-Barratt, Lukas Finnve-
mislead users. The techniques presented here might        den, Adam Bales, Avital Balwit, Peter Wills, Luca
be used to improve model truthfulness or detect           Righetti, and William Saunders. 2021. Truthful AI:
  Developing and governing AI that does not lie. arXiv     Abhilasha Ravichander, Yonatan Belinkov, and Eduard
  preprint arXiv:2110.06674.                                 Hovy. 2020. Probing the probing paradigm: Does
                                                             probing accuracy entail task relevance? In Proceed-
Evan Hernandez and Jacob Andreas. 2021. The low-             ings of the Annual Meeting of the European Associa-
  dimensional linear geometry of contextualized word         tion for Computational Linguistics.
  representations. In Proceedings of the Conference on
  Natural Language Learning.                               Maarten Sap, Ronan Le Bras, Daniel Fried, and Yejin
                                                            Choi. 2022. Neural theory-of-mind? On the limits of
Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan        social intelligence in large lms. In Proceedings of the
  Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea             2022 Conference on Empirical Methods in Natural
  Madotto, and Pascale Fung. 2023. Survey of halluci-       Language Processing.
  nation in natural language generation. ACM Comput-
  ing Surveys, 55(12):1–38.                                Murray Shanahan. 2022. Talking about large language
                                                            models. arXiv preprint arXiv:2212.03551.
Saurav Kadavath, Tom Conerly, Amanda Askell, Tom
  Henighan, Dawn Drain, Ethan Perez, Nicholas              Elena Voita and Ivan Titov. 2020. Information-theoretic
  Schiefer, Zac Hatfield Dodds, Nova DasSarma,                probing with minimum description length. In Pro-
  Eli Tran-Johnson, et al. 2022. Language models              ceedings of the Conference on Empirical Methods in
  (mostly) know what they know. arXiv preprint               Natural Language Processing.
  arXiv:2207.05221.
                                                           Ben Wang and Aran Komatsuzaki. 2021. GPT-J-
Stephanie Lin, Jacob Hilton, and Owain Evans. 2022.          6B: A 6 Billion Parameter Autoregressive Lan-
  TruthfulQA: Measuring how models mimic human               guage Model. https://github.com/kingoflolz/
   falsehoods. In Proceedings of the Annual Meeting of       mesh-transformer-jax.
   the Association for Computational Linguistics.
                                                           Andy Zou, Long Phan, Sarah Chen, James Campbell,
James Edwin Mahon. 2008. The definition of lying and         Phillip Guo, Richard Ren, Alexander Pan, Xuwang
  deception.                                                 Yin, Mantas Mazeika, Ann-Kathrin Dombrowski,
                                                             et al. 2023. Representation engineering: A top-
Samuel Marks and Max Tegmark. 2023. The geometry             down approach to AI transparency. arXiv preprint
  of truth: Emergent linear structure in large language      arXiv:2310.01405.
  model representations of true/false datasets. arXiv
  preprint arXiv:2310.06824.

Marianna Martindale, Marine Carpuat, Kevin Duh, and
 Paul McNamee. 2019. Identifying fluently inade-
 quate output in neural and statistical machine transla-
 tion. In Proceedings of Machine Translation Summit
 XVII: Research Track.

Sabrina J Mielke, Arthur Szlam, Emily Dinan, and Y-
  Lan Boureau. 2022. Reducing conversational agents’
  overconfidence through linguistic calibration. Trans-
  actions of the Association for Computational Linguis-
  tics, 10:857–872.

Yasumasa Onoe, Michael JQ Zhang, Eunsol Choi, and
  Greg Durrett. 2021. CREAK: A dataset for common-
  sense reasoning over entity knowledge. In NeurIPS
  Datasets And Benchmarks.

Fabio Petroni, Tim Rocktäschel, Sebastian Riedel,
  Patrick Lewis, Anton Bakhtin, Yuxiang Wu, and
  Alexander Miller. 2019. Language models as knowl-
  edge bases? In Proceedings of the Conference on
  Empirical Methods in Natural Language Processing.

Alec Radford, Jeffrey Wu, Rewon Child, David Luan,
  Dario Amodei, Ilya Sutskever, et al. 2019. Language
  models are unsupervised multitask learners. OpenAI
  blog, 1(8):9.

Shauli Ravfogel, Michael Twiton, Yoav Goldberg, and
  Ryan D Cotterell. 2022. Linear adversarial concept
  erasure. In Proceedings of the International Confer-
  ence on Machine Learning.
A      Sparse Probing Results

    Accuracy: 63%   Accuracy: 62%   Accuracy: 62%   Accuracy: 62%    Accuracy: 88%   Accuracy: 88%   Accuracy: 87%   Accuracy: 78%
    Sparsity: 53%   Sparsity: 96%   Sparsity: 99%   Sparsity: 99%    Sparsity: 53%   Sparsity: 90%   Sparsity: 95%   Sparsity: 98%




                             (a) BoolQ                                                          (b) SciQ

    Accuracy: 70%   Accuracy: 67%   Accuracy: 60%   Accuracy: 50%
    Sparsity: 53%   Sparsity: 90%   Sparsity: 99%   Sparsity: 100%




                            (c) CREAK

Figure 4: Sparse probing results. In these experiments, we train the same probes as in the main paper, but with a
varying ℓ1 penalty applied to the probing objective to encourage the discovery of sparse solutions. Here we report
the level of sparsity, probe accuracy, and distribution of disagreement types as we vary the strength of the regularizer
within {0, 0.01, 0.03, 0.1}. Except at extremely high sparsity values, both accuracies and error distributions remain
similar to those reported in the main set of experiments.
