---
title: Probing Functional Correctness in Diffusion Language Models (full text)
id: probing-functional-correctness-in-diffusion-language-models-full-text
tags:
- code-llm-confidence-positioning-d82d00
- full-text
created: '2026-11-09T23:28:15.193889Z'
updated: '2026-11-09T23:31:26.487360Z'
source: https://aclanthology.org/2026.acl-srw.15.pdf
status: draft
type: note
content_type: paper
deprecated: false
summary: 'ACL SRW 2026 full text: logistic-regression probes on LLaDA-8B and Dream-7B
  hidden states predict functional correctness (JSON, GSM8K, MBPP, ARC); AUC gains
  0.08-0.11 across denoising on reasoning tasks; offline probe-gated skipping saves
  36-98% compute; no ECE, no causal test.'
---

Probing Functional Correctness in Diffusion Language Models


                                                                                           Guan-Ming Chiu                                         Jeng-Yue Liu
                                                                                       National Taiwan University                           Carnegie Mellon University
                                                                                     gmchiu@arbor.ee.ntu.edu.tw                             buffettl@andrew.cmu.edu




ACL Anthology ID 2026.acl-srw.15 / revision 2 / 21 Oct 2026
                                                                                               Abstract                               models, whose bidirectional, iterative generation
                                                                                                                                      process creates a fundamentally different represen-
                                                                            Diffusion language models generate text by it-
                                                                            eratively denoising all tokens in parallel, but           tational landscape.
                                                                            when and where their hidden states encode                    We address this gap with the first probing study
                                                                            whether the output will be functionally correct           of DLM hidden states. Our contributions are:
                                                                            remains unknown. We present the first probing             (1) DLMs uniquely accumulate correctness sig-
                                                                            study of DLM internals, training linear clas-             nal across iterative denoising, a capacity absent
                                                                            sifiers on hidden states to predict functional
                                                                                                                                      in single-pass AR decoding: while step-0 hidden
                                                                            correctness. Across two models (LLaDA-8B,
                                                                            Dream-7B) and four tasks, we find that DLMs               states already carry above-chance signal compara-
                                                                            uniquely accumulate correctness signal across             ble to an AR probe on the same prompt (and thus
                                                                            denoising steps (AUC gains of 0.08–0.11 on                largely attributable to prompt difficulty rather than
                                                                            reasoning tasks), absent in single-pass AR de-            diffusion), DLMs gain a further 0.08–0.11 AUC
                                                                            coding. However, step-0 signal reflects prompt            through subsequent denoising on reasoning tasks;
                                                                            difficulty rather than diffusion-specific compu-          (2) we identify task-dependent emergence patterns,
                                                                            tation. Signal emergence is task-dependent:
                                                                                                                                      with structural tasks showing flat AUC profiles
                                                                            structural tasks show flat profiles while rea-
                                                                            soning tasks show gradual buildup. The two
                                                                                                                                      from step 0 and reasoning/code tasks requiring
                                                                            models exhibit distinct layer dynamics, with              iterative refinement; and (3) we observe distinct
                                                                            LLaDA concentrating signal in upper layers                layer dynamics between LLaDA and Dream, with
                                                                            while Dream redistributes toward lower lay-               LLaDA concentrating signal in upper layers while
                                                                            ers. We further show that probe confidence can            Dream redistributes signal toward lower layers on
                                                                            identify likely failures, enabling selective gen-         simple tasks. Code and data are available at https:
                                                                            eration that avoids 36–98% of wasted compute.             //github.com/guan404ming/dllm-probing.
                                                                        1   Introduction
                                                                        Diffusion language models (DLMs) have emerged                  2   Background
                                                                        as a promising alternative to autoregressive (AR)
                                                                        generation (Austin et al., 2021a; Sahoo et al., 2024;         Diffusion language models. LLaDA (Nie et al.,
                                                                        Lou et al., 2024). Unlike AR models, which gener-             2025) uses block masking during training and gen-
                                                                        ate tokens sequentially, DLMs produce all output              erates by progressively unmasking tokens over a
                                                                        tokens simultaneously through iterative denoising:            fixed schedule. Dream (Ye et al., 2025) employs a
                                                                        starting from a fully masked or noisy sequence and            global masking schedule with a different unmask-
                                                                        progressively refining it over many steps.                    ing strategy. Both models condition on a fully
                                                                           This parallel generation process raises a funda-           visible prompt and iteratively denoise a generation
                                                                        mental question: when during denoising, and where             region of masked tokens.
                                                                        within the model’s layers, does the network encode
                                                                        whether its output will be functionally correct? In            Probing classifiers. Probing involves training
                                                                        AR models, probing classifiers have revealed how               simple classifiers on frozen model representations
                                                                        linguistic and factual knowledge localizes across              to test whether specific information is encoded (Be-
                                                                        layers and positions (Tenney et al., 2019; Geva                linkov, 2022; Conneau et al., 2018). We adopt this
                                                                        et al., 2023; Azaria and Mitchell, 2023). However,             methodology for DLMs, probing hidden states at
                                                                        no analogous study exists for diffusion language               intermediate denoising steps.

                                                                                                                                 163
                                                              Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop), pages 163–172
                                                                                                     July 2-7, 2026 ©2026 Association for Computational Linguistics
