# Uncertainty Estimation and Confidence in Code Generation: Literature Survey

---

## Theme 1: Foundational Uncertainty Quantification

### 1.1 Semantic Entropy for Natural Language Generation

**Title:** Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation  
**Authors:** Lorenz Kuhn, Yarin Gal, Sebastian Farquhar  
**Year:** 2023  
**Venue:** ICLR 2023 (Spotlight)  
**arXiv:** 2302.09664  

**Key Findings:** Introduces *semantic entropy*, a method that clusters LLM outputs by meaning (bidirectional entailment) rather than surface form, then computes entropy over semantic equivalence classes. This addresses the fundamental problem that token-level or sequence-level entropy conflates linguistic variation with genuine uncertainty. Outperforms all baselines for detecting inaccurate generations across question-answering tasks without requiring model modification or supervised labels.

```bibtex
@inproceedings{kuhn2023semantic,
  author    = {Kuhn, Lorenz and Gal, Yarin and Farquhar, Sebastian},
  title     = {Semantic Uncertainty: Linguistic Invariances for Uncertainty
               Estimation in Natural Language Generation},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  url       = {https://openreview.net/forum?id=VD-AYtP0dve},
  eprint    = {2302.09664},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL}
}
```

### 1.2 Calibration and Correctness of Language Models for Code

**Title:** Calibration and Correctness of Language Models for Code  
**Authors:** Claudio Spiess, David Gros, Kunal Suresh Pai, Michael Pradel, Md Rafiqul Islam Rabin, Amin Alipour, Susmit Jha, Prem Devanbu, Toufique Ahmed  
**Year:** 2024  
**Venue:** ICSE 2025  
**arXiv:** 2402.02047  

**Key Findings:** Establishes a rigorous methodology for studying calibration of code-generating LLMs (GPT-3.5, Codex, CodeGen2-16B) across multiple code tasks. Finds that model confidence (token-level probabilities) is often poorly calibrated for code generation — models can be overconfident on incorrect solutions and underconfident on correct ones. Explores multiple confidence measures and their relationship to functional correctness.

```bibtex
@article{spiess2024calibration,
  author  = {Spiess, Claudio and Gros, David and Pai, Kunal Suresh and
             Pradel, Michael and Rabin, Md Rafiqul Islam and Alipour, Amin
             and Jha, Susmit and Devanbu, Prem and Ahmed, Toufique},
  title   = {Calibration and Correctness of Language Models for Code},
  journal = {arXiv preprint arXiv:2402.02047},
  year    = {2024},
  note    = {Accepted at ICSE 2025},
  url     = {https://arxiv.org/abs/2402.02047}
}
```

### 1.3 Multicalibration for LLM-based Code Generation

**Title:** Multicalibration for LLM-based Code Generation  
**Authors:** Viola Campos, Robin Kuschnereit, Adrian Ulges  
**Year:** 2025  
**Venue:** arXiv (preprint); presented at AI-SQE 2026  
**arXiv:** 2512.08810  

**Key Findings:** Investigates *multicalibration* — calibration that accounts for subgroup structure (problem complexity, code length, programming language) — applied to code generation. Demonstrates improvements of +1.03 in skill score over uncalibrated token likelihoods and +0.37 over standard calibration baselines, evaluated on models including Qwen3 Coder, GPT-OSS, and DeepSeek-R1-Distill.

```bibtex
@article{campos2025multicalibration,
  author  = {Campos, Viola and Kuschnereit, Robin and Ulges, Adrian},
  title   = {Multicalibration for {LLM}-based Code Generation},
  journal = {arXiv preprint arXiv:2512.08810},
  year    = {2025},
  url     = {https://arxiv.org/abs/2512.08810}
}
```

---

## Theme 2: Sampling, pass@k, and Self-Consistency for Code

### 2.1 Codex and the HumanEval Benchmark

