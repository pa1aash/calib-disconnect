"""Hidden-layer probe baseline + diagnostic (EAGLE-style).

The oracle proves per-method correctness is *behaviourally* discriminable (0.805). The self-expressed
digit readout only reaches 0.603. This asks the decisive question: is the per-method signal linearly
present in the model's hidden state at the `REQ <g>: ` position (the exact spot the digit-readout uses)?

  probe AUROC >> 0.603  -> signal is in the representation; the output-digit readout is the bottleneck
                          (switch method to a probe head; also the planned hidden-probe baseline).
  probe AUROC ~ 0.603   -> the model can't localize per-method failure from one solution (harder pivot).

Extract last-token hidden state per (problem, method) on train+test, L2 logistic regression, AUROC.
Probes the BASE model by default; pass --adapter to probe the trained (LoRA) model's representation.
"""
from __future__ import annotations
import argparse
from types import SimpleNamespace
import numpy as np

import config
from serialization import load_labeled
from sampling import build_prompt


def _as_problem(r):
    return SimpleNamespace(problem_id=r.problem_id, source=r.source, prompt=r.prompt,
                           style=r.style, units=[], canonical_solution=None)


def extract_features(records, model, tok, layer: int, level="l1", max_len=4096):
    """Per (problem, method): hidden state at the last token of '...REQ <g>: ' -> (X, y, problem_ids)."""
    import torch
    label_key = "indep_label_l1" if level == "l1" else "indep_label_l2"
    X, y, pids = [], [], []
    for r in records:
        labels = getattr(r, label_key)
        base = f"{build_prompt(_as_problem(r))}\n{r.independent_solution}\n\nCONFIDENCE:\n"
        for g, lab in labels.items():
            ids = tok(base + f"REQ {g}: ", return_tensors="pt", truncation=True, max_length=max_len).to(model.device)
            with torch.no_grad():
                out = model(**ids, output_hidden_states=True)
            h = out.hidden_states[layer][0, -1].float().cpu().numpy()   # chosen layer, last token
            X.append(h); y.append(int(lab)); pids.append(r.problem_id)
    return np.array(X), np.array(y), pids


def extract_all_layers(records, model, tok, level="l1", max_len=4096):
    """Like extract_features but keeps EVERY layer's last-token state in one forward pass ->
    (list_of_X_per_layer, y, pids). Lets a layer sweep avoid re-running the model per layer."""
    import torch
    label_key = "indep_label_l1" if level == "l1" else "indep_label_l2"
    Xs, y, pids = None, [], []
    for r in records:
        labels = getattr(r, label_key)
        base = f"{build_prompt(_as_problem(r))}\n{r.independent_solution}\n\nCONFIDENCE:\n"
        for g, lab in labels.items():
            ids = tok(base + f"REQ {g}: ", return_tensors="pt", truncation=True, max_length=max_len).to(model.device)
            with torch.no_grad():
                out = model(**ids, output_hidden_states=True)
            hs = out.hidden_states                       # tuple len = n_layers+1
            if Xs is None:
                Xs = [[] for _ in hs]
            for li, h in enumerate(hs):
                Xs[li].append(h[0, -1].float().cpu().numpy())
            y.append(int(lab)); pids.append(r.problem_id)
    return [np.array(x) for x in Xs], np.array(y), pids


def _auroc_ci(clf, sc, Xte, yte, pte):
    from sklearn.metrics import roc_auc_score
    p = clf.predict_proba(sc.transform(Xte))[:, 1]
    if len(set(yte.tolist())) < 2:
        return float("nan"), (float("nan"), float("nan"))
    rng = np.random.RandomState(0)
    uniq = list(dict.fromkeys(pte)); idx_by = {u: [i for i, q in enumerate(pte) if q == u] for u in uniq}
    boots = []
    for _ in range(1000):
        ii = [i for u in rng.choice(uniq, len(uniq), replace=True) for i in idx_by[u]]
        if len(set(yte[ii].tolist())) > 1:
            boots.append(roc_auc_score(yte[ii], p[ii]))
    return roc_auc_score(yte, p), (np.percentile(boots, 2.5), np.percentile(boots, 97.5))


