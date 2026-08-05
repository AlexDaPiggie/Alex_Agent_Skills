# Competition Config

Fill this per competition BEFORE starting. This is the single place model parameters live — never hardcode them into the loop.

## Competition
- **competition_id**: `REPLACE` (e.g. `playground-series-s4e10`)
- **metric**: `REPLACE` (e.g. `roc_auc`, `rmse`, `log_loss`, `accuracy`) — must match Kaggle exactly
- **submission_file**: `REPLACE` (e.g. `submission.csv`)
- **target_score**: `REPLACE` (minimum local/leaderboard score you must surpass)
- **target_buffer**: small margin added above requirement to cover CV->LB variance (e.g. `0.002` for AUC)
- **task**: `classification` | `regression` (drives fold strategy defaults)

## Validation
- **split_scheme**: `stratified_kfold` | `group_kfold` | `time_series`
- **n_splits**: `5`
- **n_repeats**: `3`
- **fixed_seed**: `42` (do not change between attempts)
- **group_column**: `NONE` (only if group_kfold)
- **variance_gate_std**: threshold for step-5 gate, as fraction of plausible metric range (e.g. `0.3`)

## Stop / Budget
- **max_attempts**: `15`
- **no_improvement_stop**: number of consecutive non-improving attempts after which to stop or restore from BEST (e.g. `3`)
- **decision_source**: `cv` (leaderboard is sanity-check only)

## Submission
- **message_prefix**: `<comp>-attempt-<n>-cv<cv>-lb<lb>` (leave placeholder tokens)
