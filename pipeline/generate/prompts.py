"""Frozen prompts: loading, hash verification, and rendering (design sections 5 and 10).

The files under pipeline/prompts/ are hashed in PROMPTS.sha256.json. Loading refuses on any mismatch,
on a missing file, and on an unlisted file. elicit_v1.txt and elicit_v2.txt must also equal the
verbatim strings in pipeline.contracts.constants.

Formatting rules (fixed here, recorded in the rendered-prompt hash):
    * Placeholders are substituted in one pass, so braces inside a problem statement or code are inert.
    * The generation user message has trailing newlines removed (the template files end with a newline
      that is an editor artifact; the elicitation files, which are compared byte for byte, have none).
    * prompt_sha256 of a GenerationRecord is the SHA-256 of the unfilled template text actually used:
      gen_chat.txt with the payload file substituted for {payload}, or base_completion_function.txt.
      config/prompts.json lists the component file hashes.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sha256_bytes, sha256_text
from pipeline.contracts.schemas import Problem

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"
HASH_FILE = "PROMPTS.sha256.json"
HASH_FORMAT = "calib-disconnect/prompts/v1"
FUNCTION_BENCHMARKS = ("humaneval_plus", "mbpp_plus")

# Stop strings for completion-style generation by base models (EvalPlus style: a new top-level
# definition, comment, decorator, print, conditional, or a closing fence ends the function body).
# Not verified against the installed evalplus source; recorded in config/prompts.json.
BASE_STOP_STRINGS: tuple[str, ...] = ("\nclass", "\ndef", "\n#", "\n@", "\nprint", "\nif", "\n```")
try:   # the execute module exports the tuple that generation must share (design section 10)
    from pipeline.execute.extract import BASE_STOP_STRINGS  # type: ignore[no-redef]
except ImportError:
    pass

_PLACEHOLDER = re.compile(r"\{(payload|prompt|statement|starter_code|program|question)\}")


class PromptIntegrityError(RuntimeError):
    """A prompt file is missing, unlisted, altered, or disagrees with the verbatim design text."""


def _fill(template: str, values: Mapping[str, str]) -> str:
    return _PLACEHOLDER.sub(lambda m: values[m.group(1)] if m.group(1) in values else m.group(0), template)


@dataclass(frozen=True)
class PromptSet:
    texts: Mapping[str, str]            # file name -> text
    file_sha256: Mapping[str, str]      # file name -> verified SHA-256
    directory: str = ""

    # ---- elicitation -------------------------------------------------------------------------
    def elicit_text(self, fmt: str) -> str:
        if fmt == "V1":
            return self.texts["elicit_v1.txt"]
        if fmt == "V2":
            return self.texts["elicit_v2.txt"]
        raise ValueError(f"unknown elicitation format {fmt!r}")

    # ---- generation --------------------------------------------------------------------------
    def payload_name(self, problem: Problem) -> str:
        if problem.benchmark in FUNCTION_BENCHMARKS:
            return "payload_function.txt"
        if problem.benchmark == "lcb_v6":
            return "payload_lcb_functional.txt" if problem.starter_code else "payload_lcb_stdin.txt"
        raise ValueError(f"unknown benchmark {problem.benchmark!r}")

    def generation_message(self, problem: Problem) -> str:
        """The user message of the generation prompt (before the chat template)."""
        name = self.payload_name(problem)
        payload = _fill(self.texts[name], {"prompt": problem.prompt, "statement": problem.prompt,
                                           "starter_code": problem.starter_code or ""})
        return _fill(self.texts["gen_chat.txt"], {"payload": payload}).rstrip("\n")

    def base_completion(self, problem: Problem) -> str:
        """Completion-style prompt for base models (section 10): the EvalPlus prompt itself."""
        if problem.benchmark not in FUNCTION_BENCHMARKS:
            raise ValueError("base-model completion prompts exist for function benchmarks only")
        return _fill(self.texts["base_completion_function.txt"], {"prompt": problem.prompt})

    def generation_prompt_text(self, problem: Problem, *, base: bool) -> str:
        return self.base_completion(problem) if base else self.generation_message(problem)

    def base_frame(self, program: str, fmt: str) -> str:
        return _fill(self.texts["base_elicitation_frame.txt"], {"program": program, "question": self.elicit_text(fmt)})

    def base_frame_suffix(self, fmt: str) -> str:
        """Frame text after the program: what is appended to prompt + completion for base models."""
        frame = self.texts["base_elicitation_frame.txt"]
        if not frame.startswith("{program}"):
            raise PromptIntegrityError("base_elicitation_frame.txt must start with {program}")
        return _fill(frame[len("{program}"):], {"question": self.elicit_text(fmt)})

    # ---- template identity -------------------------------------------------------------------
    def template_sha256(self, payload_name: str | None, *, base: bool) -> str:
        if base:
            return sha256_text(self.texts["base_completion_function.txt"])
        assert payload_name is not None
        return sha256_text(_fill(self.texts["gen_chat.txt"], {"payload": self.texts[payload_name]}))

    def template_sha256_for_prompt(self, benchmark: str, prompt_text: str, *, base: bool) -> str:
        """Identify which payload template produced prompt_text and return its template hash."""
        if base:
            return self.template_sha256(None, base=True)
        if benchmark in FUNCTION_BENCHMARKS:
            return self.template_sha256("payload_function.txt", base=False)
        if benchmark == "lcb_v6":
            lines = self.texts["payload_lcb_functional.txt"].splitlines()
            marker = next(ln for ln in lines if ln.strip() and "{" not in ln and not ln.startswith("```"))
            tail = marker
            name = "payload_lcb_functional.txt" if tail and tail in prompt_text else "payload_lcb_stdin.txt"
            return self.template_sha256(name, base=False)
        raise ValueError(f"unknown benchmark {benchmark!r}")

    def describe(self) -> dict[str, Any]:
        return {"format": HASH_FORMAT, "files": dict(sorted(self.file_sha256.items())),
                "base_stop_strings": list(BASE_STOP_STRINGS)}


def load_prompts(prompt_dir: str | Path | None = None) -> PromptSet:
    d = Path(prompt_dir) if prompt_dir is not None else PROMPT_DIR
    rec_path = d / HASH_FILE
    if not rec_path.exists():
        raise PromptIntegrityError(f"{rec_path} not found")
    rec = json.loads(rec_path.read_text())
    if rec.get("format") != HASH_FORMAT:
        raise PromptIntegrityError(f"unknown prompt hash format {rec.get('format')!r}")
    files: Mapping[str, str] = rec["files"]
    on_disk = {p.name for p in d.glob("*.txt")}
    if on_disk != set(files):
        raise PromptIntegrityError(f"prompt files differ from the record: extra={sorted(on_disk - set(files))} "
                                   f"missing={sorted(set(files) - on_disk)}")
    texts: dict[str, str] = {}
    for name, want in sorted(files.items()):
        raw = (d / name).read_bytes()
        have = sha256_bytes(raw)
        if have != want:
            raise PromptIntegrityError(f"{name}: SHA-256 {have[:12]}... differs from the recorded {want[:12]}...")
        texts[name] = raw.decode("utf-8")
    if texts["elicit_v1.txt"] != C.V1_TEXT:
        raise PromptIntegrityError("elicit_v1.txt differs from constants.V1_TEXT")
    if texts["elicit_v2.txt"] != C.V2_TEXT:
        raise PromptIntegrityError("elicit_v2.txt differs from constants.V2_TEXT")
    return PromptSet(texts=texts, file_sha256=dict(files), directory=str(d))


# ---------------------------------------------------------------------------------------------------
# Chat templates
# ---------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class RenderedPrompt:
    text: str
    sha256: str


def chat_template_string(tokenizer: Any) -> str:
    tpl = getattr(tokenizer, "chat_template", None)
    if isinstance(tpl, Mapping):
        tpl = tpl.get("default", next(iter(tpl.values()), ""))
    return tpl or ""


def chat_template_sha256(tokenizer: Any) -> str:
    """SHA-256 of the tokenizer's chat template string (recorded per model in config/prompts.json)."""
    return sha256_text(chat_template_string(tokenizer))


