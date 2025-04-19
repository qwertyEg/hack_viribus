from langchain_community.llms import HuggingFaceHub
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from vector_store import VectorStore
from watcher import Watcher
import threading
import os

class ChatBot:
    def __init__(self, 
                 hf_api_key: str,
                 pdf_dir: str = "data/pdfs",
                 vector_store_dir: str = "data/chroma"):
        self.vector_store = VectorStore(persist_directory=vector_store_dir)
        self.watcher = Watcher(pdf_dir, self.vector_store)
        
        self.llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",
            huggingfacehub_api_token=hf_api_key,
            model_kwargs={
                "temperature": 0.5,
                "max_length": 512,
                "top_p": 0.95,
                "repetition_penalty": 1.15
            },
            task="text-generation"
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.vector_store.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

        # Запускаем отслеживание изменений в отдельном потоке
        self.watcher_thread = threading.Thread(target=self.watcher.run)
        self.watcher_thread.daemon = True
        self.watcher_thread.start()

    def chat(self, query: str) -> str:
        result = self.chain({"question": query})
        answer = result["answer"]
        sources = [doc.metadata.get('source', 'Unknown') for doc in result.get('source_documents', [])]
        
        if sources:
            answer += "\n\nИсточники:\n" + "\n".join(f"- {src}" for src in set(sources))
        
        return answer

def main():
    hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not hf_api_key:
        print("Пожалуйста, установите переменную окружения HUGGINGFACE_API_KEY")
        return

    bot = ChatBot(hf_api_key=hf_api_key)
    print("Чат-бот готов к работе! Введите 'выход' для завершения.")

    while True:
        user_input = input("\nВы: ")
        if user_input.lower() == 'выход':
            break
            
        response = bot.chat(user_input)
        print(f"\nБот: {response}")

if __name__ == "__main__":
    main() 