import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

DATA_RANGE = 'B5:FA'

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Google Sheet configuration
SHEET_ID = '13PnC6wkTlmyjF4w2njUn4k7glxyb0nXX8D6yMIi5WuE'
SHEET_NAME = 'SCM FORWARD'

# Define header/data ranges
FULL_HEADER_RANGE = 'B3:FA3'
SENT_RANGE = 'W5:AV'
RECV_RANGE = 'BB5:CA'
SENT_HEADERS_RANGE = 'W3:AV3'
RECV_HEADERS_RANGE = 'BB3:CA3'

# Google Sheets API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials and authorize client
creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join('credentials', 'sheet_service_account.json'), scope
)
client = gspread.authorize(creds)

# Open the worksheet
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


# ✅ FETCH CUSTOMER DATA BY CID
def fetch_customer_row(cid):
    # Normalize incoming CID
    cid = cid.strip().upper()
    logger.info(f"🔎 Incoming CID to match: '{cid}'")

    # Fetch and normalize headers
    headers = [h.strip().upper() for h in sheet.get(FULL_HEADER_RANGE)[0] if h.strip()]
    logger.info(f"📌 Sheet Headers: {headers}")

    try:
        request_id_index = headers.index("REQUEST ID")
        name_index = headers.index("C/NEE NAME")
        project_index = headers.index("PROJECT NAME")
        address_index = headers.index("SHIPPING ADDRESS")
    except ValueError as e:
        logger.error(f"❌ Missing expected header: {e}")
        return None

    # Fetch data rows and column sets
    data = sheet.get(DATA_RANGE)
    sent_data = sheet.get(SENT_RANGE)
    recv_data = sheet.get(RECV_RANGE)
    sent_headers = [h.strip() for h in sheet.get(SENT_HEADERS_RANGE)[0]]
    recv_headers = [h.strip() for h in sheet.get(RECV_HEADERS_RANGE)[0]]

    for i, row in enumerate(data):
        # Defensive check
        if len(row) > request_id_index:
            sheet_cid = row[request_id_index].strip().upper()
            logger.info(f"[Row {i + 5}] Comparing Sheet CID='{sheet_cid}' with Input CID='{cid}'")

            if sheet_cid == cid:
                logger.info(f"✅ Matched CID row: {row}")

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

    logger.warning(f"⚠️ No matching CID found: {cid}")


    # Fetch data ranges
    data = sheet.get(DATA_RANGE)
    sent_data = sheet.get(SENT_RANGE)
    recv_data = sheet.get(RECV_RANGE)
    sent_headers = [h.strip() for h in sheet.get(SENT_HEADERS_RANGE)[0]]
    recv_headers = [h.strip() for h in sheet.get(RECV_HEADERS_RANGE)[0]]

    for i, row in enumerate(data):
        if len(row) > request_id_index:
            row_cid = row[request_id_index].strip().upper()
            logger.info(f"[Row {i + 5}] CID in sheet: '{row_cid}'")

            if row_cid == cid:
                logger.info(f"✅ Matched CID row: {row}")

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

    logger.warning(f"⚠️ No matching CID found: {cid}")

    # Fetch full data and indexed ranges
    data = sheet.get_all_values()
    sent_data = sheet.get(SENT_RANGE)
    recv_data = sheet.get(RECV_RANGE)
    sent_headers = sheet.get(SENT_HEADERS_RANGE)[0]
    recv_headers = sheet.get(RECV_HEADERS_RANGE)[0]

    # Normalize CID
    cid = cid.strip().upper()

    for i, row in enumerate(data[4:], start=5):  # row 5 = data[4]
        if len(row) > request_id_index and row[request_id_index].strip().upper() == cid:
            logger.info(f"✅ Matched CID row: {row}")

            name = row[name_index] if name_index < len(row) else "Unknown"
            project = row[project_index] if project_index < len(row) else "Unknown"
            address = row[address_index] if address_index < len(row) else ""

            sent_row = sent_data[i - 5] if i - 5 < len(sent_data) else []
            recv_row = recv_data[i - 5] if i - 5 < len(recv_data) else []

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

    logger.warning(f"⚠️ No matching CID found: {cid}")


# ✅ UPDATE RECEIVED DATA IN SHEET
def update_customer_delivery(cid, received_data):
    try:
        # Normalize received data keys
        received_data = {k.strip().upper(): v for k, v in received_data.items()}

        # Fetch all sheet data
        data = sheet.get_all_values()
        full_headers = [h.strip().upper() for h in data[2]]  # Row 3 is header
        request_id_index = full_headers.index("REQUEST ID")

        # Find the correct row number
        row_number = None
        for i, row in enumerate(data[4:], start=5):  # Skip first 4 rows, row 5 = index 4
            if len(row) > request_id_index and row[request_id_index].strip().upper() == cid.strip().upper():
                row_number = i
                break

        if not row_number:
            logger.warning(f"⚠️ No matching CID found for update: {cid}")
            return False

        # Fetch received headers
        recv_headers = [h.strip().upper() for h in sheet.get(RECV_HEADERS_RANGE)[0]]
        updated_row = []

        for header in recv_headers:
            qty = received_data.get(header, 0)
            updated_row.append(str(qty))

        range_to_update = f'BB{row_number}:CA{row_number}'
        sheet.update(range_to_update, [updated_row])
        logger.info(f"✅ Sheet updated at range: {range_to_update} for CID: {cid}")
        return True

    except Exception as e:
        logger.error(f"❌ Error while updating delivery data for CID {cid}: {e}")
        return False


# ✅ UPDATE VIDEO LINK IN COLUMN BA
def update_video_link(cid, video_url):
    try:
        data = sheet.get_all_values()
        headers = [h.strip().upper() for h in data[2]]  # Row 3 = index 2
        request_id_index = headers.index("REQUEST ID")
        video_col_index = 53  # BA = column 53 (1-indexed)

        for i, row in enumerate(data[4:], start=5):  # Row 5 = index 4
            if len(row) > request_id_index and row[request_id_index].strip().upper() == cid.strip().upper():
                sheet.update_cell(i, video_col_index, video_url)
                logger.info(f"🎥 Video link updated for CID {cid} in row {i}")
                return True

        logger.warning(f"⚠️ No matching row found for video update: {cid}")
        return False

    except Exception as e:
        logger.error(f"❌ Error updating video link: {e}")
        return False
