"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeatherData(BaseModel):
    """Weather data model"""
    city: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: float
    description: str
    icon: str
    wind_speed: float
    country: str
    timestamp: Optional[str] = None
    
class WeatherResponse(BaseModel):
    """API response for weather data"""
    success: bool
    data: Optional[WeatherData] = None
    error: Optional[str] = None

class SaveWeatherRequest(BaseModel):
    """Request model for saving weather data"""
    city: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: float
    description: str
    icon: str
    wind_speed: float
    country: str

class HistoryResponse(BaseModel):
    """Response model for historical weather data"""
    success: bool
    data: Optional[list] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    timestamp: str
