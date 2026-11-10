"""Token-level helpers: elicitation turns, answer-token variants, and code-span mapping.

Elicitation turns (design 5 and 7.12). The V1 and V2 user turns are appended after the frozen
completion. Their token ids are derived from the model's own chat template without ever re-tokenizing
the frozen completion:

    render [user G, assistant A, user U] with unique sentinels for G, A, and U and add_generation_prompt;
    the text between A and U is  EOT + bridge + header,  the text after U is the assistant header.
    elicitation text = header + <V1 or V2 text> + assistant header.

This is "render the trailing turn" and is independent of how a template rewrites earlier turns (for
example Qwen3 drops the empty thought block of earlier assistant turns). The separator whitespace
between the end-of-turn token and the user header (for example the newline after <|im_end|>) is the
bridge. The bridge is appended to the completion ids, so the teacher-forced sequence equals the
template rendering of the conversation, while the elicitation span begins at the first token of the
user header. Elicitation turns always render with thinking off (design 5, reasoning models).

Base models use the plain-text frame of base_elicitation_frame.txt: the suffix after {program}.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Sequence

from pipeline.contracts import constants as C

from .prompts import PromptSet, apply_chat, encode_prompt, render_generation_prompt

SENT_G = "QXGENQX"
SENT_A = "QXASSTQX"
SENT_U = "QXUSERQX"
THOUGHT_END_MARKERS = ("</think>",)


# ---------------------------------------------------------------------------------------------------
# Elicitation turns
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class TurnSpec:
    chat: bool
    eot_text: str
    eot_id: int | None
    bridge_text: str
    bridge_ids: tuple[int, ...]
    elicitation_text: dict[str, str]
    elicitation_ids: dict[str, tuple[int, ...]]
    prefix_identity: bool           # full-conversation render reproduces prompt + completion + turn ids
    notes: tuple[str, ...] = ()

    def describe(self, tokenizer: Any) -> dict[str, Any]:
        v2 = self.elicitation_ids["V2"]
        return {
            "rule": ("trailing-turn render with sentinels; span = first token of the user header through the "
                     "assistant header; bridge whitespace between end-of-turn and header is appended to the "
                     "completion ids, outside the span") if self.chat else
                    "plain-text frame suffix after the program; span = whole suffix",
            "chat": self.chat,
            "eot_token": self.eot_text, "eot_id": self.eot_id,
            "bridge_text": self.bridge_text, "bridge_n_tokens": len(self.bridge_ids),
            "elicitation_n_tokens": {k: len(v) for k, v in sorted(self.elicitation_ids.items())},
            "elicitation_text_v2": self.elicitation_text["V2"],
            "first_span_token": tokenizer.convert_ids_to_tokens(v2[0]),
            "p3_token": tokenizer.convert_ids_to_tokens(v2[-1]),
            "prefix_identity": self.prefix_identity,
            "notes": list(self.notes),
        }


def _special_strings(tokenizer: Any) -> list[str]:
    out = set()
    if getattr(tokenizer, "eos_token", None):
        out.add(tokenizer.eos_token)
    for tok in getattr(tokenizer, "added_tokens_decoder", {}).values():
        if getattr(tok, "special", False):
            out.add(str(tok))
    return sorted(out, key=len, reverse=True)


def _enc(tokenizer: Any, text: str) -> list[int]:
    return [int(i) for i in tokenizer(text, add_special_tokens=False)["input_ids"]] if text else []


def derive_turns(tokenizer: Any, prompts: PromptSet, *, chat: bool) -> TurnSpec:
    fmts = ("V1", "V2")
    if not chat:
        texts = {f: prompts.base_frame_suffix(f) for f in fmts}
        return TurnSpec(chat=False, eot_text="", eot_id=None, bridge_text="", bridge_ids=(),
                        elicitation_text=texts, elicitation_ids={f: tuple(_enc(tokenizer, t)) for f, t in texts.items()},
                        prefix_identity=True)
    notes: list[str] = []
    # End-of-turn string: the special token that follows an assistant message in the template.
    b_text = apply_chat(tokenizer, [{"role": "user", "content": SENT_G}, {"role": "assistant", "content": SENT_A}],
                        add_generation_prompt=False, thinking=False)
    if b_text.count(SENT_A) != 1:
        raise ValueError("chat template does not render assistant content exactly once")
    post = b_text.split(SENT_A, 1)[1]
    eot_text = next((s for s in _special_strings(tokenizer) if post.startswith(s)), "")
    eot_id = tokenizer.convert_tokens_to_ids(eot_text) if eot_text else None
    if not eot_text:
        notes.append("no end-of-turn special token follows an assistant message in the template")
    # Trailing turn.
    c_text = apply_chat(tokenizer, [{"role": "user", "content": SENT_G}, {"role": "assistant", "content": SENT_A},
                                    {"role": "user", "content": SENT_U}], add_generation_prompt=True, thinking=False)
    for s in (SENT_G, SENT_A, SENT_U):
        if c_text.count(s) != 1:
            raise ValueError(f"chat template renders {s} {c_text.count(s)} times (expected once)")
    mid, tail = c_text.split(SENT_A, 1)[1].split(SENT_U, 1)
    if eot_text and mid.startswith(eot_text):
        rest = mid[len(eot_text):]
    else:
        if eot_text:
            notes.append("end-of-turn token not rendered between turns in the multi-turn render")
        eot_text, eot_id, rest = "", None, mid
    bridge_text = re.match(r"\s*", rest).group(0)
    header = rest[len(bridge_text):]
    bridge_ids = tuple(_enc(tokenizer, bridge_text))
    texts = {f: header + prompts.elicit_text(f) + tail for f in fmts}
    ids = {f: tuple(_enc(tokenizer, t)) for f, t in texts.items()}
    joint = _enc(tokenizer, bridge_text + texts["V2"])
    if bridge_text and tuple(joint[:len(bridge_ids)]) != bridge_ids:
        notes.append("bridge tokens are not separable from the header tokens; bridge dropped")
        bridge_text, bridge_ids = "", ()
    # Diagnostic: does the plain full-conversation render reproduce prompt + completion + turn?
    probe_user, probe_completion = "QXPROBEQX", "print(1)"
    prompt_ids = encode_prompt(tokenizer, render_generation_prompt(tokenizer, probe_user, thinking=False), chat=True)
    expected = prompt_ids + _enc(tokenizer, probe_completion) + ([eot_id] if eot_id is not None else []) \
        + list(bridge_ids) + list(ids["V2"])
    full = apply_chat(tokenizer, [{"role": "user", "content": probe_user},
                                  {"role": "assistant", "content": probe_completion},
                                  {"role": "user", "content": prompts.elicit_text("V2")}],
                      add_generation_prompt=True, thinking=False)
    identity = _enc(tokenizer, full) == expected
    if not identity:
        notes.append("template rewrites earlier turns or differs from prompt + completion + turn; "
                     "elicitation derived from the trailing turn alone")
    return TurnSpec(chat=True, eot_text=eot_text, eot_id=eot_id, bridge_text=bridge_text, bridge_ids=bridge_ids,
                    elicitation_text=texts, elicitation_ids=ids, prefix_identity=identity, notes=tuple(notes))


def stop_token_ids(tokenizer: Any, model: Any | None, spec: TurnSpec) -> tuple[int, ...]:
    """Token ids that end a generation: the template's end-of-turn token, the tokenizer EOS, and the
    generation config EOS ids."""
    ids: list[int] = []
    if spec.eot_id is not None:
        ids.append(int(spec.eot_id))
    if getattr(tokenizer, "eos_token_id", None) is not None:
        ids.append(int(tokenizer.eos_token_id))
    gc = getattr(model, "generation_config", None)
    e = getattr(gc, "eos_token_id", None)
    if e is not None:
        ids.extend(int(i) for i in (e if isinstance(e, (list, tuple)) else [e]))
    return tuple(dict.fromkeys(ids))


# ---------------------------------------------------------------------------------------------------
# Answer tokens (7.12)
# ---------------------------------------------------------------------------------------------------
def decode_ids(tokenizer: Any, ids: Sequence[int]) -> str:
    return tokenizer.decode([int(i) for i in ids], skip_special_tokens=False, clean_up_tokenization_spaces=False)


def answer_token_variants(tokenizer: Any, yes_strings: Sequence[str] = C.YES_STRINGS,
                          no_strings: Sequence[str] = C.NO_STRINGS) -> dict[str, list[dict[str, Any]]]:
    """Every single token whose decoded text, with leading whitespace removed, is exactly a Yes string
    (respectively a No string). Lowercase, uppercase, and longer words do not count."""
    vocab = tokenizer.get_vocab()
    out: dict[str, list[dict[str, Any]]] = {"yes": [], "no": []}
    for key, strings in (("yes", yes_strings), ("no", no_strings)):
        for tok, tid in vocab.items():
            if not any(s in tok for s in strings):
                continue
            text = decode_ids(tokenizer, [tid])
            if text.lstrip() in strings:
                out[key].append({"id": int(tid), "token": tok, "text": text})
        out[key].sort(key=lambda d: d["id"])
        if not out[key]:
            raise ValueError(f"tokenizer has no single token for {strings}")
    return out


# ---------------------------------------------------------------------------------------------------
# Code spans
# ---------------------------------------------------------------------------------------------------
_FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)


def thought_end(decoded: str) -> int:
    """Character index just after the last thought-block end marker, or 0."""
    best = 0
    for m in THOUGHT_END_MARKERS:
        i = decoded.rfind(m)
        if i >= 0:
            best = max(best, i + len(m))
    return best


def first_fenced_interior(decoded: str, start: int = 0) -> tuple[int, int] | None:
    m = _FENCE.search(decoded, start)
    return (m.start(1), m.end(1)) if m else None


def locate_code(decoded: str, code: str) -> tuple[int, int] | None:
    """Character range of extracted code inside the decoded completion, searched after any thought
    block first and then anywhere (last occurrence)."""
    if not code:
        return None
    start = thought_end(decoded)
    for cand in (code, code.strip()):
        if not cand:
            continue
        i = decoded.find(cand, start)
        if i < 0:
            i = decoded.rfind(cand)
        if i >= 0:
            return (i, i + len(cand))
    return None


def strip_range(text: str, cs: int, ce: int) -> tuple[int, int] | None:
    while cs < ce and text[cs].isspace():
        cs += 1
    while ce > cs and text[ce - 1].isspace():
        ce -= 1
    return (cs, ce) if ce > cs else None


class _CumChars:
    """Characters of decode(ids[:i]) with an incomplete trailing multi-byte sequence removed."""

    def __init__(self, tokenizer: Any, ids: Sequence[int]):
        self.tokenizer, self.ids, self.memo = tokenizer, [int(i) for i in ids], {0: 0}

    def __call__(self, i: int) -> int:
        if i not in self.memo:
            self.memo[i] = len(decode_ids(self.tokenizer, self.ids[:i]).rstrip("�"))
        return self.memo[i]


def char_span_to_token_span(tokenizer: Any, ids: Sequence[int], cs: int, ce: int) -> tuple[int, int] | None:
    """[i0, j) tokens overlapping the character range [cs, ce) of decode(ids). Binary search over prefix
    decodes; ids are never re-tokenized."""
    n = len(ids)
    cum = _CumChars(tokenizer, ids)
    if n == 0 or ce <= cs or cum(n) <= cs:
        return None
    lo, hi = 0, n - 1                       # smallest i with cum(i + 1) > cs
    while lo < hi:
        mid = (lo + hi) // 2
        if cum(mid + 1) > cs:
            hi = mid
        else:
            lo = mid + 1
    i0 = lo
    lo, hi = i0 + 1, n                      # smallest j with cum(j) >= ce
    while lo < hi:
        mid = (lo + hi) // 2
        if cum(mid) >= ce:
            hi = mid
        else:
            lo = mid + 1
    return (i0, lo)


def align_ids_to_text(tokenizer: Any, ids: Sequence[int], text: str) -> list[int]:
    """Drop trailing tokens that lie beyond text (for stop strings that the engine cut from the text
    but not from the ids). A token straddling the cut is dropped as well."""
    cum = _CumChars(tokenizer, ids)
    n = len(ids)
    lo, hi = 0, n                           # largest i with cum(i) <= len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cum(mid) <= len(text):
            lo = mid
        else:
            hi = mid - 1
    return [int(i) for i in ids[:lo]]


def extract_fallback(sample_uid: str, completion_text: str, entry_point: str | None, truncated: bool,
                     use_execute: bool = True) -> tuple[str | None, str | None]:
    """(code, failure) when no extraction table row exists: pipeline.execute.extract.extract_code if it
    is importable, else the first fenced block after any thought block."""
    if use_execute:
        try:
            from pipeline.execute.extract import extract_code  # type: ignore[import-not-found]
            r = extract_code(sample_uid, completion_text, entry_point, truncated)
            return r.code, r.failure
        except Exception:  # not importable yet, or it raised: use the local locator
            pass
    rng = first_fenced_interior(completion_text, thought_end(completion_text))
    if rng is None:
        return None, "no_block"
    code = completion_text[rng[0]:rng[1]]
    return (code, None) if code.strip() else (None, "empty_output")
