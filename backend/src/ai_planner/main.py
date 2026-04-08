"""AI Smart Planner — FastAPI application."""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ai_planner.settings import settings
from ai_planner.routers import tasks
from ai_planner.database import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI Smart Planner starting up")
    init_db()
    yield
    logger.info("AI Smart Planner shutting down")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="An intelligent task management API that uses LLM to structure tasks",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Return error details in the response for easier debugging."""
    logger.exception("unhandled_exception", extra={"path": request.url.path})
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__,
            "path": request.url.path,
        },
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("request_started", extra={"method": request.method, "path": request.url.path})
    t0 = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - t0) * 1000)
    level = logging.ERROR if response.status_code >= 500 else logging.INFO
    logger.log(
        level,
        "request_completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
