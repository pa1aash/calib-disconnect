"""Sandbox-side harness. It runs INSIDE the sandbox (container, bubblewrap, or the trusted-only
subprocess) as ``python harness.py --job <job.pkl> --result <path or ->`` and is also imported by the
host for its pure helpers (``canonical_repr``, ``evalplus_match``, ``time_limits_for``). Importing this
module has no side effects. It depends only on the standard library and numpy, and on nothing in the
pipeline package, so the sandbox needs no copy of the repository.

Modes (``job["mode"]``)
    "reference"  trusted canonical solution: outputs (pickled), canonical reprs, runtimes
    "evalplus"   compare candidate outputs with expected outputs (EvalPlus semantics)
    "agree"      record each output's canonical repr (no comparison); exceptions become "!<TypeName>"
    "lcb"        LiveCodeBench official evaluator (vendor/lcb/testing_util.py, run_test)
    "lcb_agree"  LiveCodeBench output capture (lcb_capture.py, built from the vendored helpers)
    "probe"      isolation probes used by SandboxExecutor.preflight

The result is JSON written to ``--result``: a file path inside the work dir, or ``-`` for the original
standard output (used by the isolated backends, whose work dir is a tmpfs that vanishes with the sandbox).

EvalPlus logic copied from evalplus 0.3.1 (MIT licence, (c) OpenAI and the EvalPlus authors):
    evalplus/eval/__init__.py   unsafe_execute (comparison block), is_floats, untrusted_check (time limits)
    evalplus/eval/_special_oracle.py   MBPP_OUTPUT_NOT_NONE_TASKS, MBPP_OUTPUT_SET_EQ_TASKS, _surface_Area,
                                       _digit_distance_nums, _poly
    evalplus/eval/utils.py      time_limit, swallow_io, reliability_guard
    evalplus/gen/util/__init__.py   trusted_exec (reference outputs)
    evalplus/config.py          DEFAULT_MIN_TIME_LIMIT = 1.0, DEFAULT_GT_TIME_LIMIT_FACTOR = 4.0
tests/execute/test_execute_semantics.py checks these copies against the installed evalplus. The one
intentional change is HumanEval/32 (find_zero): upstream's ``continue`` in that branch skips the
``details[i] = True`` bookkeeping, which makes a correct solution fail the suite; here a passing
find_zero test is recorded as a pass.
"""

from __future__ import annotations

import builtins
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import pickle
import re
import signal
import sys
import time
import traceback

HARNESS_VERSION = "1"
EVALPLUS_VERSION = "0.3.1"
DEFAULT_MIN_TIME_LIMIT = 1.0
DEFAULT_GT_TIME_LIMIT_FACTOR = 4.0
SIGNATURE_FLOAT_SIG = 9
MAX_REPR_CHARS = 20_000

# evalplus/eval/_special_oracle.py (0.3.1)
MBPP_OUTPUT_NOT_NONE_TASKS = ["check_str", "text_match_three", "text_starta_endb"]
MBPP_OUTPUT_SET_EQ_TASKS = [
    "similar_elements",  # Mbpp/2
    "find_char_long",  # Mbpp/7
    "common_in_nested_lists",  # Mbpp/111
    "extract_singly",  # Mbpp/140
    "larg_nnum",  # Mbpp/232
    "intersection_array",  # Mbpp/249
    "find_dissimilar",  # Mbpp/579
    "Diff",  # Mbpp/769
]


def _surface_Area(base_edge, height):
    slant_height = math.sqrt((base_edge / 2) ** 2 + height**2)
    base_area = base_edge**2
    lateral_area = 4 * (base_edge * slant_height) / 2
    total_surface_area = base_area + lateral_area
    return round(total_surface_area)


def _digit_distance_nums(num1, num2):
    str_num1, str_num2 = str(num1), str(num2)
    max_length = max(len(str_num1), len(str_num2))
    str_num1, str_num2 = str_num1.zfill(max_length), str_num2.zfill(max_length)
    total_difference = 0
    for digit1, digit2 in zip(str_num1, str_num2):
        difference = abs(int(digit1) - int(digit2))
        total_difference += difference
    return total_difference


