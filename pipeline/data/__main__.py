"""Command line: uv run python -m pipeline.data fetch --benchmark lcb_v6 --dest <dir> [--dry-run]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import pins


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.data")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="download and verify the pinned files of a benchmark")
    f.add_argument("--benchmark", required=True, choices=["lcb_v6", "humaneval_plus", "mbpp_plus"])
    f.add_argument("--dest", required=True, type=Path, help="target directory")
    f.add_argument("--as-cache", action="store_true",
                   help="treat --dest as the bench cache root and use each pin's relative path")
    f.add_argument("--dry-run", action="store_true", help="print the actions only")
    args = ap.parse_args(argv)
    if args.cmd == "fetch":
        for pin in pins.pins_for_benchmark(args.benchmark):
            dest = args.dest / Path(pin.relpath).parent if args.as_cache else args.dest
            pins.fetch(pin, dest, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
