"""Extra HumanEval+/MBPP+ checks on downloaded assets (data read only, nothing executed).

Usage: python3 -I heplus_extra.py CACHE_EVALPLUS_DIR
Prints: v0.1.9 -> v0.1.10 per-task plus_input counts for changed tasks;
whether Mini plus inputs are a subset of full base+plus inputs; whether
NoExtreme inputs are a subset of full inputs; tasks with zero plus inputs.
"""
import gzip
import json
import sys
from pathlib import Path


def load(p):
    with gzip.open(p, "rt", encoding="utf-8") as f:
        return {r["task_id"]: r for r in (json.loads(l) for l in f if l.strip())}


def canon(x):
    return json.dumps(x, sort_keys=True)


def main():
    root = Path(sys.argv[1])
    o = load(root / "heplus_v0.1.9/HumanEvalPlus.jsonl.gz")
    n = load(root / "heplus_v0.1.10/HumanEvalPlus.jsonl.gz")
    for t in ["HumanEval/1", "HumanEval/28", "HumanEval/99", "HumanEval/160"]:
        print(t, "plus v0.1.9", len(o[t]["plus_input"]), "plus v0.1.10", len(n[t]["plus_input"]),
              "contract changed", o[t]["contract"] != n[t]["contract"])
    for t in ["HumanEval/99", "HumanEval/160"]:
        print("CONTRACT", t, "\n  old:", repr(o[t]["contract"])[:300], "\n  new:", repr(n[t]["contract"])[:300])
    for ds, full_p, sub_ps in [
        ("HE+ v0.1.10", "heplus_v0.1.10/HumanEvalPlus.jsonl.gz",
         ["heplus_v0.1.10/HumanEvalPlus-Mini.jsonl.gz", "heplus_v0.1.10/HumanEvalPlus-NoExtreme.jsonl.gz"]),
        ("MBPP+ v0.2.0", "mbppplus_v0.2.0/MbppPlus.jsonl.gz", ["mbppplus_v0.2.0/MbppPlus-NoExtreme.jsonl.gz"]),
    ]:
        full = load(root / full_p)
        for sp in sub_ps:
            sub = load(root / sp)
            bad_plus = 0
            bad_base = 0
            for t, r in sub.items():
                fp = {canon(x) for x in full[t]["plus_input"]}
                fb = {canon(x) for x in full[t]["base_input"]}
                bad_plus += sum(1 for x in r["plus_input"] if canon(x) not in fp)
                bad_base += sum(1 for x in r["base_input"] if canon(x) not in fb)
            print(ds, Path(sp).name, "plus inputs not in full plus:", bad_plus, "base not in full base:", bad_base)
        zero = sorted((t for t, r in full.items() if len(r["plus_input"]) == 0), key=lambda s: int(s.split("/")[1]))
        dup = sum(len(r["plus_input"]) - len({canon(x) for x in r["plus_input"]}) for r in full.values())
        overlap = sum(len({canon(x) for x in r["plus_input"]} & {canon(x) for x in r["base_input"]}) for r in full.values())
        print(ds, "tasks with zero plus inputs:", len(zero), zero[:30])
        print(ds, "duplicate plus inputs within task:", dup, "plus inputs equal to a base input:", overlap)


if __name__ == "__main__":
    main()
