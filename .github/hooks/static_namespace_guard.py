#!/usr/bin/env python3

import argparse, pathlib, re, sys

TOOL_PATTERNS = [
    r'"tool_name"\s*:\s*"([^"]+)"',
    r'"tool_id"\s*:\s*"([^"]+)"',
    r'name\s*=\s*"([^"]+)"'
]

NAMESPACE = re.compile(r"^cdyp7\.")

def emit(path, line, tool):
    print(f"::error file={path},line={line},title=STATIC_NAMESPACE::Invalid tool '{tool}' (must start with cdyp7.)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    bad = 0
    root = pathlib.Path(args.root)

    for f in root.rglob("*"):
        if not f.is_file():
            continue
        if not any(x in str(f) for x in ["contracts", "mcp", "tools"]):
            continue

        text = f.read_text(errors="ignore")
        for pattern in TOOL_PATTERNS:
            for m in re.finditer(pattern, text):
                tool = m.group(1)
                if not NAMESPACE.match(tool):
                    bad += 1
                    line = text[:m.start()].count("\n") + 1
                    emit(f, line, tool)

    if bad:
        sys.exit(1)

if __name__ == "__main__":
    main()
