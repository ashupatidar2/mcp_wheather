# 🌤️ WeatherPro - Professional Weather Forecast Application with Authentication

Secure, unlimited weather forecasts for cities, towns, and villages worldwide. Features complete user authentication with PostgreSQL and JWT tokens!

## ✨ Features

### 🔐 Authentication & Security
- **User Signup/Login** - Secure account creation with email validation
- **JWT Tokens** - 1-day token expiration for security
- **Bcrypt Password Hashing** - Industry-standard password encryption
- **Protected Routes** - All weather features require authentication
- **PostgreSQL Database** - Reliable user data storage

### 🌤️ Weather Features
- 🏘️ **Village Weather Support** - Get weather for small villages using advanced geocoding
- 📅 **5-Day Forecast** - Detailed daily forecasts with min/max temperatures
- ⏰ **Hourly Forecast** - 48-hour forecasts with 3-hour intervals
- 💾 **Google Sheets Integration** - Save weather data to Google Sheets
- 📜 **Search History** - Quick access to recent searches
- 🌓 **Dark/Light Theme** - Toggle between themes
- 🌍 **Global Coverage** - Weather for any location worldwide
- ✅ **100% Free** - No API keys, no rate limits, unlimited access

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Python) - High-performance async API framework
- **PostgreSQL** - Robust relational database for user management
- **SQLAlchemy** - Python SQL toolkit and ORM
- **JWT (python-jose)** - Secure token-based authentication
- **Bcrypt (passlib)** - Password hashing
- **Open-Meteo API** - Free weather data (no API key required!)
- **Photon/Nominatim** - Advanced geocoding for village support
- **Google Sheets API** - Cloud-based data storage

### Frontend
- **HTML/CSS/JavaScript** - Modern, responsive design
- **Glassmorphism UI** - Premium visual effects
- **JWT Token Management** - Secure authentication flow
- **Multi-page Architecture** - Separate pages for different features

## 📁 Project Structure

```
mcpnew/
├── backend/
│   ├── main.py                 # FastAPI application with auth routes
│   ├── models.py               # Pydantic models for weather data
│   ├── database.py             # PostgreSQL connection (SQLAlchemy)
│   ├── auth_models.py          # User model for database
│   ├── auth.py                 # Authentication utilities (JWT, bcrypt)
│   ├── auth_routes.py          # Signup/Login API endpoints
│   ├── init_db.py              # Database initialization script
│   ├── config.py               # Configuration management
│   ├── services/
│   │   ├── weather_service.py  # Open-Meteo integration
│   │   └── sheets_service.py   # Google Sheets integration
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── login.html              # Login page
│   ├── signup.html             # Signup page
│   ├── index.html              # Home page (weather search) - Protected
│   ├── features.html           # Features showcase - Protected
│   ├── forecast.html           # Forecast page - Protected
│   ├── history.html            # Search history - Protected
│   ├── about.html              # About & tech stack - Protected
│   ├── style.css               # Shared styles
│   ├── auth.js                 # Authentication JavaScript
│   ├── app.js                  # Main JavaScript (with JWT)
│   └── forecast.js             # Forecast page logic
│
├── .env                        # Environment variables (DB, JWT, Sheets)
└── .env.example                # Environment template
```

## 🛠️ Installation & Setup

### 🚀 Quick Start

**1. Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**2. Initialize Database**
```bash
cd backend
python init_db.py
```

**3. Start Server**
```bash
cd backend
python main.py   # or 
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**4. Open Browser**
```
http://localhost:8000
```

You'll be redirected to login page. Signup first, then login to access weather features!

---

### Prerequisites
- Python 3.8+
- PostgreSQL (installed and running)
- Google Cloud Project (for Sheets integration)

### 1. PostgreSQL Setup

**Install PostgreSQL** (if not installed):
```bash
sudo apt install postgresql postgresql-contrib
```

**Start PostgreSQL**:
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Set Password** (if needed):
```bash
sudo -u postgres psql
ALTER USER postgres PASSWORD 'Ashu6672';
\q
```

### 2. Backend Setup

#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Dependencies include**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `psycopg2-binary` - PostgreSQL adapter
- `sqlalchemy` - ORM
- `passlib[bcrypt]` - Password hashing
- `python-jose[cryptography]` - JWT tokens
- `requests` - HTTP client
- `google-api-python-client` - Google Sheets

#### Configure Environment Variables
Create `.env` file in project root:
```env
# Database Configuration
DATABASE_URL=

# JWT Configuration
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=1

# Google Sheets Configuration
SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

#### Initialize Database
```bash
cd backend
python init_db.py
```

This will:
- Create `weatherpro_db` database
- Create `users` table
- Set up indexes and constraints

#### Get Google Sheets Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google Sheets API
4. Create Service Account credentials
5. Download JSON credentials file
6. Share your Google Sheet with the service account email

### 3. Start Application

```bash
cd backend
python main.py
```

Application runs on: `http://localhost:8000`

**Note**: Uvicorn serves both backend API and frontend files from a single server!

## 🔐 Authentication Flow

### 1. Signup
- Navigate to `http://localhost:8000` → Redirects to `/login.html`
- Click "Sign up"
- Enter email and password (min 6 characters)
- Account created → Redirected to login

### 2. Login
- Enter email and password
- JWT token generated (1-day expiry)
- Token saved to localStorage
- Redirected to weather app

### 3. Access Weather Features
- All weather pages require valid JWT token
- Token automatically included in API requests
- Invalid/expired token → Redirected to login

