from ops.env import get_env, parse_env_file
from ops.redact import redact, scrub


def test_redact_shows_at_most_four_chars():
    assert redact("abcdefghijkl") == "abcd..."
    assert redact("abcdefgh") == "abcd..."
    assert redact("abcdef") == "abc..."      # short values show fewer characters
    assert redact("ab") == "a..."
    assert redact("a") == "..."
    assert redact("") == "<unset>" and redact(None) == "<unset>"
    for s in ("x" * 40, "key-1234-5678", "22222"):
        r = redact(s)
        assert r.endswith("...") and len(r) <= 7 and s not in r


def test_scrub_replaces_known_secret_values():
    env = {"HF_TOKEN": "hf_supersecretvalue", "RUNPOD_API_KEY": "rpa_anothersecret"}
    text = "failed with hf_supersecretvalue and rpa_anothersecret in url"
    out = scrub(text, env)
    assert "supersecret" not in out and "anothersecret" not in out
    assert "hf_s..." in out and "rpa_..." in out


def test_env_file_parsed_without_leaking(tmp_path, capsys):
    f = tmp_path / ".env"
    f.write_text("# comment\nHF_TOKEN='hf_filevalue123'\nexport RUNPOD_API_KEY=\"rpa_filevalue456\"\nBAD LINE\n")
    d = parse_env_file(f)
    assert d == {"HF_TOKEN": "hf_filevalue123", "RUNPOD_API_KEY": "rpa_filevalue456"}
    assert get_env("HF_TOKEN", environ={}, env_file=f) == "hf_filevalue123"
    assert get_env("HF_TOKEN", environ={"HF_TOKEN": "fromenv"}, env_file=f) == "fromenv"
    assert get_env("NOPE", environ={}, env_file=f) is None
    assert get_env("HF_TOKEN", environ={}, env_file=tmp_path / "missing") is None
    assert capsys.readouterr().out == ""
