# Render Deployment Guide

## Required Environment Variables on Render

Set these in **Render Dashboard → Environment** tab:

### 1. Database (REQUIRED)
```
DATABASE_URL=<your-render-postgresql-url>
```
**How to get:**
- Go to Render Dashboard
- Create a new PostgreSQL database
- Copy the "Internal Database URL"
- Paste it in environment variables

### 2. Authentication (REQUIRED)
```
SECRET_KEY=your-super-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=1
```

### 3. Google Sheets (OPTIONAL - for save feature)
```
GOOGLE_SHEET_ID=your-google-sheet-id
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
```

## Steps to Deploy

1. **Create PostgreSQL Database on Render:**
   - Dashboard → New → PostgreSQL
   - Copy "Internal Database URL"

2. **Set Environment Variables:**
   - Go to your Web Service
   - Environment tab
   - Add all variables above

3. **Deploy:**
   - Push to GitHub
   - Render auto-deploys

## Troubleshooting

### "Failed to fetch" error
- Check browser console (F12)
- Verify DATABASE_URL is set
- Check Render logs for errors

### Database connection error
- Ensure PostgreSQL database is created
- Verify DATABASE_URL format: `postgresql://user:pass@host:port/dbname`

### Authentication not working
- Verify SECRET_KEY is set
- Check if database tables are created
