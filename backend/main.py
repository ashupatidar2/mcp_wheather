"""
FastAPI application for Weather + Google Sheets integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from models import (
    WeatherResponse, 
    SaveWeatherRequest, 
    HistoryResponse,
    HealthResponse
)
from services.weather_service import weather_service
from services.sheets_service import sheets_service

# Initialize FastAPI app
app = FastAPI(
    title="Weather + Google Sheets API",
    description="API for fetching weather data and storing it in Google Sheets",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Weather + Google Sheets API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "weather": "/api/weather/{city}",
            "save": "/api/weather/save",
            "history": "/api/weather/history"
        }
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is running",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/weather/save")
async def save_weather(request: SaveWeatherRequest):
    """
    Save weather data to Google Sheets
    
    Args:
        request: Weather data to save
        
    Returns:
        Success status
    """
    try:
        # Convert request to dict
        weather_dict = request.dict()
        
        # Save to Google Sheets
        success = sheets_service.save_weather(weather_dict)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save to Google Sheets")
        
        return {
            "success": True,
            "message": "Weather data saved to Google Sheets successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/history", response_model=HistoryResponse)
async def get_history(limit: int = 50):
    """
    Get historical weather data from Google Sheets
    
    Args:
        limit: Maximum number of records to return (default: 50)
        
    Returns:
        List of historical weather records
    """
    try:
        history = sheets_service.get_history(limit=limit)
        
        return HistoryResponse(
            success=True,
            data=history
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    """
    Get current weather for a city
    
    Args:
        city: City name (e.g., "Mumbai", "London")
        
    Returns:
        Weather data
    """
    try:
        weather_data = weather_service.get_weather(city)
        
        if not weather_data:
            raise HTTPException(status_code=404, detail=f"Weather data not found for {city}")
        
        return WeatherResponse(
            success=True,
            data=weather_data
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecast/hourly/{city}")
async def get_hourly_forecast(city: str):
    """
    Get 48-hour hourly forecast for a city
    
    Args:
        city: City name
        
    Returns:
        List of hourly forecast data
    """
    try:
        hourly_data = weather_service.get_hourly_forecast(city)
        
        return {
            "success": True,
            "city": city,
            "data": hourly_data
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecast/daily/{city}")
async def get_daily_forecast(city: str):
    """
    Get 8-day daily forecast for a city
    
    Args:
        city: City name
        
    Returns:
        List of daily forecast data
    """
    try:
        daily_data = weather_service.get_daily_forecast(city)
        
        return {
            "success": True,
            "city": city,
            "data": daily_data
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/geocode/{query}")
async def geocode_location(query: str, limit: int = 5):
    """
    Geocode a location name to get coordinates and details
    
    Args:
        query: Location name
        limit: Max results (default: 5)
        
    Returns:
        List of matching locations
    """
    try:
        locations = weather_service.geocode_location(query, limit)
        
        return {
            "success": True,
            "query": query,
            "data": locations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    from config import Config
    
    uvicorn.run(
        "main:app",
        host=Config.BACKEND_HOST,
        port=Config.BACKEND_PORT,
        reload=True
    )
