from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from flask import current_app
import os
import pickle
import io

class DriveService:
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    @staticmethod
    def get_credentials():
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', DriveService.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return creds
    
    @staticmethod
    def upload_file(file):
        creds = DriveService.get_credentials()
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': file.filename,
            'mimeType': file.content_type
        }
        
        media = MediaIoBaseUpload(
            io.BytesIO(file.read()),
            mimetype=file.content_type,
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        return file.get('webViewLink') 