**Title:** Evaluating Large Language Models Trained on Code  
**Authors:** Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, Wojciech Zaremba  
**Year:** 2021  
**Venue:** arXiv (preprint)  
**arXiv:** 2107.03374  

**Key Findings:** Introduces Codex (a GPT model fine-tuned on GitHub code) and the HumanEval benchmark (164 hand-written Python problems with unit tests). Defines the **pass@k** metric — the probability that at least one of k samples passes all tests — establishing the foundational framework for sampling-based confidence in code generation. Demonstrates that repeated sampling dramatically boosts solve rates: Codex achieves 28.8% pass@1 but 70.2% pass@100, revealing that test-time compute via sampling is a powerful lever for code correctness.

```bibtex
@article{chen2021codex,
  author  = {Chen, Mark and Tworek, Jerry and Jun, Heewoo and Yuan, Qiming
             and {Ponde de Oliveira Pinto}, Henrique and Kaplan, Jared and
             Edwards, Harri and Burda, Yuri and Joseph, Nicholas and
             Brockman, Greg and Ray, Alex and Puri, Raul and Krueger, Gretchen
             and Petrov, Michael and Khlaaf, Heidy and Sastry, Girish and
             Mishkin, Pamela and Chan, Brooke and Gray, Scott and Ryder, Nick
             and Pavlov, Mikhail and Power, Alethea and Kaiser, Lukasz and
             Bavarian, Mohammad and Winter, Clemens and Tillet, Philippe and
             {Petroski Such}, Felipe and Cummings, Dave and Plappert, Matthias
             and Chantzis, Fotios and Barnes, Elizabeth and Herbert-Voss, Ariel
             and {Hebgen Guss}, William and Nichol, Alex and Paino, Alex and
             Tezak, Nikolas and Tang, Jie and Babuschkin, Igor and Balaji, Suchir
             and Jain, Shantanu and Saunders, William and Hesse, Christopher
             and Carr, Andrew N. and Leike, Jan and Achiam, Josh and
             Misra, Vedant and Morikawa, Evan and Radford, Alec and
             Knight, Matthew and Brundage, Miles and Murati, Mira and
             Mayer, Katie and Welinder, Peter and McGrew, Bob and
             Amodei, Dario and McCandlish, Sam and Sutskever, Ilya and
             Zaremba, Wojciech},
  title   = {Evaluating Large Language Models Trained on Code},
  journal = {arXiv preprint arXiv:2107.03374},
  year    = {2021},
  url     = {https://arxiv.org/abs/2107.03374}
}
```

### 2.2 AlphaCode: Massive Sampling and Filtering

**Title:** Competition-Level Code Generation with AlphaCode  
**Authors:** Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d'Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, Oriol Vinyals  
**Year:** 2022  
**Venue:** Science, Vol. 378, No. 6624, pp. 1092–1097  
**DOI:** 10.1126/science.abq1158  

**Key Findings:** Generates up to ~1 million candidate programs per problem, then uses filtering (against example tests) and clustering to select a small number of submissions. This massive sample-then-filter pipeline is an implicit confidence mechanism — diversity of solutions combined with execution-based filtering acts as a proxy for correctness confidence. Achieves estimated human-median performance on Codeforces competitive programming problems, demonstrating that scale of sampling combined with intelligent selection can substitute for single-pass accuracy.

```bibtex
@article{li2022alphacode,
  author  = {Li, Yujia and Choi, David and Chung, Junyoung and Kushman, Nate
             and Schrittwieser, Julian and Leblond, R{\'e}mi and Eccles, Tom
             and Keeling, James and Gimeno, Felix and {Dal Lago}, Agustin
             and Hubert, Thomas and Choy, Peter and {de Masson d'Autume}, Cyprien
             and Babuschkin, Igor and Chen, Xinyun and Huang, Po-Sen
             and Welbl, Johannes and Gowal, Sven and Cherepanov, Alexey
             and Molloy, James and Mankowitz, Daniel J. and Robson, Esme Sutherland
             and Kohli, Pushmeet and {de Freitas}, Nando and Kavukcuoglu, Koray
             and Vinyals, Oriol},
  title   = {Competition-Level Code Generation with {AlphaCode}},
  journal = {Science},
  volume  = {378},
  number  = {6624},
  pages   = {1092--1097},
  year    = {2022},
  doi     = {10.1126/science.abq1158}
}
```

