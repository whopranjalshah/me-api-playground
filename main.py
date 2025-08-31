import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from app.database import create_tables
from app.routers import profile, query, health, auth

# Configure logging with better formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("pranjal_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with proper error handling"""
    try:
        logger.info("Starting up Pranjal API")
        create_tables()
        logger.info("Database tables created successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        logger.info("Shutting down Pranjal API")

# Get environment variables with defaults
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
TRUSTED_HOSTS = os.getenv("TRUSTED_HOSTS", "localhost,127.0.0.1").split(",")
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="Pranjal Candidate Profile API",
    description="A comprehensive FastAPI application for managing candidate profiles with authentication and advanced querying capabilities",
    version="2.0.0",
    lifespan=lifespan,
    debug=DEBUG_MODE,
    docs_url="/docs" if DEBUG_MODE else None,
    redoc_url="/redoc" if DEBUG_MODE else None
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=TRUSTED_HOSTS
)

# CORS middleware with improved configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

# Health check endpoint at root
@app.get("/", tags=["root"])
async def root() -> Dict[str, Any]:
    """Root endpoint providing API information"""
    return {
        "message": "Welcome to Pranjal Candidate Profile API",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs" if DEBUG_MODE else "Documentation disabled in production"
    }

# Include routers with better organization
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

app.include_router(
    profile.router,
    prefix="/api/v1",
    tags=["profiles"]
)

app.include_router(
    query.router,
    prefix="/api/v1",
    tags=["queries"]
)

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["health"]
)

# Add API versioning endpoint
@app.get("/api/version", tags=["version"])
async def get_api_version() -> Dict[str, str]:
    """Get API version information"""
    return {
        "api_version": "2.0.0",
        "api_name": "Pranjal Candidate Profile API"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting Pranjal API server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )