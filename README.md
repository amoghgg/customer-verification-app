# Customer Verification App

A full-stack delivery verification system built for logistics operations where proof of delivery needs to be captured, stored, and auditable. Field agents upload video proof at the point of delivery; the platform handles mismatch detection, Google Sheets sync, and Drive storage automatically.

## The problem it solves

Delivery teams needed a way to verify that goods reached the right customer with evidence that could be pulled up later. Screenshots and WhatsApp photos weren't cutting it — no structure, no searchability, no audit trail. This app gives each delivery a video record tied to a structured entry in Sheets, accessible without touching a database.

## Features

- Video proof capture and upload from mobile or desktop
- Automatic sync to Google Sheets with structured delivery metadata
- Google Drive integration for video storage with direct links back to Sheets rows
- Mismatch detection — flags deliveries where submitted data doesn't match expected
- React frontend built for field use (minimal UI, works on low-end devices)
- Django REST backend handling auth, file processing, and Sheets/Drive API calls

## Stack

| | |
|---|---|
| Frontend | React |
| Backend | Django, Django REST Framework |
| Storage | Google Drive API |
| Records | Google Sheets API |
| Auth | Django auth + token-based |

## Getting Started

```bash
# Backend
cd backend
pip install -r requirements.txt

# Set up Google credentials
# Place your service account JSON at backend/credentials.json
# Configure SPREADSHEET_ID and DRIVE_FOLDER_ID in settings

python manage.py migrate
python manage.py runserver
```

```bash
# Frontend
cd customer-verification-app-frontend
npm install
npm start
```

## Configuration

The app expects a Google service account with Sheets and Drive access. Set the following in your environment or Django settings:

```
GOOGLE_CREDENTIALS_PATH=credentials.json
SPREADSHEET_ID=your_sheet_id
DRIVE_FOLDER_ID=your_folder_id
```
