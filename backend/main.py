import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.app.core.config import get_settings
from backend.app.utils.logger import logger
from backend.app.api.health import router as health_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    logger.info(f"Starting {settings.PROJECT_NAME} backend...")
    # Add startup initialization here (e.g. DB connection pooling, ML models loading)
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME} backend...")
    # Add shutdown cleanup here

def create_app() -> FastAPI:
    """
    Application factory to create the FastAPI instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router, prefix=settings.API_V1_STR, tags=["health"])
    
    from backend.app.api import documents, qa, chat, quizzes

    # Register routers
    app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
    app.include_router(qa.router, prefix=f"{settings.API_V1_STR}/qa", tags=["qa"])
    app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
    app.include_router(quizzes.router, prefix=f"{settings.API_V1_STR}/quizzes", tags=["quizzes"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
