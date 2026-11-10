"""Unsupervised readouts: token likelihood (7.6), sampling agreement (7.7), AST clustering (7.8).

None of these reads a label. Their rows have `label_suite=None`, `fold_seed=None`, `fold=None`.

Token likelihood, over the code tokens only (the capture excludes the fence and end-of-turn tokens):
  TL_geo: rank_score = prob = exp(mean log p)             (also the [Ribeiro] Intrinsic readout)
  TL_min: rank_score = prob = exp(min log p)
  TL_sum: rank_score = sum log p (length-confounded);  prob = exp(sum log p), the probability of the
          whole generated code, documented here because the design does not define a probability for it.
A sample with no code token is `missing`: prob = rank_score = 0 for TL_geo and TL_min, and for TL_sum
rank_score is one below the smallest observed sum and prob = 0.

Agreement: A(c_ij) = share of the other k-1 samples of the problem with the same behavior signature
(tuple of per-input canonical outputs, floats normalized to AGREEMENT_SIGNATURE_FLOAT_SIG significant
digits). A sample without a signature (None) agrees with no one. A problem with no agreement inputs (no
sample has a non-empty signature) or with a single sample is `missing` for every sample (prob and
rank_score NaN); AGREE is never imputed. `AGREE_problem` is the problem-level variant: the share of the
largest cluster of equal signatures, repeated on every sample of the problem.

AST clustering: each sample is parsed, docstrings are removed, functions, classes, arguments, and bound
names are renamed to v0, v1, ... in order of first occurrence in a depth-first source-order walk (program
wide, scope-insensitive), and the tree is dumped with `ast.dump` (comments never reach the tree).
Samples with no code or code that does not parse are singleton clusters. Score = cluster size / k.
"""

from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict

import numpy as np

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import ReadoutScore

from .common import make_score


# ---------------------------------------------------------------------------------------------------
# Token likelihood
# ---------------------------------------------------------------------------------------------------
def _code_logprobs(data: ReadoutData, i: int):
    if data.code_logprobs is not None and data.code_logprobs[i] is not None:
        return np.asarray(data.code_logprobs[i], dtype=np.float64)
    return None


def tl_scores(data: ReadoutData, model_key: str, population: str) -> dict[str, list[ReadoutScore]]:
    n = len(data.sample_uids)
    mean, mn, sm, ok = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n, dtype=bool)
    for i in range(n):
        lp = _code_logprobs(data, i)
        if lp is not None and lp.size:
            mean[i], mn[i], sm[i], ok[i] = lp.mean(), lp.min(), lp.sum(), True
        elif lp is None and data.capture is not None and data.capture[i].n_code_tokens > 0:
            c = data.capture[i]
            mean[i], mn[i], sm[i], ok[i] = c.mean_logprob, c.min_logprob, c.sum_logprob, True
    floor = (sm[ok].min() - 1.0) if ok.any() else -1.0
    out: dict[str, list[ReadoutScore]] = {"TL_geo": [], "TL_min": [], "TL_sum": []}
    for i in range(n):
        kw = dict(model_key=model_key, population=population, label_suite=None, fold_seed=None, fold=None,
                  missing=not ok[i])
        if ok[i]:
            g, m, s = float(np.exp(mean[i])), float(np.exp(mn[i])), float(sm[i])
            out["TL_geo"].append(make_score(data, i, readout="TL_geo", prob=g, rank_score=g, **kw))
            out["TL_min"].append(make_score(data, i, readout="TL_min", prob=m, rank_score=m, **kw))
            out["TL_sum"].append(make_score(data, i, readout="TL_sum", prob=float(np.exp(s)), rank_score=s, **kw))
        else:
            out["TL_geo"].append(make_score(data, i, readout="TL_geo", prob=0.0, rank_score=0.0, **kw))
            out["TL_min"].append(make_score(data, i, readout="TL_min", prob=0.0, rank_score=0.0, **kw))
            out["TL_sum"].append(make_score(data, i, readout="TL_sum", prob=0.0, rank_score=float(floor), **kw))
    return out


# ---------------------------------------------------------------------------------------------------
# Agreement
# ---------------------------------------------------------------------------------------------------
_FLOAT = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+(?=[eE]))(?:[eE][-+]?\d+)?")


def _norm_float(m: re.Match) -> str:
    try:
        return format(float(m.group(0)), f".{K.AGREEMENT_SIGNATURE_FLOAT_SIG}g")
    except ValueError:  # pragma: no cover
        return m.group(0)


def normalize_signature(sig) -> tuple[str, ...] | None:
    """Float literals inside each element are rounded to AGREEMENT_SIGNATURE_FLOAT_SIG significant digits."""
    if sig is None:
        return None
    if isinstance(sig, str):
        sig = json.loads(sig)
    return tuple(_FLOAT.sub(_norm_float, e if isinstance(e, str) else json.dumps(e, sort_keys=True)) for e in sig)