Related work. Prior studies have probed AR               AUC across the same layer-region grid) yield 0.53–
model representations for linguistic structure (Ten-     0.58 across all eight (dataset, model) settings, well
ney et al., 2019), factual knowledge (Geva et al.,       below the actual probe AUCs of 0.65–0.88 (dashed
2023), and truthfulness (Azaria and Mitchell, 2023).     grey trace in Figure 2); the slight offset above 0.50
Confidence-based methods for AR models use               reflects multiple-comparison selection across lay-
early-exit thresholds to skip computation (Schus-        ers and folds, and is uniform across configurations.
ter et al., 2022; Elbayad et al., 2020). Two con-
                                                           Functional correctness. For JSON schema val-
current works study DLM representations from
                                                           idation, an output is correct if it parses as valid
complementary angles. Shnaidman et al. (2026)
                                                           JSON and matches the reference structure. For
demonstrate activation steering for safety behav-
                                                           math reasoning (GSM8K), an output is correct if
iors in masked DLMs, showing that DLM rep-
                                                           the extracted numeric answer matches the ground
resentations are amenable to linear intervention.
                                                           truth. For code generation (MBPP), an output is
Wang et al. (2026) identify temporal oscillation
                                                           correct if the generated function passes all provided
in DLM outputs, where correct answers appear
                                                           test assertions. For science QA (ARC), an output
mid-denoising but are overwritten in later steps.
                                                           is correct if the extracted answer letter matches the
Mündler et al. (2025) propose constrained decod-
                                                           gold label.
ing with context-free grammars to enforce syntac-
tic correctness in DLM outputs; our work instead         Selective generation. We simulate instance-level
asks whether the model’s own representations al-         filtering by training a per-step probe (using the
ready encode whether the output will be correct,         best layer and region from the full analysis). Let p
without external constraints. We complement these        be the probe’s predicted probability of functional
prior findings by probing hidden representations         correctness and define confidence as max(p, 1 −
for functional correctness across the full layer-step    p). At inference time, if the probe predicts p <
grid, characterizing when and where correctness          0.5 with confidence exceeding a threshold τ , we
signal emerges.                                          skip the remaining denoising steps for that instance
                                                         entirely, producing no output rather than wasting
