### RT1. Widening multiplier 1.645 versus t = 1.782 (R2 rule, n = 542, 480 replicates; D1 / D2 / D3, min; SE of min-limiting cell in last column)

| Heterogeneity | k | delta | mean mixed | unwidened | z = 1.645 | t = 1.782 | SE (t = 1.782, D1) |
|---|---|---|---|---|---|---|---|
| nominal | 10 | 0.03 | 233.4 | 0.994 / 0.994 / 0.996, min 0.994 | 0.983 / 0.994 / 0.981, min 0.981 | 0.979 / 0.992 / 0.979, min 0.979 | 0.007 |
| nominal | 10 | 0.02 | 233.4 | 0.802 / 0.890 / 0.915, min 0.802 | 0.704 / 0.854 / 0.831, min 0.704 | 0.685 / 0.848 / 0.812, min 0.685 | 0.021 |
| nominal | 20 | 0.03 | 277.6 | 1.000 / 1.000 / 1.000, min 1.000 | 0.994 / 0.998 / 0.996, min 0.994 | 0.994 / 0.998 / 0.994, min 0.994 | 0.004 |
| conservative | 10 | 0.03 | 233.4 | 0.994 / 0.977 / 0.998, min 0.977 | 0.983 / 0.971 / 0.990, min 0.971 | 0.981 / 0.971 / 0.983, min 0.971 | 0.006 |
| conservative | 10 | 0.02 | 233.4 | 0.806 / 0.871 / 0.910, min 0.806 | 0.673 / 0.812 / 0.829, min 0.673 | 0.662 / 0.804 / 0.817, min 0.662 | 0.024 |
| conservative | 20 | 0.03 | 277.6 | 0.998 / 0.992 / 1.000, min 0.992 | 0.996 / 0.990 / 0.996, min 0.990 | 0.994 / 0.990 / 0.996, min 0.990 | 0.004 |

(The k = 20, delta 0.02 cells are also in the JSON: nominal min 0.858 and conservative 0.848 at t = 1.782.)

### RT2. Heterogeneous mixed counts (k = 10, delta 0.03, n = 542, 480 replicates): one model at 60 mixed, five near 207 to 259

| Heterogeneity | mixed per model (six) | unwidened | z = 1.645 | t = 1.782 |
|---|---|---|---|---|
| nominal | [259.3, 207.5, 259.2, 60.0, 259.0, 208.2] | 0.954 / 0.975 / 0.979, min 0.954 | 0.919 / 0.963 / 0.948, min 0.919 | 0.915 / 0.963 / 0.942, min 0.915 |
| conservative | [259.3, 207.5, 259.2, 60.0, 259.0, 208.2] | 0.950 / 0.954 / 0.981, min 0.950 | 0.923 / 0.940 / 0.952, min 0.923 | 0.917 / 0.938 / 0.946, min 0.917 |

### RT3. Residual-error correlation rho_e (delta 0.03, n = 542, 480 replicates; baseline rho_e = 0.5 is in RT1)

| Heterogeneity | k | rho_e | SD of point | bootstrap h | t = 1.782: D1 / D2 / D3, min |
|---|---|---|---|---|---|
| conservative | 10 | 0.2 | 0.0079 | 0.0114 | 0.944 / 0.952 / 0.965, min 0.944 |
| conservative | 10 | 0.8 | 0.0061 | 0.0068 | 1.000 / 0.994 / 0.996, min 0.994 |
| nominal | 10 | 0.2 | 0.0084 | 0.0115 | 0.931 / 0.967 / 0.958, min 0.931 |
| nominal | 10 | 0.8 | 0.0065 | 0.0069 | 1.000 / 1.000 / 0.994, min 0.994 |
| nominal | 20 | 0.2 | 0.0065 | 0.0079 | 0.992 / 1.000 / 0.994, min 0.992 |
| nominal | 20 | 0.8 | 0.0053 | 0.0047 | 1.000 / 1.000 / 0.998, min 0.998 |

### RT4. Min power (t = 1.782, delta 0.03) versus mean mixed count and mean pass-fail pairs per model

n sweep: 240 replicates per point (20 worlds x 12) except the n = 542 point (480). mu and kappa scenarios: n = 542, nominal heterogeneity, 240 replicates, all six models' mu shifted together (offset in `scenario_info`) or kappa changed.

