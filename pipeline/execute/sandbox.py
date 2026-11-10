"""Sandboxed execution (design section 6; method rows 5.1 to 5.3, 5.6, 5.10).

One ``SandboxExecutor`` class implements the ``Executor`` protocol behind three selectable backends:

    "container"    docker or podman, ``--network none``, ``--read-only``, tmpfs work dir, 2 GB, pids and
                   cpu limits, non-root user, a fresh container per run, image pinned by digest.
    "bwrap"        bubblewrap: ``--unshare-all`` (network included), ``--die-with-parent``,
                   ``--new-session``, read-only binds of the interpreter tree, tmpfs work dir, plus
                   prlimit and setrlimit limits. The expected backend on a RunPod pod, which is itself a
                   container where nested docker is usually unavailable.
    "trusted-only" a plain subprocess with setrlimit limits and a memory watchdog. It provides no
                   isolation and refuses every call unless ``trusted=True`` (the Mac backend).

Rules enforced here: the interpreter is pinned by absolute path and its SHA-256 goes into the cache key;
an executor built with ``execute_untrusted=False`` raises on ``trusted=False``; an isolated backend
proves isolation in ``preflight()`` before its first untrusted run; nothing ever falls back from an
isolated backend to a plain subprocess.

Each run writes a pickled job (code, inputs, limits) to a fresh directory, starts ``harness.py`` in the
sandbox, and reads the JSON result back. Candidate code never runs in this process.
"""

from __future__ import annotations

import collections
import hashlib
import json
import os
import pickle
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import uuid
import weakref
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from pipeline.contracts import constants, hashing
from pipeline.contracts.schemas import ExecutionResult, Problem, TestSuite

from . import harness as H
from .extract import normalize_code
from .reference import FUNCTION_BENCHMARKS, RefEntry, ReferenceStore, inputs_fingerprint, reference_program

BACKENDS = ("container", "bwrap", "trusted-only")
LCB_COMMIT = "28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24"  # vendor/lcb/PROVENANCE.md
SANDBOX_LABEL = {"container": "container", "bwrap": "bwrap", "trusted-only": "rlimit-subprocess"}
_HERE = Path(__file__).resolve().parent
_BUNDLE_FILES = {
    "harness.py": _HERE / "harness.py",
    "lcb_capture.py": _HERE / "lcb_capture.py",
    "testing_util.py": _HERE / "vendor" / "lcb" / "testing_util.py",
}


class SandboxError(RuntimeError):
    pass


class UntrustedExecutionRefused(SandboxError):
    """trusted=False on an executor that must not run untrusted code."""


class IsolationError(SandboxError):
    """Isolation could not be proven (preflight) or the backend is not available."""


class ReferenceUnavailable(SandboxError):
    """The reference outputs of a (problem, suite) are missing or the reference was excluded."""


_LIBPROC = None


def _darwin_footprint(pid: int) -> int:
    """ri_phys_footprint from proc_pid_rusage(RUSAGE_INFO_V2); 0 when unavailable."""
    global _LIBPROC
    import ctypes
    import struct

    try:
        if _LIBPROC is None:
            _LIBPROC = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
        buf = ctypes.create_string_buffer(512)
        if _LIBPROC.proc_pid_rusage(int(pid), 2, buf) != 0:
            return 0
        return struct.unpack_from("<Q", buf, 72)[0]
    except (OSError, AttributeError):
        return 0


# ----------------------------------------------------------------------------------------------------
# Command builders (pure functions; unit-tested as argument lists)
# ----------------------------------------------------------------------------------------------------
def sandbox_env(work: str = "/work") -> dict[str, str]:
    """The only environment the harness sees. PYTHONHASHSEED is fixed so that set and dict-of-str
    iteration order, and so output reprs, are reproducible between runs."""
    return {
        "PATH": "/usr/bin:/bin",
        "HOME": work,
        "TMPDIR": work,
        "PYTHONHASHSEED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
    }


def harness_argv(interpreter: str, harness_path: str, job_path: str, result: str) -> list[str]:
    return [interpreter, "-s", "-B", harness_path, "--job", job_path, "--result", result]


def build_trusted_argv(interpreter: str, bundle_dir: str, job_path: str, result_path: str) -> list[str]:
    return harness_argv(interpreter, os.path.join(bundle_dir, "harness.py"), job_path, result_path)


