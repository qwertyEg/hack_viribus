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
        print("Initializing CloudinaryService")
        print(f"Cloud name: {current_app.config['CLOUDINARY_CLOUD_NAME']}")
        print(f"API key: {current_app.config['CLOUDINARY_API_KEY']}")
        cloudinary.config(
            cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=current_app.config['CLOUDINARY_API_KEY'],
            api_secret=current_app.config['CLOUDINARY_API_SECRET']
        )

    def upload_file(self, file_path, folder_name):
        try:
            print(f"Starting file upload: {file_path}")
            print(f"Folder name: {folder_name}")
            
            # Определяем тип файла по расширению
            file_extension = os.path.splitext(file_path)[1].lower()
            print(f"File extension: {file_extension}")
            
            # Настройки для разных типов файлов
            upload_options = {
                'folder': f"materials/{folder_name}",
                'use_filename': True,
                'unique_filename': False,
                'type': "upload",
                'access_mode': "public",
                'overwrite': True,
                'invalidate': True,
                'eager': []
            }
            
            # Для видео добавляем специальные настройки
            if file_extension == '.mp4':
                print("Configuring video upload options")
                upload_options.update({
                    'resource_type': 'video',
                    'format': 'mp4',
                    'eager': [
                        {'format': 'mp4', 'video_codec': 'h264'}
                    ]
                })
            else:
                print("Configuring document upload options")
                # Для документов используем raw тип
                upload_options.update({
                    'resource_type': 'raw'
                })
            
            print(f"Upload options: {upload_options}")
            
            # Загружаем файл через SDK
            result = cloudinary.uploader.upload(
                file_path,
                **upload_options
            )
            
            print(f"Upload successful. Result: {result}")
            
            return {
                'url': result['secure_url'],
                'public_id': result['public_id']
            }
        except Exception as e:
            print(f"Error in upload_file: {str(e)}")
            raise Exception(f"Ошибка при загрузке файла в Cloudinary: {str(e)}")

    def delete_file(self, public_id):
        try:
            # Определяем тип файла по public_id
            resource_type = 'video' if public_id.endswith('.mp4') else 'raw'
            cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        except Exception as e:
            raise Exception(f"Ошибка при удалении файла из Cloudinary: {str(e)}")

    def get_file_content(self, public_id):
        try:
            # Определяем тип файла по public_id
            is_video = public_id.endswith('.mp4')
            
            if is_video:
                # Для видео получаем URL через CloudinaryVideo
                video = cloudinary.CloudinaryVideo(public_id)
                url = video.video_url(
                    secure=True,
                    sign_url=True,
                    expires_at=int(time.time()) + 3600
                )
            else:
                # Для документов используем стандартный подход
                url, options = cloudinary.utils.cloudinary_url(
                    public_id,
                    resource_type='raw',
                    type='upload',
                    secure=True,
                    sign_url=True,
                    expires_at=int(time.time()) + 3600
                )
            
            # Загружаем файл
            response = requests.get(url)
            response.raise_for_status()
            
            return BytesIO(response.content)
        except Exception as e:
            raise Exception(f"Ошибка при получении содержимого файла: {str(e)}")

    def get_file_url(self, public_id):
        """Получает URL файла для просмотра"""
        try:
            is_video = public_id.endswith('.mp4')
            
            if is_video:
                video = cloudinary.CloudinaryVideo(public_id)
                return video.video_url(
                    secure=True,
                    sign_url=True,
                    expires_at=int(time.time()) + 3600
                )
            else:
                url, options = cloudinary.utils.cloudinary_url(
                    public_id,
                    resource_type='raw',
                    type='upload',
                    secure=True,
                    sign_url=True,
                    expires_at=int(time.time()) + 3600
                )
                return url
        except Exception as e:
            raise Exception(f"Ошибка при получении URL файла: {str(e)}")

    def get_video_url(self, public_id):
        """Получает URL для воспроизведения видео"""
        try:
            # Создаем объект CloudinaryVideo
            video = cloudinary.CloudinaryVideo(public_id)
            
            # Получаем URL с подписью и сроком действия 1 час
            url = video.video_url(
                secure=True,
                sign_url=True,
                expires_at=int(time.time()) + 3600
            )
            
            return url
        except Exception as e:
            raise Exception(f"Ошибка при получении URL видео: {str(e)}") 