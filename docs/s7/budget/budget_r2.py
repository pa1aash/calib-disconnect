"""Wave 7 GPU-hour budget for design R2 (planning arithmetic, not measurements).

Recomputes the R1 section 12 table for the rebalanced model matrix (design R2 section 3)
at k = 10 and at k = 20 (the pre-registered k rule). Throughputs are the R1 planning
assumptions, with a 12B row interpolated between 8B and 14B. Run: python3 -I budget_r2.py
"""
import json, sys

N_LV, N_LCB, N_LCB_RECON = 542, 1055, 1055
TOK_GEN = {"lv": 200, "lcb": 400, "base": 400, "think": 6000}
TOK_FWD = {"std": 900, "think": 6900, "think_recon": 7000}
DEC = {"8B": 4000, "12B": 3000, "14B": 2500, "32B": 1000}       # vLLM decode tok/s
PRE = {"8B": 15000, "12B": 10000, "14B": 8000, "32B": 3500}     # prefill with capture tok/s
LORA = {sz: 0.77 * v for sz, v in PRE.items()}                   # elicitation-only LoRA
LORA_FULL_8B, ADAPT_GEN_8B = 5000, 2800
OVH, OVH_FULL = 1.2, 1.1

PRIMARY = {"Qwen3-8B": "8B", "Olmo-3-7B-Instruct": "8B", "gemma-4-12B-it": "12B",
           "Qwen3-14B": "14B", "Olmo-3.1-32B-Instruct": "32B", "gemma-4-31B-it": "32B"}
CODER_INSTRUCT = {"Qwen2.5-Coder-7B-Instruct": "8B", "Qwen2.5-Coder-32B-Instruct": "32B"}
BASES = {"Qwen3-8B-Base": "8B", "Olmo-3-1025-7B": "8B", "gemma-4-12B": "12B", "Qwen3-14B-Base": "14B",
         "Olmo-3-1125-32B": "32B", "gemma-4-31B": "32B", "Qwen2.5-Coder-7B": "8B", "Qwen2.5-Coder-32B": "32B"}
TRAJ = {"Olmo-3-7B-Instruct-SFT": "8B", "Olmo-3-7B-Instruct-DPO": "8B"}


