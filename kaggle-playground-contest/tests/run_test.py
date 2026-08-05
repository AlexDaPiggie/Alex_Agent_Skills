"""run_test.py — dispatch each pressure scenario to a fresh subagent and collect results.

For each scenario prompt in this repo, it:
  1. (re)creates a clean per-scenario work dir from make_fake_comp.py
  2. asks a fresh agent to carry out the task following the kaggle-playground-contest skill
  3. records the agent's full transcript to tests/results/<scenario>.log
  4. prints a short summary of observed behavior

Observed log files are manual-review material: read them and score against the
expectation checklist in each scenario file.
"""
import argparse
import json
import os
import subprocess
import sys

SCENARIOS_DIR = os.path.join(os.path.dirname(__file__), "scenarios")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
WORK_BASE = os.path.join(os.path.dirname(__file__), "work")


def load(key):
    """Return the PER_SCENARIO metadata dict for `key` from the scenario file."""
    path = os.path.join(SCENARIOS_DIR, f"{key}.md")
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    start, end = txt.index("```json"), txt.index("```", 12)
    return json.loads(txt[start + 7:end])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", help="run only this scenario key")
    ap.add_argument("--cwd", default=os.getcwd(), help="agent working directory (default: current)")
    args = ap.parse_args()

    keys = [args.key] if args.key else [f[:-3] for f in os.listdir(SCENARIOS_DIR) if f.endswith(".md")]
    os.makedirs(RESULTS_DIR, exist_ok=True)

    for key in keys:
        meta = load(key)
        workdir = os.path.join(WORK_BASE, key)
        os.makedirs(workdir, exist_ok=True)
        subprocess.run([sys.executable, "make_fake_comp.py", "--out", workdir],
                       cwd=os.path.dirname(__file__), check=True)

        # Agent invocation is handled by the harness (opencode/agent). Here we
        # only emit the prompt to stdout so a caller can pipe it to an agent.
        shell = meta["shell"] if meta.get("shell") else meta["instruction"]
        print("=" * 70)
        print(f"SCENARIO: {key}")
        print(f"WORKDIR: {workdir}")
        print("=" * 70)
        print(shell)
        print("\n--- EXPECTED (review checklist) ---")
        for e in meta["expect"]:
            print(" -", e)


if __name__ == "__main__":
    main()
