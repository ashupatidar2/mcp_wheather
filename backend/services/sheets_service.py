"""
Google Sheets service for reading/writing weather data
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import List, Dict, Optional
from config import Config

class SheetsService:
    """Service for interacting with Google Sheets"""
    
    def __init__(self):
        self.sheet_id = Config.GOOGLE_SHEET_ID
        self.credentials_dict = Config.GOOGLE_CREDENTIALS_JSON
        self.worksheet = None
        self.initialized = False
        try:
            self._initialize_sheet()
            self.initialized = True
        except Exception as e:
            print(f"⚠️  WARNING: Google Sheets initialization failed: {str(e)}")
            print(f"⚠️  Weather functionality will work, but saving to Sheets will be disabled.")
            print(f"⚠️  Please enable Google Sheets API at: https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=488668451030")
    
    def _initialize_sheet(self):
        """Initialize Google Sheets connection"""
        # Define the scope
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Authenticate using service account
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            self.credentials_dict, 
            scope
        )
        client = gspread.authorize(credentials)
        
        # Open the sheet
        spreadsheet = client.open_by_key(self.sheet_id)
        self.worksheet = spreadsheet.sheet1  # Use first sheet
        
        # Initialize headers if sheet is empty
        self._ensure_headers()
    
    def _ensure_headers(self):
        """Ensure the sheet has proper headers"""
        try:
            # Check if first row has headers
            first_row = self.worksheet.row_values(1)
            
            if not first_row or first_row[0] != "Timestamp":
                # Set headers
                headers = [
                    "Timestamp", "City", "Country", "Temperature (°C)", 
                    "Feels Like (°C)", "Humidity (%)", "Pressure (hPa)", 
                    "Description", "Wind Speed (m/s)"
                ]
                self.worksheet.insert_row(headers, 1)
                
        except Exception as e:
            raise Exception(f"Failed to set headers: {str(e)}")
    
    def save_weather(self, weather_data: Dict) -> bool:
        """
        Save weather data to Google Sheets
        
        Args:
            weather_data: Dictionary containing weather information
            
        Returns:
            True if successful, False otherwise
        """
        if not self.initialized:
            raise Exception(
                "Google Sheets API is not enabled. "
                "Please enable it at: https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=488668451030"
            )
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row = [
                timestamp,
                weather_data.get("city", ""),
                weather_data.get("country", ""),
                weather_data.get("temperature", 0),
                weather_data.get("feels_like", 0),
                weather_data.get("humidity", 0),
                weather_data.get("pressure", 0),
                weather_data.get("description", ""),
                weather_data.get("wind_speed", 0)
            ]
            
            self.worksheet.append_row(row)
            return True
            
        except Exception as e:
            raise Exception(f"Failed to save to Google Sheets: {str(e)}")
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """
        Get historical weather data from Google Sheets
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of weather records
        """
        if not self.initialized:
            raise Exception(
                "Google Sheets API is not enabled. "
                "Please enable it at: https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=488668451030"
            )
        
        try:
            # Get all records
            all_records = self.worksheet.get_all_records()
            
            # Return latest records (reverse order)
            recent_records = list(reversed(all_records))[:limit]
            
            return recent_records
            
        except Exception as e:
            raise Exception(f"Failed to read from Google Sheets: {str(e)}")

# Singleton instance
sheets_service = SheetsService()
