"""
VisionHub FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .storage import ensure_bucket_exists
from .routers import auth, boards

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Personal vision board platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(boards.router)


# Startup event
@app.on_event("startup")
def on_startup():
    """Initialize database and storage on startup"""
    print("🚀 Starting VisionHub...")
    init_db()
    ensure_bucket_exists()
    print("✅ VisionHub ready!")


# Root endpoint
@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "VisionHub API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint for Kubernetes probes"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "database": "connected",
        "storage": "connected"
    }