3   Method                                               compute on a generation predicted to be incorrect.
Hidden state extraction. Given a DLM with                We report the fraction of instances filtered and the
L layers, we run 128-step denoising and ex-              probe’s classification accuracy.
tract hidden states at 7 checkpoint steps t ∈
                                                           4   Experimental Setup
{0, 1, 4, 16, 32, 64, 127}. At each checkpoint,
we obtain the full hidden state tensor of shape          Models. We evaluate LLaDA-8B-Instruct (33
(L, gen_length, d). We partition the generation re-      layers) (Nie et al., 2025) and Dream-7B-Instruct
gion into 4 equal-length position regions and mean-      (29 layers) (Ye et al., 2025), two open-weight
pool within each region, yielding features of shape      DLMs with different masking strategies.
(L, 4, d) per instance per step. We choose 4 regions
to align with LLaDA’s block length of 32 tokens          Datasets. We select four tasks spanning
(gen_length / block_length = 4 for JSON schema’s         structural to reasoning-heavy complexity,
128-token blocks) while keeping the number of fea-       testing whether iterative denoising con-
tures manageable given the limited sample sizes.         tributes differently by task type: (1) JSON
An ablation over 1, 2, and 4 regions shows best          schema validation (272 instances from
AUC varies by less than 0.02 across configurations       eth-sri/json-mode-eval-extended,                   an
(Appendix G).                                            extension of NousResearch/json-mode-eval
                                                         that augments the original 100-instance benchmark
Probe training. For each (step, layer, region)           with additional schema variants); each instance
triple, we reduce dimensionality with PCA to 64          pairs a JSON Schema with a natural-language
components, apply standard scaling, and train a          request, and a generation is functional if it parses
logistic regression classifier to predict functional     as JSON and matches the reference structure
correctness (Pedregosa et al., 2011). We evalu-          exactly; (2) GSM8K (1,319 test instances) (Cobbe
ate with 5-fold stratified cross-validation, reporting   et al., 2021), multi-step math reasoning; (3) MBPP
AUC as our primary metric. Control probes trained        (257 sanitized test instances) (Austin et al., 2021b),
on shuffled labels (3 random permutations, max           code generation verified by execution; and (4)




                                                     164
Figure 1: AUC heatmaps (layer × step) for JSON schema and GSM8K. Each cell shows the best AUC across the 4
position regions for that (layer, step) pair. Stars mark the best layer per step. JSON schema shows strong signal
from step 0; GSM8K shows gradual emergence. Note Dream’s layer migration on JSON schema. Per-cell standard
deviations across 5-fold CV are ≤ 0.05. MBPP and ARC heatmaps in Appendix B.


                JSON     GSM8K      MBPP      ARC           denoising-dependent signal: step-0 AUC is ≈ 0.61–
    LLaDA-8B    48.5%     66.3%     40.9%    78.2%          0.67, and signal builds gradually to ≈ 0.71–0.75
    Dream-7B    46.0%     61.5%     44.4%    74.5%          by step 64–127. Dream’s ARC signal is particu-
                                                            larly flat until a sharp jump at the final step (0.61
Table 1: Baseline functional correctness rates (seed=0,     → 0.71), suggesting science reasoning requires
128 denoising steps).
                                                            nearly complete denoising before correctness is
                                                            predictable.
ARC-Challenge (1,172 test instances) (Clark et al.,            All four tasks have above-chance step-0 signal,
2018), multiple-choice science QA with short                but JSON schema gains only ∆AUC ≈ 0.04 from
answers that isolate reasoning from generation              denoising while GSM8K, MBPP, and ARC gain
length. Generation lengths are 256, 512, 256, and           ≈ 0.08–0.11, reflecting the difference between
256 tokens, respectively.                                   structural and reasoning tasks. Standard deviations
                                                            across 5-fold CV are ≤ 0.05 for all configurations,
Baseline functional rates. Table 1 shows the                indicating stable estimates. Because DLMs process
functional correctness rates with 128 denoising             all generation positions jointly via bidirectional at-
steps. All datasets have reasonable class balance,          tention, correctness-relevant information is avail-
enabling meaningful probe training.                         able across the full output region from step 0.
                                                               We also tested whether the probe could select
5     Results
                                                            better random seeds: scoring 5 seeds per instance
5.1    Task-Dependent Emergence                             at step 1 and running full denoising only for the top-
                                                            scoring seed yields +0.0% improvement for both
Figure 1 shows AUC heatmaps for JSON schema
                                                            models on JSON schema, confirming that the step-
and GSM8K (MBPP and ARC in Appendix B).
                                                            0/1 signal reflects instance-level difficulty rather
Two distinct emergence patterns are visible.
                                                            than seed-specific trajectory quality.
   For JSON schema, correctness signal is already
strong at step 0 (AUC ≈ 0.78–0.80 ± 0.04) and
                                                            5.2   Divergent Layer Dynamics
remains relatively flat across all denoising steps.
This indicates that the prompt encoding alone, be-        The heatmaps in Figure 1 reveal distinct layer dy-
fore any denoising occurs, already contains signal        namics between LLaDA and Dream (full per-step
predictive of structural correctness.                     best layers in Table 3, Appendix C).
   For GSM8K, step-0 signal is already well above            LLaDA concentrates its best probing signal con-
chance (AUC ≈ 0.67–0.71 ± 0.03), but denoising            sistently in upper layers (L22–28) across JSON
brings substantially more gain: AUC rises to ≈            schema, GSM8K, and ARC, similar to patterns ob-
0.78–0.82 ± 0.03 by step 127 (Figure 2).                  served in AR transformers. MBPP is an exception,
   MBPP follows the same gradual-buildup pattern          where best layers are more variable (L15–31).
as GSM8K: step-0 AUC is ≈ 0.75–0.76±0.04 and                 Dream shows a task-dependent migration pat-
peaks at ≈ 0.84–0.87 ± 0.05 at later steps (step 64       tern. On JSON schema, the best layer migrates
for LLaDA, step 127 for Dream).                           from the upper range (L17–23 at steps 0–16) to
   ARC-Challenge shows the weakest and most               lower layers (L4–7 at steps 32–127). On GSM8K,




                                                      165
Figure 2: Best AUC across layers at each denoising step (x-axis annotated with cumulative % of generation tokens
unmasked). JSON schema is flat (≈0.80 from step 0), while GSM8K, MBPP, and ARC show gradual emergence.
Dashed grey trace is the shuffled-label control (mean AUC across both models, averaged over 3 random label
permutations); the dotted line marks chance (0.50). Standard deviations across 5-fold CV are ≤ 0.05 for all probe
points.


MBPP, and ARC, however, Dream’s best lay-                                     JSON GSM8K MBPP              ARC
ers remain in the mid-to-upper range (L15–25)               LLaDA-8B
throughout denoising, with no downward migra-                Compute saved 98.4%        61.3%    95.5%    82.9%
                                                             Clf. accuracy 73.5%        73.5%    66.5%    79.6%
tion. We discuss a possible interpretation in terms          Majority acc. 51.5%        66.3%    59.1%    78.2%
of Dream’s AR pretraining origin in §6.
                                                            Dream-7B
                                                             Compute saved 96.7%        36.0%    97.8%    61.4%
5.3   Filtering Hopeless Instances (Offline)                 Clf. accuracy 72.4%        73.5%    70.0%    75.9%
                                                             Majority acc. 54.0%        61.5%    55.6%    74.5%
We evaluate whether per-step probe confidence can
identify instances whose outputs will be incorrect,       Table 2: Filtering simulation (τ = 0.80). Compute
enabling a hypothetical system to skip generation         saved: fraction of denoising steps avoided by skipping
entirely for hopeless instances. This is an offline       instances the probe predicts will fail (no output is pro-
simulation on hidden states already extracted from        duced for skipped instances). Clf. accuracy: fraction of
full 128-step generation, intended to characterize        instances for which the probe correctly predicts func-
the upper bound of what the probe can offer; it does      tional vs. non-functional. Majority acc.: trivial baseline
                                                          that always predicts the majority class. Lift over major-
not account for the cost of running the probe in a
                                                          ity is large for JSON (+19–22%) and MBPP (+7–15%)
live inference loop. Table 2 shows results with a         but only marginal for ARC (+1.4% on Dream).
confidence threshold of τ = 0.80.
   The results are strongly task-dependent. For
JSON schema and MBPP, both models save over
95% of compute and clear the majority baseline            softmax distribution, whose entropy or max prob-
by 7–22 percentage points: the probe is confi-            ability could in principle serve the same role. We
dent from step 0, identifying most instances pre-         re-run the same filtering simulation using two such
dicted to fail immediately. For GSM8K and ARC,            non-probe baselines (mean entropy and mean max-
savings are more modest (36–83%) because rea-             prob over masked positions in the generation re-
soning tasks require more denoising steps before          gion) and a logistic regressor trained on those scalar
the probe can confidently distinguish hopeless in-        features (LR-entropy). Across all eight (dataset,
stances. For ARC, where the baseline functional           model) settings, the probe outperforms the best raw
rate exceeds 74% (Table 1), classification accuracy       signal in classification accuracy at τ = 0.80 by
is only marginally above the majority baseline, in-       5–20 percentage points, and its peak per-step AUC
dicating limited discriminative value on this task.       exceeds LR-entropy by 0.05–0.18 on average (full
                                                          tables in Appendix J). A second control trains a
Comparison to confidence heuristics. A natural            logistic regression directly on output-text features
concern is whether a hidden-state probe is neces-         (length, format markers, and ARC predicted let-
sary at all: the model already exposes a per-token        ter); this shallow probe is also outperformed by




                                                      166
the hidden-state probe in 7 of 8 settings with an         migrate down to L4–7 by step 32, deviating sharply
average AUC gap of 0.12 and a maximum of 0.25             from Qwen-2.5’s range. This pattern is consis-
on GSM8K-Dream (Appendix K).                              tent with the hypothesis that diffusion fine-tuning
                                                          preserves the AR base’s upper-layer hierarchy on
6   Discussion                                            tasks that demand reasoning capacity, but unlocks
                                                          alternative routing to lower layers when the task is
Why does step-0 signal exist? At step 0, the
                                                          structurally simple enough that the inherited hi-
DLM has performed a forward pass over the
                                                          erarchy is no longer load-bearing. We caution
prompt with masked outputs, producing represen-
                                                          that LLaDA’s block-based and Dream’s global lin-
tations that correlate with eventual correctness. For
                                                          ear schedules unmask different positions even at
structural tasks like JSON generation, this correla-
                                                          matched cumulative fractions, so step-axis compar-
tion is strong: the representation already contains
                                                          isons (Figures 1, 2) reflect approximate denoising
signal predictive of correctness. For reasoning and
                                                          progress rather than identical model states.
code tasks, step-0 signal is weaker, and represen-
tations are iteratively refined through denoising.        7   Conclusion
The DLM step-0 signal spans all generation po-
sitions simultaneously, arising from bidirectional      We present the first probing study of DLM internals.
attention over prompt and masked tokens. An AR          Our central finding is that DLMs uniquely accumu-
baseline probe on Qwen-2.5-7B’s last prompt to-         late correctness signal through iterative denoising
ken achieves comparable AUC on most tasks (Ap-          (a 0.08–0.11 AUC gain on reasoning tasks), a ca-
pendix F), suggesting that much of the step-0 signal    pacity absent in single-pass AR decoding. The step-
reflects prompt difficulty detectable by any model.     0 hidden state already carries above-chance signal
On JSON schema, DLM step-0 AUC modestly ex-             (AUC 0.61–0.80), but this is comparable to a probe
ceeds the AR probe (0.78–0.80 vs. 0.74); on other       on an AR model conditioned on the same prompt,
tasks, the gap is negligible (Appendix F, Table 6).     indicating that step-0 signal reflects prompt dif-
The distinctive advantage of DLMs lies not in step-     ficulty rather than diffusion-specific computation.
0 signal strength but in the capacity to gain addi-     We additionally observe task-dependent emergence
tional signal through denoising, a capacity absent      and distinct layer dynamics between LLaDA and
in single-pass AR decoding entirely.                    Dream, and show that an offline filtering simulation
                                                        based on per-step probe confidence avoids 36–98%
Relationship to temporal oscillation. Wang              of wasted compute and outperforms confidence
et al. (2026) observe that DLM outputs can oscillate    heuristics derived from the model’s own softmax
during denoising: correct answers appear at inter-      distribution. Length-stratified controls confirm the
mediate steps but are overwritten later. Our probe      signal is not merely a length confound: AUC drops
measures whether hidden states encode correctness,      by 0.00–0.09 after length matching, with MBPP
not whether the current surface output is correct.      showing no drop at all.
On JSON schema, hidden-state signal is flat from           Future work includes validating filtering in a
step 0 while surface tokens are still being refined,    real inference pipeline (with the probe forward
suggesting that hidden-state signal predictive of       pass costed in), scaling to larger DLMs, and ex-
correctness is established early and oscillation re-    ploring probe-guided adaptive compute allocation.
flects surface-level instability rather than changes    Nonlinear or multi-layer probes may capture richer
in the underlying representation.                       structure.
Layer dynamics and training origin. LLaDA                 Limitations
(trained from scratch) shows stable upper-layer lo-
calization (best layers L22–28 of 33) resembling        Our probe is a simple logistic regression classifier
AR models, while Dream (fine-tuned from Qwen-           with PCA-reduced features; nonlinear probes or
2.5) exhibits layer migration on simple tasks but       multi-layer probes might reveal richer structure.
not complex ones. On GSM8K, MBPP, and ARC,              The selective generation analysis is a simulation on
Dream’s best layers stay in L15–25 (of 29), track-      states from full 128-step generation and does not
ing Qwen-2.5’s own probe best layers, which fall        account for inference overhead of running probes
in L18–27 (of 28) on the same tasks (Appendix F).       in real time. The AUC gain we observe through
On JSON schema, however, Dream’s best layers            denoising (about 0.08–0.11 on reasoning tasks)




                                                    167
cannot be cleanly attributed to diffusion-specific        from a forward pass at each candidate exit step
computation versus generic iterative refinement: a        plus probe evaluation, and would require calibrat-
single-pass AR model has no analogous compari-            ing the threshold τ on a held-out development split
son point, and we do not test multi-pass AR vari-         rather than via cross-validation as we do here.
ants (e.g., self-consistency over multiple samples)
that might also accumulate signal across passes.          Acknowledgements
   We study only two models (LLaDA-8B,                  We thank Modal for the compute credits that sup-
Dream-7B), both discrete masked diffusion LMs,          ported the experiments in this work.
and four tasks. Continuous diffusion LMs (e.g.,
Diffusion-LM, GENIE) operate on continuous em-
bedding spaces with different denoising dynamics          References
and are out of scope for this study; whether our
                                                          Jacob Austin, Daniel D. Johnson, Jonathan Ho, Danny
findings extend to that family is an open question.          Tarlow, and Rianne van den Berg. 2021a. Structured
Broader coverage across discrete masked architec-            denoising diffusion models in discrete state-spaces.
tures (e.g., MDLM, SEDD) and model scales is                 In Advances in Neural Information Processing Sys-
also needed. LLaDA (block-based) and Dream                   tems, volume 34, pages 17981–17993.
(global linear) reach approximately the same cumu-        Jacob Austin, Augustus Odena, Maxwell Nye, Maarten
lative fraction of unmasked tokens at each check-            Bosma, Henryk Michalewski, David Dohan, Ellen
point step (Figures 1, 2 are labeled accordingly),           Jiang, Carrie Cai, Michael Terry, Quoc Le, and
                                                             Charles Sutton. 2021b. Program synthesis with large
but the spatial distribution of unmasked tokens dif-         language models. arXiv preprint arXiv:2108.07732.
fers (LLaDA fills block-by-block, Dream picks
most-confident globally), so cross-model compar-          Amos Azaria and Tom Mitchell. 2023. The internal
isons should be read as approximate denoising-             state of an LLM knows when it’s lying. In Find-
                                                           ings of the Association for Computational Linguis-
progress alignments rather than identical model            tics: EMNLP 2023, pages 967–976.
states. Our interpretation of LLaDA vs. Dream
layer dynamics in terms of training origin (§6) is        Yonatan Belinkov. 2022. Probing classifiers: Promises,
correlational rather than causal: the two models            shortcomings, and advances. Computational Linguis-
                                                            tics, 48(1):207–219.
also differ in pretraining data, tokenizer, and ar-
chitecture, and a controlled fine-tuning ablation         Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot,
(e.g., diffusion fine-tuning the same AR base with          Ashish Sabharwal, Carissa Schoenick, and Oyvind
                                                            Tafjord. 2018. Think you have solved question an-
and without lower-layer routing capacity) would be          swering? try ARC, the AI2 reasoning challenge.
needed to causally establish the role of AR pretrain-       arXiv preprint arXiv:1803.05457.
ing. A length control probe achieves higher AUC
than the correctness probe in most settings (Ap-          Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
                                                            Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
pendix E); after length matching, correctness AUC           Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
drops modestly but remains well above chance.               Nakano, Christopher Hesse, and John Schulman.
Prompt-length-matched probes similarly show only            2021. Training verifiers to solve math word prob-
0.02 average AUC drop (Appendix I). A shallow-              lems. arXiv preprint arXiv:2110.14168.
feature probe trained jointly on output length, for-      Alexis Conneau, German Kruszewski, Guillaume Lam-
mat markers, and ARC predicted letter is outper-            ple, Loïc Barrault, and Marco Baroni. 2018. What
formed by the hidden-state probe in 7 of 8 settings         you can cram into a single $&!#* vector: Probing
(Appendix K); the exception is ARC-Dream where              sentence embeddings for linguistic properties. In
                                                            Proceedings of the 56th Annual Meeting of the As-
the shallow probe narrowly leads, consistent with           sociation for Computational Linguistics (Volume 1:
the marginal probe lift over majority on ARC.               Long Papers), pages 2126–2136.
   Probe selection (best layer and region) uses the
same cross-validation splits as evaluation. A nested      Maha Elbayad, Jiatao Gu, Edouard Grave, and Michael
                                                           Auli. 2020. Depth-adaptive transformer. In Interna-
CV reanalysis (Appendix H) shows AUC drops                 tional Conference on Learning Representations.
by only 0.01 on average (max 0.07), confirming
that the main patterns are not artifacts of selec-        Mor Geva, Jasmijn Bastings, Katja Filippova, and Amir
                                                           Globerson. 2023. Dissecting recall of factual associa-
tion bias. The filtering simulation in §5.3 treats         tions in auto-regressive language models. In Proceed-
the probe as free at inference time; deploying the         ings of the 2023 Conference on Empirical Methods in
same procedure live would incur additional cost            Natural Language Processing, pages 12216–12235.




                                                    168
Aaron Lou, Chenlin Meng, and Stefano Ermon.                   over 128/(gen_length/32) steps per block. Within
  2024. Discrete diffusion modeling by estimating             each block, the model selects the most confident
  the ratios of the data distribution. arXiv preprint
                                                              tokens to unmask at each step. Dream uses a global
  arXiv:2310.16834.
                                                              linear schedule: at step i, the fraction of tokens
Niels Mündler, Jasper Dekoninck, and Martin Vechev.           to unmask is determined by a linearly decreasing
  2025. Constrained decoding of diffusion LLMs                timestep schedule from t = 1 to t = ϵ, and the
  with context-free grammars.       arXiv preprint
  arXiv:2508.10111.                                           most confident masked tokens are unmasked glob-
                                                              ally.
Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang,
  Jingyang Ou, Jun Hu, Jun Zhou, Yankai Lin, Ji-Rong          Prompt construction. For JSON schema, we
  Wen, and Chongxuan Li. 2025. Large language dif-            prepend a system prompt containing the target
  fusion models. arXiv preprint arXiv:2502.09992.             schema and append a JSON code-fence marker
Fabian Pedregosa, Gaël Varoquaux, Alexandre Gram-             as a generation prefix. For GSM8K, the system
  fort, Vincent Michel, Bertrand Thirion, Olivier Grisel,     prompt instructs the model to solve step-by-step
  Mathieu Blondel, Peter Prettenhofer, Ron Weiss, Vin-        and end with #### followed by the numeric answer.
  cent Dubourg, Jake Vanderplas, Alexandre Passos,
                                                              Both models use their respective chat templates. A
  David Cournapeau, Matthieu Brucher, Matthieu Per-
  rot, and Édouard Duchesnay. 2011. Scikit-learn: Ma-         complete prompt example for each task is shown
  chine learning in Python. Journal of Machine Learn-         in Figure 3.
  ing Research, 12:2825–2830.
                                                               JSON schema (LLaDA chat template)
Subham Sekhar Sahoo, Marianne Arriola, Yair Schiff,            [BOS] system\n You are a helpful assistant
  Aaron Gokaslan, Edgar Marroquin, Justin T Chiu,              that answers in JSON. Here’s the JSON schema
  Alexander Rush, and Volodymyr Kuleshov. 2024.                you must adhere to:\n <schema>\n {schema} \n
  Simple and effective masked diffusion language mod-          </schema>\n user\n {user input}\n assistant\n
  els. arXiv preprint arXiv:2406.07524.                        “‘json\n

Tal Schuster, Adam Fisch, Jai Gupta, Mostafa Dehghani,         GSM8K (Dream chat template)
   Dara Bahri, Vinh Q Tran, Yi Tay, and Donald Metzler.        [BOS] im_start system\n Solve the math problem
   2022. Confident adaptive language modeling. In              step by step.     End your answer with ####
  Advances in Neural Information Processing Systems,           followed by the final numeric answer. im_end\n
                                                               im_start user\n {question} im_end\n im_start
  volume 35, pages 17456–17472.
                                                               assistant\n
Adi Shnaidman, Erin Feiglin, Osher Yaari, Efrat Mentel,
  Amit Levi, and Raz Lapid. 2026. Activation steer-         Figure 3: Schematic prompt examples after each
  ing for masked diffusion language models. arXiv           model’s chat template is applied (special tokens shown
  preprint arXiv:2512.24143.                                as plain words for readability; the actual tokens used are
                                                            model-specific control tokens). The generation region
Ian Tenney, Dipanjan Das, and Ellie Pavlick. 2019.          (128–512 masked tokens) is appended after the final as-
   BERT rediscovers the classical NLP pipeline. In
                                                            sistant marker. Both models share the same system/user
   Proceedings of the 57th Annual Meeting of the Asso-
   ciation for Computational Linguistics, pages 4593–       content; only the wrapping tokens differ.
   4601.
Wen Wang, Bozhen Fang, Chenchen Jing, Yongliang             Hidden state extraction. At each of the 7 check-
 Shen, Yangyi Shen, Qiuyu Wang, Hao Ouyang, Hao             point steps {0, 1, 4, 16, 32, 64, 127}, we run a
 Chen, and Chunhua Shen. 2026. Time is a feature:           forward pass with output_hidden_states=True
 Exploiting temporal dynamics in diffusion language         and extract the full hidden state tensor across all
 models. In International Conference on Learning
 Representations.                                           layers. The generation region is partitioned into 4
                                                            equal-length position regions, and we mean-pool
Jiacheng Ye, Zhihui Xie, Lin Zheng, Jiahui Gao, Zirui       within each region, producing a feature vector of
   Wu, Xin Jiang, Zhenguo Li, and Lingpeng Kong.
   2025. Dream 7B: Diffusion large language models.
                                                            dimension d (4096 for LLaDA, 3584 for Dream)
   arXiv preprint arXiv:2508.15487.                         per layer per region per instance.
                                                              Probe pipeline. For each (step, layer, region)
A    Generation and Probing Details
                                                              configuration, we construct the feature matrix X ∈
Denoising procedure. Both models run 128 de-                  Rn×d and apply: (1) StandardScaler (per-feature
noising steps. LLaDA uses block-based unmask-                 zero-mean and unit-variance normalization, with
ing: the generation region is divided into blocks of          mean and variance fitted on the training fold and ap-
32 tokens, and each block is denoised sequentially            plied to the held-out fold), (2) PCA reduction to 64




                                                        169
Figure 4: AUC heatmaps for MBPP and ARC-Challenge. Both show gradual emergence similar to GSM8K. ARC
has the weakest overall signal (AUC ≤ 0.75).


components (also fitted on the training fold), (3) lo-      D   Selective Generation Details
gistic regression with L2 regularization (C = 1.0,
LBFGS solver, max 1000 iterations). We use 5-             The selective generation simulation works as fol-
fold stratified cross-validation (random state 42)        lows. For each instance, we iterate through the
and report the mean AUC across folds.                     checkpoint steps in order. At each step, we com-
                                                          pute the probe’s confidence as max(p, 1−p) where
Computational resources. All generation and               p is the predicted probability of functional correct-
feature extraction use NVIDIA A100 (80GB)                 ness. If the probe confidently predicts failure (con-
GPUs on Modal, with 8 parallel A100s per ex-              fidence exceeds threshold τ and p < 0.5), we skip
periment. Models are loaded in bfloat16 precision.        the remaining denoising steps for that instance, pro-
Probe training runs on CPU. Total compute: ap-            ducing no output. If no checkpoint triggers skip-
proximately 30 A100-hours across all experiments.         ping, the instance proceeds to full generation. Com-
                                                                                             t +1
                                                          pute savings are computed as 1− skip 128 , where tskip
B    Additional Heatmaps                                  is the step at which filtering occurs.
                                                             The main paper reports results at τ = 0.80. Ta-
Figure 4 extends the heatmaps to MBPP and ARC.            ble 4 shows results across a range of thresholds for
Per-model best-layer ranges (LLaDA MBPP L15–              all configurations.
31; ARC L18–28 for both models) confirm that the
JSON-schema downward migration in §5.2 does               Table 4: Selective generation results across thresholds
not occur on these tasks. ARC’s heatmaps are visi-        (%). “Sv” is compute saved by skipping instances pre-
                                                          dicted to fail. “Ac” is classification accuracy.
bly washed out (most cells ≤ 0.65), consistent with
the high majority-class baseline (≥ 74%) limiting           τ      JSON        GSM8K          MBPP          ARC
                                                                  Sv  Ac       Sv Ac         Sv  Ac        Sv  Ac
headroom.
                                                            LLaDA-8B
                                                            0.60 99.2   64.0   83.4   67.2   99.1   63.4   98.6   78.1
C    Best Layer per Step                                    0.70 99.0   69.5   74.2   70.3   98.2   65.8   94.1   79.4
                                                            0.80 98.4   73.5   61.3   73.5   95.5   66.5   82.9   79.6
                                                            0.90 93.3   75.0   34.1   74.2   90.8   68.1   57.0   79.9
Table 3: Best layer (by AUC) at each denoising step.
                                                            Dream-7B
Bold values highlight Dream’s migration to lower layers     0.60 98.8   63.2 85.3 56.9 99.1 72.0           97.2   74.8
on JSON schema. Other tasks show no such migration.         0.70 97.9   69.1 66.3 62.5 98.8 70.0           86.1   75.7
    Step        0    1    4    16   32   64   127           0.80 96.7   72.4 36.0 73.5 97.8 70.0           61.4   75.9
                                                            0.90 87.3   74.6 6.2 74.8 94.9 73.5            24.2   76.8
    JSON Schema
     LLaDA 22       25   26    25   15   25    24
     Dream    17    21   23    19   4    7     5            E   Length Control Probe
    GSM8K                                                 We train a control probe (same pipeline) to predict
     LLaDA     24   24   24    25   28   24    25
     Dream     23   21   21    21   21   21    19         binary output length (above/below median) instead
                                                          of correctness. To control for the confound, we
    MBPP
     LLaDA     15   26   25    24   27   23    31         re-train the correctness probe on a length-matched
     Dream     15   15   24    18   19   25    19         subsample where functional and non-functional in-
    ARC-Challenge                                         stances have identical length distributions (binned
     LLaDA 26 25         25    24   25   25    23         matching, 10 quantile bins).
     Dream    20 20      19    19   19   19    19




                                                      170
Table 5: Best AUC for correctness, length control, and               cross-validation: an inner 3-fold CV on training
length-matched correctness probes. After controlling                 data selects the best (layer, region), and the outer
for length, correctness AUC drops modestly but remains
                                                                     5-fold evaluates on held-out data.
well above chance.
                Corr.     Length       Corr. (matched)           Table 8: AUC drop from nested vs. standard CV. Aver-
     JSON Schema                                                 age drop is 0.01; all qualitative patterns are preserved.
      LLaDA    0.85         0.98            0.81
                                                                                            Avg Drop     Max Drop
      Dream    0.84         0.99            0.75
                                                                                JSON Schema
     GSM8K
                                                                                 LLaDA      0.005             0.050
      LLaDA     0.79        0.86            0.75
                                                                                 Dream      0.035             0.072
      Dream     0.82        0.87            0.80
                                                                                GSM8K
     MBPP
                                                                                 LLaDA        0.009           0.019
      LLaDA     0.84        0.78            0.84
                                                                                 Dream        0.008           0.014
      Dream     0.87        0.80            0.87
                                                                                MBPP
     ARC
                                                                                 LLaDA        0.025           0.053
      LLaDA     0.75        0.96            0.75
                                                                                 Dream        0.021           0.038
      Dream     0.71        0.98            0.72
                                                                                ARC-Challenge
F   AR Baseline Probe                                                            LLaDA      0.002             0.015
                                                                                 Dream      0.005             0.031
We probe Qwen-2.5-7B-Instruct (Dream’s AR base
model) using the last prompt token hidden state.                     I   Prompt Length Control
Sub-A predicts DLM labels; Sub-B uses Qwen’s
                                                                 We re-train correctness probes on subsamples
own greedy outputs.
                                                                 where functional and non-functional instances have
      Table 6: AR vs. DLM step-0 probe AUC.                      matched prompt length distributions (binned match-
                                                                 ing, 10 quantile bins).
                        JSON GSM8K MBPP ARC
 Qwen Sub-A (DLM)       0.74         0.69    0.76       0.67
 Qwen Sub-B (AR)        0.77         0.77    0.69       0.74
                                                                 Table 9: AUC after controlling for prompt length. Aver-
                                                                 age drop is 0.02.
 LLaDA step-0           0.78         0.71    0.76       0.67
 Dream step-0           0.80         0.71    0.76       0.61                       Original    Prompt-matched         Drop
                                                                         JSON Schema
G    Spatial Pooling Ablation                                             LLaDA      0.80              0.75           0.052
                                                                          Dream      0.82              0.80           0.022
We pool the 4 extracted regions into 1 (global av-                       GSM8K
erage), 2 (pairwise average), or 4 (concatenation)                        LLaDA      0.78              0.77           0.015
groups and re-run the probe.                                              Dream      0.82              0.80           0.017
                                                                         MBPP
Table 7: Best AUC by number of position regions.                          LLaDA      0.81              0.86           −0.046
Spread is less than 0.03 within each configuration.                       Dream      0.88              0.85            0.028

                 1 region      2 regions    4 regions                    ARC-Challenge
                                                                          LLaDA      0.73              0.70           0.030
      JSON Schema                                                         Dream      0.71              0.68           0.029
       LLaDA     0.848             0.854      0.840
       Dream     0.846             0.828      0.847
                                                                     J    Entropy / Confidence Baseline
      GSM8K
       LLaDA      0.784            0.788      0.784              For each step we extract masked positions in the
       Dream      0.818            0.814      0.812
                                                                 generation region and compute (a) mean entropy
      MBPP
       LLaDA      0.842            0.860      0.834
                                                                 and (b) mean max-probability, pooled into the same
       Dream      0.864            0.868      0.856              4 spatial regions as the probe. We evaluate three
      ARC-Challenge                                              confidence signals: Raw -entropy (−H pooled
       LLaDA     0.747             0.740      0.744              over regions), Raw maxprob (mean max-prob),
       Dream     0.710             0.711      0.716              and LR-entropy (logistic regression on the 8-dim
                                                                 feature vector, mirroring the probe’s CV pipeline).
H    Nested Cross-Validation
                                                                    Table 10 reports the best per-step AUC across
To verify that probe selection does not inflate re-              checkpoints for each method. The probe out-
ported AUC, we rerun all experiments with nested                 performs the strongest baseline in every (dataset,




                                                               171
model) setting, with an average gap of 0.097 AUC             to the best per-step hidden-state probe.
and a maximum gap of 0.179 on GSM8K-Dream.                      Table 12 summarizes the comparison. The
Table 11 reports filtering performance at τ = 0.80           hidden-state probe outperforms the shallow probe
matching Table 2; the probe achieves higher clas-            in 7 of 8 (dataset, model) settings, with an av-
sification accuracy than every confidence baseline           erage gap of 0.12 AUC and a maximum gap of
on 7 of 8 settings (the exception is JSON-Dream,             0.25 on GSM8K-Dream. The single exception is
where LR-entropy reaches 78.3% but at less than              ARC-Dream (−0.01), consistent with the marginal
half the compute saved).                                     lift over majority baseline already noted for ARC
                                                             in Table 2. On ARC, restricting the shallow probe
Table 10: Best per-step AUC across checkpoints. Probe        to the predicted-letter one-hot alone yields AUC
is the hidden-state logistic regression from §5.3; the       0.640 for LLaDA and 0.681 for Dream, indicating
other three columns use only the model’s softmax distri-
                                                             that the answer letter is a partial but not dominant
bution at each step.
                                                             component of the shallow signal.
               Probe    LR-ent     −H     maxprob
    JSON Schema                                              Table 12: Hidden-state probe vs. shallow-feature probe
     LLaDA 0.846         0.790    0.738     0.746            (logistic regression on output length, format markers,
     Dream    0.827      0.815    0.785     0.798
                                                             and ARC predicted letter). Probe column is the best per-
    GSM8K                                                    step AUC across checkpoints; shallow is mean AUC
     LLaDA     0.785     0.701    0.675     0.667            over 5 folds.
     Dream     0.818     0.639    0.646     0.646
                                                                                 Probe    Shallow     Gap
    MBPP
     LLaDA     0.810     0.730    0.724     0.725                     JSON Schema
     Dream     0.879     0.776    0.749     0.744                      LLaDA 0.846         0.693     +0.15
                                                                       Dream    0.827      0.738     +0.09
    ARC-Challenge
     LLaDA 0.745         0.611    0.623     0.610                     GSM8K
     Dream    0.713      0.588    0.592     0.580                      LLaDA     0.785     0.685     +0.10
                                                                       Dream     0.818     0.567     +0.25

Table 11: Filtering simulation at τ = 0.80, formatted as              MBPP
                                                                       LLaDA     0.810     0.678     +0.13
compute-saved% / accuracy%. Probe column matches                       Dream     0.879     0.673     +0.21
Table 2.
                                                                      ARC-Challenge
            Probe      LR-ent        −H       maxprob                  LLaDA 0.745         0.679     +0.07
JSON Schema                                                            Dream    0.713      0.725     −0.01
 LLaDA 98.4 / 73.5 41.0 / 61.0 80.3 / 52.2 82.1 / 54.4
 Dream 96.7 / 72.4 43.1 / 78.3 85.8 / 50.0 83.1 / 52.2
GSM8K
 LLaDA 61.3 / 73.5 36.7 / 68.8 59.3 / 68.5 66.9 / 66.6
 Dream 36.0 / 73.5 6.3 / 62.2 30.5 / 62.2 31.0 / 62.2
MBPP
 LLaDA 95.5 / 66.5 34.8 / 60.7 78.3 / 48.2 82.4 / 52.9
 Dream 97.8 / 70.0 29.3 / 67.3 87.0 / 52.9 86.6 / 52.1
ARC-Challenge
 LLaDA 82.9 / 79.6 77.1 / 78.0 93.4 / 70.4 96.4 / 68.4
 Dream 61.4 / 75.9 43.5 / 74.3 49.7 / 60.8 67.3 / 51.8

K    Shallow-Feature Control
To test whether the hidden-state probe merely picks
up surface cues, we extract per-task textual fea-
tures from each generation and train a 5-fold cross-
validated logistic regression on them ("shallow
probe"). Features cover output length (charac-
ter/line count), format markers (presence of ex-
pected delimiters such as ####, “‘python, code
fences, JSON parseability, def), and, for ARC,
one-hot indicators of the predicted answer letter
(A/B/C/D). We compare the shallow probe’s AUC




                                                           172
