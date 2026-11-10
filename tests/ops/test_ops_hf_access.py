from pathlib import Path

from ops import hf_access
from ops.plans import model_repo

REPO, REV = model_repo("P1")
BASE = "https://hub.test"


class Resp:
    def __init__(self, status, js=None):
        self.status_code, self._js = status, js or {}

    def json(self):
        return self._js


class Session:
    """Maps URL suffix to (status, json); records calls and headers."""

    def __init__(self, routes):
        self.routes, self.calls = routes, []

    def get(self, url, headers=None, timeout=None, allow_redirects=True):
        self.calls.append((url, dict(headers or {})))
        for suffix, (st, js) in self.routes.items():
            if url.endswith(suffix):
                return Resp(st, js)
        return Resp(500)


REVISION = f"/api/models/{REPO}/revision/{REV}"
BARE = f"/api/models/{REPO}"
FILE = f"/{REPO}/resolve/{REV}/config.json"


def test_open_repo():
    r = hf_access.check_model("P1", Session({REVISION: (200, {"gated": False, "sha": REV})}), None, BASE)
    assert r.ok and "open" in r.message


def test_gated_without_access():
    s = Session({REVISION: (200, {"gated": "auto", "sha": REV}), FILE: (403, {})})
    r = hf_access.check_model("P1", s, None, BASE)
    assert not r.ok and "P1" in r.message and REPO in r.message
    assert "HF_TOKEN" in r.message and "licence" in r.message
    r2 = hf_access.check_model("P1", Session({REVISION: (200, {"gated": "manual"}), FILE: (401, {})}), "hf_tok", BASE)
    assert not r2.ok and "accept the licence" in r2.message


def test_gated_with_access():
    s = Session({REVISION: (200, {"gated": "auto", "sha": REV}), FILE: (302, {})})
    r = hf_access.check_model("P1", s, "hf_tokenvalue", BASE)
    assert r.ok and "access granted" in r.message
    assert any(h.get("Authorization") == "Bearer hf_tokenvalue" for _, h in s.calls)
    assert "hf_tokenvalue" not in r.message


def test_repo_404():
    s = Session({REVISION: (404, {}), BARE: (404, {})})
    r = hf_access.check_model("P1", s, None, BASE)
    assert not r.ok and "repository not found" in r.message and "P1" in r.message


def test_revision_missing():
    s = Session({REVISION: (404, {}), BARE: (200, {"gated": False})})
    r = hf_access.check_model("P1", s, None, BASE)
    assert not r.ok and "revision is absent" in r.message and REV[:8] in r.message


def test_unauthorized_names_the_action():
    r = hf_access.check_model("P1", Session({REVISION: (401, {})}), None, BASE)
    assert not r.ok and "HF_TOKEN" in r.message


def test_wrong_sha_rejected():
    r = hf_access.check_model("P1", Session({REVISION: (200, {"gated": False, "sha": "f" * 40})}), None, BASE)
    assert not r.ok and "different commit" in r.message


def test_check_models_fails_fast_and_dedupes():
    s = Session({REVISION: (401, {})})
    res = hf_access.check_models(["P1", "P2"], s, None, BASE)
    assert len(res) == 1 and not res[0].ok
    s2 = Session({"": (200, {"gated": False})})
    res2 = hf_access.check_models(["P1", "S1"], s2, None, BASE)     # S1 is the same repo and revision as P1
    assert len(res2) == 1


def test_fetch_sequence_markers_disk_and_dry_run(tmp_path):
    sizes = {"siblings": [{"size": 10 * 10**9}, {"size": 5 * 10**9}]}
    s = Session({"?blobs=true": (200, sizes)})
    out, got = [], []
    kw = dict(hf_home=tmp_path / "hf", state_dir=tmp_path / "st", session=s, token=None, out=out.append,
              downloader=lambda repo, rev, home, tok: got.append(repo), base=BASE)
    assert hf_access.fetch_models(["P1", "S1", "P2"], free_fn=lambda p: 10**12, **kw)
    assert got == [model_repo("P1")[0], model_repo("P2")[0]]               # sequential, deduplicated
    got.clear()
    assert hf_access.fetch_models(["P1", "P2"], free_fn=lambda p: 10**12, **kw) and got == []   # markers skip
    assert any("[skip]" in o for o in out)
    out.clear()
    kw["state_dir"] = tmp_path / "st2"
    assert not hf_access.fetch_models(["P1"], free_fn=lambda p: 10 * 10**9, **kw)              # 15 GB x 1.1 needed
    assert got == [] and "GB free" in out[-1]
    out.clear()
    assert hf_access.fetch_models(["P1"], dry_run=True, **{**kw, "session": None}) and "[dry-run]" in out[0]
    assert not (tmp_path / "st2" / "x").exists() and got == []


def test_download_failure_keeps_no_marker_and_hides_token(tmp_path):
    def bad(repo, rev, home, tok):
        raise RuntimeError(f"auth failed for {tok}")
    out = []
    s = Session({"?blobs=true": (200, {"siblings": [{"size": 1}]})})
    ok = hf_access.fetch_models(["P1"], hf_home=tmp_path, state_dir=tmp_path / "st", session=s, token="hf_SECRETVALUE9",
                                out=out.append, downloader=bad, free_fn=lambda p: 10**12, base=BASE)
    assert not ok and "SECRETVALUE" not in "\n".join(out) and not list((tmp_path / "st").glob("*.done"))


def test_main_dry_run_makes_no_session_call(capsys):
    class Boom:
        def get(self, *a, **k):
            raise AssertionError("network call in dry run")
    assert hf_access.main(["fetch", "--plan", "pilot", "--dry-run"], session=Boom()) == 0
    o = capsys.readouterr().out
    assert "[dry-run]" in o and "T1" in o


def test_main_check_reports_failure_code(capsys, monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.setattr(hf_access._env, "get_env", lambda *a, **k: None)
    assert hf_access.main(["check", "--models", "P1", "--base-url", BASE], session=Session({REVISION: (401, {})})) == 2
    assert "HF_TOKEN" in capsys.readouterr().out
