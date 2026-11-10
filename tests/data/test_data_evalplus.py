"""HumanEval+ and MBPP+: counts, removed IDs, the pinned patch, and suites."""

from __future__ import annotations

import copy
import shutil

import pytest

from data_helpers import CACHE, needs_cache
from pipeline.contracts import constants
from pipeline.contracts.schemas import Problem, TestSuite
from pipeline.data import evalplus_data as ed
from pipeline.data import pins as pm
from pipeline.data.inputs import canonical_repr, decode_inputs, encode_input

pytestmark = needs_cache


def test_counts(he_problems, mbpp_problems):
    assert len(he_problems) == 164 and len(mbpp_problems) == 378
    assert all(p.benchmark == "humaneval_plus" and p.problem_id.startswith("HumanEval/") for p in he_problems)
    assert all(p.benchmark == "mbpp_plus" and p.problem_id.startswith("Mbpp/") for p in mbpp_problems)
    assert len({p.problem_id for p in he_problems}) == 164
    assert all(p.io_kind == "function" and p.release_date is None for p in he_problems + mbpp_problems)


def test_removed_ids_absent(mbpp_problems):
    ids = {p.problem_id for p in mbpp_problems}
    assert len(constants.MBPP_PLUS_REMOVED_IDS) == 21
    assert not ids & set(constants.MBPP_PLUS_REMOVED_IDS)
    assert set(constants.MBPP_PATCHED_IDS) <= ids


def test_problem_fields(he_problems, mbpp_problems):
    p = he_problems[0]
    assert p.problem_id == "HumanEval/0" and p.entry_point == "has_close_elements"
    assert p.canonical_solution.startswith(p.prompt)  # complete program
    compile(p.canonical_solution, "x", "exec")
    assert p.source_sha256 == pm.PINS["humaneval_plus"].sha256
    m = next(q for q in mbpp_problems if q.problem_id == "Mbpp/2")
    assert m.source_sha256 == pm.PINS["mbpp_plus"].sha256 and "similar_elements" in m.entry_point
    assert Problem.from_dict(m.to_dict()) == m


def test_patch_equals_pinned_fix_script_and_changes_exactly_three(cache_dir):
    """The pinned file is trusted benchmark tooling (SHA-256 verified), so executing its fix() is allowed."""
    raw, _, patch_sha = ed.read_mbpp_plus_raw(cache_dir)
    assert patch_sha == pm.PINS["mbpp_plus_patch"].sha256
    path = pm.locate_verified(pm.PINS["mbpp_plus_patch"], cache_dir)
    ns: dict = {}
    exec(compile(path.read_text(), str(path), "exec"), ns)
    expected = ns["fix"](copy.deepcopy(raw))
    mine = ed.apply_mbpp_patch(raw)
    assert mine == expected
    changed = [a["task_id"] for a, b in zip(raw, mine) if a != b]
    assert sorted(changed) == sorted(constants.MBPP_PATCHED_IDS)
    assert [r["task_id"] for r in mine] == [r["task_id"] for r in raw]
    for a, b in zip(raw, mine):  # only the canonical solution differs
        if a != b:
            assert {k for k in a if a[k] != b[k]} == {"canonical_solution"}


def test_patch_input_not_mutated_and_id_check(cache_dir):
    raw, _, _ = ed.read_mbpp_plus_raw(cache_dir)
    before = copy.deepcopy(raw)
    ed.apply_mbpp_patch(raw)
    assert raw == before
    swapped = copy.deepcopy(raw)
    swapped[215], swapped[55] = swapped[55], swapped[215]  # IDs no longer at the patched row indices
    with pytest.raises(AssertionError):
        ed.apply_mbpp_patch(swapped)


def test_patched_flag(mbpp_problems):
    flagged = sorted(p.problem_id for p in mbpp_problems if p.patched)
    assert flagged == sorted(constants.MBPP_PATCHED_IDS)
    new = {p.problem_id: p.canonical_solution for p in mbpp_problems}
    assert "c.isupper()" in new["Mbpp/459"] and "components[0]" in new["Mbpp/102"] and "arr[0]" in new["Mbpp/559"]


def test_loader_refuses_tampered_file(tmp_path):
    from pipeline.data.loader import DataLoader

    src = pm.locate_verified(pm.PINS["humaneval_plus"], CACHE)
    dst = tmp_path / pm.PINS["humaneval_plus"].relpath
    dst.parent.mkdir(parents=True)
    data = bytearray(src.read_bytes())
    data[100] ^= 1  # flip one bit; byte count unchanged
    dst.write_bytes(bytes(data))
    with pytest.raises(pm.PinError):
        DataLoader(tmp_path).problems("humaneval_plus")
    assert DataLoader(tmp_path).verify_pins(("humaneval_plus",)) == [(str(dst), False)]
    with pytest.raises(pm.PinError):  # missing files raise
        DataLoader(tmp_path).verify_pins(("mbpp_plus",))


