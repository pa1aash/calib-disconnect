"""Summarize the LiveCodeBench per-problem index by shard and by release.

Usage: python3 -I lcb_summarize.py INDEX_DIR OUT_JSON
"""
import collections
import json
import sys
from pathlib import Path

SHARDS = ["test.jsonl", "test2.jsonl", "test3.jsonl", "test4.jsonl", "test5.jsonl", "test6.jsonl"]


def summ(rows):
    days = sorted(r["contest_date"] for r in rows)
    return {
        "problems": len(rows),
        "first_contest_date": days[0], "last_contest_date": days[-1],
        "platform": dict(collections.Counter(r["platform"] for r in rows)),
        "difficulty": dict(collections.Counter(r["difficulty"] for r in rows)),
        "private_encoding": dict(collections.Counter(r["private_encoding"] for r in rows)),
        "private_decode_errors": sum(1 for r in rows if r["private_error"]),
        "empty_private": sum(1 for r in rows if r["n_private"] == 0),
        "empty_public": sum(1 for r in rows if r["n_public"] == 0),
        "n_private_total": sum(r["n_private"] or 0 for r in rows),
        "n_private_min": min(r["n_private"] or 0 for r in rows),
        "n_public_total": sum(r["n_public"] for r in rows),
        "testtype": dict(collections.Counter("+".join(r["public_testtypes"]) or "none" for r in rows)),
        "functional_with_func_name": sum(1 for r in rows if r["func_name"]),
        "non_midnight_times": sum(1 for r in rows if r["contest_date"][10:] not in ("T00:00:00", "")),
        "unique_question_ids": len({r["question_id"] for r in rows}),
        "key_sets": dict(collections.Counter(",".join(r["keys"]) for r in rows)),
    }


def main():
    d, out = Path(sys.argv[1]), Path(sys.argv[2])
    by = {s: [json.loads(l) for l in (d / f"{s[:-6]}.index.jsonl").open()] for s in SHARDS}
    res = {"by_shard": {s: summ(r) for s, r in by.items()}, "by_release": {}}
    acc = []
    for i, s in enumerate(SHARDS, 1):
        acc = acc + by[s]
        res["by_release"][f"release_v{i}"] = summ(acc)
    allr = acc
    dup = [q for q, c in collections.Counter(r["question_id"] for r in allr).items() if c > 1]
    res["duplicate_question_ids_release_v6"] = dup
    res["by_month_release_v6"] = dict(sorted(collections.Counter(r["contest_date"][:7] for r in allr).items()))
    # shard ordering: does each shard start after the previous ends?
    res["shard_overlap"] = {
        SHARDS[i]: min(r["contest_date"] for r in by[SHARDS[i]]) <= max(r["contest_date"] for r in by[SHARDS[i - 1]])
        for i in range(1, len(SHARDS))
    }
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1)[:6000])


if __name__ == "__main__":
    main()
