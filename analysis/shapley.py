"""Shapley attribution over the toggle game (design sections 1.4 and 9).

Cells are keyed by bit strings over the players in order; for the gap game the players are
(r, t, d, l), so "0000" is G0 = Gamma(0, 0, 0, 0) and "1111" is R^(0) = Gamma(1, 1, 1, 1). A
coalition S has the bits of its members set to 1. Values may be floats or numpy arrays of equal
shape (per-resample cells), so the same code gives point values and replicates.

- Shapley value (exact weights): phi_v = sum_{S subset N \\ {v}} |S|! (n - |S| - 1)! / n!
  [v(S + v) - v(S)]. Efficiency: v(empty) + sum_v phi_v = v(N), asserted to 1e-12 on point values.
- Shapley interaction index of order 2 (Grabisch 1997): I_ij = sum_{S subset N \\ {i, j}}
  |S|! (n - |S| - 2)! / (n - 1)! [v(S + ij) - v(S + i) - v(S + j) + v(S)].
- Sequential decomposition for an order (p1, ..., pn): the term of p_k is v({p1..pk}) - v({p1..pk-1}).
  Labels first is (l, d, t, r); readout first is (r, t, d, l).
- The decision-cost game of the routing replay (section 10) uses the same functions with a
  different payoff.
"""

from __future__ import annotations

from itertools import combinations
from math import factorial
from typing import Mapping, Sequence

import numpy as np

from pipeline.contracts.schemas import TOGGLES, ShapleyResult

EFFICIENCY_TOL = 1e-12
LABELS_FIRST = ("l", "d", "t", "r")
READOUT_FIRST = ("r", "t", "d", "l")


def key_of(coalition, players: Sequence[str] = TOGGLES) -> str:
    s = set(coalition)
    unknown = s - set(players)
    if unknown:
        raise ValueError(f"unknown players {sorted(unknown)}")
    return "".join("1" if p in s else "0" for p in players)


def all_keys(players: Sequence[str] = TOGGLES) -> list[str]:
    n = len(players)
    return [format(i, f"0{n}b") for i in range(2 ** n)]


def _check_cells(cells: Mapping[str, object], players: Sequence[str]) -> None:
    want = set(all_keys(players))
    have = set(cells)
    if have != want:
        raise ValueError(f"cells must have exactly the {len(want)} keys over {tuple(players)}; "
                         f"missing {sorted(want - have)}, extra {sorted(have - want)}")


def shapley_values(cells: Mapping[str, object], players: Sequence[str] = TOGGLES) -> dict[str, object]:
    _check_cells(cells, players)
    n = len(players)
    out: dict[str, object] = {}
    for v in players:
        others = [p for p in players if p != v]
        total = 0.0
        for size in range(n):
            wgt = factorial(size) * factorial(n - size - 1) / factorial(n)
            for S in combinations(others, size):
                total = total + wgt * (np.asarray(cells[key_of(S + (v,), players)], dtype=np.float64)
                                       - np.asarray(cells[key_of(S, players)], dtype=np.float64))
        out[v] = total
    return out


def interaction_indices(cells: Mapping[str, object], players: Sequence[str] = TOGGLES) -> dict[str, object]:
    _check_cells(cells, players)
    n = len(players)
    out: dict[str, object] = {}
    for i, j in combinations(players, 2):
        others = [p for p in players if p not in (i, j)]
        total = 0.0
        for size in range(n - 1):
            wgt = factorial(size) * factorial(n - size - 2) / factorial(n - 1)
            for S in combinations(others, size):
                c = lambda T: np.asarray(cells[key_of(T, players)], dtype=np.float64)  # noqa: E731
                total = total + wgt * (c(S + (i, j)) - c(S + (i,)) - c(S + (j,)) + c(S))
        out[i + j] = total
    return out


def sequential(cells: Mapping[str, object], order: Sequence[str], players: Sequence[str] = TOGGLES) -> dict[str, object]:
    _check_cells(cells, players)
    if sorted(order) != sorted(players):
        raise ValueError("order must be a permutation of the players")
    out: dict[str, object] = {}
    prev: tuple[str, ...] = ()
    for p in order:
        cur = prev + (p,)
        out[p] = (np.asarray(cells[key_of(cur, players)], dtype=np.float64)
                  - np.asarray(cells[key_of(prev, players)], dtype=np.float64))
        prev = cur
    return out


def _f(x) -> float:
    return float(np.asarray(x))


