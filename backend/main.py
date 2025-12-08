"""
FastAPI application for Weather + Google Sheets integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from pathlib import Path
from models import (
    WeatherResponse, 
    SaveWeatherRequest, 
    HistoryResponse,
    HealthResponse
)
from services.weather_service import weather_service
from services.sheets_service import sheets_service

# Import authentication
from auth_routes import router as auth_router
from auth import get_current_user
from auth_models import User
from fastapi import Depends

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

# Include authentication routes
app.include_router(auth_router)

# Get frontend directory path (one level up from backend)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

@app.get("/")
async def root():
    """Serve frontend login page as default"""
    login_file = FRONTEND_DIR / "login.html"
    if login_file.exists():
        return FileResponse(login_file)
    # Fallback to index if login doesn't exist yet
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "message": "WeatherPro API with Authentication",
        "version": "2.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "health": "/api/health",
            "weather": "/api/weather/{city}",
            "save": "/api/weather/save",
            "history": "/api/weather/history"
        }
    }

# Serve frontend HTML pages
@app.get("/{page_name}.html")
async def serve_page(page_name: str):
    """Serve frontend HTML pages"""
    page_file = FRONTEND_DIR / f"{page_name}.html"
    if page_file.exists():
        return FileResponse(page_file)
    raise HTTPException(status_code=404, detail="Page not found")

# Serve CSS files
@app.get("/{file_name}.css")
async def serve_css(file_name: str):
    """Serve CSS files"""
    css_file = FRONTEND_DIR / f"{file_name}.css"
    if css_file.exists():
        return FileResponse(css_file, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

# Serve JavaScript files
@app.get("/{file_name}.js")
async def serve_js(file_name: str):
    """Serve JavaScript files"""
    js_file = FRONTEND_DIR / f"{file_name}.js"
    if js_file.exists():
        return FileResponse(js_file, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JS file not found")

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is running",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/weather/save")
async def save_weather(
    request: SaveWeatherRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Save weather data to Google Sheets (Protected - Requires Login)
    
    Args:
        request: Weather data to save
        current_user: Current logged-in user
        
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
async def get_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """
    Get historical weather data from Google Sheets (Protected - Requires Login)
    
    Args:
        limit: Maximum number of records to return (default: 50)
        current_user: Current logged-in user
        
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
async def get_weather(
    city: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get current weather for a city (Protected - Requires Login)
    
    Args:
        city: City name (e.g., "Mumbai", "London")
        current_user: Current logged-in user
        
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