def build_bwrap_argv(*, bwrap: str, interpreter: str, job_dir: str, bundle_dir: str,
                     ro_binds: Sequence[str], symlinks: Mapping[str, str] | None = None,
                     prlimit: str | None = None, cpu_seconds: int = 90, fsize_bytes: int = 16 * 1024 * 1024,
                     nofile: int = 256, env: Mapping[str, str] | None = None,
                     uid: int = 65534, gid: int = 65534) -> list[str]:
    """bubblewrap command line. Inside: /job (the job directory) and /harness (the harness bundle) are
    read-only, every path in ro_binds (interpreter tree, /usr, libraries) is bound read-only at the
    same path, /work is a tmpfs and the working directory, nothing else is writable. ``--unshare-all``
    unshares user, ipc, pid, uts, cgroup, and net, so there is no network."""
    # --unshare-user with a non-zero uid makes RLIMIT_NPROC enforceable even when the pod runs as root
    # (the kernel does not apply it to uid 0).
    argv = [bwrap, "--unshare-all", "--unshare-user", "--uid", str(uid), "--gid", str(gid), "--die-with-parent",
            "--new-session", "--clearenv"]
    for src in ro_binds:
        argv += ["--ro-bind", src, src]
    for link, target in (symlinks or {}).items():
        argv += ["--symlink", target, link]
    argv += ["--proc", "/proc", "--dev", "/dev", "--tmpfs", "/work",
             "--ro-bind", job_dir, "/job", "--ro-bind", bundle_dir, "/harness", "--chdir", "/work"]
    for k, v in (env if env is not None else sandbox_env("/work")).items():
        argv += ["--setenv", k, v]
    if prlimit:
        argv += [prlimit, f"--cpu={cpu_seconds}", f"--fsize={fsize_bytes}", "--core=0", f"--nofile={nofile}", "--"]
    argv += harness_argv(interpreter, "/harness/harness.py", "/job/job.pkl", "-")
    return argv


def image_digest(image: str) -> str:
    """The sha256 hex of a digest-pinned image reference (name@sha256:<64 hex>)."""
    if "@sha256:" not in image:
        raise ValueError(f"container image must be pinned by digest (name@sha256:...), got {image!r}")
    d = image.split("@sha256:", 1)[1]
    if len(d) != 64 or any(c not in "0123456789abcdef" for c in d):
        raise ValueError("malformed image digest")
    return d


def build_container_argv(*, runtime: str, image: str, name: str, job_dir: str, bundle_dir: str,
                         image_python: str = "/usr/local/bin/python", memory_bytes: int = constants.SANDBOX_MEMORY_BYTES,
                         pids_limit: int = 64, cpus: float = 1.0, user: str = "65534:65534",
                         work_tmpfs_bytes: int = 64 * 1024 * 1024, cpu_seconds: int = 90,
                         env: Mapping[str, str] | None = None) -> list[str]:
    """docker or podman command line: no network, read-only root, tmpfs /work, memory (swap equal, so no
    swap), pids and cpu limits, a non-root user, all capabilities dropped, no-new-privileges, a fresh
    named container removed on exit. The image must be pinned by digest."""
    image_digest(image)
    argv = [runtime, "run", "--rm", "--name", name, "--network", "none", "--read-only",
            "--tmpfs", f"/work:rw,nosuid,nodev,noexec,size={work_tmpfs_bytes}",
            "--memory", str(memory_bytes), "--memory-swap", str(memory_bytes),
            "--pids-limit", str(pids_limit), "--cpus", str(cpus), "--user", user,
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--ulimit", f"cpu={cpu_seconds}",
            "--ulimit", "core=0", "--workdir", "/work",
            "-v", f"{job_dir}:/job:ro", "-v", f"{bundle_dir}:/harness:ro"]
    for k, v in (env if env is not None else sandbox_env("/work")).items():
        argv += ["-e", f"{k}={v}"]
    argv += [image] + harness_argv(image_python, "/harness/harness.py", "/job/job.pkl", "-")
    return argv


