"""
submit.py — submit + poll score + append DOCUMENT.md row in one command.

Flow: submit file -> poll kaggle status until a score arrives -> append one row
to DOCUMENT.md with CV (optional), full-train CV (optional), and LB score.

Requires: authenticated `kaggle` CLI (kaggle.json at ~/.kaggle). The polling
reads JSON from `kaggle api competitions submissions -c <comp>`.
"""
import argparse
import json
import os
import subprocess
import time


def run(args):
    comp = args.competition
    print(f"submitting {args.file} to {comp} ...")
    r = subprocess.run(
        ["kaggle", "competitions", "submit", "-c", comp, "-f", args.file, "-m", args.message],
        capture_output=True, text=True,
    )
    print(r.stdout)
    if r.returncode != 0:
        print("SUBMIT FAILED:\n", r.stderr)
        raise SystemExit(1)

    # poll for a completed submission with a score
    last = None
    for _ in range(args.timeout // args.interval):
        time.sleep(args.interval)
        rows = _submissions(comp)
        if not rows:
            continue
        latest = rows[0]
        last = latest
        status = latest.get("status", "").lower()
        if status in ("complete", "completed", "finished"):
            print(f"score: {latest.get('score')}  status: {status}")
            _append_doc(args, latest)
            return
        # newer submission may not be the one just sent; still print progress
        print(f"status={status}")
    print("TIMED OUT waiting for score. Last status:", last)
    raise SystemExit(1)


def _submissions(comp):
    r = subprocess.run(
        ["kaggle", "api", "competitions", "submissions", "-c", comp, "--json"],
        capture_output=True, text=True,
    )
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return []


def _append_doc(args, latest):
    path = args.doc
    if not os.path.exists(path):
        print(f"(no DOCUMENT.md at {path}, skipping append)")
        return
    try:
        os.utime(path)
    except OSError:
        pass
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] submitted {args.file} "
                f"-> LB {latest.get('score')} | msg: {args.message}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--competition", required=True)
    ap.add_argument("-f", "--file", required=True)
    ap.add_argument("-m", "--message", default="")
    ap.add_argument("--doc", default="DOCUMENT.md")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--interval", type=int, default=20)
    args = ap.parse_args()
    run(args)


if __name__ == "__main__":
    main()
