"""Direction B — does a model's per-requirement TEST competence track its per-requirement CODE competence?

Signature-matching (clean single-fail mutants are too scarce, 6.5%): every self-generated test_* method
gets a pass/fail SIGNATURE across the problem's 10 labeled solutions; a reference requirement R is
"covered" by the self-suite iff some self-method's signature correlates with R's reference signature.

  code_comp(R) = mean over 10 solutions of (solution passes reference R)      [from per_solution_l1]
  test_comp(R) = max over self-methods m of phi-corr(sig_m, ref_R)            [computed here]

Headline claim: code_comp and test_comp are POSITIVELY correlated across (problem,R) pairs — the
requirements a model fails to code are the ones it fails to test for. Restricted to DISCRIMINATIVE R
(ref signature not all-0/all-1, else no signal to match).
"""
from __future__ import annotations
import argparse
import ast
import json
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from pertest_harness import _run_script          # reuse the subprocess runner
from serialization import load_labeled


def _method_names(test_code: str) -> list[str]:
    """test_* method names inside the first TestCases-like unittest class."""
    try:
        tree = ast.parse(test_code)
    except SyntaxError:
        return []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            ms = [n.name for n in node.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]
            if ms:
                return ms
    return []


def _run_method(solution_code: str, test_code: str, cls_hint: str, method: str, timeout: int) -> bool:
    """True iff (solution + self-test class) runs `method` and it PASSES."""
    runner = (f"\nimport unittest as _ut, sys as _s\n"
              f"_r=_ut.TestResult()\n{cls_hint}('{method}').run(_r)\n_s.exit(0 if _r.wasSuccessful() else 1)\n")
    return _run_script(solution_code + "\n" + test_code + runner, timeout)


def _cls_name(test_code: str) -> str:
    try:
        tree = ast.parse(test_code)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                return node.name
    except SyntaxError:
        pass
    return "TestCases"


def _phi(a: np.ndarray, b: np.ndarray) -> float:
    """Pearson/phi between two binary vectors; nan if either is constant."""
    if a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def score(labels_path, selftests_path, timeout=10, max_workers=None, limit=None):
    selftests = {}
    for line in open(selftests_path, encoding="utf-8"):
        if line.strip():
            d = json.loads(line)
            selftests.setdefault(d["problem_id"], d["test_code"])   # sample 0
    recs = load_labeled(labels_path)
    workers = max_workers or (os.cpu_count() or 8)

    code_comp, test_comp = [], []
    n_prob, n_pairs = 0, 0
    for r in recs:
        tc = selftests.get(r.problem_id)
        if not tc:
            continue
        methods = _method_names(tc)
        if not methods:
            continue
        cls = _cls_name(tc)
        sols = r.solutions
        reqs = list(r.per_solution_l1.keys())
        if len(reqs) < 2:
            continue
        # reference signatures per requirement across the n solutions
        ref = {q: np.array(r.per_solution_l1[q], dtype=float) for q in reqs}
        # self-method signatures: [method x solution] pass matrix (parallel over the grid)
        jobs = [(mi, si) for mi in range(len(methods)) for si in range(len(sols))]
        sig = np.zeros((len(methods), len(sols)))
        def _do(job):
            mi, si = job
            return mi, si, _run_method(sols[si], tc, cls, methods[mi], timeout)
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for mi, si, ok in ex.map(_do, jobs):
                sig[mi, si] = 1.0 if ok else 0.0
        n_prob += 1
        for q in reqs:
            if ref[q].std() == 0:                      # non-discriminative requirement -> skip
                continue
            corrs = [_phi(sig[mi], ref[q]) for mi in range(len(methods))]
            corrs = [c for c in corrs if not np.isnan(c)]
            if not corrs:
                continue
            test_comp.append(max(corrs))               # best-matching self-test method
            code_comp.append(float(ref[q].mean()))
            n_pairs += 1
        if limit and n_prob >= limit:
            break

    code_comp, test_comp = np.array(code_comp), np.array(test_comp)
    print(f"problems scored: {n_prob} | discriminative (problem,req) pairs: {n_pairs}")
    if n_pairs > 2:
        rho = float(np.corrcoef(code_comp, test_comp)[0, 1])
        # bootstrap CI
        rng = np.random.RandomState(0)
        boots = [np.corrcoef(code_comp[i], test_comp[i])[0, 1]
                 for i in (rng.randint(0, n_pairs, n_pairs) for _ in range(1000))]
        lo, hi = np.percentile(boots, 2.5), np.percentile(boots, 97.5)
        print(f"code_comp: mean {code_comp.mean():.3f} | test_comp(best-match phi): mean {test_comp.mean():.3f}")
        print(f"CORR(code_comp, test_comp) = {rho:.3f}  CI=[{lo:.3f}, {hi:.3f}]")
        print("  positive => requirements a model fails to CODE are the ones it fails to TEST for.")
    return code_comp, test_comp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default="/workspace/data/v4_dprc/labels/bcb_full.jsonl")
    ap.add_argument("--selftests", default="/workspace/data/v4_dprc/labels/selftests_qwen.jsonl")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    score(args.labels, args.selftests, limit=args.limit)
