"""
Weather API service for fetching weather data from OpenWeatherMap
"""
import requests
from typing import Optional, Dict
from config import Config
from models import WeatherData

class WeatherService:
    """Service for interacting with OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_API_BASE_URL
    
    def get_weather(self, city: str) -> Optional[WeatherData]:
        """
        Fetch current weather data for a city
        
        Args:
            city: City name (e.g., "Mumbai", "London")
            
        Returns:
            WeatherData object or None if error
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response into WeatherData model
            weather_data = WeatherData(
                city=data["name"],
                temperature=round(data["main"]["temp"], 1),
                feels_like=round(data["main"]["feels_like"], 1),
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                description=data["weather"][0]["description"].title(),
                icon=data["weather"][0]["icon"],
                wind_speed=round(data["wind"]["speed"], 1),
                country=data["sys"]["country"]
            )
            
            return weather_data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"City '{city}' not found")
            raise Exception(f"Weather API error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid API response format: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

# Singleton instance
weather_service = WeatherService()
