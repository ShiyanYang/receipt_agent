"""
Configuration management for Grocery Agent.

Supports three configuration sources (in priority order):
1. Environment variables (highest priority)
2. .env file (if exists)
3. Built-in defaults (lowest priority)

Usage:
    from config import config
    model_path = config.MODEL_PATH
"""

import os
import logging
from pathlib import Path

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use env vars only


class Config:
    """Base configuration with sensible defaults."""
    
    # ============ LLM Settings ============
    MODEL_PATH = os.getenv("MODEL_PATH", "./models/llama-3-8b-instruct.gguf")
    LLM_N_CTX = int(os.getenv("LLM_N_CTX", "2048"))
    LLM_N_THREADS = int(os.getenv("LLM_N_THREADS", "4"))
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
    
    # ============ Data Storage Settings ============
    PANTRY_FILE = os.getenv("PANTRY_FILE", "data/pantry.json")
    MEMORY_FILE = os.getenv("MEMORY_FILE", "memory/conversation.json")
    
    # ============ Logging Settings ============
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ============ Application Settings ============
    APP_NAME = "Grocery Agent"
    APP_VERSION = "1.0.0"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required files/paths exist."""
        if not os.path.exists(cls.MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {cls.MODEL_PATH}")
        
        # Ensure directories exist
        Path("data").mkdir(exist_ok=True)
        Path("memory").mkdir(exist_ok=True)
        
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """Return config as dictionary (for logging/debugging)."""
        return {
            k: v for k, v in cls.__dict__.items()
            if not k.startswith("_") and k.isupper()
        }


class DevelopmentConfig(Config):
    """Development configuration with verbose logging."""
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration with minimal logging."""
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration with small/fast model."""
    MODEL_PATH = os.getenv("MODEL_PATH", "./models/test-tiny.gguf")
    LLM_N_THREADS = 2
    LLM_MAX_TOKENS = 256
    LOG_LEVEL = "DEBUG"


def get_config() -> Config:
    """
    Get appropriate configuration based on environment.
    
    Environment variable: ENV
    - "production" → ProductionConfig
    - "testing" → TestingConfig
    - default → DevelopmentConfig
    """
    env = os.getenv("ENV", "development").lower()
    
    configs = {
        "production": ProductionConfig,
        "prod": ProductionConfig,
        "testing": TestingConfig,
        "test": TestingConfig,
        "development": DevelopmentConfig,
        "dev": DevelopmentConfig,
    }
    
    config_class = configs.get(env, DevelopmentConfig)
    return config_class()


# Default config instance
config = get_config()

# Setup logging with config
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)

logger = logging.getLogger(__name__)
logger.debug(f"Loaded {config.__class__.__name__} configuration")
logger.debug(f"Model: {config.MODEL_PATH}")
logger.debug(f"Log level: {config.LOG_LEVEL}")