def default_ro_binds(interpreter: str) -> tuple[tuple[str, ...], dict[str, str]]:
    """Read-only binds for bwrap: system library roots present on this host, plus the interpreter's
    prefix, base prefix, and the directory of the (unresolved) interpreter path. Symlinked roots such as
    /lib -> usr/lib become ``--symlink`` entries. Runs the pinned interpreter once (trusted code)."""
    out = subprocess.run([interpreter, "-c", "import sys,json;print(json.dumps([sys.prefix,sys.base_prefix]))"],
                         capture_output=True, text=True, check=True, timeout=30,
                         env={"PATH": "/usr/bin:/bin"})
    prefixes = json.loads(out.stdout)
    binds: list[str] = []
    links: dict[str, str] = {}
    for root in ("/usr", "/lib", "/lib64", "/bin", "/sbin", "/etc/ld.so.cache", "/etc/alternatives"):
        if os.path.islink(root):
            links[root] = os.readlink(root)
        elif os.path.exists(root):
            binds.append(root)
    for p in [*prefixes, str(Path(interpreter).parent.parent)]:
        rp = os.path.realpath(p)
        for q in (p, rp):
            if q not in binds and os.path.exists(q) and not any(q == b or q.startswith(b.rstrip("/") + "/") for b in binds):
                binds.append(q)
    return tuple(binds), links


CGROUP_ROOT = Path("/sys/fs/cgroup")


def cgroup_pids_available(root: Path = CGROUP_ROOT) -> bool:
    """cgroup v2 with the pids controller and a writable hierarchy."""
    try:
        return (root / "cgroup.controllers").exists() and "pids" in (root / "cgroup.controllers").read_text().split() \
            and os.access(root, os.W_OK)
    except OSError:
        return False


def cgroup_create(name: str, pids_max: int, root: Path = CGROUP_ROOT) -> Path | None:
    """Create ``root/name`` with pids.max; None when not possible."""
    d = root / name
    try:
        d.mkdir()
        (d / "pids.max").write_text(str(pids_max))
        return d
    except OSError:
        try:
            d.rmdir()
        except OSError:
            pass
        return None


def infrastructure_signal(returncode: int | None) -> bool:
    """A missing result with this return code is the infrastructure's doing, not the program's: SIGHUP,
    SIGINT, SIGPIPE, SIGTERM (and 143). Signals a program causes itself (SIGKILL by the memory limit,
    SIGSEGV, SIGABRT, SIGBUS, SIGFPE, SIGXCPU, SIGXFSZ) stay "killed"."""
    return returncode in (-1, -2, -13, -15, 143)


# ----------------------------------------------------------------------------------------------------
# Configuration and results
# ----------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class SandboxConfig:
    backend: str = "trusted-only"
    interpreter: str | None = None            # absolute path; default sys.executable (never PATH)
    execute_untrusted: bool = False
    memory_bytes: int = constants.SANDBOX_MEMORY_BYTES
    program_cap_s: float = constants.PROGRAM_WALL_CAP_S
    min_time_limit: float = H.DEFAULT_MIN_TIME_LIMIT
    gt_time_limit_factor: float = H.DEFAULT_GT_TIME_LIMIT_FACTOR
    lcb_timeout_s: int = 6                    # LiveCodeBench's own per-test timeout (run_test default)
    reference_test_timeout_s: float = 10.0
    startup_slack_s: float = 5.0              # interpreter and numpy start-up allowance in the wall cap
    pids_limit: int = 64
    cpus: float = 1.0
    container_runtime: str | None = None      # "docker" or "podman" (resolved on PATH) or an absolute path
    container_image: str | None = None       # name@sha256:<digest>
    container_python: str = "/usr/local/bin/python"
    bwrap_path: str | None = None
    prlimit_path: str | None = None
    ro_binds: tuple[str, ...] | None = None   # None: computed from the interpreter
    symlinks: tuple[tuple[str, str], ...] | None = None


@dataclass
class RawRun:
    result: dict | None
    returncode: int | None
    wall_s: float
    reason: str | None = None                 # "program_cap" | "memory" when the watchdog killed it
    stderr_tail: str = ""


