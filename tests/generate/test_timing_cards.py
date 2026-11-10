import json
from pathlib import Path

import pytest

from pipeline.generate import cards as CD
from pipeline.generate import prompts as P
from pipeline.generate import stage as S
from pipeline.generate import tokens as K

import gen_tinylm as T
from test_stage import _cfg, _setup

META = Path(__file__).resolve().parents[2] / ".hf-cache" / "meta"


# ---- G10: timing-only jobs ---------------------------------------------------------------------------
def _timing_cfg(**kw):
    return _cfg(k=2, extra={"timing_only": True}, **kw)


def test_timing_generate_writes_only_the_timing_set(tmp_path):
    layout, probs, man = _setup(tmp_path)
    rep = S.run_generate(_timing_cfg(models=("S1",)), layout, man)
    base = layout.root / "generations/S1/humaneval_plus"
    assert [p.name for p in base.iterdir()] == ["timing"] and list((base / "timing").glob("shard-*.parquet"))
    assert not (base / "frozen").exists() and not (layout.root / "capture").exists()
    assert not (layout.root / "config/prompts.json").exists()
    m = rep.metrics["S1/humaneval_plus/timing"]
    assert m["tokens_per_second"] > 0 and m["mean_generated_tokens"] > 0 and m["mean_thinking_tokens"] == 0
    t = json.loads((layout.logs / "timing_S1.json").read_text())
    assert t["generate"]["thinking"] is True and t["generate"]["benchmarks"]["humaneval_plus"]["samples"] == 6
    # always re-run, never skipped
    rep2 = S.run_generate(_timing_cfg(models=("S1",)), layout, man)
    assert rep2.outputs and not rep2.skipped


def test_timing_capture_ignores_generation_only_and_stores_nothing(tmp_path):
    layout, probs, man = _setup(tmp_path)
    cfg = _timing_cfg(models=("P4",), generation_only_models=("P4",))
    S.run_generate(cfg, layout, man)
    rep = S.run_capture(cfg, layout, man)
    assert not rep.outputs and not any("generation only" in n for n in rep.notes)
    assert rep.metrics["P4/humaneval_plus/timing"]["tokens_per_second"] > 0
    assert not (layout.root / "capture").exists() and not (layout.root / "config/answer_tokens.json").exists()
    t = json.loads((layout.logs / "timing_P4.json").read_text())
    assert set(t) == {"model_key", "generate", "capture"}
    assert not list(layout.root.rglob("*.safetensors"))


def test_normal_capture_never_picks_up_timing_shards(tmp_path):
    layout, probs, man = _setup(tmp_path)
    S.run_generate(_timing_cfg(), layout, man)
    rep = S.run_capture(_cfg(k=2), layout, man)
    assert not rep.outputs and not (layout.root / "capture").exists()


def test_thinking_tokens_counts_through_the_end_marker():
    tok = T.build_tokenizer()
    text = "<think>\nhmm\n</think>\nanswer"
    ids = tok(text, add_special_tokens=False)["input_ids"]
    rec = T.make_record(tok, T.problem(), text, ids=ids)
    want = len(tok("<think>\nhmm\n</think>", add_special_tokens=False)["input_ids"])
    assert S.thinking_tokens(rec, tok) == want
    assert S.thinking_tokens(T.make_record(tok, T.problem(), "no thought"), tok) == 0


# ---- G21: Gemma 4 thought markers ----------------------------------------------------------------------
GEMMA = META / "google_gemma-4-12B-it"


@pytest.mark.skipif(not (GEMMA / "chat_template.jinja").exists(), reason="chat template not cached")
def test_gemma_template_renders_empty_thought_block_in_the_prompt():
    import jinja2.sandbox
    env = jinja2.sandbox.ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
    cfg = json.loads((GEMMA / "tokenizer_config.json").read_text())
    tpl = env.from_string((GEMMA / "chat_template.jinja").read_text())
    msgs = [{"role": "user", "content": "UQ"}, {"role": "assistant", "content": "AA"}, {"role": "user", "content": "V2"}]
    off = tpl.render(messages=msgs[:1], add_generation_prompt=True, enable_thinking=False, bos_token=cfg["bos_token"])
    assert off == "<bos><|turn>user\nUQ<turn|>\n<|turn>model\n<|channel>thought\n<channel|>"
    on = tpl.render(messages=msgs[:1], add_generation_prompt=True, enable_thinking=True, bos_token=cfg["bos_token"])
    assert on.endswith("<|turn>user\nUQ<turn|>\n<|turn>model\n") and "<|think|>" in on
    full = tpl.render(messages=msgs, add_generation_prompt=True, enable_thinking=False, bos_token=cfg["bos_token"])
    assert full.endswith("<|turn>model\nAA<turn|>\n<|turn>user\nV2<turn|>\n<|turn>model\n<|channel>thought\n<channel|>")
    assert (cfg["soc_token"], cfg["eoc_token"], cfg["eot_token"]) == ("<|channel>", "<channel|>", "<turn|>")


def test_thought_end_handles_gemma_channel_markers():
    text = "<|channel>thought\nplan:\n```python\nx = 1\n```\n<channel|>```python\ndef f():\n    return 1\n```"
    s, e = K.locate_code(text, "def f():\n    return 1")
    assert s > text.index("<channel|>")
    assert K.thought_end(text) == text.index("<channel|>") + len("<channel|>")


# ---- G22: card recommendations ---------------------------------------------------------------------------
def test_tracked_card_recommendations():
    d = CD.load_tracked()["models"]
    assert set(d) == {"P1", "P2", "P3", "P4", "P5", "P6", "S1"}
    assert d["P1"]["generation_config"]["temperature"] == 0.6 and d["P1"]["generation_config"]["top_k"] == 20
    assert d["P5"]["generation_config"]["top_k"] == 64 and d["P5"]["generation_config"]["top_p"] == 0.95
    assert d["P3"]["generation_config"]["temperature"] == 0.6 and "top_k" not in d["P3"]["generation_config"]
    assert d["S1"]["repository"] == d["P1"]["repository"] and d["P4"]["readme_quotes"] == []
    assert any("Temperature=0.7" in q["text"] for q in d["P2"]["readme_quotes"])
    assert all(len(e["sha256"]) == 64 for m in d.values() for e in m["source_files"])
    files = {e["file"] for e in d["P6"]["source_files"]}
    assert "README.md" in files and "chat_template.jinja" in files


@pytest.mark.skipif(not META.exists(), reason="metadata cache absent")
def test_tracked_file_matches_the_cache():
    assert CD.build_card_recommendations(META) == CD.load_tracked()


def test_card_recommendations_written_to_prompts_json(tmp_path):
    layout, probs, man = _setup(tmp_path)
    S.run_generate(_cfg(models=("P1", "P5"), k=1), layout, man)
    cfg = json.loads((layout.root / "config/prompts.json").read_text())
    rec = cfg["card_recommendations_not_used"]
    assert set(rec) == {"P1", "P5"} and rec["P5"]["generation_config"]["top_k"] == 64


def test_base_stop_strings_are_shared_with_execute():
    from pipeline.execute.extract import BASE_STOP_STRINGS as theirs
    assert P.BASE_STOP_STRINGS == theirs
