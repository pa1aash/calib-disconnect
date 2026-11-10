# Redundancy audit (step 2.6)

- **Duplicate notes.** These are the same paper in several copies (abstract page plus full text). 16 abstract-only copies were deprecated with the tag `duplicate-abstract-only`. Unindexed full-text copies are listed in research/temp/w4-canonical-paths.md.
- **Author-group clusters.** Each cluster is one research line and is not counted as independent corroboration.
  - **Devanbu group, UC Davis.** Spiess et al. 2402.02047 (ICSE 2025, calibration and correctness); Ribeiro, Spiess, Devanbu, and Nadi 2512.07404 (ICSE 2026, internal representation); Gros and Devanbu 2512.24560 (localized calibrated uncertainty); and the per-edit Platt work 2604.06723 (authors to be confirmed from the record). Together they occupy much of code calibration, code probes, and fine-grained code confidence.
  - **Nadi group.** Ribeiro et al. 2512.07404 and its robustness follow-up 2608.08266.
  - **Bui and Vu.** OPENIA 2501.12934 and AutoProbe 2510.02934, both pre- and post-generation code-correctness probing.
  - **Sharma and David.** 2502.11620 (uncertainty estimation for code correctness) and 2505.13553 or 2606.09577 (to be confirmed from the records).
- **Shared upstream sources.** Many papers rest on Kadavath et al. 2207.05221, Kuhn et al. 2302.09664 and Farquhar et al. (Nature 2024), and Tian et al. 2305.14975. These are canonical sources and are counted once.
- **Adjusted coverage.** No atomic item drops below 2 independent groups, except L4 line-level probe localization, where the only full occupant is Gros and Devanbu. It is supplemented by the IUE thesis 2609.13975 (Top-3 line localization) and PtTrust 2504.14640.
