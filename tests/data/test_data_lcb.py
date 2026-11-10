"""LiveCodeBench by ID: the ID list, the restricted unpickler, and a synthetic shard round trip."""

from __future__ import annotations

import base64
import hashlib
import json
import pickle
import zlib

import pytest

from data_helpers import CACHE
from pipeline.contracts import hashing
from pipeline.contracts.schemas import TestSuite
from pipeline.data import lcb
from pipeline.data import pins as pm


def test_id_list_has_1055_ids_and_no_text():
    ids = lcb.load_id_list()
    assert len(ids) == lcb.EXPECTED_N_IDS == 1055
    assert set(ids[0]) == set(lcb.ID_FIELDS)
    assert len({r["question_id"] for r in ids}) == 1055
    assert sum(r["n_private"] for r in ids) == 25492 and min(r["n_private"] for r in ids) == 1
    assert sum(1 for r in ids if r["n_private"] < 5) == 18
    assert {r["io_kind"] for r in ids} == {"function", "stdin"}
    assert min(r["contest_date"] for r in ids) == "2023-05-07" and max(r["contest_date"] for r in ids) == "2025-04-06"
    assert all(len(r["contest_date"]) == 10 for r in ids)
    raw = lcb.IDS_PATH.read_text()
    assert "question_content" not in raw and "private_test_cases" not in raw


def test_id_list_matches_cache_index_when_present():
    idx = CACHE / "lcb_index"
    if not idx.is_dir():
        pytest.skip("index absent")
    built = lcb.build_id_list(idx)
    assert built["ids"] == lcb.load_id_list() and built["n"] == 1055


def test_shard_row_counts_in_id_list_match_pins():
    ids = lcb.load_id_list()
    for k in pm.LCB_SHARD_KEYS:
        name = pm.PINS[k].relpath.split("/")[-1]
        rows = [r for r in ids if r["shard"] == name]
        assert len(rows) == pm.PINS[k].rows
        assert sorted(r["line"] for r in rows) == list(range(len(rows)))


# ---- restricted unpickler -----------------------------------------------------------------------
def test_restricted_unpickler_accepts_plain_payloads():
    for obj in ("text", b"bytes", [1, 2.5, "x", None, True], {"a": [1, {"b": 2}]}, (1, 2), {1, 2}, 10**30):
        assert lcb.safe_unpickle(pickle.dumps(obj)) == obj
        if not isinstance(obj, (bytes, set)):  # protocol 0 encodes bytes and sets through a global
            assert lcb.safe_unpickle(pickle.dumps(obj, protocol=0)) == obj


class _Evil:
    def __reduce__(self):
        import os

        return (os.system, ("echo should-never-run",))


def test_restricted_unpickler_rejects_os_system():
    payload = pickle.dumps(_Evil())
    assert b"system" in payload
    with pytest.raises(pickle.UnpicklingError):
        lcb.safe_unpickle(payload)
    with pytest.raises(lcb.RefusedGlobal):
        lcb.safe_unpickle(payload)


def test_malicious_private_field_is_rejected_end_to_end():
    for payload in (pickle.dumps(_Evil()), pickle.dumps(_Evil(), protocol=0), pickle.dumps(_Evil(), protocol=2)):
        field = base64.b64encode(zlib.compress(payload)).decode()
        with pytest.raises(pickle.UnpicklingError):
            lcb.decode_private_tests(field)


def test_other_globals_and_builtins_are_refused_too():
    import collections

    for obj in (collections.OrderedDict(a=1), bytearray(b"x"), slice(1, 2), range(3), complex(1, 2)):
        with pytest.raises(pickle.UnpicklingError):
            lcb.safe_unpickle(pickle.dumps(obj))


def test_decompression_bomb_is_bounded():
    bomb = zlib.compress(b"0" * 5_000_000)
    with pytest.raises(ValueError):
        lcb._bounded_decompress(bomb, limit=1_000_000)
    assert len(lcb._bounded_decompress(bomb, limit=10_000_000)) == 5_000_000


def test_decode_private_json_and_pickled_forms_agree():
    tests = [{"input": "1\n", "output": "2\n", "testtype": "stdin"}, {"input": "3\n", "output": "4\n", "testtype": "stdin"}]
    assert lcb.decode_private_tests(json.dumps(tests)) == tests
    assert lcb.decode_private_tests(lcb.encode_private_tests(tests)) == tests
    assert lcb.decode_private_tests("") == [] and lcb.decode_private_tests(None) == []
    with pytest.raises(ValueError):
        lcb.decode_private_tests(json.dumps({"input": "x"}))


# ---- synthetic shard round trip -----------------------------------------------------------------
def _record(qid, date, n_private, func_name=None, n_public=2):
    kind = "functional" if func_name else "stdin"
    pub = [{"input": f"pub{i}-{qid}", "output": f"po{i}", "testtype": kind} for i in range(n_public)]
    priv = [{"input": f"priv{i}-{qid}", "output": f"vo{i}", "testtype": kind} for i in range(n_private)]
    return {"question_title": "T " + qid, "question_content": "Statement of " + qid, "platform": "atcoder",
            "question_id": qid, "contest_id": "c1", "contest_date": date + "T00:00:00",
            "starter_code": "class Solution:\n    pass" if func_name else "", "difficulty": "easy",
            "public_test_cases": json.dumps(pub), "private_test_cases": lcb.encode_private_tests(priv),
            "metadata": json.dumps({"func_name": func_name} if func_name else {})}


