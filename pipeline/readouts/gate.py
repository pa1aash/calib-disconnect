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
import re
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


def slice_layer_indices(layer_types, n_total: int, n_layers: int = 2) -> list[int]:
    """Decoder layers kept in the float32 slice: the first layer of every distinct value in `layer_types`
    (for example sliding_attention and full_attention), padded with the earliest unused layers up to
    `n_layers`, in original order. Without `layer_types`: the first `n_layers` layers."""
    if not layer_types:
        return list(range(min(n_layers, n_total)))
    first: dict = {}
    for i, t in enumerate(list(layer_types)[:n_total]):
        first.setdefault(t, i)
    keep = set(first.values())
    for i in range(n_total):
        if len(keep) >= n_layers:
            break
        keep.add(i)
    return sorted(keep)


def float32_slice(model, n_layers: int = 2):
    """A float32 copy of `model` with a few decoder layers (see `slice_layer_indices`), embeddings, final norm,
    and head (real weights), on the model's device. Returns (model, kept layer indices). The architecture
    class, projections, and every attention type present in the real model run on the real code path."""
    cfg = copy.deepcopy(model.config)
    tc = cfg.get_text_config()
    types = getattr(tc, "layer_types", None)
    idx = slice_layer_indices(types, tc.num_hidden_layers, n_layers)
    tc.num_hidden_layers = len(idx)
    if types:
        tc.layer_types = [list(types)[i] for i in idx]
    old = torch.get_default_dtype()
    torch.set_default_dtype(torch.float32)
    try:
        small = type(model)(cfg)
    finally:
        torch.set_default_dtype(old)
    new_of = {i: j for j, i in enumerate(idx)}
    pat = re.compile(r"(\.layers\.)(\d+)(\.)")
    sd = {}
    for k, v in model.state_dict().items():
        m = pat.search(k)
        if m:
            if int(m.group(2)) not in new_of:
                continue
            k = pat.sub(lambda mm: f"{mm.group(1)}{new_of[int(mm.group(2))]}{mm.group(3)}", k, count=1)
        sd[k] = v.detach().to("cpu", torch.float32)
    own = small.state_dict()
    small.load_state_dict({k: v for k, v in sd.items() if k in own and own[k].shape == v.shape}, strict=False)
    small.tie_weights()
    return small.to(next(model.parameters()).device).eval(), idx


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
            if register is not None:      # a reused report is still a run product (smoke run finding)
                register(report_path)
            return old
    dtype = next(model.parameters()).dtype
    kept = None
    if dtype == torch.float32:
        test_model = model
    else:
        test_model, kept = float32_slice(model, n_slice_layers)
    rep = mask_unit_test(test_model, pick_layouts(layouts), LoraSpec(), atol=K.MASK_TEST_ATOL, pad_id=pad_id,
                         yes_ids=yes_ids, no_ids=no_ids, init_std=init_std)
    rep = {**rep, "arch": arch_key(model), "model_class": type(model).__name__, "tested_dtype": "float32",
           "model_dtype": str(dtype), "tested_on": "model" if test_model is model else f"float32 slice of {len(kept)} layers",
           "slice_layer_indices": kept, "layer_types": getattr(model.config.get_text_config(), "layer_types", None)}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, indent=1, sort_keys=True) + "\n")
    if register is not None:
        register(report_path)
    if not rep["passed"]:
        raise MaskTestFailed(f"mask unit test failed for {rep['arch']}; see {report_path}")
    return rep
