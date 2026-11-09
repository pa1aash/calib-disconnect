"""The structured confidence block + tokenized-Brier scoring math.

DPRC has the model emit, after its solution, a structured per-requirement confidence block:

    CONFIDENCE:
    REQ empty_or_zero: <d>
    REQ typical: <d>

where <d> is a SINGLE digit token 0-9. The scalar confidence for a group is the model's
EXPECTED digit under its distribution over the ten digit tokens at that slot, divided by 9:

    c_g = ( sum_k k * p(token='k') ) / 9          (k = 0..9)

Training loss (ConfTuner-style tokenized Brier, a proper scoring rule) on the CONTINUOUS
per-group pass-rate target t_g:

    L_brier = mean_g ( c_g - t_g )^2

This module holds:
  - block formatting (format_conf_block, parse_conf_block)
  - a pure-numpy reference for the scalar + Brier loss (validated locally, no torch)
The torch mirror used by the Trainer lives in train_dprc.py (imports torch only on the box).
"""
from __future__ import annotations
import re
import numpy as np

DIGITS = [str(d) for d in range(10)]          # the 10 confidence tokens
DIGIT_VALUES = np.arange(10, dtype=float)     # 0..9
CONF_HEADER = "CONFIDENCE:"


def target_to_digit(t: float) -> str:
    """Nearest digit for the discrete/coarse readout + the CE-baseline (round t*9)."""
    return str(int(round(max(0.0, min(1.0, t)) * 9)))


def format_conf_block(groups: list[str], targets: dict | None = None, teacher: bool = False) -> str:
    """Render the confidence block. teacher=True fills digits from `targets` (for SFT text);
    teacher=False leaves a placeholder the model completes at inference."""
    lines = [CONF_HEADER]
    for g in groups:
        d = target_to_digit(targets[g]) if (teacher and targets) else "?"
        lines.append(f"REQ {g}: {d}")
    return "\n".join(lines) + "\n"


_REQ_RE = re.compile(r"^REQ\s+(.+?):\s*([0-9])\s*$", re.MULTILINE)


def parse_conf_block(text: str) -> dict:
    """Extract {group: scalar in [0,1]} from a model's emitted block (digit/9)."""
    return {m.group(1).strip(): int(m.group(2)) / 9.0 for m in _REQ_RE.finditer(text)}


# ---------------- pure-numpy reference scoring (validated locally) ----------------

def expected_scalar(prob_over_digits: np.ndarray) -> float:
    """c_g from a probability vector over the 10 digit tokens (softmax already applied)."""
    p = np.asarray(prob_over_digits, dtype=float)
    p = p / p.sum()
    return float((p * DIGIT_VALUES).sum() / 9.0)


def brier_loss_np(digit_probs: np.ndarray, targets: np.ndarray) -> float:
    """digit_probs: [n_groups x 10] softmax rows; targets: [n_groups] in [0,1]. Returns mean Brier."""
    scalars = np.array([expected_scalar(row) for row in digit_probs])
    return float(np.mean((scalars - np.asarray(targets, dtype=float)) ** 2))


if __name__ == "__main__":
    # format / parse round-trip
    groups = ["empty_or_zero", "typical", "large"]
    targets = {"empty_or_zero": 0.5, "typical": 1.0, "large": 0.0}
    block = format_conf_block(groups, targets, teacher=True)
    print(block)
    parsed = parse_conf_block(block)
    print("parsed:", parsed)
    # target 0.5 -> digit 4 or 5 (round(4.5)=4 in banker's? python round(4.5)=4) -> 4/9=0.444
    assert set(parsed) == set(groups)

    # scoring math: a confident, correct readout should have LOW brier vs matching targets
    # build peaked distributions at the target digit
    def peak(d):
        v = np.full(10, 0.001); v[d] = 1.0; return v / v.sum()
    dp = np.array([peak(int(round(targets[g]*9))) for g in groups])
    L_good = brier_loss_np(dp, [targets[g] for g in groups])
    # a flat/uninformed distribution should have HIGHER brier on the 0.0/1.0 targets
    flat = np.ones((3, 10)) / 10
    L_flat = brier_loss_np(flat, [targets[g] for g in groups])
    print(f"brier(peaked@target)={L_good:.4f}  brier(flat)={L_flat:.4f}")
    assert L_good < L_flat, "peaked-at-target must beat flat under Brier"
    # expected_scalar of a (near-)peak at digit 9 ~ 1.0, at digit 0 ~ 0.0 (tiny leakage mass)
    assert abs(expected_scalar(peak(9)) - 1.0) < 0.02
    assert abs(expected_scalar(peak(0)) - 0.0) < 0.02
    assert abs(expected_scalar(np.eye(10)[9]) - 1.0) < 1e-9   # true one-hot is exact
    assert abs(expected_scalar(np.eye(10)[0]) - 0.0) < 1e-9
    print("\nSELF-TEST PASSED: conf-block format/parse + tokenized-Brier scoring math correct.")
