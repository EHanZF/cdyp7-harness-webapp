#!/usr/bin/env python3

import argparse, pathlib, re, sys

BLOCK_FIELDS = [
    r'"policy_override"',
    r'"receipt_override"',
    r'"authority_override"'
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    args = p.parse_args()

    bad = 0

    for f in pathlib.Path(args.root).rglob("*"):
        if not f.is_file():
            continue

        txt = f.read_text(errors="ignore")

        for pattern in BLOCK_FIELDS:
            if re.search(pattern, txt):
                bad += 1
                print(f"::error file={f},title=POLICY_OVERRIDE::Forbidden field detected")

    if bad:
        sys.exit(1)

if __name__ == "__main__":
    main()
