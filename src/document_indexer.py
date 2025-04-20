import os
from typing import List, Dict, Optional
import requests
from tqdm import tqdm
import json
from datetime import datetime

from src.cloudinary_client import CloudinaryClient
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore

class DocumentIndexer:
    def __init__(self, vector_store_path: str = "data/vector_store"):
        self.cloudinary = CloudinaryClient()
        self.processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.vector_store_path = vector_store_path
        self.processed_files = self._load_processed_files()

    def _load_processed_files(self) -> Dict:
        """
        Загружает информацию о уже обработанных файлах
        """
        processed_files_path = os.path.join(self.vector_store_path, "processed_files.json")
        if os.path.exists(processed_files_path):
            with open(processed_files_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_processed_files(self):
        """
        Сохраняет информацию об обработанных файлах
        """
        os.makedirs(self.vector_store_path, exist_ok=True)
        processed_files_path = os.path.join(self.vector_store_path, "processed_files.json")
        with open(processed_files_path, 'w') as f:
            json.dump(self.processed_files, f, indent=2)

    def _download_file(self, url: str) -> bytes:
        """
        Скачивает файл по URL
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def process_new_files(self):
        """
        Обрабатывает новые файлы из Cloudinary
        """
        files = self.cloudinary.list_files()
        new_files = []
        
        for file in files:
            file_id = file['public_id']
            if file_id not in self.processed_files:
                new_files.append(file)
        
        if not new_files:
            print("Нет новых файлов для обработки")
            return
        
        print(f"Найдено {len(new_files)} новых файлов")
        
        for file in tqdm(new_files, desc="Обработка файлов"):
            try:
                file_id = file['public_id']
                file_url = self.cloudinary.get_file_url(file_id)
                
                # Скачиваем файл
                content = self._download_file(file_url)
                
                # Обрабатываем документ
                text, formulas = self.processor.process_document(content, file_id)
                
                # Добавляем в векторную базу
                metadata = {
                    'file_id': file_id,
                    'file_name': file.get('filename', ''),
                    'processed_at': datetime.now().isoformat(),
                    'formulas': formulas
                }
                
                self.vector_store.add_documents([text], [metadata])
                
                # Обновляем информацию об обработанных файлах
                self.processed_files[file_id] = {
                    'processed_at': datetime.now().isoformat(),
                    'file_name': file.get('filename', '')
                }
                
            except Exception as e:
                print(f"Ошибка при обработке файла {file_id}: {e}")
                continue
        
        # Сохраняем обновленную векторную базу и информацию о файлах
        self.vector_store.save(self.vector_store_path)
        self._save_processed_files()

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Поиск по векторной базе данных
        """
        results = self.vector_store.search(query, k)
        return [
            {
                'text': text,
                'file_id': metadata['file_id'],
                'file_name': metadata['file_name'],
                'formulas': metadata.get('formulas', []),
                'score': score
            }
            for text, metadata, score in results
        ]

    def load_existing_index(self):
        """
        Загружает существующий индекс
        """
        if os.path.exists(os.path.join(self.vector_store_path, 'index.faiss')):
            self.vector_store.load(self.vector_store_path)
            print("Существующий индекс загружен")
        else:
            print("Индекс не найден, будет создан новый") 