def _poly(xs: list, x: float):
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def is_floats(x) -> bool:
    """evalplus.eval.is_floats: float, non-empty list or tuple of floats, or a float ndarray."""
    if isinstance(x, float):
        return True
    if isinstance(x, (list, tuple)) and x:
        return all(isinstance(i, float) for i in x)
    np = sys.modules.get("numpy")
    if np is not None and isinstance(x, np.ndarray):
        return x.dtype == np.float64 or x.dtype == np.float32
    return False


def time_limits_for(ref_times, min_time_limit: float = DEFAULT_MIN_TIME_LIMIT,
                    factor: float = DEFAULT_GT_TIME_LIMIT_FACTOR) -> list[float]:
    """untrusted_check: ``max(min_time_limit, gt_time_limit_factor * ref_time)`` per test."""
    return [max(min_time_limit, factor * t) for t in ref_times]


def evalplus_match(dataset: str, entry_point: str, inp, out, exp, atol: float):
    """The comparison block of evalplus ``unsafe_execute``. Returns (ok, atol_after). ``atol_after``
    carries EvalPlus's in-loop promotion of a zero tolerance to 1e-6 once a float expected output is
    seen: the caller passes it back for the next test, as upstream does. Raises nothing for a plain
    mismatch (ok False); exceptions raised by the comparison itself propagate to the caller, who counts
    them as a failed test, as upstream does."""
    exact_match = out == exp

    # ============== special oracles ================= #
    if dataset == "mbpp":
        if "are_equivalent" == entry_point:  # Mbpp/164 special oracle
            exact_match = exact_match or True
        elif "sum_div" == entry_point:  # Mbpp/295 special oracle
            exact_match = exact_match or out == 0
        elif "surface_Area" == entry_point:  # Mbpp/581 special oracle
            exact_match = exact_match or abs(out - _surface_Area(*inp)) <= atol
        elif "digit_distance_nums" == entry_point:  # Mbpp/558 special oracle
            exact_match = exact_match or out == _digit_distance_nums(*inp)
        elif entry_point in MBPP_OUTPUT_SET_EQ_TASKS:
            exact_match = set(out) == set(exp)
        elif entry_point in MBPP_OUTPUT_NOT_NONE_TASKS:
            # exp is True if not None, False if None
            if isinstance(out, bool):
                exact_match = out == exp
            else:
                exact_match = exp == (out is not None)

    if dataset == "humaneval":
        if "find_zero" == entry_point:  # HumanEval/32 special oracle
            return abs(_poly(*inp, out)) <= atol, atol
    # ============== special oracles ================= #

    if atol == 0 and is_floats(exp):
        atol = 1e-6  # enforce atol for float comparison
    if not exact_match and atol != 0:
        import numpy as np

        # explicitly set rtol=1e-07 to match `np.testing.assert_allclose`'s default values
        if type(out) != type(exp):
            return False, atol
        if isinstance(exp, (list, tuple)) and len(out) != len(exp):
            return False, atol
        return bool(np.allclose(out, exp, rtol=1e-07, atol=atol)), atol
    return bool(exact_match), atol


# ----------------------------------------------------------------------------------------------------
# Canonical representation (behavior signatures, design section 7.7)
# ----------------------------------------------------------------------------------------------------
_ADDR_RE = re.compile(r"0x[0-9a-fA-F]+")


def _fmt_float(x: float, sig: int) -> str:
    if x != x:
        return "nan"
    if x in (math.inf, -math.inf):
        return "inf" if x > 0 else "-inf"
    if x == 0:
        return "0.0"
    return repr(float(f"{x:.{sig}g}"))


