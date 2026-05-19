import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.api.routes import router as api_router
from app.api.mcp_routes import router as mcp_router
from app.api.memory_routes import router as memory_router
from app.api.dashboard import router as dashboard_router

from app.core.config import assert_adapter, load_adapter


# ✅ Create app FIRST
app = FastAPI(
    title="CDYP7 Runtime Harness Tooling API",
    version="1.2.0",
)


# ✅ THEN add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Safety guard (production)
if os.getenv("ENV") == "production":
    required = ["AZURE_STORAGE_ACCOUNT_URL"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required Azure config: {missing}")


# ✅ Load adapter correctly
adapter = load_adapter()
assert_adapter(adapter)
app.state.adapter = adapter


# ✅ Register routers
app.include_router(api_router)
app.include_router(mcp_router)
app.include_router(memory_router)
app.include_router(dashboard_router)


# ✅ Static setup
STATIC = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")


# ✅ Root endpoint serves UI
@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")
