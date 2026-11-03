"""
SpatialStudio Pro - Main Application Entrypoint and Asynchronous Lifecycle
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("spatialstudio.core")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s under environment '%s'...", settings.APP_NAME, settings.APP_ENV)
    logger.info("Binding ComfyUI worker at: %s", settings.COMFYUI_HOST)
    logger.info("Perceptual Hashing Guardrails active (Hamming threshold: %d)", settings.PHASH_HAMMING_THRESHOLD)
    yield
    logger.info("Shutting down %s gracefully. Closing background workers...", settings.APP_NAME)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Autonomous Social Media Visual Factory and Headless Generative Orchestrator",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "comfyui_endpoint": settings.COMFYUI_HOST,
        "ollama_endpoint": settings.OLLAMA_HOST,
        "guardrails": {
            "phash_threshold": settings.PHASH_HAMMING_THRESHOLD,
            "watermark": settings.WATERMARK_ENABLED
        }
    }
