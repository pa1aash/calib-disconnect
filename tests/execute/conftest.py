"""Fixtures for the execute module tests. Only hand-written trusted fixtures and benchmark reference
solutions are ever executed here; model-generated code is never run (project rule)."""

import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from execute_helpers import load_heplus, load_mbppplus  # noqa: E402

from pipeline.execute.sandbox import SandboxExecutor  # noqa: E402


def pytest_collection_modifyitems(config, items):
    have_isolation = bool(shutil.which("bwrap") or shutil.which("docker") or shutil.which("podman"))
    skip = pytest.mark.skip(reason="needs bubblewrap or a container runtime (pod only)")
    for item in items:
        if "pod" in item.keywords and not have_isolation:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def heplus():
    rows = load_heplus()
    if rows is None:
        pytest.skip("HumanEval+ cache file not present")
    return rows


@pytest.fixture(scope="session")
def mbppplus():
    rows = load_mbppplus()
    if rows is None:
        pytest.skip("MBPP+ cache file not present")
    return rows


@pytest.fixture()
def executor():
    """Trusted-only backend with short limits so that the timeout fixtures finish quickly."""
    from pipeline.execute.sandbox import SandboxConfig

    ex = SandboxExecutor(SandboxConfig(backend="trusted-only", min_time_limit=0.3, program_cap_s=20.0,
                                       memory_bytes=512 * 1024 * 1024))
    return ex
