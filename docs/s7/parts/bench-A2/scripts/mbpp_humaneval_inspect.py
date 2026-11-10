"""Count MBPP (full, sanitized) and HumanEval rows; relate MBPP+ IDs to sanitized splits.

Usage: python3 -I mbpp_humaneval_inspect.py CACHE_DIR OUT_JSON
Reads JSON and parquet data only; executes nothing from the files.
"""
import gzip
import json
import sys
from pathlib import Path

import pyarrow.parquet as pq


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    res = {}
    he = pq.read_table(root / "hf_humaneval/test-00000-of-00001.parquet").to_pylist()
    res["humaneval"] = {"rows": len(he), "columns": sorted(he[0].keys()),
                        "first_id": he[0]["task_id"], "last_id": he[-1]["task_id"],
                        "unique_ids": len({r["task_id"] for r in he})}
    hf = {}
    for kind in ("full", "sanitized"):
        for s in ("prompt", "test", "train", "validation"):
            rows = pq.read_table(root / f"hf_mbpp/{kind}-{s}.parquet").to_pylist()
            ids = sorted(r["task_id"] for r in rows)
            hf[f"{kind}/{s}"] = {"rows": len(rows), "min_id": ids[0], "max_id": ids[-1], "ids": ids}
    san = json.loads((root / "gh_mbpp/sanitized-mbpp.json").read_text())
    san_ids = sorted(r["task_id"] for r in san)
    full_lines = [l for l in (root / "gh_mbpp/mbpp.jsonl").read_text().splitlines() if l.strip()]
    res["gh_sanitized_json"] = {"rows": len(san), "unique_ids": len(set(san_ids)),
                                "min_id": san_ids[0], "max_id": san_ids[-1]}
    res["gh_full_jsonl"] = {"rows": len(full_lines)}
    hf_san_all = sorted(i for k, v in hf.items() if k.startswith("sanitized/") for i in v["ids"])
    res["hf_sanitized_total"] = len(hf_san_all)
    res["hf_sanitized_equals_gh_sanitized_ids"] = hf_san_all == san_ids
    plus = {}
    for ver in ("v0.1.0", "v0.2.0"):
        with gzip.open(root / f"evalplus/mbppplus_{ver}/MbppPlus.jsonl.gz", "rt") as f:
            ids = sorted(int(json.loads(l)["task_id"].split("/")[1]) for l in f if l.strip())
        by_split = {}
        for k, v in hf.items():
            if k.startswith("sanitized/"):
                by_split[k] = len(set(ids) & set(v["ids"]))
        plus[ver] = {"n": len(ids), "in_sanitized": len(set(ids) & set(san_ids)),
                     "not_in_sanitized": sorted(set(ids) - set(san_ids)),
                     "by_sanitized_split": by_split}
    res["mbppplus_vs_sanitized"] = plus
    res["sanitized_not_in_mbppplus_v010"] = sorted(set(san_ids) - set(
        int(x) for x in []) - set())  # placeholder replaced below
    v010 = set()
    with gzip.open(root / "evalplus/mbppplus_v0.1.0/MbppPlus.jsonl.gz", "rt") as f:
        v010 = {int(json.loads(l)["task_id"].split("/")[1]) for l in f if l.strip()}
    res["sanitized_not_in_mbppplus_v010"] = sorted(set(san_ids) - v010)
    for v in hf.values():
        v["ids"] = f"{len(v['ids'])} ids"
    res["hf_mbpp"] = hf
    out.write_text(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
