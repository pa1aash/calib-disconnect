"""Canonicalization used to remove agreement inputs that equal a label input."""

from __future__ import annotations

from pipeline.data.inputs import canonical_repr


def test_float_rounding_to_six_significant_digits():
    assert canonical_repr([1.0000001]) == canonical_repr([1.0000002])
    assert canonical_repr([1.00001]) != canonical_repr([1.00002])
    assert canonical_repr([123456.7]) == canonical_repr([123456.9])  # both round to 123457
    assert canonical_repr([0.1 + 0.2]) == canonical_repr([0.3])
    assert canonical_repr([float("nan")]) == canonical_repr([float("nan")])


def test_lists_keep_order_sets_and_dicts_do_not():
    assert canonical_repr([[1, 2]]) != canonical_repr([[2, 1]])
    assert canonical_repr([{3, 1, 2}]) == canonical_repr([{2, 3, 1}])
    assert canonical_repr([frozenset({"b", "a"})]) == canonical_repr([frozenset({"a", "b"})])
    assert canonical_repr([{"a": 1, "b": 2}]) == canonical_repr([{"b": 2, "a": 1}])
    assert canonical_repr([{1, 2}]) != canonical_repr([[1, 2]])  # a set is not a list


def test_types_and_arity_are_distinguished():
    assert canonical_repr([(1, 2)]) != canonical_repr([[1, 2]])
    assert canonical_repr([1]) != canonical_repr([1.0])
    assert canonical_repr([1, 2]) != canonical_repr([(1, 2)])
    assert canonical_repr([True]) != canonical_repr([1])
    assert canonical_repr(["1"]) != canonical_repr([1])