def shapley(cells: Mapping[str, float], players: Sequence[str] = TOGGLES,
            orders: tuple[Sequence[str], Sequence[str]] = (LABELS_FIRST, READOUT_FIRST)) -> ShapleyResult:
    """Point Shapley result for the gap game (or any game with the same players)."""
    phi = shapley_values(cells, players)
    inter = interaction_indices(cells, players)
    seq1 = sequential(cells, orders[0], players)
    seq2 = sequential(cells, orders[1], players)
    g0 = _f(cells["0" * len(players)])
    res = _f(cells["1" * len(players)])
    gap = g0 + sum(_f(phi[p]) for p in players) - res
    if np.isfinite(gap):
        assert abs(gap) <= EFFICIENCY_TOL, f"Shapley efficiency gap {gap}"
    return ShapleyResult(players=tuple(players), cells={k: _f(v) for k, v in cells.items()},
                         phi={p: _f(phi[p]) for p in players},
                         interactions={k: _f(v) for k, v in inter.items()},
                         seq_labels_first={p: _f(seq1[p]) for p in players},
                         seq_readout_first={p: _f(seq2[p]) for p in players},
                         g0=g0, residual=res, efficiency_gap=float(gap))


def shapley_replicates(cell_reps: Mapping[str, np.ndarray], players: Sequence[str] = TOGGLES,
                       orders: tuple[Sequence[str], Sequence[str]] = (LABELS_FIRST, READOUT_FIRST)) -> dict[str, np.ndarray]:
    """Per-resample terms from per-resample cells. Keys: "phi_<p>", "int_<pq>", "seqL_<p>",
    "seqR_<p>", "g0", "residual". NaN propagates from undefined cells."""
    phi = shapley_values(cell_reps, players)
    inter = interaction_indices(cell_reps, players)
    seq1 = sequential(cell_reps, orders[0], players)
    seq2 = sequential(cell_reps, orders[1], players)
    out = {f"phi_{p}": np.asarray(phi[p]) for p in players}
    out.update({f"int_{k}": np.asarray(v) for k, v in inter.items()})
    out.update({f"seqL_{p}": np.asarray(seq1[p]) for p in players})
    out.update({f"seqR_{p}": np.asarray(seq2[p]) for p in players})
    out["g0"] = np.asarray(cell_reps["0" * len(players)], dtype=np.float64)
    out["residual"] = np.asarray(cell_reps["1" * len(players)], dtype=np.float64)
    eff = out["g0"] + sum(out[f"phi_{p}"] for p in players) - out["residual"]
    fin = np.isfinite(eff)
    if fin.any():
        assert np.max(np.abs(eff[fin])) <= EFFICIENCY_TOL * max(1.0, float(np.max(np.abs(out["residual"][fin])))), \
            "Shapley efficiency fails on a resample"
    return out


def point_terms(res: ShapleyResult) -> dict[str, float]:
    """The point values keyed as in shapley_replicates."""
    out = {f"phi_{p}": res.phi[p] for p in res.players}
    out.update({f"int_{k}": v for k, v in res.interactions.items()})
    out.update({f"seqL_{p}": res.seq_labels_first[p] for p in res.players})
    out.update({f"seqR_{p}": res.seq_readout_first[p] for p in res.players})
    out["g0"] = res.g0
    out["residual"] = res.residual
    return out


def readout_change_split(cells_primary: Mapping[str, object], cells_v2: Mapping[str, object],
                         rdl: tuple[int, int, int]) -> dict[str, object]:
    """Split of the readout-change step at (r, d, l) = rdl into a format step (zero-shot V1 to
    zero-shot V2) and a training step (zero-shot V2 to S^T) (section 1.4). cells_primary are the
    cells of the V1 chain and cells_v2 those of the V2 sensitivity chain; the t = 1 cells are the
    same in both chains. Returns format, training, and total (= cells[t=1] - cells_primary[t=0])."""
    r, d, l = rdl
    k0 = f"{r}0{d}{l}"
    k1 = f"{r}1{d}{l}"
    v1 = np.asarray(cells_primary[k0], dtype=np.float64)
    v2 = np.asarray(cells_v2[k0], dtype=np.float64)
    t1 = np.asarray(cells_primary[k1], dtype=np.float64)
    t1b = np.asarray(cells_v2[k1], dtype=np.float64)
    fin = np.isfinite(t1) & np.isfinite(t1b)
    if np.any(t1[fin] != t1b[fin]):
        raise ValueError("t = 1 cells differ between the chains; they must use the same S^T")
    return {"format": v2 - v1, "training": t1 - v2, "total": t1 - v1}


# Positions of the split: the full configuration and the position where t enters in each order.
SPLIT_POSITIONS = {"full_rdl_111": (1, 1, 1), "labels_first_rdl_011": (0, 1, 1), "readout_first_rdl_100": (1, 0, 0)}