def _canon(v, sig: int, depth: int) -> str:
    if depth > 60:
        return "<deep>"
    if v is None or v is True or v is False:
        return repr(v)
    t = type(v)
    if t is int:
        return repr(v)
    if isinstance(v, float):
        return _fmt_float(float(v), sig)
    if isinstance(v, complex):
        return f"complex({_fmt_float(v.real, sig)},{_fmt_float(v.imag, sig)})"
    if isinstance(v, (str, bytes)):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(_canon(x, sig, depth + 1) for x in v) + "]"
    if isinstance(v, tuple):
        inner = ", ".join(_canon(x, sig, depth + 1) for x in v)
        return "(" + inner + ("," if len(v) == 1 else "") + ")"
    if isinstance(v, (set, frozenset)):
        name = "set" if isinstance(v, set) else "frozenset"
        return name + "{" + ", ".join(sorted(_canon(x, sig, depth + 1) for x in v)) + "}"
    if isinstance(v, dict):
        items = sorted(f"{_canon(k, sig, depth + 1)}: {_canon(x, sig, depth + 1)}" for k, x in v.items())
        return "{" + ", ".join(items) + "}"
    if hasattr(v, "tolist"):  # numpy arrays and scalars
        try:
            return _canon(v.tolist(), sig, depth + 1)
        except Exception:
            pass
    if isinstance(v, int):  # int subclasses such as enums or numpy ints without tolist
        return repr(int(v))
    try:
        return _ADDR_RE.sub("0x?", repr(v))
    except Exception:
        return f"<unrepr:{type(v).__name__}>"


def canonical_repr(value, sig: int = SIGNATURE_FLOAT_SIG) -> str:
    """Canonical ``repr`` used for behavior signatures: floats are normalized to ``sig`` significant
    digits (nan and inf spelled out, signed zero merged), sets and dict items are sorted, memory
    addresses are masked, and a value whose repr exceeds MAX_REPR_CHARS is replaced by its SHA-256.
    Lists and tuples stay distinct, as do 1, 1.0, and True."""
    try:
        s = _canon(value, sig, 0)
    except Exception as e:  # e.g. int too large to render
        s = f"<unrepr:{type(e).__name__}>"
    if len(s) > MAX_REPR_CHARS:
        s = "long:" + hashlib.sha256(s.encode("utf-8", "replace")).hexdigest() + f":{len(s)}"
    return s


def exception_token(exc: BaseException) -> str:
    """Signature element for a raised exception: '!' plus the type name (no valid repr starts with '!')."""
    if type(exc).__name__ == "TimeoutException":  # this module's class or the LiveCodeBench evaluator's
        return "!Timeout"
    return "!" + type(exc).__name__


def normalize_stdout_text(text: str, sig: int = SIGNATURE_FLOAT_SIG) -> str:
    """Canonical form of a stdout capture: lines stripped as LiveCodeBench does, and every token that
    is a decimal float literal normalized to ``sig`` significant digits."""
    lines = []
    for line in text.strip().split("\n"):
        toks = []
        for tok in line.strip().split():
            if re.fullmatch(r"[-+]?(\d+\.\d*|\.\d+|\d+[eE][-+]?\d+|\d+\.\d*[eE][-+]?\d+)", tok):
                try:
                    tok = _fmt_float(float(tok), sig)
                except ValueError:
                    pass
            toks.append(tok)
        lines.append(" ".join(toks))
    return "\n".join(lines)


# ----------------------------------------------------------------------------------------------------
# Execution helpers (evalplus/eval/utils.py)
# ----------------------------------------------------------------------------------------------------
class TimeoutException(Exception):
    pass


@contextlib.contextmanager
def time_limit(seconds: float):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.setitimer(signal.ITIMER_REAL, seconds)
    signal.signal(signal.SIGALRM, signal_handler)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


class _Sink(io.StringIO):
    """Write-only sink that keeps nothing (upstream's WriteOnlyStringIO accumulates the text)."""

    def write(self, s):
        return len(s)

    def read(self, *args, **kwargs):
        raise IOError

    def readline(self, *args, **kwargs):
        raise IOError

    def readlines(self, *args, **kwargs):
        raise IOError

    def readable(self, *args, **kwargs):
        return False


class _redirect_stdin(contextlib._RedirectStream):  # type: ignore
    _stream = "stdin"


@contextlib.contextmanager
def swallow_io():
    stream = _Sink()
    with contextlib.redirect_stdout(stream):
        with contextlib.redirect_stderr(stream):
            with _redirect_stdin(stream):
                yield


