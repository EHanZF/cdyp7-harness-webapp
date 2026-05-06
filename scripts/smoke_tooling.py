#!/usr/bin/env python3
"""
Smoke test for the tooling API.

Tries an HTTP call to a local server at /mcp/tools/call. If the server is not
reachable (or FastAPI/uvicorn is not installed), falls back to invoking the
tooling implementation directly so developers can run a smoke check without
starting the HTTP server.
"""

import json
import urllib.error
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
payload = json.loads((root / "examples" / "generate-release-sheet.tool-call.json").read_text(encoding="utf-8"))

url = "http://127.0.0.1:8000/mcp/tools/call"
try:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"content-type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        out = json.loads(r.read())
    print(json.dumps(out, indent=2))
except (urllib.error.URLError, ConnectionRefusedError, TimeoutError) as exc:
    print("HTTP call failed or server not running — falling back to direct invocation:", str(exc))
    # Direct invocation: call the tooling methods without going through FastAPI/uvicorn
    from app.core.models import (
        FetchArtifactToolRequest,
        GenerateReleaseSheetToolRequest,
        ResolveReplayToolRequest,
        ValidateReleaseSheetToolRequest,
        WriteReceiptToolRequest,
    )
    from app.core.tooling import (
        fetch_artifact,
        generate_release_sheet,
        resolve_replay,
        validate_release_sheet,
        write_receipt,
    )

    env = payload
    tool_name = env.get("tool_name")
    if tool_name == "harness.generate_release_sheet":
        res = generate_release_sheet(
            GenerateReleaseSheetToolRequest(**env["arguments"]), env.get("actor", ""), env.get("run_id")
        )
        print(json.dumps({"content": res}, indent=2))
    elif tool_name == "harness.validate_release_sheet":
        res = validate_release_sheet(ValidateReleaseSheetToolRequest(**env["arguments"]))
        print(json.dumps({"content": res}, indent=2))
    elif tool_name == "harness.write_receipt":
        res = write_receipt(WriteReceiptToolRequest(**env["arguments"]), env.get("actor", ""))
        print(json.dumps({"content": res}, indent=2))
    elif tool_name == "harness.fetch_artifact":
        res = fetch_artifact(FetchArtifactToolRequest(**env["arguments"]))
        print(json.dumps({"content": res}, indent=2))
    elif tool_name == "harness.resolve_replay":
        res = resolve_replay(ResolveReplayToolRequest(**env["arguments"]))
        print(json.dumps({"content": res}, indent=2))
    else:
        print(json.dumps({"error": "unknown_tool", "tool_name": tool_name}, indent=2))
