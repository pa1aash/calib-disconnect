"""Worker process for pipeline.data.agreement.run_isolated.

Reads one JSON job per line on stdin and writes one result line on stdout. Anything the trusted
benchmark code prints is sent to stderr so that stdout carries only protocol lines.
"""

from __future__ import annotations

import json
import os
import sys
import time
import warnings

from pipeline.data.agreement import READY, RESULT, compute_agreement


def main() -> int:
    warnings.simplefilter("ignore")  # legacy escape sequences in benchmark contract strings
    out = os.fdopen(os.dup(1), "w", buffering=1)
    sys.stdout = sys.stderr
    out.write(READY + "\n")
    for line in sys.stdin:
        if not line.strip():
            continue
        job = json.loads(line)
        try:
            if job.get("sleep_s"):  # test hook: simulate a hung problem
                time.sleep(float(job["sleep_s"]))
            res = compute_agreement(job["row"], job["label"], job["seed"], job["n_generate"], job["cap"])
        except BaseException as e:  # noqa: BLE001 - report any failure to the parent
            res = {"inputs": [], "stats": {"generated": 0, "kept": 0,
                                           "status": f"error: {type(e).__name__}: {str(e)[:200]}"}}
        out.write(RESULT + json.dumps(res) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
