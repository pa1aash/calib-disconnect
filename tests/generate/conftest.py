import pytest
import torch

import gen_tinylm as T


@pytest.fixture(scope="session")
def tok():
    return T.build_tokenizer()


@pytest.fixture(scope="session")
def model(tok):
    torch.manual_seed(0)
    return T.build_model(tok)


@pytest.fixture(scope="session")
def prompts():
    from pipeline.generate.prompts import load_prompts
    return load_prompts()
