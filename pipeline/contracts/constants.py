"""Design constants, copied from the frozen design (docs/s7/PIPELINE_DESIGN_FROZEN.md).

Each constant names the section it comes from. Modules import these values and never restate them.
Changing a value here is a departure from the frozen design and needs a docs/DEVIATIONS.md entry.
"""

from __future__ import annotations

from types import MappingProxyType

DESIGN_PATH = "docs/s7/PIPELINE_DESIGN_FROZEN.md"
DESIGN_SHA256_PATH = "docs/s7/FROZEN_SHA256.txt"

# ---- Section 1.6 and 9: decisions, margin, inference -------------------------------------------
DELTA = 0.03  # applied margin in pair-weighted within-problem AUROC (section 1.6)
DELTA_SENSITIVITY = (0.02, 0.05)  # reported as sensitivity (section 1.6)
POOLED_RESIDUAL_MARGIN = 0.03  # R_pool decisions, secondary (section 1.6)
ALPHA = 0.05
DECISION_INTERVAL_LEVEL = 0.90  # two-sided 90 percent interval: each bound one-sided 95 (1.6)
SHAPLEY_SIMULTANEOUS_LEVEL = 1 - 0.05 / 4  # 98.75 percent Bonferroni over four terms (section 9)
SHAPLEY_MARGINAL_LEVEL = 0.95
T12_QUANTILE = 1.782  # t_{12, 0.95} for the refit widening (section 9, F15)
N_REFIT_DF = 12
B_BOOTSTRAP = 10_000  # section 9, row 8.1
BOOTSTRAP_SEED = 20261110  # single fixed seed for every metric (section 9, row 8.5)
UNDEFINED_REPLICATE_MAX_SHARE = 0.01  # above this the interval is "unavailable" (section 9, V13a)

# ---- Section 13: k rule and kill criteria ----------------------------------------------------------
K_DEFAULT = 10
K_EXPANDED = 20
T10 = 185  # minimum mean EvalPlus-mixed count over P1..P6 for k = 10 (section 13, F15)
T20 = 125  # compared after k = 20 generation; reported only (section 13)
K1_MAX_REFERENCE_EXCLUSION = 0.05  # K1
K3_MIN_V1_PARSE_RATE = 0.80  # K3; also the base-model V2 switch (section 10)
K4_RETRY_LR = 1e-3  # K4 retry setting (red team V2)
K4_RETRY_EPOCHS = 4

# ---- Section 7: folds and readouts -----------------------------------------------------------------
N_FOLDS = 5
PRIMARY_FOLD_SEED = 0
FOLD_SEEDS = (0, 1, 2)  # repeated cross-fitting (section 9)
N_INNER_SPLITS = 4  # inner 4-fold problem-grouped CV inside each outer training set (section 7)
LAYER_FRACTIONS = (0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0)  # depth fractions, rounded down (5)
PROBE_C_GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)  # section 7.1
PROBE_MULTI_PCA_DIM = 512  # section 7.1
PROBE_MEMBERS = ("P2", "P3", "Pmulti")  # section 7.1
MLP_PROBE_WIDTH = 256  # section 7.11

LORA_RANK = 16  # section 7.4
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LORA_TARGET = "all attention and MLP projections"
LORA_LR_GRID = (5e-5, 1e-4, 3e-4)
LORA_EFFECTIVE_BATCH = 64
LORA_MAX_EPOCHS = 2
LORA_WARMUP_FRACTION = 0.05
LORA_EVAL_EVERY_STEPS = 20
CAPACITY_RANKS = (1, 4, 16)  # alpha twice the rank (section 7.11)
CAPACITY_MODELS = ("P3", "P2")  # Olmo-3-7B-Instruct and Qwen3-14B (section 7.11)
MASK_TEST_ATOL = 1e-3  # float32 absolute tolerance (section 7.12)

TFIDF_NGRAM_RANGE = (3, 5)  # character n-grams (section 7.10)
TFIDF_MIN_DF = 3

