# backend/api/drive_setup.py

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Base directory and credentials
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials', 'drive_service_account.json')

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets'
]

# Auth
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

# Google Drive & Sheets services
drive_service = build('drive', 'v3', credentials=credentials)
sheets_service = build('sheets', 'v4', credentials=credentials)

# 🔸 These are specific to your spreadsheet
SHEET_ID = '13PnC6wkTlmyjF4w2njUn4k7glxyb0nXX8D6yMIi5WuE'
SHEET_NAME = 'SCM FORWARD'
