# 🌤️ WeatherPro - Professional Weather Forecast Application

Free, unlimited weather forecasts for cities, towns, and villages worldwide. No API keys required!

## ✨ Features

- 🏘️ **Village Weather Support** - Get weather for small villages using advanced geocoding
- 📅 **5-Day Forecast** - Detailed daily forecasts with min/max temperatures
- ⏰ **Hourly Forecast** - 48-hour forecasts with 3-hour intervals
- � **Google Sheets Integration** - Save weather data to Google Sheets
- � **Search History** - Quick access to recent searches
- 🌓 **Dark/Light Theme** - Toggle between themes
- 🌍 **Global Coverage** - Weather for any location worldwide
- ✅ **100% Free** - No API keys, no rate limits, unlimited access

## � Tech Stack

### Backend
- **FastAPI** (Python) - High-performance async API framework
- **Open-Meteo API** - Free weather data (no API key required!)
- **Photon/Nominatim** - Advanced geocoding for village support
- **Google Sheets API** - Cloud-based data storage

### Frontend
- **HTML/CSS/JavaScript** - Modern, responsive design
- **Glassmorphism UI** - Premium visual effects
- **Multi-page Architecture** - Separate pages for different features

## � Project Structure

```
mcpnew/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── services/
│   │   ├── weather_service.py  # Open-Meteo integration
│   │   └── sheets_service.py   # Google Sheets integration
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── index.html             # Home page (weather search)
│   ├── features.html          # Features showcase
│   ├── forecast.html          # Forecast page
│   ├── history.html           # Search history
│   ├── about.html             # About & tech stack
│   ├── style.css              # Shared styles
│   ├── app.js                 # Main JavaScript
│   └── forecast.js            # Forecast page logic
│
├── .env                       # Environment variables
├── run_backend.sh             # Backend startup script
└── run_frontend.sh            # Frontend startup script
```

## �️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Cloud Project (for Sheets integration)

### 1. Clone Repository
```bash
cd /home/vinayak/Documents/mcpnew
```

### 2. Backend Setup

#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables
Create `.env` file in project root:
```env
# Google Sheets Configuration
SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json

# No weather API key needed - Open-Meteo is free!
```

#### Get Google Sheets Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google Sheets API
4. Create Service Account credentials
5. Download JSON credentials file
6. Share your Google Sheet with the service account email

### 3. Start Backend Server
```bash
# From project root
./run_backend.sh

# Or manually
cd backend
python main.py
```

Backend runs on: `http://localhost:8000`

### 4. Start Frontend Server
```bash
# From project root
./run_frontend.sh

# Or manually
cd frontend
python -m http.server 3000
```

Frontend runs on: `http://localhost:3000`

## 🌐 Pages & Navigation

### Available Pages

1. **Home** (`index.html`)
   - Weather search
   - Current weather display
   - Hourly & daily forecasts
   - Save to Google Sheets
   - Recent search history

2. **Features** (`features.html`)
   - Complete feature showcase
   - 8 feature cards with details

3. **Forecast** (`forecast.html`)
   - Dedicated forecast page
   - Live weather search
   - Tabbed interface (5-day/hourly)

4. **History** (`history.html`)
   - Latest 10 searches
   - Click to re-search
   - Timestamps

5. **About** (`about.html`)
   - Project information
   - Complete tech stack
   - Data sources

## 🔧 API Endpoints

### Weather Endpoints
```
GET  /api/weather/{city}              # Current weather
GET  /api/forecast/hourly/{city}      # 48-hour forecast
GET  /api/forecast/daily/{city}       # 5-day forecast
GET  /api/geocode/{query}             # Location search
POST /api/weather/save                # Save to Sheets
GET  /api/weather/history?limit=5     # Get history
GET  /api/health                      # Health check
```

## 🎨 Design Features

- **Modern Gradient Backgrounds** - Purple/blue gradients
- **Glassmorphism Effects** - Frosted glass UI elements
- **Smooth Animations** - Hover effects and transitions
- **Responsive Design** - Mobile-first approach
- **Dark/Light Themes** - User preference saved locally

## 🌍 Data Sources

- **Weather Data**: [Open-Meteo](https://open-meteo.com) - Free, no API key
- **Geocoding**: [Photon](https://photon.komoot.io) & [Nominatim](https://nominatim.openstreetmap.org)
- **Weather Icons**: [OpenWeatherMap](https://openweathermap.org)
- **Storage**: Google Sheets API

## 📝 Usage Examples

### Search Weather
```javascript
// Search for any location
http://localhost:3000/index.html
Enter: "Mumbai" or "Garoth" or "Garoth,MP,IN"
```

### View Forecast
```javascript
// Navigate to forecast page
http://localhost:3000/forecast.html
Search location → View 5-day or hourly forecast
```

### Check History
```javascript
// View recent searches
http://localhost:3000/history.html
Click any card to re-search
```

## 🔑 Key Changes from OpenWeatherMap

### Migration to Open-Meteo

**Why?**
- ✅ 100% Free - No API key required
- ✅ No rate limits - Unlimited requests
- ✅ Better village support - Coordinates-based
- ✅ More accurate data - Multiple sources

**What Changed?**
1. Removed `WEATHER_API_KEY` requirement
2. Updated `weather_service.py` to use Open-Meteo
3. Added Photon/Nominatim geocoding
4. Improved village location search

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# View backend logs
cd backend
python main.py
```

### Frontend Issues
```bash
# Check if frontend is serving
curl http://localhost:3000/index.html

# Restart frontend
cd frontend
python -m http.server 3000
```

### Village Not Found
- Try adding state/country: `Garoth,MP,IN`
- Use nearest city as fallback
- Check spelling

## 📊 Google Sheets Format

Data is saved in this format:
```
Timestamp | City | Country | Temperature (°C) | Humidity (%) | Pressure | Description | Wind Speed
```

## 🚀 Deployment

### Production Considerations
1. Use production ASGI server (uvicorn/gunicorn)
2. Enable CORS properly
3. Add rate limiting
4. Use environment variables
5. Set up HTTPS
6. Configure caching

## � License

Free to use for personal and educational purposes.

## 🤝 Contributing

This is a personal project. Feel free to fork and modify!

## 📞 Support

For issues or questions:
- Check the About page for tech stack details
- Review API documentation
- Test with different locations

---

**Built with ❤️ using FastAPI, Open-Meteo & Google Sheets**

© 2025 WeatherPro • No API Key Required • Unlimited Access
