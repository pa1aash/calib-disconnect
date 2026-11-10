"""The 7.12 mask-test gate: run before the first trained readout of each architecture class.

`run_mask_gate` takes the loaded model and real token layouts, runs `mask_unit_test` in float32 (on the
model itself if it is float32, otherwise on a float32 copy of its first layers with the real weights),
through the same padded layout and the same S^T forward used for training, writes the report to
`config/mask_test_<arch>.json`, and raises `MaskTestFailed` if it does not pass. The stage refuses to train
after that.
"""

from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Callable, Sequence

import torch

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import TeacherForcedLayout

from .masked_lora import LoraSpec, MaskedLoraModel, mask_unit_test


class MaskTestFailed(RuntimeError):
    pass


def arch_key(model) -> str:
    return str(model.config.get_text_config().model_type or model.config.model_type)


def float32_slice(model, n_layers: int = 2):
    """A float32 copy of `model` with its first `n_layers` decoder layers, embeddings, final norm, and head
    (real weights), on the model's device. The architecture class, projections, and attention are those of
    the real model, so the mask hooks run on the real code path."""
    cfg = copy.deepcopy(model.config)
    tc = cfg.get_text_config()
    tc.num_hidden_layers = min(n_layers, tc.num_hidden_layers)
    if getattr(tc, "layer_types", None):
        tc.layer_types = list(tc.layer_types)[:tc.num_hidden_layers]
    old = torch.get_default_dtype()
    torch.set_default_dtype(torch.float32)
    try:
        small = type(model)(cfg)
    finally:
        torch.set_default_dtype(old)
    sd = {k: v.detach().to("cpu", torch.float32) for k, v in model.state_dict().items()}
    small.load_state_dict({k: v for k, v in sd.items() if k in small.state_dict() and small.state_dict()[k].shape == v.shape},
                          strict=False)
    small.tie_weights()
    dev = next(model.parameters()).device
    return small.to(dev).eval()


def pick_layouts(layouts: Sequence[TeacherForcedLayout], n: int = 4) -> list[TeacherForcedLayout]:
    """Up to n layouts with the most common elicitation length and the most varied total lengths."""
    common = Counter(len(l.elicitation_ids) for l in layouts).most_common(1)[0][0]
    same = sorted((l for l in layouts if len(l.elicitation_ids) == common),
                  key=lambda l: len(l.prompt_ids) + len(l.completion_ids))
    if len(same) <= n:
        return same
    step = (len(same) - 1) / (n - 1)
    return [same[round(i * step)] for i in range(n)]


def run_mask_gate(model, layouts: Sequence[TeacherForcedLayout], report_path: Path, *,
                  yes_ids: Sequence[int], no_ids: Sequence[int], pad_id: int = 0,
                  register: Callable[[Path], None] | None = None, n_slice_layers: int = 2,
                  init_std: float = 0.1) -> dict:
    """Run once per architecture class; an existing passing report for the class is reused."""
    report_path = Path(report_path)
    if report_path.exists():
        old = json.loads(report_path.read_text())
        if old.get("passed"):
            return old
    dtype = next(model.parameters()).dtype
    test_model = model if dtype == torch.float32 else float32_slice(model, n_slice_layers)
    rep = mask_unit_test(test_model, pick_layouts(layouts), LoraSpec(), atol=K.MASK_TEST_ATOL, pad_id=pad_id,
                         yes_ids=yes_ids, no_ids=no_ids, init_std=init_std)
    rep = {**rep, "arch": arch_key(model), "model_class": type(model).__name__, "tested_dtype": "float32",
           "model_dtype": str(dtype), "tested_on": "model" if test_model is model else f"float32 slice of {n_slice_layers} layers"}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, indent=1, sort_keys=True) + "\n")
    if register is not None:
        register(report_path)
    if not rep["passed"]:
        raise MaskTestFailed(f"mask unit test failed for {rep['arch']}; see {report_path}")
    return rep
