"""Stream one LiveCodeBench code_generation_lite jsonl shard from stdin.

Computes the SHA-256 and byte size of the raw stream and writes a small
per-problem index (no problem text, no tests) to OUT_INDEX, plus a summary
JSON to OUT_SUMMARY. The shard itself is never stored on disk.

Private tests are decoded as plain JSON, or as base64 -> zlib -> pickle ->
JSON (the format used by the LiveCodeBench runner). The pickle step uses a
restricted unpickler that refuses every global, so no code from the file
can run; a pickled plain string needs no globals.

Usage: curl ... | python3 -I lcb_stream_index.py SHARD_NAME OUT_INDEX OUT_SUMMARY
"""
import base64
import hashlib
import io
import json
import pickle
import sys
import zlib


class NoGlobals(pickle.Unpickler):
    def find_class(self, module, name):  # noqa: D401
        raise pickle.UnpicklingError(f"global refused: {module}.{name}")


def decode_private(s):
    if s is None or s == "":
        return [], "empty_string"
    try:
        v = json.loads(s)
        return v, "json"
    except Exception:
        pass
    raw = zlib.decompress(base64.b64decode(s.encode("utf-8")))
    obj = NoGlobals(io.BytesIO(raw)).load()
    if isinstance(obj, (bytes, bytearray)):
        obj = obj.decode("utf-8")
    return json.loads(obj), "b64_zlib_pickle"


def main():
    shard, out_index, out_summary = sys.argv[1], sys.argv[2], sys.argv[3]
    h = hashlib.sha256()
    size = 0
    n = 0
    rows = []
    stdin = sys.stdin.buffer
    for line in iter(stdin.readline, b""):
        h.update(line)
        size += len(line)
        if line.strip():
            rows.append(index_row(line, shard, n))
            n += 1
    with open(out_index, "w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    summary = {"shard": shard, "bytes": size, "sha256": h.hexdigest(), "problems": n}
    with open(out_summary, "w") as f:
        json.dump(summary, f, indent=1, sort_keys=True)
    print(json.dumps(summary))


def index_row(line, shard, i):
    d = json.loads(line)
    pub = json.loads(d.get("public_test_cases") or "[]")
    try:
        priv, enc = decode_private(d.get("private_test_cases"))
        priv_err = None
    except Exception as e:  # record, never guess
        priv, enc, priv_err = None, "decode_error", repr(e)[:200]
    meta = {}
    try:
        meta = json.loads(d.get("metadata") or "{}")
    except Exception:
        pass
    types = sorted({t.get("testtype") for t in pub if isinstance(t, dict)})
    return {
        "shard": shard,
        "line": i,
        "keys": sorted(d.keys()),
        "question_id": d.get("question_id"),
        "contest_id": d.get("contest_id"),
        "platform": d.get("platform"),
        "contest_date": d.get("contest_date"),
        "difficulty": d.get("difficulty"),
        "has_starter_code": bool(d.get("starter_code")),
        "n_public": len(pub),
        "public_testtypes": types,
        "n_private": None if priv is None else len(priv),
        "private_encoding": enc,
        "private_error": priv_err,
        "func_name": meta.get("func_name") if isinstance(meta, dict) else None,
    }


if __name__ == "__main__":
    main()