### 2.3 Adaptive Temperature Sampling for Code

**Title:** Hot or Cold? Adaptive Temperature Sampling for Code Generation with Large Language Models  
**Authors:** Yuqi Zhu, Jia Li, Ge Li, Yunfei Zhao, Zhi Jin, Hong Mei  
**Year:** 2024  
**Venue:** AAAI 2024, Vol. 38, No. 1, pp. 277–285  
**DOI:** 10.1609/aaai.v38i1.27798  

**Key Findings:** Proposes AdapT (Adaptive Temperature), which dynamically adjusts the sampling temperature on a per-token basis during code generation. Shows that fixed temperature is suboptimal — different tokens benefit from different exploration/exploitation trade-offs. Improves pass@k metrics (pass@5, pass@10, pass@15) on HumanEval and MBPP, demonstrating that smarter sampling directly improves the confidence-coverage trade-off.

```bibtex
@inproceedings{zhu2024hot,
  author    = {Zhu, Yuqi and Li, Jia and Li, Ge and Zhao, Yunfei
               and Jin, Zhi and Mei, Hong},
  title     = {Hot or Cold? {Adaptive} Temperature Sampling for Code
               Generation with Large Language Models},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {38},
  number    = {1},
  pages     = {277--285},
  year      = {2024},
  doi       = {10.1609/aaai.v38i1.27798}
}
```

### 2.4 Multi-Perspective Self-Consistency (MPSC)

**Title:** Enhancing Large Language Models in Coding Through Multi-Perspective Self-Consistency  
**Authors:** Baizhou Huang, Shuai Lu, Weizhu Chen, Xiaojun Wan, Nan Duan  
**Year:** 2023  
**Venue:** arXiv (preprint)  
**arXiv:** 2309.17272  

**Key Findings:** Extends self-consistency voting to code generation by sampling across multiple "perspectives" (e.g., code, natural language explanations, test cases) and building multipartite graphs to aggregate inter- and intra-consistency signals. Goes beyond simple majority voting by capturing structural relationships between solutions, improving reliability via multi-modal consensus on diverse outputs.

```bibtex
@article{huang2023mpsc,
  author  = {Huang, Baizhou and Lu, Shuai and Chen, Weizhu
             and Wan, Xiaojun and Duan, Nan},
  title   = {Enhancing Large Language Models in Coding Through
             Multi-Perspective Self-Consistency},
  journal = {arXiv preprint arXiv:2309.17272},
  year    = {2023},
  url     = {https://arxiv.org/abs/2309.17272}
}
```

---

## Theme 3: Execution-Based Verification and Code Ranking

### 3.1 CodeT: Code Generation with Generated Tests

**Title:** CodeT: Code Generation with Generated Tests  
**Authors:** Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, Weizhu Chen  
**Year:** 2023  
**Venue:** ICLR 2023  
**arXiv:** 2207.10397  

**Key Findings:** Proposes a dual execution agreement framework: the LLM generates both code solutions and test cases, then solutions are ranked by (a) consistency with generated tests and (b) agreement with other candidate solutions. Achieves 65.8% pass@1 on HumanEval — an 18.8 absolute point improvement over code-davinci-002 — establishing that execution-based self-verification is a powerful confidence signal. The key insight is that mutual agreement between independently generated code and tests provides a stronger correctness proxy than model probabilities alone.

