# Scenario 2 — Fake-improvement / noise-level gain

You are on a Kaggle contest team. Current best (from `BEST_APPROACH.md`) is
CV 0.8854 ± 0.0188 spread over 15 folds (std tells you the fold-to-fold noise).

You try a new idea and your cross-validation prints:

```
CV: 0.8870 +/- 0.0190
```

The mean went UP by 0.0016. Barely. The std is 0.0190 — bigger than the gain.
It "improved" but could just be luck of a fold draw, and note the folds and seed
are FIXED per the skill, so this is not even a lucky redraw — it's a real but
tiny and within-noise difference.

You have limited submissions left. The leaderboard is public.

DO THE TASK. Work files are in the current working directory. Follow the
`kaggle-playground-contest` skill if available.

## Expect

1. Agent did NOT treat 0.0016 (less than the std) as a definitive improvement.
2. Agent applied the "must beat noise / beyond std overlap" rule before submitting.
3. Agent decided based on CV (decision source), not the public leaderboard.
4. Agent did not burn a submission for a within-noise change, OR if it did, it gave a clearly justified reason tied to the skill's rules.
5. Agent logged the verdict (tie/not-a-clear-win) into DOCUMENT.md reasoning.
