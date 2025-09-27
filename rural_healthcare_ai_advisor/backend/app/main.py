from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.routes import api_router
from .config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Rural Healthcare AI Advisor",
        version="0.1.0",
        description=(
            "Provides first-level medical guidance for rural communities. "
            "Disclaimer: This app provides preliminary advice only and does not replace professional diagnosis."
        ),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")
    return app


app = create_app()