@pytest.fixture()
def synthetic(tmp_path):
    recs = [_record("q_a", "2024-01-02", 20), _record("q_b", "2024-02-03", 3), _record("q_c", "2024-03-04", 10, func_name="solve"),
            _record("q_d", "2024-04-05", 5)]
    shards = {"test.jsonl": recs[:2], "test2.jsonl": recs[2:]}
    pins, ids = {}, []
    cache = tmp_path / "cache"
    (cache / "lcb_v6").mkdir(parents=True)
    for n, (name, rs) in enumerate(shards.items()):
        data = b"".join(json.dumps(r).encode() + b"\n" for r in rs)
        (cache / "lcb_v6" / name).write_bytes(data)
        key = "t" + name
        pins[key] = pm.Pin(key=key, benchmark="LCB", role="pinned", url="", download_url="", revision={},
                           bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), relpath="lcb_v6/" + name, rows=len(rs))
        for line, r in enumerate(rs):
            ids.append({"question_id": r["question_id"], "shard": name, "line": line, "contest_date": r["contest_date"][:10],
                        "platform": "atcoder", "io_kind": "function" if "func_name" in r["metadata"] else "stdin",
                        "n_public": 2, "n_private": len(lcb.decode_private_tests(r["private_test_cases"]))})
    store = lcb.LcbStore(cache, ids=ids, pin_map=pins, shard_keys=list(pins))
    return store, recs, cache, pins


def test_synthetic_round_trip(synthetic):
    store, recs, _, _ = synthetic
    probs = store.problems()
    assert [p.problem_id for p in probs] == ["lcb/q_a", "lcb/q_b", "lcb/q_c", "lcb/q_d"]
    a, c = probs[0], probs[2]
    assert a.benchmark == "lcb_v6" and a.io_kind == "stdin" and a.entry_point is None and a.canonical_solution is None
    assert a.release_date == "2024-01-02" and a.prompt == "Statement of q_a" and a.starter_code is None
    assert c.io_kind == "function" and c.entry_point == "solve" and c.starter_code.startswith("class Solution")

    s = store.suites_for("q_a")
    assert set(s) == {"lcb_public", "lcb_label", "lcb_full", "agree"}
    priv_in = [f"priv{i}-q_a" for i in range(20)]
    sel = hashing.lcb_agreement_indices(priv_in)
    assert len(sel) == 4  # 20 percent of 20
    pub_in = tuple(f"pub{i}-q_a" for i in range(2))
    assert s["lcb_public"].inputs == pub_in and s["lcb_public"].expected == ("po0", "po1")
    assert s["agree"].inputs == tuple(priv_in[i] for i in sel) and s["agree"].expected is None
    assert not set(s["agree"].inputs) & set(pub_in)  # agreement never uses public tests
    label_priv = [x for x in s["lcb_label"].inputs if x not in pub_in]
    assert len(label_priv) == 16 and not set(label_priv) & set(s["agree"].inputs)
    assert s["lcb_label"].inputs[:2] == pub_in
    assert len(s["lcb_label"].expected) == len(s["lcb_label"].inputs)
    assert s["lcb_full"].inputs == pub_in + tuple(priv_in)
    assert set(s["lcb_label"].inputs) | set(s["agree"].inputs) == set(s["lcb_full"].inputs)
    for ts in s.values():
        assert TestSuite.from_dict(json.loads(json.dumps(ts.to_dict()))) == ts
        assert len(ts.input_set_sha256) == 64


def test_zero_agreement_inputs_get_empty_suite():
    assert hashing.lcb_agreement_indices(["only one"]) == []
    z = lcb.record_suites(lcb.LcbRecord("q_z", "t", "c", "atcoder", "c", "2024-01-01T00:00:00", "", "easy", None,
                                        [{"input": "p", "output": "o"}], [{"input": "i", "output": "o"}], "s", "x"))
    assert z["agree"].inputs == () and z["agree"].expected is None
    assert z["lcb_label"].inputs == ("p", "i") and z["lcb_full"].inputs == ("p", "i")


def test_zero_agreement_counted_by_store(synthetic):
    store, recs, cache, pins = synthetic
    one = _record("q_one", "2024-05-06", 1)
    data = json.dumps(one).encode() + b"\n"
    (cache / "lcb_v6" / "test3.jsonl").write_bytes(data)
    pins["test3.jsonl"] = pm.Pin(key="test3.jsonl", benchmark="LCB", role="pinned", url="", download_url="", revision={},
                                 bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), relpath="lcb_v6/test3.jsonl", rows=1)
    ids = store.ids + [{"question_id": "q_one", "shard": "test3.jsonl", "line": 0, "contest_date": "2024-05-06",
                        "platform": "atcoder", "io_kind": "stdin", "n_public": 2, "n_private": 1}]
    st = lcb.LcbStore(cache, ids=ids, pin_map=pins, shard_keys=list(pins))
    s = st.suites_for("q_one")
    assert s["agree"].inputs == () and st.zero_agreement == ["q_one"]
    st.suites_for("q_one")
    assert st.zero_agreement == ["q_one"]  # counted once


def test_store_refuses_tampered_shard(synthetic):
    store, _, cache, pins = synthetic
    f = cache / "lcb_v6" / "test.jsonl"
    b = bytearray(f.read_bytes())
    b[50] ^= 1
    f.write_bytes(bytes(b))
    st = lcb.LcbStore(cache, ids=store.ids, pin_map=pins, shard_keys=list(pins))
    with pytest.raises(pm.PinError):
        st.problems()
    with pytest.raises(pm.PinError):
        st.suites_for("q_a")


def test_store_names_fetch_command_when_shards_absent(tmp_path):
    st = lcb.LcbStore(tmp_path)
    assert len(st.missing_shards()) == 6
    with pytest.raises(pm.PinError, match="pipeline.data fetch --benchmark lcb_v6"):
        st.problems(["1873_A"])
