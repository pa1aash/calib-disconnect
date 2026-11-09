# runs

Raw outputs of pipeline runs, one subdirectory per run. Large shards (generations, logits, hidden
states) are git-ignored. Each run keeps a tracked manifest that lists every shard with its size and
SHA-256 hash, the code commit, the configuration, and the seeds, so that an ignored shard can be
verified when it is restored.

The ignore rules and the manifest format are fixed when the pipeline is designed.