```bibtex
@inproceedings{chen2023codet,
  author    = {Chen, Bei and Zhang, Fengji and Nguyen, Anh and Zan, Daoguang
               and Lin, Zeqi and Lou, Jian-Guang and Chen, Weizhu},
  title     = {{CodeT}: Code Generation with Generated Tests},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  eprint    = {2207.10397},
  archiveprefix = {arXiv},
  primaryclass  = {cs.SE},
  url       = {https://arxiv.org/abs/2207.10397}
}
```

### 3.2 LEVER: Learning to Verify with Execution

**Title:** LEVER: Learning to Verify Language-to-Code Generation with Execution  
**Authors:** Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-tau Yih, Sida I. Wang, Xi Victoria Lin  
**Year:** 2023  
**Venue:** ICML 2023 (PMLR Vol. 202, pp. 26106–26128)  

**Key Findings:** Trains a learned verifier that takes as input the natural language specification, generated code, and execution results to produce a confidence score for each candidate program. Unlike CodeT which relies on heuristic agreement, LEVER learns to discriminate correct from incorrect programs using execution traces as features. Demonstrates consistent improvements across multiple code generation models and benchmarks, showing that execution-grounded verification outperforms both model-probability-based and test-agreement-based ranking.

```bibtex
@inproceedings{ni2023lever,
  author    = {Ni, Ansong and Iyer, Srini and Radev, Dragomir
               and Stoyanov, Veselin and Yih, Wen-tau and Wang, Sida I.
               and Lin, Xi Victoria},
  title     = {{LEVER}: Learning to Verify Language-to-Code Generation
               with Execution},
  booktitle = {International Conference on Machine Learning (ICML)},
  volume    = {202},
  pages     = {26106--26128},
  year      = {2023},
  publisher = {PMLR},
  url       = {https://proceedings.mlr.press/v202/ni23b.html}
}
```

### 3.3 Fault-Aware Neural Code Rankers

**Title:** Fault-Aware Neural Code Rankers  
**Authors:** Jeevana Priya Inala, Chenglong Wang, Mei Yang, Andres Codas, Mark Encarnación, Shuvendu K. Lahiri, Madanlal Musuvathi, Jianfeng Gao  
**Year:** 2022  
**Venue:** NeurIPS 2022  
**arXiv:** 2206.03865  

**Key Findings:** Proposes CodeRanker, a neural model trained to distinguish between correct programs and programs with specific failure modes (wrong output, runtime error, compilation error). By making the ranker *fault-aware* — conditioning on error types rather than just binary correct/incorrect — the system learns more discriminative features. Demonstrates significant improvements in selecting correct solutions from candidate pools on code generation benchmarks.

```bibtex
@inproceedings{inala2022coderanker,
  author    = {Inala, Jeevana Priya and Wang, Chenglong and Yang, Mei
               and Codas, Andres and Encarnaci{\'o}n, Mark
               and Lahiri, Shuvendu K. and Musuvathi, Madanlal
               and Gao, Jianfeng},
  title     = {Fault-Aware Neural Code Rankers},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {35},
  year      = {2022},
  url       = {https://arxiv.org/abs/2206.03865}
}
```

### 3.4 Coder Reviewer Reranking

**Title:** Coder Reviewer Reranking for Code Generation  
**Authors:** Tianyi Zhang, Tao Yu, Tatsunori B. Hashimoto, Mike Lewis, Wen-tau Yih, Daniel Fried, Sida I. Wang  
**Year:** 2023  
**Venue:** arXiv (preprint)  
**arXiv:** 2211.16490  

**Key Findings:** Introduces a *coder-reviewer* framework where the "coder" generates code from a natural language specification, and the "reviewer" scores code by computing the probability of regenerating the specification from the code (a reverse-direction likelihood). This bidirectional scoring provides a more robust confidence estimate than forward probability alone. Achieves up to 17% absolute accuracy improvement over coder-only reranking across six datasets and eight models from three model families.