def _problem_groups(data: ReadoutData) -> dict[str, list[int]]:
    g: dict[str, list[int]] = defaultdict(list)
    for i, p in enumerate(data.problem_ids):
        g[p].append(i)
    return g


def agreement_scores(data: ReadoutData, model_key: str, population: str) -> dict[str, list[ReadoutScore]]:
    outputs = data.agreement_outputs or {}
    sigs = {i: normalize_signature(outputs.get(u)) for i, u in enumerate(data.sample_uids)}
    rows: dict[str, list[ReadoutScore]] = {"AGREE": [], "AGREE_problem": []}
    kw = dict(model_key=model_key, population=population, label_suite=None, fold_seed=None, fold=None)
    for pid, idxs in _problem_groups(data).items():
        k = len(idxs)
        valid = {i: sigs[i] for i in idxs if sigs[i]}          # non-None and non-empty
        counts = Counter(valid.values())
        if k < 2 or not valid:
            for i in idxs:
                for name in rows:
                    rows[name].append(make_score(data, i, readout=name, prob=float("nan"),
                                                 rank_score=float("nan"), missing=True, **kw))
            continue
        share = max(counts.values()) / k
        for i in idxs:
            a = (counts[valid[i]] - 1) / (k - 1) if i in valid else 0.0
            rows["AGREE"].append(make_score(data, i, readout="AGREE", prob=a, rank_score=a, **kw))
            rows["AGREE_problem"].append(make_score(data, i, readout="AGREE_problem", prob=share, rank_score=share, **kw))
    return rows


# ---------------------------------------------------------------------------------------------------
# AST clustering
# ---------------------------------------------------------------------------------------------------
def _bound_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(n.name)
        elif isinstance(n, ast.arg):
            names.add(n.arg)
        elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            names.add(n.id)
        elif isinstance(n, ast.ExceptHandler) and n.name:
            names.add(n.name)
    return names


class _Renamer(ast.NodeTransformer):
    def __init__(self, bound: set[str]):
        self.bound, self.map = bound, {}

    def _new(self, name: str) -> str:
        if name not in self.map:
            self.map[name] = f"v{len(self.map)}"
        return self.map[name]

    def _maybe(self, name: str) -> str:
        return self._new(name) if name in self.bound else name

    def visit_FunctionDef(self, node):
        node.name = self._new(node.name)
        node.args = self.visit(node.args)
        node.body = [self.visit(s) for s in node.body]
        node.decorator_list = [self.visit(d) for d in node.decorator_list]
        if node.returns is not None:
            node.returns = self.visit(node.returns)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        node.name = self._new(node.name)
        node.bases = [self.visit(b) for b in node.bases]
        node.keywords = [self.visit(k) for k in node.keywords]
        node.body = [self.visit(s) for s in node.body]
        node.decorator_list = [self.visit(d) for d in node.decorator_list]
        return node

    def visit_arg(self, node):
        node.arg = self._new(node.arg)
        if node.annotation is not None:
            node.annotation = self.visit(node.annotation)
        return node

    def visit_Name(self, node):
        node.id = self._maybe(node.id)
        return node

    def visit_ExceptHandler(self, node):
        if node.name:
            node.name = self._new(node.name)
        self.generic_visit(node)
        return node

    def visit_Global(self, node):
        node.names = [self._maybe(n) for n in node.names]
        return node

    visit_Nonlocal = visit_Global


def _strip_docstrings(tree: ast.AST) -> None:
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body:
            b = n.body[0]
            if isinstance(b, ast.Expr) and isinstance(b.value, ast.Constant) and isinstance(b.value.value, str):
                n.body = n.body[1:] or [ast.Pass()]


def ast_signature(code: str | None) -> str | None:
    """Normalized `ast.dump` of the code, or None if there is no code or it does not parse."""
    if not code:
        return None
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError, MemoryError, RecursionError):
        return None
    _strip_docstrings(tree)
    tree = _Renamer(_bound_names(tree)).visit(tree)
    ast.fix_missing_locations(tree)
    return ast.dump(tree, annotate_fields=True, include_attributes=False)


def ast_cluster_scores(data: ReadoutData, model_key: str, population: str) -> list[ReadoutScore]:
    texts = data.code_texts or [None] * len(data.sample_uids)
    sig = [ast_signature(t) for t in texts]
    out = []
    for pid, idxs in _problem_groups(data).items():
        k = len(idxs)
        counts = Counter(sig[i] for i in idxs if sig[i] is not None)
        for i in idxs:
            size = counts[sig[i]] if sig[i] is not None else 1   # unparseable samples are singletons
            out.append(make_score(data, i, model_key=model_key, population=population, readout="AST",
                                  label_suite=None, fold_seed=None, fold=None, prob=size / k, rank_score=size / k))
    return out
