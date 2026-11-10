"""Hidden-state probes (design 7.1, 7.9, 7.11).

Model: L2 logistic regression on features standardized with the training-fold mean and variance.
Family members: P2 (one layer at p2), P3 (one layer at p3), Pmulti (all layers at p2, concatenated,
PCA to PROBE_MULTI_PCA_DIM fit on the training rows, capped at the training rank). Layer and C
(PROBE_C_GRID) are chosen inside each outer training set by inner 4-fold problem-grouped
cross-validation, minimizing pooled out-of-fold log loss. Every scaler, PCA, and classifier of a
selection is refit on the inner training rows only, so nothing from the inner validation fold, and
nothing from the outer test fold, enters a fit.

Outputs (`crossfit_family`): P (the best member by inner CV loss), each member on its own, and
P2_single_split (the whole family selected on the first inner split only, the 7.4 sensitivity; the
name follows the READOUTS tuple, the selection spans the whole family as 7.4 describes "the probe").
`crossfit_mlp` is the 7.11 sensitivity; `crossfit_prompt` is the 7.9 prompt-only probe.

Scores: rank_score is the classifier logit (no saturation ties), prob its logistic transform.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field

import numpy as np
from scipy.special import expit
from sklearn.decomposition import PCA
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from pipeline.contracts import constants as K
from pipeline.contracts.interfaces import ReadoutData
from pipeline.contracts.schemas import FitRecord, FoldPlan, ReadoutScore

from .common import (Folds, base_rate_logloss, fit_record, hidden_array, logit, logloss, logloss_sum,
                     record_fit, scores_from_arrays, train_base_rate)

MLP_WD_GRID = (1e-3, 1e-2, 1e-1, 1.0)  # weight decay (sklearn alpha) grid for the 7.11 MLP probe; not fixed by the design
MLP_MAX_ITER = 200
LR_MAX_ITER = 500


@dataclass(frozen=True)
class FeatureSpec:
    member: str          # "P2" | "P3" | "Pmulti" | "PROMPT"
    key: str             # hidden array key
    layer: int | None    # layer index among the L candidates; None = all layers concatenated (PCA)

    @property
    def multi(self) -> bool:
        return self.layer is None


def family_specs(n_layers: int) -> dict[str, list[FeatureSpec]]:
    return {
        "P2": [FeatureSpec("P2", "hs_p2", l) for l in range(n_layers)],
        "P3": [FeatureSpec("P3", "hs_p3", l) for l in range(n_layers)],
        "Pmulti": [FeatureSpec("Pmulti", "hs_p2", None)],
    }


class _Features:
    """Memoized float32 design matrices per feature spec."""

    def __init__(self, data: ReadoutData):
        self.data = data
        self._cache: dict[FeatureSpec, np.ndarray] = {}

    def __call__(self, spec: FeatureSpec) -> np.ndarray:
        if spec not in self._cache:
            h = hidden_array(self.data, spec.key)
            x = h.reshape(h.shape[0], -1) if spec.multi else h[:, spec.layer, :]
            self._cache[spec] = np.ascontiguousarray(x, dtype=np.float32)
        return self._cache[spec]


# ---------------------------------------------------------------------------------------------------
# Fit primitives
# ---------------------------------------------------------------------------------------------------
def _design(Xtr: np.ndarray, Xaps: list[np.ndarray], multi: bool, tag: str, pids: set[str] | frozenset[str],
            state_out: dict | None = None):
    """Standardize with training mean and variance; optionally PCA fit on the training rows."""
    record_fit(f"{tag}:scaler", pids)
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd = np.where(sd < 1e-8, 1.0, sd).astype(np.float32)
    mu = mu.astype(np.float32)
    Ztr = (Xtr - mu) / sd
    Zaps = [(X - mu) / sd for X in Xaps]
    if multi:
        record_fit(f"{tag}:pca", pids)
        k = int(min(K.PROBE_MULTI_PCA_DIM, Ztr.shape[0] - 1, Ztr.shape[1]))  # cap at the training rank
        k = max(k, 1)
        solver = "randomized" if k < 0.8 * min(Ztr.shape) else "full"
        pca = PCA(n_components=k, svd_solver=solver, random_state=0).fit(Ztr)
        Ztr = pca.transform(Ztr)
        Zaps = [pca.transform(Z) for Z in Zaps]
        if state_out is not None:
            state_out.update(pca_mean=pca.mean_.astype(np.float32), pca_components=pca.components_.astype(np.float32))
    if state_out is not None:
        state_out.update(mu=mu, sd=sd)
    return Ztr, Zaps


def _lr_logits(Ztr: np.ndarray, ytr: np.ndarray, Zaps: list[np.ndarray], Cs, tag: str, pids,
               clf_out: dict | None = None) -> dict[float, list[np.ndarray]]:
    """Logits of an L2 logistic regression for each C (ascending, warm-started)."""
    record_fit(f"{tag}:classifier", pids)
    out: dict[float, list[np.ndarray]] = {}
    if len(np.unique(ytr)) < 2:
        c = float(logit(train_base_rate(ytr)))
        for C in Cs:
            out[C] = [np.full(len(Z), c) for Z in Zaps]
        if clf_out is not None:
            clf_out.update(coef=np.zeros(Ztr.shape[1], dtype=np.float64), intercept=c)
        return out
    clf = LogisticRegression(C=1.0, max_iter=LR_MAX_ITER, warm_start=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        for C in sorted(Cs):
            clf.set_params(C=C)
            clf.fit(Ztr, ytr)
            out[C] = [clf.decision_function(Z).astype(np.float64) for Z in Zaps]
    if clf_out is not None:
        clf_out.update(coef=clf.coef_[0].astype(np.float64), intercept=float(clf.intercept_[0]))
    return out


@dataclass
class Selection:
    """Inner-CV table for one outer fold."""

    loss: dict[tuple[str, int | None, float], float] = field(default_factory=dict)       # pooled CV log loss
    loss_split0: dict[tuple[str, int | None, float], float] = field(default_factory=dict)  # first inner split only
    base_rate_pooled: float = float("nan")
    base_rate_split0: float = float("nan")

    def best(self, members: tuple[str, ...] | None = None, split0: bool = False):
        table = self.loss_split0 if split0 else self.loss
        items = [(k, v) for k, v in table.items() if (members is None or k[0] in members) and np.isfinite(v)]
        if not items:
            return None
        return min(items, key=lambda kv: kv[1])  # first minimum in insertion order


def select_over_specs(feats: _Features, F: Folds, f: int, specs: list[FeatureSpec], Cs, tag: str) -> Selection:
    inner = F.inner(f)
    y = F.y
    sel = Selection()
    n_val_total = sum(len(va) for tr, va in inner if len(tr) and len(va))
    base_sum = 0.0
    for j, (tr, va) in enumerate(inner):
        if len(tr) and len(va):
            bl = base_rate_logloss(y[tr], y[va])
            base_sum += bl * len(va)
            if j == 0:
                sel.base_rate_split0 = bl
    sel.base_rate_pooled = base_sum / max(n_val_total, 1)
    for spec in specs:
        X = feats(spec)
        acc = {C: 0.0 for C in Cs}
        split0: dict[float, float] = {}
        for j, (tr, va) in enumerate(inner):
            if len(tr) == 0 or len(va) == 0:
                continue
            pids = F.problems_of(tr)
            Ztr, (Zva,) = _design(X[tr], [X[va]], spec.multi, f"{tag}:{spec.member}:inner{j}", pids)
            logits = _lr_logits(Ztr, y[tr], [Zva], Cs, f"{tag}:{spec.member}:inner{j}", pids)
            for C in Cs:
                l = logloss_sum(y[va], expit(logits[C][0]))
                acc[C] += l
                if j == 0:
                    split0[C] = l / len(va)
        for C in Cs:
            sel.loss[(spec.member, spec.layer, C)] = acc[C] / max(n_val_total, 1)
            if C in split0:
                sel.loss_split0[(spec.member, spec.layer, C)] = split0[C]
    return sel


@dataclass
class FittedProbe:
    """A fitted probe, enough to score new hidden states (reading A applies it to fresh samples)."""

    member: str
    layer: int | None
    key: str
    C: float
    mu: np.ndarray
    sd: np.ndarray
    coef: np.ndarray
    intercept: float
    pca_mean: np.ndarray | None = None
    pca_components: np.ndarray | None = None
    label_suite: str = ""
    fold_seed: int = 0
    outer_fold: int = 0

    def logits(self, hidden: dict[str, np.ndarray]) -> np.ndarray:
        h = np.asarray(hidden[self.key])
        X = h.reshape(h.shape[0], -1) if self.layer is None else h[:, self.layer, :]
        Z = (X.astype(np.float32) - self.mu) / self.sd
        if self.pca_components is not None:
            Z = (Z - self.pca_mean) @ self.pca_components.T
        return Z.astype(np.float64) @ self.coef + self.intercept

    def save(self, path) -> None:
        import json as _json
        from pathlib import Path as _P
        _P(path).parent.mkdir(parents=True, exist_ok=True)
        meta = dict(member=self.member, layer=self.layer, key=self.key, C=self.C, intercept=self.intercept,
                    label_suite=self.label_suite, fold_seed=self.fold_seed, outer_fold=self.outer_fold,
                    has_pca=self.pca_components is not None)
        arrs = dict(mu=self.mu, sd=self.sd, coef=self.coef, meta=np.array(_json.dumps(meta)))
        if self.pca_components is not None:
            arrs.update(pca_mean=self.pca_mean, pca_components=self.pca_components)
        with open(path, "wb") as fh:
            np.savez(fh, **arrs)

    @classmethod
    def load(cls, path) -> "FittedProbe":
        import json as _json
        z = np.load(path, allow_pickle=False)
        m = _json.loads(str(z["meta"]))
        return cls(member=m["member"], layer=m["layer"], key=m["key"], C=m["C"], mu=z["mu"], sd=z["sd"], coef=z["coef"],
                   intercept=m["intercept"], pca_mean=z["pca_mean"] if m["has_pca"] else None,
                   pca_components=z["pca_components"] if m["has_pca"] else None, label_suite=m["label_suite"],
                   fold_seed=m["fold_seed"], outer_fold=m["outer_fold"])


def _final_fit(feats: _Features, F: Folds, f: int, spec: FeatureSpec, C: float, tag: str
               ) -> tuple[np.ndarray, np.ndarray, FittedProbe]:
    tr, te = F.outer_train(f), F.outer_test(f)
    X = feats(spec)
    pids = F.problems_of(tr)
    st: dict = {}
    clf: dict = {}
    Ztr, (Zte,) = _design(X[tr], [X[te]], spec.multi, f"{tag}:{spec.member}:final", pids, state_out=st)
    logits = _lr_logits(Ztr, F.y[tr], [Zte], [C], f"{tag}:{spec.member}:final", pids, clf_out=clf)[C][0]
    fp = FittedProbe(member=spec.member, layer=spec.layer, key=spec.key, C=C, mu=st["mu"], sd=st["sd"],
                     coef=clf["coef"], intercept=clf["intercept"], pca_mean=st.get("pca_mean"),
                     pca_components=st.get("pca_components"), label_suite=F.suite or "", fold_seed=F.plan.fold_seed,
                     outer_fold=f)
    return te, logits, fp


def _final_logits(feats: _Features, F: Folds, f: int, spec: FeatureSpec, C: float, tag: str) -> tuple[np.ndarray, np.ndarray]:
    te, logits, _ = _final_fit(feats, F, f, spec, C, tag)
    return te, logits


# ---------------------------------------------------------------------------------------------------
# Family
# ---------------------------------------------------------------------------------------------------
@dataclass
class FamilyResult:
    scores: dict[str, list[ReadoutScore]] = field(default_factory=dict)
    fits: dict[str, list[FitRecord]] = field(default_factory=dict)
    chosen: dict[int, dict[str, dict]] = field(default_factory=dict)   # outer fold -> readout -> selection
    best_single_layer: dict[int, int] = field(default_factory=dict)    # outer fold -> layer for the MLP probe
    fitted: dict[tuple[int, str], "FittedProbe"] = field(default_factory=dict)  # (outer fold, readout) -> fitted probe


def _spec_for(specs: dict[str, list[FeatureSpec]], member: str, layer: int | None) -> FeatureSpec:
    for s in specs[member]:
        if s.layer == layer:
            return s
    raise KeyError((member, layer))


PROBE_RETRY_EXTRA_C = (1e-4, 100.0)   # K4 retry for the probe: these values are added to the grid


def crossfit_family(data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str, population: str, *,
                    want: tuple[str, ...] = ("P", "P2", "P3", "Pmulti", "P2_single_split"),
                    C_grid=K.PROBE_C_GRID) -> FamilyResult:
    """Family selection with the probe's K4 retry (section 13): if, for a majority of outer folds, the best
    inner-CV log loss of the family is no better than the training base rate, the selection is repeated
    once with PROBE_RETRY_EXTRA_C added to the C grid (every fold). If it still fails on a majority the
    result is kept and flagged. FitRecords carry `retried` and `flagged`; scores carry `flagged`."""
    res, fails = _family_once(data, plan, label_suite, model_key, population, want, C_grid, False, False)
    if fails and sum(fails) * 2 > len(fails):
        grid = tuple(sorted(set(C_grid) | set(PROBE_RETRY_EXTRA_C)))
        res, fails2 = _family_once(data, plan, label_suite, model_key, population, want, grid, True, False)
        if fails2 and sum(fails2) * 2 > len(fails2):
            res, _ = _family_once(data, plan, label_suite, model_key, population, want, grid, True, True)
    return res


def _family_once(data, plan, label_suite, model_key, population, want, C_grid, retried: bool, flagged: bool):
    F = Folds(data, plan, label_suite)
    feats = _Features(data)
    n_layers = hidden_array(data, "hs_p2").shape[1]
    specs = family_specs(n_layers)
    need_all = any(w in want for w in ("P", "P2_single_split", "MLP"))
    members = tuple(PROBE_MEMBERS) if need_all else tuple(m for m in PROBE_MEMBERS if m in want)
    all_specs = [s for m in members for s in specs[m]]
    res = FamilyResult(scores={w: [] for w in want}, fits={w: [] for w in want})
    fails: list[bool] = []
    final_cache: dict[tuple, tuple[np.ndarray, np.ndarray, FittedProbe]] = {}

    def final(f, spec, C):
        key = (f, spec.member, spec.layer, C)
        if key not in final_cache:
            final_cache[key] = _final_fit(feats, F, f, spec, C, f"probe:outer{f}")
        return final_cache[key]

    for f in F.outer_folds:
        sel = select_over_specs(feats, F, f, all_specs, C_grid, f"probe:outer{f}")
        best_any = sel.best(members)
        fails.append(best_any is None or not (best_any[1] < sel.base_rate_pooled))
        picks: dict[str, tuple[tuple, float]] = {}
        for m in members:
            b = sel.best((m,))
            if b is not None:
                picks[m] = b
        if "P" in want and picks:
            picks["P"] = min(((picks[m][0], picks[m][1]) for m in members if m in picks), key=lambda kv: kv[1])
        if "P2_single_split" in want:
            b = sel.best(members, split0=True)
            if b is not None:
                picks["P2_single_split"] = (b[0], sel.loss[b[0]])
        res.chosen[f] = {}
        for name in want:
            if name not in picks:
                continue
            (member, layer, C), cv_loss = picks[name]
            spec = _spec_for(specs, member, layer)
            te, logits, fitted = final(f, spec, C)
            res.fitted[(f, name)] = fitted
            res.scores[name] += scores_from_arrays(data, te, logits, expit(logits), folds=F, model_key=model_key,
                                                   population=population, readout=name, label_suite=label_suite,
                                                   flagged=flagged)
            info = {"member": member, "layer": layer, "C": C, "n_train": int(len(F.outer_train(f)))}
            if name == "P2_single_split":
                info["selected_on"] = "first inner split"
                loss_for_record, base_for_record = sel.loss_split0[(member, layer, C)], sel.base_rate_split0
            else:
                loss_for_record, base_for_record = cv_loss, sel.base_rate_pooled
            info["C_grid"] = list(C_grid)
            res.fits[name].append(fit_record(model_key, name, label_suite, plan, f, info, loss_for_record,
                                             base_for_record, retried=retried, flagged=flagged))
            res.chosen[f][name] = info
        # layer for the MLP probe: best single-layer member by pooled inner CV loss
        b = sel.best(("P2", "P3"))
        if b is not None:
            res.best_single_layer[f] = int(b[0][1])
    return res, fails


PROBE_MEMBERS = K.PROBE_MEMBERS


class ProbeReadout:
    """SupervisedReadout for one of P, P2, P3, Pmulti, P2_single_split. A shared `cache` dict lets the
    five readouts reuse one family computation."""

    def __init__(self, name: str, cache: dict | None = None):
        if name not in ("P", "P2", "P3", "Pmulti", "P2_single_split"):
            raise ValueError(name)
        self.name = name
        self.cache = cache if cache is not None else {}

    def crossfit(self, data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str, population: str):
        key = (id(data), plan.fold_seed, plan.population, label_suite, model_key, population)
        if key not in self.cache:
            self.cache[key] = crossfit_family(data, plan, label_suite, model_key, population)
        r: FamilyResult = self.cache[key]
        return r.scores[self.name], r.fits[self.name]


# ---------------------------------------------------------------------------------------------------
# Prompt-only probe (7.9)
# ---------------------------------------------------------------------------------------------------
def crossfit_prompt(data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str, population: str, *,
                    C_grid=K.PROBE_C_GRID) -> tuple[list[ReadoutScore], list[FitRecord]]:
    """The single-layer family at p1 (the last prompt token), same classifier, same nested selection.
    The state at p1 is identical for every sample of a problem, so the score is constant within it."""
    F = Folds(data, plan, label_suite)
    feats = _Features(data)
    n_layers = hidden_array(data, "hs_p1").shape[1]
    specs = [FeatureSpec("PROMPT", "hs_p1", l) for l in range(n_layers)]
    scores, fits = [], []
    for f in F.outer_folds:
        sel = select_over_specs(feats, F, f, specs, C_grid, f"prompt:outer{f}")
        b = sel.best(("PROMPT",))
        if b is None:
            continue
        (member, layer, C), cv = b
        spec = FeatureSpec("PROMPT", "hs_p1", layer)
        te, logits = _final_logits(feats, F, f, spec, C, f"prompt:outer{f}")
        scores += scores_from_arrays(data, te, logits, expit(logits), folds=F, model_key=model_key,
                                     population=population, readout="PROMPT", label_suite=label_suite)
        fits.append(fit_record(model_key, "PROMPT", label_suite, plan, f,
                               {"member": "PROMPT", "layer": layer, "C": C, "position": "p1"}, cv, sel.base_rate_pooled))
    return scores, fits


# ---------------------------------------------------------------------------------------------------
# MLP probe (7.11)
# ---------------------------------------------------------------------------------------------------
def _mlp_fit_predict(Xtr, ytr, Xaps, alpha: float, seed: int):
    if len(np.unique(ytr)) < 2:
        c = float(logit(train_base_rate(ytr)))
        return [np.full(len(X), c) for X in Xaps]
    clf = MLPClassifier(hidden_layer_sizes=(K.MLP_PROBE_WIDTH,), activation="relu", alpha=alpha, solver="adam",
                        max_iter=MLP_MAX_ITER, random_state=seed, batch_size=min(200, len(ytr)))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        clf.fit(Xtr, ytr)
    return [logit(clf.predict_proba(X)[:, 1], eps=1e-7) for X in Xaps]


def crossfit_mlp(data: ReadoutData, plan: FoldPlan, label_suite: str, model_key: str, population: str, *,
                 layer_by_fold: dict[int, int] | None = None, wd_grid=MLP_WD_GRID,
                 family: FamilyResult | None = None) -> tuple[list[ReadoutScore], list[FitRecord]]:
    """One hidden layer (width MLP_PROBE_WIDTH, ReLU) on [mean code-token state, p3 state] at the selected
    layer. The layer is the best single-layer family member by inner CV loss in the same outer fold; the
    weight decay is selected on the first inner split."""
    F = Folds(data, plan, label_suite)
    if layer_by_fold is None:
        fam = family or crossfit_family(data, plan, label_suite, model_key, population, want=("P2", "P3"))
        layer_by_fold = fam.best_single_layer
    hm, h3 = hidden_array(data, "hs_mean_code"), hidden_array(data, "hs_p3")
    scores, fits = [], []
    for f in F.outer_folds:
        if f not in layer_by_fold:
            continue
        l = layer_by_fold[f]
        X = np.concatenate([hm[:, l, :], h3[:, l, :]], axis=1).astype(np.float32)
        inner = F.inner(f)
        tr0, va0 = inner[0]
        best_alpha, best_loss = wd_grid[0], np.inf
        base0 = float("nan")
        if len(tr0) and len(va0):
            base0 = base_rate_logloss(F.y[tr0], F.y[va0])
            pids0 = F.problems_of(tr0)
            Ztr, (Zva,) = _design(X[tr0], [X[va0]], False, f"mlp:outer{f}:inner0", pids0)
            record_fit(f"mlp:outer{f}:inner0:classifier", pids0)
            for a in wd_grid:
                lg = _mlp_fit_predict(Ztr, F.y[tr0], [Zva], a, plan.fold_seed * 1000 + f)[0]
                ll = logloss(F.y[va0], expit(lg))
                if ll < best_loss:
                    best_alpha, best_loss = a, ll
        tr, te = F.outer_train(f), F.outer_test(f)
        pids = F.problems_of(tr)
        Ztr, (Zte,) = _design(X[tr], [X[te]], False, f"mlp:outer{f}:final", pids)
        record_fit(f"mlp:outer{f}:final:classifier", pids)
        lg = _mlp_fit_predict(Ztr, F.y[tr], [Zte], best_alpha, plan.fold_seed * 1000 + f)[0]
        scores += scores_from_arrays(data, te, lg, expit(lg), folds=F, model_key=model_key, population=population,
                                     readout="MLP", label_suite=label_suite)
        fits.append(fit_record(model_key, "MLP", label_suite, plan, f,
                               {"layer": l, "weight_decay": best_alpha, "width": K.MLP_PROBE_WIDTH,
                                "selected_on": "first inner split"}, best_loss if np.isfinite(best_loss) else float("nan"), base0))
    return scores, fits
