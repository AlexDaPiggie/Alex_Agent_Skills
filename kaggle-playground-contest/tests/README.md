# Testing the kaggle-playground-contest skill

This harness verifies the skill end-to-end: does a fresh agent that is given ONLY
the skill document follow its rules under pressure — without any rules restated
inline in the scenario?

## Principle

A pressure scenario describes a stressful situation with no rule hints. When the
skill's actual content is injected, an agent that applies the rules, and *cites
the skill's own wording* (variance gate, `mean ± std`, Common Mistakes, etc.) to
justify a decision, is following the skill — not the prompt. That is the
evidence we look for.

## Layout

```
tests/
  make_fake_comp.py        calibrated fake competition generator
  build_harness.py         inject SKILL.md into shells -> run/*.prompt.txt
  run_test.py              prints scenario prompts (manual dispatch helper)
  pressure/
    scenario-{1,2,3,4}-shell.txt   bare pressure scenarios (NO rules)
  run/
    <scenario>.prompt.txt          generated: skill + shell, ready to dispatch
  work/
    <scenario>/                    per-scenario fake comp files
  results/                         review logs go here
```

## The 4 scenarios

1. **scenario-1** — time / sunk-cost pressure: unverified idea, almost out of
   submissions. Expect: verify locally (CV) before deciding; do not submit blind.
2. **scenario-2** — fake improvement: +0.0016 mean vs 0.0190 std. Expect: treat
   as a tie (inside noise), decision source = CV not leaderboard.
3. **scenario-3** — spirit-vs-letter: teammate wants a cheap 80/20 split. Expect:
   refuse to substitute; keep fixed folds/seed + full CV as the measurement.
4. **scenario-4** — leakage trap: scaler fit on full data before split. Expect:
   flag as leak, move preprocessing inside folds, question the "it's fine" excuse.

## How to run

```bash
# 1. build the skill-injected prompts
python tests/build_harness.py

# 2. (optional) populate fresh per-scenario work dirs for the file-based scenarios
#    build_harness.py creates the dirs; generate fake comp data into each:
python tests/make_fake_comp.py --out tests/work/scenario-1-shell
python tests/make_fake_comp.py --out tests/work/scenario-2-shell
python tests/make_fake_comp.py --out tests/work/scenario-3-shell
python tests/make_fake_comp.py --out tests/work/scenario-4-shell

# 3. dispatch each tests/run/<scenario>.prompt.txt to a FRESH agent
#    (subagent with working directory = tests/work/<scenario>), and save its
#    transcript to tests/results/<scenario>.log
```

## Reviewing a result

Score each transcript against the scenario's expectation checklist in
`pressure/` docs (or the table above), and confirm:

- The agent **applies** the rule (behavior).
- The agent **cites the skill's own wording** — proof it loaded SKILL.md rather
  than guessing. Weak signals: rule followed but no reference to the skill document.

## Re-calibrating the fake data

`make_fake_comp.py` sets the target so honest work clears it but noise does not.
This is verified at generation time (prints baseline CV/mean and target). If you
change the generator, re-check: baseline CV should be comfortably below target,
and a real model (RandomForest) should exceed it.

## Notes / known limits

- Subagents may not expose the `skill` tool, so the harness injects SKILL.md as
  text instead of relying on tool-based loading. To test true tool loading, run
  the skill in the main agent context.
- Actual Kaggle upload needs real credentials; the fake comp returns 401. The
  skill's submit step is exercised; the auth/poll path is not.
