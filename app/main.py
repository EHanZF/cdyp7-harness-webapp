import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.mcp_routes import router as mcp_router
from app.api.routes import router
from app.core.config import assert_adapter, load_adapter

# Safety guard: in production we require Azure storage to be configured so the
# service cannot accidentally fall back to local filesystem for artifacts.
if os.getenv("ENV") == "production":
    required = ["AZURE_STORAGE_ACCOUNT_URL"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required Azure config: {missing}")

app = FastAPI(title="CDYP7 Runtime Harness Tooling API", version="1.0.0")
adapter = load_adapter()
assert_adapter(adapter)
app.state.adapter = adapter
app.include_router(router)
app.include_router(mcp_router)
STATIC = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")
