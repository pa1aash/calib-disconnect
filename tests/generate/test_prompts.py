import json
import shutil
from pathlib import Path

import pytest

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sha256_text
from pipeline.contracts.schemas import Problem
from pipeline.generate import prompts as P

import gen_tinylm as T

REAL = P.PROMPT_DIR


def _copy(tmp_path: Path) -> Path:
    d = tmp_path / "prompts"
    shutil.copytree(REAL, d)
    return d


def test_real_prompts_load_and_match_constants(prompts):
    assert prompts.elicit_text("V1") == C.V1_TEXT and prompts.elicit_text("V2") == C.V2_TEXT
    rec = json.loads((REAL / P.HASH_FILE).read_text())["files"]
    assert dict(prompts.file_sha256) == rec


def test_tampered_prompt_is_refused(tmp_path):
    d = _copy(tmp_path)
    (d / "gen_chat.txt").write_text((d / "gen_chat.txt").read_text() + " ")
    with pytest.raises(P.PromptIntegrityError, match="gen_chat.txt"):
        P.load_prompts(d)


def test_elicit_text_must_equal_constants_even_if_hash_updated(tmp_path):
    d = _copy(tmp_path)
    new = C.V2_TEXT.replace("Yes or No", "yes or no")
    (d / "elicit_v2.txt").write_text(new)
    rec = json.loads((d / P.HASH_FILE).read_text())
    rec["files"]["elicit_v2.txt"] = sha256_text(new)
    (d / P.HASH_FILE).write_text(json.dumps(rec))
    with pytest.raises(P.PromptIntegrityError, match="V2_TEXT"):
        P.load_prompts(d)


def test_missing_and_unlisted_files_are_refused(tmp_path):
    d = _copy(tmp_path)
    (d / "extra.txt").write_text("x")
    with pytest.raises(P.PromptIntegrityError, match="extra"):
        P.load_prompts(d)
    d2 = _copy(tmp_path / "b")
    (d2 / "payload_function.txt").unlink()
    with pytest.raises(P.PromptIntegrityError, match="payload_function"):
        P.load_prompts(d2)


def _lcb(starter):
    return Problem("lcb/q1", "lcb_v6", "Given {x} and {y}, add them.", None, None, "function" if starter else "stdin",
                   "2025-05-01", starter_code=starter)


def test_payload_selection_and_braces_are_inert(prompts):
    he = T.problem()
    msg = prompts.generation_message(he)
    assert msg.startswith("Solve the following programming problem in Python.")
    assert "Complete the following Python function." in msg and he.prompt in msg and not msg.endswith("\n")
    f = prompts.generation_message(_lcb("class Solution:\n    def f(self, x: int) -> int:\n        pass"))
    assert "Complete the following starter code." in f and "Given {x} and {y}, add them." in f
    s = prompts.generation_message(_lcb(None))
    assert "Read the input from standard input" in s and "starter code" not in s
    # unfilled-template identity
    shas = {prompts.template_sha256_for_prompt("lcb_v6", m, base=False) for m in (f, s)}
    assert len(shas) == 2
    assert prompts.template_sha256_for_prompt("humaneval_plus", msg, base=False) == \
        prompts.template_sha256("payload_function.txt", base=False)


def test_base_prompts(prompts):
    he = T.problem()
    assert prompts.base_completion(he) == he.prompt
    frame = prompts.base_frame("PROGRAM", "V2")
    assert frame == f"PROGRAM\n\nQuestion: {C.V2_TEXT}\nAnswer:"
    assert prompts.base_frame(he.prompt + "    return 1\n", "V2").endswith(prompts.base_frame_suffix("V2"))
    with pytest.raises(ValueError):
        prompts.base_completion(_lcb(None))


def test_chat_rendering_thinking_flag_and_hashes(prompts):
    tok = T.build_tokenizer()
    off = P.render_generation_prompt(tok, "hello", thinking=False)
    on = P.render_generation_prompt(tok, "hello", thinking=True)
    assert off.text.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n")
    assert on.text.endswith("<|im_start|>assistant\n")
    assert off.sha256 == sha256_text(off.text) != on.sha256
    assert "system" not in off.text
    assert P.supports_thinking_flag(tok)
    assert P.chat_template_sha256(tok) == sha256_text(T.T_PLAIN)
    nothink = T.build_tokenizer("{% for m in messages %}[{{ m['role'] }}]{{ m['content'] }}{% endfor %}{% if add_generation_prompt %}[assistant]{% endif %}")
    assert not P.supports_thinking_flag(nothink)
    assert P.render_generation_prompt(nothink, "x", thinking=True).text == "[user]x[assistant]"
    base = P.render_prompt(tok, "def f():", chat=False, thinking=False)
    assert base.text == "def f():"
