from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.contracts.layout import REPO_ROOT
from pipeline.data import pins as pinmod

CACHE = REPO_ROOT / "docs" / "s7" / "parts" / "bench-A2" / "cache"


def _cache_present() -> bool:
    return all(pinmod.locate(pinmod.PINS[k], CACHE) is not None for k in ("humaneval_plus", "mbpp_plus", "mbpp_plus_patch"))


needs_cache = pytest.mark.skipif(not _cache_present(), reason="bench-A2 cache is absent")


