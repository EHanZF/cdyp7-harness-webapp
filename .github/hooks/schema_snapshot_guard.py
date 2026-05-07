#!/usr/bin/env python3

import argparse, hashlib, pathlib, sys

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    schemas = root / "schemas"
    snap = schemas / ".snapshot"

    if not snap.exists():
        print("::warning::No snapshot file")
        return

    expected = snap.read_text().strip()

    combined = ""
    for f in sorted(schemas.glob("*.json")):
        combined += sha(f)

    current = hashlib.sha256(combined.encode()).hexdigest()

    if current != expected:
        print("::error title=SCHEMA_SNAPSHOT::Schema drift detected")
        sys.exit(1)

if __name__ == "__main__":
    main()
