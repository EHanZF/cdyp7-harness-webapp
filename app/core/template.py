from pathlib import Path

from pydantic import BaseModel

from app.core.config import ROOT
from app.core.hashing import sha256_bytes, sha256_file
from app.core.storage import blob_store


class TemplateStatus(BaseModel):
    ok: bool
    error: str | None = None
    path: str | None = None
    data: bytes | None = None


def validate_template_ref(template_ref) -> TemplateStatus:
    try:
        uri = template_ref.uri
        if uri.startswith("file://"):
            raw = uri.replace("file://", "", 1)
            p = Path(raw)
            if not p.is_absolute():
                p = ROOT / raw
            if not p.exists():
                return TemplateStatus(ok=False, error=f"Template not found: {p}")
            actual = sha256_file(p)
            if actual != template_ref.sha256:
                return TemplateStatus(ok=False, error="Template hash did not match template_ref.sha256.")
            return TemplateStatus(ok=True, path=str(p), data=p.read_bytes())
        if uri.startswith("blob://"):
            _, rest = uri.split("blob://", 1)
            container, blob_name = rest.split("/", 1)
            data = blob_store.read_bytes(container, blob_name)
            if sha256_bytes(data) != template_ref.sha256:
                return TemplateStatus(ok=False, error="Template hash did not match template_ref.sha256.")
            tmp = ROOT / "outputs" / "template-runtime.docx"
            tmp.parent.mkdir(exist_ok=True)
            tmp.write_bytes(data)
            return TemplateStatus(ok=True, path=str(tmp), data=data)
        return TemplateStatus(ok=False, error="Unsupported template URI. Use file:// or blob://")
    except Exception as exc:
        return TemplateStatus(ok=False, error=str(exc))
