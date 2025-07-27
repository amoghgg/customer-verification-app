import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = '13PnC6wkTlmyjF4w2njUn4k7glxyb0nXX8D6yMIi5WuE'
SHEET_NAME = 'SCM FORWARD'
RANGE = 'B5:FA'

# Google Sheets API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials and authorize client
creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join('credentials', 'service_account.json'), scope
)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

def fetch_customer_row(cid):
    # Define ranges
    full_header_range = 'B3:FA3'
    data_range = 'B5:FA'
    sent_range = 'W5:AV'
    recv_range = 'BB5:CA'
    sent_headers_range = 'W3:AV3'
    recv_headers_range = 'BB3:CA3'

    # Fetch headers
    headers = [h.strip() for h in sheet.get(full_header_range)[0]]
    print("📌 Headers loaded:", headers)

    try:
        request_id_index = headers.index("Request ID")
        name_index = headers.index("C/nee Name")
        project_index = headers.index("Project Name")
        address_index = headers.index("Shipping Address")
    except ValueError as e:
        print("❌ Missing expected header:", e)
        return None

    # Fetch data
    data = sheet.get(data_range)
    sent_data = sheet.get(sent_range)
    recv_data = sheet.get(recv_range)
    sent_headers = sheet.get(sent_headers_range)[0]
    recv_headers = sheet.get(recv_headers_range)[0]

    # Debug: Show available request IDs
    print("🔍 All Request IDs in sheet:")
    for idx, row in enumerate(data):
        if len(row) > request_id_index:
            print(f"Row {idx + 1}: '{row[request_id_index]}'")

    # Normalize CID for matching
    cid = cid.strip().upper()

    for i, row in enumerate(data):
        if len(row) > request_id_index and row[request_id_index].strip().upper() == cid:
            print("✅ Matched CID row:", row)

            name = row[name_index] if name_index < len(row) else "Unknown"
            project = row[project_index] if project_index < len(row) else "Unknown"
            address = row[address_index] if address_index < len(row) else ""

            sent_row = sent_data[i] if i < len(sent_data) else []
            recv_row = recv_data[i] if i < len(recv_data) else []

            items = []
            for j in range(len(sent_headers)):
                item_name = sent_headers[j].strip() if j < len(sent_headers) else f"Item {j}"

                try:
                    sent_qty = int(sent_row[j]) if j < len(sent_row) and sent_row[j].strip().isdigit() else 0
                except:
                    sent_qty = 0

                try:
                    recv_qty = int(recv_row[j]) if j < len(recv_row) and recv_row[j].strip().isdigit() else 0
                except:
                    recv_qty = 0

                if sent_qty > 0 or recv_qty > 0:
                    items.append({
                        "name": item_name,
                        "sent": sent_qty,
                        "received": recv_qty
                    })

            return {
                "cid": cid,
                "name": name,
                "project": project,
                "address": address,
                "items": items
            }

    print("⚠️ No matching CID found:", cid)
    print("▶️ Total rows fetched from sheet:", len(data))
    print("▶️ Sample first 3 rows:")
    for row in data[:3]:
        print(row)

    return None
