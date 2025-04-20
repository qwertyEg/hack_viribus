import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import json
import os
from tqdm import tqdm

class VectorStore:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.metadata = []
        self.chunk_size = 512  # размер чанка в токенах
        self.chunk_overlap = 50  # перекрытие между чанками

    def add_documents(self, texts: List[str], metadata: List[Dict]):
        """
        Добавляет документы в векторную базу данных
        """
        # Разбиваем тексты на чанки
        chunks = []
        chunk_metadata = []
        
        for text, meta in zip(texts, metadata):
            text_chunks = self._split_text(text)
            chunks.extend(text_chunks)
            chunk_metadata.extend([meta] * len(text_chunks))

        # Создаем эмбеддинги для чанков
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        
        # Добавляем в индекс
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(chunks)
        self.metadata.extend(chunk_metadata)

    def _split_text(self, text: str) -> List[str]:
        """
        Разбивает текст на чанки с перекрытием
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks

    def search(self, query: str, k: int = 5) -> List[Tuple[str, Dict, float]]:
        """
        Поиск похожих документов
        """
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):  # Проверяем, что индекс валидный
                results.append((
                    self.documents[idx],
                    self.metadata[idx],
                    float(distance)
                ))
        
        return results

    def save(self, directory: str):
        """
        Сохраняет векторную базу данных
        """
        os.makedirs(directory, exist_ok=True)
        faiss.write_index(self.index, os.path.join(directory, 'index.faiss'))
        
        with open(os.path.join(directory, 'documents.json'), 'w', encoding='utf-8') as f:
            json.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f, ensure_ascii=False, indent=2)

    def load(self, directory: str):
        """
        Загружает векторную базу данных
        """
        self.index = faiss.read_index(os.path.join(directory, 'index.faiss'))
        
        with open(os.path.join(directory, 'documents.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.documents = data['documents']
            self.metadata = data['metadata'] 