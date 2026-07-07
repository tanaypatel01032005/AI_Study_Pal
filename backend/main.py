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
    description = """
    **AI Study Pal API** provides a powerful backend for managing educational documents, generating insights, quizzes, and study plans using LLMs.
    
    ## Features
    * **Documents**: Upload and summarize educational documents.
    * **QA & Chat**: Interactive chat and RAG pipeline for document querying.
    * **Quizzes & Flashcards**: Auto-generate assessments and flashcards.
    * **Insights**: Get AI-powered analytics on learning progress.
    """
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=description,
        version="2.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        contact={
            "name": "AI Study Pal Admin",
            "url": "https://github.com/tanaypatel01032005",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
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
    
    from backend.app.api import documents, qa, chat, quizzes, flashcards, study_plans, insights

    # Register routers
    app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
    app.include_router(qa.router, prefix=f"{settings.API_V1_STR}/qa", tags=["qa"])
    app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
    app.include_router(quizzes.router, prefix=f"{settings.API_V1_STR}/quizzes", tags=["quizzes"])
    app.include_router(flashcards.router, prefix=f"{settings.API_V1_STR}/flashcards", tags=["flashcards"])
    app.include_router(study_plans.router, prefix=f"{settings.API_V1_STR}/study-plans", tags=["study-plans"])
    app.include_router(insights.router, prefix=f"{settings.API_V1_STR}/insights", tags=["insights"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
