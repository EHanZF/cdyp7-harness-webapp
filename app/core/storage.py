from pathlib import Path
from dataclasses import dataclass
from app.core.config import settings, ROOT

@dataclass
class StoredBlob:
    blob_uri: str
    blob_name: str
    size: int

class BlobStore:
    def __init__(self):
        self.local_root = ROOT
        self.use_azure = bool(settings.storage_account_url)
        self._service = None
        if self.use_azure:
            from azure.identity import DefaultAzureCredential
            from azure.storage.blob import BlobServiceClient
            self._service = BlobServiceClient(account_url=settings.storage_account_url, credential=DefaultAzureCredential())

    def upload_bytes(self, container: str, blob_name: str, data: bytes, overwrite: bool = False, content_type: str | None = None) -> StoredBlob:
        if self.use_azure:
            cc = self._service.get_container_client(container)
            try:
                cc.create_container()
            except Exception:
                pass
            bc = cc.get_blob_client(blob_name)
            bc.upload_blob(data, overwrite=overwrite, content_settings=None)
            return StoredBlob(blob_uri=bc.url, blob_name=blob_name, size=len(data))
        path = self.local_root / container / blob_name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not overwrite:
            raise FileExistsError(f'Blob already exists and overwrite=false: {container}/{blob_name}')
        path.write_bytes(data)
        return StoredBlob(blob_uri=f'file://{container}/{blob_name}', blob_name=blob_name, size=len(data))

    def read_bytes(self, container: str, blob_name: str) -> bytes:
        if self.use_azure:
            return self._service.get_blob_client(container, blob_name).download_blob().readall()
        return (self.local_root / container / blob_name).read_bytes()

    def exists(self, container: str, blob_name: str) -> bool:
        if self.use_azure:
            return self._service.get_blob_client(container, blob_name).exists()
        return (self.local_root / container / blob_name).exists()

blob_store = BlobStore()
