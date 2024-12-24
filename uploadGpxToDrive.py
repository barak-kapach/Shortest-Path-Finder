"""
upload gpx file to google drive
"""
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request


def get_access_token():
    """
    Get access token from Google
    :return: access token
    """
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    credentials.refresh(Request())
    return credentials.token


def upload_to_drive(file_path):
    """
    Upload a file to Google Drive
    :param file_path: path to the file
    :return: None
    """
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "multipart/related; boundary=foo_bar_baz"
    }
    para = {
        "name": f"{file_path}.gpx",
        "parents": ["1VrlTjWDOQx-NNMGdbYAf7DPVH4i_dKBq"]
    }

    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': ('application/gpx+xml', open(f"./{file_path}.gpx", 'rb'))
    }

    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )

    if r.status_code == 200:
        file_info = r.json()
        print("Upload to drive done!")
        print(f"File ID: {file_info['id']}, Web View Link: {file_info['webViewLink']}")
    else:
        print(f"Failed to upload file. Status code: {r.status_code}")
        print(f"Response: {r.text}")


headers = {
    "Authorization": "Bearer ya29.a0AcM612w6PDwBsix7dZttDH3BNwMVYJ4Bz4LbhwnR3VoKtHuQzbLlu4c06dy52ZOKTJZ5kaX-AWiIgwJSeEFGexGY7-FOcHlRLMBbUqKZJaRJQbmA0ODnevtJBXJ4kUb_DtZjZen2lkCmFtUPt9DvoMQ150lgiPJhTnbrSfUxaCgYKAf4SARESFQHGX2MixokvuOpBFvRs1RebbEbvkw0175"}
para = {"name": "shortestPath.gpx",
        "parents": ["1VrlTjWDOQx-NNMGdbYAf7DPVH4i_dKBq"]}

files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': ('application/gpx+xml', open("./shortest_path.gpx", 'rb'))
}

r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)

# if __name__ == '__main__':
#     upload_to_drive("shortest_path")
