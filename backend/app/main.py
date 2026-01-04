from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .storage import ensure_bucket_exists
from .routers import auth, boards

settings = get_settings()

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
    print("Starting VisionHub...")
    init_db()
    ensure_bucket_exists()
    print("VisionHub ready!")


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