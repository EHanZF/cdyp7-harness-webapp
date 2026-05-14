from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import uuid

from app.memory.ingestion import ingest_document

router = APIRouter(prefix="/ui", tags=["ui"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/ingest")
async def ingest(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        document_id = str(uuid.uuid4())
        path = UPLOAD_DIR / f"{document_id}_{file.filename}"

        with path.open("wb") as f:
            f.write(await file.read())

        stats = await ingest_document(
            document_id=document_id,
            path=path,
            filename=file.filename,
        )

        results.append({
            "document_id": document_id,
            "filename": file.filename,
            **stats,
        })

    return {
        "status": "ok",
        "documents": results,
    }
