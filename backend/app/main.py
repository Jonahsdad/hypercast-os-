from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.forecasts import router as forecasts_router
from .config import get_settings
from .logging_config import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Starting %s in %s mode", settings.app_name, settings.app_env)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("Shutting down %s", settings.app_name)


app.include_router(forecasts_router)


@app.get("/", tags=["meta"])
async def root() -> dict[str, str]:
    return {"message": "Hypercast OS API", "docs": "/docs"}
