"""Extraction on hand-written completion strings."""

import pytest

from pipeline.contracts import constants
from pipeline.execute.extract import (
    BASE_STOP_STRINGS, THOUGHT_MARKERS, extract_code, normalize_code, strip_leading_thought,
)

UID = "P1|frozen|humaneval_plus|HumanEval/53|1"
GOOD = "def add(x: int, y: int):\n    return x + y\n"


def ex(text, entry="add", truncated=False, **kw):
    return extract_code(kw.pop("uid", UID), text, entry, truncated, **kw)


def test_failure_codes_are_the_contract_codes():
    codes = {ex("").failure, ex("prose only").failure, ex("```python\ndef add(:\n```").failure,
             ex("```python\ndef other(): pass\n```").failure, ex("x", truncated=True).failure}
    assert codes == set(constants.EXTRACTION_FAILURE_CODES)


@pytest.mark.parametrize("fence", ["```python", "```Python", "```py", "```python3", "```"])
def test_fenced_variants(fence):
    r = ex(f"Here you go:\n{fence}\n{GOOD}```\nDone.")
    assert r.failure is None and r.method == "fenced" and r.code.strip() == GOOD.strip()


def test_tilde_and_long_fences_and_indent():
    assert ex(f"~~~python\n{GOOD}~~~").method == "fenced"
    assert ex(f"````python\n{GOOD}````").method == "fenced"
    assert ex(f"  ```python\n{GOOD}  ```").failure is None


def test_first_python_block_wins_and_other_languages_are_skipped():
    text = f"```bash\npip install x\n```\n```python\n{GOOD}```\n```python\ndef add(x, y):\n    return 0\n```"
    r = ex(text)
    assert r.code.strip() == GOOD.strip()


def test_untagged_non_python_block_is_skipped():
    text = f"```\n$ ls -la\ntotal 0\n```\n```\n{GOOD}```"
    assert ex(text).code.strip() == GOOD.strip()


def test_unclosed_fence_takes_the_rest():
    assert ex(f"```python\n{GOOD}").failure is None


def test_fallback_from_first_def():
    r = ex(f"Sure!\n{GOOD}")
    assert r.method == "fallback_def" and r.code.startswith("def add")
    r = ex("Note.\nclass Foo:\n    pass\ndef add(x, y):\n    return x + y\n")
    assert r.code.startswith("class Foo")


def test_no_block():
    r = ex("I cannot help with that.")
    assert (r.failure, r.code, r.method) == ("no_block", None, None)


def test_empty_output():
    assert ex("").failure == "empty_output"
    assert ex("  \n\t\n").failure == "empty_output"
    assert ex("```python\n```").failure == "empty_output"
    assert ex("<think>\n\n</think>\n\n").failure == "empty_output"


def test_syntax_error():
    assert ex("```python\ndef add(x, y:\n    return x\n```").failure == "syntax_error"


def test_missing_entry_point():
    assert ex("```python\ndef plus(x, y):\n    return x + y\n```").failure == "missing_entry_point"
    # a method of a class is not a top-level function
    assert ex("```python\nclass A:\n    def add(self, x, y):\n        return x + y\n```").failure == "missing_entry_point"
    assert ex("```python\nadd = lambda x, y: x + y\n```").failure == "missing_entry_point"


def test_async_def_counts_as_definition():
    assert ex("```python\nasync def add(x, y):\n    return x + y\n```").failure is None


def test_truncated_takes_precedence_and_keeps_no_code():
    r = ex(f"```python\n{GOOD}```", truncated=True)
    assert (r.failure, r.code) == ("truncated", None)


def test_lcb_functional_needs_class_solution_method():
    uid = "P1|frozen|lcb_v6|lcb/abc|1"
    ok = "```python\nclass Solution:\n    def twoSum(self, a, b):\n        return a + b\n```"
    assert extract_code(uid, ok, "twoSum", False).failure is None
    assert extract_code(uid, "```python\ndef twoSum(a, b):\n    return a + b\n```", "twoSum", False).failure == \
        "missing_entry_point"
    assert extract_code(uid, ok, "other", False).failure == "missing_entry_point"


def test_lcb_stdin_has_no_entry_point_check():
    uid = "P1|frozen|lcb_v6|lcb/abc|1"
    r = extract_code(uid, "```python\nprint(int(input()) * 2)\n```", None, False)
    assert r.failure is None and r.method == "fenced"
    assert extract_code(uid, "print(1)", None, False).failure == "no_block"


