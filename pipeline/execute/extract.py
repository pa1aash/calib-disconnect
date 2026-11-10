"""Code extraction from completions (design section 6, method rows 5.7 and 5.9).

Chat mode: the first fenced Python block; fallback from the first top-level ``def`` or ``class`` line to
the end of the text; a leading thought block is stripped first. Completion mode (base models, section
10): ``prompt + completion`` cut at the first stop string that occurs after the prompt.

Every failure carries one of ``constants.EXTRACTION_FAILURE_CODES``; an extraction failure is labeled
incorrect by ``labels.label_samples`` and is never executed. No code is repaired or renamed (row 5.8).
"""

from __future__ import annotations

import ast
import re
from typing import Sequence

from pipeline.contracts.constants import EXTRACTION_FAILURE_CODES
from pipeline.contracts.schemas import ExtractionResult

# Completion-mode stop strings (design section 10, base models). Exported so that the generation module
# imports the very same tuple: pipeline.execute.extract.BASE_STOP_STRINGS.
BASE_STOP_STRINGS: tuple[str, ...] = ("\ndef ", "\nclass ", "\nif __name__", "\nprint(", "\n#")

# Explicit list of thought-block markers. A thought block at the very start of the completion is
# removed before any other step. Each entry is (opening marker, closing marker, empty_only).
#  - Qwen3 style: "<think>" ... "</think>". With thinking off the block is empty (whitespace only).
#    With thinking on (reasoning stratum S1) the block holds reasoning, and fenced blocks inside it must
#    not be taken as the answer, so a non-empty block of this style is removed too.
#  - Gemma 4 style: the empty thought channel emitted with thinking off (design section 5). The exact
#    token spellings below are NOT VERIFIED against the model card or tokenizer; the pod run must check
#    them against the rendered chat template (a mismatch leaves the marker text in front of the code,
#    which the fenced-block search skips, so the failure mode is benign for the chat-mode extractor).
THOUGHT_MARKERS: tuple[tuple[str, str, bool], ...] = (
    ("<think>", "</think>", False),
    ("<|channel>thought", "<channel|>", True),
    ("<|channel|>thought", "<|channel|>", True),
    ("<start_of_thought>", "<end_of_thought>", True),
)

_FENCE_RE = re.compile(
    r"^[ \t]*(`{3,}|~{3,})[ \t]*([A-Za-z0-9_+\-#.]*)[^\n]*\n(.*?)(?:^[ \t]*\1[ \t]*$|\Z)",
    re.MULTILINE | re.DOTALL,
)
_PY_TAGS = frozenset({"python", "python3", "py", "py3", "python2", "cpython", "pycon"})
_DEF_RE = re.compile(r"^(?:async[ \t]+def|def|class)[ \t]", re.MULTILINE)

assert set(EXTRACTION_FAILURE_CODES) == {"no_block", "syntax_error", "missing_entry_point", "empty_output",
                                         "truncated"}


def strip_leading_thought(text: str) -> str:
    """Remove one leading thought block (see THOUGHT_MARKERS). Leading whitespace is ignored when looking
    for the opening marker; the text after the closing marker is returned unchanged."""
    s = text.lstrip()
    for open_m, close_m, empty_only in THOUGHT_MARKERS:
        if s.startswith(open_m):
            end = s.find(close_m, len(open_m))
            if end < 0:
                continue
            inner = s[len(open_m):end]
            if empty_only and inner.strip() not in ("", "\n"):
                continue
            if open_m == "<think>" and not empty_only:
                # A reasoning block may mention "</think>" only once; take the last close so that a
                # nested mention cannot leave reasoning text in front of the answer.
                end = s.rfind(close_m)
            return s[end + len(close_m):]
    return text


def _looks_like_python(block: str) -> bool:
    try:
        ast.parse(block)
        return bool(block.strip())
    except (SyntaxError, ValueError, RecursionError, MemoryError):
        pass
    return bool(re.search(r"^\s*(def |class |import |from \S+ import |print\(|return\b|for \w+ in |if .*:)",
                          block, re.MULTILINE))


def _first_python_block(text: str) -> str | None:
    for m in _FENCE_RE.finditer(text):
        tag = m.group(2).lower()
        body = m.group(3)
        if tag in _PY_TAGS:
            return body
        if tag == "" and _looks_like_python(body):
            return body
    return None


def _fallback_from_def(text: str) -> str | None:
    m = _DEF_RE.search(text)
    return None if m is None else text[m.start():]