# ---- Section 5: generation -------------------------------------------------------------------------
TEMPERATURE = 1.0
TOP_P = 1.0
TOP_K = None  # no top-k
REPETITION_PENALTY = None
MAX_NEW_TOKENS = 1024
MAX_NEW_TOKENS_REASONING = 16_384
V1_MAX_NEW_TOKENS = 8  # greedy
K_G_LCB_RECONCILIATION = 4  # [2610.31820] reading A on LiveCodeBench

# Verbatim elicitation turns (section 5). The prompt files under pipeline/prompts/ hold the same text
# and are hashed; pipeline.generate verifies the file against these strings and the recorded hash.
V1_TEXT = (
    "Rate the probability, from 0 to 100, that the code above passes all hidden tests. "
    "Answer with one line: Confidence: N"
)
V2_TEXT = "Does the code above pass all hidden tests? Answer Yes or No."
V1_REGEX = r"Confidence:\s*(\d{1,3})"  # section 7.2
YES_STRINGS = ("Yes",)  # single tokens whose decoded text, stripped of leading whitespace, is exact
NO_STRINGS = ("No",)  # (section 7.12)
RTUNING_PREFIX = "I am"  # section 7.5
RTUNING_SURE = "I am sure"
RTUNING_UNSURE = "I am unsure"

# ---- Section 4 and 6: benchmarks, execution, labels ------------------------------------------------
NEAR_DUP_JACCARD = 0.8  # token-set Jaccard on prompt texts (section 4, V14c)
AGREEMENT_INPUT_CAP = 50  # per problem (section 4)
AGREEMENT_DEDUP_FLOAT_SIG = 6  # canonicalization for removing label-input duplicates (section 4)
AGREEMENT_SIGNATURE_FLOAT_SIG = 9  # behavior signature comparison (section 7.7)
LCB_AGREEMENT_SHARE = 0.20  # SHA-256 of the private test input selects 20 percent (section 4)
SANDBOX_MEMORY_BYTES = 2 * 1024**3  # 2 GB (section 6)
PROGRAM_WALL_CAP_S = 60.0  # whole-program cap (section 6)
CACHE_AUDIT_SHARE = 0.01  # re-execute 1 percent of cache hits (section 6)
EXTRACTION_FAILURE_CODES = (
    "no_block",  # no fenced block and the def/class fallback also fails
    "syntax_error",
    "missing_entry_point",
    "empty_output",
    "truncated",  # hit the token cap
)

# ---- Section 8: metrics ----------------------------------------------------------------------------
ECE_EQUAL_MASS_BINS = 15  # debiased equal-mass ECE and the Murphy decomposition
ECE_EQUAL_WIDTH_BINS_RECON = 15  # [2610.31820] reconciliation only
ECE_EQUAL_WIDTH_BINS_MARGIN = 10  # MARGIN comparison only

# ---- Section 10: routing replay --------------------------------------------------------------------
TRIAGE_FRACTIONS = (0.05, 0.1, 0.2, 0.3, 0.5)

# ---- Section 2: reconciliation tie widths (this design's choices) ----------------------------------
CAMPOS_TIE_WIDTH = 0.03
R2610_TIE_WIDTH = 0.02
RECONCILIATION_LEVEL = 0.95

# ---- Benchmarks (section 4; docs/s7/BENCHMARK_PINS.md) ---------------------------------------------
BENCHMARKS = ("humaneval_plus", "mbpp_plus", "lcb_v6")
LABEL_VALIDITY_BENCHMARKS = ("humaneval_plus", "mbpp_plus")
MBPP_PLUS_REMOVED_IDS = tuple(
    f"Mbpp/{i}"
    for i in (83, 115, 117, 143, 164, 229, 249, 295, 396, 400, 407, 431, 438, 442, 461, 574, 582,
              595, 640, 746, 783)
)
MBPP_PATCHED_IDS = ("Mbpp/459", "Mbpp/102", "Mbpp/559")
EVALPLUS_TOOL_VERSION = "0.3.1"