# ---- thought blocks ------------------------------------------------------------------------------
def test_marker_list_is_explicit():
    assert ("<think>", "</think>", False) in THOUGHT_MARKERS
    assert all(len(m) == 3 for m in THOUGHT_MARKERS)


@pytest.mark.parametrize("prefix", ["<think>\n\n</think>\n\n", "<think></think>", "\n<think>\n</think>\n",
                                    "<|channel>thought\n<channel|>", "<start_of_thought><end_of_thought>"])
def test_empty_thought_block_is_stripped(prefix):
    r = ex(prefix + f"```python\n{GOOD}```")
    assert r.failure is None and r.code.strip() == GOOD.strip()


def test_nonempty_think_block_does_not_leak_its_code():
    text = "<think>\nMaybe:\n```python\ndef add(x, y):\n    return 0\n```\n</think>\n" + f"```python\n{GOOD}```"
    assert ex(text).code.strip() == GOOD.strip()


def test_gemma_nonempty_thought_is_left_alone():
    s = "<|channel>thought\nreasoning\n<channel|>answer"
    assert strip_leading_thought(s) == s


def test_thought_marker_in_the_middle_is_not_touched():
    text = f"```python\n{GOOD}```\n<think></think>"
    assert ex(text).failure is None


# ---- completion mode -----------------------------------------------------------------------------
PROMPT = 'def add(x: int, y: int):\n    """Add two numbers."""\n'


def test_stop_strings_constant():
    assert BASE_STOP_STRINGS == ("\ndef ", "\nclass ", "\nif __name__", "\nprint(", "\n#")


@pytest.mark.parametrize("stop", BASE_STOP_STRINGS)
def test_completion_cut_at_each_stop_string(stop):
    comp = "    return x + y\n" + stop[1:] + "junk(\n"
    r = ex(comp, mode="completion", prompt=PROMPT)
    assert r.failure is None and r.method == "completion"
    assert r.code == PROMPT + "    return x + y"


def test_completion_cut_at_the_earliest_stop():
    comp = "    return x + y\n\n# note\ndef other():\n    pass\n"
    assert ex(comp, mode="completion", prompt=PROMPT).code == PROMPT + "    return x + y\n"


def test_completion_ignores_stop_strings_inside_the_prompt():
    prompt = "def helper():\n    pass\n\ndef add(x, y):\n    '''doc'''\n"
    r = extract_code(UID, "    return x + y\n", "add", False, mode="completion", prompt=prompt)
    assert r.code == prompt + "    return x + y\n"


def test_completion_starting_a_new_def_has_no_body():
    r = ex("def other():\n    pass\n", mode="completion", prompt=PROMPT)
    assert r.failure == "empty_output"


def test_completion_empty_and_syntax_and_entry_point():
    assert ex("  \n", mode="completion", prompt=PROMPT).failure == "empty_output"
    assert ex("    return (x +\n", mode="completion", prompt=PROMPT).failure == "syntax_error"
    assert extract_code(UID, "    return x\n", "missing", False, mode="completion", prompt=PROMPT).failure == \
        "missing_entry_point"


def test_completion_truncated_rules():
    # no stop string seen: the function may be cut mid-way
    assert ex("    return x +", truncated=True, mode="completion", prompt=PROMPT).failure == "truncated"
    # a stop string was reached before the cap: the function is complete (stated divergence)
    r = ex("    return x + y\n\ndef f():\n    pass", truncated=True, mode="completion", prompt=PROMPT)
    assert r.failure is None


def test_completion_needs_prompt():
    with pytest.raises(ValueError):
        ex("    return 1", mode="completion")
    with pytest.raises(ValueError):
        ex("x", mode="bogus")


# ---- normalize_code ------------------------------------------------------------------------------
def test_normalize_code_removes_formatting_and_comments():
    a = "def f(x):\n    # note\n    return (x+1)\n"
    b = "def f( x ):\n\n    return x + 1  # other\n"
    assert normalize_code(a) == normalize_code(b) == "def f(x):\n    return x + 1"


def test_normalize_code_keeps_unparsable_text_raw():
    raw = "def f(:\n  ???"
    assert normalize_code(raw) == raw
    assert normalize_code("a = 1\x00") == "a = 1\x00"


def test_normalize_code_distinguishes_different_programs():
    assert normalize_code("x = 1") != normalize_code("x = 2")