def reliability_guard():
    """evalplus.eval.utils.reliability_guard (without the memory argument; limits are applied by
    ``apply_rlimits``). Not a security boundary: the sandbox is. It is kept so that the pass criterion
    matches the pinned evaluator (for example, ``open`` is unavailable to candidate code)."""
    import faulthandler

    faulthandler.disable()
    builtins.exit = None
    builtins.quit = None
    os.environ["OMP_NUM_THREADS"] = "1"
    os.kill = None
    os.system = None
    os.putenv = None
    os.remove = None
    os.removedirs = None
    os.rmdir = None
    os.fchdir = None
    os.setuid = None
    os.fork = None
    os.forkpty = None
    os.killpg = None
    os.rename = None
    os.renames = None
    os.truncate = None
    os.replace = None
    os.unlink = None
    os.fchmod = None
    os.fchown = None
    os.chmod = None
    os.chown = None
    os.chroot = None
    os.fchdir = None
    os.lchflags = None
    os.lchmod = None
    os.lchown = None
    os.getcwd = None
    os.chdir = None
    builtins.open = None

    import shutil

    shutil.rmtree = None
    shutil.move = None
    shutil.chown = None

    import subprocess

    subprocess.Popen = None  # type: ignore

    builtins.help = None  # upstream: __builtins__["help"] = None (a dict only inside a module)

    sys.modules["ipdb"] = None
    sys.modules["joblib"] = None
    sys.modules["resource"] = None
    sys.modules["psutil"] = None
    sys.modules["tkinter"] = None


def apply_rlimits(job: dict) -> list[str]:
    """Set the per-process limits inside the sandbox. Returns notes for limits the platform refused
    (macOS ignores or rejects some); the parent's watchdog covers memory and wall time there."""
    import resource

    notes: list[str] = []

    def setl(name: str, soft: int, hard: int | None = None):
        r = getattr(resource, name, None)
        if r is None:
            return
        try:
            resource.setrlimit(r, (soft, soft if hard is None else hard))
        except (ValueError, OSError) as e:
            notes.append(f"{name}: {type(e).__name__}")

    mem = int(job["memory_bytes"])
    setl("RLIMIT_AS", mem)
    setl("RLIMIT_DATA", mem)
    if sys.platform != "darwin":
        setl("RLIMIT_STACK", mem)
    setl("RLIMIT_CPU", int(job.get("cpu_seconds", 90)))
    setl("RLIMIT_FSIZE", int(job.get("fsize_bytes", 16 * 1024 * 1024)))
    setl("RLIMIT_CORE", 0)
    setl("RLIMIT_NOFILE", int(job.get("nofile", 256)))
    setl("RLIMIT_NPROC", int(job.get("nproc", 64)))
    return notes


def _status_of(exc: BaseException) -> str:
    if isinstance(exc, TimeoutException):
        return "timeout"
    if isinstance(exc, MemoryError):
        return "memory"
    return "exception"


def _load(code: str, entry_point: str):
    exec_globals: dict = {}
    with swallow_io():
        # dont_inherit: this module uses ``from __future__ import annotations``, which exec would
        # otherwise pass on to the candidate and silently defer its annotations (hiding NameErrors that
        # EvalPlus, which has no such import, reports).
        exec(compile(code, "<candidate>", "exec", flags=0, dont_inherit=True), exec_globals)
        return exec_globals[entry_point]


# ----------------------------------------------------------------------------------------------------
# Modes
# ----------------------------------------------------------------------------------------------------
def run_reference(job: dict) -> dict:
    """Trusted canonical solution on every input (evalplus ``trusted_exec`` with record_time)."""
    entry = job["entry_point"]
    not_none = job["dataset"] == "mbpp" and entry in MBPP_OUTPUT_NOT_NONE_TASKS
    res: dict = {"ok": True, "failure": None, "error": None, "runtimes": [], "outputs_canon": [],
                 "outputs_pickle_b64": None}
    try:
        fn = _load(job["code"], entry)
    except BaseException as e:
        return {**res, "ok": False, "failure": _status_of(e), "error": exception_token(e)}
    outputs = []
    cap = float(job.get("reference_test_timeout_s", 10.0))
    for inp in job["inputs"]:
        arg = copy.deepcopy(inp)
        t0 = time.perf_counter()
        try:
            with time_limit(cap):
                with swallow_io():
                    out = fn(*arg)
            dt = time.perf_counter() - t0
        except BaseException as e:
            return {**res, "ok": False, "failure": _status_of(e), "error": exception_token(e)}
        if not_none:
            out = out is not None
        outputs.append(out)
        res["runtimes"].append(dt)
        res["outputs_canon"].append(canonical_repr(out))
    try:
        import base64

        res["outputs_pickle_b64"] = base64.b64encode(pickle.dumps(outputs, protocol=4)).decode("ascii")
    except Exception as e:
        return {**res, "ok": False, "failure": "exception", "error": f"unpicklable:{type(e).__name__}"}
    return res