# ---- Section 3.2: model matrix (repository ID, pinned revision, role) ------------------------------
MODELS = MappingProxyType({
    "P1": ("Qwen/Qwen3-8B", "b968826d9c46dd6066d109eabc6255188de91218", "primary", False),
    "P2": ("Qwen/Qwen3-14B", "40c069824f4251a91eefaf281ebe4c544efd3e18", "primary", False),
    "P3": ("allenai/Olmo-3-7B-Instruct", "6e5971d9eba42665f5bd5a0fcf047f299ce1dccc", "primary", False),
    "P4": ("allenai/Olmo-3.1-32B-Instruct", "ac0587e4a7744a551c059d8cd17ba220bc940dae", "primary", False),
    "P5": ("google/gemma-4-12B-it", "43c9d014b231474fa7212dbb48a762566c2b255d", "primary", False),
    "P6": ("google/gemma-4-31B-it", "842da3794eaa0b77d5f08bae87a17459d91ff475", "primary", False),
    "B1": ("Qwen/Qwen3-8B-Base", "49e3418fbbbca6ecbdf9608b4d22e5a407081db4", "base", False),
    "B2": ("Qwen/Qwen3-14B-Base", "0b0bd3732e2c374d483664439ea334928b65f304", "base", False),
    "B3": ("allenai/Olmo-3-1025-7B", "a81bae42db3975be1671e27b9c9a56da1a9f980f", "base", False),
    "B4": ("allenai/Olmo-3-1125-32B", "c2b61dae89a1ad10e4ad5653d0e46b590902607b", "base", False),
    "B5": ("google/gemma-4-12B", "1a2c7729392586f5ecddae8807ee2ef741eabb9a", "base", False),
    "B6": ("google/gemma-4-31B", "5bbc2fb1c1b2c611d06e3d9f23c170ba21659d89", "base", False),
    "S1": ("Qwen/Qwen3-8B", "b968826d9c46dd6066d109eabc6255188de91218", "reasoning", True),
    "C1": ("Qwen/Qwen2.5-Coder-7B-Instruct", "c03e6d358207e414f1eca0bb1891e29f1db0e242", "coder", False),
    "C2": ("Qwen/Qwen2.5-Coder-32B-Instruct", "381fc969f78efac66bc87ff7ddeadb7e73c218a7", "coder", False),
    "C3": ("Qwen/Qwen2.5-Coder-7B", "0396a76181e127dfc13e5c5ec48a8cee09938b02", "coder_base", False),
    "C4": ("Qwen/Qwen2.5-Coder-32B", "2e12b5f7bc878d424d222e224ed40aee564ec45f", "coder_base", False),
    "T1": ("allenai/Olmo-3-7B-Instruct-SFT", "e1452fc572d51966ff4aaeb25118b891eb93e549", "trajectory", False),
    "T2": ("allenai/Olmo-3-7B-Instruct-DPO", "b33130b7de49f0c2553b5c2b3bc8409ff3e627d1", "trajectory", False),
    "X1": ("Qwen/Qwen3-Coder-30B-A3B-Instruct", "b2cff646eb4bb1d68355c01b18ae02e7cf42d120", "reconciliation", False),
    "X2": ("openai/gpt-oss-20b", "6cee5e81ee83917806bbde320786a8fb61efebee", "reconciliation", False),
})
"""model key -> (repository ID, revision, role, thinking on). Section 3.2."""

PRIMARY_MODELS = ("P1", "P2", "P3", "P4", "P5", "P6")
PILOT_MODEL = "T1"
THROUGHPUT_PROBE_MODELS = ("P4", "P6", "S1")

# Count dates for the LiveCodeBench contamination stratum (section 3.2).
COUNT_DATES = MappingProxyType({
    "P1": "2025-04-27", "P2": "2025-04-27", "S1": "2025-04-27", "B1": "2025-04-28", "B2": "2025-04-28",
    "P3": "2024-12-31", "P4": "2024-12-31", "B3": "2024-12-31", "B4": "2024-12-31",
    "T1": "2024-12-31", "T2": "2024-12-31",
    "P5": "2025-01-31", "P6": "2025-01-31", "B5": "2025-01-31", "B6": "2025-01-31",
    "C1": "2024-09-17", "C2": "2024-11-06", "C3": "2024-09-16", "C4": "2024-11-08",
    "X1": "2025-07-31", "X2": "2024-06-30",
})

# Local smoke test only (wave 8, step C2). Not part of the study; never in any analysis.
SMOKE_MODEL = ("Qwen/Qwen3-0.6B", "c1899de289a04d12100db370d81485cdf75e47ca")
