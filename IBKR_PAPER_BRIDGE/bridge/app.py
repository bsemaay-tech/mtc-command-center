"""FastAPI application factory for Crypto Paper Bridge."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from bridge.api.routes import init_runtime_state, install_routes
from bridge.api.ws import install_ws

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Crypto Paper Bridge starting")
    yield
    logger.info("Crypto Paper Bridge shutting down")


def create_app() -> FastAPI:
    """Build an import-safe FastAPI app without exchange or LLM calls."""
    app = FastAPI(
        title="Crypto Paper Bridge",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:8790", "http://localhost:8790"],
        allow_methods=["GET", "POST", "PUT"],
        allow_headers=["X-Confirm", "Content-Type"],
    )
    init_runtime_state(app)
    install_routes(app)
    install_ws(app)

    static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return (static_dir / "index.html").read_text(encoding="utf-8")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("bridge.app:app", host="127.0.0.1", port=8790, reload=False)