def sweep(train_path, test_path, adapter=None, model_key=config.PRIMARY_MODEL, level="l1"):
    """Probe every layer (single extraction) -> report AUROC per layer, best last."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    tok = AutoTokenizer.from_pretrained(config.MODELS[model_key], trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(config.MODELS[model_key], torch_dtype=torch.bfloat16,
                                                 device_map="auto", trust_remote_code=True)
    if adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter)
    model.eval()
    Xtr_all, ytr, _ = extract_all_layers(load_labeled(train_path), model, tok, level)
    Xte_all, yte, pte = extract_all_layers(load_labeled(test_path), model, tok, level)
    print(f"sweep: {len(Xtr_all)} layers | train {Xtr_all[0].shape} test {Xte_all[0].shape} "
          f"pos train={ytr.mean():.3f} test={yte.mean():.3f} | adapter={'yes' if adapter else 'no'}")
    best = (-1, -1.0, None)
    for li in range(len(Xtr_all)):
        sc = StandardScaler().fit(Xtr_all[li])
        clf = LogisticRegression(C=0.5, max_iter=2000, class_weight="balanced").fit(sc.transform(Xtr_all[li]), ytr)
        a, (lo, hi) = _auroc_ci(clf, sc, Xte_all[li], yte, pte)
        print(f"  layer {li:2d}: AUROC {a:.3f} CI=[{lo:.3f}, {hi:.3f}]")
        if a > best[1]:
            best = (li, a, (lo, hi))
    print(f"BEST layer {best[0]}: AUROC {best[1]:.3f} CI=[{best[2][0]:.3f}, {best[2][1]:.3f}] vs digit-readout 0.603")
    return best


def run(train_path, test_path, adapter=None, model_key=config.PRIMARY_MODEL, layer=-1, level="l1"):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import roc_auc_score

    tok = AutoTokenizer.from_pretrained(config.MODELS[model_key], trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(config.MODELS[model_key], torch_dtype=torch.bfloat16,
                                                 device_map="auto", trust_remote_code=True)
    if adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter)
    model.eval()

    tr, te = load_labeled(train_path), load_labeled(test_path)
    Xtr, ytr, _ = extract_features(tr, model, tok, layer, level)
    Xte, yte, pte = extract_features(te, model, tok, layer, level)
    print(f"probe feats: train {Xtr.shape} pos={ytr.mean():.3f} | test {Xte.shape} pos={yte.mean():.3f}")

    sc = StandardScaler().fit(Xtr)
    clf = LogisticRegression(C=0.5, max_iter=2000, class_weight="balanced").fit(sc.transform(Xtr), ytr)
    p = clf.predict_proba(sc.transform(Xte))[:, 1]
    auroc = roc_auc_score(yte, p) if len(set(yte.tolist())) > 1 else float("nan")

    # problem-grouped bootstrap CI for comparability with the digit-readout AUROC
    rng = np.random.RandomState(0)
    uniq = list(dict.fromkeys(pte)); idx_by = {u: [i for i, q in enumerate(pte) if q == u] for u in uniq}
    boots = []
    for _ in range(1000):
        samp = rng.choice(uniq, len(uniq), replace=True)
        ii = [i for u in samp for i in idx_by[u]]
        yy = yte[ii]
        if len(set(yy.tolist())) > 1:
            boots.append(roc_auc_score(yy, p[ii]))
    lo, hi = (np.percentile(boots, 2.5), np.percentile(boots, 97.5)) if boots else (float("nan"), float("nan"))
    print(f"HIDDEN-PROBE AUROC (layer {layer}{' +adapter' if adapter else ' base'}): {auroc:.3f} "
          f"CI=[{lo:.3f}, {hi:.3f}]  vs digit-readout 0.603")
    return auroc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="/workspace/data/v4_dprc/labels/bcb_train.jsonl")
    ap.add_argument("--test", default="/workspace/data/v4_dprc/labels/bcb_test.jsonl")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--layer", type=int, default=-1, help="hidden_states index; -1=last, try mid layers too")
    ap.add_argument("--level", default="l1", choices=["l1", "l2"])
    ap.add_argument("--sweep", action="store_true", help="probe every layer in one extraction, report best")
    args = ap.parse_args()
    if args.sweep:
        sweep(args.train, args.test, args.adapter, level=args.level)
    else:
        run(args.train, args.test, args.adapter, layer=args.layer, level=args.level)
