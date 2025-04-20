import os
from dotenv import load_dotenv
from src.document_indexer import DocumentIndexer
from src.chat_bot import ChatBot

def main():
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем наличие необходимых переменных окружения
    required_env_vars = [
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_API_SECRET'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Ошибка: отсутствуют необходимые переменные окружения: {', '.join(missing_vars)}")
        return
    
    # Инициализируем индексатор документов
    indexer = DocumentIndexer()
    
    # Загружаем существующий индекс, если он есть
    indexer.load_existing_index()
    
    # Обрабатываем новые файлы
    indexer.process_new_files()
    
    # Пример поиска
    # query = "Что такое машинное обучение?"
    # results = indexer.search(query)
    # print("\nРезультаты поиска:")
    # for i, result in enumerate(results, 1):
    #     print(f"\nРезультат {i}:")
    #     print(f"Файл: {result['file_name']}")
    #     print(f"Текст: {result['text'][:200]}...")
    #     if result['formulas']:
    #         print("Формулы:")
    #         for formula in result['formulas']:
    #             print(f"$${formula}$$")
    #     print(f"Релевантность: {result['score']}")
    
    # Инициализируем чат-бота
    bot = ChatBot(
        model_name="ai-forever/FRED-T5-1.7B",  # Используем FRED-T5 от Сбера
        vector_store_path="data/vector_store",
        enable_clarification=True
    )
    
    # Примеры вопросов для демонстрации
    example_questions = [
        "Что такое машинное обучение?",
        "Объясни теорему Пифагора"
        # "Какие основные этапы развития человечества?",
        # "Что такое фотосинтез?"
    ]
    
    print("\nДемонстрация работы чат-бота:")
    print("=" * 50)
    
    for i, question in enumerate(example_questions, 1):
        print(f"\nВопрос {i}: {question}")
        print("-" * 50)
        
        # Получаем ответ от бота
        response = bot.ask(question)
        
        # Выводим ответ
        print(f"Ответ: {response['answer']}")
        
        # Выводим источники
        if response['sources']:
            print("\nИсточники:")
            for j, source in enumerate(response['sources'], 1):
                print(f"{j}. {source['file_name']}")
                print(f"   Релевантность: {source['score']}")
        
        print("=" * 50)
    
    # Сохраняем историю диалогов
    bot.save_conversation_history()

if __name__ == "__main__":
    main() 