"""LiveCodeBench evaluator through the harness (hand-written fixtures, trusted-only backend), the
vendored file's provenance, and the bwrap and container command builders (argument lists only; the
tests that need the real backends are marked pod and skipped here)."""

import hashlib
import re
from pathlib import Path

import pytest

from pipeline.contracts.schemas import Problem, TestSuite
from pipeline.execute import SandboxConfig, SandboxExecutor
from pipeline.execute import sandbox as sb

VENDOR = Path(sb.__file__).parent / "vendor" / "lcb"


# ---- vendored evaluator -------------------------------------------------------------------------------
def test_vendored_file_matches_its_recorded_hash_and_commit():
    prov = (VENDOR / "PROVENANCE.md").read_text()
    sha = hashlib.sha256((VENDOR / "testing_util.py").read_bytes()).hexdigest()
    assert sha in prov and sb.LCB_COMMIT in prov
    assert hashlib.sha256((VENDOR / "LICENSE").read_bytes()).hexdigest() in prov
    assert "MIT" in prov and "2026-11-10" in prov
    # git blob hash of the verbatim file
    data = (VENDOR / "testing_util.py").read_bytes()
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    assert blob in prov


# ---- LiveCodeBench fixtures ---------------------------------------------------------------------------------
def stdin_problem():
    return Problem("lcb/s1", "lcb_v6", "Add.", None, None, "stdin", "2025-01-01")


def func_problem():
    return Problem("lcb/f1", "lcb_v6", "Add.", "add", None, "function", "2025-01-01",
                   starter_code="class Solution:\n    def add(self, a: int, b: int) -> int:\n        pass")


def suite(pid, sid, inputs, expected):
    return TestSuite(pid, sid, tuple(inputs), None if expected is None else tuple(expected), 0.0,
                     "lcb per-test timeout", "")


@pytest.fixture()
def lcb_executor():
    return SandboxExecutor(SandboxConfig(backend="trusted-only", lcb_timeout_s=1, program_cap_s=15.0))


STDIN_OK = "a, b = map(int, input().split())\nprint(a + b)\n"


def test_lcb_stdin_pass_and_wrong_and_error(lcb_executor):
    p = stdin_problem()
    s = suite(p.problem_id, "lcb_label", ["1 2\n", "30 12\n"], ["3\n", "42\n"])
    r = lcb_executor.run(STDIN_OK, p, s, trusted=True)
    assert r.passed and r.per_test == (True, True) and r.evaluator.startswith("lcb@28fef95ea8")
    assert r.suite_id == "lcb_label"
    r = lcb_executor.run("a, b = map(int, input().split())\nprint(a - b)\n", p, s, trusted=True)
    assert not r.passed and r.failure == "wrong_output" and r.per_test[-1] is False
    r = lcb_executor.run("raise ValueError('x')\n", p, s, trusted=True)
    assert not r.passed and r.failure == "exception"
    r = lcb_executor.run("print(", p, s, trusted=True)
    assert not r.passed and r.failure == "exception"


def test_lcb_stdin_tolerates_trailing_whitespace_and_float_formatting(lcb_executor):
    p = stdin_problem()
    s = suite(p.problem_id, "lcb_public", ["1\n"], ["0.5\n"])
    assert lcb_executor.run("print('0.50  ')\n", p, s, trusted=True).passed       # decimal comparison, as upstream
    assert lcb_executor.run("input()\nprint('0.5')\nprint()\n", p, s, trusted=True).passed
    assert not lcb_executor.run("print('0.6')\n", p, s, trusted=True).passed


def test_lcb_timeout_uses_the_evaluators_own_limit(lcb_executor):
    p = stdin_problem()
    s = suite(p.problem_id, "lcb_public", ["1\n"], ["1\n"])
    r = lcb_executor.run("while True:\n    pass\n", p, s, trusted=True)
    assert not r.passed and r.failure == "timeout"
    assert 0.8 < r.runtime_s < 10


