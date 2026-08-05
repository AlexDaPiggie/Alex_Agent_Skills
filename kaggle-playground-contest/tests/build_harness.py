"""
build_harness.py — inject the real SKILL.md into each pressure scenario and
write final dispatch prompts.

The goal is an end-to-end test of skill LOAD + APPLICATION: a fresh agent is
given ONLY the skill document (as its guidance) plus a bare pressure scenario.
No rules are restated inline in the scenario, so if the agent follows them, it
is following the skill, not the prompt.

Outputs: <scenario>.prompt.txt in tests/run/. These are then dispatched to a
fresh subagent with its working directory set, and transcripts reviewed against
the expectation checklist in the scenario authoring docs.
"""
import argparse
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(BASE, "SKILL.md")
PRESSURE = os.path.join(BASE, "tests", "pressure")
RUN = os.path.join(BASE, "tests", "run")
WORKBASE = os.path.join(BASE, "tests", "work")

PREAMBLE = """You are a fresh autonomous agent. The following document describes
a skill you should follow. Read it fully and apply it to the task below. Do not
skip, trim, or replace it with your own judgment — the skill is authoritative
where it applies.

===== BEGIN SKILL DOCUMENT =====
{skill}
===== END SKILL DOCUMENT =====

""" + "=" * 66 + "\nTASK\nyou are:\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    os.makedirs(RUN, exist_ok=True)
    with open(SKILL, encoding="utf-8") as f:
        skill = f.read()

    for name in os.listdir(PRESSURE):
        if not name.endswith("_shell.txt") and not name.endswith("-shell.txt"):
            continue
        if args.only and args.only not in name:
            continue
        shell_path = os.path.join(PRESSURE, name)
        with open(shell_path, encoding="utf-8") as f:
            shell = f.read()
        workdir = os.path.join(WORKBASE, name.replace(".txt", ""))
        os.makedirs(workdir, exist_ok=True)
        shell = shell.replace("<WORKDIR>", workdir)
        prompt = PREAMBLE.format(skill=skill) + shell + "\n"
        out = os.path.join(RUN, name.replace(".txt", ".prompt.txt"))
        with open(out, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
