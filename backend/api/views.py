import logging
import os
import tempfile

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http import JsonResponse   # 👈 for health check

from googleapiclient.http import MediaFileUpload
from .drive_setup import drive_service
from .sheets import fetch_customer_row, update_customer_delivery, update_video_link

# Set up logging
logger = logging.getLogger(__name__)


# ✅ Health check for Render root "/"
@api_view(['GET'])
def health_check(request):
    return JsonResponse({"status": "ok"})


@api_view(['GET'])
def customer_details(request):
    cid = request.GET.get('cid')
    logger.info(f"🔍 Fetching details for CID: {cid}")

    if not cid:
        logger.error('CID not provided in the request')
        return Response({'error': 'CID not provided'}, status=400)

    row_data = fetch_customer_row(cid)
    logger.info(f"📦 Row Data Fetched: {row_data}")

    if not row_data:
        logger.warning(f"No data found for CID: {cid}")
        return Response({
            'cid': cid,
            'name': "Unknown",
            'project': "Unknown",
            'address': "",
            'items': []
        })

    response = {
        'cid': row_data['cid'],
        'name': row_data.get('name', 'Unknown'),
        'project': row_data.get('project', 'Unknown'),
        'address': row_data.get('address', ''),
        'items': row_data.get('items', [])
    }
    return Response(response)


@api_view(['POST'])
def confirm_delivery(request):
    data = request.data
    logger.info(f"✅ Confirmation Received: {data}")

    cid = data.get('cid')
    received = data.get('received')

    if not received or not cid:
        logger.error("Invalid data received: Missing CID or received quantities")
        return Response({'error': 'Invalid data'}, status=400)

    logger.info(f"Attempting to update Google Sheet for CID: {cid}")
    update_status = update_customer_delivery(cid, received)

    if update_status:
        logger.info(f"Successfully updated delivery for CID: {cid}")
        return Response({'status': 'Confirmation submitted successfully'})
    else:
        logger.error(f"Failed to update Google Sheets for CID: {cid}")
        return Response({'error': 'Failed to update data'}, status=500)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_proof_video(request):
    cid = request.data.get("cid")
    video = request.FILES.get("file")

    if not cid or not video:
        logger.error("❌ CID or video file missing in upload")
        return Response({"error": "CID or file missing"}, status=400)

    try:
        # Save video temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            for chunk in video.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        logger.info(f"📥 Saved temporary video at: {tmp_path}")

        # Upload to Shared Drive (requires supportsAllDrives=True)
        file_metadata = {
            'name': f"{cid}_proof.mp4",
            'parents': ['1k84g7K4IMvLMXJ6FQaMvWlRUNZ3_DmJj']  # warehouse_short folder ID
        }
        media = MediaFileUpload(tmp_path, mimetype='video/mp4')
        uploaded = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        ).execute()

        # Make file public
        drive_service.permissions().create(
            fileId=uploaded['id'],
            body={'type': 'anyone', 'role': 'reader'},
            supportsAllDrives=True
        ).execute()

        video_url = f"https://drive.google.com/file/d/{uploaded['id']}/view?usp=sharing"
        logger.info(f"✅ Video uploaded to Drive: {video_url}")

        # Update Google Sheet
        update_status = update_video_link(cid, video_url)
        if update_status:
            logger.info(f"📄 Video link updated in Google Sheet for CID: {cid}")
        else:
            logger.warning(f"⚠️ CID not found when trying to update video link")

        os.remove(tmp_path)
        return Response({"success": True, "video_url": video_url})

    except Exception as e:
        logger.exception("❌ Exception during video upload")
        return Response({"error": str(e)}, status=500)
