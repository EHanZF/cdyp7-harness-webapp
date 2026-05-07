#!/usr/bin/env python3

import argparse, pathlib, sys

FORBIDDEN = [
    "learn.microsoft.com",
    "docs.aws.amazon.com",
    "developer.mozilla.org",
]

RUNTIME_DIRS = ["mcp", "packages", "apps", "scripts", "contracts"]

def is_runtime(path):
    return any(part in RUNTIME_DIRS for part in path.parts)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    args = p.parse_args()

    bad = 0

    for f in pathlib.Path(args.root).rglob("*"):
        if not f.is_file():
            continue

        txt = f.read_text(errors="ignore")

        if not is_runtime(f):
            # Allow docs/tests
            continue

        for ref in FORBIDDEN:
            if ref in txt:
                bad += 1
                print(f"::error file={f},title=FORBIDDEN_REFERENCE::Runtime code must not depend on {ref}")

    if bad:
        sys.exit(1)

if __name__ == "__main__":
    main()
