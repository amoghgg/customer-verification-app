# backend/api/drive_utils.py

import os
from googleapiclient.http import MediaFileUpload
from .drive_setup import drive_service

def upload_video_to_drive(tmp_path, cid):
    """
    Uploads video to Google Drive and returns a public shareable link.
    """
    try:
        file_metadata = {
            'name': f"{cid}_proof.mp4"
        }
        media = MediaFileUpload(tmp_path, mimetype='video/mp4')
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Make it public
        drive_service.permissions().create(
            fileId=file['id'],
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Return public URL
        return f"https://drive.google.com/file/d/{file['id']}/view?usp=sharing"

    except Exception as e:
        print(f"❌ Error uploading video to Drive: {e}")
        return None