### 4. Logout
- Click logout button (🚪) in navbar
- Token removed from localStorage
- Redirected to login page

## 🌐 Pages & Navigation

1. **Login** (`/login.html`) - Public
   - Email/password login
   - Link to signup
   - Error handling

2. **Signup** (`/signup.html`) - Public
   - Account creation
   - Password confirmation
   - Email validation

3. **Home** (`/` or `/index.html`) - Protected
   - Weather search
   - Current weather display
   - Hourly & daily forecasts
   - Save to Sheets button
   - Recent search history

4. **Features** (`/features.html`) - Protected
   - Complete feature showcase
   - 8 feature cards with details

5. **Forecast** (`/forecast.html`) - Protected
   - Dedicated forecast interface
   - Live weather search
   - Tabbed interface (5-day/hourly)

6. **History** (`/history.html`) - Protected
   - Latest 10 searches
   - Click to re-search
   - Timestamps

7. **About** (`/about.html`) - Protected
   - Project information
   - Complete tech stack
   - Data sources

## 🔧 API Endpoints

All API endpoints are available at `http://localhost:8000/api`

### Authentication Endpoints (Public)

```
POST  /api/auth/signup              # Create new account
POST  /api/auth/login               # Login and get JWT token
GET   /api/auth/me                  # Get current user (protected)
POST  /api/auth/logout              # Logout (client-side)
```

### Weather Endpoints (Protected - Require JWT Token)

```
GET   /api/weather/{city}           # Current weather
GET   /api/forecast/hourly/{city}   # 48-hour forecast
GET   /api/forecast/daily/{city}    # 5-day forecast
POST  /api/weather/save             # Save to Google Sheets
GET   /api/weather/history?limit=5  # Get search history
GET   /api/health                   # Health check (public)
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

## 🔍 View Database Data

### Option 1: PostgreSQL CLI
```bash
psql -U postgres -d weatherpro_db -c "SELECT * FROM users;"
```

### Option 2: pgAdmin4 (GUI)
1. Open pgAdmin4
2. Add Server: localhost:5432
3. Database: weatherpro_db
4. Username: postgres, Password: Ashu6672
5. Navigate to: Servers → PostgreSQL → Databases → weatherpro_db → Tables → users

### Option 3: Python Script
```bash
cd backend
python -c "from database import SessionLocal; from auth_models import User; db = SessionLocal(); users = db.query(User).all(); [print(f'{u.id}: {u.email}') for u in users]"
```

## 🧪 Usage Examples

### Search Weather
```javascript
// Open in browser
http://localhost:8000
// Login first, then search
Enter: "Mumbai" or "Garoth" or "Garoth,MP,IN"
```

### View Forecast
```javascript
// Navigate to forecast page
http://localhost:8000/forecast.html
Search location → View 5-day or hourly forecast
```

### Check History
```javascript
// View recent searches
http://localhost:8000/history.html
Click any card to re-search
```

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check if server is running
curl http://localhost:8000/api/health

# Restart server
cd backend
python main.py
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Restart
cd backend
python main.py
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Reinitialize database
cd backend
python init_db.py
```

### Authentication Issues
```bash
# Clear browser localStorage
# Open browser console (F12) and run:
localStorage.clear()

# Or logout and login again
```

### Village Not Found
Try different formats:
- `Garoth` (village name only)
- `Garoth, MP` (village + state)
- `Garoth, Madhya Pradesh, India` (full location)

## 🔒 Security Features

1. **Password Security**
   - Bcrypt hashing with automatic salt
   - Never store plaintext passwords
   - Minimum 6 character requirement

2. **JWT Security**
   - Secret key from environment variable
   - 1-day token expiration
   - Token validation on every protected request

3. **Database Security**
   - SQL injection prevention via SQLAlchemy ORM
   - Unique email constraint
   - Database credentials in `.env` file

4. **API Security**
   - CORS configured properly
   - Input validation on all endpoints
   - Error messages don't leak sensitive info

## 📝 Environment Variables

Required in `.env` file:

```env
# Database
DATABASE_URL=
# JWT
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=1

# Google Sheets (Optional)
SPREADSHEET_ID=<your-spreadsheet-id>
GOOGLE_CREDENTIALS_PATH=<path-to-credentials.json>
```

## 🚀 Deployment

For production deployment:
1. Use strong `SECRET_KEY` (generate with `openssl rand -hex 32`)
2. Set proper CORS origins (not `*`)
3. Use environment-specific `.env` files
4. Enable HTTPS
5. Use production database (not localhost)
6. Set up proper logging
7. Use process manager (systemd, supervisor)

## 📦 Dependencies

See `backend/requirements.txt` for complete list.

**Key packages**:
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- psycopg2-binary==2.9.9
- sqlalchemy==2.0.23
- passlib[bcrypt]==1.7.4
- python-jose[cryptography]==3.3.0

## 🎯 Features Roadmap

- [x] User authentication with JWT
- [x] PostgreSQL database integration
- [x] Password hashing with bcrypt
- [x] Protected weather endpoints
- [ ] Email verification
- [ ] Password reset functionality
- [ ] User profile management
- [ ] Weather alerts
- [ ] Favorite locations

## 📄 License

Free to use for personal and educational purposes.

---

**Last Updated**: December 5, 2025  
**Project Version**: 2.0 (Authentication System)  
**Database**: PostgreSQL  
**Authentication**: JWT + Bcrypt