def run_evalplus(job: dict) -> dict:
    """Candidate vs expected outputs. Stops at the first failing test when ``stop_on_fail``."""
    reliability_guard()
    entry, dataset = job["entry_point"], job["dataset"]
    inputs, expected, limits = job["inputs"], job["expected"], job["time_limits"]
    atol = float(job["atol"])
    res: dict = {"load_error": None, "load_status": None, "tests": []}
    try:
        fn = _load(job["code"], entry)
    except BaseException as e:
        res["load_error"], res["load_status"] = exception_token(e), _status_of(e)
        return res
    for i, inp in enumerate(inputs):
        rec = {"s": "pass", "t": 0.0, "e": None}
        arg = copy.deepcopy(inp)
        t0 = time.perf_counter()
        try:
            with time_limit(limits[i]):
                with swallow_io():
                    out = fn(*arg)
            rec["t"] = time.perf_counter() - t0
        except BaseException as e:
            rec["t"] = time.perf_counter() - t0
            rec["s"], rec["e"] = _status_of(e), exception_token(e)
        else:
            try:
                ok, atol = evalplus_match(dataset, entry, inp, out, expected[i], atol)
            except BaseException:
                ok = False
            if not ok:
                rec["s"] = "wrong_output"
        res["tests"].append(rec)
        if rec["s"] != "pass" and job.get("stop_on_fail", True):
            break
    return res


def run_agree(job: dict) -> dict:
    """Behavior signature: canonical repr of each output, or '!<ExceptionType>'."""
    reliability_guard()
    entry, limits = job["entry_point"], job["time_limits"]
    res: dict = {"load_error": None, "load_status": None, "tests": [], "outputs": []}
    try:
        fn = _load(job["code"], entry)
    except BaseException as e:
        tok = exception_token(e)
        res["load_error"], res["load_status"] = tok, _status_of(e)
        res["outputs"] = [tok] * len(job["inputs"])
        return res
    for i, inp in enumerate(job["inputs"]):
        arg = copy.deepcopy(inp)
        t0 = time.perf_counter()
        try:
            with time_limit(limits[i]):
                with swallow_io():
                    out = fn(*arg)
            tok, status, e_name = canonical_repr(out), "pass", None
        except BaseException as e:
            tok, status, e_name = exception_token(e), _status_of(e), exception_token(e)
        res["tests"].append({"s": status, "t": time.perf_counter() - t0, "e": e_name})
        res["outputs"].append(tok)
    return res


def _import_bundle(bundle_dir: str):
    if bundle_dir and bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)


def _lcb_status(code) -> str:
    return {-1: "timeout", -2: "wrong_output", -3: "timeout", -4: "exception", -5: "sandbox_error"}.get(
        code, "exception")


def run_lcb(job: dict) -> dict:
    """LiveCodeBench official evaluator, unmodified (vendor/lcb/testing_util.py ``run_test``)."""
    _import_bundle(job["bundle_dir"])
    import testing_util  # the vendored file, copied verbatim into the bundle

    in_out = {"inputs": list(job["inputs"]), "outputs": list(job["expected"]), "fn_name": job.get("fn_name")}
    sample = {"input_output": json.dumps(in_out)}
    results, metadata = testing_util.run_test(sample, test=job["code"], debug=False,
                                              timeout=int(job["lcb_timeout_s"]))
    tests = []
    for r in results:
        try:
            if isinstance(r, bool) or r is True:
                ok = bool(r)
            else:
                ok = bool(r > 0)
        except Exception:
            ok = False
        tests.append({"s": "pass" if ok else None, "t": 0.0, "e": None, "raw": r if isinstance(r, (bool, int)) else None})
    code = metadata.get("error_code") if isinstance(metadata, dict) else None
    for t in tests:
        if t["s"] is None:
            t["s"] = _lcb_status(code if code is not None else t["raw"])
    return {"load_error": None, "load_status": None, "tests": tests,
            "metadata": {k: v for k, v in (metadata or {}).items() if isinstance(v, (str, int, float))}}


