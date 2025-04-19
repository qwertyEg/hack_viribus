import os
from dotenv import load_dotenv
from chat_bot import ChatBot

def main():
    load_dotenv()
    
    hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
    drive_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    
    if not hf_api_key or not drive_folder_id:
        print("Пожалуйста, установите переменные окружения HUGGINGFACE_API_KEY и GOOGLE_DRIVE_FOLDER_ID")
        return

    bot = ChatBot(
        hf_api_key=hf_api_key,
        drive_folder_id=drive_folder_id
    )

    print("Синхронизация файлов с Google Drive...")
    bot.sync_drive_files()
    print("Синхронизация завершена!")

    print("\nЧат-бот готов к работе! Введите 'выход' для завершения.")
    while True:
        user_input = input("\nВы: ")
        if user_input.lower() == 'выход':
            break
            
        response = bot.chat(user_input)
        print(f"\nБот: {response}")

if __name__ == "__main__":
    main() 