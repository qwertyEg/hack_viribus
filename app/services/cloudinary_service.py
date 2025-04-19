import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import current_app
import os
import requests
from io import BytesIO
import time
import hashlib
import hmac
import base64
import urllib.parse

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=current_app.config['CLOUDINARY_API_KEY'],
            api_secret=current_app.config['CLOUDINARY_API_SECRET']
        )

    def upload_file(self, file_path, folder_name):
        try:
            # Загружаем файл через SDK с настройками для публичного доступа
            result = cloudinary.uploader.upload(
                file_path,
                folder=f"materials/{folder_name}",
                resource_type="raw",
                use_filename=True,
                unique_filename=False,
                type="upload",
                access_mode="public",
                overwrite=True,
                invalidate=True,  # Инвалидируем кэш
                eager=[]  # Не создаем производные версии
            )
            
            return {
                'url': result['secure_url'],
                'public_id': result['public_id']
            }
        except Exception as e:
            raise Exception(f"Ошибка при загрузке файла в Cloudinary: {str(e)}")

    def delete_file(self, public_id):
        try:
            cloudinary.uploader.destroy(public_id, resource_type='raw')
        except Exception as e:
            raise Exception(f"Ошибка при удалении файла из Cloudinary: {str(e)}")

    def get_file_content(self, public_id):
        try:
            # Генерируем подписанный URL с временем жизни 1 час
            url, options = cloudinary.utils.cloudinary_url(
                public_id,
                resource_type='raw',
                type='upload',
                secure=True,
                sign_url=True,
                expires_at=int(time.time()) + 3600,  # URL действителен 1 час
                access_mode="public"  # Указываем публичный доступ
            )
            
            # Загружаем файл
            response = requests.get(url)
            response.raise_for_status()
            
            return BytesIO(response.content)
        except Exception as e:
            raise Exception(f"Ошибка при получении содержимого файла: {str(e)}") 