# Raw files kept local and untracked (orchestrator note, wave 6)

Three saved upstream commit feeds are kept on disk but not tracked, because their third-party commit messages contain co-author trailers that the project's pre-commit attribution check rejects in any tracked file. They are listed in `.git/info/exclude`.

- `raw/gh_lcb_commits.atom` (LiveCodeBench GitHub commit feed)
- `raw/hf_commits_evalplus_humanevalplus.json` (Hugging Face commit list of evalplus/humanevalplus)
- `raw/hf_lcb_commits.json` (Hugging Face commit list of the LiveCodeBench dataset)

`BENCHMARKS.md` uses them for the "HF commit date" column of the LiveCodeBench release table and for the HumanEval+ mirror commit details. Those cells rest on these untracked files only; anyone re-verifying them from the repository must refetch the feeds.