def test_lcb_functional(lcb_executor):
    p = func_problem()
    s = suite(p.problem_id, "lcb_public", ["1\n2", "30\n12"], ["3", "42"])
    good = "class Solution:\n    def add(self, a: int, b: int) -> int:\n        return a + b\n"
    assert lcb_executor.run(good, p, s, trusted=True).passed
    r = lcb_executor.run(good.replace("a + b", "a - b"), p, s, trusted=True)
    assert not r.passed and r.failure == "wrong_output"
    r = lcb_executor.run("class Solution:\n    def other(self):\n        pass\n", p, s, trusted=True)
    assert not r.passed and r.failure == "exception"
    r = lcb_executor.run(good.replace("a + b", "1 // 0"), p, s, trusted=True)
    assert not r.passed and r.failure == "exception"


def test_lcb_agreement_capture(lcb_executor):
    p = stdin_problem()
    s = suite(p.problem_id, "agree", ["1 2\n", "x y\n", "3.0 4.5\n"], None)
    prog = "a, b = input().split()\nprint(float(a) + float(b))\n"
    r = lcb_executor.run(prog, p, s, trusted=True)
    assert r.passed and r.outputs == ("'3.0'", "!ValueError", "'7.5'") and r.per_test == (True, False, True)
    q = func_problem()
    fs = suite(q.problem_id, "agree", ["1\n2", '"a"\n"b"'], None)
    good = "class Solution:\n    def add(self, a, b):\n        return a + b\n"
    r = lcb_executor.run(good, q, fs, trusted=True)
    assert r.outputs == ("3", "'ab'")
    r = lcb_executor.run("class Solution:\n    def add(self, a, b):\n        return a / b\n", q, fs, trusted=True)
    assert r.outputs == ("0.5", "!TypeError")


def test_lcb_cache_keys_differ_by_suite(lcb_executor):
    p = stdin_problem()
    a = suite(p.problem_id, "lcb_public", ["1\n"], ["1\n"])
    b = suite(p.problem_id, "lcb_label", ["1\n", "2\n"], ["1\n", "2\n"])
    assert lcb_executor.cache_key(STDIN_OK, p, a) != lcb_executor.cache_key(STDIN_OK, p, b)


# ---- command builders (argument lists) ------------------------------------------------------------------------
BW = dict(bwrap="/usr/bin/bwrap", interpreter="/opt/py/bin/python", job_dir="/tmp/job1", bundle_dir="/tmp/bundle1",
          ro_binds=("/usr", "/opt/py"), symlinks={"/lib": "usr/lib", "/lib64": "usr/lib64"},
          prlimit="/usr/bin/prlimit")


def pairs(argv, flag):
    return [tuple(argv[i + 1:i + 3]) for i, a in enumerate(argv) if a == flag]


def test_bwrap_argv():
    a = sb.build_bwrap_argv(**BW)
    assert a[0] == "/usr/bin/bwrap"
    for flag in ("--unshare-all", "--die-with-parent", "--new-session", "--clearenv"):
        assert flag in a
    assert "--share-net" not in a and "--bind" not in a and "--dev-bind" not in a      # nothing writable from the host
    assert ("/usr", "/usr") in pairs(a, "--ro-bind") and ("/opt/py", "/opt/py") in pairs(a, "--ro-bind")
    assert ("/tmp/job1", "/job") in pairs(a, "--ro-bind") and ("/tmp/bundle1", "/harness") in pairs(a, "--ro-bind")
    assert ("usr/lib", "/lib") in pairs(a, "--symlink")
    assert a[a.index("--tmpfs") + 1] == "/work" and a[a.index("--chdir") + 1] == "/work"
    assert ("PYTHONHASHSEED", "0") in pairs(a, "--setenv")
    assert not any(k == "PATH" and v.startswith("/Users") for k, v in pairs(a, "--setenv"))
    i = a.index("--")                                                                    # prlimit wrapper
    assert a[i - 5].startswith("/usr/bin/prlimit") and any(x.startswith("--cpu=") for x in a[i - 4:i])
    assert any(x.startswith("--fsize=") for x in a[:i]) and "--core=0" in a
    assert a[i + 1:] == ["/opt/py/bin/python", "-s", "-B", "/harness/harness.py", "--job", "/job/job.pkl",
                         "--result", "-"]


def test_bwrap_argv_without_prlimit():
    a = sb.build_bwrap_argv(**{**BW, "prlimit": None})
    assert "--" not in a and a[-8] == "/opt/py/bin/python"


DIGEST = "a" * 64
IMG = f"registry.example/py@sha256:{DIGEST}"


