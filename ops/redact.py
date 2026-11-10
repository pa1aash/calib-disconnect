"""Redaction helpers. Any secret, token, pod ID, host address, or key filename is shown as at most
its first 4 characters followed by "...". Short values show fewer characters so that a short value is
never revealed in full."""

from __future__ import annotations

import os
from typing import Iterable, Mapping

SECRET_ENV_NAMES = ("RUNPOD_API_KEY", "HF_TOKEN", "POD_SSH_HOST", "POD_SSH_PORT", "POD_SSH_KEY")


def redact(value: object) -> str:
    """First min(4, len // 2) characters plus "...". Empty or None gives "<unset>"."""
    if value is None:
        return "<unset>"
    s = str(value)
    if not s:
        return "<unset>"
    return s[: min(4, len(s) // 2)] + "..."


def scrub(text: str, env: Mapping[str, str] | None = None, names: Iterable[str] = SECRET_ENV_NAMES) -> str:
    """Replace every occurrence of a known secret value in text by its redacted form."""
    env = os.environ if env is None else env
    out = text
    for n in names:
        v = env.get(n)
        if v and len(v) >= 3:
            out = out.replace(v, redact(v))
    return out
