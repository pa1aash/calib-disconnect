"""Inspect downloaded EvalPlus release assets (untrusted data; never executed).

Usage: python3 -I evalplus_inspect.py CACHE_EVALPLUS_DIR OUT_JSON
Reads only JSON fields; no code from the files is run.
"""
import gzip
import hashlib
import json
import statistics
import sys
from pathlib import Path

FIXES = {
    "Mbpp/459": "def remove_uppercase(str1):\n  return ''.join(c for c in str1 if not c.isupper())",
    "Mbpp/102": "def snake_to_camel(snake_str):\n    components = snake_str.split('_')\n    return components[0] + ''.join(x.title() for x in components[1:])",
    "Mbpp/559": "def max_sub_array_sum(arr, n):\n    max_so_far = arr[0] if len(arr) else 0",
}
FIX_INDEX = {"Mbpp/459": 215, "Mbpp/102": 55, "Mbpp/559": 236}


def load(p):
    with gzip.open(p, "rt", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def stats(xs):
    if not xs:
        return None
    return {
        "n": len(xs), "sum": sum(xs), "mean": round(statistics.mean(xs), 2),
        "median": statistics.median(xs), "min": min(xs), "max": max(xs),
    }


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    res = {"files": {}}
    for p in sorted(root.glob("*/*.jsonl.gz")):
        raw = p.read_bytes()
        rows = load(p)
        info = {
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "rows": len(rows), "keys": sorted(set().union(*[r.keys() for r in rows])),
            "task_ids": [r["task_id"] for r in rows],
        }
        if "base_input" in rows[0]:
            info["base_input_stats"] = stats([len(r["base_input"]) for r in rows])
            info["plus_input_stats"] = stats([len(r["plus_input"]) for r in rows])
            info["total_input_stats"] = stats([len(r["base_input"]) + len(r["plus_input"]) for r in rows])
            info["n_with_contract"] = sum(1 for r in rows if (r.get("contract") or "").strip())
            info["n_atol_nonzero"] = sum(1 for r in rows if r.get("atol"))
        if "MbppPlus" in p.name:
            fx = {}
            for tid, sig in FIXES.items():
                idx = [i for i, r in enumerate(rows) if r["task_id"] == tid]
                if not idx:
                    fx[tid] = {"present": False}
                    continue
                r = rows[idx[0]]
                cs = r.get("canonical_solution", "")
                fx[tid] = {
                    "present": True, "index": idx[0],
                    "index_matches_fix_script": idx[0] == FIX_INDEX[tid],
                    "contains_fixed_solution": sig.strip() in cs,
                    "canonical_solution": cs[:600],
                }
            info["june2024_fix_check"] = fx
        res["files"][str(p.relative_to(root))] = info
    # MBPP+ removed IDs
    a = set(res["files"]["mbppplus_v0.1.0/MbppPlus.jsonl.gz"]["task_ids"])
    b = set(res["files"]["mbppplus_v0.2.0/MbppPlus.jsonl.gz"]["task_ids"])
    key = lambda t: int(t.split("/")[1])
    res["mbppplus_removed_v010_to_v020"] = sorted(a - b, key=key)
    res["mbppplus_added_v010_to_v020"] = sorted(b - a, key=key)
    # Changed canonical solutions / inputs between versions for retained tasks
    def by_id(rel):
        return {r["task_id"]: r for r in load(root / rel)}
    for name, (old, new) in {
        "mbppplus": ("mbppplus_v0.1.0/MbppPlus.jsonl.gz", "mbppplus_v0.2.0/MbppPlus.jsonl.gz"),
        "heplus": ("heplus_v0.1.9/HumanEvalPlus.jsonl.gz", "heplus_v0.1.10/HumanEvalPlus.jsonl.gz"),
    }.items():
        o, n = by_id(old), by_id(new)
        diff = {}
        for tid in sorted(set(o) & set(n), key=key):
            changed = [k for k in sorted(set(o[tid]) | set(n[tid])) if o[tid].get(k) != n[tid].get(k)]
            if changed:
                diff[tid] = changed
        res[f"{name}_changed_fields_{old.split('/')[0]}_to_{new.split('/')[0]}"] = diff
    for f in res["files"].values():
        f["task_ids"] = f"{len(f['task_ids'])} ids"
    out.write_text(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
