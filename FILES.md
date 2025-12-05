# 📂 Project Files Documentation

Complete list of all files in WeatherPro project with authentication system.

## 🎯 Root Directory

### Configuration Files
- **`.env`** - Environment variables (Database, JWT, Google Sheets credentials)
- **`.env.example`** - Example environment file template
- **`README.md`** - Complete project documentation with authentication
- **`FILES.md`** - This file - complete file listing

## 🔧 Backend Directory (`/backend`)

### Main Application Files

- **`main.py`** - FastAPI application entry point
  - API routes and endpoints
  - Authentication route integration
  - Protected weather endpoints
  - CORS configuration
  - Static file serving (frontend)
  - Server initialization

- **`models.py`** - Pydantic data models for weather
  - WeatherData model
  - Request/Response models
  - Data validation schemas

- **`requirements.txt`** - Python dependencies
  - fastapi==0.104.1
  - uvicorn[standard]==0.24.0
  - psycopg2-binary==2.9.9
  - sqlalchemy==2.0.23
  - passlib[bcrypt]==1.7.4
  - python-jose[cryptography]==3.3.0
  - bcrypt==4.1.2
  - email-validator==2.1.0
  - requests==2.31.0
  - google-api-python-client
  - pydantic==2.5.0
  - python-dotenv==1.0.0

### Authentication Files

- **`database.py`** - PostgreSQL database connection
  - SQLAlchemy engine setup
  - Session management
  - Database dependency injection

- **`auth_models.py`** - User model for database
  - User table schema (SQLAlchemy)
  - id, email, hashed_password, is_active, created_at

- **`auth.py`** - Authentication utilities
  - Password hashing (bcrypt)
  - Password verification
  - JWT token creation (1-day expiry)
  - JWT token verification
  - Get current user dependency

- **`auth_routes.py`** - Authentication API endpoints
  - POST /api/auth/signup - User registration
  - POST /api/auth/login - User login (returns JWT)
  - GET /api/auth/me - Get current user profile
  - POST /api/auth/logout - Logout endpoint

- **`init_db.py`** - Database initialization script
  - Create weatherpro_db database
  - Create users table
  - Set up indexes

- **`config.py`** - Configuration management
  - Environment variable loading
  - Database URL configuration
  - JWT settings

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

### Authentication Pages

- **`login.html`** - Login page (Public)
  - Email/password login form
  - Error/success messages
  - Link to signup page
  - Modern glassmorphism design

- **`signup.html`** - Signup page (Public)
  - User registration form
  - Email validation
  - Password confirmation
  - Minimum 6 character validation
  - Link to login page

### Protected Weather Pages

- **`index.html`** - Home page (Protected)
  - Main weather search
  - Current weather display
  - Hourly & daily forecasts
  - Save to Sheets button
  - Recent search history
  - Logout button in navbar

- **`features.html`** - Features showcase (Protected)
  - 8 feature cards
  - Village support details
  - Forecast capabilities
  - Theme options

- **`forecast.html`** - Forecast page (Protected)
  - Dedicated forecast interface
  - Live weather search
  - Tabbed view (5-day/hourly)
  - Interactive cards

- **`history.html`** - Search history (Protected)
  - Latest 10 searches
  - Click to re-search
  - Timestamps
  - Refresh button

- **`about.html`** - About & tech stack (Protected)
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
  - Authentication page styles
  - Page-specific styles
  - Responsive breakpoints
  - Animations & transitions

### JavaScript Files

- **`auth.js`** - Authentication JavaScript
  - handleSignup() - Signup form submission
  - handleLogin() - Login form submission
  - logout() - Logout and clear token
  - checkAuth() - Auto-redirect if not authenticated
  - apiCall() - API helper with JWT token
  - Token management (localStorage)

- **`app.js`** - Main application logic (Protected)
  - JWT token integration
  - apiCallWithAuth() - API calls with token
  - Weather search functionality
  - Current weather display
  - Hourly forecast loading
  - Daily forecast loading
  - History management
  - Theme toggle
  - Save to Sheets
  - Tab switching
  - Modal handling
  - Authentication check on load
  - Logout functionality

- **`forecast.js`** - Forecast page logic
  - Forecast search
  - Daily forecast display
  - Hourly forecast display
  - Tab switching
  - Theme toggle

## 📊 Data Flow

### Authentication Flow
```
User → Signup Page
    ↓
POST /api/auth/signup
    ↓
Password hashed (bcrypt)
    ↓
User saved to PostgreSQL
    ↓
Redirect to Login
    ↓
POST /api/auth/login
    ↓
Password verified
    ↓
JWT token generated (1 day)
    ↓
Token saved to localStorage
    ↓
Redirect to Weather App
```

