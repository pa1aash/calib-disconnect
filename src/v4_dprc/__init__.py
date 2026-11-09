"""DPRC — Decoupled Per-Requirement Confidence for code LLMs (AAAI-27 extension).

Package layout:
  metrics.py         — calibration/discrimination metrics (reused from v3, + grouped bootstrap)
  pertest_harness.py — per-test-case execution harness (Build #1, CPU-parallel)
  grouping.py        — deterministic requirement-grouping rule (frozen for reproducibility)
  loaders.py         — per-test benchmark loaders (HumanEval/MBPP now; LiveCodeBench/TACO next)
"""
