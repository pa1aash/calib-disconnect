# Contract requests from pipeline.readouts (B4)

1. Readout names beyond `READOUTS`: `SZ_V1_drop` (V1 with unparsed rows dropped), `AGREE_problem` (largest-cluster
   share), `iso:SZ_V1_drop`, `iso:ST_inner234` (map fit on inner splits 2 to 4), `iso:ST_insample` (in-sample map).
   Please add them to `READOUTS` or tell analysis to read them by name.
2. Output paths with no `RunLayout` helper: the V1 parse rate and K3 switch
   (`readouts/<model>/<population>/SZ_V1/none/parse_rate.json`), recipes
   (`readouts/<model>/<population>/ST/recipes_seed<s>.json`), and the mask-test reports
   (`config/mask_test_<arch>.json`). Please add helpers.
3. Fit records may contain null for undefined losses (NaN is written as null).
4. DEVIATIONS to log (from the independent review): the split-1 selection adapter is reused for the isotonic map
   with a different learning-rate schedule than the other inner adapters (M5, see the `masked_lora.py` docstring);
   AdamW weight decay 0 and gradient clip 1.0; evaluation also at the final step; S^T ladder ranks 1 and 4 reuse
   the rank-16 recipe.
5. Resolved: the token layouts now come from `pipeline.generate.capture.TransformersCapture.build_layout`
   (`pipeline/readouts/layouts.py`); the answer-token file is read in the generate stage's format.
