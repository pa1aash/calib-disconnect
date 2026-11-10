"""Build MANIFEST.json from the downloaded files (hashed here) and the LCB stream summaries.

Usage: python3 -I build_manifest.py BENCH_A2_DIR
Hashes local files with SHA-256; for LiveCodeBench shards (streamed, not stored)
it uses the stream summaries and cross-checks them against the Hugging Face LFS oids.
"""
import hashlib
import json
import sys
from pathlib import Path

LCB_REV = "0fe84c3912ea0c4d4a78037083943e8f0c4dd505"
HE_REV = "7dce6050a7d6d172f3cc5c32aa97f52fa1a2e544"
MBPP_HF_REV = "4bb6404fdc6cacfda99d4ac4205087b89d32030c"
MBPP_GH_COMMIT = "f82046ba5aabbbb427dbfd38a254d26bff08b533"
EVALPLUS_MASTER = "26d6d00bb1fd0fa37f39c99d5290da67891d1c5e"


def sha(p):
    b = Path(p).read_bytes()
    return len(b), hashlib.sha256(b).hexdigest()


def main():
    d = Path(sys.argv[1])
    c = d / "cache"
    entries = []

    def add(bench, role, url, revision, local, **kw):
        size, h = sha(local)
        e = {"benchmark": bench, "role": role, "url": url, "revision": revision,
             "bytes": size, "sha256": h}
        e.update(kw)
        entries.append(e)

    add("HumanEval", "pinned", f"https://huggingface.co/datasets/openai/openai_humaneval/resolve/{HE_REV}/openai_humaneval/test-00000-of-00001.parquet",
        {"hf_repo": "openai/openai_humaneval", "commit": HE_REV, "branch": "main"},
        c / "hf_humaneval/test-00000-of-00001.parquet", rows=164)

    he_tags = {"v0.1.10": "68cd26d53a0dec69f85eafe1f82a2a74155a2bd6", "v0.1.9": "1e96903185780a2659be407d0ecdc5650e3957e8"}
    for tag, commit in he_tags.items():
        for name in ["HumanEvalPlus", "HumanEvalPlus-Mini", "HumanEvalPlus-NoExtreme", "HumanEvalPlus-OriginFmt"]:
            add("HumanEval+", "pinned" if tag == "v0.1.10" else "reference_only",
                f"https://github.com/evalplus/humanevalplus_release/releases/download/{tag}/{name}.jsonl.gz",
                {"gh_repo": "evalplus/humanevalplus_release", "release_tag": tag, "tag_commit": commit},
                c / f"evalplus/heplus_{tag}/{name}.jsonl.gz", rows=164)
    mb_tags = {"v0.2.0": ("64fc4195b858a17cdfdb3324f0baf37939144e14", 378), "v0.1.0": ("3f0efe4ee7457d4718bd997c01697a1e9157e40c", 399)}
    for tag, (commit, n) in mb_tags.items():
        for name in ["MbppPlus", "MbppPlus-NoExtreme", "MbppPlus-OriginFmt"]:
            add("MBPP+", "pinned" if tag == "v0.2.0" else "reference_only",
                f"https://github.com/evalplus/mbppplus_release/releases/download/{tag}/{name}.jsonl.gz",
                {"gh_repo": "evalplus/mbppplus_release", "release_tag": tag, "tag_commit": commit},
                c / f"evalplus/mbppplus_{tag}/{name}.jsonl.gz", rows=n)
    add("MBPP+", "pinned_patch", f"https://github.com/evalplus/evalplus/blob/{EVALPLUS_MASTER}/tools/mbpp/fix_v020.py",
        {"gh_repo": "evalplus/evalplus", "commit": EVALPLUS_MASTER, "git_blob": "b35a229a36fc251b5ea8c8c21fe8bc821b2c73e2"},
        d / "raw/gh_evalplus_tools_mbpp_fix_v020.py",
        note="ground-truth fixes for Mbpp/459, Mbpp/102, Mbpp/559 (v0.2.0 -> unreleased v0.2.1)")
    add("MBPP (sanitized)", "pinned", f"https://github.com/google-research/google-research/blob/{MBPP_GH_COMMIT}/mbpp/sanitized-mbpp.json",
        {"gh_repo": "google-research/google-research", "commit": MBPP_GH_COMMIT, "git_blob": "a999d25df7e489e4c183cadfa5c0ecf557a702b6"},
        c / "gh_mbpp/sanitized-mbpp.json", rows=427)
    add("MBPP (full)", "reference_only", f"https://github.com/google-research/google-research/blob/{MBPP_GH_COMMIT}/mbpp/mbpp.jsonl",
        {"gh_repo": "google-research/google-research", "commit": MBPP_GH_COMMIT, "git_blob": "96e2dc2f7dd95b7b87b38dc46e42cbed444251bb"},
        c / "gh_mbpp/mbpp.jsonl", rows=974)
    for kind in ("sanitized", "full"):
        for s in ("prompt", "test", "train", "validation"):
            add(f"MBPP ({kind}, HF)", "reference_only",
                f"https://huggingface.co/datasets/google-research-datasets/mbpp/resolve/{MBPP_HF_REV}/{kind}/{s}-00000-of-00001.parquet",
                {"hf_repo": "google-research-datasets/mbpp", "commit": MBPP_HF_REV, "branch": "main"},
                c / f"hf_mbpp/{kind}-{s}.parquet")
    tree = {f["path"]: f for f in json.loads((d / "raw/hf_lcb_tree_main.json").read_text())}
    for s in ["test.jsonl", "test2.jsonl", "test3.jsonl", "test4.jsonl", "test5.jsonl", "test6.jsonl"]:
        summ = json.loads((c / f"lcb_index/{s[:-6]}.summary.json").read_text())
        lfs = tree[s]["lfs"]["oid"]
        assert summ["sha256"] == lfs and summ["bytes"] == tree[s]["size"], s
        entries.append({"benchmark": "LiveCodeBench code_generation_lite", "role": "pinned",
                        "url": f"https://huggingface.co/datasets/livecodebench/code_generation_lite/resolve/{LCB_REV}/{s}",
                        "revision": {"hf_repo": "livecodebench/code_generation_lite", "commit": LCB_REV, "branch": "main", "hf_tags": []},
                        "bytes": summ["bytes"], "sha256": summ["sha256"], "rows": summ["problems"],
                        "sha256_matches_hf_lfs_oid": True, "stored_locally": False})
    for name in ["code_generation_lite.py", "README.md"]:
        local = d / ("raw/hf_lcb_loader_0fe84c3.py" if name.endswith(".py") else "raw/hf_lcb_README_0fe84c3.md")
        add("LiveCodeBench code_generation_lite", "pinned_metadata",
            f"https://huggingface.co/datasets/livecodebench/code_generation_lite/resolve/{LCB_REV}/{name}",
            {"hf_repo": "livecodebench/code_generation_lite", "commit": LCB_REV}, local)
    out = {"retrieved": "2026-11-10", "generator": "docs/s7/parts/bench-A2/scripts/build_manifest.py", "files": entries}
    (d / "MANIFEST.json").write_text(json.dumps(out, indent=1) + "\n")
    print(len(entries), "entries")


if __name__ == "__main__":
    main()
