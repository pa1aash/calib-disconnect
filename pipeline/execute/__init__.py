"""Module B2: code extraction, sandboxed execution, execution cache, labels, reference check.

The stage entry point is ``pipeline.execute.stage:run``. ``BASE_STOP_STRINGS`` is exported for the
generation module (base-model completion stops).
"""

from .cache import ExecCache
from .extract import BASE_STOP_STRINGS, extract_code, normalize_code, parse_sample_uid
from .labels import agreement_label_proxy, agreement_signatures, flip_table, label_samples
from .reference import ReferenceStore, exclusion_report, reference_check
from .sandbox import (
    IsolationError, ReferenceUnavailable, SandboxConfig, SandboxExecutor, UntrustedExecutionRefused,
)

__all__ = [
    "BASE_STOP_STRINGS", "ExecCache", "IsolationError", "ReferenceStore", "ReferenceUnavailable", "SandboxConfig",
    "SandboxExecutor", "UntrustedExecutionRefused", "agreement_label_proxy", "agreement_signatures",
    "exclusion_report", "extract_code", "flip_table", "label_samples", "normalize_code", "parse_sample_uid",
    "reference_check",
]
