"""Model-card sampling recommendations, recorded and not used (design section 5, G22).

The frozen generations use temperature 1.0, top-p 1.0, no top-k for every model. The recommendations of
each card are copied here from the pinned revisions' generation_config.json and README.md, with the
README line number and the verbatim line, so the paper can state exactly what was set aside.

build_card_recommendations() reads a local metadata cache (default .hf-cache/meta/<repo with / as _>/,
git-ignored) and is run by hand; the result is the tracked file card_recommendations.json, which the
generate stage copies into config/prompts.json under "card_recommendations_not_used". The stage itself
never touches the network.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from pipeline.contracts import constants as C
from pipeline.contracts.hashing import sha256_file

TRACKED = Path(__file__).with_name("card_recommendations.json")
META_FILES = ("tokenizer_config.json", "chat_template.jinja", "generation_config.json", "README.md")
SAMPLING_KEYS = ("temperature", "top_p", "top_k", "min_p", "repetition_penalty", "presence_penalty", "do_sample",
                 "max_new_tokens", "eos_token_id")
# README lines that state sampling settings (1-based line numbers at the pinned revision). Each is
# checked against its keywords when the table is built, so a wrong number fails loudly.
README_LINES: Mapping[str, tuple[int, ...]] = {
    "google/gemma-4-12B-it": (370, 371, 372),
    "google/gemma-4-31B-it": (366, 367, 368),
    "Qwen/Qwen3-8B": (129, 148, 327, 328, 329),
    "Qwen/Qwen3-14B": (129, 148, 327, 328, 329),
    "allenai/Olmo-3-7B-Instruct": (172, 173),
    "allenai/Olmo-3.1-32B-Instruct": (),     # the README states no sampling settings
}
KEYWORDS = ("temperature", "top_p", "topp", "top_k", "topk", "presence_penalty")


def meta_dir(root: Path, repo: str) -> Path:
    return Path(root) / repo.replace("/", "_")


def build_card_recommendations(root: Path, keys: tuple[str, ...] = ("P1", "P2", "P3", "P4", "P5", "P6", "S1")) -> dict[str, Any]:
    out: dict[str, Any] = {"note": "Recorded for the paper and not used: frozen generations use temperature 1.0, "
                                   "top-p 1.0, no top-k, no repetition penalty (design section 5).",
                           "models": {}}
    for key in keys:
        repo, rev = C.MODELS[key][:2]
        d = meta_dir(root, repo)
        gen = json.loads((d / "generation_config.json").read_text())
        lines = (d / "README.md").read_text().splitlines()
        quotes = []
        for n in README_LINES[repo]:
            text = lines[n - 1]
            if not any(k in text.lower() for k in KEYWORDS):
                raise ValueError(f"{repo} README line {n} does not state a sampling setting: {text!r}")
            quotes.append({"line": n, "text": text})
        out["models"][key] = {
            "repository": repo, "revision": rev,
            "generation_config": {k: gen[k] for k in SAMPLING_KEYS if k in gen},
            "readme_quotes": quotes,
            "source_files": [{"file": f, "sha256": sha256_file(d / f)} for f in META_FILES if (d / f).exists()],
        }
    return out


def load_tracked() -> dict[str, Any]:
    return json.loads(TRACKED.read_text())


if __name__ == "__main__":      # python -m pipeline.generate.cards [meta_root]
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".hf-cache/meta")
    TRACKED.write_text(json.dumps(build_card_recommendations(root), indent=1, sort_keys=True) + "\n")
