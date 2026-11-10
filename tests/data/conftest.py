from __future__ import annotations

from pathlib import Path

import pytest

from data_helpers import CACHE


@pytest.fixture(scope="session")
def cache_dir() -> Path:
    return CACHE


@pytest.fixture(scope="session")
def loader(cache_dir):
    from pipeline.data.loader import DataLoader

    return DataLoader(cache_dir, workers=4)


@pytest.fixture(scope="session")
def he_problems(loader):
    return loader.problems("humaneval_plus")


@pytest.fixture(scope="session")
def mbpp_problems(loader):
    return loader.problems("mbpp_plus")
