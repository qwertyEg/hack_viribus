from typing import Dict, Any
import openai
from flask import current_app

class ChatbotService:
    def __init__(self):
        self.api_key = current_app.config['OPENAI_API_KEY']
        openai.api_key = self.api_key
        self.model = "gpt-3.5-turbo"
        self.system_prompt = """Ты - помощник на образовательной платформе. 
        Ты должен помогать пользователям с вопросами по материалам, курсам и обучению.
        Отвечай кратко и по существу. Если не знаешь ответа, предложи обратиться к преподавателю."""

    def ask(self, query: str) -> Dict[str, Any]:
        """
        Обрабатывает запрос пользователя и возвращает ответ
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content.strip()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 