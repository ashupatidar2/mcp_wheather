# 🌤️ Weather + Google Sheets Integration

A modern web application that fetches weather data from OpenWeatherMap API and stores it in Google Sheets. Built with **FastAPI** backend and **vanilla JavaScript** frontend.

## ✨ Features

- 🔍 **Search Weather**: Get real-time weather data for any city
- 📊 **Google Sheets Integration**: Save weather data directly to Google Sheets
- 📜 **History View**: View all previously saved weather records
- 🌓 **Dark/Light Mode**: Toggle between themes with persistent preference
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- 🎨 **Modern UI**: Glassmorphism effects and smooth animations

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **OpenWeatherMap API**: Weather data provider
- **Google Sheets API**: Data storage via `gspread`
- **Pydantic**: Data validation

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with CSS variables
- **JavaScript**: Vanilla JS (no frameworks)

## 📋 Prerequisites

- Python 3.8+
- OpenWeatherMap API key
- Google Cloud Project with Sheets API enabled
- Google Service Account credentials

## 🚀 Setup Instructions

### 1. Clone/Navigate to Project
```bash
cd /home/vinayak/Documents/mcpnew
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Variables
The `.env` file is already configured with your credentials:
- ✅ Weather API Key
- ✅ Google Sheet ID
- ✅ Google Service Account JSON

**Important**: Never commit `.env` file to git!

### 4. Google Sheet Setup
Make sure your Google Sheet is shared with the service account email:
```
weather-app-service@weather-sheets-app.iam.gserviceaccount.com
```

## 🎯 Running the Application

### Start Backend Server
```bash
cd /home/vinayak/Documents/mcpnew/backend
python main.py
```
Backend will run on: `http://localhost:8000`

### Start Frontend Server
Open a new terminal:
```bash
cd /home/vinayak/Documents/mcpnew/frontend
python -m http.server 3000
```
Frontend will run on: `http://localhost:3000`

### Access the Application
Open your browser and go to: **http://localhost:3000**

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Get Weather
```
GET /api/weather/{city}
```
Example: `GET /api/weather/Mumbai`

### Save Weather
```
POST /api/weather/save
Content-Type: application/json

{
  "city": "Mumbai",
  "temperature": 28.5,
  "feels_like": 30.2,
  "humidity": 75,
  "pressure": 1013,
  "description": "Clear Sky",
  "icon": "01d",
  "wind_speed": 3.5,
  "country": "IN"
}
```

### Get History
```
GET /api/weather/history?limit=50
```

## 📁 Project Structure

```
mcpnew/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration loader
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   └── services/
│       ├── weather_service.py   # Weather API integration
│       └── sheets_service.py    # Google Sheets integration
├── frontend/
│   ├── index.html           # Main HTML
│   ├── style.css            # Styling
│   └── app.js               # JavaScript logic
├── .env                     # Environment variables (DO NOT COMMIT)
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔒 Security

- ✅ All credentials stored in `.env` file
- ✅ `.env` added to `.gitignore`
- ✅ No hardcoded API keys in code
- ✅ CORS configured for production
- ✅ Input validation with Pydantic

## 🎨 UI Features

- **Modern Design**: Gradient backgrounds and glassmorphism
- **Dark/Light Mode**: Persistent theme preference
- **Smooth Animations**: Loading states and transitions
- **Responsive**: Mobile-first design
- **Accessibility**: Semantic HTML and ARIA labels

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://localhost:8000/api/health

# Get weather
curl http://localhost:8000/api/weather/Mumbai
```

### Test Frontend
1. Open `http://localhost:3000`
2. Search for a city (e.g., "Mumbai")
3. Click "Save to Google Sheets"
4. Click "Load History" to view saved data
5. Check your Google Sheet for the new entry

## 📊 Google Sheet Format

The app automatically creates headers in your Google Sheet:

| Timestamp | City | Country | Temperature (°C) | Feels Like (°C) | Humidity (%) | Pressure (hPa) | Description | Wind Speed (m/s) |
|-----------|------|---------|------------------|-----------------|--------------|----------------|-------------|------------------|

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify `.env` file exists and has correct values
- Ensure all dependencies are installed

### Frontend can't connect to backend
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify API_BASE_URL in `frontend/app.js`

### Google Sheets error
- Verify Sheet ID is correct
- Check if service account has Editor access
- Ensure Google Sheets API is enabled

### Weather API error
- Verify API key is valid
- Check city name spelling
- Ensure you haven't exceeded API rate limits

## 📝 License

This project is open source and available for personal and educational use.

## 🙏 Credits

- **Weather Data**: [OpenWeatherMap](https://openweathermap.org/)
- **Icons**: Weather icons from OpenWeatherMap
- **Fonts**: [Google Fonts - Inter](https://fonts.google.com/specimen/Inter)

---

Built with ❤️ using FastAPI & Google Sheets API
