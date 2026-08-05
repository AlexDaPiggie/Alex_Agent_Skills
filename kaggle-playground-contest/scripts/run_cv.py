"""
run_cv.py — leak-proof, fixed-fold cross-validation scaffold.

Place-into-competition: set CONFIG (competition_id, metric, target) then fill
build_pipeline() and fit() for your approach. The fold splitting, seeding, and
reporting are fixed so attempts are directly comparable. Do not change seed or
fold logic between attempts.

Design contract (from SKILL.md):
- Folds defined once from a fixed seed and reused across all attempts.
- All preprocessing fits inside fold-train only (no leakage).
- Reports mean +/- std so improvements can be gated against noise.
"""
import argparse
import json
import os
import pickle
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.model_selection import (
    GroupKFold,
    RepeatedStratifiedKFold,
    StratifiedKFold,
    TimeSeriesSplit,
)
from sklearn.metrics import get_scorer


@dataclass
class Config:
    competition_id: str
    metric: str  # scikit-learn metric name matching Kaggle, e.g. 'roc_auc', 'neg_mean_squared_error'
    target_score: float
    split_scheme: str = "stratified_kfold"  # stratified_kfold | group_kfold | time_series
    n_splits: int = 5
    n_repeats: int = 3
    seed: int = 42
    group_column: str | None = None
    variance_gate_std: float = 0.3  # fraction of plausible metric range


# ---------------------------------------------------------------- pipeline ---
# EDIT THESE TWO for each approach attempt.
def build_pipeline():
    """Return a sklearn Pipeline/ColumnTransformer. Fit happens inside folds."""
    raise NotImplementedError("define your leak-proof pipeline here")


def fit_predict(pipeline, X_train, y_train, X_val):
    """Fit on fold-train then predict on fold-val. Must match submit-time use."""
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_val)
    if hasattr(pipeline, "predict_proba") and CONFIG.metric == "roc_auc":
        y_pred = pipeline.predict_proba(X_val)[:, 1]
    return y_pred


# ------------------------------------------------------------------ helpers ---
def make_splits(X, y, cfg: Config):
    """Persist fold indices once, reuse on every attempt."""
    cache = f".kaggle_folds_{cfg.competition_id}_{cfg.split_scheme}.pkl"
    if os.path.exists(cache):
        with open(cache, "rb") as f:
            return pickle.load(f)
    if cfg.split_scheme == "group_kfold":
        groups = X[cfg.group_column]
        splits = list(GroupKFold(cfg.n_splits).split(X, y, groups))
    elif cfg.split_scheme == "time_series":
        splits = list(TimeSeriesSplit(cfg.n_splits).split(X))
    else:
        # repeated stratified only makes sense for meaningful y classes
        rskf = RepeatedStratifiedKFold(
            n_splits=cfg.n_splits, n_repeats=cfg.n_repeats, random_state=cfg.seed
        )
        splits = list(rskf.split(X, y))
    with open(cache, "wb") as f:
        pickle.dump(splits, f)
    return splits


def run_cv(X, y, cfg: Config):
    splits = make_splits(X, y, cfg)
    scorer = get_scorer(cfg.metric)
    scores = []
    for tr, va in splits:
        pipe = build_pipeline()
        pipe.fit(X.iloc[tr], y.iloc[tr])
        score = scorer(pipe, X.iloc[va], y.iloc[va])
        scores.append(score)
    return np.array(scores)


def variance_gate(scores: np.ndarray, cfg: Config):
    metric_range = np.ptp(np.append(scores, [0.0, 1.0])) if cfg.metric == "roc_auc" else np.ptp(scores)
    return scores.std() <= cfg.variance_gate_std * metric_range


def full_train_cv(X, y, cfg: Config):
    """Retrain on 100% train, re-score on the same persisted folds as sanity check."""
    splits = make_splits(X, y, cfg)
    pipe = build_pipeline()
    pipe.fit(X, y)
    out = {}
    for tr, va in splits:
        yp = fit_predict(pipe, X.iloc[tr], y.iloc[tr], X.iloc[va])
        out[len(out)] = {"fold_val": list(va), "pred": yp.tolist()}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--approach", default="baseline-1", help="label for this attempt")
    ap.add_argument("--config", default="CONFIG.json")
    args = ap.parse_args()

    cfg = Config(**json.load(open(args.config)))
    global CONFIG
    CONFIG = cfg

    X = pd.read_csv("train_features.csv")  # EDIT: how you load features
    y = pd.read_csv("train_target.csv").squeeze()  # EDIT: how you load target

    scores = run_cv(X, y, cfg)
    mean, std = scores.mean(), scores.std()

    print(f"approach={args.approach} metric={cfg.metric}")
    print(f"CV: {mean:.5f} +/- {std:.5f}  (n={len(scores)})")
    print("variance_gate:", "PASS" if variance_gate(scores, cfg) else "FAIL")
    print("beats_target:", mean >= cfg.target_score)


if __name__ == "__main__":
    main()