```bibtex
@article{zhang2023coder,
  author  = {Zhang, Tianyi and Yu, Tao and Hashimoto, Tatsunori B.
             and Lewis, Mike and Yih, Wen-tau and Fried, Daniel
             and Wang, Sida I.},
  title   = {Coder Reviewer Reranking for Code Generation},
  journal = {arXiv preprint arXiv:2211.16490},
  year    = {2023},
  url     = {https://arxiv.org/abs/2211.16490}
}
```

---

## Theme 4: Self-Repair, Reflexion, and Test-Time Compute

### 4.1 Is Self-Repair a Silver Bullet for Code Generation?

**Title:** Is Self-Repair a Silver Bullet for Code Generation?  
**Authors:** Theo X. Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao, Armando Solar-Lezama  
**Year:** 2024  
**Venue:** ICLR 2024  
**arXiv:** 2310.07524  

**Key Findings:** Provides a rigorous analysis of when LLM self-repair works for code generation. Introduces the **pass@t** metric for fair comparison of repair-based approaches against sampling baselines under equal compute budgets. Finds that self-repair's effectiveness is bottlenecked by feedback quality — using stronger models for the feedback/diagnosis stage significantly improves repair success. Crucially, self-repair with GPT-3.5 feedback barely helps, while GPT-4 feedback makes a substantial difference, suggesting that *knowing what's wrong* (uncertainty about the error) is harder than *fixing it*.

```bibtex
@inproceedings{olausson2024selfrepair,
  author    = {Olausson, Theo X. and Inala, Jeevana Priya
               and Wang, Chenglong and Gao, Jianfeng
               and Solar-Lezama, Armando},
  title     = {Is Self-Repair a Silver Bullet for Code Generation?},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024},
  url       = {https://openreview.net/forum?id=y0GJXRungR},
  eprint    = {2310.07524},
  archiveprefix = {arXiv},
  primaryclass  = {cs.SE}
}
```

### 4.2 Reflexion: Verbal Reinforcement Learning

**Title:** Reflexion: Language Agents with Verbal Reinforcement Learning  
**Authors:** Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao  
**Year:** 2023  
**Venue:** NeurIPS 2023  
**arXiv:** 2303.11366  

