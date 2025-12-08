"""
Open-Meteo Weather Service - FREE, No API Key Required!
Supports villages and small locations via coordinates
"""
import requests
from typing import Optional, Dict, List
from datetime import datetime
from backend.models import WeatherData

class OpenMeteoService:
    """Service for Open-Meteo API (Free, unlimited)"""
    
    def __init__(self):
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://photon.komoot.io/api/"
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
    
    def geocode_location(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Geocode location using Photon (supports villages!)
        
        Args:
            query: Location name (city, village, etc.)
            limit: Max results
            
        Returns:
            List of locations with coordinates
        """
        try:
            # Try Photon first (better for villages)
            params = {
                "q": query,
                "limit": limit
            }
            
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            locations = []
            
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                coords = feature.get("geometry", {}).get("coordinates", [])
                
                if len(coords) >= 2:
                    locations.append({
                        "name": props.get("name", "Unknown"),
                        "country": props.get("country", ""),
                        "state": props.get("state", ""),
                        "lat": coords[1],
                        "lon": coords[0],
                        "type": props.get("type", "location")
                    })
            
            # Fallback to Nominatim if Photon fails
            if not locations:
                locations = self._nominatim_geocode(query, limit)
            
            return locations
            
        except Exception as e:
            # Try Nominatim as backup
            return self._nominatim_geocode(query, limit)
    
    def _nominatim_geocode(self, query: str, limit: int) -> List[Dict]:
        """Backup geocoding with Nominatim"""
        try:
            params = {
                "q": query,
                "format": "json",
                "limit": limit
            }
            headers = {
                "User-Agent": "WeatherApp/1.0"
            }
            
            response = requests.get(self.nominatim_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            locations = []
            
            for item in data:
                locations.append({
                    "name": item.get("display_name", "").split(",")[0],
                    "country": item.get("display_name", "").split(",")[-1].strip(),
                    "state": "",
                    "lat": float(item.get("lat", 0)),
                    "lon": float(item.get("lon", 0)),
                    "type": item.get("type", "location")
                })
            
            return locations
            
        except Exception as e:
            raise Exception(f"Geocoding failed: {str(e)}")
    
    def get_weather(self, city: str) -> Optional[WeatherData]:
        """
        Get current weather for any location (including villages!)
        
        Args:
            city: City/village name
            
        Returns:
            WeatherData object
        """
        try:
            # First geocode to get coordinates
            locations = self.geocode_location(city, limit=1)
            if not locations:
                raise ValueError(f"Location '{city}' not found")
            
            location = locations[0]
            lat = location["lat"]
            lon = location["lon"]
            
            # Get weather from Open-Meteo
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,pressure_msl",
                "timezone": "auto"
            }
            
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data.get("current", {})
            
            # Map weather code to description
            weather_code = current.get("weather_code", 0)
            description = self._get_weather_description(weather_code)
            icon = self._get_weather_icon(weather_code)
            
            weather_data = WeatherData(
                city=location["name"],
                temperature=round(current.get("temperature_2m", 0), 1),
                feels_like=round(current.get("apparent_temperature", 0), 1),
                humidity=current.get("relative_humidity_2m", 0),
                pressure=current.get("pressure_msl", 0),
                description=description,
                icon=icon,
                wind_speed=round(current.get("wind_speed_10m", 0), 1),
                country=location.get("country", "")
            )
            
            return weather_data
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to fetch weather: {str(e)}")
    
    def get_hourly_forecast(self, city: str) -> List[Dict]:
        """Get 48-hour forecast"""
        try:
            locations = self.geocode_location(city, limit=1)
            if not locations:
                raise ValueError(f"Location '{city}' not found")
            
            location = locations[0]
            
            params = {
                "latitude": location["lat"],
                "longitude": location["lon"],
                "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m",
                "timezone": "auto",
                "forecast_days": 2
            }
            
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hourly = data.get("hourly", {})
            
            forecast = []
            times = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            humidity = hourly.get("relative_humidity_2m", [])
            feels_like = hourly.get("apparent_temperature", [])
            pop = hourly.get("precipitation_probability", [])
            weather_codes = hourly.get("weather_code", [])
            wind = hourly.get("wind_speed_10m", [])
            
            for i in range(min(48, len(times))):
                dt = datetime.fromisoformat(times[i].replace('Z', '+00:00'))
                forecast.append({
                    "dt": int(dt.timestamp()),
                    "time": dt.strftime("%I:%M %p"),
                    "date": dt.strftime("%a, %b %d"),
                    "temp": round(temps[i], 1),
                    "feels_like": round(feels_like[i], 1),
                    "humidity": humidity[i],
                    "description": self._get_weather_description(weather_codes[i]),
                    "icon": self._get_weather_icon(weather_codes[i]),
                    "pop": pop[i] if i < len(pop) else 0,
                    "wind_speed": round(wind[i], 1)
                })
            
            return forecast
            
        except Exception as e:
            raise Exception(f"Failed to get hourly forecast: {str(e)}")
    
    def get_daily_forecast(self, city: str) -> List[Dict]:
        """Get 7-day forecast"""
        try:
            locations = self.geocode_location(city, limit=1)
            if not locations:
                raise ValueError(f"Location '{city}' not found")
            
            location = locations[0]
            
            params = {
                "latitude": location["lat"],
                "longitude": location["lon"],
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code,wind_speed_10m_max",
                "timezone": "auto",
                "forecast_days": 7
            }
            
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            daily = data.get("daily", {})
            
            forecast = []
            times = daily.get("time", [])
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])
            pop = daily.get("precipitation_probability_max", [])
            weather_codes = daily.get("weather_code", [])
            wind = daily.get("wind_speed_10m_max", [])
            
            for i in range(len(times)):
                dt = datetime.fromisoformat(times[i])
                temp_avg = (temp_max[i] + temp_min[i]) / 2
                
                forecast.append({
                    "dt": int(dt.timestamp()),
                    "date": dt.strftime("%a, %b %d"),
                    "temp_min": round(temp_min[i], 1),
                    "temp_max": round(temp_max[i], 1),
                    "temp_avg": round(temp_avg, 1),
                    "humidity": 0,  # Not available in daily
                    "description": self._get_weather_description(weather_codes[i]),
                    "icon": self._get_weather_icon(weather_codes[i]),
                    "pop": pop[i] if i < len(pop) else 0,
                    "wind_speed": round(wind[i], 1)
                })
            
            return forecast
            
        except Exception as e:
            raise Exception(f"Failed to get daily forecast: {str(e)}")
    
    def _get_weather_description(self, code: int) -> str:
        """Map WMO weather code to description"""
        weather_codes = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing Rime Fog",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            55: "Dense Drizzle",
            61: "Slight Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Slight Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            77: "Snow Grains",
            80: "Slight Rain Showers",
            81: "Moderate Rain Showers",
            82: "Violent Rain Showers",
            85: "Slight Snow Showers",
            86: "Heavy Snow Showers",
            95: "Thunderstorm",
            96: "Thunderstorm with Slight Hail",
            99: "Thunderstorm with Heavy Hail"
        }
        return weather_codes.get(code, "Unknown")
    
    def _get_weather_icon(self, code: int) -> str:
        """Map WMO code to icon code"""
        # Simplified icon mapping
        if code == 0:
            return "01d"
        elif code in [1, 2]:
            return "02d"
        elif code == 3:
            return "03d"
        elif code in [45, 48]:
            return "50d"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "10d"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "13d"
        elif code in [95, 96, 99]:
            return "11d"
        else:
            return "01d"

# Singleton instance
weather_service = OpenMeteoService()
