"""Near-duplicate groups (design section 4, red team V14c) and problem-grouped folds (section 7).

Near-duplicate scope. The label-validity population is HumanEval+ and MBPP+. Two problems are linked
when their canonical solutions are identical after ast.unparse(ast.parse(...)), or when the
token-set Jaccard similarity of their prompts is at least constants.NEAR_DUP_JACCARD (tokens are
lowercase \\w+ matches). Pairs checked: MBPP+ with MBPP+, and HumanEval+ with MBPP+. HumanEval+ with
HumanEval+ pairs are counted for a diagnostic and never grouped. LiveCodeBench problems have no
canonical solutions and are not grouped.

For HumanEval+, Problem.canonical_solution is the complete program (prompt + body), so the AST
criterion compares complete programs, docstrings included.
"""

from __future__ import annotations

import ast
import re
import warnings
from dataclasses import dataclass, field
from typing import Any, Sequence

from pipeline.contracts import constants, hashing
from pipeline.contracts.schemas import FoldPlan, NearDuplicateGroup, Problem

REASON_AST = "ast_identical"
REASON_JACCARD = "jaccard>=0.8"
_TOKEN = re.compile(r"\w+")


def tokens(text: str) -> frozenset[str]:
    return frozenset(_TOKEN.findall(text.lower()))


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def ast_key(solution: str | None) -> str | None:
    if not solution:
        return None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # legacy escape sequences in benchmark strings
            return ast.unparse(ast.parse(solution))
    except (SyntaxError, ValueError, RecursionError):
        return None


@dataclass
class NearDuplicateReport:
    groups: list[NearDuplicateGroup]
    n_edges: int
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grouped = sorted({m for g in self.groups for m in g.members})
        return {"format": "calib-disconnect/near_duplicates/v1",
                "jaccard_threshold": constants.NEAR_DUP_JACCARD,
                "n_groups": len(self.groups), "n_grouped_problems": len(grouped), "n_edges": self.n_edges,
                "groups": [g.to_dict() for g in self.groups], "diagnostics": self.diagnostics}


class _UnionFind:
    def __init__(self, items: Sequence[str]) -> None:
        self.p = {i: i for i in items}

    def find(self, x: str) -> str:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)


def near_duplicate_report(problems: Sequence[Problem]) -> NearDuplicateReport:
    probs = [p for p in problems if p.benchmark in constants.LABEL_VALIDITY_BENCHMARKS]
    ids = [p.problem_id for p in probs]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate problem IDs")
    toks = {p.problem_id: tokens(p.prompt) for p in probs}
    keys = {p.problem_id: ast_key(p.canonical_solution) for p in probs}
    bench = {p.problem_id: p.benchmark for p in probs}
    uf = _UnionFind(ids)
    edge_reasons: list[tuple[str, str, tuple[str, ...]]] = []
    he_he = {"ast_identical": 0, "jaccard": 0, "any": 0}
    order = sorted(ids)
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            reasons = []
            if keys[a] is not None and keys[a] == keys[b]:
                reasons.append(REASON_AST)
            if jaccard(toks[a], toks[b]) >= constants.NEAR_DUP_JACCARD:
                reasons.append(REASON_JACCARD)
            if not reasons:
                continue
            if bench[a] == "humaneval_plus" and bench[b] == "humaneval_plus":
                he_he["any"] += 1
                he_he["ast_identical"] += REASON_AST in reasons
                he_he["jaccard"] += REASON_JACCARD in reasons
                continue
            uf.union(a, b)
            edge_reasons.append((a, b, tuple(reasons)))
    comps: dict[str, list[str]] = {}
    for i in ids:
        comps.setdefault(uf.find(i), []).append(i)
    by_root = {r: set(m) for r, m in comps.items() if len(m) > 1}
    groups = []
    for root, members in by_root.items():
        rs = sorted({r for a, b, rr in edge_reasons if a in members for r in rr})
        ms = tuple(sorted(members))
        groups.append(NearDuplicateGroup(group_key=ms[0], members=ms, reasons=tuple(rs)))
    groups.sort(key=lambda g: g.group_key)
    diag = {"humaneval_humaneval_pairs_not_grouped": he_he, "n_problems_considered": len(probs)}
    return NearDuplicateReport(groups=groups, n_edges=len(edge_reasons), diagnostics=diag)


def near_duplicate_groups(problems: Sequence[Problem]) -> list[NearDuplicateGroup]:
    return near_duplicate_report(problems).groups


def build_folds(problem_ids: Sequence[str], groups: Sequence[NearDuplicateGroup], fold_seed: int,
                population: str) -> FoldPlan:
    """fold = hashing.fold_of(fold_seed, group key), where the group key is the group's smallest
    member ID (taken from the full group, so a subset run assigns the same fold as the full run), or
    the problem's own ID when it is in no group."""
    ids = list(problem_ids)
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate problem IDs")
    key_of: dict[str, str] = {}
    for g in groups:
        for m in g.members:
            if m in key_of and key_of[m] != g.group_key:
                raise ValueError(f"{m} is in two groups")
            key_of[m] = g.group_key
    assignment = {p: hashing.fold_of(fold_seed, key_of.get(p, p), constants.N_FOLDS) for p in sorted(ids)}
    present = set(ids)
    kept = tuple(sorted((g for g in groups if present & set(g.members)), key=lambda g: g.group_key))
    return FoldPlan(fold_seed=fold_seed, population=population, n_folds=constants.N_FOLDS,
                    assignment=assignment, groups=kept)
