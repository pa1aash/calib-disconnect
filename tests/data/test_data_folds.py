"""Near-duplicate grouping on hand-made cases and fold properties."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from pipeline.contracts import constants, hashing
from pipeline.contracts.schemas import FoldPlan, NearDuplicateGroup, Problem
from pipeline.data import folds as fl


def P(pid, prompt="", solution=None, bench=None):
    bench = bench or ("humaneval_plus" if pid.startswith("HumanEval") else "mbpp_plus")
    return Problem(problem_id=pid, benchmark=bench, prompt=prompt, entry_point="f", canonical_solution=solution,
                   io_kind="function", release_date=None)


# ---- near duplicates ----------------------------------------------------------------------------
def test_ast_identical_after_unparse():
    a = P("Mbpp/1", "alpha beta", "def f(x):\n  return x+1\n")
    b = P("Mbpp/2", "gamma delta", "def f( x ):\n    return (x + 1)  # comment\n")
    c = P("Mbpp/3", "epsilon zeta", "def f(x):\n    return x + 2\n")
    g = fl.near_duplicate_groups([c, b, a])
    assert g == [NearDuplicateGroup(group_key="Mbpp/1", members=("Mbpp/1", "Mbpp/2"), reasons=("ast_identical",))]


def test_jaccard_threshold_is_inclusive_at_point_eight():
    base = "one two three four five six seven eight nine ten"
    a = P("Mbpp/1", base, "def f(x):\n    return 1\n")
    # 10 shared tokens + 2 extra -> union 12 -> 10/12 = 0.83 >= 0.8
    b = P("Mbpp/2", base + " extra1 extra2", "def f(x):\n    return 2\n")
    # exactly 0.8: 8 shared of 10 total -> 8/10
    c = P("Mbpp/3", "one two three four five six seven eight", "def f(x):\n    return 3\n")
    d = P("Mbpp/4", "one two three four five six seven eight x y z w", "def f(x):\n    return 4\n")
    assert fl.jaccard(fl.tokens(base), fl.tokens("one two three four five six seven eight")) == pytest.approx(0.8)
    g = fl.near_duplicate_groups([a, b, c, d])
    assert [x.members for x in g] == [("Mbpp/1", "Mbpp/2", "Mbpp/3")]  # d: 8/12 < 0.8 to c, 8/12 to others
    assert g[0].reasons == ("jaccard>=0.8",)
    assert fl.jaccard(fl.tokens("a b c d e f g h i j"), fl.tokens("a b c d e f g h i j k l m")) < 0.8


def test_tokens_are_lowercase_word_characters():
    assert fl.tokens("Find the MAX, of [1, 2]!") == {"find", "the", "max", "of", "1", "2"}
    assert fl.jaccard(frozenset(), frozenset()) == 0.0


def test_cross_benchmark_pairs_are_grouped_and_key_is_smallest_id():
    he = P("HumanEval/9", "compute the running sum of numbers in a list", "def f(x):\n    return x\n")
    mb = P("Mbpp/5", "Compute the running sum of numbers in a list", "def f(x):\n    return x\n")
    g = fl.near_duplicate_groups([mb, he])
    assert len(g) == 1 and g[0].group_key == "HumanEval/9"  # "H" < "M" in string order
    assert g[0].members == ("HumanEval/9", "Mbpp/5") and g[0].reasons == ("ast_identical", "jaccard>=0.8")


def test_humaneval_pairs_are_counted_not_grouped():
    a = P("HumanEval/1", "same words here for both", "def f(x):\n    return x\n")
    b = P("HumanEval/2", "same words here for both", "def f(x):\n    return x\n")
    rep = fl.near_duplicate_report([a, b])
    assert rep.groups == []
    assert rep.diagnostics["humaneval_humaneval_pairs_not_grouped"] == {"any": 1, "ast_identical": 1, "jaccard": 1}
    # but a shared MBPP+ neighbor links them through the component
    m = P("Mbpp/1", "same words here for both", "def f(x):\n    return x\n")
    rep = fl.near_duplicate_report([a, b, m])
    assert [g.members for g in rep.groups] == [("HumanEval/1", "HumanEval/2", "Mbpp/1")]


def test_components_are_transitive_and_lcb_is_ignored():
    a = P("Mbpp/10", "x1 x2 x3 x4 x5", "def f():\n    return 1\n")
    b = P("Mbpp/11", "x1 x2 x3 x4 x5 x6", "def f():\n    return 2\n")        # 5/6 to a
    c = P("Mbpp/12", "x1 x2 x3 x4 x5 x6 x7", "def f():\n    return 3\n")     # 6/7 to b, 5/7 to a
    lcb = Problem("lcb/q", "lcb_v6", "x1 x2 x3 x4 x5", "f", None, "stdin", "2024-01-01")
    g = fl.near_duplicate_groups([a, b, c, lcb])
    assert [x.members for x in g] == [("Mbpp/10", "Mbpp/11", "Mbpp/12")]
    assert fl.near_duplicate_groups([a, lcb]) == []


def test_unparseable_solution_never_matches_by_ast():
    a = P("Mbpp/1", "aa", "def f(:")
    b = P("Mbpp/2", "bb", "def f(:")
    assert fl.near_duplicate_groups([a, b]) == []
    assert fl.near_duplicate_groups([P("Mbpp/1", "aa", None), P("Mbpp/2", "bb", None)]) == []


# ---- folds --------------------------------------------------------------------------------------
def test_fold_hand_computed_and_ungrouped_uses_own_id():
    plan = fl.build_folds(["HumanEval/0", "Mbpp/2"], [], 3, "label_validity")
    assert plan.assignment == {"HumanEval/0": hashing.fold_of(3, "HumanEval/0"), "Mbpp/2": hashing.fold_of(3, "Mbpp/2")}
    assert plan.n_folds == constants.N_FOLDS == 5 and plan.population == "label_validity" and plan.fold_seed == 3


def test_group_uses_group_key_even_when_key_problem_is_absent():
    g = NearDuplicateGroup("Mbpp/1", ("Mbpp/1", "Mbpp/2"), ("ast_identical",))
    full = fl.build_folds(["Mbpp/1", "Mbpp/2", "Mbpp/3"], [g], 0, "label_validity")
    sub = fl.build_folds(["Mbpp/2", "Mbpp/3"], [g], 0, "label_validity")
    assert full.assignment["Mbpp/2"] == full.assignment["Mbpp/1"] == hashing.fold_of(0, "Mbpp/1")
    assert sub.assignment["Mbpp/2"] == full.assignment["Mbpp/2"]
    assert fl.build_folds(["Mbpp/3"], [g], 0, "label_validity").groups == ()


def test_duplicate_ids_and_overlapping_groups_rejected():
    with pytest.raises(ValueError):
        fl.build_folds(["a", "a"], [], 0, "p")
    g1 = NearDuplicateGroup("a", ("a", "b"), ())
    g2 = NearDuplicateGroup("c", ("b", "c"), ())
    with pytest.raises(ValueError):
        fl.build_folds(["a", "b", "c"], [g1, g2], 0, "p")


def _groups_from(ids, picks):
    """Disjoint groups from a list of index tuples."""
    used, groups = set(), []
    for pick in picks:
        members = sorted({ids[i % len(ids)] for i in pick} - used)
        if len(members) > 1:
            used.update(members)
            groups.append(NearDuplicateGroup(members[0], tuple(members), ("ast_identical",)))
    return groups


ids_st = st.lists(st.integers(0, 400), min_size=1, max_size=120, unique=True).map(lambda xs: [f"Mbpp/{x}" for x in xs])
picks_st = st.lists(st.lists(st.integers(0, 500), min_size=2, max_size=5), max_size=15)


@settings(max_examples=60, deadline=None)
@given(ids=ids_st, picks=picks_st, seed=st.integers(0, 10))
def test_fold_properties(ids, picks, seed):
    groups = _groups_from(ids, picks)
    plan = fl.build_folds(ids, groups, seed, "label_validity")
    # every problem in exactly one fold, folds in range
    assert set(plan.assignment) == set(ids)
    assert all(0 <= f < 5 for f in plan.assignment.values())
    total = sum(len(plan.problems_in([f])) for f in range(5))
    assert total == len(ids)
    # every group lands in one fold
    for g in groups:
        assert len({plan.assignment[m] for m in g.members}) == 1
    # same IDs (any order) give the same plan
    again = fl.build_folds(list(reversed(ids)), list(reversed(groups)), seed, "label_validity")
    assert again.assignment == plan.assignment and again.to_dict() == plan.to_dict()
    # inner splits never include an outer-test problem; train/validation are disjoint and cover the train set
    for outer in range(5):
        test = set(plan.outer_test(outer))
        train = set(plan.outer_train(outer))
        assert not test & train and test | train == set(ids)
        splits = plan.inner_splits(outer)
        assert len(splits) == 4
        for tr, va in splits:
            assert not (set(tr) | set(va)) & test
            assert not set(tr) & set(va) and set(tr) | set(va) == train
        assert sorted(sum((va for _, va in splits), [])) == sorted(train)
    assert FoldPlan.from_dict(plan.to_dict()).assignment == plan.assignment


@settings(max_examples=30, deadline=None)
@given(ids=ids_st, seed=st.integers(0, 5))
def test_subset_assignment_is_consistent_with_full(ids, seed):
    full = fl.build_folds(ids, [], seed, "p")
    half = fl.build_folds(ids[::2], [], seed, "p")
    assert all(full.assignment[k] == v for k, v in half.assignment.items())


def test_fold_balance_is_reasonable_on_real_sized_population():
    ids = [f"HumanEval/{i}" for i in range(164)] + [f"Mbpp/{i}" for i in range(2, 400)]
    plan = fl.build_folds(ids, [], 0, "label_validity")
    sizes = [len(plan.problems_in([f])) for f in range(5)]
    assert min(sizes) > 0.6 * len(ids) / 5
