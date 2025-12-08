"""
Configuration module for loading environment variables
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Weather API
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5")
    
    # Google Sheets
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    GOOGLE_CREDENTIALS_JSON = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON", "{}"))
    
    # Server
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
    
    @classmethod
    def validate(cls):
        """Validate that all required config values are present"""
        if not cls.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is not set in .env file")
        if not cls.GOOGLE_SHEET_ID:
            raise ValueError("GOOGLE_SHEET_ID is not set in .env file")
        if not cls.GOOGLE_CREDENTIALS_JSON:
            raise ValueError("GOOGLE_CREDENTIALS_JSON is not set in .env file")
        return True

# Validate configuration on import (commented out to make it optional)
# Config.validate()
