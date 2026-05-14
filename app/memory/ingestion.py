from app.core.settings import settings
from app.memory.vector_store import upsert_embeddings


async def ingest_document(*, namespace: str, document_id: str, text: str):
    upsert_embeddings(
        namespace=namespace,
        document_id=document_id,
        chunks=[text],
        embeddings=[[0.0]],
    )

    return {
        "namespace": namespace,
        "document_id": document_id,
        "chunks": 1,
    }
