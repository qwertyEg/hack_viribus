from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os.path
import pickle
import io

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveService:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        # Проверяем наличие сохраненных учетных данных
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        # Если учетные данные недействительны или отсутствуют
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError(
                        "Файл credentials.json не найден. "
                        "Пожалуйста, создайте учетные данные в Google Cloud Console "
                        "и сохраните их в файл credentials.json"
                    )
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Сохраняем учетные данные для следующего запуска
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('drive', 'v3', credentials=self.creds)

    def create_folder(self, folder_name):
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = self.service.files().create(body=file_metadata, fields='id').execute()
            return file.get('id')
        except Exception as e:
            raise Exception(f"Ошибка при создании папки: {str(e)}")

    def upload_file(self, file_path, folder_id):
        try:
            file_name = os.path.basename(file_path)
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            return file.get('id')
        except Exception as e:
            raise Exception(f"Ошибка при загрузке файла: {str(e)}")

    def download_file(self, file_id, save_path):
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.FileIO(save_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        except Exception as e:
            raise Exception(f"Ошибка при скачивании файла: {str(e)}")

    def list_files(self, folder_id=None):
        """Получение списка файлов в папке"""
        query = f"'{folder_id}' in parents" if folder_id else None
        results = self.service.files().list(
            q=query,
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        return results.get('files', []) 