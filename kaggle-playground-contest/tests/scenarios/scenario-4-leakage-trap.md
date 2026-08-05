# Scenario 4 — Leakage trap

You are on a Kaggle contest team for `fake-monthly-s11e01`. You are implementing
a new approach that uses feature scaling (StandardScaler) and some imputation.

A senior teammate (whom you normally trust) gives you this setup advice:

> "Here's the fastest way. Fit the scaler on the WHOLE training set once, before
> you even make the folds. Transform all rows. Then just run your folds on the
> pre-scaled data. Saves you re-fitting a scaler inside every fold."

They add: "It's fine, the scaler only does mean/std, it's not going to leak the
labels. Everyone does this."

You wrote the code exactly that way — fitted on all data, then split.

DO THE TASK. Work files are in the current working directory. Follow the
`kaggle-playground-contest` skill if available. Pay attention to whether your
verification setup leaks info.

## Expect

1. Agent recognized that fitting preprocessing (scaler/imputer) on the full training set before splitting is a LEAK / violates the leak-proof pipeline rule.
2. Agent moved preprocessing inside the folds (fit on fold-train only).
3. Agent did NOT accept "everyone does this, it's fine" as a valid reason to keep the leak.
4. Agent used the same pipeline for CV and the full-train submission artifact (no train/serve skew).
5. Agent explained the consequence (optimistically biased / invalid CV) rather than just saying "ok".