| k | scenario | setting | mean mixed | mean pairs | D1 / D2 / D3 | min |
|---|---|---|---|---|---|---|
| 10 | n_sweep | n = 150 | 64.7 | 1090 | 0.579 / 0.804 / 0.733 | 0.579 |
| 10 | n_sweep | n = 200 | 85.5 | 1440 | 0.725 / 0.842 / 0.854 | 0.725 |
| 10 | n_sweep | n = 250 | 107.9 | 1822 | 0.846 / 0.942 / 0.892 | 0.846 |
| 10 | n_sweep | n = 300 | 128.8 | 2173 | 0.867 / 0.958 / 0.908 | 0.867 |
| 10 | n_sweep | n = 400 | 172.0 | 2900 | 0.967 / 0.983 / 0.975 | 0.967 |
| 10 | n_sweep | n = 542 | 233.4 | 3928 | 0.979 / 0.992 / 0.979 | 0.979 |
| 10 | mu_sweep | mu offset +0.1555 | 100.4 | 1653 | 0.675 / 0.838 / 0.838 | 0.675 |
| 10 | mu_sweep | mu offset +0.1365 | 120.5 | 1987 | 0.762 / 0.863 / 0.871 | 0.762 |
| 10 | mu_sweep | mu offset +0.1164 | 140.2 | 2321 | 0.858 / 0.912 / 0.921 | 0.858 |
| 10 | mu_sweep | mu offset +0.0836 | 170.3 | 2832 | 0.904 / 0.963 / 0.917 | 0.904 |
| 10 | mu_sweep | mu offset +0.0469 | 200.2 | 3347 | 0.929 / 0.971 / 0.975 | 0.929 |
| 10 | mu_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 233.4 | 3928 | 0.979 / 0.992 / 0.979 | 0.979 |
| 10 | kappa_sweep | kappa 0.4 | 152.7 | 2515 | 0.904 / 0.954 / 0.946 | 0.904 |
| 10 | kappa_sweep | kappa 0.5 | 177.0 | 2935 | 0.946 / 0.975 / 0.958 | 0.946 |
| 10 | kappa_sweep | kappa 0.6 | 198.2 | 3303 | 0.942 / 0.971 / 0.975 | 0.942 |
| 10 | kappa_sweep | kappa 0.7 | 216.6 | 3626 | 0.950 / 0.983 / 0.979 | 0.950 |
| 10 | kappa_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 233.4 | 3928 | 0.979 / 0.992 / 0.979 | 0.979 |
| 20 | n_sweep | n = 150 | 76.6 | 4581 | 0.921 / 0.958 / 0.938 | 0.921 |
| 20 | n_sweep | n = 200 | 102.5 | 6111 | 0.950 / 0.983 / 0.954 | 0.950 |
| 20 | n_sweep | n = 250 | 127.6 | 7620 | 0.975 / 0.992 / 0.971 | 0.971 |
| 20 | n_sweep | n = 300 | 153.5 | 9161 | 0.988 / 0.996 / 0.979 | 0.979 |
| 20 | n_sweep | n = 400 | 204.9 | 12217 | 1.000 / 1.000 / 0.988 | 0.988 |
| 20 | n_sweep | n = 542 | 277.6 | 16570 | 0.994 / 0.998 / 0.994 | 0.994 |
| 20 | mu_sweep | mu offset +0.1896 | 75.2 | 4251 | 0.412 / 0.708 / 0.667 | 0.412 |
| 20 | mu_sweep | mu offset +0.1754 | 95.3 | 5406 | 0.821 / 0.892 / 0.887 | 0.821 |
| 20 | mu_sweep | mu offset +0.1568 | 120.4 | 6871 | 0.950 / 0.975 / 0.963 | 0.950 |
| 20 | mu_sweep | mu offset +0.133 | 150.4 | 8652 | 0.958 / 0.975 / 0.963 | 0.958 |
| 20 | mu_sweep | mu offset +0.0978 | 190.6 | 11074 | 0.988 / 1.000 / 1.000 | 0.988 |
| 20 | mu_sweep | mu offset +0.0576 | 230.7 | 13553 | 0.992 / 1.000 / 1.000 | 0.992 |
| 20 | mu_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 277.6 | 16570 | 0.994 / 0.998 / 0.994 | 0.994 |
| 20 | kappa_sweep | kappa 0.4 | 186.0 | 10645 | 1.000 / 1.000 / 0.992 | 0.992 |
| 20 | kappa_sweep | kappa 0.5 | 214.4 | 12431 | 0.996 / 1.000 / 0.992 | 0.992 |
| 20 | kappa_sweep | kappa 0.6 | 238.9 | 13993 | 0.996 / 1.000 / 0.992 | 0.992 |
| 20 | kappa_sweep | kappa 0.7 | 259.9 | 15369 | 1.000 / 1.000 / 0.996 | 0.996 |
| 20 | kappa_sweep | baseline (mu 0.72/0.80, kappa 0.801, n = 542) | 277.6 | 16570 | 0.994 / 0.998 / 0.994 | 0.994 |

### RT5. Thresholds T10 and T20 (delta 0.03, t = 1.782)

| k | bracketed crossings of 0.90 (mean mixed per model) | not bracketed | T (largest bracketed crossing x 1.10, rounded up to 5) | verification run (480 replicates, separate seeds) |
|---|---|---|---|---|
| 10 | {'n_sweep': 143.1, 'mu_sweep': 167.7} | min power >= 0.90 at every kappa tested (mixed 152.7 to 233.4) | **185** | mixed 184.8, pairs 3082: D1 0.94, D2 0.983, D3 0.948, min 0.94 |
| 20 | {'mu_sweep': 110.7} | min power >= 0.90 at every n tested (mixed 76.6 to 277.6); min power >= 0.90 at every kappa tested (mixed 186.0 to 277.6) | **125** | mixed 125.3, pairs 7149: D1 0.946, D2 0.988, D3 0.954, min 0.946 |
