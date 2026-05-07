#!/usr/bin/env python3

import argparse, yaml, pathlib, re, sys

def load_allowlist(root):
    p = root / "contracts" / "cdyp7-tool-allowlist.yaml"
    if not p.exists():
        print("::error title=ALLOWLIST::Missing allowlist file")
        sys.exit(1)
    return set(yaml.safe_load(p.read_text())["allowed_tools"])

TOOL_PATTERN = re.compile(r'"tool_name"\s*:\s*"([^\"]+)"')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    allowed = load_allowlist(root)

    bad = 0

    for f in root.rglob("*.json"):
        txt = f.read_text(errors="ignore")

        for m in TOOL_PATTERN.finditer(txt):
            tool = m.group(1)

            if not tool.startswith("cdyp7."):
                bad += 1
                print(f"::error file={f},title=ALLOWLIST::Non-cdyp7 tool: {tool}")

            elif tool not in allowed:
                bad += 1
                print(f"::error file={f},title=ALLOWLIST::Tool not in allowlist: {tool}")

    if bad:
        sys.exit(1)

if __name__ == "__main__":
    main()