def budget(k):
    rows = []
    add = lambda stage, arith, n, h: rows.append({"stage": stage, "arithmetic": arith, "conditions": n, "gpu_h": round(h, 2)})
    s_lv, s_lcb = N_LV * k, N_LCB * k
    # training tokens per outer fold (one epoch, 900 tokens per sequence), counted per adapter.
    # fin: final adapter on 4 training folds; inner: adapter on 3 training folds (one inner split).
    # The isotonic map of the trained readout needs out-of-fold scores on all 4 training folds,
    # so each (outer fold, suite) needs 4 inner adapters (R1 counted 1; corrected in R2).
    # Recipe selection (3 learning rates) uses the first inner split only (R2 section 7.4).
    fin = 0.8 * s_lv * 900; inner = 0.6 * s_lv * 900; lcb_ad = 0.6 * s_lcb * 900
    sel = 3 * inner                                   # 3 rates on inner split 1 (EvalPlus suite)
    ev_inner = 3 * inner                              # inner splits 2-4, selected rate, EvalPlus suite
    or_inner = 4 * inner                              # inner splits 1-4, original suite
    per_primary = 5 * (sel + ev_inner + or_inner + 2 * fin + 2 * lcb_ad)
    # Secondary strata (coder, base, trajectory, thinking on): isotonic map of the trained readout fit on
    # the final adapter's in-sample training-fold scores (R2 section 7.3), so no inner adapters beyond selection.
    per_lv_own_recipe = 5 * (sel + 2 * fin)
    per_reuse = 5 * (2 * fin)
    # Refits for the R2 refit rule: R is within-problem AUROC, on which the isotonic map is a null player
    # (lexicographic tie-break), so a refit needs only the final adapter (EvalPlus suite).
    per_refit_seed = 5 * fin
    # generation
    for sz in ("8B", "12B", "14B", "32B"):
        ms = [m for m, z in PRIMARY.items() if z == sz]
        tok = s_lv * TOK_GEN["lv"] + s_lcb * TOK_GEN["lcb"]
        add(f"Generation, primary {sz}", f"{tok/1e6:.2f}M / {DEC[sz]}", len(ms), len(ms) * tok / DEC[sz] / 3600)
    for m, sz in CODER_INSTRUCT.items():
        tok = s_lv * TOK_GEN["lv"]
        add(f"Generation, coder instruct {m} (label-validity)", f"{tok/1e6:.2f}M / {DEC[sz]}", 1, tok / DEC[sz] / 3600)
    tok = s_lv * TOK_GEN["lv"]
    add("Generation, Olmo SFT and DPO (label-validity)", f"{tok/1e6:.2f}M / 4000", 2, 2 * tok / 4000 / 3600)
    h = sum(s_lv * TOK_GEN["base"] / DEC[sz] / 3600 for sz in BASES.values())
    add("Generation, base (label-validity)", f"{s_lv*TOK_GEN['base']/1e6:.2f}M each", len(BASES), h)
    tok = (s_lv + s_lcb) * TOK_GEN["think"]
    add("Generation, Qwen3-8B thinking on", f"{tok/1e6:.1f}M / 4000", 1, tok / 4000 / 3600)
    camp = s_lcb * 400 / 3000 + s_lcb * 1500 / 3000
    add("Generation, [Campos] models (LiveCodeBench)", "Coder-30B-A3B 400 tok and gpt-oss 1,500 tok at 3,000 tok/s", 2, camp / 3600)
    # forward pass
    h = sum((s_lv + s_lcb) * 900 / PRE[sz] / 3600 for sz in PRIMARY.values())
    add("Forward pass, primary", f"{(s_lv+s_lcb)*900/1e6:.1f}M tokens each", 6, h)
    h = sum(s_lv * 900 / PRE[sz] / 3600 for sz in list(CODER_INSTRUCT.values()) + list(BASES.values()) + list(TRAJ.values()))
    add("Forward pass, coder, base, and Olmo stages", f"{s_lv*900/1e6:.2f}M tokens each", 12, h)
    add("Forward pass, thinking on", f"{(s_lv+s_lcb)*6900/1e6:.0f}M / 15000", 1, (s_lv + s_lcb) * 6900 / 15000 / 3600)
    add("Forward pass, [Campos] models", "Coder 1,000 tok at 10,000; gpt-oss 2,500 tok at 10,000", 2, (s_lcb * 1000 + s_lcb * 2500) / 10000 / 3600)
    add("V1 greedy decode allowance", "R1 allowance scaled by conditions and k", 19, 5.0 * (19 / 17) * (k / 10))
    # trained stated readouts
    for sz in ("8B", "12B", "14B", "32B"):
        n = sum(1 for z in PRIMARY.values() if z == sz)
        add(f"Trained stated readout, primary {sz}", f"{per_primary/1e6:.1f}M / {LORA[sz]:.0f} x {OVH}", n, n * per_primary / LORA[sz] / 3600 * OVH)
    h = sum(per_lv_own_recipe / LORA[sz] / 3600 * OVH for sz in CODER_INSTRUCT.values())
    add("Trained stated readout, coder instruct (own recipe, in-sample isotonic)", f"{per_lv_own_recipe/1e6:.1f}M each", 2, h)
    h = sum(per_reuse / LORA[sz] / 3600 * OVH for sz in list(BASES.values()) + list(TRAJ.values()))
    add("Trained stated readout, base and Olmo stages (recipe reused, in-sample isotonic)", f"{per_reuse/1e6:.1f}M each", 10, h)
    think_tok = 5 * (2 * 0.8 * s_lv * 6900)
    add("Trained stated readout, thinking on (recipe reused, in-sample isotonic)", f"{think_tok/1e6:.0f}M / {LORA['8B']:.0f} x {OVH}", 1, think_tok / LORA["8B"] / 3600 * OVH)
    cap = 3 * 5 * fin
    h = cap / LORA["8B"] / 3600 * OVH + cap / LORA["14B"] / 3600 * OVH
    add("Capacity controls (Olmo-3-7B-Instruct and Qwen3-14B)", f"{cap/1e6:.1f}M per model", 2, h)
    h = sum(2 * per_refit_seed / LORA[sz] / 3600 * OVH for sz in PRIMARY.values())
    add("LoRA refits under fold seeds 1 and 2, all six primary models (final adapters, EvalPlus suite)", f"{2*per_refit_seed/1e6:.1f}M per model", 6, h)
    # generation shift, label-validity, k_g = k
    tr = 2 * 5 * fin / LORA_FULL_8B / 3600 * OVH_FULL
    fresh = N_LV * k * 200 * 2 / ADAPT_GEN_8B / 3600
    fw = 2 * (2 * s_lv) * 900 / 15000 / 3600
    rb = 2 * s_lv * 900 / 15000 / 3600
    add("Generation shift, Qwen3-8B thinking off, label-validity (k_g = k)", "R-Tuning training, fresh generation, two forward passes, reading B", 1, tr + fresh + fw + rb)
    # 2610.31820 reconciliation, LCB thinking on, k_g = 4; training on frozen LCB samples scales with k
    tr = 5 * 0.8 * s_lcb * 7000 / LORA_FULL_8B / 3600 * OVH_FULL
    fresh = N_LCB_RECON * 4 * 6000 / ADAPT_GEN_8B / 3600
    fw = 2 * N_LCB_RECON * 4 * 7000 / 15000 / 3600
    rb = s_lcb * 7000 / 15000 / 3600
    add("Generation shift, thinking on, LiveCodeBench ([2610.31820], k_g = 4)", "training on frozen samples; fresh; two forward passes; reading B", 1, tr + fresh + fw + rb)
    add("Pilot (section 13)", "T1 end to end 4.0 h; mixed-count generation and labels for P1 to P6 (in the generation rows); 32B throughput probe 1.5 h; thinking-length probe 0.5 h", 1, 6.0)
    total = sum(r["gpu_h"] for r in rows)
    return {"k": k, "rows": rows, "total": round(total, 1), "with_25pct_contingency": round(total * 1.25, 1)}


out = {"note": "Planning arithmetic under R1 section 12.1 throughput assumptions; 12B row interpolated (decode 3,000, prefill 10,000 tok/s). Not measurements.",
       "k10": budget(10), "k20": budget(20)}
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "budget_r2.json", "w"), indent=1)
for key in ("k10", "k20"):
    b = out[key]
    print(f"k={b['k']}: total {b['total']} h, with contingency {b['with_25pct_contingency']} h")
    for r in b["rows"]:
        print(f"  {r['gpu_h']:7.2f}  {r['stage']}")