def _defines_entry_point(tree: ast.Module, entry_point: str) -> bool:
    return any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == entry_point
               for n in tree.body)


def _defines_solution_method(tree: ast.Module, method: str) -> bool:
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == "Solution":
            if any(isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)) and b.name == method for b in n.body):
                return True
    return False


def parse_sample_uid(sample_uid: str) -> dict[str, str]:
    """Inverse of schemas.sample_uid: model_key|generation_set|benchmark|problem_id|sample_index."""
    parts = sample_uid.split("|")
    if len(parts) != 5:
        raise ValueError(f"not a sample uid: {sample_uid!r}")
    return {"model_key": parts[0], "generation_set": parts[1], "benchmark": parts[2], "problem_id": parts[3],
            "sample_index": parts[4]}


def _benchmark_of(sample_uid: str) -> str | None:
    try:
        return parse_sample_uid(sample_uid)["benchmark"]
    except ValueError:
        return None


def _fail(sample_uid: str, code: str) -> ExtractionResult:
    assert code in EXTRACTION_FAILURE_CODES
    return ExtractionResult(sample_uid=sample_uid, code=None, method=None, failure=code)


def _validate(sample_uid: str, code: str, method: str, entry_point: str | None,
              benchmark: str | None) -> ExtractionResult:
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError, RecursionError, MemoryError):
        return _fail(sample_uid, "syntax_error")
    if entry_point is not None:
        if benchmark == "lcb_v6":
            ok = _defines_solution_method(tree, entry_point)
        else:
            ok = _defines_entry_point(tree, entry_point)
        if not ok:
            return _fail(sample_uid, "missing_entry_point")
    return ExtractionResult(sample_uid=sample_uid, code=code, method=method, failure=None)


def extract_code(sample_uid: str, completion_text: str, entry_point: str | None, truncated: bool,
                 mode: str = "chat", prompt: str | None = None, *,
                 benchmark: str | None = None,
                 stop_strings: Sequence[str] = BASE_STOP_STRINGS) -> ExtractionResult:
    """Extract the program from one completion.

    benchmark defaults to the benchmark field of sample_uid. For "lcb_v6" with an entry point, the code
    must define ``class Solution`` with that method; for the other benchmarks it must define a top-level
    function of that name; with entry_point None (stdin programs) no entry-point check is made.

    "truncated" takes precedence in chat mode; the code is not kept (code=None) and the label is
    incorrect. In completion mode, a truncated completion that already contains a stop string is not a
    truncation (the function ended before the token cap); this is a stated divergence from the chat rule.
    """
    if mode not in ("chat", "completion"):
        raise ValueError(f"unknown mode {mode!r}")
    bench = benchmark if benchmark is not None else _benchmark_of(sample_uid)

    if mode == "completion":
        if prompt is None:
            raise ValueError("completion mode needs the prompt")
        if not completion_text.strip():
            return _fail(sample_uid, "truncated" if truncated else "empty_output")
        full = prompt + completion_text
        # A stop string may start on the prompt's last character (a newline), so the search starts there.
        start = max(len(prompt) - 1, 0)
        cut = len(full)
        found = False
        for s in stop_strings:
            i = full.find(s, start)
            if i != -1 and i < cut:
                cut, found = i, True
        if truncated and not found:
            return _fail(sample_uid, "truncated")
        code = full[:cut]
        if cut <= len(prompt):
            # The model started a new top-level definition immediately: no body was written.
            return _fail(sample_uid, "empty_output")
        return _validate(sample_uid, code, "completion", entry_point, bench)

    if truncated:
        return _fail(sample_uid, "truncated")
    text = strip_leading_thought(completion_text)
    if not text.strip():
        return _fail(sample_uid, "empty_output")
    block = _first_python_block(text)
    method = "fenced"
    if block is None:
        block = _fallback_from_def(text)
        method = "fallback_def"
    if block is None:
        return _fail(sample_uid, "no_block")
    if not block.strip():
        return _fail(sample_uid, "empty_output")
    return _validate(sample_uid, block, method, entry_point, bench)


def normalize_code(code: str) -> str:
    """``ast.unparse`` of the parsed module, or the raw text if parsing fails (design section 6)."""
    try:
        return ast.unparse(ast.parse(code))
    except Exception:  # SyntaxError, ValueError (null bytes), RecursionError, MemoryError subclasses
        return code
