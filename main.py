import os
import pickle
from googleapiclient.http import MediaFileUpload
from httplib2 import Credentials
from requests import Request
from Google import Create_Service
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
            
service = build('drive', 'v3', credentials=creds)

# Upload a file
file_metadata = {
    'name': 'photo.jpg',
    'parents': ['1wfehjduJAmq7SDodm90xTOVZRR1s_muH']
}

media_content = MediaFileUpload('photo.jpg', mimetype='image/jpg')

file = service.files().create(
    body=file_metadata,

    media_body=media_content
).execute()

print(file)
