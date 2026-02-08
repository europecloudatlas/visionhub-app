import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .storage import ensure_bucket_exists
from .routers import auth, boards

settings = get_settings()
logger = logging.getLogger("uvicorn")

app = FastAPI(
    title=settings.app_name,
    description="Personal vision board platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(boards.router)


@app.on_event("startup")
def on_startup():
    """Initialize database and storage on startup"""
    logger.info("Starting VisionHub...")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # Initialize storage
    try:
        ensure_bucket_exists()
        logger.info("S3 bucket ready")
    except Exception as e:
        logger.error(f"S3 initialization failed: {e}")
        raise
    
    logger.info("VisionHub ready!")


@app.get("/")
def root():
    return {
        "message": "VisionHub API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "database": "connected",
        "storage": "connected"
    }