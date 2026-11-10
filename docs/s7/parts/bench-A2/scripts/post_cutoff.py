"""Count LiveCodeBench code_generation_lite problems after a cutoff date.

Reads the per-problem index written by lcb_stream_index.py (one
<shard>.index.jsonl per shard; no problem text). A problem counts as
post-cutoff when the calendar day of its contest_date is strictly after
CUTOFF (contest_date values are ISO datetimes; the day part is compared).

Usage:
  python3 -I post_cutoff.py CUTOFF [--end END] [--release release_v6]
                            [--index-dir DIR] [--json]
  CUTOFF, END: YYYY-MM-DD. With --end, also counts problems whose day is
  strictly after CUTOFF and on or before END.
  --release: a release tag from the official loader (release_v1..release_v6,
  release_latest, v1..v6, or vI_vJ). Default release_v6.
"""
import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path

SHARDS = ["test.jsonl", "test2.jsonl", "test3.jsonl", "test4.jsonl", "test5.jsonl", "test6.jsonl"]


def shards_for(release):
    if release == "release_latest":
        return SHARDS
    if release.startswith("release_v"):
        return SHARDS[: int(release[len("release_v"):])]
    if "_" in release:
        a, b = release.split("_")
        return SHARDS[int(a[1:]) - 1: int(b[1:])]
    return [SHARDS[int(release[1:]) - 1]]


def day(s):
    return dt.date.fromisoformat(s[:10])


def main():
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("cutoff")
    ap.add_argument("--end")
    ap.add_argument("--release", default="release_v6")
    ap.add_argument("--index-dir", default=str(here / "cache" / "lcb_index"))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    cutoff = dt.date.fromisoformat(a.cutoff)
    end = dt.date.fromisoformat(a.end) if a.end else None
    rows = []
    for s in shards_for(a.release):
        p = Path(a.index_dir) / f"{s[:-6]}.index.jsonl"
        if not p.exists():
            sys.exit(f"missing index {p}; run lcb_stream_index.py first")
        rows += [json.loads(l) for l in p.open() if l.strip()]
    after = [r for r in rows if day(r["contest_date"]) > cutoff]
    by_month = collections.Counter(r["contest_date"][:7] for r in after)
    by_platform = collections.Counter(r["platform"] for r in after)
    by_diff = collections.Counter(r["difficulty"] for r in after)
    out = {
        "release": a.release, "shards": shards_for(a.release), "total": len(rows),
        "cutoff": a.cutoff, "rule": "day(contest_date) > cutoff",
        "post_cutoff": len(after), "pre_or_on_cutoff": len(rows) - len(after),
        "by_month": dict(sorted(by_month.items())),
        "by_platform": dict(sorted(by_platform.items())),
        "by_difficulty": dict(sorted(by_diff.items())),
        "post_cutoff_with_empty_private": sum(1 for r in after if not r["n_private"]),
    }
    if after:
        out["first_post_day"] = min(r["contest_date"][:10] for r in after)
        out["last_post_day"] = max(r["contest_date"][:10] for r in after)
    if end:
        win = [r for r in after if day(r["contest_date"]) <= end]
        out["window_end"] = a.end
        out["window_count"] = len(win)
        out["window_by_month"] = dict(sorted(collections.Counter(r["contest_date"][:7] for r in win).items()))
    if a.json:
        print(json.dumps(out, indent=1))
    else:
        for k, v in out.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
