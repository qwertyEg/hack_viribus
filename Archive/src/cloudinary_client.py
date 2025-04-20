import cloudinary
import cloudinary.api
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class CloudinaryClient:
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET')
        )
        self.api = cloudinary.api

    def list_files(self, prefix: Optional[str] = None) -> List[Dict]:
        """
        Получает список всех файлов из Cloudinary
        """
        try:
            result = self.api.resources(
                type='upload',
                prefix=prefix,
                max_results=500
            )
            return result.get('resources', [])
        except Exception as e:
            print(f"Ошибка при получении списка файлов: {e}")
            return []

    def get_file_url(self, public_id: str) -> str:
        """
        Получает URL файла по его public_id
        """
        try:
            result = self.api.resource(public_id)
            return result.get('secure_url', '')
        except Exception as e:
            print(f"Ошибка при получении URL файла: {e}")
            return ''

    def get_file_info(self, public_id: str) -> Dict:
        """
        Получает информацию о файле по его public_id
        """
        try:
            return self.api.resource(public_id)
        except Exception as e:
            print(f"Ошибка при получении информации о файле: {e}")
            return {} 