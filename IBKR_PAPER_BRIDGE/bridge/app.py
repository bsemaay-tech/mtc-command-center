"""FastAPI application factory for Crypto Paper Bridge."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup and shutdown lifecycle."""
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

    @app.get("/api/status")
    async def get_status() -> dict[str, str]:
        return {"status": "ok", "mode": "paper", "network": "testnet"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("bridge.app:app", host="127.0.0.1", port=8790, reload=False)