### Weather Search Flow (Protected)
```
User Input (city)
    ↓
Frontend (app.js) + JWT token
    ↓
Backend API (/api/weather/{city})
    ↓
JWT token verified
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

### Save to Sheets Flow (Protected)
```
Current Weather Data
    ↓
Frontend (Save button) + JWT token
    ↓
Backend API (/api/weather/save)
    ↓
JWT token verified
    ↓
sheets_service.py
    ↓
Google Sheets API
    ↓
Data saved to spreadsheet
```

### History Flow (Protected)
```
Frontend (Load History) + JWT token
    ↓
Backend API (/api/weather/history?limit=5)
    ↓
JWT token verified
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
  ├── auth_routes.py (authentication endpoints)
  ├── auth.py (JWT & password utilities)
  ├── auth_models.py (User model)
  ├── database.py (PostgreSQL connection)
  ├── models.py (weather data validation)
  ├── weather_service.py (weather data)
  └── sheets_service.py (storage)
```

### Frontend Dependencies
```
login.html / signup.html
  ├── style.css (styling)
  └── auth.js (authentication logic)

index.html (and other protected pages)
  ├── style.css (styling)
  ├── app.js (functionality + JWT)
  └── auth.js (authentication check)
```

## 📝 File Sizes (Approximate)

- **Backend**: ~35 KB total
  - main.py: ~8 KB
  - auth_routes.py: ~7 KB
  - auth.py: ~5 KB
  - auth_models.py: ~1 KB
  - database.py: ~1 KB
  - weather_service.py: ~8 KB
  - models.py: ~1 KB
  - init_db.py: ~2 KB

- **Frontend**: ~110 KB total
  - style.css: ~25 KB
  - app.js: ~18 KB
  - auth.js: ~7 KB
  - HTML pages: ~60 KB combined

## 🔄 Recent Changes

### Authentication System (v2.0)
- Added PostgreSQL database integration
- Implemented JWT token authentication
- Created User model and auth routes
- Protected all weather endpoints
- Added login/signup pages
- Integrated bcrypt password hashing
- Added token management in frontend

### Migration to Open-Meteo (v1.5)
- Updated `weather_service.py` completely
- Removed API key requirements
- Added Photon/Nominatim geocoding
- Improved village location support

### Multi-Page Architecture (v1.0)
- Created 5 separate HTML pages
- Shared CSS across all pages
- Page-specific JavaScript where needed
- Consistent navbar/footer

## 🗄️ Database Files

### PostgreSQL Database: `weatherpro_db`

**Tables**:
- `users` - User accounts
  - Columns: id, email, hashed_password, is_active, created_at
  - Indexes: Primary key on id, Unique index on email

**Access Methods**:
1. psql CLI: `psql -U postgres -d weatherpro_db`
2. pgAdmin4: GUI tool for PostgreSQL
3. Python: Via SQLAlchemy in `database.py`

## 🚀 Deployment Files

For production deployment, you'll need:
- All backend files
- All frontend files
- `.env` with production credentials
  - Strong SECRET_KEY
  - Production DATABASE_URL
  - Google Sheets credentials
- PostgreSQL database setup
- Web server configuration (nginx/apache)
- SSL certificates for HTTPS

## 📦 Dependencies Summary

### Backend Python Packages
```
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
psycopg2-binary==2.9.9
sqlalchemy==2.0.23

# Authentication
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
bcrypt==4.1.2
email-validator==2.1.0

# Weather & Sheets
requests==2.31.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0

# Utilities
pydantic==2.5.0
python-dotenv==1.0.0
```

### Frontend (No Build Required)
- Pure HTML/CSS/JavaScript
- No npm packages
- No build process
- Direct browser execution
- JWT token management via localStorage

## 🔐 Security Files

### Environment Variables (`.env`)
**Never commit to git!**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/weatherpro_db
SECRET_KEY=<secret-key-for-jwt>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=1
SPREADSHEET_ID=<google-sheets-id>
GOOGLE_CREDENTIALS_PATH=<path-to-credentials>
```

### Credentials
- **Google Sheets**: JSON credentials file (service account)
- **PostgreSQL**: Username/password in `.env`
- **JWT**: Secret key in `.env`

## 📊 API Endpoints Summary

### Public Endpoints
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/health` - Health check

### Protected Endpoints (Require JWT)
- `GET /api/auth/me` - Current user profile
- `GET /api/weather/{city}` - Current weather
- `GET /api/forecast/hourly/{city}` - Hourly forecast
- `GET /api/forecast/daily/{city}` - Daily forecast
- `POST /api/weather/save` - Save to sheets
- `GET /api/weather/history` - Search history

---

**Last Updated**: December 5, 2025  
**Project Version**: 2.0 (Authentication System)  
**Total Files**: 25+ files  
**Database**: PostgreSQL (weatherpro_db)  
**Authentication**: JWT + Bcrypt
