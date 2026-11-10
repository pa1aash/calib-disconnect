# Synthesis plan

## Core thesis
The headline "hidden states know code correctness better than the model says" is OCCUPIED on code (Ribeiro et al., ICSE 2026), and its uncontrolled form is probably inflated by supervision asymmetry, reference-versus-other-model provenance, and between-problem difficulty. The strongest defensible TMLR contribution is one execution-graded measurement paper whose headline is a controlled test (probe versus supervision-matched own readouts, including trained stated confidence, versus input-only baselines, scored pooled and within problem on self-generated code), built on an L1 sensitivity protocol and carrying an L3 offline routing replay as secondary analysis; F is used vocabulary, L4 and `src/v4_dprc` stay out.

## Strongest argumentative beats
1. **Pooled AUROC on code is a difficulty measurement** (Drafts A and C; Bulut Eq. 1; Campos Table V; Tuerlings one generation per problem). Load-bearing for why the controlled test is the contribution.
2. **The occupant's design confounds** (Draft A, probe-confound locus): fitted probe versus zero-shot verbal; human reference versus other-model failures; likelihood at 5 to 6% against 25% chance on BigCodeBench. Engage Ribeiro RQ2, which ranks own samples within task (Critic B).
3. **Trained stated confidence is now a concrete threat** (Draft B plus CREDO): code AUROC 0.690 to 0.850 after training, no probe arm. The paper must include a trained own-readout arm; if it closes the gap, that is the finding.
4. **Four switches** (Draft C): concurrent window, instrument-gap exposure, A21 code-reason acceptance, controlled-test outcome. Only the controlled test stays NARROW under every setting.
5. **Claims-reduced framing fits TMLR** (Draft B): evidence criterion is primary; incorrect novelty claims are grounds for rejection; write novelty as "we found no prior code study that ..." with named gaps.
6. **F is used, not unused or contested** (all drafts): every proposed quantity maps to Yates, Murphy, grouping loss, meta-I.
7. **L3 routing is bounded by readout quality** (comparisons Tension 5; Give-Up 0.3 to 0.55 rank-correlation break-even, pass rate above about 0.1).

## Section structure
The 10 required headings from research/prompt-decomposition.json, verbatim and in order.

## Per-section commitments
### 1. Scope, instruments, and verdict rules
- Instruments that failed (arXiv full text, OpenAlex budget, Semantic Scholar keyword) and why every CLEAN is provisional; verdict definitions; concurrency window as an operator proposal.
### 2. L1
- Comparison OCCUPIED (union) by published works alone (Ribeiro plus NeuroSym-Cal; Conflict 6); protocol NARROW; Q10 and Q13 CLEAN (provisional). Source tensions: label adequacy assumed, never tested.
### 3. L2
- Uncontrolled headline OCCUPIED; controlled test NARROW (Conflict 2); Q2a NARROW (2610.11300 and 2510.02917 found base-instruct on code; revises the earlier CLEAN); Q11 NARROW via CREDO (Conflict 1); pivot criteria 1 to 4 evaluated explicitly. Engage Draft B's strict reading as the main objection. Tensions 1 and 2 of comparisons.md.
### 4. L3
- Routing NARROW; update-after-failure CLEAN (provisional); selective prediction OCCUPIED (CodeRefuser, concurrent); repository agents OCCUPIED (Kaddour). Tension 5.
### 5. L4
- Line-level OCCUPIED (Gros and Devanbu, probes on the generator's own states, Table 4 four families; Conflict 5); per-test-group NARROW; test adequacy CLEAN (provisional); recommend v4_dprc stays out.
### 6. F
- OCCUPIED as framing; status "used"; exposition only. Tension 4.
### 7. Close occupants
- Compact table of the 10 to 15 closest occupants with status tags (A23), what each leaves open, linking dossiers by arXiv id. Include CREDO.
### 8. Verdict table
- One table per candidate, matching research/positioning/w4/VERDICTS.md as amended by synthesis-conflicts.md. Note concurrency sensitivity.
### 9. Ranked recommendation for TMLR
- Rank 1: controlled test plus L1 layer plus L3 replay (contribution sentence, evidence needs, TMLR fit on both criteria, main risk). Rank 2: L1 label-oracle and estimator protocol alone (fallback if the controlled test is scooped). Rank 3: L3 update-after-failing-test probe as a small add-on. Rank 4: L4 (out). F: framing only. Apply L2 pivot criteria explicitly; state v4_dprc does not belong.
### 10. Instrument gaps
- Every gap with the verdicts it weakens and the operator action that would close it.

## Where drafts disagreed
- Draft B's strict OCCUPIED readings versus A and C's NARROW: **commit to NARROW** for Q1c, Q2b, L3 routing (Conflicts 2 and 7), but give B's objections a dedicated paragraph each.
- Expected size of the controlled gap: **commit to "small and model-dependent"** (Conflict 3).
- L2 Q11: **commit to NARROW** with CREDO (Conflict 1).

## Length target
- response_format: argumentative. Pass 1 about 9,000 words; pass 2 final about 7,500 words.
