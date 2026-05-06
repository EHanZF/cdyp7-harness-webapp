#!/usr/bin/env python3
import json
from pathlib import Path
from app.core.models import ToolEnvelope, GenerateReleaseSheetToolRequest, ValidateReleaseSheetToolRequest, WriteReceiptToolRequest, FetchArtifactToolRequest, ResolveReplayToolRequest
root = Path(__file__).resolve().parents[2]
call = json.loads((root/'examples/generate-release-sheet.tool-call.json').read_text())
ToolEnvelope(**call)
GenerateReleaseSheetToolRequest(**call['arguments'])
ValidateReleaseSheetToolRequest(artifact_id='srs-artifact-S011-CAT5', validation_profile='system_release_sheet_cat5')
WriteReceiptToolRequest(event_type='x', actor='user@example.com', artifact_id='a', sha256='sha256:'+'a'*64)
FetchArtifactToolRequest(artifact_id='srs-artifact-S011-CAT5')
ResolveReplayToolRequest(run_id='run-local-001', adapter_version='v1.0.0')
print('OK tooling API contract models')