def run_lcb_agree(job: dict) -> dict:
    _import_bundle(job["bundle_dir"])
    import lcb_capture

    return lcb_capture.capture(job, sys.modules[__name__])


def fork_probe(limit: int) -> dict:
    """Try to start twice ``limit`` sleeping child processes. With RLIMIT_NPROC enforced the fork fails
    before that. The children are killed and reaped before returning."""
    pids: list[int] = []
    err = None
    try:
        for _ in range(2 * limit):
            pid = os.fork()
            if pid == 0:
                time.sleep(20)
                os._exit(0)
            pids.append(pid)
    except OSError as e:
        err = type(e).__name__
    n = len(pids)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
        except OSError:
            pass
    return {"probe": "fork", "forked": n, "limit": limit, "error": err,
            "result": "LIMITED" if n < 2 * limit else "UNLIMITED"}


def fork_limit_enforced(result: dict | None, limit: int) -> bool:
    """Preflight judgement of a fork probe result: the fork failed and no more than ``limit`` children
    started."""
    return bool(result) and result.get("probe") == "fork" and result.get("result") == "LIMITED" \
        and int(result.get("forked", 10**9)) <= limit


def run_probe(job: dict) -> dict:
    kind = job["probe"]
    if kind == "ok":
        return {"probe": "ok", "result": "OK"}
    if kind == "net":
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        try:
            s.connect(("127.0.0.1", int(job["port"])))
            return {"probe": "net", "result": "CONNECTED"}
        except OSError as e:
            return {"probe": "net", "result": "BLOCKED", "detail": type(e).__name__}
        finally:
            s.close()
    if kind == "write":
        out = {}
        for path in job["paths"]:
            try:
                with open(path, "w") as f:
                    f.write("x")
                out[path] = "WROTE"
            except OSError as e:
                out[path] = "DENIED:" + type(e).__name__
        return {"probe": "write", "results": out}
    if kind == "fork":
        return fork_probe(int(job["limit"]))
    if kind == "mem":
        chunks = []
        limit = int(job["memory_bytes"])
        try:
            total = 0
            while total < 3 * limit:
                chunks.append(b"x" * (64 * 1024 * 1024))
                total += 64 * 1024 * 1024
            return {"probe": "mem", "result": "UNLIMITED", "allocated": total}
        except MemoryError:
            return {"probe": "mem", "result": "LIMITED", "allocated": len(chunks) * 64 * 1024 * 1024}
    raise ValueError(f"unknown probe {kind!r}")


MODES = {"reference": run_reference, "evalplus": run_evalplus, "agree": run_agree, "lcb": run_lcb,
         "lcb_agree": run_lcb_agree, "probe": run_probe}


def main(argv: list[str]) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--result", required=True)
    args = ap.parse_args(argv)

    # Keep the real result channel on a private descriptor, then point fds 1 and 2 at /dev/null so that
    # nothing the candidate prints can reach the host or corrupt the result.
    if args.result == "-":
        out_fd = os.dup(1)
    else:
        out_fd = os.open(args.result, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    sys.set_int_max_str_digits(50_000)

    def emit(obj: dict) -> None:
        data = json.dumps(obj, separators=(",", ":")).encode("utf-8")
        view = memoryview(data)
        while view:
            n = os.write(out_fd, view)
            view = view[n:]

    try:
        import numpy  # noqa: F401  (imported before limits so that its allocations are not limited)

        with open(args.job, "rb") as f:
            job = pickle.load(f)
        if job.get("expected_pickle_b64") is not None:  # reference outputs are unpickled only in here
            import base64

            job["expected"] = pickle.loads(base64.b64decode(job["expected_pickle_b64"]))
        notes = apply_rlimits(job) if job.get("apply_rlimits", True) else []
        result = MODES[job["mode"]](job)
        result["harness"] = {"version": HARNESS_VERSION, "rlimit_notes": notes}
        emit(result)
        signal.setitimer(signal.ITIMER_REAL, 0)
    except BaseException as e:  # harness failure, never a candidate outcome
        signal.setitimer(signal.ITIMER_REAL, 0)
        try:
            emit({"harness_error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-2000:]})
        except BaseException:
            pass
        os._exit(3)
    os._exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
