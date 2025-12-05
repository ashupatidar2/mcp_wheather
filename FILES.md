# 📂 Project Files Documentation

Complete list of all files in WeatherPro project with descriptions.

## 🎯 Root Directory

### Configuration Files
- **`.env`** - Environment variables (API keys, credentials)
- **`.env.example`** - Example environment file template
- **`README.md`** - Complete project documentation
- **`FILES.md`** - This file - complete file listing

### Scripts
- **`run_backend.sh`** - Start backend server script
- **`run_frontend.sh`** - Start frontend server script

## 🔧 Backend Directory (`/backend`)

### Main Files
- **`main.py`** - FastAPI application entry point
  - API routes and endpoints
  - CORS configuration
  - Server initialization

- **`models.py`** - Pydantic data models
  - WeatherData model
  - Request/Response models
  - Data validation schemas

- **`requirements.txt`** - Python dependencies
  - fastapi
  - uvicorn
  - requests
  - gspread
  - oauth2client
  - pydantic
  - python-dotenv

### Services Directory (`/backend/services`)

- **`weather_service.py`** - Weather API integration
  - Open-Meteo API calls
  - Photon/Nominatim geocoding
  - Hourly forecast processing
  - Daily forecast aggregation
  - Weather code mapping

- **`sheets_service.py`** - Google Sheets integration
  - Save weather data
  - Retrieve history
  - Sheet formatting
  - Authentication

## 🎨 Frontend Directory (`/frontend`)

### HTML Pages

- **`index.html`** - Home page
  - Main weather search
  - Current weather display
  - Hourly & daily forecasts
  - Save to Sheets button
  - Recent search history

- **`features.html`** - Features showcase
  - 8 feature cards
  - Village support details
  - Forecast capabilities
  - Theme options

- **`forecast.html`** - Forecast page
  - Dedicated forecast interface
  - Live weather search
  - Tabbed view (5-day/hourly)
  - Interactive cards

- **`history.html`** - Search history
  - Latest 10 searches
  - Click to re-search
  - Timestamps
  - Refresh button

- **`about.html`** - About & tech stack
  - Project mission
  - Complete tech stack
  - Features list
  - Data sources with links

### CSS Files

- **`style.css`** - Main stylesheet
  - CSS variables (colors, gradients)
  - Dark/light theme support
  - Navbar & footer styles
  - Weather card styles
  - Forecast layouts
  - Page-specific styles
  - Responsive breakpoints
  - Animations & transitions

### JavaScript Files

- **`app.js`** - Main application logic
  - Weather search functionality
  - Current weather display
  - Hourly forecast loading
  - Daily forecast loading
  - History management
  - Theme toggle
  - Save to Sheets
  - Tab switching
  - Modal handling

- **`forecast.js`** - Forecast page logic
  - Forecast search
  - Daily forecast display
  - Hourly forecast display
  - Tab switching
  - Theme toggle

## 📊 Data Flow

### Weather Search Flow
```
User Input (city)
    ↓
Frontend (app.js)
    ↓
Backend API (/api/weather/{city})
    ↓
weather_service.py
    ↓
1. Geocode location (Photon/Nominatim)
2. Get weather (Open-Meteo)
    ↓
Return JSON response
    ↓
Frontend displays weather
```

### Save to Sheets Flow
```
Current Weather Data
    ↓
Frontend (Save button)
    ↓
Backend API (/api/weather/save)
    ↓
sheets_service.py
    ↓
Google Sheets API
    ↓
Data saved to spreadsheet
```

### History Flow
```
Frontend (Load History)
    ↓
Backend API (/api/weather/history?limit=5)
    ↓
sheets_service.py
    ↓
Google Sheets API
    ↓
Return latest records
    ↓
Frontend displays cards
```

## 🔑 Key File Relationships

### Backend Dependencies
```
main.py
  ├── models.py (data validation)
  ├── weather_service.py (weather data)
  └── sheets_service.py (storage)
```

### Frontend Dependencies
```
index.html
  ├── style.css (styling)
  └── app.js (functionality)

forecast.html
  ├── style.css (styling)
  └── forecast.js (functionality)

Other pages
  ├── style.css (styling)
  └── inline JS (theme toggle)
```

## 📝 File Sizes (Approximate)

- **Backend**: ~15 KB total
  - main.py: ~6 KB
  - weather_service.py: ~8 KB
  - models.py: ~1 KB

- **Frontend**: ~80 KB total
  - style.css: ~25 KB
  - app.js: ~15 KB
  - HTML pages: ~40 KB combined

## 🔄 Recent Changes

### Migration to Open-Meteo
- Updated `weather_service.py` completely
- Removed API key requirements
- Added Photon/Nominatim geocoding
- Improved village location support

### Multi-Page Architecture
- Created 5 separate HTML pages
- Shared CSS across all pages
- Page-specific JavaScript where needed
- Consistent navbar/footer

### UI Improvements
- Modern gradient backgrounds
- Glassmorphism effects
- Better responsive design
- Dark/light theme toggle

## 🚀 Deployment Files

For production deployment, you'll need:
- All backend files
- All frontend files
- `.env` with production credentials
- Google Sheets credentials JSON
- Web server configuration (nginx/apache)

## 📦 Dependencies Summary

### Backend Python Packages
```
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
gspread==5.12.0
oauth2client==4.1.3
pydantic==2.5.0
python-dotenv==1.0.0
```

### Frontend (No Build Required)
- Pure HTML/CSS/JavaScript
- No npm packages
- No build process
- Direct browser execution

---

**Last Updated**: December 5, 2025
**Project Version**: 2.0 (Open-Meteo Migration)
