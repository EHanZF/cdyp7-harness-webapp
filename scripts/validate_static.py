#!/usr/bin/env python3
import json
from pathlib import Path

import yaml

from app.core.hashing import sha256_file

root = Path(__file__).resolve().parents[1]
adapter = yaml.safe_load((root / "config/runtime-adapter.yaml").read_text())
assert adapter["tools"]["namespace"] == "harness"
assert adapter["tools"]["mode"] == "strict"
assert adapter["tools"]["on_violation"] == "fail_closed"
assert adapter["tools"]["exposed"] == [
    "harness.generate_release_sheet",
    "harness.validate_release_sheet",
    "harness.write_receipt",
    "harness.fetch_artifact",
    "harness.resolve_replay",
]
for key in [
    "approve_release",
    "infer_missing_values",
    "sign_for_approvers",
    "commit_directly_to_repository",
    "bypass_hitl",
    "mutate_source_systems",
]:
    assert adapter["release_sheet_generator"][key] is False
text = json.dumps(adapter).lower()
assert "jira" not in text
example = json.loads((root / "examples/generate-release-sheet.tool-call.json").read_text())
assert example["arguments"]["fields"]["template_ref"]["sha256"] == sha256_file(
    root / "templates/system-release-sheet-template.docx"
)
print("OK static tooling API validation")

- script: |
    mkdir -p config/releases
    echo '{"rbacPolicyVersion": "1.0.0", "routerVersion": "1.0.0"}' > config/releases/current.json
    displayName: 'Initialize Mock Config for Validation'
