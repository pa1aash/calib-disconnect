"""Statistics for the frozen design (docs/s7/PIPELINE_DESIGN_FROZEN.md, sections 1, 2.1, 8, 9, 10, 13).

Every module except analysis.stage is a set of pure functions on numpy arrays. analysis.stage reads
run files, calls these functions, and writes JSON under analysis/results/<run_id>/.
"""