# ----------------------------------------------------------------------------------------------------
# Executor
# ----------------------------------------------------------------------------------------------------
class SandboxExecutor:
    """Implements pipeline.contracts.interfaces.Executor."""

    def __init__(self, config: SandboxConfig | None = None, *, references: ReferenceStore | None = None, **kw: Any):
        cfg = config if config is not None else SandboxConfig(**kw)
        if config is not None and kw:
            raise TypeError("pass either a config or keyword arguments")
        if cfg.backend not in BACKENDS:
            raise ValueError(f"unknown backend {cfg.backend!r}; choose from {BACKENDS}")
        interp = cfg.interpreter if cfg.interpreter is not None else sys.executable
        if not os.path.isabs(interp):
            raise ValueError("the interpreter must be pinned by absolute path, never taken from PATH")
        self.cfg = cfg
        self.interpreter = interp
        self.name = cfg.backend
        self.execute_untrusted = bool(cfg.execute_untrusted)
        self.references = references
        self._lock = threading.Lock()
        self._isolation_proven = False
        self.run_info: dict[str, dict[str, Any]] = {}  # cache key -> {"first_exception": token or None}
        self.diagnostics: collections.deque = collections.deque(maxlen=200)  # (key, failure, detail, returncode)
        self.preflight_report: dict[str, Any] | None = None
        if cfg.backend == "container":
            if not cfg.container_image:
                raise ValueError("container backend needs container_image pinned by digest")
            self._image_hex = image_digest(cfg.container_image)
            self.interpreter = cfg.container_python  # path inside the image
            self.interpreter_sha256 = self._image_hex  # the image digest identifies the interpreter
            self._runtime = self._which(cfg.container_runtime or "docker") or self._which("podman")
            if not self._runtime:
                raise IsolationError("container backend selected but neither docker nor podman was found")
        else:
            if not os.path.isfile(interp):
                raise ValueError(f"interpreter not found: {interp}")
            self.interpreter_sha256 = hashing.sha256_file(os.path.realpath(interp))
        if cfg.backend == "bwrap":
            self._bwrap = cfg.bwrap_path or self._which("bwrap")
            if not self._bwrap:
                raise IsolationError("bwrap backend selected but bubblewrap was not found")
            self._prlimit = cfg.prlimit_path or self._which("prlimit")
        self._tmp = tempfile.TemporaryDirectory(prefix="calib-harness-")
        self.bundle_dir = self._tmp.name
        weakref.finalize(self, self._tmp.cleanup)
        h = hashlib.sha256()
        for fname, src in sorted(_BUNDLE_FILES.items()):
            data = src.read_bytes()
            h.update(fname.encode() + b"\0" + data)
            dst = Path(self.bundle_dir) / fname
            dst.write_bytes(data)
            dst.chmod(0o444)
        Path(self.bundle_dir).chmod(0o555)
        self.bundle_sha256 = h.hexdigest()
        self._binds: tuple[tuple[str, ...], dict[str, str]] | None = None
        self._cgroup_ok: bool | None = None

    def cgroup_pids_ok(self) -> bool:
        if self._cgroup_ok is None:
            ok = cgroup_pids_available()
            if ok:
                probe = cgroup_create(f"calib-probe-{uuid.uuid4().hex[:8]}", self.cfg.pids_limit)
                ok = probe is not None
                if probe is not None:
                    try:
                        probe.rmdir()
                    except OSError:
                        pass
            self._cgroup_ok = ok
        return self._cgroup_ok

    # -- helpers
    @staticmethod
    def _which(x: str) -> str | None:
        return x if os.path.isabs(x) and os.path.exists(x) else shutil.which(x)

    @property
    def sandbox_label(self) -> str:
        return SANDBOX_LABEL[self.cfg.backend]

    def _evaluator_label(self, problem: Problem) -> str:
        if problem.benchmark == "lcb_v6":
            return f"lcb@{LCB_COMMIT[:10]}"
        return f"evalplus=={constants.EVALPLUS_TOOL_VERSION}"

    def _evaluator_version(self, problem: Problem) -> str:
        return f"{self._evaluator_label(problem)}+harness{H.HARNESS_VERSION}:{self.bundle_sha256[:12]}"

    def _is_function(self, problem: Problem) -> bool:
        return problem.benchmark in FUNCTION_BENCHMARKS

    def _ref(self, problem: Problem, suite: TestSuite) -> RefEntry | None:
        if self.references is None:
            return None
        return self.references.get(problem.problem_id, suite.suite_id, inputs_fingerprint(suite))

    def _ensure_ref(self, problem: Problem, suite: TestSuite, capture: bool) -> RefEntry | None:
        """Reference entry of a function-benchmark suite. Label runs need a good one (computed on demand,
        trusted); capture runs use it only for time limits when it already exists."""
        if not self._is_function(problem):
            return None
        if self.references is None:
            with self._lock:
                if self.references is None:
                    self.references = ReferenceStore(None, min_time_limit=self.cfg.min_time_limit,
                                                     gt_time_limit_factor=self.cfg.gt_time_limit_factor)
        ref = self._ref(problem, suite)
        if capture:
            return ref
        if ref is None:
            ref = self.references.compute(self, problem, suite)
        if not ref.ok:
            raise ReferenceUnavailable(f"{problem.problem_id}/{suite.suite_id}: reference excluded ({ref.failure})")
        return ref

    def _limits(self, problem: Problem, suite: TestSuite, ref: RefEntry | None) -> list[float]:
        if problem.benchmark == "lcb_v6":
            return [float(self.cfg.lcb_timeout_s)] * len(suite.inputs)
        if ref is not None and ref.ok and len(ref.time_limits_s) == len(suite.inputs):
            return list(ref.time_limits_s)
        return [self.cfg.min_time_limit] * len(suite.inputs)

    def _rule(self, problem: Problem, suite: TestSuite, ref: RefEntry | None) -> str:
        c = self.cfg
        if problem.benchmark == "lcb_v6":
            return (f"{suite.time_limit_rule}|lcb:per-test {c.lcb_timeout_s}s|program cap {c.program_cap_s}s")
        refpart = f"ref={ref.ref_hash[:16]}" if ref is not None and ref.ok else "ref=none"
        return (f"{suite.time_limit_rule}|evalplus:max({c.min_time_limit},{c.gt_time_limit_factor}*ref_time)|"
                f"{refpart}|stop_on_fail|program cap {c.program_cap_s}s")

    def cache_key(self, code: str, problem: Problem, suite: TestSuite, *, capture_outputs: bool = False) -> str:
        """hashing.exec_cache_key with the design's fields. The suite field also carries the input-set
        hash, and a capture run on a label suite is a different key from a pass/fail run."""
        capture = capture_outputs or suite.suite_id == "agree"
        ref = self._ensure_ref(problem, suite, capture)
        sid = f"{suite.suite_id}@{inputs_fingerprint(suite)[:16]}"
        if capture_outputs and suite.suite_id != "agree":
            sid += ":capture"
        return hashing.exec_cache_key(normalize_code(code), problem.problem_id, sid,
                                      self._evaluator_version(problem), self._rule(problem, suite, ref),
                                      self.cfg.memory_bytes, self.interpreter_sha256)

    # -- policy
    def _require_allowed(self, trusted: bool) -> None:
        if trusted:
            return
        if self.cfg.backend == "trusted-only":
            raise UntrustedExecutionRefused("the trusted-only backend never runs untrusted code")
        if not self.execute_untrusted:
            raise UntrustedExecutionRefused("this executor was built with execute_untrusted=False")
        if not self._isolation_proven:
            self.preflight()

    # -- running one job
    def _job_base(self) -> dict[str, Any]:
        c = self.cfg
        return {"memory_bytes": c.memory_bytes, "cpu_seconds": int(c.program_cap_s) + 30, "nproc": c.pids_limit,
                "fsize_bytes": 16 * 1024 * 1024, "nofile": 256, "lcb_timeout_s": c.lcb_timeout_s,
                "reference_test_timeout_s": c.reference_test_timeout_s}

    def _launch(self, job: dict[str, Any], cap_s: float) -> RawRun:
        c = self.cfg
        job_dir = tempfile.mkdtemp(prefix="calib-job-")
        work_dir = tempfile.mkdtemp(prefix="calib-work-") if c.backend == "trusted-only" else None
        cname = f"calib-{uuid.uuid4().hex[:16]}"
        try:
            sandbox_bundle = self.bundle_dir if c.backend == "trusted-only" else "/harness"
            job["bundle_dir"] = sandbox_bundle
            job_path = os.path.join(job_dir, "job.pkl")
            with open(job_path, "wb") as f:
                pickle.dump(job, f, protocol=4)
            Path(job_dir).chmod(0o755)
            os.chmod(job_path, 0o644)
            result_file = None
            if c.backend == "trusted-only":
                result_file = os.path.join(work_dir, "result.json")
                argv = build_trusted_argv(self.interpreter, self.bundle_dir, job_path, result_file)
                env = sandbox_env(work_dir)
                cwd = work_dir
            elif c.backend == "bwrap":
                if self._binds is None:
                    if c.ro_binds is not None:
                        self._binds = (tuple(c.ro_binds), dict(c.symlinks or ()))
                    else:
                        self._binds = default_ro_binds(self.interpreter)
                argv = build_bwrap_argv(bwrap=self._bwrap, interpreter=self.interpreter, job_dir=job_dir,
                                        bundle_dir=self.bundle_dir, ro_binds=self._binds[0], symlinks=self._binds[1],
                                        prlimit=self._prlimit, cpu_seconds=int(c.program_cap_s) + 30)
                env = {"PATH": "/usr/bin:/bin"}
                cwd = "/"
            else:
                argv = build_container_argv(runtime=self._runtime, image=c.container_image, name=cname,
                                            job_dir=job_dir, bundle_dir=self.bundle_dir,
                                            image_python=c.container_python, memory_bytes=c.memory_bytes,
                                            pids_limit=c.pids_limit, cpus=c.cpus,
                                            cpu_seconds=int(c.program_cap_s) + 30)
                env = {"PATH": "/usr/bin:/bin"}
                cwd = "/"
            cg = None
            if c.backend == "bwrap" and self.cgroup_pids_ok():
                cg = cgroup_create(cname, c.pids_limit)
            try:
                return self._run_process(argv, env, cwd, cap_s, result_file, cname, cg)
            finally:
                if cg is not None:
                    try:
                        cg.rmdir()
                    except OSError:
                        pass
        finally:
            shutil.rmtree(job_dir, ignore_errors=True)
            if work_dir:
                shutil.rmtree(work_dir, ignore_errors=True)

    def _run_process(self, argv: list[str], env: dict[str, str], cwd: str, cap_s: float,
                     result_file: str | None, cname: str, cgroup: Path | None = None) -> RawRun:
        import psutil

        c = self.cfg
        with tempfile.TemporaryFile() as errf:
            p = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=errf, start_new_session=True)
            if cgroup is not None:
                try:
                    (cgroup / "cgroup.procs").write_text(str(p.pid))
                except OSError:
                    pass
            t0 = time.monotonic()
            reason = None
            stdout = b""
            watch_memory = c.backend != "container"
            try:
                ps = psutil.Process(p.pid)
            except psutil.Error:
                ps = None
            while True:
                try:
                    stdout, _ = p.communicate(timeout=0.02)
                    break
                except subprocess.TimeoutExpired:
                    pass
                if time.monotonic() - t0 > cap_s:
                    reason = "program_cap"
                elif watch_memory and ps is not None and self._rss(ps) > c.memory_bytes:
                    reason = "memory"
                if reason:
                    self._kill(p, cname)
                    try:
                        stdout, _ = p.communicate(timeout=10)
                    except subprocess.TimeoutExpired:
                        p.kill()
                        stdout = b""
                    break
            wall = time.monotonic() - t0
            errf.seek(0)
            tail = errf.read()[-1500:].decode("utf-8", "replace")
        result = None
        if reason is None:
            try:
                raw = stdout if result_file is None else (Path(result_file).read_bytes() if os.path.exists(result_file) else b"")
                if raw:
                    result = json.loads(raw)
            except (ValueError, OSError):
                result = None
        return RawRun(result=result, returncode=p.returncode, wall_s=wall, reason=reason, stderr_tail=tail)

    @staticmethod
    def _rss(ps) -> int:
        """Memory in use by the process tree. On macOS the resident size undercounts (pages go to the
        compressor), so the physical footprint from libproc is used there; setrlimit(RLIMIT_AS) is
        rejected by macOS, and this watchdog is what enforces the limit on the Mac."""
        import psutil

        total = 0
        try:
            procs = [ps, *ps.children(recursive=True)]
        except psutil.Error:
            return 0
        for q in procs:
            try:
                used = q.memory_info().rss
                if sys.platform == "darwin":
                    used = max(used, _darwin_footprint(q.pid))
                total += used
            except psutil.Error:
                pass
        return total

    def _kill(self, p: subprocess.Popen, cname: str) -> None:
        if self.cfg.backend == "container":
            try:
                subprocess.run([self._runtime, "kill", cname], capture_output=True, timeout=20)
            except (subprocess.SubprocessError, OSError):
                pass
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            try:
                p.kill()
            except OSError:
                pass

    # -- interpreting results
    def _interpret(self, raw: RawRun, n_inputs: int, capture: bool) -> dict[str, Any]:
        out: dict[str, Any] = {"passed": False, "failure": None, "per_test": (), "outputs": None, "runtime": raw.wall_s}
        if raw.reason is not None:
            out["failure"] = raw.reason
            return out
        r = raw.result
        if r is None:
            if raw.returncode is not None and (raw.returncode < 0 or raw.returncode in (137, 143)) \
                    and not infrastructure_signal(raw.returncode):
                out["failure"] = "killed"
            else:
                out["failure"] = "sandbox_error"
            out["detail"] = raw.stderr_tail
            return out
        if "harness_error" in r:
            out["failure"] = "sandbox_error"
            out["detail"] = r["harness_error"]
            return out
        tests = r.get("tests", [])
        first = r.get("load_error") or (tests[0].get("e") if tests and tests[0]["s"] == "exception" else None)
        out["first_exception"] = first
        out["per_test"] = tuple(t["s"] == "pass" for t in tests)
        out["runtime"] = float(sum(t.get("t", 0.0) for t in tests)) or raw.wall_s
        if capture:
            outs = r.get("outputs")
            out["outputs"] = tuple(outs) if outs is not None else None
        if r.get("load_error"):
            out["failure"] = r.get("load_status") or "exception"
            out["per_test"] = ()
            return out
        if capture:
            out["passed"] = bool(outs is not None and len(outs) == n_inputs)
            if not out["passed"]:
                out["failure"] = "sandbox_error"
            return out
        bad = next((t["s"] for t in tests if t["s"] != "pass"), None)
        if bad is None and len(tests) == n_inputs:
            out["passed"] = True
        else:
            out["failure"] = bad or "wrong_output"
            if bad == "sandbox_error":
                out["failure"] = "sandbox_error"
        return out

    # -- Executor protocol
    def run(self, code: str, problem: Problem, suite: TestSuite, *, trusted: bool = False,
            capture_outputs: bool = False) -> ExecutionResult:
        self._require_allowed(trusted)
        capture = capture_outputs or suite.suite_id == "agree"
        lcb = problem.benchmark == "lcb_v6"
        ref = self._ensure_ref(problem, suite, capture)
        n = len(suite.inputs)
        limits = self._limits(problem, suite, ref)
        job = self._job_base()
        job.update({"code": code, "entry_point": problem.entry_point, "inputs": list(suite.inputs),
                    "time_limits": limits, "atol": float(suite.atol), "stop_on_fail": True})
        if lcb:
            job["mode"] = "lcb_agree" if capture else "lcb"
            job["fn_name"] = problem.entry_point if problem.io_kind == "function" else None
            if not capture:
                if suite.expected is None:
                    raise ValueError(f"{problem.problem_id}/{suite.suite_id}: LiveCodeBench label suites need expected outputs")
                job["expected"] = list(suite.expected)
            cap = self.cfg.program_cap_s
        else:
            job["dataset"] = "mbpp" if problem.benchmark == "mbpp_plus" else "humaneval"
            job["mode"] = "agree" if capture else "evalplus"
            if not capture:
                job["expected_pickle_b64"] = ref.expected_pickle_b64
            cap = min(self.cfg.program_cap_s, sum(limits) + self.cfg.startup_slack_s)
        key = self.cache_key(code, problem, suite, capture_outputs=capture_outputs)
        raw = self._launch(job, cap)
        got = self._interpret(raw, n, capture)
        self.run_info[key] = {"first_exception": got.get("first_exception")}
        if got["failure"] in ("sandbox_error", "killed"):
            self.diagnostics.append((key, got["failure"], str(got.get("detail", ""))[-500:], raw.returncode))
        res = ExecutionResult(cache_key=key, problem_id=problem.problem_id, suite_id=suite.suite_id,
                              passed=got["passed"], failure=got["failure"], per_test=tuple(got["per_test"]),
                              outputs=got["outputs"], runtime_s=float(got["runtime"]),
                              evaluator=self._evaluator_label(problem), sandbox=self.sandbox_label)
        return res

    def run_reference(self, problem: Problem, suite: TestSuite) -> dict[str, Any]:
        """Run the canonical solution on every input (trusted). Returns the harness's reference record."""
        job = self._job_base()
        job.update({"mode": "reference", "code": reference_program(problem), "entry_point": problem.entry_point,
                    "dataset": "mbpp" if problem.benchmark == "mbpp_plus" else "humaneval",
                    "inputs": list(suite.inputs)})
        raw = self._launch(job, self.cfg.program_cap_s)
        fail = {"ok": False, "failure": None, "error": None, "runtimes": [], "outputs_canon": [],
                "outputs_pickle_b64": None}
        if raw.reason is not None:
            return {**fail, "failure": raw.reason, "error": raw.reason}
        r = raw.result
        if r is None or "harness_error" in r:
            killed = raw.returncode is not None and raw.returncode < 0
            return {**fail, "failure": "killed" if killed else "sandbox_error",
                    "error": (r or {}).get("harness_error") or raw.stderr_tail[-200:]}
        return {k: r.get(k, fail[k]) for k in fail}

    # -- preflight
    def _probe(self, probe: str, **extra: Any) -> RawRun:
        job = self._job_base()
        job.update({"mode": "probe", "probe": probe, **extra})
        return self._launch(job, 30.0)

    def preflight_limits(self) -> dict[str, Any]:
        """Limits-only check, usable on every backend (including trusted-only): a trivial program runs,
        and an allocation beyond the memory limit is stopped (by MemoryError, by the watchdog, or by the
        container's OOM kill). Does not prove isolation."""
        report: dict[str, Any] = {"backend": self.cfg.backend}
        ok = self._probe("ok")
        report["ok"] = bool(ok.result and ok.result.get("result") == "OK")
        mem = self._probe("mem", memory_bytes=self.cfg.memory_bytes)
        limited = (mem.result is not None and mem.result.get("result") == "LIMITED") or mem.reason == "memory" or \
            (mem.result is None and mem.returncode is not None and mem.returncode < 0) or \
            (mem.result is None and mem.returncode in (137,))
        report["memory_limit_triggers"] = bool(limited)
        problems = [k for k in ("ok", "memory_limit_triggers") if not report[k]]
        if problems:
            raise IsolationError(f"limit preflight failed: {problems}; report={report}")
        return report

    def preflight(self) -> None:
        """Prove isolation before any untrusted run. Raises IsolationError unless, inside the sandbox:
        an outbound connect fails (the host listens on a loopback port, so no packet leaves this machine),
        writes outside the work dir fail while a write in it succeeds, and the memory limit triggers.
        The trusted-only backend cannot prove isolation and always raises."""
        if self.cfg.backend == "trusted-only":
            raise IsolationError("the trusted-only backend provides no network or filesystem isolation")
        report = self.preflight_limits()
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listener.bind(("127.0.0.1", 0))
            listener.listen(4)
            net = self._probe("net", port=listener.getsockname()[1])
        finally:
            listener.close()
        report["network_blocked"] = bool(net.result and net.result.get("result") == "BLOCKED")
        paths = ["/etc/calib_probe", "/usr/calib_probe", "/harness/calib_probe", "/job/calib_probe",
                 "/calib_probe_root", "/proc/calib_probe"]
        wr = self._probe("write", paths=paths + ["/work/calib_probe"])
        res = (wr.result or {}).get("results", {})
        report["outside_writes_denied"] = bool(res) and all(str(res.get(p, "")).startswith("DENIED") for p in paths)
        report["work_dir_writable"] = res.get("/work/calib_probe") == "WROTE"
        fk = self._probe("fork", limit=self.cfg.pids_limit)
        report["fork_limit_enforced"] = H.fork_limit_enforced(fk.result, self.cfg.pids_limit)
        report["fork_probe"] = {k: (fk.result or {}).get(k) for k in ("forked", "limit", "error")}
        if self.cfg.backend == "bwrap":
            report["cgroup_pids_max"] = self.cgroup_pids_ok()
            if not report["cgroup_pids_max"]:
                report["cgroup_pids_max_note"] = "cgroup v2 pids controller not writable here; RLIMIT_NPROC under a non-root uid only"
        failed = [k for k in ("network_blocked", "outside_writes_denied", "work_dir_writable", "fork_limit_enforced")
                  if not report[k]]
        self.preflight_report = report
        if failed:
            raise IsolationError(f"isolation preflight failed: {failed}; report={report}")
        self._isolation_proven = True
