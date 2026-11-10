"""Agreement inputs for HumanEval+/MBPP+: determinism, disjointness from label inputs, the cap."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from data_helpers import CACHE, needs_cache
from pipeline.contracts import constants, hashing
from pipeline.data import agreement as agr
from pipeline.data.inputs import canonical_repr, decode_inputs

pytestmark = needs_cache

HE_IDS = ["HumanEval/0", "HumanEval/1", "HumanEval/5"]  # float lists, a string, int lists


@pytest.fixture(scope="module")
def jobs(loader, he_problems, mbpp_problems):
    out = []
    for p in he_problems + mbpp_problems:
        if p.problem_id in HE_IDS + ["Mbpp/2", "Mbpp/102"]:
            s = loader.suites(p)
            out.append((p.problem_id, loader.generation_row(p.problem_id), s["E"].inputs, p))
    return out


def test_problem_seed_uses_tuple_digest():
    want = int.from_bytes(hashing.tuple_digest(("agree", 7, "HumanEval/0"))[:8], "big")
    assert agr.problem_seed(7, "HumanEval/0") == want
    assert agr.problem_seed(7, "HumanEval/0") != agr.problem_seed(8, "HumanEval/0")
    assert agr.problem_seed(7, "HumanEval/0") != agr.problem_seed(7, "HumanEval/1")


def test_deterministic_per_seed_and_disjoint_from_label_inputs(jobs, loader):
    j = [(pid, row, label) for pid, row, label, _ in jobs]
    r1 = agr.run_isolated(j, 0, workers=4)
    r2 = agr.run_isolated(j, 0, workers=2)
    r3 = agr.run_isolated(j, 1, workers=4)
    assert {k: v["inputs"] for k, v in r1.items()} == {k: v["inputs"] for k, v in r2.items()}
    assert any(r1[k]["inputs"] != r3[k]["inputs"] for k in r1)  # a different seed changes the inputs
    for pid, row, label in j:
        res = r1[pid]
        st = res["stats"]
        assert st["status"] == "ok" and 0 < len(res["inputs"]) <= constants.AGREEMENT_INPUT_CAP
        assert st["kept"] == len(res["inputs"])
        assert st["generated"] >= st["kept"] + st["removed_label_duplicates"] + st["removed_self_duplicates"] - 0
        assert st["generated"] == (st["kept"] + st["removed_label_duplicates"] + st["removed_self_duplicates"]
                                   + st["removed_roundtrip"] + st["dropped_over_cap"])
        label_canon = {canonical_repr(a) for a in decode_inputs(pid, row["base_input"] + row["plus_input"])}
        agree_canon = [canonical_repr(a) for a in decode_inputs(pid, res["inputs"])]
        assert not label_canon & set(agree_canon)  # disjoint after canonicalization
        assert len(set(agree_canon)) == len(agree_canon)
        json.dumps(res["inputs"])  # JSON form


def test_agreement_inputs_via_loader_protocol(loader, he_problems):
    p = he_problems[0]
    s = loader.suites(p)
    a = loader.agreement_inputs(p, s, 0)
    assert a.suite_id == "agree" and a.problem_id == p.problem_id and a.expected is None
    assert 0 < len(a.inputs) <= 50 and len(a.input_set_sha256) == 64
    assert loader.agreement_stats[p.problem_id]["kept"] == len(a.inputs)
    base_and_plus = {canonical_repr(x) for x in s["E"].inputs}
    assert not base_and_plus & {canonical_repr(x) for x in a.inputs}


def test_deterministic_across_processes_with_different_hash_seeds():
    """String hash randomization must not change the output (ingredient pools and set mutation)."""
    code = (
        "import json,sys\n"
        "from pipeline.data.loader import DataLoader\n"
        "from pipeline.data import agreement as agr\n"
        f"L=DataLoader({str(CACHE)!r})\n"
        "ps=[p for p in L.problems('humaneval_plus') if p.problem_id in ('HumanEval/1','HumanEval/7','HumanEval/29')]\n"
        "ps+=[p for p in L.problems('mbpp_plus') if p.problem_id in ('Mbpp/7','Mbpp/8')]\n"
        "out={}\n"
        "for p in ps:\n"
        "    s=L.suites(p)\n"
        "    r=agr.compute_agreement(L.generation_row(p.problem_id), s['E'].inputs, 3)\n"
        "    out[p.problem_id]=r['inputs']\n"
        "print(json.dumps(out,sort_keys=True))\n"
    )
    outs = []
    for hs in ("1", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, timeout=240)
        assert r.returncode == 0, r.stderr[-2000:]
        outs.append(r.stdout.strip().splitlines()[-1])
    assert outs[0] == outs[1]
    assert len(json.loads(outs[0])) == 5


def test_hard_timeout_yields_empty_suite_not_an_error(he_problems, loader):
    p = he_problems[0]
    row = loader.generation_row(p.problem_id)
    jobs = [(p.problem_id, row, []), ("HumanEval/1", loader.generation_row("HumanEval/1"), [])]
    # the first job hangs (test hook), is killed, and the worker is replaced; the run still finishes
    res = agr.run_isolated(jobs[:1], 0, workers=1, hard_timeout_s=1.5, _sleep_s=30)
    assert res[p.problem_id]["inputs"] == [] and res[p.problem_id]["stats"]["status"] == "timeout"
    res = agr.run_isolated(jobs, 0, workers=1)
    assert all(r["stats"]["status"] == "ok" for r in res.values())


def test_failure_in_worker_is_caught(loader, he_problems):
    row = loader.generation_row(he_problems[0].problem_id)
    bad = {k: v for k, v in row.items() if k != "base_input"}  # raises KeyError inside the worker
    broken = dict(row, contract="this is not python (")        # every candidate fails the contract check
    res = agr.run_isolated([("HumanEval/0", bad, []), ("HumanEval/1", broken, [])], 0, workers=2)
    assert res["HumanEval/0"]["inputs"] == [] and res["HumanEval/0"]["stats"]["status"].startswith("error")
    assert res["HumanEval/1"]["inputs"] == [] and res["HumanEval/1"]["stats"]["status"] == "empty"
