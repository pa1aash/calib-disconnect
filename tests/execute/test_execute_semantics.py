"""EvalPlus comparison semantics (copied logic checked against the installed evalplus 0.3.1), time-limit
rule, canonical reprs, and behavior-signature canonicalization. Nothing here runs a subprocess."""

import math

import pytest

from pipeline.execute import harness as H


# ---- parity of the copied oracles with evalplus ------------------------------------------------
def test_copied_oracle_constants_match_installed_evalplus():
    import evalplus
    from evalplus.config import DEFAULT_GT_TIME_LIMIT_FACTOR, DEFAULT_MIN_TIME_LIMIT
    from evalplus.eval import _special_oracle as so

    assert evalplus.__version__ == H.EVALPLUS_VERSION == "0.3.1"
    assert H.MBPP_OUTPUT_NOT_NONE_TASKS == so.MBPP_OUTPUT_NOT_NONE_TASKS
    assert H.MBPP_OUTPUT_SET_EQ_TASKS == so.MBPP_OUTPUT_SET_EQ_TASKS
    assert H.DEFAULT_MIN_TIME_LIMIT == DEFAULT_MIN_TIME_LIMIT == 1.0
    assert H.DEFAULT_GT_TIME_LIMIT_FACTOR == DEFAULT_GT_TIME_LIMIT_FACTOR == 4.0
    for a, b in [(3, 4), (10, 7), (2.5, 3)]:
        assert H._surface_Area(a, b) == so._surface_Area(a, b)
    for a, b in [(12, 456), (1000, 9), (5, 5)]:
        assert H._digit_distance_nums(a, b) == so._digit_distance_nums(a, b)
    assert H._poly([1, 2, 3], 0.5) == so._poly([1, 2, 3], 0.5)


def test_is_floats_matches_evalplus():
    import numpy as np
    from evalplus.eval import is_floats

    for v in [1.0, 1, [1.0, 2.0], (1.0,), [], [1.0, 2], "x", None, np.array([1.0]), np.array([1]), True]:
        assert H.is_floats(v) == is_floats(v)


def test_time_limit_rule():
    assert H.time_limits_for([0.0, 0.1, 0.25, 2.0]) == [1.0, 1.0, 1.0, 8.0]
    assert H.time_limits_for([0.5], min_time_limit=0.2, factor=2.0) == [1.0]


# ---- comparison semantics -----------------------------------------------------------------------
def match(dataset, entry, inp, out, exp, atol=0.0):
    return H.evalplus_match(dataset, entry, inp, out, exp, atol)[0]


def test_exact_equality_and_mismatch():
    assert match("humaneval", "f", (1,), [1, 2], [1, 2])
    assert not match("humaneval", "f", (1,), [1, 2], [2, 1])
    assert not match("humaneval", "f", (1,), "a", "b")


def test_float_outputs_get_the_default_tolerance():
    assert match("humaneval", "f", (), 0.1 + 0.2, 0.3)          # exact_match false, atol promoted to 1e-6
    assert match("humaneval", "f", (), [1.0, 2.0000001], [1.0, 2.0])
    assert not match("humaneval", "f", (), 0.31, 0.3)
    assert H.evalplus_match("humaneval", "f", (), 0.1 + 0.2, 0.3, 0.0)[1] == 1e-6


def test_explicit_atol_is_respected():
    assert match("humaneval", "f", (), 1.05, 1.0, atol=0.1)
    assert not match("humaneval", "f", (), 1.2, 1.0, atol=0.1)


def test_tolerant_path_requires_same_type_and_length():
    assert not match("humaneval", "f", (), 1, 1.0000001, atol=1e-3)         # int output for a float answer
    assert not match("humaneval", "f", (), [1.0], [1.0, 2.0], atol=1e-3)
    assert not match("humaneval", "f", (), (1.0, 2.0), [1.0, 2.0000001], atol=1e-3)  # tuple vs list


def test_atol_promotion_persists_across_tests_like_upstream():
    ok, atol = H.evalplus_match("humaneval", "f", (), 0.3, 0.3, 0.0)
    assert ok and atol == 1e-6
    assert H.evalplus_match("humaneval", "f", (), 7.0 + 1e-9, 7.0, atol)[0]   # the promoted tolerance now applies


def test_humaneval_find_zero_special_oracle():
    xs = [-6, 11, -6, 1]  # (x-1)(x-2)(x-3)
    assert match("humaneval", "find_zero", (xs,), 2.0000000001, 999.0, atol=1e-6)
    assert not match("humaneval", "find_zero", (xs,), 2.5, 2.0, atol=1e-6)
    # only for humaneval
    assert not match("mbpp", "find_zero", (xs,), 2.0000000001, 999.0, atol=1e-6)


