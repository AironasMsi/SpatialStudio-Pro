"""
SpatialStudio Pro - Central Configuration and Environment Engine
"""
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "SpatialStudio Pro"
    APP_ENV: str = "production"
    API_PORT: int = 8000
    
    # ComfyUI Headless Farm
    COMFYUI_HOST: str = Field(default="127.0.0.1:8188", description="Target ComfyUI worker endpoint")
    COMFYUI_WS_URL: str = Field(default="ws://127.0.0.1:8188/ws", description="Execution telemetry websocket")
    
    # Local LLM Copilot (Ollama)
    OLLAMA_HOST: str = Field(default="http://127.0.0.1:11434", description="Local Ollama API endpoint")
    OLLAMA_MODEL: str = Field(default="dolphin-llama3:8b", description="Default caption and hashtag generator")
    
    # Computer Vision and Guardrails
    PHASH_HAMMING_THRESHOLD: int = Field(default=6, description="Max Hamming distance to reject duplicates")
    WATERMARK_ENABLED: bool = True
    
    # Meta Graph API Gateway
    META_GRAPH_VERSION: str = "v19.0"
    INSTAGRAM_ACCOUNT_ID: str = Field(default="", description="Instagram Business Account ID")
    META_ACCESS_TOKEN: str = Field(default="", description="Long-lived Meta Graph User/Page token")
    
    # Cloudflare Tunnel
    CLOUDFLARE_TUNNEL_URL: str = Field(default="", description="Public HTTPS tunnel for Meta webhooks")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
