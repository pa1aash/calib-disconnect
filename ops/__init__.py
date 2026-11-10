"""Pod operations (module B6): bootstrap, job runner, sync, cost guard, RunPod client, dry run.

Nothing in this package imports a heavy numerical module at import time. Stage modules are imported
only when a job actually runs (never in a dry run).
"""

REPO_ROOT_ENV = "OPS_REPO_ROOT"
