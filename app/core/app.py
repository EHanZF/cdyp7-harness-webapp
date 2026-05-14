# app/core/app.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.ui import router as ui_router
from app.api.mcp_routes import router as mcp_router
from app.core.diagnostics import router as diagnostics_router


def create_app() -> FastAPI:
    app = FastAPI()

    # API routes
    app.include_router(ui_router)
    app.include_router(mcp_router)
    app.include_router(diagnostics_router)

    # Static UI mount
    app.mount(
        "/ui",
        StaticFiles(directory="app/ui", html=True),
        name="ui",
    )

    return app