def test_container_argv():
    a = sb.build_container_argv(runtime="/usr/bin/docker", image=IMG, name="calib-1", job_dir="/tmp/job1",
                                bundle_dir="/tmp/bundle1")
    assert a[:3] == ["/usr/bin/docker", "run", "--rm"]
    assert a[a.index("--network") + 1] == "none"
    assert "--read-only" in a and "--privileged" not in a
    assert a[a.index("--tmpfs") + 1].startswith("/work:rw")
    assert a[a.index("--memory") + 1] == str(2 * 1024**3) == a[a.index("--memory-swap") + 1]
    assert a[a.index("--pids-limit") + 1] == "64" and a[a.index("--cpus") + 1] == "1.0"
    assert a[a.index("--user") + 1] == "65534:65534" and a[a.index("--cap-drop") + 1] == "ALL"
    assert "no-new-privileges" in a
    vols = pairs(a, "-v")
    assert {v for (v,) in [(x[0],) for x in vols]} == {"/tmp/job1:/job:ro", "/tmp/bundle1:/harness:ro"}
    i = a.index(IMG)
    assert a[i + 1:] == ["/usr/local/bin/python", "-s", "-B", "/harness/harness.py", "--job", "/job/job.pkl",
                         "--result", "-"]
    assert "PYTHONHASHSEED=0" in a


def test_container_image_must_be_pinned_by_digest():
    kw = dict(runtime="docker", name="n", job_dir="/j", bundle_dir="/b")
    with pytest.raises(ValueError):
        sb.build_container_argv(image="python:3.12", **kw)
    with pytest.raises(ValueError):
        sb.build_container_argv(image="python@sha256:abc", **kw)
    assert sb.image_digest(IMG) == DIGEST


def test_trusted_argv_and_env():
    a = sb.build_trusted_argv("/py/bin/python", "/bundle", "/job/job.pkl", "/work/result.json")
    assert a == ["/py/bin/python", "-s", "-B", "/bundle/harness.py", "--job", "/job/job.pkl", "--result",
                 "/work/result.json"]
    env = sb.sandbox_env("/work")
    assert env["PYTHONHASHSEED"] == "0" and env["HOME"] == "/work" and "PYTHONPATH" not in env
    assert set(env) == {"PATH", "HOME", "TMPDIR", "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "PYTHONNOUSERSITE",
                        "PYTHONUTF8", "PYTHONIOENCODING", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                        "MKL_NUM_THREADS"}


def test_no_secret_like_environment_is_forwarded():
    env = sb.sandbox_env()
    assert not any(re.search(r"KEY|TOKEN|SECRET|PASS", k) for k in env)


def test_harness_bundle_is_read_only_and_hashed(executor):
    import os
    import stat

    for name in ("harness.py", "lcb_capture.py", "testing_util.py"):
        mode = os.stat(os.path.join(executor.bundle_dir, name)).st_mode
        assert not mode & stat.S_IWUSR
    assert len(executor.bundle_sha256) == 64


# ---- pod-only: real isolation ---------------------------------------------------------------------------------------
@pytest.mark.pod
def test_bwrap_preflight_and_run_on_the_pod(heplus):
    import shutil

    if not shutil.which("bwrap"):
        pytest.skip("no bwrap")
    from execute_helpers import build

    ex = SandboxExecutor(SandboxConfig(backend="bwrap", execute_untrusted=True, min_time_limit=0.5))
    ex.preflight()
    assert ex.preflight_report["network_blocked"] and ex.preflight_report["outside_writes_denied"]
    p, s = build(heplus, "HumanEval/53", "humaneval_plus", max_plus=20)
    ok = ex.run("def add(x: int, y: int):\n    return x + y\n", p, s["O"], trusted=True)
    assert ok.passed and ok.sandbox == "bwrap"


@pytest.mark.pod
def test_container_preflight_on_the_pod():
    import os
    import shutil

    img = os.environ.get("CALIB_TEST_IMAGE")
    if not (shutil.which("docker") or shutil.which("podman")) or not img:
        pytest.skip("no container runtime or CALIB_TEST_IMAGE")
    ex = SandboxExecutor(SandboxConfig(backend="container", container_image=img, execute_untrusted=True))
    ex.preflight()
    assert ex.preflight_report["network_blocked"]
