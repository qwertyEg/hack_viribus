"""
Модуль для LLM чат-бота с использованием RAG
"""

import os
from typing import List, Dict, Optional, Tuple, Union
import time
from datetime import datetime
import json
import requests

# Импорты для работы с векторной базой данных
from src.document_indexer import DocumentIndexer
from src.prompts import SYSTEM_PROMPT, CLARIFICATION_PROMPT, RAG_PROMPT

class ChatBot:
    """
    Класс для чат-бота, использующего RAG для ответов на вопросы студентов
    """
    
    def __init__(
        self, 
        model_name: str = "ai-forever/FRED-T5-1.7B",
        vector_store_path: str = "data/vector_store",
        max_context_length: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_new_tokens: int = 512,
        enable_clarification: bool = True
    ):
        """
        Инициализация чат-бота
        
        Args:
            model_name: Название модели для генерации ответов
            vector_store_path: Путь к векторной базе данных
            max_context_length: Максимальная длина контекста
            temperature: Температура генерации (выше = более креативные ответы)
            top_p: Параметр top-p для генерации
            max_new_tokens: Максимальное количество новых токенов
            enable_clarification: Включить ли механизм уточняющих вопросов
        """
        self.model_name = model_name
        self.vector_store_path = vector_store_path
        self.max_context_length = max_context_length
        self.temperature = temperature
        self.top_p = top_p
        self.max_new_tokens = max_new_tokens
        self.enable_clarification = enable_clarification
        
        # Инициализация индексатора документов
        self.indexer = DocumentIndexer(vector_store_path=vector_store_path)
        self.indexer.load_existing_index()
        
        # Получаем API токен Hugging Face
        self.api_token = os.getenv("HUGGINGFACE_TOKEN")
        if not self.api_token:
            raise ValueError("Не найден токен Hugging Face. Пожалуйста, добавьте HUGGINGFACE_TOKEN в файл .env")
        
        # История диалогов (опционально)
        self.conversation_history = []
        
    def _format_context(self, search_results: List[Dict]) -> str:
        """
        Форматирование контекста из результатов поиска
        
        Args:
            search_results: Результаты поиска из векторной базы данных
            
        Returns:
            Отформатированный контекст
        """
        context = ""
        
        for i, result in enumerate(search_results, 1):
            file_name = result.get('file_name', 'Неизвестный файл')
            text = result.get('text', '')
            formulas = result.get('formulas', [])
            
            context += f"Документ {i}: {file_name}\n"
            context += f"Текст: {text}\n"
            
            if formulas:
                context += "Формулы:\n"
                for formula in formulas:
                    context += f"$${formula}$$\n"
            
            context += "\n"
        
        return context
    
    def _needs_clarification(self, query: str) -> Tuple[bool, str]:
        """
        Определяет, нужны ли уточняющие вопросы
        
        Args:
            query: Запрос пользователя
            
        Returns:
            (нужны ли уточнения, уточняющие вопросы)
        """
        if not self.enable_clarification:
            return False, ""
        
        # Проверяем длину запроса
        if len(query.split()) < 3:
            return True, "Пожалуйста, уточните ваш вопрос. О каком предмете или теме идет речь?"
        
        # Проверяем наличие вопросительного знака
        if "?" not in query:
            return True, "Это вопрос или утверждение? Пожалуйста, сформулируйте ваш запрос в виде вопроса."
        
        # Проверяем на слишком общие вопросы
        general_questions = ["что это", "как это", "объясни", "расскажи", "что такое"]
        if any(q in query.lower() for q in general_questions) and len(query.split()) < 5:
            return True, "Ваш вопрос слишком общий. Пожалуйста, уточните, о какой конкретно теме или концепции вы хотите узнать?"
        
        return False, ""
    
    def _generate_response(self, prompt: str) -> str:
        """
        Генерация ответа с помощью Hugging Face Inference API
        
        Args:
            prompt: Промпт для генерации
            
        Returns:
            Сгенерированный ответ
        """
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": self.max_new_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "return_full_text": False
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.model_name}",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Ошибка API Hugging Face: {response.text}")
        
        result = response.json()
        answer = result[0]["generated_text"].strip()
        
        end_time = time.time()
        print(f"Время генерации ответа: {end_time - start_time:.2f} секунд")
        
        return answer
    
    def ask(self, query: str, k: int = 5) -> Dict:
        """
        Ответ на вопрос пользователя
        
        Args:
            query: Вопрос пользователя
            k: Количество документов для поиска
            
        Returns:
            Словарь с ответом и метаданными
        """
        # Проверяем, нужны ли уточняющие вопросы
        needs_clarification, clarification_question = self._needs_clarification(query)
        
        if needs_clarification:
            return {
                "answer": clarification_question,
                "sources": [],
                "needs_clarification": True,
                "timestamp": datetime.now().isoformat()
            }
        
        # Поиск релевантных документов
        search_results = self.indexer.search(query, k=k)
        
        if not search_results:
            return {
                "answer": "К сожалению, я не нашел информации по вашему вопросу в базе данных. Пожалуйста, попробуйте переформулировать вопрос или уточните тему.",
                "sources": [],
                "needs_clarification": False,
                "timestamp": datetime.now().isoformat()
            }
        
        # Форматирование контекста
        context = self._format_context(search_results)
        
        # Формирование промпта для RAG
        rag_prompt = RAG_PROMPT.format(query=query, context=context)
        
        # Добавление системного промпта
        full_prompt = f"{SYSTEM_PROMPT}\n\n{rag_prompt}"
        
        # Генерация ответа
        answer = self._generate_response(full_prompt)
        
        # Подготовка источников
        sources = [
            {
                "file_name": result.get('file_name', 'Неизвестный файл'),
                "file_id": result.get('file_id', ''),
                "text": result.get('text', ''),
                "score": result.get('score', 0.0)
            }
            for result in search_results
        ]
        
        # Сохранение в историю (опционально)
        self.conversation_history.append({
            "query": query,
            "answer": answer,
            "sources": sources,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "answer": answer,
            "sources": sources,
            "needs_clarification": False,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_conversation_history(self, file_path: str = "data/conversation_history.json"):
        """
        Сохранение истории диалогов
        
        Args:
            file_path: Путь для сохранения истории
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        
        print(f"История диалогов сохранена в {file_path}")
    
    def load_conversation_history(self, file_path: str = "data/conversation_history.json"):
        """
        Загрузка истории диалогов
        
        Args:
            file_path: Путь к файлу с историей
        """
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            
            print(f"История диалогов загружена из {file_path}")
        else:
            print(f"Файл с историей диалогов не найден: {file_path}") 