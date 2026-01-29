"""
Configuration settings for Kling AI Clone
"""

import os
from pathlib import Path

class Config:
    # Base directories
    BASE_DIR = Path(__file__).parent
    MODEL_DIR = BASE_DIR / "models_cache"
    OUTPUT_DIR = BASE_DIR / "outputs"
    UPLOAD_DIR = BASE_DIR / "uploads"
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Model settings
    MODEL_TYPE = os.getenv("MODEL_TYPE", "stable-video-diffusion")
    ENABLE_TEXT_TO_VIDEO = True
    ENABLE_IMAGE_TO_VIDEO = True
    
    # Video generation settings
    DEFAULT_NUM_FRAMES = 24
    DEFAULT_FPS = 8
    MAX_VIDEO_LENGTH = 120  # seconds
    DEFAULT_RESOLUTION = (512, 512)
    
    # GPU settings
    USE_GPU = True
    GPU_MEMORY_FRACTION = 0.9
    ENABLE_ATTENTION_SLICING = True
    ENABLE_VAE_SLICING = True
    ENABLE_CPU_OFFLOAD = False  # Set to True for GPUs with <12GB VRAM
    
    # Model paths (Hugging Face)
    MODELS = {
        "stable-video-diffusion": "stabilityai/stable-video-diffusion-img2vid",
        "stable-video-diffusion-xt": "stabilityai/stable-video-diffusion-img2vid-xt",
        "text-to-video": "damo-vilab/text-to-video-ms-1.7b",
        "animatediff": "guoyww/animatediff-motion-adapter-v1-5-2"
    }
    
    # Queue settings
    MAX_QUEUE_SIZE = 10
    MAX_CONCURRENT_JOBS = 1
    
    # File upload settings
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
