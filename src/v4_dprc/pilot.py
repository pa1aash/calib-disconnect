"""Pilot driver + GATE-2 (the go/no-go, must finish by 07-20).

Reads a held-out slice of labeled problems, elicits the trained model's per-requirement confidence
on each problem's INDEPENDENT solution, and computes per-requirement AUROC + localization
precision@1. Applies the pre-registered GATE-2 ladder:
    per-test (L1) AUROC > 0.65   -> L1 headline
    else per-category (L2) > 0.65 -> L2 headline
    else                          -> L3 floor

`elicit_confidence` (GPU) generates + parses confidence blocks. `evaluate` (CPU) computes the gate
and is unit-tested locally with synthetic elicited confidences.
"""
from __future__ import annotations
import argparse
import numpy as np

import config
from metrics import bootstrap_grouped, localization_precision_at_1
from serialization import load_labeled
# (parse no longer needed: primed digit-readout elicitation)
from sampling import build_prompt


# ---------------------------------------------------------------- GPU: elicit confidence

def elicit_confidence(adapter_dir, records, model_key=config.PRIMARY_MODEL, level="l1"):
    """For each problem, prompt the trained model with (problem + its independent solution) and the
    CONFIDENCE header, let it emit the per-group digits, parse -> {group: c_g}. Returns list aligned
    to `records`: {problem_id: {group: conf}}."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    tok = AutoTokenizer.from_pretrained(config.MODELS[model_key], trust_remote_code=True)
    base = AutoModelForCausalLM.from_pretrained(config.MODELS[model_key], torch_dtype=torch.bfloat16,
                                                device_map="auto", trust_remote_code=True)
    model = PeftModel.from_pretrained(base, adapter_dir); model.eval()
    # prime "REQ <g>: " and read the model's digit distribution -> format is GUARANTEED, no parsing,
    # no fighting the model's JSON-confidence prior. conf = expected digit / 9 (tokenized-Brier readout).
    digit_ids = torch.tensor([tok.encode(str(d), add_special_tokens=False)[-1] for d in range(10)])
    vals = torch.arange(10, dtype=torch.float) / 9.0
    out = {}
    for r in records:
        groups = list((r.targets_l1 if level == "l1" else r.targets_l2).keys())
        acc = f"{build_prompt(_as_problem(r))}\n{r.independent_solution}\n\nCONFIDENCE:\n"
        conf = {}
        for g in groups:
            acc += f"REQ {g}: "
            ids = tok(acc, return_tensors="pt").to(model.device)
            with torch.no_grad():
                logits = model(**ids).logits[0, -1]
            p = torch.softmax(logits[digit_ids.to(logits.device)], dim=-1)
            conf[g] = float((p * vals.to(p.device)).sum())
            acc += f"{int(p.argmax())}\n"          # append greedy digit, stay in-distribution for next group
        out[r.problem_id] = conf
    return out


def _as_problem(r):
    from types import SimpleNamespace
    return SimpleNamespace(problem_id=r.problem_id, source=r.source, prompt=r.prompt,
                           style=r.style, units=[], canonical_solution=None)


# ---------------------------------------------------------------- CPU: evaluate + GATE-2

def evaluate(records, elicited, level="l1"):
    """Assemble (conf, label) pairs and compute per-requirement AUROC (problem-bootstrapped) +
    localization precision@1. `elicited[problem_id][group] = c_g`; missing groups default to 0.5."""
    label_key = "indep_label_l1" if level == "l1" else "indep_label_l2"
    flat, per_problem = [], []
    for r in records:
        labels = getattr(r, label_key)
        conf_map = elicited.get(r.problem_id, {})
        confs, labs = [], []
        for g, lab in labels.items():
            c = float(conf_map.get(g, 0.5))
            flat.append({"problem_id": r.problem_id, "conf": c, "label": int(lab)})
            confs.append(c); labs.append(int(lab))
        if confs:
            per_problem.append({"confs": confs, "labels": labs})
    boot = bootstrap_grouped(flat)
    p_at_1, n_loc = localization_precision_at_1(per_problem)
    return {"level": level, **boot, "loc_precision_at_1": p_at_1, "n_localizable": n_loc}


def gate2(eval_l1, eval_l2=None):
    """Pre-registered GATE-2 verdict from L1 (and optionally L2) evaluations."""
    thr = config.GATE2_AUROC_THRESHOLD
    a1 = eval_l1["auroc"]
    if a1 is not None and not np.isnan(a1) and a1 > thr:
        headline = "L1"; reason = f"per-test AUROC {a1:.3f} > {thr}"
    elif eval_l2 and eval_l2["auroc"] and not np.isnan(eval_l2["auroc"]) and eval_l2["auroc"] > thr:
        headline = "L2"; reason = f"per-test {a1:.3f} <= {thr} but per-category {eval_l2['auroc']:.3f} > {thr}"
    else:
        headline = "L3"; reason = f"per-test {a1:.3f} and per-category both <= {thr}; commit to selective-gen floor"
    amber = (a1 is not None and not np.isnan(a1) and a1 >= config.GATE2_AMBER_AUROC)
    return {"headline": headline, "reason": reason, "amber_or_better": bool(amber),
            "l1_auroc": a1, "l1_ci": eval_l1.get("auroc_ci"),
            "l2_auroc": (eval_l2 or {}).get("auroc")}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default=str(config.LABELS_DIR / "labels_dryrun.jsonl"))
    ap.add_argument("--adapter", default=None, help="LoRA adapter dir (GPU). Omit for local synthetic self-test.")
    args = ap.parse_args()

    if args.adapter:
        records = load_labeled(args.labels)
        elic_l1 = elicit_confidence(args.adapter, records, level="l1")
        elic_l2 = elicit_confidence(args.adapter, records, level="l2")
    else:
        # LOCAL SELF-TEST: real dry-run labels are degenerate (stub canonical passes everything ->
        # single-class labels -> AUROC undefined). Synthesize records WITH label variance + a
        # noisy-informative elicitor, to prove evaluate->gate2 yields the right verdict (AUROC>0.65).
        from serialization import LabeledProblem
        rng = np.random.RandomState(0)
        records = []
        for i in range(40):
            groups = [f"g{j}" for j in range(3)]
            labels = {g: int(rng.rand() < 0.5) for g in groups}      # mixed 0/1 across groups
            records.append(LabeledProblem(
                problem_id=f"syn/{i}", source="syn", prompt="p", style="call",
                solutions=[], independent_solution="",
                test_ids=groups, categories=groups, pass_matrix=[], independent_pass_row=[],
                targets_l1={g: 0.5 for g in groups}, targets_l2={g: 0.5 for g in groups},
                indep_label_l1=labels, indep_label_l2=labels))
        def synth(records, level):
            out = {}
            lk = "indep_label_l1" if level == "l1" else "indep_label_l2"
            for r in records:
                out[r.problem_id] = {g: float(np.clip(lab * 0.6 + 0.2 + rng.normal(0, 0.12), 0, 1))
                                     for g, lab in getattr(r, lk).items()}
            return out
        elic_l1, elic_l2 = synth(records, "l1"), synth(records, "l2")

    ev1 = evaluate(records, elic_l1, "l1")
    ev2 = evaluate(records, elic_l2, "l2")
    verdict = gate2(ev1, ev2)
    print(f"L1 per-requirement AUROC: {ev1['auroc']:.3f} CI={ev1['auroc_ci']} "
          f"(n_problems={ev1['n_problems']}, n_pairs={ev1['n_pairs']}, p@1={ev1['loc_precision_at_1']})")
    print(f"L2 per-category   AUROC: {ev2['auroc']:.3f} CI={ev2['auroc_ci']}")
    print(f"\n[GATE-2] headline={verdict['headline']}  amber_or_better={verdict['amber_or_better']}")
    print(f"         reason: {verdict['reason']}")
    if args.adapter is None:
        assert verdict["headline"] in ("L1", "L2"), "synthetic informative oracle should clear the gate"
        print("\nSELF-TEST PASSED: evaluate + GATE-2 machinery correct (synthetic oracle clears the gate).")
