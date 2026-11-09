"""Shared fixtures for the prose linter tests."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import prose_lint  # noqa: E402


@pytest.fixture(scope="session")
def cfg():
    return prose_lint.load_config(TOOLS / "prose_lint.toml")


@pytest.fixture
def lint(cfg):
    """Return a function lint(body, mode='latex', wrap=True) -> list of findings.

    In latex mode with wrap=True the body is placed inside a minimal document.
    """

    def run(body, mode="latex", wrap=True):
        if mode == "latex" and wrap:
            body = "\\documentclass{article}\n\\begin{document}\n" + body + "\n\\end{document}\n"
        return prose_lint.lint_text(body, mode, cfg, "fixture")

    return run


def cats(findings, severity=None):
    return [f.category for f in findings if severity is None or f.severity == severity]
