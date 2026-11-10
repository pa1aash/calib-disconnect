# Verdict effect of dossier A2 (wave 5, Part A)

Run date 2026-11-10. Cells refer to `research/positioning/w4/VERDICTS.md`.

## 2610.19226 (Agentic Self-Awareness), FULL TEXT

- **L3 Q2/Q7 (stated confidence updates after a shown failing test; tracks repair; valid versus spurious failures): no change, stays CLEAN (provisional).** The challenge is "one direction-neutral request to reconsider" with no evidence attached (A.2.4); no test output is shown. The stated probability comes from "a separate read-only probe" and is not re-elicited after the challenge (A.2.3, Sec 4.2). Table 6 reports transitions of binary judgment correctness, not of confidence. The label is task feasibility from design-time metadata, not code correctness. Add it to the nearest-not-occupying list beside Kaddour 2602.06948 and Barkan Exp. 3.
- **Rank 3 add-on:** NARROWS the framing only. Its CRA, "P(z1 = 1 | z0 = 0) − P(z1 = 0 | z0 = 1)" (Eq. 6), already scores correction versus harmful flips after a challenge. Rank 3 should cite it and set its own contrast apart: an evidence-bearing challenge (a real versus a spurious failing test) and a numeric confidence update, on code. A neutral challenge arm would also give a direct reference point.
- **Rank 1:** cannot be unseated. There is no hidden-state probe, no supervision-matched own readout, no input-only baseline, and no within-problem scoring. It uses one closed main model (GPT-5.5).

## 10.1109/tse.2026.3713834 (Generalization or Memorization), arXiv 2402.15938v3 FULL TEXT; TSE ABSTRACT-ONLY

- **Version caveat:** the match is unconfirmed. Crossref "relation" is empty, and Semantic Scholar lists no arXiv ID. The TSE title, the eighth author (Xuanming Zhang), and MGI appear only in the TSE record. A TSE-only section could hold a calibration analysis. The TSE abstract names none ("Accuracy, F1 Score, and AUC" are detection metrics, and MGI is a generalizability index). The residual risk is low but not zero.
- **L1 Q13 (contamination changes calibration or discrimination): no change, stays CLEAN (provisional).** v3 measures no confidence readout of correctness: there are zero hits for calibrat, uncertaint, ECE, or confidence outside the lab name. One indirect point: contamination makes sampled outputs peaked ("more than 20 times larger" zero-edit-distance density, Sec 2). That predicts inflated sampling-agreement confidence on leaked problems. The release split can test that prediction. It supports the design but does not occupy the cell.
- **L1 Q3 (release-date split): no change, stays NARROW.** CodeForces2305 is a post-cutoff set for one closed model. It contrasts pass@1 and peakedness (Table 5), not calibration.
- **Rank 1:** cannot be unseated. There are no confidence families, probes, or calibration metrics.

## Process note

The arXiv HTML for 2610.19226 dropped the math-rendered numbers, so all quoted numbers come from the locally extracted PDF. While checking the authors' repository, one request went to raw.githubusercontent.com, which is not on the allowed host list. Its content was discarded and not used. The github.com page that was used is saved in raw/.
