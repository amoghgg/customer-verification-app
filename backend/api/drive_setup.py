# backend/api/drive_setup.py

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load service account credentials from environment variable
SERVICE_ACCOUNT_INFO = json.loads(os.getenv("DRIVE_SERVICE_ACCOUNT", "{}"))

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
]

# Authenticate using credentials from env var
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

# Google Drive & Sheets clients
drive_service = build("drive", "v3", credentials=credentials)
sheets_service = build("sheets", "v4", credentials=credentials)

# 🔸 Spreadsheet details
SHEET_ID = "13PnC6wkTlmyjF4w2njUn4k7glxyb0nXX8D6yMIi5WuE"
SHEET_NAME = "SCM FORWARD"