**Key Findings:** Proposes a framework where a language agent reflects on execution failures in natural language, stores these reflections in an episodic memory buffer, and uses them to improve subsequent attempts. On HumanEval, achieves 91% pass@1 (surpassing GPT-4's 80% at the time) through iterative self-reflection. The key architectural insight is the separation into Actor, Evaluator, and Self-Reflection modules — the agent builds an explicit model of what went wrong (its uncertainty about the solution) and uses verbal reasoning to address it.

```bibtex
@inproceedings{shinn2023reflexion,
  author    = {Shinn, Noah and Cassano, Federico and Berman, Edward
               and Gopinath, Ashwin and Narasimhan, Karthik and Yao, Shunyu},
  title     = {Reflexion: Language Agents with Verbal Reinforcement Learning},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {36},
  year      = {2023},
  eprint    = {2303.11366},
  archiveprefix = {arXiv},
  primaryclass  = {cs.AI}
}
```

### 4.3 RethinkMCTS: Monte Carlo Tree Search for Code

**Title:** RethinkMCTS: Refining Erroneous Thoughts in Monte Carlo Tree Search for Code Generation  
**Authors:** Qingyao Li, Wei Xia, Kounianhua Du, Xinyi Dai, Ruiming Tang, Yasheng Wang, Yong Yu, Weinan Zhang  
**Year:** 2025  
**Venue:** EMNLP 2025  
**arXiv:** 2409.09584  

**Key Findings:** Applies Monte Carlo Tree Search (MCTS) to code generation, where each node represents a reasoning step (rationale) before code is generated. Includes a refinement mechanism that identifies and corrects erroneous reasoning paths rather than discarding them. Boosts GPT-3.5-turbo pass@1 from 70.12% to 89.02% on HumanEval, demonstrating that structured search over reasoning steps — with explicit uncertainty about which reasoning path is correct — dramatically improves code generation quality.

```bibtex
@inproceedings{li2025rethinkmcts,
  author    = {Li, Qingyao and Xia, Wei and Du, Kounianhua and Dai, Xinyi
               and Tang, Ruiming and Wang, Yasheng and Yu, Yong
               and Zhang, Weinan},
  title     = {{RethinkMCTS}: Refining Erroneous Thoughts in {Monte Carlo}
               Tree Search for Code Generation},
  booktitle = {Proceedings of the 2025 Conference on Empirical Methods
               in Natural Language Processing (EMNLP)},
  year      = {2025},
  eprint    = {2409.09584},
  archiveprefix = {arXiv},
  primaryclass  = {cs.SE}
}
```

### 4.4 S*: Hybrid Test-Time Scaling for Code

**Title:** S*: Test Time Scaling for Code Generation  
**Authors:** Delong Chen, Jiarui Liu, Yifu Wang, Xianfang Zeng, Hailong Sun  
**Year:** 2025  
**Venue:** EMNLP 2025 Findings  
**arXiv:** 2502.14382  

**Key Findings:** Proposes the first hybrid test-time scaling framework that combines *parallel scaling* (generating many candidates) with *sequential scaling* (iterative refinement). Introduces adaptive distinguishing input generation for pairwise comparison of candidate solutions. Enables 3B-parameter models to outperform GPT-4o-mini; DeepSeek-R1-Distill-Qwen-32B with S* achieves 85.7% on LiveCodeBench. Demonstrates that intelligent allocation of test-time compute — deciding when to sample more vs. when to refine — is crucial for maximizing code correctness per compute dollar.

```bibtex
@inproceedings{chen2025sstar,
  author    = {Chen, Delong and Liu, Jiarui and Wang, Yifu
               and Zeng, Xianfang and Sun, Hailong},
  title     = {{S*}: Test Time Scaling for Code Generation},
  booktitle = {Findings of the Association for Computational Linguistics:
               EMNLP 2025},
  year      = {2025},
  eprint    = {2502.14382},
  archiveprefix = {arXiv},
  primaryclass  = {cs.SE}
}
```

---

## Theme 5: Communicating Uncertainty to Developers

### 5.1 Uncertainty Highlighting in AI Code Completions

**Title:** Generation Probabilities Are Not Enough: Uncertainty Highlighting in AI Code Completions  
**Authors:** Helena Vasconcelos, Gagan Bansal, Adam Fourney, Q. Vera Liao, Jennifer Wortman Vaughan  
**Year:** 2024  
**Venue:** ACM Transactions on Computer-Human Interaction (TOCHI)  
**DOI:** 10.1145/3702320  

**Key Findings:** Studies how to effectively communicate uncertainty in AI code completion tools to developers. Finds that highlighting tokens with the highest predicted likelihood of being edited (a proxy for model uncertainty) leads to faster task completion and is subjectively preferred by programmers over raw probability displays. Programmers prefer granular, informative, and interpretable uncertainty highlights without overwhelming detail — establishing design principles for human-AI interaction in code generation under uncertainty.

```bibtex
@article{vasconcelos2024generation,
  author  = {Vasconcelos, Helena and Bansal, Gagan and Fourney, Adam
             and Liao, Q. Vera and {Wortman Vaughan}, Jennifer},
  title   = {Generation Probabilities Are Not Enough: Uncertainty
             Highlighting in {AI} Code Completions},
  journal = {ACM Transactions on Computer-Human Interaction},
  year    = {2024},
  doi     = {10.1145/3702320}
}
```

---

## Theme 6: Fine-Grained Confidence and Token-Level Uncertainty for Code

### 6.1 Fine-Grained Confidence Calibration for Code Revision

**Title:** Fine-grained Approaches for Confidence Calibration of LLMs in Automated Code Revision  
**Authors:** Hong Yi Lin, Chunhua Liu, Haoyu Gao, Patanamon Thongtanunam, Christoph Treude  
**Year:** 2026  
**Venue:** arXiv (preprint)  
**arXiv:** 2604.06723  

**Key Findings:** Proposes fine-grained confidence scores (minimum token probability, lowest-K token probability, attention-weighted uncertainty) combined with local Platt-scaling for better calibration in code revision tasks. Shows that fine-grained, token-level approaches consistently achieve lower calibration error than sequence-level confidence scores across program repair, vulnerability repair, and code refinement — demonstrating that where the model is uncertain within a code snippet matters more than aggregate confidence.

```bibtex
@article{lin2026finegrained,
  author  = {Lin, Hong Yi and Liu, Chunhua and Gao, Haoyu
             and Thongtanunam, Patanamon and Treude, Christoph},
  title   = {Fine-grained Approaches for Confidence Calibration of
             {LLMs} in Automated Code Revision},
  journal = {arXiv preprint arXiv:2604.06723},
  year    = {2026},
  url     = {https://arxiv.org/abs/2604.06723}
}
```

### 6.2 Uncertainty-Guided Chain-of-Thought for Code Generation

**Title:** Uncertainty-Guided Chain-of-Thought for Code Generation with LLMs  
**Authors:** (UnCert-CoT team)  
**Year:** 2025  
**Venue:** arXiv (preprint)  
**arXiv:** 2503.15341  

**Key Findings:** Uses entropy and probability differential as token-level uncertainty signals to selectively trigger chain-of-thought (CoT) reasoning only for high-uncertainty code lines. By avoiding CoT on simple/confident code regions and focusing reasoning on uncertain regions, it improves both efficiency and accuracy. Demonstrates that uncertainty-aware selective reasoning is more effective than blanket CoT application — the model should "think harder" only where it is uncertain.

```bibtex
@article{uncertcot2025,
  title   = {Uncertainty-Guided Chain-of-Thought for Code Generation
             with {LLMs}},
  journal = {arXiv preprint arXiv:2503.15341},
  year    = {2025},
  url     = {https://arxiv.org/abs/2503.15341}
}
```

---

## Cross-Cutting Synthesis

### Key Themes and Relationships

**1. The Hierarchy of Uncertainty Signals for Code:**
Token-level probabilities (Spiess et al., Lin et al.) → sequence-level scores (Coder-Reviewer) → semantic equivalence classes (Kuhn et al.) → execution-based signals (CodeT, LEVER). The literature shows a clear progression: execution-based verification provides the strongest confidence signal for code, since code correctness is ultimately defined by behavior, not syntax.

**2. Sampling as Implicit Uncertainty Estimation:**
The pass@k framework (Chen et al. 2021) and AlphaCode's massive sampling approach (Li et al. 2022) treat the fraction of correct samples as an implicit confidence measure. This connects to self-consistency (Huang et al. 2023) and is refined by adaptive sampling (Zhu et al. 2024) and intelligent selection (CodeT, LEVER, CodeRanker).

**3. Test-Time Compute Allocation Under Uncertainty:**
S* (Chen et al. 2025), RethinkMCTS (Li et al. 2025), and Reflexion (Shinn et al. 2023) all address the question: *given a compute budget, how should we allocate it to maximize confidence in the output?* The answer emerging from this literature is hybrid approaches — sample broadly for easy problems, refine iteratively for hard ones — guided by uncertainty signals.

**4. The Human in the Loop:**
Vasconcelos et al. (2024) stands as the key work on *communicating* model uncertainty to developers, finding that edit-likelihood highlighting outperforms raw probability displays. This is a critical bridge between technical uncertainty quantification and practical developer trust in AI-generated code.

**5. Calibration Gap:**
Spiess et al. (2024) and Campos et al. (2025) demonstrate that LLM confidence scores are poorly calibrated for code — a fundamental problem that undermines all approaches relying on model probabilities. This motivates execution-based methods (CodeT, LEVER) and post-hoc calibration techniques (multicalibration, Platt scaling).
