<<<<<<< HEAD
import hashlib
import json
import uuid
from datetime import datetime, timezone

from app.core.config import settings
from app.core.storage import blob_store


def _hash(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def append_receipt(
    event_type: str,
    actor: str,
    artifact_id: str | None = None,
    artifact_uri: str | None = None,
    artifact_sha256: str | None = None,
    metadata: dict | None = None,
) -> dict:
    event = {
        "receipt_id": "rcpt-" + uuid.uuid4().hex,
        "event_type": event_type,
        "actor": actor,
        "artifact_id": artifact_id,
        "artifact_uri": artifact_uri,
        "artifact_sha256": artifact_sha256,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    event["event_hash"] = _hash(event)
    event["receipt_hash"] = _hash({"receipt_id": event["receipt_id"], "event_hash": event["event_hash"]})
    blob_name = f"{event['receipt_id']}.json"
    stored = blob_store.upload_bytes(
        settings.receipts_container,
        blob_name,
        json.dumps(event, indent=2).encode("utf-8"),
        overwrite=False,
        content_type="application/json",
    )
    return {
        "receipt_id": event["receipt_id"],
        "receipt_blob_uri": stored.blob_uri,
        "event_type": event_type,
        "receipt_hash": event["receipt_hash"],
        "event_hash": event["event_hash"],
    }
=======
from datetime import datetime, timezone
import json, uuid, hashlib
from app.core.storage import blob_store
from app.core.config import settings

def _hash(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return 'sha256:' + hashlib.sha256(payload.encode('utf-8')).hexdigest()

def append_receipt(event_type: str, actor: str, artifact_id: str | None = None, artifact_uri: str | None = None, artifact_sha256: str | None = None, metadata: dict | None = None) -> dict:
    event = {
        'receipt_id': 'rcpt-' + uuid.uuid4().hex,
        'event_type': event_type,
        'actor': actor,
        'artifact_id': artifact_id,
        'artifact_uri': artifact_uri,
        'artifact_sha256': artifact_sha256,
        'metadata': metadata or {},
        'created_at': datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    }
    event['event_hash'] = _hash(event)
    event['receipt_hash'] = _hash({'receipt_id': event['receipt_id'], 'event_hash': event['event_hash']})
    blob_name = f"{event['receipt_id']}.json"
    stored = blob_store.upload_bytes(settings.receipts_container, blob_name, json.dumps(event, indent=2).encode('utf-8'), overwrite=False, content_type='application/json')
    return {'receipt_id': event['receipt_id'], 'receipt_blob_uri': stored.blob_uri, 'event_type': event_type, 'receipt_hash': event['receipt_hash'], 'event_hash': event['event_hash']}
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
