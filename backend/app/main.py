"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import threats, websocket, auth

app = FastAPI(
    title="Sentinel no Yaiba API",
    description="Unified security dashboard for threat intelligence aggregation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(threats.router)
app.include_router(websocket.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Sentinel no Yaiba API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy"
    }

