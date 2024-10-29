import json
import os
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Get the access token
def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    credentials.refresh(Request())
    return credentials.token


# Upload the file to Google Drive
def upload_to_drive(file_path):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    para = {
        "name": f"{file_path}.gpx",
        "parents": ["1VrlTjWDOQx-NNMGdbYAf7DPVH4i_dKBq"]
    }

    metadata = {
        'name': para['name'],
        'parents': para['parents']
    }

    # Open the file in binary mode
    with open(f"{file_path}.gpx", 'rb') as file:
        files = {
            'data': ('metadata', json.dumps(metadata), 'application/json; charset=UTF-8'),
            'file': (os.path.basename(file_path), file, 'application/gpx+xml')
        }

        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )

    if r.status_code == 200:
        file_info = r.json()
        print("Upload to drive done!")
        # print(f"File ID: {file_info['id']}, Web View Link: {file_info['webViewLink']}")
    else:
        print(f"Failed to upload file. Status code: {r.status_code}")
        print(f"Response: {r.text}")









