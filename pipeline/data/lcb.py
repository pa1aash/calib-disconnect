"""LiveCodeBench release_v6 by problem ID.

The repository tracks only IDs and counts (lcb_v6_ids.json: no problem text, no tests). Problem text and
tests are read from the six pinned shards in a git-ignored cache directory (see pins.fetch and
`python -m pipeline.data fetch --benchmark lcb_v6 --dest <dir>`).

Test encodings. Public tests are a JSON string. Private tests are JSON, or base64 of zlib of a pickle
of the JSON text. The pickle is read with an unpickler that refuses every global, so only plain
str, bytes, number, list, dict, tuple, and set payloads load; anything that names a callable raises.

Suites. Function inputs are stored as the raw input strings (one JSON argument per line), exactly as
in the shards; stdin inputs are the stdin text. Expected outputs are the raw output strings.
  lcb_public: public tests.
  lcb_label:  public tests plus the private tests NOT selected by hashing.lcb_agreement_indices.
  lcb_full:   public tests plus all private tests (labeling sensitivity only).
  agree:      the selected private inputs only, never public tests; expected=None.
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import pickle
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from pipeline.contracts import constants, hashing
from pipeline.contracts.schemas import Problem, TestSuite

from . import pins as pinmod
from .inputs import input_set_sha256

IDS_PATH = Path(__file__).with_name("lcb_v6_ids.json")
EXPECTED_N_IDS = 1055
LCB_TIME_LIMIT_RULE = "lcb:official-evaluator-default"  # the execute module records the concrete limits
MAX_DECOMPRESSED_BYTES = 2 * 1024**3


# ---------------------------------------------------------------------------------------------------
# Safe decoding of private tests
# ---------------------------------------------------------------------------------------------------
class RefusedGlobal(pickle.UnpicklingError):
    """The pickle names a global (module attribute), which is never allowed here."""


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module: str, name: str) -> Any:  # noqa: D401
        raise RefusedGlobal(f"global refused: {module}.{name}")

    def persistent_load(self, pid: Any) -> Any:
        raise RefusedGlobal("persistent ids are refused")


def safe_unpickle(raw: bytes) -> Any:
    return RestrictedUnpickler(io.BytesIO(raw)).load()


def _bounded_decompress(data: bytes, limit: int = MAX_DECOMPRESSED_BYTES) -> bytes:
    d = zlib.decompressobj()
    out = d.decompress(data, limit + 1)
    if len(out) > limit or d.unconsumed_tail:
        raise ValueError("decompressed private tests exceed the size limit")
    return out + d.flush()


def decode_private_tests(s: str | None) -> list[dict[str, Any]]:
    """Decode a private_test_cases field to a list of {input, output, testtype} dicts."""
    if s is None or s == "":
        return []
    try:
        v = json.loads(s)
    except ValueError:
        raw = _bounded_decompress(base64.b64decode(s.encode("ascii")))
        obj = safe_unpickle(raw)
        if isinstance(obj, (bytes, bytearray)):
            obj = bytes(obj).decode("utf-8")
        v = json.loads(obj) if isinstance(obj, str) else obj
    if not isinstance(v, list):
        raise ValueError("private tests did not decode to a list")
    for t in v:
        if not isinstance(t, dict) or "input" not in t or "output" not in t:
            raise ValueError("malformed private test entry")
    return v


def encode_private_tests(tests: Sequence[Mapping[str, Any]]) -> str:
    """Inverse of decode_private_tests for the pickle form (used to build synthetic fixtures)."""
    payload = pickle.dumps(json.dumps(list(tests)), protocol=pickle.HIGHEST_PROTOCOL)
    return base64.b64encode(zlib.compress(payload)).decode("ascii")


# ---------------------------------------------------------------------------------------------------
# The tracked ID list
# ---------------------------------------------------------------------------------------------------
ID_FIELDS = ("question_id", "shard", "line", "contest_date", "platform", "io_kind", "n_public", "n_private")


def _io_kind(row: Mapping[str, Any]) -> str:
    types = row.get("public_testtypes") or []
    if types:
        return "function" if types[0] == "functional" else "stdin"
    return "function" if row.get("func_name") else "stdin"


def build_id_list(index_dir: Path, shard_order: Sequence[str] | None = None) -> dict[str, Any]:
    """Build the ID list from the metadata-only index files of the bench-A2 cache."""
    names = list(shard_order or [Path(pinmod.PINS[k].relpath).name for k in pinmod.LCB_SHARD_KEYS])
    rows = []
    for shard in names:
        stem = shard.removesuffix(".jsonl")
        for line in Path(index_dir, f"{stem}.index.jsonl").read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            rows.append({"question_id": r["question_id"], "shard": r["shard"], "line": r["line"],
                         "contest_date": r["contest_date"][:10], "platform": r["platform"],
                         "io_kind": _io_kind(r), "n_public": r["n_public"], "n_private": r["n_private"]})
    return {"format": "calib-disconnect/lcb_ids/v1", "benchmark": "lcb_v6", "release": "release_v6",
            "dataset": "livecodebench/code_generation_lite",
            "dataset_commit": pinmod.PINS["lcb_v6_test"].revision["commit"],
            "note": "metadata only: no problem text and no tests",
            "n": len(rows), "ids": rows}


def load_id_list(path: Path = IDS_PATH) -> list[dict[str, Any]]:
    d = json.loads(Path(path).read_text())
    ids = d["ids"]
    if d["n"] != len(ids):
        raise ValueError("ID list count does not match its entries")
    if len({r["question_id"] for r in ids}) != len(ids):
        raise ValueError("duplicate question IDs in the ID list")
    return ids


# ---------------------------------------------------------------------------------------------------
# Reading shards
# ---------------------------------------------------------------------------------------------------
@dataclass
class LcbRecord:
    question_id: str
    title: str
    content: str
    platform: str
    contest_id: str
    contest_date: str
    starter_code: str
    difficulty: str
    func_name: str | None
    public: list[dict[str, Any]]
    private: list[dict[str, Any]]
    shard: str
    shard_sha256: str


def parse_record(line: bytes | str, shard: str, shard_sha256: str, tests: bool = True) -> LcbRecord:
    d = json.loads(line)
    meta = json.loads(d.get("metadata") or "{}")
    pub = json.loads(d.get("public_test_cases") or "[]")
    return LcbRecord(question_id=d["question_id"], title=d.get("question_title", ""),
                     content=d["question_content"], platform=d["platform"], contest_id=d.get("contest_id", ""),
                     contest_date=d["contest_date"], starter_code=d.get("starter_code") or "",
                     difficulty=d.get("difficulty", ""), func_name=(meta.get("func_name") if isinstance(meta, dict) else None),
                     public=pub, private=decode_private_tests(d.get("private_test_cases")) if tests else [],
                     shard=shard, shard_sha256=shard_sha256)


def record_problem(rec: LcbRecord) -> Problem:
    kind = "function" if rec.func_name else "stdin"
    types = {t.get("testtype") for t in rec.public} | {t.get("testtype") for t in rec.private}
    types.discard(None)
    want = "functional" if kind == "function" else "stdin"
    if types and types != {want}:
        raise ValueError(f"{rec.question_id}: test types {sorted(types)} disagree with io kind {kind}")
    return Problem(problem_id=f"lcb/{rec.question_id}", benchmark="lcb_v6", prompt=rec.content,
                   entry_point=rec.func_name if kind == "function" else None, canonical_solution=None,
                   io_kind=kind, release_date=rec.contest_date[:10], starter_code=rec.starter_code or None,
                   source_sha256=rec.shard_sha256, patched=False)


def _suite(pid: str, sid: str, inputs: Sequence[str], outputs: Sequence[str] | None) -> TestSuite:
    inputs = tuple(inputs)
    return TestSuite(problem_id=pid, suite_id=sid, inputs=inputs,
                     expected=None if outputs is None else tuple(outputs), atol=0.0,
                     time_limit_rule=LCB_TIME_LIMIT_RULE, input_set_sha256=input_set_sha256(inputs))


def record_suites(rec: LcbRecord) -> dict[str, TestSuite]:
    """The three label suites and the "agree" suite of one problem."""
    pid = f"lcb/{rec.question_id}"
    pub_in = [t["input"] for t in rec.public]
    pub_out = [t["output"] for t in rec.public]
    priv_in = [t["input"] for t in rec.private]
    priv_out = [t["output"] for t in rec.private]
    sel = hashing.lcb_agreement_indices(priv_in, constants.LCB_AGREEMENT_SHARE)
    sel_set = set(sel)
    keep = [i for i in range(len(priv_in)) if i not in sel_set]
    return {
        "lcb_public": _suite(pid, "lcb_public", pub_in, pub_out),
        "lcb_label": _suite(pid, "lcb_label", pub_in + [priv_in[i] for i in keep],
                            pub_out + [priv_out[i] for i in keep]),
        "lcb_full": _suite(pid, "lcb_full", pub_in + priv_in, pub_out + priv_out),
        "agree": _suite(pid, "agree", [priv_in[i] for i in sel], None),
    }


@dataclass
class LcbStore:
    """Reads LiveCodeBench problems by ID from verified shards.

    A shard is streamed once before any record of it is returned; its SHA-256 and byte count are
    checked against the pin during that pass, and the byte offset of every line is kept (a mismatch
    raises). Records are then read by offset, one at a time, so memory stays small.
    """

    cache_dir: Path
    ids: list[dict[str, Any]] | None = None
    pin_map: Mapping[str, pinmod.Pin] | None = None
    shard_keys: Sequence[str] | None = None
    zero_agreement: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cache_dir = Path(self.cache_dir)
        if self.ids is None:
            self.ids = load_id_list()
        if self.pin_map is None:
            self.pin_map = pinmod.PINS
        self._entries = {r["question_id"]: r for r in self.ids}
        keys = self.shard_keys or pinmod.LCB_SHARD_KEYS
        self._shard_pin = {Path(self.pin_map[k].relpath).name: self.pin_map[k] for k in keys}
        self._line_offsets: dict[str, list[int]] = {}
        self._verified: dict[str, Path] = {}

    # -- paths
    def shard_path(self, shard: str) -> Path | None:
        return pinmod.locate(self._shard_pin[shard], self.cache_dir)

    def missing_shards(self, shards: Iterable[str] | None = None) -> list[str]:
        return [s for s in (shards if shards is not None else self._shard_pin) if self.shard_path(s) is None]

    def fetch_command(self) -> str:
        return f"uv run python -m pipeline.data fetch --benchmark lcb_v6 --dest {self.cache_dir / 'lcb_v6'}"

    # -- reading
    def verify_shard(self, shard: str) -> Path:
        """Hash the whole shard against its pin and index its lines. Raises on any mismatch."""
        if shard in self._verified:
            return self._verified[shard]
        pin = self._shard_pin[shard]
        path = self.shard_path(shard)
        if path is None:
            raise pinmod.PinError(f"LiveCodeBench shard {shard} is not in {self.cache_dir}; run: {self.fetch_command()}")
        h = hashlib.sha256()
        n_bytes = 0
        offsets: list[int] = []
        with open(path, "rb") as f:
            while True:
                off = n_bytes
                line = f.readline()
                if not line:
                    break
                h.update(line)
                n_bytes += len(line)
                if line.strip():
                    offsets.append(off)
        if n_bytes != pin.bytes or h.hexdigest() != pin.sha256:
            raise pinmod.PinError(f"LiveCodeBench shard {shard} does not match its pin (bytes or SHA-256): {path}")
        self._line_offsets[shard] = offsets
        self._verified[shard] = path
        return path

    def read_one(self, question_id: str, tests: bool = True) -> LcbRecord:
        e = self._entries[question_id]
        shard = e["shard"]
        path = self.verify_shard(shard)
        with open(path, "rb") as f:
            f.seek(self._line_offsets[shard][e["line"]])
            line = f.readline()
        rec = parse_record(line, shard, self._shard_pin[shard].sha256, tests=tests)
        if rec.question_id != question_id:
            raise pinmod.PinError(f"{shard} line {e['line']} holds {rec.question_id}, ID list says {question_id}")
        return rec

    def check_available(self, question_ids: Sequence[str]) -> None:
        shards = sorted({self._entries[q]["shard"] for q in question_ids})
        miss = self.missing_shards(shards)
        if miss:
            raise pinmod.PinError(f"LiveCodeBench shards missing from {self.cache_dir}: {miss}. Run: {self.fetch_command()}")

    def problems(self, question_ids: Sequence[str] | None = None) -> list[Problem]:
        ids = list(question_ids) if question_ids is not None else [r["question_id"] for r in self.ids]
        self.check_available(ids)
        return [record_problem(self.read_one(q, tests=False)) for q in ids]

    def suites_for(self, question_id: str) -> dict[str, TestSuite]:
        s = record_suites(self.read_one(question_id, tests=True))
        if len(s["agree"].inputs) == 0 and question_id not in self.zero_agreement:
            self.zero_agreement.append(question_id)
        return s