def test_mbpp_special_oracles():
    assert match("mbpp", "are_equivalent", (), "anything", "else")                 # Mbpp/164
    assert match("mbpp", "sum_div", (), 0, 28) and not match("mbpp", "sum_div", (), 5, 28)    # Mbpp/295
    assert match("mbpp", "surface_Area", (3, 4), H._surface_Area(3, 4), 999, atol=0)       # Mbpp/581
    assert not match("mbpp", "surface_Area", (3, 4), 1, 999, atol=0)
    assert match("mbpp", "digit_distance_nums", (12, 456), H._digit_distance_nums(12, 456), 0)  # Mbpp/558
    assert not match("mbpp", "digit_distance_nums", (12, 456), 3, 0)


def test_mbpp_set_equality_tasks():
    for name in H.MBPP_OUTPUT_SET_EQ_TASKS:
        assert match("mbpp", name, (), (3, 1, 2), (1, 2, 3))
        assert not match("mbpp", name, (), (3, 1), (1, 2, 3))
    assert not match("humaneval", "similar_elements", (), (3, 1, 2), (1, 2, 3))   # dataset matters


def test_mbpp_output_not_none_tasks():
    for name in H.MBPP_OUTPUT_NOT_NONE_TASKS:
        assert match("mbpp", name, (), "match!", True)        # expected True means "not None"
        assert match("mbpp", name, (), None, False)
        assert not match("mbpp", name, (), None, True)
        assert match("mbpp", name, (), True, True) and not match("mbpp", name, (), False, True)


# ---- canonical reprs and signatures ------------------------------------------------------------
def test_floats_are_normalized_to_nine_significant_digits():
    assert H.canonical_repr(0.1 + 0.2) == H.canonical_repr(0.3) == "0.3"
    assert H.canonical_repr(1 / 3) == "0.333333333"
    assert H.canonical_repr(1234567.891234) == "1234567.89"
    assert H.canonical_repr(1.0000000004) == "1.0"
    assert H.canonical_repr(1.00000001) != H.canonical_repr(1.0)
    assert H.canonical_repr([0.1 + 0.2, (1 / 3,)]) == "[0.3, (0.333333333,)]"


def test_special_floats_and_zero():
    assert H.canonical_repr(float("nan")) == "nan"
    assert H.canonical_repr(float("inf")) == "inf" and H.canonical_repr(-math.inf) == "-inf"
    assert H.canonical_repr(-0.0) == H.canonical_repr(0.0) == "0.0"
    assert H.canonical_repr(complex(0.1 + 0.2, 1)) == "complex(0.3,1.0)"


def test_types_stay_distinct():
    reprs = {H.canonical_repr(v) for v in [1, 1.0, True, "1", [1], (1,), {1}, None]}
    assert len(reprs) == 8


def test_sets_and_dicts_are_order_independent():
    assert H.canonical_repr({3, 1, 2}) == H.canonical_repr({2, 3, 1}) == "set{1, 2, 3}"
    assert H.canonical_repr({"b": 1, "a": 2}) == H.canonical_repr({"a": 2, "b": 1})
    assert H.canonical_repr(frozenset({1})) != H.canonical_repr({1})


def test_memory_addresses_are_masked_and_long_values_hashed():
    class Opaque:
        pass

    a, b = H.canonical_repr(Opaque()), H.canonical_repr(Opaque())
    assert a == b and "0x?" in a
    big = H.canonical_repr("x" * 50_000)
    assert big.startswith("long:") and len(big) < 100
    assert H.canonical_repr("x" * 50_000) == big


def test_numpy_values_use_tolist():
    import numpy as np

    assert H.canonical_repr(np.array([1.0, 2.0])) == "[1.0, 2.0]"
    assert H.canonical_repr(np.float64(0.1 + 0.2)) == "0.3"


def test_exception_tokens_cannot_collide_with_values():
    assert H.exception_token(ValueError("x")) == "!ValueError"
    assert H.exception_token(H.TimeoutException()) == "!Timeout"
    assert not H.canonical_repr("!ValueError").startswith("!")


def test_stdout_normalization():
    assert H.normalize_stdout_text("1.0000000001 2\n  3.50 \n") == "1.0 2\n3.5"
    assert H.normalize_stdout_text("abc  def\n") == "abc def"
    assert H.normalize_stdout_text("12345678901234567890") == "12345678901234567890"   # integers are untouched


def test_signature_json_round_trip():
    from pipeline.execute.labels import signature_from_json, signature_to_json

    sig = ("[1, 2]", "!ValueError", "'a\"b'")
    assert signature_from_json(signature_to_json(sig)) == sig
    assert signature_to_json(None) is None and signature_from_json(None) is None
