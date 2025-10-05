from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .core.config import get_settings
from .dependencies.redis import lifespan


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    health_path = f"{settings.api_v1_prefix}/health"

    @app.get("/", tags=["info"])
    async def root() -> dict[str, str]:
        return {
            "message": "Seedr backend is running",
            "docs_url": "/docs",
            "health_url": health_path,
        }

    return app


app = create_app()