def supports_thinking_flag(tokenizer: Any) -> bool:
    return "enable_thinking" in chat_template_string(tokenizer)


def apply_chat(tokenizer: Any, messages: Sequence[Mapping[str, str]], *, add_generation_prompt: bool,
               thinking: bool) -> str:
    """Render messages through the tokenizer's chat template. enable_thinking is passed only when the
    template mentions it (False for thinking-off runs, True for thinking-on runs)."""
    kwargs: dict[str, Any] = {}
    if supports_thinking_flag(tokenizer):
        kwargs["enable_thinking"] = bool(thinking)
    out = tokenizer.apply_chat_template(list(messages), tokenize=False,
                                        add_generation_prompt=add_generation_prompt, **kwargs)
    if not isinstance(out, str):
        raise TypeError("apply_chat_template(tokenize=False) did not return text")
    return out


def render_generation_prompt(tokenizer: Any, user_message: str, *, thinking: bool) -> RenderedPrompt:
    """One user turn plus the assistant header, no system turn of our own."""
    text = apply_chat(tokenizer, [{"role": "user", "content": user_message}],
                      add_generation_prompt=True, thinking=thinking)
    return RenderedPrompt(text=text, sha256=sha256_text(text))


def render_prompt(tokenizer: Any, prompt_text: str, *, chat: bool, thinking: bool) -> RenderedPrompt:
    """Chat models: the chat template applied to prompt_text. Base models: prompt_text unchanged."""
    if chat:
        return render_generation_prompt(tokenizer, prompt_text, thinking=thinking)
    return RenderedPrompt(text=prompt_text, sha256=sha256_text(prompt_text))


def encode_prompt(tokenizer: Any, rendered: RenderedPrompt, *, chat: bool) -> list[int]:
    """Token ids of a rendered prompt. The chat template already contains its special tokens, so chat
    prompts are encoded without added special tokens; base prompts use the tokenizer's default."""
    ids = tokenizer(rendered.text, add_special_tokens=not chat)["input_ids"]
    return [int(i) for i in ids]
