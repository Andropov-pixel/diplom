from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time
import os
from typing import Any, List

from app.api import auth, servers, monitoring, reports, users
from app.core.config import settings
from app.db.session import async_engine, get_db
from app.db.base import Base
from app.services.telegram_bot import TelegramBotService
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.dependencies import get_current_user, get_current_superuser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Global telegram bot instance
telegram_bot = TelegramBotService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan management for startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting Server Monitoring System...")

    try:
        # Create database tables
        logger.info("Creating database tables...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created successfully")

        # Start Telegram bot
        if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_BOT_TOKEN != "your-telegram-bot-token":
            logger.info("Starting Telegram bot service...")
            await telegram_bot.start()
            logger.info("✅ Telegram bot started successfully")
        else:
            logger.warning("⚠️ Telegram bot token not configured")

    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise

    yield

    # Shutdown
    logger.info("🛑 Shutting down application...")
    try:
        await telegram_bot.stop()
        await async_engine.dispose()
        logger.info("✅ Clean shutdown completed")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Professional Server Monitoring System with Telegram Integration",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(servers.router, prefix=settings.API_V1_STR, tags=["servers"])
app.include_router(monitoring.router, prefix=settings.API_V1_STR, tags=["monitoring"])
app.include_router(reports.router, prefix=settings.API_V1_STR, tags=["reports"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])


# Root endpoints
@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "🚀 Server Monitoring System API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "telegram_bot": "active" if telegram_bot.is_running else "inactive"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Documentation endpoints
@app.get("/docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_ui():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "path": request.url.path},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
#1