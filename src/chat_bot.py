"""
Модуль для LLM чат-бота
"""

import os
import sys
import logging
from typing import Dict
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class ChatBot:
    """
    Класс для чат-бота, использующего Mistral API
    """
    
    def __init__(self):
        """
        Инициализация чат-бота
        """
        try:
            # Получаем API токен Mistral
            self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
            if not self.mistral_api_key:
                raise ValueError("Не найден токен Mistral API. Пожалуйста, добавьте MISTRAL_API_KEY в файл .env")
            
            logger.info("Чат-бот успешно инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации чат-бота: {str(e)}")
            raise

    def send_message_to_mistral(self, message: str, model: str = "mistral-small-2409") -> str:
        """
        Отправка сообщения в Mistral API
        
        Args:
            message: Текст сообщения
            model: Название модели
            
        Returns:
            Ответ от API
        """
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.mistral_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "max_tokens": 5000,
            "temperature": 0.9
        }
    
        try:
            logger.info(f"Отправка запроса к Mistral API: {message[:100]}...")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            if not response_data.get("choices"):
                raise ValueError("Нет choices в ответе API")
                
            answer = response_data["choices"][0]["message"]["content"].strip()
            logger.info(f"Получен ответ от Mistral API: {answer[:100]}...")
            return answer
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при обращении к Mistral API: {str(e)}")
            if response:
                logger.error(f"Полный ответ API: {response.text}")
            return "Извините, произошла ошибка при обращении к API. Пожалуйста, попробуйте позже."
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {str(e)}")
            return "Извините, произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."

    def ask(self, query: str) -> Dict:
        """
        Ответ на вопрос пользователя
        
        Args:
            query: Вопрос пользователя
            
        Returns:
            Словарь с ответом
        """
        try:
            logger.info(f"Обработка запроса: {query}")
            
            # Генерация ответа
            answer = self.send_message_to_mistral(query)
            
            return {
                "answer": answer,
                "sources": [],
                "needs_clarification": False,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {str(e)}", exc_info=True)
            return {
                "answer": "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.",
                "sources": [],
                "needs_clarification": False,
                "timestamp": datetime.now().isoformat()
            }

def main():
    if len(sys.argv) < 2:
        print("Usage: python chat_bot.py <message>")
        sys.exit(1)
        
    message = sys.argv[1]
    chatbot = ChatBot()
    response = chatbot.send_message_to_mistral(message)
    print(response)

if __name__ == "__main__":
    main() 