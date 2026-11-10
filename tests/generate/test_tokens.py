import pytest

from pipeline.generate import tokens as K
from pipeline.generate.prompts import apply_chat
from pipeline.contracts import constants as C

import gen_tinylm as T

V2_TURN = f"<|im_start|>user\n{C.V2_TEXT}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


@pytest.mark.parametrize("template", [T.T_PLAIN, T.T_REWRITE, T.T_SYSTEM])
def test_elicitation_turn_from_template(prompts, template):
    tok = T.build_tokenizer(template)
    spec = K.derive_turns(tok, prompts, chat=True)
    assert spec.eot_text == "<|im_end|>" and spec.eot_id == tok.convert_tokens_to_ids("<|im_end|>")
    assert spec.bridge_text == "\n" and len(spec.bridge_ids) == 1
    # starts at the first token of the user header, ends with the assistant header (thinking off)
    assert spec.elicitation_text["V2"] == V2_TURN
    assert tok.decode(spec.elicitation_ids["V2"]) == V2_TURN
    assert tok.convert_ids_to_tokens(spec.elicitation_ids["V2"][0]) == "<|im_start|>"
    assert spec.elicitation_text["V1"] == V2_TURN.replace(C.V2_TEXT, C.V1_TEXT)
    assert not spec.prefix_identity        # these templates add a thought block to the prompt only
    d = spec.describe(tok)
    assert d["first_span_token"] == "<|im_start|>" and d["elicitation_n_tokens"]["V2"] == len(spec.elicitation_ids["V2"])


def test_stable_template_has_prefix_identity_and_rewriting_is_flagged(prompts):
    stable = K.derive_turns(T.build_tokenizer(T.T_STABLE), prompts, chat=True)
    rew = K.derive_turns(T.build_tokenizer(T.T_REWRITE), prompts, chat=True)
    assert stable.prefix_identity and not stable.notes
    assert stable.elicitation_text["V2"] == V2_TURN.replace("<think>\n\n</think>\n\n", "")
    assert not rew.prefix_identity and any("rewrites" in n for n in rew.notes)


def test_base_turn_is_the_plain_text_frame(prompts):
    tok = T.build_tokenizer()
    spec = K.derive_turns(tok, prompts, chat=False)
    assert tok.decode(spec.elicitation_ids["V2"]) == f"\n\nQuestion: {C.V2_TEXT}\nAnswer:"
    assert spec.bridge_ids == () and spec.eot_id is None


def test_answer_token_variant_rule():
    tok = T.build_tokenizer()
    v = K.answer_token_variants(tok)
    yes = {d["token"] for d in v["yes"]}
    no = {d["token"] for d in v["no"]}
    assert yes == {" Yes", "Yes"}                         # not yes, YES, Yes!
    assert no == {" No", "No", "\nNo"} or no == {" No", "No", "ĊNo"}   # leading whitespace is stripped; not no, Nope
    assert all(d["text"].lstrip() in ("Yes", "No") for d in v["yes"] + v["no"])
    with pytest.raises(ValueError):
        K.answer_token_variants(T.build_tokenizer(words=[" No"]))


def test_code_span_mapping_excludes_fences():
    tok = T.build_tokenizer()
    ids = tok(T.GOOD, add_special_tokens=False)["input_ids"]
    decoded = K.decode_ids(tok, ids)
    code = "def add(a, b):\n    return a + b\n"
    loc = K.locate_code(decoded, code)
    rng = K.strip_range(decoded, *loc)
    i0, j = K.char_span_to_token_span(tok, ids, *rng)
    assert K.decode_ids(tok, ids[i0:j]) == "def add(a, b):\n    return a + b"
    assert j - i0 == len("def add(a, b):\n    return a + b")


def test_code_span_with_multibyte_characters():
    tok = T.build_tokenizer()
    text = "Ok\n```python\ns = 'é→'\nprint(s)\n```"
    ids = tok(text, add_special_tokens=False)["input_ids"]
    decoded = K.decode_ids(tok, ids)
    assert decoded == text
    code = "s = 'é→'\nprint(s)"
    rng = K.strip_range(decoded, *K.locate_code(decoded, code))
    i0, j = K.char_span_to_token_span(tok, ids, *rng)
    assert K.decode_ids(tok, ids[i0:j]) == code
    assert j - i0 > len(code)                                # é and → are several byte tokens


def test_code_inside_thought_block_is_skipped():
    text = "<think>\n```python\ndef f(): return 1\n```\n</think>\n```python\ndef f(): return 1\n```"
    tok = T.build_tokenizer()
    ids = tok(text, add_special_tokens=False)["input_ids"]
    decoded = K.decode_ids(tok, ids)
    s, e = K.locate_code(decoded, "def f(): return 1")
    assert s > decoded.index("</think>")
    assert K.first_fenced_interior(decoded, K.thought_end(decoded)) is not None


def test_align_ids_to_text_drops_stop_string_tokens():
    tok = T.build_tokenizer()
    ids = tok("return x\ndef g():", add_special_tokens=False)["input_ids"]
    assert K.align_ids_to_text(tok, ids, "return x") == ids[:len("return x")]
    assert K.align_ids_to_text(tok, ids, K.decode_ids(tok, ids)) == ids


def test_extract_fallback_first_fence_after_thought():
    code, fail = K.extract_fallback("u", "x\n```python\nA=1\n```\n```python\nB=2\n```", "A", False, use_execute=False)
    assert fail is None and code.strip() == "A=1"
    assert K.extract_fallback("u", "no code here", "A", False, use_execute=False) == (None, "no_block")
