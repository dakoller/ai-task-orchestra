"""Main application module for AI Task Orchestra."""

import logging
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from ai_task_orchestra import __version__
from ai_task_orchestra.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="AI Task Orchestra",
    description="Task scheduling and execution platform for self-hosted AI environments",
    version=__version__,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom OpenAPI schema
def custom_openapi() -> Dict:
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add custom schema components here if needed
    # openapi_schema["components"]["schemas"]["Task"] = {...}

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore


@app.get("/")
async def root() -> Dict:
    """Root endpoint returning API information."""
    return {
        "name": "AI Task Orchestra API",
        "version": __version__,
        "status": "running",
    }


@app.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "healthy"}


# Import and include API routers
# This is placed here to avoid circular imports
from ai_task_orchestra.api.v1.router import api_router
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ai_task_orchestra.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