def test_verify_pins_all_true(loader):
    res = loader.verify_pins()
    assert len(res) == 3 and all(ok for _, ok in res)


def test_suites(loader, he_problems, mbpp_problems):
    p = he_problems[0]
    s = loader.suites(p)
    assert set(s) == {"O", "E"}
    assert len(s["O"].inputs) == len(loader._rows[p.problem_id]["base_input"]) == 7 and len(s["E"].inputs) > len(s["O"].inputs)
    assert s["E"].inputs[: len(s["O"].inputs)] == s["O"].inputs  # E = base + plus, in that order
    for ts in s.values():
        assert ts.expected is None and ts.problem_id == p.problem_id
        assert ts.time_limit_rule == "evalplus==0.3.1:max(1.0, 4.0*ref_time)"
        assert TestSuite.from_dict(ts.to_dict()) == ts
    assert s["O"].input_set_sha256 != s["E"].input_set_sha256 and len(s["O"].input_set_sha256) == 64
    # atol is carried per problem
    atols = {loader.suites(q)["E"].atol for q in he_problems + mbpp_problems}
    assert atols >= {0.0, 1e-6} or atols >= {0.0, 1e-4}
    n = [len(loader.suites(q)["E"].inputs) for q in he_problems]
    assert 600 < sum(n) / len(n) < 900  # about 748 plus inputs per HumanEval task


def test_time_limit_rule_matches_evalplus_config():
    import evalplus.config as cfg

    assert (cfg.DEFAULT_MIN_TIME_LIMIT, cfg.DEFAULT_GT_TIME_LIMIT_FACTOR) == (1.0, 4.0)
    assert ed.TIME_LIMIT_RULE == f"evalplus=={constants.EVALPLUS_TOOL_VERSION}:max(1.0, 4.0*ref_time)"


def test_mbpp_inputs_decode_to_evalplus_form(loader, mbpp_problems):
    from evalplus.data.mbpp import mbpp_deserialize_inputs

    for pid in ("Mbpp/2", "Mbpp/124", "Mbpp/252", "Mbpp/75"):
        p = next(q for q in mbpp_problems if q.problem_id == pid)
        s = loader.suites(p)["E"]
        got = decode_inputs(pid, s.inputs)
        want = [list(x) for x in mbpp_deserialize_inputs(pid, [list(i) for i in s.inputs])]
        assert got == want
    two = decode_inputs("Mbpp/2", loader.suites(next(q for q in mbpp_problems if q.problem_id == "Mbpp/2"))["O"].inputs)
    assert isinstance(two[0][0], tuple)  # lists became tuples where the contract needs them


def test_encode_decode_roundtrip_for_generated_forms():
    for pid, args in (("Mbpp/2", [(1, 2), (3, 4)]), ("HumanEval/0", [[1.5, 2.5], 0.3]),
                      ("Mbpp/124", [1.5, complex(0, 2)]), ("Mbpp/252", [complex(1, 2)])):
        enc = encode_input(pid, args)
        back = decode_inputs(pid, [enc])[0]
        assert canonical_repr(back) == canonical_repr(args), pid


def test_patched_contract_adaptation(cache_dir):
    """The pinned patch renames parameters of Mbpp/102 and Mbpp/559; the stored contract then raises
    NameError. The generation contract is renamed and re-indented so the filter still works."""
    from evalplus.gen.util import trusted_check_exec

    from pipeline.data import agreement as agr

    raw, _, _ = ed.read_mbpp_plus_raw(cache_dir)
    pat = ed.apply_mbpp_patch(raw)
    gc = ed.generation_contracts(raw, pat)
    assert sorted(gc) == sorted(constants.MBPP_PATCHED_IDS)
    for r in pat:
        if r["task_id"] in gc:
            stored = agr.contract_code(r)
            adapted = agr.contract_code({**r, "contract": gc[r["task_id"]]})
            inp = decode_inputs(r["task_id"], r["base_input"][:1])
            assert trusted_check_exec(adapted, inp, r["entry_point"]) is True
            if r["task_id"] != "Mbpp/459":  # 459 keeps its parameter name
                assert trusted_check_exec(stored, inp, r["entry_point"]) is False
