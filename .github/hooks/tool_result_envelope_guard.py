#!/usr/bin/env python3

import argparse, json, pathlib, sys

FORBIDDEN = [
    "authority",
    "authority_override",
    "policy_override",
    "receipt_override",
    "promoted",
    "release_authorized",
]

REQUIRED_KEYS = {"ok", "result", "receipt_backed", "authority_effect", "promotion_gate"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    args = p.parse_args()

    bad = 0

    for f in pathlib.Path(args.root).rglob("*.json"):
        try:
            data = json.loads(f.read_text())
        except:
            continue

        if not isinstance(data, dict):
            continue

        keys = set(data.keys())

        # enforce structure
        if keys & set(FORBIDDEN):
            bad += 1
            print(f"::error file={f},title=ENVELOPE::Forbidden authority field detected")

        if "result" in data:
            if not REQUIRED_KEYS.issubset(keys):
                bad += 1
                print(f"::error file={f},title=ENVELOPE::Missing required envelope keys")

            if data.get("authority_effect") != "none":
                bad += 1
                print(f"::error file={f},title=ENVELOPE::Authority escalation detected")

    if bad:
        sys.exit(1)

if __name__ == "__main__":
    main()
