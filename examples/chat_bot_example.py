#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пример использования чат-бота
"""

import os
import sys
import json
from datetime import datetime

# Добавляем корневую директорию проекта в путь для импортов
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chat_bot import ChatBot

def main():
    """
    Пример использования чат-бота
    """
    # Инициализируем чат-бота
    bot = ChatBot(
        model_name="mistralai/Mistral-7B-Instruct-v0.2",  # Можно заменить на другую модель
        vector_store_path="../data/vector_store",
        enable_clarification=True
    )
    
    # Загружаем историю диалогов, если она есть
    history_path = "../data/conversation_history.json"
    if os.path.exists(history_path):
        bot.load_conversation_history(history_path)
    
    print("Чат-бот готов к работе! Введите 'выход' для завершения.")
    print("Введите 'история' для просмотра истории диалогов.")
    print("Введите 'сохранить' для сохранения истории диалогов.")
    
    while True:
        # Получаем вопрос от пользователя
        query = input("\nВы: ")
        
        # Проверяем команды
        if query.lower() == 'выход':
            break
        elif query.lower() == 'история':
            if bot.conversation_history:
                print("\nИстория диалогов:")
                for i, item in enumerate(bot.conversation_history, 1):
                    print(f"{i}. Вопрос: {item['query']}")
                    print(f"   Ответ: {item['answer'][:100]}...")
                    print(f"   Время: {item['timestamp']}")
                    print()
            else:
                print("\nИстория диалогов пуста.")
            continue
        elif query.lower() == 'сохранить':
            bot.save_conversation_history(history_path)
            print("\nИстория диалогов сохранена.")
            continue
        
        # Получаем ответ от бота
        start_time = datetime.now()
        response = bot.ask(query)
        end_time = datetime.now()
        
        # Выводим ответ
        print(f"\nБот: {response['answer']}")
        
        # Выводим источники
        if response['sources']:
            print("\nИсточники:")
            for i, source in enumerate(response['sources'], 1):
                print(f"{i}. {source['file_name']}")
                print(f"   Релевантность: {source['score']}")
        
        # Выводим время ответа
        print(f"\nВремя ответа: {(end_time - start_time).total_seconds():.2f} секунд")

if __name__ == "__main__":
    main() 